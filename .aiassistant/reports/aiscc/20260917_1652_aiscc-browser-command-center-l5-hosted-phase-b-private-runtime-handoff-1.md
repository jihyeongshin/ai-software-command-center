# AISCC Handoff — Hosted Phase A → Private initializer + worker

Canonical source:

`baed7ea3360f6c67c0409c25f84137ab446b90ac`

Accepted Live PostgreSQL:

```text
service:
aiscc-public-live-postgres

service id:
5238e804-eb7f-4645-b2a8-e134056be72c

deployment:
c21d2f5e-a5c2-4f11-850a-6b99f9d270d7

region:
Singapore / asia-southeast1-eqsg3a

Alembic:
20260917_0020

public TCP/domain:
absent
```

Next phase creates only:

1. `aiscc-public-live-initializer`
2. `aiscc-public-live-worker`

Both are private, one-replica, foreground Railway services.

The worker is intentionally deployed WITHOUT an OpenAI key in this phase.

Public ingress, trusted-API cutover, OpenAI-key cutover, paid canary, and release remain later phases.
