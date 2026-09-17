"""Permit the frozen ingress campaign to be flood-limited before release bootstrap."""

from alembic import op

revision = "20260918_0023"
down_revision = "20260918_0022"
branch_labels = None
depends_on = None

ROLE = "aiscc_public_live_ingress"
FUNCTION = "ingress_flood_consume_retained(text,text,bytea)"
PREDECESSOR = "flood_consume_retained(text,text,bytea)"

DDL = r"""
CREATE FUNCTION public_live_api.ingress_flood_consume_retained(c text,v text,s bytea)
RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE
 maintained bigint; n timestamptz; b bigint; source_count bigint;
 campaign_count bigint; retry integer;
BEGIN
 IF c IS DISTINCT FROM 'public-live-v1' OR v IS DISTINCT FROM 'v1'
 OR octet_length(s) IS DISTINCT FROM 32 THEN
  RAISE EXCEPTION 'LIMIT_IDENTITY_INVALID';
 END IF;
 maintained:=public_live_api.maintain_limiter();
 n:=public_live_api.clock_lock(); b:=floor(extract(epoch FROM n)/60)::bigint;
 INSERT INTO public.public_live_shared_limit VALUES(c,'CAMPAIGN',''::bytea,b,1)
 ON CONFLICT(campaign_id,kind,identity,bucket) DO UPDATE
 SET attempts=public_live_shared_limit.attempts+1
 RETURNING attempts INTO campaign_count;
 IF campaign_count<=1200 THEN
  INSERT INTO public.public_live_shared_limit VALUES(c,'SOURCE',s,b,1)
  ON CONFLICT(campaign_id,kind,identity,bucket) DO UPDATE
  SET attempts=public_live_shared_limit.attempts+1
  RETURNING attempts INTO source_count;
 ELSE
  source_count:=0;
 END IF;
 retry:=greatest(1,least(60,ceil((b+1)*60-extract(epoch FROM n))::integer));
 IF b IS DISTINCT FROM maintained THEN
  PERFORM public_live_api.maintain_limiter();
 END IF;
 RETURN jsonb_build_object(
  'allowed',source_count BETWEEN 1 AND 120 AND campaign_count<=1200,
  'retry_after',retry,'bucket',b,'now',n);
END $$;
"""


def upgrade() -> None:
    op.execute(DDL)
    op.execute(f"REVOKE ALL ON FUNCTION public_live_api.{FUNCTION} FROM PUBLIC")
    op.execute(f"GRANT EXECUTE ON FUNCTION public_live_api.{FUNCTION} TO {ROLE}")
    op.execute(f"REVOKE EXECUTE ON FUNCTION public_live_api.{PREDECESSOR} FROM {ROLE}")


def downgrade() -> None:
    op.execute(f"GRANT EXECUTE ON FUNCTION public_live_api.{PREDECESSOR} TO {ROLE}")
    op.execute(f"REVOKE EXECUTE ON FUNCTION public_live_api.{FUNCTION} FROM {ROLE}")
    op.execute(f"DROP FUNCTION public_live_api.{FUNCTION}")
