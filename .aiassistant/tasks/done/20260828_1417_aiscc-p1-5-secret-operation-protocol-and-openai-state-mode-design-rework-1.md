# 작업지시서: P1-5 Secret / Operation Protocol / OpenAI State-Mode Design Rework

## meta

- task_id: `20260828_1417_aiscc-p1-5-secret-operation-protocol-and-openai-state-mode-design-rework-1`
- created_at: `2026-08-28 14:17 KST`
- phase: `P1-5 — Agent Provider and Tool Execution`
- work_type: `DESIGN_BASELINE_REWORK`
- evidence_profile: `HIGH_RISK_DESIGN`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `scoped secret mediation + execution-operation protocol + OpenAI Responses transport state`
- predecessor_task: `20260828_1110_aiscc-p1-5-provider-tool-execution-contract-design-freeze-with-p1-4-terminal-commit-1`
- predecessor_result: `ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING`
- command_center_result: `HOLD_REWORK_REQUIRED`
- predecessor_HEAD: `d99ccc4ecde585685e93960a7fa39ecbfde89f9f`
- predecessor_design_path: `.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md`
- predecessor_design_sha256: `d2d5ce009dab6b7c369e35c917bfdb9b6d6a301216e4d35fac80a186ab465a32`
- P1_4_status: `ACCEPTED / CLOSED`
- P1_5_runtime_status: `NOT_STARTED`
- P1_6_status: `NOT_STARTED`

---

# 0. sole execution contract

This is a design-only narrow rework.

Retain the predecessor design unless directly conflicting:

- exact four-value ExecutionStatus;
- execution status separate from WorkflowState/state_version;
- P1-5 PROVIDER/TOOL selector authority separate from P1-3 ALLOW/DENY;
- server-owned ProviderProfile;
- versioned ToolRegistry;
- TOOL capability separate from underlying resource capabilities;
- bounded AgentExecutionService;
- no blind retry for unknown provider/tool outcome;
- append-only execution provenance/current projection;
- producer refs separate from P1-6 evidence admission;
- exact RuntimeMode matrix;
- OpenAI Responses custom-function adapter direction.

Rework only the three HOLD axes.

Do not implement runtime/product source.

---

# Stage 0 — persist predecessor done Task + HOLD Cycle

## expected repository

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

HEAD:
d99ccc4ecde585685e93960a7fa39ecbfde89f9f
```

If HEAD differs:

```text
STOP
→ BLOCKED_PREDECESSOR_HEAD_DRIFT
```

## expected uncommitted design candidate

Verify before Git index mutation:

```text
path:
.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md

SHA-256:
d2d5ce009dab6b7c369e35c917bfdb9b6d6a301216e4d35fac80a186ab465a32
```

Mismatch:

```text
STOP
→ BLOCKED_P1_5_DESIGN_CANDIDATE_DRIFT
```

Do not discard/reconstruct the design.

## exact Stage 0 provenance paths

Only:

```text
.aiassistant/tasks/done/20260828_1110_aiscc-p1-5-provider-tool-execution-contract-design-freeze-with-p1-4-terminal-commit-1.md

.aiassistant/records/aiscc/cycles/20260828_1417_aiscc-p1-5-secret-operation-protocol-and-openai-state-mode-design-hold-1.cycle.md
```

The P1-5 design candidate MUST NOT be staged.

Unexpected tracked path:

```text
STOP
→ BLOCKED_P1_5_DESIGN_REWORK_PROVENANCE_COLLISION
```

## one local provenance commit

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

Exact commit message:

```text
docs: record P1-5 provider tool design hold

Persist the P1-5 design review that retained the execution lifecycle,
resource authority, bounded loop, and evidence handoff but found missing
secret mediation, operation-phase, and Responses state-mode contracts.

Keep P1-5 runtime implementation blocked pending design acceptance.
```

Use LF-safe UTF-8 message file + `git commit -F`.

After commit:

```text
P1_5_DESIGN_REWORK_BASE_COMMIT=<full hash>
```

Verify exact two provenance paths, exact message, parent, clean index and no remote operation.

After this commit:

```text
git add / commit / push
→ FORBIDDEN
```

---

# Stage 1 — accepted security boundary read

Re-read:

```text
.aiassistant/rules/AISCC_SECURITY_SANDBOX.md
.aiassistant/rules/AISCC_RUNTIME_SUBSTRATE.md
.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md
```

Inspect current P1-3 implementation boundary:

```text
src/aiscc/contracts/security.py
src/aiscc/security/policy.py
src/aiscc/security/capability.py
```

Design only. Do not modify source.

Explicitly reconcile:

```text
accepted P1-2:
authorized adapter + purpose-bound opaque secret handle/capability

current P1-3:
ResourceDomain.SECRET fail closed without production secret owner extension

P1-5:
provider/tool execution requires mediated credential use
```

---

# Stage 2 — scoped secret capability extension

Update only:

```text
.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md
```

Freeze an exact typed extension equivalent to:

```text
SecretUseAuthorityPort
SecretUseSelectorAttestation
```

Names may differ.

P1-5 owns only the provider/tool execution secret-use selector/attestation.

P1-3 remains sole owner of:

```text
SecurityAdmissionDecision
ResourceGrant
Capability
capability consume/revoke
```

## required secret attestation binding

At minimum:

```text
attestation id/version
opaque secret_ref or stable non-secret identity/hash
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
operation fingerprint
destination/provider purpose
issued/expiry
max uses
revocation
policy version
```

Required:

```text
no SecretUse authority
→ SECRET DENY

wrong purpose/resource/run/state/version/mode/fingerprint
→ DENY

PROVIDER capability alone
→ no SECRET permission

TOOL capability alone
→ no SECRET permission
```

## required mediated flow

Provider:

```text
ProviderProfile.secret_ref
→ SecretUse attestation
→ P1-3 SECRET admission/capability
→ server-side ProviderAdapter consumes exact capability
→ secret resolver returns material only inside adapter boundary
→ provider transport uses it
→ raw value never enters Agent/workspace/tool args/provenance
```

Tool secret requirement follows the same pattern.

Do not choose AWS/GCP/OpenAI-specific secret manager product.

Do not allow public/model selection of secret ref.

If this exact extension cannot coexist with accepted P1-3 semantics:

```text
STOP
→ POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

---

# Stage 3 — exact ExecutionOperation lifecycle graph

Replace the contradictory single progression with one exact representable acyclic graph.

It MUST support:

```text
deny before security admission
cancel after security admission but before dispatch
dispatch started + definitely-not-sent
known provider/tool completion/failure
unknown outcome
```

Freeze every legal phase edge and illegal edge.

At minimum classify terminal events from:

```text
PREPARED
SECURITY_ADMITTED
DISPATCH_STARTED
```

without hidden transitions.

Recommended semantics:

```text
PREPARED
→ OUTCOME_KNOWN(DENIED_BEFORE_SIDE_EFFECT)
or
→ SECURITY_ADMITTED

SECURITY_ADMITTED
→ OUTCOME_KNOWN(CANCELLED_BEFORE_DISPATCH)
or
→ DISPATCH_STARTED

DISPATCH_STARTED
→ OUTCOME_KNOWN(...)
or
→ OUTCOME_UNKNOWN(...)
```

Exact names may differ.

## outcome mapping table

For every outcome/failure class freeze:

- legal source phase;
- terminal phase;
- side effect definitely absent / may have occurred / known occurred;
- retry eligibility;
- capability consume/revoke semantics;
- budget reservation release/retain semantics;
- whether `ExecutionStatus` must become `EXECUTION_FAILED`;
- whether reconciliation is required.

Clarify:

```text
RETRY_EXHAUSTED
```

as either:

```text
operation terminal class
```

or:

```text
ExecutionAttempt-level failure classification over multiple operations
```

Do not leave it dual-purpose.

---

# Stage 4 — exact OpenAI Responses V1 transport-state contract

The OpenAI Responses custom-function direction remains.

Freeze one exact V1 continuation/state strategy.

## required V1 default

Unless a directly conflicting canonical security requirement is found, use:

```text
Responses API
store=false

provider Conversation resource:
NOT_USED_AS_EXECUTION_AUTHORITY

previous_response_id:
NOT_USED_AS_SOLE_CONTINUATION_AUTHORITY

AISCC durable local operation history:
authoritative continuation source
```

For continuation:

```text
next Responses request
→ explicit bounded replay of required prior provider output items
→ exact function_call_output bound to exact call_id
→ encrypted reasoning item/content replay when required by current protocol
```

Provider response/request IDs remain diagnostic/reconciliation refs.

The design must define:

- exact durable private protocol material required for restart;
- hash/classification of that material;
- sanitization/public exclusion;
- maximum replay/context bound;
- behavior when required continuation item is missing/corrupt;
- no auto-fallback to provider-held conversation state.

If the design deliberately chooses `previous_response_id` instead, document why and freeze exact
provider-state retention/restart/privacy/failure semantics. Do not leave both modes selectable by
implementation convenience.

## current Responses status mapping

Freeze exact adapter mapping for:

```text
queued
in_progress
completed
failed
cancelled
incomplete
```

At minimum define:

- whether synchronous V1 accepts `queued/in_progress` as a terminal adapter return or requires bounded
  polling;
- how bounded polling consumes time/call/budget;
- `completed` with final message;
- `completed` with custom function call;
- `failed`;
- `cancelled`;
- `incomplete` and `incomplete_details`;
- local transport timeout when provider status is unknown.

Required:

```text
incomplete
!= implicit PROVIDER_COMPLETED

incomplete
!= arbitrary PROVIDER_REJECTED without explicit mapping

local timeout after dispatch
→ unknown outcome unless provider reconciliation proves terminal state
```

Hosted provider tools remain disabled.

---

# Stage 5 — exact design consistency pass

After rework, verify the document has no contradiction among:

```text
ProviderProfile.secret_ref
secret capability flow
ToolRegistry underlying SECRET requirements
operation phase graph
outcome taxonomy
retry matrix
ExecutionStatus failure semantics
Responses continuation state
restart persistence
P1-6 handoff
RuntimeMode matrix
next implementation proof matrix
```

Update the implementation proof matrix to include:

## SECRET_MEDIATION

- absent secret authority → DENY;
- wrong purpose/ref/resource/fingerprint → DENY;
- provider/tool capability cannot substitute for SECRET capability;
- raw secret never appears in Agent/workspace/provenance;
- capability use/revoke/expiry proof.

## OPERATION_PHASE_GRAPH

- every legal edge;
- every pre-dispatch terminal path;
- illegal edge denial;
- crash/restart at each nonterminal phase;
- outcome/budget/capability semantics.

## RESPONSES_STATE_MODE

Using fake/local adapter fixtures only:

- `store=false` serialized;
- no provider Conversation state dependency;
- required continuation item replay;
- exact call_id binding;
- encrypted reasoning/private protocol replay fixture;
- missing/corrupt continuation fails closed;
- status mapping for all six current Response statuses;
- local timeout unknown-outcome behavior.

No real provider call in design or implementation acceptance unless separately authorized.

---

# Stage 6 — exact path / scope

This rework changes exactly one design path:

```text
.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md
```

No new canonical rule.

Do not modify:

```text
src/**
tests/**
migrations/**
pyproject.toml
uv.lock
config/**
```

No P1-5 runtime implementation.

---

# evidence contract

## executor_required

- `P1_5_DESIGN_REWORK_PROVENANCE_GIT`
- `BASELINE_DESIGN_IDENTITY`
- `SECURITY_SECRET_BOUNDARY_READ`
- `SCOPED_SECRET_CAPABILITY_DESIGN`
- `OPERATION_PHASE_GRAPH_DESIGN`
- `OPENAI_RESPONSES_STATE_MODE_DESIGN`
- `OPENAI_RESPONSES_STATUS_MAPPING`
- `DESIGN_CONSISTENCY_PASS`
- `IMPLEMENTATION_PROOF_MATRIX_UPDATE`

## human_owned

`HUMAN_VERIFICATION`

If all load-bearing gaps are closed:

```text
ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING
```

Human then decides design acceptance.

## not_required

- product build;
- tests;
- PostgreSQL;
- Docker;
- provider network;
- credential;
- deployment.

## forbidden

- P1-5 runtime/source implementation;
- provider SDK installation;
- provider/API call;
- secret read/creation/configuration;
- billing configuration;
- P1-6/P1-7/P1-8 implementation;
- second Git commit after Stage 0;
- push/remote mutation;
- Browser Project Source mutation.

---

# proof non-substitution

```text
secret_ref
!= secret capability

secret-use attestation
!= P1-3 ALLOW

Provider/Tool capability
!= Secret capability

outcome enum
!= representable lifecycle graph

store=false
!= Zero Data Retention contractual guarantee

provider response ID
!= AISCC authoritative execution state

encrypted reasoning material
!= Evidence/Judgment

OpenAI protocol docs
!= live provider configuration proof
```

---

# result rules

If all three design gaps close:

```text
ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING
```

If secret mediation requires weakening P1-3 security ownership:

```text
POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

If OpenAI current protocol cannot support the frozen continuation contract:

```text
PROVIDER_PROTOCOL_CONFLICT
```

Do not silently choose another provider or hosted tool.

---

# report required fields

- Task ID/path;
- predecessor HEAD;
- Stage 0 provenance commit/full hash;
- baseline design SHA;
- post-rework design SHA;
- exact changed path;
- accepted P1-2/P1-3 secret boundary read;
- exact SecretUse authority contract;
- exact provider secret flow;
- exact tool secret flow;
- exact operation phase graph;
- exact outcome/phase/retry/budget/capability matrix;
- exact Responses V1 state strategy;
- exact continuation/replay contract;
- exact six-status mapping;
- updated implementation proof matrix;
- unresolved questions;
- forbidden-not-run;
- Human pending;
- preserved paths;
- next recommendation.

---

# export bundle

Target:

```text
.aiassistant/reports/target/20260828_1417_aiscc-p1-5-secret-operation-protocol-and-openai-state-mode-design-rework-1/
```

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md`
- compact design review summary

No runtime source or credential.

---

# Task lifecycle

```text
.aiassistant/tasks/active/20260828_1417_aiscc-p1-5-secret-operation-protocol-and-openai-state-mode-design-rework-1.md
→
.aiassistant/tasks/done/20260828_1417_aiscc-p1-5-secret-operation-protocol-and-openai-state-mode-design-rework-1.md
```

`done` means submitted, not Human accepted.

---

# preserved artifacts

Preserve:

- commit `d99ccc4ecde585685e93960a7fa39ecbfde89f9f`
- `.aiassistant/tasks/done/20260828_1110_aiscc-p1-5-provider-tool-execution-contract-design-freeze-with-p1-4-terminal-commit-1.md`
- `.aiassistant/records/aiscc/cycles/20260828_1417_aiscc-p1-5-secret-operation-protocol-and-openai-state-mode-design-hold-1.cycle.md`
- `.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md`

Historical design candidate:

```text
d2d5ce009dab6b7c369e35c917bfdb9b6d6a301216e4d35fac80a186ab465a32
```

---

# next action after Human design acceptance

```text
P1-5 Provider / Tool Execution Implementation + Runtime Verification
```

Do not implement it in this Task.
