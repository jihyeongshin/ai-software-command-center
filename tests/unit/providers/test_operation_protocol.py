from __future__ import annotations

import pytest

from aiscc.providers.events import (
    legal_operation_edge,
    lifecycle_result,
    require_legal_operation_edge,
)
from aiscc.providers.models import ExecutionOperationOutcome as O
from aiscc.providers.models import ExecutionOperationPhase as P


def test_every_accepted_operation_edge() -> None:
    assert legal_operation_edge(P.PREPARED, P.SECURITY_ADMITTED)
    assert legal_operation_edge(P.PREPARED, P.OUTCOME_KNOWN, O.DENIED_BEFORE_SIDE_EFFECT)
    assert legal_operation_edge(P.SECURITY_ADMITTED, P.DISPATCH_STARTED)
    assert legal_operation_edge(P.SECURITY_ADMITTED, P.OUTCOME_KNOWN, O.CANCELLED)
    for outcome in {
        O.DEFINITELY_NOT_SENT,
        O.PROVIDER_REJECTED,
        O.PROVIDER_COMPLETED,
        O.PROVIDER_INCOMPLETE,
        O.TOOL_COMPLETED,
        O.TOOL_FAILED,
        O.CANCELLED,
    }:
        assert legal_operation_edge(P.DISPATCH_STARTED, P.OUTCOME_KNOWN, outcome)
    assert legal_operation_edge(
        P.DISPATCH_STARTED, P.OUTCOME_UNKNOWN, O.TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME
    )


@pytest.mark.parametrize(
    ("source", "target", "outcome"),
    [
        (P.PREPARED, P.DISPATCH_STARTED, None),
        (P.PREPARED, P.OUTCOME_UNKNOWN, O.TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME),
        (P.SECURITY_ADMITTED, P.OUTCOME_UNKNOWN, O.TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME),
        (P.OUTCOME_KNOWN, P.DISPATCH_STARTED, None),
    ],
)
def test_unlisted_edge_denies_without_repair(source: P, target: P, outcome: O | None) -> None:
    with pytest.raises(ValueError, match="ILLEGAL_OPERATION_PHASE_EDGE"):
        require_legal_operation_edge(source, target, outcome)


def test_invalid_history_abort_is_the_only_start_free_terminal_edge() -> None:
    assert (
        lifecycle_result("NOT_STARTED", "EXECUTION_ABORTED_INVALID_HISTORY")
        == "EXECUTION_FAILED"
    )
    for before, event in (
        ("NOT_STARTED", "EXECUTION_FAILED"),
        ("RUNNING", "EXECUTION_ABORTED_INVALID_HISTORY"),
        ("EXECUTION_FAILED", "EXECUTION_ABORTED_INVALID_HISTORY"),
    ):
        with pytest.raises(ValueError, match="ILLEGAL_EXECUTION_STATUS_TRANSITION"):
            lifecycle_result(before, event)
