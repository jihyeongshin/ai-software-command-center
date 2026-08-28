from __future__ import annotations

from aiscc.contracts.security import SecurityActionClass
from aiscc.contracts.workflow import WorkflowState

_READ_SAFETY = frozenset(
    {
        SecurityActionClass.RUN_REVIEW_READ_ONLY,
        SecurityActionClass.SAFETY_CLEANUP_REVOKE_QUARANTINE,
        SecurityActionClass.RECOVERY_RECONCILIATION,
        SecurityActionClass.SYSTEM_DURABLE_PROVENANCE,
        SecurityActionClass.REPLAY_READ_ONLY,
    }
)

ACTION_STATE_MATRIX: dict[WorkflowState, frozenset[SecurityActionClass]] = {
    WorkflowState.READY: _READ_SAFETY | {SecurityActionClass.START_EXECUTION_CONTROL},
    WorkflowState.RUNNING: _READ_SAFETY
    | {
        SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        SecurityActionClass.PUBLIC_CANCEL_CONTROL,
        SecurityActionClass.ADMINISTRATIVE_TERMINATE_CONTROL,
    },
    WorkflowState.ADMISSION_PENDING: _READ_SAFETY,
    WorkflowState.HUMAN_REQUIRED: _READ_SAFETY,
    WorkflowState.BLOCKED: _READ_SAFETY | {SecurityActionClass.BLOCKER_RECOVERY_CHECK},
    WorkflowState.REWORK_REQUIRED: _READ_SAFETY | {SecurityActionClass.REWORK_START_CONTROL},
    WorkflowState.ACCEPTED: _READ_SAFETY,
    WorkflowState.REJECTED: _READ_SAFETY,
    WorkflowState.FAILED: _READ_SAFETY,
}


def is_action_state_eligible(state: WorkflowState, action: SecurityActionClass) -> bool:
    return action in ACTION_STATE_MATRIX[state]
