"""Add P1-8 owner seals, terminal epoch identity, and current withdrawal support.

Revision ID: 20260831_0007
Revises: 20260831_0006
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260831_0007"
down_revision: str | None = "20260831_0006"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

JSONB = postgresql.JSONB(astext_type=sa.Text())


def upgrade() -> None:
    # The reviewed 0006 migration is historical. Nullable additions preserve any
    # predecessor rows; every 0007 runtime admission writes all four values.
    op.add_column("admitted_cycles", sa.Column("terminal_epoch_key", sa.String(64)))
    op.add_column(
        "admitted_cycles", sa.Column("terminal_epoch_payload_fingerprint", sa.String(64))
    )
    op.add_column(
        "admitted_cycles", sa.Column("source_owner_event_high_watermark", sa.BigInteger())
    )
    op.add_column(
        "admitted_cycles", sa.Column("memory_policy_event_high_watermark", sa.BigInteger())
    )
    op.create_index(
        "uq_admitted_cycles_terminal_epoch_key",
        "admitted_cycles",
        ["terminal_epoch_key"],
        unique=True,
        postgresql_where=sa.text("terminal_epoch_key IS NOT NULL"),
    )

    op.create_table(
        "next_action_policy_descriptor_enrollments",
        sa.Column("enrollment_id", sa.String(128), primary_key=True),
        sa.Column("eligibility_policy_ref", sa.String(288), nullable=False),
        sa.Column("eligibility_policy_fingerprint", sa.String(64), nullable=False),
        sa.Column("action_ref", sa.String(512), nullable=False),
        sa.Column("descriptor_fingerprint", sa.String(64), nullable=False),
        sa.Column("authority_revision", sa.BigInteger(), nullable=False),
        sa.Column("payload", JSONB, nullable=False),
        sa.Column("enrolled_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "eligibility_policy_ref",
            "action_ref",
            name="uq_next_action_policy_descriptor_enrollment",
        ),
    )
    op.create_index(
        "ix_na_policy_descriptor_enrollment_policy_ref",
        "next_action_policy_descriptor_enrollments",
        ["eligibility_policy_ref"],
    )
    op.create_index(
        "ix_na_policy_descriptor_enrollment_action_ref",
        "next_action_policy_descriptor_enrollments",
        ["action_ref"],
    )
    op.execute(
        "CREATE TRIGGER next_action_policy_descriptor_enrollments_append_only "
        "BEFORE UPDATE OR DELETE ON next_action_policy_descriptor_enrollments "
        "FOR EACH ROW EXECUTE FUNCTION aiscc_reject_evidence_history_mutation()"
    )
    op.execute(
        "REVOKE INSERT, UPDATE, DELETE ON next_action_policy_descriptor_enrollments FROM PUBLIC"
    )

    op.alter_column("next_action_projections", "selection_id", nullable=True)
    op.add_column(
        "next_action_projections",
        sa.Column("state", sa.String(32), nullable=False, server_default="CURRENT"),
    )
    op.add_column(
        "next_action_projections",
        sa.Column("reason", sa.String(96), nullable=False, server_default="SELECTED_CURRENT"),
    )
    op.create_check_constraint(
        "ck_next_action_projections_state",
        "next_action_projections",
        "state IN ('CURRENT','WITHDRAWN')",
    )


def downgrade() -> None:
    op.drop_constraint(
        "ck_next_action_projections_state", "next_action_projections", type_="check"
    )
    op.drop_column("next_action_projections", "reason")
    op.drop_column("next_action_projections", "state")
    op.alter_column("next_action_projections", "selection_id", nullable=False)
    op.drop_table("next_action_policy_descriptor_enrollments")
    op.drop_index("uq_admitted_cycles_terminal_epoch_key", table_name="admitted_cycles")
    op.drop_column("admitted_cycles", "memory_policy_event_high_watermark")
    op.drop_column("admitted_cycles", "source_owner_event_high_watermark")
    op.drop_column("admitted_cycles", "terminal_epoch_payload_fingerprint")
    op.drop_column("admitted_cycles", "terminal_epoch_key")
