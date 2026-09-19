# ruff: noqa: E501
"""Reconcile one exact known-outcome failed Public Live execution."""

from alembic import op

revision = "20260919_0026"
down_revision = "20260919_0025"
branch_labels = None
depends_on = None

LIABILITY = "((8000::bigint*250000+2000::bigint*1200000+999999)/1000000)"
PROVIDER_RESOURCE = (
    "public-live-luna-v1:1:openai:"
    "e33230db3dd7d2f0153debcbb9fabc3386faac005477571931af855d70c4ae9b:responses-v1"
)
TOOL_RESOURCE = "aiscc-stockroom-tools:2:stockroom_summary:1:stockroom-summary-v1"

SQL = rf"""
CREATE FUNCTION public_live_api.known_failed_execution_reconciliation_candidates() RETURNS jsonb
LANGUAGE sql SECURITY DEFINER SET search_path=pg_catalog AS $$
 SELECT coalesce(jsonb_agg(jsonb_build_object(
   'run_id',encode(r.run_id,'hex'),
   'completed_provider_operation_id',(SELECT o.operation_id FROM public.execution_operations o
     WHERE o.execution_attempt_id=x.execution_attempt_id AND o.call_ordinal=1),
   'completed_provider_event_id',(SELECT e.event_id FROM public.operation_events e JOIN public.execution_operations o USING(operation_id)
     WHERE o.execution_attempt_id=x.execution_attempt_id AND o.call_ordinal=1
     AND e.target_phase='OUTCOME_KNOWN' AND e.outcome='PROVIDER_COMPLETED'),
   'tool_operation_id',(SELECT o.operation_id FROM public.execution_operations o
     WHERE o.execution_attempt_id=x.execution_attempt_id AND o.call_ordinal=2),
   'tool_event_id',(SELECT e.event_id FROM public.operation_events e JOIN public.execution_operations o USING(operation_id)
     WHERE o.execution_attempt_id=x.execution_attempt_id AND o.call_ordinal=2
     AND e.target_phase='OUTCOME_KNOWN' AND e.outcome='TOOL_COMPLETED'),
   'cancelled_provider_operation_id',(SELECT o.operation_id FROM public.execution_operations o
     WHERE o.execution_attempt_id=x.execution_attempt_id AND o.call_ordinal=3),
   'cancelled_provider_event_id',(SELECT e.event_id FROM public.operation_events e JOIN public.execution_operations o USING(operation_id)
     WHERE o.execution_attempt_id=x.execution_attempt_id AND o.call_ordinal=3
     AND e.target_phase='OUTCOME_KNOWN' AND e.outcome='CANCELLED'),
   'liability_micro',{LIABILITY}) ORDER BY encode(r.run_id,'hex')),'[]'::jsonb)
 FROM public.public_run r
 JOIN public.public_reservation z USING(run_id)
 JOIN public.public_outbox b USING(run_id)
 JOIN public.public_worker_work w USING(run_id)
 JOIN public.public_semantic_plan s USING(run_id)
 JOIN public.public_provider_execution x USING(run_id)
 JOIN public.execution_attempts a ON a.execution_attempt_id=x.execution_attempt_id
 WHERE r.state='ADMITTED' AND r.deadline<=public_live_api.clock_lock()
 AND z.state='HELD' AND z.amount=200000 AND z.committed_max=0 AND z.settled_cost IS NULL
 AND b.state='BOUND' AND w.closed_at IS NULL AND NOT w.recovery_required
 AND s.profile='public-live-luna-v1' AND s.profile_version=1
 AND s.phase_maximum=3 AND s.retry_maximum=1 AND s.physical_maximum=4
 AND a.provider_profile_id='public-live-luna-v1' AND a.provider_profile_version='1'
 AND a.status='EXECUTION_FAILED' AND x.work_run_id=r.owner_binding
 AND EXISTS(SELECT 1 FROM public.execution_events e WHERE e.execution_attempt_id=a.execution_attempt_id
   AND e.status_after='EXECUTION_FAILED' AND e.refs->>'failure_class'='RECOVERY_CONFLICT')
 AND NOT EXISTS(SELECT 1 FROM public.execution_events e WHERE e.execution_attempt_id=a.execution_attempt_id
   AND e.refs ? 'failure_class' AND e.refs->>'failure_class'<>'RECOVERY_CONFLICT')
 AND (SELECT count(*) FROM public.public_slot q WHERE q.run_id=r.run_id AND q.state='OCCUPIED')=1
 AND (SELECT count(*) FROM public.execution_operations o WHERE o.execution_attempt_id=a.execution_attempt_id)=3
 AND EXISTS(SELECT 1 FROM public.execution_operations o WHERE o.execution_attempt_id=a.execution_attempt_id
   AND o.call_ordinal=1 AND o.operation_kind='PROVIDER' AND o.resource_identity='{PROVIDER_RESOURCE}'
   AND o.current_phase='OUTCOME_KNOWN' AND o.outcome='PROVIDER_COMPLETED')
 AND EXISTS(SELECT 1 FROM public.execution_operations o WHERE o.execution_attempt_id=a.execution_attempt_id
   AND o.call_ordinal=2 AND o.operation_kind='TOOL' AND o.resource_identity='{TOOL_RESOURCE}'
   AND o.current_phase='OUTCOME_KNOWN' AND o.outcome='TOOL_COMPLETED')
 AND EXISTS(SELECT 1 FROM public.execution_operations o WHERE o.execution_attempt_id=a.execution_attempt_id
   AND o.call_ordinal=3 AND o.operation_kind='PROVIDER' AND o.resource_identity='{PROVIDER_RESOURCE}'
   AND o.current_phase='OUTCOME_KNOWN' AND o.outcome='CANCELLED')
 AND (SELECT count(*) FROM public.public_provider_operation_link l WHERE l.run_id=r.run_id)=2
 AND NOT EXISTS(SELECT 1 FROM public.public_provider_operation_link l WHERE l.run_id=r.run_id
   AND l.retry_of_operation_id IS NOT NULL)
 AND (SELECT count(*) FROM public.operation_events e JOIN public.execution_operations o USING(operation_id)
   WHERE o.execution_attempt_id=a.execution_attempt_id AND o.operation_kind='PROVIDER'
   AND e.target_phase='DISPATCH_STARTED')=1
 AND (SELECT count(*) FROM public.operation_events e JOIN public.execution_operations o USING(operation_id)
   WHERE o.execution_attempt_id=a.execution_attempt_id AND o.operation_kind='TOOL'
   AND e.target_phase='DISPATCH_STARTED')=1
 AND (SELECT count(*) FROM public.operation_events e JOIN public.execution_operations o USING(operation_id)
   WHERE o.execution_attempt_id=a.execution_attempt_id AND o.call_ordinal=1
   AND e.target_phase='OUTCOME_KNOWN' AND e.outcome='PROVIDER_COMPLETED')=1
 AND (SELECT count(*) FROM public.operation_events e JOIN public.execution_operations o USING(operation_id)
   WHERE o.execution_attempt_id=a.execution_attempt_id AND o.call_ordinal=2
   AND e.target_phase='OUTCOME_KNOWN' AND e.outcome='TOOL_COMPLETED')=1
 AND (SELECT count(*) FROM public.operation_events e JOIN public.execution_operations o USING(operation_id)
   WHERE o.execution_attempt_id=a.execution_attempt_id AND o.call_ordinal=3
   AND e.target_phase='OUTCOME_KNOWN' AND e.outcome='CANCELLED')=1
 AND NOT EXISTS(SELECT 1 FROM public.operation_events e JOIN public.execution_operations o USING(operation_id)
   WHERE o.execution_attempt_id=a.execution_attempt_id AND e.target_phase='OUTCOME_UNKNOWN')
 AND NOT EXISTS(SELECT 1 FROM public.operation_events e JOIN public.execution_operations o USING(operation_id)
   WHERE o.execution_attempt_id=a.execution_attempt_id AND o.call_ordinal=3
   AND e.target_phase='DISPATCH_STARTED')
 AND (SELECT count(*) FROM public.public_worker_claim c WHERE c.run_id=r.run_id AND c.released_at IS NULL)=0
 AND (SELECT count(*) FROM public.public_worker_dispatch_pin p JOIN public.public_worker_claim c USING(claim_id)
   WHERE c.run_id=r.run_id AND p.closed_at IS NULL)=0
 AND (SELECT count(*) FROM public.public_worker_dispatch_pin p JOIN public.public_worker_claim c USING(claim_id)
   WHERE c.run_id=r.run_id)=1
 AND NOT EXISTS(SELECT 1 FROM public.public_dispatch d WHERE d.run_id=r.run_id)
 AND NOT EXISTS(SELECT 1 FROM public.public_money_event m WHERE m.run_id=r.run_id AND m.event_kind='SETTLE')
 AND NOT EXISTS(SELECT 1 FROM public.public_control WHERE enabled)
$$;
-- statement
CREATE FUNCTION public_live_api.reconcile_known_failed_execution_run(r bytea) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE n timestamptz; run public.public_run; reservation public.public_reservation;
 outbox public.public_outbox; work public.public_worker_work; plan public.public_semantic_plan;
 execution public.public_provider_execution; attempt public.execution_attempts;
 op1 public.execution_operations; tool public.execution_operations; op3 public.execution_operations;
 op1_event public.operation_events; tool_event public.operation_events; op3_event public.operation_events;
 latest_claim public.public_worker_claim; prior public.public_money_event;
 liability bigint:={LIABILITY}; proof bytea; source bytea; seq bigint; count_value bigint;
BEGIN
 n:=public_live_api.clock_lock();
 SELECT * INTO STRICT run FROM public.public_run WHERE run_id=r FOR UPDATE;
 SELECT * INTO STRICT reservation FROM public.public_reservation WHERE run_id=r FOR UPDATE;
 SELECT * INTO STRICT outbox FROM public.public_outbox WHERE run_id=r FOR UPDATE;
 SELECT * INTO STRICT work FROM public.public_worker_work WHERE run_id=r FOR UPDATE;
 SELECT * INTO STRICT plan FROM public.public_semantic_plan WHERE run_id=r;
 SELECT * INTO STRICT execution FROM public.public_provider_execution WHERE run_id=r;
 SELECT * INTO STRICT attempt FROM public.execution_attempts WHERE execution_attempt_id=execution.execution_attempt_id;
 SELECT count(*) INTO count_value FROM public.execution_operations WHERE execution_attempt_id=attempt.execution_attempt_id;
 IF count_value<>3 THEN RAISE EXCEPTION 'KNOWN_FAILED_OPERATION_IDENTITY_AMBIGUOUS'; END IF;
 SELECT * INTO STRICT op1 FROM public.execution_operations WHERE execution_attempt_id=attempt.execution_attempt_id AND call_ordinal=1;
 SELECT * INTO STRICT tool FROM public.execution_operations WHERE execution_attempt_id=attempt.execution_attempt_id AND call_ordinal=2;
 SELECT * INTO STRICT op3 FROM public.execution_operations WHERE execution_attempt_id=attempt.execution_attempt_id AND call_ordinal=3;
 SELECT count(*) INTO count_value FROM public.operation_events WHERE operation_id=op1.operation_id
   AND target_phase='OUTCOME_KNOWN' AND outcome='PROVIDER_COMPLETED';
 IF count_value<>1 THEN RAISE EXCEPTION 'KNOWN_FAILED_PROVIDER_EVENT_AMBIGUOUS'; END IF;
 SELECT * INTO STRICT op1_event FROM public.operation_events WHERE operation_id=op1.operation_id
   AND target_phase='OUTCOME_KNOWN' AND outcome='PROVIDER_COMPLETED';
 SELECT count(*) INTO count_value FROM public.operation_events WHERE operation_id=tool.operation_id
   AND target_phase='OUTCOME_KNOWN' AND outcome='TOOL_COMPLETED';
 IF count_value<>1 THEN RAISE EXCEPTION 'KNOWN_FAILED_TOOL_EVENT_AMBIGUOUS'; END IF;
 SELECT * INTO STRICT tool_event FROM public.operation_events WHERE operation_id=tool.operation_id
   AND target_phase='OUTCOME_KNOWN' AND outcome='TOOL_COMPLETED';
 SELECT count(*) INTO count_value FROM public.operation_events WHERE operation_id=op3.operation_id
   AND target_phase='OUTCOME_KNOWN' AND outcome='CANCELLED';
 IF count_value<>1 THEN RAISE EXCEPTION 'KNOWN_FAILED_CANCEL_EVENT_AMBIGUOUS'; END IF;
 SELECT * INTO STRICT op3_event FROM public.operation_events WHERE operation_id=op3.operation_id
   AND target_phase='OUTCOME_KNOWN' AND outcome='CANCELLED';
 proof:=sha256(convert_to('P1_5_PUBLIC_LIVE_KNOWN_FAILED_RECONCILIATION_V1|'||encode(r,'hex')||'|'||
  op1.operation_id||'|'||op1_event.event_id||'|'||tool.operation_id||'|'||tool_event.event_id||'|'||
  op3.operation_id||'|'||op3_event.event_id||'|'||liability::text,'UTF8'));

 SELECT * INTO prior FROM public.public_money_event WHERE run_id=r AND event_kind='SETTLE';
 IF FOUND THEN
  IF run.state<>'FAILED_SAFETY' OR reservation.state<>'SETTLED' OR reservation.settled_cost<>liability
   OR prior.cost<>liability OR prior.evidence_digest<>proof OR outbox.state<>'CLOSED'
   OR work.closed_at IS NULL OR work.close_reason<>'KNOWN_FAILED_RECONCILED'
   OR EXISTS(SELECT 1 FROM public.public_slot WHERE run_id=r)
  THEN RAISE EXCEPTION 'KNOWN_FAILED_RECONCILIATION_REPLAY_CONFLICT'; END IF;
  RETURN jsonb_build_object('run_id',encode(r,'hex'),
   'completed_provider_operation_id',op1.operation_id,'completed_provider_event_id',op1_event.event_id,
   'tool_operation_id',tool.operation_id,'tool_event_id',tool_event.event_id,
   'cancelled_provider_operation_id',op3.operation_id,'cancelled_provider_event_id',op3_event.event_id,
   'liability_micro',liability,'evidence_digest',encode(proof,'hex'),
   'state',run.state,'reconciled',false);
 END IF;

 IF octet_length(r)<>16 OR n<run.deadline OR run.state<>'ADMITTED'
  OR reservation.state<>'HELD' OR reservation.amount<>200000 OR reservation.committed_max<>0
  OR reservation.settled_cost IS NOT NULL OR outbox.state<>'BOUND'
  OR work.closed_at IS NOT NULL OR work.recovery_required
  OR plan.profile<>'public-live-luna-v1' OR plan.profile_version<>1
  OR plan.phase_maximum<>3 OR plan.retry_maximum<>1 OR plan.physical_maximum<>4
  OR execution.work_run_id<>run.owner_binding
  OR attempt.provider_profile_id<>'public-live-luna-v1' OR attempt.provider_profile_version<>'1'
  OR attempt.status<>'EXECUTION_FAILED'
  OR NOT EXISTS(SELECT 1 FROM public.execution_events e WHERE e.execution_attempt_id=attempt.execution_attempt_id
    AND e.status_after='EXECUTION_FAILED' AND e.refs->>'failure_class'='RECOVERY_CONFLICT')
  OR EXISTS(SELECT 1 FROM public.execution_events e WHERE e.execution_attempt_id=attempt.execution_attempt_id
    AND e.refs ? 'failure_class' AND e.refs->>'failure_class'<>'RECOVERY_CONFLICT')
  OR op1.operation_kind<>'PROVIDER' OR op1.resource_identity<>'{PROVIDER_RESOURCE}'
  OR op1.current_phase<>'OUTCOME_KNOWN' OR op1.outcome<>'PROVIDER_COMPLETED'
  OR tool.operation_kind<>'TOOL' OR tool.resource_identity<>'{TOOL_RESOURCE}'
  OR tool.current_phase<>'OUTCOME_KNOWN' OR tool.outcome<>'TOOL_COMPLETED'
  OR op3.operation_kind<>'PROVIDER' OR op3.resource_identity<>'{PROVIDER_RESOURCE}'
  OR op3.current_phase<>'OUTCOME_KNOWN' OR op3.outcome<>'CANCELLED'
  OR (SELECT count(*) FROM public.public_provider_operation_link l WHERE l.run_id=r)<>2
  OR EXISTS(SELECT 1 FROM public.public_provider_operation_link l WHERE l.run_id=r AND l.retry_of_operation_id IS NOT NULL)
  OR (SELECT count(*) FROM public.operation_events e JOIN public.execution_operations o USING(operation_id)
    WHERE o.execution_attempt_id=attempt.execution_attempt_id AND o.operation_kind='PROVIDER'
    AND e.target_phase='DISPATCH_STARTED')<>1
  OR (SELECT count(*) FROM public.operation_events e WHERE e.operation_id=tool.operation_id AND e.target_phase='DISPATCH_STARTED')<>1
  OR EXISTS(SELECT 1 FROM public.operation_events e WHERE e.operation_id=op3.operation_id AND e.target_phase='DISPATCH_STARTED')
  OR EXISTS(SELECT 1 FROM public.operation_events e JOIN public.execution_operations o USING(operation_id)
    WHERE o.execution_attempt_id=attempt.execution_attempt_id AND e.target_phase='OUTCOME_UNKNOWN')
  OR (SELECT count(*) FROM public.public_worker_claim c WHERE c.run_id=r AND c.released_at IS NULL)<>0
  OR (SELECT count(*) FROM public.public_worker_dispatch_pin p JOIN public.public_worker_claim c USING(claim_id)
    WHERE c.run_id=r AND p.closed_at IS NULL)<>0
  OR (SELECT count(*) FROM public.public_worker_dispatch_pin p JOIN public.public_worker_claim c USING(claim_id)
    WHERE c.run_id=r)<>1
  OR (SELECT count(*) FROM public.public_slot q WHERE q.run_id=r AND q.state='OCCUPIED')<>1
  OR EXISTS(SELECT 1 FROM public.public_dispatch WHERE run_id=r)
  OR EXISTS(SELECT 1 FROM public.public_control WHERE enabled)
  OR liability<=0 OR liability>reservation.amount
  OR NOT EXISTS(SELECT 1 FROM public.public_campaign c WHERE c.campaign_id=run.campaign_id
    AND c.available+c.held+c.settled=c.limit_micro)
  OR NOT EXISTS(SELECT 1 FROM public.public_day d WHERE d.campaign_id=run.campaign_id AND d.utc_date=run.utc_date
    AND d.available+d.held+d.settled=d.limit_micro)
 THEN RAISE EXCEPTION 'KNOWN_FAILED_RECONCILIATION_PREDICATE_DENIED'; END IF;

 source:=sha256(convert_to('known-failed-closure-v1','UTF8')||r||proof);
 INSERT INTO public.public_observation VALUES(substring(source from 1 for 16),r,NULL,source,
  'CLOSURE',proof,n,liability);
 INSERT INTO public.public_money_event VALUES(r,'SETTLE',200000,liability,200000-liability,
  run.campaign_id,run.utc_date,proof,n);
 UPDATE public.public_campaign SET held=held-200000,settled=settled+liability,
  available=available+200000-liability WHERE campaign_id=run.campaign_id;
 UPDATE public.public_day SET held=held-200000,settled=settled+liability,
  available=available+200000-liability WHERE campaign_id=run.campaign_id AND utc_date=run.utc_date;
 UPDATE public.public_reservation SET committed_max=liability,settled_cost=liability,state='SETTLED'
  WHERE run_id=r;
 UPDATE public.public_slot SET run_id=NULL,state='FREE',generation=generation+1,
  heartbeat_at=NULL,expires_at=NULL WHERE run_id=r;
 UPDATE public.public_outbox SET state='CLOSED',generation=generation+1,fenced_at=n WHERE run_id=r;
 UPDATE public.public_worker_work SET closed_at=n,close_reason='KNOWN_FAILED_RECONCILED' WHERE run_id=r;
 SELECT * INTO STRICT latest_claim FROM public.public_worker_claim WHERE run_id=r ORDER BY fence DESC LIMIT 1;
 source:=sha256(r||proof||convert_to('KNOWN_FAILED_RECONCILED','UTF8'));
 SELECT coalesce(max(event_seq),0)+1 INTO seq FROM public.public_worker_claim_event WHERE run_id=r;
 INSERT INTO public.public_worker_claim_event VALUES(substring(source from 1 for 16),r,latest_claim.claim_id,
  seq,'CLOSED','KNOWN_FAILED_RECONCILED',n,NULL,NULL,op3.operation_id,source,source,
  jsonb_build_object('completed_provider_operation_id',op1.operation_id,'tool_operation_id',tool.operation_id,
    'cancelled_provider_operation_id',op3.operation_id));
 UPDATE public.public_run SET state='FAILED_SAFETY',version=version+1 WHERE run_id=r;
 source:=sha256(convert_to('failed-safety-known-execution-v1','UTF8')||r||proof);
 INSERT INTO public.public_observation VALUES(substring(source from 1 for 16),r,NULL,source,
  'USAGE',proof,n,NULL);
 IF NOT EXISTS(SELECT 1 FROM public.public_campaign c WHERE c.campaign_id=run.campaign_id
    AND c.available+c.held+c.settled=c.limit_micro)
  OR NOT EXISTS(SELECT 1 FROM public.public_day d WHERE d.campaign_id=run.campaign_id AND d.utc_date=run.utc_date
    AND d.available+d.held+d.settled=d.limit_micro)
 THEN RAISE EXCEPTION 'KNOWN_FAILED_LEDGER_CONSERVATION_REGRESSION'; END IF;
 RETURN jsonb_build_object('run_id',encode(r,'hex'),
  'completed_provider_operation_id',op1.operation_id,'completed_provider_event_id',op1_event.event_id,
  'tool_operation_id',tool.operation_id,'tool_event_id',tool_event.event_id,
  'cancelled_provider_operation_id',op3.operation_id,'cancelled_provider_event_id',op3_event.event_id,
  'liability_micro',liability,'evidence_digest',encode(proof,'hex'),
  'state','FAILED_SAFETY','reconciled',true);
END $$;
"""

FUNCTIONS = (
    "known_failed_execution_reconciliation_candidates()",
    "reconcile_known_failed_execution_run(bytea)",
)


def upgrade() -> None:
    for statement in SQL.split("-- statement"):
        if statement.strip():
            op.execute(statement)
    for signature in FUNCTIONS:
        op.execute(f"REVOKE ALL ON FUNCTION public_live_api.{signature} FROM PUBLIC")
        op.execute(
            f"GRANT EXECUTE ON FUNCTION public_live_api.{signature} TO aiscc_public_live_reconciler"
        )


def downgrade() -> None:
    for signature in reversed(FUNCTIONS):
        op.execute(
            f"REVOKE EXECUTE ON FUNCTION public_live_api.{signature} FROM aiscc_public_live_reconciler"
        )
        op.execute(f"DROP FUNCTION public_live_api.{signature}")
