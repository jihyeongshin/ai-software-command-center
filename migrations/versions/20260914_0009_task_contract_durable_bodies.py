"""Add the external Task owner's immutable complete contract bodies.

Revision ID: 20260914_0009
Revises: 20260901_0008
"""

import sqlalchemy as sa
from alembic import op

revision = "20260914_0009"
down_revision = "20260901_0008"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "task_contract_bodies",
        sa.Column("body_ref", sa.String(93), primary_key=True),
        sa.Column("body_schema_id", sa.String(64), nullable=False),
        sa.Column("body_sha256", sa.String(64), nullable=False),
        sa.Column("project_id", sa.String(96), nullable=False),
        sa.Column("contract_id", sa.String(96), nullable=False),
        sa.Column("task_id", sa.String(96), nullable=False),
        sa.Column("contract_version", sa.BigInteger(), nullable=False),
        sa.Column("canonical_body", sa.LargeBinary(), nullable=False),
        sa.Column(
            "constraint_ref",
            sa.String(),
            sa.ForeignKey("task_constraint_refs.constraint_ref"),
            nullable=False,
        ),
        sa.Column(
            "issuance_event_ref",
            sa.String(),
            sa.ForeignKey("task_constraint_authority_events.event_ref"),
            nullable=False,
        ),
        sa.Column("predecessor_version", sa.BigInteger()),
        sa.Column("predecessor_sha256", sa.String(64)),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "project_id", "contract_id", "contract_version", name="uq_task_contract_body_version"
        ),
        sa.UniqueConstraint("constraint_ref", name="uq_task_contract_body_constraint"),
        sa.UniqueConstraint("issuance_event_ref", name="uq_task_contract_body_event"),
        sa.CheckConstraint(
            "contract_version BETWEEN 1 AND 9007199254740991", name="ck_task_contract_version"
        ),
        sa.CheckConstraint(
            "octet_length(canonical_body) BETWEEN 1 AND 1048576", name="ck_task_contract_body_size"
        ),
        sa.CheckConstraint("body_sha256 ~ '^[0-9a-f]{64}$'", name="ck_task_contract_body_hash"),
        sa.CheckConstraint(
            "body_ref ~ '^task-contract-body:v1:sha256:[0-9a-f]{64}$'",
            name="ck_task_contract_body_ref",
        ),
        sa.CheckConstraint(
            "body_schema_id = 'AISCC-TASKCONTRACT-BODY-V1'", name="ck_task_contract_body_schema"
        ),
        sa.CheckConstraint(
            "(contract_version = 1 AND predecessor_version IS NULL "
            "AND predecessor_sha256 IS NULL) OR (contract_version > 1 "
            "AND predecessor_version IS NOT NULL AND predecessor_sha256 IS NOT NULL "
            "AND predecessor_version = contract_version - 1 "
            "AND predecessor_sha256 ~ '^[0-9a-f]{64}$')",
            name="ck_task_contract_predecessor",
        ),
    )
    op.execute("""CREATE FUNCTION aiscc_task_contract_body_immutable() RETURNS trigger
        LANGUAGE plpgsql AS $$ BEGIN
        RAISE EXCEPTION 'AISCC TaskContract bodies are append-only'; END $$""")
    op.execute("""CREATE TRIGGER task_contract_body_no_update_delete
        BEFORE UPDATE OR DELETE
        ON task_contract_bodies FOR EACH ROW
        EXECUTE FUNCTION aiscc_task_contract_body_immutable()""")
    op.execute("""CREATE TRIGGER task_contract_body_no_truncate BEFORE TRUNCATE
        ON task_contract_bodies FOR EACH STATEMENT
        EXECUTE FUNCTION aiscc_task_contract_body_immutable()""")


def downgrade():
    if op.get_bind().scalar(sa.text("SELECT EXISTS (SELECT 1 FROM task_contract_bodies)")):
        raise RuntimeError("TASKCONTRACT_NONEMPTY_DOWNGRADE_FORBIDDEN")
    op.drop_table("task_contract_bodies")
    op.execute("DROP FUNCTION aiscc_task_contract_body_immutable()")
