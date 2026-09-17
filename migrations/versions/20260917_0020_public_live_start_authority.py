# ruff: noqa: E501
"""Dedicated Public Live start request, initializer lease and binding authority."""

from alembic import op

revision = "20260917_0020"
down_revision = "20260917_0019"
branch_labels = None
depends_on = None

SQL = r"""
ALTER TABLE public.public_control ADD COLUMN start_gate_version bigint NOT NULL DEFAULT 1 CHECK(start_gate_version>=1);
-- statement
CREATE FUNCTION public_live_api.bump_start_gate() RETURNS trigger LANGUAGE plpgsql SET search_path=pg_catalog AS $$
BEGIN
 IF (OLD.enabled,OLD.policy_digest,OLD.incident,OLD.active_campaign) IS DISTINCT FROM
    (NEW.enabled,NEW.policy_digest,NEW.incident,NEW.active_campaign) THEN
  IF OLD.start_gate_version=9223372036854775807 THEN RAISE EXCEPTION 'START_GATE_EXHAUSTED'; END IF;
  NEW.start_gate_version:=OLD.start_gate_version+1;
 END IF;
 RETURN NEW;
END $$;
-- statement
CREATE TRIGGER public_control_start_gate BEFORE UPDATE ON public.public_control
FOR EACH ROW EXECUTE FUNCTION public_live_api.bump_start_gate();
-- statement
CREATE TABLE public.public_start_request(
 run_id bytea PRIMARY KEY REFERENCES public.public_run(run_id) ON DELETE RESTRICT CHECK(octet_length(run_id)=16),
 candidate_id bytea NOT NULL UNIQUE CHECK(octet_length(candidate_id)=32),
 candidate_body jsonb NOT NULL CHECK(octet_length(convert_to(candidate_body::text,'UTF8'))<=8192),
 gate_version bigint NOT NULL CHECK(gate_version>=1),
 phase text NOT NULL DEFAULT 'REGISTERED' CHECK(phase IN('REGISTERED','READY_CREATED','ATTEMPT_PREPARED','WORKFLOW_RUNNING','EXECUTION_RUNNING','BOUND','HALTED')),
 phase_version bigint NOT NULL DEFAULT 1 CHECK(phase_version>=1),
 work_run_id varchar(128) NOT NULL UNIQUE,
 execution_attempt_id varchar(128) UNIQUE REFERENCES public.execution_attempts(execution_attempt_id) ON DELETE RESTRICT,
 owner_instance bytea CHECK(owner_instance IS NULL OR octet_length(owner_instance)=16),
 lease_generation bigint NOT NULL DEFAULT 0 CHECK(lease_generation>=0),
 lease_expires_at timestamptz,last_reason text,binding_digest bytea CHECK(binding_digest IS NULL OR octet_length(binding_digest)=32),
 created_at timestamptz NOT NULL,updated_at timestamptz NOT NULL,
 CHECK(work_run_id='public-live-'||encode(run_id,'hex'))
);
-- statement
CREATE TABLE public.public_start_event(
 event_id bytea PRIMARY KEY CHECK(octet_length(event_id)=16),
 run_id bytea NOT NULL REFERENCES public.public_start_request(run_id) ON DELETE RESTRICT,
 phase_version bigint NOT NULL CHECK(phase_version>=1),
 kind text NOT NULL CHECK(kind IN('REGISTERED','GENESIS','START_ADMITTED','ATTEMPT_PREPARED','WORKFLOW_RUNNING','EXECUTION_RUNNING','BOUND','DENIED','HALTED','RECOVERED')),
 source_identity bytea NOT NULL CHECK(octet_length(source_identity)=32),
 safe_refs jsonb NOT NULL DEFAULT '{}' CHECK(octet_length(convert_to(safe_refs::text,'UTF8'))<=4096),
 recorded_at timestamptz NOT NULL,UNIQUE(run_id,phase_version),UNIQUE(run_id,kind,source_identity)
);
-- statement
CREATE INDEX public_start_pending ON public.public_start_request(phase,created_at,run_id) WHERE phase NOT IN('BOUND','HALTED');
-- statement
CREATE INDEX public_start_lease ON public.public_start_request(lease_expires_at) WHERE phase NOT IN('BOUND','HALTED');
-- statement
CREATE FUNCTION public_live_api.start_immutable() RETURNS trigger LANGUAGE plpgsql SET search_path=pg_catalog AS $$
BEGIN RAISE EXCEPTION 'START_HISTORY_IMMUTABLE'; END $$;
-- statement
CREATE TRIGGER public_start_event_immutable BEFORE UPDATE OR DELETE ON public.public_start_event FOR EACH ROW EXECUTE FUNCTION public_live_api.start_immutable();
-- statement
CREATE FUNCTION public_live_api.start_register_from_admission(r bytea,c bytea,p jsonb) RETURNS bytea
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE n timestamptz; g bigint; old public.public_start_request; source bytea;
BEGIN n:=public_live_api.clock_lock();
 SELECT start_gate_version INTO STRICT g FROM public.public_control;
 IF octet_length(r)<>16 OR octet_length(c)<>32 OR p->>'schema_version'<>'PUBLIC_LIVE_START_V1'
 OR p->>'public_run_id'<>encode(r,'hex') OR p->>'runtime_mode'<>'PUBLIC_BOUNDED_LIVE'
 OR p->>'scenario_id'<>'stockroom-s1-normal' OR p->>'scenario_version'<>'1.0.0'
 OR p->>'task_contract_id'<>'aiscc-public-live-stockroom-v1' OR p->>'task_contract_version'<>'1'
 OR p->>'provider_profile_id'<>'public-live-luna-v1' OR p->>'provider_profile_version'<>'1'
 OR (p->>'gate_version')::bigint<>g OR decode(p->>'candidate_id','hex') IS DISTINCT FROM c
 OR NOT EXISTS(SELECT 1 FROM public.public_run x JOIN public.public_outbox o USING(run_id)
   WHERE x.run_id=r AND x.state='ADMITTED' AND x.deadline>n AND o.state='PENDING')
 THEN RAISE EXCEPTION 'START_REGISTRATION_DENIED'; END IF;
 SELECT * INTO old FROM public.public_start_request WHERE run_id=r;
 IF old.run_id IS NOT NULL THEN
  IF old.candidate_id=c AND old.candidate_body=p THEN RETURN c; END IF;
  RAISE EXCEPTION 'START_IDENTITY_CONFLICT';
 END IF;
 INSERT INTO public.public_start_request(run_id,candidate_id,candidate_body,gate_version,work_run_id,created_at,updated_at)
 VALUES(r,c,p,g,'public-live-'||encode(r,'hex'),n,n);
 source:=sha256(r||c);
 INSERT INTO public.public_start_event VALUES(substring(source from 1 for 16),r,1,'REGISTERED',source,'{}',n);
 RETURN c;
END $$;
-- statement
CREATE FUNCTION public_live_api.admit_checked_and_start(a jsonb,p jsonb) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE result jsonb; r bytea; c bytea; n timestamptz; g bigint; x public.public_run;
BEGIN
 result:=public_live_api.admit_checked(a);
 IF result ? 'error' OR (result->>'replayed')::boolean THEN RETURN result; END IF;
 r:=decode(result->>'run_id','hex'); n:=public_live_api.clock_lock();
 SELECT * INTO STRICT x FROM public.public_run WHERE run_id=r;
 SELECT start_gate_version INTO STRICT g FROM public.public_control;
 p:=p||jsonb_build_object(
  'schema_version','PUBLIC_LIVE_START_V1','public_run_id',encode(r,'hex'),
  'campaign_id',x.campaign_id,'gate_version',g,'admitted_at',x.admitted_at,
  'deadline',x.deadline,'runtime_mode','PUBLIC_BOUNDED_LIVE',
  'issuer','PUBLIC_LIVE_CHECKED_ADMISSION_V1');
 c:=sha256(convert_to(p::text,'UTF8')); p:=p||jsonb_build_object('candidate_id',encode(c,'hex'));
 PERFORM public_live_api.start_register_from_admission(r,c,p);
 RETURN result;
END $$;
-- statement
CREATE FUNCTION public_live_api.start_json(x public.public_start_request) RETURNS jsonb LANGUAGE sql IMMUTABLE SET search_path=pg_catalog AS $$
 SELECT jsonb_build_object('run_id',encode(x.run_id,'hex'),'candidate_id',encode(x.candidate_id,'hex'),'work_run_id',x.work_run_id,
 'phase',x.phase,'phase_version',x.phase_version,'lease_generation',x.lease_generation,'lease_expires_at',x.lease_expires_at,'candidate',x.candidate_body)
$$;
-- statement
CREATE FUNCTION public_live_api.start_next(p bytea) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE n timestamptz; x public.public_start_request;
BEGIN n:=public_live_api.clock_lock(); IF octet_length(p)<>16 THEN RAISE EXCEPTION 'START_PROCESS_INVALID'; END IF;
 SELECT s.* INTO x FROM public.public_start_request s JOIN public.public_run r USING(run_id)
 JOIN public.public_outbox o USING(run_id) JOIN public.public_reservation z USING(run_id)
 JOIN public.public_slot sl ON sl.run_id=o.run_id AND sl.generation=o.generation
 JOIN public.public_control c ON true
 WHERE s.phase NOT IN('BOUND','HALTED') AND (s.lease_expires_at IS NULL OR s.lease_expires_at<=n)
 AND c.enabled AND c.incident IS NULL AND c.start_gate_version=s.gate_version
 AND r.deadline>=n+interval '35 seconds' AND z.state='HELD'
 AND o.state='PENDING' AND sl.state='OCCUPIED' AND sl.expires_at>n
 ORDER BY s.created_at,s.run_id FOR UPDATE OF s SKIP LOCKED LIMIT 1;
 IF x.run_id IS NULL THEN RETURN NULL; END IF;
 IF x.lease_generation=9223372036854775807 THEN RAISE EXCEPTION 'START_LEASE_EXHAUSTED'; END IF;
 UPDATE public.public_start_request SET owner_instance=p,lease_generation=lease_generation+1,lease_expires_at=n+interval '15 seconds',updated_at=n
 WHERE run_id=x.run_id RETURNING * INTO x; RETURN public_live_api.start_json(x);
END $$;
-- statement
CREATE FUNCTION public_live_api.start_renew(r bytea,p bytea,g bigint) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE n timestamptz; x public.public_start_request;
BEGIN n:=public_live_api.clock_lock(); UPDATE public.public_start_request SET lease_expires_at=n+interval '15 seconds',updated_at=n
 WHERE run_id=r AND owner_instance=p AND lease_generation=g AND lease_expires_at>n AND phase NOT IN('BOUND','HALTED') RETURNING * INTO x;
 IF x.run_id IS NULL THEN RAISE EXCEPTION 'START_LEASE_STALE'; END IF; RETURN public_live_api.start_json(x); END $$;
-- statement
CREATE FUNCTION public_live_api.start_context(r bytea,p bytea,g bigint) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE n timestamptz; x public.public_start_request;
BEGIN n:=public_live_api.clock_lock(); SELECT * INTO STRICT x FROM public.public_start_request WHERE run_id=r FOR UPDATE;
 IF x.owner_instance<>p OR x.lease_generation<>g OR x.lease_expires_at<=n
 OR NOT EXISTS(SELECT 1 FROM public.public_control c WHERE c.enabled AND c.incident IS NULL AND c.start_gate_version=x.gate_version)
 OR NOT EXISTS(SELECT 1 FROM public.public_run q WHERE q.run_id=r AND q.deadline>=n+interval '35 seconds')
 OR NOT EXISTS(SELECT 1 FROM public.public_reservation z WHERE z.run_id=r AND z.state='HELD')
 OR NOT EXISTS(SELECT 1 FROM public.public_outbox o JOIN public.public_slot sl ON sl.run_id=o.run_id AND sl.generation=o.generation
   WHERE o.run_id=r AND o.state='PENDING' AND sl.state='OCCUPIED' AND sl.expires_at>n)
 THEN RAISE EXCEPTION 'START_FRESHNESS_DENIED'; END IF;
 RETURN public_live_api.start_json(x)||jsonb_build_object('control_gate',(SELECT start_gate_version FROM public.public_control),
 'authority_now',n,
 'work_run',(SELECT to_jsonb(w) FROM public.work_runs w WHERE w.work_run_id=x.work_run_id),
 'attempt',(SELECT to_jsonb(a) FROM public.execution_attempts a WHERE a.execution_attempt_id=x.execution_attempt_id)); END $$;
-- statement
CREATE FUNCTION public_live_api.start_record_phase(r bytea,p bytea,g bigint,h text,s bytea) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE n timestamptz; x public.public_start_request; next_kind text;
BEGIN n:=public_live_api.clock_lock(); SELECT * INTO STRICT x FROM public.public_start_request WHERE run_id=r FOR UPDATE;
 IF x.owner_instance<>p OR x.lease_generation<>g OR x.lease_expires_at<=n OR octet_length(s)<>32 THEN RAISE EXCEPTION 'START_LEASE_STALE'; END IF;
 IF (x.phase,h) NOT IN (('REGISTERED','READY_CREATED'),('READY_CREATED','ATTEMPT_PREPARED'),('ATTEMPT_PREPARED','WORKFLOW_RUNNING'),('WORKFLOW_RUNNING','EXECUTION_RUNNING'))
 THEN RAISE EXCEPTION 'START_PHASE_DENIED'; END IF;
 next_kind:=CASE h WHEN 'READY_CREATED' THEN 'GENESIS' WHEN 'ATTEMPT_PREPARED' THEN 'ATTEMPT_PREPARED' ELSE h END;
 UPDATE public.public_start_request SET phase=h,phase_version=phase_version+1,updated_at=n WHERE run_id=r RETURNING * INTO x;
 INSERT INTO public.public_start_event VALUES(substring(sha256(r||s||convert_to(h,'UTF8')) from 1 for 16),r,x.phase_version,next_kind,s,'{}',n)
 ON CONFLICT(run_id,kind,source_identity) DO NOTHING; RETURN public_live_api.start_json(x); END $$;
-- statement
CREATE FUNCTION public_live_api.start_zero_effects(r bytea,a varchar) RETURNS boolean
LANGUAGE sql SECURITY DEFINER SET search_path=pg_catalog AS $$ SELECT EXISTS(SELECT 1 FROM public.public_start_request s WHERE s.run_id=r AND s.execution_attempt_id=a)
 AND NOT EXISTS(SELECT 1 FROM public.execution_operations o WHERE o.execution_attempt_id=a)
 AND NOT EXISTS(SELECT 1 FROM public.private_provider_protocol_states q WHERE q.execution_attempt_id=a)
 AND NOT EXISTS(SELECT 1 FROM public.execution_output_refs z WHERE z.execution_attempt_id=a) $$;
-- statement
CREATE FUNCTION public_live_api.start_set_attempt(r bytea,p bytea,g bigint,a varchar,s bytea) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE x public.public_start_request;
BEGIN SELECT * INTO STRICT x FROM public.public_start_request WHERE run_id=r FOR UPDATE;
 IF x.owner_instance<>p OR x.lease_generation<>g OR x.phase<>'READY_CREATED' OR x.execution_attempt_id IS NOT NULL
 OR NOT EXISTS(SELECT 1 FROM public.execution_attempts e WHERE e.execution_attempt_id=a AND e.work_run_id=x.work_run_id AND e.status='NOT_STARTED')
 THEN RAISE EXCEPTION 'START_ATTEMPT_DENIED'; END IF;
 UPDATE public.public_start_request SET execution_attempt_id=a WHERE run_id=r; RETURN public_live_api.start_record_phase(r,p,g,'ATTEMPT_PREPARED',s); END $$;
-- statement
CREATE FUNCTION public_live_api.start_finalize_binding(r bytea,p bytea,g bigint,d bytea,plan bytea,s bytea) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE n timestamptz; x public.public_start_request; result jsonb;
BEGIN n:=public_live_api.clock_lock(); SELECT * INTO STRICT x FROM public.public_start_request WHERE run_id=r FOR UPDATE;
 IF x.owner_instance<>p OR x.lease_generation<>g OR x.lease_expires_at<=n OR x.phase<>'EXECUTION_RUNNING'
 OR octet_length(d)<>32 OR octet_length(plan)<>32 OR octet_length(s)<>32 OR NOT public_live_api.start_zero_effects(r,x.execution_attempt_id)
 OR NOT EXISTS(SELECT 1 FROM public.public_control c WHERE c.enabled AND c.incident IS NULL
   AND c.start_gate_version=x.gate_version)
 OR NOT EXISTS(SELECT 1 FROM public.public_run q WHERE q.run_id=r AND q.deadline>=n+interval '35 seconds')
 OR NOT EXISTS(SELECT 1 FROM public.public_reservation z WHERE z.run_id=r AND z.state='HELD')
 OR NOT EXISTS(SELECT 1 FROM public.public_outbox o JOIN public.public_slot sl
   ON sl.run_id=o.run_id AND sl.generation=o.generation WHERE o.run_id=r
   AND o.state='PENDING' AND sl.state='OCCUPIED' AND sl.expires_at>n)
 THEN RAISE EXCEPTION 'START_BIND_DENIED'; END IF;
 UPDATE public.public_run SET owner_binding=x.work_run_id WHERE run_id=r AND owner_binding IS NULL;
 UPDATE public.public_outbox SET state='BOUND',owner_binding=x.work_run_id
 WHERE run_id=r AND state='PENDING' AND owner_binding IS NULL;
 IF NOT EXISTS(SELECT 1 FROM public.public_run q JOIN public.public_outbox o USING(run_id)
 WHERE q.run_id=r AND q.owner_binding=x.work_run_id AND o.state='BOUND'
 AND o.owner_binding=x.work_run_id) THEN RAISE EXCEPTION 'START_OWNER_BIND_DENIED'; END IF;
 result:=public_live_api.execution_bind(r,x.work_run_id,x.execution_attempt_id,d,plan);
 PERFORM public_live_api.worker_enroll(r,s);
 UPDATE public.public_start_request SET phase='BOUND',phase_version=phase_version+1,binding_digest=d,lease_expires_at=NULL,updated_at=n WHERE run_id=r RETURNING * INTO x;
 INSERT INTO public.public_start_event VALUES(substring(sha256(r||s||d) from 1 for 16),r,x.phase_version,'BOUND',s,'{}',n);
 RETURN result; END $$;
-- statement
CREATE FUNCTION public_live_api.start_halt(r bytea,p bytea,g bigint,h text,s bytea) RETURNS void
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE n timestamptz; x public.public_start_request;
BEGIN n:=public_live_api.clock_lock(); SELECT * INTO STRICT x FROM public.public_start_request WHERE run_id=r FOR UPDATE;
 IF x.owner_instance<>p OR x.lease_generation<>g OR x.lease_expires_at<=n OR octet_length(s)<>32 OR length(h)>64
 OR (x.execution_attempt_id IS NOT NULL AND NOT public_live_api.start_zero_effects(r,x.execution_attempt_id))
 THEN RAISE EXCEPTION 'START_HALT_DENIED'; END IF;
 UPDATE public.public_start_request SET phase='HALTED',phase_version=phase_version+1,last_reason=h,lease_expires_at=NULL,updated_at=n WHERE run_id=r RETURNING * INTO x;
 INSERT INTO public.public_start_event VALUES(substring(sha256(r||s||convert_to(h,'UTF8')) from 1 for 16),r,x.phase_version,'HALTED',s,'{}',n); END $$;
-- statement
CREATE FUNCTION public_live_api.initializer_shape_guard() RETURNS trigger LANGUAGE plpgsql SET search_path=pg_catalog AS $$
BEGIN
 IF current_user='aiscc_public_live_initializer' THEN
  IF TG_TABLE_NAME='work_runs' THEN
   IF (TG_OP='INSERT' AND (NEW.workflow_state<>'READY' OR NEW.state_version<>1 OR NEW.runtime_mode<>'PUBLIC_BOUNDED_LIVE'))
   OR (TG_OP='UPDATE' AND (OLD.workflow_state<>'READY' OR NEW.workflow_state<>'RUNNING' OR NEW.state_version<>OLD.state_version+1))
   THEN RAISE EXCEPTION 'INITIALIZER_WORKFLOW_SHAPE_DENIED'; END IF;
  ELSIF TG_TABLE_NAME='execution_attempts' THEN
   IF TG_OP='INSERT' AND (NEW.status<>'NOT_STARTED' OR NEW.execution_version<>1 OR NEW.creation_state<>'READY')
   THEN RAISE EXCEPTION 'INITIALIZER_ATTEMPT_SHAPE_DENIED'; END IF;
  END IF;
 END IF; RETURN NEW; END $$;
-- statement
CREATE TRIGGER initializer_work_run_shape BEFORE INSERT OR UPDATE ON public.work_runs FOR EACH ROW EXECUTE FUNCTION public_live_api.initializer_shape_guard();
-- statement
CREATE TRIGGER initializer_attempt_shape BEFORE INSERT OR UPDATE ON public.execution_attempts FOR EACH ROW EXECUTE FUNCTION public_live_api.initializer_shape_guard();
"""

INITIALIZER = (
    "start_next(bytea)",
    "start_renew(bytea,bytea,bigint)",
    "start_context(bytea,bytea,bigint)",
    "start_record_phase(bytea,bytea,bigint,text,bytea)",
    "start_set_attempt(bytea,bytea,bigint,character varying,bytea)",
    "start_finalize_binding(bytea,bytea,bigint,bytea,bytea,bytea)",
    "start_halt(bytea,bytea,bigint,text,bytea)",
    "start_zero_effects(bytea,character varying)",
)


def upgrade() -> None:
    for statement in SQL.split("-- statement"):
        if statement.strip():
            op.execute(statement)
    op.execute(
        "DO $$ BEGIN CREATE ROLE aiscc_public_live_initializer NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOBYPASSRLS; EXCEPTION WHEN duplicate_object THEN NULL; END $$"
    )
    op.execute(
        "DO $$ BEGIN CREATE ROLE aiscc_live_initializer_login LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOBYPASSRLS; EXCEPTION WHEN duplicate_object THEN NULL; END $$"
    )
    op.execute("GRANT aiscc_public_live_initializer TO aiscc_live_initializer_login")
    for signature in (
        *INITIALIZER,
        "start_register_from_admission(bytea,bytea,jsonb)",
        "admit_checked_and_start(jsonb,jsonb)",
    ):
        op.execute(f"REVOKE ALL ON FUNCTION public_live_api.{signature} FROM PUBLIC")
    for signature in INITIALIZER:
        op.execute(
            f"GRANT EXECUTE ON FUNCTION public_live_api.{signature} TO aiscc_public_live_initializer"
        )
    op.execute(
        "GRANT EXECUTE ON FUNCTION public_live_api.admit_checked_and_start(jsonb,jsonb) TO aiscc_public_live_runtime"
    )
    op.execute("GRANT USAGE ON SCHEMA public,public_live_api TO aiscc_public_live_initializer")
    op.execute(
        "GRANT SELECT,INSERT ON public.work_runs,public.transition_requests,public.transition_evaluations,public.transition_decisions,public.execution_attempts,public.execution_events TO aiscc_public_live_initializer"
    )
    op.execute(
        "GRANT SELECT ON public.private_provider_protocol_states,public.execution_output_refs,"
        "public.execution_operations,public.operation_events TO aiscc_public_live_initializer"
    )
    op.execute(
        "GRANT UPDATE(workflow_state,state_version,updated_at) ON public.work_runs TO aiscc_public_live_initializer"
    )
    op.execute(
        "GRANT UPDATE(status,execution_version,latest_event_sequence,causal_state,causal_state_version,updated_at) ON public.execution_attempts TO aiscc_public_live_initializer"
    )
    op.execute(
        "GRANT USAGE,SELECT ON SEQUENCE public.transition_decisions_event_sequence_seq,public.execution_events_event_sequence_seq TO aiscc_public_live_initializer"
    )
    for table in ("public_start_request", "public_start_event"):
        op.execute(
            f"REVOKE ALL ON public.{table} FROM PUBLIC,aiscc_public_live_runtime,aiscc_public_live_execution,aiscc_public_live_initializer"
        )


def downgrade() -> None:
    op.execute("DROP TRIGGER initializer_attempt_shape ON public.execution_attempts")
    op.execute("DROP TRIGGER initializer_work_run_shape ON public.work_runs")
    op.execute("DROP FUNCTION public_live_api.initializer_shape_guard()")
    for signature in reversed(INITIALIZER):
        op.execute(f"DROP FUNCTION public_live_api.{signature}")
    op.execute("DROP FUNCTION public_live_api.start_json(public.public_start_request)")
    op.execute("DROP FUNCTION public_live_api.admit_checked_and_start(jsonb,jsonb)")
    op.execute("DROP FUNCTION public_live_api.start_register_from_admission(bytea,bytea,jsonb)")
    op.execute("DROP TRIGGER public_start_event_immutable ON public.public_start_event")
    op.execute("DROP TABLE public.public_start_event")
    op.execute("DROP TABLE public.public_start_request")
    op.execute("DROP FUNCTION public_live_api.start_immutable()")
    op.execute("DROP TRIGGER public_control_start_gate ON public.public_control")
    op.execute("DROP FUNCTION public_live_api.bump_start_gate()")
    op.execute("ALTER TABLE public.public_control DROP COLUMN start_gate_version")
