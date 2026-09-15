# AISCC Cycle Record

## meta

- cycle_id: `20260916_0811_aiscc-p3-3-limiter-retention-substantive-acceptance-persistence-entry-1`
- date: `2026-09-16 KST`
- primary_semantic_owner: `Browser Command Center`
- affected_areas: `P3-3 Public Live limiter retention / bounded storage`
- work_type: `REWORK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- task_file: `.aiassistant/tasks/done/20260916_0447_aiscc-p3-3-public-live-limiter-retention-resource-bound-implementation-1.md`
- result_status: `PARTIAL_ACCEPTED`
- reject_cause: `none`
- cycle_record_action: `create`
- source_mirror_sync: `not-required`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260916_0811_aiscc-p3-3-limiter-retention-substantive-acceptance-persistence-entry-1.cycle.md`

## repository snapshot

```text
branch:
main

HEAD:
bd46b40b47cede29a8865a2b78c42f4de36dc567

candidate:
UNCOMMITTED

index:
EMPTY

Public admission:
DISABLED

Public Live:
NOT_RELEASED
```

## result integrity

Executor result ZIP SHA-256:

`318ad8d4041e6366027e2206ce08ee29c3fcaec2c59a4664c26c0a0de5e6e3d2`

Adjacent `.sha256` sidecar matched exactly.

## controlling policy

Accepted authority:

`.aiassistant/reports/aiscc/20260916_0447_aiscc-p3-3-public-live-limiter-retention-resource-bound-policy-v1-accepted.md`

Status:

`HUMAN_PROVIDED / ACCEPTED V1`

## accepted implementation

Alembic:

```text
before:
20260916_0015 sole head

after:
20260916_0016 sole head

0016 down_revision:
20260916_0015
```

Accepted `0013`, `0014`, and `0015` exact bytes remained unchanged.

`0016` adds the bounded-retention compatibility layer only:

- bucket-prune index;
- singleton limiter-maintenance state;
- mediated `SECURITY DEFINER` maintenance function;
- retained flood/read wrappers;
- existing flood function replacement only for the Human-approved campaign-global short-circuit;
- old unguarded runtime consume EXECUTE revoked.

No L1/L2/L3 authority redesign is admitted.

## accepted retention semantics

```text
current DB minute bucket:
B

retained:
B-9 .. B

expired/pruned:
bucket < B-9
```

Evidence:

- seeded 13 buckets across SOURCE/CAMPAIGN/READ;
- exactly 10 buckets / 30 rows remain after maintenance;
- B-12..B-10 removed;
- B-9..B preserved;
- current quota state preserved;
- same-current-bucket maintenance state reused without another maintenance-state update;
- next DB minute advances cleanup.

## accepted cardinality amendment

The authoritative flood path now performs:

```text
CAMPAIGN consume/check first

if campaign_count > 1200:
    deny
    no SOURCE create/increment

else:
    SOURCE consume/check
```

Evidence with 1220 concurrent unique sources across independent pools/backend PIDs:

```text
CAMPAIGN attempts:
1220

allowed decisions:
1200

SOURCE rows:
1200

SOURCE total attempts:
1200

additional post-exhaustion SOURCE increment:
0
```

Therefore the accepted Human policy bound:

`<= 1200 newly materialized SOURCE identities / campaign / minute bucket`

is proven for mediated Public ingress.

## accepted concurrency/fail-closed/security evidence

- independent DB pools / >=2 PostgreSQL backend PIDs: PASS;
- concurrent 30/120/1200 limits remain exact: PASS;
- cleanup + consume concurrency: PASS;
- minute rollover inside consume refreshes maintenance: PASS;
- missing maintenance singleton: fail-closed;
- future/unsafe maintenance state: fail-closed;
- real SQL prune failure: fail-closed;
- HTTP result on maintenance failure: `503 LIVE_UNAVAILABLE`, `retryable=true`;
- failed request reaches no L2 admission and creates no public run/outbox/reservation/rate/dispatch or held budget effect;
- READ row not created on failed gated read;
- runtime raw maintenance/limiter SELECT/DML/DELETE/TRUNCATE: denied;
- direct prune and old unguarded consume function execution: denied;
- no raw IP persisted/logged;
- provider calls: `0`.

## regression

```text
focused:
186 PASS / 0 FAIL / 0 ERROR / 0 SKIP

full suite:
1383 PASS / 3 existing Windows symlink-host SKIP / 0 FAIL / 0 ERROR
```

Static:

- Ruff PASS
- Ruff format PASS
- mypy PASS
- git diff --check PASS

No new skip/xfail/assertion dilution was admitted.

## runtime / cleanup

```text
PostgreSQL:
17.6

image:
postgres:17.6 local cache

network pull:
false

bind:
127.0.0.1:55432

private predecessor DB reuse:
false

task-owned cleanup:
PASS
```

Post-validation:

```text
Alembic head:
0016

Public admission:
false

active campaign:
none

run rows:
0

dispatch rows:
0

limiter rows:
0

maintenance rows:
1
```

## Browser source audit

Browser Command Center reviewed:

- `20260916_0016_public_live_limiter_retention.py`;
- `public_live_limits.py`;
- focused retention/concurrency/fault tests;
- migration/result/runtime/workspace evidence.

No new substantive defect requiring rework was identified.

Important implementation detail accepted:

the retained wrapper may observe a DB-minute rollover between maintenance and the underlying consume. It re-runs maintenance when the result bucket differs. Because cleanup and consume remain in the same application transaction, a refresh-maintenance failure rolls back the consume result as well.

## accepted source paths

Exact 11:

- `migrations/versions/20260916_0016_public_live_limiter_retention.py`
- `src/aiscc/persistence/public_live_limits.py`
- `tests/integration/next_action/test_genesis_bootstrap.py`
- `tests/integration/providers/test_external_ide_execution_ingress.py`
- `tests/integration/providers/test_external_ide_execution_start.py`
- `tests/integration/public_live/test_http.py`
- `tests/integration/public_live/test_persistence.py`
- `tests/integration/public_live/test_retention.py`
- `tests/integration/self_dogfood/test_task_ready_entry.py`
- `tests/integration/task_authority/test_task_contract_durability.py`
- `tests/integration/workflow/test_postgres_kernel.py`

## blocker judgment

Previous:

```text
PUBLIC_LIVE_LIMITER_RETENTION_RESOURCE_BOUND_UNRESOLVED
```

Current substantive result:

```text
RESOLVED_CANDIDATE
```

Browser Command Center accepts the implementation/evidence substantively.

However final:

```text
RESOLVED
```

is deferred until exact Git persistence and commit review.

## current command-center truth

```text
L1:
ACCEPTED / CLOSED

L2:
ACCEPTED / CLOSED

L3:
ACCEPTED / CLOSED

limiter retention implementation:
SUBSTANTIVE ACCEPTED

release blocker:
RESOLVED_CANDIDATE

Git persistence:
PENDING

Public admission:
DISABLED

Public Live:
NOT_RELEASED
```

## next action

Exact Git persistence only.

Do not start L4/L5 yet.

After persistence acceptance:

1. mark the limiter retention blocker `RESOLVED`;
2. keep Public admission disabled;
3. select the next frozen DAG action between L4/L5.
