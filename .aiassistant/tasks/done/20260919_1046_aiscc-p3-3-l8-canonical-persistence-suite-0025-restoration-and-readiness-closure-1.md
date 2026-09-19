# 작업지시서: P3-3 L8 Canonical Persistence Suite 0025 Restoration + Readiness Closure

## meta

- task_id: `20260919_1046_aiscc-p3-3-l8-canonical-persistence-suite-0025-restoration-and-readiness-closure-1`
- created_at: `2026-09-19T10:46:00+09:00`
- work_type: `TEST_AUTHORITY_RESTORATION_AND_READINESS_REPROOF`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- exact_baseline: `f3f36a1ebeed86ec18bcc0a0e60fdcd3aacc9ca1`
- fresh_ide_chat_required: `No`
- public_release_authority: `NONE`
- public_run_authority: `NONE`
- provider_call_authority: `NONE`
- production_source_change_authority: `NONE_UNLESS_REAL_DEFECT_PROVEN_THEN_STOP`
- DB_migration_authority: `NONE`
- DB_role_grant_authority: `NONE`
- Railway_worker_deploy_authority: `NONE`
- Railway_other_runtime_mutation_authority: `NONE`
- Cloudflare_mutation_authority: `NONE`
- public_domain_authority: `NONE`
- edge_trust_authority: `NONE`
- temporary_Railway_SSH_key_authority: `ONE_EPHEMERAL_KEY_IF_REQUIRED_FOR_FINAL_READONLY_PROOF`

## Goal

Close:

`CANONICAL_PERSISTENCE_SUITE_STALE_AFTER_0025`

and only then complete fresh re-release readiness proof.

The worker claim-sequence source repair is already accepted.

Do not redesign or alter that worker fix.

Do NOT release Public Live.

## accepted entry state

```text
repository baseline:
f3f36a1ebeed86ec18bcc0a0e60fdcd3aacc9ca1

worker source repair:
2e0e67e5f80c31de29b004944b858b33bc1cc27e

worker claim-sequence blocker:
CLOSED

hosted worker:
corrected deployment / healthy idle-loop candidate

migration head:
20260919_0025

0125 UNKNOWN:
reconciled / CLOSED

1919:
settled / CLOSED

Public control:
DISABLED

Public Live:
NOT_RELEASED

previous Human RELEASE_PUBLIC_LIVE:
CONSUMED
```

## exact test blocker

Current file:

`tests/integration/public_live/test_persistence.py`

was explicitly executed and yielded:

```text
25 PASS
23 FAIL
```

Browser independently confirmed current repository test configuration includes all `tests/` by default and does not exclude this file.

Browser also independently confirmed the file still contains migration-path logic that expects:

`20260919_0024`

while current accepted head is:

`20260919_0025`.

Treat the Executor's claim that all 23 failures are merely stale tests as a hypothesis to prove, not as accepted fact.

## Phase A — exact failure classification

Using a disposable local PostgreSQL instance only:

1. start from exact baseline;
2. run the whole `tests/integration/public_live/test_persistence.py`;
3. capture a concise failure taxonomy without exporting DB credentials;
4. classify every failing test into one of:
   - stale expected migration head;
   - stale test DB initialization/fixture contract;
   - stale table/count/ACL expectation caused by accepted 0025;
   - real production behavior regression;
   - unrelated pre-existing failure.

Produce a table/count proving all 23 failures are accounted for.

If any failure demonstrates a real production defect:

`PERSISTENCE_SUITE_REAL_PRODUCT_REGRESSION`

and STOP before changing production code.

If failures cannot be completely classified:

`PERSISTENCE_SUITE_FAILURE_CLASSIFICATION_INCOMPLETE`

and STOP.

## Phase B — restoration rules

Expected allowed changes:

- `tests/integration/public_live/test_persistence.py`;
- directly shared test-only fixture/helper files only if mechanically required.

Production `src/`, migrations, runtime config, deployment config are NOT authorized.

Required principles:

- canonical expected head becomes `20260919_0025`;
- tests requiring a canonical migrated DB must prepare/upgrade their isolated DB to current head;
- preserve historical migration-path coverage from 0012/earlier accepted predecessor where intended;
- preserve owner-history preservation assertions;
- preserve accounting, append-only, slot, identity, clock, runtime-permission, serialization, reconciliation and safety assertions;
- preserve 0024 ACL compatibility and add/retain 0025 UNKNOWN reconciliation expectations where the persistence suite owns that contract.

Do not:
- exclude the file in pytest config;
- add global ignore;
- skip/xfail failures;
- loosen assertions merely to pass;
- hard-code hosted production data;
- remove migration-path verification;
- modify historical migration bytes.

If a test can only pass by changing production behavior:

`PERSISTENCE_SUITE_REQUIRES_PRODUCT_CHANGE`

and STOP for Browser review.

## Phase C — canonical migration test expectations

The restored migration-path test must prove at minimum:

### empty -> head

```text
alembic head:
20260919_0025

public_control:
disabled

slots:
1/2 FREE

campaign rows:
0

owner historical rows:
unchanged
```

### predecessor lineage -> head

Where the existing test uses an earlier predecessor such as `20260914_0012`:
- migrate predecessor;
- seed owner history as before;
- migrate to head;
- prove owner rows preserved;
- prove final head 0025;
- prove post-head safe defaults.

### 0024 -> 0025 compatibility

Add or retain a focused path proving:
- DB at 0024 can migrate to 0025;
- owner/Public Live pre-existing rows remain preserved;
- new UNKNOWN reconciliation functions exist;
- PUBLIC EXECUTE revoked;
- intended reconciler EXECUTE exists;
- no new login/role/table DML grant is introduced.

Do not duplicate the entire dedicated 0025 integration suite if existing tests already prove a dimension; reference/run those tests instead where appropriate.

## Phase D — required test gates

After restoration:

1. `tests/integration/public_live/test_persistence.py`:
   - **all collected tests PASS**
   - zero FAIL
   - zero xfail/skip introduced for this repair.

2. `tests/integration/public_live/test_worker_claim_sequence.py`:
   - all PASS.

3. directly affected 0025 UNKNOWN reconciliation tests:
   - all PASS.

4. migration empty -> head and predecessor -> head tests:
   - PASS.

5. Ruff:
   - PASS.

6. format:
   - PASS.

7. `git diff --check`:
   - PASS.

8. if only tests changed, mypy production rerun is not required.

Also run a repository-level Public Live integration selection broad enough to ensure the restored fixture did not hide failures.

Do not run a real provider call.

## Phase E — commit/push

Expected source impact:

```text
production source:
0 files

migration:
0 files

test-only:
narrow persistence fixture/assertion restoration
```

Commit/push by fast-forward only.

No amend/rebase/force push.

Before push verify:
- Public control disabled;
- public domains 0;
- edge trust absent;
- no active public run;
- no open claim/pin;
- held liability 0.

Known passive Git deployment coupling may rebuild ingress/API; no runtime config mutation is authorized.

## Phase F — final fresh read-only readiness proof

After test restoration/push, perform fresh read-only checks.

If hosted DB evidence requires access and no existing path exists, at most one ephemeral Railway SSH key is authorized solely for read-only proof.

Cleanup is mandatory.

### worker
- existing corrected worker deployment remains the accepted source commit `2e0e67e5f80c31de29b004944b858b33bc1cc27e` or an equivalent later commit containing byte-identical worker source;
- worker service SUCCESS;
- public domain 0;
- no worker failure/sequence denial recurrence in a bounded recent window;
- durable worker acquisition remains progressing/EMPTY where idle;
- claimable work 0.

### 0125
- FAILED_TIMEOUT;
- SETTLED conservative 4400;
- one SETTLE;
- slot free;
- outbox closed;
- open claims/pins 0;
- provider op exactly 1 UNKNOWN;
- provider resend 0.

### 1919
- FAILED_NOT_DISPATCHED;
- settled 0;
- no duplicate settlement.

### ledger
- held 0;
- campaign/day conservation exact.

### migration/ACL
- hosted head 0025;
- 0025 reconciliation ACL exact;
- candidate set empty.

### fail-closed
- control disabled;
- active future-deadline public runs 0;
- no public ingress/worker domain;
- edge trust absent;
- no Live frontend binding.

### provider/secret
- OpenAI / gpt-5.6-luna / public-live-luna-v1 exact;
- worker-only sealed provider binding;
- standard `OPENAI_API_KEY` absent;
- no provider authority on ingress/initializer/API;
- provider calls during this Task 0.

### fixed tool
- accepted fixed in-process Stockroom contract unchanged.

### Replay
- public/release-disabled;
- all four scenarios unchanged;
- live-config false/null;
- CSP self-only.

## temporary access cleanup

If an ephemeral Railway SSH key is used:
- exactly one maximum;
- no key bytes/fingerprint export;
- read-only DB sessions;
- no public DB exposure;
- remove Railway key;
- remove local key files;
- remove helper material;
- prove absence/count only.

Failure:

`TEMP_OPERATOR_ACCESS_CLEANUP_FAILED`

and STOP.

## success target

Only if:
- all persistence-suite tests are green;
- no assertion weakening/skips;
- no production defect discovered;
- worker remains healthy;
- all fresh hosted readiness dimensions pass;
- temporary access cleanup passes;

return:

```text
CANONICAL_PERSISTENCE_SUITE_RESTORED
/
RERELEASE_READY_CANDIDATE
/
NEW_HUMAN_RELEASE_DECISION_REQUIRED
/
BROWSER_REVIEW_REQUIRED
```

Executor does not grant release authority.

## blocked outcomes

Use exact blocker:

```text
PERSISTENCE_SUITE_FAILURE_CLASSIFICATION_INCOMPLETE
PERSISTENCE_SUITE_REAL_PRODUCT_REGRESSION
PERSISTENCE_SUITE_REQUIRES_PRODUCT_CHANGE
PERSISTENCE_SUITE_STILL_RED
WORKER_IDLE_ACQUISITION_REGRESSION
UNKNOWN_RECONCILIATION_DURABILITY_REGRESSION
LEDGER_CONSERVATION_REGRESSION
MIGRATION_AUTHORITY_REGRESSION
PUBLIC_FAIL_CLOSED_STATE_REGRESSION
PROVIDER_APPLICABILITY_NOT_PROVABLE
REPLAY_READINESS_REGRESSION
TEMP_OPERATOR_ACCESS_CLEANUP_FAILED
```

## forbidden

- production source mutation;
- migration creation/change;
- worker redeploy/restart;
- Public Live release;
- control enable;
- public run;
- provider call/canary;
- retry/resend;
- reconciliation invocation;
- DB DDL/DML on hosted production;
- DB role/login/grant mutation;
- public PostgreSQL exposure;
- Railway config mutation except one ephemeral SSH key lifecycle;
- public domain/edge trust;
- frontend Live enable;
- Cloudflare mutation;
- provider secret read/copy/rotation;
- skipping/xfailing/excluding failing canonical tests;
- unrelated product work;
- amend/rebase/force push.

## canonical persistence

Persist supplied Cycle/Judgment/Handoff.

Move this Task active -> done.

Test-only commit and governance commit may be separate ordinary commits.

## required export

Create:

`.aiassistant/reports/target/20260919_1046_aiscc-p3-3-l8-canonical-persistence-suite-0025-restoration-and-readiness-closure-1/`

Required root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `PERSISTENCE_FAILURE_TAXONOMY.md`
- `PERSISTENCE_SUITE_RESTORATION.md`
- `PERSISTENCE_MIGRATION_PATH_PROOF.md`
- `PERSISTENCE_TEST_RESULTS.md`
- `SOURCE_CHANGE_AUDIT.md`
- `WORKER_HEALTH_REPROOF.md`
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
- changed test/governance files preserving repository-relative paths

Also create adjacent result ZIP and report SHA-256.

Never export:
- provider key or masked identifier;
- DB DSN/password;
- SSH key material;
- HMAC key;
- read capability;
- raw provider output;
- raw prompts/private protocol;
- private reasoning.

## final response format

1. result
2. target ZIP SHA-256
3. failure taxonomy
4. test-only restoration
5. persistence suite result
6. migration-path result
7. worker health reproof
8. temporary access cleanup
9. 0125 durability
10. 1919 durability
11. ledger/campaign
12. migration/ACL
13. fail-closed hosted state
14. provider/secret applicability
15. fixed-tool applicability
16. Replay/frontend
17. readiness result
18. Human decision state
19. blockers/unverified
