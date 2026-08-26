# AISCC Product Thesis

## document status

| field | value |
|---|---|
| document_id | `AISCC-P0-2-PRODUCT-THESIS-V1` |
| task_id | `20260826_0122_aiscc-product-thesis-prior-art-and-competition-public-runtime-baseline-1` |
| work_type | `DOC_BASELINE_UPDATE` |
| result_status | `ACCEPTED / CLOSED` |
| generated_at | `2026-08-26 KST` |
| current_stage | `REPOSITORY_CANONICAL_ACCEPTED_BASELINE` |
| current authority | `.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md` — P0-4 acceptance 후 repository local canonical |
| canonical path | `.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md` |
| repository migration | `PERFORMED_BY_P0_4_REWORK` |
| human acceptance provenance | P0-2 terminal Cycle의 `HUMAN_PROVIDED / ACCEPTED` |
| canonicalized_by_task | `20260826_1038_aiscc-repository-bootstrap-canonical-authority-and-git-policy-rework-1` |
| supersession | `20260826_0043_aiscc-product-thesis-and-prior-art-boundary-baseline-1.md`는 실행 전 superseded 되었고 본 문서와 병렬 실행·병합하지 않았다. |

이 문서의 사실·판단 표시는 다음 label을 사용한다.

- `VERIFIED_SOURCE_FACT`: official documentation/repository/original paper로 현재 재확인한 외부 사실
- `HUMAN_PROVIDED_FACT`: 사람이 직접 확인하여 제공한 사실
- `PROJECT_INFERENCE`: source와 accepted input에서 도출한 프로젝트 해석
- `ACCEPTED_PROJECT_DECISION`: 이번 Task에서 재판정하지 않는 프로젝트 결정
- `OPEN_DIFFERENTIATION_HYPOTHESIS`: 구현·실증해야 하며 유일성이 검증되지 않은 설계 가설
- `UNVERIFIED`: 아직 사실 또는 성능으로 고정할 수 없는 항목

## 1. one-sentence product thesis

> **`ACCEPTED_PROJECT_DECISION`** — AISCC는 Coding Agent 자체가 아니라, AI가 수행한 software work를 Task Contract, authority, task-scoped evidence ownership, proof admission, system-owned state transition, human judgment, durable Cycle provenance 아래에서 통제하는 **Software Engineering Governance Control Plane**이다.

이 thesis가 주장하는 것은 governance 대상과 권한 구조다. 특정 primitive의 최초 발명, 전 세계적 유일성, 경쟁 제품보다 우월한 성능은 주장하지 않는다.

## 2. target user / primary operator

### primary operator

**`PROJECT_INFERENCE` / `HUMAN_PROVIDED_ACCEPTED`**

주요 사용자는 장기 실행되는 software project에서 하나 이상의 AI Coding Agent를 실제로 운용하면서 다음 책임을 함께 지는 **hands-on software owner, tech lead, 또는 engineering lead**다.

- 어떤 policy와 Task Contract가 현재 권위인지 결정한다.
- Agent의 `done`, `tested`, `reviewed` claim과 실제 evidence를 구분한다.
- human-owned verification과 exception approval을 직접 소유한다.
- 여러 Agent/session의 결과를 하나의 project state와 다음 행동으로 수렴시킨다.
- 공개 또는 감사 가능한 개발 provenance를 남겨야 한다.

### secondary user

**`PROJECT_INFERENCE`**

동일한 문제를 가진 소규모 engineering team, AI-assisted software delivery를 감독하는 reviewer, 그리고 AI 작업의 admission/audit trail이 필요한 project maintainer가 후속 사용자 후보가 될 수 있다.

### non-target user

AISCC MVP는 일반 소비자용 챗봇, 범용 IDE autocomplete, foundation model, 또는 새로운 범용 Coding Agent를 목표로 하지 않는다.

## 3. problem statement

**`ACCEPTED_PROJECT_DECISION`**

Coding Agent의 코드 생성 능력이 높아져도 장기 프로젝트의 완료 판정과 운영 책임은 자동으로 해결되지 않는다.

1. **authority drift** — 어느 instruction, Task, canonical document, current source behavior가 실제 권위인지 불명확해질 수 있다.
2. **claim/evidence collapse** — Agent가 `tested`, `reviewed`, `done`이라고 출력한 사실이 gate-admissible evidence나 system state로 오인될 수 있다.
3. **proof type substitution** — unit test, static artifact, browser checklist, human judgment처럼 서로 다른 proof channel이 조용히 대체될 수 있다.
4. **human ownership erosion** — 실제 account, browser, visual, business, security 판단을 Agent가 완료했다고 주장할 수 있다.
5. **transition authority ambiguity** — Agent의 자연어 판단이 next state 또는 terminal state를 직접 결정할 수 있다.
6. **provenance loss** — Task, 실행, evidence, review, human decision, failure, rework, commit 사이의 연결이 raw chat에 흩어진다.
7. **memory contamination** — 검증되지 않은 session output과 accepted decision이 같은 project memory로 누적될 수 있다.
8. **operator bottleneck** — 사람이 여러 Agent 채팅을 직접 따라다니며 context와 상태를 수작업으로 재구성한다.

AISCC는 Agent autonomy를 무제한 확장하기보다, software work가 project lifecycle에 **입장(admission)** 가능한 조건과 책임자를 명시한다.

## 4. why now

**`PROJECT_INFERENCE`**

- specification workflow, agent dispatch, multi-agent execution, permission gate, reviewer, persistent memory, evidence-gated lifecycle 등 핵심 primitive는 이미 공개 제품과 연구에서 확인된다.
- 따라서 새로운 Coding Agent를 하나 더 만드는 것보다, 이 primitive들이 실제 장기 프로젝트에서 어떤 authority와 evidence contract 아래 결합되는지를 명시하는 것이 AISCC의 더 정직한 문제 설정이다.
- Agent가 더 많은 코드를 작성할수록 사람이 검토해야 할 산출물과 claim도 증가하므로, 작성 능력과 별개로 transition admission, evidence ownership, human gate, durable provenance가 중요해진다는 것이 현재 제품 가설이다.
- 2026 AI Championship의 실제 제출과 공개 서비스 운영은 이 가설을 제한된 시간 안에 구현·실증하고, 공개 가능한 provenance로 남길 수 있는 구체적 외부 제약을 제공한다.

이 section은 시장 전체의 보편적 수요나 제품-시장 적합성을 검증한 사실이 아니다.

## 5. product category and authority boundary

### 5.1 product category

```text
AISCC
= Software Engineering Governance Control Plane
!= Coding Agent
!= Agent foundation model
!= unrestricted autonomous agent swarm
!= generic project-management board
```

AISCC는 Agent가 일을 대신 수행할 수 있도록 연결하지만, 제품의 primary semantic owner는 코드 생성 모델이 아니라 **Task/Evidence/Judgment/Cycle governance**다.

### 5.2 AI / System / Human authority

| actor | owns | must not own |
|---|---|---|
| AI | reasoning, plan proposal, code/change proposal, review proposal, evidence candidate production | workflow state, evidence admission, human-owned proof completion, terminal transition |
| System | workflow state, transition precondition/admission, required evidence, proof type/owner/freshness/provenance compatibility, tool permission, bounded retry/rework routing, terminal status admission | policy exception을 임의로 승인하거나 human acceptance를 대신하는 것 |
| Human | policy decision, exceptional approval, business acceptance, designated browser/account/visual/security verification, unresolved conflict resolution, final competition submission | routine Agent execution 결과를 evidence 없이 terminal truth로 선언하는 것 |

필수 invariant:

```text
AGENT_OUTPUT
!= SYSTEM_STATE

AGENT_CLAIM
!= ADMITTED_EVIDENCE

HUMAN_OWNED_EVIDENCE
!= EXECUTOR_COMPLETED

TERMINAL_TRANSITION
→ SYSTEM_ADMISSION
→ HUMAN_GATE_WHEN_REQUIRED
```

**`ACCEPTED_PROJECT_DECISION`** — orchestration core는 AISCC가 직접 구현한 explicit state machine을 사용하며, LangGraph를 orchestration core로 사용하지 않는다. 이 결정은 framework의 우열 주장이 아니라 state, transition, admission rule의 소유권을 제품 안에 명시적으로 두기 위한 설계 선택이다.

## 6. core governance chain

### 6.1 end-to-end chain

```text
Task Contract
→ Context / Authority Load
→ Plan Proposal
→ Plan Admission
→ Execute
→ Evidence Candidate Collection
→ Evidence Admission
→ Review
→ Human Gate when required
→ Judgment
→ Curated Cycle Memory
→ Next Action
```

### 6.2 compressed product chain

```text
Task
→ Evidence
→ Judgment
→ Cycle
→ Next Action
```

### 6.3 chain invariants

- Task Contract가 작업별 목표, 비목표, 허용·금지 범위와 five-way evidence ownership을 선행 정의한다.
- instruction transport와 project document authority는 동일한 precedence 체계가 아니다.
- evidence는 type, owner, freshness, provenance, current source applicability를 잃지 않는다.
- 다른 proof channel은 Task가 명시적으로 허용하지 않는 한 서로를 대체하지 않는다.
- Agent review는 proposal/claim이며 system admission 이전에는 judgment가 아니다.
- Cycle memory에는 raw session 전체가 아니라 judgment를 통과한 reusable decision/provenance만 입장한다.
- Next Action은 Agent의 자유 형식 결론이 아니라 accepted state, blocker, baseline gap, submission critical path를 기준으로 선택한다.

Exact state name, transition graph, persistence model, retry semantics는 P1-1 `Core Domain / State Machine Design`이 소유한다. 본 P0-2 문서는 이를 확정하지 않는다.

## 7. owner/private runtime and competition public surface

**`ACCEPTED_PROJECT_DECISION`**

AISCC는 실제 owner/self-dogfooding runtime과 대회 공개 demonstration runtime을 동일한 권한 profile로 취급하지 않는다.

| mode | purpose | repository/data | LLM behavior | authority/security posture |
|---|---|---|---|---|
| `OWNER_SELF_DOGFOOD` | AISCC 자신의 실제 후반 개발과 owner work 수행 | 향후 승인된 실제 AISCC repository와 private project context | 실제 task에 필요한 live execution 가능 | P1 security/sandbox baseline과 human authorization을 따르는 private owner profile |
| `PUBLIC_RECORDED_REPLAY` | 심사자가 실제 보존 run을 이해하고 재생 | 제출 전 실제 AISCC workflow로 실행·sanitization한 stored event/evidence | page view와 replay에 LLM inference `0` | public read-only, 명확한 `Recorded Run Replay` 표시, 기본 공개 mode |
| `PUBLIC_BOUNDED_LIVE` | 제품 이해를 돕는 선택적 보너스 demo | fixed synthetic repository와 allowlisted scenario만 | server-fixed provider/model, bounded calls/retry/time/budget | free-form task·외부 repo·upload·arbitrary shell/network 금지, 실패 시 Replay 유지 |

Decision owner:

```text
decision_id: AISCC-COMPETITION-PUBLIC-RUNTIME-V1
competition_runtime_mode: PUBLIC_REPLAY_WITH_BOUNDED_LIVE
```

공개 Live Demo는 평가 가능성의 single point of failure가 아니며, private owner runtime의 권한이나 범용성을 대신 증명하지 않는다.

## 8. MVP scope

다음은 구현 목표이며 현재 구현 완료 사실이 아니다.

1. **Task Contract**
   - exact goal/non-goal/allowed/forbidden scope
   - `executor_required`, `reuse_allowed`, `human_owned`, `not_required`, `forbidden`
2. **custom explicit state machine kernel**
   - Agent proposal과 system state 분리
   - precondition/evidence/policy 기반 transition admission
   - rework, blocked, human-required, terminal path
3. **Agent execution adapter**
   - 초기 provider 연결
   - provider/model 최종 선택과 abstraction depth는 deferred
4. **evidence admission**
   - proof type, owner, freshness, provenance, source-state applicability
   - proof non-substitution
5. **human gate and judgment**
   - designated human-owned proof 차단
   - exception/policy/business acceptance
6. **curated Cycle memory and Next Action**
   - Task, evidence, judgment, commit/run provenance 연결
   - raw session과 accepted memory 분리
7. **Command Center demonstration surface**
   - state/transition/evidence/judgment trace를 사람이 이해할 수 있게 표시
8. **canonical demo scenarios**
   - 정상 evidence PASS → accept
   - evidence 부족 → transition denied/rework
   - policy conflict → mutation 전 human-required/blocked
   - human-owned browser QA claim → reject/human-pending
9. **competition public runtime**
   - zero-inference Recorded Run Replay
   - optional bounded Live Demo
   - budget/provider failure에도 Replay 가용
10. **public provenance**
    - selected Task, Cycle, code/document diff/commit mapping
    - private source, customer data, secret 제외

## 9. explicit non-goals

- 범용 Coding Agent 또는 foundation model을 새로 만드는 것
- Agent framework의 기능 수 경쟁
- unrestricted autonomous agent swarm
- final architecture, exact state/transition model, API/data model을 P0-2에서 확정하는 것
- sandbox command allowlist, container, network, secret, filesystem 구현 상세를 P0-2에서 확정하는 것
- provider/model, token cap, daily/global run cap, currency budget의 숫자를 P0-2에서 고정하는 것
- 첫 버전부터 production-scale distributed orchestration을 구축하는 것
- Kubernetes, Kafka, 다수 microservice를 선행 도입하는 것
- 경쟁 제품의 모든 기능을 단기간에 복제하는 것
- specification, orchestration, evidence gate, memory, reviewer, permission/human gate, session provenance, multi-agent primitive의 최초 발명을 주장하는 것
- `세계 최초`, `유일`, `아무도 하지 않은` novelty claim
- Self-Dogfooding만으로 우월성, 보안 완전성, 일반화, 제품-시장 적합성을 증명했다고 주장하는 것
- public mode에 free-form task, 외부 repository URL/upload, arbitrary shell/network를 제공하는 것
- 실제 deployment, API key, billing configuration을 본 baseline에서 수행하는 것

## 10. success criteria

### minimum success

**`ACCEPTED_PROJECT_DECISION`**

- 핵심 governance chain이 실제로 작동하는 프로젝트를 만든다.
- AI와 사람이 어떻게 협업했는지 공개 가능한 Task/Cycle/code provenance를 남긴다.
- 공식 마감 전에 과제를 실제로 최종 제출한다.
- 참가·제출 완료 자체를 명확한 성공으로 본다. 공식 대회 FAQ에 따르면 과제 제출 참가자에게 `AI Builder` badge가 발급된다.
- 공개 서비스가 심사 가능하도록 유지되며, Live AI 장애나 예산 소진 시에도 Recorded Replay로 평가 가능하다.

### stretch success

**`ACCEPTED_PROJECT_DECISION`**

- TOP20, Demo Day, 상위 순위 또는 수상
- 사전 정의된 비교 평가에서 governance 효과를 정량·정성 evidence로 보이는 것
- 실제 Self-Dogfooding corpus가 발표에서 이해 가능한 강한 사례가 되는 것

Stretch goal 실패는 minimum success 실패를 의미하지 않는다.

## 11. Self-Dogfooding proof strategy

### 11.1 what it is intended to prove

**`OPEN_DIFFERENTIATION_HYPOTHESIS`**

P2-4 이후 AISCC 자신의 후반 개발 Task를 동일한 governance chain으로 수행한다.

```text
AISCC development task
→ AISCC Task Contract
→ explicit transition trace
→ Agent execution
→ evidence candidate/admission
→ human gate when applicable
→ judgment
→ curated Cycle
→ code/document commit mapping
```

각 self-dogfooding run은 최소 다음 provenance를 남겨야 한다.

- orchestrator version/commit
- Task Contract와 initial state
- requested/denied/admitted transition trace와 admission reason
- Agent claim과 admitted evidence 구분
- evidence type/owner/freshness/provenance
- human gate와 manual intervention
- rework/retry/fallback
- final Cycle과 result commit mapping

이 evidence가 실제로 존재한다면 다음과 같이 제한적으로 주장할 수 있다.

- AISCC가 자신의 개발 workflow에 실제 사용되었다.
- 지정된 시나리오에서 Agent claim과 system state가 분리되었다.
- missing/wrong-owner/wrong-type evidence가 transition을 통과하지 못했다.
- human-owned verification이 human gate 전에 완료로 승격되지 않았다.
- Task에서 Cycle과 commit까지 provenance가 연결되었다.

### 11.2 what Self-Dogfooding does not prove

Self-Dogfooding execution은 다음의 proof가 아니다.

- AISCC의 세계 최초성 또는 전 세계 유일성
- 경쟁 제품보다 높은 성능, 품질, 생산성 또는 비용 효율
- 모든 repository, language, team size, provider, model에 대한 일반화
- sandbox escape 불가능, prompt injection 면역, credential 안전 등 security completeness
- unattended production reliability 또는 심사 기간 내 모든 Live scenario 성공
- product-market fit, 사용자 선호, 상업적 수요
- self-produced evidence의 독립적 객관성
- Replay가 현재 Live AI execution이라는 사실

따라서 self-dogfooding claim은 observed run과 명시된 trust model 범위로 제한한다.

## 12. claim language guard

### allowed wording

다음 표현은 필요한 evidence가 있을 때 사용할 수 있다.

- “AISCC는 `<specified mechanism>`을 구현하도록 설계되었다.”
- “AISCC의 현재 differentiation은 `<hypothesis>`이며 구현·실증 대상이다.”
- “`<dated run>`에서 `<transition/evidence behavior>`가 관찰되었다.”
- “AISCC는 공개 prior art와 overlap을 인정하면서 `<specific integration>`을 제품 가설로 검증한다.”
- “이 화면은 `Recorded Run Replay`이며 현재 Live AI execution이 아니다.”

### forbidden or evidence-dependent wording

다음 표현은 P0-2에서 사용하지 않는다.

- “세계 최초”, “유일”, “아무도 하지 않은”, “완전히 새로운”
- “AISCC가 evidence gate / memory / orchestration / reviewer / permission gate를 발명했다.”
- “Self-Dogfooding이 제품 우월성과 novelty를 증명했다.”
- “공개된 경쟁 제품에 없으므로 존재하지 않는다.”
- “안전하다”, “신뢰할 수 있다”, “비용이 낮다”, “더 정확하다”를 비교 evidence 없이 단정
- Recorded Replay를 “Live”, “지금 AI가 실행 중”으로 표시
- 계획 또는 문서만 존재하는 기능을 구현 완료로 표현

### claim admission rule

```text
EXTERNAL FACT CLAIM
→ CURRENT OFFICIAL / PRIMARY SOURCE

AISCC CAPABILITY CLAIM
→ CURRENT IMPLEMENTATION
→ APPLICABLE EVIDENCE
→ JUDGMENT

COMPARATIVE CLAIM
→ PREDEFINED METRIC
→ MATCHED CONDITIONS
→ REPRODUCIBLE RESULT

NOVELTY CLAIM
→ NOT ADMITTED IN P0-2
```

## 13. repository canonical status

P0-4 rework가 accepted substantive body를 보존하여 다음 canonical path로 migration했다.

```text
.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md
```

Canonicalization result:

- P0-2 Human acceptance와 P0-4 canonicalization provenance를 document status에 반영했다.
- accepted substantive thesis, claim boundary, runtime policy는 변경하지 않았다.
- Bootstrap Seed v1은 수정하지 않았다.
- P0-5 first mirror v1 sync 전까지 Browser Project Source active set을 교체하지 않는다.

## 14. human acceptance provenance

P0-2 terminal Cycle에서 사람은 다음을 수용했다.

1. one-sentence thesis가 제품을 Coding Agent가 아닌 governance control plane으로 정확히 한정하는가.
2. primary operator를 hands-on software owner/tech lead로 두는 것이 맞는가.
3. minimum success와 stretch success의 경계가 맞는가.
4. Self-Dogfooding의 claim과 non-claim 경계가 충분히 엄격한가.
5. `OWNER_SELF_DOGFOOD`와 public competition surface 분리가 맞는가.
6. differentiation을 유일성 주장이 아닌 구현·실증 가설로 표현했는가.

Canonical status:

```text
HUMAN_PROVIDED / ACCEPTED / CLOSED
```
