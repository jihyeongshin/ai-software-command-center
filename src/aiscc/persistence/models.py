from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Identity,
    Index,
    Integer,
    LargeBinary,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class WorkRunRow(Base):
    __tablename__ = "work_runs"
    __table_args__ = (
        CheckConstraint("state_version >= 1", name="ck_work_runs_version"),
        CheckConstraint(
            "workflow_state IN ('READY','RUNNING','ADMISSION_PENDING','HUMAN_REQUIRED',"
            "'BLOCKED','REWORK_REQUIRED','ACCEPTED','REJECTED','FAILED')",
            name="ck_work_runs_exact_state",
        ),
        CheckConstraint(
            "runtime_mode IN ('OWNER_SELF_DOGFOOD','PUBLIC_RECORDED_REPLAY','PUBLIC_BOUNDED_LIVE')",
            name="ck_work_runs_exact_runtime_mode",
        ),
    )

    work_run_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    project_id: Mapped[str] = mapped_column(String(128), nullable=False)
    task_contract_id: Mapped[str] = mapped_column(String(160), nullable=False)
    task_contract_version: Mapped[str] = mapped_column(String(80), nullable=False)
    workflow_state: Mapped[str] = mapped_column(String(40), nullable=False)
    state_version: Mapped[int] = mapped_column(Integer, nullable=False)
    runtime_mode: Mapped[str] = mapped_column(String(48), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class TransitionRequestRow(Base):
    __tablename__ = "transition_requests"
    __table_args__ = (
        CheckConstraint(
            "observed_state IS NULL OR observed_state IN "
            "('READY','RUNNING','ADMISSION_PENDING','HUMAN_REQUIRED','BLOCKED',"
            "'REWORK_REQUIRED','ACCEPTED','REJECTED','FAILED')",
            name="ck_transition_requests_exact_observed_state",
        ),
        CheckConstraint(
            "target_state IN ('READY','RUNNING','ADMISSION_PENDING','HUMAN_REQUIRED',"
            "'BLOCKED','REWORK_REQUIRED','ACCEPTED','REJECTED','FAILED')",
            name="ck_transition_requests_exact_target_state",
        ),
        CheckConstraint(
            "runtime_mode IN ('OWNER_SELF_DOGFOOD','PUBLIC_RECORDED_REPLAY','PUBLIC_BOUNDED_LIVE')",
            name="ck_transition_requests_exact_runtime_mode",
        ),
    )

    transition_request_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    request_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    project_id: Mapped[str] = mapped_column(String(128), nullable=False)
    task_contract_id: Mapped[str] = mapped_column(String(160), nullable=False)
    task_contract_version: Mapped[str] = mapped_column(String(80), nullable=False)
    work_run_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    observed_state: Mapped[str | None] = mapped_column(String(40), nullable=True)
    observed_state_version: Mapped[int] = mapped_column(Integer, nullable=False)
    target_state: Mapped[str] = mapped_column(String(40), nullable=False)
    requester_identity: Mapped[str] = mapped_column(String(160), nullable=False)
    requester_type: Mapped[str] = mapped_column(String(48), nullable=False)
    runtime_mode: Mapped[str] = mapped_column(String(48), nullable=False)
    evidence_refs: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    human_result_refs: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    judgment_refs: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    parent_request_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class TransitionEvaluationRow(Base):
    __tablename__ = "transition_evaluations"

    transition_evaluation_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    transition_request_id: Mapped[str] = mapped_column(
        ForeignKey("transition_requests.transition_request_id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    authoritative_state: Mapped[str | None] = mapped_column(String(40), nullable=True)
    authoritative_state_version: Mapped[int] = mapped_column(Integer, nullable=False)
    guards: Mapped[list[dict[str, object]]] = mapped_column(JSONB, nullable=False)
    missing_guards: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class TransitionDecisionRow(Base):
    __tablename__ = "transition_decisions"
    __table_args__ = (
        UniqueConstraint("event_sequence", name="uq_transition_decisions_event_sequence"),
        CheckConstraint(
            "resulting_state IS NULL OR resulting_state IN "
            "('READY','RUNNING','ADMISSION_PENDING','HUMAN_REQUIRED','BLOCKED',"
            "'REWORK_REQUIRED','ACCEPTED','REJECTED','FAILED')",
            name="ck_transition_decisions_exact_resulting_state",
        ),
    )

    transition_decision_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    event_sequence: Mapped[int] = mapped_column(BigInteger, Identity(start=1), nullable=False)
    transition_evaluation_id: Mapped[str] = mapped_column(
        ForeignKey("transition_evaluations.transition_evaluation_id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    transition_request_id: Mapped[str] = mapped_column(
        ForeignKey("transition_requests.transition_request_id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    outcome: Mapped[str] = mapped_column(String(24), nullable=False)
    reason: Mapped[str] = mapped_column(String(48), nullable=False)
    resulting_state: Mapped[str | None] = mapped_column(String(40), nullable=True)
    resulting_state_version: Mapped[int] = mapped_column(Integer, nullable=False)
    admitting_owner: Mapped[str] = mapped_column(String(80), nullable=False)
    kernel_version: Mapped[str] = mapped_column(String(80), nullable=False)
    decided_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ExecutionAttemptRow(Base):
    __tablename__ = "execution_attempts"
    __table_args__ = (
        UniqueConstraint("work_run_id", "attempt_ordinal", name="uq_execution_attempt_ordinal"),
        CheckConstraint(
            "status IN ('NOT_STARTED','RUNNING','EXECUTOR_COMPLETED','EXECUTION_FAILED')",
            name="ck_execution_attempt_exact_status",
        ),
        CheckConstraint("execution_version >= 1", name="ck_execution_attempt_version"),
    )

    execution_attempt_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    work_run_id: Mapped[str] = mapped_column(
        ForeignKey("work_runs.work_run_id", ondelete="RESTRICT"), nullable=False, index=True
    )
    attempt_ordinal: Mapped[int] = mapped_column(Integer, nullable=False)
    parent_attempt_id: Mapped[str | None] = mapped_column(
        ForeignKey("execution_attempts.execution_attempt_id", ondelete="RESTRICT"), nullable=True
    )
    task_contract_id: Mapped[str] = mapped_column(String(160), nullable=False)
    task_contract_version: Mapped[str] = mapped_column(String(80), nullable=False)
    runtime_mode: Mapped[str] = mapped_column(String(48), nullable=False)
    provider_profile_id: Mapped[str] = mapped_column(String(128), nullable=False)
    provider_profile_version: Mapped[str] = mapped_column(String(80), nullable=False)
    tool_registry_id: Mapped[str] = mapped_column(String(128), nullable=False)
    tool_registry_version: Mapped[str] = mapped_column(String(80), nullable=False)
    creation_state: Mapped[str] = mapped_column(String(40), nullable=False)
    creation_state_version: Mapped[int] = mapped_column(Integer, nullable=False)
    causal_state: Mapped[str] = mapped_column(String(40), nullable=False)
    causal_state_version: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False)
    execution_version: Mapped[int] = mapped_column(Integer, nullable=False)
    latest_event_sequence: Mapped[int] = mapped_column(BigInteger, nullable=False)
    counters: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ExecutionEventRow(Base):
    __tablename__ = "execution_events"
    __table_args__ = (
        UniqueConstraint(
            "execution_attempt_id", "event_identity", name="uq_execution_event_identity"
        ),
    )

    event_sequence: Mapped[int] = mapped_column(BigInteger, Identity(start=1), primary_key=True)
    event_id: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    event_identity: Mapped[str] = mapped_column(String(64), nullable=False)
    execution_attempt_id: Mapped[str] = mapped_column(
        ForeignKey("execution_attempts.execution_attempt_id", ondelete="RESTRICT"), nullable=False
    )
    event_kind: Mapped[str] = mapped_column(String(64), nullable=False)
    status_before: Mapped[str | None] = mapped_column(String(40), nullable=True)
    status_after: Mapped[str] = mapped_column(String(40), nullable=False)
    execution_version_after: Mapped[int] = mapped_column(Integer, nullable=False)
    causal_state: Mapped[str] = mapped_column(String(40), nullable=False)
    causal_state_version: Mapped[int] = mapped_column(Integer, nullable=False)
    payload_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    refs: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ExecutionOperationRow(Base):
    __tablename__ = "execution_operations"
    __table_args__ = (
        UniqueConstraint(
            "execution_attempt_id", "call_ordinal", name="uq_execution_operation_call_ordinal"
        ),
        CheckConstraint("call_ordinal >= 1", name="ck_execution_operation_call_ordinal"),
    )

    operation_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    execution_attempt_id: Mapped[str] = mapped_column(
        ForeignKey("execution_attempts.execution_attempt_id", ondelete="RESTRICT"), nullable=False
    )
    operation_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    operation_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    current_phase: Mapped[str] = mapped_column(String(40), nullable=False)
    outcome: Mapped[str | None] = mapped_column(String(64), nullable=True)
    resource_identity: Mapped[str] = mapped_column(String(512), nullable=False)
    call_ordinal: Mapped[int] = mapped_column(Integer, nullable=False)
    parent_operation_id: Mapped[str | None] = mapped_column(
        ForeignKey("execution_operations.operation_id", ondelete="RESTRICT"), nullable=True
    )
    latest_event_sequence: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class OperationEventRow(Base):
    __tablename__ = "operation_events"
    __table_args__ = (
        UniqueConstraint("operation_id", "event_identity", name="uq_operation_event_identity"),
    )

    event_sequence: Mapped[int] = mapped_column(BigInteger, Identity(start=1), primary_key=True)
    event_id: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    event_identity: Mapped[str] = mapped_column(String(64), nullable=False)
    operation_id: Mapped[str] = mapped_column(
        ForeignKey("execution_operations.operation_id", ondelete="RESTRICT"), nullable=False
    )
    source_phase: Mapped[str | None] = mapped_column(String(40), nullable=True)
    target_phase: Mapped[str] = mapped_column(String(40), nullable=False)
    outcome: Mapped[str | None] = mapped_column(String(64), nullable=True)
    refs: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class PrivateProviderProtocolStateRow(Base):
    __tablename__ = "private_provider_protocol_states"
    __table_args__ = (
        UniqueConstraint(
            "execution_attempt_id", "item_ordinal", name="uq_private_protocol_item_ordinal"
        ),
        CheckConstraint("item_ordinal >= 1", name="ck_private_protocol_item_ordinal"),
        CheckConstraint("byte_count >= 0", name="ck_private_protocol_byte_count"),
    )

    protocol_state_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    execution_attempt_id: Mapped[str] = mapped_column(
        ForeignKey("execution_attempts.execution_attempt_id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    operation_id: Mapped[str] = mapped_column(
        ForeignKey("execution_operations.operation_id", ondelete="RESTRICT"), nullable=False
    )
    item_ordinal: Mapped[int] = mapped_column(Integer, nullable=False)
    item_type: Mapped[str] = mapped_column(String(64), nullable=False)
    item_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    call_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    encrypted_body_ref: Mapped[str] = mapped_column(String(256), nullable=False)
    body_bytes: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    classification: Mapped[str] = mapped_column(String(64), nullable=False)
    byte_count: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ExecutionOutputRefRow(Base):
    __tablename__ = "execution_output_refs"

    output_ref_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    execution_attempt_id: Mapped[str] = mapped_column(
        ForeignKey("execution_attempts.execution_attempt_id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    ref_kind: Mapped[str] = mapped_column(String(64), nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    storage_ref: Mapped[str] = mapped_column(String(256), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class EvidenceRequirementSetRow(Base):
    __tablename__ = "evidence_requirement_sets"

    requirement_set_ref: Mapped[str] = mapped_column(String(224), primary_key=True)
    requirement_set_id: Mapped[str] = mapped_column(String(144), nullable=False)
    requirement_set_version: Mapped[str] = mapped_column(String(80), nullable=False)
    task_contract_id: Mapped[str] = mapped_column(String(160), nullable=False)
    task_contract_version: Mapped[str] = mapped_column(String(80), nullable=False)
    requirement_root_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class EvidenceRequirementRow(Base):
    __tablename__ = "evidence_requirements"
    __table_args__ = (
        CheckConstraint(
            "fingerprint_schema IN ("
            "'P1_6_EVIDENCE_REQUIREMENT_FINGERPRINT_V1',"
            "'P1_6_EVIDENCE_REQUIREMENT_FINGERPRINT_V2_DURABLE_CONTENT')",
            name="ck_evidence_requirements_fingerprint_schema",
        ),
        CheckConstraint(
            "((fingerprint_schema = 'P1_6_EVIDENCE_REQUIREMENT_FINGERPRINT_V1' "
            "AND NOT (payload ? 'fingerprint_schema') "
            "AND NOT (payload ? 'durable_content_requirement') "
            "AND NOT (payload ? 'durable_content_policy_ref') "
            "AND NOT (payload ? 'durable_content_policy_fingerprint')) "
            "OR (fingerprint_schema = "
            "'P1_6_EVIDENCE_REQUIREMENT_FINGERPRINT_V2_DURABLE_CONTENT' "
            "AND payload->>'fingerprint_schema' = fingerprint_schema "
            "AND payload->>'durable_content_requirement' = 'REQUIRED' "
            "AND length(payload->>'durable_content_policy_ref') > 0 "
            "AND payload->>'durable_content_policy_fingerprint' ~ '^[0-9a-f]{64}$'))",
            name="ck_evidence_requirements_schema_payload_cut",
        ),
    )

    requirement_ref: Mapped[str] = mapped_column(String(224), primary_key=True)
    requirement_set_ref: Mapped[str] = mapped_column(
        ForeignKey("evidence_requirement_sets.requirement_set_ref", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    profile: Mapped[str] = mapped_column(String(48), nullable=False)
    obligation: Mapped[str] = mapped_column(String(32), nullable=False)
    fingerprint_schema: Mapped[str] = mapped_column(String(96), nullable=False)
    fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class EvidenceContentObjectRow(Base):
    __tablename__ = "evidence_content_objects"
    __table_args__ = (
        Index("ix_evidence_content_objects_schema", "schema_id", "schema_version"),
        Index("ix_evidence_content_objects_content_hash", "content_hash"),
        UniqueConstraint(
            "owner_id",
            "owner_version",
            "object_id",
            "object_version",
            name="uq_evidence_content_object_identity",
        ),
        CheckConstraint(
            "byte_count >= 1 AND byte_count <= 65536",
            name="ck_evidence_content_objects_byte_count",
        ),
        CheckConstraint(
            "octet_length(canonical_body) = byte_count",
            name="ck_evidence_content_objects_body_length",
        ),
        CheckConstraint(
            "content_kind IN ('INLINE_CANONICAL_STRUCTURED_BODY',"
            "'DATABASE_OBSERVATION_REF','RUNTIME_OBSERVATION_REF')",
            name="ck_evidence_content_objects_kind",
        ),
        CheckConstraint(
            "sensitivity IN ('PUBLIC_SAFE','INTERNAL')",
            name="ck_evidence_content_objects_sensitivity",
        ),
    )

    serialized_ref: Mapped[str] = mapped_column(String(96), primary_key=True)
    content_identity_key: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    owner_id: Mapped[str] = mapped_column(String(160), nullable=False)
    owner_version: Mapped[str] = mapped_column(String(80), nullable=False)
    source_owner_authority_ref: Mapped[str] = mapped_column(String(320), nullable=False)
    source_owner_authority_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    object_id: Mapped[str] = mapped_column(String(160), nullable=False)
    object_version: Mapped[str] = mapped_column(String(80), nullable=False)
    content_kind: Mapped[str] = mapped_column(String(64), nullable=False)
    canonicalization: Mapped[str] = mapped_column(String(80), nullable=False)
    schema_id: Mapped[str] = mapped_column(String(160), nullable=False)
    schema_version: Mapped[str] = mapped_column(String(80), nullable=False)
    byte_count: Mapped[int] = mapped_column(Integer, nullable=False)
    content_hash_algorithm: Mapped[str] = mapped_column(String(16), nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    sensitivity: Mapped[str] = mapped_column(String(40), nullable=False)
    retention_policy: Mapped[str] = mapped_column(String(96), nullable=False)
    access_policy: Mapped[str] = mapped_column(String(64), nullable=False)
    canonical_body: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    content_authority_id: Mapped[str] = mapped_column(String(160), nullable=False)
    content_authority_version: Mapped[str] = mapped_column(String(80), nullable=False)
    content_authority_revision: Mapped[int] = mapped_column(Integer, nullable=False)
    payload_fingerprint_schema: Mapped[str] = mapped_column(String(80), nullable=False)
    payload_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)


class EvidenceCandidateContentBindingRow(Base):
    __tablename__ = "evidence_candidate_content_bindings"
    __table_args__ = (
        Index(
            "ix_evidence_candidate_content_bindings_content_ref",
            "durable_content_ref",
        ),
    )

    candidate_id: Mapped[str] = mapped_column(
        ForeignKey("evidence_candidates.candidate_id", ondelete="RESTRICT"), primary_key=True
    )
    candidate_version: Mapped[str] = mapped_column(String(80), nullable=False)
    candidate_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    durable_content_ref: Mapped[str] = mapped_column(
        ForeignKey("evidence_content_objects.serialized_ref", ondelete="RESTRICT"),
        nullable=False,
    )
    durable_content_payload_fingerprint: Mapped[str] = mapped_column(
        String(64), nullable=False
    )
    content_ref_metadata_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    requirement_ref: Mapped[str] = mapped_column(String(224), nullable=False)
    requirement_fingerprint_schema: Mapped[str] = mapped_column(String(96), nullable=False)
    requirement_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    requirement_set_ref: Mapped[str] = mapped_column(String(224), nullable=False)
    requirement_root_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    durable_content_policy_ref: Mapped[str] = mapped_column(String(320), nullable=False)
    durable_content_policy_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    binding_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    bound_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class EvidenceCheckpointRow(Base):
    __tablename__ = "evidence_checkpoints"
    __table_args__ = (
        CheckConstraint(
            "(target_state IS NOT NULL) <> "
            "(transition_purpose_id IS NOT NULL AND "
            "transition_purpose_version IS NOT NULL)",
            name="ck_evidence_checkpoint_exact_use",
        ),
    )

    checkpoint_ref: Mapped[str] = mapped_column(String(224), primary_key=True)
    requirement_set_ref: Mapped[str] = mapped_column(
        ForeignKey("evidence_requirement_sets.requirement_set_ref", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    task_contract_id: Mapped[str] = mapped_column(String(160), nullable=False)
    task_contract_version: Mapped[str] = mapped_column(String(80), nullable=False)
    source_state: Mapped[str] = mapped_column(String(40), nullable=False)
    target_state: Mapped[str | None] = mapped_column(String(40), nullable=True)
    transition_purpose_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    transition_purpose_version: Mapped[str | None] = mapped_column(String(80), nullable=True)
    fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class HumanDirectEvidenceIngressRow(Base):
    __tablename__ = "human_direct_evidence_ingress"

    ingress_record_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    ingress_record_version: Mapped[str] = mapped_column(String(80), nullable=False)
    serialized_ref: Mapped[str] = mapped_column(String(512), nullable=False, unique=True)
    fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    ingress_authority_id: Mapped[str] = mapped_column(String(160), nullable=False)
    ingress_authority_version: Mapped[str] = mapped_column(String(80), nullable=False)
    authenticated_principal_id: Mapped[str] = mapped_column(String(160), nullable=False)
    authenticated_session_id: Mapped[str] = mapped_column(String(160), nullable=False)
    task_contract_id: Mapped[str] = mapped_column(String(160), nullable=False)
    task_contract_version: Mapped[str] = mapped_column(String(80), nullable=False)
    work_run_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    checkpoint_ref: Mapped[str] = mapped_column(String(224), nullable=False)
    evidence_type_id: Mapped[str] = mapped_column(String(160), nullable=False)
    evidence_type_version: Mapped[str] = mapped_column(String(80), nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    provided_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class EvidenceCandidateRow(Base):
    __tablename__ = "evidence_candidates"

    candidate_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    candidate_version: Mapped[str] = mapped_column(String(80), nullable=False)
    candidate_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    task_contract_id: Mapped[str] = mapped_column(String(160), nullable=False)
    task_contract_version: Mapped[str] = mapped_column(String(80), nullable=False)
    checkpoint_ref: Mapped[str] = mapped_column(String(224), nullable=False)
    issuer_type: Mapped[str] = mapped_column(String(64), nullable=False)
    sensitivity: Mapped[str] = mapped_column(String(40), nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    human_ingress_record_ref: Mapped[str | None] = mapped_column(
        ForeignKey("human_direct_evidence_ingress.serialized_ref", ondelete="RESTRICT"),
        nullable=True,
    )
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class EvidenceAdmissionRequestRow(Base):
    __tablename__ = "evidence_admission_requests"

    admission_request_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    request_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    candidate_id: Mapped[str] = mapped_column(
        ForeignKey("evidence_candidates.candidate_id", ondelete="RESTRICT"), nullable=False
    )
    requirement_ref: Mapped[str] = mapped_column(String(224), nullable=False)
    requirement_set_ref: Mapped[str] = mapped_column(String(224), nullable=False)
    work_run_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    checkpoint_ref: Mapped[str] = mapped_column(String(224), nullable=False)
    observed_state: Mapped[str] = mapped_column(String(40), nullable=False)
    observed_state_version: Mapped[int] = mapped_column(Integer, nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class EvidenceEvaluationRow(Base):
    __tablename__ = "evidence_evaluations"

    evaluation_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    admission_request_id: Mapped[str] = mapped_column(
        ForeignKey("evidence_admission_requests.admission_request_id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    dimension_results: Mapped[list[dict[str, object]]] = mapped_column(JSONB, nullable=False)
    authority_version: Mapped[str] = mapped_column(String(80), nullable=False)
    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class EvidenceAdmissionDecisionRow(Base):
    __tablename__ = "evidence_admission_decisions"

    decision_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    event_sequence: Mapped[int] = mapped_column(
        BigInteger, Identity(start=1), nullable=False, unique=True
    )
    admission_request_id: Mapped[str] = mapped_column(
        ForeignKey("evidence_admission_requests.admission_request_id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    evaluation_id: Mapped[str] = mapped_column(
        ForeignKey("evidence_evaluations.evaluation_id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    outcome: Mapped[str] = mapped_column(String(24), nullable=False)
    reason: Mapped[str] = mapped_column(String(64), nullable=False)
    secondary_reasons: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    admitting_authority_version: Mapped[str] = mapped_column(String(80), nullable=False)
    decided_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class AdmittedEvidenceRow(Base):
    __tablename__ = "admitted_evidence"
    __table_args__ = (
        UniqueConstraint(
            "candidate_id",
            "requirement_ref",
            "work_run_id",
            "checkpoint_ref",
            name="uq_admitted_evidence_logical_mapping",
        ),
    )

    admitted_evidence_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    decision_id: Mapped[str] = mapped_column(
        ForeignKey("evidence_admission_decisions.decision_id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    candidate_id: Mapped[str] = mapped_column(
        ForeignKey("evidence_candidates.candidate_id", ondelete="RESTRICT"), nullable=False
    )
    requirement_ref: Mapped[str] = mapped_column(String(224), nullable=False)
    work_run_id: Mapped[str] = mapped_column(
        ForeignKey("work_runs.work_run_id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    checkpoint_ref: Mapped[str] = mapped_column(String(224), nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    coverage: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    admitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class EvidenceRequirementSatisfactionRow(Base):
    __tablename__ = "evidence_requirement_satisfactions"

    satisfaction_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    admitted_evidence_id: Mapped[str] = mapped_column(
        ForeignKey("admitted_evidence.admitted_evidence_id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    requirement_ref: Mapped[str] = mapped_column(String(224), nullable=False)
    work_run_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    checkpoint_ref: Mapped[str] = mapped_column(String(224), nullable=False)
    coverage: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class EvidenceReuseConsumptionRow(Base):
    __tablename__ = "evidence_reuse_consumptions"
    __table_args__ = (
        UniqueConstraint(
            "prior_admitted_evidence_ref",
            "requirement_ref",
            "work_run_id",
            "checkpoint_ref",
            "consumption_ordinal",
            name="uq_evidence_reuse_scope_ordinal",
        ),
    )

    consumption_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    prior_admitted_evidence_ref: Mapped[str] = mapped_column(
        String(288), nullable=False, index=True
    )
    admitted_evidence_id: Mapped[str] = mapped_column(
        ForeignKey("admitted_evidence.admitted_evidence_id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    requirement_ref: Mapped[str] = mapped_column(String(224), nullable=False)
    work_run_id: Mapped[str] = mapped_column(String(128), nullable=False)
    checkpoint_ref: Mapped[str] = mapped_column(String(224), nullable=False)
    policy_maximum: Mapped[int] = mapped_column(Integer, nullable=False)
    consumption_ordinal: Mapped[int] = mapped_column(Integer, nullable=False)
    consumed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class EvidenceSetEvaluationRow(Base):
    __tablename__ = "evidence_set_evaluations"

    evaluation_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    evaluation_version: Mapped[str] = mapped_column(String(80), nullable=False)
    work_run_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    source_state: Mapped[str] = mapped_column(String(40), nullable=False)
    state_version: Mapped[int] = mapped_column(Integer, nullable=False)
    checkpoint_ref: Mapped[str] = mapped_column(String(224), nullable=False)
    requirement_set_ref: Mapped[str] = mapped_column(String(224), nullable=False)
    outcome: Mapped[str] = mapped_column(String(24), nullable=False)
    full_requirement_root_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    checkpoint_subset_root_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    admitted_ref_root_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    evidence_authority_revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class EvidenceSetAttestationRow(Base):
    __tablename__ = "evidence_set_attestations"

    attestation_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    attestation_version: Mapped[str] = mapped_column(String(80), nullable=False)
    serialized_ref: Mapped[str] = mapped_column(String(288), nullable=False, unique=True)
    evidence_set_evaluation_id: Mapped[str] = mapped_column(
        ForeignKey("evidence_set_evaluations.evaluation_id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    work_run_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    checkpoint_ref: Mapped[str] = mapped_column(String(224), nullable=False)
    state_version: Mapped[int] = mapped_column(Integer, nullable=False)
    evidence_authority_revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class EvidenceAuthorityEventRow(Base):
    __tablename__ = "evidence_authority_events"
    __table_args__ = (
        UniqueConstraint("subject_ref", "event_kind", "replacement_ref", name="uq_evidence_event"),
    )

    event_sequence: Mapped[int] = mapped_column(BigInteger, Identity(start=1), primary_key=True)
    event_id: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    subject_ref: Mapped[str] = mapped_column(String(288), nullable=False, index=True)
    event_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    replacement_ref: Mapped[str] = mapped_column(String(288), nullable=False, default="NONE")
    reason: Mapped[str] = mapped_column(String(128), nullable=False)
    owner_id: Mapped[str] = mapped_column(String(160), nullable=False)
    authority_version: Mapped[str] = mapped_column(String(80), nullable=False)
    task_contract_id: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    task_contract_version: Mapped[str] = mapped_column(String(80), nullable=False)
    work_run_id: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    affected_refs: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    affected_mappings: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class HumanGateRow(Base):
    __tablename__ = "human_gates"

    human_gate_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    serialized_ref: Mapped[str] = mapped_column(String(288), nullable=False, unique=True)
    gate_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    task_contract_id: Mapped[str] = mapped_column(String(160), nullable=False)
    task_contract_version: Mapped[str] = mapped_column(String(80), nullable=False)
    work_run_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    opened_from_state: Mapped[str] = mapped_column(String(40), nullable=False)
    opened_from_state_version: Mapped[int] = mapped_column(Integer, nullable=False)
    bound_state_version: Mapped[int] = mapped_column(Integer, nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    opened_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class HumanGateAuthorityEventRow(Base):
    __tablename__ = "human_gate_authority_events"

    event_sequence: Mapped[int] = mapped_column(BigInteger, Identity(start=1), primary_key=True)
    event_id: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    human_gate_id: Mapped[str] = mapped_column(
        ForeignKey("human_gates.human_gate_id", ondelete="RESTRICT"), nullable=False, index=True
    )
    event_kind: Mapped[str] = mapped_column(String(40), nullable=False)
    prior_revision: Mapped[int] = mapped_column(Integer, nullable=False)
    new_revision: Mapped[int] = mapped_column(Integer, nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class HumanGateProjectionRow(Base):
    __tablename__ = "human_gate_projections"
    __table_args__ = (
        UniqueConstraint("work_run_id", "authority_epoch", name="uq_current_human_gate_epoch"),
    )

    human_gate_id: Mapped[str] = mapped_column(
        ForeignKey("human_gates.human_gate_id", ondelete="RESTRICT"), primary_key=True
    )
    work_run_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    authority_epoch: Mapped[str] = mapped_column(String(160), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    suspension_status: Mapped[str] = mapped_column(String(32), nullable=False)
    authority_revision: Mapped[int] = mapped_column(Integer, nullable=False)
    bound_state: Mapped[str] = mapped_column(String(40), nullable=False)
    bound_state_version: Mapped[int] = mapped_column(Integer, nullable=False)
    current_result_ref: Mapped[str | None] = mapped_column(String(288), nullable=True)
    latest_event_sequence: Mapped[int] = mapped_column(BigInteger, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class HumanResultRow(Base):
    __tablename__ = "human_results"

    human_result_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    serialized_ref: Mapped[str] = mapped_column(String(288), nullable=False, unique=True)
    human_result_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    human_gate_id: Mapped[str] = mapped_column(
        ForeignKey("human_gates.human_gate_id", ondelete="RESTRICT"), nullable=False, index=True
    )
    work_run_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    result_kind: Mapped[str] = mapped_column(String(24), nullable=False)
    authority_revision: Mapped[int] = mapped_column(Integer, nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    admitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class HumanResultAuthorityEventRow(Base):
    __tablename__ = "human_result_authority_events"

    event_sequence: Mapped[int] = mapped_column(BigInteger, Identity(start=1), primary_key=True)
    event_id: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    human_result_id: Mapped[str] = mapped_column(
        ForeignKey("human_results.human_result_id", ondelete="RESTRICT"), nullable=False, index=True
    )
    event_kind: Mapped[str] = mapped_column(String(40), nullable=False)
    prior_revision: Mapped[int] = mapped_column(Integer, nullable=False)
    new_revision: Mapped[int] = mapped_column(Integer, nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class HumanP1_7EvidenceProducerRow(Base):
    __tablename__ = "human_p1_7_evidence_producers"

    producer_ref_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    serialized_ref: Mapped[str] = mapped_column(String(512), nullable=False, unique=True)
    fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    human_result_ref: Mapped[str] = mapped_column(String(288), nullable=False, index=True)
    work_run_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class HumanGuardAttestationRow(Base):
    __tablename__ = "human_guard_attestations"

    attestation_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    serialized_ref: Mapped[str] = mapped_column(String(288), nullable=False, unique=True)
    fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    guard_id: Mapped[str] = mapped_column(String(48), nullable=False)
    work_run_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    state_version: Mapped[int] = mapped_column(Integer, nullable=False)
    authority_revision: Mapped[int] = mapped_column(Integer, nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class JudgmentPolicyRow(Base):
    __tablename__ = "judgment_policies"

    serialized_ref: Mapped[str] = mapped_column(String(288), primary_key=True)
    policy_scope_key: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    authority_revision: Mapped[int] = mapped_column(Integer, nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class JudgmentPolicyProjectionRow(Base):
    __tablename__ = "judgment_policy_projections"

    policy_scope_key: Mapped[str] = mapped_column(String(64), primary_key=True)
    current_policy_ref: Mapped[str] = mapped_column(
        ForeignKey("judgment_policies.serialized_ref", ondelete="RESTRICT"), nullable=False
    )
    authority_revision: Mapped[int] = mapped_column(Integer, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class CommandCenterJudgmentActionRow(Base):
    __tablename__ = "command_center_judgment_actions"

    serialized_ref: Mapped[str] = mapped_column(String(288), primary_key=True)
    fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    work_run_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class JudgmentEvaluationRow(Base):
    __tablename__ = "judgment_evaluations"

    evaluation_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    work_run_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    state_version: Mapped[int] = mapped_column(Integer, nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class JudgmentRow(Base):
    __tablename__ = "judgments"

    judgment_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    serialized_ref: Mapped[str] = mapped_column(String(288), nullable=False, unique=True)
    fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    evaluation_id: Mapped[str] = mapped_column(
        ForeignKey("judgment_evaluations.evaluation_id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    work_run_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    state_version: Mapped[int] = mapped_column(Integer, nullable=False)
    judgment_kind: Mapped[str] = mapped_column(String(40), nullable=False)
    authority_revision: Mapped[int] = mapped_column(Integer, nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class JudgmentAuthorityEventRow(Base):
    __tablename__ = "judgment_authority_events"

    event_sequence: Mapped[int] = mapped_column(BigInteger, Identity(start=1), primary_key=True)
    event_id: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    judgment_id: Mapped[str] = mapped_column(
        ForeignKey("judgments.judgment_id", ondelete="RESTRICT"), nullable=False, index=True
    )
    event_kind: Mapped[str] = mapped_column(String(40), nullable=False)
    prior_revision: Mapped[int] = mapped_column(Integer, nullable=False)
    new_revision: Mapped[int] = mapped_column(Integer, nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class JudgmentProjectionRow(Base):
    __tablename__ = "judgment_projections"

    work_run_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    judgment_id: Mapped[str] = mapped_column(
        ForeignKey("judgments.judgment_id", ondelete="RESTRICT"), nullable=False
    )
    authority_revision: Mapped[int] = mapped_column(Integer, nullable=False)
    latest_event_sequence: Mapped[int] = mapped_column(BigInteger, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class JudgmentGuardAttestationRow(Base):
    __tablename__ = "judgment_guard_attestations"

    attestation_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    serialized_ref: Mapped[str] = mapped_column(String(288), nullable=False, unique=True)
    fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    guard_id: Mapped[str] = mapped_column(String(48), nullable=False)
    work_run_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    state_version: Mapped[int] = mapped_column(Integer, nullable=False)
    authority_revision: Mapped[int] = mapped_column(Integer, nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
