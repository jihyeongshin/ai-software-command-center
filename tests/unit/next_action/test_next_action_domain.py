from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime

import pytest

from aiscc.contracts.canonical_json import canonical_sha256
from aiscc.next_action.models import (
    CATALOG_FINGERPRINT,
    CATALOG_REF,
    ELIGIBILITY_POLICY_FINGERPRINT,
    OPERATIONAL_DESCRIPTOR_FINGERPRINT,
    SELECTION_POLICY_FINGERPRINT,
    TASK_ISSUANCE_OWNER,
    HumanInputKind,
    NextActionDescriptor,
    NextActionError,
    NextActionProposal,
    P1_8NextActionPolicyAuthority,
    TaskIssuanceCandidate,
    ranking_key,
)
from aiscc.task_authority.models import NextActionPriorityClass
from aiscc.task_authority.repository import _new_context

NOW = datetime(2026, 9, 2, 1, 2, 3, 456789, tzinfo=UTC)


def configured() -> tuple[
    P1_8NextActionPolicyAuthority,
    object,
    object,
    NextActionDescriptor,
]:
    authority = P1_8NextActionPolicyAuthority()
    eligibility, selection, descriptors = authority.issue_policy_catalog_v1(now=NOW)
    return authority, eligibility, selection, descriptors[0]


def operational_proposal(
    value: NextActionDescriptor, proposal_id: str, **claims: object
) -> NextActionProposal:
    return NextActionProposal(
        proposal_id,
        "aiscc-project",
        value.action_ref,
        {
            "observed_state": "BLOCKED",
            "observed_state_version": 3,
            "operational_fact_fingerprint": "a" * 64,
            "operational_fact_ref": "p1-4-blocker:v1:blocker-1",
            "operational_work_run_id": "run-1",
        },
        "non-authoritative rationale",
        **claims,
    )


def test_caller_cannot_define_catalog_or_mint_template_action_ref() -> None:
    authority = P1_8NextActionPolicyAuthority()
    with pytest.raises(TypeError):
        authority.issue_policy_catalog_v1(  # type: ignore[call-arg]
            catalog_id="rogue", actions=(), now=NOW
        )
    _, _, _, descriptor = configured()
    assert descriptor.action_ref.action_id == "open-operational-recovery-task-issuance"
    assert "7b766d3d3f3062381" not in descriptor.action_ref.serialized


def test_exact_fixed_policy_catalog_descriptor_and_action_ref_identities() -> None:
    authority, eligibility, selection, descriptor = configured()
    assert descriptor.source_authority_ref == CATALOG_REF
    assert descriptor.source_authority_fingerprint == CATALOG_FINGERPRINT
    assert descriptor.fingerprint == OPERATIONAL_DESCRIPTOR_FINGERPRINT
    assert eligibility.fingerprint == ELIGIBILITY_POLICY_FINGERPRINT
    assert selection.fingerprint == SELECTION_POLICY_FINGERPRINT
    assert (
        canonical_sha256(
            {
                "eligibility_policy_id": descriptor.action_ref.eligibility_policy_id,
                "eligibility_policy_version": descriptor.action_ref.eligibility_policy_version,
                "action_id": descriptor.action_ref.action_id,
                "action_version": descriptor.action_ref.action_version,
                "descriptor_fingerprint": descriptor.action_ref.descriptor_fingerprint,
            }
        )
        == "a6a272fc7757439b7cc0877ace775d091539c25a4c3be8c0cd973cf2b746f157"
    )
    assert authority.recognizes_policy(eligibility)  # type: ignore[arg-type]
    assert authority.recognizes_policy(selection)  # type: ignore[arg-type]
    assert authority.recognizes_descriptor(descriptor)


def test_proposal_claims_are_audit_only_and_six_field_tuple_is_exact() -> None:
    _, _, _, descriptor = configured()
    asserted = operational_proposal(
        descriptor,
        "proposal-z",
        claimed_priority=0,
        claimed_security=True,
        claimed_blocker=True,
    )
    ordinary = operational_proposal(descriptor, "proposal-a")
    asserted_key = ranking_key(asserted, descriptor, authoritative_priority_rank=3)
    ordinary_key = ranking_key(ordinary, descriptor, authoritative_priority_rank=1)
    assert len(asserted_key) == 6
    assert ordinary_key < asserted_key
    assert asserted_key[-1] == "proposal-z"


def test_descriptor_parameter_schema_is_eligibility_authority() -> None:
    _, _, _, descriptor = configured()
    malformed = replace(
        operational_proposal(descriptor, "proposal"),
        parameters={"observed_state": "BLOCKED"},
    )
    with pytest.raises(NextActionError, match="parameters differ"):
        ranking_key(malformed, descriptor)


def test_context_descriptor_enrolls_external_owner_class_and_ordinal_only() -> None:
    authority, _, selection, _ = configured()
    context = _new_context(
        context_ref_id="context-1",
        context_logical_id="next-action-context-lineage:v1:planning-1",
        project_id="aiscc-project",
        task_contract_id="task-1",
        task_contract_version="v1",
        context_slot_id="primary",
        priority_class=NextActionPriorityClass.OPERATIONAL_HARDENING,
        critical_path_ordinal=7,
        issued_at=NOW,
        issuance_sequence=1,
        effective_sequence=1,
    )
    descriptor = authority.issue_context_bound_descriptor(
        context=context, issuance_event_sequence=1
    )
    assert authority.recognizes_descriptor(descriptor)
    assert descriptor.priority_rank == 0
    assert descriptor.critical_path_ordinal == context.critical_path_ordinal
    assert dict(selection.class_to_rank)[context.priority_class.value] == 5
    assert descriptor.canonical_payload is not None
    assert descriptor.canonical_payload["priority_classification_source_ref"] == (
        context.context_ref
    )
    assert not authority.recognizes_descriptor(replace(descriptor, critical_path_ordinal=8))


def test_task_issuance_candidate_has_fixed_external_owner_and_no_task_contract() -> None:
    _, _, _, descriptor = configured()
    candidate = TaskIssuanceCandidate(
        "candidate",
        "p1-8-next-action-selection:v1:selection",
        descriptor.action_ref,
        {},
        TASK_ISSUANCE_OWNER,
        HumanInputKind.AFTER_TASK_ISSUANCE_P1_7,
        NOW,
    )
    assert candidate.issuance_owner == "EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY"
    assert not hasattr(candidate, "task_contract")
    with pytest.raises(ValueError):
        replace(candidate, issuance_owner="P1_8")


def test_authority_seal_cannot_be_substituted() -> None:
    authority, eligibility, _, descriptor = configured()
    assert not P1_8NextActionPolicyAuthority().recognizes_policy(eligibility)  # type: ignore[arg-type]
    assert not authority.recognizes_descriptor(replace(descriptor, dependency_ordinal=99))
