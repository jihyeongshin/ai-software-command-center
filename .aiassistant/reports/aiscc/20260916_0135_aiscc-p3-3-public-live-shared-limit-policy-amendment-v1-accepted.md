# P3-3 Public Live Shared-Limit Policy Amendment V1

## status

```text
HUMAN_PROVIDED / ACCEPTED
version:
V1
accepted_at:
2026-09-16 KST
```

Human decision:

`ACCEPT AS WRITTEN`

This document promotes the previously proposed shared-limit amendment into the accepted policy authority for the P3-3 Public Live L3 implementation.

Historical frozen design `209e7534f66e9b07ce9d33742e6993370a70f4fb` remains authoritative for all pre-existing Public Live semantics. This amendment fills only the shared-limit semantics that the frozen package left unspecified.

## provenance

Predecessor proposal:

`.aiassistant/reports/aiscc/20260916_0133_aiscc-p3-3-public-live-shared-limit-policy-amendment-proposal-1.md`

Predecessor Human-decision Cycle:

`.aiassistant/records/aiscc/cycles/20260916_0133_aiscc-p3-3-l3-shared-limit-policy-ambiguity-human-decision-required-1.cycle.md`

Human decision:

```text
ACCEPT AS WRITTEN
```

The proposal remains historical provenance. This document is the accepted versioned amendment.

## 1. authenticated run-read rule

Route:

`GET /v1/public-live/runs/{run_id}`

Authority key:

`canonical run_id`

Eligibility:

- canonical run ID;
- valid, unexpired exact run-bound read capability;
- request otherwise eligible to execute the authenticated read path.

Counting:

- only capability-valid authenticated reads consume the `30/min/run` counter;
- malformed, absent, wrong, expired, or non-matching capability requests do NOT consume this authenticated read counter;
- those requests remain subject to the separate ingress flood limiter.

Window:

```text
fixed 60-second bucket
server/database clock
bucket = floor(epoch_seconds / 60)
```

Cap:

`30 requests per run per bucket`

Boundary:

- requests 1..30: eligible;
- request 31+: deny until next bucket;
- no additional burst allowance inside the bucket;
- crossing the next bucket starts a new count.

Denial:

```text
HTTP 429
code = READ_RATE_LIMIT
retryable = true
Retry-After = integer seconds until next authoritative DB bucket boundary
minimum = 1
maximum = 60
Cache-Control = no-store
```

The error response must not reveal additional run existence/capability details.

Limiter unavailable/ambiguous:

```text
fail closed
HTTP 503
code = LIVE_UNAVAILABLE
retryable = true
no paid effect
no L2 admission side effect
```

If the accepted existing HTTP error vocabulary contains one semantically exact existing 503 code, reuse it rather than create a synonymous alias. If no exact compatible code exists, `LIVE_UNAVAILABLE` is authorized by this amendment for this limiter-unavailable condition.

## 2. shared ingress flood rule

Purpose:

Bound malformed, unauthenticated, abusive, and pre-admission request floods independently from paid admission counters and independently from the authenticated per-run read quota.

Protected surface:

All requests whose normalized path enters the Public Live API namespace:

`/v1/public-live/*`

This includes POST, GET, OPTIONS, unsupported methods, and unsupported subpaths reaching the Public Live router.

Health checks and non-Public-Live application routes are outside this limiter.

### source identity

Use a server-derived canonical source-network bucket, never a browser-provided client ID.

Normalization/privacy:

- IPv4: `/32`;
- IPv6: `/64`;
- campaign-bound HMAC-SHA256 opaque bucket;
- no raw IP persisted or logged;
- current campaign/key version included in identity.

The HTTP layer must consume an already trusted/normalized source identity.

Raw `X-Forwarded-For`, `Forwarded`, or equivalent client-controlled forwarding headers are not authority by themselves.

Hosted trusted-proxy derivation remains L5 proof and is NOT claimed by L3.

### dimensions

Both dimensions must pass:

```text
A. source-network flood bucket:
120 requests / 60 seconds / source bucket

B. campaign-global flood bucket:
1200 requests / 60 seconds / campaign
```

### window

```text
fixed 60-second server/database-clock bucket
no extra burst allowance inside a bucket
```

### counting

- one Public Live ingress request consumes once from both flood dimensions before expensive body parsing, capability validation, authenticated read limiting, or L2 admission;
- malformed requests consume flood quota;
- denied flood requests do NOT consume paid admission counters, authenticated run-read counters, provider budget, or create WorkRuns;
- OPTIONS consumes flood quota;
- health/internal routes outside `/v1/public-live/*` do not consume.

### order

```text
trusted source identity derivation
→ shared flood check/consume
→ CORS/origin/method/request-shape processing
→ capability/authentication
→ authenticated per-run read limiter when GET applies
→ L2 admission/read operation
```

### flood denial

When either flood dimension is exceeded:

```text
HTTP 429
code = CLIENT_RATE_LIMIT
retryable = true
Retry-After = seconds until the later reset among exceeded limiter dimensions
Cache-Control = no-store
safe non-echoing error body
```

Limiter unavailable/ambiguous:

```text
fail closed
HTTP 503
code = LIVE_UNAVAILABLE
retryable = true
no paid/admission/provider effect
```

## 3. shared backend authority

The authoritative limiter must be shared across independent application instances.

A process-local/in-memory limiter may remain only as defense in depth.

Required properties:

- atomic check-and-consume;
- concurrency cannot exceed cap;
- common authoritative backend;
- server/database time;
- opaque source bucket only;
- no raw public-table DML authority at route layer;
- mediated least-privilege function/API;
- no coupling to paid admission counters;
- no workflow/Judgment authority;
- no provider call.

PostgreSQL is the selected authoritative backend for this amendment because Public Live already has accepted PostgreSQL persistence and this avoids introducing an additional runtime dependency before release.

## 4. required proof

The implementation must prove at minimum:

- 30th authenticated read allowed / 31st denied;
- next authoritative DB minute bucket resets the read counter;
- invalid capability requests do not consume run-read quota but do consume flood quota;
- different run IDs have independent read quotas;
- separate service instances share the same read/flood counters;
- concurrent requests cannot exceed 30, 120, or 1200 respective caps;
- source bucket A cannot consume source bucket B's source quota;
- campaign-global cap applies across source buckets;
- OPTIONS and malformed requests consume flood quota;
- flood denial causes zero paid admission/provider side effects;
- limiter backend failure is fail-closed;
- direct raw limiter-table access remains denied;
- L3 CORS/404/non-disclosure behavior remains intact.

## 5. ownership / non-substitution

This amendment owns only the missing shared-limit policy.

It does NOT authorize:

- weakening accepted L2 admission/budget/state semantics;
- L4 provider profile/model/credential work;
- real provider paid calls;
- L5 Railway/trusted-proxy/hosted ingress proof;
- deployment;
- Public admission enablement;
- Public Live release.

Local L3 proof of a normalized source-identity adapter does not substitute for L5 hosted trusted-proxy proof.
