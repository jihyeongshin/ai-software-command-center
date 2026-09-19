# AISCC Cycle Record

## meta

- cycle_id: `20260919_1046_aiscc-p3-3-l8-worker-recovery-accepted-canonical-persistence-suite-rework-entry-1`
- date: `2026-09-19 KST`
- primary_semantic_owner: `Browser Command Center`
- phase: `P3-3 / L8`
- predecessor_task: `20260919_0911_aiscc-p3-3-l8-public-worker-claim-sequence-recovery-and-rerelease-readiness-reproof-1`
- predecessor_result_zip_sha256: `0a8a983418acfb9721de6575ce7b882d665244bc415a6ada85da44163a74058a`
- result_status: `ACCEPTED_WORKER_RECOVERY / RERELEASE_READINESS_BLOCKED`
- blocker: `CANONICAL_PERSISTENCE_SUITE_STALE_AFTER_0025`
- Public_Live: `NOT_RELEASED`
- release_authority: `NONE`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260919_1046_aiscc-p3-3-l8-worker-recovery-accepted-canonical-persistence-suite-rework-entry-1.cycle.md`

## Browser bundle verification

- result ZIP SHA-256: `0a8a983418acfb9721de6575ce7b882d665244bc415a6ada85da44163a74058a`
- ZIP integrity: `PASS`
- members: `26`
- manifest rows: `25/25 hash+size PASS`
- issued Task ↔ result `TASK.md` ↔ committed `tasks/done`: `BYTE_IDENTICAL`
- Task SHA-256: `d2a8214cc011693e493ebff30a66928916949a56c8066025d385623e5910e7a8`
- raw provider/DB/SSH credential material: `NOT DETECTED`

## independently accepted worker repair

GitHub current main at review:

`f3f36a1ebeed86ec18bcc0a0e60fdcd3aacc9ca1`

Worker source repair commit:

`2e0e67e5f80c31de29b004944b858b33bc1cc27e`

The source commit changes only:
- `src/aiscc/public_live/worker_authority.py`
- `tests/integration/public_live/test_worker_claim_sequence.py`

Production source delta is the narrow protocol fix:

```text
candidate = self.sequence + 1
claim = await repository.claim(worker, candidate)
self.sequence = candidate
return claim
```

Therefore local sequence no longer advances when the DB rejects before returning.

Existing same-sequence idempotent replay remains the post-commit-response-loss recovery mechanism.

No schema, migration, role, grant, provider or secret authority change was introduced.

## deterministic repair evidence accepted

Accepted evidence:
- pre-fix divergence reproduced against PostgreSQL;
- repeated open-claim rejection leaves repaired local committed sequence unchanged;
- canonical release permits same-process recovery using the same next candidate;
- simulated response loss after DB commit replays the same sequence;
- duplicate claim/fence/ACQUIRED evidence is not created;
- normal EMPTY sequence advances exactly once;
- independent worker identity starts at 1;
- provider operations created by claim tests: 0.

Focused tests:
- new claim-sequence integration tests: 3 PASS;
- directly affected worker/start/UNKNOWN/Public Live tests: 27 PASS;
- Ruff: PASS;
- format: PASS;
- narrow mypy: PASS;
- diff check: PASS.

## hosted worker deployment accepted

Existing worker only:
- service `aiscc-public-live-worker`;
- source commit `2e0e67e5f80c31de29b004944b858b33bc1cc27e`;
- deployment success;
- Singapore / one replica;
- public domains 0;
- worker source bytes matched repository;
- env/config/secret/scale changes 0.

Fresh hosted worker idle proof:
- observed EMPTY sequences `9,10,11,12,13,14,15`;
- each transition exact +1;
- later observed `60 / EMPTY`;
- `PUBLIC_WORKER_FAILURE_UNCLASSIFIED = 0`;
- `CLAIM_SEQUENCE_DENIED = 0`;
- new public runs 0;
- provider calls 0.

This closes `PUBLIC_WORKER_CLAIM_SEQUENCE_RECOVERY_REGRESSION`.

## remaining blocker

Executor additionally ran the current canonical repository file:

`tests/integration/public_live/test_persistence.py`

Observed:

```text
25 PASS
23 FAIL
```

The file remains part of the default pytest surface because `pyproject.toml` has:

```text
testpaths = ["tests"]
```

and contains no exclusion for this file.

Browser independently confirmed the current file still asserts:

```python
assert rev == "20260919_0024" and after == before
```

while accepted canonical migration head is:

`20260919_0025`

The file also assumes a test database preparation shape that is stale relative to the current head.

Therefore this is not treated as proof of a production runtime regression yet, but release readiness cannot be accepted while a canonical Public Live persistence suite is red.

## Browser judgment

```text
worker claim-sequence regression:
ACCEPTED / CLOSED

worker deployment:
ACCEPTED

hosted idle worker:
ACCEPTED

hosted fail-closed state:
SUPPORTED

fresh rerelease readiness:
BLOCKED

exact blocker:
CANONICAL_PERSISTENCE_SUITE_STALE_AFTER_0025

Public Live:
NOT_RELEASED

Human release decision:
NOT_REQUESTED
```

## next action

Restore the canonical persistence suite to the accepted migration head and test fixture contract.

Do not paper over failures by excluding the file or weakening assertions.

If the failures reveal a real production regression instead of stale test authority, stop with the exact production blocker.

After suite restoration and fresh safe-state verification, Browser may accept readiness and request a NEW Human release decision.
