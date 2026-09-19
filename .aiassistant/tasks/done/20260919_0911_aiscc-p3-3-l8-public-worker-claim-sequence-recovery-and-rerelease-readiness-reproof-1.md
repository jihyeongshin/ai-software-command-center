# 작업지시서: P3-3 L8 Public Worker Claim Sequence Recovery + Re-release Readiness Reproof

## meta

- task_id: `20260919_0911_aiscc-p3-3-l8-public-worker-claim-sequence-recovery-and-rerelease-readiness-reproof-1`
- created_at: `2026-09-19T09:11:00+09:00`
- work_type: `SECURITY_RUNTIME_REWORK_AND_READINESS_REPROOF`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- exact_baseline: `cf3abc77a4b69335e5fa429049971858c1aa9146`
- fresh_ide_chat_required: `No`
- public_release_authority: `NONE`
- public_run_authority: `NONE`
- provider_call_authority: `NONE`
- DB_migration_authority: `NONE`
- new_DB_login_role_grant_authority: `NONE`
- source_rework_authority: `EXACT_WORKER_CLAIM_SEQUENCE_RECOVERY_ONLY`
- Railway_worker_deploy_authority: `EXISTING_WORKER_EXACT_SOURCE_DEPLOY_ONLY`
- Railway_other_service_config_mutation_authority: `NONE`
- Cloudflare_mutation_authority: `NONE`
- public_domain_authority: `NONE`
- edge_trust_authority: `NONE`
- temporary_Railway_SSH_key_authority: `ONE_EPHEMERAL_KEY_IF_REQUIRED`

## Goal

Close:

`PUBLIC_WORKER_CLAIM_SEQUENCE_RECOVERY_REGRESSION`

without changing the accepted worker/claim authority model.

Then deploy the corrected source to the existing Public Live worker only and perform a fresh release-readiness reproof.

Do NOT release Public Live.

## accepted entry state

```text
repository baseline:
cf3abc77a4b69335e5fa429049971858c1aa9146

migration head:
20260919_0025

0125 UNKNOWN:
reconciled / CLOSED

1919:
settled / CLOSED

campaign held:
0

Public control:
DISABLED

Public Live:
NOT_RELEASED

public ingress domains:
0

worker public domains:
0

edge trust:
ABSENT

provider secret:
worker-only / sealed

previous Human RELEASE_PUBLIC_LIVE:
CONSUMED
```

## blocker evidence

0415 fresh hosted proof observed:
- 200 consecutive worker `CLAIM_EXECUTION / PUBLIC_WORKER_FAILURE_UNCLASSIFIED` events over roughly 33 minutes;
- continued failures afterward;
- zero claimable work;
- zero unreleased claim;
- zero open dispatch pin;
- no new provider operation.

Fresh DB evidence showed the affected worker instance retained:

```text
last_acquire_seq = 3083
last_result_kind = CLAIM
```

Current source advances `DurableWorkerAuthority.sequence` before the DB acquisition result is known.

Current DB `worker_claim_next` accepts:
- same sequence as durable last -> idempotent replay;
- durable last + 1 -> next acquisition;
- otherwise -> sequence denial.

The production exception text was not exported, so first prove the root cause deterministically rather than treating the inference as an unquestionable fact.

## authority invariants — do not redesign

Preserve:
- one worker instance identity + process generation;
- one active claim per work/run;
- one active claim per worker as currently designed;
- monotonic durable acquisition sequence;
- same-sequence idempotent replay;
- fence monotonicity;
- 15s lease / 5s renew;
- mediated worker functions only;
- P1-5 physical provider lifecycle ownership;
- UNKNOWN -> quarantine/reconciliation -> no blind resend;
- no provider send during polling/claim;
- no secret resolution during polling/claim;
- Public fixed tool contract;
- exact four ExecutionStatus values;
- existing WorkflowState values.

If closing the bug requires changing DB schema, migration, authority model, or accepted sequence semantics:

`WORKER_CLAIM_SEQUENCE_BASELINE_SUPERSESSION_REQUIRED`

and STOP.

## Phase A — exact source/runtime diagnosis

Read exact current:
- `src/aiscc/public_live/worker_authority.py`;
- `src/aiscc/public_live/worker.py`;
- migration `20260917_0019_public_live_worker_claims.py`;
- migration `20260919_0025_public_live_unknown_reconciliation.py`;
- directly related worker tests;
- 0415 evidence.

Construct a deterministic PostgreSQL reproduction of this sequence:

```text
durable last_acquire_seq = N
worker memory sequence = N

next candidate = N+1
↓
DB rejects before advancing last_acquire_seq because existing open claim prevents acquisition
↓
client call raises
↓
external canonical reconciliation/release closes that claim
↓
same process attempts again
```

Prove current implementation can submit a sequence greater than `N+1` and remain denied despite the durable blocker being gone.

If this exact mechanism cannot be reproduced:

`CLAIM_SEQUENCE_ROOT_CAUSE_NOT_REPRODUCED`

and STOP before changing source.

## Phase B — required repair property

Implement the narrowest source-only fix.

Required semantic property:

```text
candidate sequence
= committed in-memory sequence + 1

DB call fails before a successful/idempotent response
→ committed in-memory sequence MUST NOT advance

DB call succeeds or same-sequence idempotent replay succeeds
→ committed in-memory sequence may advance to candidate
```

The expected narrow implementation shape is to advance local sequence only after `repository.claim(...)` returns successfully.

Equivalent implementation is allowed if it proves the same semantics.

Important post-commit ambiguity property:

If DB accepted sequence `N+1` but the client lost the response:
- local committed sequence may still be N;
- retrying the SAME `N+1` must use the DB's existing same-sequence idempotency branch;
- no duplicate claim;
- no fence duplication;
- no new run/provider action.

Do not add raw table sequence reads or direct DB resynchronization if the existing idempotent protocol already suffices.

Do not weaken `CLAIM_SEQUENCE_DENIED`.

## Phase C — deterministic tests

Required PostgreSQL tests:

1. normal EMPTY acquisition advances sequence exactly once;
2. normal CLAIM acquisition advances sequence exactly once;
3. existing open claim rejects candidate without advancing local committed sequence;
4. after canonical external release/closure, same process retries the same candidate and recovers;
5. sequence does not skip after repeated rejected attempts;
6. simulated response-loss after DB commit retries the same sequence and obtains the exact idempotent prior result;
7. no duplicate claim row/fence/event on same-sequence replay;
8. fresh process/new worker identity starts its own sequence correctly;
9. UNKNOWN/quarantined work remains nonclaimable;
10. terminal/closed worker work remains nonclaimable;
11. existing 15s lease / 5s renewal behavior unchanged;
12. no provider call/secret resolution occurs in claim tests.

Also run directly affected:
- worker authority unit/integration tests;
- Public Live persistence/worker tests;
- UNKNOWN reconciliation regression tests;
- Ruff;
- formatter check;
- narrow mypy for changed production owner;
- `git diff --check`.

No real provider call.

## migration rule

Expected migration impact:

`NONE`

Do not alter `20260917_0019` historical migration bytes.

Do not create `0026`.

If a DB contract change is truly necessary:

`WORKER_CLAIM_SEQUENCE_MIGRATION_REQUIRED`

and STOP for Browser review.

## source scope

Expected production source change:

`src/aiscc/public_live/worker_authority.py`

Tests may change in directly related worker/Public Live test files.

A narrow secret-safe diagnostic classification may be added only if needed and must:
- use allowlisted stable codes;
- not log raw exception, SQL, DSN, key, capability or provider data;
- not broaden work scope.

Do not touch unrelated product surfaces.

## Phase D — commit / push

Commit the exact source/test repair.

No amend/rebase/force push.

Before push freshly verify:
- control disabled;
- public domains 0;
- edge trust absent;
- claimable work 0;
- open claims/pins 0;
- unsettled reservations 0;
- no provider action pending.

Known repository coupling:
- main push may passively rebuild ingress/API.

After push verify those services remain fail-closed and no public domain appears.

## Phase E — existing worker deploy

The worker is separately managed and must be updated explicitly.

Authorized:
- deploy/restart the EXISTING `aiscc-public-live-worker` only;
- exact accepted source commit;
- same Railway service;
- same region/plan/replica count;
- same start command;
- same DB binding;
- same worker-only provider secret binding;
- no env/config/secret/scale changes.

Forbidden:
- new service;
- worker public domain;
- ingress domain;
- control enable;
- provider call;
- public run;
- secret rotation/copy.

A restart of old code alone is not closure.

## Phase F — hosted healthy idle-loop proof

After corrected worker deployment, prove fresh runtime behavior.

Required:
- worker runtime identity valid;
- no claimable work;
- no open claims/pins;
- no unsettled reservations;
- no new public run/provider operation;
- provider secret still worker-only;
- worker public domains 0.

Then prove the new worker instance can complete normal EMPTY acquisition cycles.

Preferred evidence:
- fresh worker instance exists;
- its durable `last_acquire_seq` advances monotonically through at least 5 successful EMPTY acquisitions;
- each advance is exactly +1;
- `last_result_kind=EMPTY`;
- no `CLAIM_SEQUENCE_DENIED`/claim-loop failure observation;
- no `PUBLIC_WORKER_FAILURE_UNCLASSIFIED` recurrence during the bounded proof window;
- no provider/tool operation is created.

Normal mediated worker registration and EMPTY-acquire bookkeeping are authorized runtime effects.

Manual DB DML is not authorized.

Do not create synthetic public work in hosted production solely to test acquisition.

## temporary read-only operator access

If hosted DB proof requires it, at most one ephemeral Railway SSH key is authorized.

Rules:
- read-only operator queries;
- no public PostgreSQL exposure;
- no DB DDL/DML;
- no provider secret value read;
- remove Railway key before completion;
- delete local private/public key files;
- delete helper material;
- prove cleanup by count/presence metadata only.

Cleanup failure:

`TEMP_OPERATOR_ACCESS_CLEANUP_FAILED`

and STOP.

## Phase G — fresh readiness reproof

After worker fix/deployment passes, freshly recheck:

### repository/deploy
- `HEAD == origin/main`;
- source repair commit in ancestry;
- migration head remains 0025;
- no unreviewed product mutation.

### 0125 durability
- FAILED_TIMEOUT;
- SETTLED 4400 conservative liability;
- one SETTLE;
- slot free;
- outbox closed;
- open claims/pins 0;
- provider operation exactly 1 UNKNOWN;
- retry/resend 0.

### 1919 durability
- FAILED_NOT_DISPATCHED;
- settled cost 0;
- no duplicate settlement.

### campaign/day
- held 0;
- conservation exact;
- no stale reservation.

### ACL
- 0025 exact function authority unchanged;
- candidate set empty.

### fail-closed release state
- control disabled;
- active future public runs 0;
- public domains 0;
- edge trust absent;
- no release frontend binding.

### provider/secret
- exact Luna profile;
- worker-only sealed provider binding;
- no standard `OPENAI_API_KEY`;
- no provider binding on ingress/initializer/API;
- no provider call made by this Task.

### Public fixed tool
- fixed in-process Stockroom contract remains applicable.

### Replay
- public/release-disabled;
- four scenarios unchanged;
- live-config false/null;
- CSP self-only.

## readiness success target

Only if source repair, hosted idle worker proof, temporary-access cleanup, and all fresh readiness dimensions pass:

```text
PUBLIC_WORKER_CLAIM_SEQUENCE_RECOVERY_ACCEPTED
/
RERELEASE_READY_CANDIDATE
/
NEW_HUMAN_RELEASE_DECISION_REQUIRED
/
BROWSER_REVIEW_REQUIRED
```

Executor cannot grant release authority.

## blocked outcomes

Use the narrowest blocker:

```text
CLAIM_SEQUENCE_ROOT_CAUSE_NOT_REPRODUCED
WORKER_CLAIM_SEQUENCE_BASELINE_SUPERSESSION_REQUIRED
WORKER_CLAIM_SEQUENCE_MIGRATION_REQUIRED
CLAIM_SEQUENCE_RECOVERY_TEST_FAILED
WORKER_DEPLOYMENT_IDENTITY_MISMATCH
WORKER_IDLE_ACQUISITION_REGRESSION
TEMP_OPERATOR_ACCESS_CLEANUP_FAILED
UNKNOWN_RECONCILIATION_DURABILITY_REGRESSION
LEDGER_CONSERVATION_REGRESSION
PUBLIC_FAIL_CLOSED_STATE_REGRESSION
PROVIDER_APPLICABILITY_NOT_PROVABLE
REPLAY_READINESS_REGRESSION
```

## forbidden

- Public Live release
- control enable
- public ingress/domain
- edge trust
- frontend Live enable
- Cloudflare mutation
- new public run
- provider call/canary
- provider retry/resend
- reconciliation invocation
- new migration
- DB schema/role/login/grant mutation
- public PostgreSQL exposure
- provider secret read/copy/rotation
- worker env/secret/scale changes
- unrelated product changes
- amend/rebase/force push

## canonical persistence

Persist supplied Cycle/Judgment/Handoff.

Move this Task active -> done.

Source/test fix commit and governance commit may be separate ordinary commits.

Push by fast-forward only.

## required export

Create:

`.aiassistant/reports/target/20260919_0911_aiscc-p3-3-l8-public-worker-claim-sequence-recovery-and-rerelease-readiness-reproof-1/`

Required root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `CLAIM_SEQUENCE_ROOT_CAUSE.md`
- `CLAIM_SEQUENCE_PROTOCOL_PROOF.md`
- `CLAIM_SEQUENCE_TESTS.md`
- `SOURCE_CHANGE_AUDIT.md`
- `WORKER_DEPLOYMENT_PROOF.md`
- `WORKER_IDLE_LOOP_PROOF.md`
- `UNKNOWN_RECONCILIATION_DURABILITY.md`
- `HISTORICAL_SETTLEMENT_DURABILITY.md`
- `LEDGER_CAMPAIGN_READINESS.md`
- `HOSTED_MIGRATION_ACL.md`
- `HOSTED_SAFE_STATE.md`
- `PROVIDER_READINESS_APPLICABILITY.md`
- `FIXED_TOOL_RUNTIME_APPLICABILITY.md`
- `REPLAY_FRONTEND_READINESS.md`
- `TEMP_OPERATOR_ACCESS_PROOF.md`
- `RERELEASE_DELTA_PLAN.md`
- `WORKSPACE_STATE.md`
- changed source/test/governance files preserving repository-relative paths

Also create adjacent result ZIP and report SHA-256.

Never export:
- provider key or masked key identifier;
- DB DSN/password;
- SSH key material;
- HMAC key;
- read capability;
- raw provider output;
- raw prompt/private protocol;
- private reasoning.

## final response format

1. result
2. target ZIP SHA-256
3. root-cause reproduction
4. source fix
5. tests/static checks
6. source commit/push
7. worker deployment identity
8. healthy idle-loop proof
9. temporary access cleanup
10. 0125 durability
11. 1919 durability
12. ledger/campaign
13. ACL/migration
14. fail-closed hosted state
15. provider/secret applicability
16. fixed-tool applicability
17. Replay/frontend
18. readiness result
19. Human decision state
20. blockers/unverified
