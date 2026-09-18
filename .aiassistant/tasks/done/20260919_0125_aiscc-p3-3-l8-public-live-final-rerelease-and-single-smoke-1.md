# AISCC Task — L8 Final Public Live Re-release and Single Smoke

## meta

- task_id: `20260919_0125_aiscc-p3-3-l8-public-live-final-rerelease-and-single-smoke-1`
- phase: `P3-3 / L8`
- work_type: `FINAL_PUBLIC_LIVE_RERELEASE`
- execution_model: `THIN_CC_THICK_EXECUTOR`
- exact_baseline: `75ffc31ac20ff37fdd50bef9c9446fe0703cadfa`
- fresh_ide_chat_required: `No`
- Human_release_decision: `RELEASE_PUBLIC_LIVE`
- Railway_mutation_authority: `BOUNDED_RELEASE_ONLY`
- hosted_DB_mutation_authority: `EXACT_CONTROL_RELEASE_ONLY`
- Cloudflare_mutation_authority: `EXACT_ACCEPTED_FRONTEND_RELEASE_ONLY`
- public_run_authority: `EXACTLY_ONE_BOUNDED_SMOKE`
- real_provider_authority: `EXACTLY_ONE_PUBLIC_SMOKE_RUN_NORMAL_PATH`
- rollback_authority: `EXPLICIT`
- DB_migration_authority: `NONE`
- new_DB_login_role_authority: `NONE`
- temporary_Railway_SSH_key_authority: `ONE_EPHEMERAL_KEY_IF_REQUIRED`

## Goal

Re-release the already accepted bounded Public Live feature on:

`https://aiscc-replay.pages.dev/`

while preserving Recorded Run Replay and every accepted security/budget/governance boundary.

Success candidate:

```text
Recorded Run Replay:
AVAILABLE / UNCHANGED

Bounded Live:
RELEASED

scenario:
stockroom-s1-normal / 1.0.0 only

Public admission:
ENABLED

Public Live:
RELEASED

public smoke:
EXACTLY ONE / PASS
```

This Task performs activation of already accepted functionality. It does not authorize architecture redesign.

## Human authority

The Human explicitly selected:

`RELEASE_PUBLIC_LIVE`

No further Human approval is required for the exact operations authorized below.

Executor must still stop at any actual material boundary.

## frozen accepted baseline

### repository

`75ffc31ac20ff37fdd50bef9c9446fe0703cadfa`

### hosted DB

```text
migration head:
20260919_0024

reconciler compatibility:
run_context EXECUTE -> runtime + reconciler
project_run EXECUTE -> runtime + reconciler
PUBLIC EXECUTE -> revoked
broad/table reconciler authority -> absent
```

No migration is authorized in this Task.

### retained historical smoke

```text
1919:
FAILED_NOT_DISPATCHED
reservation SETTLED / cost 0
slot FREE
outbox CLOSED
held liability 0
```

Do not mutate or re-settle it.

### Public browser origin

`https://aiscc-replay.pages.dev`

### campaign

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
```

The campaign already exists from the accepted lineage.

Do not replace/recreate it if current immutable fields match.
If any immutable field differs, STOP.

### provider

```text
provider:
OpenAI

model:
gpt-5.6-luna

profile:
accepted hosted Luna Public Live profile
```

Provider credential must remain:
- present/sealed/service-local on worker only;
- absent from ingress;
- absent from initializer;
- absent from owner/API;
- absent from shared/project variable scope.

Never read/copy/export the credential value.

### Public Live tool

Current accepted Public Live runtime contract is:

```text
Tool Broker
→ TOOL capability only
→ PublicLiveFixedStockroomDispatcher
→ canonical STOCKROOM_SUMMARY
```

For the Public fixed tool:

```text
PROCESS capability: 0
FILESYSTEM capability: 0
tool NETWORK capability: 0
tool SECRET capability: 0
Docker dependency: 0
```

Do not reintroduce a Docker/process requirement for Public Live.

Owner/Self-Dogfood Docker execution is a separate accepted path and must remain unchanged.

## must preserve

- separate Public Live DB;
- hosted migration head `20260919_0024`;
- exact reconciler ACL compatibility;
- ingress least-privilege DB identity;
- worker-only provider secret;
- fixed scenario/profile/tool registry;
- exact Luna provider profile;
- accepted unknown-send quarantine/no-blind-resend semantics;
- accepted rate/budget/campaign limits;
- Replay independent from Live;
- Replay corpus and four recorded scenarios;
- same-tab sessionStorage capability design;
- exact browser Origin/CORS contract;
- one Railway ingress public origin only;
- no wildcard/general HTTPS CSP;
- governance truth remains server/Human-owned.

## must not do

- create a new persistent Railway service/database;
- change Railway plan/region/replica scale;
- create a DB migration;
- create a DB login/role;
- broaden DB grants;
- expose owner API/database;
- move/copy provider key to another service;
- create shared provider secret;
- change provider/model/profile/scenario;
- add free-form input;
- add admin/cancel routes;
- alter Replay corpus;
- broaden CSP to wildcard, `https:`, unsafe-inline, or unsafe-eval;
- custom provider fallback;
- delete historical campaign/run/provider evidence during rollback;
- create a second public smoke run;
- blind retry after UNKNOWN/ambiguous provider send;
- amend/rebase/force-push.

## temporary operator transport

If exact hosted DB control verification/activation requires operator access and no safe path already exists, at most one ephemeral Railway SSH key is authorized.

Rules:
- Task-only;
- never commit/export key material;
- no public DB TCP exposure;
- no provider/DB secret output;
- delete Railway key before completion;
- delete local private/public key and askpass helper before completion;
- prove cleanup by presence/count only.

Cleanup failure after release activity is a material failure: disable control and rollback to Replay-only before STOP.

## known Git push deployment coupling

A GitHub main push may rebuild repository-connected ingress/API services.

Before every push:
- control disabled;
- ingress/worker safety known;
- no claimable unexpected public work;
- no pending unknown provider outcome.

After passive deployment:
- verify service health;
- verify domains/edge trust are only the exact release bindings intended at that phase;
- verify provider secret isolation;
- verify no unintended run/provider side effects.

## required activation order

An equivalent mechanically different order is allowed only if it preserves the same security ordering.

### Phase A — exact preflight

Before mutation, freshly verify:

- `HEAD == origin/main == 75ffc31ac20ff37fdd50bef9c9446fe0703cadfa` except exact supplied governance placement;
- migration head `20260919_0024`;
- reconciler ACL matrix remains accepted;
- retained 1919 settlement durable;
- control disabled;
- active future-deadline public runs 0;
- claimable work 0;
- unreleased claims 0;
- open dispatch pins 0;
- provider requests 0;
- ingress/worker public domains 0;
- edge trust absent;
- worker secret isolation exact;
- fixed-tool worker deployment/runtime applicable;
- campaign immutable fields and zero stale held liability exact;
- Replay public/healthy and release-disabled frontend exact.

Any stale or broader authority => STOP before release mutation.

### Phase B — public ingress while still disabled

Using the existing `aiscc-public-live-ingress` only:

1. create exactly one Railway-generated HTTPS public domain;
2. record exact origin;
3. set/bind only the exact accepted ingress release-origin setting required by current source;
4. set exact accepted Railway edge-trust binding required by current source;
5. redeploy/restart ingress only as required;
6. verify health;
7. with control still disabled, verify valid public POST reaches the accepted safe disabled outcome and creates no run;
8. verify invalid Origin is denied;
9. verify no run/start/worker/provider side effect.

Do not continue if ingress is not fail-closed.

### Phase C — frontend release binding while backend disabled

Modify only the accepted release surface required by current source, expected to include:

- `public/replay/live-config.json`;
- `public/replay/_headers`;
- deterministic release/build manifest or directly affected test/docs if required;
- governance/provenance.

Required frontend semantic state:

```json
{
  "api_origin": "<EXACT_HTTPS_RAILWAY_INGRESS_ORIGIN>",
  "enabled": true,
  "schema": "AISCC-PUBLIC-LIVE-FRONTEND-CONFIG-V1"
}
```

Required CSP:
- preserve existing directives;
- `connect-src` allows only `'self'` plus the exact ingress origin;
- no other external network origin.

Then:

1. run directly affected frontend/Replay tests;
2. verify all four Replay scenario identities unchanged;
3. commit/push exact release config changes;
4. deploy exact artifact to the existing Cloudflare Pages project;
5. verify public page/config/CSP;
6. backend control must still be disabled.

A temporary UI-enabled/backend-disabled state is acceptable only during this controlled activation window.

### Phase D — final backend enablement

Only after A-C pass:

Use the accepted trusted hosted DB control owner to set the existing release state.

The final enable operation must preserve exact campaign identity and set only what current canonical contract requires, semantically:

```text
active_campaign = public-live-v1
policy_digest = accepted canonical digest
incident = NULL
enabled = true
```

Do not recreate the campaign.

Immediately re-read:
- control enabled true;
- active campaign exact;
- incident null;
- campaign/budget pins exact;
- slots/counts sane;
- no run exists yet from pre-enable checks.

This is the release activation point.

### Phase E — exactly one bounded end-to-end public smoke

Run **exactly one** Public Live smoke.

Use:
- actual released public ingress path;
- accepted browser Origin contract;
- exact `stockroom-s1-normal / 1.0.0`;
- exactly one new idempotency key.

Smoke requirements:

1. POST creates exactly one public run;
2. capability is used only for the same run and never exported/logged;
3. follow canonical GET/poll path;
4. initializer/worker perform canonical processing;
5. Public fixed in-process Stockroom tool is used;
6. only normal accepted provider behavior for this single run is permitted;
7. no manual/extra provider send;
8. no second public run;
9. no fallback provider/model;
10. resulting public/system projection must remain governance-truthful;
11. Replay remains usable.

If run reaches a valid unambiguous expected terminal/public state: smoke PASS candidate.

If provider/send state becomes `UNKNOWN` or ambiguous:
- DO NOT resend;
- DO NOT create another run;
- rollback immediately to Replay-only;
- preserve all evidence.

If any material smoke failure occurs:
- do not attempt a second smoke;
- rollback.

### Phase F — final public/security verification

After smoke candidate success, verify:

- Replay public URL succeeds;
- four Replay scenarios still load;
- visible release label truthfully shows Bounded Live configured/available;
- Start control enabled;
- exact frontend API origin;
- exact CSP self + ingress origin;
- ingress health succeeds;
- invalid Origin denied;
- no owner/admin routes exposed;
- campaign/control release state exact;
- provider secret isolation exact;
- migration head remains 0024;
- reconciler ACL remains exact;
- exactly one new smoke run;
- provider request/send evidence belongs only to that run;
- usage/cost stays inside accepted cap;
- no raw secret/capability/provider output in exported evidence.

## rollback contract

Rollback is authorized immediately after any material post-mutation failure.

Order:

1. `public_control.enabled=false` first.
2. restore frontend release-disabled state:
   - `enabled=false`;
   - `api_origin=null`;
   - CSP `connect-src 'self'`;
   - deploy Replay-only artifact.
3. remove ingress edge-trust release binding.
4. remove ingress public domain.
5. restore ingress release-origin setting to safe preactivation state if current source requires cleanup.
6. keep worker provider key sealed on worker unless a separate provider-security incident requires Human rotation.
7. preserve campaign/run/provider/settlement evidence.
8. remove temporary SSH access if created.
9. verify Replay public and Live fail-closed.

The existing campaign row may remain. `control disabled` is the release authority boundary.

Rollback result:

`RELEASE_ROLLED_BACK_TO_REPLAY_ONLY / BROWSER_REVIEW_REQUIRED`

## mandatory stop before enablement

STOP if:

- HEAD/baseline mismatch;
- migration head not 0024;
- reconciler ACL regresses;
- retained settlement regresses;
- campaign immutable pin conflict;
- stale held liability appears;
- public ingress not fail-closed;
- edge identity/trust contract cannot be proved;
- frontend needs broad CSP;
- Cloudflare deployment identity ambiguous;
- worker secret isolation changed;
- fixed-tool runtime applicability changed;
- provider account/profile readiness cannot be established without a new pre-release provider call;
- new semantic/security decision required;
- more DB privilege/migration/login/role needed.

## after-enable failure semantics

After enablement:
- any material failure => rollback first, then report;
- UNKNOWN/ambiguous send => no retry, no new run, rollback;
- do not leave a partially active release;
- do not improvise a second smoke.

## acceptance targets

Successful Executor candidate:

```text
PUBLIC_LIVE_RERELEASED
/
SINGLE_SMOKE_PASS
/
BROWSER_REVIEW_REQUIRED
/
HUMAN_PUBLIC_SITE_SMOKE_PENDING
```

Safe rollback candidate:

```text
RELEASE_ROLLED_BACK_TO_REPLAY_ONLY
/
BROWSER_REVIEW_REQUIRED
```

Pre-enable blocker:

```text
PUBLIC_LIVE_RERELEASE_BLOCKED
/
<EXACT_NAMED_BLOCKER>
/
BROWSER_REVIEW_REQUIRED
```

Executor must not mark L8 closed.

## Human-owned successor

If Browser accepts a successful release candidate, Human performs the final public-site smoke/visual verification.

Only after that evidence is accepted may Browser close L8.

## tests / verification

Before external activation:
- directly affected frontend tests;
- Replay build/check;
- Public Live ingress/config focused tests;
- `git diff --check`;
- Ruff/format/narrow mypy only if changed source requires it.

Do not rerun broad unrelated suites solely for reassurance.

## Git / persistence

- persist supplied Cycle/Judgment/Handoff;
- move this Task active -> done;
- release frontend config changes must be committed/pushed before final Cloudflare deploy;
- governance persistence may be a separate ordinary commit;
- no amend/rebase/force push;
- target bundle remains ignored/untracked.

## required export

Create:

`.aiassistant/reports/target/20260919_0125_aiscc-p3-3-l8-public-live-final-rerelease-and-single-smoke-1/`

Required root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `PREFLIGHT_SAFE_STATE.md`
- `PUBLIC_INGRESS_RELEASE_BINDING.md`
- `FRONTEND_CLOUDFLARE_RELEASE_PROOF.md`
- `CONTROL_ENABLEMENT.md`
- `PUBLIC_END_TO_END_SMOKE.md`
- `POST_RELEASE_SECURITY_STATE.md`
- `ROLLBACK_PROOF.md`
- `FINAL_PUBLIC_STATE.md`
- `TEMP_OPERATOR_ACCESS_PROOF.md`
- `WORKSPACE_STATE.md`
- changed files preserving exact repository-relative paths

Also create adjacent ZIP and report SHA-256.

Never export:
- OpenAI/provider key or masked identifier;
- HMAC key;
- DB credential/DSN;
- SSH private/public key material;
- read capability;
- raw provider output;
- private reasoning.

## final response format

1. result
2. target bundle path + ZIP SHA-256
3. product/release commit(s)
4. governance commit/push
5. ingress domain/deployment identity
6. Cloudflare deployment identity
7. control/campaign final state
8. single smoke run count/state
9. provider request/send count + bounded usage classification
10. temporary access cleanup
11. Replay status
12. unverified/Human-pending items
