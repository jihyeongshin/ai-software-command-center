# AISCC Cycle Record

## meta

- cycle_id: `20260916_0405_aiscc-p3-3-public-live-l3-substantive-acceptance-persistence-entry-1`
- date: `2026-09-16 KST`
- primary_semantic_owner: `Browser Command Center`
- affected_areas: `P3-3 Public Live L3 / shared limits / public-only HTTP composition`
- work_type: `REWORK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- task_file: `.aiassistant/tasks/done/20260916_0135_aiscc-p3-3-public-live-shared-limit-and-l3-implementation-human-policy-authorized-retry-1.md`
- result_status: `PARTIAL_ACCEPTED`
- reject_cause: `none`
- cycle_record_action: `create`
- source_mirror_sync: `not-required`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260916_0405_aiscc-p3-3-public-live-l3-substantive-acceptance-persistence-entry-1.cycle.md`

## repository snapshot

```text
branch:
main

HEAD:
968a7164cb50cfeaee5a6f83b7455ab87f6ccbd1

candidate:
UNCOMMITTED

index:
EMPTY

Public admission:
DISABLED

Public Live:
NOT_RELEASED
```

## result transport integrity

Executor result ZIP:

`20260916_0135_aiscc-p3-3-public-live-shared-limit-and-l3-implementation-human-policy-authorized-retry-1.zip`

Actual SHA-256:

`c123c1784d0130ae35e8d5c0db2aa117b483c23702a0fbbcf8c170b31fce0b5c`

Adjacent sidecar matched exactly.

## authority

Human-accepted amendment:

`.aiassistant/reports/aiscc/20260916_0135_aiscc-p3-3-public-live-shared-limit-policy-amendment-v1-accepted.md`

Status:

`HUMAN_PROVIDED / ACCEPTED V1`

Applied exact limits:

```text
authenticated run read:
30 / fixed 60-second DB-clock bucket / run

source flood:
120 / fixed 60-second DB-clock bucket / opaque source bucket

campaign flood:
1200 / fixed 60-second DB-clock bucket / campaign
```

Frozen L3:

```text
Public-only HTTP API composition
depends_on:
L2
```

## accepted implementation

New migration:

`20260916_0015_public_live_shared_limits.py`

Lineage:

```text
20260916_0014
→ 20260916_0015
```

Accepted properties:

- existing 0013/0014 exact bytes unchanged;
- one new narrow limiter table;
- mediated `flood_consume` and `read_consume` functions;
- runtime raw limiter-table SELECT/INSERT/UPDATE/DELETE/TRUNCATE denied;
- fixed DB-clock 60-second buckets;
- source+campaign flood accounting shared across independent DB connections/app instances;
- authenticated read accounting separate from flood;
- source identity persisted only as HMAC opaque bucket;
- raw IP not persisted/logged;
- process-memory throttle not used as shared authority.

L3 HTTP:

- isolated Public Live ASGI composition;
- exact POST/GET and controlled OPTIONS only;
- no owner/cancel/recovery/docs/openapi composition;
- shared flood before expensive parsing/auth/admission;
- exact CORS/content/media/query/header/body/capability handling;
- accepted L2 service binding;
- no provider transport;
- Public admission remains disabled by default.

## evidence

### PostgreSQL

```text
PostgreSQL:
17.6

image:
local cached postgres:17.6

network pull:
false

bind:
127.0.0.1:55432

private DB reuse:
false

cleanup:
PASS
```

### migration / permissions

```text
0014 sole head before:
PASS

0015 single successor:
PASS

existing DB objects unchanged:
PASS

raw limiter table runtime access:
DENIED

Public admission before/after:
false / false
```

### focused

```text
178 PASS
0 FAIL
0 ERROR
0 SKIP
```

### full suite

```text
1375 PASS
3 SKIP
0 FAIL
0 ERROR
```

The three skips are unchanged Windows symlink-host capability skips.

No new skip/xfail or assertion dilution was admitted.

### static

- Ruff PASS
- Ruff format PASS
- mypy PASS
- git diff --check PASS

### runtime

- cross-instance/shared PostgreSQL counters: PASS
- concurrent 30/120/1200 boundaries: PASS
- invalid capability flood-vs-read accounting: PASS
- limiter backend fail-closed: PASS
- local HTTP default-denial/replay independence: PASS
- real provider calls: `0`
- task-owned DB/runtime cleanup: PASS

## source-level Browser audit

Browser Command Center inspected the submitted migration and Public Live limiter/HTTP/source-adapter implementation.

No new L3 acceptance defect was identified.

Notable preserved boundaries:

- `SECURITY DEFINER` DB functions use `pg_catalog` search path;
- route layer has no raw limiter-table authority;
- public source identity is server-derived and HMAC-opaque;
- raw forwarding headers are not treated as authority;
- hosted proxy/TLS proof is not claimed;
- HTTP failures do not mint provider/workflow authority;
- L2 semantic source remains unchanged.

## accepted source paths

Exact 16:

- `migrations/versions/20260916_0015_public_live_shared_limits.py`
- `src/aiscc/persistence/public_live_limits.py`
- `src/aiscc/public_live/http.py`
- `src/aiscc/public_live/source.py`
- `tests/integration/next_action/test_genesis_bootstrap.py`
- `tests/integration/providers/test_external_ide_execution_ingress.py`
- `tests/integration/providers/test_external_ide_execution_start.py`
- `tests/integration/public_live/test_http.py`
- `tests/integration/public_live/test_persistence.py`
- `tests/integration/public_live/test_shared_limits.py`
- `tests/integration/self_dogfood/test_task_ready_entry.py`
- `tests/integration/task_authority/test_task_contract_durability.py`
- `tests/integration/workflow/test_postgres_kernel.py`
- `tests/public_live_http_helpers.py`
- `tests/unit/public_live/test_http.py`
- `tests/unit/public_live/test_source.py`

## release blocker discovered during Browser review

`20260916_0015` stores historical minute-bucket limiter rows without a retention/GC policy.

This does NOT fail the frozen L3 exit criteria and does not invalidate the current disabled L3 candidate.

However Public Live may not be enabled while persistent limiter resource growth remains unbounded/unspecified.

Reason:

- Public Bounded Live must remain bounded;
- accepted security baseline requires positive finite output/resource limits before executable profile/scenario enablement;
- hostile high-cardinality source traffic can grow retained SOURCE bucket rows over time.

Record:

```text
release_blocker:
PUBLIC_LIVE_LIMITER_RETENTION_RESOURCE_BOUND_UNRESOLVED

severity:
BLOCKS_PUBLIC_ADMISSION_ENABLEMENT

blocks_L3_substantive_acceptance:
NO

blocks_Git_persistence:
NO

must_resolve_before:
Public admission enablement / Public Live release
```

No retention number or cleanup algorithm is invented in this Cycle.

## command-center judgment

```text
L1:
ACCEPTED / CLOSED

L2:
ACCEPTED / CLOSED

L3:
SUBSTANTIVE ACCEPTED

Git persistence:
PENDING

release blocker:
PUBLIC_LIVE_LIMITER_RETENTION_RESOURCE_BOUND_UNRESOLVED

Public admission:
DISABLED

Public Live:
NOT_RELEASED
```

## provenance note

The 0133 Human-decision package was never transported into the Executor canonical repository before the accepted 0135 turn.

Its exact four provenance documents are therefore included in the persistence delivery package and must be placed/committed with the rest of the L3 lineage.

## next action

Git persistence only.

No source mutation, limiter redesign, retention policy invention, PostgreSQL recreation, test rerun, provider call, deployment, L4/L5 work, or Public admission enablement.
