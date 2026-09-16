"""Public Live V1 semantic orchestration. No HTTP or credential authority.

The database derives the next role. Only the server validator and reconciler
may supply decisions/outcomes. A committed ticket is consumed once, including
when the worker crashes before sending; restart must reconcile, never resend.
"""

from __future__ import annotations

import asyncio
import hashlib
from asyncio import wait_for
from dataclasses import dataclass, replace
from datetime import datetime
from enum import StrEnum
from typing import Protocol

from aiscc.persistence.public_live import PublicLiveRepository
from aiscc.providers.models import (
    ExecutionOperationOutcome,
    ProviderCall,
    ProviderResult,
    canonical_json_bytes,
)
from aiscc.providers.service import AgentExecutionService


class Decision(StrEnum):
    COMPLETE = "COMPLETE"
    VERIFY_REQUIRED = "VERIFY_REQUIRED"
    CORRECTABLE_DEFECT = "CORRECTABLE_DEFECT"
    UNSAFE_OR_UNCORRECTABLE = "UNSAFE_OR_UNCORRECTABLE"


@dataclass(frozen=True)
class Validation:
    decision: Decision
    proof: bytes
    defect: str | None = None


class ServerValidator(Protocol):
    async def validate(self, run: bytes, request: dict, result: ProviderResult) -> Validation: ...


class PipelineStore:
    """Separate runtime/reconciler logins, both using existing L1 transactions."""

    def __init__(self, runtime: PublicLiveRepository, reconciler: PublicLiveRepository):
        self.runtime, self.reconciler = runtime, reconciler

    async def enroll(self, run: bytes, price_verified: datetime) -> None:
        async with self.reconciler.transaction() as tx:
            await tx._call(
                "SELECT public_live_api.pipeline_enroll(:r,:v)", {"r": run, "v": price_verified}
            )

    async def context(self, run: bytes) -> dict:
        async with self.runtime.transaction() as tx:
            return await tx._call("SELECT public_live_api.pipeline_context(:r)", {"r": run})

    async def authorize(
        self, run: bytes, fingerprint: bytes, inputs: int, owner_version: int
    ) -> dict:
        async with self.runtime.transaction() as tx:
            result = await tx._call(
                "SELECT public_live_api.pipeline_request(:r,:f,:i,:v)",
                {"r": run, "f": fingerprint, "i": inputs, "v": owner_version},
            )
        return result  # Send authority exists only after transaction commit.

    async def outcome(
        self,
        run: bytes,
        ordinal: int,
        kind: str,
        *,
        closed: bool,
        tokens: int | None,
        cost: int | None,
        proof: bytes,
    ) -> None:
        async with self.reconciler.transaction() as tx:
            await tx._call(
                "SELECT public_live_api.pipeline_outcome(:r,:o,:k,:c,:t,:m,:p)",
                {
                    "r": run,
                    "o": ordinal,
                    "k": kind,
                    "c": closed,
                    "t": tokens,
                    "m": cost,
                    "p": proof,
                },
            )

    async def start(self, run: bytes, ordinal: int, fingerprint: bytes, version: int) -> None:
        async with self.runtime.transaction() as tx:
            await tx._call(
                "SELECT public_live_api.pipeline_start(:r,:o,:f,:v)",
                {"r": run, "o": ordinal, "f": fingerprint, "v": version},
            )

    async def validate(self, run: bytes, ordinal: int, validation: Validation) -> None:
        async with self.reconciler.transaction() as tx:
            await tx._call(
                "SELECT public_live_api.pipeline_validate(:r,:o,:d,:p,:f)",
                {
                    "r": run,
                    "o": ordinal,
                    "d": validation.decision.value,
                    "p": validation.proof,
                    "f": validation.defect,
                },
            )

    async def claim_tool(self, run: bytes, name: str, owner_version: int) -> None:
        async with self.runtime.transaction() as tx:
            await tx._call(
                "SELECT public_live_api.pipeline_tool(:r,:n,:v)",
                {"r": run, "n": name, "v": owner_version},
            )


class PublicProviderPipeline:
    """One conditional phase per invocation; there is no unconditional call loop.

    The composition root supplies server-built inputs, P1-5 scoped capabilities,
    and a server validator. Public HTTP input is never a provider call or decision.
    Transport exceptions/timeouts retain liability and cannot authorize a retry.
    """

    def __init__(self, store: PipelineStore, validator: ServerValidator):
        self.store, self.validator = store, validator

    async def step(
        self,
        run: bytes,
        call: ProviderCall,
        prepare_execution,
    ) -> ProviderResult | None:
        from aiscc.public_live.luna_profile import bind_call

        # Validate the entire immutable profile before creating any liability.
        prepared, input_bound = bind_call(call, role="PRIMARY")
        # Reserve framing for a DB-derived validation/defect instruction. Its
        # contents are added only after atomic role selection, never by HTTP.
        input_bound += 512
        if input_bound > 8000:
            raise ValueError("SEMANTIC_INPUT_LIMIT")
        if (await self.store.context(run))["owner_binding"] != call.work_run_id:
            raise ValueError("PUBLIC_OWNER_BINDING_DENIED")
        fingerprint = hashlib.sha256(
            canonical_json_bytes(
                {
                    "operation": call.operation_fingerprint,
                    "input": list(call.input_items),
                    "tools": list(call.tools),
                    "run": run.hex(),
                }
            )
        ).digest()
        ticket = await self.store.authorize(run, fingerprint, input_bound, call.state_version)
        if not ticket["send"]:
            return None
        if ticket["role"] != "PRIMARY":
            directive = {
                "role": "developer",
                "content": (
                    f"Public Live {ticket['role']} only. "
                    f"Server validation reference: {ticket['trigger_ref']}. "
                    f"Exact permitted defect: {ticket['defect'] or 'verification required'}. "
                    "Use only the fixed Stockroom scenario context."
                ),
            }
            prepared = replace(prepared, input_items=(*prepared.input_items, directive))
        prepared, _ = bind_call(prepared, role=ticket["role"])
        prepared = replace(prepared, call_ordinal=ticket["ordinal"])
        proof = hashlib.sha256(fingerprint + b"unknown").digest()
        try:
            execution, capabilities, secret_request = prepare_execution(prepared, ticket)
            if not isinstance(execution, AgentExecutionService):
                raise TypeError("P1_5_EXECUTION_SERVICE_REQUIRED")
            await self.store.start(run, ticket["ordinal"], fingerprint, call.state_version)
            result = await wait_for(
                asyncio.to_thread(
                    execution.execute_provider,
                    prepared,
                    capabilities=capabilities,
                    secret_request=secret_request,
                ),
                timeout=35,
            )
        except Exception:
            await self.store.outcome(
                run, ticket["ordinal"], "UNKNOWN", closed=False, tokens=None, cost=None, proof=proof
            )
            raise
        proof = bytes.fromhex(result.result_hash)
        tokens = result.usage.get("output_tokens")
        inputs = result.usage.get("input_tokens")
        # Cache-write inclusive conservative micro-dollar tariff: .25 input, 1.2 output.
        cost = None if inputs is None or tokens is None else (inputs * 5 + tokens * 24 + 19) // 20
        if inputs is not None and inputs > 8000:
            cost = 4401  # Above-bound evidence closes the control gate.
        success = result.outcome is ExecutionOperationOutcome.PROVIDER_COMPLETED
        # Only an explicit definitely-not-sent result is automatically conclusively
        # closed. Provider rejection alone is insufficient to prove no side effect.
        closed = result.outcome is ExecutionOperationOutcome.DEFINITELY_NOT_SENT
        kind = "KNOWN_SUCCESS" if success else "KNOWN_FAILURE" if closed else "UNKNOWN"
        if closed:
            tokens, cost = 0, 0
        await self.store.outcome(
            run, ticket["ordinal"], kind, closed=closed, tokens=tokens, cost=cost, proof=proof
        )
        if success:
            if result.tool_call is not None:
                # A tool request is not a final text result. Composition must
                # use dispatch_tool and validate its server-owned output first.
                return result
            validation = await self.validator.validate(run, ticket, result)
            await self.store.validate(run, ticket["ordinal"], validation)
        return result

    async def dispatch_tool(
        self, run: bytes, candidate, broker, *, policy, capabilities, dispatcher, dispatch_context
    ):
        from aiscc.contracts.workflow import RuntimeMode

        if candidate.name != "stockroom_summary":
            raise ValueError("TOOL_SCOPE_DENIED")
        broker.validate_candidate(
            candidate,
            mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
            profile_id="public-live-luna-v1",
            scenario_id="stockroom-s1-normal",
            dispatch_context=dispatch_context,
        )
        if (await self.store.context(run))["owner_binding"] != dispatch_context.work_run_id:
            raise ValueError("PUBLIC_OWNER_BINDING_DENIED")
        await self.store.claim_tool(run, candidate.name, dispatch_context.state_version)
        return broker.dispatch_candidate(
            candidate,
            mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
            profile_id="public-live-luna-v1",
            scenario_id="stockroom-s1-normal",
            policy=policy,
            capabilities=capabilities,
            dispatcher=dispatcher,
            dispatch_context=dispatch_context,
        )
