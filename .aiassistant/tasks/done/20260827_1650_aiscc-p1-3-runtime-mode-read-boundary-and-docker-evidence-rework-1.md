# 작업지시서: P1-3 RuntimeMode / Docker Read Boundary and Runtime Evidence Rework

## meta

- task_id: `20260827_1650_aiscc-p1-3-runtime-mode-read-boundary-and-docker-evidence-rework-1`
- created_at: `2026-08-27 16:50 KST`
- phase: `P1-3 — Security / Runtime Safeguard Implementation and Verification`
- work_type: `SECURITY_SANDBOX_IMPLEMENTATION_REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `runtime-mode capability binding / resource-read authorization / mandatory Docker runtime evidence`
- predecessor_task: `20260827_1650_aiscc-p1-3-security-admission-runtime-broker-fail-closed-and-evidence-rework-1`
- predecessor_executor_result: `HUMAN_DOCKER_ENVIRONMENT_REPAIR_REQUIRED`
- predecessor_command_center_result: `HOLD_REWORK_REQUIRED`
- predecessor_base_commit: `1b6e84bdbb0b632e59d60670d785d3c14392216e`
- predecessor_cycle: `.aiassistant/records/aiscc/cycles/20260827_1650_aiscc-p1-3-runtime-mode-and-docker-read-boundary-hold-1.cycle.md`
- P1_3_status: `HOLD_REWORK_REQUIRED`
- P1_4_status: `NOT_STARTED / BLOCKED`

---

# 0. sole execution contract

This is a narrow continuation of the current 55-path P1-3 candidate.

Retain the predecessor corrections unless directly conflicting:

- explicit fail-closed `AuthorityStatus`;
- deny-only public diagnostic HTTP boundary;
- typed/versioned issuer-backed `ResourceGrant`;
- exact Public Live selectors;
- provider/tool/secret deny where owner missing;
- admitted capability requirement for normal process/container/network side effects;
- central use ledger;
- safety cleanup capability separation;
- cancel target model;
- redaction;
- limits/idempotency/budget primitive;
- Docker hardening;
- 55-path bootstrap.

Do NOT redesign the whole P1-3 implementation.

---

# Stage 0 — persist predecessor rework + this HOLD Cycle

## expected repository

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

HEAD:
1b6e84bdbb0b632e59d60670d785d3c14392216e
```

If HEAD differs:

```text
STOP
→ BLOCKED_PREDECESSOR_HEAD_DRIFT
```

## allowed tracked dirty provenance

Before Stage 0 commit, exact tracked dirty provenance may contain only:

```text
.aiassistant/tasks/done/20260827_1650_aiscc-p1-3-security-admission-runtime-broker-fail-closed-and-evidence-rework-1.md

.aiassistant/records/aiscc/cycles/20260827_1650_aiscc-p1-3-runtime-mode-and-docker-read-boundary-hold-1.cycle.md
```

Current 55 product/security candidate paths are expected to remain untracked/uncommitted and MUST
NOT be included in Stage 0.

If another tracked dirty path exists:

```text
STOP
→ BLOCKED_REWORK_PROVENANCE_COLLISION
```

## Stage 0 Git policy

Exactly one local provenance commit is authorized.

Use exact changed provenance paths only.

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

Commit message:

```text
docs: record P1-3 runtime mode and read-boundary hold

Persist the P1-3 review that retained the fail-closed broker rework but
found missing RuntimeMode consumption checks, unauthorized Docker
resource reads, and an unresolved Docker runtime-evidence environment.

Keep P1-4 blocked until the broker and runtime proof are complete.
```

Use a real multiline message file or another LF-safe method.
Do not use literal PowerShell backtick-`n` text as a newline mechanism.

After commit:

```text
P1_3_MODE_READ_REWORK_BASE_COMMIT=<full new hash>
```

Verify:

- parent exactly `1b6e84bdbb0b632e59d60670d785d3c14392216e`;
- commit paths only the allowed provenance subset;
- exact multiline message;
- tracked index clean;
- no remote operation.

After this commit:

```text
git add / commit / push
→ FORBIDDEN
```

The 55-path implementation candidate stays uncommitted.

---

# Stage 1 — RuntimeMode must be part of trusted runtime consumption

## defect

Current capability carries:

```text
mode
profile_version
```

but broker consumption validates only profile version, not current RuntimeMode.

All current profiles use:

```text
p1-3-v2
```

therefore profile version cannot substitute for mode identity.

## required correction

Introduce an exact trusted runtime execution context or equivalent.

Preferred semantic shape:

```text
RuntimeExecutionContext
→ principal
→ mode
→ authoritative WorkflowSnapshot
→ profile_version
```

Names may differ.

Every normal runtime broker call and safety/read broker call must consume a trusted context that
contains the current RuntimeMode.

`Capability.validate` / `SecurityPolicy.consume_capability` must enforce:

```text
current_mode is capability.mode
```

Required denial:

```text
CAPABILITY_MODE_MISMATCH
```

Mode mismatch MUST occur before side effect.

Required proof cases:

```text
OWNER_SELF_DOGFOOD capability
+ PUBLIC_BOUNDED_LIVE runtime context
→ DENY / no side effect

PUBLIC_BOUNDED_LIVE capability
+ PUBLIC_RECORDED_REPLAY runtime context
→ DENY / no side effect
```

Do not encode mode as a WorkflowState.
Do not create P1-4 authority.

A test `WorkflowSnapshot` remains a fixture, not the authoritative workflow kernel.

---

# Stage 2 — close Docker read-query authorization bypass

## defect

Current product runtime exposes capability-free arbitrary resource queries equivalent to:

```text
inspect(name)
inspect_format(name, format)
wait(name)
exists(name)
```

This is not acceptable as a public/runtime broker boundary.

`docker inspect` may reveal unrelated/sibling container environment, argv, mounts, labels and
network metadata.

## required product-runtime rule

```text
READ_ONLY
!= AUTHORIZED
```

Product/runtime access to a run-owned Docker resource requires exact read or safety authorization.

### allowed internal environment diagnostic

A fixed, non-resource-selecting environment probe may remain internal, for example:

```text
docker info --format "{{.OSType}}"
```

It MUST:

- accept no caller-selected container/resource;
- return only the fixed environment fact required for preflight;
- not expose arbitrary host/container metadata.

### run-resource inspection

Any product runtime query selecting a container/network/run resource must satisfy one of:

```text
A. exact admitted RUN_REVIEW_READ_ONLY capability
```

or:

```text
B. exact admitted SAFETY_CLEANUP_REVOKE_QUARANTINE capability
   followed by a private ownership-check primitive
```

Do not expose arbitrary `format_value` as a capability-free normal runtime API.

A safe read capability must bind:

```text
mode
profile
principal
run
current WorkflowSnapshot/state_version
action
exact resource scope
expiry/revocation/use
```

Unknown/unowned target → DENY / no metadata.

### cleanup

Cleanup may use a private fixed-format label inspection internally only after the exact safety
capability has already passed.

It must validate run ownership before remove.

### evidence observer separation

Tests may need external observation of the resource they created.

If so, use a test-only evidence observer in existing test paths.

The observer:

```text
!= product runtime API
!= SecurityAdmission
!= public capability
```

It MUST:

- inspect only test-created exact names;
- never be wired into application/runtime code;
- not be claimed as PUBLIC_BOUNDED_LIVE authority;
- not inspect unrelated containers.

No new repository path beyond the current 55-path bootstrap is allowed.

---

# Stage 3 — retain fail-closed authority model

The previous correction is retained.

Required:

```text
requester unresolved
→ DENY

task scope unresolved
→ DENY

resource grant absent/unresolved
→ DENY

limit/budget/idempotency unresolved
→ DENY

mutable target-control unresolved
→ DENY
```

Do not reintroduce default-true booleans.

Public `/v1/security/evaluate` remains:

```text
DENY / NON_AUTHORITATIVE_DIAGNOSTIC_ONLY
```

until a future System-owned authority integration exists.

## future-owner handoff note

Do not promote this to a new implementation scope, but report explicitly:

```text
AuthorityStatus.GRANTED from arbitrary caller code
!= future System-owned authoritative guard evidence
```

P1-4/P1-6/P1-7 integration must supply trusted producers/owners.

---

# Stage 4 — allowed implementation paths

Do not create a 56th product/bootstrap path.

Modify only as required within the existing candidate, expected subset:

```text
src/aiscc/contracts/security.py
src/aiscc/runtime/contracts.py
src/aiscc/security/capability.py
src/aiscc/security/policy.py
src/aiscc/runtime/process.py
src/aiscc/runtime/docker.py
src/aiscc/runtime/network.py
src/aiscc/runtime/cleanup.py

tests/conftest.py
tests/unit/security/test_capability_lifetime.py
tests/unit/security/test_permission_policy.py
tests/integration/security/test_broker_fail_closed.py

tests/runtime/security/test_action_state_cancel_authorization.py
tests/runtime/security/test_sandbox_isolation.py
tests/runtime/security/test_network_boundary.py
tests/runtime/security/test_secret_non_exposure.py
tests/runtime/security/test_timeout_retry_cancel.py
tests/runtime/security/test_cleanup_residue.py
```

Other existing 55-path files may be touched only if directly required by the two corrections.

If a new repository path is required:

```text
STOP
→ EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

No `src/aiscc/workflow/`, `providers/`, `persistence/`, migrations or deployment files.

---

# Stage 5 — static/build/targeted revalidation

Run:

```text
uv sync --frozen --all-groups
uv build
uv run ruff check .
uv run ruff format --check .
uv run mypy --strict src tests
uv run pytest -q tests/unit tests/integration
```

Required deterministic cases:

1. no capability → no normal Docker/process/network side effect;
2. DENY → no capability issue;
3. stale state/version → no side effect;
4. wrong run/action/resource/profile → no side effect;
5. wrong RuntimeMode → `CAPABILITY_MODE_MISMATCH` / no side effect;
6. exact valid capability → one bounded use;
7. max-use replay → deny;
8. arbitrary Public Live selector → deny;
9. provider/tool selector → deny;
10. public HTTP diagnostic → always non-authoritative DENY;
11. arbitrary container read with no read/safety capability → no product-runtime metadata;
12. exact read capability → only exact owned/test resource metadata allowed;
13. safety cleanup → private ownership read + cleanup only;
14. read capability cannot execute normal side effect;
15. safety capability cannot become normal execution.

---

# Stage 6 — Docker health preflight

After static/targeted pass, run the minimal existing health probe first.

Use the accepted image digest:

```text
python:3.12.14-slim-bookworm@
sha256:0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579
```

Required:

```text
docker info
docker run --rm <exact-image> python -c "print('AISCC_DOCKER_HEALTH_OK')"
```

Do not stop/restart/mutate unrelated containers.
Do not restart Docker Desktop.

If health still fails with OCI/PID/resource exhaustion:

```text
STOP
→ HUMAN_DOCKER_ENVIRONMENT_REPAIR_REQUIRED
```

Report:

- exact error;
- read-only container/PID observation if available;
- no unrelated mutation;
- final `aiscc.owner=p1-3` residue inventory.

Do NOT execute Stage 7 after failed health.

---

# Stage 7 — mandatory runtime evidence when Docker health passes

All runtime proof must use the corrected admitted-capability product broker for side effects and
authorized product reads.

A separate test-only observer may observe exact test-owned resources but is not a product authority.

## ACTION_STATE_CANCEL_AUTHORIZATION_RUNTIME

Prove:

1. wrong WorkflowState → DENY / no side effect;
2. stale capability → no side effect;
3. terminal state normal capability → no side effect;
4. blocked/terminal exact safety capability can settle an existing owned resource;
5. public session A cannot cancel B;
6. Replay/read/run-ID visibility does not grant cancel;
7. repeated authorized cancel is idempotent;
8. wrong RuntimeMode capability → no side effect.

## FILESYSTEM_PROCESS_ISOLATION_RUNTIME

Prove via Docker:

- normal execution created through exact admitted capability;
- allowed workspace/input reachable;
- sibling/private/host-forbidden target unavailable;
- product runtime cannot capability-free inspect an unrelated/sibling container;
- run-scoped labels/identity;
- non-root/read-only/drop-all/no-new-privileges/pids/memory/cpu constraints;
- cleanup observed.

## NETWORK_RUNTIME

Prove:

```text
no network capability
→ no network creation/attachment through product broker

exact internal-network capability
→ exact test network only

wrong mode/run/resource
→ DENY

unlisted/public egress
→ unavailable
```

Use local isolated fixtures only.

## SECRET_NON_EXPOSURE

Use synthetic canary only.

Verify no canary in:

- application log/output;
- security decision/provenance;
- product runtime metadata response;
- test export;
- public Replay-style test artifact.

Test-only external observer may inspect the exact test-created container solely to verify absence;
it must not inspect unrelated resources.

## TIMEOUT_RETRY_CANCEL_RUNTIME

Prove bounded timeout/retry/cancel through capability-gated broker path.

## IDEMPOTENCY_ABUSE_BUDGET_RUNTIME

Re-run required deterministic proof.

No provider hard-spend claim.

## CLEANUP_RESIDUE_RUNTIME

Prove success/failure/cancel/timeout cleanup plus controlled residue/quarantine.

All cleanup resource reads/removal must follow exact safety capability ownership path.

## FAILURE_DOMAIN

Simulated Live/provider/budget unavailable:

```text
→ Recorded Replay/read-only path remains independently available
```

No provider API.

---

# evidence contract

## executor_required

- `MODE_READ_REWORK_PROVENANCE_GIT`
- `RUNTIME_MODE_BINDING`
- `DOCKER_READ_AUTHORIZATION`
- `STATIC_SOURCE`
- `BUILD_STATIC_TYPE`
- `TARGETED_TEST`
- `DOCKER_HEALTH_PREFLIGHT`
- if health passes:
  - `ACTION_STATE_CANCEL_AUTHORIZATION_RUNTIME`
  - `FILESYSTEM_PROCESS_ISOLATION_RUNTIME`
  - `NETWORK_RUNTIME`
  - `SECRET_NON_EXPOSURE`
  - `TIMEOUT_RETRY_CANCEL_RUNTIME`
  - `IDEMPOTENCY_ABUSE_BUDGET_RUNTIME`
  - `CLEANUP_RESIDUE_RUNTIME`
  - `FAILURE_DOMAIN`

## valid blocker

If Docker health remains broken after source rework:

```text
HUMAN_DOCKER_ENVIRONMENT_REPAIR_REQUIRED
```

This is valid only after:

- RuntimeMode binding correction passes static/targeted evidence;
- Docker read boundary correction passes static/targeted evidence;
- no proof substitution;
- no unrelated Docker mutation.

## human_owned

`HUMAN_VERIFICATION`

Human final review only after all mandatory runtime evidence passes.

Expected:

```text
ACCEPTED
HOLD_REWORK_REQUIRED
or exact correction
```

## forbidden

- P1-4/P1-5 implementation;
- provider/LLM API;
- real credential;
- deployment;
- second Git commit;
- Git push/remote mutation;
- unrelated container/Docker Desktop mutation;
- Browser Project Source mutation.

---

# proof non-substitution

```text
Capability.mode field exists
!= broker mode enforcement

profile version match
!= RuntimeMode match

read-only
!= authorized read

test observer
!= product runtime capability

unit read test
!= Docker cross-run isolation proof

Docker health
!= runtime security proof

Docker runtime proof
!= Human acceptance
```

---

# accept criteria

P1-3 may return:

```text
ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING
```

only when:

- previous fail-closed/resource/broker corrections remain;
- runtime consumption enforces exact RuntimeMode;
- arbitrary Docker resource reads are mechanically closed;
- product reads require exact read/safety authority;
- static/build/unit/integration all pass;
- Docker health passes;
- all mandatory runtime evidence passes;
- no proof substitution;
- no P1-4/P1-5 scope expansion;
- Human remains pending.

If Docker health remains broken, return only:

```text
HUMAN_DOCKER_ENVIRONMENT_REPAIR_REQUIRED
```

after recording the completed source corrections.

---

# report required fields

- Task/path;
- old HEAD;
- Stage 0 provenance commit/full new base hash;
- predecessor 55-path inventory retained;
- exact modified paths;
- RuntimeExecutionContext/equivalent model;
- exact mode-mismatch denial path;
- Docker read-query product boundary before/after;
- test-only observer boundary if used;
- future AuthorityStatus producer handoff note;
- build/static/unit/integration results;
- Docker health result;
- every runtime proof result if executed;
- exact resource cleanup inventory;
- Agent claim vs admitted evidence;
- Human pending/deferred;
- forbidden-not-run;
- blocker if any;
- rollback;
- preserved paths;
- next recommendation.

---

# export bundle

Target:

```text
.aiassistant/reports/target/20260827_1650_aiscc-p1-3-runtime-mode-read-boundary-and-docker-evidence-rework-1/
```

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- all current 55 P1-3 candidate files preserving repository-relative paths
- compact non-secret proof evidence
- `REMOVED_FILES.md` only if one of the existing 55 bootstrap files is actually deleted

No caches, `.venv`, Python install, Docker layers, credentials or unrelated container data.

---

# Task lifecycle

```text
.aiassistant/tasks/active/20260827_1650_aiscc-p1-3-runtime-mode-read-boundary-and-docker-evidence-rework-1.md
→
.aiassistant/tasks/done/20260827_1650_aiscc-p1-3-runtime-mode-read-boundary-and-docker-evidence-rework-1.md
```

`done` means submitted, not Human accepted.

---

# preserved artifacts

Preserve:

- commit `a8797fdac43b4a8bc501ccdb3c86743541153319`
- commit `68c60d304b5de273e68b2783c03c117ccf8dd719`
- commit `1b6e84bdbb0b632e59d60670d785d3c14392216e`
- `.aiassistant/rules/AISCC_RUNTIME_SUBSTRATE.md`
- `.aiassistant/tasks/done/20260827_1650_aiscc-p1-3-security-admission-runtime-broker-fail-closed-and-evidence-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260827_1650_aiscc-p1-3-runtime-mode-and-docker-read-boundary-hold-1.cycle.md`
- `.aiassistant/tasks/done/20260827_1650_aiscc-p1-3-runtime-mode-read-boundary-and-docker-evidence-rework-1.md`

Preserve all 55 current P1-3 candidate paths pending final P1-3 judgment.

---

# next action after P1-3 Human acceptance

```text
P1-4 Explicit State Machine Kernel Implementation
```

Do not execute P1-4 in this Task.
