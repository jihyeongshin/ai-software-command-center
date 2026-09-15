# Human Task: P3-3 Wanted AI Championship 2026 최종 폼 검토 및 제출

## 현재 상태

```text
Public Replay:
DEPLOYED / PUBLIC_VERIFICATION_PASSED / HUMAN_ACCEPTED

Production URL:
https://aiscc-replay.pages.dev

Canonical persistence:
d7f2bbfe7dd712bf5f7d5a85873a91ccbb286acd

Human rights/license/tool disclosure:
CONFIRMED

Wanted form:
실제 스키마 확인 완료

Final submission:
NOT_COMPLETED
```

이번 Task는 **Wanted 실제 제출 완료**만 수행한다.

IDE Executor 작업은 없다.

---

## 실제 Wanted 폼에서 확인된 필수 항목

화면에서 확인된 필수 입력:

```text
대표 이미지 *
제목 *
해결하고자 한 문제 *
AI 활용 방식 및 결과 *   (500자)
사용 AI툴 및 기술 스택 *
서비스 링크 *
스크린샷 등록 *
```

스크린샷 등록 안내:

```text
서비스 대표 화면
최대 5개
16:9 비율
```

주의:

- source repository URL은 필수 항목으로 보이지 않는다.
- `사용 AI툴 및 기술 스택`은 predefined tag 방식이다.
- 실제 사용한 Codex tag가 없으므로 ChatGPT만 선택한 상태를 유지한다.
- Codex 사용 사실은 `AI 활용 방식 및 결과` 본문에서 명시한다.

---

# Operation 1 — 대표 이미지 최종 확인

현재 확정 대표 이미지:

```text
Viewport:
1440 × 910

Browser Zoom:
175%
```

Wanted preview에서 다음이 잘리지 않고 보여야 한다.

- `AISCC`
- `AI Software Command Center`
- `Recorded Run Replay`
- `From an AI claim to inspectable evidence.`
- recorded historical run 문구
- Live disabled 문구

PASS면 그대로 유지한다.

```text
Operation 1:
PASS / FAIL
```

---

# Operation 2 — 스크린샷 4장 확인

등록된 스크린샷은 다음 의미를 포함한다.

1. 4개 recorded scenario catalog
2. `Evidence admitted` recording detail
3. state transition detail
4. execution / evidence admission / human gate / judgment 구조

16:9 스크린샷 4장을 그대로 사용한다.

404/Unknown scenario QA 화면은 제출용 스크린샷에 추가할 필요 없다.

```text
Operation 2:
PASS / FAIL

등록 장수:
4
```

---

# Operation 3 — 제목

현재 권장/입력 제목:

```text
AI Software Command Center — AI 개발 작업을 증거로 통제하는 소프트웨어 거버넌스 콘솔
```

다음 조건이면 PASS:

- Coding Agent 자체로 오해시키지 않는다.
- evidence/governance 제품 정체성을 드러낸다.
- 최초/유일/우월성 claim이 없다.

```text
Operation 3:
PASS / FAIL
```

---

# Operation 4 — 해결하고자 한 문제

현재 권장/입력 문구:

```text
AI 코딩은 빨라졌지만, 무엇을 지시했고 어떤 증거로 검증되어 최종 승인됐는지를 신뢰성 있게 추적하기 어렵다는 문제를 해결합니다.
```

PASS 기준:

- AI coding 성능 자체의 부족을 문제로 정의하지 않는다.
- instruction / evidence / approval / provenance 추적 문제를 말한다.
- 과장된 novelty/superiority claim이 없다.

```text
Operation 4:
PASS / FAIL
```

---

# Operation 5 — AI 활용 방식 및 결과

500자 제한 안에서 다음 의미를 유지한다.

권장 본문:

```text
ChatGPT와 Codex를 기획·설계·구현에 활용했습니다. ChatGPT는 설계 검토, Task 발행과 Judgment 작성에, Codex는 실제 repository 작업·검증·Git commit에 사용했습니다. AI가 만든 결과를 그대로 신뢰하지 않고 작업 지시·검증 증거·사람의 확인·최종 판단을 분리해 기록하는 AISCC를 개발했으며, 실제 개발 과정에도 이 방식을 적용했습니다. 심사용 서비스에서는 실제 실행 기록을 Replay 형태로 확인할 수 있습니다.
```

PASS 기준:

- ChatGPT + Codex 실제 사용 사실이 들어간다.
- Codex를 사용했는데 Claude/Cursor 등 다른 tag/tool로 대체 표현하지 않는다.
- Replay가 live inference처럼 표현되지 않는다.
- self-dogfooding을 superiority proof로 표현하지 않는다.

```text
Operation 5:
PASS / FAIL
```

---

# Operation 6 — 사용 AI툴 및 기술 스택 tag

현재 실제 선택:

```text
ChatGPT
```

이를 유지한다.

Codex tag가 없으므로 다른 유사 tag를 대신 선택하지 않는다.

특히 실제 사용하지 않은:

- Claude
- Cursor
- GitHub Copilot
- Gemini

등은 선택하지 않는다.

```text
Operation 6:
PASS / FAIL
```

---

# Operation 7 — 서비스 링크

정확히:

```text
https://aiscc-replay.pages.dev
```

링크를 클릭/preview하여 production Replay가 정상 열리는지 마지막으로 확인한다.

새 코드/배포 변경은 하지 않는다.

```text
Operation 7:
PASS / FAIL
```

---

# Operation 8 — 제출 직전 전체 Preview

Wanted preview에서 확인:

- 대표이미지 crop이 정상
- 제목이 맞음
- 문제 정의가 맞음
- ChatGPT tag가 표시됨
- AI 활용 본문에 ChatGPT + Codex가 들어감
- 서비스 링크가 production URL
- 스크린샷 4장 정상
- private/company/customer 정보 없음
- token/account ID/credential 없음
- Live가 활성화됐다고 쓰지 않음
- 세계 최초/유일/우월성 claim 없음

```text
Operation 8:
PASS / FAIL
```

---

# Operation 9 — 최종 제출

오른쪽의:

```text
과제 제출하기
```

를 사용한다.

임시저장으로 끝내지 않는다.

확인 modal/dialog가 나오면 내용을 읽고 최종 제출한다.

마감 전 수정 가능하더라도, 이번 Task 결과는 실제 submission 완료 상태를 확보하는 것이다.

```text
Operation 9:
PASS / FAIL

실제 최종 버튼/문구:
```

---

# Operation 10 — 제출 완료 증거

최종 제출 후:

- 완료/제출 상태 문구
- `내 과제`의 상태
- 제출 완료 화면
- 제출 시각

중 가능한 것을 확인한다.

스크린샷을 Browser Command Center에 제출하면 가장 좋다.

계정 credential/private identifier는 별도로 확대/복사하지 않는다.

```text
Operation 10:
PASS / FAIL

실제 완료 문구:
제출 상태:
제출 확인 시각:
```

---

# Human 결과 제출 양식

```text
P3-3 Wanted Final Submission

Operation 1 — Representative image:
PASS / FAIL

Operation 2 — Screenshots:
PASS / FAIL
Count: 4

Operation 3 — Title:
PASS / FAIL

Operation 4 — Problem:
PASS / FAIL

Operation 5 — AI usage/result:
PASS / FAIL

Operation 6 — AI tool tag:
PASS / FAIL
Selected: ChatGPT

Operation 7 — Service URL:
PASS / FAIL
URL: https://aiscc-replay.pages.dev

Operation 8 — Final preview:
PASS / FAIL

Operation 9 — Final submit:
PASS / FAIL

Operation 10 — Submission confirmation:
PASS / FAIL

Final submission:
COMPLETED / NOT_COMPLETED

실제 제출 완료 문구:

제출 상태:

제출 확인 시각:

특이사항:
없음 / 내용
```

## STOP 조건

아래가 나오면 최종 제출 전에 Browser Command Center로 돌아온다.

- 새 필수 권리/약관 동의 문구가 나타났는데 의미가 불명확함
- 서비스 URL validation 실패
- 500자 제한 초과
- 실제 form field가 지금 확인한 스키마와 materially 다름
- 제출 button 이후 완료 여부를 확인할 수 없음
