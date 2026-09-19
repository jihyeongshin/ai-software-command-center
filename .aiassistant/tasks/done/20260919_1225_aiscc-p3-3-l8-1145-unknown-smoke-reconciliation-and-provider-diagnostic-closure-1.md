# 작업지시서: P3-3 L8 1145 UNKNOWN Smoke Reconciliation + Repeated Provider Diagnostic Closure

## meta

- task_id: `20260919_1225_aiscc-p3-3-l8-1145-unknown-smoke-reconciliation-and-provider-diagnostic-closure-1`
- created_at: `2026-09-19T12:25:00+09:00`
- work_type: `HOSTED_UNKNOWN_RECONCILIATION_AND_NARROW_PROVIDER_DIAGNOSTIC_REWORK`
- evidence_profile: `HIGH_RISK`
- execution_model: `THIN_CC_THICK_EXECUTOR`
- expected_origin_main: `704a0db9e2dac902ec84fa0430d0b9bfeaf89174`
- expected_local_predecessor_governance_commit: `bd00465546d577d85c57f23ec8fef2012b0d952f`
- fresh_ide_chat_required: `No`
- public_release_authority: `NONE`
- public_run_authority: `NONE`
- provider_call_authority: `NONE`
- provider_retry_resend_authority: `NONE`
- Cloudflare_mutation_authority: `NONE`
- public_domain_authority: `NONE`
- edge_trust_authority: `NONE`
- hosted_exact_unknown_reconciliation_authority: `EXACTLY_ONE_RETAINED_1145_RUN`
- DB_migration_authority: `NONE`
- new_DB_login_role_grant_authority: `NONE`
- production_source_change_authority: `NARROW_SECRET_SAFE_PROVIDER_UNKNOWN_DIAGNOSTIC_ONLY_IF_REQUIRED`
- Railway_worker_deploy_authority: `EXACT_DIAGNOSTIC_SOURCE_DEPLOY_IF_SOURCE_CHANGED`
- temporary_Railway_SSH_key_authority: `ONE_EPHEMERAL_KEY_IF_REQUIRED`

## Goal

Close two linked post-release obligations:

1. reconcile exactly the retained 1145 provider-UNKNOWN smoke using already accepted migration `20260919_0025`;
2. close the repeated-provider-UNKNOWN diagnostic gap without making another real provider call.

Do NOT release Public Live.

Do NOT create a new public run.

## accepted entry facts

```text
Public control:
DISABLED

Public Live:
NOT_RELEASED

public ingress domains:
0

edge trust:
ABSENT

frontend:
Replay-only / enabled=false / api_origin=null

migration head expected:
20260919_0025

1145 provider operation:
OUTCOME_UNKNOWN / TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME

1145 provider retry/resend:
0

1145 tool operations:
0
```

This is the second real release smoke to reach the same provider ambiguity class.

The previous Human `RELEASE_PUBLIC_LIVE` decision is consumed.

## starting Git/provenance contract

Expected remote:

`origin/main = 704a0db9e2dac902ec84fa0430d0b9bfeaf89174`

Executor reported local-only governance commit:

`bd00465546d577d85c57f23ec8fef2012b0d952f`

Before substantive work verify:
- local commit exists;
- parent is exactly `704a0db9e2dac902ec84fa0430d0b9bfeaf89174`;
- it contains only the supplied 1145 Cycle/Judgment/Handoff and completed 1145 Task lifecycle;
- no production/release source is in that governance commit;
- rollback tree remains exactly the accepted pre-release tree;
- no unrelated tracked mutation.

Mismatch:

`PREDECESSOR_GOVERNANCE_COMMIT_IDENTITY_MISMATCH`

and STOP.

Do not amend/rebase/force-push.

## Phase A — fail-closed hosted preflight

Before reconciliation freshly verify:
- migration head 0025;
- control disabled;
- public ingress domains 0;
- worker public domains 0;
- edge trust absent;
- frontend disabled/null;
- Replay public according to available public evidence;
- worker provider secret still worker-only/sealed/service-local;
- no provider binding on ingress/initializer/API;
- no new public run after 1145;
- no provider retry/resend after 1145.

Any current exposure => STOP.

## Phase B — exact retained 1145 target selection

Do NOT identify the target only from a copied run ID.

Fresh hosted evidence must select exactly one run satisfying all of:

- it is the 1145 V2 release smoke lineage;
- it is not 1919;
- it is not the already reconciled 0125 run;
- expired;
- public state `ADMITTED`;
- settlement absent;
- reservation `HELD`;
- reservation amount `200000`;
- slot occupied by the run;
- outbox `BOUND`;
- worker work `recovery_required=true`;
- exactly one unreleased worker claim;
- exactly one open dispatch pin;
- exactly one linked provider operation;
- semantic role PRIMARY;
- provider operation crossed `DISPATCH_STARTED`;
- current operation phase `OUTCOME_UNKNOWN`;
- outcome `TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME`;
- no known provider outcome event;
- provider retry/resend 0;
- tool operation 0;
- exactly one new 1145 public smoke exists.

Zero or multiple matches:

`1145_UNKNOWN_TARGET_IDENTITY_AMBIGUOUS`

and STOP.

## Phase C — inspect existing durable diagnostic evidence BEFORE reconciliation

Read only.

Inspect exact P1 operation/event refs and safe persisted metadata.

At minimum record:
- operation phase/outcome;
- operation/event sequence;
- `provider_status` if present;
- safe fixed refs already persisted;
- whether a safe diagnostic reason is durably distinguishable.

Do not read/export:
- raw provider response;
- raw request;
- secret;
- capability;
- private protocol encrypted content.

### classification

If existing durable metadata proves one of these without inference, report it:

```text
PROVIDER_NONTERMINAL_RESPONSE
PROVIDER_UNKNOWN_RESPONSE_STATUS
PROVIDER_MALFORMED_RESPONSE_BODY
PROVIDER_TRANSPORT_OR_CONNECTION_UNKNOWN
```

If existing evidence only proves a broader bucket, report the broader bucket.

Do not claim a specific OpenAI/network cause unless the durable evidence supports it.

## Phase D — exact 0025 reconciliation

Use only:

`public_live_api.reconcile_unknown_provider_run(bytea)`

through the accepted reconciler identity.

Do not raw-update tables.

Canonical conservative liability MUST be derived from current accepted profile authority.

Expected cross-check only:

`4400 micro-USD`

Do not operator-hardcode 4400 as actual provider charge.

Successful reconciliation must result in:

```text
public run:
FAILED_TIMEOUT

reservation:
SETTLED

settled accounting liability:
canonical conservative L

slot:
FREE

outbox:
CLOSED

open dispatch pins:
0

unreleased worker claims:
0

worker work:
retained / closed UNKNOWN_RECONCILED / non-claimable

provider operations:
still exactly 1

provider operation physical truth:
still OUTCOME_UNKNOWN

provider retry/resend:
0

tool operations:
0
```

Accounting delta from the 1145 hold:

```text
held:
-200000

settled:
+L

available:
+(200000-L)
```

for exact applicable campaign/day ledgers.

Actual provider charge remains UNKNOWN.

### idempotency

Perform the accepted safe second reconciliation invocation/equivalent idempotency proof.

Must show:
- no second SETTLE;
- no second ledger delta;
- no second claim/pin closure;
- no provider call;
- no state regression.

## Phase E — governance provenance push

After reconciliation succeeds and fail-closed state is re-proven:

Verify the local predecessor governance commit `bd00465546d577d85c57f23ec8fef2012b0d952f` is exact.

Then push it by ordinary fast-forward if still not present remotely.

Known repository-connected passive deploy coupling applies.

After push reverify:
- control disabled;
- domains 0;
- edge trust absent;
- no run/provider side effect;
- provider secret isolation unchanged.

If push cannot be made safely, report exact blocker; do not alter history.

## Phase F — repeated UNKNOWN diagnostic gap assessment

Current source facts to audit:

`OpenAIResponsesAdapter` maps multiple conditions to `TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME`, including:
- API timeout/connection;
- malformed response body;
- unknown response status;
- queued/in-progress response.

Current `AgentExecutionService` persists normal returned-result refs including:
- `result_hash`;
- `provider_status`.

It does not currently guarantee durable persistence of the adapter's fixed `sanitized_error` for returned UNKNOWN results.

Worker logs collapse execution failures to one generic safe code.

### no-change path

If the existing durable `provider_status` and current source are sufficient to preserve an operationally useful, truthful category for the next occurrence, production source change is NOT required.

Document why.

### narrow source-change path

If the exact safe cause remains materially collapsed, a narrow source change is authorized only to retain an allowlisted secret-safe diagnostic classification for future provider UNKNOWN events.

Preferred boundary:
- durable operation/event refs or equivalent existing evidence channel;
- fixed allowlisted codes only;
- no raw exception string;
- no raw HTTP response/body;
- no raw request;
- no secret/capability;
- no provider output;
- no new provider-send truth;
- no new schema/migration.

Allowed diagnostic codes should be derived from existing adapter semantics, such as:

```text
TRANSPORT_OUTCOME_UNKNOWN
MALFORMED_RESPONSE_BODY
UNKNOWN_RESPONSE_STATUS
PROVIDER_NONTERMINAL_STATUS
```

Do not persist arbitrary exception text.

If a new DB column/table/migration is required:

`PROVIDER_UNKNOWN_DIAGNOSTIC_MIGRATION_REQUIRED`

and STOP.

## Phase G — deterministic diagnostic tests

If source changes, tests must prove:
1. APITimeout/APIConnection -> safe transport classification;
2. malformed body -> safe malformed classification;
3. unknown status -> safe unknown-status classification;
4. queued/in_progress -> safe nonterminal classification;
5. durable P1 physical outcome remains `OUTCOME_UNKNOWN`;
6. no retry is authorized;
7. safe diagnostic ref is allowlisted only;
8. no secret/raw response/request/provider output persisted;
9. known-success and definitely-not-sent paths unchanged;
10. UNKNOWN reconciliation semantics unchanged.

Run:
- directly affected provider/service tests;
- worker claim-sequence regression tests;
- 0025 UNKNOWN reconciliation tests;
- Ruff;
- format check;
- narrow mypy for changed production owner;
- `git diff --check`.

No real provider call.

## Phase H — deploy diagnostic source only if changed

If source changed:
- commit/push exact diagnostic source/tests;
- deploy/restart existing worker only if required for that source to apply to future runs;
- same service/region/replica/start command/env/secret bindings;
- no public domain;
- no provider call;
- no public run.

Prove healthy idle worker after deployment.

If no source change, no worker deploy/restart is needed.

## Phase I — final Replay-only readiness reproof

Freshly verify:

### hosted DB
- migration head 0025;
- 1919 durable settled 0;
- 0125 durable FAILED_TIMEOUT / settled conservative 4400;
- 1145 now durable FAILED_TIMEOUT / settled conservative L;
- no held reservation;
- all slots free;
- open claims 0;
- open pins 0;
- UNKNOWN candidate set empty;
- campaign/day conservation exact.

### fail-closed
- control disabled;
- public domains 0;
- edge trust absent;
- frontend disabled/null/CSP self-only;
- Replay public/release-disabled.

### worker/provider
- worker healthy;
- claim sequence remains healthy;
- provider secret worker-only/sealed;
- no provider binding ingress/initializer/API;
- provider calls during this Task 0;
- no new public run.

### source/test
- current main exact;
- diagnostic source/tests accepted if changed;
- canonical persistence current-head suite remains green where directly affected.

## success result

If reconciliation, diagnostics, cleanup and fresh safe-state proof all pass:

```text
1145_UNKNOWN_SMOKE_LIABILITY_RECONCILED
/
REPEATED_PROVIDER_UNKNOWN_DIAGNOSTIC_ACCEPTED
/
REPLAY_ONLY_SAFE
/
FRESH_RERELEASE_READINESS_REQUIRED
/
BROWSER_REVIEW_REQUIRED
```

Do not grant release authority.

## blockers

Use narrow exact blockers:

```text
PREDECESSOR_GOVERNANCE_COMMIT_IDENTITY_MISMATCH
1145_UNKNOWN_TARGET_IDENTITY_AMBIGUOUS
UNKNOWN_PROVIDER_LIABILITY_NOT_PROVABLE
HOSTED_1145_UNKNOWN_RECONCILIATION_FAILED
PROVIDER_UNKNOWN_DIAGNOSTIC_MIGRATION_REQUIRED
PROVIDER_UNKNOWN_DIAGNOSTIC_SOURCE_SCOPE_EXPANSION_REQUIRED
PROVIDER_UNKNOWN_DIAGNOSTIC_TEST_FAILED
WORKER_IDLE_ACQUISITION_REGRESSION
TEMP_OPERATOR_ACCESS_CLEANUP_FAILED
PUBLIC_FAIL_CLOSED_STATE_REGRESSION
```

## temporary operator access

At most one ephemeral Railway SSH key if needed.

Rules:
- Task-only;
- private DB access only;
- no public DB endpoint;
- never export key bytes;
- never export DB DSN/password;
- never read provider secret value;
- remove Railway key;
- remove local keypair/helper;
- prove cleanup by count/presence metadata.

Cleanup failure:

`TEMP_OPERATOR_ACCESS_CLEANUP_FAILED`

and STOP with Public Live disabled.

## forbidden

- Public Live release;
- control enable;
- public ingress domain;
- edge trust;
- frontend Live enable;
- Cloudflare mutation;
- new public run;
- real provider call/canary;
- provider retry/resend;
- manual provider send;
- new migration;
- DB role/login/grant expansion;
- raw table reconciliation;
- public DB exposure;
- provider secret read/copy/rotation;
- unrelated historical test repair;
- unrelated product work;
- amend/rebase/force push.

## canonical persistence / Git

Persist supplied Cycle/Judgment/Handoff.

Move this Task active -> done.

Source/test commit only if narrow diagnostic code is actually required.

Governance commit may be separate.

Fast-forward push only.

## required export

Create:

`.aiassistant/reports/target/20260919_1225_aiscc-p3-3-l8-1145-unknown-smoke-reconciliation-and-provider-diagnostic-closure-1/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `PREDECESSOR_GOVERNANCE_PROOF.md`
- `1145_UNKNOWN_TARGET_IDENTITY.md`
- `EXISTING_PROVIDER_DIAGNOSTIC_EVIDENCE.md`
- `1145_UNKNOWN_RECONCILIATION_RESULT.md`
- `LEDGER_CONSERVATION.md`
- `WORKER_PIN_CLAIM_RECONCILIATION.md`
- `IDEMPOTENCY_PROOF.md`
- `REPEATED_UNKNOWN_DIAGNOSTIC_GAP.md`
- `DIAGNOSTIC_SOURCE_AUDIT.md`
- `DIAGNOSTIC_TESTS.md`
- `WORKER_DEPLOYMENT_PROOF.md` if source deployed, otherwise `WORKER_DEPLOYMENT_NOT_REQUIRED.md`
- `FINAL_SAFE_STATE.md`
- `TEMP_OPERATOR_ACCESS_PROOF.md`
- `WORKSPACE_STATE.md`
- changed source/test/governance files preserving repository-relative paths

Also create adjacent result ZIP and report SHA-256.

Never export:
- provider key or masked identifier;
- DB DSN/password;
- SSH key material;
- HMAC key;
- read capability;
- raw provider request/response/output;
- encrypted private protocol;
- private reasoning.

## final response format

1. result
2. target ZIP SHA-256
3. predecessor governance verification/push
4. exact 1145 target identity proof
5. pre-reconciliation provider diagnostic evidence
6. conservative liability derivation
7. reconciliation result
8. ledger deltas/conservation
9. claim/pin/work result
10. idempotency
11. repeated UNKNOWN diagnostic assessment
12. source/test changes if any
13. worker deployment if any
14. provider calls/resends
15. final Replay/Public Live state
16. temporary access cleanup
17. blockers/unverified
