# P3-3 Public Live Shared-Limit Policy Amendment Proposal

## status

```text
PROPOSED / NOT_ACCEPTED
Human approval required
```

This document proposes new policy where frozen design `209e7534...` is silent.

It does NOT claim these choices already existed in the frozen design.

## purpose

Make the L3 shared read/flood contract exact enough to implement and test without weakening the accepted Public Live security model.

## proposed authenticated run-read rule

Route:

`GET /v1/public-live/runs/{run_id}`

Authority key:

`canonical run_id`

Eligibility:

- canonical run ID;
- valid, unexpired exact run-bound read capability;
- request otherwise eligible to execute the authenticated read path.

Counting:

- only capability-valid authenticated reads consume the 30/min/run counter;
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

If the existing accepted HTTP error vocabulary has a semantically equivalent 503 code, implementation should reuse that exact existing code rather than introduce an alias. If no compatible code exists, Browser/Human must approve the API-code addition before implementation.

## proposed shared ingress flood rule

Purpose:

Bound malformed, unauthenticated, abusive, and pre-admission request floods independently from paid admission counters and independently from the authenticated per-run read quota.

Protected surface:

All requests whose normalized path enters the Public Live API namespace:

`/v1/public-live/*`

This includes POST, GET, OPTIONS and unsupported methods/subpaths reaching the Public Live router.

Health checks or non-Public-Live application routes are outside this limiter.

Source identity:

Use a server-derived canonical source-network bucket, never a browser-provided client ID.

Normalization/privacy follows the already accepted Public Live admission identity rules:

- IPv4: `/32`;
- IPv6: `/64`;
- campaign-bound HMAC-SHA256 opaque bucket;
- no raw IP persisted or logged;
- current campaign/key version included in identity.

The HTTP layer must consume an already trusted/normalized source identity. Raw `X-Forwarded-For` or equivalent headers are not authority by themselves. Hosted trusted-proxy derivation remains L5 proof.

Shared dimensions:

```text
A. source-network flood bucket:
120 requests / 60 seconds / source bucket

B. campaign-global flood bucket:
1200 requests / 60 seconds / campaign
```

Both limits must pass.

Window:

```text
fixed 60-second server/database-clock bucket
no extra burst allowance inside a bucket
```

Counting:

- one ingress request consumes once from both flood dimensions before expensive body parsing, capability validation, or L2 admission;
- malformed requests consume flood quota;
- denied flood requests do not consume paid admission counters, authenticated run-read counters, provider budget, or create WorkRuns;
- OPTIONS consumes flood quota because it is also an externally triggerable ingress request;
- internal test/health paths outside `/v1/public-live/*` do not consume.

Order:

```text
trusted source identity derivation
→ shared flood check/consume
→ CORS/origin/method/request-shape processing
→ capability/authentication
→ authenticated per-run read limiter when GET applies
→ L2 admission/read operation
```

Denial when either flood dimension is exceeded:

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
code = LIVE_UNAVAILABLE (or existing exact equivalent)
retryable = true
no paid/admission/provider effect
```

## proposed shared backend requirements

The authoritative limiter must be shared across independent application instances.

A process-local/in-memory throttle may remain only as defense in depth.

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

PostgreSQL is the recommended authoritative backend because Public Live already uses accepted PostgreSQL 17.6 persistence and it avoids introducing a new release dependency.

## proposed evidence

The implementation Task should prove:

- 30th authenticated read allowed / 31st denied;
- next DB minute bucket resets the read counter;
- invalid capability requests do not consume run-read quota but do consume flood quota;
- different run IDs have independent read quotas;
- separate service instances share the same read/flood counters;
- concurrent requests cannot exceed 30, 120, or 1200 respective caps;
- source bucket A cannot consume source bucket B's quota;
- campaign-global cap applies across source buckets;
- OPTIONS/malformed requests consume flood quota;
- flood denial causes zero paid admission/provider side effects;
- limiter backend failure is fail-closed;
- direct raw limiter-table access remains denied;
- L3 CORS/404/non-disclosure behavior remains intact.

## rationale for proposed numbers

`30/min/run` is frozen and unchanged.

`120/min/source` is a proposed abuse ceiling, not historical fact. It permits approximately 2 requests/second sustained from one source bucket, leaving ample margin for normal judging/browser retry behavior while bounding cheap malformed traffic.

`1200/min/campaign` is a proposed global safety ceiling, not historical fact. It limits distributed request amplification at the application layer while remaining far above expected interactive competition traffic.

These application-level limits do not replace later L5 edge/ingress protection. L5 must still prove trusted-proxy identity and hosted ingress controls.

## Human decision

Human may:

```text
ACCEPT AS WRITTEN
REVISE <exact fields>
REJECT
```

Only `ACCEPT AS WRITTEN` or an exact revised policy may be promoted into the next implementation Task.
