# 작업지시서: P3-3 L5 Railway Private Initializer + Worker Deployment

## meta

- task_id: `20260917_1652_aiscc-p3-3-public-live-l5-railway-private-initializer-worker-deployment-1`
- created_at: `2026-09-17 KST`
- work_type: `HOSTED_INFRASTRUCTURE`
- evidence_profile: `HIGH_RISK_NARROW_HOSTED`
- canonical_commit: `baed7ea3360f6c67c0409c25f84137ab446b90ac`
- accepted_phase_a_result_zip_sha256: `66192de47871e76489101e36a0c3bbec70a43d9114b11ce1fdc7804ed6c62e81`
- live_postgres_service_id: `5238e804-eb7f-4645-b2a8-e134056be72c`
- live_postgres_deployment_id: `c21d2f5e-a5c2-4f11-850a-6b99f9d270d7`
- public_release_effect: `NONE`

Use the current IDE Executor conversation.

This Task owns ONLY the private initializer and private worker hosted runtime deployment.

It does not authorize public ingress, OpenAI-key cutover, trusted-API cutover, Cloudflare changes, paid provider calls, or Public release.

## fixed accepted runtime shape

Create exactly two long-lived private services:

```text
aiscc-public-live-initializer
aiscc-public-live-worker
```

Both:

- Railway project `AISCC`;
- environment `production`;
- Singapore / `asia-southeast1-eqsg3a`;
- source repository `jihyeongshin/ai-software-command-center`;
- source deployment commit must equal `baed7ea3360f6c67c0409c25f84137ab446b90ac`;
- root directory `/`;
- Railpack;
- one replica;
- serverless/sleep disabled;
- restart on failure;
- NO public domain;
- NO generated public TCP;
- NO HTTP listener;
- NO health-check path;
- NO pre-deploy migration command.

The database schema is already at `20260917_0020`.

## B0 — preflight

Require:

```text
local HEAD == baed7ea3360f6c67c0409c25f84137ab446b90ac
origin/main == baed7ea3360f6c67c0409c25f84137ab446b90ac
index == empty
```

Do not require a globally clean worktree.

Existing untracked Browser governance and generated cache are non-blocking and must not be staged.

Read-only Railway inventory must prove:

```text
project == AISCC
environment == production

aiscc-public-live-postgres
service id == 5238e804-eb7f-4645-b2a8-e134056be72c
deployment == c21d2f5e-a5c2-4f11-850a-6b99f9d270d7
status == SUCCESS
private network == ready
public TCP == absent
public domain == absent
```

Verify hosted Alembic head remains:

`20260917_0020`

If any canonical identity differs:

`HOSTED_PHASE_B_PRECONDITION_MISMATCH`

and STOP before mutation.

## B1 — role-specific credential bootstrap

The Phase A migrations created these exact login/capability pairs:

```text
aiscc_live_initializer_login
→ SET ROLE aiscc_public_live_initializer

aiscc_live_worker_login
→ SET ROLE aiscc_public_live_execution
```

The login roles must NOT use the PostgreSQL owner/admin password at runtime.

Generate two independent high-entropy runtime passwords.

Requirements:

- at least 32 random bytes before encoding;
- one password only for `aiscc_live_initializer_login`;
- one password only for `aiscc_live_worker_login`;
- never print either value;
- never write either value into Task/Cycle/report/export/log evidence;
- do not place either in project-shared variables;
- do not place either on `aiscc-public-live-postgres` as a reusable application secret;
- do not reuse the existing trusted database credential;
- do not reuse one password for both roles.

Using a temporary private admin session to `aiscc-public-live-postgres`, set only the passwords for these two already-existing login roles.

No role membership, privilege, role attribute, schema, table, function, or migration change is authorized.

If the Executor cannot set the two passwords and service variables without exposing raw values in durable evidence:

`ROLE_CREDENTIAL_SECRET_HANDLING_CONFLICT`

and STOP.

Destroy any temporary local secret material immediately after the target service variables are confirmed.

If a temporary bootstrap service or Railway SSH key is required:

- it must have no public domain;
- it must be deleted before terminal acceptance;
- its admin credential/reference must not remain on either runtime service.

## B2 — deploy private initializer

Create service:

`aiscc-public-live-initializer`

Final start command:

`uv run aiscc public-live-initializer`

Exact application credential variable:

`AISCC_PUBLIC_LIVE_START_DATABASE_URL`

Its value must be a service-local secret DSN using:

- scheme `postgresql+asyncpg`;
- user `aiscc_live_initializer_login`;
- the role-specific password from B1;
- the private hostname of `aiscc-public-live-postgres`;
- the correct private PostgreSQL port/database.

Variable NAMES that must be absent from initializer:

```text
AISCC_DATABASE_URL
AISCC_PUBLIC_LIVE_DATABASE_URL
AISCC_OPENAI_API_KEY
OPENAI_API_KEY
```

Also require no Cloudflare/provider/HMAC secret names.

The initializer must have no public domain and no public port.

## B3 — deploy private worker WITHOUT provider key

Create service:

`aiscc-public-live-worker`

Final start command:

`uv run aiscc public-live-worker`

Exact application credential variable:

`AISCC_PUBLIC_LIVE_DATABASE_URL`

Its value must be a service-local secret DSN using:

- scheme `postgresql+asyncpg`;
- user `aiscc_live_worker_login`;
- the separate worker password from B1;
- the private hostname of `aiscc-public-live-postgres`;
- the correct private PostgreSQL port/database.

Variable NAMES that must be absent from worker in THIS phase:

```text
AISCC_DATABASE_URL
AISCC_PUBLIC_LIVE_START_DATABASE_URL
AISCC_OPENAI_API_KEY
OPENAI_API_KEY
```

The absence of the OpenAI key is intentional.

Do NOT copy or move the existing key from `aiscc-public-live-api`.

The worker must have no public domain and no public port.

## B4 — source/deployment identity

For both new services prove the active successful deployment is built from:

`baed7ea3360f6c67c0409c25f84137ab446b90ac`

If either service cannot be proven to use that commit:

`HOSTED_PRIVATE_RUNTIME_SOURCE_IDENTITY_UNPROVEN`

and STOP.

Do not accept branch-name-only evidence.

## B5 — actual initializer runtime identity proof

From the deployed initializer service environment, run a one-shot read-only identity proof using the canonical application code.

It must instantiate `create_initializer()` and successfully execute:

`repository.verify_runtime_identity()`

The positive result means exact DB identity:

```text
session_user = aiscc_live_initializer_login
current_user = aiscc_public_live_initializer
```

Evidence should record only the role names and PASS result, never the DSN/password.

Also prove from the same effective role:

- it does NOT have worker claim authority;
- it does NOT have broad raw DML authority outside its accepted start/P1 shape;
- it has no provider secret in environment.

If runtime identity fails:

`HOSTED_INITIALIZER_ROLE_IDENTITY_FAILED`

and STOP.

## B6 — actual worker runtime identity proof

From the deployed worker service environment, run a one-shot read-only identity proof using canonical application code.

It must instantiate `create_worker()` and successfully execute:

`authority.repository.verify_runtime_identity()`

The positive result means exact DB identity:

```text
session_user = aiscc_live_worker_login
current_user = aiscc_public_live_execution
```

Also prove from the same effective role:

- it does NOT have initializer start authority;
- it does NOT have owner/trusted DB authority;
- it has no OpenAI key in environment in this phase.

If runtime identity fails:

`HOSTED_WORKER_ROLE_IDENTITY_FAILED`

and STOP.

## B7 — foreground runtime proof

After B5/B6, run both services with their final long-lived start commands.

Require:

```text
initializer:
RUNNING / stable

worker:
RUNNING / stable
```

Observe for a bounded minimum window sufficient to cover at least:

- initializer empty polling/backoff;
- worker registration + empty polling/recovery cycle.

Minimum observation window:

`15 seconds`

During the window prove:

- no crash loop;
- no HTTP/public listener requirement;
- no start request was processed;
- no worker claim was acquired;
- no dispatch pin was created;
- no provider operation was created;
- no private provider protocol state was created;
- OpenAI calls = 0.

A fresh database with no admitted Public Live requests is expected to remain idle.

If any provider-side effect occurs:

`UNEXPECTED_PRIVATE_RUNTIME_SIDE_EFFECT`

and STOP.

## B8 — role/password residue proof

After both services are stable, verify safely:

- `aiscc_live_initializer_login` remains LOGIN / NOINHERIT / non-superuser / no CREATEDB / no CREATEROLE / no BYPASSRLS;
- `aiscc_live_worker_login` same constraints;
- capability roles remain NOLOGIN;
- each service owns only its exact service-local DB variable;
- the two runtime passwords are not equal, if this can be verified without exposing them;
- no admin/root DB credential exists on either service;
- no temporary bootstrap service remains;
- no temporary SSH key remains;
- no temporary admin variable remains.

Do not persist password hashes or raw password values in evidence.

## B9 — existing resource non-mutation

This Task MUST NOT mutate:

- `aiscc-public-live-api`;
- existing owner/trusted `Postgres`;
- `aiscc-public-live-postgres` schema/grants except the two login-role PASSWORD values;
- Cloudflare;
- Git/source.

Do not rename or remove the existing app public domain.

Do not move/remove its existing sealed OpenAI key.

## no provider action

```text
real OpenAI call:
0

worker OpenAI key:
ABSENT

Public ingress:
NOT_DEPLOYED

Public admission:
DISABLED

Public Live:
NOT_RELEASED
```

## no source/Git mutation

Do not edit source, migrations, tests, repository configuration, `.gitattributes`, or Git config.

Do not stage, commit, or push.

Do not run repository tests, Ruff, formatter, or mypy.

This Task owns hosted runtime composition evidence only.

## secret evidence rules

Evidence MAY include:

- service IDs;
- deployment IDs;
- commit IDs;
- region;
- variable NAMES;
- role names;
- privilege booleans;
- runtime/deployment status;
- zero-side-effect counts.

Evidence MUST NOT include:

- runtime passwords;
- raw DB URLs;
- password hashes;
- Railway auth token;
- OpenAI key;
- secret values.

## expected result

Preferred:

`RAILWAY_PRIVATE_INITIALIZER_WORKER_READY / HOSTED_PHASE_B_ACCEPTED_CANDIDATE`

Possible blockers:

- `HOSTED_PHASE_B_PRECONDITION_MISMATCH`
- `ROLE_CREDENTIAL_SECRET_HANDLING_CONFLICT`
- `HOSTED_PRIVATE_RUNTIME_SOURCE_IDENTITY_UNPROVEN`
- `HOSTED_INITIALIZER_ROLE_IDENTITY_FAILED`
- `HOSTED_WORKER_ROLE_IDENTITY_FAILED`
- `UNEXPECTED_PRIVATE_RUNTIME_SIDE_EFFECT`
- `PRIVATE_RUNTIME_RESIDUE_CONFLICT`

No result closes L5 or releases Public Live.

## export

Create one target ZIP containing:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `RAILWAY_BEFORE_INVENTORY.md`
- `ROLE_CREDENTIAL_BOOTSTRAP_PROOF.md`
- `INITIALIZER_DEPLOYMENT_PROOF.md`
- `WORKER_DEPLOYMENT_PROOF.md`
- `RUNTIME_ROLE_IDENTITY_PROOF.md`
- `PRIVATE_RUNTIME_IDLE_PROOF.md`
- `SECRET_NON_EXPOSURE_PROOF.md`
- `RAILWAY_AFTER_INVENTORY.md`
- `WORKSPACE_BEFORE.txt`
- `WORKSPACE_AFTER.txt`

Do not export secrets.

## final response

Report:

1. result
2. canonical local/origin commit
3. Phase A Live PostgreSQL identity/head
4. before Railway inventory
5. initializer service/deployment identity
6. initializer source commit
7. initializer variable-name allowlist/denylist
8. initializer DB session/current role proof
9. worker service/deployment identity
10. worker source commit
11. worker variable-name allowlist/denylist
12. worker DB session/current role proof
13. cross-role deny proof
14. 15s+ foreground stability proof
15. start requests processed = 0
16. worker claims acquired = 0
17. dispatch pins/provider operations/protocol state = 0
18. OpenAI key on worker = absent
19. OpenAI calls = 0
20. temporary bootstrap/SSH/admin residue = absent
21. existing resources mutated = false except exact two login-role PASSWORD values
22. source/Git mutation = 0
23. tests run = false
24. Cloudflare actions = 0
25. Public ingress = NOT_DEPLOYED
26. Public admission = DISABLED
27. Public Live = NOT_RELEASED
28. result ZIP SHA-256
