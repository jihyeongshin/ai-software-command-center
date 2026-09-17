from __future__ import annotations

from types import MappingProxyType

import pytest

from aiscc.providers.semantic import plan_next_semantic_request


def item(**values):
    return MappingProxyType(values)


def test_conditional_semantic_sequence_and_same_role_retry() -> None:
    primary = plan_next_semantic_request(prior=(), validation=None)
    assert (primary.role, primary.semantic_ordinal, primary.physical_ordinal) == (
        "PRIMARY",
        1,
        1,
    )
    verify = plan_next_semantic_request(
        prior=(
            item(
                operation_id="p1",
                role="PRIMARY",
                semantic_ordinal=1,
                outcome="KNOWN_SUCCESS",
            ),
        ),
        validation=item(decision="VERIFY_REQUIRED", proof="validation-1"),
    )
    assert verify.role == "VERIFY" and verify.validation_ref == "validation-1"
    correct = plan_next_semantic_request(
        prior=(
            item(
                operation_id="p1",
                role="PRIMARY",
                semantic_ordinal=1,
                outcome="KNOWN_SUCCESS",
            ),
            item(
                operation_id="v1",
                role="VERIFY",
                semantic_ordinal=2,
                outcome="KNOWN_SUCCESS",
            ),
        ),
        validation=item(
            decision="CORRECTABLE_DEFECT",
            proof="validation-2",
            defect_ref="exact-defect-1",
        ),
    )
    assert correct.role == "CORRECT" and correct.defect_ref == "exact-defect-1"
    retry = plan_next_semantic_request(
        prior=(
            item(
                operation_id="p1",
                role="PRIMARY",
                semantic_ordinal=1,
                outcome="KNOWN_FAILURE",
                closed_failure=True,
            ),
        ),
        validation=None,
    )
    assert retry.role == "PRIMARY" and retry.retry_of_operation_id == "p1"


def test_unknown_outcome_never_plans_retry() -> None:
    with pytest.raises(ValueError, match="UNKNOWN_OR_UNVALIDATED"):
        plan_next_semantic_request(
            prior=(
                item(
                    operation_id="p1",
                    role="PRIMARY",
                    semantic_ordinal=1,
                    outcome="UNKNOWN",
                    closed_failure=False,
                ),
            ),
            validation=None,
        )
