"""Add P1-6 durable structured evidence content without rewriting legacy identities.

Revision ID: 20260830_0005
Revises: 20260829_0004
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260830_0005"
down_revision: str | None = "20260829_0004"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

V1 = "P1_6_EVIDENCE_REQUIREMENT_FINGERPRINT_V1"
V2 = "P1_6_EVIDENCE_REQUIREMENT_FINGERPRINT_V2_DURABLE_CONTENT"


def upgrade() -> None:
    # This physical selector chooses the historical algorithm. It is deliberately not
    # inserted into or used to recompute any legacy JSON payload, fingerprint, or root.
    op.add_column(
        "evidence_requirements",
        sa.Column("fingerprint_schema", sa.String(96), nullable=True),
    )
    op.execute(
        sa.text(
            "UPDATE evidence_requirements SET fingerprint_schema = :schema "
            "WHERE fingerprint_schema IS NULL"
        ).bindparams(schema=V1)
    )
    op.alter_column("evidence_requirements", "fingerprint_schema", nullable=False)
    op.create_check_constraint(
        "ck_evidence_requirements_fingerprint_schema",
        "evidence_requirements",
        f"fingerprint_schema IN ('{V1}','{V2}')",
    )
    op.create_check_constraint(
        "ck_evidence_requirements_schema_payload_cut",
        "evidence_requirements",
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
    )

    op.create_table(
        "evidence_content_objects",
        sa.Column("serialized_ref", sa.String(96), primary_key=True),
        sa.Column("content_identity_key", sa.String(64), nullable=False, unique=True),
        sa.Column("owner_id", sa.String(160), nullable=False),
        sa.Column("owner_version", sa.String(80), nullable=False),
        sa.Column("source_owner_authority_ref", sa.String(320), nullable=False),
        sa.Column("source_owner_authority_fingerprint", sa.String(64), nullable=False),
        sa.Column("object_id", sa.String(160), nullable=False),
        sa.Column("object_version", sa.String(80), nullable=False),
        sa.Column("content_kind", sa.String(64), nullable=False),
        sa.Column("canonicalization", sa.String(80), nullable=False),
        sa.Column("schema_id", sa.String(160), nullable=False),
        sa.Column("schema_version", sa.String(80), nullable=False),
        sa.Column("byte_count", sa.Integer(), nullable=False),
        sa.Column("content_hash_algorithm", sa.String(16), nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("sensitivity", sa.String(40), nullable=False),
        sa.Column("retention_policy", sa.String(96), nullable=False),
        sa.Column("access_policy", sa.String(64), nullable=False),
        sa.Column("canonical_body", sa.LargeBinary(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("content_authority_id", sa.String(160), nullable=False),
        sa.Column("content_authority_version", sa.String(80), nullable=False),
        sa.Column("content_authority_revision", sa.Integer(), nullable=False),
        sa.Column("payload_fingerprint_schema", sa.String(80), nullable=False),
        sa.Column("payload_fingerprint", sa.String(64), nullable=False),
        sa.CheckConstraint(
            "byte_count >= 1 AND byte_count <= 65536",
            name="ck_evidence_content_objects_byte_count",
        ),
        sa.CheckConstraint(
            "octet_length(canonical_body) = byte_count",
            name="ck_evidence_content_objects_body_length",
        ),
        sa.CheckConstraint(
            "content_kind IN ('INLINE_CANONICAL_STRUCTURED_BODY',"
            "'DATABASE_OBSERVATION_REF','RUNTIME_OBSERVATION_REF')",
            name="ck_evidence_content_objects_kind",
        ),
        sa.CheckConstraint(
            "sensitivity IN ('PUBLIC_SAFE','INTERNAL')",
            name="ck_evidence_content_objects_sensitivity",
        ),
        sa.UniqueConstraint(
            "owner_id",
            "owner_version",
            "object_id",
            "object_version",
            name="uq_evidence_content_object_identity",
        ),
    )
    op.create_index(
        "ix_evidence_content_objects_schema",
        "evidence_content_objects",
        ["schema_id", "schema_version"],
    )
    op.create_index(
        "ix_evidence_content_objects_content_hash",
        "evidence_content_objects",
        ["content_hash"],
    )

    op.create_table(
        "evidence_candidate_content_bindings",
        sa.Column(
            "candidate_id",
            sa.String(128),
            sa.ForeignKey("evidence_candidates.candidate_id", ondelete="RESTRICT"),
            primary_key=True,
        ),
        sa.Column("candidate_version", sa.String(80), nullable=False),
        sa.Column("candidate_fingerprint", sa.String(64), nullable=False),
        sa.Column(
            "durable_content_ref",
            sa.String(96),
            sa.ForeignKey("evidence_content_objects.serialized_ref", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("durable_content_payload_fingerprint", sa.String(64), nullable=False),
        sa.Column("content_ref_metadata_fingerprint", sa.String(64), nullable=False),
        sa.Column("requirement_ref", sa.String(224), nullable=False),
        sa.Column("requirement_fingerprint_schema", sa.String(96), nullable=False),
        sa.Column("requirement_fingerprint", sa.String(64), nullable=False),
        sa.Column("requirement_set_ref", sa.String(224), nullable=False),
        sa.Column("requirement_root_hash", sa.String(64), nullable=False),
        sa.Column("durable_content_policy_ref", sa.String(320), nullable=False),
        sa.Column("durable_content_policy_fingerprint", sa.String(64), nullable=False),
        sa.Column("binding_fingerprint", sa.String(64), nullable=False),
        sa.Column("bound_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_evidence_candidate_content_bindings_content_ref",
        "evidence_candidate_content_bindings",
        ["durable_content_ref"],
    )

    for table in ("evidence_content_objects", "evidence_candidate_content_bindings"):
        op.execute(
            f"CREATE TRIGGER {table}_append_only BEFORE UPDATE OR DELETE ON {table} "
            "FOR EACH ROW EXECUTE FUNCTION aiscc_reject_evidence_history_mutation()"
        )
        op.execute(f"REVOKE INSERT, UPDATE, DELETE ON {table} FROM PUBLIC")


def downgrade() -> None:
    for table in ("evidence_candidate_content_bindings", "evidence_content_objects"):
        op.execute(f"DROP TRIGGER IF EXISTS {table}_append_only ON {table}")
    op.drop_index(
        "ix_evidence_candidate_content_bindings_content_ref",
        table_name="evidence_candidate_content_bindings",
    )
    op.drop_table("evidence_candidate_content_bindings")
    op.drop_index("ix_evidence_content_objects_content_hash", table_name="evidence_content_objects")
    op.drop_index("ix_evidence_content_objects_schema", table_name="evidence_content_objects")
    op.drop_table("evidence_content_objects")
    op.drop_constraint(
        "ck_evidence_requirements_schema_payload_cut",
        "evidence_requirements",
        type_="check",
    )
    op.drop_constraint(
        "ck_evidence_requirements_fingerprint_schema",
        "evidence_requirements",
        type_="check",
    )
    op.drop_column("evidence_requirements", "fingerprint_schema")
