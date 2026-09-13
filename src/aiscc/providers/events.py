from __future__ import annotations

from aiscc.providers.models import (
    ExecutionOperationOutcome as Outcome,
)
from aiscc.providers.models import (
    ExecutionOperationPhase as Phase,
)

_KNOWN_FROM_DISPATCH = frozenset(
    {
        Outcome.DEFINITELY_NOT_SENT,
        Outcome.PROVIDER_REJECTED,
        Outcome.PROVIDER_COMPLETED,
        Outcome.PROVIDER_INCOMPLETE,
        Outcome.TOOL_COMPLETED,
        Outcome.TOOL_FAILED,
        Outcome.CANCELLED,
    }
)


def legal_operation_edge(source: Phase, target: Phase, outcome: Outcome | None = None) -> bool:
    if source is Phase.PREPARED:
        return (target is Phase.SECURITY_ADMITTED and outcome is None) or (
            target is Phase.OUTCOME_KNOWN and outcome is Outcome.DENIED_BEFORE_SIDE_EFFECT
        )
    if source is Phase.SECURITY_ADMITTED:
        return (target is Phase.DISPATCH_STARTED and outcome is None) or (
            target is Phase.OUTCOME_KNOWN and outcome is Outcome.CANCELLED
        )
    if source is Phase.DISPATCH_STARTED:
        return (target is Phase.OUTCOME_KNOWN and outcome in _KNOWN_FROM_DISPATCH) or (
            target is Phase.OUTCOME_UNKNOWN
            and outcome is Outcome.TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME
        )
    return False


def require_legal_operation_edge(
    source: Phase, target: Phase, outcome: Outcome | None = None
) -> None:
    if not legal_operation_edge(source, target, outcome):
        raise ValueError("ILLEGAL_OPERATION_PHASE_EDGE")


_LIFECYCLE = {
    ("NONE", "EXECUTION_ATTEMPT_CREATED"): "NOT_STARTED",
    ("NOT_STARTED", "EXECUTION_STARTED"): "RUNNING",
    ("NOT_STARTED", "EXECUTION_ABORTED_INVALID_HISTORY"): "EXECUTION_FAILED",
    ("RUNNING", "EXECUTION_COMPLETED"): "EXECUTOR_COMPLETED",
    ("RUNNING", "EXECUTION_FAILED"): "EXECUTION_FAILED",
}


def lifecycle_result(before: str, event: str) -> str:
    try:
        return _LIFECYCLE[(before, event)]
    except KeyError as exc:
        raise ValueError("ILLEGAL_EXECUTION_STATUS_TRANSITION") from exc
