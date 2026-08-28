"""Create P1-5 provider/tool execution authority tables.

Revision ID: 20260828_0002
Revises: 20260828_0001
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260828_0002"
down_revision: str | None = "20260828_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    jsonb = postgresql.JSONB(astext_type=sa.Text())
    op.create_table(
        "execution_attempts",
        sa.Column("execution_attempt_id", sa.String(128), primary_key=True),
        sa.Column(
            "work_run_id",
            sa.String(128),
            sa.ForeignKey("work_runs.work_run_id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("attempt_ordinal", sa.Integer(), nullable=False),
        sa.Column(
            "parent_attempt_id",
            sa.String(128),
            sa.ForeignKey("execution_attempts.execution_attempt_id", ondelete="RESTRICT"),
        ),
        sa.Column("task_contract_id", sa.String(160), nullable=False),
        sa.Column("task_contract_version", sa.String(80), nullable=False),
        sa.Column("runtime_mode", sa.String(48), nullable=False),
        sa.Column("provider_profile_id", sa.String(128), nullable=False),
        sa.Column("provider_profile_version", sa.String(80), nullable=False),
        sa.Column("tool_registry_id", sa.String(128), nullable=False),
        sa.Column("tool_registry_version", sa.String(80), nullable=False),
        sa.Column("creation_state", sa.String(40), nullable=False),
        sa.Column("creation_state_version", sa.Integer(), nullable=False),
        sa.Column("causal_state", sa.String(40), nullable=False),
        sa.Column("causal_state_version", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(40), nullable=False),
        sa.Column("execution_version", sa.Integer(), nullable=False),
        sa.Column("latest_event_sequence", sa.BigInteger(), nullable=False),
        sa.Column("counters", jsonb, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("work_run_id", "attempt_ordinal", name="uq_execution_attempt_ordinal"),
        sa.CheckConstraint("execution_version >= 1", name="ck_execution_attempt_version"),
        sa.CheckConstraint(
            "status IN ('NOT_STARTED','RUNNING','EXECUTOR_COMPLETED','EXECUTION_FAILED')",
            name="ck_execution_attempt_exact_status",
        ),
    )
    op.create_index("ix_execution_attempts_work_run_id", "execution_attempts", ["work_run_id"])
    op.create_table(
        "execution_events",
        sa.Column("event_sequence", sa.BigInteger(), sa.Identity(start=1), primary_key=True),
        sa.Column("event_id", sa.String(128), unique=True, nullable=False),
        sa.Column("event_identity", sa.String(64), nullable=False),
        sa.Column(
            "execution_attempt_id",
            sa.String(128),
            sa.ForeignKey("execution_attempts.execution_attempt_id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("event_kind", sa.String(64), nullable=False),
        sa.Column("status_before", sa.String(40)),
        sa.Column("status_after", sa.String(40), nullable=False),
        sa.Column("execution_version_after", sa.Integer(), nullable=False),
        sa.Column("causal_state", sa.String(40), nullable=False),
        sa.Column("causal_state_version", sa.Integer(), nullable=False),
        sa.Column("payload_hash", sa.String(64), nullable=False),
        sa.Column("refs", jsonb, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "execution_attempt_id", "event_identity", name="uq_execution_event_identity"
        ),
    )
    op.create_table(
        "execution_operations",
        sa.Column("operation_id", sa.String(128), primary_key=True),
        sa.Column(
            "execution_attempt_id",
            sa.String(128),
            sa.ForeignKey("execution_attempts.execution_attempt_id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("operation_kind", sa.String(32), nullable=False),
        sa.Column("operation_fingerprint", sa.String(64), nullable=False),
        sa.Column("current_phase", sa.String(40), nullable=False),
        sa.Column("outcome", sa.String(64)),
        sa.Column("resource_identity", sa.String(512), nullable=False),
        sa.Column("call_ordinal", sa.Integer(), nullable=False),
        sa.Column(
            "parent_operation_id",
            sa.String(128),
            sa.ForeignKey("execution_operations.operation_id", ondelete="RESTRICT"),
        ),
        sa.Column("latest_event_sequence", sa.BigInteger(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "execution_attempt_id", "call_ordinal", name="uq_execution_operation_call_ordinal"
        ),
        sa.CheckConstraint("call_ordinal >= 1", name="ck_execution_operation_call_ordinal"),
    )
    op.create_table(
        "operation_events",
        sa.Column("event_sequence", sa.BigInteger(), sa.Identity(start=1), primary_key=True),
        sa.Column("event_id", sa.String(128), unique=True, nullable=False),
        sa.Column("event_identity", sa.String(64), nullable=False),
        sa.Column(
            "operation_id",
            sa.String(128),
            sa.ForeignKey("execution_operations.operation_id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("source_phase", sa.String(40)),
        sa.Column("target_phase", sa.String(40), nullable=False),
        sa.Column("outcome", sa.String(64)),
        sa.Column("refs", jsonb, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("operation_id", "event_identity", name="uq_operation_event_identity"),
    )
    op.create_table(
        "private_provider_protocol_states",
        sa.Column("protocol_state_id", sa.String(128), primary_key=True),
        sa.Column(
            "execution_attempt_id",
            sa.String(128),
            sa.ForeignKey("execution_attempts.execution_attempt_id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "operation_id",
            sa.String(128),
            sa.ForeignKey("execution_operations.operation_id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("item_ordinal", sa.Integer(), nullable=False),
        sa.Column("item_type", sa.String(64), nullable=False),
        sa.Column("item_hash", sa.String(64), nullable=False),
        sa.Column("call_id", sa.String(128)),
        sa.Column("encrypted_body_ref", sa.String(256), nullable=False),
        sa.Column("body_bytes", sa.LargeBinary(), nullable=False),
        sa.Column("classification", sa.String(64), nullable=False),
        sa.Column("byte_count", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "execution_attempt_id", "item_ordinal", name="uq_private_protocol_item_ordinal"
        ),
        sa.CheckConstraint("item_ordinal >= 1", name="ck_private_protocol_item_ordinal"),
        sa.CheckConstraint("byte_count >= 0", name="ck_private_protocol_byte_count"),
    )
    op.create_index(
        "ix_private_provider_protocol_states_execution_attempt_id",
        "private_provider_protocol_states",
        ["execution_attempt_id"],
    )
    op.create_table(
        "execution_output_refs",
        sa.Column("output_ref_id", sa.String(128), primary_key=True),
        sa.Column(
            "execution_attempt_id",
            sa.String(128),
            sa.ForeignKey("execution_attempts.execution_attempt_id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("ref_kind", sa.String(64), nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("storage_ref", sa.String(256), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_execution_output_refs_execution_attempt_id",
        "execution_output_refs",
        ["execution_attempt_id"],
    )
    op.execute("""
        CREATE FUNCTION aiscc_reject_execution_history_mutation()
        RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN
          RAISE EXCEPTION 'AISCC execution provenance is append-only';
        END; $$
    """)
    for table in (
        "execution_events",
        "operation_events",
        "private_provider_protocol_states",
        "execution_output_refs",
    ):
        op.execute(
            f"CREATE TRIGGER {table}_append_only BEFORE UPDATE OR DELETE ON {table} "
            "FOR EACH ROW EXECUTE FUNCTION aiscc_reject_execution_history_mutation()"
        )


def downgrade() -> None:
    for table in (
        "execution_output_refs",
        "private_provider_protocol_states",
        "operation_events",
        "execution_events",
    ):
        op.execute(f"DROP TRIGGER IF EXISTS {table}_append_only ON {table}")
    op.execute("DROP FUNCTION IF EXISTS aiscc_reject_execution_history_mutation()")
    op.drop_index(
        "ix_execution_output_refs_execution_attempt_id", table_name="execution_output_refs"
    )
    op.drop_table("execution_output_refs")
    op.drop_index(
        "ix_private_provider_protocol_states_execution_attempt_id",
        table_name="private_provider_protocol_states",
    )
    op.drop_table("private_provider_protocol_states")
    op.drop_table("operation_events")
    op.drop_table("execution_operations")
    op.drop_table("execution_events")
    op.drop_index("ix_execution_attempts_work_run_id", table_name="execution_attempts")
    op.drop_table("execution_attempts")
