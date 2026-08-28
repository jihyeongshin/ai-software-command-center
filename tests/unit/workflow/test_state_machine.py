from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime
from typing import cast

import pytest

import aiscc.workflow as workflow_package
from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.workflow.evaluator import TransitionEvaluator
from aiscc.workflow.guards import (
    GUARD_OWNER_POLICY,
    FutureOwnerGuardVerifier,
    P1_4GuardAuthority,
    TrustedGuardFact,
    required_bound_refs,
)
from aiscc.workflow.kernel import WorkflowKernel
from aiscc.workflow.matrix import TERMINAL_STATES, TRANSITION_MATRIX, required_judgment_guard
from aiscc.workflow.models import (
    DecisionOutcome,
    DecisionReason,
    GuardId,
    GuardSemanticOwner,
    RequesterType,
    TransitionRequest,
    WorkRun,
)
from aiscc.workflow.ports import TransitionRepository

EXPECTED_STATES = {
    "READY",
    "RUNNING",
    "ADMISSION_PENDING",
    "HUMAN_REQUIRED",
    "BLOCKED",
    "REWORK_REQUIRED",
    "ACCEPTED",
    "REJECTED",
    "FAILED",
}


def request(
    *,
    source: WorkflowState | None,
    version: int,
    target: WorkflowState,
    request_id: str = "request-1",
    evidence_refs: tuple[str, ...] = (),
    human_result_refs: tuple[str, ...] = (),
    judgment_refs: tuple[str, ...] = (),
) -> TransitionRequest:
    return TransitionRequest(
        transition_request_id=request_id,
        project_id="project-1",
        task_contract_id="task-1",
        task_contract_version="v1",
        work_run_id="run-1",
        observed_state=source,
        observed_state_version=version,
        target_state=target,
        requester_identity="system-1",
        requester_type=RequesterType.SYSTEM,
        runtime_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        evidence_refs=evidence_refs,
        human_result_refs=human_result_refs,
        judgment_refs=judgment_refs,
    )


def current(state: WorkflowState, version: int) -> WorkRun:
    now = datetime.now(UTC)
    return WorkRun(
        project_id="project-1",
        task_contract_id="task-1",
        task_contract_version="v1",
        work_run_id="run-1",
        state=state,
        state_version=version,
        runtime_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        created_at=now,
        updated_at=now,
    )


class TestFutureOwnerAuthority:
    __test__ = False

    def __init__(self, semantic_owner: GuardSemanticOwner) -> None:
        if semantic_owner is GuardSemanticOwner.P1_4_SYSTEM:
            raise ValueError("future test authority cannot own P1-4 guards")
        self._semantic_owner = semantic_owner
        self._issuer_token = object()

    @property
    def semantic_owner(self) -> GuardSemanticOwner:
        return self._semantic_owner

    def recognizes(self, fact: TrustedGuardFact) -> bool:
        return fact._issuer_token is self._issuer_token

    def issue(
        self,
        *,
        guard_id: GuardId,
        transition_request: TransitionRequest,
        bound_refs: tuple[str, ...],
    ) -> TrustedGuardFact:
        if GUARD_OWNER_POLICY[guard_id] is not self.semantic_owner:
            raise ValueError("test authority owner mismatch")
        return TrustedGuardFact(
            guard_id=guard_id,
            semantic_owner=self.semantic_owner,
            satisfied=True,
            reason="TRUSTED_TEST_FIXTURE_PASS",
            authority_ref=f"test-owner:{self.semantic_owner.value}",
            bound_refs=bound_refs,
            task_contract_id=transition_request.task_contract_id,
            task_contract_version=transition_request.task_contract_version,
            work_run_id=transition_request.work_run_id,
            state_version=transition_request.observed_state_version,
            _issuer_token=self._issuer_token,
        )


class TestGuardAuthority:
    __test__ = False

    def __init__(self) -> None:
        self.system = P1_4GuardAuthority()
        self._future = {
            owner: TestFutureOwnerAuthority(owner)
            for owner in (
                GuardSemanticOwner.P1_6_EVIDENCE,
                GuardSemanticOwner.P1_7_HUMAN,
                GuardSemanticOwner.P1_7_JUDGMENT,
            )
        }

    @property
    def future_verifiers(self) -> tuple[FutureOwnerGuardVerifier, ...]:
        return tuple(self._future.values())

    def issue(self, guard_id: GuardId, transition_request: TransitionRequest) -> TrustedGuardFact:
        owner = GUARD_OWNER_POLICY[guard_id]
        if owner is GuardSemanticOwner.P1_4_SYSTEM:
            return self.system.issue(
                guard_id=guard_id,
                satisfied=True,
                reason="TRUSTED_TEST_FIXTURE_PASS",
                authority_ref=f"fixture:{guard_id.value}",
                request=transition_request,
            )
        return self._future[owner].issue(
            guard_id=guard_id,
            transition_request=transition_request,
            bound_refs=required_bound_refs(guard_id, transition_request),
        )

    def evaluator(self) -> TransitionEvaluator:
        return TransitionEvaluator(self.system, self.future_verifiers)


def facts_for(
    authority: TestGuardAuthority,
    transition_request: TransitionRequest,
    guards: frozenset[GuardId],
) -> tuple[TrustedGuardFact, ...]:
    return tuple(authority.issue(guard, transition_request) for guard in sorted(guards, key=str))


def test_exact_nine_state_set_and_terminal_set() -> None:
    assert {state.value for state in WorkflowState} == EXPECTED_STATES
    assert {
        WorkflowState.ACCEPTED,
        WorkflowState.REJECTED,
        WorkflowState.FAILED,
    } == TERMINAL_STATES


def test_exact_transition_matrix_has_only_accepted_twenty_two_pairs() -> None:
    assert len(TRANSITION_MATRIX) == 22
    assert (None, WorkflowState.READY) in TRANSITION_MATRIX
    assert (WorkflowState.READY, WorkflowState.RUNNING) in TRANSITION_MATRIX
    assert (WorkflowState.ACCEPTED, WorkflowState.READY) not in TRANSITION_MATRIX
    assert (WorkflowState.REJECTED, WorkflowState.READY) not in TRANSITION_MATRIX
    assert (WorkflowState.FAILED, WorkflowState.READY) not in TRANSITION_MATRIX


@pytest.mark.parametrize("terminal", sorted(TERMINAL_STATES, key=str))
def test_terminal_outgoing_request_is_denied_without_hidden_reroute(
    terminal: WorkflowState,
) -> None:
    authority = TestGuardAuthority()
    evaluator = authority.evaluator()
    transition_request = request(source=terminal, version=9, target=WorkflowState.READY)
    evaluation, decision = evaluator.evaluate(
        request=transition_request,
        current=current(terminal, 9),
        facts=(),
    )
    assert decision.outcome is DecisionOutcome.DENIED
    assert decision.reason is DecisionReason.INVALID_TRANSITION
    assert decision.resulting_state is terminal
    assert decision.resulting_state_version == 9
    assert evaluation.authoritative_state is terminal


def test_judgment_target_mapping_is_exact() -> None:
    assert required_judgment_guard(WorkflowState.ACCEPTED) is GuardId.G_JUDGMENT_ACCEPTED
    assert required_judgment_guard(WorkflowState.REJECTED) is GuardId.G_JUDGMENT_REJECTED
    assert required_judgment_guard(WorkflowState.REWORK_REQUIRED) is GuardId.G_JUDGMENT_REWORK
    assert required_judgment_guard(WorkflowState.FAILED) is None
    assert required_judgment_guard(WorkflowState.HUMAN_REQUIRED) is None


def test_human_and_judgment_refs_do_not_directly_mutate_state() -> None:
    authority = TestGuardAuthority()
    evaluator = authority.evaluator()
    transition_request = request(
        source=WorkflowState.HUMAN_REQUIRED,
        version=4,
        target=WorkflowState.ACCEPTED,
        human_result_refs=("human-result:approve",),
        judgment_refs=("judgment:accepted",),
    )
    _, decision = evaluator.evaluate(
        request=transition_request,
        current=current(WorkflowState.HUMAN_REQUIRED, 4),
        facts=(),
    )
    assert decision.outcome is DecisionOutcome.DENIED
    assert decision.reason is DecisionReason.MISSING_GUARD
    assert decision.resulting_state is WorkflowState.HUMAN_REQUIRED
    assert decision.resulting_state_version == 4


def test_issuer_backed_guard_facts_admit_exactly_one_version_increment() -> None:
    authority = TestGuardAuthority()
    evaluator = authority.evaluator()
    transition_request = request(
        source=WorkflowState.READY,
        version=1,
        target=WorkflowState.RUNNING,
    )
    guards = TRANSITION_MATRIX[(WorkflowState.READY, WorkflowState.RUNNING)]
    evaluation, decision = evaluator.evaluate(
        request=transition_request,
        current=current(WorkflowState.READY, 1),
        facts=facts_for(authority, transition_request, guards),
    )
    assert not evaluation.missing_guards
    assert decision.outcome is DecisionOutcome.ADMITTED
    assert decision.resulting_state is WorkflowState.RUNNING
    assert decision.resulting_state_version == 2


def test_stale_request_denies_even_with_all_trusted_guards() -> None:
    authority = TestGuardAuthority()
    evaluator = authority.evaluator()
    transition_request = request(
        source=WorkflowState.READY,
        version=1,
        target=WorkflowState.RUNNING,
    )
    guards = TRANSITION_MATRIX[(WorkflowState.READY, WorkflowState.RUNNING)]
    _, decision = evaluator.evaluate(
        request=transition_request,
        current=current(WorkflowState.READY, 2),
        facts=facts_for(authority, transition_request, guards),
    )
    assert decision.outcome is DecisionOutcome.DENIED
    assert decision.reason is DecisionReason.STALE_REQUEST
    assert decision.resulting_state is WorkflowState.READY
    assert decision.resulting_state_version == 2


def test_guard_owner_policy_is_exact_and_complete() -> None:
    assert set(GUARD_OWNER_POLICY) == set(GuardId)
    assert GUARD_OWNER_POLICY[GuardId.G_CURRENT] is GuardSemanticOwner.P1_4_SYSTEM
    assert GUARD_OWNER_POLICY[GuardId.G_EVIDENCE] is GuardSemanticOwner.P1_6_EVIDENCE
    assert GUARD_OWNER_POLICY[GuardId.G_HUMAN_APPROVED] is GuardSemanticOwner.P1_7_HUMAN
    assert GUARD_OWNER_POLICY[GuardId.G_JUDGMENT_ACCEPTED] is GuardSemanticOwner.P1_7_JUDGMENT


@pytest.mark.parametrize(
    "guard_id",
    [
        GuardId.G_EVIDENCE,
        GuardId.G_HUMAN_REQUIRED,
        GuardId.G_HUMAN_NOT_REQUIRED,
        GuardId.G_NO_PENDING_HUMAN_GATE,
        GuardId.G_SUSPENDED_HUMAN_GATE,
        GuardId.G_RESUMABLE_HUMAN_GATE,
        GuardId.G_HUMAN_APPROVED,
        GuardId.G_HUMAN_REWORK,
        GuardId.G_HUMAN_REJECTED,
        GuardId.G_JUDGMENT_ACCEPTED,
        GuardId.G_JUDGMENT_REJECTED,
        GuardId.G_JUDGMENT_REWORK,
    ],
)
def test_p1_4_production_issuer_cannot_mint_future_owner_guards(guard_id: GuardId) -> None:
    authority = P1_4GuardAuthority()
    transition_request = request(source=None, version=0, target=WorkflowState.READY)
    with pytest.raises(ValueError, match="not owned by P1-4"):
        authority.issue(
            guard_id=guard_id,
            satisfied=True,
            reason="caller assertion",
            authority_ref="caller",
            request=transition_request,
        )


def test_workflow_kernel_exposes_no_guard_minting_handle_or_universal_issuer() -> None:
    kernel = WorkflowKernel(cast(TransitionRepository, object()))
    assert not hasattr(kernel, "guard_authority")
    assert not hasattr(kernel, "issue")
    assert not hasattr(kernel, "mint")
    assert not hasattr(workflow_package, "TrustedGuardAuthority")


def test_owner_mismatch_fact_is_rejected() -> None:
    authority = TestGuardAuthority()
    evaluator = authority.evaluator()
    transition_request = request(source=None, version=0, target=WorkflowState.READY)
    trusted = list(
        facts_for(authority, transition_request, TRANSITION_MATRIX[(None, WorkflowState.READY)])
    )
    contract_index = next(
        index for index, fact in enumerate(trusted) if fact.guard_id is GuardId.G_CONTRACT
    )
    trusted[contract_index] = replace(
        trusted[contract_index], semantic_owner=GuardSemanticOwner.P1_6_EVIDENCE
    )
    evaluation, decision = evaluator.evaluate(
        request=transition_request,
        current=None,
        facts=tuple(trusted),
    )
    assert decision.reason is DecisionReason.MISSING_GUARD
    assert GuardId.G_CONTRACT in evaluation.missing_guards


def test_fake_caller_created_fact_is_rejected() -> None:
    authority = TestGuardAuthority()
    evaluator = authority.evaluator()
    transition_request = request(source=None, version=0, target=WorkflowState.READY)
    trusted = list(
        facts_for(authority, transition_request, TRANSITION_MATRIX[(None, WorkflowState.READY)])
    )
    contract_index = next(
        index for index, fact in enumerate(trusted) if fact.guard_id is GuardId.G_CONTRACT
    )
    trusted[contract_index] = TrustedGuardFact(
        guard_id=GuardId.G_CONTRACT,
        semantic_owner=GuardSemanticOwner.P1_4_SYSTEM,
        satisfied=True,
        reason="CALLER_ASSERTED",
        authority_ref="caller",
        bound_refs=(),
        task_contract_id=transition_request.task_contract_id,
        task_contract_version=transition_request.task_contract_version,
        work_run_id=transition_request.work_run_id,
        state_version=transition_request.observed_state_version,
        _issuer_token=object(),
    )
    evaluation, decision = evaluator.evaluate(
        request=transition_request,
        current=None,
        facts=tuple(trusted),
    )
    assert decision.reason is DecisionReason.MISSING_GUARD
    assert GuardId.G_CONTRACT in evaluation.missing_guards


@pytest.mark.parametrize(
    (
        "source",
        "target",
        "evidence_refs",
        "human_result_refs",
        "judgment_refs",
        "expected_guard",
    ),
    [
        (
            WorkflowState.ADMISSION_PENDING,
            WorkflowState.ACCEPTED,
            ("evidence:raw",),
            (),
            (),
            GuardId.G_EVIDENCE,
        ),
        (
            WorkflowState.HUMAN_REQUIRED,
            WorkflowState.REWORK_REQUIRED,
            (),
            ("human-result:raw",),
            (),
            GuardId.G_HUMAN_REWORK,
        ),
        (
            WorkflowState.RUNNING,
            WorkflowState.REWORK_REQUIRED,
            (),
            (),
            ("judgment:raw",),
            GuardId.G_JUDGMENT_REWORK,
        ),
    ],
)
def test_raw_future_owner_refs_alone_are_non_authoritative(
    source: WorkflowState,
    target: WorkflowState,
    evidence_refs: tuple[str, ...],
    human_result_refs: tuple[str, ...],
    judgment_refs: tuple[str, ...],
    expected_guard: GuardId,
) -> None:
    authority = TestGuardAuthority()
    evaluator = authority.evaluator()
    transition_request = request(
        source=source,
        version=4,
        target=target,
        evidence_refs=evidence_refs,
        human_result_refs=human_result_refs,
        judgment_refs=judgment_refs,
    )
    evaluation, decision = evaluator.evaluate(
        request=transition_request,
        current=current(source, 4),
        facts=(),
    )
    assert decision.reason is DecisionReason.MISSING_GUARD
    assert expected_guard in evaluation.missing_guards


def test_future_owner_fact_with_wrong_bound_refs_is_rejected() -> None:
    authority = TestGuardAuthority()
    evaluator = authority.evaluator()
    transition_request = request(
        source=WorkflowState.HUMAN_REQUIRED,
        version=4,
        target=WorkflowState.ACCEPTED,
        evidence_refs=("evidence:exact",),
        human_result_refs=("human-result:exact",),
        judgment_refs=("judgment:exact",),
    )
    trusted = list(
        facts_for(
            authority,
            transition_request,
            TRANSITION_MATRIX[(WorkflowState.HUMAN_REQUIRED, WorkflowState.ACCEPTED)],
        )
    )
    evidence_index = next(
        index for index, fact in enumerate(trusted) if fact.guard_id is GuardId.G_EVIDENCE
    )
    trusted[evidence_index] = replace(trusted[evidence_index], bound_refs=("evidence:wrong",))
    evaluation, decision = evaluator.evaluate(
        request=transition_request,
        current=current(WorkflowState.HUMAN_REQUIRED, 4),
        facts=tuple(trusted),
    )
    assert decision.reason is DecisionReason.MISSING_GUARD
    assert GuardId.G_EVIDENCE in evaluation.missing_guards


def test_exact_owner_bound_facts_with_matching_refs_may_admit() -> None:
    authority = TestGuardAuthority()
    evaluator = authority.evaluator()
    transition_request = request(
        source=WorkflowState.HUMAN_REQUIRED,
        version=4,
        target=WorkflowState.ACCEPTED,
        evidence_refs=("evidence:exact",),
        human_result_refs=("human-result:exact",),
        judgment_refs=("judgment:exact",),
    )
    trusted = facts_for(
        authority,
        transition_request,
        TRANSITION_MATRIX[(WorkflowState.HUMAN_REQUIRED, WorkflowState.ACCEPTED)],
    )
    evaluation, decision = evaluator.evaluate(
        request=transition_request,
        current=current(WorkflowState.HUMAN_REQUIRED, 4),
        facts=trusted,
    )
    assert not evaluation.missing_guards
    assert decision.outcome is DecisionOutcome.ADMITTED
    assert decision.resulting_state is WorkflowState.ACCEPTED


def test_absent_future_owner_verifier_fails_closed() -> None:
    authority = TestGuardAuthority()
    evaluator = TransitionEvaluator(authority.system)
    transition_request = request(
        source=WorkflowState.ADMISSION_PENDING,
        version=3,
        target=WorkflowState.ACCEPTED,
        evidence_refs=("evidence:exact",),
        judgment_refs=("judgment:exact",),
    )
    trusted = facts_for(
        authority,
        transition_request,
        TRANSITION_MATRIX[(WorkflowState.ADMISSION_PENDING, WorkflowState.ACCEPTED)],
    )
    evaluation, decision = evaluator.evaluate(
        request=transition_request,
        current=current(WorkflowState.ADMISSION_PENDING, 3),
        facts=trusted,
    )
    assert decision.reason is DecisionReason.MISSING_GUARD
    assert GuardId.G_EVIDENCE in evaluation.missing_guards
    assert GuardId.G_JUDGMENT_ACCEPTED in evaluation.missing_guards
