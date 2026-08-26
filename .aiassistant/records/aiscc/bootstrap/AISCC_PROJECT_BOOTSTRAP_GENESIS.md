# AISCC Bootstrap Seed Metadata

- seed_id: `AISCC-BOOTSTRAP-SEED-V1`
- generated_at: `2026-08-26 00:07 KST`
- seed_role: `PRE_REPOSITORY_BROWSER_PROJECT_BOOTSTRAP`
- authority: `TEMPORARY_BOOTSTRAP_AUTHORITY`
- immutable_after_upload: `true`
- retirement_condition: `FIRST_AISCC_REPOSITORY_CANONICAL_MIRROR_V1_SYNC_CONFIRMED`
- domain_leakage_policy: `NO_SOURCE_PROJECT_PRODUCT_OR_DOMAIN_POLICY`

---


# AI Software Command Center Project Bootstrap

## 1. 문서 지위

이 문서는 새 Browser Project가 프로젝트 목적과 이미 확정된 출발 결정을 이해하기 위한 bootstrap snapshot이다.

다음은 아직 이 문서의 권위가 아니다.

- 최종 architecture
- 최종 state machine contract
- 최종 security/sandbox policy
- 최종 API/data model
- 최종 competition submission copy

위 항목은 repository 생성 전후의 별도 `DESIGN_AUDIT` 또는 `DOC_BASELINE_UPDATE`에서 확정한다.

## 2. 프로젝트 정의

프로젝트명:

```text
AI Software Command Center (AISCC)
```

현재 제품 thesis:

> AI Coding Agent 자체를 만드는 제품이 아니라, AI Agent가 수행한 software work를 Task Contract, authority, evidence ownership, proof admission, human judgment, durable decision provenance 아래에서 관리하는 Software Engineering Governance Control Plane.

## 3. 해결하려는 문제

Coding Agent의 코드 작성 능력이 높아져도 장기 프로젝트에서는 다음 문제가 남는다.

- 어떤 project policy가 현재 권위인지 불명확하다.
- Agent가 `tested`, `reviewed`, `done`이라고 말해도 실제 proof와 다를 수 있다.
- 서로 다른 proof type을 과장하여 대체할 수 있다.
- 사람이 해야 하는 browser/business/security 판단을 Agent가 완료했다고 주장할 수 있다.
- 여러 Agent/session 사이에서 실패·결정·판정의 provenance가 사라진다.
- 실행 history가 raw chat으로만 남아 다음 행동 선택에 재사용하기 어렵다.
- 사람이 여러 Agent의 채팅을 직접 감독하면서 context switching 병목이 생긴다.

AISCC는 Agent autonomy를 무제한으로 확대하기보다, **AI·System·Human의 권한을 분리하고 software work admission을 통제**한다.

## 4. 이미 확정된 출발 결정

### 4.1 참가 목표

- 대회 참가와 실제 과제 제출을 수행한다.
- 상위 순위는 stretch goal이다.
- 최소 성공은 작동하는 프로젝트, 공개 가능한 개발 provenance, 제출 완료다.
- 과장된 세계 최초 주장보다 정직한 prior-art boundary와 실제 동작을 우선한다.

### 4.2 orchestration 방향

- Agent orchestration core는 **직접 구현한 explicit state machine**을 사용한다.
- LangGraph를 orchestration core로 사용하지 않는다.
- 첫 구현이 조잡하더라도 state, transition, admission rule의 소유권을 프로젝트가 직접 가진다.
- LLM은 다음 상태를 자유 형식으로 결정하지 않는다.

### 4.3 prior-art boundary

AISCC는 다음 primitive를 발명했다고 주장하지 않는다.

- specification-driven development
- coding-agent dispatch/orchestration
- evidence-gated lifecycle
- human approval/permission gate
- persistent project memory
- agent session provenance
- reviewer agent
- multi-agent execution

경쟁 영역은 위 primitive의 발명 주장이 아니라 **일관된 governance model로의 통합과 실제 self-dogfooding 증명**이다.

### 4.4 Self-Dogfooding

P2-4 Self-Dogfooding을 핵심 시연 전략으로 채택한다.

```text
초기 kernel 이전
→ Browser Command Center + IDE Executor + Human으로 AISCC 개발

kernel usable 이후
→ AISCC가 자신의 후속 개발 task를 실행·검증·판정·기록
```

최종 발표의 강한 증거는 다음이다.

> AISCC의 후반부 개발 자체가 AISCC의 Task Contract, state transition, evidence admission, human gate, cycle memory를 통해 수행되었다.

## 5. 핵심 권한 분리

```text
AI owns
- reasoning
- plan proposal
- code/change proposal
- review proposal
- evidence candidate production

System owns
- workflow state
- transition admission
- required evidence
- proof type compatibility
- tool permission
- retry/rework routing
- terminal status admission

Human owns
- policy decision
- exceptional approval
- business acceptance
- real-account/browser/visual verification when designated
- unresolved conflict resolution
- final competition submission
```

Agent output은 system state가 아니다. Agent output은 transition engine이 평가할 claim 또는 candidate다.

## 6. MVP 업무 흐름

```text
Task Contract
→ Context/Authority Load
→ Plan
→ Plan Admission
→ Execute
→ Evidence Collection
→ Evidence Admission
→ Review
→ Human Gate when required
→ Judgment
→ Curated Cycle Memory
→ Next Action
```

초기 state 후보:

```text
CREATED
CONTEXT_READY
PLANNED
EXECUTING
VERIFYING
REVIEWING
REWORK_REQUIRED
HUMAN_REQUIRED
ACCEPTED
COMPLETED
BLOCKED
FAILED
```

이 목록은 최종 contract가 아니며 P1-1 `Core Domain / State Machine Design`이 소유한다.

## 7. 초기 기술 방향

아래는 구현 후보이며 architecture acceptance 전까지 확정 기술 계약이 아니다.

```text
Frontend: React / Next.js / TypeScript
Backend: Python / FastAPI / Pydantic
Persistence: PostgreSQL / JSONB
Realtime UI: SSE
Execution isolation: Docker
Source isolation: Git worktree
Agent provider: OpenAI first, provider abstraction later
Workflow: custom explicit state machine
```

## 8. 비목표

- 범용 Coding Agent를 새로 만드는 것
- Agent framework 기능 수 경쟁
- unrestricted autonomous agent swarm
- 첫 버전부터 production-scale distributed orchestration
- Kubernetes/Kafka/다수 microservice 도입
- 자체 foundation model 또는 fine-tuning
- 이미 존재하는 primitive의 최초 발명 주장
- 경쟁 제품 전체를 단기간에 복제

## 9. 개발 단계

### P0 — Bootstrap / Authority

- P0-1 Bootstrap Ruleset Extraction and Browser Project Source Seed
- P0-2 Product Thesis / Prior-Art Boundary Baseline
- P0-3 Browser Project Bootstrap
- P0-4 Repository Bootstrap / Canonical Authority / Git policy
- P0-5 First Project Source Mirror v1

### P1 — Governance Kernel

- Core domain / explicit state machine design
- Sandbox / tool permission security design
- State machine kernel
- Agent provider / tool execution
- Evidence admission
- Human gate / judgment
- Project memory / cycle admission

### P2 — Demonstration

- Command Center Web UI
- Synthetic Demo Repository
- Canonical Scenario Pack
- Self-Dogfooding Cutover

### P3 — Proof / Submission

- Comparative evaluation
- Public repository documentation
- Competition submission package

## 10. Self-Dogfooding cutover gate 후보

다음이 모두 충족되기 전에는 self-dogfooding 완료를 주장하지 않는다.

- explicit state transition engine 실행 가능
- task contract 저장/조회 가능
- required evidence admission 가능
- human-owned evidence가 system에서 차단됨
- forbidden action/tool permission guard 존재
- rework/blocked recovery 가능
- durable cycle record 생성 가능
- sandbox 또는 동등한 실행 격리 존재
- 사람이 cutover 승인

## 11. 최소 데모 시나리오

1. 정상 구현 → required evidence PASS → ACCEPT
2. test/evidence 부족 → transition denied → REWORK
3. canonical policy conflict → code mutation 전 HUMAN_REQUIRED 또는 BLOCKED
4. Agent가 human-owned browser QA를 완료했다고 주장 → claim reject → HUMAN_PENDING

## 12. 현재 open decision

- detailed product thesis와 prior-art comparison matrix
- repository root `AGENTS.md`의 Git tracking policy
- final package/module architecture
- tool/network/secret sandbox boundary
- exact state and transition model
- Agent provider abstraction
- synthetic demo repository domain
- self-dogfooding cutover acceptance test

## 13. 바로 다음 작업

`AISCC Product Thesis and Prior-Art Boundary Baseline`을 수행한다.
