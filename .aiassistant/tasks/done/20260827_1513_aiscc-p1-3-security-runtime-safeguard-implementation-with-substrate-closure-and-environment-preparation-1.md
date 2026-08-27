# 작업지시서: P1-3 Security / Runtime Safeguard Implementation with Runtime-Substrate Closure and Environment Preparation

## meta

- task_id: `20260827_1513_aiscc-p1-3-security-runtime-safeguard-implementation-with-substrate-closure-and-environment-preparation-1`
- created_at: `2026-08-27 15:13 KST`
- phase: `P1-3 — Security / Runtime Safeguard Implementation and Verification`
- work_type: `SECURITY_SANDBOX_IMPLEMENTATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `accepted runtime-substrate persistence → authorized environment/bootstrap → executable P1-2 safeguard implementation + runtime proof`
- predecessor_runtime_substrate_task: `20260827_1442_aiscc-p1-3-runtime-substrate-baseline-design-with-blocker-provenance-commit-1`
- predecessor_runtime_substrate_result: `HUMAN_PROVIDED / ACCEPTED`
- predecessor_base_commit: `95de4ae9d5ec36bed8636b608dc5729b47e815fe`
- runtime_substrate_decision: `AISCC-P1-3-RUNTIME-SUBSTRATE-V1`
- runtime_substrate_terminal_cycle: `.aiassistant/records/aiscc/cycles/20260827_1513_aiscc-p1-3-runtime-substrate-baseline-final-acceptance-1.cycle.md`
- P1_3_safeguard_status_before: `NOT_STARTED`
- P1_4_status: `NOT_STARTED`
- public_live_release_status: `BLOCKED_UNTIL_P1_3_ACCEPTED`

---

# 0. sole execution contract

This Task is the only active P1-3 safeguard implementation contract after Human acceptance of
`AISCC-P1-3-RUNTIME-SUBSTRATE-V1`.

Do not resume older blocked/superseded P1-3 Tasks as parallel contracts.

Preserve all prior done Tasks/Cycles as provenance.

---

# 1. Human preparation

Human performs only:

1. apply the Command Center package:

```text
20260827_1513_aiscc-p1-3-runtime-substrate-terminal-acceptance-canonical-persistence-1.zip
```

to repository root;

2. place this Task at:

```text
.aiassistant/tasks/active/20260827_1513_aiscc-p1-3-security-runtime-safeguard-implementation-with-substrate-closure-and-environment-preparation-1.md
```

3. start a fresh Executor chat.

Human does NOT create the runtime-substrate closure commit.
Human does NOT install Python/uv manually unless this Task stops with an exact environment blocker.

The Executor owns:

```text
Stage 0
accepted runtime-substrate terminal persistence local commit

→ Stage 1
authorized environment preparation

→ Stage 2
exact runtime bootstrap + dependency lock

→ Stage 3
P1-3 safeguard implementation

→ Stage 4
targeted + non-substitutable runtime evidence

→ report/export
```

Only the Stage 0 provenance commit is authorized.
P1-3 implementation remains uncommitted for Command Center/Human review.

---

# Stage 0 — accepted runtime-substrate terminal Git persistence

## expected repository identity

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

expected HEAD before substrate closure commit:
95de4ae9d5ec36bed8636b608dc5729b47e815fe
```

If HEAD differs:

```text
STOP
→ BLOCKED_PREDECESSOR_HEAD_DRIFT
```

Do not reinterpret another commit as equivalent.

## allowed closure/provenance universe

The actual tracked dirty set does NOT need an exact count.

It MUST be a subset of:

```text
.aiassistant/tasks/done/20260827_1442_aiscc-p1-3-runtime-substrate-baseline-design-with-blocker-provenance-commit-1.md

.aiassistant/rules/AISCC_RUNTIME_SUBSTRATE.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/records/aiscc/cycles/20260827_1513_aiscc-p1-3-runtime-substrate-baseline-final-acceptance-1.cycle.md
```

Ignored current active Task / target export does not count.

Rules:

```text
tracked dirty path outside allowlist
→ STOP
→ BLOCKED_RUNTIME_SUBSTRATE_CLOSURE_COLLISION

allowlisted path already clean
→ not a blocker

missing terminal canonical file
→ repair/create only from Human acceptance + terminal Cycle + accepted candidate semantics
```

Do not reset/stash/clean unrelated work.

## terminal file integrity

After Human package application or Executor-authorized narrow repair, expected Command Center file
hashes are:

```text
.aiassistant/rules/AISCC_RUNTIME_SUBSTRATE.md
sha256:
<verify against Task report; Command Center package authoritative>

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
sha256:
<verify against Task report; Command Center package authoritative>

.aiassistant/records/aiscc/DECISION_REGISTER.md
sha256:
<verify against Task report; Command Center package authoritative>

.aiassistant/records/aiscc/NEXT_ACTIONS.md
sha256:
<verify against Task report; Command Center package authoritative>

.aiassistant/records/aiscc/cycles/20260827_1513_aiscc-p1-3-runtime-substrate-baseline-final-acceptance-1.cycle.md
sha256:
<verify against Task report; Command Center package authoritative>
```

Do not fail merely because a Browser-side generated hash was not copied into this Task text.
Read the actual terminal Cycle and semantic terminal metadata and report the current hashes.

Required semantics:

```text
AISCC-P1-3-RUNTIME-SUBSTRATE-V1
→ HUMAN_PROVIDED / ACCEPTED

P1-3 safeguard implementation
→ READY / NOT_STARTED

P1-4
→ NOT_STARTED
```

## Stage 0 preflight

Before Git index mutation:

1. verify repository/branch/HEAD;
2. inspect `git status --short`;
3. verify dirty subset is inside the allowlist;
4. read the accepted runtime-substrate rule;
5. read exact terminal Cycle;
6. verify done Task exact `task_id`;
7. run `git diff --check`;
8. verify no secret/private material;
9. verify current active Task is this Task.

If semantic terminal metadata is missing/mismatched only in the five Command Center package files,
narrowly repair those files from accepted provenance.

Do NOT redesign the substrate.

## authorized local commit

Exactly one local commit is authorized before environment/bootstrap implementation.

Stage explicit changed allowlisted paths only.

Forbidden:

```text
git add .
git add -A
git commit -a
git amend
git reset
git stash
git clean
git fetch
git pull
git push
branch/tag/remote mutation
```

Exact commit message:

```text
docs: accept P1-3 runtime substrate baseline

Persist the Human-accepted AISCC runtime, build, source-layout and
sandbox-evidence substrate.

Resolve the P1-3 runtime-substrate blocker and authorize the next
safeguard implementation to prepare Python/uv, create only the accepted
bootstrap, and produce runtime evidence without starting P1-4.
```

Before commit:

```text
git diff --cached --check
git diff --cached --name-status
```

After commit:

```text
P1_3_IMPLEMENTATION_BASE_COMMIT=<new full hash>
```

Verify:

- parent is `95de4ae9d5ec36bed8636b608dc5729b47e815fe`;
- commit path set is within the exact closure/provenance allowlist;
- tracked worktree clean;
- index empty;
- no remote operation.

If fail:

```text
STOP
→ BLOCKED_RUNTIME_SUBSTRATE_CLOSURE_COMMIT_INVALID
```

After this commit, Git authorization is exhausted:

```text
git add / commit / push
→ FORBIDDEN
```

All implementation changes remain uncommitted review candidates.

---

# Stage 1 — authorized environment preparation

Human has accepted:

```text
Python / CPython 3.12.x
uv
Docker Engine Linux containers
Docker Compose v2
```

At substrate-design time:

```text
usable Python 3.12: absent
uv: absent
Docker Engine: available
Docker Compose v2: available
```

This Task explicitly authorizes environment preparation for P1-3.

## environment policy

Preferred Windows preparation path:

1. probe `winget --version`;
2. if available, verify exact package identity for `uv` through configured Winget source;
3. install `uv` in user scope where supported;
4. use `uv` managed-Python support to install a current compatible CPython `3.12.x`;
5. record exact `uv` version and Python patch;
6. do not replace system-wide Python association or modify unrelated global development tools.

The Task authorizes network only for:

```text
- configured Winget source needed to obtain uv;
- uv-managed CPython 3.12 distribution acquisition;
- Python package registry resolution/download for the exact P1-3 manifest;
- Docker registry pull for exact P1-3 base image(s);
```

Forbidden network purpose:

```text
provider/LLM API
arbitrary web browsing
external repository ingestion
deployment
credential service
production database
unrelated package installation
```

If Winget/uv bootstrap cannot be completed without admin/system-wide mutation or an unapproved
installer path:

```text
STOP
→ HUMAN_ENVIRONMENT_PREPARATION_REQUIRED
```

Do not switch to Node fallback automatically.
Fallback requires separate Human-accepted substrate baseline update.

## environment verification

Required:

```text
uv --version
uv python list / equivalent
managed Python 3.12 exact patch
docker --version
docker compose version
docker info
```

Verify Docker is in Linux-container mode.

Installed tool availability is still not security proof.

---

# Stage 2 — exact accepted runtime bootstrap

## creation authority

Create ONLY section 11 allowlisted paths from:

`.aiassistant/rules/AISCC_RUNTIME_SUBSTRATE.md`

Exact roots:

```text
.python-version
pyproject.toml
uv.lock
.dockerignore
src/aiscc/
tests/
config/security/
containers/p1_3/
```

Exact application/interface files:

```text
src/aiscc/__init__.py
src/aiscc/__main__.py
src/aiscc/bootstrap.py
src/aiscc/api/__init__.py
src/aiscc/api/app.py
src/aiscc/api/routes/__init__.py
src/aiscc/api/routes/health.py
src/aiscc/api/routes/control.py
src/aiscc/contracts/__init__.py
src/aiscc/contracts/workflow.py
src/aiscc/contracts/security.py
```

Exact security/runtime files:

```text
src/aiscc/security/__init__.py
src/aiscc/security/models.py
src/aiscc/security/policy.py
src/aiscc/security/action_state.py
src/aiscc/security/capability.py
src/aiscc/security/cancel.py
src/aiscc/security/limits.py
src/aiscc/security/provenance.py
src/aiscc/security/redaction.py
src/aiscc/runtime/__init__.py
src/aiscc/runtime/contracts.py
src/aiscc/runtime/process.py
src/aiscc/runtime/docker.py
src/aiscc/runtime/network.py
src/aiscc/runtime/cleanup.py
```

Exact non-secret config/container files:

```text
config/security/permission-profiles.v1.toml
config/security/resource-policy.v1.toml
config/security/limits.v1.toml
containers/p1_3/Dockerfile.sandbox
containers/p1_3/Dockerfile.evidence
containers/p1_3/compose.yaml
```

Exact tests/fixtures:

```text
tests/conftest.py
tests/unit/security/test_permission_policy.py
tests/unit/security/test_action_state_eligibility.py
tests/unit/security/test_public_cancel_authorization.py
tests/unit/security/test_capability_lifetime.py
tests/unit/security/test_limits_idempotency_budget.py
tests/integration/security/test_broker_fail_closed.py
tests/integration/security/test_provenance_redaction.py
tests/runtime/security/test_sandbox_isolation.py
tests/runtime/security/test_network_boundary.py
tests/runtime/security/test_secret_non_exposure.py
tests/runtime/security/test_timeout_retry_cancel.py
tests/runtime/security/test_idempotency_abuse_budget.py
tests/runtime/security/test_cleanup_residue.py
tests/runtime/security/test_failure_domain.py
tests/runtime/security/test_action_state_cancel_authorization.py
tests/fixtures/sandbox/allowed/input.txt
tests/fixtures/sandbox/probe.py
tests/fixtures/network/fixture_server.py
```

Do NOT create:

```text
src/aiscc/workflow/
src/aiscc/providers/
src/aiscc/persistence/
database migrations
deployment files
actual public scenario corpus
```

If an implementation requires another path:

```text
STOP
→ EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

## Python pin

Use the exact installed compatible CPython `3.12.x` patch and write it to:

```text
.python-version
```

Do not widen to 3.13.

## manifest/build boundary

Create `pyproject.toml` consistent with the accepted baseline:

```text
requires-python >=3.12,<3.13
Hatchling build backend
aiscc console entrypoint
FastAPI
Pydantic v2
Uvicorn
pytest
Ruff
mypy strict
```

Add only dependencies actually required by the exact implementation/tests.

Additional helper dependency is allowed only when:

- it is necessary for the accepted P1-3 bootstrap/proof;
- reason is recorded;
- it does not absorb P1-4/P1-5;
- dependency source/license/advisory is reviewed at the level available through authorized package metadata;
- it is locked in `uv.lock`.

Do not add SQLAlchemy/asyncpg/Alembic merely because they are future persistence direction unless
current P1-3 code actually needs them. P1-3 must not create persistence implementation.

Generate and review:

```text
uv.lock
```

Use frozen sync after lock generation.

Record exact resolved versions in report.

## container base image

P1-3 may select a compatible CPython 3.12 Linux slim/minimal base needed for the accepted Docker
sandbox/evidence runtime.

Requirements:

- resolve actual image digest;
- bind proof report to the exact digest;
- prefer non-EOL supported image;
- no shell/runtime image selected merely for convenience;
- no privileged container;
- do not claim image digest selection as isolation proof.

If Docker pull requires authentication or registry policy outside normal anonymous/public image
access:

```text
STOP
→ BLOCKED_REQUIRED_EVIDENCE
```

Do not create registry credentials.

---

# Stage 3 — P1-3 security safeguard implementation

## accepted authority inputs

P1-1:

```text
AgentOutput != SystemState
EvidenceCandidate != AdmittedEvidence
HumanGateStatus != HumanResult
HumanResult != Judgment
Judgment != TransitionDecision
TransitionDecision != WorkflowState
RuntimeMode != WorkflowState
```

P1-2:

```text
SecurityAdmissionDecision = ALLOW | DENY
unknown / ambiguous → DENY

fresh state_version
!= action admissible

PUBLIC_RUN_OR_REPLAY_VISIBILITY
!= PUBLIC_CANCEL_AUTHORITY

RUN_ID_KNOWLEDGE
!= TARGET_RUN_CONTROL_AUTHORIZATION
```

Runtime substrate:

```text
SecurityAdmissionDecision
!= TransitionDecision

security test state fixture
!= P1-4 state-machine kernel
```

## implementation boundary

Implement:

```text
security policy
→ consumes immutable WorkflowSnapshot/state_version
→ ALLOW / DENY + reason/provenance

runtime adapter
→ consumes admitted short-lived capability
→ executes bounded operation / cleanup
→ returns outcome/event/evidence candidate
```

Do NOT implement a mutable authoritative workflow aggregate or transition engine.

## required safeguards

### A. RuntimeMode permission profiles

Implement versioned profiles for:

```text
OWNER_SELF_DOGFOOD
PUBLIC_RECORDED_REPLAY
PUBLIC_BOUNDED_LIVE
```

Public Replay:

```text
NO LLM inference
NO source mutation
NO shell/process
NO outbound network
NO tool/provider side effect
```

Public Live:

```text
fixed synthetic repository only
allowlisted scenario only
server-fixed provider/model reference only
finite calls/retry/time/budget
no free-form task
no external repository/upload
no arbitrary shell/network
no owner/private workspace access
```

No provider API call is required or allowed in P1-3.

### B. exact SecurityActionClass

Implement accepted exact action classes:

```text
START_EXECUTION_CONTROL
RUN_EXECUTION_SIDE_EFFECT
RUN_REVIEW_READ_ONLY
PUBLIC_CANCEL_CONTROL
ADMINISTRATIVE_TERMINATE_CONTROL
REWORK_START_CONTROL
BLOCKER_RECOVERY_CHECK
SAFETY_CLEANUP_REVOKE_QUARANTINE
RECOVERY_RECONCILIATION
SYSTEM_DURABLE_PROVENANCE
REPLAY_READ_ONLY
```

Unknown class → fail-closed DENY.

### C. action × WorkflowState admission

Implement exact P1-2 matrix.

Minimum:

```text
RUN_EXECUTION_SIDE_EFFECT
→ RUNNING only
```

Fresh version alone is insufficient.

### D. state/version capability lifetime

Capability/permission must bind to:

```text
run ref
state
state_version
policy/profile version
action/resource scope
expiry/revocation
```

Any relevant state/version change requires revalidation.

Terminal state must not preserve normal execution/provider capability use solely because lease time
remains.

### E. deny-by-default resources

Implement policy boundary for:

```text
filesystem
process/shell
tool
outbound network
secret/credential
repository/worktree
provider
scenario/action
```

Unknown/unmatched → DENY.

Agent prose cannot grant capability.

### F. public cancel target authorization

Implement exact `PublicRunControlGrant`-equivalent semantics.

Required deny:

```text
run/replay visible only
run_id known only
session/principal mismatch
expired grant
revoked grant
wrong target
wrong action
wrong mode/profile
stale target state/version
```

Repeated authorized cancel must create one logical cancel intent.

Cancel admission does not directly mutate authoritative WorkflowState.

### G. secret-safe capability/provenance

No raw secret in:

```text
policy model
argv
environment dump
log
decision provenance
evidence body
Replay
```

Use synthetic ephemeral canary for tests, never a real credential.

Public profiles cannot select/request credentials.

### H. timeout/retry/cancel

Finite timeout.
Finite retry.
Explicit cancel.
No unbounded loops.
Timeout/failure cannot be reported as successful execution.

### I. idempotency/abuse/budget

Implement application-side primitives proving:

- duplicate request identity does not duplicate operation;
- limit/budget exhausted → deny before simulated paid/provider side effect;
- finite quota window/limit semantics;
- abuse/throttle unknown condition fails closed.

Do not claim provider hard-spend limit configured.

### J. cleanup/residue/quarantine

For run-owned Docker/process/filesystem resources:

```text
success
failure
cancel
timeout
→ deterministic cleanup

unresolved residue
→ residue record
→ quarantine/failure
!= clean success
```

No Docker socket inside untrusted container.

---

# Stage 4 — mandatory verification

## source/build integrity

Run at minimum:

```text
uv sync --frozen
uv build
uv run ruff check .
uv run ruff format --check .
uv run mypy --strict src tests
uv run pytest -q
```

If exact command needs a baseline-compatible minor adjustment, report it; do not disable checks
merely to pass.

## TARGETED_TEST

All P1-3 changed safeguard logic must have deterministic tests.

## ACTION_STATE_CANCEL_AUTHORIZATION_RUNTIME

Prove all seven:

1. wrong WorkflowState action → DENY;
2. prior capability after state/version transition → stale/revoked DENY;
3. terminal state normal execution/provider side effect → DENY;
4. blocked/terminal safety cleanup can settle an existing resource without opening new normal execution;
5. public session A cannot cancel session B's run;
6. Replay/read/run-ID visibility alone cannot cancel;
7. repeated authorized cancel is idempotent and creates one logical control effect.

## FILESYSTEM_PROCESS_ISOLATION_RUNTIME

Must be actual Docker/process/filesystem evidence, not policy-unit proof.

At minimum:

- exact allowed workspace/input accessible;
- sibling run/private repository/host-forbidden target not mounted/reachable;
- run-scoped process/resource identity;
- bounded process/container;
- cleanup observed.

## NETWORK_RUNTIME

Use local isolated Docker fixtures only.

Required:

```text
default deny
→ no outbound network

explicit test allow
→ exact P1-3 internal Docker network
→ exact local fixture only

unlisted target
→ denied/unreachable
```

Do NOT call public internet from the sandbox runtime proof.

Package/image acquisition network from Stage 1/2 is environment preparation and NOT this proof.

## SECRET_NON_EXPOSURE

Use synthetic ephemeral canary.

Verify canary does not appear in:

- logs;
- structured provenance;
- exported evidence;
- argv capture;
- environment dump produced by test harness;
- Replay-style public artifact if one is created for test.

Do not use real secret.

## TIMEOUT_RETRY_CANCEL_RUNTIME

Prove:

- deterministic timeout;
- finite retry count;
- cancellation stops/settles applicable resource;
- failure does not become success.

## IDEMPOTENCY_ABUSE_BUDGET_RUNTIME

Prove:

- duplicate identity → no duplicate operation;
- budget/limit exceeded → deny before simulated paid action;
- throttle/abuse tested fail-closed.

## CLEANUP_RESIDUE_RUNTIME

Prove cleanup on:

```text
success
failure
cancel
timeout
```

Include at least one controlled residue/quarantine case if safely synthesizable.

## FAILURE_DOMAIN

Prove at implementation/test level:

```text
simulated Live/provider/budget unavailable
→ Recorded Replay/read-only path remains independently available
```

This is not public deployment proof.

---

# evidence admission rules

## executor_required

- `RUNTIME_SUBSTRATE_CLOSURE_GIT`
- `ENVIRONMENT_PREPARATION`
- `RUNTIME_BOOTSTRAP`
- `STATIC_SOURCE`
- `BUILD_STATIC_TYPE`
- `TARGETED_TEST`
- `ACTION_STATE_CANCEL_AUTHORIZATION_RUNTIME`
- `FILESYSTEM_PROCESS_ISOLATION_RUNTIME`
- `NETWORK_RUNTIME`
- `SECRET_NON_EXPOSURE`
- `TIMEOUT_RETRY_CANCEL_RUNTIME`
- `IDEMPOTENCY_ABUSE_BUDGET_RUNTIME`
- `CLEANUP_RESIDUE_RUNTIME`
- `FAILURE_DOMAIN`

## human_owned

`HUMAN_VERIFICATION`

Human reviews:

- closure commit;
- installed exact Python/uv versions;
- manifest/lock dependency set;
- implementation paths;
- Docker/base-image digest and constraints;
- all runtime evidence;
- any residue/quarantine;
- security invariant drift;
- whether P1-3 may be accepted before P1-4.

Expected:

```text
ACCEPTED
HOLD_REWORK_REQUIRED
or exact correction
```

## not_required

- production provider call;
- real OpenAI API;
- production PostgreSQL;
- public cloud deployment;
- provider billing/hard-spend configuration;
- browser visual QA;
- competition submission.

## forbidden

- second Git commit;
- Git push/remote mutation;
- Node fallback without new Human baseline;
- P1-4/P1-5 implementation;
- real credential use;
- provider/LLM call;
- deployment;
- Browser Project Source mutation.

---

# proof non-substitution

```text
environment installed
!= safeguard implemented

uv.lock
!= security proof

unit test
!= Docker isolation proof

mock network deny
!= Docker network runtime proof

Docker installed
!= isolation proof

container exits
!= cleanup success

opaque secret unit test
!= production secret-manager proof

application budget
!= provider spend cap configured

security ALLOW/DENY
!= WorkflowState TransitionDecision

test WorkflowSnapshot
!= P1-4 state-machine kernel
```

---

# mandatory stop

Stop with exact blocker and minimal report/export if:

- predecessor HEAD/closure dirty set conflicts;
- runtime-substrate closure commit cannot be created safely;
- Git identity missing;
- uv/Python environment preparation requires admin or unapproved installer path;
- dependency resolution requires an unapproved package/source;
- Docker Engine/Linux mode unavailable;
- exact container proof requires privileged mode, host Docker socket inside untrusted container, or broad host mounts;
- real credential/provider access becomes necessary;
- required evidence needs a path outside accepted bootstrap;
- P1-1/P1-2 semantics conflict;
- P1-4/P1-5 scope expansion becomes necessary;
- secret/private material is encountered.

Possible named results include:

```text
BLOCKED_RUNTIME_SUBSTRATE_CLOSURE_COMMIT_INVALID
HUMAN_ENVIRONMENT_PREPARATION_REQUIRED
BLOCKED_DEPENDENCY_RESOLUTION
BLOCKED_REQUIRED_EVIDENCE
EVIDENCE_SCOPE_EXPANSION_REQUIRED
POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

Do not weaken the accepted baseline to avoid a blocker.

---

# Git policy after Stage 0

After the one authorized substrate-closure commit:

```text
git add
git commit
git push
remote operation
→ FORBIDDEN
```

P1-3 runtime/source/test/config changes remain uncommitted for review.

---

# report required fields

- task id/path;
- old HEAD;
- substrate closure dirty inventory;
- exact staged closure paths;
- closure commit message;
- full `P1_3_IMPLEMENTATION_BASE_COMMIT`;
- post-commit clean evidence;
- no remote operation;
- environment preparation commands/purpose;
- exact uv version;
- exact Python 3.12 patch;
- Docker/Compose versions and Linux mode;
- exact network sources used for environment/dependency/image acquisition;
- `.python-version` value;
- `pyproject.toml` dependency list/reasons;
- `uv.lock` hash;
- exact resolved dependency versions;
- container base tags + resolved digests;
- exact created/modified implementation paths;
- accepted bootstrap allowlist conformance;
- build/lint/type/test evidence;
- every runtime proof classification + artifact;
- Agent claim vs admitted evidence;
- blocked evidence if any;
- Human pending;
- forbidden-not-run;
- mandatory stop/scope expansion;
- rollback/uninstall/revert guidance;
- preserved exact paths;
- next recommendation.

---

# export bundle

Target:

```text
.aiassistant/reports/target/20260827_1513_aiscc-p1-3-security-runtime-safeguard-implementation-with-substrate-closure-and-environment-preparation-1/
```

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- all changed P1-3 runtime/source/test/config/container files preserving repository-relative paths
- `REMOVED_FILES.md` only when actual deletion occurred
- compact non-secret runtime evidence/logs required for Command Center review

Do not export package caches, Python installation, `.venv`, Docker image layers, credentials, or
unrelated runtime residue.

---

# Task lifecycle

When executor-required work/report/export completes or an exact mandatory blocker is safely
established:

```text
.aiassistant/tasks/active/20260827_1513_aiscc-p1-3-security-runtime-safeguard-implementation-with-substrate-closure-and-environment-preparation-1.md
→
.aiassistant/tasks/done/20260827_1513_aiscc-p1-3-security-runtime-safeguard-implementation-with-substrate-closure-and-environment-preparation-1.md
```

`done` means submitted, not Human accepted.

---

# preserved artifacts

Always preserve:

- `.aiassistant/rules/AISCC_RUNTIME_SUBSTRATE.md`
- `.aiassistant/tasks/done/20260827_1442_aiscc-p1-3-runtime-substrate-baseline-design-with-blocker-provenance-commit-1.md`
- `.aiassistant/records/aiscc/cycles/20260827_1513_aiscc-p1-3-runtime-substrate-baseline-final-acceptance-1.cycle.md`
- the one local runtime-substrate closure commit created by this Task
- `.aiassistant/tasks/done/20260827_1513_aiscc-p1-3-security-runtime-safeguard-implementation-with-substrate-closure-and-environment-preparation-1.md`

If implementation proceeds, preserve changed P1-3 source/tests/config/container files until
Command Center/Human judgment.

Environment installations/caches and Docker image layers are not repository artifacts and are not
preservation targets.

---

# next action after P1-3 Human acceptance

```text
P1-4 Explicit State Machine Kernel Implementation
```

Do not execute P1-4 in this Task.
