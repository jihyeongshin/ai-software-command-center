# 작업지시서: P1-8 Historical Replay + System Owner Capability Runtime Rework

## meta

- task_id: `20260831_1332_aiscc-p1-8-historical-replay-and-system-owner-capability-runtime-rework-1`
- created_at: `2026-08-31T13:32:00+09:00`
- phase: `P1-8 Project Memory and Cycle Admission Runtime`
- work_type: `RUNTIME_REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1_8_PROJECT_MEMORY_CYCLE`
- expected_start_head: `f4614198c2745944f7ec02639a45b0315bbc903d`
- predecessor_runtime_path_count: `19`
- predecessor_runtime_aggregate_sha256: `84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42`
- accepted_p1_8_design_sha256: `100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a`
- accepted_p1_6_durable_runtime_commit: `8320a3c567a58bab5f728a88d5c88862392d187c`
- human_p1_8_runtime_verification: `HUMAN_PENDING`

---

# 1. purpose

Close the remaining historical-replay and System-owner capability gaps in the P1-8 runtime candidate.

This is not a design rewrite.

Preserve the Human-accepted P1-8 design exactly.

Place/preserve:

```text
.aiassistant/records/aiscc/cycles/
20260831_1332_aiscc-p1-8-runtime-historical-replay-and-system-owner-capability-hold-1.cycle.md
```

---

# 2. mandatory preflight

Require:

```text
HEAD ==
f4614198c2745944f7ec02639a45b0315bbc903d

accepted P1-8 design SHA ==
100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a

predecessor runtime ==
19 paths /
84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42
```

Index must be empty.

No Git add/commit/push.

Any drift:

```text
STOP
→ REVIEWED_CANDIDATE_DRIFT
```

---

# 3. historical Memory replay must rederive from source

Refactor Cycle historical verification so every stored MemoryDeclaration is independently reconstructed from
the original authority graph.

For every declaration ordinal:

```text
load original policy ref/version/fingerprint
verify canonical policy payload and issuer/as-of-admission validity

resolve original exact source:
- structured P1-6 body through owner-issued P1_8_STRUCTURED_RESULT_V1 grant
- exact P1-4/P1-6/P1-7 deterministic pointer
- exact canonical enrolled source

derive owner-backed VerifiedMemorySource

run exact policy derivation again:
→ expected content
→ MCF_V1
→ subject
→ applicability
→ semantic slot
→ privacy

compare with immutable stored declaration / ProjectMemoryEntry / CycleMemoryReference
```

Do not use current policy/current source effectiveness as historical identity.

Do not merely compare stored normalized content with its own stored hash.

Required corruption tests:

```text
tampered ProjectMemoryEntry normalized content + matching recomputed local hash
but source body unchanged
→ historical replay FAIL

tampered stored lineage claims + internally matching lineage hash
but source-derived atoms unchanged
→ historical replay FAIL
```

Use DB corruption fixtures only in tests; production rows remain append-only.

---

# 4. CycleMemoryReference must preserve full declaration authority

Same-content reuse must not weaken verification.

Persist enough reference provenance to prove:

```text
Cycle declaration ordinal
policy ref/fingerprint
source authority ref/fingerprint
derived MemoryLineageKey
derived MCF_V1
referenced entry ID/content fingerprint
```

Historical replay:

```text
rederive declaration from source
→ compare exact lineage/content/policy/source
→ only then accept CycleMemoryReference
```

Same-content reference is a storage/projection optimization, not a semantic-authority shortcut.

---

# 5. same-content delayed-admission currentness

Fix the early same-content branch.

If admission high-watermark proves that the referenced current entry's own source/policy is already non-current:

```text
append ProjectMemoryAuthorityEvent in the same transaction
withdraw current tip before publication
create historical CycleMemoryReference
```

If existing identical content is backed by an independent still-current source, preserve that valid current tip.

Add exact tests:

```text
same source/content
source revoked
invalidation projector not yet run
new accepted Cycle arrives
→ no CURRENT tip after transaction

different source same content
existing source still current
new source revoked
→ existing source-backed CURRENT entry remains valid
→ new Cycle reference remains historical provenance only
```

---

# 6. remove public access to live System owner capabilities

Do not expose the recognized live owner objects through public/default getters.

Production/public package API must not let ordinary caller code obtain:

```text
P1_8MemoryDeclarationPolicyAuthority live issuance/invalidation capability

P1_8NextActionPolicyAuthority live issuance/invalidation capability
```

Remove or privatize:

```text
default_memory_policy_authority()
default_next_action_policy_authority()
```

from production caller-visible API.

Use a composition/bootstrap boundary equivalent to:

```text
P1_8RuntimeAuthorityBundle / bootstrap factory

→ internally owns opaque capability
→ constructs repository/service objects
→ returns only non-minting runtime interfaces
```

Repository constructors may receive the private capability internally, but callers cannot retrieve it back.

Required tests:

```text
public aiscc.memory / aiscc.next_action API
→ no live owner capability getter

foreign authority instance
→ denied

copied visible IDs
→ denied

repository/service caller
→ cannot mint policy, descriptor, owner event
```

Do not use string/class identity as sole protection.

---

# 7. POLICY_ACTION_CATALOG must be owner-authored, not caller-defined

Current `issue_policy_catalog_v1(catalog_id, actions, ...)` accepts descriptor definitions from the caller.

Replace it with an exact owner-backed issuance model.

Preferred:

```text
P1_8_POLICY_ACTION_CATALOG_V1
```

as an immutable versioned canonical owner payload with exact:

```text
catalog ID/version/fingerprint
descriptor definitions
priority classification mapping
Human requirements
allowed modes/scopes
security/privacy restrictions
```

The policy authority may issue/enroll descriptors only from that canonical catalog payload.

Alternative allowed only if an existing external owner already exists:

```text
owner-issued PolicyActionCatalog ref/hash/payload
→ exact verifier
→ P1-8 descriptor issuance
```

Caller cannot submit `actions` to define new descriptors.

If no exact owner-backed catalog can be established from accepted/current baseline:

```text
STOP
→ IMPLEMENTATION_BASELINE_GAP
```

Do not treat arbitrary bootstrap configuration as authority.

---

# 8. complete exact Memory category contracts or STOP

The accepted V1 table requires exact contracts for:

```text
DECISION
INVARIANT_POINTER
CONSTRAINT_POINTER
LESSON = NOT_SUPPORTED
BLOCKER_RESOLUTION
PROVENANCE_POINTER
NEXT_ACTION_CONTEXT
```

Runtime policy must not advertise:

```text
CONSTRAINT_POINTER → DETERMINISTIC_POINTER
BLOCKER_RESOLUTION → DETERMINISTIC_POINTER
```

without the exact contract.

For `CONSTRAINT_POINTER`, support only owner-backed:

```text
TaskContract constraint ref/fingerprint
or canonical rule constraint ref/hash/anchor
```

For `BLOCKER_RESOLUTION`, support only exact:

```text
blocker_owner
blocker_id
blocker_ref
resolution_cycle_id
accepted_transition_ref
```

If those predecessor owners do not exist:

```text
STOP
→ IMPLEMENTATION_BASELINE_GAP
```

and report the exact missing owner object/API.

Do not silently return a generic “no contract” while claiming V1 runtime complete.

---

# 9. historical NextAction descriptor verification

Historical replay must be independent of current configured catalog.

Parse the stored descriptor's exact immutable schema and recompute:

```text
descriptor fingerprint
ActionRef
source authority fingerprint
parameter schema fingerprint
priority source hash
Task template/source refs where applicable
```

Verify:

```text
stored descriptor fingerprint
== recomputed fingerprint

ENROLLED owner-event payload
binds exact descriptor fingerprint

eligibility-policy enrollment row
binds exact ActionRef/fingerprint

all valid as-of original owner-event high-watermark
```

Current catalog absence/replacement must not break historical replay.

Later revocation remains ordinary current staleness.

---

# 10. CYCLE_DERIVED historical currentness proof

At selection time persist an exact ProjectMemory applicability observation boundary.

Acceptable equivalent:

```text
memory_authority_event_high_watermark
or per-entry applicability revision/event sequence
```

`NextActionEvaluation` must commit to it.

Historical selection replay must prove every CYCLE_DERIVED memory input:

```text
same project/scope
was CURRENT at original selection issuance
at exact observed memory authority revision/high-watermark
```

Later memory revocation/supersession:

```text
historical selection replay PASS
current selection projection/current future eligibility changes separately
```

Do not rely only on `ProjectMemoryEntryRow exists`.

---

# 11. authoritative OPERATIONAL_RECOVERY priority mapping

Keep the current exact P1-4 recovery fact verification.

Add deterministic priority classification owned by `NextActionSelectionPolicy`.

The selection policy must map exact verified facts/reason classes to the accepted priority classes, including:

```text
security/policy/missing-artifact blocker
rejected/HOLD/failed/rework recovery
baseline/authority conflict
accepted core critical path
operational hardening
optional optimization
```

For OPERATIONAL_RECOVERY:

```text
verify current WorkRun/transition/Judgment/blocker facts
→ derive authoritative priority class/rank
→ store reason/source refs
→ ranking uses resolved rank
```

Descriptor may provide policy ordinal/tie-break metadata but must not make the operational fact true.

Proposal claims remain audit-only.

Add two eligible actions where static descriptor order conflicts with authoritative recovery priority and prove
the policy-derived priority wins.

---

# 12. mandatory Human context binding

For `BEFORE_SELECTION`, Human authority must bind to the actual selection context even if descriptor optional
scope strings are empty.

## OPERATIONAL_RECOVERY

Require:

```text
Judgment project == selection project
Judgment WorkRun == operational_work_run_id
Judgment TaskContract == WorkRun TaskContract
required state/version/target context matches policy/descriptor
Human-owned gate/result provenance valid
```

## CYCLE_DERIVED

Derive the required context from exact source Cycle/ProjectMemory entries.

If multiple memory refs span incompatible Task/run Human contexts:

```text
NEXT_ACTION_HUMAN_BINDING_MISMATCH
```

unless the accepted policy explicitly declares a project-level Human context and provides exact owner authority
for that broader scope.

Descriptor scope restrictions may narrow this requirement; they cannot remove it.

`AFTER_TASK_ISSUANCE_P1_7` must not satisfy `BEFORE_SELECTION`.

Add same-project foreign-work-run and foreign-task negative tests.

---

# 13. historical operational input consistency

Strengthen `_verify_authoritative_inputs_as_of()`.

For OPERATIONAL_RECOVERY prove:

```text
evaluation.operational_work_run_id
== verified transition WorkRun

selection project
== verified WorkRun project

verified WorkRun/task/state/version
== exact original recovery context

transition request/decision refs in authoritative_input_refs
== exact verified graph
```

For Human BEFORE_SELECTION replay prove the exact same context relation.

Stored hashes are not enough; semantic source relation must be recomputed.

---

# 14. policy/descriptor owner-event capability path

Owner invalidation APIs must follow the same private bootstrap capability rule as issuance.

Caller must not be able to obtain the live owner and call:

```text
invalidate(...)
apply_owner_event(...)
```

without an owner-authenticated internal command path.

Repository continues to verify opaque owner events.

Historical objects remain append-only.

---

# 15. migration

Current head:

```text
20260831_0007
```

If schema changes are needed, create additive next revision:

```text
20260831_0008_<exact-name>.py
```

Do not rewrite 0006/0007.

Likely additions may include:

```text
CycleMemoryReference authority/source fields

NextAction memory applicability observation boundary

canonical catalog identity/enrollment
```

No destructive predecessor rewrite.

---

# 16. required test groups

At minimum add:

## Cycle/Memory historical replay

```text
source body vs stored memory semantic corruption negative

source-derived lineage vs stored lineage corruption negative

CycleMemoryReference exact source/policy replay

same-content delayed revoked source zero-CURRENT

same-content independent valid source retention
```

## owner capability

```text
public package cannot obtain live System issuer

caller cannot define catalog actions

foreign owner denied

owner event minting inaccessible to ordinary repository caller
```

## category completeness

```text
each accepted V1 category exact contract
or mandatory IMPLEMENTATION_BASELINE_GAP STOP proof
```

## NextAction historical

```text
descriptor payload/fingerprint recomputation

ENROLLED event exact fingerprint binding

CYCLE_DERIVED memory was CURRENT at issuance

later memory revocation preserves historical replay
```

## recovery priority

```text
verified recovery fact changes authoritative priority

proposal/static rank cannot override source/policy class
```

## Human

```text
same project / foreign WorkRun Judgment denied

same project / foreign Task Judgment denied

correct exact context accepted

AFTER_TASK_ISSUANCE does not satisfy BEFORE_SELECTION
```

---

# 17. regressions

Fresh:

```text
complete repository

P1-4 PostgreSQL

P1-6 core + durable PostgreSQL

P1-7 PostgreSQL

P1-8 PostgreSQL

ruff
mypy src
alembic check
```

Current baseline:

```text
215 / 215 PASS
```

Explain collection delta.

No test hiding/deselection/xfail conversion.

---

# 18. mandatory STOP

STOP, do not weaken design, if:

```text
CONSTRAINT_POINTER exact owner does not exist

BLOCKER_RESOLUTION exact blocker owner does not exist

owner-backed PolicyActionCatalog authority does not exist and cannot be defined without new Human design choice

required canonical roadmap/template owner is needed for the current catalog

P1-4/P1-6/P1-7 semantics must change

P1-8 needs P1-6 write/grant-mint authority

Human binding requires a new P1-7 authority kind

schema needs destructive predecessor rewrite
```

Use:

```text
IMPLEMENTATION_BASELINE_GAP
POLICY_CONFLICT_INVESTIGATION_REQUIRED
LEGACY_PROVENANCE_REGRESSION
```

Report the smallest missing owner contract exactly.

A correct STOP is preferable to fabricating authority.

---

# 19. Git policy

Runtime candidate remains uncommitted.

```text
NO git add
NO commit
NO push
```

Final HEAD remains:

```text
f4614198c2745944f7ec02639a45b0315bbc903d
```

Move this Task active→done only on Executor completion/STOP.

Do not update canonical state.

Human P1-8 runtime verification remains:

```text
HUMAN_PENDING
```

---

# 20. export

Target:

```text
.aiassistant/reports/target/
20260831_1332_aiscc-p1-8-historical-replay-and-system-owner-capability-runtime-rework-1/
```

Required:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
```

Include byte-preserving final runtime source/test/migration paths, HOLD Cycle, done Task.

Report:

```text
predecessor:
19 paths / 84641ac35f...

final path count
per-file SHA
final aggregate

source/copy identity

HEAD/index/Git actions
```

---

# 21. expected outcomes

Successful rework:

```text
P1-8 Runtime:
REWORKED_CANDIDATE / HUMAN_PENDING
```

If the missing accepted owner contracts are real:

```text
P1-8 Runtime:
BLOCKED_REQUIRED_EVIDENCE / IMPLEMENTATION_BASELINE_GAP
```

Command Center will review the exact result before Human runtime final review.

No terminal runtime commit before Human acceptance.
