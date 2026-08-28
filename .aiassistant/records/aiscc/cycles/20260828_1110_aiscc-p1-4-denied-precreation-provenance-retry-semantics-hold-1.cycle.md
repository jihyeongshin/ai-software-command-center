# AISCC Cycle Record

## meta

- cycle_id: `20260828_1110_aiscc-p1-4-denied-precreation-provenance-retry-semantics-hold-1`
- date: `2026-08-28 11:10 KST`
- primary_semantic_owner: `P1-4 NONE-state denied provenance / fresh retry consistency semantics`
- work_type: `AUTHORITATIVE_STATE_MACHINE_IMPLEMENTATION / REWORK_JUDGMENT`
- execution_mode: `MANUAL_COMMAND_CENTER`
- predecessor_task: `20260828_0928_aiscc-p1-4-owner-bound-guards-and-consistency-gated-mutation-rework-1`
- predecessor_executor_result: `ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING`
- predecessor_base_commit: `325f876234c580d6f61d650501ed3250d152970a`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause: `DENIED_PRECREATION_PROVENANCE_POISONS_FRESH_NONE_TO_READY_RETRY`
- P1_4_status: `NOT_ACCEPTED`
- P1_5_status: `NOT_STARTED / BLOCKED`
- cycle_record_action: `create`
- source_mirror_sync: `not-required`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260828_1110_aiscc-p1-4-denied-precreation-provenance-retry-semantics-hold-1.cycle.md`

## admitted predecessor evidence

### provenance

Admit:

```text
P1_4_AUTHORITY_REWORK_BASE_COMMIT:
325f876234c580d6f61d650501ed3250d152970a

parent:
1b04e8a0d36fc0400cbeacaf65c56f643f423923

exact two-path provenance commit:
PASS

remote/history rewrite:
none
```

### candidate identity

Current P1-4 candidate remains exactly:

```text
path count:
19

aggregate SHA-256:
56a92e856e5f04faab68465b564afd90dbae83be87f813b642bdb2fd567623a5
```

Exactly eight files changed from the predecessor candidate.

### previous HOLD A — future-owner authority separation

Admit as corrected:

```text
GUARD_OWNER_POLICY:
complete / exact

P1_4GuardAuthority:
P1_4_SYSTEM guards only

P1-6 evidence guards:
external owner verifier required

P1-7 Human guards:
external owner verifier required

P1-7 Judgment guards:
external owner verifier required

WorkflowKernel:
no guard-authority / mint handle

raw evidence/Human/Judgment refs:
non-authoritative

owner mismatch / fake fact / absent verifier:
fail closed

exact owner-bound fact + exact refs:
may satisfy mapped guard
```

No P1-6/P1-7 domain admission logic was implemented.

### previous HOLD B — consistency gate on fresh mutation

Admit as structurally corrected:

```text
run advisory lock
→ request advisory lock
→ immutable duplicate lookup
→ WorkRun row lock
→ in-session consistency verification
→ evaluation/provenance
→ CAS projection mutation
→ transaction commit
```

A fresh request cannot bypass projection/admitted-lineage consistency verification.

Corrupted projection and missing-projection-with-admitted-history proof both fail before new
request/evaluation/decision provenance.

### retained verification

Admit:

```text
uv sync --frozen --all-groups:
PASS

uv build:
PASS

Ruff:
PASS

mypy --strict:
PASS

complete unit + integration:
66 PASS

P1-4 PostgreSQL integration:
9 PASS

migration:
PASS

same-version concurrency:
PASS

duplicate request idempotency:
PASS

atomic rollback:
PASS

restart durability:
PASS

append-only denied provenance:
PASS

final task-owned Docker container residue:
0

final task-owned Docker network residue:
0
```

## HOLD — denied pre-creation provenance is treated as authority corruption

Current repository consistency logic does this when no `WorkRun` projection exists:

```text
SELECT any transition_request for work_run_id

if any request exists
→ AuthorityConflictError(
    "authoritative WorkRun projection is missing while transition history exists"
  )
```

This check does not distinguish:

```text
ADMITTED history
```

from:

```text
complete DENIED-only provenance
```

### concrete failing semantic sequence

A first request may legitimately be denied before `WorkRun` creation.

Example A:

```text
NONE/v0 → READY
missing required guard
→ DENIED(MISSING_GUARD)
→ WorkRun remains absent
→ authoritative state remains NONE/v0
```

Example B:

```text
NONE/v0 → invalid target
→ DENIED(INVALID_TRANSITION)
→ WorkRun remains absent
→ authoritative state remains NONE/v0
```

A corrected fresh request should then be possible:

```text
new transition_request_id
same run identity
NONE/v0 → READY
all required trusted guards present
```

But current `_verify_consistency_in_session()` sees the prior denied `transition_request` and raises
`AuthorityConflictError` before evaluation.

Therefore one denial creates a hidden permanent behavioral state:

```text
DENIED
→ state/version unchanged
BUT
→ future NONE → READY impossible
```

That violates the accepted non-substitution/state invariant:

```text
DENIED TransitionDecision
→ no authoritative WorkflowState mutation
→ fresh corrected request remains possible from the same authoritative state/version
```

A denied transition must not silently act like an unmodeled terminal WorkflowState.

## required correction

For:

```text
projection_row is None
```

the consistency gate must distinguish admitted authority from denied audit provenance.

### allowed consistent pre-creation history

The following is consistent with authoritative `NONE/v0`:

```text
no WorkRun projection
+
zero admitted decisions for the run
+
all existing transition attempts are structurally complete
(request + evaluation + DENIED decision)
+
no partial/orphaned authority rows
```

In that case a NEW fresh request may continue evaluation from:

```text
authoritative_state:
NONE

authoritative_state_version:
0
```

### corruption / conflict

Raise `AuthorityConflictError` before any new provenance if:

```text
no WorkRun projection
+
one or more ADMITTED decisions exist
```

or if existing run history is structurally incomplete/inconsistent:

```text
request without evaluation
evaluation without decision
decision/evaluation/request identity mismatch
unexpected duplicate structural ownership
```

Do not auto-repair.

### run identity isolation

Denied-only pre-creation history must not permit a later caller to reuse the same `work_run_id` for a
different authoritative run identity.

Before allowing fresh `NONE/v0 → READY`, verify all prior denied attempts for that `work_run_id`
match the incoming immutable run identity at minimum:

```text
project_id
task_contract_id
task_contract_version
runtime_mode
```

If they conflict:

```text
AuthorityConflictError
→ no new provenance
```

Requester identity/type does not need to be identical merely to allow a corrected system retry.

## required proof

### DENIED_PRECREATION_RETRY

Case 1:

```text
fresh run ID
NONE/v0 → READY with no facts
→ DENIED(MISSING_GUARD)
→ projection absent

new request ID
same run identity
NONE/v0 → READY with valid guards
→ ADMITTED
→ READY/v1

history:
first DENIED preserved
second ADMITTED preserved
```

Case 2:

```text
fresh run ID
NONE/v0 → invalid target
→ DENIED(INVALID_TRANSITION)

new request ID
same run identity
NONE/v0 → READY with valid guards
→ ADMITTED READY/v1
```

### MULTIPLE_DENIED_PRECREATION_RETRY

Several complete denied attempts may exist before the valid fresh create.

Required:

```text
all denied provenance preserved
valid fresh create succeeds exactly once
state_version == 1
```

### DENIED_PRECREATION_IDENTITY_CONFLICT

Create denied-only pre-creation provenance under identity A.

Submit fresh `NONE/v0 → READY` under same `work_run_id` but identity B, changing one of:

```text
project_id
task_contract_id
task_contract_version
runtime_mode
```

Required:

```text
AuthorityConflictError
no new request/evaluation/decision
projection remains absent
```

### PARTIAL_HISTORY_FAIL_CLOSED

Use isolated test-only SQL/transaction to create structurally incomplete pre-creation provenance if
possible.

Required:

```text
fresh mutation
→ AuthorityConflictError
→ no auto repair
```

Do not weaken append-only production constraints.

## Command Center judgment

```text
P1-4 owner-bound guard authority:
PASS / RETAIN

P1-4 fresh mutation consistency gate:
PASS / RETAIN

P1-4 PostgreSQL concurrency/idempotency/atomicity:
PASS / RETAIN

P1-4 denied pre-creation retry semantics:
HOLD_REWORK_REQUIRED

P1-4:
NOT ACCEPTED

Human final review:
DEFERRED

P1-5:
NOT_STARTED / BLOCKED
```

## proof non-substitution

```text
DENIED provenance exists
!= WorkRun projection must exist

any transition history
!= admitted authority history

audit provenance
!= hidden WorkflowState mutation

no projection + denied-only history
!= projection corruption

same work_run_id
!= permission to cross project/task/runtime identity
```

## preservation

Preserve exact commits:

- `1b04e8a0d36fc0400cbeacaf65c56f643f423923`
- `325f876234c580d6f61d650501ed3250d152970a`

Preserve exact paths:

- `.aiassistant/tasks/done/20260828_0928_aiscc-p1-4-owner-bound-guards-and-consistency-gated-mutation-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260828_1110_aiscc-p1-4-denied-precreation-provenance-retry-semantics-hold-1.cycle.md`
- all exact 19 current P1-4 candidate paths

Preserve current candidate identity as historical evidence:

```text
19 paths
56a92e856e5f04faab68465b564afd90dbae83be87f813b642bdb2fd567623a5
```

## next action

```text
P1-4 narrow repository semantics rework:
1. persist predecessor done Task + this HOLD Cycle
2. retain current owner-bound guard and consistency-gate work
3. distinguish denied-only pre-creation provenance from admitted-history corruption
4. preserve run identity isolation
5. add PostgreSQL proof
6. re-run all P1-4 regression evidence
```

Do not execute P1-5.
