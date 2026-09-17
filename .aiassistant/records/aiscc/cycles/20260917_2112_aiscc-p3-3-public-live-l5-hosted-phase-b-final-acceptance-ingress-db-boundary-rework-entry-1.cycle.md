# AISCC Cycle Record

## meta

- cycle_id: `20260917_2112_aiscc-p3-3-public-live-l5-hosted-phase-b-final-acceptance-ingress-db-boundary-rework-entry-1`
- date: `2026-09-17 KST`
- owner: `Browser Command Center`
- phase: `P3-3 Public Live L5`
- predecessor_task: `20260917_1652_aiscc-p3-3-public-live-l5-railway-private-initializer-worker-deployment-1`
- reviewed_result_zip_sha256: `b3c6a761ac114b84fea5bb59802ea3d7ffee53709cebfbf8c068943d2060be2e`
- canonical_commit: `baed7ea3360f6c67c0409c25f84137ab446b90ac`
- result_status: `RAILWAY_PRIVATE_INITIALIZER_WORKER_READY / HOSTED_PHASE_B_ACCEPTED`
- next_status: `INGRESS_DB_LEAST_PRIVILEGE_BOUNDARY_REWORK_REQUIRED`
- l5_terminal: `OPEN`
- public_admission: `DISABLED`
- public_live: `NOT_RELEASED`

## Browser verification

```text
result ZIP SHA-256:
b3c6a761ac114b84fea5bb59802ea3d7ffee53709cebfbf8c068943d2060be2e

archive members:
13

manifest non-self members:
12 / 12 exact SHA + size PASS

canonical local/origin:
baed7ea3360f6c67c0409c25f84137ab446b90ac

Live PostgreSQL:
5238e804-eb7f-4645-b2a8-e134056be72c
private / head 20260917_0020

initializer:
391ca0a1-5ab4-458c-ae93-eefa96c3f88d
SUCCESS / private

worker:
7878e2ce-bb97-46fd-9331-624234ec4812
SUCCESS / private

initializer runtime identity:
PASS

worker runtime identity:
PASS

cross-role deny:
PASS

foreground idle observation:
35.197s

start requests:
0

worker claims:
0

dispatch pins:
0

provider operations:
0

protocol states:
0

worker OpenAI key:
ABSENT

OpenAI calls:
0

existing resource mutation:
only the two explicitly authorized login-role PASSWORD values

source/Git mutation:
0

Public ingress:
NOT_DEPLOYED

Public admission:
DISABLED

Public Live:
NOT_RELEASED
```

## newly exposed ingress prerequisite

Hosted Phase B is accepted.

Before Public ingress deployment, the Browser review rechecked the accepted D6 database boundary against the
current migration/runtime shape.

The accepted hosted design requires a distinct ingress database authority limited to admission/read/limiter
operations.

The existing capability role `aiscc_public_live_runtime` is not suitable for anonymous ingress because the accepted
0017 semantic-provider migration also grants provider-pipeline runtime functions to that role.

Therefore Public ingress MUST NOT be deployed by simply giving it membership in
`aiscc_public_live_runtime`.

This is a narrow least-privilege implementation gap, not a Phase B defect.

## next action

Add a new additive migration `20260917_0021` and a fail-closed ingress runtime-identity check that establish a
dedicated ingress capability role without changing the accepted worker/initializer/provider ownership.

No Railway mutation is authorized by the next Task.
