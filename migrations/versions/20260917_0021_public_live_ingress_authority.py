"""Add the narrow Public Live ingress database capability."""

from alembic import op

revision = "20260917_0021"
down_revision = "20260917_0020"
branch_labels = None
depends_on = None

ROLE = "aiscc_public_live_ingress"
FUNCTIONS = (
    "clock_lock()",
    "flood_consume(text,text,bytea)",
    "lock_run(bytea)",
    "read_consume(bytea)",
    "read_key(text,bytea)",
    "admission_context(text,bytea)",
    "admit_checked_and_start(jsonb,jsonb)",
    "run_context(bytea)",
)
PUBLIC_INTERNAL_FUNCTIONS = (
    "bump_start_gate()",
    "initializer_shape_guard()",
    "start_immutable()",
    "start_json(public.public_start_request)",
)


def upgrade() -> None:
    op.execute(
        f"""
        DO $$
        BEGIN
          IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='{ROLE}') THEN
            CREATE ROLE {ROLE}
              NOLOGIN NOINHERIT NOSUPERUSER NOCREATEDB NOCREATEROLE NOBYPASSRLS;
          ELSIF EXISTS (
            SELECT 1 FROM pg_roles
            WHERE rolname='{ROLE}' AND (
              rolcanlogin OR rolinherit OR rolsuper OR rolcreatedb OR rolcreaterole OR rolbypassrls
            )
          ) THEN
            RAISE EXCEPTION 'PUBLIC_LIVE_INGRESS_ROLE_INVALID';
          END IF;
        END $$
        """
    )
    op.execute(f"REVOKE ALL ON SCHEMA public_live_api FROM {ROLE}")
    op.execute(f"REVOKE ALL ON ALL TABLES IN SCHEMA public,public_live_api FROM {ROLE}")
    op.execute(f"REVOKE ALL ON ALL SEQUENCES IN SCHEMA public,public_live_api FROM {ROLE}")
    op.execute(f"REVOKE ALL ON ALL FUNCTIONS IN SCHEMA public_live_api FROM {ROLE}")
    for signature in PUBLIC_INTERNAL_FUNCTIONS:
        op.execute(f"REVOKE EXECUTE ON FUNCTION public_live_api.{signature} FROM PUBLIC")
    op.execute(f"GRANT USAGE ON SCHEMA public_live_api TO {ROLE}")
    for signature in FUNCTIONS:
        op.execute(f"GRANT EXECUTE ON FUNCTION public_live_api.{signature} TO {ROLE}")


def downgrade() -> None:
    op.execute(
        f"""
        DO $$
        BEGIN
          IF EXISTS (
            SELECT 1 FROM pg_auth_members m
            JOIN pg_roles parent ON parent.oid=m.roleid
            WHERE parent.rolname='{ROLE}'
          ) THEN
            RAISE EXCEPTION 'PUBLIC_LIVE_INGRESS_ROLE_HAS_MEMBERS';
          END IF;
        END $$
        """
    )
    for signature in FUNCTIONS:
        op.execute(f"REVOKE EXECUTE ON FUNCTION public_live_api.{signature} FROM {ROLE}")
    op.execute(f"REVOKE USAGE ON SCHEMA public_live_api FROM {ROLE}")
    op.execute(f"DROP ROLE {ROLE}")
    for signature in PUBLIC_INTERNAL_FUNCTIONS:
        op.execute(f"GRANT EXECUTE ON FUNCTION public_live_api.{signature} TO PUBLIC")
