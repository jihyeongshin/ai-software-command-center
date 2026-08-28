# 작업지시서: P1-4 Denied Pre-Creation Retry Consistency Semantics Rework

## meta

- task_id: `20260828_1110_aiscc-p1-4-denied-precreation-retry-consistency-semantics-rework-1`
- created_at: `2026-08-28 11:10 KST`
- phase: `P1-4 — Explicit State Machine Kernel Implementation`
- work_type: `AUTHORITATIVE_STATE_MACHINE_IMPLEMENTATION_REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `NONE/v0 denied provenance + fresh create retry consistency semantics`
- predecessor_task: `20260828_0928_aiscc-p1-4-owner-bound-guards-and-consistency-gated-mutation-rework-1`
- predecessor_result: `ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING`
- command_center_result: `HOLD_REWORK_REQUIRED`
- predecessor_HEAD: `325f876234c580d6f61d650501ed3250d152970a`
- predecessor_candidate_path_count: `19`
- predecessor_candidate_aggregate_sha256: `56a92e856e5f04faab68465b564afd90dbae83be87f813b642bdb2fd567623a5`
- P1_4_status_before: `HOLD_REWORK_REQUIRED`
- P1_5_status: `NOT_STARTED / BLOCKED`

---

# 0. sole execution contract

This is a narrow repository consistency semantics rework.

Retain the predecessor corrections:

```text
owner-bound future guard authority separation
opaque-ref binding
no WorkflowKernel mint handle
fresh mutation consistency gate
exact 9-state / 22-pair matrix
PostgreSQL WorkRun/state_version
advisory lock + row lock + CAS
atomic request/evaluation/decision/projection transaction
duplicate request idempotency
append-only provenance
restart durability
```

Rework only the interpretation of:

```text
no WorkRun projection + existing DENIED-only pre-creation provenance
```

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
325f876234c580d6f61d650501ed3250d152970a
```

If HEAD differs:

```text
STOP
→ BLOCKED_PREDECESSOR_HEAD_DRIFT
```

## expected current candidate

Verify before Git index mutation:

```text
path count:
19

aggregate SHA-256:
56a92e856e5f04faab68465b564afd90dbae83be87f813b642bdb2fd567623a5
```

Mismatch:

```text
STOP
→ BLOCKED_P1_4_CANDIDATE_DRIFT
```

Do not revert/discard the current candidate.

## allowed Stage 0 provenance paths

Exactly:

```text
.aiassistant/tasks/done/20260828_0928_aiscc-p1-4-owner-bound-guards-and-consistency-gated-mutation-rework-1.md

.aiassistant/records/aiscc/cycles/20260828_1110_aiscc-p1-4-denied-precreation-provenance-retry-semantics-hold-1.cycle.md
```

Current 19 candidate paths MUST NOT be staged.

Unexpected path:

```text
STOP
→ BLOCKED_P1_4_REWORK_PROVENANCE_COLLISION
```

## one local provenance commit

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
docs: record P1-4 denied precreation retry hold

Persist the P1-4 review that accepted owner-bound guard authority and
mutation-path consistency gating but found denied pre-creation
provenance incorrectly blocking fresh NONE-to-READY retries.

Keep P1-5 blocked until denied audit provenance no longer behaves like
a hidden terminal workflow state.
```

Use LF-safe UTF-8 message file and `git commit -F`.

After commit:

```text
P1_4_DENIED_RETRY_REWORK_BASE_COMMIT=<full hash>
```

Verify:

- parent == `325f876234c580d6f61d650501ed3250d152970a`;
- exact two provenance paths only;
- exact multiline message;
- index empty;
- no remote operation.

After this commit:

```text
git add / commit / push
→ FORBIDDEN
```

---

# Stage 1 — required consistency semantics

## invariant

A denied transition is immutable audit provenance, not an authoritative state mutation.

Required:

```text
DENIED
→ current WorkflowState/state_version unchanged

if authoritative state remains NONE/v0
→ a corrected fresh request may retry from NONE/v0
```

### projection absent + no history

Existing normal first-create behavior remains:

```text
no WorkRun
+ no transition history
→ evaluate fresh NONE/v0 request
```

### projection absent + complete denied-only history

Treat as consistent pre-creation `NONE/v0` only when all are true:

```text
no WorkRun projection

zero ADMITTED decisions for work_run_id

every prior request has exactly one evaluation
and exactly one decision

every prior decision == DENIED

no orphan/partial request/evaluation/decision structure

prior denied run identity is compatible with incoming request
```

Then fresh evaluation may continue from:

```text
authoritative_state = NONE
authoritative_state_version = 0
```

### projection absent + admitted history

Required:

```text
one or more ADMITTED decisions
→ AuthorityConflictError
→ no new provenance
→ no projection recreation
```

Retain the predecessor missing-projection-with-admitted-history proof.

### partial/inconsistent history

Required:

```text
request without complete evaluation/decision
or inconsistent request/evaluation/decision ownership
→ AuthorityConflictError
→ no new provenance
→ no auto repair
```

---

# Stage 2 — pre-creation run identity isolation

Denied audit provenance must not allow one `work_run_id` to be repurposed across authoritative run
identities.

For all existing denied-only requests under an absent projection, compare at minimum:

```text
project_id
task_contract_id
task_contract_version
runtime_mode
```

against the incoming fresh request.

Required:

```text
all compatible
→ fresh retry may continue

any conflict
→ AuthorityConflictError
→ no new request/evaluation/decision
→ projection remains absent
```

Do not require identical:

```text
transition_request_id
requester_identity
requester_type
created_at
target_state
```

because a corrected fresh retry is intentionally a new attempt.

Do not introduce a new table solely for this rework.

---

# Stage 3 — exact allowed candidate paths

Do not create a 20th candidate path.

Expected modifications:

```text
src/aiscc/persistence/repository.py
tests/integration/workflow/test_postgres_kernel.py
```

If a small existing-model/test helper change is truly required, only existing 19 candidate paths may
be touched and the report must justify it.

No migration/schema/dependency change is expected.

If a new path is required:

```text
STOP
→ EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

Do not modify P1-5/P1-6/P1-7/P1-8 owners.

---

# Stage 4 — mandatory PostgreSQL proof

## DENIED_PRECREATION_MISSING_GUARD_RETRY

1. fresh run ID;
2. request:

```text
NONE/v0 → READY
facts=()
```

3. required:

```text
DENIED(MISSING_GUARD)
projection absent
denied provenance count == 1
```

4. new request ID, same run identity, exact required trusted guards;
5. required:

```text
ADMITTED
READY/v1
```

6. ordered history retains:

```text
DENIED
ADMITTED
```

7. consistency check on resulting WorkRun passes.

## DENIED_PRECREATION_INVALID_TRANSITION_RETRY

1. fresh run ID;
2. invalid `NONE/v0 → non-READY target`;
3. required:

```text
DENIED(INVALID_TRANSITION)
projection absent
```

4. fresh valid `NONE/v0 → READY`;
5. required:

```text
ADMITTED READY/v1
```

## MULTIPLE_DENIED_PRECREATION_RETRY

Create at least two complete denied attempts under same compatible run identity.

Then valid fresh create:

```text
→ exactly one READY/v1 projection
→ all denied provenance retained
→ one admitted create
```

## DENIED_PRECREATION_IDENTITY_CONFLICT

Create complete denied-only history for identity A.

Fresh `NONE/v0 → READY` using same `work_run_id`, but alter one identity field per deterministic
cases:

```text
project_id
task_contract_id
task_contract_version
runtime_mode
```

Each:

```text
→ AuthorityConflictError
→ provenance counts unchanged
→ projection absent
```

## PARTIAL_PRECREATION_HISTORY_FAIL_CLOSED

Using isolated test-only SQL/transaction, create one structurally incomplete pre-creation history
case if production constraints permit.

Fresh create must:

```text
→ AuthorityConflictError
→ no new provenance
→ no auto repair
```

If the schema prevents constructing a partial committed fixture because transaction/FK constraints
make it impossible, report the exact constraint proof and exercise the nearest safe corruption case
without weakening schema.

## RETAINED CONSISTENCY PROOFS

Re-run:

```text
projection/event mismatch fresh mutation gate
missing projection + admitted history gate
healthy consistency reconstruction
restart durability
```

---

# Stage 5 — regression proof

Re-run all existing P1-4 proof:

```text
exact 9 states
exact 22 transition pairs
terminal denial
Judgment mapping

owner-bound guard authority
raw-ref denial
owner/ref mismatch denial
absent future verifier fail-closed

POSTGRES_MIGRATION
AUTHORITATIVE_STATE_MUTATION
STALE_REQUEST_CONCURRENCY
DUPLICATE_REQUEST_IDEMPOTENCY
ATOMICITY
RESTART_DURABILITY
PROJECTION_EVENT_CONSISTENCY
DENIED_PROVENANCE
```

Build/static:

```text
uv sync --frozen --all-groups
uv build
uv run ruff check .
uv run ruff format --check .
uv run mypy --strict src tests
uv run pytest -q tests/unit tests/integration
```

No skip/xfail.

Use isolated local PostgreSQL only.

Final Task-owned Docker:

```text
container residue:
0

network residue:
0
```

---

# evidence contract

## executor_required

- `P1_4_DENIED_RETRY_REWORK_PROVENANCE_GIT`
- `BASELINE_CANDIDATE_IDENTITY`
- `DENIED_PRECREATION_MISSING_GUARD_RETRY`
- `DENIED_PRECREATION_INVALID_TRANSITION_RETRY`
- `MULTIPLE_DENIED_PRECREATION_RETRY`
- `DENIED_PRECREATION_IDENTITY_CONFLICT`
- `PARTIAL_PRECREATION_HISTORY_FAIL_CLOSED`
- `CONSISTENCY_GATED_FRESH_MUTATION`
- `OWNER_BOUND_GUARD_AUTHORITY`
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

Human final review only after all required proof passes.

Expected:

```text
ACCEPTED
HOLD_REWORK_REQUIRED
or exact correction
```

## forbidden

- P1-5 provider/tool implementation;
- P1-6 evidence admission implementation;
- P1-7 Human/Judgment implementation;
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
denied audit row
!= admitted authority

no WorkRun projection
!= corruption when history is complete DENIED-only

same work_run_id
!= same authoritative run identity

state/version unchanged
!= retry impossible

one retry test
!= identity isolation proof

unit test
!= PostgreSQL provenance/retry proof
```

---

# result rules

If all rework and PostgreSQL proof passes:

```text
ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING
```

If denied-only retry requires a new durable authority concept/table:

```text
STOP
→ POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

Do not silently expand schema.

If consistency changes weaken admitted-history corruption detection:

```text
STOP
→ HOLD_REWORK_REQUIRED_CONSISTENCY
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
- post-rework aggregate;
- absent-projection consistency algorithm;
- denied-only structural-completeness rule;
- pre-creation run identity rule;
- missing-guard retry proof;
- invalid-transition retry proof;
- multi-denial retry proof;
- identity-conflict proof;
- partial-history fail-closed proof;
- retained admitted-history corruption proof;
- retained owner-bound guard proof;
- full build/static/test result;
- PostgreSQL/Docker version;
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
.aiassistant/reports/target/20260828_1110_aiscc-p1-4-denied-precreation-retry-consistency-semantics-rework-1/
```

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- all exact 19 P1-4 candidate files preserving relative paths
- compact non-secret PostgreSQL/runtime evidence

Do not export DB volume, credentials, caches, `.venv`, Docker layers or unrelated data.

---

# Task lifecycle

```text
.aiassistant/tasks/active/20260828_1110_aiscc-p1-4-denied-precreation-retry-consistency-semantics-rework-1.md
→
.aiassistant/tasks/done/20260828_1110_aiscc-p1-4-denied-precreation-retry-consistency-semantics-rework-1.md
```

`done` means submitted, not Human accepted.

---

# preserved artifacts

Preserve:

- commit `1b04e8a0d36fc0400cbeacaf65c56f643f423923`
- commit `325f876234c580d6f61d650501ed3250d152970a`
- `.aiassistant/tasks/done/20260828_0928_aiscc-p1-4-owner-bound-guards-and-consistency-gated-mutation-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260828_1110_aiscc-p1-4-denied-precreation-provenance-retry-semantics-hold-1.cycle.md`
- all exact 19 P1-4 candidate paths

Historical pre-rework candidate:

```text
19 paths
56a92e856e5f04faab68465b564afd90dbae83be87f813b642bdb2fd567623a5
```

---

# next action after P1-4 Human acceptance

```text
P1-5 Agent Provider and Tool Execution
```

Do not execute P1-5 in this Task.
