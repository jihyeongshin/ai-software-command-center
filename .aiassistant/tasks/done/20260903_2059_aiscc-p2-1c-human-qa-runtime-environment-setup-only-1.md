# 작업지시서: P2-1C Human QA Runtime Environment Setup Only

## meta

- task_id: `20260903_2059_aiscc-p2-1c-human-qa-runtime-environment-setup-only-1`
- created_at: `2026-09-03T20:59:00+09:00`
- project: `AI Software Command Center (AISCC)`
- phase: `P2-1C`
- work_type: `QA_ENVIRONMENT_SETUP_ONLY`
- evidence_profile: `BASIC`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `local disposable Human QA runtime bootstrap`

## 현재 상태

Human P2-1C Browser QA 문서는 이미 별도로 발행되어 있으며 **수정하거나 대체하지 않는다**.

Current Human QA Task:

```text
20260903_2029_aiscc-p2-1c-workrun-detail-human-browser-qa-1.md
```

Current P2-1C state:

```text
SOURCE_RUNTIME_ACCEPTED_CANDIDATE
HUMAN_QA_OPENED
OVERALL_NOT_ACCEPTED_OR_CLOSED
```

Current accepted repository base:

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

accepted HEAD:
62a3c5135a12afc38ba32e4c5f651c1f1b007549
```

P2-1C source/test candidate remains uncommitted.

Human reports that the previous QA runtime was intentionally cleaned up:

```text
AISCC web server:
stopped

QA PostgreSQL container:
removed

AISCC_DATABASE_URL:
cleared

AISCC_TEST_DATABASE_URL:
cleared
```

Therefore this Task recreates only the disposable local QA runtime.

## 이번 턴 목표

1. source/config/Git를 변경하지 않고 disposable PostgreSQL QA database를 다시 생성한다.
2. current repository migration을 `upgrade head`까지 적용한다.
3. existing accepted P2-1A integration `_seed` helper로 QA fixture를 생성한다.
4. generated Project/WorkRun IDs를 exact하게 확보한다.
5. current P2-1C candidate를 normal product entrypoint로 `127.0.0.1`에 기동한다.
6. queue 및 WorkRun detail read endpoints가 200으로 접근 가능한지 narrow sanity check한다.
7. Human이 즉시 기존 `20260903_2029 ... Human Browser QA` 문서를 수행할 수 있도록 DB와 AISCC server를 **실행 상태로 남긴다**.
8. 실제 사용 중인 DB port, server port, Project ID, useful WorkRun IDs, server PID를 최종 응답에 제공한다.

## 이번 턴 비목표

- Human QA 수행
- Human QA PASS/FAIL 판정
- QA 문서 생성/수정
- product/test source 수정
- migration source 수정
- fixture helper 수정
- 새 fixture source 작성
- P2-1D/P2-1E 작업
- Git add/commit/push
- deployment
- source cleanup
- `__pycache__` / `.pyc` cleanup
- broad test suite 실행

## authority / accepted runtime facts

Accepted runtime bootstrap:

```text
PostgreSQL:
postgres:17.6-alpine

binding:
loopback only

database composition:
AISCC_DATABASE_URL
→ existing create_engine
→ existing create_session_factory
→ PostgresCommandCenterQueries

migration:
python -m alembic upgrade head

fixture producer:
tests/integration/command_center/test_postgres_read_api.py::_seed

seed return values:
project_id
accepted_run_id
no_attempt_run_id
cycle_id
selection_id

normal application:
python -m aiscc serve --host 127.0.0.1 --port <port>
```

The seed helper is only a local QA fixture producer.
It does not become product authority and must not be edited.

## preflight

Before environment creation:

```powershell
cd C:\Users\oracl\IdeaProjects\ai-software-command-center

git branch --show-current
git rev-parse HEAD
git diff --cached --name-only
git status --short

docker version
docker image inspect postgres:17.6-alpine
```

Required:

```text
branch == main
HEAD == 62a3c5135a12afc38ba32e4c5f651c1f1b007549
Git index == empty
postgres:17.6-alpine local image == present
repository-local .venv == present
```

Current P2-1C candidate dirt and previously reported Python bytecode residue are expected.
Do not clean or restore them.

If unrelated product/config/migration dirt or non-empty index is discovered:

```text
DIRTY_WORKSPACE_MIXED
```

STOP before environment creation.

If `postgres:17.6-alpine` is absent:

```text
QA_FIXTURE_REQUIRED
reason:
postgres:17.6-alpine local image unavailable
```

Do not pull an image.

## runtime residue guard

Before Python commands:

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
```

Use it for migration, seed, sanity helper, and server process where possible.

This is to avoid adding new `.pyc` residue merely from QA environment setup.

Existing bytecode residue must not be cleaned.

## Step 1 — disposable PostgreSQL

Use a new P2-1C-specific container name:

```text
aiscc-p2-1c-human-qa
```

Check first:

```powershell
docker ps -a --filter "name=^/aiscc-p2-1c-human-qa$"
```

If a container with this exact name already exists, do not silently delete it.

Classify:

```text
QA_RUNTIME_NAME_COLLISION
```

and STOP unless it is provably the current Task-created container from this same turn.

Preferred loopback port:

```text
127.0.0.1:55439
```

Check whether the host port is available.
If unavailable, use `55440`, then `55441` if necessary.
Do not bind to `0.0.0.0`.

Create:

```powershell
docker run --name aiscc-p2-1c-human-qa --pull=never `
  -e POSTGRES_USER=aiscc `
  -e POSTGRES_PASSWORD=aiscc-local-qa `
  -e POSTGRES_DB=aiscc `
  -p 127.0.0.1:<DB_PORT>:5432 `
  -d postgres:17.6-alpine
```

Readiness:

```powershell
docker exec aiscc-p2-1c-human-qa pg_isready -U aiscc -d aiscc
```

Do not proceed until:

```text
accepting connections
```

## Step 2 — environment variables

Set in the setup PowerShell:

```powershell
$env:AISCC_DATABASE_URL = "postgresql+asyncpg://aiscc:aiscc-local-qa@127.0.0.1:<DB_PORT>/aiscc"
$env:AISCC_TEST_DATABASE_URL = $env:AISCC_DATABASE_URL
$env:PYTHONDONTWRITEBYTECODE = "1"
```

Do not print the full credential-bearing URL in the final report.

Final report may state only:

```text
DB:
127.0.0.1:<DB_PORT>/aiscc
```

## Step 3 — Alembic

Execute:

```powershell
.\.venv\Scripts\python.exe -m alembic upgrade head
```

Must PASS.

Do not edit migration files.

Optionally record current head without changing anything:

```powershell
.\.venv\Scripts\python.exe -m alembic current
```

## Step 4 — accepted QA seed

Execute the existing accepted fixture helper exactly as a fixture producer:

```powershell
$seedOutput = & .\.venv\Scripts\python.exe -c "import os,sys; sys.path.insert(0, r'tests/integration/command_center'); import test_postgres_read_api as t; r=t.run(t._seed(os.environ['AISCC_TEST_DATABASE_URL'])); print('PROJECT_ID='+r['project_id']); print('ACCEPTED_RUN_ID='+r['accepted_run_id']); print('NO_ATTEMPT_RUN_ID='+r['no_attempt_run_id']); print('CYCLE_ID='+r['cycle_id']); print('SELECTION_ID='+r['selection_id'])"
$seedOutput
```

Capture:

```powershell
$projectId = (($seedOutput | Select-String '^PROJECT_ID=').Line -replace '^PROJECT_ID=','')
$acceptedRunId = (($seedOutput | Select-String '^ACCEPTED_RUN_ID=').Line -replace '^ACCEPTED_RUN_ID=','')
$noAttemptRunId = (($seedOutput | Select-String '^NO_ATTEMPT_RUN_ID=').Line -replace '^NO_ATTEMPT_RUN_ID=','')
$cycleId = (($seedOutput | Select-String '^CYCLE_ID=').Line -replace '^CYCLE_ID=','')
$selectionId = (($seedOutput | Select-String '^SELECTION_ID=').Line -replace '^SELECTION_ID=','')
```

Required:

```text
projectId != empty
acceptedRunId != empty
noAttemptRunId != empty
```

Do not invent fixed IDs.

## Step 5 — start normal AISCC server and leave it running

Preferred server port:

```text
8765
```

If unavailable, use `8766`, then `8767`.

The server must bind only:

```text
127.0.0.1
```

Use the normal product entrypoint:

```powershell
.\.venv\Scripts\python.exe -m aiscc serve --host 127.0.0.1 --port <SERVER_PORT>
```

Because the Executor turn must finish while the Human continues QA, explicitly authorized behavior for this setup-only Task is:

- start the server as a local child/background process;
- inherit the current `AISCC_DATABASE_URL` and `PYTHONDONTWRITEBYTECODE=1`;
- record the exact PID;
- redirect stdout/stderr only to ignored temporary target files if needed;
- leave the process running after this Task completes.

Do not use a shell/network exposure beyond loopback.

If using PowerShell `Start-Process`, use repository-local Python and record the PID.

Example shape:

```powershell
$server = Start-Process `
  -FilePath ".\.venv\Scripts\python.exe" `
  -ArgumentList "-m","aiscc","serve","--host","127.0.0.1","--port","<SERVER_PORT>" `
  -PassThru

$server.Id
```

If the local PowerShell/IDE runner does not preserve inherited environment for `Start-Process`, use the narrowest equivalent local child-process method.
Do not modify source/config to solve process launch.

## Step 6 — readiness / sanity

Wait only until the local server is responsive.

Required UI shell:

```text
GET http://127.0.0.1:<SERVER_PORT>/command-center
→ 200
```

Required queue:

```text
GET http://127.0.0.1:<SERVER_PORT>/v1/command-center/projects/<PROJECT_ID>/queue?limit=100
→ 200
```

Print only safe summary:

```text
work_run_id
WorkflowState
ExecutionStatus
```

Verify:

```text
at least 1 WorkRun exists
acceptedRunId is present
```

## Step 7 — P2-1C detail sanity

For both:

```text
<ACCEPTED_RUN_ID>
<NO_ATTEMPT_RUN_ID>
```

check:

```text
GET /v1/command-center/work-runs/{work_run_id}
GET /v1/command-center/work-runs/{work_run_id}/transitions
GET /v1/command-center/work-runs/{work_run_id}/execution
```

Expected:

```text
HTTP 200
```

Do not mutate fixture data to manufacture a specific UI appearance.

Report for each seed run only:

```text
work_run_id
WorkflowState
ExecutionStatus
transition item count
execution attempt count
```

If returned transition decisions include both `ADMITTED` and `DENIED`, report which WorkRun ID is useful for Human QA Operation 3.

If not, report:

```text
ADMITTED_DENIED_COMBINED_FIXTURE:
NOT_AVAILABLE_IN_ACCEPTED_SEED
```

Do not create a new ad-hoc DB mutation merely to satisfy that optional Human QA observation.

## Step 8 — direct Human QA URLs

Provide:

```text
Landing:
http://127.0.0.1:<SERVER_PORT>/command-center

Project:
http://127.0.0.1:<SERVER_PORT>/command-center/projects/<PROJECT_ID>

Accepted WorkRun detail:
http://127.0.0.1:<SERVER_PORT>/command-center/work-runs/<ACCEPTED_RUN_ID>

No-attempt WorkRun detail:
http://127.0.0.1:<SERVER_PORT>/command-center/work-runs/<NO_ATTEMPT_RUN_ID>
```

If queue sanity discovers a more useful nonterminal WorkRun ID, also report its exact detail URL.

## success disposition — IMPORTANT

On successful setup:

```text
DO NOT CLEAN UP
```

Leave running:

```text
aiscc-p2-1c-human-qa PostgreSQL container
AISCC local web server child process
```

Do not remove:

```text
AISCC database
fixture rows
server process
```

The Human will use them immediately with the already-issued P2-1C QA document.

Cleanup occurs only after Human QA is finished.

## failure cleanup

If this setup Task creates a PostgreSQL container or server process and later setup fails before reaching `QA_RUNTIME_READY`:

- terminate only the server process created by this Task;
- remove only `aiscc-p2-1c-human-qa` created by this Task;
- do not clean source/Git/Python residue;
- report the exact failed step.

Never remove a pre-existing unrelated process/container.

## source/Git prohibitions

Absolutely forbidden:

```text
source modification
test modification
migration modification
QA document modification
.gitignore modification
git add
git commit
git push
git restore
git checkout
git reset
git stash
git clean
source cleanup
bytecode cleanup
deployment
external network/provider call
Docker image pull
```

## Task lifecycle / report

This is an environment setup Executor turn.

After successful setup and sanity checks:

```text
.aiassistant/tasks/active/20260903_2059_aiscc-p2-1c-human-qa-runtime-environment-setup-only-1.md
→
.aiassistant/tasks/done/20260903_2059_aiscc-p2-1c-human-qa-runtime-environment-setup-only-1.md
```

`done` means the setup turn completed; it does not mean Human QA passed.

A minimal target report may be created at:

```text
.aiassistant/reports/target/20260903_2059_aiscc-p2-1c-human-qa-runtime-environment-setup-only-1/
```

Required root:

```text
TASK.md
EXECUTOR_REPORT.md
EXPORT_MANIFEST.md
```

No source snapshot is required because product/test bytes must not change.

Do not stop the server/container merely because the Task is moved to done.

## final response format

Return exactly the operational facts needed by Human:

```text
result:
QA_RUNTIME_READY / BLOCKED

database:
container = aiscc-p2-1c-human-qa
host = 127.0.0.1
port = <DB_PORT>
migration = PASS / FAIL

server:
host = 127.0.0.1
port = <SERVER_PORT>
pid = <PID>
status = RUNNING / FAILED

fixture:
PROJECT_ID = <exact>
ACCEPTED_RUN_ID = <exact>
NO_ATTEMPT_RUN_ID = <exact>
NONTERMINAL_RUN_ID = <exact if identified>
ADMITTED_DENIED_COMBINED_RUN_ID = <exact or NOT_AVAILABLE_IN_ACCEPTED_SEED>

sanity:
command-center shell = 200
queue = 200
accepted detail summary/transitions/execution = 200/200/200
no-attempt detail summary/transitions/execution = 200/200/200

Human QA URLs:
<exact URLs>

source changes:
none

Git actions:
none

cleanup:
NOT_PERFORMED
reason:
Human P2-1C QA will run next
```

## judgment boundary

```text
QA_RUNTIME_READY
!=
Human QA PASS
!=
P2-1C ACCEPTED
```

Do not perform the Human QA itself.
