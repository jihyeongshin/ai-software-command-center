# 작업지시서: P2-1E Cycle / Next Action 통합 Command Center 구현 Retry

## meta

- task_id: `20260907_2252_aiscc-p2-1e-cycle-next-action-integrated-command-center-implementation-retry-1`
- created_at: `2026-09-07T22:52:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `REWORK / FRONTEND_IMPLEMENTATION / INTEGRATED_QA_ENTRY`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `NOT_APPLICABLE`
- primary_semantic_owner: `P2-1E Cycle / Next Action presentation and integrated Command Center read-only UI`
- predecessor_task: `.aiassistant/tasks/done/20260907_1814_aiscc-p2-1e-cycle-next-action-integrated-command-center-implementation-1.md`
- predecessor_blocked_cycle: `.aiassistant/records/aiscc/cycles/20260907_2241_aiscc-p2-1e-preflight-blocked-known-governance-dirt-1.cycle.md`
- predecessor_handoff: `.aiassistant/reports/aiscc/20260907_2241_aiscc-browser-command-center-p2-1e-preflight-blocked-retry-entry-handoff-1.md`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- accepted_HEAD: `36bed286abf4df6e8cecea2d379896c36be5d58a`
- accepted_tree: `221ee3e4b675bb3ca871ba38557c10ffadbf96fe`

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
PRE_IMPLEMENTATION_BLOCKED
RETRY_REQUIRED
IMPLEMENTATION:
NOT_STARTED
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

P2-2를 시작하지 않는다.

이번 Task는 `20260907_1814` P2-1E Task의 semantic target을 유지하되, Browser가 만든 잘못된 clean-worktree precondition만 교정한 retry다.

이전 Executor STOP은 source defect가 아니라 Browser-issued Task contradiction으로 판정되었다.

```text
root_cause:
BROWSER_TASK_PRECONDITION_CONTRADICTION

taxonomy:
COMMAND_AMBIGUOUS

executor symptom:
DIRTY_WORKSPACE_MIXED
```

따라서 이번 Task에서 workspace cleanup 자체를 목표로 삼지 않는다.

---

# 2. 이번 턴 목표

1. mutation 전에 exact Git/workspace retry preflight를 수행한다.
2. P2-1A에서 이미 accepted된 Cycle / NextAction read authority가 P2-1E UI 요구를 충족하는지 narrow source/contract audit `Gate A-F`를 수행한다.
3. `Gate A-F`가 모두 PASS인 경우에만 P2-1E 구현을 시작한다.
4. Cycle detail / provenance와 Next Action을 기존 P2-1A/B/C/D UI에 통합한다.
5. 기존 P2-1A/B/C/D semantic separation, Korean-first UI, read-only boundary, current-authority semantics를 보존한다.
6. changed-path source/static/targeted tests와 applicable local runtime/read API proof를 만든다.
7. Executor candidate를 Browser Command Center가 substantive review할 수 있는 target bundle로 export한다.
8. Human integrated Browser/Visual/Usability QA는 완료 주장하지 않고 `HUMAN_PENDING`으로 남긴다.

---

# 3. 이번 턴 비목표

- P2-1D 재구현 또는 Human QA 반복
- P2-2 Synthetic Demo Repository
- P2-3 Recorded Replay corpus
- P2-4 Self-Dogfooding cutover
- public deployment / release
- Project Source mirror sync
- mutation control 추가
- write API 추가
- 새로운 backend semantic owner 발명
- 새로운 DTO/persistence authority 도입
- Node/npm/SPA frontend 도입
- 1080px density 문제에 대한 사전 확정 해법 적용
- Git persistence commit

---

# 4. 반드시 읽을 canonical context

다음 목록은 minimum authoritative context set이다. exact path를 직접 읽고 unrelated rules/records/source/logs를 bulk-read하지 않는다.

## 4.1 command / transport rules

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md
.aiassistant/rules/AISCC_DOCUMENT_LANGUAGE_POLICY.md
.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md
.aiassistant/records/command-center/JUDGMENT_RUBRIC.md
```

## 4.2 inherited terminal / blocked authority

```text
.aiassistant/records/aiscc/cycles/20260907_1805_aiscc-p2-1d-persistence-final-acceptance-p2-1e-entry-authorization-1.cycle.md
.aiassistant/reports/aiscc/20260907_1805_aiscc-browser-command-center-p2-1d-completion-p2-1e-entry-handoff-1.md
.aiassistant/tasks/done/20260907_1814_aiscc-p2-1e-cycle-next-action-integrated-command-center-implementation-1.md
.aiassistant/records/aiscc/cycles/20260907_2241_aiscc-p2-1e-preflight-blocked-known-governance-dirt-1.cycle.md
.aiassistant/reports/aiscc/20260907_2241_aiscc-browser-command-center-p2-1e-preflight-blocked-retry-entry-handoff-1.md
```

## 4.3 source audit targets

```text
src/aiscc/command_center/web.py
tests/integration/command_center/test_web_ui.py
tests/unit/command_center/test_web_shell.py
src/aiscc/api/routes/command_center_ui.py
```

P2-1A Cycle/NextAction contract의 실제 DTO/query/import owner가 위 파일에서 exact import/symbol로 확인되는 경우에만 그 exact source를 read-only로 추가 조사할 수 있다.

그 read는 source/contract sufficiency 판단을 위한 것이며 mutation allowlist 확대를 뜻하지 않는다.

---

# 5. agent instruction transport / authority

- repository-root `AGENTS.md`는 thin transport bootstrap이며 project policy authority가 아니다.
- Project Rules UI 또는 automatic retrieval만으로 canonical body가 실제 context에 전달됐다고 가정하지 않는다.
- 위 `반드시 읽을 canonical context` 목록은 minimum authoritative context set이다.
- current Task, canonical rule, current source, accepted Cycle/Handoff가 충돌하면 implementation을 시작하지 않는다.
- stale Browser Project Source mirror prose가 terminal P2-1D Cycle/Handoff를 override하지 않는다.
- Human-owned Browser QA를 Agent가 완료했다고 주장하지 않는다.
- Agent report는 Command Center acceptance가 아니다.

---

# 6. retry preflight — exact known-governance-dirt contract

## 6.1 expected repository identity

mutation 전에 확인한다.

```text
branch:
main

HEAD:
36bed286abf4df6e8cecea2d379896c36be5d58a

expected tree:
221ee3e4b675bb3ca871ba38557c10ffadbf96fe

index:
empty
```

HEAD 또는 branch가 다르면 mutation 금지 후 STOP한다.

## 6.2 expected Git-visible dirt

clean worktree를 요구하지 않는다.

Human이 `2241 Cycle + Handoff`를 canonical path에 배치했고 별도 persistence commit이 없다는 inherited contract 아래, 시작 Git-visible dirt는 **정확히 다음 5개 path**여야 한다.

```text
.aiassistant/records/aiscc/cycles/20260907_1805_aiscc-p2-1d-persistence-final-acceptance-p2-1e-entry-authorization-1.cycle.md

.aiassistant/reports/aiscc/20260907_1805_aiscc-browser-command-center-p2-1d-completion-p2-1e-entry-handoff-1.md

.aiassistant/tasks/done/20260907_1814_aiscc-p2-1e-cycle-next-action-integrated-command-center-implementation-1.md

.aiassistant/records/aiscc/cycles/20260907_2241_aiscc-p2-1e-preflight-blocked-known-governance-dirt-1.cycle.md

.aiassistant/reports/aiscc/20260907_2241_aiscc-browser-command-center-p2-1e-preflight-blocked-retry-entry-handoff-1.md
```

Required equality:

```text
actual Git-visible dirt
==
expected five-path known governance dirt
```

추가 path가 있어도 안 되고, expected path가 빠져도 안 된다.

특히 다음은 0이어야 한다.

```text
unexpected product source dirt
unexpected test dirt
unexpected backend/API/DTO dirt
unexpected config/migration dirt
unexpected governance dirt outside five-path set
Git index entries
```

### 6.3 mismatch behavior

actual set이 exact five-path set과 다르면:

```text
STOP
result:
blocked
mandatory_stop:
DIRTY_WORKSPACE_MIXED
```

보고서에는 반드시:

```text
expected set
actual set
extra set
missing set
index state
branch/HEAD/tree
```

를 분리해서 적는다.

이 경우 source body audit와 mutation을 시작하지 않는다.

### 6.4 forbidden cleanup

preflight mismatch를 해결하려고 다음을 수행하지 않는다.

```text
git clean
broad reset
git restore on unrelated paths
git stash
recursive governance deletion
implicit deletion/normalization of predecessor artifacts
broad cache cleanup
```

Task가 허용하지 않은 dirt를 임의로 없애서 precondition을 맞추지 않는다.

---

# 7. accepted predecessor byte identity gate

exact five-path workspace preflight가 PASS한 뒤, source audit 전에 다음 accepted identities를 확인한다.

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

src/aiscc/api/routes/command_center_ui.py
SHA-256:
82d73e29ed5c185948ba82a5fc79083cafdb77b36b3f30760f570c295af01fd2
```

하나라도 다르면 P2-1D accepted bytes가 current source와 충돌한 것이다.

이 경우 mutation을 시작하지 말고:

```text
POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

또는 정확한 conflict classification으로 STOP한다.

P2-1D를 조용히 reopen하거나 overwrite하지 않는다.

---

# 8. source/contract audit Gate A-F

이 audit는 구현 범위를 정당화하기 위한 mandatory gate다.

모든 Gate는 source symbol/path와 실제 contract 근거를 report에 적는다.

`PASS`를 추정하지 않는다.

## Gate A — Cycle existing endpoint sufficiency

검증 대상:

```text
GET /v1/command-center/cycles/{cycle_id}
```

PASS 조건:

- endpoint가 current source에서 실제 존재한다.
- runtime `AdmittedCycle` read authority를 사용한다.
- P2-1E Cycle detail / provenance presentation에 필요한 현재 accepted DTO projection을 제공한다.
- UI convenience를 위해 새 write/read backend authority를 만들 필요가 없다.
- privacy/read-only/fail-closed semantics가 accepted P2-1A boundary와 충돌하지 않는다.

FAIL/HOLD 조건:

- required Cycle presentation을 위해 새 DTO owner, 새 query authority, persistence change 또는 new endpoint가 필요함이 source로 확인된다.

그 경우 구현하지 말고 exact gap을 보고한다.

## Gate B — NextAction existing endpoint sufficiency

검증 대상:

```text
GET /v1/command-center/projects/{project_id}/next-action
```

PASS 조건:

- endpoint가 current source에서 실제 존재한다.
- side-effect-free NextAction read semantics를 보존한다.
- P2-1E Next Action presentation에 필요한 accepted projection을 제공한다.
- UI rendering을 위해 next action을 새로 계산하거나 authoritative state를 mutate할 필요가 없다.

FAIL/HOLD 조건:

- UI 때문에 새로운 next-action calculation owner, new persistence, new API/DTO authority가 필요함이 확인된다.

## Gate C — accepted DTO/UI Cycle navigation ref

PASS 조건:

- 기존 queue/outcome/work-run UI 또는 accepted read DTO에 Cycle detail로 이동할 수 있는 stable `cycle_id` 또는 동등한 accepted navigation reference가 실제로 존재한다.
- 그 ref를 사용해 UI가 Cycle detail을 요청할 수 있다.
- fabricated ID, heuristic lookup, raw DB access, hidden authoritative reconstruction이 필요하지 않다.

FAIL/HOLD 조건:

- accepted UI/read model에서 Cycle navigation reference가 실제로 연결되지 않으며 이를 위해 범위 밖 backend/DTO mutation이 필요하다.

## Gate D — four-path implementation sufficiency

아래 네 path만으로 P2-1E source candidate를 구현할 수 있는지 판단한다.

```text
src/aiscc/command_center/web.py
src/aiscc/api/routes/command_center_ui.py
tests/integration/command_center/test_web_ui.py
tests/unit/command_center/test_web_shell.py
```

PASS 조건:

- required UI route/rendering/navigation/test coverage를 이 네 path 내에서 구현할 수 있다.
- accepted P2-1A backend/API/DTO/persistence source를 수정할 필요가 없다.

FAIL/HOLD 조건:

- 네 path 밖 product/test/config/migration 변경이 필요하다.

Gate D FAIL 시 allowlist를 임의 확대하지 않는다.

## Gate E — no dependency/config/migration requirement

PASS 조건:

- package/dependency 추가가 필요 없다.
- Node/npm frontend가 필요 없다.
- DB migration/schema change가 필요 없다.
- repository config/.gitignore/container config 변경이 필요 없다.
- external service/network integration이 필요 없다.

하나라도 필요하면 STOP하고 scope expansion을 보고한다.

## Gate F — refresh/current-authority semantics preservation

PASS 조건:

- Cycle/NextAction 추가 후에도 기존 accepted refresh/polling/current-authority semantics를 보존할 수 있다.
- failed read를 새로운 current state로 표시하지 않는다.
- stale/retained detail을 current authority로 오인시키지 않는다.
- unchanged/no-change recovery semantics를 훼손하지 않는다.
- terminal polling stop / visibility polling behavior를 무관하게 깨뜨리지 않는다.
- P2-1C/P2-1D에서 분리된 status/evidence/human/judgment 의미를 Cycle summary가 다시 collapse하지 않는다.

FAIL/HOLD 조건:

- implementation이 accepted current-authority or refresh semantics를 깨뜨려야만 가능하다.

---

# 9. audit decision

구현 시작 조건:

```text
Gate A == PASS
Gate B == PASS
Gate C == PASS
Gate D == PASS
Gate E == PASS
Gate F == PASS
```

모두 PASS가 아니면 mutation 금지.

결과는:

```text
blocked / HOLD_REWORK_REQUIRED / EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

중 실제 원인에 맞게 분류한다.

Gate 실패를 편의상 새 backend authority 추가로 해결하지 않는다.

---

# 10. 구현 범위 — Gate A-F 모두 PASS일 때만

## 10.1 product intent

P2-1E는 Command Center의 마지막 P2-1 UI slice다.

통합 목표:

```text
Project / queue
→ WorkRun detail
→ transition/execution
→ evidence
→ Human/Judgment
→ Cycle provenance
→ Next Action
```

사용자가 현재 작업의 admitted 결과와 다음 행동을 한 화면 흐름에서 이해할 수 있어야 한다.

## 10.2 web boundary

계속 유지:

```text
Python / FastAPI / Uvicorn
same-process HTML-first
plain CSS
minimal progressive JavaScript
no Node/npm/SPA framework

UI namespace:
/command-center

read API namespace:
/v1/command-center

LOCAL_PRIVATE_ONLY
read-only first
```

## 10.3 Cycle presentation

Cycle detail은 accepted read endpoint를 사용한다.

표시 대상은 source DTO가 실제 제공하는 필드 범위 안에서만 구현한다.

최소 semantic categories:

```text
Cycle identity
Task / WorkRun linkage when available
result / judgment provenance
admitted evidence summary/reference when available
Human-owned result/provenance when available
state/transition provenance when available
commit/result mapping when available
next-action relation when available
```

없는 field를 UI에서 추정/합성하지 않는다.

raw private data 또는 unrestricted raw report dump를 노출하지 않는다.

## 10.4 Next Action presentation

Next Action은 accepted side-effect-free read endpoint를 사용한다.

표시 대상은 source DTO가 실제 제공하는 범위에서:

```text
project identity/reference
selected action identity/title/type
reason
blocker
required baseline / prerequisite refs when available
human verification requirement when available
```

NextAction GET/read가 새 next action을 생성하거나 workflow state를 mutate하게 만들지 않는다.

## 10.5 navigation / integration

- accepted stable Cycle ref가 있는 위치에서 Cycle detail navigation을 제공한다.
- 프로젝트/queue/work-run 흐름과 끊기지 않게 한다.
- Next Action presentation은 현재 project context와 연결한다.
- 기존 P2-1B shell/filter 및 P2-1C/P2-1D detail behavior를 깨뜨리지 않는다.
- user-visible copy는 Korean-first다.
- canonical identifier/state/API name은 원문을 유지할 수 있다.

## 10.6 current authority / refresh semantics

기존 accepted rules를 보존한다.

특히:

```text
read failure
!= new current snapshot

retained previous detail
!= current authoritative detail

unchanged/recovery
!= fabricated update

hidden page
→ polling stop

visible page
→ polling resume when applicable

terminal state
→ polling stop when applicable
```

Cycle/NextAction UI 때문에 whole-page polling을 무조건 늘리거나 provider inference를 발생시키지 않는다.

## 10.7 density concern

P2-1B에서 다음 관찰이 deferred 되었다.

```text
approximately 1080-wide / 910-high:
page header + filters + one full WorkRun card do not all fit vertically at once
```

이번 source implementation에서 임의 3-column redesign을 선결하지 않는다.

필요한 최소 layout integration만 구현하고, 최종 integrated Browser QA에서 실제 visual/usability 결과를 사람이 판정하도록 둔다.

---

# 11. mutation allowlist

Gate A-F 모두 PASS한 경우에만 아래 path mutation을 허용한다.

```text
src/aiscc/command_center/web.py
src/aiscc/api/routes/command_center_ui.py
tests/integration/command_center/test_web_ui.py
tests/unit/command_center/test_web_shell.py
```

가능하면 필요한 path만 수정한다.

다음은 명시적으로 mutation 금지다.

```text
src/aiscc/domain/**
src/aiscc/application/**
src/aiscc/persistence/**
src/aiscc/api/**  # except exact command_center_ui.py above
alembic/**
migrations/**
pyproject.toml
uv.lock
package.json
package-lock.json
.gitignore
Docker/container/deployment config
.aiassistant/rules/**
.aiassistant/records/command-center/**
.aiassistant/records/aiscc/**  # except task lifecycle does not create Cycle; Browser owns Cycle
.aiassistant/reports/aiscc/**
```

Task lifecycle에 따른 current Task의 `active -> done` 이동과 ignored target export 생성은 canonical workflow상 허용된다.

---

# 12. 절대 금지

- `git clean`
- broad reset/restore/stash
- `git add`
- `git commit`
- `git push`
- PR merge
- deployment
- Browser Project Source upload/sync
- credentialed external action
- external network access
- public release
- P2-2/P2-3/P2-4 실행
- mutation control 추가
- write endpoint 추가
- Human QA를 Agent가 PASS로 보고
- frontend source test를 Browser QA로 대체
- mock/TestClient evidence를 PostgreSQL-backed runtime proof로 과장
- report field를 채우기 위한 unrelated full-suite/DB/browser/network 확대

---

# 13. workflow transition expectation

```text
initial project phase state:
P2-1E PRE_IMPLEMENTATION_BLOCKED / RETRY_REQUIRED

preflight PASS + Gate A-F PASS + implementation/test/runtime candidate complete:
P2-1E ACCEPTED_CANDIDATE / HUMAN_INTEGRATED_BROWSER_QA_PENDING

Human QA:
not performed by Executor

terminal P2-1E/P2-1 state:
NOT OWNED BY THIS TASK

transition authority:
Browser Command Center / Human according to evidence ownership
```

Agent가 P2-1E 또는 P2-1을 terminally accepted/closed로 확정할 수 없다.

---

# 14. evidence contract

## executor_required

### A. exact preflight

channel: `STATIC_SOURCE / GIT_WORKSPACE`

scope:
- branch/HEAD/tree/index
- exact five-path known-governance-dirt equality
- accepted four-path SHA identity

pass condition:
- exact match only

### B. source/contract audit A-F

channel: `STATIC_SOURCE`

scope:
- Cycle endpoint
- NextAction endpoint
- Cycle navigation ref
- four-path sufficiency
- dependency/config/migration sufficiency
- refresh/current-authority semantics

pass condition:
- A-F each individually evidenced and PASS before mutation

### C. source/static implementation proof

channel: `STATIC_SOURCE / FRONTEND_SOURCE_TEST`

scope:
- changed exact paths
- Korean-first visible copy
- navigation/rendering/current-authority semantics
- read-only behavior

pass condition:
- targeted source/unit/integration tests PASS
- no unrelated regression in directly affected UI contract

### D. applicable local runtime/read API integration proof

channel: `HTTP_RUNTIME / INTEGRATION_TEST`

scope:
- actual same-process/local Command Center runtime as applicable to changed behavior
- Cycle read path
- NextAction read path
- relevant UI route/render integration
- failure/recovery behavior directly affected by P2-1E

pass condition:
- actual executed runtime proof; generated artifact alone is insufficient

If current authorized environment cannot provide required runtime proof without creating a new nontrivial DB/runtime harness outside Task scope:

```text
EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

으로 중단한다.

## reuse_allowed

P2-1A/B/C/D accepted persisted behavior는 다음 조건을 모두 만족할 때만 재사용한다.

```text
accepted predecessor bytes/applicability exact
changed path가 해당 proof를 invalidate하지 않음
proof type이 current requirement와 동일
```

재사용 가능한 대표 범위:

- unchanged P2-1A read API semantics
- unchanged P2-1B shell/queue behavior
- unchanged P2-1C transition/execution semantics
- unchanged P2-1D evidence/Human/Judgment semantics

## human_owned

channel: `HUMAN_VERIFICATION / BROWSER_RUNTIME`

scope:

```text
P2-1 integrated Browser/Visual/Usability QA
including responsive 1080 / 1280 / 1440 and deferred density observation
```

Executor result:

```text
HUMAN_PENDING
```

이번 Task는 QA checklist를 실제 Human result로 간주하지 않는다.

## not_required

```text
public release
production deployment
P2-2
Project Source sync
provider/model call
external network
Git persistence commit
```

## forbidden

```text
Agent claiming Human Browser QA
proof-type substitution
new backend semantic authority for UI convenience
write/mutation controls
Git add/commit/push/deployment
broad cleanup
```

## proof_non_substitution

```text
frontend source/static test
!= Human Browser QA

TestClient/mock response
!= actual runtime proof when runtime proof is required

Agent report
!= Browser Command Center judgment

Executor completed
!= P2-1E accepted

Cycle read projection
!= raw persistence authority

NextAction display
!= next-action generation/state mutation
```

---

# 15. targeted verification expectation

Gate A-F PASS 후 구현했다면 최소 다음을 수행한다.

1. changed Python source syntax/import check
2. `tests/unit/command_center/test_web_shell.py` targeted tests
3. `tests/integration/command_center/test_web_ui.py` targeted tests
4. directly relevant existing Command Center tests discovered through the exact changed/import chain only
5. applicable local runtime/read API verification for:
   - Cycle detail/read
   - NextAction read
   - UI route integration/navigation
   - directly affected failure/current-authority behavior
6. `git diff --check` or equivalent encoding/whitespace validation
7. UTF-8/control-character validation for changed text assets

Do not automatically run unrelated full suite.

새 environment/network/browser/credential/full-suite가 필요하면 scope expansion으로 STOP한다.

---

# 16. accept 기준

Executor candidate는 다음을 모두 만족해야 Browser substantive review 대상으로 제출 가능하다.

```text
retry preflight exact PASS
accepted four-path identity PASS before mutation
Gate A-F ALL PASS before mutation
mutation within exact allowlist
no new backend/API/DTO/persistence authority
no dependency/config/migration change
Korean-first UI preserved
read-only / LOCAL_PRIVATE_ONLY preserved
Cycle presentation implemented from accepted read authority
NextAction presentation implemented from accepted read authority
stable Cycle navigation ref used
current-authority/refresh semantics preserved
targeted source/unit/integration PASS
applicable local runtime/read API proof EXECUTED_PASS
Human Browser QA == HUMAN_PENDING
forbidden actions == FORBIDDEN_NOT_RUN
```

Expected Executor disposition on success:

```text
completed
candidate_status:
P2-1E ACCEPTED_CANDIDATE / HUMAN_INTEGRATED_BROWSER_QA_PENDING
```

`ACCEPTED` 또는 `CLOSED`라고 보고하지 않는다.

---

# 17. hold / reject 기준

다음 중 하나면 implementation acceptance candidate로 제출하지 않는다.

- exact five-path workspace mismatch
- branch/HEAD mismatch
- accepted predecessor source hash mismatch
- Gate A-F 중 하나 이상 FAIL/BLOCKED
- four-path 밖 mutation 필요
- new backend/API/DTO/persistence authority 필요
- dependency/config/migration 필요
- read-only/current-authority semantics 보존 불가
- required targeted test FAIL
- required runtime proof 미수행/실패
- Human QA 완료 false claim
- proof type substitution
- forbidden Git/deployment/network action
- P2-2 scope creep

Classification은 실제 원인에 따라 다음 중 선택한다.

```text
DIRTY_WORKSPACE_MIXED
POLICY_CONFLICT_INVESTIGATION_REQUIRED
HOLD_REWORK_REQUIRED
EVIDENCE_SCOPE_EXPANSION_REQUIRED
EXECUTOR_SCOPE_CREEP
PROOF_TYPE_SUBSTITUTION
HUMAN_OWNED_EVIDENCE_FALSE_CLAIM
FORBIDDEN_ACTION_EXECUTED
```

---

# 18. mandatory stop 조건

- branch/HEAD/index mismatch
- exact five-path known-governance-dirt mismatch
- accepted source hash mismatch
- policy/baseline/current source conflict
- Gate A-F failure
- missing required canonical artifact
- forbidden action/tool request
- security boundary uncertainty
- `EVIDENCE_SCOPE_EXPANSION_REQUIRED`
- four-path 밖 mutation requirement
- Human decision required before further mutation

named blocker 이후에는 blocker를 입증하는 최소 evidence, workspace inventory, report/export와 안전한 종료만 수행한다.

---

# 19. 보고서 필수 항목

- 작업명 / work type / Task path
- read canonical paths
- initial branch/HEAD/tree/index
- expected five-path known governance dirt
- actual Git-visible dirt
- extra/missing delta
- accepted four-path pre-mutation SHA result
- Gate A-F 각각의 source/path/symbol 근거와 PASS/FAIL
- source inventory
- product source changes
- governance/provenance changes
- repository configuration changes
- added/modified/removed files
- Cycle endpoint actual source/DTO owner
- NextAction endpoint actual source/DTO owner
- Cycle navigation ref actual source
- planned vs actual mutation scope
- current-authority/refresh semantics conformance
- Task evidence contract와 actual classifications
- Agent claim vs admitted evidence
- reused predecessor evidence와 applicability
- Human pending
- forbidden-not-run
- mandatory stop/scope expansion
- test commands/results
- runtime commands/environment/results when executed
- unverified items
- rollback/revert guide
- preserved exact paths
- next turn recommendation

---

# 20. export bundle 요구

Target:

```text
.aiassistant/reports/target/20260907_2252_aiscc-p2-1e-cycle-next-action-integrated-command-center-implementation-retry-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
```

추가:

```text
changed files preserving project-relative paths
REMOVED_FILES.md only when deletion exists
```

Preflight/audit/runtime evidence를 별도 파일로 분리하는 경우 manifest에 모두 포함한다.

예:

```text
WORKSPACE_INVENTORY.md
SOURCE_CONTRACT_AUDIT.md
RUNTIME_EVIDENCE.md
```

단, 빈 evidence file을 만들기 위해 scope를 확대하지 않는다.

`tasks/active`의 Task는 Executor 제출 준비가 완료되면:

```text
.aiassistant/tasks/done/20260907_2252_aiscc-p2-1e-cycle-next-action-integrated-command-center-implementation-retry-1.md
```

으로 이동한다.

blocked turn이어도 report/export가 완성되어 Executor turn이 종료되면 done으로 이동할 수 있다.

---

# 21. artifact preservation

Executor final response/report에 최소 다음을 exact path로 보존 대상으로 적는다.

```text
.aiassistant/tasks/done/20260907_2252_aiscc-p2-1e-cycle-next-action-integrated-command-center-implementation-retry-1.md

.aiassistant/records/aiscc/cycles/20260907_1805_aiscc-p2-1d-persistence-final-acceptance-p2-1e-entry-authorization-1.cycle.md

.aiassistant/reports/aiscc/20260907_1805_aiscc-browser-command-center-p2-1d-completion-p2-1e-entry-handoff-1.md

.aiassistant/tasks/done/20260907_1814_aiscc-p2-1e-cycle-next-action-integrated-command-center-implementation-1.md

.aiassistant/records/aiscc/cycles/20260907_2241_aiscc-p2-1e-preflight-blocked-known-governance-dirt-1.cycle.md

.aiassistant/reports/aiscc/20260907_2241_aiscc-browser-command-center-p2-1e-preflight-blocked-retry-entry-handoff-1.md
```

현재 target bundle은 Browser review용 temporary artifact다.

Command Center가 이후 생성할 Cycle/Handoff는 이 Task가 미리 만들지 않는다.

---

# 22. 사람 검증 요구

이번 Executor turn에서 Human Browser QA를 수행하지 않는다.

성공 candidate가 Browser Command Center에서 source/runtime substantive acceptance를 받은 뒤 별도 Human QA entry가 열릴 수 있다.

향후 Human integrated Browser QA는 최소 다음 concern을 포함해야 한다.

```text
whole Command Center flow
Cycle detail readability / provenance clarity
Next Action clarity
navigation continuity
read failure / recovery visibility
current vs retained/stale authority distinction
responsive 1080 / 1280 / 1440
approximately 1080-wide / 910-high density concern
```

정확한 Human QA operations는 후속 Browser judgment가 freeze한다.

---

# 23. 최종 응답 형식

1. `result: completed / blocked / rejected-candidate`
2. target bundle path
3. retry preflight result
4. Gate A-F result
5. changed files
6. removed files
7. targeted/source/runtime evidence result
8. human verification: `HUMAN_PENDING` 또는 해당 blocked 상태
9. unverified items
10. preserved exact paths
11. next recommendation

장문 report 전문은 chat에 붙이지 않는다.

---

# 24. 핵심 retry directive

```text
DO NOT require a clean Git-visible worktree.

Require exact equality with the five known governance paths.

DO NOT clean those five paths.

After exact preflight PASS:
run source/contract audit Gate A-F.

Only if A-F ALL PASS:
implement P2-1E within the four-path mutation allowlist.

DO NOT invent backend authority.
DO NOT start P2-2.
DO NOT claim Human Browser QA.
DO NOT commit/push/deploy.
```
