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
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ExternalIdeExecutionLeaseRow(Base):
    __tablename__ = "external_ide_execution_leases"
    lease_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    work_run_id: Mapped[str] = mapped_column(
        ForeignKey("work_runs.work_run_id"), unique=True, nullable=False
    )
    producer_kind: Mapped[str] = mapped_column(String(64), nullable=False)
    canonical_body: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    body_sha256: Mapped[str] = mapped_column(String(64), nullable=False)


class ExternalIdeExecutionSubmissionRow(Base):
    __tablename__ = "external_ide_execution_submissions"
    submission_id: Mapped[str] = mapped_column(String(160), primary_key=True)
    lease_id: Mapped[str] = mapped_column(
        ForeignKey("external_ide_execution_leases.lease_id"), unique=True, nullable=False
    )
    work_run_id: Mapped[str] = mapped_column(ForeignKey("work_runs.work_run_id"), nullable=False)
    producer_kind: Mapped[str] = mapped_column(String(64), nullable=False)
    canonical_body: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    body_sha256: Mapped[str] = mapped_column(String(64), nullable=False)


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
    blocker_claim: Mapped[dict[str, object] | None] = mapped_column(JSONB, nullable=True)
    blocker_resolution_claim: Mapped[dict[str, object] | None] = mapped_column(JSONB, nullable=True)
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
    durable_content_payload_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
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


# P1-8 immutable authority rows intentionally retain canonical payloads alongside
# independently indexed identity/binding columns.  Projection rows are the only
# mutable rows in this group and are rebuildable from append-only events.
class CycleAdmissionRequestRow(Base):
    __tablename__ = "cycle_admission_requests"
    __table_args__ = (
        CheckConstraint(
            "terminal_state_version >= 1",
            name="ck_cycle_admission_requests_terminal_state_version",
        ),
    )

    request_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    request_version: Mapped[str] = mapped_column(String(80), nullable=False)
    request_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    cycle_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    cycle_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    project_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    work_run_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    terminal_state_version: Mapped[int] = mapped_column(Integer, nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class CycleEvaluationRow(Base):
    __tablename__ = "cycle_evaluations"
    __table_args__ = (CheckConstraint("outcome = 'ACCEPTED'", name="ck_cycle_evaluations_outcome"),)

    evaluation_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    request_id: Mapped[str] = mapped_column(
        ForeignKey("cycle_admission_requests.request_id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    evaluation_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    outcome: Mapped[str] = mapped_column(String(32), nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class CycleAdmissionDecisionRow(Base):
    __tablename__ = "cycle_admission_decisions"
    __table_args__ = (
        CheckConstraint("outcome = 'ADMITTED'", name="ck_cycle_admission_decisions_outcome"),
    )

    decision_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    evaluation_id: Mapped[str] = mapped_column(
        ForeignKey("cycle_evaluations.evaluation_id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    request_id: Mapped[str] = mapped_column(
        ForeignKey("cycle_admission_requests.request_id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    decision_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    outcome: Mapped[str] = mapped_column(String(24), nullable=False)
    reason: Mapped[str] = mapped_column(String(64), nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    decided_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class AdmittedCycleRow(Base):
    __tablename__ = "admitted_cycles"

    __table_args__ = (
        Index(
            "uq_admitted_cycles_terminal_epoch_key",
            "terminal_epoch_key",
            unique=True,
            postgresql_where=text("terminal_epoch_key IS NOT NULL"),
        ),
    )

    cycle_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    cycle_version: Mapped[str] = mapped_column(String(80), nullable=False)
    serialized_ref: Mapped[str] = mapped_column(String(288), nullable=False, unique=True)
    cycle_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    request_id: Mapped[str] = mapped_column(
        ForeignKey("cycle_admission_requests.request_id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    decision_id: Mapped[str] = mapped_column(
        ForeignKey("cycle_admission_decisions.decision_id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    project_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    work_run_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    terminal_state_version: Mapped[int] = mapped_column(Integer, nullable=False)
    terminal_epoch_key: Mapped[str | None] = mapped_column(String(64), nullable=True)
    terminal_epoch_payload_fingerprint: Mapped[str | None] = mapped_column(
        String(64), nullable=True
    )
    source_owner_event_high_watermark: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    memory_policy_event_high_watermark: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    task_constraint_ref: Mapped[str | None] = mapped_column(String(288), nullable=True)
    task_constraint_fingerprint: Mapped[str | None] = mapped_column(String(64), nullable=True)
    task_constraint_snapshot_ref: Mapped[str | None] = mapped_column(String(288), nullable=True)
    task_constraint_snapshot_fingerprint: Mapped[str | None] = mapped_column(
        String(64), nullable=True
    )
    task_constraint_event_high_watermark: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    admission_sequence: Mapped[int] = mapped_column(
        BigInteger, Identity(start=1), nullable=False, unique=True
    )
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    admitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class CycleAuthorityEventRow(Base):
    __tablename__ = "cycle_authority_events"

    event_sequence: Mapped[int] = mapped_column(BigInteger, Identity(start=1), primary_key=True)
    event_id: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    cycle_id: Mapped[str] = mapped_column(
        ForeignKey("admitted_cycles.cycle_id", ondelete="RESTRICT"), nullable=False
    )
    event_kind: Mapped[str] = mapped_column(String(40), nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class MemoryDeclarationPolicyRow(Base):
    __tablename__ = "memory_declaration_policies"

    serialized_ref: Mapped[str] = mapped_column(String(288), primary_key=True)
    fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    authority_revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class MemoryPolicyAuthorityEventRow(Base):
    __tablename__ = "memory_policy_authority_events"

    event_sequence: Mapped[int] = mapped_column(BigInteger, Identity(start=1), primary_key=True)
    event_id: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    policy_ref: Mapped[str] = mapped_column(String(288), nullable=False, index=True)
    event_kind: Mapped[str] = mapped_column(String(40), nullable=False)
    replacement_ref: Mapped[str] = mapped_column(String(288), nullable=False, default="NONE")
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ProjectMemoryEntryRow(Base):
    __tablename__ = "project_memory_entries"
    __table_args__ = (
        UniqueConstraint(
            "cycle_id",
            "declaration_ordinal",
            name="uq_project_memory_entry_cycle_ordinal",
        ),
        CheckConstraint(
            "category IN ('DECISION','INVARIANT_POINTER','CONSTRAINT_POINTER',"
            "'BLOCKER_RESOLUTION','PROVENANCE_POINTER','NEXT_ACTION_CONTEXT')",
            name="ck_project_memory_entries_category",
        ),
        CheckConstraint(
            "privacy IN ('INTERNAL','PUBLIC_SANITIZED','NON_EXPORTABLE')",
            name="ck_project_memory_entries_privacy",
        ),
    )

    entry_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    memory_lineage_key: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    project_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    cycle_id: Mapped[str] = mapped_column(
        ForeignKey("admitted_cycles.cycle_id", ondelete="RESTRICT"), nullable=False
    )
    declaration_ordinal: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[str] = mapped_column(String(40), nullable=False)
    content_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    policy_ref: Mapped[str] = mapped_column(String(288), nullable=False)
    policy_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(512), nullable=False)
    external_context_ref: Mapped[str | None] = mapped_column(
        String(288),
        ForeignKey("next_action_context_refs.context_ref", ondelete="RESTRICT"),
        nullable=True,
    )
    privacy: Mapped[str] = mapped_column(String(32), nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class CycleMemoryReferenceRow(Base):
    __tablename__ = "cycle_memory_references"
    __table_args__ = (
        UniqueConstraint(
            "cycle_id",
            "declaration_ordinal",
            name="uq_cycle_memory_reference_cycle_ordinal",
        ),
    )

    reference_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    cycle_id: Mapped[str] = mapped_column(
        ForeignKey("admitted_cycles.cycle_id", ondelete="RESTRICT"), nullable=False
    )
    entry_id: Mapped[str] = mapped_column(
        ForeignKey("project_memory_entries.entry_id", ondelete="RESTRICT"), nullable=False
    )
    declaration_ordinal: Mapped[int] = mapped_column(Integer, nullable=False)
    content_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    provenance: Mapped[dict[str, object] | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ProjectMemoryAuthorityEventRow(Base):
    __tablename__ = "project_memory_authority_events"
    __table_args__ = (
        CheckConstraint(
            "event_kind IN ('CURRENT','SUPERSEDED','REVOKED','EXPIRED')",
            name="ck_project_memory_authority_events_kind",
        ),
        CheckConstraint(
            "new_revision = prior_revision + 1",
            name="ck_project_memory_authority_events_revision",
        ),
    )

    event_sequence: Mapped[int] = mapped_column(BigInteger, Identity(start=1), primary_key=True)
    event_id: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    memory_lineage_key: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    subject_entry_id: Mapped[str] = mapped_column(String(64), nullable=False)
    replacement_entry_id: Mapped[str] = mapped_column(String(64), nullable=False, default="NONE")
    event_kind: Mapped[str] = mapped_column(String(40), nullable=False)
    prior_revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    new_revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    authority_ref: Mapped[str] = mapped_column(String(512), nullable=False)
    reason: Mapped[str] = mapped_column(String(96), nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ProjectMemoryViewRow(Base):
    __tablename__ = "project_memory_views"
    __table_args__ = (
        CheckConstraint(
            "state IN ('CURRENT','SUPERSEDED','REVOKED','EXPIRED')",
            name="ck_project_memory_views_state",
        ),
    )

    memory_lineage_key: Mapped[str] = mapped_column(String(64), primary_key=True)
    project_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    current_entry_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    state: Mapped[str] = mapped_column(String(32), nullable=False)
    reason: Mapped[str] = mapped_column(String(96), nullable=False)
    authority_revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    latest_event_sequence: Mapped[int] = mapped_column(BigInteger, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class NextActionDescriptorRow(Base):
    __tablename__ = "next_action_descriptors"

    action_ref: Mapped[str] = mapped_column(String(512), primary_key=True)
    descriptor_version: Mapped[str] = mapped_column(String(80), nullable=False)
    fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    authority_revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    enrolled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class NextActionPolicyRow(Base):
    __tablename__ = "next_action_policies"
    __table_args__ = (
        CheckConstraint(
            "policy_kind IN ('ELIGIBILITY','SELECTION')",
            name="ck_next_action_policies_kind",
        ),
    )

    policy_ref: Mapped[str] = mapped_column(String(288), primary_key=True)
    policy_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    authority_revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class NextActionOwnerEventRow(Base):
    __tablename__ = "next_action_owner_events"

    event_sequence: Mapped[int] = mapped_column(BigInteger, Identity(start=1), primary_key=True)
    event_id: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    subject_ref: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    subject_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    event_kind: Mapped[str] = mapped_column(String(40), nullable=False)
    replacement_ref: Mapped[str] = mapped_column(String(512), nullable=False, default="NONE")
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class NextActionPolicyDescriptorEnrollmentRow(Base):
    __tablename__ = "next_action_policy_descriptor_enrollments"
    __table_args__ = (
        UniqueConstraint(
            "eligibility_policy_ref",
            "action_ref",
            name="uq_next_action_policy_descriptor_enrollment",
        ),
        Index(
            "ix_na_policy_descriptor_enrollment_policy_ref",
            "eligibility_policy_ref",
        ),
        Index("ix_na_policy_descriptor_enrollment_action_ref", "action_ref"),
    )

    enrollment_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    eligibility_policy_ref: Mapped[str] = mapped_column(String(288), nullable=False)
    eligibility_policy_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    action_ref: Mapped[str] = mapped_column(String(512), nullable=False)
    descriptor_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    authority_revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    enrolled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class NextActionProposalRow(Base):
    __tablename__ = "next_action_proposals"

    proposal_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    project_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    action_ref: Mapped[str] = mapped_column(String(512), nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    proposed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class NextActionEvaluationRow(Base):
    __tablename__ = "next_action_evaluations"

    evaluation_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    project_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    project_revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class NextActionSelectionRow(Base):
    __tablename__ = "next_action_selections"
    __table_args__ = (
        UniqueConstraint(
            "project_id",
            "project_revision",
            name="uq_next_action_selection_project_revision",
        ),
    )

    selection_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    serialized_ref: Mapped[str] = mapped_column(String(288), nullable=False, unique=True)
    fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    project_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    project_revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    evaluation_id: Mapped[str] = mapped_column(
        ForeignKey("next_action_evaluations.evaluation_id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    action_ref: Mapped[str] = mapped_column(String(512), nullable=False)
    external_context_ref: Mapped[str | None] = mapped_column(String(288), nullable=True)
    external_context_fingerprint: Mapped[str | None] = mapped_column(String(64), nullable=True)
    external_context_snapshot_ref: Mapped[str | None] = mapped_column(String(288), nullable=True)
    external_context_snapshot_fingerprint: Mapped[str | None] = mapped_column(
        String(64), nullable=True
    )
    external_context_event_high_watermark: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    memory_authority_event_high_watermark: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    selected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class NextActionAuthorityEventRow(Base):
    __tablename__ = "next_action_authority_events"
    __table_args__ = (
        CheckConstraint(
            "new_revision = prior_revision + 1",
            name="ck_next_action_authority_events_revision",
        ),
    )

    event_sequence: Mapped[int] = mapped_column(BigInteger, Identity(start=1), primary_key=True)
    event_id: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    project_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    selection_id: Mapped[str] = mapped_column(String(128), nullable=False)
    event_kind: Mapped[str] = mapped_column(String(40), nullable=False)
    prior_revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    new_revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class NextActionProjectionRow(Base):
    __tablename__ = "next_action_projections"
    __table_args__ = (
        CheckConstraint(
            "state IN ('CURRENT','WITHDRAWN')",
            name="ck_next_action_projections_state",
        ),
    )

    project_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    selection_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    state: Mapped[str] = mapped_column(String(32), nullable=False, default="CURRENT")
    reason: Mapped[str] = mapped_column(String(96), nullable=False, default="SELECTED_CURRENT")
    project_revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    latest_event_sequence: Mapped[int] = mapped_column(BigInteger, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class TaskIssuanceCandidateRow(Base):
    __tablename__ = "task_issuance_candidates"
    __table_args__ = (
        CheckConstraint(
            "issuance_owner = 'EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY'",
            name="ck_task_issuance_candidates_owner",
        ),
    )

    candidate_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    selection_id: Mapped[str] = mapped_column(
        ForeignKey("next_action_selections.selection_id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    issuance_owner: Mapped[str] = mapped_column(String(160), nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


# EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY is a separate owner domain. Its immutable
# objects/events/snapshots are never projections of P1-8 Memory or NextAction rows.
class ExternalTaskAuthorityCounterRow(Base):
    __tablename__ = "external_task_authority_counters"
    __table_args__ = (
        CheckConstraint("object_sequence >= 0", name="ck_ext_task_counter_object_nonnegative"),
        CheckConstraint("event_sequence >= 0", name="ck_ext_task_counter_event_nonnegative"),
        CheckConstraint(
            "object_sequence <= 9007199254740991",
            name="ck_ext_task_counter_object_safe_integer",
        ),
        CheckConstraint(
            "event_sequence <= 9007199254740991",
            name="ck_ext_task_counter_event_safe_integer",
        ),
    )

    counter_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    object_sequence: Mapped[int] = mapped_column(BigInteger, nullable=False)
    event_sequence: Mapped[int] = mapped_column(BigInteger, nullable=False)


class ExternalTaskAuthorityIssuerBindingRow(Base):
    __tablename__ = "external_task_authority_issuer_bindings"

    binding_ref: Mapped[str] = mapped_column(String(288), primary_key=True)
    binding_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    authority_owner: Mapped[str] = mapped_column(String(160), nullable=False)
    authority_version: Mapped[str] = mapped_column(String(160), nullable=False)
    authority_revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    bound_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ExternalTaskAuthorityEventRegistryRow(Base):
    __tablename__ = "external_task_authority_event_registry"
    __table_args__ = (
        CheckConstraint("event_sequence >= 1", name="ck_ext_task_event_sequence_positive"),
        CheckConstraint(
            "event_sequence <= 9007199254740991",
            name="ck_ext_task_event_sequence_safe_integer",
        ),
        CheckConstraint(
            "event_domain IN ('TASK_CONSTRAINT','NEXT_ACTION_CONTEXT')",
            name="ck_ext_task_event_domain",
        ),
    )

    event_sequence: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    event_ref: Mapped[str] = mapped_column(String(288), nullable=False, unique=True)
    event_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    event_domain: Mapped[str] = mapped_column(String(40), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class TaskConstraintRefRow(Base):
    __tablename__ = "task_constraint_refs"
    __table_args__ = (
        UniqueConstraint("issuance_sequence", name="uq_task_constraint_issuance_sequence"),
        CheckConstraint("issuance_sequence >= 1", name="ck_task_constraint_issuance_positive"),
        CheckConstraint(
            "scope_kind IN ('PROJECT','TASK_CONTRACT','WORK_RUN')",
            name="ck_task_constraint_scope_kind",
        ),
    )

    constraint_ref: Mapped[str] = mapped_column(String(288), primary_key=True)
    constraint_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    logical_key: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    logical_constraint_id: Mapped[str] = mapped_column(String(160), nullable=False)
    scope_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    project_id: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    task_contract_id: Mapped[str | None] = mapped_column(String(160), nullable=True)
    task_contract_version: Mapped[str | None] = mapped_column(String(80), nullable=True)
    work_run_id: Mapped[str | None] = mapped_column(String(160), nullable=True)
    issuance_sequence: Mapped[int] = mapped_column(BigInteger, nullable=False)
    issuer_binding_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class TaskConstraintAuthorityEventRow(Base):
    __tablename__ = "task_constraint_authority_events"
    __table_args__ = (
        UniqueConstraint(
            "logical_key",
            "effective_sequence",
            name="uq_task_constraint_logical_effective_sequence",
        ),
        CheckConstraint("effective_sequence >= 1", name="ck_task_constraint_effective_positive"),
    )

    event_ref: Mapped[str] = mapped_column(String(288), primary_key=True)
    event_id: Mapped[str] = mapped_column(String(160), nullable=False, unique=True)
    event_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    event_sequence: Mapped[int] = mapped_column(
        ForeignKey("external_task_authority_event_registry.event_sequence", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    effective_sequence: Mapped[int] = mapped_column(BigInteger, nullable=False)
    logical_key: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    event_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    constraint_ref: Mapped[str] = mapped_column(String(288), nullable=False)
    replacement_constraint_ref: Mapped[str | None] = mapped_column(String(288), nullable=True)
    issuer_binding_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    effective_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class TaskConstraintCurrentRow(Base):
    __tablename__ = "task_constraint_current"

    logical_key: Mapped[str] = mapped_column(String(64), primary_key=True)
    current_constraint_ref: Mapped[str | None] = mapped_column(String(288), nullable=True)
    terminal_revoked: Mapped[str] = mapped_column(String(8), nullable=False)
    effective_sequence: Mapped[int] = mapped_column(BigInteger, nullable=False)
    latest_event_sequence: Mapped[int] = mapped_column(BigInteger, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class TaskConstraintOwnerSnapshotRow(Base):
    __tablename__ = "task_constraint_owner_snapshots"
    __table_args__ = (Index("ix_task_constraint_owner_snapshots_h", "owner_event_high_watermark"),)

    snapshot_ref: Mapped[str] = mapped_column(String(288), primary_key=True)
    snapshot_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    owner_event_high_watermark: Mapped[int] = mapped_column(BigInteger, nullable=False)
    ordered_event_prefix_root: Mapped[str] = mapped_column(String(64), nullable=False)
    issuer_binding_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class NextActionContextRefRow(Base):
    __tablename__ = "next_action_context_refs"
    __table_args__ = (
        UniqueConstraint("issuance_sequence", name="uq_next_action_context_issuance_sequence"),
        CheckConstraint("issuance_sequence >= 1", name="ck_next_action_context_issuance_positive"),
        CheckConstraint(
            "critical_path_ordinal BETWEEN 1 AND 1000000",
            name="ck_next_action_context_ordinal",
        ),
    )

    context_ref: Mapped[str] = mapped_column(String(288), primary_key=True)
    context_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    logical_key: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    context_logical_id: Mapped[str] = mapped_column(String(200), nullable=False)
    project_id: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    task_contract_id: Mapped[str] = mapped_column(String(160), nullable=False)
    task_contract_version: Mapped[str] = mapped_column(String(80), nullable=False)
    context_slot_id: Mapped[str] = mapped_column(String(80), nullable=False)
    priority_class: Mapped[str] = mapped_column(String(64), nullable=False)
    critical_path_ordinal: Mapped[int] = mapped_column(Integer, nullable=False)
    issuance_sequence: Mapped[int] = mapped_column(BigInteger, nullable=False)
    effective_sequence: Mapped[int] = mapped_column(BigInteger, nullable=False)
    issuer_binding_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class NextActionContextAuthorityEventRow(Base):
    __tablename__ = "next_action_context_authority_events"
    __table_args__ = (
        UniqueConstraint(
            "logical_key",
            "effective_sequence",
            name="uq_next_action_context_logical_effective_sequence",
        ),
        CheckConstraint(
            "effective_sequence >= 1", name="ck_next_action_context_effective_positive"
        ),
    )

    event_ref: Mapped[str] = mapped_column(String(288), primary_key=True)
    event_id: Mapped[str] = mapped_column(String(160), nullable=False, unique=True)
    event_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    event_sequence: Mapped[int] = mapped_column(
        ForeignKey("external_task_authority_event_registry.event_sequence", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    effective_sequence: Mapped[int] = mapped_column(BigInteger, nullable=False)
    logical_key: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    event_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    context_ref: Mapped[str] = mapped_column(String(288), nullable=False)
    replacement_context_ref: Mapped[str | None] = mapped_column(String(288), nullable=True)
    issuer_binding_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    effective_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class NextActionContextCurrentRow(Base):
    __tablename__ = "next_action_context_current"

    logical_key: Mapped[str] = mapped_column(String(64), primary_key=True)
    current_context_ref: Mapped[str | None] = mapped_column(String(288), nullable=True)
    terminal_revoked: Mapped[str] = mapped_column(String(8), nullable=False)
    effective_sequence: Mapped[int] = mapped_column(BigInteger, nullable=False)
    latest_event_sequence: Mapped[int] = mapped_column(BigInteger, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class P1_4BlockerProvenanceRow(Base):
    __tablename__ = "p1_4_blocker_provenance"
    __table_args__ = (
        UniqueConstraint("work_run_id", "blocked_epoch", name="uq_p1_4_blocker_work_run_epoch"),
        Index("ix_p1_4_blocker_work_run_id", "work_run_id"),
    )

    blocker_ref: Mapped[str] = mapped_column(String(288), primary_key=True)
    blocker_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    work_run_id: Mapped[str] = mapped_column(String(160), nullable=False)
    blocked_epoch: Mapped[int] = mapped_column(Integer, nullable=False)
    blocker_kind: Mapped[str] = mapped_column(String(40), nullable=False)
    reason_code: Mapped[str] = mapped_column(String(64), nullable=False)
    resumability: Mapped[str] = mapped_column(String(32), nullable=False)
    transition_request_id: Mapped[str] = mapped_column(
        ForeignKey("transition_requests.transition_request_id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    transition_decision_id: Mapped[str] = mapped_column(
        ForeignKey("transition_decisions.transition_decision_id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class P1_4BlockerResolvedAttestationRow(Base):
    __tablename__ = "p1_4_blocker_resolved_attestations"

    attestation_ref: Mapped[str] = mapped_column(String(288), primary_key=True)
    attestation_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    blocker_ref: Mapped[str] = mapped_column(
        ForeignKey("p1_4_blocker_provenance.blocker_ref", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    transition_request_id: Mapped[str] = mapped_column(
        ForeignKey("transition_requests.transition_request_id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    transition_decision_id: Mapped[str] = mapped_column(
        ForeignKey("transition_decisions.transition_decision_id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class P1_4BlockerProjectionRow(Base):
    __tablename__ = "p1_4_blocker_projections"

    work_run_id: Mapped[str] = mapped_column(String(160), primary_key=True)
    blocker_ref: Mapped[str | None] = mapped_column(String(288), nullable=True)
    state: Mapped[str] = mapped_column(String(32), nullable=False)
    blocked_epoch: Mapped[int] = mapped_column(Integer, nullable=False)
    authority_revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class TaskContractBodyRow(Base):
    __tablename__ = "task_contract_bodies"
    __table_args__ = (
        UniqueConstraint(
            "project_id", "contract_id", "contract_version", name="uq_task_contract_body_version"
        ),
        UniqueConstraint("constraint_ref", name="uq_task_contract_body_constraint"),
        UniqueConstraint("issuance_event_ref", name="uq_task_contract_body_event"),
        CheckConstraint(
            "contract_version BETWEEN 1 AND 9007199254740991", name="ck_task_contract_version"
        ),
        CheckConstraint(
            "octet_length(canonical_body) BETWEEN 1 AND 1048576", name="ck_task_contract_body_size"
        ),
        CheckConstraint("body_sha256 ~ '^[0-9a-f]{64}$'", name="ck_task_contract_body_hash"),
        CheckConstraint(
            "body_ref ~ '^task-contract-body:v1:sha256:[0-9a-f]{64}$'",
            name="ck_task_contract_body_ref",
        ),
        CheckConstraint(
            "body_schema_id = 'AISCC-TASKCONTRACT-BODY-V1'", name="ck_task_contract_body_schema"
        ),
        CheckConstraint(
            "(contract_version = 1 AND predecessor_version IS NULL "
            "AND predecessor_sha256 IS NULL) OR (contract_version > 1 "
            "AND predecessor_version IS NOT NULL AND predecessor_sha256 IS NOT NULL "
            "AND predecessor_version = contract_version - 1 "
            "AND predecessor_sha256 ~ '^[0-9a-f]{64}$')",
            name="ck_task_contract_predecessor",
        ),
    )
    body_ref: Mapped[str] = mapped_column(String(93), primary_key=True)
    body_schema_id: Mapped[str] = mapped_column(String(64), nullable=False)
    body_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    project_id: Mapped[str] = mapped_column(String(96), nullable=False)
    contract_id: Mapped[str] = mapped_column(String(96), nullable=False)
    task_id: Mapped[str] = mapped_column(String(96), nullable=False)
    contract_version: Mapped[int] = mapped_column(BigInteger, nullable=False)
    canonical_body: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    constraint_ref: Mapped[str] = mapped_column(
        ForeignKey("task_constraint_refs.constraint_ref"), nullable=False
    )
    issuance_event_ref: Mapped[str] = mapped_column(
        ForeignKey("task_constraint_authority_events.event_ref"), nullable=False
    )
    predecessor_version: Mapped[int | None] = mapped_column(BigInteger)
    predecessor_sha256: Mapped[str | None] = mapped_column(String(64))
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ExternalIdeExecutionStartPermitRow(Base):
    __tablename__ = "external_ide_execution_start_permits"
    permit_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    work_run_id: Mapped[str] = mapped_column(
        ForeignKey("work_runs.work_run_id"), nullable=False, unique=True
    )
    producer_kind: Mapped[str] = mapped_column(String(64), nullable=False)
    canonical_body: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    body_sha256: Mapped[str] = mapped_column(String(64), nullable=False)


class ExternalIdeExecutionStartRow(Base):
    __tablename__ = "external_ide_execution_starts"
    start_id: Mapped[str] = mapped_column(String(160), primary_key=True)
    permit_id: Mapped[str] = mapped_column(
        ForeignKey("external_ide_execution_start_permits.permit_id"), nullable=False, unique=True
    )
    work_run_id: Mapped[str] = mapped_column(
        ForeignKey("work_runs.work_run_id"), nullable=False, unique=True
    )
    transition_request_id: Mapped[str] = mapped_column(
        ForeignKey("transition_requests.transition_request_id"), nullable=False, unique=True
    )
    producer_kind: Mapped[str] = mapped_column(String(64), nullable=False)
    canonical_body: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    body_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
