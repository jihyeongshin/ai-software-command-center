# 작업지시서: P1-6 Evidence Checkpoint / Human Ingress / Optional Evidence Design Rework

## meta

- task_id: `20260829_1026_aiscc-p1-6-checkpoint-human-ingress-and-optional-evidence-design-rework-1`
- created_at: `2026-08-29 10:26 KST`
- phase: `P1-6 — Evidence Admission`
- work_type: `DESIGN_BASELINE_REWORK`
- evidence_profile: `HIGH_RISK_DESIGN`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `checkpoint-scoped evidence completeness + Human-owned ingress`
- predecessor_task: `20260828_2329_aiscc-p1-6-evidence-admission-contract-design-freeze-with-p1-5-terminal-commit-1`
- predecessor_result: `ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING`
- command_center_result: `HOLD_REWORK_REQUIRED`
- predecessor_HEAD: `bd5611f3c1c3307e8f3f5d4ab39768fd69566b57`
- predecessor_design_path: `.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md`
- predecessor_design_sha256: `9b72dc3a5a5ed8b554cc3af4fd22bd2b720e6d93c34cb54381b8462038b6ac4a`
- P1_5_status: `ACCEPTED / CLOSED`
- P1_6_runtime_status: `NOT_STARTED`
- P1_7_status: `NOT_STARTED`

---

# 0. sole execution contract

This is design-only narrow rework.

Retain the predecessor P1-6 design unless directly conflicting with this Task.

Do not implement P1-6 runtime/product source.

Close exactly four axes:

1. G_EVIDENCE evidence-checkpoint / transition-purpose binding;
2. checkpoint-specific requirement applicability so HUMAN_OWNED cannot deadlock Human-gate entry;
3. a pre-P1-7 direct Human-owned evidence ingress that does not become HumanResult/Judgment;
4. removal of first-class OPTIONAL/supplemental requirement semantics from V1.

---

# Stage 0 — persist predecessor done Task + HOLD Cycle

## expected repository

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

HEAD:
bd5611f3c1c3307e8f3f5d4ab39768fd69566b57
```

If HEAD differs:

```text
STOP
→ BLOCKED_PREDECESSOR_HEAD_DRIFT
```

## expected uncommitted design candidate

Verify before Git index mutation:

```text
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md

SHA-256:
9b72dc3a5a5ed8b554cc3af4fd22bd2b720e6d93c34cb54381b8462038b6ac4a
```

Mismatch:

```text
STOP
→ BLOCKED_P1_6_DESIGN_CANDIDATE_DRIFT
```

Do not reconstruct or replace the candidate.

## exact provenance paths

Only:

```text
.aiassistant/tasks/done/
20260828_2329_aiscc-p1-6-evidence-admission-contract-design-freeze-with-p1-5-terminal-commit-1.md

.aiassistant/records/aiscc/cycles/
20260829_1026_aiscc-p1-6-checkpoint-human-ingress-and-optional-evidence-hold-1.cycle.md
```

The P1-6 design candidate MUST NOT be staged.

Unexpected tracked path:

```text
STOP
→ BLOCKED_P1_6_DESIGN_REWORK_PROVENANCE_COLLISION
```

## one local provenance commit

Forbidden:

```text
git add .
git add -A
git commit -a
git amend
git reset
git rebase
git stash
git clean
git fetch
git pull
git push
branch/tag/remote mutation
```

Exact commit message:

```text
docs: record P1-6 evidence checkpoint design hold

Persist the P1-6 design review that retained evidence admission,
content authority, reuse, persistence, and guard ownership but found
missing checkpoint scope and pre-P1-7 Human evidence ingress semantics.

Keep P1-6 runtime blocked pending design acceptance.
```

Use LF-safe UTF-8 message file + `git commit -F`.

After commit:

```text
P1_6_DESIGN_REWORK_BASE_COMMIT=<full hash>
```

Verify exact two paths, exact parent/message, clean index and no remote operation.

After this commit:

```text
git add / commit / push
→ FORBIDDEN
```

---

# Stage 1 — canonical read

Re-read:

```text
.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md
```

Inspect current P1-4 guard owner boundary:

```text
src/aiscc/workflow/guards.py
src/aiscc/workflow/matrix.py
src/aiscc/workflow/models.py
```

Design only. Do not modify source.

Explicitly reconcile that:

```text
P1-4 has one G_EVIDENCE guard ID
but
multiple transitions/checkpoints may consume evidence authority
```

and:

```text
P1-7 Human gate/result occurs after some evidence checkpoints
```

Do not alter P1-4 state values or transition pairs.

---

# Stage 2 — exact EvidenceCheckpoint / guard-use purpose

Update only:

```text
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md
```

Freeze an exact immutable System-owned concept equivalent to:

```text
EvidenceCheckpoint
EvidenceCheckpointRef
```

or `EvidenceGatePurpose`.

At minimum bind:

```text
checkpoint_id
checkpoint_version
task_contract_id/version
source WorkflowState
target WorkflowState or exact transition-purpose identity
guard_id = G_EVIDENCE
applicable RequirementSet id/version
issued/owned by System TaskContract authority
```

A checkpoint is not caller-selected arbitrary metadata.

It must be derived/resolved from the current TaskContract + requested P1-4 transition/use context.

Required non-substitution:

```text
same WorkRun/state/version
+ different checkpoint
→ different evidence authority

G_EVIDENCE(checkpoint A)
!= G_EVIDENCE(checkpoint B)
```

No implicit "infer checkpoint from state" convention.

---

# Stage 3 — checkpoint-specific requirement applicability

Keep the immutable RequirementSet as the full TaskContract evidence policy snapshot if desired.

Add an exact versioned applicability binding on every requirement equivalent to:

```text
applicable_checkpoint_refs
```

or an exact System-owned predicate with the same effect.

Required:

```text
EvidenceSetEvaluation(checkpoint X)
→ evaluate all REQUIRED directives applicable to X
→ evaluate all FORBIDDEN directives applicable to X
→ ignore obligations that are not applicable to X for completeness
```

An ignored-for-this-checkpoint requirement remains part of the immutable RequirementSet history; it
is not `NOT_REQUIRED` globally.

Do not silently rewrite requirement profile because of checkpoint.

A requirement may apply to multiple checkpoints only when explicitly versioned that way.

## Human-gate non-deadlock requirement

Freeze at least one normative lifecycle example:

```text
Task has:
- executor_required static/runtime proof
- human_owned final-review evidence

checkpoint PRE_HUMAN:
- executor evidence applicable
- human_owned final-review not yet applicable
→ set may become SATISFIED
→ G_EVIDENCE(PRE_HUMAN) can be issued

Human handling occurs under P1-7

checkpoint POST_HUMAN:
- human_owned final-review now applicable
- required Human evidence must be admitted
→ set may become SATISFIED
→ G_EVIDENCE(POST_HUMAN) can be issued
```

Exact checkpoint names may differ.

P1-6 does not open/resolve the HumanGate.

---

# Stage 4 — bind G_EVIDENCE attestation to checkpoint

Extend the design of `EvidenceSetEvaluation` and `EvidenceSetSatisfactionAttestation`.

Required additional binding:

```text
checkpoint_id/version
source state
target state / transition-purpose identity
exact applicable requirement refs/root for this checkpoint
```

Attestation must commit to:

```text
full RequirementSet id/version/root
+
checkpoint-applicable requirement subset/root
+
admitted refs/coverage/root
```

P1-4 future-owner verifier must reject:

```text
wrong checkpoint
wrong target/use purpose
wrong source state
wrong applicable-subset root
old checkpoint attestation
```

even when:

```text
TaskContract
work_run_id
state_version
```

otherwise match.

`TransitionRequest.evidence_refs` may remain exactly one attestation ref.

The attestation may not authorize another target transition.

---

# Stage 5 — pre-P1-7 direct Human-owned evidence ingress

Freeze two distinct Human evidence producer categories.

Exact names may differ, but semantics must include:

```text
HUMAN_DIRECT_EVIDENCE
HUMAN_P1_7
```

### HUMAN_DIRECT_EVIDENCE

Purpose:

```text
manual/Command Center Human-provided evidence before P1-7 runtime exists
```

It must bind at minimum:

```text
authenticated Human principal/operator identity
ingress authority id/version
TaskContract id/version
work_run_id
checkpoint id/version
evidence type
subject/scope/resource
content/ref/hash
provided_at
```

P1-6 performs normal:

```text
issuer
content integrity
scope
freshness
sensitivity
requirement
checkpoint applicability
```

evaluation.

Required:

```text
HUMAN_DIRECT_EVIDENCE
!= HumanGate
!= HumanResult
!= Judgment
!= G_HUMAN_*
!= G_JUDGMENT_*
```

P1-6 cannot manufacture the Human principal.
The ingress must be Human-authenticated/server-issued, not a caller-provided `human=true` flag.

### HUMAN_P1_7

Remains future P1-7 owner evidence.

A requirement must explicitly name which Human producer category/categories are allowed.

If a requirement requires `HUMAN_P1_7`:

```text
HUMAN_DIRECT_EVIDENCE
→ cannot substitute
```

This keeps P1-7 ownership intact while supporting the current manual Command Center phase.

---

# Stage 6 — remove unauthorized OPTIONAL requirement obligation

The exact P1-6 V1 evidence profiles remain only:

```text
EXECUTOR_REQUIRED
REUSE_ALLOWED
HUMAN_OWNED
NOT_REQUIRED
FORBIDDEN
```

Remove:

```text
RequirementObligation=OPTIONAL
supplemental=true requirement predicate
```

as first-class V1 requirement semantics.

If `RequirementObligation` remains as an internal normalized enum, its values must be derivable
exactly from the five profiles and must not add a sixth profile/obligation.

## supplemental material

Extra evidence-like material that is not required by the TaskContract may be retained only as:

```text
supplemental candidate/provenance
```

It:

```text
does not create EvidenceRequirement
does not create EvidenceRequirementSatisfaction
does not become AdmittedEvidence
does not affect EvidenceSetEvaluation
does not enter G_EVIDENCE roots
```

unless a current TaskContract requirement explicitly authorizes it under one of the exact five
profiles.

Do not silently promote useful supplemental content.

---

# Stage 7 — cross-contract consistency matrix

Add an exact table covering:

| fact | P1-4 | P1-6 result |
|---|---|---|
| `G_EVIDENCE` owner | future owner `P1_6_EVIDENCE` | MATCH |
| checkpoint/purpose binding | transition use context | MATCH |
| Human gate ownership | P1-7 | NOT ABSORBED |
| pre-Human evidence completeness | P1-6 checkpoint slice | NO DEADLOCK |
| post-Human evidence completeness | P1-6 checkpoint slice | NO SUBSTITUTION |
| Human direct evidence | evidence only | NOT HumanResult/Judgment |
| exact five profiles | Task evidence vocabulary | MATCH |
| transition authority | P1-4 | NOT ABSORBED |

No row may remain `AMBIGUOUS`.

---

# Stage 8 — update normative examples

Update/add exact examples for:

1. pre-Human evidence checkpoint;
2. post-Human Human-owned evidence checkpoint;
3. same state/version but wrong checkpoint attestation rejection;
4. direct Human evidence accepted for a requirement that allows it;
5. direct Human evidence rejected when requirement specifically requires P1-7 producer;
6. supplemental unrequired artifact retained but not admitted/not in G_EVIDENCE.

---

# Stage 9 — implementation proof matrix update

Add mandatory next-task proofs:

## CHECKPOINT_BINDING

- attestation for checkpoint A cannot satisfy checkpoint B;
- wrong target transition/use purpose rejects;
- same WorkRun/state/version does not allow cross-checkpoint replay;
- checkpoint-applicable subset root mismatch rejects.

## HUMAN_GATE_NON_DEADLOCK

- Task with pre-Human executor requirements + post-Human human_owned requirement:
  - pre-Human checkpoint can satisfy without Human evidence;
  - post-Human checkpoint remains unsatisfied until Human evidence exists.

## HUMAN_DIRECT_INGRESS

- forged/unverified Human identity rejects;
- Human direct evidence can satisfy only an explicitly allowed HUMAN_OWNED requirement;
- direct Human evidence does not create HumanResult/Judgment/other guards;
- requirement requiring P1-7 producer rejects direct Human evidence.

## SUPPLEMENTAL_NON_AUTHORITY

- unrequired supplemental candidate can be retained as provenance;
- no `AdmittedEvidence`;
- no satisfaction mapping;
- no set/root effect;
- cannot satisfy G_EVIDENCE.

Retain all previous proof classes.

---

# Stage 10 — exact path / scope

This rework changes exactly:

```text
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md
```

No new canonical rule.

Do not modify:

```text
src/**
tests/**
migrations/**
pyproject.toml
uv.lock
config/**
```

No P1-6 runtime implementation.

---

# evidence contract

## executor_required

- `P1_6_DESIGN_REWORK_PROVENANCE_GIT`
- `BASELINE_DESIGN_IDENTITY`
- `P1_4_G_EVIDENCE_CONTEXT_READ`
- `EVIDENCE_CHECKPOINT_DESIGN`
- `CHECKPOINT_REQUIREMENT_APPLICABILITY`
- `CHECKPOINT_BOUND_G_EVIDENCE_ATTESTATION`
- `HUMAN_GATE_NON_DEADLOCK`
- `HUMAN_DIRECT_EVIDENCE_INGRESS`
- `EXACT_FIVE_PROFILE_ALIGNMENT`
- `SUPPLEMENTAL_NON_AUTHORITY`
- `CROSS_CONTRACT_CONSISTENCY`
- `IMPLEMENTATION_PROOF_MATRIX_UPDATE`

## human_owned

`HUMAN_VERIFICATION`

If all load-bearing gaps close:

```text
ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING
```

Human then decides P1-6 design acceptance.

## forbidden

- P1-6 runtime/source implementation;
- P1-7/P1-8 implementation;
- state-machine transition changes;
- new evidence profile beyond exact five;
- LLM semantic verifier implementation;
- external network/provider call;
- credential/secret access;
- second Git commit after Stage 0;
- push/remote mutation;
- Browser Project Source mutation.

---

# proof non-substitution

```text
G_EVIDENCE attestation
!= generic evidence success for every transition

Human-owned requirement
!= pre-Human checkpoint requirement unless explicitly applicable

Human direct evidence
!= HumanResult
!= Judgment

same state/version
!= same evidence checkpoint

supplemental candidate
!= EvidenceRequirement
!= AdmittedEvidence
```

---

# result rules

If all four gaps close:

```text
ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING
```

If P1-4 exact transition contract cannot support checkpoint-bound evidence without changing the
accepted state/transition semantics:

```text
POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

If Human direct evidence cannot be represented without absorbing P1-7 HumanResult/Judgment authority:

```text
OWNER_SCOPE_CONFLICT
```

Do not weaken non-substitution.

---

# report required fields

- Task ID/path;
- predecessor HEAD;
- Stage-0 provenance commit/full hash;
- baseline design SHA;
- post-rework design SHA;
- exact changed path;
- exact EvidenceCheckpoint contract;
- requirement checkpoint applicability contract;
- exact checkpoint-bound G_EVIDENCE attestation;
- same-state cross-checkpoint anti-replay behavior;
- pre/post Human checkpoint example;
- direct Human-owned ingress contract;
- P1-7-specific Human producer contract;
- exact five-profile mapping;
- supplemental non-authority behavior;
- P1-4/P1-6 consistency matrix;
- updated implementation proof matrix;
- unresolved questions;
- forbidden-not-run;
- Human pending;
- preserved paths;
- next recommendation.

---

# export bundle

Target:

```text
.aiassistant/reports/target/20260829_1026_aiscc-p1-6-checkpoint-human-ingress-and-optional-evidence-design-rework-1/
```

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md`
- compact design review summary

No runtime source, private evidence body, credential or unrelated file.

---

# Task lifecycle

```text
.aiassistant/tasks/active/20260829_1026_aiscc-p1-6-checkpoint-human-ingress-and-optional-evidence-design-rework-1.md
→
.aiassistant/tasks/done/20260829_1026_aiscc-p1-6-checkpoint-human-ingress-and-optional-evidence-design-rework-1.md
```

`done` means submitted, not Human accepted.

---

# preserved artifacts

Preserve:

- commit `bd5611f3c1c3307e8f3f5d4ab39768fd69566b57`
- `.aiassistant/tasks/done/20260828_2329_aiscc-p1-6-evidence-admission-contract-design-freeze-with-p1-5-terminal-commit-1.md`
- `.aiassistant/records/aiscc/cycles/20260829_1026_aiscc-p1-6-checkpoint-human-ingress-and-optional-evidence-hold-1.cycle.md`
- `.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md`

Historical design candidate:

```text
9b72dc3a5a5ed8b554cc3af4fd22bd2b720e6d93c34cb54381b8462038b6ac4a
```

---

# next action after Human design acceptance

```text
P1-6 Evidence Admission Implementation + Runtime Verification
```

Do not implement it in this Task.
