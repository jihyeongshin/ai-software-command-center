# 작업지시서: P1-4 Explicit State Machine Kernel Implementation with P1-3 Terminal Commit

## meta

- task_id: `20260827_1941_aiscc-p1-4-explicit-state-machine-kernel-implementation-with-p1-3-terminal-commit-1`
- created_at: `2026-08-27 19:41 KST`
- phase: `P1-4 — Explicit State Machine Kernel Implementation`
- work_type: `AUTHORITATIVE_STATE_MACHINE_IMPLEMENTATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `authoritative WorkRun state/version + transition request/evaluation/decision + atomic durable mutation/provenance`
- predecessor_phase: `P1-3 Security / Runtime Safeguard Implementation and Verification`
- predecessor_result: `HUMAN_PROVIDED / ACCEPTED / CLOSED`
- predecessor_HEAD: `575fb3c4623a28b8537d15c8b34b838982f96ce2`
- P1_3_final_candidate_count: `55`
- P1_3_final_candidate_aggregate_sha256: `4a9f49a70bbe6cc628a9bc9e6612d07b724876beaf3fd0e672b9815343018c4c`
- P1_4_status_before: `NOT_STARTED`
- P1_5_status: `NOT_STARTED`

---

# 0. sole execution contract

This Task first persists P1-3 terminal acceptance and the exact accepted 55-path implementation
candidate.

Only after that commit is verified may the same Executor turn implement P1-4.

Do not execute P1-5/P1-6/P1-7/P1-8.

---

# Human preparation

Human performs only:

1. apply:

```text
20260827_1941_aiscc-p1-3-terminal-closure-canonical-persistence-1.zip
```

to repository root;

2. place this Task at:

```text
.aiassistant/tasks/active/20260827_1941_aiscc-p1-4-explicit-state-machine-kernel-implementation-with-p1-3-terminal-commit-1.md
```

3. start a fresh Executor chat.

Human does NOT create the P1-3 terminal commit.

---

# Stage 0 — P1-3 terminal implementation/provenance commit

## expected repository

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

HEAD:
575fb3c4623a28b8537d15c8b34b838982f96ce2
```

If HEAD differs:

```text
STOP
→ BLOCKED_PREDECESSOR_HEAD_DRIFT
```

## exact accepted P1-3 candidate

Before any Git index mutation, verify:

```text
candidate count:
55

aggregate SHA-256:
4a9f49a70bbe6cc628a9bc9e6612d07b724876beaf3fd0e672b9815343018c4c
```

Exact 55 paths:

- `.python-version`
- `pyproject.toml`
- `uv.lock`
- `.dockerignore`
- `src/aiscc/__init__.py`
- `src/aiscc/__main__.py`
- `src/aiscc/bootstrap.py`
- `src/aiscc/api/__init__.py`
- `src/aiscc/api/app.py`
- `src/aiscc/api/routes/__init__.py`
- `src/aiscc/api/routes/health.py`
- `src/aiscc/api/routes/control.py`
- `src/aiscc/contracts/__init__.py`
- `src/aiscc/contracts/workflow.py`
- `src/aiscc/contracts/security.py`
- `src/aiscc/security/__init__.py`
- `src/aiscc/security/models.py`
- `src/aiscc/security/policy.py`
- `src/aiscc/security/action_state.py`
- `src/aiscc/security/capability.py`
- `src/aiscc/security/cancel.py`
- `src/aiscc/security/limits.py`
- `src/aiscc/security/provenance.py`
- `src/aiscc/security/redaction.py`
- `src/aiscc/runtime/__init__.py`
- `src/aiscc/runtime/contracts.py`
- `src/aiscc/runtime/process.py`
- `src/aiscc/runtime/docker.py`
- `src/aiscc/runtime/network.py`
- `src/aiscc/runtime/cleanup.py`
- `config/security/permission-profiles.v1.toml`
- `config/security/resource-policy.v1.toml`
- `config/security/limits.v1.toml`
- `containers/p1_3/Dockerfile.sandbox`
- `containers/p1_3/Dockerfile.evidence`
- `containers/p1_3/compose.yaml`
- `tests/conftest.py`
- `tests/unit/security/test_permission_policy.py`
- `tests/unit/security/test_action_state_eligibility.py`
- `tests/unit/security/test_public_cancel_authorization.py`
- `tests/unit/security/test_capability_lifetime.py`
- `tests/unit/security/test_limits_idempotency_budget.py`
- `tests/integration/security/test_broker_fail_closed.py`
- `tests/integration/security/test_provenance_redaction.py`
- `tests/runtime/security/test_sandbox_isolation.py`
- `tests/runtime/security/test_network_boundary.py`
- `tests/runtime/security/test_secret_non_exposure.py`
- `tests/runtime/security/test_timeout_retry_cancel.py`
- `tests/runtime/security/test_idempotency_abuse_budget.py`
- `tests/runtime/security/test_cleanup_residue.py`
- `tests/runtime/security/test_failure_domain.py`
- `tests/runtime/security/test_action_state_cancel_authorization.py`
- `tests/fixtures/sandbox/allowed/input.txt`
- `tests/fixtures/sandbox/probe.py`
- `tests/fixtures/network/fixture_server.py`

Aggregate algorithm:

```text
for every exact project-relative candidate path:
lowercase SHA-256(file bytes)

sort by project-relative path

concatenate:
<path> + NUL + <sha256> + LF

SHA-256 the concatenated UTF-8 bytes
```

Mismatch:

```text
STOP
→ BLOCKED_P1_3_ACCEPTED_CANDIDATE_DRIFT
```

Do not repair source in Stage 0.

## exact terminal closure/provenance paths

In addition to the 55 accepted candidate paths, Stage 0 may commit only:

```text
.aiassistant/tasks/done/20260827_1941_aiscc-p1-3-runtime-proof-assertion-coverage-rework-1.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/records/aiscc/cycles/20260827_1941_aiscc-p1-3-security-runtime-safeguard-final-acceptance-1.cycle.md
```

Expected total terminal commit path count when all are dirty/untracked:

```text
60
```

A listed canonical path already clean at HEAD is not itself a blocker, but every actual staged path
must belong to this 60-path universe and the report must explain any clean member.

Unexpected tracked/untracked product path outside the allowed universe:

```text
STOP
→ BLOCKED_P1_3_TERMINAL_CLOSURE_COLLISION
```

Ignored active Task/target export are not commit inputs.

## Stage 0 preflight

Before index mutation:

1. verify repository/branch/HEAD;
2. verify exact 55-path candidate count and aggregate;
3. read Human-accepted P1-3 terminal Cycle;
4. read final P1-3 done Task;
5. verify canonical state says P1-3 `ACCEPTED / CLOSED` and P1-4 `READY / NOT_STARTED`;
6. inspect `git status --short`;
7. run `git diff --check`;
8. secret/private material check;
9. verify current active Task is this Task.

## one authorized local commit

Stage explicit actual changed paths only.

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
feat: accept P1-3 security runtime safeguards

Persist the Human-accepted P1-3 security/runtime implementation and
its complete non-substitutable Docker runtime verification.

Commit the exact accepted 55-path safeguard candidate, terminal
judgment provenance, and canonical project state before P1-4 begins.
```

Use a real LF-safe multiline message file / `git commit -F`.

After commit:

```text
P1_4_BASE_COMMIT=<full new hash>
```

Verify:

- parent == `575fb3c4623a28b8537d15c8b34b838982f96ce2`;
- no path outside the exact 60-path universe;
- committed accepted-candidate aggregate still equals
  `4a9f49a70bbe6cc628a9bc9e6612d07b724876beaf3fd0e672b9815343018c4c`;
- exact multiline commit message;
- tracked worktree clean;
- index empty;
- no remote operation.

After this commit:

```text
git add / commit / push
→ FORBIDDEN
```

P1-4 implementation remains uncommitted for Command Center/Human review.

---

# Stage 1 — accepted P1-1/P1-3 read/preflight

Read canonical owners:

1. `.aiassistant/rules/AISCC_ARCHITECTURE.md`
2. `.aiassistant/rules/AISCC_ORCHESTRATION.md`
3. `.aiassistant/rules/AISCC_SECURITY_SANDBOX.md`
4. `.aiassistant/rules/AISCC_RUNTIME_SUBSTRATE.md`
5. `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
6. `.aiassistant/records/aiscc/DECISION_REGISTER.md`
7. `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
8. `.aiassistant/records/aiscc/cycles/20260827_1115_aiscc-p1-1-core-domain-state-machine-design-final-acceptance-1.cycle.md`
9. `.aiassistant/records/aiscc/cycles/20260827_1941_aiscc-p1-3-security-runtime-safeguard-final-acceptance-1.cycle.md`

Inspect existing:

```text
src/aiscc/contracts/workflow.py
src/aiscc/contracts/security.py
src/aiscc/security/**
src/aiscc/runtime/**
pyproject.toml
uv.lock
```

Do not reinterpret the P1-3 test `WorkflowSnapshot` as authoritative P1-4 state.

---

# Stage 2 — exact P1-4 ownership

P1-4 owns executable implementation of:

```text
WorkRun
WorkflowState current projection
monotonic state_version

TransitionRequest
TransitionEvaluation
TransitionDecision

ADMITTED / DENIED transition provenance
target-specific explicit transition matrix
guard-result recording
stale-request denial
duplicate transition-request idempotency
atomic admitted decision + state/version mutation
append-only transition/event history
restart-durable authoritative projection
projection/event consistency verification
```

## exact nine WorkflowState values

Do not change:

```text
READY
RUNNING
ADMISSION_PENDING
HUMAN_REQUIRED
BLOCKED
REWORK_REQUIRED
ACCEPTED
REJECTED
FAILED
```

Terminal:

```text
ACCEPTED
REJECTED
FAILED
```

Do not add `CLOSED`, `CANCELLED`, `PAUSED`, provider state or security state to `WorkflowState`.

## exact authority chain

Preserve:

```text
TransitionRequest
→ TransitionEvaluation
→ TransitionDecision
→ atomic AuthoritativeStateMutation only when ADMITTED
```

and:

```text
Judgment
!= TransitionDecision

TransitionDecision
!= WorkflowState

SecurityAdmissionDecision
!= TransitionDecision
```

Agent/HTTP caller must not mutate authoritative state directly.

---

# Stage 3 — exact transition matrix

Implement exactly the P1-1 transition matrix from `.aiassistant/rules/AISCC_ORCHESTRATION.md`.

No source/target pair absent from the accepted matrix may be admitted.

At minimum all these rows must exist exactly as accepted:

```text
NONE → READY

READY → RUNNING

RUNNING → ADMISSION_PENDING
RUNNING → BLOCKED
RUNNING → REWORK_REQUIRED
RUNNING → FAILED

ADMISSION_PENDING → HUMAN_REQUIRED
ADMISSION_PENDING → BLOCKED
ADMISSION_PENDING → REWORK_REQUIRED
ADMISSION_PENDING → ACCEPTED
ADMISSION_PENDING → REJECTED

HUMAN_REQUIRED → ACCEPTED
HUMAN_REQUIRED → REWORK_REQUIRED
HUMAN_REQUIRED → REJECTED
HUMAN_REQUIRED → BLOCKED

BLOCKED → READY
BLOCKED → HUMAN_REQUIRED
BLOCKED → REWORK_REQUIRED
BLOCKED → FAILED

REWORK_REQUIRED → READY
REWORK_REQUIRED → HUMAN_REQUIRED
REWORK_REQUIRED → REJECTED
```

Terminal outgoing transition request:

```text
→ DENIED(INVALID_TRANSITION)
```

Do not silently route a denied target into another state.

---

# Stage 4 — guard interface boundary

Implement P1-1 exact guard vocabulary, including:

```text
G_CURRENT
G_CONTRACT
G_SCOPE
G_RUNTIME_CONTEXT
G_EXECUTION_STARTED
G_EXECUTOR_SUBMISSION
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
G_BLOCKER
G_BLOCKER_RESOLVED
G_REWORK_SPEC
G_FAILURE_TERMINAL
```

P1-4 does NOT implement P1-6/P1-7 owners.

Therefore use typed trusted internal refs/results such as:

```text
EvidencePredicateResult
HumanGateProjectionRef
HumanResultRef
JudgmentRef
BlockerRef
ReworkSpecRef
ExecutionEventRef
```

or semantically equivalent immutable structures.

Critical boundary:

```text
arbitrary public caller boolean
!= authoritative guard fact
```

Do NOT expose a public HTTP endpoint where a caller can submit `evidence_ok=true`,
`human_approved=true`, `judgment=ACCEPTED`, or equivalent and obtain state mutation.

Tests may construct trusted fixtures directly.

Future P1-6/P1-7 adapters will own creation/admission of their authoritative refs.

---

# Stage 5 — persistence / atomicity implementation

P1-1 requires authoritative projection survival across restart and atomic admitted mutation.

The accepted substrate direction permits P1-4 to introduce PostgreSQL persistence.

## authorized dependencies

P1-4 may add only the persistence dependencies necessary for this kernel:

```text
SQLAlchemy 2.x
asyncpg
Alembic
```

plus a narrowly justified test helper if essential.

Update:

```text
pyproject.toml
uv.lock
```

Record exact resolved versions.

Do not add provider/LLM/tool dependencies.

## authorized new roots/paths

P1-4 may create:

```text
src/aiscc/workflow/
src/aiscc/persistence/

alembic.ini
migrations/
```

Recommended exact product files:

```text
src/aiscc/workflow/__init__.py
src/aiscc/workflow/models.py
src/aiscc/workflow/guards.py
src/aiscc/workflow/matrix.py
src/aiscc/workflow/kernel.py
src/aiscc/workflow/repository.py
src/aiscc/workflow/recovery.py

src/aiscc/persistence/__init__.py
src/aiscc/persistence/database.py
src/aiscc/persistence/workflow_repository.py

migrations/env.py
migrations/script.py.mako
migrations/versions/<timestamp>_p1_4_workflow_kernel.py
```

Exact naming may differ narrowly if the report maps semantic ownership one-to-one.

No provider/tool/evidence/Human implementation directories.

## minimum durable data model

Implement only P1-4-owned persistence.

At minimum durable ownership must support:

```text
work_run current projection
transition_request
transition_evaluation
transition_decision / transition event
```

Required WorkRun projection:

```text
project_id
task_contract_id
task_contract_version
work_run_id
current WorkflowState
state_version
RuntimeMode ref/value
execution_status if already in accepted P1-1 contract
created/updated timestamps
```

Required immutable transition provenance includes enough P1-1 `P0` fields to reconstruct:

```text
request ID
source/observed state/version
authoritative evaluated state/version
target
requester identity/type
runtime mode
guard IDs/results/reasons
opaque evidence/Human/Judgment refs
decision ADMITTED/DENIED
reason
resulting state/version
timestamps
orchestrator/kernel version
```

Do NOT implement evidence/Human/Judgment tables merely to satisfy foreign keys.
Store typed opaque refs/serialized immutable refs owned by future P1-6/P1-7.

---

# Stage 6 — concurrency / stale request / idempotency

Every transition request contains:

```text
transition_request_id
observed_state
observed_state_version
target_state
```

Required:

```text
observed_state/version != authoritative current
→ DENIED(STALE_REQUEST)
→ no state mutation
```

Admission must re-check authoritative state/version in the same transaction that records the
admitted decision and updates state/version.

Required concurrency semantics:

```text
two requests from same state/version
→ at most one admitted mutation
→ other request denied stale or returns its already-existing decision
→ no lost update
```

No last-write-wins.

## transport/idempotency

Same exact `transition_request_id` retry:

```text
→ returns existing immutable evaluation/decision
→ no duplicate mutation
→ no duplicate admitted event
```

A fresh current-state attempt requires a new request ID.

---

# Stage 7 — atomicity and append-only history

For an admitted transition:

```text
TransitionDecision(ADMITTED)
+
state_version + 1 projection mutation
+
resulting transition event/provenance
```

must commit atomically or none commit.

Denied transition:

```text
decision/evaluation provenance appended
state/version unchanged
```

Do not update or delete old transition decisions/events.

Correction requires additive successor/new request.

Database constraints and repository methods must prevent accidental mutation where practical.

---

# Stage 8 — restart / reconstruction / consistency

Mandatory:

1. create/admit several transitions;
2. dispose/recreate service/repository/session objects;
3. reload current `WorkRun`;
4. verify state/version equals durable projection;
5. load ordered immutable transition history;
6. verify history reconstructs the same admitted state/version lineage.

If projection/event consistency fails:

```text
FAIL_CLOSED
→ AUTHORITY_CONFLICT / RECOVERY_REQUIRED
```

Do not silently repair projection from event history in P1-4.

Expose a deterministic consistency-check result/API internally.

---

# Stage 9 — security integration boundary

P1-3 remains canonical.

P1-4 must not weaken or bypass:

```text
RuntimeMode separation
secret boundary
runtime capability boundary
public caller fail-closed model
```

However P1-4 `TransitionDecision` is its own System authority.

Do NOT model it as a P1-3 `SecurityAdmissionDecision`.

No public state-mutation endpoint is required in P1-4.

If an internal API/CLI harness is added for tests, it must not accept caller-asserted evidence/Human/Judgment
facts as authoritative production input.

---

# Stage 10 — verification

## build/static

Run:

```text
uv sync --frozen --all-groups
uv build
uv run ruff check .
uv run ruff format --check .
uv run mypy --strict src tests
```

## unit tests

Cover at minimum:

- exact 9-state enum unchanged;
- transition matrix exact allowed/invalid pairs;
- terminal outgoing deny;
- exact target Judgment mapping:
  - ACCEPTED target ↔ accepted Judgment
  - REJECTED target ↔ rejected Judgment
  - REWORK_REQUIRED target ↔ hold/rework Judgment;
- Human gate/result does not directly mutate state;
- denied transition leaves state/version unchanged;
- no hidden target rerouting;
- state_version increments exactly once on admitted transition.

## PostgreSQL integration/runtime tests

Use an isolated local PostgreSQL Docker container/network owned by this Task.

Do not use production DB.

Required proof:

### AUTHORITATIVE_STATE_MUTATION

```text
NONE → READY/v1
READY → RUNNING/v2
RUNNING → ADMISSION_PENDING/v3
```

plus representative Human/blocked/rework/outcome paths with trusted fixtures.

### STALE_REQUEST_CONCURRENCY

Execute two concurrent requests against the same observed state/version.

Required:

```text
exactly one admitted mutation
exactly one stale/denied result
final state_version increments once
```

Repeat enough times to prove deterministic contract, not one accidental pass.

### DUPLICATE_REQUEST_IDEMPOTENCY

Submit same request ID twice / concurrently.

Required:

```text
same immutable decision identity
one mutation only
one admitted event only
```

### ATOMICITY

Inject controlled failure at transaction boundary where practical.

Prove no state/version mutation exists without its admitted decision/provenance and vice versa.

Do not corrupt the DB manually outside the isolated test harness.

### RESTART_DURABILITY

Recreate repository/kernel process objects against same PostgreSQL DB.

Prove current projection and event history survive.

### PROJECTION_EVENT_CONSISTENCY

Prove consistency checker passes on healthy history.

Use an isolated test-only controlled inconsistency fixture if safe to prove:

```text
mismatch
→ FAIL_CLOSED
```

Do not auto-repair.

### DENIED_PROVENANCE

Invalid transition, stale request, missing guard:

```text
DENIED
→ immutable evaluation/decision provenance exists
→ current state/version unchanged
```

---

# evidence contract

## executor_required

- `P1_3_TERMINAL_GIT`
- `P1_4_REPOSITORY_PREFLIGHT`
- `STATIC_SOURCE`
- `BUILD_STATIC_TYPE`
- `TARGETED_TEST`
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

Human reviews:

- P1-3 closure commit;
- exact P1-4 source/schema/dependency scope;
- transition matrix conformance;
- concurrency/atomicity/restart proof;
- no P1-6/P1-7 authority theft;
- no P1-5 scope;
- database residue/cleanup;
- whether P1-4 may be accepted.

Expected:

```text
ACCEPTED
HOLD_REWORK_REQUIRED
or exact correction
```

## forbidden

- P1-5 provider/tool implementation;
- P1-6 evidence admission implementation;
- P1-7 Human identity/gate/Judgment implementation;
- P1-8 Cycle memory implementation;
- LangGraph core;
- public deployment;
- provider/LLM credentials or calls;
- second Git commit after Stage 0;
- Git push/remote mutation;
- Browser Project Source mutation.

---

# proof non-substitution

```text
transition matrix unit test
!= PostgreSQL concurrency proof

in-memory state
!= restart-durable authoritative projection

SQL transaction exists
!= atomicity proof

HumanResult fixture
!= P1-7 HumanResult admission implementation

JudgmentRef fixture
!= P1-7 Judgment implementation

EvidencePredicate fixture
!= P1-6 evidence admission

P1-3 SecurityAdmission
!= P1-4 TransitionDecision

P1-4 WorkRun.ACCEPTED
!= Project CLOSED
```

---

# mandatory stop

Stop with exact blocker if:

```text
BLOCKED_P1_3_ACCEPTED_CANDIDATE_DRIFT
BLOCKED_P1_3_TERMINAL_CLOSURE_COLLISION
BLOCKED_PREDECESSOR_HEAD_DRIFT
BLOCKED_DEPENDENCY_RESOLUTION
BLOCKED_REQUIRED_EVIDENCE
EVIDENCE_SCOPE_EXPANSION_REQUIRED
POLICY_CONFLICT_INVESTIGATION_REQUIRED
HOLD_REWORK_REQUIRED_CONCURRENCY
HOLD_REWORK_REQUIRED_ATOMICITY
```

Do not weaken P1-1/P1-3 to make tests pass.

---

# report required fields

- Task ID/path;
- predecessor HEAD;
- exact P1-3 55-path aggregate verification;
- exact terminal commit path inventory;
- P1-3 terminal commit message/full hash;
- `P1_4_BASE_COMMIT`;
- post-commit clean evidence;
- exact P1-4 created/modified paths;
- new dependency versions/reasons;
- migration/schema inventory;
- exact transition matrix implementation mapping;
- guard/ref boundary;
- PostgreSQL container/image/version;
- migration result;
- unit/static results;
- authoritative mutation proof;
- stale concurrency proof;
- duplicate idempotency proof;
- atomicity proof;
- restart proof;
- projection/event consistency proof;
- denied provenance proof;
- final DB/container/network residue;
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
.aiassistant/reports/target/20260827_1941_aiscc-p1-4-explicit-state-machine-kernel-implementation-with-p1-3-terminal-commit-1/
```

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- changed P1-4 source/test/migration/build files preserving repository-relative paths
- compact non-secret PostgreSQL/concurrency/atomicity/restart evidence

Do not export DB volume, credentials, `.venv`, caches, Docker layers or unrelated data.

---

# Task lifecycle

```text
.aiassistant/tasks/active/20260827_1941_aiscc-p1-4-explicit-state-machine-kernel-implementation-with-p1-3-terminal-commit-1.md
→
.aiassistant/tasks/done/20260827_1941_aiscc-p1-4-explicit-state-machine-kernel-implementation-with-p1-3-terminal-commit-1.md
```

`done` means submitted, not Human accepted.

---

# preserved artifacts

Always preserve:

- the P1-3 terminal local commit created by this Task;
- `.aiassistant/tasks/done/20260827_1941_aiscc-p1-3-runtime-proof-assertion-coverage-rework-1.md`;
- `.aiassistant/records/aiscc/cycles/20260827_1941_aiscc-p1-3-security-runtime-safeguard-final-acceptance-1.cycle.md`;
- all exact 55 accepted P1-3 implementation paths;
- `.aiassistant/tasks/done/20260827_1941_aiscc-p1-4-explicit-state-machine-kernel-implementation-with-p1-3-terminal-commit-1.md`.

If P1-4 implementation proceeds, preserve all changed P1-4 source/test/migration/build candidate
paths until Command Center/Human judgment.

---

# next action after P1-4 Human acceptance

```text
P1-5 Agent Provider and Tool Execution
```

Do not execute P1-5 in this Task.
