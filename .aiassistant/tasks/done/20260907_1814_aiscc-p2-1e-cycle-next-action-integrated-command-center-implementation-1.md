# 작업지시서: P2-1E Cycle / Next Action + Integrated Command Center Implementation

## meta

- task_id: `20260907_1814_aiscc-p2-1e-cycle-next-action-integrated-command-center-implementation-1`
- created_at: `2026-09-07T18:14:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `FRONTEND_IMPLEMENTATION / INTEGRATED_QA_ENTRY`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `NOT_APPLICABLE`
- primary_semantic_owner: `P2-1E Cycle/NextAction browser presentation and P2-1 integrated UI candidate`

## 현재 상태

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

accepted HEAD:
36bed286abf4df6e8cecea2d379896c36be5d58a

accepted tree:
221ee3e4b675bb3ca871ba38557c10ffadbf96fe

P2-1A:
ACCEPTED / PERSISTED

P2-1B:
ACCEPTED / PERSISTED

P2-1C:
HUMAN_PROVIDED / ACCEPTED / PERSISTED

P2-1D:
HUMAN_PROVIDED / ACCEPTED / PERSISTED

P2-1E:
ENTRY_AUTHORIZED / NOT_STARTED

P2-1:
ACTIVE / NOT_CLOSED

P2-2:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

Accepted P2-1D product/test identity:

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

Expected starting workspace from terminal P2-1D evidence:

```text
index:
empty

Git-visible worktree:
clean

runtime:
stopped / absent

Python cache residue:
0
```

이 identity 또는 workspace expectation과 실제 repository가 충돌하면 mutation 전에 STOP한다.

## authoritative predecessor

반드시 다음 exact canonical artifacts를 읽는다.

```text
.aiassistant/records/aiscc/cycles/20260907_1805_aiscc-p2-1d-persistence-final-acceptance-p2-1e-entry-authorization-1.cycle.md

.aiassistant/reports/aiscc/20260907_1805_aiscc-browser-command-center-p2-1d-completion-p2-1e-entry-handoff-1.md
```

P2-1E는 P2-1D를 재개하는 Task가 아니다.

P2-1D accepted bytes, accepted Human QA, accepted runtime evidence를 새 conflict 없이 다시 판정하거나 재수행하지 않는다.

## 이번 턴 목표

1. **mutation 전에 narrow source/contract audit를 수행**하여 P2-1E에 필요한 기존 UI route, Cycle read DTO, NextAction read DTO, navigation source, refresh/failure semantics를 exact source에서 확인한다.
2. audit가 아래 `implementation gate`를 만족할 때에만 P2-1E source를 구현한다.
3. 기존 P2-1A/B/C/D를 하나의 Command Center 흐름으로 보존하면서 다음을 추가한다.
   - runtime `AdmittedCycle` detail / provenance presentation
   - project-scoped `NextAction` presentation
   - existing Project queue / WorkRun detail과의 안전한 navigation integration
4. source/static/targeted integration proof를 제출하여 **Human integrated Browser/Visual/Usability QA 진입 후보**를 만든다.
5. P2-1E에서 처음으로 whole-UI vertical density concern을 source/runtime 관점에서 점검하되 Human usability 판정을 대신하지 않는다.

## 이번 턴 비목표

- P2-1D 재구현 또는 P2-1D Human QA 반복
- P2-1 terminal closure
- Git persistence commit
- P2-2 Synthetic Demo Repository
- P2-3 Replay corpus
- self-dogfooding cutover
- public release/deployment
- Project Source mirror sync
- mutation control 추가
- HumanResult/Judgment/transition/evidence admission mutation
- repository Markdown Cycle 파일을 runtime authority로 읽거나 index하는 기능
- 새로운 Project catalog authority
- new backend owner/API/DTO/persistence authority를 UI 편의를 위해 생성하는 것
- Node/npm/SPA/frontend framework 도입

## inherited P2-1 web boundary

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

exposure:
LOCAL_PRIVATE_ONLY

interaction posture:
read-only first
```

Human-facing visible copy는 Korean-first다.
Exact code/state/enum/identifier는 원문을 유지한다.

## accepted P2-1A read authority

다음 read authority는 이미 P2-1A에서 accepted/persisted 되었다.
P2-1E는 이를 소비하고 새 backend authority를 만들지 않는다.

```text
GET /v1/command-center/projects/{project_id}/queue
GET /v1/command-center/work-runs/{work_run_id}
GET /v1/command-center/work-runs/{work_run_id}/transitions
GET /v1/command-center/work-runs/{work_run_id}/execution
GET /v1/command-center/work-runs/{work_run_id}/evidence
GET /v1/command-center/work-runs/{work_run_id}/human-judgment
GET /v1/command-center/projects/{project_id}/outcomes
GET /v1/command-center/cycles/{cycle_id}
GET /v1/command-center/projects/{project_id}/next-action
```

Inherited read rules:

```text
explicit DTOs
no ORM direct serialization
privacy allowlist
status dimensions separate
Task trusted display metadata unavailable → REFERENCE_ONLY
runtime AdmittedCycle only
NextAction GET side-effect-free
repeatable read/read-only or fail closed
ETag / 304
safe 400/404/409/503
LOCAL_PRIVATE_ONLY
```

## 핵심 authority invariants

```text
AGENT_OUTPUT != SYSTEM_STATE
AGENT_CLAIM != ADMITTED_EVIDENCE
HUMAN_OWNED_EVIDENCE != EXECUTOR_COMPLETED

WorkflowState != ExecutionStatus
HumanGateStatus != HumanResult
HumanResult != Judgment
Judgment != TransitionDecision
Judgment != WorkflowState
EvidenceCandidate != AdmittedEvidence

runtime AdmittedCycle
!=
repository .aiassistant/records/aiscc/cycles/*.cycle.md file

NextActionSelection
!= TransitionDecision
!= TaskContract issuance
```

UI label/layout 때문에 이 경계를 collapse하지 않는다.

---

# 1. mandatory preflight — mutation 전에 수행

## 1.1 Git/workspace identity

다음을 exact 확인한다.

```text
git branch --show-current
git rev-parse HEAD
git status --short --untracked-files=all
git diff --cached --name-only
```

Pass condition:

```text
branch == main
HEAD == 36bed286abf4df6e8cecea2d379896c36be5d58a
index == empty
Git-visible worktree == clean
```

예상치 못한 source/config/migration/governance dirt가 하나라도 있으면:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

broad cleanup은 금지한다.

## 1.2 accepted UI byte identity

위 4개 accepted path의 SHA-256을 재계산한다.

모두 exact match해야 한다.

Mismatch면 source mutation 금지 후:

```text
POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

로 종료한다.

---

# 2. narrow source/contract audit — implementation gate

이 audit는 source mutation보다 먼저 완료해야 한다.

## 2.1 exact UI source inventory

직접 읽을 exact paths:

```text
src/aiscc/api/routes/command_center_ui.py
src/aiscc/command_center/web.py
tests/integration/command_center/test_web_ui.py
tests/unit/command_center/test_web_shell.py
```

확인할 것:

- current UI route set
- Project page rendering/JS entrypoint
- WorkRun detail page rendering/JS entrypoint
- existing API fetch abstraction / safe DOM helper
- endpoint-scoped ETag storage
- 304 handling
- last-successful DOM retention/failure-label behavior
- manual refresh ownership
- visible/nonterminal polling ownership
- hidden-tab stop/resume
- terminal polling stop
- current responsive breakpoints/layout classes
- Project page queue heading/focus preservation behavior

## 2.2 exact P2-1A Cycle / NextAction source authority inventory

`GET /v1/command-center/cycles/{cycle_id}`와 `GET /v1/command-center/projects/{project_id}/next-action`의 current route → DTO → query/service path를 **import/symbol chain으로만 좁게 추적**한다.

필수 확인:

### Cycle

- exact route path and handler
- exact response DTO type
- runtime source owner가 `AdmittedCycle`임을 확인할 source evidence
- privacy allowlisted fields
- cycle_id/project/task/run/judgment/transition/evidence/commit/result/next-action 관련 어떤 field가 실제 DTO에 존재하는지
- immutable/admitted semantics와 not-found/unavailable behavior
- ETag/304 behavior

### NextAction

- exact route path and handler
- exact response DTO type
- current selection/source authority field가 실제로 무엇인지
- project binding
- blocker/reason/action ref/display metadata 중 실제 DTO에 존재하는 field
- `NextActionSelection != TaskContract` 경계를 encode하는 source evidence
- ETag/304 behavior
- side-effect-free GET 보장 source evidence

금지:

- unrelated `src/**` bulk-read
- repository Markdown Cycle scan/index
- P1-8 source 전체를 report 채우기 위해 다시 읽는 것
- 없는 field를 추정해 UI contract로 고정하는 것

## 2.3 navigation source audit

P2-1A/B/C/D current DTO와 UI에서 **실제 admitted cycle_id 또는 safe Cycle ref가 어디에 노출되는지** 확인한다.

가능한 source를 exact source evidence로만 분류한다.

```text
Project outcomes DTO
WorkRun / Human-Judgment DTO
NextAction DTO
other already accepted read DTO
```

Cycle detail navigation은 current accepted DTO가 제공하는 safe ref로만 만든다.

Cycle ref가 어느 accepted DTO에도 존재하지 않거나 exact current page에서 안전하게 연결할 수 없다면 새 backend field를 추가하지 말고:

```text
BLOCKED_POLICY_GAP / COMMAND_CENTER_CONTRACT_GAP_REQUIRED
```

로 종료한다.

## 2.4 implementation path gate

Audit 결과 다음 조건이 모두 만족될 때만 implementation으로 진행한다.

```text
A. existing P2-1A Cycle endpoint is sufficient without API/DTO/persistence mutation
B. existing P2-1A NextAction endpoint is sufficient without API/DTO/persistence mutation
C. Cycle navigation source exists in already accepted read DTO/UI flow
D. implementation can be completed using ONLY the four mutation-allowlisted product/test paths below
E. no new package/dependency/build/config/migration is required
F. current P2-1B/C/D refresh/current-authority semantics can be preserved
```

하나라도 실패하면 source mutation 없이 audit artifact/report/export만 만들고 STOP한다.

---

# 3. exact mutation allowlist — audit gate PASS 후에만

Product/test mutation은 아래 exact 4 paths만 허용한다.

```text
src/aiscc/api/routes/command_center_ui.py
src/aiscc/command_center/web.py
tests/integration/command_center/test_web_ui.py
tests/unit/command_center/test_web_shell.py
```

위 4개 중 실제 변경되지 않은 path는 그대로 둔다.

다른 product/test/config/migration path가 필요하면 수정하지 말고:

```text
COMMAND_CENTER_PATH_SELECTION_REQUIRED
```

로 STOP한다.

Task lifecycle/temporary report artifact는 canonical rule에 따라 허용한다.

```text
.aiassistant/tasks/active/20260907_1814_aiscc-p2-1e-cycle-next-action-integrated-command-center-implementation-1.md
→
.aiassistant/tasks/done/20260907_1814_aiscc-p2-1e-cycle-next-action-integrated-command-center-implementation-1.md

.aiassistant/reports/target/20260907_1814_aiscc-p2-1e-cycle-next-action-integrated-command-center-implementation-1/**
```

---

# 4. P2-1E implementation contract

Audit gate가 PASS한 경우 아래 contract를 구현한다.

## 4.1 Cycle detail route

UI route:

```text
GET /command-center/cycles/{cycle_id}
```

이 route는 browser HTML shell만 제공하고 runtime data authority는 반드시 기존:

```text
GET /v1/command-center/cycles/{cycle_id}
```

를 사용한다.

직접 repository/DB query 금지.

### Cycle visible semantics

Cycle 페이지는 DTO가 실제 제공하는 범위에서 최소 다음 의미 그룹을 명확히 분리한다.

```text
Cycle identity / Project binding
Task / WorkRun provenance
Judgment / terminal outcome provenance
Transition provenance
Evidence provenance refs / summary
Commit/result provenance when available
Next Action relation when available
```

중요:

- 없는 field를 합성하지 않는다.
- raw repository `.cycle.md` body를 읽어 표시하지 않는다.
- runtime `AdmittedCycle`을 Browser Command Center markdown Cycle Record와 동일 객체라고 표현하지 않는다.
- private/raw evidence body 또는 non-allowlisted content를 새로 노출하지 않는다.
- technical identifiers는 원문 유지, 설명 label은 Korean-first.

### Cycle refresh behavior

Cycle은 admitted durable record이므로 새 independent auto-poll timer를 만들지 않는다.

필수:

```text
initial read
manual refresh
endpoint-local ETag / 304
truthful empty/not-found/unavailable handling
```

304는 last-successful presentation을 파괴하지 않는다.

refresh failure에서 previous successful DOM을 유지한다면 반드시 stale/retained 상태를 truthfully 표시한다.

## 4.2 Next Action presentation

Project page:

```text
GET /command-center/projects/{project_id}
```

에 Project-scoped Next Action 영역을 추가한다.

Data authority:

```text
GET /v1/command-center/projects/{project_id}/next-action
```

### NextAction semantics

다음을 반드시 분리한다.

```text
NextActionSelection
!= WorkflowState
!= TransitionDecision
!= Judgment
!= TaskContract issuance
```

DTO가 실제 제공하는 범위에서:

- selected action/ref
- source/selection provenance
- blocker/reason
- current applicability/status
- target refs / display metadata

를 사람이 읽을 수 있게 구성한다.

없는 title/type/phase를 repository/chat context에서 추론하여 채우지 않는다.
Trusted display metadata가 없으면 existing REFERENCE_ONLY posture를 유지한다.

### NextAction refresh integration

새 competing polling scheduler를 만들지 않는다.

가능하면 existing Project queue refresh lifecycle에 통합한다.

필수:

```text
manual Project refresh → queue + NextAction refresh
existing visible/nonterminal polling trigger → applicable NextAction refresh
hidden tab → no automatic refresh
terminal-only queue → existing auto-poll stop semantics 보존
NextAction endpoint ETag independent
304 → current DOM retained
endpoint-local failure → queue 성공 여부와 섞지 않고 NextAction만 truthful failure/stale state
```

NextAction failure 때문에 성공한 queue snapshot을 파괴하지 않는다.
Queue failure 때문에 concurrent NextAction payload를 무조건 current로 승격하지 않는다. Current-authority relation은 audit에서 확인한 existing project-page semantics에 맞춰 fail-closed로 유지한다.

## 4.3 navigation integration

이미 accepted DTO가 제공하는 cycle ref가 있을 때만 Cycle detail link를 만든다.

예상 integration source 후보:

```text
Project outcomes
WorkRun/Human-Judgment provenance
NextAction related Cycle ref
```

하지만 실제 source evidence가 우선한다.

금지:

- arbitrary cycle ID discovery endpoint 생성
- repository Cycle index 생성
- Markdown filename을 UI authority로 사용
- project-wide cycle catalog를 새로 발명

Cycle ref가 없는 곳에는 link를 합성하지 않는다.

## 4.4 existing P2-1A/B/C/D regression guard

다음을 보존한다.

### Shell / Project queue

- Korean-first visible copy
- responsive WorkRun cards
- no horizontal queue table regression
- pagination/refresh focus stability
- long identifier wrapping
- manual refresh
- 10-second visible/nonterminal polling
- hidden-tab polling stop/resume
- terminal polling stop

### WorkRun detail

- one canonical WorkRun detail page
- WorkflowState / ExecutionStatus separation
- TransitionRequest / Evaluation / guards / Decision separation
- DENIED != successful transition
- Evidence Requirement/Candidate/Admission/Admitted separation
- HumanGate / HumanResult / Judgment / Transition Effect separation
- summary current-authority failure semantics
- endpoint-local ETag handling
- retained last-successful section labels
- no mutation controls

P2-1E 때문에 P2-1D accepted Human QA를 invalidating 하는 source behavior regression이 생기면 candidate를 completed로 과장하지 않는다.

---

# 5. integrated density source/runtime concern

P2-1B에서 accepted/non-blocking으로 defer된 Human observation:

```text
approximately 1080-wide / 910-high:
page header + filters + one full WorkRun card do not all fit vertically at once
```

P2-1E에서 whole-UI 구성이 완성되므로 source/runtime candidate는 이 concern을 악화시키지 않아야 한다.

하지만 이번 Executor는 Human visual/usability owner가 아니다.

금지:

- 3-column layout을 자동 정답으로 가정
- font/spacing을 과도하게 축소하여 정보 계층 훼손
- long-value wrapping을 희생하여 억지로 한 화면에 맞춤
- Human QA 없이 "density fixed" 주장

Executor는 source/runtime evidence로 다음만 보고한다.

```text
responsive breakpoint behavior
horizontal overflow absence/presence
content wrapping behavior
major section order
whether added NextAction/Cycle navigation materially changes existing Project/WorkRun layout
```

최종 usability 판정은 Human integrated Browser QA가 소유한다.

---

# 6. absolute forbidden actions

```text
Git add / commit / push / fetch / pull / merge / rebase / cherry-pick
Git reset / restore / checkout / clean / stash used as normalization
broad cleanup
.gitignore change
new dependency/package/framework
Node/npm
DB schema/migration change
P1/P2 authority baseline mutation
P2-2 or later phase work
public deployment/release
credentialed external action
browser Human QA claim
HumanResult/Judgment/Transition mutation
Evidence admission mutation
Task issuance mutation
repository Markdown Cycle scanning/indexing
private source/evidence body exposure
```

---

# 7. 읽을 문서 — minimum authoritative context set

반드시 exact path로 읽는다.

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md
.aiassistant/rules/AISCC_DOCUMENT_LANGUAGE_POLICY.md

.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md
.aiassistant/records/command-center/JUDGMENT_RUBRIC.md

.aiassistant/records/aiscc/cycles/20260907_1805_aiscc-p2-1d-persistence-final-acceptance-p2-1e-entry-authorization-1.cycle.md
.aiassistant/reports/aiscc/20260907_1805_aiscc-browser-command-center-p2-1d-completion-p2-1e-entry-handoff-1.md
```

P2-1A read API contract의 exact implementation path는 section 2 audit에서 current import/symbol chain으로 좁게 추적한다.

Browser Project Source mirror의 stale current-state prose는 terminal accepted repository/Cycle/Handoff보다 우선하지 않는다.

---

# 8. agent instruction transport / authority

- repository-root instruction entrypoint는 thin transport bootstrap이며 policy authority가 아니다.
- Project Rules UI 또는 automatic retrieval만으로 canonical body가 전달됐다고 가정하지 않는다.
- 위 `읽을 문서` 목록은 minimum authoritative context set이다.
- unrelated rules/records/source/logs를 bulk-read하지 않는다.
- active Task, canonical rule, current source, accepted evidence가 충돌하면 mutation을 중단하고 conflict investigation으로 보고한다.
- Human-owned evidence를 executor-completed로 주장하지 않는다.

---

# 9. workflow transition expectation

```text
initial_state:
P2-1E ENTRY_AUTHORIZED / NOT_STARTED

expected_non_terminal_state_after_executor_candidate:
P2-1E IMPLEMENTATION_CANDIDATE_CREATED / HUMAN_BROWSER_QA_NOT_YET_ADMITTED

expected_terminal_candidate:
NONE in this Task

transition_authority:
SYSTEM / Browser Command Center judgment

Agent may directly establish P2-1E accepted/closed:
NO
```

Executor PASS는 P2-1E acceptance가 아니다.

---

# 10. evidence contract

## executor_required

### STATIC_SOURCE / CONTRACT_AUDIT

scope:

```text
section 1-2 exact preflight and source/contract audit
```

pass condition:

```text
accepted HEAD/bytes exact
clean workspace
Cycle/NextAction existing authority exact
navigation source exact
4-path mutation gate sufficient
no backend authority invention
```

필수 audit artifact:

```text
P2_1E_SOURCE_CONTRACT_AUDIT.md
```

Target bundle root에 둔다.

최소 포함:

- actual route/DTO/query source paths
- Cycle actual DTO fields used/not used
- NextAction actual DTO fields used/not used
- actual Cycle navigation ref source
- exact mutation path decision
- any field/authority gap
- implementation gate PASS/STOP

### STATIC_SOURCE / FRONTEND_SOURCE_TEST

Audit gate PASS + mutation 발생 시:

- changed path syntax/import/static inspection
- safe DOM construction / no unsafe raw HTML data insertion regression
- Korean-first visible copy inspection
- no mutation UI
- no new frontend dependency

### UNIT_TEST

Target:

```text
tests/unit/command_center/test_web_shell.py
```

Required changed-behavior coverage:

- Cycle page shell/route contract where applicable
- NextAction Project-page shell semantics
- Korean-first labels and exact identifiers
- no mutation controls
- existing P2-1B/C/D shell regression

### INTEGRATION_TEST

Target:

```text
tests/integration/command_center/test_web_ui.py
```

Required changed-behavior coverage:

- Cycle UI route → existing Cycle API consumption
- Project page → existing NextAction API consumption
- ETag/304 section-local behavior
- safe 404/409/503/error presentation
- navigation from accepted cycle ref source
- existing WorkRun detail/queue regressions

Use existing test harness only.

### STATIC QUALITY

Applicable existing project commands for changed paths:

```text
Ruff
mypy
py_compile or equivalent syntax compilation
git diff --check
```

Do not run unrelated full suites merely to fill a report field.

### LOCAL RUNTIME / READ API INTEGRATION

Required only if current canonical test/runtime harness can execute it without inventing a new environment contract.

Scope:

```text
existing FastAPI/Uvicorn Command Center local-private route
+
existing PostgreSQL-backed read projection fixture/harness when already defined
```

Proof target:

```text
/command-center/projects/{project_id}
→ NextAction section loads from accepted endpoint

/command-center/cycles/{cycle_id}
→ Cycle detail loads from accepted endpoint

no mutation/network/provider calls
```

If the repository's already-defined local integration harness requires a Task-owned disposable PostgreSQL instance, using that exact documented harness is authorized.

Do not invent credentials, schema procedure, Docker topology, port convention, or external service setup.

If required runtime proof cannot be executed without a new environment contract:

```text
EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

and stop after report/export.

## reuse_allowed

Accepted P2-1A/B/C/D proof may be reused only when the relevant accepted bytes/behavior are unchanged and current P2-1E modifications do not invalidate applicability.

Examples:

```text
P2-1A accepted read authority existence
P2-1B responsive queue/polling semantics
P2-1C transition/execution semantic separation
P2-1D evidence/human/judgment separation
```

Reuse must name predecessor provenance and applicability.

## human_owned

```text
channel:
HUMAN_VERIFICATION / BROWSER_RUNTIME / VISUAL / USABILITY

scope:
P2-1 integrated Browser QA after source/runtime candidate acceptance

status in this Task:
HUMAN_PENDING unless Human separately provides result
```

Human QA must cover whole integrated surface including the deferred vertical-density concern.

Executor must not claim it passed.

## not_required

```text
public release
production/test deployment
P2-2
P2-3
self-dogfooding cutover
Project Source mirror sync
provider/model call
external network
Git persistence commit
```

## forbidden

All actions in section 6 are `FORBIDDEN_NOT_RUN`.

## proof non-substitution

```text
frontend/unit/integration test != Human Browser QA
HTTP test client response != visual/usability acceptance
Cycle API response != repository Markdown Cycle authority
NextAction display != Task issuance
Executor report != Command Center acceptance
accepted predecessor proof != changed-path proof when applicability changed
```

---

# 11. conformance reporting

- applicability: `REQUIRED`
- applicable policy_or_invariant:
  - P2-1 accepted HTML-first/read-only/local-private contract
  - P2-1A read-model authority
  - P2-1B responsive/polling/focus semantics
  - P2-1C current-authority/stale semantics
  - P2-1D evidence/human/judgment non-collapse
  - Document Language Policy Korean-first
- required_actual_owner: existing P2-1 read API + UI shell; no new backend authority
- planned_vs_actual_scope: exact 4-path mutation boundary
- rollback_or_failure_semantics: fail closed before out-of-bound mutation; retained UI data never relabeled as newly current after failed authority refresh

---

# 12. project context impact

```text
architecture:
NONE expected

orchestration_contract:
NONE expected

security_sandbox:
NONE expected

public_provenance:
TASK_AND_CYCLE_ONLY

source_mirror_sync:
NOT_REQUIRED in this Task
```

Any canonical baseline update requirement is a blocker, not an implicit scope expansion.

---

# 13. accept 기준 — Executor candidate level

Executor submission candidate는 아래를 모두 만족해야 한다.

1. preflight accepted HEAD/bytes/workspace exact PASS.
2. `P2_1E_SOURCE_CONTRACT_AUDIT.md`가 exact source evidence를 제공.
3. implementation gate A-F exact PASS.
4. product/test mutation은 exact 4-path allowlist subset.
5. existing Cycle/NextAction APIs only; backend authority mutation 0.
6. Cycle runtime authority와 repository Markdown Cycle을 혼동하지 않음.
7. NextAction을 Task issuance/transition/judgment와 혼동하지 않음.
8. Korean-first visible copy.
9. P2-1B/C/D regressions 없음 according to required source/test/runtime evidence.
10. required targeted tests/static checks PASS.
11. applicable local runtime proof PASS 또는 명시적 `EVIDENCE_SCOPE_EXPANSION_REQUIRED` stop.
12. Human Browser QA는 `HUMAN_PENDING`으로 정직하게 남음.
13. Git index/commit/push/deploy 없음.
14. target export integrity PASS.

이 조건을 만족해도 상태는:

```text
ACCEPTED_CANDIDATE
!= P2-1E ACCEPTED
!= P2-1 CLOSED
```

---

# 14. hold/reject 기준

다음은 HOLD/BLOCK 후보:

```text
accepted HEAD/hash mismatch
unexpected dirty workspace
Cycle/NextAction existing contract insufficiency
Cycle safe navigation ref absent
backend/API/DTO/persistence mutation required
4-path allowlist insufficient
new frontend dependency required
proof-type substitution
Human QA false claim
current/stale semantics regression
P2-1D semantic collapse regression
unsafe data rendering/privacy regression
unrelated source broadening
required runtime evidence scope expansion
```

---

# 15. mandatory stop 조건

```text
POLICY_CONFLICT_INVESTIGATION_REQUIRED
DIRTY_WORKSPACE_MIXED
BLOCKED_POLICY_GAP
COMMAND_CENTER_CONTRACT_GAP_REQUIRED
COMMAND_CENTER_PATH_SELECTION_REQUIRED
EVIDENCE_SCOPE_EXPANSION_REQUIRED
SECURITY_BOUNDARY_BLOCKED
FORBIDDEN_ACTION_REQUIRED
```

named blocker 이후에는:

- blocker를 입증하는 최소 source evidence
- workspace inventory
- audit artifact
- Executor report/export
- 안전한 종료

만 수행한다.

---

# 16. 보고서 필수 항목

- task/work type/task path
- read canonical paths
- branch/HEAD/index/worktree before/after
- accepted 4-path preflight SHA results
- narrow source/contract audit result
- exact Cycle route/DTO/query chain
- exact NextAction route/DTO/query chain
- actual navigation ref source
- implementation gate A-F table
- exact changed product/test paths
- governance/provenance changes
- repository configuration changes
- evidence contract vs actual classification
- reused predecessor proof + applicability
- human pending/provided
- forbidden-not-run
- mandatory stop/scope expansion
- current/stale/304/failure semantics
- Korean-first conformance
- vertical-density source/runtime observation only, no Human claim
- unverified items
- rollback/revert guide
- preserved exact paths
- next-turn recommendation

---

# 17. export bundle 요구

Target:

```text
.aiassistant/reports/target/20260907_1814_aiscc-p2-1e-cycle-next-action-integrated-command-center-implementation-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
P2_1E_SOURCE_CONTRACT_AUDIT.md
```

Audit gate PASS + changed files 존재 시 project-relative paths를 보존하여 changed product/test file copy를 포함한다.

Deletion이 실제로 있을 때만:

```text
REMOVED_FILES.md
```

를 만든다.

No deletion이면 만들지 않는다.

Temporary target bundle은 Git ignore 대상이며 acceptance provenance 정본이 아니다.

---

# 18. Task lifecycle

Executor-required work/report/export가 완료되면:

```text
.aiassistant/tasks/active/20260907_1814_aiscc-p2-1e-cycle-next-action-integrated-command-center-implementation-1.md
→
.aiassistant/tasks/done/20260907_1814_aiscc-p2-1e-cycle-next-action-integrated-command-center-implementation-1.md
```

Move, not Copy.

`tasks/done`은 accepted 의미가 아니다.

---

# 19. 사람 검증 요구

이번 Executor Task에서 Human Browser QA를 실행하거나 PASS로 선언하지 않는다.

Source/runtime candidate가 Browser Command Center에서 substantive acceptance를 받은 뒤 별도의 **Human QA Gate Task**를 발행한다.

그 Human QA는 최소 다음 전체 통합 영역을 검증해야 한다.

```text
Project shell / queue
NextAction presentation
WorkRun detail
Transition / Execution
Evidence
Human / Judgment
Cycle navigation/detail
empty states
failure/recovery/current-vs-retained semantics
manual refresh
visible polling
hidden polling stop/resume
terminal polling stop
1080 / 1280 / 1440 responsive
approximately 1080-wide / 910-high whole-page vertical density
no mutation control
```

Human QA Task는 Human-owned이므로 IDE Executor short prompt를 요구하지 않는다.

---

# 20. preserved exact paths

이 Executor turn 종료 후 보존해야 하는 exact path:

```text
.aiassistant/tasks/done/20260907_1814_aiscc-p2-1e-cycle-next-action-integrated-command-center-implementation-1.md
```

Browser Command Center 판정 전까지 review를 위해 temporary target bundle을 유지한다.

Terminal Cycle/Handoff는 Browser Command Center가 이후 판정에서 생성한다.

---

# 21. 최종 응답 형식

1. result: `completed / blocked / rejected-candidate`
2. target bundle path
3. preflight HEAD/workspace/hash result
4. source/contract audit implementation gate result
5. changed files
6. removed files
7. executor evidence summary
8. human verification: `HUMAN_PENDING`
9. unverified items
10. preserved exact paths
