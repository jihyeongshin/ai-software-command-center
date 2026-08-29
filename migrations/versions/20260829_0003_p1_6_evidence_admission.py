"""Create P1-6 evidence admission authority tables.

Revision ID: 20260829_0003
Revises: 20260828_0002
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260829_0003"
down_revision: str | None = "20260828_0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    jsonb = postgresql.JSONB(astext_type=sa.Text())
    op.create_table(
        "evidence_requirement_sets",
        sa.Column("requirement_set_ref", sa.String(224), primary_key=True),
        sa.Column("requirement_set_id", sa.String(144), nullable=False),
        sa.Column("requirement_set_version", sa.String(80), nullable=False),
        sa.Column("task_contract_id", sa.String(160), nullable=False),
        sa.Column("task_contract_version", sa.String(80), nullable=False),
        sa.Column("requirement_root_hash", sa.String(64), nullable=False),
        sa.Column("fingerprint", sa.String(64), nullable=False),
        sa.Column("payload", jsonb, nullable=False),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "evidence_requirements",
        sa.Column("requirement_ref", sa.String(224), primary_key=True),
        sa.Column(
            "requirement_set_ref",
            sa.String(224),
            sa.ForeignKey("evidence_requirement_sets.requirement_set_ref", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("profile", sa.String(48), nullable=False),
        sa.Column("obligation", sa.String(32), nullable=False),
        sa.Column("fingerprint", sa.String(64), nullable=False),
        sa.Column("payload", jsonb, nullable=False),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_evidence_requirements_requirement_set_ref",
        "evidence_requirements",
        ["requirement_set_ref"],
    )
    op.create_table(
        "evidence_checkpoints",
        sa.Column("checkpoint_ref", sa.String(224), primary_key=True),
        sa.Column(
            "requirement_set_ref",
            sa.String(224),
            sa.ForeignKey("evidence_requirement_sets.requirement_set_ref", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("task_contract_id", sa.String(160), nullable=False),
        sa.Column("task_contract_version", sa.String(80), nullable=False),
        sa.Column("source_state", sa.String(40), nullable=False),
        sa.Column("target_state", sa.String(40)),
        sa.Column("transition_purpose_id", sa.String(128)),
        sa.Column("transition_purpose_version", sa.String(80)),
        sa.Column("fingerprint", sa.String(64), nullable=False),
        sa.Column("payload", jsonb, nullable=False),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "(target_state IS NOT NULL) <> "
            "(transition_purpose_id IS NOT NULL AND "
            "transition_purpose_version IS NOT NULL)",
            name="ck_evidence_checkpoint_exact_use",
        ),
    )
    op.create_index(
        "ix_evidence_checkpoints_requirement_set_ref",
        "evidence_checkpoints",
        ["requirement_set_ref"],
    )
    op.create_table(
        "human_direct_evidence_ingress",
        sa.Column("ingress_record_id", sa.String(128), primary_key=True),
        sa.Column("ingress_record_version", sa.String(80), nullable=False),
        sa.Column("serialized_ref", sa.String(512), nullable=False, unique=True),
        sa.Column("fingerprint", sa.String(64), nullable=False),
        sa.Column("ingress_authority_id", sa.String(160), nullable=False),
        sa.Column("ingress_authority_version", sa.String(80), nullable=False),
        sa.Column("authenticated_principal_id", sa.String(160), nullable=False),
        sa.Column("authenticated_session_id", sa.String(160), nullable=False),
        sa.Column("task_contract_id", sa.String(160), nullable=False),
        sa.Column("task_contract_version", sa.String(80), nullable=False),
        sa.Column("work_run_id", sa.String(128), nullable=False),
        sa.Column("checkpoint_ref", sa.String(224), nullable=False),
        sa.Column("evidence_type_id", sa.String(160), nullable=False),
        sa.Column("evidence_type_version", sa.String(80), nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("payload", jsonb, nullable=False),
        sa.Column("provided_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_human_direct_evidence_ingress_work_run_id",
        "human_direct_evidence_ingress",
        ["work_run_id"],
    )
    op.create_table(
        "evidence_candidates",
        sa.Column("candidate_id", sa.String(128), primary_key=True),
        sa.Column("candidate_version", sa.String(80), nullable=False),
        sa.Column("candidate_fingerprint", sa.String(64), nullable=False),
        sa.Column("task_contract_id", sa.String(160), nullable=False),
        sa.Column("task_contract_version", sa.String(80), nullable=False),
        sa.Column("checkpoint_ref", sa.String(224), nullable=False),
        sa.Column("issuer_type", sa.String(64), nullable=False),
        sa.Column("sensitivity", sa.String(40), nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column(
            "human_ingress_record_ref",
            sa.String(512),
            sa.ForeignKey("human_direct_evidence_ingress.serialized_ref", ondelete="RESTRICT"),
        ),
        sa.Column("payload", jsonb, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "evidence_admission_requests",
        sa.Column("admission_request_id", sa.String(128), primary_key=True),
        sa.Column("request_fingerprint", sa.String(64), nullable=False),
        sa.Column(
            "candidate_id",
            sa.String(128),
            sa.ForeignKey("evidence_candidates.candidate_id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("requirement_ref", sa.String(224), nullable=False),
        sa.Column("requirement_set_ref", sa.String(224), nullable=False),
        sa.Column("work_run_id", sa.String(128), nullable=False),
        sa.Column("checkpoint_ref", sa.String(224), nullable=False),
        sa.Column("observed_state", sa.String(40), nullable=False),
        sa.Column("observed_state_version", sa.Integer(), nullable=False),
        sa.Column("payload", jsonb, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_evidence_admission_requests_work_run_id", "evidence_admission_requests", ["work_run_id"]
    )
    op.create_table(
        "evidence_evaluations",
        sa.Column("evaluation_id", sa.String(128), primary_key=True),
        sa.Column(
            "admission_request_id",
            sa.String(128),
            sa.ForeignKey("evidence_admission_requests.admission_request_id", ondelete="RESTRICT"),
            nullable=False,
            unique=True,
        ),
        sa.Column("dimension_results", jsonb, nullable=False),
        sa.Column("authority_version", sa.String(80), nullable=False),
        sa.Column("evaluated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "evidence_admission_decisions",
        sa.Column("decision_id", sa.String(128), primary_key=True),
        sa.Column(
            "event_sequence", sa.BigInteger(), sa.Identity(start=1), nullable=False, unique=True
        ),
        sa.Column(
            "admission_request_id",
            sa.String(128),
            sa.ForeignKey("evidence_admission_requests.admission_request_id", ondelete="RESTRICT"),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "evaluation_id",
            sa.String(128),
            sa.ForeignKey("evidence_evaluations.evaluation_id", ondelete="RESTRICT"),
            nullable=False,
            unique=True,
        ),
        sa.Column("outcome", sa.String(24), nullable=False),
        sa.Column("reason", sa.String(64), nullable=False),
        sa.Column("secondary_reasons", jsonb, nullable=False),
        sa.Column("admitting_authority_version", sa.String(80), nullable=False),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "admitted_evidence",
        sa.Column("admitted_evidence_id", sa.String(128), primary_key=True),
        sa.Column(
            "decision_id",
            sa.String(128),
            sa.ForeignKey("evidence_admission_decisions.decision_id", ondelete="RESTRICT"),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "candidate_id",
            sa.String(128),
            sa.ForeignKey("evidence_candidates.candidate_id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("requirement_ref", sa.String(224), nullable=False),
        sa.Column(
            "work_run_id",
            sa.String(128),
            sa.ForeignKey("work_runs.work_run_id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("checkpoint_ref", sa.String(224), nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("coverage", jsonb, nullable=False),
        sa.Column("payload", jsonb, nullable=False),
        sa.Column("admitted_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "candidate_id",
            "requirement_ref",
            "work_run_id",
            "checkpoint_ref",
            name="uq_admitted_evidence_logical_mapping",
        ),
    )
    op.create_index("ix_admitted_evidence_work_run_id", "admitted_evidence", ["work_run_id"])
    op.create_table(
        "evidence_requirement_satisfactions",
        sa.Column("satisfaction_id", sa.String(128), primary_key=True),
        sa.Column(
            "admitted_evidence_id",
            sa.String(128),
            sa.ForeignKey("admitted_evidence.admitted_evidence_id", ondelete="RESTRICT"),
            nullable=False,
            unique=True,
        ),
        sa.Column("requirement_ref", sa.String(224), nullable=False),
        sa.Column("work_run_id", sa.String(128), nullable=False),
        sa.Column("checkpoint_ref", sa.String(224), nullable=False),
        sa.Column("coverage", jsonb, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_evidence_requirement_satisfactions_work_run_id",
        "evidence_requirement_satisfactions",
        ["work_run_id"],
    )
    op.create_table(
        "evidence_reuse_consumptions",
        sa.Column("consumption_id", sa.String(128), primary_key=True),
        sa.Column("prior_admitted_evidence_ref", sa.String(288), nullable=False),
        sa.Column(
            "admitted_evidence_id",
            sa.String(128),
            sa.ForeignKey("admitted_evidence.admitted_evidence_id", ondelete="RESTRICT"),
            nullable=False,
            unique=True,
        ),
        sa.Column("requirement_ref", sa.String(224), nullable=False),
        sa.Column("work_run_id", sa.String(128), nullable=False),
        sa.Column("checkpoint_ref", sa.String(224), nullable=False),
        sa.Column("policy_maximum", sa.Integer(), nullable=False),
        sa.Column("consumption_ordinal", sa.Integer(), nullable=False),
        sa.Column("consumed_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "prior_admitted_evidence_ref",
            "requirement_ref",
            "work_run_id",
            "checkpoint_ref",
            "consumption_ordinal",
            name="uq_evidence_reuse_scope_ordinal",
        ),
    )
    op.create_index(
        "ix_evidence_reuse_consumptions_prior_admitted_evidence_ref",
        "evidence_reuse_consumptions",
        ["prior_admitted_evidence_ref"],
    )
    op.create_table(
        "evidence_set_evaluations",
        sa.Column("evaluation_id", sa.String(128), primary_key=True),
        sa.Column("evaluation_version", sa.String(80), nullable=False),
        sa.Column("work_run_id", sa.String(128), nullable=False),
        sa.Column("source_state", sa.String(40), nullable=False),
        sa.Column("state_version", sa.Integer(), nullable=False),
        sa.Column("checkpoint_ref", sa.String(224), nullable=False),
        sa.Column("requirement_set_ref", sa.String(224), nullable=False),
        sa.Column("outcome", sa.String(24), nullable=False),
        sa.Column("full_requirement_root_hash", sa.String(64), nullable=False),
        sa.Column("checkpoint_subset_root_hash", sa.String(64), nullable=False),
        sa.Column("admitted_ref_root_hash", sa.String(64), nullable=False),
        sa.Column("evidence_authority_revision", sa.BigInteger(), nullable=False),
        sa.Column("payload", jsonb, nullable=False),
        sa.Column("evaluated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_evidence_set_evaluations_work_run_id", "evidence_set_evaluations", ["work_run_id"]
    )
    op.create_table(
        "evidence_set_attestations",
        sa.Column("attestation_id", sa.String(128), primary_key=True),
        sa.Column("attestation_version", sa.String(80), nullable=False),
        sa.Column("serialized_ref", sa.String(288), nullable=False, unique=True),
        sa.Column(
            "evidence_set_evaluation_id",
            sa.String(128),
            sa.ForeignKey("evidence_set_evaluations.evaluation_id", ondelete="RESTRICT"),
            nullable=False,
            unique=True,
        ),
        sa.Column("work_run_id", sa.String(128), nullable=False),
        sa.Column("checkpoint_ref", sa.String(224), nullable=False),
        sa.Column("state_version", sa.Integer(), nullable=False),
        sa.Column("evidence_authority_revision", sa.BigInteger(), nullable=False),
        sa.Column("payload", jsonb, nullable=False),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True)),
    )
    op.create_index(
        "ix_evidence_set_attestations_work_run_id", "evidence_set_attestations", ["work_run_id"]
    )
    op.create_table(
        "evidence_authority_events",
        sa.Column("event_sequence", sa.BigInteger(), sa.Identity(start=1), primary_key=True),
        sa.Column("event_id", sa.String(128), nullable=False, unique=True),
        sa.Column("subject_ref", sa.String(288), nullable=False),
        sa.Column("event_kind", sa.String(32), nullable=False),
        sa.Column("replacement_ref", sa.String(288), nullable=False, server_default="NONE"),
        sa.Column("reason", sa.String(128), nullable=False),
        sa.Column("owner_id", sa.String(160), nullable=False),
        sa.Column("authority_version", sa.String(80), nullable=False),
        sa.Column("task_contract_id", sa.String(160), nullable=False),
        sa.Column("task_contract_version", sa.String(80), nullable=False),
        sa.Column("work_run_id", sa.String(128)),
        sa.Column("affected_refs", jsonb, nullable=False),
        sa.Column("affected_mappings", jsonb, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "subject_ref", "event_kind", "replacement_ref", name="uq_evidence_event"
        ),
    )
    op.create_index(
        "ix_evidence_authority_events_subject_ref", "evidence_authority_events", ["subject_ref"]
    )
    op.create_index(
        "ix_evidence_authority_events_task_contract_id",
        "evidence_authority_events",
        ["task_contract_id"],
    )
    op.create_index(
        "ix_evidence_authority_events_work_run_id",
        "evidence_authority_events",
        ["work_run_id"],
    )
    op.execute("""
        CREATE FUNCTION aiscc_reject_evidence_history_mutation()
        RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN
          RAISE EXCEPTION 'AISCC evidence provenance is append-only';
        END; $$
    """)
    for table in (
        "evidence_requirement_sets",
        "evidence_requirements",
        "evidence_checkpoints",
        "human_direct_evidence_ingress",
        "evidence_candidates",
        "evidence_admission_requests",
        "evidence_evaluations",
        "evidence_admission_decisions",
        "admitted_evidence",
        "evidence_requirement_satisfactions",
        "evidence_reuse_consumptions",
        "evidence_set_evaluations",
        "evidence_set_attestations",
        "evidence_authority_events",
    ):
        op.execute(
            f"CREATE TRIGGER {table}_append_only BEFORE UPDATE OR DELETE ON {table} "
            "FOR EACH ROW EXECUTE FUNCTION aiscc_reject_evidence_history_mutation()"
        )


def downgrade() -> None:
    tables = (
        "evidence_authority_events",
        "evidence_set_attestations",
        "evidence_set_evaluations",
        "evidence_requirement_satisfactions",
        "evidence_reuse_consumptions",
        "admitted_evidence",
        "evidence_admission_decisions",
        "evidence_evaluations",
        "evidence_admission_requests",
        "evidence_candidates",
        "human_direct_evidence_ingress",
        "evidence_checkpoints",
        "evidence_requirements",
        "evidence_requirement_sets",
    )
    for table in tables:
        op.execute(f"DROP TRIGGER IF EXISTS {table}_append_only ON {table}")
        op.drop_table(table)
    op.execute("DROP FUNCTION IF EXISTS aiscc_reject_evidence_history_mutation()")
