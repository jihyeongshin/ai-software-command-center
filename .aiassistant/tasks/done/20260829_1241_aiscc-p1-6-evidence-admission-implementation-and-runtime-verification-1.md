# 작업지시서: P1-6 Evidence Admission Implementation + Runtime Verification

## meta

- task_id: `20260829_1241_aiscc-p1-6-evidence-admission-implementation-and-runtime-verification-1`
- created_at: `2026-08-29T12:41:00+09:00`
- phase: `P1-6 Evidence Admission`
- work_type: `EVIDENCE_ADMISSION_IMPLEMENTATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `P1-4 accepted kernel at/after d99ccc4ecde585685e93960a7fa39ecbfde89f9f; actual integration provenance must be reported`
- primary_semantic_owner: `P1-6_EVIDENCE`
- predecessor_expected_head: `c86e291f94bd9acc31e40bc78316132abfddd90b`
- accepted_design_path: `.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md`
- accepted_design_sha256: `0d9d4c194efda37f100c6183d1a7e88e1a09fe073dc3a37bbb5a3e1cd577e463`
- public_bounded_live_release: `NOT_RELEASED`
- p1_7_status: `NOT_STARTED`
- p1_8_status: `NOT_STARTED`

---

# 1. 현재 상태

Human final decision already exists:

```text
Human P1-6 design final review
판정: ACCEPTED
```

하지만 다음을 동일시하지 않는다.

```text
Human accepted in Browser chat
!= repository terminal persistence completed
```

현재 handoff가 요구하는 첫 repository action은 accepted P1-6 design의 terminal canonical persistence다.

Expected predecessor:

```text
HEAD:
c86e291f94bd9acc31e40bc78316132abfddd90b
```

Expected accepted design:

```text
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md

SHA-256:
0d9d4c194efda37f100c6183d1a7e88e1a09fe073dc3a37bbb5a3e1cd577e463
```

Latest accepted design rework Task:

```text
.aiassistant/tasks/done/
20260829_1026_aiscc-p1-6-checkpoint-human-ingress-and-optional-evidence-design-rework-1.md
```

Latest predecessor HOLD Cycle:

```text
.aiassistant/records/aiscc/cycles/
20260829_1026_aiscc-p1-6-checkpoint-human-ingress-and-optional-evidence-hold-1.cycle.md
```

P1-6 runtime/source implementation은 아직 시작되지 않았다.

---

# 2. load-bearing non-substitution invariants

다음은 절대 약화하지 않는다.

```text
AGENT_OUTPUT != SYSTEM_STATE
AGENT_CLAIM != ADMITTED_EVIDENCE
HUMAN_OWNED_EVIDENCE != EXECUTOR_COMPLETED

ExecutionStatus != WorkflowState

EXECUTOR_COMPLETED != ACCEPTED
EXECUTION_FAILED != FAILED

EvidenceCandidate != AdmittedEvidence
AdmittedEvidence != Judgment
AdmittedEvidence != TransitionDecision
AdmittedEvidence != WorkflowState

HumanResult != Judgment

SecurityAdmissionDecision != TransitionDecision
RuntimeMode != WorkflowState
```

Terminal authority:

```text
TERMINAL_TRANSITION
→ SYSTEM_ADMISSION
→ HUMAN_GATE_WHEN_REQUIRED
```

P1-6는 오직 owner-bound `G_EVIDENCE` fact/attestation만 소유한다.

P1-6 MUST NOT mint:

```text
G_CURRENT
G_HUMAN_*
G_JUDGMENT_*
TransitionDecision
WorkflowState
```

P1-7/P1-8 runtime authority를 이 Task에서 구현하지 않는다.

---

# 3. 이번 턴 목표

이 Task는 두 개의 명확히 분리된 Stage를 가진다.

## Stage 0 — accepted P1-6 design terminal persistence

1. actual repository HEAD를 검증한다.
2. accepted `AISCC_EVIDENCE_ADMISSION.md` SHA-256을 검증한다.
3. final accepted design rework Task 및 predecessor HOLD Cycle provenance를 검증한다.
4. P1-6 design terminal acceptance Cycle을 생성한다.
5. 아래 canonical state를 Human acceptance에 맞게 갱신한다.
   - `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
   - `.aiassistant/records/aiscc/DECISION_REGISTER.md`
   - `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
6. accepted design terminal persistence만 exact Git commit한다.
7. Stage 0 commit hash와 exact committed path set을 기록한다.
8. 이 commit이 성공하기 전에는 P1-6 runtime source를 변경하지 않는다.

## Stage 1 — P1-6 Evidence Admission runtime implementation

Stage 0 commit 성공 이후에만 진행한다.

1. accepted P1-6 domain/authority contract를 구현한다.
2. PostgreSQL durable provenance와 restart reconstruction을 구현한다.
3. checkpoint-specific Requirement applicability와 EvidenceSet completeness를 구현한다.
4. `HUMAN_DIRECT_EVIDENCE` ingress authority를 P1-6 경계 안에서 구현한다.
5. reuse / concurrency / idempotency / anti-replay / revocation / supersession을 구현한다.
6. exact `EvidenceSetSatisfactionAttestation`을 생성하고 P1-4 `G_EVIDENCE` verifier와 narrow integration한다.
7. accepted proof matrix를 targeted runtime tests로 검증한다.
8. P1-3/P1-4/P1-5 affected regression을 수행한다.
9. runtime implementation은 Command Center review candidate로 제출하고 **이 Task에서 implementation commit은 생성하지 않는다.**

---

# 4. 이번 턴 비목표

- P1-7 Human Gate / HumanResult / Judgment runtime 구현
- P1-8 Project Memory / Cycle Admission runtime 구현
- workflow state/transition graph 재설계
- 새로운 `WorkflowState` 또는 transition 추가
- P1-5 provider/tool execution semantics 재설계
- real OpenAI/provider call
- public Live release
- deployment
- Browser UI
- public anonymous evidence ingress
- general-purpose arbitrary file/path/URL evidence ingestion
- LLM confidence 기반 evidence authority
- first-class `OPTIONAL` evidence profile/requirement semantics
- hidden fallback from missing evidence to Agent claim
- unrelated project refactor
- broad architecture cleanup

---

# 5. Stage 0 mandatory predecessor verification

Source mutation 전에 다음을 exact하게 수행한다.

## 5.1 repository identity

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main
```

검증:

```text
actual HEAD == c86e291f94bd9acc31e40bc78316132abfddd90b
```

불일치:

```text
STOP
→ BLOCKED_PREDECESSOR_HEAD_DRIFT
```

HEAD drift를 임의로 해석하거나 later commit을 자동 채택하지 않는다.

## 5.2 accepted design hash

```text
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md
```

SHA-256 must equal:

```text
0d9d4c194efda37f100c6183d1a7e88e1a09fe073dc3a37bbb5a3e1cd577e463
```

불일치:

```text
STOP
→ POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

## 5.3 predecessor artifact presence

반드시 존재하고 expected provenance와 충돌하지 않아야 한다.

```text
.aiassistant/tasks/done/
20260829_1026_aiscc-p1-6-checkpoint-human-ingress-and-optional-evidence-design-rework-1.md

.aiassistant/records/aiscc/cycles/
20260829_1026_aiscc-p1-6-checkpoint-human-ingress-and-optional-evidence-hold-1.cycle.md
```

missing/corrupt/conflict:

```text
STOP
→ BLOCKED_MISSING_ARTIFACT
or
→ POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

## 5.4 workspace separation

Stage 0 전부터 존재하는 unrelated dirty path와 이 Task의 intended path를 분리한다.

금지:

- unrelated dirty file reset
- unrelated dirty file staging
- broad staging
- `git add .`
- `git add -A`

Stage 0 exact path allowlist만 index에 올릴 수 있다.

---

# 6. Stage 0 terminal acceptance Cycle

Command Center가 이 Task에서 authoritatively 전달하는 Human result:

```text
Human P1-6 design final review
판정: ACCEPTED
```

새 terminal Cycle path:

```text
.aiassistant/records/aiscc/cycles/
20260829_1241_aiscc-p1-6-evidence-admission-design-final-acceptance-1.cycle.md
```

이 Cycle은 raw report dump가 아니라 다음을 포함하는 curated terminal record로 작성한다.

Required semantic content:

```text
phase:
P1-6 Evidence Admission Design

execution_mode:
MANUAL_COMMAND_CENTER

human result:
HUMAN_PROVIDED / ACCEPTED

accepted design:
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md

accepted design SHA-256:
0d9d4c194efda37f100c6183d1a7e88e1a09fe073dc3a37bbb5a3e1cd577e463

predecessor HOLD:
20260829_1026_aiscc-p1-6-checkpoint-human-ingress-and-optional-evidence-hold-1.cycle.md

final design rework Task:
20260829_1026_aiscc-p1-6-checkpoint-human-ingress-and-optional-evidence-design-rework-1.md

judgment:
P1-6 Evidence Admission Design
→ ACCEPTED / CLOSED

P1-6 Runtime:
NOT_STARTED at judgment time

P1-7:
NOT_STARTED

P1-8:
NOT_STARTED

next action:
P1-6 Evidence Admission Implementation + Runtime Verification
```

Cycle MUST explicitly preserve the accepted narrow rework closures:

```text
1. EvidenceCheckpoint / exact G_EVIDENCE transition-purpose binding
2. checkpoint-specific Requirement applicability
3. pre-P1-7 HUMAN_DIRECT_EVIDENCE ingress
4. removal of first-class OPTIONAL requirement semantics
```

Cycle MUST NOT claim runtime capability exists merely because design was accepted.

---

# 7. Stage 0 canonical state updates

다음 exact paths만 accepted Human decision에 맞게 갱신한다.

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

Required resulting state semantics:

```text
P1-5 Provider / Tool Execution
→ ACCEPTED / CLOSED

P1-6 Evidence Admission Design
→ HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-6 Evidence Admission Runtime
→ NOT_STARTED before Stage 1 begins

P1-7
→ NOT_STARTED

P1-8
→ NOT_STARTED

PUBLIC_BOUNDED_LIVE
→ NOT_RELEASED

current next action
→ P1-6 Evidence Admission Implementation + Runtime Verification
```

`DECISION_REGISTER.md`에는 P1-6 accepted design decision/authority를 기존 register style에 맞게 추가 또는 갱신하되 runtime implementation status를 design acceptance와 혼동하지 않는다.

`NEXT_ACTIONS.md`의 stable queue ordering은 바꾸지 않는다. current action만 P1-6 runtime으로 승격한다.

---

# 8. Stage 0 exact Git persistence

## 8.1 authorization

이 Task는 **Stage 0 terminal persistence에 한해서만** Git index/commit을 명시적으로 허용한다.

Allowed commit content:

```text
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md
.aiassistant/tasks/done/20260829_1026_aiscc-p1-6-checkpoint-human-ingress-and-optional-evidence-design-rework-1.md
.aiassistant/records/aiscc/cycles/20260829_1241_aiscc-p1-6-evidence-admission-design-final-acceptance-1.cycle.md
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

주의:

- accepted design/rework Task가 predecessor HEAD에서 이미 tracked/committed라면 불필요하게 byte를 변경하지 않는다.
- Stage 0 commit은 실제 diff가 있는 accepted terminal persistence path만 포함할 수 있다.
- 그러나 report에는 위 accepted design/rework artifacts가 expected commit ancestry에 존재함을 별도로 검증해 기록한다.
- current active implementation Task는 Stage 0 commit에 넣지 않는다.
- runtime product source는 Stage 0 commit에 절대 포함하지 않는다.

## 8.2 Stage 0 commit message

Exact recommended commit message:

```text
chore(governance): persist accepted P1-6 evidence admission design

Record the Human-accepted P1-6 Evidence Admission design as terminal repository
provenance, update canonical AISCC state, and preserve the accepted design
lineage before any P1-6 runtime implementation begins.
```

## 8.3 forbidden Git actions

Stage 0에서도 금지:

```text
git push
PR create/merge
tag
release
remote mutation
history rewrite
amend predecessor commit
force operation
```

Stage 0 commit 실패 또는 unexpected staged path 존재:

```text
STOP
→ DIRTY_WORKSPACE_MIXED
or
→ COMMAND_PREREQUISITE_REACHED
```

Stage 1을 진행하지 않는다.

---

# 9. Stage 1 accepted evidence profile vocabulary

V1 exact profiles:

```text
EXECUTOR_REQUIRED
REUSE_ALLOWED
HUMAN_OWNED
NOT_REQUIRED
FORBIDDEN
```

No sixth profile.

금지:

```text
OPTIONAL
BEST_EFFORT
INFORMATIONAL_REQUIRED
```

등 first-class authority profile 추가.

Supplemental unrequired material은 필요하면 provenance/candidate metadata로 보존할 수 있으나 다음 authority를 만들지 않는다.

```text
EvidenceRequirement
AdmittedEvidence
EvidenceRequirementSatisfaction
EvidenceSet root contribution
G_EVIDENCE contribution
```

TaskContract가 exact five profiles 중 하나로 명시적으로 승인하지 않은 material은 evidence-set authority가 아니다.

---

# 10. Stage 1 exact domain ownership

P1-6 implementation은 다음 concepts를 구현한다.

```text
EvidenceRequirement
EvidenceRequirementSet

EvidenceCheckpoint
EvidenceCheckpointRef

EvidenceCandidate
EvidenceCandidateRef

EvidenceBodyRef
EvidenceContentRef

EvidenceAdmissionRequest
EvidenceEvaluation
EvidenceAdmissionDecision

AdmittedEvidence
AdmittedEvidenceRef

EvidenceRequirementSatisfaction
EvidenceSetEvaluation
EvidenceSetSatisfactionAttestation

EvidenceRejectionReason
EvidenceOwner
EvidenceSemanticOwner
```

Required non-substitution:

```text
AgentOutput != EvidenceCandidate
P1-5 producer ref != EvidenceCandidate admission
EvidenceCandidate != AdmittedEvidence
AdmittedEvidence != EvidenceSet satisfied
AdmittedEvidenceRef != G_EVIDENCE
EvidenceSetSatisfactionAttestation != TransitionDecision
```

---

# 11. implementation owner root / source layout

Primary new owner root:

```text
src/aiscc/evidence/
```

Preferred module split; existing project conventions may require narrow adaptation, but do not collapse authority boundaries:

```text
src/aiscc/evidence/__init__.py
src/aiscc/evidence/models.py
src/aiscc/evidence/ports.py
src/aiscc/evidence/requirements.py
src/aiscc/evidence/checkpoints.py
src/aiscc/evidence/issuers.py
src/aiscc/evidence/content.py
src/aiscc/evidence/admission.py
src/aiscc/evidence/set_evaluator.py
src/aiscc/evidence/attestation.py
src/aiscc/evidence/events.py
```

Narrow existing integration may touch only when required:

```text
src/aiscc/workflow/**
src/aiscc/persistence/**
src/aiscc/contracts/**
existing Alembic migration location
targeted tests for P1-6 and directly affected P1-3/P1-4/P1-5 behavior
```

Do NOT create:

```text
src/aiscc/human/
src/aiscc/memory/
```

If actual repository structure materially conflicts with this owner split:

```text
STOP
→ POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

Do not create a parallel duplicate architecture.

---

# 12. EvidenceRequirement authority

Every requirement is immutable/versioned and System/TaskContract-owned.

At minimum bind:

```text
requirement_id
requirement_version

TaskContract id/version

semantic owner

exact evidence profile

producer/issuer constraints

content/reference constraints

subject/scope/resource

freshness policy

coverage/completeness rule

reuse policy

sensitivity/export policy

checkpoint applicability
```

Forbidden:

```text
Agent
Executor
public input
```

가 requirement를 add/remove/weaken/reinterpret 하는 것.

New Requirement version MUST NOT silently reinterpret old `AdmittedEvidence`.

---

# 13. EvidenceCheckpoint authority

`EvidenceCheckpoint`는 System/TaskContract-owned immutable/versioned authority다.

At minimum bind:

```text
checkpoint_id
checkpoint_version

TaskContract id/version

source WorkflowState

target WorkflowState
or
exact transition-purpose identity

guard_id:
G_EVIDENCE

RequirementSet id/version

System TaskContract authority version
```

Required invariant:

```text
same WorkRun
same WorkflowState
same state_version
different checkpoint
→ different G_EVIDENCE authority
```

Forbidden:

```text
infer checkpoint only from WorkflowState
caller-supplied arbitrary checkpoint metadata
cross-checkpoint attestation reuse
```

---

# 14. checkpoint-specific Requirement applicability

RequirementSet은 immutable TaskContract snapshot으로 유지할 수 있다.

각 requirement는 exact versioned applicability를 가진다.

Equivalent field:

```text
applicable_checkpoint_refs
```

At checkpoint X:

```text
EvidenceSetEvaluation(X)
→ evaluate all REQUIRED requirements applicable to X
→ evaluate all FORBIDDEN requirements applicable to X
→ obligations not applicable to X do not block completeness
```

Not applicable at checkpoint X:

```text
!= globally rewritten NOT_REQUIRED
```

Pre-Human / Post-Human anti-deadlock semantics를 구현한다.

```text
PRE_HUMAN:
executor/static/runtime requirement applicable
future human final-review requirement not applicable
→ set may become SATISFIED
→ G_EVIDENCE(PRE_HUMAN) may be issued

POST_HUMAN:
human final-review evidence applicable
→ remains UNSATISFIED until Human evidence admitted
```

P1-6 MUST NOT open/resolve `HumanGate`.

---

# 15. HUMAN_OWNED producer split

Exact producer categories:

```text
HUMAN_DIRECT_EVIDENCE
HUMAN_P1_7
```

## 15.1 HUMAN_DIRECT_EVIDENCE

Purpose:

```text
current Manual Command Center Human-provided evidence
before P1-7 runtime exists
```

Must bind:

```text
authenticated Human principal/operator identity
server-issued ingress authority id/version

TaskContract id/version

work_run_id

checkpoint id/version

evidence type

subject/scope/resource

content/ref/hash

provided_at
```

Caller boolean/text MUST NOT assert authenticated Human identity.

Required:

```text
HUMAN_DIRECT_EVIDENCE
!= HumanGate
!= HumanResult
!= Judgment
!= G_HUMAN_*
!= G_JUDGMENT_*
```

Implementation must remain inside P1-6 ingress/issuer/admission boundary.

## 15.2 HUMAN_P1_7

Future owner-produced Human evidence.

If requirement explicitly requires:

```text
HUMAN_P1_7
```

then:

```text
HUMAN_DIRECT_EVIDENCE
→ cannot substitute
```

P1-6 cannot fabricate `HUMAN_P1_7`.

---

# 16. producer / issuer authority

Accepted producer categories include exact equivalents of:

```text
P1-5 ExecutionSubmissionRef
AgentOutputRef
ToolOutputRef
ExecutionArtifactRef

System runtime/static/database proof

HUMAN_DIRECT_EVIDENCE

future HUMAN_P1_7

reused prior AdmittedEvidenceRef
```

Non-authoritative alone:

```text
raw string
raw path
raw hash
raw URL
Executor says PASS
file exists
P1-5 producer ref exists
```

Candidate identity at minimum:

```text
candidate_id

issuer type/id/version

producer work_run / execution_attempt when applicable

TaskContract id/version

checkpoint id/version where applicable

subject/scope/resource

evidence type

content/ref identity

content hash

created/observed time

sensitivity classification
```

---

# 17. content / reference authority

Supported exact equivalents:

```text
immutable inline structured body
content-addressed artifact/blob/file ref
P1-5 immutable producer ref
database/runtime observation ref
Human-provided structured ref
prior AdmittedEvidenceRef reuse candidate
```

Must reject:

```text
unverified arbitrary path
unverified arbitrary URL
mutable latest pointer
hash string without trusted body/ref owner
summary claim when requirement requires exact raw proof
```

Content-addressed evidence verifies:

```text
actual body/bytes
→ canonical hash
→ schema/type/classification
```

Private body may remain private while immutable metadata/hash/ref is durable.

---

# 18. admission evaluation dimensions

Every final candidate evaluation explicitly records decisions for:

```text
REQUIREMENT_MATCH
ISSUER_AUTHORITY
TYPE
TASK_CONTRACT_BINDING
CHECKPOINT_BINDING
SUBJECT_SCOPE
RESOURCE_BINDING
CONTENT_INTEGRITY
SCHEMA_FORMAT
FRESHNESS
APPLICABILITY
COVERAGE
SENSITIVITY_POLICY
REUSE_POLICY
REVOCATION_SUPERSESSION
DUPLICATE_IDEMPOTENCY
```

Unknown/ambiguous:

```text
→ REJECTED
```

No LLM confidence score or free-form reasoning may substitute for these authority dimensions.

---

# 19. admission decisions / rejection taxonomy

Final authoritative outcomes:

```text
ADMITTED
REJECTED
```

`PENDING` may exist only as non-final processing status.

Implement durable sanitized rejection reasons covering at least exact accepted semantics:

```text
UNKNOWN_REQUIREMENT
REQUIREMENT_VERSION_MISMATCH
FORBIDDEN_EVIDENCE
ISSUER_NOT_AUTHORIZED
TASK_CONTRACT_MISMATCH
CHECKPOINT_MISMATCH
SUBJECT_SCOPE_MISMATCH
RESOURCE_MISMATCH
TYPE_MISMATCH
CONTENT_MISSING
CONTENT_HASH_MISMATCH
SCHEMA_INVALID
STALE
NOT_APPLICABLE
INSUFFICIENT_COVERAGE
REUSE_NOT_ALLOWED
REUSE_INCOMPATIBLE
REVOKED_OR_SUPERSEDED
HUMAN_OWNED_REQUIRED
HUMAN_PRODUCER_CATEGORY_MISMATCH
DUPLICATE_IDENTITY_CONFLICT
AUTHORITY_CONFLICT
```

Before freezing enum/source names, exact accepted design source is authoritative if spelling differs.

---

# 20. EvidenceSet completeness

Authority chain:

```text
TaskContract
→ RequirementSet

checkpoint
→ exact applicable subset

AdmittedEvidence
→ exact per-requirement mappings

EvidenceSetEvaluation
→ SATISFIED / UNSATISFIED for checkpoint
```

Required:

```text
missing applicable EXECUTOR_REQUIRED
→ UNSATISFIED

missing applicable HUMAN_OWNED
→ UNSATISFIED

FORBIDDEN candidate
→ rejected
→ satisfies nothing

NOT_REQUIRED
→ creates no required evidence row

REUSE_ALLOWED
→ current-task/current-checkpoint reuse admission still required
```

One evidence item may satisfy multiple requirements only via explicit exact per-requirement coverage mappings.

No hidden fan-out.

---

# 21. G_EVIDENCE owner-bound attestation

P1-6 may issue exact `EvidenceSetSatisfactionAttestation`.

At minimum bind:

```text
attestation id/version

P1-6 authority version

TaskContract id/version

work_run_id

authoritative source WorkflowState/state_version

EvidenceCheckpoint id/version

target state / transition-purpose identity

RequirementSet id/version/root

checkpoint-applicable requirement subset/root

exact admitted-evidence refs/coverage/root

satisfied=true

issued_at / expiry if used
```

P1-4 verifier must reject:

```text
wrong TaskContract
wrong work_run
wrong state/version
wrong checkpoint
wrong source
wrong target/use-purpose
wrong full RequirementSet root
wrong applicable-subset root
stale/superseded admitted evidence
wrong authority version
```

Required:

```text
raw AdmittedEvidence refs
!= G_EVIDENCE

checkpoint A attestation
!= checkpoint B authority
```

P1-6 never decides or mutates workflow transition.

---

# 22. concurrency / idempotency / anti-replay

Admission request binds exact equivalents of:

```text
candidate fingerprint

requirement id/version

checkpoint id/version

TaskContract id/version

work_run_id

RequirementSet version
```

Required behavior:

```text
same request ID + same fingerprint
→ immutable same decision

same request ID + different fingerprint
→ identity conflict

concurrent same logical candidate
→ at most one authoritative admitted identity

stale RequirementSet/TaskContract/checkpoint
→ REJECT
```

Prior `AdmittedEvidence` reuse:

```text
→ new current-task/current-checkpoint admission required
```

Old `G_EVIDENCE` cannot replay across:

```text
new Task
new WorkRun
new state_version
new checkpoint
new RequirementSet version
```

Use PostgreSQL constraints/transactions consistent with the existing persistence architecture.

---

# 23. persistence / revocation / supersession

Persistence direction:

```text
PostgreSQL
append-only provenance
```

Minimum durable concepts:

```text
EvidenceRequirement / RequirementSet snapshot

EvidenceCheckpoint snapshot/ref

EvidenceCandidate

EvidenceAdmissionRequest

EvidenceEvaluation

EvidenceAdmissionDecision

AdmittedEvidence

EvidenceRequirementSatisfaction mapping

EvidenceSetEvaluation

EvidenceSetSatisfactionAttestation

revocation / supersession / correction event
```

Rules:

```text
Admitted body/hash/ref identity
→ immutable

correction
→ old evidence remains historical
→ new candidate
→ new admission
→ explicit correction/supersession relation

revocation/supersession
→ invalidates future/current set satisfaction
→ new attestation cannot rely on invalid evidence

restart
→ deterministic authority reconstruction

corruption/incomplete provenance
→ fail closed
→ no auto repair
```

Schema/migration은 existing P1-5 PostgreSQL/Alembic conventions를 따른다.

새 migration framework를 도입하지 않는다.

---

# 24. freshness / applicability

Freshness는 requirement-owned.

Implement exact equivalents of accepted policy categories:

```text
IMMUTABLE_BUILD_ARTIFACT

TASK_EXECUTION_SCOPED

WORKRUN_STATE_VERSION_SCOPED

TIME_WINDOW

CONFIG_VERSION_SCOPED

HUMAN_RESULT_SCOPED
```

Forbidden:

```text
one global timestamp freshness rule
fresh timestamp == fresh evidence
same immutable bytes == universally applicable
```

---

# 25. security / sensitive evidence

Classification at least:

```text
PUBLIC_SAFE
INTERNAL
PRIVATE_SENSITIVE
SECRET_FORBIDDEN
```

Raw secret MUST NEVER become evidence body.

Secret proof uses non-secret forms such as:

```text
non-secret canary result
redacted metadata
hash/reference
non-exposure proof
```

Public Replay visibility MUST NOT expose private evidence payload merely because immutable metadata exists.

No real credential/provider/network action is required or allowed by this Task.

---

# 26. P1-4 handoff integration

P1-4 workflow contract remains frozen.

Exact WorkflowState set:

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

No state addition/removal/rename.

P1-6 integrates only the `G_EVIDENCE` guard owner boundary.

Required integration proof:

```text
EvidenceSetSatisfactionAttestation
→ P1-4 G_EVIDENCE verifier input

P1-4 verifier
→ validates exact owner-bound attestation bindings

P1-4 TransitionDecision remains P1-4/System-owned
```

P1-6 MUST NOT directly call a workflow-state mutation as evidence admission side effect.

---

# 27. P1-5 handoff integration

P1-5 accepted runtime remains closed.

Producer refs:

```text
AgentOutputRef
ToolOutputRef
ExecutionArtifactRef
ExecutionSubmissionRef
```

Required:

```text
producer ref existence
!= EvidenceCandidate admission
!= AdmittedEvidence
```

P1-5 provider/tool execution behavior is not reopened unless actual repository evidence contradicts accepted baseline.

Real provider calls in this Task:

```text
0
```

Replay provider/tool/process/network/secret execution:

```text
0
```

---

# 28. required implementation proof matrix

The Executor must implement and verify all of the following categories.

```text
NON_SUBSTITUTION

REQUIREMENT_MATCH

ISSUER_CONTENT_AUTHORITY

FRESHNESS_APPLICABILITY

SET_COMPLETENESS

G_EVIDENCE

CHECKPOINT_BINDING

HUMAN_GATE_NON_DEADLOCK

HUMAN_DIRECT_INGRESS

SUPPLEMENTAL_NON_AUTHORITY

CONCURRENCY_IDEMPOTENCY

REUSE_ANTI_REPLAY

REVOCATION_SUPERSESSION

RESTART

SECURITY_EXPORT

P1_4_G_EVIDENCE_HANDOFF
```

---

# 29. mandatory proof cases

At minimum verify:

```text
AgentOutputRef alone
→ not admitted

ExecutionSubmissionRef alone
→ not admitted

raw path/hash/string
→ not admitted

unknown requirement/version
→ rejected

forged issuer
→ rejected

content hash mismatch
→ rejected

state-version scoped stale proof
→ rejected

reuse compatible
→ new current-task admission required

reuse incompatible
→ rejected

one missing applicable required evidence
→ checkpoint UNSATISFIED

all applicable exact requirements satisfied
→ checkpoint SATISFIED

checkpoint A attestation
→ cannot satisfy checkpoint B

same WorkRun/state/version
→ still cannot cross checkpoint

pre-Human checkpoint
→ may satisfy without post-Human Human evidence

post-Human checkpoint
→ human_owned evidence required

forged Human direct identity
→ rejected

HUMAN_DIRECT_EVIDENCE
→ cannot satisfy HUMAN_P1_7-only requirement

supplemental unrequired artifact
→ no AdmittedEvidence
→ no set effect
→ no G_EVIDENCE effect

revoked/superseded evidence
→ old G_EVIDENCE cannot be reused

restart
→ exact authority reconstructed
```

Additional concurrency proof:

```text
same request id + same fingerprint
→ same immutable decision

same request id + different fingerprint
→ conflict

concurrent same logical candidate
→ one authoritative admitted identity
```

---

# 30. evidence contract

## executor_required

### A. STATIC_SOURCE

scope:

```text
P1-6 models / authority boundaries / imports / migration shape /
P1-4 and P1-5 narrow integration
```

pass condition:

- exact five profiles only
- no P1-7/P1-8 authority implementation
- no workflow state/transition expansion
- no arbitrary path/URL trust shortcut
- no direct workflow-state mutation from P1-6
- accepted rejection semantics represented
- diff/check/encoding clean

### B. UNIT_TEST

scope:

```text
requirement/checkpoint matching
issuer authority
content integrity
freshness/applicability
set completeness
attestation binding
human-direct producer split
supplemental non-authority
reuse/revocation semantics
```

pass condition:

- mandatory proof cases applicable at pure-domain level pass
- negative paths are explicit and deterministic

### C. INTEGRATION_TEST

scope:

```text
PostgreSQL persistence
idempotency/concurrency
revocation/supersession
restart reconstruction
P1-4 G_EVIDENCE handoff
P1-5 immutable ref admission boundary
```

pass condition:

- durable authority reconstructs identically after process/repository service reconstruction
- DB constraints prevent duplicate authoritative identities
- invalid/stale/superseded data fails closed
- no blind auto-repair

### D. DATABASE_RUNTIME

Use only the existing local P1-5/P1-3 PostgreSQL/Docker test harness and conventions.

pass condition:

- migration upgrade succeeds from accepted predecessor schema
- targeted persistence/runtime tests pass
- no external DB
- no production/test-server access
- cleanup/residue is reported

If existing local runtime prerequisite is unavailable:

```text
BLOCKED_REQUIRED_EVIDENCE
```

Do not invent a new external environment.

### E. REGRESSION

Run targeted directly affected accepted predecessor suites only.

Must include the repository's existing relevant regression for:

```text
P1-4 workflow / G_EVIDENCE owner boundary
P1-5 persistence/execution ref behavior
P1-3 security/runtime boundary where changed integration touches it
```

Do not run unrelated broad/full suite merely to increase pass count.

### F. SECURITY_EXPORT

Verify:

- no raw secret persisted
- `SECRET_FORBIDDEN` rejected
- private body not exported as public-safe merely due to hash/ref
- rejection/event/report output sanitized
- no credential/network/provider call occurred

### G. RESTART

Explicitly reconstruct evidence authority from durable PostgreSQL state after fresh service/repository object reconstruction.

In-memory object reuse is not restart proof.

## reuse_allowed

Accepted predecessor proof may be reused only for unchanged behavior and exact applicability:

```text
P1-5 terminal runtime baseline
P1-4 accepted transition graph
P1-3 accepted security runtime boundary
```

Reused proof MUST include exact provenance and why current P1-6 changes do not invalidate it.

No predecessor proof may substitute for new P1-6 implementation/runtime proof.

## human_owned

```text
P1-6 runtime final acceptance
business/product acceptance
actual future HumanGate behavior
future P1-7 HumanResult/Judgment
public deployment/release
```

Current Task completion status before Human review:

```text
HUMAN_PENDING
```

Synthetic/local tests of `HUMAN_DIRECT_EVIDENCE` identity authority are executor-required and are NOT a substitute for future Human judgment.

## not_required

```text
browser QA
frontend source test
external HTTP service
real provider API
public deployment
production/test environment observation
competition submission
```

## forbidden

```text
real provider call
credentialed external action
public Live enable/release
P1-7 implementation
P1-8 implementation
workflow-state graph modification
arbitrary shell/network feature exposure
raw-secret evidence body
git push
PR merge
deployment
Stage 1 implementation commit
```

## proof_non_substitution

```text
P1-5 ref != EvidenceCandidate admission
EvidenceCandidate != AdmittedEvidence
AdmittedEvidence != EvidenceSet satisfied
AdmittedEvidenceRef != G_EVIDENCE
EvidenceSetSatisfactionAttestation != TransitionDecision

unit test != PostgreSQL runtime proof
in-memory reconstruction != restart proof
Executor claim != Human acceptance
HUMAN_DIRECT_EVIDENCE != HUMAN_P1_7
Human direct evidence != HumanResult != Judgment
```

---

# 31. allowed scope

## Stage 0 allowed_paths

```text
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md
.aiassistant/tasks/done/20260829_1026_aiscc-p1-6-checkpoint-human-ingress-and-optional-evidence-design-rework-1.md
.aiassistant/records/aiscc/cycles/20260829_1241_aiscc-p1-6-evidence-admission-design-final-acceptance-1.cycle.md
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

Stage 0 only:

```text
exact Git add
exact Git commit
```

## Stage 1 allowed_paths

Primary:

```text
src/aiscc/evidence/**
```

Narrow integration only as required:

```text
src/aiscc/workflow/**
src/aiscc/persistence/**
src/aiscc/contracts/**
existing migration directory
targeted P1-6 tests
directly affected P1-3/P1-4/P1-5 tests
```

Governance/report lifecycle:

```text
.aiassistant/tasks/active/<this-task>
.aiassistant/tasks/done/<this-task>
.aiassistant/reports/target/20260829_1241_aiscc-p1-6-evidence-admission-implementation-and-runtime-verification-1/**
```

No unrelated paths.

---

# 32. forbidden paths / scope

Do not create or modify for feature implementation:

```text
src/aiscc/human/**
src/aiscc/memory/**
```

Do not modify unless exact conflict investigation proves required and Command Center re-authorizes:

```text
product thesis
prior-art baseline
competition public runtime baseline
P1-1 transition graph semantics
P1-2 security policy semantics
P1-5 provider/tool execution semantics
root AGENTS.md
.gitignore
CI/deployment
public UI
```

No broad source-formatting/reorganization.

---

# 33. 읽을 문서 — minimum authoritative context set

Before broad source inspection, explicitly read:

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md

.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/tasks/done/
20260829_1026_aiscc-p1-6-checkpoint-human-ingress-and-optional-evidence-design-rework-1.md

.aiassistant/records/aiscc/cycles/
20260829_1026_aiscc-p1-6-checkpoint-human-ingress-and-optional-evidence-hold-1.cycle.md
```

Then resolve only the exact canonical/source files necessary for:

```text
P1-4 G_EVIDENCE verifier owner
P1-5 immutable producer refs
existing PostgreSQL/Alembic persistence conventions
existing security/runtime integration conventions
```

Do not bulk-read unrelated rules/records/source/logs.

The accepted `AISCC_EVIDENCE_ADMISSION.md` is the final semantic authority for P1-6 if implementation details in old tasks/reports differ.

---

# 34. agent instruction transport / authority

- repository-root instruction entrypoint is thin transport bootstrap, not policy authority.
- Project Rules UI / automatic retrieval does not prove canonical body was loaded.
- Task must-read list is minimum authoritative context set.
- exact paths must be explicitly read.
- active Task, canonical rule, accepted Cycle, source behavior, tests conflict:
  ```text
  STOP
  → POLICY_CONFLICT_INVESTIGATION_REQUIRED
  ```
- do not silently “fix” accepted semantics from general coding preference.
- do not claim human-owned evidence as executor-completed.

---

# 35. implementation sequencing

Required order:

```text
S0-1 repository/HEAD/workspace preflight

S0-2 accepted design hash + predecessor artifact verification

S0-3 terminal acceptance Cycle creation

S0-4 canonical state updates

S0-5 exact diff/encoding/secret check

S0-6 exact Stage 0 Git commit

S0-7 verify commit content and clean separation

ONLY THEN:

S1-1 inspect exact P1-4/P1-5/persistence integration owners

S1-2 domain models + immutable authority objects

S1-3 Requirement / Checkpoint snapshots

S1-4 issuer/content authority

S1-5 admission request/evaluation/decision persistence

S1-6 AdmittedEvidence + requirement satisfaction mapping

S1-7 set evaluator + checkpoint completeness

S1-8 G_EVIDENCE attestation

S1-9 P1-4 verifier integration

S1-10 reuse/idempotency/concurrency/revocation/supersession

S1-11 Human direct ingress authority

S1-12 restart reconstruction

S1-13 targeted verification matrix

S1-14 report/export + current Task active→done
```

Do not begin Stage 1 before Stage 0 commit exists.

---

# 36. mandatory stop conditions

Stop implementation on:

```text
BLOCKED_PREDECESSOR_HEAD_DRIFT

accepted design SHA mismatch

missing accepted rework Task/HOLD Cycle

policy/source/test conflict

unexpected staged/unrelated dirty collision

Stage 0 commit failure

new external runtime/network/credential requirement

P1-7/P1-8 authority required to proceed

need to change accepted WorkflowState/transition graph

need to weaken five-profile model

need to trust arbitrary path/URL/hash without accepted authority

evidence persistence integrity cannot be made fail-closed

EVIDENCE_SCOPE_EXPANSION_REQUIRED

SECURITY_BOUNDARY_BLOCKED
```

After named blocker:

- capture minimum evidence
- record workspace inventory
- produce report/export
- perform safe cleanup only
- do not continue unrelated implementation/testing

---

# 37. workflow transition expectation

```text
initial project phase:
P1-6 design Human-accepted / terminal persistence pending

Stage 0 terminal result:
P1-6 Evidence Admission Design
→ ACCEPTED / CLOSED in repository canonical provenance

Stage 1 runtime result:
implementation candidate only

human pending after executor completion:
P1-6 runtime final review

transition_authority:
SYSTEM

Agent direct terminal authority:
No
```

This MANUAL_COMMAND_CENTER Task does not claim AISCC self-dogfooding runtime.

---

# 38. conformance reporting

```text
applicability:
REQUIRED

applicable policy/invariant:
accepted AISCC_EVIDENCE_ADMISSION contract

required_actual_owner:
P1-6_EVIDENCE

planned_vs_actual_scope:
must be reported exactly

rollback_or_failure_semantics:
fail closed; Stage 0 commit remains durable even if Stage 1 fails
```

Important failure separation:

```text
Stage 0 accepted design commit succeeds
+ Stage 1 implementation fails
→ DO NOT roll back accepted design terminal persistence
→ report implementation failure/rework separately
```

---

# 39. project context impact

architecture:

```text
NONE unless actual accepted source conflict discovered
```

orchestration_contract:

```text
NARROW_INTEGRATION_ONLY
P1-4 state/transition semantics frozen
```

security_sandbox:

```text
NARROW_INTEGRATION_ONLY
no new public capability
```

public_provenance:

```text
CANONICAL_UPDATE_REQUIRED for Stage 0
TASK_AND_CYCLE_ONLY / candidate source for Stage 1
```

P1-7:

```text
MUST REMAIN NOT_STARTED
```

P1-8:

```text
MUST REMAIN NOT_STARTED
```

PUBLIC_BOUNDED_LIVE:

```text
MUST REMAIN NOT_RELEASED
```

---

# 40. accept 기준 — Executor candidate

Executor submission is a valid review candidate only if all are true:

## Stage 0

- actual start HEAD exactly matched expected predecessor.
- accepted design SHA exactly matched.
- predecessor artifacts were present.
- terminal acceptance Cycle was created.
- three canonical state files were updated consistently.
- Stage 0 exact commit succeeded.
- no runtime implementation path was included in Stage 0 commit.
- commit hash/path set is reported.

## Stage 1

- exact five profiles only.
- checkpoint-specific applicability implemented.
- `HUMAN_DIRECT_EVIDENCE != HUMAN_P1_7`.
- supplemental unrequired material has zero admitted/set/G_EVIDENCE authority.
- evidence admission dimensions fail closed.
- PostgreSQL durable provenance exists.
- concurrency/idempotency/anti-replay proven.
- revocation/supersession invalidates future/current satisfaction.
- restart reconstructs exact authority.
- `EvidenceSetSatisfactionAttestation` is checkpoint/state/version/use-purpose-bound.
- P1-4 validates attestation without P1-6 owning transition.
- mandatory proof matrix passes.
- directly affected predecessor regressions pass.
- no real provider/network/credential action.
- no P1-7/P1-8 implementation.
- no implementation commit.
- target bundle complete.
- Task moved active→done only after executor turn/report/export complete.

Final P1-6 runtime acceptance remains Human/Command Center-owned.

---

# 41. hold/reject 기준

HOLD/REJECT candidate if any:

```text
Stage 0 predecessor mismatch ignored

accepted design changed without new Human decision

runtime source mixed into design terminal commit

new evidence profile added

OPTIONAL restored as first-class requirement authority

AgentOutput/P1-5 ref auto-admitted

raw path/hash/URL trusted as evidence

single admitted item treated as set satisfaction

checkpoint applicability inferred only from WorkflowState

cross-checkpoint G_EVIDENCE reuse accepted

HUMAN_DIRECT_EVIDENCE treated as HUMAN_P1_7

caller asserted Human identity accepted

supplemental artifact contributes to G_EVIDENCE

revoked/superseded evidence remains valid for new attestation

restart relies on in-memory state

P1-6 directly mutates WorkflowState/TransitionDecision

P1-7/P1-8 implementation added

raw secret persisted/exported

real provider call executed

Stage 1 implementation committed

required runtime/concurrency/restart proof missing
```

---

# 42. report 필수 항목

`EXECUTOR_REPORT.md` must include:

1. task/work type/task path
2. read canonical paths
3. automatically discovered instruction inventory
4. explicit tool-read inventory
5. repository/branch/start HEAD
6. workspace before
7. accepted design hash actual/expected
8. predecessor artifact verification
9. Stage 0 changed files
10. Stage 0 exact staged path list
11. Stage 0 commit hash
12. Stage 0 commit file list
13. Stage 0 post-commit HEAD
14. Stage 1 source inventory
15. product source changes
16. governance/provenance changes
17. repository configuration changes
18. migration/schema changes
19. Task evidence contract
20. actual evidence classification
21. mandatory proof matrix result — each category
22. test commands and exact pass/fail counts
23. PostgreSQL/runtime version actually used
24. restart proof method/result
25. concurrency/idempotency proof method/result
26. P1-4 G_EVIDENCE handoff proof
27. P1-5 ref non-substitution proof
28. Human direct ingress authority proof
29. supplemental non-authority proof
30. security/export result
31. real provider calls: exact count, expected `0`
32. network/credential actions: expected `none`
33. P1-7/P1-8 source creation: expected `none`
34. Stage 1 Git commit: expected `none`
35. Agent claims vs admitted evidence distinction
36. human pending/provided
37. mandatory stop/scope expansion
38. planned-vs-actual conformance
39. unverified items
40. rollback/revert guide
41. UTF-8/Markdown/control-character validation
42. workspace after
43. preserved artifact exact paths
44. next turn recommendation

---

# 43. export bundle

Target:

```text
.aiassistant/reports/target/
20260829_1241_aiscc-p1-6-evidence-admission-implementation-and-runtime-verification-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
```

Also include:

- all Stage 0 changed governance/provenance files preserving project-relative paths
- all Stage 1 changed product source/test/migration files preserving project-relative paths
- `REMOVED_FILES.md` only if deletion exists

Do not include:

- secrets
- credentials
- private env
- DB dumps
- build/cache
- previous target bundles
- unchanged broad source
- generated runtime residue

---

# 44. Task lifecycle

Initial local placement:

```text
.aiassistant/tasks/active/
20260829_1241_aiscc-p1-6-evidence-admission-implementation-and-runtime-verification-1.md
```

After executor-required implementation/report/export is complete or a named blocker safely terminates the turn:

```text
.aiassistant/tasks/done/
20260829_1241_aiscc-p1-6-evidence-admission-implementation-and-runtime-verification-1.md
```

`done` means executor submission ready.

It does NOT mean:

```text
P1-6 runtime ACCEPTED
Human final review complete
P1-7 started
```

Current Task moving to `done` is not authorized to be committed in Stage 1.

---

# 45. preserved exact paths

Must survive cleanup:

```text
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md

.aiassistant/tasks/done/
20260829_1026_aiscc-p1-6-checkpoint-human-ingress-and-optional-evidence-design-rework-1.md

.aiassistant/records/aiscc/cycles/
20260829_1026_aiscc-p1-6-checkpoint-human-ingress-and-optional-evidence-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260829_1241_aiscc-p1-6-evidence-admission-design-final-acceptance-1.cycle.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/tasks/done/
20260829_1241_aiscc-p1-6-evidence-admission-implementation-and-runtime-verification-1.md
```

Stage 1 implementation/test/migration source changes are review candidate files and must remain in the working tree until Command Center judgment.

Temporary target bundle is review input and may be deleted after judgment unless later explicitly preserved.

---

# 46. 사람 검증 요구

Executor turn 종료 시:

```text
P1-6 runtime final acceptance:
HUMAN_PENDING
```

Human/Command Center must review:

- target bundle
- Stage 0 commit provenance
- Stage 1 changed source
- proof matrix
- runtime/concurrency/restart evidence
- P1-4 handoff integrity
- security/export boundary

Executor MUST NOT write:

```text
P1-6 runtime ACCEPTED
P1-7 ready/started
```

as terminal truth.

---

# 47. 최종 응답 형식

1. result: `completed / blocked / rejected-candidate`
2. Stage 0 start HEAD
3. accepted design SHA verification
4. Stage 0 commit hash
5. Stage 0 committed exact paths
6. target bundle path
7. Stage 1 changed files
8. removed files
9. verification summary
10. real provider calls count
11. human verification: `HUMAN_PENDING`
12. unverified items
13. preserved exact paths
14. next recommendation

장문 report 전문은 chat에 붙이지 않는다.
