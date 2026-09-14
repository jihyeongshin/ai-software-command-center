from dataclasses import replace
from datetime import UTC, datetime

import pytest

from aiscc.contracts.canonical_json import canonical_json_bytes
from aiscc.next_action.genesis import (
    ACTION,
    ISSUER_VERSION,
    MODE,
    OWNER,
    GenesisContextV1,
    GenesisNextActionAuthorityV1,
)
from aiscc.next_action.models import default_next_action_policy_authority
from aiscc.task_authority.contracts import TaskContractError

# Existing shared V1 policy epoch used throughout P1-8 integration regressions.
NOW = datetime(2026, 8, 31, 8, 13, tzinfo=UTC)


def authority(context):
    return GenesisNextActionAuthorityV1(
        canonical_json_bytes(
            dict(
                **context.payload(),
                genesis_authority_id="genesis",
                source_mode=MODE,
                action_id=ACTION,
                issuer=OWNER,
                issuer_version=ISSUER_VERSION,
                issued_at=NOW.isoformat(timespec="microseconds"),
            )
        )
    )


def test_closed_canonical_genesis_and_separate_catalog(tmp_path):
    context = GenesisContextV1("project", "repo", str(tmp_path), "1" * 40, "P2-4")
    value = authority(context)
    owner = default_next_action_policy_authority()
    policy, selection, descriptors = owner.issue_genesis_policy_catalog(authority=value, now=NOW)
    assert owner.recognizes_policy(policy) and owner.recognizes_policy(selection)
    assert len(descriptors) == 1 and owner.recognizes_descriptor(descriptors[0])
    descriptor = descriptors[0]
    assert descriptor.action_ref.action_id == ACTION
    assert [m.value for m in descriptor.allowed_selection_modes] == [MODE]
    assert set(descriptor.parameter_rules) == {
        "genesis_authority_ref",
        "genesis_authority_fingerprint",
    }
    assert "cycle" not in value.value and "work_run_id" not in value.value
    assert not owner.recognizes_descriptor(replace(descriptor, project_restriction="other"))
    copied = value.value
    copied["project_id"] = "other"
    assert value.value["project_id"] == "project"
    for field, wrong in [
        ("source_mode", "CYCLE_DERIVED"),
        ("action_id", "open-cycle-derived-task-issuance"),
        ("issuer", "browser"),
        ("runtime_mode", "REPLAY"),
        ("cycle_execution_mode", "MANUAL_COMMAND_CENTER"),
        ("base_commit", "bad"),
    ]:
        with pytest.raises((TaskContractError, ValueError)):
            GenesisNextActionAuthorityV1(canonical_json_bytes({**value.value, field: wrong}))
    with pytest.raises(TaskContractError):
        GenesisNextActionAuthorityV1(
            canonical_json_bytes({**value.value, "source_cycle_id": "invented"})
        )
