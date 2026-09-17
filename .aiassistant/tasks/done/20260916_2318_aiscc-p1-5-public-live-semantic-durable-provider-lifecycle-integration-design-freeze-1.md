# 작업지시서: P1-5 Public Live Semantic ↔ Durable Provider Lifecycle Integration Design Freeze

## meta

- task_id: `20260916_2318_aiscc-p1-5-public-live-semantic-durable-provider-lifecycle-integration-design-freeze-1`
- created_at: `2026-09-16 KST`
- work_type: `DESIGN_AUDIT`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_HEAD: `96a4029ec3a82c9b2a88b9718732aa0f00ecad20`
- predecessor_result_zip_sha256: `904dca55431ed34bc8d1c1e0c97ebda9342f09c74e18679550fdcd2e925abc73`
- primary_semantic_owner: `P1-5 provider/tool execution authority extension for Public Live`
- implementation_authorized: `NO`

Use the current IDE Executor conversation. No fresh chat is required.

## predecessor judgment

Browser accepted:

`P1_5_PROVIDER_AUTHORITY_EXTENSION_REQUIRED`

The 2303 worker-authority design is incomplete and must remain paused at D11.

This Task designs only the missing P1-5/Public Live integration contract.

## fixed authorities that MUST NOT change

Do not add or rename WorkflowState or ExecutionStatus.

Preserve:

```text
ExecutionStatus:
NOT_STARTED
RUNNING
EXECUTOR_COMPLETED
EXECUTION_FAILED

ExecutionStatus != WorkflowState
Judgment != TransitionDecision
AgentOutput != SystemState
EvidenceCandidate != AdmittedEvidence
```

Also preserve:

- P1-4 sole state/version/TransitionDecision authority;
- P1-3 capability/security/secret mediation;
- issuer-backed single-use SecretResolutionLease;
- P1-5 server-owned ProviderProfile / ToolRegistry;
- P1-5 durable operation and recovery authority;
- unknown outcome => no blind retry;
- local private protocol history as continuation authority;
- `store=false`, `background=false`, `stream=false`, `parallel_tool_calls=false`;
- Replay provider/tool/process/network/secret execution = 0;
- Public Live fixed synthetic repo/scenario/provider/model;
- L4 provider policy:
  - PRIMARY low;
  - optional VERIFY low;
  - optional CORRECT medium;
  - semantic calls <=3;
  - same-role retry <=1/run;
  - physical provider requests <=4;
  - no model/provider fallback;
- hosted topology and D8=A;
- Public admission disabled until later release.

If satisfying Public Live semantics requires changing any invariant above:

`P1_5_BASELINE_SUPERSESSION_REQUIRED`

and STOP.

## mandatory source recovery

Read exact current source and rules for:

1. `src/aiscc/providers/service.py`
2. `src/aiscc/providers/models.py`
3. `src/aiscc/providers/authority.py`
4. `src/aiscc/providers/hosted_secret.py`
5. `src/aiscc/persistence/repository.py`
6. `src/aiscc/public_live/provider_pipeline.py`
7. `src/aiscc/public_live/provider_authority.py`
8. `src/aiscc/public_live/luna_profile.py`
9. `src/aiscc/public_live/service.py`
10. `src/aiscc/persistence/public_live.py`
11. migrations `20260916_0017` and existing P1-5 execution migration
12. canonical `AISCC_PROVIDER_TOOL_EXECUTION`
13. canonical `AISCC_SECURITY_SANDBOX`
14. accepted L4 provider policy / real-provider canary plan
15. 2303 `CURRENT_SCHEMA_AND_OWNER_AUDIT.md` and `DURABLE_WORKER_AUTHORITY_DESIGN.md`.

Do not infer lifecycle names or states from memory.

## objective

Freeze one exact lifecycle composition where Public Live semantic planning controls WHAT semantic request is next, while P1-5 continues to own whether and how any provider side effect may occur.

The design must make these boundaries mechanically unambiguous:

```text
semantic plan
!= durable provider operation

durable operation
!= dispatch permission

dispatch permission
!= secret permission

provider outcome
!= semantic validation

semantic validation
!= workflow acceptance
```

## E1 — selected integration architecture

Compare at least:

### A — parameterize/extend `AgentExecutionService`

P1-5 remains the sole durable provider lifecycle owner but accepts a server-owned immutable semantic execution plan and a non-terminal completion policy for Public Live.

### B — new P1-5 `DurableProviderOperationCoordinator`

A narrow shared P1-5 owner sits below Public Live semantic planning and above existing durable repository/adapter primitives. Both generic Agent execution and Public Live use the same operation/dispatch/recovery semantics.

### C — Public Live directly owns P1-5 operation lifecycle

`PublicProviderPipeline` directly creates/reserves/dispatches P1-5 operations.

Analyze and choose exactly one.

C should be rejected unless exact canonical authority proves that P1-5 lifecycle ownership can be delegated without weakening its baseline.

## E2 — semantic plan object

Define a server-owned immutable object equivalent to:

```text
SemanticProviderPlan
```

It must contain only bounded, authoritative fields, for example:

- run/attempt identity;
- semantic ordinal;
- semantic role PRIMARY | VERIFY | CORRECT;
- reasoning effort fixed by role;
- profile ref/version;
- model/provider fixed refs;
- normalized local private protocol input/history ref;
- max output/tokens;
- tool plan;
- retry_of when exact same-role retry;
- stable operation fingerprint inputs.

Public/user/Agent input must not construct or mutate it.

Specify its owner and validation.

## E3 — no-reservation planning

Freeze the rule:

```text
Public Live semantic planning
→ may select next semantic role/request candidate
→ MUST NOT itself reserve money/provider operation or mark dispatch
```

Planning remains pure/non-side-effecting until P1-5 accepts the exact plan and all dispatch guards.

Identify which existing `PublicProviderPipeline` functions must become pure planners versus remain durable semantic record owners.

## E4 — stable cross-layer operation identity

Define one exact relationship among:

- Public Live `(run_id, semantic_ordinal, role, retry_of)`;
- P1-5 `attempt_id`;
- P1-5 `operation_id`;
- Public provider physical ordinal;
- operation fingerprint.

Requirements:

- one physical provider send = one immutable P1-5 operation;
- retry = distinct physical operation, linked to same semantic role;
- no operation ID reuse after unknown/terminal outcome;
- idempotent restart can recover the same operation without minting a duplicate send.

## E5 — operation creation / reservation ordering

Freeze exact ordering.

Required safety property:

- missing/blank secret => provider calls 0;
- missing/blank secret => no provider money reservation / public dispatch liability;
- no provider operation may be considered DISPATCHED until the exact final durable send marker is committed.

Choose exact order among:

1. plan validation;
2. worker claim/fence validation;
3. WorkRun/execution freshness;
4. capability admission;
5. SecretResolutionLease mint/consume;
6. secret resolution;
7. budget reservation;
8. P1-5 operation prepare;
9. final freshness/fence check;
10. durable dispatch-start marker;
11. adapter send.

If a secret must be resolved before some durable PREPARED operation exists, define how restart provenance remains truthful without leaking the secret.

## E6 — secret lifetime

Define:

- when SecretResolutionLease is minted;
- when consumed;
- whether resolved secret may live only in the worker parent stack/frame;
- exactly when it becomes unusable;
- behavior if final dispatch check fails after resolution;
- behavior on crash between resolution and dispatch marker;
- no persistence/log/public projection.

No lease reuse after restart.

## E7 — dispatch marker authority

Select exactly one canonical marker that means:

`remote provider send MAY have occurred`

Do not retain conflicting independent meanings between:

- P1-5 operation dispatch marker;
- `public_dispatch`;
- `public_provider_request.sent_at`;
- public run projection `DISPATCH_STARTED`.

Design whether Public Live records are derived projections from P1-5 or participate atomically in the same transaction.

The final contract must eliminate ambiguity for crash recovery.

## E8 — claim/fence integration point

Even though worker claim D1-D17 is paused, define the integration hook required by the later worker design.

Immediately before the dispatch marker/send, P1-5 must verify:

- claim ID;
- fence;
- current ownership;
- WorkRun state/version;
- execution attempt/version;
- operation fingerprint;
- provider/profile/scenario refs;
- remaining bounds/capabilities.

Design an API/transaction boundary where a stale worker cannot pass a point-in-time check and then send after ownership changes.

Do not finalize claim schema here; define only the required P1-5 extension hook.

## E9 — provider call construction

Define one server-owned builder from accepted SemanticProviderPlan + current local private history into the exact `ProviderCall`.

Requirements:

- hosted Luna profile only for hosted Public Live;
- role-specific reasoning effort;
- fixed model;
- no public-selected endpoint/model/provider;
- exact tool registry contract;
- no arbitrary URL;
- stable fingerprint;
- same input/history authority as restart continuation.

The builder is pure. It must not reserve, dispatch, resolve secret, mutate DB or mark outcomes.

## E10 — provider outcome ownership

P1-5 remains the owner of physical provider operation outcome classification.

Define exact mapping for:

- COMPLETED;
- conclusively closed failure;
- cancelled before side effect;
- timeout/transport unknown;
- malformed provider response;
- local validation failure after a known provider response.

Do not allow Public Live semantic validation to rewrite a physical UNKNOWN into known failure/success.

## E11 — semantic validation after physical outcome

Define sequence:

```text
P1-5 known completed physical response
→ sanitized bounded candidate
→ Public Live validation
→ one of:
   pipeline complete
   VERIFY plan
   CORRECT plan
   same-role retry if exact known-closed retry condition
```

Specify what is durable and which owner writes it.

PRIMARY success alone must not terminalize the attempt if validation requires VERIFY/CORRECT.

## E12 — attempt completion policy

This is load-bearing.

Design how a Public Live P1-5 attempt stays RUNNING across multiple semantic physical operations without violating current P1-5 rules.

Compare:

A. one P1-5 attempt containing multiple sequential provider operations until semantic pipeline terminal;
B. one P1-5 attempt per semantic request;
C. another exact model.

The design MUST preserve:

- no replacement attempt under an already-RUNNING WorkRun if baseline forbids it;
- exact four ExecutionStatus values;
- unknown outcome recovery;
- bounded total calls;
- restart durability.

Choose one.

If this cannot be done without changing P1-5 attempt semantics beyond a narrow extension:

`P1_5_BASELINE_SUPERSESSION_REQUIRED`

and STOP.

## E13 — same-role retry

Freeze exact retry conditions.

Required:

- only conclusively known closed/not-sent eligible outcomes;
- same semantic role + same reasoning effort;
- max one retry/run;
- physical request count <=4;
- retry has a new immutable operation ID/ordinal;
- UNKNOWN is never retryable before reconciliation;
- missing secret is not a paid/provider retry and must not consume the provider retry budget unless canonical policy explicitly says otherwise.

Resolve the prior `retry_allowed` contradiction.

## E14 — budget accounting

Define exactly when:

- run reservation exists;
- request max liability is reserved;
- known actual usage replaces liability;
- unknown retains conservative liability;
- closed-before-send releases request liability;
- semantic continuation checks remaining run/day/campaign bounds.

Do not let semantic planner spend or release money directly.

## E15 — terminalization

Define which owner decides:

- P1-5 `EXECUTOR_COMPLETED`;
- P1-5 `EXECUTION_FAILED`;
- Public Live pipeline completed;
- Public Live unavailable;
- WorkRun workflow transition candidate.

Public Live validation may inform P1-5 completion policy but cannot mutate WorkflowState.

Unknown physical outcome must not yield success terminalization.

## E16 — restart/recovery

Provide a matrix for crashes at least:

1. before secret lease;
2. after lease mint, before resolution;
3. after secret resolution, before request reservation;
4. after reservation/prepared operation, before dispatch marker;
5. after dispatch marker, before send call returns;
6. after provider response received, before durable outcome;
7. after durable outcome, before semantic validation;
8. after semantic validation plans next role;
9. during same-role retry;
10. during final terminalization.

For each:
- authoritative source;
- allowed recovery;
- prohibited inference;
- retry eligibility;
- liability handling.

## E17 — persistence projection relationship

Decide the canonical relationship among P1-5 execution tables and Public Live provider tables.

Choose whether Public Live tables are:

- authoritative semantic projections derived from P1-5 physical operations;
- atomically co-owned in the same transaction boundary;
- another exact relationship.

There must not be two independent sources of truth for send/outcome.

## E18 — migration impact

Identify exact schema changes, if any, needed to:

- link P1-5 operation ID to Public Live provider request;
- defer attempt terminalization;
- record semantic role/validation without duplicating outcome truth;
- support restart/retry.

Do not write the migration.

If existing schema suffices, prove how.

## E19 — API/owner contract

Specify exact production interfaces, inputs, outputs, failure codes and transaction boundaries for:

- plan_next_semantic_request;
- prepare/authorize durable provider operation;
- resolve secret;
- commit dispatch start;
- settle provider outcome;
- validate semantic result;
- plan retry/next role;
- complete/fail execution.

Names may differ to match existing conventions.

State which module owns each interface.

## E20 — worker design unblock contract

Produce an explicit handoff back to the paused D1-D17 worker design.

State exactly which facts become available after this P1-5 extension design is accepted:

- work eligibility predicate;
- operation construction owner;
- final claim/fence hook;
- dispatch marker;
- retry/unknown rules;
- completion policy;
- recovery inputs.

The worker design must then resume rather than be regenerated from scratch.

## E21 — proof contract

Define later deterministic tests for:

- PRIMARY only happy path;
- PRIMARY→VERIFY;
- PRIMARY→VERIFY→CORRECT;
- same-role known-closed retry;
- missing secret no reservation/send;
- stale claim/fence deny;
- crash before dispatch;
- crash after dispatch UNKNOWN;
- restart after known response before validation;
- no duplicate operation/send after restart;
- budget liability reconciliation;
- Replay zero execution.

No real provider call.

## alternatives / final design artifact

Create:

`P1_5_PUBLIC_LIVE_PROVIDER_LIFECYCLE_EXTENSION_DESIGN.md`

Create:

`P1_5_PUBLIC_LIVE_PROVIDER_LIFECYCLE_EXTENSION_DECISION.json`

The design must include:

- current conflict;
- E1-E21;
- selected architecture;
- rejected alternatives;
- state/authority sequence diagrams;
- crash/recovery matrix;
- ownership matrix;
- schema impact;
- implementation map;
- proof map;
- exact supersession statement.

## supersession statement

The output must explicitly classify the result as one of:

### narrow compatible extension

`P1_5_PUBLIC_LIVE_LIFECYCLE_EXTENSION_COMPATIBLE / HUMAN_REVIEW_REQUIRED`

Meaning:
- no WorkflowState/ExecutionStatus/value-set change;
- no transfer of P1-5 side-effect authority;
- no weakening unknown-outcome/no-blind-retry/secret mediation;
- new policy/composition is a versioned P1-5 extension.

### baseline supersession required

`P1_5_BASELINE_SUPERSESSION_REQUIRED`

Meaning the exact current P1-5 baseline cannot support the required semantic lifecycle without changing load-bearing semantics.

Do not hide a supersession as a normal implementation detail.

## source mutation

FORBIDDEN.

Do not change:
- product source;
- tests;
- migrations;
- lockfiles;
- deployment config.

## external actions forbidden

```text
OpenAI requests:
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

## checks

Required:

- exact HEAD;
- index state;
- current source identity;
- migration head;
- design consistency against P1-3/P1-4/P1-5/L4;
- no-secret scan;
- no source mutation.

No full test suite is required for this design-only Task.

## export

Create:

`.aiassistant/reports/target/20260916_2318_aiscc-p1-5-public-live-semantic-durable-provider-lifecycle-integration-design-freeze-1/`

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `P1_5_PUBLIC_LIVE_PROVIDER_LIFECYCLE_EXTENSION_DESIGN.md`
- `P1_5_PUBLIC_LIVE_PROVIDER_LIFECYCLE_EXTENSION_DECISION.json`
- `CURRENT_PROVIDER_LIFECYCLE_CONFLICT_AUDIT.md`
- `DESIGN_CONSISTENCY_CHECK.md`
- `IMPLEMENTATION_MAP.md`
- `WORKER_DESIGN_RESUME_HANDOFF.md`
- `WORKSPACE_BEFORE.txt`
- `WORKSPACE_AFTER.txt`
- result ZIP

## final response

1. result
2. HEAD
3. current conflict
4. selected integration architecture
5. semantic plan authority
6. operation identity
7. reservation/secret/dispatch ordering
8. dispatch marker owner
9. claim/fence hook
10. provider call builder
11. outcome owner
12. semantic validation sequence
13. attempt completion policy
14. retry policy
15. budget accounting
16. terminalization
17. crash/recovery matrix
18. persistence relationship
19. schema impact
20. API/owner contract
21. worker-design resume contract
22. proof contract
23. supersession classification
24. source mutations
25. external actions
26. Public state
27. workspace/index
28. Human-review status
