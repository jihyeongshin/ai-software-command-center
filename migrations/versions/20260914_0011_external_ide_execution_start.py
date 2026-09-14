"""Append-only external IDE start authority, separate from completion."""

import sqlalchemy as sa
from alembic import op

revision = "20260914_0011"
down_revision = "20260914_0010"
branch_labels = None
depends_on = None
TABLES = ("external_ide_execution_start_permits", "external_ide_execution_starts")


def upgrade():
    for table in TABLES:
        permit = table == TABLES[0]
        columns = [
            sa.Column(
                "permit_id" if permit else "start_id",
                sa.String(128 if permit else 160),
                primary_key=True,
            ),
            sa.Column(
                "work_run_id",
                sa.String(128),
                sa.ForeignKey("work_runs.work_run_id"),
                nullable=False,
                unique=True,
            ),
            sa.Column("producer_kind", sa.String(64), nullable=False),
            sa.Column("canonical_body", sa.LargeBinary(), nullable=False),
            sa.Column("body_sha256", sa.String(64), nullable=False),
            sa.CheckConstraint("producer_kind = 'LOCAL_IDE_SELF_DOGFOOD_V1'"),
            sa.CheckConstraint("body_sha256 ~ '^[0-9a-f]{64}$'"),
            sa.CheckConstraint("octet_length(canonical_body) BETWEEN 1 AND 1048576"),
        ]
        if not permit:
            columns.extend(
                [
                    sa.Column(
                        "permit_id",
                        sa.String(128),
                        sa.ForeignKey(TABLES[0] + ".permit_id"),
                        nullable=False,
                        unique=True,
                    ),
                    sa.Column(
                        "transition_request_id",
                        sa.String(128),
                        sa.ForeignKey("transition_requests.transition_request_id"),
                        nullable=False,
                        unique=True,
                    ),
                ]
            )
        op.create_table(table, *columns)
    op.execute("""CREATE FUNCTION aiscc_external_ide_start_immutable() RETURNS trigger
        LANGUAGE plpgsql AS $$ BEGIN
        RAISE EXCEPTION 'AISCC external IDE start authority is append-only'; END $$""")
    for table in TABLES:
        op.execute(f"""CREATE TRIGGER {table}_immutable BEFORE UPDATE OR DELETE ON {table}
            FOR EACH ROW EXECUTE FUNCTION aiscc_external_ide_start_immutable()""")
        op.execute(f"""CREATE TRIGGER {table}_no_truncate BEFORE TRUNCATE ON {table}
            FOR EACH STATEMENT EXECUTE FUNCTION aiscc_external_ide_start_immutable()""")


def downgrade():
    if any(op.get_bind().scalar(sa.text(f"SELECT EXISTS (SELECT 1 FROM {t})")) for t in TABLES):
        raise RuntimeError("EXTERNAL_IDE_START_NONEMPTY_DOWNGRADE_FORBIDDEN")
    for table in reversed(TABLES):
        op.drop_table(table)
    op.execute("DROP FUNCTION aiscc_external_ide_start_immutable()")
