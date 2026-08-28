# 작업지시서: P1-5 Missing Provider Usage Token Accounting Rework

## meta

- task_id: `20260828_2215_aiscc-p1-5-missing-provider-usage-token-accounting-rework-1`
- created_at: `2026-08-28 22:15 KST`
- phase: `P1-5 — Agent Provider and Tool Execution`
- work_type: `IMPLEMENTATION_AND_RUNTIME_VERIFICATION_REWORK`
- evidence_profile: `HIGH_RISK_NARROW`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `durable conservative output-token accounting`
- predecessor_task: `20260828_2038_aiscc-p1-5-durable-bounds-side-effect-gate-and-public-context-rework-1`
- predecessor_result: `ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING`
- command_center_result: `HOLD_REWORK_REQUIRED`
- predecessor_HEAD: `d652f01c1c76a9c2ed3c550a7fab6b8414b59c07`
- predecessor_candidate_count: `42`
- predecessor_candidate_aggregate_sha256: `b641cf28833446683d418eb0f671c746a68489074b972fa416039662c93de0b2`
- P1_5_design_status: `HUMAN_PROVIDED / ACCEPTED / CLOSED`
- P1_5_runtime_status_before: `HOLD_REWORK_REQUIRED`
- P1_6_status: `NOT_STARTED`

---

# 0. sole execution contract

This is a final narrow correctness rework.

Retain all current 42-path implementation behavior.

Change only missing-provider-usage token accounting and the exact tests/evidence needed to prove it.

Do not redesign:

- ProviderProfile;
- durable counter schema;
- WorkRun freshness;
- Public Live fixed context;
- Tool broker;
- SecretResolutionLease;
- Responses local continuation;
- execution lifecycle;
- P1-4 handoff.

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
d652f01c1c76a9c2ed3c550a7fab6b8414b59c07
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
b641cf28833446683d418eb0f671c746a68489074b972fa416039662c93de0b2
```

Exact predecessor Task bytes:

```text
.aiassistant/tasks/done/
20260828_2038_aiscc-p1-5-durable-bounds-side-effect-gate-and-public-context-rework-1.md

SHA-256:
4c56d226773b9481f491eb5afcaa73f5eb7823bc24a848e6a542e36519c0d1d7
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
20260828_2038_aiscc-p1-5-durable-bounds-side-effect-gate-and-public-context-rework-1.md

.aiassistant/records/aiscc/cycles/
20260828_2215_aiscc-p1-5-missing-provider-usage-token-bound-hold-1.cycle.md
```

The 42 candidate paths MUST NOT be staged.

Exactly one local provenance commit is authorized.

Exact commit message:

```text
docs: record P1-5 missing usage token bound hold

Persist the P1-5 runtime review that retained the durable execution,
security, Public Live, and restart proofs but found missing provider
usage could undercharge the authoritative output-token bound.

Keep P1-6 blocked until token accounting is conservative and durable.
```

Use LF-safe UTF-8 message file + `git commit -F`.

After commit:

```text
P1_5_TOKEN_REWORK_BASE_COMMIT=<full hash>
```

Verify exact two paths, parent/message, clean index and no remote operation.

After this commit:

```text
git add / commit / push
→ FORBIDDEN
```

---

# Stage 1 — candidate universe

The original absolute P1-5 universe remains:

```text
50 paths maximum
```

Current candidate:

```text
42 paths
```

No new source path is expected.

Expected actual modifications are narrowly:

```text
src/aiscc/providers/service.py
tests/integration/providers/test_execution_persistence.py
```

A currently-existing unit/fake-server candidate path may be touched only if necessary for exact proof:

```text
tests/unit/providers/test_service.py
tests/fixtures/providers/fake_responses_server.py
```

Do not add a 43rd path solely for this rework.

No new dependency.

---

# Stage 2 — remove non-conservative byte/4 token authority

Current forbidden behavior:

```text
usage.output_tokens missing
→ ceil(canonical_output_bytes / 4)
→ authoritative durable token charge
```

Remove this as an authority rule.

The helper may be deleted if no non-authoritative use remains.

Do not add a tokenizer dependency.

Do not derive authoritative model token usage from visible output byte length.

---

# Stage 3 — exact V1 missing-usage rule

Use this exact recommended rule unless a direct implementation contradiction is found:

```text
requested_max_output_tokens = ProviderCall.output_token_maximum

provider result usage.output_tokens present:
    token_charge = reported exact non-negative integer

provider result usage.output_tokens absent:
    token_charge = requested_max_output_tokens
```

Required properties:

```text
requested_max_output_tokens
→ server-owned
→ bounded by remaining durable output_token_bound
→ serialized as Responses max_output_tokens
```

Therefore missing usage may overcharge but cannot undercharge the accepted durable ceiling.

If `requested_max_output_tokens` is absent/invalid at settlement time:

```text
→ fail closed
→ no zero/estimated charge
```

Do not mutate already-known provider outcome.

The provider operation may remain truthfully `PROVIDER_COMPLETED`, while the attempt fails if the
conservative charge exhausts/violates the cumulative execution bound.

---

# Stage 4 — reported usage validation

Before durable settlement, validate `usage.output_tokens` if present.

Required:

```text
type:
exact integer

minimum:
0

maximum:
<= requested_max_output_tokens
```

Malformed, negative or greater-than-request-ceiling usage:

```text
→ fail closed
→ no undercharge
→ sanitized provider-protocol/accounting failure
```

Do not coerce strings/floats/bools.

If the accepted OpenAI SDK surface returns an integer type, retain that exact value.

---

# Stage 5 — production-path proof

Use isolated PostgreSQL + production `AgentExecutionService.execute()` + local fake Responses
endpoint only.

## MISSING_USAGE_FULL_CHARGE

- configure durable `output_token_bound`;
- first provider request sends exact `max_output_tokens=M`;
- fake response omits `usage`;
- provider returns valid completed output;
- durable `output_tokens` increases by exactly `M`;
- recreate repository/service;
- counter remains exactly `M`.

## MISSING_USAGE_CANNOT_UNDERCHARGE

Use an output body such that:

```text
ceil(canonical_output_bytes / 4) < M
```

Required:

```text
persisted token charge:
M
```

not the old byte estimate.

## REPORTED_USAGE_EXACT

Fake response returns:

```text
usage.output_tokens=N
0 <= N <= M
```

Required:

```text
persisted charge:
N
```

not M.

## MALFORMED_USAGE_FAIL_CLOSED

At minimum:

```text
negative
greater than requested M
non-integer if the fake protocol can represent it
```

Each:

```text
→ no undercharged durable settlement
→ attempt fails closed
```

## CUMULATIVE_RESTART_BOUND

Across at least two provider calls with service/repository recreation:

```text
reported charge + missing-usage full charge
→ durable cumulative output_tokens
```

When remaining bound reaches zero:

```text
next provider operation
→ denied before provider side effect
→ adapter/server invocation count unchanged
```

No direct SQL counter mutation as proof.

---

# Stage 6 — regression

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

Required retained proof classes:

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

Add:

```text
CONSERVATIVE_MISSING_USAGE_TOKEN_ACCOUNTING
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

fake provider processes:
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

- `P1_5_TOKEN_REWORK_PROVENANCE_GIT`
- `BASELINE_42_PATH_CANDIDATE_IDENTITY`
- `MISSING_USAGE_FULL_CHARGE`
- `MISSING_USAGE_CANNOT_UNDERCHARGE`
- `REPORTED_USAGE_EXACT`
- `MALFORMED_USAGE_FAIL_CLOSED`
- `CUMULATIVE_RESTART_BOUND`
- `FULL_P1_3_P1_4_P1_5_REGRESSION`
- `POSTGRES_MIGRATION`
- `FINAL_RESIDUE`

## human_owned

`HUMAN_VERIFICATION`

If all proof passes:

```text
ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING
```

Executor MUST NOT close P1-5.

## forbidden

- new dependency/tokenizer;
- P1-6/P1-7/P1-8 implementation;
- real provider/OpenAI network call;
- API key/real secret;
- billing/spend configuration;
- public deployment;
- LangGraph core;
- second Git commit after Stage 0;
- Git push/remote mutation;
- candidate path outside original exact 50-path universe.

---

# proof non-substitution

```text
canonical body bytes
!= actual provider token usage

bytes/4 estimate
!= conservative token ceiling

missing usage
!= zero usage

requested max_output_tokens
!= actual usage
but may be charged in full as a conservative unknown-usage authority

local fake provider
!= public release
```

---

# result rules

All required proof passes:

```text
ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING
```

Need to weaken accepted P1-5 design:

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
- Stage-0 provenance commit/full hash;
- baseline 42-path aggregate;
- post-rework path count/set/aggregate;
- exact changed paths;
- removed old missing-usage rule;
- exact V1 missing-usage rule;
- exact reported-usage validation;
- missing-usage production proof;
- cumulative restart token-bound proof;
- full static/build/test counts;
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
.aiassistant/reports/target/20260828_2215_aiscc-p1-5-missing-provider-usage-token-accounting-rework-1/
```

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- all actual post-rework candidate files preserving project-relative paths
- compact non-secret runtime/PostgreSQL/static evidence

No raw secret, DB volume, `.venv`, Docker layer, cache or unrelated file.

---

# Task lifecycle

```text
.aiassistant/tasks/active/20260828_2215_aiscc-p1-5-missing-provider-usage-token-accounting-rework-1.md
→
.aiassistant/tasks/done/20260828_2215_aiscc-p1-5-missing-provider-usage-token-accounting-rework-1.md
```

`done` means submitted, not Human accepted.

---

# preserved artifacts

Preserve:

- commit `d652f01c1c76a9c2ed3c550a7fab6b8414b59c07`
- `.aiassistant/tasks/done/20260828_2038_aiscc-p1-5-durable-bounds-side-effect-gate-and-public-context-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260828_2215_aiscc-p1-5-missing-provider-usage-token-bound-hold-1.cycle.md`
- all exact current 42 P1-5 candidate paths

Historical/current candidate identity:

```text
42 paths
b641cf28833446683d418eb0f671c746a68489074b972fa416039662c93de0b2
```

---

# next action after P1-5 runtime Human acceptance

```text
P1-6 Evidence Admission
```

Do not implement P1-6 in this Task.
