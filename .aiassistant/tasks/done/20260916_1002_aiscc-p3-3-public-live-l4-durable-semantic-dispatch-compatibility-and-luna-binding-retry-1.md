# 작업지시서: P3-3 Public Live L4 Durable Semantic Dispatch Compatibility + Luna Binding Retry

## meta

- task_id: `20260916_1002_aiscc-p3-3-public-live-l4-durable-semantic-dispatch-compatibility-and-luna-binding-retry-1`
- created_at: `2026-09-16 KST`
- work_type: `REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `e287117ba021411b82560df0af61901f7a8212bb`
- primary_semantic_owner: `P3-3 Public Live durable provider-request orchestration + L4 accepted Luna profile`
- predecessor_task: `20260916_0950_aiscc-p3-3-public-live-l4-provider-profile-binding-implementation-1`

Use the current IDE Executor conversation. No fresh chat is required.

## current state

- branch: `main`
- expected HEAD: `e287117ba021411b82560df0af61901f7a8212bb`
- L1/L2/L3: `ACCEPTED / CLOSED`
- retention blocker: `RESOLVED`
- L4 Human provider policy: `HUMAN_PROVIDED / ACCEPTED V1`
- L4 implementation: `REWORK AUTHORIZED`
- L5: separate
- Public admission: `DISABLED`
- Public Live: `NOT_RELEASED`

## controlling provider policy

`.aiassistant/reports/aiscc/20260916_0950_aiscc-p3-3-public-live-l4-provider-profile-v1-accepted.md`

No Human re-decision is required.

Exact accepted policy:

```text
provider:
OpenAI

model:
gpt-5.6-luna

PRIMARY:
reasoning low

VERIFY:
reasoning low
conditional only

CORRECT:
reasoning medium
conditional only

max semantic calls:
3

max provider retry:
1

max physical provider requests:
4

retry:
known-conclusively-closed failure only

unknown outcome:
no blind retry

input:
<=8000/request

output:
<=2000/request

substantive output:
<=6000/run

tool:
stockroom_summary only
<=1 dispatch/run

connect/read/hard-wall:
5/30/35 seconds

run deadline:
90 seconds

provider/model fallback:
none
```

Frozen `$0.20/run`, `$4/day`, `$15/campaign`, 20 starts/day and concurrency 2 remain unchanged.

## predecessor blocker accepted as valid

The current accepted persistence/runtime does not have a durable representation for successful PRIMARY -> VERIFY -> CORRECT.

The next implementation MUST NOT fake these phases as retries or hide them process-locally.

## Phase C1 — exact migration/runtime topology

Before mutation:

1. verify exact HEAD;
2. verify index/tracked workspace status;
3. inspect Alembic heads/history;
4. require sole canonical current head `20260916_0016`;
5. verify accepted migrations `0013`, `0014`, `0015`, `0016` byte-identical;
6. if any successor/multi-head exists unexpectedly: STOP.

If PASS, create exactly one successor:

`migrations/versions/20260916_0017_public_live_semantic_provider_requests.py`

```text
revision:
20260916_0017

down_revision:
20260916_0016
```

Do not edit accepted migrations.

## Phase C2 — pre-mutation design

Write:

`L4_DURABLE_SEMANTIC_REQUEST_DESIGN.md`

before source mutation.

It must inventory exact current tables/functions/services and choose the narrowest compatible design.

The design MUST preserve:

```text
physical provider request identity
!= logical semantic role
!= retry ancestry
```

### minimum durable information

Each physical provider request or equivalent authoritative record must durably bind at least:

- run/request identity;
- physical request ordinal `1..4`;
- semantic role `PRIMARY | VERIFY | CORRECT`;
- logical semantic sequence ordinal `1..3`;
- reasoning effort, server-derived:
  - PRIMARY -> low
  - VERIFY -> low
  - CORRECT -> medium;
- retry-of physical request, nullable;
- retry attempt indicator/count;
- server-owned trigger/validation authority ref or digest;
- correction defect class/ref or digest when CORRECT;
- request/idempotency fingerprint;
- provider/profile/model version;
- max input/output tokens;
- committed max provider cost;
- admitted remaining run deadline / hard wall;
- dispatch/outcome certainty;
- provider request/response immutable refs when applicable;
- usage truth/unknown-usage state;
- settlement/reconciliation status;
- timestamps using authoritative server/DB time where applicable.

Do not persist arbitrary public prompt text as control authority.

## semantic phase authorization

### PRIMARY

- first semantic role only;
- no Human/public trigger;
- Luna low;
- one logical phase.

### VERIFY

May be admitted only after:

- PRIMARY logical outcome is durably known/completed;
- server-owned deterministic/application validation produced an immutable `verification_required` decision/ref;
- run has not terminally completed provider semantic pipeline;
- call/token/time/cost/tool gates still pass.

Luna low.

### CORRECT

May be admitted only after:

- prior semantic outcome is durably known/completed;
- server-owned validation produced an exact correctable defect class/ref;
- correction is permitted by scenario policy;
- provider semantic pipeline not terminally completed;
- all remaining bounds pass.

Luna medium.

Public/user input cannot directly mint verification/correction authority.

## retry authorization

A retry:

- is NOT a new semantic phase;
- references one exact failed physical provider request;
- retains the same semantic role;
- retains the same reasoning effort;
- retains or narrows token/cost/tool scope;
- consumes the single run-level retry reserve;
- increments physical provider request count;
- is allowed only when predecessor outcome is conclusively known closed/non-side-effecting under accepted provider semantics.

Unknown outcome:

```text
NO RETRY
→ reconciliation / conservative failure path
```

## exact ceilings

Enforce atomically/durably:

```text
logical semantic phases <=3

retry attempts/run <=1

physical provider requests/run <=4

tool dispatch/run <=1

input/request <=8000

output/request <=2000

substantive output/run <=6000

frozen application reservation/budget unchanged
```

Concurrent service instances must not exceed any ceiling.

## Public Live projection compatibility

The old two-dispatch encoding may not prematurely project a successful PRIMARY into final provider-pipeline completion.

The compatibility extension must define an explicit durable provider-pipeline completion decision.

Allowed approach:

- narrow new semantic-provider-request relation and mediated API layered under the existing Public Live run;
- or minimal versioned extension of existing dispatch persistence/functions.

Choose the narrower design after source audit.

Required externally visible semantics:

```text
intermediate PRIMARY/VERIFY success
!= provider semantic pipeline complete
!= GOVERNANCE_PENDING solely because that phase succeeded
```

The main Public Live run may advance to the existing governance-pending semantics only when the server-owned pipeline completion decision is durably satisfied.

Do NOT add a new P1 WorkflowState.

Do NOT let Agent/provider output choose workflow state.

## compatibility with historical rows

Existing rows/runs created under the old two-dispatch contract must remain readable/reconcilable.

Migration/upgrade must not reinterpret historical ordinal 2 rows as VERIFY/CORRECT.

Any new columns on existing relations must use backward-compatible defaults/nullability and explicit new-version guards.

## mediated DB/API boundary

Runtime route/provider code must not get raw table DML privileges.

Use mediated least-privilege DB functions/repository APIs.

Required:

- atomic authorization/insert of physical provider request;
- atomic retry-reserve enforcement;
- atomic semantic sequence enforcement;
- durable outcome recording;
- durable validation/defect gate recording or exact immutable ref binding;
- provider-pipeline completion/finalization;
- reconciliation for unknown/in-flight outcome;
- concurrent cross-instance correctness.

SECURITY DEFINER functions must use safe qualified names / controlled search_path and revoke PUBLIC.

## Phase C3 — accepted Luna provider profile binding

After compatibility substrate exists, bind the already accepted profile through existing P1-5/provider authorities.

Required:

- immutable/versioned profile;
- exact OpenAI/gpt-5.6-luna binding;
- no user override;
- no provider/model fallback;
- role -> reasoning mapping;
- 3+1/4 ceilings;
- token/output/cost/deadline/tool bounds;
- 24h provider-price freshness marker/reference;
- no claim provider hard-spend setting is configured.

## deterministic validation interface

The semantic escalation decision must be server-owned.

Tests may use a deterministic validator fixture.

Required outcome vocabulary must be narrow and versioned, e.g. equivalent semantics to:

```text
COMPLETE
VERIFY_REQUIRED
CORRECTABLE_DEFECT
UNSAFE_OR_UNCORRECTABLE
```

Do not expose arbitrary model-generated free-form text as permission to escalate.

If exact vocabulary already exists, reuse it.

If introducing a new vocabulary, keep it local to Public Live provider-pipeline decision authority; do not create a new P1 WorkflowState.

## deadline rules

Before every physical request:

```text
remaining run time >= admitted hard provider-call wall
```

Otherwise deny new provider request.

Retry and CORRECT are subject to the same check.

Run deadline remains 90 seconds.

## cost/accounting rules

Every physical provider request must bind its maximum provider liability before send.

Use conservative Luna envelope:

`<= $0.0044 / physical request`

But application reservation remains:

`$0.20 / run`

Do not reduce existing reservation unless a future Human policy says so.

Unknown/missing usage remains conservative and may not silently settle to zero.

Four physical requests at planning max:

`<= $0.0176`

is evidence of policy envelope, not provider hard-limit configuration.

## PostgreSQL runtime — explicitly authorized

Do not assume predecessor runtime exists.

Use:

```text
postgres:17.6

local cache only

network pull:
FORBIDDEN

task-owned container/volume

bind:
127.0.0.1:55432

private/pre-existing DB reuse:
FORBIDDEN
```

Emit:

`LOCAL_POSTGRES_RUNTIME.json`

before DB runtime tests.

Cleanup task-owned runtime best-effort after evidence.

## provider test boundary

Real OpenAI/provider network calls:

`0`

Use deterministic fake/local provider endpoints/adapters only.

No real credential or billing/account access.

## required evidence

### `MIGRATION_TOPOLOGY`

- sole pre-head 0016;
- additive 0017 only;
- 0013-0016 unchanged;
- backward-compatible old rows.

### `DURABLE_REQUEST_MODEL`

Prove every physical provider request is independently durable/restart-recoverable and binds semantic role/retry ancestry/limits/outcome.

### `SEMANTIC_SEQUENCE`

Prove:

- PRIMARY low first;
- happy path may complete after PRIMARY;
- VERIFY cannot occur without server validation ref;
- VERIFY is low;
- CORRECT cannot occur without exact defect ref;
- CORRECT is medium;
- Public input cannot trigger semantic escalation;
- logical semantic calls <=3.

### `RETRY_UNKNOWN_OUTCOME`

Prove:

- <=1 retry/run;
- retry same role/effort;
- known-closed only;
- unknown outcome blocks retry;
- restart does not duplicate an uncertain physical request.

### `PHYSICAL_REQUEST_CAP`

Across concurrent independent DB/service instances:

- physical request count <=4;
- semantic phases <=3;
- retries <=1;
- sequence cannot race/bypass.

### `PIPELINE_PROJECTION`

Prove:

- intermediate PRIMARY/VERIFY success does not prematurely finalize the provider pipeline;
- provider pipeline completion is durable/server-owned;
- only completion allows existing governance-pending projection;
- no new WorkflowState invented.

### `PROFILE_BINDING`

- OpenAI / gpt-5.6-luna immutable;
- role -> reasoning effort exact;
- no fallback/public override.

### `TOKEN_COST_DEADLINE_TOOL`

- input <=8000/request;
- output <=2000/request;
- substantive output <=6000/run;
- tool dispatch <=1/run;
- 5/30/35/90 time rules;
- <=$0.0044 physical request planning envelope;
- frozen `$0.20/$4/$15` unchanged.

### `FAILURE_RESTART_RECONCILIATION`

Prove:

- crash/restart after request authorization but before send;
- after send with known outcome;
- after send with unknown outcome;
- after semantic validation before next request;
- no duplicate physical request;
- no blind retry;
- no silent lost liability.

### `SECURITY`

- no raw runtime table DML;
- no provider/model/reasoning user selection;
- no real credential;
- no real provider network;
- no hidden fallback;
- no arbitrary tool.

### `REGRESSION`

At minimum:

- focused semantic-request/profile tests;
- Public Live persistence/service/HTTP tests;
- accepted P1-5 provider runtime tests;
- broader repository suite;
- no skip/xfail/assertion dilution.

Previous accepted baseline:

`1383 PASS / 3 existing SKIP / 0 FAIL / 0 ERROR`

New total must not regress without exact justified blocker.

### `WORKSPACE_INTEGRITY`

- HEAD unchanged;
- index empty before/after;
- exact changed path inventory;
- no commit/push/deploy.

## account/Human evidence remains pending

Do not attempt:

- API Project discovery via secret/local credential scanning;
- actual model permission;
- effective RPM/TPM;
- billing health;
- project hard-spend `$15/month`;
- alerts `$10/$12`;
- scoped real credential capability;
- paid provider verification.

These remain Human/account prerequisites.

## allowed final result

If compatibility + profile binding + evidence pass:

`COMPLETED / ACCEPTED_CANDIDATE`

Do not claim terminal L4 acceptance.

## mandatory stop

- HEAD mismatch;
- migration topology mismatch;
- accepted 0013-0016 changed;
- exact durable semantic model cannot be implemented without broader P1 workflow redesign;
- compatibility requires inventing a new WorkflowState;
- unknown-outcome safety must be weakened;
- provider/account/credential/real call required;
- L5 dependency required;
- cached PostgreSQL unavailable;
- unrelated dirty collision.

## export

Target:

`.aiassistant/reports/target/20260916_1002_aiscc-p3-3-public-live-l4-durable-semantic-dispatch-compatibility-and-luna-binding-retry-1/`

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `L4_DURABLE_SEMANTIC_REQUEST_DESIGN.md`
- `MIGRATION_TOPOLOGY.json`
- `LOCAL_POSTGRES_RUNTIME.json`
- concise sequence/retry/request-cap/projection/profile/cost/restart/security evidence
- changed source/test/migration files preserving repository-relative paths

## Task lifecycle

active:

`.aiassistant/tasks/active/20260916_1002_aiscc-p3-3-public-live-l4-durable-semantic-dispatch-compatibility-and-luna-binding-retry-1.md`

done:

`.aiassistant/tasks/done/20260916_1002_aiscc-p3-3-public-live-l4-durable-semantic-dispatch-compatibility-and-luna-binding-retry-1.md`

## final response

1. result
2. target bundle
3. blocker resolution
4. migration 0017/topology
5. durable physical request model
6. semantic call progression
7. retry/unknown-outcome
8. pipeline projection
9. Luna profile binding
10. token/cost/deadline/tool evidence
11. PostgreSQL/concurrency/restart evidence
12. regression
13. provider calls
14. account/Human pending evidence
15. Public admission before/after
16. workspace integrity
17. unverified
