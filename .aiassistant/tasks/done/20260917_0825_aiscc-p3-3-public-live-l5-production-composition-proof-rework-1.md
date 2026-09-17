# 작업지시서: P3-3 L5 Production Composition / Proof Rework

## meta

- task_id: `20260917_0825_aiscc-p3-3-public-live-l5-production-composition-proof-rework-1`
- created_at: `2026-09-17 KST`
- work_type: `REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_HEAD: `96a4029ec3a82c9b2a88b9718732aa0f00ecad20`
- reviewed_predecessor_zip_sha256: `35479a09be4edc0f946e06cc163420eb777dfcd5fd1cc506cff647e4afbca24b`
- accepted_designs_reopened: `NO`

Use the current IDE Executor conversation. No fresh chat is required.

## starting state

Do NOT reset/restore the cumulative Public Live candidate.

Expected:

```text
HEAD:
96a4029ec3a82c9b2a88b9718732aa0f00ecad20

index:
empty

current cumulative source inventory:
37 files
```

Before mutation, verify the exact 37-file identity from the reviewed 0217 result.

If mismatch:

`PREDECESSOR_SOURCE_IDENTITY_MISMATCH`

and STOP.

## fixed accepted designs

Do NOT reopen:

- `P1_5_PUBLIC_LIVE_SEMANTIC_LIFECYCLE_V1`;
- `PUBLIC_LIVE_DURABLE_WORKER_AUTHORITY_V1`;
- `PUBLIC_LIVE_START_AUTHORITY_V1 / TOPOLOGY_D`.

This Task fixes implementation non-conformance only.

# R1 — complete real production worker execution composition

Current defect:

```text
aiscc public-live-worker
→ create_worker()
→ execute_claim=None
→ PUBLIC_WORKER_P1_EXECUTOR_REQUIRED
```

Implement a concrete production claim executor under the existing accepted P1-5/Public Live owners.

Normal:

```text
aiscc public-live-worker
```

must run the durable worker loop without an injected test callback.

The production claim executor must implement the accepted chain:

```text
claim context
→ semantic plan
→ P1-5 immutable provider operation
→ exact operation link
→ P1-3/P1-5 provider/secret authority
→ single-use HostedOpenAISecretResolver lease
→ final claim/fence/state/version/budget/profile revalidation
→ canonical P1-5 DISPATCH_STARTED + dispatch pin
→ hosted adapter send
→ P1-5 physical outcome
→ pin closure / UNKNOWN quarantine
→ semantic validation
→ next role / same-role retry / attempt terminalization
```

Requirements:

- `plan_next_semantic_request` has a real production caller;
- `build_public_provider_call` has a real production caller;
- `execution_link_operation` has an exact mediated caller/grant;
- `HostedOpenAISecretResolver` is actually invoked in the production dispatch path;
- no free-form provider/model/endpoint;
- no caller-supplied run selector;
- no raw worker P1 initialization DML;
- no alternate side-effect authority.

If the accepted P1-5 service cannot be extended to own this without a new authority semantic:

`ACCEPTED_AUTHORITY_IMPLEMENTATION_CONFLICT`

and STOP.

# R2 — implement claim renewal and atomic dispatch pin/fence lifecycle

Current defect:

- `worker_renew(...)` exists but foreground worker never calls it;
- accepted cadence 5s is absent;
- `public_worker_dispatch_pin` exists but no production API creates/closes it;
- no final atomic fence hook is connected to `DISPATCH_STARTED`.

Implement the accepted semantics.

## renewal

Before canonical dispatch:

- renew active claim every 5 seconds while long claim-owned work is in progress;
- 15-second DB-clock TTL remains fixed;
- renewal is supervised and scoped to the exact claim;
- no detached/unowned background work;
- renewal failure immediately prevents any new side effect.

After canonical dispatch has entered MAY_HAVE_SENT authority, recovery must rely on dispatch pin/P1 outcome rules, not on heartbeat inference.

## operation bind / pin / close

Add exact mediated APIs, consistent with the accepted D14/E8 design, for concepts equivalent to:

```text
bind_claim_operation(...)
verify_claim_for_dispatch(...)
pin_dispatch_started(...)
close_dispatch_pin(...)
quarantine_claim(...)
recover_expired_claims(...)
```

Names may follow repository conventions.

Hard requirements:

- stale worker/fence cannot create or use provider dispatch authority;
- operation belongs to the claim's bound P1 attempt;
- final state/version/execution_version/profile/budget/capability checks are current;
- canonical P1-5 `DISPATCH_STARTED` remains physical MAY_HAVE_SENT truth;
- dispatch pin and P1 marker must not create independent contradictory truth;
- open pin prevents ordinary release/reclaim/resend;
- known outcome closes pin with exact outcome event/proof;
- unknown keeps quarantine/no-blind-resend semantics.

If the exact transaction cannot atomically preserve P1-5 ownership plus current fence:

`ACCEPTED_AUTHORITY_IMPLEMENTATION_CONFLICT`

and STOP rather than weakening the contract.

# R3 — make hosted-l5-proof genuinely executable

Current defect:

- provider-double URL is validation-only;
- proof never contacts/observes the provider double;
- receipt count comes from static `expectation(...)`;
- sandbox termination still raises `SANDBOX_TERMINATION_REQUIRES_PROCESS_SUPERVISOR`.

Implement the accepted operator proof.

## QA transport

Use a distinct synthetic QA provider transport.

It may target only the accepted private proof endpoint class.

Production hosted OpenAI adapter remains exact OpenAI-only and MUST NOT be loosened.

## observed receipts

The provider double must expose a bounded receipt observation mechanism.

Proof output must derive:

```text
provider_receipts
```

from observed provider-double durable/response state, not from a constant.

Required actual modes:

### before-dispatch

- production initializer path executed;
- production worker claim/fence path executed;
- fault before `DISPATCH_STARTED`;
- observed provider receipts = 0;
- durable definitely-not-sent state.

### after-dispatch

- production dispatch pin + `DISPATCH_STARTED` executed;
- QA provider double observes exactly one request;
- completion deliberately withheld/interrupted;
- restart/reconciliation produces UNKNOWN/quarantine;
- no second receipt / blind resend.

### known-closed-failure

- provider double returns an explicitly closed failure;
- one same-role retry only under accepted ceiling;
- receipts reflect the real attempted sends.

### sandbox-termination

- invoke the existing accepted process/sandbox supervisor;
- execute termination;
- prove child/container absent OR exact durable quarantine;
- do not return a static expectation.

No real OpenAI or real secret.

# R4 — implement/prove least-privilege initializer login runtime

Current defect:

The migration defines:

```text
aiscc_live_initializer_login
  LOGIN
  NOINHERIT

aiscc_public_live_initializer
  NOLOGIN
  NOINHERIT
```

with membership, while production application code does not demonstrate activation of the capability role.

Implement the exact accepted login→capability activation mechanism.

Requirements:

- runtime authenticates as the LOGIN role;
- runtime uses only the accepted initializer capability role for narrow startup operations;
- it never SET ROLEs to migration/schema owner;
- no owner/admin fallback;
- no broad inherited privileges;
- connection/session startup verifies expected `session_user` / `current_user` or exact accepted equivalent;
- drift/missing membership/grant fails startup before P1 mutation.

The worker runtime role must receive equivalent actual-session proof for its own mediated functions.

## mandatory runtime privilege tests

Use real PostgreSQL roles in the task-owned DB.

Prove by actual connection, not `has_*_privilege` metadata alone:

- initializer LOGIN can perform the exact accepted start flow;
- initializer LOGIN cannot write provider operations/private protocol/evidence/judgment/memory;
- initializer LOGIN cannot become migration/schema owner;
- worker login can perform mediated worker claim functions;
- worker login cannot perform raw start/P1 initialization DML;
- ingress login cannot invoke initializer-only APIs.

Do not print credentials/DSNs.

# R5 — enforce current start freshness before every new P1 start side effect

Current defect:

`CanonicalStartOwners.admit_start(...)` uses historical `admitted_at` as the `now` value for P1-3 capability issue/consume.

Replace that with authoritative current time.

Requirements:

- historical `admitted_at` remains provenance only;
- current DB/runtime time is used for deadline/TTL checks;
- current `public_control.start_gate_version` and enabled/incident authority are rechecked;
- current run deadline/reservation/outbox/slot authority is rechecked as required by the accepted start design;
- stale gate/policy/deadline denies BEFORE the next new P1 side effect;
- no expired candidate can mint fresh start capabilities merely because its historical admission time was valid.

Use the existing `start_context(...)` or a narrow accepted extension to return current durable freshness facts.

Do not let caller-provided time become authority.

## recovery

For a start that already has durable earlier P1 state when a later freshness check fails:

- follow the accepted start crash/recovery matrix;
- never infer rollback/success from journal phase;
- never expose it to the worker until immutable bind;
- do not invent a new WorkflowState or ExecutionStatus;
- if safe cleanup cannot be expressed under the accepted authority, fail closed and report exact blocker.

# R6 — result ZIP path contract

The reviewed ZIP used Windows `\` archive member separators for project files.

Next result ZIP MUST use exact POSIX project-relative names:

```text
src/aiscc/...
tests/...
migrations/versions/...
config/public_live/...
```

Do not emit backslash member paths.

Browser must be able to match `SOURCE_INVENTORY.json` paths directly to ZIP member names without normalization.

# mandatory focused tests

Add tests that would have failed the reviewed candidate.

Minimum:

1. normal CLI worker composition:
   - create production worker without injected callback;
   - prove concrete claim executor installed;
   - execute one fake-transport semantic step through production composition;

2. semantic production wiring:
   - PRIMARY;
   - PRIMARY→VERIFY;
   - PRIMARY→VERIFY→CORRECT;
   - same-role known-closed retry;
   - operation link exists for each physical operation;

3. secret:
   - `HostedOpenAISecretResolver` reached only after exact dispatch authorization;
   - missing secret => 0 request liability / 0 `DISPATCH_STARTED` / 0 adapter invocation;

4. renewal:
   - hold pre-dispatch claim longer than 15s under deterministic clock/control;
   - observe 5s renew behavior;
   - competing worker cannot acquire;
   - lost renewal prevents next side effect;

5. dispatch pin:
   - stale fence denied;
   - operation bind + pin created;
   - open pin blocks release/reclaim;
   - known outcome closes pin;
   - unknown remains quarantined;
   - no duplicate send;

6. hosted proof:
   - provider-double URL actually used by QA transport;
   - receipt count actually observed;
   - after-dispatch exactly one receipt;
   - no blind second receipt;
   - sandbox termination executes supervisor path;

7. initializer runtime role:
   - actual LOGIN-role connection succeeds only through accepted capability role;
   - prohibited raw operations fail;

8. start freshness:
   - expired start candidate denied before new P1 side effect;
   - gate version changed after registration denied before next side effect;
   - historical `admitted_at` cannot extend capability validity;

9. normal CLIs:
   - `public-live-initializer --check`;
   - normal initializer loop composition;
   - `public-live-worker --check`;
   - normal worker loop composition;
   - hosted proof check + actual fake proof modes.

# PostgreSQL / migration constraints

Preserve exactly:

```text
20260916_0018
20260917_0019
20260917_0020
```

No fourth migration.

Modify 0018/0019/0020 in the current uncommitted candidate if required; they are not canonical yet.

Do not rewrite any migration <= `20260916_0017`.

If a fourth migration becomes necessary:

`MIGRATION_SCOPE_EXPANSION_REQUIRED`

and STOP.

# complete regression

After focused fixes:

- PostgreSQL 17.6;
- empty DB → head;
- 0017 → 0018 → 0019 → 0020;
- focused Public Live/start/worker/provider tests;
- full repository suite;
- Ruff;
- formatter check;
- mypy changed production owners;
- `git diff --check`;
- package/CLI smoke;
- secret scan.

Predecessor reported baseline:

```text
1496 PASS
3 existing SKIP
0 FAIL
0 ERROR
```

No new unexplained skip/xfail.

Explain test-count delta.

# external actions forbidden

```text
real OpenAI:
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

# acceptable outcome

Expected:

`HOSTED_PUBLIC_LIVE_PRODUCTION_COMPOSITION_REWORKED / LOCAL_ACCEPTED_CANDIDATE`

Possible blockers:

- `ACCEPTED_AUTHORITY_IMPLEMENTATION_CONFLICT`
- `MIGRATION_SCOPE_EXPANSION_REQUIRED`
- `PREDECESSOR_SOURCE_IDENTITY_MISMATCH`
- `LEAST_PRIVILEGE_RUNTIME_CONFLICT`

None terminally accepts L5.

# export contract

Create one result ZIP under:

`.aiassistant/reports/target/20260917_0825_aiscc-p3-3-public-live-l5-production-composition-proof-rework-1/`

Required root evidence:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `SOURCE_INVENTORY.json`
- `PRODUCTION_WORKER_COMPOSITION_PROOF.md`
- `CLAIM_RENEWAL_DISPATCH_PIN_PROOF.md`
- `HOSTED_PROOF_DRIVER_EVIDENCE.md`
- `START_RUNTIME_ROLE_PROOF.md`
- `START_FRESHNESS_PROOF.md`
- `LIFECYCLE_IMPLEMENTATION_AUDIT.md`
- `DURABLE_WORKER_IMPLEMENTATION_AUDIT.md`
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

Also include EVERY cumulative changed source/test/migration/config file relative to HEAD under exact POSIX project-relative ZIP member names.

`SOURCE_INVENTORY.json path == ZIP member name` must be direct string equality for every changed file.

# final response

1. result
2. HEAD
3. reviewed predecessor ZIP identity
4. cumulative source identity
5. R1 production worker composition
6. R2 renewal / dispatch pin
7. R3 hosted proof actual receipt/sandbox result
8. R4 initializer/worker runtime role proof
9. R5 current freshness
10. P1-5 semantic lifecycle wiring
11. secret resolver integration
12. migrations 0018/0019/0020
13. CORS / hosted adapter retained results
14. PostgreSQL proof
15. focused tests
16. full regression/static/type/package
17. ZIP POSIX path validation
18. real provider calls
19. external actions
20. Public state
21. workspace/index
22. result ZIP SHA-256
23. next Browser gate
