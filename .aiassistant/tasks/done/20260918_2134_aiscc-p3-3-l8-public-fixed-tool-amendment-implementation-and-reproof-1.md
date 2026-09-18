# AISCC Task — L8 Public Fixed Tool Amendment Implementation and Affected L5/L6 Reproof

## meta

- task_id: `20260918_2134_aiscc-p3-3-l8-public-fixed-tool-amendment-implementation-and-reproof-1`
- phase: `P3-3 / L8 re-release recovery`
- work_type: `PUBLIC_LIVE_RUNTIME_CONTRACT_AMENDMENT_IMPLEMENTATION`
- execution_model: `THIN_CC_THICK_EXECUTOR`
- entry_commit: `0c915f04aaf3b0b026ac6224f1c6c10d390f7075`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- Human_decision: `ACCEPT_PUBLIC_FIXED_IN_PROCESS_TOOL`
- public_release_authority: `NONE`
- public_run_authority: `NONE`
- real_provider_call_authority: `NONE`
- hosted_DB_mutation_authority: `NONE`
- ingress_public_exposure_authority: `NONE`
- Cloudflare_mutation_authority: `NONE`
- existing_private_worker_redeploy_authority: `BOUNDED`

## Goal

Implement the Human-approved Public-Live-only Stockroom runtime amendment:

```text
PUBLIC_BOUNDED_LIVE
stockroom-s1-normal / 1.0.0

Tool Broker
-> TOOL authority only
-> fixed deterministic in-process Stockroom dispatcher
-> canonical existing STOCKROOM_SUMMARY
-> ToolOutputRef
```

Then re-prove the affected Public Live L5/L6 security/runtime assertions without any public run or real provider request.

Do not release Public Live in this Task.

## Why this is an explicit amendment

The previous frozen Public Live implementation reused the Docker-backed Stockroom process path.

Railway production worker does not provide the Docker executable/daemon needed by that path.

The Human has explicitly accepted a narrower Public Live contract for the competition deployment.

This is not an implicit implementation shortcut.

## Exact amended runtime contract

Applies only when all are true:

```text
runtime_mode = PUBLIC_BOUNDED_LIVE
scenario_id = stockroom-s1-normal
scenario_version = 1.0.0
provider_profile = public-live-luna-v1 / 1
tool = stockroom_summary
arguments = exact empty object
```

Required Public Live tool semantics:

```text
tool identity:
aiscc-stockroom-tools / current accepted version

tool side effect:
READ_ONLY

tool result:
existing canonical STOCKROOM_SUMMARY

TOOL capability:
exactly one required/consumed

PROCESS capability:
zero

FILESYSTEM capability:
zero

tool NETWORK capability:
zero

tool SECRET capability:
zero

subprocess:
zero

Docker:
zero dependency

filesystem access during dispatch:
zero

network access during dispatch:
zero
```

The OpenAI provider path is separate and remains:

```text
provider:
OpenAI

model:
gpt-5.6-luna

provider secret:
worker-only / sealed / HostedOpenAISecretResolver

provider network:
existing bounded provider authority
```

Do not conflate provider network authority with tool network authority.

## Owner/Self-Dogfood non-regression

`OWNER_SELF_DOGFOOD` must remain on the existing Docker-backed Stockroom path.

Do not modify its semantic contract:

- Docker image provenance;
- fixed image/currentness checks;
- process scope;
- `network=none`;
- workspace boundary;
- timeout/kill/settlement;
- `KNOWN_TOOL_* / UNKNOWN_TOOL_OUTCOME`;
- output stream/JSON validation.

If the easiest implementation would change Owner/Self-Dogfood behavior, do not take that path.

## Preferred source shape

Executor chooses mechanics, but preserve semantic separation.

A good shape is:

- keep current owner `StockroomSummaryDispatcher` / Docker registry path intact;
- introduce a Public-Live-specific fixed dispatcher and, if needed, Public-Live-specific registry/authority builder;
- reuse the existing `ToolRegistryBroker` validation/receipt/durable-operation flow;
- avoid pretending a PROCESS resource exists when none is used.

Do not duplicate unrelated provider/service orchestration.

## Required Tool Broker semantics

The fixed tool MUST still traverse the real Tool Broker path:

```text
Provider ToolCallCandidate
-> registry lookup
-> exact schema validation
-> profile/mode/scenario allowlist
-> operation fingerprint
-> TOOL capability issue
-> TOOL capability consumption receipt
-> receipt claim/binding for dispatch
-> fixed dispatcher
-> output schema/hash validation
-> durable TOOL operation
-> provider continuation
```

No direct shortcut from provider result to `STOCKROOM_SUMMARY`.

No caller-supplied tool output.

## Fixed dispatcher requirements

The Public Live fixed dispatcher must:

1. accept only the exact Public Live tool definition;
2. accept only the exact empty JSON object;
3. require the authentic claimed Tool Broker receipt/dispatch identity expected by the current broker contract;
4. reject missing, duplicate, mismatched or already-consumed authority;
5. return a fresh safe object equivalent to the canonical `STOCKROOM_SUMMARY`;
6. emit `ToolOutputRef` with correct argument/result hash binding;
7. perform no filesystem access;
8. perform no network access;
9. perform no subprocess/process creation;
10. perform no environment/secret read.

Do not use the production OpenAI secret.

## Public Live authority requirements

After amendment, Public Live Stockroom authority must not mint/own/request:

- `ResourceDomain.PROCESS`;
- `ResourceDomain.FILESYSTEM`;
- tool `ResourceDomain.NETWORK`.

The fixed tool still requires the appropriate `ResourceDomain.TOOL` authority.

Provider/SECRET authority remains independently governed by the existing provider path.

Update security policy special cases only as narrowly as required.

Do not broaden any other Public Live or Owner mode.

## Dispatch-context truthfulness

The current Public Live dispatch context contains a resolved Stockroom spec fingerprint derived from Docker spec.

Under the amended Public Live contract, do not retain a field/value that falsely claims a Docker process spec was resolved.

Executor must choose the smallest truthful compatible binding, for example:
- a Public-Live fixed-tool resource/implementation fingerprint;
- or another existing typed binding that accurately represents the deterministic dispatcher.

If changing this requires a shared contract extension, keep it additive and Public-Live-specific.

Owner/Self-Dogfood Docker dispatch context must remain unchanged.

## L5 affected reproof

Re-open only affected Public Live L5 assertions.

Prove:

### Tool/process/filesystem/network boundary

For Public Live:
- tool process execution does not exist;
- filesystem dispatch authority does not exist;
- tool network dispatch authority does not exist;
- Docker executable and daemon are not prerequisites;
- public fixed dispatcher cannot invoke arbitrary shell/argv/path/URL;
- no raw provider secret can reach the tool.

### Replay independence

Replay still has no dependency on:
- worker;
- provider;
- Public Live DB;
- fixed tool dispatcher.

### Worker hosted runtime

On the existing private `aiscc-public-live-worker` service only:

- deploy the accepted candidate if source commit/redeploy is needed;
- keep admission disabled;
- keep ingress private;
- do not create work;
- prove worker starts/registers normally without Docker;
- prove no Docker-required observation/failure remains relevant to the production Public Live composition;
- prove provider key presence remains worker-only/sealed and is not read/used;
- provider request count remains unchanged.

Do not add a new Railway service/resource.

## L6 affected reproof

Use isolated/disposable PostgreSQL and synthetic provider transport.

At minimum prove the amended production composition supports:

```text
provider call 1
-> stockroom_summary tool call
-> fixed brokered tool completion
-> provider continuation
-> terminal governed execution
```

with expected durable operation lineage such as:

```text
PROVIDER / completed
TOOL / completed
PROVIDER / completed
```

according to the current canonical semantics.

Also prove:

- exact scenario/profile/repository pins;
- no PROCESS capability request/receipt;
- no filesystem/network tool capability request/receipt;
- fixed dispatcher invocation count exactly one for normal S1;
- malformed/non-empty tool args denied before output;
- foreign scenario/profile/mode denied;
- duplicate/forged receipt/dispatch reuse denied;
- provider retry/call bounds unchanged;
- unknown-provider send semantics unchanged;
- admission/rate/budget/slot limits unaffected;
- Replay independence unchanged.

No actual OpenAI request.

## Failed 1919 smoke

Read-only only.

Retain:

- failed run;
- reservation;
- slot;
- campaign;
- zero-send evidence.

Do not reconcile/settle it in this Task.

Verify the existing mediated `FAILED_NOT_DISPATCHED` closure path remains compatible and report the exact separately authorized follow-up needed.

## Worker observability cleanup

2036 added Docker prerequisite observations for diagnosis.

After the Public Live contract no longer depends on Docker:

- remove or revise runtime observations that would falsely imply Docker is still a Public Live prerequisite;
- retain useful secret-safe generic claim failure observability;
- do not emit raw exceptions/environment values.

Do not remove owner Docker diagnostics if they are owned elsewhere and still truthful.

## Source scope

Expected narrow owners may include:

- `src/aiscc/public_live/stockroom_runtime.py`
- `src/aiscc/public_live/provider_authority.py`
- `src/aiscc/public_live/worker.py`
- `src/aiscc/security/policy.py`
- minimal shared Tool Broker/model code only if required for truthful receipt/binding semantics;
- focused Public Live tests;
- governance/state projection;
- this Task lifecycle.

`src/aiscc/providers/stockroom_tool.py` owner Docker semantics should remain unchanged unless an additive helper extraction is necessary and proven non-regressive.

No frontend changes.

No DB migration.

## Required tests

Run targeted tests sufficient to prove the changed semantic owners.

Minimum categories:

1. public fixed tool exact empty-object success;
2. non-empty/extra args denied;
3. wrong mode/profile/scenario denied;
4. exactly one TOOL capability consumed;
5. zero PROCESS capability;
6. zero FILESYSTEM capability;
7. zero tool NETWORK capability;
8. no subprocess/Docker lookup in Public Live dispatch;
9. no filesystem read/write in Public Live dispatch;
10. no network/socket/HTTP use in Public Live dispatch;
11. duplicate/forged dispatch authority denied;
12. canonical output schema/hash exact;
13. durable Tool operation exists;
14. provider continuation receives tool output;
15. owner Docker path regression remains PASS;
16. current worker/root-cause diagnostic tests updated truthfully;
17. isolated PostgreSQL amended production chain PASS;
18. Replay builder/check PASS;
19. real provider call count = 0.

Also:
- Ruff;
- formatter check;
- narrow mypy for changed production source;
- `git diff --check`.

Run broader affected Public Live integration/security tests if feasible.

Do not use a real provider or public endpoint.

## Hosted private proof

Allowed external action:

Existing Railway production `aiscc-public-live-worker` private service may be redeployed to the candidate source for no-send proof.

Before deploy verify:
- control/admission disabled;
- no queued/new work except retained failed evidence not claimable for new execution;
- no public ingress;
- no edge trust;
- provider key worker-only/sealed.

After deploy verify:
- deployment healthy/running;
- worker registers;
- fixed tool composition has no Docker prerequisite;
- no provider usage;
- no new execution/run side effects.

If the retained 1919 row can be automatically reclaimed/claimed by the worker after redeploy and this could mutate it, STOP before worker redeploy and report:
`HOSTED_PRIVATE_PROOF_BLOCKED_BY_RETAINED_WORK`.

Do not mutate the retained run merely to make hosted proof convenient.

## Stop boundaries

STOP if:

- eliminating Docker requires weakening provider/secret authority;
- fixed tool would bypass Tool Broker receipts;
- a public process/filesystem/network capability remains necessary;
- DB migration/grant is required;
- new hosted service/resource is required;
- retained 1919 work would be executed/mutated by private proof;
- proof requires real provider call;
- Owner/Self-Dogfood Docker semantics cannot remain unchanged.

Use the narrowest result.

## Acceptance target

Successful implementation/reproof candidate:

```text
PUBLIC_FIXED_TOOL_IMPLEMENTED
/
AFFECTED_L5_L6_REPROOF_CANDIDATE
/
BROWSER_REVIEW_REQUIRED
```

If source is correct but hosted private proof is safely blocked by retained work:

```text
PUBLIC_FIXED_TOOL_LOCAL_REPROOF_CANDIDATE
/
HOSTED_PRIVATE_PROOF_BLOCKED_BY_RETAINED_WORK
```

No result means Public Live released.

## Git / persistence

- exact baseline required;
- ordinary commit/push authorized;
- supplied Cycle/Judgment/Handoff must be persisted;
- active Task -> done;
- target export remains ignored/untracked;
- no amend/rebase/force push.

## export

Create:

`.aiassistant/reports/target/20260918_2134_aiscc-p3-3-l8-public-fixed-tool-amendment-implementation-and-reproof-1/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `AMENDED_RUNTIME_CONTRACT.md`
- `PUBLIC_TOOL_AUTHORITY_PROOF.md`
- `OWNER_DOCKER_NONREGRESSION.md`
- `L5_AFFECTED_REPROOF.md`
- `L6_AFFECTED_REPROOF.md`
- `HOSTED_PRIVATE_WORKER_PROOF.md`
- `FAILED_1919_FOLLOWUP.md`
- `FINAL_SAFE_STATE.md`
- `WORKSPACE_STATE.md`
- changed files preserving repository-relative paths

Also create adjacent ZIP and verify integrity.

Never export:
- OpenAI API key;
- DB DSN;
- HMAC key;
- read capability;
- raw provider output;
- raw exception/environment values.
