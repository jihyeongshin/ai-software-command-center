# 작업지시서: P1-8 Prerequisite Owner Authority Exact Contract Design Rework

## meta

- task_id: `20260831_1332_aiscc-p1-8-prerequisite-owner-authority-exact-contract-design-rework-1`
- created_at: `2026-08-31T13:32:00+09:00`
- phase: `P1-8 Runtime Prerequisite Authority Contracts`
- work_type: `DESIGN_REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_start_head: `f4614198c2745944f7ec02639a45b0315bbc903d`
- predecessor_design_path: `.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md`
- predecessor_design_sha256: `556faad8a77d917fcbfc9ab7b0ba62bd65f985a6f4a1e585c08af668dd14393c`
- blocked_runtime_path_count: `19`
- blocked_runtime_aggregate_sha256: `84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42`
- runtime_implementation: `FORBIDDEN`
- human_design_review: `PENDING`

---

# 1. purpose

Rework only the exact remaining prerequisite design gaps.

Preserve the already-correct ownership decisions and canonical catalog payload unless a required correction changes
their exact fingerprint.

Do not modify runtime source/test/migration.

Do not resume P1-8 runtime.

Place/preserve:

```text
.aiassistant/records/aiscc/cycles/
20260831_1332_aiscc-p1-8-prerequisite-owner-authority-exact-contract-gap-hold-1.cycle.md
```

---

# 2. mandatory preflight

Require:

```text
HEAD ==
f4614198c2745944f7ec02639a45b0315bbc903d

predecessor design SHA ==
556faad8a77d917fcbfc9ab7b0ba62bd65f985a6f4a1e585c08af668dd14393c

blocked runtime ==
19 paths /
84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42
```

Index must be empty.

No Git add/commit/push.

---

# 3. preserve these decisions

Do not redesign:

```text
TaskConstraint owner
→ EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY extension

canonical-rule constraints
→ NOT_SUPPORTED_V1

P1-4 owns blocker provenance

P1-4 owns blocker-resolution transition provenance

P1-8 owns resolution_cycle_id relation projection

resolution transition ref
!= terminal ACCEPTED transition ref

one ACTIVE blocker per WorkRun BLOCKED epoch

canonical two-action P1_8_POLICY_ACTION_CATALOG_V1

two actions:
open-operational-recovery-task-issuance
open-cycle-derived-task-issuance

both:
AFTER_TASK_ISSUANCE_P1_7

Task issuance:
EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY

private live System capability composition

no caller/config catalog definition

no retroactive authority laundering
```

Catalog hashes may remain unchanged if findings below do not alter catalog payload.

---

# 4. TaskConstraint scope contract

Freeze exact field-presence rules.

For each:

```text
PROJECT
TASK_CONTRACT
WORK_RUN
```

define exactly:

```text
scope_id source
task_contract_id/version required | forbidden | exact sentinel
work_run_id required | forbidden
project_id required
```

Prefer no ambiguous empty-string/sentinel semantics.

If a field is not applicable, either:

```text
omit it from the schema variant
```

or freeze exact JSON null semantics and include that in canonical hashing.

Do not leave implementation-dependent optionality.

---

# 5. TaskConstraint owner event model

Add exact immutable:

```text
TaskConstraintAuthorityEventV1
```

or exact semantic equivalent.

Freeze:

```text
event identity/ref/version/fingerprint
constraint ref/fingerprint
event kind:
ISSUED
SUPERSEDED
REVOKED

replacement/superseding ref
owner authority ID/version/revision
project/scope
event sequence
effective sequence/time
current applicability disposition
```

Freeze fail-closed fold rules:

```text
exact one ISSUED origin

monotonic owner event sequence

duplicate same event
→ replay

conflicting duplicate
→ authority conflict

SUPERSEDED
→ replacement exact current candidate

REVOKED
→ no current constraint

unknown/gap/out-of-order
→ fail closed
```

Freeze historical high-watermark semantics.

Do not encode pure revocation only as another constraint object.

---

# 6. TaskConstraint owner capability boundary

Because this is a new external Task authority runtime extension, freeze its issuer/verifier boundary too.

Required:

```text
external Command Center Task authority bootstrap/composition
→ owns opaque issue/supersede/revoke capability

P1-8
→ verifier/read port only

ordinary caller/runtime repository
→ cannot mint/revoke TaskConstraintRef
```

Process-local capability is not historical identity; durable owner payload/event provenance is.

---

# 7. exact blocker taxonomy

Resolve `blocker_kind` vs `reason_code`.

Freeze exact V1 representation.

Recommended:

```text
BlockerKindV1:
SECURITY
POLICY
ARTIFACT
BASELINE
AUTHORITY
EXTERNAL_DEPENDENCY
EXECUTION

BlockerReasonCodeV1:
SECURITY_BOUNDARY
POLICY_CONFLICT
MISSING_REQUIRED_ARTIFACT
BASELINE_GAP
AUTHORITY_CONFLICT
EXTERNAL_DEPENDENCY
EXECUTION_BLOCKER
```

with a closed one-to-one or explicit allowed matrix.

Alternative: remove one field and use a single exact reason enum.

Either is acceptable if exact.

Then freeze:

```text
reason → resumability
```

and exact allowed terminal paths.

For every reason state whether:

```text
RESUMABLE
→ positive G_BLOCKER_RESOLVED allowed

NON_RESUMABLE
→ positive resolution forbidden; only FAILED/other exact terminal path
```

Do not leave this to implementation.

---

# 8. exact blocker guard binding

Freeze what:

```text
g_blocker_resolved_attestation_ref/fingerprint
```

means.

Choose exactly one:

### Option A

Existing P1-4 TransitionEvaluation/Decision carries an immutable typed guard-consumption binding:

```text
guard_id = G_BLOCKER_RESOLVED
blocker_ref/fingerprint
resolution_source_ref/fingerprint
```

and the resolution object references that exact evaluation/decision payload.

### Option B

Create an explicit:

```text
P1_4BlockerResolvedAttestationV1
```

with exact immutable fields/fingerprint/owner.

Do not support both as interchangeable V1 authority.

Freeze replay and transaction ordering.

---

# 9. exact NEXT_ACTION_CONTEXT ranking source

Add an exact source contract for:

```text
P1_8_CURRENT_NEXT_ACTION_CONTEXT_MEMORY_V1
```

The ranking policy must not rely on an undefined semantic field inside arbitrary structured memory.

Freeze exact owner-backed source body, for example:

```text
P1_8_NEXT_ACTION_CONTEXT_SOURCE_V1

project_id
task_contract_id/version
work_run_id
source_cycle_id

priority_class:
ACCEPTED_CORE_CRITICAL_PATH
OPERATIONAL_HARDENING
OPTIONAL_OPTIMIZATION

critical_path_ordinal
context_ref
context_fingerprint
```

But use the exact existing P1-6 structured source schema if one already exists; do not invent duplicate authority.

Freeze:

```text
source schema ID/version
JSON selector
canonicalization
P1-6 Requirement V2 durable eligibility
source authority/ref/fingerprint
field validation
MemoryDeclaration derivation
MCF_V1 relation
privacy
```

Caller values are equality claims only.

If these fields are absent from existing exact P1-6 source authority and require a new structured-result owner
contract:

```text
STOP
→ IMPLEMENTATION_BASELINE_GAP
```

and report the missing owner.

---

# 10. resolve critical-path ordinal ambiguity

The candidate currently contains:

```text
descriptor.critical_path_ordinal
```

and separately says `NEXT_ACTION_CONTEXT` supplies an owner-derived critical-path ordinal.

Freeze exactly:

```text
which ordinal is authoritative ranking input
which ordinal is only descriptor tie-break metadata
```

Recommended:

```text
CYCLE_DERIVED authoritative critical_path_ordinal
→ source-memory owner-derived ordinal

descriptor critical_path_ordinal
→ descriptor/catalog tie-break only
```

If so, rename the ranking tuple labels to make this distinction explicit.

For OPERATIONAL_RECOVERY, no memory critical-path ordinal is required.

---

# 11. priority policy payload update

If exact source contract or ranking tuple semantics change the semantic priority policy payload, recompute:

```text
priority policy fingerprint
catalog priority_source_contract_fingerprint
catalog fingerprint
descriptor fingerprints
```

Do not retain old hashes after semantic payload change.

If no semantic catalog fields change, document why catalog hash remains exact.

Independent verification must recompute all affected hashes.

---

# 12. historical/current replay

Freeze exact replay for the newly completed contracts.

## constraint

```text
TaskConstraintRef
+ TaskConstraintAuthorityEvent history
through original admission high-watermark
→ original validity
```

Current event history is not required to be current now.

## blocker

```text
blocker object
+ exact guard-consumption binding
+ resolution transition object
+ terminal ACCEPTED transition
→ rederived relation
```

## NEXT_ACTION_CONTEXT

Historical selection:

```text
original exact memory source/MCF
+ memory applicability state at selection high-watermark
→ priority_class/ordinal rederived
```

Later memory staleness does not corrupt historical selection.

---

# 13. exact question additions

Reworked design/report must answer:

1. For each TaskConstraint scope kind, which fields are present?
2. What exact object represents constraint revocation?
3. What is the owner-event fold/high-watermark algorithm?
4. How is TaskConstraint mint/revoke capability hidden from P1-8/callers?
5. What exact values are `blocker_kind`?
6. What exact values are `reason_code`?
7. What exact kind→reason matrix applies?
8. Which blockers are resumable?
9. Can a NON_RESUMABLE blocker ever emit positive `G_BLOCKER_RESOLVED`?
10. What exact durable object/binding does `g_blocker_resolved_attestation_ref` identify?
11. What exact source schema supplies CYCLE_DERIVED `priority_class`?
12. What exact source supplies authoritative critical-path ordinal?
13. What does descriptor `critical_path_ordinal` mean after this distinction?
14. Which affected hashes changed?
15. Are any further Human-owned semantic choices still open?

No implicit answer.

---

# 14. output

Update the same candidate rule:

```text
.aiassistant/rules/
AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
```

Do not create a second competing prerequisite rule.

Executor result:

```text
CANDIDATE / HUMAN_REVIEW_REQUIRED
```

only if every exact contract above is closed.

If an owner-backed NEXT_ACTION_CONTEXT source is absent:

```text
BLOCKED_REQUIRED_EVIDENCE / IMPLEMENTATION_BASELINE_GAP
```

is the correct submission.

---

# 15. Git/runtime policy

```text
NO runtime source/test/migration changes

NO git add
NO commit
NO push

final HEAD:
f4614198c2745944f7ec02639a45b0315bbc903d
```

P1-8 Runtime remains blocked.

Human review remains pending.

---

# 16. export

Target:

```text
.aiassistant/reports/target/
20260831_1332_aiscc-p1-8-prerequisite-owner-authority-exact-contract-design-rework-1/
```

Include:

```text
updated prerequisite design
exact-contract HOLD Cycle
done Task
EXPORT_MANIFEST.md
EXECUTOR_REPORT.md
TASK.md
```

Report:

```text
predecessor design SHA
reworked design SHA

all canonical catalog/policy/schema fingerprints
blocked runtime identity unchanged

source/export byte identity
HEAD/index/Git actions
```

---

# 17. expected state

```text
P1-8 prerequisite owner authority design:
CANDIDATE / HUMAN_REVIEW_REQUIRED
or
BLOCKED_REQUIRED_EVIDENCE if exact source owner is absent

P1-8 Runtime:
BLOCKED_REQUIRED_EVIDENCE

P2:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```
