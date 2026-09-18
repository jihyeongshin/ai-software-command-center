# 작업지시서: P3-3 L8 retained 1919 failed-not-dispatched settlement

## meta

- task_id: `20260918_2344_aiscc-p3-3-l8-retained-1919-failed-not-dispatched-settlement-1`
- created_at: `2026-09-18T23:44:00+09:00`
- work_type: `HOSTED_RECONCILIATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- exact_baseline: `81148b72613b42f228e66cabab55085438e9fe51`
- fresh_ide_chat_required: `No`
- hosted_DB_mutation_authority: `EXACT_ONE_RUN_SETTLEMENT_ONLY`
- public_release_authority: `NONE`
- public_run_authority: `NONE`
- provider_call_authority: `NONE`
- Railway_config_mutation_authority: `NONE`
- Cloudflare_mutation_authority: `NONE`

## Goal

Terminally reconcile the one retained 1919 Public Live smoke that is proven definitely not dispatched.

Use the existing mediated reconciliation/persistence contract to project it to:

`FAILED_NOT_DISPATCHED`

with zero provider cost, release/refund its held reservation, free its slot and close its outbox while preserving immutable evidence.

Do not release Public Live.

## Current accepted prerequisite state

Before this Task:

```text
Public admission:
DISABLED

Public Live:
NOT_RELEASED

ingress public domains:
0

worker public domains:
0

edge trust:
ABSENT

provider key:
worker-only / sealed / service-local

claimable work:
0

unreleased claims:
0

dispatch pins:
0

execution operations:
0

provider requests:
0

public dispatch rows:
0

active future-deadline runs:
0

real provider calls:
0
```

Affected L5/L6 reproof for the fixed-tool amendment is Browser-accepted.

## Exact target selection

Do not use a manually typed run ID unless independently matched to the database facts.

Select the target by strict hosted evidence.

There must be exactly one retained run satisfying all of:

- historical 1919 smoke lineage;
- current run state `ADMITTED`;
- deadline expired;
- settlement absent;
- reservation `HELD`;
- committed reservation = `200000` micro-USD;
- slot currently bound to this run;
- outbox not already terminally settled;
- claimable work = false;
- unreleased worker claim count = 0;
- open dispatch pin count = 0;
- Public Live dispatch count = 0;
- execution operation count = 0;
- provider request count = 0.

If zero or more than one run matches:

`FAILED_SMOKE_TARGET_IDENTITY_AMBIGUOUS`

and STOP without mutation.

## Authoritative definitely-not-sent closure proof

Lease/deadline expiry alone is insufficient.

Before closure, construct a task-bound non-secret closure evidence packet from authoritative facts including at minimum:

- target run identity;
- admitted/deadline state;
- current DB clock after deadline;
- public dispatch rows = 0;
- execution operations = 0;
- provider requests = 0;
- worker dispatch pins = 0;
- unreleased claims = 0;
- all historical claims for the target released;
- no active/future-deadline execution;
- current worker state has no claimable target;
- current ingress domains = 0;
- public control disabled.

The evidence packet must contain no credential/value/capability.

Derive a canonical SHA-256 proof from that exact packet.

The proof must mean only:

`THIS EXACT RETAINED RUN PROVED DEFINITELY_NOT_DISPATCHED`

It must not be reusable for another run.

## reconciliation authority

Use the existing:

`ReconciliationService.close(run_id, evidence, target="FAILED_NOT_DISPATCHED")`

semantic boundary and the trusted `aiscc_public_live_reconciler` persistence authority.

The current source intentionally leaves external closure verification as a later-layer responsibility.

For this one operator reconciliation, a **task-owned closure authority adapter** is authorized only if it:

1. performs the authoritative checks above itself;
2. binds the proof to the exact run and current fenced generation;
3. returns the 32-byte proof only after every required zero/no-send predicate passes;
4. exposes no HTTP/public entry point;
5. is not installed as a general runtime bypass;
6. performs no provider/network action;
7. is temporary/operator-only or narrow canonical operator code if persistence is necessary.

Do not use the synthetic test `SyntheticEvidence` as production evidence.

Do not directly invoke `settle()` or `admit_closure()` while bypassing `ReconciliationService.close()` merely for convenience.

### hosted reconciler binding

Use an already existing trusted reconciler-capable DB binding.

Do not:
- create a new database login;
- add a DB grant;
- broaden worker/ingress/API privileges.

If no existing hosted access path can exercise `aiscc_public_live_reconciler` safely:

`RECONCILER_HOSTED_BINDING_REQUIRED`

and STOP before mutation.

## expected close mechanics

Current canonical `ReconciliationService.close()` must be allowed to:

1. fence the retained outbox if needed;
2. ask closure authority for exact proof;
3. calculate conservative cost from dispatch markers;
4. admit closure through reconciler authority;
5. settle reservation;
6. project run to `FAILED_NOT_DISPATCHED`.

Because dispatch marker count is zero, expected settlement cost is:

`0 micro-USD`

Do not force that value manually if canonical calculation disagrees; mismatch => STOP.

## expected post-state

After a successful one-run close, verify exactly:

```text
target public_run.state:
FAILED_NOT_DISPATCHED

target settlement:
PRESENT

target settlement cost:
0

target reservation:
SETTLED / settled_cost=0

target slot:
FREE / no run_id

target outbox:
CLOSED

target closure observation:
exactly one accepted closure identity/proof

target SETTLE money event:
exactly one / cost 0 / refund 200000

target public dispatch rows:
0

target execution operations:
0

target provider requests:
0
```

Expected ledger conservation:

```text
campaign held:
decrease by 200000

campaign available:
increase by 200000

campaign settled:
unchanged by provider cost (0)

admission/day held:
decrease by 200000

admission/day available:
increase by 200000

day settled:
unchanged by provider cost (0)
```

Verify actual deltas rather than relying on these expectations.

## worker-work evidence

The historical `public_worker_work` row may remain as immutable execution lineage.

Do not delete it.

After run settlement it must remain non-claimable because the run is no longer in an admissible worker state.

If a canonical existing mechanism marks it closed as part of reconciliation, record that behavior.

Do not invent a worker-work deletion.

## idempotency proof

After successful close, perform a safe second invocation or equivalent canonical idempotency check only if it does not create a new proof conflict.

Expected:
- no second SETTLE event;
- no second ledger mutation;
- no state regression.

If the existing close contract returns false for identical already-settled evidence, that is acceptable.

Do not construct a different closure proof for the retry.

## no provider / no release

This Task authorizes:

```text
new public runs:
0

real OpenAI/provider calls:
0

public ingress creation:
0

edge-trust changes:
0

admission enablement:
0

Cloudflare changes:
0
```

Worker provider credential must not be resolved or used.

## final safety verification

After settlement:

- Public control remains disabled;
- Public Live remains NOT_RELEASED;
- ingress and worker domains remain 0;
- provider-secret isolation remains exact;
- provider requests remain 0;
- no claimable work;
- no unreleased claims/pins;
- Replay unchanged.

## product-source boundary

Prefer no persistent product-source change.

A task-owned operator closure adapter/script may be created only when needed to exercise the existing mediated reconciliation contract safely.

If persistent source is required:
- keep it operator-only;
- no HTTP/public route;
- no provider integration;
- narrow tests required;
- Browser review required before considering it accepted.

Do not alter schema/migrations.

## tests/checks

Required:
- pre/post DB invariant comparison;
- settlement/ledger conservation verification;
- close idempotency verification;
- target uniqueness proof;
- secret-safe export scan;
- `git diff --check`;
- exact changed-path inventory.

If persistent source changes:
- focused reconciliation tests;
- Ruff/format/narrow mypy for changed source.

No real provider test.

## stop boundaries

STOP if:

- exact target identity is ambiguous;
- any dispatch/provider evidence exists;
- unreleased claim/pin exists;
- closure proof cannot be derived without assumption;
- trusted reconciler DB binding is unavailable;
- canonical close computes nonzero cost unexpectedly;
- a DB migration/grant/new login is needed;
- provider material would need to be read;
- control becomes enabled or a public domain appears.

## acceptance target

Success:

```text
RETAINED_1919_SETTLED
/
FAILED_NOT_DISPATCHED
/
RELEASE_READINESS_ENTRY_CANDIDATE
/
BROWSER_REVIEW_REQUIRED
```

Blocked authority:

```text
RECONCILER_HOSTED_BINDING_REQUIRED
```

Ambiguous evidence:

```text
FAILED_SMOKE_TARGET_IDENTITY_AMBIGUOUS
```

No result means Public Live is released.

## canonical persistence

Persist supplied Cycle/Judgment/Handoff and move this Task active -> done.

Update current state/decision/next action truthfully.

Ordinary commit/push authorized for exact governance/task-lifecycle and any narrowly authorized operator-only code/tests if required.

Target export remains ignored/untracked.

No amend/rebase/force-push.

## target export

Create:

`.aiassistant/reports/target/20260918_2344_aiscc-p3-3-l8-retained-1919-failed-not-dispatched-settlement-1/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `TARGET_IDENTITY_PROOF.md`
- `CLOSURE_EVIDENCE_PROOF.md`
- `RECONCILER_AUTHORITY_PROOF.md`
- `HOSTED_STATE_BEFORE.md`
- `SETTLEMENT_RESULT.md`
- `LEDGER_CONSERVATION.md`
- `IDEMPOTENCY_PROOF.md`
- `FINAL_SAFE_STATE.md`
- `WORKSPACE_STATE.md`
- changed files preserving repository-relative paths

Also create adjacent result ZIP and report SHA-256.

Never export:
- provider key or masked key identifier;
- DB DSN/password;
- HMAC key;
- read capability;
- raw provider output.
