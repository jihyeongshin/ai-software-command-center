# 작업지시서: P3-3 L8 authorized read-only hosted re-release readiness reproof

## meta

- task_id: `20260919_0415_aiscc-p3-3-l8-authorized-readonly-hosted-rerelease-readiness-reproof-1`
- created_at: `2026-09-19T04:15:00+09:00`
- work_type: `L8_RERELEASE_READINESS_REPROOF`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- exact_baseline: `645d5603a29415fbf87179c136011fa12a305643`
- fresh_ide_chat_required: `No`
- public_release_authority: `NONE`
- public_run_authority: `NONE`
- provider_call_authority: `NONE`
- DB_mutation_authority: `NONE`
- DB_migration_authority: `NONE`
- Railway_config_mutation_authority: `NONE_EXCEPT_ONE_EPHEMERAL_SSH_KEY_IF_REQUIRED`
- Cloudflare_mutation_authority: `NONE`
- public_domain_authority: `NONE`
- edge_trust_authority: `NONE`
- temporary_Railway_SSH_key_authority: `ONE_EPHEMERAL_KEY_IF_REQUIRED`
- provider_secret_value_authority: `NONE`

## Goal

Retry the post-UNKNOWN fresh re-release readiness preflight and close only the missing hosted-evidence gap.

This Task is read-only with respect to product/runtime state.

The sole authorized infrastructure mutation is registration/removal of one temporary Railway SSH key if required to create a private operator transport for read-only evidence.

Do NOT release Public Live.

## accepted current lineage

```text
0240 UNKNOWN reconciliation:
ACCEPTED / CLOSED

0125 retained smoke:
FAILED_TIMEOUT

0125 provider physical truth:
OUTCOME_UNKNOWN retained

0125 conservative settlement:
4400 micro-USD

migration source/head expected:
20260919_0025

0250:
ACCEPTED_CORRECT_STOP

0250 blocker:
HOSTED_READ_ONLY_EVIDENCE_PATH_UNAVAILABLE

Public Live:
NOT_RELEASED

prior Human RELEASE_PUBLIC_LIVE:
CONSUMED
```

## starting repository authority

Required:

`HEAD == origin/main == 645d5603a29415fbf87179c136011fa12a305643`

Verify:
- parent is `f5c3edd826ef87696cfd260a3e08d0aabe1becda`;
- no product/source/test/migration/config mutation after baseline;
- 0250 governance commit is exact;
- index state known;
- unrelated untracked residue untouched.

If not exact:

`REPOSITORY_BASELINE_MISMATCH`

and STOP.

## temporary Railway SSH access

### when allowed

Use no new key if an existing safe private read-only path is available.

Otherwise exactly one fresh ephemeral Railway SSH key may be created.

It is authorized only for:
- Railway private service access;
- private PostgreSQL evidence queries;
- value-free service/variable metadata checks needed by this Task.

### strict constraints

- one key maximum;
- Task-only lifetime;
- do not commit key material;
- do not export public/private key bytes;
- do not print key fingerprint if it encodes material beyond ordinary non-secret metadata;
- do not expose PostgreSQL via public TCP proxy/domain;
- do not copy DB password/DSN into evidence;
- do not read provider secret values;
- do not use the access path to mutate DB rows/schema/roles;
- do not invoke reconciliation;
- do not restart/redeploy solely for evidence;
- delete the Railway key before final result;
- delete local private/public key files and askpass/helper material;
- verify cleanup using count/presence metadata only.

If cleanup cannot be completed:

`TEMP_OPERATOR_ACCESS_CLEANUP_FAILED`

and STOP.

Public Live must remain disabled.

## read-only DB/session rule

Every hosted DB session used for proof must be read-only where technically supported.

Prefer:
- `default_transaction_read_only=on`, or
- explicit read-only transaction semantics.

No DDL/DML.

Evidence queries may inspect:
- rows;
- counts;
- pg privilege/catalog metadata;
- Alembic version;
- current role/session identity;
- mediated read-only candidate function.

Do not call the mutating reconciliation function.

## readiness dimension 1 — repository / deployment lineage

Freshly verify:
- exact Git baseline;
- source/security commit `d4d56d9a722d857515492805f69b125a742fa4bf` remains in ancestry;
- sole static migration head 0025;
- current Railway deployment identities for ingress/worker/initializer/API/Postgres;
- no unexpected product deployment/source drift attributable to this Task.

Passive repo-connected deploy observation is allowed.

No deploy mutation.

## readiness dimension 2 — hosted migration / reconciliation ACL

Fresh hosted DB proof:

- `alembic_version = 20260919_0025`;
- `PUBLIC` has no EXECUTE on:
  - `public_live_api.unknown_provider_reconciliation_candidates()`
  - `public_live_api.reconcile_unknown_provider_run(bytea)`;
- existing `aiscc_public_live_reconciler` has the exact intended EXECUTE authority;
- no new DB login/role was added by 0025;
- no broad table DML authority was added by 0025;
- runtime/reconciler compatibility from 0024 remains valid;
- candidate function currently returns an empty set after the accepted 0125 settlement.

Do not invoke `reconcile_unknown_provider_run`.

## readiness dimension 3 — 0125 UNKNOWN reconciliation durability

Freshly prove exact retained run state:

```text
public run:
FAILED_TIMEOUT

reservation:
SETTLED

settled_cost:
4400

SETTLE event count:
1

slot:
FREE / run_id null

outbox:
CLOSED

open worker dispatch pins:
0

unreleased worker claims:
0

worker work:
retained / closed UNKNOWN_RECONCILED / non-claimable

provider physical operations:
1

provider durable outcome:
OUTCOME_UNKNOWN

provider ambiguity:
TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME

provider retry/resend:
0

tool operations:
0
```

Also prove:
- no second ledger delta;
- no second reconciliation;
- no new known provider output/result;
- no state regression;
- candidate set no longer includes this run.

Do not invoke reconciliation again.

## readiness dimension 4 — historical 1919 durability

Freshly prove:
- state `FAILED_NOT_DISPATCHED`;
- reservation SETTLED;
- settled cost 0;
- slot free;
- outbox closed;
- no duplicate settlement;
- retained worker lineage nonclaimable;
- no conflict with 0125 accounting.

No mutation.

## readiness dimension 5 — campaign / day ledger

Fresh hosted proof:

Campaign `public-live-v1`:
- scenario/version exact;
- cutoff `2026-10-17T15:00:00Z` exclusive;
- per-run reservation policy 200000;
- campaign limit 15000000;
- daily limit 4000000;
- daily starts max 20;
- concurrency 2;
- campaign held = 0;
- campaign conservation exact.

For the 0125 UTC day:
- held = 0;
- conservation exact;
- settled conservative liability includes exactly the accepted 4400 for 0125;
- no duplicate SETTLE.

If other legitimate historical settled amounts exist, itemize and reconcile them rather than assuming global settled total must equal 4400.

Never describe 4400 as actual provider billing.

## readiness dimension 6 — fail-closed hosted runtime

Freshly prove:

- `public_control.enabled=false`;
- Public Live NOT_RELEASED;
- active future-deadline public runs = 0;
- claimable public worker work = 0;
- unreleased claims = 0;
- open dispatch pins = 0;
- no unexpected unreconciled reservation;
- ingress public domains = 0;
- worker public domains = 0;
- edge trust absent;
- no release frontend origin binding;
- no run/provider action occurred in this Task.

Any exposure/regression => exact blocker.

## readiness dimension 7 — provider / secret applicability

Value-free metadata only.

Freshly prove:
- provider/model/profile remains `OpenAI / gpt-5.6-luna / public-live-luna-v1`;
- worker is the sole provider-secret owner;
- worker secret binding is service-local/sealed;
- standard `OPENAI_API_KEY` absent;
- ingress provider secret authority absent;
- initializer provider secret authority absent;
- API provider secret authority absent;
- no project/shared provider secret binding relevant to Public Live;
- conservative request liability source still derives 4400;
- no provider/canary call made.

Historical 0125 outcome remains UNKNOWN and MUST NOT be called provider-health PASS.

If provider applicability cannot be proved without reading the secret value or calling OpenAI:

`PROVIDER_APPLICABILITY_NOT_PROVABLE`

and STOP.

## readiness dimension 8 — fixed Public tool applicability

Freshly prove current deployment/source still matches:

```text
PUBLIC_BOUNDED_LIVE
→ Tool Broker
→ TOOL only
→ PublicLiveFixedStockroomDispatcher
→ stockroom_summary
```

Public fixed tool capabilities:

```text
PROCESS=0
FILESYSTEM=0
tool NETWORK=0
tool SECRET=0
Docker dependency=0
```

Owner/Self-Dogfood Docker path remains separate.

No runtime mutation.

## readiness dimension 9 — Replay / frontend

Fresh public/read-only proof:
- Replay URL HTTP success;
- health/corpus index available;
- all four recorded scenarios unchanged from repo;
- `live-config.json.enabled=false`;
- `api_origin=null`;
- CSP `connect-src 'self'`;
- no stale Bounded Live release label;
- Replay independently usable.

No Cloudflare mutation.

## readiness dimension 10 — exact potential next release delta

Refresh plan only.

Do not execute.

Required future order:

```text
NEW Human RELEASE_PUBLIC_LIVE
→ public-bind existing ingress while control disabled
→ prove fail-closed ingress
→ exact frontend API origin + narrow CSP
→ Cloudflare deploy
→ control enable LAST
→ exactly one new public smoke
→ Browser review
→ Human public-site smoke
→ L8 close
```

If a future smoke reaches UNKNOWN:
- no resend;
- no second run;
- rollback immediately;
- preserve evidence;
- use accepted 0025 reconciliation path under separate Browser-authorized reconciliation authority.

Do not auto-reconcile inside the release smoke Task unless a future Task explicitly authorizes that operation.

## success result

Only if every fresh readiness dimension passes and temporary access cleanup passes:

```text
RERELEASE_READY_CANDIDATE
/
NEW_HUMAN_RELEASE_DECISION_REQUIRED
/
BROWSER_REVIEW_REQUIRED
```

## blocked results

Use the narrowest exact blocker, including:

```text
REPOSITORY_BASELINE_MISMATCH
TEMP_OPERATOR_ACCESS_CLEANUP_FAILED
HOSTED_MIGRATION_HEAD_MISMATCH
MIGRATION_AUTHORITY_REGRESSION
UNKNOWN_RECONCILIATION_DURABILITY_REGRESSION
HISTORICAL_SETTLEMENT_DURABILITY_REGRESSION
LEDGER_CONSERVATION_REGRESSION
PUBLIC_FAIL_CLOSED_STATE_REGRESSION
PROVIDER_APPLICABILITY_NOT_PROVABLE
FIXED_TOOL_APPLICABILITY_REGRESSION
REPLAY_READINESS_REGRESSION
```

Do not hide multiple material blockers; list primary + secondary if required.

## forbidden

- Public Live release
- public control enable
- new public run
- provider call/canary
- provider retry/resend
- reconciliation invocation
- DB DDL/DML
- new migration
- new DB login/role/membership/grant
- public PostgreSQL exposure
- Railway service config mutation other than one temporary SSH key lifecycle
- service restart/redeploy for convenience
- public ingress domain
- edge trust
- frontend Live enable
- Cloudflare mutation
- provider secret read/copy/rotation
- unrelated product work
- amend/rebase/force push

## canonical persistence / Git

Persist supplied Cycle/Judgment/Handoff and move this Task active -> done.

Only governance/task-lifecycle commit/push is authorized.

No product/source/test/migration/config changes.

Known unrelated untracked residue must remain untouched.

## required export

Create:

`.aiassistant/reports/target/20260919_0415_aiscc-p3-3-l8-authorized-readonly-hosted-rerelease-readiness-reproof-1/`

Required root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `REPOSITORY_DEPLOYMENT_AUTHORITY.md`
- `HOSTED_MIGRATION_ACL.md`
- `UNKNOWN_RECONCILIATION_DURABILITY.md`
- `HISTORICAL_SETTLEMENT_DURABILITY.md`
- `LEDGER_CAMPAIGN_READINESS.md`
- `HOSTED_SAFE_STATE.md`
- `PROVIDER_READINESS_APPLICABILITY.md`
- `FIXED_TOOL_RUNTIME_APPLICABILITY.md`
- `REPLAY_FRONTEND_READINESS.md`
- `TEMP_OPERATOR_ACCESS_PROOF.md`
- `RERELEASE_DELTA_PLAN.md`
- `WORKSPACE_STATE.md`
- changed governance files preserving repository-relative paths

Also create adjacent result ZIP and report SHA-256.

Never export:
- provider key or masked identifier;
- DB DSN/password;
- SSH private/public key material;
- HMAC key;
- read capability;
- raw provider output;
- raw prompts/private protocol;
- private reasoning.

## final response format

1. result
2. target bundle path + ZIP SHA-256
3. governance commit/push
4. temporary access lifecycle/cleanup
5. hosted migration/ACL
6. 0125 durability
7. 1919 durability
8. campaign/day ledger
9. fail-closed hosted state
10. provider/secret applicability
11. fixed-tool applicability
12. Replay/frontend
13. next release delta
14. Human verification state
15. blockers/unverified items
