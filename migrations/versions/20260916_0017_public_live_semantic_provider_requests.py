"""Versioned Luna semantic requests; preserve legacy dispatch and money authority."""

from alembic import op

revision = "20260916_0017"
down_revision = "20260916_0016"
branch_labels = None
depends_on = None

SQL = r"""
-- statement
ALTER TABLE public.public_dispatch DROP CONSTRAINT public_dispatch_ordinal_check;
-- statement
ALTER TABLE public.public_dispatch ADD CONSTRAINT public_dispatch_ordinal_check CHECK(ordinal
 BETWEEN 1 AND 4);
-- statement
CREATE TABLE public.public_provider_pipeline (
 run_id bytea PRIMARY KEY REFERENCES public.public_run ON DELETE RESTRICT,
 profile text NOT NULL CHECK(profile='public-live-luna-v1'),
 price_verified timestamptz NOT NULL,
 price_reference text NOT NULL DEFAULT
 'https://developers.openai.com/api/docs/models/gpt-5.6-luna',
 completed boolean NOT NULL DEFAULT false,
 tool_claimed boolean NOT NULL DEFAULT false
);
-- statement
CREATE TABLE public.public_provider_request (
 run_id bytea NOT NULL REFERENCES public.public_provider_pipeline ON DELETE RESTRICT,
 ordinal integer NOT NULL CHECK(ordinal BETWEEN 1 AND 4),
 semantic_ordinal integer NOT NULL CHECK(semantic_ordinal BETWEEN 1 AND 3),
 role text NOT NULL CHECK(role IN ('PRIMARY','VERIFY','CORRECT')),
 effort text NOT NULL CHECK((role='CORRECT' AND effort='medium') OR (role<>'CORRECT' AND
 effort='low')),
 retry_of integer,
 fingerprint bytea NOT NULL CHECK(octet_length(fingerprint)=32),
 trigger_ref bytea CHECK(octet_length(trigger_ref)=32),
 defect text,
 provider text NOT NULL DEFAULT 'openai' CHECK(provider='openai'),
 model text NOT NULL DEFAULT 'gpt-5.6-luna' CHECK(model='gpt-5.6-luna'),
 profile_version integer NOT NULL DEFAULT 1 CHECK(profile_version=1),
 input_bound integer NOT NULL CHECK(input_bound BETWEEN 1 AND 8000),
 output_bound integer NOT NULL DEFAULT 2000 CHECK(output_bound=2000),
 max_cost bigint NOT NULL DEFAULT 4400 CHECK(max_cost=4400),
 connect_seconds integer NOT NULL DEFAULT 5 CHECK(connect_seconds=5),
 read_seconds integer NOT NULL DEFAULT 30 CHECK(read_seconds=30),
 wall_seconds integer NOT NULL DEFAULT 35 CHECK(wall_seconds=35),
 authorized_at timestamptz NOT NULL,
 sent_at timestamptz,
 outcome_at timestamptz,
 deadline timestamptz NOT NULL,
 outcome text NOT NULL DEFAULT 'STARTED' CHECK(outcome IN
 ('STARTED','KNOWN_SUCCESS','KNOWN_FAILURE','UNKNOWN')),
 closed_failure boolean NOT NULL DEFAULT false,
 output_tokens integer CHECK(output_tokens BETWEEN 0 AND 2000),
 usage_missing boolean NOT NULL DEFAULT true,
 recorded_cost bigint,
 response_ref bytea CHECK(octet_length(response_ref)=32),
 PRIMARY KEY(run_id,ordinal), UNIQUE(run_id,fingerprint),
 FOREIGN KEY(run_id,ordinal) REFERENCES public.public_dispatch ON DELETE RESTRICT,
 FOREIGN KEY(run_id,retry_of) REFERENCES public.public_provider_request ON DELETE RESTRICT,
 CHECK(retry_of IS NULL OR retry_of<ordinal)
);
-- statement
CREATE UNIQUE INDEX public_provider_one_retry ON public.public_provider_request(run_id) WHERE
 retry_of IS NOT NULL;
-- statement
CREATE UNIQUE INDEX public_provider_one_role ON public.public_provider_request(run_id,role) WHERE
 retry_of IS NULL;
-- statement
CREATE TABLE public.public_provider_validation (
 run_id bytea NOT NULL, ordinal integer NOT NULL,
 decision text NOT NULL CHECK(decision IN
 ('COMPLETE','VERIFY_REQUIRED','CORRECTABLE_DEFECT','UNSAFE_OR_UNCORRECTABLE')),
 proof bytea NOT NULL CHECK(octet_length(proof)=32),
 defect text CHECK(defect IN ('SUMMARY_MISMATCH','MISSING_REQUIRED_FACT')),
 created_at timestamptz NOT NULL,
 PRIMARY KEY(run_id,ordinal),
 FOREIGN KEY(run_id,ordinal) REFERENCES public.public_provider_request ON DELETE RESTRICT,
 CHECK((decision='CORRECTABLE_DEFECT')=(defect IS NOT NULL))
);
-- statement
ALTER FUNCTION public_live_api.mark_dispatch(bytea,bigint,integer,bigint) RENAME TO
 mark_dispatch_legacy;
-- statement
ALTER FUNCTION public_live_api.project_run(bytea,bigint,text,bytea) RENAME TO project_run_legacy;
-- statement
ALTER FUNCTION public_live_api.mark_checked(bytea,bigint,integer,bigint,bigint)
 RENAME TO mark_checked_legacy;
-- statement
CREATE FUNCTION public_live_api.mark_checked(r bytea,g bigint,n integer,bound bigint,v bigint)
RETURNS void LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
BEGIN
 PERFORM public_live_api.lock_run(r);
 IF EXISTS(SELECT 1 FROM public.public_provider_pipeline WHERE run_id=r) OR n NOT IN (1,2)
 THEN RAISE EXCEPTION 'SEMANTIC_DISPATCH_REQUIRED'; END IF;
 PERFORM public_live_api.mark_checked_legacy(r,g,n,bound,v);
END $$;
-- statement
CREATE FUNCTION public_live_api.mark_dispatch(r bytea,g bigint,n integer,bound bigint) RETURNS
 void
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
BEGIN
 PERFORM public_live_api.lock_run(r);
 IF EXISTS(SELECT 1 FROM public.public_provider_pipeline WHERE run_id=r) OR n NOT IN (1,2)
 THEN RAISE EXCEPTION 'SEMANTIC_DISPATCH_REQUIRED'; END IF;
 PERFORM public_live_api.mark_dispatch_legacy(r,g,n,bound);
END $$;
-- statement
CREATE FUNCTION public_live_api.project_run(r bytea,expected bigint,target text,proof bytea)
 RETURNS bigint
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
BEGIN
 PERFORM public_live_api.lock_run(r);
 IF target='GOVERNANCE_PENDING' AND EXISTS(SELECT 1 FROM public.public_provider_pipeline
 WHERE run_id=r AND NOT completed) THEN RAISE EXCEPTION 'PIPELINE_NOT_COMPLETE'; END IF;
 RETURN public_live_api.project_run_legacy(r,expected,target,proof);
END $$;
-- statement
CREATE FUNCTION public_live_api.pipeline_enroll(r bytea,verified timestamptz) RETURNS void
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE v public.public_run; n timestamptz;
BEGIN
 v:=public_live_api.lock_run(r); n:=public_live_api.clock_lock();
 IF verified IS NULL OR verified>n OR verified<=n-interval '24 hours' THEN RAISE EXCEPTION
 'PRICE_STALE'; END IF;
 IF EXISTS(SELECT 1 FROM public.public_provider_pipeline WHERE run_id=r AND
 price_verified=verified) THEN RETURN; END IF;
 IF v.state<>'ADMITTED' OR EXISTS(SELECT 1 FROM public.public_dispatch WHERE run_id=r)
 OR NOT EXISTS(SELECT 1 FROM public.public_campaign WHERE campaign_id=v.campaign_id
 AND scenario_id='stockroom-s1-normal' AND scenario_version='1.0.0') THEN RAISE EXCEPTION
 'ENROLL_DENIED'; END IF;
 INSERT INTO public.public_provider_pipeline(run_id,profile,price_verified)
 VALUES(r,'public-live-luna-v1',verified);
END $$;
-- statement
CREATE FUNCTION public_live_api.pipeline_context(r bytea) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
BEGIN
 PERFORM public_live_api.lock_run(r);
 RETURN jsonb_build_object('owner_binding',(SELECT owner_binding FROM public.public_run WHERE
 run_id=r),
 'settlement',(SELECT to_jsonb(s)-'run_id' FROM public.public_reservation s WHERE run_id=r),
 'pipeline',(SELECT to_jsonb(p) - 'run_id' FROM public.public_provider_pipeline p WHERE run_id=r),
 'requests',coalesce((SELECT jsonb_agg(to_jsonb(q)-'run_id' ORDER BY ordinal) FROM
 public.public_provider_request q WHERE run_id=r),'[]'::jsonb),
 'validations',coalesce((SELECT jsonb_agg(to_jsonb(v)-'run_id' ORDER BY ordinal) FROM
 public.public_provider_validation v WHERE run_id=r),'[]'::jsonb));
END $$;
-- statement
CREATE FUNCTION public_live_api.pipeline_request(r bytea,fp bytea,inputs integer,owner_version
 bigint) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE v public.public_run; p public.public_provider_pipeline; prev
 public.public_provider_request;
 gate public.public_provider_validation; n timestamptz; physical integer; logical integer;
 role_name text;
 ancestor integer; trig bytea; defect_name text; generation_value bigint;
BEGIN
 v:=public_live_api.lock_run(r); n:=public_live_api.clock_lock();
 SELECT * INTO STRICT p FROM public.public_provider_pipeline WHERE run_id=r;
 IF EXISTS(SELECT 1 FROM public.public_provider_request WHERE run_id=r AND fingerprint=fp)
 THEN RETURN jsonb_build_object('send',false,'reason','ALREADY_AUTHORIZED'); END IF;
 IF p.completed OR p.price_verified>n OR p.price_verified<=n-interval '24 hours'
 OR n+interval '35 seconds'>v.deadline OR octet_length(fp) IS DISTINCT FROM 32
 OR inputs IS NULL OR inputs NOT BETWEEN 1 AND 8000 OR v.state NOT IN
 ('ADMITTED','DISPATCH_STARTED')
 OR NOT EXISTS(SELECT 1 FROM public.public_control WHERE enabled AND incident IS NULL)
 OR NOT EXISTS(SELECT 1 FROM public.work_runs WHERE work_run_id=v.owner_binding
 AND runtime_mode='PUBLIC_BOUNDED_LIVE' AND workflow_state='RUNNING' AND
 state_version=owner_version)
 THEN RAISE EXCEPTION 'PIPELINE_GATE_DENIED'; END IF;
 SELECT generation INTO STRICT generation_value FROM public.public_outbox WHERE run_id=r AND
 state='BOUND';
 IF NOT EXISTS(SELECT 1 FROM public.public_slot WHERE run_id=r AND generation=generation_value
 AND state='OCCUPIED' AND expires_at>n) THEN RAISE EXCEPTION 'SLOT_UNAVAILABLE'; END IF;
 SELECT * INTO prev FROM public.public_provider_request WHERE run_id=r ORDER BY ordinal DESC
 LIMIT 1;
 physical:=coalesce(prev.ordinal,0)+1;
 IF physical>4 THEN RAISE EXCEPTION 'REQUEST_LIMIT'; END IF;
 IF prev.ordinal IS NULL THEN role_name:='PRIMARY'; logical:=1;
 ELSIF prev.outcome='KNOWN_FAILURE' AND prev.closed_failure THEN
  IF EXISTS(SELECT 1 FROM public.public_provider_request WHERE run_id=r AND retry_of IS NOT NULL)
  OR inputs>prev.input_bound THEN RAISE EXCEPTION 'RETRY_LIMIT'; END IF;
  role_name:=prev.role; logical:=prev.semantic_ordinal; ancestor:=prev.ordinal;
  trig:=prev.trigger_ref; defect_name:=prev.defect;
 ELSIF prev.outcome='KNOWN_SUCCESS' THEN
  SELECT * INTO STRICT gate FROM public.public_provider_validation WHERE run_id=r AND
 ordinal=prev.ordinal;
  IF gate.decision='VERIFY_REQUIRED' AND prev.role='PRIMARY' THEN role_name:='VERIFY';
  ELSIF gate.decision='CORRECTABLE_DEFECT' AND prev.role IN ('PRIMARY','VERIFY') THEN
 role_name:='CORRECT';
  ELSE RAISE EXCEPTION 'NO_SEMANTIC_TRANSITION'; END IF;
  logical:=prev.semantic_ordinal+1; trig:=gate.proof; defect_name:=gate.defect;
 ELSE RAISE EXCEPTION 'UNCERTAIN_OR_CLOSED_REQUEST'; END IF;
 IF logical>3 THEN RAISE EXCEPTION 'SEMANTIC_LIMIT'; END IF;
 INSERT INTO public.public_dispatch VALUES(r,physical,generation_value,n,4400,'STARTED',NULL,0);
 INSERT INTO public.public_provider_request(run_id,ordinal,semantic_ordinal,role,effort,retry_of,
 fingerprint,trigger_ref,defect,input_bound,authorized_at,deadline)
 VALUES(r,physical,logical,role_name,CASE WHEN role_name='CORRECT' THEN 'medium' ELSE 'low' END,
 ancestor,fp,trig,defect_name,inputs,n,v.deadline);
 UPDATE public.public_reservation SET committed_max=committed_max+4400 WHERE run_id=r AND
 state='HELD';
 IF NOT FOUND THEN RAISE EXCEPTION 'RESERVATION_NOT_HELD'; END IF;
 UPDATE public.public_run SET state='DISPATCH_STARTED',version=version+1 WHERE run_id=r;
 RETURN (SELECT to_jsonb(q)-'run_id'||jsonb_build_object('send',true) FROM
 public.public_provider_request q WHERE run_id=r AND ordinal=physical);
END $$;
-- statement
CREATE FUNCTION public_live_api.pipeline_start(r bytea,o integer,fp bytea,owner_version bigint)
 RETURNS void
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE v public.public_run; n timestamptz;
BEGIN
 v:=public_live_api.lock_run(r); n:=public_live_api.clock_lock();
 IF v.state<>'DISPATCH_STARTED' OR n+interval '35 seconds'>v.deadline
 OR NOT EXISTS(SELECT 1 FROM public.public_reservation WHERE run_id=r AND state='HELD')
 OR NOT EXISTS(SELECT 1 FROM public.public_provider_pipeline WHERE run_id=r AND NOT completed
 AND price_verified<=n AND price_verified>n-interval '24 hours')
 OR NOT EXISTS(SELECT 1 FROM public.public_outbox b JOIN public.public_slot s
 ON s.run_id=b.run_id AND s.generation=b.generation WHERE b.run_id=r
 AND b.state='BOUND' AND s.state='OCCUPIED' AND s.expires_at>n)
 OR NOT EXISTS(SELECT 1 FROM public.public_control WHERE enabled AND incident IS NULL)
 OR NOT EXISTS(SELECT 1 FROM public.work_runs WHERE work_run_id=v.owner_binding
 AND runtime_mode='PUBLIC_BOUNDED_LIVE' AND workflow_state='RUNNING' AND
 state_version=owner_version)
 THEN RAISE EXCEPTION 'SEND_GATE_DENIED'; END IF;
 UPDATE public.public_provider_request SET sent_at=n WHERE run_id=r AND ordinal=o
 AND fingerprint=fp AND sent_at IS NULL AND outcome='STARTED';
 IF NOT FOUND THEN RAISE EXCEPTION 'SEND_ALREADY_CLAIMED'; END IF;
END $$;
-- statement
CREATE FUNCTION public_live_api.pipeline_outcome(r bytea,o integer,kind text,closed
 boolean,tokens integer,cost bigint,proof bytea) RETURNS void
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE q public.public_provider_request; charge bigint; v public.public_run;
BEGIN
 v:=public_live_api.lock_run(r);
 SELECT * INTO STRICT q FROM public.public_provider_request WHERE run_id=r AND ordinal=o;
 IF q.outcome<>'STARTED' THEN
  IF q.outcome=kind AND q.response_ref=proof AND q.output_tokens IS NOT DISTINCT FROM tokens
  AND q.closed_failure=closed AND q.recorded_cost IS NOT DISTINCT FROM cost THEN RETURN; END IF;
  RAISE EXCEPTION 'OUTCOME_CONFLICT';
 END IF;
 IF kind NOT IN ('KNOWN_SUCCESS','KNOWN_FAILURE','UNKNOWN') OR closed IS NULL
 OR (closed AND kind<>'KNOWN_FAILURE') OR octet_length(proof) IS DISTINCT FROM 32
 OR kind IS NULL OR tokens<0 OR cost<0 OR (closed AND (tokens IS DISTINCT FROM 0 OR cost IS
 DISTINCT FROM 0)) THEN RAISE EXCEPTION 'OUTCOME_INVALID'; END IF;
 IF tokens>2000 OR cost>4400 THEN
  PERFORM public_live_api.observe(jsonb_build_object(
  'observation_id',encode(substring(sha256(r||int4send(o)||proof) from 1 for 16),'hex'),
   'run_id',encode(r,'hex'),'ordinal',o,'source_identity',encode(sha256(r||int4send(o)||proof),'hex'),
   'classification','ABOVE_BOUND','evidence_digest',encode(proof,'hex'),'cost_micro',cost));
  UPDATE public.public_control SET enabled=false,incident='ABOVE_BOUND_USAGE';
  PERFORM public_live_api.project_run(r,v.version,'FAILED_SAFETY',proof);
  RETURN;
 END IF;
 charge:=CASE WHEN kind='UNKNOWN' OR cost IS NULL OR tokens IS NULL THEN 4400 ELSE cost END;
 PERFORM public_live_api.record_outcome(r,o,kind,charge,proof,
 sha256(r||int4send(o)||proof),substring(sha256(r||int4send(o)||proof) from 1 for 16));
 UPDATE public.public_provider_request SET
 outcome=kind,closed_failure=closed,output_tokens=tokens,
 usage_missing=(tokens IS NULL OR cost IS
 NULL),recorded_cost=cost,response_ref=proof,outcome_at=public_live_api.clock_lock() WHERE
 run_id=r AND ordinal=o;
 IF kind='UNKNOWN' AND v.state='DISPATCH_STARTED' THEN
  PERFORM public_live_api.project_run(r,v.version,'UNKNOWN_OUTCOME',proof);
 END IF;
END $$;
-- statement
CREATE FUNCTION public_live_api.pipeline_validate(r bytea,o integer,decision_value text,proof
 bytea,defect_value text) RETURNS void
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE q public.public_provider_request; old public.public_provider_validation; v
 public.public_run;
BEGIN
 v:=public_live_api.lock_run(r);
 SELECT * INTO STRICT q FROM public.public_provider_request WHERE run_id=r AND ordinal=o;
 SELECT * INTO old FROM public.public_provider_validation WHERE run_id=r AND ordinal=o;
 IF old.ordinal IS NOT NULL THEN
  IF old.decision=decision_value AND old.proof=proof AND old.defect IS NOT DISTINCT FROM
 defect_value THEN RETURN; END IF;
  RAISE EXCEPTION 'VALIDATION_CONFLICT';
 END IF;
 IF q.outcome<>'KNOWN_SUCCESS' OR EXISTS(SELECT 1 FROM public.public_provider_request WHERE
 run_id=r AND ordinal>o)
 OR EXISTS(SELECT 1 FROM public.public_provider_pipeline WHERE run_id=r AND completed)
 THEN RAISE EXCEPTION 'VALIDATION_DENIED'; END IF;
 INSERT INTO public.public_provider_validation
 VALUES(r,o,decision_value,proof,defect_value,public_live_api.clock_lock());
 IF decision_value='COMPLETE' THEN
  UPDATE public.public_provider_pipeline SET completed=true WHERE run_id=r;
  PERFORM public_live_api.project_run(r,v.version,'GOVERNANCE_PENDING',q.response_ref);
 END IF;
END $$;
-- statement
CREATE FUNCTION public_live_api.pipeline_tool(r bytea,tool_name text,owner_version bigint)
RETURNS void
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE v public.public_run;
BEGIN
 v:=public_live_api.lock_run(r);
 IF v.state<>'DISPATCH_STARTED' OR public_live_api.clock_lock()>=v.deadline
 OR NOT EXISTS(SELECT 1 FROM public.work_runs WHERE work_run_id=v.owner_binding
 AND workflow_state='RUNNING' AND runtime_mode='PUBLIC_BOUNDED_LIVE'
 AND state_version=owner_version)
 OR NOT EXISTS(SELECT 1 FROM public.public_reservation WHERE run_id=r AND state='HELD')
 OR NOT EXISTS(SELECT 1 FROM public.public_outbox WHERE run_id=r AND state='BOUND')
 OR NOT EXISTS(SELECT 1 FROM public.public_control WHERE enabled AND incident IS NULL)
 THEN RAISE EXCEPTION 'TOOL_GATE_DENIED'; END IF;
 IF tool_name IS DISTINCT FROM 'stockroom_summary' THEN RAISE EXCEPTION 'TOOL_DENIED'; END IF;
 UPDATE public.public_provider_pipeline SET tool_claimed=true WHERE run_id=r AND NOT tool_claimed
 AND NOT completed
 AND EXISTS(SELECT 1 FROM public.public_provider_request WHERE run_id=r AND
 outcome='KNOWN_SUCCESS');
 IF NOT FOUND THEN RAISE EXCEPTION 'TOOL_ALREADY_CLAIMED'; END IF;
END $$;
"""

RUNTIME = (
    "pipeline_start(bytea,integer,bytea,bigint)",
    "pipeline_context(bytea)",
    "pipeline_request(bytea,bytea,integer,bigint)",
    "pipeline_tool(bytea,text,bigint)",
)
TRUSTED = (
    "pipeline_enroll(bytea,timestamp with time zone)",
    "pipeline_outcome(bytea,integer,text,boolean,integer,bigint,bytea)",
    "pipeline_validate(bytea,integer,text,bytea,text)",
)


def upgrade():
    for statement in SQL.split("-- statement"):
        if statement.strip():
            op.execute(statement)
    for signature in (*RUNTIME, *TRUSTED):
        op.execute(f"REVOKE ALL ON FUNCTION public_live_api.{signature} FROM PUBLIC")
        role = (
            "aiscc_public_live_runtime" if signature in RUNTIME else "aiscc_public_live_reconciler"
        )
        op.execute(f"GRANT EXECUTE ON FUNCTION public_live_api.{signature} TO {role}")
    for name in (
        "public_provider_pipeline",
        "public_provider_request",
        "public_provider_validation",
    ):
        op.execute(
            f"REVOKE ALL ON public.{name} FROM "
            "PUBLIC,aiscc_public_live_runtime,aiscc_public_live_reconciler"
        )
    for signature in (
        "mark_dispatch_legacy(bytea,bigint,integer,bigint)",
        "mark_checked_legacy(bytea,bigint,integer,bigint,bigint)",
        "project_run_legacy(bytea,bigint,text,bytea)",
    ):
        op.execute(
            f"REVOKE ALL ON FUNCTION public_live_api.{signature} FROM "
            "PUBLIC,aiscc_public_live_runtime,aiscc_public_live_reconciler"
        )
    for signature in (
        "mark_dispatch(bytea,bigint,integer,bigint)",
        "mark_checked(bytea,bigint,integer,bigint,bigint)",
        "project_run(bytea,bigint,text,bytea)",
    ):
        op.execute(f"REVOKE ALL ON FUNCTION public_live_api.{signature} FROM PUBLIC")
        op.execute(
            f"GRANT EXECUTE ON FUNCTION public_live_api.{signature} TO aiscc_public_live_runtime"
        )


def downgrade():
    if (
        op.get_bind()
        .exec_driver_sql("SELECT EXISTS(SELECT 1 FROM public.public_provider_pipeline)")
        .scalar()
    ):
        raise RuntimeError("SEMANTIC_PIPELINE_IN_USE")
    for signature in (*RUNTIME, *TRUSTED):
        op.execute(f"DROP FUNCTION public_live_api.{signature}")
    op.execute(
        "DROP TABLE "
        "public.public_provider_validation,public.public_provider_request,public.public_provider_pipeline"
    )
    for signature in (
        "mark_dispatch(bytea,bigint,integer,bigint)",
        "mark_checked(bytea,bigint,integer,bigint,bigint)",
        "project_run(bytea,bigint,text,bytea)",
    ):
        op.execute(f"DROP FUNCTION public_live_api.{signature}")
    op.execute(
        "ALTER FUNCTION "
        "public_live_api.mark_dispatch_legacy(bytea,bigint,integer,bigint) RENAME TO mark_dispatch"
    )
    op.execute(
        "ALTER FUNCTION public_live_api.project_run_legacy(bytea,bigint,text,bytea) "
        "RENAME TO project_run"
    )
    op.execute(
        "ALTER FUNCTION public_live_api.mark_checked_legacy(bytea,bigint,integer,bigint,bigint) "
        "RENAME TO mark_checked"
    )
    op.execute(
        "GRANT EXECUTE ON FUNCTION "
        "public_live_api.mark_checked(bytea,bigint,integer,bigint,bigint) "
        "TO aiscc_public_live_runtime"
    )
    op.execute("ALTER TABLE public.public_dispatch DROP CONSTRAINT public_dispatch_ordinal_check")
    op.execute(
        "ALTER TABLE public.public_dispatch ADD CONSTRAINT "
        "public_dispatch_ordinal_check CHECK(ordinal IN (1,2))"
    )
    op.execute(
        "GRANT EXECUTE ON FUNCTION "
        "public_live_api.mark_dispatch(bytea,bigint,integer,bigint) TO aiscc_public_live_runtime"
    )
    op.execute(
        "GRANT EXECUTE ON FUNCTION "
        "public_live_api.project_run(bytea,bigint,text,bytea) TO aiscc_public_live_runtime"
    )
