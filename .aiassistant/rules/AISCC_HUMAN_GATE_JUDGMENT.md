# AISCC Human Gate and Judgment

## 1. 목적과 문서 상태

| field | value |
|---|---|
| document_id | `AISCC-P1-7-HUMAN-GATE-JUDGMENT-V1-CANDIDATE` |
| task_id | `20260829_2204_aiscc-p1-7-pre-human-evidence-gate-binding-design-rework-1` |
| work_type | `REWORK / DOC_BASELINE_UPDATE` |
| result_status | `DESIGN_CANDIDATE / HUMAN_REVIEW_PENDING` |
| authority_status | repository design candidate; Human final review 전에는 accepted canonical authority가 아님 |
| design_base_commit | `fc30aa3151494e15b132f8c48be8ca2c1bf8855d` |
| predecessor_candidate_sha256 | `01cf086c5c996a674c696aaf76522f7e139684d1115356f22179b583a0b74d1c` |
| semantic owners | `P1_7_HUMAN`, `P1_7_JUDGMENT` |
| implementation_status | `NOT_STARTED` |
| runtime/database verification | `NOT_EXECUTED` |

이 문서는 P1-7의 `HumanGate`, authenticated Human principal, `HumanResult`,
`HUMAN_P1_7` evidence producer, `Judgment`, Human/Judgment guard authority를 설계한다. 이 문서는
P1-7 runtime, database migration, test, P1-8 memory/Cycle admission 또는 `WorkflowState` mutation을
구현하지 않는다.

```text
DESIGN_CANDIDATE / HUMAN_REVIEW_PENDING
!= ACCEPTED
!= IMPLEMENTED
!= VERIFIED_RUNTIME
```

## 2. predecessor authority와 exact source findings

### 2.1 frozen predecessors

이 설계는 다음 accepted predecessor를 변경하지 않는다.

- `.aiassistant/rules/AISCC_ORCHESTRATION.md`
- `.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md`
- P1-4 PostgreSQL workflow kernel at start HEAD
- P1-6 PostgreSQL evidence admission runtime at start HEAD

Exact `WorkflowState`는 다음 9개다.

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

P1-4 source의 `GuardSemanticOwner`와 `GUARD_OWNER_POLICY`는 P1-7에 충분한 exact owner slot을
이미 정의한다. 따라서 이 candidate는 새 guard ID를 만들지 않는다.

| exact guard ID | exact semantic owner |
|---|---|
| `G_HUMAN_REQUIRED` | `P1_7_HUMAN` |
| `G_HUMAN_NOT_REQUIRED` | `P1_7_HUMAN` |
| `G_NO_PENDING_HUMAN_GATE` | `P1_7_HUMAN` |
| `G_SUSPENDED_HUMAN_GATE` | `P1_7_HUMAN` |
| `G_RESUMABLE_HUMAN_GATE` | `P1_7_HUMAN` |
| `G_HUMAN_APPROVED` | `P1_7_HUMAN` |
| `G_HUMAN_REWORK` | `P1_7_HUMAN` |
| `G_HUMAN_REJECTED` | `P1_7_HUMAN` |
| `G_JUDGMENT_ACCEPTED` | `P1_7_JUDGMENT` |
| `G_JUDGMENT_REJECTED` | `P1_7_JUDGMENT` |
| `G_JUDGMENT_REWORK` | `P1_7_JUDGMENT` |

`G_EVIDENCE`의 owner는 계속 `P1_6_EVIDENCE`다. 나머지 P1-4 guard owner는 변경하지 않는다.

P1-4 source의 `FutureOwnerGuardVerifier.recognizes(fact, request)`는 request-aware다. P1-4의
generic verifier는 fact의 exact owner, `bound_refs`, TaskContract, WorkRun, `state_version`을
`TransitionRequest`와 비교한다. P1-7 owner verifier는 여기에 source state, target state,
gate/result/judgment authority revision과 target-use identity를 추가로 검증해야 한다.

### 2.2 exact P1-7-relevant transition guards

모든 row는 P1-4가 암묵적으로 평가하는 `G_CURRENT`를 추가로 요구한다.

| source -> target | exact non-current guard set |
|---|---|
| `RUNNING -> REWORK_REQUIRED` | `G_HUMAN_NOT_REQUIRED`, `G_JUDGMENT_REWORK`, `G_REWORK_SPEC` |
| `ADMISSION_PENDING -> HUMAN_REQUIRED` | `G_HUMAN_REQUIRED` |
| `ADMISSION_PENDING -> REWORK_REQUIRED` | `G_HUMAN_NOT_REQUIRED`, `G_JUDGMENT_REWORK`, `G_REWORK_SPEC` |
| `ADMISSION_PENDING -> ACCEPTED` | `G_EVIDENCE`, `G_HUMAN_NOT_REQUIRED`, `G_JUDGMENT_ACCEPTED` |
| `ADMISSION_PENDING -> REJECTED` | `G_HUMAN_NOT_REQUIRED`, `G_JUDGMENT_REJECTED` |
| `HUMAN_REQUIRED -> ACCEPTED` | `G_EVIDENCE`, `G_HUMAN_APPROVED`, `G_JUDGMENT_ACCEPTED` |
| `HUMAN_REQUIRED -> REWORK_REQUIRED` | `G_HUMAN_REWORK`, `G_JUDGMENT_REWORK`, `G_REWORK_SPEC` |
| `HUMAN_REQUIRED -> REJECTED` | `G_HUMAN_REJECTED`, `G_JUDGMENT_REJECTED` |
| `HUMAN_REQUIRED -> BLOCKED` | `G_BLOCKER` |
| `BLOCKED -> READY` | `G_BLOCKER_RESOLVED`, `G_NO_PENDING_HUMAN_GATE`, `G_CONTRACT`, `G_SCOPE` |
| `BLOCKED -> HUMAN_REQUIRED` | `G_BLOCKER_RESOLVED`, `G_SUSPENDED_HUMAN_GATE`, `G_RESUMABLE_HUMAN_GATE` |
| `BLOCKED -> REWORK_REQUIRED` | `G_BLOCKER_RESOLVED`, `G_HUMAN_NOT_REQUIRED`, `G_JUDGMENT_REWORK`, `G_REWORK_SPEC` |
| `REWORK_REQUIRED -> READY` | `G_REWORK_SPEC`, `G_NO_PENDING_HUMAN_GATE`, `G_CONTRACT`, `G_SCOPE` |
| `REWORK_REQUIRED -> HUMAN_REQUIRED` | `G_HUMAN_REQUIRED` |
| `REWORK_REQUIRED -> REJECTED` | `G_HUMAN_NOT_REQUIRED`, `G_JUDGMENT_REJECTED` |

P1-4 source의 `required_bound_refs`는 result guards에 `TransitionRequest.human_result_refs`,
Judgment guards에 `TransitionRequest.judgment_refs`, `G_EVIDENCE`에
`TransitionRequest.evidence_refs`를 사용한다. P1-7 구현은 result/Judgment guard마다 exact one ref를
요구한다. Gate-policy/lifecycle guards는 request tuple이 비어 있으므로 durable attestation을
`authority_ref`로 resolve하고 request-aware verifier가 exact gate/use를 검증한다.

### 2.3 P1-6 exact Human/checkpoint findings

P1-6의 exact producer categories는 다음 둘이며 상호 대체할 수 없다.

```text
HUMAN_DIRECT_EVIDENCE
HUMAN_P1_7
```

P1-6의 exact lifecycle checkpoint purposes는 다음 둘이다.

```text
PRE_HUMAN_EVIDENCE
POST_HUMAN_EVIDENCE
```

`EvidenceCheckpoint`는 System/TaskContract-owned이고 source state와 exact target transition 또는
exact transition-purpose identity를 가진다. `EvidenceSetSatisfactionAttestation`은 TaskContract,
WorkRun, source state/version, checkpoint, target/use, RequirementSet roots, admitted-evidence roots,
evidence authority revision을 bind한다.

Current P1-6 source에서 `TaskContractEvidenceAuthority.seal_checkpoint()`와
`PostgresEvidenceRepository.register_authority()`는 System-issued checkpoint를 immutable
RequirementSet snapshot에 등록하고, `EvidenceCheckpointUseRegistry`는 exact TaskContract/source/
target-or-purpose use를 하나의 checkpoint ref로 resolve한다. `evaluate_set()`은 checkpoint에
applicable한 requirement가 0개여도 `all_satisfied=true`를 유지하고 exact empty applicable tuple,
`canonical_hash([])` subset root와 admitted-ref root를 가진 `SATISFIED` evaluation 및
`EvidenceSetSatisfactionAttestation`을 생성한다. 따라서 empty subset도 동일한 P1-6 authority path를
사용할 수 있으며 별도 no-evidence shortcut이 필요하지 않다.

Current source의 admission path는 P1-4와 동일한 `run:{work_run_id}` transaction advisory lock을
사용한다. Set evaluation은 `WorkRunRow FOR UPDATE`와 P1-6 evidence locks를 사용하고,
`load_effective_attestation()`은 current WorkRun state/version, current RequirementSet/root,
checkpoint/root, admitted refs, expiry와 evidence authority revision을 다시 검증하지만 자체
transaction을 연다. 그러므로 later P1-7 gate-open implementation은 shared run transaction 안에서
current P1-6 authority를 transaction-aware하게 다시 읽어야 한다. Process-local cache 또는 shared
transaction 밖에서 먼저 읽은 결과는 gate-open authority가 아니다.

## 3. non-substitution invariants

다음은 이 설계의 load-bearing invariant다.

```text
caller boolean/text != authenticated Human authority
Agent says "human approved" != HumanResult

HumanGate != HumanResult
HumanGateStatus != HumanResult
HumanResult != Judgment
Judgment != TransitionDecision
TransitionDecision != WorkflowState

HUMAN_DIRECT_EVIDENCE != HUMAN_P1_7
HumanResult != EvidenceCandidate
EvidenceCandidate != AdmittedEvidence
AdmittedEvidence != Judgment

G_EVIDENCE != G_HUMAN_* != G_JUDGMENT_*
HumanResult != G_HUMAN_*
Judgment != G_JUDGMENT_*

P1-7 service != P1-4 transition engine
P1-7 persistence != WorkRun mutation authority
```

Agent/LLM 출력, display name, chat message, UI button value, raw `result_kind`, evidence ref 또는
Human silence는 어떤 Human/Judgment guard도 mint하지 않는다.

## 4. HumanGate model

### 4.1 exact lifecycle

Accepted P1-1 lifecycle를 그대로 유지한다.

```text
HumanGateStatus
= NOT_REQUIRED | PENDING | RESOLVED | CANCELLED

HumanGateSuspensionStatus
= NOT_APPLICABLE | ACTIVE | SUSPENDED
```

허용 lifecycle은 다음과 같다.

```text
NOT_REQUIRED -> PENDING
PENDING/ACTIVE -> RESOLVED/NOT_APPLICABLE
PENDING/ACTIVE <-> PENDING/SUSPENDED
PENDING -> CANCELLED/NOT_APPLICABLE
```

`RESOLVED`와 `CANCELLED`는 해당 gate record에서 terminal이다. 만료는 별도 status를 추가하지
않고 additive expiry authority event 뒤 `CANCELLED`로 투영한다. Silence는 만료, 취소, 승인,
거절 또는 rework가 아니다.

### 4.2 exact V1 purpose and multiplicity

V1 exact purpose ref는 다음 하나다.

```text
HumanGatePurposeRef = P1_7_WORK_RESULT_REVIEW@v1
```

이 purpose는 한 번의 `HUMAN_REQUIRED` authority epoch에서 `APPROVE`, `REWORK`, `REJECT` 중
하나를 받는 outcome-review gate다. 세 결과마다 별도 gate를 만들지 않는다.

V1 multiplicity는 다음으로 고정한다.

```text
one current unsuperseded gate
per TaskContract + WorkRun + current HUMAN_REQUIRED authority epoch

conjunctive multi-gate: NOT_SUPPORTED
disjunctive multi-gate: NOT_SUPPORTED
quorum/voting gate: NOT_SUPPORTED
```

여러 Human principal이 한 gate에 submit할 권한을 가질 수는 있지만, gate가 여러 개인 것은
아니다. 다중 결과 winner 규칙은 section 14를 따른다.

### 4.3 System-owned creation and identity

`ADMISSION_PENDING -> HUMAN_REQUIRED` 또는 `REWORK_REQUIRED -> HUMAN_REQUIRED` 요청 전에
P1-7 Human authority는 server-owned gate ref를 reserve한다. `G_HUMAN_REQUIRED` attestation은 exact
gate-opening use의 System-owned `PRE_HUMAN_EVIDENCE` checkpoint와 current effective P1-6
`EvidenceSetSatisfactionAttestation`이 section 9의 binding을 모두 통과한 뒤에만 발행한다. P1-4가
transition을 admit할 때 같은 run transaction에서 gate open event와
`HUMAN_REQUIRED/v+1` projection을 함께 기록한다. Transition이 deny되면 reserved identity와
attestation은 historical denied provenance일 뿐 open gate가 아니다.

`HumanGate`의 immutable minimum fields는 다음과 같다.

```text
human_gate_id / human_gate_version
gate_fingerprint
gate_purpose_id / gate_purpose_version
task_contract_id / task_contract_version
work_run_id
opened_from WorkflowState / state_version
bound WorkflowState = HUMAN_REQUIRED / resulting state_version
opening transition_request_id / transition_decision_id
allowed_result_kinds = APPROVE | REWORK | REJECT
HumanAuthorityPolicyRef / version
designated principal/role selector fingerprint
gate authority id/version
gate_authority_revision
status / suspension_status
blocker_ref when suspended
opened_at
expires_at or null
supersedes_gate_ref or null
```

Gate identity, policy, expiry, allowed outcomes와 binding은 caller metadata에서 만들지 않는다.
TaskContract/System authority가 발행한 exact policy만 사용한다.

### 4.4 state/version rebinding without history mutation

Gate record는 open 시점 binding을 보존한다. `HUMAN_REQUIRED -> BLOCKED`가 admit되면 같은 P1-4
transaction에서 additive `HumanGateAuthorityEvent(SUSPENDED)`를 기록하고 current gate authority
projection을 resulting `BLOCKED/v+1`에 bind한다. `BLOCKED -> HUMAN_REQUIRED`가 admit되면
`REACTIVATED` event가 resulting `HUMAN_REQUIRED/v+1` binding을 만든다. 원 gate/event는 수정하지
않는다.

`BLOCKED -> FAILED`는 pending gate에 `CANCELLED` event를 atomic하게 기록한다. 이 lifecycle
projection을 같은 transaction에 기록할 수 없으면 transition 전체가 fail closed해야 하며
partial WorkRun/gate mutation을 허용하지 않는다.

## 5. Human principal authority

P1-7은 identity provider 제품을 선택하지 않지만 다음 abstraction을 freeze한다.

```text
AuthenticatedHumanPrincipal
HumanPrincipalAuthority
HumanActionAuthority
HumanAuthorityPolicyRef
```

`AuthenticatedHumanPrincipal`의 minimum binding은 다음과 같다.

```text
principal_id
principal_authority_id / principal_authority_version
authentication_session_id
authenticated_at
authentication_expires_at
authentication_strength/policy ref
internal role/subject refs
issuer authenticity
```

`HumanActionAuthority`는 authenticated principal과 exact gate/action을 연결하는 short-lived,
single-purpose server-issued authority다.

```text
principal ref
HumanGate id/version/current authority revision
allowed action = SUBMIT_HUMAN_RESULT
TaskContract/work_run
current HUMAN_REQUIRED state/version
allowed result kinds
issued_at / expires_at
single-use or exact idempotency scope
issuer authority id/version
```

`principal_id`, session ID, role claim 또는 display name을 caller가 문자열로 제공하는 것만으로는
authority가 아니다. Agent가 전달한 Human claim은 인증 입력으로도 사용하지 않는다.

P1-6의 `AuthenticatedHumanPrincipalAuthority`와 같은 upstream identity system을 공유할 수는
있지만 P1-6 `HUMAN_DIRECT_EVIDENCE` ingress token/record를 P1-7 Human action authority로 재사용할
수 없다. 각 semantic owner가 독립 issuer/verifier를 유지한다.

## 6. HumanResult model

### 6.1 exact vocabulary

Accepted exact V1 vocabulary는 다음 세 값뿐이다.

```text
HumanResultKind
= APPROVE | REWORK | REJECT
```

`BLOCK`, `ACCEPTED`, `REWORK_REQUIRED`, `REJECTED`, free-form state name 또는 caller boolean은
`HumanResultKind`가 아니다.

### 6.2 immutable fields

`HumanResult`는 다음 immutable fields를 bind한다.

```text
human_result_id / human_result_version
human_result_fingerprint
HumanGate id/version/current gate_authority_revision
HumanGatePurposeRef
authenticated Human principal ref
HumanActionAuthority ref
task_contract_id / task_contract_version
work_run_id
source WorkflowState = HUMAN_REQUIRED / state_version
eligible target-use set derived from result kind
result_kind
structured_reason_code + reason vocabulary version
optional private comment/content ref + exact hash/sensitivity
submitted_at / admitted_at
idempotency_key / canonical idempotency fingerprint
result authority id/version/revision
supersedes_human_result_ref or null
```

`structured_reason_code`는 server/TaskContract-owned versioned vocabulary다. Free text는 authority가
아니며 optional content ref로만 보존한다.

### 6.3 admission

HumanResult admission은 다음을 같은 PostgreSQL transaction에서 수행한다.

1. shared `run:{work_run_id}` lock과 `WorkRunRow FOR UPDATE`로 current
   `HUMAN_REQUIRED/state_version`을 확인한다.
2. current unsuperseded gate, gate revision, `PENDING/ACTIVE`, non-expiry를 확인한다.
3. authenticated principal과 exact `HumanActionAuthority`를 확인한다.
4. TaskContract/run/purpose/result kind/fingerprint를 확인한다.
5. immutable HumanResult와 result authority event를 append한다.
6. gate projection을 `RESOLVED/NOT_APPLICABLE`로 atomic하게 갱신한다.

HumanResult admission은 `WorkRun.state_version`을 바꾸지 않는다. Result를 저장하는 API가
`WorkflowState`를 update하거나 P1-4 transition을 내부 shortcut으로 호출해서도 안 된다.

## 7. HUMAN_P1_7 producer contract

### 7.1 producer identity

P1-7은 admitted current HumanResult에서 다음 immutable producer ref를 발행할 수 있다.

```text
HumanP1_7EvidenceProducerRef
```

Minimum binding:

```text
producer_ref id/version/fingerprint
P1-7 producer authority id/version
task_contract_id / task_contract_version
work_run_id
source WorkflowState / state_version
HumanGate id/version/authority revision
HumanResult id/version/result authority revision
authenticated principal ref or privacy-preserving internal subject ref
EvidenceCheckpoint id/version
evidence_type id/version
subject/scope/resource identity
content kind = HUMAN_STRUCTURED_REF
owner-backed immutable content ref/hash
sensitivity/export policy
issued_at / expiry
issuer authenticity
```

P1-7 producer ref는 `EvidenceIssuerType.HUMAN_P1_7` 및
`HumanEvidenceProducerCategory.HUMAN_P1_7` candidate만 seed한다. P1-7 owner verifier는 gate,
result, principal, current authority revision과 exact candidate bindings를 검증한다. P1-6
`HUMAN_DIRECT_EVIDENCE` verifier와 issuer handle을 공유하지 않는다.

### 7.2 handoff and rejection

Exact sequence는 다음과 같다.

```text
admitted HumanResult
-> issuer-backed HumanP1_7EvidenceProducerRef
-> P1-6 EvidenceCandidate(category=HUMAN_P1_7)
-> P1-6 EvidenceAdmissionRequest
-> P1-6 EvidenceEvaluation
-> P1-6 ADMITTED or REJECTED
```

```text
HumanResult != EvidenceCandidate
HumanP1_7EvidenceProducerRef != AdmittedEvidence
P1-7 issuer authenticity != P1-6 evidence sufficiency
```

P1-6 rejection은 HumanResult를 지우지 않는다. 해당 post-Human requirement는
`UNSATISFIED`로 남고 `G_EVIDENCE`가 발행되지 않는다. P1-7은 P1-6 exact rejection reason을
보존하고 `HUMAN_EVIDENCE_REJECTED` lifecycle reason으로 표시할 수 있지만 admission truth를
재해석하거나 auto-admit할 수 없다.

Requirement가 exact `HUMAN_P1_7`을 요구하면 `HUMAN_DIRECT_EVIDENCE`는 substitute할 수 없다.
반대로 direct evidence requirement에 P1-7 result를 자동 투입하지 않는다.

## 8. Judgment model

### 8.1 semantic object and exact outcome

`JudgmentStatus=PENDING`은 아직 current authoritative Judgment가 없다는 projection이다. Immutable
Judgment object의 exact V1 outcome은 다음 세 값뿐이다.

```text
JudgmentKind
= ACCEPTED | REJECTED | HOLD_REWORK_REQUIRED
```

`BLOCK`은 JudgmentKind가 아니다. `BLOCKED`는 P1-4 `G_BLOCKER` path다.

### 8.2 exact policy owners

Accepted `TaskContract.judgment_owner_policy`를 유지한다.

```text
SYSTEM_DETERMINISTIC
HUMAN
COMMAND_CENTER
```

P1-7 Judgment authority는 어느 policy가 선택되어도 immutable System-issued Judgment record를
만든다. `HUMAN`은 admitted HumanResult가 semantic input이며, `COMMAND_CENTER`는 exact
Command Center policy/principal authority를 요구한다. `SYSTEM_DETERMINISTIC`은 versioned rule과
admitted refs만 평가한다.

V1에서 Agent/LLM `JudgmentCandidate`는 optional historical provenance로만 보관할 수 있다.
Authoritative Judgment evaluation input, tie breaker, confidence threshold 또는 guard minting
input으로 사용하지 않는다.

### 8.3 immutable fields and evaluation

`Judgment` minimum fields:

```text
judgment_id / judgment_version / judgment_fingerprint
judgment_authority_id / judgment_authority_version / authority revision
task_contract_id / task_contract_version
work_run_id
source WorkflowState / state_version
target-use identity
judgment_owner_policy / policy id/version/fingerprint
HumanGate/HumanResult refs and authority revisions when applicable
P1-6 AdmittedEvidence refs / EvidenceSetSatisfactionAttestation ref/root when applicable
other exact owner-backed policy input refs
JudgmentKind
structured reason taxonomy/version
JudgmentEvaluation ref
issued_at
supersedes_judgment_ref or null
```

`JudgmentEvaluation`은 모든 required input의 authenticity, current revision, Task/run/state/version,
target-use와 policy applicability를 기록한다. Missing/ambiguous/stale input은 fail closed하고
Judgment를 발행하지 않는다.

## 9. G_HUMAN_* owner-bound contract

### 9.1 common attestation binding

`HumanGuardAttestation`은 P1-7 Human authority만 발행한다. 모든 attestation은 최소 다음을
bind한다.

```text
attestation id/version/fingerprint
exact guard_id
semantic_owner = P1_7_HUMAN
P1-7 Human authority id/version/revision
task_contract_id / task_contract_version
work_run_id
source WorkflowState / state_version
target WorkflowState
exact source-target-use fingerprint
HumanGate id/version/current gate_authority_revision
HumanGatePurposeRef
Human principal/result ref when applicable
current result authority revision when applicable
issued_at / expires_at
issuer authenticity
```

`G_HUMAN_REQUIRED`에만 다음 typed payload를 mandatory로 추가한다. 이것은 다른 Human guard의
nullable common field가 아니다.

```text
HumanRequiredEvidenceBinding:
  pre_human_evidence_attestation_ref / attestation_version
  pre_human_checkpoint_ref / checkpoint_version / checkpoint_fingerprint
  pre_human_task_contract_id / task_contract_version
  pre_human_work_run_id
  pre_human_source WorkflowState / state_version
  pre_human_target WorkflowState or transition_purpose_id/version
  pre_human_requirement_set_id / requirement_set_version
  pre_human_requirement_set_root
  ordered_applicable_requirement_refs / pre_human_applicable_subset_root
  ordered_admitted_evidence_refs / admitted_ref_root
  satisfied = true
  pre_human_evidence_authority_version / evidence_authority_revision
  issued_at / expires_at
  pre_human_p1_6_authority_id / authority_version / issuer authenticity
```

`HumanGuardAttestation`은 guard-specific discriminated payload를 사용한다.
`guard_id=G_HUMAN_REQUIRED`이면 `HumanRequiredEvidenceBinding`이 반드시 존재하고, 다른
`G_HUMAN_*`이면 이 payload를 가질 수 없다.

P1-7 issuer는 attestation에서 current `TrustedGuardFact`를 만들 수 있다. Generic P1-4 binding과
request-aware P1-7 verifier가 모두 통과해야 한다.

### 9.2 exact guard predicates

| guard | exact P1-7 predicate |
|---|---|
| `G_HUMAN_REQUIRED` | exact TaskContract/use가 Human result를 요구하고 reserved gate ref가 current이며, section 9.3의 exact current PRE_HUMAN P1-6 authority를 bind하고, P1-4 admitted transition과 atomic하게 `PENDING/ACTIVE`로 열 수 있음 |
| `G_HUMAN_NOT_REQUIRED` | exact TaskContract/use에 HumanResult requirement가 없고 applicable unresolved current gate도 없다는 positive current policy fact |
| `G_NO_PENDING_HUMAN_GATE` | exact run/state/version에 `PENDING/ACTIVE` 또는 `PENDING/SUSPENDED` current gate가 없음 |
| `G_SUSPENDED_HUMAN_GATE` | exact current gate가 `PENDING/SUSPENDED`이고 blocker/provenance와 연결됨 |
| `G_RESUMABLE_HUMAN_GATE` | exact suspended gate가 current policy/principal/task/run에서 still-applicable하며 resulting `HUMAN_REQUIRED` epoch에 rebind 가능 |
| `G_HUMAN_APPROVED` | exact current gate가 `RESOLVED`이고 current unsuperseded HumanResult kind가 `APPROVE` |
| `G_HUMAN_REWORK` | exact current gate가 `RESOLVED`이고 current unsuperseded HumanResult kind가 `REWORK` |
| `G_HUMAN_REJECTED` | exact current gate가 `RESOLVED`이고 current unsuperseded HumanResult kind가 `REJECT` |

Result guard의 `TransitionRequest.human_result_refs`는 exact one current HumanResult ref다. 다른
Human guards는 current P1-4 `required_bound_refs` contract에 따라 empty tuple을 유지하고,
`authority_ref`가 가리키는 attestation에서 gate/policy refs를 검증한다.

Wrong TaskContract, WorkRun, source state/version, target, gate, purpose, principal/result, authority
version/revision, expired/cancelled/superseded gate/result 또는 다른 transition-use는 모두 reject한다.
한 gate/use의 fact를 다른 gate/use에 재사용할 수 없다.

### 9.3 `G_HUMAN_REQUIRED` PRE_HUMAN evidence predicate

모든 Human-required transition-purpose는 TaskContract/System authority가 발행한 exact one current
`PRE_HUMAN_EVIDENCE` checkpoint를 가져야 한다. P1-7은 checkpoint를 caller input, WorkflowState
추론 또는 process configuration으로 선택하지 않는다.

`G_HUMAN_REQUIRED`는 다음 조건이 모두 같은 gate-opening use에 대해 참일 때만 current다.

1. exact TaskContract/use가 Human handling을 요구하고 reserved HumanGate identity/policy가 current다.
2. System-owned PRE_HUMAN checkpoint ref/version/fingerprint가 current이며 exact TaskContract,
   source state/version, target state 또는 transition-purpose와 일치한다.
3. P1-6 owner port가 반환한 exact `EvidenceSetSatisfactionAttestation`이 `satisfied=true`이고
   effective, unexpired, unrevoked, unsuperseded다.
4. Attestation의 TaskContract, WorkRun, source state/version, target/use, checkpoint,
   RequirementSet id/version/full root, ordered applicable refs/subset root, admitted refs/root,
   P1-6 issuer/authority version과 evidence authority revision이 current authority와 exact match한다.
5. 그 exact values가 `HumanRequiredEvidenceBinding`에 commit되어 있고, reserved gate를 admitted
   transition과 같은 transaction에서 열 수 있다.

Checkpoint-applicable tuple 자체가 empty여도 이 predicate는 면제되지 않는다. P1-6가 exact
checkpoint를 평가하여 생성한 empty applicable tuple, exact empty roots와 `SATISFIED` attestation을
그대로 bind한다. Required row는 없지만 `NOT_REQUIRED`/`FORBIDDEN` directive가 checkpoint에
applicable하면 P1-6가 계산한 실제 applicable refs/subset root를 bind하며 P1-7이 empty로 바꾸지 않는다.
P1-7은 P1-6 evaluation을 재수행하거나 evidence truth를 재발행하지 않고, `no evidence required`
boolean/정책 문구/빈 ref를 대체 authority로 인정하지 않는다.

Missing, stale, expired, revoked, superseded 또는 wrong-bound PRE_HUMAN authority이면 P1-7 verifier는
`G_HUMAN_REQUIRED`를 recognize하지 않는다. 결과는 no current guard fact, no gate-open event, no
`HUMAN_REQUIRED` transition이며 P1-4의 exact denied provenance만 허용된다.

## 10. G_JUDGMENT_* owner-bound contract

### 10.1 common attestation binding

`JudgmentGuardAttestation`은 P1-7 Judgment authority만 발행한다.

```text
attestation id/version/fingerprint
exact guard_id
semantic_owner = P1_7_JUDGMENT
P1-7 Judgment authority id/version/revision
task_contract_id / task_contract_version
work_run_id
source WorkflowState / state_version
target WorkflowState / exact source-target-use fingerprint
Judgment id/version/current judgment authority revision
HumanGate/HumanResult refs and revisions when applicable
G_EVIDENCE attestation ref/root/revision when applicable
policy id/version/fingerprint
issued_at / expires_at
issuer authenticity
```

### 10.2 exact mapping

| exact guard | required current JudgmentKind |
|---|---|
| `G_JUDGMENT_ACCEPTED` | `ACCEPTED` |
| `G_JUDGMENT_REJECTED` | `REJECTED` |
| `G_JUDGMENT_REWORK` | `HOLD_REWORK_REQUIRED` |

각 Judgment guard의 `TransitionRequest.judgment_refs`는 exact one current Judgment ref다.
`Judgment` 자체, raw result, Agent proposal 또는 P1-6 attestation은 guard fact가 아니다.

Verifier는 Judgment가 current unsuperseded인지, HumanResult/gate dependency와 evidence authority가
여전히 effective한지, Task/run/source state/version/target-use와 policy/authority revision이 exact
match하는지 확인한다. 하나라도 stale하면 guard를 recognize하지 않는다.

## 11. P1-4 transition handoff

Exact handoff는 다음 하나뿐이다.

```text
current P1-7 Human/Judgment durable authority
-> exact HumanGuardAttestation / JudgmentGuardAttestation
-> exact TrustedGuardFact
-> P1-4 FutureOwnerGuardVerifier(fact, TransitionRequest)
-> TransitionEvaluation
-> TransitionDecision
-> only when ADMITTED: atomic WorkRun mutation/state_version + 1
```

P1-7은 `TransitionRequest`를 제안할 수 있으나 `TransitionDecision`을 만들거나 WorkRun row를
직접 update하지 않는다. `HumanResult.save()` 또는 `Judgment.save()`에 state mutation side effect를
넣지 않는다.

P1-7 implementation은 current P1-4의 separate verifier slots를 그대로 사용한다.

```text
one verifier for P1_7_HUMAN
one verifier for P1_7_JUDGMENT
```

Guard issuance/current-revision validation과 P1-4 evaluation은 shared `run:{work_run_id}`
serialization boundary 안에서 수행되어야 한다. Process-local cache만으로 current authority를
증명할 수 없다. Current synchronous verifier port가 transaction-bound reload를 보장하기에
부족하면 later implementation은 P1-4 semantics를 바꾸지 않는 narrow transaction-context
integration을 추가해야 한다. 그 integration 없이 stale cached fact를 accept해서는 안 된다.

Gate-open transition의 exact transaction order는 다음과 같다.

1. P1-4 canonical `run:{work_run_id}` advisory transaction lock을 먼저 획득한다.
2. `WorkRunRow FOR UPDATE` 후 current TaskContract, WorkflowState, `state_version`과 transition use를
   검증한다.
3. System-owned exact PRE_HUMAN checkpoint를 resolve하고, transaction-aware P1-6 owner port로 current
   effective attestation과 RequirementSet/full root/subset root/evidence authority revision을 다시
   읽는다. P1-6 authority serialization lock이 필요하면 run/row lock 뒤 deterministic order로
   같은 transaction에서 획득한다.
4. Exact `HumanRequiredEvidenceBinding`을 포함한 current `G_HUMAN_REQUIRED` fact를 발행하고 P1-4가
   같은 transaction의 exact `TransitionRequest`에 대해 평가한다.
5. `ADMITTED`일 때만 gate-open event와 `WorkRun=HUMAN_REQUIRED/state_version+1`을 atomic append한다.
   어느 participant라도 실패하면 모두 rollback한다.

Current P1-6 `load_effective_attestation()`처럼 자체 transaction을 여는 reload만으로 step 3을
대체할 수 없다. Later implementation은 current P1-6 truth를 복제하지 않는 narrow transaction-aware
read/verify port를 사용해야 한다.

Gate open/suspend/reactivate/cancel lifecycle projection이 P1-4 admitted transition에 필수인 row는
동일 database transaction의 owner participant로 append한다. Participant failure는 전체 transition
rollback이다. 이 participant는 새 guard나 state를 만들지 않으며 P1-4 admission을 우회하지 않는다.

## 12. P1-6 pre-/post-Human evidence integration

### 12.1 non-deadlocking sequence

```text
PRE_HUMAN_EVIDENCE checkpoint
-> exact checkpoint-applicable requirements evaluated by P1-6
-> applicable subset is SATISFIED, including an exact empty subset/root when no row applies
-> P1-6 exact pre-Human EvidenceSetSatisfactionAttestation
-> exact HumanRequiredEvidenceBinding and gate-open policy input; P1-6 does not open a gate
-> P1-4 may admit ADMISSION_PENDING/REWORK_REQUIRED -> HUMAN_REQUIRED

HumanGate PENDING/ACTIVE
-> admitted HumanResult
-> gate RESOLVED

when exact POST_HUMAN_EVIDENCE requirement applies:
HumanP1_7EvidenceProducerRef
-> P1-6 candidate/admission
-> post-Human set evaluation
-> exact post-Human G_EVIDENCE attestation

current HumanResult + applicable P1-6 refs + exact policy
-> Judgment
-> exact P1-7 guard facts
-> P1-4 transition request/evaluation/decision/mutation
```

P1-6 accepted contract에 따라 pre-Human attestation은
`ADMISSION_PENDING -> HUMAN_REQUIRED` matrix row의 `G_EVIDENCE`로 삽입하지 않는다. 그 row에는
`G_HUMAN_REQUIRED`만 있다. Pre-Human attestation은 gate-open policy의 exact owner-backed input이며
P1-7이 P1-6 truth를 재발행하는 것이 아니다. `REWORK_REQUIRED -> HUMAN_REQUIRED`에도 동일한 exact
PRE_HUMAN binding rule을 적용하며, 다른 transition-purpose의 attestation을 rebind할 수 없다.

### 12.2 which outcome transitions require post-Human G_EVIDENCE

Current exact matrix에서:

- `HUMAN_REQUIRED -> ACCEPTED`는 `G_EVIDENCE`를 요구한다. TaskContract가 final Human evidence를
  `HUMAN_P1_7`으로 지정하면 exact `POST_HUMAN_EVIDENCE` admission과 attestation이 mandatory다.
- `HUMAN_REQUIRED -> REWORK_REQUIRED`는 `G_EVIDENCE`를 요구하지 않는다. Exact Human result,
  `G_JUDGMENT_REWORK`, `G_REWORK_SPEC`가 필요하다.
- `HUMAN_REQUIRED -> REJECTED`는 `G_EVIDENCE`를 요구하지 않는다. Exact Human result와
  `G_JUDGMENT_REJECTED`가 필요하다.

Rework/reject Judgment policy가 admitted evidence를 semantic input으로 요구할 수는 있지만 그것이
matrix에 없는 새 `G_EVIDENCE` guard를 만들지는 않는다. P1-4 guard set 변경이 필요하면 별도
predecessor baseline Task가 필요하다.

### 12.3 authority revision propagation

HumanResult/gate가 supersede/revoke되면 P1-7 `HUMAN_P1_7` issuer verifier는 즉시 old producer ref를
reject한다. 해당 ref가 P1-6 admission/attestation에 기여했다면 P1-7은 P1-6 owner port에 exact
producer invalidation을 요청한다. P1-6만 evidence authority event와 set-attestation invalidation을
입장한다. 그 작업이 complete하지 않으면 dependent Judgment/guards는 fail closed한다.

## 13. outcome mapping

HumanResult, Judgment, guard와 WorkflowState는 separate layers지만 exact compatibility는 다음과
같다.

| HumanResultKind | eligible Human guard | eligible JudgmentKind | eligible P1-4 target | additional exact guards |
|---|---|---|---|---|
| `APPROVE` | `G_HUMAN_APPROVED` | `ACCEPTED` | `ACCEPTED` | `G_EVIDENCE`, `G_JUDGMENT_ACCEPTED` |
| `REWORK` | `G_HUMAN_REWORK` | `HOLD_REWORK_REQUIRED` | `REWORK_REQUIRED` | `G_JUDGMENT_REWORK`, `G_REWORK_SPEC` |
| `REJECT` | `G_HUMAN_REJECTED` | `REJECTED` | `REJECTED` | `G_JUDGMENT_REJECTED` |

이 표는 direct mutation mapping이 아니다. 각 row는 current HumanResult가 해당 Judgment/guard
evaluation의 eligible input이라는 뜻이며, P1-4가 나머지 guard를 separately admit해야 한다.

```text
HumanResult(APPROVE) != Judgment(ACCEPTED) != WorkflowState.ACCEPTED
HumanResult(REWORK) != Judgment(HOLD_REWORK_REQUIRED) != WorkflowState.REWORK_REQUIRED
HumanResult(REJECT) != Judgment(REJECTED) != WorkflowState.REJECTED
```

HumanResult와 contradiction인 Judgment는 발행할 수 없다. `BLOCKED`/`FAILED`는 이 outcome mapping
밖의 P1-4 control/technical paths다.

## 14. concurrency, idempotency, and replay

### 14.1 lock order and current authority

P1-7 transaction의 canonical first lock은 P1-4/P1-6과 같은
`run:{work_run_id}` advisory transaction lock이다. 이후 `WorkRunRow FOR UPDATE`, exact gate/result 또는
Judgment identity lock을 deterministic order로 획득한다. 모든 admission은 current WorkRun과
authority revision을 lock 안에서 다시 읽는다. Gate-open path는 P1-6 current effective PRE_HUMAN
attestation 및 full/subset roots/evidence authority revision도 이 lock 경계 안에서 다시 읽는다.

### 14.2 idempotency

```text
same immutable request ID + same canonical fingerprint
-> same immutable gate/result/Judgment/decision response

same immutable request ID + different fingerprint
-> identity conflict
-> no new authority event
```

Gate-open duplicate는 exact same reserved/open gate를 반환한다. Result/Judgment duplicate는 existing
immutable record를 반환한다.

### 14.3 concurrent Human result winner

V1 winner policy는 다음으로 고정한다.

```text
FIRST_DURABLY_ADMITTED
```

Exact 의미:

- authorized submissions는 gate row lock 아래 serialized된다.
- P1-7 validation을 모두 통과하고 smallest durable result-admission event sequence를 얻은 하나만
  gate를 `RESOLVED`로 만든다.
- client timestamp, network arrival claim, display role order 또는 last-write-wins는 authority가
  아니다.
- same ID/fingerprint retry는 winner record를 반환한다.
- 다른 result ID는 gate가 이미 resolved되었으므로 `HUMAN_GATE_CLOSED`로 reject된다.
- 결과 correction은 winner overwrite가 아니라 section 15의 new gate/result lineage다.

V1은 quorum, majority, priority vote 또는 multiple-approval aggregation을 지원하지 않는다.

### 14.4 stale and replay

다음은 모두 fail closed다.

```text
state_version changed before HumanResult admission
PRE_HUMAN attestation missing or no longer effective before G_HUMAN_REQUIRED issue/use
PRE_HUMAN checkpoint, TaskContract, WorkRun, source state/version, target/use or roots mismatch
P1-6 evidence authority revision changed before G_HUMAN_REQUIRED use
gate revision changed before result admission
result/gate changed before Judgment issue
evidence revision changed before Judgment issue
Judgment/result/gate changed before P1-4 guard use
old guard used for another target/use
```

Old guard fact를 새 state/version, 다른 gate transition-purpose 또는 새 P1-6 evidence authority
revision에 auto-rebind하지 않는다. Retry는 shared transaction에서 fresh WorkRun과 P1-6 authority를
다시 읽은 새 request다.

## 15. correction, revocation, and supersession

Historical gate/result/Judgment는 in-place mutate하지 않는다.

```text
correction
-> new immutable object/event
-> explicit supersedes ref
-> authority revision increment
-> old guard attestations unusable
```

Current WorkRun이 아직 `HUMAN_REQUIRED`인 동안 authorized correction은 current resolved gate를
supersede하는 새 gate를 동일 state/version의 새 Human authority epoch로 열 수 있다. 이는
WorkflowState self-transition이 아니고 `state_version`을 변경하지 않는 P1-7 authority operation이다.
새 gate는 old gate/result refs를 보존하며 exact new HumanResult를 요구한다.

Terminal P1-4 transition이 이미 admit된 뒤에는 같은 WorkRun에서 Human/Judgment correction으로
terminal state를 되돌릴 수 없다. Correction은 새 TaskContract/WorkRun lineage에서 처리한다.

Revocation/supersession은:

1. P1-7 authority revision을 증가시킨다.
2. old `G_HUMAN_*`/`G_JUDGMENT_*` attestation을 unusable하게 만든다.
3. dependent `HUMAN_P1_7` producer ref를 invalid하게 만든다.
4. P1-6 dependent evidence가 있으면 P1-6-owned invalidation을 요구한다.
5. 과거 P1-4 transition/event를 rewrite하지 않는다.

### 15.1 V1 policy exception/override

```text
V1 policy exception / override: NOT_SUPPORTED
```

Human은 forbidden security boundary, identity/authenticity, P1-6 evidence truth, P1-4 transition
ownership 또는 stale version을 override할 수 없다. Exception semantics가 필요하면 별도 baseline
design과 Human acceptance가 필요하다.

## 16. persistence and restart

Future implementation 방향은 PostgreSQL, append-only provenance, deterministic restart
reconstruction이다. Minimum durable concepts는 다음과 같다.

```text
HumanGateRow / HumanGateRef
HumanGateAuthorityEventRow
current HumanGate projection

HumanResultRow / HumanResultRef
HumanResultAuthorityEventRow
current HumanResult authority projection

HumanP1_7EvidenceProducerRow / Ref

JudgmentRow / JudgmentRef
JudgmentEvaluationRow
JudgmentAuthorityEventRow
current Judgment authority projection

HumanGuardAttestationRow
JudgmentGuardAttestationRow
```

`HumanGuardAttestationRow(guard_id=G_HUMAN_REQUIRED)`는 section 9.1의 typed
`HumanRequiredEvidenceBinding` 전체를 durable하게 보존한다. Restart reconstruction은 referenced
P1-6 attestation을 current P1-6 owner port로 다시 검증하고 current WorkRun/checkpoint/
RequirementSet/evidence authority와 exact match할 때만 guard authority를 effective로 project한다.

각 append-only authority event는 monotonic event sequence, object/ref, TaskContract/run,
state/version, prior/new authority revision, owner, reason, timestamp와 affected refs를 보존한다.

Restart는 ordered provenance로 다음을 reconstruct한다.

```text
current gate and lifecycle/suspension
current result authority
current Judgment authority
effective HUMAN_P1_7 producer refs
effective Human/Judgment guard attestations
```

Stored projection과 reconstructed history가 다르거나 missing/orphaned event, illegal lineage,
identity conflict, revision gap이 있으면:

```text
AUTHORITY_CONFLICT or PROVENANCE_INCOMPLETE
-> fail closed
-> no auto repair
-> no new HumanResult/Judgment/guard
-> no P1-4 transition request
```

## 17. security, privacy, and export

P1-7 Human artifact sensitivity는 P1-6과 동일한 exact vocabulary를 사용한다.

```text
PUBLIC_SAFE
INTERNAL
PRIVATE_SENSITIVE
SECRET_FORBIDDEN
```

| class | durable handling | review export | public Cycle/Replay |
|---|---|---|---|
| `PUBLIC_SAFE` | exact sanitized structured body/ref 허용 | policy가 허용한 body/ref | explicit public-export policy가 허용한 최소 projection만 |
| `INTERNAL` | access-controlled store | authorized reviewer에게 metadata/ref 또는 exact permitted body | default deny; sanitized metadata만 explicit policy로 허용 |
| `PRIVATE_SENSITIVE` | encrypted/access-controlled private ref; hash/classification만 authority record에 보존 | separate authorized private channel only | body/comment/principal identity 금지 |
| `SECRET_FORBIDDEN` | raw body reject; security policy에 따라 quarantine/destroy | sanitized detector/rejection metadata only | export 금지 |

Raw secret, credential, private token, session secret는 Human comment/reason/evidence body로 받거나
보존하지 않는다.

Authenticated principal internal identity와 public display identity는 분리한다. V1 public
provenance 기본값은 다음이다.

```text
human_review = performed | pending | not_required
principal_display = HUMAN_REVIEWER
internal principal/session identifiers = omitted
comment/reason body = omitted
result_kind = only when explicitly classified PUBLIC_SAFE
```

Run/Replay visibility는 private Human artifact read authority가 아니다. Public display label은
identity proof로 역사용할 수 없다.

## 18. rejection and failure taxonomy

P1-7 native sanitized reason set은 다음으로 freeze한다.

```text
UNKNOWN_HUMAN_GATE
HUMAN_GATE_VERSION_MISMATCH
HUMAN_GATE_NOT_CURRENT
HUMAN_GATE_CLOSED
HUMAN_GATE_CANCELLED
HUMAN_GATE_EXPIRED

HUMAN_PRINCIPAL_NOT_AUTHORIZED
HUMAN_AUTHORITY_MISMATCH

TASK_CONTRACT_MISMATCH
WORK_RUN_MISMATCH
WORKFLOW_STATE_MISMATCH
STATE_VERSION_MISMATCH
TRANSITION_PURPOSE_MISMATCH

HUMAN_RESULT_IDENTITY_CONFLICT
HUMAN_RESULT_STALE
HUMAN_RESULT_SUPERSEDED

HUMAN_EVIDENCE_ADMISSION_REQUIRED
HUMAN_EVIDENCE_REJECTED

PRE_HUMAN_EVIDENCE_AUTHORITY_MISSING
PRE_HUMAN_EVIDENCE_AUTHORITY_MISMATCH
PRE_HUMAN_EVIDENCE_AUTHORITY_STALE

JUDGMENT_INPUT_INCOMPLETE
JUDGMENT_POLICY_MISMATCH
JUDGMENT_STALE
JUDGMENT_SUPERSEDED

GUARD_AUTHORITY_MISMATCH
GUARD_REPLAY_REJECTED

AUTHORITY_CONFLICT
PROVENANCE_INCOMPLETE
```

이 reason은 raw private data를 포함하지 않는다. P1-4가 transition을 deny하면 P1-7은 P1-4 exact
`DecisionReason` (`STALE_REQUEST`, `INVALID_TRANSITION`, `MISSING_GUARD`, `GUARD_FAILED`,
`CONTRACT_MISMATCH`, `RUNTIME_MODE_MISMATCH`)을 변경하지 않는다. P1-6가 evidence를 reject하면
P1-6 exact `EvidenceRejectionReason`을 원인으로 보존하고 P1-7 wrapper reason으로 evidence truth를
재분류하지 않는다.

`HUMAN_GATE_EXPIRED`는 새 lifecycle status가 아니라 expiry event로 `CANCELLED` projection을 만든
reason이다. `HUMAN_EVIDENCE_REJECTED`는 P1-7 pipeline 상태 이유이며 P1-6의 exact rejection code를
대체하지 않는다. `PRE_HUMAN_EVIDENCE_AUTHORITY_*`는 P1-7 guard prerequisite의 sanitized failure이고
P1-6 evaluation/rejection을 재분류하지 않는다. P1-6가 반환한 exact source reason/provenance는
그대로 보존한다.

## 19. future implementation ownership

P1-7은 separate semantic owner packages를 사용한다.

```text
src/aiscc/human/**
-> principal/action authority
-> HumanGate lifecycle
-> HumanResult admission
-> HUMAN_P1_7 producer
-> P1_7_HUMAN verifier

src/aiscc/judgment/**
-> Judgment policy/evaluation
-> Judgment persistence authority
-> P1_7_JUDGMENT verifier
```

Narrow integrations:

| root | allowed future responsibility |
|---|---|
| `src/aiscc/workflow/**` | existing owner verifier registration, transaction-bound P1-7 fact validation, atomic gate lifecycle participant; no state/matrix change |
| `src/aiscc/evidence/**` | exact `HUMAN_P1_7` issuer verifier/producer invalidation handoff; no P1-6 admission semantic change |
| `src/aiscc/persistence/**` | P1-7 append-only rows, projections, locks, restart reconstruction; no P1-4 history rewrite |
| `src/aiscc/contracts/**` | immutable public/internal DTO ports only; no caller-minted authority |

Future implementation must publish an exact file/migration/test allowlist. This design authorizes no
source, migration, test 또는 dependency change.

## 20. mandatory future implementation proof matrix

| proof class | mandatory future proof |
|---|---|
| `NON_SUBSTITUTION` | Agent claim, caller `approved=true`, display name, raw result enum이 HumanResult/Judgment/guard/state를 만들지 않음 |
| `HUMAN_GATE_AUTHORITY` | server-issued exact gate만 open; wrong Task/run/purpose/version 또는 arbitrary caller gate reject |
| `HUMAN_PRINCIPAL_AUTHORITY` | wrong/expired/session-mismatched principal/action authority reject; display identity는 authority 아님 |
| `HUMAN_RESULT_IDEMPOTENCY` | same ID+fingerprint는 same immutable result; same ID+different fingerprint는 `HUMAN_RESULT_IDENTITY_CONFLICT` |
| `HUMAN_RESULT_STALENESS` | stale WorkRun/gate/result authority revision은 no result/no gate resolution |
| `HUMAN_P1_7_EVIDENCE_HANDOFF` | P1-7 producer ref는 candidate만 seed; P1-6 admission 전 `AdmittedEvidence`/`G_EVIDENCE` 없음 |
| `POST_HUMAN_EVIDENCE_NON_DEADLOCK` | pre-Human subset은 final Human requirement 없이 만족 가능; post-Human exact producer admission 후에만 accepted-use attestation 가능 |
| `PRE_HUMAN_EVIDENCE_GATE_BINDING` | missing attestation, wrong checkpoint/TaskContract/WorkRun/source state-version/target-use/RequirementSet full root/applicable subset root, expired/revoked/superseded 또는 stale evidence authority revision은 no `G_HUMAN_REQUIRED`/no gate/no transition; exact current attestation+gate policy만 issue 가능; empty applicable subset도 exact P1-6 SATISFIED attestation이 mandatory; concurrent authority change는 stale fact reject |
| `JUDGMENT_AUTHORITY` | HumanResult/Agent proposal/admitted evidence alone은 Judgment 아님; complete current policy inputs만 exact Judgment 발행 |
| `G_HUMAN_BINDING` | wrong gate/result/principal/Task/run/state/version/target/revision/expiry는 guard verifier reject |
| `G_JUDGMENT_BINDING` | wrong Judgment/Human/evidence/policy/Task/run/state/version/target/revision은 guard verifier reject |
| `P1_4_TRANSITION_HANDOFF` | HumanResult/Judgment persistence는 WorkRun을 변경하지 않으며 P1-4 ADMITTED decision만 mutation |
| `CONCURRENT_HUMAN_RESULT` | PostgreSQL concurrency에서 exactly one `FIRST_DURABLY_ADMITTED` winner; loser는 closed-gate reject |
| `CORRECTION_SUPERSESSION` | correction은 additive new gate/result/Judgment; old records remain and old guards unusable |
| `GUARD_ANTI_REPLAY` | new state_version/gate revision/target-use에서 old Human/Judgment guard unusable |
| `RESTART` | PostgreSQL restart 후 current gate/result/Judgment/guard authority가 identical reconstruction; corruption fail closed |
| `SECURITY_EXPORT` | raw secret/private comment/internal principal/session은 review/public/Replay boundary 밖; sanitized projection만 허용 |

Additional mandatory runtime assertions:

- P1-6 rejects `HUMAN_P1_7` candidate -> requirement remains `UNSATISFIED`, no Judgment/guard/state.
- Current post-Human evidence + current HumanResult + exact policy -> eligible Judgment, not direct state.
- Old HumanResult superseded -> old `G_HUMAN_*` and dependent `G_JUDGMENT_*` unusable.
- Old Judgment superseded -> old `G_JUDGMENT_*` unusable.
- `HumanResult`/`Judgment` transaction failure -> no partial gate/authority projection.
- Gate lifecycle participant failure during admitted-target transaction -> no partial WorkRun mutation.

## 21. non-goals

이 V1 design의 non-goals:

- P1-7 runtime/source/database/test implementation
- P1-8 Cycle, project closure, memory, NextAction design/implementation
- new `WorkflowState`, transition pair 또는 guard ID
- conjunctive/disjunctive/quorum/voting Human gates
- Human policy exception/override
- external identity provider selection/integration
- public Human review UI/notification system
- LLM-as-judge 또는 Agent-authored authoritative Judgment
- P1-6 evidence admission redesign
- P1-4 transition engine replacement
- provider call, credential, deployment, Public Bounded Live release

## 22. unresolved and deliberately deferred questions

P1-7 core authority semantics에 대한 unresolved load-bearing question은 없다. 다음은 implementation
선택으로 deliberate defer하며 authority semantics를 바꿀 수 없다.

- external authentication/identity provider 제품
- notification transport와 Human review UI
- physical PostgreSQL table/index names와 retention durations
- private comment object-store 제품
- public sanitized display의 presentation text

이 선택은 authenticated authority, exact binding, first-durable winner, privacy default-deny 또는
P1-4/P1-6 owner separation을 약화할 수 없다.

## 23. Human design review

미해결 preference 질문은 없다. Human final review는 다음 candidate decisions를 exact
accept/rework 대상으로 판단해야 한다.

1. V1 gate multiplicity: one current gate per current `HUMAN_REQUIRED` authority epoch.
2. exact HumanResult vocabulary: `APPROVE | REWORK | REJECT`.
3. policy exception/override: `NOT_SUPPORTED`.
4. concurrent winner: `FIRST_DURABLY_ADMITTED` under PostgreSQL serialization.
5. Agent/LLM proposal: historical non-authoritative provenance only; Judgment input/guard authority 아님.
6. public identity: internal identity/session/comment default omitted; `HUMAN_REVIEWER` sanitized label.
7. `G_HUMAN_REQUIRED`: exact current P1-6 PRE_HUMAN attestation을 typed payload로 bind하며 empty
   applicable subset에도 별도 shortcut 없이 동일 attestation path를 요구함.

```text
Human design verification: HUMAN_PENDING
P1-7 runtime: NOT_STARTED
P1-8: NOT_STARTED
```
