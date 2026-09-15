# 작업지시서: P3-3 Cloudflare Pages Direct Upload production deployment and public verification

## meta

- task_id: `20260915_1239_aiscc-p3-3-cloudflare-pages-direct-upload-production-deployment-and-public-verification-1`
- created_at: `2026-09-15T12:39:23+09:00`
- work_type: `DEPLOYMENT`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- fresh_ide_chat_required: `No`
- primary_semantic_owner: `P3-3 Cloudflare Pages public deployment / Browser Command Center`

## exact baseline

Before any Cloudflare/network mutation verify:

```text
branch = main
HEAD = d13d261eb976fc839e78ba0878080bea93ad5201
index = empty
tracked worktree = clean
Git-visible untracked = 0
```

Run:

```text
python scripts/build_public_replay.py --check
```

Required result:

- PASS;
- corpus root `a870da635941d7149edbbef911e8b2d75ff6fe12e8ade80c09dddc9086df795e`;
- four scenarios;
- no output mutation.

If baseline or check differs, STOP before Cloudflare actions.

## deployment decision

This Task authorizes one bounded production deployment:

```text
platform:
Cloudflare Pages

deployment mode:
Direct Upload

requested project name:
aiscc-replay

production branch:
main

artifact directory:
public/replay

commit metadata:
d13d261eb976fc839e78ba0878080bea93ad5201

Live:
disabled
```

Do not reopen deployment-mode selection in this Task.

Known limitation:

Cloudflare Pages Direct Upload projects cannot later be converted to Git integration on the same project. This has been accepted for the competition release route.

## official Cloudflare command contract

Current Cloudflare documentation supports:

```text
npx wrangler whoami --json
npx wrangler pages project list --json
npx wrangler pages project create <PROJECT-NAME> --production-branch <BRANCH>
npx wrangler pages deploy <DIRECTORY> --project-name <PROJECT-NAME> --commit-hash <SHA>
npx wrangler pages deployment list --project-name <PROJECT-NAME> --environment production --json
```

Record the exact Wrangler version actually used.

Do not modify package.json/package-lock or install Wrangler into repository dependencies.

An ephemeral `npx` acquisition/cache is permitted and is not repository source.

## authentication gate

First execute:

```text
npx wrangler whoami --json
```

### authenticated

If command returns authenticated user/account information:

- record only non-secret account/display identifiers needed to disambiguate the selected account;
- never record OAuth/API token values;
- proceed.

### unauthenticated

If non-zero / not authenticated:

```text
STOP:
HUMAN_CLOUDFLARE_AUTH_REQUIRED
```

Do NOT run:

```text
wrangler login
```

automatically.

Do not create tokens.

Report the exact Human action required:

```text
Authenticate Wrangler to the intended Cloudflare account, then rerun this same deployment Task.
```

No project/deployment mutation is allowed after this STOP.

## account ambiguity

If `whoami` shows multiple accounts and the intended account cannot be determined from existing accepted repository authority:

```text
STOP:
HUMAN_CLOUDFLARE_ACCOUNT_SELECTION_REQUIRED
```

Do not choose an account by guessing.

## Pages project preflight

Run:

```text
npx wrangler pages project list --json
```

Inspect exact projects.

### existing `aiscc-replay`

If exact project name `aiscc-replay` exists:

- reuse it;
- record its current production branch and domains if returned;
- list existing production deployments;
- do not create a duplicate;
- if existing project identity clearly conflicts with AISCC or contains an unrelated production service, STOP `CLOUDFLARE_PROJECT_IDENTITY_CONFLICT`.

### no `aiscc-replay`

Creation is authorized:

```text
npx wrangler pages project create aiscc-replay --production-branch main
```

After creation, re-list project and verify exact name.

Do not silently accept another requested project name.

If Cloudflare returns a distinct platform-generated pages.dev domain due global hostname collision, record the actual domain returned; project name must still remain `aiscc-replay`.

## exact deployment artifact integrity

Immediately before deploy:

1. run `python scripts/build_public_replay.py --check`;
2. hash every file under `public/replay`;
3. compare the exact Human-accepted/persisted file set against Git commit `d13d261eb976fc839e78ba0878080bea93ad5201`;
4. verify Git blob/worktree byte identity for deployment directory;
5. verify no `functions/`, `_worker.js`, or other executable server runtime is inside the upload directory unless already part of accepted bytes — expected none.

Do not rebuild/write.

Do not edit deployment files.

Create target evidence:

`CLOUDFLARE_DEPLOYMENT_INPUT_MANIFEST.json`

with relative paths, bytes, SHA-256, Git blob identity where applicable, corpus root, source commit.

## production deploy

Deploy exactly:

```text
npx wrangler pages deploy public/replay \
  --project-name aiscc-replay \
  --commit-hash d13d261eb976fc839e78ba0878080bea93ad5201
```

Do not pass preview `--branch` for the production deploy.

Capture:

- exit code;
- Wrangler version;
- deployment ID if returned;
- project name;
- actual deployment URL;
- production URL/domain from returned/listed Cloudflare state;
- source commit metadata.

Do not print auth tokens or raw credential storage.

Run:

```text
npx wrangler pages deployment list \
  --project-name aiscc-replay \
  --environment production \
  --json
```

Confirm the new deployment is the production deployment corresponding to this Task.

If deploy command succeeds but production deployment identity cannot be proven, classify `DEPLOYED_UNVERIFIED` and STOP before public-release claim.

## public URL source

Use only URL/domain values returned by authenticated Cloudflare commands.

Never construct/guess `<name>.pages.dev` as evidence.

Normalize the verified production origin:

`https://<actual-production-domain>`

Record preview/deployment-specific URLs separately from the stable production origin.

## external public verification

After Cloudflare reports successful production deployment, perform read-only HTTPS requests against the actual production origin.

No browser automation is required.

### required status/body checks

Verify:

```text
/                              -> 200
/health.json                   -> 200
/data/REPLAY_CORPUS_INDEX.json -> 200
/data/stockroom-s1-normal.json -> 200
/data/stockroom-s2-missing-evidence.json -> 200
/data/stockroom-s3-policy-conflict.json -> 200
/data/stockroom-s4-human-owned-claim.json -> 200
/assets/app.js                 -> 200
/assets/styles.css             -> 200
/does-not-exist               -> 404
/404.html                      -> 200
```

### exact public-byte checks

Download exact bodies for:

- health;
- Replay index;
- four scenario JSON;
- app.js;
- styles.css;
- index.html where transport/content encoding permits exact raw-byte comparison.

Compare SHA-256 to persisted local artifact.

At minimum the five JSON corpus files MUST be exact byte matches.

If Cloudflare transport applies compression, hash the decoded HTTP body bytes returned by the client, not wire-compressed framing.

### health identity

Public `/health.json` must parse as:

```text
status = ok
mode = RECORDED_RUN_REPLAY
live = false
corpus_root_sha256 = a870da635941d7149edbbef911e8b2d75ff6fe12e8ade80c09dddc9086df795e
scenario_count = 4
owner_database = false
provider_inference = false
```

### effective security headers

For production `/` verify response includes exact/equivalent accepted policy:

```text
X-Content-Type-Options: nosniff
Referrer-Policy: no-referrer
X-Frame-Options: DENY
Permissions-Policy:
  camera=(), microphone=(), geolocation=(), payment=(), usb=()

Content-Security-Policy:
  default-src 'none';
  script-src 'self';
  style-src 'self';
  connect-src 'self';
  img-src 'self';
  font-src 'none';
  object-src 'none';
  base-uri 'none';
  frame-ancestors 'none';
  form-action 'none'

Cache-Control: no-cache
```

Cloudflare may normalize whitespace/order; compare semantics, not raw header formatting.

Any materially weaker/missing security directive => `PUBLIC_HEADER_VERIFICATION_FAILED`.

### content truth scan

Verify public landing body contains the meaning:

```text
Recorded Run Replay

This is a recorded historical run.
Viewing it does not execute AI.

Live Demo is not enabled.
Recorded Run Replay remains available.
```

Do not require exact punctuation if the persisted accepted HTML uses equivalent text.

### private/runtime isolation

Public HTML/JS requests and static content must not reference:

- owner/private API host;
- PostgreSQL;
- OpenAI/provider endpoint;
- Railway endpoint;
- upload/task/repository input;
- active Live execution endpoint.

No external network calls should be required by normal Replay page load other than the Cloudflare origin itself.

## custom 404 verification

Verify:

```text
/does-not-exist
```

returns actual HTTP 404.

Verify body is either the authored static 404 page or another truthful Cloudflare 404 that does not imply successful execution.

If Cloudflare does not serve the authored `404.html` for unknown paths but returns a truthful 404 status/body, record the difference. This is not automatically a blocker unless the result breaks Human-approved truthfulness or navigation.

## post-deploy repository boundary

Deployment must not mutate repository source.

After deployment verify:

```text
HEAD = d13d261eb976fc839e78ba0878080bea93ad5201
index = empty
tracked worktree = clean
Git-visible untracked = 0
```

Wrangler/npx ignored cache outside Git-visible workspace may be recorded as non-blocking local residue.

Do not delete credentials/cache as part of Task completion.

## canonical state updates after proven deployment

Only if production deployment + public verification PASS:

Update:

### CURRENT_STATE_SUMMARY

```text
Recorded Replay local implementation:
HUMAN_PROVIDED / ACCEPTED / PERSISTED

Public Replay deployment:
DEPLOYED / PUBLIC_VERIFICATION_PASSED

Public Replay production URL:
<actual verified URL>

Public Bounded Live:
NOT_RELEASED / DISABLED_FOR_INITIAL_RELEASE

P3-3:
ACTIVE / FINAL_SUBMISSION_PENDING
```

### NEXT_ACTIONS

```text
1. Human public-URL final visual QA
2. rights/tool/model disclosure confirmation
3. final competition submission
4. judging-window availability monitoring
```

### AISCC_P3_3_PUBLIC_RELEASE_READINESS.md

Narrow R01/R02 to resolved deployment evidence.

### AISCC_PUBLIC_RELEASE_MANIFEST_CANDIDATE.json

Add actual Cloudflare project/deployment/public URL identities without secret values.

### AISCC_COMPETITION_SUBMISSION_PACKAGE.md

Replace service URL `PENDING_DEPLOYMENT` with exact verified public production URL.

Do not mark final competition submission complete.

Do not change:

- README;
- public comparative docs;
- public Replay artifact bytes;
- P3-1 result semantics;
- Live classification.

If deployment/public verification does not fully PASS, do not upgrade these canonical release statuses.

## no Git persistence in this Task

Do not commit/push any post-deploy governance state changes.

A subsequent Browser judgment/Human public QA determines the exact persistence/final-submit path.

## required evidence artifacts

Target bundle must contain:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `CLOUDFLARE_AUTH_PREFLIGHT.json`
- `CLOUDFLARE_PROJECT_PREFLIGHT.json`
- `CLOUDFLARE_DEPLOYMENT_INPUT_MANIFEST.json`
- `CLOUDFLARE_DEPLOYMENT_RESULT.json`
- `CLOUDFLARE_PRODUCTION_DEPLOYMENT.json`
- `PUBLIC_HTTP_VERIFICATION.json`
- `PUBLIC_HEADER_VERIFICATION.json`
- `PUBLIC_BYTE_IDENTITY.json`
- `POST_DEPLOY_REPOSITORY_STATE.json`
- changed canonical governance/readiness/submission records if successful
- `HUMAN_PUBLIC_URL_QA_GUIDE.md` if successful
- `HOUSEKEEPING.json`

No credential/token values may appear.

## Human public URL QA guide

If deployment and Executor verification PASS, create a short Korean Operation-based guide covering:

1. production URL opens;
2. Recorded identity;
3. four scenario outcomes;
4. Live disabled;
5. responsive 1080/1280/1440;
6. unknown scenario;
7. real production 404;
8. browser Network external-origin check;
9. visible private/internal data;
10. final overall ACCEPTED/REWORK.

This is separate from Executor HTTP verification.

## evidence contract

executor_required:

### `CLOUDFLARE_AUTH`
- authenticated intended account or named Human blocker;
- no secret disclosure.

### `DEPLOYMENT`
- exact `public/replay` persisted bytes;
- exact Pages project identity;
- production deployment tied to commit `d13d261eb976fc839e78ba0878080bea93ad5201`.

### `PUBLIC_HTTP_RUNTIME`
- required public 200/404;
- exact Replay JSON byte identity;
- health identity;
- stable production URL obtained from Cloudflare evidence.

### `SECURITY_CONFORMANCE`
- effective headers;
- no Live/provider/owner/private dependency.

### `REPOSITORY_CONFORMANCE`
- deployment does not dirty source repository.

reuse_allowed:
- Human QA accepted local implementation;
- persistence commit `d13d261eb976fc839e78ba0878080bea93ad5201`;
- canonical corpus sanitization/provenance.

human_owned:
- Cloudflare authentication if absent;
- account disambiguation if ambiguous;
- post-deployment visual QA;
- rights/tool/model roster confirmation;
- final competition submission.

not_required:
- Railway;
- OpenAI/provider inference;
- DB;
- Live;
- Git push;
- custom domain.

forbidden:
- secret values in evidence;
- automatic `wrangler login`;
- alternate project-name guessing;
- Live enablement;
- source rebuild/edit;
- Railway/OpenAI resource creation;
- competition final submit.

proof_non_substitution:
- Wrangler deploy success != public verification;
- preview URL != stable production URL;
- production URL 200 != exact corpus identity;
- local headers file != effective public headers;
- public deployment != Human visual acceptance;
- public service != final competition submission.

## terminal classifications

### success

```text
DEPLOYMENT_CANDIDATE / HUMAN_PUBLIC_QA_PENDING
```

### authentication blocker

```text
BLOCKED_HUMAN_CLOUDFLARE_AUTH
```

### account ambiguity

```text
BLOCKED_HUMAN_CLOUDFLARE_ACCOUNT_SELECTION
```

### project conflict

```text
BLOCKED_CLOUDFLARE_PROJECT_IDENTITY_CONFLICT
```

### deployment/public verification failure

```text
DEPLOYMENT_REWORK_REQUIRED
```

Do not declare P3-3 closed or competition submitted.

## mandatory stop

Immediately stop Cloudflare mutation if:

- repo baseline fails;
- builder check fails;
- auth is absent;
- account identity is ambiguous;
- existing `aiscc-replay` is unrelated/conflicting;
- accepted deployment directory bytes differ from commit;
- secret disclosure would be required;
- deployment command targets a project other than exact `aiscc-replay`;
- public verification shows private/owner/Live dependency.

After stop, collect only minimal evidence/report/export.

## export

Target:

`.aiassistant/reports/target/20260915_1239_aiscc-p3-3-cloudflare-pages-direct-upload-production-deployment-and-public-verification-1/`

Terminal ZIP:

`.aiassistant/reports/target/20260915_1239_aiscc-p3-3-cloudflare-pages-direct-upload-production-deployment-and-public-verification-1.zip`

## final response

1. result
2. repository baseline
3. Wrangler version/auth classification
4. Cloudflare account/project identity
5. deployment ID/production URL
6. public HTTP verification
7. public byte identity
8. effective headers
9. repository terminal state
10. changed governance/readiness records
11. Human public QA status
12. target bundle + ZIP
13. remaining final-submission blockers
