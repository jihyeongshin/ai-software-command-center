# AISCC Cycle Record

## meta

- cycle_id: `20260828_2215_aiscc-p1-5-missing-provider-usage-token-bound-hold-1`
- date: `2026-08-28 22:15 KST`
- primary_semantic_owner: `P1-5 durable output-token accounting`
- work_type: `IMPLEMENTATION_AND_RUNTIME_VERIFICATION / REWORK_JUDGMENT`
- execution_mode: `MANUAL_COMMAND_CENTER`
- predecessor_task: `20260828_2038_aiscc-p1-5-durable-bounds-side-effect-gate-and-public-context-rework-1`
- predecessor_executor_result: `ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING`
- predecessor_HEAD: `d652f01c1c76a9c2ed3c550a7fab6b8414b59c07`
- predecessor_candidate_count: `42`
- predecessor_candidate_aggregate_sha256: `b641cf28833446683d418eb0f671c746a68489074b972fa416039662c93de0b2`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause:
  - `MISSING_PROVIDER_USAGE_TOKEN_ACCOUNTING_IS_NOT_CONSERVATIVE`
- P1_5_runtime_status: `NOT_ACCEPTED`
- P1_6_status: `NOT_STARTED`
- cycle_record_action: `create`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260828_2215_aiscc-p1-5-missing-provider-usage-token-bound-hold-1.cycle.md`

## admitted predecessor evidence

### candidate identity

The submitted export contains exactly:

```text
42 candidate paths

aggregate SHA-256:
b641cf28833446683d418eb0f671c746a68489074b972fa416039662c93de0b2
```

All 42 candidate file SHA-256 values and the aggregate were independently recomputed from the
submitted bundle and matched.

### provenance

Executor reported:

```text
P1_5_FINAL_RUNTIME_REWORK_BASE_COMMIT:
d652f01c1c76a9c2ed3c550a7fab6b8414b59c07

parent:
3312e24b60e0bd10b7c859546d6fdfa3bd2cb025

Stage-0 exact two-path provenance commit:
PASS

post-Stage-0 Git writes:
0
```

Predecessor Task bytes in the submitted bundle:

```text
SHA-256:
4c56d226773b9481f491eb5afcaa73f5eb7823bc24a848e6a542e36519c0d1d7
```

### previous HOLD axes now corrected

Retain:

```text
durable PostgreSQL counters/deadline:
PASS

restart-durable provider/round/tool/budget/output/time bounds:
PASS

Public Live fixed repository/version + scenario authority:
PASS

P1-3 REPOSITORY/SCENARIO capability path:
PASS

provider/tool per-side-effect WorkRun freshness:
PASS

provider-returned tool stale-state denial:
PASS

Tool exact validation/consume before DISPATCH_STARTED:
PASS

same-domain wrong-resource pre-dispatch denial:
PASS

atomic consume pre-dispatch cancellation:
PASS

known provider pre-side-effect denial same-invocation terminalization:
PASS

WORKFLOW_LEFT_RUNNING safety closure:
PASS

durable local Responses continuation:
PASS

SecretResolutionLease:
PASS

Replay zero execution:
PASS
```

### retained verification

Executor-reported evidence:

```text
uv sync --frozen --all-groups:
PASS

uv build:
PASS

ruff:
PASS

mypy --strict:
PASS

unit + integration:
143 PASS

P1-5 persistence/freshness/bounds integration:
22 PASS

P1-5 runtime:
10 PASS

P1-3 Docker runtime:
10 PASS

PostgreSQL:
17.6

Alembic head:
20260828_0002

real provider calls:
0

final Task-owned residue:
0
```

## HOLD — missing provider usage token estimate is not conservative

Current production P1-5 code handles a completed provider result with:

```text
reported_tokens = result.usage.get("output_tokens")

if reported_tokens is present:
    charge reported_tokens
else:
    charge ceil(canonical_output_bytes / 4)
```

The helper explicitly states:

```text
absent usage costs one token per started four canonical output bytes
```

This is not a conservative upper bound on model token consumption.

For byte-level tokenization, an output can require materially more than one token per four UTF-8
bytes. More importantly, provider `output_tokens` may include reasoning-token consumption that is not
recoverable from the serialized visible output body.

Therefore:

```text
actual provider output token usage
> ceil(canonical output bytes / 4)
```

is possible.

With multiple provider calls, the durable cumulative `output_token_bound` can then be exceeded while
the PostgreSQL counter still appears within the bound.

The accepted Task explicitly required:

```text
If provider usage metadata is absent:
- byte bound remains enforceable from canonical body;
- token budget must follow one exact conservative V1 rule;
- do not silently count missing usage as zero if that could exceed the accepted token bound.
```

The current `/4` estimate violates that contract.

## required V1 correction

Do not use tokenizer estimation or visible-output byte ratio as authoritative token accounting.

Recommended exact V1 rule:

```text
provider request max_output_tokens:
M

provider result usage.output_tokens present:
charge exact reported usage

provider result usage.output_tokens absent:
charge M in full
```

Rationale:

```text
M
→ server-owned pre-dispatch ceiling supplied to the provider
→ conservative durable reservation for the unknown actual usage
```

This may overcharge and stop future calls early, but it cannot undercharge the accepted token bound.

Alternative allowed rule:

```text
missing usage
→ fail closed immediately
```

but the implementation/report must choose one exact V1 rule.

Do NOT:

```text
estimate with bytes / N
invoke a tokenizer dependency
treat missing usage as zero
trust visible output body as proof of reasoning-token usage
```

No new dependency is authorized.

## required proof

Using the production durable `AgentExecutionService.execute()` path and local fake Responses endpoint:

### MISSING_USAGE_FULL_CHARGE

For the recommended rule:

1. configure a known `output_token_bound`;
2. send provider request with exact remaining `max_output_tokens=M`;
3. fake provider returns `completed` with valid output but omits `usage`;
4. assert durable counter increases by exactly `M`;
5. recreate repository/service;
6. next provider operation sees the remaining durable bound exactly;
7. no restart reset.

### MISSING_USAGE_CANNOT_UNDERCHARGE

Use a body whose serialized byte count would produce:

```text
ceil(bytes / 4) < M
```

and prove the persisted charge is still `M`, not the byte-derived estimate.

### REPORTED_USAGE_EXACT

When `usage.output_tokens=N` is present:

```text
durable charge:
N
```

not M.

### CUMULATIVE_BOUND

Across restart:

```text
reported/missing usage charges
→ exact durable cumulative count
→ next operation denied before provider side effect when remaining bound is exhausted
```

Provider invocation count must not increase on the denied call.

## Command Center judgment

```text
42-path candidate identity:
PASS

durable bounds:
PASS / RETAIN

per-side-effect freshness:
PASS / RETAIN

Public Live fixed context:
PASS / RETAIN

Tool dispatch ordering:
PASS / RETAIN

workflow-left-running safety closure:
PASS / RETAIN

durable continuation:
PASS / RETAIN

secret mediation:
PASS / RETAIN

missing provider usage token accounting:
HOLD_REWORK_REQUIRED

P1-5 runtime:
NOT ACCEPTED

P1-6:
NOT_STARTED
```

## proof non-substitution

```text
canonical output bytes
!= provider token usage

visible output tokens estimate
!= reasoning token usage

max_output_tokens request ceiling
!= actual usage
but may be used as conservative full-charge authority when usage is absent

143 tests PASS
!= missing-usage undercharge semantics accepted
```

## preservation

Preserve exact commit:

- `d652f01c1c76a9c2ed3c550a7fab6b8414b59c07`

Preserve exact predecessor/current candidate identity:

```text
42 paths
b641cf28833446683d418eb0f671c746a68489074b972fa416039662c93de0b2
```

Preserve exact paths:

- `.aiassistant/tasks/done/20260828_2038_aiscc-p1-5-durable-bounds-side-effect-gate-and-public-context-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260828_2215_aiscc-p1-5-missing-provider-usage-token-bound-hold-1.cycle.md`
- all exact 42 current P1-5 candidate paths.

## next action

```text
P1-5 final token-accounting rework
→ conservative missing-usage durable charge
→ production-path restart proof
→ complete regression
→ Human review
```

Do not start P1-6.
