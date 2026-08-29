# AI Software Command Center — P1-6 Design Accepted Command Center Handoff

## 0. purpose

이 문서는 Browser Command Center 세션을 새 채팅으로 이주하기 위한 durable handoff다.

새 채팅은 다음을 사용할 수 없다고 가정한다.

```text
이전 Browser 채팅 memory/context:
사용 불가

File Library:
사용 불가

GPT Project Source:
사용 불가

이전 첨부 ZIP:
사용 불가
```

새 채팅은 아래 두 가지를 authority로 사용한다.

```text
1. local repository canonical files
2. this handoff document
```

Browser chat 자체는 canonical source가 아니다.

---

# 1. repository / project identity

```text
project:
AI Software Command Center

repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

remote:
https://github.com/jihyeongshin/ai-software-command-center.git

branch:
main
```

Competition:

```text
Wanted AI Championship 2026
deadline:
2026-09-20
```

Core product thesis:

```text
AISCC is a Software Engineering Governance Control Plane,
not a generic coding agent.

Task
→ Evidence
→ Judgment
→ Cycle
→ Next Action
```

Core orchestration:

```text
direct explicit state machine
LangGraph core:
NOT USED
```

---

# 2. non-substitution invariants

These are load-bearing and must not be weakened.

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

Terminal authority remains:

```text
TERMINAL_TRANSITION
→ SYSTEM_ADMISSION
→ HUMAN_GATE_WHEN_REQUIRED
```

---

# 3. current phase state

As of Human review on 2026-08-29:

```text
P0-1
→ ACCEPTED / CLOSED

P0-2
→ ACCEPTED / CLOSED

P0-3
→ HUMAN_CONFIRMED / CLOSED

P0-4
→ ACCEPTED / CLOSED

P0-5
→ ACCEPTED / CLOSED

P1-1 Explicit State Machine Contract
→ ACCEPTED / CLOSED

P1-2 Security / Sandbox Runtime Boundary
→ ACCEPTED / CLOSED

P1-3 Runtime Substrate + Security Safeguard
→ ACCEPTED / CLOSED

P1-4 Explicit State Machine Kernel
→ ACCEPTED / CLOSED

P1-5 Provider / Tool Execution Design
→ HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-5 Provider / Tool Execution Runtime
→ HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-6 Evidence Admission Design
→ HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-6 Evidence Admission Runtime
→ NOT_STARTED

P1-7 Human Gate and Judgment
→ NOT_STARTED

P1-8 Project Memory and Cycle Admission
→ NOT_STARTED

PUBLIC_BOUNDED_LIVE
→ NOT_RELEASED
```

Current next phase:

```text
P1-6 Evidence Admission Implementation + Runtime Verification
```

---

# 4. current Git provenance

Important lineage:

```text
P1-4 terminal acceptance:
d99ccc4ecde585685e93960a7fa39ecbfde89f9f

P1-5 design HOLD provenance:
d96949f3643e6a0610942e33d70e9da259e1e432

P1-5 terminal design + initial runtime base:
3b150181f1c008d0b95fd53a32cb6e62d174ab4f

P1-5 runtime integration HOLD provenance:
3312e24b60e0bd10b7c859546d6fdfa3bd2cb025

P1-5 bounds/public-context HOLD provenance:
d652f01c1c76a9c2ed3c550a7fab6b8414b59c07

P1-5 token-accounting HOLD provenance:
15036a5ff316fccbd6d891b9ce43563de056e342

P1-5 terminal runtime acceptance + P1-6 design base:
bd5611f3c1c3307e8f3f5d4ab39768fd69566b57

P1-6 design HOLD provenance:
c86e291f94bd9acc31e40bc78316132abfddd90b
```

Expected repository HEAD at handoff:

```text
c86e291f94bd9acc31e40bc78316132abfddd90b
```

The new Command Center MUST verify the actual local HEAD before any mutation.

If HEAD differs:

```text
STOP
→ BLOCKED_PREDECESSOR_HEAD_DRIFT
```

Do not guess which later commit is correct.

---

# 5. P1-4 authoritative workflow kernel — frozen

Exact `WorkflowState` set:

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

Exact 22 transitions:

```text
NONE → READY

READY → RUNNING

RUNNING → ADMISSION_PENDING
RUNNING → BLOCKED
RUNNING → REWORK_REQUIRED
RUNNING → FAILED

ADMISSION_PENDING → HUMAN_REQUIRED
ADMISSION_PENDING → BLOCKED
ADMISSION_PENDING → REWORK_REQUIRED
ADMISSION_PENDING → ACCEPTED
ADMISSION_PENDING → REJECTED

HUMAN_REQUIRED → ACCEPTED
HUMAN_REQUIRED → REWORK_REQUIRED
HUMAN_REQUIRED → REJECTED
HUMAN_REQUIRED → BLOCKED

BLOCKED → READY
BLOCKED → HUMAN_REQUIRED
BLOCKED → REWORK_REQUIRED
BLOCKED → FAILED

REWORK_REQUIRED → READY
REWORK_REQUIRED → HUMAN_REQUIRED
REWORK_REQUIRED → REJECTED
```

Terminal:

```text
ACCEPTED
REJECTED
FAILED
→ no outgoing transition
```

Guard owners include:

```text
G_EVIDENCE
→ future owner P1_6_EVIDENCE
```

P1-6 may produce only the exact owner-bound evidence guard fact.
P1-6 cannot mint:

```text
G_CURRENT
G_HUMAN_*
G_JUDGMENT_*
TransitionDecision
WorkflowState
```

---

# 6. P1-5 accepted runtime baseline

Final P1-5 candidate:

```text
42 paths

aggregate SHA-256:
ffeb5ba70649c564c482c2cff79ce8e2b0a462f811d8e03f2c1096f170bd39d6
```

P1-5 Human final review:

```text
Human P1-5 runtime final review
판정: ACCEPTED
```

Final admitted verification:

```text
unit + integration:
145 PASS

P1-5 persistence/accounting:
23 PASS

P1-5 runtime:
10 PASS

P1-3 Docker runtime regression:
10 PASS

PostgreSQL:
17.6

Alembic:
20260828_0002

OpenAI Python SDK:
3.5.0

real provider calls:
0

final Task-owned residue:
0
```

Accepted P1-5 execution properties:

```text
PostgreSQL durable ExecutionAttempt / ExecutionOperation / events

ExecutionStatus:
NOT_STARTED
RUNNING
EXECUTOR_COMPLETED
EXECUTION_FAILED

restart-durable provider/round/tool/retry/time/output/budget bounds

per-side-effect WorkRun/state_version freshness

P1-3 PROVIDER / TOOL / SECRET capability mediation

consumed-authority SecretResolutionLease

exact Tool ResourceRequirement binding

OpenAI Responses V1:
background=false
stream=false
store=false
parallel_tool_calls=false
truncation=disabled

conversation:
omitted

previous_response_id:
omitted

AISCC durable local private protocol history:
sole continuation authority

unknown provider/tool outcome:
no blind retry

missing provider usage:
request max_output_tokens M charged in full

reported output_tokens N:
exact integer
0 <= N <= M

Replay:
provider/tool/process/network/secret execution exactly zero

PUBLIC_BOUNDED_LIVE local proof:
fixed synthetic repository/version + scenario + server-owned provider/tool config

PUBLIC_BOUNDED_LIVE release:
NOT_RELEASED
```

P1-5 handoff to P1-6:

```text
AgentOutputRef
ToolOutputRef
ExecutionArtifactRef
ExecutionSubmissionRef

!= EvidenceCandidate admission
!= AdmittedEvidence
```

---

# 7. P1-6 accepted design identity

Human final review:

```text
Human P1-6 design final review
판정: ACCEPTED
```

Canonical design path:

```text
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md
```

Accepted final design SHA-256:

```text
0d9d4c194efda37f100c6183d1a7e88e1a09fe073dc3a37bbb5a3e1cd577e463
```

The design became accepted after narrow rework that closed:

```text
1. EvidenceCheckpoint / exact G_EVIDENCE transition-purpose binding
2. checkpoint-specific Requirement applicability
3. pre-P1-7 HUMAN_DIRECT_EVIDENCE ingress
4. removal of first-class OPTIONAL requirement semantics
```

P1-6 runtime/source implementation has NOT started.

---

# 8. P1-6 exact evidence profile vocabulary

V1 evidence profiles are exactly:

```text
EXECUTOR_REQUIRED
REUSE_ALLOWED
HUMAN_OWNED
NOT_REQUIRED
FORBIDDEN
```

No sixth evidence profile exists.

First-class `OPTIONAL` requirement semantics are NOT allowed.

Supplemental unrequired material may be retained only as:

```text
supplemental candidate / provenance
```

It must NOT create:

```text
EvidenceRequirement
AdmittedEvidence
EvidenceRequirementSatisfaction
EvidenceSet root contribution
G_EVIDENCE contribution
```

unless a current TaskContract explicitly authorizes it under one of the exact five profiles.

---

# 9. P1-6 exact domain model to implement

The accepted design freezes concepts equivalent to:

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

Non-substitution:

```text
AgentOutput != EvidenceCandidate

P1-5 producer ref != EvidenceCandidate admission

EvidenceCandidate != AdmittedEvidence

AdmittedEvidence != EvidenceSet satisfied

AdmittedEvidenceRef != G_EVIDENCE

EvidenceSetSatisfactionAttestation != TransitionDecision
```

---

# 10. EvidenceRequirement authority

Every requirement is immutable/versioned and System/TaskContract-owned.

At minimum it binds:

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

Agent/Executor/public input cannot:

```text
add
remove
weaken
reinterpret
```

requirements.

A new Requirement version does not silently reinterpret old AdmittedEvidence.

---

# 11. EvidenceCheckpoint authority

This is a critical accepted rework.

`EvidenceCheckpoint` is System/TaskContract-owned.

At minimum it binds:

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

Checkpoint is not arbitrary caller metadata.

Required invariant:

```text
same WorkRun
same WorkflowState
same state_version
different checkpoint
→ different G_EVIDENCE authority
```

No implicit convention like:

```text
infer checkpoint only from WorkflowState
```

is authoritative.

---

# 12. checkpoint-specific requirement applicability

The full RequirementSet may remain one immutable TaskContract snapshot.

Every requirement has exact versioned applicability equivalent to:

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

A requirement not applicable at checkpoint X is NOT globally rewritten to `NOT_REQUIRED`.

Human-gate anti-deadlock example:

```text
TaskContract:
executor_required static/runtime proof
human_owned final review

PRE_HUMAN checkpoint:
executor proof applicable
human final review not yet applicable

→ set may become SATISFIED
→ G_EVIDENCE(PRE_HUMAN) may be issued

P1-7 Human handling occurs separately

POST_HUMAN checkpoint:
human final-review evidence applicable and required

→ remains UNSATISFIED until Human evidence is admitted
```

P1-6 does not open or resolve HumanGate.

---

# 13. HUMAN_OWNED accepted producer split

Two distinct Human evidence producer categories are frozen.

```text
HUMAN_DIRECT_EVIDENCE

HUMAN_P1_7
```

## HUMAN_DIRECT_EVIDENCE

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

P1-6 still performs all normal evidence admission checks.

Required non-substitution:

```text
HUMAN_DIRECT_EVIDENCE
!= HumanGate
!= HumanResult
!= Judgment
!= G_HUMAN_*
!= G_JUDGMENT_*
```

The Human identity cannot be asserted by caller boolean/text.

## HUMAN_P1_7

Future P1-7 owner-produced Human evidence.

If a requirement explicitly requires `HUMAN_P1_7`:

```text
HUMAN_DIRECT_EVIDENCE
→ cannot substitute
```

P1-6 cannot fabricate either producer identity.

---

# 14. producer / issuer authority

Candidates may originate from exact producer categories including:

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

But:

```text
raw string/path/hash/URL
!= trusted producer

Executor says PASS
!= trusted evidence

file exists
!= content admitted

P1-5 producer ref exists
!= AdmittedEvidence
```

Candidate identity must bind at minimum:

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

# 15. content / reference authority

P1-6 may support:

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

Private body may stay private while immutable metadata/hash/ref becomes durable.

---

# 16. admission evaluation dimensions

Every candidate evaluation explicitly decides:

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

No LLM confidence score may substitute for authority dimensions.

---

# 17. admission decisions / rejection taxonomy

Authoritative outcomes:

```text
ADMITTED
REJECTED
```

`PENDING` may exist only as processing status, not final admission authority.

The accepted design contains durable sanitized rejection reasons covering at least:

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

Exact source names may be checked from the canonical design before implementation.

---

# 18. evidence-set completeness

A single admitted item never means the evidence gate is satisfied.

Authority:

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

Rules:

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
→ current-task reuse admission still required
```

One evidence item may satisfy multiple requirements only through explicit exact per-requirement
coverage mappings.

No hidden fan-out.

---

# 19. G_EVIDENCE owner-bound attestation

P1-6 may issue an exact `EvidenceSetSatisfactionAttestation`.

At minimum it binds:

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

Raw AdmittedEvidence refs do NOT satisfy `G_EVIDENCE`.

An attestation for checkpoint A cannot satisfy checkpoint B.

P1-6 never decides or mutates the workflow transition.

---

# 20. reuse / concurrency / anti-replay

Admission request binds exact:

```text
candidate fingerprint

requirement id/version

checkpoint id/version

TaskContract id/version

work_run_id

RequirementSet version
```

Same request ID + same fingerprint:

```text
→ immutable same decision
```

Same ID + different fingerprint:

```text
→ identity conflict
```

Concurrent same logical candidate:

```text
→ at most one authoritative admitted identity
```

Stale RequirementSet/TaskContract/checkpoint:

```text
→ REJECT
```

Prior AdmittedEvidence reuse requires a new current-task/current-checkpoint admission.

Old G_EVIDENCE attestation cannot be replayed for:

```text
new Task
new WorkRun
new state_version
new checkpoint
new requirement-set version
```

---

# 21. persistence / revocation / supersession

Next implementation direction is PostgreSQL, append-only provenance.

Minimum durable entities:

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

Admitted body/hash/ref identity is immutable.

Correction:

```text
old evidence remains historical

new candidate
→ new admission

explicit correction/supersession relation
```

Revocation/supersession invalidates future/current set satisfaction before a new attestation may be
issued.

Restart reconstructs the same authority deterministically.

Corruption/incomplete provenance:

```text
→ fail closed
→ no auto repair
```

---

# 22. freshness / applicability

Freshness is requirement-owned.

Expected policy categories include exact equivalents of:

```text
IMMUTABLE_BUILD_ARTIFACT

TASK_EXECUTION_SCOPED

WORKRUN_STATE_VERSION_SCOPED

TIME_WINDOW

CONFIG_VERSION_SCOPED

HUMAN_RESULT_SCOPED
```

Do not use one global timestamp freshness rule.

Required:

```text
fresh timestamp
!= fresh evidence

same immutable bytes
!= applicable if scope/version/checkpoint changed
```

---

# 23. security / sensitive evidence

Evidence classification must distinguish at least:

```text
PUBLIC_SAFE
INTERNAL
PRIVATE_SENSITIVE
SECRET_FORBIDDEN
```

Raw secrets are never admitted as evidence bodies.

Secret proof uses:

```text
non-secret canary result
redacted metadata
hash/reference
non-exposure proof
```

Private evidence payload is not exposed merely because a public Replay is visible.

---

# 24. implementation ownership for P1-6

Expected new owner root:

```text
src/aiscc/evidence/
```

Expected components:

```text
models.py
ports.py
requirements.py
checkpoints.py
issuers.py
content.py
admission.py
set_evaluator.py
attestation.py
events.py
```

Exact filenames are not yet canonical unless the implementation Task freezes them.

Narrow existing integration may touch:

```text
src/aiscc/workflow/**
src/aiscc/persistence/**
src/aiscc/contracts/**
```

Only for P1-6 handoff.

Do NOT create:

```text
src/aiscc/human/
src/aiscc/memory/
```

P1-7 / P1-8 own those phases.

---

# 25. required P1-6 implementation proof matrix

The implementation Task must preserve and execute at least:

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

Important mandatory proofs:

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

---

# 26. immediate next action in the new chat

The new Browser Command Center must NOT directly start source implementation.

First action:

```text
Human P1-6 design acceptance
→ terminal canonical persistence
→ exact design commit
→ issue P1-6 Evidence Admission Implementation + Runtime Verification Task
```

Required first-turn sequence:

```text
1. verify repository HEAD == c86e291f94bd9acc31e40bc78316132abfddd90b

2. verify:
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md

SHA-256:
0d9d4c194efda37f100c6183d1a7e88e1a09fe073dc3a37bbb5a3e1cd577e463

3. create P1-6 design final acceptance Cycle

4. update canonical:
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

5. prepare exact local terminal persistence / repo-root placement packet

6. issue:
P1-6 Evidence Admission Implementation + Runtime Verification Task

7. that Task Stage 0 must Git-persist:
- accepted AISCC_EVIDENCE_ADMISSION.md
- final P1-6 design rework done Task
- terminal P1-6 design Cycle
- updated canonical state

8. only after that exact commit may Executor implement P1-6 runtime

9. P1-7 remains NOT_STARTED
```

Do not silently combine P1-6 runtime implementation with P1-7.

---

# 27. terminal P1-6 design acceptance still needs canonical persistence

Human acceptance exists in Browser chat:

```text
Human P1-6 design final review
판정: ACCEPTED
```

But as of this handoff, do NOT assume the repository already contains:

```text
P1-6 design terminal acceptance Cycle
updated P1-6 ACCEPTED canonical state
accepted design commit
```

These are the new Command Center's first canonicalization action.

This distinction is critical:

```text
Human accepted in chat
!= repository terminal persistence completed
```

---

# 28. known latest P1-6 artifacts

Latest accepted candidate path:

```text
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md
```

Accepted SHA:

```text
0d9d4c194efda37f100c6183d1a7e88e1a09fe073dc3a37bbb5a3e1cd577e463
```

Latest rework Task:

```text
.aiassistant/tasks/done/
20260829_1026_aiscc-p1-6-checkpoint-human-ingress-and-optional-evidence-design-rework-1.md
```

Latest HOLD Cycle:

```text
.aiassistant/records/aiscc/cycles/
20260829_1026_aiscc-p1-6-checkpoint-human-ingress-and-optional-evidence-hold-1.cycle.md
```

Historical predecessor design SHA:

```text
9b72dc3a5a5ed8b554cc3af4fd22bd2b720e6d93c34cb54381b8462038b6ac4a
```

Accepted rework design SHA:

```text
0d9d4c194efda37f100c6183d1a7e88e1a09fe073dc3a37bbb5a3e1cd577e463
```

---

# 29. preserved durable artifacts

The following must survive cleanup.

## commits

```text
d99ccc4ecde585685e93960a7fa39ecbfde89f9f
d96949f3643e6a0610942e33d70e9da259e1e432
3b150181f1c008d0b95fd53a32cb6e62d174ab4f
3312e24b60e0bd10b7c859546d6fdfa3bd2cb025
d652f01c1c76a9c2ed3c550a7fab6b8414b59c07
15036a5ff316fccbd6d891b9ce43563de056e342
bd5611f3c1c3307e8f3f5d4ab39768fd69566b57
c86e291f94bd9acc31e40bc78316132abfddd90b
```

## canonical / task / cycle paths

```text
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md

.aiassistant/tasks/done/
20260829_1026_aiscc-p1-6-checkpoint-human-ingress-and-optional-evidence-design-rework-1.md

.aiassistant/records/aiscc/cycles/
20260829_1026_aiscc-p1-6-checkpoint-human-ingress-and-optional-evidence-hold-1.cycle.md
```

Also preserve all accepted P1-5 runtime candidate paths represented by:

```text
42 paths
ffeb5ba70649c564c482c2cff79ce8e2b0a462f811d8e03f2c1096f170bd39d6
```

---

# 30. workflow / Git safety rules

Tracked durable categories:

```text
.aiassistant/rules/**
.aiassistant/records/command-center/**
.aiassistant/records/aiscc/**
.aiassistant/tasks/done/**
.aiassistant/reports/aiscc/**
.aiassistant/project-sources/PROJECT_SOURCE_BUNDLE_REGISTRY.md
.aiassistant/project-sources/manifests/**
```

Ignored/ephemeral:

```text
.idea/
.aiassistant/bootstrap-input/
.aiassistant/tasks/active/
.aiassistant/reports/target/
.aiassistant/project-sources/bundles/
```

Task lifecycle:

```text
tasks/active
→ tasks/done
```

`done` means Executor submitted, not Human accepted.

Each timestamped Task normally starts in a new Codex conversation.

No `git add .` or broad accidental staging in provenance-controlled Tasks.

Human acceptance / terminal persistence / implementation candidate commits must remain explicitly
separated when the Task says so.

---

# 31. next-session BOOTSTRAP SHORT

Copy this text into the new Browser Command Center chat together with this handoff file.

```text
AI Software Command Center Browser Command Center handoff다.

첨부된 handoff markdown을 먼저 전체 읽고, 그 문서를 이번 새 세션의 bootstrap authority로 사용하라.

새 세션에서는 이전 Browser 채팅 memory, File Library, GPT Project Source 접근이 없다고 가정한다.
repository canonical + handoff 문서만 authority다.

Repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

Expected HEAD:
c86e291f94bd9acc31e40bc78316132abfddd90b

Current phase state:
P1-5 Provider / Tool Execution → ACCEPTED / CLOSED
P1-6 Evidence Admission Design → Human final ACCEPTED
P1-6 Runtime → NOT_STARTED
P1-7 → NOT_STARTED
PUBLIC_BOUNDED_LIVE → NOT_RELEASED

Accepted P1-6 design:
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md

SHA-256:
0d9d4c194efda37f100c6183d1a7e88e1a09fe073dc3a37bbb5a3e1cd577e463

Human final decision:
Human P1-6 design final review
판정: ACCEPTED

중요:
Human acceptance는 Browser chat에서 발생했지만 아직 repository terminal persistence가 완료됐다고 가정하지 마라.

첫 작업:
1. actual HEAD 검증
2. accepted design SHA 검증
3. P1-6 design terminal acceptance Cycle 생성
4. CURRENT_STATE_SUMMARY / DECISION_REGISTER / NEXT_ACTIONS 갱신
5. exact terminal persistence / placement packet 생성
6. P1-6 Evidence Admission Implementation + Runtime Verification Task 발행

그 implementation Task Stage 0에서 accepted AISCC_EVIDENCE_ADMISSION.md + final rework done Task + terminal Cycle + canonical state를 exact commit한 뒤에만 source 구현을 허용하라.

P1-6 accepted contract에서 반드시 유지:
- exact five profiles:
  EXECUTOR_REQUIRED / REUSE_ALLOWED / HUMAN_OWNED / NOT_REQUIRED / FORBIDDEN
- EvidenceCheckpoint / transition-purpose-bound G_EVIDENCE
- checkpoint-specific requirement applicability
- HUMAN_DIRECT_EVIDENCE != HUMAN_P1_7
- Human direct evidence != HumanResult != Judgment
- supplemental unrequired material has no AdmittedEvidence/G_EVIDENCE authority
- EvidenceCandidate != AdmittedEvidence
- prior AdmittedEvidence reuse requires current-task/checkpoint admission
- revocation/supersession invalidates future set satisfaction
- P1-6 cannot mint P1-4/P1-7 authority other than exact G_EVIDENCE fact
- P1-7/P1-8 must remain NOT_STARTED during P1-6 implementation

Do not re-open accepted P1-5 unless actual repository evidence contradicts the handoff.
```

---

# 32. handoff judgment

Session decision:

```text
CURRENT CHAT:
CLOSE after this handoff

NEXT CHAT:
NEW Browser Command Center session
```

Reason:

```text
phase boundary:
P1-6 design → P1-6 runtime

current chat:
contains long P1-5/P1-6 design and repeated rework history

new chat:
reduces predecessor/candidate/hash confusion
and makes P1-6 implementation the single active concern
```

The next session should begin by terminally persisting the already Human-accepted P1-6 design, not by
re-litigating the design.
