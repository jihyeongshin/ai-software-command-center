# AISCC Orchestration

## 1. document status

| field | value |
|---|---|
| document_id | `AISCC-P1-1-ORCHESTRATION-V1` |
| task_id | `20260827_1008_aiscc-p1-1-human-gate-result-projection-alignment-rework-1` |
| work_type | `REWORK` |
| result_status | `ACCEPTED / CLOSED` |
| implementation status | `NOT_IMPLEMENTED` |
| orchestration core | custom explicit state machine; LangGraph core `NOT_USED` |
| semantic owner | workflow state, transition authority와 admission semantics |
| paired contract | `.aiassistant/rules/AISCC_ARCHITECTURE.md` |
| predecessor judgment | `HOLD_REWORK_REQUIRED` — HumanGateStatus/HumanResult projection alignment required |
| human acceptance provenance | `2026-08-27` Human P1-1 final review: `ACCEPTED` |
| terminal cycle | `.aiassistant/records/aiscc/cycles/20260827_1115_aiscc-p1-1-core-domain-state-machine-design-final-acceptance-1.cycle.md` |

이 문서는 Human P1-1 final review에서 `ACCEPTED`된 repository canonical orchestration design baseline이다. 실행 가능한 state machine이나 runtime proof는 아니며 implementation status는 `NOT_IMPLEMENTED`다.

## 2. authority contract

```text
Agent
→ MAY propose action / target / evidence candidate
→ MUST NOT mutate authoritative workflow state

System
→ owns transition evaluation, admission/denial, and authoritative state mutation

Human
→ owns designated policy / business / verification decisions
→ submits `HumanResult`; System admits it as a Judgment input, not as state mutation

Judgment owner selected by TaskContract policy
→ owns semantic `ACCEPTED` / `REJECTED` / `HOLD_REWORK_REQUIRED` outcome

System transition authority
→ separately decides whether that Judgment and all target guards admit mutation

Terminal state
→ cannot be established from Agent prose alone
```

`Agent "done"`, process exit `0`, generated report, evidence candidate, `HumanResult`, authoritative `Judgment` 또는 Human silence 중 어느 것도 그 자체로 transition admission event가 아니다.

## 3. exact canonical state set

`WorkflowState`의 exact finite set은 아래 9개다. 이 목록 밖의 값은 invalid다.

```text
READY
RUNNING
ADMISSION_PENDING
HUMAN_REQUIRED
BLOCKED
REWORK_REQUIRED
ACCEPTED
REJECTED
FAILED
```

### 3.1 state definitions

| state | meaning | terminal | request entry by | admissible predecessors | required abstract predicates | allowed outgoing | Human input | retry/rework and recovery |
|---|---|---:|---|---|---|---|---|---|
| `READY` | admitted `TaskContract`와 runtime context가 있고 실행을 시작할 수 있음 | No | System, authorized operator; Agent may propose only | creation, `BLOCKED`, `REWORK_REQUIRED` | contract/version valid; required baseline available; mode policy selected; unresolved pending Human gate 없음 | `RUNNING` | Not inherently | restart 후 durable contract/state/version에서 재개; rework revision/ref가 있으면 보존 |
| `RUNNING` | admitted execution attempt가 진행 중 | No | execution adapter/System; Agent may propose start | `READY` | start authorization; permission profile ref; no unresolved stop guard | `ADMISSION_PENDING`, `BLOCKED`, `REWORK_REQUIRED`, `FAILED` | Not inherently | transient retry는 execution policy 안에서 event로 기록; governance rework는 `REWORK_REQUIRED` |
| `ADMISSION_PENDING` | Executor submission/candidates는 존재하나 evidence/Judgment/terminal admission pipeline이 끝나지 않음 | No | Agent/Executor/System may request; System admits | `RUNNING` | execution completion event admitted; submission provenance bound | `HUMAN_REQUIRED`, `BLOCKED`, `REWORK_REQUIRED`, `ACCEPTED`, `REJECTED` | Contract-dependent | restart 시 evidence/Judgment candidate refs로 평가 재개; duplicate completion은 idempotent |
| `HUMAN_REQUIRED` | designated Human gate의 input 또는 그 input에 따른 Judgment/transition routing이 완료되지 않음 | No | System only after gate-required evaluation/recovery; Agent may propose target but cannot open/resolve gate | `ADMISSION_PENDING`, `BLOCKED`, `REWORK_REQUIRED` | applicable Human requirement; open gate가 `PENDING/ACTIVE`, 또는 admitted result gate가 `RESOLVED`이고 outcome transition이 아직 미입장 | `ACCEPTED`, `REWORK_REQUIRED`, `REJECTED`, `BLOCKED` | Yes | silence/absence 동안 `PENDING/ACTIVE`; admission 뒤 gate는 `RESOLVED`지만 workflow는 별도 Judgment/transition 전까지 유지 |
| `BLOCKED` | 현재 실행자가 해결할 수 없는 prerequisite, authority conflict 또는 external dependency가 unresolved | No | Agent/System/Human may report/request; System admits | `RUNNING`, `ADMISSION_PENDING`, `HUMAN_REQUIRED` | blocker identity, owner, resumability와 reason recorded | `READY`, `HUMAN_REQUIRED`, `REWORK_REQUIRED`, `FAILED` | Sometimes | suspended pending gate가 있으면 blocker resolution 뒤 `HUMAN_REQUIRED`; gate가 없으면 `READY`; non-Human correction이면 `REWORK_REQUIRED`; abandoned/irrecoverable이면 `FAILED` |
| `REWORK_REQUIRED` | current execution attempt 또는 submission이 그대로는 계속되거나 accepted될 수 없지만 같은 contract lineage에서 명시된 correction이 가능 | No | policy-selected Judgment owner/System; Agent may propose but not decide | `RUNNING`, `ADMISSION_PENDING`, `HUMAN_REQUIRED`, `BLOCKED` | applicable authoritative `HOLD_REWORK_REQUIRED` Judgment, exact rework reason, failed guard refs, next revision boundary | `READY`, `HUMAN_REQUIRED`, `REJECTED` | Judgment policy-dependent | 새 attempt/revision ref를 만든 뒤 `READY`; 새 Human result가 필요하면 `HUMAN_REQUIRED`; unbounded silent retry 금지 |
| `ACCEPTED` | TaskContract의 semantic outcome이 authoritative `ACCEPTED` Judgment로 입장되고 모든 target guards를 별도 TransitionDecision이 입장함 | Yes | Agent/Human/System may request; System alone admits | `ADMISSION_PENDING`, `HUMAN_REQUIRED` | applicable `ACCEPTED` Judgment; all required admitted evidence; no forbidden/authority conflict; HumanResult admitted when required; current version | none | When contract requires | same `WorkRun` 재개 금지; 후속 work는 새 Task/Run. Project/phase `CLOSED`를 자동 의미하지 않음 |
| `REJECTED` | authoritative `REJECTED` Judgment와 target guards가 입장되어 같은 `WorkRun` rework를 허용하지 않음 | Yes | Human/System; Agent may recommend only | `ADMISSION_PENDING`, `HUMAN_REQUIRED`, `REWORK_REQUIRED` | applicable rejection Judgment/ref; owner and reason valid; HumanResult when required; current version | none | Judgment policy-dependent | correction은 새 TaskContract/WorkRun lineage로 시작; 기존 run 불변 |
| `FAILED` | execution 또는 governance attempt가 retry/recovery 한도를 소진했거나 irrecoverable하게 종료됨 | Yes | execution adapter/System; Human may direct abandonment | `RUNNING`, `BLOCKED` | failure class/reason; retry exhaustion or irrecoverability; current version | none | Not inherently | retry는 새 `WorkRun` 또는 explicit rework Task로 시작; 기존 failed run을 되돌리지 않음 |

모든 terminal state는 해당 `WorkRun`에만 terminal이다. `ACCEPTED`, `REJECTED`, `FAILED` 어느 것도 project-level `CLOSED`를 자동 생성하지 않는다.

## 4. separate status dimensions

### 4.1 execution status

`ExecutionStatus`는 `NOT_STARTED`, `RUNNING`, `EXECUTOR_COMPLETED`, `EXECUTION_FAILED` 중 하나다. 이는 execution adapter의 admitted event를 나타내며 workflow acceptance가 아니다.

- `EXECUTOR_COMPLETED`: Task 범위의 산출과 executor-required 검사가 제출되었다는 뜻이다.
- `EXECUTION_FAILED`: 실행 attempt가 실패했다는 뜻이다. retry 가능성/terminal 여부는 transition evaluation이 결정한다.
- Agent의 자연어 self-report만으로 status를 바꾸지 않는다.

### 4.2 Human gate status

`HumanGateStatus`의 exact outcome-neutral lifecycle set은 `NOT_REQUIRED`, `PENDING`, `RESOLVED`, `CANCELLED`다. 결과 의미는 gate status가 아니라 exact `HumanResult`에만 보존한다. `WorkflowState=HUMAN_REQUIRED`는 workflow가 designated `HumanResult`를 기다리는 durable wait condition이고, `HumanGate` record는 requirement, owner, request/result/admission provenance를 보유한다.

`HumanGateSuspensionStatus`의 exact set은 `NOT_APPLICABLE`, `ACTIVE`, `SUSPENDED`다. `ACTIVE`와 `SUSPENDED`는 `HumanGateStatus=PENDING`에서만 유효하다.

| `HumanGateStatus` | exact meaning | admitted result | allowed suspension |
|---|---|---|---|
| `NOT_REQUIRED` | applicable contract/policy가 Human result를 요구하지 않음 | none | `NOT_APPLICABLE` |
| `PENDING` | gate가 열렸고 admitted result가 아직 없음 | none | `ACTIVE` 또는 `SUSPENDED` |
| `RESOLVED` | exact gate/version에 HumanResult 하나가 admitted됨 | exactly one | `NOT_APPLICABLE` |
| `CANCELLED` | result admission 전에 gate가 명시적으로 폐기됨 | none | `NOT_APPLICABLE` |

허용 lifecycle은 `NOT_REQUIRED → PENDING`, `PENDING/ACTIVE → RESOLVED`, `PENDING/ACTIVE ↔ PENDING/SUSPENDED`, `PENDING → CANCELLED`다. `RESOLVED`와 `CANCELLED`는 해당 gate record에서 terminal이며 correction/reconsideration은 새 gate 또는 explicit superseding record를 사용한다.

`HumanResult`의 exact semantic outcome set은 `APPROVE`, `REWORK`, `REJECT`다. designated Human이 제출하고 System이 owner, requirement applicability, task/run identity, gate version, current state/version을 검사해 admission한다. result admission event와 `PENDING/ACTIVE → RESOLVED/NOT_APPLICABLE` projection은 atomic하게 기록되거나 둘 다 적용되지 않는다. gate 하나에는 admitted result가 정확히 하나만 허용된다.

| HumanResult | admitted gate projection | semantic effect | does NOT imply |
|---|---|---|---|
| `APPROVE` | `HumanGateStatus=RESOLVED`; `result_ref.outcome=APPROVE` | policy-selected `ACCEPTED` Judgment를 만들 수 있는 Human input | `JudgmentStatus=ACCEPTED` 또는 `WorkflowState=ACCEPTED` |
| `REWORK` | `HumanGateStatus=RESOLVED`; `result_ref.outcome=REWORK` | policy-selected `HOLD_REWORK_REQUIRED` Judgment를 만들 수 있는 Human input | automatic `JudgmentStatus=HOLD_REWORK_REQUIRED` 또는 `WorkflowState=REWORK_REQUIRED` |
| `REJECT` | `HumanGateStatus=RESOLVED`; `result_ref.outcome=REJECT` | policy-selected `REJECTED` Judgment를 만들 수 있는 Human input | `JudgmentStatus=REJECTED` 또는 `WorkflowState=REJECTED` |

```text
HumanGate lifecycle
!= HumanResult semantic outcome
!= Judgment
!= TransitionDecision
!= WorkflowState
```

wrong owner, wrong proof type, stale/current-version mismatch, non-applicable, duplicate 또는 `PENDING/SUSPENDED` 동안 제출된 result는 즉시 admitted되지 않는다. suspended 동안 제출된 valid candidate는 보존할 수 있지만 blocker resolution과 `HUMAN_REQUIRED` 복귀 뒤 fresh current state/version에서 재검증하기 전까지 gate는 `PENDING`이고 result admission은 deferred다. Human이 semantic owner여도 System은 admitted `HumanResult`를 별도 immutable authoritative `Judgment`의 input으로 입장한다. Human silence/absence는 `PENDING`을 유지한다.

### 4.3 judgment status

`JudgmentStatus`는 `PENDING`, `ACCEPTED`, `REJECTED`, `HOLD_REWORK_REQUIRED`다. `PENDING`은 아직 applicable authoritative outcome Judgment가 없다는 pipeline projection이며 terminal/rework guard로 사용할 수 없다. `Judgment`는 Task/evidence/Human policy 아래 current work outcome이 무엇을 의미하는지 답하는 semantic record다.

`TaskContract.judgment_owner_policy`는 다음 중 정확히 하나를 선택한다.

- `SYSTEM_DETERMINISTIC`: versioned deterministic rule이 admitted evidence와 execution facts로 Judgment를 생성한다.
- `HUMAN`: designated Human이 semantic outcome을 소유한다. admitted `HumanResult`가 필수 input이고 System이 별도 Judgment record로 입장한다.
- `COMMAND_CENTER`: Command Center rubric/owner가 semantic outcome을 소유하고 System이 별도 Judgment record로 입장한다. 별도 Human gate가 요구되면 admitted `HumanResult`도 선행 input이다.

Agent reviewer output은 `JudgmentCandidate`일 뿐이다. System deterministic Judgment는 Agent prose나 self-assessment를 truth로 사용하지 않고 versioned policy와 admitted refs만 사용한다. Judgment는 immutable이며 correction은 `supersedes_judgment_id`를 가진 additive successor로 기록한다. current Task/run/version에 applicable한 unsuperseded Judgment만 guard가 될 수 있다.

```text
JUDGMENT
!= TRANSITION_DECISION

Judgment exists
!= state automatically mutated
```

`TransitionDecision`은 authoritative current state/version, requested target, applicable Judgment ref와 나머지 target guards를 기계적으로 검사해 `ADMITTED` 또는 `DENIED`를 내리는 System decision이다. semantic Judgment를 만들거나 대신하지 않는다.

System은 다음 exact mapping을 만족하는 authoritative Judgment ref를 검증한 뒤에만 outcome state를 입장한다.

| requested target | required `JudgmentStatus` |
|---|---|
| `ACCEPTED` | `ACCEPTED` |
| `REJECTED` | `REJECTED` |
| `REWORK_REQUIRED` | `HOLD_REWORK_REQUIRED` |

`FAILED`는 semantic accept/reject/rework Judgment가 아니라 irrecoverable/retry-exhausted execution/governance attempt의 technical terminal state다. `G_FAILURE_TERMINAL`과 failure provenance로 admission하며 project disposition/closure는 이후 Judgment/Cycle owner가 별도로 결정한다.

## 5. authoritative ordering and transition protocol

terminal/rework outcome의 canonical ordering은 아래 하나뿐이다.

```text
Agent / Executor output
→ EvidenceCandidateRef
→ evidence admission
→ review / JudgmentCandidate
→ HumanGate `PENDING / ACTIVE` when required
→ HumanResult admission + HumanGate `RESOLVED` when required
→ authoritative Judgment admitted
→ TransitionRequest
→ TransitionEvaluation
→ TransitionDecision
→ atomic AuthoritativeStateMutation
→ CycleRecord admission
→ NextAction projection
```

`Judgment`를 terminal state mutation 뒤에 다시 생성하지 않는다. Cycle은 admitted Judgment와 resulting transition을 함께 참조하지만 새 semantic Judgment를 소급 생성하지 않는다.

이 ordering은 `ACCEPTED`, `REJECTED`, `REWORK_REQUIRED` outcome routing에 적용한다. `READY`, `RUNNING`, `ADMISSION_PENDING`, `HUMAN_REQUIRED`, `BLOCKED`, `FAILED` control/execution transition은 target-specific non-Judgment guard로 입장할 수 있다. `HUMAN_REQUIRED`는 authoritative Judgment 전에 Human input을 기다리는 pre-Judgment control transition이다.

transition 단계는 결합하거나 생략하지 않는다.

1. `TransitionRequest`: requester가 `observed_state`, `observed_version`, target과 applicable Judgment/evidence/Human refs를 제출한다.
2. `TransitionEvaluation`: System이 authoritative current state/version, contract/policy, target-specific Judgment와 abstract evidence/Human predicates를 평가한다.
3. `TransitionDecision`: System transition authority가 `ADMITTED` 또는 `DENIED`와 exact reason을 기록한다. 이는 semantic Judgment가 아니다.
4. `AuthoritativeStateMutation`: `ADMITTED`일 때만 decision event와 atomic하게 target state 및 `state_version + 1`을 기록한다.

denied request는 state를 바꾸지 않는다. Human input 부재가 확인되면 원 target request를 deny한 뒤 System이 별도의 fresh `TransitionRequest`로 `HUMAN_REQUIRED`를 요청한다. correctable outcome이면 policy-selected owner가 authoritative `HOLD_REWORK_REQUIRED` Judgment를 먼저 입장한 뒤에만 별도의 fresh request로 `REWORK_REQUIRED`를 요청한다. denial이 다른 state로 몰래 변환되어서는 안 된다.

## 6. abstract guard vocabulary

transition matrix의 guard identifier는 다음 exact 의미를 가진다.

| guard | meaning |
|---|---|
| `G_CURRENT` | request의 observed state/version이 authoritative current state/version과 exact match |
| `G_CONTRACT` | exact `TaskContract` version이 valid하고 run에 binding됨 |
| `G_SCOPE` | requested action/target이 allowed scope이며 forbidden action이 없음 |
| `G_RUNTIME_CONTEXT` | required runtime mode/policy refs가 존재; detailed permission result는 P1-2/P1-3 owner |
| `G_EXECUTION_STARTED` | authorized execution-start event 존재 |
| `G_EXECUTOR_SUBMISSION` | executor completion event와 candidate provenance가 존재 |
| `G_EVIDENCE` | P1-6 interface가 모든 applicable evidence requirement를 `SATISFIED`로 반환 |
| `G_HUMAN_REQUIRED` | applicable requirement의 owner가 Human이고 admitted result가 없으며 exact gate가 `PENDING/ACTIVE`이거나 이 transition에서 그렇게 생성될 수 있음 |
| `G_HUMAN_NOT_REQUIRED` | applicable `TaskContract`/judgment policy가 HumanResult를 요구하지 않음 |
| `G_NO_PENDING_HUMAN_GATE` | unresolved `HumanGateStatus=PENDING` gate가 없음 |
| `G_SUSPENDED_HUMAN_GATE` | exact gate가 `HumanGateStatus=PENDING`, `HumanGateSuspensionStatus=SUSPENDED`이며 blocker와 provenance-linked됨 |
| `G_RESUMABLE_HUMAN_GATE` | blocker가 resolved되고 suspended pending gate의 owner/applicability/task/run/gate-version이 여전히 valid함 |
| `G_HUMAN_APPROVED` | gate가 `RESOLVED`이고 exact admitted `result_ref.outcome=APPROVE`가 current requirement/version에 valid함 |
| `G_HUMAN_REWORK` | gate가 `RESOLVED`이고 exact admitted `result_ref.outcome=REWORK`가 current requirement/version에 valid함 |
| `G_HUMAN_REJECTED` | gate가 `RESOLVED`이고 exact admitted `result_ref.outcome=REJECT`가 current requirement/version에 valid함 |
| `G_JUDGMENT_ACCEPTED` | current Task/run/version에 applicable한 unsuperseded authoritative Judgment의 status가 `ACCEPTED` |
| `G_JUDGMENT_REJECTED` | current Task/run/version에 applicable한 unsuperseded authoritative Judgment의 status가 `REJECTED` |
| `G_JUDGMENT_REWORK` | current Task/run/version에 applicable한 unsuperseded authoritative Judgment의 status가 `HOLD_REWORK_REQUIRED` |
| `G_BLOCKER` | blocker identity, owner, reason, resumability가 기록됨 |
| `G_BLOCKER_RESOLVED` | blocker owner의 applicable resolution evidence가 admitted됨 |
| `G_REWORK_SPEC` | failed guard와 bounded correction/revision lineage가 명시됨 |
| `G_FAILURE_TERMINAL` | retry exhausted, abandoned 또는 irrecoverable failure가 system policy로 판정됨 |

모든 transition은 암묵적으로 `G_CURRENT`를 요구한다.

## 7. exact transition matrix

아래 row만 admissible transition이다. 표에 없는 source/target pair와 terminal state의 outgoing request는 `INVALID_TRANSITION`으로 deny한다. `v+1`은 admitted mutation 뒤의 monotonic state version이다.

공통 provenance `P0`:

```text
project/task/run IDs; contract version; request/evaluation/decision IDs;
source state/version; target; requester identity/type; runtime mode;
guard IDs/results; evidence/HumanResult/authoritative Judgment refs; owner-policy refs;
decision and reason; admitting owner; timestamp; resulting state/version
```

| source | requested target | requester | admission owner | abstract guard | admitted result | denied result | Human gate behavior | provenance emitted |
|---|---|---|---|---|---|---|---|---|
| `NONE` | `READY` | System / authorized operator | System | `G_CONTRACT`, `G_SCOPE`, `G_RUNTIME_CONTEXT` | new run `READY/v1` | no run; denial reason | not opened | `P0` + creation refs |
| `READY` | `RUNNING` | Agent/System/operator request | System | `G_CONTRACT`, `G_SCOPE`, `G_RUNTIME_CONTEXT`, `G_EXECUTION_STARTED` | `RUNNING/v+1` | remain `READY`; retry after exact correction | unchanged | `P0` + execution-attempt ref |
| `RUNNING` | `ADMISSION_PENDING` | Agent/Executor/System | System | `G_EXECUTOR_SUBMISSION`, `G_SCOPE` | `ADMISSION_PENDING/v+1`; execution=`EXECUTOR_COMPLETED` | remain `RUNNING`; incomplete/invalid submission reason | unchanged | `P0` + candidate refs |
| `RUNNING` | `BLOCKED` | Agent/System/Human | System | `G_BLOCKER` | `BLOCKED/v+1` | remain `RUNNING` | open only if blocker owner is Human requirement rather than ordinary blocker | `P0` + blocker ref |
| `RUNNING` | `REWORK_REQUIRED` | System/Command Center; Agent recommendation | System | `G_HUMAN_NOT_REQUIRED`, `G_JUDGMENT_REWORK`, `G_REWORK_SPEC`; correctable current-attempt condition | `REWORK_REQUIRED/v+1` | remain `RUNNING`; missing/stale/wrong-status Judgment or invalid rework spec reason | Human-owned correction cannot use this row; submit/evaluate through Human gate path | `P0` + Judgment ref + failed guard/rework reason |
| `RUNNING` | `FAILED` | adapter/System/Human abandonment | System | `G_FAILURE_TERMINAL` | `FAILED/v+1` | remain `RUNNING`; retry remains possible | unchanged | `P0` + failure/retry record |
| `ADMISSION_PENDING` | `HUMAN_REQUIRED` | System | System | `G_HUMAN_REQUIRED`; all non-Human prerequisites ready or exact pending reason recorded | `HUMAN_REQUIRED/v+1`; gate=`PENDING/ACTIVE` | remain `ADMISSION_PENDING` | create/open exact gate; no auto-pass | `P0` + gate/request refs |
| `ADMISSION_PENDING` | `BLOCKED` | Agent/System/Human | System | `G_BLOCKER` | `BLOCKED/v+1` | remain `ADMISSION_PENDING` | no Human gate unless blocker is reclassified by fresh evaluation | `P0` + blocker ref |
| `ADMISSION_PENDING` | `REWORK_REQUIRED` | System/Command Center; Agent recommendation | System | `G_HUMAN_NOT_REQUIRED`, `G_JUDGMENT_REWORK`, `G_REWORK_SPEC`; evidence missing/wrong/stale but correctable | `REWORK_REQUIRED/v+1` | remain `ADMISSION_PENDING`; missing/stale/wrong-status Judgment, Human-required, or invalid rework spec reason | if HumanResult required, deny this row and separately admit `HUMAN_REQUIRED` | `P0` + Judgment ref + failed guard/evidence/rework refs |
| `ADMISSION_PENDING` | `ACCEPTED` | Agent/System/Command Center request | System | `G_EVIDENCE`, `G_HUMAN_NOT_REQUIRED`, `G_JUDGMENT_ACCEPTED`; no authority/forbidden conflict | `ACCEPTED/v+1` | remain `ADMISSION_PENDING`; exact unmet evidence/Human/Judgment/current guard reason | Human gate must be `NOT_REQUIRED`; if required, deny and separately admit `HUMAN_REQUIRED` | `P0` + admitted evidence + authoritative Judgment refs |
| `ADMISSION_PENDING` | `REJECTED` | System/Command Center | System | `G_HUMAN_NOT_REQUIRED`, `G_JUDGMENT_REJECTED`; no same-run rework | `REJECTED/v+1` | remain `ADMISSION_PENDING`; missing/stale/wrong-status Judgment or Human-required reason | if HumanResult required, deny this row and separately admit `HUMAN_REQUIRED` | `P0` + authoritative Judgment ref |
| `HUMAN_REQUIRED` | `ACCEPTED` | Human/System; Agent recommendation | System | `G_EVIDENCE`, `G_HUMAN_APPROVED`, `G_JUDGMENT_ACCEPTED` | gate remains `RESOLVED` with outcome=`APPROVE`; `ACCEPTED/v+1` | remain `HUMAN_REQUIRED`; invalid/wrong/stale HumanResult, missing/stale/wrong-status Judgment, or unmet evidence reason | HumanResult is Judgment input only; silence leaves gate `PENDING/ACTIVE` | `P0` + gate/result admission + authoritative Judgment refs |
| `HUMAN_REQUIRED` | `REWORK_REQUIRED` | Human/System | System | `G_HUMAN_REWORK`, `G_JUDGMENT_REWORK`, `G_REWORK_SPEC` | gate remains `RESOLVED` with outcome=`REWORK`; `REWORK_REQUIRED/v+1` | remain `HUMAN_REQUIRED`; invalid/wrong/stale HumanResult, missing/stale/wrong-status Judgment, or invalid rework spec reason | exact result is input to a separate Judgment; neither result nor resolved gate mutates workflow | `P0` + gate/result admission + Judgment + failed guard/rework refs |
| `HUMAN_REQUIRED` | `REJECTED` | Human/System | System | `G_HUMAN_REJECTED`, `G_JUDGMENT_REJECTED` | gate remains `RESOLVED` with outcome=`REJECT`; `REJECTED/v+1` | remain `HUMAN_REQUIRED`; invalid/wrong/stale HumanResult or missing/stale/wrong-status Judgment reason | wrong owner/proof or silence leaves gate `PENDING/ACTIVE` | `P0` + gate/result admission + authoritative Judgment refs |
| `HUMAN_REQUIRED` | `BLOCKED` | System/Human | System | `G_BLOCKER`; gate=`PENDING/ACTIVE`; gate cannot currently accept a result because of authority/policy dependency | `BLOCKED/v+1`; gate=`PENDING/SUSPENDED` | remain `HUMAN_REQUIRED` | Human absence alone is not blocker; submitted result admission is deferred while suspended | `P0` + blocker + gate status/suspension refs |
| `BLOCKED` | `READY` | blocker owner/System/operator | System | `G_BLOCKER_RESOLVED`, `G_NO_PENDING_HUMAN_GATE`, `G_CONTRACT`, `G_SCOPE` | `READY/v+1` | remain `BLOCKED`; suspended pending gate must use `BLOCKED → HUMAN_REQUIRED` | no unresolved gate exists | `P0` + resolution ref |
| `BLOCKED` | `HUMAN_REQUIRED` | blocker owner/System | System | `G_BLOCKER_RESOLVED`, `G_SUSPENDED_HUMAN_GATE`, `G_RESUMABLE_HUMAN_GATE` | `HUMAN_REQUIRED/v+1`; gate=`PENDING/ACTIVE` | remain `BLOCKED`; invalid/stale gate or unresolved blocker reason | reactivate exact gate; any deferred result candidate is revalidated, never auto-admitted | `P0` + resolution + gate status/suspension refs |
| `BLOCKED` | `REWORK_REQUIRED` | System/Command Center | System | `G_BLOCKER_RESOLVED`, `G_HUMAN_NOT_REQUIRED`, `G_JUDGMENT_REWORK`, `G_REWORK_SPEC` | `REWORK_REQUIRED/v+1` | remain `BLOCKED`; unresolved blocker, Human-required, missing/stale/wrong-status Judgment, or invalid rework spec reason | Human-owned path must first restore/open `HUMAN_REQUIRED`; no hidden gate outcome | `P0` + resolution + Judgment/rework refs |
| `BLOCKED` | `FAILED` | System/Human abandonment | System | `G_FAILURE_TERMINAL` | `FAILED/v+1`; any pending gate=`CANCELLED` | remain `BLOCKED` | late result denied after gate cancellation; Human silence alone cannot satisfy failure guard | `P0` + failure decision + gate cancellation ref when applicable |
| `REWORK_REQUIRED` | `READY` | Agent/System/operator | System | `G_REWORK_SPEC`; new attempt/revision ref; `G_NO_PENDING_HUMAN_GATE`, `G_CONTRACT`, `G_SCOPE` | `READY/v+1` | remain `REWORK_REQUIRED` | prior resolved gate/result remains immutable; no free-text Human correction substitutes for a new gate | `P0` + prior/new attempt lineage |
| `REWORK_REQUIRED` | `HUMAN_REQUIRED` | System | System | `G_HUMAN_REQUIRED`; new applicable Human requirement for correction/final disposition | `HUMAN_REQUIRED/v+1`; new gate=`PENDING/ACTIVE` | remain `REWORK_REQUIRED` | opens a new exact gate; prior resolved/cancelled gate is not reopened | `P0` + new gate/request + prior rework lineage refs |
| `REWORK_REQUIRED` | `REJECTED` | System/Command Center | System | `G_HUMAN_NOT_REQUIRED`, `G_JUDGMENT_REJECTED`; no same-run correction remains | `REJECTED/v+1` | remain `REWORK_REQUIRED`; Human-required, missing/stale/wrong-status Judgment, or remaining correction reason | Human-owned disposition must use `REWORK_REQUIRED → HUMAN_REQUIRED`; silence does not reject | `P0` + authoritative Judgment ref |

## 8. evidence interface boundary

P1-1 transition engine은 P1-6이 제공할 abstract result만 소비한다.

```text
EvidencePredicateResult
= SATISFIED
| MISSING
| WRONG_OWNER
| WRONG_PROOF_TYPE
| STALE
| NOT_APPLICABLE
```

각 result는 `EvidenceRequirementRef`, candidate/admitted ref, evaluated TaskContract/state version과 provenance-linked돼야 한다.

- `SATISFIED`: 해당 requirement만 충족한다. authoritative Judgment, 다른 requirement 또는 Human gate를 만들거나 대체하지 않는다.
- `MISSING`: target transition deny. executor가 보완 가능하면 `HOLD_REWORK_REQUIRED` Judgment와 별도 transition을 거치는 `REWORK_REQUIRED` 후보, 외부 dependency면 `BLOCKED`, Human-owned이면 `HUMAN_REQUIRED` 후보.
- `WRONG_OWNER`: deny. Agent가 Human proof를 제출해도 Human result가 되지 않는다.
- `WRONG_PROOF_TYPE`: deny. static/unit/browser/checklist 등 channel non-substitution을 유지한다.
- `STALE`: deny. fresh evidence와 new request가 필요하며 이전 evidence를 current version에 재사용하지 않는다.
- `NOT_APPLICABLE`: contract가 명시한 비적용 requirement에만 사용하며 missing과 혼동하지 않는다.
- `HUMAN_PENDING`: evidence result나 Judgment의 success가 아니라 `HumanGateStatus=PENDING`; terminal/rework transition을 deny하고 applicable한 경우 `HUMAN_REQUIRED`를 별도 입장한다.

evidence schema, verifier, owner registry, freshness 계산과 admission 구현은 P1-6에 deferred한다.

## 9. Human gate boundary

evidence/Judgment evaluation이 applicable `EvidenceRequirementRef` 또는 `judgment_owner_policy`에서 designated Human owner를 발견하고 valid `HumanResult`가 없을 때 System은 terminal/rework target을 deny한다. 그 뒤 fresh request로 `HUMAN_REQUIRED`를 입장하고 durable `HumanGate`를 연다.

Human gate 최소 semantics:

- gate는 requirement, designated owner, requested decision, applicable task/run/state/version, gate version, lifecycle/suspension, submitted/result/admission refs를 가진다.
- wait 중 workflow는 `HUMAN_REQUIRED`, gate는 `PENDING/ACTIVE`다. timeout이나 silence는 `RESOLVED`가 아니며 어떤 outcome도 만들지 않는다.
- `APPROVE`, `REWORK`, `REJECT` 모두 designated Human이 제출하고 System이 owner/applicability/task/run/gate-version/current-version을 확인한 뒤에만 admitted된다.
- admitted outcome은 모두 gate를 exact `RESOLVED`로 투영하며 result ref가 semantic difference를 보존한다. `RESOLVED` 자체는 approve/rework/reject를 뜻하지 않는다.
- admitted HumanResult는 policy-selected semantic owner가 별도 authoritative `Judgment`를 만들기 위한 input이며 Judgment 자체가 아니다.
- HumanResult와 일치하는 authoritative Judgment가 먼저 입장된 뒤, 별도 TransitionRequest/Evaluation/Decision이 모든 target guard를 만족해야 outcome state로 이동한다.
- wrong owner, wrong proof type, stale, non-applicable 또는 duplicate HumanResult는 gate projection을 바꾸거나 Judgment를 authorize하지 않는다.
- `HUMAN_REQUIRED → BLOCKED`는 gate를 `PENDING/SUSPENDED`로 투영한다. suspended 동안 result admission은 deferred되고 candidate만 보존할 수 있다.
- blocker resolution 뒤 exact gate가 still-applicable이면 `BLOCKED → HUMAN_REQUIRED`로 `PENDING/ACTIVE`를 복원하고 deferred candidate를 fresh current version에서 재검증한다. pending gate가 없을 때만 `BLOCKED → READY`가 가능하다.
- irrecoverable `BLOCKED → FAILED`는 pending gate를 `CANCELLED`로 투영하며 이후 result를 deny한다.

identity, authentication, UI, notification, timeout policy와 exception workflow는 P1-7 owner다.

## 10. failure, blocked, rework, and rejection semantics

| condition | observable semantic result |
|---|---|
| execution error, retry still possible | `ExecutionStatus=EXECUTION_FAILED`; workflow는 current state에 남거나 policy에 따라 `REWORK_REQUIRED` request |
| execution irrecoverable/retry exhausted | terminal `FAILED` |
| executor-producible evidence missing/wrong/stale | requested terminal transition denied; `REWORK_REQUIRED` candidate |
| external prerequisite unavailable | non-terminal `BLOCKED` |
| policy/authority conflict | non-terminal `BLOCKED`; Human/Command Center resolution 없이는 진행 금지 |
| Human-owned result absent | non-terminal `HUMAN_REQUIRED`; silence는 success 아님 |
| policy-selected owner admits exact correction Judgment | non-terminal `REWORK_REQUIRED`; separate transition admission required |
| authoritative `REJECTED` Judgment with no same-run correction | terminal `REJECTED`; separate transition admission required |
| authoritative `ACCEPTED` Judgment + all target predicates admitted | terminal `ACCEPTED` |

`FAILED`는 execution/governance attempt가 성공적으로 끝나지 못한 기술적/operational terminal outcome이다. `REJECTED`는 authoritative judgment가 결과를 받아들이지 않은 policy/business/verification outcome이다. `REWORK_REQUIRED`는 correction이 허용된 non-terminal routing이다.

## 11. concurrency and stale-request contract

모든 request는 evaluation 시작과 admission 직전에 authoritative current state/version에 대해 검증한다.

```text
request.observed_version != current.state_version
OR request.observed_state != current.state
→ DENIED(STALE_REQUEST)
→ no mutation
→ requester must reload and issue a new request
```

동시에 같은 version에서 요청 두 개가 평가되더라도 하나가 입장하여 version을 증가시키면 나머지는 stale로 deny된다. last-write-wins, silent overwrite, stale evidence 또는 stale Judgment rebinding은 금지한다. 정확한 lock/transaction/compare-and-swap 기술은 P1-4에 deferred한다.

retry는 같은 request를 새 version에 자동 재적용하는 것이 아니다. fresh state를 읽고 새 request ID로 재평가한다. 같은 idempotency identity의 transport retry는 기존 decision을 반환해야 하며 duplicate mutation을 만들지 않는다.

## 12. deterministic and replayable transition trace

admitted/denied 모든 evaluation은 최소 다음 필드를 durable event로 남긴다.

- `project_id`, `task_contract_id`, `task_contract_version`, `work_run_id`
- `transition_request_id`, optional parent/retry/rework request ID
- source state와 requester가 observed한 version
- evaluation 시 authoritative state/version
- requested target state
- requester identity/type와 admitting System owner/version
- `RuntimeMode`와 applicable policy/contract refs
- guard identifiers, 각 result와 reason code
- evidence requirement/candidate/admitted refs
- Human gate/submitted/admitted `HumanResult` refs
- Human gate status before/after, suspension before/after, gate version과 admitted result outcome
- Judgment candidate, authoritative Judgment, semantic owner-policy와 supersession refs
- `ADMITTED` 또는 `DENIED`와 exact reason code
- request/evaluation/decision timestamps
- resulting state/version; denial이면 unchanged state/version
- orchestrator version/commit when runtime exists

Recorded Replay는 이 event order와 immutable refs를 사용해 당시의 판단을 재구성한다. current policy로 과거 결정을 다시 꾸미거나 Agent prose로 누락 필드를 채우지 않는다.

## 13. restart and recovery

- restart 후 authoritative current state/version과 append-only events를 읽어 projection을 검증한다.
- `RUNNING`에서 execution lease/heartbeat가 불명확하다는 사실만으로 success나 terminal failure를 만들지 않는다. P1-4/P1-5 recovery policy가 fresh observation으로 request해야 한다.
- `ADMISSION_PENDING`은 durable submission/evidence/Judgment candidate refs로 evaluation을 재개한다.
- `HUMAN_REQUIRED`는 exact `PENDING/ACTIVE` gate를 복원하고 admitted HumanResult와 authoritative Judgment 없이는 그대로 유지한다.
- `BLOCKED`는 blocker/resolution refs와 gate lifecycle/suspension을 함께 복원한다. `PENDING/SUSPENDED` gate가 있으면 blocker resolution 뒤 `HUMAN_REQUIRED`로만 재개하고, gate가 없을 때만 `READY`로 재개한다.
- terminal state는 correction event 없이 mutate하지 않으며 후속 작업은 새 lineage다.
- event/projection 불일치는 fail-closed하고 authority conflict로 처리한다.

## 14. terminal semantics

`ACCEPTED`, `REJECTED`, `FAILED`만 terminal이다.

- `ACCEPTED`: current-version authoritative `ACCEPTED` Judgment와 모든 target guard가 별도 TransitionDecision으로 입장됨.
- `REJECTED`: current-version authoritative `REJECTED` Judgment와 모든 target guard가 별도 TransitionDecision으로 입장됨.
- `FAILED`: 현재 `WorkRun`이 irrecoverable/retry-exhausted failure로 종료됨.

다음은 terminal이 아니다.

- `ExecutionStatus=EXECUTOR_COMPLETED`
- `ADMISSION_PENDING`
- `HUMAN_REQUIRED`
- evidence candidate가 모두 존재한다는 Agent claim
- admitted `HumanResult`
- authoritative `Judgment` without admitted TransitionDecision
- `JudgmentStatus=HOLD_REWORK_REQUIRED`

Project/phase `CLOSED`, Cycle admission, stable `NextAction`은 P1-8 project projection이며 terminal `WorkRun` state와 별도다.

## 15. mode-invariant orchestration

`OWNER_SELF_DOGFOOD`, `PUBLIC_RECORDED_REPLAY`, `PUBLIC_BOUNDED_LIVE`는 workflow state가 아니다.

- Self-Dogfooding은 동일 transition authority와 evidence/Human semantics를 사용하고 orchestrator version/commit을 trace에 남긴다.
- Recorded Replay는 보존된 trace를 read-only로 재생하며 transition request를 생성하지 않는다.
- Bounded Live는 P1-2/P1-3 permission policy로 실행 범위를 제한하지만 evidence 또는 terminal guard를 완화하지 않는다.
- Live/provider/budget failure는 Replay의 prior truth를 바꾸지 않으며 Live run을 success로 표시하지 않는다.

## 16. deferred design ownership

- P1-2: runtime mode별 security/sandbox/tool/network/secret boundary와 timeout/cancel policy design
- P1-3: safeguard implementation과 applicable verification
- P1-4: state kernel, durability, atomic admission, idempotency/concurrency implementation
- P1-5: provider/tool execution adapter와 execution events
- P1-6: evidence predicates, owner/type/freshness/provenance admission implementation
- P1-7: Human identity/gate/judgment implementation
- P1-8: Cycle admission, project closure와 `NextAction` projection

이 문서는 위 구현을 수행하거나 특정 DB/API/provider를 선택하지 않는다.

## 17. design question decisions

1. 가장 작은 state set은 section 3의 9개다. execution/Human/judgment를 별도 dimension으로 분리하여 state explosion 없이 authority 의미를 보존한다.
2. `HUMAN_REQUIRED`는 durable workflow wait state다. 별도 `HumanGate`는 outcome-neutral lifecycle/suspension을, `HumanResult`는 exact semantic outcome을 보유하며 서로 대체하지 않는다.
3. `BLOCKED`는 non-terminal이다. suspended pending gate가 있으면 applicable resolution 뒤 `HUMAN_REQUIRED`로 복귀하고, gate가 없으면 `READY`, non-Human rework Judgment가 있으면 `REWORK_REQUIRED`로 재개한다.
4. `FAILED`는 irrecoverable/retry-exhausted attempt, `REJECTED`는 final negative judgment, `REWORK_REQUIRED`는 correction 가능한 non-terminal routing이다.
5. Executor 완료는 `ExecutionStatus=EXECUTOR_COMPLETED`와 submission provenance다. System terminal result는 evidence/Human input과 별도로 admitted된 authoritative Judgment를 current version의 target guard로 검증한 TransitionDecision이 `ACCEPTED` mutation을 입장한 결과다.
6. concurrency boundary는 `WorkRun.state_version`과 request의 observed state/version 사이이며 admission 직전에도 재검증한다.
7. P1-4 전에는 Task/Run identity, contract/judgment-owner-policy version, current state/version, complete transition/evidence/HumanResult/Judgment refs와 atomic append/projection semantics가 durable requirement로 고정돼야 한다.
8. P1-2 security detail, P1-6 evidence admission detail, P1-7 Human implementation, P1-8 Cycle/NextAction admission은 의도적으로 deferred한다.
9. Self-Dogfooding은 동일 state set/authority, orchestrator version, denied/admitted trace, manual intervention과 fresh evidence semantics를 요구한다.
10. Recorded Replay는 immutable ordered transition events, evaluated policy/guard/evidence/Human refs, timestamps와 resulting version으로 과거 run을 그대로 재구성해야 한다.
