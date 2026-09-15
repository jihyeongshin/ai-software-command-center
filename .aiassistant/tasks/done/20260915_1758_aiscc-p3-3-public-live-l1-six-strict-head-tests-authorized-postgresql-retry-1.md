# 작업지시서: P3-3 Public Live L1 six-strict-head-tests-authorized PostgreSQL retry

## meta

- task_id: `20260915_1758_aiscc-p3-3-public-live-l1-six-strict-head-tests-authorized-postgresql-retry-1`
- created_at: `2026-09-15T17:58:10+09:00`
- work_type: `IMPLEMENTATION_RETRY`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- fresh_ide_chat_required: `No`
- primary_semantic_owner: `P3-3 Public Live L1 persistence primitives`

## objective

Replace the 1751 numeric maximum-two ambiguity gate with exact authority for the six discovered strict Alembic head assertions, then resume the complete L1 implementation.

## transport ordering

1. verify outer ZIP SHA-256 / exact four members / CRC;
2. read this Task from the authenticated ZIP;
3. verify the exact pre-delivery repository baseline below;
4. place this Task FIRST at:
   `.aiassistant/tasks/active/20260915_1758_aiscc-p3-3-public-live-l1-six-strict-head-tests-authorized-postgresql-retry-1.md`;
5. re-read/re-hash canonical active Task;
6. place Cycle/Judgment/Handoff from the exact companion manifest.

Before terminal export move current Task to:

`.aiassistant/tasks/done/20260915_1758_aiscc-p3-3-public-live-l1-six-strict-head-tests-authorized-postgresql-retry-1.md`

## exact companion manifest

- member: `20260915_1758_aiscc-p3-3-public-live-l1-six-head-assertions-discovered-accepted-retry-entry-1.cycle.md`
  - destination: `.aiassistant/records/aiscc/cycles/20260915_1758_aiscc-p3-3-public-live-l1-six-head-assertions-discovered-accepted-retry-entry-1.cycle.md`
  - SHA-256: `35974a318a79f77e6ab54527bcb507ef93cba6fc5d01de9dddc6a53486daadb2`
- member: `20260915_1758_aiscc-p3-3-public-live-l1-head-assertion-scope-browser-judgment-1.md`
  - destination: `.aiassistant/reports/aiscc/20260915_1758_aiscc-p3-3-public-live-l1-head-assertion-scope-browser-judgment-1.md`
  - SHA-256: `0d043548664f365a6820beeebc404c53991ff532ce8082d192109941aed1e2db`
- member: `20260915_1758_aiscc-browser-command-center-p3-3-public-live-l1-six-head-tests-authorized-retry-entry-handoff-1.md`
  - destination: `.aiassistant/reports/aiscc/20260915_1758_aiscc-browser-command-center-p3-3-public-live-l1-six-head-tests-authorized-retry-entry-handoff-1.md`
  - SHA-256: `98cc974b4191537e5e0a026eebdd6bc3520af37703de6516f8fc267c3ad19afb`

Any collision with differing bytes => STOP `TRANSPORT_CANONICAL_COLLISION`.

## exact pre-delivery repository baseline

Require:

```text
branch = main
HEAD = 209e7534f66e9b07ce9d33742e6993370a70f4fb
index = empty
tracked worktree = clean
Git-visible untracked = 20 exact
Git-visible Python bytecode = 0
```

Expected 20 provenance files:

- `.aiassistant/records/aiscc/cycles/20260915_1702_aiscc-p3-3-live-prerequisite-design-frozen-l1-entry-1.cycle.md`
  - SHA-256 `fcc34bc99f4e285c8dcdfe696d3b5db70fe12e076461361d70a9b293cbfaa758`
- `.aiassistant/records/aiscc/cycles/20260915_1718_aiscc-p3-3-public-live-l1-test-environment-blocker-accepted-retry-entry-1.cycle.md`
  - SHA-256 `6ed0ebb242df3cebc99d4d080d8844506199e6dca9869ceeffb3fed178570b2d`
- `.aiassistant/records/aiscc/cycles/20260915_1723_aiscc-p3-3-public-live-l1-transport-contract-blocker-accepted-retry-entry-1.cycle.md`
  - SHA-256 `20cbe1737132e2b06d31014f4db8f8d04be9d51a3103651c3b531b8beced9659`
- `.aiassistant/records/aiscc/cycles/20260915_1743_aiscc-p3-3-public-live-l1-bytecode-residue-blocker-accepted-retry-entry-1.cycle.md`
  - SHA-256 `d3df523580e2eb0f115e4e2a56e4f7c7101664cdf19d40c34da8b545b9237530`
- `.aiassistant/records/aiscc/cycles/20260915_1751_aiscc-p3-3-public-live-l1-migration-policy-block-accepted-retry-entry-1.cycle.md`
  - SHA-256 `fd182f220455531e6483a96c755f68bdc9cb3fce35dc99d3d5b1ff321f76b60b`
- `.aiassistant/reports/aiscc/20260915_1702_aiscc-browser-command-center-p3-3-public-live-l1-implementation-entry-handoff-1.md`
  - SHA-256 `be0ea77af7091b8e57df34868a2e475c7bed89b7dcec7d4619107c5c2d4ab870`
- `.aiassistant/reports/aiscc/20260915_1702_aiscc-p3-3-live-prerequisite-design-freeze-final-browser-acceptance-1.md`
  - SHA-256 `cba13ba6e9215f23ef4277fe72d240ce9eefdf70d7023e111111ddc943f379bc`
- `.aiassistant/reports/aiscc/20260915_1718_aiscc-browser-command-center-p3-3-public-live-l1-postgresql-runtime-retry-entry-handoff-1.md`
  - SHA-256 `3beac2a74fc07069a92aa727c127c6508f033fc094188309915f99eb5b5bc235`
- `.aiassistant/reports/aiscc/20260915_1718_aiscc-p3-3-public-live-l1-test-environment-blocker-browser-judgment-1.md`
  - SHA-256 `52c23f98f821195bf0a47935f3903fdc5af588ee286ab47d53df63ae292d3d36`
- `.aiassistant/reports/aiscc/20260915_1723_aiscc-browser-command-center-p3-3-public-live-l1-transport-corrected-retry-entry-handoff-1.md`
  - SHA-256 `6a3398c2ad6cbd66adfa83b339bd89395b1f32310b1f8a528878bf55ed844d0c`
- `.aiassistant/reports/aiscc/20260915_1723_aiscc-p3-3-public-live-l1-transport-contract-browser-judgment-1.md`
  - SHA-256 `c024b161e973dad78c1bf36831e14ab515ec27aedb7d041ba8160825f241deda`
- `.aiassistant/reports/aiscc/20260915_1743_aiscc-browser-command-center-p3-3-public-live-l1-bytecode-clean-retry-entry-handoff-1.md`
  - SHA-256 `f504d2d2153698d6346e9dcbfa1c01bb0d70228c391850a5f72e6b23ab5856dd`
- `.aiassistant/reports/aiscc/20260915_1743_aiscc-p3-3-public-live-l1-bytecode-residue-browser-judgment-1.md`
  - SHA-256 `5a44e454b8c1ccab68010977ebb4c0bf3608760f5c6bfc7155044b3690ef5c09`
- `.aiassistant/reports/aiscc/20260915_1751_aiscc-browser-command-center-p3-3-public-live-l1-migration-scope-expanded-retry-entry-handoff-1.md`
  - SHA-256 `6103eb7a64a1c15800512e35172847bacbd85a4e340d394d166e742b881c03bb`
- `.aiassistant/reports/aiscc/20260915_1751_aiscc-p3-3-public-live-l1-migration-policy-block-browser-judgment-1.md`
  - SHA-256 `69afedc579ce90bf2d5488cbb020862847490b0b0c722ecc49839611177f3c1b`
- `.aiassistant/tasks/done/20260915_1702_aiscc-p3-3-public-live-l1-schema-repository-transaction-primitives-implementation-1.md`
  - SHA-256 `102f79a47601c00a8496e1a77a5ddb99d9a5af083d86b215a9c266f4de3df2af`
- `.aiassistant/tasks/done/20260915_1718_aiscc-p3-3-public-live-l1-postgresql-runtime-authorized-implementation-retry-1.md`
  - SHA-256 `32cd6d2e6dbf497c1f5c0382cecf1fef1ddbb46b043afe40ec9890504b46fad8`
- `.aiassistant/tasks/done/20260915_1723_aiscc-p3-3-public-live-l1-transport-manifest-corrected-postgresql-retry-1.md`
  - SHA-256 `4c3279e14c5ee9b866037ea61f347f7157abbb5abf23d1f1e7738198ce3c24a7`
- `.aiassistant/tasks/done/20260915_1743_aiscc-p3-3-public-live-l1-bytecode-residue-cleanup-authorized-postgresql-retry-1.md`
  - SHA-256 `f97f2aa72ca7cd5661455f6e6f3dd5e0acf1a1e63f69a68e4bc98d82a79d0cff`
- `.aiassistant/tasks/done/20260915_1751_aiscc-p3-3-public-live-l1-migration-scope-expanded-postgresql-retry-1.md`
  - SHA-256 `99677363e5df58588114180fbb3ce85e7b78253a62c1873f3f2a2d40fe5b60ce`

Every path/hash MUST match.

Extra/missing/mismatch => STOP `L1_RETRY_BASELINE_MISMATCH`.

Do not clean/reset/delete provenance.

## Python bytecode prevention

Remain under:

```text
PYTHONDONTWRITEBYTECODE=1
```

All direct Python/Alembic/pytest invocations use existing `.venv` Python with `-B`.

Do not change `.gitignore`.

New Git-visible bytecode => STOP `L1_BYTECODE_RECURRENCE`.

## accepted discovery result

The previous tracked-repository discovery is admitted as the scope basis, but re-hash the six exact test files before modifying them.

Exactly these six existing tests are authorized:

- `tests/integration/next_action/test_genesis_bootstrap.py`
  - pre-edit SHA-256: `08143e72d9fa2c565fa40c91e7ec438bded9c240e5ee76faac6b7f7dd17ca229`
  - discovered line: `267`
  - current assertion fragment: `assert asyncio.run(snapshot())[:2] == ("20260914_0012", ())`
- `tests/integration/providers/test_external_ide_execution_ingress.py`
  - pre-edit SHA-256: `c63835776e95c6c182dff2aff1d52042667a9e6f3481276d47d43f3a310ad807`
  - discovered line: `435`
  - current assertion fragment: `assert asyncio.run(snapshot())[:3] == ("20260914_0012", (), ())`
- `tests/integration/providers/test_external_ide_execution_start.py`
  - pre-edit SHA-256: `637285027d028bf173f597712b84b8af853e788d0daeac4c9df2433f9652a5fa`
  - discovered line: `443`
  - current assertion fragment: `assert empty[0] == "20260914_0012" and empty[2] == ((), ())`
- `tests/integration/self_dogfood/test_task_ready_entry.py`
  - pre-edit SHA-256: `23dde6fa35d0301b2465073088adb63e33e52df18bed32557082088c108657e0`
  - discovered line: `89`
  - current assertion fragment: `"20260914_0012"`
- `tests/integration/task_authority/test_task_contract_durability.py`
  - pre-edit SHA-256: `a5fca4048d8429c727909ebeac558ab8f54382cf0adb87d1ea68a9b1a4c6d124`
  - discovered line: `792`
  - current assertion fragment: `assert asyncio.run(snapshot())[:2] == ("20260914_0012", 0)`
- `tests/integration/workflow/test_postgres_kernel.py`
  - pre-edit SHA-256: `66b67f7b2652c6170bd95ecf32831cd3c7e9a07f6230059516656ed725423b0c`
  - discovered line: `300`
  - current assertion fragment: `assert revision == "20260914_0012"`

For every file above require its pre-edit SHA-256 exact.

Hash mismatch => STOP `L1_STRICT_HEAD_TEST_BASE_CHANGED`.

## exact six-test modification authority

For the six files only:

- change the expected Alembic current/upgrade head identity from `20260914_0012` to `20260915_0013`;
- mechanically necessary nearby variable/test label/comment text may change only when needed for truthfulness;
- preserve all surrounding database snapshot, empty-state, upgrade, rollback and business assertions.

Forbidden:

- skipping/xfailing tests;
- loosening equality to partial/regex checks;
- deleting migration assertions;
- changing expected application data merely to pass;
- modifying any seventh existing test because of the migration head without a new STOP/Task.

After edits, prove each of the six still contains an exact assertion for `20260915_0013`.

## exact migration authority

Create exactly one additive Alembic revision:

```text
revision:
20260915_0013

down_revision:
20260914_0012
```

Preferred path:

`migrations/versions/20260915_0013_public_live_persistence_primitives.py`

No multiple heads.

After creation:

`alembic heads`

must produce exactly:

`20260915_0013 (head)`

## migration and L1 substantive contract

Read authority chain:

1. 1702 original L1;
2. 1718 PostgreSQL runtime expansion;
3. 1723 transport correction;
4. 1743 bytecode prevention;
5. 1751 migration scope;
6. this 1758 exact six-test authorization.

Implement the frozen L1 contract only:

- additive Public Live persistence schema;
- repository transaction primitives;
- integer micro-USD budget substrate;
- exact two-slot model;
- idempotency/dispatch/read-capability constraints;
- rollback and row-lock serialization;
- DB clock / last_clock fail-closed behavior;
- fail-closed initialization;
- focused tests/helpers.

No L2 admission service.

No public HTTP route, provider call/profile, frontend, Railway/Cloudflare/Wanted or Live enablement.

## PostgreSQL 17.6 runtime

Recreate/reverify isolated Task-owned runtime:

```text
image:
postgres:17.6

container:
aiscc-p3-3-l1-postgres-17-6

bind:
127.0.0.1 only

preferred port:
55432
```

Image must already be cached. If absent, STOP `L1_LOCAL_POSTGRES_IMAGE_UNAVAILABLE`.

Create target-only `LOCAL_POSTGRES_RUNTIME.json` PASS before product source mutation.

## migration evidence

Must execute and PASS:

1. source baseline head `20260914_0012`;
2. source new single head `20260915_0013`;
3. fresh empty PostgreSQL DB -> `20260915_0013`;
4. PostgreSQL DB at `20260914_0012` -> `20260915_0013`;
5. all six exact strict-head integration tests;
6. no unexpected owner/private historical data rewrite;
7. fail-closed Public Live defaults on both fresh and upgrade paths.

## mandatory L1 PostgreSQL evidence

Execute the complete 1702 L1 test requirements, including:

- required schema objects;
- default admission disabled;
- exactly slots 1/2 FREE;
- no enabled campaign;
- idempotency uniqueness;
- one-run/one-slot invariants;
- no third slot;
- dispatch ordinal 1/2 only;
- integer money nonnegative/bounded invariants;
- reserve/settle idempotence/uniqueness;
- read-capability hash uniqueness;
- observation identity uniqueness;
- UTC timestamps;
- rollback;
- conflicting row-lock serialization;
- DB clock/last_clock regression fail-closed.

Run relevant persistence/security regressions and broader local suite when no additional environment/network is required.

## changed-path plan

Before source mutation create target-only draft:

`L1_CHANGED_PATH_PLAN.json`

It must include from the start:

- new migration path;
- exact six existing strict-head test paths;
- current governance lineage.

Add L1 persistence/domain/repository/test-helper paths only when grounded by implementation necessity.

Before staging freeze the exact plan.

Stage set must exact-equal frozen plan.

No target/export/bytecode paths staged.

## successful commit lineage

A successful commit must preserve:

- all 20 predecessor governance/provenance paths unchanged;
- current 1758 Task/Cycle/Judgment/Handoff;
- authorized L1 source/migration/test changes.

Commit message exactly:

`feat(aiscc): add public live persistence primitives`

No push/tag/release.

## success invariants

```text
Public Live = NOT_RELEASED
Public admission = DISABLED
Public HTTP routes = NOT_IMPLEMENTED_BY_L1
Provider paid calls = IMPOSSIBLE_FROM_L1
L2 = NOT_IMPLEMENTED
```

Terminal repository:

```text
index = empty
tracked worktree = clean
Git-visible untracked = 0
Git-visible Python bytecode = 0
```

## allowed results

Success:

`PERSISTENCE_CANDIDATE / L1_IMPLEMENTED`

Blockers:

- `L1_RETRY_BASELINE_MISMATCH`
- `TRANSPORT_CANONICAL_COLLISION`
- `L1_BYTECODE_RECURRENCE`
- `L1_STRICT_HEAD_TEST_BASE_CHANGED`
- `L1_MIGRATION_BASELINE_CHANGED`
- `L1_LOCAL_POSTGRES_IMAGE_UNAVAILABLE`
- `L1_POSTGRES_CONTAINER_NAME_CONFLICT`
- `L1_REPOSITORY_ARCHITECTURE_CONFLICT`
- `L1_MIGRATION_POLICY_BLOCK`
- `L1_TEST_BLOCKED`
- `L1_IMPLEMENTATION_REWORK_REQUIRED`
- `EVIDENCE_SCOPE_EXPANSION_REQUIRED`

## target export

Target:

`.aiassistant/reports/target/20260915_1758_aiscc-p3-3-public-live-l1-six-strict-head-tests-authorized-postgresql-retry-1/`

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `TRANSPORT_VERIFICATION.json`
- `BASELINE_VERIFICATION.json`
- `STRICT_HEAD_TEST_AUTHORIZATION_VERIFICATION.json`
- `LOCAL_POSTGRES_RUNTIME.json`
- `SOURCE_INVENTORY.json`
- `MIGRATION_BASELINE.json`
- `MIGRATION_RESULT.json`
- `SCHEMA_INVENTORY.json`
- `CONSTRAINT_INDEX_INVENTORY.json`
- `REPOSITORY_PRIMITIVE_INVENTORY.json`
- `L1_SECURITY_TEST_MATRIX.json`
- `TEST_RESULTS.json`
- `FAIL_CLOSED_INITIALIZATION.json`
- `L1_CHANGED_PATH_PLAN.json`
- `STAGED_COMMIT_MANIFEST.json` when applicable
- `POSTCOMMIT_VERIFICATION.json` when applicable
- `DOCKER_CLEANUP.json`
- `TERMINAL_WORKSPACE.json`
- committed changed files preserving relative paths on success.

Terminal ZIP:

`.aiassistant/reports/target/20260915_1758_aiscc-p3-3-public-live-l1-six-strict-head-tests-authorized-postgresql-retry-1.zip`

## final response

1. result classification
2. 20-path baseline verification
3. exact six strict-head test pre/post verification
4. migration result
5. PostgreSQL runtime
6. schema/repository primitives
7. test results
8. exact changed-path plan
9. commit hash/parent if success
10. Docker cleanup
11. terminal workspace
12. target ZIP
13. L2 eligibility
