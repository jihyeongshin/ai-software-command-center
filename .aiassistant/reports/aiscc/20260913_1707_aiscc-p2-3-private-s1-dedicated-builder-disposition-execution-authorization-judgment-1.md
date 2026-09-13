# AISCC Command Center Judgment

## meta

- judgment_id: `20260913_1707_aiscc-p2-3-private-s1-dedicated-builder-disposition-execution-authorization-judgment-1`
- created_at: `2026-09-13T17:07:32+09:00`
- project: `AI Software Command Center (AISCC)`
- authority_type: `PRIVATE_S1_INVALID_HISTORY_DISPOSITION_EXECUTION`
- persistence_result_zip_sha256: `0db3994c4053f2def2dbe755315d7a7630a317b2091a13e96485a27635f6d6e1`
- current_HEAD: `d04f6a322f3a3ea49778314e4005b5878b20f121`
- result_status: `PRIVATE_DISPOSITION_EXECUTION_AUTHORIZED / DEDICATED_BUILDER_EXACT_GATE`
- private_runtime_read_authorized: `Yes / exact retained resources`
- private_runtime_mutation_authorized: `Conditional / one persisted disposition`
- new_execution_authorized: `No`
- new_run_or_attempt_authorized: `No`

# persisted authority

The dedicated disposition-only composition is FINAL_ADMITTED / PERSISTED.

```text
Commit A:
7e2ea251f88ca07c6fd1bde38f73956f8885adbe

Commit B/current HEAD:
d04f6a322f3a3ea49778314e4005b5878b20f121

public builder:
build_stockroom_invalid_history_disposition
```

# exact subject

```text
run_id:
aiscc-p2-3-private-s1-normal-v1-run

attempt_id:
aiscc-p2-3-private-s1-normal-v1-attempt-1

requester_identity:
aiscc-owner-operator
```

Expected initial durable authority:

```text
WorkRun RUNNING/v2
ExecutionAttempt NOT_STARTED/v1
attempt causal READY/v1
execution operations 0
execution outputs/submission 0
runtime evidence 0
Judgment 0
```

Expected retained workspace authority from the successful 1435 preflight:

```text
objects:
20

files:
14

bounded bytes:
2320

inventory fingerprint:
18433a8d92affe915d01e3bb1265b387a07dc6478e09c92306854908ab396068
```

This expected fingerprint must be re-observed before mutation; prior observation is not a substitute for current preflight.

# authorized source path

If and only if all preflight/recheck predicates in the Task pass:

```text
service = await build_stockroom_invalid_history_disposition(...)
request = await service.authorize(...)
result = await service.dispose(request)
```

Expected durable result:

```text
attempt:
EXECUTION_FAILED/v2 / causal RUNNING-v2

WorkRun:
FAILED/v3

workspace:
QUARANTINED / bytes preserved
```

# prohibited

Do not use:

```text
build_stockroom_production
build_stockroom_production_application
prepare_capture
StockroomCaptureRunner.run
EXECUTION_STARTED
provider/tool execution
new run/attempt
evidence/Judgment
DB-direct UPDATE/DELETE/INSERT
broad cleanup
automatic second dispose call
```

Any mismatch or exception means STOP_PRESERVE and read-only stage classification only.
