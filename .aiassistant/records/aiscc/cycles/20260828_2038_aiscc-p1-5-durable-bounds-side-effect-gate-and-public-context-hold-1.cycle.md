# AISCC Cycle Record

## meta

- cycle_id: `20260828_2038_aiscc-p1-5-durable-bounds-side-effect-gate-and-public-context-hold-1`
- date: `2026-08-28 20:38 KST`
- primary_semantic_owner: `P1-5 durable bounded execution + exact pre-side-effect authority`
- work_type: `IMPLEMENTATION_AND_RUNTIME_VERIFICATION / REWORK_JUDGMENT`
- execution_mode: `MANUAL_COMMAND_CENTER`
- predecessor_task: `20260828_1823_aiscc-p1-5-durable-execution-public-live-continuation-and-secret-lease-rework-1`
- predecessor_executor_result: `ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING`
- predecessor_HEAD: `3312e24b60e0bd10b7c859546d6fdfa3bd2cb025`
- predecessor_candidate_count: `42`
- predecessor_candidate_aggregate_sha256: `ef6dd8d9d226fdf9e2f13f51b28ba87898bff6cfbd56f1921b9f587eea602f37`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause:
  - `DURABLE_EXECUTION_BOUNDS_ARE_PROCESS_LOCAL_AND_NOT_ENFORCED_ON_EXECUTE_PATH`
  - `TOOL_SIDE_EFFECT_USES_STALE_WORKRUN_SNAPSHOT`
  - `TOOL_DISPATCH_STARTED_PRECEDES_EXACT_CAPABILITY_CONSUMPTION`
  - `PRE_SIDE_EFFECT_DENIAL_DOES_NOT_TERMINALIZE_OPERATION_IMMEDIATELY`
  - `WORKFLOW_LEFT_RUNNING_FAILURE_CANNOT_BE_DURABLY_CLOSED`
  - `PUBLIC_BOUNDED_LIVE_FIXED_REPOSITORY_CONTEXT_NOT_AUTHORITY_BOUND`
- P1_5_runtime_status: `NOT_ACCEPTED`
- P1_6_status: `NOT_STARTED`
- cycle_record_action: `create`
- source_mirror_sync: `not-required`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260828_2038_aiscc-p1-5-durable-bounds-side-effect-gate-and-public-context-hold-1.cycle.md`

## admitted predecessor evidence

### provenance

Admit Executor-reported provenance:

```text
P1_5_RUNTIME_REWORK_BASE_COMMIT:
3312e24b60e0bd10b7c859546d6fdfa3bd2cb025

parent:
3b150181f1c008d0b95fd53a32cb6e62d174ab4f

predecessor terminal Cycle blob:
09f086ba984e4946da9b58b0f5372bae72402a243b205cb83993d6f4f4717cf0

predecessor report-only wrong digest:
09f086ba54327e3c96b46adbba1c5849d7c43f8fd382782fd515a73e9b7d7cf0

classification:
REPORT_TRANSCRIPTION_ONLY
```

The exact predecessor Task bytes were preserved and the Stage-0 provenance commit was reported as an
exact two-path additive commit with no remote mutation.

### candidate identity

The submitted export contains exactly:

```text
42 candidate paths

aggregate SHA-256:
ef6dd8d9d226fdf9e2f13f51b28ba87898bff6cfbd56f1921b9f587eea602f37
```

Every candidate path SHA-256 and the aggregate were independently recomputed from the submitted ZIP:

```text
42 / 42:
PASS
```

### previous HOLDs now corrected

Retain as corrected:

```text
PUBLIC_BOUNDED_LIVE
→ PROVIDER / TOOL / SECRET profile eligibility added

production durable AgentExecutionService.execute:
implemented

local durable Responses protocol body:
implemented / restart-readable

caller continuation:
not authoritative

SecretResolutionLease:
implemented

raw secret_ref resolver interface:
removed from production resolution boundary

ToolDefinition exact ResourceRequirement:
implemented

same-domain / wrong-resource tool capability:
DENY

OWNER + PUBLIC_BOUNDED_LIVE two-round local fake provider/tool restart proof:
PASS

private protocol missing/body/order/call_id corruption:
fail closed before second provider invocation

P1-6:
not implemented
```

### retained verification

Executor-reported:

```text
uv sync --frozen --all-groups:
PASS

uv build:
PASS

ruff:
PASS

mypy --strict:
PASS

unit + integration:
126 PASS

PostgreSQL integration:
38 PASS

OWNER + PUBLIC_BOUNDED_LIVE durable two-round restart:
2 PASS

P1-3 Docker security + P1-5 runtime:
20 PASS

PostgreSQL:
17.6

Alembic head:
20260828_0002

real provider calls:
0

final Task-owned residue:
0
```

These remain regression evidence for the components they actually exercise.

## HOLD A — durable AgentExecutionService does not enforce durable profile bounds

The accepted P1-5 design requires server-owned finite bounds for:

```text
provider calls
agent rounds
tool calls
provider retry
wall time
output/token size
budget
```

The current `ExecutionAttemptRow` has a `counters` JSON projection, but `create_attempt()` initializes:

```text
counters={}
```

and no production repository method updates or reconstructs those counters.

Current durable:

```text
AgentExecutionService.execute(...)
```

increments only process-local:

```text
self.counters.provider_calls
self.counters.rounds
self.counters.tool_calls
self.counters.budget_units
```

The bound functions:

```text
_check_bounds()
admit_output()
admit_tool_side_effect()
admit_provider_retry()
_check_open_and_time()
```

are used by the older synchronous `execute_provider()` component path, not by the authoritative
durable `execute()` path.

The durable `execute()` path also does not persist/reconstruct:

```text
provider call count
round count
tool call count
retry count
budget units
output bytes/tokens
total wall-clock execution deadline
```

Therefore:

```text
service object recreation
→ counters reset
→ profile maxima can be bypassed
```

The accepted restart proof actually recreates the service between provider rounds, proving that the
current process-local counters are not the durable authority.

The existing `BOUNDED_LOOP` tests exercise component counters rather than the production durable
entrypoint.

Required invariant:

```text
restart
!= bound reset
```

## HOLD B — state/version is not revalidated before every side effect

The durable loop reloads `WorkRun` once at the beginning of a provider round.

After the provider returns a tool call, it calls:

```text
_execute_durable_tool(
    current=<snapshot loaded before provider side effect>,
    attempt=<same old attempt ref>,
    ...
)
```

without reloading authoritative `WorkRun/state_version`.

Thus a workflow transition occurring while the provider call is in flight can leave:

```text
current snapshot:
RUNNING/vN

actual WorkRun:
non-RUNNING or vN+1
```

and the tool path still attempts to create P1-3 grants/capabilities from the stale snapshot.

P1-3 in-memory `SecurityPolicy` cannot independently read PostgreSQL authoritative WorkRun; it trusts
the snapshot supplied to it.

Required:

```text
before each provider side effect
→ reload authoritative WorkRun/attempt

after provider result and before any tool side effect
→ reload authoritative WorkRun/attempt again

state/version mismatch or WorkflowState != RUNNING
→ zero new side effect
→ execution attempt fails truthfully
```

## HOLD C — Tool DISPATCH_STARTED is recorded before exact capability validation/consumption

Current durable tool path:

```text
create PREPARED
→ issue candidate capabilities
→ advance SECURITY_ADMITTED
→ advance DISPATCH_STARTED
→ ToolRegistryBroker.dispatch_candidate(...)
     exact capability matching
     atomic capability consumption
     optional secret lease resolution
     dispatcher side effect
```

This reverses the accepted operation semantics.

`DISPATCH_STARTED` is supposed to mean the boundary immediately before actual adapter/dispatcher
crossing after all required security authority is admitted/consumed.

With the current code, an exact-resource mismatch or atomic capability consume failure occurs after
the operation is already marked `DISPATCH_STARTED`.

A later recovery therefore records:

```text
OUTCOME_UNKNOWN
```

even though the dispatcher was definitely never invoked.

Required exact ordering:

```text
PREPARED
→ exact selector/grant/capability construction

security/requirement failure
→ OUTCOME_KNOWN(DENIED_BEFORE_SIDE_EFFECT)
→ no DISPATCH_STARTED

valid exact requirements
→ SECURITY_ADMITTED

atomic capability consume failure / pre-dispatch cancel
→ OUTCOME_KNOWN(CANCELLED)
→ no DISPATCH_STARTED

successful exact consume
→ create required secret lease
→ final WorkRun/state/version recheck
→ DISPATCH_STARTED immediately before dispatcher/resolver side-effect boundary
→ side effect
```

The Tool broker must expose an admitted/prepared dispatch boundary or equivalent; test code must not
substitute.

## HOLD D — provider pre-side-effect denial can leave PREPARED operation + RUNNING attempt

In the durable provider path:

```text
create_operation(PREPARED)
→ _provider_capabilities(...)
```

`_provider_capabilities()` / `_issue_capability()` may raise on:

```text
selector authority denial
ResourceGrant denial
P1-3 SecurityDecision denial
Capability issuance denial
```

There is no local catch that immediately records:

```text
OUTCOME_KNOWN(DENIED_BEFORE_SIDE_EFFECT)
EXECUTION_FAILED
```

The operation remains `PREPARED` and the attempt remains `RUNNING` until a later call/restart invokes
the recovery path.

That violates the accepted immediate known pre-side-effect outcome semantics.

Required:

```text
known pre-side-effect denial in current invocation
→ durable known denial before returning
→ no side effect
→ attempt terminalized exactly once
```

Recovery is for crash/interruption, not normal control flow.

## HOLD E — current repository cannot record WORKFLOW_LEFT_RUNNING failure

`PostgresExecutionRepository.transition_attempt()` currently requires:

```text
WorkRun.workflow_state == RUNNING
```

for every execution lifecycle mutation.

`advance_operation()` also requires RUNNING/current causal state for every edge.

But accepted P1-5 design says:

```text
RUNNING attempt
+ authoritative workflow leaves RUNNING
→ no new execution side effect
→ attempt becomes EXECUTION_FAILED
→ failure class WORKFLOW_LEFT_RUNNING
```

The current repository cannot persist that failure after the authoritative WorkRun has already left
RUNNING.

Required narrow safety-closure semantics:

```text
non-RUNNING WorkRun
→ never admit start/complete/new side-effect progression

but
→ allow only exact fail-closed terminalization of an already-RUNNING attempt
   and its nonterminal operation(s)

failure_class:
WORKFLOW_LEFT_RUNNING

no WorkflowState/state_version mutation
no new provider/tool/secret side effect
```

Do not permit general execution lifecycle mutation outside RUNNING.

## HOLD F — Public Bounded Live fixed repository/version is not authority-bound

The accepted P1-2/P1-5 boundary is:

```text
PUBLIC_BOUNDED_LIVE
→ fixed synthetic repository/version
→ fixed scenario
→ server-fixed provider/model/profile/tool registry
```

Current positive integration binds:

```text
RuntimeMode
scenario_id
ProviderProfile
ToolRegistry
```

but `AgentExecutionService.execute()` has no server-owned repository/version authority input and
obtains no exact P1-3 `ResourceDomain.REPOSITORY` / `SCENARIO` admission for the P1-5 public context.

The positive test creates a generic WorkRun and passes:

```text
scenario_id="p1-5-fixed-synthetic"
```

There is no production assertion that the run is bound to the accepted P1-5 synthetic repository
identity/version.

Required:

```text
PUBLIC_BOUNDED_LIVE
→ exact server-owned public execution context
→ exact synthetic repository identity/version
→ exact scenario identity/version
→ exact P1-3 REPOSITORY + SCENARIO authority
→ then P1-5 provider/tool execution
```

Caller/public input cannot choose or replace those identities.

Wrong repository/version/scenario must deny before provider/tool/secret side effects.

Replay remains zero execution.

## evidence integrity judgment

The report claims:

```text
Required proof classes passed:
...
BOUNDED_LOOP
MODE_SECURITY
...
```

But the source shows:

```text
component-local counter tests
!= durable execute() bound enforcement

fixed mode/scenario test
!= fixed repository/version authority
```

Therefore these two proof-class claims are not admitted as complete.

This is an evidence-scope defect caused by missing production behavior, not merely report wording.

## Command Center judgment

```text
predecessor terminal hash correction:
PASS / CLOSED

42-path export identity:
PASS

Public Live PROVIDER/TOOL/SECRET positive path:
PASS / RETAIN

durable local continuation body/restart:
PASS / RETAIN

SecretResolutionLease:
PASS / RETAIN

exact Tool resource matching:
PASS / RETAIN

durable AgentExecutionService composition:
PARTIAL / RETAIN

durable bounded-loop enforcement:
HOLD_REWORK_REQUIRED

per-side-effect WorkRun freshness:
HOLD_REWORK_REQUIRED

tool dispatch phase ordering:
HOLD_REWORK_REQUIRED

immediate pre-side-effect denial terminalization:
HOLD_REWORK_REQUIRED

WORKFLOW_LEFT_RUNNING safety closure:
HOLD_REWORK_REQUIRED

fixed Public Live repository/version authority:
HOLD_REWORK_REQUIRED

P1-5 runtime:
NOT ACCEPTED

P1-6:
NOT_STARTED
```

## proof non-substitution

```text
ExecutionAttempt.counters column exists
!= counters are authoritative

process-local counter
!= restart-durable bound

one WorkRun reload per provider round
!= revalidation before every side effect

SECURITY_ADMITTED event
!= capabilities successfully consumed

DISPATCH_STARTED event
!= dispatcher boundary if security checks still follow

recovery can close PREPARED later
!= normal denial terminalized now

fixed scenario string
!= fixed synthetic repository/version authority

126 tests PASS
!= untested durable bound bypass accepted
```

## preservation

Preserve exact commit:

- `3312e24b60e0bd10b7c859546d6fdfa3bd2cb025`

Preserve exact predecessor/current candidate identity:

```text
42 paths
ef6dd8d9d226fdf9e2f13f51b28ba87898bff6cfbd56f1921b9f587eea602f37
```

Preserve exact paths:

- `.aiassistant/tasks/done/20260828_1823_aiscc-p1-5-durable-execution-public-live-continuation-and-secret-lease-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260828_2038_aiscc-p1-5-durable-bounds-side-effect-gate-and-public-context-hold-1.cycle.md`
- all exact 42 current P1-5 candidate paths.

## next action

```text
P1-5 final narrow runtime integration rework
→ durable counters/deadline/limits
→ exact pre-side-effect WorkRun freshness
→ correct security-admitted/dispatch-start ordering
→ immediate denial terminalization
→ workflow-left-running safety closure
→ fixed Public Live repository/scenario authority
→ full restart/concurrency/security regression
```

Do not start P1-6.
