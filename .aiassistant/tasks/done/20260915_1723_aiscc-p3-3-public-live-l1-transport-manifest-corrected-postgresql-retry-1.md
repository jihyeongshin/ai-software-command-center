# 작업지시서: P3-3 Public Live L1 transport-manifest-corrected PostgreSQL retry

## meta

- task_id: `20260915_1723_aiscc-p3-3-public-live-l1-transport-manifest-corrected-postgresql-retry-1`
- created_at: `2026-09-15T17:23:57+09:00`
- work_type: `IMPLEMENTATION_RETRY`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- fresh_ide_chat_required: `Yes`
- primary_semantic_owner: `P3-3 Public Live L1 persistence primitives`

## objective

Correct the 1718 delivery transport contract and then resume the unchanged PostgreSQL-runtime-authorized L1 implementation.

The previous stop was transport-only.

No Docker/source/migration/test work was performed after the conflict was detected.

## primary Task transport authority

Current Task ZIP member:

`20260915_1723_aiscc-p3-3-public-live-l1-transport-manifest-corrected-postgresql-retry-1.md`

Exact canonical lifecycle:

```text
initial:
.aiassistant/tasks/active/20260915_1723_aiscc-p3-3-public-live-l1-transport-manifest-corrected-postgresql-retry-1.md

before terminal success/blocker export:
.aiassistant/tasks/done/20260915_1723_aiscc-p3-3-public-live-l1-transport-manifest-corrected-postgresql-retry-1.md
```

The current Task member is authenticated by:

- exact outer delivery ZIP SHA-256 supplied in the Browser short prompt;
- ZIP CRC/member-name verification;
- this exact member filename.

No self-referential member SHA is required.

## §3.3 transport manifest — exact non-primary members

Every remaining ZIP member has an exact destination and expected SHA-256 below.

- member: `20260915_1718_aiscc-p3-3-public-live-l1-postgresql-runtime-authorized-implementation-retry-1.md`
  - destination: `.aiassistant/tasks/done/20260915_1718_aiscc-p3-3-public-live-l1-postgresql-runtime-authorized-implementation-retry-1.md`
  - SHA-256: `32cd6d2e6dbf497c1f5c0382cecf1fef1ddbb46b043afe40ec9890504b46fad8`
  - behavior: `verify_existing_exact_or_place`
- member: `20260915_1718_aiscc-p3-3-public-live-l1-test-environment-blocker-accepted-retry-entry-1.cycle.md`
  - destination: `.aiassistant/records/aiscc/cycles/20260915_1718_aiscc-p3-3-public-live-l1-test-environment-blocker-accepted-retry-entry-1.cycle.md`
  - SHA-256: `6ed0ebb242df3cebc99d4d080d8844506199e6dca9869ceeffb3fed178570b2d`
  - behavior: `place_if_missing_verify_if_present`
- member: `20260915_1718_aiscc-p3-3-public-live-l1-test-environment-blocker-browser-judgment-1.md`
  - destination: `.aiassistant/reports/aiscc/20260915_1718_aiscc-p3-3-public-live-l1-test-environment-blocker-browser-judgment-1.md`
  - SHA-256: `52c23f98f821195bf0a47935f3903fdc5af588ee286ab47d53df63ae292d3d36`
  - behavior: `place_if_missing_verify_if_present`
- member: `20260915_1718_aiscc-browser-command-center-p3-3-public-live-l1-postgresql-runtime-retry-entry-handoff-1.md`
  - destination: `.aiassistant/reports/aiscc/20260915_1718_aiscc-browser-command-center-p3-3-public-live-l1-postgresql-runtime-retry-entry-handoff-1.md`
  - SHA-256: `3beac2a74fc07069a92aa727c127c6508f033fc094188309915f99eb5b5bc235`
  - behavior: `place_if_missing_verify_if_present`
- member: `20260915_1723_aiscc-p3-3-public-live-l1-transport-contract-blocker-accepted-retry-entry-1.cycle.md`
  - destination: `.aiassistant/records/aiscc/cycles/20260915_1723_aiscc-p3-3-public-live-l1-transport-contract-blocker-accepted-retry-entry-1.cycle.md`
  - SHA-256: `20cbe1737132e2b06d31014f4db8f8d04be9d51a3103651c3b531b8beced9659`
  - behavior: `place_exact`
- member: `20260915_1723_aiscc-p3-3-public-live-l1-transport-contract-browser-judgment-1.md`
  - destination: `.aiassistant/reports/aiscc/20260915_1723_aiscc-p3-3-public-live-l1-transport-contract-browser-judgment-1.md`
  - SHA-256: `c024b161e973dad78c1bf36831e14ab515ec27aedb7d041ba8160825f241deda`
  - behavior: `place_exact`
- member: `20260915_1723_aiscc-browser-command-center-p3-3-public-live-l1-transport-corrected-retry-entry-handoff-1.md`
  - destination: `.aiassistant/reports/aiscc/20260915_1723_aiscc-browser-command-center-p3-3-public-live-l1-transport-corrected-retry-entry-handoff-1.md`
  - SHA-256: `6a3398c2ad6cbd66adfa83b339bd89395b1f32310b1f8a528878bf55ed844d0c`
  - behavior: `place_exact`

### placement rule

For `verify_existing_exact_or_place` / `place_if_missing_verify_if_present`:

- if the canonical path exists and hash matches, preserve it;
- if missing, place the exact ZIP member bytes;
- if it exists with a different hash, STOP `TRANSPORT_CANONICAL_COLLISION`;
- never overwrite differing canonical bytes.

For `place_exact`:

- place exact bytes at the destination;
- if already present, require exact SHA-256 equality;
- mismatch => STOP.

After placement, re-hash every destination and require equality with this manifest.

Only after the full transport manifest passes may substantive work begin.

## corrected candidate baseline before this delivery

Require:

```text
branch = main
HEAD = 209e7534f66e9b07ce9d33742e6993370a70f4fb
index = empty
tracked worktree = clean
```

Before placing this new delivery, expected Git-visible untracked is exactly five paths:

### 1702 provenance

- `.aiassistant/tasks/done/20260915_1702_aiscc-p3-3-public-live-l1-schema-repository-transaction-primitives-implementation-1.md`
  - SHA-256 `102f79a47601c00a8496e1a77a5ddb99d9a5af083d86b215a9c266f4de3df2af`
- `.aiassistant/records/aiscc/cycles/20260915_1702_aiscc-p3-3-live-prerequisite-design-frozen-l1-entry-1.cycle.md`
  - SHA-256 `fcc34bc99f4e285c8dcdfe696d3b5db70fe12e076461361d70a9b293cbfaa758`
- `.aiassistant/reports/aiscc/20260915_1702_aiscc-p3-3-live-prerequisite-design-freeze-final-browser-acceptance-1.md`
  - SHA-256 `cba13ba6e9215f23ef4277fe72d240ce9eefdf70d7023e111111ddc943f379bc`
- `.aiassistant/reports/aiscc/20260915_1702_aiscc-browser-command-center-p3-3-public-live-l1-implementation-entry-handoff-1.md`
  - SHA-256 `be0ea77af7091b8e57df34868a2e475c7bed89b7dcec7d4619107c5c2d4ab870`

### 1718 Task

```text
.aiassistant/tasks/done/20260915_1718_aiscc-p3-3-public-live-l1-postgresql-runtime-authorized-implementation-retry-1.md
SHA-256 32cd6d2e6dbf497c1f5c0382cecf1fef1ddbb46b043afe40ec9890504b46fad8
```

Any extra/missing/hash mismatch => STOP `L1_RETRY_BASELINE_MISMATCH`.

Do not clean/reset/delete these paths.

## predecessor 1718 substantive contract

After transport verification, read:

`.aiassistant/tasks/done/20260915_1718_aiscc-p3-3-public-live-l1-postgresql-runtime-authorized-implementation-retry-1.md`

Its substantive L1 implementation contract remains authoritative and is incorporated here by reference.

This retry changes only:

1. transport completeness;
2. current provenance lineage.

The already-authorized environment scope remains:

```text
isolated local PostgreSQL 17.6
local Docker Desktop/Engine
loopback-only container
official Docker Hub postgres:17.6 pull only if image is not cached
```

No other external network/service is authorized.

## mandatory pre-implementation gates

After transport passes:

1. confirm Alembic head is still `20260914_0012`;
2. run Replay builder with the existing repository Python/.venv environment;
3. inspect `docker version` and `docker info`;
4. follow the exact 1718 Docker/PostgreSQL rules;
5. create target-only `LOCAL_POSTGRES_RUNTIME.json` before source mutation.

If the Docker engine requires admin elevation, installation/repair, interactive policy bypass, or cannot be started under the authorized local user session:

`L1_LOCAL_POSTGRES_ENGINE_HUMAN_START_REQUIRED`

If exact official `postgres:17.6` cannot be obtained under the allowed image-pull scope:

`L1_LOCAL_POSTGRES_IMAGE_UNAVAILABLE`

## L1 implementation boundary

Execute the full original 1702/1718 L1 contract:

- additive Public Live PostgreSQL schema;
- durable repository transaction primitives;
- integer micro-USD budget substrate;
- exact two-slot model;
- idempotency/dispatch/read-capability constraints;
- rollback and row-lock evidence;
- DB clock/last_clock fail-closed behavior;
- fail-closed migration initialization;
- focused and relevant PostgreSQL integration tests.

Do NOT implement:

- L2 admission service;
- public HTTP routes;
- provider calls/profile;
- frontend;
- Railway/Cloudflare/Wanted changes;
- Live enablement.

## source/commit boundary

On success, preserve in the commit:

- four 1702 provenance paths;
- complete 1718 quartet;
- complete 1723 quartet;
- L1 migration/schema;
- L1 persistence/domain/repository implementation;
- L1-focused tests/helpers.

Before staging create exact target-only:

`L1_CHANGED_PATH_PLAN.json`

Stage exactly that plan.

No target/export artifact may be staged.

Commit message exactly:

```text
feat(aiscc): add public live persistence primitives
```

No push/tag/release.

## mandatory success invariants

At success:

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

L2 becomes eligible only after Browser acceptance of this result.

## result classifications

Success:

`PERSISTENCE_CANDIDATE / L1_IMPLEMENTED`

Allowed blockers:

- `L1_RETRY_BASELINE_MISMATCH`
- `TRANSPORT_CANONICAL_COLLISION`
- `L1_MIGRATION_BASELINE_CHANGED`
- `L1_LOCAL_POSTGRES_ENGINE_HUMAN_START_REQUIRED`
- `L1_LOCAL_POSTGRES_IMAGE_UNAVAILABLE`
- `L1_POSTGRES_CONTAINER_NAME_CONFLICT`
- `L1_REPOSITORY_ARCHITECTURE_CONFLICT`
- `L1_MIGRATION_POLICY_BLOCK`
- `L1_TEST_BLOCKED`
- `L1_IMPLEMENTATION_REWORK_REQUIRED`
- `EVIDENCE_SCOPE_EXPANSION_REQUIRED`

## target export

Target:

`.aiassistant/reports/target/20260915_1723_aiscc-p3-3-public-live-l1-transport-manifest-corrected-postgresql-retry-1/`

Required root artifacts:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `TRANSPORT_VERIFICATION.json`
- `LOCAL_POSTGRES_RUNTIME.json` when environment gate is reached
- `SOURCE_INVENTORY.json`
- `MIGRATION_BASELINE.json`
- `SCHEMA_INVENTORY.json`
- `CONSTRAINT_INDEX_INVENTORY.json`
- `REPOSITORY_PRIMITIVE_INVENTORY.json`
- `L1_SECURITY_TEST_MATRIX.json`
- `TEST_RESULTS.json`
- `FAIL_CLOSED_INITIALIZATION.json`
- `L1_CHANGED_PATH_PLAN.json`
- `STAGED_COMMIT_MANIFEST.json` when commit candidate exists
- `POSTCOMMIT_VERIFICATION.json` when commit occurs
- `TERMINAL_WORKSPACE.json`
- changed committed files preserving repository-relative paths when applicable.

Terminal ZIP:

`.aiassistant/reports/target/20260915_1723_aiscc-p3-3-public-live-l1-transport-manifest-corrected-postgresql-retry-1.zip`

## final response

1. result classification
2. transport manifest verification
3. baseline/provenance verification
4. local PostgreSQL result
5. migration/schema/repository implementation
6. tests
7. exact changed-path plan
8. commit hash/parent if success
9. Docker cleanup/residue
10. terminal workspace
11. target ZIP
12. whether L2 is eligible
