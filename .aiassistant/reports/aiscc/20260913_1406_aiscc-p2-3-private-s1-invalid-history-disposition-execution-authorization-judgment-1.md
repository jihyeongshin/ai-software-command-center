# AISCC Command Center Judgment

## meta

- judgment_id: `20260913_1406_aiscc-p2-3-private-s1-invalid-history-disposition-execution-authorization-judgment-1`
- created_at: `2026-09-13T14:06:56+09:00`
- project: `AI Software Command Center (AISCC)`
- authority_type: `PRIVATE_S1_INVALID_HISTORY_DISPOSITION_EXECUTION`
- persistence_result_zip_sha256: `012cc5f5abdaff9669c13f15268924f18ae13eedbec524d03c6b29dfa789862e`
- current_HEAD: `86288febf1cbd94bbb0235cfc680bf6c6c8f7772`
- result_status: `PRIVATE_DISPOSITION_EXECUTION_AUTHORIZED / EXACT_PRECONDITION_GATE`
- private_runtime_read_authorized: `Yes / exact retained resources only`
- private_runtime_mutation_authorized: `Conditional / exact source-owned disposition only`
- new_execution_authorized: `No`
- new_run_or_attempt_authorized: `No`

# Browser acceptance of persistence

The 1343 persistence result is accepted.

```text
Commit A:
4341138dde5fbea487f10a8af256f78c5dcf37f3

Commit B / current HEAD:
86288febf1cbd94bbb0235cfc680bf6c6c8f7772

Commit A path set:
23 exact

Commit B path set:
4 exact

final workspace:
clean

canonical next action:
PRIVATE_S1_INVALID_HISTORY_DISPOSITION_EXECUTION
ENTRY_READY / NOT_STARTED / NOT_AUTHORIZED
```

This Judgment changes that next action from `NOT_AUTHORIZED` to **conditionally authorized by this exact Task**.

# exact private subject

```text
run_id:
aiscc-p2-3-private-s1-normal-v1-run

attempt_id:
aiscc-p2-3-private-s1-normal-v1-attempt-1

expected WorkRun:
RUNNING / v2

expected ExecutionAttempt:
NOT_STARTED / execution_version 1 / causal READY-v1

expected execution operations:
0

expected runtime evidence:
0

expected Judgment:
0
```

# accepted immutable invalid-history provenance

The source-owned disposition request must use exactly these non-workspace provenance refs:

```text
aiscc-accepted-runtime-evidence:v1:0036:sha256:041285052e8fad97636231be69775e0dd7003b3d1b1683b64200cdc931eb0ac5
aiscc-accepted-disposition-contract:v1:1242:sha256:b1dc8f91d1ba01c0198953fad70ace3d3c45276fe279d35c50521f2ad02b1381
```

The service itself must append the exact workspace inventory fingerprint authority.

# authorized operation

If and only if every read-only preflight requirement in the Task is exact, execute exactly one source-owned disposition
request through the persisted implementation:

```text
StockroomProductionApplication.invalid_history_disposition_service()
→ StockroomInvalidHistoryDisposition.authorize(...)
→ StockroomInvalidHistoryDisposition.dispose(...)
```

Expected durable sequence:

```text
NOT_STARTED/v1
→ EXECUTION_ABORTED_INVALID_HISTORY
→ EXECUTION_FAILED/v2

WorkRun RUNNING/v2
→ G_FAILURE_TERMINAL
→ FAILED/v3

workspace:
active exact attempt workspace
→ QUARANTINED
```

# explicit prohibitions

This Judgment does not authorize:

```text
prepare_capture
StockroomCaptureRunner.run
EXECUTION_STARTED
provider/tool execution
new WorkRun
new attempt
runtime evidence
Judgment
DB-direct repair
manual UPDATE/DELETE/INSERT
broad filesystem cleanup
deleting quarantine
retrying dispose automatically after an exception
```

A preflight mismatch or an exception at any mutation stage means STOP_PRESERVE and Browser review.
