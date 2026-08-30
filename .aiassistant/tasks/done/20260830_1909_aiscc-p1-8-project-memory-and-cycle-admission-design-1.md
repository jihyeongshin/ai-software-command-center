# 작업지시서: P1-8 Project Memory and Cycle Admission Design

## meta

- task_id: `20260830_1909_aiscc-p1-8-project-memory-and-cycle-admission-design-1`
- created_at: `2026-08-30T19:09:00+09:00`
- phase: `P1-8 Project Memory and Cycle Admission`
- work_type: `DESIGN_AUDIT`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1_8_PROJECT_MEMORY_CYCLE`
- expected_start_head: `4b84a9f66c148b198d3f4b6b01cffc4641fdceb1`
- predecessor_p1_7_runtime_commit: `b4ba49ebaeb437d885bf22d52473c7d8a79832d1`
- predecessor_p1_7_terminal_governance_commit: `abd5228f5d1338aa820298cc76eaf7db82b0ce4f`
- predecessor_p1_7_handoff_correction_commit: `4b84a9f66c148b198d3f4b6b01cffc4641fdceb1`
- predecessor_p1_7_runtime_aggregate_sha256: `1933e0451d101b142e099cc987babb426f87422d15338775d9d87bbf29fa2f90`
- corrected_p1_8_handoff_sha256: `0169b07642e72d1c7025c98946402e53102c3de2f72a4b3df78ba0ed851004c5`
- p1_7_status: `HUMAN_PROVIDED / ACCEPTED / CLOSED`
- p1_8_status_before_task: `NOT_STARTED`
- public_bounded_live: `NOT_RELEASED`

---

# 1. current authority state

The P1-7 terminal lineage is accepted and corrected.

Exact lineage:

```text
P1-7 design terminal parent:
c87cfc75f14476e10b4a02a2ab0bd295720a85a0

P1-7 accepted runtime Commit A:
b4ba49ebaeb437d885bf22d52473c7d8a79832d1

P1-7 terminal governance Commit B:
abd5228f5d1338aa820298cc76eaf7db82b0ce4f

P1-7 handoff provenance correction Commit C:
4b84a9f66c148b198d3f4b6b01cffc4641fdceb1
```

P1-7 Runtime:

```text
HUMAN_PROVIDED / ACCEPTED / CLOSED
```

P1-8 is now the canonical next action.

This Task starts P1-8 **design only**.

No P1-8 runtime implementation exists or is authorized by this Task.

---

# 2. mandatory preflight

Before broad source inspection:

## 2.1 HEAD

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

## 2.2 corrected durable handoff

Require:

```text
sha256(
.aiassistant/reports/aiscc/
20260830_1712_aiscc-p1-7-runtime-accepted-p1-8-command-center-handoff-1.md
)
==
0169b07642e72d1c7025c98946402e53102c3de2f72a4b3df78ba0ed851004c5
```

Require exact inherited guard inventory:

```text
P1_7_HUMAN:
G_HUMAN_REQUIRED
G_HUMAN_NOT_REQUIRED
G_NO_PENDING_HUMAN_GATE
G_SUSPENDED_HUMAN_GATE
G_RESUMABLE_HUMAN_GATE
G_HUMAN_APPROVED
G_HUMAN_REWORK
G_HUMAN_REJECTED

P1_7_JUDGMENT:
G_JUDGMENT_ACCEPTED
G_JUDGMENT_REJECTED
G_JUDGMENT_REWORK
```

Any mismatch:

```text
STOP
→ P1_7_HANDOFF_PROVENANCE_DRIFT
```

## 2.3 workspace

Record:

```text
git status --short
git diff --name-only
git diff --cached --name-only
```

Expected index:

```text
empty
```

Expected tracked worktree:

```text
clean
```

This active Task and generated target bundle may be ignored/untracked according to repository policy.

Unrelated tracked dirty content:

```text
STOP
→ DIRTY_WORKSPACE_MIXED
```

---

# 3. minimum authoritative context

Read exactly:

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md

.aiassistant/reports/aiscc/
20260830_1712_aiscc-p1-7-runtime-accepted-p1-8-command-center-handoff-1.md

.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md
.aiassistant/reports/aiscc/AISCC_PRIOR_ART_BOUNDARY.md

.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md
.aiassistant/rules/AISCC_HUMAN_GATE_JUDGMENT.md

.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md
.aiassistant/records/command-center/CYCLE_RECORD_TEMPLATE.md
.aiassistant/records/command-center/NEXT_ACTION_SELECTION_RUBRIC.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

Do not treat Browser Project Source mirrors as current canonical authority if they differ from repository
canonical.

Do not bulk-read unrelated rules/reports/source.

---

# 4. accepted predecessor invariants — frozen

P1-8 must consume these invariants and must not reinterpret them.

## 4.1 product chain

Accepted compressed product chain:

```text
Task
→ Evidence
→ Judgment
→ Cycle
→ Next Action
```

Accepted end-to-end intent includes:

```text
Judgment
→ Curated Cycle Memory
→ Next Action
```

Raw session output is not accepted project memory merely because it exists.

## 4.2 P1-4 transition authority

```text
TransitionRequest != TransitionEvaluation != TransitionDecision

only P1-4:
→ issues admitted TransitionDecision
→ mutates WorkflowState/state_version
```

P1-8 cannot directly mutate `WorkRun`.

## 4.3 P1-6 evidence authority

```text
EvidenceCandidate != AdmittedEvidence

P1-6 alone owns:
Evidence admission
EvidenceSetSatisfactionAttestation
G_EVIDENCE
```

P1-8 cannot mint or reinterpret evidence authority.

## 4.4 P1-7 Human/Judgment authority

```text
HumanResult != Judgment
Judgment != TransitionDecision
HumanResult/Judgment != WorkflowState
```

P1-8 cannot mint or reinterpret:

```text
G_HUMAN_*
G_JUDGMENT_*
HumanGate
HumanResult
Judgment
```

## 4.5 exact inherited P1-7 future-owner guards

P1-8 may consume but must not absorb or replace:

```text
P1_7_HUMAN:
G_HUMAN_REQUIRED
G_HUMAN_NOT_REQUIRED
G_NO_PENDING_HUMAN_GATE
G_SUSPENDED_HUMAN_GATE
G_RESUMABLE_HUMAN_GATE
G_HUMAN_APPROVED
G_HUMAN_REWORK
G_HUMAN_REJECTED

P1_7_JUDGMENT:
G_JUDGMENT_ACCEPTED
G_JUDGMENT_REJECTED
G_JUDGMENT_REWORK
```

---

# 5. accepted product/prior-art boundary

The design must preserve the accepted P0-2 claim ceiling.

Known prior art already covers:

```text
persistent project memory
event-sourced provenance
judgment/pre-action governance
session-to-knowledge curation
human-curated reusable knowledge
```

Do not claim those primitives as AISCC inventions.

P1-8 exists to implement/test the accepted differentiation hypotheses:

```text
AISCC-DH-06:
judgment-passed curated memory/cycle admission

AISCC-DH-07:
Task → Evidence → Judgment → Cycle → Next Action
```

The design must remain compatible with future evidence for:

```text
durable Cycle model
rejected-memory exclusion
Next Action reuse trace
end-to-end Task/Cycle/commit mapping
```

No novelty or superiority claim is generated by this design Task.

---

# 6. design target artifact

Create:

```text
.aiassistant/rules/
AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md
```

This is the P1-8 canonical design candidate.

It is NOT accepted merely because Executor creates it.

Human/Command Center review is required.

Do not update canonical state files during this Task.

Do not commit the design candidate.

---

# 7. core design question A — product Cycle vs Command Center Cycle Record

The repository already has human-readable governance artifacts:

```text
.aiassistant/records/aiscc/cycles/*.cycle.md
```

P1-8 must explicitly decide whether the runtime product domain object is named:

```text
Cycle
CycleRecord
ProjectCycle
CuratedCycle
```

or another exact term.

The design MUST prevent silent conflation between:

```text
Command Center Markdown Cycle Record
```

and:

```text
runtime System-owned/admitted Cycle memory object
```

Required decision:

```text
What object is authoritative runtime provenance?
What object is a public/governance projection?
What object is admitted reusable project memory?
```

The Markdown Cycle Record may remain a human/public projection and must not become runtime authority merely
because a file exists.

---

# 8. core design question B — exact non-substitution vocabulary

Define exact V1 domain terms and freeze their relationships.

At minimum evaluate/freeze exact equivalents of:

```text
CycleCandidate
CycleAdmissionRequest
CycleEvaluation
CycleAdmissionDecision
AdmittedCycle

ProjectMemoryEntry
ProjectMemoryView

NextActionProposal
NextActionSelection
```

Exact names may differ, but every semantic role must have one explicit owner.

Required non-substitution statements must include exact equivalents of:

```text
CommandCenterCycleRecord != AdmittedCycle

raw session/chat != ProjectMemory

Agent summary != ProjectMemory

Judgment != CycleAdmissionDecision

TransitionDecision != CycleAdmissionDecision

WorkflowState != CycleAdmissionDecision

AdmittedCycle != ProjectMemoryView

ProjectMemoryEntry != TaskContract

ProjectMemoryEntry != canonical rule/policy authority

memory retrieval result != evidence

memory retrieval result != Judgment

NextActionProposal != NextActionSelection

NextActionSelection != TransitionDecision
```

If some proposed object is unnecessary in V1, state which owner absorbs the responsibility and why.

Do not leave overlapping ownership implicit.

---

# 9. core design question C — Cycle admission eligibility

Freeze the exact admission preconditions.

The accepted product thesis requires curated memory rather than raw session accumulation and targets
`rejected-memory exclusion`.

The design must explicitly decide the relation among:

```text
P1-7 Judgment
P1-4 terminal WorkflowState
P1-6 admitted evidence/provenance
TaskContract
WorkRun
Git/run provenance
Cycle admission
```

At minimum resolve:

```text
Does curated memory admission require:
JudgmentKind.ACCEPTED?

Does it also require:
WorkflowState.ACCEPTED?

Must Judgment and WorkflowState refer to the same exact
TaskContract / WorkRun / source state_version / transition lineage?

What happens to:
REJECTED
FAILED
REWORK_REQUIRED
BLOCKED
HOLD_REWORK_REQUIRED

Do those remain durable operational provenance but stay excluded from reusable curated memory?

Can a later accepted correction/supersession create a new admissible Cycle without mutating the old one?
```

The design MUST preserve:

```text
historical operational provenance
!= reusable curated project memory
```

If accepted predecessor documents conflict on rejected-memory semantics:

```text
STOP
→ POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

Do not silently choose a permissive memory policy.

---

# 10. core design question D — exact Cycle contents

Define exact authoritative fields.

The authoritative admitted Cycle must be ref/root based and reconstructable.

At minimum evaluate/freeze bindings to:

```text
project_id

TaskContract id/version

WorkRun id

terminal WorkflowState/state_version

TransitionDecision ref/version

P1-7 Judgment ref/version/kind

P1-6 evidence attestation/root refs when applicable

HumanResult ref when applicable

execution/provider/tool provenance refs when applicable

commit/repository provenance
when the Task produces durable Git work

source artifact roots

created/issued/admitted timestamps

admission authority id/version/revision

privacy/export classification
```

Human-readable summaries may exist, but:

```text
summary text
!= authoritative provenance
```

Do not make free-form LLM summaries part of admission identity unless exact deterministic hashing and authority
semantics are explicitly justified.

---

# 11. core design question E — memory content taxonomy

P1-8 must decide what becomes reusable project memory.

At minimum evaluate/freeze typed categories equivalent to:

```text
DECISION
INVARIANT
CONSTRAINT
LESSON
BLOCKER_RESOLUTION
PROVENANCE_POINTER
NEXT_ACTION_CONTEXT
```

Do not create categories merely for completeness.

For each accepted category define:

```text
source authority
required Cycle provenance
scope
applicability
supersession/correction behavior
retrieval eligibility
public/private export behavior
```

Critical:

```text
memory content
must not silently become policy authority
```

A memory entry that suggests a rule change is at most:

```text
rule update candidate / proposal
```

until a dedicated canonical-rule update is admitted through its own Task/Human process.

This closes prompt/memory contamination risk.

---

# 12. core design question F — ProjectMemory admission and projection

Define whether:

```text
AdmittedCycle
```

itself is the reusable memory object, or whether a second admission/projector creates:

```text
ProjectMemoryEntry
```

from an AdmittedCycle.

Avoid unnecessary double-admission.

But preserve a clear separation between:

```text
immutable historical Cycle provenance
```

and:

```text
current ProjectMemoryView / active reusable entries
```

Freeze:

```text
entry identity/version
project scope
subject/resource scope
source Cycle refs
current/superseded/revoked state
correction lineage
applicability/freshness if any
deterministic projection rules
```

Historical validity:

```text
!=
current memory applicability
```

---

# 13. core design question G — correction, supersession, revocation

Design append-only behavior.

No in-place rewriting of accepted historical provenance.

Freeze exact semantics for:

```text
Cycle correction
memory correction
supersession
revocation/invalidation
retraction due to later discovered provenance corruption
```

Required:

```text
old immutable object remains historical
new object/event changes current authority/applicability
```

Prevent:

```text
old stale Cycle
→ silently remains active memory after authoritative supersession
```

Define cycle/graph protection for correction chains.

---

# 14. core design question H — concurrency and idempotency

Freeze global/project identity and serialization.

At minimum decide:

```text
Can two concurrent admissions for the same TaskContract/WorkRun terminal epoch occur?

What globally unique immutable IDs exist?

What is the deterministic proposal/admission fingerprint?

What lock scope is canonical:
WorkRun
Cycle ID
Project memory scope
or combination?

What deterministic lock ordering prevents deadlock?

Same ID + same proposal
→ exact immutable replay?

Same ID + different proposal
→ typed identity conflict?
```

P1-8 must not create a second terminal transition race.

A Cycle should normally be downstream of already-admitted terminal authority.

---

# 15. core design question I — restart / persistence

Target persistence remains PostgreSQL unless an accepted architecture owner says otherwise.

Freeze append-only tables/events/projections needed for:

```text
Cycle candidate/request/evaluation/decision/admission
current ProjectMemory view
correction/supersession
Next Action selection when in scope
```

Restart must deterministically reconstruct:

```text
historical admitted Cycles
current memory applicability
source authority bindings
current Next Action state when durable
```

Corrupt/incomplete provenance:

```text
fail closed
no auto repair
```

Do not use in-memory-only truth as V1 authority.

---

# 16. core design question J — deterministic retrieval

The P0-2 MVP explicitly does not require a large RAG/vector platform.

P1-8 V1 should prioritize inspectable deterministic retrieval.

Design/freeze:

```text
project scope
memory category
subject/resource
TaskContract/domain tags if accepted
source Cycle
current applicability
recency/version
```

If semantic/vector search is considered:

```text
it must be optional/non-authoritative
```

and cannot change memory admission/currentness.

A retrieval ranking score:

```text
!= authority
```

---

# 17. core design question K — Next Action ownership

This is load-bearing.

The accepted Product Thesis says:

```text
Next Action is not an Agent free-form conclusion.

It is selected using:
accepted state
blocker
baseline gap
submission critical path
```

P1-8 must freeze one exact V1 owner model.

At minimum evaluate:

```text
A. P1-8 System-owned deterministic NextActionSelection

B. Command Center/Human-owned NextActionSelection
   with P1-8 only providing admitted memory inputs

C. split:
   Agent/LLM NextActionProposal
   → deterministic policy evaluation
   → Command Center/Human gate where required
   → durable NextActionSelection
```

Whichever V1 is selected, define:

```text
proposal != selection

selection != WorkflowState

selection != TransitionDecision

selection cannot directly mutate WorkRun

source Cycle/memory refs

selection policy id/version

reason codes

blocker/baseline/security priority

queue/critical-path input

idempotency/correction

human authority when applicable
```

Also distinguish runtime product `NextAction` from repository governance:

```text
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

A Markdown roadmap file is not runtime NextAction authority merely because it exists.

---

# 18. core design question L — Task/Cycle/commit mapping

Freeze how public provenance maps:

```text
Task
→ WorkRun
→ Evidence roots
→ Judgment
→ terminal TransitionDecision
→ admitted Cycle
→ memory entry
→ Next Action
→ Git commit(s)
```

Do not require a Git commit for Tasks that legitimately produce no Git change.

When a commit exists:

```text
commit ref
must be exact immutable provenance
```

A commit message or branch name alone is insufficient authority.

---

# 19. core design question M — privacy / export

Cycle memory may later support public replay/self-dogfooding.

Freeze V1 classifications equivalent to:

```text
PRIVATE_INTERNAL
PUBLIC_SANITIZED
NON_EXPORTABLE
```

or reuse accepted security classifications where appropriate.

Do not persist/export:

```text
credential
secret
private raw conversation
private Human identity
customer/private repository content
```

merely because a Cycle references it.

Public projection must use refs/sanitized labels where accepted.

Historical private provenance may remain internally referenced without becoming public payload.

---

# 20. core design question N — self-dogfooding boundary

P2-4 will own actual Self-Dogfooding cutover.

P1-8 should only make the governance substrate possible.

Design should support recording:

```text
orchestrator version/commit
Task
transition trace
evidence admission
Human intervention
Judgment
Cycle
Next Action
commit mapping
```

but this Task must not claim:

```text
AISCC_SELF_DOGFOOD active
```

and must not generate a self-dogfooding proof corpus.

---

# 21. explicit V1 non-goals

Unless a baseline conflict proves otherwise, keep outside P1-8 V1 design:

```text
large vector DB / RAG platform

cross-company/global memory federation

automatic free-form skill generation

automatic canonical-rule mutation from memory

model fine-tuning

agent personality/profile memory

arbitrary raw chat/session storage as trusted memory

multi-agent voting on memory truth

P2 UI

P2 demo corpus

P2 self-dogfooding cutover

P3 public deployment/release
```

---

# 22. source inspection

After reading the canonical documents, inspect only enough current source/schema to prove integration
feasibility and naming compatibility.

Expected source areas:

```text
src/aiscc/workflow/**
src/aiscc/evidence/**
src/aiscc/human/**
src/aiscc/judgment/**
src/aiscc/persistence/**

migrations/versions/**
```

Read targeted symbols only.

Do not create P1-8 runtime source.

Report:

```text
existing reusable primitives
naming collisions
transaction/lock hooks available
schema integration constraints
future implementation touch points
```

---

# 23. design candidate required sections

`AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md` must contain at minimum:

1. purpose / scope
2. predecessor authority map
3. exact domain vocabulary
4. ownership table
5. mandatory non-substitution
6. Cycle vs Command Center Cycle Record boundary
7. Cycle admission eligibility
8. exact Cycle identity/payload
9. memory taxonomy
10. memory admission/projection
11. historical vs current applicability
12. correction/supersession/revocation
13. concurrency/idempotency/lock ordering
14. PostgreSQL persistence/restart
15. fail-closed corruption behavior
16. deterministic retrieval
17. Next Action owner/selection contract
18. Task/Cycle/commit mapping
19. privacy/export classification
20. Self-Dogfooding handoff
21. P2/P3 boundaries
22. failure/error vocabulary
23. implementation handoff checklist
24. design decisions still requiring Human choice, if any
25. prior-art/claim ceiling

Avoid prose-only ambiguity.

Use exact enums/tables/state diagrams where needed.

---

# 24. allowed paths/actions

## allowed source mutation

Create/modify only:

```text
.aiassistant/rules/
AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md
```

Task lifecycle:

```text
.aiassistant/tasks/active/
20260830_1909_aiscc-p1-8-project-memory-and-cycle-admission-design-1.md

→

.aiassistant/tasks/done/
20260830_1909_aiscc-p1-8-project-memory-and-cycle-admission-design-1.md
```

Temporary review bundle:

```text
.aiassistant/reports/target/
20260830_1909_aiscc-p1-8-project-memory-and-cycle-admission-design-1/**
```

No other tracked mutation.

## allowed actions

```text
read exact canonical docs
targeted read-only source/schema inspection
create design candidate
static Markdown/UTF-8 validation
Git diff/status inspection
```

---

# 25. forbidden

Do NOT modify:

```text
src/**
tests/**
migrations/**

.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md
.aiassistant/rules/AISCC_HUMAN_GATE_JUDGMENT.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/reports/aiscc/
20260830_1712_aiscc-p1-7-runtime-accepted-p1-8-command-center-handoff-1.md
```

Do NOT:

```text
implement P1-8 runtime

create migration/runtime table

change P1-4/P1-6/P1-7 authority

change existing guard ownership

create new WorkflowState or TransitionDecision kind

mint G_EVIDENCE / G_HUMAN_* / G_JUDGMENT_*

implement P2/P3

start Self-Dogfooding

run provider/network/credentialed external action

deploy / Public Live

git add / commit / push
```

No source mirror sync.

---

# 26. evidence contract

## executor_required

### DESIGN_SOURCE

Scope:

```text
canonical predecessor documents
targeted current source/schema
```

Pass:

```text
design decisions are traceable to accepted baseline/current source
no invented predecessor authority
```

### DESIGN_NON_SUBSTITUTION

Pass:

```text
Cycle/memory/NextAction vocabulary has one exact owner each
no P1-4/P1-6/P1-7 authority substitution
raw session/projection/summary not treated as authoritative memory
```

### DESIGN_PERSISTENCE

Pass:

```text
append-only/restart/concurrency/correction/fail-closed semantics are explicit enough for runtime implementation
```

### DESIGN_MEMORY_CONTAMINATION

Pass:

```text
rejected/raw/untrusted output cannot silently enter current curated project memory
memory cannot silently become canonical policy
```

### DESIGN_NEXT_ACTION

Pass:

```text
one exact V1 Next Action ownership model is selected
proposal/selection/transition authority are separated
```

### STATIC_GOVERNANCE

Pass:

```text
UTF-8
Markdown
no prohibited control characters
no secret value
```

## reuse_allowed

Reuse accepted:

```text
P0-2 Product Thesis / Prior-Art baseline

P1-4 accepted state-machine authority

P1-6 accepted evidence authority

P1-7 accepted Human/Judgment authority

corrected P1-7 → P1-8 handoff
```

Only if exact canonical files match current repository baseline.

## human_owned

```text
P1-8 design final review
→ HUMAN_PENDING
```

Executor cannot mark the design accepted.

## not_required

```text
runtime unit/integration/PostgreSQL tests:
NOT_REQUIRED

migration:
NOT_REQUIRED

browser QA:
NOT_REQUIRED

provider/network:
NOT_REQUIRED
```

## forbidden

```text
runtime implementation evidence

deployment/public-live evidence

Human design acceptance claimed by Executor
```

---

# 27. proof non-substitution

Required exact statements in design/report:

```text
Agent output != ProjectMemory

raw session != AdmittedCycle

Command Center Cycle Record != runtime Cycle authority

Judgment != CycleAdmissionDecision

TransitionDecision != CycleAdmissionDecision

AdmittedCycle != current ProjectMemoryView

memory retrieval != evidence

memory retrieval != Judgment

ProjectMemory != canonical rule authority

NextActionProposal != NextActionSelection

NextActionSelection != TransitionDecision

historical memory validity != current memory applicability
```

And inherited:

```text
G_EVIDENCE != G_HUMAN_* != G_JUDGMENT_*
HumanResult != Judgment
Judgment != TransitionDecision
SecurityAdmissionDecision != TransitionDecision
```

---

# 28. mandatory stop

STOP on:

```text
HEAD drift

corrected P1-7 handoff drift

canonical predecessor conflict

accepted P0-2 memory/rejected-memory boundary cannot be reconciled

P1-8 requires changing P1-4/P1-6/P1-7 authority

current persistence primitives cannot support design without predecessor policy change

need to add WorkflowState/transition pair during this design

unrelated tracked dirty collision

design requires P2/P3 implementation decision
```

Report exact:

```text
POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

or:

```text
DESIGN_BASELINE_GAP
```

Do not silently broaden scope.

---

# 29. accept criteria for Executor submission

All must hold:

```text
exact start HEAD verified

corrected P1-7 handoff SHA verified

design candidate created at exact canonical candidate path

runtime Cycle vs Command Center Cycle Record boundary explicit

exact vocabulary/owner table explicit

Cycle admission eligibility explicit

rejected/raw memory contamination policy explicit

Task/Evidence/Judgment/terminal-state bindings explicit

Cycle identity/payload explicit

memory taxonomy/projection explicit

correction/supersession/revocation explicit

concurrency/idempotency/lock ordering explicit

PostgreSQL persistence/restart/fail-closed explicit

deterministic retrieval explicit

one exact V1 Next Action ownership model selected

Task/Cycle/commit mapping explicit

privacy/export explicit

Self-Dogfooding/P2/P3 boundary explicit

prior-art claim ceiling preserved

no P1-8 runtime source/tests/migrations created

no predecessor canonical file changed

no Git add/commit/push

human acceptance:
HUMAN_PENDING
```

---

# 30. report requirements

Report exact:

1. Task path
2. start/final HEAD
3. corrected P1-8 handoff SHA
4. explicit canonical read inventory
5. targeted source/schema read inventory
6. created design candidate path
7. product Cycle exact term
8. Command Center Cycle Record boundary
9. exact domain vocabulary
10. exact semantic owner table
11. Cycle admission eligibility
12. rejected/HOLD/failed/rework memory handling
13. terminal P1-4/P1-7/P1-6 source-authority binding
14. Cycle identity/fingerprint proposal
15. authoritative Cycle payload
16. memory taxonomy
17. memory projection/currentness
18. correction/supersession/revocation
19. global/project identity + lock ordering
20. idempotency conflict semantics
21. restart/fail-closed model
22. deterministic retrieval
23. selected Next Action V1 owner model
24. proposal/selection/TransitionDecision separation
25. Task/Cycle/commit mapping
26. privacy/export model
27. memory-to-policy contamination prevention
28. Self-Dogfooding handoff
29. prior-art claim ceiling
30. open Human design choices, if any
31. runtime implementation = NOT_STARTED
32. P2/P3 = NOT_STARTED
33. provider/network/credential/deployment = 0
34. Git actions = none
35. human verification = HUMAN_PENDING
36. preserved exact paths
37. next recommendation

---

# 31. export bundle

Target:

```text
.aiassistant/reports/target/
20260830_1909_aiscc-p1-8-project-memory-and-cycle-admission-design-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
```

Include byte-preserving copies of:

```text
.aiassistant/rules/AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md

.aiassistant/tasks/done/
20260830_1909_aiscc-p1-8-project-memory-and-cycle-admission-design-1.md
```

Manifest:

```text
actual source/copy SHA-256
64 lowercase hex
source/copy identity PASS
start/final HEAD
changed-path inventory
forbidden-path mutation check
```

---

# 32. Git/lifecycle

No Git add/commit/push.

Expected final HEAD:

```text
4b84a9f66c148b198d3f4b6b01cffc4641fdceb1
```

Expected tracked diff:

```text
.aiassistant/rules/AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md
```

Task moves active → done according to repository policy.

Temporary target remains ignored/review-only.

---

# 33. expected submission state

Successful Executor submission:

```text
P1-7:
ACCEPTED / CLOSED

P1-8 Design:
DESIGN_CANDIDATE / HUMAN_PENDING

P1-8 Runtime:
NOT_STARTED

P2:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

Command Center next:

```text
review P1-8 design candidate

→ ACCEPT
or
→ HOLD_REWORK_REQUIRED

Human final design review only after Command Center PASS
```

---

# 34. preserved exact paths

Preserve after submission:

```text
.aiassistant/reports/aiscc/
20260830_1712_aiscc-p1-7-runtime-accepted-p1-8-command-center-handoff-1.md

.aiassistant/rules/
AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md

.aiassistant/tasks/done/
20260830_1909_aiscc-p1-8-project-memory-and-cycle-admission-design-1.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

The target bundle is temporary and deletable after Command Center judgment unless explicitly preserved later.
