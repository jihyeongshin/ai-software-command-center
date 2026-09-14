from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta, timezone

import pytest

from aiscc.next_action.models import ActionRef, HumanInputKind, TaskIssuanceCandidate
from aiscc.task_authority.contracts import candidate_fingerprint
from aiscc.task_authority.models import ExternalTaskAuthorityError
from aiscc.task_authority.repository import PostgresExternalTaskAuthorityRepository


def test_candidate_fingerprint_utc_instant_stable_and_semantic_changes_differ():
    value = TaskIssuanceCandidate(
        "candidate",
        "selection",
        ActionRef("policy", "v1", "action", "v1", "1" * 64),
        {},
        "EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY",
        HumanInputKind.AFTER_TASK_ISSUANCE_P1_7,
        datetime(2026, 9, 10, 18, 24, tzinfo=timezone(timedelta(hours=9))),
    )
    assert candidate_fingerprint(value) == candidate_fingerprint(
        replace(value, created_at=value.created_at.astimezone(UTC))
    )
    assert candidate_fingerprint(value) != candidate_fingerprint(
        replace(value, candidate_id="changed")
    )


def test_unbound_or_forged_writer_capability_denied_before_access():
    def forbidden():
        raise AssertionError("opened a session")

    repository = PostgresExternalTaskAuthorityRepository(forbidden)
    for capability in (None, object()):
        with pytest.raises(ExternalTaskAuthorityError):
            repository._require_capability(capability)
