# 작업지시서: P3-3 Public Live L4 Accepted Luna Provider Profile Binding

## meta

- task_id: `20260916_0950_aiscc-p3-3-public-live-l4-provider-profile-binding-implementation-1`
- created_at: `2026-09-16 KST`
- work_type: `IMPLEMENTATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `e287117ba021411b82560df0af61901f7a8212bb`
- primary_semantic_owner: `P3-3 Public Live L4 immutable provider profile binding`

Use the current IDE Executor conversation. No fresh chat is required.

## current state

- HEAD: `e287117ba021411b82560df0af61901f7a8212bb`
- L1/L2/L3: `ACCEPTED / CLOSED`
- retention blocker: `RESOLVED`
- L4 provider policy: `HUMAN_PROVIDED / ACCEPTED V1`
- L4 implementation: `ENTRY_AUTHORIZED`
- L5: separate / not selected
- Public admission: `DISABLED`
- Public Live: `NOT_RELEASED`

## controlling authority

Read first:

`.aiassistant/reports/aiscc/20260916_0950_aiscc-p3-3-public-live-l4-provider-profile-v1-accepted.md`

It supersedes the 0930 Terra proposal and frozen L4 two-call limit only in the exact fields stated there.

## exact accepted provider profile

```text
provider:
OpenAI

model:
gpt-5.6-luna

API:
Responses

tier:
default/standard

primary reasoning:
low

conditional semantic verification:
low

bounded correction:
medium

max substantive semantic calls:
3

max retry:
1

max total provider requests:
4

max input/request:
8000 billable tokens

max output/request:
2000

max aggregate substantive output/run:
6000

tool:
stockroom_summary only

max tool dispatch/run:
1

connect timeout:
5s

read timeout:
30s

hard provider-call wall:
35s

run deadline:
90s

fallback:
none
```

Price planning envelope:

```text
<= $0.0044/request
<= $0.0176/run
```

Frozen application budgets unchanged.

## mandatory call-role semantics

Do NOT implement four unconditional calls.

Expected state machine:

```text
PRIMARY_LOW
→ deterministic/application validation

if model semantic verification needed:
    VERIFY_LOW
    → validation

if exact correctable semantic defect:
    CORRECT_MEDIUM
    → validation

known-closed provider failure only:
    one RETRY using the failed logical call's reasoning effort
```

Maximum substantive phases:

`3`

Maximum provider retry:

`1`

Maximum requests:

`4`

Unknown outcome:

`NO BLIND RETRY`

## Phase 1 — current binding audit

Reconfirm exact current owner paths/symbols for:

- ProviderProfile registry;
- OpenAI Responses adapter;
- provider selector;
- token/output/call limits;
- timeout/deadline checks;
- retry/unknown-outcome path;
- tool dispatch constraints;
- Public Live L2/L3 integration point.

Emit:

`L4_BINDING_IMPLEMENTATION_PLAN.md`

before mutation.

## Phase 2 — implementation

Allowed changes only when needed to bind accepted profile:

- immutable/versioned provider profile declaration;
- exact Luna model binding;
- call-role/reasoning policy representation;
- <=3 substantive / <=1 retry / <=4 total guards;
- 8000/2000/6000 token/output guards;
- 5/30/35/90 second guard composition;
- tool dispatch <=1;
- price envelope/profile metadata;
- 24h current-price freshness marker/reference;
- Public Live profile selection fixed to this profile;
- deterministic validation-driven escalation plumbing;
- directly affected tests.

Prefer existing accepted P1-5/P3-3 abstractions. Do not create parallel provider authority.

## escalation guard

`medium` reasoning is permitted only for bounded correction.

It must require an exact server-owned defect classification/validation result.

Public/user input must not be able to request `medium`.

Verifier/correction prompts must remain server-owned bounded scenario messages.

## retry guard

One retry maximum.

Retry only after conclusively known-closed failure.

No retry after unknown outcome.

Retry inherits logical call role and reasoning effort.

Retry cannot expand semantic call ceiling.

## deadline guard

Before starting each provider request, ensure admitted worst-case local hard wall does not exceed remaining 90-second run deadline.

Do not start a call that cannot fit.

## cost guard

Bind accepted conservative price envelope as provider-profile metadata/application admission input.

Do not claim provider-side spend configuration.

Do not raise frozen application budgets.

## provider/account boundary

No real provider call is authorized.

No raw API key read/export.

No billing/project setting mutation.

No broad env/home credential scan.

Tests must use deterministic fake/local provider endpoints/adapters only.

## required evidence

### `PROFILE_BINDING`

- exact provider/model/profile immutable;
- public cannot select/override;
- no fallback.

### `CALL_ROLE_STATE_MACHINE`

Prove:
- happy path uses one low call;
- verification only when deterministic gate requests it;
- correction only after exact defect and uses medium;
- no correction-medium from public input;
- <=3 substantive calls.

### `RETRY`

Prove:
- <=1;
- known-closed only;
- unknown outcome never retried;
- retry inherits effort;
- total provider requests <=4.

### `TOKEN_COST`

Prove:
- 8000 input/request;
- 2000 output/request;
- 6000 substantive output/run;
- accepted price envelope represented;
- no budget increase.

### `DEADLINE`

Prove:
- 5/30/35 limits;
- 90s run deadline;
- new call denied when worst-case wall cannot fit.

### `TOOL_BOUNDARY`

- stockroom_summary only;
- <=1 dispatch/run;
- no arbitrary tool.

### `SECURITY`

- no user provider/model/reasoning selection;
- no credential leakage;
- no real network/provider call;
- no fallback.

### `REGRESSION`

- focused provider-profile tests;
- accepted P1-5 provider runtime tests;
- Public Live L2/L3 tests;
- broader suite as repository harness supports;
- no skip/xfail/assertion dilution.

### `WORKSPACE_INTEGRITY`

- HEAD/index/worktree before/after;
- exact changed paths;
- no commit/push/deploy.

## human/account pending evidence

Executor must explicitly leave pending:

- dedicated API Project reference;
- actual model permission;
- effective project/account RPM/TPM;
- billing health;
- project hard spend limit `$15/month`;
- alerts `$10/$12`;
- scoped credential capability/reference;
- any paid provider verification.

## forbidden

- real paid provider call;
- real credential use;
- billing/account mutation;
- L5 deployment/trusted-proxy work;
- Public admission enablement;
- Git commit/push;
- changing L1/L2/L3 semantics;
- increasing frozen budgets/admission counts.

## acceptable final result

If implementation/tests pass:

`COMPLETED / ACCEPTED_CANDIDATE`

L4 must NOT be claimed terminally accepted because account evidence and later provider verification remain Human-owned.

## mandatory stop

- HEAD mismatch;
- accepted policy missing;
- existing provider architecture cannot express call-role policy without semantic redesign;
- mutation would weaken accepted P1-5 retry/unknown-outcome contract;
- account/credential required to complete non-paid implementation;
- real provider call required;
- L5 dependency required;
- unrelated dirty collision.

## export

Target:

`.aiassistant/reports/target/20260916_0950_aiscc-p3-3-public-live-l4-provider-profile-binding-implementation-1/`

Required root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `L4_BINDING_IMPLEMENTATION_PLAN.md`
- profile/call-role/retry/deadline/cost/security evidence
- changed source/test files preserving relative paths

## Task lifecycle

active:

`.aiassistant/tasks/active/20260916_0950_aiscc-p3-3-public-live-l4-provider-profile-binding-implementation-1.md`

done after report/export:

`.aiassistant/tasks/done/20260916_0950_aiscc-p3-3-public-live-l4-provider-profile-binding-implementation-1.md`

## final response

1. result
2. target bundle
3. accepted profile authority
4. changed files
5. immutable provider/model binding
6. call-role state machine
7. retry/unknown-outcome evidence
8. token/cost/deadline evidence
9. tool/security evidence
10. regression
11. provider calls
12. Public admission before/after
13. account/Human pending evidence
14. workspace integrity
15. unverified
