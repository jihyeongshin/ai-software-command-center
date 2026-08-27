# AISCC Cycle Record

## meta

- cycle_id: `20260827_1650_aiscc-p1-3-security-admission-runtime-broker-and-evidence-hold-1`
- date: `2026-08-27 16:50 KST`
- primary_semantic_owner: `P1-3 executable security admission / runtime broker / runtime evidence judgment`
- work_type: `SECURITY_SANDBOX_IMPLEMENTATION`
- execution_mode: `MANUAL_COMMAND_CENTER`
- task_file: `20260827_1545_aiscc-p1-3-security-runtime-safeguard-implementation-with-additive-commit-recovery-1.md`
- task_done_path: `.aiassistant/tasks/done/20260827_1545_aiscc-p1-3-security-runtime-safeguard-implementation-with-additive-commit-recovery-1.md`
- executor_result: `BLOCKED_REQUIRED_EVIDENCE`
- command_center_result: `HOLD_REWORK_REQUIRED`
- reject_cause:
  - `SECURITY_ADMISSION_RUNTIME_BYPASS`
  - `FAIL_OPEN_SECURITY_GUARD_DEFAULTS`
  - `RESOURCE_CAPABILITY_NOT_EXACT`
  - `REQUIRED_DOCKER_RUNTIME_EVIDENCE_BLOCKED`
- cycle_record_action: `create`
- source_mirror_sync: `not-required`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260827_1650_aiscc-p1-3-security-admission-runtime-broker-and-evidence-hold-1.cycle.md`

## admitted repository / Git provenance

The Executor safely corrected the prior commit-message defect through additive provenance.

```text
predecessor content-valid/message-defective commit:
a8797fdac43b4a8bc501ccdb3c86743541153319

additive corrective provenance commit:
68c60d304b5de273e68b2783c03c117ccf8dd719

parent of corrective commit:
a8797fdac43b4a8bc501ccdb3c86743541153319

history rewrite:
not run

remote mutation:
not run
```

The corrective commit path/message/parent validation is admitted as `EXECUTED_PASS`.

## admitted environment/bootstrap evidence

Admit:

```text
uv:
0.12.6

uv-managed CPython:
3.12.14

.python-version:
3.12.14

Docker Engine:
28.3.3 / Linux containers / linux-amd64

Docker Compose:
v2.39.2-desktop.1

bootstrap:
55/55 Human-accepted paths created

uv.lock:
2877B2C17E45750C6CD18F6A67E3FF78855C8CD98AB65E48873979C5EB0822E6

uv sync --frozen:
PASS

uv build:
PASS

ruff lint:
PASS

ruff format check:
PASS

mypy --strict:
PASS

unit/integration tests:
14 PASS
```

Docker sandbox base:

```text
python:3.12.14-slim-bookworm
digest:
sha256:0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579
```

No P1-4/P1-5/provider/deployment/credential scope expansion was reported.

## admitted implementation strengths

The submitted candidate establishes useful P1-3 building blocks that SHOULD be retained unless a
direct contradiction is found:

- exact 9-state `WorkflowSnapshot` fixture/interface;
- exact eleven `SecurityActionClass` values;
- action × WorkflowState matrix;
- `RUN_EXECUTION_SIDE_EFFECT → RUNNING only`;
- versioned RuntimeMode profile model;
- `Capability` state/version/action/resource/expiry/use/revocation fields;
- requester/session/target-bound `PublicRunControlGrant`;
- cancel idempotency store;
- budget/idempotency/throttle primitives;
- deterministic decision provenance/redaction;
- bounded host-process timeout/retry/cancel primitive;
- Docker hardening arguments:
  - read-only rootfs;
  - tmpfs;
  - drop all capabilities;
  - no-new-privileges;
  - non-root UID/GID;
  - PID/memory/CPU limits;
  - default `--network none`;
- run labels and ownership-checked cleanup;
- internal Docker network helper;
- exact 55-path bootstrap boundary.

These strengths do not make P1-3 acceptable while the following load-bearing gaps remain.

---

# HOLD issue A — SecurityAdmission does not gate runtime side effects

Accepted P1-3 integration shape requires:

```text
SecurityPolicy / SecurityAdmission
→ admitted short-lived capability
→ runtime adapter
→ bounded side effect
```

The candidate does not enforce this.

Observed source behavior:

```text
DockerRuntime.command(...)
→ executes arbitrary docker CLI args
→ no Capability required

DockerRuntime.secure_run_args(...)
→ constructs process/container execution
→ no Capability required

BoundedProcessRunner.run(...)
→ executes arbitrary argv
→ no Capability required
```

`Capability` exists but is used only by tests/unit validation. Runtime execution does not consume it.

The runtime tests themselves call the raw Docker/process helpers directly.

Therefore:

```text
SecurityAdmissionDecision = DENY
does not mechanically prevent
runtime/process/docker side effect
```

This is a load-bearing security admission bypass.

Required rework invariant:

```text
NORMAL RUNTIME SIDE EFFECT
→ admitted capability required
→ capability freshly validated against current WorkflowSnapshot
→ exact action/resource/run/profile scope matches
→ capability consumption recorded
→ then bounded runtime adapter may execute

NO VALID ADMITTED CAPABILITY
→ NO SIDE EFFECT
```

System-owned safety cleanup/recovery may use a separately explicit safety capability/action class,
not a generic raw runtime bypass.

Raw Docker/subprocess invocation may exist only as a private/internal implementation primitive that
cannot be reached as the normal execution API.

---

# HOLD issue B — security guard inputs fail open by default

Current `PermissionRequest` defines security guards such as:

```text
requester_authorized=True
task_scope_allowed=True
resource_capability=True
limits_valid=True
budget_allowed=True
idempotency_allowed=True
target_control_authorized=True
```

This makes missing System evidence equivalent to passing the guard.

That contradicts the accepted invariant:

```text
unknown / ambiguous permission
→ DENY
```

and:

```text
Agent/caller claim
!= System-admitted authority
```

The HTTP candidate endpoint also copies caller-supplied state into both:

```text
observed
authoritative
```

which must never be treated as actual System-owned authoritative state.

Required correction:

- security-critical guard/admission inputs must be explicit and fail closed;
- omitted/unresolved requester/task/resource/limit/budget/idempotency/control authority → DENY;
- caller/public input cannot manufacture `authoritative` WorkflowSnapshot;
- an inert diagnostic endpoint may remain, but it must not produce an authoritative ALLOW solely
  from caller-supplied state and default-true guard values;
- future P1-4 owns authoritative state, so P1-3 may use an explicit trusted test/system context
  interface without implementing the P1-4 kernel.

---

# HOLD issue C — resource capability is boolean, not an exact capability/selector

P1-2/P1-3 require deny-by-default resource admission and executable public Live hard prohibitions.

Current candidate effectively uses:

```text
resource_domain in profile.resources
AND
resource_capability == True
AND
scenario fixed
AND
resource_id does not start with owner:/external:/shell:
```

This is not an exact resource capability.

A caller/internal bug can provide:

```text
resource_capability=True
```

for a known domain with an arbitrary `resource_id`.

The submitted source does not yet encode an exact server-owned selector/grant for:

- fixed synthetic repository/workspace;
- allowed process/sandbox resource;
- allowed local network fixture/equivalent runtime network capability;
- future provider/model resource boundary;
- other mutable resource IDs.

Required correction:

```text
boolean resource_capability
→ NOT sufficient

RESOURCE ALLOW
→ typed/versioned System-owned resource grant or exact policy selector
→ exact domain
→ exact resource ID/pattern owned by policy
→ exact mode/profile/scenario
→ capability freshness/scope
```

Where P1-5 or later ownership is required, the current P1-3 policy MUST fail closed rather than
inventing provider/tool authority.

Public Live hard prohibitions must be executable policy, not blacklist prefixes.

---

# HOLD issue D — required Docker runtime evidence is blocked

The Executor correctly did not substitute unit/static evidence.

Reported runtime result:

```text
runtime suite:
2 passed / 8 failed

failure boundary:
Docker OCI container creation

symptoms:
resource temporarily unavailable
pthread_create failed
OCI shim creation failure
unpigz thread creation failure
```

A plain unconstrained Python container also failed.

Read-only environment observation reported unrelated pre-existing container:

```text
admin-platform-edge-1
≈ 49,610 PIDs
```

The Executor did not stop/restart unrelated containers or Docker Desktop.

That was correct.

P1-3 still lacks admitted proof for:

- action-state/cancel runtime path using the real admission broker;
- filesystem/process isolation;
- network deny/allow;
- secret non-exposure Docker harness;
- Docker cancel;
- complete cleanup/residue runtime behavior.

Environment repair MUST NOT be achieved by this Executor mutating unrelated workload.

Before mandatory Docker proof rerun:

```text
plain minimal Docker container start
→ PASS required
```

If it still fails:

```text
HUMAN_DOCKER_ENVIRONMENT_REPAIR_REQUIRED
```

Human decides how to restore Docker/PID capacity.

---

# proof admission

| Evidence | Admission |
|---|---|
| additive corrective Git provenance | `EXECUTED_PASS` |
| uv/Python/Docker environment inventory | `EXECUTED_PASS` |
| 55-path runtime bootstrap | `EXECUTED_PASS` |
| lock/build/lint/format/mypy | `EXECUTED_PASS` |
| unit/integration 14 tests | `EXECUTED_PASS` |
| action/state model source | `REWORK_CANDIDATE` |
| cancel grant/idempotency source | `REWORK_CANDIDATE` |
| Docker hardening source | `REWORK_CANDIDATE` |
| runtime security admission coupling | `FAIL_REWORK_REQUIRED` |
| fail-closed guard provenance | `FAIL_REWORK_REQUIRED` |
| exact resource capability enforcement | `FAIL_REWORK_REQUIRED` |
| filesystem/process isolation runtime | `BLOCKED_REQUIRED_EVIDENCE` |
| network runtime | `BLOCKED_REQUIRED_EVIDENCE` |
| secret Docker runtime | `BLOCKED_REQUIRED_EVIDENCE` |
| timeout/cancel Docker runtime | `BLOCKED_REQUIRED_EVIDENCE` |
| cleanup/residue full runtime | `BLOCKED_REQUIRED_EVIDENCE` |
| Human verification | `DEFERRED_BY_REWORK` |

## proof non-substitution

```text
Capability class exists
!= runtime requires Capability

boolean says authorized
!= System-owned authorization evidence

known ResourceDomain
!= exact resource capability

unit SecurityPolicy test
!= denied side effect mechanically impossible

Docker command hardening args
!= Docker isolation runtime proof

plain Docker host failure
!= application assertion failure
```

---

# command-center judgment

```text
P1-3:
HOLD_REWORK_REQUIRED

narrow rework scope:
1. SECURITY_ADMISSION_RUNTIME_BINDING
2. FAIL_CLOSED_GUARD_PROVENANCE
3. EXACT_RESOURCE_CAPABILITY
4. RUNTIME_EVIDENCE_RERUN_WHEN_DOCKER_HEALTHY

P1-3 Human final review:
DEFERRED

P1-4:
NOT_STARTED / BLOCKED
```

Do not discard the current 55-path implementation candidate.
Rework it in place within the accepted bootstrap.

---

# preservation

Preserve exact commits:

- `a8797fdac43b4a8bc501ccdb3c86743541153319`
- `68c60d304b5de273e68b2783c03c117ccf8dd719`

Preserve exact canonical/provenance paths:

- `.aiassistant/rules/AISCC_RUNTIME_SUBSTRATE.md`
- `.aiassistant/tasks/done/20260827_1545_aiscc-p1-3-security-runtime-safeguard-implementation-with-additive-commit-recovery-1.md`
- `.aiassistant/records/aiscc/cycles/20260827_1650_aiscc-p1-3-security-admission-runtime-broker-and-evidence-hold-1.cycle.md`

Preserve all 55 P1-3 candidate runtime/source/test/config/container paths pending rework judgment.

Temporary target export/evidence may be replaced by the rework export after durable Task/Cycle
provenance is safely persisted.

---

# next action

```text
P1-3 narrow rework
→ persist previous done Task + this HOLD Cycle
→ bind admitted capability to every normal runtime side effect
→ make security guard inputs fail closed
→ replace boolean resource capability with exact typed/policy-owned grant/selector
→ rerun static/unit/integration
→ preflight plain Docker start
→ if healthy, rerun all mandatory Docker runtime proof
→ Human P1-3 review only after required evidence passes
```

Do not execute P1-4.
