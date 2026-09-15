# P3-3 Public Live Limiter Retention / Resource-Bound Policy V1

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

This document promotes the `20260916_0445` proposal into accepted policy authority.

It addresses:

`PUBLIC_LIVE_LIMITER_RETENTION_RESOURCE_BOUND_UNRESOLVED`

The accepted request-rate caps remain unchanged:

```text
authenticated run read:
30 / 60s / run

source flood:
120 / 60s / source bucket

campaign flood:
1200 / 60s / campaign
```

## provenance

Historical proposal:

`.aiassistant/reports/aiscc/20260916_0445_aiscc-p3-3-public-live-limiter-retention-resource-bound-policy-proposal-1.md`

Human decision:

```text
ACCEPT AS WRITTEN
```

This accepted V1 document is the controlling authority for the implementation Task.

## 1. retention horizon

Use the authoritative database-clock fixed-minute bucket already defined by the accepted shared-limit policy.

Retain exactly:

```text
current bucket
+ previous 9 buckets
= maximum 10 minute buckets
```

For current bucket `B`, rows with:

```text
bucket < B - 9
```

are expired limiter state and must be eligible for deletion.

Limiter state is enforcement state, not durable workflow/evidence provenance.

No public replay, workflow, provider, budget, or judgment authority depends on retaining expired limiter rows.

## 2. cardinality bound after campaign-global exhaustion

Amend only the globally-denied case:

```text
increment/check CAMPAIGN first

IF resulting campaign count > 1200:
    deny CLIENT_RATE_LIMIT
    DO NOT create or increment a SOURCE row for that request

ELSE:
    consume/check SOURCE normally
```

Rationale:

- after campaign-global exhaustion, every remaining request in that minute is already denied;
- further source-dimension accounting cannot change the allow/deny result in that bucket;
- continuing to materialize arbitrary new source identities would permit unbounded source-row cardinality under a distributed flood;
- before campaign exhaustion, source accounting remains exact and unchanged.

Effect:

```text
maximum new SOURCE identities materialized
per campaign / minute bucket:
<= 1200
```

No request beyond the campaign-global cap gains access.

## 3. READ-row retention

Authenticated READ rows use the same 10-bucket retention horizon.

Only a valid run-bound read capability may create/increment a READ row.

Invalid/missing/expired capability requests remain unable to create READ rows and remain governed only by shared flood limits.

No change to the `30/min/run` rule.

## 4. cleanup ownership

Cleanup is System-owned database maintenance through a mediated API.

Route/public runtime code must not receive raw table DELETE authority.

Implementation must use an additive successor migration to `20260916_0015`.

Existing accepted migration `0015` must remain byte-identical.

The additive implementation may introduce:

- an index supporting expired-bucket deletion;
- a minimal maintenance state/lock primitive when required;
- a `SECURITY DEFINER` mediated prune function;
- `CREATE OR REPLACE` of the accepted flood function only to apply the Human-approved post-global-exhaustion short-circuit.

No unrelated Public Live schema or authority may change.

## 5. cleanup cadence

Cleanup is demand-driven and database-clock-owned.

Before or as part of an authoritative limiter consume path:

1. obtain a narrow database-owned cleanup serialization guard;
2. at most once per current bucket, prune rows where `bucket < current_bucket - 9`;
3. record the last successfully pruned bucket in bounded maintenance state;
4. continue limiter evaluation only after required cleanup state is safe.

No background daemon is required for correctness.

If no Public Live traffic occurs, no new limiter rows are created; deferred cleanup is acceptable until the next limiter operation.

## 6. failure semantics

If required cleanup cannot establish a safe bounded state because of database/maintenance failure:

```text
fail closed
HTTP 503 LIVE_UNAVAILABLE
retryable=true
no L2 admission
no provider call
no paid budget effect
```

A temporary inability to acquire the cleanup serialization guard MAY reuse a recently successful prune from the same current bucket.

It must not treat an unknown/stale maintenance state as safe.

## 7. storage-bound evidence

Implementation must prove at minimum:

- buckets older than the 10-bucket horizon are removed;
- current and previous 9 buckets are retained;
- cleanup uses DB clock, never client time;
- cleanup cannot delete current-bucket enforcement state;
- campaign request 1200 may still source-account normally;
- campaign request 1201+ is globally denied without creating a new SOURCE identity row;
- source distinct-row count in one campaign/bucket cannot exceed 1200 solely through Public ingress;
- valid authenticated READ behavior remains 30/min/run;
- invalid capabilities still create no READ rows;
- cleanup works across independent app instances;
- concurrent cleanup/consume does not admit above 30/120/1200;
- runtime role still has no raw SELECT/DML/DELETE authority on limiter tables;
- maintenance failure is fail-closed;
- existing L1/L2/L3 HTTP behavior and full regression remain green.

## 8. privacy and provenance

No raw IPv4/IPv6 address is persisted during retention or cleanup.

Opaque source HMAC buckets remain the only source identity stored in limiter state.

Deleted limiter rows are not workflow/evidence/Judgment provenance and must not be copied to public logs before deletion.

Operational cleanup evidence may record aggregate row counts/buckets only, not raw/opaque identity values.

## 9. release effect

Human acceptance alone does NOT resolve the blocker.

Only after implementation, PostgreSQL proof, regression, Git persistence, and Browser Command Center acceptance may:

```text
PUBLIC_LIVE_LIMITER_RETENTION_RESOURCE_BOUND_UNRESOLVED
→ RESOLVED
```

Public admission remains disabled until later release authority.
