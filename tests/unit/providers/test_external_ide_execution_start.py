from dataclasses import FrozenInstanceError

import pytest

from aiscc.providers.authority import ExecutionReferenceAuthority
from aiscc.providers.external_ide import (
    ExternalIdeExecutionStartPermitV1,
    ExternalIdeExecutionStartRef,
    VerifiedExternalIdeExecutionStartV1,
)
from tests.unit.providers.test_external_ide_execution_ingress import NOW, sample


def start_sample(root):
    v = sample(root)
    for k in ("lease_id", "start_transition_id", "expected_hashes"):
        v.pop(k)
    return v | dict(
        schema="AISCC-EXTERNAL-IDE-START-PERMIT-V1",
        permit_id="permit",
        state="READY",
        state_version=1,
        ready_transition_id="ready",
    )


@pytest.mark.parametrize(
    "field,value",
    [
        ("producer", "GENERIC"),
        ("unexpected", "field"),
        ("state", "RUNNING"),
        ("state_version", True),
        ("state_version", 0),
        ("state_version", 2**54),
        ("contract_version", False),
        ("body_sha256", "A" * 64),
        ("body_ref", "bad"),
        ("project_id", "e\u0301"),
        ("allowed_paths", ["../file"]),
        ("allowed_paths", ["src/**", "src/**"]),
        ("allowed_paths", ["**"]),
        ("forbidden_paths", ["src/file.txt"]),
        ("expires_at", NOW.isoformat()),
        ("issued_at", "2026-09-14T18:00:00+09:00"),
        ("repository_root", "relative"),
        ("base_commit", "f" * 64),
        ("scope_fingerprint", "0" * 64),
    ],
)
def test_closed_start_permit(tmp_path, field, value):
    with pytest.raises(ValueError):
        ExternalIdeExecutionStartPermitV1(start_sample(tmp_path) | {field: value})


def test_constructed_permit_or_ref_is_not_start_authority(tmp_path):
    permit = ExternalIdeExecutionStartPermitV1(start_sample(tmp_path))
    assert (
        permit.canonical_body
        == ExternalIdeExecutionStartPermitV1(start_sample(tmp_path)).canonical_body
    )
    with pytest.raises(TypeError):
        permit.value["project_id"] = "forged"
    with pytest.raises(FrozenInstanceError):
        permit.canonical_body = b"{}"
    ref = ExternalIdeExecutionStartRef(permit, "a" * 64, object())
    with pytest.raises(ValueError):
        _ = VerifiedExternalIdeExecutionStartV1(ref).common_ref
    with pytest.raises(ValueError):
        ExecutionReferenceAuthority().register_start(ref)
