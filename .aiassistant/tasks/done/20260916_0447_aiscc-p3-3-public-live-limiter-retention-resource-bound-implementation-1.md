# 작업지시서: P3-3 Public Live Limiter Retention / Resource-Bound Implementation

## meta

- task_id: `20260916_0447_aiscc-p3-3-public-live-limiter-retention-resource-bound-implementation-1`
- created_at: `2026-09-16 KST`
- work_type: `REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `bd46b40b47cede29a8865a2b78c42f4de36dc567`
- primary_semantic_owner: `P3-3 Public Live limiter bounded-storage release blocker`
- predecessor_blocker: `PUBLIC_LIVE_LIMITER_RETENTION_RESOURCE_BOUND_UNRESOLVED`

## current state

- branch: `main`
- expected HEAD: `bd46b40b47cede29a8865a2b78c42f4de36dc567`
- L1: `ACCEPTED / CLOSED`
- L2: `ACCEPTED / CLOSED`
- L3: `ACCEPTED / CLOSED`
- retention policy: `HUMAN_PROVIDED / ACCEPTED V1`
- retention implementation: `NOT_STARTED`
- release blocker: `UNRESOLVED`
- Public admission: `DISABLED`
- Public Live: `NOT_RELEASED`

Use the current IDE Executor conversation. No fresh chat is required.

## controlling authority

Read first:

`.aiassistant/reports/aiscc/20260916_0447_aiscc-p3-3-public-live-limiter-retention-resource-bound-policy-v1-accepted.md`

It must state:

`HUMAN_PROVIDED / ACCEPTED`

Historical proposal:

`.aiassistant/reports/aiscc/20260916_0445_aiscc-p3-3-public-live-limiter-retention-resource-bound-policy-proposal-1.md`

is provenance only.

## exact accepted policy

Existing request-rate caps remain unchanged:

```text
READ:
30 / fixed 60-second DB-clock bucket / run

SOURCE:
120 / fixed 60-second DB-clock bucket / opaque source identity

CAMPAIGN:
1200 / fixed 60-second DB-clock bucket / campaign
```

Retention:

```text
current bucket + previous 9
= 10 buckets maximum

delete/prune eligible:
bucket < current_bucket - 9
```

Campaign-global exhaustion amendment:

```text
increment/check CAMPAIGN first

if resulting campaign count > 1200:
    deny CLIENT_RATE_LIMIT
    do not create or increment SOURCE row

else:
    consume/check SOURCE normally
```

Cleanup:

```text
System-owned mediated DB maintenance
DB clock authoritative
at most once per current bucket
unknown/stale/unsafe maintenance state => fail closed
```

Maintenance failure:

```text
503 LIVE_UNAVAILABLE
retryable=true
no L2 admission
no provider call
no paid budget effect
```

## must-read current paths

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- `.aiassistant/rules/AISCC_SECURITY_SANDBOX.md`
- `.aiassistant/rules/AISCC_ORCHESTRATION.md`
- `.aiassistant/records/aiscc/cycles/20260916_0447_aiscc-p3-3-limiter-retention-policy-human-acceptance-implementation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260916_0447_aiscc-browser-command-center-limiter-retention-policy-human-acceptance-implementation-entry-1.md`
- `.aiassistant/reports/aiscc/20260916_0447_aiscc-browser-command-center-limiter-retention-policy-accepted-implementation-handoff-1.md`
- `.aiassistant/reports/aiscc/20260916_0447_aiscc-p3-3-public-live-limiter-retention-resource-bound-policy-v1-accepted.md`
- `migrations/versions/20260916_0015_public_live_shared_limits.py`
- `src/aiscc/persistence/public_live_limits.py`
- `src/aiscc/public_live/http.py`
- `src/aiscc/public_live/source.py`
- `tests/integration/public_live/test_shared_limits.py`
- `tests/integration/public_live/test_http.py`

Do not bulk-read unrelated source/rules.

## Phase R1 — migration topology

Before source mutation:

1. verify branch/main and HEAD exact;
2. inspect Alembic heads/history;
3. require sole canonical current head:
   `20260916_0015`;
4. verify accepted `0013`, `0014`, `0015` bytes unchanged;
5. if any newer canonical migration exists or multi-head exists, STOP;
6. if PASS, create exactly:
   `migrations/versions/20260916_0016_public_live_limiter_retention.py`
7. revision:
   `20260916_0016`
8. down_revision:
   `20260916_0015`

If 0016 already exists unexpectedly, STOP.

## Phase R2 — implementation design

Before mutation write:

`LIMITER_RETENTION_IMPLEMENTATION_DESIGN.md`

It must document:

- exact retention table/index impact;
- cleanup serialization primitive;
- maintenance state shape, if used;
- prune function signature;
- flood function replacement behavior;
- lock/order/concurrency reasoning;
- failure semantics;
- why current bucket cannot be deleted;
- why SOURCE cardinality <= 1200/campaign/bucket under Public ingress;
- raw privilege model;
- rollback/downgrade implications.

Do not implement a background daemon.

## allowed DB mutation

Exactly one additive 0016 migration may:

- add index(es) on the existing limiter table strictly for expired-bucket pruning;
- add a bounded maintenance-state relation or equivalent narrow DB primitive;
- add mediated `SECURITY DEFINER` prune/maintenance function(s);
- `CREATE OR REPLACE` the existing accepted flood-consume function solely for the Human-approved CAMPAIGN-first/global-denied SOURCE short-circuit;
- add exact EXECUTE grants for mediated functions;
- revoke PUBLIC as required.

## forbidden DB mutation

- edit 0013/0014/0015;
- change 30/120/1200 values;
- alter L1/L2 state/budget/outbox tables;
- raw runtime DELETE/SELECT/INSERT/UPDATE/TRUNCATE grant on limiter tables;
- generic platform-wide retention framework;
- provider/deployment/config state;
- unrelated schema.

## cleanup correctness

Required logic:

- authoritative current minute bucket from DB clock;
- prune only `bucket < current_bucket - 9`;
- keep current + previous 9;
- never delete current-bucket rows;
- at most once per current bucket when maintenance state is already current;
- concurrent app instances safely serialize/reuse same-current-bucket successful maintenance state;
- unknown/stale maintenance state is not treated as safe;
- maintenance/prune error causes fail-closed limiter operation.

If database transactional behavior makes “at most once” require a slightly different internal locking mechanism, that mechanism is allowed only if externally visible semantics remain exact.

## campaign/source cardinality

The authoritative flood path must:

1. perform cleanup safety gate;
2. consume/check CAMPAIGN;
3. if campaign count > 1200:
   - return global denial;
   - do not materialize or increment SOURCE;
4. otherwise consume/check SOURCE;
5. preserve existing source 120 cap.

Must prove:

```text
new distinct SOURCE rows
per campaign/minute bucket
<= 1200
```

under requests solely through the mediated Public ingress function.

Do not claim this as a universal database row bound against privileged administrative/manual writes; the bound is for accepted Public ingress authority.

## read limiter

READ consume must also pass the cleanup safety gate.

No behavior change:

```text
30/min/run
valid capability only
invalid capability creates no READ row
```

## Python/HTTP changes

Modify Python/HTTP only when required to:

- call the new mediated maintenance-aware functions;
- map maintenance failure to existing accepted `503 LIVE_UNAVAILABLE`;
- preserve all existing L3 HTTP semantics.

Do not add public maintenance endpoint.

Do not expose prune controls to public callers.

## PostgreSQL runtime — explicitly authorized

Do not assume predecessor runtime exists.

```text
PostgreSQL:
17.6

image:
postgres:17.6 local cache only

network pull:
FORBIDDEN

container/volume:
CURRENT TASK OWNED

bind:
127.0.0.1:55432

private/pre-existing DB:
FORBIDDEN
```

Before DB tests emit:

`LOCAL_POSTGRES_RUNTIME.json`

Use the same task-owned DB for migration, cleanup, concurrency, HTTP regression and broader suite where applicable.

Cleanup task-owned runtime best-effort after evidence.

## required evidence

### `HUMAN_POLICY_AUTHORITY`

- accepted policy V1 present;
- status accepted;
- exact 10-bucket/global-short-circuit semantics mapped.

### `MIGRATION_TOPOLOGY`

- sole pre-head 0015;
- exactly one new 0016;
- 0013/0014/0015 unchanged.

### `RETENTION_DATABASE`

Prove:

- B-10 and older deleted when current is B;
- B-9 through B retained;
- current B never deleted;
- DB time, not caller time, controls threshold;
- cleanup state bounded and current-bucket-aware;
- no raw runtime table DELETE/DML privilege.

### `CARDINALITY_BOUND`

Prove:

- campaign request 1200 may source-account;
- request 1201+ global deny does not create/increment SOURCE;
- <=1200 distinct SOURCE rows/campaign/bucket under mediated ingress;
- SOURCE 120 cap unchanged;
- multiple source buckets aggregate to campaign cap.

### `CONCURRENCY`

Prove across independent DB connections/app service instances:

- cleanup/consume concurrency does not admit over 30/120/1200;
- cleanup cannot delete active current bucket;
- same-bucket maintenance serialization is safe;
- campaign-global short-circuit cannot race into >1200 new SOURCE identities.

### `FAIL_CLOSED`

Inject/observe maintenance failure and prove:

- HTTP/adapter result 503 `LIVE_UNAVAILABLE`;
- no L2 admission;
- no provider call;
- no WorkRun creation;
- no paid budget effect.

### `PRIVACY_SECURITY`

- no raw IP persisted/logged;
- opaque source buckets only;
- cleanup evidence contains aggregate bucket/row-count information only;
- public route gets no maintenance/delete authority.

### `REGRESSION`

Must include:

- limiter focused tests;
- L3 HTTP focused tests;
- accepted L2/public-live tests;
- broader repository suite supported by harness;
- no hidden skip/xfail/assertion dilution.

### `WORKSPACE_INTEGRITY`

- before/after HEAD/index/worktree;
- exact changed paths;
- no unrelated dirt mutation;
- no commit/push/deploy.

## blocker resolution candidate

Executor may report:

```text
PUBLIC_LIVE_LIMITER_RETENTION_RESOURCE_BOUND_UNRESOLVED
→ RESOLVED_CANDIDATE
```

only if all required implementation/evidence passes.

It MUST NOT claim final `RESOLVED`.

Browser Command Center owns final blocker resolution and later Git persistence acceptance.

## reuse_allowed

- L3 terminal acceptance at `bd46b40...` for unchanged L3 semantics;
- 0135/0405 shared-limiter and HTTP evidence as predecessor baseline only;
- no prior proof substitutes for new retention/cardinality evidence.

## human_owned

- final retention implementation acceptance;
- blocker final resolution;
- Git persistence authorization;
- L4/L5 selection;
- Public admission/release.

## forbidden

- L4 provider work;
- L5 Railway/deployment/trusted-proxy proof;
- real provider call;
- Public admission enablement;
- Git commit/push;
- deployment;
- policy redesign.

## accept candidate criteria

All applicable:

- expected HEAD exact;
- accepted policy exact;
- 0015 sole head pre-change;
- additive 0016 only;
- accepted migrations unchanged;
- 10-bucket retention exact;
- campaign 1201+ creates no SOURCE row;
- <=1200 Public SOURCE identities/campaign/minute;
- cleanup/concurrency PASS;
- raw DML remains denied;
- maintenance failure fail-closed;
- L1/L2/L3 regression green;
- Public admission remains disabled;
- provider calls = 0;
- no L4/L5 scope;
- no unrelated dirty mutation;
- report/export complete;
- no commit/push/deploy.

Final status may be:

`COMPLETED / RESOLVED_CANDIDATE`

It must not claim final blocker closure.

## mandatory stop

- HEAD mismatch;
- accepted policy missing/mismatch;
- migration topology not exact;
- 0015 must be edited rather than safely superseded;
- retention semantics cannot be implemented without weakening accepted rate/security boundaries;
- database cleanup semantics ambiguous in a mutation-critical way;
- L4/L5/provider/deployment required;
- cached PostgreSQL missing;
- unsafe port collision;
- unrelated dirty collision;
- evidence scope expansion beyond Task.

After blocker: minimum evidence, workspace inventory, report/export, safe task-owned cleanup only.

## export bundle

Target:

`.aiassistant/reports/target/20260916_0447_aiscc-p3-3-public-live-limiter-retention-resource-bound-implementation-1/`

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `LIMITER_RETENTION_IMPLEMENTATION_DESIGN.md`
- `MIGRATION_TOPOLOGY.json`
- `LOCAL_POSTGRES_RUNTIME.json`
- concise retention/cardinality/concurrency/fail-closed/privacy evidence
- changed/new source/test/migration preserving relative paths
- `REMOVED_FILES.md` only for actual deletion

## Task lifecycle

active:

`.aiassistant/tasks/active/20260916_0447_aiscc-p3-3-public-live-limiter-retention-resource-bound-implementation-1.md`

done after executor-required work/report/export:

`.aiassistant/tasks/done/20260916_0447_aiscc-p3-3-public-live-limiter-retention-resource-bound-implementation-1.md`

## final response

1. result
2. target bundle
3. accepted policy authority
4. migration topology / 0016
5. changed files
6. retention evidence
7. cardinality bound evidence
8. concurrency evidence
9. fail-closed evidence
10. privacy/security evidence
11. regression
12. Public admission before/after
13. provider calls
14. blocker status (`RESOLVED_CANDIDATE` only if proven)
15. cleanup/residue
16. human verification
17. unverified
18. preserved paths
