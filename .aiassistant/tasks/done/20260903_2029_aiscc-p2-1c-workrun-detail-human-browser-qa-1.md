# Human QA Task: P2-1C WorkRun Detail Browser / Visual / Polling

## meta

- task_id: `20260903_2029_aiscc-p2-1c-workrun-detail-human-browser-qa-1`
- created_at: `2026-09-03T20:29:00+09:00`
- project: `AI Software Command Center (AISCC)`
- phase: `P2-1C`
- work_type: `QA_ONLY / HUMAN_VERIFICATION`
- owner: `Human`
- execution_mode: `MANUAL_COMMAND_CENTER`
- source/runtime candidate aggregate: `2e4ca49afcd074aa2eac768b6f966d3d48044067917328a35c7839e078b35af3`
- predecessor Browser judgment:
  `.aiassistant/records/aiscc/cycles/20260903_2029_aiscc-p2-1c-stale-authority-rework-source-runtime-acceptance-human-qa-entry-1.cycle.md`
- current state: `SOURCE_RUNTIME_ACCEPTED_CANDIDATE / HUMAN_QA_OPENED`
- P2-1D: `NOT_STARTED / DO NOT START`

## 목적

이번 Task는 IDE Executor 작업이 아니다.

Human이 실제 브라우저에서 P2-1C WorkRun 상세 화면의:

- 정보 계층;
- domain semantics;
- navigation;
- responsive layout;
- polling;
- stale/current refresh-failure presentation

을 검증하는 Human QA Gate다.

이 Task를 다운로드하여 수행하고 결과를 Browser Command Center에 제출한다.

## 검증 기준 환경

- Browser: Chrome
- Zoom: `100%`
- viewport widths:
  - `1080`
  - `1280`
  - `1440`
- current source/runtime candidate:
  `2e4ca49afcd074aa2eac768b6f966d3d48044067917328a35c7839e078b35af3`
- current P2-1C working tree 사용
- source 수정 금지
- Git commit/push/deployment 금지

가능하면 아래 두 종류 WorkRun을 사용한다.

1. nonterminal WorkRun
   - polling 관찰용
2. terminal WorkRun
   - `ACCEPTED`, `REJECTED`, 또는 `FAILED`
   - terminal polling stop 관찰용

가능하면 transition 기록에:

```text
ADMITTED
DENIED
```

가 모두 보이는 WorkRun을 사용한다.

가능하면 execution 기록에:

```text
EXECUTOR_COMPLETED
```

attempt가 존재하는 WorkRun을 사용한다.

## Operation 1 — Queue → WorkRun Detail → Project navigation

### 절차

1. Command Center project queue를 연다.
2. WorkRun row/card의 `WorkRun 상세` 진입 동작을 사용한다.
3. WorkRun 상세 화면이 열린 것을 확인한다.
4. 상세 화면에서 `프로젝트 큐로` navigation을 사용한다.
5. 다시 상세로 진입해 동일 WorkRun context가 정상 표시되는지 확인한다.

### PASS 기대

- queue → detail navigation이 명확하다.
- detail 화면의 WorkRun ID가 선택한 WorkRun과 일치한다.
- project navigation이 올바른 project queue로 돌아간다.
- navigation 때문에 layout이 깨지거나 horizontal page pan이 생기지 않는다.
- mutation/approval/rework/reject control은 보이지 않는다.

## Operation 2 — WorkRun detail hierarchy / current state / Task-Scope

### 절차

WorkRun 상세 상단부터 아래 순서로 읽는다.

- 현재 상태
- Task / 범위
- blocker — 존재할 때
- 전이 기록
- 실행 기록

### PASS 기대

사람이 화면만 보고 최소 다음을 구분할 수 있다.

```text
WorkRun
TaskContract
WorkflowState
state_version
RuntimeMode
Task / Scope availability
blocker
```

- 내부 identifier와 사용자용 설명이 뒤섞여 읽기 어렵지 않다.
- 긴 ID/ref가 레이아웃을 밀어내지 않는다.
- 중요한 상태와 기술 세부정보의 시각적 계층이 식별 가능하다.

## Operation 3 — Transition semantics: ADMITTED vs DENIED

### 절차

transition이 있는 WorkRun에서 전이 기록을 읽는다.

가능하면 `ADMITTED`와 `DENIED`가 모두 있는 run을 사용한다.

### PASS 기대

- `TransitionRequest`
- evaluation / guards
- `TransitionDecision`

이 서로 다른 의미로 보인다.

특히 `DENIED`는:

```text
성공한 state transition
```

처럼 오해되지 않는다.

화면에서 다음 의미가 이해 가능해야 한다.

```text
DENIED
→ 요청/평가/결정 기록은 존재
→ authoritative state를 성공적으로 변경한 전이는 아님
```

`ADMITTED`와 `DENIED`가 색상 하나만으로 구분되지 않고 text semantics도 존재해야 한다.

## Operation 4 — Execution semantics / readability

### 절차

execution attempt와 operation이 있는 WorkRun을 읽는다.

### PASS 기대

- attempt와 operation 계층을 구분할 수 있다.
- `ExecutionStatus`를 읽을 수 있다.
- `EXECUTOR_COMPLETED`가 보이는 경우 아래 의미가 명확하다.

```text
EXECUTOR_COMPLETED
!=
WorkRun ACCEPTED
```

- execution 정보가 transition 정보와 혼동되지 않는다.
- 긴 operation/resource/ref 값이 layout을 파괴하지 않는다.

## Operation 5 — Responsive visual QA

각 viewport에서 Zoom `100%`로 Operation 2~4 화면을 다시 확인한다.

### 1080

PASS:

- 전체 page horizontal pan 없음
- WorkRun summary/Task/transition/execution 주요 내용이 viewport 안에서 읽을 수 있음
- transition columns가 무의미하게 겹치거나 잘리지 않음
- 긴 identifier가 card/container 밖으로 돌출되지 않음
- button/link가 겹치거나 화면 밖으로 밀리지 않음

### 1280

PASS:

- 동일 조건 PASS
- 정보 밀도와 여백이 과도하게 압축되거나 벌어지지 않음

### 1440

PASS:

- 동일 조건 PASS
- content가 지나치게 넓게 늘어나 가독성을 잃지 않음
- hierarchy가 1080/1280과 의미적으로 동일함

각 width에서 FAIL이 있으면:

- exact viewport
- 화면 위치/section
- 보이는 문제
- 가능하면 screenshot

을 기록한다.

## Operation 6 — visible nonterminal polling / hidden-tab stop / resume

### 준비

nonterminal WorkRun 상세를 연다.

Chrome DevTools → Network를 열고 현재 WorkRun의 세 read endpoint를 관찰한다.

```text
GET /v1/command-center/work-runs/{work_run_id}
GET /v1/command-center/work-runs/{work_run_id}/transitions
GET /v1/command-center/work-runs/{work_run_id}/execution
```

### 6-A visible polling

1. 탭을 visible 상태로 둔다.
2. initial load 이후 약 20~25초 관찰한다.

PASS:

- nonterminal WorkRun이면 세 endpoint refresh가 약 10초 cadence로 반복된다.
- refresh 때문에 화면 scroll/focus가 튀지 않는다.
- mutation request가 발생하지 않는다.

### 6-B hidden tab stop

1. Network log를 확인한 후 다른 browser tab으로 이동한다.
2. 최소 15초 이상 현재 WorkRun tab을 hidden 상태로 둔다.
3. 다시 WorkRun tab으로 돌아오기 전에 request 발생 여부를 확인한다.

PASS:

- hidden 상태에서 반복 polling이 계속되지 않는다.

### 6-C visible resume

1. WorkRun tab으로 돌아온다.
2. Network와 화면을 확인한다.

PASS:

- visible 복귀 후 detail refresh가 재개된다.
- screen focus/scroll가 부자연스럽게 초기화되지 않는다.
- 이후 nonterminal이면 polling이 다시 이어진다.

## Operation 7 — terminal WorkRun polling stop

### 절차

`ACCEPTED`, `REJECTED`, 또는 `FAILED` WorkRun 상세를 연다.

Network에서 initial 세 endpoint load 이후 15초 이상 관찰한다.

### PASS 기대

terminal WorkRun에서는 지속적인 10초 polling이 반복되지 않는다.

수동 새로고침은 여전히 동작할 수 있다.

## Operation 8 — retained stale/current refresh-failure presentation

이 Operation은 이번 rework의 핵심 Human QA다.

### 준비

1. transition/execution 데이터가 보이는 WorkRun 상세를 정상 load한다.
2. 정상 상태에서 section copy를 확인한다.

정상 예:

```text
최신 전이 기록
최신 실행 기록
```

또는 current/unchanged 의미의 정상 copy.

### failure 재현

가장 간단한 방법:

1. Chrome DevTools → Network에서 `Offline`을 켠다.
2. `수동 새로고침`을 누른다.
3. refresh failure 상태의 화면을 확인한다.

이 방법은 세 endpoint 전체를 실패시키므로 source-level concurrent-success suppression 자체를 증명하는 시험은 아니다.
이번 Human QA에서는 stale/current **표현**을 검증한다.

### PASS 기대

이전 성공 transition/execution DOM을 유지하는 경우:

- 이전 내용이 계속 보일 수 있다.
- 하지만 section label에 `최신` 의미가 남아서는 안 된다.
- 다음과 같은 stale/retained/last-successful semantics가 명확해야 한다.

```text
마지막 성공 ...
새로고침 실패 ...
과거 snapshot ...
```

page-level read state 역시 새 current snapshot을 확정하지 못했다는 의미와 모순되지 않아야 한다.

특히 아래 조합은 FAIL이다.

```text
page:
현재 snapshot 확정 실패

section:
최신 전이 기록
최신 실행 기록
```

### recovery

1. DevTools Network를 다시 `Online`으로 바꾼다.
2. 수동 새로고침한다.

PASS:

- current authority가 다시 성공하면 정상 current detail을 표시한다.
- transition/execution section copy가 다시 current/latest 의미로 복원된다.
- stale warning이 영구 고착되지 않는다.

## 전체 PASS 기준

다음이 모두 PASS여야 한다.

```text
Operation 1 PASS
Operation 2 PASS
Operation 3 PASS
Operation 4 PASS
Operation 5 — 1080 PASS
Operation 5 — 1280 PASS
Operation 5 — 1440 PASS
Operation 6-A PASS
Operation 6-B PASS
Operation 6-C PASS
Operation 7 PASS
Operation 8 failure PASS
Operation 8 recovery PASS
```

## 즉시 FAIL / REWORK 후보

- `DENIED`가 성공 전이처럼 보임
- `EXECUTOR_COMPLETED`가 WorkRun accepted처럼 보임
- 1080/1280/1440 중 page-level horizontal pan 또는 주요 section overlap
- hidden tab에서 polling이 계속됨
- terminal WorkRun에서 지속 polling이 계속됨
- refresh failure 뒤 retained stale data가 `최신`으로 계속 표시됨
- offline→online recovery 뒤 stale label이 정상 current 상태로 복원되지 않음
- queue/detail/project navigation이 잘못된 context로 이동
- mutation control이 노출됨

## 결과 제출 형식

Browser Command Center에 아래 형식으로 제출한다.

```text
Human P2-1C browser QA

Browser:
Chrome

Zoom:
100%

Operation 1 navigation:
PASS / FAIL
notes:

Operation 2 hierarchy:
PASS / FAIL
notes:

Operation 3 ADMITTED/DENIED:
PASS / FAIL
notes:

Operation 4 execution semantics:
PASS / FAIL
notes:

Operation 5 1080:
PASS / FAIL
notes:

Operation 5 1280:
PASS / FAIL
notes:

Operation 5 1440:
PASS / FAIL
notes:

Operation 6-A visible polling:
PASS / FAIL
notes:

Operation 6-B hidden stop:
PASS / FAIL
notes:

Operation 6-C visible resume:
PASS / FAIL
notes:

Operation 7 terminal polling stop:
PASS / FAIL
notes:

Operation 8 stale failure presentation:
PASS / FAIL
notes:

Operation 8 recovery:
PASS / FAIL
notes:

Overall:
PASS / FAIL
```

FAIL이 있으면 screenshot을 함께 제출해도 된다.

## 결과 이후

Human QA 전체 PASS:

```text
→ Browser Command Center final P2-1C judgment
→ 아직 자동 commit 금지
→ final acceptance/persistence 단계 판정
```

Human QA 하나라도 substantive FAIL:

```text
→ P2-1C HOLD_REWORK_REQUIRED
→ 새 timestamp rework Task
```

P2-1D는 P2-1C final acceptance/persistence 전까지 시작하지 않는다.
