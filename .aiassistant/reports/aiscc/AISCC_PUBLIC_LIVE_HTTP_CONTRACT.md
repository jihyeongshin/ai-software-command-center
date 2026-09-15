# Public HTTP contract

HUMAN_ACCEPTED / FROZEN; not implemented. Uses A1/I1/R1/M1 and schema plan. Mount a distinct public application with only routes below; do not expose current `src/aiscc/api/app.py` owner composition. Read visibility is separate from execution, Judgment and control authority (`src/aiscc/security/cancel.py` and existing cancel authorization tests support that distinction). Public cancel has no route and no capability in this slice.

## Origin and transport

HTTPS only. Require exact Origin `https://aiscc-replay.pages.dev` for POST and GET. Unexpected, `null`, multiple or absent Origin: 403 ORIGIN_DENIED. Non-browser callers may forge Origin, so they still require trusted ingress, rate/budget admission and read capability. CORS is neither authentication nor abuse prevention.

Successful allowed-origin responses and safe errors: `Access-Control-Allow-Origin: https://aiscc-replay.pages.dev`, `Vary: Origin`, `Cache-Control: no-store`, `X-Content-Type-Options: nosniff`. Omit Access-Control-Allow-Credentials (browser credentials mode omit; cookies ignored/rejected as authority). No wildcard. Preflight OPTIONS on these route patterns: exact Origin, requested method POST or GET, requested headers subset of Content-Type, Idempotency-Key, X-Run-Read-Capability; then 204 with Allow-Methods `POST, GET, OPTIONS`, Allow-Headers those three, Max-Age 300 and Vary Origin. Reject invalid preflight 403, no reflected origin/header. Preflight creates no DB admission or run. Invalid origins receive no CORS allow-origin. No redirect endpoints.

## POST /v1/public-live/runs

Content-Type application/json (optional charset=utf-8 only). Maximum 1024 raw bytes including streamed bodies; reject excess before parsing. UTF-8 strict, no duplicate keys, object only, exactly two string fields:

```json
{"scenario_id":"stockroom-s1-normal","scenario_version":"1.0.0"}
```

Required Idempotency-Key: 32 lowercase hex random characters. Reject duplicate header instances. No query parameters, file upload, task text, repository URL, model, provider or free-form fields. Server supplies policy/content pins. Aggregate request headers bounded to 8192 bytes by ingress/app; excess 431. No compressed request body (415).

201 after confirmed A1 commit, exactly:

```json
{"run_id":"<22 unpadded base64url chars>","state":"ADMITTED","read_capability":"<43 unpadded base64url chars>","read_expires_at":"<UTC RFC3339>","replayed":false}
```

Run ID is 128 random bits; read capability is independent 256 random bits. Server stores SHA-256 of decoded capability bytes, compares constant-time, scopes to exact run and expiry. Token is never an idempotency key, URL query/path, cookie, log, trace or provider credential. Return only once on successful 201; store the capability in same-tab sessionStorage until its 24h expiry or tab/session close. Same-tab refresh retains the capability and can resume GET. An independent new tab/session without the capability has no recovery. URL, cookie and localStorage persistence are forbidden; never log the capability. Initial 201 never received means no capability recovery and no automatic replacement run. Tab/session close loses the capability. UX distinguishes ordinary refresh from lost initial response; preserve idempotency key in session memory for safe retry and keep Replay available. No recovery route or public cancel. This contract is Human-accepted H5.

Within 600s, same key/bucket/payload returns 202 exactly `{"run_id":"...","replayed":true}`; no token or status/usage. At/after expiry 410. Token is never recoverable from key or IP. Changing IP loses replay receipt access (403) but a valid read token remains usable; IP is admission authority, not read authority. Public status by run ID alone was considered and rejected because fixed synthetic input does not eliminate cross-user timing/activity disclosure.

## GET /v1/public-live/runs/{run_id}

Require exact 22-character canonical base64url run ID and `X-Run-Read-Capability` with 43 canonical base64url characters. No query parameters. Unknown/malformed run, absent/wrong/expired capability: same 404 NOT_FOUND response, no run existence details. Capability expires exactly admitted_at+24h. Limit authenticated reads to 30/minute per run, durable or trusted shared ingress authority; failed reads have separate bounded ingress flood controls. Never consume paid admission counters on reads.

200 projection has exactly: run_id, state, reason_code (nullable safe enum), admitted_at, updated_at, deadline_at, mode=`PUBLIC_BOUNDED_LIVE`, scenario_id, scenario_version, result (null or bounded synthetic summary object). Summary contains `workflow_state` from actual admitted authority, `summary_text` (max 4000 Unicode characters), `evidence_status` (PENDING/ADMITTED/UNAVAILABLE). Total response <=16384 UTF-8 bytes. No raw provider output, chain of thought, secrets, stack, host path, owner IDs or database content. Truncation of summary text is explicitly indicated inside summary_text; never truncate semantic state/evidence. HTML consumers render text, not executable HTML. Provider success alone cannot produce workflow_state ACCEPTED.

## Errors and retries

Error schema exactly `{"error":{"code":"<enum>","retryable":false}}`, with boolean varied below. No raw input echoes. All errors are no-store. Retry-After integer seconds appears only for bounded temporary throttle/capacity decisions.

| HTTP | Code | Retry behavior |
|---|---|---|
| 400 | INVALID_REQUEST | Fix schema/header; no admission |
| 413 / 415 / 431 | BODY_TOO_LARGE / UNSUPPORTED_MEDIA / HEADERS_TOO_LARGE | No automatic retry |
| 403 | ORIGIN_DENIED / CLIENT_BINDING_DENIED | No automatic retry |
| 404 / 405 | NOT_FOUND / METHOD_NOT_ALLOWED | No retry; cancel route absent |
| 409 | IDEMPOTENCY_CONFLICT | Do not change payload under same key |
| 410 | IDEMPOTENCY_EXPIRED | No automatic new key/run |
| 429 | CLIENT_RATE_LIMIT / GLOBAL_DAY_LIMIT / READ_RATE_LIMIT | Same-key retry after UTC/window boundary; retryable true |
| 503 | CAPACITY_UNAVAILABLE | Same-key retry with bounded backoff; retryable true |
| 503 | DB_UNAVAILABLE / COMMIT_OUTCOME_UNKNOWN | Same-key retry only; retryable true; never infer rollback |
| 503 | IDENTITY_UNAVAILABLE / LIVE_DISABLED / BUDGET_UNAVAILABLE / CAMPAIGN_CLOSED / POLICY_UNAVAILABLE | retryable false; retain Replay |
| 500 | INTERNAL_ERROR | No fresh-key auto retry; use same key to resolve uncertain admission |

First POST transport timeout also follows uncertain-commit handling. Browser retry does not imply provider retry. HTTP success acknowledges an admission/projection, never Human acceptance. A separate static Replay page stays usable during API outage and never relabels a failed Live attempt as Replay success.
