# 작업지시서: P3-3 Public Live L1 PostgreSQL-runtime-authorized implementation retry

## meta

- task_id: `20260915_1718_aiscc-p3-3-public-live-l1-postgresql-runtime-authorized-implementation-retry-1`
- created_at: `2026-09-15T17:18:35+09:00`
- work_type: `IMPLEMENTATION_RETRY`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- fresh_ide_chat_required: `Yes`
- primary_semantic_owner: `P3-3 Public Live L1 persistence primitives`

## objective

Resume the blocked 1702 L1 implementation with one explicit evidence-scope expansion:

```text
isolated local PostgreSQL 17.6 runtime
```

Then implement and verify the original frozen L1 additive schema/repository transaction primitives.

This Task supersedes only the missing local PostgreSQL test-environment prerequisite.

All original L1 product/security boundaries remain unchanged.

## exact baseline gate

Before any Docker/environment mutation or source edit require:

```text
branch = main
HEAD = 209e7534f66e9b07ce9d33742e6993370a70f4fb
index = empty
tracked worktree = clean
```

Expected Git-visible untracked is exactly the four 1702 governance/provenance paths:

- `.aiassistant/tasks/done/20260915_1702_aiscc-p3-3-public-live-l1-schema-repository-transaction-primitives-implementation-1.md`
  - SHA-256 `102f79a47601c00a8496e1a77a5ddb99d9a5af083d86b215a9c266f4de3df2af`
- `.aiassistant/records/aiscc/cycles/20260915_1702_aiscc-p3-3-live-prerequisite-design-frozen-l1-entry-1.cycle.md`
  - SHA-256 `fcc34bc99f4e285c8dcdfe696d3b5db70fe12e076461361d70a9b293cbfaa758`
- `.aiassistant/reports/aiscc/20260915_1702_aiscc-p3-3-live-prerequisite-design-freeze-final-browser-acceptance-1.md`
  - SHA-256 `cba13ba6e9215f23ef4277fe72d240ce9eefdf70d7023e111111ddc943f379bc`
- `.aiassistant/reports/aiscc/20260915_1702_aiscc-browser-command-center-p3-3-public-live-l1-implementation-entry-handoff-1.md`
  - SHA-256 `be0ea77af7091b8e57df34868a2e475c7bed89b7dcec7d4619107c5c2d4ab870`

Every path/hash MUST match.

Extra/missing/hash mismatch => STOP:

`L1_RETRY_BASELINE_MISMATCH`

Do not clean/reset/delete predecessor provenance.

After this delivery, current Cycle/Judgment/Handoff are additionally authorized provenance and current Task is active/ignored.

## migration baseline

Before source mutation confirm current Alembic head remains:

```text
20260914_0012
```

If repository current head differs, STOP:

`L1_MIGRATION_BASELINE_CHANGED`

and report the actual head without editing.

## mandatory canonical authority

Read the current canonical frozen design and original 1702 done Task.

At minimum:

- `.aiassistant/tasks/done/20260915_1702_aiscc-p3-3-public-live-l1-schema-repository-transaction-primitives-implementation-1.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_ADMISSION_SECURITY_DESIGN.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_DB_SCHEMA_PLAN.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_FAILURE_STATE_MACHINE.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_HUMAN_DECISIONS.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_IMPLEMENTATION_SEQUENCE.json`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_SECURITY_TEST_MATRIX.json`
- current migration/persistence/test configuration.

The original 1702 Task remains the substantive L1 contract unless this retry explicitly changes environment handling.

## builder baseline

Use the existing project Python environment that 1702 proved workable.

Run:

```text
python scripts/build_public_replay.py --check
```

or the repository's exact existing `.venv` interpreter equivalent if `python` is not on PATH.

PASS required.

Do not create a new Python environment.

## newly authorized local PostgreSQL environment

### target

```text
PostgreSQL:
17.6

purpose:
isolated L1 integration/migration test runtime only

network exposure:
127.0.0.1 only

hosted/external:
forbidden
```

### Docker engine

First inspect local Docker availability without mutation:

```text
docker version
docker info
```

If engine is already healthy, continue.

If Docker Desktop is installed but the engine is stopped, this Task authorizes starting the existing local Docker Desktop application/service under the current user.

Use the installed product's normal local start mechanism only.

Wait a bounded period, maximum 120 seconds, for `docker info` to succeed.

Do not change Docker global settings.

If Docker cannot be started without administrator escalation, interactive GUI approval, policy bypass, installation or repair:

STOP:

`L1_LOCAL_POSTGRES_ENGINE_HUMAN_START_REQUIRED`

Do not edit product source.

### image

Check exact image locally first:

```text
postgres:17.6
```

If it is not cached, this Task authorizes exactly one external image acquisition:

```text
official Docker Hub postgres:17.6 image only
```

No other external network is allowed.

After pull, record:

- image ID;
- RepoDigest if available;
- image creation metadata;
- PostgreSQL reported version.

If pull requires login, credential creation, policy bypass or another registry:

STOP:

`L1_LOCAL_POSTGRES_IMAGE_UNAVAILABLE`

### container

Use a Task-owned container name:

```text
aiscc-p3-3-l1-postgres-17-6
```

Before creation, inspect whether that exact name exists.

If absent, create a new container.

If present:

- reuse only if it is clearly Task-owned, image/version match exactly, and no non-Task data is attached;
- otherwise STOP `L1_POSTGRES_CONTAINER_NAME_CONFLICT`.

Bind only to loopback.

Preferred host port:

```text
127.0.0.1:55432 -> 5432
```

If 55432 is occupied, choose another free loopback high port and record it.

Use disposable local-only values such as:

```text
database:
aiscc_public_live_l1_test

user:
aiscc_l1_test

password:
local-disposable-test-only
```

These values are not production credentials and MUST NOT be committed.

Do not print unrelated environment variables or secrets.

Use an ephemeral named/anonymous Docker volume or container-local storage.

Do not mount repository source into PostgreSQL.

### readiness

Require:

- PostgreSQL server reports version 17.6;
- loopback connection succeeds;
- repository test/migration client can connect;
- empty isolated test database can be created/reset.

Do not connect to any other local or remote database.

## repository test DB configuration

Inspect the current repository's exact test configuration and determine the supported database URL/env-var mechanism.

Do not invent an env-var name if the repository already defines one.

Inject the disposable test DSN only into the current process/test command environment.

Do not create or commit `.env` files unless the original L1 Task and repository policy explicitly require a tracked test fixture, which is not expected here.

## environment evidence gate before source mutation

Before editing L1 source, create target-only:

`LOCAL_POSTGRES_RUNTIME.json`

including:

- Docker engine status;
- image identity/digest;
- container name;
- PostgreSQL version;
- loopback host/port;
- repository test-env variable NAME only;
- migration baseline head;
- connection/readiness PASS;
- no secret value.

Only after this evidence is PASS may L1 implementation begin.

## substantive implementation contract

Now execute the original 1702 L1 Task in full.

Implement the frozen additive Public Live persistence substrate for the separate Public Live PostgreSQL DB.

Required concepts remain:

```text
public_control
public_campaign
public_day
public_client
public_run
public_idempotency
public_rate_event
public_reservation
public_slot
public_outbox
public_dispatch
public_money_event
public_observation
```

Required fail-closed initial state remains:

```text
admission disabled
slots 1 and 2 only, FREE
no enabled campaign
no provider credential/config
no implicit positive spend authority
```

Required money authority remains integer micro-USD.

Required lock-order/repository primitive/constraint/index/test contract remains exactly as in the 1702 Task and frozen canonical design.

Do not collapse L2 admission orchestration into L1.

## test requirements

With the authorized PostgreSQL 17.6 runtime, execute the full L1 PostgreSQL integration evidence required by the 1702 Task.

At minimum the mandatory L1 cases from 1702 must execute against real PostgreSQL, including:

- migration;
- constraints;
- uniqueness;
- rollback;
- row locking/serialization;
- DB clock/last_clock regression behavior;
- fail-closed initialization.

Also run existing relevant persistence/security regressions and the normal broader local automated suite if it does not require another new environment/network.

If a different new environment is required, STOP again with `EVIDENCE_SCOPE_EXPANSION_REQUIRED`; do not silently broaden.

## Docker cleanup

After all required database evidence is captured, attempt:

```text
stop/remove Task-owned container
remove Task-owned ephemeral volume if safely identifiable
```

Do not remove shared images, shared volumes or unrelated containers.

Cleanup is best-effort housekeeping.

If cleanup alone is blocked after successful evidence/commit, do NOT invalidate an otherwise successful L1 result.

Report exact local residue as non-blocking.

## source boundaries

Same as 1702.

Allowed only:

- L1 migration/schema;
- L1 persistence/domain/repository;
- focused tests/helpers;
- 1702 predecessor governance provenance;
- current 1718 governance provenance.

Forbidden:

- `public/replay/**`;
- frontend;
- public API routes;
- provider adapter/profile;
- Railway/Cloudflare;
- Live admission service;
- competition submission;
- unrelated refactor.

## changed-path plan

Before staging, generate target-only:

`L1_CHANGED_PATH_PLAN.json`

It must include exact source/migration/test/governance allowlist.

Stage exactly that plan.

Because the 1702 blocker lineage is currently untracked, a successful retry commit MUST preserve those four predecessor provenance files unchanged.

Current 1718 Task/Cycle/Judgment/Handoff must also be persisted.

No target files are staged.

## commit

On complete L1 success only:

```text
feat(aiscc): add public live persistence primitives
```

No push/tag/release.

If implementation or required test fails, do not create a success commit merely to persist partial source.

Classify and export the blocker/rework evidence.

## post-success invariants

Must remain:

```text
Public Live:
NOT_RELEASED

Public admission:
DISABLED

Public HTTP routes:
NOT_IMPLEMENTED_BY_L1

Provider paid calls:
IMPOSSIBLE_FROM_L1

L2:
not implemented
```

## result classifications

Success:

```text
PERSISTENCE_CANDIDATE / L1_IMPLEMENTED
```

Environment blockers:

```text
L1_LOCAL_POSTGRES_ENGINE_HUMAN_START_REQUIRED
L1_LOCAL_POSTGRES_IMAGE_UNAVAILABLE
L1_POSTGRES_CONTAINER_NAME_CONFLICT
```

Other allowed blockers:

```text
L1_RETRY_BASELINE_MISMATCH
L1_MIGRATION_BASELINE_CHANGED
L1_REPOSITORY_ARCHITECTURE_CONFLICT
L1_MIGRATION_POLICY_BLOCK
L1_TEST_BLOCKED
L1_IMPLEMENTATION_REWORK_REQUIRED
EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

## target export

Target:

`.aiassistant/reports/target/20260915_1718_aiscc-p3-3-public-live-l1-postgresql-runtime-authorized-implementation-retry-1/`

Required root artifacts:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
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
- `STAGED_COMMIT_MANIFEST.json` when commit candidate exists
- `POSTCOMMIT_VERIFICATION.json` when commit occurs
- `TERMINAL_WORKSPACE.json`
- changed committed files preserving repository-relative paths when applicable.

Terminal ZIP:

`.aiassistant/reports/target/20260915_1718_aiscc-p3-3-public-live-l1-postgresql-runtime-authorized-implementation-retry-1.zip`

## final response

1. result classification
2. baseline/provenance verification
3. local PostgreSQL environment result
4. migration head before/after
5. schema/repository primitives
6. fail-closed defaults
7. PostgreSQL tests/results
8. broader relevant regression results
9. exact changed path plan
10. commit hash/parent if success
11. Docker cleanup/residue
12. terminal workspace
13. target bundle + ZIP
14. whether L2 is eligible
