# AISCC Handoff — Secret-bearing deployment accepted → Hosted L5 proof bridge

## current deployed state

```text
source:
96a4029ec3a82c9b2a88b9718732aa0f00ecad20

Railway:
AISCC / production

backend:
aiscc-public-live-api
Online
Singapore

Postgres:
Online
Singapore

AISCC_OPENAI_API_KEY:
service-local
sealed
hidden

health:
/health = 200

Public admission:
DISABLED

Public Live:
NOT_RELEASED
```

## retained architecture fact

The prior deployment-readiness audit found:

`src/aiscc/public_live/http.py` is an isolated fail-closed Public Live ASGI composition and is not mounted by the trusted production API.

Do not claim hosted Public Live proof until that production composition boundary is explicitly established and tested.

## next

IDE Executor audits the exact current source and frozen L5 authority, then either:

- implements the smallest unambiguous production composition/proof bridge while admission remains disabled; or
- stops with a named design blocker if route/trust composition is not already canonically determined.

The paid Luna canary remains forbidden in this next Task.
