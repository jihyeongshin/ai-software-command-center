# 작업지시서: P3-3 Public Live L1 bytecode-residue-cleanup-authorized PostgreSQL retry

## meta

- task_id: `20260915_1743_aiscc-p3-3-public-live-l1-bytecode-residue-cleanup-authorized-postgresql-retry-1`
- created_at: `2026-09-15T17:43:06+09:00`
- work_type: `IMPLEMENTATION_RETRY`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- fresh_ide_chat_required: `Yes`
- primary_semantic_owner: `P3-3 Public Live L1 persistence primitives`

## objective

Remove only the exact Executor-generated Python bytecode residue from the 1723 blocked attempt, prevent recurrence, recreate the isolated PostgreSQL 17.6 runtime, and execute the unchanged L1 implementation contract.

## transport ordering — mandatory

This retry corrects the prior procedural ordering.

1. verify outer ZIP SHA-256/member set/CRC;
2. read this Task member from the authenticated ZIP;
3. verify repository baseline described below;
4. place THIS Task first at:
   `.aiassistant/tasks/active/20260915_1743_aiscc-p3-3-public-live-l1-bytecode-residue-cleanup-authorized-postgresql-retry-1.md`;
5. re-hash/read canonical active Task;
6. only then place Cycle/Judgment/Handoff using the exact manifest below.

Do not place companions before the primary Task.

Before terminal export move the current Task to:

`.aiassistant/tasks/done/20260915_1743_aiscc-p3-3-public-live-l1-bytecode-residue-cleanup-authorized-postgresql-retry-1.md`

## companion transport manifest

- `20260915_1743_aiscc-p3-3-public-live-l1-bytecode-residue-blocker-accepted-retry-entry-1.cycle.md`
  - destination: `.aiassistant/records/aiscc/cycles/20260915_1743_aiscc-p3-3-public-live-l1-bytecode-residue-blocker-accepted-retry-entry-1.cycle.md`
  - SHA-256: `d3df523580e2eb0f115e4e2a56e4f7c7101664cdf19d40c34da8b545b9237530`
- `20260915_1743_aiscc-p3-3-public-live-l1-bytecode-residue-browser-judgment-1.md`
  - destination: `.aiassistant/reports/aiscc/20260915_1743_aiscc-p3-3-public-live-l1-bytecode-residue-browser-judgment-1.md`
  - SHA-256: `5a44e454b8c1ccab68010977ebb4c0bf3608760f5c6bfc7155044b3690ef5c09`
- `20260915_1743_aiscc-browser-command-center-p3-3-public-live-l1-bytecode-clean-retry-entry-handoff-1.md`
  - destination: `.aiassistant/reports/aiscc/20260915_1743_aiscc-browser-command-center-p3-3-public-live-l1-bytecode-clean-retry-entry-handoff-1.md`
  - SHA-256: `f504d2d2153698d6346e9dcbfa1c01bb0d70228c391850a5f72e6b23ab5856dd`

For each companion:

- if destination absent, place exact bytes;
- if destination exists, exact SHA-256 equality is required;
- differing bytes => STOP `TRANSPORT_CANONICAL_COLLISION`.

After placement, re-hash all companion destinations.

## exact pre-delivery baseline

Before placing current delivery require:

```text
branch = main
HEAD = 209e7534f66e9b07ce9d33742e6993370a70f4fb
index = empty
tracked worktree = clean
Git-visible untracked = 44 exact
```

### 12 governance/provenance files — preserve

- `.aiassistant/records/aiscc/cycles/20260915_1702_aiscc-p3-3-live-prerequisite-design-frozen-l1-entry-1.cycle.md`
  - SHA-256 `fcc34bc99f4e285c8dcdfe696d3b5db70fe12e076461361d70a9b293cbfaa758`
- `.aiassistant/records/aiscc/cycles/20260915_1718_aiscc-p3-3-public-live-l1-test-environment-blocker-accepted-retry-entry-1.cycle.md`
  - SHA-256 `6ed0ebb242df3cebc99d4d080d8844506199e6dca9869ceeffb3fed178570b2d`
- `.aiassistant/records/aiscc/cycles/20260915_1723_aiscc-p3-3-public-live-l1-transport-contract-blocker-accepted-retry-entry-1.cycle.md`
  - SHA-256 `20cbe1737132e2b06d31014f4db8f8d04be9d51a3103651c3b531b8beced9659`
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
- `.aiassistant/tasks/done/20260915_1702_aiscc-p3-3-public-live-l1-schema-repository-transaction-primitives-implementation-1.md`
  - SHA-256 `102f79a47601c00a8496e1a77a5ddb99d9a5af083d86b215a9c266f4de3df2af`
- `.aiassistant/tasks/done/20260915_1718_aiscc-p3-3-public-live-l1-postgresql-runtime-authorized-implementation-retry-1.md`
  - SHA-256 `32cd6d2e6dbf497c1f5c0382cecf1fef1ddbb46b043afe40ec9890504b46fad8`
- `.aiassistant/tasks/done/20260915_1723_aiscc-p3-3-public-live-l1-transport-manifest-corrected-postgresql-retry-1.md`
  - SHA-256 `4c3279e14c5ee9b866037ea61f347f7157abbb5abf23d1f1e7738198ce3c24a7`

### 32 Executor-generated Python bytecode files — exact cleanup allowlist

- `migrations/versions/__pycache__/20260828_0001_p1_4_workflow_kernel.cpython-312.pyc`
  - SHA-256 `1ddb98158aeb800f5bf61ac73ba0c935e691847d14813156dc2b413c51425a76`
- `migrations/versions/__pycache__/20260828_0002_p1_5_provider_tool_execution.cpython-312.pyc`
  - SHA-256 `95de18080c4809baec8b9f38e6380e9fe214bd5246dc19b2699318799ec42ebf`
- `migrations/versions/__pycache__/20260829_0003_p1_6_evidence_admission.cpython-312.pyc`
  - SHA-256 `aad6a66eb7a40d0390ee146edee3ebfb1ccd6e64849498fb17efde47bb4737b3`
- `migrations/versions/__pycache__/20260829_0004_p1_7_human_gate_judgment.cpython-312.pyc`
  - SHA-256 `ab49d2774002d1dfd2bef8cd71ecbb428b3eb132bad5aa5147c601772ecec35d`
- `migrations/versions/__pycache__/20260830_0005_p1_6_durable_evidence_content.cpython-312.pyc`
  - SHA-256 `d60b90c632492183f1d3eae8e74189b14f7330d94dcae9d90be0c96a734e1b84`
- `migrations/versions/__pycache__/20260831_0006_p1_8_project_memory_cycle_admission.cpython-312.pyc`
  - SHA-256 `f202d3bdeddb42b8b04b6e20f8fd4dcc735f0b0112d1217ff83752df405a6014`
- `migrations/versions/__pycache__/20260831_0007_p1_8_authority_contract_rework.cpython-312.pyc`
  - SHA-256 `d1ec01c066327c71f39c4485c57d815816875e40c149705655eae970daaff084`
- `migrations/versions/__pycache__/20260901_0008_p1_8_prerequisite_authority_reconciliation.cpython-312.pyc`
  - SHA-256 `1c58fdf3f17e99b468e347ddd4989d684d10441b1a43a7c3d2e29114afdd9554`
- `migrations/versions/__pycache__/20260914_0009_task_contract_durable_bodies.cpython-312.pyc`
  - SHA-256 `82934dad59ca30bee5e40b808f8be6c9617d39a57259c96238aebe69aa0e146d`
- `migrations/versions/__pycache__/20260914_0010_external_ide_execution_ingress.cpython-312.pyc`
  - SHA-256 `d77314fd8dbd3cb0960cf327435b126091d70463a10b734b5397fe41fc95138b`
- `migrations/versions/__pycache__/20260914_0011_external_ide_execution_start.cpython-312.pyc`
  - SHA-256 `5a816bcca574954c54f627c00f4a9c5858b953ebe86465f18dc117f5e85b024f`
- `migrations/versions/__pycache__/20260914_0012_self_dogfood_genesis_authority.cpython-312.pyc`
  - SHA-256 `4a23cc13f2dcc024489758e689c53adf541d58f43f48b07a65453661f4bc4933`
- `src/aiscc/__pycache__/__init__.cpython-312.pyc`
  - SHA-256 `06d2481b99a5a8664f3dd696b2abd8f591e1d39c585ff99c2b2f8bfa09729fb9`
- `src/aiscc/contracts/__pycache__/__init__.cpython-312.pyc`
  - SHA-256 `3d0d3ffdc632664f4f6a32d181605740fc9fc2d0874b8f1d7f0f5e244faf24de`
- `src/aiscc/contracts/__pycache__/canonical_json.cpython-312.pyc`
  - SHA-256 `7afe38ba528aba7f36b79529d812e1174fd9932b8601f89f9181e92e94147aa0`
- `src/aiscc/contracts/__pycache__/security.cpython-312.pyc`
  - SHA-256 `6c7619af0222902f65ac721ee4458cd13ef0f629d1a37f659ac5a2d6e3f63741`
- `src/aiscc/contracts/__pycache__/workflow.cpython-312.pyc`
  - SHA-256 `82f06d734047d3b53d29bf82c4933d3f2b160e32f25b5e54a567ae29ff8ff2d3`
- `src/aiscc/persistence/__pycache__/__init__.cpython-312.pyc`
  - SHA-256 `920baa3bccb3c1475a993b375444cbcfc116592533e0a4ebe37cfd0a7030d440`
- `src/aiscc/persistence/__pycache__/database.cpython-312.pyc`
  - SHA-256 `b3b9e7a479d10ecf00f9561be432dfe1321b148d021fda502da4482089c7af3a`
- `src/aiscc/persistence/__pycache__/models.cpython-312.pyc`
  - SHA-256 `7d1cc92d15c26fcbc81f193b9c2767c1697e0d05fd65284d179fa5c864d3d28f`
- `src/aiscc/persistence/__pycache__/repository.cpython-312.pyc`
  - SHA-256 `edde99c6e2f4f6969970e274fe15fe9e0f2f3fa94fd69632ec24be5e014b89b2`
- `src/aiscc/providers/__pycache__/__init__.cpython-312.pyc`
  - SHA-256 `1a0000bba428e7c1753eac26590163be2879a0faff9678be383518f7635a5bb7`
- `src/aiscc/providers/__pycache__/events.cpython-312.pyc`
  - SHA-256 `45693cb5d8c0c059794c78c16965974a27e301000690b2cffe19ff025512014c`
- `src/aiscc/providers/__pycache__/models.cpython-312.pyc`
  - SHA-256 `a1c9adf5adf83bf15ec73b273a8c47c160967e988d9320267b73e5abb314220b`
- `src/aiscc/workflow/__pycache__/__init__.cpython-312.pyc`
  - SHA-256 `b3a6f423a4b6d7f07ab3db7f6a5fed9116db02f67cc47481b4f486f4e78e6acb`
- `src/aiscc/workflow/__pycache__/evaluator.cpython-312.pyc`
  - SHA-256 `1b0729241f18463996e6df492e098d867150d15043173c96f4c700bcd43075a7`
- `src/aiscc/workflow/__pycache__/guards.cpython-312.pyc`
  - SHA-256 `71af9a35ed2e765a1a41d14b86dcce4cb3fc87d507ef1090387382d60e306aff`
- `src/aiscc/workflow/__pycache__/kernel.cpython-312.pyc`
  - SHA-256 `e7d3420af8c46f863d3eba21c538ed44ba5be695bdeb138fa17a35eb143d24be`
- `src/aiscc/workflow/__pycache__/matrix.cpython-312.pyc`
  - SHA-256 `3e646d4ec7cffef9ff25200407e5536a3f922f9484296f8d1511141c0c641f09`
- `src/aiscc/workflow/__pycache__/models.cpython-312.pyc`
  - SHA-256 `55c64f7a9400a6ee89156d7fc0fafa205b16b5a0dda0db3e38ddc2d40efbab05`
- `src/aiscc/workflow/__pycache__/participants.cpython-312.pyc`
  - SHA-256 `b56169a627bcfd3df39857172ed7e94cd845c40a4600577e08d3da0e3142da3e`
- `src/aiscc/workflow/__pycache__/ports.cpython-312.pyc`
  - SHA-256 `0de22d6eb37e5ee9aa262087e7d29c5797342405851a17e74b2b1ad234151a50`

No additional untracked path is allowed.

Any missing/extra/hash mismatch => STOP `L1_RETRY_BASELINE_MISMATCH`.

## exact bytecode cleanup authorization

After the full 44-path baseline is verified and after this Task is placed/read canonically:

Delete exactly the 32 `.pyc` files listed above.

This deletion is explicitly Human/Command-Center-authorized Task cleanup of known Executor-generated runtime residue.

Rules:

- delete no other file;
- do not delete/modify the 12 governance files;
- do not change `.gitignore`;
- do not use broad recursive cleanup commands;
- delete by exact allowlisted file path;
- before deleting each file require exact SHA-256 match;
- if any hash changed, STOP without deleting that file;
- empty `__pycache__` directories may be removed only if empty, but directory cleanup is optional and non-substantive.

After deletion require:

```text
tracked worktree = clean
index = empty
Git-visible untracked = exactly the 12 governance/provenance files
```

plus current ignored active Task / current companions as applicable.

Write target-only:

`BYTECODE_RESIDUE_CLEANUP.json`

with before/after counts, every removed path/hash, and proof no other file was removed.

## bytecode recurrence prevention

Before ANY Python process/import/Alembic/pytest command in this retry set the current shell/process environment:

```text
PYTHONDONTWRITEBYTECODE=1
```

Use the existing `.venv` interpreter with `-B` for every direct Python invocation.

Examples:

```text
.venv\Scripts\python.exe -B -m alembic heads
.venv\Scripts\python.exe -B scripts/build_public_replay.py --check
.venv\Scripts\python.exe -B -m pytest ...
```

Do not invoke bare `alembic`, bare `pytest`, or Python without `-B`.

After every major Python phase check that no new `*.pyc` / `__pycache__` file has become Git-visible.

If new bytecode appears despite these controls, STOP:

`L1_BYTECODE_RECURRENCE`

Do not change `.gitignore` to hide it.

## migration/builder gate

After cleanup:

- Alembic head must remain `20260914_0012`;
- Replay builder must PASS.

Mismatch => STOP.

## PostgreSQL 17.6 local runtime

1723 already proved the local machine can run the required runtime, but that container was removed.

Recreate a fresh Task-owned isolated runtime:

```text
container:
aiscc-p3-3-l1-postgres-17-6

image:
postgres:17.6

network:
127.0.0.1 only

preferred host port:
55432
```

The image was previously cached, but re-check locally.

No network pull is needed or authorized unless the exact image is unexpectedly absent; if absent, STOP `L1_LOCAL_POSTGRES_IMAGE_UNAVAILABLE` rather than broadening network in this retry.

Use disposable local test DB/user/password only in process/container environment.

Do not commit secrets.

Require PostgreSQL reported version 17.6, loopback readiness, asyncpg/SQLAlchemy connection and empty database reset.

Create a new target-only `LOCAL_POSTGRES_RUNTIME.json` before source mutation.

## substantive L1 authority

Read and execute the existing done Tasks in authority order:

1. 1702 original L1 substantive Task;
2. 1718 PostgreSQL environment expansion;
3. 1723 transport correction;
4. this 1743 residue-corrected retry.

The substantive L1 contract is unchanged.

Implement only:

- additive Public Live PostgreSQL schema/migration;
- L1 persistence/domain/repository transaction primitives;
- integer micro-USD substrate;
- exact two-slot model;
- idempotency/dispatch/read-capability constraints;
- rollback/locking/DB-clock primitives;
- fail-closed initialization;
- focused L1 tests/helpers.

Do NOT implement:

- L2 admission service;
- public HTTP routes;
- provider profile/calls;
- frontend;
- Railway/Cloudflare/Wanted;
- Live enablement.

## required PostgreSQL evidence

Execute real PostgreSQL 17.6 tests for all mandatory 1702 L1 cases, including:

- migration from current head;
- default admission disabled;
- exactly slots 1/2 FREE;
- no enabled campaign;
- idempotency uniqueness;
- one-run/one-slot invariants;
- no third slot;
- dispatch ordinal 1/2 only;
- money nonnegative/bounded invariants;
- RESERVE/SETTLE uniqueness/idempotence contract;
- read-capability hash uniqueness;
- observation identity uniqueness;
- UTC timestamps;
- transaction rollback;
- conflicting row-lock serialization;
- DB clock / last_clock regression fail-closed;
- owner/private historical rows and Replay unaffected.

Run relevant regression tests and broader local suite when it requires no new environment/network.

## changed-path plan and staging

Before staging create target-only:

`L1_CHANGED_PATH_PLAN.json`

Allowed categories only:

```text
L1 migration/schema
L1 persistence/domain/repository
L1 focused tests/helpers
12 predecessor governance/provenance paths
current 1743 Task/Cycle/Judgment/Handoff
```

No bytecode path may be staged.

No target/export path may be staged.

Prove staged path set exact-equals the plan.

If any new unrelated dirt appears, STOP without cleanup unless this Task explicitly classifies it.

## commit

On full L1 success only:

```text
feat(aiscc): add public live persistence primitives
```

No push/tag/release.

## Docker terminal cleanup

After evidence/commit attempt, stop/remove only the Task-owned container and its safely identified ephemeral volume.

Preserve shared `postgres:17.6` image.

Cleanup failure alone after successful evidence does not invalidate L1; report residue.

## terminal success invariants

```text
Public Live:
NOT_RELEASED

Public admission:
DISABLED

Public HTTP routes:
NOT_IMPLEMENTED_BY_L1

Provider paid calls:
IMPOSSIBLE_FROM_L1
```

Terminal repository success requires:

```text
index = empty
tracked worktree = clean
Git-visible untracked = 0
no Git-visible Python bytecode residue
```

## result classifications

Success:

`PERSISTENCE_CANDIDATE / L1_IMPLEMENTED`

Allowed blockers:

- `L1_RETRY_BASELINE_MISMATCH`
- `TRANSPORT_CANONICAL_COLLISION`
- `L1_BYTECODE_RECURRENCE`
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

`.aiassistant/reports/target/20260915_1743_aiscc-p3-3-public-live-l1-bytecode-residue-cleanup-authorized-postgresql-retry-1/`

Required root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `TRANSPORT_VERIFICATION.json`
- `BASELINE_VERIFICATION.json`
- `BYTECODE_RESIDUE_CLEANUP.json`
- `LOCAL_POSTGRES_RUNTIME.json`
- `SOURCE_INVENTORY.json`
- `MIGRATION_BASELINE.json`
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
- changed committed files preserving relative paths when success.

Terminal ZIP:

`.aiassistant/reports/target/20260915_1743_aiscc-p3-3-public-live-l1-bytecode-residue-cleanup-authorized-postgresql-retry-1.zip`

## final response

1. result classification
2. transport ordering verification
3. 44-path baseline verification
4. bytecode cleanup proof
5. no-bytecode-recurrence proof
6. PostgreSQL runtime result
7. migration/schema/repository implementation
8. tests/results
9. exact changed-path plan
10. commit hash/parent if success
11. Docker cleanup
12. terminal workspace
13. target ZIP
14. L2 eligibility
