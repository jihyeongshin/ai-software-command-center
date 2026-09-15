"""Public Live V1 shared HTTP limits; existing schema and authority unchanged."""

from alembic import op

revision = "20260916_0015"
down_revision = "20260916_0014"
branch_labels = None
depends_on = None

DDL = r"""
CREATE TABLE public.public_live_shared_limit (
 campaign_id text NOT NULL CHECK(length(campaign_id) BETWEEN 1 AND 200),
 kind text NOT NULL CHECK(kind IN ('SOURCE','CAMPAIGN','READ')),
 identity bytea NOT NULL,
 bucket bigint NOT NULL CHECK(bucket>=0),
 attempts bigint NOT NULL CHECK(attempts>=1),
 PRIMARY KEY(campaign_id,kind,identity,bucket),
 CHECK((kind='SOURCE' AND octet_length(identity)=32) OR
 (kind='CAMPAIGN' AND octet_length(identity)=0) OR
 (kind='READ' AND octet_length(identity)=16))
);
-- statement
CREATE FUNCTION public_live_api.flood_consume(c text,v text,s bytea) RETURNS jsonb
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
-- statement
CREATE FUNCTION public_live_api.read_consume(r bytea) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE v public.public_run; n timestamptz; b bigint; count_value bigint; retry integer;
BEGIN
 v:=public_live_api.lock_run(r); n:=public_live_api.clock_lock();
 IF n>=v.read_expires THEN RAISE EXCEPTION 'READ_EXPIRED'; END IF;
 b:=floor(extract(epoch FROM n)/60)::bigint;
 INSERT INTO public.public_live_shared_limit VALUES(v.campaign_id,'READ',r,b,1)
 ON CONFLICT(campaign_id,kind,identity,bucket) DO UPDATE
 SET attempts=public_live_shared_limit.attempts+1
 RETURNING attempts INTO count_value;
 retry:=greatest(1,least(60,ceil((b+1)*60-extract(epoch FROM n))::integer));
 RETURN jsonb_build_object('allowed',count_value<=30,'retry_after',retry,'bucket',b,'now',n);
END $$;
"""


def upgrade():
    for statement in DDL.split("-- statement"):
        op.execute(statement)
    op.execute(
        "REVOKE ALL ON public.public_live_shared_limit "
        "FROM PUBLIC, aiscc_public_live_runtime, aiscc_public_live_reconciler"
    )
    for signature in ("flood_consume(text,text,bytea)", "read_consume(bytea)"):
        op.execute(f"REVOKE ALL ON FUNCTION public_live_api.{signature} FROM PUBLIC")
        op.execute(
            f"GRANT EXECUTE ON FUNCTION public_live_api.{signature} TO aiscc_public_live_runtime"
        )


def downgrade():
    # No automatic live quota reset: separate draining authorization is required.
    if (
        op.get_bind()
        .exec_driver_sql("SELECT EXISTS(SELECT 1 FROM public.public_live_shared_limit)")
        .scalar()
    ):
        raise RuntimeError("PUBLIC_SHARED_LIMIT_IN_USE")
    op.execute("DROP FUNCTION public_live_api.read_consume(bytea)")
    op.execute("DROP FUNCTION public_live_api.flood_consume(text,text,bytea)")
    op.execute("DROP TABLE public.public_live_shared_limit")
