# 작업지시서: P1-3 Security / Runtime Safeguard Implementation with Additive Commit Recovery

## meta

- task_id: `20260827_1545_aiscc-p1-3-security-runtime-safeguard-implementation-with-additive-commit-recovery-1`
- created_at: `2026-08-27 15:45 KST`
- phase: `P1-3 — Security / Runtime Safeguard Implementation and Verification`
- work_type: `SECURITY_SANDBOX_IMPLEMENTATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `additive Git provenance recovery → environment/bootstrap → executable security safeguard + runtime evidence`
- predecessor_task: `20260827_1513_aiscc-p1-3-security-runtime-safeguard-implementation-with-substrate-closure-and-environment-preparation-1`
- predecessor_result: `BLOCKED_RUNTIME_SUBSTRATE_CLOSURE_COMMIT_INVALID`
- predecessor_commit: `a8797fdac43b4a8bc501ccdb3c86743541153319`
- predecessor_parent: `95de4ae9d5ec36bed8636b608dc5729b47e815fe`
- blocker_cycle: `.aiassistant/records/aiscc/cycles/20260827_1545_aiscc-p1-3-runtime-substrate-closure-commit-message-blocker-1.cycle.md`
- accepted_runtime_substrate: `AISCC-P1-3-RUNTIME-SUBSTRATE-V1`
- P1_3_safeguard_status_before: `NOT_STARTED`
- P1_4_status: `NOT_STARTED`

---

# 0. sole execution contract / recovery policy

This Task supersedes the blocked predecessor for execution.

The previous commit:

```text
a8797fdac43b4a8bc501ccdb3c86743541153319
```

MUST remain in history.

It has correct parent/content/path inventory and only an exact-message encoding defect.

History rewrite is forbidden.

```text
git amend
git reset
git rebase
commit recreation
force update
→ FORBIDDEN
```

Recovery is additive only.

---

# Stage 0 — additive corrective provenance commit

## expected repository identity

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

HEAD:
a8797fdac43b4a8bc501ccdb3c86743541153319
```

If HEAD differs:

```text
STOP
→ BLOCKED_PREDECESSOR_HEAD_DRIFT
```

## expected tracked dirty provenance

The completed predecessor Task should now be durable as a done Task, and Human/Command Center
provides the blocker Cycle.

Allowed tracked dirty set:

```text
.aiassistant/tasks/done/20260827_1513_aiscc-p1-3-security-runtime-safeguard-implementation-with-substrate-closure-and-environment-preparation-1.md

.aiassistant/records/aiscc/cycles/20260827_1545_aiscc-p1-3-runtime-substrate-closure-commit-message-blocker-1.cycle.md
```

Rules:

```text
tracked dirty path outside these two paths
→ STOP
→ BLOCKED_CORRECTIVE_PROVENANCE_COLLISION

one allowed path already clean/tracked
→ stage only actual dirty member
→ explain

both paths absent/unavailable
→ STOP
→ BLOCKED_CORRECTIVE_PROVENANCE_MISSING
```

Ignored current active Task / target export are not commit inputs.

## Stage 0 preflight

Before Git index mutation:

1. verify repository root;
2. verify branch `main`;
3. verify HEAD exact;
4. inspect `git status --short`;
5. verify dirty tracked subset;
6. read predecessor done Task and exact `task_id`;
7. read blocker Cycle and exact `cycle_id`;
8. inspect `git show -s --format=fuller a8797fda...`;
9. verify parent of `a8797fda...`;
10. verify the prior commit path inventory contains only its six authorized substrate-closure paths;
11. run `git diff --check`;
12. verify no secret/private material;
13. verify current active Task is this Task.

Do not modify canonical P1-1/P1-2/runtime-substrate files in Stage 0.

## exact recovery semantics to preserve

The corrective provenance MUST state:

```text
a8797fdac43b4a8bc501ccdb3c86743541153319

intended semantic purpose:
accept/persist AISCC-P1-3-RUNTIME-SUBSTRATE-V1

actual content:
valid accepted runtime-substrate canonical/provenance

known defect:
commit message contains literal PowerShell `n text instead of intended line breaks

history policy:
preserve commit; no amend/reset/rebase

P1-3 safeguard implementation at that commit:
NOT_STARTED
```

The blocker Cycle is the canonical detailed recovery record.

## authorized Git operations

Exactly one additive local provenance commit is authorized.

Allowed:

```text
git add -- <explicit actual changed allowed provenance paths>
git diff --cached --check
git diff --cached --name-status
git status --short
git commit
git rev-parse HEAD
git show --name-status --stat <new-head>
```

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

If Git identity is unavailable:

```text
STOP
→ HUMAN_GIT_IDENTITY_REQUIRED
```

## exact corrective commit message

Use this exact message:

```text
docs: record P1-3 substrate closure message correction

Preserve the content-valid runtime-substrate closure commit with its
known PowerShell newline-encoding defect.

Record the intended Human-accepted substrate semantics additively,
without rewriting history, and resume P1-3 safeguard implementation
from the corrected provenance head.
```

Important implementation note:

- construct the multi-line commit message using a method that preserves real line breaks;
- PowerShell single-quoted `` `n `` text MUST NOT be used as a newline mechanism;
- recommended safe method: create a temporary UTF-8 no-BOM message file outside repository or in
  an ignored temp location and use `git commit -F <message-file>`;
- delete the temporary message file after commit;
- the temporary message file is not a repository artifact.

## Stage 0 acceptance gate

After commit:

```text
P1_3_IMPLEMENTATION_BASE_COMMIT=<new full hash>
```

Verify:

1. parent == `a8797fdac43b4a8bc501ccdb3c86743541153319`;
2. commit path inventory contains only allowed provenance path(s);
3. `git show -s --format=%B <new-head>` exactly equals the required message including real line breaks;
4. no literal backtick-plus-`n` encoding defect;
5. tracked worktree clean;
6. index empty;
7. no remote operation.

If any check fails:

```text
STOP
→ BLOCKED_CORRECTIVE_PROVENANCE_COMMIT_INVALID
```

After this commit:

```text
git add
git commit
git push
remote operation
→ FORBIDDEN
```

P1-3 implementation stays uncommitted for review.

---

# Stage 1 — accepted environment preparation

Accepted canonical substrate:

```text
Python / CPython 3.12.x
requires-python >=3.12,<3.13

FastAPI
Pydantic v2
Uvicorn

uv
Hatchling

src/aiscc/
tests/
config/security/
containers/p1_3/

Docker Engine Linux containers
Docker Compose v2
```

At substrate-design time:

```text
usable CPython 3.12:
absent

uv:
absent

Docker Engine / Linux containers:
available

Docker Compose v2:
available
```

This Task authorizes environment preparation.

## environment installation policy

Preferred Windows path:

1. probe `winget --version`;
2. verify exact `uv` package identity through configured Winget source;
3. install `uv` without unrelated global tool mutation;
4. use `uv` managed Python support to acquire current compatible CPython `3.12.x`;
5. record exact `uv` version and Python patch;
6. do not replace system-wide Python association or alter unrelated SDKs.

Allowed network purposes:

```text
configured Winget source for uv
uv-managed CPython distribution acquisition
Python package registry for exact P1-3 dependencies
Docker registry for exact P1-3 base images
```

Forbidden network purposes:

```text
OpenAI/provider/LLM API
arbitrary browsing
external repository ingestion
deployment
credential services
production DB
unrelated package installs
```

If preparation requires an unapproved admin/system-wide installer path:

```text
STOP
→ HUMAN_ENVIRONMENT_PREPARATION_REQUIRED
```

Do not automatically switch to Node fallback.

## environment verification

Record:

```text
uv --version
managed CPython exact 3.12.x patch
docker --version
docker compose version
docker info / Linux-container mode
```

Installed tool availability is not security proof.

---

# Stage 2 — exact accepted runtime bootstrap

Create ONLY the Human-accepted bootstrap allowlist from
`.aiassistant/rules/AISCC_RUNTIME_SUBSTRATE.md`.

Required roots/files include:

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

Required exact application/contracts:

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

Required security/runtime:

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

Required config/container:

```text
config/security/permission-profiles.v1.toml
config/security/resource-policy.v1.toml
config/security/limits.v1.toml

containers/p1_3/Dockerfile.sandbox
containers/p1_3/Dockerfile.evidence
containers/p1_3/compose.yaml
```

Required tests/fixtures:

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

Forbidden bootstrap:

```text
src/aiscc/workflow/
src/aiscc/providers/
src/aiscc/persistence/
database migrations
deployment files
actual public scenario corpus
```

If another repository path becomes necessary:

```text
STOP
→ EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

## Python/build

Use exact installed compatible CPython `3.12.x`.

Write exact patch to `.python-version`.

`pyproject.toml` must preserve:

```text
requires-python >=3.12,<3.13
Hatchling
aiscc console entrypoint
FastAPI
Pydantic v2
Uvicorn
pytest
Ruff
mypy strict
```

Add only dependencies actually required by P1-3 implementation/proof.

Do not add persistence dependencies unless current P1-3 code actually requires them; no
persistence implementation is authorized.

Generate:

```text
uv.lock
```

and use frozen sync after lock generation.

Record exact dependency versions/reasons.

## Docker image

Select compatible CPython 3.12 Linux minimal/slim base as needed.

Record:

- tag;
- resolved digest;
- purpose.

No privileged container.
No Docker socket inside untrusted container.
No broad host mount.

If registry authentication is required:

```text
STOP
→ BLOCKED_REQUIRED_EVIDENCE
```

Do not create credentials.

---

# Stage 3 — safeguard implementation

## accepted authority invariants

```text
SecurityAdmissionDecision = ALLOW | DENY

SecurityAdmissionDecision
!= TransitionDecision

fresh state_version
!= action admissible

RuntimeMode
!= WorkflowState

PUBLIC_RUN_OR_REPLAY_VISIBILITY
!= PUBLIC_CANCEL_AUTHORITY

RUN_ID_KNOWLEDGE
!= TARGET_RUN_CONTROL_AUTHORIZATION

security test state fixture
!= P1-4 workflow kernel
```

## A. RuntimeMode profiles

Implement:

```text
OWNER_SELF_DOGFOOD
PUBLIC_RECORDED_REPLAY
PUBLIC_BOUNDED_LIVE
```

Public Replay:

```text
NO inference
NO source mutation
NO process/shell
NO outbound network
NO tool/provider side effect
```

Public Live:

```text
fixed synthetic repository only
allowlisted scenario only
server-fixed provider/model reference only
finite call/retry/time/budget
no free-form task
no external repo/upload
no arbitrary shell/network
no owner/private workspace
```

No provider API call in P1-3.

## B. exact SecurityActionClass

Implement:

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

Unknown → DENY.

## C. action × WorkflowState

Implement exact accepted matrix.

Minimum:

```text
RUN_EXECUTION_SIDE_EFFECT
→ RUNNING only
```

Version freshness alone is insufficient.

## D. capability lifetime

Capability binds to:

```text
run ref
state
state_version
profile/policy version
action/resource scope
expiry/revocation
```

Relevant state/version change requires revalidation.

Terminal state cannot preserve normal execution/provider capability merely because lease remains.

## E. deny-by-default resources

Policy domains:

```text
filesystem
process/shell
tool
network
secret/credential
repository/worktree
provider
scenario/action
```

Unknown/unmatched → DENY.

Agent prose cannot grant capability.

## F. public cancel authorization

Implement `PublicRunControlGrant`-equivalent binding.

DENY:

```text
visibility only
run ID only
session/principal mismatch
expired/revoked grant
wrong target/action/mode/profile
stale target state/version
```

Repeated authorized cancel → one logical intent.

Cancel admission does not mutate WorkflowState directly.

## G. secret-safe handling

No raw secret in:

```text
policy model
argv
logs
decision provenance
evidence
Replay-style public artifact
```

Use synthetic ephemeral canary only.

## H. timeout/retry/cancel

Finite timeout.
Finite retry.
Explicit cancellation.
No silent success.
No unbounded loop.

## I. idempotency/abuse/budget

Prove:

- duplicate identity does not duplicate operation;
- exhausted budget/limit denies before simulated paid action;
- finite quota/limit semantics;
- unknown abuse/throttle condition fails closed.

No provider hard-spend configuration claim.

## J. cleanup/residue/quarantine

For run-owned resources:

```text
success/failure/cancel/timeout
→ deterministic cleanup

unresolved residue
→ record + quarantine/failure
!= clean success
```

---

# Stage 4 — mandatory verification

## build/static

Run:

```text
uv sync --frozen
uv build
uv run ruff check .
uv run ruff format --check .
uv run mypy --strict src tests
uv run pytest -q
```

Do not disable checks merely to pass.

## runtime proof — mandatory

### ACTION_STATE_CANCEL_AUTHORIZATION_RUNTIME

Prove all:

1. wrong WorkflowState action → DENY;
2. stale capability after state/version change → DENY/revoke;
3. terminal state normal execution/provider side effect → DENY;
4. blocked/terminal safety cleanup can settle existing resource without opening normal execution;
5. session A cannot cancel session B run;
6. Replay/read/run-ID visibility alone cannot cancel;
7. repeated authorized cancel is idempotent.

### FILESYSTEM_PROCESS_ISOLATION_RUNTIME

Actual Docker/process/filesystem evidence:

- allowed workspace/input accessible;
- sibling/private/host forbidden target not mounted/reachable;
- run-scoped identity;
- bounded process/container;
- cleanup observed.

### NETWORK_RUNTIME

Local isolated Docker fixture only:

```text
default deny → no outbound network
explicit allow → exact P1-3 internal network/local fixture
unlisted target → denied/unreachable
```

No public-internet sandbox proof.

### SECRET_NON_EXPOSURE

Synthetic canary absent from:

- log;
- provenance;
- exported evidence;
- argv capture;
- environment dump produced by harness;
- Replay-style test artifact.

### TIMEOUT_RETRY_CANCEL_RUNTIME

Prove bounded timeout/retry/cancel and no false success.

### IDEMPOTENCY_ABUSE_BUDGET_RUNTIME

Prove duplicate/budget/throttle behavior.

### CLEANUP_RESIDUE_RUNTIME

Prove success/failure/cancel/timeout cleanup and controlled residue/quarantine if safely
synthesizable.

### FAILURE_DOMAIN

Prove simulated Live/provider/budget unavailable does not disable recorded read-only Replay path.

---

# evidence contract

## executor_required

- `CORRECTIVE_PROVENANCE_GIT`
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

- corrective provenance commit;
- exact implementation base commit;
- uv/Python versions;
- manifest/lock;
- source/bootstrap paths;
- image digests/constraints;
- runtime proof;
- residue/quarantine;
- P1-1/P1-2 invariant preservation;
- whether P1-3 may be accepted before P1-4.

Expected:

```text
ACCEPTED
HOLD_REWORK_REQUIRED
or exact correction
```

## forbidden

- history rewrite;
- second Git commit;
- Git push/remote mutation;
- Node fallback;
- P1-4/P1-5 implementation;
- real provider credential/API;
- deployment;
- Browser Project Source mutation.

---

# proof non-substitution

```text
corrective provenance commit
!= P1-3 safeguard acceptance

environment installed
!= safeguard implemented

uv.lock
!= runtime security proof

unit test
!= Docker isolation proof

Docker installed
!= isolation proof

mock network deny
!= Docker network proof

container exit
!= cleanup success

application budget
!= provider spend cap configured

security ALLOW/DENY
!= TransitionDecision
```

---

# mandatory stop

Stop with exact blocker if:

```text
BLOCKED_PREDECESSOR_HEAD_DRIFT
BLOCKED_CORRECTIVE_PROVENANCE_COLLISION
BLOCKED_CORRECTIVE_PROVENANCE_MISSING
BLOCKED_CORRECTIVE_PROVENANCE_COMMIT_INVALID
HUMAN_GIT_IDENTITY_REQUIRED
HUMAN_ENVIRONMENT_PREPARATION_REQUIRED
BLOCKED_DEPENDENCY_RESOLUTION
BLOCKED_REQUIRED_EVIDENCE
EVIDENCE_SCOPE_EXPANSION_REQUIRED
POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

Do not weaken accepted baseline or broaden into P1-4/P1-5.

---

# report required fields

- Task ID/path;
- prior invalid-message commit and exact defect;
- Stage 0 dirty inventory;
- exact staged provenance paths;
- corrective commit message bytes/line validation;
- full `P1_3_IMPLEMENTATION_BASE_COMMIT`;
- post-commit clean evidence;
- no history rewrite/no remote evidence;
- exact environment preparation commands and network purpose;
- exact uv/Python/Docker/Compose versions;
- `.python-version`;
- `pyproject.toml` dependencies/reasons;
- `uv.lock` hash;
- exact resolved versions;
- Docker image tags/digests;
- exact created/modified implementation paths;
- bootstrap allowlist conformance;
- build/lint/type/test results;
- every runtime proof class/result/artifact;
- Agent claim vs admitted evidence;
- Human pending;
- forbidden-not-run;
- blocker/scope expansion if any;
- rollback/uninstall/revert guidance;
- preserved exact paths;
- next recommendation.

---

# export bundle

Target:

```text
.aiassistant/reports/target/20260827_1545_aiscc-p1-3-security-runtime-safeguard-implementation-with-additive-commit-recovery-1/
```

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- all changed P1-3 implementation/test/config/container files preserving relative paths
- compact non-secret runtime evidence/logs
- `REMOVED_FILES.md` only if actual deletion exists

Do not export package caches, `.venv`, Python installation, Docker layers, credentials or unrelated
residue.

---

# Task lifecycle

When work/report/export completes or exact blocker is safely established:

```text
.aiassistant/tasks/active/20260827_1545_aiscc-p1-3-security-runtime-safeguard-implementation-with-additive-commit-recovery-1.md
→
.aiassistant/tasks/done/20260827_1545_aiscc-p1-3-security-runtime-safeguard-implementation-with-additive-commit-recovery-1.md
```

`done` means submitted, not Human accepted.

---

# preserved artifacts

Always preserve:

- `.aiassistant/tasks/done/20260827_1513_aiscc-p1-3-security-runtime-safeguard-implementation-with-substrate-closure-and-environment-preparation-1.md`
- `.aiassistant/records/aiscc/cycles/20260827_1545_aiscc-p1-3-runtime-substrate-closure-commit-message-blocker-1.cycle.md`
- commit `a8797fdac43b4a8bc501ccdb3c86743541153319`
- the additive corrective provenance commit created by this Task
- `.aiassistant/rules/AISCC_RUNTIME_SUBSTRATE.md`
- `.aiassistant/tasks/done/20260827_1545_aiscc-p1-3-security-runtime-safeguard-implementation-with-additive-commit-recovery-1.md`

If implementation proceeds, preserve all changed P1-3 runtime/security source/tests/config/container
files until Command Center/Human judgment.

Environment caches/installations and Docker image layers are not repository preservation targets.

---

# next action after P1-3 Human acceptance

```text
P1-4 Explicit State Machine Kernel Implementation
```

Do not execute P1-4 in this Task.
