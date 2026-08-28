from __future__ import annotations

from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.providers.authority import ExecutionReferenceAuthority
from aiscc.providers.models import (
    ExecutionAttemptRef,
    ExecutionStatus,
    ExecutionSubmissionRef,
)
from aiscc.workflow.guards import P1_4GuardAuthority
from aiscc.workflow.models import GuardId, RequesterType, TransitionRequest


def _request(target: WorkflowState) -> TransitionRequest:
    return TransitionRequest(
        "request",
        "project",
        "task",
        "1",
        "run",
        WorkflowState.READY,
        1,
        target,
        "system",
        RequesterType.SYSTEM,
        RuntimeMode.OWNER_SELF_DOGFOOD,
    )


def test_p1_4_mints_its_fact_only_after_issuer_backed_start_ref_validation() -> None:
    refs = ExecutionReferenceAuthority()
    request = _request(WorkflowState.RUNNING)
    ref = refs.register_start(
        ExecutionAttemptRef(
            "attempt",
            "run",
            "task",
            "1",
            WorkflowState.READY,
            1,
            1,
            ExecutionStatus.NOT_STARTED,
            refs.issuer_ref,
        )
    )
    fact = P1_4GuardAuthority().issue_from_execution_ref(
        guard_id=GuardId.G_EXECUTION_STARTED,
        execution_ref=ref,
        verifier=refs,
        request=request,
    )
    assert fact.guard_id is GuardId.G_EXECUTION_STARTED


def test_raw_or_forged_execution_ref_cannot_satisfy_handoff() -> None:
    refs = ExecutionReferenceAuthority()
    request = _request(WorkflowState.RUNNING)
    forged = ExecutionAttemptRef(
        "attempt",
        "run",
        "task",
        "1",
        WorkflowState.READY,
        1,
        1,
        ExecutionStatus.NOT_STARTED,
        refs.issuer_ref,
    )
    try:
        P1_4GuardAuthority().issue_from_execution_ref(
            guard_id=GuardId.G_EXECUTION_STARTED,
            execution_ref=forged,
            verifier=refs,
            request=request,
        )
    except ValueError as exc:
        assert "unrecognized" in str(exc)
    else:
        raise AssertionError("forged ref was accepted")


def test_submission_ref_is_producer_authority_not_evidence_admission() -> None:
    refs = ExecutionReferenceAuthority()
    submission = refs.register_submission(
        ExecutionSubmissionRef(
            "submission",
            "attempt",
            "run",
            "task",
            "1",
            WorkflowState.RUNNING,
            2,
            ExecutionStatus.EXECUTOR_COMPLETED,
            "f" * 64,
            refs.issuer_ref,
        )
    )
    assert submission.status is ExecutionStatus.EXECUTOR_COMPLETED
    assert not hasattr(submission, "evidence_admitted")
