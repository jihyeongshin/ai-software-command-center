# 작업지시서: P1-5 Durable Execution / Public Live / Continuation / Secret Lease Rework

## meta

- task_id: `20260828_1823_aiscc-p1-5-durable-execution-public-live-continuation-and-secret-lease-rework-1`
- created_at: `2026-08-28 18:23 KST`
- phase: `P1-5 — Agent Provider and Tool Execution`
- work_type: `IMPLEMENTATION_AND_RUNTIME_VERIFICATION_REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `integrated durable provider/tool execution authority`
- predecessor_task: `20260828_1529_aiscc-p1-5-provider-tool-execution-implementation-and-runtime-verification-1`
- predecessor_result: `ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING`
- command_center_result: `HOLD_REWORK_REQUIRED`
- predecessor_HEAD: `3b150181f1c008d0b95fd53a32cb6e62d174ab4f`
- predecessor_candidate_count: `40`
- predecessor_candidate_aggregate_sha256: `3f944acf3e0941418a955ca1e60aeb23a78271122569baa3ed2580962ce666bd`
- P1_5_design_status: `HUMAN_PROVIDED / ACCEPTED / CLOSED`
- P1_5_runtime_status_before: `HOLD_REWORK_REQUIRED`
- P1_6_status: `NOT_STARTED`

---

# 0. sole execution contract

Retain the predecessor 40-path implementation candidate.

Do not redesign the accepted P1-5 contract.

Close only the identified integration/security/proof gaps:

1. exact PUBLIC_BOUNDED_LIVE P1-5 resource-domain positive path;
2. one production durable AgentExecutionService path;
3. durable local Responses continuation authority;
4. consumed SECRET authority at resolver boundary;
5. exact Tool underlying-resource binding;
6. predecessor terminal Cycle hash evidence correction.

No P1-6/P1-7/P1-8 implementation.

No real provider call/API key/billing/deployment.

---

# Stage 0A — predecessor Git / terminal blob verification

Expected:

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

HEAD:
3b150181f1c008d0b95fd53a32cb6e62d174ab4f
```

Verify:

```text
parent:
d96949f3643e6a0610942e33d70e9da259e1e432
```

Verify the actual committed blob at:

```text
.aiassistant/records/aiscc/cycles/
20260828_1529_aiscc-p1-5-provider-tool-execution-design-final-acceptance-1.cycle.md
```

inside commit `3b150181f1c008d0b95fd53a32cb6e62d174ab4f`.

Required SHA-256:

```text
09f086ba984e4946da9b58b0f5372bae72402a243b205cb83993d6f4f4717cf0
```

Do not trust the predecessor report's different textual digest.

If actual committed blob differs:

```text
STOP
→ BLOCKED_P1_5_TERMINAL_COMMIT_HASH_CONFLICT
```

Also verify committed accepted design SHA:

```text
12070677aa1cfa74b7eea9a52db24f78aacd2bf23d655f125a7689797d172443
```

and exact predecessor Stage-0 six-path commit/message.

---

# Stage 0B — baseline candidate identity

Before Git index mutation verify exact current uncommitted candidate:

```text
candidate count:
40

aggregate SHA-256:
3f944acf3e0941418a955ca1e60aeb23a78271122569baa3ed2580962ce666bd
```

Do not revert/discard it.

Unexpected candidate drift:

```text
STOP
→ BLOCKED_P1_5_CANDIDATE_DRIFT
```

---

# Stage 0C — persist predecessor done Task + HOLD Cycle

Allowed provenance paths exactly:

```text
.aiassistant/tasks/done/
20260828_1529_aiscc-p1-5-provider-tool-execution-implementation-and-runtime-verification-1.md

.aiassistant/records/aiscc/cycles/
20260828_1823_aiscc-p1-5-runtime-integration-public-live-and-continuation-authority-hold-1.cycle.md
```

The predecessor done Task bytes must match the submitted Task contract:

```text
SHA-256:
74498fe365b92739b5f676799c154750f4b1ca16b32238bf87616b3a8c57c961
```

If not:

```text
STOP
→ BLOCKED_P1_5_DONE_TASK_PROVENANCE_MISMATCH
```

Current implementation candidate paths MUST NOT be staged.

Exactly one local provenance commit is authorized.

Exact commit message:

```text
docs: record P1-5 runtime integration hold

Persist the P1-5 runtime review that retained the provider, security,
persistence, and Replay components but found missing positive Public
Live admission and missing durable end-to-end execution authority.

Keep P1-6 blocked until the P1-5 runtime path is integrated and proven.
```

Use LF-safe UTF-8 message file + `git commit -F`.

After commit:

```text
P1_5_RUNTIME_REWORK_BASE_COMMIT=<full hash>
```

Verify exact two paths, exact parent/message, clean index and no remote action.

After this commit:

```text
git add / commit / push
→ FORBIDDEN
```

---

# Stage 1 — candidate universe

The original exact 50-path P1-5 implementation universe remains the absolute maximum.

Current candidate uses 40.

The previously unused authorized paths may now be added only if needed:

```text
config/security/permission-profiles.v1.toml
config/security/resource-policy.v1.toml
src/aiscc/security/models.py
src/aiscc/persistence/database.py
src/aiscc/workflow/models.py
tests/runtime/providers/test_secret_non_exposure.py
tests/unit/security/test_permission_policy.py
tests/unit/security/test_capability_lifetime.py
tests/unit/workflow/test_state_machine.py
tests/integration/security/test_broker_fail_closed.py
```

No 51st path.

If required:

```text
STOP
→ EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

No new dependency is expected.

Do not add any dependency beyond the already accepted/locked:

```text
openai
jsonschema
```

---

# Stage 2 — PUBLIC_BOUNDED_LIVE P1-5 resource admission

Correct P1-3/P1-5 integration so PUBLIC_BOUNDED_LIVE can admit the exact P1-5 domains required by its
fixed synthetic scenario:

```text
ResourceDomain.PROVIDER
ResourceDomain.TOOL
ResourceDomain.SECRET
```

Required:

```text
PUBLIC_RECORDED_REPLAY
→ these domains remain non-executable

PUBLIC_BOUNDED_LIVE
→ domains are profile-eligible
→ still require exact P1-5 selector/SecretUse authority
→ still require every P1-3 security guard
```

Do not create an unconditional allow.

Update both executable policy and canonical non-secret security config when they represent the same
permission profile.

Positive proof must obtain and consume valid P1-3 capabilities in PUBLIC_BOUNDED_LIVE.

Required positive local/fake provider path:

```text
fixed synthetic run
fixed scenario
fixed profile/model
fixed local fake endpoint
valid PROVIDER selector
valid SECRET selector
P1-3 grants/ALLOW/capabilities
→ exactly one provider local-fake side effect
```

Required positive TOOL path:

```text
fixed registry/tool
valid TOOL selector
exact required underlying capabilities
→ exactly one registered dispatcher invocation
```

Wrong profile/scenario/resource/selector remains DENY.

Replay stays zero execution.

---

# Stage 3 — exact server-owned ProviderProfile / ToolDefinition schema alignment

Implement the accepted design fields that are currently missing.

ProviderProfile must carry exact equivalents of:

```text
tool allowlist
timeout policy sufficient to distinguish connect/read/total or an exact V1 equivalent
private_protocol_retention_policy_ref
budget_policy_ref
data_classification_policy_ref
issued_at
revoked_at / enabled lifecycle
```

The local acceptance base URL remains fixture configuration only; do not claim it is release
configuration.

ToolDefinition must carry exact equivalents of:

```text
retry/idempotency policy
enabled/revoked lifecycle
exact underlying resource requirements
optional exact server-owned SecretRequirement
output bound/schema contract
```

Do not expose secret/resource selectors through model-visible arguments.

The fixture config may use empty underlying requirements for `synthetic_lookup`, but the production
model/broker must support exact requirements.

---

# Stage 4 — exact Tool underlying-resource binding

Replace domain-only broker authorization.

A ToolDefinition must define the exact server-owned underlying resource requirements.

Before dispatch, for every requirement verify exact:

```text
ResourceDomain
ResourceScope/resource identity
SecurityActionClass
operation fingerprint
selector attestation where applicable
principal/run/state/version/mode/profile/scenario
```

A supplied capability with:

```text
correct domain
but wrong resource identity
```

must DENY before dispatcher.

For a secret-requiring tool:

```text
exact SecretRequirement
→ exact P1-5 SecretUse attestation
→ P1-3 SECRET grant/capability
→ consumed secret-resolution lease
```

The model arguments never choose secret ref/purpose/destination.

Add deterministic unit proof for same-domain/wrong-resource confused-deputy defense.

---

# Stage 5 — consumed SECRET authority at resolver boundary

A raw `secret_ref` must not be enough to resolve material.

Introduce an unforgeable exact consumption/lease proof or semantic equivalent.

Required flow:

```text
validate all required capabilities
→ atomically consume all
→ broker creates exact secret-resolution lease/receipt
   bound to the consumed SECRET capability/use
→ resolver verifies lease
→ resolve exact secret_ref
→ adapter/dispatcher use
→ close lease
```

Lease/receipt must bind at minimum:

```text
secret non-secret identity
capability ID / consumed use ordinal
principal
work_run_id
execution_attempt_id
operation_id
state/version
RuntimeMode
profile/scenario
purpose/destination
operation fingerprint
expiry
closed/revoked state
```

A forged lease or raw ref:

```text
→ resolver DENY
→ zero material resolution
```

A PROVIDER/TOOL capability cannot generate a secret lease.

Do not put raw material into the lease/provenance.

---

# Stage 6 — durable private provider protocol body

Metadata/hash/reference alone is insufficient for restart continuation.

Implement a restart-durable private protocol payload boundary within the existing authorized
persistence/migration paths.

No new source path.

Required durable state for each continuation item:

```text
canonical exact provider item bytes or an exact private payload reference whose body is actually
restart-readable by production P1-5 code
content hash
item type/order
call_id when applicable
byte count
classification
```

The acceptance database may store private canonical bytes in a private/binary field/table under the
existing migration path. Do not claim public-release infrastructure encryption from this local proof.

Raw secret material is forbidden in protocol payload.

Provider encrypted reasoning content is opaque protocol material only.

Integrity verification must recompute the stored body hash, not merely validate that the hash string
has 64 hex characters.

Corrupt body/hash/order/ref:

```text
→ AuthorityConflictError / fail closed
→ no provider invocation
→ no auto repair
```

---

# Stage 7 — local durable continuation is the only continuation authority

`ProviderCall.input_items` must not accept arbitrary continuation history as authority.

Implement a production path equivalent to:

```text
initial operation
→ server-owned initial input

continuation operation
→ load exact durable private protocol state
→ verify body/hash/order/type/call_id/bounds
→ append exact admitted function_call_output
→ build ProviderCall input internally
→ adapter
```

Use `validate_continuation()` or replace it with an integrated equivalent.

Delete/deprecate any production bypass where a caller can provide unverified continuation items.

Required:

```text
missing durable continuation
→ no provider call

corrupt durable continuation
→ no provider call

wrong call_id/order
→ no provider call

valid durable continuation
→ exact local fake continuation request
```

No provider Conversation/`previous_response_id` fallback.

---

# Stage 8 — compose one durable AgentExecutionService entrypoint

The production P1-5 service must compose the accepted loop.

It may use multiple internal methods, but one production entrypoint used by integration/runtime proof
must own the causal sequence.

Required sequence for a provider operation:

```text
reload P1-4 WorkRun + P1-5 attempt
→ consistency check
→ create durable PREPARED operation
→ issue exact P1-5 selector attestations
→ issue/evaluate exact P1-3 ResourceGrants/PermissionRequests
→ issue exact P1-3 capabilities
→ if denied:
     durable OUTCOME_KNOWN(DENIED_BEFORE_SIDE_EFFECT)
     fail attempt as required
     zero resolver/provider calls
→ advance SECURITY_ADMITTED
→ atomically consume exact capabilities / create secret lease
→ advance DISPATCH_STARTED immediately before adapter crossing
→ resolve secret through verified lease
→ adapter local fake call
→ durable known/unknown outcome
→ persist exact private protocol/output refs
→ tool proposal:
     ToolRegistryBroker exact admission/dispatch
     persist ToolOutputRef
     build durable continuation
     next bounded provider operation
→ final output:
     persist AgentOutputRef
     atomically EXECUTION_COMPLETED + ExecutionSubmissionRef
```

The P1-5 service does not mutate P1-4 WorkflowState/state_version.

P1-4 READY→RUNNING setup remains external/system-owned and is exercised through the accepted P1-4
kernel or exact repository authority in integration proof.

Test code must not manually perform the load-bearing operation edges around the provider call in
place of the production service.

---

# Stage 9 — integrated owner end-to-end proof

Using isolated PostgreSQL + official OpenAI SDK + local fake Responses endpoint:

1. create authoritative WorkRun READY;
2. create ExecutionAttempt NOT_STARTED;
3. admit P1-4 READY→RUNNING through the accepted P1-4 authority path;
4. start P1-5 attempt;
5. fake Responses round 1 returns exact `function_call`;
6. production AgentExecutionService:
   - persists PREPARED/security/dispatch/outcome;
   - dispatches exact synthetic tool;
   - persists ToolOutputRef/private continuation;
7. recreate service/repository objects to prove restart durability;
8. continuation loads only durable protocol state;
9. fake Responses round 2 returns exact final message;
10. persist AgentOutputRef;
11. complete attempt + immutable ExecutionSubmissionRef.

Required final:

```text
WorkRun:
RUNNING
state_version:
unchanged by P1-5 execution events after the external READY→RUNNING transition

ExecutionStatus:
EXECUTOR_COMPLETED

provider calls:
2

tool calls:
1

operation history:
complete / ordered / consistent

submission:
immutable / issuer-backed

P1-6 admitted evidence:
0
```

No test/manual repository edge may substitute for production service orchestration.

---

# Stage 10 — integrated PUBLIC_BOUNDED_LIVE positive proof

Use the same production service with:

```text
RuntimeMode.PUBLIC_BOUNDED_LIVE
fixed synthetic repository
fixed scenario
fixed profile
fixed tool registry
local fake provider endpoint
```

Required:

```text
valid exact selector/capability path
→ provider/tool execution succeeds

public-selected profile/model/tool/secret/scenario/destination
→ DENY before side effect
```

This is acceptance proof only; it does not release Public Bounded Live.

No external network.

---

# Stage 11 — continuation/recovery negative proof

Using the integrated production service:

### MISSING_CONTINUATION

After first tool round, remove required private continuation payload in isolated test transaction.

Fresh continuation:

```text
→ fail closed
→ provider invocation count unchanged
→ no fallback
```

### CORRUPT_CONTINUATION

Corrupt body/hash/order/call_id separately.

Each:

```text
→ fail closed
→ provider invocation count unchanged
→ no auto repair
```

### RESTART_AT_PHASES

Recreate service/repository at:

```text
PREPARED
SECURITY_ADMITTED
DISPATCH_STARTED
```

and enforce the accepted recovery semantics.

No duplicate side effect.

---

# Stage 12 — secret mediator proof

Required:

```text
resolver.resolve(raw secret_ref only)
→ impossible / denied by interface

forged lease
→ DENY

expired/closed/revoked/wrong-operation lease
→ DENY

valid consumed SECRET lease
→ one resolution

provider/tool capability without SECRET
→ zero resolution

atomic consume failure
→ zero resolution
```

Synthetic canary scan remains mandatory.

---

# Stage 13 — evidence/report correction

The rework report must state:

```text
predecessor Task-required terminal Cycle SHA:
09f086ba984e4946da9b58b0f5372bae72402a243b205cb83993d6f4f4717cf0

actual blob in predecessor Stage-0 commit:
<recomputed exact SHA>
```

Do not repeat the predecessor report's `09f086ba543...` value as verified authority.

Explain whether it was report-only transcription or actual commit conflict.

---

# Stage 14 — full regression

Run:

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

Mandatory proof classes:

```text
RESOURCE_AUTHORITY
PUBLIC_LIVE_POSITIVE_EXECUTION
SECRET_MEDIATION
TOOL_EXACT_UNDERLYING_RESOURCE_BINDING
OPERATION_PHASE_GRAPH
DURABLE_AGENT_LOOP
RESPONSES_STATE_MODE
DURABLE_CONTINUATION_AUTHORITY
REPLAY_ZERO_EXECUTION
PROVIDER_ADAPTER_CONTRACT
EXECUTION_STATUS_EVENTS
AMBIGUOUS_PROVIDER_FAILURE
BOUNDED_LOOP
PERSISTENCE_AND_HANDOFF
MODE_SECURITY
FINAL_RESIDUE
```

PostgreSQL migration from empty DB to current head must PASS.

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

- `P1_5_RUNTIME_REWORK_PROVENANCE_GIT`
- `PREDECESSOR_TERMINAL_COMMIT_BLOB_VERIFICATION`
- `BASELINE_40_PATH_CANDIDATE_IDENTITY`
- `PUBLIC_LIVE_POSITIVE_EXECUTION`
- `DURABLE_AGENT_LOOP`
- `DURABLE_CONTINUATION_AUTHORITY`
- `SECRET_RESOLUTION_LEASE`
- `TOOL_EXACT_UNDERLYING_RESOURCE_BINDING`
- `P1_3_SECURITY_REGRESSION`
- `P1_4_WORKFLOW_REGRESSION`
- `POSTGRES_MIGRATION`
- `EXECUTION_STATUS_EVENTS`
- `AMBIGUOUS_PROVIDER_FAILURE`
- `REPLAY_ZERO_EXECUTION`
- `FINAL_RESIDUE`

## human_owned

`HUMAN_VERIFICATION`

If all proof passes:

```text
ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING
```

Executor MUST NOT close P1-5.

## forbidden

- P1-6/P1-7/P1-8 implementation;
- real OpenAI/provider network call;
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
positive selector unit test
!= PUBLIC_BOUNDED_LIVE executable path

manual test orchestration
!= production durable service orchestration

hash metadata
!= durable provider payload

continuation helper
!= continuation authority enforced

SECRET capability consumed
!= resolver verifies consumed authority

underlying ResourceDomain
!= exact ResourceScope requirement

local fake Live proof
!= public release
```

---

# result rules

All required proof passes:

```text
ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING
```

Actual predecessor terminal blob mismatch:

```text
BLOCKED_P1_5_TERMINAL_COMMIT_HASH_CONFLICT
```

Accepted P1-3 ownership would need weakening:

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

---

# report required fields

- Task ID/path;
- predecessor HEAD;
- actual predecessor terminal Cycle blob SHA;
- Stage-0 provenance commit/full hash;
- baseline 40-path aggregate;
- exact post-rework candidate path count/set/aggregate;
- newly used paths from the original 50-path universe;
- exact PUBLIC_BOUNDED_LIVE permission-profile delta;
- successful positive Public Live local proof;
- exact integrated AgentExecutionService causal sequence;
- exact secret lease/receipt contract;
- exact Tool underlying-resource requirement model;
- exact durable private protocol payload model;
- continuation reconstruction source/path;
- missing/corrupt continuation no-call proof;
- owner end-to-end two-round + tool + restart proof;
- P1-3/P1-4 regression;
- test/static/build counts;
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
.aiassistant/reports/target/20260828_1823_aiscc-p1-5-durable-execution-public-live-continuation-and-secret-lease-rework-1/
```

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- all actual post-rework P1-5 candidate files preserving project-relative paths
- compact non-secret static/PostgreSQL/runtime evidence

No raw secret, DB volume, `.venv`, Docker layer, cache or unrelated file.

---

# Task lifecycle

```text
.aiassistant/tasks/active/20260828_1823_aiscc-p1-5-durable-execution-public-live-continuation-and-secret-lease-rework-1.md
→
.aiassistant/tasks/done/20260828_1823_aiscc-p1-5-durable-execution-public-live-continuation-and-secret-lease-rework-1.md
```

`done` means submitted, not Human accepted.

---

# preserved artifacts

Preserve:

- commit `3b150181f1c008d0b95fd53a32cb6e62d174ab4f`
- `.aiassistant/tasks/done/20260828_1529_aiscc-p1-5-provider-tool-execution-implementation-and-runtime-verification-1.md`
- `.aiassistant/records/aiscc/cycles/20260828_1823_aiscc-p1-5-runtime-integration-public-live-and-continuation-authority-hold-1.cycle.md`
- all exact predecessor 40 candidate paths

Historical candidate identity:

```text
40 paths
3f944acf3e0941418a955ca1e60aeb23a78271122569baa3ed2580962ce666bd
```

---

# next action after P1-5 runtime Human acceptance

```text
P1-6 Evidence Admission
```

Do not implement P1-6 in this Task.
