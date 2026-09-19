# AISCC Browser Command Center Handoff — worker claim-sequence recovery blocker

## current baseline

`cf3abc77a4b69335e5fa429049971858c1aa9146`

## current public state

```text
Public control:
DISABLED

Public Live:
NOT_RELEASED

ingress domains:
0

worker domains:
0

edge trust:
ABSENT

held liability:
0

open claims:
0

open dispatch pins:
0

Replay:
release-disabled
```

## blocker

`PUBLIC_WORKER_CLAIM_SEQUENCE_RECOVERY_REGRESSION`

Production worker repeatedly fails its claim loop despite no claimable work.

Current source increments the in-memory sequence before DB acceptance. A failed `last+1` attempt can therefore cause permanent divergence from durable `last_acquire_seq`.

Do not solve this by restart alone.

## next work

Narrow source fix + deterministic PostgreSQL tests + existing worker redeploy + healthy idle-loop proof + fresh readiness reproof.

No provider call, public run, control enablement or release is authorized.
