# AISCC Task — L8 Final Public Live Activation and Smoke

## meta

- task_id: `20260918_1919_aiscc-p3-3-l8-public-live-final-activation-and-smoke-1`
- phase: `P3-3 / L8`
- work_type: `FINAL_PUBLIC_LIVE_ACTIVATION`
- execution_model: `THIN_CC_THICK_EXECUTOR`
- entry_commit: `0e9feab441352816d284d095f8c3a6863b8aa6a5`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- Human_release_decision: `RELEASE_PUBLIC_LIVE`
- Railway_mutation_authority: `BOUNDED_RELEASE_ONLY`
- hosted_DB_mutation_authority: `EXACT_CAMPAIGN_AND_CONTROL_ACTIVATION_ONLY`
- Cloudflare_mutation_authority: `EXACT_ACCEPTED_FRONTEND_RELEASE_ONLY`
- real_provider_authority: `ONE_BOUNDED_PUBLIC_SMOKE_RUN`
- rollback_authority: `EXPLICIT`

## Goal

Activate the already accepted bounded Public Live feature on the existing public site:

`https://aiscc-replay.pages.dev/`

while preserving Recorded Run Replay and all frozen security/budget/governance boundaries.

Successful end state:

```text
Recorded Run Replay:
AVAILABLE

Bounded Live:
RELEASED

scenario:
stockroom-s1-normal / 1.0.0 only

Public admission:
ENABLED

Public Live:
RELEASED

Replay:
UNCHANGED / AVAILABLE
```

This is activation of accepted functionality, not architecture redesign.

## Human authority

The Human explicitly selected:

`RELEASE_PUBLIC_LIVE`

No further Human approval is required for the exact operations authorized by this Task.

Stop only at an actual material boundary listed below.

## Frozen release values

### Public browser origin

`https://aiscc-replay.pages.dev`

### Campaign

```text
campaign_id:
public-live-v1

hmac_version:
v1

scenario_id:
stockroom-s1-normal

scenario_version:
1.0.0

campaign budget:
15,000,000 micro-USD ($15)

per-run reservation:
200,000 micro-USD ($0.20)

daily budget:
4,000,000 micro-USD ($4)

global admissions/day:
20

concurrency:
2

client:
3/hour
10/day

campaign cutoff exclusive:
2026-10-17T15:00:00Z
(2026-10-18 00:00:00 KST)
```

Campaign `starts_at` is the hosted DB clock at actual release preparation time. Do not invent a historical start time.

Campaign `policy_digest` must be derived from canonical `StartContract.load().digest`.

Campaign `content_digest` must be derived from canonical accepted Public Live resource/profile identity (`hosted_luna_profile().public_repository_version` / `RESOURCE_VERSION`) and must match the already accepted source pins.

Do not manually substitute copied digest literals when canonical source can derive them.

### Railway edge trust

Exact accepted value:

```text
AISCC_PUBLIC_LIVE_RAILWAY_EDGE_TRUST=
HOSTED_OVERWRITE_PROOF_ACCEPTED_V1
```

### Provider credential

`AISCC_OPENAI_API_KEY` must remain:
- present/sealed on `aiscc-public-live-worker`;
- absent from ingress;
- absent from initializer;
- absent from owner API;
- not project/shared.

## Must preserve

- separate Public Live DB;
- migration head `20260918_0023`;
- ingress least-privilege DB identity;
- worker-only provider secret;
- no owner/private DB route;
- fixed scenario/profile/tool registry;
- exact `gpt-5.6-luna` profile;
- accepted unknown-send quarantine/no-blind-resend semantics;
- accepted rate/budget/campaign limits;
- Replay independent of Live;
- Replay corpus bytes and four recorded scenarios;
- same-tab sessionStorage capability design;
- exact browser Origin/CORS contract;
- exact one Railway ingress origin;
- no wildcard/general HTTPS CSP;
- governance state remains server/Human-owned.

## Must not do

- create new persistent Railway services/databases;
- change Railway plan/region/replica scale;
- broaden DB roles/grants;
- run a migration;
- expose owner API/DB;
- put provider key on any service except worker;
- create project/shared provider secret;
- change model/provider/profile/scenario;
- add free-form input;
- add admin/cancel routes;
- alter Replay corpus;
- broaden CSP to wildcard, `https:`, unsafe-inline or unsafe-eval;
- use custom provider fallback;
- delete campaign/run/provider evidence during rollback;
- amend/rebase/force push.

## Allowed mutations

### Railway

Existing `aiscc-public-live-ingress` only:
- create one Railway-generated public HTTPS domain;
- set/update `PUBLIC_LIVE_API_ORIGIN` to that exact origin;
- set `AISCC_PUBLIC_LIVE_RAILWAY_EDGE_TRUST=HOSTED_OVERWRITE_PROOF_ACCEPTED_V1`;
- redeploy as required;
- remove those release bindings during rollback.

Existing worker/initializer:
- normal restart/redeploy caused by release-safe existing configuration only when necessary;
- do not alter provider secret scope or service authority.

### Hosted DB

Exact release preparation/activation only:
- insert the fixed `public-live-v1` campaign if absent;
- set `public_control.policy_digest`;
- set `public_control.active_campaign`;
- set `public_control.enabled=true` as the final backend activation step.

No other row mutation is authorized except runtime mutations caused by the single bounded smoke run and canonical worker/initializer processing.

If campaign already exists:
- proceed only if every immutable pin/budget/time field matches the frozen release contract;
- otherwise STOP.

### Repository/frontend

Allowed release config changes:
- `public/replay/live-config.json`;
- `public/replay/_headers`;
- deterministic Replay build manifest/artifacts required by those bytes;
- directly affected tests/docs;
- governance/provenance artifacts.

Required final frontend config:

```json
{
  "api_origin": "<EXACT_HTTPS_RAILWAY_INGRESS_ORIGIN>",
  "enabled": true,
  "schema": "AISCC-PUBLIC-LIVE-FRONTEND-CONFIG-V1"
}
```

Required CSP:
- preserve all current directives;
- `connect-src` must allow only `'self'` plus the exact Railway ingress origin.

No other external network origin.

### Cloudflare

Deploy the exact final static artifact to the existing Replay Pages project.

No new Pages project/domain.

## Required activation order

Use this ordering unless an equivalent ordering is demonstrably safer and preserves the same boundaries.

### Phase A — Preflight

Before mutations verify:
- HEAD/origin main exact entry commit;
- Replay public URL healthy;
- ingress currently private;
- edge trust absent;
- DB head `0023`;
- control disabled;
- campaign absent or exact-identical;
- worker secret present/sealed presence-only;
- provider key absent on API/initializer/ingress;
- worker/initializer/ingress healthy enough to continue.

Any unexpected broader authority => STOP.

### Phase B — Public ingress while still disabled

1. Create one Railway-generated HTTPS domain for existing ingress.
2. Record exact origin.
3. Set `PUBLIC_LIVE_API_ORIGIN` to that exact origin.
4. Set exact edge-trust accepted value.
5. Redeploy ingress.
6. Verify `/health` HTTP 200.
7. With control still disabled, verify public POST cannot create a run and returns the expected safe disabled state.
8. Verify invalid Origin is denied.
9. Verify no run/start/provider/worker side effects.

Do not continue if the public ingress is not fail-closed.

### Phase C — Materialize campaign while disabled

Using a task-owned trusted private DB activation mechanism:

- derive canonical policy/content digests from current source;
- insert exact `public-live-v1` row only if absent;
- `starts_at = DB clock at release preparation`;
- `ends_at = 2026-10-17T15:00:00Z`;
- `limit_micro = 15000000`;
- `available = 15000000`;
- `held = 0`;
- `settled = 0`;
- exact HMAC/scenario/version/digests.

Keep `public_control.enabled=false`.

Set active campaign/policy only if doing so while disabled is required for clean final activation; enabled must remain false.

Re-read and prove exact immutable values.

Do not fabricate a daily row; canonical admission owns runtime daily ledger creation unless current accepted DB semantics explicitly require otherwise.

### Phase D — Frontend release binding

1. Bind exact ingress origin in `live-config.json`.
2. Set `enabled=true`.
3. Add exact ingress origin to CSP `connect-src`.
4. Run deterministic Replay build/check.
5. Verify four Replay corpus identities unchanged.
6. Run frontend/H5/regression tests.
7. Commit/push exact frontend release-config changes.
8. Deploy exact artifact to existing Cloudflare Pages project.
9. Verify public page still loads Replay and serves exact new config/CSP.

At this point backend control is still disabled.

A brief state where UI is enabled but backend returns safe `LIVE_DISABLED` is acceptable during controlled activation; do not hide or fabricate success.

### Phase E — Final backend enablement

Only after A-D pass:

Atomically/set in the trusted hosted DB control owner:

```text
active_campaign = public-live-v1
policy_digest = canonical StartContract digest
incident = NULL
enabled = true
```

Immediately re-read:
- control enabled true;
- active campaign exact;
- incident null;
- campaign exact;
- slots/rate/budget invariants sane.

This is the release activation point.

### Phase F — One bounded end-to-end public smoke

Run exactly one public Live smoke for the fixed scenario.

Use the actual released public API path and accepted browser-origin contract.

Smoke must:
- POST exact scenario/version with one idempotency key;
- capture 201 capability without exporting it to report/log;
- follow GET using the capability;
- allow initializer/worker canonical processing;
- permit only the normal accepted provider call budget for this single run;
- never manually duplicate provider sends;
- stop on unknown outcome according to accepted production semantics;
- verify no second public run is created accidentally;
- verify resulting public projection remains governance-truthful;
- verify Replay remains usable.

Do not export read capability or raw provider output.

If the public run reaches a valid non-ambiguous terminal/public state, PASS.

If the run is UNKNOWN according to accepted semantics, do not resend; treat release smoke as BLOCKED and rollback to Replay-only.

### Phase G — final public verification

Verify from the public internet:

- `https://aiscc-replay.pages.dev/` returns successfully;
- all four Recorded Run Replay scenarios still load;
- release note says Bounded Live configured;
- Start control is enabled in a normal session-storage-capable browser/runtime proof;
- frontend config references exactly the ingress origin;
- CSP permits exactly self + ingress origin;
- ingress `/health` succeeds;
- invalid Origin denied;
- no owner/admin routes appear;
- campaign/control current release state correct;
- worker secret isolation still correct;
- project spend remains below hard cap;
- no unexpected additional provider run/request evidence;
- no raw secret/capability in logs/export.

## Rollback contract

Rollback is authorized immediately on any material post-mutation failure.

Rollback order:

1. `public_control.enabled=false` first.
2. restore frontend to release-disabled:
   - `enabled=false`;
   - `api_origin=null`;
   - CSP `connect-src 'self'`;
   - deploy Replay-only artifact.
3. remove ingress edge-trust variable.
4. remove ingress public domain when not needed for investigation.
5. restore ingress release origin setting to safe preactivation form if needed.
6. leave worker provider key sealed on worker unless a provider-security incident specifically requires separate Human rotation.
7. preserve campaign/run/provider evidence; do not delete it.
8. verify Replay public and Live fail-closed.

A rollback may leave the campaign row present and immutable; control disabled is the authority boundary.

Report rollback as `RELEASE_ROLLED_BACK_TO_REPLAY_ONLY`.

## Stop boundary

STOP before final enablement if:
- DB head/role differs;
- campaign conflicts with frozen pins;
- public ingress cannot be proven fail-closed;
- edge identity proof no longer holds;
- frontend requires broad CSP;
- Cloudflare deployment identity is ambiguous;
- worker secret isolation changed;
- provider account becomes blocked;
- new semantic/security policy is needed.

After enablement:
- material smoke failure => rollback immediately, then report;
- UNKNOWN provider/send outcome => no retry/new run, rollback to Replay-only;
- do not leave a partially activated state.

Do not STOP for:
- CLI syntax/mechanism differences;
- need for task-owned temporary private DB activator/verifier;
- generated Railway domain name;
- deterministic build artifact regeneration;
- passive unrelated Railway autodeploy observation.

## Acceptance target

Return one of:

```text
PUBLIC_LIVE_RELEASED / BROWSER_HUMAN_FINAL_SMOKE_PENDING
```

or

```text
RELEASE_ROLLED_BACK_TO_REPLAY_ONLY
```

or the narrowest pre-enable blocker.

Executor must not mark L8 closed. Browser/Human performs final judgment.

## Evidence expected

Required channels:

- `HUMAN_RELEASE_DECISION_PROVENANCE`
- `PREFLIGHT_SAFE_STATE`
- `PUBLIC_INGRESS_RELEASE_BINDING`
- `CAMPAIGN_MATERIALIZATION`
- `FRONTEND_RELEASE_BINDING`
- `CLOUDFLARE_DEPLOYMENT`
- `CONTROL_ENABLEMENT`
- `PUBLIC_END_TO_END_SMOKE`
- `POST_RELEASE_SECURITY_STATE`
- `ROLLBACK_READINESS`
- `FINAL_PUBLIC_STATE`

Evidence must include exact:
- Railway ingress service/domain/deployment IDs;
- environment variable presence/classification, never secret values;
- campaign/control non-secret row facts;
- frontend config/CSP;
- Cloudflare deployment identity;
- public HTTP status/results;
- run count and sanitized state lineage;
- provider request count/usage classification;
- Git commit(s)/changed paths;
- final admission/release state.

## Tests / verification

Before external activation:
- directly affected frontend tests;
- public Replay build/check;
- Public Live ingress/config tests;
- `git diff --check`;
- Ruff/format/narrow mypy where changed Python exists.

Do not rerun broad unrelated suites solely for reassurance.

## Git / persistence

- verify entry HEAD and origin/main;
- persist supplied Cycle/Judgment/Handoff;
- move this Task active -> done;
- release frontend config changes must be committed/pushed before Cloudflare final deploy;
- governance persistence may be a separate ordinary commit;
- no amend/rebase/force-push.

## export

Create:

`.aiassistant/reports/target/20260918_1919_aiscc-p3-3-l8-public-live-final-activation-and-smoke-1/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `PREFLIGHT_SAFE_STATE.md`
- `PUBLIC_INGRESS_RELEASE_BINDING.md`
- `CAMPAIGN_ACTIVATION_PROOF.md`
- `FRONTEND_CLOUDFLARE_RELEASE_PROOF.md`
- `PUBLIC_END_TO_END_SMOKE.md`
- `POST_RELEASE_SECURITY_STATE.md`
- `ROLLBACK_PROOF.md`
- `FINAL_PUBLIC_STATE.md`
- `WORKSPACE_STATE.md`
- changed files preserving exact project-relative paths

Also create:

`.aiassistant/reports/target/20260918_1919_aiscc-p3-3-l8-public-live-final-activation-and-smoke-1.zip`

Verify archive integrity and report SHA-256.

Never export:
- OpenAI API key;
- HMAC key;
- DB credentials/DSN;
- read capability;
- raw provider output;
- chain-of-thought/private reasoning.
