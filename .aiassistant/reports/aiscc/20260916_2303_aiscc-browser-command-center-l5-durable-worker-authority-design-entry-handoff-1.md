# AISCC Handoff — Durable worker composition blocker accepted → work-source authority design

## current state

```text
HEAD:
96a4029ec3a82c9b2a88b9718732aa0f00ecad20

reviewed 2253 result ZIP:
c264eaefe92a206c1872c55b4577e7f27abfed38bb998b8d163a1f839ec3747d

2253 result:
DURABLE_WORKER_COMPOSITION_DESIGN_REQUIRED

Browser:
ACCEPTED MANDATORY STOP

2012 hosted binding design:
ACCEPTED / CLOSED

Human D8:
A — ACCEPT_APPLICATION_MEDIATED_EGRESS

Public admission:
DISABLED

Public Live:
NOT_RELEASED

real provider calls:
0
```

## blocker

The current durable Public Live APIs require the worker to already know a `run_id`.

There is no accepted mediated authority that lets a separately startable worker discover and claim eligible durable work.

That authority must be designed before implementation.

## next

Design only.

Do not change product source, tests, schema, deployment, Railway, Cloudflare, OpenAI configuration, Git history or Public state.

After Browser accepts the design, a narrow implementation rework may resume R1 and then R2-R5.
