# 작업지시서: P3-3 L5 Hosted Public Live Binding Local Implementation

## meta

- task_id: `20260916_2148_aiscc-p3-3-public-live-l5-hosted-binding-local-implementation-1`
- created_at: `2026-09-16 KST`
- work_type: `SECURITY_RUNTIME_IMPLEMENTATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_HEAD: `96a4029ec3a82c9b2a88b9718732aa0f00ecad20`
- accepted_design_result_zip_sha256: `4b40a040e9ec764926dedd1a46e09d93fb0472694baddae49ccfcea7b35d9b0a`
- primary_semantic_owner: `P3-3 L5 hosted production binding implementation`

Use the current IDE Executor conversation. No fresh chat is required.

## accepted Human decision

D8 is now final:

`A — ACCEPT_APPLICATION_MEDIATED_EGRESS`

Do not reopen A/B unless implementation discovers a factual contradiction.

Accepted rationale:

- bounded competition runtime, not production customer workload;
- structural service/database/secret separation limits blast radius;
- public/child arbitrary networking remains denied;
- provider/model/transport remain server-fixed;
- OpenAI project hard spend limit `$15` is an independent provider-spend backstop;
- the hard-spend cap does not substitute for service/DB/secret isolation.

## exact accepted topology to implement toward

```text
Cloudflare Pages
  public UI + static Recorded Replay

Railway future service:
aiscc-public-live-ingress
  public
  only Public Live HTTP composition
  no owner routes
  no OpenAI key
  Live DB access only

Railway future service:
aiscc-public-live-worker
  private/no public domain
  durable provider worker
  sole AISCC_OPENAI_API_KEY owner
  application-mediated OpenAI transport
  Live DB access only

Railway future service:
aiscc-trusted-api
  current aiscc.api.app:app
  later no anonymous public domain
  owner DB only
  no OpenAI key after later cutover

Railway future DB:
aiscc-public-live-postgres
  separate Live DB
  no public TCP exposure

temporary QA:
aiscc-public-live-provider-double
  private
  fake provider only
```

This Task implements code/local proof only. It does not create any of those Railway resources.

## authority recovery

Before mutation, re-read:

- accepted 2012 `HOSTED_PUBLIC_LIVE_BINDING_DESIGN.md`;
- accepted 2012 `HOSTED_PUBLIC_LIVE_BINDING_DECISION.json`;
- frozen L5 authority at commit `209e7534f66e9b07ce9d33742e6993370a70f4fb`;
- current P1-3 security/sandbox authority;
- current P1-5 provider/tool/secret authority;
- current Public Live L1-L4 runtime/security authority.

If the transported acceptance artifacts disagree with the 2012 candidate or current source: STOP.

## mandatory implementation goals

### I1 — dedicated Public Live ingress composition

Create/complete a production-hostable ASGI composition that imports/constructs ONLY the accepted Public Live surface.

Exact public route contract:

```text
GET /health

POST /v1/public-live/runs

GET /v1/public-live/runs/{run_id}

OPTIONS only for the two Public Live API routes
```

Explicitly absent/default-denied:

```text
/v1/command-center/**
/command-center/**
/v1/security/**
/docs
/redoc
/openapi.json
admin/debug routes
public cancel route
all unknown routes
all unsupported methods
```

Do not mount `aiscc.api.app:app` into the public ingress.

Public admission must remain `DISABLED`.

While disabled:

```text
POST /v1/public-live/runs
→ truthful LIVE_DISABLED
→ zero provider dispatch
```

Preserve the accepted GET projection semantics.

### I2 — RailwayEdgeIdentityAuthority

Implement a server-owned identity authority for the ingress composition.

Only this owner may mint/set `direct_peer_verified`.

Required inputs/behavior:

1. exact configured `PUBLIC_LIVE_API_ORIGIN`/host authority;
2. exactly one raw `X-Real-IP`;
3. one bare parseable IP only;
4. reject comma lists, duplicate header instances, whitespace-list ambiguity, ports, brackets where not canonical, IPv6 zone IDs and ambiguous forms;
5. `X-Forwarded-Proto` exactly `https`;
6. exactly one syntactically valid `X-Railway-Edge` as provenance only;
7. `Forwarded`, `X-Forwarded-For`, and `CF-Connecting-IP` are conflict-deny signals;
8. no Railway CIDR/hop-count assumption;
9. no public/request-controlled verification boolean;
10. raw IP/raw forwarding headers never enter durable logs/DB/reports/responses.

Important:

Railway `X-Real-IP` remains release-disabled trust until later hosted overwrite/spoof proof succeeds.

Implement an explicit release/config gate so local/source existence does not imply trusted production activation.

Missing/untrusted/conflicting identity must fail before admission/provider side effects.

### I3 — Uvicorn security posture

Expose a deterministic Public Live ingress start path whose later production command is equivalent to:

```text
uvicorn ... --host 0.0.0.0 --port $PORT --no-proxy-headers
```

Do not rely on `FORWARDED_ALLOW_IPS`.

ASGI `scope["client"]` must not be security-authoritative end-user identity.

Do not use trust-all `*`.

### I4 — worker-only provider/secret composition

Create/complete a separately startable durable Public Live worker composition.

Requirements:

- no anonymous HTTP Public Live route;
- no owner Command Center route;
- use existing durable provider/outbox/supervisor owners;
- use `HostedOpenAISecretResolver`;
- real secret resolution remains lease-mediated;
- no child/sandbox inheritance;
- no generic public-selected endpoint/model/provider;
- fixed accepted Luna profile only;
- keep real provider calls impossible in ordinary local tests.

Do not read the real key.

### I5 — application-mediated egress contract

Implement/enforce the accepted D8 application boundary.

Worker provider transport:

```text
scheme:
https

host:
api.openai.com

port:
443

redirect:
disabled

provider/model:
server fixed
```

Live DB:

- only the configured Live Postgres private DSN owner;
- no owner DB binding in ingress or worker composition.

Sandbox/tool child:

`network=none`

Requirements:

- no caller/user field can select destination;
- no arbitrary URL tool;
- no fallback provider/host;
- generic proxy environment variables must not silently redirect the provider transport;
- unexpected destination fails before socket creation where the current transport abstraction permits proof;
- record safe destination class/count only, never secret/header/payload/IP material.

Do NOT claim infrastructure firewall enforcement.

### I6 — separate Live DB composition

Create the runtime configuration boundary needed for ingress/worker to bind to a distinct Live database.

Do not bind ingress/worker to owner Command Center DB repositories.

Prefer reuse of existing schema/migrations and semantic owners.

Do not create a migration merely to encode deployment topology.

If implementing separate Live DB requires a load-bearing schema redesign or new cross-DB authority semantics:

`LIVE_DATABASE_SCHEMA_DESIGN_REQUIRED`

and STOP.

### I7 — operator-only hosted L5 proof CLI

Implement the accepted non-HTTP operator proof mode:

`aiscc hosted-l5-proof`

It must refuse to run unless explicit QA configuration proves:

- unique short-lived proof campaign identity;
- fake/sentinel secret only;
- private fake provider-double target;
- no real OpenAI provider target;
- public admission disabled.

It must never be reachable from anonymous HTTP routing.

Required deterministic fault points:

1. terminate before durable `DISPATCH_STARTED`;
2. terminate after committed `DISPATCH_STARTED` while fake provider double withholds response;
3. known closed fake failure path;
4. sandbox/tool process-tree termination path.

Proof semantics:

```text
pre-dispatch termination
→ DEFINITELY_NOT_SENT
→ zero fake-provider receipts
→ no provider spend

post-dispatch termination
→ OUTCOME_UNKNOWN
→ TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME
→ durable quarantine
→ no blind resend

known closed fake failure
→ retry only if accepted same-role one-retry policy permits

sandbox/tool termination
→ child/container absent OR explicit durable quarantine before release
```

The fake provider double records opaque request IDs/counts only.

### I8 — Replay independence proof support

Do not change the accepted Cloudflare static Replay architecture.

Add only the local/test hooks necessary to prove:

- Live ingress unavailable does not trigger inference;
- worker/provider unavailable does not trigger inference;
- Replay serving path performs zero provider/tool/process/network/secret execution;
- no hidden Live→Replay success substitution.

No Cloudflare mutation.

### I9 — secret non-exposure

With fake sentinel secrets only, prove absence from:

- ingress process environment where secret must be absent;
- child/sandbox env;
- HTTP responses;
- logs;
- durable DB rows;
- public serialization/projection;
- Replay artifacts;
- proof reports.

Never print sentinel itself in exported evidence; report occurrence counts/hashes/classifications only.

### I10 — preserve trusted owner API

`aiscc.api.app:app` remains the owner/trusted composition.

Do not mount Public Live into it as an anonymous route.

Do not remove/rename its existing routes in this local implementation Task unless exact packaging mechanics require a non-semantic entrypoint change.

Actual Railway rename/domain removal occurs later under Human authorization.

## expected local start surfaces

Use existing repository CLI/package conventions.

The implementation must end with exact documented local commands for:

- trusted owner API;
- Public Live ingress;
- Public Live worker;
- hosted-l5-proof QA mode.

Only `aiscc hosted-l5-proof` is exact-name frozen by the accepted design.

For ingress/worker start command names, prefer existing CLI conventions and report the exact chosen commands; do not introduce unnecessary alternate entrypoints.

## tests

Mandatory focused proof:

### ingress route exclusion

- health only;
- disabled POST;
- accepted GET projection;
- exact OPTIONS;
- owner route families absent;
- docs/debug absent;
- unknown route deny;
- unsupported method deny.

### identity parser/authority

- valid canonical IPv4;
- valid canonical IPv6;
- IPv4-mapped IPv6 normalization if retained by accepted source semantics;
- duplicate X-Real-IP;
- comma-list;
- port suffix;
- bracket ambiguity;
- IPv6 zone;
- whitespace ambiguity;
- multiple proto;
- non-https proto;
- missing Railway edge provenance;
- malformed Railway edge provenance;
- forged Forwarded;
- forged X-Forwarded-For;
- forged CF-Connecting-IP;
- Host mismatch;
- release trust gate disabled;
- request attempt to self-set verification.

### owner/DB boundary

- ingress cannot construct/import owner Command Center query/service owners;
- worker cannot construct owner DB owners;
- trusted API does not accidentally bind Live anonymous routes.

Use runtime/component proof where feasible; static import assertions alone cannot substitute for runtime evidence when a runtime proof is possible.

### egress

- provider destination is fixed;
- caller cannot supply URL;
- redirect disabled;
- proxy env cannot retarget transport;
- fallback host/provider unavailable;
- fake transport only in QA;
- sandbox/tool child network none.

### supervisor

Execute fake transport fault matrix with durable PostgreSQL state.

### secret

fake sentinel occurrence count exactly zero in prohibited outputs/artifacts.

### Replay

zero execution under simulated Live/provider failure.

## complete regression

Because shared security/runtime/provider/public-live owners may change, run the complete accepted repository test harness.

Accepted predecessor baseline:

`1460 PASS / 3 existing Windows symlink SKIP / 0 FAIL / 0 ERROR`

Requirements:

- no new skip;
- no new xfail;
- no assertion dilution;
- explain count changes from newly added tests.

Also run:

- Ruff;
- repository formatter check;
- mypy for all changed production owners;
- `git diff --check`;
- source secret scan without printing values;
- package/CLI smoke for every new start surface.

## source scope

Smallest semantic-owner change only.

Likely owners include existing Public Live HTTP/runtime/provider/hosted-secret/CLI/runtime packaging areas and directly corresponding tests.

Do not touch unrelated Command Center UI/state/evidence/memory semantics.

If a new module is cleaner than contaminating the trusted owner API, prefer the new module.

## real provider / external actions

Strictly forbidden:

```text
OpenAI real requests:
0

real OpenAI key read/export:
0

Railway mutation:
0

Railway deploy/restart:
0

Railway service creation:
0

Railway Postgres creation:
0

Railway domain generation:
0

Railway Edge Rule mutation:
0

Cloudflare mutation:
0

Git commit:
0

Git push:
0

Public admission enable:
0

Public Live release:
0
```

## acceptable outcomes

### expected

`HOSTED_PUBLIC_LIVE_BINDING_IMPLEMENTED / LOCAL_ACCEPTED_CANDIDATE`

### schema blocker

`LIVE_DATABASE_SCHEMA_DESIGN_REQUIRED`

### source/design mismatch

`ACCEPTED_BINDING_DESIGN_IMPLEMENTATION_CONFLICT`

None terminally accepts L5.

## mandatory stop

- HEAD mismatch;
- accepted design artifact mismatch;
- implementation requires weakening P1 security/runtime invariants;
- Public Live must be mounted into owner API to proceed;
- anonymous public route would gain owner DB access;
- real OpenAI key/provider call becomes necessary;
- safe egress contract would require a caller-selected destination;
- separate Live DB requires new authority semantics beyond current accepted design;
- complete regression fails after shared-owner changes;
- secret sentinel appears in prohibited durable/public artifacts;
- hosted proof would require deployment action in this Task.

## export

Create:

`.aiassistant/reports/target/20260916_2148_aiscc-p3-3-public-live-l5-hosted-binding-local-implementation-1/`

Required:

- `EXECUTOR_REPORT.md`
- `SOURCE_INVENTORY.json`
- `BINDING_IMPLEMENTATION_AUDIT.md`
- `INGRESS_ROUTE_PROOF.md`
- `IDENTITY_AUTHORITY_PROOF.md`
- `EGRESS_MEDIATION_PROOF.md`
- `SUPERVISOR_PROOF.md`
- `SECRET_NON_EXPOSURE_PROOF.md`
- `REPLAY_INDEPENDENCE_PROOF.md`
- `LOCAL_START_COMMANDS.md`
- `TEST_EVIDENCE.json`
- `WORKSPACE_BEFORE.txt`
- `WORKSPACE_AFTER.txt`
- exact Task copy
- result ZIP

## final response

1. result
2. HEAD
3. accepted design identity
4. source paths changed
5. Public Live ingress composition
6. route exclusion proof
7. RailwayEdgeIdentityAuthority
8. proxy/Uvicorn behavior
9. worker composition
10. Live DB boundary
11. application-mediated egress
12. hosted-l5-proof CLI
13. supervisor/no-send/unknown proof
14. secret non-exposure
15. Replay independence
16. tests/full regression/static/type/package checks
17. real provider calls
18. external actions
19. Public state
20. workspace integrity
21. next Browser gate
