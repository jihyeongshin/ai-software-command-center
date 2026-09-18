# ruff: noqa: E501
"""Bridge canonical P1-5 UNKNOWN into mediated Public Live reconciliation."""

from alembic import op

revision = "20260919_0025"
down_revision = "20260919_0024"
branch_labels = None
depends_on = None

LIABILITY = "((8000::bigint*250000+2000::bigint*1200000+999999)/1000000)"
PROVIDER_RESOURCE = (
    "public-live-luna-v1:1:openai:"
    "e33230db3dd7d2f0153debcbb9fabc3386faac005477571931af855d70c4ae9b:responses-v1"
)

SQL = rf"""
CREATE FUNCTION public_live_api.unknown_provider_reconciliation_candidates() RETURNS jsonb
LANGUAGE sql SECURITY DEFINER SET search_path=pg_catalog AS $$
 SELECT coalesce(jsonb_agg(jsonb_build_object(
   'run_id',encode(r.run_id,'hex'),
   'operation_id',(SELECT l.operation_id FROM public.public_provider_operation_link l WHERE l.run_id=r.run_id),
   'outcome_event_id',(SELECT e.event_id FROM public.operation_events e JOIN public.public_provider_operation_link l USING(operation_id)
     WHERE l.run_id=r.run_id AND e.target_phase='OUTCOME_UNKNOWN'
     AND e.outcome='TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME'),
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
 AND b.state='BOUND' AND w.recovery_required AND w.closed_at IS NULL
 AND s.profile='public-live-luna-v1' AND s.profile_version=1
 AND s.phase_maximum=3 AND s.retry_maximum=1 AND s.physical_maximum=4
 AND a.provider_profile_id='public-live-luna-v1' AND a.provider_profile_version='1'
 AND a.status='EXECUTION_FAILED' AND x.work_run_id=r.owner_binding
 AND EXISTS(SELECT 1 FROM public.public_slot q WHERE q.run_id=r.run_id AND q.state<>'FREE')
 AND (SELECT count(*) FROM public.public_worker_claim c WHERE c.run_id=r.run_id AND c.released_at IS NULL)=1
 AND (SELECT count(*) FROM public.public_worker_dispatch_pin p JOIN public.public_worker_claim c USING(claim_id)
   WHERE c.run_id=r.run_id AND p.closed_at IS NULL)=1
 AND (SELECT count(*) FROM public.public_provider_operation_link l WHERE l.run_id=r.run_id)=1
 AND EXISTS(SELECT 1 FROM public.public_provider_operation_link l JOIN public.execution_operations o USING(operation_id)
   WHERE l.run_id=r.run_id AND l.retry_of_operation_id IS NULL
   AND o.operation_kind='PROVIDER' AND o.resource_identity='{PROVIDER_RESOURCE}'
   AND o.current_phase='OUTCOME_UNKNOWN' AND o.outcome='TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME')
 AND (SELECT count(*) FROM public.execution_operations o WHERE o.execution_attempt_id=x.execution_attempt_id AND o.operation_kind='PROVIDER')=1
 AND NOT EXISTS(SELECT 1 FROM public.execution_operations o WHERE o.execution_attempt_id=x.execution_attempt_id AND o.operation_kind='TOOL')
 AND NOT EXISTS(SELECT 1 FROM public.public_dispatch d WHERE d.run_id=r.run_id)
 AND NOT EXISTS(SELECT 1 FROM public.execution_output_refs o WHERE o.execution_attempt_id=x.execution_attempt_id)
 AND (SELECT count(*) FROM public.operation_events e JOIN public.public_provider_operation_link l USING(operation_id)
   WHERE l.run_id=r.run_id AND e.target_phase='DISPATCH_STARTED')=1
 AND (SELECT count(*) FROM public.operation_events e JOIN public.public_provider_operation_link l USING(operation_id)
   WHERE l.run_id=r.run_id AND e.target_phase='OUTCOME_UNKNOWN'
   AND e.outcome='TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME')=1
 AND NOT EXISTS(SELECT 1 FROM public.operation_events e JOIN public.public_provider_operation_link l USING(operation_id)
   WHERE l.run_id=r.run_id AND e.target_phase='OUTCOME_KNOWN')
 AND NOT EXISTS(SELECT 1 FROM public.public_control WHERE enabled)
$$;
-- statement
CREATE FUNCTION public_live_api.reconcile_unknown_provider_run(r bytea) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE n timestamptz; run public.public_run; reservation public.public_reservation;
 outbox public.public_outbox; work public.public_worker_work; claim public.public_worker_claim;
 pin public.public_worker_dispatch_pin; link public.public_provider_operation_link;
 operation public.execution_operations; unknown_event public.operation_events;
 dispatch_event public.operation_events; plan public.public_semantic_plan;
 execution public.public_provider_execution; attempt public.execution_attempts;
 liability bigint:={LIABILITY}; proof bytea; source bytea; seq bigint; count_value bigint;
 prior public.public_money_event;
BEGIN
 n:=public_live_api.clock_lock();
 SELECT * INTO STRICT run FROM public.public_run WHERE run_id=r FOR UPDATE;
 SELECT * INTO STRICT reservation FROM public.public_reservation WHERE run_id=r FOR UPDATE;
 SELECT * INTO STRICT outbox FROM public.public_outbox WHERE run_id=r FOR UPDATE;
 SELECT * INTO STRICT work FROM public.public_worker_work WHERE run_id=r FOR UPDATE;
 SELECT * INTO STRICT plan FROM public.public_semantic_plan WHERE run_id=r;
 SELECT * INTO STRICT execution FROM public.public_provider_execution WHERE run_id=r;
 SELECT * INTO STRICT attempt FROM public.execution_attempts WHERE execution_attempt_id=execution.execution_attempt_id;
 SELECT count(*) INTO count_value FROM public.public_provider_operation_link WHERE run_id=r;
 IF count_value<>1 THEN RAISE EXCEPTION 'UNKNOWN_PROVIDER_OPERATION_IDENTITY_AMBIGUOUS'; END IF;
 SELECT * INTO STRICT link FROM public.public_provider_operation_link WHERE run_id=r;
 SELECT * INTO STRICT operation FROM public.execution_operations WHERE operation_id=link.operation_id FOR UPDATE;
 SELECT count(*) INTO count_value FROM public.operation_events WHERE operation_id=operation.operation_id
  AND target_phase='OUTCOME_UNKNOWN' AND outcome='TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME';
 IF count_value<>1 THEN RAISE EXCEPTION 'UNKNOWN_PROVIDER_EVENT_IDENTITY_AMBIGUOUS'; END IF;
 SELECT * INTO STRICT unknown_event FROM public.operation_events WHERE operation_id=operation.operation_id
  AND target_phase='OUTCOME_UNKNOWN' AND outcome='TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME';
 proof:=sha256(convert_to('P1_5_PUBLIC_LIVE_UNKNOWN_RECONCILIATION_V1|'||encode(r,'hex')||'|'||
  operation.operation_id||'|'||unknown_event.event_identity||'|'||liability::text,'UTF8'));

 SELECT * INTO prior FROM public.public_money_event WHERE run_id=r AND event_kind='SETTLE';
 IF FOUND THEN
  SELECT * INTO STRICT pin FROM public.public_worker_dispatch_pin WHERE operation_id=operation.operation_id;
  SELECT * INTO STRICT claim FROM public.public_worker_claim WHERE claim_id=pin.claim_id;
  IF run.state<>'FAILED_TIMEOUT' OR reservation.state<>'SETTLED' OR reservation.settled_cost<>liability
   OR prior.cost<>liability OR prior.evidence_digest<>proof OR pin.closed_at IS NULL
   OR pin.outcome_event_id<>unknown_event.event_id OR pin.closure_evidence_digest<>proof
   OR claim.released_at IS NULL OR work.closed_at IS NULL
  THEN RAISE EXCEPTION 'UNKNOWN_RECONCILIATION_REPLAY_CONFLICT'; END IF;
  RETURN jsonb_build_object('run_id',encode(r,'hex'),'operation_id',operation.operation_id,
   'outcome_event_id',unknown_event.event_id,'liability_micro',liability,
   'evidence_digest',encode(proof,'hex'),'state',run.state,'reconciled',false);
 END IF;

 IF octet_length(r)<>16 OR n<run.deadline OR run.state<>'ADMITTED'
  OR reservation.state<>'HELD' OR reservation.amount<>200000 OR reservation.committed_max<>0
  OR reservation.settled_cost IS NOT NULL OR outbox.state<>'BOUND'
  OR NOT work.recovery_required OR work.closed_at IS NOT NULL
  OR plan.profile<>'public-live-luna-v1' OR plan.profile_version<>1
  OR plan.phase_maximum<>3 OR plan.retry_maximum<>1 OR plan.physical_maximum<>4
  OR execution.work_run_id<>run.owner_binding
  OR attempt.provider_profile_id<>'public-live-luna-v1' OR attempt.provider_profile_version<>'1'
  OR attempt.status<>'EXECUTION_FAILED' OR link.retry_of_operation_id IS NOT NULL
  OR operation.operation_kind<>'PROVIDER' OR operation.resource_identity<>'{PROVIDER_RESOURCE}'
  OR operation.current_phase<>'OUTCOME_UNKNOWN'
  OR operation.outcome<>'TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME'
  OR operation.latest_event_sequence<>unknown_event.event_sequence
  OR liability<=0 OR liability>reservation.amount
  OR EXISTS(SELECT 1 FROM public.public_control WHERE enabled)
  OR EXISTS(SELECT 1 FROM public.public_dispatch WHERE run_id=r)
  OR EXISTS(SELECT 1 FROM public.execution_output_refs WHERE execution_attempt_id=execution.execution_attempt_id)
  OR EXISTS(SELECT 1 FROM public.execution_operations WHERE execution_attempt_id=execution.execution_attempt_id AND operation_kind='TOOL')
  OR (SELECT count(*) FROM public.execution_operations WHERE execution_attempt_id=execution.execution_attempt_id AND operation_kind='PROVIDER')<>1
  OR EXISTS(SELECT 1 FROM public.operation_events WHERE operation_id=operation.operation_id AND target_phase='OUTCOME_KNOWN')
 THEN RAISE EXCEPTION 'UNKNOWN_RECONCILIATION_PREDICATE_DENIED'; END IF;

 SELECT * INTO STRICT pin FROM public.public_worker_dispatch_pin WHERE operation_id=operation.operation_id FOR UPDATE;
 SELECT * INTO STRICT claim FROM public.public_worker_claim WHERE claim_id=pin.claim_id FOR UPDATE;
 SELECT * INTO STRICT dispatch_event FROM public.operation_events WHERE event_id=pin.dispatch_event_id;
 IF pin.closed_at IS NOT NULL OR claim.run_id<>r OR claim.released_at IS NOT NULL
  OR claim.current_operation_id<>operation.operation_id OR dispatch_event.operation_id<>operation.operation_id
  OR dispatch_event.target_phase<>'DISPATCH_STARTED'
  OR (SELECT count(*) FROM public.public_worker_claim WHERE run_id=r AND released_at IS NULL)<>1
  OR (SELECT count(*) FROM public.public_worker_dispatch_pin p JOIN public.public_worker_claim c USING(claim_id)
      WHERE c.run_id=r AND p.closed_at IS NULL)<>1
  OR NOT EXISTS(SELECT 1 FROM public.public_slot WHERE run_id=r AND state<>'FREE' FOR UPDATE)
 THEN RAISE EXCEPTION 'UNKNOWN_WORKER_QUARANTINE_PREDICATE_DENIED'; END IF;

 source:=sha256(convert_to('unknown-public-projection-v1','UTF8')||r||proof);
 INSERT INTO public.public_observation VALUES(substring(source from 1 for 16),r,NULL,source,
  'UNKNOWN',proof,n,liability);
 UPDATE public.public_run SET state='UNKNOWN_OUTCOME',version=version+1 WHERE run_id=r;
 UPDATE public.public_outbox SET state='CLOSED',generation=generation+1,fenced_at=n WHERE run_id=r;
 UPDATE public.public_slot SET state='SUSPECT' WHERE run_id=r;
 UPDATE public.public_reservation SET committed_max=liability WHERE run_id=r;

 UPDATE public.public_worker_dispatch_pin SET closed_at=n,closure_evidence_digest=proof,
  outcome_event_id=unknown_event.event_id WHERE operation_id=operation.operation_id;
 source:=sha256(claim.claim_id||convert_to(operation.operation_id,'UTF8')||
  convert_to(unknown_event.event_id,'UTF8')||proof);
 SELECT coalesce(max(event_seq),0)+1 INTO seq FROM public.public_worker_claim_event WHERE run_id=r;
 INSERT INTO public.public_worker_claim_event VALUES(substring(source from 1 for 16),r,claim.claim_id,
  seq,'PIN_CLOSED','UNKNOWN_RECONCILED',n,NULL,NULL,operation.operation_id,source,source,
  jsonb_build_object('outcome_event_id',unknown_event.event_id,'outcome','OUTCOME_UNKNOWN'));

 UPDATE public.public_worker_claim SET released_at=n,release_reason='EXECUTION_TERMINAL'
  WHERE claim_id=claim.claim_id;
 source:=sha256(claim.claim_id||proof||convert_to('EXECUTION_TERMINAL','UTF8'));
 SELECT coalesce(max(event_seq),0)+1 INTO seq FROM public.public_worker_claim_event WHERE run_id=r;
 INSERT INTO public.public_worker_claim_event VALUES(substring(source from 1 for 16),r,claim.claim_id,
  seq,'RELEASED','EXECUTION_TERMINAL',n,NULL,NULL,operation.operation_id,source,source,
  jsonb_build_object('outcome','OUTCOME_UNKNOWN'));

 UPDATE public.public_worker_work SET closed_at=n,close_reason='UNKNOWN_RECONCILED' WHERE run_id=r;
 source:=sha256(r||proof||convert_to('UNKNOWN_RECONCILED','UTF8'));
 SELECT coalesce(max(event_seq),0)+1 INTO seq FROM public.public_worker_claim_event WHERE run_id=r;
 INSERT INTO public.public_worker_claim_event VALUES(substring(source from 1 for 16),r,claim.claim_id,
  seq,'CLOSED','UNKNOWN_RECONCILED',n,NULL,NULL,operation.operation_id,source,source,
  jsonb_build_object('outcome','OUTCOME_UNKNOWN'));

 source:=sha256(convert_to('unknown-closure-v1','UTF8')||r||proof);
 INSERT INTO public.public_observation VALUES(substring(source from 1 for 16),r,NULL,source,
  'CLOSURE',proof,n,liability);
 INSERT INTO public.public_money_event VALUES(r,'SETTLE',200000,liability,200000-liability,
  run.campaign_id,run.utc_date,proof,n);
 UPDATE public.public_campaign SET held=held-200000,settled=settled+liability,
  available=available+200000-liability WHERE campaign_id=run.campaign_id;
 UPDATE public.public_day SET held=held-200000,settled=settled+liability,
  available=available+200000-liability WHERE campaign_id=run.campaign_id AND utc_date=run.utc_date;
 UPDATE public.public_reservation SET settled_cost=liability,state='SETTLED' WHERE run_id=r;
 UPDATE public.public_slot SET run_id=NULL,state='FREE',generation=generation+1,
  heartbeat_at=NULL,expires_at=NULL WHERE run_id=r;
 UPDATE public.public_run SET state='FAILED_TIMEOUT',version=version+1 WHERE run_id=r;
 source:=sha256(convert_to('failed-timeout-projection-v1','UTF8')||r||proof);
 INSERT INTO public.public_observation VALUES(substring(source from 1 for 16),r,NULL,source,
  'USAGE',proof,n,NULL);
 RETURN jsonb_build_object('run_id',encode(r,'hex'),'operation_id',operation.operation_id,
  'outcome_event_id',unknown_event.event_id,'liability_micro',liability,
  'evidence_digest',encode(proof,'hex'),'state','FAILED_TIMEOUT','reconciled',true);
END $$;
"""

FUNCTIONS = (
    "unknown_provider_reconciliation_candidates()",
    "reconcile_unknown_provider_run(bytea)",
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
