# AISCC Browser Command Center Handoff — accepted retention policy → bounded-storage implementation

## repository identity

```text
branch:
main

HEAD:
bd46b40b47cede29a8865a2b78c42f4de36dc567
```

## controlling policy

`.aiassistant/reports/aiscc/20260916_0447_aiscc-p3-3-public-live-limiter-retention-resource-bound-policy-v1-accepted.md`

Status:

`HUMAN_PROVIDED / ACCEPTED V1`

## accepted implementation rules

```text
retention horizon:
10 DB minute buckets total

prune:
bucket < current_bucket - 9

campaign 1201+:
global deny
no SOURCE row create/increment

cleanup cadence:
at most once/current bucket, demand-driven

maintenance failure:
503 LIVE_UNAVAILABLE / fail closed
```

Existing limits unchanged:

```text
30/min/run
120/min/source
1200/min/campaign
```

## migration rule

Current accepted head should be:

`20260916_0015`

If exact topology passes, create one additive successor:

`20260916_0016_public_live_limiter_retention.py`

Do not edit 0015.

## release boundary

This implementation may produce a release-blocker `RESOLVED_CANDIDATE`.

It does not enable Public admission and does not release Public Live.

L4/L5 remain separate future work.
