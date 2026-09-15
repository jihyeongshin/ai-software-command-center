# 작업지시서: P3-3 Cloudflare public endpoint verification baseline-corrected retry

## meta

- task_id: `20260915_1343_aiscc-p3-3-cloudflare-public-endpoint-verification-baseline-corrected-retry-1`
- created_at: `2026-09-15T13:43:11+09:00`
- work_type: `PUBLIC_VERIFICATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- fresh_ide_chat_required: `No`
- primary_semantic_owner: `P3-3 public deployment verification / Browser Command Center`

## correction from predecessor

The predecessor 1310 Task incorrectly required zero Git-visible untracked files.

Current accepted repository state contains exact governance provenance that MUST remain present.

Do not broad-clean it.

## required repository baseline

```text
branch = main
HEAD = d13d261eb976fc839e78ba0878080bea93ad5201
index = empty
tracked worktree = clean
```

Before this delivery, exact accepted pre-existing untracked inventory is:

- `.aiassistant/records/aiscc/cycles/20260915_1239_aiscc-p3-3-public-replay-persistence-accepted-cloudflare-deployment-entry-1.cycle.md`
  - SHA-256 `6a1fa922b800574f4736893a14c6db68add28aec676aa8cedf975ca1a95eecdd`
- `.aiassistant/records/aiscc/cycles/20260915_1310_aiscc-p3-3-human-dashboard-deployment-provided-public-verification-entry-1.cycle.md`
  - SHA-256 `fad91ccc70558d70ce476057e5a3456bf619736cf73fa3e7d98574b46321ebc9`
- `.aiassistant/reports/aiscc/20260915_1239_aiscc-browser-command-center-p3-3-cloudflare-pages-production-deployment-entry-handoff-1.md`
  - SHA-256 `b9e8ca56bc31b6e5f8518362c0d3d06c046f5aa7b79e6f0c7fc2b0db42d50805`
- `.aiassistant/reports/aiscc/20260915_1239_aiscc-p3-3-public-replay-persistence-browser-acceptance-1.md`
  - SHA-256 `ddf7a81905e283971166be92d3d0e37b125e83f4feed1315a8956c88b91cb354`
- `.aiassistant/reports/aiscc/20260915_1310_aiscc-browser-command-center-p3-3-public-endpoint-verification-entry-handoff-1.md`
  - SHA-256 `958fe755216fd306844603a2fc35c35b3edcf247f573fc4bb0f136ed4cb45230`
- `.aiassistant/reports/aiscc/20260915_1310_aiscc-p3-3-human-dashboard-deployment-browser-admission-1.md`
  - SHA-256 `ad053e775a01705e4f7bcc183eff4b25c237869152fede5f3a71d478c7d422df`
- `.aiassistant/tasks/done/20260915_1239_aiscc-p3-3-cloudflare-pages-direct-upload-production-deployment-and-public-verification-1.md`
  - SHA-256 `4e03c333ef9503754a64b5298708183efff5d9a498ea01a4ea384f5cff1fdaec`
- `.aiassistant/tasks/done/20260915_1310_aiscc-p3-3-cloudflare-public-endpoint-byte-header-and-runtime-verification-1.md`
  - SHA-256 `c97d17f66495d4e88b36d52743cd67c6deb18f46f9b4a987ec3d9a0eb17887ed`

After this delivery transport, these three current canonical files are additionally authorized:

- `.aiassistant/records/aiscc/cycles/20260915_1343_aiscc-p3-3-public-verification-baseline-contract-blocked-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260915_1343_aiscc-p3-3-public-verification-baseline-blocker-browser-judgment-1.md`
- `.aiassistant/reports/aiscc/20260915_1343_aiscc-browser-command-center-p3-3-public-verification-baseline-corrected-retry-entry-handoff-1.md`

The active Task is handled according to normal project task transport/lifecycle rules.

Therefore do NOT require `Git-visible untracked = 0`.

Instead verify:

1. every eight predecessor path above exists at exact SHA-256;
2. three inbound canonical authority files match delivery bytes;
3. no OTHER unexplained Git-visible modified/staged/untracked path exists.

If any unrelated extra path exists, STOP `DIRTY_WORKSPACE_MIXED`.

Do not delete or commit the authorized governance paths.

## exact public authority

```text
Cloudflare Pages project:
aiscc-replay

production origin:
https://aiscc-replay.pages.dev

Human Dashboard deployment:
PASS

deployment verification:
PENDING

source HEAD:
d13d261eb976fc839e78ba0878080bea93ad5201

canonical corpus root:
a870da635941d7149edbbef911e8b2d75ff6fe12e8ade80c09dddc9086df795e

Live:
false / DISABLED_FOR_INITIAL_RELEASE
```

## objective

Independently verify the actual public Cloudflare Pages origin against the persisted Human-accepted Public Replay artifact.

No public mutation is authorized.

## builder/source check

Run:

```text
python scripts/build_public_replay.py --check
```

PASS required.

Do not run builder write mode.

Verify local `public/replay/**` remains identical to Git commit `d13d261eb976fc839e78ba0878080bea93ad5201`.

## network boundary

Read-only HTTPS is authorized ONLY to:

`https://aiscc-replay.pages.dev`

Ordinary DNS/TLS infrastructure needed to reach this origin is implicit.

Forbidden:

- Cloudflare Dashboard/API;
- Wrangler;
- unrelated domains;
- provider/OpenAI/Railway;
- owner/private API;
- discovered external links/endpoints.

Do not follow external redirects.

If the production origin redirects to another materially different application origin, STOP `PUBLIC_ORIGIN_REDIRECT_CONFLICT`.

## required HTTP matrix

Verify:

```text
/                                         -> 200
/health.json                              -> 200
/data/REPLAY_CORPUS_INDEX.json            -> 200
/data/stockroom-s1-normal.json            -> 200
/data/stockroom-s2-missing-evidence.json  -> 200
/data/stockroom-s3-policy-conflict.json   -> 200
/data/stockroom-s4-human-owned-claim.json -> 200
/assets/app.js                            -> 200
/assets/styles.css                        -> 200
/404.html                                 -> 200
/does-not-exist                           -> 404
```

Record final URL, status, content type, body bytes, SHA-256, redirects.

Use `Accept-Encoding: identity` where practical.

## exact public byte identity

For each exact local persisted file below compare decoded HTTP response body bytes byte-for-byte:

- `index.html`
- `404.html`
- `health.json`
- `assets/app.js`
- `assets/styles.css`
- `data/REPLAY_CORPUS_INDEX.json`
- four scenario JSON files

Required corpus/index identity is exact.

No normalization, CRLF conversion, reserialization, or semantic-only comparison is allowed.

Create `PUBLIC_BYTE_IDENTITY.json`.

## health contract

Public `/health.json` must parse exactly:

```text
status = "ok"
mode = "RECORDED_RUN_REPLAY"
live = false
corpus_root_sha256 = "a870da635941d7149edbbef911e8b2d75ff6fe12e8ade80c09dddc9086df795e"
scenario_count = 4
owner_database = false
provider_inference = false
```

## effective security headers

For production `/`, verify semantics of:

```text
X-Content-Type-Options: nosniff
Referrer-Policy: no-referrer
X-Frame-Options: DENY

Permissions-Policy contains:
camera=()
microphone=()
geolocation=()
payment=()
usb=()

Content-Security-Policy contains:
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

Cache-Control contains:
no-cache
```

Header order/whitespace/case normalization may differ.

Any missing/materially weaker required directive => `PUBLIC_HEADER_VERIFICATION_FAILED`.

Record Cloudflare-added headers separately.

## 404

`GET /does-not-exist` must be actual HTTP 404.

PASS body must be truthful and must not imply execution success.

Record whether Cloudflare serves the authored `404.html` body or another truthful 404.

## content truth

Verify production landing contains the accepted meaning:

```text
AI Software Command Center
Recorded Run Replay
This is a recorded historical run.
Viewing it does not execute AI.
Live Demo is not enabled.
Recorded Run Replay remains available.
```

## runtime isolation

Inspect public HTML/JS/CSS and exact fetch targets.

Expected no references to:

- owner/private API;
- PostgreSQL;
- OpenAI/provider;
- Railway;
- analytics/tracker/CDN;
- active Live endpoint;
- file upload;
- repository URL input;
- free-form task execution;
- mutation forms/actions.

Expected same-origin Replay fetch set only:

```text
data/REPLAY_CORPUS_INDEX.json
data/stockroom-s1-normal.json
data/stockroom-s2-missing-evidence.json
data/stockroom-s3-policy-conflict.json
data/stockroom-s4-human-owned-claim.json
```

Do not query any unexpected external reference; record and fail.

## TLS/origin

Record non-invasive evidence:

- requested origin;
- final origin;
- HTTPS success;
- client certificate validation;
- redirect chain.

## canonical record updates — only on full PASS

If and only if ALL required verification passes, narrowly update:

### CURRENT_STATE_SUMMARY

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

### NEXT_ACTIONS

```text
1. Human public-URL final visual QA
2. rights/tool/model disclosure confirmation
3. public verification + Human QA persistence
4. final competition submission
5. judging-window availability monitoring
```

### AISCC_P3_3_PUBLIC_RELEASE_READINESS.md

Resolve public serving/deployment blockers with the exact verified origin/evidence.

### AISCC_PUBLIC_RELEASE_MANIFEST_CANDIDATE.json

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

No Cloudflare account identifiers or credentials.

### AISCC_COMPETITION_SUBMISSION_PACKAGE.md

Replace `PENDING_DEPLOYMENT` service URL with:

`https://aiscc-replay.pages.dev`

Keep final submission pending.

Do NOT modify:

- README;
- public/replay/**;
- canonical Replay source corpus;
- comparative result/protocol;
- P3-2 public docs;
- DECISION_REGISTER unless existing semantics are actually contradicted — no such change is expected.

If any required public check fails, do not update release status records.

## Human public URL QA guide

On full PASS create:

`HUMAN_PUBLIC_URL_QA_GUIDE.md`

Korean, Operation-oriented.

Operations:

1. production landing;
2. Recorded identity;
3. S1/S2/S3/S4 outcome;
4. Live disabled/no mutation;
5. responsive 1080/1280/1440;
6. unknown scenario;
7. real production 404;
8. browser Network external-origin boundary;
9. visible private/internal data;
10. overall ACCEPTED/REWORK.

Human does not need to repeat hash/header checks.

## terminal repository contract

Public verification must not modify application/public source.

At terminal:

- HEAD remains `d13d261eb976fc839e78ba0878080bea93ad5201`;
- index remains empty;
- no public/replay source byte changed;
- exact authorized governance provenance remains present;
- on PASS, only permitted canonical state/readiness/submission records may be tracked-modified;
- no unexplained new Git-visible path.

Target/export artifacts remain ignored according to project rules.

## required evidence artifacts

- `PUBLIC_HTTP_VERIFICATION.json`
- `PUBLIC_BYTE_IDENTITY.json`
- `PUBLIC_HEADER_VERIFICATION.json`
- `PUBLIC_RUNTIME_ISOLATION.json`
- `PUBLIC_404_VERIFICATION.json`
- `PUBLIC_TLS_ORIGIN.json`
- `POST_VERIFY_REPOSITORY_STATE.json`
- `VALIDATION.json`
- `HUMAN_PUBLIC_URL_QA_GUIDE.md` on PASS

## evidence contract

executor_required:
- PUBLIC_HTTP_RUNTIME
- PUBLIC_PROVENANCE / exact byte identity
- SECURITY_CONFORMANCE
- REPOSITORY_CONFORMANCE
- DOC_STATE_RECONCILIATION on PASS only

reuse_allowed:
- Human Dashboard deployment evidence
- Human local visual QA
- persisted source commit `d13d261eb976fc839e78ba0878080bea93ad5201`

human_owned:
- final public URL visual QA
- rights/tool/model roster confirmation
- final competition submission

not_required:
- Node/npm/Wrangler
- Cloudflare credentials
- DB/provider/Railway/OpenAI
- Live

forbidden:
- public mutation/deployment retry
- Cloudflare API/Dashboard
- source rebuild/write
- Git commit/push
- Live enablement
- final competition submit
- unrelated external requests

proof_non_substitution:
- deployed URL != verification PASS
- HTTP 200 != exact byte identity
- local `_headers` != effective public headers
- Executor public verification != Human visual QA
- public deployment != final competition submission

## terminal classification

Full PASS:

`PUBLIC_VERIFICATION_CANDIDATE / HUMAN_PUBLIC_QA_PENDING`

Any public verification defect:

`PUBLIC_DEPLOYMENT_REWORK_REQUIRED`

Repository authority mismatch:

named blocker / STOP before public requests.

## export

Target:

`.aiassistant/reports/target/20260915_1343_aiscc-p3-3-cloudflare-public-endpoint-verification-baseline-corrected-retry-1/`

Terminal ZIP:

`.aiassistant/reports/target/20260915_1343_aiscc-p3-3-cloudflare-public-endpoint-verification-baseline-corrected-retry-1.zip`

## final response

1. result
2. baseline/provenance allowance
3. production origin
4. HTTP matrix
5. byte identity
6. health
7. effective headers
8. 404
9. runtime isolation
10. repository terminal state
11. changed canonical records
12. Human public QA
13. target bundle + ZIP
14. remaining submission blockers
