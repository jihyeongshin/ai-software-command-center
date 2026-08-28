# AISCC Cycle Record

## meta

- cycle_id: `20260828_1529_aiscc-p1-5-provider-tool-execution-design-final-acceptance-1`
- date: `2026-08-28 15:29 KST`
- primary_semantic_owner: `P1-5 provider/tool execution design final judgment`
- work_type: `COMMAND_CENTER_RECORD_UPDATE`
- result_status: `ACCEPTED / CLOSED`
- human_result: `ACCEPTED`
- design_status: `CANONICAL_BASELINE_ACCEPTED`
- implementation_status: `NOT_STARTED`
- cycle_record_action: `create`
- source_mirror_sync: `not-required`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260828_1529_aiscc-p1-5-provider-tool-execution-design-final-acceptance-1.cycle.md`

## Human final review

Human explicitly provided:

```text
Human P1-5 design final review
판정: ACCEPTED
```

Admit as:

```text
classification:
HUMAN_PROVIDED

channel:
HUMAN_VERIFICATION

scope:
P1-5 Provider / Tool Execution Contract Design Freeze

result:
ACCEPTED
```

## accepted design provenance

Final design Executor Task:

```text
20260828_1417_aiscc-p1-5-secret-operation-protocol-and-openai-state-mode-design-rework-1
```

Design rework base commit:

```text
d96949f3643e6a0610942e33d70e9da259e1e432
```

Accepted canonical design path:

```text
.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md
```

Accepted design SHA-256:

```text
12070677aa1cfa74b7eea9a52db24f78aacd2bf23d655f125a7689797d172443
```

P1-5 runtime/product source remains unimplemented at Human design acceptance.

## accepted execution-status contract

Exact `ExecutionStatus` set:

```text
NOT_STARTED
RUNNING
EXECUTOR_COMPLETED
EXECUTION_FAILED
```

Accepted non-substitution:

```text
ExecutionStatus != WorkflowState

execution status/event mutation
!= WorkflowState transition

execution status/event mutation
→ MUST NOT increment WorkRun.state_version

EXECUTOR_COMPLETED != ACCEPTED

EXECUTION_FAILED != FAILED
```

`ExecutionAttempt.execution_version` is separate from P1-4 `WorkRun.state_version`.

## accepted execution attempt lifecycle

Accepted lifecycle:

```text
no attempt
→ EXECUTION_ATTEMPT_CREATED
→ NOT_STARTED

NOT_STARTED
+ admitted READY → RUNNING workflow lineage
→ EXECUTION_STARTED
→ RUNNING

RUNNING
+ final output/submission + known terminal operations + cleanup
→ EXECUTION_COMPLETED
→ EXECUTOR_COMPLETED

RUNNING
+ fatal/cancel/retry-exhausted/unknown-outcome/workflow-left-running/recovery conflict
→ EXECUTION_FAILED
→ EXECUTION_FAILED
```

A terminal attempt never returns to `RUNNING`.
A same-WorkRun retry is a new `ExecutionAttempt` under a fresh admitted workflow lineage.

## accepted provider/tool resource authority

P1-5 supplies exact server-owned selector authority for:

```text
ResourceDomain.PROVIDER
ResourceDomain.TOOL
```

P1-3 remains sole owner of:

```text
SecurityAdmissionDecision
ResourceGrant
Capability
capability consume/revoke/use count
```

Accepted invariant:

```text
P1-5 selector attestation
!= P1-3 ALLOW
!= ResourceGrant
!= Capability
```

Missing/unknown/revoked selector authority fails closed.

Provider/model/tool/endpoint selection is server-owned and cannot come from public/Agent input.

Provider operation identity binds the accepted operation fingerprint.
Tool authorization binds exact registry/schema/argument fingerprint.

## accepted scoped secret mediation

P1-5 owns a typed secret-use selector/attestation boundary equivalent to:

```text
SecretUseAuthorityPort
SecretUseSelectorAttestation
```

P1-3 remains sole SECRET admission and capability owner.

Accepted flow:

```text
server-owned ProviderProfile / ToolDefinition secret_ref
→ P1-5 SecretUse selector attestation
→ separate P1-3 SECRET ResourceGrant
→ SecurityAdmissionDecision
→ SECRET Capability
→ broker validates/atomically consumes exact required capabilities
→ private adapter/dispatcher resolver supplies material only inside adapter boundary
```

Accepted non-substitution:

```text
secret_ref != secret authority
SecretUseSelectorAttestation != SecurityAdmissionDecision
PROVIDER Capability != SECRET Capability
TOOL Capability != SECRET Capability
```

Raw secret material may not enter Agent input/output, public/session data, workspace, environment dump,
command/tool arguments, provider durable protocol history, event/provenance bodies, Replay or review
export.

No concrete secret-manager product is selected by this design.

## accepted ToolRegistry / broker

ToolRegistry is versioned and server-owned.

Every tool has exact schema/version, side-effect class, mode/profile/scenario allowlist, underlying
resource requirements, timeout/retry/idempotency and output bounds.

Accepted path:

```text
model-proposed tool/call arguments
→ untrusted candidate
→ exact registry lookup
→ strict schema validation
→ canonical argument fingerprint
→ P1-5 TOOL selector authority
→ P1-3 TOOL SecurityAdmissionDecision/Capability
→ independent PROCESS/FILESYSTEM/NETWORK/SECRET admission as required
→ registered dispatcher only
```

A TOOL capability never implies an underlying resource capability.
Arbitrary shell, executable, path, URL and destination from model output remain denied.

## accepted bounded agent loop

Normal provider/tool execution requires authoritative:

```text
WorkflowState=RUNNING
```

Each provider/tool side effect revalidates exact current `WorkflowState/state_version` through P1-3
capability semantics.

The loop is bounded by server-owned profile values for:

- provider calls;
- agent rounds;
- tool calls;
- provider retry count;
- timeout;
- output/token size;
- budget.

A state/version change invalidates existing capability.
No hidden continuation is allowed.

## accepted durable operation protocol

Exact phase model is acyclic and supports pre-side-effect terminal outcomes.

Semantically:

```text
PREPARED
→ OUTCOME_KNOWN(DENIED_BEFORE_SIDE_EFFECT)
or
→ SECURITY_ADMITTED

SECURITY_ADMITTED
→ OUTCOME_KNOWN(CANCELLED)
or
→ DISPATCH_STARTED

DISPATCH_STARTED
→ OUTCOME_KNOWN(...)
or
→ OUTCOME_UNKNOWN(...)
```

Every legal phase edge is append-only and durable.

`RETRY_EXHAUSTED` is an execution-attempt-level failure classification over truthful operation
outcomes, not a dual-purpose single-operation result.

Unknown provider/tool outcome must not be blindly retried.

## accepted OpenAI Responses V1 protocol

Concrete adapter direction:

```text
OpenAI Responses API
custom function tools only
parallel_tool_calls=false
background=false
stream=false
store=false
truncation=disabled
```

Provider-hosted execution tools remain disabled.

Accepted continuation authority:

```text
AISCC local durable private protocol history
→ authoritative continuation source

provider Conversation resource
→ NOT execution authority

previous_response_id
→ NOT sole continuation authority
→ omitted by V1 adapter
```

Continuation explicitly replays the required prior provider output items, exact
`function_call_output/call_id`, and opaque encrypted reasoning protocol material when required.

Provider response/request IDs are diagnostic/reconciliation refs only.

Accepted Response status mapping covers exactly:

```text
queued
in_progress
completed
failed
cancelled
incomplete
```

`queued/in_progress` are not silently treated as completion.
`incomplete` is a distinct known incomplete result.
A local timeout after dispatch remains an unknown outcome unless reconciliation proves a known
terminal result.

No real OpenAI provider/model/account/API key/billing configuration is accepted by this design.

## accepted persistence boundary

P1-5 runtime must persist/reconstruct:

- `ExecutionAttempt` identity and current status projection;
- monotonic `execution_version`;
- append-only lifecycle events;
- every execution operation and legal phase edge;
- known/unknown terminal outcome;
- operation and argument fingerprints;
- selector/admission/capability refs;
- private provider protocol-state refs/hashes/order/call IDs;
- output/artifact/submission refs;
- usage/duration/retry/cancel/failure classifications.

Lifecycle event append + status projection CAS is atomic.
Operation phase append + operation projection CAS is atomic.

Fresh execution mutation verifies event/projection consistency and required private protocol-state
integrity before side effects.
Mismatch fails closed without auto repair.

Pure execution event admission never increments P1-4 `state_version`.

## accepted P1-6 handoff

P1-5 may produce immutable refs equivalent to:

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

P1-6 remains sole evidence requirement/admission owner.

P1-4 may validate exact issuer-backed P1-5 execution-start/submission refs before minting its own
`G_EXECUTION_STARTED` or `G_EXECUTOR_SUBMISSION`; P1-5 cannot mint P1-4 guard authority.

## exact RuntimeMode acceptance

```text
OWNER_SELF_DOGFOOD
→ explicit server-owned bounded provider/tool profile
→ isolated worktree/runtime
→ no Agent Git commit/push/deploy authority

PUBLIC_RECORDED_REPLAY
→ provider calls 0
→ tool calls 0
→ process/network execution 0
→ missing/corrupt Replay never falls through to Live

PUBLIC_BOUNDED_LIVE
→ fixed synthetic repository/version
→ fixed scenario
→ server-fixed provider/model/profile/tool registry
→ bounded time/calls/retries/output/budget
→ no public free-form task/provider/model/endpoint/secret selection
```

Public Bounded Live remains `NOT_RELEASED`.

## implementation gate

Human design acceptance opens:

```text
P1-5 Provider / Tool Execution Implementation + Runtime Verification
→ READY
```

The implementation acceptance contract requires fake/local provider transport plus executable
PostgreSQL/P1-3 security proof.

No real provider call is required for P1-5 implementation acceptance.

Real provider account, model, API key, billing/spend guard and public release configuration remain a
later Human-authorized release/configuration concern.

## terminal judgment

```text
P1-5 Provider / Tool Execution Design
→ HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-5 runtime implementation
→ READY / NOT_STARTED

P1-6
→ NOT_STARTED
```

## preservation

Preserve exact commits:

- `d99ccc4ecde585685e93960a7fa39ecbfde89f9f`
- `d96949f3643e6a0610942e33d70e9da259e1e432`

Preserve exact paths:

- `.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md`
- `.aiassistant/tasks/done/20260828_1417_aiscc-p1-5-secret-operation-protocol-and-openai-state-mode-design-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260828_1529_aiscc-p1-5-provider-tool-execution-design-final-acceptance-1.cycle.md`
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`

Preserve accepted design identity:

```text
12070677aa1cfa74b7eea9a52db24f78aacd2bf23d655f125a7689797d172443
```

## next action

```text
P1-5 Provider / Tool Execution Implementation + Runtime Verification
```
