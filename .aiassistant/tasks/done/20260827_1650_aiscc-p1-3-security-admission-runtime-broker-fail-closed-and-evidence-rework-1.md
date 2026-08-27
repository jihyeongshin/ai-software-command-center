# 작업지시서: P1-3 Security Admission Runtime Broker, Fail-Closed Guards and Runtime Evidence Rework

## meta

- task_id: `20260827_1650_aiscc-p1-3-security-admission-runtime-broker-fail-closed-and-evidence-rework-1`
- created_at: `2026-08-27 16:50 KST`
- phase: `P1-3 — Security / Runtime Safeguard Implementation and Verification`
- work_type: `REWORK / SECURITY_SANDBOX_IMPLEMENTATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- predecessor_task: `20260827_1545_aiscc-p1-3-security-runtime-safeguard-implementation-with-additive-commit-recovery-1`
- predecessor_executor_result: `BLOCKED_REQUIRED_EVIDENCE`
- predecessor_command_center_result: `HOLD_REWORK_REQUIRED`
- predecessor_HEAD: `68c60d304b5de273e68b2783c03c117ccf8dd719`
- predecessor_cycle: `.aiassistant/records/aiscc/cycles/20260827_1650_aiscc-p1-3-security-admission-runtime-broker-and-evidence-hold-1.cycle.md`
- accepted_runtime_substrate: `AISCC-P1-3-RUNTIME-SUBSTRATE-V1`
- P1_4_status: `NOT_STARTED / BLOCKED`

---

# 0. scope

This is a narrow rework of the existing 55-path P1-3 candidate.

Do NOT redesign or discard the candidate broadly.

Retain unless directly conflicting:

- exact 9 WorkflowStates;
- exact eleven SecurityActionClass values;
- accepted action × state matrix;
- cancel requester/session/target grant model;
- idempotency/budget/throttle primitives;
- redaction/provenance;
- Docker hardening flags;
- accepted Python/uv/Hatchling bootstrap;
- existing 55-path repository layout.

Fix exactly:

```text
A. SecurityAdmission → runtime side-effect binding
B. fail-closed security guard provenance
C. exact resource capability/selector
D. mandatory runtime evidence after Docker health preflight
```

---

# Stage 0 — persist predecessor done Task + HOLD Cycle

## expected repository

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

HEAD:
68c60d304b5de273e68b2783c03c117ccf8dd719
```

The current P1-3 implementation candidate remains uncommitted.

Allowed tracked provenance inputs for this one local commit:

```text
.aiassistant/tasks/done/20260827_1545_aiscc-p1-3-security-runtime-safeguard-implementation-with-additive-commit-recovery-1.md

.aiassistant/records/aiscc/cycles/20260827_1650_aiscc-p1-3-security-admission-runtime-broker-and-evidence-hold-1.cycle.md
```

The existing 55 product/security candidate files MUST NOT be staged in Stage 0.

Before staging:

1. verify HEAD;
2. inspect `git status --short`;
3. verify the P1-3 candidate path set is contained in the exact 55-path allowlist below;
4. verify no unrelated tracked/untracked product file collision;
5. read predecessor done Task;
6. read HOLD Cycle;
7. `git diff --check`;
8. verify no secret/private material;
9. verify current active Task is this Task.

If unrelated path exists:

```text
STOP
→ BLOCKED_REWORK_WORKSPACE_COLLISION
```

## exact existing P1-3 candidate allowlist — 55 paths

```text
.python-version
pyproject.toml
uv.lock
.dockerignore
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
config/security/permission-profiles.v1.toml
config/security/resource-policy.v1.toml
config/security/limits.v1.toml
containers/p1_3/Dockerfile.sandbox
containers/p1_3/Dockerfile.evidence
containers/p1_3/compose.yaml
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

No new product path is authorized.

If rework requires a 56th product path:

```text
STOP
→ EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

## authorized provenance commit

Exactly one local commit is authorized.

Stage only actual predecessor done Task + HOLD Cycle.

Exact commit message:

```text
docs: record P1-3 security admission and runtime evidence hold

Persist the P1-3 implementation review that found an admission-to-runtime
bypass, fail-open guard defaults, incomplete resource capability binding,
and blocked Docker runtime evidence.

Keep the current safeguard source as an uncommitted rework candidate and
block P1-4 until P1-3 runtime enforcement and proof are complete.
```

Use real LF multiline message, preferably UTF-8 no-BOM message file + `git commit -F`.

After commit:

```text
P1_3_REWORK_BASE_COMMIT=<new full hash>
```

Verify:

- parent == `68c60d304b5de273e68b2783c03c117ccf8dd719`;
- commit contains only provenance path(s);
- exact multiline message;
- no history rewrite;
- no remote mutation.

After Stage 0:

```text
git add / commit / push
→ FORBIDDEN
```

The 55-path rework candidate remains uncommitted.

---

# Stage 1 — required source rework

## A. SecurityAdmission must mechanically gate side effects

Current forbidden shape:

```text
DockerRuntime.command(raw_args)
→ side effect without admitted Capability

BoundedProcessRunner.run(argv)
→ side effect without admitted Capability
```

Required authority chain:

```text
System-owned/trusted security inputs
→ SecurityPolicy.evaluate
→ ALLOW
→ issue short-lived Capability
→ runtime broker validates Capability against current WorkflowSnapshot
→ exact action/resource/run/profile match
→ consume use
→ bounded side effect
```

No valid capability:

```text
→ no normal side effect
```

Required:

- normal process/container/network execution API cannot accept arbitrary execution without a
  validated admitted capability;
- raw subprocess/Docker command primitive, if retained, must be private/internal and not the normal
  security execution boundary;
- runtime proof must exercise the admitted-capability broker path;
- safety cleanup/revoke/quarantine uses an explicit safety action/capability, not an unscoped bypass;
- capability validation/consumption result must be included in secret-safe provenance.

Do not implement P1-4 state mutation.

Use immutable `WorkflowSnapshot` trusted input/test fixture only.

## B. Guard inputs must fail closed

Current default-true pattern is forbidden.

Required:

```text
requester authorization unresolved → DENY
Task scope unresolved → DENY
resource authorization unresolved → DENY
limit/budget/idempotency unresolved → DENY
mutable target-control authorization unresolved → DENY
```

Implementation options must preserve exact accepted semantics.

Preferred:

- remove fail-open `True` defaults from `PermissionRequest`; or
- use explicit typed guard-result objects whose unknown/default state is DENY.

Do not encode Human/system authority as caller prose.

### HTTP diagnostic boundary

`/v1/security/evaluate` MUST NOT manufacture System authoritative state by:

```text
caller state
→ observed
→ authoritative
```

If P1-4 authority is unavailable, choose one fail-closed candidate behavior such as:

```text
HTTP diagnostic request
→ NON_AUTHORITATIVE / DENY
```

or an internal-only trusted context not constructible from public request.

Do not create P1-4 workflow owner.

## C. exact resource capability / selector

Replace security-critical boolean-only resource authorization.

Required typed/versioned semantics:

```text
ResourceGrant / ResourceCapability / exact policy-owned selector
→ grant/capability id
→ version
→ mode/profile
→ scenario
→ domain
→ exact allowed resource scope
→ run/principal when mutable
→ expiry/revocation where applicable
```

Names may differ; semantics must be exact.

Public Live:

```text
fixed synthetic scenario only
fixed synthetic workspace/repository resource only
no owner/private repository
no arbitrary resource ID
no arbitrary shell/process selector
no arbitrary network
no arbitrary provider/model
```

P1-5-owned provider/tool authority is not implemented now.

Where no current owner exists:

```text
DENY
```

rather than inventing provider/tool authority.

Blacklist prefixes are not sufficient as the sole hard prohibition.

## D. capability lifetime

Retain:

```text
state/version change
→ previous execution capability stale/revalidated

terminal state
→ normal execution capability unusable
```

Runtime broker must enforce this immediately before side effect.

---

# Stage 2 — static/unit/integration revalidation

Run at minimum:

```text
uv sync --frozen
uv build
uv run ruff check .
uv run ruff format --check .
uv run mypy --strict src tests
uv run pytest -q tests/unit tests/integration
```

Add/adjust tests within the existing exact test paths.

Required test cases:

1. missing/unresolved each security guard → DENY;
2. normal Docker/process broker call with no capability → no side effect;
3. DENY decision cannot be converted into executable capability;
4. stale capability → broker does not execute;
5. wrong action/resource/run/profile capability → broker does not execute;
6. valid capability → one bounded execution;
7. repeated use beyond max uses → denied;
8. arbitrary known-domain resource ID without exact resource grant → DENY;
9. public Live owner/external/arbitrary resource selector → DENY;
10. provider/tool resource without current P1-5 exact authority → DENY;
11. public HTTP diagnostic input cannot manufacture authoritative ALLOW;
12. safety cleanup requires exact safety capability and cannot become normal execution.

---

# Stage 3 — Docker health preflight

Before runtime security suite, run a minimal read-only host/environment probe.

Required:

```text
docker info
docker run --rm <already accepted exact Python base image> python -c "print('AISCC_DOCKER_HEALTH_OK')"
```

The health probe is environment precondition only, not isolation proof.

Do NOT stop/restart/change:

```text
admin-platform-edge-1
or any unrelated container
or Docker Desktop service
```

within this Task.

If minimal Docker container still cannot start:

```text
STOP
→ HUMAN_DOCKER_ENVIRONMENT_REPAIR_REQUIRED
```

Report:

- exact Docker error;
- current read-only PID/resource observation;
- test-owned resource cleanup;
- no unrelated mutation.

Human chooses environment remediation.

Do not mark P1-3 acceptance candidate.

If health probe passes, continue Stage 4.

---

# Stage 4 — mandatory runtime evidence rerun

Runtime proof MUST use the corrected admitted-capability runtime broker for normal side effects.

## ACTION_STATE_CANCEL_AUTHORIZATION_RUNTIME

Prove:

1. wrong WorkflowState → DENY and no runtime side effect;
2. stale capability after state/version change → no side effect;
3. terminal state normal execution capability → no side effect;
4. blocked/terminal safety cleanup with exact safety capability can settle existing resource;
5. session A cannot cancel session B run;
6. Replay/read/run-ID visibility cannot cancel;
7. repeated authorized cancel → one logical control effect.

## FILESYSTEM_PROCESS_ISOLATION_RUNTIME

Actual Docker evidence:

- only exact granted workspace mounted;
- allowed input visible;
- owner/private/sibling/host repository not mounted/reachable;
- normal execution container created through admitted capability broker;
- non-root/read-only/cap-drop/no-new-privileges/PID-memory-CPU constraints inspected;
- exact run ownership;
- cleanup observed.

## NETWORK_RUNTIME

Actual Docker evidence:

```text
no network capability
→ --network none / unreachable

exact internal-network capability
→ exact P1-3 isolated network + local fixture reachable

unlisted/external target
→ unavailable
```

A caller-supplied arbitrary network name is not sufficient authority.

## SECRET_NON_EXPOSURE

Synthetic canary only.

Verify canary absent from:

- argv;
- container environment;
- logs;
- decision provenance;
- runtime provenance;
- exported evidence;
- Replay-style public artifact.

## TIMEOUT_RETRY_CANCEL_RUNTIME

- finite timeout;
- finite retry;
- explicit cancel;
- broker/capability consumption semantics correct;
- no false success.

## IDEMPOTENCY_ABUSE_BUDGET_RUNTIME

Retain/re-run bounded ledger proof.

## CLEANUP_RESIDUE_RUNTIME

Prove:

- success/failure/cancel/timeout cleanup;
- wrong ownership / unresolved residue → quarantine/failure;
- safety cleanup path itself requires exact safety capability.

## FAILURE_DOMAIN

Retain/re-run:

```text
simulated Live/provider/budget failure
→ Recorded Replay path remains available
```

---

# evidence contract

## executor_required

- `REWORK_PROVENANCE_GIT`
- `STATIC_SOURCE`
- `FAIL_CLOSED_GUARD_MODEL`
- `SECURITY_ADMISSION_RUNTIME_BINDING`
- `EXACT_RESOURCE_CAPABILITY`
- `BUILD_STATIC_TYPE`
- `TARGETED_TEST`
- `DOCKER_HEALTH_PREFLIGHT`
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

Human review occurs only after all required executable evidence passes.

If Docker health is still blocked:

```text
Human final security acceptance
→ DEFERRED
```

## forbidden

- stop/restart unrelated container;
- Docker Desktop restart/service mutation;
- real provider/LLM API;
- production credential;
- deployment;
- P1-4/P1-5 implementation;
- new product path outside 55;
- second Git commit;
- Git push/remote mutation;
- Browser Project Source mutation.

---

# proof non-substitution

```text
SecurityDecision class
!= runtime broker enforced

Capability class
!= runtime requires capability

boolean authorization
!= exact resource grant

caller state
!= authoritative WorkflowState

unit side-effect-deny test
!= Docker isolation proof

Docker health probe
!= Docker security proof

runtime test calling raw docker helper
!= security admission integration proof
```

---

# mandatory stop

Stop with exact blocker if:

```text
BLOCKED_PREDECESSOR_HEAD_DRIFT
BLOCKED_REWORK_WORKSPACE_COLLISION
EVIDENCE_SCOPE_EXPANSION_REQUIRED
POLICY_CONFLICT_INVESTIGATION_REQUIRED
BLOCKED_DEPENDENCY_RESOLUTION
HUMAN_DOCKER_ENVIRONMENT_REPAIR_REQUIRED
BLOCKED_REQUIRED_EVIDENCE
```

Do not weaken P1-2/P1-3 baseline to avoid a blocker.

---

# accept criteria

Candidate may return:

```text
ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING
```

only when:

- runtime side effects are mechanically capability-gated;
- all security-critical unresolved inputs fail closed;
- exact resource capability/selector exists;
- public Live hard prohibitions are executable;
- static/build/unit/integration pass;
- Docker health passes;
- all mandatory Docker/runtime evidence passes through corrected broker path;
- no proof substitution;
- no P1-4/P1-5 scope expansion;
- no unrelated Docker mutation;
- Human remains pending until actual review.

---

# report required fields

- Task/path;
- predecessor result;
- old HEAD;
- Stage 0 exact provenance commit/new `P1_3_REWORK_BASE_COMMIT`;
- initial 55-path candidate inventory;
- exact modified paths;
- fail-closed guard changes;
- HTTP authoritative-boundary decision;
- resource capability model;
- runtime broker/capability execution chain;
- raw runtime primitive reachability boundary;
- build/static/unit/integration results;
- Docker health preflight;
- each runtime proof with exact command/artifact/result;
- Docker resource cleanup inventory;
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
.aiassistant/reports/target/20260827_1650_aiscc-p1-3-security-admission-runtime-broker-fail-closed-and-evidence-rework-1/
```

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- all 55 current P1-3 candidate files preserving relative paths
- compact non-secret proof evidence
- `REMOVED_FILES.md` only if a file in the accepted 55-path bootstrap is actually deleted

No cache, `.venv`, Python install, Docker layers or secret material.

---

# Task lifecycle

```text
.aiassistant/tasks/active/20260827_1650_aiscc-p1-3-security-admission-runtime-broker-fail-closed-and-evidence-rework-1.md
→
.aiassistant/tasks/done/20260827_1650_aiscc-p1-3-security-admission-runtime-broker-fail-closed-and-evidence-rework-1.md
```

`done` means submitted, not Human accepted.

---

# preserved artifacts

Always preserve:

- commit `a8797fdac43b4a8bc501ccdb3c86743541153319`
- commit `68c60d304b5de273e68b2783c03c117ccf8dd719`
- `.aiassistant/rules/AISCC_RUNTIME_SUBSTRATE.md`
- `.aiassistant/tasks/done/20260827_1545_aiscc-p1-3-security-runtime-safeguard-implementation-with-additive-commit-recovery-1.md`
- `.aiassistant/records/aiscc/cycles/20260827_1650_aiscc-p1-3-security-admission-runtime-broker-and-evidence-hold-1.cycle.md`
- the Stage 0 rework-provenance commit created by this Task
- `.aiassistant/tasks/done/20260827_1650_aiscc-p1-3-security-admission-runtime-broker-fail-closed-and-evidence-rework-1.md`

Preserve all 55 P1-3 candidate product/security paths pending final P1-3 judgment.

---

# next action after accepted P1-3

```text
P1-4 Explicit State Machine Kernel Implementation
```

Do not execute P1-4 in this Task.
