from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import StrEnum

from aiscc.contracts.workflow import WorkflowState
from aiscc.evidence.models import EvidenceSensitivity, canonical_hash
from aiscc.workflow.models import GuardId

HUMAN_GATE_PURPOSE_ID = "P1_7_WORK_RESULT_REVIEW"
HUMAN_GATE_PURPOSE_VERSION = "v1"
HUMAN_GUARD_ATTESTATION_VERSION = "p1-7-human-guard-v1"
HUMAN_GUARD_AUTHORITY_ID = "AISCC_P1_7_HUMAN_GUARD_AUTHORITY_V1"
HUMAN_AUTHORITY_VERSION = "AISCC-P1-7-HUMAN-AUTHORITY-V1"


class HumanGateStatus(StrEnum):
    NOT_REQUIRED = "NOT_REQUIRED"
    PENDING = "PENDING"
    RESOLVED = "RESOLVED"
    CANCELLED = "CANCELLED"


class HumanGateSuspensionStatus(StrEnum):
    NOT_APPLICABLE = "NOT_APPLICABLE"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"


class HumanResultKind(StrEnum):
    APPROVE = "APPROVE"
    REWORK = "REWORK"
    REJECT = "REJECT"


class HumanAuthorityReason(StrEnum):
    UNKNOWN_HUMAN_GATE = "UNKNOWN_HUMAN_GATE"
    HUMAN_GATE_NOT_CURRENT = "HUMAN_GATE_NOT_CURRENT"
    HUMAN_GATE_CLOSED = "HUMAN_GATE_CLOSED"
    HUMAN_GATE_EXPIRED = "HUMAN_GATE_EXPIRED"
    HUMAN_PRINCIPAL_NOT_AUTHORIZED = "HUMAN_PRINCIPAL_NOT_AUTHORIZED"
    HUMAN_AUTHORITY_MISMATCH = "HUMAN_AUTHORITY_MISMATCH"
    TASK_CONTRACT_MISMATCH = "TASK_CONTRACT_MISMATCH"
    WORK_RUN_MISMATCH = "WORK_RUN_MISMATCH"
    WORKFLOW_STATE_MISMATCH = "WORKFLOW_STATE_MISMATCH"
    STATE_VERSION_MISMATCH = "STATE_VERSION_MISMATCH"
    TRANSITION_PURPOSE_MISMATCH = "TRANSITION_PURPOSE_MISMATCH"
    HUMAN_RESULT_IDENTITY_CONFLICT = "HUMAN_RESULT_IDENTITY_CONFLICT"
    HUMAN_RESULT_STALE = "HUMAN_RESULT_STALE"
    PRE_HUMAN_EVIDENCE_AUTHORITY_MISSING = "PRE_HUMAN_EVIDENCE_AUTHORITY_MISSING"
    PRE_HUMAN_EVIDENCE_AUTHORITY_MISMATCH = "PRE_HUMAN_EVIDENCE_AUTHORITY_MISMATCH"
    PRE_HUMAN_EVIDENCE_AUTHORITY_STALE = "PRE_HUMAN_EVIDENCE_AUTHORITY_STALE"
    GUARD_AUTHORITY_MISMATCH = "GUARD_AUTHORITY_MISMATCH"
    GUARD_REPLAY_REJECTED = "GUARD_REPLAY_REJECTED"
    AUTHORITY_CONFLICT = "AUTHORITY_CONFLICT"
    PROVENANCE_INCOMPLETE = "PROVENANCE_INCOMPLETE"


class HumanAuthorityError(RuntimeError):
    def __init__(self, reason: HumanAuthorityReason) -> None:
        super().__init__(reason.value)
        self.reason = reason


class HumanResultIdentityConflictError(HumanAuthorityError):
    pass


@dataclass(frozen=True, slots=True)
class AuthenticatedHumanPrincipal:
    principal_id: str
    principal_authority_id: str
    principal_authority_version: str
    authentication_session_id: str
    authenticated_at: datetime
    authentication_expires_at: datetime
    authentication_policy_ref: str
    internal_role_refs: tuple[str, ...]
    _issuer_token: object = field(repr=False, compare=False)


@dataclass(frozen=True, slots=True)
class HumanGateReservation:
    human_gate_id: str
    human_gate_version: str
    gate_fingerprint: str
    purpose_id: str
    purpose_version: str
    task_contract_id: str
    task_contract_version: str
    work_run_id: str
    opened_from_state: WorkflowState
    opened_from_state_version: int
    target_state: WorkflowState
    authority_policy_ref: str
    authority_policy_version: str
    designated_principal_selector_fingerprint: str
    expires_at: datetime | None
    _issuer_token: object = field(repr=False, compare=False)


@dataclass(frozen=True, slots=True)
class HumanGate:
    human_gate_id: str
    human_gate_version: str
    gate_fingerprint: str
    purpose_id: str
    purpose_version: str
    task_contract_id: str
    task_contract_version: str
    work_run_id: str
    opened_from_state: WorkflowState
    opened_from_state_version: int
    bound_state: WorkflowState
    bound_state_version: int
    opening_transition_request_id: str
    opening_transition_decision_id: str
    authority_policy_ref: str
    authority_policy_version: str
    designated_principal_selector_fingerprint: str
    gate_authority_id: str
    gate_authority_version: str
    gate_authority_revision: int
    status: HumanGateStatus
    suspension_status: HumanGateSuspensionStatus
    opened_at: datetime
    expires_at: datetime | None
    supersedes_gate_ref: str | None = None

    @property
    def serialized_ref(self) -> str:
        return f"p1-7-gate:{self.human_gate_version}:{self.human_gate_id}"


@dataclass(frozen=True, slots=True)
class HumanActionAuthority:
    action_authority_id: str
    action_authority_version: str
    principal_id: str
    authentication_session_id: str
    human_gate_ref: str
    gate_authority_revision: int
    task_contract_id: str
    task_contract_version: str
    work_run_id: str
    state_version: int
    allowed_result_kinds: frozenset[HumanResultKind]
    issued_at: datetime
    expires_at: datetime
    idempotency_scope: str
    _issuer_token: object = field(repr=False, compare=False)


@dataclass(frozen=True, slots=True)
class HumanResult:
    human_result_id: str
    human_result_version: str
    human_result_fingerprint: str
    human_gate_ref: str
    gate_authority_revision: int
    purpose_id: str
    purpose_version: str
    principal_id: str
    principal_authority_ref: str
    human_action_authority_ref: str
    task_contract_id: str
    task_contract_version: str
    work_run_id: str
    source_state: WorkflowState
    state_version: int
    result_kind: HumanResultKind
    structured_reason_code: str
    reason_vocabulary_version: str
    private_comment_ref: str | None
    private_comment_hash: str | None
    sensitivity: EvidenceSensitivity
    submitted_at: datetime
    admitted_at: datetime
    idempotency_key: str
    result_authority_id: str
    result_authority_version: str
    result_authority_revision: int
    supersedes_human_result_ref: str | None = None

    @property
    def serialized_ref(self) -> str:
        return f"p1-7-result:{self.human_result_version}:{self.human_result_id}"


@dataclass(frozen=True, slots=True)
class HumanRequiredEvidenceBinding:
    attestation_ref: str
    attestation_version: str
    checkpoint_ref: str
    checkpoint_fingerprint: str
    task_contract_id: str
    task_contract_version: str
    work_run_id: str
    source_state: WorkflowState
    state_version: int
    target_state: WorkflowState | None
    transition_purpose_id: str | None
    transition_purpose_version: str | None
    requirement_set_id: str
    requirement_set_version: str
    requirement_set_root: str
    ordered_applicable_requirement_refs: tuple[str, ...]
    applicable_subset_root: str
    ordered_admitted_evidence_refs: tuple[str, ...]
    admitted_ref_root: str
    evidence_authority_version: str
    evidence_authority_revision: int
    issued_at: datetime
    expires_at: datetime | None
    p1_6_authority_id: str
    p1_6_authority_version: str


@dataclass(frozen=True, slots=True)
class HumanGuardAttestation:
    attestation_id: str
    attestation_version: str
    fingerprint: str
    guard_id: GuardId
    task_contract_id: str
    task_contract_version: str
    work_run_id: str
    source_state: WorkflowState
    state_version: int
    target_state: WorkflowState
    target_use_fingerprint: str
    human_gate_ref: str
    gate_authority_revision: int
    purpose_id: str
    purpose_version: str
    human_result_ref: str | None
    result_authority_revision: int | None
    authority_id: str
    authority_version: str
    authority_revision: int
    issued_at: datetime
    expires_at: datetime | None
    pre_human_evidence: HumanRequiredEvidenceBinding | None = None

    @property
    def serialized_ref(self) -> str:
        return f"p1-7-human-guard:{self.attestation_version}:{self.attestation_id}"


def human_guard_attestation_payload(value: HumanGuardAttestation) -> dict[str, object]:
    payload = asdict(value)
    payload["guard_id"] = value.guard_id.value
    payload["source_state"] = value.source_state.value
    payload["target_state"] = value.target_state.value
    payload["issued_at"] = value.issued_at.isoformat()
    payload["expires_at"] = value.expires_at.isoformat() if value.expires_at else None
    if value.pre_human_evidence is not None:
        binding = value.pre_human_evidence
        payload_binding = payload["pre_human_evidence"]
        assert isinstance(payload_binding, dict)
        payload_binding["source_state"] = binding.source_state.value
        payload_binding["target_state"] = (
            binding.target_state.value if binding.target_state else None
        )
        payload_binding["ordered_applicable_requirement_refs"] = list(
            binding.ordered_applicable_requirement_refs
        )
        payload_binding["ordered_admitted_evidence_refs"] = list(
            binding.ordered_admitted_evidence_refs
        )
        payload_binding["issued_at"] = binding.issued_at.isoformat()
        payload_binding["expires_at"] = (
            binding.expires_at.isoformat() if binding.expires_at else None
        )
    return payload


def human_guard_attestation_fingerprint(value: HumanGuardAttestation) -> str:
    payload = human_guard_attestation_payload(value)
    payload.pop("fingerprint")
    return canonical_hash(payload)


@dataclass(frozen=True, slots=True)
class HumanP1_7EvidenceProducerRef:
    producer_ref_id: str
    producer_ref_version: str
    fingerprint: str
    task_contract_id: str
    task_contract_version: str
    work_run_id: str
    source_state: WorkflowState
    state_version: int
    human_gate_ref: str
    gate_authority_revision: int
    human_result_ref: str
    result_authority_revision: int
    principal_subject_ref: str
    checkpoint_ref: str
    evidence_type_id: str
    evidence_type_version: str
    subject_id: str
    scope_id: str
    resource_id: str | None
    content_hash: str
    sensitivity: EvidenceSensitivity
    export_policy: str
    authority_id: str
    authority_version: str
    issued_at: datetime
    expires_at: datetime | None

    @property
    def serialized_ref(self) -> str:
        return (
            f"p1-7-producer:{self.producer_ref_version}:{self.producer_ref_id}:{self.fingerprint}"
        )
