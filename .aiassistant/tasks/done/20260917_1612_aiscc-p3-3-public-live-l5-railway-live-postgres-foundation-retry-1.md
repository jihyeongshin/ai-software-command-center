# 작업지시서: P3-3 L5 Railway Live PostgreSQL Foundation Retry

## meta

- task_id: `20260917_1612_aiscc-p3-3-public-live-l5-railway-live-postgres-foundation-retry-1`
- created_at: `2026-09-17 KST`
- work_type: `HOSTED_INFRASTRUCTURE`
- evidence_profile: `HIGH_RISK_NARROW_HOSTED`
- canonical_commit: `baed7ea3360f6c67c0409c25f84137ab446b90ac`
- canonical_parent: `dc73fe8c7cbdaee176124dfd71f3ac9d76e8eeb6`
- predecessor_repair_result_zip_sha256: `a4996d9ee699d3160a78251c346a0a45cc7014fde5917c493059297bb6486f6c`
- public_release_effect: `NONE`

Use the current IDE Executor conversation.

This Task resumes the Railway Phase A that previously stopped before any Railway access.

The source-inventory omission is now closed. Do not reopen the two-file source recovery.

## fixed accepted topology

This phase owns ONLY:

`separate Public Live PostgreSQL + migration/role foundation`

Later phases own:

- private initializer deployment;
- private worker deployment;
- public ingress deployment;
- existing trusted API rename/privatization;
- worker-only OpenAI secret placement;
- hosted provider/sandbox proof;
- paid canary;
- Public release.

Do not collapse these phases.

## A0 — repository preflight

Require:

```text
HEAD == baed7ea3360f6c67c0409c25f84137ab446b90ac
origin/main == baed7ea3360f6c67c0409c25f84137ab446b90ac
index == empty
```

Do not require a globally clean worktree.

Generated `__pycache__`, `.pyc`, target exports, and other ignored/untracked local residue are NON_BLOCKING and must not be staged.

Verify these canonical committed blobs exist:

```text
src/aiscc/public_live/luna_profile.py
Git canonical SHA-256:
bb90ad7337045e5cea3006b52a39e04ce28f16b1fbdf47b26c6db7210b9199a4

src/aiscc/public_live/provider_authority.py
Git canonical SHA-256:
b3a8373c5ea1bbdb61efe999643aef0412687a2171849d1dc1fc48982cbaf851
```

If repository identity differs:

`HOSTED_PHASE_A_SOURCE_IDENTITY_MISMATCH`

and STOP before Railway mutation.

## A1 — Railway read-only current-state inventory

Authenticate using the existing authorized Railway CLI/session.

Do not request or print a Railway token.

Before mutation verify exact context:

```text
project:
AISCC

environment:
production
```

Record safe metadata only:

- project/environment identity;
- service/resource names;
- service types;
- region;
- deployment state;
- public-domain presence/absence;
- public TCP/database exposure presence/absence;
- source repository/ref/commit when visible;
- variable NAMES only, never values.

Expected existing resources may include:

- the current application service historically named `aiscc-public-live-api`;
- the existing owner/trusted PostgreSQL resource.

Do not rename, restart, redeploy, delete, or reconfigure any existing resource in this phase.

If Railway authentication is unavailable:

`RAILWAY_AUTH_REQUIRED`

and STOP.

If the active project/environment is not exact:

`RAILWAY_PROJECT_CONTEXT_MISMATCH`

and STOP.

## A2 — create separate Public Live PostgreSQL

Create exactly one new PostgreSQL resource/service with canonical name:

`aiscc-public-live-postgres`

Requirements:

- Railway project `AISCC`;
- environment `production`;
- Singapore region, using Railway's current Singapore region identifier when exposed;
- dedicated persistent storage/volume;
- private Railway networking only;
- no public database TCP endpoint;
- no public domain;
- not shared with the existing owner/trusted PostgreSQL;
- no OpenAI secret;
- no application provider secret.

If Railway initially generates public database networking by default, remove/disable it before any application use or migration evidence is admitted.

If public TCP cannot be disabled:

`RAILWAY_PRIVATE_POSTGRES_CONFLICT`

and STOP.

Record observed PostgreSQL image/version after startup. Do not assume a version from local tests.

## A3 — temporary private migration operator

Migrations must run INSIDE Railway private networking.

Create a temporary service only if required, named:

`aiscc-public-live-migrator`

Constraints:

- source repository: canonical AISCC repository;
- source ref/commit must resolve to `baed7ea3360f6c67c0409c25f84137ab446b90ac`;
- no public domain;
- Singapore;
- no `AISCC_OPENAI_API_KEY`;
- no Cloudflare secret/config;
- no Public Live HMAC/provider secret;
- private DB admin connection only;
- no long-lived owner/trusted application DB URL reuse.

Use Railway service references/private variables rather than copying raw credential values when supported.

Do not expose database URLs/passwords in console evidence.

Run exactly:

`uv run alembic upgrade head`

against `aiscc-public-live-postgres`.

Do not start the application server.
Do not start Public ingress, worker, or initializer.

If the migrator cannot be pinned/proven to canonical source:

`HOSTED_MIGRATOR_SOURCE_IDENTITY_UNPROVEN`

and STOP before accepting migration evidence.

## A4 — migration head proof

From a private Railway execution context verify:

```text
Alembic current:
20260917_0020
```

Also verify migration history includes through:

```text
20260916_0018_public_live_execution_integration
20260917_0019_public_live_worker_claims
20260917_0020_public_live_start_authority
```

No historical migration rewrite is allowed.

## A5 — database role / grant / object proof

Verify the accepted role foundation from the hosted database.

At minimum, exact accepted roles:

```text
aiscc_public_live_execution
NOLOGIN

aiscc_live_worker_login
LOGIN
NOINHERIT

aiscc_public_live_initializer
NOLOGIN
NOINHERIT

aiscc_live_initializer_login
LOGIN
NOINHERIT
```

Also enumerate the ingress/runtime capability role(s) created by migrations through 0017 and report exact observed names/attributes.

Do not invent an ingress login role if the migrations do not define one.

Verify:

- no runtime role is superuser;
- no runtime role has CREATEDB;
- no runtime role has CREATEROLE;
- no runtime role has BYPASSRLS;
- worker/initializer capability roles are NOLOGIN;
- 0018 execution integration objects exist;
- 0019 worker claim/fence/pin/event objects exist;
- 0020 start-authority objects exist;
- accepted mediated Public Live DB functions exist;
- runtime roles do not have broad unrestricted raw-table mutation authority.

Evidence should contain role/grant booleans and object names, not credentials.

If required role/object/grant structure is missing:

`MIGRATION_ROLE_PROOF_FAILED`

and STOP.

## A6 — temporary migrator cleanup

After A4/A5 pass:

- delete/remove `aiscc-public-live-migrator`;
- verify it has no remaining deployment/domain;
- verify no temporary admin DB variable remains on application services;
- verify the separate Live PostgreSQL remains online/private;
- verify no public TCP/domain was introduced.

If Railway forces retention of an admin-credential-bearing migration service:

`MIGRATION_OPERATOR_LIFETIME_CONFLICT`

and STOP for Browser judgment rather than silently retaining it.

## A7 — existing resources stay untouched

This Task MUST NOT:

- rename the current existing app service;
- remove/change its public domain;
- move/remove its current OpenAI secret;
- mutate the existing owner/trusted PostgreSQL;
- deploy `aiscc-public-live-ingress`;
- deploy `aiscc-public-live-initializer`;
- deploy `aiscc-public-live-worker`;
- change Cloudflare;
- call OpenAI;
- enable Public admission;
- release Public Live.

Automatic deployment already triggered by earlier `main` pushes is an observed fact only; do not manually redeploy it here.

## no source / Git mutation

Do not modify product source, migration files, tests, or repository config.

Do not stage, commit, or push.

Do not run repository unit/integration/full test suites.

Only Railway infrastructure/migration verification is authorized.

## secret evidence rules

Evidence MAY include:

- service/resource names;
- region;
- PostgreSQL version;
- deployment IDs;
- source commit;
- variable NAMES;
- role names and boolean attributes;
- object/grant names;
- redacted private topology.

Evidence MUST NOT include:

- raw database passwords;
- credential-bearing connection URLs;
- Railway token;
- OpenAI key;
- secret variable values.

If a command prints a secret-bearing URL, redact it before evidence storage.

## expected result

Preferred:

`RAILWAY_LIVE_POSTGRES_FOUNDATION_READY / HOSTED_PHASE_A_ACCEPTED_CANDIDATE`

Possible blockers:

- `HOSTED_PHASE_A_SOURCE_IDENTITY_MISMATCH`
- `RAILWAY_AUTH_REQUIRED`
- `RAILWAY_PROJECT_CONTEXT_MISMATCH`
- `RAILWAY_PRIVATE_POSTGRES_CONFLICT`
- `HOSTED_MIGRATOR_SOURCE_IDENTITY_UNPROVEN`
- `MIGRATION_ROLE_PROOF_FAILED`
- `MIGRATION_OPERATOR_LIFETIME_CONFLICT`

None of these closes L5 or releases Public Live.

## export

Create one target ZIP containing:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `RAILWAY_BEFORE_INVENTORY.md`
- `LIVE_POSTGRES_PROVISIONING_PROOF.md`
- `MIGRATION_EXECUTION_PROOF.md`
- `DATABASE_ROLE_GRANT_PROOF.md`
- `MIGRATION_OPERATOR_CLEANUP_PROOF.md`
- `SECRET_NON_EXPOSURE_PROOF.md`
- `RAILWAY_AFTER_INVENTORY.md`
- `WORKSPACE_BEFORE.txt`
- `WORKSPACE_AFTER.txt`

No secret values.

## final response

Report:

1. result
2. canonical local/origin commit
3. canonical two-file source identity
4. Railway project/environment
5. before inventory
6. new Live PostgreSQL identity
7. hosted PostgreSQL version
8. region
9. private-network proof
10. public TCP/domain = absent
11. migrator source commit
12. migration result/head
13. 0018/0019/0020 presence
14. worker role proof
15. initializer role proof
16. ingress/runtime role observation
17. mediated function/grant proof
18. migrator cleanup
19. temporary admin credential residue = absent
20. existing resources mutated = false
21. source/Git mutation = 0
22. tests run = false
23. OpenAI calls = 0
24. Cloudflare actions = 0
25. Public admission = DISABLED
26. Public Live = NOT_RELEASED
27. result ZIP SHA-256
