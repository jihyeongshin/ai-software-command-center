"""Operator-only hosted L5 proof configuration. This module exposes no HTTP route."""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import urllib.request
from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from threading import Event
from types import MappingProxyType
from urllib.parse import urlsplit

from aiscc.providers.models import ExecutionOperationOutcome, ProviderCall, ProviderResult
from aiscc.public_live.provider_pipeline import PipelineStore
from aiscc.runtime.contracts import RuntimeOutcomeStatus
from aiscc.runtime.process import BoundedProcessRunner


class FaultPoint(StrEnum):
    BEFORE_DISPATCH = "before-dispatch"
    AFTER_DISPATCH = "after-dispatch"
    KNOWN_CLOSED_FAILURE = "known-closed-failure"
    SANDBOX_TERMINATION = "sandbox-termination"


@dataclass(frozen=True)
class HostedProofSettings:
    campaign: str
    provider_double_url: str
    fake_secret_class: str
    admission_disabled: bool
    local_transport: bool = False

    @classmethod
    def from_environment(cls, environ: Mapping[str, str]) -> HostedProofSettings:
        campaign = environ.get("AISCC_HOSTED_L5_PROOF_CAMPAIGN", "")
        target = environ.get("AISCC_HOSTED_L5_PROVIDER_DOUBLE_URL", "")
        secret_class = environ.get("AISCC_HOSTED_L5_FAKE_SECRET_CLASS", "")
        disabled = environ.get("AISCC_PUBLIC_LIVE_ADMISSION", "DISABLED") == "DISABLED"
        local = environ.get("AISCC_HOSTED_L5_PROOF_LOCAL_TRANSPORT") == "ENABLED"
        parsed = urlsplit(target)
        if (
            re.fullmatch(r"proof-[a-z0-9]{16,64}", campaign) is None
            or parsed.scheme != "http"
            or not parsed.hostname
            or not (
                parsed.hostname.endswith(".railway.internal")
                or (local and parsed.hostname == "127.0.0.1")
            )
            or parsed.username
            or parsed.password
            or parsed.query
            or parsed.fragment
            or secret_class != "SYNTHETIC_SENTINEL_ONLY"
            or not disabled
            or "AISCC_OPENAI_API_KEY" in environ
            or "OPENAI_API_KEY" in environ
        ):
            raise ValueError("HOSTED_L5_PROOF_CONFIGURATION_DENIED")
        return cls(campaign, target, secret_class, disabled, local)


@dataclass(frozen=True)
class ProofExpectation:
    fault_point: FaultPoint
    durable_phase: str
    outcome: str
    provider_receipts: int
    retry_allowed: bool
    quarantine_required: bool


@dataclass(frozen=True)
class OperatorProofResult:
    run_id: str
    observation: ProofExpectation
    initializer_executed: bool
    durable_claim_executed: bool
    supervisor_executed: bool = False


def expectation(fault_point: FaultPoint) -> ProofExpectation:
    values = {
        FaultPoint.BEFORE_DISPATCH: ProofExpectation(
            fault_point, "OUTCOME_KNOWN", "DEFINITELY_NOT_SENT", 0, False, False
        ),
        FaultPoint.AFTER_DISPATCH: ProofExpectation(
            fault_point,
            "OUTCOME_UNKNOWN",
            "TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME",
            1,
            False,
            True,
        ),
        FaultPoint.KNOWN_CLOSED_FAILURE: ProofExpectation(
            fault_point, "OUTCOME_KNOWN", "DEFINITELY_NOT_SENT", 1, True, False
        ),
        FaultPoint.SANDBOX_TERMINATION: ProofExpectation(
            fault_point, "OUTCOME_KNOWN", "DEFINITELY_NOT_SENT", 0, False, False
        ),
    }
    return values[fault_point]


async def execute_provider_fault(
    store: PipelineStore,
    *,
    run_id: bytes,
    owner_version: int,
    fault_point: FaultPoint,
) -> ProofExpectation:
    """Drive a synthetic fault through the existing durable provider authority."""
    if fault_point is FaultPoint.SANDBOX_TERMINATION:
        raise ValueError("SANDBOX_TERMINATION_REQUIRES_PROCESS_SUPERVISOR")
    fingerprint = hashlib.sha256(b"hosted-l5-proof\0" + fault_point.value.encode()).digest()
    ticket = await store.authorize(run_id, fingerprint, 8000, owner_version)
    if not ticket.get("send") or ticket.get("ordinal") != 1:
        raise RuntimeError("HOSTED_L5_PROOF_SEND_AUTHORITY_DENIED")
    proof = hashlib.sha256(fingerprint + b"synthetic-fault").digest()
    if fault_point is FaultPoint.BEFORE_DISPATCH:
        await store.outcome(run_id, 1, "KNOWN_FAILURE", closed=True, tokens=0, cost=0, proof=proof)
    else:
        await store.start(run_id, 1, fingerprint, owner_version)
        if fault_point is FaultPoint.AFTER_DISPATCH:
            await store.outcome(
                run_id, 1, "UNKNOWN", closed=False, tokens=None, cost=None, proof=proof
            )
        else:
            await store.outcome(
                run_id, 1, "KNOWN_FAILURE", closed=True, tokens=0, cost=0, proof=proof
            )
    return expectation(fault_point)


async def run_operator_proof(
    environ: Mapping[str, str], fault_point: FaultPoint
) -> OperatorProofResult:
    """Run the operator proof through the production initializer and claim owners."""
    from aiscc.public_live.initializer import create_initializer
    from aiscc.public_live.worker import create_worker

    settings = HostedProofSettings.from_environment(environ)
    if not settings.admission_disabled:
        raise ValueError("HOSTED_L5_PROOF_ADMISSION_MUST_BE_DISABLED")
    initializer = create_initializer(
        {
            "AISCC_PUBLIC_LIVE_START_DATABASE_URL": environ.get(
                "AISCC_PUBLIC_LIVE_START_DATABASE_URL", ""
            )
        }
    )
    worker = create_worker(environ)
    adapter = QAProviderDoubleAdapter(settings.provider_double_url, settings.campaign, fault_point)
    worker.adapter = adapter  # distinct synthetic proof transport, never the hosted OpenAI adapter
    previous = os.environ.get("AISCC_OPENAI_API_KEY")
    try:
        await initializer.repository.verify_runtime_identity()
        await worker.authority.repository.verify_runtime_identity()
        initialized = await initializer.step()
        if not initialized:
            raise RuntimeError("HOSTED_L5_PROOF_START_CANDIDATE_REQUIRED")
        await worker.authority.register()
        claim = await worker.authority.claim_next_work()
        if claim is None:
            raise RuntimeError("HOSTED_L5_PROOF_DURABLE_CLAIM_REQUIRED")
        from aiscc.public_live.worker_authority import ActiveClaim

        active = ActiveClaim(claim)
        if fault_point is FaultPoint.BEFORE_DISPATCH:
            os.environ["AISCC_OPENAI_API_KEY"] = ""
        else:
            os.environ["AISCC_OPENAI_API_KEY"] = "synthetic-hosted-proof-only"
        supervisor = False
        if fault_point is FaultPoint.SANDBOX_TERMINATION:
            cancel = Event()
            cancel.set()
            outcome = await __import__("asyncio").to_thread(
                BoundedProcessRunner._run_unchecked,
                (sys.executable, "-c", "import time; time.sleep(30)"),
                timeout_seconds=5,
                max_attempts=1,
                cancel=cancel,
                security_reason="HOSTED_L5_OPERATOR_PROOF",
                security_provenance={"proof": "sandbox-supervisor"},
            )
            supervisor = (
                outcome.status is RuntimeOutcomeStatus.CANCELLED
                and outcome.cleanup_complete
                and outcome.executed
            )
            if not supervisor:
                raise RuntimeError("HOSTED_L5_SUPERVISOR_PROOF_FAILED")
        else:
            await worker.execute_claim(active)
        receipts = adapter.observe_receipts()
        values = {
            FaultPoint.BEFORE_DISPATCH: ("OUTCOME_KNOWN", "DEFINITELY_NOT_SENT", False, False),
            FaultPoint.AFTER_DISPATCH: (
                "OUTCOME_UNKNOWN",
                "TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME",
                False,
                True,
            ),
            FaultPoint.KNOWN_CLOSED_FAILURE: (
                "OUTCOME_KNOWN",
                "DEFINITELY_NOT_SENT",
                True,
                False,
            ),
            FaultPoint.SANDBOX_TERMINATION: (
                "OUTCOME_KNOWN",
                "DEFINITELY_NOT_SENT",
                False,
                False,
            ),
        }
        phase, outcome_name, retry, quarantine = values[fault_point]
        observed = ProofExpectation(fault_point, phase, outcome_name, receipts, retry, quarantine)
        if not quarantine:
            await worker.authority.repository.release(active.ref, "KNOWN_STEP_CLOSED")
        return OperatorProofResult(claim.run_id.hex(), observed, True, True, supervisor)
    finally:
        if previous is None:
            os.environ.pop("AISCC_OPENAI_API_KEY", None)
        else:
            os.environ["AISCC_OPENAI_API_KEY"] = previous
        await initializer.close()
        await worker.close()


class QAProviderDoubleAdapter:
    """Operator-only private HTTP transport with observed durable receipt count."""

    def __init__(self, base_url: str, campaign: str, fault: FaultPoint) -> None:
        self.base_url = base_url.rstrip("/")
        self.campaign = campaign
        self.fault = fault
        self.invocation_count = 0
        self._last_observed = 0
        self.calls: list[ProviderCall] = []

    def call(self, call: ProviderCall, *, secret: str) -> ProviderResult:
        if secret != "synthetic-hosted-proof-only":
            raise ValueError("QA_SYNTHETIC_SECRET_REQUIRED")
        self.invocation_count += 1
        self.calls.append(call)
        if self.fault is FaultPoint.KNOWN_CLOSED_FAILURE and self.invocation_count == 1:
            return ProviderResult(
                call.operation_id,
                "closed-before-send",
                ExecutionOperationOutcome.DEFINITELY_NOT_SENT,
                None,
                (),
                None,
                None,
                MappingProxyType({}),
                None,
                hashlib.sha256(b"definitely-not-sent\0" + call.operation_id.encode()).hexdigest(),
            )
        body = json.dumps(
            {
                "campaign": self.campaign,
                "operation_id": call.operation_id,
                "fault": self.fault.value,
            }
        ).encode()
        request = urllib.request.Request(
            self.base_url + "/responses",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=5) as response:  # noqa: S310 - fixed private proof URL
            payload = json.loads(response.read())
        count = payload.get("receipt_count")
        if type(count) is not int or count < 1:
            raise RuntimeError("QA_PROVIDER_RECEIPT_INVALID")
        self._last_observed = count
        if self.fault is FaultPoint.AFTER_DISPATCH:
            raise TimeoutError("synthetic response withheld after receipt")
        outcome = ExecutionOperationOutcome.PROVIDER_COMPLETED
        output = ({"type": "message", "content": [{"type": "output_text", "text": "synthetic"}]},)
        return ProviderResult(
            call.operation_id,
            "closed" if not output else "completed",
            outcome,
            f"proof-{count}",
            output,
            "synthetic" if output else None,
            None,
            MappingProxyType({"input_tokens": 1, "output_tokens": 1} if output else {}),
            None,
            hashlib.sha256(body + str(count).encode()).hexdigest(),
        )

    def observe_receipts(self) -> int:
        request = urllib.request.Request(
            f"{self.base_url}/receipts?campaign={self.campaign}", method="GET"
        )
        with urllib.request.urlopen(request, timeout=5) as response:  # noqa: S310 - fixed private proof URL
            payload = json.loads(response.read())
        count = payload.get("receipt_count")
        if type(count) is not int or count < self._last_observed:
            raise RuntimeError("QA_PROVIDER_RECEIPT_OBSERVATION_INVALID")
        return count
