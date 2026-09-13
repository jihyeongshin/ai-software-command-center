# AISCC Command Center Judgment

## meta

- judgment_id: `20260913_0138_aiscc-p2-3-s1-execution-lifecycle-owner-confirmed-rework-judgment-1`
- created_at: `2026-09-13T01:38:20+09:00`
- reviewed_task: `20260913_0115_aiscc-p2-3-s1-execution-lifecycle-desync-source-ownership-diagnosis-1`
- reviewed_result_zip_sha256: `14007a21c9adeefc33459eb4d8fd7a2bb274e97e4578ceb59c56bd4523db9838`
- result_status: `ACCEPTED / EXECUTION_LIFECYCLE_DEFECT_OWNER_IDENTIFIED`
- source_rework_authorized: `Yes / exact 2 paths maximum`
- runtime_recovery_authorized: `No`
- private_runtime_access_authorized: `No`

## accepted diagnosis

The 0115 bundle is accepted: 17 members, one top-level directory, CRC PASS, manifest 16/16 exact, contract 28/28 PASS, no source/test/state mutation, no runtime/DB/Docker access.

Diagnosis B is confirmed:

```text
create_attempt
→ durable attempt NOT_STARTED / READY-v1

G_EXECUTION_STARTED
→ validates the exact prepared NOT_STARTED ref

Workflow READY → RUNNING
→ admitted WorkRun RUNNING/v2

StockroomCaptureOwnerAdapter
→ refreshes only WorkRun snapshot
→ omits durable transition_attempt(EXECUTION_STARTED)

AgentExecutionService.execute
→ load_authority sees NOT_STARTED
→ returns NOT_STARTED before create_operation/provider/tool dispatch
```

Exact defect owner:

```text
src/aiscc/scenarios/stockroom_production.py
StockroomCaptureOwnerAdapter
```

Modify at most:

```text
src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Do not modify provider service/repository, capture runner, models/events/authority, workflow kernel/guards, schema/migrations.

Required correction:

```text
after READY→RUNNING is ADMITTED
→ apply durable EXECUTION_STARTED to the same exact prepared attempt
→ reload WorkRun + attempt
→ verify RUNNING + exact causal state/version
→ refresh the adapter's current attempt view from authoritative data
→ only then return the READY→RUNNING owner call as ADMITTED
```

If the durable start or verification fails, no security/materialization/execution may follow.

The already stranded 0036 attempt remains HOLD/PRESERVED and is not recovery-authorized by this Judgment.
