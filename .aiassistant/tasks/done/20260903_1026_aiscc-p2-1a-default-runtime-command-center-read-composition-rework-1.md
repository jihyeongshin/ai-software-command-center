# 작업지시서: P2-1A default runtime Command Center read composition rework

## meta

- task_id: `20260903_1026_aiscc-p2-1a-default-runtime-command-center-read-composition-rework-1`
- created_at: `2026-09-03T10:26:00+09:00`
- project: `AI Software Command Center (AISCC)`
- phase: `P2-1A — Command Center Read-model/API Projection Foundation`
- work_type: `REWORK / BACKEND_IMPLEMENTATION`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- predecessor_head: `6b0383fce036471e6760999a2352276e2806fca5`
- predecessor_task: `.aiassistant/tasks/done/20260903_0910_aiscc-p2-1a-command-center-read-model-api-projection-foundation-implementation-1.md`
- predecessor_judgment_cycle: `.aiassistant/records/aiscc/cycles/20260903_1024_aiscc-p2-1a-command-center-read-model-api-partial-acceptance-default-runtime-composition-rework-1.cycle.md`
- target_bundle: `.aiassistant/reports/target/20260903_1026_aiscc-p2-1a-default-runtime-command-center-read-composition-rework-1/`
- fresh_chat_policy: `REUSE_CURRENT_P2_1A_IMPLEMENTATION_CHAT_ALLOWED`
- implementation_commit_authority: `NONE`
- success_boundary: `P2_1A_REWORK_CANDIDATE / DEFAULT_RUNTIME_COMPOSITION_PROVEN / COMMAND_CENTER_REVIEW_REQUIRED`

## 0. blocker to fix

Current exported application code contains:

```python
app = create_app()
```

and `create_app()` defaults to:

```text
UnavailableCommandCenterQueries
```

The successful HTTP evidence injected:

```text
PostgresCommandCenterQueries(...)
```

from the test harness rather than proving the normal AISCC product entrypoint is composed.

Required correction:

```text
configured local AISCC runtime
→ default application entrypoint
→ PostgreSQL-backed CommandCenterQueries
→ exact 9 /v1/command-center/** reads operational
```

Do not alter the accepted read-model semantics merely to fix composition.

## 1. exact goal

1. transport exact current Task + exact 1024 rework Cycle;
2. reuse the current fresh P2-1A implementation chat;
3. verify baseline HEAD/index and exact current nine-file P2-1A product/test dirt;
4. inspect the real default application/server/database composition;
5. define and implement the narrowest fail-closed PostgreSQL Command Center read dependency composition;
6. prove the normal AISCC default server/application entrypoint uses the PostgreSQL adapter when configured;
7. preserve safe unavailable behavior when the read store cannot be configured;
8. add/update only focused tests necessary for default composition;
9. rerun targeted/static/regression/HTTP no-write evidence;
10. export changed/reworked source evidence;
11. move current Task active→matching done;
12. stop without Git staging/commit.

## 2. do not rework accepted semantics

The following 0910 results are accepted unless the composition correction directly exposes a defect:

```text
read DTO/status separation
privacy allowlist
PostgreSQL query semantics
REPEATABLE READ READ ONLY
ETag/cursor/error contract
exact 9 read routes
Task metadata REFERENCE_ONLY
runtime AdmittedCycle only
side-effect-free NextAction
LOCAL_PRIVATE_ONLY
```

Do not rewrite these for style.

## 3. Downloads transport

Exactly two new files:

```text
C:\Users\oracl\Downloads\20260903_1026_aiscc-p2-1a-default-runtime-command-center-read-composition-rework-1.md
C:\Users\oracl\Downloads\20260903_1024_aiscc-p2-1a-command-center-read-model-api-partial-acceptance-default-runtime-composition-rework-1.cycle.md
```

Destinations:

```text
.aiassistant/tasks/active/20260903_1026_aiscc-p2-1a-default-runtime-command-center-read-composition-rework-1.md
.aiassistant/records/aiscc/cycles/20260903_1024_aiscc-p2-1a-command-center-read-model-api-partial-acceptance-default-runtime-composition-rework-1.cycle.md
```

1024 Cycle expected SHA-256:

```text
95e0bd4170413abd8ddbc5e4743aad4737aa75fc05247b4a1309eb373e558015
```

Precheck both exact sources, absent destinations, and Cycle SHA before moving either.

Failure:

```text
TRANSPORT_PRECONDITION_FAILED
```

All PASS:

- Move, not Copy;
- verify exact destination identity and Downloads source absence.

## 4. session authority

Reuse the current `0910` P2-1A implementation chat.

Required lineage:

```text
0910 fresh implementation chat
→ 1026 same-slice rework
```

No new chat required.

If this is not the same P2-1A implementation chat or another unrelated implementation Task has executed in it,
STOP:

```text
SESSION_LINEAGE_CONFLICT
```

## 5. repository / dirty baseline

Require:

```text
repository == ai-software-command-center
branch == main
HEAD == 6b0383fce036471e6760999a2352276e2806fca5
index == empty
```

Expected current product/test dirt is exactly the P2-1A candidate set:

```text
src/aiscc/api/app.py
src/aiscc/api/routes/command_center.py
src/aiscc/command_center/__init__.py
src/aiscc/command_center/postgres_queries.py
src/aiscc/command_center/privacy.py
src/aiscc/command_center/queries.py
src/aiscc/command_center/read_models.py
tests/integration/command_center/test_postgres_read_api.py
tests/unit/command_center/test_read_contracts.py
```

Expected pre-existing governance/provenance dirt includes the accepted/review lineage:

```text
0311 Cycle
0313 done Task
0904 Cycle
0908 Cycle
0910 done Task
1024 Cycle after transport
```

No unrelated product dirt may be auto-cleaned or absorbed.

## 6. required exact source inspection

Read:

```text
src/aiscc/__main__.py
src/aiscc/api/app.py
src/aiscc/persistence/database.py
```

Then follow only exact directly referenced composition/config helpers required to understand:

```text
aiscc serve
→ uvicorn app target
→ database URL/config resolution
→ engine/session-factory lifecycle
→ FastAPI startup/shutdown lifecycle
```

Report exact call chain before mutation.

Do not bulk-read unrelated application code.

## 7. composition contract

Implement the narrowest source-supported composition.

Required external behavior:

### configured database

When the normal local AISCC server has the existing supported database configuration:

```text
default AISCC application
→ PostgresCommandCenterQueries
→ existing session factory
```

and all exact 9 Command Center endpoints must execute against PostgreSQL without a test-only `create_app(...)`
injection seam.

### unavailable configuration

When Command Center read persistence cannot be configured safely:

```text
fail closed
```

Acceptable behavior must be explicit and tested:

```text
app starts + Command Center returns 503 PROJECTION_UNAVAILABLE
```

or, if existing application configuration policy already requires DB availability at process startup:

```text
startup fails safely with existing configuration semantics
```

Do not invent a third policy.

## 8. engine/session lifecycle

Do not create a new database owner.

Reuse the existing database engine/session-factory primitives.

If app composition owns a created engine, it must be disposed through FastAPI lifespan/startup-shutdown semantics.

Do not:

- create one engine per request;
- leak an engine across test shutdown;
- change transaction semantics in `PostgresCommandCenterQueries`;
- change migration/schema ownership.

If current source proves that correct engine lifecycle requires modifying one exact existing composition path beyond
`src/aiscc/api/app.py`, that path is authorized only if it is:

```text
src/aiscc/__main__.py
```

No other existing product path is pre-authorized for mutation.

If another product path must change:

```text
IMPLEMENTATION_PATH_EXPANSION_REQUIRED
```

STOP before modifying it.

## 9. allowed mutation paths

Existing P2-1A candidate files remain allowed.

For this rework, preferred actual modifications are limited to:

```text
src/aiscc/api/app.py
tests/integration/command_center/test_postgres_read_api.py
tests/unit/command_center/test_read_contracts.py
```

Conditional exact additional existing path:

```text
src/aiscc/__main__.py
```

only if Section 8 source evidence proves it necessary.

Do not add new product modules.

Do not modify:

```text
src/aiscc/persistence/database.py
```

unless a mandatory-stop report first establishes that the existing primitives cannot support correct composition.
This Task does not pre-authorize changing the database owner.

## 10. runtime proof must use the real default entrypoint

The rework HTTP proof MUST NOT prove only:

```python
create_app(PostgresCommandCenterQueries(...))
```

Instead, it must start the same application entrypoint used by normal:

```text
aiscc serve
```

or the exact module/app target proven equivalent by Section 6.

Supply the existing test database URL/config using the same supported configuration mechanism as normal local
runtime.

Required:

```text
default entrypoint + configured DB
→ exact 9 routes operational
```

No special test-only dependency injection may be required for the success path.

## 11. required runtime assertions

Repeat the accepted P2-1A HTTP contract against the default configured entrypoint:

- exact 9 GET endpoints return expected safe envelopes;
- `X-AISCC-Exposure=LOCAL_PRIVATE_ONLY`;
- ETag + `304`;
- HEAD;
- OPTIONS;
- POST/PUT/PATCH/DELETE safe rejection;
- `400 INVALID_QUERY`;
- `404 NOT_FOUND`;
- `409 AUTHORITY_CONFLICT`;
- safe unavailable/composition behavior;
- repeated GET authoritative event counts unchanged.

Also prove:

```text
default configured app:
PostgresCommandCenterQueries active

default unavailable app/config:
fails closed
```

Do not inspect private dependency internals through a debug route.

## 12. static/source tests

Add explicit regression tests proving:

1. the normal app entrypoint is not permanently bound to `UnavailableCommandCenterQueries` when DB configuration is present;
2. configured default composition uses `PostgresCommandCenterQueries`;
3. unavailable configuration fails closed;
4. application-owned engine/session lifecycle closes cleanly;
5. route behavior remains read-only.

Avoid brittle source-text-only assertions when runtime composition can be tested directly.

## 13. verification

Required:

```text
targeted P2-1A unit/integration
repository-local Ruff changed scope
repository-local mypy changed scope
git diff --check
```

Run applicable existing unit+integration regression if no new environment/package/network scope is needed.

HTTP runtime must use local loopback and existing PostgreSQL harness only.

No package installation or external network.

## 14. mandatory stop

STOP if correct default composition requires:

- a new package/dependency;
- a new database/config authority;
- a migration/table;
- authentication/external exposure decision;
- modification outside Section 9;
- P1 semantic owner change;
- non-loopback runtime;
- unrelated dirty source cleanup.

Status:

```text
EVIDENCE_SCOPE_EXPANSION_REQUIRED
or
IMPLEMENTATION_PATH_EXPANSION_REQUIRED
```

Do not substitute test-only injection again.

## 15. export

Target:

```text
.aiassistant/reports/target/20260903_1026_aiscc-p2-1a-default-runtime-command-center-read-composition-rework-1/
```

Required root:

```text
TASK.md
EXECUTOR_REPORT.md
DEFAULT_COMPOSITION_EVIDENCE.md
HTTP_RUNTIME_EVIDENCE.md
EXPORT_MANIFEST.md
```

Export all product/test files changed relative to the original baseline HEAD, preserving repository-relative paths.

`DEFAULT_COMPOSITION_EVIDENCE.md` must include:

- exact `aiscc serve` → application call chain;
- configured database composition path;
- unavailable/fail-closed path;
- engine/session lifecycle;
- exact runtime proof command;
- why the proof is not test-only dependency injection.

## 16. Task lifecycle

After implementation/evidence/export:

```text
.aiassistant/tasks/active/20260903_1026_aiscc-p2-1a-default-runtime-command-center-read-composition-rework-1.md
→
.aiassistant/tasks/done/20260903_1026_aiscc-p2-1a-default-runtime-command-center-read-composition-rework-1.md
```

Move, not Copy.

Do not stage or commit.

## 17. success

Successful candidate:

```text
P2_1A_REWORK_CANDIDATE
/ DEFAULT_RUNTIME_COMPOSITION_PROVEN
/ COMMAND_CENTER_REVIEW_REQUIRED
```

Do not declare:

```text
P2-1A ACCEPTED
P2-1B STARTED
P2-1 ACCEPTED
```

## 18. preserved artifacts

Preserve:

- `.aiassistant/tasks/done/20260903_0910_aiscc-p2-1a-command-center-read-model-api-projection-foundation-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260903_1024_aiscc-p2-1a-command-center-read-model-api-partial-acceptance-default-runtime-composition-rework-1.cycle.md`
- `.aiassistant/tasks/done/20260903_1026_aiscc-p2-1a-default-runtime-command-center-read-composition-rework-1.md`
- current P2-1A product/test candidate dirt
- accepted baseline commit `6b0383fce036471e6760999a2352276e2806fca5`.

Target bundle remains temporary through Browser review.
