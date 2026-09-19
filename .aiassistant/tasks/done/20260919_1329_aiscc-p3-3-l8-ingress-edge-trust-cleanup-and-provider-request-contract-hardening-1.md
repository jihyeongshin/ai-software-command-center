# 작업지시서: P3-3 L8 Ingress Edge-Trust Cleanup + Provider Request Contract Hardening

## meta

- task_id: `20260919_1329_aiscc-p3-3-l8-ingress-edge-trust-cleanup-and-provider-request-contract-hardening-1`
- created_at: `2026-09-19T13:29:38+09:00`
- work_type: `HOSTED_CONFIG_CLEANUP_AND_PROVIDER_REQUEST_COMPATIBILITY_HARDENING`
- evidence_profile: `HIGH_RISK`
- execution_model: `THIN_CC_THICK_EXECUTOR`
- exact_baseline: `f3f8acd5af11c56de2dacba2777aa3e0e9b85cb7`
- fresh_ide_chat_required: `No`
- public_release_authority: `NONE`
- public_run_authority: `NONE`
- provider_call_authority: `NONE`
- provider_retry_resend_authority: `NONE`
- Cloudflare_mutation_authority: `NONE`
- Railway_ingress_config_mutation_authority: `REMOVE_EDGE_TRUST_BINDING_ONLY`
- Railway_ingress_redeploy_authority: `EXACT_CURRENT_SOURCE_PRIVATE_NO_DOMAIN`
- Railway_worker_deploy_authority: `ONLY_IF_PROVIDER_REQUEST_SOURCE_CHANGED`
- public_domain_authority: `NONE`
- edge_trust_enable_authority: `NONE`
- DB_mutation_authority: `NONE`
- DB_migration_authority: `NONE`
- new_DB_login_role_grant_authority: `NONE`
- production_source_change_authority: `NARROW_PROVIDER_REQUEST_CONTRACT_HARDENING_ONLY`
- real_provider_canary_authority: `NONE`
- temporary_Railway_SSH_key_authority: `ONE_EPHEMERAL_KEY_IF_REQUIRED_FOR_READONLY_PROOF`

## Goal

Close exactly:

1. `INGRESS_EDGE_TRUST_ROLLBACK_RESIDUE`
2. `REPEATED_PROVIDER_BAD_REQUEST_COMPATIBILITY_UNPROVED`

without creating a public run or making a real provider call.

Do NOT release Public Live.

## accepted entry state

```text
Git main:
f3f8acd5af11c56de2dacba2777aa3e0e9b85cb7

diagnostic source:
aca0f5112b37675d6fb2449352f890abfa0d0076

migration head:
20260919_0025

1919:
FAILED_NOT_DISPATCHED / SETTLED 0

0125:
FAILED_TIMEOUT / SETTLED conservative 4400

1145:
FAILED_TIMEOUT / SETTLED conservative 4400

campaign held:
0

open claims:
0

open pins:
0

Public control:
DISABLED

Public Live:
NOT_RELEASED

public ingress domains:
0

frontend:
Replay-only
```

## Browser external API-contract evidence

As of 2026-09-19, Browser independently checked official OpenAI API documentation.

Supported/current facts:
- model `gpt-5.6-luna` exists and supports Responses API and function calling;
- reasoning effort `low` is supported;
- Responses create supports:
  - `include`;
  - `parallel_tool_calls`;
  - `service_tier`;
  - `store`;
  - `max_output_tokens`;
  - `truncation`;
  - custom function tools;
- `reasoning.encrypted_content` is a supported include value for stateless/store-false reasoning continuation;
- strict function schemas require `additionalProperties:false` and every defined property to be represented in `required`.

Do not trust Browser summary blindly. If network access is available, recheck current official `developers.openai.com` docs. Do not access the authenticated OpenAI API.

## Phase A — exact repository / hosted preflight

Verify:
- `HEAD == origin/main == f3f8acd5af11c56de2dacba2777aa3e0e9b85cb7`;
- diagnostic source commit `aca0f5112b37675d6fb2449352f890abfa0d0076` in ancestry;
- no unrelated tracked mutation;
- migration head 0025 via read-only evidence if available;
- control disabled;
- held reservations 0;
- active future public runs 0;
- claimable work 0;
- open claims/pins 0;
- provider calls after 1225: 0;
- ingress public domains 0;
- worker public domains 0;
- frontend release-disabled.

If public exposure exists:

`PUBLIC_FAIL_CLOSED_STATE_REGRESSION`

and STOP.

## Phase B — audit ingress variable ownership WITHOUT reading secret values

Inspect Railway variable/binding metadata for the existing `aiscc-public-live-ingress`.

Required focus:
- `AISCC_PUBLIC_LIVE_RAILWAY_EDGE_TRUST`;
- `PUBLIC_LIVE_API_ORIGIN`.

Current expected rollback state:

```text
AISCC_PUBLIC_LIVE_RAILWAY_EDGE_TRUST:
must be ABSENT after cleanup

PUBLIC_LIVE_API_ORIGIN:
ABSENT or exact safe disabled-state representation

public domains:
0
```

Determine whether the stale edge-trust value is:
- service-local;
- inherited/shared;
- reference-bound.

Do not print/export the variable value.

If removing it would require mutating a shared/global variable used by another service, do not blindly delete shared state.

Prefer:
- detach/remove the ingress service binding only; or
- remove the ingress-local variable only.

If exact service-local cleanup cannot be performed without broader shared mutation:

`INGRESS_EDGE_TRUST_SCOPE_EXPANSION_REQUIRED`

and STOP.

## Phase C — remove stale edge-trust binding

Authorized mutation:

**only** remove/detach `AISCC_PUBLIC_LIVE_RAILWAY_EDGE_TRUST` from the ingress service's effective runtime configuration.

Also ensure no release-origin binding remains.

Do not:
- create public domain;
- set edge trust to an enabled value;
- add a new release origin;
- change DB bindings;
- change source-key/HMAC binding;
- change provider secret bindings;
- change scale/region/start command;
- mutate worker/initializer/API config.

After mutation, deploy/restart the existing ingress using exact current source.

Required result:
- deployment SUCCESS/healthy;
- public domain count 0;
- effective edge-trust binding ABSENT;
- release origin absent/safe disabled;
- no `PUBLIC_LIVE_EDGE_CONFIGURATION_DENIED`;
- no public run/provider call;
- control remains disabled.

## Phase D — exact provider request-contract audit

Audit the exact request generated by:

`OpenAIResponsesAdapter.call()`

for hosted profile `public-live-luna-v1`.

No authenticated HTTP call.

Build/serialize the exact canonical PRIMARY request locally with:
- model `gpt-5.6-luna`;
- fixed initial inputs;
- fixed `stockroom_summary` tool;
- reasoning effort low;
- max output tokens 2000;
- store false;
- background false;
- stream false;
- parallel tool calls false;
- truncation disabled;
- service tier default;
- reasoning encrypted-content include.

Create a field-by-field compatibility matrix against current official Responses API documentation.

Classify every field:

```text
SUPPORTED
DOCUMENTED_OPTIONAL
AISCC_POLICY_CONSTRAINT
INCOMPATIBLE
UNPROVED
```

Do not infer the historical provider's raw error message.

## Phase E — strict zero-argument function-schema hardening

Current AISCC fixed tool is semantically zero-argument.

Current registry source has historically allowed a schema shape equivalent to:

```json
{
  "type": "object",
  "required": [],
  "additionalProperties": false
}
```

Canonicalize the exact public tool input schema to:

```json
{
  "type": "object",
  "properties": {},
  "required": [],
  "additionalProperties": false
}
```

unless current official documentation provides a stronger exact requirement.

Update `bind_call`/validation so there is ONE canonical hosted schema shape, not two silently accepted alternatives.

This is compatibility hardening.

Do NOT claim it was definitively the cause of the historical 400 unless you have direct evidence.

Preserve:
- zero user-supplied tool args;
- strict true;
- one fixed tool only;
- process/filesystem/tool-network/tool-secret = 0;
- Public Docker dependency = 0;
- Owner/Self-Dogfood separate.

No migration.

If additional provider request fields must change based on official docs, each change must be:
- exact;
- documented;
- narrowly justified;
- covered by deterministic tests.

If request compatibility requires architecture/profile/authority redesign:

`PROVIDER_REQUEST_CONTRACT_SCOPE_EXPANSION_REQUIRED`

and STOP.

## Phase F — diagnostic contract check

Retain the accepted diagnostic source semantics:

```text
TRANSPORT_OUTCOME_UNKNOWN
PROVIDER_HTTP_ERROR_RESPONSE
MALFORMED_RESPONSE_BODY
UNKNOWN_RESPONSE_STATUS
PROVIDER_NONTERMINAL_STATUS
PROVIDER_DISPATCH_EXCEPTION
```

No arbitrary exception text.

No raw provider body/request/output.

No retry authority change.

If source edits are required for request hardening, ensure `provider_diagnostic` behavior remains unchanged.

## Phase G — deterministic tests

Required tests without network/provider:

1. exact canonical hosted request serialization snapshot/structural assertion;
2. exact model = `gpt-5.6-luna`;
3. exact zero-argument tool schema includes `properties: {}`;
4. strict true;
5. no extra tool;
6. parallel tool calls false;
7. store false;
8. reasoning effort low;
9. max output tokens 2000;
10. include only accepted encrypted reasoning value plus any exact existing required include;
11. service tier and truncation match official contract;
12. request stays under AISCC input bound;
13. APIStatusError maps to `PROVIDER_HTTP_ERROR_RESPONSE`;
14. timeout/connection maps to `TRANSPORT_OUTCOME_UNKNOWN`;
15. malformed/unknown/nonterminal mappings unchanged;
16. durable service persists only allowlisted diagnostic refs;
17. no provider retry;
18. fixed-tool dispatcher tests remain green;
19. worker claim sequence tests remain green;
20. 0025 UNKNOWN reconciliation tests remain green;
21. canonical persistence directly affected selection remains green.

Also:
- Ruff PASS;
- format PASS;
- narrow mypy PASS for changed production owner;
- `git diff --check` PASS;
- secret-safe scan PASS.

No real provider call.

## Phase H — commit/push and worker deployment

If source/test changes are required:
- commit exact request-contract hardening;
- fast-forward push only;
- no amend/rebase/force;
- no unrelated file changes.

Because request construction is worker-owned, deploy the existing `aiscc-public-live-worker` to exact new source if production source changed.

Worker deployment constraints:
- same service;
- same region;
- same replica count;
- same start command;
- same DB binding;
- same provider secret binding;
- public domains 0;
- no provider call;
- no public run.

Prove healthy idle acquisition after deployment.

Repository-connected ingress may passively redeploy from the push. Its effective edge trust must remain absent and it must become/remain healthy.

## Phase I — final read-only Replay-only readiness reproof

Freshly prove:

### ingress
- healthy current deployment;
- edge-trust binding ABSENT;
- release origin absent/safe disabled;
- public domains 0;
- no startup configuration denial.

### DB
- migration head 0025;
- 1919/0125/1145 durable terminal states unchanged;
- held 0;
- slots free;
- claimable work 0;
- open claims/pins 0;
- UNKNOWN reconciliation candidate set empty;
- campaign/day conservation exact.

### provider/worker
- worker healthy;
- accepted claim-sequence fix retained;
- request-contract source current;
- provider secret worker-only/sealed/service-local;
- ingress/initializer/API have no provider secret authority;
- provider calls during this Task 0.

### Replay
- public/release-disabled;
- `enabled=false`;
- `api_origin=null`;
- CSP `connect-src 'self'`;
- four Replay scenarios unchanged.

## success target

If both blockers close:

```text
INGRESS_EDGE_TRUST_RESIDUE_CLOSED
/
PROVIDER_REQUEST_CONTRACT_HARDENED
/
REPLAY_ONLY_SAFE
/
EXACT_TOOL_PROVIDER_CANARY_DECISION_REQUIRED
/
BROWSER_REVIEW_REQUIRED
```

Do not grant provider-call authority.

Do not grant release authority.

## blockers

Use the narrowest exact blocker:

```text
INGRESS_EDGE_TRUST_SCOPE_EXPANSION_REQUIRED
INGRESS_EDGE_TRUST_CLEANUP_FAILED
INGRESS_PRIVATE_DEPLOYMENT_UNHEALTHY
PROVIDER_REQUEST_CONTRACT_SCOPE_EXPANSION_REQUIRED
PROVIDER_REQUEST_CONTRACT_UNPROVED
PROVIDER_REQUEST_CONTRACT_TEST_FAILED
WORKER_DEPLOYMENT_IDENTITY_MISMATCH
WORKER_IDLE_ACQUISITION_REGRESSION
PUBLIC_FAIL_CLOSED_STATE_REGRESSION
TEMP_OPERATOR_ACCESS_CLEANUP_FAILED
```

## temporary operator access

At most one ephemeral Railway SSH key if required for read-only DB proof.

- no public DB endpoint;
- no key bytes exported;
- no DB credentials exported;
- no provider secret value read;
- remove Railway key;
- remove local keypair/helper;
- prove cleanup by metadata.

## forbidden

- Public Live release;
- public control enable;
- public ingress domain creation;
- edge-trust enable;
- frontend Live enable;
- Cloudflare mutation;
- new public run;
- real provider call/canary;
- provider retry/resend;
- manual provider send;
- DB DDL/DML;
- migration;
- DB role/login/grant expansion;
- public DB exposure;
- provider secret read/copy/rotation;
- unrelated historical-test repair;
- unrelated product work.

## canonical persistence

Persist supplied Cycle/Judgment/Handoff.

Move this Task active -> done.

Source/test commit only for exact provider request hardening.

Governance commit may be separate.

Fast-forward push only.

## required export

Create:

`.aiassistant/reports/target/20260919_1329_aiscc-p3-3-l8-ingress-edge-trust-cleanup-and-provider-request-contract-hardening-1/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `INGRESS_VARIABLE_OWNERSHIP.md`
- `INGRESS_EDGE_TRUST_CLEANUP.md`
- `INGRESS_PRIVATE_DEPLOYMENT_PROOF.md`
- `PROVIDER_REQUEST_CONTRACT_MATRIX.md`
- `STRICT_TOOL_SCHEMA_AUDIT.md`
- `REQUEST_CONTRACT_SOURCE_AUDIT.md`
- `REQUEST_CONTRACT_TESTS.md`
- `WORKER_DEPLOYMENT_PROOF.md` if source changed, otherwise `WORKER_DEPLOYMENT_NOT_REQUIRED.md`
- `HOSTED_SAFE_STATE.md`
- `PROVIDER_SECRET_APPLICABILITY.md`
- `REPLAY_FRONTEND_READINESS.md`
- `TEMP_OPERATOR_ACCESS_PROOF.md`
- `WORKSPACE_STATE.md`
- changed source/test/governance files preserving repository-relative paths

Also create adjacent result ZIP and report SHA-256.

Never export:
- provider key or masked key identifier;
- DB DSN/password;
- SSH key material;
- HMAC/source key;
- read capability;
- raw provider request containing secret material;
- raw provider response/body/output;
- private reasoning.

## final response format

1. result
2. target ZIP SHA-256
3. ingress variable ownership
4. edge-trust cleanup
5. ingress deployment health
6. provider request compatibility matrix
7. exact strict tool-schema change
8. source/test commit(s)
9. worker deployment if any
10. tests/static checks
11. provider calls/resends
12. DB/ledger/claim/pin safe state
13. provider-secret isolation
14. Replay state
15. temporary access cleanup
16. next canary decision state
17. blockers/unverified
