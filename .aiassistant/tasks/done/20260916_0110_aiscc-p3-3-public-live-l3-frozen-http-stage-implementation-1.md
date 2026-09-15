# 작업지시서: P3-3 Public Live L3 Frozen HTTP Stage Implementation

## meta

- task_id: `20260916_0110_aiscc-p3-3-public-live-l3-frozen-http-stage-implementation-1`
- created_at: `2026-09-16 KST`
- work_type: `BACKEND_IMPLEMENTATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `968a7164cb50cfeaee5a6f83b7455ab87f6ccbd1`
- primary_semantic_owner: `P3-3 Public Live frozen L3 stage`

## current state

- branch: `main`
- expected HEAD: `968a7164cb50cfeaee5a6f83b7455ab87f6ccbd1`
- L1: `ACCEPTED / CLOSED`
- L2: `ACCEPTED / CLOSED`
- L3: `ENTRY_AUTHORIZED / NOT_STARTED`
- L4: `ENTRY_ELIGIBLE / SEPARATE`
- L5: `ENTRY_ELIGIBLE / SEPARATE`
- L6: `BLOCKED_ON_L3_L4_L5`
- Public admission: `DISABLED`
- Public Live: `NOT_RELEASED`

Use the current IDE Executor conversation. No fresh chat is required.

## goal

Recover the exact frozen L3 contract from historical accepted design and, if unambiguous, implement only L3 in the same turn.

Do not stop after successful authority discovery.

## authority anchor

Accepted/frozen design commit:

`209e7534f66e9b07ce9d33742e6993370a70f4fb`

Read historical objects directly:

- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_IMPLEMENTATION_SEQUENCE.json`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_HTTP_CONTRACT.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_ADMISSION_SECURITY_DESIGN.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_SECURITY_TEST_MATRIX.json`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_FAILURE_STATE_MACHINE.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_HUMAN_DECISIONS.md`

Also read current canonical:

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- `.aiassistant/rules/AISCC_SECURITY_SANDBOX.md`
- `.aiassistant/rules/AISCC_ORCHESTRATION.md`
- `.aiassistant/records/aiscc/cycles/20260916_0110_aiscc-p3-3-public-live-l2-terminal-acceptance-l3-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260916_0110_aiscc-browser-command-center-public-live-l2-terminal-acceptance-l3-selection-1.md`
- `.aiassistant/reports/aiscc/20260916_0110_aiscc-browser-command-center-public-live-l2-complete-l3-entry-handoff-1.md`

## authority gate — before source mutation

Produce `RESOLVED_L3_AUTHORITY.json` containing:

- design commit;
- exact implementation-sequence L3 object;
- exact L3 stage title;
- dependencies;
- entry criteria;
- exit criteria;
- non-goals;
- exact historical refs/hashes;
- applicable security-test-matrix case IDs;
- ambiguity flag.

Pass only if:

```text
ambiguity = false
dependency on L2 is satisfied by current accepted commit
```

If L3 in the frozen sequence has another unmet dependency, STOP and report it.

Do not rename or reinterpret the stage.

## scope gate

Before mutation produce `L3_RESOLVED_SCOPE.md` with:

- exact current framework/route integration path(s);
- exact current L2 service symbols used;
- request parsing and validation ownership;
- response/status mapping ownership;
- CORS/origin/header/content-type rules if frozen L3 owns them;
- replay-vs-live failure-domain behavior;
- exact tests to add/change;
- explicit L4/L5/L6+ exclusions;
- DB/runtime plan if required.

If scope cannot be derived without invention: STOP.

## expected outer boundary

The Browser shorthand expects L3 to be the public HTTP-facing stage, but this shorthand is NOT authority.

Historical frozen design controls.

No source mutation should rely solely on the phrase "public HTTP".

## L2 binding boundary

Current accepted L2 is implemented under:

- `src/aiscc/public_live/`
- `src/aiscc/persistence/public_live.py`
- migration head `20260916_0014`

Do not redesign L2.

L3 may call the accepted L2 API and map frozen HTTP inputs/outcomes around it.

If L3 requires L2 semantic mutation or new DB schema:

- STOP;
- do not silently fold L2 rework into L3.

## allowed source discovery

After authority gate:

- locate the current server/router/framework entrypoint by exact existing route conventions;
- inspect only directly adjacent HTTP/router/error-mapping/config symbols needed for L3;
- inspect existing CORS/security middleware only if frozen L3 contract requires it;
- inspect directly affected tests.

Do not broad-read unrelated app modules.

## allowed mutation

Only exact L3-owned:

- HTTP/router/request/response integration source;
- minimal public-live HTTP adapter/service binding;
- directly affected unit/integration tests;
- task/report/export artifacts.

Existing L2 source may be imported/used but not semantically rewritten.

## forbidden scope

- L4 real provider profile/model/credential implementation;
- real paid provider calls;
- L5 Railway/deployment/supervisor/hosted ingress proof;
- L6 integrated release;
- public release/enablement;
- arbitrary repo upload/URL;
- free-form task submission;
- arbitrary shell/network;
- user-selected provider/model/credential;
- Git commit/push;
- deployment;
- design-baseline mutation.

## PostgreSQL/runtime lifecycle — explicitly authorized when required

If frozen L3 tests require DB-backed HTTP execution:

```text
PostgreSQL:
17.6

image:
postgres:17.6

source:
LOCAL CACHE ONLY

network pull:
FORBIDDEN

container/volume:
CURRENT TASK OWNED

host bind:
127.0.0.1:55432

private DB reuse:
FORBIDDEN
```

Do not assume predecessor runtime exists.

Before DB-backed tests emit `LOCAL_POSTGRES_RUNTIME.json`.

Use task-local synthetic credentials only.

Cleanup task-owned runtime best-effort after evidence.

## HTTP/local server evidence

If a local HTTP server is required:

- bind loopback only;
- use an available local port;
- do not expose externally;
- use existing repository run/test harness;
- no deployment;
- no Cloudflare/Railway mutation.

Record local HTTP runtime identity in `LOCAL_HTTP_RUNTIME.json`.

## evidence contract

### executor_required — `L3_AUTHORITY`

- frozen L3 sequence object recovered;
- exact historical refs/hashes;
- applicable test matrix cases mapped;
- ambiguity false.

### executor_required — `STATIC_SOURCE`

- exact L3-only changed paths;
- L2 semantic source unchanged unless only import/export plumbing explicitly allowed by frozen design;
- no L4/L5/L6+ implementation;
- Public admission production state remains disabled.

### executor_required — `HTTP_CONTRACT`

Execute all frozen L3-applicable cases for:

- method/path;
- content type;
- input shape/size;
- request identity/idempotency mapping;
- status/error mapping;
- origin/CORS/header behavior;
- replay/live separation;
- safe denial/fail-closed behavior.

Exact cases are derived from historical matrix, not invented here.

### executor_required — `INTEGRATION_TEST`

- HTTP adapter → accepted L2 service binding;
- no admission bypass;
- typed denial remains truthful;
- duplicate/retry semantics preserve L2 identity rules;
- malformed/oversized requests fail before forbidden work;
- no real provider send.

### executor_required — `DATABASE_RUNTIME`

Only when frozen L3 applicable tests require DB-backed L2 interaction.

### executor_required — `SECURITY_SANDBOX`

- no free-form task;
- no repository URL/upload;
- no arbitrary shell/network;
- no user-selected provider/model/credential;
- origin/CORS/security rules as frozen;
- failure is fail-closed.

### executor_required — `REGRESSION`

- L3 directly affected tests;
- accepted L2 tests remain green;
- broader suite when supported by repository harness;
- no hidden skip/xfail narrowing.

### executor_required — `WORKSPACE_INTEGRITY`

- before/after HEAD/index/worktree;
- exact changed-path attribution;
- no unrelated dirt mutation;
- no Git commit/push/deploy.

## reuse allowed

- L2 terminal acceptance at `968a7164...` for unchanged L2 semantics;
- 2336 PostgreSQL/full-suite evidence as predecessor baseline only, not current L3 proof.

## human owned

- Browser Command Center L3 terminal acceptance;
- Git persistence authorization;
- L4/L5 selection;
- public release.

## proof non-substitution

- HTTP unit test != DB-backed L2 binding proof;
- local HTTP != Railway ingress proof;
- mock/synthetic provider boundary != L4 real provider proof;
- L3 accepted != Public Live released;
- Executor candidate != Browser terminal acceptance.

## accept candidate criteria

All applicable:

- expected HEAD exact;
- frozen L3 authority unambiguous;
- L2 dependency satisfied;
- L3-only implementation;
- exact frozen HTTP/security cases PASS;
- no admission bypass;
- no L2/schema redesign;
- no L4/L5/L6+ scope;
- real provider calls = 0;
- Public admission production state remains disabled;
- directly affected regression PASS;
- broader suite honestly reported;
- no skip/xfail/assertion dilution;
- no unrelated dirt mutation;
- report/export complete;
- no commit/push/deploy.

Final executor result may be:

`COMPLETED / ACCEPTED_CANDIDATE`

It MUST NOT claim terminal L3 acceptance.

## mandatory stop

- HEAD mismatch;
- frozen L3 stage missing/ambiguous;
- unmet dependency other than L2;
- L2 semantic/schema change required;
- L4/L5 dependency required to fake L3 completion;
- forbidden external/provider/deployment action required;
- PostgreSQL prerequisite unavailable when required;
- local port collision that cannot be resolved without unrelated mutation;
- security ambiguity;
- unrelated dirty collision;
- evidence scope expansion.

After blocker: minimum evidence, workspace inventory, report/export, task-owned cleanup only.

## export bundle

Target:

`.aiassistant/reports/target/20260916_0110_aiscc-p3-3-public-live-l3-frozen-http-stage-implementation-1/`

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `RESOLVED_L3_AUTHORITY.json`
- `L3_RESOLVED_SCOPE.md`
- `LOCAL_HTTP_RUNTIME.json` when local HTTP runtime is used
- `LOCAL_POSTGRES_RUNTIME.json` when PostgreSQL is used
- changed/new L3 files preserving relative paths
- concise HTTP/security/test evidence artifacts
- `REMOVED_FILES.md` only when actual deletion exists

## Task lifecycle

active:

`.aiassistant/tasks/active/20260916_0110_aiscc-p3-3-public-live-l3-frozen-http-stage-implementation-1.md`

done after executor-required work/report/export:

`.aiassistant/tasks/done/20260916_0110_aiscc-p3-3-public-live-l3-frozen-http-stage-implementation-1.md`

## final response

1. result
2. target bundle
3. resolved L3 stage/title/dependencies
4. authority refs
5. changed files
6. HTTP contract evidence
7. PostgreSQL/local HTTP runtime evidence
8. security evidence
9. regression
10. Public admission before/after
11. provider calls
12. cleanup/residue
13. human verification
14. unverified
15. preserved paths
