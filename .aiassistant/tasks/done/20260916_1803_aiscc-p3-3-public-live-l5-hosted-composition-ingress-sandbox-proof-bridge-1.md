# 작업지시서: P3-3 L5 Hosted Composition / Ingress / Sandbox Proof Bridge

## meta

- task_id: `20260916_1803_aiscc-p3-3-public-live-l5-hosted-composition-ingress-sandbox-proof-bridge-1`
- created_at: `2026-09-16 KST`
- work_type: `HOSTED_L5_PROOF_BRIDGE`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_HEAD: `96a4029ec3a82c9b2a88b9718732aa0f00ecad20`
- primary_semantic_owner: `P3-3 Public Live L5 hosted proof`

Use the current IDE Executor conversation. No fresh chat is required.

## current accepted deployed state

```text
accepted/published/deployed source:
96a4029ec3a82c9b2a88b9718732aa0f00ecad20

Railway Project:
AISCC

Environment:
production

backend:
aiscc-public-live-api
ONLINE / ACTIVE
Singapore

Postgres:
ONLINE
Singapore

AISCC_OPENAI_API_KEY:
service-local / sealed / present

trusted API:
/health = 200

Public admission:
DISABLED

Public Live:
NOT_RELEASED

real provider calls:
0
```

## governing exact L5 exit

Recover and re-verify the exact frozen L5 authority from frozen commit:

`209e7534f66e9b07ce9d33742e6993370a70f4fb`

Required exit:

1. Railway trusted peer and header overwrite contract demonstrated with spoof cases.
2. Supervisor termination, no-send fencing and remote-unknown quarantine demonstrated.
3. No public owner DB route or secret exposure.
4. Tool/network/filesystem isolation and Replay independence proven.
5. Actual paid/deployment actions require separate authorization.

If the recovered authority differs: STOP.

## retained accepted facts

Preserve:

- accepted Luna profile and adaptive role/call policy;
- accepted secret mediation and single-use lease semantics;
- `AISCC_OPENAI_API_KEY` service-only resolver contract;
- Public Live context capability authority;
- missing/blank secret pre-dispatch `LIVE_UNAVAILABLE`;
- actual post-dispatch uncertainty remains UNKNOWN / no blind retry;
- child environment deny of provider keys;
- public admission remains disabled;
- Replay remains zero-execution.

The prior readiness audit explicitly found:

`src/aiscc/public_live/http.py` exists as an isolated fail-closed Public Live ASGI composition but is NOT mounted by `aiscc.api.app:app`.

## Phase A — exact production composition audit

Before mutation, inspect at minimum:

- `src/aiscc/api/app.py`
- `src/aiscc/api/**`
- `src/aiscc/public_live/http.py`
- `src/aiscc/public_live/**`
- trusted proxy/header normalization owners
- supervisor/worker termination owners
- no-send/unknown-outcome owners
- Docker/process/child environment owners
- Replay/static composition owners
- deployment metadata
- tests proving L1/L2/L5 behavior
- frozen L5 historical refs named by the authority record.

Write:

`HOSTED_L5_PROOF_BRIDGE_AUDIT.md`

Answer exactly:

1. What production route/mount shape is already canonical for Public Live, if any?
2. What component owns trusted-peer identity?
3. Which client-controlled forwarding/trust headers are stripped/overwritten?
4. Which exact spoof cases are already testable?
5. How is supervisor termination connected to no-send fencing?
6. How is actual remote-unknown outcome quarantined?
7. Which public routes can reach owner DB/state and which are forbidden?
8. Can any public/child/sandbox process observe `AISCC_OPENAI_API_KEY` or `OPENAI_API_KEY`?
9. What outbound network destinations can the public runtime use?
10. How is Replay kept independent when Live/provider/runtime fails?
11. What exact hosted proof still cannot be produced until a later Human/Railway operation?

Do not invent route names, headers, proxy identities, environment names or authority classes.

## Phase B — smallest production proof bridge

Only if the current accepted architecture already determines the exact mount/route/trust contract unambiguously, implement the smallest additive bridge needed for hosted L5 proof.

Allowed source scope is limited to the exact current semantic owners discovered in Phase A, plus directly corresponding tests.

Requirements:

- Public admission MUST remain disabled.
- Mounting a disabled/fail-closed Public Live route is allowed only if the existing composition already truthfully returns disabled/unavailable semantics without provider execution.
- No route may expose owner/private DB mutation/read APIs to anonymous public callers.
- No raw secret may become reachable through request scope, child env, error, log, response, trace or public evidence.
- Do not create a bypass endpoint for canary/provider calls.
- Do not create a direct-key diagnostic route.
- Do not weaken trusted-peer/header overwrite rules.
- Do not expose arbitrary shell/network/repository/upload inputs.
- Do not change WorkflowState/ExecutionStatus/provider role/retry/money semantics.

If the exact production mount/route or trusted-peer composition is not canonically determined:

`HOSTED_COMPOSITION_BINDING_DESIGN_REQUIRED`

and STOP without guessing.

## Phase C — local non-paid proof

No real provider call.

Use fake/sentinel secrets and local PostgreSQL/Docker only where needed.

Required local proof classes:

### trusted peer/header overwrite

Prove canonical peer identity is server-owned and client-supplied trust/forwarding headers cannot self-authorize.

Include positive and spoof cases.

### supervisor/no-send/unknown

Prove:

- termination before dispatch => definitely not sent / zero provider request;
- dispatch uncertainty => remote unknown quarantine;
- no blind retry;
- worker/process termination is bounded and child tree does not remain detached.

### public owner DB boundary

Prove public routes cannot invoke owner/private mutation/review/admin DB owners merely by knowing IDs or sending crafted headers.

### secret non-exposure

With fake sentinel in trusted parent environment, prove sentinel absent from:

- public request/response;
- child process env;
- sandbox/container env;
- logs;
- durable DB/public serialization;
- Replay artifacts.

### tool/network/filesystem isolation

Use accepted product runtime path, not a hand-built substitute.

Prove public runtime has only the accepted allowlisted capability surface and no arbitrary owner filesystem/network access.

### Replay independence

Simulate Live/provider/secret/worker failure and prove Replay/static path performs zero provider/tool/process/network/secret execution and remains independently available according to accepted semantics.

## Phase D — hosted Human QA plan

Emit:

`HOSTED_L5_HUMAN_QA_PLAN.md`

Map every frozen L5 exit item to:

- already accepted local evidence;
- source change, if any;
- exact later Railway/HTTP Human action;
- exact expected PASS evidence;
- whether a deployment is required;
- whether public networking is required;
- whether Cloudflare is required;
- whether provider spend is required.

The plan must keep the paid canary separate.

## real provider canary

FORBIDDEN in this Task.

Retain the accepted canary contract:

```text
provider: OpenAI
model: gpt-5.6-luna
API: Responses
reasoning: low
fixed synthetic non-secret input
tools: none
store=false
background=false
stream=false
max physical paid requests: 1
retry: 0 for canary
public request: none
```

Do not execute it.

The canary may be authorized only after Browser accepts the hosted isolation/egress prerequisites identified by this Task.

## tests/checks

Run exact focused tests for every changed semantic owner.

If shared security/runtime/public-live owners change, run the full repository suite using the accepted harness.

Current accepted full baseline:

`1460 PASS / 3 existing SKIP / 0 FAIL / 0 ERROR`

No new skip/xfail/assertion dilution.

Also run:

- Ruff;
- formatter check under repository convention;
- mypy changed production owners;
- `git diff --check`;
- secret scan without printing secret values.

## external actions forbidden

```text
real OpenAI/provider request:
0

Railway mutation:
0

Railway deploy/restart:
0

Railway public networking:
0

Cloudflare mutation:
0

Git commit:
0

Git push:
0

Public admission enable:
0

Public Live release:
0
```

Do not read or export the real OpenAI key.

## acceptable outcomes

### implementation path

`HOSTED_L5_PROOF_BRIDGE_IMPLEMENTED / LOCAL_ACCEPTED_CANDIDATE`

### no source change required

`HOSTED_L5_PROOF_BRIDGE_PROVEN / HUMAN_HOSTED_QA_REQUIRED`

### canonical composition ambiguous

`HOSTED_COMPOSITION_BINDING_DESIGN_REQUIRED`

None of these terminally accepts L5.

## mandatory stop

- HEAD mismatch;
- frozen L5 authority mismatch;
- exact mount/trust route requires guessing;
- safe hosted proof requires provider key exposure;
- proof requires weakening public admission or security policy;
- full regression fails after shared-owner change;
- fake sentinel appears in durable/public/log artifacts;
- real provider/Railway credentials are required.

## export

Create:

`.aiassistant/reports/target/20260916_1803_aiscc-p3-3-public-live-l5-hosted-composition-ingress-sandbox-proof-bridge-1/`

Required:

- `EXECUTOR_REPORT.md`
- `HOSTED_L5_PROOF_BRIDGE_AUDIT.md`
- `HOSTED_L5_HUMAN_QA_PLAN.md`
- `TEST_EVIDENCE.json`
- `SOURCE_INVENTORY.json` if source changed
- secret non-exposure evidence
- ingress spoof evidence
- supervisor/no-send/unknown evidence
- Replay independence evidence
- `WORKSPACE_BEFORE.txt`
- `WORKSPACE_AFTER.txt`
- exact Task copy
- result ZIP

## final response

1. result
2. HEAD
3. frozen L5 authority
4. production composition audit
5. source changes
6. trusted-peer/header spoof proof
7. supervisor/no-send/unknown proof
8. owner DB/public boundary proof
9. secret non-exposure proof
10. tool/network/filesystem isolation proof
11. Replay independence proof
12. tests/static/type checks
13. provider calls
14. external actions
15. Human hosted QA plan
16. canary status
17. Public state
18. workspace integrity
19. next Browser gate
