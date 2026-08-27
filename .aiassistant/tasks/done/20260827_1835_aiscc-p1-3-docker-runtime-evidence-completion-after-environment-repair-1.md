# 작업지시서: P1-3 Docker Runtime Evidence Completion after Human Environment Repair

## meta

- task_id: `20260827_1835_aiscc-p1-3-docker-runtime-evidence-completion-after-environment-repair-1`
- created_at: `2026-08-27 18:35 KST`
- phase: `P1-3 — Security / Runtime Safeguard Implementation and Verification`
- work_type: `RUNTIME_EVIDENCE_COMPLETION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `Docker health revalidation + mandatory P1-3 runtime proof`
- predecessor_task: `20260827_1650_aiscc-p1-3-runtime-mode-read-boundary-and-docker-evidence-rework-1`
- predecessor_result: `HUMAN_DOCKER_ENVIRONMENT_REPAIR_REQUIRED`
- predecessor_command_center_cycle: `.aiassistant/records/aiscc/cycles/20260827_1835_aiscc-p1-3-source-rework-pass-docker-environment-blocked-1.cycle.md`
- predecessor_HEAD: `a9bce3f695d044e0a7f772100690c26051b963e3`
- candidate_path_count: `55`
- candidate_aggregate_sha256: `48d34d7153b416aa82ff9d8749eecacc363920be199345d9c52761de1d35f54c`
- source_mutation: `FORBIDDEN`
- P1_3_status_before: `RUNTIME_EVIDENCE_BLOCKED`
- P1_4_status: `NOT_STARTED / BLOCKED`

---

# 0. execution prerequisite

Human must first repair the local Docker PID/process environment.

This Task MUST NOT:

- stop/restart unrelated containers;
- restart Docker Desktop;
- change Docker daemon limits;
- mutate unrelated services.

Those actions are Human-owned.

If Human has not repaired the environment, the Task may still run the health probe, but if the same
OCI/PID failure remains it MUST stop immediately with:

```text
HUMAN_DOCKER_ENVIRONMENT_REPAIR_REQUIRED
```

No source change is permitted to work around an environment failure.

---

# Stage 0 — persist predecessor done Task + environment-blocker Cycle

## expected repository

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

HEAD:
a9bce3f695d044e0a7f772100690c26051b963e3
```

If HEAD differs:

```text
STOP
→ BLOCKED_PREDECESSOR_HEAD_DRIFT
```

## allowed tracked dirty provenance

Only:

```text
.aiassistant/tasks/done/20260827_1650_aiscc-p1-3-runtime-mode-read-boundary-and-docker-evidence-rework-1.md

.aiassistant/records/aiscc/cycles/20260827_1835_aiscc-p1-3-source-rework-pass-docker-environment-blocked-1.cycle.md
```

The existing 55 P1-3 candidate paths remain untracked/uncommitted and MUST NOT be staged.

Unexpected tracked dirty path:

```text
STOP
→ BLOCKED_RUNTIME_EVIDENCE_PROVENANCE_COLLISION
```

## one authorized local provenance commit

Stage explicit changed provenance paths only.

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
docs: record P1-3 Docker environment evidence blocker

Persist the P1-3 source rework judgment that closed RuntimeMode and
Docker resource-read authorization gaps.

Record that mandatory runtime evidence remains blocked only by the
Human-owned Docker PID/process environment and keep P1-4 blocked.
```

Use a real LF multiline message file / `git commit -F` or equivalent safe method.

After commit:

```text
P1_3_RUNTIME_EVIDENCE_BASE_COMMIT=<full new hash>
```

Verify:

- parent exactly `a9bce3f695d044e0a7f772100690c26051b963e3`;
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

# Stage 1 — candidate immutability gate

This Task is evidence-only.

Product/source/test/config/container candidate mutation is forbidden.

Expected current candidate:

```text
path count:
55

aggregate SHA-256:
48d34d7153b416aa82ff9d8749eecacc363920be199345d9c52761de1d35f54c
```

Aggregate definition:

```text
for every one of the exact 55 candidate project-relative paths:
1. compute lowercase SHA-256 of file bytes
2. sort by project-relative path
3. append:
   <path> + NUL + <sha256> + LF
4. SHA-256 the concatenated UTF-8 byte stream
```

Required:

```text
actual path count == 55
actual aggregate == 48d34d7153b416aa82ff9d8749eecacc363920be199345d9c52761de1d35f54c
```

Mismatch:

```text
STOP
→ BLOCKED_CANDIDATE_SOURCE_DRIFT
```

Do not repair source in this Task.

Also run:

```text
git diff --check
```

No 56th product/bootstrap path.

---

# Stage 2 — reused source evidence confirmation

The immediately preceding candidate already passed:

```text
uv sync --frozen --all-groups
uv build
ruff check
ruff format --check
mypy --strict
tests/unit + tests/integration → 26 PASS
```

Because this Task forbids source mutation and verifies the exact aggregate digest, those results are:

```text
reuse_allowed / SAME_CANDIDATE
```

For operational confidence, rerun at minimum:

```text
uv sync --frozen --all-groups
uv run pytest -q tests/unit tests/integration
```

Expected:

```text
26 PASS
```

If a deterministic source assertion now fails:

```text
STOP
→ HOLD_REWORK_REQUIRED_SOURCE_REGRESSION
```

Do not change source in this Task.

---

# Stage 3 — Docker health gate

Accepted image:

```text
python:3.12.14-slim-bookworm@
sha256:0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579
```

Run:

```text
docker info
docker stats --no-stream --format "table {{.Name}}\t{{.PIDs}}"

docker run --rm \
  python:3.12.14-slim-bookworm@sha256:0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579 \
  python -c "print('AISCC_DOCKER_HEALTH_OK')"
```

Read-only PID observation is allowed.

Do not inspect unrelated container environment/argv/mount/private metadata.

Expected:

```text
AISCC_DOCKER_HEALTH_OK
exit code 0
```

If health fails due OCI shim / PID / OS-thread / Docker daemon environment:

```text
STOP
→ HUMAN_DOCKER_ENVIRONMENT_REPAIR_REQUIRED
```

Do not execute Stage 4.

Do not mutate unrelated container or Docker Desktop.

Before Stage 4 verify:

```text
docker ps -a --filter "label=aiscc.owner=p1-3"
```

There must be no unintended stale P1-3 residue.

---

# Stage 4 — mandatory runtime evidence

Execute the current candidate exactly as-is.

Primary command:

```text
uv run pytest -q tests/runtime/security
```

Do not edit a failing test or implementation in this Task.

If a runtime assertion fails due product/security behavior rather than host environment:

```text
STOP
→ HOLD_REWORK_REQUIRED_RUNTIME_ASSERTION
```

Export the exact failed class/test/evidence.

## required evidence classes

### ACTION_STATE_CANCEL_AUTHORIZATION_RUNTIME

Must prove:

1. wrong WorkflowState → DENY / no side effect;
2. stale state/version capability → DENY;
3. terminal state normal execution → DENY;
4. exact blocked/terminal safety capability can settle existing owned resource;
5. public session A cannot cancel B;
6. Replay/read/run-ID visibility does not grant cancel authority;
7. repeated authorized cancel is idempotent;
8. wrong RuntimeMode capability → DENY before side effect.

### FILESYSTEM_PROCESS_ISOLATION_RUNTIME

Actual Docker proof:

- execution through admitted capability;
- allowed fixture reachable;
- sibling/private/host-forbidden target unavailable;
- product runtime cannot capability-free read unrelated container metadata;
- run-scoped labels/resource identity;
- non-root;
- read-only rootfs;
- dropped capabilities;
- no-new-privileges;
- PID/memory/CPU bounds;
- no broad host mount;
- cleanup observed.

### NETWORK_RUNTIME

Local isolated Docker proof only:

```text
default network deny
exact internal test network allow
unlisted target unavailable
wrong mode/run/resource denied before side effect
```

No public-internet proof.

### SECRET_NON_EXPOSURE

Synthetic canary only.

Verify absence from:

- app output/log;
- security provenance;
- product metadata;
- evidence export;
- Replay-style test artifact.

No real credential.

### TIMEOUT_RETRY_CANCEL_RUNTIME

Prove finite timeout, retry, cancellation and no false success.

### IDEMPOTENCY_ABUSE_BUDGET_RUNTIME

Prove duplicate/idempotency, exhausted budget before simulated paid effect and fail-closed throttle.

This Task does not claim provider hard-spend configuration.

### CLEANUP_RESIDUE_RUNTIME

Prove:

```text
success
failure
cancel
timeout
→ cleanup

controlled residue
→ quarantine/failure
!= clean success
```

Exact safety capability required for product cleanup.

### FAILURE_DOMAIN

Simulated Live/provider/budget unavailable:

```text
Recorded Replay/read-only path remains available
```

No provider API.

---

# Stage 5 — final residue and proof inventory

After runtime tests, always collect:

```text
docker ps -a --filter "label=aiscc.owner=p1-3"
docker network ls --filter "label=aiscc.owner=p1-3"
```

Expected clean success:

```text
no unintended P1-3 container residue
no unintended P1-3 network residue
```

If controlled quarantine evidence intentionally leaves residue, it must be:

- exact test-owned resource;
- recorded as quarantine evidence;
- safely removed through the authorized test cleanup path before final Task completion when the
  test contract expects cleanup.

Unexplained residue:

```text
STOP
→ HOLD_REWORK_REQUIRED_RUNTIME_RESIDUE
```

---

# evidence admission

## executor_required

- `RUNTIME_EVIDENCE_PROVENANCE_GIT`
- `CANDIDATE_IMMUTABILITY`
- `SOURCE_EVIDENCE_RECONFIRMATION`
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

## reuse_allowed

Immediately preceding source evidence may be reused only when:

```text
55-path count exact
+
aggregate digest exact
+
no source mutation in this Task
```

## human_owned

`HUMAN_VERIFICATION`

Only after every mandatory runtime proof passes.

Human reviews:

- environment repair result;
- runtime-evidence base commit;
- candidate digest;
- Docker health;
- exact runtime test results;
- isolation/network/secret evidence;
- timeout/retry/cancel;
- idempotency/budget;
- cleanup/residue;
- P1-1/P1-2 invariant preservation.

Expected:

```text
ACCEPTED
HOLD_REWORK_REQUIRED
or exact correction
```

## forbidden

- candidate source/test/config/container edits;
- unrelated Docker/container mutation;
- Docker Desktop restart by Executor;
- P1-4/P1-5;
- provider/LLM;
- real credential;
- deployment;
- second Git commit;
- Git push/remote;
- Browser Project Source mutation.

---

# proof non-substitution

```text
Human Docker repair
!= runtime proof

Docker health
!= security proof

26 source tests
!= Docker isolation proof

candidate digest match
!= runtime evidence

runtime tests PASS
!= Human P1-3 acceptance
```

---

# Task result rules

If Docker health still fails:

```text
HUMAN_DOCKER_ENVIRONMENT_REPAIR_REQUIRED
```

If candidate/source drift is detected:

```text
BLOCKED_CANDIDATE_SOURCE_DRIFT
```

If runtime test fails because of product/security assertion:

```text
HOLD_REWORK_REQUIRED_RUNTIME_ASSERTION
```

If all mandatory evidence passes:

```text
ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING
```

Executor MUST NOT claim P1-3 closed.

---

# report required fields

- task/path;
- old HEAD;
- Stage 0 exact provenance paths;
- full `P1_3_RUNTIME_EVIDENCE_BASE_COMMIT`;
- candidate 55-path count;
- candidate aggregate digest;
- source evidence reuse/reconfirmation;
- Docker/PID health observations;
- exact health result;
- exact runtime test count/results;
- every required proof class result;
- evidence artifact/log references;
- final P1-3 residue inventory;
- no source mutation evidence;
- no unrelated Docker mutation evidence;
- Agent claim vs admitted evidence;
- Human pending/deferred;
- blocker if any;
- rollback;
- preserved paths;
- next recommendation.

---

# export bundle

Target:

```text
.aiassistant/reports/target/20260827_1835_aiscc-p1-3-docker-runtime-evidence-completion-after-environment-repair-1/
```

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- exact 55 candidate files preserving repository-relative paths
- compact non-secret runtime proof evidence/logs

No source mutation is allowed, therefore source hashes in export must equal the predecessor
candidate.

Do not export Docker unrelated-resource data, credentials, `.venv`, package caches, Docker layers
or private host metadata.

---

# Task lifecycle

```text
.aiassistant/tasks/active/20260827_1835_aiscc-p1-3-docker-runtime-evidence-completion-after-environment-repair-1.md
→
.aiassistant/tasks/done/20260827_1835_aiscc-p1-3-docker-runtime-evidence-completion-after-environment-repair-1.md
```

`done` means submitted, not Human accepted.

---

# preserved artifacts

Preserve:

- commit `a9bce3f695d044e0a7f772100690c26051b963e3`
- `.aiassistant/tasks/done/20260827_1650_aiscc-p1-3-runtime-mode-read-boundary-and-docker-evidence-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260827_1835_aiscc-p1-3-source-rework-pass-docker-environment-blocked-1.cycle.md`
- `.aiassistant/tasks/done/20260827_1835_aiscc-p1-3-docker-runtime-evidence-completion-after-environment-repair-1.md`
- all exact 55 P1-3 candidate paths unchanged until Human P1-3 judgment

---

# next action after all evidence + Human acceptance

```text
P1-4 Explicit State Machine Kernel Implementation
```

Do not execute P1-4 in this Task.
