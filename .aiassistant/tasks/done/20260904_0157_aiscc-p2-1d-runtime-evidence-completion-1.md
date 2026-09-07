# 작업지시서: P2-1D PostgreSQL-backed runtime evidence completion

## meta

- task_id: `20260904_0157_aiscc-p2-1d-runtime-evidence-completion-1`
- created_at: `2026-09-04T01:57:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `QA_ONLY`
- work_subtype: `RUNTIME_EVIDENCE_COMPLETION`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `NOT_APPLICABLE`
- primary_semantic_owner: `P2-1D Evidence + Human/Judgment WorkRun detail runtime evidence completion`

## 현재 상태

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

current accepted HEAD:
08368eceac625c9a74b4347021ed65540cb08b3c

current accepted tree:
c7c601677eb2a4ca2fa7b594465ebd16ed8da9f4

P2-1A:
ACCEPTED / PERSISTED

P2-1B:
ACCEPTED / PERSISTED

P2-1C:
HUMAN_PROVIDED / ACCEPTED / PERSISTED

P2-1D source/static:
ACCEPTED

P2-1D runtime:
EVIDENCE_BLOCKED

P2-1D Human QA:
NOT_OPEN / HUMAN_PENDING

P2-1D persistence:
NOT_STARTED

P2-1E:
NOT_STARTED

P2-2:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

Accepted P2-1D candidate bytes that MUST remain unchanged in this Task:

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

Protected unchanged P2-1A/P2-1C authority includes:

```text
src/aiscc/api/routes/command_center_ui.py
SHA-256:
82d73e29ed5c185948ba82a5fc79083cafdb77b36b3f30760f570c295af01fd2
```

Latest Executor-reported pre-handoff dirty class:

```text
144 Git-visible entries
=
133 known Python __pycache__ / .pyc paths
+
8 governance/provenance paths
+
3 modified P2-1D product/test paths

index:
empty
```

That `144` count is predecessor evidence only. Do NOT assume it is still current.
This Task MUST establish the current exact workspace before any Docker/database/server action.

Open blocker:

```text
FULL APPLICABLE UNIT+INTEGRATION REGRESSION:
BLOCKED_REQUIRED_EVIDENCE

POSTGRESQL-BACKED NORMAL LOCAL HTTP RUNTIME:
BLOCKED_REQUIRED_EVIDENCE
```

The prior implementation Task intentionally prohibited creating the required DB/container/server environment.
The current Task exists only to authorize and collect that missing runtime evidence.

## Browser judgment / handoff identity to transport or verify

The following Browser-produced artifacts are authoritative inputs for this Task.

Canonical destination 1:

```text
.aiassistant/records/aiscc/cycles/20260904_0150_aiscc-p2-1d-source-static-partial-acceptance-runtime-evidence-expansion-required-1.cycle.md
SHA-256:
ed698f158c83d82012462d8500c66ae1bee609fa086f6b16e218a19fed4fcfe3
```

Canonical destination 2:

```text
.aiassistant/reports/aiscc/20260904_0152_aiscc-browser-command-center-p2-1d-runtime-evidence-completion-entry-handoff-1.md
SHA-256:
6127f9dcf56d5898b8e8b0b44a2c33e3cdde2f476867871c7c64a1a410931079
```

Transport rule:

1. If each canonical destination already exists, verify exact SHA-256 and do not rewrite it.
2. If either destination is absent, transport only an explicitly available Human-provided Browser artifact whose bytes match the exact SHA-256 above.
3. The local source filename may contain a download suffix such as `(1)`; filename is NOT authority. SHA-256 + intended canonical destination are authority.
4. Do not search broadly for “similar” files, do not guess an alternate artifact, and do not partially admit only one artifact if the other required artifact is unavailable.
5. If exact bytes for both required Browser artifacts cannot be established, STOP with `BLOCKED_MISSING_ARTIFACT`.
6. Transport is byte-preserving. Do not edit, normalize, re-encode, or regenerate Browser artifacts.

These two governance paths are the only predecessor Browser provenance additions authorized in this Task.

## 이번 턴 목표

1. Before runtime creation, prove current branch/HEAD/index/worktree provenance and exact accepted P2-1D candidate hashes.
2. Admit or exact-verify the two Browser provenance artifacts above.
3. Create a disposable, loopback-only PostgreSQL 17.6 local runtime using the already present Docker image and existing repository migrations.
4. Set `AISCC_DATABASE_URL` and `AISCC_TEST_DATABASE_URL` only in the Task-owned QA shell/process environment.
5. Run the full applicable unit + integration regression under PostgreSQL and establish a current PASS/FAIL result.
6. Start the normal application entrypoint with `python -m aiscc serve` on loopback and prove the P2-1D WorkRun detail/read endpoints against PostgreSQL.
7. Prove endpoint-local ETag / `If-None-Match` / `304` behavior.
8. Prove repeated GET/read polling does not mutate authoritative workflow/evidence/human/judgment state using the existing accepted observation mechanism.
9. Exercise safe unavailable/fail-closed behavior and current/stale/recovery behavior only through existing accepted runtime/test hooks. Do not change source to manufacture evidence.
10. Produce a complete evidence/report/export bundle without changing accepted product/test/migration/config bytes.
11. On a completely passing runtime result, leave only the explicitly Task-owned loopback PostgreSQL container and normal AISCC server running for the later Human Browser QA Gate, and report exact resource identity/ports/PID and shutdown commands.
12. If runtime evidence exposes a product defect, stop and return `HOLD_REWORK_REQUIRED`; do not repair it in this Task.

## 이번 턴 비목표

- P2-1D source implementation or rework
- new UI behavior
- new endpoint or backend authority
- test rewriting to make the suite pass
- migration/schema changes
- repository configuration changes
- P2-1D Git persistence
- Human Browser/Visual/Usability QA
- P2-1E
- P2-2
- deployment
- Project Source mirror refresh
- external provider/network verification

## 허용 범위

### allowed_paths — byte-preserving provenance transport / lifecycle only

```text
.aiassistant/records/aiscc/cycles/20260904_0150_aiscc-p2-1d-source-static-partial-acceptance-runtime-evidence-expansion-required-1.cycle.md

.aiassistant/reports/aiscc/20260904_0152_aiscc-browser-command-center-p2-1d-runtime-evidence-completion-entry-handoff-1.md

.aiassistant/tasks/active/20260904_0157_aiscc-p2-1d-runtime-evidence-completion-1.md

.aiassistant/tasks/done/20260904_0157_aiscc-p2-1d-runtime-evidence-completion-1.md

.aiassistant/reports/target/20260904_0157_aiscc-p2-1d-runtime-evidence-completion-1/**
```

### allowed_paths — read-only product/test/config inspection

```text
src/**
tests/**
alembic/**
alembic.ini
pyproject.toml
```

Read-only inspection outside those exact classes is allowed only when an already-read canonical file or a current command identifies a directly applicable exact path. Do not bulk-read unrelated repository content.

### allowed_actions

- `git status`, `git diff`, `git diff --check`, `git ls-files`, `git rev-parse`, `git hash-object`/SHA-256 equivalents, and other read-only Git inspection
- exact SHA-256 verification
- byte-preserving transport of the two Browser artifacts above
- repository-local `.venv` execution
- inspect whether local Docker is available
- inspect whether `postgres:17.6-alpine` already exists locally
- create one Task-owned disposable PostgreSQL container from the already-local image with `--pull=never`
- bind PostgreSQL only to loopback
- choose the first free port from `55439`, `55440`, `55441`
- set Task-local `AISCC_DATABASE_URL`, `AISCC_TEST_DATABASE_URL`, `PYTHONDONTWRITEBYTECODE=1`
- run existing Alembic migration to current head
- use existing accepted test/runtime fixture producer or existing repository-local seed path
- execute the full applicable unit + integration suite
- execute current static sanity commands when useful to correlate a runtime failure, but do not substitute them for runtime proof
- start the normal application entrypoint on loopback
- choose the first free server port from `8765`, `8766`, `8767`
- local loopback HTTP requests only
- read-only PostgreSQL observations required to demonstrate GET/no-mutation
- Task-owned runtime shutdown/removal on failure/block
- on full PASS only, leave the exact Task-owned PostgreSQL container and normal server running for the next Human Browser QA Gate
- generate temporary evidence files under the target bundle
- move this Task from `tasks/active` to `tasks/done` after executor-required work/report/export is complete, including blocked/hold outcomes

## 절대 금지

### forbidden_paths — mutation

```text
src/**
tests/**
alembic/**
alembic.ini
pyproject.toml
.gitignore
AGENTS.md
.aiassistant/rules/**
.aiassistant/records/command-center/**
.aiassistant/records/aiscc/**
.aiassistant/reports/aiscc/**
```

Exception: the two exact Browser provenance destination files explicitly listed under allowed paths may be created only by byte-preserving transport and may not be edited.

### forbidden_actions

- modify any accepted P2-1D product/test byte
- modify P2-1A/P2-1C read authority
- modify/add/delete migration
- modify repository/build/test configuration
- add a new test or weaken/skip/xfail an existing test to obtain PASS
- `git add`
- `git commit`
- `git push`
- `git reset`
- `git restore`
- `git checkout` for cleanup/reversion
- `git clean`
- `git stash`
- broad cache cleanup
- delete or normalize the predecessor 133 Python cache class merely for cleanliness
- Docker image pull
- external network access
- non-loopback bind
- credentialed external action
- browser/visual QA
- deployment
- Project Source upload/sync
- source fix after any runtime defect is found
- invent a new durable fixture/product authority just to satisfy evidence
- print credential-bearing DB URLs, secret values, tokens, or private environment values into public provenance/report

## 읽을 문서

Minimum authoritative context set:

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md

.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md
.aiassistant/records/command-center/JUDGMENT_RUBRIC.md

.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_SECURITY_SANDBOX.md

.aiassistant/records/aiscc/cycles/20260903_2218_aiscc-p2-1c-persistence-final-acceptance-p2-1d-entry-authorization-1.cycle.md
.aiassistant/reports/aiscc/20260903_2220_aiscc-browser-command-center-p2-1c-completion-p2-1d-entry-handoff-1.md

.aiassistant/records/aiscc/cycles/20260903_2255_aiscc-p2-1d-predecessor-transport-blocked-missing-artifact-1.cycle.md
.aiassistant/reports/aiscc/20260903_2255_aiscc-browser-command-center-p2-1d-transport-blocked-rework-entry-handoff-1.md

.aiassistant/tasks/done/20260903_2315_aiscc-p2-1d-evidence-human-judgment-detail-transport-corrected-implementation-retry-1.md

.aiassistant/records/aiscc/cycles/20260904_0150_aiscc-p2-1d-source-static-partial-acceptance-runtime-evidence-expansion-required-1.cycle.md
.aiassistant/reports/aiscc/20260904_0152_aiscc-browser-command-center-p2-1d-runtime-evidence-completion-entry-handoff-1.md
```

If a required exact path is missing or its identity conflicts with the Task, stop before runtime creation.

Do not bulk-read all historical Tasks/Cycles.

## agent instruction transport / authority

- repository-root instruction entrypoint is a thin transport bootstrap, not project policy authority.
- Project Rules UI or automatic retrieval does not prove that canonical rule bodies are in context.
- Read the Task and every exact must-read path directly.
- Distinguish automatically discovered instructions from explicit tool reads.
- local canonical repository > terminal persisted accepted Cycle/rule/commit > latest Browser judgment Cycle > current Handoff > Browser Project Source mirror > chat memory.
- If Task, canonical rule, current source, current test, accepted Cycle, or observed repository state conflicts, stop and report exact conflict.
- Do not infer a new accepted state from Agent prose or test completion.
- Do not claim Human-owned verification as executor-completed.

## hard preflight gate — MUST run before Docker/database/server creation

### A. repository identity

Prove and report:

```text
branch == main

HEAD ==
08368eceac625c9a74b4347021ed65540cb08b3c

index == empty
```

If any fail:

```text
STOP
result:
BLOCKED_REQUIRED_EVIDENCE or HOLD_REWORK_REQUIRED as appropriate

Docker/database/server creation:
FORBIDDEN_AFTER_MISMATCH
```

### B. accepted candidate byte identity

Verify exact SHA-256:

```text
src/aiscc/command_center/web.py
0e41ffb18256628a3c76150feeb6fc5c6b4d311d566b1e4c5b8d50987b308706

tests/integration/command_center/test_web_ui.py
2913359e913d7974d9165b0b013c7617438e1accf999af3c25bb876bd974821f

tests/unit/command_center/test_web_shell.py
29dfddb01aabfce7b5746cc762575271d2b16ad1c585d3b93e1d6ece1c575fa1

src/aiscc/api/routes/command_center_ui.py
82d73e29ed5c185948ba82a5fc79083cafdb77b36b3f30760f570c295af01fd2
```

If any mismatch:

```text
STOP
source mutation:
NO
runtime environment creation:
NO
classification:
DIRTY_WORKSPACE_MIXED / SOURCE_IDENTITY_CONFLICT
```

### C. exact Git-visible dirt classification

Re-run exact current Git status.

The predecessor `144` count is not itself an acceptance condition.

Classify every current Git-visible path into:

```text
known predecessor Python cache
known governance/provenance
three P2-1D candidate product/test paths
current Task-authorized new governance provenance
unexpected
```

Expected durable predecessor governance paths include:

```text
.aiassistant/records/aiscc/cycles/20260903_1718_aiscc-p2-1b-shell-queue-persistence-final-acceptance-1.cycle.md
.aiassistant/reports/aiscc/20260903_1720_aiscc-browser-command-center-p2-1b-completion-p2-1c-entry-handoff-1.md

.aiassistant/tasks/done/20260903_2226_aiscc-p2-1d-evidence-human-judgment-detail-implementation-1.md

.aiassistant/records/aiscc/cycles/20260903_2218_aiscc-p2-1c-persistence-final-acceptance-p2-1d-entry-authorization-1.cycle.md
.aiassistant/reports/aiscc/20260903_2220_aiscc-browser-command-center-p2-1c-completion-p2-1d-entry-handoff-1.md

.aiassistant/records/aiscc/cycles/20260903_2255_aiscc-p2-1d-predecessor-transport-blocked-missing-artifact-1.cycle.md
.aiassistant/reports/aiscc/20260903_2255_aiscc-browser-command-center-p2-1d-transport-blocked-rework-entry-handoff-1.md

.aiassistant/tasks/done/20260903_2315_aiscc-p2-1d-evidence-human-judgment-detail-transport-corrected-implementation-retry-1.md
```

Current Browser provenance expected after exact verification/transport:

```text
.aiassistant/records/aiscc/cycles/20260904_0150_aiscc-p2-1d-source-static-partial-acceptance-runtime-evidence-expansion-required-1.cycle.md
.aiassistant/reports/aiscc/20260904_0152_aiscc-browser-command-center-p2-1d-runtime-evidence-completion-entry-handoff-1.md
```

If any unexpected source/config/migration dirt exists, or if current workspace cannot be fully classified without destructive cleanup:

```text
STOP
classification:
DIRTY_WORKSPACE_MIXED

do not clean/reset/stash/restore
```

## authorized disposable PostgreSQL runtime

Proceed only after the entire hard preflight passes.

### local prerequisites

Required:

```text
repository-local .venv:
present

Docker:
locally available

image:
postgres:17.6-alpine
already present locally
```

Image verification is read-only.

If image is absent:

```text
STOP
BLOCKED_REQUIRED_EVIDENCE
reason:
LOCAL_POSTGRES_IMAGE_ABSENT

docker pull:
FORBIDDEN
```

### container identity

Preferred exact name:

```text
aiscc-p2-1d-runtime-evidence
```

If an object with this exact name already exists before this Task, do not delete, replace, or repurpose it unless the current Task can prove it is its own newly created resource in the current run. Otherwise stop and report the collision.

Use:

```text
--pull=never
postgres:17.6-alpine
```

Network exposure:

```text
loopback only
```

Port preference, first free only:

```text
127.0.0.1:55439
127.0.0.1:55440
127.0.0.1:55441
```

If all three are occupied, stop rather than selecting an arbitrary external/broad port.

Use only a disposable local database/user/password created for this Task.
Do not print the credential-bearing URL or password into the report, public Cycle, console excerpt, or export evidence.

### Task-local environment

Set only for the QA/evidence shell and processes:

```text
AISCC_DATABASE_URL=<Task-local PostgreSQL URL>
AISCC_TEST_DATABASE_URL=<Task-local PostgreSQL URL or repository-required test DB URL>
PYTHONDONTWRITEBYTECODE=1
```

Do not persist these into repository files.

### migrations

Run existing:

```text
python -m alembic upgrade head
```

Required:

```text
migration execution:
PASS

migration source mutation:
NONE
```

## required evidence execution

### 1. full applicable unit + integration regression

Run the repository's current full applicable unit + integration test command under the authorized PostgreSQL environment.

Pass condition:

```text
failed:
0

errors:
0

database prerequisite skips/failures caused by missing AISCC_TEST_DATABASE_URL:
0
```

Expected intentional/non-applicable skips may remain only if they are already part of current accepted test semantics; list count/reason.

Do not alter tests to convert a failure into a skip/pass.

If a test failure establishes a current candidate defect:

```text
STOP further acceptance evidence not needed to classify the defect
result:
HOLD_REWORK_REQUIRED

source fix:
FORBIDDEN
```

You may collect minimal directly related failure evidence and safely shut down Task-owned runtime.

### 2. normal configured application entrypoint

Start the product using the normal entrypoint:

```text
python -m aiscc serve --host 127.0.0.1 --port <port>
```

Server port preference, first free only:

```text
8765
8766
8767
```

Pass condition:

```text
normal entrypoint starts against the Task PostgreSQL database
no source/config mutation is required
loopback-only binding is confirmed
```

### 3. existing accepted fixture producer / runtime seed

Use only an existing repository-local accepted mechanism to create or identify a WorkRun that exercises the P2-1D Evidence + Human/Judgment detail.

Do NOT:
- add a new durable product seed authority
- modify migrations
- patch application source
- patch tests

Record the exact existing fixture/command/path used.

### 4. required HTTP runtime proof

Against the running normal entrypoint and PostgreSQL-backed WorkRun, prove:

```text
GET /command-center/work-runs/{work_run_id}
→ 200

GET /v1/command-center/work-runs/{work_run_id}
→ 200

GET /v1/command-center/work-runs/{work_run_id}/transitions
→ 200

GET /v1/command-center/work-runs/{work_run_id}/execution
→ 200

GET /v1/command-center/work-runs/{work_run_id}/evidence
→ 200

GET /v1/command-center/work-runs/{work_run_id}/human-judgment
→ 200
```

Capture only sanitized response evidence. Do not export secrets/private environment values.

### 5. endpoint-local ETag / 304

For the five `/v1/command-center/work-runs/{id}...` read endpoints:

1. obtain current endpoint response and its ETag when the endpoint contract supplies one;
2. repeat the same endpoint with `If-None-Match`;
3. verify `304` and no replacement body/current-state mutation;
4. demonstrate endpoint-local scope with a representative cross-endpoint check so an ETag from one endpoint is not silently treated as the identity of a different endpoint.

If an endpoint intentionally does not expose ETag under the accepted contract, identify the exact contract/test/source basis rather than inventing a requirement.

### 6. read-only / no-authoritative-mutation proof

Before a bounded sequence of repeated GETs/poll-like requests, record the existing accepted authoritative observation set.

After the same requests, prove that GET/read polling did not create or mutate authoritative workflow/evidence/human/judgment state.

Use the existing accepted observation mechanism and record exactly what was compared, for example the directly applicable event/projection counts/versions already used by repository tests or prior accepted runtime harness.

Do not invent a new product mutation API or schema merely to observe this.

Pass condition:

```text
authoritative mutation caused by GET/read polling:
NONE
```

### 7. safe unavailable / fail-closed runtime behavior

Using only existing accepted runtime behavior/hooks, prove the applicable safe unavailable/fail-closed behavior.

At minimum, a missing/non-addressable WorkRun or an accepted existing failure hook must not be projected as a valid new current result.

Do not stop PostgreSQL or mutate source merely to manufacture an artificial failure if that behavior is not already an accepted runtime hook.

If a specific stale/recovery scenario cannot be safely executed at HTTP runtime without source/environment expansion, classify that exact scenario honestly; do not substitute source tests for runtime proof.

### 8. P2-1D current/stale/recovery semantics

Where existing accepted harness/runtime hooks support it, demonstrate that:

```text
summary authority failure:
dependent results are not newly applied as current

endpoint-local failure:
last successful section remains available when applicable

recovery:
a later successful response can become current without fabricating authority
```

Browser-visible stale styling, actual document visibility polling, and responsive visual semantics remain Human-owned and are NOT executor-completed evidence.

## evidence contract

### executor_required

- channel: `SESSION_AUTHORITY`
  - scope: branch / HEAD / index / exact workspace classification
  - pass_condition: exact preflight passes before runtime creation

- channel: `TRANSPORT_IDENTITY`
  - scope: exact `0150 Cycle` + `0152 Handoff`
  - pass_condition: canonical destinations match exact SHA-256; byte-preserving transport only when needed

- channel: `STATIC_SOURCE_IDENTITY`
  - scope: accepted P2-1D candidate hashes and protected UI route hash
  - pass_condition: exact pre/post match; no source mutation

- channel: `DATABASE_RUNTIME`
  - scope: local PostgreSQL 17.6, Alembic current head, accepted fixture/runtime seed
  - pass_condition: normal DB environment is usable without repository mutation

- channel: `UNIT_TEST`
  - scope: full applicable unit suite under `AISCC_TEST_DATABASE_URL`
  - pass_condition: no failures/errors

- channel: `INTEGRATION_TEST`
  - scope: full applicable integration suite under PostgreSQL
  - pass_condition: no failures/errors

- channel: `HTTP_RUNTIME`
  - scope: normal `python -m aiscc serve`, HTML + five WorkRun read endpoints, ETag/304, read-only behavior, safe unavailable/current-stale-recovery where executable
  - pass_condition: required runtime semantics pass

- channel: `PUBLIC_PROVENANCE`
  - scope: Task/report/evidence bundle and exact preserved paths
  - pass_condition: complete, no secrets/private data, Task lifecycle correctly reported

### reuse_allowed

- channel: `STATIC_SOURCE`
  - predecessor: `20260904_0150 ... partial acceptance Cycle`
  - provenance_condition: candidate three source/test SHA-256 remain exact
  - applicability_condition: no product/test source mutation in this Task
  - use: source/static semantics remain accepted and are not re-litigated merely because runtime evidence was missing

- channel: `FRONTEND_SOURCE_TEST`
  - predecessor: focused `24 passed, 1 skipped`, Ruff/mypy/syntax/diff checks from `0150`
  - provenance_condition: exact candidate bytes unchanged
  - applicability_condition: current runtime Task does not modify source/test
  - limitation: cannot replace current PostgreSQL full regression or normal HTTP runtime

### human_owned

- channel: `BROWSER_RUNTIME / VISUAL / USABILITY QA`
  - scope:
    - EvidenceRequirement / EvidenceCandidate / AdmittedEvidence visual distinction
    - RequirementSatisfaction / set evaluation readability
    - HumanGate / HumanResult / Judgment / Transition Effect distinction
    - empty/absence states
    - stale/current failure presentation
    - recovery presentation
    - 1080 / 1280 / 1440 responsive integration
    - transition/execution detail regression
    - visible polling
    - hidden-tab stop
    - visible-tab resume
    - terminal polling stop
    - no mutation controls
  - expected_result: `HUMAN_PENDING`
  - gate: `DO_NOT_OPEN` until this runtime bundle receives substantive Browser Command Center acceptance

### not_required

- channel: `EXTERNAL_NETWORK`
  - reason: local QA only

- channel: `PROVIDER_RUNTIME`
  - reason: P2-1D read UI runtime does not require external model/provider calls

- channel: `DEPLOYMENT`
  - reason: P2-1D not accepted/persisted

- channel: `PROJECT_SOURCE_MIRROR`
  - reason: no accepted canonical product commit is created in this Task

### forbidden

- action_or_channel: `SOURCE_OR_TEST_REWORK`
  - reason: QA-only Task; defect must route to separate rework

- action_or_channel: `GIT_PERSISTENCE`
  - reason: Human Browser QA has not occurred

- action_or_channel: `HUMAN_QA_FALSE_CLAIM`
  - reason: Browser/visual evidence is Human-owned

- action_or_channel: `DOCKER_PULL_OR_EXTERNAL_NETWORK`
  - reason: runtime expansion is explicitly bounded to existing local resources

### proof_non_substitution

```text
focused source test != PostgreSQL full regression
TestClient != normal configured HTTP runtime
HTTP runtime != Human Browser/Visual QA
Agent report != Browser Command Center acceptance
runtime PASS != P2-1D persistence
HumanResult != Judgment
Judgment != TransitionDecision
Judgment != WorkflowState
```

## workflow transition expectation

```text
applicability:
PROJECT_WORKFLOW / MANUAL_COMMAND_CENTER

initial P2-1D state:
SOURCE_STATIC_ACCEPTED / RUNTIME_EVIDENCE_BLOCKED / HUMAN_QA_NOT_OPEN

successful executor candidate:
RUNTIME_EVIDENCE_COMPLETED_CANDIDATE

Browser Command Center successful disposition after substantive review:
P2-1D SOURCE_RUNTIME ACCEPTED_CANDIDATE_FOR_HUMAN_QA
Human QA HUMAN_PENDING / OPEN_NEXT

terminal P2-1D acceptance:
NOT AUTHORIZED IN THIS TASK

transition authority:
Browser Command Center / Human gate according to canonical workflow

Agent may directly mark P2-1D accepted/persisted:
No
```

## conformance reporting

- applicability: `REQUIRED`
- applicable policy_or_invariant:
  - `EvidenceCandidate != AdmittedEvidence`
  - `HumanGateStatus != HumanResult != Judgment != TransitionDecision != WorkflowState`
  - read-only UI must not mutate authoritative state
  - proof type non-substitution
  - local runtime permission bounded to Task scope
- required_actual_owner:
  - runtime evidence producer: Executor
  - evidence admission/judgment: Browser Command Center
  - Browser/visual/usability evidence: Human
- planned_vs_actual_scope:
  - report exact deviations, ports, fixture mechanism, skips, and any unavailable runtime sub-scenario
- rollback_or_failure_semantics:
  - runtime defect -> no source repair; `HOLD_REWORK_REQUIRED`
  - missing local prerequisite -> `BLOCKED_REQUIRED_EVIDENCE`
  - workspace/authority mismatch -> stop before environment creation

## project context impact

architecture:
- `NONE`

orchestration_contract:
- `NONE`

security_sandbox:
- `NONE`; current accepted local runtime boundary is exercised, not changed

public_provenance:
- `TASK_AND_CYCLE_ONLY`
- this Executor Task itself becomes durable `tasks/done` provenance after report/export completion
- Browser Cycle is created only after substantive review

## accept 기준

Executor candidate is suitable for Browser substantive runtime review only when all are true:

1. hard preflight passes;
2. exact Browser provenance is admitted/verified;
3. exact P2-1D candidate hashes remain unchanged before and after;
4. local `postgres:17.6-alpine` is used with `--pull=never` and loopback-only binding;
5. Alembic current head succeeds;
6. full applicable unit + integration regression has `0 failed / 0 errors`;
7. normal `python -m aiscc serve` starts against PostgreSQL;
8. HTML + all required WorkRun read endpoints return expected success;
9. applicable endpoint-local ETag / 304 passes;
10. repeated GET/read polling causes no authoritative mutation;
11. safe unavailable/fail-closed runtime behavior passes for the executable accepted scenario;
12. any current/stale/recovery runtime scenario claimed as executed is actual runtime evidence, not source-test substitution;
13. source/test/migration/config changes are none;
14. Git index remains empty;
15. no external network/pull/deployment/credentialed action occurred;
16. Human Browser QA remains `HUMAN_PENDING`;
17. report/export is complete and secret-safe;
18. success-only retained runtime resources are exact Task-owned resources and fully identified.

Successful Executor result wording:

```text
COMPLETED / RUNTIME_EVIDENCE_CANDIDATE
```

Do NOT say:

```text
P2-1D ACCEPTED
P2-1D PERSISTED
Human QA PASS
```

## hold / blocked 기준

### HOLD_REWORK_REQUIRED

Use when current authorized runtime proves an actual product/test semantic defect, including:

- full regression failure attributable to current candidate behavior rather than missing prerequisite;
- normal configured entrypoint cannot operate because of current candidate defect;
- required P2-1D read endpoint returns incorrect status/contract;
- ETag/304 violates accepted endpoint-local semantics;
- GET/read polling mutates authoritative state;
- fail-closed/current-stale-recovery semantics contradict the accepted source/runtime contract.

After such finding:

```text
source fix:
FORBIDDEN

additional broad investigation:
FORBIDDEN

collect minimal directly related evidence
safe shutdown Task-owned runtime
report/export
stop
```

### BLOCKED_REQUIRED_EVIDENCE

Use when proof cannot be created because of a prerequisite not authorized to repair, including:

- local Docker unavailable;
- `postgres:17.6-alpine` not present locally;
- no authorized loopback port among the fixed choices;
- required exact Browser provenance unavailable;
- required existing fixture/runtime seed mechanism genuinely absent;
- environment prerequisite remains unresolved without repository/source/config mutation.

### DIRTY_WORKSPACE_MIXED / authority conflict

Use and stop before environment creation when:

- HEAD/branch/index does not match;
- accepted source hash mismatch;
- unexpected source/config/migration dirt exists;
- exact workspace cannot be classified without destructive cleanup.

## mandatory stop 조건

- policy baseline conflict
- missing required exact Browser artifact
- branch/HEAD/index mismatch
- candidate/protected source SHA mismatch
- unexpected dirty source/config/migration
- Docker unavailable
- local PostgreSQL image absent
- all fixed loopback ports unavailable
- external network would be required
- source/test/config/migration modification would be required to continue
- a current runtime product defect is established
- credential/private data exposure risk
- any request to perform Human Browser QA inside this Task
- any request to stage/commit/push/deploy
- evidence scope would need to expand beyond this Task

After a named blocker: collect only minimal blocker evidence, final workspace/resource inventory, report/export, Task lifecycle completion, and safe shutdown of any Task-owned runtime resource. Do not continue unrelated tests/runtime.

## runtime resource final disposition

### On any BLOCKED / HOLD / FAIL

Stop the Task-owned AISCC server if started.
Remove the Task-owned PostgreSQL container if created.
Do not touch any pre-existing container/process.
Report:

```text
task-owned server:
stopped / not-started

task-owned postgres:
removed / not-created

unrelated runtime resources:
untouched
```

### On full runtime PASS

It is explicitly authorized to leave the following running for later Human Browser QA:

```text
one Task-owned PostgreSQL container:
aiscc-p2-1d-runtime-evidence

one normal AISCC server:
127.0.0.1:<8765|8766|8767>
```

Report exact:

- container name and container id prefix
- loopback DB port
- DB image identity
- server PID/process identity
- server loopback port
- WorkRun ID/route needed for Human QA, but no secret
- exact shutdown commands
- confirmation that there are no other Task-created long-lived resources

Do not claim that retained runtime itself is Human QA.

## report/export 요구

Target:

```text
.aiassistant/reports/target/20260904_0157_aiscc-p2-1d-runtime-evidence-completion-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
RUNTIME_EVIDENCE.md
```

`RUNTIME_EVIDENCE.md` must contain sanitized, concise evidence for:

- preflight identity
- PostgreSQL image/container/runtime identity
- migration result
- full unit+integration command/result
- server entrypoint result
- fixture/runtime seed mechanism
- required HTTP status results
- ETag/304 checks
- no-authoritative-mutation observation
- safe unavailable/fail-closed result
- current/stale/recovery scenarios actually executed
- final runtime resource disposition

If the two Browser provenance files were newly transported during this Task, include byte-identical copies preserving their project-relative paths in the target bundle as changed governance/provenance evidence.

No product/test source needs to be exported as a “changed file” because product/test mutation is forbidden.
If source identity evidence is needed, report path + SHA only.

`REMOVED_FILES.md`:
- create only if an authorized tracked deletion occurred;
- expected: absent.

Manifest must include:
- Task identity
- payload file count
- per-file byte count
- per-file SHA-256
- no private env/credential/token
- target path
- repository/branch/HEAD
- final index state
- final Git-visible classification summary

## 보고서 필수 항목

1. task / work type / task path
2. explicitly read canonical paths
3. automatically discovered instruction inventory vs explicit reads
4. repository branch/HEAD/index
5. exact preflight workspace classification
6. exact candidate/protected source SHA pre/post
7. Browser provenance transport/verification result
8. product source changes: `none`
9. test source changes: `none`
10. migration/config changes: `none`
11. governance/provenance changes
12. temporary runtime artifacts
13. PostgreSQL image/container/port identity without secret
14. migration result
15. full unit+integration exact command/result
16. normal server entrypoint / PID / port
17. fixture/runtime seed identity
18. HTTP endpoint results
19. ETag/304 evidence
20. no-authoritative-mutation evidence
21. safe unavailable/fail-closed evidence
22. current/stale/recovery actual execution classification
23. evidence contract actual classifications
24. Agent claim vs admitted evidence
25. Human QA: `HUMAN_PENDING / NOT_EXECUTED`
26. forbidden-not-run
27. mandatory stop/scope expansion
28. final Git status/index
29. final runtime resource disposition
30. rollback/shutdown guide
31. unverified items
32. preserved exact paths
33. next-turn recommendation

## 사람 검증 요구

This Task performs no Human Browser QA.

Required result:

```text
BROWSER_RUNTIME / VISUAL / USABILITY:
HUMAN_PENDING
```

If Executor runtime evidence is fully successful, the next Browser Command Center judgment may open a separate Human QA Gate.

## preserved artifact exact paths

Must preserve after this Task:

```text
.aiassistant/tasks/done/20260903_2226_aiscc-p2-1d-evidence-human-judgment-detail-implementation-1.md
.aiassistant/tasks/done/20260903_2315_aiscc-p2-1d-evidence-human-judgment-detail-transport-corrected-implementation-retry-1.md
.aiassistant/tasks/done/20260904_0157_aiscc-p2-1d-runtime-evidence-completion-1.md

.aiassistant/records/aiscc/cycles/20260903_1718_aiscc-p2-1b-shell-queue-persistence-final-acceptance-1.cycle.md
.aiassistant/reports/aiscc/20260903_1720_aiscc-browser-command-center-p2-1b-completion-p2-1c-entry-handoff-1.md

.aiassistant/records/aiscc/cycles/20260903_2218_aiscc-p2-1c-persistence-final-acceptance-p2-1d-entry-authorization-1.cycle.md
.aiassistant/reports/aiscc/20260903_2220_aiscc-browser-command-center-p2-1c-completion-p2-1d-entry-handoff-1.md

.aiassistant/records/aiscc/cycles/20260903_2255_aiscc-p2-1d-predecessor-transport-blocked-missing-artifact-1.cycle.md
.aiassistant/reports/aiscc/20260903_2255_aiscc-browser-command-center-p2-1d-transport-blocked-rework-entry-handoff-1.md

.aiassistant/records/aiscc/cycles/20260904_0150_aiscc-p2-1d-source-static-partial-acceptance-runtime-evidence-expansion-required-1.cycle.md
.aiassistant/reports/aiscc/20260904_0152_aiscc-browser-command-center-p2-1d-runtime-evidence-completion-entry-handoff-1.md
```

Temporary target/export content is disposable after Browser judgment unless a later Cycle explicitly preserves something from it.

On full PASS, the Task-owned local PostgreSQL container and AISCC loopback server are temporarily preserved only for the subsequent Human QA Gate; they are not Git/public provenance artifacts.

## 최종 응답 형식

1. result: `completed / blocked / hold-rework-required`
2. target bundle path
3. repository branch/HEAD/index
4. preflight workspace classification
5. Browser provenance transport result
6. product/test/migration/config changes
7. full unit+integration result
8. PostgreSQL/runtime/HTTP evidence result
9. ETag/304 and no-mutation result
10. Human verification: `HUMAN_PENDING`
11. unverified items
12. final runtime resources
13. preserved exact paths
14. next-turn recommendation

Do not paste the long report body into chat.
