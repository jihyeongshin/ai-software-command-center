# 작업지시서: P3-3 L5 Durable Worker Work-Source / Claim Authority Design Freeze

## meta

- task_id: `20260916_2303_aiscc-p3-3-public-live-l5-durable-worker-work-source-authority-design-freeze-1`
- created_at: `2026-09-16 KST`
- work_type: `DESIGN_AUDIT`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_HEAD: `96a4029ec3a82c9b2a88b9718732aa0f00ecad20`
- predecessor_result_zip_sha256: `c264eaefe92a206c1872c55b4577e7f27abfed38bb998b8d163a1f839ec3747d`
- primary_semantic_owner: `P3-3 Public Live durable worker discovery / claim / lease / fencing authority`

Use the current IDE Executor conversation. No fresh chat is required.

## predecessor judgment

Browser accepted:

`DURABLE_WORKER_COMPOSITION_DESIGN_REQUIRED`

This Task is design-only and is not an implementation retry.

## fixed upstream decisions

Do NOT reopen:

- 2012 Hosted Public Live Binding Design;
- separate public ingress / private worker / private trusted API / separate Live Postgres topology;
- Human D8=A application-mediated egress;
- fixed OpenAI/Luna provider policy;
- Public admission disabled;
- Public Live not released.

## mandatory authority recovery

Read and reconcile the exact current canonical owners for:

1. `PublicLiveRepository`;
2. `PipelineStore`;
3. `ReconciliationService`;
4. `PublicProviderPipeline`;
5. public outbox/request/start/outcome tables and migrations;
6. P1-4 WorkRun/state/version authority;
7. P1-5 execution/provider/tool/secret authority;
8. P1-3 security capability / cleanup / recovery authority;
9. accepted L3/L4/L5 Public Live pipeline and retry semantics;
10. 2012 hosted binding design;
11. 2253 `DURABLE_WORKER_COMPOSITION_AUDIT.md`.

Do not infer table state names, indexes or columns from memory. Cite exact current source paths and migration definitions.

## objective

Produce one exact mediated durable worker authority design that lets the private Public Live worker safely discover and claim eligible work without caller-supplied run IDs and without bypassing existing run-specific authority.

The design must make later implementation mechanically unambiguous.

## invariant

The new work-source authority is discovery/claim authority only.

It MUST NOT itself become provider side-effect authority.

Exact separation:

```text
discoverable durable candidate
!= claimed work
!= current WorkRun/state/version valid
!= provider dispatch authorized
!= secret use authorized
!= provider outcome known
```

Every existing side-effect guard remains required after claim.

## D1 — work-item identity

Define the exact durable work-item identity.

Prefer existing durable identities if sufficient.

Decide whether the claim key is:

- outbox row ID;
- run ID + outbox kind/version;
- run ID + request ordinal;
- another existing immutable identifier.

Do not introduce a display-name/string-only authority.

Specify uniqueness and idempotency.

## D2 — exact discoverable state

Define exactly which durable records are discoverable by the private worker.

Required exclusions include, where applicable:

- terminal WorkRun;
- stale state/version;
- already durably dispatched work;
- `OUTCOME_UNKNOWN`;
- quarantined work;
- exhausted retry;
- cancelled/closed work;
- work from disabled Public admission;
- wrong scenario/profile/version;
- owner/private work.

The discovery query must be deterministic and bounded.

Specify ordering/fairness, batch size and starvation behavior.

## D3 — atomic claim

Define one mediated repository/service operation that atomically:

```text
find eligible work
+
lock/compare current eligibility
+
mint claim
+
return opaque claimed-work reference
```

No worker raw-table query.

Compare at least:

A. PostgreSQL `FOR UPDATE SKIP LOCKED` plus durable claim columns/row;
B. dedicated durable worker-claim table with unique active-claim constraint;
C. PostgreSQL advisory lock only.

Select exactly one and reject the others.

The selected design must remain restart-durable.

## D4 — worker identity and claim lease

Specify:

- server-generated worker instance ID;
- process-generation ID if distinct;
- claim ID;
- claimed_at;
- lease_expires_at;
- heartbeat/renewal rule;
- maximum lease duration;
- renewal ceiling;
- release reason;
- no user/public control over any of these.

Do not use Railway replica IP/container hostname as semantic authority unless explicitly classified as non-authoritative provenance only.

## D5 — fencing

Design a monotonic or otherwise non-reusable fencing value so a stale worker cannot dispatch after another worker has reclaimed the item.

Every dispatch authorization must bind:

```text
claim_id
+ fencing value
+ run/work item
+ authoritative current state/version
```

Stale claim/fence => fail closed before secret use/provider send.

Specify where the fence is stored and incremented.

## D6 — duplicate workers / concurrency

Design behavior for:

- two workers polling the same queue;
- worker restart;
- process crash after claim before dispatch;
- crash after `DISPATCH_STARTED`;
- claim expiry while old worker is still alive;
- rolling Railway deploy with old + new replicas;
- future replica count >1 even if current deployment starts at 1.

Exactly one worker may own a dispatchable claim at a time.

Do not solve this only with current Railway replica count=1.

## D7 — dispatch revalidation

After claim, and immediately before any provider/secret side effect, revalidate at minimum:

- claim/fence current;
- work item still dispatchable;
- authoritative WorkRun state/version;
- accepted scenario/profile/version;
- budget/call/retry limits;
- provider capability;
- secret capability/lease.

Claim age or heartbeat must not substitute for current workflow freshness.

## D8 — retry and unknown outcome

Preserve accepted semantics:

```text
known conclusively not-sent / known closed failure
→ retry only under accepted same-role retry ceiling

DISPATCH_STARTED + uncertain completion
→ OUTCOME_UNKNOWN
→ quarantine/reconciliation
→ no blind resend
```

A claim expiry or worker restart MUST NOT turn unknown work back into ordinary discoverable work.

Define how discovery excludes unknown/quarantined items.

## D9 — crash recovery

Specify exact restart recovery states for:

1. claim acquired, no dispatch started;
2. dispatch start durably committed, no outcome;
3. known provider outcome committed;
4. cleanup/release interrupted.

For each, identify the authoritative durable source and allowed next action.

Do not infer success from process exit, heartbeat loss or missing response.

## D10 — secret lease composition

Define the exact point at which `HostedOpenAISecretResolver` is invoked.

Required order:

```text
claim/fence valid
→ dispatch authorization valid
→ secret-resolution lease minted/consumed
→ secret resolved in worker parent only
→ provider transport
```

Never resolve the secret during polling/discovery/claim.

No secret in claim rows/events/logs.

## D11 — provider call construction authority

The worker must not construct a free-form `ProviderCall` from arbitrary DB text.

Design the exact server-owned builder/selector that derives:

- fixed hosted Luna profile;
- accepted reasoning role;
- normalized local durable input/history;
- output/token bounds;
- exact operation ID/fingerprint;
- tool contract when applicable.

Identify which current canonical owner can be reused and what narrow extension, if any, is required.

If creating this builder changes accepted P1-5 semantics, STOP with `P1_5_PROVIDER_AUTHORITY_EXTENSION_REQUIRED`.

## D12 — polling / wake-up behavior

Specify bounded worker loop behavior:

- poll interval and/or database notification mechanism;
- maximum batch;
- empty-queue backoff;
- shutdown signal;
- in-flight claim settling;
- no busy loop;
- no detached task;
- database failure behavior.

Prefer the simplest mechanism that is deterministic and sufficient for the competition runtime.

Do not introduce Redis/Kafka/SQS unless current accepted architecture requires it.

## D13 — schema/migration

Determine whether current schema can represent:

- claim ID;
- worker ID;
- fence;
- lease;
- heartbeat;
- release/recovery reason.

If not, design the exact additive migration.

Requirements:

- no destructive rewrite;
- no owner DB dependency;
- indexes/unique constraints sufficient for claim concurrency;
- old rows receive a fail-closed/default-safe interpretation.

Provide proposed table/column/constraint names only after inspecting current schema naming conventions.

## D14 — mediated API surface

Define exact repository/service interfaces.

At minimum cover concepts equivalent to:

```text
claim_next_work(...)
renew_claim(...)
release_claim(...)
verify_claim_for_dispatch(...)
recover_expired_claims(...)
```

Names may differ to match current conventions.

For each operation specify:

- caller;
- inputs;
- transaction boundary;
- outputs;
- failure codes;
- durable events;
- idempotency;
- forbidden use.

Raw SQL outside the persistence owner remains forbidden.

## D15 — provenance / safe observability

Specify durable safe fields:

- work-item opaque ID;
- run ID/ref as internal authority;
- claim ID;
- worker opaque ID;
- fence;
- state/version observed;
- timestamps;
- reason/result codes;
- provider destination class, not secret/value;
- no raw prompts/secret/provider payload in public logs.

## D16 — hosted proof reuse

Design how `aiscc hosted-l5-proof` later uses the same work-source/claim authority with the private provider double.

It must prove:

- pre-dispatch crash => expired/released claim can be safely retried only if durable provider dispatch never started;
- post-dispatch crash => unknown/quarantine and no claim rediscovery/blind resend;
- provider-double receipt counts;
- stale fence denial;
- worker restart recovery;
- sandbox termination remains a separate process-supervisor proof path.

QA proof must not add an HTTP bypass or fake production authority.

## D17 — implementation map

Produce an exact path-level implementation plan.

Classify each path as:

- existing owner extended;
- new production module;
- migration;
- unit test;
- PostgreSQL integration test;
- hosted-proof test;
- unchanged reused owner.

Keep the change set minimal.

## alternatives / selected design

Create:

`DURABLE_WORKER_AUTHORITY_DESIGN.md`

It must include:

- current gap;
- D1-D17;
- alternatives;
- selected design;
- rejected alternatives and reasons;
- concurrency sequence diagrams in text;
- crash/restart matrix;
- authority/non-substitution matrix;
- migration plan;
- implementation map;
- proof map.

Create:

`DURABLE_WORKER_AUTHORITY_DECISION.json`

with stable machine-readable keys for D1-D17.

## consistency requirements

The design MUST preserve:

- `AgentOutput != SystemState`;
- `ExecutionStatus != WorkflowState`;
- claim != provider dispatch authority;
- P1-3 capability mediation;
- P1-4 current state/version authority;
- P1-5 server-owned provider/tool/secret authority;
- unknown-outcome no-blind-retry;
- fixed Public Live repository/scenario/provider/model;
- no public arbitrary network/secret/provider choice;
- separate Live DB / owner DB isolation;
- Replay zero execution.

Canonical P1 security already requires restart recovery to rely on durable run/attempt lease and authoritative state/security events, and to quarantine unknown ownership rather than infer success from missing heartbeat. Preserve that behavior.

## source mutation

FORBIDDEN.

This Task may create only design/report/governance artifacts.

Do not change:

- product source;
- tests;
- migrations;
- lockfiles;
- deployment config.

## external actions forbidden

```text
OpenAI:
0

real key read/export:
0

Railway:
0

Cloudflare:
0

Git add/commit/push:
0

Public admission enable:
0

Public Live release:
0
```

## acceptable outcome

Expected:

`DURABLE_WORKER_AUTHORITY_DESIGN_CANDIDATE / HUMAN_REVIEW_REQUIRED`

Possible:

`P1_5_PROVIDER_AUTHORITY_EXTENSION_REQUIRED`

or

`CURRENT_SCHEMA_EVIDENCE_INSUFFICIENT`

No result terminally accepts L5.

## export

Create:

`.aiassistant/reports/target/20260916_2303_aiscc-p3-3-public-live-l5-durable-worker-work-source-authority-design-freeze-1/`

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `DURABLE_WORKER_AUTHORITY_DESIGN.md`
- `DURABLE_WORKER_AUTHORITY_DECISION.json`
- `CURRENT_SCHEMA_AND_OWNER_AUDIT.md`
- `DESIGN_CONSISTENCY_CHECK.md`
- `IMPLEMENTATION_MAP.md`
- `WORKSPACE_BEFORE.txt`
- `WORKSPACE_AFTER.txt`
- result ZIP

No unchanged product source export is required unless this Task explicitly changes to a separately authorized `SOURCE_EVIDENCE_EXPORT`; it does not.

## final response

1. result
2. HEAD
3. current gap
4. selected claim model
5. work-item identity
6. discoverable state
7. claim/lease/fence
8. duplicate-worker semantics
9. dispatch revalidation
10. retry/unknown preservation
11. crash recovery
12. secret lease point
13. ProviderCall construction owner
14. polling behavior
15. schema/migration
16. mediated API surface
17. hosted-proof reuse
18. implementation map
19. source mutations
20. external actions
21. Public state
22. workspace/index
23. Human-review status
