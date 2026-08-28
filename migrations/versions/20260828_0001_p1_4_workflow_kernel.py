"""Create the P1-4 authoritative workflow kernel store.

Revision ID: 20260828_0001
Revises:
Create Date: 2026-08-28 09:28:00+09:00
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260828_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "work_runs",
        sa.Column("work_run_id", sa.String(length=128), primary_key=True),
        sa.Column("project_id", sa.String(length=128), nullable=False),
        sa.Column("task_contract_id", sa.String(length=160), nullable=False),
        sa.Column("task_contract_version", sa.String(length=80), nullable=False),
        sa.Column("workflow_state", sa.String(length=40), nullable=False),
        sa.Column("state_version", sa.Integer(), nullable=False),
        sa.Column("runtime_mode", sa.String(length=48), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("state_version >= 1", name="ck_work_runs_version"),
        sa.CheckConstraint(
            "workflow_state IN ('READY','RUNNING','ADMISSION_PENDING','HUMAN_REQUIRED',"
            "'BLOCKED','REWORK_REQUIRED','ACCEPTED','REJECTED','FAILED')",
            name="ck_work_runs_exact_state",
        ),
        sa.CheckConstraint(
            "runtime_mode IN ('OWNER_SELF_DOGFOOD','PUBLIC_RECORDED_REPLAY','PUBLIC_BOUNDED_LIVE')",
            name="ck_work_runs_exact_runtime_mode",
        ),
    )
    op.create_table(
        "transition_requests",
        sa.Column("transition_request_id", sa.String(length=128), primary_key=True),
        sa.Column("request_fingerprint", sa.String(length=64), nullable=False),
        sa.Column("project_id", sa.String(length=128), nullable=False),
        sa.Column("task_contract_id", sa.String(length=160), nullable=False),
        sa.Column("task_contract_version", sa.String(length=80), nullable=False),
        sa.Column("work_run_id", sa.String(length=128), nullable=False),
        sa.Column("observed_state", sa.String(length=40), nullable=True),
        sa.Column("observed_state_version", sa.Integer(), nullable=False),
        sa.Column("target_state", sa.String(length=40), nullable=False),
        sa.Column("requester_identity", sa.String(length=160), nullable=False),
        sa.Column("requester_type", sa.String(length=48), nullable=False),
        sa.Column("runtime_mode", sa.String(length=48), nullable=False),
        sa.Column("evidence_refs", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("human_result_refs", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("judgment_refs", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("parent_request_id", sa.String(length=128), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "observed_state IS NULL OR observed_state IN "
            "('READY','RUNNING','ADMISSION_PENDING','HUMAN_REQUIRED','BLOCKED',"
            "'REWORK_REQUIRED','ACCEPTED','REJECTED','FAILED')",
            name="ck_transition_requests_exact_observed_state",
        ),
        sa.CheckConstraint(
            "target_state IN ('READY','RUNNING','ADMISSION_PENDING','HUMAN_REQUIRED',"
            "'BLOCKED','REWORK_REQUIRED','ACCEPTED','REJECTED','FAILED')",
            name="ck_transition_requests_exact_target_state",
        ),
        sa.CheckConstraint(
            "runtime_mode IN ('OWNER_SELF_DOGFOOD','PUBLIC_RECORDED_REPLAY','PUBLIC_BOUNDED_LIVE')",
            name="ck_transition_requests_exact_runtime_mode",
        ),
    )
    op.create_index(
        "ix_transition_requests_work_run_id",
        "transition_requests",
        ["work_run_id"],
        unique=False,
    )
    op.create_table(
        "transition_evaluations",
        sa.Column("transition_evaluation_id", sa.String(length=128), primary_key=True),
        sa.Column(
            "transition_request_id",
            sa.String(length=128),
            sa.ForeignKey("transition_requests.transition_request_id", ondelete="RESTRICT"),
            nullable=False,
            unique=True,
        ),
        sa.Column("authoritative_state", sa.String(length=40), nullable=True),
        sa.Column("authoritative_state_version", sa.Integer(), nullable=False),
        sa.Column("guards", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("missing_guards", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("evaluated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "transition_decisions",
        sa.Column("transition_decision_id", sa.String(length=128), primary_key=True),
        sa.Column("event_sequence", sa.BigInteger(), sa.Identity(start=1), nullable=False),
        sa.Column(
            "transition_evaluation_id",
            sa.String(length=128),
            sa.ForeignKey("transition_evaluations.transition_evaluation_id", ondelete="RESTRICT"),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "transition_request_id",
            sa.String(length=128),
            sa.ForeignKey("transition_requests.transition_request_id", ondelete="RESTRICT"),
            nullable=False,
            unique=True,
        ),
        sa.Column("outcome", sa.String(length=24), nullable=False),
        sa.Column("reason", sa.String(length=48), nullable=False),
        sa.Column("resulting_state", sa.String(length=40), nullable=True),
        sa.Column("resulting_state_version", sa.Integer(), nullable=False),
        sa.Column("admitting_owner", sa.String(length=80), nullable=False),
        sa.Column("kernel_version", sa.String(length=80), nullable=False),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("event_sequence", name="uq_transition_decisions_event_sequence"),
        sa.CheckConstraint(
            "resulting_state IS NULL OR resulting_state IN "
            "('READY','RUNNING','ADMISSION_PENDING','HUMAN_REQUIRED','BLOCKED',"
            "'REWORK_REQUIRED','ACCEPTED','REJECTED','FAILED')",
            name="ck_transition_decisions_exact_resulting_state",
        ),
    )
    op.execute(
        """
        CREATE FUNCTION aiscc_reject_transition_history_mutation()
        RETURNS trigger LANGUAGE plpgsql AS $$
        BEGIN
          RAISE EXCEPTION 'AISCC transition provenance is append-only';
        END;
        $$
        """
    )
    for table_name in (
        "transition_requests",
        "transition_evaluations",
        "transition_decisions",
    ):
        op.execute(
            f"""
            CREATE TRIGGER {table_name}_append_only
            BEFORE UPDATE OR DELETE ON {table_name}
            FOR EACH ROW EXECUTE FUNCTION aiscc_reject_transition_history_mutation()
            """
        )


def downgrade() -> None:
    for table_name in (
        "transition_decisions",
        "transition_evaluations",
        "transition_requests",
    ):
        op.execute(f"DROP TRIGGER IF EXISTS {table_name}_append_only ON {table_name}")
    op.execute("DROP FUNCTION IF EXISTS aiscc_reject_transition_history_mutation()")
    op.drop_table("transition_decisions")
    op.drop_table("transition_evaluations")
    op.drop_index("ix_transition_requests_work_run_id", table_name="transition_requests")
    op.drop_table("transition_requests")
    op.drop_table("work_runs")
