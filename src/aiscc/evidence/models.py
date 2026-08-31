from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from aiscc.contracts.workflow import WorkflowState


class EvidenceAdmissionOutcome(StrEnum):
    ADMITTED = "ADMITTED"
    REJECTED = "REJECTED"


class EvidenceSetOutcome(StrEnum):
    SATISFIED = "SATISFIED"
    UNSATISFIED = "UNSATISFIED"


class RequirementSatisfaction(StrEnum):
    SATISFIED = "SATISFIED"
    UNSATISFIED = "UNSATISFIED"


class EvidenceRequirementProfile(StrEnum):
    EXECUTOR_REQUIRED = "EXECUTOR_REQUIRED"
    REUSE_ALLOWED = "REUSE_ALLOWED"
    HUMAN_OWNED = "HUMAN_OWNED"
    NOT_REQUIRED = "NOT_REQUIRED"
    FORBIDDEN = "FORBIDDEN"


class RequirementObligation(StrEnum):
    REQUIRED = "REQUIRED"
    NOT_REQUIRED = "NOT_REQUIRED"
    FORBIDDEN = "FORBIDDEN"


class HumanEvidenceProducerCategory(StrEnum):
    HUMAN_DIRECT_EVIDENCE = "HUMAN_DIRECT_EVIDENCE"
    HUMAN_P1_7 = "HUMAN_P1_7"


class EvidenceSensitivity(StrEnum):
    PUBLIC_SAFE = "PUBLIC_SAFE"
    INTERNAL = "INTERNAL"
    PRIVATE_SENSITIVE = "PRIVATE_SENSITIVE"
    SECRET_FORBIDDEN = "SECRET_FORBIDDEN"


class EvidenceDimensionOutcome(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class EvidenceSemanticOwner(StrEnum):
    P1_6_EVIDENCE = "P1_6_EVIDENCE"


class RequirementFingerprintSchema(StrEnum):
    V1 = "P1_6_EVIDENCE_REQUIREMENT_FINGERPRINT_V1"
    V2_DURABLE_CONTENT = "P1_6_EVIDENCE_REQUIREMENT_FINGERPRINT_V2_DURABLE_CONTENT"


class DurableContentRequirement(StrEnum):
    NOT_APPLICABLE = "NOT_APPLICABLE"
    REQUIRED = "REQUIRED"


class DurableContentErrorCode(StrEnum):
    REQUIRED = "DURABLE_CONTENT_REQUIRED"
    KIND_NOT_SUPPORTED = "DURABLE_CONTENT_KIND_NOT_SUPPORTED"
    TOO_LARGE = "DURABLE_CONTENT_TOO_LARGE"
    SENSITIVITY_DENIED = "DURABLE_CONTENT_SENSITIVITY_DENIED"
    IDENTITY_CONFLICT = "DURABLE_CONTENT_IDENTITY_CONFLICT"
    MISSING = "DURABLE_CONTENT_MISSING"
    INTEGRITY_MISMATCH = "DURABLE_CONTENT_INTEGRITY_MISMATCH"
    SCHEMA_MISMATCH = "DURABLE_CONTENT_SCHEMA_MISMATCH"
    ACCESS_DENIED = "DURABLE_CONTENT_ACCESS_DENIED"
    REQUIREMENT_SCHEMA_UNKNOWN = "DURABLE_CONTENT_REQUIREMENT_SCHEMA_UNKNOWN"
    REQUIREMENT_FINGERPRINT_MISMATCH = "DURABLE_CONTENT_REQUIREMENT_FINGERPRINT_MISMATCH"
    REQUIREMENT_LEGACY_IDENTITY_CONFLICT = (
        "DURABLE_CONTENT_REQUIREMENT_LEGACY_IDENTITY_CONFLICT"
    )
    P1_8_SOURCE_NOT_DURABLE = "P1_8_STRUCTURED_SOURCE_NOT_DURABLE"


class EvidenceIssuerType(StrEnum):
    P1_5_EXECUTION_SUBMISSION = "P1_5_EXECUTION_SUBMISSION"
    P1_5_AGENT_OUTPUT = "P1_5_AGENT_OUTPUT"
    P1_5_TOOL_OUTPUT = "P1_5_TOOL_OUTPUT"
    P1_5_EXECUTION_ARTIFACT = "P1_5_EXECUTION_ARTIFACT"
    SYSTEM_STATIC_PROOF = "SYSTEM_STATIC_PROOF"
    SYSTEM_BUILD_PROOF = "SYSTEM_BUILD_PROOF"
    SYSTEM_DATABASE_OBSERVATION = "SYSTEM_DATABASE_OBSERVATION"
    SYSTEM_RUNTIME_OBSERVATION = "SYSTEM_RUNTIME_OBSERVATION"
    HUMAN_DIRECT_EVIDENCE = "HUMAN_DIRECT_EVIDENCE"
    HUMAN_P1_7 = "HUMAN_P1_7"
    PRIOR_ADMITTED_EVIDENCE = "PRIOR_ADMITTED_EVIDENCE"


class EvidenceContentKind(StrEnum):
    INLINE_CANONICAL_STRUCTURED_BODY = "INLINE_CANONICAL_STRUCTURED_BODY"
    CONTENT_ADDRESSED_ARTIFACT_REF = "CONTENT_ADDRESSED_ARTIFACT_REF"
    P1_5_IMMUTABLE_PRODUCER_REF = "P1_5_IMMUTABLE_PRODUCER_REF"
    DATABASE_OBSERVATION_REF = "DATABASE_OBSERVATION_REF"
    RUNTIME_OBSERVATION_REF = "RUNTIME_OBSERVATION_REF"
    HUMAN_STRUCTURED_REF = "HUMAN_STRUCTURED_REF"
    PRIOR_ADMITTED_EVIDENCE_REF = "PRIOR_ADMITTED_EVIDENCE_REF"


class FreshnessPolicyKind(StrEnum):
    IMMUTABLE_BUILD_ARTIFACT = "IMMUTABLE_BUILD_ARTIFACT"
    TASK_EXECUTION_SCOPED = "TASK_EXECUTION_SCOPED"
    WORKRUN_STATE_VERSION_SCOPED = "WORKRUN_STATE_VERSION_SCOPED"
    TIME_WINDOW = "TIME_WINDOW"
    CONFIG_VERSION_SCOPED = "CONFIG_VERSION_SCOPED"
    HUMAN_RESULT_SCOPED = "HUMAN_RESULT_SCOPED"


class EvidenceAdmissionDimension(StrEnum):
    REQUIREMENT_MATCH = "REQUIREMENT_MATCH"
    ISSUER_AUTHORITY = "ISSUER_AUTHORITY"
    TYPE = "TYPE"
    TASK_CONTRACT_BINDING = "TASK_CONTRACT_BINDING"
    CHECKPOINT_BINDING = "CHECKPOINT_BINDING"
    HUMAN_PRODUCER_CATEGORY = "HUMAN_PRODUCER_CATEGORY"
    SUBJECT_SCOPE = "SUBJECT_SCOPE"
    RESOURCE_BINDING = "RESOURCE_BINDING"
    CONTENT_INTEGRITY = "CONTENT_INTEGRITY"
    SCHEMA_FORMAT = "SCHEMA_FORMAT"
    FRESHNESS = "FRESHNESS"
    APPLICABILITY = "APPLICABILITY"
    COVERAGE = "COVERAGE"
    SENSITIVITY_POLICY = "SENSITIVITY_POLICY"
    REUSE_POLICY = "REUSE_POLICY"
    REVOCATION_SUPERSESSION = "REVOCATION_SUPERSESSION"
    DUPLICATE_IDEMPOTENCY = "DUPLICATE_IDEMPOTENCY"


class EvidenceRejectionReason(StrEnum):
    ADMITTED = "ADMITTED"
    UNKNOWN_REQUIREMENT = "UNKNOWN_REQUIREMENT"
    REQUIREMENT_VERSION_MISMATCH = "REQUIREMENT_VERSION_MISMATCH"
    CHECKPOINT_MISMATCH = "CHECKPOINT_MISMATCH"
    FORBIDDEN_EVIDENCE = "FORBIDDEN_EVIDENCE"
    ISSUER_NOT_AUTHORIZED = "ISSUER_NOT_AUTHORIZED"
    HUMAN_PRODUCER_CATEGORY_MISMATCH = "HUMAN_PRODUCER_CATEGORY_MISMATCH"
    TASK_CONTRACT_MISMATCH = "TASK_CONTRACT_MISMATCH"
    SUBJECT_SCOPE_MISMATCH = "SUBJECT_SCOPE_MISMATCH"
    RESOURCE_MISMATCH = "RESOURCE_MISMATCH"
    TYPE_MISMATCH = "TYPE_MISMATCH"
    CONTENT_MISSING = "CONTENT_MISSING"
    CONTENT_HASH_MISMATCH = "CONTENT_HASH_MISMATCH"
    SCHEMA_INVALID = "SCHEMA_INVALID"
    STALE = "STALE"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    INSUFFICIENT_COVERAGE = "INSUFFICIENT_COVERAGE"
    REUSE_NOT_ALLOWED = "REUSE_NOT_ALLOWED"
    REUSE_INCOMPATIBLE = "REUSE_INCOMPATIBLE"
    REVOKED_OR_SUPERSEDED = "REVOKED_OR_SUPERSEDED"
    HUMAN_OWNED_REQUIRED = "HUMAN_OWNED_REQUIRED"
    DUPLICATE_IDENTITY_CONFLICT = "DUPLICATE_IDENTITY_CONFLICT"
    AUTHORITY_CONFLICT = "AUTHORITY_CONFLICT"


class EvidenceAuthorityEventKind(StrEnum):
    REVOKED = "REVOKED"
    SUPERSEDED = "SUPERSEDED"
    CORRECTED = "CORRECTED"


class EvidenceAuthorityConflictError(RuntimeError):
    """Durable P1-6 authority is missing, ambiguous, or inconsistent."""


class EvidenceIdentityConflictError(RuntimeError):
    """An immutable P1-6 identity was reused with different content."""


class DurableContentError(EvidenceAuthorityConflictError):
    """Typed fail-closed durable-content authority failure."""

    def __init__(self, code: DurableContentErrorCode, message: str) -> None:
        super().__init__(f"{code.value}: {message}")
        self.code = code


@dataclass(frozen=True, slots=True)
class AuthoritativeWorkRunSnapshot:
    """System-owned WorkRun authority observed under the P1-4 transaction lock."""

    work_run_id: str
    task_contract_id: str
    task_contract_version: str
    workflow_state: WorkflowState
    state_version: int
    authority_ref: str
    authority_version: str


@dataclass(frozen=True, slots=True)
class EvidenceOwner:
    owner_type: EvidenceIssuerType
    owner_id: str
    owner_version: str
    authority_ref: str


@dataclass(frozen=True, slots=True)
class EvidenceCheckpointRef:
    checkpoint_id: str
    checkpoint_version: str

    def serialized(self) -> str:
        return f"{self.checkpoint_id}@{self.checkpoint_version}"


@dataclass(frozen=True, slots=True)
class EvidenceRequirementRef:
    requirement_id: str
    requirement_version: str

    def serialized(self) -> str:
        return f"{self.requirement_id}@{self.requirement_version}"


@dataclass(frozen=True, slots=True)
class EvidenceCheckpoint:
    ref: EvidenceCheckpointRef
    task_contract_id: str
    task_contract_version: str
    source_state: WorkflowState
    target_state: WorkflowState | None
    transition_purpose_id: str | None
    transition_purpose_version: str | None
    requirement_set_id: str
    requirement_set_version: str
    task_authority_id: str
    task_authority_version: str
    issued_at: datetime
    revoked_at: datetime | None = None
    supersedes_checkpoint_ref: str | None = None
    fingerprint: str = ""
    _issuer_token: object = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        target = self.target_state is not None
        purpose = bool(self.transition_purpose_id and self.transition_purpose_version)
        if target == purpose:
            raise ValueError("checkpoint requires exactly one target or transition purpose")
        _require_aware(self.issued_at)


@dataclass(frozen=True, slots=True)
class FreshnessPolicy:
    kind: FreshnessPolicyKind
    max_age_seconds: int | None = None
    config_version: str | None = None


@dataclass(frozen=True, slots=True)
class EvidenceRequirement:
    ref: EvidenceRequirementRef
    task_contract_id: str
    task_contract_version: str
    requirement_set_id: str
    requirement_set_version: str
    semantic_owner: EvidenceSemanticOwner
    profile: EvidenceRequirementProfile
    obligation: RequirementObligation
    applicable_checkpoint_refs: tuple[str, ...]
    evidence_type_id: str
    evidence_type_version: str
    allowed_issuer_types: frozenset[EvidenceIssuerType]
    allowed_issuer_ids: frozenset[str]
    allowed_human_categories: frozenset[HumanEvidenceProducerCategory]
    allowed_content_kinds: frozenset[EvidenceContentKind]
    schema_id: str
    schema_version: str
    subject_id: str
    scope_id: str
    resource_id: str | None
    freshness_policy: FreshnessPolicy
    required_coverage: frozenset[str]
    reuse_maximum: int
    compatible_requirement_refs: frozenset[str]
    maximum_sensitivity: EvidenceSensitivity
    public_export_allowed: bool
    issued_at: datetime
    fingerprint: str
    revoked_at: datetime | None = None
    supersedes_requirement_ref: str | None = None
    _issuer_token: object = field(default=None, repr=False, compare=False)
    fingerprint_schema: RequirementFingerprintSchema = RequirementFingerprintSchema.V1
    durable_content_requirement: DurableContentRequirement = (
        DurableContentRequirement.NOT_APPLICABLE
    )
    durable_content_policy_ref: str | None = None
    durable_content_policy_fingerprint: str | None = None


@dataclass(frozen=True, slots=True)
class EvidenceRequirementSet:
    requirement_set_id: str
    requirement_set_version: str
    task_contract_id: str
    task_contract_version: str
    ordered_requirement_refs: tuple[str, ...]
    requirement_root_hash: str
    ordered_checkpoint_refs: tuple[str, ...]
    semantic_owner: EvidenceSemanticOwner
    authority_version: str
    issued_at: datetime
    fingerprint: str
    revoked_at: datetime | None = None
    supersedes_set_ref: str | None = None
    _issuer_token: object = field(default=None, repr=False, compare=False)


@dataclass(frozen=True, slots=True)
class EvidenceContentRef:
    content_kind: EvidenceContentKind
    owner_id: str
    owner_version: str
    object_id: str
    object_version: str
    canonicalization: str
    schema_id: str
    schema_version: str
    byte_count: int
    content_hash: str
    sensitivity: EvidenceSensitivity
    retention_policy: str
    access_policy: str
    _owner_token: object = field(default=None, repr=False, compare=False)


@dataclass(frozen=True, slots=True)
class DurableEvidenceContentObject:
    serialized_ref: str
    content_identity_key: str
    owner_id: str
    owner_version: str
    source_owner_authority_ref: str
    source_owner_authority_fingerprint: str
    object_id: str
    object_version: str
    content_kind: EvidenceContentKind
    canonicalization: str
    schema_id: str
    schema_version: str
    byte_count: int
    content_hash_algorithm: str
    content_hash: str
    sensitivity: EvidenceSensitivity
    retention_policy: str
    access_policy: str
    canonical_body_bytes: bytes
    created_at: datetime
    content_authority_id: str
    content_authority_version: str
    content_authority_revision: int
    payload_fingerprint_schema: str
    payload_fingerprint: str


@dataclass(frozen=True, slots=True)
class EvidenceCandidateDurableContentBinding:
    candidate_id: str
    candidate_version: str
    candidate_fingerprint: str
    durable_content_ref: str
    durable_content_payload_fingerprint: str
    content_ref_metadata_fingerprint: str
    requirement_ref: str
    requirement_fingerprint_schema: RequirementFingerprintSchema
    requirement_fingerprint: str
    requirement_set_ref: str
    requirement_root_hash: str
    durable_content_policy_ref: str
    durable_content_policy_fingerprint: str
    bound_at: datetime
    binding_fingerprint: str


@dataclass(frozen=True, slots=True)
class HistoricalContentAccessGrant:
    consumer: str
    purpose: str = ""
    _capability_token: object = field(default_factory=object, repr=False, compare=False)


@dataclass(frozen=True, slots=True)
class VerifiedHistoricalContentMetadata:
    content: DurableEvidenceContentObject


@dataclass(frozen=True, slots=True)
class VerifiedHistoricalContent:
    metadata: VerifiedHistoricalContentMetadata
    canonical_body_bytes: bytes


EvidenceBodyRef = EvidenceContentRef


@dataclass(frozen=True, slots=True)
class HumanDirectEvidenceIngressRef:
    ingress_record_id: str
    ingress_record_version: str
    fingerprint: str

    def serialized(self) -> str:
        return (
            f"p1-6-human-ingress:{self.ingress_record_version}:"
            f"{self.ingress_record_id}:{self.fingerprint}"
        )


@dataclass(frozen=True, slots=True)
class HumanDirectEvidenceIngress:
    ref: HumanDirectEvidenceIngressRef
    candidate_id: str
    candidate_version: str
    authenticated_principal_id: str
    authenticated_session_id: str
    principal_authority_id: str
    principal_authority_version: str
    authenticated_at: datetime
    ingress_authority_id: str
    ingress_authority_version: str
    task_contract_id: str
    task_contract_version: str
    work_run_id: str
    checkpoint_ref: EvidenceCheckpointRef
    evidence_type_id: str
    evidence_type_version: str
    subject_id: str
    scope_id: str
    resource_id: str | None
    content_ref: EvidenceContentRef
    provided_at: datetime
    issued_at: datetime
    issuer_authenticity_ref: str
    _issuer_token: object = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        _require_aware(self.authenticated_at)
        _require_aware(self.provided_at)
        _require_aware(self.issued_at)


@dataclass(frozen=True, slots=True)
class EvidenceCandidate:
    candidate_id: str
    candidate_version: str
    candidate_fingerprint: str
    issuer: EvidenceOwner
    producer_work_run_id: str | None
    execution_attempt_id: str | None
    operation_id: str | None
    task_contract_id: str
    task_contract_version: str
    checkpoint_ref: EvidenceCheckpointRef
    observed_state: WorkflowState
    observed_state_version: int
    subject_id: str
    scope_id: str
    resource_id: str | None
    evidence_type_id: str
    evidence_type_version: str
    content_ref: EvidenceContentRef
    created_at: datetime
    observed_at: datetime
    coverage: frozenset[str]
    producer_attestation_ref: str
    human_producer_category: HumanEvidenceProducerCategory | None = None
    human_ingress_record_ref: str | None = None
    prior_admitted_evidence_ref: str | None = None
    config_version: str | None = None
    _issuer_token: object = field(default=None, repr=False, compare=False)


@dataclass(frozen=True, slots=True)
class EvidenceCandidateRef:
    candidate_id: str
    candidate_version: str
    candidate_fingerprint: str


@dataclass(frozen=True, slots=True)
class EvidenceAdmissionRequest:
    admission_request_id: str
    candidate_ref: EvidenceCandidateRef
    requirement_ref: EvidenceRequirementRef
    requirement_fingerprint: str
    requirement_set_id: str
    requirement_set_version: str
    requirement_root_hash: str
    task_contract_id: str
    task_contract_version: str
    work_run_id: str
    checkpoint_ref: EvidenceCheckpointRef
    checkpoint_fingerprint: str
    observed_state: WorkflowState
    observed_state_version: int
    target_state: WorkflowState | None
    transition_purpose_id: str | None
    transition_purpose_version: str | None
    requester_identity: str
    created_at: datetime
    request_fingerprint: str


@dataclass(frozen=True, slots=True)
class EvidenceDimensionResult:
    dimension: EvidenceAdmissionDimension
    outcome: EvidenceDimensionOutcome
    authority_ref: str
    authority_version: str
    reason: str


@dataclass(frozen=True, slots=True)
class EvidenceEvaluation:
    evaluation_id: str
    admission_request_id: str
    dimension_results: tuple[EvidenceDimensionResult, ...]
    evaluated_at: datetime
    authority_version: str


@dataclass(frozen=True, slots=True)
class EvidenceAdmissionDecision:
    decision_id: str
    admission_request_id: str
    evaluation_id: str
    candidate_id: str
    requirement_ref: str
    requirement_set_ref: str
    outcome: EvidenceAdmissionOutcome
    reason: EvidenceRejectionReason
    secondary_reasons: tuple[EvidenceRejectionReason, ...]
    admitting_authority_version: str
    decided_at: datetime


@dataclass(frozen=True, slots=True)
class AdmittedEvidence:
    admitted_evidence_id: str
    decision_id: str
    candidate_ref: EvidenceCandidateRef
    requirement_ref: EvidenceRequirementRef
    task_contract_id: str
    task_contract_version: str
    work_run_id: str
    checkpoint_ref: EvidenceCheckpointRef
    content_ref: EvidenceContentRef
    coverage: tuple[str, ...]
    admitted_at: datetime


@dataclass(frozen=True, slots=True)
class AdmittedEvidenceRef:
    admitted_evidence_id: str
    authority_version: str

    def serialized(self) -> str:
        return f"p1-6-admitted:{self.authority_version}:{self.admitted_evidence_id}"


@dataclass(frozen=True, slots=True)
class EvidenceRequirementSatisfaction:
    requirement_ref: str
    outcome: RequirementSatisfaction
    admitted_evidence_refs: tuple[str, ...]
    coverage: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class EvidenceSetEvaluation:
    evaluation_id: str
    evaluation_version: str
    task_contract_id: str
    task_contract_version: str
    work_run_id: str
    source_state: WorkflowState
    state_version: int
    checkpoint_ref: EvidenceCheckpointRef
    requirement_set_id: str
    requirement_set_version: str
    full_requirement_root_hash: str
    ordered_applicable_requirement_refs: tuple[str, ...]
    checkpoint_subset_root_hash: str
    requirement_results: tuple[EvidenceRequirementSatisfaction, ...]
    admitted_ref_root_hash: str
    evidence_authority_revision: int
    outcome: EvidenceSetOutcome
    evaluated_at: datetime


@dataclass(frozen=True, slots=True)
class EvidenceSetSatisfactionAttestation:
    attestation_id: str
    attestation_version: str
    evidence_set_evaluation_id: str
    evaluation_version: str
    task_contract_id: str
    task_contract_version: str
    work_run_id: str
    source_state: WorkflowState
    state_version: int
    checkpoint_ref: EvidenceCheckpointRef
    checkpoint_fingerprint: str
    target_state: WorkflowState | None
    transition_purpose_id: str | None
    transition_purpose_version: str | None
    requirement_set_id: str
    requirement_set_version: str
    full_requirement_root_hash: str
    ordered_applicable_requirement_refs: tuple[str, ...]
    checkpoint_subset_root_hash: str
    ordered_admitted_evidence_refs: tuple[str, ...]
    admitted_ref_root_hash: str
    satisfied: bool
    evidence_authority_version: str
    evidence_authority_revision: int
    issued_at: datetime
    expires_at: datetime | None
    issuer_id: str
    issuer_version: str

    @property
    def serialized_ref(self) -> str:
        return f"p1-6-attestation:{self.attestation_version}:{self.attestation_id}"


@dataclass(frozen=True, slots=True)
class EvidenceReuseConsumption:
    consumption_id: str
    prior_admitted_evidence_ref: str
    admitted_evidence_id: str
    requirement_ref: str
    work_run_id: str
    checkpoint_ref: str
    policy_maximum: int
    consumption_ordinal: int
    consumed_at: datetime


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _require_aware(value: datetime) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("authority timestamp must be timezone-aware")


def utc_now() -> datetime:
    return datetime.now(UTC)
