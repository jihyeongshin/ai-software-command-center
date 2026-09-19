# Human QA Gate — AISCC Public-Site Smoke

## meta

- qa_id: `20260919_2133_aiscc-p3-3-l8-human-public-site-smoke-qa-1`
- gate_type: `HUMAN_QA_GATE`
- executor: `HUMAN`
- IDE_Executor: `DO_NOT_USE`
- short_prompt: `NOT_REQUIRED`
- public_url: `https://aiscc-replay.pages.dev/`
- expected_release_main: `b821b1ed677ad6d8b93ab1d6b5090218471bd925`
- expected_release_state: `PUBLIC_LIVE_RELEASED`
- live_run_authority_for_this_QA: `EXACTLY_ONE_HUMAN_START_CLICK`

## 목적

실제 공개 브라우저에서 최종 release UI가 정상 노출되고,
사람이 `Start bounded Live`를 한 번 실행했을 때 동일 탭에서
Public Live가 정상적으로 terminal `COMPLETED`까지 표시되는지 확인한다.

이 QA는 browser/visual/useability evidence다.

Backend를 수정하거나 IDE Executor를 실행하는 작업이 아니다.

## 테스트 환경

권장:

```text
Browser:
Chrome

Zoom:
100%

Session:
새 Incognito 창 또는 기존 AISCC sessionStorage가 없는 새 브라우저 세션

URL:
https://aiscc-replay.pages.dev/
```

DevTools는 필요하지 않다.

read capability, idempotency key, cookie, request header/token을 복사하거나 제출하지 않는다.

## 중요한 실행 제한

이번 Human QA에서 Live 시작 버튼은 **정확히 한 번만 클릭**한다.

실패/오류/timeout이 발생해도:
- Retry 버튼을 누르지 않는다.
- 새 탭에서 다시 실행하지 않는다.
- 새 Live run을 만들지 않는다.
- 보이는 상태를 그대로 기록하고 STOP한다.

페이지의 Recorded Replay 항목을 보는 것은 추가 Live run을 만들지 않는다.

## Operation 1 — 공개 페이지 접속

`https://aiscc-replay.pages.dev/` 접속.

PASS 기준:
- 페이지가 정상 렌더링된다.
- 브라우저 자체 오류/Cloudflare 오류 페이지가 아니다.
- Recorded Run Replay 영역과 Bounded Live 영역이 보인다.

결과:

`PASS / FAIL`

## Operation 2 — Recorded Replay 유지 확인

Recorded Replay catalog가 정상 보이는지 확인한다.

PASS 기준:
- 기존 네 개 recorded scenario가 보인다.
- 그중 하나를 선택했을 때 recorded detail이 정상 표시된다.
- 문구가 이것이 live execution이 아니라 recorded replay임을 구분한다.

이 단계에서는 Live 시작 버튼을 누르지 않는다.

결과:

`PASS / FAIL`

## Operation 3 — Live release UI 확인

Bounded Live 영역 확인.

PASS 기준:
- release note가 Live가 이 release에 구성되어 있음을 나타낸다.
- `Start bounded Live` 버튼이 활성화되어 있다.
- Replay가 계속 사용 가능하다는 안내가 보인다.
- Live unavailable / Live is not enabled 문구가 아니다.

결과:

`PASS / FAIL`

## Operation 4 — Human Live 시작

`Start bounded Live` 버튼을 **한 번만 클릭**한다.

PASS 기준:
- submission 진행 상태가 표시된다.
- 동일 탭에서 하나의 Live session으로 전환된다.
- 새로운 오류 페이지로 이동하지 않는다.

클릭 횟수:

`1`

결과:

`PASS / FAIL`

## Operation 5 — terminal 상태 대기

아무 버튼도 추가로 누르지 말고 자동 polling을 기다린다.

현재 frontend는 약 3초 간격, 최대 40 polls의 bounded polling을 사용한다.

PASS 기준:
- 최종 `Server status` 영역이 나타난다.
- `Run state`가 `COMPLETED`가 된다.
- 자동 status update가 terminal state에서 중단되었다는 안내가 보인다.
- error/unavailable 상태로 끝나지 않는다.

보이는 Run ID는 제출해도 된다.

read capability는 제출하지 않는다.

결과:

`PASS / FAIL`

Run ID:

`<visible run id>`

최종 Run state:

`<visible state>`

## Operation 6 — public projection identity 확인

terminal Server status에서 확인:

```text
Mode:
PUBLIC_BOUNDED_LIVE

Scenario / version:
stockroom-s1-normal / 1.0.0
```

PASS 기준:
- 위 두 값이 정확하다.
- Reason이 실패 reason으로 표시되지 않는다.

현재 public projection은 raw provider output을 공개하지 않는 경계를 사용한다.

따라서 raw OpenAI response/output가 화면에 보이지 않는 것은 FAIL 사유가 아니다.

결과:

`PASS / FAIL`

## Operation 7 — Replay와 Live의 공존 확인

Live가 `COMPLETED`된 후 Recorded Replay scenario 하나를 다시 선택한다.

PASS 기준:
- Recorded Replay가 여전히 정상 동작한다.
- Replay 선택이 새 Live run을 만들지 않는다.
- Live terminal 상태와 Recorded Replay가 서로 구분되어 보인다.

Live를 다시 시작하지 않는다.

결과:

`PASS / FAIL`

## Operation 8 — 기본 시각/사용성 확인

같은 화면에서 확인:

PASS 기준:
- 주요 글자가 겹치거나 잘리지 않는다.
- Live 버튼/상태/Run state를 읽을 수 있다.
- 심각한 horizontal overflow나 깨진 layout이 없다.
- Live와 Recorded Replay를 사용자가 구분할 수 있다.

이 Gate는 새 디자인 평가가 아니라 release-blocking visual smoke다.
사소한 취향 차이는 FAIL 사유가 아니다.

결과:

`PASS / FAIL`

## 제출 형식

아래 형식으로 이 Browser Command Center 채팅에 그대로 제출한다.

```text
Human Public-Site Smoke

Operation 1 공개 페이지 접속:
PASS / FAIL

Operation 2 Recorded Replay:
PASS / FAIL

Operation 3 Live release UI:
PASS / FAIL

Operation 4 Human Live 시작:
PASS / FAIL
클릭 횟수: 1

Operation 5 terminal 상태:
PASS / FAIL
Run ID: <visible run id>
최종 Run state: <visible state>

Operation 6 projection identity:
PASS / FAIL
Mode: <visible value>
Scenario / version: <visible value>

Operation 7 Replay/Live 공존:
PASS / FAIL

Operation 8 시각/사용성:
PASS / FAIL

추가 관찰:
<없으면 없음>
```

가능하면 terminal `COMPLETED` 상태의 Live 영역 스크린샷 1장을 함께 첨부한다.

스크린샷에는 브라우저 DevTools/Network/Storage를 포함하지 않는다.

## 판정 규칙

모든 Operation PASS:

`HUMAN_PUBLIC_SITE_SMOKE_PASS`

하나라도 FAIL:

`HUMAN_PUBLIC_SITE_SMOKE_FAIL`

FAIL이면 재시도하지 말고 결과를 제출한다.

Browser Command Center가 다음 조치를 판정한다.

## 다음 단계

PASS 후:

```text
Human QA evidence admission
→ Browser terminal L8 judgment
→ final Cycle/Handoff
```

이 QA 자체는 L8을 자동으로 닫지 않는다.
