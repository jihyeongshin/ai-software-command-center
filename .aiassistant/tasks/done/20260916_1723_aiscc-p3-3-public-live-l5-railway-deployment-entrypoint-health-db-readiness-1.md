# 작업지시서: P3-3 L5 Railway Deployment Entrypoint / Health / DB Readiness

## meta

- task_id: `20260916_1723_aiscc-p3-3-public-live-l5-railway-deployment-entrypoint-health-db-readiness-1`
- created_at: `2026-09-16 KST`
- work_type: `DEPLOYMENT_READINESS_IMPLEMENTATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_HEAD: `96a4029ec3a82c9b2a88b9718732aa0f00ecad20`
- primary_semantic_owner: `P3-3 L5 hosted deployment readiness`

Use the current IDE Executor conversation. No fresh chat is required.

## current authoritative state

```text
accepted/published HEAD:
96a4029ec3a82c9b2a88b9718732aa0f00ecad20

Railway Project:
AISCC

Environment:
production

Postgres:
Online / Singapore

Backend service:
aiscc-public-live-api
Singapore / 1 replica / Offline

Railway Source:
jihyeongshin/ai-software-command-center
branch main
STAGED ONLY / NOT DEPLOYED

Railway Start Command:
UNSET

Railway Healthcheck Path:
UNSET

OpenAI production secret:
NOT ENTERED

Public admission:
DISABLED

Public Live:
NOT_RELEASED
```

## mandatory preflight

Require:

- HEAD exactly `96a4029ec3a82c9b2a88b9718732aa0f00ecad20`;
- index empty;
- accepted source tree unchanged;
- no tracked source mutation since the accepted/published commit.

If not: STOP.

## Phase A — source audit before mutation

Inspect exact current repository owners for:

- `pyproject.toml`;
- `uv.lock`;
- `src/aiscc/__main__.py`;
- `src/aiscc/bootstrap.py`;
- `src/aiscc/api/**`;
- persistence/database configuration;
- Alembic configuration and migration invocation;
- existing health/status routes;
- current environment variable conventions;
- `config/deployment/public-live-railway.v1.toml`;
- tests covering API startup/bootstrap/database/provider-secret absence.

Write first:

`RAILWAY_DEPLOYMENT_READINESS_AUDIT.md`

It must answer from source, not guess:

1. What exact command currently starts the HTTP API?
2. Does it bind to `0.0.0.0` and Railway-provided `PORT`?
3. What exact route can be used as liveness/healthcheck?
4. Does that route perform provider inference, resolve the OpenAI secret, mutate state, or depend on Public Live admission?
5. What exact environment variable/config supplies PostgreSQL?
6. How is Alembic `upgrade head` expected to run in deployment?
7. Can the trusted API process start with `AISCC_OPENAI_API_KEY` missing?
8. Does a missing OpenAI key remain `LIVE_UNAVAILABLE` only at hosted provider execution?
9. Does startup or health make any real provider/network call?
10. What exact Railway Build / Pre-deploy / Start / Health values should Human configure?

If all required production behavior already exists and is proven, do not mutate source merely to create a new abstraction.

## Phase B — narrow implementation only if required

If one or more required behaviors are absent, implement the smallest compatible change.

Authorized source scope:

- `pyproject.toml` only if an existing project script/entrypoint must be corrected or added;
- `src/aiscc/__main__.py`;
- `src/aiscc/bootstrap.py`;
- exact files under `src/aiscc/api/` that own application startup/routes;
- exact persistence configuration file(s) needed to consume the existing production DB URL convention;
- `config/deployment/public-live-railway.v1.toml` as deployment metadata/contract only;
- directly corresponding tests.

Do not refactor unrelated workflow/security/provider logic.

### server entrypoint requirements

Hosted API must:

- listen on `0.0.0.0`;
- consume the platform-provided `PORT`;
- reject invalid port configuration deterministically;
- not require the OpenAI API key merely to boot;
- not invoke OpenAI/provider during import/startup;
- preserve Public admission `DISABLED`.

Prefer an existing canonical CLI/module entrypoint if it already owns these semantics.

Do not introduce a second competing application bootstrap.

### health/readiness requirements

Choose exact route(s) based on current architecture.

At minimum Railway healthcheck route must be:

- unauthenticated only if current public health convention permits it;
- read-only;
- bounded;
- no provider call;
- no OpenAI secret resolution;
- no Task/run creation;
- no state transition;
- no evidence admission;
- no Public Live enablement.

If DB readiness is part of the route, it may perform only the minimum bounded read needed to prove the authoritative PostgreSQL dependency is reachable.

Do not expose DSN, credentials, internal exceptions or schema data.

### PostgreSQL binding

Determine the current canonical application variable name from source.

Do not invent a new variable name if an accepted one already exists.

Production contract must use Railway private/internal Postgres connectivity, not Postgres Public Access.

Do not copy DB credentials into source/governance.

### migration contract

Determine the safest existing migration command.

Preferred deployment contract is an explicit Railway **Pre-deploy** migration command rather than hidden migration on every application import/start, unless current accepted architecture already proves another safe owner.

Do not execute against the real Railway database in this Task.

### missing provider secret

Locally prove that with `AISCC_OPENAI_API_KEY` absent:

- API process can boot;
- health/readiness can succeed when non-provider dependencies are healthy;
- no OpenAI SDK/provider request occurs;
- an actual hosted-provider execution attempt fails closed as the already accepted `LIVE_UNAVAILABLE` pre-dispatch path.

No real credential.

## Phase C — local runtime proof

Use task-owned local PostgreSQL 17.6 if needed.

No private/pre-existing DB.

Use cached image only; no pull if the accepted Task convention still applies.

Prove the exact production-like start command locally using a non-default test `PORT`.

Required runtime evidence:

- process starts;
- binds expected host/port;
- health endpoint returns expected bounded response;
- no OpenAI key;
- provider calls 0;
- DB dependency behavior matches documented readiness semantics;
- graceful process shutdown;
- no secret/environment dump.

If exact deployment command depends on a package build/install step, reproduce it using the repository's accepted `uv` workflow.

## exact Railway contract output

Emit:

`RAILWAY_RUNTIME_CONFIGURATION.md`

with explicit Human-enterable values:

```text
Root Directory:
<exact>

Builder:
<exact; prefer Railway/Railpack default if sufficient>

Build Command:
<exact or DEFAULT>

Pre-deploy Command:
<exact or NONE>

Start Command:
<exact>

Healthcheck Path:
<exact>

PORT:
Railway-provided / do not hard-code

Backend Region:
asia-southeast1-eqsg3a

Postgres connection:
<exact application variable name and Railway reference strategy; no credential value>

AISCC_OPENAI_API_KEY:
NOT YET ENTERED / service-only sealed later

Serverless:
<recommended exact current value>

Restart Policy:
<recommended exact current value>
```

Do not include any secret value.

## tests/checks

Run:

- focused startup/health/config tests;
- API tests affected by changes;
- persistence bootstrap tests affected by DB config;
- hosted missing-secret regression;
- Ruff;
- format check;
- mypy on changed production files;
- `git diff --check`.

If production source changes shared startup/bootstrap logic, run the appropriate broader repository regression and state the exact scope/reason.

## real external actions forbidden

```text
Railway Deploy Changes:
0

Railway variable mutation:
0

Railway DB mutation:
0

Railway public networking mutation:
0

OpenAI secret read/use:
0

real OpenAI/provider calls:
0

Cloudflare mutation:
0

Git commit:
0

Git push:
0

Public enable:
0
```

## acceptable outcomes

### no source change needed

`DEPLOYMENT_READINESS_PROVEN / CONFIGURATION_ONLY_CANDIDATE`

### source/test change needed and all local proof passes

`DEPLOYMENT_READINESS_IMPLEMENTED / LOCAL_ACCEPTED_CANDIDATE`

Neither outcome terminally closes L5.

## mandatory stop

- HEAD mismatch;
- exact HTTP bootstrap cannot be established from source;
- safe health route would require security-policy weakening;
- Railway startup would require exposing provider secret to build/public context;
- production DB binding requires Public Access;
- migration ownership requires an architectural redesign;
- local production-like startup proof cannot run;
- real Railway/OpenAI credential/action is required to continue.

## export

Create:

`.aiassistant/reports/target/20260916_1723_aiscc-p3-3-public-live-l5-railway-deployment-entrypoint-health-db-readiness-1/`

Required:

- `EXECUTOR_REPORT.md`
- `RAILWAY_DEPLOYMENT_READINESS_AUDIT.md`
- `RAILWAY_RUNTIME_CONFIGURATION.md`
- `TEST_EVIDENCE.json`
- `SOURCE_INVENTORY.json` if source changed
- `LOCAL_POSTGRES_RUNTIME.json` if PostgreSQL runtime is used
- `WORKSPACE_BEFORE.txt`
- `WORKSPACE_AFTER.txt`
- exact Task copy
- result ZIP

## final response

1. result
2. HEAD
3. source audit conclusion
4. exact HTTP entrypoint
5. exact host/PORT behavior
6. exact healthcheck route
7. DB variable/binding contract
8. migration contract
9. missing OpenAI secret startup behavior
10. local production-like runtime proof
11. provider calls
12. source/test changes
13. focused/broader tests
14. static/type/diff checks
15. exact Railway Human configuration values
16. external actions
17. Public state
18. workspace integrity
19. next Human Railway deployment gate status
