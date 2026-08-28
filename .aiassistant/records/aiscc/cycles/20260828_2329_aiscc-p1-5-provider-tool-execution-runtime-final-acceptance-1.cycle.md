# AISCC Cycle Record

## meta

- cycle_id: `20260828_2329_aiscc-p1-5-provider-tool-execution-runtime-final-acceptance-1`
- date: `2026-08-28 23:29 KST`
- primary_semantic_owner: `P1-5 provider/tool execution runtime final judgment`
- work_type: `COMMAND_CENTER_RECORD_UPDATE`
- result_status: `ACCEPTED / CLOSED`
- human_result: `ACCEPTED`
- design_status: `ACCEPTED / CLOSED`
- implementation_status: `IMPLEMENTED / ACCEPTED`
- runtime_verification: `EXECUTED_PASS`
- cycle_record_action: `create`
- source_mirror_sync: `not-required`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260828_2329_aiscc-p1-5-provider-tool-execution-runtime-final-acceptance-1.cycle.md`

## Human final review

Human explicitly provided:

```text
Human P1-5 runtime final review
판정: ACCEPTED
```

Admit as:

```text
classification:
HUMAN_PROVIDED

channel:
HUMAN_VERIFICATION

scope:
P1-5 Provider / Tool Execution Runtime Implementation

result:
ACCEPTED
```

## final implementation provenance

Final Executor Task:

```text
20260828_2215_aiscc-p1-5-missing-provider-usage-token-accounting-rework-1
```

Final pre-terminal-closure HEAD:

```text
15036a5ff316fccbd6d891b9ce43563de056e342
```

Relevant additive provenance lineage:

```text
3b150181f1c008d0b95fd53a32cb6e62d174ab4f
→ P1-5 accepted design terminal persistence + initial runtime implementation base

3312e24b60e0bd10b7c859546d6fdfa3bd2cb025
→ durable execution / Public Live / continuation / secret-lease HOLD provenance

d652f01c1c76a9c2ed3c550a7fab6b8414b59c07
→ durable bounds / side-effect gate / public context HOLD provenance

15036a5ff316fccbd6d891b9ce43563de056e342
→ missing-provider-usage token-bound HOLD provenance
```

Final accepted P1-5 runtime candidate:

```text
path count:
42

aggregate SHA-256:
ffeb5ba70649c564c482c2cff79ce8e2b0a462f811d8e03f2c1096f170bd39d6
```

No additional P1-5 source mutation is admitted after this digest and before Human acceptance.

## accepted execution authority

P1-5 now owns executable provider/tool execution while preserving:

```text
AgentOutput != SystemState
ExecutionStatus != WorkflowState
EXECUTOR_COMPLETED != ACCEPTED
EXECUTION_FAILED != FAILED
SecurityAdmissionDecision != provider/tool result
provider/tool output != AdmittedEvidence
```

Exact `ExecutionStatus`:

```text
NOT_STARTED
RUNNING
EXECUTOR_COMPLETED
EXECUTION_FAILED
```

Pure P1-5 execution event/status mutation does not mutate P1-4 `WorkflowState` or increment
`WorkRun.state_version`.

## accepted provider/tool/security composition

Production runtime composes:

```text
P1-5 server-owned ProviderProfile / ToolRegistry
→ exact selector/SecretUse authority
→ P1-3 ResourceGrant / SecurityAdmissionDecision / Capability
→ exact capability consumption
→ private provider/tool side-effect boundary
```

Accepted non-substitution:

```text
P1-5 selector attestation != P1-3 ALLOW
PROVIDER Capability != SECRET Capability
TOOL Capability != underlying PROCESS/FILESYSTEM/NETWORK/SECRET Capability
```

Tool underlying resources are exact server-owned requirements, not domain-only presence checks.

## accepted secret mediation

Runtime uses a consumed-authority secret-resolution lease/receipt.

```text
atomic capability consume
→ exact SecretResolutionLease
→ private resolver verifies lease
→ secret material resolution
```

A raw `secret_ref`, PROVIDER capability, TOOL capability or forged/wrong/expired/closed lease cannot
resolve material.

Synthetic secret non-exposure proof passed.

## accepted durable execution protocol

PostgreSQL persists/reconstructs:

- ExecutionAttempt projection;
- execution lifecycle events;
- ExecutionOperation projection;
- operation phase/outcome history;
- provider/tool authority/admission/capability refs;
- durable private Responses protocol payload/order/hash/call-id state;
- output/tool/submission refs;
- durable counters/deadline/budget/output accounting.

Attempt/event and operation/event projection changes are atomic/CAS-protected and restart-durable.

Known pre-side-effect denials terminalize in the same invocation.
`DISPATCH_STARTED` occurs only after exact required authority has been validated/consumed and the
final WorkRun freshness gate passes.

Already-started attempts may be fail-closed terminalized as `WORKFLOW_LEFT_RUNNING` after the
authoritative WorkRun leaves RUNNING, without admitting new side effects or mutating P1-4 state.

## accepted per-side-effect freshness

Before every provider/tool side effect:

```text
reload authoritative WorkRun / ExecutionAttempt
→ require exact current RUNNING state/version/attempt execution version
→ obtain/use fresh exact authority
→ side effect
```

A provider result does not authorize a later tool side effect using the pre-provider snapshot.

Workflow/state-version drift:

```text
→ zero new provider/tool/secret side effect
→ attempt closes truthfully
```

## accepted durable bounds

Server-owned P1-5 bounds are PostgreSQL authority, not process-local counters.

Accepted durable limits include:

```text
provider calls
agent rounds
tool calls
provider retries
wall-clock deadline
input/output bytes
output tokens
budget units
continuation item/byte/token-estimate bounds
```

Service/repository restart does not reset limits.

For provider output-token accounting:

```text
request max_output_tokens = M

usage.output_tokens = exact integer N
and 0 <= N <= M
→ durable charge N

usage.output_tokens absent
→ durable charge M

malformed / negative / bool / float / string / N > M
→ fail closed
```

No byte/token estimate or tokenizer dependency is authoritative for missing provider usage.

## accepted OpenAI Responses V1 adapter

Concrete adapter:

```text
official openai Python SDK
local deterministic fake Responses endpoint for acceptance proof

background=false
stream=false
store=false
parallel_tool_calls=false
truncation=disabled

conversation:
omitted

previous_response_id:
omitted
```

Provider-hosted execution tools are not exposed.

AISCC durable local private protocol history is the continuation authority.

Missing/corrupt body/hash/order/call-id/private protocol state fails closed before provider
invocation; no provider-held continuation fallback is used.

Exact status mapping covers:

```text
queued
in_progress
completed
failed
cancelled
incomplete
```

Unknown outcome is never blindly retried.

## accepted durable bounded agent loop

Production `AgentExecutionService` owns the causal sequence equivalent to:

```text
reload WorkRun/attempt
→ durable PREPARED operation
→ selector/resource/security authority
→ SECURITY_ADMITTED
→ durable bound reservation
→ atomic capability consume / secret lease
→ final freshness recheck
→ DISPATCH_STARTED
→ provider/tool side effect
→ durable known/unknown outcome
→ durable protocol/output refs
→ bounded continuation/tool round
→ AgentOutputRef
→ ExecutionSubmissionRef
→ EXECUTOR_COMPLETED
```

Test-side manual orchestration is not the authority for the accepted runtime path.

## accepted Public modes

### OWNER_SELF_DOGFOOD

```text
server-owned bounded provider/tool profile
isolated runtime/worktree
no Agent Git commit/push/deploy authority
```

### PUBLIC_RECORDED_REPLAY

Instrumentation proves exactly:

```text
provider calls: 0
tool dispatches: 0
process broker calls: 0
network broker calls: 0
secret resolver calls: 0
```

Replay failure does not fall through to Live.

### PUBLIC_BOUNDED_LIVE

Acceptance proof uses:

```text
fixed synthetic repository identity/version
fixed scenario identity/version
server-owned provider/model/profile
server-owned ToolRegistry
exact P1-3 REPOSITORY/SCENARIO/PROVIDER/TOOL/SECRET authority
local fake Responses endpoint
```

Wrong repository/version/scenario/profile/model/tool/secret/state/version fails before unauthorized
side effect.

This executable local proof does NOT release Public Bounded Live.

```text
PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

## accepted P1-4 handoff

P1-5 produces issuer-backed execution-start/submission refs.

Raw strings are non-authoritative.

P1-4 alone may validate exact issuer-backed P1-5 refs and mint its own:

```text
G_EXECUTION_STARTED
G_EXECUTOR_SUBMISSION
```

P1-5 cannot mint P1-4 `TrustedGuardFact`.

The exact P1-4 nine-state set and 22 transition pairs remain unchanged.

## accepted P1-6 boundary

P1-5 may produce immutable:

```text
AgentOutputRef
ToolOutputRef
ExecutionArtifactRef
ExecutionSubmissionRef
```

But:

```text
producer ref
!= EvidenceCandidate admission
!= AdmittedEvidence
```

P1-6 remains sole Evidence Admission owner.

No P1-6 implementation exists in this accepted P1-5 candidate.

## final verification admitted

### static / build

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
```

### tests

```text
unit + integration:
145 PASS

P1-5 persistence/accounting integration:
23 PASS

P1-5 runtime:
10 PASS

P1-3 Docker runtime regression:
10 PASS

skip / xfail:
0
```

### versions

```text
Python:
3.12.14

uv:
0.12.7

OpenAI Python SDK:
3.5.0

PostgreSQL:
17.6

Alembic head:
20260828_0002

Docker client/server:
28.3.3 / 28.3.3
```

### external effects / residue

```text
real provider calls:
0

Task Docker containers:
0

Task/P1-5 Docker networks:
0

fake provider listeners:
0

temporary uv/workspace residue:
0
```

## terminal judgment

```text
P1-5 Provider / Tool Execution Design
→ HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-5 Provider / Tool Execution Runtime
→ HUMAN_PROVIDED / ACCEPTED / CLOSED

final implementation:
42 paths
ffeb5ba70649c564c482c2cff79ce8e2b0a462f811d8e03f2c1096f170bd39d6

P1-6 Evidence Admission
→ READY / DESIGN_FREEZE_REQUIRED
```

## preservation

Preserve exact commits:

- `3b150181f1c008d0b95fd53a32cb6e62d174ab4f`
- `3312e24b60e0bd10b7c859546d6fdfa3bd2cb025`
- `d652f01c1c76a9c2ed3c550a7fab6b8414b59c07`
- `15036a5ff316fccbd6d891b9ce43563de056e342`

Preserve exact paths:

- `.aiassistant/tasks/done/20260828_2215_aiscc-p1-5-missing-provider-usage-token-accounting-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260828_2329_aiscc-p1-5-provider-tool-execution-runtime-final-acceptance-1.cycle.md`
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
- all exact 42 accepted P1-5 implementation candidate paths.

Preserve final candidate identity:

```text
42 paths
ffeb5ba70649c564c482c2cff79ce8e2b0a462f811d8e03f2c1096f170bd39d6
```

## next action

```text
P1-6 Evidence Admission
→ first subtask:
Evidence Admission Contract Design Freeze
```
