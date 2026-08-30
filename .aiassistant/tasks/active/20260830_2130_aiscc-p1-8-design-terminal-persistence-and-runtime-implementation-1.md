# 작업지시서: P1-8 Design Terminal Persistence + Runtime Implementation

## meta

- task_id: `20260830_2130_aiscc-p1-8-design-terminal-persistence-and-runtime-implementation-1`
- created_at: `2026-08-30T21:30:00+09:00`
- phase: `P1-8 Project Memory and Cycle Admission`
- work_type: `DESIGN_TERMINAL_PERSISTENCE_AND_RUNTIME_IMPLEMENTATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1_8_PROJECT_MEMORY_CYCLE`
- expected_start_head: `4b84a9f66c148b198d3f4b6b01cffc4641fdceb1`
- accepted_design_path: `.aiassistant/rules/AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md`
- accepted_design_sha256: `100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a`
- human_final_design_review: `HUMAN_PROVIDED / ACCEPTED`
- predecessor_p1_7_runtime_commit: `b4ba49ebaeb437d885bf22d52473c7d8a79832d1`
- predecessor_p1_7_terminal_governance_commit: `abd5228f5d1338aa820298cc76eaf7db82b0ce4f`
- predecessor_p1_7_handoff_correction_commit: `4b84a9f66c148b198d3f4b6b01cffc4641fdceb1`
- predecessor_p1_7_runtime_aggregate_sha256: `1933e0451d101b142e099cc987babb426f87422d15338775d9d87bbf29fa2f90`
- p1_8_design_status: `HUMAN_PROVIDED / ACCEPTED`
- p1_8_runtime_status_before_task: `NOT_STARTED`
- p2_status: `NOT_STARTED`
- public_bounded_live: `NOT_RELEASED`

---

# 1. Human final design judgment

Human review is complete.

Exact Human decision:

```text
Human P1-8 design final review
판정: ACCEPTED
```

Do not ask for design acceptance again.

Do not reinterpret the accepted design.

The exact accepted design bytes are:

```text
.aiassistant/rules/AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md

SHA-256:
100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a
```

The design file itself must not be edited to change `HUMAN_PENDING` metadata or wording before Stage 0A.
Human acceptance is terminal provenance outside the immutable accepted design bytes.

---

# 2. task objective

This Task has three strictly ordered stages.

```text
Stage 0A
→ persist the exact Human-accepted P1-8 design bytes as one design commit

Stage 0B
→ persist Human acceptance, full P1-8 design HOLD/task lineage, and canonical state
   in a separate governance commit that references the actual Stage 0A commit

Stage 1
→ implement the accepted P1-8 runtime
→ produce an uncommitted runtime candidate
→ Human runtime acceptance remains pending
```

Do not combine stages.

Do not amend prior commits.

Do not commit Stage 1 runtime candidate.

---

# 3. mandatory preflight

Before any mutation or Git index action:

## 3.1 HEAD

Require:

```text
HEAD ==
4b84a9f66c148b198d3f4b6b01cffc4641fdceb1
```

Mismatch:

```text
STOP
→ REVIEWED_BASELINE_DRIFT
```

No reset, rebase, checkout overwrite, clean, or amend.

## 3.2 accepted design

Require:

```text
sha256(.aiassistant/rules/AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md)
==
100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a
```

Mismatch:

```text
STOP
→ ACCEPTED_DESIGN_DRIFT
```

## 3.3 accepted P1-7 handoff

Require:

```text
sha256(
.aiassistant/reports/aiscc/
20260830_1712_aiscc-p1-7-runtime-accepted-p1-8-command-center-handoff-1.md
)
==
0169b07642e72d1c7025c98946402e53102c3de2f72a4b3df78ba0ed851004c5
```

Require inherited guards remain exact:

```text
P1_7_HUMAN:
8

P1_7_JUDGMENT:
3

G_SUSPENDED_HUMAN_GATE:
present

G_RESUMABLE_HUMAN_GATE:
present
```

Mismatch:

```text
STOP
→ P1_7_HANDOFF_PROVENANCE_DRIFT
```

## 3.4 workspace

Record:

```text
git status --short
git diff --name-only
git diff --cached --name-only
```

Index must be empty.

Expected tracked design diff before Stage 0A:

```text
.aiassistant/rules/AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md
```

Expected P1-8 design governance lineage may also be uncommitted and is reserved for Stage 0B.

Any unrelated tracked dirty path:

```text
STOP
→ DIRTY_WORKSPACE_MIXED
```

Never use:

```text
git add .
git add -A
git reset
git clean
```

---

# 4. frozen predecessor authority

P1-8 implementation must consume, not duplicate or weaken:

```text
P1-4:
TransitionRequest / TransitionEvaluation / TransitionDecision
WorkflowState / state_version
canonical durable WorkRun history

P1-6:
EvidenceCandidate / AdmittedEvidence
EvidenceSetSatisfactionAttestation
projection-independent historical evidence provenance
current-effectiveness separation
G_EVIDENCE

P1-7:
HumanGate / HumanResult
Judgment
historical producer/Judgment/evidence provenance
G_HUMAN_*
G_JUDGMENT_*
```

Mandatory non-substitution remains:

```text
CycleAdmissionDecision != Judgment
CycleAdmissionDecision != TransitionDecision
AdmittedCycle != CommandCenterCycleRecord
ProjectMemoryEntry != canonical rule
ProjectMemoryEntry != TaskContract
MemoryRetrievalResult != AdmittedEvidence
MemoryRetrievalResult != Judgment
NextActionProposal != NextActionSelection
NextActionSelection != TransitionDecision
TaskIssuanceCandidate != TaskContract
```

P1-8 must not mint:

```text
WorkflowState
TransitionDecision
G_EVIDENCE
G_HUMAN_*
G_JUDGMENT_*
HumanResult
Judgment
```

---

# 5. Stage 0A — exact accepted design commit

Stage exactly one path:

```text
.aiassistant/rules/AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md
```

Before commit verify:

```text
git diff --cached --name-only
```

equals exactly that one path.

Verify staged blob SHA-256:

```text
100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a
```

No other path may be staged.

Recommended exact commit message:

```text
docs(design): freeze P1-8 project memory and cycle admission

Freeze the Human-accepted P1-8 design for accepted-only Cycle admission,
curated project-memory projection, append-only applicability, deterministic
retrieval, enrolled Next Action selection, and historical/current authority
separation without changing P1-4, P1-6, or P1-7 ownership.
```

Create Stage 0A commit.

Record:

```text
P1_8_DESIGN_ACCEPTANCE_COMMIT=<40-char SHA>
```

Verify:

```text
parent ==
4b84a9f66c148b198d3f4b6b01cffc4641fdceb1

changed paths ==
exactly 1

design blob SHA ==
100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a
```

Do not amend Stage 0A.

---

# 6. Stage 0B — design terminal governance persistence

Only begin after Stage 0A commit SHA is known and verified.

## 6.1 create design final acceptance Cycle

Create:

```text
.aiassistant/records/aiscc/cycles/
20260830_2130_aiscc-p1-8-project-memory-and-cycle-admission-design-final-acceptance-1.cycle.md
```

It must contain actual immutable values:

```text
Human review:
HUMAN_PROVIDED / ACCEPTED

accepted design commit:
<exact P1_8_DESIGN_ACCEPTANCE_COMMIT>

accepted design SHA:
100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a

P1-7 predecessor terminal:
4b84a9f66c148b198d3f4b6b01cffc4641fdceb1

P1-8 Design:
ACCEPTED / CLOSED

P1-8 Runtime:
NOT_STARTED / IMPLEMENTATION_AUTHORIZED

P2:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

Record the design review lineage:

```text
1909 initial design candidate

1933 HOLD:
memory source-to-content authority
memory lineage/correction authority
NextAction eligibility authority

2011 HOLD:
historical source provenance
vs current source/memory applicability

2011 HOLD:
historical policy/descriptor validity
vs current policy/catalog applicability
```

Record all three HOLD findings as CLOSED by the Human-accepted final design.

No placeholder commit IDs.

## 6.2 persist design Task/HOLD lineage

Stage 0B must preserve exact existing artifacts:

### design Tasks

```text
.aiassistant/tasks/done/
20260830_1909_aiscc-p1-8-project-memory-and-cycle-admission-design-1.md

.aiassistant/tasks/done/
20260830_1933_aiscc-p1-8-memory-authority-lineage-and-next-action-eligibility-design-rework-1.md

.aiassistant/tasks/done/
20260830_2011_aiscc-p1-8-historical-source-and-current-applicability-separation-design-rework-1.md

.aiassistant/tasks/done/
20260830_2011_aiscc-p1-8-historical-policy-and-current-policy-separation-design-rework-1.md
```

### design HOLD Cycles

```text
.aiassistant/records/aiscc/cycles/
20260830_1933_aiscc-p1-8-design-memory-authority-lineage-next-action-eligibility-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260830_2011_aiscc-p1-8-design-historical-source-current-applicability-separation-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260830_2011_aiscc-p1-8-design-historical-policy-current-policy-separation-hold-1.cycle.md
```

Do not rewrite historical HOLD artifacts.

## 6.3 canonical state

Update exactly:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

Required state:

```text
P1-7
→ HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-8 Design
→ HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-8 accepted design commit
→ <exact P1_8_DESIGN_ACCEPTANCE_COMMIT>

P1-8 accepted design SHA
→ 100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a

P1-8 Runtime
→ NOT_STARTED / IMPLEMENTATION_AUTHORIZED

P2
→ NOT_STARTED

PUBLIC_BOUNDED_LIVE
→ NOT_RELEASED
```

`NEXT_ACTIONS.md` must point to:

```text
P1-8 Runtime Implementation
```

No P2 start.

## 6.4 current Task provenance

Stage this Task at its active path:

```text
.aiassistant/tasks/active/
20260830_2130_aiscc-p1-8-design-terminal-persistence-and-runtime-implementation-1.md
```

The Task remains active because Stage 1 continues after Stage 0B.

## 6.5 exact Stage 0B allowlist

Stage exactly 12 paths:

```text
4 prior done design Tasks
3 prior HOLD Cycles
1 new final acceptance Cycle
3 canonical state files
1 current active Task
```

No design rule file: it already belongs to Stage 0A.

No runtime source/test/migration.

No target bundle.

Before commit:

```text
git diff --cached --name-only
```

must equal exact 12-path allowlist.

Recommended exact commit message:

```text
chore(governance): accept P1-8 design and authorize runtime

Record the Human final acceptance of the P1-8 Project Memory and Cycle Admission
design, preserve its complete design-review provenance, and advance the canonical
next action to P1-8 runtime implementation without starting P2 or Public Live.
```

Create Stage 0B commit.

Record:

```text
P1_8_DESIGN_TERMINAL_GOVERNANCE_COMMIT=<40-char SHA>
```

Verify first-parent lineage:

```text
4b84a9f66c148b198d3f4b6b01cffc4641fdceb1
→ P1_8_DESIGN_ACCEPTANCE_COMMIT
→ P1_8_DESIGN_TERMINAL_GOVERNANCE_COMMIT
```

Do not amend either commit.

---

# 7. Stage 1 — runtime implementation authority

Only start runtime mutation after Stage 0A/0B verification succeeds.

The accepted design is now the sole P1-8 semantic baseline.

Stage 1 output:

```text
P1-8 runtime candidate
→ uncommitted
→ Executor-completed only
→ Human runtime acceptance pending
```

No Stage 1 `git add`, commit, push, or deployment.

---

# 8. exact V1 runtime scope

Implement all accepted V1 runtime authority required to realize:

```text
Task
→ Evidence
→ Judgment
→ AdmittedCycle
→ ProjectMemory
→ NextActionSelection
```

without creating Task authority.

## 8.1 Cycle domain

Implement exact semantic equivalents of:

```text
CycleCandidate
CycleAdmissionRequest
CycleEvaluation
CycleAdmissionDecision
AdmittedCycle
CycleAuthorityEvent
```

Required:

```text
accepted terminal only

exact TaskContract/WorkRun/Judgment/TransitionDecision binding

required P1-6 historical attestation/root binding

historical source provenance
!= current source effectiveness

CycleAdmissionDecision
!= Judgment
!= TransitionDecision
```

`CommandCenterCycleRecord` remains repository governance only.

No Markdown file may mint runtime Cycle authority.

## 8.2 Memory domain

Implement exact semantic equivalents of:

```text
MemoryDeclaration
MemoryDeclarationAuthorityPolicy
ProjectMemoryEntry
ProjectMemoryEntryId
MemoryLineageKey
CycleMemoryReference
ProjectMemoryAuthorityEvent
ProjectMemoryView
MemoryRetrievalResult
```

Required V1 policies:

```text
accepted Cycle deterministic projection only

LESSON
→ NOT_SUPPORTED

one CURRENT tip per MemoryLineageKey

EXPLICIT_SUPERSESSION_ONLY

caller mutation intent
!= correction/supersession/revocation authority

direct ProjectMemory write
→ forbidden
```

## 8.3 Next Action domain

Implement exact semantic equivalents of:

```text
NextActionProposal
ActionRef
NextActionDescriptor
NextActionEligibilityPolicy
NextActionSelectionPolicy
NextActionEvaluation
NextActionSelection
NextActionAuthorityEvent
TaskIssuanceCandidate
```

Required:

```text
P1-8 System-owned deterministic selection

current enrolled descriptor eligibility
→ before ranking

proposal claims
→ non-authoritative

NextActionSelection
!= TransitionDecision

TaskIssuanceCandidate
!= TaskContract

Task authority
→ EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY
```

Implement both accepted modes:

```text
OPERATIONAL_RECOVERY
CYCLE_DERIVED
```

`CYCLE_DERIVED` may use only `CURRENT` ProjectMemory.

---

# 9. MemoryDeclaration source authority

Implement immutable/versioned:

```text
MemoryDeclarationAuthorityPolicy
```

with exact accepted authority modes:

```text
DETERMINISTIC_POINTER
STRUCTURED_RESULT_ATTESTED
OWNER_ATTESTED
NOT_SUPPORTED
```

V1 category behavior must match accepted design exactly.

At minimum:

```text
LESSON
→ NOT_SUPPORTED
```

No caller-authored semantic inference.

For every declaration:

```text
resolve exact policy

resolve exact immutable source

derive/reconstruct canonical content

recompute MCF_V1

declaration fingerprint == expected fingerprint
```

Negative:

```text
accepted WorkRun + valid source ref + unrelated structured content
→ fail closed
```

---

# 10. historical source / current applicability split

For `STRUCTURED_RESULT_ATTESTED`, consume accepted P1-6 projection-independent historical provenance.

Historical source proof must include exact equivalents of:

```text
EvidenceRequirement ref/fingerprint
EvidenceCheckpoint ref/fingerprint
EvidenceSetSatisfactionAttestation ref/version/root
AdmittedEvidence complete historical issuance
EvidenceContentRef schema/canonicalization/hash
exact terminal Judgment/TransitionDecision binding
```

Do not require current P1-6 effectiveness for historical Cycle identity.

Required cases:

```text
valid at terminal + current
→ Cycle ADMITTED
→ memory CURRENT

valid at terminal + later revoked/superseded/expired
→ same historical Cycle/entry
→ memory non-CURRENT
→ default retrieval excluded

invalid at terminal
or not in exact consumed attestation/root
→ Cycle rejected
```

Delayed admission of already non-current source must have:

```text
zero externally visible temporary CURRENT state
```

---

# 11. historical policy / current policy split

Implement durable owner-event histories for:

```text
MemoryDeclarationAuthorityPolicy

NextActionEligibilityPolicy
NextActionSelectionPolicy
NextActionDescriptor
```

New Cycle/new NextAction selection:

```text
current eligible policy/descriptor required
```

Historical replay:

```text
exact immutable policy/descriptor version
+ as-of-original-issuance validity
required

currentness now
NOT required
```

Later policy/descriptor supersession/revocation:

```text
immutable old Cycle/entry/selection
→ preserved

current projection/future eligibility
→ append-only update
```

Historical corruption and ordinary current staleness must use distinct typed errors.

---

# 12. stable memory lineage and mutation authority

Implement exact deterministic versioned `MemoryLineageKey`.

Required properties:

```text
stable across Cycles

does not contain:
cycle_id
content_fingerprint

contains exact semantic slot identity

same category/subject
!= same lineage automatically
```

V1:

```text
0..1 CURRENT tip per MemoryLineageKey
```

Use:

```text
lineage advisory lock
expected lineage revision
database unique current-tip constraint
```

Different-content replacement requires exact accepted authority:

```text
SOURCE_OWNER_AUTHORITY_EVENT

or

TASK_AUTHORITY_STRUCTURED_MEMORY_DIRECTIVE
```

P1-8 deterministic applicability policy may handle:

```text
expiry
same-content replay/CycleMemoryReference
```

but must not invent different-content correction authority.

---

# 13. deterministic retrieval

Implement structured deterministic retrieval only.

Required query dimensions:

```text
project
scope
MemoryLineageKey/semantic slot
category allowlist
current-only / authorized historical
as-of revision/event sequence
privacy clearance
limit
```

Default:

```text
current-only = true
```

Exact ordering must match accepted design.

No embedding/vector/LLM relevance in authority path.

Historical result must be visibly marked:

```text
NOT_CURRENT_CONTEXT
```

when non-current.

---

# 14. Next Action eligibility and deterministic selection

## 14.1 action catalog

`NextActionEligibilityPolicy` owns exact enrolled descriptors.

Proposal may only:

```text
nominate exact ActionRef
provide allowed parameters
provide non-authoritative rationale
```

Proposal cannot:

```text
define action
change priority
claim authoritative security/blocker/baseline rank
change Task owner
bypass Human requirement
```

Novel action:

```text
NEXT_ACTION_ACTION_NOT_ENROLLED
```

## 14.2 authoritative ranking inputs

Resolve priority only from accepted authoritative sources:

```text
selection policy
current P1-4 blocker/failure refs
current P1-7 Judgment where applicable
enrolled canonical baseline/roadmap/critical-path ref/hash/ordinal
CURRENT ProjectMemory contextual refs
```

Caller priority claims are ignored.

Implement exact deterministic ranking tuple from accepted design.

## 14.3 current/historical separation

New selection:

```text
current policies + current descriptor
```

Historical replay:

```text
exact original policy/descriptor/enrollment
+ as-of-issuance validity
```

Later current invalidation:

```text
append-only NextActionAuthorityEvent
→ current selection non-current
```

No old selection rewrite.

---

# 15. Task issuance boundary

Implement:

```text
NextActionSelection
→ TaskIssuanceCandidate
```

Do NOT implement:

```text
runtime TaskContract issuer
automatic TaskContract creation
automatic WorkRun creation
```

`TaskIssuanceCandidate` is non-authoritative.

Exact owner label/contract:

```text
EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY
```

A later issued TaskContract may be linked append-only, but P1-8 cannot mint it.

---

# 16. PostgreSQL persistence

Use PostgreSQL durable authority.

Create the next exact Alembic migration after:

```text
20260829_0004
```

Recommended migration:

```text
20260830_0005_p1_8_project_memory_cycle_admission.py
```

If repository migration naming rules require a different timestamp while preserving linear ancestry, report the
exact chosen revision and reason.

Durable logical storage must cover accepted design §14:

```text
cycle candidates/requests/evaluations/decisions
admitted cycles
cycle authority events

memory declaration policies + owner events
project memory entries
cycle-memory references
memory authority events
current memory projection

NextAction eligibility/selection policies
descriptors + owner events
proposals/evaluations/selections
NextAction authority events
current NextAction projection
```

No in-memory-only authority.

---

# 17. fingerprint / canonicalization

Use one explicit versioned canonical serializer contract.

Required deterministic fingerprints include at minimum:

```text
CycleCandidate / request / evaluation / decision / admitted payload

MemoryDeclarationAuthorityPolicy

MCF_V1 memory content

MemoryLineageKey serialization

ProjectMemoryEntry

ProjectMemoryAuthorityEvent

NextActionEligibilityPolicy
NextActionSelectionPolicy
NextActionDescriptor
NextActionProposal
NextActionEvaluation
NextActionSelection
TaskIssuanceCandidate
```

Current applicability/current catalog revisions must not pollute immutable historical identities.

Add fixed test vectors.

---

# 18. concurrency / lock ordering

Implement accepted exact lock order:

```text
1. P1-4 WorkRun row FOR UPDATE
2. cycle/request global identity advisory locks, lexical
3. terminal epoch advisory lock
4. project-memory scope advisory lock
5. affected MemoryLineageKeys, lexical byte order
6. project NextAction projection lock only when applicable
```

V1 operation may not span two WorkRuns or two project scopes in one transaction.

Required concurrency proofs:

```text
same Cycle request/id
same terminal epoch
same MemoryLineageKey successor
same NextAction selection/project revision
```

No last-write-wins.

Typed stale/conflict results.

---

# 19. append-only correction / projection rebuild

Never update/delete immutable:

```text
AdmittedCycle
CycleAdmissionDecision
ProjectMemoryEntry
NextActionSelection
```

Use append-only:

```text
CycleAuthorityEvent
ProjectMemoryAuthorityEvent
NextActionAuthorityEvent
```

Projection tables are rebuildable caches, not authority.

Restart must reconstruct exact:

```text
historical Cycle identities
historical source/policy validity
current memory tips/applicability
historical NextAction selections
current NextAction projection
```

Corruption/mismatch:

```text
fail closed
no auto repair
```

---

# 20. privacy / export

Implement accepted classes:

```text
PRIVATE_INTERNAL
PUBLIC_SANITIZED
NON_EXPORTABLE
```

Do not admit/export:

```text
credentials
secrets
raw prompts/chat
private Human identity
hidden chain-of-thought
unrestricted logs
```

`PUBLIC_SANITIZED` requires versioned allowlist/export policy.

Runtime Cycle/Memory admission must not make a private source publicly readable.

---

# 21. expected source layout

Prefer clear owner packages.

Recommended:

```text
src/aiscc/cycle/**
src/aiscc/memory/**
src/aiscc/next_action/**
```

Shared integration may touch narrowly:

```text
src/aiscc/persistence/models.py
src/aiscc/persistence/repository.py
src/aiscc/persistence/ports.py

src/aiscc/workflow/**
src/aiscc/evidence/**
src/aiscc/human/**
src/aiscc/judgment/**
```

Predecessor packages should normally be consumed, not semantically modified.

If a predecessor package needs a projection-independent read helper, add the narrowest owner-side helper and
prove no semantic change.

Do not copy P1-4/P1-6/P1-7 authority logic into P1-8.

---

# 22. required tests

## 22.1 unit

At minimum:

```text
canonical fingerprint test vectors

Cycle/Memory/NextAction model validation

MemoryLineageKey normalization

MCF_V1

LESSON NOT_SUPPORTED

ActionRef/descriptor parameter schema

deterministic ranking/tie-break
```

## 22.2 PostgreSQL integration — Cycle

Prove:

```text
accepted exact terminal lineage
→ ADMITTED

REJECTED/HOLD/FAILED/BLOCKED/rework
→ no AdmittedCycle

foreign TaskContract/WorkRun/Judgment/TransitionDecision
→ fail closed

historical P1-6 source valid
→ admitted

source not in exact terminal consumed root
→ rejected

source invalid at terminal
→ rejected

source valid at terminal then later current-stale
→ same historical replay identity
```

## 22.3 PostgreSQL integration — memory

Prove:

```text
accepted source ref + unrelated caller content
→ reject

LESSON
→ NOT_SUPPORTED

direct memory write
→ forbidden

same-content cross-Cycle
→ CycleMemoryReference where accepted

different semantic slot
→ different lineage

unauthorized correction/supersession/revocation
→ reject

explicit authorized supersession
→ old historical entry preserved
→ one new CURRENT tip

already-revoked source at delayed admission
→ no temporary CURRENT visibility

source invalidation after admission
→ append-only applicability change
→ immutable Cycle/entry unchanged

memory policy v1 valid at admission
→ v2 later current
→ historical replay same identity
→ new v1 admission rejected
```

## 22.4 PostgreSQL integration — retrieval

Prove deterministic ordering/as-of.

Default retrieval excludes:

```text
SUPERSEDED
REVOKED
EXPIRED
```

Historical authorized mode returns state/reason.

Projection rebuild returns byte-equivalent ordered refs.

## 22.5 PostgreSQL integration — Next Action

Prove:

```text
arbitrary proposal action
→ NOT_ENROLLED

caller priority/security/blocker claim
→ ignored / cannot elevate

eligible ActionRef + valid parameters
→ ranking allowed

BEFORE_SELECTION Human input missing
→ HUMAN_INPUT_REQUIRED
→ no Selection

OPERATIONAL_RECOVERY
→ source-domain operational facts
→ no ProjectMemory admission requirement

CYCLE_DERIVED
→ CURRENT ProjectMemory only

NextAction policy/descriptor v1 valid at issuance
→ v2 later current
→ historical replay same selection
→ new old-v1 selection rejected

append-only current selection withdrawal
→ old selection preserved

TaskIssuanceCandidate created
→ no TaskContract minted
```

## 22.6 concurrency

Fresh concurrent PostgreSQL tests:

```text
same request
same Cycle ID
same terminal epoch
same MemoryLineageKey successor
same project NextAction revision
```

Expected:

```text
one winner
same-proposal replay
or typed conflict

no duplicate current tips
no duplicate current selections
```

## 22.7 restart / corruption

Prove:

```text
restart replay

projection rebuild

missing source row

fingerprint corruption

policy owner-event gap/duplicate

memory applicability event gap/duplicate

multiple current tips

NextAction owner-event corruption

historical policy/source as-of mismatch
```

All fail closed where authority is corrupt.

---

# 23. predecessor regressions

Mandatory regression suites must preserve:

```text
P1-4 state/transition persistence and history

P1-6 evidence admission/current/historical provenance

P1-7 HumanGate/HumanResult/Judgment/current/historical authority
```

At minimum rerun the established P1-4/P1-6/P1-7 PostgreSQL regression groups plus full unit/integration suite.

No behavior change is accepted merely because P1-8 tests pass.

---

# 24. runtime non-goals / forbidden implementation

Do not implement:

```text
P2 UI

P2 Self-Dogfooding cutover

P3 public deployment/release

vector database / embeddings / RAG authority path

automatic free-form skill generation

canonical rule mutation from memory

runtime TaskContract issuer

multi-agent memory voting

provider/model fine-tuning
```

No external provider call, credentialed network, IdP, deployment, Public Live.

---

# 25. mandatory STOP conditions

STOP with exact typed report on:

```text
Stage 0A accepted design SHA mismatch

Stage 0B terminal governance staged-set mismatch

predecessor P1-4/P1-6/P1-7 semantic change required

accepted design cannot be implemented from durable predecessor provenance

TaskContract runtime issuance must be invented to complete P1-8

historical source/policy validity cannot be reconstructed from existing durable predecessor data

migration requires destructive predecessor schema rewrite

unrelated dirty workspace collision

P2/P3 scope becomes necessary
```

Use:

```text
POLICY_BASELINE_GAP
POLICY_CONFLICT_INVESTIGATION_REQUIRED
IMPLEMENTATION_BASELINE_GAP
```

as appropriate.

Do not silently weaken the design.

---

# 26. Git policy after Stage 0B

Once Stage 0B is committed:

```text
NO further git add
NO runtime commit
NO push
```

Runtime candidate remains working-tree only.

Do not amend:

```text
P1_8_DESIGN_ACCEPTANCE_COMMIT
P1_8_DESIGN_TERMINAL_GOVERNANCE_COMMIT
```

At Task completion move:

```text
.aiassistant/tasks/active/
20260830_2130_aiscc-p1-8-design-terminal-persistence-and-runtime-implementation-1.md

→

.aiassistant/tasks/done/
20260830_2130_aiscc-p1-8-design-terminal-persistence-and-runtime-implementation-1.md
```

That lifecycle move belongs to the uncommitted runtime candidate review set.

---

# 27. evidence contract

## executor_required

### DESIGN_TERMINAL_GIT

```text
Stage 0A exact accepted design commit
Stage 0B exact terminal governance commit
first-parent lineage
no amend
```

### STATIC_SOURCE

```text
ruff
mypy src
```

### P1_8_CYCLE

```text
accepted terminal admission
excluded outcomes
predecessor exact bindings
idempotency/concurrency
historical replay
```

### P1_8_MEMORY

```text
source-to-content authority
LESSON exclusion
lineage/current tip
explicit supersession
current/historical applicability
deterministic retrieval
```

### P1_8_NEXT_ACTION

```text
descriptor enrollment
eligibility before ranking
System deterministic selection
current/historical policy separation
TaskIssuanceCandidate boundary
```

### POSTGRESQL

```text
fresh migration
constraints
transactions
locks
restart
projection rebuild
corruption fail-closed
```

### PREDECESSOR_REGRESSION

```text
P1-4
P1-6
P1-7
```

### SECURITY_EXPORT

```text
privacy/export
secret-pattern scan without values
actual exported byte hashes
```

## human_owned

```text
P1-8 runtime final acceptance
→ HUMAN_PENDING
```

Executor must not mark runtime `ACCEPTED`.

## forbidden

```text
provider
external IdP
credentialed network
deployment
Public Live
P2/P3
```

---

# 28. runtime candidate export

Target:

```text
.aiassistant/reports/target/
20260830_2130_aiscc-p1-8-design-terminal-persistence-and-runtime-implementation-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
```

Include byte-preserving copies of all Stage 1 changed:

```text
runtime source
migration
tests
Task done lifecycle path
```

Also include read-only copies sufficient to review terminal provenance:

```text
P1-8 design final acceptance Cycle
CURRENT_STATE_SUMMARY.md
DECISION_REGISTER.md
NEXT_ACTIONS.md
```

Do not include secrets.

Manifest must report:

```text
start HEAD
Stage 0A SHA
Stage 0B SHA
final HEAD
accepted design SHA
runtime changed-path count
per-file SHA-256
runtime aggregate SHA-256
source/copy identity
Git status/index
```

Runtime aggregate algorithm:

```text
sort repository-relative Stage 1 runtime/test/migration paths ordinally

serialize:
<path>\t<lowercase_sha256>\n

SHA-256 concatenated UTF-8 bytes
```

Governance Task lifecycle file may be reported separately and must not be mixed into the runtime aggregate.

---

# 29. Executor report required fields

Report exact:

1. Task path
2. start HEAD
3. accepted design SHA verification
4. corrected P1-7 handoff SHA verification
5. preflight status/index inventory
6. Stage 0A staged path set
7. Stage 0A design blob SHA
8. Stage 0A commit SHA
9. Stage 0A parent
10. design final acceptance Cycle path
11. Human acceptance recorded
12. design HOLD/task lineage persisted
13. canonical state update
14. Stage 0B exact 12-path staged set
15. Stage 0B commit SHA
16. Stage 0B parent
17. Stage 0A→0B lineage
18. Stage 1 migration revision
19. exact runtime packages/files changed
20. exact domain object/API inventory
21. Cycle admission transaction
22. accepted terminal binding
23. historical source/current applicability split
24. memory declaration authority implementation
25. MemoryLineageKey/current-tip implementation
26. correction/supersession/revocation authority
27. retrieval implementation
28. historical memory-policy replay
29. NextAction descriptor/eligibility implementation
30. deterministic ranking
31. historical NextAction policy/descriptor replay
32. TaskIssuanceCandidate external-owner boundary
33. concurrency/lock order evidence
34. restart/projection rebuild evidence
35. corruption fail-closed evidence
36. privacy/export evidence
37. P1-4 regression
38. P1-6 regression
39. P1-7 regression
40. full unit/integration count
41. PostgreSQL version
42. Alembic revision
43. ruff
44. mypy
45. provider/network/credential/deployment actions
46. runtime path count
47. runtime aggregate SHA-256
48. Stage 1 Git actions = none
49. final HEAD
50. final index status
51. P1-8 runtime Human verification = HUMAN_PENDING
52. P2 = NOT_STARTED
53. PUBLIC_BOUNDED_LIVE = NOT_RELEASED
54. preserved exact paths
55. next recommendation

---

# 30. expected successful submission state

```text
P1-7:
ACCEPTED / CLOSED

P1-8 Design:
HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-8 Runtime:
EXECUTOR_COMPLETED / HUMAN_PENDING

P2:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

Command Center next:

```text
review exact P1-8 runtime candidate

→ PASS / HUMAN_FINAL_REVIEW_REQUIRED
or
→ HOLD_REWORK_REQUIRED
```

No runtime terminal commit before Human acceptance.

---

# 31. preserved exact paths

After successful submission, explicitly preserve:

```text
.aiassistant/rules/
AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md

.aiassistant/records/aiscc/cycles/
20260830_1933_aiscc-p1-8-design-memory-authority-lineage-next-action-eligibility-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260830_2011_aiscc-p1-8-design-historical-source-current-applicability-separation-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260830_2011_aiscc-p1-8-design-historical-policy-current-policy-separation-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260830_2130_aiscc-p1-8-project-memory-and-cycle-admission-design-final-acceptance-1.cycle.md

.aiassistant/tasks/done/
20260830_1909_aiscc-p1-8-project-memory-and-cycle-admission-design-1.md

.aiassistant/tasks/done/
20260830_1933_aiscc-p1-8-memory-authority-lineage-and-next-action-eligibility-design-rework-1.md

.aiassistant/tasks/done/
20260830_2011_aiscc-p1-8-historical-source-and-current-applicability-separation-design-rework-1.md

.aiassistant/tasks/done/
20260830_2011_aiscc-p1-8-historical-policy-and-current-policy-separation-design-rework-1.md

.aiassistant/tasks/done/
20260830_2130_aiscc-p1-8-design-terminal-persistence-and-runtime-implementation-1.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

The target export bundle is review-only and deletable after Command Center judgment unless explicitly preserved
later.
