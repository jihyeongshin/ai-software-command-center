# AISCC Cycle Record

## meta

- cycle_id: `20260828_0928_aiscc-p1-4-authority-owner-and-consistency-gate-hold-1`
- date: `2026-08-28 09:28 KST`
- primary_semantic_owner: `P1-4 authoritative guard ownership + projection/event mutation gate`
- work_type: `AUTHORITATIVE_STATE_MACHINE_IMPLEMENTATION / REWORK_JUDGMENT`
- execution_mode: `MANUAL_COMMAND_CENTER`
- predecessor_task: `20260828_0928_aiscc-p1-4-explicit-state-machine-kernel-resume-with-direct-canonical-placement-1`
- predecessor_executor_result: `ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING`
- predecessor_base_commit: `1b04e8a0d36fc0400cbeacaf65c56f643f423923`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause:
  - `FUTURE_OWNER_GUARD_AUTHORITY_MINT_BYPASS`
  - `PROJECTION_EVENT_CONSISTENCY_NOT_MUTATION_GATED`
- P1_4_status: `NOT_ACCEPTED`
- P1_5_status: `NOT_STARTED / BLOCKED`
- cycle_record_action: `create`
- source_mirror_sync: `not-required`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260828_0928_aiscc-p1-4-authority-owner-and-consistency-gate-hold-1.cycle.md`

## admitted predecessor evidence

### P1-3 terminal/provenance persistence

Admit:

```text
P1_4_BASE_COMMIT:
1b04e8a0d36fc0400cbeacaf65c56f643f423923

parent:
575fb3c4623a28b8537d15c8b34b838982f96ce2

committed path count:
70

P1-3 accepted candidate:
55 paths

P1-3 accepted aggregate:
4a9f49a70bbe6cc628a9bc9e6612d07b724876beaf3fd0e672b9815343018c4c

post-commit tracked worktree:
clean

post-commit index:
empty

remote mutation:
none
```

The repeated P1-4 preflight transport blockers are now durably closed.

### P1-4 candidate identity

Current uncommitted P1-4 candidate:

```text
path count:
19

aggregate SHA-256:
c5c6177dbf228683def88cd01907dd55db0a479824a7e9a56b7b1b5040067051
```

Exact candidate paths:

```text
alembic.ini
migrations/env.py
migrations/script.py.mako
migrations/versions/20260828_0001_p1_4_workflow_kernel.py
pyproject.toml
src/aiscc/persistence/__init__.py
src/aiscc/persistence/database.py
src/aiscc/persistence/models.py
src/aiscc/persistence/repository.py
src/aiscc/workflow/__init__.py
src/aiscc/workflow/evaluator.py
src/aiscc/workflow/guards.py
src/aiscc/workflow/kernel.py
src/aiscc/workflow/matrix.py
src/aiscc/workflow/models.py
src/aiscc/workflow/ports.py
tests/integration/workflow/test_postgres_kernel.py
tests/unit/workflow/test_state_machine.py
uv.lock
```

### implementation strengths retained

Admit candidate strengths:

```text
exact 9 WorkflowState values
exact 22 transition pairs
terminal outgoing denial
exact Judgment target mapping
no hidden reroute

PostgreSQL authoritative WorkRun/state_version
request/evaluation/decision provenance
append-only history triggers
per-run/per-request advisory locks
row lock + CAS mutation
same-transaction provenance/projection mutation
duplicate request fingerprint/idempotency
restart-durable projection/history
deterministic consistency checker
```

### static/runtime evidence retained

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

P1-4 PostgreSQL integration:
8 PASS

unit + integration:
43 PASS

PostgreSQL migration:
PASS

same-version concurrency:
PASS

duplicate request idempotency:
PASS

controlled transaction rollback:
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

These remain valid for unchanged portions of the candidate.

## HOLD A — P1-4 can mint P1-6/P1-7-owned guard authority

Current production source exposes:

```text
TrustedGuardAuthority.issue(...)
```

for every `GuardId` except `G_CURRENT`.

Therefore the P1-4-owned issuer can directly create satisfied facts for, among others:

```text
G_EVIDENCE

G_HUMAN_REQUIRED
G_HUMAN_NOT_REQUIRED
G_NO_PENDING_HUMAN_GATE
G_SUSPENDED_HUMAN_GATE
G_RESUMABLE_HUMAN_GATE
G_HUMAN_APPROVED
G_HUMAN_REWORK
G_HUMAN_REJECTED

G_JUDGMENT_ACCEPTED
G_JUDGMENT_REJECTED
G_JUDGMENT_REWORK
```

The issuer is also reachable through:

```text
WorkflowKernel.guard_authority
```

and is exported from:

```text
aiscc.workflow
```

The current issuer validates only:

```text
issuer token
task contract ID/version
work_run_id
state_version
```

It does not validate the semantic owner of the guard, and `authority_ref` is caller-selected opaque
text.

The current tests themselves demonstrate that any required guard can be minted by the same generic
authority fixture.

This means:

```text
caller boolean != authoritative guard fact
```

is satisfied, but the stronger accepted boundary is not:

```text
P1-4 transition authority
!= P1-6 evidence authority

P1-4 transition authority
!= P1-7 Human/Judgment authority
```

A private Python token is not semantic owner separation when P1-4 itself owns and exposes the minting
object.

### required correction

P1-4 production code MUST NOT be able to mint future-owner guard facts.

At minimum:

1. remove the public/external minting handle from `WorkflowKernel`;
2. do not export a generic production issuer that can create every GuardId;
3. encode guard-owner provenance in the trusted fact contract;
4. validate `guard_id × semantic owner`;
5. P1-6-owned evidence guards and P1-7-owned Human/Judgment guards require an injected external
   trusted authority/verifier boundary;
6. while P1-6/P1-7 are not implemented, production use of those future-owner guards is fail-closed
   unless an injected authority implementation provides an owner-bound fact;
7. tests may use a test-only authority implementation/factory to exercise the matrix;
8. test-only authority MUST NOT be exported/wired as production authority.

Do NOT implement P1-6 evidence admission or P1-7 Human/Judgment logic.

The rework is about owner-bound authority plumbing only.

### opaque ref boundary

Raw `evidence_refs`, `human_result_refs`, and `judgment_refs` remain non-authoritative by themselves.

Where a future-owner fact represents one of these artifact classes, the fact must bind to the exact
opaque reference(s) it attests to or otherwise provide an equivalent immutable owner-bound reference
identity.

Required invariant:

```text
request ref string alone
→ no authority

P1-4 generic issuer
→ cannot bless future-owner ref

owner-bound future authority assertion
→ may satisfy exact matching future-owner guard
```

## HOLD B — consistency checker is not on the authoritative mutation path

Current flow:

```text
WorkflowKernel.request_transition(...)
→ PostgresTransitionRepository.decide(...)
→ read current WorkRun
→ evaluate
→ persist provenance
→ mutate projection
```

`decide()` does NOT call or otherwise enforce projection/event consistency before a new mutation.

`verify_consistency()` exists as a separate opt-in method.

The current mismatch test proves:

```text
manual projection corruption
→ verify_consistency() raises AuthorityConflictError
```

but also proves that the corrupted projection remains loadable:

```text
kernel.load(...)
→ corrupted WorkRun still returned
```

Nothing in `request_transition()` prevents a subsequent caller from observing that corrupted
state/version and submitting a matching new request.

Therefore:

```text
consistency checker exists
!= authoritative mutation fail-closed gate
```

### required correction

Before evaluating/persisting any NEW transition request, under the same run serialization /
transaction boundary:

```text
current durable projection
+
append-only admitted lineage
→ consistency verification
```

Required:

```text
projection/event mismatch
→ AuthorityConflictError / RECOVERY_REQUIRED
→ no new request row
→ no evaluation row
→ no decision row
→ no state/version mutation
```

No automatic repair.

A same-ID immutable duplicate lookup may return its already-existing historical decision without
creating new authority, but no fresh mutation path may proceed on an inconsistent run.

Use an in-session/internal consistency function so the check and mutation share the authoritative
transaction/lock context.

Do not rely on a caller remembering to invoke `verify_consistency()` first.

## source/report overclaim note

The predecessor report says opaque evidence/Human/Judgment/blocker/rework/execution references are
recorded.

The durable request model directly records:

```text
evidence_refs
human_result_refs
judgment_refs
parent_request_id
```

It does not directly expose dedicated blocker/rework/execution reference fields.

This is not independently promoted to a blocker in this Cycle because guard observations retain
authority provenance and P1-4 must not implement future domain objects merely for completeness.

The next report must describe exactly what is persisted and avoid broadening that claim.

## Command Center judgment

```text
P1-3 terminal Git:
PASS / CLOSED

P1-4 transition matrix:
PASS / RETAIN

P1-4 PostgreSQL transaction/concurrency/idempotency:
PASS / RETAIN

P1-4 restart/append-only proof:
PASS / RETAIN

future-owner guard separation:
HOLD_REWORK_REQUIRED

projection/event mutation gate:
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
issuer-token-backed fact
!= semantic owner authorization

no public HTTP mutation route
!= no in-process authority bypass

opaque ref recorded
!= admitted owner authority

verify_consistency API
!= mutation-path fail-closed enforcement

consistency test called explicitly
!= every fresh transition is consistency gated

43 tests PASS
!= missing governance invariant accepted
```

## preservation

Preserve exact commit:

- `1b04e8a0d36fc0400cbeacaf65c56f643f423923`

Preserve exact paths:

- `.aiassistant/tasks/done/20260828_0928_aiscc-p1-4-explicit-state-machine-kernel-resume-with-direct-canonical-placement-1.md`
- `.aiassistant/records/aiscc/cycles/20260828_0928_aiscc-p1-4-authority-owner-and-consistency-gate-hold-1.cycle.md`
- all exact 19 current P1-4 candidate paths pending rework judgment
- all accepted P1-3 terminal implementation/provenance already contained in the base commit

Preserve current P1-4 candidate identity as historical evidence:

```text
19 paths
c5c6177dbf228683def88cd01907dd55db0a479824a7e9a56b7b1b5040067051
```

## next action

```text
P1-4 narrow rework:
1. persist predecessor done Task + this HOLD Cycle
2. keep current 19-path candidate in place
3. close future-owner guard mint bypass
4. put consistency verification on every fresh mutation path
5. re-run static/unit/PostgreSQL evidence
6. retain no P1-5/P1-6/P1-7/P1-8 implementation
```
