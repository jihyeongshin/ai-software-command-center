# 작업지시서: P1-3 Runtime Proof Assertion Coverage Rework

## meta

- task_id: `20260827_1941_aiscc-p1-3-runtime-proof-assertion-coverage-rework-1`
- created_at: `2026-08-27 19:41 KST`
- phase: `P1-3 — Security / Runtime Safeguard Implementation and Verification`
- work_type: `RUNTIME_EVIDENCE_ASSERTION_REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `missing mandatory runtime assertions only`
- predecessor_task: `20260827_1835_aiscc-p1-3-docker-runtime-evidence-completion-after-environment-repair-1`
- predecessor_result: `HOLD_REWORK_REQUIRED_RUNTIME_ASSERTION`
- predecessor_HEAD: `4e7f5bd9e828c936d6686535ed96e8ec7748e59c`
- predecessor_candidate_path_count: `55`
- predecessor_candidate_aggregate_sha256: `48d34d7153b416aa82ff9d8749eecacc363920be199345d9c52761de1d35f54c`
- product_source_mutation: `FORBIDDEN`
- P1_3_status_before: `HOLD_REWORK_REQUIRED`
- P1_4_status: `NOT_STARTED / BLOCKED`

---

# 0. sole execution contract

This is an assertion/evidence-coverage rework only.

The current product runtime/security implementation has no observed runtime assertion failure.

Therefore this Task MUST NOT modify:

```text
src/aiscc/**
config/security/**
containers/p1_3/**
pyproject.toml
uv.lock
.python-version
.dockerignore
```

unless a later Command Center Task explicitly authorizes source rework.

If a newly-added mandatory assertion demonstrates a product/security defect:

```text
STOP
→ HOLD_REWORK_REQUIRED_RUNTIME_ASSERTION
```

Do not fix product source in this Task.

---

# Stage 0 — persist predecessor evidence Task + HOLD Cycle

## expected repository

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

HEAD:
4e7f5bd9e828c936d6686535ed96e8ec7748e59c
```

If HEAD differs:

```text
STOP
→ BLOCKED_PREDECESSOR_HEAD_DRIFT
```

## allowed tracked dirty provenance

Only:

```text
.aiassistant/tasks/done/20260827_1835_aiscc-p1-3-docker-runtime-evidence-completion-after-environment-repair-1.md

.aiassistant/records/aiscc/cycles/20260827_1941_aiscc-p1-3-runtime-proof-assertion-coverage-hold-1.cycle.md
```

The current 55 P1-3 candidate paths remain untracked/uncommitted and MUST NOT be staged.

Unexpected tracked dirty path:

```text
STOP
→ BLOCKED_ASSERTION_REWORK_PROVENANCE_COLLISION
```

## one authorized local provenance commit

Stage only actual changed members of the exact provenance set.

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
docs: record P1-3 runtime proof assertion hold

Persist the evidence run where Docker health and all existing runtime
tests passed but three mandatory proof classes lacked explicit runtime
assertions required by the P1-3 evidence contract.

Limit the next rework to assertion coverage and keep product source and
P1-4 unchanged.
```

Use a real LF-safe multiline message file / `git commit -F` or equivalent.

After commit:

```text
P1_3_ASSERTION_REWORK_BASE_COMMIT=<full new hash>
```

Verify:

- parent exactly `4e7f5bd9e828c936d6686535ed96e8ec7748e59c`;
- only allowed provenance paths;
- exact multiline message;
- index clean;
- no remote operation.

After this commit:

```text
git add / commit / push
→ FORBIDDEN
```

---

# Stage 1 — baseline candidate immutability

Before editing assertions, verify:

```text
path count:
55

aggregate SHA-256:
48d34d7153b416aa82ff9d8749eecacc363920be199345d9c52761de1d35f54c
```

Use the exact aggregate algorithm from the predecessor Task/Cycle.

Mismatch:

```text
STOP
→ BLOCKED_CANDIDATE_SOURCE_DRIFT
```

Also record per-file SHA-256 for every test path that will be edited.

---

# Stage 2 — exact allowed assertion paths

The only candidate paths that may be modified are existing test/evidence-observer paths:

```text
tests/conftest.py

tests/runtime/security/test_action_state_cancel_authorization.py
tests/runtime/security/test_sandbox_isolation.py
tests/runtime/security/test_network_boundary.py
```

Modify `tests/conftest.py` only if required to expose fixed, exact test-owned Docker metadata needed
for assertions.

No new repository path.

Do not edit:

```text
tests/unit/**
tests/integration/**
other tests/runtime/security/**
src/**
config/**
containers/**
manifest/lock/build files
```

If another path is necessary:

```text
STOP
→ EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

---

# Stage 3 — ACTION_STATE_CANCEL_AUTHORIZATION_RUNTIME assertion completion

Add runtime-class proof for wrong RuntimeMode.

Required case:

```text
valid OWNER_SELF_DOGFOOD capability
+ same principal
+ same run
+ same WorkflowSnapshot/state_version
+ same profile version
+ same action
+ same exact resource scope
+ PUBLIC_BOUNDED_LIVE runtime execution context
→ DENY(CAPABILITY_MODE_MISMATCH)
→ no Docker/process side effect
```

Also prove the symmetric or second public-mode mismatch where practical:

```text
PUBLIC_BOUNDED_LIVE capability
+ PUBLIC_RECORDED_REPLAY runtime context
→ DENY(CAPABILITY_MODE_MISMATCH)
→ no side effect
```

At least one mismatch MUST pass through an actual runtime broker method, not only
`SecurityPolicy.consume_capability()`.

Evidence must show side-effect absence using an exact test-owned resource/marker.

Retain existing stale/terminal/safety/cancel/idempotency assertions.

---

# Stage 4 — FILESYSTEM_PROCESS_ISOLATION_RUNTIME assertion completion

The current `test_sandbox_isolation.py` already executes an admitted Docker container and obtains
test-owned Docker metadata.

Extend assertions to prove the mandatory hardening fields.

## required container identity

Assert exact:

```text
aiscc.run_id == current run_id
aiscc.owner == p1-3
```

The observer may return only metadata for the explicitly registered test container.

## required hardening

Assert equivalent Docker inspect values:

```text
ReadonlyRootfs == true
Config.User == "65532:65532" or exact effective equivalent
HostConfig.CapDrop includes ALL
HostConfig.SecurityOpt includes no-new-privileges
HostConfig.PidsLimit == 64
HostConfig.Memory == 134217728
HostConfig.NanoCpus == 500000000
HostConfig.NetworkMode == "none"
```

Assert tmpfs contract:

```text
/tmp
→ rw
→ noexec
→ nosuid
→ bounded size equivalent to configured 16 MiB
```

Do not require string formatting if Docker returns semantically equivalent structured metadata.

## required mount inventory

For the sandbox test container:

- exact test fixture directory is mounted read-only at `/workspace`;
- no owner repository root mount;
- no `.git` mount;
- no host home mount;
- no Docker socket mount;
- no sibling run workspace mount;
- no unexpected broad host bind mount.

Prefer structured JSON parsing over brittle substring checks.

## required cross-run product-read denial

Create two exact test-owned run identities/resources, or one exact owned resource plus a mismatched
`WorkflowSnapshot`.

Using product `DockerRuntime.read_container_metadata()`:

```text
read capability bound to run A
+ target owned by run B
→ DENY / no metadata
```

or an equivalent exact cross-run case.

The test-only observer may verify that the target exists and is run-B-owned.

The assertion MUST demonstrate product-runtime denial, not merely observer registration limits.

Cleanup both test resources through their exact safety capability paths.

---

# Stage 5 — NETWORK_RUNTIME assertion completion

Retain existing positive internal-network and connectivity-denial tests.

Add broker-level pre-side-effect denial assertions.

## no capability

For exact test network name/resource:

```text
DockerRuntime.create_internal_network(
  capability=None,
  ...
)
→ executed == false
→ CAPABILITY_REQUIRED
→ test-only observer / docker ls confirms network does not exist
```

Do not rely only on return value if an exact test-owned external observation can safely confirm
absence.

## wrong RuntimeMode

Create an otherwise-valid network capability for mode A.

Attempt network creation with mode B:

```text
→ CAPABILITY_MODE_MISMATCH
→ no network side effect
```

## wrong run/state snapshot

Use capability bound to run A with current run B or changed state/version:

```text
→ DENY
→ no network side effect
```

Expected specific reason may be:

```text
CAPABILITY_RUN_MISMATCH
or
CAPABILITY_STALE_STATE_VERSION
```

according to exact mismatch used.

## wrong resource scope

Use capability for network resource A and request network resource B:

```text
→ CAPABILITY_RESOURCE_SCOPE_MISMATCH
→ no resource-B network side effect
```

## observation

If a test-only network observer is needed, implement it only inside existing `tests/conftest.py`.

It must require explicit registration of exact test-owned network names and must not inspect
unrelated Docker networks.

It remains:

```text
test-only evidence observer
!= product runtime authority
```

---

# Stage 6 — source/static revalidation

After assertion edits:

```text
uv sync --frozen --all-groups
uv build
uv run ruff check .
uv run ruff format --check .
uv run mypy --strict src tests
uv run pytest -q tests/unit tests/integration
```

Expected unit/integration baseline:

```text
26 PASS
```

No source/config/container mutation.

Record new hashes for the modified test paths and new 55-path aggregate digest.

The aggregate is expected to change only because of the authorized test assertion edits.

If any non-authorized candidate path hash changes:

```text
STOP
→ BLOCKED_UNAUTHORIZED_CANDIDATE_MUTATION
```

---

# Stage 7 — Docker health

Run:

```text
docker info

docker run --rm \
  python:3.12.14-slim-bookworm@sha256:0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579 \
  python -c "print('AISCC_DOCKER_HEALTH_OK')"
```

If the Human-owned PID/thread problem has recurred:

```text
STOP
→ HUMAN_DOCKER_ENVIRONMENT_REPAIR_REQUIRED
```

Do not mutate unrelated containers/Docker Desktop.

---

# Stage 8 — complete runtime proof

Run:

```text
uv run pytest -q tests/runtime/security
```

No test may be skipped/xfailed to obtain PASS.

If any newly-added mandatory assertion fails due actual product/runtime behavior:

```text
STOP
→ HOLD_REWORK_REQUIRED_RUNTIME_ASSERTION
```

Report the exact assertion and observed behavior.

Do NOT modify `src/**` in this Task.

## required admission

After PASS, explicitly map every mandatory subclaim to the exact runtime test/assertion.

### ACTION_STATE_CANCEL_AUTHORIZATION_RUNTIME

Must include all eight:

1. wrong WorkflowState;
2. stale capability;
3. terminal normal execution denial;
4. blocked/terminal safety cleanup;
5. session A cannot cancel B;
6. Replay/read/run-ID visibility no cancel;
7. repeated cancel idempotent;
8. wrong RuntimeMode no side effect.

### FILESYSTEM_PROCESS_ISOLATION_RUNTIME

Must include:

- admitted execution;
- exact fixture access;
- non-root;
- read-only rootfs/workspace;
- run labels;
- cap-drop;
- no-new-privileges;
- PID/memory/CPU bounds;
- tmpfs bounds/options;
- exact mount inventory;
- no host/sibling/private broad mount;
- no network by default;
- cross-run product-read denial;
- cleanup.

### NETWORK_RUNTIME

Must include:

- no-capability pre-side-effect denial;
- exact internal network success;
- default/no-network behavior;
- unlisted target unavailable;
- wrong RuntimeMode pre-side-effect denial;
- wrong run/state pre-side-effect denial;
- wrong resource pre-side-effect denial;
- cleanup.

### other proof classes

Re-run and admit:

- `SECRET_NON_EXPOSURE`
- `TIMEOUT_RETRY_CANCEL_RUNTIME`
- `IDEMPOTENCY_ABUSE_BUDGET_RUNTIME`
- `CLEANUP_RESIDUE_RUNTIME`
- `FAILURE_DOMAIN`

---

# Stage 9 — final residue

Always collect:

```text
docker ps -a --filter "label=aiscc.owner=p1-3"
docker network ls --filter "label=aiscc.owner=p1-3"
```

Expected:

```text
no unintended container residue
no unintended network residue
```

Unexplained residue:

```text
STOP
→ HOLD_REWORK_REQUIRED_RUNTIME_RESIDUE
```

---

# evidence contract

## executor_required

- `ASSERTION_REWORK_PROVENANCE_GIT`
- `BASELINE_CANDIDATE_IMMUTABILITY`
- `AUTHORIZED_ASSERTION_MUTATION`
- `SOURCE_STATIC_REVALIDATION`
- `DOCKER_HEALTH_PREFLIGHT`
- `ACTION_STATE_CANCEL_AUTHORIZATION_RUNTIME`
- `FILESYSTEM_PROCESS_ISOLATION_RUNTIME`
- `NETWORK_RUNTIME`
- `SECRET_NON_EXPOSURE`
- `TIMEOUT_RETRY_CANCEL_RUNTIME`
- `IDEMPOTENCY_ABUSE_BUDGET_RUNTIME`
- `CLEANUP_RESIDUE_RUNTIME`
- `FAILURE_DOMAIN`
- `FINAL_RESIDUE_INVENTORY`

## human_owned

`HUMAN_VERIFICATION`

Only after every mandatory proof class is admitted.

Expected:

```text
ACCEPTED
HOLD_REWORK_REQUIRED
or exact correction
```

## forbidden

- any `src/**` edit;
- config/container/manifest/lock edit;
- new candidate path;
- second Git commit;
- Git push/remote mutation;
- unrelated Docker/container mutation;
- Docker Desktop restart by Executor;
- P1-4/P1-5;
- provider/LLM;
- real credentials;
- deployment;
- Browser Project Source mutation.

---

# proof non-substitution

```text
integration wrong-mode PASS
!= runtime-class wrong-mode proof

Docker inspect collected
!= asserted hardening proof

connectivity failure
!= broker pre-side-effect authorization denial

test-only observer
!= product runtime authority

all runtime tests PASS
!= Human P1-3 acceptance
```

---

# Task result rules

If assertion coverage is implemented and every required proof passes:

```text
ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING
```

If a new assertion exposes actual product behavior defect:

```text
HOLD_REWORK_REQUIRED_RUNTIME_ASSERTION
```

If unauthorized source drift is needed:

```text
EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

If Docker host issue recurs:

```text
HUMAN_DOCKER_ENVIRONMENT_REPAIR_REQUIRED
```

Executor MUST NOT claim P1-3 `ACCEPTED / CLOSED`.

---

# report required fields

- task/path;
- old HEAD;
- Stage 0 provenance paths;
- full `P1_3_ASSERTION_REWORK_BASE_COMMIT`;
- baseline 55-path aggregate;
- exact modified test paths + before/after hashes;
- new 55-path aggregate;
- confirmation no non-test candidate mutation;
- exact new assertions by proof class;
- static/build/unit/integration result;
- Docker health;
- runtime suite count/time;
- mandatory proof-class assertion mapping;
- final residue;
- Agent claim vs admitted evidence;
- Human pending;
- forbidden-not-run;
- blocker if any;
- rollback;
- preserved paths;
- next recommendation.

---

# export bundle

Target:

```text
.aiassistant/reports/target/20260827_1941_aiscc-p1-3-runtime-proof-assertion-coverage-rework-1/
```

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- all exact 55 candidate files preserving relative paths
- compact non-secret runtime evidence summary

No cache, `.venv`, Docker layers, credentials or unrelated Docker metadata.

---

# Task lifecycle

```text
.aiassistant/tasks/active/20260827_1941_aiscc-p1-3-runtime-proof-assertion-coverage-rework-1.md
→
.aiassistant/tasks/done/20260827_1941_aiscc-p1-3-runtime-proof-assertion-coverage-rework-1.md
```

`done` means submitted, not Human accepted.

---

# preserved artifacts

Preserve:

- commit `4e7f5bd9e828c936d6686535ed96e8ec7748e59c`
- `.aiassistant/tasks/done/20260827_1835_aiscc-p1-3-docker-runtime-evidence-completion-after-environment-repair-1.md`
- `.aiassistant/records/aiscc/cycles/20260827_1941_aiscc-p1-3-runtime-proof-assertion-coverage-hold-1.cycle.md`
- `.aiassistant/tasks/done/20260827_1941_aiscc-p1-3-runtime-proof-assertion-coverage-rework-1.md`
- all exact 55 P1-3 candidate paths

The pre-rework aggregate remains historical evidence:

```text
48d34d7153b416aa82ff9d8749eecacc363920be199345d9c52761de1d35f54c
```

The post-rework aggregate must be reported after authorized assertion edits.

---

# next action after complete runtime proof + Human acceptance

```text
P1-4 Explicit State Machine Kernel Implementation
```

Do not execute P1-4 in this Task.
