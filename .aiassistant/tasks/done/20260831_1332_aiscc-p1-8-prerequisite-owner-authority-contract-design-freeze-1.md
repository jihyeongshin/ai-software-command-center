# 작업지시서: P1-8 Prerequisite Owner Authority Contract Design Freeze

## meta

- task_id: `20260831_1332_aiscc-p1-8-prerequisite-owner-authority-contract-design-freeze-1`
- created_at: `2026-08-31T13:32:00+09:00`
- phase: `P1-8 Runtime Prerequisite Authority Contracts`
- work_type: `DESIGN_FREEZE`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `CROSS_OWNER / COMMAND_CENTER`
- expected_start_head: `f4614198c2745944f7ec02639a45b0315bbc903d`
- accepted_p1_8_design_sha256: `100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a`
- blocked_p1_8_runtime_path_count: `19`
- blocked_p1_8_runtime_aggregate_sha256: `84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42`
- runtime_implementation: `FORBIDDEN`
- human_design_review: `PENDING`

---

# 1. purpose

Design and freeze the three missing owner-authority prerequisites that block the already accepted P1-8 runtime
design.

The three contracts are:

```text
A. immutable Task/constraint provenance authority
   required by P1-8 CONSTRAINT_POINTER

B. immutable P1-4 blocker provenance + blocker-resolution transition authority
   required by P1-8 BLOCKER_RESOLUTION

C. immutable canonical P1-8 POLICY_ACTION_CATALOG_V1 payload/ref/fingerprint
   required by NextAction descriptor enrollment
```

Do not implement runtime source/migrations/tests in this Task.

Do not modify the blocked 19-path runtime candidate.

---

# 2. mandatory preflight

Require:

```text
HEAD ==
f4614198c2745944f7ec02639a45b0315bbc903d

accepted P1-8 design SHA ==
100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a

blocked runtime ==
19 paths /
84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42
```

Require exact baseline-gap Cycle:

```text
.aiassistant/records/aiscc/cycles/
20260831_1332_aiscc-p1-8-prerequisite-owner-authority-baseline-gap-hold-1.cycle.md
```

Any runtime drift:

```text
STOP
→ REVIEWED_CANDIDATE_DRIFT
```

Index must be empty.

No Git add/commit/push.

---

# 3. candidate design artifact

Create one canonical candidate design:

```text
.aiassistant/rules/
AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
```

Korean-first prose.

English identifiers.

This file is a candidate until Human final design review.

Do not modify:

```text
AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md
AISCC_ORCHESTRATION.md
AISCC_EVIDENCE_ADMISSION.md
AISCC_HUMAN_GATE_JUDGMENT.md
```

in this Task.

---

# 4. authority-owner inventory first

Before proposing new contracts, inspect the current exact owner graph and report whether any suitable authority
already exists.

At minimum inspect:

```text
TaskContract / external Command Center Task authority

P1-4 WorkRun / TransitionRequest / TransitionDecision / guard authority

P1-6 TaskContractEvidenceAuthority and immutable requirement/checkpoint owner shapes

P1-7 Judgment/Human provenance

canonical rule/document authority and stable anchor/hash conventions

NEXT_ACTIONS / roadmap governance authority
```

For every candidate source, classify:

```text
EXISTING_EXACT_OWNER
EXISTING_BUT_INSUFFICIENT
ABSENT
```

Do not infer authority from Markdown presence.

---

# 5. Contract A — Task Constraint Authority

Freeze an owner contract sufficient for:

```text
P1-8 CONSTRAINT_POINTER
```

Required exact conceptual output:

```text
TaskConstraintRef
```

or equivalent immutable owner-issued reference.

It must bind at least:

```text
constraint_owner
logical_constraint_id
authority_ref
authority_version
authority_fingerprint
project/scope
TaskContract identity/version where applicable
constraint schema/version
issued/effective sequence or immutable issuance revision
```

Required owner rule:

```text
P1-8 cannot mint/register/modify TaskConstraintRef
```

Determine the exact owner.

Preferred order:

```text
1. existing external Command Center / TaskContract authority
2. existing canonical-rule authority with exact hash+anchor
3. minimal new Task authority extension
```

Do not make P1-8 the constraint owner.

## historical/current semantics

Freeze:

```text
historical constraint issuance validity
!= current constraint applicability
```

Historical P1-8 Cycle replay must verify the exact original constraint ref/fingerprint.

New admission must use the current eligible constraint source according to the accepted Memory policy.

Later constraint supersession must not rewrite old ProjectMemory.

## canonical rule alternative

If canonical rule constraints are supported, freeze exact:

```text
document logical authority ID
repository-relative path or durable ref
document content SHA-256
stable anchor ID
anchor payload/hash
constraint logical ID
```

A line number alone is not a stable authority.

---

# 6. Contract B — P1-4 Blocker Provenance Authority

Freeze a P1-4-owned immutable blocker identity.

Required conceptual object:

```text
P1_4BlockerProvenance
```

or equivalent.

Must bind at least:

```text
blocker_owner = P1_4
blocker_id
blocker_ref
blocker_fingerprint
project_id
TaskContract ID/version
WorkRun ID
blocker kind/reason code
created state/version or transition epoch
source authority refs
authority revision/event sequence
```

No free-text narrative as authority.

P1-8 may reference it but cannot create/mutate it.

---

# 7. Blocker resolution authority without cyclic ownership

Do NOT put `resolution_cycle_id` under P1-4 ownership.

Freeze the cross-owner relation exactly.

Recommended authority split:

```text
P1-4 owner:
BlockerProvenanceRef
+
BlockerResolutionTransitionRef
```

where the transition-side object proves:

```text
exact blocker_ref
same TaskContract/WorkRun
exact P1-4 TransitionDecision ref/fingerprint
transition request/evaluation/guard authority
G_BLOCKER_RESOLVED or exact accepted equivalent
resulting state/version
resolution event sequence
```

Then P1-8 deterministically derives:

```text
BLOCKER_RESOLUTION content =
{
  blocker_owner,
  blocker_id,
  blocker_ref,
  resolution_cycle_id = the P1-8 Cycle being admitted,
  accepted_transition_ref = exact verified P1-4 resolution transition
}
```

Freeze whether `accepted_transition_ref` is:

```text
A. the exact transition that resolved the blocker

or

B. the later terminal ACCEPTED transition that proves final accepted completion
```

If both are needed, freeze two refs explicitly rather than overloading one name.

The design must remove ambiguity.

## cycle relation

P1-8 must verify:

```text
blocker provenance
→ resolution transition
→ same WorkRun lineage
→ final accepted terminal lineage
→ current Cycle identity
```

without P1-4 depending on a future P1-8 Cycle.

---

# 8. blocker lifecycle/current semantics

Freeze:

```text
blocker historical existence/resolution
!= current WorkRun blocker state
```

A resolved blocker remains historical provenance.

A later new blocker does not mutate the old blocker/ref.

If one WorkRun may have multiple blockers, define:

```text
identity
ordering
same-kind duplicates
resolution cardinality
```

If V1 supports only one active blocker per WorkRun/epoch, state that exact bound.

No hidden list/quorum semantics.

---

# 9. Contract C — canonical P1-8 Policy Action Catalog

Freeze:

```text
P1_8_POLICY_ACTION_CATALOG_V1
```

as an immutable owner-authored payload.

Owner:

```text
P1_8_NEXT_ACTION_ELIGIBILITY_POLICY_AUTHORITY_V1
```

Caller/bootstrap configuration cannot define action descriptors.

## exact catalog identity

Freeze:

```text
catalog_id
catalog_version
catalog_schema
catalog_payload
catalog_fingerprint
authority_id/version/revision
issued/effective sequence
supersedes/revokes refs
```

Catalog fingerprint must be computed from the exact canonical payload.

No caller-supplied fingerprint.

---

# 10. exact V1 action entries

The design must contain the exact initial V1 descriptor entries, not only a schema.

For each action freeze:

```text
action_id
action_version
action_kind

allowed selection mode:
OPERATIONAL_RECOVERY | CYCLE_DERIVED

project/scope restrictions

parameter schema ID/version/fingerprint
allowed/default parameter rules

priority classification source contract
policy dependency ordinal
critical-path ordinal
descriptor policy ordinal

required Human input:
NONE | BEFORE_SELECTION | AFTER_TASK_ISSUANCE_P1_7

Task issuance owner:
EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY

Task template ref/hash if applicable

privacy/security restrictions

current_projection_on_invalidation
```

The catalog should be the minimum set needed for accepted P1-8 behavior.

Do not add speculative product actions.

---

# 11. required action inventory method

Before choosing entries, inventory exact accepted use cases from:

```text
P1-8 design examples and tests

canonical NEXT_ACTIONS / current roadmap

current P1-4 BLOCKED/REWORK/FAILED recovery needs

current Task issuance templates/authority if any
```

Classify every proposed action:

```text
REQUIRED_FOR_ACCEPTED_V1
OPTIONAL_FUTURE
UNSUPPORTED_NO_OWNER
```

Only `REQUIRED_FOR_ACCEPTED_V1` may enter the V1 catalog.

If an action needs a missing Task template/roadmap owner:

```text
do not fabricate it
```

Either:

```text
omit the action if accepted V1 remains complete without it

or

mark an explicit additional prerequisite baseline gap
```

---

# 12. priority mapping

Freeze the exact `NextActionSelectionPolicy` priority mapping from verified source-domain facts.

It must operationalize the accepted order:

```text
1. security/policy/missing-artifact blocker
2. rejected/HOLD/failed/rework recovery
3. canonical baseline gap/authority conflict
4. accepted core critical path
5. operational hardening
6. optional optimization
```

For each class freeze:

```text
allowed source authority kinds
exact reason codes / state classes
priority rank
required refs
tie-break inputs
```

Descriptor-static priority cannot make a blocker/recovery condition true.

---

# 13. Human-binding design

Freeze action-level Human requirement semantics.

For `BEFORE_SELECTION` define exact context binding for:

```text
OPERATIONAL_RECOVERY
CYCLE_DERIVED
```

At minimum:

```text
project
TaskContract
WorkRun or Cycle lineage
state/version/target where applicable
required Judgment kind/status
HumanResult/gate provenance
```

For multiple CYCLE_DERIVED memory refs, define whether:

```text
same Task/WorkRun context is required
```

or whether a separately owner-authorized project-level Human context exists.

Do not invent project-wide Human approval without explicit authority.

`AFTER_TASK_ISSUANCE_P1_7` remains post-issuance only.

---

# 14. capability/composition boundary

Freeze how live System owner capabilities are held.

Required:

```text
bootstrap/composition root
→ owns opaque issuance/invalidation capability

repository/service runtime interface
→ can verify/use current authority

ordinary caller/public package
→ cannot obtain live mint/revoke capability
```

No public:

```text
default_*_authority() -> live owner
```

getter.

Define a test-only factory separately.

This contract applies to:

```text
Memory policy owner
NextAction policy/catalog owner
```

---

# 15. historical replay contract additions

Freeze the prerequisite data needed for P1-8 historical replay.

## constraint

```text
original exact constraint ref/fingerprint/as-of validity
```

## blocker

```text
original blocker provenance
exact blocker-resolution transition provenance
same WorkRun relation
final accepted terminal relation
```

## action catalog

```text
original catalog/policy/descriptor immutable payload
exact enrollment
owner event high-watermark
```

Later current revocation/supersession must not invalidate historical identity.

---

# 16. migration/cut-line design only

Do not implement migration.

Freeze expected additive storage requirements.

Potential owner tables/objects may include exact equivalents of:

```text
task_constraint_authority

p1_4_blocker_provenance
p1_4_blocker_resolution_transition

p1_8_policy_action_catalog
p1_8_policy_action_catalog_entry
```

But do not force tables if current immutable payload tables can safely hold the authority.

State:

```text
which owner persists which object
append-only rules
unique identities
foreign key direction
migration ordering
historical backfill policy
```

Legacy rows without these new owner refs must not be silently upgraded.

---

# 17. no retroactive authority laundering

Mandatory:

```text
legacy TaskContract without constraint authority
→ cannot gain a historical constraint by caller backfill

legacy P1-4 blocker guard without immutable blocker provenance
→ cannot become BLOCKER_RESOLUTION memory source by caller interpretation

existing caller-authored PolicyActionCatalog candidate
→ not grandfathered as canonical owner catalog
```

Prospective issuance only unless an exact deterministic owner-backed reconstruction is proven.

---

# 18. design output must answer exact questions

The candidate design and Executor report must answer:

1. Who exactly owns `TaskConstraintRef`?
2. Is the owner existing or newly added?
3. What exact immutable fields/fingerprint define it?
4. How is a canonical-rule constraint enrolled, if supported?
5. Who exactly owns blocker identity?
6. What exact object/ref proves blocker resolution?
7. Which transition does `accepted_transition_ref` mean?
8. How is the P1-8 `resolution_cycle_id` added without cyclic ownership?
9. Can one WorkRun have multiple active blockers in V1?
10. What exact `P1_8_POLICY_ACTION_CATALOG_V1` actions exist?
11. Why is each action REQUIRED_FOR_ACCEPTED_V1?
12. What exact parameter schema does each action allow?
13. What exact source facts determine authoritative priority rank?
14. Which actions require `BEFORE_SELECTION` vs `AFTER_TASK_ISSUANCE_P1_7`?
15. What exact Human context is required?
16. How are live System capabilities hidden from ordinary callers?
17. What historical replay evidence is added for each new owner contract?
18. What additive persistence/migration is expected later?
19. Which legacy artifacts remain ineligible?
20. Are any further Human-owned decisions still open?

No implicit answer.

---

# 19. expected design status

Executor submission:

```text
P1-8 prerequisite owner authority design
→ CANDIDATE / HUMAN_REVIEW_REQUIRED

P1-8 Runtime
→ BLOCKED_REQUIRED_EVIDENCE

P2
→ NOT_STARTED
```

No runtime resume Task until this design is Human-accepted and any required predecessor owner runtime is
implemented/accepted.

---

# 20. Git policy

Design candidate remains uncommitted.

```text
NO git add
NO commit
NO push
```

Final HEAD:

```text
f4614198c2745944f7ec02639a45b0315bbc903d
```

Move Task active→done on Executor submission.

No canonical state update in this Task.

---

# 21. export

Target:

```text
.aiassistant/reports/target/
20260831_1332_aiscc-p1-8-prerequisite-owner-authority-contract-design-freeze-1/
```

Required:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
```

Include byte-preserving copies of:

```text
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md

.aiassistant/records/aiscc/cycles/
20260831_1332_aiscc-p1-8-prerequisite-owner-authority-baseline-gap-hold-1.cycle.md

done Task
```

No runtime source/test/migration export is required except exact hash inventory proving the blocked 19-path
candidate remained unchanged.

---

# 22. preserved exact paths

Preserve after submission:

```text
.aiassistant/rules/AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md

.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md

.aiassistant/records/aiscc/cycles/
20260831_1332_aiscc-p1-8-prerequisite-owner-authority-baseline-gap-hold-1.cycle.md

.aiassistant/tasks/done/
20260831_1332_aiscc-p1-8-prerequisite-owner-authority-contract-design-freeze-1.md
```
