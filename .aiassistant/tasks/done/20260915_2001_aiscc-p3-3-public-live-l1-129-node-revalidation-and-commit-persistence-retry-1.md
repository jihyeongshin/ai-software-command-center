# 작업지시서: P3-3 Public Live L1 129-node revalidation and commit persistence retry

## meta

- task_id: `20260915_2001_aiscc-p3-3-public-live-l1-129-node-revalidation-and-commit-persistence-retry-1`
- created_at: `2026-09-15T20:01:40+09:00`
- work_type: `PERSISTENCE_REVALIDATION_RETRY`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- fresh_ide_chat_required: `No`

## objective

Correct the stale 1834 focused-node count contract, perform fresh complete L1 revalidation against the immutable accepted candidate, and commit only if every corrected gate passes.

No product code/test modification is authorized.

## transport ordering

1. verify outer ZIP SHA-256 / exact 4 members / CRC;
2. read this Task from authenticated ZIP;
3. verify exact pre-delivery 37-path candidate baseline;
4. place this Task FIRST at:
   `.aiassistant/tasks/active/20260915_2001_aiscc-p3-3-public-live-l1-129-node-revalidation-and-commit-persistence-retry-1.md`;
5. re-read/re-hash canonical Task;
6. place Cycle/Judgment/Handoff using the exact manifest below.

Before staging, move this Task byte-for-byte to:

`.aiassistant/tasks/done/20260915_2001_aiscc-p3-3-public-live-l1-129-node-revalidation-and-commit-persistence-retry-1.md`

## companion transport manifest

- member: `20260915_2001_aiscc-p3-3-public-live-l1-stale-focused-count-blocker-accepted-retry-entry-1.cycle.md`
  - destination: `.aiassistant/records/aiscc/cycles/20260915_2001_aiscc-p3-3-public-live-l1-stale-focused-count-blocker-accepted-retry-entry-1.cycle.md`
  - SHA-256: `1913ee58d0986940d531d52fa2888ecd91e48fdfe51454958c9b9d6eaaae2a01`
- member: `20260915_2001_aiscc-p3-3-public-live-l1-stale-focused-count-browser-judgment-1.md`
  - destination: `.aiassistant/reports/aiscc/20260915_2001_aiscc-p3-3-public-live-l1-stale-focused-count-browser-judgment-1.md`
  - SHA-256: `2797ac0c8bcb0b990f50991331d65fbc6d6c3e3e3d62a6e12fdda7b44d636187`
- member: `20260915_2001_aiscc-browser-command-center-p3-3-public-live-l1-129-node-commit-retry-entry-handoff-1.md`
  - destination: `.aiassistant/reports/aiscc/20260915_2001_aiscc-browser-command-center-p3-3-public-live-l1-129-node-commit-retry-entry-handoff-1.md`
  - SHA-256: `eaad03573fd26d772fc1cea7faf6bb405cb63376a3e2df81b7b5a507b689bd71`

Differing canonical collision => STOP `TRANSPORT_CANONICAL_COLLISION`.

## exact pre-delivery candidate baseline

Require:

```text
branch = main
HEAD = 209e7534f66e9b07ce9d33742e6993370a70f4fb
index = empty
tracked modified = 6 exact
Git-visible untracked = 31 exact
Git-visible Python bytecode = 0
```

Exact 37 paths/hashes:

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
- `.aiassistant/records/aiscc/cycles/20260915_1758_aiscc-p3-3-public-live-l1-six-head-assertions-discovered-accepted-retry-entry-1.cycle.md`
  - SHA-256 `35974a318a79f77e6ab54527bcb507ef93cba6fc5d01de9dddc6a53486daadb2`
- `.aiassistant/records/aiscc/cycles/20260915_1834_aiscc-p3-3-public-live-l1-candidate-accepted-baseline-debt-disposition-entry-1.cycle.md`
  - SHA-256 `805101f0e0f75ebb56bc75fa1898b0c5cbcc83278b327686fb63694816f74514`
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
- `.aiassistant/reports/aiscc/20260915_1758_aiscc-browser-command-center-p3-3-public-live-l1-six-head-tests-authorized-retry-entry-handoff-1.md`
  - SHA-256 `98cc974b4191537e5e0a026eebdd6bc3520af37703de6516f8fc267c3ad19afb`
- `.aiassistant/reports/aiscc/20260915_1758_aiscc-p3-3-public-live-l1-head-assertion-scope-browser-judgment-1.md`
  - SHA-256 `0d043548664f365a6820beeebc404c53991ff532ce8082d192109941aed1e2db`
- `.aiassistant/reports/aiscc/20260915_1834_aiscc-browser-command-center-p3-3-public-live-l1-commit-persistence-entry-handoff-1.md`
  - SHA-256 `f11b6ee20fae19363bfc02fa9d91771cc7bec0e7353eaa232a20fb489a999e6f`
- `.aiassistant/reports/aiscc/20260915_1834_aiscc-p3-3-public-live-l1-implementation-browser-acceptance-1.md`
  - SHA-256 `62d6325217036e2a1fb3a50afde625b16a6ffc1117bce71f3e92c8d899488070`
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
- `.aiassistant/tasks/done/20260915_1758_aiscc-p3-3-public-live-l1-six-strict-head-tests-authorized-postgresql-retry-1.md`
  - SHA-256 `d7113e2bed0335a5c41d3c2e5c4d76f16434b7af4aeb604ead554e6298bed278`
- `.aiassistant/tasks/done/20260915_1834_aiscc-p3-3-public-live-l1-baseline-regression-disposition-and-commit-persistence-1.md`
  - SHA-256 `7082960d03f18775c34a3a63f8ae855cb7b68e3e69d69a71467ffc4f494bd02e`
- `migrations/versions/20260915_0013_public_live_persistence_primitives.py`
  - SHA-256 `cdd62521702183d5a53ad6879a5808138f263da2ca40b30e3a8e3ac9eabc5a62`
- `src/aiscc/persistence/public_live.py`
  - SHA-256 `ee76aca9ff1e8de61653a5614e8165177cb4c372d84ebd2a73c2629c5c4e987a`
- `tests/integration/next_action/test_genesis_bootstrap.py`
  - SHA-256 `0c7d9400cfc1ebc629154ab3f134c995fee83507bfb41b5a01d618ef1c522c5e`
- `tests/integration/providers/test_external_ide_execution_ingress.py`
  - SHA-256 `0d40566d93d201448c0ea59fa1572f6b1031e4c38f41c6ad70a12e75e84901c0`
- `tests/integration/providers/test_external_ide_execution_start.py`
  - SHA-256 `91972844ddaaedaac1e41a4b30cb36a2637cf586c2f06b43633db26b4c801b96`
- `tests/integration/public_live/test_persistence.py`
  - SHA-256 `f195292ba2a6dffb67a05ba57d604b56ed24d9b3bd8a95717d36fb80a70ac599`
- `tests/integration/self_dogfood/test_task_ready_entry.py`
  - SHA-256 `a4d77da6ebc2218501d4249b6d5d02f00fa23945cdce100654ee6bbbc3e7d47d`
- `tests/integration/task_authority/test_task_contract_durability.py`
  - SHA-256 `8ff9defd6be9a925df8646d378fb0c08f6eb0fcda0b7f88b3eed201f6d8db006`
- `tests/integration/workflow/test_postgres_kernel.py`
  - SHA-256 `1b642ab9a75cd158d56afe7fc08cc70276c8064f2600f46a493bf7315629ba5d`

Any extra/missing/hash mismatch => STOP `L1_ACCEPTED_CANDIDATE_MISMATCH`.

Do not clean/reset/reconstruct the candidate.

## immutable accepted L1 source/test candidate

The 9 L1 source/test paths in the exact baseline are immutable.

No source/test/migration edit is authorized.

If a genuine L1 defect is found:

`L1_ACCEPTED_CANDIDATE_REWORK_REQUIRED`

Do not patch it in this Task.

## corrected focused-node authority

Historical accepted evidence:

```text
1758 STRICT_AND_L1_RESULTS.xml
SHA-256:
1af7e977f5f376010f0492d04887947ce998a08dfe323ce9f65a46ed5f85d560

historical focused nodes:
127
```

The immutable accepted candidate's complete L1 file has 23 nodes.

1834 fresh collection proved the complete current combined collection is 129 nodes.

The corrected expected focused set is:

```text
all 127 node IDs from the 1758 accepted STRICT_AND_L1_RESULTS.xml

PLUS exactly:

tests/integration/public_live/test_persistence.py::test_migration_paths_and_owner_preservation

tests/integration/public_live/test_persistence.py::test_trusted_reconciliation_known_cost_and_denials
```

No other added node.

No missing historical node.

### mandatory collection proof

Before executing the focused suite:

1. parse the 1758 accepted XML;
2. verify its SHA-256 exactly;
3. derive its exact 127 node IDs;
4. collect the current six strict-head files + complete L1 file;
5. require exactly 129 current node IDs;
6. require set equality to historical 127 + the exact two additions above.

Write target-only:

`FOCUSED_129_NODE_SET_VERIFICATION.json`

If mismatch:

`L1_FOCUSED_NODE_SET_CHANGED`

and STOP.

## Python / bytecode

Maintain:

```text
PYTHONDONTWRITEBYTECODE=1
```

All direct Python/Alembic/pytest commands use existing `.venv` interpreter with `-B`.

No bare Python/Alembic/pytest.

New Git-visible bytecode => STOP `L1_BYTECODE_RECURRENCE`.

## PostgreSQL runtime

Recreate Task-owned isolated cached PostgreSQL 17.6:

```text
container:
aiscc-p3-3-l1-postgres-17-6

image:
postgres:17.6

bind:
127.0.0.1 only

preferred port:
55432
```

No image pull/network expansion.

If cached image absent => STOP `L1_LOCAL_POSTGRES_IMAGE_UNAVAILABLE`.

Create target-only `LOCAL_POSTGRES_RUNTIME.json` PASS.

## mandatory fresh revalidation

### A. migration identity

Require:

```text
single Alembic head:
20260915_0013

down_revision:
20260914_0012
```

### B. complete corrected focused suite

Execute exact verified 129-node set.

Expected:

```text
129 PASS
0 FAIL
0 ERROR
```

This supersedes the stale 127-count requirement.

### C. complete L1 persistence suite

Execute complete:

`tests/integration/public_live/test_persistence.py`

Expected:

```text
23 PASS
0 FAIL
0 ERROR
```

Do not infer 23 from the combined run; preserve standalone evidence too.

### D. mandatory L1 properties

Reconfirm evidence for:

- empty DB -> head;
- 0012 -> 0013 upgrade;
- fail-closed initialization;
- exactly two FREE slots;
- no enabled campaign;
- money constraints;
- idempotency/read/dispatch/observation constraints;
- rollback;
- row-lock serialization;
- DB clock regression;
- runtime/reconciler permission separation.

### E. broader local suite

Run the same broader non-runtime suite used in 1758.

Allowed non-green outcome is exactly the known three node IDs:

1. `tests/integration/command_center/test_postgres_read_api.py::test_postgres_read_models_http_runtime_and_no_mutation`
2. `tests/integration/command_center/test_postgres_read_api.py::test_postgres_conflict_and_http_503_fail_closed`
3. `tests/integration/command_center/test_web_ui.py::test_default_entrypoint_ui_queue_etag_and_event_no_mutation`

Expected semantic:

`ValueError: G_EXECUTOR_SUBMISSION requires an issuer-verified execution ref`

Require:

```text
no fourth failure
no error
no changed failure node
no changed exception semantic
```

Environment-limited skips equivalent to the accepted 1758 run are allowed.

Classify:

`BROADER_SUITE_NON_GREEN / EXACT_PREEXISTING_3_FAILURES`

Do NOT call broader suite PASS.

If failure set changes => STOP `L1_REGRESSION_SET_CHANGED`.

## known debt mutation prohibition

Do not modify:

- `src/aiscc/workflow/guards.py`;
- `tests/integration/command_center/test_postgres_read_api.py`;
- `tests/integration/command_center/test_web_ui.py`.

No skip/xfail/guard weakening.

## static checks

Require fresh:

- Ruff PASS on L1 new source/test/migration surface;
- mypy PASS at the accepted L1 scope;
- `git diff --check` PASS;
- Replay builder PASS;
- `public/replay/**` unchanged;
- no public API route;
- no provider action;
- no bytecode residue.

## staging

Create target-only:

`L1_129_NODE_PERSISTENCE_CHANGED_PATH_PLAN.json`

Final stage set exactly:

```text
37 exact pre-delivery candidate paths
+ current 2001 Task/Cycle/Judgment/Handoff
= 41 paths
```

No target/export path staged.

No guard/known-failing fixture file staged.

No product path other than the already accepted nine L1 source/test paths.

Prove exact staged-set equality.

## commit

On complete fresh revalidation only:

```text
feat(aiscc): add public live persistence primitives
```

No push/tag/release.

## postcommit proof

Require:

```text
parent = 209e7534f66e9b07ce9d33742e6993370a70f4fb
changed path count = 41
index = empty
tracked worktree = clean
Git-visible untracked = 0
Git-visible Python bytecode = 0
```

Reopen committed accepted L1 source/test paths and require their SHA-256 remains exactly equal to the pre-delivery candidate hashes.

Require source migration head still `20260915_0013`.

## terminal product truth

Must remain:

```text
Public Live = NOT_RELEASED
Public admission = DISABLED
Public HTTP routes = NOT_IMPLEMENTED_BY_L1
Provider paid calls = IMPOSSIBLE_FROM_L1
L2 = NOT_IMPLEMENTED
```

## result classification

Success:

```text
PERSISTENCE_CANDIDATE / L1_IMPLEMENTED_AND_COMMITTED / PREEXISTING_BASELINE_REGRESSION_DEBT
```

Allowed blockers:

- `L1_ACCEPTED_CANDIDATE_MISMATCH`
- `TRANSPORT_CANONICAL_COLLISION`
- `L1_FOCUSED_NODE_SET_CHANGED`
- `L1_BYTECODE_RECURRENCE`
- `L1_LOCAL_POSTGRES_IMAGE_UNAVAILABLE`
- `L1_ACCEPTED_CANDIDATE_REWORK_REQUIRED`
- `L1_REGRESSION_SET_CHANGED`
- `L1_TEST_BLOCKED`
- `EVIDENCE_SCOPE_EXPANSION_REQUIRED`

## Docker cleanup

Stop/remove only Task-owned PostgreSQL container and safely identified Task-owned ephemeral volume.

Cleanup residue alone after successful evidence/commit is non-blocking; report exact residue.

## target export

Target:

`.aiassistant/reports/target/20260915_2001_aiscc-p3-3-public-live-l1-129-node-revalidation-and-commit-persistence-retry-1/`

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `TRANSPORT_VERIFICATION.json`
- `ACCEPTED_CANDIDATE_VERIFICATION.json`
- `FOCUSED_129_NODE_SET_VERIFICATION.json`
- `KNOWN_BASELINE_REGRESSION_DISPOSITION.json`
- `LOCAL_POSTGRES_RUNTIME.json`
- `REVALIDATION_RESULTS.json`
- `L1_129_NODE_PERSISTENCE_CHANGED_PATH_PLAN.json`
- `STAGED_COMMIT_MANIFEST.json`
- `POSTCOMMIT_VERIFICATION.json`
- `DOCKER_CLEANUP.json`
- `TERMINAL_WORKSPACE.json`
- committed L1 source/test files preserving repository-relative paths;
- current acceptance lineage.

Terminal ZIP:

`.aiassistant/reports/target/20260915_2001_aiscc-p3-3-public-live-l1-129-node-revalidation-and-commit-persistence-retry-1.zip`

## final response

1. result classification
2. exact 37-path candidate verification
3. exact 129-node set proof
4. 129 focused result
5. 23 standalone L1 result
6. broader exact-3-failure disposition
7. static checks
8. staged 41-path equality
9. commit hash/parent
10. Docker cleanup
11. terminal workspace
12. target ZIP
13. L2 eligibility remains Browser-pending until commit judgment
