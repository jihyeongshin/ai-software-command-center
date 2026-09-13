# AISCC Command Center Judgment

## meta

- judgment_id: `20260913_1242_aiscc-p2-3-disposition-forbidden-contract-rework-authorization-judgment-1`
- created_at: `2026-09-13T12:42:29+09:00`
- reviewed_task: `20260913_1224_aiscc-p2-3-stranded-s1-invalid-history-disposition-design-1`
- reviewed_result_zip_sha256: `9d24bf9a9cfe2a2cd86c3c80d1f5fb2c8282c1f0373a4282ea43061efbdf0962`
- result_status: `ACCEPTED / DISPOSITION_FORBIDDEN_BY_CURRENT_CONTRACT`
- contract_rework_authorized: `Yes / exact bounded candidate`
- source_rework_authorized: `Yes / exact bounded candidate`
- private_runtime_access_authorized: `No`
- runtime_disposition_authorized: `No`

# Browser judgment

1224 is accepted.

Independent verification:

```text
18 members / one top-level / CRC PASS
manifest 17 / 17 exact
TASK.md == canonical done Task
contract 34 / 34 PASS
source/test/state mutation NONE
runtime/DB/Docker access NONE
```

Accepted classification:

```text
DISPOSITION_FORBIDDEN_BY_CURRENT_CONTRACT
```

Current contract has no truthful start-free edge from `ExecutionStatus.NOT_STARTED` to a terminal status after a
pre-start execution-side-effect has already occurred. Moving only the WorkRun to FAILED/BLOCKED is insufficient because
the child attempt remains nonterminal.

# authorized contract amendment candidate

Introduce one narrowly typed execution lifecycle event:

```text
EXECUTION_ABORTED_INVALID_HISTORY
```

Its only legal lifecycle edge is:

```text
NOT_STARTED → EXECUTION_FAILED
```

Its exact purpose is disposition of an already-invalid history where execution-side-effects occurred before
`EXECUTION_STARTED`.

It is NOT:
```text
a retry mechanism
a delayed start
a generic cancel
a substitute for EXECUTION_FAILED from RUNNING
a permission to ignore unknown provider outcomes
```

Required reason code for the present class:

```text
INVALID_HISTORY_SIDE_EFFECT_BEFORE_EXECUTION_START
```

The event must be append-only, exact-run/attempt bound, current-WorkRun-version bound, idempotent for the exact same
abort provenance, and forbidden through the ordinary generic transition API.

# required source-owned disposition order

A future runtime invocation implemented by this candidate must express only:

```text
1. preflight exact invalid-history shape
2. durable EXECUTION_ABORTED_INVALID_HISTORY on the existing exact attempt
3. authoritative reload: attempt == EXECUTION_FAILED
4. WorkRun RUNNING → FAILED using authentic G_FAILURE_TERMINAL provenance
5. authoritative reload: WorkRun == FAILED
6. restart-safe safety settlement of old materialization
   - exact deterministic ownership verification
   - never reuse old materialized content
   - if authentic old lease is unavailable, quarantine rather than adopt/delete
7. no evidence/Judgment creation
```

No private runtime execution is authorized in this candidate Task.
