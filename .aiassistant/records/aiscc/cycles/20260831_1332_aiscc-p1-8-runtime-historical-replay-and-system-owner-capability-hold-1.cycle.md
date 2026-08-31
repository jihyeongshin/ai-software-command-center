# AISCC Cycle Record

## meta

- cycle_id: `20260831_1332_aiscc-p1-8-runtime-historical-replay-and-system-owner-capability-hold-1`
- date: `2026-08-31T13:32:00+09:00`
- phase: `P1-8 Project Memory and Cycle Admission Runtime`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1_8_PROJECT_MEMORY_CYCLE`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause: `HISTORICAL_REPLAY_AND_SYSTEM_OWNER_CAPABILITY_GAPS`
- reviewed_head: `f4614198c2745944f7ec02639a45b0315bbc903d`
- predecessor_runtime_path_count: `18`
- predecessor_runtime_aggregate_sha256: `37c7860008bdf04ce75e4b1e01c98185b1afdc5da73e67328bbe35670eceaf92`
- reviewed_runtime_path_count: `19`
- reviewed_runtime_aggregate_sha256: `84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42`

---

# 1. independent candidate verification

Export bytes were independently recomputed.

```text
runtime path count:
19

19 / 19 per-file SHA:
MATCH

runtime aggregate:
84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42
MATCH

HEAD:
f4614198c2745944f7ec02639a45b0315bbc903d

Git add/commit/push:
none
```

Submitted verification:

```text
complete repository:
215 / 215 PASS

P1-4 PostgreSQL:
18 / 18 PASS

P1-6:
7 / 7 PASS

P1-7:
2 / 2 PASS

P1-8:
4 / 4 PASS

PostgreSQL:
17.6

Alembic:
20260831_0007

ruff:
PASS

mypy:
76 source files PASS
```

This HOLD is not caused by export drift or test failure.

---

# 2. 1143 findings that are CLOSED

The rework correctly closes substantial portions of the prior HOLD.

```text
caller lineage claims
→ equality-only; owner-derived atoms used for persistence

memory privacy
→ source/policy most-restrictive classification

Memory policy durable payload
→ category source contracts added

terminal epoch
→ durable key + unique DB constraint

different Cycle ID / same terminal epoch
→ replay or TERMINAL_EPOCH_CONFLICT

TaskContract caller hash
→ replaced by owner-verified P1-8 task-scope equality binding

source/policy admission high-watermarks
→ durably persisted

NextAction ActionRef
→ eligibility-policy/action/descriptor fingerprint binding

eligibility-policy → exact descriptor enrollment
→ durably persisted

OPERATIONAL_RECOVERY
→ current P1-4 WorkRun/transition fact required

Human input enum
→ NONE / BEFORE_SELECTION / AFTER_TASK_ISSUANCE_P1_7

NextAction policy/descriptor invalidation
→ append-only current withdrawal

0006 historical migration
→ preserved
0007 additive migration
→ added
```

These should not be redesigned.

---

# 3. FINDING A — historical Cycle replay does not rederive stored Memory from the historical source

The Human-accepted design section 10.2 requires historical replay to:

```text
original policy payload/as-of validity
+ stored historical source provenance
→ reconstruct expected content
→ recompute MCF_V1
→ recompute MemoryLineageKey
→ compare with stored ProjectMemoryEntry/CycleMemoryReference
```

Current `_verify_cycle_in_session()` instead:

```text
recomputes MemoryLineageKey from stored declaration claims

recomputes content fingerprint from stored ProjectMemoryEntry.normalized_content

verifies the P1-6 historical body exists/integrity passes

but does not re-run derive_memory_declaration() from that historical source body/policy
```

For structured sources the result returned by:

```text
verify_historical_admitted_evidence_with_content(...)
```

is not used to reconstruct the stored memory object during replay.

Therefore the verifier proves:

```text
stored content is internally self-consistent
+ source exists
```

but not:

```text
stored content actually equals the policy-derived historical source content
```

Likewise deterministic pointer entries are not rederived from exact P1-4/P1-6/P1-7/canonical source authority
during replay.

Required correction:

```text
for every declaration ordinal:
  resolve historical policy version/as-of validity
  reconstruct exact historical VerifiedMemorySource
  derive_memory_declaration(...)
  recompute owner-derived subject/applicability/semantic slot/privacy/content/MCF
  compare exact stored entry or CycleMemoryReference binding
```

Current policy currentness must not be required.

Later source/policy staleness remains separate from historical identity.

---

# 4. FINDING B — CycleMemoryReference replay proves only content fingerprint, not exact source/policy derivation

Current historical replay for a `CycleMemoryReference` mainly verifies:

```text
reference exists
reference.content_fingerprint == declaration.claimed_content_fingerprint
```

It does not prove the new Cycle's declaration independently derives that same content from its own exact
historical source/policy authority.

This allows the same-content reuse path to have weaker authority verification than a newly materialized entry.

Required invariant:

```text
same-content reuse
!= skip MemoryDeclaration source authority verification
```

The replay must first rederive the declaration exactly, then prove:

```text
derived MCF_V1 == referenced current/historical entry content_fingerprint
lineage == referenced entry lineage
policy/source/category contract == exact declaration authority
```

---

# 5. FINDING C — delayed same-content admission can leave a stale CURRENT tip

In `_persist_memory()` the same-content branch returns early after creating `CycleMemoryReference`.

It does not reconcile the just-observed:

```text
source_current
source event high-watermark
policy event high-watermark
```

with the existing current tip.

Scenario:

```text
existing entry E is CURRENT
same source is revoked in P1-6
ProjectMemory invalidation projection has not yet been applied
new accepted Cycle with same content arrives

Cycle admission observes source_current = false
but same-content branch only writes CycleMemoryReference
and leaves E CURRENT
```

That violates:

```text
delayed admission of already non-current source
→ zero temporary CURRENT exposure
```

Required correction:

- if the referenced entry's authority source/policy is already non-current at the admission high-watermark,
  append the required ProjectMemoryAuthorityEvent and withdraw the current tip in the same transaction;
- if same content is backed by a *different still-current* existing source authority, do not incorrectly revoke
  that independent source;
- store enough `CycleMemoryReference` provenance to distinguish these cases.

Add exact delayed same-content + unapplied source-owner event tests.

---

# 6. FINDING D — the real System owner capability is publicly retrievable and callable

The rework adds opaque seals, but then exposes the actual owner objects through:

```text
default_memory_policy_authority()
default_next_action_policy_authority()
```

and package `__init__.py` uses wildcard exports.

A caller with ordinary module access can therefore obtain the exact recognized owner object and call:

```text
memory authority:
issue_v1(...)
invalidate(...)

NextAction authority:
issue_policy_catalog_v1(...)
invalidate(...)
```

This is not the same as a rogue *foreign* authority instance; it is direct access to the real authority.

The accepted boundary is:

```text
caller/configuration object
!= System owner issuance authority
```

and the prior P1-6 durable-content solution intentionally bound owner capabilities through bootstrap/repository
composition rather than exposing a default global writer/access authority.

Required correction:

- no public/default getter may return the live issuance/invalidation capability;
- bootstrap/composition creates the owner capability and injects only the minimum repository/service interface;
- request/caller code can submit proposals or owner-authenticated commands, but cannot call the raw mint/invalidate
  methods;
- repository recognizes only its bootstrap-bound capability;
- tests must prove that importing the public P1-8 package does not expose a path to mint/enroll/revoke a recognized
  policy/descriptor/event.

An internal test factory may exist under test-only composition, but it must not be production authority API.

---

# 7. FINDING E — POLICY_ACTION_CATALOG contents are caller-selected at issuance time

Even when the exact singleton owner is used, current:

```text
issue_policy_catalog_v1(catalog_id, actions, now)
```

accepts arbitrary caller/configuration `actions`.

Those inputs directly determine:

```text
action IDs
allowed modes
parameter schema
priority rank
critical/dependency ordinals
Human requirement
project/scope restrictions
security/privacy restrictions
```

and the System authority then seals them.

That is equivalent to:

```text
caller defines descriptor
→ System function blesses it
```

which violates accepted design section 17.2:

```text
POLICY_ACTION_CATALOG
→ P1-8 policy authority issues the immutable catalog entry
→ caller cannot enroll/define descriptor
```

Required correction:

Choose one exact owner-backed V1 catalog source:

```text
A. fixed canonical P1-8 policy catalog payload embedded/versioned under the owner authority

or

B. a separately owner-issued canonical PolicyActionCatalog object/ref/fingerprint that the P1-8 authority
   verifies before descriptor issuance
```

Caller proposals must never supply descriptor-definition fields.

If no canonical catalog authority exists in the current predecessor baseline:

```text
STOP
→ IMPLEMENTATION_BASELINE_GAP
```

Do not solve this by treating arbitrary bootstrap configuration as authority.

---

# 8. FINDING F — accepted Memory category coverage remains incomplete without the required STOP

The accepted design exact V1 table defines:

```text
DECISION
INVARIANT_POINTER
CONSTRAINT_POINTER
LESSON = NOT_SUPPORTED
BLOCKER_RESOLUTION
PROVENANCE_POINTER
NEXT_ACTION_CONTEXT
```

Current canonical Memory policy source contracts cover:

```text
DECISION
NEXT_ACTION_CONTEXT
PROVENANCE_POINTER
INVARIANT_POINTER
```

but omit exact contracts for:

```text
CONSTRAINT_POINTER
BLOCKER_RESOLUTION
```

while `CATEGORY_MODES` still advertises both as `DETERMINISTIC_POINTER`.

The 1143 Task explicitly required:

```text
if required predecessor owner/source authority does not exist
→ STOP / IMPLEMENTATION_BASELINE_GAP
```

The Executor report acknowledges unavailable P1-4 blocker/external owner sources but continued and returned a
runtime candidate.

Required correction:

- either implement the exact accepted owner/source contracts without fabricating authority;
- or STOP with the smallest missing predecessor owner contract.

Do not silently leave a category mode supported while its exact source authority contract is absent.

---

# 9. FINDING G — historical NextAction replay does not independently recompute descriptor authority

Current historical replay verifies:

```text
descriptor.fingerprint == selection payload descriptor_fingerprint
enrollment exists
ENROLLED event exists
```

but does not independently recompute:

```text
canonical_hash(descriptor immutable payload)
== descriptor.fingerprint
```

unless the descriptor happens to still exist in the repository's *current configured* descriptor map.

Historical replay must not depend on current catalog configuration.

It also does not require the ENROLLED owner event payload to bind the exact descriptor fingerprint.

Required correction:

```text
parse durable historical descriptor payload by its exact schema
recompute descriptor fingerprint independently
verify source-authority binding
verify ActionRef
verify enrollment row
verify ENROLLED owner-event payload/fingerprint
verify all as-of issuance
```

This must work even when the original descriptor is no longer in the current configured catalog.

---

# 10. FINDING H — CYCLE_DERIVED historical replay does not prove memory was CURRENT at original selection

New selection correctly requires current ProjectMemory.

Historical replay currently checks only that each stored memory entry:

```text
exists
belongs to the same project
```

It does not reconstruct the memory applicability event history **as of NextActionSelection issuance**.

The accepted design requires CYCLE_DERIVED inputs to have been CURRENT at original selection time while allowing
later revocation/supersession without corrupting historical selection replay.

Required correction:

Persist/bind an exact memory-applicability observation high-watermark or equivalent immutable evaluation input.

Historical replay must prove:

```text
entry was CURRENT at selection issuance
same project/scope
exact authority revision/event boundary
```

Then later events may make it non-current without invalidating historical selection identity.

---

# 11. FINDING I — OPERATIONAL_RECOVERY verifies existence but does not derive authoritative priority class from the recovery fact

Current `_require_operational_recovery()` correctly proves:

```text
current WorkRun is BLOCKED/FAILED/REWORK_REQUIRED
exact P1-4 transition fact exists
```

but `ranking_key()` still uses descriptor-static:

```text
priority_rank
dependency_ordinal
critical_path_ordinal
descriptor_policy_ordinal
```

The recovery fact is only a gate/ref list; it does not participate in the authoritative priority classification.

Accepted design section 17.4 requires priority facts to derive from:

```text
selection policy mapping
+ current P1-4 blocker/failure/rework authority
+ applicable P1-7 Judgment/baseline facts
```

Proposal claims remain ignored.

Required correction:

- selection policy owns an exact deterministic mapping from verified operational fact classes/reasons to
  authoritative priority class/rank;
- NextActionEvaluation stores that resolved priority fact/ref/reason trace;
- ranking uses the resolved authoritative priority rank, not a caller-originated catalog number alone.

---

# 12. FINDING J — BEFORE_SELECTION Human binding can be weakened by an empty descriptor scope

Current Human check always requires:

```text
same project
Human-owned Judgment
Human gate/result present
```

but task/run/state/target equality is enforced only if those optional strings exist in
`descriptor.scope_restrictions`.

Because current catalog issuance accepts caller-specified descriptor definitions, a descriptor can omit those
restrictions and then a different Human Judgment from the same project can satisfy `BEFORE_SELECTION`.

Required correction:

For `BEFORE_SELECTION`, derive the required context from the actual selection authority:

- `OPERATIONAL_RECOVERY`: exact operational WorkRun/task/state/version/transition context;
- `CYCLE_DERIVED`: exact source Cycle/ProjectMemory task/run/scope context, with an explicit accepted rule for
  multiple memory refs.

Descriptor scope can narrow the context but cannot remove this mandatory binding.

`AFTER_TASK_ISSUANCE_P1_7` remains post-issuance only.

---

# 13. command-center judgment

```text
P1-6 core:
ACCEPTED / CLOSED

P1-6 Durable Evidence Content Extension:
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
