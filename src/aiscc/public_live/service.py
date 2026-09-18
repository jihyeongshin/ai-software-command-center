"""L2 atomic admission/reconciliation; all external authorities are fail-closed ports.

This module has no HTTP route, provider transport, activation or closure-proof
fabrication. Public DB and production workflow owners use separately scoped
repositories on the isolated synthetic public database.
"""

from __future__ import annotations

import hashlib
import secrets
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field, replace
from datetime import datetime
from typing import Protocol

from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.persistence.public_live import (
    Observation,
    ObservationKind,
    PersistRun,
    PublicLiveRepository,
    RunIdentity,
)
from aiscc.public_live.identity import AdmissionDenied, IdentityPolicy, request_identity
from aiscc.public_live.luna_profile import (
    conservative_request_liability_micro,
    hosted_luna_profile,
)
from aiscc.public_live.start_authority import StartContract
from aiscc.workflow.guards import TrustedGuardFact
from aiscc.workflow.kernel import WorkflowKernel
from aiscc.workflow.models import DecisionOutcome, TransitionRequest


@dataclass(frozen=True)
class Receipt:
    run_id: bytes
    replayed: bool
    read_capability: bytes | None = field(default=None, repr=False)
    read_expires_at: datetime | None = None


class AdmissionService:
    def __init__(
        self,
        repository: PublicLiveRepository,
        identity: IdentityPolicy,
        *,
        policy_digest: bytes,
        content_digest: bytes,
        start_contract: StartContract | None = None,
    ) -> None:
        if len(policy_digest) != 32 or len(content_digest) != 32:
            raise ValueError("POLICY_UNAVAILABLE")
        self.repository = repository
        self.identity = identity
        self.policy_digest = policy_digest
        self.content_digest = content_digest
        self.start_contract = start_contract

    async def admit(
        self, body: bytes, key: str, *, peer: str, headers: tuple[tuple[str, str], ...]
    ) -> Receipt:
        key_hash, payload = request_identity(body, key, self.policy_digest, self.content_digest)
        bucket = self.identity.bucket(peer, headers)
        identity = RunIdentity.generate()
        value = PersistRun(
            identity.run_id,
            self.identity.campaign_id,
            bucket,
            key_hash,
            hashlib.sha256(identity.read_capability).digest(),
            payload,
            1,
        )
        async with self.repository.transaction() as tx:
            binding = await tx.read_idempotency(self.identity.campaign_id, key_hash)
            if binding is not None:
                context = await tx.admission_context(self.identity.campaign_id, bucket)
                if context is None:
                    raise AdmissionDenied("POLICY_UNAVAILABLE")
                _, original_payload = request_identity(
                    body,
                    key,
                    bytes.fromhex(context["policy_digest"]),
                    bytes.fromhex(context["content_digest"]),
                )
                value = replace(value, payload_digest=original_payload)
            if self.start_contract is None:
                result = await tx.admit_checked(
                    value,
                    policy_digest=self.policy_digest,
                    content_digest=self.content_digest,
                    hmac_version=self.identity.key_version,
                )
            else:
                start_payload = dict(self.start_contract.payload)
                start_payload.update(
                    {
                        "contract_digest": self.start_contract.digest,
                        "policy_digest": self.policy_digest.hex(),
                        "content_digest": self.content_digest.hex(),
                        "idempotency_ref": key_hash.hex(),
                        "admitted_payload_hash": value.payload_digest.hex(),
                        "reservation_ref": "public-reservation:" + value.run_id.hex(),
                        "slot_generation": 1,
                        "requester_ref": hashlib.sha256(bucket).hexdigest(),
                    }
                )
                result = await tx.admit_checked_with_start(
                    value,
                    policy_digest=self.policy_digest,
                    content_digest=self.content_digest,
                    hmac_version=self.identity.key_version,
                    start_contract=start_payload,
                )
            expiry = None
            if "error" not in result and not result["replayed"]:
                ctx = await tx.run_context(identity.run_id)
                expiry = datetime.fromisoformat(ctx["read_expires"])
        # A denied clock-regression transaction must still commit its disabled gate.
        # A commit exception propagates without returning token/receipt or dispatch authority.
        if "error" in result:
            raise AdmissionDenied(result["error"])
        return Receipt(
            bytes.fromhex(result["run_id"]),
            result["replayed"],
            None if result["replayed"] else identity.read_capability,
            expiry,
        )


PreparedTransition = Callable[
    [str], Awaitable[tuple[TransitionRequest, tuple[TrustedGuardFact, ...]]]
]


class ProductionOwnerAdmission:
    """System-provided immutable preparation; production P1-4 remains the writer.

    The preparation callable must use the same request identity on retries. Its
    trusted owner-issued facts are verified by the kernel, never by public input.
    """

    def __init__(self, kernel: WorkflowKernel, prepare: PreparedTransition):
        self.kernel = kernel
        self.prepare = prepare

    async def admit(self, run_id: bytes) -> str:
        owner_id = "public-live-" + run_id.hex()
        request, facts = await self.prepare(owner_id)
        if (
            request.work_run_id != owner_id
            or request.runtime_mode is not RuntimeMode.PUBLIC_BOUNDED_LIVE
            or request.observed_state is not None
            or request.observed_state_version != 0
            or request.target_state is not WorkflowState.READY
        ):
            raise AdmissionDenied("OWNER_ADMISSION_INVALID")
        decision = await self.kernel.request_transition(request, facts)
        if decision.outcome is not DecisionOutcome.ADMITTED:
            raise AdmissionDenied("OWNER_ADMISSION_DENIED")
        owner = await self.kernel.verify_consistency(owner_id)
        if owner.runtime_mode is not RuntimeMode.PUBLIC_BOUNDED_LIVE:
            raise AdmissionDenied("OWNER_ADMISSION_INVALID")
        return owner_id


class DispatchAuthority(Protocol):
    async def authorize(self, run_id: bytes, ordinal: int, owner_id: str) -> tuple[int, int]:
        """Verify execution/security and envelope; return max micro-USD, owner version."""


class ReconciliationAuthority(Protocol):
    async def outcome(
        self, run_id: bytes, ordinal: int, evidence: object
    ) -> tuple[ObservationKind, int | None, bytes]:
        """Verify producer evidence, not caller-supplied success/cost assertions."""

    async def closure(self, run_id: bytes, generation: int, evidence: object) -> bytes | None:
        """Prove worker termination and every possible send ended/cannot escape. None denies."""


@dataclass(frozen=True)
class DispatchTicket:
    run_id: bytes
    ordinal: int
    generation: int
    max_cost: int


class ReconciliationService:
    def __init__(
        self,
        runtime: PublicLiveRepository,
        reconciler: PublicLiveRepository,
        owner: ProductionOwnerAdmission,
        *,
        dispatch: DispatchAuthority | None = None,
        evidence: ReconciliationAuthority | None = None,
    ):
        self.runtime = runtime
        self.reconciler = reconciler
        self.owner = owner
        self.dispatch = dispatch
        self.evidence = evidence

    async def bind(self, run_id: bytes) -> str:
        async with self.runtime.transaction() as tx:
            ctx = await tx.run_context(run_id)
            if ctx["outbox"]["state"] == "BOUND":
                binding = ctx["owner_binding"]
                if not isinstance(binding, str):
                    raise AdmissionDenied("OWNER_BINDING_INVALID")
                return binding
            if ctx["outbox"]["state"] != "PENDING" or tx.now >= datetime.fromisoformat(
                ctx["deadline"]
            ):
                raise AdmissionDenied("OUTBOX_CLOSED")
            generation = ctx["outbox"]["generation"]
        # Never acquire owner locks while holding public control/row locks.
        owner_id = await self.owner.admit(run_id)
        async with self.reconciler.transaction() as tx:
            current = await tx.run_context(run_id)
            if current["outbox"]["state"] == "BOUND" and current["owner_binding"] == owner_id:
                return owner_id
            if (
                current["outbox"]["state"] != "PENDING"
                or current["outbox"]["generation"] != generation
                or tx.now >= datetime.fromisoformat(current["deadline"])
            ):
                raise AdmissionDenied("OUTBOX_CLOSED")
            await tx.bind_owner(run_id, generation, owner_id)
        return owner_id

    async def authorize_dispatch(self, run_id: bytes, ordinal: int) -> DispatchTicket:
        if self.dispatch is None or ordinal not in (1, 2):
            raise AdmissionDenied("DISPATCH_AUTHORITY_UNAVAILABLE")
        async with self.runtime.transaction() as tx:
            ctx = await tx.run_context(run_id)
            if ctx["outbox"]["state"] != "BOUND":
                raise AdmissionDenied("OWNER_ADMISSION_REQUIRED")
            generation = ctx["outbox"]["generation"]
            owner_id = ctx["owner_binding"]
        maximum, version = await self.dispatch.authorize(run_id, ordinal, owner_id)
        if type(maximum) is not int or not 0 < maximum <= 200000 or type(version) is not int:
            raise AdmissionDenied("ENVELOPE_INVALID")
        async with self.runtime.transaction() as tx:
            await tx.mark_checked(run_id, generation, ordinal, maximum, version)
        return DispatchTicket(run_id, ordinal, generation, maximum)

    async def recover_unknown(self, run_id: bytes) -> None:
        async with self.runtime.transaction() as tx:
            ctx = await tx.run_context(run_id)
            if ctx["state"] == "UNKNOWN_OUTCOME":
                return
            if not any(d["state"] in ("STARTED", "UNKNOWN") for d in ctx["dispatches"]):
                raise AdmissionDenied("NO_AMBIGUOUS_MARKER")
            await tx.project_run(
                run_id,
                ctx["version"],
                "UNKNOWN_OUTCOME",
                hashlib.sha256(b"unknown-marker-v1" + run_id).digest(),
            )

    async def heartbeat(self, run_id: bytes) -> None:
        async with self.runtime.transaction() as tx:
            ctx = await tx.run_context(run_id)
            await tx.heartbeat(run_id, ctx["outbox"]["generation"])

    async def recover_lease(self, run_id: bytes) -> bool:
        """Supervisor calls on restart/heartbeat expiry; elapsed time never frees capacity."""
        async with self.runtime.transaction() as tx:
            ctx = await tx.run_context(run_id)
            slot = ctx["slot"]
            if slot is None or ctx["settlement"] is not None:
                return False
            if tx.now < datetime.fromisoformat(
                slot["expires_at"]
            ) and tx.now < datetime.fromisoformat(ctx["deadline"]):
                return False
            await tx.quarantine(run_id, slot["generation"])
            if ctx["state"] == "DISPATCH_STARTED" and any(
                d["state"] in ("STARTED", "UNKNOWN") for d in ctx["dispatches"]
            ):
                await tx.project_run(
                    run_id,
                    ctx["version"],
                    "UNKNOWN_OUTCOME",
                    hashlib.sha256(b"unknown-marker-v1" + run_id).digest(),
                )
        return True

    async def record_outcome(self, run_id: bytes, ordinal: int, evidence: object) -> None:
        if self.evidence is None:
            raise AdmissionDenied("EVIDENCE_AUTHORITY_UNAVAILABLE")
        kind, cost, proof = await self.evidence.outcome(run_id, ordinal, evidence)
        if kind not in (
            ObservationKind.KNOWN_SUCCESS,
            ObservationKind.KNOWN_FAILURE,
            ObservationKind.UNKNOWN,
        ):
            raise AdmissionDenied("OUTCOME_INVALID")
        if len(proof) != 32 or (cost is not None and (type(cost) is not int or cost < 0)):
            raise AdmissionDenied("OUTCOME_INVALID")
        async with self.reconciler.transaction() as tx:
            ctx = await tx.run_context(run_id)
            marker = next((d for d in ctx["dispatches"] if d["ordinal"] == ordinal), None)
            if marker is None:
                raise AdmissionDenied("NO_MARKER")
            value = marker["max_cost"] if cost is None or kind is ObservationKind.UNKNOWN else cost
            identity = hashlib.sha256(
                run_id + bytes((ordinal,)) + kind.value.encode() + proof
            ).digest()
            if cost is not None and cost > marker["max_cost"]:
                await tx.observe(
                    Observation(
                        secrets.token_bytes(16),
                        run_id,
                        identity,
                        ObservationKind.ABOVE_BOUND,
                        proof,
                        ordinal,
                        cost,
                    )
                )
                if ctx["settlement"] is None and not ctx["state"].startswith("FAILED_"):
                    await tx.project_run(run_id, ctx["version"], "FAILED_SAFETY", proof)
                return
            if ctx["settlement"] is not None:
                await tx.observe(
                    Observation(
                        secrets.token_bytes(16),
                        run_id,
                        identity,
                        ObservationKind.LATE_USAGE,
                        proof,
                        ordinal,
                        cost,
                    )
                )
                return
            if marker["state"] != "STARTED":
                if (
                    marker["state"] == kind.value
                    and marker["cost"] == value
                    and marker["proof"] == proof.hex()
                ):
                    return
                raise AdmissionDenied("OUTCOME_CONFLICT")
            await tx.record_outcome(run_id, ordinal, kind, value, proof, identity)
            if cost is None:
                await tx.observe(
                    Observation(
                        secrets.token_bytes(16),
                        run_id,
                        hashlib.sha256(b"missing-usage-v1" + identity).digest(),
                        ObservationKind.USAGE,
                        proof,
                        ordinal,
                        None,
                    )
                )
            if ctx["state"] == "DISPATCH_STARTED":
                target = (
                    "GOVERNANCE_PENDING"
                    if kind is ObservationKind.KNOWN_SUCCESS
                    else ("UNKNOWN_OUTCOME" if kind is ObservationKind.UNKNOWN else None)
                )
                if target:
                    await tx.project_run(run_id, ctx["version"], target, proof)

    async def close(self, run_id: bytes, evidence: object, *, target: str | None) -> bool:
        if self.evidence is None:
            raise AdmissionDenied("CLOSURE_AUTHORITY_UNAVAILABLE")
        async with self.runtime.transaction() as tx:
            ctx = await tx.run_context(run_id)
            if ctx["settlement"] is not None:
                generation = ctx["outbox"]["generation"] - 1
            elif ctx["outbox"]["fenced_at"] is None:
                await tx.fence(run_id, ctx["outbox"]["generation"])
                generation = ctx["outbox"]["generation"] + 1
            else:
                generation = ctx["outbox"]["generation"]
        proof = await self.evidence.closure(run_id, generation, evidence)
        if proof is None:
            return False  # Remains fenced/quarantined; no refund on lease/deadline alone.
        if len(proof) != 32:
            raise AdmissionDenied("CLOSURE_INVALID")
        async with self.reconciler.transaction() as tx:
            ctx = await tx.run_context(run_id)
            if ctx["settlement"] is not None:
                if ctx["settlement"]["proof"] != proof.hex() or (target and target != ctx["state"]):
                    raise AdmissionDenied("SETTLEMENT_CONFLICT")
                return False
            cost = sum(
                d["cost"] if d["state"] in ("KNOWN_SUCCESS", "KNOWN_FAILURE") else d["max_cost"]
                for d in ctx["dispatches"]
            )
            identity = hashlib.sha256(b"closure-v1" + run_id + proof).digest()
            await tx.admit_closure(run_id, generation, cost, proof, identity)
            await tx.settle(run_id, cost, proof)
            if target:
                await tx.project_run(run_id, ctx["version"], target, proof)
            elif ctx["state"] != "UNKNOWN_OUTCOME":
                raise AdmissionDenied("TERMINAL_PROJECTION_REQUIRED")
        return True


@dataclass(frozen=True, slots=True)
class UnknownProviderTarget:
    run_id: bytes
    operation_id: str
    outcome_event_id: str
    liability_micro: int


@dataclass(frozen=True, slots=True)
class UnknownProviderReconciliation:
    target: UnknownProviderTarget
    reconciled: bool
    state: str
    evidence_digest: str


class UnknownProviderReconciliationService:
    """Bridge canonical P1-5 UNKNOWN truth into the Public Live projection."""

    def __init__(self, reconciler: PublicLiveRepository) -> None:
        self.reconciler = reconciler

    async def select_exact_target(self) -> UnknownProviderTarget:
        async with self.reconciler.transaction() as tx:
            candidates = await tx.unknown_reconciliation_candidates()
        if len(candidates) != 1:
            raise AdmissionDenied("UNKNOWN_SMOKE_TARGET_IDENTITY_AMBIGUOUS")
        value = candidates[0]
        try:
            target = UnknownProviderTarget(
                bytes.fromhex(value["run_id"]),
                value["operation_id"],
                value["outcome_event_id"],
                value["liability_micro"],
            )
        except (KeyError, TypeError, ValueError) as error:
            raise AdmissionDenied("UNKNOWN_SMOKE_TARGET_IDENTITY_INVALID") from error
        expected = conservative_request_liability_micro(hosted_luna_profile())
        if (
            len(target.run_id) != 16
            or not target.operation_id
            or not target.outcome_event_id
            or type(target.liability_micro) is not int
            or target.liability_micro != expected
            or not 0 < target.liability_micro <= 200_000
        ):
            raise AdmissionDenied("UNKNOWN_PROVIDER_LIABILITY_NOT_PROVABLE")
        return target

    async def reconcile_target(
        self, target: UnknownProviderTarget
    ) -> UnknownProviderReconciliation:
        expected = conservative_request_liability_micro(hosted_luna_profile())
        if target.liability_micro != expected:
            raise AdmissionDenied("UNKNOWN_PROVIDER_LIABILITY_NOT_PROVABLE")
        async with self.reconciler.transaction() as tx:
            value = await tx.reconcile_unknown_provider(target.run_id)
        if (
            value.get("run_id") != target.run_id.hex()
            or value.get("operation_id") != target.operation_id
            or value.get("outcome_event_id") != target.outcome_event_id
            or value.get("liability_micro") != expected
            or value.get("state") != "FAILED_TIMEOUT"
            or not isinstance(value.get("evidence_digest"), str)
            or len(value["evidence_digest"]) != 64
            or type(value.get("reconciled")) is not bool
        ):
            raise AdmissionDenied("UNKNOWN_RECONCILIATION_RESULT_INVALID")
        return UnknownProviderReconciliation(
            target,
            value["reconciled"],
            value["state"],
            value["evidence_digest"],
        )

    async def reconcile_exact(self) -> UnknownProviderReconciliation:
        return await self.reconcile_target(await self.select_exact_target())
