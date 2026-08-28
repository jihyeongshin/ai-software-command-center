# 작업지시서: P1-4 Explicit State Machine Kernel Resume with Direct Canonical Placement

## meta

- task_id: `20260828_0928_aiscc-p1-4-explicit-state-machine-kernel-resume-with-direct-canonical-placement-1`
- created_at: `2026-08-28 09:28 KST`
- phase: `P1-4 — Explicit State Machine Kernel Implementation`
- work_type: `AUTHORITATIVE_STATE_MACHINE_IMPLEMENTATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `direct exact terminal canonical placement → terminal/preflight provenance commit → P1-4 authoritative kernel`
- predecessor_task: `20260827_2252_aiscc-p1-4-explicit-state-machine-kernel-resume-with-repair-v4-1`
- predecessor_result: `BLOCKED_TERMINAL_REPAIR_INPUT_MISMATCH`
- predecessor_HEAD: `575fb3c4623a28b8537d15c8b34b838982f96ce2`
- P1_3_result: `HUMAN_PROVIDED / ACCEPTED / CLOSED`
- P1_3_candidate_count: `55`
- P1_3_candidate_aggregate_sha256: `4a9f49a70bbe6cc628a9bc9e6612d07b724876beaf3fd0e672b9815343018c4c`
- P1_4_status_before: `NOT_STARTED`
- P1_5_status: `NOT_STARTED`

---

# 0. sole execution contract

The nested repair-input ZIP transport is retired.

Human has extracted one exact repository-root placement packet that directly installed this Task
and the exact terminal canonical files/Cycles.

There is no `.aiassistant/bootstrap-input/*.zip` prerequisite in this Task.

The Executor verifies the directly placed canonical file hashes and then continues:

```text
direct canonical hash verification
→ one terminal + all-preflight provenance commit
→ same-turn P1-4 implementation
```

---

# Stage 0A — repository / stale-active / accepted-candidate preflight

Expected:

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

HEAD:
575fb3c4623a28b8537d15c8b34b838982f96ce2

P1-3 candidate count:
55

P1-3 candidate aggregate:
4a9f49a70bbe6cc628a9bc9e6612d07b724876beaf3fd0e672b9815343018c4c
```

Verify index empty.

A stale ignored active predecessor may exist:

```text
.aiassistant/tasks/active/20260827_2252_aiscc-p1-4-explicit-state-machine-kernel-resume-with-repair-v4-1.md
```

Durable done copy:

```text
.aiassistant/tasks/done/20260827_2252_aiscc-p1-4-explicit-state-machine-kernel-resume-with-repair-v4-1.md
```

The Executor may remove only the stale ignored active copy IFF:

```text
both exist
AND exact task_id matches
AND SHA-256(active bytes) == SHA-256(done bytes)
```

Otherwise:

```text
STOP
→ BLOCKED_ACTIVE_DONE_TASK_COLLISION
```

Never remove the durable done copy.

---

# Stage 0B — direct canonical authority verification

The following eight repository canonical files were directly placed by the Human packet.

They MUST exist exactly at these paths and match these hashes:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
sha256:
301b6c000e3b1686d076b21dbf8159149fdaea4637c6eb4a996811993e0d0199

.aiassistant/records/aiscc/DECISION_REGISTER.md
sha256:
a0041810b25c8a46dd30bc8572536b10ad7b6bc600d4a2a4a7d3376a531dc4d6

.aiassistant/records/aiscc/NEXT_ACTIONS.md
sha256:
388e0a6ac5608d787c8121ac1f48ddee0b46e825995a4ac2d9c931ba0900a049

.aiassistant/records/aiscc/cycles/20260827_2109_aiscc-p1-4-preflight-terminal-state-persistence-conflict-1.cycle.md
sha256:
dd270ca27d4d12ea35311078f06754415d428bc5b6498544d376e52b628fb365

.aiassistant/records/aiscc/cycles/20260827_2109_aiscc-p1-4-terminal-repair-input-missing-blocker-1.cycle.md
sha256:
8c4ad53ca0fd32f816536af2d11b54013bf48576da787d2fb3d3276d959727a1

.aiassistant/records/aiscc/cycles/20260827_2252_aiscc-p1-4-terminal-repair-input-v2-missing-repeat-blocker-1.cycle.md
sha256:
476b2935dcf31a8761c60f0889669176e30c034fc755c22bc674ae3056de9b41

.aiassistant/records/aiscc/cycles/20260827_2252_aiscc-p1-4-terminal-closure-universe-and-diffcheck-conflict-1.cycle.md
sha256:
1754b29027f6c0479af01e28e9cdc690dfd072e354154df25e1982d48f816254

.aiassistant/records/aiscc/cycles/20260828_0928_aiscc-p1-4-terminal-repair-input-v4-missing-blocker-1.cycle.md
sha256:
0e66c9bdaedc78d70e062fb02a9a10ff9becbdd6165aa482d2b8aea794e99076

```

Do not fetch, reconstruct, merge, or use a bootstrap repair ZIP.

For every path:

```text
exists
AND SHA-256 == expected
```

Required.

For `DECISION_REGISTER.md` additionally verify:

```text
ends with exactly one LF
does not end with two LF bytes
```

Then run:

```text
git diff --check
```

Required:

```text
PASS
```

Any hash mismatch:

```text
STOP
→ BLOCKED_DIRECT_CANONICAL_PLACEMENT_MISMATCH
```

If exact hashes pass but diff check fails:

```text
STOP
→ BLOCKED_TERMINAL_REPAIR_FORMAT_CONFLICT
```

Do not edit canonical bytes.

---

# Stage 0C — semantic terminal/preflight gate

Verify:

```text
CURRENT_STATE_SUMMARY
→ P1-3 ACCEPTED / CLOSED
→ P1-4 READY / NOT_STARTED

DECISION_REGISTER
→ AISCC-P1-3-SECURITY-RUNTIME-SAFEGUARDS-V1
→ HUMAN_PROVIDED / ACCEPTED / CLOSED

NEXT_ACTIONS
→ P1-3 completed
→ P1-4 current next action

five P1-4 blocker Cycles
→ all are pre-implementation Stage 0 blockers
```

Also verify unchanged P1-3 terminal Cycle:

```text
.aiassistant/records/aiscc/cycles/
20260827_1941_aiscc-p1-3-security-runtime-safeguard-final-acceptance-1.cycle.md
```

---

# Stage 0D — exact terminal + five-preflight provenance commit

Allowed commit universe:

```text
55 exact accepted P1-3 implementation paths

.aiassistant/tasks/done/20260827_1941_aiscc-p1-3-runtime-proof-assertion-coverage-rework-1.md
.aiassistant/records/aiscc/cycles/20260827_1941_aiscc-p1-3-security-runtime-safeguard-final-acceptance-1.cycle.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/tasks/done/20260827_1941_aiscc-p1-4-explicit-state-machine-kernel-implementation-with-p1-3-terminal-commit-1.md
.aiassistant/records/aiscc/cycles/20260827_2109_aiscc-p1-4-preflight-terminal-state-persistence-conflict-1.cycle.md

.aiassistant/tasks/done/20260827_2109_aiscc-p1-4-explicit-state-machine-kernel-implementation-with-exact-terminal-state-repair-1.md
.aiassistant/records/aiscc/cycles/20260827_2109_aiscc-p1-4-terminal-repair-input-missing-blocker-1.cycle.md

.aiassistant/tasks/done/20260827_2109_aiscc-p1-4-explicit-state-machine-kernel-resume-with-repair-input-v2-1.md
.aiassistant/records/aiscc/cycles/20260827_2252_aiscc-p1-4-terminal-repair-input-v2-missing-repeat-blocker-1.cycle.md

.aiassistant/tasks/done/20260827_2252_aiscc-p1-4-explicit-state-machine-kernel-resume-with-placement-packet-1.md
.aiassistant/records/aiscc/cycles/20260827_2252_aiscc-p1-4-terminal-closure-universe-and-diffcheck-conflict-1.cycle.md

.aiassistant/tasks/done/20260827_2252_aiscc-p1-4-explicit-state-machine-kernel-resume-with-repair-v4-1.md
.aiassistant/records/aiscc/cycles/20260828_0928_aiscc-p1-4-terminal-repair-input-v4-missing-blocker-1.cycle.md
```

Maximum universe count:

```text
70
```

Already-clean allowed members are not blockers.
Every actual staged path must belong to this exact universe.

Active Tasks and target reports are ignored and never staged.

Before staging:

```text
git status --short
git diff --check
```

Recompute accepted P1-3 aggregate immediately before commit:

```text
4a9f49a70bbe6cc628a9bc9e6612d07b724876beaf3fd0e672b9815343018c4c
```

Exactly one local commit is authorized.

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
feat: accept P1-3 safeguards and record P1-4 preflights

Persist the Human-accepted P1-3 security/runtime implementation and
the exact terminal canonical state.

Record all blocked P1-4 preflights, then resume P1-4 from the verified
authoritative repository state.
```

Use LF-safe UTF-8 message file + `git commit -F`.

After commit:

```text
P1_4_BASE_COMMIT=<full hash>
```

Verify:

- parent == `575fb3c4623a28b8537d15c8b34b838982f96ce2`;
- all committed paths are in the exact 70-path universe;
- committed 55-path P1-3 aggregate exact;
- exact multiline commit message;
- tracked worktree clean;
- index empty;
- no remote operation.

After this one commit:

```text
git add / commit / push
→ FORBIDDEN
```

P1-4 implementation remains uncommitted for Command Center/Human review.

---

# Stage 1 — accepted P1-1/P1-3 canonical read

Read:

1. `.aiassistant/rules/AISCC_ARCHITECTURE.md`
2. `.aiassistant/rules/AISCC_ORCHESTRATION.md`
3. `.aiassistant/rules/AISCC_SECURITY_SANDBOX.md`
4. `.aiassistant/rules/AISCC_RUNTIME_SUBSTRATE.md`
5. `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
6. `.aiassistant/records/aiscc/DECISION_REGISTER.md`
7. `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
8. `.aiassistant/records/aiscc/cycles/20260827_1115_aiscc-p1-1-core-domain-state-machine-design-final-acceptance-1.cycle.md`
9. `.aiassistant/records/aiscc/cycles/20260827_1941_aiscc-p1-3-security-runtime-safeguard-final-acceptance-1.cycle.md`
10. `.aiassistant/records/aiscc/cycles/20260827_2109_aiscc-p1-4-preflight-terminal-state-persistence-conflict-1.cycle.md`
11. `.aiassistant/records/aiscc/cycles/20260827_2109_aiscc-p1-4-terminal-repair-input-missing-blocker-1.cycle.md`
12. `.aiassistant/records/aiscc/cycles/20260827_2252_aiscc-p1-4-terminal-repair-input-v2-missing-repeat-blocker-1.cycle.md`
13. `.aiassistant/records/aiscc/cycles/20260827_2252_aiscc-p1-4-terminal-closure-universe-and-diffcheck-conflict-1.cycle.md`
14. `.aiassistant/records/aiscc/cycles/20260828_0928_aiscc-p1-4-terminal-repair-input-v4-missing-blocker-1.cycle.md`

Inspect existing P1-3 runtime/security contracts.

Do not treat the P1-3 test `WorkflowSnapshot` as authoritative P1-4 state.

---

# Stage 2 — P1-4 exact ownership

Implement:

```text
WorkRun
authoritative current WorkflowState
monotonic state_version

TransitionRequest
TransitionEvaluation
TransitionDecision

exact explicit transition matrix
guard evaluation result recording

ADMITTED / DENIED append-only transition provenance
stale-request denial
duplicate request idempotency
atomic admitted state/version mutation
restart-durable authoritative projection
projection/event consistency fail-closed check
```

Do not use LangGraph as orchestration core.

Preserve:

```text
AgentOutput != SystemState
Judgment != TransitionDecision
TransitionDecision != WorkflowState
SecurityAdmissionDecision != TransitionDecision
RuntimeMode != WorkflowState
```

---

# Stage 3 — exact WorkflowState / transition matrix

Exact nine states:

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

Do not add workflow states.

Implement the exact accepted P1-1 transition matrix from `AISCC_ORCHESTRATION.md`.

At minimum it contains exactly:

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

Absent pair:

```text
DENIED(INVALID_TRANSITION)
```

Terminal outgoing request:

```text
DENIED(INVALID_TRANSITION)
```

No hidden rerouting.

---

# Stage 4 — trusted guard boundary

Implement exact accepted guard vocabulary from `AISCC_ORCHESTRATION.md`, including:

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

P1-4 does NOT implement P1-6/P1-7.

Use immutable typed trusted internal refs/results for evidence/Human/Judgment/blocker/rework/execution
inputs.

Critical:

```text
public caller boolean
!= authoritative guard fact

caller evidence_ok=true
!= admitted evidence

caller human_approved=true
!= HumanResult

caller judgment=ACCEPTED
!= authoritative Judgment
```

No public authoritative state mutation endpoint using caller-asserted facts.

Tests may construct trusted fixtures directly.

---

# Stage 5 — PostgreSQL persistence / atomicity

P1-4 may add only:

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

Authorized new roots:

```text
src/aiscc/workflow/
src/aiscc/persistence/
alembic.ini
migrations/
```

No provider/evidence/Human/Cycle-memory implementation roots.

Minimum durable ownership:

```text
work_run current projection
transition request
transition evaluation
transition decision/event provenance
```

WorkRun projection must include:

```text
project_id
task_contract_id
task_contract_version
work_run_id
WorkflowState
state_version
RuntimeMode
created/updated timestamps
```

Transition provenance must reconstruct:

```text
request ID
observed source state/version
authoritative evaluated state/version
target
requester identity/type
RuntimeMode
guard IDs/results/reasons
opaque evidence/Human/Judgment refs
ADMITTED/DENIED
decision reason
resulting state/version
timestamps
kernel/orchestrator version
```

Do not implement P1-6/P1-7 tables merely for foreign keys.

---

# Stage 6 — stale concurrency / duplicate idempotency

Every transition request contains:

```text
transition_request_id
observed_state
observed_state_version
target_state
```

Required:

```text
observed state/version != authoritative current
→ DENIED(STALE_REQUEST)
→ no mutation
```

Admission re-check and mutation occur in the same DB transaction.

Concurrent same-version requests:

```text
at most one admitted mutation
other request → STALE_REQUEST or its already-existing immutable decision
no lost update
```

Same exact request ID retry/concurrency:

```text
same immutable decision identity
one admitted event
one mutation
```

Fresh current-state attempt requires a new request ID.

---

# Stage 7 — atomicity / append-only provenance

Admitted transition:

```text
ADMITTED TransitionDecision
+ state_version + 1
+ resulting provenance/event
→ atomically commit all or none
```

Denied:

```text
immutable denial provenance
+ state/version unchanged
```

Old decisions/events are not updated/deleted.

---

# Stage 8 — restart / consistency

Prove:

1. create/admit transitions;
2. dispose/recreate kernel/repository/session objects;
3. reload WorkRun;
4. state/version survives;
5. ordered transition history survives;
6. admitted history reconstructs same current state/version.

Consistency mismatch:

```text
FAIL_CLOSED
→ AUTHORITY_CONFLICT / RECOVERY_REQUIRED
```

Do not auto-repair in P1-4.

---

# Stage 9 — verification

## build/static

```text
uv sync --frozen --all-groups
uv build
uv run ruff check .
uv run ruff format --check .
uv run mypy --strict src tests
```

## unit

At minimum:

- exact 9 states;
- exact allowed/invalid transition matrix;
- terminal outgoing deny;
- Judgment target mapping;
- Human result cannot directly mutate;
- denied transition leaves state/version unchanged;
- no hidden reroute;
- admitted state_version increments exactly once.

## isolated PostgreSQL Docker integration

Use Task-owned local PostgreSQL container/network only.

No production DB.

Required proof classes:

```text
POSTGRES_MIGRATION
AUTHORITATIVE_STATE_MUTATION
STALE_REQUEST_CONCURRENCY
DUPLICATE_REQUEST_IDEMPOTENCY
ATOMICITY
RESTART_DURABILITY
PROJECTION_EVENT_CONSISTENCY
DENIED_PROVENANCE
FINAL_DB_CONTAINER_RESIDUE
```

### authoritative mutation

Prove:

```text
NONE → READY/v1
READY → RUNNING/v2
RUNNING → ADMISSION_PENDING/v3
```

plus representative blocked/rework/Human/outcome paths using trusted fixtures.

### stale concurrency

Two simultaneous requests against one observed state/version.

Required:

```text
exactly one admitted mutation
exactly one stale/denied
state_version increments once
```

Repeat deterministically.

### duplicate request ID

Same ID twice/concurrently:

```text
same immutable decision
one mutation
one admitted event
```

### atomicity

Use a controlled test-only failure injection at repository transaction boundary.

Prove no projection mutation without admitted decision/provenance and no admitted mutation record
without corresponding projection update.

### restart durability

Recreate service/repository/session objects against same DB and verify projection/history.

### consistency

Healthy lineage → PASS.

Controlled isolated mismatch fixture → fail closed.

No automatic repair.

### denied provenance

Invalid transition, stale request, missing guard:

```text
DENIED provenance exists
state/version unchanged
```

---

# evidence contract

## executor_required

- `P1_3_TERMINAL_REPAIR_INPUT`
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

- exact terminal repair/commit;
- P1-4 source/schema/dependencies;
- transition matrix;
- trusted guard boundary;
- PostgreSQL concurrency/atomicity/restart/consistency proof;
- no P1-5/P1-6/P1-7/P1-8 authority theft;
- residue cleanup;
- final P1-4 acceptance.

Expected:

```text
ACCEPTED
HOLD_REWORK_REQUIRED
or exact correction
```

## forbidden

- P1-5 provider/tool implementation;
- P1-6 evidence admission implementation;
- P1-7 Human gate/Judgment implementation;
- P1-8 Cycle-memory implementation;
- LangGraph core;
- provider/LLM call/credential;
- public deployment;
- second Git commit after Stage 0;
- Git push/remote mutation;
- Browser Project Source mutation.

---

# proof non-substitution

```text
correct repair ZIP
!= repository commit

transition unit test
!= PostgreSQL concurrency proof

in-memory WorkRun
!= restart-durable authority

SQL transaction
!= atomicity proof

trusted Human/Judgment fixture
!= P1-7 implementation

trusted Evidence fixture
!= P1-6 implementation

P1-3 SecurityAdmission
!= P1-4 TransitionDecision

WorkRun ACCEPTED
!= Project CLOSED
```

---

# mandatory stop

Stop with exact blocker if:

```text
BLOCKED_PREDECESSOR_HEAD_DRIFT
BLOCKED_P1_3_ACCEPTED_CANDIDATE_DRIFT
BLOCKED_TERMINAL_REPAIR_INPUT_MISMATCH
BLOCKED_P1_3_TERMINAL_CLOSURE_COLLISION
BLOCKED_DEPENDENCY_RESOLUTION
BLOCKED_REQUIRED_EVIDENCE
EVIDENCE_SCOPE_EXPANSION_REQUIRED
POLICY_CONFLICT_INVESTIGATION_REQUIRED
HOLD_REWORK_REQUIRED_CONCURRENCY
HOLD_REWORK_REQUIRED_ATOMICITY
```

Do not weaken accepted P1-1/P1-3 semantics.

---

# report required fields

- Task ID/path;
- old HEAD;
- repair-input ZIP hash;
- repair-input entry hashes;
- canonical post-repair hashes;
- P1-3 candidate aggregate;
- exact Stage 0 staged/committed paths;
- terminal/provenance commit message;
- full `P1_4_BASE_COMMIT`;
- post-commit clean evidence;
- exact P1-4 changed paths;
- dependencies/versions/reasons;
- migration/schema inventory;
- transition matrix mapping;
- trusted guard/ref boundary;
- PostgreSQL image/version;
- migration result;
- build/static/unit results;
- authoritative mutation proof;
- stale concurrency proof;
- duplicate idempotency proof;
- atomicity proof;
- restart durability;
- consistency proof;
- denied provenance;
- final DB/container/network residue;
- Agent claim vs admitted evidence;
- Human pending;
- forbidden-not-run;
- rollback;
- preserved exact paths;
- next recommendation.

---

# export bundle

Target:

```text
.aiassistant/reports/target/20260828_0928_aiscc-p1-4-explicit-state-machine-kernel-resume-with-direct-canonical-placement-1/
```

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- changed P1-4 source/test/migration/build files preserving repository-relative paths
- compact non-secret PostgreSQL/runtime evidence

Do not export bootstrap repair ZIP, DB volume, credentials, `.venv`, caches, Docker layers or
unrelated data.

---

# Task lifecycle

```text
.aiassistant/tasks/active/20260828_0928_aiscc-p1-4-explicit-state-machine-kernel-resume-with-direct-canonical-placement-1.md
→
.aiassistant/tasks/done/20260828_0928_aiscc-p1-4-explicit-state-machine-kernel-resume-with-direct-canonical-placement-1.md
```

`done` means submitted, not Human accepted.

---

# preserved artifacts

Always preserve:

- the Stage 0 P1-3 terminal/preflight-provenance commit;
- `.aiassistant/tasks/done/20260827_1941_aiscc-p1-4-explicit-state-machine-kernel-implementation-with-p1-3-terminal-commit-1.md`;
- `.aiassistant/records/aiscc/cycles/20260827_2109_aiscc-p1-4-preflight-terminal-state-persistence-conflict-1.cycle.md`;
- all exact 55 accepted P1-3 implementation paths;
- `.aiassistant/tasks/done/20260828_0928_aiscc-p1-4-explicit-state-machine-kernel-resume-with-direct-canonical-placement-1.md`.

The ignored bootstrap repair ZIP is temporary and may be deleted after successful Stage 0 commit.

If P1-4 implementation proceeds, preserve all changed P1-4 source/test/migration/build candidate
paths until Command Center/Human judgment.

---

# next action after P1-4 Human acceptance

```text
P1-5 Agent Provider and Tool Execution
```

Do not execute P1-5 in this Task.
