# AISCC Cycle Record

## meta

- cycle_id: `20260829_1026_aiscc-p1-6-checkpoint-human-ingress-and-optional-evidence-hold-1`
- date: `2026-08-29 10:26 KST`
- primary_semantic_owner: `P1-6 evidence-set scope / Human-owned ingress / exact profile vocabulary`
- work_type: `DESIGN_BASELINE / REWORK_JUDGMENT`
- execution_mode: `MANUAL_COMMAND_CENTER`
- predecessor_task: `20260828_2329_aiscc-p1-6-evidence-admission-contract-design-freeze-with-p1-5-terminal-commit-1`
- predecessor_executor_result: `ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING`
- predecessor_HEAD: `bd5611f3c1c3307e8f3f5d4ab39768fd69566b57`
- predecessor_design_path: `.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md`
- predecessor_design_sha256: `9b72dc3a5a5ed8b554cc3af4fd22bd2b720e6d93c34cb54381b8462038b6ac4a`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause:
  - `G_EVIDENCE_ATTESTATION_NOT_EVIDENCE_CHECKPOINT_OR_TRANSITION_PURPOSE_BOUND`
  - `HUMAN_OWNED_REQUIREMENT_CAN_DEADLOCK_PRE_HUMAN_GATE_EVIDENCE_COMPLETENESS`
  - `NO_PRE_P1_7_DIRECT_HUMAN_OWNED_INGRESS_CONTRACT`
  - `SUPPLEMENTAL_OPTIONAL_REQUIREMENT_INTRODUCES_UNAUTHORIZED_SIXTH_OBLIGATION_SEMANTIC`
- P1_5_status: `ACCEPTED / CLOSED`
- P1_6_design_status: `NOT_ACCEPTED`
- P1_6_runtime_status: `NOT_STARTED`
- P1_7_status: `NOT_STARTED`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260829_1026_aiscc-p1-6-checkpoint-human-ingress-and-optional-evidence-hold-1.cycle.md`

## admitted predecessor evidence

### P1-5 terminal persistence

Admit:

```text
P1_6_DESIGN_BASE_COMMIT:
bd5611f3c1c3307e8f3f5d4ab39768fd69566b57

parent:
15036a5ff316fccbd6d891b9ce43563de056e342

terminal commit paths:
47

P1-5 accepted candidate:
42 paths

aggregate:
ffeb5ba70649c564c482c2cff79ce8e2b0a462f811d8e03f2c1096f170bd39d6

post-commit tracked worktree:
clean

post-commit index:
empty

remote operation:
0
```

P1-5 remains `ACCEPTED / CLOSED`.

### P1-6 design candidate

Exact candidate:

```text
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md

SHA-256:
9b72dc3a5a5ed8b554cc3af4fd22bd2b720e6d93c34cb54381b8462038b6ac4a
```

Bundle integrity:

```text
TASK:
503cbfadef6781e845cd89fa5873c4292338c6dd398ed755d669c626626751c6

EXECUTOR_REPORT:
2d632ee8ffca4e2f8557d210892760b1d1ff56047f60df03bd66ac11bb7801e1

DESIGN_REVIEW_SUMMARY:
96ad25cd90cdfd7ec27a35f5a14a9e8a78221e2744651e7b8cd99f9a0c193bc2
```

No P1-6 runtime/source implementation occurred.

## retained design strengths

Retain without reopening unless directly affected by this rework:

```text
EvidenceRequirement / EvidenceRequirementSet versioning
EvidenceCandidate != AdmittedEvidence
exact issuer/producer authority
content/body/reference integrity
admission evaluation dimensions
ADMITTED / REJECTED exact outcome
sanitized rejection taxonomy
per-requirement satisfaction mapping
reuse requires new current-task admission
append-only persistence
revocation / supersession / correction
freshness / applicability policies
sensitive/private evidence export boundary
P1-6 future-owner G_EVIDENCE issuer separation
P1-6 cannot mint P1-7 or P1-4-owned guards
PostgreSQL implementation direction
implementation proof matrix
```

## HOLD A — G_EVIDENCE has no evidence-checkpoint / transition-purpose binding

Current `EvidenceSetSatisfactionAttestation` binds:

```text
TaskContract
WorkRun
WorkflowState/state_version
RequirementSet/version/root
admitted evidence refs/coverage/root
authority version
issued/expiry
```

but it does not bind an exact evidence checkpoint, transition target, or transition-intent purpose.

Current design also states:

```text
TransitionRequest.evidence_refs
→ exact one-element tuple containing the attestation ref
```

The P1-4 kernel has one `G_EVIDENCE` semantic owner but multiple transition rows may consume
`G_EVIDENCE`.

Therefore an attestation that is valid for one evidence gate at the same WorkRun state/version can be
replayed for a different transition purpose unless the verifier infers hidden semantics outside the
attestation.

Required invariant:

```text
G_EVIDENCE for checkpoint A
!= G_EVIDENCE for checkpoint B
```

Raw state/version equality is insufficient.

### required correction

Freeze an exact System-owned evidence checkpoint / guard-use purpose.

Names may differ, but the contract must provide an immutable identifier equivalent to:

```text
EvidenceCheckpoint
or
EvidenceGatePurpose
```

and bind it through:

```text
EvidenceRequirement
EvidenceSetEvaluation
EvidenceSetSatisfactionAttestation
P1-4 FutureOwnerGuardVerifier
TransitionRequest target/use context
```

At minimum the attestation must commit to an exact guard-use identity sufficient to prevent reuse
across different P1-4 transition purposes.

A safe V1 direction is:

```text
checkpoint_id/version
source WorkflowState
target WorkflowState or exact transition-purpose identity
TaskContract id/version
RequirementSet id/version/root
```

P1-6 does not decide the transition. It verifies evidence for the System-owned requested checkpoint.

Wrong checkpoint/target/purpose:

```text
→ G_EVIDENCE verification DENY
```

## HOLD B — HUMAN_OWNED can make the full set impossible before Human gate entry

Current design normalizes:

```text
HUMAN_OWNED
→ REQUIRED
```

and the exact set algorithm requires every:

```text
EXECUTOR_REQUIRED
REUSE_ALLOWED
HUMAN_OWNED
```

row to be `SATISFIED` before the set becomes `SATISFIED` and can mint `G_EVIDENCE`.

This treats the entire TaskContract RequirementSet as one unconditional completeness set.

But P1-4's workflow has a distinct `HUMAN_REQUIRED` state and P1-7 owns the Human gate/result.

A Task may need:

```text
pre-Human evidence complete
→ enter HUMAN_REQUIRED

then
Human-owned evidence/result exists
→ later evidence/judgment/terminal path
```

Under the current P1-6 design, a `HUMAN_OWNED` directive in the same full set remains
`UNSATISFIED` before the Human gate exists.

That can create the circular dependency:

```text
need G_EVIDENCE to advance to Human-required handling
but
G_EVIDENCE requires HUMAN_OWNED evidence
but
Human-owned evidence may only exist after Human handling
```

P1-6 must not encode such a workflow deadlock.

### required correction

Keep one immutable TaskContract RequirementSet if desired, but make requirement applicability exact
per evidence checkpoint.

At minimum each requirement must bind an immutable checkpoint applicability rule equivalent to:

```text
required_for_checkpoint(s)
```

or a server-owned predicate with the same semantics.

Then:

```text
EvidenceSetEvaluation(checkpoint X)
→ evaluates only requirements applicable to checkpoint X
→ still evaluates all applicable prohibitions
```

A `HUMAN_OWNED` requirement may be required for a post-Human checkpoint without blocking the
pre-Human checkpoint.

Do not make P1-6 infer phase from current state by convention.
The checkpoint mapping is TaskContract/System-owned and versioned.

The same requirement may apply to more than one checkpoint only if explicitly listed.

## HOLD C — no direct Human-owned ingress before P1-7 exists

The Task contract explicitly required that, before P1-7 exists:

```text
human_owned requirement
→ remains unsatisfied
unless
Human evidence is explicitly supplied through a Human-owned ingress defined by P1-6 design
```

Current design defines the only Human issuer as:

```text
HUMAN_P1_7
```

and section 16 requires:

```text
P1-7 issuer authenticity and gate/result binding verification
```

Therefore, before P1-7 implementation, there is no production Human-owned ingress contract at all.

The design permits a fake Human-owner verifier only for tests, which is not the same thing.

### required correction

Define a Human-owned evidence ingress that can exist before P1-7 without stealing P1-7 authority.

A safe exact split is:

```text
HUMAN_DIRECT_EVIDENCE
→ authenticated/manual Command Center Human evidence artifact
→ proves only the exact evidence predicate
→ NOT HumanGate
→ NOT HumanResult
→ NOT Judgment

HUMAN_P1_7
→ future P1-7 owner-produced Human gate/result evidence
```

Exact names may differ.

The direct Human ingress must bind:

```text
Human principal / authenticated operator identity
TaskContract
work_run_id
checkpoint
evidence type
content/ref/hash
created/provided time
ingress authority/version
```

and must still undergo full P1-6 content/scope/freshness admission.

P1-6 cannot convert direct Human evidence into:

```text
HumanResult
Judgment
G_HUMAN_*
G_JUDGMENT_*
```

When a requirement explicitly requires `HUMAN_P1_7`, direct Human evidence cannot substitute.

## HOLD D — supplemental OPTIONAL predicate exceeds the exact five-profile contract

The Task requires the project evidence vocabulary:

```text
executor_required
reuse_allowed
human_owned
not_required
forbidden
```

and separately says optional evidence may be retained but does not create requirements.

Current candidate adds:

```text
RequirementObligation=OPTIONAL
supplemental=true
```

and describes it as an optional supplemental predicate.

That creates a sixth requirement-obligation semantic outside the exact Task evidence vocabulary and
contradicts:

```text
optional evidence may be retained
but does not create requirements
```

### required correction

Remove `OPTIONAL` as a requirement obligation in P1-6 V1.

Use only the exact five profile-derived obligation semantics.

Extra non-required material may be retained as:

```text
supplemental EvidenceCandidate/provenance
```

but it is not `AdmittedEvidence` and creates no requirement/satisfaction mapping unless a current
TaskContract requirement explicitly authorizes it under one of the exact five profiles.

If the project later wants first-class optional evidence requirements, that requires a separate
Human-accepted baseline change.

## Command Center judgment

```text
P1-5 terminal Git:
PASS / CLOSED

P1-6 requirement versioning:
PASS / RETAIN

issuer/content authority:
PASS / RETAIN

reuse/anti-replay:
PASS / RETAIN

admission dimensions/reasons:
PASS / RETAIN

append-only persistence:
PASS / RETAIN

revocation/supersession:
PASS / RETAIN

sensitivity/export:
PASS / RETAIN

G_EVIDENCE owner separation:
PASS / RETAIN

G_EVIDENCE checkpoint/transition-purpose binding:
HOLD_REWORK_REQUIRED

Human-owned pre/post gate completeness semantics:
HOLD_REWORK_REQUIRED

pre-P1-7 direct Human-owned ingress:
HOLD_REWORK_REQUIRED

exact five-profile vocabulary:
HOLD_REWORK_REQUIRED

P1-6 design:
NOT ACCEPTED

P1-6 runtime:
NOT_STARTED

P1-7:
NOT_STARTED
```

## proof non-substitution

```text
state/version-bound G_EVIDENCE
!= transition-purpose-bound G_EVIDENCE

one full RequirementSet
!= one valid completeness set for every workflow checkpoint

HUMAN_P1_7 issuer
!= pre-P1-7 direct Human evidence ingress

fake Human test verifier
!= production Human-owned ingress

supplemental optional predicate
!= exact five evidence profiles

Human evidence
!= HumanResult
!= Judgment
```

## preservation

Preserve exact commit:

- `bd5611f3c1c3307e8f3f5d4ab39768fd69566b57`

Preserve exact paths:

- `.aiassistant/tasks/done/20260828_2329_aiscc-p1-6-evidence-admission-contract-design-freeze-with-p1-5-terminal-commit-1.md`
- `.aiassistant/records/aiscc/cycles/20260829_1026_aiscc-p1-6-checkpoint-human-ingress-and-optional-evidence-hold-1.cycle.md`
- `.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md`

Preserve historical design candidate identity:

```text
9b72dc3a5a5ed8b554cc3af4fd22bd2b720e6d93c34cb54381b8462038b6ac4a
```

## next action

```text
P1-6 design-only narrow rework
→ evidence checkpoint / transition-purpose binding
→ checkpoint-specific requirement applicability
→ pre-P1-7 direct Human-owned evidence ingress
→ remove unauthorized OPTIONAL requirement obligation
→ Human design review
```

Do not implement P1-6 runtime.
