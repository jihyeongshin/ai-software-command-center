# 작업지시서: P1-8 Historical Source vs Current Applicability Design Rework

## meta

- task_id: `20260830_2011_aiscc-p1-8-historical-source-and-current-applicability-separation-design-rework-1`
- created_at: `2026-08-30T20:11:00+09:00`
- phase: `P1-8 Project Memory and Cycle Admission`
- work_type: `DESIGN_REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1_8_PROJECT_MEMORY_CYCLE`
- expected_start_head: `4b84a9f66c148b198d3f4b6b01cffc4641fdceb1`
- predecessor_design_sha256: `68d8b4a0317637698af85ee692f97468ba57e3a4c3d6c7b62f13d170d80133cd`
- corrected_p1_7_handoff_sha256: `0169b07642e72d1c7025c98946402e53102c3de2f72a4b3df78ba0ed851004c5`
- p1_8_design_status: `HOLD_REWORK_REQUIRED / HUMAN_PENDING`
- p1_8_runtime_status: `NOT_STARTED`

---

# 1. purpose

Rework only the historical-source/current-applicability conflation identified by Command Center.

The 1933 findings are considered CLOSED:

```text
MemoryDeclaration source-to-content authority
MemoryLineageKey
correction/supersession authority
NextAction enrolled ActionRef eligibility
Task issuance boundary
```

Do not redesign them.

Place/preserve:

```text
.aiassistant/records/aiscc/cycles/
20260830_2011_aiscc-p1-8-design-historical-source-current-applicability-separation-hold-1.cycle.md
```

---

# 2. mandatory preflight

Require:

```text
HEAD ==
4b84a9f66c148b198d3f4b6b01cffc4641fdceb1

sha256(.aiassistant/rules/AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md)
==
68d8b4a0317637698af85ee692f97468ba57e3a4c3d6c7b62f13d170d80133cd

corrected P1-7 handoff SHA ==
0169b07642e72d1c7025c98946402e53102c3de2f72a4b3df78ba0ed851004c5
```

Mismatch:

```text
STOP
→ REVIEWED_DESIGN_DRIFT
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
20260830_2011_aiscc-p1-8-historical-source-and-current-applicability-separation-design-rework-1.md

→

.aiassistant/tasks/done/
20260830_2011_aiscc-p1-8-historical-source-and-current-applicability-separation-design-rework-1.md
```

Temporary export only:

```text
.aiassistant/reports/target/
20260830_2011_aiscc-p1-8-historical-source-and-current-applicability-separation-design-rework-1/**
```

No runtime source/test/migration.

No canonical state update.

---

# 4. exact design correction — historical structured-result authority

In §9.2 and every related section, remove/replace the requirement that a
`STRUCTURED_RESULT_ATTESTED` source must be:

```text
current applicable AdmittedEvidence
```

as the criterion for historical Cycle admission.

Freeze an exact equivalent of:

```text
HistoricalStructuredResultAuthority
```

or use existing P1-6 terms directly.

The exact source contract must require immutable projection-independent P1-6 provenance equivalent to:

```text
EvidenceRequirement ref/version/fingerprint

EvidenceCheckpoint ref/version/fingerprint

EvidenceSetSatisfactionAttestation ref/version
that was valid at the exact historical terminal lineage

AdmittedEvidence ref/version
whose complete historical P1-6 issuance provenance is valid

EvidenceContentRef object/version/hash/schema/canonicalization/byte-count

structured result schema ID/version
field path or object ref
canonical structured bytes

same TaskContract / WorkRun / checkpoint / state-version
same accepted Judgment / terminal TransitionDecision evidence binding
```

CycleEvaluation must consume P1-6 historical provenance, not P1-6 current-effectiveness projection.

Required non-substitution:

```text
historically valid P1-6 source
!= currently effective P1-6 source
```

---

# 5. terminal-epoch source binding

Cycle eligibility already requires exact accepted P1-6/Judgment/TransitionDecision refs.

Strengthen/clarify that a structured memory source is eligible only when it was part of the exact historical
authority consumed by the accepted terminal lineage.

At minimum:

```text
MemoryDeclaration source admitted-evidence ref
must belong to the exact historical evidence attestation/root referenced by the accepted Judgment/terminal
TransitionDecision when evidence was required
```

If a category legitimately uses an accepted structured result that the TaskContract marks optional for terminal
acceptance, freeze the exact separate eligibility rule.

Do not permit:

```text
some evidence was valid in the same WorkRun
```

to substitute for:

```text
this exact structured result was an accepted source under the Cycle memory policy
```

---

# 6. three-way state separation

Add one normative section/table that separates:

```text
A. Historical Source Provenance
B. Historical AdmittedCycle / ProjectMemoryEntry Content
C. Current ProjectMemory Applicability
```

Required exact semantics:

| Dimension | Mutable/current? | Authority |
|---|---:|---|
| historical source issuance | immutable historical | P1-4/P1-6/P1-7/canonical source owner |
| AdmittedCycle identity/content | immutable historical | P1-8 Cycle admission over exact predecessor provenance |
| ProjectMemoryEntry identity/content | immutable historical | deterministic P1-8 projection |
| ProjectMemory applicability | current rebuildable projection | append-only P1-8 applicability events consuming source-owner authority |

Required non-substitution:

```text
historical source validity
!= current source effectiveness
!= current memory applicability
```

---

# 7. delayed admission / replay cases

Freeze exact behavior.

## 7.1 source valid then and still current

```text
historical source:
VALID

AdmittedCycle:
ADMITTED

memory:
CURRENT
```

## 7.2 source valid at terminal but now revoked/superseded/expired

Required V1 behavior:

```text
historical source:
VALID

AdmittedCycle:
ADMITTED / replayable

historical ProjectMemoryEntry:
preserved

current applicability:
REVOKED / SUPERSEDED / EXPIRED
as determined by exact source-owner events/policy

retrieval default:
not returned

NextAction current context:
not usable
```

If the current design creates the entry and applicability event in one admission transaction, state the exact
ordering.

Recommended:

```text
historical entry creation
→ fold source-owner applicability events as-of admission observation
→ write/rebuild non-CURRENT projection
```

Do not temporarily expose it as CURRENT.

## 7.3 source never valid at terminal

```text
historical source provenance:
INVALID

Cycle admission:
REJECTED

no ProjectMemoryEntry
```

Use existing `CYCLE_EVIDENCE_BINDING_MISMATCH` where exact, or add a narrowly named historical-source code.

---

# 8. source correction after Cycle admission

Preserve append-only semantics.

Freeze:

```text
source owner correction/revocation/supersession
→ does not rewrite old AdmittedCycle
→ does not rewrite ProjectMemoryEntry content
→ creates/feeds exact ProjectMemoryAuthorityEvent
→ changes current ProjectMemoryView only
```

Different replacement semantic content:

```text
requires a new accepted Cycle
+ valid explicit supersession authority
```

under the existing `EXPLICIT_SUPERSESSION_ONLY` rule.

---

# 9. historical replay ordering

Add exact idempotency order:

```text
existing cycle ID/request
→ verify immutable historical Cycle/source provenance
→ same fingerprint: return same historical object
→ different fingerprint: typed identity conflict
→ current applicability reconstructed separately afterward
```

A later source revocation/currentness change must not change historical Cycle fingerprint or turn same-proposal
replay into a different Cycle identity.

Likewise:

```text
ProjectMemoryEntryId/content fingerprint
```

must not contain current applicability state/revision.

---

# 10. source snapshots/revisions

Freeze what is historical identity vs current observation.

Historical identity includes at minimum:

```text
source object immutable refs/fingerprints
P1-6 authority revision at historical issuance
checkpoint/state/version
Judgment/TransitionDecision refs
content/schema/canonicalization
```

Current applicability observation includes:

```text
latest source-owner authority-event revision/sequence
memory lineage applicability revision
as-of observation timestamp/sequence
```

Do not conflate these fields in one fingerprint.

---

# 11. deterministic retrieval / Next Action implications

Preserve:

```text
default deterministic retrieval
→ CURRENT ProjectMemory only
```

Explicit historical retrieval may return non-current entries with state/reason.

NextAction `CYCLE_DERIVED` current context must use only current applicable memory.

Historical AdmittedCycle existence alone must not make revoked/superseded/expired memory a current
NextAction input.

`OPERATIONAL_RECOVERY` remains independent source-domain handling and is not changed by this Task.

---

# 12. required design proof examples

Add/report at least:

## 12.1 terminal-valid but current-stale positive historical replay

```text
structured result validly admitted at state vN
→ consumed by accepted Judgment/terminal transition
→ WorkRun advances / evidence later becomes non-current

historical Cycle admission/replay
→ succeeds with same Cycle identity

current ProjectMemory applicability
→ non-CURRENT according to later source event
```

## 12.2 source invalid before terminal negative

```text
structured result revoked before exact accepted terminal evidence binding
or not part of the consumed attestation/root

→ Cycle admission reject
```

## 12.3 no temporary CURRENT exposure

```text
delayed Cycle admission observes source already REVOKED
→ ProjectMemoryEntry is never externally visible as CURRENT
```

---

# 13. error vocabulary

Reuse existing codes where exact.

If additional clarity is required, add narrowly typed equivalents such as:

```text
CYCLE_HISTORICAL_SOURCE_PROVENANCE_INVALID
CYCLE_SOURCE_CURRENTNESS_NOT_AUTHORITY
```

Do not create a code implying that ordinary current staleness invalidates historical Cycle identity.

---

# 14. predecessor authority

Do not alter:

```text
P1-4 transition authority

P1-6 admission/currentness semantics

P1-7 Human/Judgment semantics

1933 MemoryDeclaration authority modes

MemoryLineageKey / EXPLICIT_SUPERSESSION_ONLY

NextAction enrolled descriptor eligibility

external Task issuance boundary
```

If exact historical source verification requires a P1-6 semantic change:

```text
STOP
→ POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

The accepted P1-6 runtime already has projection-independent historical provenance verification; P1-8 should
consume it.

---

# 15. forbidden

No:

```text
src/**
tests/**
migrations/**

canonical state updates

P1-8 runtime implementation

P2/P3

Self-Dogfooding

provider/network/credential/deployment

Git add/commit/push
```

Do not modify corrected P1-7 handoff.

---

# 16. evidence contract

## executor_required

```text
DESIGN_HISTORICAL_SOURCE_PROVENANCE
DESIGN_CURRENT_APPLICABILITY_SEPARATION
DESIGN_DELAYED_ADMISSION
DESIGN_HISTORICAL_REPLAY
DESIGN_SOURCE_INVALIDATION
DESIGN_CURRENT_RETRIEVAL
STATIC_GOVERNANCE
```

## human_owned

```text
P1-8 design final review
→ HUMAN_PENDING
```

---

# 17. accept criteria

All must hold:

```text
STRUCTURED_RESULT_ATTESTED no longer requires current P1-6 effectiveness as historical identity

exact historical P1-6 source provenance is required

source must bind to exact terminal accepted authority when required

historical source / AdmittedCycle / current applicability are explicitly separated

valid-at-terminal but later stale/revoked source preserves historical Cycle identity

such memory is not exposed as CURRENT

invalid-at-terminal source rejects Cycle admission

source owner invalidation updates applicability append-only

same historical replay identity survives later currentness changes

current applicability is excluded from immutable content/Cycle identity fingerprints

deterministic retrieval/NextAction use only CURRENT memory

1933 findings remain unchanged/closed

runtime remains NOT_STARTED

Git actions = none

Human verification = HUMAN_PENDING
```

---

# 18. export

Target:

```text
.aiassistant/reports/target/
20260830_2011_aiscc-p1-8-historical-source-and-current-applicability-separation-design-rework-1/
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
20260830_2011_aiscc-p1-8-design-historical-source-current-applicability-separation-hold-1.cycle.md

.aiassistant/tasks/done/
20260830_2011_aiscc-p1-8-historical-source-and-current-applicability-separation-design-rework-1.md
```

Report actual source/copy SHA-256.

---

# 19. expected final state

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

# 20. preserved exact paths

Preserve:

```text
.aiassistant/reports/aiscc/
20260830_1712_aiscc-p1-7-runtime-accepted-p1-8-command-center-handoff-1.md

.aiassistant/rules/
AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md

.aiassistant/records/aiscc/cycles/
20260830_1933_aiscc-p1-8-design-memory-authority-lineage-next-action-eligibility-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260830_2011_aiscc-p1-8-design-historical-source-current-applicability-separation-hold-1.cycle.md

.aiassistant/tasks/done/
20260830_1909_aiscc-p1-8-project-memory-and-cycle-admission-design-1.md

.aiassistant/tasks/done/
20260830_1933_aiscc-p1-8-memory-authority-lineage-and-next-action-eligibility-design-rework-1.md

.aiassistant/tasks/done/
20260830_2011_aiscc-p1-8-historical-source-and-current-applicability-separation-design-rework-1.md
```
