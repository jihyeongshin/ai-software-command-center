from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.evidence.models import (
    EvidenceAdmissionOutcome,
    EvidenceRequirementProfile,
    EvidenceSemanticOwner,
    EvidenceSetOutcome,
    RequirementObligation,
)
from aiscc.human.models import (
    HumanGateStatus,
    HumanGateSuspensionStatus,
    HumanResultKind,
)
from aiscc.judgment.models import JudgmentKind, JudgmentOwnerPolicy
from aiscc.providers.models import (
    ExecutionOperationOutcome,
    ExecutionOperationPhase,
    ExecutionStatus,
    OperationKind,
)
from aiscc.workflow.models import DecisionOutcome, DecisionReason, RequesterType

SCHEMA_VERSION = "p2-1-command-center-read-v1"


class ReadModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Presence(StrEnum):
    NONE = "NONE"
    PRESENT = "PRESENT"


class Availability(StrEnum):
    REFERENCE_ONLY = "REFERENCE_ONLY"
    UNAVAILABLE = "UNAVAILABLE"
    AVAILABLE = "AVAILABLE"


class ReadConsistency(StrEnum):
    VERIFIED = "VERIFIED"


class DerivedStateEffect(StrEnum):
    CHANGED = "CHANGED"
    UNCHANGED = "UNCHANGED"


class ErrorCode(StrEnum):
    INVALID_QUERY = "INVALID_QUERY"
    NOT_FOUND = "NOT_FOUND"
    AUTHORITY_CONFLICT = "AUTHORITY_CONFLICT"
    NO_LONGER_CURRENT = "NO_LONGER_CURRENT"
    PROJECTION_UNAVAILABLE = "PROJECTION_UNAVAILABLE"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class ReadMeta(ReadModel):
    schema_version: str = SCHEMA_VERSION
    snapshot_at: datetime
    source_revisions: dict[str, int | str]
    consistency: ReadConsistency = ReadConsistency.VERIFIED
    next_cursor: str | None = None
    poll_after_ms: int | None = 10_000


class SuccessEnvelope[DataT: ReadModel](ReadModel):
    data: DataT
    meta: ReadMeta


class ErrorDetail(ReadModel):
    code: ErrorCode
    message: str
    retryable: bool
    correlation_id: str


class ErrorEnvelope(ReadModel):
    error: ErrorDetail


class TaskContractView(ReadModel):
    id: str
    version: str


class TaskDisplayView(ReadModel):
    availability: Availability = Availability.REFERENCE_ONLY
    message: str = "Metadata unavailable"
    title: str | None = None
    type: str | None = None
    source_ref: str | None = None


class ScopeView(ReadModel):
    availability: Availability = Availability.REFERENCE_ONLY
    message: str = "Metadata unavailable"
    allowed: tuple[str, ...] | None = None
    forbidden: tuple[str, ...] | None = None


class WorkflowView(ReadModel):
    state: WorkflowState
    state_version: int = Field(ge=1)
    created_at: datetime | None = None
    updated_at: datetime


class ExecutionSummaryView(ReadModel):
    attempt_present: bool
    execution_attempt_id: str | None = None
    attempt_ordinal: int | None = None
    status: ExecutionStatus | None = None
    execution_version: int | None = None


class HumanGateSummaryView(ReadModel):
    presence: Presence
    human_gate_id: str | None = None
    status: HumanGateStatus | None = None
    suspension_status: HumanGateSuspensionStatus | None = None
    authority_revision: int | None = None


class HumanResultSummaryView(ReadModel):
    presence: Presence
    result_kind: HumanResultKind | None = None
    authority_revision: int | None = None


class JudgmentSummaryView(ReadModel):
    presence: Presence
    judgment_id: str | None = None
    kind: JudgmentKind | None = None
    owner_policy: JudgmentOwnerPolicy | None = None
    authority_revision: int | None = None


class TransitionDecisionSummaryView(ReadModel):
    presence: Presence
    decision_id: str | None = None
    outcome: DecisionOutcome | None = None
    reason: DecisionReason | None = None
    resulting_state: WorkflowState | None = None
    resulting_state_version: int | None = None


class NextActionSummaryView(ReadModel):
    presence: Presence
    selection_id: str | None = None
    action_ref: str | None = None
    project_revision: int | None = None
    selected_at: datetime | None = None


class QueueRow(ReadModel):
    project_id: str
    work_run_id: str
    task_contract: TaskContractView
    task_display: TaskDisplayView
    workflow: WorkflowView
    execution: ExecutionSummaryView
    human_gate: HumanGateSummaryView
    human_result: HumanResultSummaryView
    judgment: JudgmentSummaryView
    latest_transition_decision: TransitionDecisionSummaryView
    next_action: NextActionSummaryView
    runtime_mode: RuntimeMode


class QueueData(ReadModel):
    project_id: str
    items: tuple[QueueRow, ...]


class TaskConstraintView(ReadModel):
    presence: Presence
    constraint_ref: str | None = None
    constraint_fingerprint: str | None = None
    snapshot_ref: str | None = None
    snapshot_fingerprint: str | None = None
    owner_event_high_watermark: int | None = None


class BlockerView(ReadModel):
    presence: Presence
    blocker_ref: str | None = None
    blocker_kind: str | None = None
    reason_code: str | None = None
    resumability: str | None = None
    blocked_epoch: int | None = None
    authority_revision: int | None = None
    updated_at: datetime | None = None


class WorkRunData(ReadModel):
    project_id: str
    work_run_id: str
    task_contract: TaskContractView
    runtime_mode: RuntimeMode
    workflow: WorkflowView
    task_constraint: TaskConstraintView
    task_display: TaskDisplayView
    scope: ScopeView
    blocker: BlockerView


class TransitionRequestView(ReadModel):
    transition_request_id: str
    observed_state: WorkflowState | None
    observed_state_version: int
    target_state: WorkflowState
    requester_type: RequesterType
    runtime_mode: RuntimeMode
    evidence_refs: tuple[str, ...]
    human_result_refs: tuple[str, ...]
    judgment_refs: tuple[str, ...]
    parent_request_id: str | None
    created_at: datetime


class GuardView(ReadModel):
    guard_id: str
    outcome: str
    reason: str | None = None


class TransitionEvaluationView(ReadModel):
    transition_evaluation_id: str
    authoritative_state: WorkflowState | None
    authoritative_state_version: int
    guards: tuple[GuardView, ...]
    missing_guards: tuple[str, ...]
    evaluated_at: datetime


class TransitionDecisionView(ReadModel):
    transition_decision_id: str
    outcome: DecisionOutcome
    reason: DecisionReason
    resulting_state: WorkflowState | None
    resulting_state_version: int
    decided_at: datetime
    derived_state_effect: DerivedStateEffect


class TransitionRecord(ReadModel):
    request: TransitionRequestView
    evaluation: TransitionEvaluationView
    decision: TransitionDecisionView


class TransitionsData(ReadModel):
    work_run_id: str
    items: tuple[TransitionRecord, ...]


class DurableCountersView(ReadModel):
    schema_version: str | None = None
    provider_calls: int = 0
    agent_rounds: int = 0
    tool_calls: int = 0
    provider_retries: int = 0
    output_bytes: int = 0
    output_tokens: int = 0
    budget_units: int = 0
    started_at: datetime | None = None
    deadline_at: datetime | None = None


class SubmissionView(ReadModel):
    presence: Presence
    submission_ref: str | None = None
    content_hash: str | None = None


class ExecutionOperationView(ReadModel):
    operation_id: str
    kind: OperationKind
    fingerprint: str
    phase: ExecutionOperationPhase
    outcome: ExecutionOperationOutcome | None
    call_ordinal: int
    resource: str = "REDACTED_RESOURCE_IDENTITY"
    parent_operation_id: str | None
    created_at: datetime
    updated_at: datetime


class ExecutionAttemptView(ReadModel):
    execution_attempt_id: str
    attempt_ordinal: int
    parent_attempt_id: str | None
    task_contract: TaskContractView
    runtime_mode: RuntimeMode
    provider_profile_id: str
    provider_profile_version: str
    tool_registry_id: str
    tool_registry_version: str
    creation_state: WorkflowState
    creation_state_version: int
    causal_state: WorkflowState
    causal_state_version: int
    status: ExecutionStatus
    execution_version: int
    counters: DurableCountersView
    submission: SubmissionView
    operations: tuple[ExecutionOperationView, ...]
    created_at: datetime
    updated_at: datetime


class ExecutionData(ReadModel):
    work_run_id: str
    attempts: tuple[ExecutionAttemptView, ...]


class EvidenceRequirementView(ReadModel):
    requirement_ref: str
    profile: EvidenceRequirementProfile
    obligation: RequirementObligation
    semantic_owner: EvidenceSemanticOwner
    evidence_type_id: str
    evidence_type_version: str
    freshness_kind: str
    applicable_checkpoint_refs: tuple[str, ...]
    fingerprint: str


class EvidenceCheckpointView(ReadModel):
    checkpoint_ref: str
    source_state: WorkflowState
    target_state: WorkflowState | None
    transition_purpose_id: str | None
    transition_purpose_version: str | None
    requirement_set_ref: str
    fingerprint: str


class EvidenceRequirementSetView(ReadModel):
    requirement_set_ref: str
    ordered_requirement_refs: tuple[str, ...]
    ordered_checkpoint_refs: tuple[str, ...]
    semantic_owner: EvidenceSemanticOwner
    requirement_root_hash: str
    fingerprint: str


class EvidenceContentMetadataView(ReadModel):
    content_ref: str
    content_kind: str
    schema_id: str
    schema_version: str
    byte_count: int
    content_hash: str
    sensitivity: str


class EvidenceCandidateView(ReadModel):
    candidate_id: str
    candidate_version: str
    candidate_fingerprint: str
    checkpoint_ref: str
    issuer_type: str
    sensitivity: str
    content_hash: str
    created_at: datetime
    durable_content: EvidenceContentMetadataView | None = None


class EvidenceAdmissionDecisionView(ReadModel):
    decision_id: str
    candidate_id: str
    requirement_ref: str
    checkpoint_ref: str
    outcome: EvidenceAdmissionOutcome
    reason: str
    decided_at: datetime


class AdmittedEvidenceView(ReadModel):
    admitted_evidence_id: str
    decision_id: str
    candidate_id: str
    requirement_ref: str
    checkpoint_ref: str
    content_hash: str
    coverage: tuple[str, ...]
    admitted_at: datetime


class RequirementSatisfactionView(ReadModel):
    satisfaction_id: str
    admitted_evidence_id: str
    requirement_ref: str
    checkpoint_ref: str
    coverage: tuple[str, ...]
    created_at: datetime


class EvidenceSetEvaluationView(ReadModel):
    evaluation_id: str
    checkpoint_ref: str
    requirement_set_ref: str
    outcome: EvidenceSetOutcome
    evidence_authority_revision: int
    evaluated_at: datetime


class EvidenceSetAttestationView(ReadModel):
    attestation_id: str
    serialized_ref: str
    checkpoint_ref: str
    state_version: int
    evidence_authority_revision: int
    issued_at: datetime
    expires_at: datetime | None


class EvidenceData(ReadModel):
    work_run_id: str
    requirement_sets: tuple[EvidenceRequirementSetView, ...]
    checkpoints: tuple[EvidenceCheckpointView, ...]
    requirements: tuple[EvidenceRequirementView, ...]
    candidates: tuple[EvidenceCandidateView, ...]
    admission_decisions: tuple[EvidenceAdmissionDecisionView, ...]
    admitted_evidence: tuple[AdmittedEvidenceView, ...]
    satisfactions: tuple[RequirementSatisfactionView, ...]
    set_evaluations: tuple[EvidenceSetEvaluationView, ...]
    set_attestations: tuple[EvidenceSetAttestationView, ...]


class HumanGateView(ReadModel):
    presence: Presence
    human_gate_id: str | None = None
    gate_ref: str | None = None
    purpose_id: str | None = None
    purpose_version: str | None = None
    status: HumanGateStatus | None = None
    suspension_status: HumanGateSuspensionStatus | None = None
    bound_state: WorkflowState | None = None
    bound_state_version: int | None = None
    authority_revision: int | None = None
    opened_at: datetime | None = None
    updated_at: datetime | None = None


class HumanResultView(ReadModel):
    presence: Presence
    human_result_id: str | None = None
    human_result_ref: str | None = None
    result_kind: HumanResultKind | None = None
    structured_reason_code: str | None = None
    authority_revision: int | None = None
    admitted_at: datetime | None = None


class JudgmentView(ReadModel):
    presence: Presence
    judgment_id: str | None = None
    judgment_ref: str | None = None
    kind: JudgmentKind | None = None
    owner_policy: JudgmentOwnerPolicy | None = None
    reason_code: str | None = None
    state_version: int | None = None
    authority_revision: int | None = None
    issued_at: datetime | None = None


class TransitionEffectView(ReadModel):
    presence: Presence
    transition_decision_id: str | None = None
    outcome: DecisionOutcome | None = None
    resulting_state: WorkflowState | None = None
    resulting_state_version: int | None = None
    derived_state_effect: DerivedStateEffect | None = None


class HumanJudgmentData(ReadModel):
    work_run_id: str
    human_gate: HumanGateView
    human_result: HumanResultView
    judgment: JudgmentView
    transition_effect: TransitionEffectView


class AdmittedCycleSummaryView(ReadModel):
    presence: Presence
    cycle_id: str | None = None
    cycle_ref: str | None = None
    admission_sequence: int | None = None
    admitted_at: datetime | None = None


class OutcomeRow(ReadModel):
    project_id: str
    work_run_id: str
    task_contract: TaskContractView
    workflow: WorkflowView
    judgment: JudgmentSummaryView
    admitted_cycle: AdmittedCycleSummaryView


class OutcomesData(ReadModel):
    project_id: str
    items: tuple[OutcomeRow, ...]


class MemorySafeSummaryView(ReadModel):
    entry_id: str
    category: str
    privacy: str
    content_fingerprint: str
    applicability: str
    authority_revision: int
    created_at: datetime


class CycleData(ReadModel):
    cycle_id: str
    cycle_version: str
    cycle_ref: str
    cycle_fingerprint: str
    project_id: str
    work_run_id: str
    task_contract: TaskContractView
    terminal_state_version: int
    transition_decision_id: str
    judgment_ref: str
    evidence_attestation_ref: str
    evidence_root: str
    admission_sequence: int
    admitted_at: datetime
    task_constraint: TaskConstraintView
    current_memory: tuple[MemorySafeSummaryView, ...]


class NextActionProjectionView(ReadModel):
    presence: Presence
    state: str | None = None
    reason: str | None = None
    project_revision: int | None = None
    latest_event_sequence: int | None = None
    updated_at: datetime | None = None


class NextActionSelectionView(ReadModel):
    presence: Presence
    selection_id: str | None = None
    selection_ref: str | None = None
    action_ref: str | None = None
    project_revision: int | None = None
    selected_at: datetime | None = None


class TaskIssuanceCandidateView(ReadModel):
    presence: Presence
    candidate_id: str | None = None
    issuance_owner: str | None = None
    required_post_issuance_human_input: str | None = None
    created_at: datetime | None = None


class NextActionData(ReadModel):
    project_id: str
    projection: NextActionProjectionView
    selection: NextActionSelectionView
    task_issuance_candidate: TaskIssuanceCandidateView
