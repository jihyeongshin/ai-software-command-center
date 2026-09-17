# ruff: noqa: E501
"""Durable Public Live worker claim, lease and fence authority."""

from alembic import op

revision = "20260917_0019"
down_revision = "20260916_0018"
branch_labels = None
depends_on = None

SQL = r"""
DO $$ BEGIN CREATE ROLE aiscc_public_live_execution NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOBYPASSRLS;
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
-- statement
DO $$ BEGIN CREATE ROLE aiscc_live_worker_login LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOBYPASSRLS;
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
-- statement
CREATE TABLE public.public_worker_instance(
 worker_id bytea PRIMARY KEY CHECK(octet_length(worker_id)=16),
 process_generation bytea NOT NULL CHECK(octet_length(process_generation)=16),
 registered_at timestamptz NOT NULL,draining boolean NOT NULL DEFAULT false,
 last_acquire_seq bigint NOT NULL DEFAULT 0 CHECK(last_acquire_seq>=0),
 last_acquire_hash bytea CHECK(octet_length(last_acquire_hash)=32),
 last_result_claim_id bytea,last_result_kind text NOT NULL DEFAULT 'EMPTY' CHECK(last_result_kind IN('EMPTY','CLAIM')),
 last_acquire_at timestamptz,
 CHECK((last_acquire_seq=0)=(last_acquire_at IS NULL)),
 CHECK((last_result_kind='CLAIM')=(last_result_claim_id IS NOT NULL))
);
-- statement
CREATE TABLE public.public_worker_work(
 run_id bytea PRIMARY KEY REFERENCES public.public_provider_execution(run_id) ON DELETE RESTRICT CHECK(octet_length(run_id)=16),
 work_kind text NOT NULL DEFAULT 'PUBLIC_LIVE_PIPELINE_V1' CHECK(work_kind='PUBLIC_LIVE_PIPELINE_V1'),
 contract_version text NOT NULL DEFAULT 'WORKER_V1' CHECK(contract_version='WORKER_V1'),
 registered_at timestamptz NOT NULL,fence bigint NOT NULL DEFAULT 0 CHECK(fence>=0),
 recovery_required boolean NOT NULL DEFAULT false,closed_at timestamptz,close_reason text,
 CHECK((closed_at IS NULL)=(close_reason IS NULL))
);
-- statement
CREATE TABLE public.public_worker_claim(
 claim_id bytea PRIMARY KEY CHECK(octet_length(claim_id)=16),
 run_id bytea NOT NULL REFERENCES public.public_worker_work(run_id) ON DELETE RESTRICT,
 worker_id bytea NOT NULL REFERENCES public.public_worker_instance(worker_id) ON DELETE RESTRICT,
 process_generation bytea NOT NULL CHECK(octet_length(process_generation)=16),
 fence bigint NOT NULL CHECK(fence>=1),acquisition_seq bigint NOT NULL CHECK(acquisition_seq>=1),
 acquired_action text NOT NULL CHECK(acquired_action IN('EXECUTE','VALIDATE')),
 claimed_at timestamptz NOT NULL,heartbeat_at timestamptz NOT NULL,lease_expires_at timestamptz NOT NULL,
 claim_version bigint NOT NULL DEFAULT 1 CHECK(claim_version>=1),current_operation_id varchar(128),
 released_at timestamptz,release_reason text,
 UNIQUE(run_id,fence),UNIQUE(worker_id,acquisition_seq),
 CHECK(claimed_at<=heartbeat_at AND heartbeat_at<=lease_expires_at AND lease_expires_at<=heartbeat_at+interval '15 seconds'),
 CHECK((released_at IS NULL)=(release_reason IS NULL))
);
-- statement
ALTER TABLE public.public_worker_instance ADD CONSTRAINT public_worker_instance_last_claim_fk
FOREIGN KEY(last_result_claim_id) REFERENCES public.public_worker_claim(claim_id) DEFERRABLE INITIALLY DEFERRED;
-- statement
CREATE UNIQUE INDEX public_worker_one_open_run ON public.public_worker_claim(run_id) WHERE released_at IS NULL;
-- statement
CREATE UNIQUE INDEX public_worker_one_open_instance ON public.public_worker_claim(worker_id) WHERE released_at IS NULL;
-- statement
CREATE INDEX public_worker_claim_expiry ON public.public_worker_claim(lease_expires_at,run_id,claim_id) WHERE released_at IS NULL;
-- statement
CREATE TABLE public.public_worker_dispatch_pin(
 operation_id varchar(128) PRIMARY KEY REFERENCES public.execution_operations(operation_id) ON DELETE RESTRICT,
 claim_id bytea NOT NULL REFERENCES public.public_worker_claim(claim_id) ON DELETE RESTRICT,
 dispatch_event_id varchar(128) NOT NULL UNIQUE REFERENCES public.operation_events(event_id) ON DELETE RESTRICT,
 pinned_at timestamptz NOT NULL,closed_at timestamptz,closure_evidence_digest bytea,
 outcome_event_id varchar(128) REFERENCES public.operation_events(event_id) ON DELETE RESTRICT,
 CHECK(closure_evidence_digest IS NULL OR octet_length(closure_evidence_digest)=32),
 CHECK((closed_at IS NULL AND closure_evidence_digest IS NULL AND outcome_event_id IS NULL)
 OR (closed_at IS NOT NULL AND closure_evidence_digest IS NOT NULL AND outcome_event_id IS NOT NULL))
);
-- statement
CREATE UNIQUE INDEX public_worker_one_open_pin ON public.public_worker_dispatch_pin(claim_id) WHERE closed_at IS NULL;
-- statement
CREATE TABLE public.public_worker_claim_event(
 event_id bytea PRIMARY KEY CHECK(octet_length(event_id)=16),run_id bytea NOT NULL REFERENCES public.public_worker_work(run_id),
 claim_id bytea REFERENCES public.public_worker_claim(claim_id),event_seq bigint NOT NULL CHECK(event_seq>=1),
 kind text NOT NULL CHECK(kind IN('ENROLLED','ACQUIRED','RENEWED','OPERATION_BOUND','PINNED','PIN_CLOSED','RELEASED','REVOKED','QUARANTINED','RECOVERED','CLOSED')),
 reason text,recorded_at timestamptz NOT NULL,observed_state_version bigint,observed_execution_version bigint,
 operation_id varchar(128) REFERENCES public.execution_operations(operation_id),
 source_digest bytea NOT NULL CHECK(octet_length(source_digest)=32),payload_hash bytea NOT NULL CHECK(octet_length(payload_hash)=32),
 refs jsonb NOT NULL DEFAULT '{}' CHECK(octet_length(convert_to(refs::text,'UTF8'))<=4096),
 UNIQUE(run_id,event_seq),UNIQUE(run_id,kind,source_digest)
);
-- statement
CREATE FUNCTION public_live_api.worker_register_instance(w bytea,p bytea) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE n timestamptz; x public.public_worker_instance;
BEGIN n:=public_live_api.clock_lock();
 IF octet_length(w)<>16 OR octet_length(p)<>16 THEN RAISE EXCEPTION 'INSTANCE_INVALID'; END IF;
 INSERT INTO public.public_worker_instance(worker_id,process_generation,registered_at) VALUES(w,p,n)
 ON CONFLICT(worker_id) DO NOTHING;
 SELECT * INTO STRICT x FROM public.public_worker_instance WHERE worker_id=w;
 IF x.process_generation<>p THEN RAISE EXCEPTION 'INSTANCE_CONFLICT'; END IF;
 RETURN jsonb_build_object('worker_id',encode(w,'hex'),'process_generation',encode(p,'hex'),'draining',x.draining);
END $$;
-- statement
CREATE FUNCTION public_live_api.worker_enroll(r bytea,s bytea) RETURNS void
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE n timestamptz; seq bigint;
BEGIN n:=public_live_api.clock_lock();
 IF octet_length(s)<>32 OR NOT EXISTS(SELECT 1 FROM public.public_provider_execution WHERE run_id=r)
 THEN RAISE EXCEPTION 'WORK_ENROLL_DENIED'; END IF;
 INSERT INTO public.public_worker_work(run_id,registered_at) VALUES(r,n) ON CONFLICT(run_id) DO NOTHING;
 SELECT coalesce(max(event_seq),0)+1 INTO seq FROM public.public_worker_claim_event WHERE run_id=r;
 INSERT INTO public.public_worker_claim_event VALUES(substring(sha256(r||s) from 1 for 16),r,NULL,seq,'ENROLLED',NULL,n,NULL,NULL,NULL,s,sha256(r||s),'{}')
 ON CONFLICT(run_id,kind,source_digest) DO NOTHING;
END $$;
-- statement
CREATE FUNCTION public_live_api.worker_claim_next(w bytea,p bytea,seq_value bigint,h bytea) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE i public.public_worker_instance; k public.public_worker_work; c public.public_worker_claim; n timestamptz; cid bytea; ev bigint;
BEGIN n:=public_live_api.clock_lock();
 SELECT * INTO STRICT i FROM public.public_worker_instance WHERE worker_id=w FOR UPDATE;
 IF i.process_generation<>p OR i.draining OR octet_length(h)<>32 OR seq_value<1 THEN RAISE EXCEPTION 'CLAIM_PRINCIPAL_DENIED'; END IF;
 IF seq_value=i.last_acquire_seq THEN
  IF i.last_result_kind='EMPTY' THEN RETURN jsonb_build_object('kind','EMPTY'); END IF;
  SELECT * INTO STRICT c FROM public.public_worker_claim WHERE claim_id=i.last_result_claim_id;
  RETURN jsonb_build_object('kind','CLAIM','run_id',encode(c.run_id,'hex'),'claim_id',encode(c.claim_id,'hex'),'fence',c.fence,'claim_version',c.claim_version,'lease_expires_at',c.lease_expires_at);
 END IF;
 IF seq_value<>i.last_acquire_seq+1 OR EXISTS(SELECT 1 FROM public.public_worker_claim WHERE worker_id=w AND released_at IS NULL)
 THEN RAISE EXCEPTION 'CLAIM_SEQUENCE_DENIED'; END IF;
 SELECT x.* INTO k FROM public.public_worker_work x JOIN public.public_provider_execution e USING(run_id)
 JOIN public.work_runs wr ON wr.work_run_id=e.work_run_id JOIN public.execution_attempts a ON a.execution_attempt_id=e.execution_attempt_id
 JOIN public.public_run pr USING(run_id) JOIN public.public_outbox o USING(run_id)
 WHERE x.closed_at IS NULL AND NOT x.recovery_required AND wr.workflow_state='RUNNING' AND a.status='RUNNING'
 AND pr.state IN('ADMITTED','DISPATCH_STARTED') AND pr.deadline>n AND o.state='BOUND'
 AND NOT EXISTS(SELECT 1 FROM public.public_worker_claim q WHERE q.run_id=x.run_id AND q.released_at IS NULL)
 ORDER BY x.registered_at,x.run_id FOR UPDATE OF x SKIP LOCKED LIMIT 1;
 IF k.run_id IS NULL THEN UPDATE public.public_worker_instance SET last_acquire_seq=seq_value,last_acquire_hash=h,last_result_kind='EMPTY',last_result_claim_id=NULL,last_acquire_at=n WHERE worker_id=w; RETURN jsonb_build_object('kind','EMPTY'); END IF;
 IF k.fence=9223372036854775807 THEN RAISE EXCEPTION 'FENCE_EXHAUSTED'; END IF;
 UPDATE public.public_worker_work SET fence=fence+1 WHERE run_id=k.run_id RETURNING fence INTO k.fence;
 cid:=substring(sha256(k.run_id||w||p||int8send(k.fence)||int8send(seq_value)||h) from 1 for 16);
 INSERT INTO public.public_worker_claim(claim_id,run_id,worker_id,process_generation,fence,acquisition_seq,acquired_action,claimed_at,heartbeat_at,lease_expires_at)
 VALUES(cid,k.run_id,w,p,k.fence,seq_value,'EXECUTE',n,n,n+interval '15 seconds') RETURNING * INTO c;
 SELECT coalesce(max(event_seq),0)+1 INTO ev FROM public.public_worker_claim_event WHERE run_id=k.run_id;
 INSERT INTO public.public_worker_claim_event VALUES(substring(sha256(cid||h) from 1 for 16),k.run_id,cid,ev,'ACQUIRED',NULL,n,NULL,NULL,NULL,h,sha256(cid||h),'{}');
 UPDATE public.public_worker_instance SET last_acquire_seq=seq_value,last_acquire_hash=h,last_result_kind='CLAIM',last_result_claim_id=cid,last_acquire_at=n WHERE worker_id=w;
 RETURN jsonb_build_object('kind','CLAIM','run_id',encode(k.run_id,'hex'),'claim_id',encode(cid,'hex'),'fence',k.fence,'claim_version',1,'lease_expires_at',c.lease_expires_at);
END $$;
-- statement
CREATE FUNCTION public_live_api.worker_renew(c bytea,w bytea,p bytea,f bigint,v bigint) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE n timestamptz; x public.public_worker_claim; deadline_value timestamptz;
BEGIN n:=public_live_api.clock_lock(); SELECT * INTO STRICT x FROM public.public_worker_claim WHERE claim_id=c FOR UPDATE;
 IF x.worker_id<>w OR x.process_generation<>p OR x.fence<>f OR x.claim_version<>v OR x.released_at IS NOT NULL OR x.lease_expires_at<=n
 OR EXISTS(SELECT 1 FROM public.public_worker_work WHERE run_id=x.run_id AND (recovery_required OR closed_at IS NOT NULL))
 THEN RAISE EXCEPTION 'CLAIM_STALE'; END IF;
 SELECT deadline INTO STRICT deadline_value FROM public.public_run WHERE run_id=x.run_id;
 IF deadline_value<=n THEN RAISE EXCEPTION 'CLAIM_DEADLINE'; END IF;
 UPDATE public.public_worker_claim SET heartbeat_at=n,lease_expires_at=least(n+interval '15 seconds',deadline_value),claim_version=claim_version+1 WHERE claim_id=c RETURNING * INTO x;
 RETURN jsonb_build_object('run_id',encode(x.run_id,'hex'),'claim_id',encode(c,'hex'),'fence',x.fence,'claim_version',x.claim_version,'lease_expires_at',x.lease_expires_at);
END $$;
-- statement
CREATE FUNCTION public_live_api.worker_recover_expired(w bytea,p bytea) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE n timestamptz; i public.public_worker_instance; x public.public_worker_claim; recovered integer:=0; quarantined integer:=0;
BEGIN n:=public_live_api.clock_lock(); SELECT * INTO STRICT i FROM public.public_worker_instance WHERE worker_id=w;
 IF i.process_generation<>p THEN RAISE EXCEPTION 'RECOVERY_PRINCIPAL_DENIED'; END IF;
 FOR x IN SELECT * FROM public.public_worker_claim c WHERE c.released_at IS NULL AND c.lease_expires_at<=n
   ORDER BY c.lease_expires_at,c.run_id,c.claim_id FOR UPDATE SKIP LOCKED LIMIT 16 LOOP
  IF EXISTS(SELECT 1 FROM public.public_worker_dispatch_pin d WHERE d.claim_id=x.claim_id AND d.closed_at IS NULL) THEN
   UPDATE public.public_worker_work SET recovery_required=true WHERE run_id=x.run_id;
   quarantined:=quarantined+1;
  ELSE
   UPDATE public.public_worker_claim SET released_at=n,release_reason='LIVE_UNAVAILABLE' WHERE claim_id=x.claim_id;
   recovered:=recovered+1;
  END IF;
 END LOOP;
 RETURN jsonb_build_object('recovered',recovered,'quarantined',quarantined);
END $$;
-- statement
CREATE FUNCTION public_live_api.worker_claim_context(c bytea,w bytea,p bytea,f bigint,v bigint) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE n timestamptz; x public.public_worker_claim; e public.public_provider_execution;
 wr public.work_runs; a public.execution_attempts;
BEGIN n:=public_live_api.clock_lock();
 SELECT * INTO STRICT x FROM public.public_worker_claim WHERE claim_id=c FOR UPDATE;
 IF x.worker_id<>w OR x.process_generation<>p OR x.fence<>f OR x.claim_version<>v
 OR x.released_at IS NOT NULL OR x.lease_expires_at<=n THEN RAISE EXCEPTION 'CLAIM_STALE'; END IF;
 SELECT * INTO STRICT e FROM public.public_provider_execution WHERE run_id=x.run_id;
 SELECT * INTO STRICT wr FROM public.work_runs WHERE work_run_id=e.work_run_id;
 SELECT * INTO STRICT a FROM public.execution_attempts WHERE execution_attempt_id=e.execution_attempt_id;
 IF wr.workflow_state<>'RUNNING' OR a.status<>'RUNNING' OR a.work_run_id<>wr.work_run_id
 OR a.causal_state<>'RUNNING' OR a.causal_state_version<>wr.state_version
 THEN RAISE EXCEPTION 'CLAIM_EXECUTION_STALE'; END IF;
 RETURN jsonb_build_object('run_id',encode(x.run_id,'hex'),'work_run_id',e.work_run_id,
 'execution_attempt_id',e.execution_attempt_id,'state_version',wr.state_version,
 'execution_version',a.execution_version,'fence',x.fence,'claim_version',x.claim_version);
END $$;
-- statement
CREATE FUNCTION public_live_api.worker_bind_operation(c bytea,w bytea,p bytea,f bigint,v bigint,opid varchar) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE n timestamptz; x public.public_worker_claim; link public.public_provider_operation_link; ev bigint; source bytea;
BEGIN n:=public_live_api.clock_lock();
 SELECT * INTO STRICT x FROM public.public_worker_claim WHERE claim_id=c FOR UPDATE;
 IF x.worker_id<>w OR x.process_generation<>p OR x.fence<>f OR x.claim_version<>v
 OR x.released_at IS NOT NULL OR x.lease_expires_at<=n
 THEN RAISE EXCEPTION 'CLAIM_STALE'; END IF;
 SELECT * INTO STRICT link FROM public.public_provider_operation_link WHERE operation_id=opid;
 IF link.run_id<>x.run_id OR (x.current_operation_id IS NOT NULL AND x.current_operation_id<>opid
   AND NOT EXISTS(SELECT 1 FROM public.execution_operations prior
    JOIN public.public_worker_dispatch_pin prior_pin ON prior_pin.operation_id=prior.operation_id
    WHERE prior.operation_id=x.current_operation_id AND prior.current_phase='OUTCOME_KNOWN'
    AND prior_pin.closed_at IS NOT NULL))
 OR NOT EXISTS(SELECT 1 FROM public.execution_operations o JOIN public.public_provider_execution e
   ON e.execution_attempt_id=o.execution_attempt_id WHERE o.operation_id=opid AND e.run_id=x.run_id
   AND o.current_phase IN('PREPARED','SECURITY_ADMITTED'))
 THEN RAISE EXCEPTION 'CLAIM_OPERATION_BIND_DENIED'; END IF;
 UPDATE public.public_worker_claim SET current_operation_id=opid WHERE claim_id=c;
 source:=sha256(c||convert_to(opid,'UTF8')||int8send(f));
 SELECT coalesce(max(event_seq),0)+1 INTO ev FROM public.public_worker_claim_event WHERE run_id=x.run_id;
 INSERT INTO public.public_worker_claim_event VALUES(substring(source from 1 for 16),x.run_id,c,ev,'OPERATION_BOUND',NULL,n,NULL,NULL,opid,source,source,'{}')
 ON CONFLICT(run_id,kind,source_digest) DO NOTHING;
 RETURN jsonb_build_object('operation_id',opid,'claim_id',encode(c,'hex'),'fence',f,'claim_version',v);
END $$;
-- statement
CREATE FUNCTION public_live_api.worker_pin_dispatch(c bytea,w bytea,p bytea,f bigint,v bigint,opid varchar,eventid varchar) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE n timestamptz; x public.public_worker_claim; ev bigint; source bytea;
BEGIN n:=public_live_api.clock_lock();
 SELECT * INTO STRICT x FROM public.public_worker_claim WHERE claim_id=c FOR UPDATE;
 IF x.worker_id<>w OR x.process_generation<>p OR x.fence<>f OR x.claim_version<>v
 OR x.released_at IS NOT NULL OR x.lease_expires_at<=n OR x.current_operation_id<>opid
 OR NOT EXISTS(SELECT 1 FROM public.public_worker_work k WHERE k.run_id=x.run_id AND k.fence=f AND NOT k.recovery_required AND k.closed_at IS NULL)
 OR NOT EXISTS(SELECT 1 FROM public.operation_events e WHERE e.event_id=eventid AND e.operation_id=opid AND e.target_phase='DISPATCH_STARTED')
 OR NOT EXISTS(SELECT 1 FROM public.execution_operations o JOIN public.public_provider_operation_link l USING(operation_id)
   WHERE o.operation_id=opid AND l.run_id=x.run_id AND o.current_phase='DISPATCH_STARTED')
 THEN RAISE EXCEPTION 'CLAIM_DISPATCH_FENCE_DENIED'; END IF;
 INSERT INTO public.public_worker_dispatch_pin(operation_id,claim_id,dispatch_event_id,pinned_at)
 VALUES(opid,c,eventid,n) ON CONFLICT(operation_id) DO NOTHING;
 IF NOT EXISTS(SELECT 1 FROM public.public_worker_dispatch_pin d WHERE d.operation_id=opid AND d.claim_id=c AND d.dispatch_event_id=eventid)
 THEN RAISE EXCEPTION 'DISPATCH_PIN_CONFLICT'; END IF;
 source:=sha256(c||convert_to(opid,'UTF8')||convert_to(eventid,'UTF8'));
 SELECT coalesce(max(event_seq),0)+1 INTO ev FROM public.public_worker_claim_event WHERE run_id=x.run_id;
 INSERT INTO public.public_worker_claim_event VALUES(substring(source from 1 for 16),x.run_id,c,ev,'PINNED',NULL,n,NULL,NULL,opid,source,source,jsonb_build_object('dispatch_event_id',eventid))
 ON CONFLICT(run_id,kind,source_digest) DO NOTHING;
 RETURN jsonb_build_object('operation_id',opid,'dispatch_event_id',eventid,'pinned',true);
END $$;
-- statement
CREATE FUNCTION public_live_api.worker_close_dispatch_pin(opid varchar,eventid varchar,evidence bytea) RETURNS boolean
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE n timestamptz; d public.public_worker_dispatch_pin; x public.public_worker_claim; ev bigint; source bytea;
BEGIN n:=public_live_api.clock_lock();
 SELECT * INTO d FROM public.public_worker_dispatch_pin WHERE operation_id=opid FOR UPDATE;
 IF d.operation_id IS NULL THEN RETURN false; END IF;
 IF d.closed_at IS NOT NULL THEN
  IF d.outcome_event_id=eventid AND d.closure_evidence_digest=evidence THEN RETURN true; END IF;
  RAISE EXCEPTION 'DISPATCH_PIN_CLOSURE_CONFLICT';
 END IF;
 IF octet_length(evidence)<>32 OR NOT EXISTS(SELECT 1 FROM public.operation_events e
  WHERE e.event_id=eventid AND e.operation_id=opid AND e.target_phase='OUTCOME_KNOWN')
 THEN RAISE EXCEPTION 'DISPATCH_PIN_CLOSURE_DENIED'; END IF;
 UPDATE public.public_worker_dispatch_pin SET closed_at=n,closure_evidence_digest=evidence,outcome_event_id=eventid WHERE operation_id=opid;
 SELECT * INTO STRICT x FROM public.public_worker_claim WHERE claim_id=d.claim_id;
 source:=sha256(d.claim_id||convert_to(opid,'UTF8')||convert_to(eventid,'UTF8')||evidence);
 SELECT coalesce(max(event_seq),0)+1 INTO ev FROM public.public_worker_claim_event WHERE run_id=x.run_id;
 INSERT INTO public.public_worker_claim_event VALUES(substring(source from 1 for 16),x.run_id,d.claim_id,ev,'PIN_CLOSED',NULL,n,NULL,NULL,opid,source,source,jsonb_build_object('outcome_event_id',eventid));
 RETURN true;
END $$;
-- statement
CREATE FUNCTION public_live_api.worker_quarantine_dispatch(opid varchar,eventid varchar,evidence bytea) RETURNS boolean
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE n timestamptz; d public.public_worker_dispatch_pin; x public.public_worker_claim; ev bigint; source bytea;
BEGIN n:=public_live_api.clock_lock();
 SELECT * INTO d FROM public.public_worker_dispatch_pin WHERE operation_id=opid FOR UPDATE;
 IF d.operation_id IS NULL THEN RETURN false; END IF;
 IF octet_length(evidence)<>32 OR NOT EXISTS(SELECT 1 FROM public.operation_events e
  WHERE e.event_id=eventid AND e.operation_id=opid AND e.target_phase='OUTCOME_UNKNOWN')
 THEN RAISE EXCEPTION 'DISPATCH_QUARANTINE_DENIED'; END IF;
 SELECT * INTO STRICT x FROM public.public_worker_claim WHERE claim_id=d.claim_id;
 UPDATE public.public_worker_work SET recovery_required=true WHERE run_id=x.run_id;
 source:=sha256(d.claim_id||convert_to(opid,'UTF8')||convert_to(eventid,'UTF8')||evidence);
 SELECT coalesce(max(event_seq),0)+1 INTO ev FROM public.public_worker_claim_event WHERE run_id=x.run_id;
 INSERT INTO public.public_worker_claim_event VALUES(substring(source from 1 for 16),x.run_id,d.claim_id,ev,'QUARANTINED','UNKNOWN_QUARANTINE',n,NULL,NULL,opid,source,source,jsonb_build_object('outcome_event_id',eventid))
 ON CONFLICT(run_id,kind,source_digest) DO NOTHING;
 RETURN true;
END $$;
-- statement
CREATE FUNCTION public_live_api.worker_release(c bytea,w bytea,p bytea,f bigint,v bigint,reason_value text,s bytea) RETURNS void
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE n timestamptz; x public.public_worker_claim; ev bigint;
BEGIN n:=public_live_api.clock_lock(); SELECT * INTO STRICT x FROM public.public_worker_claim WHERE claim_id=c FOR UPDATE;
 IF x.worker_id<>w OR x.process_generation<>p OR x.fence<>f OR x.claim_version<>v OR x.released_at IS NOT NULL OR octet_length(s)<>32
 OR reason_value NOT IN('CLAIM_ONLY_RELEASE','DRAINING','KNOWN_STEP_CLOSED','EXECUTION_TERMINAL','LIVE_UNAVAILABLE')
 OR EXISTS(SELECT 1 FROM public.public_worker_dispatch_pin WHERE claim_id=c AND closed_at IS NULL)
 THEN RAISE EXCEPTION 'CLAIM_RELEASE_DENIED'; END IF;
 UPDATE public.public_worker_claim SET released_at=n,release_reason=reason_value WHERE claim_id=c;
 SELECT coalesce(max(event_seq),0)+1 INTO ev FROM public.public_worker_claim_event WHERE run_id=x.run_id;
 INSERT INTO public.public_worker_claim_event VALUES(substring(sha256(c||s||convert_to(reason_value,'UTF8')) from 1 for 16),x.run_id,c,ev,'RELEASED',reason_value,n,NULL,NULL,NULL,s,sha256(c||s),'{}');
END $$;
"""

RUNTIME = (
    "worker_register_instance(bytea,bytea)",
    "worker_claim_next(bytea,bytea,bigint,bytea)",
    "worker_renew(bytea,bytea,bytea,bigint,bigint)",
    "worker_recover_expired(bytea,bytea)",
    "worker_claim_context(bytea,bytea,bytea,bigint,bigint)",
    "worker_bind_operation(bytea,bytea,bytea,bigint,bigint,character varying)",
    "worker_pin_dispatch(bytea,bytea,bytea,bigint,bigint,character varying,character varying)",
    "worker_close_dispatch_pin(character varying,character varying,bytea)",
    "worker_quarantine_dispatch(character varying,character varying,bytea)",
    "worker_release(bytea,bytea,bytea,bigint,bigint,text,bytea)",
)


def upgrade() -> None:
    for statement in SQL.split("-- statement"):
        if statement.strip():
            op.execute(statement)
    for signature in (*RUNTIME, "worker_enroll(bytea,bytea)"):
        op.execute(f"REVOKE ALL ON FUNCTION public_live_api.{signature} FROM PUBLIC")
    for signature in RUNTIME:
        op.execute(
            f"GRANT EXECUTE ON FUNCTION public_live_api.{signature} TO aiscc_public_live_execution"
        )
    op.execute("GRANT aiscc_public_live_execution TO aiscc_live_worker_login")
    op.execute("GRANT USAGE ON SCHEMA public_live_api TO aiscc_public_live_execution")
    op.execute(
        "GRANT EXECUTE ON FUNCTION public_live_api.execution_link_operation(bytea,integer,"
        "character varying,text,character varying) TO aiscc_public_live_execution"
    )
    op.execute(
        "GRANT EXECUTE ON FUNCTION public_live_api.execution_record_validation("
        "character varying,text,bytea,text),public_live_api.execution_semantic_history(bytea) "
        "TO aiscc_public_live_execution"
    )
    # Exact canonical P1-5 provider lifecycle store.  The worker has no INSERT on
    # WorkRun/attempt and no start-authority table privilege.
    op.execute(
        "GRANT SELECT ON public.work_runs,public.execution_attempts TO aiscc_public_live_execution"
    )
    op.execute(
        "GRANT SELECT,INSERT,UPDATE ON public.execution_operations,public.operation_events,"
        "public.private_provider_protocol_states,public.execution_output_refs,"
        "public.execution_events TO aiscc_public_live_execution"
    )
    op.execute(
        "GRANT UPDATE(status,execution_version,latest_event_sequence,counters,causal_state,"
        "causal_state_version,updated_at) ON public.execution_attempts TO aiscc_public_live_execution"
    )
    op.execute(
        "GRANT USAGE,SELECT ON SEQUENCE public.operation_events_event_sequence_seq,"
        "public.execution_events_event_sequence_seq TO aiscc_public_live_execution"
    )
    op.execute(
        "GRANT EXECUTE ON FUNCTION public_live_api.worker_enroll(bytea,bytea) TO aiscc_public_live_reconciler"
    )
    for table in (
        "public_worker_instance",
        "public_worker_work",
        "public_worker_claim",
        "public_worker_dispatch_pin",
        "public_worker_claim_event",
    ):
        op.execute(
            f"REVOKE ALL ON public.{table} FROM PUBLIC,aiscc_public_live_runtime,aiscc_public_live_reconciler,aiscc_public_live_execution"
        )


def downgrade() -> None:
    for signature in (*RUNTIME, "worker_enroll(bytea,bytea)"):
        op.execute(f"DROP FUNCTION public_live_api.{signature}")
    op.execute("DROP TABLE public.public_worker_claim_event")
    op.execute("DROP TABLE public.public_worker_dispatch_pin")
    op.execute(
        "ALTER TABLE public.public_worker_instance DROP CONSTRAINT public_worker_instance_last_claim_fk"
    )
    op.execute("DROP TABLE public.public_worker_claim")
    op.execute("DROP TABLE public.public_worker_work")
    op.execute("DROP TABLE public.public_worker_instance")
