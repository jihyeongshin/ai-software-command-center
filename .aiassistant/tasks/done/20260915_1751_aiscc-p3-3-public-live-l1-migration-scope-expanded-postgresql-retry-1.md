# 작업지시서: P3-3 Public Live L1 migration-scope-expanded PostgreSQL retry

## meta

- task_id: `20260915_1751_aiscc-p3-3-public-live-l1-migration-scope-expanded-postgresql-retry-1`
- created_at: `2026-09-15T17:51:19+09:00`
- work_type: `IMPLEMENTATION_RETRY`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- fresh_ide_chat_required: `No`
- primary_semantic_owner: `P3-3 Public Live L1 persistence primitives`

## objective

Resolve the 1743 migration-policy blocker by explicitly authorizing the exact migration-head transition required by the frozen L1 design, then resume the original L1 implementation.

This Task does not broaden L1 beyond persistence primitives.

## transport ordering

1. verify outer ZIP SHA-256 / exact 4 members / CRC;
2. read this Task from the authenticated ZIP;
3. verify the pre-delivery repository baseline below;
4. place this Task first at:
   `.aiassistant/tasks/active/20260915_1751_aiscc-p3-3-public-live-l1-migration-scope-expanded-postgresql-retry-1.md`;
5. re-read/re-hash canonical active Task;
6. place the companions below.

Before terminal export move current Task to:

`.aiassistant/tasks/done/20260915_1751_aiscc-p3-3-public-live-l1-migration-scope-expanded-postgresql-retry-1.md`

## exact companion transport manifest

- member: `20260915_1751_aiscc-p3-3-public-live-l1-migration-policy-block-accepted-retry-entry-1.cycle.md`
  - destination: `.aiassistant/records/aiscc/cycles/20260915_1751_aiscc-p3-3-public-live-l1-migration-policy-block-accepted-retry-entry-1.cycle.md`
  - SHA-256: `fd182f220455531e6483a96c755f68bdc9cb3fce35dc99d3d5b1ff321f76b60b`
- member: `20260915_1751_aiscc-p3-3-public-live-l1-migration-policy-block-browser-judgment-1.md`
  - destination: `.aiassistant/reports/aiscc/20260915_1751_aiscc-p3-3-public-live-l1-migration-policy-block-browser-judgment-1.md`
  - SHA-256: `69afedc579ce90bf2d5488cbb020862847490b0b0c722ecc49839611177f3c1b`
- member: `20260915_1751_aiscc-browser-command-center-p3-3-public-live-l1-migration-scope-expanded-retry-entry-handoff-1.md`
  - destination: `.aiassistant/reports/aiscc/20260915_1751_aiscc-browser-command-center-p3-3-public-live-l1-migration-scope-expanded-retry-entry-handoff-1.md`
  - SHA-256: `6103eb7a64a1c15800512e35172847bacbd85a4e340d394d166e742b881c03bb`

Destination collision with different bytes => STOP `TRANSPORT_CANONICAL_COLLISION`.

## exact candidate baseline before this delivery

Require:

```text
branch = main
HEAD = 209e7534f66e9b07ce9d33742e6993370a70f4fb
index = empty
tracked worktree = clean
Git-visible untracked = 16 exact
Git-visible Python bytecode = 0
```

Expected 16 provenance paths:

- `.aiassistant/records/aiscc/cycles/20260915_1702_aiscc-p3-3-live-prerequisite-design-frozen-l1-entry-1.cycle.md`
  - SHA-256 `fcc34bc99f4e285c8dcdfe696d3b5db70fe12e076461361d70a9b293cbfaa758`
- `.aiassistant/records/aiscc/cycles/20260915_1718_aiscc-p3-3-public-live-l1-test-environment-blocker-accepted-retry-entry-1.cycle.md`
  - SHA-256 `6ed0ebb242df3cebc99d4d080d8844506199e6dca9869ceeffb3fed178570b2d`
- `.aiassistant/records/aiscc/cycles/20260915_1723_aiscc-p3-3-public-live-l1-transport-contract-blocker-accepted-retry-entry-1.cycle.md`
  - SHA-256 `20cbe1737132e2b06d31014f4db8f8d04be9d51a3103651c3b531b8beced9659`
- `.aiassistant/records/aiscc/cycles/20260915_1743_aiscc-p3-3-public-live-l1-bytecode-residue-blocker-accepted-retry-entry-1.cycle.md`
  - SHA-256 `d3df523580e2eb0f115e4e2a56e4f7c7101664cdf19d40c34da8b545b9237530`
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
- `.aiassistant/tasks/done/20260915_1702_aiscc-p3-3-public-live-l1-schema-repository-transaction-primitives-implementation-1.md`
  - SHA-256 `102f79a47601c00a8496e1a77a5ddb99d9a5af083d86b215a9c266f4de3df2af`
- `.aiassistant/tasks/done/20260915_1718_aiscc-p3-3-public-live-l1-postgresql-runtime-authorized-implementation-retry-1.md`
  - SHA-256 `32cd6d2e6dbf497c1f5c0382cecf1fef1ddbb46b043afe40ec9890504b46fad8`
- `.aiassistant/tasks/done/20260915_1723_aiscc-p3-3-public-live-l1-transport-manifest-corrected-postgresql-retry-1.md`
  - SHA-256 `4c3279e14c5ee9b866037ea61f347f7157abbb5abf23d1f1e7738198ce3c24a7`
- `.aiassistant/tasks/done/20260915_1743_aiscc-p3-3-public-live-l1-bytecode-residue-cleanup-authorized-postgresql-retry-1.md`
  - SHA-256 `f97f2aa72ca7cd5661455f6e6f3dd5e0acf1a1e63f69a68e4bc98d82a79d0cff`

Every path/hash MUST match.

Any extra/missing/hash mismatch => STOP `L1_RETRY_BASELINE_MISMATCH`.

Do not clean/reset/delete provenance.

## Python bytecode prevention remains mandatory

Before any Python/Alembic/pytest command:

```text
PYTHONDONTWRITEBYTECODE=1
```

Use only the existing `.venv` interpreter with `-B` for direct Python commands.

No bare `python`, `alembic`, or `pytest`.

New Git-visible bytecode => STOP `L1_BYTECODE_RECURRENCE`.

## pre-edit migration discovery gate

Before ANY source/test/migration edit:

1. verify current Alembic head is exactly `20260914_0012`;
2. search tracked repository text for exact literal `20260914_0012`;
3. classify every match by path and semantic role;
4. identify the strict regression assertion(s) that specifically verify Alembic `upgrade head` / current-head identity.

Write target-only:

`MIGRATION_HEAD_ASSERTION_DISCOVERY.json`

with:

- every tracked literal match path;
- file SHA-256;
- line/semantic role;
- whether modification is authorized;
- reason.

### exact authorization predicate for existing test modification

An existing test file may be modified under this Task IFF all are true:

```text
it is under tests/
it already contains the exact literal 20260914_0012
that literal participates in an assertion/expectation for Alembic current-head or upgrade-head result
change needed is only the expected head identity 20260914_0012 -> 20260915_0013 plus mechanically necessary nearby naming/comment updates
```

If zero qualifying test files exist => STOP `L1_STRICT_HEAD_TEST_NOT_FOUND`.

If more than two qualifying test files exist, or if any qualifying change requires semantic relaxation beyond advancing the exact head => STOP `L1_MIGRATION_HEAD_ASSERTION_SCOPE_AMBIGUOUS`.

Non-test occurrences of the old head are NOT automatically authorized for modification.

Do not change historical governance/provenance merely because it contains the old revision id.

## explicit new migration authority

This Task explicitly authorizes exactly one new Alembic revision:

```text
revision id:
20260915_0013

down_revision:
20260914_0012

semantic owner:
Public Live L1 additive persistence primitives
```

Preferred filename, following current convention:

`migrations/versions/20260915_0013_public_live_persistence_primitives.py`

If repository migration naming policy requires a different suffix but the same exact revision id, record the exact path before creation in `L1_CHANGED_PATH_PLAN.json`.

Multiple heads are forbidden.

After creation:

```text
alembic heads
```

must report exactly one head:

`20260915_0013`

## migration semantics

The new revision must be additive and implement only the frozen canonical Public Live L1 DB schema.

It MUST NOT:

- rewrite/drop owner historical tables;
- alter Replay artifacts;
- enable public admission;
- create an enabled campaign;
- embed provider credentials;
- grant implicit positive spend authority.

Fresh/upgrade behavior must be deterministic against isolated PostgreSQL 17.6.

## PostgreSQL runtime

Recreate/reverify the same isolated local runtime:

```text
image: postgres:17.6
container: aiscc-p3-3-l1-postgres-17-6
bind: 127.0.0.1 only
preferred port: 55432
```

Image must already be cached for this retry. If absent, STOP `L1_LOCAL_POSTGRES_IMAGE_UNAVAILABLE`.

Before source mutation require target-only `LOCAL_POSTGRES_RUNTIME.json` PASS.

## substantive L1 contract

Read the done authority chain in order:

1. 1702 original L1 Task;
2. 1718 PostgreSQL-runtime expansion;
3. 1723 transport correction;
4. 1743 bytecode cleanup/recurrence prevention;
5. this 1751 migration-scope correction.

Then implement the frozen L1 contract in full:

- additive Public Live schema;
- persistence/domain/repository transaction primitives;
- integer micro-USD substrate;
- exact two-slot model;
- idempotency/dispatch/read-capability constraints;
- rollback/row-lock serialization;
- DB clock / last_clock fail-closed behavior;
- fail-closed initialization;
- focused PostgreSQL 17.6 tests.

Do NOT implement L2 admission orchestration.

Do NOT implement public API routes, provider calls/profile, frontend, Railway/Cloudflare/Wanted, or Live enablement.

## strict-head regression update authority

The pre-edit discovery output determines the exact qualifying existing test path(s).

For each qualifying test path:

- record pre-edit SHA-256;
- update only the head expectation from `20260914_0012` to `20260915_0013` and directly necessary nearby test label/comment text;
- preserve all behavioral assertions;
- do not weaken `upgrade head` success, single-head, migration integrity, rollback, or database-state checks.

The updated strict-head test must execute against real PostgreSQL 17.6 and PASS.

## mandatory migration evidence

At minimum prove:

1. old repository head is exactly `20260914_0012` before change;
2. new repository head is exactly `20260915_0013` after change;
3. fresh empty DB -> head PASS;
4. DB at `20260914_0012` -> `20260915_0013` PASS;
5. strict-head regression PASS with the new exact head;
6. exactly one Alembic head;
7. no owner/private historical data rewrite;
8. fail-closed Public Live defaults after both fresh and upgrade paths.

## L1 PostgreSQL evidence

Execute the full mandatory L1 test contract from 1702, including constraints, uniqueness, rollback, locking, clock regression, fail-closed initialization and relevant regressions.

Broader local suite may run only if it needs no new environment/network.

## exact source-scope expansion

Compared with 1743, this Task newly authorizes only:

```text
one new migration revision 20260915_0013
qualifying existing strict-head migration regression test path(s) discovered by the predicate above
```

The rest of source scope remains the original narrow L1 allowlist:

- L1 persistence/domain/repository code;
- L1 focused tests/helpers;
- governance provenance.

No unrelated regression update is authorized.

## changed-path plan

Before the first source edit, create target-only draft:

`L1_CHANGED_PATH_PLAN.json`

It must already contain:

- the exact new migration path;
- every discovered qualifying strict-head test path;
- planned L1 persistence/domain/repository paths if known;
- category/reason/pre-existing status.

Update the plan as legitimate L1 paths become necessary, but never broaden outside this Task.

Before staging freeze the plan and prove staged-set exact equality.

## commit

On full success only:

```text
feat(aiscc): add public live persistence primitives
```

No partial-success commit, no push/tag/release.

## terminal success invariants

```text
Public Live = NOT_RELEASED
Public admission = DISABLED
Public HTTP routes = NOT_IMPLEMENTED_BY_L1
Provider paid calls = IMPOSSIBLE_FROM_L1
L2 = NOT_IMPLEMENTED
```

Repository terminal success:

```text
index = empty
tracked worktree = clean
Git-visible untracked = 0
Git-visible Python bytecode = 0
```

## result classifications

Success:

`PERSISTENCE_CANDIDATE / L1_IMPLEMENTED`

Allowed blockers:

- `L1_RETRY_BASELINE_MISMATCH`
- `TRANSPORT_CANONICAL_COLLISION`
- `L1_BYTECODE_RECURRENCE`
- `L1_MIGRATION_BASELINE_CHANGED`
- `L1_STRICT_HEAD_TEST_NOT_FOUND`
- `L1_MIGRATION_HEAD_ASSERTION_SCOPE_AMBIGUOUS`
- `L1_LOCAL_POSTGRES_IMAGE_UNAVAILABLE`
- `L1_POSTGRES_CONTAINER_NAME_CONFLICT`
- `L1_REPOSITORY_ARCHITECTURE_CONFLICT`
- `L1_MIGRATION_POLICY_BLOCK`
- `L1_TEST_BLOCKED`
- `L1_IMPLEMENTATION_REWORK_REQUIRED`
- `EVIDENCE_SCOPE_EXPANSION_REQUIRED`

## target export

Target:

`.aiassistant/reports/target/20260915_1751_aiscc-p3-3-public-live-l1-migration-scope-expanded-postgresql-retry-1/`

Required root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `TRANSPORT_VERIFICATION.json`
- `BASELINE_VERIFICATION.json`
- `MIGRATION_HEAD_ASSERTION_DISCOVERY.json`
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
- changed committed files preserving repository-relative paths on success.

Terminal ZIP:

`.aiassistant/reports/target/20260915_1751_aiscc-p3-3-public-live-l1-migration-scope-expanded-postgresql-retry-1.zip`

## final response

1. result classification
2. baseline/provenance verification
3. migration-head assertion discovery
4. exact new migration path/revision
5. PostgreSQL runtime result
6. schema/repository implementation
7. strict-head + L1 test results
8. exact changed-path plan
9. commit hash/parent if success
10. Docker cleanup
11. terminal workspace
12. target ZIP
13. L2 eligibility
