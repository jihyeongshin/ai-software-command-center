# AISCC Cycle Record

## meta

- cycle_id: `20260831_1143_aiscc-p1-8-runtime-memory-next-action-authority-and-terminal-epoch-hold-1`
- date: `2026-08-31T11:43:00+09:00`
- phase: `P1-8 Project Memory and Cycle Admission Runtime`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1_8_PROJECT_MEMORY_CYCLE`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause: `P1_8_AUTHORITY_CEILINGS_UNDER_IMPLEMENTED`
- reviewed_head: `f4614198c2745944f7ec02639a45b0315bbc903d`
- reviewed_runtime_path_count: `18`
- reviewed_runtime_aggregate_sha256: `37c7860008bdf04ce75e4b1e01c98185b1afdc5da73e67328bbe35670eceaf92`

---

# 1. independently verified candidate identity

The exported runtime bytes were independently hashed.

```text
18 / 18 runtime per-file SHA-256:
MATCH

runtime aggregate:
37c7860008bdf04ce75e4b1e01c98185b1afdc5da73e67328bbe35670eceaf92
MATCH

HEAD:
f4614198c2745944f7ec02639a45b0315bbc903d

Git add/commit/push:
none
```

Reported verification evidence is accepted as submitted:

```text
complete repository:
212 / 212 PASS

P1-4 PostgreSQL:
18 / 18 PASS

P1-6:
7 / 7 PASS

P1-7:
2 / 2 PASS

PostgreSQL:
17.6

Alembic:
20260831_0006

ruff:
PASS

mypy:
76 source files PASS
```

This HOLD is based on source/design authority review, not candidate identity drift.

---

# 2. accepted portions

Preserve the following implementation work unless a narrow change is required by the findings below.

```text
P1-6 durable historical body consumer integration
P1_8_STRUCTURED_RESULT_V1 owner-issued read grant use
legacy metadata-only structured source denial
PostgreSQL P1-8 schema/migration baseline
append-only Cycle/Memory/NextAction history tables
projection tables separated from immutable history
MCF_V1 fixed serializer
MemoryLineageKeyV1 hash shape
one-current-tip projection structure
same-content CycleMemoryReference mechanism
basic restart/rebuild corruption checks
TaskIssuanceCandidate external owner constant
no TaskContract minting
no P2/P3/Public Live
```

---

# 3. FINDING A — caller-controlled MemoryDeclaration lineage/taxonomy remains semantic authority

Accepted design requires:

```text
policy/source-derived subject
policy/source-derived applicability
policy/source-derived semantic slot
policy/source-derived privacy ceiling

caller values
→ equality claims only
```

Current runtime instead accepts caller fields directly:

```text
MemoryDeclaration.subject_key
MemoryDeclaration.applicability_key
MemoryDeclaration.semantic_slot
```

and `PostgresCycleAdmissionRepository._persist_memory()` passes them directly into:

```text
memory_lineage_key(...)
```

The only validation is syntactic normalization.

Therefore a caller with an otherwise legitimate terminal source can choose a different semantic lineage by
choosing another syntactically valid subject/applicability/slot.

That violates the accepted 1933 design closure:

```text
caller free text / caller-selected lineage atoms
!= MemoryLineageKey authority
```

## deterministic pointer categories are also collapsed

Current `derive_memory_content()` treats every `DETERMINISTIC_POINTER` category as:

```text
pointer_ref must be one of a small terminal ref set
derived content = {"authority_ref": pointer_ref}
```

This does not implement the accepted exact category contracts:

```text
INVARIANT_POINTER
→ exact enrolled canonical authority/ref/fingerprint/anchor

CONSTRAINT_POINTER
→ exact constraint owner/logical ID/ref/fingerprint

BLOCKER_RESOLUTION
→ exact blocker owner/id/ref + accepted resolution Cycle/TransitionDecision refs

PROVENANCE_POINTER
→ exact role/object kind/logical ID/ref/fingerprint
```

A transition ref can currently be nominated under an unrelated deterministic-pointer category without the
category-specific owner tuple.

## privacy is not source/policy-derived

New memory entries are persisted with:

```text
privacy = INTERNAL
```

unconditionally.

This can be more permissive than `NON_EXPORTABLE`, and it ignores the accepted rule:

```text
effective privacy
= more restrictive of source privacy and policy ceiling
```

### required correction

P1-8 must derive:

```text
subject_key
applicability_key
semantic_slot
privacy
normalized content
```

from the exact enrolled policy + owner-backed source.

Caller declarations may contain claimed values only for equality checking.

If a required source owner does not exist in the predecessor runtime for a category, do not fabricate it.
Return/STOP with:

```text
IMPLEMENTATION_BASELINE_GAP
```

for that category rather than weakening the accepted category contract.

---

# 4. FINDING B — MemoryDeclaration policy authority is caller/configuration mintable

`MemoryDeclarationAuthorityPolicy` is a freely constructible dataclass.

`PostgresCycleAdmissionRepository` accepts any injected policy and exposes:

```text
enroll_memory_policy()
```

which persists that injected policy as `ISSUED`.

There is no bootstrap-bound owner capability proving:

```text
P1_8_MEMORY_DECLARATION_POLICY_AUTHORITY_V1
```

issued the policy.

A caller can therefore construct a different policy with different modes/selectors/priorities and use a
repository configured with that policy to enroll/admit it.

Required invariant:

```text
caller/configured policy object
!= P1-8 policy issuance authority
```

### required correction

Introduce one exact owner authority equivalent to:

```text
P1_8MemoryDeclarationPolicyAuthority
```

that:

```text
owns the V1 policy issuance capability
mints/enrolls only exact Human-accepted V1 policy payloads
persists canonical immutable policy payload/fingerprint
issues policy owner events
binds repository new-admission policy resolution
```

Repository must not accept a caller-substitutable issuer/verifier per operation.

A rogue policy object or foreign owner authority must fail closed.

---

# 5. FINDING C — memory-policy invalidation/current-withdrawal path is missing

Accepted design section 12.6 requires:

```text
memory policy owner event
→ ProjectMemoryAuthorityEvent
→ ProjectMemoryView withdrawal where disposition requires it
```

Current runtime only enrolls `ISSUED` policy state and rejects a non-singleton event history for new admission.

There is no owner-backed policy supersession/revocation API that:

```text
preserves historical Cycle replay
withdraws current entries according to immutable policy disposition
updates/rebuilds current projection append-only
```

Required correction:

```text
policy event history
ISSUED / SUPERSEDED / REVOKED
with exact as-of validity

new admission
→ current policy only

historical replay
→ original as-of policy validity

current memory use
→ withdrawal event when required
```

Ordinary current policy staleness must not become historical corruption.

---

# 6. FINDING D — terminal epoch uniqueness is not enforced for different Cycle IDs

Accepted design:

```text
one terminal epoch
→ one admission lineage

same terminal epoch + same payload
→ replay

same terminal epoch + different payload
→ TERMINAL_EPOCH_CONFLICT
```

Current runtime obtains a terminal advisory lock, but after the lock it checks only:

```text
AdmittedCycleRow by candidate.cycle_id
```

There is no lookup/unique constraint for an already-admitted different `cycle_id` on the same terminal epoch.

The migration likewise has no unique terminal-epoch key/constraint.

Thus two serial requests using different Cycle IDs can both be admitted for the same accepted terminal
WorkRun/state version.

### required correction

Persist an exact deterministic terminal epoch identity equivalent to:

```text
(project_id,
 task_contract_id,
 task_contract_version,
 work_run_id,
 terminal_transition_decision_ref,
 resulting_state_version)
```

and enforce database + transaction semantics:

```text
same epoch + same immutable payload
→ replay existing lineage

same epoch + different payload
→ TERMINAL_EPOCH_CONFLICT
```

Add fresh concurrent and serial different-Cycle-ID proofs.

---

# 7. FINDING E — admission-observation source high-watermark is not durably bound

Accepted design requires one transaction to fold source-owner authority events through an exact admission
observation high-watermark, then publish initial current applicability.

Current runtime calculates currentness using:

```text
_invalid_at(... datetime.max ...)
```

but does not persist the exact source-event high-watermark/revision that was folded into the initial
applicability decision.

Consequences:

```text
historical replay cannot prove exactly which currentness events were observed at admission

projection rebuild cannot deterministically distinguish initial observation from later source-owner events
```

and a concurrent source invalidation has no durable admission-observation boundary.

### required correction

Persist/bind, without contaminating immutable historical Cycle identity:

```text
source authority event high-watermark / revision
observed currentness
initial applicability authority event
```

according to the accepted design.

Later source events:

```text
do not rewrite Cycle/entry
→ append current applicability events only
```

Add delayed-admission/concurrent-invalidation proof showing the accepted high-watermark semantics and no
unexplained CURRENT projection.

---

# 8. FINDING F — NextAction policy/descriptor enrollment authority is self-mintable

Current runtime permits:

```text
NextActionEligibilityPolicy(...)
NextActionSelectionPolicy(...)
NextActionDescriptor.create(...)

PostgresNextActionRepository(
    ...,
    eligibility_policy=<caller/configuration object>,
    selection_policy=<caller/configuration object>,
    descriptors=(...)
)

repository.enroll_configured_authority()
```

No exact owner capability proves that:

```text
P1_8_NEXT_ACTION_ELIGIBILITY_POLICY_AUTHORITY_V1
```

issued/enrolled those objects.

Policy fingerprints are supplied as fields rather than recomputed from a complete owner-authored canonical
payload.

The eligibility policy row also does not durably commit to the exact descriptor enrollment set.

Therefore a caller/configuration path can create a new action catalog and then select from it.

This reopens the 1933 action-laundering finding.

### required correction

Introduce exact System owner authority objects/capabilities for:

```text
NextActionEligibilityPolicy
NextActionSelectionPolicy
NextActionDescriptor enrollment
```

Required:

```text
policy canonical payload/fingerprint computed by owner
exact descriptor refs/fingerprints enrolled by eligibility policy
repository cannot substitute a caller-created policy/descriptor authority
rogue/foreign owner objects denied
```

---

# 9. FINDING G — ActionRef/Descriptor contract is materially narrower than accepted V1

Accepted `ActionRefV1` binds:

```text
eligibility policy ID/version
action ID/version
descriptor fingerprint
```

Current `ActionRef` binds only:

```text
source_kind
source_id
source_version
action_key
```

Accepted descriptor authority includes, among other fields:

```text
project/scope restrictions
parameter schema ID/version/fingerprint
source authority kind/ref/version/fingerprint
allowed selection mode
priority classification source ref/hash/ordinal
required Human input kind
Task template ref/hash when applicable
privacy/security restrictions
authority revision
issued/revoked/supersedes refs/effective sequence
current_projection_on_invalidation
```

Current descriptor contains mostly:

```text
parameter_schema
static priority ordinals
requires_human_input bool
```

and does not verify canonical roadmap/template source authority.

### required correction

Implement the accepted exact V1 descriptor/ActionRef authority shape or exact semantically equivalent durable
shape.

Do not accept an arbitrary string called `CANONICAL_ROADMAP_ITEM` as canonical roadmap authority.

If no predecessor owner/hash/anchor exists for a source kind:

```text
do not enroll that source kind
or STOP with IMPLEMENTATION_BASELINE_GAP
```

---

# 10. FINDING H — OPERATIONAL_RECOVERY is not bound to actual P1-4/P1-7 operational facts

Current `select()` for `OPERATIONAL_RECOVERY` receives no WorkRun/blocker/failure authority refs.

It merely forbids memory refs and ranks current enrolled descriptors by static descriptor ordinals.

Therefore an operational recovery action may be selected for a project that has no current:

```text
BLOCKED
REWORK_REQUIRED
REJECTED
FAILED
```

authority fact.

Accepted design requires current source-domain operational facts and authoritative priority classification.

### required correction

`OPERATIONAL_RECOVERY` evaluation must consume and verify exact source-domain facts, such as accepted design
equivalents of:

```text
current WorkRun state/version
exact blocker/failure/rework refs
relevant current P1-7 Judgment refs
```

and derive authoritative priority classification from those owner refs + selection policy.

No matching operational authority:

```text
→ no recovery selection
```

Static descriptor rank alone is not blocker/failure authority.

---

# 11. FINDING I — Human input binding accepts unrelated historical Judgment

Current Human-required NextAction check is effectively:

```text
historical Judgment exists
work_run_id != ""
serialized_ref matches supplied ref
```

It does not bind the Judgment to:

```text
same project
same TaskContract/scope
required Human input kind
the selected descriptor/action
the relevant current operational/Cycle context
```

An unrelated historical Judgment can therefore satisfy a Human-required descriptor.

### required correction

Implement the exact accepted Human requirement enum/contract:

```text
NONE
BEFORE_SELECTION
AFTER_TASK_ISSUANCE_P1_7
```

For `BEFORE_SELECTION`, verify the exact P1-7 authority required by the descriptor/policy and same
project/task/run/scope/context.

`AFTER_TASK_ISSUANCE_P1_7` must not be treated as pre-selection approval.

Foreign/unrelated Judgment:

```text
→ NEXT_ACTION_HUMAN_INPUT_REQUIRED
```

P1-8 never mints HumanResult/Judgment.

---

# 12. FINDING J — current NextAction invalidation/withdrawal is incomplete

Accepted design requires later policy/descriptor revocation or `WITHDRAW_CURRENT` disposition to append:

```text
NextActionAuthorityEvent
→ current projection becomes non-current
```

while historical selection replay continues to succeed.

Current runtime can reject a stale descriptor for a **new** selection, but `rebuild_projection()` folds only
selection authority events and does not fold owner-policy/descriptor invalidation into current projection
withdrawal.

### required correction

Implement owner-event-driven current withdrawal:

```text
policy/descriptor owner event
→ append NextActionAuthorityEvent with expected project revision
→ current selection withdrawn when contract requires
```

Historical selection remains immutable/replayable.

Add tests for:

```text
selection valid at issuance
descriptor/policy revoked later
historical replay PASS
current projection withdrawn
new stale selection DENY
```

---

# 13. candidate / terminal authority binding cleanup

Current `CycleCandidate.task_contract_fingerprint` is caller supplied, and source review did not find a
verification against an owner-backed TaskContract fingerprint.

Do not let an unverified caller hash become historical TaskContract authority.

Required:

```text
exact predecessor-owned TaskContract identity/hash if one exists
```

or derive only a clearly named deterministic P1-8 binding over owner-verified TaskContract ID/version fields.

If the Human-accepted `TaskContract ref/hash` requirement cannot be satisfied from current predecessor
authority:

```text
STOP
→ IMPLEMENTATION_BASELINE_GAP
```

Do not fabricate authority by hashing caller values.

---

# 14. tests/evidence required by this rework

Add focused tests that were absent from the reviewed candidate.

## Memory

```text
rogue MemoryDeclaration policy owner
→ denied

caller changes subject/applicability/semantic slot
while source/policy derives another value
→ denied

wrong deterministic-pointer category/source tuple
→ denied

source privacy NON_EXPORTABLE
→ cannot become INTERNAL/PUBLIC

policy revoked after admission
→ historical replay PASS
→ current view withdrawn

policy revoked before admission
→ new admission DENY
```

## Cycle

```text
different Cycle IDs + same terminal epoch + same payload
→ one admitted lineage / replay

different Cycle IDs + same terminal epoch + different payload
→ TERMINAL_EPOCH_CONFLICT

fresh concurrent variant of the above

source currentness high-watermark persisted/replayed
concurrent source invalidation
→ deterministic current applicability
```

## NextAction

```text
rogue eligibility/selection policy authority
→ denied

rogue descriptor enrollment
→ denied

descriptor not actually enrolled by selected eligibility policy
→ denied

fake CANONICAL_ROADMAP_ITEM source without exact authority/hash/anchor
→ denied

OPERATIONAL_RECOVERY without actual blocker/failure/rework authority
→ denied

OPERATIONAL_RECOVERY with exact current source-domain authority
→ deterministic selection

foreign-project / foreign-task Human Judgment
→ HUMAN_INPUT_REQUIRED

AFTER_TASK_ISSUANCE_P1_7
→ does not satisfy BEFORE_SELECTION

descriptor/policy revocation
→ historical replay succeeds
→ current projection withdrawn
```

---

# 15. command-center judgment

```text
P1-6 core:
ACCEPTED / CLOSED

P1-6 Durable Evidence Content Extension:
DESIGN + RUNTIME
ACCEPTED / CLOSED

P1-8 Design:
HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-8 Runtime:
HOLD_REWORK_REQUIRED / HUMAN_PENDING

P2:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

No Human P1-8 runtime final review yet.

No runtime commit is authorized.
