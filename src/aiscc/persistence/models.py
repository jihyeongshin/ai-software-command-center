from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Identity,
    Integer,
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
