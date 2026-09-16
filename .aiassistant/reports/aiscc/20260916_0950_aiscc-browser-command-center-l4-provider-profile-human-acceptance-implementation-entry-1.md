# AISCC Browser Command Center Judgment

## 판정

```text
result_status:
HUMAN_PROVIDED / ACCEPTED

L4 provider profile:
ACCEPTED V1

implementation:
ENTRY_AUTHORIZED
```

## accepted profile

```text
provider:
OpenAI

model:
gpt-5.6-luna

primary reasoning:
low

semantic verification:
low

bounded correction:
medium

max substantive calls:
3

max retry:
1

max total provider requests:
4
```

## rationale captured as policy effect

Happy-path latency remains biased toward one low-reasoning call.

Additional model work is conditional rather than automatic.

Medium reasoning is reserved for exact bounded correction cases.

The fourth request is retry reserve, not a fourth semantic phase.

## retained frozen limits

```text
$0.20/run
$4/day
$15/campaign
20 starts/day
2 concurrent slots
90s run deadline
```

## cost envelope

Current planning bound:

```text
$0.0044 max/request
$0.0176 max/run at four requests
```

The cost advantage does not change admission counts automatically.

## implementation authorization

Next Executor may bind this accepted immutable profile into the current provider/runtime/Public Live dispatch path and add deterministic fake-provider tests.

Still forbidden:

- paid provider call;
- credential-value read/export;
- provider account/billing mutation;
- Public admission enablement;
- L5/deployment;
- Git commit/push.

## account evidence remains separate

Accepted profile policy != configured provider account evidence.

Still pending:

- API Project reference/isolation;
- model access;
- effective limits;
- billing health;
- hard-spend target evidence;
- scoped credential capability.
