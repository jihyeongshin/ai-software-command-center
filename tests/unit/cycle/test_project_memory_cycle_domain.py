from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime

import pytest

from aiscc.cycle.models import (
    CycleAdmissionError,
    CycleAdmissionRequest,
    CycleCandidate,
    MemoryCategory,
    MemoryDeclaration,
)
from aiscc.memory.models import (
    CATEGORY_MODES,
    MemoryAuthorityMode,
    P1_8MemoryDeclarationPolicyAuthority,
    PrivacyClassification,
    ProjectMemoryError,
    VerifiedMemorySource,
    default_memory_policy,
    derive_memory_content,
    derive_memory_declaration,
    memory_content_fingerprint,
    memory_lineage_key,
    project_memory_entry_id,
)

NOW = datetime(2026, 8, 31, tzinfo=UTC)


def test_mcf_v1_fixed_vector() -> None:
    assert (
        memory_content_fingerprint(
            category=MemoryCategory.DECISION,
            authority_mode=MemoryAuthorityMode.STRUCTURED_RESULT_ATTESTED,
            policy_ref="p1-8-memory-policy:v1:project-memory-v1",
            normalized_derived_content={"outcome": "accepted", "revision": 7},
        )
        == "67bf89d7ebbe2fbf46a8edf8b6acf2fcd20ff998afcb2cb77b8d21f2be2388e8"
    )


def test_memory_lineage_key_v1_fixed_vector_and_stability() -> None:
    first = memory_lineage_key(
        project_id="aiscc-project",
        category=MemoryCategory.DECISION,
        subject_key="release",
        applicability_key="project:aiscc",
        semantic_slot="final",
    )
    assert first == "d7f57870a0443c1f0ff5a1cc463125d81be23f258b3c35075665bde166941662"
    assert first == memory_lineage_key(
        project_id="aiscc-project",
        category=MemoryCategory.DECISION,
        subject_key="release",
        applicability_key="project:aiscc",
        semantic_slot="final",
    )


def test_memory_entry_id_is_not_lineage_and_binds_cycle() -> None:
    lineage = "a" * 64
    first = project_memory_entry_id(
        cycle_id="cycle-1",
        memory_declaration_ordinal=1,
        policy_fingerprint="b" * 64,
        memory_lineage_key_value=lineage,
        content_fingerprint="c" * 64,
    )
    second = project_memory_entry_id(
        cycle_id="cycle-2",
        memory_declaration_ordinal=1,
        policy_fingerprint="b" * 64,
        memory_lineage_key_value=lineage,
        content_fingerprint="c" * 64,
    )
    assert first != lineage
    assert first != second


def test_different_semantic_slot_has_different_lineage() -> None:
    common = dict(
        project_id="aiscc-project",
        category=MemoryCategory.CONSTRAINT_POINTER,
        subject_key="deploy",
        applicability_key="project:aiscc",
    )
    assert memory_lineage_key(**common, semantic_slot="network") != memory_lineage_key(
        **common, semantic_slot="credentials"
    )


def test_lineage_atoms_reject_caller_free_text_and_noncanonical_unicode() -> None:
    with pytest.raises(ProjectMemoryError):
        memory_lineage_key(
            project_id="AISCC Project",
            category=MemoryCategory.DECISION,
            subject_key="release",
            applicability_key="project:aiscc",
            semantic_slot="final",
        )


def test_exact_category_mode_matrix_and_lesson_not_supported() -> None:
    assert CATEGORY_MODES == {
        MemoryCategory.DECISION: MemoryAuthorityMode.STRUCTURED_RESULT_ATTESTED,
        MemoryCategory.INVARIANT_POINTER: MemoryAuthorityMode.DETERMINISTIC_POINTER,
        MemoryCategory.CONSTRAINT_POINTER: MemoryAuthorityMode.DETERMINISTIC_POINTER,
        MemoryCategory.LESSON: MemoryAuthorityMode.NOT_SUPPORTED,
        MemoryCategory.BLOCKER_RESOLUTION: MemoryAuthorityMode.DETERMINISTIC_POINTER,
        MemoryCategory.PROVENANCE_POINTER: MemoryAuthorityMode.DETERMINISTIC_POINTER,
        MemoryCategory.NEXT_ACTION_CONTEXT: MemoryAuthorityMode.STRUCTURED_RESULT_ATTESTED,
    }
    policy = default_memory_policy(NOW)
    lesson = MemoryDeclaration(
        MemoryCategory.LESSON,
        "release",
        "project:aiscc",
        "lesson",
        policy.serialized_ref,
        policy.fingerprint,
        "0" * 64,
    )
    with pytest.raises(CycleAdmissionError, match="NOT_SUPPORTED"):
        derive_memory_content(
            lesson,
            policy,
            structured_source=None,
            accepted_pointer_refs=frozenset(),
        )


def test_structured_memory_is_reconstructed_not_caller_authored() -> None:
    policy = default_memory_policy(NOW)
    actual = {"outcome": "accepted", "reason": "human-review"}
    fingerprint = memory_content_fingerprint(
        category=MemoryCategory.DECISION,
        authority_mode=MemoryAuthorityMode.STRUCTURED_RESULT_ATTESTED,
        policy_ref=policy.serialized_ref,
        normalized_derived_content=actual,
    )
    declaration = MemoryDeclaration(
        MemoryCategory.DECISION,
        "release",
        "project:aiscc",
        "final",
        policy.serialized_ref,
        policy.fingerprint,
        fingerprint,
        "p1-6-admitted:v1:source",
        "/decision",
    )
    mode, derived, value = derive_memory_content(
        declaration,
        policy,
        structured_source={"decision": actual, "untrusted": "ignored"},
        accepted_pointer_refs=frozenset(),
    )
    assert mode is MemoryAuthorityMode.STRUCTURED_RESULT_ATTESTED
    assert derived == actual and value == fingerprint
    with pytest.raises(ProjectMemoryError):
        derive_memory_content(
            replace(declaration, claimed_content_fingerprint="f" * 64),
            policy,
            structured_source={"decision": actual},
            accepted_pointer_refs=frozenset(),
        )


def test_deterministic_pointer_must_be_terminal_bound() -> None:
    policy = default_memory_policy(NOW)
    pointer = "terminal-transition"
    fingerprint = memory_content_fingerprint(
        category=MemoryCategory.PROVENANCE_POINTER,
        authority_mode=MemoryAuthorityMode.DETERMINISTIC_POINTER,
        policy_ref=policy.serialized_ref,
        normalized_derived_content={"authority_ref": pointer},
    )
    declaration = MemoryDeclaration(
        MemoryCategory.PROVENANCE_POINTER,
        "release",
        "project:aiscc",
        "transition",
        policy.serialized_ref,
        policy.fingerprint,
        fingerprint,
        pointer_ref=pointer,
    )
    with pytest.raises(ProjectMemoryError):
        derive_memory_content(
            declaration,
            policy,
            structured_source=None,
            accepted_pointer_refs=frozenset({"other"}),
        )
    assert (
        derive_memory_content(
            declaration,
            policy,
            structured_source=None,
            accepted_pointer_refs=frozenset({pointer}),
        )[2]
        == fingerprint
    )


def test_cycle_candidate_and_request_fingerprints_are_canonical() -> None:
    policy = default_memory_policy(NOW)
    declaration = MemoryDeclaration(
        MemoryCategory.PROVENANCE_POINTER,
        "release",
        "project:aiscc",
        "transition",
        policy.serialized_ref,
        policy.fingerprint,
        "a" * 64,
        pointer_ref="transition-1",
    )
    candidate = CycleCandidate(
        "cycle-1",
        "v1",
        "aiscc-project",
        "task-1",
        "v1",
        "b" * 64,
        "run-1",
        5,
        "request-1",
        "decision-1",
        "c" * 64,
        "p1-7-judgment:v1:judgment-1",
        "d" * 64,
        "p1-6-attestation:v1:attestation-1",
        "e" * 64,
        (declaration,),
        "task-constraint:v1:constraint-1",
        "f" * 64,
        "task-constraint-owner-snapshot:v1:snapshot-1",
        "0" * 64,
        1,
    )
    request = CycleAdmissionRequest("admit-1", "v1", candidate, "system", NOW)
    assert len(candidate.fingerprint) == 64
    assert request.fingerprint == replace(request).fingerprint
    assert replace(candidate, terminal_state_version=6).fingerprint != candidate.fingerprint


def test_policy_seal_owner_derived_lineage_and_privacy_fail_closed() -> None:
    authority = P1_8MemoryDeclarationPolicyAuthority()
    policy = authority.issue_v1(NOW)
    assert authority.recognizes(policy)
    assert not P1_8MemoryDeclarationPolicyAuthority().recognizes(policy)
    assert not authority.recognizes(replace(policy, authority_revision=2))

    source = VerifiedMemorySource(
        "P1_6_ADMITTED_STRUCTURED_RESULT",
        "p1-6-admitted:v1:source",
        "a" * 64,
        "result-object",
        "AISCC-PROOF",
        "v1",
        PrivacyClassification.NON_EXPORTABLE,
        "aiscc-project",
        "task-1",
        {"decision": {"outcome": "accepted"}},
    )
    content_fingerprint = memory_content_fingerprint(
        category=MemoryCategory.DECISION,
        authority_mode=MemoryAuthorityMode.STRUCTURED_RESULT_ATTESTED,
        policy_ref=policy.serialized_ref,
        normalized_derived_content={"outcome": "accepted"},
    )
    declaration = MemoryDeclaration(
        MemoryCategory.DECISION,
        "task-contract:task-1",
        "project:aiscc-project",
        "decision/aiscc-proof/terminal-decision",
        policy.serialized_ref,
        policy.fingerprint,
        content_fingerprint,
        source_evidence_ref=source.authority_ref,
        source_selector="/decision",
        source_object_kind=source.object_kind,
        source_schema_id=source.schema_id,
        source_schema_version=source.schema_version,
    )
    derived = derive_memory_declaration(declaration, policy, source=source)
    assert derived.privacy is PrivacyClassification.NON_EXPORTABLE
    with pytest.raises(ProjectMemoryError, match="SOURCE_MISMATCH"):
        derive_memory_declaration(
            replace(declaration, subject_key="task-contract:other"), policy, source=source
        )
