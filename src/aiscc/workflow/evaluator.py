from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.workflow.guards import (
    GUARD_OWNER_POLICY,
    FutureOwnerGuardVerifier,
    P1_4GuardAuthority,
    TrustedGuardFact,
    p1_4_authority_matches_fact,
    verifier_matches_fact,
)
from aiscc.workflow.matrix import TRANSITION_MATRIX
from aiscc.workflow.models import (
    DecisionOutcome,
    DecisionReason,
    GuardId,
    GuardObservation,
    GuardSemanticOwner,
    TransitionDecision,
    TransitionEvaluation,
    TransitionRequest,
    WorkRun,
)

KERNEL_VERSION = "AISCC-P1-4-KERNEL-V1"


class TransitionEvaluator:
    def __init__(
        self,
        p1_4_guard_authority: P1_4GuardAuthority,
        future_owner_verifiers: tuple[FutureOwnerGuardVerifier, ...] = (),
    ) -> None:
        self._p1_4_guard_authority = p1_4_guard_authority
        self._future_owner_verifiers: dict[GuardSemanticOwner, FutureOwnerGuardVerifier] = {}
        for verifier in future_owner_verifiers:
            if verifier.semantic_owner is GuardSemanticOwner.P1_4_SYSTEM:
                raise ValueError("P1-4 authority cannot be replaced by an external verifier")
            if verifier.semantic_owner in self._future_owner_verifiers:
                raise ValueError("one future-owner verifier is allowed per semantic owner")
            self._future_owner_verifiers[verifier.semantic_owner] = verifier

    def evaluate(
        self,
        *,
        request: TransitionRequest,
        current: WorkRun | None,
        facts: tuple[TrustedGuardFact, ...],
        now: datetime | None = None,
    ) -> tuple[TransitionEvaluation, TransitionDecision]:
        evaluated_at = now or datetime.now(UTC)
        current_state = current.state if current is not None else None
        current_version = current.state_version if current is not None else 0
        current_matches = (
            request.observed_state is current_state
            and request.observed_state_version == current_version
        )
        observations: list[GuardObservation] = [
            GuardObservation(
                guard_id=GuardId.G_CURRENT,
                semantic_owner=GuardSemanticOwner.P1_4_SYSTEM,
                satisfied=current_matches,
                reason="CURRENT_STATE_VERSION_MATCH" if current_matches else "STALE_REQUEST",
                authority_ref="AISCC_SYSTEM_CURRENT_PROJECTION",
                bound_refs=(),
            )
        ]

        fact_by_guard: dict[GuardId, TrustedGuardFact] = {}
        for supplied_fact in facts:
            if self._validates(supplied_fact, request):
                fact_by_guard.setdefault(supplied_fact.guard_id, supplied_fact)

        required = TRANSITION_MATRIX.get((current_state, request.target_state))
        missing: list[GuardId] = []
        if required is not None:
            for guard_id in sorted(required, key=str):
                trusted_fact = fact_by_guard.get(guard_id)
                if trusted_fact is None:
                    missing.append(guard_id)
                    observations.append(
                        GuardObservation(
                            guard_id=guard_id,
                            semantic_owner=GUARD_OWNER_POLICY[guard_id],
                            satisfied=False,
                            reason="TRUSTED_GUARD_FACT_MISSING",
                            authority_ref="NONE",
                            bound_refs=(),
                        )
                    )
                else:
                    observations.append(
                        GuardObservation(
                            guard_id=trusted_fact.guard_id,
                            semantic_owner=trusted_fact.semantic_owner,
                            satisfied=trusted_fact.satisfied,
                            reason=trusted_fact.reason,
                            authority_ref=trusted_fact.authority_ref,
                            bound_refs=trusted_fact.bound_refs,
                        )
                    )

        reason = self._reason(
            request=request,
            current=current,
            current_matches=current_matches,
            required=required,
            observations=observations,
            missing=missing,
        )
        outcome = (
            DecisionOutcome.ADMITTED
            if reason is DecisionReason.ADMITTED
            else DecisionOutcome.DENIED
        )
        resulting_state = (
            request.target_state if outcome is DecisionOutcome.ADMITTED else current_state
        )
        resulting_version = (
            current_version + 1 if outcome is DecisionOutcome.ADMITTED else current_version
        )
        evaluation_id = str(uuid4())
        evaluation = TransitionEvaluation(
            transition_evaluation_id=evaluation_id,
            transition_request_id=request.transition_request_id,
            authoritative_state=current_state,
            authoritative_state_version=current_version,
            guards=tuple(observations),
            missing_guards=tuple(missing),
            evaluated_at=evaluated_at,
        )
        decision = TransitionDecision(
            transition_decision_id=str(uuid4()),
            transition_evaluation_id=evaluation_id,
            transition_request_id=request.transition_request_id,
            outcome=outcome,
            reason=reason,
            resulting_state=resulting_state,
            resulting_state_version=resulting_version,
            admitting_owner="AISCC_SYSTEM_TRANSITION_AUTHORITY",
            kernel_version=KERNEL_VERSION,
            decided_at=evaluated_at,
        )
        return evaluation, decision

    def _validates(self, fact: TrustedGuardFact, request: TransitionRequest) -> bool:
        expected_owner = GUARD_OWNER_POLICY[fact.guard_id]
        if fact.semantic_owner is not expected_owner:
            return False
        if expected_owner is GuardSemanticOwner.P1_4_SYSTEM:
            return p1_4_authority_matches_fact(self._p1_4_guard_authority, fact, request)
        verifier = self._future_owner_verifiers.get(expected_owner)
        return verifier is not None and verifier_matches_fact(verifier, fact, request)

    @staticmethod
    def _reason(
        *,
        request: TransitionRequest,
        current: WorkRun | None,
        current_matches: bool,
        required: frozenset[GuardId] | None,
        observations: list[GuardObservation],
        missing: list[GuardId],
    ) -> DecisionReason:
        if not current_matches:
            return DecisionReason.STALE_REQUEST
        if required is None:
            return DecisionReason.INVALID_TRANSITION
        if current is not None:
            contract_matches = (
                current.project_id == request.project_id
                and current.task_contract_id == request.task_contract_id
                and current.task_contract_version == request.task_contract_version
                and current.work_run_id == request.work_run_id
            )
            if not contract_matches:
                return DecisionReason.CONTRACT_MISMATCH
            if current.runtime_mode is not request.runtime_mode:
                return DecisionReason.RUNTIME_MODE_MISMATCH
        if missing:
            return DecisionReason.MISSING_GUARD
        if any(not observation.satisfied for observation in observations):
            return DecisionReason.GUARD_FAILED
        return DecisionReason.ADMITTED


def authoritative_runtime_mode(current: WorkRun | None, request: TransitionRequest) -> RuntimeMode:
    return current.runtime_mode if current is not None else request.runtime_mode


def authoritative_state(current: WorkRun | None) -> WorkflowState | None:
    return current.state if current is not None else None
