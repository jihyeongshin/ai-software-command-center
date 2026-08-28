# AISCC Cycle Record

## meta

- cycle_id: `20260828_1823_aiscc-p1-5-runtime-integration-public-live-and-continuation-authority-hold-1`
- date: `2026-08-28 18:23 KST`
- primary_semantic_owner: `P1-5 executable provider/tool execution path`
- work_type: `IMPLEMENTATION_AND_RUNTIME_VERIFICATION / REWORK_JUDGMENT`
- execution_mode: `MANUAL_COMMAND_CENTER`
- predecessor_task: `20260828_1529_aiscc-p1-5-provider-tool-execution-implementation-and-runtime-verification-1`
- predecessor_executor_result: `ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING`
- predecessor_HEAD: `3b150181f1c008d0b95fd53a32cb6e62d174ab4f`
- predecessor_candidate_count: `40`
- predecessor_candidate_aggregate_sha256: `3f944acf3e0941418a955ca1e60aeb23a78271122569baa3ed2580962ce666bd`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause:
  - `PUBLIC_BOUNDED_LIVE_P1_5_RESOURCE_DOMAINS_NOT_ADMISSIBLE`
  - `EXECUTION_COMPONENTS_NOT_COMPOSED_INTO_DURABLE_AGENT_LOOP`
  - `LOCAL_DURABLE_CONTINUATION_NOT_ENFORCED_ON_PROVIDER_PATH`
  - `SECRET_RESOLVER_DOES_NOT_VERIFY_CONSUMED_SECRET_AUTHORITY`
  - `TOOL_UNDERLYING_RESOURCE_BINDING_IS_DOMAIN_ONLY`
  - `EXECUTOR_REPORT_TERMINAL_CYCLE_HASH_MISSTATED`
- P1_5_runtime_status: `NOT_ACCEPTED`
- P1_6_status: `NOT_STARTED`
- cycle_record_action: `create`
- source_mirror_sync: `not-required`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260828_1823_aiscc-p1-5-runtime-integration-public-live-and-continuation-authority-hold-1.cycle.md`

## admitted predecessor evidence

### Stage 0

Admit reported Stage-0 identity subject to the exact commit-object hash recheck required by the next Task:

```text
P1_5_IMPLEMENTATION_BASE_COMMIT:
3b150181f1c008d0b95fd53a32cb6e62d174ab4f

parent:
d96949f3643e6a0610942e33d70e9da259e1e432

Stage-0 committed path count:
6

accepted design SHA-256:
12070677aa1cfa74b7eea9a52db24f78aacd2bf23d655f125a7689797d172443

post-Stage-0 Git writes:
0
```

### candidate identity

Exact exported P1-5 candidate:

```text
path count:
40

aggregate SHA-256:
3f944acf3e0941418a955ca1e60aeb23a78271122569baa3ed2580962ce666bd
```

All 40 exported path hashes and the aggregate were independently recomputed from the submitted
bundle and matched its manifest.

### retained implementation strengths

Retain:

```text
ExecutionStatus exact set:
NOT_STARTED
RUNNING
EXECUTOR_COMPLETED
EXECUTION_FAILED

operation phases/outcomes:
implemented

P1-5 provider/tool selector authority:
implemented

P1-5 secret-use selector authority:
implemented

P1-3 atomic multi-capability consume:
implemented

PostgreSQL ExecutionAttempt/Operation/Event projections:
implemented

append-only execution provenance triggers:
implemented

OpenAI Responses adapter:
official SDK + local fake endpoint only

Responses flags:
store=false
background=false
stream=false
parallel_tool_calls=false
truncation=disabled

Replay zero-execution service:
implemented

P1-4 execution ref validation boundary:
implemented

P1-6:
not implemented
```

### retained verification

Executor-reported evidence:

```text
uv sync --frozen --all-groups:
PASS

uv build:
PASS

ruff:
PASS

mypy --strict:
PASS

full unit + integration:
122 PASS

P1-3 Docker runtime regression:
10 PASS

P1-5 runtime proof before residue:
9 PASS

P1-5 final residue:
1 PASS

PostgreSQL:
17.6

Alembic head:
20260828_0002

real provider calls:
0

final Task-owned container/network/process/workspace residue:
0
```

These remain useful regression evidence for unchanged behavior, but they do not substitute for the
missing integrated execution proof below.

## HOLD A — PUBLIC_BOUNDED_LIVE cannot obtain P1-5 resource grants

Current P1-3 `default_profiles()` defines PUBLIC_BOUNDED_LIVE resources as:

```text
FILESYSTEM
PROCESS
NETWORK
REPOSITORY
SCENARIO
```

It does not include:

```text
PROVIDER
TOOL
SECRET
```

Yet `SecurityPolicy.issue_resource_grant()` requires:

```text
scope.domain in profile.resources
```

before the P1-5 selector extension is even consulted.

Therefore a valid fixed PUBLIC_BOUNDED_LIVE provider/tool/secret selector cannot produce a P1-3
ResourceGrant.

The P1-5 ProviderProfile and ToolRegistry both declare PUBLIC_BOUNDED_LIVE as allowed, but the P1-3
permission profile makes the positive path unreachable.

The runtime test named:

```text
test_public_live_is_fixed_profile_scenario_only_and_still_requires_capabilities
```

only calls the service with:

```text
capabilities=()
```

and proves denial/fixed-context behavior. It does not prove one valid PUBLIC_BOUNDED_LIVE provider or
tool execution.

Required invariant:

```text
PUBLIC_RECORDED_REPLAY
→ PROVIDER / TOOL / SECRET remain non-executable

PUBLIC_BOUNDED_LIVE
+ exact P1-5 server-owned selector
+ exact P1-3 guards
→ PROVIDER / TOOL / SECRET may be admitted for the fixed synthetic scenario only
```

This must be implemented without weakening any other P1-3 guard.

## HOLD B — AgentExecutionService is not the accepted durable bounded agent loop

Current `AgentExecutionService` receives:

```text
ProviderCall
+ already-created CapabilityConsumeRequest tuple
```

then validates current state and directly calls:

```text
consume capabilities
→ secret resolver
→ provider adapter
```

It does not own/integrate:

- `PostgresExecutionRepository`;
- provider/tool selector authorities;
- P1-3 ResourceGrant/PermissionRequest/Capability creation;
- durable PREPARED operation creation;
- durable SECURITY_ADMITTED edge;
- durable DISPATCH_STARTED edge;
- durable known/unknown outcome admission;
- ToolRegistryBroker;
- tool output persistence;
- durable continuation loading;
- AgentOutputRef persistence;
- ExecutionSubmissionRef creation;
- attempt completion/failure.

The runtime ambiguous-outcome test manually calls repository methods around the adapter from test code.

Therefore:

```text
repository component works
+
adapter component works
+
service bound counters work
!=
accepted durable AgentExecutionService loop implemented
```

A production P1-5 entrypoint must compose these authorities so the side effect cannot occur outside
the durable operation protocol.

## HOLD C — local durable Responses continuation is not authoritative on the production path

`validate_continuation()` exists in `openai_responses.py`, but production code does not call it.

Its only current callers are tests.

`ProviderCall.input_items` is accepted directly by the adapter and serialized directly into the
Responses request.

The persistence layer stores metadata:

```text
item_hash
call_id
encrypted_body_ref
byte_count
```

but no production component loads the exact durable private protocol body and reconstructs the next
provider request from that durable state.

Therefore after restart there is no implemented path proving:

```text
AISCC durable local protocol history
→ sole continuation authority
```

and no production path by which missing/corrupt durable continuation prevents the next provider call.

Required:

```text
continuation request
→ load exact durable private protocol payload
→ verify hashes/order/type/call_id/bounds
→ reconstruct exact input items
→ only then create ProviderCall / cross adapter boundary
```

Raw caller-provided continuation items cannot substitute.

## HOLD D — secret resolver cannot verify consumed SECRET authority

Accepted design requires the private resolver to receive/verify an exact consumed SECRET authority
before material resolution.

Current port is:

```text
SecretResolver.resolve(secret_ref: str) -> str
```

The service consumes capabilities first, but the resolver receives only the opaque ref.

Therefore the resolver has no way to prove that this particular resolution is bound to:

- the exact consumed SECRET capability;
- principal/run/attempt;
- state/version;
- operation fingerprint;
- purpose/destination;
- use ordinal.

Required:

```text
successful atomic capability consumption
→ unforgeable/broker-issued secret-resolution lease/receipt
→ private resolver verifies exact lease
→ only then material resolution
```

A raw `secret_ref` alone must be insufficient to invoke the resolver.

## HOLD E — ToolDefinition binds underlying resources only by domain

Current `ToolDefinition` carries:

```text
underlying_resource_domains: frozenset[ResourceDomain]
```

Current broker verifies only that required domains are present and every supplied capability uses the
same operation fingerprint.

It does not compare supplied underlying capabilities with an exact server-owned resource identity or
SecretRequirement because the registry model does not carry those exact requirements.

This is weaker than the accepted design:

```text
ToolDefinition
→ exact server-owned underlying resource requirements
→ separate exact P1-3 capability for each resource
```

Required:

```text
same domain + wrong resource identity
→ DENY before dispatcher
```

For any secret-requiring tool:

```text
exact server-owned SecretRequirement
→ exact SecretUse attestation
→ exact SECRET capability/lease
```

The model/tool arguments never select those values.

## evidence integrity correction

The predecessor `EXECUTOR_REPORT.md` states the verified terminal Cycle SHA as:

```text
09f086ba54327e3c96b46adbba1c5849d7c43f8fd382782fd515a73e9b7d7cf0
```

but the Task's exact Stage-0 authority requires:

```text
09f086ba984e4946da9b58b0f5372bae72402a243b205cb83993d6f4f4717cf0
```

This may be a report-only transcription defect, because Stage 0 otherwise reported PASS.

The next Task MUST verify the actual blob committed at
`3b150181f1c008d0b95fd53a32cb6e62d174ab4f` before any new provenance commit.

If the committed blob does not match the Task-required SHA, stop.

## Command Center judgment

```text
P1-5 component implementations:
PASS / RETAIN

P1-5 PostgreSQL projections:
PASS / RETAIN

P1-5 adapter local fake transport:
PASS / RETAIN

Replay zero execution:
PASS / RETAIN

PUBLIC_BOUNDED_LIVE positive execution:
HOLD_REWORK_REQUIRED

durable integrated AgentExecutionService:
HOLD_REWORK_REQUIRED

durable continuation authority:
HOLD_REWORK_REQUIRED

secret resolution consumed-authority proof:
HOLD_REWORK_REQUIRED

exact Tool underlying-resource binding:
HOLD_REWORK_REQUIRED

P1-5 runtime:
NOT ACCEPTED

P1-6:
NOT_STARTED
```

## proof non-substitution

```text
selector port implemented
!= PUBLIC_BOUNDED_LIVE resource domain admitted

component test orchestration
!= production durable orchestration

validate_continuation helper
!= durable continuation authority enforced

consume SECRET capability before resolve
!= resolver verifies consumed authority

same ResourceDomain
!= exact server-owned underlying resource

122 tests PASS
!= missing required positive/integrated proof accepted
```

## preservation

Preserve exact commit:

- `3b150181f1c008d0b95fd53a32cb6e62d174ab4f`

Preserve exact candidate identity:

```text
40 paths
3f944acf3e0941418a955ca1e60aeb23a78271122569baa3ed2580962ce666bd
```

Preserve exact paths:

- `.aiassistant/tasks/done/20260828_1529_aiscc-p1-5-provider-tool-execution-implementation-and-runtime-verification-1.md`
- `.aiassistant/records/aiscc/cycles/20260828_1823_aiscc-p1-5-runtime-integration-public-live-and-continuation-authority-hold-1.cycle.md`
- all exact 40 predecessor P1-5 implementation candidate paths.

## next action

```text
P1-5 runtime narrow integration rework
→ verify predecessor terminal commit blob
→ enable exact PUBLIC_BOUNDED_LIVE P1-5 resource domains
→ compose one durable execution entrypoint
→ enforce durable local continuation authority
→ mediate secret resolution with consumed-authority lease
→ exact Tool underlying-resource binding
→ re-run complete P1-3/P1-4/P1-5 proof
```

Do not start P1-6.
