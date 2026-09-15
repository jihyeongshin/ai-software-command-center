# 작업지시서: P3-3 Public Live L1 baseline-regression disposition and commit persistence

## meta

- task_id: `20260915_1834_aiscc-p3-3-public-live-l1-baseline-regression-disposition-and-commit-persistence-1`
- created_at: `2026-09-15T18:34:20+09:00`
- work_type: `PERSISTENCE_REVALIDATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- fresh_ide_chat_required: `No`

## objective

Persist the exact Browser-accepted 1758 L1 implementation candidate.

No new product implementation is authorized.

The three known broader-suite failures are explicitly dispositioned as pre-existing baseline regression debt for this L1 persistence decision.

## transport ordering

1. verify outer ZIP SHA-256 / exact 4 members / CRC;
2. read this Task from the authenticated ZIP;
3. verify the exact 33-path candidate baseline below;
4. place this Task FIRST at:
   `.aiassistant/tasks/active/20260915_1834_aiscc-p3-3-public-live-l1-baseline-regression-disposition-and-commit-persistence-1.md`;
5. re-read/re-hash canonical Task;
6. place Cycle/Judgment/Handoff from the exact manifest below.

Before staging move this Task byte-for-byte to:

`.aiassistant/tasks/done/20260915_1834_aiscc-p3-3-public-live-l1-baseline-regression-disposition-and-commit-persistence-1.md`

## companion transport manifest

- member: `20260915_1834_aiscc-p3-3-public-live-l1-candidate-accepted-baseline-debt-disposition-entry-1.cycle.md`
  - destination: `.aiassistant/records/aiscc/cycles/20260915_1834_aiscc-p3-3-public-live-l1-candidate-accepted-baseline-debt-disposition-entry-1.cycle.md`
  - SHA-256: `805101f0e0f75ebb56bc75fa1898b0c5cbcc83278b327686fb63694816f74514`
- member: `20260915_1834_aiscc-p3-3-public-live-l1-implementation-browser-acceptance-1.md`
  - destination: `.aiassistant/reports/aiscc/20260915_1834_aiscc-p3-3-public-live-l1-implementation-browser-acceptance-1.md`
  - SHA-256: `62d6325217036e2a1fb3a50afde625b16a6ffc1117bce71f3e92c8d899488070`
- member: `20260915_1834_aiscc-browser-command-center-p3-3-public-live-l1-commit-persistence-entry-handoff-1.md`
  - destination: `.aiassistant/reports/aiscc/20260915_1834_aiscc-browser-command-center-p3-3-public-live-l1-commit-persistence-entry-handoff-1.md`
  - SHA-256: `f11b6ee20fae19363bfc02fa9d91771cc7bec0e7353eaa232a20fb489a999e6f`

Differing canonical collision => STOP `TRANSPORT_CANONICAL_COLLISION`.

## exact pre-delivery candidate baseline

Require:

```text
branch = main
HEAD = 209e7534f66e9b07ce9d33742e6993370a70f4fb
index = empty
tracked modified = 6 exact
Git-visible untracked = 27 exact
Git-visible Python bytecode = 0
```

Exact 33 candidate paths/hashes:

- `tests/integration/next_action/test_genesis_bootstrap.py`
  - SHA-256 `0c7d9400cfc1ebc629154ab3f134c995fee83507bfb41b5a01d618ef1c522c5e`
- `tests/integration/providers/test_external_ide_execution_ingress.py`
  - SHA-256 `0d40566d93d201448c0ea59fa1572f6b1031e4c38f41c6ad70a12e75e84901c0`
- `tests/integration/providers/test_external_ide_execution_start.py`
  - SHA-256 `91972844ddaaedaac1e41a4b30cb36a2637cf586c2f06b43633db26b4c801b96`
- `tests/integration/self_dogfood/test_task_ready_entry.py`
  - SHA-256 `a4d77da6ebc2218501d4249b6d5d02f00fa23945cdce100654ee6bbbc3e7d47d`
- `tests/integration/task_authority/test_task_contract_durability.py`
  - SHA-256 `8ff9defd6be9a925df8646d378fb0c08f6eb0fcda0b7f88b3eed201f6d8db006`
- `tests/integration/workflow/test_postgres_kernel.py`
  - SHA-256 `1b642ab9a75cd158d56afe7fc08cc70276c8064f2600f46a493bf7315629ba5d`
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
- `migrations/versions/20260915_0013_public_live_persistence_primitives.py`
  - SHA-256 `cdd62521702183d5a53ad6879a5808138f263da2ca40b30e3a8e3ac9eabc5a62`
- `src/aiscc/persistence/public_live.py`
  - SHA-256 `ee76aca9ff1e8de61653a5614e8165177cb4c372d84ebd2a73c2629c5c4e987a`
- `tests/integration/public_live/test_persistence.py`
  - SHA-256 `f195292ba2a6dffb67a05ba57d604b56ed24d9b3bd8a95717d36fb80a70ac599`

No additional path is allowed.

Any hash/membership mismatch => STOP `L1_ACCEPTED_CANDIDATE_MISMATCH`.

Do not clean/reset/reconstruct the candidate.

## immutable accepted L1 source

During this persistence Task, the following 9 L1 source/test paths are immutable and MUST retain the exact hashes above:

```text
6 strict-head integration tests
migrations/versions/20260915_0013_public_live_persistence_primitives.py
src/aiscc/persistence/public_live.py
tests/integration/public_live/test_persistence.py
```

No code/test edit is authorized.

If revalidation finds an actual L1 defect, STOP `L1_ACCEPTED_CANDIDATE_REWORK_REQUIRED`; do not patch it here.

## known baseline regression debt — exact disposition

The following three failures are accepted as pre-existing baseline debt for this L1 persistence decision:

1. `tests/integration/command_center/test_postgres_read_api.py::test_postgres_read_models_http_runtime_and_no_mutation`
2. `tests/integration/command_center/test_postgres_read_api.py::test_postgres_conflict_and_http_503_fail_closed`
3. `tests/integration/command_center/test_web_ui.py::test_default_entrypoint_ui_queue_etag_and_event_no_mutation`

Expected failure semantic:

`ValueError: G_EXECUTOR_SUBMISSION requires an issuer-verified execution ref`

This Task explicitly FORBIDS modifying:

- `src/aiscc/workflow/guards.py`;
- `tests/integration/command_center/test_postgres_read_api.py`;
- `tests/integration/command_center/test_web_ui.py`;

and forbids weakening/skipping/xfailing the guard or these tests.

Record target-only:

`KNOWN_BASELINE_REGRESSION_DISPOSITION.json`

with:

- three exact node IDs;
- expected exception semantic;
- baseline reproduction evidence identity from 1758;
- unchanged baseline SHA-256 of guard/fixture files;
- classification `PREEXISTING_NOT_L1_CAUSED`;
- follow-up status `DEFERRED_SEPARATE_TASK`.

Do not call the broader suite PASS.

## Python and PostgreSQL environment

Maintain:

```text
PYTHONDONTWRITEBYTECODE=1
```

Use existing `.venv` Python with `-B`.

No bare Python/Alembic/pytest.

Recreate a Task-owned isolated cached PostgreSQL 17.6 container on loopback only.

No image pull/network expansion.

If cached image is absent, STOP `L1_LOCAL_POSTGRES_IMAGE_UNAVAILABLE`.

Use disposable process-only credentials.

Cleanup Task-owned container/volume best-effort after evidence.

## required revalidation

Without modifying accepted source:

### 1. exact migration identity

Require:

```text
alembic heads:
20260915_0013 (head)

down_revision:
20260914_0012
```

### 2. exact strict-head + L1 focused suite

Re-run the accepted focused suite covering:

- all six strict-head integration tests;
- complete `tests/integration/public_live/test_persistence.py`.

Expected:

```text
127 PASS
```

If count changes only because parametrization/tool output representation changes, prove exact node-set equivalence. Otherwise STOP.

### 3. L1 persistence suite

Require:

```text
23 PASS
```

and preserve evidence for migration fresh/upgrade, fail-closed defaults, constraints, rollback, lock wait, clock regression and role separation.

### 4. broader regression

Run the same broader local non-runtime suite used in 1758.

Allowed result is only:

```text
exact same 3 known failures
no additional failures/errors
same environment-limited skips are acceptable
```

Any fourth failure, changed failure node, changed exception semantic, or error => STOP `L1_REGRESSION_SET_CHANGED`.

The report must say:

`BROADER_SUITE_NON_GREEN / EXACT_PREEXISTING_3_FAILURES`

not PASS.

### 5. static/invariant checks

Require:

- Ruff PASS for the three new L1 paths;
- mypy PASS for `public_live.py` or the same accepted repository-level check;
- `git diff --check` PASS;
- Replay builder PASS;
- `public/replay/**` unchanged;
- no public HTTP route;
- no provider calls;
- no bytecode residue.

## staging plan

Create target-only:

`L1_PERSISTENCE_CHANGED_PATH_PLAN.json`

Final staged set MUST be exactly:

```text
33 accepted candidate paths
+ current 20260915_1834 Task/Cycle/Judgment/Handoff
= 37 paths
```

No canonical state-summary update in this Task.

No target/export file staged.

No known failing Command Center fixture/guard file staged.

Prove exact set equality before commit.

## commit

On complete revalidation only:

```text
feat(aiscc): add public live persistence primitives
```

No amend of unrelated history.

No push/tag/release.

## postcommit proof

Require:

```text
parent = 209e7534f66e9b07ce9d33742e6993370a70f4fb
changed path count = 37
index = empty
tracked worktree = clean
Git-visible untracked = 0
Git-visible Python bytecode = 0
```

Reopen committed L1 files and verify their hashes equal the accepted precommit candidate hashes.

Verify:

```text
alembic head source = 20260915_0013
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

Do NOT claim full-suite green.

Allowed blockers:

- `L1_ACCEPTED_CANDIDATE_MISMATCH`
- `TRANSPORT_CANONICAL_COLLISION`
- `L1_LOCAL_POSTGRES_IMAGE_UNAVAILABLE`
- `L1_ACCEPTED_CANDIDATE_REWORK_REQUIRED`
- `L1_REGRESSION_SET_CHANGED`
- `L1_TEST_BLOCKED`
- `EVIDENCE_SCOPE_EXPANSION_REQUIRED`

## target export

Target:

`.aiassistant/reports/target/20260915_1834_aiscc-p3-3-public-live-l1-baseline-regression-disposition-and-commit-persistence-1/`

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `TRANSPORT_VERIFICATION.json`
- `ACCEPTED_CANDIDATE_VERIFICATION.json`
- `KNOWN_BASELINE_REGRESSION_DISPOSITION.json`
- `LOCAL_POSTGRES_RUNTIME.json`
- `REVALIDATION_RESULTS.json`
- `L1_PERSISTENCE_CHANGED_PATH_PLAN.json`
- `STAGED_COMMIT_MANIFEST.json`
- `POSTCOMMIT_VERIFICATION.json`
- `DOCKER_CLEANUP.json`
- `TERMINAL_WORKSPACE.json`
- committed L1 source/test files preserving relative paths;
- current acceptance provenance.

Terminal ZIP:

`.aiassistant/reports/target/20260915_1834_aiscc-p3-3-public-live-l1-baseline-regression-disposition-and-commit-persistence-1.zip`

## final response

1. result classification
2. exact accepted-candidate verification
3. known baseline regression disposition
4. focused/L1 revalidation
5. broader suite exact failure set
6. staged path count
7. commit hash/parent
8. Replay/Live invariants
9. Docker cleanup
10. terminal workspace
11. target ZIP
12. L2 eligibility remains Browser-pending until this commit is judged
