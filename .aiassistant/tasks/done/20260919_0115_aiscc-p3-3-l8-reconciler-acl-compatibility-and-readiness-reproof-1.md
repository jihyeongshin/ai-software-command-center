# 작업지시서: P3-3 L8 reconciler ACL compatibility and readiness reproof

## meta

- task_id: `20260919_0115_aiscc-p3-3-l8-reconciler-acl-compatibility-and-readiness-reproof-1`
- created_at: `2026-09-19T01:15:00+09:00`
- work_type: `SECURITY_DB_COMPATIBILITY_REWORK_AND_RERELEASE_READINESS_REPROOF`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- exact_baseline: `6e6c2198a2034664ee8ff9d85d9e78a52fa403c9`
- fresh_ide_chat_required: `No`
- public_release_authority: `NONE`
- public_run_authority: `NONE`
- provider_call_authority: `NONE`
- Cloudflare_mutation_authority: `NONE`
- new_DB_login_role_authority: `NONE`
- broad_DB_grant_authority: `NONE`
- exact_DB_compatibility_fix_authority: `YES`
- temporary_Railway_SSH_key_authority: `ONE_EPHEMERAL_KEY_IF_REQUIRED`

## Goal

Resolve the exact canonical mismatch that prevents the normal hosted `ReconciliationService` contract from operating under the existing `aiscc_public_live_reconciler` authority.

Then obtain fresh hosted evidence and retry the re-release readiness preflight.

Do not release Public Live.

## Current accepted state

```text
entry baseline:
6e6c2198a2034664ee8ff9d85d9e78a52fa403c9

2344 settlement:
ACCEPTED / CLOSED

retained 1919 run:
FAILED_NOT_DISPATCHED

Public admission:
DISABLED

Public Live:
NOT_RELEASED

ingress / worker public domains:
0 / 0

Replay:
PUBLIC / UNCHANGED

fixed-tool Public Live amendment:
ACCEPTED

affected hosted L5:
ACCEPTED / CLOSED

affected L6:
ACCEPTED

L7:
ACCEPTED / CLOSED
```

0102 correct-stop blocker:

```text
RECONCILER_RUNTIME_ACL_ASYMMETRY_UNRESOLVED
```

Secondary evidence blocker:

```text
HOSTED_READ_ONLY_DB_ACCESS_PATH_UNAVAILABLE
```

## Exact defect boundary

Canonical source currently has a general `ReconciliationService` contract that uses:

```text
runtime repository
+
reconciler repository
```

For the terminal reconciliation transaction, the reconciler repository requires at least:

```text
public_live_api.run_context(bytea)
public_live_api.project_run(bytea,bigint,text,bytea)
```

Current canonical migration lineage grants these compatibility functions to:

```text
aiscc_public_live_runtime
```

but not to:

```text
aiscc_public_live_reconciler
```

The 2344 task-owned role-switching adapter was authorized only for one exact historical run. It is not the permanent runtime solution.

## Required security semantics

The finished canonical contract must allow the existing reconciler repository to execute the exact functions required by `ReconciliationService` while preserving least privilege.

The intended authority boundary is:

- `PUBLIC`: no execute authority on the protected functions;
- `aiscc_public_live_runtime`: existing required authority preserved;
- `aiscc_public_live_reconciler`: only the exact additional function authority required by the canonical reconciliation service;
- no direct table DML privilege added;
- no new role;
- no new login;
- no role-membership broadening;
- no `GRANT ALL`;
- ingress/API/worker login privileges are not broadened;
- DB-enforced `project_run` state predicates remain intact;
- no raw-table settlement/projection bypass.

The Executor owns the implementation mechanics.

A narrow compatibility migration granting the exact required functions is an allowed solution class.

A code-side repository split is also allowed only if it preserves transaction/settlement/projection semantics and is demonstrably narrower or equally safe.

If the fix requires any broader persistent privilege than the exact proven compatibility need:

`RECONCILER_ACL_FIX_NEEDS_HUMAN_SECURITY_DECISION`

and STOP before applying it.

## Source and test requirements before hosted mutation

Before hosted application:

1. re-confirm the exact current mismatch from source/migration authority;
2. implement the narrow correction;
3. add focused regression proving distinct runtime/reconciler authority works as intended;
4. prove `PUBLIC` stays revoked;
5. prove reconciler does not gain unrelated protected function/table authority;
6. prove `ReconciliationService.close()` can execute its normal context/closure/settlement/projection path using distinct role-scoped repositories in a controlled test;
7. prove already-settled identical close remains idempotent;
8. run focused Public Live reconciliation/integration regression;
9. Ruff/format/narrow mypy for changed Python if Python source changes;
10. `git diff --check`.

Do not broaden into a full L6 rerun unless an actual regression indicates it is necessary.

## Hosted migration authority

This Task authorizes applying only the exact accepted compatibility migration to the existing hosted Public Live PostgreSQL through the existing migration/operator mechanism.

Allowed:

- exact migration revision needed for this ACL compatibility;
- exact EXECUTE grant(s) to the existing `aiscc_public_live_reconciler` role when they are the narrow accepted fix;
- existing initializer/migration mechanism invocation or restart only as necessary to apply that revision;
- read-only privilege verification afterward.

Forbidden:

- new DB login;
- new DB role;
- role membership changes;
- table grants;
- public schema/table exposure;
- unrelated migration;
- destructive data change;
- campaign/control enablement;
- settlement retry.

If migration head or hosted schema provenance is ambiguous, STOP.

## temporary operator transport

Because 0102 found no registered Railway SSH key, this Task authorizes at most one fresh ephemeral SSH key **only if required** to reach the existing services for migration/proof.

Rules:

1. generate/use it only for this Task;
2. never commit key material;
3. never export private/public key content in evidence;
4. do not print/store DB DSN/password/provider secret;
5. use no public TCP database exposure;
6. remove the key from Railway before final submission;
7. remove all local key/askpass helper material;
8. prove cleanup by metadata/count only, not by exporting key values.

If the temporary key cannot be removed and verified:

`TEMP_OPERATOR_ACCESS_CLEANUP_FAILED`

and STOP with Public Live still disabled.

If an already-safe existing operator path is available, prefer it and do not create a key.

## known Git push deployment coupling

A GitHub `main` push may automatically rebuild the existing repository-connected ingress/API Railway services.

Treat that as known infrastructure coupling.

Before push:
- Public control disabled;
- ingress/worker public domains 0;
- no claimable/public work;
- provider requests 0.

After any automatic deployment:
- verify the same fail-closed invariants;
- do not add a public domain;
- do not enable edge trust;
- do not enable admission;
- do not invoke the provider.

An unexpected release/public exposure is a mandatory STOP.

## fresh hosted ACL proof

After the correction is applied, prove without exposing secrets:

- reconciler has EXECUTE on the exact required reconciliation compatibility functions;
- runtime retains required existing authority;
- PUBLIC remains revoked;
- no unrelated reconciler function/table authority was added;
- hosted migration head is the expected new head;
- no new DB role/login/membership was created.

Use privilege metadata and mediated function behavior. Do not export credentials.

## fresh readiness reproof

After ACL compatibility is accepted locally and applied hosted, freshly observe:

### settlement durability

- retained run remains `FAILED_NOT_DISPATCHED`;
- reservation `SETTLED / settled_cost=0`;
- slot free;
- outbox closed;
- exactly one closure observation;
- exactly one SETTLE event;
- 1919 hold remains fully released;
- historical worker-work remains non-claimable;
- no second settlement/refund.

Do not call `close()` again merely to prove this.

### fail-closed hosted state

- Public control disabled;
- Public Live not released;
- ingress public domains 0;
- worker public domains 0;
- edge trust absent;
- active future-deadline public runs 0;
- claimable work 0;
- unreleased claims 0;
- open pins 0;
- public dispatch rows 0;
- execution operations 0;
- no new provider request.

### provider applicability

Without reading secret values:
- no provider-secret scope/binding change is introduced by this Task;
- accepted worker deployment/provider adapter/model/profile applicability remains exact or is freshly re-established by value-free metadata;
- ingress/initializer/API must not gain provider authority;
- do not call OpenAI.

If exact applicability cannot be established without reading secret material or making a provider call, return a named blocker.

### fixed-tool applicability

- active worker remains compatible with the accepted deterministic in-process fixed Stockroom tool;
- no Public tool process/filesystem/tool-network/tool-secret authority is introduced;
- Owner/Self-Dogfood Docker path remains separate.

### Replay/frontend

Fresh public check:
- Replay reachable;
- four recorded scenarios unchanged;
- Live remains fail-closed while disabled;
- `enabled=false`;
- `api_origin=null`;
- no stale contradictory release label.

### budget/campaign

Fresh DB evidence:
- campaign `public-live-v1`;
- scenario/version exact;
- cutoff `2026-10-17T15:00:00Z` exclusive;
- per-run reservation 200000;
- daily budget 4000000;
- campaign budget 15000000;
- daily starts 20;
- concurrency 2;
- no retained 1919 held liability;
- current ledger/control state internally coherent.

Do not prepare/enable the campaign if that is a state mutation.

## release-delta plan

Refresh the exact current-state → future-release delta plan.

No step is executed.

The plan must retain:

```text
Human release authorization
→ fail-closed ingress exposure/binding as separately authorized
→ frontend exact API origin binding
→ fail-closed proof
→ control enable last
→ exactly one bounded public smoke
→ Browser review
→ Human public-site smoke
→ L8 close
```

and exact Replay-only rollback semantics.

## success result

Only if ACL compatibility and every fresh readiness dimension pass:

```text
RECONCILER_ACL_COMPATIBILITY_ACCEPTED
/
RERELEASE_READY_CANDIDATE
/
HUMAN_RELEASE_DECISION_REQUIRED
/
BROWSER_REVIEW_REQUIRED
```

This is still not release authorization.

## blocked results

Use the narrowest exact blocker, including as applicable:

```text
RECONCILER_ACL_FIX_NEEDS_HUMAN_SECURITY_DECISION
HOSTED_ACL_MIGRATION_MISMATCH
TEMP_OPERATOR_ACCESS_CLEANUP_FAILED
SETTLEMENT_DURABILITY_REGRESSION
PUBLIC_FAIL_CLOSED_STATE_REGRESSION
PROVIDER_APPLICABILITY_NOT_PROVABLE
REPLAY_READINESS_REGRESSION
BUDGET_CAMPAIGN_READINESS_BLOCKED
```

Preserve Public Live disabled.

## forbidden

- Public Live release
- admission enablement
- new public run
- real provider call
- Cloudflare mutation
- public ingress domain creation
- edge-trust enablement
- provider secret read/copy/rotation
- new DB login/role
- broad DB grant
- direct table mutation bypassing migration/service authority
- another settlement
- unrelated product work
- force push/rebase/amend

## canonical persistence / Git

Persist supplied Cycle/Judgment/Handoff and this Task.

Product/security fix commit and governance persistence commits are allowed when scoped exactly to this Task.

No unrelated cleanup.

Target export remains ignored/untracked.

## required export

Create:

`.aiassistant/reports/target/20260919_0115_aiscc-p3-3-l8-reconciler-acl-compatibility-and-readiness-reproof-1/`

Required root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `ACL_SOURCE_PROOF.md`
- `ACL_ROLE_MATRIX.md`
- `ACL_TEST_RESULT.md`
- `HOSTED_MIGRATION_PROOF.md`
- `TEMP_OPERATOR_ACCESS_PROOF.md`
- `SETTLEMENT_DURABILITY.md`
- `HOSTED_SAFE_STATE.md`
- `PROVIDER_READINESS_APPLICABILITY.md`
- `FIXED_TOOL_RUNTIME_APPLICABILITY.md`
- `REPLAY_FRONTEND_READINESS.md`
- `BUDGET_CAMPAIGN_READINESS.md`
- `RERELEASE_DELTA_PLAN.md`
- `WORKSPACE_STATE.md`
- changed files preserving repository-relative paths

Also create adjacent result ZIP and report SHA-256.

Never export:
- provider key or masked identifier;
- DB DSN/password;
- SSH private/public key material;
- HMAC key;
- read capability;
- raw provider output.

## 최종 응답 형식

1. result
2. target bundle path + ZIP SHA-256
3. product/security commit(s)
4. governance commit/push
5. ACL role matrix
6. hosted migration result
7. temporary access cleanup result
8. readiness dimensions PASS/BLOCKED
9. Human verification state
10. unverified items
