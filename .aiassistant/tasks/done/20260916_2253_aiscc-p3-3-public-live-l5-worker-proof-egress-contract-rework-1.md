# 작업지시서: P3-3 L5 Worker / Hosted-Proof / Egress Contract Rework

## meta

- task_id: `20260916_2253_aiscc-p3-3-public-live-l5-worker-proof-egress-contract-rework-1`
- created_at: `2026-09-16 KST`
- work_type: `REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_HEAD: `96a4029ec3a82c9b2a88b9718732aa0f00ecad20`
- reviewed_predecessor_zip_sha256: `6f38fec7898cce3016ea508d4df902490dd9d95e9d2df2c985640447d5eb2a1f`
- accepted_design_status: `ACCEPTED / CLOSED`

Use the current IDE Executor conversation. No fresh chat is required.

## rework boundary

Do NOT reopen the accepted 2012 binding design or Human D8=A decision.

Preserve unless directly required:

- dedicated Public Live ingress composition;
- structural owner-route exclusion;
- `RailwayEdgeIdentityAuthority` release gate;
- `proxy_headers=False`;
- distinct Live DB variable boundary;
- provider-secret denial in ingress;
- owner DB denial;
- Replay zero-execution architecture.

This is a focused correction of five Browser findings.

## R1 — implement a real separately startable private durable worker

Current behavior is insufficient because `public-live-worker` is check-only and raises when asked to run.

Implement the accepted private worker process using existing canonical owners rather than inventing a parallel execution stack.

Required composition:

```text
server-owned durable work source
→ accepted PipelineStore / outbox authority
→ accepted supervisor / dispatcher authority
→ single-use secret-resolution lease
→ HostedOpenAISecretResolver
→ exact hosted Luna OpenAI adapter
→ durable outcome / quarantine / retry authority
```

Requirements:

- no anonymous HTTP route;
- no owner Command Center route/import;
- Live DB only;
- no owner DB variable;
- only the worker service may resolve the OpenAI key;
- secret resolution remains after exact lease consumption;
- no child/sandbox inheritance;
- clean startup/shutdown;
- bounded polling or existing canonical durable work-loop semantics;
- no busy loop;
- no detached child/process;
- missing secret remains fail-closed before provider dispatch according to the accepted L4/L5 semantics;
- real provider calls remain impossible in tests.

`--check` may remain as a composition smoke option, but normal `aiscc public-live-worker` must run the actual durable worker process rather than intentionally fail.

If the repository has no accepted server-owned work-source/supervisor owner that can be composed without introducing new authority semantics:

`DURABLE_WORKER_COMPOSITION_DESIGN_REQUIRED`

and STOP rather than inventing one.

## R2 — make `aiscc hosted-l5-proof` an executable proof driver

The CLI must no longer merely print `ProofExpectation`.

Under exact QA-only configuration it must execute the accepted D9 proof path.

Required inputs are server/operator-owned configuration only:

- unique proof campaign;
- `AISCC_PUBLIC_LIVE_DATABASE_URL`;
- private `*.railway.internal` provider-double endpoint;
- synthetic-secret class;
- admission disabled;
- no real OpenAI key variables;
- explicit fault point.

Required behavior by fault:

### before-dispatch

- use durable proof state;
- terminate/close before durable `DISPATCH_STARTED`;
- provider-double receipt count = 0;
- outcome = definitely not sent / known closed;
- provider spend = 0;
- report the actual durable retry eligibility.

### after-dispatch

- commit `DISPATCH_STARTED`;
- perform one synthetic QA dispatch to the private provider double;
- provider double withholds/interrupts completion according to the proof protocol;
- prove one receipt;
- process generation terminates/restarts or equivalent accepted supervisor fault is exercised;
- restarted authority observes `UNKNOWN`;
- quarantine required;
- no blind resend.

### known-closed-failure

- fake provider returns a conclusively closed failure;
- retry behavior matches the exact same-role one-retry policy.

### sandbox-termination

- exercise the existing process/sandbox supervisor owner;
- prove child/container absence OR durable explicit quarantine before release.

The proof driver must emit only safe classifications/counts/opaque IDs.

It must not be reachable through HTTP.

Do not use the real OpenAI key.

## R3 — strict production hosted provider adapter

Fix the provider endpoint/profile guard.

Exact behavior:

```text
OpenAIResponsesAdapter(hosted=True)
→ accepts ONLY hosted_luna_profile()
→ exact https://api.openai.com/v1
→ no localhost
→ no *.railway.internal
→ no alternate profile

OpenAIResponsesAdapter(hosted=False)
→ acceptance/local fake endpoint only
→ never real OpenAI
```

The QA provider double must use a distinct synthetic QA transport/adapter owned by hosted proof code.

Do not loosen the production adapter to make QA work.

Add explicit negative tests proving `hosted=True` rejects loopback/fake/alternate profiles before socket creation.

## R4 — proof retry semantic consistency

Current contradiction:

```text
expectation(BEFORE_DISPATCH).retry_allowed == false
```

while durable state allows an accepted same-role retry.

Recover the exact accepted L4/L5 retry rule and make:

- `ProofExpectation`;
- CLI output;
- durable proof state;
- tests;
- reports

agree exactly.

Do not change durable retry authority merely to match the old static expectation.

## R5 — exact CORS preflight pairing

Tighten the current preflight logic.

Required:

```text
OPTIONS /v1/public-live/runs
Access-Control-Request-Method: POST
→ allowed

OPTIONS /v1/public-live/runs/{run_id}
Access-Control-Request-Method: GET
→ allowed

collection + GET preflight
→ denied

item + POST preflight
→ denied
```

Do not broaden actual methods or routes.

## mandatory tests

Add focused tests for every finding.

Minimum:

### worker

- normal worker start reaches real durable loop/supervisor composition with fake owners;
- graceful shutdown;
- missing secret pre-dispatch fail-closed;
- owner DB denied;
- no anonymous HTTP surface;
- `HostedOpenAISecretResolver` is actually part of dispatch composition;
- no real provider request.

### proof CLI

- each four fault modes executes a real proof branch, not static print;
- provider-double receipt counts are observed, not hard-coded;
- restart/reconciliation state checked;
- sandbox/process termination checked;
- real provider/key configuration denied;
- public admission must be disabled.

### provider adapter

- hosted exact Luna profile PASS with a transport double that does not hit the Internet;
- hosted loopback profile DENY before socket;
- hosted alternate profile DENY before socket;
- non-hosted real OpenAI profile DENY;
- proxy env cannot retarget;
- redirects disabled.

### proof retry

- before-dispatch reported retry eligibility matches durable authority;
- known-closed retry obeys same-role one-retry ceiling;
- unknown outcome remains no-blind-retry.

### CORS

- correct collection POST preflight PASS;
- correct item GET preflight PASS;
- wrong pairings denied.

## regression

Because shared provider/public-live runtime owners change, run the full accepted repository suite.

Predecessor evidence:

```text
1487 PASS
3 existing Windows symlink SKIP
0 FAIL
0 ERROR
```

Requirements:

- no new skip/xfail;
- explain test-count delta;
- Ruff PASS;
- formatter check changed files PASS;
- mypy changed production owners PASS;
- `git diff --check` PASS;
- secret scan PASS without printing values.

## external actions forbidden

```text
real OpenAI requests:
0

real key read/export:
0

Railway mutation/deploy/service/DB/domain:
0

Cloudflare mutation:
0

Git add/commit/push:
0

Public admission enable:
0

Public Live release:
0
```

## export contract

The result ZIP MUST include at root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `SOURCE_INVENTORY.json`
- all proof/evidence files required by this Task
- `TEST_EVIDENCE.json`
- `WORKSPACE_BEFORE.txt`
- `WORKSPACE_AFTER.txt`

And MUST include every changed source/test file under its exact project-relative path.

Do not repeat the 2148 export omission.

## acceptable outcome

Expected:

`HOSTED_PUBLIC_LIVE_BINDING_REWORKED / LOCAL_ACCEPTED_CANDIDATE`

Possible blocker:

`DURABLE_WORKER_COMPOSITION_DESIGN_REQUIRED`

Neither terminally accepts L5.

## final response

1. result
2. HEAD
3. Browser findings R1-R5 disposition
4. changed paths
5. worker composition
6. hosted proof driver
7. provider adapter strictness
8. retry semantic result
9. CORS exactness
10. focused tests
11. full regression/static/type checks
12. real provider calls
13. external actions
14. Public state
15. workspace/index
16. result ZIP SHA-256
17. next Browser gate
