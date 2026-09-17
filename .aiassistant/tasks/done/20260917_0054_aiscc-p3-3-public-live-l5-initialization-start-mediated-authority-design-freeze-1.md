# 작업지시서: P3-3 L5 Public Live Initialization / Start Mediated Authority Design Freeze

## meta

- task_id: `20260917_0054_aiscc-p3-3-public-live-l5-initialization-start-mediated-authority-design-freeze-1`
- created_at: `2026-09-17 KST`
- work_type: `DESIGN_AUDIT`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_HEAD: `96a4029ec3a82c9b2a88b9718732aa0f00ecad20`
- predecessor_result_zip_sha256: `dd53684f56443f68fc8a2d5d945323fbd6ce501a83fe8c43bcee7c6aea58181b`
- primary_semantic_owner: `Public Live fresh-run P1-3/P1-4/P1-5 mediated initialization authority`
- implementation_authorized: `NO`

Use the current IDE Executor conversation. No fresh chat is required.

## predecessor judgment

Browser accepted the 0032 mandatory stop:

`ACCEPTED_AUTHORITY_IMPLEMENTATION_CONFLICT`

This Task is DESIGN ONLY.

Do not continue migrations/runtime implementation during this turn.

## fixed accepted authorities

Do NOT reopen:

### P1 core

- exact nine WorkflowState values;
- P1-4 sole WorkRun/state_version/TransitionDecision authority;
- TransitionRequest → TransitionEvaluation → TransitionDecision → atomic mutation;
- stale state/version fail-closed;
- idempotent transition request semantics.

### P1-3

- `START_EXECUTION_CONTROL` is the only start admission class in READY;
- normal provider/tool side effects require RUNNING;
- security admission != transition authority;
- caller-created authority facts are not trusted simply because typed.

### P1-5

- exact four ExecutionStatus values;
- P1-5 owns ExecutionAttempt / ExecutionOperation lifecycle;
- execution-start/submission handoff remains issuer/owner controlled;
- secret/provider/tool authority remains separate from WorkflowState;
- unknown outcome no blind retry.

### accepted Public Live extensions

- `P1_5_PUBLIC_LIVE_SEMANTIC_LIFECYCLE_V1`;
- `PUBLIC_LIVE_DURABLE_WORKER_AUTHORITY_V1`;
- dedicated claim tables;
- claim != dispatch authority;
- canonical physical ambiguity marker = P1-5 `DISPATCH_STARTED`;
- ordinary worker gets no raw P1 DML;
- separate Live DB / owner DB isolation;
- worker-only OpenAI secret ownership;
- Public admission remains disabled;
- Public Live remains not released.

## exact current gap to recover

Read exact current source for:

1. `ProductionOwnerAdmission`;
2. `ReconciliationService.bind`;
3. `WorkflowKernel`;
4. `TransitionRepository` / PostgreSQL transition implementation;
5. P1-5 `create_attempt`;
6. P1-5 `transition_attempt`;
7. P1-5 execution-start issuer/authority;
8. P1-3 START_EXECUTION_CONTROL admission;
9. Public Live registration/outbox lifecycle;
10. current accepted P1-5 public mediated API methods;
11. current proposed worker DB roles/grants from accepted worker design;
12. current migration head and role/grant conventions.

Prove the exact fresh-run call path and the exact database writes it currently requires.

Do not rely on the 0032 report alone.

## objective

Freeze one exact production authority path for:

```text
accepted Public Live start candidate
→ P1-3 START_EXECUTION_CONTROL admitted
→ authoritative WorkRun created/bound in READY
→ ExecutionAttempt prepared
→ P1-4 READY → RUNNING admitted
→ P1-5 EXECUTION_STARTED admitted
→ immutable public_run_id ↔ work_run_id ↔ execution_attempt_id binding
→ ordinary restricted worker may later discover/claim work
```

The design must not grant the ordinary worker raw P1 table DML.

## S1 — start-candidate owner

Define who may request a fresh Public Live execution start.

Candidate must originate only from accepted Public Live ingress/admission authority.

Define exact immutable start-candidate fields:

- public run ID;
- fixed scenario/version;
- fixed synthetic repository/version;
- RuntimeMode;
- Task/profile/policy refs;
- requester/session provenance where required;
- budget/idempotency admission refs;
- creation timestamp;
- current admission-gate version.

No caller may provide:

- WorkflowState;
- state_version;
- TransitionDecision;
- ExecutionStatus;
- execution_attempt_id;
- provider/model/secret;
- arbitrary repo/path/command/network destination.

## S2 — exact trusted start owner

Compare and choose exactly ONE production owner model.

At minimum analyze:

### A — ingress-owned application start coordinator

The public ingress process invokes the existing P1-3/P1-4/P1-5 Python owners directly against Live DB using a narrowly scoped start-capable DB credential.

### B — private internal start-broker process/service

A separate private server-side start authority invokes the existing P1 owners with a privileged Live DB role; ingress/worker communicate only through an authenticated bounded internal protocol or durable request.

### C — PostgreSQL mediated start API

The ordinary runtime role receives EXECUTE-only access to narrowly scoped `SECURITY DEFINER` functions/procedures that perform the accepted start lifecycle.

### D — initialization queue / scheduler owner

Ingress durably registers a start request; a dedicated private initializer consumes it under the start-authority role and performs the P1 lifecycle before work becomes worker-discoverable.

You may identify another architecture only if the current repository already contains a more exact accepted owner.

Select exactly one.

Do not select C merely because it is simple: prove how P1-4 evaluation semantics and P1-3 admission remain authoritative rather than being reimplemented or caller-asserted in SQL.

Do not select B/D merely because they isolate privileges: account for new service/network/topology authority and operational complexity.

## S3 — runtime-role matrix

Freeze exact production roles/credentials for all affected processes:

- public ingress;
- start owner;
- durable worker;
- migration owner;
- trusted owner API;
- proof mode.

For each state whether it has:

- Live DB CONNECT;
- table SELECT;
- raw INSERT/UPDATE/DELETE;
- EXECUTE on mediated DB API;
- owner DB access;
- OpenAI secret;
- outbound provider access;
- internal RPC access.

Least privilege required.

The ordinary worker must remain unable to perform raw P1 initialization writes.

## S4 — P1-3 start admission

Define exact `START_EXECUTION_CONTROL` evaluation.

Required:

```text
start candidate
+ authoritative READY/start context
+ current policy/profile/scenario
+ budget/idempotency
→ P1-3 SecurityAdmissionDecision
```

Specify:

- caller/principal;
- exact action/resource;
- capability/grant if applicable;
- freshness source;
- denial behavior;
- provenance.

Start admission must not itself create WorkflowState.

## S5 — WorkRun genesis authority

Freeze how a Public Live WorkRun is authoritatively created.

The design must define:

- stable work_run_id derivation or minting owner;
- initial RuntimeMode;
- initial TaskContract binding;
- initial WorkflowState establishment;
- initial state_version;
- idempotency identity;
- duplicate start request behavior;
- exact append-only provenance.

Do not invent a direct `RUNNING` insert.

## S6 — READY → RUNNING transition

Reuse the canonical P1-4 flow.

Required:

```text
TransitionRequest
→ TransitionEvaluation
→ TransitionDecision
→ atomic state/version mutation
```

Define who issues the request and which owner performs each step.

No caller-supplied "approved=true" shortcut.

Specify transaction/CAS behavior under duplicates and concurrent start attempts.

## S7 — P1-5 attempt preparation/start

Freeze exact order between:

- WorkRun READY;
- `create_attempt`;
- START_EXECUTION_CONTROL;
- READY → RUNNING;
- `EXECUTION_STARTED`.

Reconcile with current source requirements.

Specify:

- when execution_attempt_id is minted;
- what state permits attempt preparation;
- what state permits transition to RUNNING;
- what exact P1-5 event changes ExecutionStatus to RUNNING;
- crash behavior between each step.

Do not change the four ExecutionStatus values.

## S8 — cross-owner transaction boundary

Determine whether the complete start can be one database transaction.

If yes:
- identify exact owners participating;
- identify transaction owner;
- show how existing repositories can share the transaction without privilege leakage.

If no:
- define the durable saga/state machine;
- define every intermediate durable state;
- define idempotent recovery;
- define which intermediate states are discoverable to the ordinary worker (expected: none until fully initialized).

Do not rely on process memory.

## S9 — immutable binding

Freeze the canonical binding:

```text
public_run_id
↔ work_run_id
↔ execution_attempt_id
```

Define:

- table/record owner;
- uniqueness;
- immutable-after-bind rule;
- idempotent duplicate behavior;
- stale/conflict behavior;
- whether the binding is part of 0018, 0019, or an additional required migration.

If an additional migration is truly required, state it explicitly.

Do not silently repurpose unrelated columns.

## S10 — worker visibility gate

Define exactly when a fresh run becomes discoverable to `claim_next_work`.

Required minimum gate:

```text
WorkRun = RUNNING
AND P1 ExecutionStatus = RUNNING
AND immutable binding exists
AND admission/profile/scenario/budget authority current
AND no blocker/unknown/quarantine/terminal condition
```

The claim subsystem may not initialize missing P1 state.

## S11 — crash/recovery matrix

Cover at minimum:

1. after Public run registration, before WorkRun creation;
2. after WorkRun READY, before attempt preparation;
3. after attempt prepared, before READY → RUNNING;
4. after READY → RUNNING, before P1-5 EXECUTION_STARTED;
5. after EXECUTION_STARTED, before immutable binding;
6. after immutable binding, before ordinary worker claim;
7. duplicate ingress/start request;
8. start-owner crash/restart;
9. DB commit result unknown;
10. policy/admission changes during start.

For each specify:

- authoritative durable source;
- recovery owner;
- retry/idempotency rule;
- prohibited inference;
- worker visibility.

## S12 — privilege-failure behavior

Define fail-closed behavior if:

- runtime role lacks required grant;
- mediated function/RPC unavailable;
- owner credential missing;
- start owner unavailable;
- transaction fails;
- role/grant drift detected.

No fallback to raw DML.

No fallback to owner/admin connection.

## S13 — topology compatibility

Explicitly classify selected architecture as:

### compatible

`PUBLIC_LIVE_START_AUTHORITY_COMPATIBLE`

Meaning it fits the already accepted topology without introducing a new load-bearing public/service trust boundary.

### topology extension

`PUBLIC_LIVE_START_AUTHORITY_TOPOLOGY_EXTENSION_REQUIRED`

Meaning a new private service/process/network edge is load-bearing and needs explicit Human acceptance.

Do not hide a topology extension as implementation detail.

## S14 — migration/grant impact

Identify exact future implementation changes.

Classify separately:

- schema migration;
- role/grant SQL;
- application source;
- CLI/service start command;
- tests;
- Railway service/env configuration.

Determine whether accepted `0018` / `0019` remain sufficient.

If an additional migration is required, specify proposed ordering but do not implement it.

## S15 — hosted proof integration

The later `aiscc hosted-l5-proof` must exercise the SAME initialization/start authority.

Define proof cases:

- normal initialization;
- duplicate start idempotency;
- stale start request;
- denied START_EXECUTION_CONTROL;
- crash between READY and RUNNING;
- crash between RUNNING and EXECUTION_STARTED;
- start-owner unavailable;
- restricted worker raw P1 write denied;
- worker cannot claim until initialization fully complete.

No fixture-precreated RUNNING state as substitute.

## S16 — implementation resume map

Produce the exact next implementation map after design acceptance.

It must state:

- which existing 0032 partial edits are retained/retested;
- which P1-3/P1-4/P1-5 owner files change;
- which Public Live files change;
- migration/grant files;
- exact tests;
- expected CLI/service composition;
- whether implementation can resume under the same two accepted lifecycle/worker designs.

## mandatory alternatives table

Create an explicit comparison table for A/B/C/D with:

- authority preservation;
- raw-DML exposure;
- P1-4 semantic reuse;
- new topology;
- egress/network impact;
- crash recovery;
- operational complexity;
- migration/grant impact;
- proofability.

Then select one.

## required design artifacts

Create:

- `PUBLIC_LIVE_START_AUTHORITY_DESIGN.md`
- `PUBLIC_LIVE_START_AUTHORITY_DECISION.json`
- `CURRENT_START_PATH_AND_PRIVILEGE_AUDIT.md`
- `START_AUTHORITY_ALTERNATIVES.md`
- `START_CRASH_RECOVERY_MATRIX.md`
- `START_ROLE_GRANT_MATRIX.md`
- `IMPLEMENTATION_RESUME_MAP.md`
- `DESIGN_CONSISTENCY_CHECK.md`

The main design must cover S1-S16 completely.

## acceptance classification

Return exactly one:

### narrow compatible design candidate

`PUBLIC_LIVE_START_AUTHORITY_DESIGN_COMPLETE / HUMAN_REVIEW_REQUIRED`

### topology change needed

`PUBLIC_LIVE_START_AUTHORITY_TOPOLOGY_EXTENSION_REQUIRED`

### deeper P1 authority conflict

`P1_START_AUTHORITY_BASELINE_EXTENSION_REQUIRED`

Do not call any of these accepted.

## source mutation

FORBIDDEN.

No changes to:

- product source;
- tests;
- migrations;
- config;
- lockfiles.

Do not revert the two existing untested partial edits from 0032.

## external actions forbidden

```text
OpenAI:
0

real key:
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
- predecessor 12-file candidate identity;
- exact 0032 two-file partial-edit identity;
- P1-3/P1-4/P1-5 source owner audit;
- current migration/role/grant audit;
- accepted extension/design identity;
- no-secret scan;
- no source mutation.

No full test suite is required for this design-only Task.

## export

Create:

`.aiassistant/reports/target/20260917_0054_aiscc-p3-3-public-live-l5-initialization-start-mediated-authority-design-freeze-1/`

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `PUBLIC_LIVE_START_AUTHORITY_DESIGN.md`
- `PUBLIC_LIVE_START_AUTHORITY_DECISION.json`
- `CURRENT_START_PATH_AND_PRIVILEGE_AUDIT.md`
- `START_AUTHORITY_ALTERNATIVES.md`
- `START_CRASH_RECOVERY_MATRIX.md`
- `START_ROLE_GRANT_MATRIX.md`
- `IMPLEMENTATION_RESUME_MAP.md`
- `DESIGN_CONSISTENCY_CHECK.md`
- `WORKSPACE_BEFORE.txt`
- `WORKSPACE_AFTER.txt`
- result ZIP

## final response

1. result
2. HEAD
3. exact current gap
4. current start path
5. selected architecture A/B/C/D
6. start-candidate owner
7. runtime-role matrix
8. P1-3 admission
9. WorkRun genesis
10. READY→RUNNING
11. P1-5 attempt/start
12. transaction/saga boundary
13. immutable binding
14. worker visibility gate
15. crash/recovery
16. privilege-failure behavior
17. topology classification
18. migration/grant impact
19. hosted proof integration
20. implementation resume map
21. source mutations
22. external actions
23. Public state
24. workspace/index
25. Human-review status
