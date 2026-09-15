# AISCC P3-3 Live Readiness Audit → Security Prerequisite Design Handoff

## current state

```text
HEAD:
5e35ec0d60d84c7a05a2e58ebcc6560863879e5b

Competition submission:
COMPLETED

P3-3:
SUBMITTED / POST_SUBMISSION_IMPROVEMENT_WINDOW

Static Replay:
DEPLOYED / VERIFIED / HUMAN_ACCEPTED

Public Bounded Live:
BLOCKED_PREREQUISITE
```

## first blocker cluster

The accepted audit found that internal execution bounds cannot substitute for public admission safety.

Before provider integration, define an atomic server-owned contract that decides whether a public request may create a paid run.

## design target

A future S1-only Live path may proceed only when one atomic admission boundary can prove:

- scenario exactly allowlisted;
- request schema bounded;
- idempotency cannot duplicate paid work;
- caller bucket/rate state is server-derived;
- global capacity is available;
- daily/campaign USD reserve is available;
- run/read capability is issued safely;
- failure before dispatch releases only what is safe to release;
- ambiguous sent outcomes never create free budget or duplicate dispatch.

No implementation is authorized by this handoff.
