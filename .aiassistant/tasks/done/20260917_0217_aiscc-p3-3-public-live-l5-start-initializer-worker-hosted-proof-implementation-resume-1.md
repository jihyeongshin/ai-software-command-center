# 작업지시서: P3-3 L5 Start Initializer + Durable Worker + Hosted Proof Implementation Resume

## meta

- task_id: `20260917_0217_aiscc-p3-3-public-live-l5-start-initializer-worker-hosted-proof-implementation-resume-1`
- created_at: `2026-09-17 KST`
- work_type: `SECURITY_RUNTIME_IMPLEMENTATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_HEAD: `96a4029ec3a82c9b2a88b9718732aa0f00ecad20`
- predecessor_blocked_implementation_zip_sha256: `dd53684f56443f68fc8a2d5d945323fbd6ce501a83fe8c43bcee7c6aea58181b`
- accepted_p1_5_extension_result_zip_sha256: `dbc4258feeb474b823f077951bb0004966228f14377d2c00deb8d131d9e93826`
- accepted_worker_design_result_zip_sha256: `c1d0549b017c89d251c283bb6b6cc603a84f33050bd4259ee1d61cd915822ba5`
- accepted_start_design_result_zip_sha256: `c047198743571ed6dd3a99f16f7d43e019843c1439f4a089df7fb3dcd0bc49e2`
- accepted_start_authority: `PUBLIC_LIVE_START_AUTHORITY_V1 / TOPOLOGY_D`

Use the current IDE Executor conversation. No fresh chat is required.

## Human-accepted authority set

All three are now final design authority:

```text
P1_5_PUBLIC_LIVE_SEMANTIC_LIFECYCLE_V1
HUMAN_PROVIDED / ACCEPTED / CLOSED

PUBLIC_LIVE_DURABLE_WORKER_AUTHORITY_V1
HUMAN_PROVIDED / ACCEPTED / CLOSED

PUBLIC_LIVE_START_AUTHORITY_V1 / TOPOLOGY_D
HUMAN_PROVIDED / ACCEPTED / CLOSED
```

Do not reopen these designs.

## mandatory preflight

Verify:

```text
HEAD == 96a4029ec3a82c9b2a88b9718732aa0f00ecad20
index == empty
```

Do NOT require a clean worktree.

The current worktree is expected to contain the cumulative local Public Live candidate.

Before substantive mutation:

1. verify the canonical predecessor 12-file candidate identity;
2. verify the exact two 0032 partial-edit identities;
3. verify the 0054 start-design result ZIP identity:
   `c047198743571ed6dd3a99f16f7d43e019843c1439f4a089df7fb3dcd0bc49e2`;
4. read its exact:
   - `PUBLIC_LIVE_START_AUTHORITY_DESIGN.md`
   - `PUBLIC_LIVE_START_AUTHORITY_DECISION.json`
   - `CURRENT_START_PATH_AND_PRIVILEGE_AUDIT.md`
   - `START_ROLE_GRANT_MATRIX.md`
   - `START_CRASH_RECOVERY_MATRIX.md`
   - `IMPLEMENTATION_RESUME_MAP.md`;
5. verify accepted P1-5 lifecycle and durable-worker design identities.

If any required accepted design artifact is missing or hash-mismatched:

`ACCEPTED_AUTHORITY_ARTIFACT_MISMATCH`

and STOP.

If current predecessor source bytes differ before this Task begins:

`PREDECESSOR_SOURCE_IDENTITY_MISMATCH`

and STOP.

Do not reset/restore the worktree merely to make it clean.

## implementation objective

Complete the accepted Public Live production composition locally:

```text
anonymous ingress
→ checked admission + immutable start candidate
→ private initializer
→ P1 READY/start lifecycle
→ immutable public/work/attempt binding
→ restricted durable worker claim
→ P1-5 semantic/provider lifecycle
→ hosted Luna transport
```

Admission stays disabled in released configuration.

No real provider request is allowed.

# I1 — retain and test 0032 partial edits

Retain unless exact accepted authority requires a correction:

- `src/aiscc/providers/openai_responses.py`
  - strict hosted Luna / exact OpenAI endpoint boundary;
- `src/aiscc/public_live/http.py`
  - exact route-specific CORS preflight pairing.

These are unaccepted until the tests in this Task pass.

# I2 — implement accepted 0018 lifecycle integration

Implement the exact Human-accepted P1-5 Public Live lifecycle extension.

Migration:

`20260916_0018_public_live_execution_integration.py`

or the exact repository-convention name with revision `20260916_0018`.

Required:

- additive only;
- no historical rewrite;
- Public Live semantic/provider projection links to exact P1 operation identity;
- one physical-send truth remains P1-5;
- old rows remain fail-closed/default-safe;
- duplicate physical-operation linkage prevented.

Lifecycle:

```text
one RUNNING P1 attempt
→ PRIMARY
→ optional VERIFY
→ optional CORRECT
→ at most one accepted same-role retry
```

Physical provider lifecycle remains P1-5-owned.

# I3 — implement accepted 0019 durable worker claims

Migration:

`20260917_0019_public_live_worker_claims.py`

or exact repository-convention equivalent.

Implement dedicated durable work/claim/event state with the accepted:

- server-generated worker/process/claim IDs;
- database-clock 15s lease;
- 5s renewal cadence;
- monotonic fencing;
- one active claim per run/work item;
- one active claim per worker when frozen by the accepted design;
- dispatch pin;
- terminal/UNKNOWN/quarantine exclusion;
- deterministic bounded discovery;
- durable recovery events.

Claim remains discovery/ownership coordination only.

It does not grant P1 start/provider/secret authority.

# I4 — implement accepted 0020 start authority

Create additive migration:

`20260917_0020_public_live_start_authority.py`

revision:
`20260917_0020`

down_revision:
`20260917_0019`

Do not add a fourth migration.

If exact implementation unavoidably requires another migration:

`MIGRATION_SCOPE_EXPANSION_REQUIRED`

and STOP.

0020 must implement the exact accepted start-authority design.

## start gate / candidate

Add the monotonic start admission gate epoch and immutable durable start candidate/request/event state.

Only checked Public Live admission may register a start candidate.

Candidate must bind the exact fixed:

- public run ID;
- campaign/admission gate epoch;
- admitted timestamp/deadline;
- `PUBLIC_BOUNDED_LIVE`;
- scenario `stockroom-s1-normal/1.0.0`;
- synthetic repository identity/version from accepted hosted profile;
- provider profile `public-live-luna-v1/1` digest metadata;
- fixed TaskContract ref/version/hash;
- campaign/policy/scenario digests;
- public idempotency/admitted payload hash;
- reservation/slot provenance;
- opaque requester/session provenance where required.

No raw IP/header/prompt/key.

`candidate_id = SHA256(canonical candidate JSON)`.

Unique public run binding.

No backfill of old runs.

## fixed start manifest

Create:

`config/public_live/start-contract.v1.json`

Bind the accepted fixed server-owned contract:

- TaskContract id `aiscc-public-live-stockroom-v1`;
- version `1`;
- accepted synthetic repo/scenario/profile/policy refs;
- execution bounds.

Missing/unregistered/hash mismatch:

`START_CONTRACT_UNAVAILABLE`

A request-supplied digest never creates authority.

# I5 — implement private initializer runtime

Create/complete:

- `src/aiscc/public_live/start_authority.py`
- `src/aiscc/public_live/start_repository.py`
- `src/aiscc/public_live/initializer.py`
- required `bootstrap.py` / `__main__.py` wiring.

CLI:

```text
aiscc public-live-initializer
aiscc public-live-initializer --check
```

Normal command must run one foreground supervised bounded loop.

No HTTP listener.

No provider adapter.

No OpenAI secret resolution.

No owner DB.

No detached task.

No busy loop.

Use bounded deterministic PostgreSQL polling/recovery consistent with the accepted start design.

# I6 — initializer DB role and least privilege

0020 owns the exact accepted capability/login role design:

```text
aiscc_public_live_initializer
aiscc_live_initializer_login
```

Preserve accepted properties:

- capability role NOLOGIN;
- runtime login separate;
- NOSUPERUSER;
- NOCREATEDB;
- NOCREATEROLE;
- NOINHERIT;
- NOBYPASSRLS;
- no schema/table/function ownership;
- no PUBLIC/global/grant-option privilege;
- no SET ROLE to migration/schema owner.

Initializer accesses Live DB only.

No owner DB.

No provider key.

No provider egress.

No DELETE/TRUNCATE.

## exact P1 table scope

The accepted initializer P1 startup scope is exactly:

- `work_runs`
- `transition_requests`
- `transition_evaluations`
- `transition_decisions`
- `execution_attempts`
- `execution_events`

SELECT/INSERT only as frozen.

UPDATE only the exact accepted mutable columns:

```text
work_runs:
workflow_state
state_version
updated_at

execution_attempts:
status
execution_version
latest_event_sequence
causal_state
causal_state_version
updated_at
```

No execution operation/provider-history/evidence/judgment/memory raw writes.

Sequence usage only for the exact required provenance sequences resolved by schema, not guessed broad grants.

# I7 — mediated start DB API

Implement exact bounded initializer functions equivalent to the accepted names:

```text
start_next
start_renew
start_context
start_record_phase
start_finalize_binding
start_halt
start_zero_effects
```

Internal registration:

`start_register_from_admission`

must have no direct runtime EXECUTE grant.

Only checked admission calls it.

Requirements:

- schema-qualified SQL;
- fixed safe search_path;
- no dynamic SQL;
- PUBLIC revoked;
- exact signature grants only;
- exact job lease/process generation validation;
- no arbitrary provider charge/closure mutation.

SQL does not evaluate P1 semantic policy.

Python P1 owners remain semantic authorities.

# I8 — P1-3 READY start context authority

Implement distinct:

`PublicLiveStartContextAuthority`

in the initializer composition only.

It must verify:

- admitted durable candidate;
- fixed manifest;
- exact initializer principal/process;
- exact run/READY version;
- exact repository/scenario resources;
- policy/profile/scenario/gate versions;
- operation fingerprint.

Action:

`START_EXECUTION_CONTROL`

Only authoritative READY is eligible.

No pre-genesis guessed READY permission.

Issue only the exact accepted fresh bounded single-use repository/scenario capabilities.

Do not widen existing RUNNING `PublicLiveContextResourceAuthority`.

# I9 — inert WorkRun genesis

Use current P1-4 owner semantics.

Canonical work ID remains:

`public-live-<public_run_id hex>`

Genesis:

```text
NONE / v0
→ READY / v1
```

through:

```text
TransitionRequest
→ TransitionEvaluation
→ TransitionDecision
→ atomic WorkRun projection mutation
```

No direct RUNNING insert.

No bypass of owner-bound facts.

Stable genesis request ID follows the accepted 0054 design.

Duplicate identical request reuses durable decision.

Identity conflict fails closed.

# I10 — attempt preparation and READY→RUNNING

Implement the accepted ordering exactly.

The final implementation must reuse current P1-5 attempt authority and P1-4 transition authority.

At minimum:

```text
authoritative READY
→ START_EXECUTION_CONTROL admitted
→ P1-5 NOT_STARTED attempt prepared
→ issuer-verified execution-start ref
→ P1-4 READY→RUNNING through normal transition flow
→ P1-5 EXECUTION_STARTED
```

Do not change:

- 9 WorkflowState values;
- 4 ExecutionStatus values.

No caller-supplied approved flag.

No raw direct state mutation outside the existing owner repositories.

# I11 — immutable binding and worker visibility

Implement exactly one immutable binding:

```text
public_run_id
↔ work_run_id
↔ execution_attempt_id
```

Binding only after the accepted start lifecycle is fully established.

Duplicate exact bind is idempotent.

Conflict is fail-closed.

Ordinary worker discoverability requires at minimum:

```text
WorkRun = RUNNING
AND P1 ExecutionStatus = RUNNING
AND immutable binding exists
AND current admission/profile/scenario/budget authority
AND no blocker
AND no UNKNOWN
AND no quarantine
AND no terminal state
```

Worker claim code must never initialize missing P1 state.

# I12 — initializer recovery saga

Implement the exact accepted durable saga/journal semantics.

The start journal/lease is coordination only.

It never overrides canonical P1 truth.

Recovery must cover:

1. registered candidate before WorkRun;
2. READY before attempt;
3. attempt prepared before READY→RUNNING;
4. RUNNING before EXECUTION_STARTED;
5. EXECUTION_STARTED before immutable binding;
6. binding before worker claim;
7. duplicate start;
8. initializer crash/restart;
9. unknown DB commit result;
10. policy/gate change during start.

No heartbeat/journal-phase inference of P1 success.

No worker visibility until full bind.

# I13 — defensive DB constraints / triggers

Implement only the exact structural defenses frozen by 0054.

They may enforce:

- admitted start request identity;
- `PUBLIC_BOUNDED_LIVE`;
- fixed manifest binding;
- genesis READY/v1 structural shape;
- canonical READY→RUNNING projection shape with persisted transition provenance;
- NOT_STARTED attempt creation under READY;
- exact CREATED/STARTED startup events;
- narrow safety failure for zero-effect unbound startup.

They MUST NOT reimplement P1-3 or P1-4 semantic evaluation in SQL.

No broad RLS retrofit for unrelated roles.

# I14 — worker implementation

Complete the already accepted durable worker implementation.

Normal:

`aiscc public-live-worker`

must run actual mediated durable work.

No caller run selector.

No raw initialization DML.

Use accepted:

- candidate window 16;
- acquisition batch 1;
- claim TTL 15s;
- renew 5s;
- empty backoff 1/2/4/cap5s;
- DB failure backoff 1/2/4/8/cap10s;
- recovery scan max16.

No anonymous HTTP.

No owner routes.

Live DB only.

# I15 — P1-5 lifecycle / secret / dispatch

Complete the accepted P1-5 Public Live lifecycle integration.

Required physical ordering must match the accepted design artifacts.

Hard invariants:

```text
missing/blank secret
→ provider calls 0
→ request liability 0
→ no DISPATCH_STARTED
```

Secret only after P1-3/P1-5 authority and single-use lease.

Final claim/fence + state/version/profile/budget/capability revalidation immediately before canonical `DISPATCH_STARTED`.

P1-5 `DISPATCH_STARTED` remains the sole MAY_HAVE_SENT marker.

UNKNOWN remains quarantine/no-blind-retry.

# I16 — strict hosted adapter

Retain/test strict hosted OpenAI boundary:

```text
hosted=True
→ exact hosted Luna profile only
→ exact https://api.openai.com/v1 only
→ loopback denied
→ *.railway.internal denied
→ alternate profile/model/provider denied
```

QA provider double uses a distinct synthetic transport.

Proxy env must not retarget production transport.

Redirects disabled.

# I17 — CORS exact pairing

Retain/test:

```text
OPTIONS /v1/public-live/runs + POST
→ allow

OPTIONS /v1/public-live/runs/{run_id} + GET
→ allow

collection + GET
→ deny

item + POST
→ deny
```

# I18 — executable hosted-l5-proof

`aiscc hosted-l5-proof` must exercise the SAME production initialization/claim/fence/P1 operation authority against:

- isolated proof PostgreSQL;
- synthetic sentinel secret class;
- private/local provider double;
- admission disabled;
- no real key;
- no real OpenAI.

Do NOT fixture-precreate RUNNING WorkRuns.

Proof must execute initializer authority first.

Required proof cases:

- normal initialization;
- duplicate start idempotency;
- stale gate/start denial;
- denied START_EXECUTION_CONTROL;
- crash READY→RUNNING boundary;
- crash RUNNING→EXECUTION_STARTED boundary;
- initializer unavailable;
- worker raw P1 write denied;
- worker cannot claim before immutable binding;
- pre-dispatch crash;
- post-dispatch UNKNOWN/quarantine;
- stale claim fence;
- known closed same-role retry;
- worker restart recovery;
- sandbox/process termination.

Static expectation output is not proof.

# I19 — role/grant negative proof

On task-owned isolated PostgreSQL, prove:

- ingress cannot execute initializer start APIs directly;
- ordinary worker cannot execute start owner APIs;
- ordinary worker raw P1 initialization INSERT/UPDATE denied;
- initializer cannot write provider operation/private history tables;
- initializer cannot access owner DB;
- initializer has no provider secret;
- initializer has no provider egress path in application composition;
- missing/extra dangerous privilege causes startup refusal where accepted.

Do not print passwords/DSNs.

# I20 — migration tests

Use PostgreSQL.

Mandatory:

```text
empty DB → 0018 → 0019 → 0020 → head
PASS

0017 → 0018 → 0019 → 0020
PASS
```

Verify:

- revision chain exact;
- constraints/indexes/functions/triggers/grants;
- idempotent duplicate start;
- concurrent initializers;
- start lease/fence recovery;
- immutable binding;
- no worker visibility before bind;
- concurrent worker claims;
- stale fence denial;
- UNKNOWN exclusion;
- terminal/quarantine exclusion.

No older migration rewrite.

# I21 — lifecycle/start integration tests

Mandatory deterministic tests:

- admitted candidate registration atomic with admission;
- duplicate admitted key -> same candidate/run;
- denied admission -> no start candidate;
- NONE/v0→READY/v1;
- START_EXECUTION_CONTROL only on authoritative READY;
- attempt preparation exact;
- READY→RUNNING canonical P1-4 flow;
- P1-5 EXECUTION_STARTED exact;
- immutable bind;
- crash at every accepted start saga boundary;
- ACK-loss / DB-commit-unknown recovery;
- policy/gate drift fail closed;
- start-owner missing credential/function/grant fail closed;
- no fallback to owner/admin connection.

# I22 — provider/worker semantic tests

Retain all prior mandatory 0032 tests:

- PRIMARY only;
- PRIMARY→VERIFY;
- PRIMARY→VERIFY→CORRECT;
- same-role known-closed retry;
- missing secret zero call/liability/dispatch;
- crash before dispatch;
- crash after dispatch UNKNOWN;
- restart after known response before semantic validation;
- no duplicate operation/send;
- budget liability reconciliation;
- exact four ExecutionStatus unchanged;
- real durable worker loop;
- no caller run selector;
- polling/backoff/shutdown;
- provider-double receipt counts observed;
- hosted adapter deny matrix;
- CORS exactness;
- owner/docs/debug routes absent;
- admission remains disabled.

# I23 — Replay / secret non-exposure

Prove:

- Replay provider/tool/process/network/secret execution exactly zero;
- initializer has no OpenAI secret;
- ingress has no OpenAI secret;
- child/sandbox has no provider secret;
- no key/sentinel/raw prompt/provider Authorization in DB/log/report/response/Replay;
- Live failure never becomes fake Live success.

Never print the sentinel value.

# I24 — complete regression / static / package

Run full repository suite after shared-owner changes.

Previous pre-blocker baseline:

`1487 PASS / 3 existing Windows symlink SKIP / 0 FAIL / 0 ERROR`

Requirements:

- no new unexplained skip;
- no new xfail;
- explain test-count delta;
- Ruff PASS;
- formatter check PASS;
- mypy changed production owners PASS;
- `git diff --check` PASS;
- no-secret scan PASS;
- package/CLI smoke PASS:
  - trusted owner API;
  - Public Live ingress;
  - `public-live-initializer --check`;
  - `public-live-worker --check`;
  - `hosted-l5-proof` safe check mode if provided.

## topology / deployment config boundary

Local source may define the future initializer runtime contract and configuration keys.

It may NOT create or mutate Railway services/resources.

Expected future service name:

`aiscc-public-live-initializer`

Expected future secret/DB variable:

`AISCC_PUBLIC_LIVE_START_DATABASE_URL`

Do not read or require a real production value.

No public port/domain.

# forbidden external actions

Strict:

```text
real OpenAI requests:
0

real key read/export:
0

Railway mutation/deploy/restart:
0

Railway service/database/domain creation:
0

Railway role/grant mutation:
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

# mandatory stop

STOP if:

- HEAD mismatch;
- predecessor source identity mismatch;
- accepted design artifact/hash mismatch;
- implementation requires changing WorkflowState/ExecutionStatus value sets;
- P1-3/P1-4/P1-5 semantic owner is replaced by SQL/caller assertion;
- ordinary worker requires raw P1 initialization DML;
- ingress requires privileged P1 startup credential;
- initializer requires OpenAI key/provider egress/owner DB;
- worker becomes discoverable before immutable binding;
- claim/start lease becomes WorkflowState or provider authority;
- P1-5 `DISPATCH_STARTED` ceases to be the physical ambiguity marker;
- UNKNOWN becomes ordinary retryable/discoverable work;
- migration beyond 0018/0019/0020 is required;
- real provider/key is needed for tests;
- full regression fails after shared-owner changes.

After blocker, only minimal evidence/report/export work is allowed.

# acceptable outcome

Expected:

`HOSTED_PUBLIC_LIVE_START_AND_DURABLE_WORKER_IMPLEMENTED / LOCAL_ACCEPTED_CANDIDATE`

Possible blockers:

- `ACCEPTED_AUTHORITY_IMPLEMENTATION_CONFLICT`
- `ACCEPTED_AUTHORITY_ARTIFACT_MISMATCH`
- `PREDECESSOR_SOURCE_IDENTITY_MISMATCH`
- `MIGRATION_SCOPE_EXPANSION_REQUIRED`

None terminally accepts L5.

# export contract

Create:

`.aiassistant/reports/target/20260917_0217_aiscc-p3-3-public-live-l5-start-initializer-worker-hosted-proof-implementation-resume-1/`

ZIP root MUST contain:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `SOURCE_INVENTORY.json`
- `START_AUTHORITY_IMPLEMENTATION_AUDIT.md`
- `START_ROLE_GRANT_PROOF.md`
- `START_CRASH_RECOVERY_PROOF.md`
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

No changed source byte may be omitted.

# final response

1. result
2. HEAD
3. predecessor candidate identity
4. accepted authority identities
5. changed paths
6. migration 0018
7. migration 0019
8. migration 0020
9. start manifest
10. initializer runtime
11. initializer role/grants
12. start queue/journal/lease
13. P1-3 start authority
14. WorkRun genesis
15. attempt preparation
16. READY→RUNNING
17. P1-5 EXECUTION_STARTED
18. immutable binding
19. worker visibility gate
20. start crash/recovery
21. durable worker claim/fence
22. provider lifecycle/dispatch/secret
23. hosted adapter
24. CORS
25. hosted-l5-proof
26. role/grant negative proof
27. migration/PostgreSQL tests
28. focused integration tests
29. full regression/static/type/package
30. real provider calls
31. external actions
32. Public state
33. workspace/index
34. result ZIP SHA-256
35. next Browser gate
