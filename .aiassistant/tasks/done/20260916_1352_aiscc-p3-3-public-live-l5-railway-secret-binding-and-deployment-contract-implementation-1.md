# 작업지시서: P3-3 Public Live L5 Railway Secret Binding + Deployment Contract Implementation

## meta

- task_id: `20260916_1352_aiscc-p3-3-public-live-l5-railway-secret-binding-and-deployment-contract-implementation-1`
- created_at: `2026-09-16 KST`
- work_type: `SECURITY_SANDBOX_IMPLEMENTATION / RELEASE_PREPARATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `04436a11adc6dd6e70b4a98568fe878cc4c9f4aa`
- primary_semantic_owner: `P3-3 L5 hosted deployment / secret injection boundary`

Use the current IDE Executor conversation. No fresh chat is required.

## current state

```text
HEAD:
04436a11adc6dd6e70b4a98568fe878cc4c9f4aa

L1:
CLOSED

L2:
CLOSED

L3:
CLOSED

L4:
ACCEPTED / CLOSED

L5:
SELECTED / ENTRY_AUTHORIZED

Public admission:
DISABLED

Public Live:
NOT_RELEASED
```

## canonical Human evidence

Read:

`.aiassistant/reports/aiscc/20260916_1352_aiscc-p3-3-public-live-l4-openai-account-evidence-human-accepted.md`

This is Human-provided configuration evidence.

Never request the raw API key from Human.

## frozen authority recovery — mandatory first phase

Before mutation, recover exact L5 from frozen design commit:

`209e7534f66e9b07ce9d33742e6993370a70f4fb`

Read historical:

- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_IMPLEMENTATION_SEQUENCE.json`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_ADMISSION_SECURITY_DESIGN.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_HUMAN_DECISIONS.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_SECURITY_TEST_MATRIX.json`
- exact L5-referenced historical files

Emit:

`RESOLVED_L5_AUTHORITY.json`

Required:

- exact L5 title;
- dependencies;
- entry;
- exit;
- non-goals;
- exact historical refs;
- exact required hosted/deployment proof;
- whether real provider canary belongs to L5, L6 or later;
- ambiguity false.

If missing/ambiguous:

`POLICY_CONFLICT_INVESTIGATION_REQUIRED`

and STOP before mutation.

## current official platform facts

The Command Center has current official Railway evidence that:

- service variables are service-scoped environment variables;
- Railway variables are available to build and runtime;
- production variables can be sealed;
- sealed values are not visible in UI or retrievable via API;
- sealed variables are not copied into PR environments or duplicated environments/services;
- Southeast Asia Metal is Singapore, region id `asia-southeast1-eqsg3a`.

Reverify official Railway docs if network is available.

Do not use community guides as authority.

## accepted secret-deployment direction

The OpenAI service-account key is a hosted backend runtime credential.

It is NOT a local developer credential and NOT a public/client credential.

Required trust path:

```text
Human-controlled OpenAI secret
→ Railway production backend service variable
→ trusted server-side secret resolver
→ accepted P1-3/P1-5 SECRET capability / resolution authority
→ OpenAI Responses adapter
```

### exact forbidden destinations

Raw key must never enter:

- Git/source files;
- `.env*` committed files;
- Task/Cycle/Judgment/Handoff/export;
- browser/Cloudflare/JavaScript bundle;
- PostgreSQL;
- public request body/header/cookie;
- run workspace;
- public sandbox;
- child process environment;
- command arguments;
- stdout/stderr/log/trace;
- Replay/public evidence;
- provider durable protocol history.

## deployment variable contract

Preferred environment variable:

`AISCC_OPENAI_API_KEY`

Reason:

avoid accidental global OpenAI SDK auto-discovery outside the accepted secret resolver.

However:

- first inspect current accepted P1-3/P1-5 secret conventions;
- if an equivalent explicit non-autodiscovery variable name already exists, reuse it;
- do not create a parallel secret authority.

Do NOT use `OPENAI_API_KEY` merely for SDK convenience if that bypasses mediated resolution.

The final chosen variable name must be recorded in:

`L5_SECRET_BINDING_CONTRACT.md`

but its value must never appear.

## Railway scope contract

Target secret scope:

```text
environment:
production only

service:
exact Bounded Live backend/API service only

variable class:
service-level, NOT project-shared

protection:
sealed after Human entry

preview/PR:
must not receive production key

Cloudflare:
must not receive production key

PostgreSQL service:
must not receive production key
```

If actual repository/deployment topology uses different canonical service names, recover them and record exact identity without guessing.

## build-time exposure constraint

Railway variables are available during build as well as runtime.

Therefore audit build/deploy code for:

- environment dumps;
- debug print of all env;
- Dockerfile `RUN env` / `printenv`;
- build scripts that serialize environment;
- diagnostic bundles that capture secret variables.

Required:

`RAILWAY_SECRET_BUILD_EXPOSURE_AUDIT.md`

Any path that would print/persist the secret during build is a blocker.

Do not introduce a broader secret manager unless required.

## server-side resolver requirements

Inspect current P1-3/P1-5 secret implementation.

The trusted backend must expose only an opaque secret identity to orchestration, e.g. equivalent to:

`openai/public-live/runtime/v1`

The exact identifier may reuse an existing registry convention.

Only the trusted provider adapter/dispatcher may obtain the raw value.

Preferred semantics:

1. select immutable server-owned provider profile;
2. obtain fresh SECRET capability/resolution lease;
3. resolver reads exact configured environment variable;
4. resolver validates non-empty presence without logging;
5. raw value is handed directly to the OpenAI client constructor/request adapter;
6. raw value is never returned to Agent/run/workspace;
7. lease/use-count is consumed/revoked according to accepted P1-5 semantics.

Do not weaken the accepted secret-resolution lease model.

## child/sandbox environment proof

Inspect all subprocess/container/sandbox environment construction.

Required invariant:

```text
AISCC_OPENAI_API_KEY
(or selected equivalent)
NOT PRESENT
```

inside:

- public run process;
- Docker/sandbox child;
- tool process;
- arbitrary subprocess;
- captured environment artifact.

Use fake sentinel secret values for tests.

Never use the real key.

## missing-secret behavior

Missing/empty production key must fail closed only for Live provider work.

Expected behavior:

```text
provider capability:
UNAVAILABLE

Public Live provider request:
LIVE_UNAVAILABLE / fail closed

Replay/static:
remain available

startup/health:
must not expose key value
```

Do not make static/Replay availability depend on OpenAI credential presence.

## provider adapter binding

Bind the secret resolver result explicitly to the accepted OpenAI Responses adapter.

Do not rely on implicit environment discovery if it makes the raw key reachable outside the adapter boundary.

Keep accepted OpenAI request behavior:

```text
model:
gpt-5.6-luna

background:
false

stream:
false

store:
false

parallel_tool_calls:
false

truncation:
disabled
```

and accepted adaptive reasoning/call/token/cost/deadline policy.

## real provider canary — plan, not automatic execution

Emit:

`REAL_PROVIDER_CANARY_PLAN.md`

The canary should occur only after:

- Railway backend deployed in accepted target environment;
- production secret entered by Human;
- variable sealed;
- same trusted resolver/adapter path active;
- public admission remains disabled.

Canary requirements when later explicitly authorized:

```text
provider:
OpenAI

model:
gpt-5.6-luna

API:
Responses

reasoning:
low

input:
fixed synthetic non-secret canary

tools:
none unless frozen successor stage explicitly requires one

store:
false

background:
false

stream:
false

max paid requests:
1

max output:
minimal bounded value

public request:
none
```

Capture only:

- HTTP/provider success/failure class;
- model identifier;
- request id if non-secret;
- token usage;
- bounded cost calculation;
- latency;
- secret non-exposure result.

Do not persist raw secret or unnecessary response prose.

### canary authorization rule

If exact recovered L5 explicitly owns the canary AND all non-secret prerequisites are met, this Task may only prepare the executable canary command/path.

Do NOT execute a paid provider call in this Task.

Paid execution requires a later explicit Command Center Task after Human has injected the sealed Railway variable.

## deployment configuration

Narrowly inspect:

- `railway.toml` / config-as-code if present;
- backend service entrypoint;
- region config;
- healthcheck/readiness;
- public/private networking;
- trusted proxy handling;
- child runtime/sandbox config;
- database binding.

Allowed source/config changes in this Task:

- secret-binding resolver/config metadata;
- fail-closed missing-secret behavior;
- deployment configuration required by exact L5;
- Singapore region binding if exact L5 requires and current config lacks it;
- tests/evidence helpers directly required for this boundary.

Do not perform real deployment unless a later exact Task authorizes external Railway mutation.

## region

Accepted project direction:

`Railway Southeast Asia / Singapore`

Current official Railway region identifier:

`asia-southeast1-eqsg3a`

If exact current repository config uses a canonical equivalent, preserve it.

## rotation contract

Emit:

`OPENAI_KEY_ROTATION_RUNBOOK.md`

Required sequence:

1. create replacement key in same dedicated OpenAI Project;
2. restrict it to `/v1/responses` Write;
3. update the exact Railway sealed backend service variable;
4. deploy/restart via approved release process;
5. execute the later authorized provider canary;
6. after canary PASS, revoke previous key;
7. persist only non-secret key identity/rotation evidence.

No dual-key selection by public/runtime input.

## required tests/evidence

### `L5_AUTHORITY`
exact frozen L5 recovered.

### `SECRET_BINDING`
opaque secret ref → mediated resolver → adapter only.

### `SECRET_NON_EXPOSURE`
sentinel value absent from:
- logs;
- reports;
- child env;
- sandbox env;
- DB;
- Replay/public serialization.

### `MISSING_SECRET_FAIL_CLOSED`
Live unavailable; Replay/static independent.

### `RAILWAY_CONFIG`
service-only variable contract, sealed-production instructions, no shared/frontend propagation, Singapore target.

### `BUILD_EXPOSURE`
no env dump or secret serialization during build.

### `ROTATION`
runbook complete.

### `CANARY_PLAN`
one paid request maximum, but NOT executed.

### `REGRESSION`
focused secret/runtime tests plus directly affected Public Live/P1-3/P1-5 tests; broader suite if source changes justify it.

### `WORKSPACE_INTEGRITY`
HEAD/index/worktree before/after; no commit/push/deploy.

## Human-owned next evidence

Executor must leave these as Human pending:

- actual Railway project/service creation if not already present;
- actual service/environment identity;
- Human entry of the secret value;
- sealing the Railway variable;
- Railway deployment;
- hosted secret non-exposure confirmation;
- one paid real-provider canary;
- hosted trusted-proxy/network/runtime proof.

## forbidden

- requesting raw key from Human;
- reading password manager;
- scanning home directory for key;
- committing `.env`;
- using standard `OPENAI_API_KEY` to bypass resolver;
- real OpenAI call;
- Railway deploy/mutation;
- Cloudflare mutation;
- public enablement;
- Git commit/push;
- L6 work before exact L5 completion.

## allowed outcomes

1. `COMPLETED / ACCEPTED_CANDIDATE`
   - L5 authority resolved;
   - source/config secret boundary implemented/proven locally;
   - no external deploy/call.

2. `HUMAN_RAILWAY_DEPLOYMENT_REQUIRED`
   - local implementation/proof complete;
   - exact hosted configuration steps/evidence ready.

3. `POLICY_CONFLICT_INVESTIGATION_REQUIRED`
   - exact L5 authority conflicts with this Task.

4. `HOLD_REWORK_REQUIRED`
   - accepted secret/runtime substrate cannot safely support deployment contract.

Executor must not claim L5 terminal acceptance.

## export

Target:

`.aiassistant/reports/target/20260916_1352_aiscc-p3-3-public-live-l5-railway-secret-binding-and-deployment-contract-implementation-1/`

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `RESOLVED_L5_AUTHORITY.json`
- `L5_SECRET_BINDING_CONTRACT.md`
- `RAILWAY_SECRET_BUILD_EXPOSURE_AUDIT.md`
- `REAL_PROVIDER_CANARY_PLAN.md`
- `OPENAI_KEY_ROTATION_RUNBOOK.md`
- focused security/test evidence
- changed source/config/test files preserving relative paths

## final response

1. result
2. target bundle
3. exact L5 authority
4. chosen secret environment variable and opaque secret identity
5. exact resolver/adapter binding
6. child/sandbox non-exposure proof
7. missing-secret behavior
8. Railway service/environment/region contract
9. build-time exposure audit
10. rotation runbook
11. canary ownership/plan
12. tests/regression
13. provider calls
14. external deployment actions
15. Human pending evidence
16. Public admission before/after
17. workspace integrity
