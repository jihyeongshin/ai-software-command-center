# AISCC Cycle Record

## meta

- cycle_id: `20260903_1436_aiscc-p2-1b-human-browser-qa-gate-execution-guidance-correction-1`
- date: `2026-09-03T14:36:00+09:00`
- project: `AI Software Command Center (AISCC)`
- primary_semantic_owner: `Browser Command Center Human QA procedure`
- affected_areas: `P2-1B Human Browser QA runtime/fixture bootstrap guidance`
- work_type: `HUMAN_QA_GATE_CORRECTION`
- predecessor_head: `4ea1fe6f7cb8e11ff5ccfde70462eba931c4071e`
- predecessor_candidate_cycle: `.aiassistant/records/aiscc/cycles/20260903_1431_aiscc-p2-1b-shell-queue-rework-acceptance-pending-human-browser-qa-1.cycle.md`
- superseded_qa_sheet: `20260903_1433_aiscc-p2-1b-human-browser-visual-qa-gate-1.md`
- result_status: `QA_GATE_DOCUMENT_REWORKED / RUNTIME_FIXTURE_GUIDANCE_ADDED / HUMAN_QA_PENDING`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260903_1436_aiscc-p2-1b-human-browser-qa-gate-execution-guidance-correction-1.cycle.md`
- product_source_change: `none`
- P2_1B_status: `ACCEPTED_PENDING_HUMAN_BROWSER_QA`

## correction reason

The first Human QA sheet correctly defined Browser operations but did not tell the Human how to create the runtime
preconditions needed to execute them.

Missing operational guidance:

```text
how to start PostgreSQL
how to migrate the disposable QA database
how to seed a valid Command Center Project/WorkRun fixture
how to obtain the exact generated Project ID
how to start the normal AISCC application with that database
which URL to open
how to verify that the fixture includes terminal/nonterminal rows
how to clean up the QA runtime
```

This made the Human-owned QA gate non-self-contained.

## source-supported runtime facts

Accepted P2-1A/P2-1B evidence established:

```text
normal application entrypoint:
python -m aiscc serve --host 127.0.0.1 --port <port>

Command Center PostgreSQL composition:
AISCC_DATABASE_URL
→ existing create_engine
→ existing create_session_factory
→ PostgresCommandCenterQueries

integration evidence database:
postgres:17.6-alpine
loopback-only published port
Alembic upgrade head

integration seed owner:
tests/integration/command_center/test_postgres_read_api.py::_seed

seed-generated project identity:
cc-project-<uuid>

seed return values:
project_id
accepted_run_id
no_attempt_run_id
cycle_id
selection_id
```

The `project_id` is intentionally generated per seed run and therefore cannot be supplied as a fixed value in a
static Human QA sheet.

## corrected QA posture

The replacement Human QA sheet now contains an exact Windows/PowerShell bootstrap procedure:

```text
Docker Desktop prerequisite
→ disposable PostgreSQL container
→ pg_isready
→ AISCC_DATABASE_URL / AISCC_TEST_DATABASE_URL
→ Alembic upgrade head
→ existing accepted integration _seed helper
→ copy exact printed PROJECT_ID
→ normal python -m aiscc serve entrypoint
→ pre-QA queue sanity check
→ Chrome Human QA
→ Ctrl+C / docker rm -f / environment cleanup
```

The seed helper is used only as a local Human QA fixture producer. It does not become runtime Project authority and
does not alter product source.

## supersession

For P2-1B Human QA execution:

```text
20260903_1433_...human-browser-visual-qa-gate-1.md
= SUPERSEDED_FOR_EXECUTION_GUIDANCE

20260903_1438_...human-browser-visual-qa-gate-with-runtime-fixture-guidance-1.md
= CURRENT HUMAN QA SHEET
```

The QA operations and PASS/REWORK semantic criteria remain materially the same; the replacement adds prerequisite
bootstrap, sanity checks, exact Project ID discovery, and cleanup.

## state

```text
P2-1B source/runtime:
ACCEPTED

Human Browser/Visual QA:
HUMAN_PENDING

P2-1C:
NOT_STARTED
```

## preserved artifacts

Preserve:

- `.aiassistant/records/aiscc/cycles/20260903_1431_aiscc-p2-1b-shell-queue-rework-acceptance-pending-human-browser-qa-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260903_1436_aiscc-p2-1b-human-browser-qa-gate-execution-guidance-correction-1.cycle.md`
- `20260903_1438_aiscc-p2-1b-human-browser-visual-qa-gate-with-runtime-fixture-guidance-1.md` as the current Human QA worksheet during this gate.

The QA worksheet itself is not product/runtime authority.

## next action

next_action:
- owner: `Human`
- work_type: `HUMAN_BROWSER_VISUAL_QA`
- title: `P2-1B Human Browser QA using disposable seeded PostgreSQL fixture`
- IDE_Task_required: `No`
- blocker: `none if Docker Desktop and repository-local .venv are available`
- P2_1C_execution: `forbidden until Human QA + persistence`
