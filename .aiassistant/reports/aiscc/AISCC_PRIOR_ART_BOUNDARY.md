# AISCC Prior-Art Boundary

## document status

| field | value |
|---|---|
| document_id | `AISCC-P0-2-PRIOR-ART-BOUNDARY-V1` |
| task_id | `20260826_0122_aiscc-product-thesis-prior-art-and-competition-public-runtime-baseline-1` |
| result_status | `ACCEPTED / CLOSED` |
| generated_at | `2026-08-26 KST` |
| verification_cutoff | `2026-08-26 KST` |
| canonical path | `.aiassistant/reports/aiscc/AISCC_PRIOR_ART_BOUNDARY.md` |
| repository migration | `PERFORMED_BY_P0_4_REWORK` |
| human acceptance provenance | P0-2 terminal Cycle의 `HUMAN_PROVIDED / ACCEPTED` |
| canonicalized_by_task | `20260826_1038_aiscc-repository-bootstrap-canonical-authority-and-git-policy-rework-1` |
| audit posture | prior-art 방향은 `CLOSED`; 구체적 factual wording만 current primary source로 재검증 |

## methodology and label boundary

이 문서는 comprehensive patentability search나 전 세계 제품 전수조사가 아니다. Task가 지정한 load-bearing comparison category를 official documentation, official repository, original paper로 재검증한 product boundary다.

- `VERIFIED_SOURCE_FACT`: source register의 official/primary source가 직접 지원하는 내용
- `HUMAN_PROVIDED_FACT`: 사람이 제공했지만 외부 official source와 별도 구분해야 하는 내용
- `PROJECT_INFERENCE`: source의 공통점·차이를 AISCC 관점에서 해석한 내용
- `ACCEPTED_PROJECT_DECISION`: prior-art primitive를 최초 발명으로 주장하지 않는 결정
- `OPEN_DIFFERENTIATION_HYPOTHESIS`: 구현·실증 대상으로 남긴 AISCC 조합/통제 가설
- `UNVERIFIED`: 전수조사·구현 evidence·비교 실험 없이는 확정할 수 없는 내용

```text
product marketing copy != prior-art proof
search snippet != primary source verification
feature aggregation != system novelty proof
self-dogfooding != product superiority proof
absence from reviewed sources != worldwide absence
```

# 1. KNOWN PRIOR ART

## 1.1 comparison matrix

| category | product/research | verified capability or thesis | official/primary source | overlap with AISCC | AISCC may claim | AISCC must not claim | verification date |
|---|---|---|---|---|---|---|---|
| specification-driven development | Kiro Specs | `VERIFIED_SOURCE_FACT`: requirements/user stories, design documentation, discrete trackable tasks로 feature/bugfix를 구조화하며 parallel task execution을 제공한다. | [PA-01] Kiro official docs | Task Contract, requirements/design/tasks 분해, accountability | AISCC가 이 prior art를 인정하고 별도의 evidence ownership/admission을 설계 대상으로 둔다고 말할 수 있다. | spec artifact, requirements→design→tasks workflow, parallel task execution을 AISCC가 발명했다고 주장하지 않는다. | 2026-08-26 |
| specification-driven development | GitHub Spec Kit | `VERIFIED_SOURCE_FACT`: specification을 중심으로 constitution→specify→plan→tasks→implement→converge workflow를 제공하는 open-source toolkit이다. | [PA-02] GitHub official repository | policy/constitution, plan/task decomposition, implementation convergence | AISCC가 spec-driven input을 사용할 수 있으나 primary differentiation은 governance admission이라고 말할 수 있다. | Spec-Driven Development 또는 executable specification primitive의 최초 발명을 주장하지 않는다. | 2026-08-26 |
| coding-agent dispatch/orchestration | OpenAI Symphony | `VERIFIED_SOURCE_FACT`: issue tracker를 coding-agent control plane으로 사용하고 open task마다 dedicated agent workspace를 연결하며 지속 실행·재시작·human review를 조직한다. | [PA-03] OpenAI official article and repository | task-board control plane, agent dispatch, workspace/session orchestration, status/state-machine use | AISCC가 Symphony와 달리 task-scoped proof ownership과 system admission을 중심 가설로 둔다고 제한적으로 비교할 수 있다. | issue tracker control plane, agent-per-task dispatch, continuous orchestration, self-generated code workflow의 최초 발명을 주장하지 않는다. | 2026-08-26 |
| multi-agent execution / orchestration | Factory Droid Exec / Mission Mode | `VERIFIED_SOURCE_FACT`: Mission Mode가 work를 계획하고 worker agent에 위임하며 결과를 validate하는 multi-agent orchestrator이고, tool restriction/enable/disable과 autonomy/permission controls를 제공한다. | [PA-04] Factory official docs | multi-agent plan/delegation/validation, tool permission, autonomy profiles | AISCC가 자체 explicit state machine과 evidence admission semantics를 구현 대상으로 선택했다고 말할 수 있다. | multi-agent orchestration, validator role, tool control, approval/autonomy primitive를 AISCC가 발명했다고 주장하지 않는다. | 2026-08-26 |
| evidence-gated lifecycle | Proof-or-Stop | `VERIFIED_SOURCE_FACT`: lifecycle state는 current evidence 없이 claim에 불과하며, fresh하고 tracked-source-state-bound하며 mechanically verifiable한 evidence가 gate를 만족할 때만 transition을 허용한다. Agent output을 lifecycle state가 아닌 claim으로 취급한다. | [PA-05] original paper | Agent claim/admitted evidence 분리, evidence-gated transition, freshness/source-state binding, reviewer gate, self-application | AISCC가 이 강한 overlap을 명시하고 task-scoped ownership taxonomy와 end-to-end productization을 별도 hypothesis로 검증한다고 말할 수 있다. | evidence-gated lifecycle, agent-as-claim, proof admission, false-DONE 방지, self-application의 최초 발명을 주장하지 않는다. | 2026-08-26 |
| persistent memory / judgment governance | PROJECTMEM | `VERIFIED_SOURCE_FACT`: append-only typed event log를 deterministic summary로 투영하고, 과거 실패 반복·fragile file 수정을 경고하는 deterministic pre-action gate를 제공하며 이를 `Memory-as-Governance`로 제시한다. immutable log는 provenance trail 역할을 한다. | [PA-06] original paper and official repository | persistent project memory, event provenance, deterministic gate, judgment layer, self-study | AISCC가 judgment를 통과한 Cycle admission과 Task→Cycle 연결을 자신의 구현 hypothesis로 제시할 수 있다. | persistent project memory, event-sourced provenance, judgment layer, memory-as-governance, self-study/dogfooding primitive를 AISCC가 발명했다고 주장하지 않는다. | 2026-08-26 |
| agent session provenance | SpecStory | `VERIFIED_SOURCE_FACT`: 여러 AI tool의 conversation을 Markdown으로 저장하여 reasoning, decision, tradeoff를 versioned/reusable/shareable/git-friendly knowledge로 보존한다. | [PA-07] SpecStory official docs and repository | session capture, intent/reasoning provenance, Git-friendly history | AISCC가 raw session capture보다 admitted Task/Evidence/Judgment/Cycle provenance를 우선한다는 설계 차이를 설명할 수 있다. | AI session 저장, conversation-to-Markdown, reasoning/decision provenance의 최초 발명을 주장하지 않는다. | 2026-08-26 |
| reusable learning / skill extraction | SpecStory Lore | `VERIFIED_SOURCE_FACT`: 저장된 session을 evidence-backed agent skill candidate로 mine하고, 실제 run과 user reply를 근거로 하며 human sign-off 전에는 skill을 쓰지 않는다고 설명한다. | [PA-08] SpecStory official Lore page and repository | run evidence에서 reusable rule/skill 후보 생성, human curation | AISCC가 Cycle/judgment를 통과한 memory/rule admission을 별도 hypothesis로 구현한다고 말할 수 있다. | session history나 review feedback에서 reusable skill을 생성하거나 human approval로 curate하는 접근의 최초 발명을 주장하지 않는다. | 2026-08-26 |
| permission / human gate | Claude Code | `VERIFIED_SOURCE_FACT`: permission rule은 model이 아니라 Claude Code harness가 집행하며, tool call 승인 방식과 allow/deny behavior를 permission mode/rule로 통제한다. | [PA-09] Anthropic official docs | model intent와 system-enforced permission 분리, human approval, tool gate | AISCC가 instruction transport, document authority, tool permission을 서로 다른 control plane concern으로 분리한다고 말할 수 있다. | model 외부 permission enforcement, tool approval mode, human gate primitive의 최초 발명을 주장하지 않는다. | 2026-08-26 |
| coding-agent human review / provenance | GitHub Copilot cloud agent | `VERIFIED_SOURCE_FACT`: agent를 제한된 branch/credential 아래 두고 human review 전 merge를 금지하며, agent가 자신의 PR을 approve/merge할 수 없고 session log와 signed commit으로 traceability를 제공한다. | [PA-10] GitHub official docs | human merge gate, branch/credential restriction, auditable agent work | AISCC가 software lifecycle 전반의 evidence owner/admission을 더 세분화하려는 hypothesis를 제시할 수 있다. | human review gate, restricted branch, agent work audit trail, code-agent provenance primitive의 최초 발명을 주장하지 않는다. | 2026-08-26 |
| reviewer / autofix | Cursor Bugbot | `VERIFIED_SOURCE_FACT`: PR review에서 발견한 issue에 대해 Cloud Agent를 생성해 fix를 만들고 branch에 push한 뒤 결과를 PR comment로 남기는 Autofix workflow를 제공한다. | [PA-11] Cursor official docs | reviewer agent, review finding→fix loop, bounded attempt configuration | AISCC가 reviewer finding을 evidence/judgment/rework chain에 입장시키는 방법을 검증한다고 말할 수 있다. | reviewer agent, automated PR review, review finding 기반 autofix loop의 최초 발명을 주장하지 않는다. | 2026-08-26 |
| reviewer / code understanding | Devin Review | `VERIFIED_SOURCE_FACT`: complex PR을 logical diff와 explanation으로 조직하고 bug/security finding, comment/approval/request-changes, codebase-aware interaction을 제공하는 code review platform이다. | [PA-12] Devin official docs | reviewer platform, bug/security finding, human review workflow | AISCC가 review output을 terminal truth가 아닌 claim/evidence candidate로 다루는 제품 가설을 제시할 수 있다. | AI code review, bug catcher, security finding, review platform의 최초 발명을 주장하지 않는다. | 2026-08-26 |

## 1.2 known primitive inventory

**`ACCEPTED_PROJECT_DECISION`**

다음 primitive에는 강한 prior art가 존재하므로 AISCC의 발명으로 주장하지 않는다.

- specification-driven development
- coding-agent dispatch/orchestration
- evidence-gated lifecycle / Proof-or-Stop 계열
- evidence admission과 Agent claim/state 분리
- human approval / permission gate
- persistent project memory와 event provenance
- agent session provenance
- reviewer agent와 AI code review
- multi-agent execution과 validator role
- review/session evidence에서 reusable rule/skill을 생성하는 접근
- self-application 또는 dogfooding을 evaluation corpus로 사용하는 접근

# 2. PARTIAL OVERLAP

| AISCC design area | strongest observed overlap | current boundary judgment |
|---|---|---|
| task-scoped evidence ownership taxonomy | Proof-or-Stop의 gate-admissible evidence, 일반 Task/evidence workflow | `PROJECT_INFERENCE`: exact five-way taxonomy의 동일 구현 여부는 조사 범위에서 확인하지 못했지만 evidence owner/type 분류 자체를 novelty로 주장할 수 없다. |
| proof type non-substitution | Proof-or-Stop의 stated trust model과 gate-specific evidence | `PROJECT_INFERENCE`: AISCC는 proof channel compatibility를 제품 invariant로 전면화하려 하나 primitive의 최초성은 주장하지 않는다. |
| instruction transport vs project document authority | Claude Code의 prompt instruction과 harness-enforced permission 분리; spec tools의 repository instruction | `PROJECT_INFERENCE`: exact authority model 조합은 AISCC hypothesis지만 “prompt와 system permission은 다르다”는 primitive는 기존에 존재한다. |
| Agent claim vs admitted evidence | Proof-or-Stop의 direct overlap | `VERIFIED_SOURCE_FACT`: 매우 직접적인 overlap이므로 AISCC 독자 발명으로 주장해서는 안 된다. |
| system-owned state transition admission | Proof-or-Stop evidence gate; Symphony task status/state-machine orchestration | `PROJECT_INFERENCE`: AISCC가 직접 소유한 explicit state machine의 구현은 자기 제품 사실이 될 수 있으나, system-enforced transition 자체는 novelty가 아니다. |
| judgment-passed curated memory/cycle admission | PROJECTMEM judgment/pre-action gate; SpecStory/Lore session-to-knowledge curation | `PROJECT_INFERENCE`: AISCC의 exact Cycle semantics는 구현 target이지만 persistent/governed memory primitive는 prior art다. |
| Task→Evidence→Judgment→Cycle→Next Action chain | Kiro/Spec Kit task flow, Proof-or-Stop evidence gate, PROJECTMEM memory, reviewer products | `OPEN_DIFFERENTIATION_HYPOTHESIS`: 통합 product chain으로서 실용적 가치가 있는지 구현·실증해야 하며, feature aggregation만으로 novelty를 증명하지 못한다. |
| Self-Dogfooding | OpenAI Symphony의 internal self-use, Proof-or-Stop self-application, PROJECTMEM self-study | `VERIFIED_SOURCE_FACT`: self-use 자체는 강한 prior art다. AISCC는 자신의 exact governance trace를 evidence로 제시할 수 있을 뿐 최초성을 주장할 수 없다. |

# 3. DO-NOT-CLAIM

## 3.1 categorical prohibition

AISCC 문서, README, 발표, 대회 제출문, UI copy에서 다음을 근거 없이 주장하지 않는다.

1. AISCC가 specification-driven development를 발명했다.
2. AISCC가 coding-agent dispatch, issue/task orchestration, multi-agent execution을 발명했다.
3. AISCC가 evidence-gated lifecycle, Proof-or-Stop, false-DONE 방지, Agent-as-claim 접근을 발명했다.
4. AISCC가 evidence admission 또는 proof gate를 최초로 만들었다.
5. AISCC가 human approval, permission gate, tool allow/deny를 최초로 만들었다.
6. AISCC가 persistent project memory, event-sourced memory, judgment layer를 최초로 만들었다.
7. AISCC가 agent session provenance 또는 conversation-to-Markdown을 최초로 만들었다.
8. AISCC가 reviewer agent, AI code review, review autofix loop를 최초로 만들었다.
9. AISCC가 review/session evidence에서 reusable rule/skill을 만드는 접근을 최초로 만들었다.
10. AISCC의 기능 조합이 곧 세계 최초·유일·발명이라는 주장
11. Self-Dogfooding이 novelty, 우월성, 보안 완전성 또는 일반화를 자동 증명한다는 주장
12. 검토한 public source에서 보이지 않았다는 이유로 private/internal product에도 기능이 없다고 단정하는 주장
13. Recorded Run Replay를 현재 Live AI execution으로 표시하는 주장
14. 구현 문서·mock·checklist만으로 runtime capability가 존재한다고 주장하는 것
15. 비교 실험 없이 더 정확함, 더 안전함, 더 저렴함, 더 생산적임을 단정하는 것

## 3.2 prohibited language examples

```text
세계 최초의 AI software governance system
유일하게 evidence를 검증하는 coding-agent platform
아무도 만들지 않은 Task-to-Cycle workflow
최초의 self-dogfooding agent orchestrator
기존 제품에는 없는 완전한 human gate
```

위 문구는 삭제하거나 다음처럼 제한한다.

```text
AISCC는 공개 prior art와 overlap을 인정한 상태에서,
<exact mechanism>을 하나의 governance chain으로 구현하고
<defined scenarios>에서 그 동작을 검증하는 제품 가설이다.
```

# 4. AISCC DIFFERENTIATION HYPOTHESES

다음은 `OPEN_DIFFERENTIATION_HYPOTHESIS`다. 검증된 유일성이 아니며 구현·실증 전 capability claim도 아니다.

| id | hypothesis | intended distinction | evidence required before stronger claim | does not prove |
|---|---|---|---|---|
| `AISCC-DH-01` | task-scoped evidence ownership taxonomy | 각 Task가 `executor_required`, `reuse_allowed`, `human_owned`, `not_required`, `forbidden`을 실행 전에 소유한다. | schema/validation 구현, owner mismatch denial test, real Cycle trace | taxonomy의 worldwide uniqueness |
| `AISCC-DH-02` | proof type non-substitution | static/unit/integration/runtime/browser/human proof를 type-compatible gate 없이 대체하지 않는다. | incompatible proof rejection tests와 admitted/rejected evidence trace | semantic correctness 전체, 모든 false positive 제거 |
| `AISCC-DH-03` | instruction transport와 project document authority 분리 | Agent에게 어떻게 instruction이 전달됐는지와 어떤 document가 policy authority인지 분리한다. | conflict cases, explicit source-load trace, system admission behavior | 다른 제품에 유사 authority model이 없음 |
| `AISCC-DH-04` | Agent claim과 admitted evidence 분리 | Agent output은 claim/candidate이고 system이 type/owner/freshness/provenance를 검사해 입장시킨다. | evidence admission implementation과 false-completion scenarios | primitive의 최초성; Proof-or-Stop보다 우월함 |
| `AISCC-DH-05` | system-owned state transition admission | Agent가 next/terminal state를 직접 소유하지 않고 explicit transition engine이 admission한다. | deterministic transition tests, denied transition trace, human-required gate | 모든 state-machine orchestrator보다 새로움 |
| `AISCC-DH-06` | judgment를 통과한 curated memory/cycle admission | raw session 전체가 아니라 Task/evidence/judgment 결과를 reusable Cycle로 입장시킨다. | durable Cycle model, rejected-memory exclusion, next-action reuse trace | persistent memory의 최초성; 장기 기억 품질 우월성 |
| `AISCC-DH-07` | Task→Evidence→Judgment→Cycle→Next Action 연결 | work instruction, proof, 판정, 기억, 다음 행동을 하나의 inspectable chain으로 연결한다. | end-to-end scenario corpus와 Task/Cycle/commit mapping | feature aggregation만으로 novelty 또는 superiority |
| `AISCC-DH-08` | same-governance Self-Dogfooding | AISCC의 후반 개발을 동일한 governance chain으로 수행한다. | orchestrator commit, transition/evidence/human trace, external review 가능한 corpus | 제품 우월성, 독립 검증, 보안 완전성, 일반화 |

### differentiation claim ceiling at P0-2

현재 허용되는 최대 표현:

> AISCC는 이미 존재하는 specification, orchestration, evidence gate, permission, memory, reviewer, provenance primitive를 발명했다고 주장하지 않는다. AISCC의 differentiation은 task-scoped evidence ownership과 proof non-substitution, system-owned transition admission, curated Cycle memory를 하나의 inspectable governance chain으로 구현하고, 그 동일한 chain으로 자신의 후반 개발을 수행해 보는 제품 설계 가설이다.

# 5. UNVERIFIED / OPEN QUESTIONS

1. `UNVERIFIED` — 위 source set이 전 세계 public/private prior art를 exhaustive하게 포괄하는지.
2. `UNVERIFIED` — AISCC의 exact taxonomy와 chain 조합이 다른 비공개 제품·내부 tool·연구 prototype에 존재하지 않는지.
3. `UNVERIFIED` — reviewed product의 paid/private/preview 기능이 public docs보다 더 넓은지.
4. `UNVERIFIED` — AISCC가 실제 프로젝트에서 operator context switching, false completion, review burden을 유의미하게 줄이는지.
5. `UNVERIFIED` — AISCC의 proof compatibility와 ownership model이 다양한 repository/language/provider에 일반화되는지.
6. `UNVERIFIED` — custom explicit state machine이 framework 기반 orchestration보다 유지보수·신뢰성·비용 측면에서 우월한지.
7. `UNVERIFIED` — Self-Dogfooding corpus가 independent evaluation 없이도 외부 심사자에게 충분히 설득력 있는지.
8. `UNVERIFIED` — public bounded live의 abuse resistance, availability, latency, cost profile.
9. `UNVERIFIED` — 각 source/product의 2026-09-20 제출 시점 기능 상태가 2026-08-26과 동일한지.
10. `UNVERIFIED` — 오픈소스, 외부 API, 생성형 AI 이용 조건의 프로젝트별 법적 적용. 라이선스 사실 확인과 법률 판단은 동일하지 않다.

Open question은 novelty language를 허용하는 빈칸이 아니다. 확인되지 않은 항목은 `UNVERIFIED`로 유지한다.

# 6. CLAIM EVIDENCE RULES

## 6.1 external factual claim

```text
current product/research fact
→ official documentation / official repository / original paper
→ exact source register entry
→ verification date
→ source-supported scope only
```

- 검색 결과 snippet과 홍보성 2차 기사만으로 load-bearing claim을 고정하지 않는다.
- product page의 marketing phrase를 independent performance proof로 사용하지 않는다.
- source가 지원하지 않는 세부 기능은 제거하거나 `UNVERIFIED`로 표시한다.
- negative claim은 특히 엄격하게 제한한다. “공개 문서에서 찾지 못했다”는 “존재하지 않는다”가 아니다.

## 6.2 AISCC capability claim

```text
planned document
!= implemented capability

implemented source
!= runtime proof

Agent report
!= admitted evidence

admitted evidence
!= human acceptance
```

AISCC 기능을 현재형으로 주장하려면 current source, applicable evidence, system judgment가 연결되어야 한다.

## 6.3 comparative claim

비교 우월성을 주장하려면 최소 다음이 필요하다.

- 사전에 정의한 question, metric, baseline, task set
- 가능한 한 동일한 model/provider/compute/time condition
- success/failure와 exclusion rule
- reproducible run artifact
- human-owned 평가가 필요하면 human result
- limitation과 confidence 범위

그 전에는 “우월하다”가 아니라 “비교할 예정이다” 또는 “이 설계 차이를 검증한다”로 표현한다.

## 6.4 Self-Dogfooding claim

Self-Dogfooding claim은 다음과 연결되어야 한다.

- exact Task
- orchestrator version/commit
- transition trace
- Agent claim / admitted evidence 구분
- human gate
- Cycle/commit mapping
- manual fallback과 failure

Self-Dogfooding은 “사용했다”를 증명할 수 있지만 “유일하다”, “최고다”, “독립적으로 검증됐다”를 증명하지 않는다.

## 6.5 Replay / Live claim

```text
Recorded Run Replay
!= current Live AI execution

Replay availability
!= Live AI budget availability

public page accessibility
!= all live scenarios succeeding
```

UI, README, 발표, 제출문에서 Replay와 Live를 명시적으로 구분한다.

## 6.6 freshness rule

- P3 submission copy 작성 전 source register의 기능·일정을 재검증한다.
- source update date와 access date를 구분한다.
- changeable provider pricing/model/cap은 P0-2 claim에 포함하지 않는다.

# 7. source register

| id | source type | publisher / authors | title | official/primary URL | source date/update | facts used | limitation |
|---|---|---|---|---|---|---|---|
| `PA-01` | official documentation | Kiro | Specs | https://kiro.dev/docs/specs/ | page updated 2026-08-04; verified 2026-08-26 | requirements/design/tasks structure, tracking, parallel task execution | docs describe product capability, not independent effectiveness |
| `PA-02` | official repository | GitHub | `github/spec-kit` | https://github.com/github/spec-kit | current repository; verified 2026-08-26 | spec-driven toolkit; constitution→specify→plan→tasks→implement→converge | repository claim is not comparative proof |
| `PA-03` | official article + repository | OpenAI | An open-source spec for Codex orchestration: Symphony / `openai/symphony` | https://openai.com/index/open-source-codex-orchestration-symphony/ ; https://github.com/openai/symphony | article 2026-04-27; verified 2026-08-26 | issue tracker control plane, agent per task, workspace loop, human review, state-machine status | published internal outcomes are not AISCC comparison evidence |
| `PA-04` | official documentation | Factory | Droid Exec / Mission Mode; Autonomy and Safety | https://docs.factory.ai/droid-exec/overview ; https://docs.factory.ai/autonomy-and-safety/auto-run | verified 2026-08-26 | multi-agent plan/delegate/validate, tool and autonomy controls | product behavior may depend on plan/config/version |
| `PA-05` | original paper | Jek Huang, Jeffery Hsia, Jiayi Sun, Freddie Shi, Wei Huang, Ian H. White | Proof-or-Stop: Don't Trust the Agent, Trust the Evidence | https://arxiv.org/abs/2607.14890 | submitted 2026-07-16; verified 2026-08-26 | Agent claim vs lifecycle state, fresh/source-bound/mechanical evidence gate, self-application | preprint; evaluation limitations stated by authors |
| `PA-06` | original paper + official repository | Ripon Chandra Malo, Tong Qiu | PROJECTMEM | https://arxiv.org/abs/2606.12329 ; https://github.com/riponcm/projectmem | submitted 2026-06-10; verified 2026-08-26 | append-only events, deterministic projection, pre-action gate, Memory-as-Governance, provenance | preprint and self-study; not broad independent validation |
| `PA-07` | official documentation + repository | SpecStory | Overview / `getspecstory` | https://docs.specstory.com/ ; https://github.com/specstoryai/getspecstory | verified 2026-08-26 | session capture to Markdown, reasoning/decision provenance, reusable/versioned knowledge | product docs, not independent outcome study |
| `PA-08` | official product page + repository | SpecStory | Lore | https://specstory.com/lore ; https://github.com/specstoryai/getspecstory | verified 2026-08-26 | session corpus→evidence-backed skill candidate, human sign-off | exact algorithms/effectiveness not independently verified here |
| `PA-09` | official documentation | Anthropic | Claude Code permissions | https://code.claude.com/docs/en/permissions | verified 2026-08-26 | harness-enforced permission rules, modes, approval behavior | version/plan/config may alter availability |
| `PA-10` | official documentation | GitHub | Risks and mitigations for Copilot cloud agent | https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations | verified 2026-08-26 | restricted branch/credentials, human review before merge, session/commit traceability | describes one GitHub agent surface, not all Copilot modes |
| `PA-11` | official documentation | Cursor | Bugbot | https://cursor.com/docs/bugbot | verified 2026-08-26 | PR review issue→Cloud Agent autofix→branch/comment; attempt bound option | product docs, not comparative accuracy evidence |
| `PA-12` | official documentation | Cognition | Devin Review | https://docs.devin.ai/work-with-devin/devin-review | verified 2026-08-26 | organized PR review, bug/security finding, review interaction | product docs, not independent review-quality proof |

## source register conclusion

- load-bearing prior-art rows: `12/12` current official/primary source 존재
- secondary article-only claim: `0`
- search snippet-only admitted claim: `0`
- worldwide uniqueness established: `No`
- prior-art audit direction reopened: `No`
- required boundary result: prior art 인정 + AISCC differentiation을 open implementation hypothesis로 유지

## human acceptance provenance

P0-2 terminal Cycle에서 사람은 다음 boundary를 수용했다.

1. matrix의 overlap 강도가 과소 또는 과대 표현되지 않았는가.
2. `Proof-or-Stop`과 `PROJECTMEM`에 대한 DO-NOT-CLAIM이 충분히 엄격한가.
3. eight differentiation hypotheses가 실제 AISCC 구현 target을 정확히 나타내는가.
4. 대회 제출과 README에서 사용할 claim ceiling이 적절한가.
5. 추가로 반드시 비교해야 할 primary source가 있는가. 추가 source 발견은 audit 방향을 재개방하지 않고 factual register 보강으로 처리한다.

Canonical status:

```text
HUMAN_PROVIDED / ACCEPTED / CLOSED
```
