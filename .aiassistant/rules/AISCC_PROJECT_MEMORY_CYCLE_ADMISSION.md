# AISCC Project Memory and Cycle Admission Design

document_id: `AISCC-P1-8-PROJECT-MEMORY-CYCLE-ADMISSION-DESIGN-1`  
design_status: `REWORKED_DESIGN_CANDIDATE / HUMAN_PENDING`  
acceptance_owner: `Human`  
implementation_status: `DESIGN_ONLY`  
predecessor_handoff_sha256: `0169b07642e72d1c7025c98946402e53102c3de2f72a4b3df78ba0ed851004c5`  
predecessor_design_sha256: `8024613cc0c4d525e010db937ba8a249dcbfa77feeb7faa5cc9f6862864068b2`  
closed_1933_rework_hold_cycle_sha256: `305ec8c3d38f9faa8544c7e56227b4162d8ca14d29ae42c0eabf2744e287374d`  
closed_2011_source_current_hold_cycle_sha256: `1d583e3cb414d69ba25d0233614d75cd91cf858ea5be649904337de2c6589952`  
rework_hold_cycle_sha256: `48205ef25d1f5e092717a372aab4f062d758eafc00b3d7c52a7058e4c00187ba`  
created_at_kst: `2026-08-30`

> 이 문서는 P1-8 구현 권한이 아니라 Human review를 위한 design candidate다. `HUMAN_PENDING` 상태에서는 canonical rule, TaskContract, runtime authority 또는 accepted baseline으로 사용할 수 없다.

## 1. Purpose and scope

이 설계는 AISCC의 accepted execution provenance를 재사용 가능한 project memory로 투영하는 admission boundary와 그 결과를 사용하는 V1 Next Action 선택 모델을 고정한다.

범위는 다음으로 제한한다.

- runtime admission 대상과 저장 의미를 정의한다.
- repository Markdown인 `CommandCenterCycleRecord`와 runtime authority인 `AdmittedCycle`을 분리한다.
- raw session, Agent summary, executor prose가 memory authority로 승격되는 경로를 차단한다.
- rejected, HOLD, failed, blocked, rework provenance와 reusable curated memory의 관계를 고정한다.
- append-only correction, supersession, revocation과 historical/current applicability를 분리한다.
- PostgreSQL concurrency, idempotency, transaction, restart, corruption 처리 계약을 정의한다.
- V1 Next Action owner를 하나로 고정하고 Proposal, Evaluation, Selection, TransitionDecision을 분리한다.

다음은 명시적으로 범위 밖이다.

- runtime source, test, migration 또는 schema 생성
- 대형 RAG/vector/search platform
- P2 Command Center UI
- Self-Dogfooding cutover
- P3 deployment, Public Live, credentialed external action
- P1-4/P1-6/P1-7 authority의 변경, 흡수 또는 재해석

## 2. Predecessor authority map

P1-8은 predecessor가 소유한 사실을 읽고 exact immutable reference로 연결할 뿐 다시 판정하지 않는다.

| Domain object / fact | Existing owner | P1-8 relation | Forbidden substitution |
|---|---|---|---|
| `TaskContract` identity/version/scope | Task authority | admission scope와 memory source scope로 참조 | memory가 TaskContract를 수정하거나 대체 |
| `WorkRun` state/version | P1-4 workflow kernel | exact terminal snapshot 검증 | Cycle이 WorkflowState를 선언 |
| `TransitionRequest` / `TransitionEvaluation` / `TransitionDecision` | P1-4 | accepted terminal lineage 참조 | NextActionSelection 또는 CycleAdmissionDecision이 state mutation |
| `EvidenceCandidate` / `AdmittedEvidence` | P1-6 | Judgment와 terminal decision이 사용한 exact refs 참조 | P1-8이 evidence truth/admission 재판정 |
| `EvidenceSetSatisfactionAttestation` / root | P1-6 | exact work run/checkpoint/state/version/authority revision binding 확인 | memory summary가 evidence attestation |
| `HumanGate` / `HumanResult` | P1-7 Human Gate | Judgment provenance로만 참조 | Agent approval 또는 memory가 HumanResult |
| `Judgment` | P1-7 Judgment authority | accepted admission prerequisite와 exact ref | CycleEvaluation이 Judgment |
| `CommandCenterCycleRecord` | repository Command Center governance | public/human-readable provenance projection | Markdown record가 runtime admitted Cycle |
| `AdmittedCycle` / project-memory projection | P1-8 | 이 설계가 정의하는 새 runtime authority | raw session 또는 Command Center Markdown이 직접 생성 |
| `NextActionSelection` | P1-8 System selection authority | versioned deterministic policy 결과 | Agent proposal 또는 TransitionDecision과 동일시 |

P1-8은 P1-4의 state machine, P1-6의 evidence admission, P1-7의 Human/Judgment guard list를 변경하지 않는다. 특히 `G_SUSPENDED_HUMAN_GATE`, `G_RESUMABLE_HUMAN_GATE`를 포함한 P1-7 Human guard 8개와 Judgment guard 3개는 predecessor authority 그대로다.

## 3. Exact domain vocabulary

### 3.1 Admission objects

- `CycleCandidate`: caller가 제출한 structured candidate. 아직 accepted provenance도 memory도 아니다.
- `CycleAdmissionRequest`: candidate ID, caller ID, idempotency key, expected source bindings를 담은 immutable request.
- `CycleEvaluation`: System이 predecessor refs, eligibility, schema, privacy, lineage, current binding을 평가한 immutable 설명.
- `CycleAdmissionDecision`: `ADMITTED` 또는 `REJECTED`를 고정하는 P1-8 System-owned immutable decision.
- `AdmittedCycle`: `ADMITTED` decision에 의해 생성되는 immutable accepted runtime provenance aggregate.
- `CycleAuthorityEvent`: correction, supersession, revocation, projection 변화의 append-only event.

### 3.2 Memory objects

- `MemoryDeclaration`: CycleCandidate 안의 typed structured memory 요청. admission 전에는 authority가 없다.
- `MemoryDeclarationAuthorityPolicy`: category별 source-to-content authority mode, source kind, derivation schema, scope/privacy ceiling을 고정하는 P1-8 System-owned immutable policy.
- `ProjectMemoryEntry`: AdmittedCycle에서 결정론적으로 투영된 immutable reusable memory item.
- `ProjectMemoryEntryId`: 한 accepted Cycle projection에서 생성된 immutable entry identity.
- `MemoryLineageKey`: accepted successor Cycles 사이에서 안정적으로 유지되는 semantic lineage identity.
- `CycleMemoryReference`: 새 entry를 만들지 않고 기존 동일-content current entry를 새 AdmittedCycle에 연결하는 immutable provenance link.
- `ProjectMemoryApplicability`: historical entry가 현재 선택 입력으로 사용 가능한지 나타내는 append-only 상태 해석.
- `ProjectMemoryView`: current applicable entries의 reconstructable projection/cache. authority source가 아니다.
- `MemoryRetrievalResult`: exact query specification과 ordered memory refs를 담은 재현 가능한 결과.

### 3.3 Next Action objects

- `NextActionProposal`: Agent, Human, executor 또는 System component가 제출할 수 있는 비권위 후보.
- `ActionRef`: exact enrolled NextActionDescriptor의 policy/action identity와 fingerprint를 가리키는 immutable ref.
- `NextActionDescriptor`: action kind, scope, parameter schema, authority source, Human/Task issuance boundary를 고정한 enrolled immutable definition.
- `NextActionEligibilityPolicy`: eligible descriptor catalog, source enrollment, scope/schema constraints를 소유하는 versioned P1-8 System policy.
- `NextActionSelectionPolicy`: eligible actions에 적용할 authoritative priority-source mapping, reason codes, ordering/tie-break만 소유하는 versioned P1-8 System policy. Action enrollment 권한은 없다.
- `NextActionEvaluation`: versioned selection policy가 proposals와 authoritative inputs에 적용된 immutable System 평가.
- `NextActionSelection`: V1에서 P1-8 System만 소유하는 authoritative project-next-action 선택.
- `TaskIssuanceCandidate`: selected descriptor/template와 validated parameters를 외부 Task authority에 전달하는 non-authoritative issuance request.
- `TransitionDecision`: P1-4가 소유하는 WorkRun state mutation decision. NextActionSelection과 별개다.

### 3.4 Repository record term

- `CommandCenterCycleRecord`: `.aiassistant/records/aiscc/cycles/*.md`에 존재하는 repository Markdown Cycle Record의 exact term이다. accepted, rejected, HOLD, failed, rework provenance를 human-readable하게 기록할 수 있지만 runtime admission authority는 아니다.

`CycleRecord`라는 무수식 용어는 새 runtime code/schema/API에서 금지한다. 문맥 충돌을 피하기 위해 runtime은 반드시 `AdmittedCycle`, repository Markdown은 반드시 `CommandCenterCycleRecord`라 부른다.

## 4. Ownership table

| Operation | Exact owner | Other actors |
|---|---|---|
| CycleCandidate 작성 | Agent/Human/executor/System component | 누구나 proposal 가능 |
| Cycle eligibility 평가 | P1-8 System | caller prose 사용 금지 |
| CycleAdmissionDecision 발행 | P1-8 System | Human acceptance의 대체가 아님 |
| HumanResult 발행 | Human via P1-7 | P1-8은 참조만 |
| Judgment 발행 | P1-7 Judgment authority | P1-8은 참조만 |
| WorkflowState 변경 | P1-4 TransitionDecision | P1-8 객체는 mutation 금지 |
| MemoryDeclarationAuthorityPolicy 발행 | P1-8 System `P1_8_MEMORY_DECLARATION_POLICY_AUTHORITY_V1` | caller는 policy 등록/수정 불가 |
| ProjectMemoryEntry 투영 | P1-8 System | AdmittedCycle payload에서만 |
| Memory current applicability 평가/event 발행 | P1-8 System event processor | exact source-owner event 또는 source-attested mutation directive 필요 |
| Memory correction/supersession/revocation semantic authority | source object owner 또는 Task authority의 exact structured directive | caller intent는 authority가 아님 |
| NextActionProposal 작성 | Agent/Human/System component | 비권위 |
| NextActionEligibilityPolicy / Descriptor 발행 | P1-8 System `P1_8_NEXT_ACTION_ELIGIBILITY_POLICY_AUTHORITY_V1` | exact enrolled source ref 필요 |
| NextActionSelectionPolicy 발행 | P1-8 System `P1_8_NEXT_ACTION_SELECTION_POLICY_AUTHORITY_V1` | ranking policy이며 action enrollment 불가 |
| NextActionEvaluation / Selection | **P1-8 System** | V1의 유일한 selection owner |
| TaskIssuanceCandidate 생성 | P1-8 System | non-authoritative handoff only |
| TaskContract 발행/수정 | external Command Center / Task authority | P1-8 V1에는 runtime Task issuer가 없음 |
| CommandCenterCycleRecord 작성/검토 | Command Center governance / Human | runtime 객체를 수동으로 mint할 수 없음 |
| Design acceptance | Human | 현재 `HUMAN_PENDING` |

## 5. Mandatory non-substitution rules

다음 문장은 normative다.

> `Command Center Cycle Record != runtime admitted Cycle`

> `CommandCenterCycleRecord != AdmittedCycle`

> `Command Center Cycle Record != runtime Cycle authority`

> `CycleCandidate != CycleAdmissionDecision != AdmittedCycle`

> `raw session != Agent summary != ProjectMemoryEntry`

> `raw session/chat != ProjectMemoryEntry`

> `raw session != AdmittedCycle`

> `Agent summary != ProjectMemoryEntry`

> `Agent output != ProjectMemory`

> `HumanResult != Judgment != TransitionDecision`

> `Judgment != CycleAdmissionDecision`

> `TransitionDecision != CycleAdmissionDecision`

> `WorkflowState != CycleAdmissionDecision`

> `AdmittedCycle != ProjectMemoryView`

> `AdmittedCycle != current ProjectMemoryView`

> `ProjectMemoryEntry != TaskContract`

> `ProjectMemoryEntry != canonical rule/policy authority`

> `MemoryRetrievalResult != AdmittedEvidence`

> `MemoryRetrievalResult != Judgment`

> `memory retrieval != evidence`

> `memory retrieval != Judgment`

> `NextActionProposal != NextActionEvaluation != NextActionSelection != TransitionDecision`

> `NextActionProposal != NextActionSelection`

> `NextActionSelection != WorkflowState`

> `NextActionSelection != TransitionDecision`

> `historically admitted != currently applicable`

> `historical memory validity != current memory applicability`

> `historically valid P1-6 source != currently effective P1-6 source`

> `historical source validity != current source effectiveness != current memory applicability`

> `historical policy issuance validity != current policy applicability`

> `historical NextAction policy/descriptor validity != current enrollment eligibility`

> `project memory != canonical rule != TaskContract authority`

> `G_EVIDENCE != G_HUMAN_* != G_JUDGMENT_*`

> `SecurityAdmissionDecision != TransitionDecision`

> `accepted Cycle source != authority for arbitrary caller-authored memory payload`

> `ProjectMemoryEntryId != MemoryLineageKey`

> `CycleCandidate correction intent != correction authority`

> `CycleCandidate supersession intent != supersession authority`

> `CycleCandidate revocation intent != revocation authority`

> `deterministic ranking != action authority`

> `NextActionProposal != NextActionDescriptor`

> `NextActionSelection != TaskContract`

> `TaskIssuanceCandidate != TaskContract`

따라서:

- raw chat/session transcript, Agent summary, executor report prose, commit message, Markdown Cycle만으로는 `AdmittedCycle` 또는 `ProjectMemoryEntry`를 생성할 수 없다.
- memory 내용은 canonical rule이나 TaskContract를 자동 생성, 수정, supersede, revoke, reinterpret할 수 없다.
- canonical rule/TaskContract 변경은 그 authority가 소유한 별도 human-governed issuance 절차를 거쳐야 한다. Memory는 그 절차의 입력 provenance일 수만 있다.
- P1-8 System admission은 Human acceptance를 사칭하지 않는다. Admission prerequisite인 P1-7 `Judgment(kind=ACCEPTED)`를 exact ref로 소비한다.

## 6. Runtime AdmittedCycle vs CommandCenterCycleRecord

| Dimension | `AdmittedCycle` | `CommandCenterCycleRecord` |
|---|---|---|
| Form | runtime immutable row/aggregate | tracked repository Markdown |
| Owner | P1-8 System admission authority | Command Center governance |
| Accepted-only | Yes | No |
| Creation basis | strict structured eligibility + immutable refs | workflow/public provenance documentation |
| Machine authority | project-memory source authority | none for runtime admission |
| Can include rejected/HOLD/failed | No | Yes |
| Correction | append-only authority event and successor | append-only Markdown correction/supersession convention |
| Primary use | deterministic memory and selection input | Human review, audit, handoff, repository history |

A `CommandCenterCycleRecord` may reference zero or one `AdmittedCycle`. A runtime `AdmittedCycle` may later be projected into a `CommandCenterCycleRecord`. Neither direction is automatic authority conversion. A Markdown file hash is an audit pointer, not admission proof.

## 7. Cycle admission eligibility

### 7.1 Strict V1 rule

V1에서 `AdmittedCycle`은 다음 조건을 모두 만족할 때만 생성한다.

1. TaskContract ID/version과 project scope가 존재하고 exact하게 일치한다.
2. WorkRun ID가 존재하며 current durable state가 `WorkflowState.ACCEPTED`다.
3. exact P1-7 Judgment가 존재하며 `JudgmentKind.ACCEPTED`다.
4. Judgment의 project/task/work-run/source-state/version/authority-revision binding이 admission candidate와 일치한다.
5. exact P1-4 terminal `TransitionDecision`의 resulting state가 `ACCEPTED`이고 resulting state version이 candidate와 일치한다.
6. terminal TransitionDecision이 같은 Judgment ref를 guard input/provenance로 사용하며, Judgment source snapshot과 TransitionDecision source snapshot의 predecessor contract가 일치한다.
7. required evidence가 있는 Task라면 P1-6 attestation/root refs가 Judgment와 terminal decision이 소비한 exact refs와 일치한다.
8. predecessor refs가 존재하고 fingerprint/hash/authority revision 검증을 통과한다.
9. structured payload, memory declarations, privacy/export policy, correction graph가 schema와 policy를 통과한다.
10. terminal epoch uniqueness와 idempotency constraints를 통과한다.

P1-8은 evidence나 Judgment를 새로 판정하지 않는다. 위 검사는 predecessor가 발행한 immutable objects가 서로 exact하게 결합되어 있는지 확인하는 reference-integrity/eligibility 검사다.

`STRUCTURED_RESULT_ATTESTED` declaration이 있으면 조건 7~8은 section 9.2의
`HistoricalStructuredResultAuthorityV1` 검증을 포함한다. Exact source ref는 accepted terminal lineage가
소비한 attestation의 ordered admitted-evidence refs/coverage/root에 속해야 하고 terminal consumption
snapshot에서 valid해야 한다. Cycle admission/replay 시점의 current P1-6 effectiveness는 이 조건이
아니며, terminal 이후의 stale/revoked/superseded/expired 상태는 section 11의 current applicability로
별도 처리한다.

### 7.2 Excluded outcomes

다음은 reusable curated memory admission에 부적격이다.

| Source outcome | Runtime AdmittedCycle | Reusable ProjectMemoryEntry | Required provenance home |
|---|---:|---:|---|
| Judgment `REJECTED` / state `REJECTED` | No | No | P1-4/P1-6/P1-7 histories + optional CommandCenterCycleRecord |
| Judgment `HOLD_REWORK_REQUIRED` / state `REWORK_REQUIRED` | No | No | same |
| `FAILED` | No | No | P1-4 failure/event history + optional CommandCenterCycleRecord |
| `BLOCKED` | No | No | current WorkRun/blocker provenance + optional CommandCenterCycleRecord |
| non-terminal/rework in progress | No | No | source domain histories |
| raw abandoned session | No | No | operational retention only, if policy permits |

이 제외는 provenance 삭제가 아니다. Rejected/HOLD/failed/rework 사실은 원 소유 domain과 `CommandCenterCycleRecord`에 보존되며 Next Action의 recovery priority input으로 사용할 수 있다. 다만 reusable curated memory로 복사하거나 semantic authority를 부여하지 않는다.

후속의 별도 WorkRun이 accepted되면 그 accepted terminal epoch만 새 AdmittedCycle을 만들 수 있다. 그 Cycle은 이전 실패/HOLD refs를 `BLOCKER_RESOLUTION` 또는 `PROVENANCE_POINTER`로 가리킬 수 있으나, 실패/HOLD payload 자체를 accepted memory로 승격하지 않는다.

## 8. Cycle identity and authoritative payload

### 8.1 Identity

- `cycle_id`: globally unique immutable ID.
- `terminal_epoch_key`:
  `(project_id, task_contract_id, task_contract_version, work_run_id, terminal_transition_decision_ref, resulting_state_version)`
- 한 terminal epoch에는 current admission lineage 하나만 허용한다.
- correction successor는 새 `cycle_id`를 사용하고 `supersedes_cycle_id`로 이전 Cycle을 가리킨다.

### 8.2 Candidate fingerprint

`cycle_candidate_fingerprint`는 RFC 8785에 준하는 canonical JSON 또는 구현 시 고정할 동등한 canonical serializer의 UTF-8 bytes에 대한 SHA-256이다. 다음 authoritative fields를 포함한다.

- schema/version, project ID
- TaskContract ID/version/ref/hash
- WorkRun ID와 accepted resulting state/version
- terminal TransitionRequest/Evaluation/Decision refs와 fingerprints
- Judgment ref/fingerprint/authority revision
- HumanResult refs when Judgment requires them
- evidence attestation/root/admitted-evidence refs and revisions when required
- structured result classification and artifact/commit/run refs
- ordered typed MemoryDeclarations
- exact MemoryDeclarationAuthorityPolicy refs/fingerprints
- resolved source-to-content authority refs/fingerprints
- verified MemoryLineageKeys
- owner-authorized correction/supersession/revocation source refs when applicable
- privacy/export classification
- selection-relevant structured facts explicitly allowed by schema

The fingerprint binds the exact immutable P1-6 issuance graph and the exact accepted terminal
consumption refs described in section 9.2. It excludes current P1-6 effectiveness, later source-owner
event sequence, current ProjectMemory applicability state/revision, and applicability observation
time. Those current facts are projected separately and cannot change historical Cycle identity.

The exact `MemoryDeclarationAuthorityPolicy` ref/version/fingerprint admitted with the Cycle is an
immutable historical identity field. Later-current policy tip ref/revision, later policy-owner event sequence,
and whether that historical policy is current now are excluded. New admission eligibility checks those
current facts before identity construction; replay verifies the stored historical policy version instead.

Normative exclusion:

- current MemoryDeclarationAuthorityPolicy revision/current-tip ref
- policy supersession/revocation event sequence after original admission
- current source-enrollment membership and current policy applicability result

must not appear in `cycle_candidate_fingerprint`, `AdmittedCycle` payload fingerprint,
`ProjectMemoryEntry` content fingerprint, `MCF_V1` or `ProjectMemoryEntryId`. The original exact policy
ref/version/fingerprint remains in historical identity.

다음은 fingerprint와 semantic authority에서 제외한다.

- server timestamps, database sequence, retry count
- free-form display summary
- raw Agent/session text
- executor self-asserted acceptance
- caller correction/supersession/revocation intent without an accepted authority source
- local filesystem path만 있는 unverifiable pointers

### 8.3 AdmittedCycle payload

AdmittedCycle은 candidate의 verified authoritative payload, CycleAdmissionDecision ref, admission sequence, server-issued timestamp, immutable source refs, declaration-policy refs, derived-content fingerprints, lineage keys, payload fingerprint를 보존한다. Caller가 제출한 memory content는 equality 검사용 claim일 뿐 admitted payload source가 아니다. Human-readable `display_summary`는 선택적으로 저장할 수 있지만 `NON_AUTHORITATIVE`로 표시하고 retrieval ranking, admission, selection decision에 사용하지 않는다.

## 9. Project memory taxonomy

### 9.1 MemoryDeclarationAuthorityPolicy

`MemoryDeclarationAuthorityPolicy`는 `P1_8_MEMORY_DECLARATION_POLICY_AUTHORITY_V1`가 발행한다. Caller, Agent, executor, CycleCandidate는 policy를 mint/register/modify할 수 없다. Category마다 current unsuperseded eligible policy 하나만 허용한다. **New Cycle admission**은 그 current policy의 exact ID/version/fingerprint와 current valid source enrollment를 요구하며 unknown, revoked, superseded 또는 stale policy는 `MEMORY_POLICY_CURRENTLY_INELIGIBLE`로 fail closed한다.

각 immutable policy는 다음을 고정한다.

- policy ID/version/fingerprint와 authority ID/version/revision
- category와 exact authority mode
- allowed source object kinds와 source schema/version
- exact source field paths/object refs
- content derivation schema/version과 canonicalization algorithm
- subject, applicability, semantic-slot derivation
- privacy ceiling과 export allowlist
- issued-at/issuance sequence, revoked/superseded owner-event refs와 effective sequences
- `supersession_current_use_disposition = PRESERVE_EXISTING | WITHDRAW_CURRENT`; revocation은 항상 `WITHDRAW_CURRENT`
- category-specific failure code

#### 9.1.1 Historical policy authority and replay

Existing AdmittedCycle replay는 current policy lookup을 admission criterion으로 사용하지 않는다. 대신
다음 immutable tuple인 `HistoricalMemoryPolicyAuthorityV1`을 검증한다.

- stored exact policy ref, policy ID/version/fingerprint
- canonical immutable policy payload와 recomputed fingerprint
- policy authority ID/version/revision과 issuer authenticity
- policy issued-at/issuance sequence, supersedes/revocation event refs/effective sequences
- original CycleEvaluation/CycleAdmissionDecision ref, admission sequence/timestamp, admitted payload fingerprint
- policy가 original admission sequence/timestamp에서 current unsuperseded eligible이었고 exact source
  enrollment가 당시 valid했다는 as-of owner-event proof
- AdmittedCycle과 ordered MemoryDeclarations가 저장한 exact policy ref/fingerprint equality

Historical verifier는 original admission high-watermark까지만 policy owner events를 fold한다. 그 시점보다
뒤의 policy supersession/revocation/current catalog revision은 historical validity에 넣지 않는다. 따라서
policy v1로 valid하게 admitted된 Cycle은 v2가 current가 된 뒤에도 같은 immutable Cycle/entry identity로
replay한다. 반대로 v1이 original admission 전에 이미 revoked/superseded였거나 immutable payload,
fingerprint, authority revision 또는 original source enrollment graph가 불완전/불일치하면
`MEMORY_POLICY_HISTORICAL_PROVENANCE_INVALID`이며 current policy repair로 소급 복구할 수 없다.

Later policy-owner event가 historical entry의 current use를 withdraw해야 하면 event processor는 invalidated
policy의 immutable disposition과 exact owner event를 참조한 `ProjectMemoryAuthorityEvent`를 append한다.
`WITHDRAW_CURRENT`는 current ProjectMemoryView만 non-`CURRENT`로 만들며 AdmittedCycle,
ProjectMemoryEntry, `MCF_V1`, entry ID 또는 historical policy binding을 rewrite하지 않는다.

Authority mode enum:

- `DETERMINISTIC_POINTER`: immutable source fields의 allowlisted canonical projection만 content다. Caller description은 포함하지 않는다.
- `STRUCTURED_RESULT_ATTESTED`: exact content가 TaskContract-authorized structured result artifact의 exact field/object로 이미 존재해야 한다.
- `OWNER_ATTESTED`: defined owner가 exact content/fingerprint를 immutable attestation으로 발행한 경우만 허용한다.
- `NOT_SUPPORTED`: V1 admission 불가.

`OWNER_ATTESTED`는 contract shape를 보존하지만 V1 category binding은 `0`개다. 현재 predecessor에는 generic lesson/context semantic owner가 없으므로 P1-7 Human/Judgment authority를 확장하거나 사칭하지 않는다. 향후 사용은 별도 Human-accepted P1-8 policy revision이 필요하다.

### 9.2 Common source-to-content verification

`MCF_V1` content fingerprint는 다음 canonical JSON의 UTF-8 bytes에 대한 SHA-256이다.

`{fingerprint_schema:"p1-8-memory-content-v1", category, authority_mode, policy_ref, normalized_derived_content}`

`STRUCTURED_RESULT_ATTESTED` source는 exact tuple을 모두 요구한다.

- TaskContract ID/version
- P1-6 `EvidenceRequirement` ref/version/fingerprint와 result schema ID/version
- P1-6 `EvidenceCheckpoint` ref/version/fingerprint
- `EvidenceSetSatisfactionAttestation` ref/version, set-evaluation ref/version, full RequirementSet
  root, checkpoint-subset root, ordered admitted-evidence refs/coverage, admitted-ref root,
  historical P1-6 authority ID/version/revision, issued-at
- `AdmittedEvidence` ref/version과 그 candidate/request/evaluation/`ADMITTED` decision, issuer,
  producer, requirement/set/checkpoint, admission timestamp를 포함한 complete historical issuance provenance
- `EvidenceContentRef` object ID/version, owner/store authority, canonicalization, schema ID/version,
  byte count, content hash
- structured field path 또는 object ref
- field/object canonical bytes와 `MCF_V1` expected fingerprint
- same TaskContract/WorkRun/checkpoint/source WorkflowState/state_version binding
- exact accepted Judgment ref/version과 terminal TransitionDecision ref/version/resulting state_version,
  그리고 둘이 소비한 exact evidence-attestation/root binding

이 tuple을 `HistoricalStructuredResultAuthorityV1`이라 한다. Evaluator는 accepted P1-6 runtime의
`verify_historical_set_attestation_provenance`와 동등한 projection-independent verification으로
immutable checkpoint/RequirementSet/Requirement/evaluation/attestation/admission/content graph 전체를
재계산한다. 이 검사는 P1-6 current-effectiveness projection, current RequirementSet, current evidence
authority revision, current WorkRun state/version, 현재의 non-revocation 또는 freshness를 요구하지 않는다.

Historical terminal validity는 다음을 모두 만족할 때만 성립한다.

1. attestation과 complete issuance graph가 exact terminal epoch에서 canonical하고 `SATISFIED` /
   `ADMITTED`였음이 immutable provenance로 검증된다.
2. declaration의 `AdmittedEvidenceRef`가 attestation의 ordered admitted-evidence refs에 실제로
   포함되고 exact requirement result/coverage와 admitted-ref root에 커밋되어 있다.
3. evidence가 terminal acceptance에 required였으면 그 exact attestation ref/root가 accepted
   Judgment와 terminal TransitionDecision이 소비한 evidence binding과 byte-exact하게 일치한다.
4. source-owner invalidation event가 terminal consumption snapshot 이전 또는 그 snapshot에 이미
   유효했다면 historical validity는 실패한다. terminal snapshot 뒤의 event는 current effectiveness만
   바꾸며 이 historical validity를 바꾸지 않는다.

같은 WorkRun의 다른 valid evidence, 같은 bytes, 현재 effective evidence, 또는 unrelated attestation은
대체할 수 없다. V1에서 terminal acceptance에 optional이어서 exact consumed attestation/root에
포함되지 않은 structured result는 `STRUCTURED_RESULT_ATTESTED` memory source로 `NOT_SUPPORTED`이다.
그 source를 허용하려면 TaskContract가 별도 applicable EvidenceRequirement/checkpoint authority로
미리 enroll하고 accepted terminal lineage가 그 exact attestation/root를 소비해야 한다. P1-8이나
caller가 사후에 optional source authority를 만들 수 없다.

Caller는 source locator와 claimed content/fingerprint를 제출할 수 있지만 content를 rewrite할 수 없다. Evaluator가 source bytes/fields에서 expected content를 재구성하고 ProjectMemoryEntry에는 expected content만 투영한다.

### 9.3 Exact V1 category contract

| Category | Authority mode | Allowed source object kinds | Exact content derivation/binding | Scope/applicability and semantic slot | Privacy ceiling | Failure |
|---|---|---|---|---|---|---|
| `DECISION` | `STRUCTURED_RESULT_ATTESTED` | `P1_6_ADMITTED_STRUCTURED_RESULT` whose Requirement schema is enrolled by policy | exact result object at policy-fixed field path; `MCF_V1` equality; accepted Cycle lineage required | source TaskContract scope; slot `decision/{result_schema_id}/{policy_decision_slot_id}` | `PRIVATE_INTERNAL` | missing → `MEMORY_DECLARATION_AUTHORITY_NOT_FOUND`; mismatch → `MEMORY_DECLARATION_SOURCE_MISMATCH` |
| `INVARIANT_POINTER` | `DETERMINISTIC_POINTER` | enrolled canonical authority ref/hash/anchor | exact tuple `{authority_id, authority_ref, authority_fingerprint, anchor_id}` only; invariant prose forbidden | policy-derived project/domain applicability; slot `invariant/{authority_id}/{anchor_id}` | `PUBLIC_SANITIZED` only when source is public, otherwise `PRIVATE_INTERNAL` | missing/mismatch as above |
| `CONSTRAINT_POINTER` | `DETERMINISTIC_POINTER` | enrolled TaskContract constraint ref/fingerprint or canonical rule constraint ref/hash/anchor | exact tuple `{constraint_owner, logical_constraint_id, authority_ref, authority_fingerprint}` only | source logical scope; slot `constraint/{constraint_owner}/{logical_constraint_id}` | `PRIVATE_INTERNAL` | missing/mismatch as above |
| `LESSON` | `NOT_SUPPORTED` | none | no semantic inference or caller-authored lesson | none | none | `MEMORY_DECLARATION_MODE_NOT_SUPPORTED` |
| `BLOCKER_RESOLUTION` | `DETERMINISTIC_POINTER` | exact P1-4 blocker provenance ref plus accepted resolution Cycle/TransitionDecision refs | exact relation tuple `{blocker_owner, blocker_id, blocker_ref, resolution_cycle_id, accepted_transition_ref}`; narrative forbidden | blocker logical scope; slot `blocker-resolution/{blocker_owner}/{blocker_id}` | `PRIVATE_INTERNAL` | missing/mismatch as above |
| `PROVENANCE_POINTER` | `DETERMINISTIC_POINTER` | allowlisted immutable refs already verified in AdmittedCycle | exact tuple `{provenance_role, source_object_kind, source_logical_id, source_ref, source_fingerprint}` | source scope; slot `provenance/{role}/{kind}/{logical_id}` | `PUBLIC_SANITIZED` only when every source allows export, otherwise `PRIVATE_INTERNAL` | missing/mismatch as above |
| `NEXT_ACTION_CONTEXT` | `STRUCTURED_RESULT_ATTESTED` | `P1_6_ADMITTED_STRUCTURED_RESULT` at a policy-enrolled context field, or exact enrolled descriptor context object | exact policy-fixed context object; no rationale/free text; `MCF_V1` equality | source Task/project scope; slot `next-action-context/{context_schema_id}/{policy_context_slot_id}` | `PRIVATE_INTERNAL` | missing/mismatch as above |

`DECISION`과 P1-6 structured-result 기반 `NEXT_ACTION_CONTEXT`의
`P1_6_ADMITTED_STRUCTURED_RESULT`는 section 9.2의 `HistoricalStructuredResultAuthorityV1`을
만족하는 exact historical source만 뜻한다. 현재 effective하다는 사실만으로는 부족하고,
terminal 당시 consumed attestation/root에 속하지 않는 source는 허용하지 않는다. Enrolled descriptor
context object 경로는 기존 policy-enrolled exact descriptor-object binding을 그대로 사용하며 P1-6
historical authority 규칙이 그 기존 mode/source authority를 재설계하거나 대체하지 않는다.

`PUBLIC_SANITIZED`는 visibility maximum일 뿐 자동 export permission이 아니다. Source privacy와 policy ceiling 중 더 제한적인 분류를 사용한다.

카테고리, policy ref/fingerprint, source locator, project scope, subject key source, claimed fingerprint, privacy class가 없는 declaration은 reject한다. 자유 형식 summary에서 category/content/source/semantic slot을 추론하는 기능은 V1에서 금지한다.

## 10. Memory admission and deterministic projection

### 10.1 One admission boundary

ProjectMemoryEntry는 별도의 semantic admission 결과가 아니다. `CycleEvaluation`이 MemoryDeclarations를 함께 검증하고, `CycleAdmissionDecision(ADMITTED)`이 성공한 동일 transaction에서 deterministic projection으로 생성한다.

따라서:

`MemoryDeclaration -> CycleEvaluation -> CycleAdmissionDecision -> AdmittedCycle -> ProjectMemoryEntry`

이 경로 외의 direct insert/upsert/import는 금지한다.

### 10.2 CycleEvaluation source reconstruction

New Cycle admission의 모든 MemoryDeclaration에 대해 CycleEvaluation은 다음 순서를 실행한다.

1. exact current unsuperseded eligible MemoryDeclarationAuthorityPolicy를 ID/version/fingerprint로
   resolve하고 current valid source enrollment를 확인한다.
2. 그 current policy가 허용한 exact immutable source object를 resolve한다.
3. `STRUCTURED_RESULT_ATTESTED`이면 section 9.2의 projection-independent historical verifier로
   exact terminal-epoch issuance graph와 consumed attestation/root membership를 먼저 검증한다.
   current effectiveness lookup은 이 historical proof를 대신하지 않는다.
4. policy derivation schema로 expected content, subject, applicability, semantic slot을 재구성한다.
5. `MCF_V1(expected content)`를 계산한다.
6. expected content/fingerprint와 declaration claim이 byte-exact 일치하는지 확인한다.
7. privacy ceiling과 Cycle Task/WorkRun/Judgment/TransitionDecision bindings를 확인한다.
8. historical identity 결정과 분리하여 source-owner events를 admission observation high-watermark까지
   fold하고 current source effectiveness 및 initial ProjectMemory applicability를 계산한다.
9. MemoryLineageKey와 current tip/revision을 확인한다.
10. 필요한 correction/supersession/revocation authority source를 별도로 확인한다.

Existing AdmittedCycle historical replay는 다음 순서를 사용한다.

1. stored CycleAdmissionDecision/AdmittedCycle payload에서 original exact policy ref/version/fingerprint와
   original admission sequence/timestamp를 읽는다.
2. section 9.1.1 `HistoricalMemoryPolicyAuthorityV1`로 immutable policy payload/authority와 original
   admission 당시 validity/source enrollment를 검증한다.
3. 그 historical policy version과 stored historical source provenance에서 expected content,
   `MCF_V1`, MemoryLineageKey, ProjectMemoryEntryId를 다시 계산해 stored objects와 비교한다.
4. same immutable request/cycle/payload/policy fingerprint이면 동일 CycleAdmissionDecision,
   AdmittedCycle, ProjectMemoryEntry IDs/content를 반환한다.
5. current policy catalog/events는 historical identity를 결정한 뒤 current applicability projection을
   별도로 reconstruct할 때만 읽으며 current-view publication 전에 fold한다.

Replay는 original policy가 지금 current인지, v2가 v1을 supersede했는지, current source enrollment가
v1을 아직 포함하는지를 historical identity criterion으로 요구하지 않는다.

하나라도 실패하면 전체 CycleAdmissionDecision은 `REJECTED`이며 partial ProjectMemoryEntry projection은 없다.

- source authority 없음: `MEMORY_DECLARATION_AUTHORITY_NOT_FOUND`
- new admission policy/source enrollment가 current eligible하지 않음: `MEMORY_POLICY_CURRENTLY_INELIGIBLE`
- historical policy payload/authority/as-of-admission validity 불일치:
  `MEMORY_POLICY_HISTORICAL_PROVENANCE_INVALID`
- derived/attested content mismatch: `MEMORY_DECLARATION_SOURCE_MISMATCH`
- unsupported mode/category/inference: `MEMORY_DECLARATION_MODE_NOT_SUPPORTED`
- invalid/incomplete historical issuance graph or terminal-root membership:
  `CYCLE_HISTORICAL_SOURCE_PROVENANCE_INVALID`
- currentness를 historical authority로 제시한 경우: `CYCLE_SOURCE_CURRENTNESS_NOT_AUTHORITY`

### 10.3 ProjectMemoryEntryId and stable MemoryLineageKey

Normative:

`ProjectMemoryEntryId != MemoryLineageKey`

`ProjectMemoryEntryId`는 한 projection의 immutable identity다.

`entry_id = sha256(canonical-json-v1({cycle_id, memory_declaration_ordinal, policy_fingerprint, memory_lineage_key, content_fingerprint}))`

`MemoryLineageKey`는 cross-Cycle stable semantic identity다.

`MemoryLineageKeyV1 = sha256(canonical-json-v1({lineage_key_schema:"p1-8-memory-lineage-v1", project_id, category, subject_key, applicability_key, semantic_slot}))`

Constraints:

- `cycle_id`와 `content_fingerprint`를 포함하지 않는다.
- policy/source가 derive한 key atoms만 사용하고 caller-supplied free text는 사용하지 않는다.
- `subject_key`는 stable logical owner/object ID다.
- `applicability_key`는 `{scope_kind, stable_scope_id, applicability_policy_id}`이며 source version은 entry provenance에만 둔다.
- `semantic_slot`은 section 9 category table의 exact policy slot shape를 사용한다.
- key atom은 UTF-8 NFC, ASCII-safe ID grammar `[a-z0-9][a-z0-9._:/@-]{0,159}`, no trim/coercion으로 normalize한다. 위반은 reject한다.
- same subject/category라도 semantic slot이 다르면 다른 lineage다.

동일 admitted payload replay는 동일 entry IDs를 반환한다. 동일 lineage의 current tip과 same content fingerprint를 새 Cycle이 재사용하면 새 entry를 만들지 않고 `CycleMemoryReference`만 생성한다. Different content는 valid explicit supersession authority가 없으면 `MEMORY_SUPERSESSION_AUTHORITY_REQUIRED`로 reject한다.

### 10.4 Authority ceiling

ProjectMemoryEntry가 보유하는 authority는 “이 typed content가 이 accepted Cycle에서 admitted되었다”는 provenance까지다. 그 content가:

- 현재 canonical policy인지,
- 다른 Task에 mandatory한지,
- TaskContract를 override하는지,
- 새 evidence/Judgment인지

를 의미하지 않는다. Retrieval consumer는 canonical authority와 충돌하면 canonical authority를 우선하고 memory conflict를 typed stale/corrupt input으로 처리한다.

## 11. Historical admission and current applicability

Historical admission은 immutable fact다. Current applicability는 시간에 따라 변하는 projection이다.

### 11.1 Normative three-way authority separation

| Dimension | Mutable/current? | Exact authority and effect |
|---|---:|---|
| historical source issuance/provenance | immutable historical | P1-4/P1-6/P1-7/canonical source owner의 exact terminal-epoch objects, refs, roots, fingerprints, issuance authority revision |
| historical MemoryDeclaration policy issuance/validity | immutable historical | P1-8 policy owner의 exact policy ref/version/fingerprint/payload/authority revision과 original Cycle admission as-of validity |
| `AdmittedCycle` identity/content | immutable historical | P1-8 Cycle admission over exact verified predecessor provenance; later currentness는 identity input이 아님 |
| `ProjectMemoryEntry` identity/content | immutable historical | admitted Cycle에서 deterministic P1-8 projection; applicability event로 content를 rewrite하지 않음 |
| current source effectiveness | current, owner-event-derived | source owner의 append-only revocation/supersession/correction/freshness/state-version semantics; historical issuance를 삭제하지 않음 |
| current MemoryDeclaration policy applicability | current, policy-owner-event-derived | new admission eligibility와 policy-contract-required memory withdrawal만 제어; historical Cycle replay identity를 바꾸지 않음 |
| current ProjectMemory applicability | current rebuildable projection | P1-8가 exact source-owner authority events와 P1-8 applicability events를 fold한 결과; retrieval/selection eligibility만 제어 |

Normative:

`historical source provenance != current source effectiveness != current ProjectMemory applicability`

`historical policy issuance validity != current policy applicability`

Historical source provenance의 identity snapshot에는 source object refs/fingerprints, historical P1-6
authority revision, checkpoint/source state/version, exact Judgment/TransitionDecision refs, content
schema/canonicalization/hash가 들어간다. Current observation에는 source-owner authority-event
high-watermark/revision, memory-lineage applicability revision, observed-at/admitted-at이 들어간다.
Current observation fields와 current policy ref/revision/event sequence는 Cycle candidate/payload,
`MCF_V1`, `ProjectMemoryEntryId` 또는 immutable entry content fingerprint에 들어가지 않는다. Original
admission의 exact historical policy ref/version/fingerprint는 immutable identity에 남는다.

### 11.2 Terminal-time validity and later currentness

- source가 exact terminal consumption snapshot에서 valid하고 그 consumed attestation/root에 속하면
  historical Cycle source로 valid하다.
- source-owner revocation/supersession/correction/expiry가 terminal consumption snapshot 이전 또는
  그 snapshot에서 이미 effective했다면 Cycle은 `CYCLE_HISTORICAL_SOURCE_PROVENANCE_INVALID`로
  reject하고 ProjectMemoryEntry를 만들지 않는다. 이후의 current repair는 그 terminal epoch를
  소급하여 valid하게 만들 수 없다.
- source가 terminal 당시 valid했지만 이후 `REVOKED`, `SUPERSEDED`, `CORRECTED` 또는 `EXPIRED`가
  되면 AdmittedCycle과 ProjectMemoryEntry identity/content는 유지한다. 다만 current applicability는
  exact owner event/policy에 따라 non-`CURRENT`이며 default retrieval과 NextAction context에서 제외한다.

### 11.3 Delayed admission and initial publication order

Delayed admission도 하나의 transaction에서 다음 순서를 고정한다.

1. immutable historical Cycle/source provenance와 exact terminal-root membership를 검증한다.
2. same request/cycle fingerprint replay를 해석하고, 신규이면 immutable CycleAdmissionDecision,
   AdmittedCycle, ProjectMemoryEntry를 생성한다.
3. transaction이 획득한 source-owner event high-watermark까지 모든 applicable authority event를 fold한다.
4. 그 결과에 맞는 initial `ProjectMemoryAuthorityEvent`와 lineage applicability revision을 기록한다.
5. current projection을 같은 transaction에서 `CURRENT`, `SUPERSEDED`, `REVOKED` 또는 `EXPIRED`로
   publish한다.

Source가 admission 전에 이미 non-current이면 entry는 historical object로 생성되지만 step 5까지
외부에 보이지 않으며, transaction commit 후에도 `CURRENT`로 한 순간도 노출되지 않는다. Historical
verification 실패 시 전체 transaction은 reject/rollback되어 AdmittedCycle과 partial entry가 없다.

각 ProjectMemoryEntry는 logically 다음 상태 중 하나를 갖는다.

- `CURRENT`: 현재 scope에서 deterministic retrieval/selection input으로 사용 가능.
- `SUPERSEDED`: exact same MemoryLineageKey의 accepted successor entry가 validated explicit supersession authority로 current tip을 대체. historical query에는 남음.
- `REVOKED`: source corruption/invalidation 또는 policy-owned revocation 때문에 현재 사용 금지. historical query에는 이유와 함께 남음.
- `EXPIRED`: TaskContract가 명시한 time/version applicability가 종료. historical admission은 유지.

V1 cardinality는 exact하게 다음과 같다.

- 각 `MemoryLineageKey`마다 `CURRENT` tip은 최대 `1`개다.
- current-use가 revoked/expired되면 `0`개가 허용된다.
- multi-current per lineage는 모든 category에서 금지한다.
- same category/subject라도 different semantic slot은 different MemoryLineageKey이므로 각각 current tip 하나를 가질 수 있다.
- rebuildable current projection은 unique key `(memory_lineage_key) WHERE state = CURRENT`와 expected lineage revision으로 이 cardinality를 강제한다.

Current 상태는 row overwrite가 아니라 `ProjectMemoryAuthorityEvent`를 fold하여 계산한다. Projection table/cache가 손실되어도 immutable entries/events에서 재구성 가능해야 한다.

Retrieval default는 `CURRENT`만 반환한다. Historical mode는 explicit caller authorization과 query flag가 있어야 하며, 각 result에 historical state, reason, event ref를 붙인다.

## 12. Correction, supersession, revocation

### 12.1 Append-only rule

AdmittedCycle, CycleAdmissionDecision, ProjectMemoryEntry, NextActionSelection은 update/delete로 수정하지 않는다.

- `CORRECTION`: 동일 historical event의 payload/provenance 오류를 새 object로 바로잡는다.
- `SUPERSESSION`: 이후 accepted fact/decision이 이전 current applicability를 대체한다.
- `REVOCATION`: source invalidation/corruption으로 current use를 금지하며 replacement가 없을 수 있다.

각 event는 owner, reason code, source authority refs, expected current revision, predecessor ID, successor ID(있을 때), timestamp, event sequence를 포함한다.

### 12.2 Exact V1 supersession and mutation authority

V1 supersession rule은 `EXPLICIT_SUPERSESSION_ONLY`다.

- later Cycle, same category, same subject 또는 same lineage key만으로 auto-supersede하지 않는다.
- different content가 current lineage에 진입하려면 exact mutation authority가 필요하다.
- Caller의 `supersedes`, `corrects`, `revokes` fields는 claim/audit input일 뿐 authority가 아니다.
- `CycleCandidate correction intent != correction authority`.

Accepted authority source kinds:

1. `SOURCE_OWNER_AUTHORITY_EVENT`  
   P1-4/P1-6/P1-7 또는 canonical source owner가 실제 소유 object에 대해 발행한 immutable correction/supersession/revocation event. Event ID/version/fingerprint, owner authority ID/version/revision, affected source ref/fingerprint, replacement source ref/fingerprint(있을 때), event sequence가 exact해야 한다.
2. `TASK_AUTHORITY_STRUCTURED_MEMORY_DIRECTIVE`  
   TaskContract-authorized structured result artifact 안의 exact mutation directive. `STRUCTURED_RESULT_ATTESTED` 검증을 통과한 accepted successor Cycle에서만 사용하며 mutation kind, MemoryLineageKey, expected current entry ID/revision, replacement declaration/content fingerprint, reason code를 exact하게 포함한다.
3. `P1_8_DETERMINISTIC_APPLICABILITY_POLICY`  
   이미 source-attested된 expiry predicate 평가와 same-content replay/CycleMemoryReference 생성에만 사용한다. Different-content correction/supersession/revocation authority는 만들 수 없다.

V1에는 caller-authored generic `OWNER_ATTESTED` mutation object가 없다. 새 Human/P1-7 authority도 만들지 않는다.

Authority priority:

1. current source-owner revocation/corruption event
2. current source-owner correction/supersession event
3. Task-authority structured memory directive
4. P1-8 deterministic expiry/replay policy

Revoked/corrupt source를 lower-priority directive가 되살릴 수 없다. Same priority의 incompatible events 또는 incomparable owner revisions는 `MEMORY_APPLICABILITY_CONFLICT`로 fail closed한다.

Mutation-specific requirements:

- `CORRECTION`: exact predecessor source error와 replacement source/content를 bind한다. Replacement ProjectMemoryEntry는 새 accepted Cycle에서만 생성한다.
- `SUPERSESSION`: exact current tip/revision과 replacement entry/content를 bind한 explicit directive 또는 source-owner replacement event가 필요하다.
- `REVOCATION`: exact current tip/revision과 affected source를 bind하며 successor 없이 current tip을 zero로 만들 수 있다.

### 12.3 ProjectMemoryAuthorityEvent fields

각 event는 최소 다음 immutable fields를 포함한다.

- event ID/version/kind/fingerprint
- project ID와 MemoryLineageKey/schema version
- expected lineage revision
- expected current entry ID/fingerprint
- predecessor entry ID와 successor entry ID(있을 때)
- authority source kind/ref/version/fingerprint/revision
- authority owner ID/version
- affected source refs/fingerprints
- replacement source/content fingerprint(있을 때)
- reason code, issued_at, admitted_at, event sequence

P1-8 System은 이 source authority를 평가해 event를 발행하지만 semantic correction intent의 원 owner가 아니다.

### 12.4 Graph constraints

- self-reference 금지
- cycle 금지
- project/scope crossing 금지
- correction/supersession predecessor는 존재해야 함
- 하나의 current lineage tip만 허용
- stale expected revision은 typed conflict
- correction은 predecessor를 삭제/덮어쓰지 않음

### 12.5 Source invalidation

P1-6/P1-7/P1-4 owner가 source revocation/correction/supersession을 발행하면 P1-8은 그 exact owner-issued event를 참조해 affected Cycle/Memory current applicability를 append-only로 변경한다. P1-8이 predecessor object를 revoke하거나 과거 TransitionDecision을 rewrite하지 않는다.

Event processor는 source-owner event ID/version/fingerprint/revision/effective sequence, affected source
ref/fingerprint, affected memory lineage/entry ref, prior applicability revision을 exact하게 bind한 새
`ProjectMemoryAuthorityEvent`를 append한다. 이 event만 current `ProjectMemoryView`를 변경한다.
Old AdmittedCycle, ProjectMemoryEntry content, `MCF_V1`, entry ID, terminal/source snapshot은 update/delete
하지 않는다. Projection rebuild는 같은 owner-event sequence를 fold하여 같은 as-of applicability를
재현해야 한다.

Source correction이 다른 semantic content를 만들면 old entry를 고치는 대신 새 accepted Cycle과
section 12.2의 valid explicit supersession authority가 필요하다. `EXPLICIT_SUPERSESSION_ONLY`,
`ProjectMemoryEntryId != MemoryLineageKey`, mutation-authority priority는 그대로 유지된다.

### 12.6 Memory policy invalidation

`MemoryDeclarationAuthorityPolicy` owner의 later supersession/revocation은 historical source invalidation과
구별되는 policy event다. New admission은 event fold 후 current policy만 사용할 수 있다. Existing Cycle
replay는 original admission 시점 policy validity를 검증하므로 later event 때문에 실패하지 않는다.

Later event가 invalidated policy의 `supersession_current_use_disposition = WITHDRAW_CURRENT`이거나
revocation이면 다음 append-only chain을 사용한다.

`policy owner event -> ProjectMemoryAuthorityEvent -> current ProjectMemoryView`

Event는 policy ref/version/fingerprint, owner authority revision, effective sequence, affected Cycle/entry
refs와 expected applicability revision을 bind한다. Old AdmittedCycle/ProjectMemoryEntry identity/content와
historical policy ref는 그대로이며, ordinary current policy staleness는 historical corruption error로
변환하지 않는다.

## 13. Concurrency, idempotency, and lock order

### 13.1 Idempotency

- same immutable request ID + same fingerprint: 기존 결과를 그대로 replay한다.
- same immutable request ID + different fingerprint: `CYCLE_REQUEST_IDENTITY_CONFLICT`.
- same cycle ID + same fingerprint: 기존 Cycle/decision을 replay한다.
- same cycle ID + different fingerprint: `CYCLE_IDENTITY_CONFLICT`.
- same terminal epoch + same admitted payload: existing lineage tip을 replay한다.
- same terminal epoch + different payload without validated correction authority source: `TERMINAL_EPOCH_CONFLICT`.
- same ProjectMemoryEntryId + same fingerprint: existing immutable entry replay.
- same ProjectMemoryEntryId + different fingerprint: `MEMORY_LINEAGE_IDENTITY_CONFLICT`.
- same MemoryLineageKey/revision + competing different-content successors: exactly one winner; loser is stale/conflict.
- same NextAction proposal/selection ID에도 동일 규칙을 적용한다.

Historical replay는 다음 순서를 고정한다.

1. existing immutable request ID/cycle ID/terminal epoch를 lookup한다.
2. stored candidate/payload, exact historical source snapshot, original
   `HistoricalMemoryPolicyAuthorityV1`을 projection-independent/as-of-admission 방식으로 다시 검증한다.
3. same fingerprint이면 동일 CycleAdmissionDecision, AdmittedCycle, ProjectMemoryEntry IDs/content를
   반환한다. different fingerprint이면 해당 typed identity conflict를 반환한다.
4. 그 뒤에만 latest source-owner events와 ProjectMemoryAuthorityEvents를 fold하여 current applicability
   projection을 reconstruct한다.

Later source currentness와 current policy/catalog 변화는 historical Cycle/source/content fingerprint에
포함되지 않으므로 같은 historical proposal replay를 새 Cycle identity로 만들지 않는다. Historical
policy graph corruption은 `MEMORY_POLICY_HISTORICAL_PROVENANCE_INVALID`, historical source graph corruption은
`CYCLE_PROVENANCE_CORRUPT` 또는 `CYCLE_HISTORICAL_SOURCE_PROVENANCE_INVALID`로 fail closed하지만,
정상적인 later source/policy revocation/supersession/expiry는 replay 성공 후 current view만 바꾼다.
New admission의 initial publication은 section 11.3 high-watermark와 expected lineage revision을 같은
transaction에서 확인한다.

### 13.2 Deterministic lock order

새 admission transaction은 다음 순서를 고정한다.

1. exact P1-4 WorkRun row `FOR UPDATE`
2. cycle/request global identity advisory locks, lexical key order
3. terminal epoch advisory lock
4. project-memory scope advisory lock `(project_id, scope_key)`
5. affected MemoryLineageKeys, lexical byte order
6. project NextAction projection lock, selection이 같은 transaction에 포함될 때만

두 WorkRun 또는 두 project scope를 다루는 operation은 V1에서 금지한다. 필요한 경우 별도 serial transactions로 분리한다. P1-4/P1-6/P1-7 lock을 획득한 상태에서 역순으로 P1-8 lock을 요청하는 API는 제공하지 않는다.

### 13.3 Concurrent outcomes

동일 terminal epoch의 동시 requests 중 하나만 새 admission을 생성한다. loser는 commit 후 fingerprint를 비교하여 replay 또는 typed conflict로 종료한다. 현재 projection update는 expected revision compare-and-swap semantics와 unique constraints를 함께 사용한다. “last write wins”는 금지한다.

동일 MemoryLineageKey의 concurrent successors는 lineage advisory lock과 expected lineage revision 아래 serialize한다. Unique current-tip constraint는 `0..1 CURRENT` cardinality를 보조하며, constraint violation을 retry 없는 generic database error로 숨기지 않고 `MEMORY_APPLICABILITY_CONFLICT`로 변환한다.

## 14. PostgreSQL persistence and restart semantics

이 절은 future implementation contract이며 migration을 생성하지 않는다.

### 14.1 Logical durable stores

- cycle candidates/requests/evaluations/decisions
- admitted cycles
- cycle authority events
- memory declaration authority policies
- immutable memory-policy issuance/supersession/revocation event history
- project memory entries/CycleMemoryReferences/authority events
- rebuildable current-memory projection
- NextAction eligibility policies/descriptors/proposals/evaluations/selections/events
- immutable NextAction selection-policy/eligibility-policy/descriptor owner-event history
- rebuildable current-next-action projection

### 14.2 Transaction boundary

하나의 **new** Cycle admission은 current declaration policy/source-enrollment resolution, projection-independent historical
source/content/terminal binding 검증, lineage lock/revision 검증, immutable evaluation/decision insert,
AdmittedCycle insert, ProjectMemoryEntry 또는 CycleMemoryReference projection, admission-observation
source-event high-watermark fold, initial applicability event, current projection update를 하나의 PostgreSQL
transaction으로 수행한다. Historical identity는 high-watermark의 current state를 포함하지 않으며,
current projection은 high-watermark fold가 끝나기 전 외부에 publish하지 않는다. 일부만 durable하거나
non-current entry가 잠시 `CURRENT`인 상태는 허용하지 않는다.

Existing Cycle replay transaction은 original admission sequence를 기준으로 immutable historical policy와
source provenance를 검증한 뒤 same identity를 반환하고, current policy/source/applicability event를
별도로 fold한다. Current policy가 historical verifier input으로 역유입되지 않는다.

New NextAction selection은 별도 transaction을 기본으로 한다. admission transaction이 commit된 후
current eligibility/selection policy, current enrolled descriptor와 authoritative inputs를 다시 읽어
selection한다. Historical selection replay는 original issuance as-of policy/descriptor graph를 먼저
검증하고 current projection을 나중에 rebuild한다. 이 분리는 Cycle 성공과 NextAction selection 실패를
혼합하지 않는다.

### 14.3 Restart

- process-local cache/queue는 authority가 아니다.
- restart 후 durable requests/decisions/events를 읽어 동일 결과를 replay한다.
- `PENDING` 같은 durable intermediate status를 구현한다면 lease/owner/expiry만으로 admission을 확정할 수 없고, transaction rollback 또는 deterministic resume가 가능해야 한다.
- projection은 immutable log에서 rebuild하며 rebuild 전에는 stale projection을 current authority로 제공하지 않는다.
- incomplete external export는 admission rollback 사유가 아니다. export는 committed object를 참조하는 재시도 가능한 별도 operation이다.

## 15. Fail-closed corruption handling

다음 조건에서는 admission/retrieval/selection을 fail closed한다.

- referenced object missing
- stored fingerprint와 recomputed fingerprint 불일치
- authority revision/root mismatch
- new admission의 missing/revoked/superseded MemoryDeclarationAuthorityPolicy 또는 current source enrollment
- replay의 immutable historical MemoryDeclarationAuthorityPolicy payload/authority/as-of validity mismatch
- source-to-content mismatch
- invalid/non-deterministic MemoryLineageKey normalization or multiple current tips
- accepted Judgment와 accepted WorkRun/TransitionDecision binding 불일치
- impossible correction/supersession graph
- duplicate current lineage tip
- event sequence gap/duplicate
- projection과 immutable log 불일치
- unknown enum/schema version
- privacy/export policy ambiguity
- new selection의 missing/revoked/superseded NextAction eligibility/selection policy, current unenrolled descriptor, or parameter-schema mismatch
- replay의 immutable historical NextAction policy/descriptor/enrollment/as-of issuance mismatch
- canonical authority conflict를 deterministic하게 resolve할 수 없음

자동 repair, silent row rewrite, best-effort admission, summary 기반 복구는 금지한다. 시스템은 typed error, affected refs, safe retry 가능 여부를 기록한다. Repair는 별도 TaskContract와 owner-authorized append-only correction으로만 수행한다.

## 16. Deterministic retrieval contract

### 16.1 Query specification

V1 query는 다음 structured fields만 사용한다.

- project ID
- exact scope selector: project/task-contract/task/work-run/subject
- MemoryLineageKey 또는 semantic-slot selector when supplied
- category allowlist
- current-only 또는 authorized historical mode
- as-of authority revision/event sequence
- privacy/export clearance
- deterministic limit

Free-form semantic query, embedding similarity, Agent-generated relevance score는 V1 authority path에 없다.

Default query는 항상 `current-only = true`이며 exact as-of projection에서 `CURRENT`인 entry만 반환한다.
Authorized historical mode만 non-current entry를 state/reason/source-owner event ref와 함께 반환할 수
있고, 그 결과에는 `NOT_CURRENT_CONTEXT`를 표시한다. Historical Cycle/entry 존재는 default retrieval
eligibility가 아니다.

### 16.2 Ordering

결과 순서는 다음 tuple의 ascending/descending direction을 API version에 고정한다.

1. scope specificity: exact TaskContract, exact task, project
2. policy category priority
3. applicability effective revision descending
4. Cycle admission sequence descending
5. MemoryLineageKey lexical ascending
6. memory declaration ordinal ascending
7. memory entry ID lexical ascending

동일 query specification과 동일 as-of revision은 byte-equivalent ordered refs를 반환해야 한다.

### 16.3 Retrieval result

각 result는 ProjectMemoryEntryId/fingerprint, MemoryLineageKey/schema version, source Cycle ID, source Judgment/TransitionDecision/evidence refs, content authority policy/ref/mode, current applicability state/revision, category, privacy class를 포함한다. Display summary는 convenience field일 뿐 score나 authority에 관여하지 않는다.

## 17. V1 Next Action owner and selection model

### 17.1 Selected owner model

V1은 **System-owned deterministic selection**을 유일한 owner model로 선택한다.

- P1-8 System이 `NextActionEvaluation`과 `NextActionSelection`을 소유한다.
- Human/Agent/executor/System component는 `NextActionProposal`을 제출할 수 있으나 proposal은 선택이 아니다.
- Human이 발행한 TaskContract/canonical policy는 selection input일 수 있지만, V1 selection object의 owner는 P1-8 System 하나다.
- 필요 Human 판단이 아직 없는 항목은 System이 선택을 위조하지 않고 `NEXT_ACTION_HUMAN_INPUT_REQUIRED`로 fail closed한다.

### 17.2 NextActionEligibilityPolicy and enrolled descriptors

`NextActionEligibilityPolicy`는 `P1_8_NEXT_ACTION_ELIGIBILITY_POLICY_AUTHORITY_V1`가 발행하는 immutable versioned action catalog다. Proposal caller는 descriptor를 register/modify할 수 없다. **New NextActionSelection**은 exact current unsuperseded eligible `NextActionEligibilityPolicy`, exact current `NextActionSelectionPolicy`, 그리고 current policy에 enrolled된 exact current `NextActionDescriptor`를 모두 요구한다.

`ActionRefV1 = {eligibility_policy_id, eligibility_policy_version, action_id, action_version, descriptor_fingerprint}`

각 `NextActionDescriptor`는 다음 exact fields를 포함한다.

- action ID/version, action kind
- project ID와 allowed scope kind/IDs
- parameter schema ID/version/fingerprint와 allowed/default parameter rules
- source authority kind/ref/version/fingerprint
- allowed selection mode: `OPERATIONAL_RECOVERY` 또는 `CYCLE_DERIVED`
- priority classification source kind/ref/hash와 policy ordinal
- required Human input kind: `NONE`, `BEFORE_SELECTION`, `AFTER_TASK_ISSUANCE_P1_7`
- Task issuance owner: exact `EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY`
- Task template ref/hash when one exists
- privacy/security restrictions
- issued/revoked/supersedes refs, authority revision
- issuance/effective event sequence와 `current_projection_on_invalidation = PRESERVE_UNTIL_REPLACED | WITHDRAW_CURRENT`; revocation은 항상 `WITHDRAW_CURRENT`
- descriptor fingerprint

Selected V1 descriptor source kinds:

| Source kind | V1 rule |
|---|---|
| `POLICY_ACTION_CATALOG` | P1-8 policy authority가 descriptor 전체를 immutable catalog entry로 발행. Caller cannot enroll. |
| `CANONICAL_ROADMAP_ITEM` | exact canonical roadmap/critical-path item ref, document hash, stable anchor를 policy가 명시적으로 enroll해야 함. Markdown 존재만으로는 enrollment 아님. Operational schema/owner는 policy descriptor가 고정. |
| `TASK_CONTRACT_FOLLOW_UP_TEMPLATE` | external Task authority가 발행한 exact TaskContract/template ref/hash/schema를 policy가 enroll해야 함. Proposal이 template을 만들 수 없음. |
| `OWNER_BLOCKER_RECOVERY_ACTION` | `NOT_SUPPORTED` as a direct V1 descriptor source because no predecessor generic recovery-action issuer exists. P1-4/P1-7 blocker facts는 eligibility/priority input일 뿐 action definition이 아님. |

Eligibility policy와 selection policy도 policy ID/version/fingerprint, canonical payload, authority
ID/version/revision, issuance/effective event sequence, issued/revoked/supersedes refs,
`current_projection_on_invalidation`을 immutable fields로 보존한다. Ranking policy는 여전히 action을
enroll할 수 없고 descriptor authority는 eligibility policy에만 있다.

#### 17.2.1 Historical NextAction policy/descriptor authority

Existing `NextActionSelection` replay는 current catalog/enrollment lookup을 issuance criterion으로 사용하지
않는다. 대신 `HistoricalNextActionAuthorityV1`의 다음 exact tuple을 검증한다.

- stored selection ID/payload fingerprint, issued-at/issuance sequence, selection revision
- exact eligibility policy ID/version/fingerprint와 canonical immutable payload
- exact selection policy ID/version/fingerprint와 canonical immutable payload
- 두 policy의 authority ID/version/revision, issuer authenticity, issuance/effective event history
- exact ActionRef와 descriptor ID/version/fingerprint/canonical immutable payload/source-authority binding
- eligibility policy가 original selection issuance에서 descriptor를 exact fingerprint로 enrolled했고,
  eligibility policy, selection policy, descriptor가 모두 그 시점에 valid했다는 as-of owner-event proof
- stored NextActionEvaluation, canonical parameters/fingerprint, authoritative input refs, reason/ranking trace,
  selection payload의 deterministic recomputation equality

Historical verifier는 original selection issuance high-watermark까지만 policy/descriptor owner events를
fold한다. Later v2 supersession/revocation, current catalog version, current enrollment 여부는 replay
criterion이 아니다. Original issuance 전에 policy/descriptor가 이미 revoked/superseded/unenrolled였거나
stored payload/fingerprint/authority/ranking trace가 불완전 또는 불일치하면
`NEXT_ACTION_POLICY_HISTORICAL_PROVENANCE_INVALID`로 fail closed한다. Later ordinary current staleness는
historical corruption이 아니며 동일 immutable NextActionSelection replay를 허용한다.

### 17.3 Proposal ceiling and pre-ranking eligibility

NextActionProposal이 할 수 있는 것:

- exact current `ActionRef` nominate
- descriptor parameter schema가 허용한 parameters 제출
- non-authoritative rationale와 source hints 제출

할 수 없는 것:

- 새 ActionRef/descriptor/action kind/template 정의
- descriptor fingerprint/version 변경
- priority/security/blocker/baseline/critical-path classification 주장으로 authority 생성
- Task issuance owner 변경
- Human requirement bypass
- descriptor의 project/scope/privacy/security 경계 확장

Evaluation order:

1. current unsuperseded eligible NextActionEligibilityPolicy와 current NextActionSelectionPolicy를
   exact ID/version/fingerprint로 resolve
2. ActionRef exact current catalog lookup, current enrolled descriptor version/fingerprint equality와
   non-revocation/non-supersession 검증
3. descriptor source authority ref/hash/currentness 검증
4. selection mode/project/scope 검증
5. parameter schema validation 및 canonical parameter fingerprint 계산
6. required Human input 확인
7. authoritative priority facts resolve
8. eligible candidates만 current selection policy로 deterministic ranking

Novel/unregistered ActionRef는 `NEXT_ACTION_ACTION_NOT_ENROLLED`, payload fingerprint mismatch는
`NEXT_ACTION_DESCRIPTOR_MISMATCH`, known descriptor/policy version이 now revoked/superseded/unenrolled이면
`NEXT_ACTION_DESCRIPTOR_CURRENTLY_INELIGIBLE`, parameter mismatch는
`NEXT_ACTION_PARAMETER_SCHEMA_MISMATCH`다. Current eligibility/selection policy가 없으면
`NEXT_ACTION_POLICY_NOT_FOUND`다. `BEFORE_SELECTION` Human input이 없으면
`NEXT_ACTION_HUMAN_INPUT_REQUIRED`이며 selection을 생성하지 않는다.

### 17.4 Authoritative priority facts and deterministic ranking

Priority facts의 allowed authority sources:

- versioned eligibility/selection policy mapping
- current P1-4 WorkRun state와 exact blocker/failure refs
- current P1-7 Judgment refs where applicable
- exact enrolled canonical baseline/roadmap/critical-path ref/hash/ordinal
- current ProjectMemoryEntry refs as contextual inputs only

Rejected/HOLD/failed/rework provenance는 source domain operational facts로 평가하며 ProjectMemoryEntry로 변환하지 않는다. Proposal의 priority/security/blocker/baseline fields는 audit-only이며 ranking input/fingerprint에서 제외한다.

V1 priority order:

1. authoritative security/policy/missing-artifact blocker
2. authoritative rejected/HOLD/failed/rework recovery
3. authoritative canonical baseline gap/authority conflict
4. enrolled accepted core critical path
5. enrolled operational hardening
6. enrolled optional optimization

Eligible candidates의 ranking tuple:

`(authoritative_priority_rank, policy_dependency_ordinal, enrolled_critical_path_ordinal, descriptor_policy_ordinal, ActionRef lexical, proposal_id lexical)`

Input conflict/missing authority는 selection 없이 typed error다.

`deterministic ranking != action authority`

Ranking은 action을 enroll하지 않으며 eligibility를 통과한 descriptors 사이의 order만 결정한다.

### 17.5 Two selection modes

- `OPERATIONAL_RECOVERY`: current BLOCKED/REWORK_REQUIRED/REJECTED/FAILED provenance를 source domain에서 직접 읽되 enrolled recovery descriptor만 선택한다. AdmittedCycle을 요구하지 않으며 memory를 만들지 않는다.
- `CYCLE_DERIVED`: current AdmittedCycle lineage의 **`CURRENT` ProjectMemoryEntry만** current
  ProjectMemoryView에서 읽고 enrolled accepted critical-path descriptor에서 선택한다. Historical-only,
  `SUPERSEDED`, `REVOKED`, `EXPIRED` entry와 historical retrieval result는 eligibility/ranking/context
  input으로 사용할 수 없다.

두 mode 모두 System-owned이며 같은 eligibility-before-ranking contract를 사용한다.

### 17.6 Selection identity and authoritative payload

NextActionSelection payload:

- globally unique selection ID와 project/scope
- selection mode
- selection policy와 eligibility policy ID/version/fingerprint
- selected ActionRef와 full descriptor fingerprint
- validated canonical parameters와 parameter fingerprint
- source AdmittedCycle/ProjectMemoryEntry refs
- operational recovery refs when applicable
- authoritative blocker/baseline/security/queue/critical-path source refs/revisions
- ordered reason codes와 deterministic eligibility/ranking trace
- required Human input kind와 Task issuance owner
- expected/observed project selection revision
- selection payload fingerprint와 predecessor selection ref

Selection identity에는 original issuance의 exact eligibility-policy, selection-policy, descriptor
versions/fingerprints가 들어간다. Later current policy/catalog revision, later policy/descriptor owner-event
sequence, current enrollment 여부와 current-next-action projection state는 selection payload fingerprint에
들어가지 않는다.

Same selection ID + same fingerprint는 replay하고 different fingerprint는 `NEXT_ACTION_IDENTITY_CONFLICT`다. Correction/supersession/revocation은 append-only selection event와 new selection으로 처리한다. Stale expected revision은 `NEXT_ACTION_STALE_REVISION`이며 last-write-wins를 허용하지 않는다.

Historical replay order:

1. stored selection ID/payload와 original issuance sequence를 lookup한다.
2. section 17.2.1 `HistoricalNextActionAuthorityV1`으로 exact historical eligibility policy,
   selection policy, descriptor, enrollment과 deterministic evaluation/selection payload를 검증한다.
3. same immutable fingerprint이면 same NextActionEvaluation/NextActionSelection identity와 payload를
   반환하고, different fingerprint이면 `NEXT_ACTION_IDENTITY_CONFLICT`다.
4. 그 뒤에만 current policy/descriptor events를 fold하여 current-next-action projection을 rebuild한다.

Later policy/descriptor supersession/revocation은 old NextActionSelection을 rewrite하지 않는다. New
selection에서는 stale version을 사용할 수 없다. Existing current projection이 invalidated policy/descriptor를
가리키고 applicable immutable `current_projection_on_invalidation = WITHDRAW_CURRENT` 또는 revocation이
있으면 P1-8은 exact policy/descriptor owner event, selection ref/fingerprint, expected current revision을
bind한 append-only `NextActionAuthorityEvent`를 발행해 current selection을 non-current로 만든다. Historical
selection과 its original policy/descriptor refs는 보존되며 future selection eligibility만 current catalog를
따른다.

### 17.7 Separation from workflow transition

NextActionSelection은 project-level authoritative recommendation/projection이며 다음을 할 수 없다.

- WorkRun state mutation
- TransitionRequest 자동 생성/승인
- TransitionDecision 대체
- TaskContract 자동 발행/수정
- HumanGate/HumanResult/Judgment 대체

### 17.8 Exact Task issuance boundary

Targeted current-source inspection found TaskContract IDs/versions and TaskContract-scoped P1-6/P1-7 policy issuers, but no general runtime TaskContract object or Task issuer. 따라서 P1-8 V1은 Task 발행 권한을 새로 만들지 않는다.

Exact handoff:

`NextActionSelection -> TaskIssuanceCandidate -> external Command Center/Task authority process -> issued TaskContract ref -> new WorkRun/P1-4 flow`

- P1-8 System은 selected enrolled descriptor/template와 validated parameters로 TaskIssuanceCandidate를 deterministic하게 만들 수 있다.
- `TaskIssuanceCandidate != TaskContract`이며 실행 권한이 없다.
- exact owner `EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY`가 별도 governance/Human process로 TaskContract를 issue/reject/revise한다.
- issued TaskContract ref가 생기면 append-only fulfillment/link event로 Selection에 연결할 수 있으나 Selection을 rewrite하지 않는다.
- `AFTER_TASK_ISSUANCE_P1_7`은 발행된 Task의 P1-7 flow에서만 처리하며 P1-8이 HumanResult/Judgment를 mint하지 않는다.

### 17.9 Repository roadmap boundary

`.aiassistant/records/aiscc/NEXT_ACTIONS.md`는 repository governance roadmap이다. Markdown roadmap에 항목이 존재한다는 사실만으로 runtime ActionRef/NextActionDescriptor/NextActionSelection authority가 되지 않는다. Exact document hash/anchor를 current eligibility policy가 enroll해야 하며 runtime selection은 그 파일을 자동 수정하거나 canonical roadmap authority를 흡수하지 않는다.

## 18. Task, Cycle, commit, run, and artifact mapping

AdmittedCycle은 다음 cardinality를 명시적으로 보존한다.

- one project
- one exact TaskContract ID/version
- one exact WorkRun
- one accepted terminal TransitionDecision
- one accepted Judgment
- zero or more P1-6 evidence refs as required by TaskContract
- zero or more commit refs
- zero or more executor run/report/artifact refs
- zero or more ProjectMemoryEntries

Commit은 acceptance authority가 아니다. commit ref에는 repository identity, full commit SHA, tree SHA 또는 path/blob hashes, role(implementation/evidence/design/closure), source observation method를 기록한다.

Executor report/run은 evidence pointer일 수 있지만 Human-owned result를 executor-completed로 주장할 수 없다. Missing required commit/run/artifact mapping은 TaskContract requirement에 따라 admission reject가 되며, optional mapping의 부재는 명시적 `NOT_REQUIRED`로만 허용한다.

Repository `CommandCenterCycleRecord`가 AdmittedCycle을 가리킬 때는 cycle ID, admission decision ID, payload fingerprint를 기록해야 한다. 그 Markdown의 수정은 runtime Cycle을 수정하지 않는다.

## 19. Privacy, retention, and export

V1 privacy class는 다음 셋이다.

- `PRIVATE_INTERNAL`: project 내부 deterministic retrieval만 허용.
- `PUBLIC_SANITIZED`: policy-approved field allowlist와 redaction을 통과한 export 가능 projection.
- `NON_EXPORTABLE`: runtime 내부 provenance만 유지하고 external/repository export 금지.

원칙:

- credentials, secrets, raw prompts/chat, personal data, hidden chain-of-thought, unrestricted logs는 memory content로 admission하지 않는다.
- source artifact가 private여도 exact opaque ref/hash만 허용될 수 있으며 access check를 우회하지 않는다.
- export는 admitted object의 새 sanitized projection이며 source object를 mutation하지 않는다.
- `PUBLIC_SANITIZED`는 자동 분류하지 않는다. versioned export policy와 field-level allowlist가 필요하다.
- retention 만료는 historical admission을 위조하지 않는다. payload tombstone이 허용되는 법적 요구가 있다면 hash/provenance tombstone과 owner-authorized event를 남기고 retrieval을 fail closed한다.
- CommandCenterCycleRecord export는 별도 governance review 대상이며 runtime admission을 의미하지 않는다.

## 20. Self-Dogfooding handoff boundary

이 설계가 Human accepted되고 future P1-8 implementation/evidence가 별도 acceptance를 통과하기 전까지:

- 기존 repository workflow가 canonical operating path다.
- runtime AdmittedCycle/ProjectMemory/NextActionSelection을 실제 project authority로 사용하지 않는다.
- raw historical Task/Cycle Markdown을 bulk-import하지 않는다.
- backfill은 별도 TaskContract, allowlisted sources, deterministic mapping, Human-owned acceptance가 필요하다.
- cutover/rollback plan과 dual-read divergence evidence 없이 Self-Dogfooding을 선언하지 않는다.

따라서 이 문서의 생성은 cutover가 아니다.

## 21. P2 and P3 boundaries

P1-8 future implementation은 headless domain/API/persistence/evidence에 한정한다.

- P2 UI는 이 contract를 소비할 수 있으나 admission semantics를 UI 상태로 재정의할 수 없다.
- vector/RAG/search ranking은 optional P2+ convenience layer이며 authoritative retrieval을 대체할 수 없다.
- P3 deployment/Public Live는 별도 security, operations, credentials, rollback, Human approval 범위다.
- external integration이 제출한 summary/proposal은 CycleCandidate/NextActionProposal일 뿐이다.

## 22. Failure and error vocabulary

Future implementation은 최소한 다음 typed codes를 사용하고 free-form message만으로 분기하지 않는다.

| Code | Meaning | Retry class |
|---|---|---|
| `CYCLE_SOURCE_NOT_FOUND` | required predecessor ref missing | after source repair |
| `CYCLE_SOURCE_BINDING_MISMATCH` | project/task/run/state/version mismatch | no, new valid request |
| `CYCLE_NOT_ACCEPTED` | Judgment or terminal state not ACCEPTED | no |
| `CYCLE_EVIDENCE_BINDING_MISMATCH` | exact P1-6 roots/refs mismatch | no |
| `CYCLE_HISTORICAL_SOURCE_PROVENANCE_INVALID` | historical issuance graph is missing/corrupt/invalid at terminal, or declaration source is not in the exact terminal-consumed attestation/root | no; new valid terminal lineage required |
| `CYCLE_SOURCE_CURRENTNESS_NOT_AUTHORITY` | caller/current projection is offered as a substitute for immutable historical source proof | corrected request with historical provenance |
| `CYCLE_REQUEST_IDENTITY_CONFLICT` | request ID reused with different fingerprint | no |
| `CYCLE_IDENTITY_CONFLICT` | cycle ID reused with different fingerprint | no |
| `TERMINAL_EPOCH_CONFLICT` | competing payload for same terminal epoch | correction only |
| `CYCLE_SCHEMA_UNSUPPORTED` | unknown schema/version/category | after upgrade |
| `CYCLE_PRIVACY_POLICY_VIOLATION` | content/export policy failure | corrected request |
| `CYCLE_PROVENANCE_CORRUPT` | hash/revision/graph/event corruption | owner-authorized repair |
| `MEMORY_DIRECT_WRITE_FORBIDDEN` | projection boundary bypass attempt | no |
| `MEMORY_AUTHORITY_ESCALATION_FORBIDDEN` | canonical/TaskContract promotion attempt | no |
| `MEMORY_DECLARATION_AUTHORITY_NOT_FOUND` | category policy or exact immutable source authority missing | after owner source issuance |
| `MEMORY_POLICY_HISTORICAL_PROVENANCE_INVALID` | stored policy payload/fingerprint/authority or as-of-original-admission validity/source enrollment is corrupt or invalid | no; historical provenance investigation |
| `MEMORY_POLICY_CURRENTLY_INELIGIBLE` | policy/source enrollment requested for a new admission is revoked, superseded, stale, or not the current eligible version | refresh and use current policy |
| `MEMORY_DECLARATION_SOURCE_MISMATCH` | source-derived/attested content fingerprint differs from declaration | corrected declaration |
| `MEMORY_DECLARATION_MODE_NOT_SUPPORTED` | category/mode requires unsupported semantic inference | no in V1 |
| `MEMORY_LINEAGE_IDENTITY_CONFLICT` | entry/lineage ID or normalized key reused inconsistently | no |
| `MEMORY_SUPERSESSION_AUTHORITY_REQUIRED` | different-content current-tip replacement lacks accepted authority source | after authority issuance |
| `MEMORY_CORRECTION_AUTHORITY_REQUIRED` | correction claim lacks source-owner event or structured directive | after authority issuance |
| `MEMORY_REVOCATION_AUTHORITY_REQUIRED` | revocation claim lacks source-owner event or structured directive | after authority issuance |
| `MEMORY_APPLICABILITY_CONFLICT` | stale or multiple current tips | retry after refresh/repair |
| `MEMORY_RETRIEVAL_REVISION_UNAVAILABLE` | requested as-of snapshot cannot be reconstructed | repair |
| `NEXT_ACTION_POLICY_NOT_FOUND` | no exact current eligible eligibility/selection policy | after policy issuance |
| `NEXT_ACTION_POLICY_HISTORICAL_PROVENANCE_INVALID` | stored eligibility/selection policy or descriptor payload/authority/enrollment was invalid or corrupt at original selection issuance | no; historical provenance investigation |
| `NEXT_ACTION_ACTION_NOT_ENROLLED` | proposal ActionRef is absent from current eligibility catalog | after authoritative enrollment |
| `NEXT_ACTION_DESCRIPTOR_MISMATCH` | ActionRef fingerprint/version differs from enrolled descriptor | corrected proposal |
| `NEXT_ACTION_DESCRIPTOR_CURRENTLY_INELIGIBLE` | known policy/descriptor version is now revoked, superseded, or unenrolled and cannot create a new selection | refresh and use current ActionRef/policies |
| `NEXT_ACTION_PARAMETER_SCHEMA_MISMATCH` | proposed parameters fail enrolled schema/scope | corrected proposal |
| `NEXT_ACTION_INPUT_CONFLICT` | unresolved current authority conflict | after correction |
| `NEXT_ACTION_HUMAN_INPUT_REQUIRED` | policy requires missing Human-owned input | after Human action |
| `NEXT_ACTION_IDENTITY_CONFLICT` | selection/proposal ID payload conflict | no |
| `NEXT_ACTION_STALE_REVISION` | expected project selection revision stale | immediate safe retry |
| `PERSISTENCE_UNAVAILABLE` | PostgreSQL transaction cannot complete | safe retry |

Historical/current error non-substitution is normative. `*_HISTORICAL_PROVENANCE_INVALID`는 immutable
payload/authority/as-of-original-issuance가 실제로 invalid 또는 corrupt할 때만 사용한다. Later ordinary
supersession/revocation/current catalog change에는 사용하지 않는다. `*_CURRENTLY_INELIGIBLE`와
`NEXT_ACTION_POLICY_NOT_FOUND`는 new admission/new selection의 current eligibility failure이며 old immutable
Cycle/Selection replay를 실패시키지 않는다.

Every failure record includes request ID, project ID, relevant refs, observed/expected revisions, code, retry class, server timestamp. It must not leak secret payloads.

## 23. Future implementation handoff checklist

Future implementation Task must require all of the following before runtime coding:

- Human acceptance of this design and accepted revision/hash
- exact model/schema/API names preserving `AdmittedCycle` vs `CommandCenterCycleRecord`
- immutable DTOs and canonical fingerprint test vectors
- PostgreSQL migration and constraints for uniqueness, append-only events, lineage tips
- deterministic lock-order and concurrent request tests
- restart/replay/projection rebuild tests
- P1-4 accepted terminal binding integration tests
- P1-6 projection-independent historical attestation/issuance/root tests separated from current-effectiveness tests
- P1-7 accepted Judgment and supersession/revocation integration tests
- rejected/HOLD/failed/rework exclusion tests
- direct memory write and authority escalation rejection tests
- MemoryDeclarationAuthorityPolicy issuer/current-policy tests and all-category source-to-content test vectors
- new Cycle current-policy/current-enrollment tests separated from historical policy as-of-admission replay tests
- memory policy v1→v2 replay identity, new-v1 rejection, and policy-required append-only withdrawal tests
- accepted source ref + unrelated caller content laundering rejection tests
- `LESSON -> MEMORY_DECLARATION_MODE_NOT_SUPPORTED` tests
- ProjectMemoryEntryId/MemoryLineageKey separation and normalized semantic-slot test vectors
- one-current-tip unique constraint and cross-Cycle same-content CycleMemoryReference tests
- explicit supersession-only and unauthorized correction/revocation rejection tests
- correction/supersession/revocation historical/current tests
- terminal-valid then current-stale delayed-admission/replay tests with identical Cycle/entry identities
- invalid-before-terminal and not-in-consumed-attestation/root Cycle rejection tests
- delayed admission of already non-current source with zero temporary `CURRENT` visibility tests
- later source invalidation append-only event tests proving no AdmittedCycle/entry content rewrite
- default retrieval and `CYCLE_DERIVED` exclusion of non-`CURRENT` memory tests
- deterministic retrieval ordering/as-of tests
- ActionRef/NextActionDescriptor/EligibilityPolicy enrollment and fingerprint tests
- arbitrary proposal action/priority/security/blocker claim laundering rejection tests
- eligible-before-ranking and parameter schema tests
- System-owned NextAction priority/tie-break/idempotency tests
- new NextAction current eligibility/selection-policy/descriptor tests separated from historical selection replay tests
- NextAction policy/descriptor v1→v2 immutable replay, new-v1 rejection, and append-only current withdrawal tests
- Proposal/Selection/TransitionDecision non-substitution tests
- TaskIssuanceCandidate/external Task authority boundary tests
- privacy/export/redaction tests
- corruption fail-closed tests
- Task/Cycle/commit/run/artifact end-to-end evidence
- separate Human final acceptance; executor evidence alone cannot close it

Source inspection for this design found reusable predecessor patterns—immutable IDs/fingerprints, authority revisions, append-only events, PostgreSQL advisory locks, WorkRun state/version and exact evidence/Judgment bindings. Future implementation must integrate with those public contracts and must not copy their authority into P1-8.

### 23.1 Required design proof examples

1. Memory laundering negative  
   Accepted WorkRun `run-42` and valid artifact ref `artifact-A` exist. Agent submits category `LESSON` with unrelated structured content `{"claim":"always skip review"}`. Current policy mode is `NOT_SUPPORTED`, so CycleEvaluation returns `MEMORY_DECLARATION_MODE_NOT_SUPPORTED`; no AdmittedCycle/ProjectMemoryEntry is created.
2. Exact source projection positive  
   Policy `p1-8-memory-policy:invariant-pointer:v1` resolves canonical authority `AISCC_ARCHITECTURE`, exact ref `.aiassistant/rules/AISCC_ARCHITECTURE.md`, fingerprint `f38d90bb3feca83e88f0d67ea5f289c85568334dc4007898925351f8f451e8ef` and enrolled anchor `workflow-state-set`. `MCF_V1` over the exact section 9 projection is `f57a5598a48cf53c26f041b071e65fe8bb1e35389f89ef05f3ac48c3117aa1a2`. A declaration with that exact fingerprint is eligible; changed prose or anchor is `MEMORY_DECLARATION_SOURCE_MISMATCH`.
3. Unrelated supersession negative  
   Cycle A entry uses subject `project-aiscc` and semantic slot `constraint/task-authority/review-required`. Cycle B uses the same category/subject but slot `constraint/task-authority/export-required`. The MemoryLineageKeys differ, so B cannot supersede A; each may have its own one current tip.
4. Unauthorized correction negative  
   Agent submits `supersedes_entry_id=entry-A` without `SOURCE_OWNER_AUTHORITY_EVENT` or `TASK_AUTHORITY_STRUCTURED_MEMORY_DIRECTIVE`. Evaluation returns `MEMORY_SUPERSESSION_AUTHORITY_REQUIRED` and leaves entry-A current.
5. Next-action laundering negative  
   Proposal names `action_id=deploy-now` with caller-authored shell payload but no current ActionRef. Eligibility returns `NEXT_ACTION_ACTION_NOT_ENROLLED` before ranking; no NextActionSelection or TaskIssuanceCandidate is created.
6. Eligible action positive  
   Proposal references exact enrolled `ActionRef(policy-v3, rework-design, v1, descriptor-fingerprint)`, parameters validate against descriptor schema v2, and priority is derived from current HOLD/rework source refs plus policy ordinal. Eligibility passes and deterministic ranking is permitted. Proposal rationale/claimed priority is ignored.
7. Terminal-valid, current-stale historical replay  
   Structured result `ae-7` was validly admitted at WorkRun state version `vN`, appears in the exact
   ordered admitted refs/root of attestation `att-7`, and that attestation was consumed by the accepted
   Judgment/terminal TransitionDecision. A later source-owner event revokes `ae-7`. Delayed Cycle admission
   and same-fingerprint replay both return the same AdmittedCycle and ProjectMemoryEntry IDs; current
   applicability is `REVOKED`, default retrieval omits it, and `CYCLE_DERIVED` cannot use it.
8. Invalid-at-terminal source negative  
   Structured result `ae-8` was revoked before the exact terminal consumption snapshot, or is absent from
   the consumed attestation's ordered admitted refs/root. Even if it is from the same WorkRun or later becomes
   current, CycleEvaluation returns `CYCLE_HISTORICAL_SOURCE_PROVENANCE_INVALID`; no AdmittedCycle or
   ProjectMemoryEntry is created.
9. Delayed admission has no temporary CURRENT exposure  
   Historical source `ae-9` was valid at terminal but a committed owner event superseded it before P1-8
   admission. The admission transaction verifies history, creates immutable historical objects, folds the
   source-event high-watermark, records initial `SUPERSEDED` applicability, and publishes once. No external
   query can observe the entry as `CURRENT`.
10. Historical memory policy replay and new-admission split  
    Cycle `cycle-10` was admitted under exact `MemoryDeclarationAuthorityPolicy v1`. Policy v2 later
    supersedes v1. Same-fingerprint replay verifies v1's immutable payload/authority and that v1 was valid at
    the original admission sequence, then returns the same AdmittedCycle/ProjectMemoryEntry identities without
    requiring v1 to be current. A new admission naming v1 returns `MEMORY_POLICY_CURRENTLY_INELIGIBLE` and must
    resolve current v2.
11. Historical NextAction policy replay and new-selection split  
    Selection `selection-11` was issued under exact eligibility policy v1, selection policy v1 and enrolled
    descriptor v1. Later v2 policy/catalog supersedes them. Replay verifies the original immutable
    policy/descriptor payloads, enrollment and as-of-issuance validity and returns the same selection. A new
    selection using the old ActionRef returns `NEXT_ACTION_DESCRIPTOR_CURRENTLY_INELIGIBLE`; current v2 policies
    and descriptor are required.
12. Invalid-before-original-issuance policy negative  
    Memory policy v1 was already revoked before `cycle-12`'s claimed admission sequence, or a NextAction policy
    or descriptor v1 was already revoked/unenrolled before `selection-12`'s claimed issuance. Historical
    verification returns `MEMORY_POLICY_HISTORICAL_PROVENANCE_INVALID` or
    `NEXT_ACTION_POLICY_HISTORICAL_PROVENANCE_INVALID`. Later current policy repair cannot make the old claimed
    issuance valid.

## 24. Human review choices and acceptance gate

이 candidate는 V1 semantic choices를 다음처럼 닫아 제안한다.

- runtime term: `AdmittedCycle`
- accepted-only Cycle admission: Yes
- rejected/HOLD/failed/rework reusable memory admission: No
- memory production: Cycle admission transaction의 deterministic projection
- memory content authority: category별 versioned `MemoryDeclarationAuthorityPolicy` + exact source reconstruction
- new Cycle policy: current unsuperseded eligible MemoryDeclarationAuthorityPolicy + current valid source enrollment required
- historical Cycle policy replay: original exact policy ref/version/fingerprint and as-of-admission validity required; currentness not required
- later memory-policy invalidation: immutable Cycle/entry preserved; policy-contract-required withdrawal via append-only ProjectMemoryAuthorityEvent
- `LESSON`: V1 `NOT_SUPPORTED`
- direct raw session/summary import: No
- canonical rule/TaskContract auto-promotion: No
- memory identity: `ProjectMemoryEntryId != MemoryLineageKey`
- current-tip cardinality: one CURRENT per MemoryLineageKey
- supersession: `EXPLICIT_SUPERSESSION_ONLY`
- correction/revocation authority: source-owner event 또는 Task-authority structured directive only
- current/historical separation: append-only events + rebuildable projection
- structured-result historical authority: projection-independent exact P1-6 issuance graph plus terminal-consumed attestation/root membership; current effectiveness is not historical identity
- optional structured-result source outside terminal-consumed attestation/root: V1 `NOT_SUPPORTED`
- delayed admission of terminal-valid but now non-current source: preserve immutable Cycle/entry and publish directly as non-`CURRENT`
- historical replay: same immutable identity before separate current-applicability reconstruction
- V1 retrieval: structured exact deterministic retrieval, no vector/RAG authority
- default retrieval and `CYCLE_DERIVED`: `CURRENT` ProjectMemory only
- V1 Next Action owner: P1-8 System
- action eligibility: current versioned `ActionRef/NextActionDescriptor` enrollment required before ranking
- new NextAction selection policy: current eligibility policy + current selection policy + current enrolled descriptor required
- historical NextAction replay: original exact policy/descriptor versions and as-of-issuance validity required; current enrollment not required
- later NextAction policy/descriptor invalidation: immutable Selection preserved; current projection/future eligibility changed append-only
- proposal priority/security/blocker claims: non-authoritative and ignored
- NextAction selection modes: `OPERATIONAL_RECOVERY` and `CYCLE_DERIVED`
- Task issuance after Selection: external Command Center/Task authority; P1-8 produces non-authoritative TaskIssuanceCandidate only
- Self-Dogfooding cutover: not part of this Task

남은 Human-owned action은 이 design candidate 전체를 `ACCEPTED`, `REWORK_REQUIRED` 또는 `REJECTED`로 판정하는 것이다. Executor는 그 판정을 대신하지 않는다.

현재 판정:

`HUMAN_PENDING`

## 25. Prior-art and claim ceiling

Persistent project memory, event provenance, append-only correction, human curation, session-to-knowledge workflows, pre-action judgment gates, RAG/vector retrieval은 일반적 선행 영역 또는 prior-art boundary 안에 있다.

AISCC가 현재 주장할 수 있는 것은 accepted Product Thesis의 다음 통합 가설 수준을 넘지 않는다.

`Task -> Evidence -> Judgment -> Cycle -> Next Action`

그리고 이 설계가 구체화한 “Judgment-passed accepted provenance만 reusable curated memory로 admission하고 rejected/failed provenance는 operational history로 보존하며 deterministic next-action selection과 연결한다”는 조합은 differentiation hypothesis다. Patentability, novelty, freedom-to-operate 또는 broad ownership claim이 아니다.

Human acceptance와 구현 evidence가 없는 동안 이 문서는 claim proof가 아니며 `HUMAN_PENDING` design candidate다.
