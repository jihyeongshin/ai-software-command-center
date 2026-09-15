# 작업지시서: P3-3 Public Live L2 Atomic Admission Service Implementation

## meta

- task_id: `20260915_2325_aiscc-p3-3-public-live-l2-atomic-admission-service-implementation-1`
- created_at: `2026-09-15 KST`
- work_type: `BACKEND_IMPLEMENTATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `a2672c7a66bfd6b3d805caf2b187dae41b6181e5`
- primary_semantic_owner: `P3-3 Public Live L2 atomic admission service`
- ide_executor_session: `FRESH_CHAT_REQUIRED`

## 현재 상태

- branch: `main`
- expected HEAD: `a2672c7a66bfd6b3d805caf2b187dae41b6181e5`
- P3-3 Public Live L1: `ACCEPTED / CLOSED`
- Command Center broader baseline: `GREEN / ACCEPTED / CLOSED`
- predecessor full suite: `1220 PASS / 3 SKIP / 0 FAIL / 0 ERROR`
- L2: `SELECTED / ENTRY_AUTHORIZED / NOT_STARTED`
- L3: `BLOCKED_ON_L2`
- L4: `ENTRY_ELIGIBLE / SEPARATE`
- L5: `ENTRY_ELIGIBLE / SEPARATE`
- Public Live: `NOT_RELEASED`
- Public admission: `DISABLED`

## 이번 턴 목표

1. Human-accepted/frozen Public Live design package의 exact repository authority를 fail-closed 방식으로 resolve한다.
2. `PUBLIC_LIVE_IMPLEMENTATION_SEQUENCE.json`의 frozen L2 contract를 읽고 exact L2 scope를 확정한다.
3. accepted L1 persistence primitives 위에 L2 atomic admission service만 구현한다.
4. L2의 atomicity, idempotency, budget/admission fail-closed semantics와 concurrency behavior를 frozen design대로 검증한다.
5. L3/L4/L5/L6+ 범위를 침범하지 않는다.
6. report/export를 생성하고 Browser Command Center가 판정할 `ACCEPTED_CANDIDATE`를 제출한다.

## 이번 턴 비목표

- L3 public HTTP API/routes
- L4 real provider profile/configuration
- real provider paid call
- L5 Railway ingress, trusted proxy, hosted sandbox/deployment proof
- deployment/resource mutation
- public admission enablement
- campaign enablement
- frontend/browser UI
- Replay redesign
- L6/L7/L8
- release/submission
- new schema/migration unless the frozen L2 contract explicitly requires it; if it does, STOP and report design/scope conflict because L1 owns the accepted additive schema baseline
- architecture/policy redesign
- Git commit/push

## 절대 authority bootstrap gate — SOURCE MUTATION BEFORE PASS IS FORBIDDEN

Current Browser evidence knows the seven frozen artifact basenames, but does not claim exact current repository paths.

Before any product/test source mutation:

1. verify HEAD exactly equals:
   `a2672c7a66bfd6b3d805caf2b187dae41b6181e5`
2. using Git-tracked file inventory only, resolve each exact basename:
   - `PUBLIC_LIVE_ADMISSION_SECURITY_DESIGN.md`
   - `PUBLIC_LIVE_DB_SCHEMA_PLAN.md`
   - `PUBLIC_LIVE_HTTP_CONTRACT.md`
   - `PUBLIC_LIVE_FAILURE_STATE_MACHINE.md`
   - `PUBLIC_LIVE_IMPLEMENTATION_SEQUENCE.json`
   - `PUBLIC_LIVE_SECURITY_TEST_MATRIX.json`
   - `PUBLIC_LIVE_OPEN_DECISIONS.md`
3. each basename MUST resolve to exactly one tracked path.
4. zero matches or multiple matches => `BLOCKED_MISSING_ARTIFACT` / `POLICY_CONFLICT_INVESTIGATION_REQUIRED`; STOP before source mutation.
5. record the seven resolved exact paths and SHA-256 in `RESOLVED_L2_AUTHORITY.json`.
6. read all seven exact resolved paths.
7. verify their contents identify the accepted/frozen Public Live prerequisite design and are compatible with the accepted design lineage around commit `209e7534f66e9b07ce9d33742e6993370a70f4fb`.
8. extract the exact L2 entry/scope/dependencies from `PUBLIC_LIVE_IMPLEMENTATION_SEQUENCE.json`.
9. if the frozen package disagrees with this Task's high-level boundary, the frozen package wins only after reporting the conflict; DO NOT silently broaden. STOP as `POLICY_CONFLICT_INVESTIGATION_REQUIRED`.

Only after this gate passes may implementation begin.

## 반드시 읽을 exact known paths

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- `.aiassistant/rules/AISCC_SECURITY_SANDBOX.md`
- `.aiassistant/rules/AISCC_ORCHESTRATION.md`
- `.aiassistant/records/aiscc/cycles/20260915_2126_aiscc-p3-3-public-live-l1-terminal-acceptance-l2-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260915_2325_aiscc-command-center-baseline-regression-repair-terminal-closure-l2-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260915_2325_aiscc-browser-command-center-baseline-regression-repair-terminal-acceptance-l2-selection-1.md`
- `.aiassistant/reports/aiscc/20260915_2325_aiscc-browser-command-center-baseline-closed-public-live-l2-entry-handoff-1.md`
- plus all seven exact paths resolved by the authority bootstrap gate

Do not bulk-read unrelated rules/records/source/logs.

## accepted outer invariants

These are ceilings/boundaries, not a substitute for the frozen L2 design.

```text
PUBLIC_REPLAY_WITH_BOUNDED_LIVE

Public admission:
DISABLED until explicit later release authority

Replay/static path:
must remain available independently of Live/provider failure

Public free-form task:
FORBIDDEN

Public repository URL/upload:
FORBIDDEN

Public arbitrary shell/network:
FORBIDDEN

Live scenario scope:
ALLOWLIST_ONLY

Provider/model:
server-fixed; user cannot choose

Paid provider action in this Task:
FORBIDDEN
```

Public admission sequence baseline includes:

```text
LIVE_REQUEST
→ SCENARIO_ALLOWLIST_CHECK
→ IDEMPOTENCY / ABUSE CHECK
→ APPLICATION_BUDGET_CHECK
→ PROVIDER_AVAILABILITY CHECK
→ ISOLATED EXECUTION ADMISSION
→ BOUNDED RUN
→ TRUTHFUL RESULT LABEL
```

Implement only the L2-owned segment exactly as frozen by the seven design artifacts.

## L1 ownership boundary

L1 already owns accepted persistence/schema primitives.

Do not re-open L1 unless the frozen L2 contract proves an actual missing primitive.

If implementation appears to require:

- new migration,
- schema change,
- L1 invariant weakening,
- reservation/settlement semantic change,
- budget integer representation change,
- row-lock/clock invariant redesign,

STOP with `POLICY_CONFLICT_INVESTIGATION_REQUIRED` or `DOC_UPDATE_REQUIRED`.

Do not silently fold L1 rework into L2.

## allowed source discovery

After authority bootstrap passes:

- inspect only the L1 Public Live persistence/service modules and tests referenced by the resolved L2 design;
- inspect symbols explicitly named in the L2 implementation sequence;
- inspect narrow adjacent source necessary to bind those symbols.

Before source mutation, write to the temporary target bundle:

`L2_RESOLVED_SCOPE.md`

containing:

- seven resolved authority paths;
- exact L2 sequence entry;
- exact planned changed paths;
- exact planned new paths;
- proof channels;
- explicit excluded L3/L4/L5 paths/concerns.

If the frozen design does not support a narrow changed-path plan, STOP rather than broadening.

## allowed mutation scope

Mutation is allowed only after the authority and scope gates pass.

Allowed:

- exact L2 application/domain/service source paths derived from frozen L2 design;
- exact L2 unit/integration tests;
- minimal shared test helper changes directly required by L2;
- task/report/export artifacts.

Not allowed:

- HTTP route/controller/ASGI public endpoint implementation unless frozen sequence explicitly classifies it as L2; if ambiguous, STOP because L3 owns public HTTP.
- real provider adapter/profile/config changes;
- Railway/deployment config;
- frontend source;
- unrelated Command Center source;
- migrations/schema changes;
- canonical design edits.

## PostgreSQL runtime prerequisite — EXPLICITLY AUTHORIZED WHEN REQUIRED

Do not assume a predecessor PostgreSQL container exists.

If L2 DB/runtime evidence requires PostgreSQL:

```text
engine:
PostgreSQL 17.6

image:
postgres:17.6

image acquisition:
LOCAL CACHE ONLY

network image pull:
FORBIDDEN

container ownership:
CURRENT TASK ONLY

host bind:
127.0.0.1:55432

container port:
5432

private/pre-existing DB reuse:
FORBIDDEN
```

Preflight:

- inspect local cached `postgres:17.6`;
- if absent, DO NOT pull; STOP `BLOCKED_MISSING_ARTIFACT`;
- if `127.0.0.1:55432` is occupied by unrelated owner, do not kill/reuse it; STOP;
- do not start/reset/reuse private predecessor DBs.

Before DB tests create:

`LOCAL_POSTGRES_RUNTIME.json`

with version/image/cache/no-pull/container/loopback/health/redacted-URL/private-reuse=false evidence.

Use the same task-owned runtime through required L2 DB/concurrency evidence.

After evidence collection, cleanup only task-owned container/ephemeral volume best-effort.
Cleanup failure is `NON_BLOCKING_LOCAL_RESIDUE`, not automatic evidence invalidation.

## evidence contract

executor_required:

- channel: `AUTHORITY_RESOLUTION`
  scope: seven frozen Public Live artifacts
  pass_condition:
    - exactly one Git-tracked path per exact basename
    - all seven read
    - frozen L2 entry extracted
    - no authority conflict
    - `RESOLVED_L2_AUTHORITY.json` produced

- channel: `STATIC_SOURCE`
  scope: planned-vs-actual L2 changed paths and forbidden layer separation
  pass_condition:
    - only L2-owned source/tests changed
    - no L3/L4/L5/L6+ change
    - no migration/schema change
    - Public admission remains disabled

- channel: `UNIT_TEST`
  scope: exact L2 domain/service behavior required by frozen test matrix
  pass_condition: all applicable L2 unit tests PASS

- channel: `INTEGRATION_TEST`
  scope: exact L2 admission transaction/idempotency/fail-closed behavior required by frozen design
  pass_condition: all applicable L2 integration tests PASS

- channel: `DATABASE_RUNTIME`
  scope: only when required by frozen L2 matrix
  pass_condition:
    - PostgreSQL 17.6 isolated task runtime
    - no pull/private DB reuse
    - exact L2 atomicity/concurrency evidence PASS

- channel: `SECURITY_SANDBOX`
  scope: L2 admission boundary only
  pass_condition:
    - forbidden public inputs/capabilities do not become admitted work
    - no provider paid call
    - no public admission enablement
    - failure is fail-closed as frozen design requires

- channel: `REGRESSION`
  scope: directly affected accepted predecessor tests plus broader suite when current repository test harness supports it
  pass_condition:
    - no failure attributable to L2
    - Command Center repaired baseline remains green
    - any unrelated environment blocker is reported, not hidden

- channel: `WORKSPACE_INTEGRITY`
  scope: before/after HEAD/index/worktree and changed path inventory
  pass_condition:
    - no unrelated dirt mutation
    - no Git commit/push
    - exact changed-path attribution

reuse_allowed:

- channel: `L1_ACCEPTANCE`
  predecessor: `20260915_2126 L1 terminal acceptance`
  applicability_condition: L1 source/schema remains unchanged

- channel: `BASELINE_REPAIR`
  predecessor: `20260915_2325 baseline terminal closure`
  applicability_condition: repaired Command Center source remains unchanged

human_owned:

- channel: `BROWSER_COMMAND_CENTER_JUDGMENT`
  scope: L2 acceptance and Git persistence authorization
  expected_result_format: Browser judgment

- channel: `PUBLIC_RELEASE`
  scope: Public admission enablement / release
  expected_result_format: later Human release decision
  current_status: `NOT_ALLOWED_IN_L2`

not_required unless frozen design explicitly says otherwise:

- BROWSER_RUNTIME
- public HTTP route execution
- real provider call
- Railway deployment
- public release

forbidden:

- provider paid call
- network image pull
- private DB reuse
- public admission enablement
- deployment
- Git commit/push
- L3/L4/L5/L6+ implementation
- design baseline mutation

proof_non_substitution:

- `authority basename match != frozen design compatibility`
- `unit PASS != PostgreSQL atomicity proof`
- `HTTP artifact != L2 DB/runtime proof`
- `mock provider availability != real provider profile proof`
- `L2 executor report != Browser acceptance`
- `green targeted tests != public release readiness`
- `Public Live admission service implemented != Public Live enabled/released`

## conformance reporting

- applicability: `REQUIRED`
- applicable policy_or_invariant:
  - system-owned admission / fail-closed authority
  - accepted Public Live runtime boundary
  - frozen seven-document Public Live design
  - L1 persistence ownership
- required_actual_owner: `L2 atomic admission service`
- planned_vs_actual_scope: exact resolved L2 paths only
- rollback_or_failure_semantics:
  - authority ambiguity => STOP
  - schema/L1 gap => STOP, do not silently expand
  - L3/L4/L5 dependency needed => STOP and report exact dependency
  - runtime prerequisite unavailable => STOP with evidence
  - test failure => no Git persistence

## accept candidate 기준

All applicable conditions must hold:

- exact starting HEAD
- authority bootstrap PASS
- seven exact resolved design paths recorded
- exact frozen L2 entry recorded
- L2-only implementation
- no schema/migration change
- no Public admission enablement
- no L3/L4/L5/L6+ change
- no real provider call
- required unit/integration PASS
- required PostgreSQL atomicity/concurrency PASS when applicable
- security/fail-closed cases PASS
- directly affected regression PASS
- broader suite result honestly reported
- no guard/policy weakening
- no unrelated dirty mutation
- report/export complete
- no Git commit/push/deploy

Executor final result may be `COMPLETED / ACCEPTED_CANDIDATE`; it MUST NOT claim terminal L2 acceptance.

## hold/reject/stop 기준

- any frozen design basename missing or duplicated
- frozen design/Task conflict
- expected HEAD mismatch
- required L2 scope cannot be resolved narrowly
- schema/migration change required
- L1 accepted invariant must change
- L3/L4/L5 implementation required to make L2 pass
- cached PostgreSQL 17.6 missing when DB evidence required
- port collision
- private DB reuse required
- provider/network/credential action required
- public admission enablement required
- unrelated dirty collision
- security boundary ambiguity
- evidence scope expansion beyond Task

Named blocker 이후에는 minimum evidence, workspace inventory, report/export, task-owned cleanup만 수행한다.

## 보고서 필수 항목

- Task/work type/path
- starting branch/HEAD
- seven resolved authority paths + hashes
- frozen L2 sequence entry
- L2 resolved source scope
- source inventory
- product source changes
- governance/provenance changes
- repository config changes
- migration/schema changes
- Public admission status before/after
- provider call count
- PostgreSQL runtime evidence when used
- unit/integration/database/security/regression evidence
- Agent claim vs admitted evidence
- forbidden-not-run
- planned-vs-actual conformance
- mandatory stop/scope expansion
- cleanup/residue
- UTF-8/diff checks
- rollback
- preserved exact paths
- next recommendation

## export bundle 요구

Target:

`.aiassistant/reports/target/20260915_2325_aiscc-p3-3-public-live-l2-atomic-admission-service-implementation-1/`

Required root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `RESOLVED_L2_AUTHORITY.json`
- `L2_RESOLVED_SCOPE.md`
- `LOCAL_POSTGRES_RUNTIME.json` when PostgreSQL is used
- changed/new L2 files preserving project-relative paths
- `REMOVED_FILES.md` only when deletion exists

Task lifecycle:

- active:
  `.aiassistant/tasks/active/20260915_2325_aiscc-p3-3-public-live-l2-atomic-admission-service-implementation-1.md`
- done after executor-required work/report/export:
  `.aiassistant/tasks/done/20260915_2325_aiscc-p3-3-public-live-l2-atomic-admission-service-implementation-1.md`

## 최종 응답 형식

1. result: completed / blocked / rejected-candidate
2. target bundle path
3. authority bootstrap result
4. exact resolved L2 authority paths
5. changed files
6. migration/schema result
7. PostgreSQL runtime result
8. test/evidence results
9. Public admission before/after
10. provider call count
11. cleanup/residue
12. human verification
13. unverified items
14. preserved exact paths
