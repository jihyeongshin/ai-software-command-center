# 작업지시서: P3-3 Public Live Human-Authorized Shared Limiter + L3 Implementation Retry

## meta

- task_id: `20260916_0135_aiscc-p3-3-public-live-shared-limit-and-l3-implementation-human-policy-authorized-retry-1`
- created_at: `2026-09-16 KST`
- work_type: `REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `968a7164cb50cfeaee5a6f83b7455ab87f6ccbd1`
- primary_semantic_owner: `P3-3 Public Live shared-limit substrate + L3 Public-only HTTP API composition`
- predecessor_task: `20260916_0122_aiscc-p3-3-public-live-shared-limit-extension-and-l3-implementation-retry-1`

## current state

- branch: `main`
- expected HEAD: `968a7164cb50cfeaee5a6f83b7455ab87f6ccbd1`
- L1: `ACCEPTED / CLOSED`
- L2: `ACCEPTED / CLOSED`
- L3 stage: `Public-only HTTP API composition`
- L3 shared-limit policy: `HUMAN_PROVIDED / ACCEPTED V1`
- L3 implementation: `ENTRY_AUTHORIZED / NOT_STARTED`
- Public admission: `DISABLED`
- Public Live: `NOT_RELEASED`

Use the current IDE Executor conversation. No fresh chat is required.

## controlling policy authority

Read first:

`.aiassistant/reports/aiscc/20260916_0135_aiscc-p3-3-public-live-shared-limit-policy-amendment-v1-accepted.md`

Status must read:

`HUMAN_PROVIDED / ACCEPTED`

The older:

`.aiassistant/reports/aiscc/20260916_0133_aiscc-p3-3-public-live-shared-limit-policy-amendment-proposal-1.md`

is provenance only and must not override the accepted V1 amendment.

## historical authority

Accepted/frozen design commit:

`209e7534f66e9b07ce9d33742e6993370a70f4fb`

Read as needed:

- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_IMPLEMENTATION_SEQUENCE.json`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_HTTP_CONTRACT.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_ADMISSION_SECURITY_DESIGN.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_SECURITY_TEST_MATRIX.json`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_FAILURE_STATE_MACHINE.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_HUMAN_DECISIONS.md`

If frozen historical authority conflicts with the accepted 0135 amendment only on the previously unspecified shared-limit details, the 0135 accepted amendment controls those details.

For all other semantics, the frozen 209e design controls.

## current canonical must-read

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- `.aiassistant/rules/AISCC_SECURITY_SANDBOX.md`
- `.aiassistant/rules/AISCC_ORCHESTRATION.md`
- `.aiassistant/records/aiscc/cycles/20260916_0135_aiscc-p3-3-shared-limit-policy-human-acceptance-l3-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260916_0135_aiscc-browser-command-center-shared-limit-policy-human-acceptance-l3-retry-1.md`
- `.aiassistant/reports/aiscc/20260916_0135_aiscc-browser-command-center-shared-limit-policy-accepted-l3-retry-handoff-1.md`
- `.aiassistant/tasks/done/20260916_0122_aiscc-p3-3-public-live-shared-limit-extension-and-l3-implementation-retry-1.md`
- `src/aiscc/persistence/public_live.py`
- `src/aiscc/public_live/`
- `migrations/versions/20260916_0014_public_live_compatibility.py`

## exact Human-approved shared-limit contract

### authenticated run-read

Route:

`GET /v1/public-live/runs/{run_id}`

Counter key:

`canonical run_id`

Window:

```text
fixed 60-second bucket
database/server clock
floor(epoch_seconds / 60)
```

Cap:

`30 / run / bucket`

Counting:

- only capability-valid authenticated reads consume;
- invalid/missing/expired/non-matching capability reads do not consume read quota;
- those invalid reads still consume ingress flood quota.

Boundary:

- 1..30 allowed;
- 31+ denied;
- next DB bucket resets.

Denial:

```text
429
READ_RATE_LIMIT
retryable=true
Retry-After=1..60 seconds to next DB bucket boundary
Cache-Control=no-store
```

Backend unavailable:

```text
503 LIVE_UNAVAILABLE
retryable=true
no L2 admission
no paid/provider effect
```

### shared ingress flood

Protected surface:

`/v1/public-live/*`

Includes POST/GET/OPTIONS/unsupported methods/subpaths reaching the Public Live router.

Both dimensions must pass:

```text
source:
120 / 60 seconds / canonical opaque source bucket

campaign:
1200 / 60 seconds / campaign
```

Window:

`fixed 60-second DB-clock bucket`

Source identity:

- IPv4 `/32`
- IPv6 `/64`
- campaign-bound HMAC-SHA256 opaque bucket
- campaign/key version included
- raw IP not persisted/logged
- raw Forwarded/X-Forwarded-For not authority

Order:

```text
trusted normalized source identity
→ shared flood consume
→ CORS/origin/method/request-shape
→ capability/auth
→ run-read limit for authenticated GET
→ L2 admission/read
```

Every ingress request consumes once from both flood dimensions before expensive processing.

Malformed and OPTIONS requests consume flood quota.

Flood-denied requests consume no run-read quota, no paid admission budget, no provider budget, and create no WorkRun.

Flood denial:

```text
429
CLIENT_RATE_LIMIT
retryable=true
Retry-After=seconds until later reset among exceeded dimensions
Cache-Control=no-store
```

Backend unavailable:

```text
503 LIVE_UNAVAILABLE
retryable=true
no paid/admission/provider effect
```

## Phase S1 — migration topology

Before mutation:

1. verify HEAD exact;
2. inspect Alembic heads/history;
3. require current canonical head `20260916_0014`;
4. if `0014` is not the sole current head, STOP;
5. verify accepted `0013` and `0014` bytes unchanged.

If PASS, create exactly:

`migrations/versions/20260916_0015_public_live_shared_limits.py`

with:

```text
revision = 20260916_0015
down_revision = 20260916_0014
```

If this filename/revision already exists unexpectedly: STOP.

## Phase S2 — database shared-limit substrate

Implement only the minimum PostgreSQL substrate needed by the accepted policy.

Allowed new schema objects:

- narrow limiter relation(s);
- indexes/constraints only on those new relations;
- mediated atomic consume/check functions;
- exact runtime function EXECUTE grants;
- optional mediated diagnostic/read function strictly needed by tests/Retry-After.

Forbidden:

- edit accepted migrations;
- alter existing accepted Public Live table/column/index/type ownership;
- raw runtime SELECT/INSERT/UPDATE/DELETE on limiter tables;
- generic reusable platform-wide rate-limit framework;
- unrelated schema.

### required DB semantics

- server/DB clock owns bucket;
- fixed 60-second buckets;
- atomic consume;
- concurrency cannot exceed cap;
- source and campaign dimensions consumed atomically for one ingress attempt;
- if either flood dimension would deny, behavior must not partially create a successful admission-side effect;
- run-read limiter separate from flood limiter;
- invalid capability path never consumes run-read counter;
- opaque source identity only;
- no raw IP storage/logging;
- no WorkRun/provider/budget authority.

Choose a minimal schema/function design; document it in:

`SHARED_LIMIT_IMPLEMENTATION_DESIGN.md`

before implementation.

## source identity adapter boundary

L3 requires a server-owned trusted normalized source identity input.

Allowed for L3:

- a narrow server-owned source-identity abstraction/adapter;
- deterministic local/runtime-test implementation using trusted direct peer metadata;
- normalization to IPv4 `/32` or IPv6 `/64`;
- campaign-bound HMAC-SHA256 opaque bucket;
- no raw IP persistence/logging.

Forbidden:

- trusting raw Forwarded/X-Forwarded-For directly;
- claiming Railway/proxy trust configuration as proven;
- implementing L5 hosted ingress policy.

If current framework cannot supply a trustworthy direct-peer identity in local execution without L5 semantics, implement a fail-closed adapter boundary and prove it with local server-owned injection. Report hosted identity derivation as L5 pending.

## Python persistence/service boundary

Prefer existing Public Live persistence abstraction.

Route/middleware code must not directly mutate limiter tables.

Add only minimal wrapper functions for mediated DB API.

Existing process-memory throttle may remain as defense in depth but is not authoritative.

## PostgreSQL runtime — explicitly authorized

Do not assume predecessor runtime exists.

```text
postgres:17.6
LOCAL CACHE ONLY
network pull forbidden
task-owned container/volume
127.0.0.1:55432
private DB reuse forbidden
```

Before DB tests emit:

`LOCAL_POSTGRES_RUNTIME.json`

Use the same runtime for migration, shared-limit, L3 HTTP DB-backed, and regression evidence as applicable.

Cleanup current task-owned runtime best-effort after evidence.

## Phase S3 — shared-limit proof

Must prove:

### run read

- request 30 allowed;
- request 31 denied;
- next DB minute bucket reset;
- different run IDs isolated;
- invalid capability does not consume read quota;
- independent application/service instances share read counter;
- concurrent boundary cannot exceed 30.

### source flood

- request 120 allowed;
- request 121 denied;
- next DB minute bucket reset;
- independent source buckets isolated;
- independent application/service instances share source counter;
- concurrent boundary cannot exceed 120.

### campaign flood

- request 1200 allowed;
- request 1201 denied;
- aggregate across multiple source buckets;
- independent application/service instances share campaign counter;
- concurrent boundary cannot exceed 1200.

### composition

- one ingress request consumes both flood dimensions exactly once;
- malformed request consumes flood, not read/admission;
- OPTIONS consumes flood;
- flood denial prevents CORS/body/auth/L2/provider expensive side effects beyond safe denial handling;
- limiter backend failure => 503 fail-closed;
- raw limiter table access denied to runtime role.

Synthetic time acceleration or DB-clock control may be used in tests only if it does not change production semantics and is clearly test-owned.

## Phase L3 — continue in same turn

After S1-S3 PASS, continue immediately.

Frozen L3:

`Public-only HTTP API composition`

Do not stop merely because shared limiter implementation completed.

Reconfirm exact L3 route/HTTP/security matrix from historical authority.

## L3 expected responsibilities

Only when supported by frozen authority:

- public POST/GET route composition;
- request body/content-type/input limits;
- CORS/origin handling;
- capability handling;
- exact HTTP status/error mapping;
- safe non-disclosure;
- shared flood and read limiter integration;
- accepted L2 service binding;
- Replay/Live failure-domain separation.

## L3 non-goals

- L4 provider profile/model/credential;
- real provider paid call;
- L5 Railway/trusted proxy/deployment proof;
- L6/L7/L8;
- Public admission production enablement;
- public release;
- Git commit/push;
- deployment.

## local HTTP runtime

When HTTP runtime proof is required:

- loopback only;
- available local port;
- no external exposure;
- existing repository runtime/harness;
- emit `LOCAL_HTTP_RUNTIME.json`;
- provider calls = 0.

## evidence contract

### executor_required — `HUMAN_POLICY_AUTHORITY`

- accepted 0135 amendment read;
- status `HUMAN_PROVIDED / ACCEPTED`;
- exact limits/ordering mapped into implementation.

### executor_required — `MIGRATION_TOPOLOGY`

- sole head 0014 before;
- one additive 0015;
- accepted migrations unchanged.

### executor_required — `SHARED_LIMIT_DATABASE`

- schema/function least privilege;
- runtime raw DML denied;
- DB-clock fixed buckets;
- exact caps 30/120/1200.

### executor_required — `SHARED_LIMIT_CONCURRENCY`

- independent app/service instances share authoritative counters;
- concurrent cap proof for 30/120/1200;
- no partial/bypass behavior.

### executor_required — `SOURCE_IDENTITY_PRIVACY`

- IPv4 /32, IPv6 /64;
- HMAC opaque bucket;
- key/campaign version binding;
- raw IP not persisted/logged;
- forwarding headers not directly trusted;
- L5 hosted proxy proof clearly unverified.

### executor_required — `L3_HTTP_CONTRACT`

All frozen L3-applicable POST/GET/CORS/content-type/input/status/header/non-disclosure cases plus accepted limit responses.

### executor_required — `L3_INTEGRATION`

HTTP → shared limiter → accepted L2 with no bypass.

### executor_required — `SECURITY_SANDBOX`

- no free-form task;
- no arbitrary repo upload/URL;
- no arbitrary shell/network;
- no provider/model/credential selection;
- no paid provider call;
- limiter failure fail-closed.

### executor_required — `REGRESSION`

- shared limiter focused tests;
- L3 tests;
- accepted L2 tests;
- broader suite supported by repository harness;
- no hidden skip/xfail/assertion dilution.

### executor_required — `WORKSPACE_INTEGRITY`

- exact before/after HEAD/index/worktree;
- only authorized migration/shared-limit/L3/test/governance paths changed;
- no unrelated dirt mutation;
- no commit/push/deploy.

## reuse_allowed

- L2 terminal acceptance at `968a7164...` for unchanged semantics;
- frozen L3 authority resolution from predecessor;
- previous full-suite result only as baseline, not current proof.

## human_owned

- Browser Command Center shared-limit implementation acceptance;
- Browser Command Center L3 terminal acceptance;
- Git persistence authorization;
- L4/L5 selection;
- Public release.

## proof non-substitution

- policy accepted != implementation proven;
- one process limiter != shared proof;
- PostgreSQL limit proof != HTTP proof;
- local direct-peer identity != L5 trusted-proxy proof;
- local HTTP != Railway proof;
- L3 candidate != Browser terminal acceptance;
- L3 accepted != Public Live release.

## accept candidate criteria

All applicable:

- HEAD exact;
- accepted V1 policy consumed exactly;
- migration 0015 only after exact topology PASS;
- 0013/0014 unchanged;
- no unrelated existing schema mutation;
- 30/120/1200 shared limits proven;
- concurrency/cross-instance proof PASS;
- raw limiter table DML denied;
- source identity privacy PASS;
- exact frozen L3 HTTP/security matrix PASS;
- accepted L2 semantics unchanged;
- provider calls = 0;
- Public admission remains disabled;
- L4/L5/L6+ untouched;
- regression green;
- no skip/xfail/assertion dilution;
- report/export complete;
- no Git commit/push/deploy.

Final Executor result may be:

`COMPLETED / ACCEPTED_CANDIDATE`

It MUST NOT claim terminal L3 acceptance.

## mandatory stop

- HEAD mismatch;
- accepted policy file/status missing;
- migration topology mismatch;
- 0013/0014 changed;
- exact policy cannot be implemented without weakening accepted security;
- trusted normalized source identity cannot be established even as a fail-closed local adapter boundary;
- L4/L5/provider/deployment required;
- cached PostgreSQL missing;
- unsafe port collision;
- unrelated dirty collision;
- evidence scope expansion.

After blocker: minimum evidence, workspace inventory, report/export, task-owned cleanup only.

## export bundle

Target:

`.aiassistant/reports/target/20260916_0135_aiscc-p3-3-public-live-shared-limit-and-l3-implementation-human-policy-authorized-retry-1/`

Required root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `SHARED_LIMIT_IMPLEMENTATION_DESIGN.md`
- `MIGRATION_TOPOLOGY.json`
- `LOCAL_POSTGRES_RUNTIME.json`
- `RESOLVED_L3_AUTHORITY.json`
- `L3_RESOLVED_SCOPE.md`
- `LOCAL_HTTP_RUNTIME.json` when HTTP runtime used
- concise shared-limit/concurrency/privacy/HTTP/security evidence
- changed/new source/test/migration files preserving project-relative paths
- `REMOVED_FILES.md` only for actual deletion

## Task lifecycle

active:

`.aiassistant/tasks/active/20260916_0135_aiscc-p3-3-public-live-shared-limit-and-l3-implementation-human-policy-authorized-retry-1.md`

done after executor-required work/report/export:

`.aiassistant/tasks/done/20260916_0135_aiscc-p3-3-public-live-shared-limit-and-l3-implementation-human-policy-authorized-retry-1.md`

## final response

1. result
2. target bundle
3. accepted policy authority
4. migration topology / 0015
5. shared limiter implementation
6. changed files
7. PostgreSQL/runtime evidence
8. 30/120/1200 shared/concurrency evidence
9. source identity/privacy evidence
10. L3 HTTP evidence
11. security evidence
12. regression
13. Public admission before/after
14. provider calls
15. cleanup/residue
16. human verification
17. unverified
18. preserved paths
