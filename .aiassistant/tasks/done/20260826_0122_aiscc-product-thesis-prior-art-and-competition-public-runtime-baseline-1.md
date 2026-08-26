# 작업지시서: AISCC Product Thesis, Prior-Art Boundary, and Competition Public Runtime Baseline

## meta

- task_id: `20260826_0122_aiscc-product-thesis-prior-art-and-competition-public-runtime-baseline-1`
- created_at: `2026-08-26 01:22 KST`
- phase: `P0-2 — Product Thesis / Prior-Art Boundary Baseline`
- work_type: `DOC_BASELINE_UPDATE`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- browser_project: `AI Software Command Center`
- task_transport: `BROWSER_CHAT_ATTACHMENT`
- repository_status: `NOT_CREATED`
- primary_semantic_owner: `product thesis / prior-art claim boundary / competition public runtime product boundary`
- predecessor_cycle: `20260826_0007_aiscc-bootstrap-ruleset-extraction-and-initial-browser-project-source-seed-1`
- supersedes_task: `20260826_0043_aiscc-product-thesis-and-prior-art-boundary-baseline-1`
- superseded_task_execution_status: `NOT_EXECUTED`
- supersession_reason: `competition service-link availability, public inference cost, abuse resistance, Replay fallback, and operational horizon were not yet included`

## 현재 상태

- `AI Software Command Center` Browser Project 생성 완료
- Bootstrap Seed v1 active source `14/14` 업로드 완료
- P0-1 Bootstrap Ruleset Extraction: `ACCEPTED / CLOSED`
- P0-3 Browser Project Bootstrap: `HUMAN_CONFIRMED / CLOSED`
- Bootstrap Seed v1은 repository 생성 전 `TEMPORARY_BOOTSTRAP_AUTHORITY`
- Bootstrap Seed v1은 immutable하며 이번 작업에서 수정·교체하지 않는다.
- Prior-Art / Competitive Landscape Audit: `CLOSED`
- 대회 참가와 실제 과제 제출: `CONFIRMED`
- 상위 순위: stretch goal
- minimum success: 작동하는 프로젝트, 공개 가능한 AI 협업 provenance, 실제 과제 제출 완료
- orchestration core: 직접 구현한 explicit state machine
- P2-4 Self-Dogfooding: 핵심 실증 전략
- 공개 서비스는 심사 기간 동안 접속 가능해야 하므로 inference 비용·남용·서비스 가용성을 제품 경계에서 선제적으로 통제해야 한다.

## supersession guard

이 Task가 P0-2의 유일한 current Task Contract다.

다음 이전 Task는 실행하지 않는다.

```text
20260826_0043_aiscc-product-thesis-and-prior-art-boundary-baseline-1.md
```

이전 Task의 유효한 범위는 본 Task에 흡수되었다. 두 Task를 병합하거나 각각 실행하지 않는다.

## 이번 턴 목표

1. AISCC의 제품 thesis를 과장 없이 명확하게 고정한다.
2. 이미 존재하는 prior art와 AISCC가 주장해서는 안 되는 primitive를 명시한다.
3. AISCC differentiation을 `검증된 유일성`이 아니라 `제품 설계 가설과 구현·실증 대상`으로 정의한다.
4. P2-4 Self-Dogfooding이 어떤 claim을 증명하고 어떤 claim은 증명하지 못하는지 경계를 고정한다.
5. 대회 공개 서비스와 실제 AISCC owner/self-dogfooding runtime을 분리하고, 공개 서비스의 기본 동작을 `PUBLIC_REPLAY_WITH_BOUNDED_LIVE`로 고정한다.
6. 공개 페이지 열람·Recorded Run Replay는 LLM inference 없이 동작하고, Live AI 실행은 allowlist·호출 수·시간·예산으로 제한되며, 예산 소진 후에도 Replay를 통해 서비스 링크가 정상 작동하도록 제품 경계를 고정한다.
7. 대회 일정과 지식재산권·비밀정보·라이선스 유의사항을 product/submission boundary에 반영한다.
8. repository 생성 시 canonical path로 migration 가능한 pre-repository baseline artifact를 만든다.

## 이번 턴 비목표

- final architecture 확정
- exact state/transition model 확정
- sandbox command allowlist 또는 container implementation 상세 확정
- API/data model 설계
- Agent provider 또는 모델 최종 선정
- token 단가·월 예산·일별 run 수의 최종 숫자 확정
- rate limiter, authentication, billing meter 실제 구현
- repository 생성 또는 `.gitignore` 작성
- Project Source active set 수정·추가·삭제
- 실제 public deployment
- API key 생성·등록·결제 설정
- prior-art audit 방향 재개방
- 경쟁 제품 기능 전체 복제 계획
- `세계 최초`, `유일`, `아무도 하지 않은` novelty claim
- 대회 제출 문구 최종 작성
- 대회용 대표 이미지 또는 UI 시안 작성

## 읽을 Project Source

아래 exact source를 먼저 읽는다.

1. `00_AISCC_BOOTSTRAP__SEED_INDEX.md`
2. `01_AISCC_BOOTSTRAP__PROJECT_BOOTSTRAP.md`
3. `10_AISCC_RULES__AGENT_AUTHORITY_AND_TRANSPORT.md`
4. `20_AISCC_COMMAND_CENTER__README.md`
5. `21_AISCC_COMMAND_CENTER__WORKFLOW.md`
6. `22_AISCC_COMMAND_CENTER__TASK_FILE_TEMPLATE.md`
7. `24_AISCC_COMMAND_CENTER__JUDGMENT_RUBRIC.md`
8. `25_AISCC_COMMAND_CENTER__CYCLE_RECORD_TEMPLATE.md`
9. `26_AISCC_COMMAND_CENTER__NEXT_ACTION_SELECTION_RUBRIC.md`
10. `32_AISCC_RULES__PROJECT_SOURCE_MIRROR.md`
11. `33_AISCC_RULES__DOCUMENT_LANGUAGE_POLICY.md`

이 목록은 minimum authoritative context set이다. 현재 작업과 무관한 Project Source를 bulk-read하지 않는다.

## 사람 확정 입력

다음은 재판정 대상이 아니라 이번 baseline의 accepted project input이다.

### 1. 참가 및 성공 기준

- 대회에 참가하고 실제 과제를 제출한다.
- 상위 순위는 목표일 수 있으나 필수 성공조건은 아니다.
- 공개 가능한 AI 협업 provenance와 작동하는 결과물을 남긴다.
- `AI Builder` 참가 결과를 포함하여 실제 제출 완료 자체를 명확한 성공으로 본다.

### 2. orchestration

- Agent orchestration core는 직접 구현한 explicit state machine을 사용한다.
- LangGraph를 orchestration core로 사용하지 않는다.
- Agent가 next state 또는 terminal state를 직접 소유하지 않는다.
- AI Reviewer의 판단은 proposal/claim이며 최종 transition admission은 System 또는 지정된 Human이 소유한다.

### 3. prior-art audit closure

다음 primitive에는 강한 prior art가 존재하므로 AISCC의 최초 발명으로 주장하지 않는다.

- specification-driven development
- coding-agent dispatch/orchestration
- evidence-gated lifecycle / Proof-or-Stop 계열
- evidence admission
- human approval / permission gate
- persistent project memory
- agent session provenance
- reviewer agent
- multi-agent execution
- review feedback에서 reusable rule/skill을 생성하는 접근

비교 대상 범주는 최소 다음을 포함한다.

- specification: `Kiro`, `GitHub Spec Kit`
- dispatch/orchestration: `OpenAI Symphony`, `Factory`
- evidence-gated lifecycle: `Proof-or-Stop`
- memory/governance: `PROJECTMEM`
- session provenance / reusable learning: `SpecStory`, `Lore`
- permission/human gate primitives: `Claude Code`, `Factory`, `GitHub Copilot` 등
- review/learning/autofix: `Cursor Bugbot`, `Devin Review` 등

위 이름은 baseline 작성 시 최신 official source 또는 original paper로 factual phrasing을 재확인한다. Audit의 project decision을 재개방하지 않되, source가 지원하지 않는 세부 주장은 제거하거나 `UNVERIFIED`로 표시한다.

### 4. 현재 differentiation hypothesis

아래는 `세계 최초` 주장이 아니라 AISCC가 구현하고 실증할 제품 설계 가설이다.

1. task-scoped evidence ownership taxonomy
   - `executor_required`
   - `reuse_allowed`
   - `human_owned`
   - `not_required`
   - `forbidden`
2. proof type non-substitution
3. instruction transport와 project document authority의 분리
4. Agent claim과 admitted evidence의 분리
5. system-owned state transition admission
6. judgment를 통과한 curated memory/cycle admission
7. Task → Evidence → Judgment → Cycle → Next Action의 연결
8. 자기 자신의 후반 개발을 같은 governance chain으로 수행하는 Self-Dogfooding

### 5. 대회 제출·운영 관련 사람 제공 사실

사람이 대회 제출 화면과 행사 일정 화면에서 확인하여 제공한 내용이다.

- 과제 제출 마감: `2026-09-20`
- 예선 심사 및 온라인 투표: `2026-09-21`부터 `2026-10-05`까지
- TOP20 발표: `2026-10-07`
- Demo Day & 시상식: `2026-10-17`
- 서비스 링크는 심사 기간 동안 접속 가능한 상태로 유지해야 한다.
- 제출한 과제는 마감 이후 수정할 수 없고 열람만 가능하다.
- 주요 AI 도구 명칭과 활용 방식을 반드시 기재해야 한다.
- 회사/기관 업무상 저작물, 직무발명, 계약 위반 결과물, 제3자 권리 침해 결과물은 제출할 수 없다.
- 개인정보·회사 또는 기관 비밀정보를 포함하지 않아야 한다.
- 오픈소스·외부 API·생성형 AI의 라이선스와 이용 조건을 준수해야 한다.

외부 사실로 재서술할 때는 공식 대회 페이지에서 current verification을 수행한다. 공식 source가 동적 페이지 등의 이유로 일부 항목을 재확인하지 못하면 `HUMAN_PROVIDED`와 `OFFICIAL_SOURCE_NOT_RECONFIRMED`를 구분한다.

### 6. Competition Public Runtime 결정

다음 product boundary를 accepted project decision으로 고정한다.

```text
decision_id: AISCC-COMPETITION-PUBLIC-RUNTIME-V1
competition_runtime_mode: PUBLIC_REPLAY_WITH_BOUNDED_LIVE
default_public_mode: RECORDED_RUN_REPLAY
default_page_view_llm_calls: 0
public_freeform_task: FORBIDDEN
public_repository_url_or_upload: FORBIDDEN
public_arbitrary_shell_or_network: FORBIDDEN
live_scenario_scope: ALLOWLIST_ONLY
live_model_and_provider: SERVER_FIXED
live_run_model_calls: BOUNDED
live_run_retry: BOUNDED
live_run_duration: BOUNDED
application_budget_guard: REQUIRED
provider_budget_or_hard_spend_guard: REQUIRED_WHEN_SUPPORTED
budget_exhaustion_behavior: LIVE_DISABLED_REPLAY_AVAILABLE
minimum_verified_screening_availability: 2026-09-21 through 2026-10-05
project_operational_horizon: through 2026-10-17
```

의미:

- 공개 페이지와 Recorded Run Replay는 저장된 DB/event/evidence를 조회·재생하며 LLM을 호출하지 않는다.
- Recorded Run Replay는 제출 전 실제 AISCC workflow로 실행해 보존한 run이어야 하며 화면에서 `Recorded Run Replay`로 명확히 표시한다.
- Live Demo는 제품 이해를 돕는 보너스이며 심사 가능성의 단일 실패 지점이 아니다.
- Live Demo는 fixed synthetic repository와 allowlisted scenario만 사용한다.
- 자유 형식 task, 외부 repository, 파일 업로드, arbitrary command/network는 public mode에서 제공하지 않는다.
- 동일 요청의 refresh/retry는 새로운 inference를 무조건 생성하지 않도록 idempotency/budget policy를 후속 설계에서 둔다.
- application-level budget이 소진되거나 provider 호출이 실패해도 서비스 링크와 Replay는 계속 정상 동작해야 한다.
- exact model, token cap, daily/global run cap, currency budget은 추후 security/runtime/release baseline이 소유한다.
- 실제 owner/self-dogfooding runtime과 competition public demonstration runtime을 동일한 권한 profile로 취급하지 않는다.

## 조사 및 source 기준

- current/niche factual claim은 web으로 검증한다.
- 제품은 official documentation/repository를 우선한다.
- 연구 아이디어는 original paper 또는 official repository를 우선한다.
- 대회 일정·제출조건은 official event page/FAQ/submission page를 우선한다.
- 검색 결과 snippet, 홍보성 2차 기사, 출처 없는 비교표만으로 claim을 고정하지 않는다.
- 각 source의 publish/update date와 현재 접근 가능한 기능을 구분한다.
- source fact, human-provided fact, project inference, accepted project decision, open hypothesis를 섞지 않는다.
- 비공개 내부 제품이 존재하지 않는다고 단정하지 않는다.
- exact model pricing이나 provider feature가 바뀔 수 있으므로 P0-2에서 숫자를 고정하지 않는다.

문서 전반에서 다음 label을 명시적으로 사용한다.

```text
VERIFIED_SOURCE_FACT
HUMAN_PROVIDED_FACT
PROJECT_INFERENCE
ACCEPTED_PROJECT_DECISION
OPEN_DIFFERENTIATION_HYPOTHESIS
UNVERIFIED
```

## 산출물

다음 4개 Markdown artifact와 하나의 downloadable package를 생성한다.

### 1. `AISCC_PRODUCT_THESIS.md`

필수 내용:

- document status / future canonical path
- one-sentence product thesis
- target user / primary operator
- problem statement
- why now
- AI / System / Human authority boundary
- core governance chain
- owner/private runtime과 public competition demonstration surface의 분리
- MVP scope
- explicit non-goals
- minimum success / stretch success
- Self-Dogfooding proof strategy
- Self-Dogfooding이 증명하지 못하는 것
- claim language guard
- repository migration target:
  `.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md`

### 2. `AISCC_PRIOR_ART_BOUNDARY.md`

필수 section:

1. `KNOWN PRIOR ART`
2. `PARTIAL OVERLAP`
3. `DO-NOT-CLAIM`
4. `AISCC DIFFERENTIATION HYPOTHESES`
5. `UNVERIFIED / OPEN QUESTIONS`
6. `CLAIM EVIDENCE RULES`
7. source register

비교 matrix 최소 column:

- category
- product/research
- verified capability or thesis
- official/primary source
- overlap with AISCC
- AISCC may claim
- AISCC must not claim
- verification date

repository migration target:

```text
.aiassistant/reports/aiscc/AISCC_PRIOR_ART_BOUNDARY.md
```

### 3. `AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md`

필수 section:

1. document status / decision ID
2. verified competition facts
3. human-provided competition facts
4. accepted project decisions
5. runtime mode split
   - `OWNER_SELF_DOGFOOD`
   - `PUBLIC_RECORDED_REPLAY`
   - `PUBLIC_BOUNDED_LIVE`
6. zero-inference public browsing/replay contract
7. bounded live contract
8. budget exhaustion and provider failure fallback
9. public security/data/IP boundary
10. availability timeline and operational horizon
11. truthful replay/live labeling
12. deferred implementation decisions and future owner
13. P1-2 / P2-3 / P3-3 responsibility handoff

반드시 포함할 invariant:

```text
PUBLIC_PAGE_VIEW_OR_REPLAY
→ NO_LLM_INFERENCE

PUBLIC_LIVE_RUN
→ FIXED_SYNTHETIC_REPOSITORY
→ ALLOWLISTED_SCENARIO
→ BOUNDED_CALLS / RETRY / TIME / BUDGET

LIVE_UNAVAILABLE_OR_BUDGET_EXHAUSTED
→ RECORDED_REPLAY_REMAINS_AVAILABLE
```

repository migration target:

```text
.aiassistant/reports/aiscc/AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md
```

### 4. `AISCC_P0_2_BASELINE_CYCLE.md`

필수 내용:

- task summary
- superseded Task inventory
- read Project Source inventory
- web/primary source inventory
- verified source fact vs human-provided fact vs inference vs accepted project decision
- artifact inventory
- claim boundary check
- public runtime boundary consistency check
- human review status
- next action
- future canonical cycle path:
  `.aiassistant/records/aiscc/cycles/20260826_0122_aiscc-product-thesis-prior-art-and-competition-public-runtime-baseline-1.cycle.md`

### downloadable package

Package는 위 4개 Markdown만 포함한다.

권장 filename:

```text
20260826_0122_aiscc-p0-2-product-thesis-prior-art-and-public-runtime-baseline-candidate-1.zip
```

## evidence contract

### executor_required

- channel: `STATIC_SOURCE`
  - scope: 위 11개 Bootstrap Seed Project Source exact read
  - pass_condition: source role, temporary authority, immutable boundary, Task/Evidence/Judgment/Cycle 구조를 정확히 반영

- channel: `PRIOR_ART_PRIMARY_SOURCE`
  - scope: matrix에 포함한 각 load-bearing competitor/research claim
  - pass_condition: official docs/repository 또는 original paper citation 존재

- channel: `COMPETITION_OFFICIAL_SOURCE`
  - scope: 제출 마감, 심사/투표 일정, 서비스 링크 가용성, AI 도구 명시, 권리·비밀정보·라이선스 유의사항
  - pass_condition: official source citation 또는 재확인 실패가 명시된 `HUMAN_PROVIDED_FACT`

- channel: `PUBLIC_RUNTIME_BOUNDARY_CONSISTENCY`
  - scope: Product Thesis와 Public Runtime Boundary 간 mode/authority/fallback 일치
  - pass_condition: page/replay zero-inference, bounded live, public free-form 금지, budget fallback, operational horizon이 충돌 없이 명시

- channel: `DOCUMENT_INTEGRITY`
  - scope: 생성한 4개 Markdown과 package
  - pass_condition: UTF-8, fence parity, broken placeholder 없음, filename 일치, package count `4/4`

- channel: `CLAIM_BOUNDARY_REVIEW`
  - scope: world-first/unique/invention claim 및 fact/inference/decision 혼합 검사
  - pass_condition: 금지 claim 없음, open hypothesis 명시, public Replay를 Live AI처럼 과장하지 않음

### reuse_allowed

- predecessor: `Prior-Art / Competitive Landscape Audit CLOSED`
  - reusable_scope: project-level direction, comparison categories, DO-NOT-CLAIM 결정
  - condition: 구체적인 외부 factual statement는 current primary source로 다시 뒷받침

- predecessor: `20260826_0007_aiscc-bootstrap-ruleset-extraction-and-initial-browser-project-source-seed-1`
  - reusable_scope: Seed 생성·14/14 업로드·temporary authority·P0 ordering
  - condition: Bootstrap Seed active set을 수정하지 않음

- predecessor: human-provided competition screenshots/text
  - reusable_scope: 일정과 제출 유의사항의 사람 확인
  - condition: `HUMAN_PROVIDED_FACT`로 표시하고 official source verification 여부를 별도 기록

### human_owned

- channel: `HUMAN_VERIFICATION`
  - scope: product thesis, differentiation wording, Competition Public Runtime boundary 최종 수용
  - expected_result: `ACCEPTED`, `HOLD_REWORK_REQUIRED`, 또는 exact correction

- channel: `PUBLIC_SERVICE_RUNTIME`
  - scope: 실제 배포 링크 접근성, provider budget 설정, live run, browser/visual/useability 결과
  - expected_result: 이번 Task에서는 `HUMAN_PENDING` 또는 `NOT_REQUIRED`; 실제 배포 단계에서 별도 수행

### not_required

- product source
- Git repository
- commit/push
- runtime implementation
- database/HTTP/browser execution
- actual LLM live run
- provider API key 또는 billing 설정
- exact cost benchmark
- Project Source mirror sync

### forbidden

- Bootstrap Seed 14개 수정 또는 부분 교체
- Browser Project Source active set 추가/삭제
- superseded P0-2 Task와 병렬 실행
- repository가 생성된 것처럼 canonical path에 저장했다고 주장
- source가 지원하지 않는 최초/유일 claim
- Recorded Run Replay를 Live Run으로 표시
- public free-form execution을 accepted decision처럼 추가
- private Dialodog source, 회사 기밀, 고객 data 포함
- API key/credential 생성·출력·저장
- 실제 외부 deployment 또는 유료 API 호출
- architecture/state/security 상세 implementation을 이번 baseline에서 확정

## proof non-substitution

- product marketing copy != prior-art proof
- search snippet != primary source verification
- user screenshot/text != automatically verified official source fact
- self-dogfooding execution != product superiority proof
- feature aggregation != system novelty proof
- user experience != worldwide uniqueness proof
- Agent-generated matrix != human acceptance
- prior audit closure != every factual detail being permanently current
- Recorded Run Replay != current Live AI execution
- Replay availability != Live AI budget availability
- provider hard spend guard plan != configured provider limit evidence
- public service page accessibility != all live scenarios succeeding

## accept 기준

- 제품 thesis가 1문장으로 설명 가능하다.
- 제품이 Coding Agent 자체가 아니라 governance control plane임이 명확하다.
- primary operator와 해결 문제가 구체적이다.
- AI/System/Human 권한이 충돌 없이 분리된다.
- prior-art matrix가 primary source로 추적 가능하다.
- `DO-NOT-CLAIM`이 명시적이고 충분히 엄격하다.
- differentiation은 hypothesis/implementation target로 표현된다.
- Self-Dogfooding의 강점과 한계를 모두 기술한다.
- competition public surface와 owner/self-dogfooding runtime을 구분한다.
- 공개 기본 열람과 Replay가 zero-inference임이 명확하다.
- Live 실행은 allowlist와 bounded resource/budget 아래에만 존재한다.
- budget/provider failure 시 Replay fallback으로 service link가 계속 평가 가능하다.
- 공식 일정·사람 제공 사실·project operational decision을 혼동하지 않는다.
- ranking stretch / submission minimum 원칙이 유지된다.
- P0-4 repository bootstrap에 바로 migration 가능한 문서 구조다.
- Seed active source를 수정하지 않는다.

## hold/reject 기준

- `세계 최초`, `유일`, `아무도 하지 않은` 표현을 근거 없이 사용
- Factory/Kiro/Symphony/Proof-or-Stop/PROJECTMEM/SpecStory 등과의 overlap 은폐
- Self-Dogfooding을 성능 우월성 또는 novelty의 자동 proof로 과장
- source fact, human-provided fact, project inference, accepted project decision을 구분하지 않음
- Recorded Replay를 Live AI처럼 표시하거나 계획
- public free-form task/repository upload/arbitrary shell/network를 scope에 포함
- Live AI가 unavailable하면 전체 서비스 링크도 사용할 수 없게 설계
- application/provider budget guard와 fallback을 누락
- exact model·요금·run cap을 근거 없이 premature fixed decision으로 선언
- 과도한 architecture/implementation scope 확장
- Browser Project Source 14개를 수정 또는 교체
- private source/domain leakage

## 결과 status

사람 검토 전:

```text
ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING
```

사람 수용 후:

```text
ACCEPTED / CLOSED
```

외부 source 일부를 재확인하지 못했지만 사람 제공 사실과 product decision은 문서화 가능한 경우:

```text
ACCEPTED_CANDIDATE / OFFICIAL_SOURCE_PARTIAL / HUMAN_REVIEW_PENDING
```

## 다음 작업

P0-2가 수용되면 P0-3은 이미 human-confirmed이므로 다음은 바로:

```text
P0-4 Repository Bootstrap / Canonical Authority / Git Policy
```

P0-4는 본 Task가 생성한 세 canonical baseline 후보와 Cycle을 repository에 migration하되, P0-5 first mirror v1 전까지 Browser Project Source의 Bootstrap Seed v1을 수정하지 않는다.

## 보고서/최종 응답 요구

1. result status
2. read Project Source inventory
3. verified official/primary source inventory
4. generated artifact 4개
5. downloadable package link
6. claim boundary result
7. public runtime boundary result
8. human review pending 항목
9. unverified factual claims
10. future canonical paths
11. next action

장문 artifact 본문을 chat에 중복 출력하지 않는다.
