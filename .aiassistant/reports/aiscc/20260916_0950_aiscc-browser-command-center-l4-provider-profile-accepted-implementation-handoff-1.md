# AISCC Browser Command Center Handoff — accepted Luna adaptive profile → L4 binding

## repository

```text
HEAD:
e287117ba021411b82560df0af61901f7a8212bb
```

## controlling provider policy

`.aiassistant/reports/aiscc/20260916_0950_aiscc-p3-3-public-live-l4-provider-profile-v1-accepted.md`

Status:

`HUMAN_PROVIDED / ACCEPTED V1`

## exact call state

```text
1 primary:
Luna low

2 optional verifier:
Luna low

3 optional bounded correction:
Luna medium

4 retry reserve:
inherits retried logical call effort
```

Limits:

```text
semantic calls <=3
retry <=1
total provider requests <=4
```

Do not implement this as four unconditional sequential calls.

## preserved boundaries

- no free-form public prompt;
- fixed scenario;
- fixed provider/model;
- fixed tool;
- no fallback;
- unknown-outcome no blind retry;
- run deadline 90s;
- frozen monetary/admission budgets unchanged.

## next task

Bind the accepted profile using deterministic/fake-provider evidence only.

Real provider/account verification remains later Human/account work.
