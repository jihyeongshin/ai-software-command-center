# 작업지시서: P3-3 L5 Ingress DB Least-Privilege Boundary Rework

## meta

- task_id: `20260917_2112_aiscc-p3-3-public-live-l5-ingress-db-least-privilege-boundary-rework-1`
- created_at: `2026-09-17 KST`
- work_type: `SECURITY_BOUNDARY_REWORK`
- evidence_profile: `HIGH_RISK_NARROW`
- expected_HEAD: `baed7ea3360f6c67c0409c25f84137ab446b90ac`
- accepted_phase_b_result_zip_sha256: `b3c6a761ac114b84fea5bb59802ea3d7ffee53709cebfbf8c068943d2060be2e`
- public_release_effect: `NONE`

Use the current IDE Executor conversation.

This is a LOCAL source/migration security-boundary correction.

Do NOT access or mutate Railway in this Task.

The already-running Phase B initializer/worker are accepted and out of scope.

## reason

The accepted hosted D6 boundary requires anonymous Public ingress to use a dedicated DB authority containing only
admission/read/limiter privileges.

The existing capability role:

`aiscc_public_live_runtime`

is too broad for ingress because current accepted migrations also grant it provider-pipeline runtime functions.

Do NOT deploy ingress using that role.

## R0 — preflight

Require:

```text
HEAD == baed7ea3360f6c67c0409c25f84137ab446b90ac
origin/main == baed7ea3360f6c67c0409c25f84137ab446b90ac
index == empty
```

Do not require a globally clean worktree.

Ignore untracked governance/export/cache residue.

If HEAD/origin/index differs:

`INGRESS_BOUNDARY_PREFLIGHT_MISMATCH`

and STOP.

## R1 — exact migration shape

Add exactly one new forward migration:

`migrations/versions/20260917_0021_public_live_ingress_authority.py`

Required metadata:

```text
revision = "20260917_0021"
down_revision = "20260917_0020"
```

Do not edit migrations `<= 20260917_0020`.

Create one new capability role:

`aiscc_public_live_ingress`

Required role attributes:

```text
NOLOGIN
NOINHERIT
NOSUPERUSER
NOCREATEDB
NOCREATEROLE
NOBYPASSRLS
```

This is a capability role only.

Do NOT create the deployment LOGIN role in the migration.
`aiscc_live_ingress_login` remains a later Railway deployment binding with a service-local password.

## R2 — exact ingress privilege allowlist

Before writing grants, resolve the exact PostgreSQL function signatures from the canonical migration history and a
local migrated PostgreSQL catalog.

Do not guess a signature.

The new capability role may receive only the minimum schema/function authority required by the current ingress code
and its later production admission binding.

Logical function allowlist:

```text
public_live_api.clock_lock
public_live_api.flood_consume
public_live_api.lock_run
public_live_api.read_consume
public_live_api.read_key
public_live_api.admission_context
public_live_api.admit_checked_and_start
public_live_api.run_context
```

Grant only:

- the schema USAGE required to invoke those routines;
- EXECUTE on the exact resolved overload/signature for each listed routine.

No table/view/sequence DML grant is allowed.

No function outside that logical list may be granted.

In particular ingress MUST NOT have EXECUTE on any function in these authority families:

```text
provider pipeline:
pipeline_enroll
pipeline_context
pipeline_request
pipeline_start
pipeline_outcome
pipeline_validate
pipeline_tool

P1-5 execution:
execution_*

durable worker:
worker_*

initializer/start:
start_*

trusted reconciliation/provider settlement:
reconciler/trusted-only routines
```

The exact deny proof must use catalog-resolved signatures, not name-only assumptions.

## R3 — existing role preservation

Do NOT weaken or repurpose:

```text
aiscc_public_live_runtime
aiscc_public_live_reconciler
aiscc_public_live_execution
aiscc_public_live_initializer
```

No existing grant is removed merely to make the ingress role look narrow.

The new ingress role is additive and separate.

The worker and initializer accepted DB authorities remain unchanged.

## R4 — fail-closed ingress runtime identity

Update the minimum production code needed so hosted `aiscc-public-live-ingress` can fail closed if its database
principal is misbound.

Preferred scope:

```text
src/aiscc/public_live/ingress.py
```

A small supporting method/module is allowed only if necessary.

The future hosted deployment login is exactly:

`aiscc_live_ingress_login`

At ingress lifespan startup, before reporting startup complete, verify through the configured Live DB connection:

```text
session_user == aiscc_live_ingress_login
current_user == aiscc_live_ingress_login
```

and verify:

```text
member/usable capability:
aiscc_public_live_ingress == true

forbidden role membership/use:
aiscc_public_live_runtime == false
aiscc_public_live_reconciler == false
aiscc_public_live_execution == false
aiscc_public_live_initializer == false
```

Also fail closed if the login itself is:

- superuser;
- CREATEDB;
- CREATEROLE;
- BYPASSRLS.

The startup proof must not require an owner/trusted database credential.

Do not add a provider client, owner repository, owner DB variable, fallback role, or automatic privilege repair.

Wrong identity/privilege => startup failure with a safe non-secret reason.

## R5 — repository terminology correction

Where the canonical source currently says anonymous ingress should use membership in
`aiscc_public_live_runtime`, correct that documentation/comment only as necessary to identify the new
`aiscc_public_live_ingress` capability.

Do not rewrite unrelated architecture prose.

## R6 — local PostgreSQL migration proof

Use an isolated local PostgreSQL test runtime.

Prove:

```text
20260917_0020 -> 20260917_0021:
PASS

fresh supported DB -> head:
PASS
```

Then create a temporary test login equivalent to future hosted binding:

```text
aiscc_live_ingress_login
LOGIN
INHERIT
member ONLY of aiscc_public_live_ingress
```

Use a test-only password that never enters committed files/reports.

The login's INHERIT attribute is deliberate because current ingress DB engine does not perform `SET ROLE`.
The inherited authority must still be limited to the single narrow ingress capability role.

## R7 — positive DB authority proof

Using the temporary ingress login, prove the exact allowed routines are executable.

Use safe/read-only or rolled-back invocations where a function would otherwise create state.

For stateful routines, catalog privilege proof plus a transaction that is explicitly rolled back is acceptable when
a valid domain fixture is impractical.

At minimum demonstrate that the login can reach the DB path required by:

- repository transaction clock;
- flood limiter;
- capability-scoped read path;
- admission/idempotency context;
- atomic admit+start path.

Do not fabricate a successful Public release.

## R8 — negative authority proof

Using the same temporary ingress login, prove:

```text
raw INSERT/UPDATE/DELETE on Public Live tables:
DENIED

provider-pipeline runtime functions:
DENIED

execution_*:
DENIED

worker_*:
DENIED

start_*:
DENIED

reconciler/trusted-only provider settlement:
DENIED
```

Also prove it has no membership/use of the four forbidden capability roles from R4.

Any one unexpected positive privilege is:

`INGRESS_DB_AUTHORITY_TOO_BROAD`

and STOP.

## R9 — ingress startup identity tests

Add narrow tests proving:

1. exact future login + exact ingress capability => startup identity PASS;
2. owner/admin DB login => FAIL CLOSED;
3. broad `aiscc_public_live_runtime` login/member => FAIL CLOSED;
4. worker login => FAIL CLOSED;
5. initializer login => FAIL CLOSED;
6. login with extra forbidden capability membership => FAIL CLOSED.

Do not loosen the runtime check to make tests pass.

## R10 — regression boundary

Run only focused tests.

Required:

- new 0021 migration/grant integration tests;
- ingress startup/runtime-identity tests;
- existing Public Live HTTP ingress tests directly affected by `ingress.py`;
- existing migration-head smoke required to prove 0020→0021 and fresh→head.

Do NOT run the full repository test suite.

Reuse prior accepted evidence for unrelated worker/initializer/provider logic.

If a direct failure proves another source owner must change:

`INGRESS_BOUNDARY_SCOPE_EXPANSION_REQUIRED`

and STOP instead of broadening automatically.

## R11 — static verification

Run on changed Python only:

```text
ruff check
ruff format --check
```

Run mypy only on changed production modules plus direct imported owner modules needed for type closure.

Run:

`git diff --check`

No repo-wide formatting or mypy.

## R12 — unchanged hosted boundary

This local Task MUST NOT:

- access Railway;
- alter hosted Postgres;
- restart initializer/worker;
- deploy ingress;
- change Cloudflare;
- read/move the existing OpenAI key;
- call OpenAI;
- enable Public admission;
- release Public Live.

## migration downgrade safety

Downgrade may drop the new ingress capability role only when no login/member dependency prevents safe removal.

Do not CASCADE through deployment principals or unrelated grants.

A downgrade that would destroy unrelated authority must fail closed.

## expected result

Preferred:

`INGRESS_DB_LEAST_PRIVILEGE_BOUNDARY_READY / LOCAL_ACCEPTED_CANDIDATE`

Possible blockers:

- `INGRESS_BOUNDARY_PREFLIGHT_MISMATCH`
- `INGRESS_DB_AUTHORITY_TOO_BROAD`
- `INGRESS_RUNTIME_IDENTITY_FAIL_CLOSED_BROKEN`
- `INGRESS_BOUNDARY_SCOPE_EXPANSION_REQUIRED`

## export

Create one target ZIP containing:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `SOURCE_INVENTORY.json`
- `INGRESS_ROLE_FUNCTION_ALLOWLIST.json`
- `INGRESS_DB_AUTHORITY_PROOF.md`
- `INGRESS_RUNTIME_IDENTITY_PROOF.md`
- `MIGRATION_0021_PROOF.md`
- `TARGETED_TEST_EVIDENCE.json`
- `STATIC_CHECKS.md`
- `WORKSPACE_BEFORE.txt`
- `WORKSPACE_AFTER.txt`
- every changed source/test/migration file at exact project-relative POSIX path.

Do not export DB passwords or DSNs.

## final response

Report:

1. result
2. HEAD/origin
3. changed path count
4. migration 0021 identity
5. exact ingress capability role attributes
6. exact resolved function allowlist
7. raw DML deny proof
8. provider-pipeline deny proof
9. execution/worker/start/reconciler deny proof
10. future ingress login membership shape
11. ingress startup identity positive proof
12. wrong/broad-role startup deny proof
13. 0020→0021 migration proof
14. fresh→head migration proof
15. focused tests + totals
16. Ruff
17. format-check
18. narrow mypy
19. diff-check
20. source mutation summary
21. Railway actions = 0
22. OpenAI calls = 0
23. Cloudflare actions = 0
24. Public ingress = NOT_DEPLOYED
25. Public admission = DISABLED
26. Public Live = NOT_RELEASED
27. result ZIP SHA-256
