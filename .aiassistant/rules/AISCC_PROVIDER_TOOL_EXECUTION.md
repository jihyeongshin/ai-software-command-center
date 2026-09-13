# AISCC Provider / Tool Execution Contract

## 1. document status

| field | value |
|---|---|
| document_id | `AISCC-P1-5-PROVIDER-TOOL-EXECUTION-V1-CANDIDATE` |
| task_id | `20260828_1417_aiscc-p1-5-secret-operation-protocol-and-openai-state-mode-design-rework-1` |
| work_type | `DESIGN_BASELINE_REWORK` |
| result_status | `ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING` |
| authority_status | uncommitted repository canonical candidate; not accepted until Human review |
| design_base_commit | `d96949f3643e6a0610942e33d70e9da259e1e432` |
| predecessor candidate SHA-256 | `d2d5ce009dab6b7c369e35c917bfdb9b6d6a301216e4d35fac80a186ab465a32` |
| semantic owner | provider/tool execution authority, scoped secret mediation, execution operation/status contract, adapter state and bounded loop |
| implementation_status | `NOT_IMPLEMENTED` |
| runtime/provider verification | `NOT_EXECUTED` |

This document freezes the P1-5 implementation contract. It does not configure a provider, install an
SDK, create a credential, make a provider call, or admit Human-owned acceptance.

## 2. governing invariants and scope

P1-5 preserves the accepted P1-1 through P1-4 boundaries.

```text
ExecutionStatus != WorkflowState
execution-status update != WorkflowState transition
execution-status update MUST NOT increment WorkRun.state_version

EXECUTOR_COMPLETED != ACCEPTED
EXECUTION_FAILED != FAILED

ProviderResult != AgentOutput
AgentOutput != SystemState
AgentOutput != EvidenceCandidate admission
ToolOutput != AdmittedEvidence

SecurityAdmissionDecision != provider/tool authority selector
SecurityAdmissionDecision != secret-use selector attestation
SecurityAdmissionDecision != provider/tool result
SecurityAdmissionDecision != TransitionDecision

secret_ref != secret authority
PROVIDER capability != SECRET capability
TOOL capability != SECRET capability
```

P1-5 owns provider/tool profiles, resource-selector attestations, adapter calls, tool registry and
dispatch, bounded agent execution, execution attempts/events/status projection, and immutable output
refs. P1-5 does not own WorkflowState mutation, evidence admission, HumanResult/Judgment, Cycle
admission, provider account configuration, billing, or deployment.

## 3. exact execution aggregate and status lifecycle

### 3.1 aggregate

`ExecutionAttempt` is an immutable-identity child of one authoritative `WorkRun`. It has:

- `execution_attempt_id`, `work_run_id`, attempt ordinal, parent attempt ref;
- exact TaskContract ID/version and `RuntimeMode`;
- provider profile ID/version and tool-registry version;
- creation `WorkflowState/state_version` and current causal state/version;
- exact `ExecutionStatus` current projection and monotonic `execution_version`;
- first/latest event sequence, operation refs, output/submission/failure refs;
- server-owned idempotency identity and timestamps.

The `WorkRun` execution projection points to the latest attempt. Prior attempts and their terminal
status remain immutable. `execution_version` serializes execution projection updates and is separate
from `WorkRun.state_version`.

### 3.2 exact status set

No value may be added to this set:

```text
NOT_STARTED
RUNNING
EXECUTOR_COMPLETED
EXECUTION_FAILED
```

### 3.3 admitted lifecycle

| event | before | after | exact admission conditions |
|---|---|---|---|
| `EXECUTION_ATTEMPT_CREATED` | no new attempt | `NOT_STARTED` | authoritative WorkRun is `READY`; exact start-control authorization, Task/profile/mode and attempt lineage are current; no other nonterminal attempt |
| `EXECUTION_STARTED` | `NOT_STARTED` | `RUNNING` | exact prepared attempt was referenced by admitted `READY -> RUNNING`; authoritative WorkRun is now `RUNNING` at the bound version; no side effect has started; execution CAS succeeds |
| `EXECUTION_ABORTED_INVALID_HISTORY` | `NOT_STARTED` | `EXECUTION_FAILED` | same exact WorkRun/attempt lineage; current WorkRun is `RUNNING` at the exact expected state version; exact expected execution version; zero execution operations; no execution output/submission, admitted runtime evidence, or Judgment; trusted source-owned immutable provenance proves an execution side effect occurred before `EXECUTION_STARTED`; required reason is `INVALID_HISTORY_SIDE_EFFECT_BEFORE_EXECUTION_START`; atomic lock/recheck and CAS succeed |
| `EXECUTION_COMPLETED` | `RUNNING` | `EXECUTOR_COMPLETED` | final `AgentOutputRef` and `ExecutionSubmissionRef` are durably created; every admitted operation has known terminal outcome; required cleanup/sanitization is complete; WorkRun remains the exact bound `RUNNING/version` |
| `EXECUTION_FAILED` | `RUNNING` | `EXECUTION_FAILED` | fatal, cancelled, retry-exhausted, unknown-outcome, workflow-left-running, or recovery-conflict event is durably classified; new side effects are closed |

No other same-attempt status transition is valid. Duplicate exact events return the existing event and
projection. A second different terminal event is an authority conflict.

`EXECUTION_ABORTED_INVALID_HISTORY` is the only start-free terminalization edge. It disposes an
attempt whose immutable history proves that an execution side effect occurred before execution start.
It appends one typed event, preserves the original `NOT_STARTED` creation/`READY` causal state in the
event metadata, separately binds the current `RUNNING` WorkRun state/version, records the exact reason
and immutable provenance refs, and projects the attempt to `EXECUTION_FAILED`. It never fabricates a
provider output or `ExecutionSubmissionRef`.

This event is not `EXECUTION_STARTED`, a generic cancellation edge, or legal merely because a timeout
occurred. It is forbidden after provider operation creation, does not authorize retry, and cannot be
requested through the generic lifecycle transition API or by direct database/projection editing.
Ordinary `EXECUTION_FAILED` from `RUNNING` remains unchanged. Exact retry of the same abort identity,
versions, reason, and provenance returns the existing authoritative result without another event;
any changed reason, identity, version, or provenance is an authority conflict.

`EXECUTION_ATTEMPT_CREATED` is an inert start preparation admitted under P1-3
`START_EXECUTION_CONTROL`. It supplies a candidate ref that P1-4 System authority may validate when
issuing `G_EXECUTION_STARTED`; P1-5 cannot mint a P1-4 guard fact. Normal provider/tool work begins
only after `WorkflowState=RUNNING` and `EXECUTION_STARTED` admission.

### 3.4 retry and rework

An attempt in `EXECUTOR_COMPLETED` or `EXECUTION_FAILED` never returns to `RUNNING`. Same-WorkRun
retry is permitted only as a new `ExecutionAttempt` after an admitted workflow lineage has returned
the WorkRun to `READY` and a fresh start authorization is admitted. This includes an admitted
`REWORK_REQUIRED -> READY` lineage. A terminal WorkflowState cannot create a new attempt.

Provider-internal retry is not an ExecutionStatus retry. It creates a new provider operation-attempt
under the same `ExecutionAttempt` while status remains `RUNNING`, consumes the same finite profile
budget, and is permitted only by section 9.4.

### 3.5 concurrency, crash, and idempotency

- attempt creation is serialized per `work_run_id` and uses latest-attempt CAS;
- lifecycle admission is serialized per `execution_attempt_id` and uses `execution_version` CAS;
- start identity is `work_run_id + ready_state_version + attempt_ordinal + profile/version`;
- lifecycle event identity is `execution_attempt_id + event_kind + causal state/version + payload hash`;
- same identity and fingerprint returns the existing event; same identity with different immutable
  content is an authority conflict;
- concurrent starts admit at most one; concurrent terminal events admit at most one;
- event append and current execution projection update are one database transaction;
- a crash between P1-4 `READY -> RUNNING` and P1-5 `EXECUTION_STARTED` leaves status `NOT_STARTED`;
  recovery may admit the exact start from durable prepared/transition refs, but no side effect may run
  first;
- leaving WorkflowState `RUNNING` invalidates normal capabilities. A still-`RUNNING` execution
  projection is reconciled to `EXECUTION_FAILED` with the causal old and current state/version; it is
  never silently resumed.

## 4. provider/tool resource authority integration

### 4.1 owner split

P1-5 supplies server-owned resource identity for `ResourceDomain.PROVIDER` and
`ResourceDomain.TOOL`; P1-3 remains the ALLOW/DENY and capability issuer.

```text
P1-5 ProviderToolResourceAuthority
-> validates registry/profile selector and emits owner-bound selector attestation

P1-3 SecurityPolicy
-> validates every security guard
-> issues SecurityAdmissionDecision, ResourceGrant, and short-lived Capability
```

A selector attestation is neither a `SecurityAdmissionDecision` nor a capability. If the injected
P1-5 authority/verifier is absent, returns unknown, or cannot prove exact ownership, `PROVIDER` and
`TOOL` remain `DENY`. No global boolean, caller allowlist, display-name match, or Agent assertion is
accepted.

The next implementation introduces a typed `ProviderToolResourcePolicyPort` into `SecurityPolicy`.
For P1-5 domains, `_scope_is_policy_owned` delegates only to that port and then continues all existing
P1-3 requester/task/action-state/limit/budget/idempotency/target-control checks. The port cannot call
`SecurityPolicy.evaluate`, issue a `ResourceGrant`, or access its issuer tokens.

### 4.2 canonical resource identity

Provider resource identity is the tuple:

```text
PROVIDER
provider_profile_id
provider_profile_version
provider_id
model_ref_hash
adapter_protocol_version
```

Tool resource identity is the tuple:

```text
TOOL
tool_registry_id
tool_registry_version
tool_id
tool_schema_version
dispatcher_version
```

The structured tuple is authoritative. `ResourceScope.resource_id` is only its stable serialized
projection. The raw model reference is read from the server profile, never public/Agent input.

### 4.3 selector attestation

`ProviderToolSelectorAttestation` is immutable, issuer-backed, versioned, and binds:

- attestation ID/version and resource-domain canonical identity;
- `RuntimeMode`, profile ID/version, scenario ID/version;
- principal, `work_run_id`, `execution_attempt_id`;
- authoritative `WorkflowState/state_version` and `SecurityActionClass`;
- exact operation fingerprint;
- issued/expiry time, max uses, revocation state and policy version.

P1-3 `ResourceGrant` and `Capability` must carry and validate the same operation fingerprint and
selector-attestation ref in addition to their existing exact scope equality. A mismatch denies before
side effect. State/version, mode, profile, run, principal, expiry, revocation and use bounds remain
independent mandatory checks.

### 4.4 operation fingerprint

Canonical JSON uses RFC 8785 JSON Canonicalization Scheme bytes, UTF-8, then lowercase SHA-256. No
raw secret is included. Provider fingerprint input is:

```text
schema_version, operation_kind, work_run_id, execution_attempt_id,
WorkflowState/state_version, RuntimeMode, scenario ID/version,
provider profile ID/version, provider/model/adapter identity,
normalized input hash, tool-definition-set hash, output/token/time bounds,
call ordinal, parent operation ID
```

Tool fingerprint input is:

```text
schema_version, operation_kind, work_run_id, execution_attempt_id,
WorkflowState/state_version, RuntimeMode, scenario ID/version,
registry ID/version, tool ID/schema version, canonical argument object,
underlying resource requirement hashes, call ordinal, provider call/call_id ref
```

Canonicalization failure, non-finite number, duplicate JSON key, unknown field, invalid Unicode, or
schema mismatch denies authorization.

### 4.5 scoped secret-use authority extension

Accepted P1-2 permits only an authorized adapter to use a purpose-bound opaque secret handle. Current
P1-3 intentionally returns false for `ResourceDomain.SECRET` because no production secret owner is
installed. P1-5 extends that fail-closed point through an injected typed port; it does not remove the
P1-3 check.

```text
P1-5 SecretUseAuthorityPort
-> validates server-owned provider/tool secret selector
-> issues/verifies SecretUseSelectorAttestation only

P1-3 SecurityPolicy
-> remains sole SecurityAdmissionDecision owner
-> remains sole ResourceGrant and Capability issuer
-> remains sole capability consume/revoke/use-count owner
```

`SecretUseAuthorityPort` has no access to P1-3 issuer tokens and cannot call `SecurityPolicy.evaluate`,
issue a grant/capability, resolve secret material, or dispatch an operation. Its exact methods are:

```text
attest(SecretUseSelectorRequest) -> SecretUseSelectorAttestation | DENY_REASON
verify(attestation, SecretUseSelectorRequest) -> VALID | DENY_REASON
```

The request is assembled only from current server-owned profile/registry data and authoritative
run/security context. Public, Task, Agent, provider response, and tool arguments cannot provide or
override any selector field. If the port is absent, returns unknown, or cannot verify the exact
attestation, P1-3 `_scope_is_policy_owned` remains false for `ResourceDomain.SECRET` and admission is
`DENY`.

`SecretUseSelectorAttestation` is immutable, typed, issuer-backed, and versioned. It binds exactly:

- attestation ID/version and secret-authority policy version;
- opaque `secret_ref` plus a stable non-secret secret identity hash and exact secret class;
- enumerated purpose ID and exact destination/provider purpose;
- the section 4.2 provider or tool canonical resource identity;
- registered adapter protocol/version or dispatcher/version identity;
- principal, `work_run_id`, `execution_attempt_id`, and operation ID;
- authoritative `WorkflowState/state_version` and `RuntimeMode`;
- profile ID/version and scenario ID/version;
- exact operation fingerprint from section 4.4;
- issue/expiry timestamps, positive finite max uses, use ordinal, and revocation state.

The corresponding `ResourceScope` has `domain=ResourceDomain.SECRET` and a stable serialized identity
derived from secret class and non-secret identity hash; it never embeds the raw secret or a public
lookup key. P1-3 `ResourceGrant` and `Capability` must bind the attestation ref, exact operation
fingerprint, purpose, destination, run/state/version/mode/profile/scenario, expiry, revocation and use
bounds. Any mismatch denies before material resolution.

```text
secret_ref
!= SecretUseSelectorAttestation
!= SecurityAdmissionDecision
!= ResourceGrant
!= Capability

PROVIDER or TOOL ALLOW
!= SECRET ALLOW
```

Provider credential use follows this exact mediated flow:

```text
server-owned ProviderProfile.secret_ref and purpose
-> P1-5 SecretUseSelectorAttestation
-> separate P1-3 SECRET ResourceGrant / SecurityAdmissionDecision / Capability
-> broker validates PROVIDER and SECRET capabilities independently
-> broker consumes both exact capabilities immediately before adapter crossing
-> server-side ProviderAdapter asks the private resolver for the exact secret lease
-> resolver verifies the consumed SECRET capability and returns material only inside adapter scope
-> adapter applies material directly to the exact profile-owned transport destination
-> lease closes and all related capabilities are revoked at terminal outcome/timeout/cancel/cleanup
```

All capabilities are validated before either use is consumed. Consumption is one local broker
admission transaction; after consumption, a resolver/transport failure does not restore a use. Raw
material never enters Agent input/output, public/session data, workspace, environment dump, command
arguments, ToolRegistry arguments, provider protocol history, event/provenance bodies, or Replay.
Redaction is defense in depth and never substitutes for the mediated boundary.

A ToolDefinition may declare a server-owned `SecretRequirement` containing the same exact selector
fields. Tool secret use follows:

```text
exact ToolDefinition SecretRequirement
-> P1-5 SecretUseSelectorAttestation
-> separate P1-3 SECRET grant/admission/capability
-> broker independently consumes TOOL plus SECRET and every other underlying capability
-> registered server dispatcher's private resolver supplies material only inside dispatcher scope
-> bounded tool invocation
-> lease close and revoke
```

The model/tool arguments cannot name a secret, purpose, provider, destination, resolver, or reference.
A TOOL capability cannot resolve material. A PROVIDER capability cannot resolve material. Missing,
expired, revoked, use-exhausted, wrong-purpose, wrong-resource, wrong-adapter/dispatcher,
wrong-principal/run/attempt/state/version/mode/profile/scenario/destination, or fingerprint-mismatched
secret authority is `DENY` before resolution. No concrete secret-manager product is selected here.

## 5. server-owned ProviderProfile

`ProviderProfile` is versioned, immutable after publication, non-secret configuration with these
required fields:

| field | contract |
|---|---|
| `profile_id`, `version` | stable server-owned identity; exact version required |
| `provider_id`, `adapter_protocol_version` | registered adapter identity/protocol |
| `model_ref` | server-fixed opaque model reference; never caller-selected |
| `endpoint_ref` | server-owned endpoint class/ref, not a public URL field |
| `allowed_runtime_modes` | explicit finite set |
| `scenario_allowlist` | exact scenario IDs/versions; owner mode still explicit |
| `secret_ref` | opaque server secret reference only; never secret material or authority; requires section 4.5 attestation plus separate P1-3 SECRET capability |
| `tool_registry_id/version`, `tool_allowlist` | exact custom-function surface |
| `provider_call_maximum` | positive finite count including retries/continuations |
| `agent_round_trip_maximum` | positive finite loop rounds |
| `tool_call_maximum` | positive finite total tool calls |
| `timeout_policy` | connect/read/total positive finite bounds |
| `retry_policy` | finite attempts, backoff, retryable known classes; unknown-outcome retry forbidden |
| `output_token_bound`, `output_byte_bound` | positive finite response bounds |
| `input_byte_bound` | positive finite serialized request bound |
| `continuation_item_maximum`, `continuation_byte_bound`, `continuation_token_estimate_bound` | positive finite local replay bounds; no truncation/fallback |
| `private_protocol_retention_policy_ref` | server-owned classification/encryption/retention contract for local continuation state |
| `budget_policy_ref` | authoritative P1-3 application budget policy ref |
| `data_classification_policy_ref` | input/output retention, sanitation and public-projection rules |
| `parallel_tool_calls` | fixed `false` for the V1 deterministic loop |
| `enabled`, `issued_at`, `revoked_at` | server lifecycle; disabled/revoked fails closed |

Exact numeric values, live model IDs, price, account, endpoint, API key and provider spend limit are
not frozen here. An implementation/release configuration must supply positive finite values and
current evidence.

Mode requirements:

- `PUBLIC_RECORDED_REPLAY`: no provider profile is executable; provider calls are exactly zero.
- `PUBLIC_BOUNDED_LIVE`: scenario selects one server-fixed profile/version; public input cannot
  select provider, model, endpoint, secret, tool or fallback.
- `OWNER_SELF_DOGFOOD`: an explicitly owner-authorized server profile is required and remains finite,
  state-bound, budget-bound and tool-registry-bound.

## 6. provider-neutral core and OpenAI adapter direction

### 6.1 separation

```text
AgentExecutionService
-> ProviderAdapter port
-> ProviderCall
-> ProviderResult
-> AgentOutput producer record
```

`AgentExecutionService` owns the bounded loop, not provider serialization. `ProviderAdapter` owns
only protocol mapping and sanitized transport classification. `ProviderProfile` owns provider/model
choice. `ProviderCall` is an immutable admitted operation command. `ProviderResult` is an immutable
transport result. `AgentOutput` is the final producer output assembled by AISCC after validation.

The adapter must not mutate WorkRun or ExecutionStatus, mint security/transition decisions, select a
credential/model outside the profile, expose raw errors/secrets, execute a tool, or convert output to
evidence truth.

### 6.2 ProviderCall and ProviderResult

`ProviderCall` binds operation ID/fingerprint, attempt/run/state/version/mode, profile/version,
server-selected model/endpoint/secret refs, bounded input refs/hashes, exact custom-tool definitions,
call ordinal, timeout/output limits and prior known continuation refs.

`ProviderResult` records operation ID, provider request/response refs when known, exact outcome class,
structured output items, proposed custom tool calls, usage metadata, sanitized error class, result
hash, duration and received timestamp. Raw secret, stack trace, private endpoint detail and
unsanitized provider payload are excluded from public/provenance views.

### 6.3 concrete OpenAI Responses adapter direction

After Human acceptance, the first concrete adapter protocol is OpenAI Responses API custom function
calling. It is a protocol direction, not a configured provider fact. V1 uses exactly
`background=false`, `stream=false`, `store=false`, `parallel_tool_calls=false`, and
`truncation=disabled`. The adapter:

- sends only the server profile's model and limits;
- defines only current ToolRegistry entries as `type=function` tools with JSON Schema and
  `strict=true`;
- yields zero or one custom call per round for deterministic authorization and accounting;
- treats returned `function_call` name/arguments/`call_id` as untrusted proposals;
- returns a sanitized `function_call_output` bound to the exact `call_id` only after AISCC registry,
  TOOL admission, underlying-resource admission and dispatch complete;
- does not expose or enable provider-hosted web search, file search, MCP/connectors, shell, computer,
  code execution, apply-patch, or any other hosted execution tool;
- rejects an unexpected hosted-tool output item as `PROVIDER_REJECTED`/protocol violation and starts
  no AISCC side effect.

The request sets `include=["reasoning.encrypted_content"]` when the selected profile/model protocol can
emit reasoning items. This asks for opaque encrypted continuation material; it does not expose or
admit reasoning as truth.

### 6.4 exact V1 continuation and transport-state strategy

V1 has one state strategy and no runtime-selectable alternative:

```text
Responses store=false
conversation field = OMITTED
previous_response_id field = OMITTED
provider Conversation resource = NOT_USED
provider response/request ID = DIAGNOSTIC_AND_RECONCILIATION_REF_ONLY
AISCC durable local protocol history = SOLE CONTINUATION AUTHORITY
```

`store=false` is an API storage request flag, not a Zero Data Retention contractual claim. V1 never
retrieves a response or falls back to `previous_response_id`/Conversation when local continuation
state is unavailable. A deployment cannot switch modes for convenience; changing this strategy needs
a separately accepted design update.

Before accepting a tool proposal or final output, AISCC durably records a
`PrivateProviderProtocolState` for that provider operation. It contains, in provider-returned order:

- protocol schema/adapter/profile/model versions and response ordinal;
- the exact bounded request item hashes and instruction/tool-definition-set hashes;
- every required prior response output item, including message, function-call and reasoning items;
- item type/ID/order, exact `call_id`, function name/argument hash, and assistant-item phase if present;
- encrypted reasoning content bytes when returned and required for continuation;
- exact tool output ref/hash and the sanitized `function_call_output` bytes bound to that `call_id`;
- provider request/response IDs as diagnostic refs, response status, usage, content hash, byte count,
  classification, creation time and retention/cleanup policy ref.

The private protocol body is encrypted at rest by the future persistence boundary, integrity-hashed,
access-controlled to the adapter/orchestrator, and excluded from Agent/public output, provenance
bodies, Evidence/Judgment, Replay, logs, and reports. Hashes and classified refs may enter provenance;
opaque encrypted reasoning bytes may not. Encrypted reasoning material is protocol state only and is
never parsed, summarized, treated as evidence, or used to infer success.

The next request explicitly replays the exact bounded initial/user inputs and every required prior
provider output item, then appends exactly one `function_call_output` for the admitted call ID. Item
order, IDs, `call_id`, function identity, encrypted content and assistant `phase` are preserved exactly.
No item is reconstructed from prose or provider response ID.

ProviderProfile adds positive finite `continuation_item_maximum`, `continuation_byte_bound`,
`continuation_token_estimate_bound`, and `private_protocol_retention_policy_ref`. These are independent
of call/round/output bounds. If required state is missing, corrupt, hash-mismatched, out of order,
unsupported, over any bound, or lacks an exact call-ID/tool-output pair, AISCC records
`DENIED_BEFORE_SIDE_EFFECT` from `PREPARED`, admits `EXECUTION_FAILED`, and makes no provider call.
There is no automatic truncation, compaction, provider-held-state fallback, or silent continuation.

### 6.5 exact Responses status mapping

V1 is synchronous and performs zero follow-up status-poll calls. The original create call consumes one
provider-call count, elapsed-time bound and budget reservation. A returned `queued` or `in_progress`
is not a terminal adapter success; because V1 does not depend on stored provider state, it maps to
`TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME`, retains conservative budget reservation, requires
reconciliation, and admits `EXECUTION_FAILED` without polling or retry.

| Responses status/shape | P1-5 operation outcome | exact behavior |
|---|---|---|
| `queued` | `TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME` / `OUTCOME_UNKNOWN` | nonterminal provider state returned from the synchronous call; no output/tool admission, no polling, no retry, retain budget, reconcile, fail attempt |
| `in_progress` | `TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME` / `OUTCOME_UNKNOWN` | same as `queued` |
| `completed` + one valid final message | `PROVIDER_COMPLETED` / `OUTCOME_KNOWN` | durably validate/bound/sanitize exact output items, then permit final `AgentOutputRef` creation |
| `completed` + one valid custom `function_call` | `PROVIDER_COMPLETED` / `OUTCOME_KNOWN` | durably store exact private protocol items and emit one untrusted tool proposal; no AgentOutput or workflow truth yet |
| `completed` + invalid/multiple/hosted/unsupported item | `PROVIDER_REJECTED` / `OUTCOME_KNOWN` | protocol violation; no tool side effect, no continuation, fail attempt |
| `failed` | `PROVIDER_REJECTED` / `OUTCOME_KNOWN` | persist sanitized error/status; retry only for an exact profile-enumerated known retryable code and remaining bounds |
| `cancelled` | `CANCELLED` / `OUTCOME_KNOWN` from `DISPATCH_STARTED` | provider terminal cancellation is verified; no output/tool admission and attempt fails; a local cancel request alone cannot create this mapping |
| `incomplete` | `PROVIDER_INCOMPLETE` / `OUTCOME_KNOWN` | persist sanitized `incomplete_details`; never create AgentOutput/tool proposal, never relabel completed/rejected, no V1 automatic retry, fail attempt |

An absent/unknown status, malformed terminal body, local transport timeout after `DISPATCH_STARTED`, or
connection loss before a durable terminal response maps to
`TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME`. Later reconciliation may append a known provider terminal fact
but never rewrites the original unknown event or silently resumes the attempt.

Protocol references at design time: [Responses create](https://developers.openai.com/api/reference/cli/resources/responses/methods/create),
[Function calling](https://developers.openai.com/api/docs/guides/function-calling), and
[manual history/reasoning replay guidance](https://developers.openai.com/api/docs/guides/latest-model).
Exact SDK, model/account availability and live behavior remain future implementation/release evidence.

## 7. versioned ToolRegistry and broker

### 7.1 registry entry

`ToolRegistry` and every `ToolDefinition` are server-owned and immutable by version. Every entry has:

```text
registry_id, registry_version
tool_id, schema_version, dispatcher_version
description
strict JSON input schema
side_effect_classification
allowed RuntimeMode/profile/scenario tuples
underlying resource requirements
timeout policy
retry/idempotency policy
output byte/schema bound
enabled/revoked lifecycle
```

`side_effect_classification` is exactly `READ_ONLY`, `IDEMPOTENT_BY_KEY`, or `NON_IDEMPOTENT`.
Unknown classification fails closed. Schemas reject additional properties, require every declared
field (nullable fields explicitly include null), and cannot contain executable names, free-form shell,
repository URLs, network destinations or credential fields supplied by the model.

Any `SecretRequirement` is a separate server-owned registry field with exact secret class/ref hash,
purpose, destination, dispatcher and use bounds. It is never projected into the model-visible input
schema or accepted from arguments.

### 7.2 dispatch order

```text
model function_call candidate
-> exact registry/version lookup
-> strict schema validation
-> RFC 8785 argument canonicalization and fingerprint
-> P1-5 TOOL selector attestation
-> P1-3 TOOL SecurityAdmissionDecision and capability
-> product dispatcher lookup
-> separate P1-3 admission/capability for every underlying PROCESS / FILESYSTEM / NETWORK / SECRET action
-> bounded invocation
-> sanitized ToolOutputRef and operation event
```

A TOOL capability authorizes only the logical registry invocation. It never authorizes its underlying
process, filesystem, network, repository or secret operation. Unknown tool, schema version, field,
dispatcher, operation fingerprint or underlying authority denies before side effect.

There is no arbitrary shell tool, dynamic executable, model-selected URL, model-selected repository,
or generic network-fetch tool. Tool descriptions cannot expand policy.

## 8. deterministic bounded agent loop

One `ExecutionAttempt` follows this exact order:

1. load and consistency-check authoritative WorkRun and current execution projection;
2. under `READY`, create `NOT_STARTED` attempt and inert start authorization;
3. after P1-4 admits `READY -> RUNNING`, admit `ExecutionStatus=RUNNING`;
4. before every provider/tool side effect, reload authoritative WorkRun and require the same
   `RUNNING/state_version`, mode, profile and scenario;
5. create durable operation intent, obtain every exact provider/tool/secret selector attestation and
   separate P1-3 admission/capability required by that operation;
6. make one provider call;
7. if final structured output, validate/sanitize/bound and create `AgentOutputRef`;
8. if one custom tool proposal, perform section 7 admission/dispatch, record `ToolOutputRef`, then
   continue with a new admitted provider operation;
9. stop at any profile maximum, denial, timeout, cancellation, stale capability or unknown outcome;
10. atomically admit `EXECUTOR_COMPLETED` plus `ExecutionSubmissionRef`, or admit
    `EXECUTION_FAILED` plus exact failure ref;
11. P1-4 separately evaluates any `RUNNING -> ADMISSION_PENDING/BLOCKED/REWORK_REQUIRED/FAILED`
    request. P1-5 never requests an outcome state as an authoritative decision.

Provider calls, agent rounds, tool calls, provider retry attempts, elapsed time, output tokens/bytes
and budget are independent monotonic counters. Every configured maximum is positive and finite; the
effective bound is the minimum of profile, scenario, security capability and budget bounds.

If WorkflowState or `state_version` changes during the loop, all old capabilities become stale and no
silent continuation occurs. A fresh capability may continue the same execution attempt only when the
authoritative WorkRun is still the identical `RUNNING/state_version`, the attempt projection remains
`RUNNING`, all preceding operation outcomes are known, and mode/profile/scenario/counters remain
valid. Otherwise the attempt fails and any retry requires section 3.4 new-attempt lineage.

## 9. durable operation protocol and outcome taxonomy

### 9.1 operation phase

Each provider/tool side effect has one append-only `ExecutionOperation`. Its exact acyclic phase set
is:

```text
PREPARED
SECURITY_ADMITTED
DISPATCH_STARTED
OUTCOME_KNOWN
OUTCOME_UNKNOWN
```

The complete legal edge set is:

```text
PREPARED
-> OUTCOME_KNOWN(DENIED_BEFORE_SIDE_EFFECT)
-> SECURITY_ADMITTED

SECURITY_ADMITTED
-> OUTCOME_KNOWN(CANCELLED)                 # pre-dispatch cancellation
-> DISPATCH_STARTED                        # atomic with capability consumption

DISPATCH_STARTED
-> OUTCOME_KNOWN(DEFINITELY_NOT_SENT)
-> OUTCOME_KNOWN(PROVIDER_REJECTED)
-> OUTCOME_KNOWN(PROVIDER_COMPLETED)
-> OUTCOME_KNOWN(PROVIDER_INCOMPLETE)
-> OUTCOME_KNOWN(TOOL_COMPLETED)
-> OUTCOME_KNOWN(TOOL_FAILED)
-> OUTCOME_KNOWN(CANCELLED)                 # verified terminal provider/tool cancellation
-> OUTCOME_UNKNOWN(TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME)
```

No other edge exists. In particular, `PREPARED -> DISPATCH_STARTED`, `PREPARED -> OUTCOME_UNKNOWN`,
`SECURITY_ADMITTED -> OUTCOME_UNKNOWN`, a pre-dispatch outcome other than the two listed above, an
unknown outcome other than `TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME`, or any outgoing edge from a
terminal phase is an authority conflict. Duplicate exact phase events are idempotent; same identity
with different phase/outcome is a conflict.

`PREPARED` is durable intent with no admitted composite authority and no side effect. All required
PROVIDER/TOOL/SECRET/underlying-resource decisions and capabilities must be durable before
`SECURITY_ADMITTED`; partial authority is revoked and the operation terminates as denied.
`SECURITY_ADMITTED` proves all capabilities exist but none has been consumed and dispatch has not
started. `SECURITY_ADMITTED -> DISPATCH_STARTED`, capability validation, and consumption are one local
broker admission boundary immediately before adapter/dispatcher crossing. `DISPATCH_STARTED` does not
claim the external side observed the request. Only a terminal phase may drive accounting,
continuation, output, retry or attempt completion/failure.

Crash/restart is exact: `PREPARED` is re-evaluated or denied before side effect; `SECURITY_ADMITTED`
proves dispatch did not cross and recovery revokes capabilities then records pre-dispatch `CANCELLED`;
`DISPATCH_STARTED` becomes unknown unless the exact adapter/provider/dispatcher record proves one
known terminal outcome. `OUTCOME_KNOWN` and `OUTCOME_UNKNOWN` are never rewritten. Later reconciliation
is a new append-only fact referencing the unknown operation, not a hidden phase transition.

### 9.2 exact outcome classes

```text
DENIED_BEFORE_SIDE_EFFECT
DEFINITELY_NOT_SENT
PROVIDER_REJECTED
PROVIDER_COMPLETED
PROVIDER_INCOMPLETE
TOOL_COMPLETED
TOOL_FAILED
TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME
CANCELLED
```

- `DENIED_BEFORE_SIDE_EFFECT`: P1-5/P1-3/schema/budget/capability deny; dispatch did not start.
- `DEFINITELY_NOT_SENT`: adapter proves no bytes/request were handed to transport.
- `PROVIDER_REJECTED`: provider returned a known rejection and no successful result.
- `PROVIDER_COMPLETED`: complete bounded provider response is durably captured and hashed.
- `PROVIDER_INCOMPLETE`: provider returned a known terminal `incomplete` response and exact sanitized
  `incomplete_details`; it is neither completed nor an arbitrary rejection.
- `TOOL_COMPLETED` / `TOOL_FAILED`: dispatcher returned a known bounded outcome.
- `TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME`: dispatch may have reached provider/tool but no truthful
  terminal result is known.
- `CANCELLED`: dispatch was definitely prevented/stopped before effect, or the adapter/dispatcher
  provides a verified terminal cancellation. A local cancel request alone is insufficient.

`RETRY_EXHAUSTED` is not an `ExecutionOperation` outcome. It is exactly an
`ExecutionAttemptFailureClass` over a finite ordered set of operation attempts. The last operation
retains its truthful outcome; the failure ref lists every operation ID/outcome, the exhausted bound,
and remaining budget. It admits `EXECUTION_FAILED` once and cannot be reused as a provider/tool
terminal result.

### 9.3 exact outcome/phase/authority matrix

| outcome | legal source -> terminal | side-effect fact | retry eligibility | capability semantics | budget semantics | attempt must become `EXECUTION_FAILED` | reconciliation |
|---|---|---|---|---|---|---|---|
| `DENIED_BEFORE_SIDE_EFFECT` | `PREPARED -> OUTCOME_KNOWN` | definitely absent | none for this operation; corrected authority requires a new operation identity and remaining attempt bounds | consume none; revoke any partial grant/capability | release unused reservation; charge no provider/tool use | yes | no |
| pre-dispatch `CANCELLED` | `SECURITY_ADMITTED -> OUTCOME_KNOWN` | definitely absent | none | consume none; revoke all admitted capabilities | release external/tool reservation; retain local admission accounting | yes | no |
| `DEFINITELY_NOT_SENT` | `DISPATCH_STARTED -> OUTCOME_KNOWN` | definitely absent; adapter proves transport/dispatcher did not accept the request | new operation only when profile/tool class permits and all bounds remain | dispatch use is consumed; revoke operation capabilities | release external spend reservation after proof; retain call/time attempt counters | no while retry remains; otherwise `RETRY_EXHAUSTED` makes yes | no |
| `PROVIDER_REJECTED` | `DISPATCH_STARTED -> OUTCOME_KNOWN` | provider request known occurred; successful result absent | only exact profile-enumerated known retryable code | consume and revoke PROVIDER/SECRET/underlying operation capabilities | settle known usage/charge, release provably unused reservation | no while eligible retry remains; otherwise yes | no |
| `PROVIDER_COMPLETED` | `DISPATCH_STARTED -> OUTCOME_KNOWN` | provider call and bounded result known occurred | never retry same operation | consume and revoke all operation capabilities | charge known usage and settle reservation | no | no |
| `PROVIDER_INCOMPLETE` | `DISPATCH_STARTED -> OUTCOME_KNOWN` | provider call occurred; completion absent | no V1 automatic retry | consume and revoke all operation capabilities | settle returned usage and conservatively charge/release by authoritative meter | yes | no; outcome is known |
| `TOOL_COMPLETED` | `DISPATCH_STARTED -> OUTCOME_KNOWN` | exact dispatcher result/effect disposition known | never retry same operation | consume and revoke TOOL/SECRET and every underlying capability | charge/settle exact tool/resource use | no | no; normal cleanup still applies |
| `TOOL_FAILED` | `DISPATCH_STARTED -> OUTCOME_KNOWN` | exact `NONE`, `KNOWN_APPLIED`, or `KNOWN_PARTIAL` effect disposition required | section 9.4 side-effect-class rules only | consume and revoke TOOL/SECRET and every underlying capability | settle known use; release only provably unused reservation | no while eligible retry remains; otherwise yes | no for classification; `KNOWN_PARTIAL` requires bounded cleanup/compensation |
| `TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME` | `DISPATCH_STARTED -> OUTCOME_UNKNOWN` | may have occurred | none | consume and revoke all operation capabilities | retain reservation/possible charge conservatively | yes | yes |
| post-dispatch `CANCELLED` | `DISPATCH_STARTED -> OUTCOME_KNOWN` | provider/dispatcher proves terminal cancellation and no ambiguous effect | none | consume and revoke all operation capabilities | settle known use and release only provably unused reservation | yes | no; ambiguity would be unknown instead |

### 9.4 retry rules

Provider retry is allowed only for `DEFINITELY_NOT_SENT` or a profile-enumerated, known retryable
`PROVIDER_REJECTED`, with a new operation-attempt ID, new capability use, remaining call/time/budget
and the same immutable input fingerprint. `PROVIDER_COMPLETED` is never retried.

`TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME` is never blindly retried, because an external provider is not
assumed idempotent. It durably closes the attempt as `EXECUTION_FAILED`, conservatively retains budget
reservation/charge for reconciliation, and requires operator/provider-specific reconciliation before
any new attempt. No WorkflowState mutation follows automatically.

Tool retry also requires remaining bounds and:

- `READ_ONLY`: known definitely-not-started or known failed-without-effect only;
- `IDEMPOTENT_BY_KEY`: exact server-generated idempotency key and verified dispatcher contract;
- `NON_IDEMPOTENT`: no automatic retry after dispatch starts;
- unknown outcome: no automatic retry for any class.

Every retry is a new `ExecutionOperation` with a new operation-attempt ID, a fresh selector/secret
attestation, fresh P1-3 admissions/capabilities and an independently consumed provider-call/time/budget
count. When no eligible retry remains, one attempt-level `RETRY_EXHAUSTED` failure ref admits
`EXECUTION_FAILED`; it does not change the last operation outcome.

### 9.5 cancellation and timeout

Cancel/timeout closes new operation admission, revokes capabilities, requests bounded termination and
records the actual outcome. If send/effect ambiguity remains, classification is
`TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME` with `cancel_requested=true`, not `CANCELLED`. Cancellation and
timeout update ExecutionStatus only through the lifecycle event and never mutate WorkflowState.

### 9.6 operation identity

Operation ID and idempotency key bind:

```text
work_run_id
execution_attempt_id
operation kind and ordinal
provider/tool canonical resource identity
operation fingerprint
WorkflowState/state_version
RuntimeMode/profile/scenario versions
parent operation/response/call_id when applicable
```

Same key plus same fingerprint returns the durable existing operation. Same key plus different
content is an authority conflict and produces no side effect.

## 10. append-only execution persistence

### 10.1 event minimum

Every event/operation record supports:

- Task/run/execution attempt/event/operation identities and ordering sequence;
- observed and authoritative WorkflowState/state_version;
- ExecutionStatus before/after and `execution_version` when applicable;
- RuntimeMode, profile/provider/model-hash/adapter and registry/tool versions;
- P1-5 provider/tool and secret-use selector refs, P1-3 resource grant/capability/admission refs;
- request/input/tool-argument/result hashes, never raw secrets;
- private provider protocol-state ref/hash/classification/byte count, never its opaque body in public
  provenance;
- usage metadata, duration, retry/cancel/failure/outcome class;
- output/artifact/submission refs and hashes;
- data classification/sanitization result, timestamp and admitting System owner.

### 10.2 projection and atomicity

Append-only records include attempt creation, lifecycle events, every section 9 legal phase edge,
provider/tool results, private protocol-state refs, output refs, cancellation/reconciliation and
conflict/denial. The mutable projection contains latest attempt, ExecutionStatus, `execution_version`,
counters and latest sequence.

Lifecycle event append and projection CAS are atomic. Operation phase append and operation-projection
CAS are atomic. `PREPARED` is durable before evaluation; all authority refs are durable before
`SECURITY_ADMITTED`; capability consumption and `DISPATCH_STARTED` admission share one local broker
boundary; terminal outcome is additive. Event identity uniqueness makes duplicate admission
idempotent. Per-attempt serialization and database ordering prevent concurrent counter or status loss.

Restart reconstructs every attempt and operation projection from ordered events and compares it with
the stored projection before fresh start, side effect, continuation, completion or failure. It also
verifies every required private protocol-state hash, item order, `call_id` and bound. Missing event,
illegal phase/lifecycle, counter mismatch, corrupt/missing continuation item, duplicate conflicting
identity, projection mismatch, orphan outcome or unknown resource ownership fails closed. Recovery
never auto-repairs, falls back to provider-held state, or infers success from process exit, provider
prose, missing heartbeat or last Agent message.

Pure execution event/status admission never increments `WorkRun.state_version`. It records the causal
and current state/version and leaves all WorkflowState mutation to P1-4.

## 11. output and P1-6 handoff

P1-5 producer refs are immutable content-addressed records:

- `AgentOutputRef`: final bounded/sanitized Agent output and provider-result lineage;
- `ToolOutputRef`: one known tool outcome and exact operation/argument/result hashes;
- `ExecutionArtifactRef`: classified artifact metadata/hash and storage ref;
- `ExecutionSubmissionRef`: one completed attempt, terminal execution event, complete output/artifact
  ref set, event range/hash, Task/run/profile/registry and causal `RUNNING/state_version`.

Only `EXECUTION_COMPLETED` may create an `ExecutionSubmissionRef`. P1-4 System authority validates
this producer ref and may issue its own owner-bound `G_EXECUTOR_SUBMISSION` fact; P1-5 cannot mint the
fact or transition `RUNNING -> ADMISSION_PENDING`.

```text
AgentOutputRef / ToolOutputRef / ExecutionArtifactRef / ExecutionSubmissionRef
!= EvidenceCandidateRef admission
!= AdmittedEvidenceRef
!= Judgment
```

P1-6 later owns requirement matching, candidate admission/rejection, owner/proof type, freshness,
applicability and admitted evidence refs. P1-5 supplies immutable producer identity, content/result
hashes, execution lineage, sanitizer classification, causal state/version and security refs only. A
provider/tool success, execution completion or P1-5 sanitizer PASS cannot satisfy an evidence
requirement by itself.

## 12. exact RuntimeMode matrix

| contract | `OWNER_SELF_DOGFOOD` | `PUBLIC_RECORDED_REPLAY` | `PUBLIC_BOUNDED_LIVE` |
|---|---|---|---|
| provider calls | explicit owner-authorized server profile; finite | exactly `0` | server-fixed scenario profile; finite |
| tool calls | explicit registry/profile allowlist | exactly `0` | exact scenario registry allowlist; finite |
| process/network side effects | separate exact P1-3 capabilities in isolated worktree/runtime | exactly `0` | no arbitrary shell/direct network; only scenario-defined broker actions |
| secret use | server-owned purpose-bound ref plus separate SecretUse attestation and P1-3 SECRET capability | exactly `0`; no secret authority | server-fixed profile/registry ref only; public/model cannot select; separate exact SECRET capability |
| provider/model/endpoint/secret choice | server owner only | none | server only; public cannot choose |
| repository | pinned owner-authorized isolated snapshot/worktree; canonical checkout direct mutation denied | sanitized stored projection only | fixed synthetic repository/version only |
| input | TaskContract-bound owner input | recorded admitted trace only | bounded scenario fields; no free-form prompt/task/URL/upload |
| limits/budget | finite profile and application budget | no execution budget consumed | finite per-run/session/application/global budget |
| failure | truthful attempt failure; no authority expansion | truthful Replay read error; never hidden Live | Live failure/budget exhaustion keeps Replay available |
| Git/deployment | no Agent commit/push/deploy authority | none | none |

Missing Replay never triggers Live. Public Live output is a private candidate until separate
sanitization/evidence/public-projection admission. This document does not claim Public Live release.

## 13. next implementation ownership and path contract

The next Human-authorized implementation Task may create a P1-5 root under:

```text
src/aiscc/providers/
```

Expected exact ownership categories:

| path direction | owner contract |
|---|---|
| `src/aiscc/providers/models.py` | statuses, attempts, operations, profile/tool/output DTOs |
| `src/aiscc/providers/ports.py` | provider adapter, provider/tool and SecretUse authority, execution repository ports |
| `src/aiscc/providers/profiles.py` | versioned server profile loading/validation |
| `src/aiscc/providers/authority.py` | provider/tool and SecretUse selector attestation issuer/verifier; no P1-3 issuer authority |
| `src/aiscc/providers/openai_responses.py` | concrete stateless `store=false` Responses custom-function protocol/status adapter |
| `src/aiscc/providers/tools.py` | versioned registry, schema validation and dispatcher |
| `src/aiscc/providers/service.py` | bounded AgentExecutionService loop |
| `src/aiscc/providers/events.py` | lifecycle/operation phase event construction, private protocol-state refs and consistency |
| `config/providers/` | non-secret provider profiles and tool registry versions |
| `src/aiscc/persistence/` + new Alembic revision | execution attempt/event/projection durability only |
| `src/aiscc/contracts/security.py`, `src/aiscc/security/policy.py`, `src/aiscc/security/capability.py` | narrow P1-5 typed selector/fingerprint integration while retaining P1-3 ALLOW/DENY ownership |
| `src/aiscc/workflow/` | narrow P1-4 validation of P1-5 start/submission refs only; no matrix/state change |
| `tests/unit/providers/`, `tests/integration/providers/`, `tests/runtime/providers/` | proof matrix below |

The implementation Task must issue an exact path allowlist before creating files. It may add the
OpenAI SDK only through reviewed manifest/lock changes; a fake/local transport remains mandatory for
acceptance. It must not create `src/aiscc/evidence/`, `src/aiscc/human/`, or `src/aiscc/memory/`.

## 14. next implementation proof matrix

### 14.1 RESOURCE_AUTHORITY

- missing P1-5 authority, unknown/revoked provider/model/tool and malformed selector -> DENY;
- public/Agent provider/model/tool/endpoint/secret selection -> DENY;
- wrong mode/scenario/profile/registry/version/principal/run/attempt -> DENY;
- operation or argument fingerprint mismatch -> DENY before side effect;
- stale WorkflowState/state_version, expired/revoked/use-exhausted capability -> DENY;
- prove P1-5 selector alone cannot mint P1-3 ALLOW/capability.

### 14.2 SECRET_MEDIATION

- absent SecretUse authority or unresolved `secret_ref` -> SECRET DENY;
- wrong secret class/purpose/ref/resource/adapter/dispatcher/destination/run/state/version/mode/
  profile/scenario/fingerprint/expiry/use/revocation -> DENY before resolution;
- prove PROVIDER and TOOL capabilities cannot substitute for a SECRET capability;
- prove all required capabilities validate before atomic consume and material resolution;
- synthetic canary proves raw material never appears in Agent input/output, workspace, argv, tool args,
  environment dump, provider protocol history, event/provenance, error, report or Replay;
- prove independent use count, expiry, terminal revoke and resolver lease closure for provider and tool
  flows.

### 14.3 OPERATION_PHASE_GRAPH

- exercise every legal section 9.1 edge and exact allowed outcome/source combination;
- deny every unlisted edge without side effect or projection repair;
- prove PREPARED denial and SECURITY_ADMITTED pre-dispatch cancellation are terminal and append-only;
- crash/restart at PREPARED, SECURITY_ADMITTED and DISPATCH_STARTED and prove the exact recovery rule;
- verify each matrix row's side-effect fact, retry, capability consume/revoke, budget and
  reconciliation semantics;
- prove `RETRY_EXHAUSTED` exists only as an attempt-level failure ref over truthful operation outcomes.

### 14.4 RESPONSES_STATE_MODE

With fake/local adapter fixtures only, prove exact `background=false`, `stream=false`, `store=false`,
`parallel_tool_calls=false`, `truncation=disabled`, omitted Conversation/`previous_response_id`, and no
provider retrieval/polling. Prove bounded ordered replay of every required output item, exact
`function_call_output`/`call_id` binding, opaque encrypted reasoning and assistant-phase preservation,
private classification/hash, and missing/corrupt/over-bound continuation fail-closed. Exercise exact
mapping for `queued`, `in_progress`, `completed` final, `completed` function call, `failed`, `cancelled`
and `incomplete`, plus local timeout/unknown status. No fixture may enable a hosted provider tool.

### 14.5 REPLAY_ZERO_EXECUTION

In `PUBLIC_RECORDED_REPLAY`, instrument provider adapter, ToolRegistry dispatcher, process and network
brokers and prove invocation counts remain exactly `0`, including missing/corrupt Replay.

### 14.6 PROVIDER_ADAPTER_CONTRACT

With deterministic fake/local transport only, prove bounded serialization, profile-owned model,
strict custom-function definitions, structured final output, local-history `call_id` continuation,
hosted-tool rejection, output/error sanitization and no secret exposure.

### 14.7 TOOL_BROKER

- unknown/version-mismatched tool and schema-invalid/extra args -> DENY before side effect;
- exact tool -> product dispatcher only after TOOL capability consumption;
- TOOL authorization cannot bypass PROCESS/FILESYSTEM/NETWORK/SECRET admission;
- canonical argument fingerprint mismatch -> DENY;
- timeout/cancel/retry matrix for all three side-effect classifications;
- arbitrary shell, executable, path, URL and destination injection -> DENY.

### 14.8 EXECUTION_STATUS_EVENTS

- exact four-status set and lifecycle; illegal transitions denied;
- duplicate same event idempotent; different-fingerprint duplicate conflict;
- concurrent create/start/complete/fail admits one projection update;
- status/event admission does not change `WorkRun.state_version`;
- `EXECUTOR_COMPLETED` does not create `ACCEPTED` or admitted evidence;
- new same-WorkRun attempt requires admitted rework/READY lineage;
- PostgreSQL restart reconstructs projection; event/projection conflict fails closed without repair.

### 14.9 AMBIGUOUS_PROVIDER_FAILURE

Admit an operation, simulate timeout after ambiguous send, and prove: durable unknown outcome, no
blind retry, conservative budget handling, `EXECUTION_FAILED`, no WorkflowState mutation, and no
provider/tool continuation. Separately prove definitely-not-sent bounded retry.

### 14.10 BOUNDED_LOOP

Independently exhaust provider calls, rounds, tool calls, retries, time, output and budget; prove one
exact failure event and no hidden continuation. Change WorkflowState/version mid-loop and prove old
capability denial and attempt failure. Prove fresh capability continuation only under the identical
RUNNING/version contract.

### 14.11 PERSISTENCE_AND_HANDOFF

- every operation phase edge is durable and known/unknown outcome is additive;
- operation/event/projection ordering and hashes survive restart;
- private Responses protocol-state refs/hashes/order/call IDs survive restart while bodies remain
  private;
- raw secrets and unsanitized errors are absent from durable/public events;
- `ExecutionSubmissionRef` is produced only on completion;
- P1-4 validates submission without accepting caller booleans;
- P1-6 fake boundary sees producer refs only and no evidence is auto-admitted.

### 14.12 MODE_SECURITY_AND_FINAL_RESIDUE

Execute the complete owner/replay/public matrix with fake/local provider fixtures and actual applicable
P1-3 broker evidence. Prove fixed public repository/scenario/profile/tool set, no canonical checkout
mutation, no public free-form input, Replay availability under Live/provider/budget failure, and zero
Task-owned Docker/network/process/workspace residue.

No real provider call is required. Runtime proof cannot be replaced by unit/static evidence.

## 15. deferred configuration and Human boundary

Semantically unresolved questions: none for the implementation boundary frozen here.

Deliberately deferred, and not evidence of a design gap:

- exact live model/account/project/endpoint, API key, billing, price and provider hard-spend limit;
- exact numeric call/token/time/budget values;
- production secret manager and release deployment;
- P1-6 evidence admission, P1-7 Human/Judgment, P1-8 Cycle/NextAction;
- current release capability verification and public enablement.

Provider-neutral core and OpenAI Responses custom-function adapter protocol become canonical only if
Human accepts this document. Exact commercial configuration remains P3-3 release-time evidence.

```text
design result: ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING
P1-5 runtime implementation: NOT_STARTED
provider configured: NO
real provider call: NOT_EXECUTED
public Live: NOT_RELEASED
```
