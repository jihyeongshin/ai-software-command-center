from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Identity,
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
