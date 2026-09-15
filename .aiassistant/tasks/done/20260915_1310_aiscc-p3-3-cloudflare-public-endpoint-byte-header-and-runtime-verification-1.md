# 작업지시서: P3-3 Cloudflare public endpoint byte/header/runtime verification

## meta

- task_id: `20260915_1310_aiscc-p3-3-cloudflare-public-endpoint-byte-header-and-runtime-verification-1`
- created_at: `2026-09-15T13:10:25+09:00`
- work_type: `PUBLIC_VERIFICATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- fresh_ide_chat_required: `No`
- primary_semantic_owner: `P3-3 public deployment verification / Browser Command Center`

## exact authority

Human-provided deployment evidence:

```text
Cloudflare Pages project:
aiscc-replay

production origin:
https://aiscc-replay.pages.dev

deployment:
successful according to Cloudflare Dashboard

deployment method:
Dashboard Direct Upload

uploaded ZIP:
20260915_1303_aiscc-public-replay-cloudflare-dashboard-upload.zip

uploaded ZIP SHA-256:
27cf1e6a462f4d2b4c211965ab2143532bb2cc79768a51005f0ec90e9b2b0ac2
```

Expected deployed source:

```text
repository HEAD:
d13d261eb976fc839e78ba0878080bea93ad5201

artifact:
public/replay

canonical corpus root:
a870da635941d7149edbbef911e8b2d75ff6fe12e8ade80c09dddc9086df795e

Live:
false
```

## objective

Verify that the actual public Cloudflare Pages origin serves the Human-accepted/persisted Public Replay bytes truthfully and safely.

This Task is read-only with respect to the public service.

No Cloudflare credential is required or permitted.

## repository preflight

Before public requests verify:

```text
branch = main
HEAD = d13d261eb976fc839e78ba0878080bea93ad5201
index = empty
tracked worktree = clean
Git-visible untracked = 0
```

Then:

```text
python scripts/build_public_replay.py --check
```

PASS is required.

Do not rebuild/write public files.

If repository baseline or builder check fails, STOP before network verification.

## only authorized network origin

Read-only HTTPS is authorized only to:

`https://aiscc-replay.pages.dev`

No other origin/domain/API may be queried, except DNS/TLS infrastructure intrinsically required to resolve/connect to this exact origin.

Do not authenticate to Cloudflare.

Do not call Cloudflare API/Dashboard endpoints.

Do not follow links to external origins.

If the production origin redirects to a materially different application origin, record and STOP `PUBLIC_ORIGIN_REDIRECT_CONFLICT` unless the redirect is an ordinary canonical HTTPS normalization on the same service.

## required public requests

Use explicit `Accept-Encoding: identity` where practical so response body hashes can be compared deterministically.

Verify:

```text
/                                      expected 200
/health.json                           expected 200
/data/REPLAY_CORPUS_INDEX.json         expected 200
/data/stockroom-s1-normal.json         expected 200
/data/stockroom-s2-missing-evidence.json expected 200
/data/stockroom-s3-policy-conflict.json  expected 200
/data/stockroom-s4-human-owned-claim.json expected 200
/assets/app.js                         expected 200
/assets/styles.css                     expected 200
/404.html                              expected 200
/does-not-exist                       expected 404
```

Record final URL, status, content type, content length where available, and SHA-256 of decoded response body.

Do not store cookies/auth state.

## exact byte identity

Compare public body bytes against local persisted `public/replay` files.

Required exact byte match:

- `data/REPLAY_CORPUS_INDEX.json`
- all four scenario JSON files
- `health.json`
- `assets/app.js`
- `assets/styles.css`
- `index.html`
- `404.html`

If Cloudflare changes line endings/content, that is a mismatch.

Do not waive byte mismatch because the page visually looks correct.

Required result artifact:

`PUBLIC_BYTE_IDENTITY.json`

Include local path, local SHA, public SHA, local bytes, public bytes, match bool.

## health identity

Public `/health.json` must parse to exact semantic values:

```text
status = "ok"
mode = "RECORDED_RUN_REPLAY"
live = false
corpus_root_sha256 = "a870da635941d7149edbbef911e8b2d75ff6fe12e8ade80c09dddc9086df795e"
scenario_count = 4
owner_database = false
provider_inference = false
```

Any difference => FAIL.

## effective security headers

Verify effective production response headers for `/`.

Required semantic policy:

```text
X-Content-Type-Options = nosniff
Referrer-Policy = no-referrer
X-Frame-Options = DENY
Permissions-Policy includes:
camera=()
microphone=()
geolocation=()
payment=()
usb=()

Content-Security-Policy includes:
default-src 'none'
script-src 'self'
style-src 'self'
connect-src 'self'
img-src 'self'
font-src 'none'
object-src 'none'
base-uri 'none'
frame-ancestors 'none'
form-action 'none'

Cache-Control includes:
no-cache
```

Header order/whitespace may differ.

Missing or materially weaker required directive => `PUBLIC_HEADER_VERIFICATION_FAILED`.

Also record Cloudflare-added non-security headers separately without treating them as defects.

## 404 behavior

Verify:

```text
GET /does-not-exist
```

returns actual HTTP `404`.

Record public body.

PASS when:

- status is 404;
- body is truthful;
- body does not imply successful AI execution.

Preferred/expected authored wording includes:

```text
Page not found.
No AI execution was started.
Live Demo is not enabled.
```

Cloudflare may serve a different truthful 404. If so, classify separately and assess whether Human QA is required for wording.

## public content truth scan

Fetch `/` and verify visible/source text contains the accepted meanings:

```text
AI Software Command Center
Recorded Run Replay

This is a recorded historical run.
Viewing it does not execute AI.

Live Demo is not enabled.
Recorded Run Replay remains available.
```

Verify the static artifact contains no active user task/upload/mutation form.

Do not infer rendered DOM from HTML alone where JS-generated content is involved; use source/JS static inspection plus later Human QA.

## public runtime isolation scan

Inspect public HTML/JS/CSS and requested URLs for references to:

- owner/private API;
- PostgreSQL;
- OpenAI/provider endpoint;
- Railway;
- arbitrary external API;
- active Live endpoint;
- user repository URL input;
- file upload;
- free-form task execution;
- analytics/tracker/CDN.

Expected:

```text
none
```

Do not query discovered unexpected external endpoints; record as evidence and fail.

## same-origin data contract

`assets/app.js` must continue to request only same-origin allowlisted Replay JSON paths.

Record the exact fetch targets found.

Expected total Replay data set:

```text
REPLAY_CORPUS_INDEX.json
stockroom-s1-normal.json
stockroom-s2-missing-evidence.json
stockroom-s3-policy-conflict.json
stockroom-s4-human-owned-claim.json
```

## TLS/origin evidence

Record:

- requested origin;
- final origin;
- HTTPS success;
- certificate validation result as exposed by the HTTP client;
- any redirects.

Do not perform invasive TLS scanning.

## repository terminal state

Public verification must not mutate source.

At end verify:

```text
HEAD = d13d261eb976fc839e78ba0878080bea93ad5201
index = empty
tracked worktree = clean
Git-visible untracked = 0
```

Temporary HTTP evidence belongs only in target report/export paths according to project policy.

## canonical record updates — only on full PASS

If all required public verification passes, update:

### `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`

Narrowly to:

```text
Recorded Replay local implementation:
HUMAN_PROVIDED / ACCEPTED / PERSISTED

Public Replay deployment:
DEPLOYED / PUBLIC_VERIFICATION_PASSED

Public production URL:
https://aiscc-replay.pages.dev

Public Bounded Live:
NOT_RELEASED / DISABLED_FOR_INITIAL_RELEASE

P3-3:
ACTIVE / HUMAN_PUBLIC_QA_PENDING
```

### `.aiassistant/records/aiscc/NEXT_ACTIONS.md`

Project:

```text
1. Human public-URL final visual QA
2. rights/tool/model disclosure confirmation
3. post-public-QA persistence
4. final competition submission
5. judging-window availability monitoring
```

### `.aiassistant/reports/aiscc/AISCC_P3_3_PUBLIC_RELEASE_READINESS.md`

Resolve the public deployment blocker with exact URL/public verification evidence.

### `.aiassistant/reports/aiscc/AISCC_PUBLIC_RELEASE_MANIFEST_CANDIDATE.json`

Record:

```text
platform = Cloudflare Pages
project = aiscc-replay
deployment_method = Dashboard Direct Upload
production_url = https://aiscc-replay.pages.dev
source_commit = d13d261eb976fc839e78ba0878080bea93ad5201
public_verification = PASSED
live = false
```

No account ID/token.

### `.aiassistant/reports/aiscc/AISCC_COMPETITION_SUBMISSION_PACKAGE.md`

Replace service URL `PENDING_DEPLOYMENT` with:

`https://aiscc-replay.pages.dev`

Keep final submission status pending.

Do not change README/public Replay bytes/comparative evidence.

If any required verification fails, do not upgrade canonical release status.

## Human public URL QA guide

On full Executor PASS, generate:

`HUMAN_PUBLIC_URL_QA_GUIDE.md`

Korean Operation-oriented format.

Required Operations:

1. actual production URL landing;
2. Recorded identity;
3. four scenario outcomes;
4. Live disabled / no mutation control;
5. responsive 1080/1280/1440;
6. unknown scenario;
7. public real 404;
8. Browser Network: Cloudflare origin only;
9. visible private/internal data;
10. overall `ACCEPTED / REWORK`.

Do not require Human to inspect headers or hashes; Executor owns those.

## evidence artifacts

Create:

- `PUBLIC_HTTP_VERIFICATION.json`
- `PUBLIC_BYTE_IDENTITY.json`
- `PUBLIC_HEADER_VERIFICATION.json`
- `PUBLIC_RUNTIME_ISOLATION.json`
- `PUBLIC_404_VERIFICATION.json`
- `PUBLIC_TLS_ORIGIN.json`
- `POST_VERIFY_REPOSITORY_STATE.json`
- `VALIDATION.json`
- `HUMAN_PUBLIC_URL_QA_GUIDE.md` on full PASS

## evidence contract

executor_required:

- `PUBLIC_HTTP_RUNTIME`
  - required status/body checks;
- `PUBLIC_PROVENANCE`
  - exact byte identity to persisted source;
- `SECURITY_CONFORMANCE`
  - effective headers and runtime isolation;
- `REPOSITORY_CONFORMANCE`
  - zero source mutation;
- `DOC_STATE_RECONCILIATION`
  - only on full PASS.

reuse_allowed:

- Human Dashboard deployment evidence;
- Human local QA acceptance;
- persisted commit `d13d261eb976fc839e78ba0878080bea93ad5201`.

human_owned:

- final public URL visual/readability QA;
- rights/tool/model disclosure confirmation;
- final competition submission.

not_required:

- Cloudflare credential;
- Node/npm/Wrangler;
- DB;
- provider/LLM;
- Railway;
- Live.

forbidden:

- Cloudflare mutation;
- deployment retry;
- source rebuild/write;
- Git commit/push;
- Live enablement;
- final competition submit;
- requests to unrelated external origins.

proof_non_substitution:

- Dashboard success != public verification;
- HTTP 200 != byte identity;
- byte identity != header correctness;
- Executor verification != Human visual QA;
- deployed service != competition submission.

## terminal classification

Full PASS:

```text
PUBLIC_VERIFICATION_CANDIDATE / HUMAN_PUBLIC_QA_PENDING
```

Verification failure:

```text
PUBLIC_DEPLOYMENT_REWORK_REQUIRED
```

Do not declare final competition submission complete or P3-3 closed.

## export

Target:

`.aiassistant/reports/target/20260915_1310_aiscc-p3-3-cloudflare-public-endpoint-byte-header-and-runtime-verification-1/`

Required root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- evidence artifacts listed above
- changed canonical governance/readiness/submission records only if PASS
- `REMOVED_FILES.md` only for actual deletion, none expected.

Terminal ZIP:

`.aiassistant/reports/target/20260915_1310_aiscc-p3-3-cloudflare-public-endpoint-byte-header-and-runtime-verification-1.zip`

## final response

1. result
2. production origin
3. HTTP matrix
4. byte identity
5. effective headers
6. 404
7. runtime isolation
8. repository terminal state
9. changed canonical records
10. Human public QA
11. target bundle + ZIP
12. remaining final-submission blockers
