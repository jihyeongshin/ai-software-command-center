"""Add P1-8 accepted Cycle, curated memory, and NextAction authorities.

Revision ID: 20260831_0006
Revises: 20260830_0005
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260831_0006"
down_revision: str | None = "20260830_0005"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

JSONB = postgresql.JSONB(astext_type=sa.Text())


def _history_table(name: str, *columns: sa.Column[object], constraints: object = ()) -> None:
    extras = constraints if isinstance(constraints, tuple) else (constraints,)
    op.create_table(name, *columns, *extras)


def _immutability(name: str) -> None:
    op.execute(
        f"CREATE TRIGGER {name}_append_only BEFORE UPDATE OR DELETE ON {name} "
        "FOR EACH ROW EXECUTE FUNCTION aiscc_reject_evidence_history_mutation()"
    )
    op.execute(f"REVOKE INSERT, UPDATE, DELETE ON {name} FROM PUBLIC")


def upgrade() -> None:
    _history_table(
        "cycle_admission_requests",
        sa.Column("request_id", sa.String(128), primary_key=True),
        sa.Column("request_version", sa.String(80), nullable=False),
        sa.Column("request_fingerprint", sa.String(64), nullable=False),
        sa.Column("cycle_id", sa.String(128), nullable=False),
        sa.Column("cycle_fingerprint", sa.String(64), nullable=False),
        sa.Column("project_id", sa.String(128), nullable=False),
        sa.Column("work_run_id", sa.String(128), nullable=False),
        sa.Column("terminal_state_version", sa.Integer(), nullable=False),
        sa.Column("payload", JSONB, nullable=False),
        sa.Column("requested_at", sa.DateTime(timezone=True), nullable=False),
        constraints=sa.CheckConstraint(
            "terminal_state_version >= 1",
            name="ck_cycle_admission_requests_terminal_state_version",
        ),
    )
    op.create_index(
        "ix_cycle_admission_requests_cycle_id", "cycle_admission_requests", ["cycle_id"]
    )
    op.create_index(
        "ix_cycle_admission_requests_project_id", "cycle_admission_requests", ["project_id"]
    )
    op.create_index(
        "ix_cycle_admission_requests_work_run_id", "cycle_admission_requests", ["work_run_id"]
    )
    _history_table(
        "cycle_evaluations",
        sa.Column("evaluation_id", sa.String(128), primary_key=True),
        sa.Column(
            "request_id",
            sa.String(128),
            sa.ForeignKey("cycle_admission_requests.request_id", ondelete="RESTRICT"),
            nullable=False,
            unique=True,
        ),
        sa.Column("evaluation_fingerprint", sa.String(64), nullable=False),
        sa.Column("outcome", sa.String(32), nullable=False),
        sa.Column("payload", JSONB, nullable=False),
        sa.Column("evaluated_at", sa.DateTime(timezone=True), nullable=False),
        constraints=sa.CheckConstraint("outcome = 'ACCEPTED'", name="ck_cycle_evaluations_outcome"),
    )
    _history_table(
        "cycle_admission_decisions",
        sa.Column("decision_id", sa.String(128), primary_key=True),
        sa.Column(
            "evaluation_id",
            sa.String(128),
            sa.ForeignKey("cycle_evaluations.evaluation_id", ondelete="RESTRICT"),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "request_id",
            sa.String(128),
            sa.ForeignKey("cycle_admission_requests.request_id", ondelete="RESTRICT"),
            nullable=False,
            unique=True,
        ),
        sa.Column("decision_fingerprint", sa.String(64), nullable=False),
        sa.Column("outcome", sa.String(24), nullable=False),
        sa.Column("reason", sa.String(64), nullable=False),
        sa.Column("payload", JSONB, nullable=False),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=False),
        constraints=sa.CheckConstraint(
            "outcome = 'ADMITTED'", name="ck_cycle_admission_decisions_outcome"
        ),
    )
    _history_table(
        "admitted_cycles",
        sa.Column("cycle_id", sa.String(128), primary_key=True),
        sa.Column("cycle_version", sa.String(80), nullable=False),
        sa.Column("serialized_ref", sa.String(288), nullable=False, unique=True),
        sa.Column("cycle_fingerprint", sa.String(64), nullable=False),
        sa.Column(
            "request_id",
            sa.String(128),
            sa.ForeignKey("cycle_admission_requests.request_id", ondelete="RESTRICT"),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "decision_id",
            sa.String(128),
            sa.ForeignKey("cycle_admission_decisions.decision_id", ondelete="RESTRICT"),
            nullable=False,
            unique=True,
        ),
        sa.Column("project_id", sa.String(128), nullable=False),
        sa.Column("work_run_id", sa.String(128), nullable=False),
        sa.Column("terminal_state_version", sa.Integer(), nullable=False),
        sa.Column(
            "admission_sequence", sa.BigInteger(), sa.Identity(start=1), nullable=False, unique=True
        ),
        sa.Column("payload", JSONB, nullable=False),
        sa.Column("admitted_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_admitted_cycles_project_id", "admitted_cycles", ["project_id"])
    op.create_index("ix_admitted_cycles_work_run_id", "admitted_cycles", ["work_run_id"])
    _history_table(
        "cycle_authority_events",
        sa.Column("event_sequence", sa.BigInteger(), sa.Identity(start=1), primary_key=True),
        sa.Column("event_id", sa.String(128), nullable=False, unique=True),
        sa.Column(
            "cycle_id",
            sa.String(128),
            sa.ForeignKey("admitted_cycles.cycle_id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("event_kind", sa.String(40), nullable=False),
        sa.Column("payload", JSONB, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    _history_table(
        "memory_declaration_policies",
        sa.Column("serialized_ref", sa.String(288), primary_key=True),
        sa.Column("fingerprint", sa.String(64), nullable=False),
        sa.Column("authority_revision", sa.BigInteger(), nullable=False),
        sa.Column("payload", JSONB, nullable=False),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
    )
    _history_table(
        "memory_policy_authority_events",
        sa.Column("event_sequence", sa.BigInteger(), sa.Identity(start=1), primary_key=True),
        sa.Column("event_id", sa.String(128), nullable=False, unique=True),
        sa.Column("policy_ref", sa.String(288), nullable=False),
        sa.Column("event_kind", sa.String(40), nullable=False),
        sa.Column("replacement_ref", sa.String(288), nullable=False, server_default="NONE"),
        sa.Column("payload", JSONB, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_memory_policy_authority_events_policy_ref",
        "memory_policy_authority_events",
        ["policy_ref"],
    )
    _history_table(
        "project_memory_entries",
        sa.Column("entry_id", sa.String(64), primary_key=True),
        sa.Column("memory_lineage_key", sa.String(64), nullable=False),
        sa.Column("project_id", sa.String(128), nullable=False),
        sa.Column(
            "cycle_id",
            sa.String(128),
            sa.ForeignKey("admitted_cycles.cycle_id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("declaration_ordinal", sa.Integer(), nullable=False),
        sa.Column("category", sa.String(40), nullable=False),
        sa.Column("content_fingerprint", sa.String(64), nullable=False),
        sa.Column("policy_ref", sa.String(288), nullable=False),
        sa.Column("policy_fingerprint", sa.String(64), nullable=False),
        sa.Column("source_ref", sa.String(512), nullable=False),
        sa.Column("privacy", sa.String(32), nullable=False),
        sa.Column("payload", JSONB, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        constraints=(
            sa.UniqueConstraint(
                "cycle_id",
                "declaration_ordinal",
                name="uq_project_memory_entry_cycle_ordinal",
            ),
            sa.CheckConstraint(
                "category IN ('DECISION','INVARIANT_POINTER','CONSTRAINT_POINTER',"
                "'BLOCKER_RESOLUTION','PROVENANCE_POINTER','NEXT_ACTION_CONTEXT')",
                name="ck_project_memory_entries_category",
            ),
            sa.CheckConstraint(
                "privacy IN ('INTERNAL','PUBLIC_SANITIZED','NON_EXPORTABLE')",
                name="ck_project_memory_entries_privacy",
            ),
        ),
    )
    op.create_index(
        "ix_project_memory_entries_memory_lineage_key",
        "project_memory_entries",
        ["memory_lineage_key"],
    )
    op.create_index(
        "ix_project_memory_entries_project_id", "project_memory_entries", ["project_id"]
    )
    _history_table(
        "cycle_memory_references",
        sa.Column("reference_id", sa.String(64), primary_key=True),
        sa.Column(
            "cycle_id",
            sa.String(128),
            sa.ForeignKey("admitted_cycles.cycle_id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "entry_id",
            sa.String(64),
            sa.ForeignKey("project_memory_entries.entry_id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("declaration_ordinal", sa.Integer(), nullable=False),
        sa.Column("content_fingerprint", sa.String(64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        constraints=sa.UniqueConstraint(
            "cycle_id",
            "declaration_ordinal",
            name="uq_cycle_memory_reference_cycle_ordinal",
        ),
    )
    _history_table(
        "project_memory_authority_events",
        sa.Column("event_sequence", sa.BigInteger(), sa.Identity(start=1), primary_key=True),
        sa.Column("event_id", sa.String(128), nullable=False, unique=True),
        sa.Column("memory_lineage_key", sa.String(64), nullable=False),
        sa.Column("subject_entry_id", sa.String(64), nullable=False),
        sa.Column("replacement_entry_id", sa.String(64), nullable=False, server_default="NONE"),
        sa.Column("event_kind", sa.String(40), nullable=False),
        sa.Column("prior_revision", sa.BigInteger(), nullable=False),
        sa.Column("new_revision", sa.BigInteger(), nullable=False),
        sa.Column("authority_ref", sa.String(512), nullable=False),
        sa.Column("reason", sa.String(96), nullable=False),
        sa.Column("payload", JSONB, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        constraints=(
            sa.CheckConstraint(
                "event_kind IN ('CURRENT','SUPERSEDED','REVOKED','EXPIRED')",
                name="ck_project_memory_authority_events_kind",
            ),
            sa.CheckConstraint(
                "new_revision = prior_revision + 1",
                name="ck_project_memory_authority_events_revision",
            ),
        ),
    )
    op.create_index(
        "ix_project_memory_authority_events_memory_lineage_key",
        "project_memory_authority_events",
        ["memory_lineage_key"],
    )
    op.create_table(
        "project_memory_views",
        sa.Column("memory_lineage_key", sa.String(64), primary_key=True),
        sa.Column("project_id", sa.String(128), nullable=False),
        sa.Column("current_entry_id", sa.String(64), nullable=True),
        sa.Column("state", sa.String(32), nullable=False),
        sa.Column("reason", sa.String(96), nullable=False),
        sa.Column("authority_revision", sa.BigInteger(), nullable=False),
        sa.Column("latest_event_sequence", sa.BigInteger(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "state IN ('CURRENT','SUPERSEDED','REVOKED','EXPIRED')",
            name="ck_project_memory_views_state",
        ),
    )
    op.create_index("ix_project_memory_views_project_id", "project_memory_views", ["project_id"])

    _history_table(
        "next_action_descriptors",
        sa.Column("action_ref", sa.String(512), primary_key=True),
        sa.Column("descriptor_version", sa.String(80), nullable=False),
        sa.Column("fingerprint", sa.String(64), nullable=False),
        sa.Column("authority_revision", sa.BigInteger(), nullable=False),
        sa.Column("payload", JSONB, nullable=False),
        sa.Column("enrolled_at", sa.DateTime(timezone=True), nullable=False),
    )
    _history_table(
        "next_action_policies",
        sa.Column("policy_ref", sa.String(288), primary_key=True),
        sa.Column("policy_kind", sa.String(32), nullable=False),
        sa.Column("fingerprint", sa.String(64), nullable=False),
        sa.Column("authority_revision", sa.BigInteger(), nullable=False),
        sa.Column("payload", JSONB, nullable=False),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
        constraints=sa.CheckConstraint(
            "policy_kind IN ('ELIGIBILITY','SELECTION')",
            name="ck_next_action_policies_kind",
        ),
    )
    _history_table(
        "next_action_owner_events",
        sa.Column("event_sequence", sa.BigInteger(), sa.Identity(start=1), primary_key=True),
        sa.Column("event_id", sa.String(128), nullable=False, unique=True),
        sa.Column("subject_ref", sa.String(512), nullable=False),
        sa.Column("subject_kind", sa.String(32), nullable=False),
        sa.Column("event_kind", sa.String(40), nullable=False),
        sa.Column("replacement_ref", sa.String(512), nullable=False, server_default="NONE"),
        sa.Column("payload", JSONB, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_next_action_owner_events_subject_ref", "next_action_owner_events", ["subject_ref"]
    )
    _history_table(
        "next_action_proposals",
        sa.Column("proposal_id", sa.String(128), primary_key=True),
        sa.Column("fingerprint", sa.String(64), nullable=False),
        sa.Column("project_id", sa.String(128), nullable=False),
        sa.Column("action_ref", sa.String(512), nullable=False),
        sa.Column("payload", JSONB, nullable=False),
        sa.Column("proposed_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_next_action_proposals_project_id", "next_action_proposals", ["project_id"])
    _history_table(
        "next_action_evaluations",
        sa.Column("evaluation_id", sa.String(128), primary_key=True),
        sa.Column("project_id", sa.String(128), nullable=False),
        sa.Column("project_revision", sa.BigInteger(), nullable=False),
        sa.Column("fingerprint", sa.String(64), nullable=False),
        sa.Column("payload", JSONB, nullable=False),
        sa.Column("evaluated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_next_action_evaluations_project_id", "next_action_evaluations", ["project_id"]
    )
    _history_table(
        "next_action_selections",
        sa.Column("selection_id", sa.String(128), primary_key=True),
        sa.Column("serialized_ref", sa.String(288), nullable=False, unique=True),
        sa.Column("fingerprint", sa.String(64), nullable=False),
        sa.Column("project_id", sa.String(128), nullable=False),
        sa.Column("project_revision", sa.BigInteger(), nullable=False),
        sa.Column(
            "evaluation_id",
            sa.String(128),
            sa.ForeignKey("next_action_evaluations.evaluation_id", ondelete="RESTRICT"),
            nullable=False,
            unique=True,
        ),
        sa.Column("action_ref", sa.String(512), nullable=False),
        sa.Column("payload", JSONB, nullable=False),
        sa.Column("selected_at", sa.DateTime(timezone=True), nullable=False),
        constraints=sa.UniqueConstraint(
            "project_id",
            "project_revision",
            name="uq_next_action_selection_project_revision",
        ),
    )
    op.create_index(
        "ix_next_action_selections_project_id", "next_action_selections", ["project_id"]
    )
    _history_table(
        "next_action_authority_events",
        sa.Column("event_sequence", sa.BigInteger(), sa.Identity(start=1), primary_key=True),
        sa.Column("event_id", sa.String(128), nullable=False, unique=True),
        sa.Column("project_id", sa.String(128), nullable=False),
        sa.Column("selection_id", sa.String(128), nullable=False),
        sa.Column("event_kind", sa.String(40), nullable=False),
        sa.Column("prior_revision", sa.BigInteger(), nullable=False),
        sa.Column("new_revision", sa.BigInteger(), nullable=False),
        sa.Column("payload", JSONB, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        constraints=sa.CheckConstraint(
            "new_revision = prior_revision + 1",
            name="ck_next_action_authority_events_revision",
        ),
    )
    op.create_index(
        "ix_next_action_authority_events_project_id", "next_action_authority_events", ["project_id"]
    )
    op.create_table(
        "next_action_projections",
        sa.Column("project_id", sa.String(128), primary_key=True),
        sa.Column("selection_id", sa.String(128), nullable=False),
        sa.Column("project_revision", sa.BigInteger(), nullable=False),
        sa.Column("latest_event_sequence", sa.BigInteger(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    _history_table(
        "task_issuance_candidates",
        sa.Column("candidate_id", sa.String(128), primary_key=True),
        sa.Column(
            "selection_id",
            sa.String(128),
            sa.ForeignKey("next_action_selections.selection_id", ondelete="RESTRICT"),
            nullable=False,
            unique=True,
        ),
        sa.Column("issuance_owner", sa.String(160), nullable=False),
        sa.Column("payload", JSONB, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        constraints=sa.CheckConstraint(
            "issuance_owner = 'EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY'",
            name="ck_task_issuance_candidates_owner",
        ),
    )

    immutable = (
        "cycle_admission_requests",
        "cycle_evaluations",
        "cycle_admission_decisions",
        "admitted_cycles",
        "cycle_authority_events",
        "memory_declaration_policies",
        "memory_policy_authority_events",
        "project_memory_entries",
        "cycle_memory_references",
        "project_memory_authority_events",
        "next_action_descriptors",
        "next_action_policies",
        "next_action_owner_events",
        "next_action_proposals",
        "next_action_evaluations",
        "next_action_selections",
        "next_action_authority_events",
        "task_issuance_candidates",
    )
    for name in immutable:
        _immutability(name)


def downgrade() -> None:
    tables = (
        "task_issuance_candidates",
        "next_action_projections",
        "next_action_authority_events",
        "next_action_selections",
        "next_action_evaluations",
        "next_action_proposals",
        "next_action_owner_events",
        "next_action_policies",
        "next_action_descriptors",
        "project_memory_views",
        "project_memory_authority_events",
        "cycle_memory_references",
        "project_memory_entries",
        "memory_policy_authority_events",
        "memory_declaration_policies",
        "cycle_authority_events",
        "admitted_cycles",
        "cycle_admission_decisions",
        "cycle_evaluations",
        "cycle_admission_requests",
    )
    for name in tables:
        op.drop_table(name)
