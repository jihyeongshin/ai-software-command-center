# 작업지시서: P3-3 Public Live Shared-Limit Extension + L3 Implementation Retry

## meta

- task_id: `20260916_0122_aiscc-p3-3-public-live-shared-limit-extension-and-l3-implementation-retry-1`
- created_at: `2026-09-16 KST`
- work_type: `REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `968a7164cb50cfeaee5a6f83b7455ab87f6ccbd1`
- primary_semantic_owner: `P3-3 Public Live shared limiter prerequisite + L3 Public-only HTTP API composition`
- predecessor_task: `20260916_0110_aiscc-p3-3-public-live-l3-frozen-http-stage-implementation-1`

## current state

- branch: `main`
- expected HEAD: `968a7164cb50cfeaee5a6f83b7455ab87f6ccbd1`
- L1: `ACCEPTED / CLOSED`
- L2: `ACCEPTED / CLOSED`
- L3 authority: `RESOLVED`
- L3 implementation: `BLOCKED_ON_SHARED_LIMIT_SUBSTRATE`
- Public admission: `DISABLED`
- Public Live: `NOT_RELEASED`

Use the current IDE Executor conversation. No fresh chat is required.

## predecessor accepted finding

The predecessor resolved the frozen L3 stage as:

```text
Public-only HTTP API composition
depends_on:
L2
```

It also established before source mutation:

- frozen L3 requires a shared per-run read limit of `30 requests / minute`;
- frozen L3 requires a separate shared flood limit;
- current throttle is process-memory scoped;
- current accepted Public Live DB API has no shared limiter primitive sufficient to prove those requirements;
- L3 Task scope did not authorize a substrate/schema extension, so it stopped correctly.

Do not repeat the earlier authority-discovery work except as needed to bind exact limiter semantics.

## goal

One combined turn:

```text
C1 exact limiter contract recovery
→ C2 current shared-primitive audit
→ C3 narrow shared limiter implementation if required
→ C4 PostgreSQL/security/concurrency proof
→ L3 HTTP implementation
→ L3 HTTP/security/regression evidence
→ Browser ACCEPTED_CANDIDATE
```

Do not stop after C3/C4 if the prerequisite passes.

## frozen authority

Accepted/frozen design commit:

`209e7534f66e9b07ce9d33742e6993370a70f4fb`

Read historical objects directly:

- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_IMPLEMENTATION_SEQUENCE.json`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_HTTP_CONTRACT.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_ADMISSION_SECURITY_DESIGN.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_SECURITY_TEST_MATRIX.json`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_FAILURE_STATE_MACHINE.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_HUMAN_DECISIONS.md`

Current canonical must-read:

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- `.aiassistant/rules/AISCC_SECURITY_SANDBOX.md`
- `.aiassistant/rules/AISCC_ORCHESTRATION.md`
- `.aiassistant/records/aiscc/cycles/20260916_0122_aiscc-p3-3-l3-blocked-missing-shared-rate-limit-authority-rework-1.cycle.md`
- `.aiassistant/reports/aiscc/20260916_0122_aiscc-browser-command-center-p3-3-l3-blocked-shared-rate-limit-authority-judgment-1.md`
- `.aiassistant/reports/aiscc/20260916_0122_aiscc-browser-command-center-p3-3-shared-limit-l3-retry-handoff-1.md`
- `.aiassistant/tasks/done/20260916_0110_aiscc-p3-3-public-live-l3-frozen-http-stage-implementation-1.md`
- `src/aiscc/persistence/public_live.py`
- `src/aiscc/public_live/`
- `migrations/versions/20260916_0014_public_live_compatibility.py`

## C1 — exact shared-limit contract recovery

Before product/test/migration mutation, write:

`L3_SHARED_LIMIT_CONTRACT.md`

It must recover from frozen authority, with exact historical refs:

### per-run read limiter

Known accepted value:

```text
30 requests / minute / run
```

Resolve exactly:

- which GET/read route(s) it applies to;
- run identity key;
- requester/session/IP involvement, if any;
- window algorithm semantics if specified;
- boundary behavior;
- denial HTTP status/body/header semantics;
- whether failed/not-found reads consume;
- whether duplicate reads consume;
- clock/time-source expectations;
- fail-open vs fail-closed behavior.

### separate flood limiter

Do NOT invent values.

Resolve exactly from frozen authority:

- protected route/action set;
- limiter key/dimension;
- exact cap;
- exact window;
- burst semantics if specified;
- denial behavior;
- whether it composes with the 30/min run limiter;
- order of checks;
- evidence/test-matrix case IDs.

If any mutation-critical limiter semantic is not specified or conflicts across frozen artifacts:

`POLICY_CONFLICT_INVESTIGATION_REQUIRED` and STOP.

## C2 — current shared-primitive audit

Narrowly inspect current accepted source for an existing cross-instance shared limiter.

A qualifying existing primitive must be:

- authoritative/shared across independent service instances;
- durable or atomically shared in a common backend;
- exact-key/window semantics compatible with C1;
- concurrency-safe;
- fail-closed as required;
- least privilege;
- covered by usable tests.

A Python dict/cache/process-local throttle does NOT qualify.

Before mutation write:

`SHARED_LIMIT_SUBSTRATE_AUDIT.md`

with:

- inspected exact paths/symbols;
- qualifying primitive found: yes/no;
- reuse plan or missing-gap proof.

If a qualifying primitive exists, reuse it and do not create a migration.

## C3 — additive shared limiter substrate, only when C2 = missing

This Task explicitly authorizes a narrow database extension.

### migration topology gate

Before creating anything:

1. inspect Alembic heads/history;
2. require current applicable head to be `20260916_0014` unless a new unrelated canonical successor already exists;
3. multi-head/unknown lineage => STOP;
4. never edit any existing accepted migration.

### allowed database mutation

Exactly one additive successor migration is permitted.

Its scope may contain only the minimum shared limiting substrate required by C1:

- narrow Public Live limiter persistence relation(s), when required;
- indexes/constraints on those new limiter relation(s) only;
- mediated atomic check/consume function(s);
- minimum read function/view only if required for evidence/HTTP headers;
- runtime EXECUTE privilege only on exact mediated functions.

Existing accepted Public Live tables may be referenced by foreign key only if the frozen contract and lifecycle make that necessary; do not alter their columns/indexes/ACLs.

### forbidden database mutation

- edit `20260915_0013` or `20260916_0014`;
- alter/drop existing accepted columns/tables/indexes/types;
- grant runtime raw SELECT/INSERT/UPDATE/DELETE on limiter/public tables;
- broad schema usage/ownership expansion;
- provider/deployment/config data;
- arbitrary generic rate-limit framework.

### shared limiter invariants

The DB/backend authority must, as applicable to C1:

- atomically check and consume in one transaction/statement boundary;
- prevent concurrent requests from exceeding the exact cap;
- be shared by independent application/service instances;
- never use client-provided count/window truth;
- use server/database time when frozen semantics require server authority;
- fail closed on unavailable/ambiguous limiter state according to C1;
- preserve exact limiter dimensions;
- make duplicate/retry accounting behavior explicit;
- not mint L2 admission/workflow authority;
- not spend provider budget or create WorkRuns by itself.

In-memory limiting may remain only as optional defense in depth; it is not the admitted shared proof.

## C4 — Python adapter / persistence boundary

Add only the minimum wrapper/service needed for L3 to call the mediated shared limiter.

Prefer the established Public Live persistence abstraction.

Do not put shared-authority truth solely in HTTP middleware memory.

Do not give route code raw SQL/table access.

## PostgreSQL runtime — explicitly authorized

Do not assume predecessor runtime exists.

```text
engine:
PostgreSQL 17.6

image:
postgres:17.6

source:
LOCAL CACHE ONLY

network pull:
FORBIDDEN

container/volume:
CURRENT TASK OWNED ONLY

host bind:
127.0.0.1:55432

private/pre-existing DB reuse:
FORBIDDEN
```

Before DB evidence emit:

`LOCAL_POSTGRES_RUNTIME.json`

Use the same task-owned runtime for:

- migration proof;
- limiter concurrency/shared-instance proof;
- L3 DB-backed HTTP proof;
- directly affected regression/full suite when applicable.

Cleanup task-owned resources best-effort after evidence.

## shared-limit evidence

Executor-required.

### migration/schema

Prove:

- current accepted migrations unchanged;
- exactly one new successor when C2 required it;
- only new limiter relation(s)/functions/indexes/constraints introduced;
- no unrelated schema/ACL drift.

### permission/security

Using the runtime role, prove:

- mediated consume/check allowed;
- raw limiter table read/write denied unless an exact frozen read projection explicitly requires a mediated view/function;
- public existing table permissions unchanged;
- invalid limiter key/action fails closed.

### exact per-run read behavior

Prove the frozen `30/min/run` semantics exactly.

At minimum, if consistent with C1:

- allowed requests through limit;
- first request above limit denied;
- different run key isolated;
- independent app/service instances share the same counter;
- concurrent boundary requests cannot exceed cap;
- window reset behavior as frozen;
- HTTP denial mapping exact when L3 is implemented.

Do not assume these examples override C1 if the frozen contract specifies a different counting boundary.

### flood behavior

Execute the exact frozen flood cases and dimensions from C1/security matrix.

Must include shared/cross-instance proof, not merely one in-memory app instance.

## continue into L3

If C1–C4 pass, continue in the same turn.

Use the previously resolved L3 stage:

`Public-only HTTP API composition`

Reconfirm the exact L3 exit/test-matrix mapping from historical authority, then implement L3 only.

## L3 allowed mutation

Only exact paths required for:

- Public Live HTTP/router/request/response composition;
- CORS/origin/content-type/input limits as frozen;
- shared limiter adapter/binding;
- accepted L2 service binding;
- directly affected tests.

Minimal changes to existing app/router configuration are allowed only when required to mount the L3 routes.

## L3 forbidden scope

- L2 semantic redesign unrelated to shared limiting;
- L4 provider profile/model/credential implementation;
- real provider paid call;
- L5 Railway/deployment/supervisor/hosted ingress proof;
- L6/L7/L8;
- production Public admission enablement;
- arbitrary repo upload/URL;
- free-form task;
- arbitrary shell/network;
- user-selected provider/model/credential;
- Git commit/push;
- deployment.

## local HTTP runtime

If runtime HTTP proof is required:

- bind loopback only;
- use an available local port;
- no external exposure;
- emit `LOCAL_HTTP_RUNTIME.json`;
- use local synthetic/fake downstream boundaries only;
- provider calls = 0.

## evidence contract

### executor_required — `SHARED_LIMIT_AUTHORITY`

- `L3_SHARED_LIMIT_CONTRACT.md`
- exact frozen refs/test IDs
- no ambiguity

### executor_required — `SHARED_LIMIT_SUBSTRATE`

- current primitive audit
- reuse or exact additive backend
- cross-instance shared proof
- concurrency cap proof
- fail-closed proof

### executor_required — `MIGRATION_TOPOLOGY`

When new DB substrate is required:

- single successor;
- accepted migrations unchanged;
- narrow new limiter schema only.

### executor_required — `DATABASE_RUNTIME`

- PostgreSQL 17.6 local-cache/no-pull
- task-owned
- permission proof
- shared/concurrency proof.

### executor_required — `L3_HTTP_CONTRACT`

All frozen L3-applicable POST/GET/CORS/content/input/status/header/read-limit/flood cases.

### executor_required — `L3_INTEGRATION`

HTTP → shared limiter → accepted L2 binding, with no admission bypass.

### executor_required — `SECURITY_SANDBOX`

- no free-form task;
- no repo URL/upload;
- no arbitrary shell/network;
- no provider/model/credential selection;
- shared limit cannot be bypassed by process-local partition;
- failure is fail-closed.

### executor_required — `REGRESSION`

- limiter focused tests;
- L3 directly affected tests;
- accepted L2 tests;
- broader suite when repository harness supports it;
- no hidden skip/xfail narrowing.

### executor_required — `WORKSPACE_INTEGRITY`

- exact before/after HEAD/index/worktree;
- exact changed paths;
- no unrelated dirt mutation;
- no commit/push/deploy.

## reuse_allowed

- L2 terminal acceptance at `968a7164...` only for unchanged L2 semantics;
- predecessor L3 authority resolution may be reused after historical refs still resolve;
- predecessor `1278 PASS / 3 SKIP / 0 FAIL / 0 ERROR` is baseline only, not current proof.

## human_owned

- Browser Command Center shared-substrate acceptance;
- Browser Command Center L3 terminal acceptance;
- Git persistence authorization;
- L4/L5 selection;
- Public release.

## proof non-substitution

- in-memory throttle PASS != shared limiter proof;
- single app instance != cross-instance shared proof;
- DB limiter proof != L3 HTTP contract proof;
- local HTTP != Railway/hosted ingress proof;
- fake provider boundary != L4 provider proof;
- L3 candidate != Browser acceptance;
- L3 accepted != Public Live release.

## accept candidate criteria

All applicable:

- expected HEAD exact;
- frozen limiter semantics unambiguous;
- qualifying shared substrate exists or narrow additive extension succeeds;
- no accepted migration modified;
- shared/cross-instance/concurrency limits PASS;
- exact 30/min read behavior PASS;
- exact frozen flood behavior PASS;
- direct raw table authority not widened;
- L3 HTTP/security cases PASS;
- accepted L2 semantics preserved;
- provider calls = 0;
- Public admission remains disabled;
- L4/L5/L6+ untouched;
- regression green;
- no skip/xfail/assertion dilution;
- no unrelated dirt mutation;
- report/export complete;
- no commit/push/deploy.

Final Executor result may be:

`COMPLETED / ACCEPTED_CANDIDATE`

It MUST NOT claim terminal L3 acceptance.

## mandatory stop

- HEAD mismatch;
- frozen limiter semantic ambiguity;
- migration multi-head/lineage conflict;
- existing accepted schema must be weakened/changed;
- shared enforcement cannot be achieved within narrow Public Live substrate;
- flood semantics absent/conflicting;
- provider/deployment/L4/L5 work required;
- cached PostgreSQL missing when DB extension is required;
- port collision not safely avoidable;
- security ambiguity;
- unrelated dirty collision;
- evidence scope expansion beyond this Task.

After blocker: minimum evidence, workspace inventory, report/export, task-owned cleanup only.

## export bundle

Target:

`.aiassistant/reports/target/20260916_0122_aiscc-p3-3-public-live-shared-limit-extension-and-l3-implementation-retry-1/`

Required root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `L3_SHARED_LIMIT_CONTRACT.md`
- `SHARED_LIMIT_SUBSTRATE_AUDIT.md`
- `MIGRATION_TOPOLOGY.json` when migration is created
- `LOCAL_POSTGRES_RUNTIME.json` when PostgreSQL is used
- `RESOLVED_L3_AUTHORITY.json`
- `L3_RESOLVED_SCOPE.md`
- `LOCAL_HTTP_RUNTIME.json` when HTTP runtime is used
- changed/new source/test/migration files preserving project-relative paths
- concise shared-limit/HTTP/security/test evidence
- `REMOVED_FILES.md` only when actual deletion exists

## Task lifecycle

active:

`.aiassistant/tasks/active/20260916_0122_aiscc-p3-3-public-live-shared-limit-extension-and-l3-implementation-retry-1.md`

done after executor-required work/report/export:

`.aiassistant/tasks/done/20260916_0122_aiscc-p3-3-public-live-shared-limit-extension-and-l3-implementation-retry-1.md`

## final response

1. result
2. target bundle
3. shared-limit frozen contract
4. current substrate audit
5. migration/topology result
6. changed files
7. PostgreSQL/shared/concurrency evidence
8. L3 HTTP evidence
9. security evidence
10. regression
11. Public admission before/after
12. provider calls
13. cleanup/residue
14. human verification
15. unverified
16. preserved paths
