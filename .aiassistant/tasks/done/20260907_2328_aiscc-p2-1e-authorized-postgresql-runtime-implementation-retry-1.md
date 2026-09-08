# 작업지시서: P2-1E authorized PostgreSQL runtime prerequisite + Cycle/NextAction integrated implementation retry

## meta

- task_id: `20260907_2328_aiscc-p2-1e-authorized-postgresql-runtime-implementation-retry-1`
- created_at: `2026-09-07T23:28:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `REWORK / FRONTEND_IMPLEMENTATION / RUNTIME_PREREQUISITE`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `Browser Command Center P2-1E runtime-enabled implementation retry`
- predecessor_task: `.aiassistant/tasks/done/20260907_2252_aiscc-p2-1e-cycle-next-action-integrated-command-center-implementation-retry-1.md`
- predecessor_cycle: `.aiassistant/records/aiscc/cycles/20260907_2320_aiscc-p2-1e-runtime-prerequisite-blocked-after-source-audit-1.cycle.md`
- predecessor_handoff: `.aiassistant/reports/aiscc/20260907_2320_aiscc-browser-command-center-p2-1e-runtime-prerequisite-blocked-retry-entry-handoff-1.md`
- accepted_p2_1d_head: `36bed286abf4df6e8cecea2d379896c36be5d58a`
- accepted_p2_1d_tree: `221ee3e4b675bb3ca871ba38557c10ffadbf96fe`
- success_ceiling: `P2-1E ACCEPTED_CANDIDATE / HUMAN_INTEGRATED_BROWSER_QA_PENDING`
- public_bounded_live: `NOT_RELEASED`

---

# 1. 현재 상태

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
HUMAN_PROVIDED / ACCEPTED / PERSISTED

P2-1E:
ENTRY_AUTHORIZED
SOURCE_CONTRACT_AUDIT:
EXECUTED_PASS / REUSE_ALLOWED_WHEN_APPLICABLE
IMPLEMENTATION:
NOT_STARTED
RUNTIME_PREREQUISITE:
AUTHORIZED_BY_THIS_TASK
HUMAN_INTEGRATED_BROWSER_QA:
NOT_ENTERED

P2-1:
ACTIVE / NOT_CLOSED

P2-2:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

P2-1D를 reopen하지 않는다.

P2-2/P2-3/P2-4를 시작하지 않는다.

이번 Task는 `2320` blocker를 해소하기 위해 **기존 repository-provided PostgreSQL integration/runtime harness의 로컬 disposable prerequisite를 명시적으로 허용**하고, 그 prerequisite가 준비된 경우 P2-1E 구현과 runtime evidence까지 한 번에 수행한다.

---

# 2. 이번 턴 목표

1. current repository/workspace를 사실 그대로 preflight하고, predecessor governance provenance와 accepted four-path source identity의 applicability를 확인한다.
2. `2252`에서 Browser Command Center가 이미 admitted한 source/contract audit Gate A-F를, source identity와 applicability가 유지되는 경우 `REUSED_ACCEPTED`로 사용한다.
3. 기존 repository runtime pattern만 사용하여 disposable local PostgreSQL prerequisite를 준비한다.
4. exact four-path mutation boundary 안에서 P2-1E를 구현한다.
5. Cycle detail / provenance presentation을 existing accepted Cycle read authority에 연결한다.
6. project NextAction presentation을 existing accepted NextAction read authority에 연결한다.
7. accepted project outcome에서 admitted Cycle로 이동할 수 있는 stable navigation을 제공한다.
8. 기존 P2-1B/C/D의 current-authority / retained-stale / failure / recovery / ETag / 304 / polling 의미를 보존한다.
9. changed-path targeted tests와 actual PostgreSQL-backed Cycle/NextAction/UI runtime proof를 실행한다.
10. implementation/runtime candidate가 유효하면 `P2-1E ACCEPTED_CANDIDATE / HUMAN_INTEGRATED_BROWSER_QA_PENDING`까지만 보고한다.

---

# 3. 이번 턴 비목표

- P2-1D 재설계/재구현
- P2-1 terminal acceptance 또는 closure
- Human Browser/Visual/Usability QA 수행 또는 PASS 주장
- P2-2 Synthetic Demo Repository
- P2-3 Replay corpus
- P2-4 Self-Dogfooding cutover
- public release/deployment
- Project Source mirror refresh
- new backend/API/DTO/persistence authority
- new persistence abstraction
- new test DB harness
- new migration
- dependency/config change
- mutation controls
- Node/npm/SPA frontend 도입
- external network/provider access
- Git persistence

---

# 4. 권위와 predecessor evidence

Authority precedence:

```text
local canonical repository
>
terminal-persisted accepted Cycle/rule/commit
>
latest Browser judgment Cycle
>
current Handoff
>
Browser Project Source mirror
>
chat memory
```

이 Task는 다음 Browser judgment를 직접 상속한다.

## 4.1 `2320` Cycle

Canonical path:

```text
.aiassistant/records/aiscc/cycles/20260907_2320_aiscc-p2-1e-runtime-prerequisite-blocked-after-source-audit-1.cycle.md
```

Human-transported exact content identity expected from Browser artifact:

```text
bytes:
16058

SHA-256:
782e804604b35d8bae364a33b4b4467166d427bc9fcae005378c83f97dd5fdaf
```

## 4.2 `2320` Handoff

Canonical path:

```text
.aiassistant/reports/aiscc/20260907_2320_aiscc-browser-command-center-p2-1e-runtime-prerequisite-blocked-retry-entry-handoff-1.md
```

Human-transported exact content identity expected from Browser artifact:

```text
bytes:
12606

SHA-256:
4c82d21d8a134679f2e14c18441e6cb664ec564fbb639104b35f1adc59cdb167
```

## 4.3 predecessor Task identity

Canonical path:

```text
.aiassistant/tasks/done/20260907_2252_aiscc-p2-1e-cycle-next-action-integrated-command-center-implementation-retry-1.md
```

Accepted Browser-reviewed Task identity:

```text
bytes:
30295

SHA-256:
fb01199f8553190fce50a59db79d38f57ef525374b48b498af1c9f17d6c4ea9f
```

If these mandatory predecessor artifacts are missing or byte-mismatched, STOP before product mutation with:

```text
BLOCKED_MISSING_ARTIFACT
```

or, when content conflicts rather than being absent:

```text
POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

Do not guess alternate filenames.

---

# 5. 읽을 문서 — minimum authoritative context set

Before implementation, read these exact canonical paths:

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md
.aiassistant/rules/AISCC_DOCUMENT_LANGUAGE_POLICY.md

.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md

.aiassistant/records/aiscc/cycles/20260907_1805_aiscc-p2-1d-persistence-final-acceptance-p2-1e-entry-authorization-1.cycle.md
.aiassistant/reports/aiscc/20260907_1805_aiscc-browser-command-center-p2-1d-completion-p2-1e-entry-handoff-1.md

.aiassistant/records/aiscc/cycles/20260907_2241_aiscc-p2-1e-preflight-blocked-known-governance-dirt-1.cycle.md
.aiassistant/reports/aiscc/20260907_2241_aiscc-browser-command-center-p2-1e-preflight-blocked-retry-entry-handoff-1.md

.aiassistant/tasks/done/20260907_2252_aiscc-p2-1e-cycle-next-action-integrated-command-center-implementation-retry-1.md

.aiassistant/records/aiscc/cycles/20260907_2320_aiscc-p2-1e-runtime-prerequisite-blocked-after-source-audit-1.cycle.md
.aiassistant/reports/aiscc/20260907_2320_aiscc-browser-command-center-p2-1e-runtime-prerequisite-blocked-retry-entry-handoff-1.md
```

Read the current implementation/test owners:

```text
src/aiscc/command_center/web.py
src/aiscc/api/routes/command_center_ui.py
tests/integration/command_center/test_web_ui.py
tests/unit/command_center/test_web_shell.py
```

Read-only runtime-harness authority:

```text
tests/integration/command_center/test_postgres_read_api.py
```

For PostgreSQL startup/migration/runtime preparation, read only the exact repository files/imported symbols needed to use the **existing** environment/schema/migration path. Record every additional exact path read in the report.

Do not bulk-read unrelated rules, records, source trees, logs, all migrations, or historical bundles.

---

# 6. agent instruction transport / authority

- repository-root instruction entrypoint는 thin transport bootstrap이며 project policy authority가 아니다.
- Project Rules UI 또는 automatic retrieval만으로 canonical rule body가 Agent context에 전달됐다고 가정하지 않는다.
- 위 must-read 목록은 minimum authoritative context set이다.
- active Task File, canonical rule, current source, accepted evidence가 충돌하면 implementation을 중단한다.
- `2252` Gate A-F는 Browser Command Center가 admitted한 predecessor STATIC_SOURCE evidence다.
- exact applicability가 유지되는 경우 전체 source/contract audit을 반복하지 않는다.
- Human-owned Browser QA를 executor-completed로 주장하지 않는다.

---

# 7. mutation 전 Git/workspace preflight

## 7.1 기본 원칙

이 Task는 `clean worktree`를 무조건 요구하지 않는다.

`2320` judgment 이후 predecessor governance provenance가 Git-visible일 수 있으며, Human이 중간 governance persistence commit을 수행했을 수도 있다.

따라서 **현재 실제 repository state에서 기대 상태를 도출**한다.

Mandatory observations:

```text
git branch --show-current
git rev-parse HEAD
git rev-parse HEAD^{tree}
git status --short
git diff --cached --name-only
```

Report:

```text
branch
HEAD
tree
index
Git-visible path count
tracked modified
untracked
product/test/config/migration
governance/provenance
runtime/cache residue
```

## 7.2 required baseline

```text
branch:
main

index:
empty
```

Accepted persisted product baseline ancestor:

```text
36bed286abf4df6e8cecea2d379896c36be5d58a
```

If current HEAD is still exactly this value, that is valid.

If current HEAD differs because Human performed a later governance-only persistence commit, do not reject solely because HEAD changed.

Instead prove:

```text
accepted four product/test bytes remain exact
AND
no unexpected product/test/config/migration change is present
AND
mandatory predecessor governance artifacts are present or committed with exact identity
```

If current HEAD/source makes the accepted Gate A-F applicability uncertain, STOP before mutation with:

```text
SOURCE_IDENTITY_CHANGED_REAUDIT_REQUIRED
```

Do not silently redo a broad audit in the same turn.

## 7.3 known governance lineage

At minimum, absent an intervening persistence commit, the lineage may contain:

```text
.aiassistant/records/aiscc/cycles/20260907_1805_aiscc-p2-1d-persistence-final-acceptance-p2-1e-entry-authorization-1.cycle.md
.aiassistant/reports/aiscc/20260907_1805_aiscc-browser-command-center-p2-1d-completion-p2-1e-entry-handoff-1.md
.aiassistant/tasks/done/20260907_1814_aiscc-p2-1e-cycle-next-action-integrated-command-center-implementation-1.md
.aiassistant/records/aiscc/cycles/20260907_2241_aiscc-p2-1e-preflight-blocked-known-governance-dirt-1.cycle.md
.aiassistant/reports/aiscc/20260907_2241_aiscc-browser-command-center-p2-1e-preflight-blocked-retry-entry-handoff-1.md
.aiassistant/tasks/done/20260907_2252_aiscc-p2-1e-cycle-next-action-integrated-command-center-implementation-retry-1.md
.aiassistant/records/aiscc/cycles/20260907_2320_aiscc-p2-1e-runtime-prerequisite-blocked-after-source-audit-1.cycle.md
.aiassistant/reports/aiscc/20260907_2320_aiscc-browser-command-center-p2-1e-runtime-prerequisite-blocked-retry-entry-handoff-1.md
```

These paths are provenance, not cleanup targets.

If they are committed, absence from `git status` is expected.

If they are untracked/modified exactly as canonical transport artifacts, classify them as known governance provenance.

If extra unknown governance dirt exists, report exact delta and STOP; do not normalize it.

## 7.4 forbidden cleanup

Never use:

```text
git clean
git restore
git checkout
git reset
git stash
```

Do not recursively delete `.aiassistant` provenance.

Do not remove predecessor artifacts for cleanliness.

Do not perform broad Python cache cleanup.

Task-created runtime residue cleanup is separately authorized in Section 15.

---

# 8. accepted four-path predecessor identity

Before runtime preparation and before mutation, verify these exact SHA-256 values:

```text
src/aiscc/command_center/web.py
0e41ffb18256628a3c76150feeb6fc5c6b4d311d566b1e4c5b8d50987b308706

src/aiscc/api/routes/command_center_ui.py
82d73e29ed5c185948ba82a5fc79083cafdb77b36b3f30760f570c295af01fd2

tests/integration/command_center/test_web_ui.py
2913359e913d7974d9165b0b013c7617438e1accf999af3c25bb876bd974821f

tests/unit/command_center/test_web_shell.py
29dfddb01aabfce7b5746cc762575271d2b16ad1c585d3b93e1d6ece1c575fa1
```

If all four match, classify:

```text
ACCEPTED_PREDECESSOR_BYTES:
EXECUTED_PASS

2252_GATE_A_F_APPLICABILITY:
MATCHED
```

Then reuse Gate A-F.

If any differs before this Task's own mutation:

```text
STOP
SOURCE_IDENTITY_CHANGED_REAUDIT_REQUIRED
```

Report exact mismatching path/hash only.

Do not clean or overwrite it.

---

# 9. predecessor source/contract audit — reuse contract

When Section 8 passes, admit the following as:

```text
REUSED_ACCEPTED
```

## Gate A

```text
Cycle existing endpoint sufficiency:
PASS
```

Authority:

```text
GET /v1/command-center/cycles/{cycle_id}
```

## Gate B

```text
NextAction existing endpoint sufficiency:
PASS
```

Authority:

```text
GET /v1/command-center/projects/{project_id}/next-action
```

## Gate C

Stable Cycle navigation source:

```text
project outcomes admitted_cycle.cycle_id / cycle_ref
```

## Gate D

Implementation mutation boundary:

```text
existing four paths are sufficient
```

## Gate E

```text
new dependency/config/migration:
NOT_REQUIRED
```

## Gate F

```text
refresh/current-authority semantics preservation:
FEASIBLE / PASS
```

Do not reopen new backend/API/DTO/persistence authority unless the preflight/source identity invalidates this admitted evidence.

---

# 10. P2-1E product implementation contract

## 10.1 web substrate

Preserve:

```text
Python / FastAPI / Uvicorn
same-process HTML-first
plain CSS
minimal progressive JavaScript
no Node/npm frontend framework

UI namespace:
/command-center

read API namespace:
/v1/command-center

runtime mode:
LOCAL_PRIVATE_ONLY

interaction:
read-only first
```

Do not add mutation controls.

## 10.2 exact allowed mutation paths

Only these product/test paths may change:

```text
src/aiscc/command_center/web.py
src/aiscc/api/routes/command_center_ui.py
tests/integration/command_center/test_web_ui.py
tests/unit/command_center/test_web_shell.py
```

Normal Task lifecycle may additionally move:

```text
.aiassistant/tasks/active/20260907_2328_aiscc-p2-1e-authorized-postgresql-runtime-implementation-retry-1.md
→
.aiassistant/tasks/done/20260907_2328_aiscc-p2-1e-authorized-postgresql-runtime-implementation-retry-1.md
```

Temporary ignored export/runtime artifacts are allowed only under their canonical temporary locations.

Any required mutation outside the four product/test paths:

```text
STOP
EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

unless it is only the normal Task lifecycle/export action above.

## 10.3 Cycle detail / provenance

Implement a human-readable Cycle presentation consuming only:

```text
GET /v1/command-center/cycles/{cycle_id}
```

Requirements:

- existing P2-1A explicit DTO/read projection is the data authority;
- do not serialize ORM/persistence objects directly;
- do not expose unrestricted raw report/persistence content;
- do not fabricate absent DTO fields;
- `CycleData.current_memory` must be labeled/treated as **current project memory context**, not the historical Cycle result itself;
- provenance/task/judgment/result references must remain semantically distinct when the DTO exposes them;
- technical identifiers may remain original;
- visible human-facing copy is Korean-first;
- safe DOM only;
- no mutation controls.

## 10.4 accepted outcome → Cycle navigation

Use the admitted stable source:

```text
project outcomes admitted_cycle.cycle_id / cycle_ref
```

Requirements:

- accepted/outcome presentation may expose a visible navigation affordance only when a stable admitted Cycle ref exists;
- navigation must not infer a Cycle id from unrelated text;
- missing Cycle ref must remain truthful absence, not a fabricated link;
- link/navigation is read-only;
- navigation must resolve through the existing UI owner and existing Cycle read authority;
- do not invent a second Cycle backend authority.

## 10.5 project NextAction presentation

Consume only:

```text
GET /v1/command-center/projects/{project_id}/next-action
```

Requirements:

- `NextActionData` projection is display data;
- projection != selection execution;
- projection != task issuance candidate;
- rendering NextAction must not create, select, mutate, or issue a next action;
- unavailable/absent fields stay absent;
- no hidden mutation request;
- Korean-first human copy;
- technical state/result identifiers remain exact where applicable;
- distinguish empty/none from fetch failure.

## 10.6 current-authority / retained / failure / recovery

Preserve the accepted P2-1C/P2-1D invariant:

```text
failed read
!= new current snapshot
```

```text
retained last-successful detail
!= authoritative current data
```

```text
304 / no change
!= fabricated update
```

For P2-1E reads:

- each endpoint keeps endpoint-local ETag / has-data semantics where the current web model uses them;
- a failed Cycle or NextAction read must not overwrite last-successful content as newly current;
- retained data, when displayed, must be labeled truthfully as retained/stale/refresh-failed;
- never label retained data as `최신`;
- 304 preserves existing valid DOM/data and does not fabricate a transition/update;
- later successful recovery may restore current labels;
- one endpoint failure must not invalidate independent successful sibling sections unless current-authority dependency actually requires it;
- do not regress existing WorkRun summary-dependent current-authority gating.

## 10.7 polling / visibility / terminal semantics

Existing accepted behavior:

```text
manual refresh:
available

automatic:
10-second visible/nonterminal polling

hidden tab:
polling stopped

visible resume:
polling resumes

terminal WorkRun:
automatic polling stopped

ETag:
endpoint-local

304:
preserve last-successful DOM
```

P2-1E integration must not create a second timer that violates these semantics.

Do not make Cycle/NextAction integration cause hidden-tab polling, terminal polling, or duplicate requests contrary to current accepted behavior.

If Cycle detail is not logically subject to WorkRun polling, do not invent polling merely for symmetry.

## 10.8 semantic separation regression guard

Must remain true:

```text
WorkflowState != ExecutionStatus

EvidenceRequirement != EvidenceCandidate
EvidenceCandidate != AdmittedEvidence
AdmittedEvidence != automatic requirement satisfaction

HumanGateStatus != HumanResult
HumanResult != Judgment
Judgment != TransitionDecision
Judgment != WorkflowState

Agent claim != AdmittedEvidence
EXECUTOR_COMPLETED != WorkRun ACCEPTED

NextAction projection != NextAction selection
NextAction projection != Task issuance
Cycle presentation != unrestricted raw persistence
```

## 10.9 security / UI guard

Preserve:

```text
LOCAL_PRIVATE_ONLY
read-only
safe DOM
CSP/security headers
no mutation controls
```

Do not introduce:

```text
innerHTML
eval
new Function
credential display
secret-bearing URL display
external script/CDN
external fetch
```

unless the current accepted source already uses a safe equivalent and the Task-listed security baseline explicitly permits it. No new external dependency is authorized.

---

# 11. explicitly authorized local PostgreSQL runtime prerequisite

This section resolves the exact `2320` blocker.

## 11.1 authorization boundary

Allowed:

1. use the **existing repository-provided PostgreSQL integration harness**;
2. use the **existing schema/migration initialization path**;
3. prepare/use **one disposable local PostgreSQL database**;
4. set/pass `AISCC_TEST_DATABASE_URL` and `AISCC_DATABASE_URL` only in the local Task execution/runtime environment;
5. use local loopback networking only;
6. use repository-local `.venv`;
7. use existing local Docker and an already-present compatible PostgreSQL image;
8. clean up only Task-created runtime/container/database residue.

Forbidden:

- new DB abstraction;
- new test harness outside allowed test mutation;
- new migration;
- dependency/config changes merely to make runtime work;
- `.env`/credential file persistence;
- credential value in report/export;
- Docker registry pull;
- external network;
- external provider;
- remote DB;
- production/test shared infrastructure.

## 11.2 preferred established runtime pattern

Reuse the already accepted local AISCC pattern:

```text
repository-local .venv

Docker image:
postgres:17.6-alpine

Docker pull policy:
--pull=never

container name:
aiscc-p2-1e-runtime-evidence

PostgreSQL bind:
127.0.0.1:55439
fallback:
127.0.0.1:55440
then:
127.0.0.1:55441

normal AISCC server:
python -m aiscc serve --host 127.0.0.1 --port 8765

server port fallback:
8766
then:
8767
```

Before creating anything:

- check whether the required local image already exists;
- check whether preferred container/ports are already occupied;
- do not remove or alter unrelated existing containers/processes.

If `postgres:17.6-alpine` is absent locally:

```text
STOP
BLOCKED_REQUIRED_EVIDENCE

exact prerequisite:
local postgres:17.6-alpine image absent
```

Do not pull.

If Docker/local runtime is unavailable:

```text
STOP
BLOCKED_REQUIRED_EVIDENCE
```

Report the exact prerequisite.

## 11.3 database lifecycle

Use a Task-owned disposable database only.

Prefer ephemeral/tmpfs storage when the established local pattern supports it.

Use the existing migration path:

```text
python -m alembic upgrade head
```

Do not modify migration files.

Use current migration head as produced by the repository; do not hard-code or rewrite it merely to match historical evidence.

Set only in the Task shell/process environment:

```text
AISCC_DATABASE_URL
AISCC_TEST_DATABASE_URL
PYTHONDONTWRITEBYTECODE=1
```

Do not print credential-bearing URL values.

Report only:

```text
variable present/absent
database host class:
loopback

database:
Task-owned disposable

PostgreSQL version
image identity when inspectable
container identity
loopback port
migration head
```

## 11.4 pre-existing Human runtime

If a Human has already prepared an equivalent local disposable PostgreSQL environment:

- verify it is local/private/disposable and compatible;
- verify required variables can be passed to the exact processes;
- do not rebuild merely for ritual;
- do not delete it at cleanup unless this Task created/owns it.

---

# 12. implementation workflow

After Sections 7-11 readiness passes:

```text
REUSED_ACCEPTED Gate A-F
→ implement exact four paths
→ static/source validation
→ targeted unit/integration
→ prepare/verify PostgreSQL runtime
→ migrate existing schema
→ seed via existing accepted fixture producers
→ start normal loopback AISCC entrypoint
→ prove Cycle/NextAction/UI success + ETag/304 + read-only
→ prove directly affected safe failure/recovery using existing non-destructive hooks
→ final workspace/runtime inventory
→ report/export
→ Task lifecycle done
```

Do not mutate product source before preflight and runtime-prerequisite feasibility are both established.

If runtime prerequisite cannot be established inside Section 11, STOP **before product mutation**. This avoids creating another unverifiable candidate.

---

# 13. evidence contract

## 13.1 executor_required

### A. workspace / provenance preflight

channel:

```text
STATIC_SOURCE / GIT_WORKSPACE
```

scope:

- branch/HEAD/tree/index;
- current Git-visible inventory;
- mandatory predecessor artifact identity;
- accepted four-path hashes;
- unexpected product/test/config/migration dirt = 0.

pass condition:

```text
preflight is internally consistent
AND
accepted four-path applicability is exact
AND
no unknown conflicting dirt
```

### B. reused source/contract audit applicability

channel:

```text
STATIC_SOURCE
```

scope:

```text
2252 Gate A-F applicability
```

pass condition:

```text
four-path predecessor identity exact
AND
no conflicting source authority
```

classification:

```text
REUSED_ACCEPTED
```

Do not claim it as newly executed audit.

### C. source/static implementation proof

channel:

```text
STATIC_SOURCE / FRONTEND_SOURCE_TEST
```

scope:

- four changed paths only;
- safe DOM;
- read-only;
- Korean-first;
- no fabricated DTO fields;
- Cycle/NextAction semantic separation;
- stale/current/304 semantics;
- no new mutation authority.

pass condition:

```text
all changed-path static assertions pass
```

### D. targeted unit tests

channel:

```text
UNIT_TEST
```

minimum command scope:

```text
tests/unit/command_center/test_web_shell.py
```

pass condition:

```text
0 failures
```

### E. targeted PostgreSQL-backed integration tests

channel:

```text
INTEGRATION_TEST / DATABASE_RUNTIME
```

minimum command scope:

```text
tests/integration/command_center/test_web_ui.py
```

Environment:

```text
authorized disposable local PostgreSQL
AISCC_TEST_DATABASE_URL present to process
```

pass condition:

```text
0 failures
```

Do not substitute a no-DB skip for PASS.

### F. normal configured PostgreSQL-backed HTTP runtime

channel:

```text
HTTP_RUNTIME / DATABASE_RUNTIME
```

Use:

```text
python -m aiscc serve --host 127.0.0.1 --port <authorized-loopback-port>
```

Use existing accepted fixture producers, including the existing PostgreSQL read-API seed path where applicable.

At minimum prove with actual seeded IDs:

```text
GET /command-center
→ 200

GET /command-center/projects/{project_id}
→ 200

Cycle UI route implemented by current UI owner
→ 200

GET /v1/command-center/projects/{project_id}/outcomes
→ 200

GET /v1/command-center/cycles/{cycle_id}
→ 200

GET /v1/command-center/projects/{project_id}/next-action
→ 200
```

Also verify that accepted outcome data carries/uses the admitted Cycle ref for UI navigation when fixture data provides it.

### G. ETag / 304 proof

channel:

```text
HTTP_RUNTIME
```

For directly affected API endpoints:

```text
Cycle endpoint:
ETag present when applicable
own If-None-Match → 304 / no fabricated payload

NextAction endpoint:
ETag present when applicable
own If-None-Match → 304 / no fabricated payload
```

If endpoint-specific accepted semantics differ in current P2-1A source, follow that exact source contract and report it rather than inventing headers.

### H. read-only / no-authoritative-mutation

channel:

```text
HTTP_RUNTIME / DATABASE_RUNTIME
```

Use the existing accepted observation mechanism.

Pass condition:

```text
Cycle/NextAction/UI reads
→ no authoritative state mutation observed
→ no next-action creation/selection/issuance side effect
```

### I. directly affected failure/recovery

channel:

```text
HTTP_RUNTIME / INTEGRATION_TEST
```

Requirements:

- use existing non-destructive repository test/runtime hooks;
- do not stop shared DB or corrupt durable data merely to manufacture a failure;
- prove at least one safe failure response for Cycle/NextAction applicable runtime path;
- prove a subsequent successful read/recovery;
- prove failed read is not treated as a new current snapshot in the affected UI state model;
- prove 304/no-change does not fabricate an update.

If API/runtime safe failure can be proven but Browser DOM visual stale/recovery behavior is Human-owned, report:

```text
API/runtime failure/recovery:
EXECUTED_PASS

Browser visual stale/recovery:
HUMAN_PENDING
```

Do not substitute the API proof for Human browser observation.

## 13.2 reuse_allowed

Allowed predecessor evidence:

```text
P2-1A/B/C/D accepted persisted semantics
2252 Gate A-F STATIC_SOURCE audit
```

Only when:

```text
source identity/applicability remains exact
AND
current Task did not modify the predecessor behavior being reused
```

Reused evidence does not prove changed P2-1E lines.

## 13.3 human_owned

channel:

```text
BROWSER_RUNTIME / VISUAL / USABILITY
```

scope after candidate review only:

```text
Cycle navigation/detail
Next Action presentation
current-authority/error/recovery behavior
existing Transition/Execution regression
existing Evidence/Human/Judgment regression
responsive 1080 / 1280 / 1440
approximately 1080 × 910 deferred density observation
```

Current Task result:

```text
HUMAN_PENDING
```

Executor must not claim PASS.

## 13.4 not_required

```text
full unrelated suite:
NOT_REQUIRED by this Task

public release:
NOT_REQUIRED

deployment:
NOT_REQUIRED

P2-2:
NOT_REQUIRED / FORBIDDEN

Project Source sync:
NOT_REQUIRED_AT_THIS_CHECKPOINT

new migration:
NOT_REQUIRED

new backend/API/DTO/persistence:
NOT_REQUIRED
```

Do not run a broad suite merely to fill a report field.

## 13.5 forbidden

```text
Git add
Git commit
Git push
deployment
public release
external network/provider
Docker image pull
remote database
browser automation claiming Human QA
new backend/API/DTO/persistence authority
new migration/dependency/config for evidence
P2-2/P2-3/P2-4
mutation controls
broad cleanup
proof-type substitution
```

---

# 14. proof non-substitution

Preserve explicitly:

```text
2252 source audit
!= current implementation proof

unit test
!= PostgreSQL runtime proof

TestClient/static artifact
!= normal configured runtime proof

HTTP API recovery
!= Human browser DOM recovery

frontend source test
!= Human Browser QA

generated checklist
!= Human verification

Executor report
!= Browser Command Center acceptance

P2-1E ACCEPTED_CANDIDATE
!= P2-1E ACCEPTED

P2-1E ACCEPTED
!= P2-1 CLOSED
```

---

# 15. runtime cleanup / retention disposition

Default after executor evidence collection:

```text
cleanup Task-owned runtime
```

Task-owned examples:

```text
aiscc-p2-1e-runtime-evidence container
Task-owned disposable database/tmpfs
Task-owned loopback AISCC server process
Task-scoped environment variables in the execution shell
```

Do not remove:

```text
pre-existing Human-owned container/database
unrelated Docker resources
unrelated process
predecessor governance provenance
unrelated cache
```

Before cleanup, record:

```text
container name/id if Task-owned
PostgreSQL version
loopback DB port
AISCC server port/PID when available
migration head
```

After cleanup, record:

```text
Task-owned container:
absent

Task-owned server:
stopped

Task-owned DB residue:
none / exact known remaining reason

AISCC_TEST_DATABASE_URL:
not persisted

AISCC_DATABASE_URL:
not persisted
```

If Browser Command Center later wants to retain the runtime for Human QA, that must be a separate explicit decision. This Executor Task defaults to cleanup after evidence/export.

---

# 16. directly affected regression guard

The P2-1E implementation must not regress accepted P2-1B/C/D behavior.

Source/tests must cover, where applicable:

```text
Project/task queue still renders
WorkRun detail route still renders

WorkflowState / ExecutionStatus remain distinct

TransitionRequest / TransitionEvaluation / guards / TransitionDecision remain distinct

EvidenceRequirement / EvidenceCandidate / AdmittedEvidence remain distinct

HumanGate / HumanResult / Judgment / Transition Effect remain distinct

manual refresh remains

10-second visible/nonterminal polling remains

hidden-tab polling stop remains

visible-tab resume remains

terminal polling stop remains

endpoint-local ETag behavior remains

304 preserves last-successful data

summary-current-authority failure does not promote dependent stale data

safe Korean-first failure copy remains truthful

safe recovery remains truthful

no mutation controls
```

Do not require Human visual proof for this section; executor source/test/runtime evidence is allowed, while actual visual/usability remains Human-owned.

---

# 17. accept 기준

Executor may report `completed` / candidate only if all of the following are true:

```text
preflight:
PASS

mandatory predecessor transport:
PASS

accepted four-path identity before mutation:
PASS

2252 Gate A-F applicability:
REUSED_ACCEPTED

authorized local PostgreSQL prerequisite:
READY

implementation mutation:
exact four paths only

Cycle presentation:
IMPLEMENTED

accepted outcome → Cycle navigation:
IMPLEMENTED

NextAction presentation:
IMPLEMENTED

read-only/no mutation:
PASS

current-authority/retained/failure/304 semantics:
PRESERVED

targeted unit:
PASS

targeted PostgreSQL integration:
PASS

normal PostgreSQL-backed HTTP runtime:
PASS

Cycle runtime:
PASS

NextAction runtime:
PASS

UI route/navigation runtime:
PASS

directly affected failure/recovery:
PASS at required executor-owned proof level

forbidden actions:
ABSENT

Human Browser QA:
HUMAN_PENDING
```

Success ceiling:

```text
P2-1E ACCEPTED_CANDIDATE
/
HUMAN_INTEGRATED_BROWSER_QA_PENDING
```

The Executor must not claim:

```text
P2-1E ACCEPTED
P2-1 CLOSED
Human Browser QA PASS
P2-2 STARTED
```

---

# 18. hold/reject 기준

Report a blocked/rework result when any of these occurs.

## source/provenance blocker

```text
mandatory predecessor artifact missing/mismatch
unexpected product/test/config/migration dirt
accepted four-path identity mismatch before Task mutation
authority conflict
```

Disposition:

```text
BLOCKED_MISSING_ARTIFACT
POLICY_CONFLICT_INVESTIGATION_REQUIRED
SOURCE_IDENTITY_CHANGED_REAUDIT_REQUIRED
```

as applicable.

## local runtime prerequisite blocker

Examples:

```text
local Docker unavailable
postgres:17.6-alpine absent locally
existing migration/runtime path cannot initialize disposable DB
required local loopback port/resource cannot be prepared within allowed boundary
```

Disposition:

```text
BLOCKED_REQUIRED_EVIDENCE
```

with the exact prerequisite.

Do not pull or broaden.

## implementation/runtime defect

If P2-1E mutation occurs and targeted tests/runtime reveal a product defect:

```text
result:
rejected-candidate / HOLD_REWORK_REQUIRED
```

Do not hide the failure.

Do not claim Human QA entry.

## scope expansion

If a required proof would need:

```text
external network
new credentials
new migration
new repository config
new persistence abstraction
new backend/API/DTO owner
mutation outside four paths
```

STOP:

```text
EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

---

# 19. mandatory stop conditions

- policy baseline conflict;
- missing required artifact;
- unknown/unrelated Git-visible product/test/config/migration dirt;
- accepted four-path source identity mismatch before mutation;
- forbidden action/tool request;
- security boundary uncertainty;
- local PostgreSQL prerequisite unavailable within Section 11;
- new backend/API/DTO/persistence authority becomes necessary;
- dependency/config/migration mutation becomes necessary;
- external network or credential becomes necessary;
- Human decision becomes necessary before further mutation;
- `EVIDENCE_SCOPE_EXPANSION_REQUIRED`.

After a named blocker:

- stop product mutation;
- gather only minimal blocker evidence;
- record workspace/runtime inventory;
- produce report/export;
- perform safe Task-owned cleanup;
- move Task to done if executor turn is complete.

---

# 20. conformance reporting

applicability:

```text
REQUIRED
```

Applicable invariants:

```text
Agent claim != AdmittedEvidence
Human-owned QA != Executor-completed
NextAction projection != selection/issuance
Cycle presentation != unrestricted persistence
failed read != new current snapshot
retained/stale != current authority
304 != fabricated update
```

Required actual owner:

```text
existing P2-1A read API
+
existing P2-1B/C/D web UI owners
```

Planned vs actual scope:

```text
exact four-path mutation
+
Task-owned local runtime only
```

Any deviation must be reported.

---

# 21. project context impact

architecture:

```text
NONE
```

orchestration_contract:

```text
NONE
```

security_sandbox:

```text
NONE
```

unless a genuine conflict is discovered, in which case STOP.

public_provenance:

```text
TASK_AND_CYCLE_ONLY
```

This Task does not itself create the Browser judgment Cycle.

source_mirror_sync:

```text
not-required
```

---

# 22. 보고서 필수 항목

`EXECUTOR_REPORT.md` must include:

1. task/work type/task path;
2. read canonical paths;
3. predecessor artifact byte/hash verification;
4. branch/HEAD/tree/index;
5. exact Git-visible before inventory;
6. known governance provenance classification;
7. accepted four-path pre-mutation hashes;
8. reused `2252` Gate A-F evidence and applicability reason;
9. runtime prerequisite readiness;
10. local PostgreSQL image/container/version/loopback binding without credential value;
11. migration head;
12. product source changes;
13. test changes;
14. governance/provenance changes;
15. repository configuration changes;
16. added/modified/removed files;
17. targeted unit result;
18. targeted PostgreSQL integration result;
19. normal HTTP runtime result;
20. actual Cycle/NextAction/UI route IDs/statuses used;
21. ETag/304 result;
22. read-only/no-authoritative-mutation observation;
23. directly affected failure/recovery result;
24. current-authority/retained semantics result;
25. Agent claims vs admitted/reused/human-pending evidence;
26. forbidden-not-run;
27. mandatory stop/scope expansion if any;
28. runtime cleanup result;
29. exact Git-visible after inventory;
30. UTF-8/Markdown/control-character validation;
31. unverified items;
32. rollback/revert guide;
33. preserved exact paths;
34. next-turn recommendation.

Do not print credentials/secrets.

---

# 23. export bundle 요구

Target:

```text
.aiassistant/reports/target/20260907_2328_aiscc-p2-1e-authorized-postgresql-runtime-implementation-retry-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
```

Include changed product/test files preserving project-relative paths.

Include runtime evidence transcript/artifact only when sanitized and needed for Browser review.

Do not export:

```text
credential values
private env
database dumps
runtime database files
Docker layer data
unrelated source
previous target bundles
cache
```

`REMOVED_FILES.md` only when a repository file was actually deleted. Runtime/container cleanup is not a repository-file deletion.

Before final response validate:

```text
UTF-8:
PASS

unexpected control characters:
0

Markdown fences:
balanced

manifest bytes/hash:
exact
```

---

# 24. Task lifecycle

Start:

```text
.aiassistant/tasks/active/20260907_2328_aiscc-p2-1e-authorized-postgresql-runtime-implementation-retry-1.md
```

When executor-required work/report/export is complete, including blocked/rejected-candidate disposition:

```text
.aiassistant/tasks/done/20260907_2328_aiscc-p2-1e-authorized-postgresql-runtime-implementation-retry-1.md
```

`done` does not mean accepted.

Do not Git-add/commit this lifecycle in this Task.

---

# 25. 사람 검증 요구

Current Task:

```text
owner:
Human

channel:
BROWSER_RUNTIME / VISUAL / USABILITY

status:
HUMAN_PENDING
```

Do not open/claim this gate inside the Executor.

If the Executor produces a valid P2-1E implementation/runtime candidate, Browser Command Center must first substantively judge the submitted bundle.

Only after Browser candidate admission may the next Human QA Gate begin.

Expected later Human QA scope:

```text
Cycle navigation/detail
Next Action presentation
current-authority/error/recovery behavior
Transition/Execution regression
Evidence/Human/Judgment regression
responsive 1080 / 1280 / 1440
approximately 1080 × 910 density observation
```

Do not pre-decide a 3-column redesign.

---

# 26. 최종 응답 형식

1. `result: completed / blocked / rejected-candidate`
2. target bundle path
3. changed files
4. removed repository files
5. runtime prerequisite/result
6. targeted tests/runtime summary
7. human verification: `HUMAN_PENDING`
8. unverified items
9. preserved exact paths
10. success ceiling / next recommendation

장문 report는 chat에 붙이지 않는다.
