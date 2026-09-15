# 작업지시서: P3-3 Public Live L1 Compatibility Extension + L2 Implementation Retry

## meta

- task_id: `20260915_2336_aiscc-p3-3-public-live-l1-compatibility-extension-and-l2-implementation-retry-1`
- created_at: `2026-09-15 KST`
- work_type: `REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `a2672c7a66bfd6b3d805caf2b187dae41b6181e5`
- primary_semantic_owner: `P3-3 Public Live L1→L2 compatibility + L2 atomic admission service`
- predecessor_task: `20260915_2340_aiscc-p3-3-public-live-l2-historical-design-authority-recovery-and-implementation-retry-1`

## 현재 상태

- branch: `main`
- expected HEAD: `a2672c7a66bfd6b3d805caf2b187dae41b6181e5`
- historical Public Live design: accepted/frozen at `209e7534f66e9b07ce9d33742e6993370a70f4fb`
- L1 original implementation: `ACCEPTED / CLOSED`
- Command Center repaired baseline: `GREEN / ACCEPTED / CLOSED`
- L2 authority: `RESOLVED / AMBIGUITY FALSE`
- L2 implementation: `BLOCKED_ON_L1_COMPATIBILITY_API`
- Public Live: `NOT_RELEASED`
- Public admission: `DISABLED`

Use the current IDE Executor conversation. No fresh chat is required.

## accepted predecessor finding

The predecessor established through static source evidence:

1. frozen L2/failure semantics require durable state projection including `UNKNOWN_OUTCOME`, `GOVERNANCE_PENDING`, and truthful terminal projections;
2. accepted L1 API has no permitted runtime API for those `public_run.state` writes;
3. direct runtime table DML is denied and must remain denied;
4. therefore L2 cannot be correctly implemented without a narrow mediated L1 compatibility API;
5. admission-context/rate read support may also require a narrow projection, but necessity must be derived from frozen L2 authority.

Do not re-open the earlier invalid seven-basename issue.

## 이번 턴 목표

This is one combined execution turn.

### Phase C1 — Compatibility contract derivation

1. re-read the relevant historical frozen authority directly at commit `209e7534...`;
2. derive the exact allowed durable run-state transitions and required preconditions;
3. determine whether L2 actually requires a minimum admission-context/rate projection;
4. bind the extension to existing L1 lock/version/permission invariants.

### Phase C2 — Additive L1→L2 compatibility implementation

5. verify Alembic migration topology;
6. create a new additive migration successor to the accepted L1 migration;
7. add only mediated API function/view/grant surface needed for L2;
8. expose it through the existing Python persistence transaction abstraction where appropriate;
9. preserve direct DML denial and least privilege;
10. prove the compatibility extension on isolated PostgreSQL 17.6.

### Phase L2 — Continue immediately when C2 passes

11. implement L2 `Atomic admission and durable reconciliation service`;
12. execute frozen L2 unit/integration/database/security evidence;
13. execute directly affected regression and broader suite when supported;
14. produce Browser Command Center `ACCEPTED_CANDIDATE`.

Do NOT stop after C1/C2 merely because the prerequisite was successfully implemented. Continue to L2 in the same turn.

## 이번 턴 비목표

- retroactively reject L1
- edit accepted `20260915_0013` migration
- table/column/index/type schema redesign
- L3 public HTTP routes/controllers
- L4 real provider profile or real paid provider call
- L5 Railway ingress/sandbox/deployment
- L6/L7/L8
- public admission enablement
- frontend/browser UI
- design baseline mutation
- Git commit/push
- deployment

## must-read current paths

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- `.aiassistant/rules/AISCC_SECURITY_SANDBOX.md`
- `.aiassistant/rules/AISCC_ORCHESTRATION.md`
- `.aiassistant/tasks/done/20260915_2340_aiscc-p3-3-public-live-l2-historical-design-authority-recovery-and-implementation-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260915_2336_aiscc-p3-3-l2-authority-resolved-l1-api-gap-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260915_2336_aiscc-browser-command-center-p3-3-l2-authority-resolved-l1-api-gap-judgment-1.md`
- `.aiassistant/reports/aiscc/20260915_2336_aiscc-browser-command-center-p3-3-l1-compatibility-l2-implementation-retry-handoff-1.md`
- `src/aiscc/persistence/public_live.py`
- `migrations/versions/20260915_0013_public_live_persistence_primitives.py`
- `tests/integration/public_live/test_persistence.py`

Historical frozen authority to read directly from Git object at `209e7534f66e9b07ce9d33742e6993370a70f4fb`:

- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_ADMISSION_SECURITY_DESIGN.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_DB_SCHEMA_PLAN.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_FAILURE_STATE_MACHINE.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_IMPLEMENTATION_SEQUENCE.json`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_SECURITY_TEST_MATRIX.json`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_HUMAN_DECISIONS.md`

Read HTTP contract only if an L2 question actually requires it; do not implement L3 HTTP.

## Phase C1 gate — exact compatibility contract

Before mutation, write:

`L1_L2_COMPATIBILITY_CONTRACT.md`

It must identify from frozen authority:

- exact durable run states L2 must project;
- exact allowed predecessor→target transitions;
- whether transitions are monotonic/terminal;
- required current-version/CAS behavior;
- required owner/admission/marker predicates;
- which role owns the write;
- required failure semantics for stale/invalid/duplicate calls;
- whether rate/admission context read projection is truly required;
- minimum fields if such read projection is required;
- why direct table DML remains forbidden;
- exact historical refs supporting each rule.

No invented transition is allowed.

If frozen authority is ambiguous on a mutation that must be implemented:
`POLICY_CONFLICT_INVESTIGATION_REQUIRED` and STOP.

## Phase C2 gate — migration topology

Before creating migration:

1. inspect Alembic heads/history locally;
2. verify `20260915_0013` represents the expected accepted L1 predecessor lineage;
3. require a single applicable current head for this branch;
4. if another migration already succeeds 0013, use the actual current head only when it is unrelated and the additive extension can cleanly depend on it without changing accepted semantics; report exact lineage;
5. if multi-head/conflict/unknown migration ownership exists: STOP.

### migration mutation policy

DO NOT edit:

`migrations/versions/20260915_0013_public_live_persistence_primitives.py`

Allowed:

- exactly one new additive migration for L1→L2 compatibility;
- function definitions under the existing mediated API schema;
- minimum safe view/function if C1 proves admission-context read is required;
- EXECUTE/SELECT grants only to the existing runtime role as needed;
- revoke/default-deny posture consistent with L1.

Forbidden:

- new/altered public tables;
- add/drop/alter table columns;
- new indexes;
- raw table UPDATE/SELECT grants to runtime;
- ownership transfer;
- SECURITY boundary widening unrelated to the compatibility function;
- bypassing version/lock/admission predicates.

If a table/column/index change is actually required: STOP and report, do not perform it.

## compatibility API semantics

Exact function names/signatures are derived from existing naming conventions and C1; do not invent broad APIs.

Required safety properties, when supported by frozen authority:

- state mutation is mediated;
- target state is allowlisted;
- invalid predecessor→target transition fails closed;
- stale expected version fails closed;
- mutation and version increment are atomic;
- duplicate/idempotent requests do not create contradictory state;
- terminal state cannot silently revert;
- runtime still cannot direct-DML public tables;
- safe status truthfully reflects committed state;
- state projection cannot independently mint workflow/Judgment authority outside the frozen Public Live runtime contract.

If admission-context/rate projection is required:

- expose only minimum fields needed by L2;
- no raw rate-table SELECT grant;
- preserve lock-order/retention invariants;
- do not reconstruct authority from unrelated broad reads.

## Python persistence API

Update `src/aiscc/persistence/public_live.py` only as needed to expose the new mediated compatibility surface through the established transaction abstraction.

Do not move SQL authorization logic into Python.

Do not create a Python path that bypasses the DB permission boundary.

## L2 implementation scope

After C2 tests pass, continue directly.

Use the recovered frozen authority:

```text
L2:
Atomic admission and durable reconciliation service

depends_on:
L1
```

Expected L2 current source namespace may include new narrow files under:

- `src/aiscc/public_live/`
- `tests/unit/public_live/`
- `tests/integration/public_live/`

but actual paths/symbols must be recorded in `L2_RESOLVED_SCOPE.md` before L2 mutation.

Do not implement L3 public HTTP.

Do not implement real provider sending.

Unique outbox/admission binding, idempotency, budget/slot/marker ordering, reconciliation and frozen failure projection must follow recovered authority.

## PostgreSQL runtime — EXPLICITLY AUTHORIZED

When DB evidence begins, do not assume any predecessor runtime exists.

```text
engine:
PostgreSQL 17.6

image:
postgres:17.6

image source:
LOCAL CACHE ONLY

network pull:
FORBIDDEN

container/volume:
CURRENT TASK OWNED

host bind:
127.0.0.1:55432

container port:
5432

private/pre-existing DB reuse:
FORBIDDEN
```

Preflight:

- inspect cached image;
- missing image => STOP without pull;
- unrelated 55432 owner => STOP without killing/reusing it;
- task-local synthetic credentials only.

Before DB tests write:

`LOCAL_POSTGRES_RUNTIME.json`

Use the same task-owned runtime for:

- migration upgrade proof;
- compatibility API tests;
- L2 integration/concurrency/crash tests;
- directly affected regression/full suite where appropriate.

Cleanup only task-owned container/volume after evidence, best effort.

## evidence contract

### executor_required — `COMPATIBILITY_AUTHORITY`

Pass:

- `L1_L2_COMPATIBILITY_CONTRACT.md`
- exact historical refs
- no unresolved semantic ambiguity

### executor_required — `MIGRATION_TOPOLOGY`

Pass:

- current heads/history recorded
- accepted 0013 lineage preserved
- exactly one additive migration
- no edit to 0013
- no table/column/index schema mutation

### executor_required — `DATABASE_RUNTIME`

Pass:

- isolated PostgreSQL 17.6
- local cache / no pull
- no private DB reuse
- migration applies cleanly
- permission boundary tests run on runtime role

### executor_required — `COMPATIBILITY_API`

At minimum prove applicable cases:

- allowed state projection PASS;
- invalid transition DENIED;
- stale version DENIED;
- duplicate/idempotent behavior truthful;
- terminal rollback/reversion denied when frozen contract requires terminality;
- direct table DML still denied;
- safe status reflects committed durable state;
- minimum admission-context read works only if C1 required it;
- raw table SELECT remains denied.

### executor_required — `L2_UNIT`

Exact frozen L2 unit behavior PASS.

### executor_required — `L2_INTEGRATION`

Frozen L2 atomic admission/reconciliation behavior PASS.

### executor_required — `L2_CONCURRENCY_CRASH`

Include frozen applicable two-worker/double-settlement/crash/marker ordering/outbox-owner-binding proofs.

### executor_required — `SECURITY_SANDBOX`

- no public arbitrary capability;
- no user-selected provider/model/credential;
- no real provider call;
- no public admission enablement;
- failure paths fail closed.

### executor_required — `REGRESSION`

- accepted L1 persistence tests;
- repaired Command Center tests directly affected;
- broader existing suite when supported;
- no hidden skip/xfail narrowing.

### executor_required — `WORKSPACE_INTEGRITY`

- exact before/after HEAD/index/worktree;
- only authorized compatibility/L2/test/governance paths changed;
- no unrelated dirt mutation;
- no Git commit/push/deploy.

## reuse_allowed

- historical authority recovery from predecessor 2340 may be reused only after commit/hash refs still resolve;
- L1 acceptance may be reused for untouched existing invariants;
- baseline repair full suite may be reused as predecessor baseline, not current proof.

## human_owned

- Browser Command Center L1 compatibility acceptance;
- Browser Command Center L2 terminal acceptance;
- Git persistence authorization;
- public admission/release.

## forbidden

- direct runtime public-table DML grant;
- editing 0013;
- table/column/index schema mutation;
- design baseline edits;
- L3/L4/L5/L6+ implementation;
- real provider paid calls;
- network image pull;
- private DB reuse;
- public admission enablement;
- deployment;
- Git commit/push.

## proof non-substitution

- migration applied != compatibility permission proof
- compatibility API PASS != L2 implementation PASS
- unit PASS != DB concurrency/crash proof
- local PostgreSQL != Railway proof
- mock provider availability != L4 proof
- executor candidate != Browser acceptance
- L2 implemented != Public Live released

## accept candidate 기준

All applicable:

- expected HEAD;
- C1 contract unambiguous;
- additive migration topology valid;
- accepted 0013 untouched;
- no table/column/index schema mutation;
- compatibility permission/API proofs PASS;
- L2-only service implementation after compatibility;
- required L2 unit/integration/concurrency/crash/security PASS;
- Public admission remains disabled;
- provider paid calls = 0;
- L3/L4/L5+ untouched;
- regression green;
- no skip/xfail/assertion dilution;
- report/export complete;
- no commit/push/deploy.

Final executor status may be:

`COMPLETED / ACCEPTED_CANDIDATE`

It must not claim terminal acceptance.

## mandatory stop

- expected HEAD mismatch;
- historical frozen semantics ambiguous;
- migration graph conflict/multi-head uncertainty;
- table/column/index schema change required;
- existing L1 invariant must be weakened;
- direct DML grant required;
- L3/L4/L5 required to fake L2 completion;
- cached PostgreSQL missing;
- loopback port collision;
- security boundary ambiguity;
- unrelated dirty collision;
- evidence scope expansion.

After blocker: minimum evidence, workspace inventory, report/export, safe task-owned cleanup only.

## export bundle

Target:

`.aiassistant/reports/target/20260915_2336_aiscc-p3-3-public-live-l1-compatibility-extension-and-l2-implementation-retry-1/`

Required root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `L1_L2_COMPATIBILITY_CONTRACT.md`
- `MIGRATION_TOPOLOGY.json`
- `L2_RESOLVED_SCOPE.md`
- `LOCAL_POSTGRES_RUNTIME.json` when DB runtime used
- changed/new source/test/migration files preserving relative paths
- relevant concise test/evidence artifacts
- `REMOVED_FILES.md` only when deletion exists

## Task lifecycle

active:

`.aiassistant/tasks/active/20260915_2336_aiscc-p3-3-public-live-l1-compatibility-extension-and-l2-implementation-retry-1.md`

done after executor-required work/report/export:

`.aiassistant/tasks/done/20260915_2336_aiscc-p3-3-public-live-l1-compatibility-extension-and-l2-implementation-retry-1.md`

## final response

1. result
2. target bundle
3. compatibility contract result
4. migration topology/new migration
5. changed files
6. schema/table change result
7. PostgreSQL runtime
8. compatibility API evidence
9. L2 evidence
10. regression
11. Public admission before/after
12. provider call count
13. cleanup/residue
14. human verification
15. unverified
16. preserved paths
