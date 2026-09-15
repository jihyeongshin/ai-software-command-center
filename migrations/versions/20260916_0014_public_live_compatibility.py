"""Mediated L1/L2 compatibility; no table, column, index or role changes."""

from alembic import op

revision = "20260916_0014"
down_revision = "20260915_0013"
branch_labels = None
depends_on = None

DDL = r"""
CREATE FUNCTION public_live_api.admission_context(c text,b bytea) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE n timestamptz; p public.public_campaign; ctl public.public_control;
 d date; day_count integer; day_available bigint; hour_count bigint; client_count bigint;
 slot integer;
BEGIN
 n:=public_live_api.clock_lock(); d:=(n AT TIME ZONE 'UTC')::date;
 SELECT * INTO ctl FROM public.public_control WHERE id=1;
 SELECT * INTO p FROM public.public_campaign WHERE campaign_id=c FOR UPDATE;
 IF NOT FOUND THEN RETURN NULL; END IF;
 PERFORM 1 FROM public.public_day WHERE campaign_id=c AND utc_date=d FOR UPDATE;
 PERFORM 1 FROM public.public_client WHERE campaign_id=c AND bucket_hash=b FOR UPDATE;
 PERFORM 1 FROM public.public_slot ORDER BY slot_id FOR UPDATE;
 SELECT admitted_count,available INTO day_count,day_available FROM public.public_day
 WHERE campaign_id=c AND utc_date=d;
 SELECT count(*) FILTER(WHERE admitted_at>n-interval '1 hour' AND admitted_at<=n),
 count(*) FILTER(WHERE utc_date=d) INTO hour_count,client_count
 FROM public.public_rate_event WHERE campaign_id=c AND bucket_hash=b;
 SELECT slot_id INTO slot FROM public.public_slot WHERE state='FREE' ORDER BY slot_id LIMIT 1;
 RETURN jsonb_build_object('now',n,'campaign_id',c,'enabled',ctl.enabled AND ctl.incident IS NULL
 AND ctl.active_campaign=c AND ctl.policy_digest=p.policy_digest,'starts_at',p.starts_at,
 'ends_at',p.ends_at,'policy_digest',encode(p.policy_digest,'hex'),
 'content_digest',encode(p.content_digest,'hex'),'scenario_id',p.scenario_id,
 'scenario_version',p.scenario_version,'hmac_version',p.hmac_version,
 'day_count',coalesce(day_count,0),'hour_count',hour_count,'client_day_count',client_count,
 'day_available',coalesce(day_available,4000000),'campaign_available',p.available,'slot_id',slot);
END $$;
-- statement
CREATE FUNCTION public_live_api.admit_checked(p jsonb) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE ctx jsonb; key_value jsonb; c text:=p->>'campaign_id';
 b bytea:=decode(p->>'bucket_hash','hex'); k bytea:=decode(p->>'key_hash','hex'); n timestamptz;
BEGIN
 n:=public_live_api.clock_lock(); key_value:=public_live_api.read_key(c,k);
 IF key_value IS NOT NULL THEN
  IF decode(substr(key_value->>'bucket_hash',3),'hex')<>b THEN
   RETURN jsonb_build_object('error','CLIENT_BINDING_DENIED'); END IF;
  IF decode(substr(key_value->>'payload_hash',3),'hex')<>decode(p->>'payload_digest','hex') THEN
   RETURN jsonb_build_object('error','IDEMPOTENCY_CONFLICT'); END IF;
  IF n >= (key_value->>'replay_until')::timestamptz THEN
   RETURN jsonb_build_object('error','IDEMPOTENCY_EXPIRED'); END IF;
  RETURN jsonb_build_object('replayed',true,'run_id',substr(key_value->>'run_id',3));
 END IF;
 ctx:=public_live_api.admission_context(c,b);
 IF ctx IS NULL THEN RETURN jsonb_build_object('error','POLICY_UNAVAILABLE'); END IF;
 IF p->>'policy_digest' IS DISTINCT FROM ctx->>'policy_digest'
 OR p->>'content_digest' IS DISTINCT FROM ctx->>'content_digest'
 OR p->>'hmac_version' IS DISTINCT FROM ctx->>'hmac_version'
 OR ctx->>'scenario_id'<>'stockroom-s1-normal' OR ctx->>'scenario_version'<>'1.0.0'
 OR (ctx->>'ends_at')::timestamptz>'2026-10-17T15:00:00Z'::timestamptz
 THEN RETURN jsonb_build_object('error','POLICY_UNAVAILABLE'); END IF;
 IF NOT (ctx->>'enabled')::boolean THEN RETURN jsonb_build_object('error','LIVE_DISABLED'); END IF;
 IF n<(ctx->>'starts_at')::timestamptz OR n>=(ctx->>'ends_at')::timestamptz
 OR n>='2026-10-17T15:00:00Z'::timestamptz THEN
  RETURN jsonb_build_object('error','CAMPAIGN_CLOSED'); END IF;
 IF (ctx->>'hour_count')::bigint>=3 OR (ctx->>'client_day_count')::bigint>=10 THEN
  RETURN jsonb_build_object('error','CLIENT_RATE_LIMIT'); END IF;
 IF (ctx->>'day_count')::integer>=20 THEN RETURN
 jsonb_build_object('error','GLOBAL_DAY_LIMIT'); END IF;
 IF ctx->>'slot_id' IS NULL THEN RETURN jsonb_build_object('error','CAPACITY_UNAVAILABLE'); END IF;
 IF (ctx->>'day_available')::bigint<200000 OR (ctx->>'campaign_available')::bigint<200000 THEN
  RETURN jsonb_build_object('error','BUDGET_UNAVAILABLE'); END IF;
 PERFORM public_live_api.persist_run(p || jsonb_build_object('slot_id',(ctx->>'slot_id')::integer));
 RETURN jsonb_build_object('replayed',false,'run_id',p->>'run_id');
END $$;
-- statement
CREATE FUNCTION public_live_api.run_context(r bytea) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE v public.public_run; result jsonb;
BEGIN
 v:=public_live_api.lock_run(r);
 SELECT jsonb_build_object('run_id',encode(r,'hex'),'state',v.state,'version',v.version,
 'admitted_at',v.admitted_at,'deadline',v.deadline,'read_expires',v.read_expires,
 'owner_binding',v.owner_binding,'outbox',public_live_api.read_outbox(r),
 'slot',(SELECT jsonb_build_object('state',state,'generation',generation,'expires_at',expires_at)
 FROM public.public_slot WHERE run_id=r),
 'dispatches',coalesce((SELECT jsonb_agg(jsonb_build_object('ordinal',ordinal,'state',state,
 'max_cost',max_cost,'cost',provisional_cost,'proof',encode(usage_evidence_digest,'hex'),
 'usage_missing',EXISTS(SELECT 1 FROM public.public_observation o WHERE o.run_id=r
 AND o.ordinal=public_dispatch.ordinal AND o.classification='USAGE' AND o.cost_micro IS NULL)) ORDER
 BY ordinal)
 FROM public.public_dispatch WHERE run_id=r),'[]'::jsonb),
 'settlement',(SELECT jsonb_build_object('cost',cost,'proof',encode(evidence_digest,'hex'))
 FROM public.public_money_event WHERE run_id=r AND event_kind='SETTLE')) INTO result;
 RETURN result;
END $$;
-- statement
CREATE FUNCTION public_live_api.project_run(r bytea,expected bigint,target text,proof bytea)
RETURNS bigint LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE v public.public_run; identity bytea; prior public.public_observation;
 n timestamptz; markers bigint; closed boolean; allowed boolean:=false;
BEGIN
 v:=public_live_api.lock_run(r); n:=public_live_api.clock_lock();
 IF expected<1 OR octet_length(proof) IS DISTINCT FROM 32 OR target IS NULL THEN
  RAISE EXCEPTION 'PROJECTION_REQUEST_INVALID'; END IF;
 identity:=sha256(r || convert_to('public-projection-v1:'||expected::text||':'||target,'UTF8')
 || proof);
 SELECT * INTO prior FROM public.public_observation WHERE source_identity=identity;
 IF FOUND THEN
  IF v.state=target AND v.version=expected+1 THEN RETURN v.version; END IF;
  RAISE EXCEPTION 'PROJECTION_REPLAY_CONFLICT';
 END IF;
 IF v.version<>expected THEN RAISE EXCEPTION 'PROJECTION_STALE_VERSION'; END IF;
 IF v.state IN ('COMPLETED','FAILED_NOT_DISPATCHED','FAILED_PROVIDER',
 'FAILED_TIMEOUT','FAILED_SAFETY')
 THEN RAISE EXCEPTION 'PROJECTION_TERMINAL'; END IF;
 SELECT count(*) INTO markers FROM public.public_dispatch WHERE run_id=r;
 closed:=EXISTS(SELECT 1 FROM public.public_money_event WHERE run_id=r AND event_kind='SETTLE'
 AND evidence_digest=proof);
 IF target='UNKNOWN_OUTCOME' AND v.state='DISPATCH_STARTED' AND EXISTS(
 SELECT 1 FROM public.public_dispatch WHERE run_id=r AND state IN ('STARTED','UNKNOWN')) THEN
  allowed:=true;
  UPDATE public.public_slot SET state='SUSPECT' WHERE run_id=r;
 ELSIF target='GOVERNANCE_PENDING' AND v.state='DISPATCH_STARTED' AND v.owner_binding IS NOT NULL
 AND EXISTS(SELECT 1 FROM public.work_runs WHERE work_run_id=v.owner_binding
 AND runtime_mode='PUBLIC_BOUNDED_LIVE') AND EXISTS(SELECT 1 FROM public.public_dispatch
 WHERE run_id=r AND state='KNOWN_SUCCESS' AND usage_evidence_digest=proof) THEN allowed:=true;
 ELSIF target='FAILED_NOT_DISPATCHED' AND v.state='ADMITTED' AND markers=0 AND closed
 AND EXISTS(SELECT 1 FROM public.public_money_event WHERE run_id=r AND event_kind='SETTLE' AND
 cost=0)
 THEN allowed:=true;
 ELSIF target='FAILED_PROVIDER' AND v.state='DISPATCH_STARTED' AND markers>0 AND closed
 AND NOT EXISTS(SELECT 1 FROM public.public_dispatch WHERE run_id=r AND state<>'KNOWN_FAILURE')
 THEN allowed:=true;
 ELSIF target='FAILED_TIMEOUT' AND v.state IN
 ('DISPATCH_STARTED','GOVERNANCE_PENDING','UNKNOWN_OUTCOME')
 AND n>=v.deadline AND closed THEN allowed:=true;
 ELSIF target='COMPLETED' AND v.state='GOVERNANCE_PENDING' AND closed AND EXISTS(
 SELECT 1 FROM public.work_runs WHERE work_run_id=v.owner_binding AND
 runtime_mode='PUBLIC_BOUNDED_LIVE'
 AND workflow_state IN ('ACCEPTED','REJECTED','FAILED')) THEN allowed:=true;
 ELSIF target='FAILED_SAFETY' AND EXISTS(SELECT 1 FROM public.public_observation
 WHERE run_id=r AND classification='ABOVE_BOUND' AND evidence_digest=proof)
 AND EXISTS(SELECT 1 FROM public.public_control WHERE NOT enabled AND incident='ABOVE_BOUND_USAGE')
 THEN allowed:=true;
 END IF;
 IF NOT allowed THEN RAISE EXCEPTION 'PROJECTION_PREDICATE_DENIED'; END IF;
 INSERT INTO public.public_observation VALUES(substring(identity from 1 for 16),r,NULL,identity,
 'USAGE',proof,n,NULL);
 UPDATE public.public_run SET state=target,version=version+1 WHERE run_id=r AND version=expected;
 IF NOT FOUND THEN RAISE EXCEPTION 'PROJECTION_STALE_VERSION'; END IF;
 RETURN expected+1;
END $$;
-- statement
CREATE FUNCTION public_live_api.mark_checked(r bytea,g bigint,n integer,bound
 bigint,owner_version bigint)
RETURNS void LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE v public.public_run;
BEGIN
 v:=public_live_api.lock_run(r);
 IF v.state NOT IN ('ADMITTED','DISPATCH_STARTED') OR NOT EXISTS(
 SELECT 1 FROM public.work_runs WHERE work_run_id=v.owner_binding
 AND runtime_mode='PUBLIC_BOUNDED_LIVE' AND workflow_state='RUNNING'
 AND state_version=owner_version) THEN RAISE EXCEPTION 'PUBLIC_OWNER_NOT_RUNNING'; END IF;
 PERFORM public_live_api.mark_dispatch(r,g,n,bound);
END $$;
"""

FUNCTIONS = (
    "admission_context(text,bytea)",
    "admit_checked(jsonb)",
    "run_context(bytea)",
    "project_run(bytea,bigint,text,bytea)",
    "mark_checked(bytea,bigint,integer,bigint,bigint)",
)


def upgrade():
    for statement in DDL.split("-- statement"):
        op.execute(statement)
    for signature in FUNCTIONS:
        op.execute(f"REVOKE ALL ON FUNCTION public_live_api.{signature} FROM PUBLIC")
        op.execute(
            f"GRANT EXECUTE ON FUNCTION public_live_api.{signature} TO aiscc_public_live_runtime"
        )


def downgrade():
    # A live deployment must drain under separate authorization before removing API.
    if op.get_bind().exec_driver_sql("SELECT EXISTS(SELECT 1 FROM public.public_run)").scalar():
        raise RuntimeError("PUBLIC_LIVE_COMPATIBILITY_IN_USE")
    for signature in reversed(FUNCTIONS):
        op.execute(f"DROP FUNCTION IF EXISTS public_live_api.{signature}")
