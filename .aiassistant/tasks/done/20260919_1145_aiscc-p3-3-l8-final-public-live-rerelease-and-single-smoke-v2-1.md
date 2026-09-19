# AISCC Task — L8 Final Public Live Re-release and Single Smoke V2

## meta

- task_id: `20260919_1145_aiscc-p3-3-l8-final-public-live-rerelease-and-single-smoke-v2-1`
- phase: `P3-3 / L8`
- work_type: `FINAL_PUBLIC_LIVE_RERELEASE_V2`
- execution_model: `THIN_CC_THICK_EXECUTOR`
- exact_baseline: `ade1ccdfd6248e264dddbe98cf77371e9189a3d6`
- fresh_ide_chat_required: `No`
- Human_release_decision: `RELEASE_PUBLIC_LIVE`
- Public_Live_entry_state: `NOT_RELEASED`
- Railway_mutation_authority: `BOUNDED_RELEASE_ONLY`
- hosted_DB_mutation_authority: `EXACT_CONTROL_RELEASE_ONLY`
- Cloudflare_mutation_authority: `EXACT_ACCEPTED_FRONTEND_RELEASE_ONLY`
- public_run_authority: `EXACTLY_ONE_BOUNDED_SMOKE_RUN`
- real_provider_authority: `CANONICAL_SINGLE_RUN_NORMAL_PATH_ONLY`
- provider_manual_send_authority: `NONE`
- provider_blind_retry_authority: `NONE`
- rollback_authority: `EXPLICIT`
- UNKNOWN_reconciliation_authority: `NONE_IN_THIS_TASK`
- DB_migration_authority: `NONE`
- new_DB_login_role_authority: `NONE`
- broad_DB_grant_authority: `NONE`
- temporary_Railway_SSH_key_authority: `ONE_EPHEMERAL_KEY_IF_REQUIRED`

## Goal

Perform the final bounded re-release of Public Live on the already accepted architecture and execute exactly one public end-to-end smoke run.

Success candidate:

```text
Recorded Run Replay:
AVAILABLE / UNCHANGED

Bounded Live:
RELEASED

scenario:
stockroom-s1-normal / 1.0.0 only

public smoke runs:
EXACTLY ONE

smoke:
UNAMBIGUOUS TERMINAL PASS

Browser:
REVIEW REQUIRED

Human public-site smoke:
PENDING
```

Do not redesign architecture or repair unrelated historical tests.

## frozen accepted baseline

### repository

`ade1ccdfd6248e264dddbe98cf77371e9189a3d6`

Required ancestry includes:

```text
worker claim-sequence repair:
2e0e67e5f80c31de29b004944b858b33bc1cc27e

persistence-suite restoration:
109fb5f59a4f44c9826d51a13169a898f16187e5
```

### hosted DB

Expected migration head:

`20260919_0025`

Accepted 0025 UNKNOWN reconciliation authority:
- `unknown_provider_reconciliation_candidates()`
- `reconcile_unknown_provider_run(bytea)`
- PUBLIC execute revoked;
- intended reconciler authority only.

This Task MUST NOT invoke the mutating UNKNOWN reconciliation function.

### historical retained runs

1919:

```text
state:
FAILED_NOT_DISPATCHED

reservation:
SETTLED / cost 0

slot:
FREE

held liability:
0
```

0125:

```text
state:
FAILED_TIMEOUT

provider physical truth:
OUTCOME_UNKNOWN retained

reservation:
SETTLED / conservative liability 4400 micro-USD

slot:
FREE

outbox:
CLOSED

open claims/pins:
0

provider resend:
0
```

Do not mutate or re-settle either run.

### campaign

```text
campaign_id:
public-live-v1

scenario:
stockroom-s1-normal / 1.0.0

campaign budget:
15000000 micro-USD

daily budget:
4000000 micro-USD

per-run reservation:
200000 micro-USD

global admissions/day:
20

concurrency:
2

client:
3/hour / 10/day

cutoff exclusive:
2026-10-17T15:00:00Z
```

Fresh preflight must prove current held liability is 0.

### provider

```text
provider:
OpenAI

model:
gpt-5.6-luna

profile:
public-live-luna-v1 / version 1

provider_call_maximum:
4

provider_retry_maximum:
1

tool_call_maximum:
1
```

Important:

`provider_call_maximum=4` is a bounded profile ceiling, not authorization to manually create calls.

Only the canonical runtime for the exactly one smoke run may create provider operations/calls.

No manual/provider-side test send.

No extra canary.

No second smoke run.

### Public Live tool

```text
Tool Broker
→ TOOL capability only
→ PublicLiveFixedStockroomDispatcher
→ stockroom_summary
```

Public fixed tool:

```text
PROCESS:
0

FILESYSTEM:
0

tool NETWORK:
0

tool SECRET:
0

Docker dependency:
0
```

Owner/Self-Dogfood Docker remains separate.

### worker

The existing `aiscc-public-live-worker` must use source containing the accepted sequence fix:

```text
candidate = sequence + 1
DB mediated claim
commit local sequence only after successful return
```

Do not redeploy old worker code.

## known non-blocking historical test debt

Two exploratory historical migration-path tests outside the accepted current-head readiness selection remain red.

They are not release scope.

Do not modify them.

Do not use them as a reason to change production/runtime state in this Task.

## required activation order

### Phase A — fresh preflight before mutation

Freshly verify:

#### Git / repository
- `HEAD == origin/main == ade1ccdfd6248e264dddbe98cf77371e9189a3d6` except exact supplied governance placement;
- source/test ancestry exact;
- index clean for tracked release scope;
- no unreviewed production/config change.

#### DB / campaign
- migration head 0025;
- 0025 ACL exact;
- control disabled;
- active future-deadline public runs 0;
- claimable worker work 0;
- unreleased claims 0;
- open dispatch pins 0;
- UNKNOWN reconciliation candidate set empty;
- campaign held 0;
- relevant day held 0;
- ledger conservation exact;
- 1919 and 0125 durable closed states unchanged.

#### hosted exposure
- ingress public domains 0;
- worker public domains 0;
- edge trust absent;
- frontend release-disabled;
- no stale Live API origin.

#### worker
- existing worker deployment healthy;
- corrected worker source applicable;
- recent bounded idle evidence contains no claim-sequence regression;
- no outstanding worker failure that could prevent a new run.

#### provider/secret
Value-free metadata only:
- worker is sole provider-secret owner;
- provider secret binding sealed/service-local;
- standard `OPENAI_API_KEY` absent;
- ingress/initializer/API provider binding absent;
- provider/model/profile exact.

Do not call OpenAI during preflight.

#### Replay
- public page/config reachable;
- all four recorded scenarios unchanged;
- `live-config.json.enabled=false`;
- `api_origin=null`;
- CSP `connect-src 'self'`.

Any material mismatch => STOP before release mutation.

### Phase B — public ingress while backend disabled

Using the EXISTING `aiscc-public-live-ingress` only:

1. create exactly one Railway-generated HTTPS public domain;
2. record exact origin;
3. configure only the exact accepted public release-origin binding required by current source;
4. configure only the exact accepted edge-trust binding;
5. redeploy/restart ingress only as mechanically required;
6. verify health;
7. with control still disabled:
   - valid public Origin request must reach safe disabled outcome;
   - invalid Origin must be denied;
   - no run must be created;
   - no worker/provider action must occur.

Do not proceed if ingress is not fail-closed.

### Phase C — frontend release binding while backend disabled

Modify only the accepted release surface required by current source, expected:
- `public/replay/live-config.json`;
- `public/replay/_headers`;
- deterministic release/build manifest;
- directly affected release tests if required.

Required config:

```json
{
  "api_origin": "<EXACT_HTTPS_RAILWAY_INGRESS_ORIGIN>",
  "enabled": true,
  "schema": "AISCC-PUBLIC-LIVE-FRONTEND-CONFIG-V1"
}
```

CSP:
- preserve existing directives;
- `connect-src` allows only `'self'` plus exact ingress origin;
- no wildcard/general HTTPS;
- no unsafe broadening.

Then:
1. run directly affected frontend/Replay tests;
2. verify four Replay scenario identities unchanged;
3. commit/push exact release-surface changes;
4. deploy exact artifact to existing Cloudflare Pages project;
5. verify public page/config/CSP;
6. backend control MUST still be disabled.

### Phase D — control enablement LAST

Only after A-C PASS.

Use accepted trusted hosted control authority.

Enable the existing campaign only:

```text
active_campaign:
public-live-v1

policy_digest:
accepted current digest

incident:
NULL

enabled:
true
```

Do not recreate campaign.

Immediately reread:
- enabled true;
- campaign exact;
- incident null;
- budget/slot state sane;
- zero public run created before the smoke.

This is the release activation point.

### Phase E — exactly one bounded public smoke run

Create exactly ONE public smoke run through the actual released public ingress.

Use:
- released public ingress;
- browser Origin contract;
- exact `stockroom-s1-normal / 1.0.0`;
- one new idempotency key.

Rules:

1. one POST creates at most one run through idempotency;
2. never create a second smoke run;
3. use read capability only in-memory for the same run and never export it;
4. follow canonical GET/poll path;
5. allow only canonical worker/runtime orchestration;
6. allow Public fixed in-process Stockroom tool only;
7. provider operations/calls may occur only through canonical runtime for this run;
8. total provider behavior must stay inside accepted profile limits;
9. no manual provider call;
10. no alternate provider/model;
11. no blind resend after physical ambiguity;
12. no second run after any failure;
13. no raw provider output exported;
14. Replay must remain usable.

#### success candidate

Only if the run reaches an unambiguous expected terminal successful state and all provider/tool operations are canonically closed.

Collect:
- run terminal state;
- work/execution terminal state;
- provider operation count/phases/outcomes;
- tool operation count;
- usage/cost accounting;
- reservation/slot/outbox settlement;
- worker claim/pin closure;
- public projection;
- no secret/output leakage.

#### UNKNOWN / ambiguous provider outcome

If ANY provider operation reaches:
- `OUTCOME_UNKNOWN`;
- timeout/transport ambiguous outcome;
- any physical send ambiguity;

then:

```text
NO RESEND
NO SECOND RUN
ROLLBACK IMMEDIATELY
PRESERVE EVIDENCE
```

Do not invoke 0025 reconciliation in this Task.

After rollback, export the retained liability/claim/pin state and return Browser review for a separately authorized reconciliation.

#### known material failure

For any material non-UNKNOWN smoke failure:
- no second smoke;
- rollback;
- preserve evidence;
- return Browser review.

### Phase F — successful-release verification

Only after the single smoke reaches an unambiguous terminal PASS candidate:

Verify:
- Replay public succeeds;
- all four Replay scenarios still load;
- frontend Live release label/state truthful;
- start control available;
- exact API origin;
- exact narrow CSP;
- ingress health;
- invalid Origin denied;
- no owner/admin route exposure;
- campaign control enabled exact;
- migration head still 0025;
- 0025 ACL unchanged;
- worker corrected source remains deployed;
- worker provider-secret isolation exact;
- exactly one new public run;
- all provider operations belong only to that run;
- all provider operations terminal known;
- no UNKNOWN;
- no unauthorized provider call/retry;
- tool operation within profile max 1;
- reservation/ledger/slot/outbox terminal and conserved;
- no raw secret/capability/provider output in evidence.

Do NOT rollback a successful release merely because Browser/Human review remains pending.

## rollback contract

Any material post-mutation failure triggers rollback.

Order:

1. set `public_control.enabled=false` FIRST;
2. restore frontend release-disabled state:
   - `enabled=false`;
   - `api_origin=null`;
   - CSP `connect-src 'self'`;
3. deploy Replay-only frontend artifact;
4. remove ingress edge-trust release binding;
5. remove ingress public domain;
6. restore ingress release-origin setting to safe preactivation state if current source requires it;
7. keep worker provider secret sealed on worker;
8. preserve campaign/run/provider/accounting evidence;
9. remove temporary SSH access if created;
10. verify Replay public and Live fail-closed.

Do not delete failed smoke evidence.

## temporary operator transport

If exact hosted control/read verification requires operator access, at most one ephemeral Railway SSH key is authorized.

Rules:
- Task-only;
- no public PostgreSQL endpoint;
- never export key bytes;
- never export DB credential/DSN;
- never read/export provider secret value;
- remove Railway key before completion;
- remove local keypair/helper material;
- prove cleanup by presence/count metadata only.

Cleanup failure after release activity:
- disable control;
- rollback Replay-only;
- return `TEMP_OPERATOR_ACCESS_CLEANUP_FAILED`.

## Git / deployment coupling

A main push may passively rebuild repository-connected ingress/API services.

Before each push:
- control disabled unless this is after the successful terminal smoke and only governance persistence is pending;
- no pending UNKNOWN;
- no unexpected claimable work;
- exact release state known.

After passive deployment:
- verify service health;
- verify domain/edge trust state;
- verify no unintended run/provider action.

No amend/rebase/force push.

## successful Executor result

```text
PUBLIC_LIVE_RERELEASED
/
SINGLE_PUBLIC_SMOKE_PASS
/
BROWSER_REVIEW_REQUIRED
/
HUMAN_PUBLIC_SITE_SMOKE_PENDING
```

Executor must not mark L8 closed.

## safe rollback result

```text
RELEASE_ROLLED_BACK_TO_REPLAY_ONLY
/
BROWSER_REVIEW_REQUIRED
```

Include exact smoke failure classification.

## pre-enable blocker result

```text
PUBLIC_LIVE_RERELEASE_BLOCKED
/
<EXACT_NAMED_BLOCKER>
/
BROWSER_REVIEW_REQUIRED
```

## forbidden

- second public smoke run;
- manual provider send/canary;
- provider fallback;
- blind resend after UNKNOWN;
- invocation of 0025 mutating UNKNOWN reconciliation;
- new migration;
- DB role/login/grant expansion;
- new Railway service/database;
- worker public domain;
- public DB endpoint;
- provider secret move/copy/rotation;
- free-form public input;
- owner/admin exposure;
- Public Docker/process execution;
- unrelated historical test repair;
- unrelated product work;
- force push/rebase/amend.

## canonical persistence / evidence

Persist supplied Cycle/Judgment/Handoff.

Move this Task active -> done.

Release-surface commit(s) and governance commit may be separate ordinary commits.

The target export remains ignored/untracked.

## required export

Create:

`.aiassistant/reports/target/20260919_1145_aiscc-p3-3-l8-final-public-live-rerelease-and-single-smoke-v2-1/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `PREFLIGHT_SAFE_STATE.md`
- `PUBLIC_INGRESS_RELEASE_BINDING.md`
- `FRONTEND_CLOUDFLARE_RELEASE_PROOF.md`
- `CONTROL_ENABLEMENT.md`
- `PUBLIC_END_TO_END_SMOKE.md`
- `PROVIDER_OPERATION_PROOF.md`
- `TOOL_OPERATION_PROOF.md`
- `ACCOUNTING_SETTLEMENT_PROOF.md`
- `WORKER_CLAIM_PIN_PROOF.md`
- `POST_RELEASE_SECURITY_STATE.md`
- `ROLLBACK_PROOF.md` if rollback occurred, otherwise `ROLLBACK_NOT_USED.md`
- `FINAL_PUBLIC_STATE.md`
- `TEMP_OPERATOR_ACCESS_PROOF.md`
- `WORKSPACE_STATE.md`
- changed release/governance files preserving repository-relative paths

Also create adjacent result ZIP and report SHA-256.

Never export:
- OpenAI/provider key or masked identifier;
- HMAC key;
- DB credential/DSN;
- SSH key material;
- read capability;
- raw provider output;
- private protocol state;
- private reasoning.

## final response format

1. result
2. target bundle path + ZIP SHA-256
3. preflight
4. release commit(s)
5. governance commit/push
6. ingress domain/deployment identity
7. Cloudflare deployment identity
8. control/campaign final state
9. exactly-one smoke run identity/state
10. provider operation/call counts and terminal classifications
11. tool operation count/result classification
12. accounting/reservation/slot/outbox state
13. worker claim/pin terminal state
14. provider secret/security state
15. temporary access cleanup
16. Replay status
17. rollback state
18. Browser/Human pending items
