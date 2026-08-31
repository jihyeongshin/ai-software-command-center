# AISCC Cycle Record

## meta

- cycle_id: `20260831_1332_aiscc-p1-8-prerequisite-owner-authority-exact-contract-gap-hold-1`
- date: `2026-08-31T13:32:00+09:00`
- phase: `P1-8 Runtime Prerequisite Authority Contracts`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `AISCC_COMMAND_CENTER`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause: `PREREQUISITE_OWNER_AUTHORITY_EXACT_CONTRACT_GAPS`
- reviewed_head: `f4614198c2745944f7ec02639a45b0315bbc903d`
- candidate_design_path: `.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md`
- candidate_design_sha256: `556faad8a77d917fcbfc9ab7b0ba62bd65f985a6f4a1e585c08af668dd14393c`
- blocked_runtime_path_count: `19`
- blocked_runtime_aggregate_sha256: `84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42`

---

# 1. candidate identity

Independent verification:

```text
candidate design SHA:
556faad8a77d917fcbfc9ab7b0ba62bd65f985a6f4a1e585c08af668dd14393c

blocked runtime:
19 paths /
84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42
UNCHANGED

catalog canonical hash:
57c2b89286311038faae9d780ae5572124cc850065a0012954e2f8eefdea121c
MATCH

operational parameter schema hash:
92fe98cbc7cae63ab1f72161b625eb9bbd3281592f7731f98d24f30b4dd326f1
MATCH

cycle-derived parameter schema hash:
3e4407fef8f429031038018d8ee8fab0cb91ad583277f28e0d75064b226ea646
MATCH

priority policy hash:
f7c69da9e2e4ad8fadc93d813703023c63c712ab8662b7aa29402e0a7217d315
MATCH

Git add/commit/push:
none
```

---

# 2. accepted design directions

The following design choices are sound and should be preserved.

```text
TaskConstraint owner
→ EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY extension
→ P1-8 verify-only

Blocker identity/resolution
→ P1-4-owned

resolution_cycle_id
→ P1-8-owned relation field
→ no cyclic P1-4 → future P1-8 dependency

blocker resolution transition
!= final terminal ACCEPTED transition

V1 blocker cardinality
→ at most one ACTIVE blocker per WorkRun BLOCKED epoch

canonical-rule constraint
→ NOT_SUPPORTED_V1

P1_8_POLICY_ACTION_CATALOG_V1
→ owner-authored immutable catalog
→ caller/config cannot define descriptors

V1 action inventory
→ two minimal TaskIssuanceCandidate handoff actions only

TaskIssuanceCandidate
!= TaskContract

Task issuance owner
→ EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY

both V1 actions
→ AFTER_TASK_ISSUANCE_P1_7

live Memory/NextAction owner capability
→ private composition boundary

no retroactive authority laundering
```

---

# 3. FINDING A — TaskConstraint currentness/event model is not exact enough

`TaskConstraintRefV1` freezes the immutable ref payload, but current applicability semantics remain ambiguous.

The candidate includes:

```text
scope_kind = PROJECT | TASK_CONTRACT | WORK_RUN
scope_id

task_contract_id
task_contract_version

supersedes_constraint_ref
revokes_constraint_ref

issuance_sequence
effective_sequence
```

but does not freeze:

```text
exact scope-field cardinality for each scope_kind

whether PROJECT-scoped constraints may/shall carry TaskContract fields

how a pure revoke-without-replacement is represented

the exact owner event object for ISSUED / SUPERSEDED / REVOKED

owner-event high-watermark folding

current applicability disposition
```

`revokes_constraint_ref` embedded in a newly issued `TaskConstraintRefV1` is not sufficient to define a standalone
revocation event.

Required rework:

Freeze an exact owner event model equivalent to:

```text
TaskConstraintAuthorityEventV1

event_id/ref/version/fingerprint
constraint_ref/fingerprint
event_kind = ISSUED | SUPERSEDED | REVOKED
replacement_ref = NONE | exact ref
project/scope
owner authority ref/version/revision
event_sequence
effective_sequence
issued_at
current_projection_disposition
```

Also freeze exact allowed field presence for:

```text
PROJECT
TASK_CONTRACT
WORK_RUN
```

No sentinel/empty-field ambiguity.

Historical replay:

```text
original ref + owner events through original high-watermark
```

New admission:

```text
current eligible ref only
```

---

# 4. FINDING B — blocker taxonomy/resumability and G_BLOCKER_RESOLVED binding are ambiguous

The candidate defines both:

```text
blocker_kind
reason_code
resumability = RESUMABLE | NON_RESUMABLE
```

but gives only one combined vocabulary:

```text
SECURITY_BOUNDARY
POLICY_CONFLICT
MISSING_REQUIRED_ARTIFACT
BASELINE_GAP
AUTHORITY_CONFLICT
EXTERNAL_DEPENDENCY
EXECUTION_BLOCKER
```

It does not freeze:

```text
which values are blocker_kind
which values are reason_code
allowed blocker_kind → reason_code matrix
which reason codes are RESUMABLE vs NON_RESUMABLE
whether NON_RESUMABLE may ever emit positive blocker resolution
```

This is load-bearing because NextAction priority policy consumes exact reason codes and blocker resolution eligibility.

The candidate also includes:

```text
g_blocker_resolved_attestation_ref/fingerprint
resolution_source_authority_ref/fingerprint
```

without freezing the exact durable owner object/schema that these refs identify.

Required rework:

Freeze exact V1 enums/matrix.

Prefer one of:

```text
A. blocker_kind is the exact authoritative reason enum; remove reason_code

or

B. separate exact BlockerKindV1 and BlockerReasonCodeV1 enums
   with a closed mapping table
```

Freeze exact resumability mapping and terminal behavior.

Freeze exact `G_BLOCKER_RESOLVED` durable binding:

```text
guard-derived binding inside TransitionEvaluation/Decision
```

or a separately persisted exact owner attestation object.

Do not leave implementation choice open.

---

# 5. FINDING C — CYCLE_DERIVED priority authority lacks an exact NEXT_ACTION_CONTEXT source schema

The priority policy says ranks 4–6 require a:

```text
CURRENT P1_8_CURRENT_NEXT_ACTION_CONTEXT_MEMORY_V1
```

whose owner-derived:

```text
priority_class
critical-path ordinal
```

determine authoritative ranking.

However this prerequisite design does not freeze the exact source payload/schema/selector that makes those fields
owner-authoritative.

The prior P1-8 Memory contract only identifies:

```text
NEXT_ACTION_CONTEXT
→ STRUCTURED_RESULT_ATTESTED
```

and a generic structured selector.

Required rework:

Freeze an exact `NEXT_ACTION_CONTEXT` V1 source contract sufficient for ranking.

At minimum:

```text
source schema ID/version
exact JSON selector/object shape
priority_class enum
critical_path_ordinal field and bounds
dependency/policy ordinal if source-owned
project/TaskContract/WorkRun/Cycle binding
source authority ref/fingerprint
P1-6 durable structured-content requirement
Memory MCF binding
privacy ceiling
selection-time CURRENT applicability high-watermark
```

Resolve the ambiguity between:

```text
descriptor critical_path_ordinal
vs
source-memory critical_path_ordinal
```

and state exactly which value participates in the ranking tuple.

Caller-provided `next_action_context_ref/fingerprint` remains locator/equality claim only.

If no exact owner-backed structured source exists for the required ranking fields:

```text
IMPLEMENTATION_BASELINE_GAP
```

rather than inventing them in P1-8.

---

# 6. judgment

```text
P1-8 prerequisite owner authority design:
HOLD_REWORK_REQUIRED / HUMAN_REVIEW_NOT_READY

P1-8 Runtime:
BLOCKED_REQUIRED_EVIDENCE

blocked runtime:
19 paths /
84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42
UNCHANGED

P2:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

No Human final design review yet.

No runtime implementation is authorized.

