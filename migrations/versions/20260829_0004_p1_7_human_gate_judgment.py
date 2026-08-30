"""Create P1-7 Human gate, result, Judgment, and guard authority tables.

Revision ID: 20260829_0004
Revises: 20260829_0003
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260829_0004"
down_revision: str | None = "20260829_0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    jsonb = postgresql.JSONB(astext_type=sa.Text())
    op.create_table(
        "human_gates",
        sa.Column("human_gate_id", sa.String(128), primary_key=True),
        sa.Column("serialized_ref", sa.String(288), nullable=False, unique=True),
        sa.Column("gate_fingerprint", sa.String(64), nullable=False),
        sa.Column("task_contract_id", sa.String(160), nullable=False),
        sa.Column("task_contract_version", sa.String(80), nullable=False),
        sa.Column("work_run_id", sa.String(128), nullable=False),
        sa.Column("opened_from_state", sa.String(40), nullable=False),
        sa.Column("opened_from_state_version", sa.Integer(), nullable=False),
        sa.Column("bound_state_version", sa.Integer(), nullable=False),
        sa.Column("payload", jsonb, nullable=False),
        sa.Column("opened_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_human_gates_work_run_id", "human_gates", ["work_run_id"])
    op.create_table(
        "human_gate_authority_events",
        sa.Column("event_sequence", sa.BigInteger(), sa.Identity(start=1), primary_key=True),
        sa.Column("event_id", sa.String(128), nullable=False, unique=True),
        sa.Column(
            "human_gate_id",
            sa.String(128),
            sa.ForeignKey("human_gates.human_gate_id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("event_kind", sa.String(40), nullable=False),
        sa.Column("prior_revision", sa.Integer(), nullable=False),
        sa.Column("new_revision", sa.Integer(), nullable=False),
        sa.Column("payload", jsonb, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_human_gate_authority_events_human_gate_id",
        "human_gate_authority_events",
        ["human_gate_id"],
    )
    op.create_table(
        "human_gate_projections",
        sa.Column(
            "human_gate_id",
            sa.String(128),
            sa.ForeignKey("human_gates.human_gate_id", ondelete="RESTRICT"),
            primary_key=True,
        ),
        sa.Column("work_run_id", sa.String(128), nullable=False),
        sa.Column("authority_epoch", sa.String(160), nullable=False),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("suspension_status", sa.String(32), nullable=False),
        sa.Column("authority_revision", sa.Integer(), nullable=False),
        sa.Column("bound_state", sa.String(40), nullable=False),
        sa.Column("bound_state_version", sa.Integer(), nullable=False),
        sa.Column("current_result_ref", sa.String(288)),
        sa.Column("latest_event_sequence", sa.BigInteger(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("work_run_id", "authority_epoch", name="uq_current_human_gate_epoch"),
    )
    op.create_index(
        "ix_human_gate_projections_work_run_id", "human_gate_projections", ["work_run_id"]
    )
    op.create_table(
        "human_results",
        sa.Column("human_result_id", sa.String(128), primary_key=True),
        sa.Column("serialized_ref", sa.String(288), nullable=False, unique=True),
        sa.Column("human_result_fingerprint", sa.String(64), nullable=False),
        sa.Column(
            "human_gate_id",
            sa.String(128),
            sa.ForeignKey("human_gates.human_gate_id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("work_run_id", sa.String(128), nullable=False),
        sa.Column("result_kind", sa.String(24), nullable=False),
        sa.Column("authority_revision", sa.Integer(), nullable=False),
        sa.Column("payload", jsonb, nullable=False),
        sa.Column("admitted_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_human_results_human_gate_id", "human_results", ["human_gate_id"])
    op.create_index("ix_human_results_work_run_id", "human_results", ["work_run_id"])
    op.create_table(
        "human_result_authority_events",
        sa.Column("event_sequence", sa.BigInteger(), sa.Identity(start=1), primary_key=True),
        sa.Column("event_id", sa.String(128), nullable=False, unique=True),
        sa.Column(
            "human_result_id",
            sa.String(128),
            sa.ForeignKey("human_results.human_result_id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("event_kind", sa.String(40), nullable=False),
        sa.Column("prior_revision", sa.Integer(), nullable=False),
        sa.Column("new_revision", sa.Integer(), nullable=False),
        sa.Column("payload", jsonb, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_human_result_authority_events_human_result_id",
        "human_result_authority_events",
        ["human_result_id"],
    )
    op.create_table(
        "human_p1_7_evidence_producers",
        sa.Column("producer_ref_id", sa.String(128), primary_key=True),
        sa.Column("serialized_ref", sa.String(512), nullable=False, unique=True),
        sa.Column("fingerprint", sa.String(64), nullable=False),
        sa.Column("human_result_ref", sa.String(288), nullable=False),
        sa.Column("work_run_id", sa.String(128), nullable=False),
        sa.Column("payload", jsonb, nullable=False),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_human_p1_7_evidence_producers_human_result_ref",
        "human_p1_7_evidence_producers",
        ["human_result_ref"],
    )
    op.create_index(
        "ix_human_p1_7_evidence_producers_work_run_id",
        "human_p1_7_evidence_producers",
        ["work_run_id"],
    )
    _guard_table("human_guard_attestations", jsonb)
    op.create_table(
        "judgment_policies",
        sa.Column("serialized_ref", sa.String(288), primary_key=True),
        sa.Column("policy_scope_key", sa.String(64), nullable=False),
        sa.Column("fingerprint", sa.String(64), nullable=False),
        sa.Column("authority_revision", sa.Integer(), nullable=False),
        sa.Column("payload", jsonb, nullable=False),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_judgment_policies_policy_scope_key", "judgment_policies", ["policy_scope_key"]
    )
    op.create_table(
        "judgment_policy_projections",
        sa.Column("policy_scope_key", sa.String(64), primary_key=True),
        sa.Column(
            "current_policy_ref",
            sa.String(288),
            sa.ForeignKey("judgment_policies.serialized_ref", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("authority_revision", sa.Integer(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "command_center_judgment_actions",
        sa.Column("serialized_ref", sa.String(288), primary_key=True),
        sa.Column("fingerprint", sa.String(64), nullable=False),
        sa.Column("work_run_id", sa.String(128), nullable=False),
        sa.Column("payload", jsonb, nullable=False),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_command_center_judgment_actions_work_run_id",
        "command_center_judgment_actions",
        ["work_run_id"],
    )
    op.create_table(
        "judgment_evaluations",
        sa.Column("evaluation_id", sa.String(128), primary_key=True),
        sa.Column("work_run_id", sa.String(128), nullable=False),
        sa.Column("state_version", sa.Integer(), nullable=False),
        sa.Column("payload", jsonb, nullable=False),
        sa.Column("evaluated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_judgment_evaluations_work_run_id", "judgment_evaluations", ["work_run_id"])
    op.create_table(
        "judgments",
        sa.Column("judgment_id", sa.String(128), primary_key=True),
        sa.Column("serialized_ref", sa.String(288), nullable=False, unique=True),
        sa.Column("fingerprint", sa.String(64), nullable=False),
        sa.Column(
            "evaluation_id",
            sa.String(128),
            sa.ForeignKey("judgment_evaluations.evaluation_id", ondelete="RESTRICT"),
            nullable=False,
            unique=True,
        ),
        sa.Column("work_run_id", sa.String(128), nullable=False),
        sa.Column("state_version", sa.Integer(), nullable=False),
        sa.Column("judgment_kind", sa.String(40), nullable=False),
        sa.Column("authority_revision", sa.Integer(), nullable=False),
        sa.Column("payload", jsonb, nullable=False),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_judgments_work_run_id", "judgments", ["work_run_id"])
    op.create_table(
        "judgment_authority_events",
        sa.Column("event_sequence", sa.BigInteger(), sa.Identity(start=1), primary_key=True),
        sa.Column("event_id", sa.String(128), nullable=False, unique=True),
        sa.Column(
            "judgment_id",
            sa.String(128),
            sa.ForeignKey("judgments.judgment_id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("event_kind", sa.String(40), nullable=False),
        sa.Column("prior_revision", sa.Integer(), nullable=False),
        sa.Column("new_revision", sa.Integer(), nullable=False),
        sa.Column("payload", jsonb, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_judgment_authority_events_judgment_id",
        "judgment_authority_events",
        ["judgment_id"],
    )
    op.create_table(
        "judgment_projections",
        sa.Column("work_run_id", sa.String(128), primary_key=True),
        sa.Column(
            "judgment_id",
            sa.String(128),
            sa.ForeignKey("judgments.judgment_id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("authority_revision", sa.Integer(), nullable=False),
        sa.Column("latest_event_sequence", sa.BigInteger(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    _guard_table("judgment_guard_attestations", jsonb)
    op.execute("""
        CREATE FUNCTION aiscc_reject_p1_7_history_mutation()
        RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN
          RAISE EXCEPTION 'AISCC P1-7 authority provenance is append-only';
        END; $$
    """)
    for table in _HISTORY_TABLES:
        op.execute(
            f"CREATE TRIGGER {table}_append_only BEFORE UPDATE OR DELETE ON {table} "
            "FOR EACH ROW EXECUTE FUNCTION aiscc_reject_p1_7_history_mutation()"
        )


def _guard_table(name: str, jsonb: postgresql.JSONB) -> None:
    op.create_table(
        name,
        sa.Column("attestation_id", sa.String(128), primary_key=True),
        sa.Column("serialized_ref", sa.String(288), nullable=False, unique=True),
        sa.Column("fingerprint", sa.String(64), nullable=False),
        sa.Column("guard_id", sa.String(48), nullable=False),
        sa.Column("work_run_id", sa.String(128), nullable=False),
        sa.Column("state_version", sa.Integer(), nullable=False),
        sa.Column("authority_revision", sa.Integer(), nullable=False),
        sa.Column("payload", jsonb, nullable=False),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True)),
    )
    op.create_index(f"ix_{name}_work_run_id", name, ["work_run_id"])


_HISTORY_TABLES = (
    "human_gates",
    "human_gate_authority_events",
    "human_results",
    "human_result_authority_events",
    "human_p1_7_evidence_producers",
    "human_guard_attestations",
    "judgment_policies",
    "command_center_judgment_actions",
    "judgment_evaluations",
    "judgments",
    "judgment_authority_events",
    "judgment_guard_attestations",
)


def downgrade() -> None:
    for table in _HISTORY_TABLES:
        op.execute(f"DROP TRIGGER IF EXISTS {table}_append_only ON {table}")
    for table in (
        "judgment_guard_attestations",
        "judgment_projections",
        "judgment_authority_events",
        "judgments",
        "judgment_evaluations",
        "command_center_judgment_actions",
        "judgment_policy_projections",
        "judgment_policies",
        "human_guard_attestations",
        "human_p1_7_evidence_producers",
        "human_result_authority_events",
        "human_results",
        "human_gate_projections",
        "human_gate_authority_events",
        "human_gates",
    ):
        op.drop_table(table)
    op.execute("DROP FUNCTION IF EXISTS aiscc_reject_p1_7_history_mutation()")
