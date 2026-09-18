# 작업지시서: P3-3 L8 Railway shared-to-service-local variable migration and hosted L5 reproof

## meta

- task_id: `20260918_2312_aiscc-p3-3-l8-shared-to-service-local-variable-migration-and-hosted-reproof-1`
- created_at: `2026-09-18T23:12:39+09:00`
- work_type: `HOSTED_SECURITY_CONFIGURATION_MIGRATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- exact_baseline: `3832fff7751c387b8e559cc273cf30836238d48d`
- fresh_ide_chat_required: `No`
- public_release_authority: `NONE`
- public_run_authority: `NONE`
- provider_call_authority: `NONE`
- hosted_DB_mutation_authority: `NONE`
- Cloudflare_mutation_authority: `NONE`
- Railway_shared_variable_mutation_authority: `BOUNDED_EXACT`

## Goal

Remove over-broad Railway project/environment variable inheritance while preserving the already accepted worker-local sealed provider credential.

Then repeat only the affected hosted L5 no-send/security assertions.

Do not release Public Live.

## Current proven state

Service-local inventory:

```text
worker:
AISCC_OPENAI_API_KEY PRESENT / SEALED
OPENAI_API_KEY ABSENT
AISCC_PUBLIC_LIVE_RAILWAY_EDGE_TRUST ABSENT

ingress:
all three local bindings ABSENT

initializer:
all three local bindings ABSENT

API:
all three local bindings ABSENT
```

Effective runtime presence:

```text
worker:
AISCC_OPENAI_API_KEY PRESENT
OPENAI_API_KEY PRESENT
AISCC_PUBLIC_LIVE_RAILWAY_EDGE_TRUST PRESENT

ingress:
all three PRESENT

initializer:
all three PRESENT

API:
all three PRESENT
```

No values may be read, printed, copied, hashed, rotated or exported.

## Intended terminal invariant

```text
aiscc-public-live-worker:
AISCC_OPENAI_API_KEY PRESENT / SEALED / SERVICE-LOCAL
OPENAI_API_KEY ABSENT
AISCC_PUBLIC_LIVE_RAILWAY_EDGE_TRUST ABSENT

aiscc-public-live-ingress:
AISCC_OPENAI_API_KEY ABSENT
OPENAI_API_KEY ABSENT
AISCC_PUBLIC_LIVE_RAILWAY_EDGE_TRUST ABSENT

aiscc-public-live-initializer:
AISCC_OPENAI_API_KEY ABSENT
OPENAI_API_KEY ABSENT
AISCC_PUBLIC_LIVE_RAILWAY_EDGE_TRUST ABSENT

aiscc-public-live-api:
AISCC_OPENAI_API_KEY ABSENT
OPENAI_API_KEY ABSENT
AISCC_PUBLIC_LIVE_RAILWAY_EDGE_TRUST ABSENT

ingress public domains:
0

worker public domains:
0

public_control.enabled:
false

claimable work:
0

unreleased claims:
0

dispatch pins:
0

new execution operations:
0

new provider requests:
0

real OpenAI calls:
0
```

## Phase A — exact shared-scope provenance preflight

Before mutation, determine presence/scope metadata only.

For each exact variable:

- `AISCC_OPENAI_API_KEY`
- `OPENAI_API_KEY`
- `AISCC_PUBLIC_LIVE_RAILWAY_EDGE_TRUST`

record:
- Railway project/environment scope owner;
- whether a service-local override exists per app service;
- whether any variable is a reference to another variable;
- affected service set when the shared binding is removed.

Do not read the value.

### Worker preservation proof

Before deleting shared `AISCC_OPENAI_API_KEY`, prove the worker's accepted sealed local binding:

- is service-local;
- is independently present;
- is not merely an alias/reference that would disappear with the shared binding;
- remains the canonical resolver variable expected by `HostedOpenAISecretResolver`.

If this cannot be proven without revealing material:

`WORKER_LOCAL_PROVIDER_BINDING_INDEPENDENCE_UNPROVEN`

and STOP.

## Phase B — source/runtime owner audit

Perform a narrow current-source audit for the three variable names and their configuration owners.

Required decisions:

### AISCC_OPENAI_API_KEY

Accepted owner:
- Public Live worker only.

Ingress explicitly forbids provider material.

Initializer/API must not require it for the Public Live path.

If a different accepted owner is found, STOP.

### OPENAI_API_KEY

No accepted Public Live component should require the standard variable.

If any current accepted service legitimately depends on shared `OPENAI_API_KEY`, STOP with:

`SHARED_STANDARD_OPENAI_KEY_OWNER_CONFLICT`

Do not delete it until Browser reviews that owner.

### AISCC_PUBLIC_LIVE_RAILWAY_EDGE_TRUST

While ingress has no public domain, this must be absent.

No other app service should own it.

If a different accepted owner is found, STOP.

## Phase C — shared variable migration

Only after A/B pass, mutate the exact shared/project/environment bindings.

Preferred order:

1. remove shared `OPENAI_API_KEY`;
2. remove shared `AISCC_PUBLIC_LIVE_RAILWAY_EDGE_TRUST`;
3. verify worker service-local `AISCC_OPENAI_API_KEY` still exists independently;
4. remove shared `AISCC_OPENAI_API_KEY`.

Do not touch the worker-local sealed binding.

Do not create a replacement key.

Do not copy provider material from shared scope to service scope.

The preservation mechanism is the already existing service-local worker binding.

## Natural Railway deployment authority

Shared-variable changes may naturally redeploy/restart existing services.

Authorized existing app services only:

- `aiscc-public-live-worker`
- `aiscc-public-live-ingress`
- `aiscc-public-live-initializer`
- `aiscc-public-live-api`

No new service/resource/database/domain/volume/environment.

Observe exact deployment IDs/status.

If Git governance persistence later passively triggers existing Git-integrated deployments, record them and re-run the terminal invariant afterward.

## Fail-safe conditions before mutation

Require:

- Public control disabled;
- ingress domains 0;
- worker domains 0;
- claimable work 0;
- unreleased claims 0;
- dispatch pins 0;
- active future-deadline runs 0;
- retained 1919 run non-claimable;
- no new provider request in progress.

If not, STOP.

## Post-migration effective presence proof

After all naturally triggered deployments reach terminal healthy state, perform presence-only verification across all four app services.

Required:

```text
worker:
AISCC_OPENAI_API_KEY PRESENT
OPENAI_API_KEY ABSENT
edge trust ABSENT

ingress:
both provider keys ABSENT
edge trust ABSENT

initializer:
both provider keys ABSENT
edge trust ABSENT

API:
both provider keys ABSENT
edge trust ABSENT
```

Never print values.

## affected hosted L5 reproof

After variable isolation succeeds, prove:

### Secret isolation

- worker is the sole provider-secret owner;
- worker key remains sealed/service-local;
- ingress/initializer/API receive no provider keys;
- no raw/masked provider material appears in logs/evidence.

### Edge state

- ingress edge trust absent;
- ingress public domain count 0;
- worker public domain count 0.

### Fixed-tool worker state

- worker deployment healthy;
- startup remains consistent with fixed Stockroom runtime;
- no Docker prerequisite is required;
- no work was claimed/dispatched;
- provider request count did not increase;
- no real OpenAI call occurred.

### Fail-closed

- `public_control.enabled=false`;
- Replay unchanged;
- Public Live NOT_RELEASED;
- no new public run.

Successful evidence becomes:

`AFFECTED_L5_HOSTED_REPROOF_CANDIDATE`.

## retained 1919 failed smoke

Read-only only.

Do not:
- settle;
- reconcile;
- free reservation/slot;
- retry;
- delete;
- rewrite.

Verify it remains non-claimable and definitely-not-sent evidence remains consistent.

Settlement is a separate later Task.

## rollback / unexpected state

If a shared-variable removal unexpectedly causes the worker-local `AISCC_OPENAI_API_KEY` to become absent:

- do not attempt provider execution;
- keep control disabled and domains absent;
- do not reconstruct/copy the secret;
- report `WORKER_PROVIDER_BINDING_LOST_AFTER_SHARED_REMOVAL`;
- Human can restore from the separately held credential source under a later authorized secret-binding Task.

Do not weaken the secret-isolation invariant merely to restore service health.

## no provider call

This Task authorizes zero OpenAI/provider requests.

Worker health/register proof must not consume the key.

## Git / persistence

No product source change is expected.

Persist supplied Cycle/Judgment/Handoff and Task lifecycle.

Update current state/decision/next action truthfully.

Ordinary governance-only commit/push authorized after hosted proof.

No amend/rebase/force-push.

Target export remains ignored/untracked.

## checks

Required:
- `git diff --check`;
- changed-path inventory;
- target ZIP integrity;
- bounded secret scan without values;
- Railway presence/scope before-after evidence;
- deployment IDs/status;
- no-send counters before-after.

No broad source test suite is required unless product source unexpectedly changes; product source change is not authorized.

## stop boundaries

STOP if:
- worker-local binding independence cannot be proven;
- standard shared key has a legitimate accepted owner;
- shared edge-trust has a legitimate accepted owner;
- control is enabled;
- public domain appears;
- claimable/provider work appears;
- provider material must be read/copied;
- a new resource is required;
- DB mutation is required;
- real provider call is required.

## acceptance target

Success:

```text
SHARED_VARIABLE_MIGRATION_COMPLETE
/
AFFECTED_L5_HOSTED_REPROOF_CANDIDATE
/
BROWSER_REVIEW_REQUIRED
```

Blocked owner conflict:

```text
SHARED_VARIABLE_OWNER_CONFLICT
```

Worker binding uncertainty:

```text
WORKER_LOCAL_PROVIDER_BINDING_INDEPENDENCE_UNPROVEN
```

No result means Public Live is released.

## export

Create:

`.aiassistant/reports/target/20260918_2312_aiscc-p3-3-l8-shared-to-service-local-variable-migration-and-hosted-reproof-1/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `SHARED_VARIABLE_PROVENANCE.md`
- `SOURCE_OWNER_AUDIT.md`
- `HOSTED_STATE_BEFORE.md`
- `HOSTED_STATE_AFTER.md`
- `AFFECTED_L5_HOSTED_REPROOF.md`
- `FAILED_1919_READ_ONLY_STATE.md`
- `FINAL_SAFE_STATE.md`
- `WORKSPACE_STATE.md`
- changed governance files preserving repository-relative paths

Create adjacent result ZIP and report SHA-256.

Never export:
- provider key or masked key identifier;
- Railway variable value;
- DB DSN/password;
- HMAC key;
- read capability;
- raw provider output.
