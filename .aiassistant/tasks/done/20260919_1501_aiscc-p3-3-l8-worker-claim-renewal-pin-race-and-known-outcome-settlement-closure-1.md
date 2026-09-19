# 작업지시서: P3-3 L8 Worker Claim Renewal/Dispatch Pin Race + P1-5 Known-Outcome Settlement Closure

## meta

- task_id: `20260919_1501_aiscc-p3-3-l8-worker-claim-renewal-pin-race-and-known-outcome-settlement-closure-1`
- created_at: `2026-09-19T15:01:00+09:00`
- work_type: `WORKER_CONCURRENCY_REPAIR_AND_HOSTED_KNOWN_OUTCOME_RECONCILIATION`
- evidence_profile: `HIGH_RISK`
- execution_model: `THIN_CC_THICK_EXECUTOR`
- exact_baseline: `29ce5ce4b39958558091862c345c749584fd2d0f`
- fresh_ide_chat_required: `No`
- public_release_authority: `NONE`
- public_run_authority: `NONE`
- real_provider_call_authority: `NONE`
- provider_retry_resend_authority: `NONE`
- public_control_enable_authority: `NONE`
- PARKED_topology_mutation_authority: `KEEP_EXISTING / HEALTH_REPROOF_ONLY`
- full_teardown_authority: `NONE_UNLESS_NEW_SECURITY_BOUNDARY_FAILURE`
- worker_source_change_authority: `NARROW_CLAIM_VERSION_SYNCHRONIZATION_REPAIR`
- DB_migration_authority: `ONE_NARROW_0026_KNOWN_OUTCOME_RECONCILIATION_MIGRATION_IF_PROVEN_REQUIRED`
- hosted_DB_mutation_authority: `EXACT_RETAINED_THIRD_SMOKE_SETTLEMENT_ONLY`
- DB_role_grant_authority: `RECONCILER_FUNCTION_EXECUTE_ONLY_IF_MIGRATION_0026_CREATED`
- new_DB_login_authority: `NONE`
- Cloudflare_mutation_authority: `NONE`
- temporary_Railway_SSH_key_authority: `ONE_EPHEMERAL_KEY_IF_REQUIRED`

## Goal

Close both:

1. `PUBLIC_WORKER_CLAIM_RENEWAL_DISPATCH_PIN_RACE`
2. `P1_5_KNOWN_OUTCOME_FAILED_EXECUTION_SETTLEMENT_GAP`

while keeping the accepted `PARKED_FAIL_CLOSED` topology assembled and disabled.

Do NOT release Public Live.

Do NOT make a real provider call.

## accepted entry state

```text
Git main:
29ce5ce4b39958558091862c345c749584fd2d0f

Public Live:
NOT_RELEASED

public_control.enabled:
FALSE

frontend:
Replay-only / enabled=false / api_origin=null / CSP self-only

PARKED ingress:
public domain PRESENT
exact release origin PRESENT
edge-trust binding PRESENT
healthy

migration head:
20260919_0025

historical 1919:
FAILED_NOT_DISPATCHED / SETTLED 0

historical 0125:
FAILED_TIMEOUT / SETTLED conservative 4400

historical 1145:
FAILED_TIMEOUT / SETTLED conservative 4400

third 1335 smoke:
expired ADMITTED / unsettled

campaign:
available 14791200
held 200000
settled 8800

provider request blocker:
CLOSED by actual PROVIDER_COMPLETED

fixed tool blocker:
CLOSED by actual TOOL_COMPLETED
```

## Phase A — exact preflight and retained-target identity

Verify:
- `HEAD == origin/main == 29ce5ce4b39958558091862c345c749584fd2d0f`;
- migration head 0025;
- control false;
- no new public run after the 1335 smoke;
- no provider send after the one 1335 physical send;
- PARKED ingress domain/origin/edge trust still present;
- ingress healthy;
- frontend Replay-only;
- provider secret worker-only.

Select the retained smoke by strict hosted predicates, not copied ID alone.

Exactly one target must satisfy:

```text
lineage:
the sole new 1335 third-release smoke

deadline:
expired

public state:
ADMITTED

settlement:
absent

reservation:
HELD / amount 200000 / settled_cost NULL

slot:
OCCUPIED by target

outbox:
BOUND

execution attempt:
EXECUTION_FAILED

failure class:
RECOVERY_CONFLICT

provider operations:
exactly 2

provider op A:
DISPATCH_STARTED -> OUTCOME_KNOWN / PROVIDER_COMPLETED

provider op B:
SECURITY_ADMITTED -> OUTCOME_KNOWN / CANCELLED
and NO DISPATCH_STARTED

tool operations:
exactly 1
DISPATCH_STARTED -> OUTCOME_KNOWN / TOOL_COMPLETED

physical provider sends:
exactly 1

provider retry/resend:
0

provider UNKNOWN:
0

open claims:
0

open dispatch pins:
0

worker work:
open/retained but canonical claimable=false

SETTLE money events:
0
```

If zero or multiple matches:

`THIRD_SMOKE_KNOWN_OUTCOME_TARGET_AMBIGUOUS`

and STOP.

Capture immutable pre-mutation evidence.

## Phase B — deterministic claim-renewal race reproduction

Use disposable PostgreSQL only.

Reproduce the exact race before changing source.

The test must orchestrate barriers, not rely on timing luck.

Required interleaving:

```text
1. acquire live claim version N
2. consumer snapshots claim version N for an exact-version mediated DB action
3. pause consumer before exact-version DB function
4. renewal commits and advances durable/current claim to N+1
5. resume consumer with stale N
6. exact version check rejects it
```

At minimum reproduce against the dispatch-pin path.

Also audit whether the same race exists for:
- `worker_claim_context`;
- `worker_bind_operation`;
- any other exact claim-version mediated operation.

Record all affected consumers.

If the observed hosted failure cannot be reproduced from this race:

`WORKER_CLAIM_RENEWAL_RACE_NOT_REPRODUCED`

and STOP before speculative source change.

## Phase C — source repair boundary

Preferred invariant:

```text
A coroutine using an exact claim version for one short mediated DB authority operation
must hold a shared claim-version guard until that DB operation returns.

Renewal must acquire the same guard before reading/renewing/replacing active.ref.
```

Implement the synchronization at the `ActiveClaim` authority boundary.

Acceptable shape:
- `asyncio.Lock` or equivalent task-local async guard;
- guarded method/context-manager that supplies the current `ClaimRef`;
- renewal uses the same guard.

Required guarded consumers:
- initial exact-version claim context read;
- exact-version operation bind;
- exact-version dispatch pin/start transaction;
- any other audited exact-version consumer.

Do NOT:
- hold the guard across provider HTTP calls;
- hold it across tool execution;
- stop renewal for the whole execution;
- weaken DB exact-version predicates;
- accept stale claim versions in SQL;
- remove fencing/version checks.

The guard covers only short DB authority transactions.

After fix, deterministic race test must prove:
- renewal waits while exact-version operation is using N; OR
- consumer sees N+1 before entering the mediated function;
- no stale-version pin failure;
- no duplicate dispatch marker;
- no duplicate operation bind;
- no lease starvation.

## Phase D — regression tests for worker repair

Required:
- deterministic renewal-vs-pin race PASS;
- renewal-vs-bind race PASS if bind is affected;
- renewal-vs-context race PASS if context is affected;
- existing claim-sequence tests PASS;
- lost-response/idempotent claim replay PASS;
- worker recovery tests PASS;
- P1-5 provider/tool durable tests PASS;
- 0025 UNKNOWN reconciliation tests PASS;
- no real provider call.

Static:
- Ruff PASS;
- format PASS;
- narrow mypy PASS;
- `git diff --check` PASS.

Preserve repository encoding/EOL policy; do not create broad line-ending-only diffs.

## Phase E — audit existing known-outcome settlement authority

Before creating migration 0026, determine whether an existing mediated canonical path can settle the retained target truthfully.

Critical rule:

The old `ReconciliationService.close()` derives cost from legacy `public_dispatch` markers.

If the retained P1-5 run has no applicable legacy dispatch rows and that path would derive `0`, it is NOT a valid settlement path because one real provider send occurred.

Do not use:
- raw table UPDATE;
- operator-supplied zero;
- UNKNOWN reconciliation;
- FAILED_NOT_DISPATCHED reconciliation.

Required accounting principle:

```text
provider operation crossed DISPATCH_STARTED:
billable conservative liability exists

provider operation cancelled before DISPATCH_STARTED:
zero provider liability

fixed in-process tool:
zero provider liability
```

If durable exact provider input/output usage is sufficient to derive a trustworthy actual charge under the accepted pricing contract, document and use the canonical calculation.

If exact actual charge is not durably provable, use the accepted conservative per-physical-send liability:

`conservative_request_liability_micro(hosted_luna_profile())`

Current expected cross-check for exactly one dispatched provider request:

`4400 micro-USD`

This is a conservative accounting liability, not a claim about the actual OpenAI bill.

## Phase F — migration 0026 only if required

If no existing mediated path can settle the P1-5 known-outcome failed execution correctly, one new migration is authorized.

Expected revision:

`20260919_0026`

Expected purpose:

`public_live_known_outcome_failed_execution_reconciliation`

Provide narrow mediated functions such as:

```text
known_failed_execution_reconciliation_candidates()
reconcile_known_failed_execution_run(bytea)
```

Exact naming may follow repository convention.

### candidate predicate

A candidate must prove the exact durable P1-5 pattern from Phase A.

At minimum:
- expired ADMITTED;
- HELD 200000;
- BOUND outbox;
- occupied slot;
- execution attempt `EXECUTION_FAILED`;
- failure class/evidence consistent with `RECOVERY_CONFLICT`;
- one provider operation with `DISPATCH_STARTED` and known completed outcome;
- one local fixed-tool operation completed;
- one later provider operation cancelled before dispatch;
- no UNKNOWN operation;
- provider physical send count exactly 1;
- retry 0;
- open claims/pins 0;
- canonical claimable work false;
- control disabled;
- no legacy public dispatch ambiguity;
- no prior SETTLE.

### settlement behavior

Required post-state:

```text
public run:
FAILED_SAFETY
unless current canonical state semantics prove a more truthful existing terminal state

reservation:
SETTLED

settled_cost:
derived conservative/actual canonical liability

slot:
FREE

outbox:
CLOSED

held:
0

SETTLE:
exactly 1

worker work:
retained lineage, terminal/nonclaimable;
close canonically if the new bridge owns that invariant

provider operations:
unchanged

provider completed physical truth:
unchanged

cancelled-before-dispatch provider truth:
unchanged

tool truth:
unchanged
```

`FAILED_PROVIDER` must NOT be used merely because a provider was involved; the provider completed successfully.

If no existing public terminal state truthfully represents this system-owned safety/authority failure, STOP with:

`PUBLIC_RUN_TERMINAL_STATE_MODEL_EXPANSION_REQUIRED`

Do not silently invent a new state in this Task.

### ACL

- revoke PUBLIC execute;
- grant only `aiscc_public_live_reconciler`;
- no new login;
- no table DML grant expansion;
- no runtime/ingress/worker authority broadening.

### idempotency

Second invocation:
- no second SETTLE;
- no second ledger delta;
- no state regression;
- exact same evidence digest.

## Phase G — local migration/reconciliation tests

If 0026 is created:

Required:
1. candidate exact positive case;
2. reject provider UNKNOWN;
3. reject provider op without DISPATCH_STARTED;
4. reject two physical provider sends if v1 predicate only accepts one;
5. reject tool not completed;
6. reject later provider if it crossed DISPATCH_STARTED;
7. reject retry/resend;
8. reject active control;
9. reject open claim/pin;
10. reject prior SETTLE;
11. cost/liability matches Python accepted profile helper;
12. post-state conservation exact;
13. idempotent replay;
14. 0025 UNKNOWN path unchanged;
15. 0024 -> 0025 -> 0026 migration compatibility;
16. PUBLIC execute revoked / reconciler only.

Whole directly affected persistence selection must pass.

## Phase H — commit/push and hosted migration

Expected changes:
- narrow worker concurrency source;
- focused worker concurrency tests;
- migration 0026 + focused tests only if Phase E proves required;
- governance/task lifecycle.

No frontend release change.

Fast-forward only.
No amend/rebase/force.

Before push:
- control false;
- PARKED ingress healthy;
- no provider call;
- no active/future public run.

After push/passive deploy:
- PARKED ingress remains healthy;
- domain/origin/edge trust remain exact;
- no public admission;
- provider calls 0.

If 0026 exists:
- apply exact migration to hosted PostgreSQL;
- verify head 0026;
- verify ACL;
- no other DB mutation.

## Phase I — exact retained-smoke settlement

Only after source/migration tests pass.

Re-select the target by the same strict predicate.

Invoke only the accepted mediated known-outcome reconciliation.

Expected liability:
- one physical provider dispatch only;
- conservative expected cross-check `4400` if exact usage is not durably provable.

Expected campaign transition from entry:

```text
held:
200000 -> 0

settled:
8800 -> 13200   (if liability=4400)

available:
14791200 -> 14986800  (if liability=4400)

conservation:
15000000 exact
```

Verify actual values rather than forcing these numbers.

Physical provider truth must not change.

No provider call.

## Phase J — deploy repaired worker

Deploy the existing worker service to the exact repaired source.

Constraints:
- same service;
- same region;
- same replica count;
- same start command;
- same DB binding;
- same worker-only provider secret;
- public domain 0.

No real provider call and no public run.

Prove:
- service SUCCESS;
- runtime fixed-source identity exact;
- healthy EMPTY acquisition;
- no `CLAIM_SEQUENCE_DENIED`;
- no renewal/pin failure in bounded idle/read-only evidence.

## Phase K — final PARKED readiness proof

Freshly verify:

```text
Public control:
FALSE

Public Live:
NOT_RELEASED

frontend:
Replay-only

PARKED ingress:
domain/origin/edge trust retained
healthy
valid request -> LIVE_DISABLED
invalid Origin -> denied

migration:
0026 if created, otherwise existing canonical head

third smoke:
terminally reconciled
reservation SETTLED
slot FREE
outbox CLOSED
held 0
claim/pin 0
claimable work 0

1919/0125/1145:
unchanged

provider calls during this Task:
0

new public runs:
0

provider secret:
worker-only / sealed
```

## success target

```text
WORKER_CLAIM_RENEWAL_DISPATCH_PIN_RACE_FIXED
/
THIRD_SMOKE_KNOWN_OUTCOME_RECONCILED
/
PARKED_FAIL_CLOSED_READY
/
NEW_HUMAN_RELEASE_DECISION_REQUIRED
/
BROWSER_REVIEW_REQUIRED
```

Do not release Public Live.

## blockers

Use the narrowest exact blocker:

```text
THIRD_SMOKE_KNOWN_OUTCOME_TARGET_AMBIGUOUS
WORKER_CLAIM_RENEWAL_RACE_NOT_REPRODUCED
WORKER_CLAIM_VERSION_GUARD_SCOPE_EXPANSION_REQUIRED
WORKER_CLAIM_RACE_TEST_FAILED
KNOWN_OUTCOME_LIABILITY_NOT_PROVABLE
KNOWN_OUTCOME_MEDIATED_SETTLEMENT_UNAVAILABLE
PUBLIC_RUN_TERMINAL_STATE_MODEL_EXPANSION_REQUIRED
MIGRATION_0026_SCOPE_EXPANSION_REQUIRED
MIGRATION_0026_TEST_FAILED
HOSTED_KNOWN_OUTCOME_RECONCILIATION_FAILED
LEDGER_CONSERVATION_REGRESSION
WORKER_DEPLOYMENT_IDENTITY_MISMATCH
WORKER_IDLE_ACQUISITION_REGRESSION
PARKED_FAIL_CLOSED_STATE_REGRESSION
TEMP_OPERATOR_ACCESS_CLEANUP_FAILED
```

## procedural correction for future smoke

Future release smoke GET polling must include the exact browser Origin header from the first read.

Do not repeat the 1335 initial headerless polling.

## temporary operator access

At most one ephemeral Railway SSH key if required.

- no public DB endpoint;
- no key bytes/private material export;
- no DB DSN/password export;
- no provider secret value read;
- remove Railway key;
- remove local keypair/helper;
- prove cleanup by metadata.

## forbidden

- Public Live release;
- control enable;
- fourth public smoke;
- real provider call/canary;
- provider resend/retry;
- frontend Live enable;
- ingress topology teardown;
- public DB;
- provider secret movement/rotation;
- weakening DB exact-version predicates;
- raw-table settlement;
- settlement cost 0 despite proven provider dispatch;
- unrelated product work;
- unrelated historical test repair.

## required export

Create:

`.aiassistant/reports/target/20260919_1501_aiscc-p3-3-l8-worker-claim-renewal-pin-race-and-known-outcome-settlement-closure-1/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `THIRD_SMOKE_TARGET_IDENTITY.md`
- `CLAIM_RENEWAL_RACE_REPRODUCTION.md`
- `CLAIM_VERSION_CONSUMER_AUDIT.md`
- `WORKER_RACE_SOURCE_FIX.md`
- `WORKER_RACE_TESTS.md`
- `KNOWN_OUTCOME_SETTLEMENT_AUTHORITY_AUDIT.md`
- `KNOWN_OUTCOME_LIABILITY_PROOF.md`
- `MIGRATION_0026_PROOF.md` if created, otherwise `MIGRATION_0026_NOT_REQUIRED.md`
- `KNOWN_OUTCOME_RECONCILIATION_RESULT.md`
- `LEDGER_CONSERVATION.md`
- `WORKER_DEPLOYMENT_PROOF.md`
- `PARKED_FINAL_READINESS.md`
- `TEMP_OPERATOR_ACCESS_PROOF.md`
- `WORKSPACE_STATE.md`
- changed source/test/migration/governance files preserving repository-relative paths

Also create adjacent result ZIP and report SHA-256.

Never export:
- provider key or masked identifier;
- DB DSN/password;
- SSH private/public key material;
- HMAC/source key;
- read capability;
- raw provider request/response/output;
- private reasoning.

## final response format

1. result
2. target ZIP SHA-256
3. target identity
4. deterministic race reproduction
5. exact affected claim-version consumers
6. source fix
7. race/regression tests
8. known-outcome settlement authority audit
9. liability derivation
10. migration 0026 if any
11. hosted settlement result
12. ledger conservation
13. worker deployment
14. provider calls/resends
15. PARKED final state
16. temporary access cleanup
17. readiness
18. Human release decision state
19. blockers/unverified
