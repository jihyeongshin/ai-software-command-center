# AISCC Cycle Record

## meta

- cycle_id: `20260916_1412_aiscc-p3-3-l5-local-secret-binding-rework-durable-missing-secret-evidence-gap-1`
- date: `2026-09-16 KST`
- primary_semantic_owner: `Browser Command Center`
- affected_areas: `P3-3 Public Live L5 hosted secret binding / durable provider execution / local security proof`
- work_type: `REWORK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- predecessor_task: `.aiassistant/tasks/done/20260916_1352_aiscc-p3-3-public-live-l5-railway-secret-binding-and-deployment-contract-implementation-1.md`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause: `IMPLEMENTATION_DEFECT_AND_EVIDENCE_GAP`
- detailed_cause: `DURABLE_MISSING_SECRET_MISCLASSIFIED_AS_UNKNOWN_OUTCOME_AND_REQUIRED_BROAD_REGRESSION_DB_SANDBOX_SECRET_PROOF_INCOMPLETE`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260916_1412_aiscc-p3-3-l5-local-secret-binding-rework-durable-missing-secret-evidence-gap-1.cycle.md`

## result integrity

Executor result ZIP SHA-256:

`faafc3a6a257435b6a7ae75d269da96cd921cd97d276703be6203d6016d647a8`

Adjacent sidecar matched exactly.

## predecessor result

Executor reported:

`HUMAN_RAILWAY_DEPLOYMENT_REQUIRED / local ACCEPTED_CANDIDATE`

Repository:

```text
HEAD before/after:
04436a11adc6dd6e70b4a98568fe878cc4c9f4aa

index:
EMPTY

commit/push/deploy:
NONE

real provider calls:
0

Public admission:
DISABLED
```

Exact L5 authority was correctly recovered:

```text
L5:
Deployment packaging, ingress and sandbox proof

depends_on:
L0
```

The proposed Railway secret boundary and Human-pending hosted proof classification are retained.

## accepted direction retained

The following design direction does NOT require Human re-decision:

```text
variable:
AISCC_OPENAI_API_KEY

opaque secret ref:
secret-ref:openai/public-live/runtime/v1

scope:
Railway production backend service only

Railway variable:
service-level / sealed

project-shared:
NO

frontend/Cloudflare:
NO

PostgreSQL:
NO raw secret

public sandbox/child env:
NO raw secret

adapter:
explicit server-side OpenAI Responses adapter

implicit OPENAI_API_KEY discovery:
FORBIDDEN
```

Railway build exposure caveat remains explicit: sealed variables are still supplied to builds and deployments, so sealing is not build isolation.

## implementation defect

Browser source audit found a semantic mismatch between the non-durable helper and the authoritative durable execution path.

`HostedOpenAISecretResolver.resolve()`:

```text
missing/blank AISCC_OPENAI_API_KEY
→ HostedSecretUnavailable
→ no SDK call possible
```

`AgentExecutionService.execute_provider()` correctly catches this and returns:

```text
LIVE_UNAVAILABLE
DEFINITELY_NOT_SENT
provider_calls = 0
```

However the durable `AgentExecutionService.execute()` path currently performs:

```text
start_dispatch_if_fresh(...)
→ resolver.resolve(...)
→ except Exception
→ OUTCOME_UNKNOWN
→ TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME
```

Therefore a missing secret — where the request is conclusively not sent — is incorrectly persisted as an unknown provider outcome.

This violates the Task's required missing-secret fail-closed contract and the Executor report claim that missing secret is `DEFINITELY_NOT_SENT`.

## required correction

The durable path must preserve the authoritative distinction:

```text
secret unavailable before SDK/provider invocation
= known not sent
!= unknown outcome
```

Required observable semantics:

- no SDK/client request;
- no provider call counter increment;
- no token/usage charge;
- no provider liability beyond zero sent requests;
- operation outcome durably `DEFINITELY_NOT_SENT` or exact canonical equivalent;
- sanitized reason `LIVE_UNAVAILABLE`;
- execution fails closed without unknown-outcome quarantine;
- no blind retry is automatically attempted;
- Replay/static remains independent.

Do not weaken unknown-outcome handling for actual post-send/transport uncertainty.

## evidence gaps

Predecessor evidence:

```text
focused:
267 PASS

final narrow sentinel:
8 PASS

full suite:
NOT_RUN

PostgreSQL durable missing-secret proof:
NOT_RUN

DB secret sentinel proof:
NOT_RUN

actual local sandbox/container secret sentinel:
NOT_RUN

real provider:
NOT_RUN
```

Because source changes touch shared runtime paths including process environment, Docker control and Git observation, the broader regression clause is applicable.

The accepted pre-L5 full baseline is:

`1423 PASS / 3 existing Windows symlink-host SKIP / 0 FAIL / 0 ERROR`

The retry must run the broader suite after correction and prove no skip/xfail/assertion dilution.

## blocker judgment

```text
L5 local secret binding:
REWORK_REQUIRED

Human Railway deployment gate:
NOT_YET_AUTHORIZED

L5:
OPEN

Public admission:
DISABLED

Public Live:
NOT_RELEASED
```

No actual Railway secret entry, deployment or paid provider call should occur until this local rework is accepted.
