"""Owner-only Stockroom capture orchestration core.

The runner sequences explicit injected owners.  It creates no authoritative
decision, evidence, Human result, Judgment, security grant, or runtime result.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.scenarios.driver import (
    PreparedStockroomDriver,
    StockroomCaptureProgressRef,
    StockroomCaptureResult,
    StockroomCaptureStatus,
    StockroomDriverRequest,
    StockroomRunPreparationBinding,
)
from aiscc.scenarios.enrollment import StockroomEnrollment

S1 = "stockroom-s1-normal"
S2 = "stockroom-s2-missing-evidence"
S3 = "stockroom-s3-policy-conflict"
S4 = "stockroom-s4-human-owned-claim"
_SCENARIOS = (S1, S2, S3, S4)


@dataclass(frozen=True, slots=True)
class OwnerCallResult:
    """Opaque projection returned by an authoritative owner adapter."""

    status: str
    owner_ref: str
    workflow_state: WorkflowState
    state_version: int
    reason: str | None = None


class StockroomCaptureOwnerPort(Protocol):
    async def initial_ready(self, prepared: PreparedStockroomDriver) -> OwnerCallResult: ...

    async def create_attempt(
        self, prepared: PreparedStockroomDriver, ready_ref: str
    ) -> OwnerCallResult: ...

    async def request_transition(
        self,
        prepared: PreparedStockroomDriver,
        *,
        target: WorkflowState,
        observed_state: WorkflowState,
        observed_version: int,
        authority_refs: tuple[str, ...],
    ) -> OwnerCallResult: ...

    async def seal_security_context(
        self, prepared: PreparedStockroomDriver, running_ref: str
    ) -> OwnerCallResult: ...

    async def authorize_runtime(
        self, prepared: PreparedStockroomDriver, security_context_ref: str
    ) -> OwnerCallResult: ...

    async def materialize(
        self, prepared: PreparedStockroomDriver, security_ref: str
    ) -> OwnerCallResult: ...

    async def execute(
        self, prepared: PreparedStockroomDriver, materialization_ref: str
    ) -> OwnerCallResult: ...

    async def submit_runtime_evidence(
        self, prepared: PreparedStockroomDriver, predecessor_ref: str
    ) -> OwnerCallResult: ...

    async def submit_static_policy_evidence(
        self, prepared: PreparedStockroomDriver, running_ref: str
    ) -> OwnerCallResult: ...

    async def evaluate_evidence(
        self, prepared: PreparedStockroomDriver, candidate_ref: str | None
    ) -> OwnerCallResult: ...

    async def submit_agent_human_claim(
        self, prepared: PreparedStockroomDriver, execution_ref: str
    ) -> OwnerCallResult: ...

    async def open_human_gate(
        self, prepared: PreparedStockroomDriver, evidence_ref: str
    ) -> OwnerCallResult: ...

    async def issue_judgment(
        self,
        prepared: PreparedStockroomDriver,
        *,
        judgment_status: str,
        evidence_ref: str | None,
    ) -> OwnerCallResult: ...

    async def create_policy_blocker(
        self, prepared: PreparedStockroomDriver, evidence_ref: str
    ) -> OwnerCallResult: ...


class StockroomCaptureRunner:
    def __init__(self, owners: StockroomCaptureOwnerPort) -> None:
        self._owners = owners

    async def run(self, prepared: PreparedStockroomDriver) -> StockroomCaptureResult:
        request = _validate_prepared(prepared)
        progress: list[StockroomCaptureProgressRef] = []
        state = WorkflowState.READY
        version = request.run_binding.expected_initial_state_version

        def record(owner: str, operation: str, result: OwnerCallResult) -> None:
            progress.append(
                StockroomCaptureProgressRef(
                    owner,
                    operation,
                    result.owner_ref,
                    result.status,
                    result.workflow_state,
                    result.state_version,
                )
            )

        def accept(
            owner: str,
            operation: str,
            result: OwnerCallResult,
            expected_status: str,
        ) -> str | None:
            record(owner, operation, result)
            if result.status != expected_status:
                return result.reason or result.status
            if result.workflow_state is not state or result.state_version != version:
                return "OWNER_RESULT_STATE_VERSION_MISMATCH"
            return None

        async def transition(
            operation: str,
            target: WorkflowState,
            authority_refs: tuple[str, ...],
        ) -> tuple[OwnerCallResult, bool]:
            nonlocal state, version
            observed_version = version
            result = await self._owners.request_transition(
                prepared,
                target=target,
                observed_state=state,
                observed_version=observed_version,
                authority_refs=authority_refs,
            )
            record("WORKFLOW", operation, result)
            if (
                result.status != "ADMITTED"
                or result.workflow_state is not target
                or result.state_version != observed_version + 1
            ):
                return result, False
            state, version = result.workflow_state, result.state_version
            return result, True

        async def stop(
            result: OwnerCallResult, reason: str | None = None
        ) -> StockroomCaptureResult:
            return StockroomCaptureResult(
                request.scenario_id,
                request.run_binding.run_id,
                request.run_binding.attempt_id,
                StockroomCaptureStatus.STOPPED,
                state,
                version,
                tuple(progress),
                stop_reason=reason or result.reason or result.status,
                retry_requires_new_attempt=True,
            )

        ready = await self._owners.initial_ready(prepared)
        record("WORKFLOW", "INITIAL_READY", ready)
        if (
            ready.status != "ADMITTED"
            or ready.workflow_state is not WorkflowState.READY
            or ready.state_version != request.run_binding.expected_initial_state_version
        ):
            return await stop(ready)
        state, version = ready.workflow_state, ready.state_version
        attempt = await self._owners.create_attempt(prepared, ready.owner_ref)
        if failure := accept("EXECUTION", "CREATE_ATTEMPT", attempt, "ADMITTED"):
            return await stop(attempt, failure)
        running, running_admitted = await transition(
            "READY_TO_RUNNING", WorkflowState.RUNNING, (attempt.owner_ref,)
        )
        if not running_admitted:
            return await stop(running)
        if request.scenario_id == S3:
            static = await self._owners.submit_static_policy_evidence(
                prepared, running.owner_ref
            )
            if failure := accept(
                "EVIDENCE", "SUBMIT_STATIC_POLICY", static, "ADMITTED"
            ):
                return await stop(static, failure)
            evidence = await self._owners.evaluate_evidence(prepared, static.owner_ref)
            if failure := accept("EVIDENCE", "EVALUATE", evidence, "SATISFIED"):
                return await stop(evidence, failure)
            blocker = await self._owners.create_policy_blocker(prepared, evidence.owner_ref)
            if failure := accept(
                "WORKFLOW", "CREATE_POLICY_BLOCKER", blocker, "ADMITTED"
            ):
                return await stop(blocker, failure)
            blocked, blocked_admitted = await transition(
                "RUNNING_TO_BLOCKED", WorkflowState.BLOCKED, (blocker.owner_ref,)
            )
            if not blocked_admitted:
                return await stop(blocked)
            return _complete(request, state, version, progress, evidence=(evidence.owner_ref,))

        security = await self._owners.seal_security_context(prepared, running.owner_ref)
        if failure := accept("SECURITY", "SEAL_CONTEXT", security, "ADMITTED"):
            return await stop(security, failure)
        grant = await self._owners.authorize_runtime(prepared, security.owner_ref)
        if failure := accept("SECURITY", "AUTHORIZE_RUNTIME", grant, "ADMITTED"):
            return await stop(grant, failure)

        materialized = await self._owners.materialize(prepared, grant.owner_ref)
        if failure := accept("RUNTIME", "MATERIALIZE", materialized, "ADMITTED"):
            return await stop(materialized, failure)
        execution = await self._owners.execute(prepared, materialized.owner_ref)
        if failure := accept("EXECUTION", "EXECUTE", execution, "COMPLETED"):
            return await stop(execution, failure)
        pending, pending_admitted = await transition(
            "RUNNING_TO_ADMISSION_PENDING",
            WorkflowState.ADMISSION_PENDING,
            (execution.owner_ref,),
        )
        if not pending_admitted:
            return await stop(pending)

        candidate_ref: str | None = None
        if request.scenario_id != S2:
            candidate = await self._owners.submit_runtime_evidence(prepared, pending.owner_ref)
            if failure := accept("EVIDENCE", "SUBMIT_RUNTIME", candidate, "ADMITTED"):
                return await stop(candidate, failure)
            candidate_ref = candidate.owner_ref
        evidence = await self._owners.evaluate_evidence(prepared, candidate_ref)
        expected_evidence = "UNSATISFIED" if request.scenario_id == S2 else "SATISFIED"
        if failure := accept("EVIDENCE", "EVALUATE", evidence, expected_evidence):
            return await stop(evidence, failure)

        if request.scenario_id == S4:
            claim = await self._owners.submit_agent_human_claim(prepared, execution.owner_ref)
            if failure := accept("HUMAN", "REJECT_AGENT_CLAIM", claim, "REJECTED"):
                return await stop(claim, failure)
            gate = await self._owners.open_human_gate(prepared, evidence.owner_ref)
            if failure := accept("HUMAN", "OPEN_GATE", gate, "PENDING"):
                return await stop(gate, failure)
            human_required, human_required_admitted = await transition(
                "TO_HUMAN_REQUIRED", WorkflowState.HUMAN_REQUIRED, (gate.owner_ref,)
            )
            if not human_required_admitted:
                return await stop(human_required)
            return _complete(
                request,
                state,
                version,
                progress,
                evidence=(evidence.owner_ref,),
                human_gate_ref=gate.owner_ref,
            )

        judgment_status = "HOLD_REWORK_REQUIRED" if request.scenario_id == S2 else "ACCEPTED"
        judgment = await self._owners.issue_judgment(
            prepared,
            judgment_status=judgment_status,
            evidence_ref=evidence.owner_ref if candidate_ref is not None else None,
        )
        if failure := accept("JUDGMENT", "ISSUE", judgment, "ADMITTED"):
            return await stop(judgment, failure)
        target = (
            WorkflowState.REWORK_REQUIRED
            if request.scenario_id == S2
            else WorkflowState.ACCEPTED
        )
        final, final_admitted = await transition(
            f"TO_{target.value}", target, (judgment.owner_ref,)
        )
        if not final_admitted:
            return await stop(final)
        return _complete(
            request,
            state,
            version,
            progress,
            evidence=(() if candidate_ref is None else (evidence.owner_ref,)),
            judgment_ref=judgment.owner_ref,
            retry_requires_new_attempt=request.scenario_id == S2,
        )


def _validate_prepared(prepared: PreparedStockroomDriver) -> StockroomDriverRequest:
    if type(prepared) is not PreparedStockroomDriver:
        raise ValueError("STOCKROOM_PREPARED_DRIVER_REQUIRED")
    request = prepared.request
    if (
        type(request) is not StockroomDriverRequest
        or type(request.enrollment) is not StockroomEnrollment
        or type(request.run_binding) is not StockroomRunPreparationBinding
        or request.runtime_mode is not RuntimeMode.OWNER_SELF_DOGFOOD
        or request.scenario_id not in _SCENARIOS
        or request.scenario_version != "1.0.0"
        or request.run_binding.run_id == request.run_binding.attempt_id
    ):
        raise ValueError("STOCKROOM_CAPTURE_BINDING_DENIED")
    return request


def _complete(
    request: StockroomDriverRequest,
    state: WorkflowState,
    version: int,
    progress: list[StockroomCaptureProgressRef],
    *,
    evidence: tuple[str, ...] = (),
    human_gate_ref: str | None = None,
    judgment_ref: str | None = None,
    retry_requires_new_attempt: bool = False,
) -> StockroomCaptureResult:
    return StockroomCaptureResult(
        request.scenario_id,
        request.run_binding.run_id,
        request.run_binding.attempt_id,
        StockroomCaptureStatus.COMPLETED,
        state,
        version,
        tuple(progress),
        evidence,
        human_gate_ref,
        None,
        judgment_ref,
        None,
        retry_requires_new_attempt,
    )
