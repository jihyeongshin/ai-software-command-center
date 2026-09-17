"""Align Public Live ingress with retained limiter wrappers."""

from alembic import op

revision = "20260918_0022"
down_revision = "20260917_0021"
branch_labels = None
depends_on = None

ROLE = "aiscc_public_live_ingress"
RETAINED_FUNCTIONS = (
    "flood_consume_retained(text,text,bytea)",
    "read_consume_retained(bytea)",
)
NON_RETAINED_FUNCTIONS = (
    "flood_consume(text,text,bytea)",
    "read_consume(bytea)",
)


def upgrade() -> None:
    for signature in RETAINED_FUNCTIONS:
        op.execute(f"GRANT EXECUTE ON FUNCTION public_live_api.{signature} TO {ROLE}")
    for signature in NON_RETAINED_FUNCTIONS:
        op.execute(f"REVOKE EXECUTE ON FUNCTION public_live_api.{signature} FROM {ROLE}")


def downgrade() -> None:
    for signature in NON_RETAINED_FUNCTIONS:
        op.execute(f"GRANT EXECUTE ON FUNCTION public_live_api.{signature} TO {ROLE}")
    for signature in RETAINED_FUNCTIONS:
        op.execute(f"REVOKE EXECUTE ON FUNCTION public_live_api.{signature} FROM {ROLE}")
