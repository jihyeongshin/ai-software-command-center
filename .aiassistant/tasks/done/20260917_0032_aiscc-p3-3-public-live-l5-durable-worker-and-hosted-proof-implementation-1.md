# 작업지시서: P3-3 L5 Durable Worker + Hosted Proof Implementation

## meta

- task_id: `20260917_0032_aiscc-p3-3-public-live-l5-durable-worker-and-hosted-proof-implementation-1`
- created_at: `2026-09-17 KST`
- work_type: `SECURITY_RUNTIME_IMPLEMENTATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_HEAD: `96a4029ec3a82c9b2a88b9718732aa0f00ecad20`
- accepted_p1_5_extension: `P1_5_PUBLIC_LIVE_SEMANTIC_LIFECYCLE_V1`
- accepted_p1_5_result_zip_sha256: `dbc4258feeb474b823f077951bb0004966228f14377d2c00deb8d131d9e93826`
- accepted_worker_authority: `PUBLIC_LIVE_DURABLE_WORKER_AUTHORITY_V1`
- accepted_worker_design_result_zip_sha256: `c1d0549b017c89d251c283bb6b6cc603a84f33050bd4259ee1d61cd915822ba5`

Use the current IDE Executor conversation. No fresh chat is required.

## starting-state rule

HEAD must remain:

`96a4029ec3a82c9b2a88b9718732aa0f00ecad20`

The worktree is expected to contain the existing accepted local candidate changes from the 2148/2228/2253 chain.

Do NOT reset, checkout, restore or discard those candidate changes merely to obtain a clean worktree.

Before mutation:

1. recover the exact predecessor candidate source inventory from the canonical 2148/2228/2253 artifacts;
2. verify the current candidate bytes match that predecessor identity;
3. verify index is empty.

If the predecessor candidate identity does not match:

`PREDECESSOR_SOURCE_IDENTITY_MISMATCH`

and STOP.

## accepted authority — do not redesign

The following are now Human-accepted:

### P1-5 lifecycle extension

`P1_5_PUBLIC_LIVE_SEMANTIC_LIFECYCLE_V1`

### durable worker authority

`PUBLIC_LIVE_DURABLE_WORKER_AUTHORITY_V1`

Do not reopen either design in this Task.

If exact implementation proves an unavoidable contradiction with an accepted authority:

`ACCEPTED_AUTHORITY_IMPLEMENTATION_CONFLICT`

and STOP.

## implementation goals

### I1 — P1-5 Public Live lifecycle extension

Implement the accepted versioned extension inside the existing P1-5 provider execution owner.

Required semantics:

```text
one RUNNING P1 attempt
→ PRIMARY
→ optional VERIFY
→ optional CORRECT
→ at most one exact same-role retry
→ terminalize only after semantic pipeline terminal
```

Preserve exact four `ExecutionStatus` values.

Do not add WorkflowState.

Public Live semantic planning/validation remains pure.

Physical provider operation lifecycle remains P1-5-owned.

#### immutable semantic plan

Implement a server-owned immutable semantic plan equivalent to:

`SemanticProviderPlan`

It must bind at minimum:

- run/attempt;
- semantic ordinal;
- role PRIMARY | VERIFY | CORRECT;
- role-specific reasoning effort;
- fixed hosted Luna profile/model/provider;
- normalized local private protocol input/history reference;
- output/token bounds;
- tool plan where applicable;
- retry linkage;
- stable operation fingerprint inputs.

Public/user/Agent input cannot choose provider/model/endpoint/secret or mutate the plan.

#### one physical send = one P1 operation

Every physical provider request is one immutable P1 operation.

A same-role retry is a NEW immutable operation with a new operation ID/ordinal.

Do not reuse operation IDs after terminal/unknown outcomes.

### I2 — additive lifecycle migration `20260916_0018`

Implement the accepted lifecycle linkage as an additive migration.

Use the exact schema names frozen by the accepted P1-5 lifecycle design.

Requirements:

- no destructive rewrite;
- no historical row rewrite;
- Public Live semantic/provider projection links to exact P1 operation identity;
- one canonical physical-send truth remains P1-5;
- old rows remain readable with fail-closed/default-safe interpretation;
- indexes/constraints prevent duplicate physical-operation linkage.

If the exact accepted design did not assign a final table/column name, use the repository's current naming conventions and report the mapping.

Do not combine claim schema into 0018.

### I3 — durable worker claim migration `20260917_0019`

Implement the accepted dedicated durable worker claim architecture.

Must represent the accepted concepts:

- durable work-item identity;
- claim ID;
- worker instance ID;
- process generation ID if frozen separately;
- fencing value;
- claimed_at;
- lease_expires_at;
- heartbeat/renewal timestamp;
- release/recovery reason;
- dispatch pin / post-`DISPATCH_STARTED` no-reclaim state;
- link to exact P1 operation where applicable;
- durable claim/recovery events.

Required DB invariants:

- one active claim per run/work item;
- one active claim per worker where accepted design requires it;
- monotonic/non-reusable fence;
- stale claimant cannot pass final dispatch verification;
- UNKNOWN/quarantined/terminal work is not ordinary discoverable work.

Migration is additive only.

### I4 — mediated durable work-source owner

Implement the accepted mediated repository/service owner.

No raw-table polling from worker code outside the persistence owner.

Required capabilities equivalent to:

```text
claim_next_work(...)
renew_claim(...)
release_claim(...)
verify_claim_for_dispatch(...)
recover_expired_claims(...)
```

Exact names should follow repository conventions.

Required behavior:

- deterministic bounded candidate discovery;
- worker cannot supply arbitrary run ID;
- atomic claim acquisition;
- DB clock for lease semantics;
- TTL 15s;
- renew cadence 5s;
- stale fence fail closed;
- bounded recovery scan;
- crash before dispatch can be safely recovered only from durable facts;
- claim expiry alone never means provider definitely-not-sent.

### I5 — real separately startable `public-live-worker`

Finish R1.

Normal:

`aiscc public-live-worker`

must run the actual supervised durable worker loop.

`--check` may remain a composition-only smoke mode.

Worker requirements:

- foreground supervised loop;
- no anonymous HTTP server;
- no owner Command Center route;
- Live DB only;
- no owner DB binding;
- no caller-supplied run selector;
- acquisition batch = 1;
- candidate window = 16;
- empty queue backoff = 1s → 2s → 4s → cap 5s;
- DB failure backoff = 1s → 2s → 4s → 8s → cap 10s;
- recovery scan max = 16;
- graceful shutdown;
- settle/release only when durable authority allows;
- no detached provider task;
- no busy loop.

### I6 — exact secret / dispatch ordering

Implement the accepted order.

Required safety chain:

```text
semantic plan valid
→ worker claim/fence current
→ WorkRun/execution freshness current
→ P1-3/P1-5 capability current
→ single-use SecretResolutionLease minted/consumed
→ secret resolved only in trusted worker parent
→ request liability/budget reservation where accepted
→ P1 operation prepared
→ final claim/fence + state/version + profile/budget/capability revalidation
→ atomic canonical DISPATCH_STARTED marker
→ adapter send
```

The exact order must match the accepted extension artifacts if they place liability/operation preparation slightly differently; do not invent a conflicting sequence.

Hard properties:

- missing/blank secret => provider calls 0;
- missing/blank secret => request liability 0;
- missing/blank secret => no `DISPATCH_STARTED`;
- secret is never resolved during polling/claim;
- secret never persists in DB/log/report/public projection;
- no lease reuse after restart.

### I7 — canonical dispatch truth

Implement one physical ambiguity truth:

`P1-5 DISPATCH_STARTED`

Public Live `sent_at` / provider-request dispatch indicators become derived/linked projection only.

Crash semantics:

```text
no DISPATCH_STARTED
→ provider send not proven
→ retry/recovery only under accepted known-closed rules

DISPATCH_STARTED + no durable known outcome
→ OUTCOME_UNKNOWN
→ quarantine/reconciliation
→ no blind resend
```

Do not create an independent second send marker with authority.

### I8 — pure ProviderCall builder

Finish the D11 implementation.

Implement one pure server-owned builder:

```text
SemanticProviderPlan
+ accepted local private protocol history
→ ProviderCall
```

Requirements:

- production hosted Public Live => exact hosted Luna profile only;
- fixed `https://api.openai.com/v1`;
- role-specific reasoning effort;
- fixed provider/model;
- exact output/token/tool bounds;
- stable operation fingerprint;
- no DB mutation;
- no secret resolution;
- no budget reservation;
- no dispatch marker;
- no arbitrary endpoint.

### I9 — strict hosted OpenAI adapter

Finish previous R3.

Required:

```text
OpenAIResponsesAdapter(hosted=True)
→ ONLY exact hosted Luna production profile
→ ONLY https://api.openai.com/v1
→ loopback denied
→ *.railway.internal denied
→ alternate model/provider/profile denied
```

QA provider-double traffic must use a distinct synthetic QA transport/adapter.

Do not relax hosted production validation to make QA work.

Proxy environment variables must not silently redirect hosted transport.

Redirects remain disabled.

### I10 — retry semantics

Finish previous R4.

One consistent authority across:

- P1 operation state;
- Public semantic plan;
- proof expectation/report;
- worker recovery;
- tests.

Required:

- definitely-not-sent / conclusively closed failure => retry only when accepted same-role one-retry ceiling permits;
- retry creates new operation;
- retry retains same semantic role/reasoning effort;
- UNKNOWN => no retry before reconciliation;
- missing secret is not a physical provider retry and does not consume physical retry budget unless the accepted design explicitly states otherwise;
- total physical provider requests <= 4/run.

### I11 — semantic continuation / terminalization

After P1-5 records a known physical outcome:

```text
known bounded response
→ Public semantic validation
→ complete
   OR VERIFY plan
   OR CORRECT plan
   OR exact same-role retry when eligible
```

PRIMARY success alone must not prematurely terminalize the P1 attempt if VERIFY/CORRECT remains required.

P1-5 owns physical outcome and final `EXECUTOR_COMPLETED` / `EXECUTION_FAILED`.

Public semantic validator does not mutate WorkflowState.

### I12 — executable `aiscc hosted-l5-proof`

Finish previous R2.

The command must execute the actual production claim/fence/operation/recovery mechanisms against an isolated proof PostgreSQL database and private provider double.

It must be operator-only and unreachable over anonymous HTTP.

Required QA guards:

- unique short-lived proof campaign identity;
- proof DB identity is isolated/non-production;
- synthetic sentinel secret class only;
- provider target is private proof double;
- real OpenAI target denied;
- real `AISCC_OPENAI_API_KEY` presence denied;
- Public admission disabled.

Required modes:

#### pre-dispatch crash

- claim acquired;
- terminate before canonical `DISPATCH_STARTED`;
- provider-double receipts = 0;
- durable state proves not dispatched;
- recovery/retry eligibility derives from accepted authority.

#### post-dispatch crash

- canonical `DISPATCH_STARTED` committed;
- provider-double receipt observed when protocol requires;
- completion withheld/uncertain;
- restart/reconciliation => UNKNOWN/quarantine;
- no rediscovery/blind resend.

#### stale fence

- old claimant denied before secret use/send.

#### known closed failure

- one exact same-role retry only when accepted policy permits.

#### worker restart

- state reconstructed from durable claim/operation events;
- no heartbeat-only inference.

#### sandbox termination

- execute the existing process/sandbox supervisor proof path;
- prove child/container absent OR explicit durable quarantine before release.

No real OpenAI request.

### I13 — CORS exact path/method pairing

Finish previous R5.

Required:

```text
OPTIONS /v1/public-live/runs
Access-Control-Request-Method: POST
→ allow

OPTIONS /v1/public-live/runs/{run_id}
Access-Control-Request-Method: GET
→ allow

collection + GET preflight
→ deny

item + POST preflight
→ deny
```

Do not broaden actual route methods.

### I14 — preserve ingress/identity boundaries

Preserve the already good parts unless a direct dependency requires a narrow change:

- dedicated Public Live ingress composition;
- owner routes structurally absent;
- `RailwayEdgeIdentityAuthority`;
- `proxy_headers=False`;
- `scope["client"]` not authoritative end-user identity;
- `X-Real-IP` release trust gate remains disabled pending hosted proof;
- no guessed Railway CIDR/hop count;
- ingress has no OpenAI secret;
- ingress cannot bind owner DB;
- Replay remains static/zero-execution.

### I15 — safe observability

Durable/internal safe fields may include:

- opaque work ID;
- internal run ref;
- claim ID;
- worker opaque ID;
- fence;
- state/version;
- P1 operation ID;
- semantic role;
- timestamps;
- reason/result codes;
- provider destination class/count.

Must not persist/export:

- raw OpenAI key;
- raw provider Authorization header;
- raw prompt;
- unsanitized provider payload;
- raw public forwarding identity;
- public user-selectable URL/provider/model.

### I16 — tests: migrations / PostgreSQL

Run on PostgreSQL.

Mandatory:

- empty DB → migration head PASS;
- current predecessor head `20260916_0017` → 0018 → 0019 PASS;
- constraints/indexes verified;
- concurrent claim acquisition with >=2 workers;
- stale fence denial;
- expired claim recovery;
- post-dispatch no-reclaim;
- UNKNOWN exclusion;
- terminal/quarantined work exclusion;
- graceful worker restart;
- no duplicate send after recovery.

### I17 — tests: P1-5 lifecycle

Mandatory deterministic fake-transport tests:

- PRIMARY-only happy path;
- PRIMARY→VERIFY;
- PRIMARY→VERIFY→CORRECT;
- same-role known-closed retry;
- missing secret: call 0 / liability 0 / dispatch marker absent;
- crash before dispatch;
- crash after dispatch => UNKNOWN;
- restart after known response before semantic validation;
- no duplicate operation/send after restart;
- budget liability reconciliation;
- exact four ExecutionStatus values unchanged.

### I18 — tests: worker / hosted proof

Mandatory:

- normal worker loop performs actual mediated claim→P1 operation flow;
- no caller run selector;
- 15s lease / 5s renew semantics;
- bounded polling/backoff;
- shutdown;
- provider double receipt counts observed, not hard-coded;
- hosted proof pre/post-dispatch/stale-fence/known-closed/restart modes;
- sandbox termination proof path executes;
- operator proof rejects production DB/real OpenAI configuration.

### I19 — tests: adapter / ingress

Mandatory:

- hosted exact Luna profile accepted with no network send;
- hosted loopback denied before socket;
- hosted Railway-internal fake endpoint denied;
- hosted alternate profile denied;
- non-hosted real OpenAI denied;
- proxy env cannot retarget;
- redirect disabled;
- exact CORS pairings;
- owner routes absent;
- docs/debug absent;
- unknown route default deny;
- admission remains disabled;
- disabled POST produces zero provider work.

### I20 — Replay / secret non-exposure

Prove:

- Replay path provider/tool/process/network/secret execution = 0;
- Live/provider/worker failure does not silently become a fake Live success;
- sentinel secret occurrence count = 0 in prohibited outputs;
- ingress env has no provider secret;
- child/sandbox env has no provider secret;
- no secret in DB rows/logs/responses/reports/Replay.

Never print sentinel value in exported evidence.

## complete regression

Run full repository suite.

Previous local candidate evidence:

`1487 PASS / 3 existing Windows symlink SKIP / 0 FAIL / 0 ERROR`

Requirements:

- no new unexplained skip;
- no new xfail;
- explain test-count delta;
- Ruff PASS;
- formatter check PASS;
- mypy changed production owners PASS;
- `git diff --check` PASS;
- source secret scan PASS without printing values;
- package/CLI smoke PASS for:
  - trusted owner API;
  - Public Live ingress;
  - `public-live-worker`;
  - `hosted-l5-proof`.

## migration ownership

Expected migration order:

```text
current:
20260916_0017

new:
20260916_0018
20260917_0019
```

If repository migration naming rules require a different exact identifier while preserving order, report the exact identifiers and rationale.

Do not create additional migrations unless unavoidable.

If another migration is necessary:

`MIGRATION_SCOPE_EXPANSION_REQUIRED`

and STOP.

## source scope

Keep the implementation narrow.

Likely owners:

- P1-5 provider service/models/authority;
- hosted secret resolver integration;
- P1 persistence repository;
- Public Live provider pipeline/authority;
- Public Live worker;
- hosted proof;
- CLI;
- Public Live HTTP/CORS;
- two migrations;
- direct unit/integration tests.

Do not touch unrelated Command Center UI/state/memory/evidence owners.

## forbidden external actions

Strictly:

```text
real OpenAI requests:
0

real key read/export:
0

Railway mutation/deploy/restart:
0

Railway service/database/domain creation:
0

Railway secret mutation:
0

Cloudflare mutation:
0

Git add:
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

## mandatory stop

STOP if:

- HEAD mismatch;
- predecessor candidate identity mismatch;
- accepted P1-5 or durable-worker design artifact mismatch;
- implementation requires changing WorkflowState or ExecutionStatus value sets;
- P1-5 physical provider lifecycle authority would move into Public Live semantic code;
- raw worker polling would bypass mediated repository authority;
- final dispatch cannot atomically enforce current fence/freshness;
- UNKNOWN would become rediscoverable/retryable;
- secret must be resolved during polling/claim;
- real provider/key becomes necessary for tests;
- migration beyond accepted 0018/0019 scope is required;
- owner DB/public ingress boundary must be weakened;
- complete regression fails after shared-owner changes.

After named blocker, only minimal evidence/report/export work is allowed.

## acceptable outcome

Expected:

`HOSTED_PUBLIC_LIVE_DURABLE_WORKER_IMPLEMENTED / LOCAL_ACCEPTED_CANDIDATE`

Possible blockers:

- `ACCEPTED_AUTHORITY_IMPLEMENTATION_CONFLICT`
- `PREDECESSOR_SOURCE_IDENTITY_MISMATCH`
- `MIGRATION_SCOPE_EXPANSION_REQUIRED`

None terminally accepts L5.

## export contract

Create:

`.aiassistant/reports/target/20260917_0032_aiscc-p3-3-public-live-l5-durable-worker-and-hosted-proof-implementation-1/`

ZIP root MUST contain:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `SOURCE_INVENTORY.json`
- `LIFECYCLE_IMPLEMENTATION_AUDIT.md`
- `DURABLE_WORKER_IMPLEMENTATION_AUDIT.md`
- `CLAIM_FENCE_PROOF.md`
- `HOSTED_PROOF_DRIVER_EVIDENCE.md`
- `PROVIDER_ADAPTER_BOUNDARY_PROOF.md`
- `RETRY_UNKNOWN_OUTCOME_PROOF.md`
- `SECRET_NON_EXPOSURE_PROOF.md`
- `INGRESS_ROUTE_CORS_PROOF.md`
- `REPLAY_INDEPENDENCE_PROOF.md`
- `MIGRATION_PROOF.md`
- `TEST_EVIDENCE.json`
- `LOCAL_START_COMMANDS.md`
- `WORKSPACE_BEFORE.txt`
- `WORKSPACE_AFTER.txt`

Also include EVERY changed source/test/migration/config file under its exact project-relative path.

Do not repeat the earlier export omission.

## final response

1. result
2. HEAD
3. predecessor candidate identity
4. accepted P1-5 extension identity
5. accepted durable-worker authority identity
6. changed paths
7. migration 0018
8. migration 0019
9. lifecycle extension implementation
10. claim/lease/fence implementation
11. real worker loop
12. dispatch/secret ordering
13. canonical dispatch marker
14. ProviderCall builder
15. hosted adapter boundary
16. retry/UNKNOWN semantics
17. hosted-l5-proof execution
18. CORS exactness
19. ingress/owner/DB isolation
20. Replay independence
21. secret non-exposure
22. PostgreSQL/migration tests
23. focused tests
24. full regression/static/type/package checks
25. real provider calls
26. external actions
27. Public state
28. workspace/index
29. result ZIP SHA-256
30. next Browser gate
