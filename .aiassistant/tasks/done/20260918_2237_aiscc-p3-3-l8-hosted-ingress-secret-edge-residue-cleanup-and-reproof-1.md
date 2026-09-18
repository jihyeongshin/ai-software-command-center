# 작업지시서: P3-3 L8 hosted ingress provider-secret / edge-trust residue cleanup and no-send reproof

## meta

- task_id: `20260918_2237_aiscc-p3-3-l8-hosted-ingress-secret-edge-residue-cleanup-and-reproof-1`
- created_at: `2026-09-18T22:37:00+09:00`
- work_type: `REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P3-3 / L8 hosted Public Live security configuration`
- exact_baseline: `232f0b7b9ad3d08ead3382e7cbebd527d17811c4`
- fresh_ide_chat_required: `No`
- public_release_authority: `NONE`
- public_run_authority: `NONE`
- provider_call_authority: `NONE`
- hosted_DB_mutation_authority: `NONE`
- Cloudflare_mutation_authority: `NONE`

## 현재 상태

Browser accepted:

- Public fixed Stockroom implementation;
- Owner Docker non-regression;
- affected local L6 reproof;
- existing private worker Docker-free startup/registration.

Public Live remains fail-closed:

```text
Public admission:
DISABLED

Public Live:
NOT_RELEASED

ingress public domains:
0

worker public domains:
0

real provider calls during 2134:
0
```

Hosted reproof found an exact configuration residue:

```text
aiscc-public-live-ingress:
AISCC_OPENAI_API_KEY = PRESENT / VALUE NOT READ
AISCC_PUBLIC_LIVE_RAILWAY_EDGE_TRUST = PRESENT / VALUE NOT READ
```

The required pre-release invariant is worker-only provider secret and no edge trust while ingress remains private.

## provenance correction

Do not use the non-canonical SHA recorded in the previous target report.

Authoritative GitHub lineage:

```text
actual source commit:
15551972c0f402fd3e6076f01335007ec2a6f663

current main / Task baseline:
232f0b7b9ad3d08ead3382e7cbebd527d17811c4
```

## 이번 턴 목표

1. Verify exact fail-closed hosted state before mutation.
2. Determine the **scope/provenance** of the two ingress variable bindings without exposing values.
3. Remove only the effective ingress binding for:
   - `AISCC_OPENAI_API_KEY`
   - `AISCC_PUBLIC_LIVE_RAILWAY_EDGE_TRUST`
4. Redeploy/restart only as naturally required by those exact configuration removals.
5. Prove provider-secret isolation is worker-only.
6. Repeat the affected hosted L5 no-send assertions.
7. Persist governance/provenance and produce target export.

## 절대 유지할 invariant

Successful terminal state:

```text
aiscc-public-live-worker:
AISCC_OPENAI_API_KEY PRESENT / SEALED

aiscc-public-live-ingress:
AISCC_OPENAI_API_KEY ABSENT
OPENAI_API_KEY ABSENT
AISCC_PUBLIC_LIVE_RAILWAY_EDGE_TRUST ABSENT

aiscc-public-live-initializer:
provider key ABSENT

aiscc-public-live-api:
provider key ABSENT

ingress public domains:
0

worker public domains:
0

public_control.enabled:
false

new public runs:
0

claimable work:
0

unreleased claims:
0

dispatch pins:
0

execution operations caused by this Task:
0

provider requests caused by this Task:
0

real OpenAI calls:
0
```

The retained 1919 failed run/campaign/reservation/slot evidence must remain untouched.

## variable provenance rule

Before deleting a variable, establish whether the effective value is:

- exact service-local ingress binding;
- Railway reference/inherited binding;
- shared/project/environment-scoped binding.

### allowed

If the binding can be removed from ingress **without changing the worker's provider-secret binding or any other service**, remove it.

### mandatory stop

If removing the ingress provider key would require deleting/changing a shared/project/environment variable used by the worker, STOP with:

`INGRESS_PROVIDER_SECRET_INHERITANCE_REQUIRES_SEPARATE_DECISION`

Do not rotate, reveal, copy or recreate the secret.

Apply the same scope discipline to edge trust. Do not delete a broader shared value merely to satisfy ingress if its ownership is ambiguous.

## Railway allowed mutation

Only existing service:

`aiscc-public-live-ingress`

Authorized configuration removals:

- ingress effective `AISCC_OPENAI_API_KEY`;
- ingress effective `AISCC_PUBLIC_LIVE_RAILWAY_EDGE_TRUST`.

No value may be printed.

A resulting ingress redeploy/restart is allowed.

No new domain, service, database, volume, environment, secret or paid resource.

## Railway forbidden mutation

- worker provider key removal/rotation;
- initializer/API provider-key creation;
- `AISCC_PUBLIC_LIVE_SOURCE_HMAC_KEY` change;
- Live DB credential change;
- DB role/grant change;
- public domain creation;
- edge-trust addition;
- admission/control enablement;
- campaign/run/reservation/slot mutation;
- worker manual execution/redeploy unless an existing passive Git integration triggers it;
- new Railway resource.

## preflight evidence

Before mutation verify presence/status only:

- exact project/environment/service identity;
- ingress domain count = 0;
- worker domain count = 0;
- `public_control.enabled=false`;
- claimable work = 0;
- unreleased claims = 0;
- dispatch pins = 0;
- execution operations current count;
- provider requests current count;
- active future-deadline runs = 0;
- retained 1919 work still non-claimable;
- worker key present/sealed;
- ingress provider key present;
- ingress edge trust present;
- initializer/API provider keys absent if currently true.

If any work can be dispatched/provider-sent, STOP before mutation.

## cleanup ordering

Preferred:

1. capture preflight counts/presence;
2. remove ingress provider-secret binding;
3. remove ingress edge-trust binding;
4. allow at most the normal configuration-triggered ingress deployment/restart;
5. wait for terminal deployment health;
6. verify ingress still has public domain count 0;
7. verify effective variables after deploy;
8. repeat DB no-send counters;
9. verify worker provider key remains present/sealed.

If the platform applies both removals in one safe bounded change, prefer one deployment over repeated deploy loops.

## affected hosted L5 reproof

Required PASS evidence:

### secret isolation

```text
worker:
provider secret present

ingress:
provider secret absent

initializer:
provider secret absent

owner API:
provider secret absent
```

Also verify standard `OPENAI_API_KEY` is absent on app services unless an already accepted unrelated owner explicitly requires it; any unexpected presence => STOP and report.

### edge trust

```text
ingress:
AISCC_PUBLIC_LIVE_RAILWAY_EDGE_TRUST absent
public domains = 0
```

No spoof/public HTTP matrix is required because ingress remains private.

### fixed-tool worker state

Reuse changed-path source evidence from accepted 2134 implementation.

Fresh hosted proof only needs to verify:

- worker remains healthy/registered;
- no Docker prerequisite is reintroduced;
- no claim/dispatch/operation/provider request occurred;
- no new public run occurred.

Do not redeploy worker just to refresh evidence.

### fail-closed state

Verify:

- control disabled;
- no public ingress;
- Replay unchanged;
- no provider usage caused by this Task.

## 1919 failed smoke

Do NOT reconcile or settle it in this Task.

Read-only prove it remains retained and non-claimable.

The next separate Task may authorize:

`ReconciliationService.close(..., target="FAILED_NOT_DISPATCHED")`

only after Browser accepts this hosted configuration cleanup.

## Git / passive deployment caveat

The previous authorized Git push triggered pre-existing Railway Git integrations for existing ingress/API services.

This Task may commit/push only governance/task-lifecycle artifacts after hosted proof.

If that ordinary push passively triggers existing Railway deployments:

- do not treat the passive trigger as a new manual authorization;
- record exact affected existing services/deployment IDs;
- do not expand scope;
- re-run the final presence/domain/control/no-send checks after those deployments.

If a passive deployment changes the required invariant, STOP and report.

No product source change is expected.

## tests/checks

No broad source test suite is required because this Task is hosted configuration/provenance rework.

Required:

- `git diff --check` for governance files;
- exact changed-path inventory;
- target export hash/integrity;
- secret scan without printing values;
- read-only hosted state comparison before/after.

## stop boundary

STOP if:

- variable scope is ambiguous/shared and deletion can affect worker or other services;
- provider key value would need to be read/exported;
- control is unexpectedly enabled;
- ingress unexpectedly has a public domain;
- claimable work or new provider work appears;
- failed 1919 evidence would need mutation;
- cleanup requires a new Railway resource or DB change;
- any real provider call is required.

## acceptance target

Success:

```text
HOSTED_INGRESS_SECURITY_RESIDUE_CLEANED
/
AFFECTED_L5_HOSTED_REPROOF_CANDIDATE
/
BROWSER_REVIEW_REQUIRED
```

Blocked shared/inherited variable:

```text
INGRESS_PROVIDER_SECRET_INHERITANCE_REQUIRES_SEPARATE_DECISION
```

No result means Public Live is released.

## canonical persistence

Persist supplied:
- Cycle;
- Judgment;
- Handoff;
- this Task active -> done.

Update current state/decision/next action to truthful post-cleanup candidate state.

Ordinary commit/push is authorized for exact governance/task-lifecycle files only after hosted proof.

No amend/rebase/force-push.

## target export

Create:

`.aiassistant/reports/target/20260918_2237_aiscc-p3-3-l8-hosted-ingress-secret-edge-residue-cleanup-and-reproof-1/`

Required root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `HOSTED_CONFIG_BEFORE.md`
- `VARIABLE_PROVENANCE.md`
- `HOSTED_CONFIG_AFTER.md`
- `AFFECTED_L5_HOSTED_REPROOF.md`
- `FAILED_1919_READ_ONLY_STATE.md`
- `FINAL_SAFE_STATE.md`
- `WORKSPACE_STATE.md`
- changed governance files preserving repository-relative paths

Also create adjacent ZIP and verify SHA-256.

Never export:
- raw/masked provider key;
- Railway variable value;
- DB DSN/password;
- HMAC key;
- read capability;
- raw provider output.
