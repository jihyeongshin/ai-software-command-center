# AISCC Handoff — Phase B accepted → ingress DB least-privilege correction

Hosted resources remain in place:

```text
aiscc-public-live-postgres:
5238e804-eb7f-4645-b2a8-e134056be72c

aiscc-public-live-initializer:
391ca0a1-5ab4-458c-ae93-eefa96c3f88d

aiscc-public-live-worker:
7878e2ce-bb97-46fd-9331-624234ec4812
```

Do not mutate them in the next Task.

The next source change creates one new NOLOGIN capability role:

`aiscc_public_live_ingress`

It must own only the exact HTTP ingress DB functions needed for:

- clock/limiter;
- capability-scoped read;
- idempotency/admission context;
- atomic admit + start;
- safe run context.

It must not own provider-pipeline, worker, initializer, reconciler, or raw-table mutation authority.

After local acceptance and Git persistence, a later hosted migration/deployment Task will:

1. apply 0021 to the private Live PostgreSQL;
2. create deployment login `aiscc_live_ingress_login`;
3. deploy `aiscc-public-live-ingress`;
4. perform the hosted Railway-edge spoof matrix while admission remains disabled.
