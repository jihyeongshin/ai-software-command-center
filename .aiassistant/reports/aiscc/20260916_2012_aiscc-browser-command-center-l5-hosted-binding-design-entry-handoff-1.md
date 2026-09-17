# AISCC Handoff — L5 proof bridge stopped correctly → hosted production binding design

## current source/deployment state

```text
accepted source:
96a4029ec3a82c9b2a88b9718732aa0f00ecad20

Railway:
AISCC / production

trusted backend:
aiscc-public-live-api
ONLINE / ACTIVE
Singapore
1 replica

Postgres:
ONLINE
Singapore

AISCC_OPENAI_API_KEY:
service-local
sealed
hidden

health:
/health = 200

real provider calls:
0
```

## current architecture fact

`aiscc.api.app:app` is the deployed trusted app.

It contains owner Command Center read/UI routes and security diagnostics.

`aiscc.public_live.http.PublicLiveApp` is a separate isolated fail-closed ASGI composition and is not mounted into the deployed trusted app.

Do not expose the current trusted app anonymously merely because its `/health` route works.

## platform facts to reconcile

Official Railway documentation verified on 2026-09-16:

- Global edge terminates TLS and forwards to the service.
- Public requests include documented Railway headers including `X-Real-IP` and `X-Railway-Edge`.
- Edge Rules can enforce host/path/header/client-IP allow/block style policy, but documented actions do not provide generic header mutation.
- Browser clients cannot directly use Railway private domains.
- Uvicorn forwarded-header trust must be explicit and must not blindly trust arbitrary clients.

## next task

Design only.

No code changes.
No Railway changes.
No provider calls.
No canary.
No Git mutation.

The output must make the later implementation mechanically unambiguous.
