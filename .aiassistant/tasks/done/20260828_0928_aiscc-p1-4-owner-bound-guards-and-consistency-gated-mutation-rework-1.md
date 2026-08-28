# 작업지시서: P1-4 Owner-Bound Guards and Consistency-Gated Mutation Rework

## meta

- task_id: `20260828_0928_aiscc-p1-4-owner-bound-guards-and-consistency-gated-mutation-rework-1`
- created_at: `2026-08-28 09:28 KST`
- phase: `P1-4 — Explicit State Machine Kernel Implementation`
- work_type: `AUTHORITATIVE_STATE_MACHINE_IMPLEMENTATION_REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `future-owner guard separation + projection/event fail-closed mutation gate`
- predecessor_task: `20260828_0928_aiscc-p1-4-explicit-state-machine-kernel-resume-with-direct-canonical-placement-1`
- predecessor_result: `ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING`
- command_center_result: `HOLD_REWORK_REQUIRED`
- predecessor_HEAD: `1b04e8a0d36fc0400cbeacaf65c56f643f423923`
- predecessor_candidate_path_count: `19`
- predecessor_candidate_aggregate_sha256: `c5c6177dbf228683def88cd01907dd55db0a479824a7e9a56b7b1b5040067051`
- P1_4_status_before: `HOLD_REWORK_REQUIRED`
- P1_5_status: `NOT_STARTED / BLOCKED`

---

# 0. sole execution contract

This is a narrow P1-4 rework.

Retain the predecessor candidate unless directly conflicting:

```text
exact 9 WorkflowState values
exact 22 transition pairs
terminal denial
Judgment target mapping
PostgreSQL WorkRun/state_version
append-only request/evaluation/decision provenance
advisory-lock + row-lock + CAS concurrency
same-request idempotency
atomic transaction
restart durability
deterministic reconstruction
```

Rework only:

1. semantic owner separation for trusted guards;
2. automatic projection/event consistency gating for every fresh authoritative mutation.

Do not redesign P1-4.

---

# Stage 0 — persist predecessor done Task + HOLD Cycle

## expected repository

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

HEAD:
1b04e8a0d36fc0400cbeacaf65c56f643f423923
```

If HEAD differs:

```text
STOP
→ BLOCKED_PREDECESSOR_HEAD_DRIFT
```

## expected uncommitted P1-4 candidate

Before Git index mutation verify:

```text
candidate path count:
19

aggregate SHA-256:
c5c6177dbf228683def88cd01907dd55db0a479824a7e9a56b7b1b5040067051
```

Exact candidate paths are the 19 paths recorded in the HOLD Cycle.

Mismatch:

```text
STOP
→ BLOCKED_P1_4_CANDIDATE_DRIFT
```

Do not discard/revert the candidate.

## allowed Stage 0 provenance paths

Exactly:

```text
.aiassistant/tasks/done/20260828_0928_aiscc-p1-4-explicit-state-machine-kernel-resume-with-direct-canonical-placement-1.md

.aiassistant/records/aiscc/cycles/20260828_0928_aiscc-p1-4-authority-owner-and-consistency-gate-hold-1.cycle.md
```

Current 19 candidate paths MUST NOT be staged.

Unexpected tracked provenance/product path:

```text
STOP
→ BLOCKED_P1_4_REWORK_PROVENANCE_COLLISION
```

## exactly one local provenance commit

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
docs: record P1-4 authority and consistency hold

Persist the P1-4 review that retained the PostgreSQL state-machine
candidate but found future-owner guard minting and a missing
projection/event consistency gate on fresh authoritative mutations.

Keep P1-5 blocked until these governance boundaries are closed.
```

Use LF-safe UTF-8 message file and `git commit -F`.

After commit:

```text
P1_4_AUTHORITY_REWORK_BASE_COMMIT=<full new hash>
```

Verify:

- parent == `1b04e8a0d36fc0400cbeacaf65c56f643f423923`;
- exact provenance paths only;
- exact multiline message;
- index empty;
- no remote operation.

After this commit:

```text
git add / commit / push
→ FORBIDDEN
```

---

# Stage 1 — future-owner guard authority separation

## defect

Current production `TrustedGuardAuthority` can mint every guard except `G_CURRENT`.

Current `WorkflowKernel` exposes that issuer.

That allows P1-4 code to manufacture guards semantically owned by future P1-6/P1-7.

## required invariant

```text
P1-4 TransitionDecision authority
!= P1-6 Evidence authority

P1-4 TransitionDecision authority
!= P1-7 Human/Judgment authority
```

### production guard contract

Introduce an explicit semantic owner for trusted guard facts, or equivalent immutable authority
classification.

At minimum distinguish:

```text
P1_4_SYSTEM
P1_6_EVIDENCE
P1_7_HUMAN
P1_7_JUDGMENT
```

Names may differ.

Encode an exact guard-to-owner policy.

Required examples:

```text
G_CURRENT
→ P1-4 internal only

G_EVIDENCE
→ P1-6_EVIDENCE

G_HUMAN_APPROVED
G_HUMAN_REWORK
G_HUMAN_REJECTED
and Human-gate projection guards
→ P1-7_HUMAN

G_JUDGMENT_ACCEPTED
G_JUDGMENT_REJECTED
G_JUDGMENT_REWORK
→ P1-7_JUDGMENT
```

For other guards, preserve the accepted semantic owner documented by the P1-1/P1-4 contract.
Do not invent P1-6/P1-7 implementation logic.

### issuer restrictions

Production P1-4 code must not expose a generic issuer that can mint all owner classes.

Required:

- `WorkflowKernel` exposes no guard-minting authority handle;
- package public exports do not provide a production universal mint path;
- P1-4-owned issuer can issue only P1-4-owned guards;
- future-owner guards require an injected external verifier/authority port or equivalent
  owner-specific capability;
- absent future owner implementation → fail closed;
- a caller-created/fake fact or owner mismatch → rejected.

### test fixtures

Tests may use a test-only authority fixture capable of issuing owner-bound facts.

It must live only in existing test files or existing `tests/conftest.py`.

It must not be imported/wired by production `src/**`.

No P1-6/P1-7 admission logic is implemented.

---

# Stage 2 — opaque ref binding

Raw request refs remain opaque and non-authoritative.

For future-owner fact types where the request carries the corresponding opaque refs:

```text
G_EVIDENCE
↔ evidence_refs

G_HUMAN_APPROVED / G_HUMAN_REWORK / G_HUMAN_REJECTED
↔ human_result_refs

G_JUDGMENT_ACCEPTED / G_JUDGMENT_REJECTED / G_JUDGMENT_REWORK
↔ judgment_refs
```

Require the trusted future-owner fact to bind to the exact referenced identity/set, or an equivalent
immutable digest/selector.

Required:

```text
request refs only
→ DENY

future-owner fact with wrong/missing bound refs
→ DENY

owner-bound fact with exact refs
→ may satisfy that guard
```

Do not interpret domain content.
Do not implement evidence verification or Human/Judgment semantics.

If a guard has no dedicated request ref field in the current P1-4 contract, do not invent a whole
future-domain schema solely to satisfy this Stage. Preserve authority provenance in the guard
observation and report the exact boundary.

---

# Stage 3 — consistency gate on fresh mutation path

## defect

Current `verify_consistency()` is opt-in.

A fresh `request_transition()` may proceed directly from a corrupted projection if the submitted
observed state/version matches the corrupted projection.

## required implementation

Inside the authoritative repository transaction, after run serialization and before evaluating a
NEW request:

```text
load current projection
→ verify current projection against admitted append-only lineage
→ only then evaluate fresh TransitionRequest
```

Use an in-session/private consistency method.

Do not open a second race window between consistency check and mutation.

### behavior

For an existing WorkRun:

```text
projection/history consistent
→ normal evaluation may continue

projection/history inconsistent
→ raise AuthorityConflictError
→ no new TransitionRequest row
→ no TransitionEvaluation row
→ no TransitionDecision row
→ no WorkRun mutation
```

For first creation:

```text
no WorkRun
+ no admitted history for run
→ NONE → READY may evaluate

no WorkRun
+ existing transition/admitted history
→ AuthorityConflictError
```

Do not auto-repair.

### duplicate existing request

An exact same-ID/fingerprint request may return its already-existing immutable decision.

It must not create new authority or mutate projection.

If implementation chooses to consistency-check duplicate reads too, that is allowed, but the
minimum requirement is that every NEW mutation-capable request is consistency gated.

---

# Stage 4 — exact allowed candidate paths

Do not create a 20th P1-4 candidate path.

Modify only existing candidate paths as directly required, expected subset:

```text
src/aiscc/workflow/__init__.py
src/aiscc/workflow/models.py
src/aiscc/workflow/guards.py
src/aiscc/workflow/evaluator.py
src/aiscc/workflow/kernel.py
src/aiscc/workflow/ports.py
src/aiscc/persistence/repository.py
src/aiscc/persistence/models.py
migrations/versions/20260828_0001_p1_4_workflow_kernel.py
tests/unit/workflow/test_state_machine.py
tests/integration/workflow/test_postgres_kernel.py
```

`pyproject.toml` / `uv.lock` should not change unless genuinely required; no new dependency is
expected.

If a new candidate path is required:

```text
STOP
→ EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

No P1-5/P1-6/P1-7/P1-8 roots/files.

---

# Stage 5 — required unit proof

Add deterministic proof for:

1. P1-4 production issuer cannot issue `G_EVIDENCE`;
2. P1-4 production issuer cannot issue Human/Judgment guards;
3. owner mismatch fact → rejected;
4. fake/caller-created fact → rejected;
5. `WorkflowKernel` has no public guard issuer/mint handle;
6. raw `evidence_refs` alone → DENY;
7. raw `human_result_refs` alone → DENY;
8. raw `judgment_refs` alone → DENY;
9. future-owner fact with wrong bound refs → DENY;
10. exact owner-bound test fixture fact + matching refs may satisfy the exact guard;
11. exact 22 transition pairs unchanged;
12. exact 9 states unchanged;
13. terminal outgoing deny unchanged.

Test helper authority must be test-only.

---

# Stage 6 — required PostgreSQL integration proof

Retain all predecessor proof and add:

## CONSISTENCY_GATED_FRESH_MUTATION

1. build a valid run to READY/v1;
2. corrupt projection state/version in isolated test transaction;
3. submit a fresh request whose observed state/version matches the corrupted projection;
4. required result:

```text
AuthorityConflictError
```

5. prove:

```text
new request row count:
0

new evaluation row count:
0

new decision row count:
0

projection:
unchanged from deliberately corrupted fixture

auto-repair:
none
```

Clean the isolated database afterward.

## MISSING_PROJECTION_WITH_HISTORY

Create a valid run, then test-only delete/corrupt the projection in a controlled way while preserving
admitted provenance.

Fresh mutation attempt:

```text
→ AuthorityConflictError
→ no new transition provenance
→ no recreation/repair
```

If append-only/foreign-key design prevents safe fixture construction through normal SQL, use a
test-only isolated transaction/fixture with exact rollback/cleanup and explain it.

## RETAINED PROOFS

Re-run:

```text
POSTGRES_MIGRATION
AUTHORITATIVE_STATE_MUTATION
STALE_REQUEST_CONCURRENCY
DUPLICATE_REQUEST_IDEMPOTENCY
ATOMICITY
RESTART_DURABILITY
PROJECTION_EVENT_CONSISTENCY
DENIED_PROVENANCE
```

No test skip/xfail.

---

# Stage 7 — static/build/full verification

Run:

```text
uv sync --frozen --all-groups
uv build
uv run ruff check .
uv run ruff format --check .
uv run mypy --strict src tests
uv run pytest -q tests/unit tests/integration
```

Use the same isolated local PostgreSQL version/image unless a verified environmental reason requires
otherwise.

Record:

- exact test count;
- exact migration result;
- exact Docker/PostgreSQL version;
- final task-owned container/network residue.

Expected:

```text
container residue:
0

network residue:
0
```

---

# evidence contract

## executor_required

- `P1_4_REWORK_PROVENANCE_GIT`
- `BASELINE_CANDIDATE_IDENTITY`
- `OWNER_BOUND_GUARD_AUTHORITY`
- `OPAQUE_REF_BINDING`
- `CONSISTENCY_GATED_FRESH_MUTATION`
- `STATIC_SOURCE`
- `BUILD_STATIC_TYPE`
- `POSTGRES_MIGRATION`
- `AUTHORITATIVE_STATE_MUTATION`
- `STALE_REQUEST_CONCURRENCY`
- `DUPLICATE_REQUEST_IDEMPOTENCY`
- `ATOMICITY`
- `RESTART_DURABILITY`
- `PROJECTION_EVENT_CONSISTENCY`
- `DENIED_PROVENANCE`
- `FINAL_DB_CONTAINER_RESIDUE`

## human_owned

`HUMAN_VERIFICATION`

Only after all required evidence passes.

Expected:

```text
ACCEPTED
HOLD_REWORK_REQUIRED
or exact correction
```

## forbidden

- P1-5 provider/tool implementation;
- P1-6 evidence admission logic;
- P1-7 Human/Judgment logic;
- P1-8 Cycle memory;
- LangGraph core;
- provider/LLM calls/credentials;
- public deployment;
- second Git commit after Stage 0;
- Git push/remote mutation;
- unrelated Docker mutation.

---

# proof non-substitution

```text
private Python token
!= semantic owner authority

test-only universal issuer
!= production future-owner authority

opaque ref string
!= owner admission

explicit consistency API
!= mutation-path consistency gate

projection corruption detected manually
!= fresh mutation automatically denied

unit owner test
!= PostgreSQL mutation fail-closed proof
```

---

# result rules

If all rework and runtime proof passes:

```text
ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING
```

If owner separation requires implementing P1-6/P1-7 semantics:

```text
STOP
→ POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

Do not steal that scope.

If consistency gating cannot be made atomic with current repository boundary:

```text
STOP
→ HOLD_REWORK_REQUIRED_ATOMICITY
```

If a 20th candidate path is required:

```text
STOP
→ EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

Executor MUST NOT claim P1-4 `ACCEPTED / CLOSED`.

---

# report required fields

- Task ID/path;
- predecessor HEAD;
- Stage 0 provenance commit/full hash;
- baseline 19-path aggregate;
- exact modified candidate paths;
- post-rework 19-path aggregate;
- guard semantic-owner model;
- production issuer restrictions;
- test-only authority boundary;
- opaque-ref binding behavior;
- consistency-gate code path;
- fresh-corruption mutation denial proof;
- missing-projection/history proof;
- transition matrix/state-set regression proof;
- dependencies/schema delta if any;
- build/static/test results;
- PostgreSQL/Docker version;
- retained concurrency/idempotency/atomicity/restart proof;
- final residue;
- Agent claim vs admitted evidence;
- Human pending;
- forbidden-not-run;
- rollback;
- preserved paths;
- next recommendation.

---

# export bundle

Target:

```text
.aiassistant/reports/target/20260828_0928_aiscc-p1-4-owner-bound-guards-and-consistency-gated-mutation-rework-1/
```

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- all exact 19 P1-4 candidate files preserving relative paths
- compact non-secret PostgreSQL/runtime evidence

No DB volume, credentials, caches, `.venv`, Docker layers or unrelated data.

---

# Task lifecycle

```text
.aiassistant/tasks/active/20260828_0928_aiscc-p1-4-owner-bound-guards-and-consistency-gated-mutation-rework-1.md
→
.aiassistant/tasks/done/20260828_0928_aiscc-p1-4-owner-bound-guards-and-consistency-gated-mutation-rework-1.md
```

`done` means submitted, not Human accepted.

---

# preserved artifacts

Preserve:

- commit `1b04e8a0d36fc0400cbeacaf65c56f643f423923`
- `.aiassistant/tasks/done/20260828_0928_aiscc-p1-4-explicit-state-machine-kernel-resume-with-direct-canonical-placement-1.md`
- `.aiassistant/records/aiscc/cycles/20260828_0928_aiscc-p1-4-authority-owner-and-consistency-gate-hold-1.cycle.md`
- all exact 19 P1-4 candidate paths

Historical pre-rework candidate identity:

```text
19 paths
c5c6177dbf228683def88cd01907dd55db0a479824a7e9a56b7b1b5040067051
```

---

# next action after P1-4 Human acceptance

```text
P1-5 Agent Provider and Tool Execution
```

Do not execute P1-5 in this Task.
