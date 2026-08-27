# AISCC Cycle Record

## meta

- cycle_id: `20260827_1650_aiscc-p1-3-runtime-mode-and-docker-read-boundary-hold-1`
- date: `2026-08-27 16:50 KST`
- primary_semantic_owner: `P1-3 security runtime broker final-source review + Docker evidence blocker`
- work_type: `SECURITY_SANDBOX_IMPLEMENTATION / REWORK_JUDGMENT`
- execution_mode: `MANUAL_COMMAND_CENTER`
- predecessor_task: `20260827_1650_aiscc-p1-3-security-admission-runtime-broker-fail-closed-and-evidence-rework-1`
- predecessor_result: `HUMAN_DOCKER_ENVIRONMENT_REPAIR_REQUIRED`
- predecessor_base_commit: `1b6e84bdbb0b632e59d60670d785d3c14392216e`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause:
  - `RUNTIME_MODE_CAPABILITY_BINDING_INCOMPLETE`
  - `DOCKER_READ_QUERY_AUTHORIZATION_BYPASS`
  - `DOCKER_RUNTIME_EVIDENCE_ENVIRONMENT_BLOCKED`
- cycle_record_action: `create`
- source_mirror_sync: `not-required`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260827_1650_aiscc-p1-3-runtime-mode-and-docker-read-boundary-hold-1.cycle.md`

## admitted predecessor evidence

### Stage 0 provenance

Admit:

```text
P1_3_REWORK_BASE_COMMIT:
1b6e84bdbb0b632e59d60670d785d3c14392216e

parent:
68c60d304b5de273e68b2783c03c117ccf8dd719

paths:
exact predecessor done Task + prior HOLD Cycle

history rewrite / remote mutation:
none
```

### source rework strengths

The predecessor corrected the three previously identified load-bearing gaps substantially:

1. boolean default-true security guards were removed;
2. unresolved/missing authority fields now fail closed;
3. public HTTP diagnostic cannot manufacture authoritative ALLOW;
4. `ResourceGrant` is typed, versioned, policy-issued, short-lived and exact-scope bound;
5. Public Live arbitrary owner/external/provider/tool selectors deny;
6. normal process/container/network side effects require a registered admitted capability;
7. capability use is centrally consumed and stale/wrong action/resource/run/profile cases deny;
8. safety cleanup is separated from normal execution capability;
9. static/build/type/unit/integration evidence passes;
10. 55-path bootstrap boundary remains intact.

These corrections are retained.

### static/build evidence

Admit:

```text
uv sync --frozen --all-groups:
PASS

uv build:
PASS

ruff check:
PASS

ruff format --check:
PASS

mypy --strict:
PASS

unit + integration:
22 PASS
```

This evidence is source/static/targeted proof only.

## Docker environment blocker

The mandatory health probe failed before container command execution:

```text
docker run --rm
python:3.12.14-slim-bookworm@
sha256:0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579
python -c "print('AISCC_DOCKER_HEALTH_OK')"
```

Failure:

```text
failed to start shim:
fork/exec /usr/bin/containerd-shim-runc-v2:
resource temporarily unavailable
```

Read-only observation:

```text
admin-platform-edge-1
≈ 49,612 PIDs
```

No unrelated container or Docker Desktop mutation was performed.

Admit:

```text
DOCKER_HEALTH_PREFLIGHT
→ EXECUTED_FAIL

Stage 4 runtime proof
→ NOT_EXECUTED

proof substitution
→ none
```

The environment blocker is real and remains unresolved.

## HOLD issue A — RuntimeMode is stored but not enforced at runtime consumption

Current `Capability` stores:

```text
mode: RuntimeMode
profile_version: str
```

However runtime consumption validates:

```text
issuer
registration
revocation
expiry
use count
principal
run
WorkflowSnapshot/state_version
profile_version
action
ResourceScope
```

but does not compare an authoritative/current `RuntimeMode` against `capability.mode`.

Current broker APIs also do not receive an explicit mode/runtime execution context.

This is load-bearing because current permission profiles share the same version string:

```text
OWNER_SELF_DOGFOOD       → p1-3-v2
PUBLIC_RECORDED_REPLAY   → p1-3-v2
PUBLIC_BOUNDED_LIVE      → p1-3-v2
```

Therefore:

```text
profile_version match
!= RuntimeMode match
```

An OWNER capability must never become executable in a PUBLIC_BOUNDED_LIVE or
PUBLIC_RECORDED_REPLAY execution context merely because principal/run/state/action/scope/profile
happen to match.

Required correction:

```text
RuntimeExecutionContext
or equivalent trusted broker input
→ principal
→ current RuntimeMode
→ authoritative WorkflowSnapshot/state_version
→ profile version

Capability consumption
→ current mode == capability.mode
→ otherwise DENY(CAPABILITY_MODE_MISMATCH)
```

Minimum invariant:

```text
CAPABILITY VALID
→ MODE MATCH
→ PROFILE MATCH
→ RUN/STATE/VERSION MATCH
→ ACTION/SCOPE MATCH
→ USE/EXPIRY/REVOCATION PASS
```

RuntimeMode remains separate from WorkflowState.

Do not add a WorkflowState or redefine P1-1 semantics.

## HOLD issue B — unrestricted Docker read queries bypass resource authorization

Current `DockerRuntime` exposes capability-free methods equivalent to:

```text
inspect(name)
inspect_format(name, arbitrary_format)
wait(name)
exists(name)
```

`docker inspect` is not security-neutral merely because it is read-only.

It may reveal:

```text
environment variables
container command/argv
mount paths
labels
network configuration
image metadata
```

for arbitrary sibling/unrelated containers.

This violates the accepted boundaries:

```text
per-run isolation
secret non-exposure
owner/private workspace isolation
public run visibility != broader resource authority
unknown/unproven resource access → DENY
```

Required correction:

- product runtime MUST NOT expose arbitrary container introspection by name without exact admitted
  read/safety authority;
- exact container/resource/run ownership must be validated before resource metadata is returned;
- `inspect_format` MUST NOT accept arbitrary format strings through a capability-free product API;
- cleanup ownership inspection may remain an internal/private primitive only after an exact safety
  capability has been admitted;
- fixed Docker environment diagnostics such as a narrowly-scoped `docker info --format {{.OSType}}`
  may remain an internal preflight helper because they do not select arbitrary run resources;
- evidence harness may use a test-only external observer to inspect resources it created for proof,
  but that observer:
  - is not a product runtime API,
  - is not an authorization path,
  - cannot be represented as PUBLIC_BOUNDED_LIVE authority.

Minimum invariant:

```text
ARBITRARY CONTAINER NAME
+ NO EXACT READ/SAFETY CAPABILITY
→ NO PRODUCT-RUNTIME INSPECTION
```

and:

```text
READ_ONLY
!= AUTHORIZED
```

## source issue not promoted to blocker — authority producer ownership

`AuthorityStatus` is now explicit and fail-closed, but authoritative producers for requester/task/
budget/idempotency etc. are not yet implemented.

This is acceptable only because:

- the public diagnostic endpoint is deny-only;
- P1-3 does not claim those future owner systems are implemented;
- P1-4/P1-6/P1-7 remain separate.

Future integration MUST NOT treat arbitrary caller-created `AuthorityStatus.GRANTED` as System
admission evidence.

This risk must remain explicit in the P1-4/P1-6/P1-7 handoff.

## command-center judgment

```text
previous HOLD A-C source correction:
PASS / RETAIN

RuntimeMode capability binding:
HOLD_REWORK_REQUIRED

Docker read-query authorization:
HOLD_REWORK_REQUIRED

Docker health:
HUMAN_DOCKER_ENVIRONMENT_REPAIR_REQUIRED

mandatory runtime evidence:
BLOCKED_REQUIRED_EVIDENCE

P1-3:
NOT ACCEPTED

Human P1-3 final review:
DEFERRED

P1-4:
NOT_STARTED / BLOCKED
```

## proof non-substitution

```text
Capability carries mode
!= broker validates current mode

same profile version
!= same RuntimeMode authority

read-only Docker query
!= authorized resource read

unit test
!= Docker isolation/runtime proof

Docker health failure
!= application/security runtime failure

static broker correctness
!= accepted P1-3 runtime enforcement
```

## preservation

Preserve exact commits:

- `a8797fdac43b4a8bc501ccdb3c86743541153319`
- `68c60d304b5de273e68b2783c03c117ccf8dd719`
- `1b6e84bdbb0b632e59d60670d785d3c14392216e`

Preserve exact paths:

- `.aiassistant/rules/AISCC_RUNTIME_SUBSTRATE.md`
- `.aiassistant/tasks/done/20260827_1650_aiscc-p1-3-security-admission-runtime-broker-fail-closed-and-evidence-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260827_1650_aiscc-p1-3-runtime-mode-and-docker-read-boundary-hold-1.cycle.md`

Preserve all current 55 P1-3 runtime/security source/test/config/container candidate paths.

Do not delete or revert the corrected predecessor candidate.

## next action

```text
P1-3 narrow rework:
1. persist this HOLD provenance
2. bind RuntimeMode into capability consumption/runtime broker
3. close arbitrary Docker read-query product API
4. static/build/unit/integration revalidation
5. Docker health probe
6. if healthy → execute all mandatory runtime evidence
7. if unhealthy → HUMAN_DOCKER_ENVIRONMENT_REPAIR_REQUIRED
```

Do not execute P1-4.
