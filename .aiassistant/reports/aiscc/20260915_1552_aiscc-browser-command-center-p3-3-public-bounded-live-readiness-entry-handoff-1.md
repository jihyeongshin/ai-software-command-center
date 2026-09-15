# AISCC P3-3 Post-Submission → Public Bounded Live Readiness Handoff

## authoritative current state

```text
HEAD:
5e35ec0d60d84c7a05a2e58ebcc6560863879e5b

Competition submission:
COMPLETED

P3-3:
SUBMITTED / POST_SUBMISSION_IMPROVEMENT_WINDOW

Static Replay:
DEPLOYED / VERIFIED / HUMAN_ACCEPTED

Production URL:
https://aiscc-replay.pages.dev

Public Bounded Live:
NOT_RELEASED
```

## safety baseline

The submitted static Replay is already sufficient for judging and must remain operational if all Live components fail.

Do not make Live the only route to evaluate AISCC.

## accepted architectural direction

Previously accepted competition direction remains:

```text
Public UI / Replay:
Cloudflare Pages

Bounded Live API / PostgreSQL:
Railway Hobby
Singapore

LLM:
separate OpenAI API Project
```

The audit must not silently replace this provider direction.

## current provider facts

Current official Browser re-verification supports:

- Railway Hobby and Singapore deployment;
- OpenAI project-level model/rate controls;
- OpenAI project hard spend limits;
- GPT-5.6 Terra as a current balance-of-intelligence-and-cost model.

No actual account/project/resource/secret has yet been authorized or configured by this handoff.

## desired outcome

Return either:

1. `LIVE_IMPLEMENTATION_READY / HUMAN_ACCEPTANCE_PENDING`; or
2. `REPLAY_ONLY_RETAIN / BLOCKED_PREREQUISITE`.

Do not implement product source until Browser/Human accepts the frozen minimal Live design.
