# 작업지시서: P3-3 Cloudflare public verification browser-signature-corrected retry

## meta

- task_id: `20260915_1358_aiscc-p3-3-cloudflare-public-verification-browser-signature-corrected-retry-1`
- created_at: `2026-09-15T13:58:56+09:00`
- work_type: `PUBLIC_VERIFICATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- fresh_ide_chat_required: `No`
- primary_semantic_owner: `P3-3 public endpoint verification / Browser Command Center`

## objective

Repeat the public verification against the already-deployed Cloudflare Pages production origin using a fixed browser-compatible anonymous HTTP request profile.

The previous Python-urllib default client was blocked by Cloudflare error `1010` before application content was served.

This retry changes only verification-client request headers.

## exact origin

`https://aiscc-replay.pages.dev`

No other application/API origin is authorized.

## repository baseline

Before network access verify:

```text
branch = main
HEAD = d13d261eb976fc839e78ba0878080bea93ad5201
index = empty
tracked worktree = clean
```

Expected pre-existing Git-visible governance provenance is exactly these 12 path/hash pairs:

- `.aiassistant/records/aiscc/cycles/20260915_1239_aiscc-p3-3-public-replay-persistence-accepted-cloudflare-deployment-entry-1.cycle.md`
  - SHA-256 `6a1fa922b800574f4736893a14c6db68add28aec676aa8cedf975ca1a95eecdd`
- `.aiassistant/records/aiscc/cycles/20260915_1310_aiscc-p3-3-human-dashboard-deployment-provided-public-verification-entry-1.cycle.md`
  - SHA-256 `fad91ccc70558d70ce476057e5a3456bf619736cf73fa3e7d98574b46321ebc9`
- `.aiassistant/records/aiscc/cycles/20260915_1343_aiscc-p3-3-public-verification-baseline-contract-blocked-retry-entry-1.cycle.md`
  - SHA-256 `0c47278311fc099802d7d50ea3c2d499245fb2b9b71c801b7ea297af9d9ac279`
- `.aiassistant/reports/aiscc/20260915_1239_aiscc-browser-command-center-p3-3-cloudflare-pages-production-deployment-entry-handoff-1.md`
  - SHA-256 `b9e8ca56bc31b6e5f8518362c0d3d06c046f5aa7b79e6f0c7fc2b0db42d50805`
- `.aiassistant/reports/aiscc/20260915_1239_aiscc-p3-3-public-replay-persistence-browser-acceptance-1.md`
  - SHA-256 `ddf7a81905e283971166be92d3d0e37b125e83f4feed1315a8956c88b91cb354`
- `.aiassistant/reports/aiscc/20260915_1310_aiscc-browser-command-center-p3-3-public-endpoint-verification-entry-handoff-1.md`
  - SHA-256 `958fe755216fd306844603a2fc35c35b3edcf247f573fc4bb0f136ed4cb45230`
- `.aiassistant/reports/aiscc/20260915_1310_aiscc-p3-3-human-dashboard-deployment-browser-admission-1.md`
  - SHA-256 `ad053e775a01705e4f7bcc183eff4b25c237869152fede5f3a71d478c7d422df`
- `.aiassistant/reports/aiscc/20260915_1343_aiscc-browser-command-center-p3-3-public-verification-baseline-corrected-retry-entry-handoff-1.md`
  - SHA-256 `20abf9b6efea4343f76ad1239d9768b20540075acb9d8624c0fba3128bdf76f8`
- `.aiassistant/reports/aiscc/20260915_1343_aiscc-p3-3-public-verification-baseline-blocker-browser-judgment-1.md`
  - SHA-256 `39a5aca6d21dec725ed85c11c931bf04d4194f3c00550edbd0255db77a7c394c`
- `.aiassistant/tasks/done/20260915_1239_aiscc-p3-3-cloudflare-pages-direct-upload-production-deployment-and-public-verification-1.md`
  - SHA-256 `4e03c333ef9503754a64b5298708183efff5d9a498ea01a4ea384f5cff1fdaec`
- `.aiassistant/tasks/done/20260915_1310_aiscc-p3-3-cloudflare-public-endpoint-byte-header-and-runtime-verification-1.md`
  - SHA-256 `c97d17f66495d4e88b36d52743cd67c6deb18f46f9b4a987ec3d9a0eb17887ed`
- `.aiassistant/tasks/done/20260915_1343_aiscc-p3-3-cloudflare-public-endpoint-verification-baseline-corrected-retry-1.md`
  - SHA-256 `96061074b8638dbb9e7f4d851a868a6d76af388d87a417ca911870bbc4ebc17d`

After delivery transport, the new Cycle/Judgment/Handoff are additional authorized provenance and the active Task follows normal ignored-task lifecycle.

Any extra unexplained Git-visible dirt or hash mismatch => STOP.

Do not delete/clean/commit authorized governance provenance.

Run:

```text
python scripts/build_public_replay.py --check
```

PASS is required.

## reused diagnostic evidence

Do NOT repeat the Python-urllib default-UA 11-request run.

Reuse predecessor evidence:

```text
default urllib UA -> Cloudflare 403 / error 1010
```

This is diagnostic evidence only.

## browser-compatible profile gate

Probe only:

`GET https://aiscc-replay.pages.dev/`

No cookies.

No authentication.

No Cloudflare challenge bypass.

Use `Accept-Encoding: identity`.

### Profile A — Chromium-compatible

Use these exact semantic request headers:

```text
User-Agent:
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36

Accept:
text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8

Accept-Language:
en-US,en;q=0.9

Accept-Encoding:
identity

Upgrade-Insecure-Requests:
1
```

### Profile B — Firefox-compatible fallback

Profile B may be attempted ONLY if Profile A receives Cloudflare `403` with body containing `error code: 1010`.

```text
User-Agent:
Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:155.0) Gecko/20100101 Firefox/155.0

Accept:
text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8

Accept-Language:
en-US,en;q=0.5

Accept-Encoding:
identity

Upgrade-Insecure-Requests:
1
```

Do not add cookies, authorization, Referer, spoofed Cloudflare headers, or challenge tokens.

## gate outcomes

### one profile reaches application

Choose the FIRST profile that returns expected application content/status.

Freeze that profile for all subsequent requests in this Task.

Do not alternate profiles per endpoint.

Record:

`PUBLIC_BROWSER_SIGNATURE_DIAGNOSTIC.json`

with:
- reused predecessor default-UA result;
- Profile A root result;
- Profile B result if applicable;
- selected profile;
- no cookie/auth state.

### both profiles receive 1010

STOP:

```text
PUBLIC_BROWSER_INTEGRITY_POLICY_BLOCK
```

Do not disable Browser Integrity Check.

Do not mutate Cloudflare.

Do not perform the remaining endpoint matrix.

Human action after STOP:

1. open `https://aiscc-replay.pages.dev` in a normal browser;
2. report whether the landing renders;
3. Browser Command Center then decides whether the verifier or Cloudflare policy needs adjustment.

### another unexpected root error

STOP:

`PUBLIC_ORIGIN_UNEXPECTED_RESPONSE`

Preserve body/headers without exploring unrelated origins.

## endpoint verification after profile selection

Using the single selected browser-compatible profile verify:

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

For non-HTML files keep the selected User-Agent and anonymous/no-cookie state. Accept may be narrowed to the appropriate MIME type, but this MUST be deterministic and recorded.

Do not follow any Report-To/NEL endpoint.

## exact public byte identity

Compare decoded response bytes against persisted local files.

Required exact match:

- index.html
- health.json
- REPLAY_CORPUS_INDEX.json
- all four scenario JSON files
- app.js
- styles.css
- 404.html

Record SHA-256, bytes and match bool.

If actual application content is reached and any body differs, classify actual byte mismatch.

## health contract

Public `/health.json`:

```text
status = "ok"
mode = "RECORDED_RUN_REPLAY"
live = false
corpus_root_sha256 = "a870da635941d7149edbbef911e8b2d75ff6fe12e8ade80c09dddc9086df795e"
scenario_count = 4
owner_database = false
provider_inference = false
```

## effective application headers

Validate only from successful application `/` response, not a Cloudflare error page.

Required:

```text
X-Content-Type-Options: nosniff
Referrer-Policy: no-referrer
X-Frame-Options: DENY

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

Whitespace/order normalization is allowed.

## 404

`/does-not-exist` must return actual 404.

The body must be truthful and must not imply AI execution.

## runtime isolation

Inspect served HTML/JS/CSS and selected same-origin fetch targets.

No:
- owner/private API;
- PostgreSQL;
- OpenAI/provider endpoint;
- Railway;
- external analytics/CDN;
- active Live endpoint;
- repository URL input;
- file upload;
- free-form task execution.

Normal Replay data requests must stay same-origin.

## security-setting boundary

Do NOT:

- disable Browser Integrity Check;
- change Security settings;
- add custom domain;
- mutate Pages project;
- redeploy;
- authenticate to Cloudflare;
- use API tokens;
- use browser automation that stores authenticated Cloudflare session state.

This is public anonymous verification only.

## canonical reconciliation — full PASS only

On full PASS, narrow-update:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
- `.aiassistant/reports/aiscc/AISCC_P3_3_PUBLIC_RELEASE_READINESS.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_RELEASE_MANIFEST_CANDIDATE.json`
- `.aiassistant/reports/aiscc/AISCC_COMPETITION_SUBMISSION_PACKAGE.md`

State:

```text
Public Replay deployment:
DEPLOYED / PUBLIC_VERIFICATION_PASSED

Production URL:
https://aiscc-replay.pages.dev

Live:
NOT_RELEASED / DISABLED_FOR_INITIAL_RELEASE

P3-3:
ACTIVE / HUMAN_PUBLIC_QA_PENDING
```

Do not mark competition submission complete.

Do not modify README, public/replay bytes, canonical Replay corpus, P3-1/P3-2 accepted docs.

## Human public QA guide

On full PASS generate Korean Operation-oriented:

`HUMAN_PUBLIC_URL_QA_GUIDE.md`

Operations:

1. production landing;
2. Recorded identity;
3. four scenario outcomes;
4. Live disabled/no mutation;
5. responsive 1080/1280/1440;
6. unknown selector;
7. real public 404;
8. browser Network expected Cloudflare origin only;
9. visible private/internal data;
10. overall ACCEPTED/REWORK.

Human does not repeat hashes/headers.

## required evidence

- `PUBLIC_BROWSER_SIGNATURE_DIAGNOSTIC.json`
- `PUBLIC_HTTP_VERIFICATION.json`
- `PUBLIC_BYTE_IDENTITY.json`
- `PUBLIC_HEADER_VERIFICATION.json`
- `PUBLIC_RUNTIME_ISOLATION.json`
- `PUBLIC_404_VERIFICATION.json`
- `PUBLIC_TLS_ORIGIN.json`
- `POST_VERIFY_REPOSITORY_STATE.json`
- `VALIDATION.json`
- `HUMAN_PUBLIC_URL_QA_GUIDE.md` only on full PASS

## evidence contract

executor_required:

- browser-signature diagnostic;
- exact application endpoint statuses;
- public/local byte identity;
- successful-response effective headers;
- 404;
- runtime isolation;
- repository conformance.

reuse_allowed:

- prior Cloudflare 1010 diagnostic;
- Human Dashboard deployment evidence;
- local Human QA;
- persisted source commit.

human_owned:

- final public URL visual QA;
- any Cloudflare security-policy decision if both browser profiles still fail;
- rights/tool/model disclosure;
- final competition submission.

forbidden:

- Cloudflare mutation;
- BIC disable;
- deployment retry;
- source mutation;
- Git commit/push;
- Live enablement;
- unrelated network origins;
- final submission.

## terminal classifications

Full PASS:

`PUBLIC_VERIFICATION_CANDIDATE / HUMAN_PUBLIC_QA_PENDING`

Both browser profiles 1010:

`PUBLIC_BROWSER_INTEGRITY_POLICY_BLOCK`

Other public verification defect:

`PUBLIC_DEPLOYMENT_REWORK_REQUIRED`

## export

Target:

`.aiassistant/reports/target/20260915_1358_aiscc-p3-3-cloudflare-public-verification-browser-signature-corrected-retry-1/`

Terminal ZIP:

`.aiassistant/reports/target/20260915_1358_aiscc-p3-3-cloudflare-public-verification-browser-signature-corrected-retry-1.zip`

## final response

1. result
2. selected browser profile or blocker
3. production origin
4. HTTP matrix
5. byte identity
6. effective headers
7. 404
8. runtime isolation
9. repository state
10. changed canonical records
11. Human public QA status
12. target bundle + ZIP
13. remaining submission blockers
