from __future__ import annotations

import asyncio
from datetime import UTC, datetime

import pytest

from aiscc.contracts.workflow import WorkflowState
from aiscc.evidence.models import EvidenceSensitivity
from aiscc.human.authority import HumanPrincipalAuthority, public_human_projection
from aiscc.human.models import (
    HumanAuthorityError,
    HumanGate,
    HumanGateStatus,
    HumanGateSuspensionStatus,
    HumanResultKind,
)
from aiscc.judgment.models import JudgmentKind

NOW = datetime(2026, 8, 30, 1, 0, tzinfo=UTC)


def gate() -> HumanGate:
    return HumanGate(
        "gate-1",
        "v1",
        "a" * 64,
        "P1_7_WORK_RESULT_REVIEW",
        "v1",
        "task-1",
        "v1",
        "run-1",
        WorkflowState.ADMISSION_PENDING,
        3,
        WorkflowState.HUMAN_REQUIRED,
        4,
        "request-1",
        "decision-1",
        "policy-1",
        "v1",
        "selector-1",
        "human-authority",
        "v1",
        1,
        HumanGateStatus.PENDING,
        HumanGateSuspensionStatus.ACTIVE,
        NOW,
        None,
    )


def test_principal_authority_is_not_caller_text_and_public_export_is_sanitized() -> None:
    authority = HumanPrincipalAuthority(clock=lambda: NOW)
    principal = authority.authenticate(
        principal_id="internal-human-42",
        session_id="private-session-99",
        role_refs=("reviewer",),
    )
    with pytest.raises(HumanAuthorityError):
        asyncio.run(
            authority.issue_action_authority(
                principal,
                gate(),
                idempotency_scope="result-1",  # type: ignore[arg-type]
            )
        )
    projection = public_human_projection(gate(), HumanResultKind.APPROVE)
    assert projection == {
        "human_review": "pending",
        "principal_display": "HUMAN_REVIEWER",
        "result_kind": "APPROVE",
    }
    assert "internal-human-42" not in repr(projection)
    assert "private-session-99" not in repr(projection)
    assert EvidenceSensitivity.SECRET_FORBIDDEN.value not in repr(projection)


def test_non_substitution_vocabularies_are_disjoint() -> None:
    assert set(HumanResultKind) == {
        HumanResultKind.APPROVE,
        HumanResultKind.REWORK,
        HumanResultKind.REJECT,
    }
    assert set(JudgmentKind) == {
        JudgmentKind.ACCEPTED,
        JudgmentKind.REJECTED,
        JudgmentKind.HOLD_REWORK_REQUIRED,
    }
    assert not set(item.value for item in HumanResultKind) <= set(
        item.value for item in JudgmentKind
    )
    with pytest.raises(ValueError):
        HumanResultKind("ACCEPTED")
