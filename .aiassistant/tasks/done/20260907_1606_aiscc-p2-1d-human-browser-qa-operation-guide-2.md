# P2-1D Human Browser QA — Operation Guide

## 문서 목적

이 문서는 **사람이 Browser에서 직접 수행하는 QA 절차서**다.

```text
work_type: HUMAN_QA_GATE
owner: Human
executor: NOT_APPLICABLE
short Executor prompt: NOT_REQUIRED
```

IDE Executor에 전달하지 않는다.

현재 P2-1D는 아래 상태다.

```text
SOURCE_STATIC_ACCEPTED
RUNTIME_EVIDENCE_ACCEPTED
HUMAN_BROWSER_QA_PENDING
NOT_PERSISTED
```

이번 QA에서 source 수정, DB 수정, Git 작업은 하지 않는다.

---

# QA 대상

## Primary — ACCEPTED WorkRun

```text
http://127.0.0.1:8765/command-center/work-runs/cc-accepted-21588967e0a74d2aa708f2a9fb7a83df
```

## Empty State — READY WorkRun

```text
http://127.0.0.1:8765/command-center/work-runs/cc-no-attempt-21588967e0a74d2aa708f2a9fb7a83df
```

## Polling — BLOCKED WorkRun

```text
http://127.0.0.1:8765/command-center/work-runs/cc-blocked-21588967e0a74d2aa708f2a9fb7a83df
```

Browser Zoom:

```text
100%
```

---

# Operation 1 — 서버 접속 확인

## 수행

1. Primary URL을 연다.
2. 새로고침한다.

## PASS

- 화면이 정상 표시된다.
- `127.0.0.1:8765` 접속 오류가 없다.
- WorkRun detail 화면이 열린다.

## 접속이 안 되면

```text
BLOCKED_ENVIRONMENT
```

으로 보고하고 QA를 중단한다.

이 경우 source defect로 판단하지 않는다.

---

# Operation 2 — 전체 화면 구조 확인

대상:

```text
Primary ACCEPTED WorkRun
```

## 확인할 영역

화면을 위에서 아래까지 확인한다.

기존 영역:

```text
WorkRun / Task
WorkflowState / state_version
RuntimeMode
Transition
Execution
```

P2-1D 추가 영역:

```text
Evidence
Human / Judgment
```

## PASS

- 모두 하나의 WorkRun detail 화면 안에 있다.
- Evidence/Human 때문에 별도 경쟁 detail 화면으로 분리되지 않는다.
- Transition / Execution / Evidence / Human 영역이 서로 구분된다.
- 화면은 조회 전용으로 보인다.

---

# Operation 3 — Evidence 구분 확인

대상:

```text
Primary ACCEPTED WorkRun
```

## 확인할 항목

화면에서 아래 항목들을 찾는다.

```text
EvidenceRequirement
EvidenceCandidate
EvidenceAdmissionDecision
AdmittedEvidence
```

## PASS

다음이 눈으로 구분되어야 한다.

```text
EvidenceRequirement != EvidenceCandidate
EvidenceCandidate != AdmittedEvidence
```

추가 확인:

- Candidate가 곧 승인된 Evidence처럼 보이지 않는다.
- Admission Decision이 최종 Judgment처럼 보이지 않는다.
- 긴 ID 때문에 글자가 겹치거나 카드가 깨지지 않는다.
- owner / type / channel / provenance 정보가 있다면 읽을 수 있다.

---

# Operation 4 — Evidence 충족 결과 확인

대상:

```text
Primary ACCEPTED WorkRun
```

## 확인할 항목

```text
RequirementSatisfaction
EvidenceSetEvaluation
EvidenceSetAttestation
```

## PASS

다음 의미가 서로 구분되어 보여야 한다.

```text
개별 Requirement 충족
!=
전체 Evidence Set 평가
!=
Attestation
```

추가 확인:

- `UNSATISFIED`가 곧 WorkRun 실패처럼 보이지 않는다.
- hash / root / attestation ID가 너무 길어도 layout이 깨지지 않는다.

---

# Operation 5 — Human / Judgment 구분 확인

대상:

```text
Primary ACCEPTED WorkRun
```

## 확인할 항목

```text
HumanGate
HumanResult
Judgment
Transition Effect
```

## PASS

4개가 서로 다른 의미로 보여야 한다.

```text
HumanGate
!= HumanResult
!= Judgment
!= Transition Effect
```

특히 확인:

- HumanResult가 곧 Judgment처럼 보이지 않는다.
- Judgment가 곧 WorkflowState처럼 보이지 않는다.
- Transition Effect가 Judgment와 별도 의미로 보인다.
- 하나의 generic status로 합쳐져 있지 않는다.

---

# Operation 6 — 데이터 없음 상태 확인

대상:

```text
READY WorkRun
```

URL:

```text
http://127.0.0.1:8765/command-center/work-runs/cc-no-attempt-21588967e0a74d2aa708f2a9fb7a83df
```

## 확인

Evidence / Execution / Human / Judgment 중 아직 데이터가 없는 영역을 본다.

## PASS

- `undefined`
- `null`
- 깨진 빈 table
- 의미 없는 빈 카드

가 보이지 않는다.

대신 사람이 이해할 수 있는 `없음`, `아직 없음`, empty state 형태로 보여야 한다.

또한:

- 데이터가 없다고 실패로 표시하지 않는다.
- 존재하지 않는 Judgment나 HumanResult를 만들어서 표시하지 않는다.

---

# Operation 7 — 반응형 확인

대상:

```text
Primary ACCEPTED WorkRun
```

Browser Zoom:

```text
100%
```

확인 width:

```text
1080
1280
1440
```

DevTools responsive mode 또는 Browser 창 크기를 사용한다.

## 각 width에서 PASS 확인

- 페이지 전체에 불필요한 가로 스크롤이 없다.
- 카드나 글자가 서로 겹치지 않는다.
- 긴 ID가 옆 영역을 침범하지 않는다.
- Evidence 영역을 읽을 수 있다.
- HumanGate / HumanResult / Judgment / Transition Effect를 구분할 수 있다.
- Transition / Execution 기존 영역도 깨지지 않는다.

결과는 아래처럼 기록한다.

```text
1080: PASS / FAIL
1280: PASS / FAIL
1440: PASS / FAIL
```

---

# Operation 8 — 기존 Transition / Execution 회귀 확인

대상:

```text
Primary ACCEPTED WorkRun
```

## 확인

기존 P2-1C 영역을 다시 본다.

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

- 기존 정보가 사라지지 않았다.
- P2-1D 추가 영역 때문에 깨지지 않았다.
- `EXECUTOR_COMPLETED`가 WorkRun `ACCEPTED`와 같은 의미처럼 보이지 않는다.

### DENIED 표시

실제 DENIED fixture가 있으면 확인한다.

없으면:

```text
DENIED actual instance: NOT_OBSERVED
```

로 기록한다.

DENIED 확인을 위해 DB 데이터를 만들거나 수정하지 않는다.

---

# Operation 9 — 화면이 보이는 상태에서 Polling 확인

대상:

```text
BLOCKED WorkRun
```

URL:

```text
http://127.0.0.1:8765/command-center/work-runs/cc-blocked-21588967e0a74d2aa708f2a9fb7a83df
```

## 수행

1. DevTools를 연다.
2. `Network` 탭을 연다.
3. Network log를 지운다.
4. 현재 QA 탭을 화면에 계속 보이게 둔다.
5. 약 `25초` 관찰한다.

## PASS

- 자동 GET 요청이 반복된다.
- 대략 10초 단위 polling이 보인다.
- polling 중 화면이 깜빡이거나 비어버리지 않는다.
- 요청은 조회용 GET이다.

---

# Operation 10 — 숨긴 탭에서 Polling 중지 확인

Operation 9에 이어서 수행한다.

## 수행

1. Network log를 지운다.
2. 다른 Browser 탭으로 이동한다.
3. QA 탭을 약 `25초` 숨긴 상태로 둔다.
4. 다시 QA 탭으로 돌아온다.

## PASS

- 숨긴 동안 polling GET이 계속 반복되지 않는다.
- 탭 전환 직전에 시작된 요청 1건 정도는 허용한다.
- 하지만 10초 단위 요청이 계속 누적되면 FAIL이다.

---

# Operation 11 — 다시 보이는 탭에서 Polling 재개 확인

Operation 10 직후 수행한다.

## 수행

1. QA 탭을 다시 화면에 표시한다.
2. Network를 본다.
3. 최대 약 `15초` 관찰한다.

## PASS

- page reload 없이 polling이 다시 시작된다.
- 요청이 한꺼번에 여러 개 폭증하지 않는다.
- 화면의 기존 데이터가 유지된다.

---

# Operation 12 — Terminal WorkRun Polling 중지 확인

대상:

```text
Primary ACCEPTED WorkRun
```

## 수행

1. Primary URL을 다시 연다.
2. Network log를 지운다.
3. 약 `25초` 관찰한다.

## PASS

- 최초 조회 후 10초 polling이 반복되지 않는다.
- Terminal WorkRun에서는 자동 polling이 멈춘다.
- 수동 새로고침은 가능하다.

---

# Operation 13 — Summary 조회 실패 화면 확인

대상:

```text
BLOCKED WorkRun
```

이 Operation은 **DB나 source를 수정하지 않고 Browser DevTools만 사용**한다.

## 수행

1. BLOCKED WorkRun을 정상적으로 먼저 연다.
2. 모든 영역이 표시된 것을 확인한다.
3. DevTools → Network에서 아래 요청을 찾는다.

```text
GET /v1/command-center/work-runs/cc-blocked-21588967e0a74d2aa708f2a9fb7a83df
```

4. 해당 요청을 우클릭한다.
5. `Block request URL`을 선택한다.
6. 자동 polling이 한 번 이상 발생할 때까지 기다린다.

## PASS

- 조회 실패 메시지가 화면에 표시된다.
- 기존에 성공적으로 표시되던 데이터가 즉시 사라지지 않는다.
- 실패 후 retained data를 `최신 상태`라고 잘못 표시하지 않는다.
- stale / retained 의미가 분명하다.

이전 accepted 의미 기준:

```text
조회 오류
읽기 요청을 안전하게 완료하지 못했습니다.
마지막으로 성공한 snapshot을 유지하며 새 현재 상태로 표시하지 않습니다.
```

실제 화면 문구가 다르면 **실제 문구를 그대로 기록**한다.

---

# Operation 14 — Summary 조회 복구 확인

Operation 13에 이어서 수행한다.

## 수행

1. `Block request URL`을 해제한다.
2. 자동 polling을 기다리거나 수동 새로고침한다.

## PASS

- 정상 조회로 복구된다.
- stale/error 상태가 해제된다.
- 기존 화면과 현재 화면 사이에 이상한 중복이나 역전이 없다.

실제 복구 안내 문구가 있다면 그대로 기록한다.

---

# Operation 15 — Evidence endpoint만 실패시키기

대상:

```text
BLOCKED WorkRun
```

## 수행

1. 정상 화면에서 Evidence 영역이 표시되는 것을 먼저 확인한다.
2. DevTools → Network에서 아래 요청을 찾는다.

```text
GET /v1/command-center/work-runs/cc-blocked-21588967e0a74d2aa708f2a9fb7a83df/evidence
```

3. 해당 요청만 `Block request URL` 한다.
4. Summary 요청은 막지 않는다.
5. polling이 한 번 이상 발생할 때까지 기다린다.

## PASS

- 페이지 전체가 실패하지 않는다.
- 다른 정상 영역은 계속 표시된다.
- Evidence 영역은 마지막 성공 데이터를 유지하거나 실패 상태를 명확히 표시한다.
- Evidence를 빈 값으로 조용히 덮어쓰지 않는다.
- stale Evidence를 current/latest처럼 표시하지 않는다.

실제 오류 문구가 있다면 그대로 기록한다.

---

# Operation 16 — Evidence endpoint 복구 확인

Operation 15에 이어서 수행한다.

## 수행

1. Evidence endpoint block을 해제한다.
2. 자동 polling 또는 수동 새로고침한다.

## PASS

- Evidence가 정상적으로 다시 표시된다.
- 중복 카드나 중복 row가 생기지 않는다.
- error/stale 표시가 정상 상태로 돌아온다.

---

# Operation 17 — Mutation UI가 없는지 확인

Primary / READY / BLOCKED 세 화면을 둘러본다.

## 없어야 하는 기능

```text
state 변경
transition 승인/거부
evidence admit/reject
HumanResult 제출
Judgment 승인/거부/rework
terminal 상태 변경
```

## PASS

사용자가 authoritative 상태를 변경하는 control이 없다.

허용:

```text
조회
navigation
manual refresh
```

---

# Operation 18 — Network Mutation 요청이 없는지 확인

QA를 진행하면서 Network 탭을 확인한다.

## PASS

정상 UI 동작 중 다음 method가 없어야 한다.

```text
POST
PUT
PATCH
DELETE
```

자동 polling과 수동 refresh는 GET이어야 한다.

---

# 최종 결과 제출 양식

QA가 끝나면 아래 형식으로 Browser Command Center 채팅에 붙여넣는다.

```text
P2-1D Human Browser QA

Operation 1 서버 접속:
PASS / BLOCKED_ENVIRONMENT

Operation 2 전체 화면 구조:
PASS / FAIL

Operation 3 Evidence 구분:
PASS / FAIL

Operation 4 Evidence 충족 결과:
PASS / FAIL

Operation 5 Human / Judgment 구분:
PASS / FAIL

Operation 6 Empty State:
PASS / FAIL

Operation 7 반응형:
1080 PASS / FAIL
1280 PASS / FAIL
1440 PASS / FAIL

Operation 8 Transition / Execution 회귀:
PASS / FAIL
DENIED actual instance:
OBSERVED / NOT_OBSERVED

Operation 9 Visible polling:
PASS / FAIL

Operation 10 Hidden polling stop:
PASS / FAIL

Operation 11 Visible polling resume:
PASS / FAIL

Operation 12 Terminal polling stop:
PASS / FAIL

Operation 13 Summary failure:
PASS / FAIL
실제 문구:
<여기에 기록>

Operation 14 Summary recovery:
PASS / FAIL
실제 문구:
<여기에 기록>

Operation 15 Evidence endpoint failure:
PASS / FAIL
실제 문구:
<여기에 기록>

Operation 16 Evidence recovery:
PASS / FAIL

Operation 17 Mutation UI 없음:
PASS / FAIL

Operation 18 Mutation request 없음:
PASS / FAIL

추가 관찰:
- 없음
```

---

# FAIL이 발생한 경우 추가 기록

FAIL 항목에는 가능하면 아래만 추가한다.

```text
WorkRun:
화면 width:
문제가 발생한 영역:
실제로 보인 상태:
기대 상태:
재현 순서:
```

Screenshot은 있으면 도움이 되지만 필수는 아니다.

---

# QA 이후

모든 필수 Operation PASS:

```text
Human result:
HUMAN_PROVIDED / PASS
```

실제 UI 결함 발견:

```text
FAIL / REWORK_REQUIRED
```

서버만 접속 불가:

```text
BLOCKED_ENVIRONMENT
```

이번 QA가 끝나기 전까지 P2-1D Git persistence는 진행하지 않는다.
