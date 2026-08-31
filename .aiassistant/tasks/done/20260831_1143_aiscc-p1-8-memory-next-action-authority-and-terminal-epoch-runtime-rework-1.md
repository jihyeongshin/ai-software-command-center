# 작업지시서: P1-8 Memory + NextAction Authority and Terminal Epoch Runtime Rework

## meta

- task_id: `20260831_1143_aiscc-p1-8-memory-next-action-authority-and-terminal-epoch-runtime-rework-1`
- created_at: `2026-08-31T11:43:00+09:00`
- phase: `P1-8 Project Memory and Cycle Admission Runtime`
- work_type: `RUNTIME_REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1_8_PROJECT_MEMORY_CYCLE`
- expected_start_head: `f4614198c2745944f7ec02639a45b0315bbc903d`
- predecessor_runtime_path_count: `18`
- predecessor_runtime_aggregate_sha256: `37c7860008bdf04ce75e4b1e01c98185b1afdc5da73e67328bbe35670eceaf92`
- accepted_p1_8_design_sha256: `100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a`
- accepted_p1_6_durable_runtime_commit: `8320a3c567a58bab5f728a88d5c88862392d187c`
- p1_8_human_runtime_verification: `HUMAN_PENDING`

---

# 1. purpose

Rework the reviewed P1-8 runtime candidate to enforce the Human-accepted authority ceilings.

This is not a design rewrite.

The accepted design remains:

```text
.aiassistant/rules/AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md
SHA-256:
100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a
```

Place/preserve the Command Center HOLD Cycle:

```text
.aiassistant/records/aiscc/cycles/
20260831_1143_aiscc-p1-8-runtime-memory-next-action-authority-and-terminal-epoch-hold-1.cycle.md
```

---

# 2. mandatory preflight

Require:

```text
HEAD ==
f4614198c2745944f7ec02639a45b0315bbc903d

accepted P1-8 design SHA ==
100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a

P1-6 durable runtime commit ==
8320a3c567a58bab5f728a88d5c88862392d187c
```

Require exact reviewed predecessor runtime:

```text
18 paths
37c7860008bdf04ce75e4b1e01c98185b1afdc5da73e67328bbe35670eceaf92
```

Any drift:

```text
STOP
→ REVIEWED_CANDIDATE_DRIFT
```

Index must be empty.

No Git add/commit/push.

---

# 3. preserve accepted implementation foundations

Do not regress:

```text
P1-6 owner-issued P1_8_STRUCTURED_RESULT_V1 historical read grant

legacy metadata-only structured source denial

MCF_V1 canonical hashing

MemoryLineageKeyV1 canonical hashing shape

append-only history + rebuildable projections

same-content CycleMemoryReference

P1-6/P1-7 historical provenance

TaskIssuanceCandidate != TaskContract

EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY

PostgreSQL persistence/restart model

P2/P3/Public Live boundaries
```

---

# 4. MemoryDeclaration policy owner authority

Implement an exact System-owned policy issuer equivalent to:

```text
P1_8MemoryDeclarationPolicyAuthority
```

It must own:

```text
P1_8_MEMORY_DECLARATION_POLICY_AUTHORITY_V1
```

and issue/enroll only canonical immutable policy objects.

Repository must not allow a caller/configuration object to self-register as policy authority.

Required negative:

```text
rogue policy object
rogue policy authority instance
copied visible authority IDs
→ new admission DENIED
```

Required positive:

```text
bootstrap-bound exact P1-8 policy authority
→ current V1 policy enrollment PASS
```

Do not use class-name/string equality alone.

---

# 5. exact policy payload and category source contracts

The durable `MemoryDeclarationAuthorityPolicy` must carry enough exact immutable authority to enforce accepted
design sections 9.1–9.3.

At minimum bind:

```text
policy ID/version/fingerprint
authority ID/version/revision
category
authority mode
allowed source object kinds
allowed source schema/version
exact source field path/object selector
content derivation schema/version/canonicalization
subject derivation rule
applicability derivation rule
semantic-slot derivation rule
privacy ceiling/export ceiling
issued/effective sequencing
supersession/revocation disposition
```

Implement exact V1 category semantics.

For `DETERMINISTIC_POINTER`, do not reduce all categories to:

```text
{"authority_ref": pointer_ref}
```

Enforce the accepted category-specific exact tuple.

If a category requires a predecessor owner/source object that does not exist:

```text
STOP
→ IMPLEMENTATION_BASELINE_GAP
```

Do not fabricate a generic pointer authority.

---

# 6. lineage atoms become owner-derived, caller claims only

New Cycle evaluation must derive from policy/source:

```text
subject_key
applicability_key
semantic_slot
```

Caller declaration values, if retained in request schema, are only equality claims.

Required:

```text
owner-derived subject/applicability/slot
!= caller claim
→ MEMORY_DECLARATION_SOURCE_MISMATCH
```

`MemoryLineageKeyV1` is then calculated only from the owner-derived atoms.

Syntactic normalization alone is insufficient.

Add tests proving a caller cannot move identical source content into another logical lineage by choosing another
valid-looking atom.

---

# 7. privacy derivation

Do not hardcode all memory entries to `INTERNAL`.

Compute:

```text
effective privacy
= max-restriction(source privacy, policy privacy ceiling)
```

under the accepted P1-8 privacy model.

Required:

```text
NON_EXPORTABLE source
→ cannot become INTERNAL or PUBLIC_SANITIZED

PUBLIC_SANITIZED
→ visibility maximum only
→ no automatic export permission
```

Persist exact source/policy privacy authority refs/fingerprints as needed for replay.

---

# 8. memory policy owner-event/current projection

Implement append-only owner events:

```text
ISSUED
SUPERSEDED
REVOKED
```

with exact immutable disposition.

New admission:

```text
current unsuperseded eligible policy only
```

Historical Cycle replay:

```text
exact original as-of-admission policy validity
currentness now NOT required
```

Current memory applicability:

```text
policy revocation
or WITHDRAW_CURRENT disposition

→ append ProjectMemoryAuthorityEvent
→ withdraw affected current entries
```

Historical entries/Cycles remain immutable.

Add policy invalidation/rebuild/restart proofs.

---

# 9. terminal epoch identity

Introduce an exact durable terminal epoch key.

Equivalent accepted fields:

```text
project_id
task_contract_id
task_contract_version
work_run_id
terminal_transition_decision_ref
resulting_state_version
```

Enforce:

```text
one terminal epoch
→ one admission lineage
```

Database support must prevent duplicate distinct Cycle IDs for the same epoch.

Required semantics:

```text
same epoch + same immutable admitted payload
→ replay existing Cycle lineage

same epoch + different payload
→ TERMINAL_EPOCH_CONFLICT
```

Do not rely only on advisory lock + `cycle_id` lookup.

Add serial and concurrent tests using different Cycle IDs.

---

# 10. exact TaskContract binding

Do not store an unverified caller-provided `task_contract_fingerprint` as historical authority.

Use one of:

```text
exact predecessor-owned TaskContract ref/hash
```

if available,

or an explicitly named deterministic **P1-8 binding fingerprint** computed solely from already owner-verified
TaskContract ID/version/project fields.

If the accepted TaskContract hash/ref contract cannot be satisfied without inventing new owner authority:

```text
STOP
→ IMPLEMENTATION_BASELINE_GAP
```

Do not fabricate authority.

---

# 11. admission source-event high-watermark

Persist an exact initial currentness observation boundary.

For every current-sensitive source/policy needed by admission, bind equivalent:

```text
owner-event high-watermark / revision
observation result
initial applicability event
```

Do not put later currentness into immutable Cycle historical identity.

Required:

```text
historical source validity
→ terminal epoch proof

current source effectiveness
→ admission observation high-watermark

current ProjectMemory applicability
→ append-only projection
```

Later owner events append current applicability changes.

Add a concurrent source-invalidation/admission test and deterministic restart/rebuild proof.

---

# 12. NextAction policy/descriptor owner authority

Implement exact System-owned authority equivalent to:

```text
P1_8NextActionPolicyAuthority
```

covering:

```text
NextActionEligibilityPolicy
NextActionSelectionPolicy
NextActionDescriptor enrollment
```

Caller/configuration objects cannot self-enroll.

Required negative:

```text
rogue eligibility policy
rogue selection policy
rogue descriptor
foreign authority instance
copied visible authority IDs
→ DENIED
```

The eligibility policy must durably bind the exact enrolled descriptor refs/fingerprints.

---

# 13. ActionRef and descriptor contract

Bring runtime objects to the accepted V1 authority shape.

`ActionRef` must bind exact equivalent of:

```text
eligibility policy ID/version
action ID/version
descriptor fingerprint
```

Descriptor must durably bind accepted fields including:

```text
project/scope restrictions
parameter schema ID/version/fingerprint + exact rules
source authority kind/ref/version/fingerprint
allowed selection mode
authoritative priority classification source ref/hash/ordinal
required Human input kind
Task issuance owner
Task template ref/hash where applicable
privacy/security restrictions
authority revision
issued/effective sequencing
supersedes/revocation refs
current_projection_on_invalidation
```

Do not treat arbitrary `source_id/source_version` strings as canonical authority.

For:

```text
CANONICAL_ROADMAP_ITEM
TASK_CONTRACT_FOLLOW_UP_TEMPLATE
POLICY_ACTION_CATALOG
```

verify the exact enrolled owner source.

If a required owner does not exist:

```text
NOT_SUPPORTED
or IMPLEMENTATION_BASELINE_GAP
```

according to the accepted design; never self-mint it from proposal/configuration.

---

# 14. eligibility-policy-to-descriptor enrollment binding

New selection must prove:

```text
current eligibility policy
→ exact descriptor ActionRef/fingerprint is enrolled by that policy
```

A globally persisted descriptor is insufficient.

Historical replay must prove the same relationship as-of original selection issuance.

Add:

```text
descriptor exists/current
but not enrolled by selected eligibility policy
→ NEXT_ACTION_ACTION_NOT_ENROLLED
```

---

# 15. authoritative OPERATIONAL_RECOVERY inputs

Change the selection contract so `OPERATIONAL_RECOVERY` consumes exact owner-backed operational facts.

At minimum accepted equivalents:

```text
current P1-4 WorkRun/state/version
exact blocker/failure/rework refs where applicable
current P1-7 Judgment refs where applicable
selection-policy authority mapping
```

Required:

```text
no actual recovery condition
→ no OPERATIONAL_RECOVERY selection
```

Do not infer recovery authority from:

```text
proposal rationale
proposal claims
static descriptor rank alone
```

Priority class/rank must be owner/policy-derived.

---

# 16. CYCLE_DERIVED authority

Preserve:

```text
CURRENT ProjectMemory only
same project/scope
```

Also validate descriptor mode/scope authority.

Historical/non-current entries:

```text
SUPERSEDED
REVOKED
EXPIRED
NOT_CURRENT_CONTEXT
→ never current selection input
```

---

# 17. Human input kinds and exact P1-7 binding

Replace boolean-only Human requirement with accepted exact enum:

```text
NONE
BEFORE_SELECTION
AFTER_TASK_ISSUANCE_P1_7
```

For `BEFORE_SELECTION`, require an exact P1-7 Judgment/Human authority binding to the descriptor/policy's
required project/task/run/scope/context.

Reject:

```text
foreign project Judgment
foreign TaskContract Judgment
unrelated WorkRun Judgment
wrong Human input kind
```

`AFTER_TASK_ISSUANCE_P1_7`:

```text
does not authorize selection
does not require pre-selection Judgment
is handed to the later externally issued Task flow only
```

P1-8 never mints P1-7 authority.

---

# 18. NextAction current invalidation

Implement policy/descriptor owner-event processing.

When:

```text
descriptor/policy REVOKED
or current_projection_on_invalidation = WITHDRAW_CURRENT
```

append exact:

```text
NextActionAuthorityEvent
```

with expected project revision and withdraw current projection.

Required:

```text
historical replay
→ PASS

current projection
→ withdrawn

new selection with stale object
→ DENY
```

Do not rewrite old selection.

---

# 19. historical NextAction replay

Verify full original authority graph as-of selection issuance:

```text
selection immutable payload/fingerprint
evaluation/ranking trace
eligibility policy payload/fingerprint/authority
selection policy payload/fingerprint/authority
descriptor payload/fingerprint/source authority
exact policy-to-descriptor enrollment
policy/descriptor owner-event fold through original high-watermark
validated parameters
authoritative input refs
Human input authority when required
```

Later revocation is not historical corruption.

Revocation/supersession already effective before original issuance:

```text
→ historical provenance invalid
```

---

# 20. migration

The current head is:

```text
20260831_0006
```

If schema changes are required, create the next linear additive migration.

Do not edit/rewrite `20260831_0006` historical migration in place if doing so would make the reviewed migration
identity ambiguous.

Preferred:

```text
20260831_0007_p1_8_authority_contract_rework.py
```

Use exact next repository convention.

Required likely additions include equivalents of:

```text
terminal_epoch_key unique identity

policy authority/payload/enrollment linkage

descriptor enrollment relationship

source/policy current-observation metadata

current selection withdrawal support
```

No destructive predecessor rewrite.

---

# 21. required regression tests

## 21.1 Cycle

```text
same terminal epoch + different Cycle IDs + same payload
→ one lineage / replay

same terminal epoch + different payload
→ typed conflict

concurrent variants
→ same guarantees

unverified TaskContract hash claim
→ cannot become authority
```

## 21.2 Memory authority

```text
rogue memory policy
→ denied

caller-selected lineage atoms
→ denied

wrong category/source tuple
→ denied

privacy ceiling/source privacy
→ enforced

policy revocation current withdrawal
→ historical replay preserved

policy invalid-before-admission
→ deny
```

## 21.3 source high-watermark

```text
delayed admission with source already revoked
→ zero CURRENT exposure

concurrent source invalidation
→ exact high-watermark semantics

restart
→ same current projection
```

## 21.4 NextAction owner/catalog

```text
rogue policy/descriptor enrollment
→ denied

descriptor not enrolled by eligibility policy
→ denied

fake roadmap/template source
→ denied

policy/descriptor historical replay as-of issuance
→ exact
```

## 21.5 operational recovery

```text
no current blocker/failure/rework authority
→ no recovery selection

exact owner-backed recovery facts
→ deterministic selection

caller claims
→ no priority effect
```

## 21.6 Human binding

```text
foreign project Judgment
→ denied

foreign task/run Judgment
→ denied

wrong Human requirement kind
→ denied

correct BEFORE_SELECTION authority
→ PASS

AFTER_TASK_ISSUANCE_P1_7
→ no pre-selection substitution
```

## 21.7 current withdrawal

```text
current selection
→ descriptor/policy invalidated
→ historical replay PASS
→ current projection withdrawn
→ new stale selection denied
```

---

# 22. predecessor regressions

Fresh rerun:

```text
complete repository suite

P1-4 PostgreSQL
P1-6 core PostgreSQL
P1-6 durable-content PostgreSQL
P1-7 PostgreSQL
P1-8 Cycle/Memory/NextAction PostgreSQL
```

Baseline complete repository:

```text
212 / 212 PASS
```

Explain collection delta.

No hidden deselection/ignore/xfail conversion.

Run:

```text
ruff
mypy src
alembic check
```

Report exact versions/counts.

---

# 23. Git policy

Runtime rework candidate remains uncommitted.

```text
NO git add
NO commit
NO push
```

Final HEAD must remain:

```text
f4614198c2745944f7ec02639a45b0315bbc903d
```

Move Task active→done only on Executor completion.

Do not update canonical state files.

Human P1-8 runtime verification:

```text
HUMAN_PENDING
```

---

# 24. mandatory STOP conditions

STOP rather than weakening accepted design when:

```text
a required Memory category has no predecessor owner/source authority

canonical roadmap/template authority does not exist for a requested descriptor source kind

exact TaskContract hash/ref cannot be owner-verified and accepted design cannot be satisfied by an explicitly
non-authoritative derived binding

P1-4/P1-6/P1-7 semantics would need mutation

P1-8 would need P1-6 durable write/grant-mint authority

terminal high-watermark semantics require forbidden predecessor lock-order inversion

migration would require destructive predecessor rewrite

P2/P3 scope is required
```

Use exact:

```text
IMPLEMENTATION_BASELINE_GAP
POLICY_CONFLICT_INVESTIGATION_REQUIRED
LEGACY_PROVENANCE_REGRESSION
```

and report the smallest missing owner contract.

---

# 25. export

Target:

```text
.aiassistant/reports/target/
20260831_1143_aiscc-p1-8-memory-next-action-authority-and-terminal-epoch-runtime-rework-1/
```

Required:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
```

Include byte-preserving final runtime changed source/test/migration paths, HOLD Cycle, and done Task.

Runtime aggregate:

```text
source/test/migration only
```

Report:

```text
predecessor 18-path aggregate
final path count
per-file SHA
final aggregate
source/copy identity
HEAD/index/Git actions
```

---

# 26. expected submission state

```text
P1-8 Design:
ACCEPTED / CLOSED

P1-8 Runtime:
REWORKED_CANDIDATE / HUMAN_PENDING

P2:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

Command Center next:

```text
review exact reworked candidate

→ PASS / HUMAN_FINAL_REVIEW_REQUIRED
or
→ HOLD_REWORK_REQUIRED
or
→ BLOCKED_REQUIRED_EVIDENCE if a real predecessor owner baseline is missing
```

No runtime terminal commit before Human final acceptance.
