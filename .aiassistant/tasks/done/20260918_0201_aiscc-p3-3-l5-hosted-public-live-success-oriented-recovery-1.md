# AISCC Task

## meta

- task_id: `20260918_0201_aiscc-p3-3-l5-hosted-public-live-success-oriented-recovery-1`
- phase: `P3-3 / Public Live L5`
- work_type: `HOSTED_PUBLIC_LIVE_SUCCESS_ORIENTED_RECOVERY`
- execution_model: `THIN_CC_THICK_EXECUTOR`
- entry_commit: `92a7e8305cead29bcb75c4c96ba732f2f35c4143`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- predecessor: `20260918_0115_aiscc-p3-3-l5-ingress-retained-limiter-capability-retry-1`
- supersedes_unexecuted_task: `20260918_0153_aiscc-p3-3-l5-hosted-limiter-runtime-diagnostic-1`
- public_release_authority: `NONE`

## Goal

Make the hosted Public Live L5 ingress path succeed through the current acceptance boundary:

1. valid hosted control POST reaches `503 LIVE_DISABLED`;
2. required Railway edge/spoof/CORS/method matrix passes;
3. final state remains fail-closed with Public admission `DISABLED` and Public Live `NOT_RELEASED`.

The Executor owns the implementation method inside the contract below.

## Must preserve

- Public Replay remains unchanged and publicly available.
- Public admission remains `DISABLED`.
- Public Live remains `NOT_RELEASED`.
- OpenAI/provider calls remain `0`.
- ingress database authority remains least-privilege; no raw table DML authority.
- no owner workflow authority is granted to ingress.
- no secret, DSN, password, HMAC key, private key, client IP, or raw sensitive header value is exported.
- accepted migration/source history remains forward-only; no destructive rollback of accepted hosted state.
- Human/Browser retains release and state-transition authority.

## Must not do

- enable Public admission.
- perform OpenAI/provider inference.
- change Cloudflare Replay or competition submission surface.
- change frozen product semantics, budgets, scenario identity/version, retention policy, client identity policy, or release policy.
- broaden ingress into owner/runtime/reconciler/execution/initializer authority.
- mutate owner API, worker, or initializer configuration deliberately.
- perform destructive data reset or delete accepted hosted evidence/state to make tests pass.
- add unrelated production-hardening work.
- download/install unapproved runtimes or tools from the Internet.

Passive Railway autodeploys caused solely by an authorized Git push are not by themselves a Task violation. Do not manually reconfigure unrelated services; observe their health/state only.

## Authority closure

The Executor may solve any implementation/environment issue required to achieve the Goal **within Public Live L5 ingress / limiter / fixed-campaign bootstrap / related hosted binding boundaries**, provided all Must preserve / Must not do clauses remain true.

Already-frozen values may be materialized if missing. If a required value is not already canonically determined and choosing it would create new product/security semantics, HOLD.

The Executor may create forward migrations, source/test changes, fixed-scenario bootstrap/configuration logic, or narrow Railway ingress/DB changes when they are necessary to satisfy the existing frozen design. The Executor may commit and push such changes after proving them locally.

No L6/L7/L8 transition is authorized by this Task.

## Allowed mutation surface

- `src/aiscc/public_live/**`
- Public Live persistence/limiter/ingress support code needed for L5
- `migrations/versions/**` only for forward Public Live corrections
- related Public Live unit/integration tests and fixtures
- task-owned temporary helper scripts/files outside canonical source
- hosted Public Live PostgreSQL schema/state only insofar as it materializes already-frozen Public Live L5 prerequisites
- Railway ingress service and task-owned temporary private diagnostic/migrator services
- Git commits/pushes for in-scope source changes
- canonical Task/report export handling

Changes outside this surface require HOLD unless they are non-semantic generated/test residue that can be safely ignored or cleaned.

## Executor freedom

Within the contract, choose the most effective implementation method yourself.

Examples of allowed freedom:

- locate and use an already-approved Python interpreter (`uv`, project `.venv`, IDE interpreter, approved container/runtime, etc.);
- choose shell/PowerShell/Python helpers;
- create narrow temporary diagnostics;
- choose test fixture strategy;
- choose test order and commands;
- choose Railway CLI/API workflow;
- choose one or multiple logically scoped commits;
- choose migration/helper structure;
- inspect canonical source/history to resolve implementation details;
- replace a failing operational mechanism with an equivalent one when semantic/security authority is unchanged.

Do not STOP merely because the procedure differs from what Browser CC might have expected.

## Current known evidence

- canonical `main` baseline: `92a7e8305cead29bcb75c4c96ba732f2f35c4143`.
- `20260918_0022` aligns ingress with retained limiter wrappers.
- ignored non-authority forwarding headers were corrected.
- local targeted checks passed for the 0115 correction.
- hosted DB reached migration `20260918_0022`.
- ingress function surface remained exactly 8 and raw DML remained 0.
- hosted `/health` returned `200`.
- valid hosted POST still returned `503 LIVE_UNAVAILABLE`.
- final public ingress domain and edge-trust exposure were removed after the failed proof.

Treat `LIVE_UNAVAILABLE` as the current implementation problem to solve, not as a predetermined root cause.

## Evidence expected

Provide enough evidence for Browser independent judgment, not a prescribed command transcript.

At minimum:

- exact entry and final Git commit(s);
- concise explanation of diagnosed root cause and why the chosen fix stays inside existing semantics;
- source/migration/test paths changed;
- relevant automated test results;
- effective ingress DB authority proof after changes;
- hosted migration/configuration state required by the fix;
- hosted control POST result;
- spoof/overwrite/CORS/method matrix result if control reaches `LIVE_DISABLED`;
- final public-domain / edge-trust / admission / OpenAI-call state;
- any passive unrelated Railway autodeploy observed as a side effect of Git push;
- exact result ZIP SHA-256 and manifest integrity.

Do not export raw secrets or uncontrolled error bodies.

## Stop boundary

HOLD / STOP only when one of these is true:

- success requires changing a frozen product/security semantic rather than implementing it;
- success requires Public admission enablement or an OpenAI/provider call;
- success requires materially broader DB/service authority;
- success requires deliberate mutation of owner API / worker / initializer authority or behavior;
- success requires destructive accepted-state deletion/reset;
- success requires a new external paid product/service or materially new cost commitment;
- success requires public exposure beyond the bounded ingress proof;
- there are multiple unrelated architectural blockers such that this is no longer a bounded L5 implementation problem;
- no approved runtime/toolchain can be found locally without external installation;
- evidence cannot distinguish safe success from a security/authority regression.

A different command, interpreter, helper, fixture, deployment mechanism, or commit shape is **not** a STOP condition by itself.

## Success

`L5_HOSTED_INGRESS_PROOF_CANDIDATE_SUCCESS` requires:

- valid control POST reaches `503 LIVE_DISABLED`;
- spoof/overwrite checks preserve trusted `X-Real-IP` authority and reject ambiguous attacker-controlled authority;
- required CORS/method/route behavior passes;
- ingress stays least-privilege;
- admission remains disabled;
- provider/OpenAI calls remain 0;
- final exposure is exactly the Task-intended safe state.

This Task does not release Public Live.

## export

Create:

`.aiassistant/reports/target/20260918_0201_aiscc-p3-3-l5-hosted-public-live-success-oriented-recovery-1/`

Required root files:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `EVIDENCE_SUMMARY.md`

Include changed source/migration/test files or patches sufficient for Browser review when source mutation occurs.

Also create:

`.aiassistant/reports/target/20260918_0201_aiscc-p3-3-l5-hosted-public-live-success-oriented-recovery-1.zip`

Verify ZIP member integrity and report ZIP SHA-256.
