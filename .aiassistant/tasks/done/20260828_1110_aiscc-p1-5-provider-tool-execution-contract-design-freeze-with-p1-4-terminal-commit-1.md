# 작업지시서: P1-5 Provider / Tool Execution Contract Design Freeze with P1-4 Terminal Commit

## meta

- task_id: `20260828_1110_aiscc-p1-5-provider-tool-execution-contract-design-freeze-with-p1-4-terminal-commit-1`
- created_at: `2026-08-28 11:10 KST`
- phase: `P1-5 — Agent Provider and Tool Execution`
- work_type: `DESIGN_BASELINE`
- evidence_profile: `HIGH_RISK_DESIGN`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `provider/tool execution authority + execution event/status contract`
- predecessor_phase: `P1-4 Explicit State Machine Kernel Implementation`
- predecessor_result: `HUMAN_PROVIDED / ACCEPTED / CLOSED`
- predecessor_HEAD: `aec4d24ba3ae23d8252c9582130aea99aac333a1`
- P1_4_final_candidate_count: `19`
- P1_4_final_candidate_aggregate_sha256: `1316fd14faf6a2ad85f43ae9e9a2bab45c1736e4f28bea40d35865f53dee4cb5`
- P1_5_status_before: `READY / DESIGN_FREEZE_REQUIRED`
- P1_6_status: `NOT_STARTED`

---

# 0. sole execution contract

This Task first persists the Human-accepted P1-4 terminal implementation and canonical state.

After that one commit, the same Executor turn performs **P1-5 design only**.

Do not implement provider/tool runtime source in this Task.

The design output is a Human-review candidate, not an accepted baseline.

---

# Stage 0 — exact P1-4 terminal implementation/provenance commit

## expected repository

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

HEAD:
aec4d24ba3ae23d8252c9582130aea99aac333a1
```

If HEAD differs:

```text
STOP
→ BLOCKED_PREDECESSOR_HEAD_DRIFT
```

## exact accepted P1-4 candidate

Before any Git index mutation verify:

```text
candidate count:
19

aggregate SHA-256:
1316fd14faf6a2ad85f43ae9e9a2bab45c1736e4f28bea40d35865f53dee4cb5
```

Exact 19 paths:

- `alembic.ini`
- `migrations/env.py`
- `migrations/script.py.mako`
- `migrations/versions/20260828_0001_p1_4_workflow_kernel.py`
- `pyproject.toml`
- `src/aiscc/persistence/__init__.py`
- `src/aiscc/persistence/database.py`
- `src/aiscc/persistence/models.py`
- `src/aiscc/persistence/repository.py`
- `src/aiscc/workflow/__init__.py`
- `src/aiscc/workflow/evaluator.py`
- `src/aiscc/workflow/guards.py`
- `src/aiscc/workflow/kernel.py`
- `src/aiscc/workflow/matrix.py`
- `src/aiscc/workflow/models.py`
- `src/aiscc/workflow/ports.py`
- `tests/integration/workflow/test_postgres_kernel.py`
- `tests/unit/workflow/test_state_machine.py`
- `uv.lock`

Use the exact aggregate algorithm already used by P1-4.

Mismatch:

```text
STOP
→ BLOCKED_P1_4_ACCEPTED_CANDIDATE_DRIFT
```

Do not repair P1-4 source.

## exact canonical terminal files

The Human placement packet must directly provide these exact canonical files:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
sha256:
6341e09eda06555cdc8380ae78f04246449d94f90d754fdb8dd841ba2b0ac818

.aiassistant/records/aiscc/DECISION_REGISTER.md
sha256:
be8e524879dfc832837f3eddc6f5b9709ca83583b91ecfb8d31920b6bdde7879

.aiassistant/records/aiscc/NEXT_ACTIONS.md
sha256:
5754328f8cd985f8119a80fad153b7ab5c52d352793325099a37c78c30f8c072

.aiassistant/records/aiscc/cycles/20260828_1110_aiscc-p1-4-explicit-state-machine-kernel-final-acceptance-1.cycle.md
sha256:
aa0b69ba699aec1059ecd27b7751d22a83d6054378b0c116939ab76cfbb9c85e

```

Verify exact SHA-256 before staging.

Unexpected canonical bytes:

```text
STOP
→ BLOCKED_P1_4_TERMINAL_CANONICAL_MISMATCH
```

## exact Stage 0 commit universe

The terminal commit may contain only:

```text
19 exact accepted P1-4 candidate paths

.aiassistant/tasks/done/20260828_1110_aiscc-p1-4-denied-precreation-retry-consistency-semantics-rework-1.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/records/aiscc/cycles/20260828_1110_aiscc-p1-4-explicit-state-machine-kernel-final-acceptance-1.cycle.md
```

Expected maximum universe:

```text
24 paths
```

Already-clean allowed members are not blockers.
Every actual staged path must belong to this universe.

The active P1-5 Task and target report MUST NOT be staged.

## pre-commit

Run:

```text
git status --short
git diff --check
```

Recompute the accepted 19-path aggregate immediately before staging.

Required:

```text
1316fd14faf6a2ad85f43ae9e9a2bab45c1736e4f28bea40d35865f53dee4cb5
```

## one authorized local commit

Forbidden:

```text
git add .
git add -A
git commit -a
git amend
git reset
git rebase
git stash
git clean
git fetch
git pull
git push
branch/tag/remote mutation
```

Stage explicit actual changed paths only.

Exact commit message:

```text
feat: accept P1-4 explicit state machine kernel

Persist the Human-accepted P1-4 PostgreSQL state-machine implementation,
its final concurrency and consistency verification, and terminal
canonical project state.

Commit the exact accepted 19-path kernel candidate before P1-5 begins.
```

Use LF-safe UTF-8 message file and `git commit -F`.

After commit:

```text
P1_5_DESIGN_BASE_COMMIT=<full new hash>
```

Verify:

- parent == `aec4d24ba3ae23d8252c9582130aea99aac333a1`;
- all committed paths are within the exact 24-path universe;
- accepted P1-4 candidate aggregate at committed HEAD is exact;
- exact multiline message;
- tracked worktree clean;
- index empty;
- no remote operation.

After Stage 0:

```text
git add / commit / push
→ FORBIDDEN
```

The P1-5 design candidate remains uncommitted for review.

---

# Stage 1 — canonical read / authority preflight

Read:

1. `.aiassistant/rules/AISCC_ARCHITECTURE.md`
2. `.aiassistant/rules/AISCC_ORCHESTRATION.md`
3. `.aiassistant/rules/AISCC_SECURITY_SANDBOX.md`
4. `.aiassistant/rules/AISCC_RUNTIME_SUBSTRATE.md`
5. `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
6. `.aiassistant/records/aiscc/DECISION_REGISTER.md`
7. `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
8. `.aiassistant/records/aiscc/cycles/20260828_1110_aiscc-p1-4-explicit-state-machine-kernel-final-acceptance-1.cycle.md`

Inspect relevant implementation boundaries only:

```text
src/aiscc/contracts/workflow.py
src/aiscc/contracts/security.py
src/aiscc/security/**
src/aiscc/runtime/**
src/aiscc/workflow/**
src/aiscc/persistence/**
pyproject.toml
uv.lock
```

Do not modify product source.

---

# Stage 2 — design deliverable

Create exactly one canonical design candidate:

```text
.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md
```

No other new canonical rule.

The document must be implementation-ready and exact enough that the next P1-5 implementation Task
does not invent load-bearing authority semantics.

---

# Stage 3 — canonical ExecutionStatus contract

Freeze the P1-1 exact status set without adding values:

```text
NOT_STARTED
RUNNING
EXECUTOR_COMPLETED
EXECUTION_FAILED
```

Define exact ownership and durable semantics.

Required invariants:

```text
ExecutionStatus
!= WorkflowState

execution-status update
!= WorkflowState transition

execution-status update
→ MUST NOT increment WorkRun.state_version

EXECUTOR_COMPLETED
!= ACCEPTED

EXECUTION_FAILED
!= FAILED
```

Design the exact admitted execution-status lifecycle.

At minimum answer:

- which event admits `NOT_STARTED → RUNNING`;
- which event admits `RUNNING → EXECUTOR_COMPLETED`;
- which event admits `RUNNING → EXECUTION_FAILED`;
- whether any same-WorkRun retry from `EXECUTION_FAILED` is permitted;
- how provider-internal retries differ from `ExecutionStatus` retry;
- idempotency key for execution event admission;
- concurrent start/completion behavior;
- restart durability;
- append-only event vs mutable current projection;
- how execution status binds to authoritative `work_run_id` and current state/version without
  becoming a workflow transition.

The design must reconcile P1-1 semantics explicitly.

---

# Stage 4 — provider/tool resource authority handoff from P1-3

P1-3 intentionally fails closed for:

```text
ResourceDomain.PROVIDER
ResourceDomain.TOOL
```

until P1-5 owns exact policy.

Design the precise integration.

Required invariant:

```text
P1-5 selector/profile authority
!= SecurityAdmissionDecision
```

P1-3 `SecurityPolicy` remains the ALLOW/DENY owner.

P1-5 may define exact server-owned provider/tool resource selectors that P1-3 can consult when
deciding whether a ResourceScope is policy-owned.

The design must choose and justify an integration shape such as an injected typed policy port.

Required behavior when no P1-5 authority is installed:

```text
PROVIDER / TOOL
→ DENY
```

No global boolean or arbitrary caller-provided allowlist.

Freeze:

- provider resource canonical identity;
- tool resource canonical identity;
- profile/version identity;
- scenario binding;
- mode binding;
- run/principal binding where mutable;
- state/version freshness;
- expiry/revocation/use bounds where applicable;
- exact operation/input or argument fingerprint binding.

The provider/model/tool choice cannot come from public/Agent input.

---

# Stage 5 — provider profile contract

Define a versioned, server-owned, non-secret `ProviderProfile` or exact equivalent.

At minimum cover:

```text
profile_id
version
provider_id
model_ref
runtime modes
scenario allowlist
secret_ref
provider-call maximum
agent round-trip maximum
tool-call maximum
timeout
retry policy
output/token bound
budget policy ref
```

Exact numeric production values are NOT frozen in this design unless already accepted elsewhere.

The design freezes the **fields/authority**, not current commercial model/pricing.

Required:

```text
PUBLIC_RECORDED_REPLAY
→ provider disabled

PUBLIC_BOUNDED_LIVE
→ server-fixed provider/model/profile
→ public cannot choose provider/model/endpoint/secret

OWNER_SELF_DOGFOOD
→ explicit owner-authorized server profile
→ still bounded
```

Actual provider resource/account/API key/billing/spend-hard-limit/current model ID verification remains
future configuration/release evidence.

---

# Stage 6 — provider adapter contract

Freeze a provider-neutral core port and at least one concrete adapter direction consistent with the
accepted deployment direction.

The design must separate:

```text
AgentExecutionService
ProviderAdapter
ProviderProfile
ProviderCall
ProviderResult
AgentOutput
```

Required non-substitution:

```text
ProviderResult
!= AgentOutput admission into workflow truth

AgentOutput
!= EvidenceCandidate admission

AgentOutput
!= WorkflowState
```

The adapter must not:

- mutate WorkRun state;
- mint SecurityAdmissionDecision;
- select its own credential/model outside server profile;
- expose raw provider error/secret publicly;
- invoke provider-hosted tools that bypass AISCC tool admission.

If an OpenAI adapter is selected, the design must prefer the current supported structured
function/tool-call surface and must route custom tool requests back through AISCC's own ToolRegistry
and security broker. Exact live model/account configuration remains deferred.

No real provider call in this Task.

---

# Stage 7 — tool registry and tool-call contract

Define a server-owned versioned ToolRegistry.

Every tool must have at minimum:

```text
tool_id
schema_version
description
input schema
side-effect classification
allowed RuntimeMode/profile/scenario
underlying resource requirements
timeout
retry/idempotency policy
output bound
```

Required:

```text
model-proposed tool name/arguments
→ untrusted candidate

registry lookup + schema validation
→ required

P1-5 TOOL resource authority
→ required

P1-3 SecurityAdmissionDecision/capability
→ required before logical tool invocation

underlying PROCESS/FILESYSTEM/NETWORK side effects
→ their own P1-3 capability required
```

A TOOL capability must not automatically authorize its underlying shell/network/filesystem action.

No arbitrary shell tool.
No dynamic executable from model output.
No URL/network destination from model output.

Freeze how exact argument canonicalization/fingerprint binds to the tool authorization.

---

# Stage 8 — bounded agent loop

Define a deterministic bounded execution loop.

At minimum:

```text
load authoritative WorkRun
→ require WorkflowState RUNNING for normal provider/tool side effects

admit ExecutionStatus RUNNING
→ provider call
→ optional bounded custom tool calls
→ provider continuation
→ final AgentOutput
→ execution completion/failure event
```

Every provider/tool side effect revalidates current state/version through P1-3 capability semantics.

Define exact maxima as profile-owned values, not caller inputs:

- provider calls;
- agent rounds;
- tool calls;
- provider retry count;
- timeout;
- output size/token bound.

Required:

```text
state/version changes during loop
→ existing capability stale
→ no silent continuation
```

The design must define whether a fresh capability can continue the same execution attempt and under
which owner/policy.

---

# Stage 9 — idempotency, timeout, ambiguous provider outcome

This is load-bearing.

Freeze distinct failure classes at minimum:

```text
DENIED_BEFORE_SIDE_EFFECT
DEFINITELY_NOT_SENT
PROVIDER_REJECTED
PROVIDER_COMPLETED
TOOL_COMPLETED
TOOL_FAILED
TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME
CANCELLED
RETRY_EXHAUSTED
```

Names may differ, semantics may not.

Do not assume an external provider is idempotent unless the adapter has explicit verified support.

Required:

```text
unknown provider side-effect outcome
→ MUST NOT blindly auto-retry paid/provider mutation
```

Design a durable pre-side-effect operation record / intent and post-side-effect result record, or an
equivalent mechanism that can truthfully distinguish:

```text
not attempted
attempt admitted
outcome known
outcome unknown
```

Define how operation IDs/idempotency keys bind to:

```text
work_run_id
execution attempt
provider/tool resource
input/argument fingerprint
state/version
```

Tool retry must respect tool-specific idempotency/side-effect class.

---

# Stage 10 — execution events / persistence contract

Define restart-surviving append-only execution provenance.

At minimum execution events/operation records must support:

```text
work_run_id
execution_attempt_id
execution_event_id / operation_id
current WorkflowState/state_version observed
ExecutionStatus before/after when applicable
RuntimeMode
provider/tool profile/version
resource/capability/admission refs
request/input hash
tool argument hash
provider/tool result hash
usage metadata
duration
retry/cancel/failure classification
timestamp
sanitization/classification result
```

Never persist raw secrets.

Define:

- append-only history;
- mutable current ExecutionStatus projection;
- atomicity of status projection + lifecycle event;
- ordering/concurrency;
- duplicate event admission;
- restart reconstruction;
- conflict fail-closed behavior.

P1-5 must not modify `state_version` for pure execution-status/event admission.

---

# Stage 11 — output / P1-6 evidence handoff

Define exact producer boundary.

P1-5 may produce immutable refs such as:

```text
AgentOutputRef
ToolOutputRef
ExecutionArtifactRef
ExecutionSubmissionRef
```

or exact equivalents.

But:

```text
producer output ref
!= EvidenceCandidate admission
!= AdmittedEvidence
```

P1-6 owns:

- evidence requirement matching;
- owner/type/freshness/applicability;
- evidence candidate admission/rejection;
- admitted evidence refs.

Define which P1-5 event/ref later supplies `G_EXECUTOR_SUBMISSION` input and which facts remain only
candidate metadata.

Do not implement P1-6.

---

# Stage 12 — mode-specific security contract

Design exact behavior for all modes.

## OWNER_SELF_DOGFOOD

- owner-authorized server provider profile;
- explicit repository/tool/destination bounds;
- isolated worktree/runtime only;
- no direct canonical checkout mutation;
- no Git commit/push authority from agent output.

## PUBLIC_RECORDED_REPLAY

Hard zero-execution:

```text
provider calls:
0

tool calls:
0

process/network side effects:
0
```

Missing Replay must not trigger Live.

## PUBLIC_BOUNDED_LIVE

- fixed synthetic repository/version;
- fixed scenario;
- server-fixed provider/model profile;
- exact scenario tool allowlist;
- bounded calls/retries/time/budget;
- no free-form prompt/task;
- no arbitrary shell/network;
- no public credential/provider/model selection;
- failure/budget exhaustion preserves Replay availability.

Do not claim public release/configuration.

---

# Stage 13 — provider-specific adapter decision boundary

The accepted deployment direction names a separate OpenAI API Project, but current commercial model,
account, pricing, hard-spend configuration and release capability are not frozen here.

The design must classify:

```text
provider-neutral core contract:
P1-5 canonical

concrete adapter protocol:
P1-5 canonical after Human acceptance

exact live model/account/API-key/billing/spend-limit:
future configuration / P3-3 release-time verification
```

If the design selects an OpenAI adapter, it must explicitly forbid provider-hosted execution tools
that bypass AISCC's server-owned ToolRegistry/security path.

No API key or external network call.

---

# Stage 14 — implementation ownership / path contract

Freeze the next implementation ownership.

Expected new source root:

```text
src/aiscc/providers/
```

P1-5 may later modify narrowly required P1-3/P1-4 integration files, but the design must enumerate
which owner contract each modification serves.

Expected categories:

```text
provider/tool domain models + ports
provider/tool resource authority
provider adapter
tool registry/dispatcher
agent execution service
execution event/status persistence
migration
unit/integration tests
versioned non-secret provider profile config
```

Do not create:

```text
src/aiscc/evidence/
src/aiscc/human/
src/aiscc/memory/
```

Those remain P1-6/P1-7/P1-8.

---

# Stage 15 — implementation verification plan

Design the exact next-task proof matrix.

At minimum require:

## RESOURCE_AUTHORITY

- provider/tool absent authority → DENY;
- unknown provider/model/tool → DENY;
- public user cannot select provider/model/tool;
- wrong mode/scenario/profile/version → DENY;
- exact operation/argument fingerprint mismatch → DENY;
- stale state/version capability → DENY.

## REPLAY_ZERO_EXECUTION

Prove provider/tool invocation count remains exactly zero.

## PROVIDER_ADAPTER_CONTRACT

Using deterministic fake/local transport only:

- bounded request serialization;
- structured final output;
- custom tool-call parsing;
- provider-hosted execution tools rejected/not exposed;
- error sanitization;
- no secret leak.

## TOOL_BROKER

- unknown tool → DENY;
- schema-invalid args → DENY before side effect;
- allowed exact tool → product dispatcher;
- TOOL authorization does not bypass underlying PROCESS/FILESYSTEM/NETWORK authorization;
- argument fingerprint binding;
- timeout/cancel/retry behavior.

## EXECUTION_STATUS_EVENTS

- exact status lifecycle;
- idempotent duplicate event;
- concurrent start/complete;
- no `state_version` increment;
- `EXECUTOR_COMPLETED != ACCEPTED`;
- restart reconstruction;
- event/projection conflict fail-closed.

## AMBIGUOUS_PROVIDER_FAILURE

- admitted operation;
- simulated transport timeout after ambiguous send;
- no blind retry;
- durable unknown-outcome event;
- truthful `EXECUTION_FAILED` or exact designed status/result semantics;
- no workflow-state mutation.

## BOUNDED_LOOP

- max provider calls;
- max rounds;
- max tool calls;
- retry exhaustion;
- capability becomes stale after WorkflowState/version change;
- no hidden continuation.

## FINAL_RESIDUE

No Task-owned Docker/network/process residue.

No real provider call is required for implementation acceptance unless a later Human-authorized Task
explicitly adds it.

---

# design evidence contract

## executor_required

- `P1_4_TERMINAL_GIT`
- `P1_5_CANONICAL_READ`
- `PROVIDER_TOOL_AUTHORITY_DESIGN`
- `EXECUTION_STATUS_EVENT_DESIGN`
- `PROVIDER_PROFILE_DESIGN`
- `PROVIDER_ADAPTER_DESIGN`
- `TOOL_REGISTRY_BROKER_DESIGN`
- `BOUNDED_AGENT_LOOP_DESIGN`
- `IDEMPOTENCY_AMBIGUOUS_FAILURE_DESIGN`
- `PERSISTENCE_RESTART_DESIGN`
- `P1_6_HANDOFF_DESIGN`
- `MODE_SECURITY_DESIGN`
- `IMPLEMENTATION_PATH_OWNERSHIP`
- `IMPLEMENTATION_PROOF_MATRIX`

## human_owned

`HUMAN_VERIFICATION`

Human decides whether:

```text
AISCC_PROVIDER_TOOL_EXECUTION.md
→ ACCEPTED
```

## not_required

- product build;
- unit/integration runtime;
- provider network call;
- PostgreSQL migration;
- Docker runtime;
- real credential;
- deployment.

Reason:

This Task is a design freeze after the P1-4 terminal commit.

## forbidden

- product/runtime source implementation;
- provider SDK/dependency installation;
- provider/API network call;
- API key/credential creation/read/print;
- billing/spend-limit configuration;
- P1-6/P1-7/P1-8 implementation;
- public deployment;
- second Git commit after Stage 0;
- Git push/remote mutation;
- Browser Project Source mutation.

---

# proof non-substitution

```text
provider profile design
!= provider configured

OpenAI adapter design
!= live OpenAI call verified

tool schema
!= tool side effect authorized

ExecutionStatus
!= WorkflowState

EXECUTOR_COMPLETED
!= ACCEPTED

AgentOutputRef
!= EvidenceCandidate admission

security ALLOW
!= provider success

design acceptance
!= P1-5 runtime implementation acceptance
```

---

# mandatory stop

Stop if:

```text
P1-5 design requires changing accepted P1-3 hard prohibition
without an exact P1-5-owned extension boundary
→ POLICY_CONFLICT_INVESTIGATION_REQUIRED

P1-5 design would need P1-6/P1-7/P1-8 semantics
→ OWNER_SCOPE_CONFLICT

current canonical rules contradict each other
→ POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

Do not solve a policy conflict by silently weakening P1-2/P1-3/P1-4.

---

# report required fields

- Task ID/path;
- predecessor HEAD;
- exact P1-4 19-path aggregate verification;
- terminal commit path inventory;
- `P1_5_DESIGN_BASE_COMMIT`;
- canonical post-commit clean evidence;
- exact design path changed;
- exact provider/tool authority model;
- exact ExecutionStatus lifecycle;
- exact execution event durability;
- exact provider profile fields;
- exact provider adapter boundary;
- exact tool registry/broker contract;
- exact bounded-loop contract;
- exact timeout/retry/unknown-outcome semantics;
- exact P1-6 handoff;
- exact mode matrix;
- implementation path ownership;
- implementation proof matrix;
- unresolved design question if any;
- Agent claim vs Human pending;
- forbidden-not-run;
- preserved paths;
- next recommendation.

---

# export bundle

Target:

```text
.aiassistant/reports/target/20260828_1110_aiscc-p1-5-provider-tool-execution-contract-design-freeze-with-p1-4-terminal-commit-1/
```

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md`
- compact design review summary

No product source, credential or unrelated file.

---

# Task lifecycle

```text
.aiassistant/tasks/active/20260828_1110_aiscc-p1-5-provider-tool-execution-contract-design-freeze-with-p1-4-terminal-commit-1.md
→
.aiassistant/tasks/done/20260828_1110_aiscc-p1-5-provider-tool-execution-contract-design-freeze-with-p1-4-terminal-commit-1.md
```

`done` means submitted, not Human accepted.

---

# preserved artifacts

Always preserve:

- the P1-4 terminal local commit created by this Task;
- `.aiassistant/tasks/done/20260828_1110_aiscc-p1-4-denied-precreation-retry-consistency-semantics-rework-1.md`;
- `.aiassistant/records/aiscc/cycles/20260828_1110_aiscc-p1-4-explicit-state-machine-kernel-final-acceptance-1.cycle.md`;
- all exact 19 accepted P1-4 implementation paths;
- `.aiassistant/tasks/done/20260828_1110_aiscc-p1-5-provider-tool-execution-contract-design-freeze-with-p1-4-terminal-commit-1.md`;
- `.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md` candidate until Human review.

---

# next action after Human accepts P1-5 design

```text
P1-5 Provider / Tool Execution Implementation + Runtime Verification
```

Do not implement it in this Task.
