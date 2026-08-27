# AISCC Architecture

## 1. document status

| field | value |
|---|---|
| document_id | `AISCC-P1-1-ARCHITECTURE-V1` |
| task_id | `20260827_1008_aiscc-p1-1-human-gate-result-projection-alignment-rework-1` |
| work_type | `REWORK` |
| result_status | `ACCEPTED / CLOSED` |
| authority status | repository canonical accepted baseline |
| implementation status | `NOT_IMPLEMENTED` |
| semantic owner | AISCC core domain model과 aggregate ownership boundary |
| paired contract | `.aiassistant/rules/AISCC_ORCHESTRATION.md` |
| predecessor judgment | `HOLD_REWORK_REQUIRED` — HumanGateStatus/HumanResult projection alignment required |
| human acceptance provenance | `2026-08-27` Human P1-1 final review: `ACCEPTED` |
| terminal cycle | `.aiassistant/records/aiscc/cycles/20260827_1115_aiscc-p1-1-core-domain-state-machine-design-final-acceptance-1.cycle.md` |

이 문서는 Human P1-1 final review에서 `ACCEPTED`된 repository canonical design baseline이다. 구현 결과는 아니며 runtime/state-machine implementation status는 `NOT_IMPLEMENTED`다.

## 2. architecture scope

AISCC는 Coding Agent가 아니라 software work의 권위, 증거, 상태 전이, Human judgment, provenance를 통제하는 `Software Engineering Governance Control Plane`이다.

```text
Coding Agent
→ action / target / evidence candidate를 제안

AISCC System
→ TaskContract와 authoritative state/version을 기준으로 전이를 평가·입장

Human / Command Center
→ 지정된 policy, verification, business judgment를 소유
```

초기 MVP는 하나의 AISCC system boundary와 하나의 authoritative logical state store를 가정한다. 이 가정은 단일 프로세스나 특정 DB 제품을 뜻하지 않는다. 어떤 배포 형태에서도 동일 `WorkRun`의 authoritative state/version을 둘 이상의 독립 owner가 동시에 확정해서는 안 된다.

P1-1이 소유하는 것은 core domain 이름, semantic ownership, exact workflow-state contract, transition authority, durability/concurrency 요구다. 다음은 소유하지 않는다.

- product/runtime, API, DB schema 또는 UI 구현
- provider/model/tool adapter 구현
- sandbox/permission/network/secret 상세 정책과 safeguard
- evidence type별 admission 알고리즘
- Human Gate UI/identity/approval 구현
- Cycle 저장 구현과 memory selection 알고리즘
- deployment/provider/resource/credential/billing 설정

## 3. canonical dimensions

서로 다른 사실을 하나의 `status` 필드로 합치지 않는다.

| dimension | exact values 또는 owner contract | authoritative owner | 목적 |
|---|---|---|---|
| `WorkflowState` | `READY`, `RUNNING`, `ADMISSION_PENDING`, `HUMAN_REQUIRED`, `BLOCKED`, `REWORK_REQUIRED`, `ACCEPTED`, `REJECTED`, `FAILED` | System transition authority | 한 `WorkRun`의 governance lifecycle |
| `ExecutionStatus` | `NOT_STARTED`, `RUNNING`, `EXECUTOR_COMPLETED`, `EXECUTION_FAILED` | System이 execution adapter event를 입장하여 기록 | Executor 수행 진행과 산출 완료 여부 |
| `HumanGateStatus` | `NOT_REQUIRED`, `PENDING`, `RESOLVED`, `CANCELLED` | System durable gate projection; outcome-neutral | Human gate lifecycle만 표현 |
| `HumanGateSuspensionStatus` | `NOT_APPLICABLE`, `ACTIVE`, `SUSPENDED` | System durable gate projection; `PENDING` gate에만 `ACTIVE`/`SUSPENDED` 허용 | BLOCKED 중 gate wait의 일시 중단 여부 |
| `JudgmentStatus` | `PENDING`, `ACCEPTED`, `REJECTED`, `HOLD_REWORK_REQUIRED` | `TaskContract`의 `judgment_owner_policy`가 정한 Human/Command Center/System semantic owner; System이 immutable Judgment를 입장 | Task outcome의 semantic 판단 |
| `RuntimeMode` | `OWNER_SELF_DOGFOOD`, `PUBLIC_RECORDED_REPLAY`, `PUBLIC_BOUNDED_LIVE` | runtime policy owner | permission, data, execution policy 선택 |

`ExecutionStatus=EXECUTOR_COMPLETED`는 `WorkflowState=ACCEPTED`를 뜻하지 않는다. `HumanGateStatus=RESOLVED`는 Human input 하나가 admitted됐다는 lifecycle 사실일 뿐 Task success가 아니다. `JudgmentStatus=ACCEPTED`도 해당 authoritative `Judgment`가 System에 입장된 뒤 별도 transition admission이 발생하기 전에는 workflow mutation이 아니다. Project-level `CLOSED`는 `CycleRecord`/phase projection의 판단이며 `WorkRun.ACCEPTED`와 동일 개념이 아니다.

## 4. core domain glossary

각 canonical term은 하나의 의미만 가진다. 유사 표현은 아래 term의 설명용 alias일 뿐 별도 aggregate가 아니다.

| term | exact semantics | semantic owner |
|---|---|---|
| `Project` | Task, run, accepted policy, Cycle lineage와 stable next-action projection을 묶는 최상위 governance identity. source repository 자체와 동일하지 않다. | Project governance owner / Command Center |
| `TaskContract` | 목표, 비목표, allowed/forbidden scope, authority input, evidence ownership, stop condition을 고정한 immutable versioned work contract. | Command Center; Human이 policy 선택을 확정 |
| `WorkRun` | 하나의 `TaskContract` version을 실행·평가하는 authoritative execution aggregate. current `WorkflowState`, monotonic `state_version`, execution status와 immutable event refs를 가진다. | AISCC System |
| `WorkflowState` | `WorkRun` lifecycle의 exact finite state 중 하나. Agent prose가 아니라 admitted transition만 변경한다. | AISCC System |
| `TransitionRequest` | 특정 observed state/version에서 target state로 이동해 달라는 immutable proposal. mutation 명령이 아니다. | requester가 생성; System이 보존·평가 |
| `TransitionEvaluation` | current state/version, applicable policy와 abstract guard result를 결합한 immutable 평가 기록. | System transition evaluator |
| `TransitionDecision` | authoritative current state/version과 target-specific guards를 평가한 기계적 `ADMITTED` 또는 `DENIED` 결정. semantic `Judgment`를 만들거나 대신하지 않는다. `TransitionAdmission`은 `ADMITTED` variant다. | System transition authority |
| `EvidenceRequirementRef` | `TaskContract`가 요구하는 evidence predicate와 owner/type/freshness/applicability rule의 stable reference. 상세 규칙은 P1-6 소유다. | TaskContract / future P1-6 catalog |
| `EvidenceCandidateRef` | Agent, Executor, tool 또는 Human이 제출한 proof 후보를 가리키는 immutable ref. 존재만으로 requirement 충족이 아니다. | producer가 제출; System evidence boundary가 보존 |
| `AdmittedEvidenceRef` | P1-6 admission 결과가 특정 requirement, source state/version, provenance에 binding됐음을 가리키는 immutable ref. | System evidence admission owner |
| `HumanGate` | designated Human input 없이는 authoritative `Judgment`를 만들 수 없게 하는 system-managed durable lifecycle record. status는 outcome-neutral이며 result content를 복제하지 않는다. | System record; designated Human이 result content를 소유 |
| `HumanResult` | designated Human이 특정 gate/task/run/gate-version에 제출한 immutable `APPROVE`, `REWORK`, `REJECT` input. admitted result는 gate를 `RESOLVED`로 투영하지만 그 자체가 `Judgment`나 state mutation은 아니다. | designated Human; System이 owner/applicability/version을 admission |
| `JudgmentCandidate` | Agent reviewer, deterministic evaluator 또는 Human input에서 만들어진 semantic outcome proposal. authoritative `Judgment`가 아니다. | candidate producer |
| `Judgment` | Task/evidence/Human policy 아래 current work outcome을 `ACCEPTED`, `REJECTED`, `HOLD_REWORK_REQUIRED` 중 하나로 의미화한 immutable authoritative record. terminal/rework transition보다 먼저 입장되며 `TransitionDecision`과 다르다. | `TaskContract.judgment_owner_policy`가 정한 Human/Command Center/System owner; System이 입장 |
| `CycleRecord` | Task, run, evidence, transition, judgment, commit/result와 next action의 admitted public provenance를 append-only로 연결한 record. raw session dump가 아니다. | Command Center; future P1-8 admission owner |
| `NextAction` | accepted project projection과 blocker/queue policy에서 선택된 stable action. Agent recommendation은 candidate일 뿐이다. | Command Center/System selection policy |

### 4.1 Human gate lifecycle and result mapping

`HumanGateStatus`의 exact outcome-neutral lifecycle set은 `NOT_REQUIRED`, `PENDING`, `RESOLVED`, `CANCELLED`다.

| status | exact meaning | admitted HumanResult ref | suspension status |
|---|---|---|---|
| `NOT_REQUIRED` | current Task/policy evaluation에 applicable Human gate가 없음 | none | `NOT_APPLICABLE` |
| `PENDING` | gate가 열렸고 admitted HumanResult가 아직 없음 | none | `ACTIVE` 또는 `SUSPENDED` |
| `RESOLVED` | exact gate/version에 HumanResult 하나가 admitted됨 | exactly one | `NOT_APPLICABLE` |
| `CANCELLED` | gate가 superseded/inapplicable이거나 WorkRun terminal failure로 더 이상 result를 받지 않음 | none | `NOT_APPLICABLE` |

Allowed lifecycle projection:

```text
NOT_REQUIRED → PENDING
PENDING / ACTIVE → RESOLVED
PENDING / ACTIVE ↔ PENDING / SUSPENDED
PENDING → CANCELLED
```

`RESOLVED`와 `CANCELLED`는 해당 gate record에 대해 immutable terminal lifecycle projections다. correction/reconsideration은 기존 gate/result mutation이 아니라 새 gate 또는 explicit superseding record를 사용한다.

`HumanResult`의 exact outcome set은 `APPROVE`, `REWORK`, `REJECT`다. 세 outcome 모두 designated Human만 제출하고 System이 owner, requirement applicability, task/run identity, gate version, current state/version을 검사해 admission한다. result admission event와 `PENDING/ACTIVE → RESOLVED/NOT_APPLICABLE` projection은 atomic하게 기록되거나 둘 다 적용되지 않는다. wrong owner/proof type, non-applicable, stale 또는 duplicate result는 gate projection을 바꾸지 않는다. gate 하나에는 admitted result가 정확히 하나만 허용된다.

| HumanResult | admitted gate projection | semantic effect | does NOT imply |
|---|---|---|---|
| `APPROVE` | `HumanGateStatus=RESOLVED`; `result_ref.outcome=APPROVE` | policy-selected `ACCEPTED` Judgment를 만들 수 있는 Human input | `JudgmentStatus=ACCEPTED` 또는 `WorkflowState=ACCEPTED` |
| `REWORK` | `HumanGateStatus=RESOLVED`; `result_ref.outcome=REWORK` | policy-selected `HOLD_REWORK_REQUIRED` Judgment를 만들 수 있는 Human input | automatic `JudgmentStatus=HOLD_REWORK_REQUIRED` 또는 `WorkflowState=REWORK_REQUIRED` |
| `REJECT` | `HumanGateStatus=RESOLVED`; `result_ref.outcome=REJECT` | policy-selected `REJECTED` Judgment를 만들 수 있는 Human input | `JudgmentStatus=REJECTED` 또는 `WorkflowState=REJECTED` |

`HUMAN_REQUIRED → BLOCKED`가 admitted되면 gate는 `PENDING`을 유지하고 suspension만 `ACTIVE → SUSPENDED`로 바뀐다. suspended gate에 제출된 result는 candidate로 보존할 수 있지만 admission은 deferred되며 gate는 `RESOLVED`가 되지 않는다. blocker resolution 뒤 System은 exact gate의 owner/applicability/task/run/gate-version을 재검증하고 `BLOCKED → HUMAN_REQUIRED`를 admit하여 `PENDING/ACTIVE`로 복귀시킨 다음 candidate를 fresh current state/version에서 다시 검사한다. unresolved pending gate가 없을 때만 `BLOCKED → READY`가 허용된다. irrecoverable `BLOCKED → FAILED`는 pending gate를 `CANCELLED`로 만들고 이후 result를 deny한다.

```text
HumanGate lifecycle
!= HumanResult semantic outcome
!= authoritative Judgment
!= TransitionDecision
!= WorkflowState
```

## 5. aggregate and ownership boundaries

| aggregate / record | mutable by | history semantics | system-state relation | Agent-output relation | Human-decision relation | future persistence owner |
|---|---|---|---|---|---|---|
| `Project` | Project governance owner; System은 admitted projection만 갱신 | identity와 accepted decision lineage 보존 | 여러 `WorkRun`과 current project projection의 root | Agent는 project 변경 제안만 가능 | policy/closure decision refs를 연결 | P1-8 project memory/cycle admission |
| `TaskContract` | 발행 전 Command Center; 발행 후 수정 대신 새 version | issued version immutable | `WorkRun`의 guard 기준 | Agent는 계약을 수정하거나 범위를 확장할 수 없음 | Human policy choice가 있으면 provenance로 고정 | P1-4/P1-8 durable contract store |
| `WorkRun` | System transition authority만 current projection mutation | transition/event history append-only | authoritative workflow state owner | Agent output은 submission/candidate ref만 생성 | admitted Human result를 gate ref로 연결 | P1-4 kernel persistence |
| `TransitionRequest` | 생성 후 immutable | 모든 request, stale/denied 포함 보존 | mutation 이전의 proposal | Agent가 생성할 수 있으나 효력 없음 | Human/System도 requester가 될 수 있음 | P1-4 transition log |
| `TransitionEvaluation` | System evaluator가 생성 후 immutable | guard result와 policy version 보존 | decision의 근거 | Agent self-assessment는 evaluation이 아님 | Human ref가 필요한 guard를 표현 | P1-4 transition log; P1-6/P1-7 refs |
| `TransitionDecision` | System transition authority가 생성 후 immutable | admission/denial 모두 append-only | admitted variant만 atomic state mutation과 결합; applicable Judgment ref를 target guard로 검사 | Agent가 결정할 수 없음 | Human result/Judgment와 별개인 mechanical decision | P1-4 transition log |
| evidence refs | candidate producer와 System admission owner를 분리 | candidate/admission/rejection provenance immutable | admitted ref만 guard를 충족 | Agent output은 candidate까지만 | Human-owned proof는 Human ref 없이는 입장 불가 | P1-6 evidence admission |
| `HumanGate` / `HumanResult` | System이 outcome-neutral lifecycle/suspension projection open·resolve·cancel; Human이 result 제출 | request/candidate/admission/lifecycle/suspension history append-only | `PENDING` 동안 authoritative Judgment와 terminal/rework transition 금지; `RESOLVED`도 state mutation 아님 | Agent는 HumanResult를 대행할 수 없음 | designated Human이 outcome content 소유 | P1-7 human gate/judgment |
| `JudgmentCandidate` | producer가 생성 후 immutable | accepted/rejected candidate 모두 provenance 보존 가능 | state mutation 효력 없음 | Agent review는 여기까지만 가능 | admitted HumanResult를 input으로 참조 가능 | P1-7 judgment pipeline |
| `Judgment` | policy-selected semantic owner가 결정하고 System이 입장; 정정은 superseding Judgment | immutable supersession lineage append-only | terminal/rework transition의 선행 guard input이며 mutation 자체는 아님 | Agent가 authoritative Judgment를 발행할 수 없음 | Human-owned policy이면 admitted HumanResult가 필수 input | P1-7 judgment persistence |
| `CycleRecord` | admission 전 Command Center; admission 후 immutable, correction은 additive successor | append-only curated history | project projection 재구성 근거 | raw Agent prose 자동 입장 금지 | accepted/hold/reject Human provenance 연결 | P1-8 cycle admission |
| `NextAction` | System/Command Center projection owner | selection event 보존, current projection은 교체 가능 | accepted state 이후의 별도 project projection | Agent recommendation은 candidate | policy choice 시 Human judgment 반영 | P1-8 projection owner |

## 6. authority and information flow

아래 ordering은 `ACCEPTED`, `REJECTED`, `REWORK_REQUIRED` semantic outcome routing에 적용한다.

```text
Agent / Executor output
→ EvidenceCandidateRef
→ AdmittedEvidenceRef
→ review / JudgmentCandidate
→ HumanGate `PENDING / ACTIVE` when required
→ admitted HumanResult + HumanGate `RESOLVED` when required
→ authoritative Judgment admitted
→ TransitionRequest
→ TransitionEvaluation
→ TransitionDecision
→ atomic authoritative state/version mutation when admitted
→ CycleRecord admission
→ NextAction projection
```

`READY`, `RUNNING`, `ADMISSION_PENDING`, `HUMAN_REQUIRED`, `BLOCKED`, `FAILED` 같은 control/execution transition은 target-specific non-Judgment guard로 입장할 수 있다. 특히 `HUMAN_REQUIRED`는 authoritative Judgment를 만들기 전에 Human input을 기다리기 위한 pre-Judgment control transition이다. 이 예외는 terminal/rework outcome이 Judgment를 선행해야 한다는 규칙을 완화하지 않는다.

`TaskContract.judgment_owner_policy`는 semantic owner를 exact하게 선택한다.

- `SYSTEM_DETERMINISTIC`: versioned policy가 admitted evidence와 execution facts를 결정적으로 평가해 `Judgment`를 생성한다. Agent review를 입력 truth로 사용하지 않는다.
- `HUMAN`: designated Human의 admitted `HumanResult`가 필수 input이며 Human이 semantic outcome을 소유한다. System은 provenance와 applicability를 확인해 별도 `Judgment` record로 입장한다.
- `COMMAND_CENTER`: Command Center rubric/owner가 semantic outcome을 소유하며 System이 별도 `Judgment`로 입장한다. Human-owned gate가 함께 요구되면 admitted `HumanResult`도 선행 input이다.

발행된 `TaskContract`에서 owner policy를 추론하거나 실행 중 자동 변경하지 않는다. `Judgment` 정정은 기존 record mutation이 아니라 `supersedes_judgment_id`를 가진 additive successor다. current Task/run/version에 applicable한 unsuperseded Judgment만 transition guard가 될 수 있다.

필수 경계:

- `AgentOutput != WorkflowState`
- `EvidenceCandidateRef != AdmittedEvidenceRef`
- `Executor completed != evidence sufficient`
- `Human result submitted != Human result admitted`
- `HumanGateStatus=RESOLVED != HumanResult outcome`
- `HumanResult != Judgment`
- `Judgment != TransitionDecision`
- `Judgment exists != state automatically mutated`
- `WorkRun ACCEPTED != project/phase CLOSED`
- `NextAction proposal != authoritative NextAction`

## 7. runtime mode separation

`RuntimeMode`는 `WorkRun` 생성 시 고정되는 execution context dimension이다. mode 변경은 같은 run의 state transition이 아니며, 정책이 허용할 때 새 run/context를 만든다.

| mode | effect on policy | effect on workflow truth |
|---|---|---|
| `OWNER_SELF_DOGFOOD` | owner-authorized repository/data/tool profile과 P1 security policy 적용 | 동일 state set, admission, Human gate, provenance 규칙 사용 |
| `PUBLIC_RECORDED_REPLAY` | read-only stored trace; page/replay LLM inference `0`; run mutation 금지 | 과거 admitted trace를 표시할 뿐 새 workflow truth를 만들지 않음 |
| `PUBLIC_BOUNDED_LIVE` | fixed synthetic repository, allowlisted scenario, bounded calls/retry/time/budget, public deny-by-default profile | 동일 state/authority semantics; 제한이 완화되거나 terminal admission이 우회되지 않음 |

mode가 permission/runtime policy를 선택할 수는 있지만 `PUBLIC_BOUNDED_LIVE_ACCEPTED` 같은 workflow state를 만들지 않는다. Replay availability도 prior Live run의 success나 current execution을 의미하지 않는다.

## 8. persistence, concurrency, and recovery semantics

### 8.1 restart-surviving truth

다음은 process restart 전에 durable해야 한다.

- stable `Project`, `TaskContract`, `WorkRun` identifiers와 exact contract version
- current `WorkflowState`, `ExecutionStatus`, `state_version`, `RuntimeMode`
- 모든 `TransitionRequest`, `TransitionEvaluation`, `TransitionDecision`
- admitted mutation의 source/result state와 version
- evidence requirement/candidate/admission refs와 provenance binding
- `HumanGateStatus`, `HumanGateSuspensionStatus`, gate version, submitted/admitted `HumanResult` ref
- Judgment candidate, authoritative Judgment, owner-policy와 supersession refs
- `CycleRecord`, `NextAction` provenance refs
- retry/rework lineage, parent run/request, reason

in-memory state만을 authoritative truth로 인정하지 않는다.

### 8.2 monotonic version rule

각 `WorkRun`은 `state_version`을 가진다. admitted transition 하나는 정확히 한 번 version을 증가시킨다. denial은 state/version을 바꾸지 않지만 immutable decision event를 남긴다. mutation과 admission event는 분리되어 관측되는 partial success를 허용하지 않는다.

```text
request.observed_state/version
== authoritative current state/version
→ guard evaluation eligible

otherwise
→ STALE_REQUEST denial
→ retry requires a new request from fresh state/version
```

동일 idempotency identity의 재전송은 기존 decision을 재사용하거나 duplicate로 deny해야 하며 두 번 mutation해서는 안 된다. DB lock/transaction 기술은 P1-4가 선택하되 이 invariant를 만족해야 한다.

### 8.3 append-only and projections

Append-only:

- issued `TaskContract` versions
- transition requests/evaluations/decisions
- evidence candidate/admission/rejection refs
- Human gate lifecycle/suspension and request/result/admission events
- Judgment candidates, admitted judgments와 supersession lineage
- Cycle records와 correction lineage

Mutable current projection:

- `WorkRun` current state/status/version
- current Human gate lifecycle/suspension projection
- Project current phase/accepted-baseline/NextAction projection

projection은 append-only provenance에서 deterministic하게 재구성 가능해야 한다. recovery는 마지막 Agent message가 아니라 durable admitted event와 version을 사용한다.

### 8.4 stable identifiers and minimum transition provenance

Stable identity 최소 집합:

- `project_id`, `task_contract_id`, `task_contract_version`, `work_run_id`
- `transition_request_id`, `transition_evaluation_id`, `transition_decision_id`
- evidence requirement/candidate/admission IDs
- `human_gate_id`, `human_result_id`, `judgment_candidate_id`, `judgment_id`, `cycle_record_id`

전이를 재구성하기 위한 최소 provenance는 run/task, source state/version, requested target, requester identity/type, runtime mode, guard identifiers/results, evidence/Human refs, applicable authoritative Judgment와 owner-policy ref, policy/contract version, admission/denial reason, admitting owner, timestamp, resulting state/version이다.

## 9. future owner handoff

| phase | owns | P1-1 invariant it must preserve |
|---|---|---|
| P1-2 Security / Sandbox / Runtime Boundary Design | mode별 filesystem/process/tool/network/secret/permission 및 fail-closed policy | mode는 state와 분리; public profile이 authority를 우회하지 않음 |
| P1-3 safeguard implementation/verification | P1-2 safeguard 구현과 applicable proof | safeguard proof와 workflow acceptance proof를 대체하지 않음 |
| P1-4 state machine kernel implementation | exact state/version, request/evaluation/decision, atomic admission, durable recovery | Agent mutation 금지, stale overwrite 금지, deterministic trace |
| P1-5 provider/tool execution | Agent/provider invocation과 tool execution adapter | output은 candidate/event이며 state mutation 권한 없음 |
| P1-6 evidence admission | type/owner/freshness/provenance/applicability predicates와 admission | candidate/admitted ref 분리, proof non-substitution |
| P1-7 human gate/judgment | Human identity, request/result, lifecycle/suspension projection, judgment admission과 UX | exact outcome-neutral status/mapping 유지; silence와 `RESOLVED` 모두 Task success 아님 |
| P1-8 memory/cycle admission | curated Cycle, correction/supersession, NextAction projection | raw session 자동 입장 금지; project closure와 run acceptance 분리 |

P1-1은 위 interface constraint만 정하며 해당 phase의 구현·상세 설계를 선행하지 않는다.

## 10. claim and implementation boundary

- custom explicit state machine은 accepted architecture decision이지만 현재 구현되지 않았다.
- 이 문서의 diagram/table은 runtime proof가 아니다.
- evidence gate, persistent memory, orchestration, human gate, provenance는 known prior-art primitive이며 AISCC의 최초 발명으로 주장하지 않는다.
- candidate가 Human review를 통과하기 전에는 `AISCC-P1-1-ARCHITECTURE-CANDIDATE-V3`를 accepted canonical design으로 표현하지 않는다.
