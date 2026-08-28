from __future__ import annotations

import pytest

from aiscc.providers.models import (
    ExecutionAttemptFailureClass,
    ExecutionOperationOutcome,
    ExecutionOperationPhase,
    ExecutionStatus,
    canonical_sha256,
    parse_strict_json_object,
)


def test_exact_enum_sets_and_canonical_fingerprint() -> None:
    assert {item.value for item in ExecutionStatus} == {
        "NOT_STARTED",
        "RUNNING",
        "EXECUTOR_COMPLETED",
        "EXECUTION_FAILED",
    }
    assert len(ExecutionOperationPhase) == 5
    assert len(ExecutionOperationOutcome) == 9
    assert ExecutionAttemptFailureClass.RETRY_EXHAUSTED.value == "RETRY_EXHAUSTED"
    assert canonical_sha256({"b": 2, "a": 1}) == canonical_sha256({"a": 1, "b": 2})


@pytest.mark.parametrize("raw", ['{"a":1,"a":2}', '{"a":NaN}', "[1]", '{"a":1.5}'])
def test_invalid_or_unrepresentable_fingerprint_input_fails_closed(raw: str) -> None:
    with pytest.raises(ValueError):
        parse_strict_json_object(raw)
