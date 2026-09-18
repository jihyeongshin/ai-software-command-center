# 작업지시서: P3-3 L8 fresh re-release readiness preflight

## meta

- task_id: `20260919_0102_aiscc-p3-3-l8-fresh-rerelease-readiness-preflight-1`
- created_at: `2026-09-19T01:02:00+09:00`
- work_type: `L8_RERELEASE_READINESS_PREFLIGHT`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- exact_baseline: `61ce804988dd0c32fef112f23bb2193b07a83541`
- fresh_ide_chat_required: `No`
- hosted_mutation_authority: `NONE`
- public_release_authority: `NONE`
- public_run_authority: `NONE`
- provider_call_authority: `NONE`
- Railway_config_mutation_authority: `NONE`
- Cloudflare_mutation_authority: `NONE`
- DB_mutation_authority: `NONE`

## 현재 상태

Browser Command Center has accepted the 2344 retained-run settlement.

```text
retained 1919 run:
FAILED_NOT_DISPATCHED

reservation:
SETTLED / settled_cost=0

slot:
FREE

outbox:
CLOSED

held liability:
0

Public admission:
DISABLED

Public Live:
NOT_RELEASED

ingress / worker public domains:
0 / 0

Replay:
PUBLIC / UNCHANGED
```

Affected hosted L5 is `ACCEPTED / CLOSED`.
Affected L6 remains `ACCEPTED`.
L7 is `ACCEPTED / CLOSED`.
The real Luna canary is historical accepted evidence and may be reused only if its exact applicability remains unchanged.

Known workspace note:
- prior Executor reported unrelated untracked governance residue and local `__pycache__`.
- do not clean/reset unrelated paths.
- do not treat unrelated pre-existing dirt as a blocker unless it collides with an exact path needed by this Task.

## 이번 턴 목표

Perform a fresh **read-only** release-readiness preflight after settlement.

Establish whether the current system can safely proceed to a later Human-authorized Public Live re-release without changing any hosted/public state in this Task.

The Executor chooses the inspection mechanics. CC owns the semantic/security boundary below.

## 반드시 확인할 readiness dimensions

### 1. repository / canonical authority

- `HEAD == origin/main == 61ce804988dd0c32fef112f23bb2193b07a83541` at entry, unless an exact already-supplied Browser artifact placement explains a governance-only delta.
- supplied Cycle/Judgment/Handoff are placed at canonical paths.
- 2344 Task remains under `tasks/done`.
- no product/runtime/source mutation is required for this preflight.

### 2. retained 1919 settlement durability

Read-only prove the accepted settlement remains durable:

- target run `FAILED_NOT_DISPATCHED`;
- reservation `SETTLED / settled_cost=0`;
- no held 200000 residue;
- slot `FREE`;
- outbox `CLOSED`;
- exactly one closure observation;
- exactly one SETTLE money event;
- historical worker-work retained and non-claimable;
- no second refund/event/state regression.

Do not perform another close.

### 3. fail-closed hosted state

Freshly observe:

- Public control disabled;
- Public Live not released;
- ingress public domains 0;
- worker public domains 0;
- edge trust absent;
- no active future-deadline Public Live run;
- no claimable work;
- unreleased claims 0;
- dispatch pins 0;
- public dispatch rows 0;
- execution operations 0;
- no new Public Live provider request.

### 4. provider-secret / provider-readiness applicability

Without reading or resolving secret values:

- worker remains sole provider-secret owner;
- worker credential remains sealed/service-local;
- ingress/initializer/API provider-key authority remains absent;
- no standard/provider duplicate secret exposure is reintroduced;
- accepted provider adapter/model/profile for `gpt-5.6-luna` is unchanged from the accepted canary lineage.

Do **not** run another real provider canary.

If accepted canary applicability is no longer exact, report a named readiness blocker rather than calling the provider.

### 5. Public fixed-tool runtime applicability

Freshly verify the currently deployed worker/runtime still corresponds to the Human-accepted Public fixed-tool contract:

```text
PUBLIC_BOUNDED_LIVE
stockroom-s1-normal / 1.0.0
Tool Broker
→ TOOL authority only
→ fixed deterministic in-process Stockroom dispatcher
```

For the Public fixed tool:
- process capability 0;
- filesystem capability 0;
- tool-network capability 0;
- tool-secret capability 0;
- Docker is not a Public Live prerequisite.

Owner/Self-Dogfood Docker path remains a separate unchanged contract.

Do not redeploy.

### 6. Replay/frontend readiness

- Recorded Run Replay remains publicly reachable and unchanged.
- current public page is still fail-closed for Live while release-disabled.
- no stale visible copy/config contradicts disabled state.
- determine the exact already-accepted frontend/config delta that a later release Task would need, but do not apply it.
- Replay must remain independently usable if a later Live attempt fails.

### 7. budget/campaign readiness

Read-only verify the frozen release constraints remain internally coherent, including:
- campaign `public-live-v1`;
- fixed scenario/version;
- cutoff `2026-10-17T15:00:00Z` exclusive;
- per-run reservation `200000 micro-USD`;
- daily/campaign budgets and start/concurrency bounds already accepted for this release lineage;
- no held liability from 1919 remains.

Do not enable or prepare the campaign in this Task if doing so mutates hosted state.

### 8. exact re-release delta / rollback plan

Produce a concise release-delta plan from the **current observed state** to a future release attempt.

It must distinguish:
- mutations a later Human-authorized release Task would perform;
- proof to collect before/after each mutation;
- exact rollback trigger;
- Replay-only rollback end state.

Do not execute the plan.

## evidence contract

executor_required:
- repository/head/Task provenance verification
- read-only hosted settlement durability proof
- read-only fail-closed hosted state
- read-only provider-secret ownership metadata proof without secret value
- fixed-tool deployed-runtime applicability
- Replay/frontend disabled-state check
- budget/campaign read-only readiness
- release-delta / rollback plan
- exact changed-path inventory
- secret-safe export scan
- `git diff --check` for any governance-only persistence

reuse_allowed:
- 2344 Browser-accepted settlement evidence, only for identity/history; durability must be freshly observed
- affected L5/L6 accepted proof when unchanged applicability is freshly established
- L7 Human QA/source proof when frontend source/config lineage is unchanged
- real Luna canary only if worker secret/provider/model/profile applicability is exactly unchanged
- prior Replay acceptance when public artifact/hash/deployment lineage remains unchanged

human_owned:
- Public Live re-release decision
- any actual activation/release
- final public-site smoke after a later release
- provider/account UI corroboration if later explicitly requested

not_required:
- new real provider call
- new public run
- new browser Human QA in this preflight
- broad regression suite
- production-hardening redesign

forbidden:
- DB mutation
- another settlement/close
- provider call
- new public run
- admission enablement
- public domain creation
- edge-trust mutation
- Railway variable/deployment/resource mutation
- Cloudflare mutation
- provider-secret read/copy/rotation
- migration/grant/new login
- unrelated source changes

## proof non-substitution

- historical 2344 settlement evidence != fresh durability observation
- old canary != current canary applicability unless exact unchanged lineage is proved
- source config != deployed hosted state
- automated frontend check != Human final public-site smoke
- Executor readiness claim != Browser acceptance
- Browser readiness acceptance != Human release authorization

## success result

Return only if all readiness dimensions are satisfied:

```text
RERELEASE_READY_CANDIDATE
/
HUMAN_RELEASE_DECISION_REQUIRED
/
BROWSER_REVIEW_REQUIRED
```

This is not release authorization.

## blocked result

If any readiness dimension is stale, unsafe, ambiguous, or would require mutation/provider use to prove, return:

```text
RERELEASE_READINESS_BLOCKED
/
<EXACT_NAMED_BLOCKER>
/
BROWSER_REVIEW_REQUIRED
```

Preserve fail-closed state.

## mandatory stop 조건

STOP after minimum evidence if:

- current hosted state contradicts accepted settlement/safety state;
- any unexpected claimable/public work exists;
- provider request/send would be required to establish readiness;
- secret value would need to be read;
- a hosted mutation is required merely to inspect readiness;
- a public domain or enabled control is unexpectedly present;
- provider-secret isolation is not exact;
- deployed runtime no longer matches the accepted fixed-tool contract;
- Replay is unavailable or Live-disabled truthfulness is broken;
- authority/canonical baseline conflicts;
- unrelated dirty state collides with required exact paths.

## canonical persistence

Persist supplied Cycle/Judgment/Handoff and update current state/decision/next action truthfully for the Browser-accepted 2344 settlement and this readiness candidate.

Ordinary commit/push is authorized **only** for exact governance/task-lifecycle persistence created by this Task.

No product/runtime/test/migration/config change may be committed.

No amend/rebase/force-push.

## target export

Create:

`.aiassistant/reports/target/20260919_0102_aiscc-p3-3-l8-fresh-rerelease-readiness-preflight-1/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `REPOSITORY_AUTHORITY.md`
- `SETTLEMENT_DURABILITY.md`
- `HOSTED_SAFE_STATE.md`
- `PROVIDER_READINESS_APPLICABILITY.md`
- `FIXED_TOOL_RUNTIME_APPLICABILITY.md`
- `REPLAY_FRONTEND_READINESS.md`
- `BUDGET_CAMPAIGN_READINESS.md`
- `RERELEASE_DELTA_PLAN.md`
- `WORKSPACE_STATE.md`
- changed governance files preserving repository-relative paths

Also create adjacent result ZIP and report SHA-256.

Never export:
- provider key or masked key identifier;
- DB DSN/password;
- HMAC key;
- read capability;
- raw provider output.

## 최종 응답 형식

1. result
2. target bundle path + ZIP SHA-256
3. canonical commit/push if performed
4. readiness dimensions PASS/BLOCKED
5. human verification: `HUMAN_PENDING` only if readiness candidate is ready
6. unverified items
7. preserved exact paths
