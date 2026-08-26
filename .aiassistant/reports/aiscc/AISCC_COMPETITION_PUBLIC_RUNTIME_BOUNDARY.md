# AISCC Competition Public Runtime Boundary

# 1. document status / decision ID

| field | value |
|---|---|
| document_id | `AISCC-P0-2-COMPETITION-PUBLIC-RUNTIME-BOUNDARY-V1` |
| task_id | `20260826_0122_aiscc-product-thesis-prior-art-and-competition-public-runtime-baseline-1` |
| result_status | `ACCEPTED / CLOSED` |
| generated_at | `2026-08-26 KST` |
| decision_id | `AISCC-COMPETITION-PUBLIC-RUNTIME-V1` |
| competition_runtime_mode | `PUBLIC_REPLAY_WITH_BOUNDED_LIVE` |
| canonical path | `.aiassistant/reports/aiscc/AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md` |
| repository migration | `PERFORMED_BY_P0_4_REWORK` |
| human acceptance provenance | P0-2 terminal Cycle의 `HUMAN_PROVIDED / ACCEPTED` |
| canonicalized_by_task | `20260826_1038_aiscc-repository-bootstrap-canonical-authority-and-git-policy-rework-1` |
| runtime/deployment action in P0-2 | `FORBIDDEN_NOT_RUN` |

Classification labels:

- `VERIFIED_SOURCE_FACT`
- `HUMAN_PROVIDED_FACT`
- `PROJECT_INFERENCE`
- `ACCEPTED_PROJECT_DECISION`
- `OPEN_DIFFERENTIATION_HYPOTHESIS`
- `UNVERIFIED`

# 2. verified competition facts

Official source: Wanted `AI Championship 2026` event landing/FAQ, verified `2026-08-26 KST`.

| fact | classification | official finding | product/submission impact |
|---|---|---|---|
| submission deadline | `VERIFIED_SOURCE_FACT` | 과제 제출은 `2026-09-20 23:59:59 KST`까지 완료해야 하며 접수만 하고 제출하지 않으면 심사·투표 대상이 아니다. | P3 submission은 temporary save가 아닌 final submit까지 완료해야 한다. |
| preliminary judging and voting | `VERIFIED_SOURCE_FACT` | `2026-09-21`부터 `2026-10-05`까지 예선 심사와 온라인 투표가 진행된다. | public service의 minimum verified screening availability window다. |
| TOP20 / Demo Day | `VERIFIED_SOURCE_FACT` | TOP20 발표 `2026-10-07`, Demo Day & 시상식 `2026-10-17`. | operational horizon을 최소 Demo Day까지 잡는 project decision의 외부 기준이다. |
| service link availability | `VERIFIED_SOURCE_FACT` | 심사 기간에 서비스 링크가 정상 접속되어야 하며 접속 불가로 심사가 어려우면 심사 대상에서 제외될 수 있다. | Live AI와 무관하게 page와 Replay가 계속 평가 가능해야 한다. |
| post-deadline edit freeze | `VERIFIED_SOURCE_FACT` | `2026-09-20`까지 수정 가능하고 마감 이후에는 수정 불가, 열람만 가능하다. | 제출 copy/link/config freeze 전에 recovery와 fallback을 검증해야 한다. |
| AI tool disclosure | `VERIFIED_SOURCE_FACT` | 주요 AI 도구 명칭과 활용 방식을 반드시 기재해야 한다. | AISCC public provenance와 submission disclosure에 실제 사용 tool/provider를 정직하게 기록한다. |
| work-for-hire / contract boundary | `VERIFIED_SOURCE_FACT` | 회사·기관 업무상 결과물, 직무발명·업무상저작물, 제3자 계약 또는 소속기관 규정 위반 결과물을 제출할 수 없다. | private employer/client source와 업무상 저작물을 repo, Replay, live scenario, submission에서 제외한다. |
| third-party rights | `VERIFIED_SOURCE_FACT` | 타인의 저작권·상표권·특허권·영업비밀 등을 침해해서는 안 된다. | synthetic repository와 public assets의 ownership/license provenance가 필요하다. |
| license and terms | `VERIFIED_SOURCE_FACT` | 오픈소스·외부 API·생성형 AI 이용 시 각 license와 terms를 준수해야 한다. | dependency/API/model terms register와 attribution을 P3에서 재검증한다. |
| paid API cost | `VERIFIED_SOURCE_FACT` | 유료 API 등의 이용료는 원칙적으로 참가자 부담이다. | public live는 bounded budget과 fail-safe Replay가 필요하다. |
| privacy/confidentiality | `VERIFIED_SOURCE_FACT` | 본인·타인의 개인정보와 소속기관의 기밀·비밀정보를 포함하지 않아야 하며 과제가 site/홍보에 노출될 수 있다. | public data는 synthetic/sanitized만 허용하고 secret/PII/private source를 금지한다. |
| project IP / organizer use | `VERIFIED_SOURCE_FACT` | 권리는 원칙적으로 참가자에게 귀속되지만 주최사는 운영·심사·홍보 범위에서 무상 이용할 수 있고 종료 후에도 게재될 수 있다. | 공개 가능한 source/data만 제출하며 장기 공개 가능성을 전제로 검토한다. |
| participant result | `VERIFIED_SOURCE_FACT` | 과제 제출 참가자 전원에게 `AI Builder` badge가 발급된다. | 실제 final submission 완료를 minimum success로 보는 project decision과 정합한다. |
| schedule change | `VERIFIED_SOURCE_FACT` | 주최사 사정으로 일정 변경·조기 종료가 가능하고 official site로 안내한다. | P3-3 및 운영 기간 중 official schedule을 재검증한다. |

Official source register:

- `COMP-01`: https://static.wanted.co.kr/ai-championship/2026/landing.html
- official event entry: https://event.wanted.co.kr/ai-championship/2026
- verification date: `2026-08-26 KST`

# 3. human-provided competition facts

이번 Task의 사람 제공 일정·제출 유의사항은 external fact로 사용하기 전에 official source와 대조했다.

| human-provided item | original classification | official reconfirmation | resulting use |
|---|---|---|---|
| 과제 제출 마감 `2026-09-20` | `HUMAN_PROVIDED_FACT` | `CONFIRMED`, official FAQ는 `23:59:59 KST`까지 명시 | `VERIFIED_SOURCE_FACT`로 재서술 가능 |
| 예선 심사·투표 `2026-09-21`~`2026-10-05` | `HUMAN_PROVIDED_FACT` | `CONFIRMED` | `VERIFIED_SOURCE_FACT`로 재서술 가능 |
| TOP20 `2026-10-07`, Demo Day `2026-10-17` | `HUMAN_PROVIDED_FACT` | `CONFIRMED` | `VERIFIED_SOURCE_FACT`로 재서술 가능 |
| 서비스 링크 심사 기간 가용 | `HUMAN_PROVIDED_FACT` | `CONFIRMED` | public runtime availability requirement |
| 마감 후 수정 불가·열람만 가능 | `HUMAN_PROVIDED_FACT` | `CONFIRMED` | pre-deadline freeze/recovery gate |
| 주요 AI 도구와 활용 방식 기재 | `HUMAN_PROVIDED_FACT` | `CONFIRMED` | submission disclosure requirement |
| 업무상 저작물·직무발명·계약 위반·제3자 권리 침해 금지 | `HUMAN_PROVIDED_FACT` | `CONFIRMED` | public IP boundary |
| 개인정보·기관 비밀정보 금지 | `HUMAN_PROVIDED_FACT` | `CONFIRMED` | data sanitization boundary |
| OSS·외부 API·생성형 AI license/terms 준수 | `HUMAN_PROVIDED_FACT` | `CONFIRMED` | dependency/provider compliance gate |

```text
OFFICIAL_SOURCE_NOT_RECONFIRMED: none
```

사람이 제공한 사실이라는 provenance는 보존하되, 현재 문서에서는 공식 source가 지원하는 범위만 `VERIFIED_SOURCE_FACT`로 사용한다.

# 4. accepted project decisions

다음은 `ACCEPTED_PROJECT_DECISION`이며 P0-2에서 재판정하거나 exact 숫자를 임의 추가하지 않는다.

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

Additional accepted interpretation:

- public page와 Recorded Run Replay는 stored DB/event/evidence만 조회·재생하며 LLM을 호출하지 않는다.
- Recorded Run은 제출 전에 실제 AISCC workflow로 실행하여 보존한 run이어야 한다.
- Live Demo는 optional bonus이며 evaluation의 single point of failure가 아니다.
- public Live는 fixed synthetic repository와 allowlisted scenario만 사용한다.
- refresh/retry가 새 inference를 무조건 생성하지 않도록 idempotency/budget policy가 필요하다.
- application budget이나 provider 호출이 실패해도 public page와 Replay는 정상 동작해야 한다.
- exact provider/model/cap/budget 숫자는 future security/runtime/release baseline이 소유한다.
- owner/self-dogfooding runtime과 public demonstration runtime은 동일 permission profile이 아니다.

# 5. runtime mode split

## 5.1 `OWNER_SELF_DOGFOOD`

Purpose:

- AISCC가 자신의 실제 후반 개발을 수행하는 owner/private runtime
- real Task, actual repository, admitted evidence, human gate, Cycle/commit provenance 생성

Boundary:

- public anonymous user가 접근할 수 없다.
- repository, source, credentials, network, tools는 P1 security/sandbox policy와 explicit owner authorization 범위만 사용한다.
- public mode보다 넓은 권한이 필요할 수 있으나 unrestricted profile을 의미하지 않는다.
- competition Live가 이 profile을 복제하거나 노출하지 않는다.
- owner runtime 성공은 public service availability proof가 아니다.

## 5.2 `PUBLIC_RECORDED_REPLAY`

Purpose:

- 심사자가 AISCC의 Task→transition→evidence→judgment→Cycle을 inference 비용 없이 이해한다.
- Live AI failure와 budget exhaustion에도 제품을 평가할 수 있게 한다.

Boundary:

- default public mode다.
- page view, run list, timeline, evidence detail, judgment, Replay control은 LLM inference를 호출하지 않는다.
- stored run은 제출 전에 실제 AISCC workflow로 실행한 결과여야 한다.
- private/company/customer source, PII, secret, credential, proprietary prompt 원문을 sanitization한다.
- 화면과 submission copy에서 `Recorded Run Replay`로 표시한다.
- Replay는 read-only이며 public input으로 원 run을 mutate하지 않는다.

## 5.3 `PUBLIC_BOUNDED_LIVE`

Purpose:

- 제한된 real-time run으로 product mechanism 이해를 보조한다.

Boundary:

- optional bonus이며 공개 서비스의 기본 가용성 조건이 아니다.
- fixed synthetic repository만 사용한다.
- allowlisted scenario만 선택 가능하다.
- free-form prompt/task, repository URL, source upload, arbitrary command/network를 제공하지 않는다.
- provider/model은 server-fixed다.
- calls, retries, duration, application spend가 bounded여야 한다.
- provider hard-spend guard는 provider가 지원할 때 함께 설정한다.
- admission 전에 budget/availability/abuse gate를 통과하지 못하면 Live를 시작하지 않는다.
- failure, timeout, budget exhaustion을 Replay 성공처럼 위장하지 않는다.

## 5.4 permission-profile separation invariant

```text
OWNER_SELF_DOGFOOD_PERMISSION_PROFILE
!= PUBLIC_BOUNDED_LIVE_PERMISSION_PROFILE

PUBLIC_BOUNDED_LIVE
!= GENERAL-PURPOSE CODING AGENT ACCESS
```

# 6. zero-inference public browsing/replay contract

필수 invariant:

```text
PUBLIC_PAGE_VIEW_OR_REPLAY
→ NO_LLM_INFERENCE
```

Contract:

1. landing page, project explanation, scenario list, run list, recorded event timeline, evidence viewer, judgment, Cycle summary, replay controls는 pre-stored data만 사용한다.
2. page render, refresh, route navigation, replay play/pause/seek/speed 변경은 model call을 만들지 않는다.
3. Replay 설명용 summary가 필요하면 제출 전 생성·검토·저장하며 page request 시 동적으로 생성하지 않는다.
4. analytics, observability, availability check가 LLM call을 유발하지 않는다.
5. Replay asset이 없거나 손상되면 명시적 Replay error를 표시한다. 이를 hidden Live call로 대체하지 않는다.
6. 공개 route는 user-provided task, repository, file, shell, network instruction을 받지 않는다.
7. Replay data는 original run timestamp, orchestrator version/commit, scenario ID, recorded/live type, evidence/judgment provenance를 보존한다.
8. sanitization과 license/IP review가 완료되지 않은 run은 public catalog에 입장시키지 않는다.

`default_page_view_llm_calls: 0`은 제품 decision이다. 아직 runtime instrumentation으로 검증된 implementation fact는 아니다.

# 7. bounded live contract

필수 invariant:

```text
PUBLIC_LIVE_RUN
→ FIXED_SYNTHETIC_REPOSITORY
→ ALLOWLISTED_SCENARIO
→ BOUNDED_CALLS / RETRY / TIME / BUDGET
```

## 7.1 input boundary

Allowed:

- server-defined scenario ID 선택
- 사전에 정의한 bounded parameter가 필요한 경우 allowlisted enum/range 선택
- human-readable start/cancel interaction

Forbidden:

- free-form task/prompt
- external repository URL
- repository or arbitrary file upload
- user-provided dependency/package
- arbitrary shell command
- arbitrary network destination
- credential/API key 입력
- owner/private data 선택

## 7.2 execution boundary

- fixed synthetic repository는 project-owned 또는 license-cleared material만 포함한다.
- each scenario는 allowed tools/actions, expected stop conditions, evidence contract를 사전 정의한다.
- model/provider는 server-fixed이며 browser request가 변경하지 못한다.
- model call count, retry count, wall-clock duration, token/context/output cap, per-run/application budget은 finite bound를 가져야 한다.
- exact 숫자는 P0-2에서 고정하지 않는다.
- request idempotency는 refresh/double-click/retry가 새 paid run을 무조건 생성하지 않게 해야 한다.
- retry는 silent unbounded loop가 아니며 exhaustion 시 terminal failure로 기록한다.
- application budget gate는 provider call 전에 fail-closed로 판단한다.
- provider hard-spend guard는 제공되는 기능 범위에서 defense-in-depth로 사용한다.
- provider/model 자동 fallback은 budget/profile을 우회해서는 안 된다.
- public output에는 secret, internal stack trace, host path, private prompt/context를 노출하지 않는다.

## 7.3 admission rule

```text
LIVE_REQUEST
→ SCENARIO_ALLOWLIST_CHECK
→ IDEMPOTENCY / ABUSE CHECK
→ APPLICATION_BUDGET_CHECK
→ PROVIDER_AVAILABILITY CHECK
→ ISOLATED EXECUTION ADMISSION
→ BOUNDED RUN
→ TRUTHFUL RESULT LABEL
```

각 gate의 exact architecture와 persistence는 deferred다.

# 8. budget exhaustion and provider failure fallback

필수 invariant:

```text
LIVE_UNAVAILABLE_OR_BUDGET_EXHAUSTED
→ RECORDED_REPLAY_REMAINS_AVAILABLE
```

| condition | Live behavior | public page / Replay behavior | truthful UX requirement |
|---|---|---|---|
| application budget exhausted | new Live admission 차단 | 정상 열람·Replay 계속 제공 | “Live Demo unavailable: application budget exhausted”와 Replay CTA |
| provider hard limit/spend guard reached | provider call 시도 없이 또는 fail-closed 차단 | 정상 유지 | provider limit을 Replay success로 표현하지 않음 |
| provider outage/rate limit | bounded retry 이후 Live failure | 정상 유지 | Live failure reason과 Recorded Replay 구분 |
| model timeout/error | run을 failed/blocked로 종료; terminal success 금지 | 정상 유지 | partial event를 success replay처럼 표시하지 않음 |
| application dependency failure limited to Live path | Live 비활성 | static/read-only path가 독립적으로 동작하도록 설계 | service 전체 outage로 확대하지 않음 |
| budget guard configuration evidence 없음 | public Live launch 금지 | Replay-only mode 유지 | “Live not enabled”로 표시 |
| replay store/page failure | 별도 service incident | Live를 자동 대체제로 사용하지 않음 | 평가 가능성 복구가 최우선 |

Design requirement:

- static/replay serving path와 paid inference path의 failure domain을 가능한 한 분리한다.
- Live button availability는 cached guess가 아니라 application gate 결과와 정합해야 한다.
- Live disabled 상태에서도 project thesis, recorded scenarios, evidence, Cycle, provenance를 열람할 수 있어야 한다.
- exact cost budget과 daily/global cap은 release owner가 설정하고 evidence로 남긴다.

# 9. public security / data / IP boundary

## 9.1 public data

Allowed:

- project-owned synthetic repository
- license-cleared dependency/sample
- sanitized AISCC run event/evidence
- public Task/Cycle/provenance selected for competition

Forbidden:

- private Dialodog source 또는 다른 회사/private project source
- 실제 고객/사용자 data
- 개인정보, 연락처, 계좌, 인증정보
- company/institution confidential or secret information
- API key, token, cookie, private key, credential
- employer work product, 직무발명, 업무상저작물, 계약 위반 결과물
- third-party copyrighted source without permission/license
- internal path/log/prompt 원문 중 secret 또는 private context

## 9.2 public execution

- no arbitrary repository, upload, shell, network
- no user-selected provider/model/credential
- no hidden access from public runtime to owner workspace
- no shared mutable state that lets one public run inspect another run's private data
- no Replay artifact admission before sanitization/license review
- no public claim that sandbox is secure until P1 design, implementation, and applicable security evidence exist

## 9.3 IP and license register requirement

P3 submission 이전에 최소 다음을 기록한다.

- project source ownership
- third-party dependency and license
- copied/generated asset provenance
- external API/provider terms relevant to public demo
- model/tool names and use disclosures
- recorded scenario repository ownership
- excluded private/company materials

Official contest rule의 확인은 legal advice나 계약 해석을 대신하지 않는다. 불명확한 권리는 human/legal review 대상으로 fail-closed 처리한다.

# 10. availability timeline and operational horizon

| date/window | classification | external event | AISCC operational obligation |
|---|---|---|---|
| through `2026-09-20 23:59:59 KST` | `VERIFIED_SOURCE_FACT` | final submission deadline; 이후 수정 불가 | final link, Replay, disclosure, license/IP, fallback을 제출 전에 검증하고 freeze |
| `2026-09-21` through `2026-10-05` | `VERIFIED_SOURCE_FACT` + `ACCEPTED_PROJECT_DECISION` | preliminary judging and online voting | `minimum_verified_screening_availability`; page/Replay 정상 접속을 최우선 SLO로 취급 |
| `2026-10-07` | `VERIFIED_SOURCE_FACT` | TOP20 announcement | 선정 여부와 무관하게 service 상태 확인; 선정 시 Demo Day 준비 전환 |
| through `2026-10-17` | `VERIFIED_SOURCE_FACT` + `ACCEPTED_PROJECT_DECISION` | Demo Day & awards / project operational horizon | public page/Replay 유지; Live는 budget/guard 안에서만 제공 |
| after `2026-10-17` | `UNVERIFIED` | 공식 page가 종료 정책을 별도 확정하지 않음 | archive/decommission/continued hosting은 후속 human decision |

Official schedule는 변경될 수 있으므로 다음 시점에 재확인한다.

- final submission 직전
- screening window 시작일
- TOP20 발표 직후
- Demo Day 준비 시

# 11. truthful replay / live labeling

## 11.1 required labels

Recorded artifact:

```text
Recorded Run Replay
Recorded at: <timestamp>
Scenario: <allowlisted scenario id>
Orchestrator version/commit: <value>
This is a replay of a previously executed AISCC workflow.
No LLM inference is performed while viewing this replay.
```

Live artifact:

```text
Live Demo
Started at: <timestamp>
Scenario: <allowlisted scenario id>
Provider/model: server fixed
Calls/retries/time/budget: bounded by server policy
```

Fallback:

```text
Live Demo is currently unavailable.
Recorded Run Replay remains available.
```

## 11.2 prohibited labeling

- Replay 화면에 “AI is working now”, “Live”, current token stream처럼 오인시키는 copy
- 과거 run timestamp를 숨겨 current execution처럼 보이게 하는 것
- Live failure 후 Recorded result를 동일 run의 성공 결과처럼 전환하는 것
- stored pre-generated summary를 current model reasoning이라고 표시하는 것
- budget exhaustion을 product success로 표시하는 것

## 11.3 provenance display

Replay와 Live 모두 가능한 범위에서 다음을 구분한다.

- run type: `RECORDED_REPLAY` / `LIVE`
- scenario ID/version
- synthetic repository version/commit
- orchestrator version/commit
- task and evidence contract
- transition trace and admission reason
- Agent claim vs admitted/rejected evidence
- human gate result
- final judgment
- recording/execution timestamp

# 12. deferred implementation decisions and future owner

P0-2에서 확정하지 않는 항목:

- exact provider/model
- per-run model call count, retry count, token/context/output cap
- daily/global run cap와 currency budget
- provider pricing
- authentication, anonymous session policy, rate limiter
- idempotency key, reservation/lease semantics, concurrency control
- application budget ledger/meter implementation
- provider spend guard configuration과 evidence
- replay event/data schema, storage, cache/CDN
- container/worktree/process/network/secret boundary
- command/tool allowlist implementation
- queue, cancellation, timeout, recovery
- observability, alerting, uptime check, incident response
- deployment provider/infrastructure
- exact UI copy와 visual design
- post-competition retention/decommission

Future semantic owners:

| decision area | future owner | P0-2 handoff |
|---|---|---|
| exact state/transition and run lifecycle | P1-1 `Core Domain / State Machine Design` | public mode가 Agent-owned terminal state를 허용하지 않는 invariant 전달 |
| sandbox/tool/network/secret and public/private permission profile | P1-2 security/sandbox design | free-form/repo upload/shell/network 금지, fixed synthetic allowlist, fail-closed 전달 |
| synthetic repository, scenario allowlist, recorded run corpus | P2-3 canonical scenario pack | actual AISCC run, sanitization, replay metadata, truthful label 전달 |
| public deployment, exact budget/cap/provider config, availability and submission disclosure | P3-3 release/submission package | zero-inference baseline, bounded live, fallback, dates, IP/license/tool disclosure 전달 |

`PROJECT_INFERENCE`: 위 phase-number responsibility mapping은 현재 bootstrap phase structure와 Task handoff 요구를 반영한 후보다. P0-4 이후 exact task title/path가 canonical queue에서 확정되어야 한다.

# 13. P1-2 / P2-3 / P3-3 responsibility handoff

## P1-2 — security/sandbox/runtime boundary

MUST own:

- `OWNER_SELF_DOGFOOD`와 `PUBLIC_BOUNDED_LIVE` permission profile 분리
- fixed synthetic repository isolation
- public tool/command/network allowlist and deny-by-default
- secret/credential/host filesystem/process boundary
- run timeout/cancel/retry failure semantics
- public request idempotency and abuse/throttling baseline
- application budget guard contract와 provider guard capability audit
- security evidence contract; unit test와 sandbox runtime proof의 비대체

MUST NOT weaken:

- public free-form 금지
- external repository/upload 금지
- arbitrary shell/network 금지
- budget failure 시 Replay 유지

## P2-3 — canonical scenario and Replay corpus

MUST own:

- project-owned synthetic repository/version
- allowlisted scenario definitions
- 각 scenario의 Task/evidence/human ownership contract
- actual AISCC execution과 recorded event/evidence capture
- sanitization, IP/license review, secret scan
- `Recorded Run Replay` metadata와 truthful UI contract
- normal, missing-evidence, policy-conflict, human-owned-claim scenarios
- replay integrity와 no-inference verification candidate

MUST NOT:

- fabricated run을 actual run으로 표시
- Replay를 Live로 표시
- private/company/customer source를 포함

## P3-3 — public release and competition submission

MUST own:

- official schedule/FAQ re-verification
- final service link and browser accessibility evidence
- static/Replay path availability and recovery
- exact provider/model/calls/retry/time/token/daily/global/currency caps
- application budget guard configuration evidence
- provider hard-spend guard evidence when supported
- Live enabled/disabled decision and fallback UX
- IP/license/AI tool/use disclosure
- post-deadline edit freeze checklist
- screening window monitoring through `2026-10-05`
- operational horizon through `2026-10-17`
- final human submission confirmation

# consistency result

```text
Product Thesis owner/public split: MATCHED
PUBLIC_PAGE_VIEW_OR_REPLAY → NO_LLM_INFERENCE: MATCHED
PUBLIC_LIVE fixed synthetic + allowlist: MATCHED
bounded calls/retry/time/budget: MATCHED
public free-form/repo upload/shell/network prohibition: MATCHED
budget/provider failure → Replay fallback: MATCHED
screening availability and operational horizon: MATCHED
Recorded Replay truthful labeling: MATCHED
exact cost/model/cap premature fixation: ABSENT
```

# human acceptance provenance

P0-2 terminal Cycle에서 사람은 다음 public runtime boundary를 수용했다.

1. `PUBLIC_REPLAY_WITH_BOUNDED_LIVE`를 public product boundary로 수용하는가.
2. Live가 optional bonus이고 Replay가 default/screening fallback이라는 점이 맞는가.
3. public free-form/repository upload/arbitrary shell/network 금지가 충분히 명시적인가.
4. minimum availability `2026-09-21`~`2026-10-05`, operational horizon through `2026-10-17`가 맞는가.
5. private owner runtime과 public permission profile이 충분히 분리되었는가.
6. P1-2/P2-3/P3-3 handoff owner가 적절한가.

Canonical status:

```text
HUMAN_PROVIDED / ACCEPTED / CLOSED
```
