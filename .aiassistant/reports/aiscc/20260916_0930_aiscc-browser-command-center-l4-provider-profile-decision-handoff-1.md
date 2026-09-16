# AISCC Browser Command Center Handoff — L4 provider profile Human decision

## current repository

```text
branch:
main

HEAD:
e287117ba021411b82560df0af61901f7a8212bb
```

## exact L4

```text
title:
Real provider profile prerequisite

dependency:
L0
```

Frozen monetary/call bounds are unchanged.

## Human decision requested

Review:

`.aiassistant/reports/aiscc/20260916_0930_aiscc-p3-3-public-live-l4-provider-profile-proposal-v1.md`

Status:

`PROPOSED / NOT_ACCEPTED`

Browser recommendation:

`ACCEPT AS WRITTEN`

## proposal

- OpenAI
- `gpt-5.6-terra`
- Responses API default/standard tier
- low reasoning
- <=8000 input tokens/call
- <=2000 output/call
- <=4000 output/run
- <=2 paid calls total
- <=1 retry, only after known closed failure
- 5/30/35-second connect/read/local-call limits
- only local `stockroom_summary`, <=1 dispatch/run
- conservative price envelope: 44,000 micro-USD/call, 88,000/run
- price facts expire after 24h
- dedicated API Project hard-limit target: $15/month
- spend alerts: $10 and $12
- standard global endpoint, synthetic data only
- no provider/model fallback

## not decided/proven by approval

Human profile approval is not account evidence.

Still pending:

- API Project opaque reference;
- actual model access;
- effective RPM/TPM;
- billing health;
- configured hard limit;
- credential-reference binding;
- any paid-provider verification call.

## next step

Human may answer:

`ACCEPT AS WRITTEN`

or provide exact revisions.

No Executor Task is included in this package.
