# 작업지시서: P3-3 L5 Railway Live PostgreSQL Foundation

## meta

- task_id: `20260917_1524_aiscc-p3-3-public-live-l5-railway-live-postgres-foundation-1`
- created_at: `2026-09-17 KST`
- work_type: `HOSTED_INFRASTRUCTURE`
- evidence_profile: `HIGH_RISK_NARROW_HOSTED`
- canonical_commit: `dc73fe8c7cbdaee176124dfd71f3ac9d76e8eeb6`
- canonical_parent: `96a4029ec3a82c9b2a88b9718732aa0f00ecad20`
- accepted_local_result: `PUBLIC_LIVE_LOCAL_IMPLEMENTATION / ACCEPTED`
- public_release_effect: `NONE`

Use the current IDE Executor conversation.

This is the first hosted phase after local implementation persistence.

## fixed accepted topology

Do not redesign the accepted L5 topology.

This phase owns only the separate Public Live PostgreSQL foundation.

Later phases own:

- private initializer;
- private worker;
- public ingress;
- trusted API privatization/rename;
- worker OpenAI secret placement;
- hosted provider/sandbox proof;
- paid canary;
- Public release.

## A0 — local/remote preflight

Require:

```text
local HEAD == dc73fe8c7cbdaee176124dfd71f3ac9d76e8eeb6
origin/main == dc73fe8c7cbdaee176124dfd71f3ac9d76e8eeb6
index == empty
```

Do not require globally clean worktree.

The prior persistence result retained two unstaged tracked paths:

```text
src/aiscc/public_live/luna_profile.py
src/aiscc/public_live/provider_authority.py
```

Before any Railway mutation, reconcile these two exact paths read-only.

For each path:

1. read committed bytes with `git show HEAD:<path>`;
2. read current worktree bytes;
3. compare exact bytes;
4. if different, compare after CRLF/LF normalization only;
5. if still different, compare parsed Python AST and ordered string-literal values.

Classification:

- exact or line-ending-only difference → `NON_SEMANTIC_DIRTY_RESIDUE`, continue;
- AST + string-literal identical formatter-only difference → `NON_SEMANTIC_DIRTY_RESIDUE`, continue;
- any AST or string-value semantic difference → `LOAD_BEARING_DIRTY_SOURCE_CONFLICT`, STOP before Railway mutation.

Do NOT reset, checkout, format, stage, or edit either path.

Record this proof because both files are load-bearing Public Live owners.

## A1 — Railway current-state inventory before mutation

Use Railway CLI/API available to the Executor.

Read-only first.

Verify exact project/environment:

```text
project:
AISCC

environment:
production
```

Record only safe metadata:

- project/environment identity;
- services and databases by name;
- region;
- public/private networking state;
- source repository/ref/commit where visible;
- deploy status;
- variable NAMES only, never values;
- domain presence/absence;
- current existing service identity.

Expected pre-existing hosted resources include the current owner/trusted application service and an existing PostgreSQL resource.

Do not rename, delete, restart, redeploy, or mutate pre-existing services in this phase.

If Railway authentication is unavailable:

`RAILWAY_AUTH_REQUIRED`

and STOP.

If the active project/environment is not exact:

`RAILWAY_PROJECT_CONTEXT_MISMATCH`

and STOP.

## A2 — create separate Public Live PostgreSQL

Create exactly one new PostgreSQL resource/service named:

`aiscc-public-live-postgres`

Requirements:

- environment: `production`;
- region: Singapore / Railway `asia-southeast1-eqsg3a` when Railway exposes that exact region identifier;
- dedicated persistent volume;
- private Railway networking only;
- no generated public TCP/database endpoint;
- no public domain;
- not shared with the existing owner/trusted database;
- no OpenAI secret;
- no project-shared application secret.

If a Railway template would necessarily expose public TCP and it cannot be disabled before use:

`RAILWAY_PRIVATE_POSTGRES_CONFLICT`

and STOP rather than accepting a public database.

Record provider image/version and actual region as observed facts.

Do not assert PostgreSQL 17.6 unless the hosted resource actually reports it.

## A3 — ephemeral private migration operator

The accepted schema head is:

`20260917_0020`

Migrations must execute inside Railway private networking without temporarily enabling Public PostgreSQL access.

Create one temporary private migration service only if required, named:

`aiscc-public-live-migrator`

Constraints:

- source repository: canonical AISCC repository;
- source commit/ref must resolve to `dc73fe8c7cbdaee176124dfd71f3ac9d76e8eeb6`;
- no public domain;
- Singapore;
- serverless/off behavior may follow Railway constraints because this service is temporary;
- database admin connection is service-local/private only;
- no `AISCC_OPENAI_API_KEY`;
- no Cloudflare variables;
- no Public Live source HMAC key;
- no provider egress requirement;
- no project-shared admin database secret.

Run exactly:

`uv run alembic upgrade head`

against `aiscc-public-live-postgres`.

Do not run application server or Public worker/initializer.

If the migration service cannot be pinned/proven to the canonical commit, STOP:

`HOSTED_MIGRATOR_SOURCE_IDENTITY_UNPROVEN`

## A4 — migration and role proof

After migration, verify from inside the same private Railway network:

```text
Alembic current:
20260917_0020
```

Verify the accepted capability/login-role structure at minimum:

```text
aiscc_public_live_execution:
exists / NOLOGIN

aiscc_live_worker_login:
exists / LOGIN / NOINHERIT

aiscc_public_live_initializer:
exists / NOLOGIN / NOINHERIT

aiscc_live_initializer_login:
exists / LOGIN / NOINHERIT
```

Also verify the pre-existing Public Live ingress/runtime capability role required by migrations through 0017 exists.

Do not guess its login-role name if the schema does not define one in the current migration history; report exact observed role names instead.

Verify:

- 0018 execution-integration objects exist;
- 0019 durable-worker claim/fence objects exist;
- 0020 start-authority objects exist;
- `public_live_api` mediated functions for worker/start authority exist;
- no role is superuser;
- runtime roles do not have CREATEDB/CREATEROLE/BYPASSRLS;
- initializer/worker capability roles remain NOLOGIN;
- raw Public Live tables are not granted as broad unrestricted runtime mutation authority.

Do not print password hashes, connection URLs, credentials, or secret values.

## A5 — migration operator cleanup

After A4 passes:

- remove/delete `aiscc-public-live-migrator`;
- ensure no migration/admin database URL remains in any application service;
- ensure no public domain was created for the migrator;
- ensure the new Public Live PostgreSQL remains private and online.

If Railway requires retaining a migration service for later operations, do NOT silently keep an admin credential-bearing long-lived service.

STOP:

`MIGRATION_OPERATOR_LIFETIME_CONFLICT`

and report the platform constraint for Browser judgment.

## A6 — existing services remain untouched

This phase MUST NOT:

- rename `aiscc-public-live-api`;
- remove its current public domain;
- remove/move its current OpenAI key;
- deploy `aiscc-public-live-ingress`;
- deploy `aiscc-public-live-initializer`;
- deploy `aiscc-public-live-worker`;
- modify Cloudflare;
- invoke OpenAI;
- enable Public admission;
- release Public Live.

Existing service automatic deployment already caused by the accepted main push is not a new mutation by this Task; record observed status only.

## no source/Git mutation

Do not modify source or governance files other than the current Task done/export artifacts.

Do not commit or push.

Do not run repository test suites.

This phase is Railway resource/configuration proof only.

## secret evidence rules

Evidence may include:

- variable names;
- service names;
- role names;
- region;
- deploy IDs;
- commit IDs;
- safe grant/role booleans;
- redacted host topology.

Evidence MUST NOT include:

- database passwords;
- raw URLs containing credentials;
- OpenAI key;
- Railway tokens;
- secret variable values.

## expected result

Preferred:

`RAILWAY_LIVE_POSTGRES_FOUNDATION_READY / HOSTED_PHASE_A_ACCEPTED_CANDIDATE`

Possible blockers:

- `LOAD_BEARING_DIRTY_SOURCE_CONFLICT`
- `RAILWAY_AUTH_REQUIRED`
- `RAILWAY_PROJECT_CONTEXT_MISMATCH`
- `RAILWAY_PRIVATE_POSTGRES_CONFLICT`
- `HOSTED_MIGRATOR_SOURCE_IDENTITY_UNPROVEN`
- `MIGRATION_ROLE_PROOF_FAILED`
- `MIGRATION_OPERATOR_LIFETIME_CONFLICT`

None closes L5 and none enables Public Live.

## export

Create one target ZIP containing:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `LOAD_BEARING_DIRTY_RECONCILIATION.md`
- `RAILWAY_BEFORE_INVENTORY.md`
- `LIVE_POSTGRES_PROVISIONING_PROOF.md`
- `MIGRATION_EXECUTION_PROOF.md`
- `DATABASE_ROLE_GRANT_PROOF.md`
- `MIGRATION_OPERATOR_CLEANUP_PROOF.md`
- `SECRET_NON_EXPOSURE_PROOF.md`
- `RAILWAY_AFTER_INVENTORY.md`
- `WORKSPACE_BEFORE.txt`
- `WORKSPACE_AFTER.txt`

Do not export secrets.

## final response

Report:

1. result
2. canonical commit/local+remote identity
3. load-bearing dirty reconciliation
4. Railway project/environment
5. before resource inventory
6. new Live PostgreSQL service identity
7. hosted PostgreSQL version
8. region
9. private networking proof
10. public TCP/domain = absent
11. migrator source commit
12. migration result/head
13. worker role proof
14. initializer role proof
15. ingress/runtime capability-role observation
16. 0018/0019/0020 object proof
17. migrator cleanup
18. admin credential residue = absent
19. pre-existing services mutated = false
20. OpenAI calls = 0
21. Cloudflare actions = 0
22. Public admission = DISABLED
23. Public Live = NOT_RELEASED
24. source/Git mutations = 0
25. result ZIP SHA-256
