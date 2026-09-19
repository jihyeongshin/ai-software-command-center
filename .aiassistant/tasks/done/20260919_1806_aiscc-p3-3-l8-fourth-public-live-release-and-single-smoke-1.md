# AISCC Task — P3-3 L8 Fourth Public Live Release + Exactly-One Smoke

## meta

- task_id: `20260919_1806_aiscc-p3-3-l8-fourth-public-live-release-and-single-smoke-1`
- created_at: `2026-09-19T18:06:00+09:00`
- work_type: `FOURTH_BOUNDED_PUBLIC_RELEASE`
- evidence_profile: `HIGH_RISK`
- execution_model: `THIN_CC_THICK_EXECUTOR`
- exact_baseline: `b1cbb8a3c130f591b5563d4b87c109785e5adddb`
- expected_parent: `29ce5ce4b39958558091862c345c749584fd2d0f`
- expected_migration_head: `20260919_0026`
- fresh_ide_chat_required: `No`
- Human_release_authority: `RELEASE_PUBLIC_LIVE`
- Human_release_authority_scope: `THIS_TASK_ONLY`
- Human_release_authority_consumed_on_execution: `YES`
- Railway_ingress_topology_authority: `REUSE_EXISTING_PARKED`
- Railway_ingress_domain_creation_authority: `NONE_UNLESS_EXISTING_ACCEPTED_DOMAIN_IS_MISSING`
- Railway_ingress_config_authority: `VERIFY_EXISTING_EXACT_ORIGIN_EDGE_TRUST`
- Railway_worker_mutation_authority: `NONE_UNLESS_HEALTH_RECOVERY_OF_EXACT_ACCEPTED_SOURCE`
- Cloudflare_mutation_authority: `EXACT_RELEASE_ENABLE / REPLAY_ONLY_ROLLBACK`
- public_control_authority: `ENABLE_LAST / DISABLE_FIRST_ON_FAILURE`
- public_run_authority: `EXACTLY_ONE`
- real_provider_authority: `CANONICAL_RUNTIME_FOR_THAT_ONE_RUN_ONLY`
- private_provider_canary_authority: `NONE`
- manual_provider_call_authority: `NONE`
- provider_blind_retry_resend_authority: `NONE`
- UNKNOWN_reconciliation_authority: `EXACT_NEW_RUN_ONLY_IF_0025_PREDICATE_MATCHES`
- known_failed_reconciliation_authority: `EXACT_NEW_RUN_ONLY_IF_0026_PREDICATE_MATCHES`
- DB_migration_authority: `NONE`
- DB_role_grant_authority: `NONE`
- full_teardown_authority: `ONLY_SECURITY_BOUNDARY_FAILURE`
- fifth_release_authority: `NONE`
- temporary_Railway_SSH_key_authority: `ONE_EPHEMERAL_KEY_IF_REQUIRED`

## Goal

Perform the fourth bounded Public Live release by reusing the already accepted PARKED topology.

Execute exactly one real public smoke.

No separate provider canary.

## accepted entry contract

Expected:

```text
Git main:
b1cbb8a3c130f591b5563d4b87c109785e5adddb

migration:
20260919_0026

Public Live:
NOT_RELEASED

public_control:
FALSE

frontend:
Replay-only

PARKED ingress:
public domain PRESENT
exact release origin PRESENT
edge trust PRESENT
healthy

worker:
repaired claim-version source deployed
healthy

provider secret:
worker-only / sealed

campaign:
held 0

slots:
all FREE

open claim/pin:
0/0

unknown reconciliation candidates:
0

known-failed reconciliation candidates:
0
```

Historical runs:
- 1919 terminal/settled;
- 0125 FAILED_TIMEOUT/settled conservative liability;
- 1145 FAILED_TIMEOUT/settled conservative liability;
- 1335 FAILED_SAFETY/settled conservative liability.

Do not trust copied values alone. Re-read current hosted truth.

## Phase A — fresh release preflight

Before any release mutation verify:

### Git/source
- `HEAD == origin/main == b1cbb8a3c130f591b5563d4b87c109785e5adddb`;
- worktree clean for release scope;
- worker deployed source identity is exactly `b1cbb8a3c130f591b5563d4b87c109785e5adddb`;
- request hardening is present;
- claim-version guard is present;
- no unreviewed production source drift.

### migration/DB
- head `20260919_0026`;
- control disabled;
- campaign incident null;
- held 0;
- all public slots free;
- active/future public run count 0;
- claimable work 0;
- open claims 0;
- open pins 0;
- 0025 candidates 0;
- 0026 candidates 0;
- campaign/day ledger conservation exact.

### PARKED ingress
- accepted Railway ingress domain still exists;
- effective `PUBLIC_LIVE_API_ORIGIN` is exact same domain origin;
- accepted Railway edge trust is present;
- ingress current deployment healthy;
- valid-origin request while control=false → safe `LIVE_DISABLED`;
- invalid Origin → denied;
- missing/malformed edge identity → denied;
- owner/admin routes not exposed;
- no new run/provider call from reproof.

### worker/security
- worker healthy;
- public domain 0;
- provider key authority worker-only;
- ingress/initializer/API have no provider key;
- no provider send after predecessor acceptance.

### frontend
- public Replay reachable as evidence permits;
- Live disabled;
- current `api_origin=null`;
- current CSP `connect-src 'self'`;
- four Replay scenarios unchanged.

Any material mismatch → STOP before release.

## Phase B — frontend release enable while backend still disabled

Use exact already-accepted ingress origin.

Change only release-bound frontend artifacts required for:
- `live-config.json`: `enabled=true`, exact `api_origin`;
- CSP `connect-src 'self' <exact-origin>`;
- deterministic replay build manifest;
- directly affected deterministic test expectations.

No product feature changes.

Run focused frontend/build tests.

Fast-forward commit/push only.

Deploy existing Cloudflare Pages project.

During all of Phase B:

`public_control.enabled` MUST remain `false`.

Verify:
- production page reachable;
- release config exact;
- exact one allowed external connect origin;
- Replay four scenarios unchanged;
- no public run;
- no provider operation;
- no claim/pin.

If frontend release deploy fails:
- restore Replay-only frontend;
- KEEP backend PARKED;
- STOP.

## Phase C — final parked gate immediately before activation

Re-read:
- ingress healthy;
- worker healthy;
- migration 0026;
- control false;
- held 0;
- slots free;
- claim/pin 0;
- reconciliation candidate sets empty;
- no run created during frontend deployment.

Then enable **only** existing `public-live-v1` control.

Control activation is LAST.

Immediately verify:
- control enabled true;
- correct campaign;
- incident null;
- cutoff still future;
- budgets valid;
- slots free;
- zero new runs before smoke.

## Phase D — exactly one fourth public smoke

Create exactly ONE public run.

Requirements:
- exact scenario `stockroom-s1-normal`;
- exact version `1.0.0`;
- one fresh idempotency key;
- exact browser/public Origin;
- one POST only;
- do not repeat POST even if client loses response;
- retain returned capability only in memory;
- do not export capability.

### polling correction

Every GET/read request from the FIRST poll must include the exact browser Origin header.

Do not repeat the 1335 headerless polling mistake.

Poll only the same run through the canonical read path.

### forbidden during smoke
- second public run;
- manual provider request;
- private canary;
- alternate model/provider;
- blind resend;
- ad hoc DB state mutation;
- direct worker invocation outside canonical queue/runtime.

## Phase E — success predicate

The smoke is successful only if the full public path reaches an unambiguous accepted terminal success.

At minimum prove:

```text
new public run count:
exactly 1

provider request:
canonical hosted gpt-5.6-luna

provider/tool protocol:
within fixed accepted phase/physical bounds

fixed stockroom_summary:
only allowed tool

provider UNKNOWN:
0

execution attempt:
terminal successful state

public run:
truthful accepted success/terminal projection

reservation:
SETTLED

slot:
FREE

outbox:
CLOSED

open claim/pin:
0/0

claimable work:
0

retry/resend:
0 unless an already accepted canonical semantic retry is explicitly represented and within profile;
blind retry:
0

ledger:
conserved

provider secret:
worker-only
```

Do not infer success from frontend response alone.

If PASS:
- keep `public_control.enabled=true`;
- keep frontend Live enabled;
- keep ingress release topology;
- do NOT rollback;
- export evidence;
- stop for Browser review.

Success target:

```text
PUBLIC_LIVE_RELEASED
/
FOURTH_SINGLE_PUBLIC_SMOKE_PASS
/
BROWSER_REVIEW_REQUIRED
/
HUMAN_PUBLIC_SITE_SMOKE_PENDING
```

Executor cannot declare L8 closed.

## Phase F — mandatory failure handling

For ANY material failure after control enable:

### first action
Set:

`public_control.enabled=false`

FIRST.

Prove:
- second admission impossible;
- new public run count remains exactly 1.

Then restore frontend Replay-only:
- `enabled=false`;
- `api_origin=null`;
- CSP `connect-src 'self'`;
- deterministic manifest/test expectations;
- deploy Cloudflare rollback.

KEEP backend PARKED:
- ingress domain KEEP;
- exact origin KEEP;
- edge trust KEEP;
- ingress healthy KEEP;
- worker KEEP;
- provider secret topology KEEP.

No full teardown for ordinary execution/provider/tool failure.

## Phase G — exact automatic reconciliation if failure leaves retained liability

After control=false and frontend rollback, classify the exact new run.

### G1 provider UNKNOWN

If and only if the exact new run satisfies accepted migration 0025 predicate:

Invoke:

`public_live_api.reconcile_unknown_provider_run(bytea)`

for that run only.

Requirements:
- no resend;
- provider physical truth remains UNKNOWN;
- conservative liability only;
- SETTLE exactly once;
- held 0;
- slot free;
- outbox closed;
- claim/pin 0;
- work nonclaimable/closed;
- idempotent second proof.

### G2 known-outcome failed execution

If and only if the exact new run satisfies accepted migration 0026 predicate:

Invoke:

`public_live_api.reconcile_known_failed_execution_run(bytea)`

for that run only.

Requirements:
- physical provider/tool truths unchanged;
- cancelled-before-dispatch provider contributes zero;
- conservative liability derived canonically for dispatched provider send;
- SETTLE exactly once;
- held 0;
- slot free;
- outbox closed;
- claim/pin 0;
- idempotent replay.

### G3 neither predicate matches

Do not force either reconciler.

Preserve state and stop with exact blocker:

`FOURTH_SMOKE_RETENTION_PATTERN_UNCOVERED`

No raw-table repair.

## Phase H — full teardown only for security-boundary failure

Trigger full teardown only if fresh evidence shows any of:

- run admission while control=false;
- invalid Origin/edge identity accepted;
- provider secret authority outside worker;
- owner/admin route public exposure;
- public DB exposure;
- backend continues dispatching new provider work after control disable;
- accepted PARKED boundary cannot be restored.

Then:
1. control false first;
2. frontend Replay-only;
3. remove public ingress domain;
4. remove release origin;
5. remove edge trust;
6. preserve evidence;
7. STOP.

Do not use full teardown merely because provider/tool/execution failed.

## Phase I — final failure proof

For ordinary failed release require:

```text
Public control:
FALSE

frontend:
Replay-only

PARKED ingress:
domain/origin/edge trust PRESENT
healthy

new public run count:
1

second run:
0

provider blind resend:
0

held:
0 if accepted reconciler applied;
otherwise explicitly retained with blocker

open claim/pin:
0 if covered cleanup path applies

provider secret:
worker-only
```

Failure target:

```text
RELEASE_ROLLED_BACK_TO_PARKED_FAIL_CLOSED
/
<EXACT_FAILURE_CLASS>
/
BROWSER_REVIEW_REQUIRED
```

No fifth release authority.

## Phase J — canonical Git/export

Fast-forward only.

No amend/rebase/force.

Be careful with repository-connected passive deployments.

After successful smoke, do not push a rollback/governance commit that changes release frontend bytes.

After failed smoke, rollback frontend commit may be pushed only after control=false.

Persist supplied Cycle/Judgment/Handoff and move this Task active→done.

### export byte rule

Previous result had one CRLF-vs-LF changed-copy mismatch.

For this result:
- changed source/test/migration/release copies in export must use the exact canonical Git blob bytes;
- verify byte SHA against Git blob, not only LF-normalized content;
- report any mismatch rather than claiming N/N PASS.

## temporary operator access

At most one ephemeral Railway SSH key if required.

- no public DB endpoint;
- no key bytes exported;
- no DB credentials exported;
- no provider secret read;
- cleanup mandatory.

## forbidden

- private provider canary;
- second public smoke;
- fifth release attempt;
- manual provider send;
- blind provider resend;
- alternate provider/model;
- unbounded/free-form user tool input;
- new migration;
- new DB role/login/grant;
- public DB;
- worker public domain;
- provider secret movement/rotation;
- raw-table reconciliation;
- ordinary-failure full teardown;
- unrelated product work;
- unrelated historical test repair.

## required export

Create:

`.aiassistant/reports/target/20260919_1806_aiscc-p3-3-l8-fourth-public-live-release-and-single-smoke-1/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `RELEASE_PREFLIGHT.md`
- `PARKED_REPROOF.md`
- `FRONTEND_RELEASE_PROOF.md`
- `CONTROL_ENABLEMENT.md`
- `FOURTH_PUBLIC_SMOKE.md`
- `PROVIDER_OPERATION_PROOF.md`
- `TOOL_OPERATION_PROOF.md`
- `WORKER_CLAIM_PIN_PROOF.md`
- `ACCOUNTING_SETTLEMENT_PROOF.md`
- `RECONCILIATION_0025_PROOF.md` if used, otherwise `RECONCILIATION_0025_NOT_USED.md`
- `RECONCILIATION_0026_PROOF.md` if used, otherwise `RECONCILIATION_0026_NOT_USED.md`
- `FINAL_PUBLIC_STATE.md`
- `PARKED_ROLLBACK_PROOF.md` if failed, otherwise `PARKED_ROLLBACK_NOT_USED.md`
- `PROVIDER_SECRET_APPLICABILITY.md`
- `TEMP_OPERATOR_ACCESS_PROOF.md`
- `WORKSPACE_STATE.md`
- changed release/governance files using exact Git blob bytes

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
3. preflight
4. PARKED reproof
5. frontend release commit/deployment
6. control enablement
7. exactly-one smoke identity
8. polling Origin proof
9. provider operations
10. tool operations
11. worker claim/pin
12. accounting/slot/outbox
13. reconciliation 0025/0026 if any
14. final released or PARKED state
15. provider-secret/security state
16. temporary access cleanup
17. Git/export byte identity
18. Browser review state
19. Human public-site smoke state
20. blockers/unverified
