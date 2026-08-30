# 작업지시서: P1-8 Memory Authority, Lineage, and Next Action Eligibility Design Rework

## meta

- task_id: `20260830_1933_aiscc-p1-8-memory-authority-lineage-and-next-action-eligibility-design-rework-1`
- created_at: `2026-08-30T19:33:00+09:00`
- phase: `P1-8 Project Memory and Cycle Admission`
- work_type: `DESIGN_REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1_8_PROJECT_MEMORY_CYCLE`
- expected_start_head: `4b84a9f66c148b198d3f4b6b01cffc4641fdceb1`
- predecessor_design_sha256: `ba1a8f5903b4bf7798fab81a07790a977185eff55ba4933ad51eae54985bea1d`
- corrected_p1_7_handoff_sha256: `0169b07642e72d1c7025c98946402e53102c3de2f72a4b3df78ba0ed851004c5`
- p1_8_design_status: `HOLD_REWORK_REQUIRED / HUMAN_PENDING`
- p1_8_runtime_status: `NOT_STARTED`

---

# 1. purpose

Rework only the three load-bearing P1-8 design gaps identified by Command Center:

```text
A. MemoryDeclaration content authority

B. stable ProjectMemory lineage + correction/supersession authority

C. NextAction action eligibility authority
```

Preserve all accepted predecessor boundaries and all sound portions of the 1909 candidate.

Place/preserve the Command Center HOLD Cycle:

```text
.aiassistant/records/aiscc/cycles/
20260830_1933_aiscc-p1-8-design-memory-authority-lineage-next-action-eligibility-hold-1.cycle.md
```

---

# 2. mandatory preflight

Require:

```text
HEAD ==
4b84a9f66c148b198d3f4b6b01cffc4641fdceb1

sha256(.aiassistant/rules/AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md)
==
ba1a8f5903b4bf7798fab81a07790a977185eff55ba4933ad51eae54985bea1d

corrected P1-7 handoff SHA ==
0169b07642e72d1c7025c98946402e53102c3de2f72a4b3df78ba0ed851004c5
```

Any mismatch:

```text
STOP
→ REVIEWED_DESIGN_DRIFT
```

Record:

```text
git status --short
git diff --name-only
git diff --cached --name-only
```

No Git add/commit/push.

---

# 3. allowed mutation

Modify only:

```text
.aiassistant/rules/
AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md
```

Task lifecycle:

```text
.aiassistant/tasks/active/
20260830_1933_aiscc-p1-8-memory-authority-lineage-and-next-action-eligibility-design-rework-1.md

→

.aiassistant/tasks/done/
20260830_1933_aiscc-p1-8-memory-authority-lineage-and-next-action-eligibility-design-rework-1.md
```

Temporary target bundle only under:

```text
.aiassistant/reports/target/
20260830_1933_aiscc-p1-8-memory-authority-lineage-and-next-action-eligibility-design-rework-1/**
```

No runtime source/test/migration.

No canonical state update.

---

# 4. FINDING-A — MemoryDeclaration authority

The reworked design must add an explicit versioned owner contract equivalent to:

```text
MemoryDeclarationAuthorityPolicy
```

Do not leave declaration authority as “typed payload + exact source refs”.

For every V1 memory category freeze:

```text
category
authority mode
allowed source object kinds
exact content derivation/binding
required source refs/fingerprints
content fingerprint algorithm
scope/applicability derivation
privacy ceiling
failure code
```

## 4.1 exact authority modes

Select exact names, but semantics must distinguish at least:

```text
DETERMINISTIC_POINTER
STRUCTURED_RESULT_ATTESTED
OWNER_ATTESTED
```

No semantic inference from arbitrary prose.

### DETERMINISTIC_POINTER

Content must be a deterministic projection of immutable source fields.

Suitable candidates:

```text
INVARIANT_POINTER
CONSTRAINT_POINTER
PROVENANCE_POINTER
BLOCKER_RESOLUTION where relation is purely ref-based
```

The declaration cannot add descriptive facts beyond the exact source projection schema.

### STRUCTURED_RESULT_ATTESTED

The exact memory content/fingerprint must already exist in a TaskContract-authorized structured result artifact.

Required binding:

```text
TaskContract result schema/version
artifact ref/hash
structured field path or object ref
content fingerprint
Cycle Task/WorkRun/Judgment binding
```

The caller may point to it but cannot rewrite it.

### OWNER_ATTESTED

Use only if an accepted owner actually exists for that content type.

The design must identify:

```text
owner
attestation object
immutable identity/fingerprint
Task/run/scope binding
```

Do not invent a new Human/P1-7 authority without explicitly making it a new P1-8 design decision requiring
Human review.

## 4.2 V1 category table

For all exact categories:

```text
DECISION
INVARIANT_POINTER
CONSTRAINT_POINTER
LESSON
BLOCKER_RESOLUTION
PROVENANCE_POINTER
NEXT_ACTION_CONTEXT
```

freeze one authority mode and exact source contract.

If `LESSON` cannot be deterministically/source-attested in current V1:

```text
LESSON:
NOT_SUPPORTED
```

is acceptable and preferred over Agent-authored semantic memory.

Likewise `NEXT_ACTION_CONTEXT` must be exact structured context from an accepted source/policy; an Agent cannot
invent arbitrary context text.

## 4.3 CycleEvaluation

Freeze exact rule:

```text
for every MemoryDeclaration:
  resolve exact policy
  resolve exact immutable source
  derive/reconstruct expected content
  expected content fingerprint == declaration content fingerprint
```

Mismatch:

```text
MEMORY_DECLARATION_SOURCE_MISMATCH
```

Missing authority:

```text
MEMORY_DECLARATION_AUTHORITY_NOT_FOUND
```

Unsupported semantic inference:

```text
MEMORY_DECLARATION_MODE_NOT_SUPPORTED
```

Required non-substitution:

```text
accepted Cycle source
!= authority for arbitrary caller-authored memory payload
```

---

# 5. FINDING-B — stable memory lineage identity

Add explicit separation:

```text
ProjectMemoryEntryId
!= MemoryLineageKey
```

Freeze one stable versioned lineage key.

Recommended shape:

```text
MemoryLineageKey = (
  project_id,
  category,
  subject_key,
  applicability_key,
  semantic_slot
)
```

Exact names may differ, but the key must:

```text
not contain cycle_id
not contain content_fingerprint
remain stable across accepted successor Cycles
be deterministically normalized/versioned
prevent unrelated memories from sharing a lineage
```

Define `semantic_slot` or equivalent precisely enough that:

```text
same subject/category but different facts
```

do not accidentally supersede each other.

## 5.1 current tips

Freeze:

```text
one CURRENT tip per MemoryLineageKey
```

or explicitly define the categories where multi-current is legal.

If multi-current is allowed:

```text
the cardinality and deterministic retrieval semantics must be exact
```

Do not leave “same subject/applicability” as prose.

## 5.2 supersession behavior

Choose exact V1 rule for how a new entry becomes successor:

```text
EXPLICIT_SUPERSESSION_ONLY

or

POLICY_DETERMINISTIC_AUTO_SUPERSESSION
```

If auto:

```text
exact policy id/version
lineage key
predecessor expected revision
replacement eligibility
```

must be frozen.

A later Cycle with the same subject/category alone must NOT automatically supersede an earlier entry.

## 5.3 correction/revocation authority

Freeze who can make these effective:

```text
CORRECTION
SUPERSESSION
REVOCATION
```

Required non-substitution:

```text
CycleCandidate correction intent
!= correction authority
```

Allowed authority sources should be exact equivalents of:

```text
predecessor source-owner correction/revocation event

P1-8 deterministic lineage policy

explicit owner-authorized correction attestation
```

Define priority when more than one source exists.

Random Agent/executor proposal fields must never revoke/supersede current memory.

## 5.4 immutable/historical behavior

Preserve:

```text
old entry remains historical
current tip changes through append-only event
correction graph cycle/self-reference/project crossing fail closed
```

Add exact event authority fields and expected-revision binding.

---

# 6. FINDING-C — NextAction action eligibility authority

Keep:

```text
P1-8 System-owned deterministic NextActionSelection
```

but add a separate exact action eligibility contract.

Define exact equivalent of:

```text
NextActionDescriptor
ActionRef
NextActionEligibilityPolicy
```

A Proposal cannot mint a new action definition.

## 6.1 eligible source authorities

Freeze which authorities can enroll an action descriptor.

At minimum evaluate:

```text
versioned NextActionSelectionPolicy action catalog

accepted canonical roadmap/critical-path item

TaskContract-defined follow-up action/template

owner-authorized blocker recovery action
```

Select exact V1 sources.

Every descriptor must include exact immutable:

```text
action_id/version
action_kind
project/scope
parameter schema/version
source authority ref/hash
allowed selection mode
priority classification source
required Human input/gate
Task issuance owner
privacy/security restrictions
descriptor fingerprint
```

## 6.2 proposal ceiling

`NextActionProposal` may:

```text
nominate an eligible ActionRef
supply parameters allowed by descriptor schema
supply non-authoritative rationale
```

It may NOT:

```text
define a new ActionRef
change priority
claim blocker/security classification
change Task issuance owner
bypass Human requirement
change scope beyond descriptor
```

Required:

```text
proposal action eligibility
→ verified before ranking
```

Novel/unregistered action:

```text
NEXT_ACTION_ACTION_NOT_ENROLLED
```

or:

```text
NEXT_ACTION_HUMAN_INPUT_REQUIRED
```

according to selected V1 policy.

## 6.3 authoritative priority facts

Freeze that:

```text
security/blocker/baseline/critical-path priority
```

comes from exact policy/source-domain authority, not proposal fields.

The deterministic selector ranks only **eligible** proposals/actions.

Required non-substitution:

```text
deterministic ranking
!= action authority
```

## 6.4 Task issuance boundary

Keep:

```text
NextActionSelection
!= TaskContract
```

Define exact next step:

```text
Selection
→ issued-Task candidate/ref
→ Task authority process
```

P1-8 cannot issue/modify TaskContract unless the design explicitly chooses a Task authority integration already
supported by predecessor baseline.

If no such runtime Task issuer exists in P1-8 V1:

```text
Selection remains an authoritative recommendation/projection
and Task issuance stays external/Command Center owned
```

State this exactly.

---

# 7. correction to existing design sections

Update at minimum:

```text
§4 Ownership table
§5 Mandatory non-substitution
§8 Cycle payload/fingerprint if new refs are authoritative
§9 Memory taxonomy
§10 Memory admission
§11 Current applicability
§12 Correction/supersession/revocation
§13 concurrency if lineage locks change
§16 retrieval if lineage/current tip changes
§17 Next Action owner/inputs/policy
§22 error vocabulary
§23 implementation checklist
§24 Human review choices
```

Add new sections if clearer.

Do not rewrite unrelated accepted content.

---

# 8. failure vocabulary additions

Add exact typed equivalents for:

```text
MEMORY_DECLARATION_AUTHORITY_NOT_FOUND
MEMORY_DECLARATION_SOURCE_MISMATCH
MEMORY_DECLARATION_MODE_NOT_SUPPORTED

MEMORY_LINEAGE_IDENTITY_CONFLICT
MEMORY_SUPERSESSION_AUTHORITY_REQUIRED
MEMORY_CORRECTION_AUTHORITY_REQUIRED

NEXT_ACTION_ACTION_NOT_ENROLLED
NEXT_ACTION_DESCRIPTOR_MISMATCH
NEXT_ACTION_PARAMETER_SCHEMA_MISMATCH
```

Preserve existing errors unless exact renaming is justified.

---

# 9. required design proofs

Executor report must show concrete examples for each.

## 9.1 memory laundering negative

```text
accepted WorkRun + valid artifact ref
+ Agent-authored unrelated structured LESSON
→ reject
```

## 9.2 exact source projection positive

```text
valid deterministic pointer declaration
→ exact expected content fingerprint
→ eligible for Cycle admission
```

## 9.3 unrelated supersession negative

```text
Cycle B has same category/subject but different semantic slot
→ cannot supersede Cycle A memory
```

## 9.4 unauthorized correction negative

```text
Agent sets supersedes/revokes intent
without accepted correction authority
→ reject
```

## 9.5 next-action laundering negative

```text
Agent proposal defines a new arbitrary action payload
→ not eligible for ranking
→ no NextActionSelection
```

## 9.6 eligible action positive

```text
proposal references exact enrolled ActionRef
+ valid schema parameters
+ authoritative priority inputs
→ deterministic ranking permitted
```

---

# 10. predecessor boundaries

Do not change:

```text
P1-4:
TransitionDecision / WorkflowState

P1-6:
Evidence admission / G_EVIDENCE

P1-7:
HumanGate / HumanResult / Judgment / G_HUMAN_* / G_JUDGMENT_*
```

Do not create:

```text
new WorkflowState
new P1-4 guard
new P1-6 evidence profile
new P1-7 Human/Judgment authority
```

unless stopping with:

```text
POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

---

# 11. source inspection

Targeted read-only source inspection is allowed if needed to decide:

```text
whether a runtime Task authority/TaskContract issuer already exists
whether structured result artifacts expose exact immutable payloads
whether P1-8 can reuse a canonical scope/key type
```

Do not implement source.

If no runtime Task issuer exists, explicitly keep Task issuance outside P1-8 V1 rather than inventing it.

---

# 12. forbidden

No:

```text
src/**
tests/**
migrations/**

canonical state update

P1-8 runtime implementation

P2/P3

Self-Dogfooding

provider/network/credential/deployment

Git add/commit/push
```

Do not modify the corrected P1-7 handoff.

---

# 13. evidence contract

## executor_required

```text
DESIGN_MEMORY_DECLARATION_AUTHORITY
DESIGN_MEMORY_LINEAGE
DESIGN_MEMORY_CORRECTION_AUTHORITY
DESIGN_NEXT_ACTION_ELIGIBILITY
DESIGN_TASK_ISSUANCE_BOUNDARY
DESIGN_NON_SUBSTITUTION
STATIC_GOVERNANCE
```

## human_owned

```text
P1-8 design final review
→ HUMAN_PENDING
```

No Executor acceptance claim.

---

# 14. accept criteria

All must hold:

```text
every V1 memory category has exact authority mode/source contract

arbitrary caller-authored structured memory cannot piggyback on accepted source refs

MemoryLineageKey is stable across Cycles and exact

current-tip cardinality is explicit

supersession rule is deterministic and owner-authorized

correction/revocation authority is explicit

caller intent alone cannot mutate current memory applicability

NextActionProposal cannot define new authoritative action

eligible ActionRef/descriptor authority is exact and versioned

priority classification cannot be caller supplied

Task issuance boundary after NextActionSelection is explicit

all predecessor non-substitution rules remain

runtime remains NOT_STARTED

Git actions = none

Human verification = HUMAN_PENDING
```

---

# 15. export

Target:

```text
.aiassistant/reports/target/
20260830_1933_aiscc-p1-8-memory-authority-lineage-and-next-action-eligibility-design-rework-1/
```

Required:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
```

Include byte-preserving copies of:

```text
.aiassistant/rules/AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md

.aiassistant/records/aiscc/cycles/
20260830_1933_aiscc-p1-8-design-memory-authority-lineage-next-action-eligibility-hold-1.cycle.md

.aiassistant/tasks/done/
20260830_1933_aiscc-p1-8-memory-authority-lineage-and-next-action-eligibility-design-rework-1.md
```

Report actual source/copy SHA-256.

---

# 16. expected final state

Successful rework submission:

```text
P1-7:
ACCEPTED / CLOSED

P1-8 Design:
REWORKED_DESIGN_CANDIDATE / HUMAN_PENDING

P1-8 Runtime:
NOT_STARTED

P2:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

Command Center:

```text
review reworked design
→ PASS / HUMAN_FINAL_REVIEW_REQUIRED
or
→ HOLD_REWORK_REQUIRED
```

---

# 17. preserved exact paths

Preserve:

```text
.aiassistant/reports/aiscc/
20260830_1712_aiscc-p1-7-runtime-accepted-p1-8-command-center-handoff-1.md

.aiassistant/rules/
AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md

.aiassistant/records/aiscc/cycles/
20260830_1933_aiscc-p1-8-design-memory-authority-lineage-next-action-eligibility-hold-1.cycle.md

.aiassistant/tasks/done/
20260830_1909_aiscc-p1-8-project-memory-and-cycle-admission-design-1.md

.aiassistant/tasks/done/
20260830_1933_aiscc-p1-8-memory-authority-lineage-and-next-action-eligibility-design-rework-1.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```
