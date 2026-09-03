# AISCC Cycle Record

## meta

- cycle_id: `20260903_1024_aiscc-p2-1a-command-center-read-model-api-partial-acceptance-default-runtime-composition-rework-1`
- date: `2026-09-03T10:24:00+09:00`
- project: `AI Software Command Center (AISCC)`
- primary_semantic_owner: `Browser Command Center P2-1A implementation review`
- affected_areas: `P2-1A read-model/API implementation, FastAPI default application composition`
- work_type: `COMMAND_CENTER_JUDGMENT / REWORK`
- predecessor_head: `6b0383fce036471e6760999a2352276e2806fca5`
- predecessor_task: `.aiassistant/tasks/done/20260903_0910_aiscc-p2-1a-command-center-read-model-api-projection-foundation-implementation-1.md`
- submitted_bundle: `20260903_0910_aiscc-p2-1a-command-center-read-model-api-projection-foundation-implementation-1.zip`
- submitted_bundle_sha256: `379d31d201b65a01fd93707a5d0e30b223f704cb40d15217f577d91705e13bf2`
- result_status: `PARTIAL_ACCEPTED / HOLD_REWORK_REQUIRED / DEFAULT_RUNTIME_COMPOSITION_MISSING`
- reject_cause: `PROOF_TYPE_SUBSTITUTION / TEST_INJECTED_APP_NOT_DEFAULT_APPLICATION_COMPOSITION`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260903_1024_aiscc-p2-1a-command-center-read-model-api-partial-acceptance-default-runtime-composition-rework-1.cycle.md`
- P2_status: `STARTED / P2-1 ACTIVE`
- P2_1A_status: `REWORK_REQUIRED`

## package verification

Browser-side independent verification:

```text
archive SHA-256:
379d31d201b65a01fd93707a5d0e30b223f704cb40d15217f577d91705e13bf2

archive entries:
25

manifest-declared payloads:
13

manifest byte/hash mismatches:
0

changed product/test snapshots:
9

UTF-8/BOM/trailing-whitespace issues:
0

Task SHA-256:
cda8c49df4a8bc3a43de2c40fcc99b44362f968ac73457cafe1752df151c030c
```

## admitted implementation scope

The following implementation work is accepted as a valid P2-1A candidate foundation:

```text
src/aiscc/command_center/__init__.py
src/aiscc/command_center/read_models.py
src/aiscc/command_center/queries.py
src/aiscc/command_center/postgres_queries.py
src/aiscc/command_center/privacy.py
src/aiscc/api/routes/command_center.py
src/aiscc/api/app.py
tests/unit/command_center/test_read_contracts.py
tests/integration/command_center/test_postgres_read_api.py
```

Admitted evidence:

```text
SESSION_AUTHORITY:
NEW_P2_1A_IMPLEMENTATION_CHAT / PASS

targeted tests:
16 passed

applicable unit + integration regression:
227 passed

Ruff:
PASS

mypy:
PASS

git diff --check:
PASS

PostgreSQL repeatable-read/read-only query adapter:
IMPLEMENTED

exact 9 GET API routes:
IMPLEMENTED

ETag / 304:
EXECUTED_PASS

safe 404 / 409 / 503:
EXECUTED_PASS

unsupported POST/PUT/PATCH/DELETE:
405 / no mutation

authoritative event-count vector before/after HTTP sequence:
UNCHANGED
```

The implementation preserves the accepted semantic separations and privacy/read-only boundaries.

## substantive blocker

The exported application composition is:

```python
def create_app(command_center_queries: CommandCenterQueries | None = None) -> FastAPI:
    ...
    application.state.command_center_queries = (
        command_center_queries or UnavailableCommandCenterQueries()
    )
    ...

app = create_app()
```

Therefore the module-level application used by the normal product entrypoint contains:

```text
UnavailableCommandCenterQueries
```

unless an external caller explicitly injects `PostgresCommandCenterQueries`.

The submitted successful HTTP runtime proof used:

```python
create_app(PostgresCommandCenterQueries(create_session_factory(engine)))
```

inside the integration/runtime harness.

The unavailable-composition case was separately tested to return:

```text
503 PROJECTION_UNAVAILABLE
```

This is a correct fail-closed fallback, but it does not prove that the normal AISCC application entrypoint actually
composes the new PostgreSQL Command Center read dependencies when the database is configured.

## why this is a Task-contract failure

The 0910 Task explicitly required:

```text
implement read-only query protocols and PostgreSQL screen/query adapters
...
compose only read dependencies into FastAPI
...
local HTTP runtime
```

The accepted 0313 substrate audit also identified:

```text
src/aiscc/api/app.py:
Command Center router, composition, and read dependencies are all new work

src/aiscc/bootstrap.py:
builds security policy only; does not compose repositories into the web app
```

The current implementation created an injectable composition seam but did not complete the default runtime
composition.

Therefore:

```text
test-injected FastAPI app runtime
!=
default AISCC product application runtime
```

This is proof-type substitution if used to claim the normal application entrypoint is operational.

## accepted / not accepted split

### accepted

- DTO/read-model contract
- status separation
- privacy projection
- PostgreSQL read adapter
- repeatable-read/read-only transaction
- exact route surface
- error envelope
- ETag/cursor semantics
- side-effect-free NextAction query
- unit/integration regression evidence
- injected live-loopback HTTP behavior

### not yet accepted

```text
DEFAULT AISCC APPLICATION COMPOSITION
DEFAULT ENTRYPOINT HTTP AVAILABILITY
P2-1A terminal acceptance
P2-1B start
```

## rework direction

The rework must first read the exact default server/application composition:

```text
src/aiscc/__main__.py
src/aiscc/api/app.py
src/aiscc/persistence/database.py
```

and any exact directly-called bootstrap/config path proven by those files.

It must establish one explicit runtime contract:

```text
database configured
→ default AISCC app composes PostgresCommandCenterQueries
→ /v1/command-center/** is operational

database unavailable/not configured
→ fail closed with PROJECTION_UNAVAILABLE or application-start behavior explicitly justified
```

The exact behavior must fit the existing local/private server configuration and must not add authentication,
network exposure, migration, or package scope.

## workspace / lifecycle

No rollback is required.

The existing nine product/test changes remain the current P2-1A rework baseline.

No Git staging/commit occurred.

The current fresh P2-1A implementation chat may be reused for this narrowly-scoped rework because:

```text
same slice
same product authority
same dirty workspace
no accepted commit boundary crossed
```

## state

```text
P2:
STARTED / P2-1 ACTIVE

P2-1 Design:
HUMAN_PROVIDED / ACCEPTED

P2-1A:
PARTIAL_ACCEPTED / REWORK_REQUIRED

P2-1B:
NOT_STARTED
```

## preserved artifacts

Preserve:

- `.aiassistant/tasks/done/20260903_0910_aiscc-p2-1a-command-center-read-model-api-projection-foundation-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260903_0904_aiscc-p2-1-command-center-web-ui-design-audit-command-center-acceptance-human-design-gate-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260903_0908_aiscc-p2-1-command-center-web-ui-human-design-final-acceptance-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260903_1024_aiscc-p2-1a-command-center-read-model-api-partial-acceptance-default-runtime-composition-rework-1.cycle.md`
- current nine product/test P2-1A candidate files in the dirty worktree.
- accepted baseline commit `6b0383fce036471e6760999a2352276e2806fca5`.

## next action

next_action:
- work_type: `REWORK / BACKEND_IMPLEMENTATION`
- title: `P2-1A default runtime Command Center read composition`
- blocker: `default module-level app uses UnavailableCommandCenterQueries`
- required_baseline: `main@6b0383fce036471e6760999a2352276e2806fca5 + exact current P2-1A nine-file candidate dirt`
- new_IDE_chat_required: `No`
- Human_verification_needed: `No`
