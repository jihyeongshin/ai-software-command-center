# 작업지시서: P3-3 L8 post-UNKNOWN fresh re-release readiness preflight

## meta

- task_id: `20260919_0250_aiscc-p3-3-l8-post-unknown-fresh-rerelease-readiness-preflight-1`
- created_at: `2026-09-19T02:50:00+09:00`
- work_type: `L8_RERELEASE_READINESS_PREFLIGHT`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- exact_baseline: `f5c3edd826ef87696cfd260a3e08d0aabe1becda`
- fresh_ide_chat_required: `No`
- hosted_mutation_authority: `NONE`
- public_release_authority: `NONE`
- public_run_authority: `NONE`
- provider_call_authority: `NONE`
- Railway_config_mutation_authority: `NONE`
- Cloudflare_mutation_authority: `NONE`
- DB_mutation_authority: `NONE`
- temporary_access_creation_authority: `NONE`

## Goal

Perform a fresh read-only re-release readiness preflight after migration `20260919_0025` and successful reconciliation of the retained 0125 UNKNOWN smoke.

This Task does not authorize release.

## accepted entry state

```text
repository baseline:
f5c3edd826ef87696cfd260a3e08d0aabe1becda

migration head:
20260919_0025

0240 UNKNOWN lifecycle rework:
ACCEPTED / CLOSED

0125 retained smoke:
FAILED_TIMEOUT

0125 provider physical truth:
OUTCOME_UNKNOWN retained

0125 reservation:
SETTLED / conservative liability 4400

0125 slot:
FREE

0125 open pin:
0

0125 unreleased claim:
0

Public control:
DISABLED

Public Live:
NOT_RELEASED

public ingress domains:
0

edge trust:
ABSENT

Replay:
PUBLIC / release-disabled
```

The prior Human `RELEASE_PUBLIC_LIVE` authority is consumed.

## mandatory read-only rule

Do not mutate hosted state in order to obtain evidence.

If current available operator/read-only access is insufficient:

`RERELEASE_READINESS_BLOCKED / HOSTED_READ_ONLY_EVIDENCE_PATH_UNAVAILABLE`

and STOP.

Do not create an SSH key in this Task.

## readiness dimension 1 — repository / canonical authority

Freshly verify:
- local HEAD and origin/main identity;
- baseline exactness;
- supplied Cycle/Judgment/Handoff canonical placement;
- 0240 Task remains done;
- no unreviewed product/runtime mutation after baseline;
- source commit `d4d56d9a722d857515492805f69b125a742fa4bf` remains in ancestry;
- current migration source head is 0025.

## readiness dimension 2 — 0125 UNKNOWN reconciliation durability

Fresh hosted evidence must prove:

```text
run:
FAILED_TIMEOUT

reservation:
SETTLED

settled_cost:
4400 conservative liability

SETTLE events:
exactly 1

slot:
FREE / run_id null

outbox:
CLOSED

open dispatch pins:
0

unreleased worker claims:
0

worker work:
retained / closed / non-claimable

provider operations:
exactly 1

provider durable outcome:
OUTCOME_UNKNOWN

provider retries/resends:
0

tool operations:
0
```

Also verify:
- no second ledger delta;
- no second reconciliation event;
- no state regression;
- no new provider result/output appeared.

Do not invoke reconciliation again merely to prove durability.

## readiness dimension 3 — historical 1919 durability

Freshly confirm the historical 1919 settlement remains closed and does not conflict with 0125 accounting.

At minimum:
- `FAILED_NOT_DISPATCHED`;
- reservation settled cost 0;
- slot free;
- nonclaimable historical worker lineage;
- no duplicate SETTLE.

Do not settle it again.

## readiness dimension 4 — ledger / campaign readiness

Fresh hosted evidence:

- campaign `public-live-v1`;
- scenario/version exact;
- cutoff `2026-10-17T15:00:00Z` exclusive;
- per-run reservation `200000`;
- campaign limit `15000000`;
- day limit `4000000`;
- daily starts max `20`;
- concurrency `2`;
- campaign held liability `0`;
- campaign conservation `available + held + settled = 15000000`;
- the 0125 smoke's UTC-day ledger held liability `0`;
- day conservation exact;
- `4400` is recorded only as conservative settled liability;
- no claim that it is actual provider billing.

If other legitimate historical accounting exists, report it rather than assuming only 4400 total settled.

## readiness dimension 5 — UNKNOWN reconciliation authority applicability

Freshly establish:

- hosted migration head is exactly `20260919_0025`;
- `unknown_provider_reconciliation_candidates()` remains inaccessible to PUBLIC;
- `reconcile_unknown_provider_run(bytea)` remains inaccessible to PUBLIC;
- existing reconciler has only the accepted exact function authority;
- no new role/login/table DML authority appeared;
- current candidate set is empty after settlement;
- known-completed and definitely-not-sent paths remain separate from UNKNOWN path by current source identity.

No DB mutation.

## readiness dimension 6 — fail-closed hosted release state

Freshly observe:

- `public_control.enabled=false`;
- Public Live not released;
- ingress public domains 0;
- worker public domains 0;
- edge trust absent;
- no active future-deadline public run;
- no claimable work;
- no unreleased claim;
- no open dispatch pin;
- no unexpected provider request/run after 0240;
- no release frontend binding.

Any unexpected exposure is BLOCKED.

## readiness dimension 7 — provider / secret applicability

Do not read secret values.

Freshly prove value-free metadata:

- worker remains sole provider-secret owner;
- worker binding is service-local/sealed;
- standard `OPENAI_API_KEY` remains absent;
- ingress/initializer/API provider authority remains absent;
- provider/model/profile still exact `OpenAI / gpt-5.6-luna / public-live-luna-v1`;
- accepted one-request conservative liability derivation remains `4400` from source identity;
- no real canary/provider call is made.

Important:

The prior 0125 call ended UNKNOWN.

Do not reinterpret that event as provider health PASS.

Readiness evidence must distinguish:
- provider configuration/profile applicability: may PASS;
- last real transport outcome: historical UNKNOWN.

If a persistent current provider/network incident is visible from existing non-secret metadata/log state, return an exact blocker.

Do not call the provider to test it.

## readiness dimension 8 — fixed Public tool applicability

Freshly establish current worker deployment/source still matches:

```text
Public Bounded Live
→ Tool Broker
→ TOOL only
→ PublicLiveFixedStockroomDispatcher
→ stockroom_summary
```

and:

```text
PROCESS = 0
FILESYSTEM = 0
tool NETWORK = 0
tool SECRET = 0
Public Docker dependency = 0
```

Owner/Self-Dogfood Docker path remains separate.

## readiness dimension 9 — Replay/frontend

Fresh public/read-only proof:

- `https://aiscc-replay.pages.dev/` reachable;
- all four recorded scenarios unchanged;
- `live-config.json` has `enabled=false`;
- `api_origin=null`;
- CSP `connect-src 'self'`;
- no stale release label or contradictory visible state;
- Replay remains independently usable.

No Cloudflare mutation.

## readiness dimension 10 — exact next release delta / rollback plan

Refresh the exact current-state → potential next release delta.

Do not execute it.

The plan must preserve:

```text
NEW Human release authorization
→ existing ingress public binding while control disabled
→ fail-closed public ingress proof
→ exact frontend API-origin/CSP binding
→ Cloudflare deploy
→ control enable LAST
→ exactly one new public smoke
→ no second run on failure/UNKNOWN
→ Browser review
→ Human public-site smoke
→ L8 close
```

Rollback:

```text
control disabled first
→ Replay-only frontend restore
→ edge trust removal
→ ingress public domain removal
→ preserve run/provider/accounting evidence
```

Because the previous smoke ended UNKNOWN, the plan must explicitly state that a future UNKNOWN is now expected to reconcile through the accepted 0025 path, but release smoke still fails and rolls back. Do not auto-retry.

## success result

Only if all readiness dimensions pass:

```text
RERELEASE_READY_CANDIDATE
/
NEW_HUMAN_RELEASE_DECISION_REQUIRED
/
BROWSER_REVIEW_REQUIRED
```

## blocked result

Use the narrowest exact blocker:

```text
RERELEASE_READINESS_BLOCKED
/
<EXACT_NAMED_BLOCKER>
/
BROWSER_REVIEW_REQUIRED
```

Examples:
- `UNKNOWN_RECONCILIATION_DURABILITY_REGRESSION`
- `LEDGER_CONSERVATION_REGRESSION`
- `HOSTED_READ_ONLY_EVIDENCE_PATH_UNAVAILABLE`
- `PUBLIC_FAIL_CLOSED_STATE_REGRESSION`
- `PROVIDER_APPLICABILITY_NOT_PROVABLE`
- `PERSISTENT_PROVIDER_TRANSPORT_INCIDENT_VISIBLE`
- `REPLAY_READINESS_REGRESSION`
- `MIGRATION_AUTHORITY_REGRESSION`

## forbidden

- Public Live release
- admission enable
- public ingress domain creation
- edge trust
- frontend Live enable
- Cloudflare mutation
- Railway config mutation
- DB mutation
- provider call
- provider retry/resend
- new public run
- reconciliation invocation for convenience
- new migration
- new DB login/role/grant
- SSH key creation
- provider secret read/copy/rotation
- unrelated product work
- amend/rebase/force push

## Git / canonical persistence

Persist supplied Cycle/Judgment/Handoff and move this Task active -> done.

Only governance/task-lifecycle commit/push is authorized.

No product/source/test/migration/config change.

Known unrelated untracked residue must remain untouched.

## required export

Create:

`.aiassistant/reports/target/20260919_0250_aiscc-p3-3-l8-post-unknown-fresh-rerelease-readiness-preflight-1/`

Required root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `REPOSITORY_AUTHORITY.md`
- `UNKNOWN_RECONCILIATION_DURABILITY.md`
- `HISTORICAL_SETTLEMENT_DURABILITY.md`
- `LEDGER_CAMPAIGN_READINESS.md`
- `UNKNOWN_RECONCILIATION_AUTHORITY.md`
- `HOSTED_SAFE_STATE.md`
- `PROVIDER_READINESS_APPLICABILITY.md`
- `FIXED_TOOL_RUNTIME_APPLICABILITY.md`
- `REPLAY_FRONTEND_READINESS.md`
- `RERELEASE_DELTA_PLAN.md`
- `WORKSPACE_STATE.md`
- changed governance files preserving repository-relative paths

Also create adjacent result ZIP and report SHA-256.

Never export:
- provider key or masked identifier;
- DB DSN/password;
- SSH key material;
- HMAC key;
- read capability;
- raw provider output;
- private reasoning.

## final response format

1. result
2. target bundle path + ZIP SHA-256
3. governance commit/push
4. UNKNOWN reconciliation durability
5. historical settlement durability
6. ledger/campaign readiness
7. migration/authority readiness
8. fail-closed hosted state
9. provider applicability + explicit historical UNKNOWN note
10. fixed-tool applicability
11. Replay/frontend readiness
12. next release delta
13. Human verification state
14. blockers/unverified items
