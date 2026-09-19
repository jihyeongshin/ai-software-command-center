# ruff: noqa: E501
"""Close the Public Live projection from canonical P1-5 successful execution truth."""

from alembic import op

revision = "20260919_0027"
down_revision = "20260919_0026"
branch_labels = None
depends_on = None

LIABILITY = "((8000::bigint*250000+2000::bigint*1200000+999999)/1000000)"
PROVIDER_RESOURCE = (
    "public-live-luna-v1:1:openai:"
    "e33230db3dd7d2f0153debcbb9fabc3386faac005477571931af855d70c4ae9b:responses-v1"
)
TOOL_RESOURCE = "aiscc-stockroom-tools:2:stockroom_summary:1:stockroom-summary-v1"

SQL = rf"""
CREATE FUNCTION public_live_api.successful_execution_reconciliation_candidates() RETURNS jsonb
LANGUAGE sql SECURITY DEFINER SET search_path=pg_catalog AS $$
 SELECT coalesce(jsonb_agg(jsonb_build_object(
  'run_id',encode(r.run_id,'hex'),'execution_attempt_id',a.execution_attempt_id,
  'provider_request_count',(SELECT count(*) FROM public.public_provider_operation_link l WHERE l.run_id=r.run_id),
  'physical_provider_send_count',(SELECT count(*) FROM public.execution_operations o JOIN public.operation_events e USING(operation_id)
    WHERE o.execution_attempt_id=a.execution_attempt_id AND o.operation_kind='PROVIDER' AND e.target_phase='DISPATCH_STARTED'),
  'tool_operation_count',(SELECT count(*) FROM public.execution_operations o WHERE o.execution_attempt_id=a.execution_attempt_id AND o.operation_kind='TOOL'),
  'liability_micro',(SELECT count(*)*{LIABILITY} FROM public.execution_operations o JOIN public.operation_events e USING(operation_id)
    WHERE o.execution_attempt_id=a.execution_attempt_id AND o.operation_kind='PROVIDER' AND e.target_phase='DISPATCH_STARTED')
 ) ORDER BY encode(r.run_id,'hex')),'[]'::jsonb)
 FROM public.public_run r
 JOIN public.public_reservation z USING(run_id)
 JOIN public.public_outbox b USING(run_id)
 JOIN public.public_worker_work w USING(run_id)
 JOIN public.public_semantic_plan s USING(run_id)
 JOIN public.public_provider_execution x USING(run_id)
 JOIN public.execution_attempts a ON a.execution_attempt_id=x.execution_attempt_id
 JOIN public.work_runs wr ON wr.work_run_id=x.work_run_id
 JOIN public.public_campaign c ON c.campaign_id=r.campaign_id
 WHERE r.state='ADMITTED' AND z.state='HELD' AND z.amount=200000
 AND z.committed_max=0 AND z.settled_cost IS NULL AND b.state='BOUND'
 AND w.closed_at IS NULL AND NOT w.recovery_required
 AND c.scenario_id='stockroom-s1-normal' AND c.scenario_version='1.0.0'
 AND s.profile='public-live-luna-v1' AND s.profile_version=1
 AND s.phase_maximum=3 AND s.retry_maximum=1 AND s.physical_maximum=4
 AND x.work_run_id=r.owner_binding AND a.work_run_id=x.work_run_id
 AND a.provider_profile_id='public-live-luna-v1' AND a.provider_profile_version='1'
 AND a.status='EXECUTOR_COMPLETED' AND wr.workflow_state='RUNNING'
 AND (SELECT count(*) FROM public.execution_events e WHERE e.execution_attempt_id=a.execution_attempt_id
   AND e.status_after='EXECUTOR_COMPLETED' AND e.refs ? 'agent_output_ref'
   AND e.refs ? 'execution_submission_ref' AND e.refs ? 'execution_submission_hash'
   AND e.refs ? 'execution_submission_storage_ref')=1
 AND (SELECT count(*) FROM public.execution_output_refs o WHERE o.execution_attempt_id=a.execution_attempt_id
   AND o.ref_kind='AgentOutputRef' AND length(o.content_hash)=64
   AND o.storage_ref='private://agent-output/'||o.output_ref_id
   AND EXISTS(SELECT 1 FROM public.execution_events e WHERE e.execution_attempt_id=a.execution_attempt_id
     AND e.status_after='EXECUTOR_COMPLETED' AND e.refs->>'agent_output_ref'=o.output_ref_id))=1
 AND (SELECT count(*) FROM public.public_provider_operation_link l WHERE l.run_id=r.run_id) BETWEEN 1 AND 4
 AND (SELECT count(*) FROM public.execution_operations o WHERE o.execution_attempt_id=a.execution_attempt_id AND o.operation_kind='TOOL') BETWEEN 0 AND 1
 AND (SELECT count(*) FROM public.execution_operations o WHERE o.execution_attempt_id=a.execution_attempt_id)=
   (SELECT count(*) FROM public.public_provider_operation_link l WHERE l.run_id=r.run_id)+
   (SELECT count(*) FROM public.execution_operations o WHERE o.execution_attempt_id=a.execution_attempt_id AND o.operation_kind='TOOL')
 AND NOT EXISTS(SELECT 1 FROM public.execution_operations o WHERE o.execution_attempt_id=a.execution_attempt_id
   AND (o.operation_kind NOT IN('PROVIDER','TOOL') OR o.current_phase<>'OUTCOME_KNOWN'))
 AND NOT EXISTS(SELECT 1 FROM public.execution_operations o LEFT JOIN public.public_provider_operation_link l USING(operation_id)
   WHERE o.execution_attempt_id=a.execution_attempt_id AND o.operation_kind='PROVIDER'
   AND (l.run_id IS DISTINCT FROM r.run_id OR o.resource_identity<>'{PROVIDER_RESOURCE}'
    OR o.outcome NOT IN('PROVIDER_COMPLETED','DEFINITELY_NOT_SENT')))
 AND NOT EXISTS(SELECT 1 FROM public.execution_operations o WHERE o.execution_attempt_id=a.execution_attempt_id
   AND o.operation_kind='TOOL' AND (o.resource_identity<>'{TOOL_RESOURCE}' OR o.outcome<>'TOOL_COMPLETED'))
 AND NOT EXISTS(SELECT 1 FROM public.operation_events e JOIN public.execution_operations o USING(operation_id)
   WHERE o.execution_attempt_id=a.execution_attempt_id AND e.target_phase='OUTCOME_UNKNOWN')
 AND NOT EXISTS(SELECT 1 FROM public.execution_operations o WHERE o.execution_attempt_id=a.execution_attempt_id
   AND o.operation_kind='PROVIDER' AND ((o.outcome='PROVIDER_COMPLETED' AND
      ((SELECT count(*) FROM public.operation_events e WHERE e.operation_id=o.operation_id AND e.target_phase='DISPATCH_STARTED')<>1 OR
       (SELECT count(*) FROM public.operation_events e WHERE e.operation_id=o.operation_id AND e.target_phase='OUTCOME_KNOWN' AND e.outcome='PROVIDER_COMPLETED')<>1))
    OR (o.outcome='DEFINITELY_NOT_SENT' AND
      ((SELECT count(*) FROM public.operation_events e WHERE e.operation_id=o.operation_id AND e.target_phase='DISPATCH_STARTED')<>0 OR
       (SELECT count(*) FROM public.operation_events e WHERE e.operation_id=o.operation_id AND e.target_phase='OUTCOME_KNOWN' AND e.outcome='DEFINITELY_NOT_SENT')<>1))))
 AND NOT EXISTS(SELECT 1 FROM public.execution_operations o WHERE o.execution_attempt_id=a.execution_attempt_id
   AND o.operation_kind='TOOL' AND ((SELECT count(*) FROM public.operation_events e WHERE e.operation_id=o.operation_id AND e.target_phase='DISPATCH_STARTED')<>1
    OR (SELECT count(*) FROM public.operation_events e WHERE e.operation_id=o.operation_id AND e.target_phase='OUTCOME_KNOWN' AND e.outcome='TOOL_COMPLETED')<>1))
 AND (SELECT count(*) FROM public.public_worker_claim q WHERE q.run_id=r.run_id AND q.released_at IS NULL)=0
 AND (SELECT count(*) FROM public.public_worker_dispatch_pin p JOIN public.public_worker_claim q USING(claim_id)
   WHERE q.run_id=r.run_id AND p.closed_at IS NULL)=0
 AND (SELECT count(*) FROM public.public_worker_dispatch_pin p JOIN public.public_worker_claim q USING(claim_id)
   WHERE q.run_id=r.run_id)=(SELECT count(*) FROM public.execution_operations o JOIN public.operation_events e USING(operation_id)
     WHERE o.execution_attempt_id=a.execution_attempt_id AND o.operation_kind='PROVIDER' AND e.target_phase='DISPATCH_STARTED')
 AND NOT EXISTS(SELECT 1 FROM public.public_worker_dispatch_pin p JOIN public.public_worker_claim q USING(claim_id)
   JOIN public.execution_operations o USING(operation_id) WHERE q.run_id=r.run_id
   AND (p.closed_at IS NULL OR p.outcome_event_id IS NULL OR o.outcome<>'PROVIDER_COMPLETED'))
 AND (SELECT count(*) FROM public.public_provider_operation_link l JOIN public.execution_operations o USING(operation_id)
   JOIN public.public_provider_semantic_validation v USING(operation_id)
   WHERE l.run_id=r.run_id AND o.call_ordinal=(SELECT max(z.call_ordinal) FROM public.execution_operations z
    WHERE z.execution_attempt_id=a.execution_attempt_id AND z.operation_kind='PROVIDER')
   AND o.outcome='PROVIDER_COMPLETED' AND v.decision='COMPLETE')=1
 AND NOT EXISTS(SELECT 1 FROM public.public_provider_semantic_validation v JOIN public.public_provider_operation_link l USING(operation_id)
   WHERE l.run_id=r.run_id AND v.decision='UNSAFE_OR_UNCORRECTABLE')
 AND (SELECT count(*) FROM public.public_provider_operation_link l WHERE l.run_id=r.run_id AND l.retry_of_operation_id IS NOT NULL)<=1
 AND NOT EXISTS(SELECT 1 FROM public.public_provider_operation_link l JOIN public.public_provider_operation_link p
   ON p.operation_id=l.retry_of_operation_id JOIN public.execution_operations po ON po.operation_id=p.operation_id
   WHERE l.run_id=r.run_id AND l.retry_of_operation_id IS NOT NULL
   AND (p.run_id<>r.run_id OR p.semantic_role<>l.semantic_role OR p.request_ordinal>=l.request_ordinal OR po.outcome<>'DEFINITELY_NOT_SENT'))
 AND NOT EXISTS(SELECT 1 FROM public.public_provider_operation_link l JOIN public.execution_operations o USING(operation_id)
   WHERE l.run_id=r.run_id AND o.outcome='DEFINITELY_NOT_SENT'
   AND (SELECT count(*) FROM public.public_provider_operation_link z WHERE z.retry_of_operation_id=l.operation_id)<>1)
 AND (SELECT l.semantic_role FROM public.public_provider_operation_link l WHERE l.run_id=r.run_id ORDER BY l.request_ordinal LIMIT 1)='PRIMARY'
 AND NOT EXISTS(SELECT 1 FROM public.public_provider_operation_link l WHERE l.run_id=r.run_id AND l.semantic_role='VERIFY'
   AND NOT EXISTS(SELECT 1 FROM public.public_provider_operation_link p JOIN public.public_provider_semantic_validation v USING(operation_id)
     WHERE p.run_id=r.run_id AND p.request_ordinal<l.request_ordinal AND p.semantic_role='PRIMARY' AND v.decision='VERIFY_REQUIRED'))
 AND NOT EXISTS(SELECT 1 FROM public.public_provider_operation_link l WHERE l.run_id=r.run_id AND l.semantic_role='CORRECT'
   AND NOT EXISTS(SELECT 1 FROM public.public_provider_operation_link p JOIN public.public_provider_semantic_validation v USING(operation_id)
     WHERE p.run_id=r.run_id AND p.request_ordinal<l.request_ordinal AND p.semantic_role IN('PRIMARY','VERIFY') AND v.decision='CORRECTABLE_DEFECT'))
 AND (SELECT count(*) FROM public.public_slot q WHERE q.run_id=r.run_id AND q.state='OCCUPIED')=1
 AND NOT EXISTS(SELECT 1 FROM public.public_dispatch d WHERE d.run_id=r.run_id)
 AND NOT EXISTS(SELECT 1 FROM public.public_money_event m WHERE m.run_id=r.run_id AND m.event_kind='SETTLE')
 AND EXISTS(SELECT 1 FROM public.public_campaign q WHERE q.campaign_id=r.campaign_id AND q.available+q.held+q.settled=q.limit_micro)
 AND EXISTS(SELECT 1 FROM public.public_day d WHERE d.campaign_id=r.campaign_id AND d.utc_date=r.utc_date AND d.available+d.held+d.settled=d.limit_micro)
$$;
-- statement
CREATE FUNCTION public_live_api.complete_successful_execution_run(r bytea) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE n timestamptz; run public.public_run; reservation public.public_reservation;
 outbox public.public_outbox; work public.public_worker_work; plan public.public_semantic_plan;
 execution public.public_provider_execution; attempt public.execution_attempts; wr public.work_runs;
 completion public.execution_events; output public.execution_output_refs; latest_claim public.public_worker_claim;
 prior public.public_money_event; provider_count bigint; send_count bigint; tool_count bigint;
 liability bigint; proof bytea; source bytea; seq bigint; evidence_text text; candidate jsonb;
BEGIN
 n:=public_live_api.clock_lock();
 SELECT * INTO STRICT run FROM public.public_run WHERE run_id=r FOR UPDATE;
 SELECT * INTO STRICT reservation FROM public.public_reservation WHERE run_id=r FOR UPDATE;
 SELECT * INTO STRICT outbox FROM public.public_outbox WHERE run_id=r FOR UPDATE;
 SELECT * INTO STRICT work FROM public.public_worker_work WHERE run_id=r FOR UPDATE;
 SELECT * INTO STRICT plan FROM public.public_semantic_plan WHERE run_id=r;
 SELECT * INTO STRICT execution FROM public.public_provider_execution WHERE run_id=r;
 SELECT * INTO STRICT attempt FROM public.execution_attempts WHERE execution_attempt_id=execution.execution_attempt_id;
 SELECT * INTO STRICT wr FROM public.work_runs WHERE work_run_id=execution.work_run_id;
 SELECT * INTO STRICT completion FROM public.execution_events WHERE execution_attempt_id=attempt.execution_attempt_id
   AND status_after='EXECUTOR_COMPLETED' AND refs ? 'agent_output_ref' AND refs ? 'execution_submission_ref'
   AND refs ? 'execution_submission_hash' AND refs ? 'execution_submission_storage_ref';
 SELECT * INTO STRICT output FROM public.execution_output_refs WHERE execution_attempt_id=attempt.execution_attempt_id
   AND ref_kind='AgentOutputRef' AND output_ref_id=completion.refs->>'agent_output_ref';
 SELECT count(*) INTO provider_count FROM public.public_provider_operation_link WHERE run_id=r;
 SELECT count(*) INTO tool_count FROM public.execution_operations WHERE execution_attempt_id=attempt.execution_attempt_id AND operation_kind='TOOL';
 SELECT count(*) INTO send_count FROM public.execution_operations o JOIN public.operation_events e USING(operation_id)
   WHERE o.execution_attempt_id=attempt.execution_attempt_id AND o.operation_kind='PROVIDER' AND e.target_phase='DISPATCH_STARTED';
 liability:=send_count*{LIABILITY};
 SELECT string_agg(o.call_ordinal::text||':'||o.operation_id||':'||o.operation_kind||':'||o.outcome||':'||
   coalesce((SELECT string_agg(e.event_id,',' ORDER BY e.event_sequence) FROM public.operation_events e
    WHERE e.operation_id=o.operation_id AND e.target_phase IN('DISPATCH_STARTED','OUTCOME_KNOWN')),''),'|' ORDER BY o.call_ordinal)
 INTO evidence_text FROM public.execution_operations o WHERE o.execution_attempt_id=attempt.execution_attempt_id;
 proof:=sha256(convert_to('P1_5_PUBLIC_LIVE_SUCCESS_RECONCILIATION_V1|'||encode(r,'hex')||'|'||
   attempt.execution_attempt_id||'|'||completion.event_id||'|'||output.output_ref_id||'|'||output.content_hash||'|'||
   coalesce(evidence_text,'')||'|'||liability::text,'UTF8'));

 SELECT * INTO prior FROM public.public_money_event WHERE run_id=r AND event_kind='SETTLE';
 IF FOUND THEN
  IF run.state<>'COMPLETED' OR reservation.state<>'SETTLED' OR reservation.settled_cost<>liability
   OR prior.cost<>liability OR prior.evidence_digest<>proof OR outbox.state<>'CLOSED'
   OR work.closed_at IS NULL OR work.close_reason<>'SUCCESS_RECONCILED'
   OR EXISTS(SELECT 1 FROM public.public_slot WHERE run_id=r)
  THEN RAISE EXCEPTION 'SUCCESS_RECONCILIATION_REPLAY_CONFLICT'; END IF;
  RETURN jsonb_build_object('run_id',encode(r,'hex'),'execution_attempt_id',attempt.execution_attempt_id,
   'provider_request_count',provider_count,'physical_provider_send_count',send_count,
   'tool_operation_count',tool_count,'liability_micro',liability,'evidence_digest',encode(proof,'hex'),
   'state',run.state,'reconciled',false);
 END IF;

 SELECT item INTO candidate FROM jsonb_array_elements(public_live_api.successful_execution_reconciliation_candidates()) item
  WHERE item->>'run_id'=encode(r,'hex');
 IF candidate IS NULL OR candidate->>'execution_attempt_id'<>attempt.execution_attempt_id
  OR (candidate->>'provider_request_count')::bigint<>provider_count
  OR (candidate->>'physical_provider_send_count')::bigint<>send_count
  OR (candidate->>'tool_operation_count')::bigint<>tool_count
  OR (candidate->>'liability_micro')::bigint<>liability
  OR output.storage_ref<>'private://agent-output/'||output.output_ref_id OR length(output.content_hash)<>64
  OR length(completion.refs->>'execution_submission_ref')=0
  OR length(completion.refs->>'execution_submission_hash')<>64
  OR completion.refs->>'execution_submission_storage_ref'<>'private://execution-submission/'||(completion.refs->>'execution_submission_ref')
  OR liability<=0 OR liability>reservation.amount
 THEN RAISE EXCEPTION 'SUCCESS_RECONCILIATION_PREDICATE_DENIED'; END IF;

 source:=sha256(convert_to('successful-execution-closure-v1','UTF8')||r||proof);
 INSERT INTO public.public_observation VALUES(substring(source from 1 for 16),r,NULL,source,'CLOSURE',proof,n,liability);
 INSERT INTO public.public_money_event VALUES(r,'SETTLE',200000,liability,200000-liability,run.campaign_id,run.utc_date,proof,n);
 UPDATE public.public_campaign SET held=held-200000,settled=settled+liability,available=available+200000-liability
   WHERE campaign_id=run.campaign_id;
 UPDATE public.public_day SET held=held-200000,settled=settled+liability,available=available+200000-liability
   WHERE campaign_id=run.campaign_id AND utc_date=run.utc_date;
 UPDATE public.public_reservation SET committed_max=liability,settled_cost=liability,state='SETTLED' WHERE run_id=r;
 UPDATE public.public_slot SET run_id=NULL,state='FREE',generation=generation+1,heartbeat_at=NULL,expires_at=NULL WHERE run_id=r;
 UPDATE public.public_outbox SET state='CLOSED',generation=generation+1,fenced_at=n WHERE run_id=r;
 UPDATE public.public_worker_work SET closed_at=n,close_reason='SUCCESS_RECONCILED' WHERE run_id=r;
 SELECT * INTO STRICT latest_claim FROM public.public_worker_claim WHERE run_id=r ORDER BY fence DESC LIMIT 1;
 source:=sha256(r||proof||convert_to('SUCCESS_RECONCILED','UTF8'));
 SELECT coalesce(max(event_seq),0)+1 INTO seq FROM public.public_worker_claim_event WHERE run_id=r;
 INSERT INTO public.public_worker_claim_event VALUES(substring(source from 1 for 16),r,latest_claim.claim_id,seq,
  'CLOSED','SUCCESS_RECONCILED',n,NULL,NULL,NULL,source,source,
  jsonb_build_object('execution_attempt_id',attempt.execution_attempt_id,'completion_event_id',completion.event_id,
   'provider_request_count',provider_count,'physical_provider_send_count',send_count,'tool_operation_count',tool_count));
 UPDATE public.public_run SET state='COMPLETED',version=version+1 WHERE run_id=r;
 source:=sha256(convert_to('completed-successful-execution-v1','UTF8')||r||proof);
 INSERT INTO public.public_observation VALUES(substring(source from 1 for 16),r,NULL,source,'USAGE',proof,n,NULL);
 IF NOT EXISTS(SELECT 1 FROM public.public_campaign c WHERE c.campaign_id=run.campaign_id AND c.available+c.held+c.settled=c.limit_micro)
  OR NOT EXISTS(SELECT 1 FROM public.public_day d WHERE d.campaign_id=run.campaign_id AND d.utc_date=run.utc_date AND d.available+d.held+d.settled=d.limit_micro)
 THEN RAISE EXCEPTION 'SUCCESS_LEDGER_CONSERVATION_REGRESSION'; END IF;
 RETURN jsonb_build_object('run_id',encode(r,'hex'),'execution_attempt_id',attempt.execution_attempt_id,
  'provider_request_count',provider_count,'physical_provider_send_count',send_count,
  'tool_operation_count',tool_count,'liability_micro',liability,'evidence_digest',encode(proof,'hex'),
  'state','COMPLETED','reconciled',true);
END $$;
"""

FUNCTIONS = (
    "successful_execution_reconciliation_candidates()",
    "complete_successful_execution_run(bytea)",
)


def upgrade() -> None:
    for statement in SQL.split("-- statement"):
        if statement.strip():
            op.execute(statement)
    for signature in FUNCTIONS:
        op.execute(f"REVOKE ALL ON FUNCTION public_live_api.{signature} FROM PUBLIC")
        op.execute(
            f"GRANT EXECUTE ON FUNCTION public_live_api.{signature} "
            "TO aiscc_public_live_execution,aiscc_public_live_reconciler"
        )


def downgrade() -> None:
    for signature in reversed(FUNCTIONS):
        op.execute(
            f"REVOKE EXECUTE ON FUNCTION public_live_api.{signature} "
            "FROM aiscc_public_live_execution,aiscc_public_live_reconciler"
        )
        op.execute(f"DROP FUNCTION public_live_api.{signature}")
