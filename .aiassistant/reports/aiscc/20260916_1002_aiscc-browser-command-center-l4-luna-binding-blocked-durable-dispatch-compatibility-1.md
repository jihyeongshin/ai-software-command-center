# AISCC Browser Command Center Judgment

## 판정

```text
result_status:
HOLD_REWORK_REQUIRED

reject_cause:
POLICY_BASELINE_CONFLICT

executor_fault:
NO

accepted Luna policy:
UNCHANGED / ACCEPTED V1

implementation:
BLOCKED_BEFORE_MUTATION
```

## finding

The 0950 Executor stopped correctly.

The current durable Public Live dispatch contract is a two-request retry model and cannot encode the accepted L4 adaptive pipeline:

```text
PRIMARY_LOW
→ optional VERIFY_LOW
→ optional CORRECT_MEDIUM
+ one known-closed retry reserve
```

without violating existing restart-safe/provider-liability semantics.

## prohibited workarounds

Do not:

- represent VERIFY/CORRECT as fake retries;
- reuse a dispatch ordinal;
- hide multiple paid requests behind a process-local-only scheduler;
- collapse multiple physical provider requests into one durable request identity;
- allow unknown-outcome requests to be resent;
- move cost/token/deadline accounting out of authoritative persistence.

## authorized rework direction

A narrow additive compatibility extension is authorized.

The extension must keep these distinct and durable:

- semantic logical role;
- physical provider request;
- retry ancestry;
- request ordinal/identity;
- reasoning effort;
- validation/defect authority;
- committed token/cost/time envelope;
- outcome certainty;
- settlement/reconciliation state.

No accepted 0013-0016 migration may be edited.

## projection rule

The authoritative Public Live run must not be projected to final governance-pending semantics merely because an intermediate semantic provider phase completed successfully.

Only the server-owned semantic pipeline may decide that provider work is complete.

Intermediate PRIMARY/VERIFY completion remains durable provider evidence, not terminal Public Live provider completion.

The implementation must not invent a new P1 workflow state.

## next Task

Issue one combined compatibility + Luna binding retry.

Expected current HEAD:

`e287117ba021411b82560df0af61901f7a8212bb`

No Human provider-policy decision is pending.

Account/provider evidence remains separately pending.
