# AISCC Cycle Record

## meta

- cycle_id: `20260828_1110_aiscc-p1-4-explicit-state-machine-kernel-final-acceptance-1`
- date: `2026-08-28 11:10 KST`
- primary_semantic_owner: `P1-4 explicit authoritative state-machine kernel final judgment`
- work_type: `COMMAND_CENTER_RECORD_UPDATE`
- result_status: `ACCEPTED / CLOSED`
- human_result: `ACCEPTED`
- implementation_status: `IMPLEMENTED`
- database_runtime_proof: `EXECUTED_PASS`
- cycle_record_action: `create`
- source_mirror_sync: `not-required`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260828_1110_aiscc-p1-4-explicit-state-machine-kernel-final-acceptance-1.cycle.md`

## Human final review

Human explicitly provided:

```text
Human P1-4 final review
판정: ACCEPTED
```

Admit as:

```text
classification:
HUMAN_PROVIDED

channel:
HUMAN_VERIFICATION

scope:
P1-4 Explicit State Machine Kernel Implementation

result:
ACCEPTED
```

## final candidate provenance

Final Executor Task:

```text
20260828_1110_aiscc-p1-4-denied-precreation-retry-consistency-semantics-rework-1
```

Final pre-terminal-closure HEAD:

```text
aec4d24ba3ae23d8252c9582130aea99aac333a1
```

Relevant additive provenance lineage:

```text
1b04e8a0d36fc0400cbeacaf65c56f643f423923
→ P1-3 terminal persistence + P1-4 implementation base

325f876234c580d6f61d650501ed3250d152970a
→ P1-4 authority/consistency HOLD provenance

aec4d24ba3ae23d8252c9582130aea99aac333a1
→ P1-4 denied-precreation retry HOLD provenance
```

Final accepted P1-4 candidate:

```text
path count:
19

aggregate SHA-256:
1316fd14faf6a2ad85f43ae9e9a2bab45c1736e4f28bea40d35865f53dee4cb5
```

No additional P1-4 source mutation is admitted after this digest and before Human acceptance.

## accepted state-machine kernel

The accepted kernel implements:

```text
exact WorkflowState set:
9 states

exact allowed transition matrix:
22 source/target pairs

authoritative WorkRun
authoritative current WorkflowState
monotonic state_version

TransitionRequest
TransitionEvaluation
TransitionDecision

ADMITTED / DENIED append-only transition provenance
atomic admitted state/version mutation
stale-request denial
duplicate-request idempotency
restart-durable projection
projection/event consistency fail-closed behavior
```

The orchestration core remains directly implemented explicit state-machine logic.

```text
LangGraph orchestration core:
NOT_USED
```

## accepted authority separation

Retain:

```text
AgentOutput != SystemState

Judgment != TransitionDecision
TransitionDecision != WorkflowState

SecurityAdmissionDecision != TransitionDecision

RuntimeMode != WorkflowState
```

P1-4 semantic guard ownership is explicit.

```text
P1_4_SYSTEM
→ P1-4-owned guard facts only

P1_6_EVIDENCE
→ future external Evidence authority

P1_7_HUMAN
→ future external Human authority

P1_7_JUDGMENT
→ future external Judgment authority
```

Production `WorkflowKernel` exposes no universal guard mint authority.

Raw:

```text
evidence_refs
human_result_refs
judgment_refs
```

remain non-authoritative without exact owner-bound trusted facts.

## accepted PostgreSQL authority semantics

Accepted implementation uses PostgreSQL-backed durable authority with:

- SQLAlchemy 2 async;
- asyncpg;
- Alembic;
- WorkRun current projection;
- append-only transition request/evaluation/decision history;
- database constraints/triggers preventing historical mutation;
- per-run and per-request advisory serialization;
- row lock + compare-and-swap state mutation.

For an admitted transition:

```text
ADMITTED TransitionDecision
+ resulting state
+ state_version + 1
+ durable provenance
→ one transaction
```

For a denied transition:

```text
DENIED provenance
→ durable

WorkflowState/state_version
→ unchanged
```

## accepted concurrency / idempotency semantics

Same observed state/version concurrent requests:

```text
at most one admitted mutation
other request
→ stale/denied
```

Same exact `transition_request_id` retry:

```text
same immutable request fingerprint
→ same existing immutable decision
→ no duplicate mutation/event
```

Same request ID with different immutable request/fact content:

```text
→ RequestIdentityConflictError
```

## accepted consistency semantics

Every NEW mutation-capable transition request is consistency-gated inside the run serialization /
database transaction boundary.

```text
projection/history mismatch
→ AuthorityConflictError
→ no new request/evaluation/decision
→ no state mutation
→ no automatic repair
```

`verify_consistency()` is not merely an optional pre-call requirement; fresh mutation itself is
fail-closed.

### absent projection + history

Accepted distinction:

```text
no WorkRun projection
+ complete DENIED-only pre-creation history
+ same immutable run identity
→ authoritative NONE/v0 remains valid
→ corrected fresh NONE/v0 request may proceed
```

versus:

```text
no projection
+ ADMITTED history
→ AuthorityConflictError

no projection
+ partial/orphaned/inconsistent history
→ AuthorityConflictError

no projection
+ denied history under conflicting project/task/version/runtime identity
→ AuthorityConflictError
```

Therefore DENIED audit provenance does not behave like a hidden terminal WorkflowState.

## final verification admitted

### build/static

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

### test/runtime

```text
targeted P1-4 PostgreSQL integration:
17 PASS

full unit + integration:
74 PASS

skip / xfail:
0
```

Retained proof classes:

```text
AUTHORITATIVE_STATE_MUTATION
→ PASS

STALE_REQUEST_CONCURRENCY
→ PASS

DUPLICATE_REQUEST_IDEMPOTENCY
→ PASS

ATOMICITY
→ PASS

RESTART_DURABILITY
→ PASS

PROJECTION_EVENT_CONSISTENCY
→ PASS

DENIED_PROVENANCE
→ PASS

OWNER_BOUND_GUARD_AUTHORITY
→ PASS

DENIED_PRECREATION_RETRY
→ PASS

PRECREATION_IDENTITY_ISOLATION
→ PASS

PARTIAL_PRECREATION_HISTORY_FAIL_CLOSED
→ PASS
```

### environment

```text
Python:
CPython 3.12.14

uv:
0.12.6

Docker client/server:
28.3.3 / 28.3.3

PostgreSQL:
17.6

PostgreSQL image:
postgres:17.6-bookworm

Alembic head:
20260828_0001
```

Final Task-owned residue:

```text
containers:
0

networks:
0
```

## execution-status handoff

P1-1 already defines a separate canonical `ExecutionStatus` dimension:

```text
NOT_STARTED
RUNNING
EXECUTOR_COMPLETED
EXECUTION_FAILED
```

P1-4 intentionally did not steal P1-5 execution-adapter ownership.

Therefore P1-5 must implement execution events/projection without treating them as WorkflowState or
changing `state_version` merely because execution status changes.

```text
ExecutionStatus
!= WorkflowState

EXECUTOR_COMPLETED
!= ACCEPTED
```

## P1-5 design-baseline requirement

P1-1/P1-2 define the owner/boundary but do not yet freeze the exact P1-5 implementation contract for:

- provider/tool resource authority;
- provider/model/tool server-owned profile identity;
- provider/tool capability integration with P1-3;
- execution event/projection durability;
- provider-call/tool-call idempotency;
- ambiguous provider failure/retry semantics;
- provider output / tool output candidate boundary;
- exact provider adapter transport;
- tool registry and argument binding.

These are load-bearing governance decisions.

Therefore:

```text
P1-5:
READY

first subtask:
PROVIDER_TOOL_EXECUTION_CONTRACT_DESIGN_FREEZE
```

No P1-5 runtime implementation is accepted or implied by P1-4 closure.

## release consequence

P1-4 acceptance closes the authoritative workflow-state kernel prerequisite.

It does NOT mean:

```text
provider execution implemented
tool execution implemented
evidence admission implemented
Human gate implemented
Cycle/memory implemented
public bounded Live released
```

Public Bounded Live remains:

```text
NOT_RELEASED
```

## terminal judgment

```text
P1-4 Explicit State Machine Kernel Implementation
→ HUMAN_PROVIDED / ACCEPTED / CLOSED

implementation:
IMPLEMENTED

PostgreSQL runtime proof:
EXECUTED_PASS

P1-5:
READY / DESIGN_FREEZE_REQUIRED
```

## preservation

Preserve exact commits:

- `1b04e8a0d36fc0400cbeacaf65c56f643f423923`
- `325f876234c580d6f61d650501ed3250d152970a`
- `aec4d24ba3ae23d8252c9582130aea99aac333a1`

Preserve exact paths:

- `.aiassistant/tasks/done/20260828_1110_aiscc-p1-4-denied-precreation-retry-consistency-semantics-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260828_1110_aiscc-p1-4-explicit-state-machine-kernel-final-acceptance-1.cycle.md`
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
- all exact 19 accepted P1-4 implementation candidate paths

Preserve final candidate identity:

```text
19 paths
1316fd14faf6a2ad85f43ae9e9a2bab45c1736e4f28bea40d35865f53dee4cb5
```

## next action

```text
P1-5 Agent Provider and Tool Execution
→ first subtask:
Provider / Tool Execution Contract Design Freeze
```
