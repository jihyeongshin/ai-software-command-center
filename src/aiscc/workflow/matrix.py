from __future__ import annotations

from aiscc.contracts.workflow import WorkflowState
from aiscc.workflow.models import GuardId

StateSource = WorkflowState | None


TRANSITION_MATRIX: dict[tuple[StateSource, WorkflowState], frozenset[GuardId]] = {
    (None, WorkflowState.READY): frozenset(
        {GuardId.G_CONTRACT, GuardId.G_SCOPE, GuardId.G_RUNTIME_CONTEXT}
    ),
    (WorkflowState.READY, WorkflowState.RUNNING): frozenset(
        {
            GuardId.G_CONTRACT,
            GuardId.G_SCOPE,
            GuardId.G_RUNTIME_CONTEXT,
            GuardId.G_EXECUTION_STARTED,
        }
    ),
    (WorkflowState.RUNNING, WorkflowState.ADMISSION_PENDING): frozenset(
        {GuardId.G_EXECUTOR_SUBMISSION, GuardId.G_SCOPE}
    ),
    (WorkflowState.RUNNING, WorkflowState.BLOCKED): frozenset({GuardId.G_BLOCKER}),
    (WorkflowState.RUNNING, WorkflowState.REWORK_REQUIRED): frozenset(
        {GuardId.G_HUMAN_NOT_REQUIRED, GuardId.G_JUDGMENT_REWORK, GuardId.G_REWORK_SPEC}
    ),
    (WorkflowState.RUNNING, WorkflowState.FAILED): frozenset({GuardId.G_FAILURE_TERMINAL}),
    (WorkflowState.ADMISSION_PENDING, WorkflowState.HUMAN_REQUIRED): frozenset(
        {GuardId.G_HUMAN_REQUIRED}
    ),
    (WorkflowState.ADMISSION_PENDING, WorkflowState.BLOCKED): frozenset({GuardId.G_BLOCKER}),
    (WorkflowState.ADMISSION_PENDING, WorkflowState.REWORK_REQUIRED): frozenset(
        {GuardId.G_HUMAN_NOT_REQUIRED, GuardId.G_JUDGMENT_REWORK, GuardId.G_REWORK_SPEC}
    ),
    (WorkflowState.ADMISSION_PENDING, WorkflowState.ACCEPTED): frozenset(
        {GuardId.G_EVIDENCE, GuardId.G_HUMAN_NOT_REQUIRED, GuardId.G_JUDGMENT_ACCEPTED}
    ),
    (WorkflowState.ADMISSION_PENDING, WorkflowState.REJECTED): frozenset(
        {GuardId.G_HUMAN_NOT_REQUIRED, GuardId.G_JUDGMENT_REJECTED}
    ),
    (WorkflowState.HUMAN_REQUIRED, WorkflowState.ACCEPTED): frozenset(
        {GuardId.G_EVIDENCE, GuardId.G_HUMAN_APPROVED, GuardId.G_JUDGMENT_ACCEPTED}
    ),
    (WorkflowState.HUMAN_REQUIRED, WorkflowState.REWORK_REQUIRED): frozenset(
        {GuardId.G_HUMAN_REWORK, GuardId.G_JUDGMENT_REWORK, GuardId.G_REWORK_SPEC}
    ),
    (WorkflowState.HUMAN_REQUIRED, WorkflowState.REJECTED): frozenset(
        {GuardId.G_HUMAN_REJECTED, GuardId.G_JUDGMENT_REJECTED}
    ),
    (WorkflowState.HUMAN_REQUIRED, WorkflowState.BLOCKED): frozenset({GuardId.G_BLOCKER}),
    (WorkflowState.BLOCKED, WorkflowState.READY): frozenset(
        {
            GuardId.G_BLOCKER_RESOLVED,
            GuardId.G_NO_PENDING_HUMAN_GATE,
            GuardId.G_CONTRACT,
            GuardId.G_SCOPE,
        }
    ),
    (WorkflowState.BLOCKED, WorkflowState.HUMAN_REQUIRED): frozenset(
        {
            GuardId.G_BLOCKER_RESOLVED,
            GuardId.G_SUSPENDED_HUMAN_GATE,
            GuardId.G_RESUMABLE_HUMAN_GATE,
        }
    ),
    (WorkflowState.BLOCKED, WorkflowState.REWORK_REQUIRED): frozenset(
        {
            GuardId.G_BLOCKER_RESOLVED,
            GuardId.G_HUMAN_NOT_REQUIRED,
            GuardId.G_JUDGMENT_REWORK,
            GuardId.G_REWORK_SPEC,
        }
    ),
    (WorkflowState.BLOCKED, WorkflowState.FAILED): frozenset({GuardId.G_FAILURE_TERMINAL}),
    (WorkflowState.REWORK_REQUIRED, WorkflowState.READY): frozenset(
        {
            GuardId.G_REWORK_SPEC,
            GuardId.G_NO_PENDING_HUMAN_GATE,
            GuardId.G_CONTRACT,
            GuardId.G_SCOPE,
        }
    ),
    (WorkflowState.REWORK_REQUIRED, WorkflowState.HUMAN_REQUIRED): frozenset(
        {GuardId.G_HUMAN_REQUIRED}
    ),
    (WorkflowState.REWORK_REQUIRED, WorkflowState.REJECTED): frozenset(
        {GuardId.G_HUMAN_NOT_REQUIRED, GuardId.G_JUDGMENT_REJECTED}
    ),
}

TERMINAL_STATES = frozenset({WorkflowState.ACCEPTED, WorkflowState.REJECTED, WorkflowState.FAILED})


def required_judgment_guard(target: WorkflowState) -> GuardId | None:
    return {
        WorkflowState.ACCEPTED: GuardId.G_JUDGMENT_ACCEPTED,
        WorkflowState.REJECTED: GuardId.G_JUDGMENT_REJECTED,
        WorkflowState.REWORK_REQUIRED: GuardId.G_JUDGMENT_REWORK,
    }.get(target)
