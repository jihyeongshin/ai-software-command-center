from __future__ import annotations

from dataclasses import replace
from datetime import datetime

from aiscc.evidence.models import (
    EvidenceCheckpoint,
    EvidenceRequirement,
    EvidenceRequirementProfile,
    EvidenceRequirementSet,
    EvidenceSemanticOwner,
    RequirementObligation,
    canonical_hash,
)

_OBLIGATION = {
    EvidenceRequirementProfile.EXECUTOR_REQUIRED: RequirementObligation.REQUIRED,
    EvidenceRequirementProfile.REUSE_ALLOWED: RequirementObligation.REQUIRED,
    EvidenceRequirementProfile.HUMAN_OWNED: RequirementObligation.REQUIRED,
    EvidenceRequirementProfile.NOT_REQUIRED: RequirementObligation.NOT_REQUIRED,
    EvidenceRequirementProfile.FORBIDDEN: RequirementObligation.FORBIDDEN,
}


class TaskContractEvidenceAuthority:
    """System-only issuer for immutable requirement/checkpoint snapshots."""

    def __init__(self, authority_id: str, authority_version: str) -> None:
        if not authority_id or not authority_version:
            raise ValueError("TaskContract evidence authority identity is required")
        self.authority_id = authority_id
        self.authority_version = authority_version
        self._issuer_token = object()

    def seal_requirement(self, value: EvidenceRequirement) -> EvidenceRequirement:
        if value.semantic_owner is not EvidenceSemanticOwner.P1_6_EVIDENCE:
            raise ValueError("requirement semantic owner must be P1_6_EVIDENCE")
        if value.obligation is not _OBLIGATION[value.profile]:
            raise ValueError("requirement profile/obligation mismatch")
        payload = _requirement_payload(value)
        return replace(value, fingerprint=canonical_hash(payload), _issuer_token=self._issuer_token)

    def seal_checkpoint(self, value: EvidenceCheckpoint) -> EvidenceCheckpoint:
        payload = _checkpoint_payload(value)
        return replace(value, fingerprint=canonical_hash(payload), _issuer_token=self._issuer_token)

    def seal_set(
        self,
        value: EvidenceRequirementSet,
        requirements: tuple[EvidenceRequirement, ...],
        checkpoints: tuple[EvidenceCheckpoint, ...],
    ) -> EvidenceRequirementSet:
        if any(item._issuer_token is not self._issuer_token for item in requirements):
            raise ValueError("unrecognized requirement issuer")
        if any(item._issuer_token is not self._issuer_token for item in checkpoints):
            raise ValueError("unrecognized checkpoint issuer")
        requirement_refs = tuple(item.ref.serialized() for item in requirements)
        checkpoint_refs = tuple(item.ref.serialized() for item in checkpoints)
        if value.ordered_requirement_refs != requirement_refs:
            raise ValueError("RequirementSet ordered requirement refs mismatch")
        if value.ordered_checkpoint_refs != checkpoint_refs:
            raise ValueError("RequirementSet ordered checkpoint refs mismatch")
        root = canonical_hash([(item.ref.serialized(), item.fingerprint) for item in requirements])
        if value.requirement_root_hash and value.requirement_root_hash != root:
            raise ValueError("RequirementSet root mismatch")
        sealed = replace(value, requirement_root_hash=root)
        return replace(
            sealed,
            fingerprint=canonical_hash(_set_payload(sealed)),
            _issuer_token=self._issuer_token,
        )

    def recognizes(self, value: object) -> bool:
        return getattr(value, "_issuer_token", None) is self._issuer_token


def _requirement_payload(value: EvidenceRequirement) -> dict[str, object]:
    return {
        "ref": value.ref.serialized(),
        "task": [value.task_contract_id, value.task_contract_version],
        "set": [value.requirement_set_id, value.requirement_set_version],
        "owner": value.semantic_owner.value,
        "profile": value.profile.value,
        "obligation": value.obligation.value,
        "checkpoints": list(value.applicable_checkpoint_refs),
        "type": [value.evidence_type_id, value.evidence_type_version],
        "issuer_types": sorted(item.value for item in value.allowed_issuer_types),
        "issuer_ids": sorted(value.allowed_issuer_ids),
        "human_categories": sorted(item.value for item in value.allowed_human_categories),
        "content_kinds": sorted(item.value for item in value.allowed_content_kinds),
        "schema": [value.schema_id, value.schema_version],
        "subject": value.subject_id,
        "scope": value.scope_id,
        "resource": value.resource_id,
        "freshness": {
            "kind": value.freshness_policy.kind.value,
            "max_age_seconds": value.freshness_policy.max_age_seconds,
            "config_version": value.freshness_policy.config_version,
        },
        "coverage": sorted(value.required_coverage),
        "reuse_maximum": value.reuse_maximum,
        "compatible": sorted(value.compatible_requirement_refs),
        "maximum_sensitivity": value.maximum_sensitivity.value,
        "public_export_allowed": value.public_export_allowed,
        "issued_at": value.issued_at.isoformat(),
        "revoked_at": value.revoked_at.isoformat() if value.revoked_at else None,
        "supersedes": value.supersedes_requirement_ref,
    }


def _checkpoint_payload(value: EvidenceCheckpoint) -> dict[str, object]:
    return {
        "ref": value.ref.serialized(),
        "task": [value.task_contract_id, value.task_contract_version],
        "source": value.source_state.value,
        "target": value.target_state.value if value.target_state else None,
        "purpose": [value.transition_purpose_id, value.transition_purpose_version],
        "set": [value.requirement_set_id, value.requirement_set_version],
        "authority": [value.task_authority_id, value.task_authority_version],
        "issued_at": value.issued_at.isoformat(),
        "revoked_at": value.revoked_at.isoformat() if value.revoked_at else None,
        "supersedes": value.supersedes_checkpoint_ref,
    }


def _set_payload(value: EvidenceRequirementSet) -> dict[str, object]:
    return {
        "set": [value.requirement_set_id, value.requirement_set_version],
        "task": [value.task_contract_id, value.task_contract_version],
        "requirements": list(value.ordered_requirement_refs),
        "root": value.requirement_root_hash,
        "checkpoints": list(value.ordered_checkpoint_refs),
        "owner": value.semantic_owner.value,
        "authority_version": value.authority_version,
        "issued_at": value.issued_at.isoformat(),
        "revoked_at": value.revoked_at.isoformat() if value.revoked_at else None,
        "supersedes": value.supersedes_set_ref,
    }


def authority_timestamp(value: datetime) -> str:
    return value.isoformat()
