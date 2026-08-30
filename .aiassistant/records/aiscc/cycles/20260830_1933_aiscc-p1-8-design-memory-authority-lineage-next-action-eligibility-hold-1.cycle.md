# AISCC Cycle Record

## meta

- cycle_id: `20260830_1933_aiscc-p1-8-design-memory-authority-lineage-next-action-eligibility-hold-1`
- date: `2026-08-30T19:33:00+09:00`
- phase: `P1-8 Project Memory and Cycle Admission Design`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1_8_PROJECT_MEMORY_CYCLE`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause: `MEMORY_AUTHORITY_LINEAGE_AND_NEXT_ACTION_ELIGIBILITY_UNDER_SPECIFIED`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260830_1933_aiscc-p1-8-design-memory-authority-lineage-next-action-eligibility-hold-1.cycle.md`

## reviewed submission

```text
start/final HEAD:
4b84a9f66c148b198d3f4b6b01cffc4641fdceb1

corrected P1-7→P1-8 handoff:
0169b07642e72d1c7025c98946402e53102c3de2f72a4b3df78ba0ed851004c5

P1-8 design candidate:
.aiassistant/rules/AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md

design SHA-256:
ba1a8f5903b4bf7798fab81a07790a977185eff55ba4933ad51eae54985bea1d

runtime implementation:
NOT_STARTED

Git add/commit/push:
0
```

Export source/copy identity independently verified:

```text
design candidate:
ba1a8f5903b4bf7798fab81a07790a977185eff55ba4933ad51eae54985bea1d

done Task:
ccad55a911449adaa8b797a401c2c0f9656d2c87a749f703c73896c184a7bf83

TASK.md:
ccad55a911449adaa8b797a401c2c0f9656d2c87a749f703c73896c184a7bf83

EXECUTOR_REPORT.md:
7ccd510a1ab5902d4cc72d83572d6f2fc81d012aaacd89ac7ad6d54eb4c63584
```

## accepted design strengths

The design correctly freezes:

```text
CommandCenterCycleRecord != AdmittedCycle
raw session != ProjectMemoryEntry
Judgment != CycleAdmissionDecision
TransitionDecision != CycleAdmissionDecision
ProjectMemory != canonical policy authority
NextActionProposal != NextActionSelection != TransitionDecision
historical admission != current applicability
```

It also correctly preserves:

```text
P1-4 transition ownership
P1-6 evidence ownership
P1-7 Human/Judgment ownership

accepted-only AdmittedCycle eligibility
rejected/HOLD/failed/rework exclusion from reusable memory
append-only correction model
PostgreSQL restart/fail-closed direction
deterministic V1 retrieval
System-owned deterministic NextActionSelection
P2/P3/Self-Dogfooding boundaries
```

These portions should be preserved unless the narrow findings below require an exact clarification.

---

# FINDING-1 — accepted WorkRun can still launder arbitrary structured MemoryDeclaration content

Current design allows:

```text
CycleCandidate:
callable by Agent / Human / executor / System component

MemoryDeclaration:
typed structured memory request
```

and requires:

```text
category
project scope
subject key
applicability predicate
typed content payload
exact source refs
privacy class
```

But it does not define a load-bearing relation proving that the **typed content payload itself** is
authoritatively derived from, or exactly attested by, the cited source.

For example `LESSON` requires only:

```text
accepted artifact/provenance ref
```

and `NEXT_ACTION_CONTEXT` requires:

```text
accepted Cycle source + policy allowlist
```

This prevents raw prose admission in name, but it does not prevent:

```text
accepted WorkRun
+ legitimate artifact ref
+ arbitrary caller-authored structured payload
→ ProjectMemoryEntry
```

The same problem exists for `DECISION` unless the structured result artifact is required to contain the exact
decision payload/fingerprint being projected.

Required invariant:

```text
accepted source ref
!= authority for arbitrary memory content
```

P1-8 must freeze an exact per-category `MemoryDeclarationAuthorityPolicy`.

At minimum each category needs one of:

```text
DETERMINISTIC_POINTER
→ content is mechanically derived from exact immutable source fields

STRUCTURED_RESULT_ATTESTED
→ exact content/fingerprint exists in a TaskContract-authorized structured result artifact

OWNER_ATTESTED
→ exact content/fingerprint is attested by a defined owner authority
```

V1 must not admit a category whose semantic content cannot be proven through one of the accepted modes.

Especially:

```text
LESSON
```

must not mean “Agent writes a nice lesson and cites an accepted artifact.”

If no exact structured/owner-backed source exists:

```text
LESSON declaration
→ reject / NOT_SUPPORTED in V1
```

is acceptable and safer than semantic inference.

CycleEvaluation must verify:

```text
declaration content fingerprint
== exact source-derived / source-attested fingerprint
```

not only ref existence and schema.

---

# FINDING-2 — ProjectMemoryEntry has no stable lineage identity or exact supersession authority

Current immutable entry key is:

```text
(project_id, cycle_id, memory_declaration_ordinal, category, subject_key, content_fingerprint)
```

This uniquely identifies an entry, but every new Cycle necessarily creates a new identity.

The design then says:

```text
SUPERSEDED:
a newer accepted entry replaces an older entry with the same subject/applicability
```

and:

```text
one current lineage tip only
```

but does not define a stable cross-Cycle lineage key that determines which entries are in the same semantic
lineage.

Required invariant:

```text
entry identity
!= memory lineage identity
```

Freeze a stable exact equivalent of:

```text
MemoryLineageKey =
(project_id, category, subject_key, applicability_key, semantic_slot)
```

where every field and normalization rule is deterministic and versioned.

The design must decide:

```text
Can multiple CURRENT entries exist for one lineage?
If no, what exact unique constraint/projection key prevents it?

Does a later accepted entry auto-supersede the current tip?
If yes, what exact declaration/policy proves replacement semantics?

Can an unrelated accepted Cycle with the same subject/category accidentally supersede memory?
Must be NO.
```

Also define the authority for:

```text
CORRECTION
SUPERSESSION
REVOCATION
```

Current `correction/supersession intent` is part of caller candidate fingerprint, but the design does not say who
is authorized to make that intent effective.

Required:

```text
caller correction intent
!= correction authority
```

At minimum freeze exact sources such as:

```text
source-owner correction/revocation event

or

P1-8 deterministic supersession policy over exact MemoryLineageKey

or

separate owner-authorized correction attestation
```

with exact precedence.

A random Agent/executor CycleCandidate must not be able to supersede/revoke current memory by setting intent
fields.

---

# FINDING-3 — arbitrary NextActionProposal can be authority-laundered by deterministic selection

The design correctly separates:

```text
NextActionProposal
!= NextActionEvaluation
!= NextActionSelection
!= TransitionDecision
```

and correctly makes `NextActionSelection` System-owned.

However the selected action itself is currently described as:

```text
selected proposal/action
or issued-Task candidate ref
```

while:

```text
Agent / Human / executor / System component
```

may all submit proposals.

The design defines deterministic priority and tie-breaks, but it does not freeze an **action eligibility
authority** that constrains what a proposal is allowed to introduce.

Therefore a deterministic selector could still produce authoritative:

```text
NextActionSelection
```

from an arbitrary caller-defined action payload, even though the selector itself behaved deterministically.

Required invariant:

```text
deterministic selection
!= authoritative action eligibility
```

Freeze exact V1 action eligibility.

Recommended shape:

```text
NextActionDescriptor / ActionRef
```

must already be enrolled by a versioned authoritative source such as:

```text
NextActionSelectionPolicy action catalog

accepted canonical roadmap item

TaskContract-defined follow-up action/template

owner-authorized blocker recovery action
```

A `NextActionProposal` may nominate/bind parameters to an eligible action ref but must not define new action
authority.

For every proposal/selection define:

```text
action_ref
action_kind
parameter schema/version
allowed project/scope
source authority ref/hash
required Human gate if any
Task issuance owner
```

Novel/unregistered action:

```text
→ NEXT_ACTION_HUMAN_INPUT_REQUIRED
or
→ NEXT_ACTION_ACTION_NOT_ENROLLED
```

not System selection.

Priority, blocker classification, and critical-path rank must be derived from authoritative policy/source facts,
not caller-supplied proposal claims.

---

# command-center judgment

```text
P1-7:
ACCEPTED / CLOSED

P1-8 Design:
HOLD_REWORK_REQUIRED / HUMAN_PENDING

P1-8 Runtime:
NOT_STARTED

P2:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

No runtime implementation is authorized.

No Human final P1-8 design review should occur until these three findings are closed.

## preserved exact paths

Preserve:

```text
.aiassistant/reports/aiscc/
20260830_1712_aiscc-p1-7-runtime-accepted-p1-8-command-center-handoff-1.md

.aiassistant/rules/
AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md

.aiassistant/tasks/done/
20260830_1909_aiscc-p1-8-project-memory-and-cycle-admission-design-1.md

.aiassistant/records/aiscc/cycles/
20260830_1933_aiscc-p1-8-design-memory-authority-lineage-next-action-eligibility-hold-1.cycle.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```
