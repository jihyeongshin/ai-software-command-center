# 작업지시서: AISCC P2-1D PostgreSQL Runtime Evidence Completion

## meta

- task_id: `20260907_1531_aiscc-p2-1d-postgresql-runtime-evidence-completion-1`
- created_at: `2026-09-07T15:31:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `QA_ONLY / RUNTIME_EVIDENCE_COMPLETION`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `NOT_APPLICABLE`
- primary_semantic_owner: `P2-1D Evidence + Human/Judgment detail runtime evidence completion`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- accepted/current HEAD: `08368eceac625c9a74b4347021ed65540cb08b3c`
- accepted/current tree: `c7c601677eb2a4ca2fa7b594465ebd16ed8da9f4`

## 현재 상태

```text
P0:
CLOSED

P1:
ACCEPTED / CLOSED

P2:
STARTED / P2-1 ACTIVE

P2-1A:
ACCEPTED / PERSISTED

P2-1B:
ACCEPTED / PERSISTED

P2-1C:
HUMAN_PROVIDED / ACCEPTED / PERSISTED

P2-1D:
IMPLEMENTATION_CANDIDATE_CREATED
SOURCE_STATIC_ACCEPTED
RUNTIME_EVIDENCE_BLOCKED
HUMAN_BROWSER_QA_NOT_OPEN
NOT_PERSISTED

P2-1E:
NOT_STARTED

P2-2:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

Current P2-1D candidate bytes:

```text
src/aiscc/command_center/web.py
SHA-256:
0e41ffb18256628a3c76150feeb6fc5c6b4d311d566b1e4c5b8d50987b308706

tests/integration/command_center/test_web_ui.py
SHA-256:
2913359e913d7974d9165b0b013c7617438e1accf999af3c25bb876bd974821f

tests/unit/command_center/test_web_shell.py
SHA-256:
29dfddb01aabfce7b5746cc762575271d2b16ad1c585d3b93e1d6ece1c575fa1
```

Current Browser judgment:

```text
P2-1D SOURCE_STATIC:
ACCEPTED

P2-1D RUNTIME:
NOT_ACCEPTED / BLOCKED_REQUIRED_EVIDENCE

P2-1D HUMAN QA:
NOT_OPEN / HUMAN_PENDING
```

The 23 failures in the predecessor full run were all reported as:

```text
KeyError:
AISCC_TEST_DATABASE_URL
```

Those failures did not establish a source defect, but they also are not accepted as PASS.

## authority / predecessor transport precondition

Before runtime work, transport the two new Browser-governance artifacts from the Human's Downloads directory into their exact canonical repository destinations.

Expected Downloads source paths:

```text
C:\Users\oracl\Downloads\20260904_0150_aiscc-p2-1d-source-static-partial-acceptance-runtime-evidence-expansion-required-1.cycle.md

C:\Users\oracl\Downloads\20260904_0152_aiscc-browser-command-center-p2-1d-runtime-evidence-completion-entry-handoff-1.md
```

Expected source identities:

```text
20260904_0150_aiscc-p2-1d-source-static-partial-acceptance-runtime-evidence-expansion-required-1.cycle.md
bytes:
18388
SHA-256:
ed698f158c83d82012462d8500c66ae1bee609fa086f6b16e218a19fed4fcfe3

20260904_0152_aiscc-browser-command-center-p2-1d-runtime-evidence-completion-entry-handoff-1.md
bytes:
16375
SHA-256:
6127f9dcf56d5898b8e8b0b44a2c33e3cdde2f476867871c7c64a1a410931079
```

Exact canonical destinations:

```text
.aiassistant/records/aiscc/cycles/20260904_0150_aiscc-p2-1d-source-static-partial-acceptance-runtime-evidence-expansion-required-1.cycle.md

.aiassistant/reports/aiscc/20260904_0152_aiscc-browser-command-center-p2-1d-runtime-evidence-completion-entry-handoff-1.md
```

Transport rules:

1. Verify both exact Downloads paths exist before copying anything.
2. Verify byte count and SHA-256 of both source files before copying anything.
3. If either source path is absent or hash/byte identity differs, STOP as `BLOCKED_MISSING_ARTIFACT`.
4. Do not search alternate Downloads filenames.
5. Do not guess `(1)`, `(2)`, renamed, or similarly named files.
6. All-or-nothing: if both exact source identities pass, copy both to exact canonical destinations.
7. If a destination already exists, verify exact byte/hash identity. If exact, treat it as already transported; if not exact, STOP.
8. Verify destination byte/hash identity after transport.
9. This transport is governance/provenance admission only. It is not product mutation and does not authorize unrelated governance normalization.

## 이번 턴 목표

1. Exact predecessor `0150 Cycle` and `0152 Handoff` transport identity를 repository canonical path에서 확정한다.
2. Accepted P2-1D source/static candidate bytes를 변경하지 않는다.
3. Repository-local `.venv`와 already-local `postgres:17.6-alpine` image를 사용해 disposable PostgreSQL runtime을 구성한다.
4. `AISCC_DATABASE_URL`과 `AISCC_TEST_DATABASE_URL`이 설정된 상태에서 full applicable unit+integration regression을 실행한다.
5. existing Alembic migrations와 accepted fixture producer를 사용해 normal `python -m aiscc serve` entrypoint를 구동한다.
6. current WorkRun의 canonical HTML + five read endpoints에 대해 DB-backed HTTP runtime proof를 만든다.
7. endpoint-local `ETag` / `If-None-Match` / `304`를 증명한다.
8. repeated GET/read/polling이 authoritative state/event를 mutate하지 않음을 existing accepted observation mechanism으로 증명한다.
9. safe unavailable/fail-closed, current/stale/recovery behavior 중 existing accepted runtime/test hook으로 증명 가능한 범위만 증명한다.
10. 성공 시 다음 Human Browser QA가 재사용할 수 있도록 verified loopback PostgreSQL container와 AISCC server를 running 상태로 남기고 exact runtime inventory를 보고한다.

## 이번 턴 비목표

- P2-1D source/test/migration 수정
- P2-1D UI redesign
- Human Browser/Visual/Usability QA 수행 또는 통과 주장
- P2-1D Git persistence
- P2-1E 또는 P2-2 시작
- Project Source mirror refresh
- production/test external environment 접근
- external provider/API 호출
- deployment
- source defect의 즉석 수정

## 허용 범위

### allowed_paths — read

```text
AGENTS.md

.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md

.aiassistant/records/aiscc/cycles/20260903_2218_aiscc-p2-1c-persistence-final-acceptance-p2-1d-entry-authorization-1.cycle.md
.aiassistant/reports/aiscc/20260903_2220_aiscc-browser-command-center-p2-1c-completion-p2-1d-entry-handoff-1.md
.aiassistant/records/aiscc/cycles/20260903_2255_aiscc-p2-1d-predecessor-transport-blocked-missing-artifact-1.cycle.md
.aiassistant/reports/aiscc/20260903_2255_aiscc-browser-command-center-p2-1d-transport-blocked-rework-entry-handoff-1.md

.aiassistant/records/aiscc/cycles/20260904_0150_aiscc-p2-1d-source-static-partial-acceptance-runtime-evidence-expansion-required-1.cycle.md
.aiassistant/reports/aiscc/20260904_0152_aiscc-browser-command-center-p2-1d-runtime-evidence-completion-entry-handoff-1.md

src/aiscc/command_center/web.py
src/aiscc/api/routes/command_center_ui.py
src/aiscc/api/app.py

tests/unit/**
tests/integration/**
alembic/**
pyproject.toml
```

Do not bulk-read unrelated source/log/rule trees. Read only exact files needed to identify the existing accepted DB fixture/runtime helpers and the applicable full unit+integration suite.

### allowed_paths — write

Only:

```text
.aiassistant/records/aiscc/cycles/20260904_0150_aiscc-p2-1d-source-static-partial-acceptance-runtime-evidence-expansion-required-1.cycle.md
.aiassistant/reports/aiscc/20260904_0152_aiscc-browser-command-center-p2-1d-runtime-evidence-completion-entry-handoff-1.md

.aiassistant/tasks/active/20260907_1531_aiscc-p2-1d-postgresql-runtime-evidence-completion-1.md
→
.aiassistant/tasks/done/20260907_1531_aiscc-p2-1d-postgresql-runtime-evidence-completion-1.md

.aiassistant/reports/target/20260907_1531_aiscc-p2-1d-postgresql-runtime-evidence-completion-1/**
```

The two predecessor governance files may only be byte-preserving exact copies from the verified Downloads sources.

### allowed_actions

- read-only repository/source inspection within the above scope
- exact SHA-256 and byte-count verification
- exact predecessor governance transport as defined above
- `git status`, `git diff`, `git diff --check`, `git ls-files`, `git rev-parse`, and other read-only Git inspection
- repository-local `.venv` execution
- local Docker inspection
- `docker image inspect postgres:17.6-alpine`
- create/start/inspect/stop/remove only the Task-owned disposable container `aiscc-p2-1d-runtime-evidence`
- loopback-only port binding
- existing Alembic migration execution against the Task-owned local database
- existing accepted fixture producer usage
- full applicable unit+integration regression
- normal local AISCC server start using `python -m aiscc serve`
- local loopback HTTP GET/HEAD-like read verification as applicable
- read-only DB observation needed to prove no authoritative mutation
- Task target bundle generation
- leave verified Task-owned PostgreSQL container and AISCC server running on success only

## 절대 금지

### forbidden_paths — mutation

```text
src/**
tests/**
alembic/**
migrations/**
pyproject.toml
requirements*
Dockerfile*
docker-compose*
.gitignore
AGENTS.md
.aiassistant/rules/**
.aiassistant/records/command-center/**
.aiassistant/records/aiscc/**   # except the exact 0150 transport destination
.aiassistant/reports/aiscc/**  # except the exact 0152 transport destination
```

### forbidden_actions

- source/test/migration/config correction
- `git add`
- `git commit`
- `git push`
- `git restore`
- `git checkout`
- `git reset`
- `git clean`
- `git stash`
- broad workspace cleanup
- delete known Python `__pycache__` / `.pyc` dirt merely for cleanliness
- Docker image pull
- external network
- external API/provider
- credentialed external action
- browser automation / Human QA substitution
- production/test infrastructure
- deployment
- Project Source upload/sync
- guessing alternate Downloads filenames
- moving predecessor `2226` Task back to active
- changing candidate bytes to make runtime pass

## preflight — mandatory before environment mutation

Verify and report:

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

HEAD:
08368eceac625c9a74b4347021ed65540cb08b3c

index:
empty
```

Verify current candidate hashes exactly:

```text
src/aiscc/command_center/web.py
0e41ffb18256628a3c76150feeb6fc5c6b4d311d566b1e4c5b8d50987b308706

tests/integration/command_center/test_web_ui.py
2913359e913d7974d9165b0b013c7617438e1accf999af3c25bb876bd974821f

tests/unit/command_center/test_web_shell.py
29dfddb01aabfce7b5746cc762575271d2b16ad1c585d3b93e1d6ece1c575fa1
```

Run exact Git-visible inventory and classify:

```text
known Python cache/runtime residue
known governance/provenance
current P2-1D candidate source/test
unexpected product/config/migration dirt
index state
```

Do not assume the predecessor `144` count is still current.

Expected known predecessor class before the new `0150/0152` transport was:

```text
133 known Python __pycache__ / .pyc paths
+
8 governance/provenance paths
+
3 modified P2-1D product/test paths
=
144 Git-visible entries
```

After exact `0150/0152` transport, two additional governance/provenance paths may appear.

Count drift alone is not automatically a blocker. Any unexpected non-cache product/config/migration dirt, candidate hash mismatch, branch/HEAD mismatch, or non-empty index is a mandatory stop.

## agent instruction transport / authority

```text
repository-root instruction entrypoint
!= project policy authority
```

- `AGENTS.md` is a thin transport bootstrap.
- Task-listed canonical sources are the minimum authoritative context set.
- Project Rules UI/automatic retrieval alone is not sufficient proof of canonical body delivery.
- If active Task, canonical rules, current source, or accepted evidence conflict, STOP and report conflict investigation.
- Do not treat Agent output as admitted evidence.
- Do not claim Human-owned evidence as completed.
- Do not silently substitute proof channels.

## authorized disposable PostgreSQL runtime

### prerequisite check

Required:

```text
repository-local .venv
local Docker daemon
already-local image:
postgres:17.6-alpine
```

Verify image with an operation that cannot pull.

If the image is absent:

```text
BLOCKED_REQUIRED_EVIDENCE
blocker:
LOCAL_POSTGRES_IMAGE_ABSENT
```

Do not pull it.

### container identity

Preferred exact container name:

```text
aiscc-p2-1d-runtime-evidence
```

If a container with that name already exists, inspect it first.

- If it is clearly Task-owned from this exact task and is safe to reuse, report and reuse.
- Otherwise STOP; do not delete an unrelated container.

Preferred PostgreSQL host port sequence:

```text
127.0.0.1:55439
127.0.0.1:55440
127.0.0.1:55441
```

Choose the first available loopback port. Do not bind `0.0.0.0`.

Use:

```text
--pull=never
postgres:17.6-alpine
```

Use disposable local-only database credentials. Do not print credential-bearing URLs in the public report, manifest, Cycle, or chat response.

### shell environment

Set only for the QA/evidence shell:

```text
AISCC_DATABASE_URL
AISCC_TEST_DATABASE_URL
PYTHONDONTWRITEBYTECODE=1
```

Do not persist them into repository files.

### migrations

Run existing migrations only:

```text
python -m alembic upgrade head
```

Do not modify migration source.

## runtime fixture boundary

Use an existing accepted fixture producer/helper already present in repository tests/runtime support.

Requirements:

- identify its exact path/symbol in the report;
- do not create a new durable product authority;
- do not modify source or tests;
- create only the minimum local Task-owned data needed for one or more observable current WorkRuns;
- record the WorkRun ID(s) used in runtime evidence;
- fixture creation is setup, not evidence of application correctness.

If no applicable existing accepted fixture producer/helper is available without source modification:

```text
BLOCKED_REQUIRED_EVIDENCE
```

Do not invent one.

## normal product entrypoint

Start:

```text
python -m aiscc serve --host 127.0.0.1 --port <server-port>
```

Preferred server port sequence:

```text
8765
8766
8767
```

Use the first available loopback port.

This must be the normal configured product entrypoint, not TestClient, not a generated mock server, and not an alternate one-off application wrapper.

## evidence contract

### executor_required

#### channel: `GOVERNANCE_TRANSPORT`

Scope:

- exact `0150 Cycle` and `0152 Handoff` source/destination identity
- all-or-nothing byte-preserving transport

Pass:

```text
source exact path:
PASS

source bytes/SHA:
PASS

destination exact path:
PASS

destination bytes/SHA:
PASS
```

#### channel: `WORKSPACE_PRECONDITION`

Pass:

- `main`
- exact accepted HEAD
- empty index
- exact three candidate hashes
- no unexpected non-cache product/config/migration dirt

#### channel: `DATABASE_RUNTIME`

Pass:

- Task-owned `postgres:17.6-alpine` container starts with `--pull=never`
- loopback-only bind
- database health ready
- existing Alembic migrations apply successfully
- no migration/source/config modification

#### channel: `UNIT_TEST + INTEGRATION_TEST`

Run the repository's full applicable unit+integration regression under the authorized `AISCC_TEST_DATABASE_URL`.

Pass condition:

```text
0 failed
0 errors
all applicable tests pass
skips, if any, are explicitly classified and do not hide an applicable failure
```

Do not report the predecessor 23 environment failures as current PASS. Rerun them under the authorized environment.

#### channel: `HTTP_RUNTIME`

Under the normal configured PostgreSQL-backed `python -m aiscc serve` entrypoint, prove at minimum:

```text
GET /command-center/work-runs/{id}
→ 200

GET /v1/command-center/work-runs/{id}
→ 200

GET /v1/command-center/work-runs/{id}/transitions
→ 200

GET /v1/command-center/work-runs/{id}/execution
→ 200

GET /v1/command-center/work-runs/{id}/evidence
→ 200

GET /v1/command-center/work-runs/{id}/human-judgment
→ 200
```

Use current fixture-generated WorkRun IDs.

Do not use TestClient as a substitute.

#### channel: `HTTP_CACHE_RUNTIME`

For each endpoint that implements ETag semantics, verify independently:

```text
initial GET:
200 + ETag

If-None-Match with current endpoint ETag:
304

304:
no replacement body/current-state fabrication
```

Report endpoint-scoped ETag values only as non-sensitive runtime evidence where appropriate.

#### channel: `READ_ONLY_NO_MUTATION`

Using the existing accepted observation mechanism, compare authoritative projection/event identity before and after repeated reads/poll-like GET sequences.

Pass condition:

```text
read-only requests:
no authoritative WorkRun state/version mutation
no new transition event
no new execution/evidence/human/judgment authority record caused by read path
```

Exact observed tables/events/fields or existing repository helper must be named in the report.

Do not invent a new persistence observation contract.

#### channel: `SAFE_UNAVAILABLE / RECOVERY`

Use existing accepted runtime/test hooks only where available.

Required behavior to verify when safely reproducible without source mutation:

- unavailable dependency/read failure does not mint new current authority;
- last successful/current data is not silently replaced by fabricated success;
- recovery returns to current data when dependency resumes;
- sibling endpoint success is not invalidated solely by one endpoint-local failure where the accepted runtime architecture supports this.

Do not damage durable data merely to manufacture failure.

If exact browser-visible stale copy/recovery remains Human-owned, classify that portion `HUMAN_PENDING`; do not substitute source tests.

#### channel: `PUBLIC_PROVENANCE`

Pass:

- exact Task file moved active → done only after executor-required work/report/export is complete or a terminal blocker is reported;
- target bundle complete;
- no secret/private value exposed;
- exact preserved paths listed.

### reuse_allowed

```text
P2-1D SOURCE_STATIC:
REUSED_ACCEPTED
provenance:
20260904_0150 Cycle

candidate hashes:
must remain exact

focused source/static checks:
may be cited as predecessor evidence only; they do not replace current DB-backed runtime proof
```

### human_owned

```text
channel:
BROWSER_RUNTIME / VISUAL / USABILITY QA

status:
HUMAN_PENDING

gate:
DO NOT OPEN inside this Task
```

Do not execute or claim:

- Human visual distinction judgment
- responsive 1080 / 1280 / 1440 acceptance
- Human usability acceptance
- visible/hidden tab polling judgment
- terminal polling-stop visual judgment

The Browser Command Center may open that gate only after substantive acceptance of this runtime evidence bundle.

### not_required

- deployment
- external provider/model call
- external network
- production/test infrastructure
- Project Source sync
- P2-1D persistence
- P2-1E / P2-2

### forbidden

- product/test/migration/config mutation
- Git stage/commit/push
- destructive Git cleanup
- external Docker image pull
- browser QA substitution

## proof non-substitution

```text
TestClient
!= PostgreSQL-backed normal HTTP runtime

source/static test
!= Human Browser QA

successful GET
!= no-authoritative-mutation proof

fixture creation
!= runtime correctness proof

Executor Report
!= Command Center acceptance

Agent claim
!= admitted evidence

HumanResult
!= Judgment
!= TransitionDecision
!= WorkflowState
```

## success disposition

If all executor-required runtime evidence passes:

```text
executor result:
COMPLETED

recommended Command Center state:
P2-1D SOURCE/RUNTIME = ACCEPTED_CANDIDATE_FOR_HUMAN_QA

Human QA:
HUMAN_PENDING / OPEN_NEXT
```

Do not persist/commit P2-1D.

On successful completion, leave the verified Task-owned PostgreSQL container and normal AISCC server running **only if safe**.

Report exact:

```text
container name
PostgreSQL loopback host port
AISCC server loopback port
server PID/process identity
WorkRun ID(s)
database health
server health
```

Do not print credential-bearing environment values.

This runtime retention is explicitly authorized so the next Human Browser QA can reuse the exact verified environment.

## failure disposition

### actual source/runtime defect

If the authorized runtime exposes a candidate defect:

```text
STOP
result:
HOLD_REWORK_REQUIRED

source/runtime:
NOT_ACCEPTED

Human QA:
DO_NOT_OPEN
```

Do not fix the source in this QA-only Task.

Capture the narrow failing evidence and return a rework recommendation for a separate source Task.

### prerequisite unavailable

Examples:

```text
postgres:17.6-alpine image absent
Docker daemon unavailable
repository-local .venv absent
accepted fixture producer unavailable without mutation
required loopback runtime cannot be started safely
```

Result:

```text
BLOCKED_REQUIRED_EVIDENCE
```

Do not broaden scope to solve the prerequisite.

## mandatory stop conditions

- exact Downloads predecessor artifact missing or hash mismatch
- destination predecessor artifact exists with different bytes
- branch != `main`
- HEAD != `08368eceac625c9a74b4347021ed65540cb08b3c`
- index non-empty
- any of the three candidate hashes differ
- unexpected non-cache product/config/migration dirt
- local `postgres:17.6-alpine` unavailable
- Docker/network behavior would require image pull/external network
- policy/baseline conflict
- source modification would be required
- runtime reveals a real candidate defect
- Human decision required before further executor work

After a named blocker: collect only minimal blocker evidence, exact workspace/runtime inventory, report/export, safe shutdown of any partially created Task-owned runtime, then stop.

## dirty workspace / cleanup policy

Known predecessor dirty state must not be normalized.

Do not use:

```text
git clean
git restore
git checkout
git reset
git stash
```

Do not delete known Python cache paths merely for cleanliness.

Task-owned runtime cleanup:

- on success: leave verified PostgreSQL container + AISCC server running as authorized, and report exact inventory;
- on failure/blocker: stop/remove only resources created by this Task when safe, unless preserving a failing state is explicitly necessary for evidence; report residue exactly;
- never touch unrelated Docker containers/processes.

## 보고서 필수 항목

- task/work type/task path
- read canonical paths
- exact predecessor transport evidence
- branch/HEAD/index
- exact candidate hashes
- full Git-visible workspace classification before/after
- product source changes: must be `none`
- test source changes: must be `none`
- migration/config changes: must be `none`
- governance/provenance changes: exact `0150`, `0152`, and Task active→done paths
- runtime resource inventory
- PostgreSQL image identity/version
- Alembic head/result
- fixture producer exact path/symbol
- WorkRun ID(s)
- full applicable unit+integration result
- normal entrypoint command class and loopback port
- six HTTP route results
- endpoint-local ETag/304 evidence
- no-authoritative-mutation observation
- safe unavailable/recovery evidence or exact `HUMAN_PENDING`/not-applicable boundary
- evidence contract result classification
- Agent claim vs admitted evidence
- Human QA: `HUMAN_PENDING / NOT_EXECUTED`
- forbidden-not-run
- mandatory stop/scope expansion if any
- source/runtime defect status
- preserved exact paths
- unverified items
- rollback/runtime cleanup guide
- next turn recommendation

## export bundle 요구

Target:

```text
.aiassistant/reports/target/20260907_1531_aiscc-p2-1d-postgresql-runtime-evidence-completion-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
RUNTIME_ENVIRONMENT_EVIDENCE.md
FULL_REGRESSION_EVIDENCE.md
HTTP_RUNTIME_EVIDENCE.md
```

Include changed governance/provenance files preserving project-relative paths where required by the canonical export rule.

No product/test source copy is required because this Task forbids their mutation. Exact candidate hashes in `EXECUTOR_REPORT.md` are required.

Deletion exists only if this Task actually deletes a Task-owned repository artifact, which is not expected. Therefore do not create `REMOVED_FILES.md` unless a real repository deletion occurred.

## 사람 검증 요구

This Task does not open Human Browser QA.

Expected final Human status:

```text
HUMAN_PENDING
```

After the Browser Command Center substantively accepts the runtime bundle, a separate Human QA Gate may be issued.

## preserved artifacts

Must survive cleanup after this Task:

```text
.aiassistant/tasks/done/20260903_2226_aiscc-p2-1d-evidence-human-judgment-detail-implementation-1.md
.aiassistant/tasks/done/20260903_2315_aiscc-p2-1d-evidence-human-judgment-detail-transport-corrected-implementation-retry-1.md

.aiassistant/records/aiscc/cycles/20260903_1718_aiscc-p2-1b-shell-queue-persistence-final-acceptance-1.cycle.md
.aiassistant/reports/aiscc/20260903_1720_aiscc-browser-command-center-p2-1b-completion-p2-1c-entry-handoff-1.md

.aiassistant/records/aiscc/cycles/20260903_2218_aiscc-p2-1c-persistence-final-acceptance-p2-1d-entry-authorization-1.cycle.md
.aiassistant/reports/aiscc/20260903_2220_aiscc-browser-command-center-p2-1c-completion-p2-1d-entry-handoff-1.md

.aiassistant/records/aiscc/cycles/20260903_2255_aiscc-p2-1d-predecessor-transport-blocked-missing-artifact-1.cycle.md
.aiassistant/reports/aiscc/20260903_2255_aiscc-browser-command-center-p2-1d-transport-blocked-rework-entry-handoff-1.md

.aiassistant/records/aiscc/cycles/20260904_0150_aiscc-p2-1d-source-static-partial-acceptance-runtime-evidence-expansion-required-1.cycle.md
.aiassistant/reports/aiscc/20260904_0152_aiscc-browser-command-center-p2-1d-runtime-evidence-completion-entry-handoff-1.md

.aiassistant/tasks/done/20260907_1531_aiscc-p2-1d-postgresql-runtime-evidence-completion-1.md
```

The target review bundle is temporary and may be deleted after substantive Browser judgment unless a later judgment explicitly preserves it.

## 최종 응답 형식

1. `result: completed / blocked / rejected-candidate`
2. target bundle path
3. predecessor transport result
4. branch/HEAD/index + candidate identity
5. changed files
6. removed files
7. runtime environment inventory
8. full regression result
9. HTTP runtime / ETag / no-mutation result
10. Human verification
11. unverified items
12. preserved exact paths
13. next turn recommendation
