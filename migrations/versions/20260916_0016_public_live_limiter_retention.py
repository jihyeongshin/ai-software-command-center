"""Bound Public Live limiter retention; preserve accepted rate/owner semantics."""

from alembic import op

revision = "20260916_0016"
down_revision = "20260916_0015"
branch_labels = None
depends_on = None

ORIGINAL_FLOOD = r"""
CREATE OR REPLACE FUNCTION public_live_api.flood_consume(c text,v text,s bytea) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE n timestamptz; b bigint; source_count bigint; campaign_count bigint; retry integer;
BEGIN
 n:=public_live_api.clock_lock(); b:=floor(extract(epoch FROM n)/60)::bigint;
 IF octet_length(s) IS DISTINCT FROM 32 OR c IS NULL OR v IS NULL OR NOT EXISTS(
 SELECT 1 FROM public.public_campaign WHERE campaign_id=c AND hmac_version=v)
 THEN RAISE EXCEPTION 'LIMIT_IDENTITY_INVALID'; END IF;
 INSERT INTO public.public_live_shared_limit VALUES(c,'CAMPAIGN',''::bytea,b,1)
 ON CONFLICT(campaign_id,kind,identity,bucket) DO UPDATE
 SET attempts=public_live_shared_limit.attempts+1
 RETURNING attempts INTO campaign_count;
 INSERT INTO public.public_live_shared_limit VALUES(c,'SOURCE',s,b,1)
 ON CONFLICT(campaign_id,kind,identity,bucket) DO UPDATE
 SET attempts=public_live_shared_limit.attempts+1
 RETURNING attempts INTO source_count;
 retry:=greatest(1,least(60,ceil((b+1)*60-extract(epoch FROM n))::integer));
 RETURN jsonb_build_object('allowed',source_count<=120 AND campaign_count<=1200,
 'retry_after',retry,'bucket',b,'now',n);
END $$;
"""


MAINTENANCE = r"""
CREATE INDEX public_live_shared_limit_bucket_idx ON public.public_live_shared_limit(bucket);
-- statement
CREATE TABLE public.public_live_limiter_maintenance (
 id smallint PRIMARY KEY CHECK(id=1),
 last_bucket bigint CHECK(last_bucket>=0)
);
-- statement
INSERT INTO public.public_live_limiter_maintenance VALUES(1,NULL);
-- statement
CREATE FUNCTION public_live_api.maintain_limiter() RETURNS bigint
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE n timestamptz; b bigint; previous bigint;
BEGIN
 n:=public_live_api.clock_lock(); b:=floor(extract(epoch FROM n)/60)::bigint;
 SELECT last_bucket INTO previous FROM public.public_live_limiter_maintenance
 WHERE id=1 FOR UPDATE;
 IF NOT FOUND OR previous>b THEN RAISE EXCEPTION 'LIMIT_MAINTENANCE_UNSAFE'; END IF;
 IF previous IS NULL OR previous<b THEN
  DELETE FROM public.public_live_shared_limit WHERE bucket<b-9;
  UPDATE public.public_live_limiter_maintenance SET last_bucket=b WHERE id=1;
 END IF;
 RETURN b;
END $$;
"""

SHORT_CIRCUIT = r"""
 IF campaign_count>1200 THEN
  retry:=greatest(1,least(60,ceil((b+1)*60-extract(epoch FROM n))::integer));
  RETURN jsonb_build_object('allowed',false,'retry_after',retry,'bucket',b,'now',n);
 END IF;
"""


def upgrade():
    for statement in MAINTENANCE.split("-- statement"):
        op.execute(statement)
    op.execute(
        ORIGINAL_FLOOD.replace(
            " INSERT INTO public.public_live_shared_limit VALUES(c,'SOURCE',s,b,1)",
            SHORT_CIRCUIT + " INSERT INTO public.public_live_shared_limit VALUES(c,'SOURCE',s,b,1)",
        )
    )
    for name, declaration, arguments, signature in (
        ("flood_consume", "c text,v text,s bytea", "c,v,s", "text,text,bytea"),
        ("read_consume", "r bytea", "r", "bytea"),
    ):
        op.execute(f"""
CREATE FUNCTION public_live_api.{name}_retained({declaration}) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE maintained bigint; result jsonb;
BEGIN
 maintained:=public_live_api.maintain_limiter();
 result:=public_live_api.{name}({arguments});
 IF (result->>'bucket')::bigint IS DISTINCT FROM maintained THEN
  PERFORM public_live_api.maintain_limiter();
 END IF;
 RETURN result;
END $$;
""")
        op.execute(
            f"REVOKE ALL ON FUNCTION public_live_api.{name}_retained({signature}) FROM PUBLIC"
        )
        op.execute(
            f"GRANT EXECUTE ON FUNCTION public_live_api.{name}_retained({signature}) "
            "TO aiscc_public_live_runtime"
        )
        op.execute(
            f"REVOKE EXECUTE ON FUNCTION public_live_api.{name}({signature}) "
            "FROM aiscc_public_live_runtime"
        )
    op.execute("REVOKE ALL ON FUNCTION public_live_api.maintain_limiter() FROM PUBLIC")
    op.execute(
        "REVOKE ALL ON public.public_live_limiter_maintenance "
        "FROM PUBLIC,aiscc_public_live_runtime,aiscc_public_live_reconciler"
    )


def downgrade():
    if (
        op.get_bind()
        .exec_driver_sql(
            "SELECT (SELECT enabled FROM public.public_control) OR "
            "EXISTS(SELECT 1 FROM public.public_live_shared_limit)"
        )
        .scalar()
    ):
        raise RuntimeError("PUBLIC_LIMITER_RETENTION_IN_USE")
    for signature in ("flood_consume_retained(text,text,bytea)", "read_consume_retained(bytea)"):
        op.execute(f"DROP FUNCTION public_live_api.{signature}")
    op.execute(ORIGINAL_FLOOD)
    for signature in ("flood_consume(text,text,bytea)", "read_consume(bytea)"):
        op.execute(
            f"GRANT EXECUTE ON FUNCTION public_live_api.{signature} TO aiscc_public_live_runtime"
        )
    op.execute("DROP FUNCTION public_live_api.maintain_limiter()")
    op.execute("DROP TABLE public.public_live_limiter_maintenance")
    op.execute("DROP INDEX public.public_live_shared_limit_bucket_idx")
