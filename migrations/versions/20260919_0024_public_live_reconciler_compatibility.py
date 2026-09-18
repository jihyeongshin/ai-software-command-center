"""Grant the reconciler its exact compatibility API dependencies."""

from alembic import op

revision = "20260919_0024"
down_revision = "20260918_0023"
branch_labels = None
depends_on = None

ROLE = "aiscc_public_live_reconciler"
FUNCTIONS = (
    "run_context(bytea)",
    "project_run(bytea,bigint,text,bytea)",
)


def upgrade() -> None:
    for signature in FUNCTIONS:
        op.execute(f"REVOKE ALL ON FUNCTION public_live_api.{signature} FROM PUBLIC")
        op.execute(f"GRANT EXECUTE ON FUNCTION public_live_api.{signature} TO {ROLE}")


def downgrade() -> None:
    for signature in reversed(FUNCTIONS):
        op.execute(f"REVOKE EXECUTE ON FUNCTION public_live_api.{signature} FROM {ROLE}")
