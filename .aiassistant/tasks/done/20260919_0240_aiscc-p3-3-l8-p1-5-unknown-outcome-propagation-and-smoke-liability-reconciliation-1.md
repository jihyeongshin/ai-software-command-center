# 작업지시서: P3-3 L8 P1-5 UNKNOWN outcome propagation and smoke liability reconciliation

## meta

- task_id: `20260919_0240_aiscc-p3-3-l8-p1-5-unknown-outcome-propagation-and-smoke-liability-reconciliation-1`
- created_at: `2026-09-19T02:40:00+09:00`
- work_type: `SECURITY_RUNTIME_REWORK_AND_HOSTED_RECONCILIATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_origin_main: `3465d0f5eb5b2a390923907d54496f25860c50f0`
- expected_local_predecessor_governance_commit: `01e5e02383c64d4a72bbc5b2c713b3fd23adb94e`
- fresh_ide_chat_required: `No`
- public_release_authority: `NONE`
- public_run_authority: `NONE`
- provider_call_authority: `NONE`
- Cloudflare_mutation_authority: `NONE`
- public_domain_authority: `NONE`
- edge_trust_authority: `NONE`
- DB_migration_authority: `ONE_NARROW_COMPATIBILITY_MIGRATION_IF_REQUIRED`
- hosted_exact_smoke_reconciliation_authority: `YES_AFTER_SOURCE_PROOF`
- new_DB_login_role_authority: `NONE`
- broad_DB_grant_authority: `NONE`
- temporary_Railway_SSH_key_authority: `ONE_EPHEMERAL_KEY_IF_REQUIRED`

## Goal

Close the narrow implementation gap exposed by the 0125 real smoke:

```text
P1-5 physical provider operation:
DISPATCH_STARTED -> OUTCOME_UNKNOWN

Public Live aggregate:
remains expired ADMITTED with held reservation/slot/claim/pin
```

Implement the already accepted invariant:

```text
UNKNOWN physical outcome
→ no blind retry
→ immutable quarantine evidence
→ conservative liability
→ mediated terminal Public Live reconciliation
```

Then reconcile exactly the one retained 0125 smoke.

Do NOT release Public Live.

## accepted authority — do not redesign

The following remain accepted and must not be superseded silently:

- `P1_5_PUBLIC_LIVE_SEMANTIC_LIFECYCLE_V1`;
- P1-5 is the sole physical provider lifecycle owner;
- `P1-5 DISPATCH_STARTED` is the canonical marker that a remote send MAY have occurred;
- UNKNOWN is never retryable before reconciliation;
- Public Live semantic/provider projections must not become a competing physical-send truth;
- one RUNNING P1 attempt may contain bounded sequential operations;
- exact four `ExecutionStatus` values remain unchanged;
- no new WorkflowState values;
- capability/secret mediation remains P1-3/P1-5 owned;
- worker claim/fence authority remains durable and mediated;
- Replay executes zero provider/tool/process/network/secret side effects.

If implementation requires changing any of these load-bearing semantics:

`P1_5_BASELINE_SUPERSESSION_REQUIRED`

and STOP.

## starting Git/provenance state

Expected remote:

`origin/main = 3465d0f5eb5b2a390923907d54496f25860c50f0`

Executor previously reported local-only commit:

`01e5e02383c64d4a72bbc5b2c713b3fd23adb94e`

with parent `3465d0f5eb5b2a390923907d54496f25860c50f0`.

Before any source work:

1. verify local HEAD exactly;
2. verify `01e5e02383c64d4a72bbc5b2c713b3fd23adb94e` contains only:
   - supplied 0125 Cycle;
   - supplied 0125 Judgment;
   - supplied 0125 Handoff;
   - 0125 Task moved to `tasks/done`;
3. verify no product/source change exists in that commit;
4. verify index state;
5. verify rollback release-surface bytes equal the pre-release baseline tree.

If the local commit differs:

`PREDECESSOR_GOVERNANCE_COMMIT_IDENTITY_MISMATCH`

and STOP without reset/rebase/amend.

### governance push authority

After proving:

- Public control disabled;
- public ingress domains 0;
- edge trust absent;
- Replay-only frontend exact;
- no provider resend/new run;

this Task explicitly authorizes pushing the verified governance-only `01e5e02383c64d4a72bbc5b2c713b3fd23adb94e` commit even though the retained UNKNOWN evidence still exists.

Reason: canonical provenance must not remain local-only.

Treat repository-connected passive deployments as known coupling and re-verify fail-closed state after push.

## exact retained smoke selection

Do not identify the target only from a manually copied run ID.

Fresh hosted evidence must select exactly one run satisfying all of:

- created by the 0125 release smoke lineage;
- not the historical 1919 run;
- expired;
- current Public Live run state `ADMITTED`;
- settlement absent;
- reservation `HELD`;
- reservation amount `200000 micro-USD`;
- slot occupied by the run;
- worker work present and `recovery_required=true`;
- exactly one unreleased worker claim;
- exactly one open dispatch pin;
- exactly one linked P1-5 provider operation;
- provider operation crossed `DISPATCH_STARTED`;
- provider operation current durable outcome is `OUTCOME_UNKNOWN`;
- provider ambiguity classification corresponds to timeout/transport unknown;
- no known provider response exists;
- no tool operation exists;
- no provider retry/resend exists;
- no second 0125 public smoke exists.

If zero or more than one match:

`UNKNOWN_SMOKE_TARGET_IDENTITY_AMBIGUOUS`

and STOP.

## root-cause / contract audit

Before mutation, map the exact current production path:

```text
Public admission
→ start authority
→ durable worker claim
→ P1-5 operation
→ worker dispatch pin
→ P1-5 DISPATCH_STARTED
→ adapter transport
→ P1-5 OUTCOME_UNKNOWN
```

Identify why the durable P1-5 UNKNOWN truth does not currently produce all required Public Live consequences:

- aggregate UNKNOWN/failure projection;
- conservative provider liability accounting;
- reservation settlement;
- slot release;
- dispatch-pin terminalization;
- worker-claim release;
- worker-work terminal/recovery closure.

Distinguish:
- what existing source already does correctly;
- what missing bridge/reconciler function is required;
- what is only an operator reconciliation concern;
- what needs persistent product source.

Do not create an independent provider-send truth.

## required semantic end state

The source fix must support this general rule for Public Live provider UNKNOWN:

1. canonical physical truth remains the P1-5 operation/event;
2. the linked Public Live run becomes fail-closed and non-successful;
3. no retry/new physical operation is authorized from UNKNOWN;
4. liability is conservative, never assumed zero;
5. worker dispatch pin can become terminally reconciled only from the exact authoritative UNKNOWN evidence;
6. stale/unreleased worker claim is released only after the pin/reconciliation invariant is satisfied;
7. worker work becomes non-claimable/terminal;
8. reservation is settled through mediated accounting;
9. slot/outbox capacity is released by canonical settlement;
10. audit evidence remains immutable.

### final public run state

Prefer the existing accepted state vocabulary.

For an expired run with unresolved remote provider outcome, the expected final public projection is:

`FAILED_TIMEOUT`

only if the existing state-machine semantics can truthfully derive it through an authoritative UNKNOWN intermediate/reconciliation path.

Do NOT add a new WorkflowState.

If the accepted existing Public Live state machine cannot terminalize this truthfully without a new semantic decision:

`PUBLIC_UNKNOWN_TERMINALIZATION_CONTRACT_GAP`

and STOP after source/design evidence. Do not invent a state.

## conservative provider liability

The remote provider receipt is unknown.

Therefore:

```text
definitely-not-sent cost:
NOT APPLICABLE

actual provider charge:
UNKNOWN / do not claim

accounting settlement:
CONSERVATIVE BOUNDED LIABILITY
```

Derive the exact conservative liability from current canonical provider/profile/operation authority.

Current source lineage suggests a one-request maximum liability of `4400 micro-USD`.

Treat `4400` as an expected cross-check only.

Do not hard-code it into an operator script or report as actual provider spend.

If the canonical derivation is `L` and is valid:

Expected budget transformation from the current 200000 hold is semantically:

```text
held:
-200000

settled:
+L

available:
+(200000 - L)
```

for both campaign and current UTC-day ledgers, subject to canonical actual DB accounting rules.

Verify actual deltas.

If `L < 0`, `L > 200000`, differs across authoritative sources, or cannot be proved:

`UNKNOWN_PROVIDER_LIABILITY_NOT_PROVABLE`

and STOP before settlement.

## source / migration boundary

Prefer a narrow source correction using existing tables and roles.

One additive compatibility migration is authorized only if required to expose a mediated exact reconciliation primitive or predicate for the already accepted UNKNOWN semantics.

Allowed migration characteristics:

- additive/narrow;
- no new provider-send truth table;
- no destructive historical rewrite;
- no new DB login;
- no new DB role;
- no broad/table DML grants to runtime identities;
- PUBLIC revoked;
- exact existing role/function authority only;
- existing historical 0125 evidence remains readable.

If more than one migration, broad role redesign, or schema authority expansion is required:

`UNKNOWN_RECONCILIATION_MIGRATION_SCOPE_EXPANSION_REQUIRED`

and STOP.

## worker pin / claim requirements

Current unknown evidence has one open dispatch pin and one unreleased claim.

The fix must not simply delete or raw-update them.

A successful mediated reconciliation must prove:

- exact pin belongs to the exact UNKNOWN P1-5 operation;
- exact UNKNOWN outcome event is authoritative;
- pin is terminally closed/quarantined with immutable evidence;
- worker claim becomes releasable only after pin closure;
- claim is released exactly once;
- worker work remains preserved as lineage but is no longer claimable;
- restart cannot rediscover/re-send this operation.

No direct table deletion.

No blind `released_at` or `closed_at` mutation outside a mediated authority function.

## P1-5 / Public Live projection requirements

The source fix must preserve:

```text
physical send truth:
P1-5 operation/events

Public Live projection:
derived/reconciled consequence
```

Required regression:

- P1-5 `DEFINITELY_NOT_SENT` still follows known-closed/retry policy;
- P1-5 `PROVIDER_COMPLETED` behavior unchanged;
- P1-5 `OUTCOME_UNKNOWN` never retries;
- Public Live UNKNOWN cannot remain indefinitely claimable;
- public run cannot report success from UNKNOWN;
- settlement cost cannot become 0 merely because legacy `public_dispatch` rows are absent;
- legacy compatibility rows are not treated as authoritative if P1-5 physical operation truth exists.

## focused deterministic tests

Before hosted mutation, add/run focused PostgreSQL tests proving at minimum:

1. one Public Live operation reaches `DISPATCH_STARTED`;
2. durable P1-5 outcome becomes UNKNOWN;
3. no second provider operation can be created/sent;
4. exact worker pin becomes quarantine/reconciliation-bound;
5. claim/work are not rediscoverable;
6. conservative liability is derived from canonical operation/profile authority;
7. mediated reconciliation settles exactly once;
8. reservation/slot/outbox deltas are exact;
9. public run terminalizes truthfully under existing state vocabulary;
10. second reconciliation is idempotent;
11. provider actual receipt is never inferred;
12. no raw provider output/secret is required;
13. known-completed and definitely-not-sent paths do not regress;
14. migration empty/head and predecessor->head paths PASS if a migration is added.

Also run:
- directly affected P1-5/Public Live integration tests;
- worker claim/fence tests;
- Ruff;
- formatter check;
- narrow mypy for changed production owners;
- `git diff --check`;
- secret-safe scan.

No real provider call.

## hosted exact smoke reconciliation

Only after source/tests are accepted locally and any authorized migration is successfully applied:

1. reselect exact target by the strict hosted predicate above;
2. capture pre-state;
3. derive canonical conservative liability `L`;
4. use the new/existing mediated reconciliation path;
5. do not call provider;
6. do not create a new run;
7. do not retry the UNKNOWN operation;
8. do not mutate historical 1919 evidence.

Successful post-state must include:

```text
target public run:
truthful terminal failed state
(expected FAILED_TIMEOUT if canonical path proves it)

target settlement:
PRESENT

settled accounting liability:
L

reservation:
SETTLED

slot:
FREE / no run_id

outbox:
CLOSED

open worker dispatch pins for target:
0

unreleased worker claims for target:
0

worker work:
retained / non-claimable

provider operations:
still exactly 1

provider resend:
0

tool operations:
0
```

Campaign/day held liability for the smoke must become 0.

Do not claim `L` is the provider's actual billed amount.

## idempotency

Perform a safe second reconciliation invocation/equivalent check only if supported by the canonical path.

Must prove:
- no second SETTLE event;
- no second budget delta;
- no second pin/claim close event beyond idempotent replay semantics;
- no state regression;
- no provider call.

## hosted safe state after reconciliation

Must remain:

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
enabled=false / api_origin=null

Replay:
PUBLIC / unchanged

provider secret:
worker-only / sealed / service-local
```

## temporary operator transport

At most one ephemeral Railway SSH key may be used if required.

Same cleanup contract as prior Tasks:

- no key bytes exported;
- no public DB endpoint;
- remove Railway key;
- remove local private/public key files;
- remove helper material;
- prove cleanup by metadata/count only.

Cleanup failure:

`TEMP_OPERATOR_ACCESS_CLEANUP_FAILED`

and STOP with Public Live disabled.

## no release authority

This Task does NOT authorize:

- Public Live enablement;
- public ingress domain;
- edge trust;
- Cloudflare release binding;
- frontend Live enablement;
- provider call;
- public smoke;
- second run;
- Human final public-site smoke.

The previous Human `RELEASE_PUBLIC_LIVE` decision is consumed and cannot be reused.

## acceptance target

Success:

```text
P1_5_PUBLIC_LIVE_UNKNOWN_RECONCILIATION_ACCEPTED
/
0125_SMOKE_LIABILITY_RECONCILED
/
REPLAY_ONLY_SAFE
/
FRESH_READINESS_REQUIRED
/
BROWSER_REVIEW_REQUIRED
```

Blockers include:

```text
PREDECESSOR_GOVERNANCE_COMMIT_IDENTITY_MISMATCH
UNKNOWN_SMOKE_TARGET_IDENTITY_AMBIGUOUS
P1_5_BASELINE_SUPERSESSION_REQUIRED
PUBLIC_UNKNOWN_TERMINALIZATION_CONTRACT_GAP
UNKNOWN_PROVIDER_LIABILITY_NOT_PROVABLE
UNKNOWN_RECONCILIATION_MIGRATION_SCOPE_EXPANSION_REQUIRED
HOSTED_UNKNOWN_RECONCILIATION_FAILED
TEMP_OPERATOR_ACCESS_CLEANUP_FAILED
```

## successor sequence after Browser acceptance

Do not issue/reuse release authority from this Task.

Required later sequence:

1. fresh re-release readiness;
2. NEW Human `RELEASE_PUBLIC_LIVE` or `KEEP_REPLAY_ONLY` decision;
3. only then a separately authorized release attempt.

## canonical persistence / Git

Persist supplied Cycle/Judgment/Handoff and move this Task active -> done.

Known predecessor local governance commit may be pushed after its exact identity and fail-closed state are verified.

Source/migration/test changes may be committed/pushed only within this Task scope.

Repository-connected passive deployments must not expose a public ingress or enable control.

No amend/rebase/force-push.

Target export remains ignored/untracked.

## required export

Create:

`.aiassistant/reports/target/20260919_0240_aiscc-p3-3-l8-p1-5-unknown-outcome-propagation-and-smoke-liability-reconciliation-1/`

Required root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `PREDECESSOR_GOVERNANCE_PROOF.md`
- `UNKNOWN_TARGET_IDENTITY.md`
- `UNKNOWN_LIFECYCLE_ROOT_CAUSE.md`
- `SOURCE_REWORK_AUDIT.md`
- `MIGRATION_PROOF.md` if migration exists, otherwise explicit `MIGRATION_NOT_REQUIRED.md`
- `UNKNOWN_LIFECYCLE_TESTS.md`
- `CONSERVATIVE_LIABILITY_PROOF.md`
- `HOSTED_STATE_BEFORE.md`
- `UNKNOWN_RECONCILIATION_RESULT.md`
- `LEDGER_CONSERVATION.md`
- `WORKER_PIN_CLAIM_RECONCILIATION.md`
- `IDEMPOTENCY_PROOF.md`
- `FINAL_SAFE_STATE.md`
- `TEMP_OPERATOR_ACCESS_PROOF.md`
- `WORKSPACE_STATE.md`
- changed source/test/migration/governance files preserving repository-relative paths

Also create adjacent result ZIP and report SHA-256.

Never export:
- provider key or masked identifier;
- DB DSN/password;
- SSH private/public key material;
- HMAC key;
- read capability;
- raw provider response/output;
- raw prompt/private protocol;
- private reasoning.

## final response format

1. result
2. target bundle path + ZIP SHA-256
3. predecessor governance push result
4. source/migration commits
5. root cause
6. canonical UNKNOWN authority mapping
7. conservative liability derivation
8. hosted reconciliation result
9. ledger deltas
10. worker pin/claim/work result
11. idempotency
12. provider calls/resends
13. final Replay/Public Live state
14. temporary access cleanup
15. unverified/blockers
