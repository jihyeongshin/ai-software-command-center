# P2-1E Human Integrated Browser QA — Operation Guide

## 0. 문서 목적 / Gate 성격

이 문서는 **사람이 실제 Browser에서 직접 수행하는 P2-1E 최종 통합 QA 절차서**다.

```text
work_type: HUMAN_QA_GATE / HUMAN_QA_ONLY
owner: Human
executor: NOT_APPLICABLE
short Executor prompt: NOT_REQUIRED
execution_mode: MANUAL_COMMAND_CENTER
```

IDE Executor 구현 Task가 아니다. 이 문서를 IDE Executor에 전달하지 않는다.

현재 authority:

```text
P2-1D:
HUMAN_PROVIDED / ACCEPTED / PERSISTED

P2-1E SOURCE_CONTRACT_AUDIT:
EXECUTED_PASS / REUSED_ACCEPTED

P2-1E IMPLEMENTATION:
ACCEPTED_CANDIDATE

P2-1E POSTGRESQL_BACKED_RUNTIME:
EXECUTED_PASS

P2-1E HUMAN_INTEGRATED_BROWSER_QA:
HUMAN_PENDING / ENTERING

P2-1:
ACTIVE / NOT_CLOSED

P2-2:
NOT_STARTED
```

이번 QA에서 source/test/migration/config를 수정하지 않는다.
Git persistence도 수행하지 않는다.

Human QA PASS는 다음까지만 의미한다.

```text
P2-1E:
HUMAN_PROVIDED / ACCEPTED candidate
```

다음을 자동 의미하지 않는다.

```text
P2-1 CLOSED
P2-2 STARTED
```

---

# 1. QA 대상 candidate identity

QA 전에 아래 네 파일이 P2-1E accepted candidate bytes인지 확인 가능하면 확인한다.
Human QA 자체를 위해 새 source hash 검증을 강제하지는 않지만, 다른 작업으로 candidate bytes가 변경됐음을 알고 있다면 QA를 시작하지 않는다.

```text
src/aiscc/command_center/web.py
d58360e4df00c167225960ee9fef93e64cc4910adf173b20263c8449d58c5631

src/aiscc/api/routes/command_center_ui.py
10951dee88468bf95faae2c47b3cca649e37fc8adccc7586f47dd8729127bf37

tests/integration/command_center/test_web_ui.py
99bad1694845900870cd83a4e62303653ed7e2b52496fa12dfef766ce45e820d

tests/unit/command_center/test_web_shell.py
8c8ffffdd9546206a3d92d02dc09dcc5a388e7b34a97432b5f6b1685f298ebe5
```

Accepted baseline HEAD before candidate:

```text
36bed286abf4df6e8cecea2d379896c36be5d58a
```

Do not normalize the workspace with:

```text
git clean
git reset
git restore
git checkout
git stash
```

Known ignored residue:

```text
.aiassistant/reports/target/20260907_2328_aiscc-p2-1e-retained-mypy-cache/
```

이 path 때문에 broad cleanup을 수행하지 않는다.

---

# 2. Human QA runtime 준비

## 2.1 전제

`2328` Task-owned runtime은 이미 정리되었다.
따라서 Browser를 열기 전에 Human QA용 narrow local runtime을 다시 준비해야 한다.

Repository:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center
```

Required local prerequisites:

```text
repository-local .venv
local Docker
local postgres:17.6-alpine image
```

허용 runtime pattern:

```text
PostgreSQL 17.6
postgres:17.6-alpine
--pull=never
loopback only
Task-owned disposable DB
tmpfs /var/lib/postgresql/data
existing Alembic migration path
existing repository fixture/setup path
normal AISCC entrypoint
```

금지:

```text
Docker image pull
external network/provider
remote DB
new DB harness
new migration
source/test/config mutation
Git add/commit/push
public deployment
```

Local image가 없고 준비하려면 network pull이 필요한 경우:

```text
BLOCKED_ENVIRONMENT
```

으로 보고하고 QA를 시작하지 않는다.

## 2.2 PostgreSQL

권장 Human-QA resource identity:

```text
container:
aiscc-p2-1e-human-qa

bind preference:
127.0.0.1:55439 -> 5432
fallback:
127.0.0.1:55440 -> 5432
127.0.0.1:55441 -> 5432

storage:
tmpfs /var/lib/postgresql/data
```

반드시:

```text
--pull=never
postgres:17.6-alpine
```

을 사용한다.

DB username/password/database 및 `AISCC_DATABASE_URL` / `AISCC_TEST_DATABASE_URL` 값은 **Human QA shell의 임시 값**으로만 둔다.
Credential-bearing URL이나 password 값을 QA 결과, screenshot, Cycle, chat에 붙여넣지 않는다.

환경변수:

```text
AISCC_DATABASE_URL
AISCC_TEST_DATABASE_URL
PYTHONDONTWRITEBYTECODE=1
```

DB URL의 driver/scheme은 repository의 현재 accepted runtime/test harness가 사용하는 형식을 그대로 사용한다.
새 URL convention을 만들지 않는다.

Migration:

```text
.venv\Scripts\python.exe -m alembic upgrade head
```

Expected head:

```text
20260901_0008
```

Migration source를 수정하지 않는다.

## 2.3 deterministic fixture/setup

P2-1E QA data는 **existing repository-provided fixture/setup path**만 사용한다.
새 durable authority나 ad-hoc production-like data를 만들지 않는다.

Accepted fixture chain owner:

```text
tests/integration/command_center/test_postgres_read_api.py
→ database_url fixture
→ _seed
```

P2-1E accepted runtime도 이 existing harness 계열을 사용했다.

Human QA fixture는 최소 아래 관찰 대상을 제공해야 한다.

```text
A. Project with queue + outcomes + NextAction
B. accepted outcome with admitted_cycle.cycle_id / cycle_ref
C. Cycle detail reachable from the accepted outcome
D. outcome with no admitted Cycle ref, or equivalent truthful absence fixture
E. NextAction NONE/empty dimension fixture
F. nonterminal WorkRun for visible polling
G. terminal WorkRun for terminal polling stop
H. existing Evidence/Human/Judgment detail fixture
```

기존 fixture/setup이 D 또는 E를 안전하게 제공하지 못하면 임의 DB row 수정으로 제조하지 않는다.
그 경우 해당 Operation은:

```text
BLOCKED_FIXTURE_GAP
```

으로 보고한다.

`DENIED` Transition actual instance는 별도 예외다.
없으면 아래처럼 truthfully 보고해도 된다.

```text
DENIED actual instance:
NOT_OBSERVED
```

## 2.4 AISCC server

Normal entrypoint:

```text
.venv\Scripts\python.exe -m aiscc serve --host 127.0.0.1 --port 8765
```

8765가 Task-unrelated process 때문에 사용 중이면:

```text
8766
then 8767
```

순으로 사용 가능하다.

외부 bind는 금지한다.

---

# 3. QA URL 확정

Browser Zoom:

```text
100%
```

Base:

```text
http://127.0.0.1:8765
```

server port를 fallback으로 바꿨다면 아래 모든 URL의 port만 동일하게 치환한다.

Fixture setup 직후 아래 값을 기록한다.

```text
QA_PROJECT_ID=<actual seeded project_id>
QA_CYCLE_ID=<actual admitted cycle_id>
QA_PRIMARY_WORK_RUN_ID=<actual nonterminal/current regression WorkRun id>
QA_TERMINAL_WORK_RUN_ID=<actual terminal WorkRun id>
QA_NO_CYCLE_PROJECT_ID=<same project or fixture project containing no-cycle outcome>
QA_NONE_NEXT_ACTION_PROJECT_ID=<project with truthful NONE/empty NextAction>
```

이 값이 확보된 후 이번 QA의 exact URLs는 다음이다.

```text
Project:
http://127.0.0.1:8765/command-center/projects/<QA_PROJECT_ID>

Cycle:
http://127.0.0.1:8765/command-center/cycles/<QA_CYCLE_ID>

Primary WorkRun regression:
http://127.0.0.1:8765/command-center/work-runs/<QA_PRIMARY_WORK_RUN_ID>

Terminal WorkRun regression:
http://127.0.0.1:8765/command-center/work-runs/<QA_TERMINAL_WORK_RUN_ID>

No-Cycle outcome project:
http://127.0.0.1:8765/command-center/projects/<QA_NO_CYCLE_PROJECT_ID>

NONE NextAction project:
http://127.0.0.1:8765/command-center/projects/<QA_NONE_NEXT_ACTION_PROJECT_ID>
```

QA 결과 제출 시 `<...>` placeholder를 남기지 말고 실제 expanded ID/URL을 `QA runtime identity`에 기록한다.

---

# Operation 1 — 서버 / Project page 접속

## 수행

1. Project URL을 연다.
2. 새로고침한다.

## PASS

- `127.0.0.1` 접속 오류가 없다.
- Command Center Project page가 정상 표시된다.
- queue/current project 정보가 보인다.
- P2-1E 추가 영역 때문에 페이지 전체가 깨지지 않는다.

접속 자체가 실패하면:

```text
BLOCKED_ENVIRONMENT
```

으로 보고하고 source defect로 판정하지 않는다.

---

# Operation 2 — P2-1E 통합 Project 화면 구조

Project page를 위에서 아래까지 확인한다.

기존 영역:

```text
Project / Queue
WorkRun cards
Outcome / Judgment 관련 projection
기존 navigation / filters / refresh
```

P2-1E 통합 영역:

```text
NextAction
accepted outcome → Cycle navigation
```

## PASS

- 기존 Project queue가 유지된다.
- NextAction이 기존 authority/card hierarchy를 압도하거나 덮지 않는다.
- accepted outcome의 Cycle navigation은 관련 outcome 문맥 안에서 식별 가능하다.
- 페이지는 read-only로 보인다.
- 긴 ID 때문에 layout이 무너지지 않는다.

---

# Operation 3 — NextAction semantic separation

Project page의 NextAction 영역에서 아래 세 차원을 찾는다.

```text
projection
selection
task_issuance_candidate
```

## PASS

사람이 다음을 서로 다른 사실로 이해할 수 있어야 한다.

```text
projection
!= selection
!= task issuance candidate
```

특히:

- 화면 표시만으로 새 NextAction이 생성된 것처럼 보이지 않는다.
- `selection`이 task 발행 완료처럼 보이지 않는다.
- `task_issuance_candidate`가 authoritative Task 발행 완료처럼 보이지 않는다.
- 세 값 중 `NONE`이 있어도 다른 차원의 값을 조용히 대신하지 않는다.

---

# Operation 4 — accepted outcome → Cycle navigation

## 수행

1. Project page에서 admitted Cycle ref가 있는 accepted outcome을 찾는다.
2. Cycle link/control을 클릭한다.

## PASS

- 실제 Browser click으로 Cycle detail page로 이동한다.
- destination URL의 `cycle_id`가 clicked outcome의 admitted `cycle_id`와 일치한다.
- 다른 outcome/Cycle로 이동하지 않는다.
- URL에 raw/unescaped 이상 문자열이 노출되지 않는다.
- 뒤로가기로 Project page로 정상 복귀 가능하다.

---

# Operation 5 — Cycle detail provenance semantics

Cycle page에서 최소 아래 의미가 구분되는지 확인한다.

```text
Task / Task constraint refs
Judgment
TransitionDecision
Evidence provenance / refs
Cycle identity / result
```

## PASS

- `Judgment != TransitionDecision`로 보인다.
- Evidence ref가 곧 Judgment처럼 보이지 않는다.
- Task constraint/ref와 historical Cycle result가 섞이지 않는다.
- raw persistence dump처럼 무제한 내부 정보가 노출되지 않는다.
- 긴 ref/hash/id가 layout을 깨지 않는다.

---

# Operation 6 — current_memory labeling

Cycle detail의 `current_memory` 또는 그 사람용 표시를 확인한다.

## PASS

아래 의미가 분명해야 한다.

```text
current project memory context
!=
historical Cycle result
```

즉:

- `current_memory`가 과거 Cycle 당시 snapshot 자체인 것처럼 보이지 않는다.
- 현재 project memory context라는 labeling이 있다.
- current memory가 historical Judgment/TransitionDecision/Evidence 결과를 덮어쓰지 않는다.

---

# Operation 7 — Cycle missing-ref / no-link truthful state

No-Cycle fixture Project page를 연다.

## PASS

- admitted Cycle ref가 없는 outcome에 가짜 Cycle link가 생기지 않는다.
- 빈 `href`, `#`, `undefined`, `null` navigation이 보이지 않는다.
- 존재하지 않는 Cycle이 있는 것처럼 표시하지 않는다.
- 필요하면 `없음`/미입장/참조 없음에 해당하는 truthful state가 표시된다.

Fixture 자체가 없으면:

```text
BLOCKED_FIXTURE_GAP
```

으로 보고하고 임의 DB mutation으로 만들지 않는다.

---

# Operation 8 — NextAction empty / NONE truthful state

NONE NextAction fixture Project page를 연다.

## PASS

- `projection`, `selection`, `task_issuance_candidate`의 NONE/absence가 각각 truthful하게 표시된다.
- `undefined`, `null`, 깨진 빈 카드가 없다.
- NextAction이 없는 상태를 오류나 Task 발행 완료로 오인시키지 않는다.
- 한 dimension의 값으로 다른 dimension의 NONE을 채우지 않는다.

Fixture 자체가 없으면:

```text
BLOCKED_FIXTURE_GAP
```

으로 보고한다.

---

# Operation 9 — Project current-authority failure gating

목적:

```text
queue/current authority failure
→ companion NextAction/outcomes를 새 current로 승격하지 않음
```

## 수행

1. Project page를 정상적으로 연어 queue/outcomes/NextAction의 last-successful 상태를 먼저 확보한다.
2. DevTools → Network에서 아래 queue read를 찾는다.

```text
GET /v1/command-center/projects/<QA_PROJECT_ID>/queue
```

3. `Block request URL`을 적용한다.
4. visible/nonterminal polling 또는 수동 refresh가 일어나게 한다.

## PASS

- Project page 전체가 빈 값으로 무너지지 않는다.
- 이전 성공 queue/current data가 있으면 retained 된다.
- 동시에 도착한 outcomes/NextAction 응답이 새 authoritative current처럼 승격되지 않는다.
- retained companion section은 stale/retained/refresh-failed 의미가 분명하다.
- stale data를 `최신`/current처럼 부르지 않는다.

실제 visible copy를 결과에 기록한다.

---

# Operation 10 — Cycle / NextAction endpoint-local failure retained/stale

## 10-A NextAction

1. Operation 9의 queue block을 해제하고 정상 Project page로 복구한다.
2. 아래 endpoint만 block한다.

```text
GET /v1/command-center/projects/<QA_PROJECT_ID>/next-action
```

3. refresh/polling을 발생시킨다.

### PASS

- Project page 전체가 실패하지 않는다.
- last-successful NextAction DOM이 있으면 유지된다.
- NextAction section만 실패/stale 의미를 표시한다.
- empty value로 조용히 덮어쓰지 않는다.
- endpoint failure가 queue/outcomes를 실패로 위조하지 않는다.

실제 visible copy를 기록한다.

## 10-B Cycle

1. NextAction block을 해제한다.
2. Cycle page를 정상 load한다.
3. 아래 endpoint를 block한다.

```text
GET /v1/command-center/cycles/<QA_CYCLE_ID>
```

4. Cycle page의 수동 refresh를 수행한다.

### PASS

- last-successful Cycle detail이 있으면 유지된다.
- retained/stale 또는 read failure 의미가 표시된다.
- 기존 Cycle DOM을 빈 값으로 바꾸지 않는다.
- failed read가 새 ETag/current snapshot처럼 보이지 않는다.

실제 visible copy를 기록한다.

---

# Operation 11 — retained/stale → current recovery

Operation 10의 blocked URL을 모두 해제한다.

## 수행

1. Project NextAction을 다시 refresh한다.
2. Cycle detail을 다시 refresh한다.

## PASS

- 정상 data가 다시 current로 표시된다.
- stale/error label이 정상 상태로 돌아온다.
- 중복 card/row/section이 생기지 않는다.
- 과거 retained DOM과 새 current DOM이 동시에 authoritative처럼 남지 않는다.

실제 recovery copy가 있으면 기록한다.

---

# Operation 12 — 304 / no-change behavior

DevTools Network를 연고 정상 Project/Cycle refresh를 반복한다.

확인 대상:

```text
queue
outcomes
next-action
cycle
```

## PASS

- endpoint-local cache/ETag 동작이 보인다.
- 304/no-change가 발생해도 기존 DOM이 사라지지 않는다.
- no-change를 새 update처럼 표시하지 않는다.
- loading → empty → rebuilt와 같은 불필요한 flicker가 없다.
- 다른 endpoint ETag 때문에 잘못된 304가 발생한 징후가 없다.

Browser/Network가 304를 직접 노출하지 않는 환경이면 DOM 안정성 및 no-fabricated-update 관찰 결과와 함께:

```text
304 actual network status:
NOT_OBSERVED
```

를 기록한다. 이 경우 source/runtime predecessor proof를 Human-observed 304로 과장하지 않는다.

---

# Operation 13 — Transition / Execution regression

Primary WorkRun regression URL을 연다.

확인:

```text
TransitionRequest
TransitionEvaluation
guards
TransitionDecision

ExecutionAttempt
ExecutionOperation
ExecutionStatus
```

## PASS

- P2-1E 추가 이후 기존 detail이 사라지거나 깨지지 않았다.
- `DENIED != successful transition` 의미가 유지된다.
- `EXECUTOR_COMPLETED != WorkRun ACCEPTED` 의미가 유지된다.
- 읽기 전용이다.

DENIED fixture가 없으면:

```text
DENIED actual instance:
NOT_OBSERVED
```

으로 기록한다.

---

# Operation 14 — Evidence / Human / Judgment regression

Primary WorkRun regression URL에서 확인한다.

```text
EvidenceRequirement
EvidenceCandidate
EvidenceAdmissionDecision
AdmittedEvidence
RequirementSatisfaction
EvidenceSetEvaluation
EvidenceSetAttestation

HumanGate
HumanResult
Judgment
Transition Effect
```

## PASS

- 기존 P2-1D semantic separation이 유지된다.
- Candidate가 AdmittedEvidence처럼 보이지 않는다.
- HumanResult가 Judgment처럼 보이지 않는다.
- Judgment가 WorkflowState/TransitionDecision처럼 보이지 않는다.
- P2-1E 추가로 layout이 깨지지 않는다.

---

# Operation 15 — visible 10-second polling

Nonterminal WorkRun 또는 nonterminal Project fixture를 사용한다.

## 수행

1. DevTools Network log를 지운다.
2. QA tab을 visible 상태로 둔다.
3. 약 25초 관찰한다.

## PASS

- 대략 10초 단위 GET polling이 보인다.
- 두 개의 독립 P2-1E polling timer가 겹쳐 요청 폭증을 만들지 않는다.
- 화면이 flicker/empty 되지 않는다.
- mutation method가 없다.

---

# Operation 16 — hidden polling stop

Operation 15에 이어서:

1. Network log를 지운다.
2. 다른 Browser tab으로 이동한다.
3. QA tab을 약 25초 숨긴다.
4. 다시 돌아온다.

## PASS

- hidden 동안 10초 polling이 계속 누적되지 않는다.
- tab 전환 직전 이미 시작된 1건 정도는 허용한다.

---

# Operation 17 — visible polling resume

Operation 16 직후:

1. QA tab을 visible로 둔다.
2. 최대 15초 관찰한다.

## PASS

- reload 없이 polling이 재개된다.
- 동시에 여러 polling loop가 폭증하지 않는다.
- retained/current 화면이 정상 유지된다.

---

# Operation 18 — terminal polling stop

Terminal WorkRun URL을 연다.

## 수행

1. Network log를 지운다.
2. 약 25초 관찰한다.

## PASS

- initial GET 이후 10초 polling이 반복되지 않는다.
- terminal WorkRun은 자동 polling이 멈춘다.
- 수동 refresh는 가능하다.

---

# Operation 19 — responsive 1080

Browser Zoom:

```text
100%
```

Viewport width:

```text
1080
```

Project page + Cycle page + Primary WorkRun page를 확인한다.

## PASS

- 불필요한 whole-page 가로 scroll이 없다.
- 긴 ID/ref가 옆 영역을 침범하지 않는다.
- Project queue / NextAction / outcome Cycle link를 읽을 수 있다.
- Cycle provenance dimension을 구분할 수 있다.
- Transition/Execution/Evidence/Human/Judgment 기존 영역도 읽을 수 있다.

---

# Operation 20 — responsive 1280

Viewport width:

```text
1280
```

Operation 19와 같은 세 page를 확인한다.

## PASS

Operation 19의 responsive 조건을 모두 만족한다.

---

# Operation 21 — responsive 1440

Viewport width:

```text
1440
```

Operation 19와 같은 세 page를 확인한다.

## PASS

Operation 19의 responsive 조건을 모두 만족한다.

---

# Operation 22 — 약 1080 × 910 whole-page density 관찰

이 항목은 P2-1B에서 deferred된 whole-page density 관찰이다.

Viewport approximate:

```text
1080 × 910
Browser Zoom 100%
```

Project page를 본다.

## 관찰 목적

다음을 **미리 정답으로 가정하지 않는다**.

```text
3-column이 반드시 낫다
2-column이 반드시 낫다
한 화면에 특정 카드 개수가 반드시 보여야 한다
```

## PASS 기준

- 주요 heading / queue / NextAction / outcome navigation hierarchy를 따라갈 수 있다.
- 스크롤을 사용해도 정보가 겹치거나 control이 가려지지 않는다.
- 긴 값 wrapping 때문에 card가 비정상 폭발하지 않는다.
- 사용자가 현재 Project → WorkRun/Cycle로 이동하는 흐름을 이해할 수 있다.

추가로 실제 관찰을 자유롭게 기록한다.

```text
first viewport에서 보이는 범위:
<실제 관찰>

과도한 vertical density:
YES / NO

개선 필요 의견:
<있으면 기록; 바로 redesign 결정하지 않음>
```

---

# 4. Mutation regression — QA 전체 공통 확인

QA 동안 DevTools Network를 확인한다.

정상 UI interaction에서 다음 method가 없어야 한다.

```text
POST
PUT
PATCH
DELETE
```

허용:

```text
GET
navigation
manual refresh
read polling
```

또한 visible mutation control이 없어야 한다.

```text
state 변경
transition 승인/거부
evidence admit/reject
HumanResult 제출
Judgment 승인/거부/rework
NextAction 생성/선택/발행
Cycle mutation
terminal 상태 변경
```

이 항목에서 mutation이 관찰되면 별도 Operation 번호를 만들지 말고 `추가 관찰`에 즉시 기록하고 전체 QA를 FAIL로 보고한다.

---

# 5. 최종 결과 제출 양식

QA 종료 후 아래 block을 그대로 Browser Command Center 채팅에 붙여넣는다.

```text
P2-1E Human Integrated Browser QA

QA runtime identity:
server: http://127.0.0.1:<actual-port>
project_id: <actual>
cycle_id: <actual>
primary_work_run_id: <actual>
terminal_work_run_id: <actual>

Operation 1 서버 / Project page 접속:
PASS / BLOCKED_ENVIRONMENT

Operation 2 P2-1E 통합 Project 화면 구조:
PASS / FAIL

Operation 3 NextAction semantic separation:
PASS / FAIL

Operation 4 accepted outcome → Cycle navigation:
PASS / FAIL

Operation 5 Cycle detail provenance semantics:
PASS / FAIL

Operation 6 current_memory labeling:
PASS / FAIL

Operation 7 Cycle missing-ref/no-link truthful state:
PASS / FAIL / BLOCKED_FIXTURE_GAP

Operation 8 NextAction empty/NONE truthful state:
PASS / FAIL / BLOCKED_FIXTURE_GAP

Operation 9 Project current-authority failure gating:
PASS / FAIL
실제 문구:
<기록>

Operation 10 Cycle / NextAction endpoint-local failure retained/stale:
NextAction PASS / FAIL
Cycle PASS / FAIL
실제 NextAction 문구:
<기록>
실제 Cycle 문구:
<기록>

Operation 11 retained/stale → current recovery:
PASS / FAIL
실제 복구 문구:
<기록 또는 없음>

Operation 12 304 / no-change behavior:
PASS / FAIL
304 actual network status:
OBSERVED / NOT_OBSERVED

Operation 13 Transition / Execution regression:
PASS / FAIL
DENIED actual instance:
OBSERVED / NOT_OBSERVED

Operation 14 Evidence / Human / Judgment regression:
PASS / FAIL

Operation 15 visible 10-second polling:
PASS / FAIL

Operation 16 hidden polling stop:
PASS / FAIL

Operation 17 visible polling resume:
PASS / FAIL

Operation 18 terminal polling stop:
PASS / FAIL

Operation 19 responsive 1080:
PASS / FAIL

Operation 20 responsive 1280:
PASS / FAIL

Operation 21 responsive 1440:
PASS / FAIL

Operation 22 approximately 1080 × 910 density:
PASS / FAIL
first viewport에서 보이는 범위:
<기록>
과도한 vertical density:
YES / NO
개선 필요 의견:
<기록 또는 없음>

Mutation UI:
ABSENT / OBSERVED

Mutation request POST/PUT/PATCH/DELETE:
ABSENT / OBSERVED

추가 관찰:
- 없음
```

---

# 6. FAIL / BLOCKED 발생 시 추가 기록

FAIL 항목에는 가능하면 아래만 추가한다.

```text
URL:
viewport width/height:
문제가 발생한 영역:
실제로 보인 상태:
기대 상태:
재현 순서:
Network request/status if relevant:
```

Screenshot은 있으면 도움이 되지만 필수는 아니다.

분류:

```text
actual UI/behavior defect
→ FAIL / REWORK_REQUIRED

server / local prerequisite unavailable only
→ BLOCKED_ENVIRONMENT

required safe fixture case unavailable
→ BLOCKED_FIXTURE_GAP
```

`BLOCKED_ENVIRONMENT` 또는 `BLOCKED_FIXTURE_GAP`을 source defect로 자동 승격하지 않는다.

---

# 7. QA 이후 cleanup

Human QA 결과를 기록한 뒤에만 **이번 Human QA가 생성한 runtime residue만** 정리한다.

정리 대상:

```text
Human QA AISCC server process
exact Human QA PostgreSQL container: aiscc-p2-1e-human-qa
Human QA shell의 AISCC_DATABASE_URL
Human QA shell의 AISCC_TEST_DATABASE_URL
Human QA shell의 PYTHONDONTWRITEBYTECODE
```

확인:

```text
127.0.0.1:<QA server port> listener absent
127.0.0.1:<QA DB port> listener absent
exact container aiscc-p2-1e-human-qa absent
```

금지:

```text
unrelated Docker container/image/volume cleanup
git clean/reset/restore/checkout/stash
broad __pycache__ cleanup
candidate source cleanup
0020 Cycle/Handoff cleanup
```

Known ignored mypy cache residue는 이번 Human QA cleanup 범위가 아니다.

---

# 8. Human result ceiling / 다음 Command Center 행동

모든 required Operation이 PASS이고 required fixture gap이 없으면:

```text
Human result:
HUMAN_PROVIDED / PASS

P2-1E:
HUMAN_PROVIDED / ACCEPTED candidate
```

그 다음 Browser Command Center가 **새 substantive judgment**를 수행한다.
그 judgment 전에는 persistence/closure를 시작하지 않는다.

UI/behavior defect가 있으면:

```text
HOLD_REWORK_REQUIRED
```

으로 판정하고 새 timestamp rework lineage를 발행한다.

Human QA PASS만으로 다음을 수행하지 않는다.

```text
P2-1 CLOSED
P2-2 STARTED
Git persistence
public release/deployment
```

---

# 9. 보존 provenance

Human machine에 아래 0020 provenance가 canonical repository path에 있어야 한다.

```text
.aiassistant/records/aiscc/cycles/20260908_0020_aiscc-p2-1e-implementation-runtime-candidate-accepted-human-qa-pending-1.cycle.md

.aiassistant/reports/aiscc/20260908_0020_aiscc-browser-command-center-p2-1e-candidate-accepted-human-qa-entry-handoff-1.md
```

이번 Human QA guide의 later canonical preservation target:

```text
.aiassistant/tasks/done/20260908_0051_aiscc-p2-1e-human-integrated-browser-qa-operation-guide-1.md
```

Human QA 결과가 제출되기 전에는 이 guide 자체가 P2-1E acceptance evidence가 아니다.
