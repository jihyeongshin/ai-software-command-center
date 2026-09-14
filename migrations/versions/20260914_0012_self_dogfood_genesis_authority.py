"""Add immutable one-time self-dogfood genesis authority, without Cycle backfill."""

import sqlalchemy as sa
from alembic import op

revision = "20260914_0012"
down_revision = "20260914_0011"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "self_dogfood_genesis_authority",
        sa.Column("record_id", sa.String(160), primary_key=True),
        sa.Column("project_id", sa.String(96), nullable=False),
        sa.Column("record_kind", sa.String(16), nullable=False),
        sa.Column("canonical_body", sa.LargeBinary(), nullable=False),
        sa.Column("fingerprint", sa.String(64), nullable=False),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("project_id", "record_kind", name="uq_genesis_project_kind"),
        sa.CheckConstraint("record_kind IN ('ISSUED','TASK_BOUND')", name="ck_genesis_record_kind"),
        sa.CheckConstraint("fingerprint ~ '^[0-9a-f]{64}$'", name="ck_genesis_fingerprint"),
        sa.CheckConstraint(
            "octet_length(canonical_body) BETWEEN 1 AND 16384", name="ck_genesis_body_size"
        ),
    )
    op.execute("""CREATE FUNCTION aiscc_genesis_immutable() RETURNS trigger
        LANGUAGE plpgsql AS $$ BEGIN
        RAISE EXCEPTION 'AISCC Genesis authority is append-only'; END $$""")
    op.execute("""CREATE TRIGGER genesis_no_update_delete BEFORE UPDATE OR DELETE
        ON self_dogfood_genesis_authority FOR EACH ROW
        EXECUTE FUNCTION aiscc_genesis_immutable()""")
    op.execute("""CREATE TRIGGER genesis_no_truncate BEFORE TRUNCATE
        ON self_dogfood_genesis_authority FOR EACH STATEMENT
        EXECUTE FUNCTION aiscc_genesis_immutable()""")


def downgrade():
    if op.get_bind().scalar(
        sa.text("SELECT EXISTS (SELECT 1 FROM self_dogfood_genesis_authority)")
    ):
        raise RuntimeError("GENESIS_NONEMPTY_DOWNGRADE_FORBIDDEN")
    op.drop_table("self_dogfood_genesis_authority")
    op.execute("DROP FUNCTION aiscc_genesis_immutable()")
