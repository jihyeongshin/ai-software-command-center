# AISCC Cycle Record

## meta

- cycle_id: `20260916_0100_aiscc-p3-3-public-live-l1-compatibility-l2-substantive-acceptance-persistence-entry-1`
- date: `2026-09-16 KST`
- primary_semantic_owner: `Browser Command Center`
- affected_areas: `P3-3 Public Live L1→L2 compatibility / L2 atomic admission`
- work_type: `REWORK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- task_file: `.aiassistant/tasks/done/20260915_2336_aiscc-p3-3-public-live-l1-compatibility-extension-and-l2-implementation-retry-1.md`
- result_status: `PARTIAL_ACCEPTED`
- reject_cause: `none`
- cycle_record_action: `create`
- source_mirror_sync: `not-required`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260916_0100_aiscc-p3-3-public-live-l1-compatibility-l2-substantive-acceptance-persistence-entry-1.cycle.md`

## repository snapshot

- branch: `main`
- base/current HEAD before persistence: `a2672c7a66bfd6b3d805caf2b187dae41b6181e5`
- source candidate: `UNCOMMITTED`
- index: `empty`
- public admission: `DISABLED`
- Public Live: `NOT_RELEASED`

## inbound result integrity

Executor result ZIP SHA-256:

`417913375532cc9c77f8545a59db8a4e8645e39d489c1fc3fe58efdb4847d55c`

Adjacent sidecar reports the same SHA-256.

## authority result

Historical frozen Public Live authority was recovered and verified:

```text
design commit:
209e7534f66e9b07ce9d33742e6993370a70f4fb

parent:
5e35ec0d60d84c7a05a2e58ebcc6560863879e5b

changed paths:
30 exact

L2:
Atomic admission and durable reconciliation service

ambiguity:
false
```

The earlier unsupported seven-basename premise remains superseded.

## accepted compatibility implementation

New additive Alembic revision:

```text
20260916_0014
down_revision:
20260915_0013
```

Accepted boundary:

- accepted `20260915_0013` unchanged;
- no public table/column/index/type/ownership change;
- public table ACLs unchanged;
- five mediated `SECURITY DEFINER` functions added under `public_live_api`;
- `search_path=pg_catalog`;
- PUBLIC EXECUTE revoked;
- exact EXECUTE granted to existing runtime role;
- runtime direct public-table SELECT/DML remains denied.

Compatibility surface:

- `admission_context`
- `admit_checked`
- `run_context`
- `project_run`
- `mark_checked`

The extension resolves the previously admitted L1→L2 API gap without weakening direct-DML denial.

## accepted L2 implementation

New bounded L2 service source:

- `src/aiscc/public_live/identity.py`
- `src/aiscc/public_live/service.py`
- package initializer and persistence wrappers

Semantic scope accepted:

- strict bounded request identity/input derivation;
- atomic admission/idempotency/rate/budget/slot/outbox path;
- actual WorkRun owner binding outside public DB locks;
- dispatch authorization remains external/fail-closed;
- durable marker-before-ticket;
- unknown-outcome no-resend behavior;
- reliable closure before settlement/projection;
- conservative missing/unknown usage accounting;
- above-bound safety disable/projection;
- truthful governance-pending/completed projection;
- no public HTTP route;
- no real provider transport;
- no activation/release path.

## evidence results

### database runtime

```text
PostgreSQL:
17.6

image:
postgres:17.6 local cache

network pull:
false

host:
127.0.0.1:55432

private DB reuse:
false

cleanup:
PASS
```

### migration/security

- migration topology: `PASS`
- 0013 SHA unchanged: `PASS`
- before/after public columns/indexes/constraints/table ACL equality: `PASS`
- direct public-table runtime access: all denied
- compatibility function security: `PASS`

### focused evidence

```text
compatibility focused:
8 cases PASS

L2 identity/unit + integration/concurrency/crash focused:
58 PASS final focused aggregate

static:
ruff format PASS
ruff PASS
mypy PASS
```

### final regression

```text
1278 PASS
3 SKIP
0 FAIL
0 ERROR
```

The three skips are the same Windows symlink-host capability skips.

No new skip/xfail was introduced.

A post-full-suite line-ending-only normalization affected two already-edited test lines; AST equality was verified and the directly affected migration preservation test was rerun:

```text
1 PASS
```

This does not change admitted application semantics.

## source changes accepted for persistence

Exact source/test/migration count:

```text
16
```

- `migrations/versions/20260916_0014_public_live_compatibility.py`
- `src/aiscc/persistence/public_live.py`
- `src/aiscc/public_live/__init__.py`
- `src/aiscc/public_live/identity.py`
- `src/aiscc/public_live/service.py`
- `tests/integration/next_action/test_genesis_bootstrap.py`
- `tests/integration/providers/test_external_ide_execution_ingress.py`
- `tests/integration/providers/test_external_ide_execution_start.py`
- `tests/integration/public_live/conftest.py`
- `tests/integration/public_live/test_compatibility.py`
- `tests/integration/public_live/test_persistence.py`
- `tests/integration/public_live/test_service.py`
- `tests/integration/self_dogfood/test_task_ready_entry.py`
- `tests/integration/task_authority/test_task_contract_durability.py`
- `tests/integration/workflow/test_postgres_kernel.py`
- `tests/unit/public_live/test_identity.py`

Seven existing integration files change only expected migration-head assertions from `20260915_0013` to `20260916_0014`.

## proof admission

Admitted:

- historical authority recovery;
- migration topology/schema/permission proof;
- isolated PostgreSQL proof;
- compatibility API proof;
- L2 unit/integration/concurrency/crash evidence;
- final full-suite result;
- workspace/index integrity;
- cleanup evidence.

Not admitted / remains future-owned:

- L3 HTTP behavior;
- real ingress overwrite proof;
- L4 real provider profile/cost/provider calls;
- L5 Railway/supervisor/deployment;
- integrated public release;
- Public Live enablement.

Proof substitution detected: `No`.

## command-center judgment

```text
L1 original scope:
ACCEPTED / CLOSED

L1→L2 compatibility:
SUBSTANTIVE ACCEPTED

L2:
SUBSTANTIVE ACCEPTED

Git persistence:
PENDING

Public Live:
NOT_RELEASED

Public admission:
DISABLED
```

Terminal L2 closure is deferred only until exact accepted source/governance persistence is completed and reviewed.

## preserved existing provenance to persist

- `.aiassistant/records/aiscc/cycles/20260915_2325_aiscc-command-center-baseline-regression-repair-terminal-closure-l2-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260915_2325_aiscc-browser-command-center-baseline-closed-public-live-l2-entry-handoff-1.md`
- `.aiassistant/reports/aiscc/20260915_2325_aiscc-browser-command-center-baseline-regression-repair-terminal-acceptance-l2-selection-1.md`
- `.aiassistant/tasks/done/20260915_2325_aiscc-p3-3-public-live-l2-atomic-admission-service-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260915_2340_aiscc-p3-3-l2-blocked-invalid-authority-artifact-assumption-rework-1.cycle.md`
- `.aiassistant/reports/aiscc/20260915_2340_aiscc-browser-command-center-p3-3-l2-blocked-invalid-authority-artifact-assumption-judgment-1.md`
- `.aiassistant/reports/aiscc/20260915_2340_aiscc-browser-command-center-p3-3-l2-historical-design-authority-recovery-retry-handoff-1.md`
- `.aiassistant/tasks/done/20260915_2340_aiscc-p3-3-public-live-l2-historical-design-authority-recovery-and-implementation-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260915_2336_aiscc-p3-3-l2-authority-resolved-l1-api-gap-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260915_2336_aiscc-browser-command-center-p3-3-l1-compatibility-l2-implementation-retry-handoff-1.md`
- `.aiassistant/reports/aiscc/20260915_2336_aiscc-browser-command-center-p3-3-l2-authority-resolved-l1-api-gap-judgment-1.md`
- `.aiassistant/tasks/done/20260915_2336_aiscc-p3-3-public-live-l1-compatibility-extension-and-l2-implementation-retry-1.md`

## next action

Exact Git persistence only.

No source mutation, no PostgreSQL recreation, no test broadening, no provider call, no deployment, no L3/L4/L5 implementation.
