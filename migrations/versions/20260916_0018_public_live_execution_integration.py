# ruff: noqa: E501
"""Bind Public Live semantic requests to the canonical P1-5 lifecycle."""

from alembic import op

revision = "20260916_0018"
down_revision = "20260916_0017"
branch_labels = None
depends_on = None

SQL = r"""
CREATE TABLE public.public_provider_execution (
 run_id bytea PRIMARY KEY REFERENCES public.public_run(run_id) ON DELETE RESTRICT,
 work_run_id varchar(128) NOT NULL UNIQUE REFERENCES public.work_runs(work_run_id) ON DELETE RESTRICT,
 execution_attempt_id varchar(128) NOT NULL UNIQUE REFERENCES public.execution_attempts(execution_attempt_id) ON DELETE RESTRICT,
 binding_digest bytea NOT NULL CHECK(octet_length(binding_digest)=32),
 bound_at timestamptz NOT NULL,
 CHECK(work_run_id='public-live-'||encode(run_id,'hex'))
);
-- statement
CREATE TABLE public.public_semantic_plan (
 run_id bytea PRIMARY KEY REFERENCES public.public_provider_execution(run_id) ON DELETE RESTRICT,
 execution_attempt_id varchar(128) NOT NULL UNIQUE REFERENCES public.execution_attempts(execution_attempt_id) ON DELETE RESTRICT,
 plan_version text NOT NULL DEFAULT 'PUBLIC_LIVE_SEMANTIC_PLAN_V1' CHECK(plan_version='PUBLIC_LIVE_SEMANTIC_PLAN_V1'),
 plan_digest bytea NOT NULL UNIQUE CHECK(octet_length(plan_digest)=32),
 profile text NOT NULL DEFAULT 'public-live-luna-v1' CHECK(profile='public-live-luna-v1'),
 profile_version integer NOT NULL DEFAULT 1 CHECK(profile_version=1),
 phase_maximum integer NOT NULL DEFAULT 3 CHECK(phase_maximum=3),
 retry_maximum integer NOT NULL DEFAULT 1 CHECK(retry_maximum=1),
 physical_maximum integer NOT NULL DEFAULT 4 CHECK(physical_maximum=4),
 created_at timestamptz NOT NULL
);
-- statement
CREATE TABLE public.public_provider_operation_link (
 operation_id varchar(128) PRIMARY KEY REFERENCES public.execution_operations(operation_id) ON DELETE RESTRICT,
 run_id bytea NOT NULL REFERENCES public.public_provider_execution(run_id) ON DELETE RESTRICT,
 request_ordinal integer NOT NULL,
 semantic_role text NOT NULL CHECK(semantic_role IN ('PRIMARY','VERIFY','CORRECT')),
 retry_of_operation_id varchar(128) REFERENCES public.execution_operations(operation_id) ON DELETE RESTRICT,
 linked_at timestamptz NOT NULL,
 UNIQUE(run_id,request_ordinal)
);
-- statement
CREATE TABLE public.public_provider_semantic_validation(
 operation_id varchar(128) PRIMARY KEY REFERENCES public.public_provider_operation_link(operation_id) ON DELETE RESTRICT,
 decision text NOT NULL CHECK(decision IN('COMPLETE','VERIFY_REQUIRED','CORRECTABLE_DEFECT','UNSAFE_OR_UNCORRECTABLE')),
 proof bytea NOT NULL CHECK(octet_length(proof)=32),defect_ref text,created_at timestamptz NOT NULL,
 CHECK((decision='CORRECTABLE_DEFECT')=(defect_ref IS NOT NULL))
);
-- statement
CREATE FUNCTION public_live_api.execution_bind(
 r bytea,w varchar,a varchar,d bytea,p bytea
) RETURNS jsonb LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE n timestamptz; old public.public_provider_execution; wr public.work_runs; ea public.execution_attempts;
BEGIN
 n:=public_live_api.clock_lock();
 IF octet_length(r)<>16 OR octet_length(d)<>32 OR octet_length(p)<>32
 THEN RAISE EXCEPTION 'EXECUTION_BINDING_INVALID'; END IF;
 SELECT * INTO wr FROM public.work_runs WHERE work_run_id=w FOR UPDATE;
 SELECT * INTO ea FROM public.execution_attempts WHERE execution_attempt_id=a FOR UPDATE;
 IF wr.work_run_id IS NULL OR ea.execution_attempt_id IS NULL OR ea.work_run_id<>w
 OR wr.workflow_state<>'RUNNING' OR ea.status<>'RUNNING'
 OR wr.runtime_mode<>'PUBLIC_BOUNDED_LIVE' OR ea.runtime_mode<>'PUBLIC_BOUNDED_LIVE'
 OR wr.state_version<>ea.causal_state_version
 OR NOT EXISTS(SELECT 1 FROM public.public_run x JOIN public.public_outbox o USING(run_id)
   WHERE x.run_id=r AND x.owner_binding=w AND x.state='ADMITTED' AND x.deadline>n AND o.state='BOUND')
 OR EXISTS(SELECT 1 FROM public.execution_operations x WHERE x.execution_attempt_id=a)
 THEN RAISE EXCEPTION 'EXECUTION_BINDING_DENIED'; END IF;
 SELECT * INTO old FROM public.public_provider_execution WHERE run_id=r;
 IF old.run_id IS NOT NULL THEN
  IF old.work_run_id=w AND old.execution_attempt_id=a AND old.binding_digest=d
  THEN RETURN jsonb_build_object('run_id',encode(r,'hex'),'work_run_id',w,'execution_attempt_id',a); END IF;
  RAISE EXCEPTION 'EXECUTION_BINDING_CONFLICT';
 END IF;
 INSERT INTO public.public_provider_execution VALUES(r,w,a,d,n);
 INSERT INTO public.public_semantic_plan(run_id,execution_attempt_id,plan_digest,created_at)
 VALUES(r,a,p,n);
 RETURN jsonb_build_object('run_id',encode(r,'hex'),'work_run_id',w,'execution_attempt_id',a);
END $$;
-- statement
CREATE FUNCTION public_live_api.execution_context(r bytea) RETURNS jsonb
LANGUAGE sql SECURITY DEFINER SET search_path=pg_catalog AS $$
 SELECT CASE WHEN e.run_id IS NULL THEN NULL ELSE jsonb_build_object(
  'run_id',encode(e.run_id,'hex'),'work_run_id',e.work_run_id,
  'execution_attempt_id',e.execution_attempt_id,'binding_digest',encode(e.binding_digest,'hex'),
  'plan_digest',encode(p.plan_digest,'hex')) END
 FROM public.public_provider_execution e JOIN public.public_semantic_plan p USING(run_id)
 WHERE e.run_id=r
$$;
-- statement
CREATE FUNCTION public_live_api.execution_link_operation(
 r bytea,o integer,opid varchar,role_name text,retry_op varchar
) RETURNS void LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE e public.public_provider_execution; x public.execution_operations; parent public.public_provider_operation_link;
BEGIN
 SELECT * INTO STRICT e FROM public.public_provider_execution WHERE run_id=r;
 SELECT * INTO STRICT x FROM public.execution_operations WHERE operation_id=opid FOR UPDATE;
 IF x.execution_attempt_id<>e.execution_attempt_id OR x.operation_kind<>'PROVIDER'
 OR x.call_ordinal<>o OR role_name NOT IN('PRIMARY','VERIFY','CORRECT')
 OR (retry_op IS NOT NULL)<>(EXISTS(SELECT 1 FROM public.public_provider_operation_link z WHERE z.operation_id=retry_op))
 THEN RAISE EXCEPTION 'OPERATION_LINK_DENIED'; END IF;
 IF retry_op IS NOT NULL THEN
  SELECT * INTO STRICT parent FROM public.public_provider_operation_link WHERE operation_id=retry_op;
  IF parent.run_id<>r OR parent.semantic_role<>role_name OR parent.request_ordinal>=o
  THEN RAISE EXCEPTION 'OPERATION_RETRY_LINK_DENIED'; END IF;
 END IF;
 INSERT INTO public.public_provider_operation_link VALUES(opid,r,o,role_name,retry_op,public_live_api.clock_lock())
 ON CONFLICT(operation_id) DO NOTHING;
 IF NOT EXISTS(SELECT 1 FROM public.public_provider_operation_link WHERE operation_id=opid
 AND run_id=r AND request_ordinal=o AND semantic_role=role_name
 AND retry_of_operation_id IS NOT DISTINCT FROM retry_op)
 THEN RAISE EXCEPTION 'OPERATION_LINK_CONFLICT'; END IF;
END $$;
-- statement
CREATE FUNCTION public_live_api.execution_record_validation(opid varchar,decision_value text,proof_value bytea,defect_value text) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE n timestamptz; link public.public_provider_operation_link; old public.public_provider_semantic_validation;
BEGIN n:=public_live_api.clock_lock(); SELECT * INTO STRICT link FROM public.public_provider_operation_link WHERE operation_id=opid;
 IF octet_length(proof_value)<>32 OR decision_value NOT IN('COMPLETE','VERIFY_REQUIRED','CORRECTABLE_DEFECT','UNSAFE_OR_UNCORRECTABLE')
 OR (decision_value='CORRECTABLE_DEFECT')<>(defect_value IS NOT NULL)
 OR (decision_value='VERIFY_REQUIRED' AND link.semantic_role<>'PRIMARY')
 OR (decision_value='CORRECTABLE_DEFECT' AND link.semantic_role NOT IN('PRIMARY','VERIFY'))
 OR NOT EXISTS(SELECT 1 FROM public.execution_operations o WHERE o.operation_id=opid
   AND o.current_phase='OUTCOME_KNOWN' AND o.outcome='PROVIDER_COMPLETED')
 THEN RAISE EXCEPTION 'SEMANTIC_VALIDATION_DENIED'; END IF;
 SELECT * INTO old FROM public.public_provider_semantic_validation WHERE operation_id=opid;
 IF old.operation_id IS NOT NULL THEN
  IF old.decision=decision_value AND old.proof=proof_value AND old.defect_ref IS NOT DISTINCT FROM defect_value
  THEN RETURN jsonb_build_object('operation_id',opid,'decision',old.decision); END IF;
  RAISE EXCEPTION 'SEMANTIC_VALIDATION_CONFLICT';
 END IF;
 INSERT INTO public.public_provider_semantic_validation VALUES(opid,decision_value,proof_value,defect_value,n);
 RETURN jsonb_build_object('operation_id',opid,'decision',decision_value);
END $$;
-- statement
CREATE FUNCTION public_live_api.execution_semantic_history(r bytea) RETURNS jsonb
LANGUAGE sql SECURITY DEFINER SET search_path=pg_catalog AS $$
 SELECT coalesce(jsonb_agg(jsonb_build_object(
  'operation_id',l.operation_id,'role',l.semantic_role,'semantic_ordinal',
   CASE l.semantic_role WHEN 'PRIMARY' THEN 1 WHEN 'VERIFY' THEN 2 ELSE 3 END,
  'retry_of_operation_id',l.retry_of_operation_id,'outcome',
   CASE WHEN o.outcome='PROVIDER_COMPLETED' THEN 'KNOWN_SUCCESS'
        WHEN o.outcome='DEFINITELY_NOT_SENT' THEN 'KNOWN_FAILURE' ELSE 'UNKNOWN' END,
  'closed_failure',o.outcome='DEFINITELY_NOT_SENT','validation_decision',v.decision,
  'validation_proof',CASE WHEN v.proof IS NULL THEN NULL ELSE encode(v.proof,'hex') END,
  'defect_ref',v.defect_ref) ORDER BY l.request_ordinal),'[]'::jsonb)
 FROM public.public_provider_operation_link l JOIN public.execution_operations o USING(operation_id)
 LEFT JOIN public.public_provider_semantic_validation v USING(operation_id) WHERE l.run_id=r
$$;
"""


def upgrade() -> None:
    for statement in SQL.split("-- statement"):
        if statement.strip():
            op.execute(statement)
    for signature in (
        "execution_bind(bytea,character varying,character varying,bytea,bytea)",
        "execution_context(bytea)",
        "execution_link_operation(bytea,integer,character varying,text,character varying)",
        "execution_record_validation(character varying,text,bytea,text)",
        "execution_semantic_history(bytea)",
    ):
        op.execute(f"REVOKE ALL ON FUNCTION public_live_api.{signature} FROM PUBLIC")
    op.execute(
        "GRANT EXECUTE ON FUNCTION public_live_api.execution_context(bytea) "
        "TO aiscc_public_live_runtime,aiscc_public_live_reconciler"
    )
    op.execute(
        "GRANT EXECUTE ON FUNCTION public_live_api.execution_bind(bytea,character varying,"
        "character varying,bytea,bytea) TO aiscc_public_live_reconciler"
    )
    for table in (
        "public_provider_execution",
        "public_semantic_plan",
        "public_provider_operation_link",
        "public_provider_semantic_validation",
    ):
        op.execute(
            f"REVOKE ALL ON public.{table} FROM PUBLIC,aiscc_public_live_runtime,"
            "aiscc_public_live_reconciler"
        )


def downgrade() -> None:
    op.execute("DROP FUNCTION public_live_api.execution_semantic_history(bytea)")
    op.execute("DROP FUNCTION public_live_api.execution_record_validation(varchar,text,bytea,text)")
    op.execute(
        "DROP FUNCTION public_live_api.execution_link_operation(bytea,integer,varchar,text,varchar)"
    )
    op.execute("DROP FUNCTION public_live_api.execution_context(bytea)")
    op.execute("DROP FUNCTION public_live_api.execution_bind(bytea,varchar,varchar,bytea,bytea)")
    op.execute("DROP TABLE public.public_provider_semantic_validation")
    op.execute("DROP TABLE public.public_provider_operation_link")
    op.execute("DROP TABLE public.public_semantic_plan")
    op.execute("DROP TABLE public.public_provider_execution")
