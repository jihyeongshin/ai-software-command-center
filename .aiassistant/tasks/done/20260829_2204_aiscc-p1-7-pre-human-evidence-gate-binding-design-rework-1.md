# 작업지시서: P1-7 PRE_HUMAN Evidence / HumanGate Binding Design Rework

## meta

- task_id: `20260829_2204_aiscc-p1-7-pre-human-evidence-gate-binding-design-rework-1`
- created_at: `2026-08-29`
- phase: `P1-7 Human Gate and Judgment`
- work_type: `REWORK / DOC_BASELINE_UPDATE`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1-7_HUMAN_JUDGMENT`
- expected_start_head: `fc30aa3151494e15b132f8c48be8ca2c1bf8855d`
- predecessor_design_candidate_sha256: `01cf086c5c996a674c696aaf76522f7e139684d1115356f22179b583a0b74d1c`
- p1_7_runtime_status: `NOT_STARTED`
- p1_8_status: `NOT_STARTED`

---

# 1. current state

Existing design candidate:

```text
.aiassistant/rules/AISCC_HUMAN_GATE_JUDGMENT.md
```

Current status remains:

```text
DESIGN_CANDIDATE / HUMAN_REVIEW_PENDING
```

Command Center judgment:

```text
HOLD_REWORK_REQUIRED
```

HOLD reason is narrow:

```text
PRE_HUMAN P1-6 EvidenceSetSatisfactionAttestation is declared a required gate-open
policy input, but G_HUMAN_REQUIRED does not yet bind/verify that authority.
```

Do not rewrite the design broadly.

---

# 2. preserve already-accepted candidate decisions

Do not reopen unless this exact fix requires it:

```text
exact P1-4 P1_7_HUMAN / P1_7_JUDGMENT guard slots

HumanGate:
system-owned

V1 gate multiplicity:
one current gate per current HUMAN_REQUIRED authority epoch

HumanResultKind:
APPROVE | REWORK | REJECT

JudgmentKind:
ACCEPTED | REJECTED | HOLD_REWORK_REQUIRED

HUMAN_DIRECT_EVIDENCE != HUMAN_P1_7

HumanResult != Judgment

Judgment != TransitionDecision

G_EVIDENCE != G_HUMAN_* != G_JUDGMENT_*

concurrent HumanResult winner:
FIRST_DURABLY_ADMITTED

V1 policy exception/override:
NOT_SUPPORTED

Agent/LLM proposal:
non-authoritative historical provenance only

P1-4:
exclusive TransitionDecision/WorkflowState mutation owner
```

---

# 3. exact finding to close

Current candidate section 12 declares:

```text
PRE_HUMAN_EVIDENCE
→ P1-6 EvidenceSetSatisfactionAttestation
→ gate-open policy input
→ HUMAN_REQUIRED
```

but current `G_HUMAN_REQUIRED` authority does not bind that P1-6 attestation.

This is a semantic authority gap.

Required relationship:

```text
P1-6 PRE_HUMAN EvidenceSetSatisfactionAttestation
!= G_HUMAN_REQUIRED

but

current effective PRE_HUMAN attestation
→ mandatory owner-backed input to G_HUMAN_REQUIRED
```

P1-7 may verify/consume P1-6 authority.
P1-7 must not reproduce P1-6 evidence evaluation or mint P1-6 truth.

---

# 4. design changes required

Update only the sections necessary to freeze the following.

## 4.1 HumanGate open prerequisite

Before a gate-open `G_HUMAN_REQUIRED` attestation may be issued, define exact current prerequisite:

```text
PRE_HUMAN_EVIDENCE checkpoint ref/version
current EvidenceSetSatisfactionAttestation ref/version
P1-6 authority version
TaskContract id/version
work_run_id
source WorkflowState/state_version
target state / transition-purpose identity
RequirementSet id/version/root
checkpoint-applicable subset/root
evidence authority revision
satisfied=true
effective/not-revoked/not-superseded
```

Exact values must match the intended gate-opening P1-4 transition use.

## 4.2 `HumanGuardAttestation` binding

For `G_HUMAN_REQUIRED`, add exact conditional fields equivalent to:

```text
pre_human_evidence_attestation_ref
pre_human_checkpoint_ref
pre_human_requirement_set_root
pre_human_applicable_subset_root
pre_human_evidence_authority_revision
pre_human_p1_6_authority_version
```

Do not add these as meaningless nullable fields to all Human guards unless a clean typed/conditional
binding model is explicitly defined.

The design should prefer a typed guard-specific payload or exact `G_HUMAN_REQUIRED` payload extension.

## 4.3 `G_HUMAN_REQUIRED` predicate

Freeze predicate equivalent to:

```text
G_HUMAN_REQUIRED is current only if:

- TaskContract/use requires Human handling
- reserved HumanGate identity/policy is current
- exact PRE_HUMAN checkpoint for this gate-opening use is System-owned/current
- exact P1-6 pre-Human satisfaction attestation is current/effective
- attestation TaskContract/work_run/source state/state_version/target-use match
- RequirementSet/full root/applicable subset root match current authority
- evidence authority revision matches current P1-6 authority
- P1-6 attestation has not expired/revoked/superseded
- HumanGate can be atomically opened with the admitted P1-4 transition
```

Wrong/missing/stale pre-Human authority:

```text
→ G_HUMAN_REQUIRED verifier reject
→ no gate open
→ no HUMAN_REQUIRED transition
```

## 4.4 no-applicable-pre-Human-evidence case

Resolve explicitly.

Read accepted P1-6 semantics first and choose the rule that they support.

Preferred deterministic V1 model:

```text
Every Human-required transition-purpose has a System-owned PRE_HUMAN_EVIDENCE checkpoint.

If its applicable required subset is empty:
→ P1-6 still evaluates the exact checkpoint
→ SATISFIED empty subset/root
→ issues exact EvidenceSetSatisfactionAttestation
→ G_HUMAN_REQUIRED binds that attestation
```

This gives one uniform authority path and avoids a caller-controlled "no evidence needed" shortcut.

If current P1-6 runtime/design cannot issue an attestation for an empty applicable subset:

```text
STOP
→ POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

Do not invent a second P1-7-only no-evidence authority path.

## 4.5 authority freshness / replay

Freeze:

```text
pre-Human attestation becomes stale/superseded
before P1-4 guard use
→ old G_HUMAN_REQUIRED unusable

new WorkRun state_version
→ old G_HUMAN_REQUIRED unusable

different HumanGate transition-purpose
→ old pre-Human attestation cannot be rebound

P1-6 evidence-authority revision changes
→ G_HUMAN_REQUIRED must re-evaluate current P1-6 authority
```

P1-7 process-local cache is not enough.

## 4.6 shared transaction boundary

Preserve:

```text
run:{work_run_id} advisory transaction lock
+ WorkRunRow FOR UPDATE
```

Design exact order for gate-open transition:

```text
P1-7 verifies current P1-6 PRE_HUMAN authority
→ issues current G_HUMAN_REQUIRED fact
→ P1-4 evaluates transition
→ if ADMITTED:
   gate open event + WorkRun HUMAN_REQUIRED/state_version+1
   in same transaction
```

If P1-6 attestation can change independently under the same WorkRun lock, the later implementation
must re-read current P1-6 authority inside the shared transaction.

---

# 5. proof matrix additions

Add an explicit future proof class:

```text
PRE_HUMAN_EVIDENCE_GATE_BINDING
```

Mandatory future proofs:

```text
missing PRE_HUMAN attestation
→ no G_HUMAN_REQUIRED
→ no gate
→ no HUMAN_REQUIRED transition

wrong checkpoint
→ reject

wrong TaskContract
→ reject

wrong WorkRun
→ reject

wrong source state/version
→ reject

wrong target/use
→ reject

wrong RequirementSet root
→ reject

wrong applicable subset root
→ reject

stale/superseded evidence authority revision
→ reject

effective current PRE_HUMAN attestation
+ exact Human policy/gate reservation
→ G_HUMAN_REQUIRED may be issued

empty applicable required subset
→ exact P1-6 SATISFIED checkpoint attestation still required and bound

pre-Human attestation changes concurrently
→ stale G_HUMAN_REQUIRED cannot admit transition
```

Do not treat `POST_HUMAN_EVIDENCE_NON_DEADLOCK` as a substitute for this proof.

---

# 6. required source/canonical inspection

Before editing, re-read:

```text
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_HUMAN_GATE_JUDGMENT.md
```

Inspect exact current P1-6 behavior necessary to verify:

```text
PRE_HUMAN_EVIDENCE checkpoint creation
empty applicable subset evaluation
EvidenceSetSatisfactionAttestation issuance
effective-attestation reload/current authority verification
shared WorkRun lock
```

Likely exact symbols under:

```text
src/aiscc/evidence/checkpoints.py
src/aiscc/evidence/set_evaluator.py
src/aiscc/evidence/attestation.py
src/aiscc/evidence/repository.py
```

If empty-subset attestation is not supported or accepted semantics differ materially:

```text
STOP
→ POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

---

# 7. allowed changes

Primary:

```text
.aiassistant/rules/AISCC_HUMAN_GATE_JUDGMENT.md
```

Task/report lifecycle:

```text
.aiassistant/records/aiscc/cycles/
20260829_2204_aiscc-p1-7-pre-human-evidence-gate-binding-hold-1.cycle.md

.aiassistant/tasks/active/
20260829_2204_aiscc-p1-7-pre-human-evidence-gate-binding-design-rework-1.md

.aiassistant/tasks/done/
20260829_2204_aiscc-p1-7-pre-human-evidence-gate-binding-design-rework-1.md

.aiassistant/reports/target/
20260829_2204_aiscc-p1-7-pre-human-evidence-gate-binding-design-rework-1/**
```

No runtime/source/test/migration mutation.

---

# 8. forbidden

Do not modify:

```text
src/**
tests/**
migrations/**

.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

No:

```text
git add
git commit
git push
P1-7 runtime implementation
P1-8 work
provider/network/credential action
```

---

# 9. evidence contract

executor_required:

```text
STATIC_CANONICAL_INSPECTION
PRE_HUMAN_BINDING_DESIGN
DESIGN_CONSISTENCY
DOCUMENT_VALIDATION
```

reuse_allowed:

```text
all unaffected decisions from 2204 predecessor candidate
```

human_owned:

```text
P1-7 final design review
→ HUMAN_PENDING
```

not_required:

```text
unit/integration/PostgreSQL runtime
browser/provider/deployment
```

forbidden:

```text
runtime implementation
Git commit
P1-8
```

proof_non_substitution:

```text
PRE_HUMAN EvidenceSetSatisfactionAttestation
!= G_HUMAN_REQUIRED

but

P1-7 policy statement "evidence satisfied"
!= P1-6 authoritative attestation
```

---

# 10. accept criteria

All must hold:

```text
predecessor design SHA verified

P1-6 empty-subset PRE_HUMAN behavior verified from current source

G_HUMAN_REQUIRED binds exact current PRE_HUMAN attestation authority

missing/stale/wrong pre-Human authority rejects gate-open guard

no alternate P1-7-only no-evidence shortcut

shared run transaction freshness semantics defined

future proof matrix includes PRE_HUMAN_EVIDENCE_GATE_BINDING

all unaffected P1-7 design decisions preserved

candidate remains DESIGN_CANDIDATE / HUMAN_REVIEW_PENDING

P1-7 runtime remains NOT_STARTED

no Git commit
```

---

# 11. report/export

Target:

```text
.aiassistant/reports/target/
20260829_2204_aiscc-p1-7-pre-human-evidence-gate-binding-design-rework-1/
```

Required:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
.aiassistant/rules/AISCC_HUMAN_GATE_JUDGMENT.md
.aiassistant/records/aiscc/cycles/20260829_2204_aiscc-p1-7-pre-human-evidence-gate-binding-hold-1.cycle.md
```

Report exact:

```text
start HEAD
predecessor design SHA
P1-6 PRE_HUMAN empty-subset source finding
changed design sections
exact G_HUMAN_REQUIRED binding
freshness/replay rule
proof matrix addition
conflict result
product source changes = none
Git actions = none
human review = HUMAN_PENDING
```

---

# 12. lifecycle

Start:

```text
.aiassistant/tasks/active/
20260829_2204_aiscc-p1-7-pre-human-evidence-gate-binding-design-rework-1.md
```

Finish:

```text
.aiassistant/tasks/done/
20260829_2204_aiscc-p1-7-pre-human-evidence-gate-binding-design-rework-1.md
```

Do not return the predecessor done Task to active.

---

# 13. next action

If the narrow rework passes Command Center review:

```text
P1-7 design
→ HUMAN_FINAL_REVIEW
```

Only after Human design acceptance:

```text
terminal design persistence
→ P1-7 runtime implementation Task
```
