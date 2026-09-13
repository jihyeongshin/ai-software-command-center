# AISCC Command Center Judgment

## meta

- judgment_id: `20260913_1343_aiscc-p2-3-invalid-history-abort-candidate-final-acceptance-judgment-1`
- created_at: `2026-09-13T13:43:21+09:00`
- project: `AI Software Command Center (AISCC)`
- reviewed_task: `20260913_1242_aiscc-p2-3-invalid-history-abort-contract-and-disposition-source-rework-1`
- reviewed_result_zip_sha256: `b1dc8f91d1ba01c0198953fad70ace3d3c45276fe279d35c50521f2ad02b1381`
- result_status: `ACCEPTED / INVALID_HISTORY_ABORT_CONTRACT_AND_SOURCE_CANDIDATE_COMPLETE`
- git_persistence_authorized: `Yes`
- retained_private_runtime_access_authorized: `No`
- runtime_disposition_authorized: `No`

# Browser judgment

1242 is accepted.

Independent Browser verification:

```text
result ZIP:
26 members / one top-level / CRC PASS

manifest:
25 / 25 exact bytes and SHA-256

TASK.md:
canonical done Task exact

contract:
60 / 60 PASS
```

Accepted contract/source behavior:

```text
EXECUTION_ABORTED_INVALID_HISTORY:
NOT_STARTED → EXECUTION_FAILED

required reason:
INVALID_HISTORY_SIDE_EFFECT_BEFORE_EXECUTION_START

generic transition_attempt:
cannot invoke special abort

dedicated repository owner:
abort_invalid_history_attempt

Stockroom disposition owner:
StockroomInvalidHistoryDisposition
```

Required durable order is implemented and tested:

```text
exact invalid-history preflight
→ append-only dedicated attempt abort
→ authoritative EXECUTION_FAILED reload
→ authentic G_FAILURE_TERMINAL
→ WorkRun RUNNING→FAILED
→ authoritative FAILED reload
→ restart-safe workspace quarantine
```

Workspace settlement:

```text
does not adopt/reconstruct historical lease
does not recursively delete old bytes
rechecks exact identity/inventory fingerprint
rejects symlink/reparse/hardlink/special-object ambiguity
moves only the exact verified attempt workspace into bounded quarantine
preserves quarantined bytes
never exposes quarantined content as an active workspace
```

Validation:

```text
operation protocol:
6 passed

workspace:
38 passed / 2 host-conditional skipped

provider persistence:
24 / 24 PASS

Stockroom scenario/disposition:
56 / 56 PASS

workflow handoff:
3 / 3 PASS

full unit:
745 passed / 3 host-conditional skipped / 0 failed

py_compile / Ruff / git diff --check:
PASS
```

Isolated PostgreSQL reached migration head `20260901_0008` and was removed.

Retained private S1 PostgreSQL/runtime/materialized workspace was not accessed.

# accepted exact candidate

```text
.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md
382433d24959827fc606592e7beb78f34934209fa2f9c34aabdeda1c6e322784
src/aiscc/providers/events.py
69b0339a12630eb552ef479a819c78596a2c0094437b4458a30eebb730c18a98
src/aiscc/persistence/repository.py
57dac018f6505468d62588761825025776d07384947424dad37b63f9f35e5e54
src/aiscc/scenarios/stockroom_production.py
abbe7f81840de7d9525900511f967512c72cf114104128501c681c19fbacd127
src/aiscc/runtime/stockroom_workspace.py
1b8366b5c5a6e9054dbd65ef36cd09808074c88ccf6c7ad060a9a76a488efaab
tests/unit/providers/test_operation_protocol.py
7160869c0342691574b8c3fb8bb3d8e741afd85ddefed08e8d96af826a263602
tests/integration/providers/test_execution_persistence.py
ba0f0a424dc0170c1400755804481e5e584643cac77cd8f539075f18f9ac6c9d
tests/integration/scenarios/test_stockroom_capture_runner.py
0f6c21edec2b70695a3727148e47143559aa2dc65b07058c6a8d59a18ee22fb6
tests/unit/runtime/test_stockroom_workspace.py
0dcd21e8f73ae84feb5eceb0a4a9addd7d6c8598455acda46b9559c029b0d706
```

# acceptance limits

This acceptance does not authorize the real 0036 disposition.

Until a later Browser-issued execution Task:

```text
no private DB query
no workspace inspection/quarantine
no attempt abort
no WorkRun failure
no new run/attempt
no cleanup
```
