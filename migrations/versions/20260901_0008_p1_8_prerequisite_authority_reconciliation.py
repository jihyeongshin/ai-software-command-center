"""P1-8 prerequisite authority reconciliation (additive only).

Revision ID: 20260901_0008
Revises: 20260831_0007
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "20260901_0008"
down_revision: str | None = "20260831_0007"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("transition_requests", sa.Column("blocker_claim", JSONB, nullable=True))
    op.add_column(
        "transition_requests", sa.Column("blocker_resolution_claim", JSONB, nullable=True)
    )
    for name, type_ in (
        ("task_constraint_ref", sa.String(288)),
        ("task_constraint_fingerprint", sa.String(64)),
        ("task_constraint_snapshot_ref", sa.String(288)),
        ("task_constraint_snapshot_fingerprint", sa.String(64)),
        ("task_constraint_event_high_watermark", sa.BigInteger()),
    ):
        op.add_column("admitted_cycles", sa.Column(name, type_, nullable=True))
    op.add_column(
        "project_memory_entries", sa.Column("external_context_ref", sa.String(288), nullable=True)
    )
    op.add_column("cycle_memory_references", sa.Column("provenance", JSONB, nullable=True))
    for name, type_ in (
        ("external_context_ref", sa.String(288)),
        ("external_context_fingerprint", sa.String(64)),
        ("external_context_snapshot_ref", sa.String(288)),
        ("external_context_snapshot_fingerprint", sa.String(64)),
        ("external_context_event_high_watermark", sa.BigInteger()),
        ("memory_authority_event_high_watermark", sa.BigInteger()),
    ):
        op.add_column("next_action_selections", sa.Column(name, type_, nullable=True))

    op.create_table(
        "external_task_authority_counters",
        sa.Column("counter_id", sa.String(64), primary_key=True),
        sa.Column("object_sequence", sa.BigInteger(), nullable=False),
        sa.Column("event_sequence", sa.BigInteger(), nullable=False),
        sa.CheckConstraint("object_sequence >= 0", name="ck_ext_task_counter_object_nonnegative"),
        sa.CheckConstraint("event_sequence >= 0", name="ck_ext_task_counter_event_nonnegative"),
        sa.CheckConstraint(
            "object_sequence <= 9007199254740991",
            name="ck_ext_task_counter_object_safe_integer",
        ),
        sa.CheckConstraint(
            "event_sequence <= 9007199254740991",
            name="ck_ext_task_counter_event_safe_integer",
        ),
    )
    op.create_table(
        "external_task_authority_issuer_bindings",
        sa.Column("binding_ref", sa.String(288), primary_key=True),
        sa.Column("binding_fingerprint", sa.String(64), nullable=False, unique=True),
        sa.Column("authority_owner", sa.String(160), nullable=False),
        sa.Column("authority_version", sa.String(160), nullable=False),
        sa.Column("authority_revision", sa.BigInteger(), nullable=False),
        sa.Column("payload", JSONB, nullable=False),
        sa.Column("bound_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "external_task_authority_event_registry",
        sa.Column("event_sequence", sa.BigInteger(), primary_key=True),
        sa.Column("event_ref", sa.String(288), nullable=False, unique=True),
        sa.Column("event_fingerprint", sa.String(64), nullable=False),
        sa.Column("event_domain", sa.String(40), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("event_sequence >= 1", name="ck_ext_task_event_sequence_positive"),
        sa.CheckConstraint(
            "event_sequence <= 9007199254740991",
            name="ck_ext_task_event_sequence_safe_integer",
        ),
        sa.CheckConstraint(
            "event_domain IN ('TASK_CONSTRAINT','NEXT_ACTION_CONTEXT')",
            name="ck_ext_task_event_domain",
        ),
    )
    op.create_table(
        "task_constraint_refs",
        sa.Column("constraint_ref", sa.String(288), primary_key=True),
        sa.Column("constraint_fingerprint", sa.String(64), nullable=False, unique=True),
        sa.Column("logical_key", sa.String(64), nullable=False),
        sa.Column("logical_constraint_id", sa.String(160), nullable=False),
        sa.Column("scope_kind", sa.String(32), nullable=False),
        sa.Column("project_id", sa.String(160), nullable=False),
        sa.Column("task_contract_id", sa.String(160), nullable=True),
        sa.Column("task_contract_version", sa.String(80), nullable=True),
        sa.Column("work_run_id", sa.String(160), nullable=True),
        sa.Column("issuance_sequence", sa.BigInteger(), nullable=False),
        sa.Column("issuer_binding_fingerprint", sa.String(64), nullable=False),
        sa.Column("payload", JSONB, nullable=False),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("issuance_sequence >= 1", name="ck_task_constraint_issuance_positive"),
        sa.CheckConstraint(
            "scope_kind IN ('PROJECT','TASK_CONTRACT','WORK_RUN')",
            name="ck_task_constraint_scope_kind",
        ),
        sa.UniqueConstraint(
            "issuance_sequence", name="uq_task_constraint_issuance_sequence"
        ),
    )
    op.create_index("ix_task_constraint_refs_logical_key", "task_constraint_refs", ["logical_key"])
    op.create_index("ix_task_constraint_refs_project_id", "task_constraint_refs", ["project_id"])
    op.create_table(
        "task_constraint_authority_events",
        sa.Column("event_ref", sa.String(288), primary_key=True),
        sa.Column("event_id", sa.String(160), nullable=False, unique=True),
        sa.Column("event_fingerprint", sa.String(64), nullable=False),
        sa.Column(
            "event_sequence",
            sa.BigInteger(),
            sa.ForeignKey(
                "external_task_authority_event_registry.event_sequence",
                ondelete="RESTRICT",
            ),
            nullable=False,
            unique=True,
        ),
        sa.Column("effective_sequence", sa.BigInteger(), nullable=False),
        sa.Column("logical_key", sa.String(64), nullable=False),
        sa.Column("event_kind", sa.String(32), nullable=False),
        sa.Column("constraint_ref", sa.String(288), nullable=False),
        sa.Column("replacement_constraint_ref", sa.String(288), nullable=True),
        sa.Column("issuer_binding_fingerprint", sa.String(64), nullable=False),
        sa.Column("payload", JSONB, nullable=False),
        sa.Column("effective_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "logical_key",
            "effective_sequence",
            name="uq_task_constraint_logical_effective_sequence",
        ),
        sa.CheckConstraint("effective_sequence >= 1", name="ck_task_constraint_effective_positive"),
    )
    op.create_index(
        "ix_task_constraint_authority_events_logical_key",
        "task_constraint_authority_events",
        ["logical_key"],
    )
    op.create_table(
        "task_constraint_current",
        sa.Column("logical_key", sa.String(64), primary_key=True),
        sa.Column("current_constraint_ref", sa.String(288), nullable=True),
        sa.Column("terminal_revoked", sa.String(8), nullable=False),
        sa.Column("effective_sequence", sa.BigInteger(), nullable=False),
        sa.Column("latest_event_sequence", sa.BigInteger(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "task_constraint_owner_snapshots",
        sa.Column("snapshot_ref", sa.String(288), primary_key=True),
        sa.Column("snapshot_fingerprint", sa.String(64), nullable=False, unique=True),
        sa.Column("owner_event_high_watermark", sa.BigInteger(), nullable=False),
        sa.Column("ordered_event_prefix_root", sa.String(64), nullable=False),
        sa.Column("issuer_binding_fingerprint", sa.String(64), nullable=False),
        sa.Column("payload", JSONB, nullable=False),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_task_constraint_owner_snapshots_h",
        "task_constraint_owner_snapshots",
        ["owner_event_high_watermark"],
    )
    op.create_table(
        "next_action_context_refs",
        sa.Column("context_ref", sa.String(288), primary_key=True),
        sa.Column("context_fingerprint", sa.String(64), nullable=False, unique=True),
        sa.Column("logical_key", sa.String(64), nullable=False),
        sa.Column("context_logical_id", sa.String(200), nullable=False),
        sa.Column("project_id", sa.String(160), nullable=False),
        sa.Column("task_contract_id", sa.String(160), nullable=False),
        sa.Column("task_contract_version", sa.String(80), nullable=False),
        sa.Column("context_slot_id", sa.String(80), nullable=False),
        sa.Column("priority_class", sa.String(64), nullable=False),
        sa.Column("critical_path_ordinal", sa.Integer(), nullable=False),
        sa.Column("issuance_sequence", sa.BigInteger(), nullable=False),
        sa.Column("effective_sequence", sa.BigInteger(), nullable=False),
        sa.Column("issuer_binding_fingerprint", sa.String(64), nullable=False),
        sa.Column("payload", JSONB, nullable=False),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "issuance_sequence >= 1", name="ck_next_action_context_issuance_positive"
        ),
        sa.CheckConstraint(
            "critical_path_ordinal BETWEEN 1 AND 1000000",
            name="ck_next_action_context_ordinal",
        ),
        sa.UniqueConstraint(
            "issuance_sequence", name="uq_next_action_context_issuance_sequence"
        ),
    )
    op.create_index(
        "ix_next_action_context_refs_logical_key", "next_action_context_refs", ["logical_key"]
    )
    op.create_index(
        "ix_next_action_context_refs_project_id", "next_action_context_refs", ["project_id"]
    )
    op.create_table(
        "next_action_context_authority_events",
        sa.Column("event_ref", sa.String(288), primary_key=True),
        sa.Column("event_id", sa.String(160), nullable=False, unique=True),
        sa.Column("event_fingerprint", sa.String(64), nullable=False),
        sa.Column(
            "event_sequence",
            sa.BigInteger(),
            sa.ForeignKey(
                "external_task_authority_event_registry.event_sequence",
                ondelete="RESTRICT",
            ),
            nullable=False,
            unique=True,
        ),
        sa.Column("effective_sequence", sa.BigInteger(), nullable=False),
        sa.Column("logical_key", sa.String(64), nullable=False),
        sa.Column("event_kind", sa.String(32), nullable=False),
        sa.Column("context_ref", sa.String(288), nullable=False),
        sa.Column("replacement_context_ref", sa.String(288), nullable=True),
        sa.Column("issuer_binding_fingerprint", sa.String(64), nullable=False),
        sa.Column("payload", JSONB, nullable=False),
        sa.Column("effective_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "logical_key",
            "effective_sequence",
            name="uq_next_action_context_logical_effective_sequence",
        ),
        sa.CheckConstraint(
            "effective_sequence >= 1", name="ck_next_action_context_effective_positive"
        ),
    )
    op.create_index(
        "ix_next_action_context_authority_events_logical_key",
        "next_action_context_authority_events",
        ["logical_key"],
    )
    op.create_table(
        "next_action_context_current",
        sa.Column("logical_key", sa.String(64), primary_key=True),
        sa.Column("current_context_ref", sa.String(288), nullable=True),
        sa.Column("terminal_revoked", sa.String(8), nullable=False),
        sa.Column("effective_sequence", sa.BigInteger(), nullable=False),
        sa.Column("latest_event_sequence", sa.BigInteger(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "p1_4_blocker_provenance",
        sa.Column("blocker_ref", sa.String(288), primary_key=True),
        sa.Column("blocker_fingerprint", sa.String(64), nullable=False, unique=True),
        sa.Column("work_run_id", sa.String(160), nullable=False),
        sa.Column("blocked_epoch", sa.Integer(), nullable=False),
        sa.Column("blocker_kind", sa.String(40), nullable=False),
        sa.Column("reason_code", sa.String(64), nullable=False),
        sa.Column("resumability", sa.String(32), nullable=False),
        sa.Column(
            "transition_request_id",
            sa.String(128),
            sa.ForeignKey(
                "transition_requests.transition_request_id", ondelete="RESTRICT"
            ),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "transition_decision_id",
            sa.String(128),
            sa.ForeignKey(
                "transition_decisions.transition_decision_id", ondelete="RESTRICT"
            ),
            nullable=False,
            unique=True,
        ),
        sa.Column("payload", JSONB, nullable=False),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("work_run_id", "blocked_epoch", name="uq_p1_4_blocker_work_run_epoch"),
    )
    op.create_index("ix_p1_4_blocker_work_run_id", "p1_4_blocker_provenance", ["work_run_id"])
    op.create_table(
        "p1_4_blocker_resolved_attestations",
        sa.Column("attestation_ref", sa.String(288), primary_key=True),
        sa.Column("attestation_fingerprint", sa.String(64), nullable=False, unique=True),
        sa.Column(
            "blocker_ref",
            sa.String(288),
            sa.ForeignKey("p1_4_blocker_provenance.blocker_ref", ondelete="RESTRICT"),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "transition_request_id",
            sa.String(128),
            sa.ForeignKey(
                "transition_requests.transition_request_id", ondelete="RESTRICT"
            ),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "transition_decision_id",
            sa.String(128),
            sa.ForeignKey(
                "transition_decisions.transition_decision_id", ondelete="RESTRICT"
            ),
            nullable=False,
            unique=True,
        ),
        sa.Column("payload", JSONB, nullable=False),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "p1_4_blocker_projections",
        sa.Column("work_run_id", sa.String(160), primary_key=True),
        sa.Column("blocker_ref", sa.String(288), nullable=True),
        sa.Column("state", sa.String(32), nullable=False),
        sa.Column("blocked_epoch", sa.Integer(), nullable=False),
        sa.Column("authority_revision", sa.BigInteger(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_foreign_key(
        "fk_project_memory_entries_external_context_ref",
        "project_memory_entries",
        "next_action_context_refs",
        ["external_context_ref"],
        ["context_ref"],
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_project_memory_entries_external_context_ref",
        "project_memory_entries",
        type_="foreignkey",
    )
    for table in (
        "p1_4_blocker_projections",
        "p1_4_blocker_resolved_attestations",
        "p1_4_blocker_provenance",
        "next_action_context_current",
        "next_action_context_authority_events",
        "next_action_context_refs",
        "task_constraint_owner_snapshots",
        "task_constraint_current",
        "task_constraint_authority_events",
        "task_constraint_refs",
        "external_task_authority_event_registry",
        "external_task_authority_issuer_bindings",
        "external_task_authority_counters",
    ):
        op.drop_table(table)
    for name in (
        "memory_authority_event_high_watermark",
        "external_context_event_high_watermark",
        "external_context_snapshot_fingerprint",
        "external_context_snapshot_ref",
        "external_context_fingerprint",
        "external_context_ref",
    ):
        op.drop_column("next_action_selections", name)
    op.drop_column("cycle_memory_references", "provenance")
    op.drop_column("project_memory_entries", "external_context_ref")
    for name in (
        "task_constraint_event_high_watermark",
        "task_constraint_snapshot_fingerprint",
        "task_constraint_snapshot_ref",
        "task_constraint_fingerprint",
        "task_constraint_ref",
    ):
        op.drop_column("admitted_cycles", name)
    op.drop_column("transition_requests", "blocker_resolution_claim")
    op.drop_column("transition_requests", "blocker_claim")
