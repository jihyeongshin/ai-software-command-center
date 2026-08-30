# AISCC Cycle Record

## meta

- cycle_id: `20260830_2011_aiscc-p1-8-design-historical-source-current-applicability-separation-hold-1`
- date: `2026-08-30T20:11:00+09:00`
- phase: `P1-8 Project Memory and Cycle Admission Design`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1_8_PROJECT_MEMORY_CYCLE`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause: `HISTORICAL_SOURCE_AND_CURRENT_APPLICABILITY_CONFLATED`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260830_2011_aiscc-p1-8-design-historical-source-current-applicability-separation-hold-1.cycle.md`

## reviewed submission

```text
start/final HEAD:
4b84a9f66c148b198d3f4b6b01cffc4641fdceb1

predecessor design SHA:
ba1a8f5903b4bf7798fab81a07790a977185eff55ba4933ad51eae54985bea1d

reworked design SHA:
68d8b4a0317637698af85ee692f97468ba57e3a4c3d6c7b62f13d170d80133cd

corrected P1-7→P1-8 handoff:
0169b07642e72d1c7025c98946402e53102c3de2f72a4b3df78ba0ed851004c5

runtime implementation:
NOT_STARTED

Git add/commit/push:
0
```

Export byte identity independently verified:

```text
design:
68d8b4a0317637698af85ee692f97468ba57e3a4c3d6c7b62f13d170d80133cd

1933 HOLD Cycle:
305ec8c3d38f9faa8544c7e56227b4162d8ca14d29ae42c0eabf2744e287374d

1933 done Task:
e5fb8c7a4eb58225729d2b32a48f1a513bf7961e1fc4596b484b235333f38ba0

TASK.md:
e5fb8c7a4eb58225729d2b32a48f1a513bf7961e1fc4596b484b235333f38ba0

EXECUTOR_REPORT.md:
d81673a7ddd45bcc61185df2b62a96e00d4d62b3b8fdff3691c670d20f5730e0
```

## predecessor 1933 findings — review result

The 1933 design rework materially closes all three findings that motivated it.

Accepted as closed:

```text
MemoryDeclaration source-to-content authority
→ CLOSED

stable ProjectMemoryEntryId / MemoryLineageKey separation
→ CLOSED

explicit correction/supersession/revocation semantic authority
→ CLOSED

NextAction enrolled ActionRef/Descriptor eligibility
→ CLOSED

proposal priority/action laundering
→ CLOSED

Task issuance boundary
→ CLOSED
```

Particularly accepted:

```text
LESSON
→ V1 NOT_SUPPORTED

ProjectMemoryEntryId != MemoryLineageKey

one CURRENT tip per MemoryLineageKey

EXPLICIT_SUPERSESSION_ONLY

caller mutation intent != mutation authority

deterministic ranking != action authority

NextActionSelection
→ TaskIssuanceCandidate
→ EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY
→ TaskContract
```

These findings are not to be reopened absent regression.

---

# load-bearing finding — historical source validity is conflated with current source applicability

The reworked design correctly states:

```text
historically admitted != currently applicable
historical memory validity != current memory applicability
```

and P1-6/P1-7 predecessor design/runtime already froze the same historical/current distinction.

However §9.2 `Common source-to-content verification` requires for every
`STRUCTURED_RESULT_ATTESTED` declaration:

```text
current applicable AdmittedEvidence ref/authority revision
```

This is incompatible with the downstream timing of P1-8 Cycle admission.

## why this is load-bearing

P1-8 `AdmittedCycle` is created only after:

```text
P1-7 Judgment = ACCEPTED
P1-4 terminal TransitionDecision → WorkflowState.ACCEPTED
```

The P1-6 evidence that justified that accepted lineage is bound to the predecessor checkpoint/source state and
may no longer be **currently effective** after the WorkRun state/version advances.

P1-6/P1-7 already distinguish:

```text
valid historical evidence issuance
!= current effective evidence
```

A historical source may also later be:

```text
REVOKED
SUPERSEDED
CORRECTED
freshness-expired
```

without erasing the fact that it was validly admitted and consumed at the accepted terminal epoch.

Therefore:

```text
current applicable P1-6 evidence
```

cannot be the identity criterion for historical Cycle/source authority.

## required exact separation

P1-8 must freeze two different questions.

### A. Cycle / memory content historical source provenance

For `STRUCTURED_RESULT_ATTESTED`, CycleEvaluation must prove that the exact structured result:

```text
was validly admitted by P1-6 at the exact historical checkpoint/state/version

was included in the exact evidence attestation/root consumed by the accepted Judgment / terminal transition
when the TaskContract required it

has exact immutable AdmittedEvidence / content / schema / field-path provenance
```

This check must use projection-independent historical P1-6 provenance.

It must NOT require that the evidence is still current/effective at Cycle admission/replay time.

### B. ProjectMemory current applicability

After historical source validity is proven, P1-8 separately evaluates whether the source is currently:

```text
CURRENT
SUPERSEDED
REVOKED
EXPIRED
CORRECTED
```

according to exact owner events/current applicability policy.

This result controls:

```text
ProjectMemoryEntry current applicability
retrieval eligibility
NextAction contextual use
```

It does not rewrite historical Cycle admission.

Required invariant:

```text
historical source provenance
!= current source effectiveness
!= current ProjectMemory applicability
```

---

# required lifecycle semantics

The design must explicitly choose and freeze behavior for these cases.

## case 1 — valid at terminal and still current at P1-8 admission

```text
historical source provenance:
VALID

current source applicability:
CURRENT

AdmittedCycle:
ADMITTED

ProjectMemoryEntry:
CURRENT
```

## case 2 — valid at terminal, later invalidated before delayed/replayed P1-8 admission

Example:

```text
accepted WorkRun / Judgment / terminal transition completed

then source owner emits:
REVOKED / SUPERSEDED / CORRECTED

then P1-8 reconstructs/admit-replays the historical Cycle
```

Required behavior must preserve history.

Recommended V1:

```text
historical source provenance:
VALID

AdmittedCycle:
ADMITTED as historical accepted provenance

ProjectMemoryEntry:
created/projected with current applicability derived immediately from source-owner events
→ REVOKED / SUPERSEDED / EXPIRED as appropriate
→ never exposed as CURRENT
```

If the design chooses not to materialize a non-current ProjectMemoryEntry, it must still preserve an exact
historical Cycle/declaration projection record sufficient to reconstruct why it is not current.

Do not reject the historical Cycle merely because current source authority changed after the terminal epoch.

## case 3 — source was never valid at terminal

```text
source was already invalid/rejected/revoked
before the exact accepted Judgment/terminal transition

or

the source ref was not part of the exact consumed P1-6 attestation/root
```

Required:

```text
Cycle admission:
REJECT

CYCLE_EVIDENCE_BINDING_MISMATCH
or exact typed historical-source provenance error
```

Current source repair cannot retroactively make the old terminal epoch valid.

---

# deterministic source snapshot

Freeze exact source time/revision semantics.

Cycle candidate/evaluation must bind at minimum:

```text
historical evidence attestation ref/version
historical evidence authority revision
historical checkpoint ref/version/fingerprint
historical admitted evidence ref/version
content ref/hash/schema/canonicalization
exact accepted Judgment ref/version
exact terminal TransitionDecision ref/version
terminal epoch state/version
```

Current applicability evaluation must separately bind:

```text
source authority event sequence/revision
ProjectMemory lineage revision
evaluation observed_at / admitted_at
```

Do not put current applicability state into the historical content fingerprint in a way that changes the
immutable content identity.

---

# replay semantics

Freeze:

```text
same historical Cycle ID + same historical source fingerprint
→ same immutable AdmittedCycle replay
```

even if current source applicability has changed.

The replay may produce/rebuild a different **current applicability projection** as later owner events are
folded, but it must not create a different historical Cycle identity.

Required:

```text
historical replay identity first
→ current applicability projection second
```

---

# correction/source invalidation relation

Preserve §12 source invalidation semantics, but explicitly connect them to the above boundary.

A later P1-4/P1-6/P1-7/canonical source owner:

```text
correction
supersession
revocation
```

must:

```text
not erase old AdmittedCycle
not mutate old ProjectMemoryEntry content
append an applicability/correction authority event
update/rebuild current ProjectMemoryView
```

If a source correction creates different semantic content, a new accepted Cycle plus explicit supersession
authority is still required for the replacement content under the existing `EXPLICIT_SUPERSESSION_ONLY` rule.

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

No Human final P1-8 design review should occur until this historical/current source boundary is explicit.

## preserved exact paths

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
```
