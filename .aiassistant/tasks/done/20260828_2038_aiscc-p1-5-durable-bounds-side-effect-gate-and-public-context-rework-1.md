# 작업지시서: P1-5 Durable Bounds / Side-Effect Gate / Public Context Rework

## meta

- task_id: `20260828_2038_aiscc-p1-5-durable-bounds-side-effect-gate-and-public-context-rework-1`
- created_at: `2026-08-28 20:38 KST`
- phase: `P1-5 — Agent Provider and Tool Execution`
- work_type: `IMPLEMENTATION_AND_RUNTIME_VERIFICATION_REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `restart-durable bounds + exact pre-side-effect workflow/security gate`
- predecessor_task: `20260828_1823_aiscc-p1-5-durable-execution-public-live-continuation-and-secret-lease-rework-1`
- predecessor_result: `ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING`
- command_center_result: `HOLD_REWORK_REQUIRED`
- predecessor_HEAD: `3312e24b60e0bd10b7c859546d6fdfa3bd2cb025`
- predecessor_candidate_count: `42`
- predecessor_candidate_aggregate_sha256: `ef6dd8d9d226fdf9e2f13f51b28ba87898bff6cfbd56f1921b9f587eea602f37`
- P1_5_design_status: `HUMAN_PROVIDED / ACCEPTED / CLOSED`
- P1_5_runtime_status_before: `HOLD_REWORK_REQUIRED`
- P1_6_status: `NOT_STARTED`

---

# 0. sole execution contract

Retain the current exact 42-path candidate.

Retain as accepted candidate behavior:

- P1-5 PROVIDER/TOOL/SECRET selector integration;
- PUBLIC_BOUNDED_LIVE provider/tool local positive path;
- durable AgentExecutionService structural composition;
- PostgreSQL private protocol body;
- local-history-only Responses continuation;
- SecretResolutionLease;
- exact Tool `ResourceRequirement`;
- Replay zero execution;
- P1-4 execution-ref handoff.

Rework only:

1. durable/restart-safe bounds;
2. exact WorkRun freshness before every side effect;
3. correct Tool security/dispatch phase ordering;
4. immediate known denial terminalization;
5. workflow-left-running safety closure;
6. fixed PUBLIC_BOUNDED_LIVE repository/scenario authority.

No P1-6/P1-7/P1-8 implementation.
No real provider call/API key/billing/deployment.

---

# Stage 0 — provenance

## expected repository

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

HEAD:
3312e24b60e0bd10b7c859546d6fdfa3bd2cb025
```

If HEAD differs:

```text
STOP
→ BLOCKED_PREDECESSOR_HEAD_DRIFT
```

## exact baseline candidate

Before Git index mutation verify:

```text
candidate count:
42

aggregate SHA-256:
ef6dd8d9d226fdf9e2f13f51b28ba87898bff6cfbd56f1921b9f587eea602f37
```

Exact predecessor Task bytes:

```text
.aiassistant/tasks/done/
20260828_1823_aiscc-p1-5-durable-execution-public-live-continuation-and-secret-lease-rework-1.md

SHA-256:
d4dbc18af8dca1619688208df748062bef308f3da4cc8b6bc8c2322b3a7bc025
```

Mismatch:

```text
STOP
→ BLOCKED_P1_5_CANDIDATE_OR_TASK_DRIFT
```

## exact provenance paths

Only:

```text
.aiassistant/tasks/done/
20260828_1823_aiscc-p1-5-durable-execution-public-live-continuation-and-secret-lease-rework-1.md

.aiassistant/records/aiscc/cycles/
20260828_2038_aiscc-p1-5-durable-bounds-side-effect-gate-and-public-context-hold-1.cycle.md
```

Current 42 candidate paths MUST NOT be staged.

Exactly one local provenance commit is authorized.

Exact commit message:

```text
docs: record P1-5 durable execution bounds hold

Persist the P1-5 runtime review that retained the durable provider,
tool, continuation, and secret-lease path but found process-local bounds
and incomplete pre-side-effect workflow/security authority.

Keep P1-6 blocked until the durable execution gate is fail-closed.
```

Use LF-safe UTF-8 message file + `git commit -F`.

After commit:

```text
P1_5_FINAL_RUNTIME_REWORK_BASE_COMMIT=<full hash>
```

Verify exact two paths, exact parent/message, clean index, no remote operation.

After this commit:

```text
git add / commit / push
→ FORBIDDEN
```

---

# Stage 1 — absolute candidate universe

The original P1-5 exact maximum remains:

```text
50 paths
```

Current candidate:

```text
42 paths
```

The only still-unused authorized paths are:

```text
src/aiscc/security/models.py
src/aiscc/persistence/database.py
src/aiscc/workflow/models.py
tests/runtime/providers/test_secret_non_exposure.py
tests/unit/security/test_permission_policy.py
tests/unit/security/test_capability_lifetime.py
tests/unit/workflow/test_state_machine.py
tests/integration/security/test_broker_fail_closed.py
```

Use them only if genuinely required.

No 51st path.

```text
51st path required
→ EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

No new dependency.

---

# Stage 2 — restart-durable bound projection

The durable `AgentExecutionService.execute()` path must use PostgreSQL as the bound authority.

Implement an exact durable projection equivalent to:

```text
provider_calls
agent_rounds
tool_calls
provider_retries
output_bytes
output_tokens
budget_units
started_at / absolute execution deadline
```

The existing `ExecutionAttemptRow.counters` may be used.

Do not create a new table merely for counters.

## required authority

Every counter/deadline mutation:

```text
→ execution-attempt advisory/row lock
→ verify attempt event projection
→ verify private protocol integrity
→ verify current WorkRun binding
→ compare against server-owned ProviderProfile bounds
→ atomic reserve/increment
→ durable projection update
```

A failed bound reservation:

```text
→ no side effect
→ no counter increment
→ one exact failure event
→ attempt EXECUTION_FAILED
```

A successful side effect reservation remains consumed even if the external outcome becomes unknown.

Restart/recreated service reads counters/deadline from PostgreSQL, not `self.counters`.

Process-local counters may remain only as non-authoritative diagnostics.

## required limits on production durable path

Enforce all accepted bounds:

```text
provider_call_maximum
agent_round_trip_maximum
tool_call_maximum
provider_retry_maximum
total_timeout_seconds
input_byte_bound
output_byte_bound
output_token_bound
budget_unit_maximum
continuation_item_maximum
continuation_byte_bound
continuation_token_estimate_bound
```

Provider request `max_output_tokens` remains defense-in-depth; durable output/usage authority must
also enforce the accepted limits.

If provider usage metadata is absent:

- byte bound remains enforceable from canonical body;
- token budget must follow one exact conservative V1 rule documented in source/report;
- do not silently count missing usage as zero if that could exceed the accepted token bound.

## retry

If durable V1 implements retry, only accepted definitely-not-sent / exact known-retryable cases may
use it.

Unknown outcome:

```text
retry:
0
```

If no durable auto-retry is implemented for a given result class, report it exactly; the retry
maximum remains a ceiling, not permission to blind retry.

---

# Stage 3 — durable bound proof across restarts

Using the production `execute()` path and isolated PostgreSQL:

For every bound below, consume to `maximum - 1`, recreate repository/service objects, then prove the
next admitted unit reaches exactly the maximum and the following unit fails before side effect:

```text
provider calls
agent rounds
tool calls
budget
output bytes
output tokens
```

Wall time:

```text
persist start/deadline
→ recreate service
→ advance deterministic clock beyond deadline
→ no provider/tool/secret side effect
→ EXECUTION_FAILED(LIMIT_EXHAUSTED)
```

Retry bound if a retryable durable path exists.

Required:

```text
restart
→ counter/deadline unchanged
```

No direct mutation of `service.counters` is accepted as durable bound proof.

---

# Stage 4 — authoritative public execution context

Freeze an executable server-owned context for PUBLIC_BOUNDED_LIVE equivalent to:

```text
fixed repository identity
fixed repository version
fixed scenario identity/version
fixed ProviderProfile identity/version
fixed ToolRegistry identity/version
```

Do not create a new public request-selectable authority object.

The existing ProviderProfile/config/model may carry the fixed context if exact and server-owned.

Before any PUBLIC_BOUNDED_LIVE provider/tool/secret side effect, obtain/validate exact P1-3:

```text
ResourceDomain.REPOSITORY
ResourceDomain.SCENARIO
```

authority for the P1-5 fixed synthetic context.

Correct P1-3 policy/config narrowly so:

```text
p1-5-fixed-synthetic
→ exact P1-5 synthetic repository/version only
→ exact P1-5 scenario only
```

while preserving the P1-3 fixed synthetic scenario.

No wildcard prefix or caller-supplied repository/path.

Required:

```text
wrong repository identity
wrong repository version
wrong scenario identity/version
public-selected context
→ DENY before PROVIDER / TOOL / SECRET side effect
```

Replay remains zero execution.

The local positive proof does NOT release Public Bounded Live.

---

# Stage 5 — revalidate WorkRun immediately before every side effect

Production durable provider path:

```text
load WorkRun/attempt
→ construct operation/security authority
→ immediately before DISPATCH_STARTED:
   reload authoritative WorkRun/attempt
→ exact same RUNNING state/version/attempt execution version required
→ only then consume/dispatch according to the exact ordering below
```

Production durable tool path:

```text
provider returns tool candidate
→ BEFORE any Tool side effect:
   reload WorkRun/attempt from PostgreSQL
→ require exact current RUNNING state/version
→ use the reloaded values for all Tool selector/grant/capability authority
```

Do not reuse the snapshot loaded before the provider network/local-fake call as Tool authority.

Required concurrency proof:

1. provider round begins at RUNNING/vN;
2. before tool dispatch, mutate WorkRun through accepted P1-4 transition to a different state/version;
3. production service:
   - tool dispatcher count remains `0`;
   - secret resolver count for tool remains `0`;
   - no new provider/tool side effect;
   - attempt is durably closed with `WORKFLOW_LEFT_RUNNING`.

Also prove stale version with RUNNING-equivalent impossible/denied according to P1-4 semantics.

---

# Stage 6 — fail-closed workflow-left-running terminalization

Narrowly extend execution repository lifecycle rules so an already-RUNNING execution attempt can be
closed after the authoritative WorkRun leaves RUNNING.

Allowed outside RUNNING:

```text
ONLY:
RUNNING ExecutionAttempt
→ EXECUTION_FAILED

failure class:
WORKFLOW_LEFT_RUNNING
or exact recovery/unknown classification required to truthfully close an already-started operation
```

Forbidden outside RUNNING:

```text
EXECUTION_STARTED
EXECUTION_COMPLETED
new PREPARED operation
SECURITY_ADMITTED for new side effect
DISPATCH_STARTED for new side effect
new output/submission authority
```

For a nonterminal operation when WorkRun leaves RUNNING:

```text
PREPARED
→ known cancelled/denied terminal

SECURITY_ADMITTED
→ known cancelled terminal

DISPATCH_STARTED
→ unknown terminal unless a known result is already durably available
```

No auto repair.
No P1-4 state mutation.

This is safety closure only.

---

# Stage 7 — correct Provider pre-side-effect denial path

For production durable provider operation:

```text
PREPARED
→ selector/grant/capability construction
```

Catch every known pre-side-effect authority failure:

```text
P1-5 selector denial
SecretUse denial
P1-3 ResourceGrant denial
P1-3 SecurityDecision denial
P1-3 Capability issuance denial
durable bound denial
public context denial
fresh WorkRun denial
```

Required same invocation result:

```text
operation:
OUTCOME_KNOWN(DENIED_BEFORE_SIDE_EFFECT or exact accepted pre-dispatch cancellation)

attempt:
EXECUTION_FAILED

provider invocation:
0

secret resolution:
0
```

Do not require a later `execute()` call merely to clean normal denial provenance.

Crash/restart recovery remains separate.

---

# Stage 8 — split Tool admission from dispatch boundary

Refactor the existing Tool broker within current authorized source so the production service can
perform:

```text
validate model candidate
→ exact ToolDefinition/args/fingerprint
→ exact TOOL + underlying ResourceRequirement + optional SecretRequirement verification
→ obtain exact capabilities
→ SECURITY_ADMITTED
→ atomic validate-all-then-consume
→ optional exact secret lease created
→ final WorkRun/attempt freshness check
→ DISPATCH_STARTED
→ resolver/dispatcher side effect
→ exact output validation
→ OUTCOME_KNOWN / OUTCOME_UNKNOWN
```

No capability/resource/argument validation that may deny the operation is allowed after
`DISPATCH_STARTED`, except validation of the actual returned output/result.

Required:

```text
same-domain wrong-resource
→ OUTCOME_KNOWN(DENIED_BEFORE_SIDE_EFFECT)
→ dispatcher count 0
→ DISPATCH_STARTED event count 0

atomic consume failure
→ OUTCOME_KNOWN(CANCELLED)
→ dispatcher count 0
→ DISPATCH_STARTED event count 0
```

Secret resolution must happen only after exact consumed SECRET lease and after the final freshness
gate.

---

# Stage 9 — provider dispatch ordering

Provider path must similarly ensure:

```text
PREPARED
→ selectors/grants/capabilities built
→ SECURITY_ADMITTED
→ durable bounds reserved
→ atomic capability consume
→ exact SecretResolutionLease issued
→ final WorkRun/attempt freshness reload
→ DISPATCH_STARTED
→ secret resolve
→ adapter crossing
```

If final freshness fails after capability consumption:

```text
no provider call
no secret resolution
consumed use is not restored
operation closes known cancelled
attempt WORKFLOW_LEFT_RUNNING
```

This preserves conservative capability-use semantics without side effect.

---

# Stage 10 — integrated bounded public-live proof

Using the same production durable service with local fake Responses:

```text
RuntimeMode.PUBLIC_BOUNDED_LIVE
exact fixed synthetic repository/version
exact fixed scenario
exact server ProviderProfile
exact ToolRegistry
```

Run the two-round provider → tool → restart → provider completion path.

Assert:

```text
provider calls:
2

tool calls:
1

all durable counters:
exact

repository/scenario context:
exact

WorkRun:
RUNNING during execution

ExecutionStatus:
EXECUTOR_COMPLETED

P1-6 admitted evidence:
0
```

Then recreate service and prove no counter reset.

Negative matrix:

```text
wrong repo
wrong repo version
wrong scenario
wrong profile/model
wrong tool
wrong secret
wrong state/version
→ zero unauthorized side effects
```

---

# Stage 11 — bounded-loop production proof

The mandatory `BOUNDED_LOOP` proof MUST call the durable production entrypoint/repository authority.

Do not use:

```text
service.counters = ...
legacy execute_provider() only
component admit_* methods only
```

as substitute.

At minimum prove:

```text
PROVIDER_CALL_LIMIT
AGENT_ROUND_LIMIT
TOOL_CALL_LIMIT
BUDGET_LIMIT
OUTPUT_BYTE_LIMIT
OUTPUT_TOKEN_LIMIT
WALL_TIME_LIMIT
```

are restart-durable and fail before the next side effect.

If provider retry is implemented, prove retry bound through the durable entrypoint.
If no durable retry side effect exists, report:

```text
durable auto retry:
0
```

and prove unknown outcomes never retry.

---

# Stage 12 — regression

Re-run:

```text
uv sync --frozen --all-groups
uv build
uv run ruff check .
uv run ruff format --check .
uv run mypy --strict src tests
uv run pytest -q tests/unit tests/integration
```

No skip/xfail.

Re-run:

```text
P1-3 Docker runtime regression
all P1-5 runtime tests
```

Required proof classes:

```text
RESOURCE_AUTHORITY
PUBLIC_LIVE_POSITIVE_EXECUTION
PUBLIC_LIVE_FIXED_REPOSITORY_CONTEXT
SECRET_MEDIATION
TOOL_EXACT_UNDERLYING_RESOURCE_BINDING
OPERATION_PHASE_GRAPH
DURABLE_AGENT_LOOP
DURABLE_BOUNDED_LOOP
PER_SIDE_EFFECT_WORKFLOW_FRESHNESS
WORKFLOW_LEFT_RUNNING_SAFETY_CLOSURE
RESPONSES_STATE_MODE
DURABLE_CONTINUATION_AUTHORITY
REPLAY_ZERO_EXECUTION
PROVIDER_ADAPTER_CONTRACT
EXECUTION_STATUS_EVENTS
AMBIGUOUS_PROVIDER_FAILURE
PERSISTENCE_AND_HANDOFF
MODE_SECURITY
FINAL_RESIDUE
```

PostgreSQL empty DB → current Alembic head:

```text
PASS
```

Final Task-owned residue:

```text
Docker containers:
0

Docker networks:
0

fake provider background processes:
0

temporary workspaces:
0
```

Real provider calls:

```text
0
```

---

# evidence contract

## executor_required

- `P1_5_FINAL_RUNTIME_REWORK_PROVENANCE_GIT`
- `BASELINE_42_PATH_CANDIDATE_IDENTITY`
- `DURABLE_BOUNDED_LOOP`
- `PUBLIC_LIVE_FIXED_REPOSITORY_CONTEXT`
- `PER_SIDE_EFFECT_WORKFLOW_FRESHNESS`
- `WORKFLOW_LEFT_RUNNING_SAFETY_CLOSURE`
- `PROVIDER_PRE_SIDE_EFFECT_DENIAL_TERMINALIZATION`
- `TOOL_PRE_DISPATCH_SECURITY_ORDERING`
- `PUBLIC_LIVE_POSITIVE_EXECUTION`
- `DURABLE_AGENT_LOOP`
- `DURABLE_CONTINUATION_AUTHORITY`
- `SECRET_RESOLUTION_LEASE`
- `TOOL_EXACT_UNDERLYING_RESOURCE_BINDING`
- `P1_3_SECURITY_REGRESSION`
- `P1_4_WORKFLOW_REGRESSION`
- `POSTGRES_MIGRATION`
- `REPLAY_ZERO_EXECUTION`
- `FINAL_RESIDUE`

## human_owned

`HUMAN_VERIFICATION`

All proof passes:

```text
ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING
```

Executor MUST NOT close P1-5.

## forbidden

- P1-6/P1-7/P1-8 implementation;
- real provider/OpenAI network call;
- real API key/secret;
- billing/spend configuration;
- public deployment;
- LangGraph core;
- second Git commit after Stage 0;
- Git push/remote mutation;
- candidate path outside original exact 50-path universe.

---

# proof non-substitution

```text
ExecutionAttempt.counters exists
!= durable bound enforced

local service counter
!= restart authority

provider round starts fresh
!= tool side effect uses fresh WorkRun

capabilities exist
!= security consumed before DISPATCH_STARTED

recovery can close later
!= normal denial closed now

scenario allowlist
!= fixed repository/version authority

component BOUNDED_LOOP test
!= durable production BOUNDED_LOOP proof

local Public Live proof
!= public release
```

---

# result rules

All required proof passes:

```text
ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING
```

Accepted P1-3/P1-4 ownership must be weakened:

```text
POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

51st path required:

```text
EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

Real provider call required:

```text
EXTERNAL_EVIDENCE_SCOPE_REQUIRED
```

Executor MUST NOT claim P1-5 `ACCEPTED / CLOSED`.

---

# report required fields

- Task ID/path;
- predecessor HEAD;
- Stage-0 provenance commit/full hash;
- baseline 42-path aggregate;
- exact post-rework candidate count/set/aggregate;
- newly used paths from original 50-path universe;
- exact durable counter/deadline schema;
- exact bound reservation transaction;
- durable bound restart proof;
- exact fixed Public Live repository/scenario context;
- exact P1-3 REPOSITORY/SCENARIO authority path;
- exact pre-provider freshness gate;
- exact pre-tool freshness gate;
- workflow-left-running safety closure behavior;
- provider denial immediate terminalization proof;
- Tool security-admitted/dispatch-start ordering;
- integrated Public Live positive proof;
- two-round restart proof;
- P1-3/P1-4 regression;
- build/static/test counts;
- PostgreSQL/Alembic/Docker versions;
- final residue;
- real provider calls `0`;
- P1-6 not implemented;
- Human pending;
- forbidden-not-run;
- rollback;
- preserved paths;
- next recommendation.

---

# export bundle

Target:

```text
.aiassistant/reports/target/20260828_2038_aiscc-p1-5-durable-bounds-side-effect-gate-and-public-context-rework-1/
```

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- all actual post-rework P1-5 candidate files preserving project-relative paths
- compact non-secret runtime/PostgreSQL/static evidence

No raw secret, DB volume, `.venv`, Docker layer, cache or unrelated file.

---

# Task lifecycle

```text
.aiassistant/tasks/active/20260828_2038_aiscc-p1-5-durable-bounds-side-effect-gate-and-public-context-rework-1.md
→
.aiassistant/tasks/done/20260828_2038_aiscc-p1-5-durable-bounds-side-effect-gate-and-public-context-rework-1.md
```

`done` means submitted, not Human accepted.

---

# preserved artifacts

Preserve:

- commit `3312e24b60e0bd10b7c859546d6fdfa3bd2cb025`
- `.aiassistant/tasks/done/20260828_1823_aiscc-p1-5-durable-execution-public-live-continuation-and-secret-lease-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260828_2038_aiscc-p1-5-durable-bounds-side-effect-gate-and-public-context-hold-1.cycle.md`
- all exact current 42 P1-5 candidate paths

Historical candidate identity:

```text
42 paths
ef6dd8d9d226fdf9e2f13f51b28ba87898bff6cfbd56f1921b9f587eea602f37
```

---

# next action after P1-5 runtime Human acceptance

```text
P1-6 Evidence Admission
```

Do not implement P1-6 in this Task.
