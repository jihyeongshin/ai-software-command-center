# ruff: noqa: E501
"""Expose a capability-scoped, allowlisted Public Live execution projection."""

from alembic import op

revision = "20260919_0028"
down_revision = "20260919_0027"
branch_labels = None
depends_on = None

TOOL_RESOURCE = "aiscc-stockroom-tools:2:stockroom_summary:1:stockroom-summary-v1"
TOOL_RESULT_HASH = "33158cca652adbfdcc2513dde646fe16bfdc58a3292a9d96eb46880c2297bd82"

SQL = rf"""
CREATE FUNCTION public_live_api.inspectable_execution_projection(r bytea) RETURNS jsonb
LANGUAGE plpgsql STABLE SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE x record; op record; steps jsonb:='[]'::jsonb; stock jsonb:=NULL;
 ordinal integer:=2; action text; public_status text; summary text;
BEGIN
 SELECT pr.state,pe.execution_attempt_id,a.status,z.state reservation_state,
  coalesce((SELECT s.state FROM public.public_slot s WHERE s.run_id=r),'FREE') slot_state,
  b.state outbox_state,coalesce(w.close_reason,'OPEN') work_state
 INTO x
 FROM public.public_run pr JOIN public.public_campaign c USING(campaign_id)
 JOIN public.public_provider_execution pe USING(run_id)
 JOIN public.public_semantic_plan sp USING(run_id)
 JOIN public.execution_attempts a ON a.execution_attempt_id=pe.execution_attempt_id
 JOIN public.public_reservation z USING(run_id) JOIN public.public_outbox b USING(run_id)
 LEFT JOIN public.public_worker_work w USING(run_id)
 WHERE pr.run_id=r AND c.scenario_id='stockroom-s1-normal' AND c.scenario_version='1.0.0'
 AND sp.profile='public-live-luna-v1' AND sp.profile_version=1;
 IF NOT FOUND THEN RETURN NULL; END IF;

 FOR op IN
  SELECT o.operation_kind,o.current_phase,o.outcome,o.resource_identity,o.call_ordinal,
   l.semantic_role,l.retry_of_operation_id,v.decision
  FROM public.execution_operations o
  LEFT JOIN public.public_provider_operation_link l USING(operation_id)
  LEFT JOIN public.public_provider_semantic_validation v USING(operation_id)
  WHERE o.execution_attempt_id=x.execution_attempt_id ORDER BY o.call_ordinal
 LOOP
  public_status:=CASE WHEN op.current_phase='OUTCOME_UNKNOWN' THEN 'OUTCOME_UNKNOWN'
   WHEN op.outcome='DEFINITELY_NOT_SENT' THEN 'DEFINITELY_NOT_SENT'
   WHEN op.current_phase='OUTCOME_KNOWN' THEN 'COMPLETED' ELSE 'IN_PROGRESS' END;
  IF op.operation_kind='PROVIDER' AND op.semantic_role IN('PRIMARY','VERIFY','CORRECT') THEN
   action:=CASE WHEN op.current_phase='OUTCOME_UNKNOWN' THEN 'OUTCOME_UNKNOWN'
    WHEN op.outcome='DEFINITELY_NOT_SENT' THEN 'DEFINITELY_NOT_SENT'
    WHEN op.outcome='PROVIDER_COMPLETED' AND EXISTS(
      SELECT 1 FROM public.execution_operations t WHERE t.execution_attempt_id=x.execution_attempt_id
      AND t.operation_kind='TOOL' AND t.call_ordinal=op.call_ordinal+1 AND t.resource_identity='{TOOL_RESOURCE}')
      THEN 'APPROVED_TOOL_REQUESTED'
    WHEN op.outcome='PROVIDER_COMPLETED' AND op.decision='COMPLETE' THEN 'BOUNDED_SUMMARY_PRODUCED'
    ELSE 'PROVIDER_STEP_RECORDED' END;
   steps:=steps||jsonb_build_array(jsonb_build_object('ordinal',ordinal,'kind','PROVIDER',
    'role',op.semantic_role,'status',public_status,'action',action,
    'tool_name',CASE WHEN action='APPROVED_TOOL_REQUESTED' THEN 'stockroom_summary' ELSE NULL END,
    'retry',op.retry_of_operation_id IS NOT NULL));
   ordinal:=ordinal+1;
  ELSIF op.operation_kind='TOOL' AND op.resource_identity='{TOOL_RESOURCE}' THEN
   steps:=steps||jsonb_build_array(jsonb_build_object('ordinal',ordinal,'kind','TOOL',
    'tool_name','stockroom_summary','status',public_status));
   ordinal:=ordinal+1;
   IF op.outcome='TOOL_COMPLETED'
    AND EXISTS(SELECT 1 FROM public.operation_events e JOIN public.execution_operations q USING(operation_id)
      WHERE q.execution_attempt_id=x.execution_attempt_id AND q.call_ordinal=op.call_ordinal
      AND e.target_phase='OUTCOME_KNOWN' AND e.refs->>'result_hash'='{TOOL_RESULT_HASH}')
    AND EXISTS(SELECT 1 FROM public.execution_output_refs o WHERE o.execution_attempt_id=x.execution_attempt_id
      AND o.ref_kind='ToolOutputRef' AND o.content_hash='{TOOL_RESULT_HASH}')
   THEN stock:=jsonb_build_object('items',jsonb_build_array(
     jsonb_build_object('sku','BOX-A','on_hand',12,'reserved',2,'available',10,'needs_reorder',false),
     jsonb_build_object('sku','BOX-B','on_hand',5,'reserved',5,'available',0,'needs_reorder',true),
     jsonb_build_object('sku','BOX-C','on_hand',4,'reserved',1,'available',3,'needs_reorder',true)),
     'total_available',13); END IF;
  END IF;
 END LOOP;
 steps:=steps||jsonb_build_array(jsonb_build_object('ordinal',ordinal,'kind','EXECUTION','status',x.status));
 ordinal:=ordinal+1;
 steps:=steps||jsonb_build_array(jsonb_build_object('ordinal',ordinal,'kind','PUBLIC_PROJECTION',
  'state',x.state,'reservation',x.reservation_state,'slot',x.slot_state,'outbox',x.outbox_state,'work',x.work_state));
 summary:=CASE WHEN x.status='EXECUTOR_COMPLETED' THEN 'Bounded execution completed from durable fixed-scenario evidence.'
  WHEN x.status='EXECUTION_FAILED' THEN 'Bounded execution ended with a recorded failure.'
  ELSE 'Durable bounded execution evidence is being recorded.' END;
 RETURN jsonb_build_object('schema','AISCC-PUBLIC-LIVE-INSPECTABLE-RESULT-V1',
  'workflow_state',x.status,'evidence_status','ADMITTED','summary_text',summary,
  'instruction',jsonb_build_object('authority','SERVER_OWNED','text','Produce the bounded Stockroom summary.'),
  'trace',steps,'stockroom',stock,
  'human_boundary',jsonb_build_object('state','NOT_PERFORMED',
   'statement','Successful AI execution does not become Human acceptance automatically.'));
END $$
"""


def upgrade() -> None:
    op.execute(SQL)
    op.execute(
        "REVOKE ALL ON FUNCTION public_live_api.inspectable_execution_projection(bytea) FROM PUBLIC"
    )
    op.execute(
        "GRANT EXECUTE ON FUNCTION public_live_api.inspectable_execution_projection(bytea) "
        "TO aiscc_public_live_ingress"
    )


def downgrade() -> None:
    op.execute(
        "REVOKE EXECUTE ON FUNCTION public_live_api.inspectable_execution_projection(bytea) "
        "FROM aiscc_public_live_ingress"
    )
    op.execute("DROP FUNCTION public_live_api.inspectable_execution_projection(bytea)")
