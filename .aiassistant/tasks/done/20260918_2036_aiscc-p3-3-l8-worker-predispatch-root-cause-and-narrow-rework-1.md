# AISCC Task — L8 Worker Pre-Dispatch Root Cause and Narrow Rework

## meta

- task_id: `20260918_2036_aiscc-p3-3-l8-worker-predispatch-root-cause-and-narrow-rework-1`
- phase: `P3-3 / L8 re-release recovery`
- work_type: `WORKER_PREDISPATCH_ROOT_CAUSE_AND_NARROW_REWORK`
- execution_model: `THIN_CC_THICK_EXECUTOR`
- entry_commit: `6c5251fcfd78e01fa1a881f1bfd14b8af5d4bc9c`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- public_release_authority: `NONE`
- public_run_authority: `NONE`
- real_provider_call_authority: `NONE`
- hosted_DB_mutation_authority: `NONE`
- Railway_public_exposure_authority: `NONE`

## Goal

Confirm and correct the exact worker pre-dispatch failure that caused the 1919 public smoke to remain `ADMITTED`, while the system stays Replay-only and no new provider/public run is created.

Also repair the accidental Git tracking of the temporary 1919 target export and reconcile current governance state.

## Current accepted facts

- Public Replay is the current public surface.
- Public admission is disabled.
- Public Live is not released.
- frontend config is disabled/null.
- ingress public domain is absent.
- edge trust is absent.
- worker provider credential remains worker-only/sealed.
- failed 1919 smoke:
  - one public run;
  - start request BOUND;
  - workflow/execution RUNNING;
  - one worker claim;
  - zero execution operations;
  - zero dispatch/provider-request rows;
  - zero provider sends;
  - no UNKNOWN send;
  - claim released/recovered `LIVE_UNAVAILABLE`.
- campaign and failed-run accounting are retained evidence.

## Strong Browser hypothesis

Current source has this pre-operation path:

```text
_execute_production_claim()
  -> compose_public_stockroom(...)
  -> stockroom.dispatcher(..., runner=None, ...)
  -> shutil.which("docker")
  -> if absent: PUBLIC_LIVE_STOCKROOM_DOCKER_REQUIRED
```

`AgentExecutionService.execute()` is called only after dispatcher construction.

The hosted evidence shows exactly zero execution operations.

Treat this as a hypothesis to prove, not as a fact to assume.

## Goals in order

1. Verify entry HEAD/origin main and current fail-closed external state.
2. Persist the supplied rollback Cycle/Judgment/Handoff.
3. Reconcile:
   - `CURRENT_STATE_SUMMARY.md`
   - `DECISION_REGISTER.md`
   - `NEXT_ACTIONS.md`
   to the actual current state:
   Human release authorized historically, one activation attempt rolled back, Replay-only current, L8 still open/rework.
4. Remove the accidentally tracked:
   `.aiassistant/reports/target/20260918_1919_aiscc-p3-3-l8-public-live-final-activation-and-smoke-1/**`
   from canonical Git tracking.
   The local ignored export may remain if useful; do not treat cleanup failure as product failure.
5. Add the smallest secret-safe worker failure observability needed to preserve an allowlisted pre-dispatch failure classification.
6. Confirm the exact failure boundary using:
   - local/disposable exact-role reproduction and/or
   - read-only/presence-only hosted worker inspection,
   without creating a public run or provider request.
7. If the exact bug can be corrected **without weakening the accepted tool/process/network/filesystem isolation semantics or adding new external resources**, implement the narrow fix and prove the production worker can reach the first durable operation using a synthetic/no-send fixture.
8. If fixing it requires changing the accepted isolation/runtime security contract, stop with:
   `HOSTED_STOCKROOM_RUNTIME_DECISION_REQUIRED`
   and describe the smallest truthful alternatives.

## Must preserve

- Replay public/unchanged.
- Public admission disabled.
- Public Live not released.
- ingress remains private/no edge trust.
- no new public run.
- no real OpenAI/provider call.
- worker provider key stays sealed and worker-only.
- no provider secret output/logging.
- failed 1919 run/campaign/reservation/slot evidence is not deleted or rewritten.
- no DB migration or privilege expansion.
- accepted L3-L7 evidence remains historical authority.
- `AGENT_OUTPUT != SYSTEM_STATE`.

## Must not do

- create another Public Live run;
- enable control/admission;
- create ingress domain/edge trust;
- deploy enabled frontend/Cloudflare Live config;
- perform real provider call;
- consume the production API key for diagnosis;
- mutate campaign/run/reservation/slot rows;
- settle/delete the failed smoke run in this Task;
- add new Railway service/database/resource;
- change DB role/grants;
- change scenario/model/provider;
- weaken network/filesystem/process isolation merely to make Railway work;
- silently replace the accepted Stockroom tool with a fake/precomputed result;
- broaden CSP;
- amend/rebase/force-push.

## Governance cleanup contract

Current `main` tracks a temporary target subtree even though:

```text
.gitignore:
.aiassistant/reports/target/

IDE_EXECUTOR_REPORT_EXPORT:
target bundle = temporary / Git ignored
```

Remove that exact 1919 target subtree from Git tracking.

Preferred:
- preserve local ignored bytes if still needed;
- commit repository deletions only.

Do not remove canonical:
- 1919 Cycle;
- 1919 Judgment;
- 1919 Handoff;
- 1919 done Task.

## Safe observability contract

The worker loop currently swallows exceptions.

Add only the minimum observability necessary to classify a failure without leaking:
- exception values that may contain DSNs/secrets;
- environment values;
- provider output;
- capability/token material.

Allowed evidence shape examples:
- fixed internal error code;
- allowlisted exception class;
- stage name such as `STOCKROOM_COMPOSITION`, `EXECUTION_ENTRY`, `OPERATION_CREATE`;
- one-way digest of a fixed safe classification payload.

Do not dump `repr(error)` or raw exception strings unless the code is explicitly allowlisted and known non-secret.

Observability must not change retry/send semantics.

## Root-cause proof

At minimum prove:

### A. hosted worker runtime prerequisite

Presence-only:
- exact worker service;
- whether a trusted Docker executable/daemon path required by current `StockroomDockerRunner` is actually available;
- no secret values.

### B. code-order proof

Show whether the failure occurs:
- before `AgentExecutionService.execute()`;
- before `create_operation`;
- before provider capability/secret resolution;
- before provider send.

### C. exact reproduction

Use an isolated/disposable PostgreSQL at migration head `20260918_0023` with the real execution role/permissions where feasible.

Reproduce the production worker composition with:
- fixed scenario;
- no real provider;
- no public exposure.

If a synthetic runner is injected only for test comparison, label it clearly and do not use that as proof that the hosted production runtime works.

### D. retained hosted evidence consistency

Map the 1919 durable evidence to the confirmed failure stage:
- BOUND start;
- acquired claim;
- no operation;
- no provider send.

## Narrow fix authority

Executor may implement a fix only when all of the following are true:

- no new security/product semantic;
- no weaker process/network/filesystem boundary;
- no new external persistent resource;
- no DB migration/grant;
- no provider/public release requirement.

Examples of potentially in-scope fixes:
- incorrect runtime-path lookup;
- lazy construction ordering when it preserves the same eventual sandbox contract;
- packaging omission where the exact accepted sandbox runtime is already supported by the existing deployment;
- safe error handling/claim release that does not alter send authority.

If the real problem is that Railway cannot provide the accepted Docker/process isolation mechanism at all, that is **not** an in-scope implementation detail.

Return:

`HOSTED_STOCKROOM_RUNTIME_DECISION_REQUIRED`

Do not invent a weaker substitute.

## Failed-smoke accounting

Read-only determine:
- current failed run state;
- held reservation;
- slot state/generation;
- whether an already-accepted canonical reconciliation operation exists for definitely-not-sent pre-dispatch expiry.

Do not execute reconciliation in this Task.

Produce the exact future reconciliation action, if one already exists, or state that a separately authorized recovery design is required.

## Railway authority

Read-only/presence-only inspection is allowed.

A private worker redeploy is allowed only if:
- required to deploy the secret-safe observability or a narrow semantics-preserving fix;
- no environment variable/secret/domain/edge/control changes occur;
- no work exists that can cause provider dispatch.

Do not expose ingress.

## Tests / verification

When source changes:
- focused worker pre-dispatch tests;
- exact failure-observability tests;
- Public Live worker/authority regression;
- disposable PostgreSQL exact-role path where required;
- `git diff --check`;
- Ruff/format/narrow mypy.

No real provider request.

## Stop boundary

Stop with the narrowest exact result if:

- Railway lacks the accepted sandbox mechanism and replacement changes security semantics;
- a new service/daemon/paid resource is needed;
- DB migration/grant is needed;
- failed-run recovery needs new policy;
- any provider/public run is required to prove the fix;
- raw secret/error disclosure would be required.

## Acceptance targets

Possible successful outputs:

```text
WORKER_PREDISPATCH_ROOT_CAUSE_CONFIRMED / NARROW_FIX_CANDIDATE
```

or, when the fix is also safely completed/proven:

```text
WORKER_PREDISPATCH_NARROW_FIX_CANDIDATE / BROWSER_REVIEW_REQUIRED
```

or the honest boundary:

```text
HOSTED_STOCKROOM_RUNTIME_DECISION_REQUIRED
```

No result in this Task means Public Live is released.

## Git / persistence

- baseline must start at `6c5251fcfd78e01fa1a881f1bfd14b8af5d4bc9c`;
- ordinary commit/push authorized after proof;
- remove the accidental tracked target subtree;
- current Task active -> done;
- do not track the new target export;
- no amend/rebase/force push.

## export

Create:

`.aiassistant/reports/target/20260918_2036_aiscc-p3-3-l8-worker-predispatch-root-cause-and-narrow-rework-1/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `ROOT_CAUSE_PROOF.md`
- `HOSTED_RUNTIME_PREREQUISITE.md`
- `FAILED_SMOKE_ACCOUNTING.md`
- `GOVERNANCE_RECONCILIATION.md`
- `FINAL_SAFE_STATE.md`
- `WORKSPACE_STATE.md`
- changed files preserving project-relative paths

Also create the adjacent result ZIP.

The target bundle must remain Git-ignored/untracked.

Never export:
- raw OpenAI key;
- DB DSN;
- HMAC key;
- read capability;
- raw provider output;
- unbounded/raw exception payloads.
