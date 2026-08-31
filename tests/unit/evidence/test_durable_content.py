from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime

import pytest

from aiscc.contracts.workflow import WorkflowState
from aiscc.evidence.content import (
    P1_6DurableContentAuthority,
    P1_6HistoricalContentAccessAuthority,
    canonicalize_structured_json,
)
from aiscc.evidence.models import (
    DurableContentError,
    DurableContentErrorCode,
    DurableContentRequirement,
    EvidenceCheckpoint,
    EvidenceCheckpointRef,
    EvidenceContentKind,
    EvidenceRequirement,
    EvidenceRequirementProfile,
    EvidenceRequirementRef,
    EvidenceRequirementSet,
    EvidenceSemanticOwner,
    EvidenceSensitivity,
    FreshnessPolicy,
    FreshnessPolicyKind,
    HistoricalContentAccessGrant,
    RequirementFingerprintSchema,
    RequirementObligation,
)
from aiscc.evidence.requirements import TaskContractEvidenceAuthority, _requirement_payload

NOW = datetime(2026, 8, 30, 15, 0, tzinfo=UTC)
POLICY_HASH = "1" * 64
SOURCE_HASH = "2" * 64


def requirement() -> EvidenceRequirement:
    return EvidenceRequirement(
        ref=EvidenceRequirementRef("structured-result", "v1"),
        task_contract_id="task",
        task_contract_version="v1",
        requirement_set_id="set",
        requirement_set_version="v1",
        semantic_owner=EvidenceSemanticOwner.P1_6_EVIDENCE,
        profile=EvidenceRequirementProfile.EXECUTOR_REQUIRED,
        obligation=RequirementObligation.REQUIRED,
        applicable_checkpoint_refs=("pre-human@v1",),
        evidence_type_id="STRUCTURED_RESULT",
        evidence_type_version="v1",
        allowed_issuer_types=frozenset(),
        allowed_issuer_ids=frozenset(),
        allowed_human_categories=frozenset(),
        allowed_content_kinds=frozenset(
            {EvidenceContentKind.INLINE_CANONICAL_STRUCTURED_BODY}
        ),
        schema_id="AISCC-STRUCTURED-RESULT",
        schema_version="v1",
        subject_id="source",
        scope_id="repository",
        resource_id="repo@commit",
        freshness_policy=FreshnessPolicy(FreshnessPolicyKind.TASK_EXECUTION_SCOPED),
        required_coverage=frozenset({"result"}),
        reuse_maximum=1,
        compatible_requirement_refs=frozenset(),
        maximum_sensitivity=EvidenceSensitivity.INTERNAL,
        public_export_allowed=False,
        issued_at=NOW,
        fingerprint="",
    )


def test_canonical_json_fixed_vector_and_nfc() -> None:
    assert canonicalize_structured_json(b'{"z":1,"a":"e\xcc\x81"}') == (
        '{"a":"é","z":1}'.encode()
    )
    assert canonicalize_structured_json({"e\N{COMBINING ACUTE ACCENT}": "x"}) == (
        '{"é":"x"}'.encode()
    )


@pytest.mark.parametrize(
    "raw",
    (
        b'{"a":1,"a":2}',
        b'{"e\xcc\x81":1,"\xc3\xa9":2}',
        b'{"value":1.5}',
        b'{"value":NaN}',
        b'{"value":Infinity}',
    ),
)
def test_canonical_json_rejects_ambiguous_inputs(raw: bytes) -> None:
    with pytest.raises(DurableContentError) as raised:
        canonicalize_structured_json(raw)
    assert raised.value.code is DurableContentErrorCode.SCHEMA_MISMATCH


def test_depth_node_and_byte_hard_boundaries() -> None:
    depth_32: object = 0
    for _ in range(32):
        depth_32 = [depth_32]
    canonicalize_structured_json(depth_32)
    with pytest.raises(DurableContentError) as depth_error:
        canonicalize_structured_json([depth_32])
    assert depth_error.value.code is DurableContentErrorCode.TOO_LARGE

    canonicalize_structured_json([0] * 4095)
    with pytest.raises(DurableContentError) as node_error:
        canonicalize_structured_json([0] * 4096)
    assert node_error.value.code is DurableContentErrorCode.TOO_LARGE

    assert len(canonicalize_structured_json("x" * 65_534)) == 65_536
    with pytest.raises(DurableContentError) as byte_error:
        canonicalize_structured_json("x" * 65_535)
    assert byte_error.value.code is DurableContentErrorCode.TOO_LARGE


def test_durable_kind_sensitivity_matrix_and_identity_vectors() -> None:
    authority = P1_6DurableContentAuthority()
    arguments = {
        "owner_id": "owner",
        "owner_version": "v1",
        "source_owner_authority_ref": "issuer@v1",
        "source_owner_authority_fingerprint": SOURCE_HASH,
        "object_id": "object",
        "object_version": "v1",
        "value": {"result": "PASS"},
        "kind": EvidenceContentKind.INLINE_CANONICAL_STRUCTURED_BODY,
        "schema_id": "AISCC-STRUCTURED-RESULT",
        "schema_version": "v1",
        "sensitivity": EvidenceSensitivity.INTERNAL,
        "created_at": NOW,
    }
    first = authority.prepare_structured(**arguments)
    replay = authority.prepare_structured(**arguments)
    changed = authority.prepare_structured(**(arguments | {"value": {"result": "FAIL"}}))
    rogue = P1_6DurableContentAuthority().prepare_structured(**arguments)
    assert first.content == replay.content
    assert first.content.content_identity_key == changed.content.content_identity_key
    assert first.content.payload_fingerprint != changed.content.payload_fingerprint
    assert authority.recognizes(first)
    assert not authority.recognizes(rogue)

    with pytest.raises(DurableContentError) as kind_error:
        authority.prepare_structured(
            **(arguments | {"kind": EvidenceContentKind.HUMAN_STRUCTURED_REF})
        )
    assert kind_error.value.code is DurableContentErrorCode.KIND_NOT_SUPPORTED
    for sensitivity in (
        EvidenceSensitivity.PRIVATE_SENSITIVE,
        EvidenceSensitivity.SECRET_FORBIDDEN,
    ):
        with pytest.raises(DurableContentError) as sensitivity_error:
            authority.prepare_structured(**(arguments | {"sensitivity": sensitivity}))
        assert sensitivity_error.value.code is DurableContentErrorCode.SENSITIVITY_DENIED


def test_historical_access_capability_is_owner_issued_and_purpose_fixed() -> None:
    authority = P1_6HistoricalContentAccessAuthority()
    foreign_authority = P1_6HistoricalContentAccessAuthority()
    valid = authority.issue_p1_8_structured_result_grant()
    forged = HistoricalContentAccessGrant(valid.consumer, valid.purpose)
    foreign = foreign_authority.issue_p1_8_structured_result_grant()

    assert authority.recognizes(valid)
    assert not authority.recognizes(forged)
    assert not authority.recognizes(foreign)
    assert valid.consumer == "P1_8"
    assert valid.purpose == "P1_8_STRUCTURED_RESULT_V1"
    assert "capability" not in repr(valid).lower()
    assert not hasattr(valid, "allow_internal")
    assert not hasattr(valid, "allow_public_safe_body")
    assert not hasattr(valid, "issue_p1_8_structured_result_grant")
    assert not hasattr(valid, "prepare_structured")


def test_requirement_v1_v2_fingerprint_schemas_are_explicit_and_stable() -> None:
    authority = TaskContractEvidenceAuthority("task-authority", "v1")
    legacy = authority.seal_requirement(requirement())
    assert legacy.fingerprint_schema is RequirementFingerprintSchema.V1
    assert legacy.durable_content_requirement is DurableContentRequirement.NOT_APPLICABLE
    assert set(_requirement_payload(legacy)).isdisjoint(
        {
            "fingerprint_schema",
            "durable_content_requirement",
            "durable_content_policy_ref",
            "durable_content_policy_fingerprint",
        }
    )
    assert legacy.fingerprint == "49357aeb14bea01d7798759efcb2d5a01b2b40bb119e547d4d30904e20919e46"
    checkpoint = authority.seal_checkpoint(
        EvidenceCheckpoint(
            ref=EvidenceCheckpointRef("pre-human", "v1"),
            task_contract_id="task",
            task_contract_version="v1",
            source_state=WorkflowState.ADMISSION_PENDING,
            target_state=WorkflowState.HUMAN_REQUIRED,
            transition_purpose_id=None,
            transition_purpose_version=None,
            requirement_set_id="set",
            requirement_set_version="v1",
            task_authority_id="task-authority",
            task_authority_version="v1",
            issued_at=NOW,
        )
    )
    legacy_set = authority.seal_set(
        EvidenceRequirementSet(
            requirement_set_id="set",
            requirement_set_version="v1",
            task_contract_id="task",
            task_contract_version="v1",
            ordered_requirement_refs=(legacy.ref.serialized(),),
            requirement_root_hash="",
            ordered_checkpoint_refs=(checkpoint.ref.serialized(),),
            semantic_owner=EvidenceSemanticOwner.P1_6_EVIDENCE,
            authority_version="AISCC-P1-6-EVIDENCE-AUTHORITY-V1",
            issued_at=NOW,
            fingerprint="",
        ),
        (legacy,),
        (checkpoint,),
    )
    assert legacy_set.requirement_root_hash == (
        "a96efb57072865db05d9ddd8d67cc2d8a98a227586d5a8ffa57a93e8ed553680"
    )

    v2 = authority.seal_requirement(
        replace(
            requirement(),
            ref=EvidenceRequirementRef("structured-result", "v2"),
            requirement_set_version="v2",
            fingerprint_schema=RequirementFingerprintSchema.V2_DURABLE_CONTENT,
            durable_content_requirement=DurableContentRequirement.REQUIRED,
            durable_content_policy_ref="p1-6-durable-policy@v1",
            durable_content_policy_fingerprint=POLICY_HASH,
        )
    )
    assert v2.fingerprint == "65203bafad4d439a002b6fe2b948bc8e44b7d7fbe3c40cb95e53c27b3565e502"
    assert v2.fingerprint != legacy.fingerprint
    assert _requirement_payload(v2)["fingerprint_schema"] == v2.fingerprint_schema.value


def test_v1_cannot_be_mutated_to_required() -> None:
    with pytest.raises(DurableContentError) as raised:
        TaskContractEvidenceAuthority("task-authority", "v1").seal_requirement(
            replace(
                requirement(),
                durable_content_requirement=DurableContentRequirement.REQUIRED,
                durable_content_policy_ref="p1-6-durable-policy@v1",
                durable_content_policy_fingerprint=POLICY_HASH,
            )
        )
    assert raised.value.code is DurableContentErrorCode.REQUIREMENT_LEGACY_IDENTITY_CONFLICT
