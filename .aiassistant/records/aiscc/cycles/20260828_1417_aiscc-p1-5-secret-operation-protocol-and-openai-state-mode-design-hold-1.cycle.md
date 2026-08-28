# AISCC Cycle Record

## meta

- cycle_id: `20260828_1417_aiscc-p1-5-secret-operation-protocol-and-openai-state-mode-design-hold-1`
- date: `2026-08-28 14:17 KST`
- primary_semantic_owner: `P1-5 provider/tool execution design authority`
- work_type: `DESIGN_BASELINE / REWORK_JUDGMENT`
- execution_mode: `MANUAL_COMMAND_CENTER`
- predecessor_task: `20260828_1110_aiscc-p1-5-provider-tool-execution-contract-design-freeze-with-p1-4-terminal-commit-1`
- predecessor_executor_result: `ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING`
- predecessor_base_commit: `d99ccc4ecde585685e93960a7fa39ecbfde89f9f`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause:
  - `SCOPED_SECRET_CAPABILITY_EXTENSION_BOUNDARY_NOT_FROZEN`
  - `EXECUTION_OPERATION_PHASE_GRAPH_PRE_SIDE_EFFECT_TERMINAL_CONFLICT`
  - `OPENAI_RESPONSES_CONTINUATION_AND_STATE_MODE_UNFROZEN`
- P1_5_design_status: `NOT_ACCEPTED`
- P1_5_runtime_status: `NOT_STARTED`
- P1_6_status: `NOT_STARTED`
- cycle_record_action: `create`
- source_mirror_sync: `not-required`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260828_1417_aiscc-p1-5-secret-operation-protocol-and-openai-state-mode-design-hold-1.cycle.md`

## admitted predecessor evidence

### P1-4 terminal persistence

Admit:

```text
P1_5_DESIGN_BASE_COMMIT:
d99ccc4ecde585685e93960a7fa39ecbfde89f9f

parent:
aec4d24ba3ae23d8252c9582130aea99aac333a1

P1-4 accepted candidate:
19 paths

P1-4 aggregate:
1316fd14faf6a2ad85f43ae9e9a2bab45c1736e4f28bea40d35865f53dee4cb5

terminal commit path count:
24

exact commit message:
PASS

post-commit tracked tree/index:
clean

remote mutation:
none
```

P1-4 remains `ACCEPTED / CLOSED`.

### P1-5 design candidate identity

Exact candidate:

```text
.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md

SHA-256:
d2d5ce009dab6b7c369e35c917bfdb9b6d6a301216e4d35fac80a186ab465a32
```

No P1-5 runtime/product source was implemented.

### design strengths retained

Retain:

```text
ExecutionStatus exact set:
NOT_STARTED
RUNNING
EXECUTOR_COMPLETED
EXECUTION_FAILED

ExecutionStatus != WorkflowState
EXECUTOR_COMPLETED != ACCEPTED
EXECUTION_FAILED != FAILED

P1-5 selector authority != SecurityAdmissionDecision

P1-3 remains ALLOW/DENY / ResourceGrant / Capability owner

PROVIDER/TOOL no P1-5 authority
→ DENY

ProviderProfile:
server-owned / versioned / bounded

ToolRegistry:
server-owned / versioned / strict schema

TOOL capability
!= underlying PROCESS / FILESYSTEM / NETWORK authority

bounded agent loop:
finite

unknown provider outcome:
no blind retry

P1-5 producer refs
!= EvidenceCandidate admission
!= AdmittedEvidence

PUBLIC_RECORDED_REPLAY:
provider/tool/process/network execution 0

P1-6/P1-7/P1-8:
not implemented
```

The OpenAI Responses custom-function direction itself is not rejected.

## HOLD A — scoped secret capability extension is missing

Accepted P1-2 secret semantics require:

```text
credential/secret allow condition
→ authorized adapter
→ purpose-bound opaque handle
→ expiry/use-count valid

public sandbox
→ no direct secret-store access

server-side mediated adapter
→ scoped secret capability only
```

P1-3 executable `SecurityPolicy` currently hard-denies `ResourceDomain.SECRET` in its policy-owned
scope check. P1-3 did not implement a production secret-authority extension; its secret runtime proof
was non-exposure proof.

The P1-5 design freezes:

```text
ProviderToolResourcePolicyPort
```

for:

```text
ResourceDomain.PROVIDER
ResourceDomain.TOOL
```

but no exact production authority exists for provider credential use.

`ProviderProfile.secret_ref` alone is only an opaque configuration reference.

It is not:

```text
a scoped secret grant
a secret capability
permission to resolve secret material
```

The design also requires tools to obtain underlying `SECRET` authority, but gives no path by which
P1-3 can admit such a scope.

Therefore an implementation would have to invent one of these incompatible behaviors:

```text
A. bypass P1-3 SECRET and resolve secret directly
B. silently weaken P1-3 hard deny
C. invent a new secret authority during implementation
```

All are forbidden.

### required correction

Freeze an exact mediated-secret extension boundary without weakening P1-2/P1-3 ownership.

At minimum define a typed owner port equivalent to:

```text
SecretUseAuthorityPort
```

with P1-5 owning only provider/tool execution secret-use selector semantics and P1-3 remaining sole
security admission/capability owner.

Required secret-use attestation binds:

```text
opaque secret_ref or stable non-secret secret identity/hash
secret class
purpose
provider/tool canonical resource identity
adapter/dispatcher identity
principal
work_run_id
execution_attempt_id
WorkflowState/state_version
RuntimeMode
profile/scenario version
destination/provider purpose
operation fingerprint
expiry
max uses
revocation
policy version
```

Provider/tool code must receive no raw secret from the model, Task/public input, sandbox or tool
arguments.

Required flow:

```text
server-owned ProviderProfile / ToolDefinition
→ exact secret_ref
→ P1-5 SecretUse authority attestation
→ P1-3 SECRET ResourceGrant / SecurityAdmissionDecision / Capability
→ server-side mediated adapter consumes capability
→ secret store resolves material only inside adapter boundary
→ raw value never enters Agent/workspace/provenance
```

No installed SecretUse authority:

```text
SECRET
→ DENY
```

A PROVIDER or TOOL capability does not imply SECRET authority.

If the implementation cannot add this exact extension without changing accepted P1-3 semantics,
stop with `POLICY_CONFLICT_INVESTIGATION_REQUIRED`.

Do not select a concrete secret-manager product in this design.

## HOLD B — exact operation phase graph cannot represent pre-side-effect terminal outcomes

Current exact graph:

```text
PREPARED
→ SECURITY_ADMITTED
→ DISPATCH_STARTED
→ OUTCOME_KNOWN | OUTCOME_UNKNOWN
```

But current exact outcome taxonomy includes:

```text
DENIED_BEFORE_SIDE_EFFECT
CANCELLED
```

that may terminate before `DISPATCH_STARTED`.

Concrete contradictions:

```text
PREPARED
+ P1-5/P1-3 deny
→ DENIED_BEFORE_SIDE_EFFECT
```

has no valid phase edge.

Also:

```text
SECURITY_ADMITTED
+ cancel before adapter/dispatcher crossing
→ CANCELLED
```

has no valid phase edge.

Therefore the implementation would need to invent hidden transitions or leave a nonterminal operation
record.

### required correction

Freeze one exact acyclic operation lifecycle.

A valid design may use, for example:

```text
PREPARED
→ OUTCOME_KNOWN(DENIED_BEFORE_SIDE_EFFECT)

PREPARED
→ SECURITY_ADMITTED

SECURITY_ADMITTED
→ OUTCOME_KNOWN(CANCELLED)

SECURITY_ADMITTED
→ DISPATCH_STARTED

DISPATCH_STARTED
→ OUTCOME_KNOWN(...)
DISPATCH_STARTED
→ OUTCOME_UNKNOWN(TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME)
```

Exact names may differ; semantics may not.

Freeze for every outcome class:

```text
earliest legal source phase
terminal phase
whether dispatch may have occurred
whether retry is eligible
whether capability use is consumed/revoked
whether budget reservation is released/retained
whether attempt status must fail
```

Clarify whether `RETRY_EXHAUSTED` is:

```text
an operation outcome
or
an execution-attempt failure classification over multiple operations
```

Do not use one enum ambiguously for both.

Denied/failed audit provenance remains append-only.

## HOLD C — OpenAI Responses continuation/state mode is not frozen

The design chooses:

```text
OpenAI Responses API
strict custom function calling
parallel_tool_calls=false
```

This direction is compatible with the current API.

However it does not freeze whether continuation is:

```text
provider-held state via previous_response_id/conversation
```

or:

```text
AISCC-held stateless replay with store=false
```

The design currently says only:

```text
prior known continuation refs
preserve protocol items required for a valid continuation
```

That is not implementation-ready because the choice changes:

- restart authority;
- provider-side retained state;
- local durable operation payload;
- reasoning-item handling;
- privacy/data handling;
- whether provider response ID is required for continuation;
- unknown-outcome/reconciliation semantics.

Current OpenAI Responses API supports both provider-held `previous_response_id` and stateless
continuation. Stateless use with `store=false` may require replaying returned output items and
encrypted reasoning content.

### required V1 decision

Freeze one V1 transport-state mode.

Recommended for AISCC governance:

```text
OpenAI Responses V1 adapter:
store=false
no Conversation resource as execution authority
no previous_response_id as the sole continuation state

AISCC local durable operation history
→ authoritative continuation source

next provider request
→ explicitly replays the exact required prior provider output items
→ includes exact function_call_output bound to call_id
→ includes encrypted reasoning item material when the selected reasoning protocol requires it
```

Provider response/request IDs remain diagnostic/reconciliation refs, not execution authority.

If a different V1 mode is chosen, justify it and freeze its restart/privacy semantics exactly.

### response-status mapping

Also map every current Responses status into the P1-5 known/unknown contract:

```text
completed
failed
in_progress
cancelled
queued
incomplete
```

At minimum freeze which statuses may produce:

```text
PROVIDER_COMPLETED
known provider failure/rejection
continued/polled state if allowed
TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME
```

An `incomplete` response must not be silently treated as a generic provider rejection or final
AgentOutput without an exact rule.

Hosted provider tools remain disabled.

## Command Center judgment

```text
P1-4 terminal commit:
PASS / CLOSED

ExecutionStatus lifecycle:
PASS / RETAIN

PROVIDER/TOOL selector authority:
PASS / RETAIN

ProviderProfile / ToolRegistry:
PASS / RETAIN

bounded loop / unknown-outcome no-blind-retry:
PASS / RETAIN

P1-6 handoff:
PASS / RETAIN

scoped secret capability boundary:
HOLD_REWORK_REQUIRED

ExecutionOperation lifecycle:
HOLD_REWORK_REQUIRED

OpenAI Responses transport-state/status mapping:
HOLD_REWORK_REQUIRED

P1-5 design:
NOT ACCEPTED

P1-5 runtime:
NOT_STARTED

P1-6:
NOT_STARTED
```

## proof non-substitution

```text
secret_ref
!= secret capability

PROVIDER capability
!= SECRET capability

TOOL capability
!= SECRET capability

outcome taxonomy
!= representable operation state machine

Responses API selected
!= exact continuation protocol frozen

provider response ID
!= local authoritative execution state

design candidate
!= Human acceptance
```

## preservation

Preserve exact commit:

- `d99ccc4ecde585685e93960a7fa39ecbfde89f9f`

Preserve exact paths:

- `.aiassistant/tasks/done/20260828_1110_aiscc-p1-5-provider-tool-execution-contract-design-freeze-with-p1-4-terminal-commit-1.md`
- `.aiassistant/records/aiscc/cycles/20260828_1417_aiscc-p1-5-secret-operation-protocol-and-openai-state-mode-design-hold-1.cycle.md`
- `.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md`

Preserve historical design candidate identity:

```text
d2d5ce009dab6b7c369e35c917bfdb9b6d6a301216e4d35fac80a186ab465a32
```

## next action

```text
P1-5 design-only narrow rework
→ secret mediated capability extension
→ exact operation phase/outcome graph
→ exact OpenAI Responses V1 continuation/state/status mapping
→ Human design review
```

Do not implement P1-5 runtime.
