# AISCC Task — P3-3 L8 Fifth Public Live Release + Exactly-One Smoke

## meta

- task_id: `20260919_2133_aiscc-p3-3-l8-fifth-public-live-release-and-single-smoke-1`
- created_at: `2026-09-19T21:33:00+09:00`
- work_type: `FIFTH_BOUNDED_PUBLIC_RELEASE`
- evidence_profile: `HIGH_RISK`
- execution_model: `THIN_CC_THICK_EXECUTOR`
- exact_baseline: `ec2e4895b5f4d26d987a627dfb40a5b9f1451970`
- expected_migration_head: `20260919_0027`
- fresh_ide_chat_required: `No`
- Human_release_authority: `RELEASE_PUBLIC_LIVE`
- Human_release_authority_scope: `THIS_TASK_ONLY`
- Human_release_authority_consumed_on_execution: `YES`
- public_run_authority: `EXACTLY_ONE`
- real_provider_authority: `CANONICAL_RUNTIME_FOR_THAT_ONE_RUN_ONLY`
- private_provider_canary_authority: `NONE`
- manual_provider_call_authority: `NONE`
- blind_retry_resend_authority: `NONE`
- frontend_mutation_authority: `EXACT_RELEASE_ENABLE / REPLAY_ONLY_ROLLBACK`
- public_control_authority: `ENABLE_LAST / DISABLE_FIRST_ON_FAILURE`
- backend_topology_authority: `REUSE_EXISTING_PARKED`
- DB_migration_authority: `NONE`
- DB_role_grant_authority: `NONE`
- automatic_success_finalizer_authority: `NORMAL_RUNTIME_0027`
- cleanup_0025_authority: `EXACT_NEW_RUN_ONLY_AFTER_CONTROL_FALSE`
- cleanup_0026_authority: `EXACT_NEW_RUN_ONLY_AFTER_CONTROL_FALSE`
- cleanup_0027_authority: `EXACT_NEW_RUN_ONLY_AFTER_CONTROL_FALSE_AND_ONLY_IF_AUTO_FINALIZER_FAILED`
- full_teardown_authority: `ONLY_SECURITY_BOUNDARY_FAILURE`
- sixth_release_authority: `NONE`
- temporary_Railway_SSH_key_authority: `ONE_EPHEMERAL_KEY_IF_REQUIRED`

## Goal

Perform the fifth bounded Public Live release.

Execute exactly one real public smoke through the actual production release topology.

The decisive purpose is to prove that a successful canonical execution now automatically closes the Public Live projection through migration/runtime finalizer 0027.

No private provider canary.

## accepted entry contract

Expected:

```text
Git main:
ec2e4895b5f4d26d987a627dfb40a5b9f1451970

migration:
20260919_0027

Public Live:
NOT_RELEASED

public_control:
FALSE

frontend:
Replay-only / api_origin=null / self-only CSP

PARKED ingress:
domain PRESENT
exact origin PRESENT
edge trust PRESENT
healthy

worker:
exact ec2e4895b5f4d26d987a627dfb40a5b9f1451970
healthy
public domain 0

provider secret:
worker-only / sealed

campaign:
held 0

slots:
all FREE

claimable work:
0

open claims/pins:
0/0

0025 candidates:
0

0026 candidates:
0

0027 candidates:
0
```

Re-read all hosted truth; do not rely on copied values.

## Phase A — fresh release preflight

Before any release mutation verify:

### Git/source
- `HEAD == origin/main == ec2e4895b5f4d26d987a627dfb40a5b9f1451970`;
- worktree clean for release scope;
- worker deployed source exactly `ec2e4895b5f4d26d987a627dfb40a5b9f1451970`;
- migration 0027 success finalizer source present;
- claim-version guard present;
- request-contract hardening present.

### DB
- migration head 0027;
- control false;
- campaign incident null;
- held 0;
- all slots free;
- active/future public runs 0;
- claimable work 0;
- open claims/pins 0/0;
- 0025/0026/0027 candidate sets empty;
- campaign/day conservation exact.

### PARKED ingress
- existing accepted Railway public domain present;
- `PUBLIC_LIVE_API_ORIGIN` exact;
- edge trust exact/present;
- ingress healthy;
- valid Origin while disabled → safe `LIVE_DISABLED`;
- invalid Origin denied;
- malformed/missing edge identity denied;
- owner/admin routes not publicly exposed;
- no new run/provider call from reproof.

### worker/security
- worker healthy;
- provider secret only worker;
- no provider secret in ingress/API/initializer;
- no provider call after predecessor acceptance.

### frontend
- current Replay public;
- `enabled=false`;
- `api_origin=null`;
- CSP self-only;
- accepted four Replay scenarios unchanged.

Any mismatch → STOP before release.

## Phase B — frontend release enable while backend remains disabled

Bind only the accepted ingress origin.

Required release frontend:
- `live-config.json`: `enabled=true`, exact `api_origin`;
- CSP: `connect-src 'self' <exact-origin>`;
- deterministic build manifest;
- directly affected deterministic test expectation.

No unrelated UI/product changes.

Run focused frontend/build checks.

Fast-forward commit/push only.

Deploy existing Cloudflare Pages project.

Throughout Phase B:

`public_control.enabled=false`

Verify:
- production page reachable;
- release config exact;
- exact one external connect origin;
- Replay scenarios unchanged;
- no public run;
- no provider operation;
- no claim/pin.

Failure here:
- restore Replay-only;
- keep backend PARKED;
- STOP.

## Phase C — final activation gate

Immediately before enabling control re-read:
- migration 0027;
- ingress healthy;
- worker healthy exact source;
- control false;
- held 0;
- slots free;
- open claim/pin 0;
- 0025/0026/0027 candidates empty;
- no run created during frontend release.

Then enable only the existing `public-live-v1` control.

Control enablement is LAST.

Immediately verify:
- enabled true;
- correct campaign;
- incident null;
- cutoff future;
- budget/slots sane;
- zero run before smoke.

## Phase D — exactly one fifth public smoke

Create exactly ONE run using:
- scenario `stockroom-s1-normal`;
- version `1.0.0`;
- one fresh idempotency key;
- exact browser/public Origin;
- ONE POST only.

Never repeat POST if response is lost or delayed.

Retain read capability only in process memory and never export it.

### polling

Every GET from the FIRST poll must include the exact Origin.

Poll only the same run.

No headerless probe.

### forbidden during smoke
- second run;
- private provider canary;
- manual provider call;
- alternate model/provider;
- blind resend;
- raw DB state mutation;
- direct worker invocation.

## Phase E — required automatic-success proof

A successful release requires all of the following to happen automatically as part of normal runtime.

### execution
- exact one admitted public run;
- P1-5 attempt reaches `EXECUTOR_COMPLETED`;
- all operations terminal;
- no `OUTCOME_UNKNOWN`;
- accepted provider/tool bounds maintained;
- no blind retry/resend.

### claim boundary
- execution claim released canonically;
- open claim 0;
- open pin 0.

### automatic 0027 finalization
Without any operator/reconciler manual call:
- `public_run.state = COMPLETED`;
- reservation `SETTLED`;
- settled cost/liability derived by 0027;
- slot `FREE`;
- outbox `CLOSED`;
- worker work `CLOSED / SUCCESS_RECONCILED`;
- success candidate set becomes empty;
- SETTLE exactly once;
- ledger conservation exact.

### governance invariant
The corresponding core WorkRun must NOT be automatically marked Browser/Human accepted.

Expected:

`EXECUTOR_COMPLETED != WorkRun.ACCEPTED`

No runtime Judgment or Project closure.

### provider/tool physical truth
- provider operations remain their physical known outcomes;
- tool remains local fixed tool;
- success finalizer must not create provider/tool operations.

If all PASS:
- KEEP control enabled;
- KEEP frontend Live enabled;
- KEEP ingress released;
- export evidence;
- stop for Browser review.

Success target:

```text
PUBLIC_LIVE_RELEASED
/
FIFTH_SINGLE_PUBLIC_SMOKE_PASS
/
AUTO_SUCCESS_FINALIZATION_PASS
/
BROWSER_REVIEW_REQUIRED
/
HUMAN_PUBLIC_SITE_SMOKE_PENDING
```

Executor cannot close L8.

## Phase F — any material failure after activation

First action:

`public_control.enabled=false`

FIRST.

Prove:
- second admission impossible;
- run count remains exactly one.

Then restore frontend Replay-only:
- `enabled=false`;
- `api_origin=null`;
- CSP self-only;
- deterministic manifest/tests;
- deploy rollback.

KEEP backend PARKED:
- ingress domain KEEP;
- exact origin KEEP;
- edge trust KEEP;
- ingress healthy KEEP;
- worker KEEP;
- provider secret topology KEEP.

Do not full teardown for ordinary execution/finalization failure.

## Phase G — cleanup classification after rollback

Only after control=false and frontend rollback.

### G1 — provider UNKNOWN exact pattern

If exact fifth run matches 0025:
- invoke 0025 for that run only;
- no resend;
- conservative liability;
- held 0;
- slot free;
- outbox closed;
- claim/pin 0;
- idempotent replay.

Release result remains FAILED/PARKED.

### G2 — known failed execution exact pattern

If exact fifth run matches 0026:
- invoke 0026 for that run only;
- preserve provider/tool physical truth;
- settle exact conservative liability;
- held 0;
- slot free;
- outbox closed;
- claim/pin 0;
- idempotent replay.

Release result remains FAILED/PARKED.

### G3 — successful execution but automatic finalizer failure

If execution attempt reached `EXECUTOR_COMPLETED` but Public Live did NOT automatically reach `COMPLETED/SETTLED`:

This is:

`AUTO_SUCCESS_FINALIZATION_FAILED`

The release is FAILED.

Do not leave control enabled merely because execution succeeded.

After rollback to PARKED:
1. prove exact one successful retained run;
2. prove no open claim/pin;
3. prove strict 0027 candidate;
4. invoke 0027 canonically for cleanup;
5. prove COMPLETED/SETTLED/FREE/CLOSED;
6. prove provider call count did not change.

Manual 0027 cleanup does NOT convert the fifth release result into PASS.

### G4 — uncovered pattern

If no accepted predicate matches:

`FIFTH_SMOKE_RETENTION_PATTERN_UNCOVERED`

Do not force settlement.

Preserve evidence and STOP.

## Phase H — security-boundary failure

Full teardown only if fresh evidence proves:
- admission while control=false;
- invalid Origin/edge identity accepted;
- provider secret outside worker;
- owner/admin route publicly exposed;
- public DB exposed;
- new provider dispatch continues after control=false;
- PARKED boundary cannot be restored.

Then:
1. control false first;
2. frontend Replay-only;
3. remove public ingress domain;
4. remove release origin;
5. remove edge trust;
6. preserve evidence;
7. STOP.

## Phase I — final successful public state

If success:

```text
public_control:
TRUE

frontend:
Live enabled

ingress:
released / healthy

public smoke:
COMPLETED

reservation:
SETTLED

slot:
FREE

outbox:
CLOSED

worker work:
CLOSED

open claim/pin:
0/0

held:
0

0025/0026/0027 candidates:
0

provider secret:
worker-only
```

No rollback commit.

Do not disable control after a successful smoke merely to persist governance.

## Phase J — final failed PARKED state

If failure:

```text
public_control:
FALSE

frontend:
Replay-only

backend:
PARKED / healthy

new run count:
exactly 1

second run:
0

blind resend:
0

held:
0 if an accepted cleanup path applies,
otherwise explicitly retained with blocker

provider secret:
worker-only
```

No sixth release authority.

## Git / passive deployment rules

Fast-forward only.

No amend/rebase/force.

Release commit may contain only exact frontend release changes.

On success:
- do not revert release frontend bytes;
- governance persistence commits must preserve release frontend state.

On failure:
- control false BEFORE rollback frontend commit;
- rollback release bytes exactly;
- governance persistence follows rollback.

Changed export copies must use exact Git blob bytes.

## temporary operator access

At most one ephemeral Railway SSH key if required.

- no public DB endpoint;
- no key material export;
- no DB credential export;
- no provider secret read;
- cleanup mandatory.

## forbidden

- second smoke;
- sixth release attempt;
- private provider canary;
- manual provider send;
- blind resend;
- alternate provider/model;
- new migration;
- DB role/login/grant changes;
- public DB;
- worker public domain;
- provider secret movement;
- raw-table reconciliation;
- ordinary-failure full teardown;
- manual 0027 invocation while claiming a release PASS;
- unrelated product work;
- unrelated historical test repair.

## required export

Create:

`.aiassistant/reports/target/20260919_2133_aiscc-p3-3-l8-fifth-public-live-release-and-single-smoke-1/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `RELEASE_PREFLIGHT.md`
- `PARKED_REPROOF.md`
- `FRONTEND_RELEASE_PROOF.md`
- `CONTROL_ENABLEMENT.md`
- `FIFTH_PUBLIC_SMOKE.md`
- `POLLING_ORIGIN_PROOF.md`
- `PROVIDER_OPERATION_PROOF.md`
- `TOOL_OPERATION_PROOF.md`
- `WORKER_CLAIM_PIN_PROOF.md`
- `AUTO_SUCCESS_FINALIZATION_PROOF.md`
- `ACCOUNTING_SETTLEMENT_PROOF.md`
- `RECONCILIATION_0025_PROOF.md` if cleanup used, otherwise `RECONCILIATION_0025_NOT_USED.md`
- `RECONCILIATION_0026_PROOF.md` if cleanup used, otherwise `RECONCILIATION_0026_NOT_USED.md`
- `RECONCILIATION_0027_PROOF.md` if manual cleanup used, otherwise `RECONCILIATION_0027_NOT_USED.md`
- `FINAL_PUBLIC_STATE.md`
- `PARKED_ROLLBACK_PROOF.md` if failed, otherwise `PARKED_ROLLBACK_NOT_USED.md`
- `PROVIDER_SECRET_APPLICABILITY.md`
- `TEMP_OPERATOR_ACCESS_PROOF.md`
- `WORKSPACE_STATE.md`
- changed release/governance files with exact Git blob bytes

Also create adjacent result ZIP and report SHA-256.

Never export:
- provider key or masked identifier;
- DB DSN/password;
- SSH key material;
- HMAC/source key;
- read capability;
- raw provider request/response/output;
- private reasoning.

## final response format

1. result
2. target ZIP SHA-256
3. preflight
4. PARKED reproof
5. frontend release commit/deployment
6. control enablement
7. exactly-one smoke identity
8. polling Origin proof
9. provider operations
10. tool operations
11. execution attempt terminal state
12. claim/pin release
13. automatic success-finalizer result
14. accounting/slot/outbox/work
15. cleanup reconciliation if any
16. final RELEASED or PARKED state
17. core WorkRun/Judgment invariant
18. provider-secret/security state
19. temporary access cleanup
20. Git/export byte identity
21. Browser review state
22. Human public-site smoke state
23. blockers/unverified
