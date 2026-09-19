# 작업지시서: P3-3 L8 Successful Execution → Public COMPLETED Projection and Settlement Closure

## meta

- task_id: `20260919_2027_aiscc-p3-3-l8-successful-execution-public-projection-and-settlement-closure-1`
- created_at: `2026-09-19T20:27:00+09:00`
- work_type: `SUCCESSFUL_EXECUTION_PUBLIC_TERMINALIZATION`
- evidence_profile: `HIGH_RISK`
- execution_model: `THIN_CC_THICK_EXECUTOR`
- exact_baseline: `a5418f8fd98bb0ef075b61da6e5adf002ff1a6c1`
- fresh_ide_chat_required: `No`
- Public_Live_entry_state: `NOT_RELEASED`
- public_release_authority: `NONE`
- public_run_authority: `NONE`
- real_provider_call_authority: `NONE`
- provider_retry_resend_authority: `NONE`
- frontend_Live_enable_authority: `NONE`
- public_control_enable_authority: `NONE`
- PARKED_topology_authority: `KEEP / HEALTH_REPROOF`
- production_source_change_authority: `NARROW_SUCCESS_FINALIZATION_ONLY`
- DB_migration_authority: `ONE_NARROW_0027_IF_REQUIRED`
- DB_function_grant_authority: `EXACT_SUCCESS_FINALIZER_ONLY`
- raw_table_mutation_authority: `NONE`
- retained_fourth_smoke_mutation_authority: `CANONICAL_SUCCESS_FINALIZER_ONLY`
- fifth_release_authority: `NONE`
- temporary_Railway_SSH_key_authority: `ONE_EPHEMERAL_KEY_IF_REQUIRED`

## Goal

Close:

`P1_5_SUCCESSFUL_EXECUTION_PUBLIC_CLOSURE_MISSING`

for both:
1. future normal Public Live successful executions; and
2. the exact retained fourth smoke.

The fix must make a future successful execution automatically reach a truthful terminal Public Live state without operator raw-table repair.

No real provider call in this Task.

## accepted entry state

Expected hosted state:

```text
Git main:
a5418f8fd98bb0ef075b61da6e5adf002ff1a6c1

migration:
20260919_0026

public_control:
FALSE

frontend:
Replay-only

PARKED ingress:
domain/origin/edge trust PRESENT
healthy

fourth smoke:
expired ADMITTED
reservation HELD 200000
settled_cost NULL
slot OCCUPIED
outbox BOUND
worker work open / recovery_required=false
open claims 0
open pins 0

execution attempt:
EXECUTOR_COMPLETED

provider operations:
2
both DISPATCH_STARTED
both OUTCOME_KNOWN / PROVIDER_COMPLETED

tool operations:
1
DISPATCH_STARTED
OUTCOME_KNOWN / TOOL_COMPLETED

provider UNKNOWN:
0

provider retry ancestry:
0
```

Campaign/day conservation must still hold.

## Phase A — exact preflight and target identity

Verify:
- `HEAD == origin/main == a5418f8fd98bb0ef075b61da6e5adf002ff1a6c1`;
- tracked worktree clean for task scope;
- migration 0026;
- control false;
- no new public run after fourth smoke;
- no provider call after fourth smoke;
- PARKED ingress healthy;
- frontend Replay-only;
- provider secret worker-only;
- 0025 candidates 0;
- 0026 candidates 0.

Select the retained fourth smoke by strict predicates, not copied ID alone.

Exactly one target must match the accepted successful-execution pattern.

If zero/multiple:

`FOURTH_SUCCESS_TARGET_AMBIGUOUS`

and STOP.

## Phase B — deterministic local reproduction of the missing success closure

Use disposable PostgreSQL and synthetic provider only.

Reproduce the current pre-fix behavior:

```text
public admission
→ worker claim
→ synthetic PROVIDER_COMPLETED
→ fixed TOOL_COMPLETED
→ synthetic PROVIDER_COMPLETED
→ execution attempt EXECUTOR_COMPLETED
→ claim released

BUT

public_run remains ADMITTED
reservation remains HELD
slot remains OCCUPIED
outbox remains BOUND
worker work remains open
```

No network/provider call.

The test must prove this is the exact missing bridge before changing source.

If not reproducible:

`SUCCESS_PUBLIC_CLOSURE_GAP_NOT_REPRODUCED`

and STOP.

## Phase C — audit existing mediated authority before adding 0027

Audit:
- `ReconciliationService.close()`;
- legacy `public_dispatch` accounting;
- P1-5 execution operation/event/counter evidence;
- worker release ordering;
- current DB API roles.

Do not reuse `ReconciliationService.close()` if it would derive zero or otherwise depend on absent legacy `public_dispatch` rows.

Do not backfill legacy dispatch rows merely to satisfy that older path.

Prefer one canonical P1-5-aware success closure.

If an existing exact mediated function already correctly derives success and liability from P1-5 truth, use it and document why 0027 is unnecessary.

Otherwise create migration 0027.

## Phase D — success semantics and invariants

Required invariant:

```text
EXECUTOR_COMPLETED
!=
WorkRun.ACCEPTED
```

Never:
- mark the core WorkRun ACCEPTED;
- create Browser Judgment acceptance;
- close a project/cycle from worker execution.

The success finalizer may only close the Public Live projection:

```text
public_run:
COMPLETED

reservation:
SETTLED

slot:
FREE

outbox:
CLOSED

worker work:
CLOSED / nonclaimable
```

The P1-5 execution attempt remains `EXECUTOR_COMPLETED`.

Physical provider/tool operation truths remain unchanged.

## Phase E — accepted successful execution evidence

The success closure must be derived from durable evidence, never caller-supplied success/cost.

At minimum require:
- exact Public Live campaign/scenario/profile;
- public run `ADMITTED`;
- reservation `HELD`, unsettled;
- outbox `BOUND`;
- canonical P1-5 owner binding;
- execution attempt `EXECUTOR_COMPLETED`;
- durable execution submission/output reference exists and is internally consistent;
- no operation `OUTCOME_UNKNOWN`;
- no open claim/pin at finalization point;
- no prior SETTLE;
- ledger conservation valid.

### current exact normal success shape

The observed fourth smoke has:

```text
provider op #1:
DISPATCH_STARTED
→ PROVIDER_COMPLETED

tool:
DISPATCH_STARTED
→ TOOL_COMPLETED

provider op #2:
DISPATCH_STARTED
→ PROVIDER_COMPLETED

retry ancestry:
0
```

Audit the currently authorized semantic planner/profile to determine all success variants reachable under the existing Public Live policy.

The finalizer must either:
1. safely cover every currently authorized successful variant; or
2. explicitly constrain/reject uncovered variants before release readiness.

Do not silently implement only the observed shape if the current runtime can legitimately produce another successful shape.

If this requires a broader semantic-profile redesign:

`SUCCESS_CLOSURE_VARIANT_SCOPE_EXPANSION_REQUIRED`

and STOP.

## Phase F — liability derivation

Do not claim the actual OpenAI invoice.

For each provider operation:

- no `DISPATCH_STARTED` → liability 0;
- conclusively `DEFINITELY_NOT_SENT` → liability 0;
- physical provider send with known completed outcome → derive canonical liability;
- UNKNOWN is not a success-finalizer candidate.

If durable exact input/output usage is sufficient and current accepted tariff contract permits exact computation, use the canonical exact calculation.

If exact input usage is not durably provable, use:

`conservative_request_liability_micro(hosted_luna_profile())`

for each physically dispatched provider operation that is not conclusively definitely-not-sent.

Current fourth-smoke expected cross-check:

```text
physical provider sends:
2

conservative one-send liability:
4400 micro-USD

total conservative liability:
8800 micro-USD
```

Fixed in-process tool provider liability:

`0`

The function must derive this from durable operation evidence; caller may not supply the amount.

## Phase G — migration 0027 if required

Expected revision:

`20260919_0027`

Suggested purpose:

`public_live_successful_execution_reconciliation`

Names may follow repository convention.

Provide a strict candidate/read function and one idempotent finalizer, for example:

```text
successful_execution_reconciliation_candidates()
complete_successful_execution_run(bytea)
```

### ACL principle

The finalizer must be callable automatically by the normal worker success path without granting raw table DML.

Allowed narrow authority:
- exact SECURITY DEFINER function;
- PUBLIC execute revoked;
- `aiscc_public_live_execution` execute only if required for automatic worker finalization;
- `aiscc_public_live_reconciler` execute may also be granted for retained historical cleanup;
- no new login;
- no table grant expansion;
- no ingress/initializer/API authority.

If automatic closure can be achieved without granting the execution role this function, prefer the narrower existing authority.

Document the exact decision.

### idempotency

Second call after successful closure:
- no second SETTLE;
- no second ledger delta;
- no state regression;
- exact same evidence digest / reconciled=false-or-equivalent truthful replay.

## Phase H — runtime automatic success finalization

Future successful Public Live runs must close automatically.

Preferred ordering:

```text
AgentExecutionService returns EXECUTOR_COMPLETED
→ worker stops provider/tool execution
→ claim is canonically released
→ short DB-only success finalizer runs
→ Public Live run becomes COMPLETED
```

Do not hold the claim-version guard across:
- provider HTTP;
- tool execution;
- the whole execution lifecycle.

Do not re-run provider/tool if the finalizer transiently fails.

A finalizer failure after `EXECUTOR_COMPLETED` must remain a DB-only closure/retry problem.

No provider resend authority may be created by success-finalization recovery.

If current worker-loop architecture requires a narrow post-release callback/hook, implement and test only that boundary.

## Phase I — local regression tests

Required without network:

1. pre-fix missing-closure reproduction exists as regression setup;
2. successful provider→tool→provider execution automatically closes Public Live;
3. public run becomes `COMPLETED`;
4. reservation SETTLED;
5. slot FREE;
6. outbox CLOSED;
7. worker work CLOSED/nonclaimable;
8. core WorkRun remains non-accepted / unchanged;
9. execution attempt remains `EXECUTOR_COMPLETED`;
10. provider/tool operation truth unchanged;
11. liability derived from physical provider sends only;
12. tool liability zero;
13. no UNKNOWN candidate accepted;
14. no failed execution accepted;
15. no incomplete provider/tool operation accepted;
16. no prior SETTLE accepted except idempotent replay;
17. no open claim/pin accepted at post-release finalizer boundary;
18. ledger conservation exact;
19. idempotent finalizer;
20. finalizer failure cannot cause provider resend;
21. worker claim sequence/renewal guard tests remain green;
22. 0025 UNKNOWN reconciliation unchanged;
23. 0026 known-failed reconciliation unchanged;
24. migration chain 0025→0026→0027 green if 0027 exists;
25. ACL exact.

Also:
- directly affected persistence suite PASS;
- Ruff PASS;
- format PASS;
- narrow mypy PASS;
- `git diff --check` PASS;
- secret-safe scan PASS.

## Phase J — commit/push and hosted deployment

Fast-forward only.

No amend/rebase/force.

Expected source scope:
- success-finalizer DB/repository/service boundary;
- narrow worker post-release finalization hook if required;
- migration 0027 if required;
- focused tests;
- governance lifecycle.

No frontend release changes.

Before push:
- control false;
- frontend Replay-only;
- PARKED healthy.

After push/passive deployments:
- ingress PARKED healthy;
- frontend unchanged Replay-only;
- provider calls 0;
- public runs 0 new.

If production worker source changed:
deploy existing worker service to exact new source with same region/replica/start command/DB/provider-secret bindings.

No public domain on worker.

## Phase K — hosted migration and retained fourth smoke closure

If 0027 exists:
- apply it;
- verify migration head 0027;
- verify PUBLIC revoke and exact role grants.

Re-select the retained target by strict predicate.

Invoke only the canonical success finalizer.

Do not mutate raw tables.

Required retained fourth-smoke result:

```text
public_run:
COMPLETED

reservation:
SETTLED

slot:
FREE

outbox:
CLOSED

worker work:
CLOSED / nonclaimable

open claim/pin:
0/0

provider ops:
unchanged, 2 x PROVIDER_COMPLETED

tool:
unchanged, TOOL_COMPLETED

provider calls during this Task:
0
```

Expected liability cross-check if conservative:

`8800 micro-USD`

Expected campaign cross-check if liability=8800:

```text
available:
14,978,000

held:
0

settled:
22,000

total:
15,000,000
```

Expected affected-day cross-check if liability=8800:

```text
available:
3,982,400

held:
0

settled:
17,600

total:
4,000,000
```

Verify canonical actual values, not copied arithmetic.

## Phase L — final PARKED readiness

Freshly prove:

```text
Public Live:
NOT_RELEASED

public_control:
FALSE

frontend:
Replay-only

PARKED ingress:
domain/origin/edge trust retained
healthy

fourth smoke:
COMPLETED / SETTLED

held:
0

slots:
all FREE

claimable work:
0

open claim/pin:
0/0

0025 candidates:
0

0026 candidates:
0

0027 success candidates:
0 after reconciliation

worker:
healthy exact repaired source

provider calls this Task:
0

new public runs:
0

provider secret:
worker-only / sealed
```

## success target

```text
SUCCESSFUL_EXECUTION_PUBLIC_CLOSURE_IMPLEMENTED
/
FOURTH_SMOKE_COMPLETED_AND_SETTLED
/
PARKED_FAIL_CLOSED_READY
/
NEW_HUMAN_RELEASE_DECISION_REQUIRED
/
BROWSER_REVIEW_REQUIRED
```

Do NOT release Public Live in this Task.

## blockers

Use the narrowest exact blocker:

```text
FOURTH_SUCCESS_TARGET_AMBIGUOUS
SUCCESS_PUBLIC_CLOSURE_GAP_NOT_REPRODUCED
EXISTING_SUCCESS_SETTLEMENT_AUTHORITY_AMBIGUOUS
SUCCESS_CLOSURE_VARIANT_SCOPE_EXPANSION_REQUIRED
SUCCESS_LIABILITY_NOT_PROVABLE
SUCCESS_FINALIZER_ACL_SCOPE_EXPANSION_REQUIRED
MIGRATION_0027_TEST_FAILED
SUCCESS_FINALIZER_RUNTIME_INTEGRATION_FAILED
FINALIZER_PROVIDER_RESEND_REGRESSION
HOSTED_SUCCESS_RECONCILIATION_FAILED
LEDGER_CONSERVATION_REGRESSION
WORKER_DEPLOYMENT_IDENTITY_MISMATCH
PARKED_FAIL_CLOSED_STATE_REGRESSION
TEMP_OPERATOR_ACCESS_CLEANUP_FAILED
```

## temporary operator access

At most one ephemeral Railway SSH key if required.

- no public DB endpoint;
- no key material export;
- no DB DSN/password export;
- no provider secret value read;
- remove Railway key;
- remove local helper/keypair;
- prove cleanup by metadata.

## forbidden

- fifth Public Live release;
- control enable;
- frontend Live enable;
- new public run;
- real provider call/canary;
- provider retry/resend;
- manual provider send;
- raw-table settlement;
- core WorkRun acceptance mutation;
- Browser Judgment creation by runtime;
- public DB;
- provider secret movement/rotation;
- ingress topology teardown;
- unrelated product work;
- unrelated historical test repair.

## required export

Create:

`.aiassistant/reports/target/20260919_2027_aiscc-p3-3-l8-successful-execution-public-projection-and-settlement-closure-1/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `FOURTH_SUCCESS_TARGET_IDENTITY.md`
- `SUCCESS_CLOSURE_GAP_REPRODUCTION.md`
- `SUCCESS_AUTHORITY_AUDIT.md`
- `SUCCESS_VARIANT_AUDIT.md`
- `SUCCESS_LIABILITY_PROOF.md`
- `SUCCESS_FINALIZER_SOURCE.md`
- `SUCCESS_FINALIZER_TESTS.md`
- `MIGRATION_0027_PROOF.md` if created, otherwise `MIGRATION_0027_NOT_REQUIRED.md`
- `HOSTED_FOURTH_SUCCESS_RECONCILIATION.md`
- `LEDGER_CONSERVATION.md`
- `WORKER_DEPLOYMENT_PROOF.md` if source changed, otherwise `WORKER_DEPLOYMENT_NOT_REQUIRED.md`
- `PARKED_FINAL_READINESS.md`
- `PROVIDER_SECRET_APPLICABILITY.md`
- `TEMP_OPERATOR_ACCESS_PROOF.md`
- `WORKSPACE_STATE.md`
- changed source/test/migration/governance files preserving repository-relative paths using exact Git blob bytes

Also create adjacent result ZIP and report SHA-256.

Never export:
- provider key or masked key identifier;
- DB DSN/password;
- SSH key material;
- HMAC/source key;
- read capability;
- raw provider request/response/output;
- private reasoning.

## final response format

1. result
2. target ZIP SHA-256
3. fourth target identity
4. missing-closure reproduction
5. existing authority audit
6. success semantic variant audit
7. liability derivation
8. source/runtime finalizer change
9. migration 0027 if any
10. tests/static checks
11. hosted fourth-smoke reconciliation
12. final ledger
13. worker deployment
14. provider calls/resends
15. PARKED final state
16. provider-secret/security state
17. temporary access cleanup
18. Git/export byte identity
19. Browser review state
20. Human release decision state
