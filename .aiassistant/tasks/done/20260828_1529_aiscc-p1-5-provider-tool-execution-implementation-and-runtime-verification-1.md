# 작업지시서: P1-5 Provider / Tool Execution Implementation + Runtime Verification

## meta

- task_id: `20260828_1529_aiscc-p1-5-provider-tool-execution-implementation-and-runtime-verification-1`
- created_at: `2026-08-28 15:29 KST`
- phase: `P1-5 — Agent Provider and Tool Execution`
- work_type: `IMPLEMENTATION_AND_RUNTIME_VERIFICATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `provider/tool authority + execution attempts/operations/events + bounded adapter loop`
- predecessor_design_task: `20260828_1417_aiscc-p1-5-secret-operation-protocol-and-openai-state-mode-design-rework-1`
- predecessor_result: `HUMAN_PROVIDED / ACCEPTED / CLOSED`
- predecessor_HEAD: `d96949f3643e6a0610942e33d70e9da259e1e432`
- accepted_design_path: `.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md`
- accepted_design_sha256: `12070677aa1cfa74b7eea9a52db24f78aacd2bf23d655f125a7689797d172443`
- P1_4_status: `ACCEPTED / CLOSED`
- P1_5_runtime_status_before: `READY / NOT_STARTED`
- P1_6_status: `NOT_STARTED`

---

# 0. sole execution contract

Implement the Human-accepted P1-5 design exactly.

This Task first Git-persists the accepted design + terminal canonical state.
After that one commit, all P1-5 implementation source remains uncommitted for Human review.

No P1-6/P1-7/P1-8 implementation.

No real provider call, real API key, billing configuration or public deployment.

---

# Stage 0 — exact P1-5 design terminal commit

## expected repository

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

HEAD:
d96949f3643e6a0610942e33d70e9da259e1e432
```

If HEAD differs:

```text
STOP
→ BLOCKED_PREDECESSOR_HEAD_DRIFT
```

## accepted design identity

Verify exact repository candidate:

```text
.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md

SHA-256:
12070677aa1cfa74b7eea9a52db24f78aacd2bf23d655f125a7689797d172443
```

Mismatch:

```text
STOP
→ BLOCKED_P1_5_ACCEPTED_DESIGN_DRIFT
```

Do not reconstruct or edit accepted design before Stage 0 commit.

## terminal canonical files

Human placement must provide exact bytes:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
sha256:
11706bbcbe7ea4cefb86a5b75c074783427f5e03f4c45ed61e36284a635c405a

.aiassistant/records/aiscc/DECISION_REGISTER.md
sha256:
c8dcf43f90be9522249e12c943208609fa69ea2b054876a6efae1168b5c51772

.aiassistant/records/aiscc/NEXT_ACTIONS.md
sha256:
6e0771e6b7ebab89648d50b8e880a625d7af09ad536c4d0864bf41951d0f5a26

.aiassistant/records/aiscc/cycles/20260828_1529_aiscc-p1-5-provider-tool-execution-design-final-acceptance-1.cycle.md
sha256:
09f086ba984e4946da9b58b0f5372bae72402a243b205cb83993d6f4f4717cf0

```

Verify SHA-256 before staging.

Mismatch:

```text
STOP
→ BLOCKED_P1_5_DESIGN_TERMINAL_CANONICAL_MISMATCH
```

## exact Stage 0 commit universe

Only these six paths are allowed:

```text
.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md

.aiassistant/tasks/done/20260828_1417_aiscc-p1-5-secret-operation-protocol-and-openai-state-mode-design-rework-1.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/records/aiscc/cycles/20260828_1529_aiscc-p1-5-provider-tool-execution-design-final-acceptance-1.cycle.md
```

Active Task and target report are never staged.

Before staging:

```text
git status --short
git diff --check
```

Stage explicit actual changed paths only.

Exactly one local commit is authorized.

Exact commit message:

```text
feat: accept P1-5 provider tool execution design

Persist the Human-accepted P1-5 provider/tool execution contract,
including secret mediation, operation protocol, bounded execution, and
stateless Responses continuation semantics.

Open the P1-5 runtime implementation gate from the canonical design.
```

Use LF-safe UTF-8 message file + `git commit -F`.

After commit:

```text
P1_5_IMPLEMENTATION_BASE_COMMIT=<full new hash>
```

Verify:

- parent == `d96949f3643e6a0610942e33d70e9da259e1e432`;
- every committed path is inside the exact six-path universe;
- committed `AISCC_PROVIDER_TOOL_EXECUTION.md` SHA remains `12070677aa1cfa74b7eea9a52db24f78aacd2bf23d655f125a7689797d172443`;
- exact multiline commit message;
- tracked worktree clean;
- index empty;
- no remote mutation.

After Stage 0:

```text
git add / commit / push
→ FORBIDDEN
```

---

# Stage 1 — canonical / current-provider-protocol preflight

Read canonical:

```text
.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_SECURITY_SANDBOX.md
.aiassistant/rules/AISCC_RUNTIME_SUBSTRATE.md
.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

Verify current official OpenAI Python/Responses protocol before adding the SDK, using official OpenAI
documentation/package metadata only.

Required compatibility observations:

```text
official Python package:
openai

Responses create API:
available

request controls needed by accepted V1:
store=false
background=false
stream=false
parallel_tool_calls=false
truncation=disabled

custom function tools:
available

previous_response_id/conversation:
available but V1 adapter MUST omit them as accepted

Response status surface:
must support the accepted mapping for
queued / in_progress / completed / failed / cancelled / incomplete
```

If current official API materially contradicts the accepted design:

```text
STOP
→ PROVIDER_PROTOCOL_CONFLICT
```

No live provider call.

---

# Stage 2 — exact implementation candidate universe

P1-5 implementation may create/modify only this exact maximum 50-path universe:

- `pyproject.toml`
- `uv.lock`
- `config/providers/provider-profiles.v1.toml`
- `config/providers/tool-registry.v1.toml`
- `config/security/permission-profiles.v1.toml`
- `config/security/resource-policy.v1.toml`
- `src/aiscc/providers/__init__.py`
- `src/aiscc/providers/models.py`
- `src/aiscc/providers/ports.py`
- `src/aiscc/providers/profiles.py`
- `src/aiscc/providers/authority.py`
- `src/aiscc/providers/openai_responses.py`
- `src/aiscc/providers/tools.py`
- `src/aiscc/providers/service.py`
- `src/aiscc/providers/events.py`
- `src/aiscc/contracts/security.py`
- `src/aiscc/security/models.py`
- `src/aiscc/security/policy.py`
- `src/aiscc/security/capability.py`
- `src/aiscc/persistence/__init__.py`
- `src/aiscc/persistence/database.py`
- `src/aiscc/persistence/models.py`
- `src/aiscc/persistence/repository.py`
- `src/aiscc/workflow/__init__.py`
- `src/aiscc/workflow/models.py`
- `src/aiscc/workflow/guards.py`
- `migrations/versions/20260828_0002_p1_5_provider_tool_execution.py`
- `tests/conftest.py`
- `tests/unit/providers/test_models.py`
- `tests/unit/providers/test_authority.py`
- `tests/unit/providers/test_operation_protocol.py`
- `tests/unit/providers/test_openai_responses.py`
- `tests/unit/providers/test_tools.py`
- `tests/unit/providers/test_service.py`
- `tests/integration/providers/test_execution_persistence.py`
- `tests/integration/providers/test_security_resource_authority.py`
- `tests/integration/providers/test_secret_mediation.py`
- `tests/integration/providers/test_workflow_handoff.py`
- `tests/runtime/providers/test_replay_zero_execution.py`
- `tests/runtime/providers/test_mode_security.py`
- `tests/runtime/providers/test_ambiguous_provider_failure.py`
- `tests/runtime/providers/test_secret_non_exposure.py`
- `tests/runtime/providers/test_final_residue.py`
- `tests/fixtures/providers/fake_responses_server.py`
- `tests/fixtures/providers/recorded_replay.json`
- `tests/unit/security/test_permission_policy.py`
- `tests/unit/security/test_capability_lifetime.py`
- `tests/unit/workflow/test_state_machine.py`
- `tests/integration/security/test_broker_fail_closed.py`
- `tests/integration/workflow/test_postgres_kernel.py`

Not every path must change.

Any required 51st path:

```text
STOP
→ EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

Do not create:

```text
src/aiscc/evidence/
src/aiscc/human/
src/aiscc/memory/
```

Do not modify API/public deployment/UI.

---

# Stage 3 — dependency authority

Permitted direct dependency additions only:

```text
openai
jsonschema
```

Use current stable versions compatible with Python 3.12 at execution time and lock exact resolved
versions in `uv.lock`.

Report exact resolved versions.

Do not add agent frameworks, LangGraph, provider-hosted tool frameworks, secret-manager SDKs or
database libraries beyond already accepted substrate.

If `jsonschema` is not required because strict validation is implemented using an already accepted
dependency without reducing semantics, it may be omitted.

The OpenAI package is used only against a deterministic local fake Responses endpoint during
acceptance verification.

---

# Stage 4 — exact domain / authority implementation

Implement under:

```text
src/aiscc/providers/
```

At minimum implement exact equivalents of:

```text
ExecutionStatus
ExecutionAttempt
ExecutionAttemptRef
ExecutionSubmissionRef

ExecutionOperation
ExecutionOperationPhase
ExecutionOperationOutcome
ExecutionAttemptFailureClass

ProviderProfile
ProviderCanonicalIdentity
ProviderToolSelectorRequest
ProviderToolSelectorAttestation

SecretUseSelectorRequest
SecretUseSelectorAttestation

ToolDefinition
ToolRegistry
ToolCallCandidate

AgentOutputRef
ToolOutputRef
ExecutionArtifactRef

ProviderCall
ProviderResult
```

No public/caller boolean may become authority.

All identifiers/fingerprints are immutable and validated.

Operation/argument fingerprint canonicalization MUST implement the accepted canonical-JSON + lowercase
SHA-256 contract and reject invalid/unrepresentable inputs fail-closed.

---

# Stage 5 — P1-3 PROVIDER / TOOL / SECRET extension

Implement a typed injected policy boundary while preserving P1-3 ownership.

Required:

```text
P1-5 authority
→ selector/attestation only

P1-3 SecurityPolicy
→ sole ALLOW/DENY
→ sole ResourceGrant issuer
→ sole Capability issuer
→ sole capability consume/revoke/use-count owner
```

For `ResourceDomain.PROVIDER` / `TOOL`:

```text
absent P1-5 authority
→ DENY

invalid/expired/revoked/wrong selector
→ DENY

valid owner-bound selector
→ continue every existing P1-3 guard
→ P1-3 may issue exact grant/capability
```

For `ResourceDomain.SECRET`:

```text
absent SecretUse authority
→ DENY

secret_ref alone
→ DENY

PROVIDER/TOOL capability alone
→ DENY SECRET use
```

Implement exact SECRET selector binding from the accepted design.

## atomic multi-capability broker consumption

Provider or Tool dispatch may require multiple capabilities.

Implement a P1-3-owned or P1-3-mediated exact validate-all-then-consume boundary so:

```text
all required capabilities validate first
→ only then consume all exact uses

one validation fails
→ zero uses consumed
→ no secret resolution
→ no side effect
```

After successful consume, resolver/transport failure does not restore a use.

This boundary must be race-safe inside the process authority model used by P1-3.

---

# Stage 6 — non-secret versioned config

Create:

```text
config/providers/provider-profiles.v1.toml
config/providers/tool-registry.v1.toml
```

These are implementation/test-safe profiles, not public release configuration.

Required:

- no credential material;
- no production billing claim;
- no public-release claim;
- at least one deterministic fake/local OpenAI Responses profile;
- finite bounds for provider calls/rounds/tool calls/retry/time/output/budget;
- fixed synthetic scenario binding;
- server-owned opaque `secret_ref` only;
- tool registry contains only safe deterministic fixture tools needed for proof;
- arbitrary shell/network destination is absent.

If P1-3 non-secret resource policy metadata changes, update only the two authorized
`config/security/**` files and preserve default deny.

Do not configure a real OpenAI account/model/API key.

---

# Stage 7 — PostgreSQL execution persistence

Add one Alembic revision:

```text
migrations/versions/20260828_0002_p1_5_provider_tool_execution.py
```

Minimum durable authority:

```text
execution_attempt projection
execution event history
execution operation projection
operation phase/outcome history
private provider protocol-state item/reference history
immutable output/artifact/submission refs
```

Required semantics:

### attempt projection

At minimum:

```text
execution_attempt_id
work_run_id
attempt ordinal
parent attempt ref
task contract id/version
RuntimeMode
provider profile id/version
tool registry id/version
creation state/version
current causal state/version
ExecutionStatus
execution_version
latest event sequence
counters
timestamps
```

### operation projection

At minimum:

```text
operation_id
execution_attempt_id
operation kind
operation fingerprint
current phase
known/unknown outcome
provider/tool resource identity
call ordinal / parent operation
latest operation event sequence
timestamps
```

### append-only event history

Persist exact legal:

```text
attempt lifecycle events
operation phase edges
known/unknown outcomes
resource/admission/capability refs
private protocol-state refs/hashes
output refs/hashes
usage/retry/cancel/failure classification
```

Use database constraints/triggers to prevent update/delete of append-only event/history rows.

Lifecycle event + attempt projection CAS:

```text
one transaction
```

Operation edge + operation projection CAS:

```text
one transaction
```

Pure execution events MUST NOT update P1-4 `work_runs.state_version`.

Fresh mutation must reconstruct/verify execution projection and required private protocol-state
integrity before continuation/side effect.

Mismatch:

```text
→ fail closed
→ no auto repair
```

---

# Stage 8 — P1-4 execution-ref handoff

P1-5 cannot mint P1-4 guards.

Implement issuer-backed typed P1-5 references so P1-4 System authority can validate before issuing:

```text
G_EXECUTION_STARTED
G_EXECUTOR_SUBMISSION
```

If required, extend the existing P1-4 request/guard binding narrowly inside the authorized
`src/aiscc/workflow/**` and persistence/migration paths.

Required:

```text
raw string ref
→ no authority

P1-5 issuer-backed ref
+ exact task/run/attempt/state/version/status binding
→ P1-4 may validate

P1-5
→ cannot issue TrustedGuardFact for P1-4
```

Do not change:

```text
exact 9 WorkflowState values
exact 22 transition pairs
Judgment mapping
P1-6/P1-7 owner separation
```

Re-run all P1-4 tests.

---

# Stage 9 — OpenAI Responses V1 adapter

Implement a concrete provider-neutral port plus OpenAI adapter.

Use the official Python `openai` SDK.

Acceptance transport:

```text
local deterministic fake Responses HTTP endpoint only
```

No api.openai.com call.

Exact request invariants:

```text
background=false
stream=false
store=false
parallel_tool_calls=false
truncation=disabled

conversation omitted
previous_response_id omitted

model
→ only from server-owned ProviderProfile

custom function tools
→ only from exact ToolRegistry
→ strict schema

provider-hosted execution tools
→ never exposed
```

Continuation source:

```text
AISCC durable private protocol history only
```

Persist/replay exact required prior output items, function-call items, exact `call_id`,
`function_call_output`, assistant phase and opaque encrypted reasoning protocol material when present.

Missing/corrupt/order-invalid/over-bound continuation:

```text
DENY / fail closed
```

No fallback to provider-held Conversation/response retrieval.

Exact Response status mapping follows accepted design for:

```text
queued
in_progress
completed
failed
cancelled
incomplete
```

No polling/retrieval network continuation in accepted V1 unless current accepted design explicitly
contains it. `queued/in_progress` must become truthful unknown/reconciliation-required outcomes.

Local timeout after `DISPATCH_STARTED`:

```text
TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME
→ no blind provider retry
```

---

# Stage 10 — ToolRegistry / broker

Implement strict versioned registry loading.

Required dispatch order:

```text
model-proposed tool name/args
→ untrusted ToolCallCandidate
→ exact registry/version lookup
→ strict schema validation
→ reject extra/unknown args
→ canonical argument fingerprint
→ TOOL selector attestation
→ P1-3 TOOL grant/admission/capability
→ all underlying resource admissions
→ atomic capability consumption
→ registered dispatcher
→ bounded result
```

Underlying resources are independently authorized:

```text
PROCESS
FILESYSTEM
NETWORK
SECRET
```

A TOOL capability does not substitute.

No arbitrary:

```text
shell
executable
path
URL
network destination
secret ref
provider/model
```

from model arguments.

---

# Stage 11 — bounded AgentExecutionService

Implement the accepted deterministic loop.

Normal side effects require exact authoritative:

```text
WorkflowState=RUNNING
```

Before every provider/tool side effect:

- reload/check current WorkRun;
- enforce exact state/version;
- enforce current execution attempt/status/version;
- obtain fresh exact selector + P1-3 security capability;
- re-check all profile/scenario limits.

Enforce finite profile-owned maxima independently:

```text
provider calls
agent rounds
tool calls
provider retry
wall time
output/token size
budget
```

Limit exhaustion produces one truthful failure classification/event and closes new side effects.

A WorkflowState/state_version change mid-loop invalidates prior capabilities.
No silent continuation.

A fresh capability may continue only when the accepted design's identical RUNNING/current-version
conditions are met.

---

# Stage 12 — exact operation lifecycle

Implement every accepted legal edge.

Mandatory pre-dispatch behavior:

```text
PREPARED
→ OUTCOME_KNOWN(DENIED_BEFORE_SIDE_EFFECT)

PREPARED
→ SECURITY_ADMITTED

SECURITY_ADMITTED
→ OUTCOME_KNOWN(CANCELLED)

SECURITY_ADMITTED
→ DISPATCH_STARTED
```

After `DISPATCH_STARTED`, known or unknown terminal outcome only according to the accepted matrix.

Unlisted edge:

```text
DENY
→ no side effect
→ no projection repair
```

`RETRY_EXHAUSTED` remains attempt-level only.

Crash/restart at each nonterminal phase must follow the accepted recovery semantics.

---

# Stage 13 — secret mediation / canary

Use a synthetic secret value only for verification.

Required flow:

```text
opaque fake secret_ref
→ P1-5 SecretUse attestation
→ P1-3 SECRET capability
→ private fake resolver
→ adapter/dispatcher local call
→ lease close/revoke
```

Prove synthetic raw secret never appears in:

```text
Agent input/output
workspace
argv
tool args
environment dump
provider durable protocol history
execution event/provenance
exception/error
report/export
recorded Replay
```

Scanning/redaction is proof defense-in-depth only; it does not replace capability mediation.

---

# Stage 14 — Replay zero-execution

In `PUBLIC_RECORDED_REPLAY` instrument:

```text
provider adapter
ToolRegistry dispatcher
process broker
network broker
secret resolver
```

Required invocation counts:

```text
0
0
0
0
0
```

Also prove:

```text
missing/corrupt Replay
→ error
→ no fallback Live
→ still zero invocation
```

---

# Stage 15 — mandatory tests / proof

## static/build

Run:

```text
uv sync --frozen --all-groups
uv build
uv run ruff check .
uv run ruff format --check .
uv run mypy --strict src tests
```

After dependency addition, first update lock through the explicit permitted dependency operation;
then final verification must use `--frozen`.

## full regression

Run:

```text
uv run pytest -q tests/unit tests/integration
```

No skip/xfail.

All existing P1-3/P1-4 tests must remain passing.

## isolated PostgreSQL

Use local Docker PostgreSQL.

Apply full Alembic head.

Record exact:

```text
PostgreSQL version/image
Alembic head
```

## required P1-5 proof classes

### RESOURCE_AUTHORITY

- absent P1-5 authority → PROVIDER/TOOL DENY;
- unknown/revoked/wrong profile/model/tool/mode/scenario/principal/run/attempt → DENY;
- operation/argument fingerprint mismatch → DENY;
- P1-5 selector cannot mint P1-3 ALLOW/capability.

### SECRET_MEDIATION

- absent/wrong secret authority → DENY before resolution;
- PROVIDER/TOOL capability cannot substitute for SECRET;
- validate-all-then-consume atomicity;
- synthetic secret non-exposure;
- use count/expiry/revoke/lease closure.

### OPERATION_PHASE_GRAPH

- every legal edge;
- every unlisted edge denied;
- pre-security deny terminal;
- pre-dispatch cancel terminal;
- crash/restart at PREPARED / SECURITY_ADMITTED / DISPATCH_STARTED;
- exact known/unknown outcome semantics;
- `RETRY_EXHAUSTED` attempt-level only.

### RESPONSES_STATE_MODE

With official OpenAI SDK against local fake endpoint:

- exact V1 request flags;
- omitted Conversation/previous_response_id;
- local durable continuation replay;
- exact call_id binding;
- encrypted reasoning opaque replay;
- missing/corrupt/over-bound continuation fail-closed;
- all six statuses mapped;
- hosted tools absent.

### REPLAY_ZERO_EXECUTION

All five invocation counters remain `0`, including Replay failure.

### PROVIDER_ADAPTER_CONTRACT

- server-owned model/profile only;
- strict function definitions;
- bounded serialization/output;
- final output vs custom-function path;
- sanitization;
- no secret leakage.

### TOOL_BROKER

- unknown/version mismatch/schema-invalid/extra args → DENY;
- exact tool dispatch only;
- TOOL does not bypass underlying capability;
- argument fingerprint binding;
- timeout/cancel/retry by side-effect class;
- shell/path/URL/destination injection denied.

### EXECUTION_STATUS_EVENTS

- exact four statuses;
- exact legal lifecycle;
- illegal transitions denied;
- duplicate same event idempotent;
- conflicting duplicate rejected;
- concurrent create/start/complete/fail one projection mutation;
- `work_runs.state_version` unchanged by pure execution event;
- `EXECUTOR_COMPLETED != ACCEPTED`;
- restart reconstruction;
- projection/event mismatch fail-closed.

### AMBIGUOUS_PROVIDER_FAILURE

- durable PREPARED;
- admitted security;
- DISPATCH_STARTED;
- simulated local transport timeout after ambiguous send;
- OUTCOME_UNKNOWN durable;
- no blind retry;
- conservative budget semantics;
- execution attempt fails truthfully;
- no WorkflowState mutation.

Also prove definitely-not-sent bounded retry separately.

### BOUNDED_LOOP

Exhaust each independent bound:
provider calls / rounds / tools / retries / time / output / budget.

Each:
one exact failure event, no hidden continuation.

Mutate P1-4 state/version mid-loop:
old capability denial + attempt failure.

### PERSISTENCE_AND_HANDOFF

- lifecycle/operation ordering survives restart;
- private protocol refs/hashes/order/call IDs survive restart;
- output/submission refs immutable;
- P1-4 validates issuer-backed start/submission refs;
- raw strings cannot satisfy P1-4;
- P1-6 fake boundary sees producer refs only;
- no evidence auto-admitted.

### MODE_SECURITY_AND_FINAL_RESIDUE

Execute owner/replay/public-bounded-live matrix with fake/local provider only.

Prove public fixed synthetic repo/scenario/profile/tool set and no public free-form/provider/model/secret
selection.

Final Task-owned residue:

```text
Docker containers:
0

Docker networks:
0

background fake provider processes:
0

temporary workspaces:
0
```

---

# Stage 16 — dependency/provider safety

Forbidden:

- real OpenAI/provider network call;
- real API key read/create/use;
- provider billing/spend configuration;
- external arbitrary URL;
- provider-hosted execution tools;
- shell or network tool driven from model arguments;
- LangGraph core;
- Git commit/push after Stage 0;
- public deployment.

Use synthetic/local credentials only.

---

# Stage 17 — result / report

If all executor proof passes:

```text
ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING
```

Executor MUST NOT claim:

```text
P1-5 ACCEPTED / CLOSED
```

Human owns final acceptance.

Stop with exact blocker if:

```text
accepted design cannot be implemented without P1-3 weakening
→ POLICY_CONFLICT_INVESTIGATION_REQUIRED

official current Responses protocol contradicts accepted V1
→ PROVIDER_PROTOCOL_CONFLICT

51st candidate path required
→ EVIDENCE_SCOPE_EXPANSION_REQUIRED

real provider call becomes necessary for claimed proof
→ EXTERNAL_EVIDENCE_SCOPE_REQUIRED
```

---

# report required fields

- Task ID/path;
- predecessor HEAD;
- design terminal commit/full `P1_5_IMPLEMENTATION_BASE_COMMIT`;
- accepted design SHA verification;
- exact implementation candidate path set/count/aggregate;
- exact dependency additions + locked versions;
- exact changed P1-3/P1-4 integration paths and reason;
- exact ProviderProfile/ToolRegistry config identity;
- exact P1-5 selector/SecretUse authority behavior;
- atomic multi-capability consume behavior;
- execution schema/Alembic head;
- execution status lifecycle;
- operation phase graph;
- Responses request flags/state/status mapping;
- fake/local transport design;
- Replay zero-execution counters;
- resource/secret/tool proof;
- concurrency/idempotency/restart/consistency proof;
- ambiguous outcome proof;
- bounded-loop proof;
- P1-4 handoff proof;
- P1-6 non-substitution proof;
- static/build/full test counts;
- PostgreSQL/Docker versions;
- final residue;
- real provider calls: `0`;
- Human pending;
- forbidden-not-run;
- rollback;
- preserved paths;
- next recommendation.

---

# export bundle

Target:

```text
.aiassistant/reports/target/20260828_1529_aiscc-p1-5-provider-tool-execution-implementation-and-runtime-verification-1/
```

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- every actual P1-5 implementation candidate file preserving relative path
- compact non-secret static/PostgreSQL/runtime evidence

Do not export:

- `.venv`
- DB volume
- raw secret
- real provider credential
- Docker layer
- cache
- unrelated repository files

---

# Task lifecycle

```text
.aiassistant/tasks/active/20260828_1529_aiscc-p1-5-provider-tool-execution-implementation-and-runtime-verification-1.md
→
.aiassistant/tasks/done/20260828_1529_aiscc-p1-5-provider-tool-execution-implementation-and-runtime-verification-1.md
```

`done` means submitted, not Human accepted.

---

# preserved artifacts

Always preserve:

- Stage 0 `P1_5_IMPLEMENTATION_BASE_COMMIT`;
- `.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md`;
- `.aiassistant/tasks/done/20260828_1417_aiscc-p1-5-secret-operation-protocol-and-openai-state-mode-design-rework-1.md`;
- `.aiassistant/records/aiscc/cycles/20260828_1529_aiscc-p1-5-provider-tool-execution-design-final-acceptance-1.cycle.md`;
- all actual P1-5 implementation candidate paths until Human judgment;
- `.aiassistant/tasks/done/20260828_1529_aiscc-p1-5-provider-tool-execution-implementation-and-runtime-verification-1.md` after submission.

---

# next action after Human accepts P1-5 runtime

```text
P1-6 Evidence Admission
```

Do not implement P1-6 in this Task.
