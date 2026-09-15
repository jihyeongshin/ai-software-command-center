# 작업지시서: P3-3 Public Live L2 Historical Design Authority Recovery + Implementation Retry

## meta

- task_id: `20260915_2340_aiscc-p3-3-public-live-l2-historical-design-authority-recovery-and-implementation-retry-1`
- created_at: `2026-09-15 KST`
- work_type: `REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `a2672c7a66bfd6b3d805caf2b187dae41b6181e5`
- primary_semantic_owner: `P3-3 Public Live L2 atomic admission service`
- predecessor_blocked_task: `20260915_2325_aiscc-p3-3-public-live-l2-atomic-admission-service-implementation-1`

## 현재 상태

- branch: `main`
- expected HEAD: `a2672c7a66bfd6b3d805caf2b187dae41b6181e5`
- L1: `ACCEPTED / CLOSED`
- Command Center baseline: `GREEN / ACCEPTED / CLOSED`
- L2: `ENTRY_AUTHORIZED / NOT_STARTED`
- Public Live: `NOT_RELEASED`
- Public admission: `DISABLED`

Known governance residue from the blocked predecessor may exist as untracked/tracked governance files. Do not treat known 2325/2340 Task/Cycle/Judgment/Handoff provenance as product dirty-workspace collision.

## critical correction

The previous Task's seven frozen design basenames were not source-backed.

They are **NOT authority requirements** for this retry.

Do not:

- require those names;
- restore them;
- infer repository loss from their absence;
- use them to define L2.

The actual recovery anchor is the accepted/frozen historical design commit.

## historical authority anchor

Expected accepted/frozen Public Live prerequisite design lineage:

```text
parent:
5e35ec0d60d84c7a05a2e58ebcc6560863879e5b

design commit:
209e7534f66e9b07ce9d33742e6993370a70f4fb

expected changed-path count:
30 exact
```

L1 implementation commit:

```text
3709c88fc0abd2f4219228ced931a9164f286dc4
parent = 209e7534f66e9b07ce9d33742e6993370a70f4fb
```

## 이번 턴 목표

This is one combined retry. Do not stop after successful discovery.

1. recover the exact 30-path historical Public Live design commit manifest;
2. prove the commit parent/count and accepted/frozen provenance;
3. identify the real historical file(s) that own the L2 atomic admission contract;
4. extract exact L2 scope, dependencies, non-goals, evidence/security requirements;
5. write a resolved authority/scope artifact before source mutation;
6. if and only if authority is unambiguous, continue in the SAME TURN and implement L2;
7. execute the frozen L2-required evidence;
8. submit an `ACCEPTED_CANDIDATE` or an exact blocker.

## 이번 턴 비목표

- re-design Public Live
- fabricate/restore nonexistent design filenames
- L3 public HTTP API unless historical L2 contract explicitly and unambiguously owns a narrow internal HTTP-independent piece; public route ownership remains presumed L3
- L4 real provider profile or paid provider call
- L5 Railway ingress/sandbox/deployment
- L6/L7/L8
- public admission enablement
- deployment
- Git commit/push
- unrelated Command Center work
- schema/migration change unless historical L2 contract unmistakably proves L2 owns it; if so STOP because accepted L1 ownership must be reconciled first

## must-read current canonical paths

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- `.aiassistant/rules/AISCC_SECURITY_SANDBOX.md`
- `.aiassistant/rules/AISCC_ORCHESTRATION.md`
- `.aiassistant/records/aiscc/cycles/20260915_2126_aiscc-p3-3-public-live-l1-terminal-acceptance-l2-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260915_2126_aiscc-p3-3-public-live-l1-terminal-browser-acceptance-1.md`
- `.aiassistant/reports/aiscc/20260915_2126_aiscc-browser-command-center-p3-3-public-live-l1-complete-nextaction-selection-handoff-1.md`
- `.aiassistant/tasks/done/20260915_2325_aiscc-p3-3-public-live-l2-atomic-admission-service-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260915_2340_aiscc-p3-3-l2-blocked-invalid-authority-artifact-assumption-rework-1.cycle.md`
- `.aiassistant/reports/aiscc/20260915_2340_aiscc-browser-command-center-p3-3-l2-blocked-invalid-authority-artifact-assumption-judgment-1.md`
- `.aiassistant/reports/aiscc/20260915_2340_aiscc-browser-command-center-p3-3-l2-historical-design-authority-recovery-retry-handoff-1.md`

If a listed 2126 artifact is missing, resolve its exact committed equivalent by exact filename/hash lineage; otherwise STOP.

## authority recovery gate

Before product/test source mutation:

### A. repository identity

Verify:

```text
HEAD == a2672c7a66bfd6b3d805caf2b187dae41b6181e5
branch == main
```

### B. historical commit identity

Verify both commits exist locally:

```text
5e35ec0d60d84c7a05a2e58ebcc6560863879e5b
209e7534f66e9b07ce9d33742e6993370a70f4fb
```

Verify `209e7534...` parent is exactly `5e35ec0d...`.

If commit/parent mismatch: `POLICY_CONFLICT_INVESTIGATION_REQUIRED` and STOP.

### C. exact 30-path manifest

Use Git historical diff/tree, not working-tree filename assumptions.

Recover:

```text
git diff --name-status 5e35ec0d... 209e7534...
```

or equivalent.

Pass condition:

```text
changed path count == 30 exact
```

Record all 30 paths, status, historical blob hash/SHA-256 where practical into:

`PUBLIC_LIVE_DESIGN_COMMIT_MANIFEST.json`

If count != 30: STOP before mutation.

### D. bounded historical content search

The exact 30-path set is the allowed historical discovery universe.

For each text artifact in the 30-path set, read its content at:

```text
209e7534:<path>
```

Do not require the file to exist at current HEAD.

Search within that bounded set for explicit evidence of:

- `L0`, `L1`, `L2`, `L3`, `L4`, `L5`, `L6`, `L7`, `L8`;
- `atomic admission`;
- admission service/transaction/orchestration;
- idempotency;
- application budget;
- provider availability boundary;
- isolated execution admission;
- failure/fail-closed semantics;
- security/evidence matrix;
- implementation sequence/order;
- L1/L2 ownership split.

Do not infer L2 from filename alone.

### E. acceptance/frozen provenance

Search repository governance/history narrowly using the exact commit hash `209e7534...` and/or exact design task/cycle identity discovered from the 30-path set.

Allowed search domains:

- `.aiassistant/tasks/done/**`
- `.aiassistant/records/aiscc/cycles/**`
- `.aiassistant/reports/aiscc/**`
- commit metadata for `209e7534...`

Required result:

- evidence that the design commit/package was accepted/frozen or was the direct accepted prerequisite parent for L1.

If no acceptance/frozen provenance is recoverable: STOP `POLICY_CONFLICT_INVESTIGATION_REQUIRED`.

### F. L2 owner resolution

Produce:

`RESOLVED_L2_AUTHORITY.json`

with:

- design commit;
- parent;
- exact 30-path manifest reference;
- exact historical authority paths for L2;
- each authority historical ref as `209e7534...:<path>`;
- SHA-256 of historical content;
- acceptance/frozen provenance refs;
- exact L2 stage name;
- exact dependencies;
- exact non-goals;
- exact required evidence;
- ambiguity flag.

Pass only when `ambiguity = false`.

### G. planned implementation scope

Before mutation, produce:

`L2_RESOLVED_SCOPE.md`

containing:

- quoted/short-paraphrased historical L2 contract refs;
- exact current source symbols/paths to change;
- exact tests to add/change;
- explicit L1 untouched paths;
- explicit L3/L4/L5+ exclusions;
- database/runtime evidence plan.

If exact implementation scope cannot be derived without design invention: STOP.

## current outer invariants

These remain hard ceilings:

```text
Public Live = PUBLIC_REPLAY_WITH_BOUNDED_LIVE
Public admission = DISABLED
Public free-form task = FORBIDDEN
Public repository upload/URL = FORBIDDEN
Public arbitrary shell/network = FORBIDDEN
Live scenario = ALLOWLIST_ONLY
Provider/model = server-fixed
Paid provider action in this Task = FORBIDDEN
Replay/static failure domain independent from Live
```

Agent/System/Human authority separation remains unchanged.

## L1 ownership boundary

L1 is accepted/closed at `3709c88f...`.

Do not change L1 persistence/schema invariants merely to simplify L2.

If historical L2 design requires an L1/schema change that is not already present:

- do not mutate;
- STOP with exact conflict;
- report `POLICY_CONFLICT_INVESTIGATION_REQUIRED` or `DOC_UPDATE_REQUIRED`.

## source discovery after authority pass

After `RESOLVED_L2_AUTHORITY.json` and `L2_RESOLVED_SCOPE.md` are PASS:

- inspect only current L1 Public Live modules named/referenced by historical design;
- inspect exact adjacent service/domain/repository symbols needed by L2;
- inspect directly affected tests.

No broad source-tree exploration.

## allowed mutation

Only exact L2-owned current application/domain/service source and directly affected tests resolved from accepted design.

No current canonical design-doc mutation.

No schema/migration source change.

No public route/controller layer unless historical L2 authority explicitly owns it and it does not conflict with the accepted L3 boundary; ambiguity => STOP.

No real provider/deployment source.

## PostgreSQL runtime prerequisite — EXPLICITLY AUTHORIZED WHEN REQUIRED

Do not assume predecessor DB runtime exists.

When historical L2 evidence requires PostgreSQL:

```text
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

private/pre-existing DB:
FORBIDDEN
```

Preflight:

1. local image inspect;
2. missing image => STOP, no pull;
3. unrelated port owner => STOP, do not kill/reuse;
4. create task-owned DB with synthetic task-local credentials;
5. emit `LOCAL_POSTGRES_RUNTIME.json` before DB tests;
6. same runtime through all DB/concurrency/regression evidence;
7. cleanup current task resources best-effort after evidence;
8. cleanup failure = non-blocking residue unless it changes test truth.

## evidence contract

executor_required:

### `HISTORICAL_AUTHORITY`
- exact parent/commit
- exact 30 paths
- acceptance/frozen provenance
- resolved L2 historical owner(s)
- `RESOLVED_L2_AUTHORITY.json`
- ambiguity false

### `STATIC_SOURCE`
- planned-vs-actual L2 paths
- no L1/schema/L3/L4/L5+ unauthorized change
- Public admission remains disabled

### `UNIT_TEST`
- all L2 unit behavior required by recovered historical contract

### `INTEGRATION_TEST`
- atomic admission/idempotency/fail-closed behavior required by recovered contract

### `DATABASE_RUNTIME`
- when required by recovered contract
- PostgreSQL 17.6 isolated runtime
- atomicity/concurrency evidence

### `SECURITY_SANDBOX`
- public untrusted input cannot obtain forbidden capability
- no provider paid call
- no user-selected provider/model/credential
- failure does not silently admit work

### `REGRESSION`
- directly affected predecessor tests
- repaired Command Center baseline remains green
- broader suite when supported by existing harness
- no hidden skip/xfail narrowing

### `WORKSPACE_INTEGRITY`
- before/after HEAD/index/worktree
- unrelated dirt unchanged
- no commit/push/deploy

reuse_allowed:

- L1 acceptance at `3709c88f...`, only if L1 source/schema unchanged;
- baseline repair evidence at `a2672c7...`, only if repaired test source unchanged.

human_owned:

- Browser Command Center terminal L2 acceptance;
- Git persistence authorization;
- Public admission/release.

forbidden:

- invented authority artifact names;
- design reconstruction from memory;
- schema/migration mutation;
- L3/L4/L5/L6+ implementation;
- real provider paid call;
- network image pull;
- private DB reuse;
- public admission enablement;
- deployment;
- Git commit/push.

proof_non_substitution:

- historical commit existence != accepted design provenance;
- filename match != L2 ownership;
- unit test != DB atomicity;
- local DB proof != Railway/deployment proof;
- mock provider availability != L4 real provider proof;
- executor completed != Browser accepted;
- L2 implemented != Public Live released.

## accept candidate 기준

All applicable:

- expected HEAD exact;
- design commit/parent exact;
- 30-path manifest exact;
- accepted/frozen provenance recovered;
- L2 historical authority resolved with ambiguity false;
- L2-only implementation;
- no L1/schema/migration mutation;
- no L3/L4/L5+ expansion;
- Public admission remains disabled;
- provider paid calls = 0;
- required tests/evidence PASS;
- repaired baseline not regressed;
- no skip/xfail/assertion dilution;
- report/export complete;
- no commit/push/deploy.

Final Executor result may be:

```text
COMPLETED / ACCEPTED_CANDIDATE
```

It MUST NOT claim terminal L2 acceptance.

## mandatory stop

- HEAD mismatch;
- design commit missing;
- parent mismatch;
- historical changed path count != 30;
- accepted/frozen provenance unavailable;
- L2 owner ambiguous;
- historical design conflicts with accepted L1/current canonical policy;
- L1/schema change required;
- L3/L4/L5 dependency required to fake L2 completion;
- PostgreSQL prerequisite unavailable when required;
- security ambiguity;
- unrelated dirty collision;
- evidence scope expansion.

After named blocker: minimum evidence, workspace inventory, report/export, safe task-owned cleanup only.

## export bundle

Target:

`.aiassistant/reports/target/20260915_2340_aiscc-p3-3-public-live-l2-historical-design-authority-recovery-and-implementation-retry-1/`

Required root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `PUBLIC_LIVE_DESIGN_COMMIT_MANIFEST.json`
- `RESOLVED_L2_AUTHORITY.json`
- `L2_RESOLVED_SCOPE.md`
- `LOCAL_POSTGRES_RUNTIME.json` when DB runtime is used
- changed/new L2 files preserving project-relative paths
- `REMOVED_FILES.md` only for actual source deletion

## Task lifecycle

active:

`.aiassistant/tasks/active/20260915_2340_aiscc-p3-3-public-live-l2-historical-design-authority-recovery-and-implementation-retry-1.md`

done after executor-required work/report/export:

`.aiassistant/tasks/done/20260915_2340_aiscc-p3-3-public-live-l2-historical-design-authority-recovery-and-implementation-retry-1.md`

## final response

1. result
2. target bundle
3. historical design commit/parent/path-count verification
4. resolved L2 historical authority refs
5. acceptance/frozen provenance
6. changed files
7. schema/migration result
8. PostgreSQL runtime result
9. test/evidence results
10. Public admission before/after
11. provider call count
12. cleanup/residue
13. human verification
14. unverified items
15. preserved exact paths
