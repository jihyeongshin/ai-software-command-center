# AISCC Task — L8 PARKED_FAIL_CLOSED Topology + Third Public Release

## meta

- task_id: `20260919_1335_aiscc-p3-3-l8-parked-fail-closed-topology-and-third-public-release-1`
- created_at: `2026-09-19T13:35:00+09:00`
- phase: `P3-3 / L8`
- work_type: `PARKED_TOPOLOGY_ADOPTION_AND_THIRD_PUBLIC_RELEASE`
- execution_model: `THIN_CC_THICK_EXECUTOR`
- exact_baseline: `684de919fd62ef9ecc04bceec8548ee9834458b0`
- request_contract_hardening_commit: `9ddbc6da753d5af1d8e14354f608d101dff2b2e0`
- fresh_ide_chat_required: `No`
- Human_direction: `DIRECT_RELEASE_WITHOUT_SEPARATE_PRIVATE_CANARY`
- Public_Live_entry_state: `NOT_RELEASED`
- Railway_ingress_domain_authority: `ONE_EXISTING_SERVICE_PUBLIC_DOMAIN`
- Railway_ingress_config_authority: `EXACT_RELEASE_ORIGIN_AND_EDGE_TRUST_ONLY`
- Railway_ingress_deploy_authority: `EXACT_CURRENT_SOURCE`
- Railway_worker_mutation_authority: `NONE_UNLESS_PASSIVE_REDEPLOY_REQUIRES_HEALTH_PROOF`
- Cloudflare_mutation_authority: `EXACT_RELEASE_AND_ROLLBACK_FRONTEND_ONLY`
- hosted_control_authority: `ENABLE_FOR_EXACT_RELEASE / DISABLE_FOR_ROLLBACK`
- public_run_authority: `EXACTLY_ONE_THIRD_RELEASE_SMOKE`
- real_provider_authority: `CANONICAL_RUNTIME_FOR_THAT_ONE_RUN_ONLY`
- provider_manual_send_authority: `NONE`
- provider_retry_resend_authority: `NONE`
- UNKNOWN_reconciliation_authority: `EXACTLY_THE_NEW_THIRD_SMOKE_IF_UNKNOWN_AFTER_CONTROL_DISABLED`
- DB_migration_authority: `NONE`
- new_DB_role_grant_authority: `NONE`
- full_teardown_authority: `ONLY_ON_SECURITY_BOUNDARY_FAILURE`
- temporary_Railway_SSH_key_authority: `ONE_EPHEMERAL_KEY_IF_REQUIRED`

## Goal

1. adopt and prove a reusable `PARKED_FAIL_CLOSED` backend topology;
2. immediately perform the third bounded Public Live release;
3. execute exactly one real public smoke through the actual release topology;
4. on ordinary execution-layer failure, rollback to PARKED rather than tearing down backend infrastructure.

Do NOT insert a separate private provider canary.

## accepted entry state

```text
Git main:
684de919fd62ef9ecc04bceec8548ee9834458b0

provider request hardening:
9ddbc6da753d5af1d8e14354f608d101dff2b2e0

migration:
20260919_0025

1919:
FAILED_NOT_DISPATCHED / SETTLED 0

0125:
FAILED_TIMEOUT / SETTLED conservative 4400

1145:
FAILED_TIMEOUT / SETTLED conservative 4400

campaign:
available 14991200 / held 0 / settled 8800

slots:
FREE

claimable work:
0

open claims/pins:
0/0

UNKNOWN candidates:
0

Public control:
DISABLED

Public Live:
NOT_RELEASED

frontend:
Replay-only

public ingress domains:
0
```

## accepted provider request contract

The current worker must use the exact hardened contract.

At minimum:

```text
model:
gpt-5.6-luna

endpoint:
Responses API

reasoning effort:
low for PRIMARY

max output tokens:
2000

parallel tool calls:
false

store:
false

stream:
false

background:
false

tool count:
1

tool:
stockroom_summary
```

Exact zero-argument strict parameters:

```json
{
  "type": "object",
  "properties": {},
  "required": [],
  "additionalProperties": false
}
```

Do not alter this contract during release unless a pre-provider local test reveals a deterministic regression.

No real provider pre-canary.

## new rollback model

### PARKED_FAIL_CLOSED — default

This is the required rollback target for ordinary execution failures.

```text
Railway ingress public domain:
PRESENT

PUBLIC_LIVE_API_ORIGIN:
PRESENT / exact ingress HTTPS origin

AISCC_PUBLIC_LIVE_RAILWAY_EDGE_TRUST:
PRESENT / exact accepted proof binding

ingress deployment:
HEALTHY

worker:
HEALTHY

provider secret:
worker-only / sealed

public_control.enabled:
FALSE

frontend:
Replay-only / Live disabled

new public admission:
DENIED

new provider call:
NONE
```

The backend release topology remains assembled.

### FULL_TEARDOWN — exceptional only

Full removal of domain/origin/edge trust is required only if evidence shows a security-boundary failure, including:
- run creation while `public_control=false`;
- Railway edge/source identity spoof/boundary failure;
- provider secret present outside worker;
- owner/admin route exposed through public ingress;
- public DB exposure;
- ingress cannot deny invalid origin/source;
- backend remains able to dispatch work after control is disabled.

Provider HTTP error, provider UNKNOWN, provider schema rejection, tool failure, and ordinary worker execution failure are **not** full-teardown triggers if PARKED safety holds.

## Phase A — exact preflight

Before mutations verify:

### Git
- `HEAD == origin/main == 684de919fd62ef9ecc04bceec8548ee9834458b0`;
- `9ddbc6da753d5af1d8e14354f608d101dff2b2e0` in ancestry;
- tracked worktree clean for release scope.

### DB
- migration 0025;
- control disabled;
- active future public runs 0;
- held 0;
- slots free;
- claimable work 0;
- open claims/pins 0;
- UNKNOWN candidate 0;
- 1919/0125/1145 states unchanged;
- campaign/day conservation exact.

### worker/provider
- worker healthy;
- request-contract hardened source deployed;
- claim sequence healthy;
- worker-only sealed provider secret;
- provider key absent from ingress/initializer/API;
- no new provider operation since 1145.

### frontend
- Replay public;
- Live disabled;
- no stale release origin in frontend;
- current CSP safe.

Any mismatch => STOP before creating public ingress topology.

## Phase B — construct canonical PARKED backend topology

Use existing `aiscc-public-live-ingress` only.

1. create/restore exactly one Railway-generated HTTPS public domain;
2. derive exact origin from that domain;
3. configure `PUBLIC_LIVE_API_ORIGIN` to that exact origin;
4. configure `AISCC_PUBLIC_LIVE_RAILWAY_EDGE_TRUST` to the already accepted exact proof value, without exporting it;
5. do not change DB/source-key/provider-secret bindings;
6. deploy current exact source;
7. require healthy deployment.

While `public_control=false`, verify:

- valid Railway edge request + valid public Origin reaches only the disabled admission result;
- invalid Origin denied;
- malformed/missing edge identity denied;
- no public run created;
- no claim/pin created;
- no provider operation/call;
- no tool operation;
- no owner/admin route exposed;
- public DB remains unavailable;
- worker public domain remains 0.

If all PASS, declare:

`PARKED_FAIL_CLOSED_ESTABLISHED`

Do NOT remove these backend resources after ordinary execution failures.

## Phase C — parked-state durability proof

Before activating frontend or control, verify the parked topology survives at least one ingress redeploy/restart from current source:

```text
domain:
same exact origin

edge trust:
same exact accepted binding

control:
false

deployment:
healthy

new runs:
0
```

This proves the topology is reusable rather than a one-shot release configuration.

If ingress cannot remain healthy in this exact parked topology:

`PARKED_INGRESS_TOPOLOGY_UNHEALTHY`

and STOP.

## Phase D — frontend release binding

Only after PARKED proof.

Bind frontend to the exact ingress origin as the accepted release surface:

- `live-config.json`: `enabled=true`, exact `api_origin`;
- CSP: `connect-src 'self' <exact-origin>`;
- deterministic build manifest;
- exact directly affected tests.

Deploy existing Cloudflare Pages project.

Backend control remains FALSE throughout this Phase.

Verify:
- page reachable;
- exact config;
- exact narrow CSP;
- four Replay scenarios unchanged;
- no run/provider side effect before control enable.

If frontend deploy fails, restore Replay-only frontend; KEEP backend PARKED.

## Phase E — control enablement LAST

Only after A-D PASS.

Enable only the existing `public-live-v1` campaign.

Immediately re-read:
- enabled true;
- active campaign exact;
- incident null;
- budget/slots sane;
- zero new run before smoke.

## Phase F — exactly one third public smoke

Create exactly ONE run through the actual public release frontend/ingress contract.

Required:
- exact `stockroom-s1-normal / 1.0.0`;
- one fresh idempotency key;
- canonical public Origin;
- one POST only;
- same run polled through canonical GET/read path;
- no second POST/run;
- no manual provider call;
- no alternate model/provider;
- no blind resend.

The runtime may create only canonical provider operations for this single run and within accepted profile ceilings.

### expected diagnostic advantage

If provider returns an HTTP/API error or other UNKNOWN, durable operation refs must now include the accepted fixed safe `provider_diagnostic`.

Do not export raw provider body/request/output.

### success

Success requires an unambiguous expected terminal run, closed known provider operations, valid fixed-tool operation as applicable, conserved accounting, free slot, closed outbox, released claim/pin, and no secret leakage.

On success:
- keep Public Live RELEASED;
- do not park;
- export evidence;
- Browser review;
- Human public-site smoke pending.

## Phase G — failure handling

### first mandatory action

For ANY material failure after control enable:

`public_control.enabled=false` FIRST.

Then prove no second admission/run can occur.

### ordinary execution-layer failure

For:
- provider HTTP error;
- provider UNKNOWN;
- provider protocol incompatibility;
- tool/request failure;
- worker execution failure where identity/security boundary remains intact;

rollback to PARKED:

1. control already false;
2. restore frontend Replay-only:
   - `enabled=false`;
   - `api_origin=null`;
   - CSP `connect-src 'self'`;
3. deploy Replay-only frontend;
4. KEEP Railway ingress public domain;
5. KEEP exact `PUBLIC_LIVE_API_ORIGIN`;
6. KEEP edge-trust proof;
7. KEEP ingress service healthy;
8. KEEP worker/provider secret topology;
9. no second run/provider resend.

Required final status:

`RELEASE_ROLLED_BACK_TO_PARKED_FAIL_CLOSED`

### provider UNKNOWN exact reconciliation

If the new single smoke reaches provider `OUTCOME_UNKNOWN`:

After:
- control=false;
- no second run;
- no resend;
- exact target predicate proves one unique new smoke;

invoke accepted:

`public_live_api.reconcile_unknown_provider_run(bytea)`

through reconciler authority for that exact run only.

Requirements:
- conservative liability derived from accepted profile;
- physical provider truth remains UNKNOWN;
- SETTLE exactly once;
- held -> 0;
- slot free;
- outbox closed;
- claim/pin 0;
- worker work UNKNOWN_RECONCILED/nonclaimable;
- candidate set returns empty;
- idempotent second proof shows no duplicate delta.

This automatic reconciliation is authorized to avoid another cleanup cycle.

### FULL_TEARDOWN

If and only if a security-boundary failure is observed:
- control=false first;
- frontend Replay-only;
- remove public ingress domain;
- remove release origin;
- remove edge-trust binding;
- preserve evidence;
- stop.

Do not full-teardown for an ordinary provider failure.

## Phase H — final success proof

If the smoke succeeds, verify:
- exactly one new public run;
- Public Live enabled;
- exact frontend origin/CSP;
- ingress healthy/domain exact;
- invalid origin/source denied;
- migration 0025 unchanged;
- worker hardened source exact;
- provider diagnostic source exact;
- provider/tool operation counts bounded;
- no UNKNOWN;
- accounting settled exact;
- slots free;
- claim/pin closed;
- Replay remains available;
- provider secret worker-only.

Result:

```text
PUBLIC_LIVE_RERELEASED
/
THIRD_SINGLE_PUBLIC_SMOKE_PASS
/
PARKED_FAIL_CLOSED_POLICY_ADOPTED
/
BROWSER_REVIEW_REQUIRED
/
HUMAN_PUBLIC_SITE_SMOKE_PENDING
```

## Phase I — final failed-smoke parked proof

If ordinary failure occurs, after parked rollback and optional exact UNKNOWN reconciliation verify:

```text
Public control:
FALSE

frontend:
Replay-only

ingress domain:
PRESENT

release origin:
PRESENT

edge trust:
PRESENT

ingress:
HEALTHY

new run count:
exactly 1 for this Task

second run:
0

provider resend:
0

held:
0 if reconciliation/known cleanup completed

claim/pin:
0

provider secret:
worker-only
```

Result:

```text
RELEASE_ROLLED_BACK_TO_PARKED_FAIL_CLOSED
/
<EXACT_FAILURE_CLASS>
/
BROWSER_REVIEW_REQUIRED
```

No fourth release authority.

## source-change boundary

No production source change is expected for PARKED topology itself.

The current ingress already supports a healthy exact-origin release composition.

Do not add an originless disabled-ingress code path solely to preserve full teardown.

If PARKED cannot be represented without product source change:

`PARKED_TOPOLOGY_SOURCE_CHANGE_REQUIRED`

and STOP for Browser review.

## Git / deployment coupling

Fast-forward only.

No amend/rebase/force.

Any release frontend commit may passively deploy repository-connected services.

Before any push after control has been enabled, first establish whether smoke is terminal and safe.

Governance persistence after a successful release must not accidentally disable/redeploy release surfaces.

## temporary operator access

At most one ephemeral Railway SSH key if needed.

- no public DB endpoint;
- no key bytes exported;
- no DB credentials exported;
- no provider secret read;
- cleanup mandatory.

## forbidden

- separate private provider canary;
- second public smoke run;
- manual provider send;
- blind provider resend;
- alternate provider/model;
- new migration;
- DB role/login/grant expansion;
- public DB;
- worker public domain;
- free-form public prompt/tool args;
- unrelated historical test repair;
- unrelated product work;
- full teardown after ordinary execution failure;
- fourth release attempt.

## required export

Create:

`.aiassistant/reports/target/20260919_1335_aiscc-p3-3-l8-parked-fail-closed-topology-and-third-public-release-1/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `PREFLIGHT_SAFE_STATE.md`
- `PARKED_TOPOLOGY_CONFIGURATION.md`
- `PARKED_INGRESS_HEALTH_PROOF.md`
- `PARKED_FAIL_CLOSED_ADMISSION_PROOF.md`
- `FRONTEND_RELEASE_PROOF.md`
- `CONTROL_ENABLEMENT.md`
- `THIRD_PUBLIC_SMOKE.md`
- `PROVIDER_OPERATION_PROOF.md`
- `PROVIDER_DIAGNOSTIC_PROOF.md`
- `TOOL_OPERATION_PROOF.md`
- `ACCOUNTING_SETTLEMENT_PROOF.md`
- `WORKER_CLAIM_PIN_PROOF.md`
- `PARKED_ROLLBACK_PROOF.md` if failure, otherwise `PARKED_ROLLBACK_NOT_USED.md`
- `UNKNOWN_RECONCILIATION_PROOF.md` if applicable, otherwise `UNKNOWN_RECONCILIATION_NOT_USED.md`
- `FINAL_PUBLIC_STATE.md`
- `TEMP_OPERATOR_ACCESS_PROOF.md`
- `WORKSPACE_STATE.md`
- changed release/governance files preserving repository-relative paths

Also create adjacent result ZIP and report SHA-256.

Never export:
- provider key or masked identifier;
- DB DSN/password;
- SSH key material;
- HMAC/source key;
- read capability;
- raw provider request/response/output;
- private reasoning.

## final response format

1. result
2. target ZIP SHA-256
3. preflight
4. parked topology
5. parked fail-closed proof
6. release/frontend commit(s)
7. ingress deployment/domain identity
8. Cloudflare deployment identity
9. control final state
10. exactly-one smoke identity/state
11. provider operation + diagnostic
12. tool result
13. accounting/reservation/slot/outbox
14. claim/pin/work
15. UNKNOWN reconciliation if used
16. final released or PARKED state
17. provider-secret/security state
18. temporary access cleanup
19. Browser/Human pending state
