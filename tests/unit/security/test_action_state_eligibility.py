from __future__ import annotations

from aiscc.contracts.security import SecurityActionClass
from aiscc.contracts.workflow import WorkflowState
from aiscc.security.action_state import ACTION_STATE_MATRIX, is_action_state_eligible


def test_matrix_covers_exact_nine_states() -> None:
    assert set(ACTION_STATE_MATRIX) == set(WorkflowState)


def test_mutable_execution_is_only_admissible_while_running() -> None:
    action = SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT
    eligible = {state for state in WorkflowState if is_action_state_eligible(state, action)}
    assert eligible == {WorkflowState.RUNNING}


def test_terminal_states_only_admit_read_or_safety_classes() -> None:
    forbidden = {
        SecurityActionClass.START_EXECUTION_CONTROL,
        SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        SecurityActionClass.PUBLIC_CANCEL_CONTROL,
        SecurityActionClass.ADMINISTRATIVE_TERMINATE_CONTROL,
        SecurityActionClass.REWORK_START_CONTROL,
        SecurityActionClass.BLOCKER_RECOVERY_CHECK,
    }
    for state in (WorkflowState.ACCEPTED, WorkflowState.REJECTED, WorkflowState.FAILED):
        assert ACTION_STATE_MATRIX[state].isdisjoint(forbidden)
