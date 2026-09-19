# AISCC Cycle Record

## meta

- cycle_id: `20260919_0911_aiscc-p3-3-l8-worker-claim-sequence-regression-rework-entry-1`
- date: `2026-09-19 KST`
- primary_semantic_owner: `Browser Command Center`
- phase: `P3-3 / L8`
- predecessor_task: `20260919_0415_aiscc-p3-3-l8-authorized-readonly-hosted-rerelease-readiness-reproof-1`
- predecessor_result_zip_sha256: `685289b0136e7e7263bf3fcf41d2e57b411cf4a1d8c96b93ba473416b9fc4937`
- result_status: `ACCEPTED_CORRECT_STOP / RERELEASE_READINESS_BLOCKED`
- blocker: `PUBLIC_WORKER_CLAIM_SEQUENCE_RECOVERY_REGRESSION`
- Public_Live: `NOT_RELEASED`
- release_authority: `NONE`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260919_0911_aiscc-p3-3-l8-worker-claim-sequence-regression-rework-entry-1.cycle.md`

## Browser bundle verification

- result ZIP SHA-256: `685289b0136e7e7263bf3fcf41d2e57b411cf4a1d8c96b93ba473416b9fc4937`
- ZIP integrity: `PASS`
- members: `19`
- manifest rows: `18/18 hash+size PASS`
- issued Task ↔ result `TASK.md` ↔ committed `tasks/done`: `BYTE_IDENTICAL`
- Task SHA-256: `2129e68649325e08c44ca0bf135526aaa165a1ecaee03f7617656cc85f7ce011`
- secret-safe scan: `PASS`

## fresh hosted evidence accepted

The 0415 retry successfully closed the prior read-path blocker.

Accepted fresh evidence includes:

- one task-owned ephemeral Railway SSH key used only for private read-only evidence;
- cleanup PASS: Railway key absent, local private/public key absent;
- PostgreSQL session read-only;
- migration head `20260919_0025`;
- 0025 reconciliation ACL exact;
- 0125 UNKNOWN settlement durable;
- 1919 settlement durable;
- campaign/day conservation exact;
- control disabled;
- no public ingress/worker domain;
- edge trust absent;
- provider secret worker-only / sealed;
- fixed in-process Public Stockroom tool applicable;
- Replay release-disabled and healthy according to fresh Executor HTTP evidence.

The Browser external web fetch environment could not independently reach the Pages URL during review, so public HTTP availability is admitted from the fresh Executor evidence rather than independently reproduced by Browser. Repository and Git provenance were independently verified.

## newly discovered runtime blocker

The production worker emitted a persistent sequence of:

`CLAIM_EXECUTION / PUBLIC_WORKER_FAILURE_UNCLASSIFIED`

The latest exported observation covered 200 consecutive failures over about 33 minutes and continued afterward.

At the same time:

- claimable work: 0;
- unreleased claims: 0;
- open dispatch pins: 0;
- unsettled reservations: 0;
- provider operations remained 1 historical UNKNOWN;
- provider calls/resends during Task: 0.

Therefore the loop is fail-closed but not runtime-ready.

## bounded root-cause finding

Fresh DB evidence showed the current worker instance retained:

```text
last_acquire_seq:
3083

last_result_kind:
CLAIM
```

from the retained 0125 attempt.

Current source independently verified by Browser:

```python
async def claim_next_work(...):
    ...
    self.sequence += 1
    return await self.repository.claim(self.worker, self.sequence)
```

Current DB contract independently verified by Browser:

```text
worker_claim_next accepts:
seq == last_acquire_seq       -> idempotent replay
OR
seq == last_acquire_seq + 1   -> next acquisition

anything else:
CLAIM_SEQUENCE_DENIED
```

When an open claim causes the `last+1` request to fail, the current process has already incremented its in-memory sequence while DB `last_acquire_seq` remains unchanged.

A later external UNKNOWN reconciliation can release the durable claim, but the same process can now submit `last+2`, `last+3`, ... forever and never resynchronize.

The original production exception text was intentionally not exported by the secret-safe logger. Therefore the exact exception in that running process is not independently observed, but:
- the persistent failure is direct evidence;
- the durable sequence state is direct evidence;
- the source/DB transition mismatch is direct evidence;
- the claim-sequence mechanism is a strong bounded root-cause inference that must be deterministically reproduced before repair acceptance.

## Browser judgment

```text
0415 execution:
ACCEPTED_CORRECT_STOP

hosted evidence path:
CLOSED

all non-worker readiness dimensions:
SUPPORTED / NO MATERIAL REGRESSION FOUND

fresh rerelease readiness:
BLOCKED

primary blocker:
PUBLIC_WORKER_CLAIM_SEQUENCE_RECOVERY_REGRESSION

Public Live:
NOT_RELEASED

Human release decision:
NOT_REQUESTED
```

A worker restart alone is not accepted as closure because it would hide the recurrence mechanism.

## next action

Implement a narrow durable/in-memory acquire-sequence recovery fix, prove it deterministically, deploy only the existing worker to the accepted source commit, prove healthy idle acquisition without provider/run activity, and reprove release readiness.

No release authority is granted.
