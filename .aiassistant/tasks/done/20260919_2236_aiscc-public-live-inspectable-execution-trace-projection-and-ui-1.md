# 작업지시서: Public Live Inspectable Execution Trace Projection + UI

## meta

- task_id: `20260919_2236_aiscc-public-live-inspectable-execution-trace-projection-and-ui-1`
- created_at: `2026-09-19T22:36:00+09:00`
- work_type: `BACKEND_IMPLEMENTATION / FRONTEND_IMPLEMENTATION / COMPETITION_UX_ENHANCEMENT`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `b821b1ed677ad6d8b93ab1d6b5090218471bd925`
- primary_semantic_owner: `Browser Command Center`
- fresh_ide_chat_required: `No`
- exact_baseline: `b821b1ed677ad6d8b93ab1d6b5090218471bd925`
- expected_migration_head_at_entry: `20260919_0027`
- expected_new_migration_if_required: `20260919_0028`
- L8_status: `CLOSED / MUST_REMAIN_CLOSED`
- Public_Live_entry_state: `RELEASED`
- public_control_entry_state: `TRUE`
- public_run_authority: `NONE`
- real_provider_call_authority: `NONE`
- manual_provider_call_authority: `NONE`
- provider_retry_resend_authority: `NONE`
- provider_worker_execution_contract_change_authority: `NONE`
- admission_contract_change_authority: `NONE`
- backend_read_projection_change_authority: `YES / NARROW`
- frontend_live_trace_change_authority: `YES`
- DB_migration_authority: `ONE_ADDITIVE_0028_IF_REQUIRED`
- raw_table_grant_authority: `NONE`
- Cloudflare_deploy_authority: `YES / EXACT_CHANGED_FRONTEND`
- Railway_ingress_deploy_authority: `YES / EXACT_CHANGED_READ_PROJECTION`
- Railway_worker_mutation_authority: `NONE`
- public_control_mutation_authority: `NONE_UNLESS_SECURITY_OR_CURRENT_RELEASE_SAFETY_REQUIRES_FAIL_CLOSED`
- Human_browser_QA: `HUMAN_OWNED / AFTER_BROWSER_REVIEW`

## 현재 상태

- current canonical baseline: `b821b1ed677ad6d8b93ab1d6b5090218471bd925`
- predecessor cycle: `20260919_2231_aiscc-p3-3-l8-public-live-terminal-closure-1.cycle.md`
- P3-3 / L8: `CLOSED`
- Public Live: `RELEASED`
- frontend Live config: `enabled=true`
- current migration: `20260919_0027`
- known dirty workspace: `none expected`
- open blocker: `none`
- UX issue:
  - current public projection returns `result=null`;
  - frontend therefore displays `No bounded public result is available yet.` even for `COMPLETED`;
  - actual durable execution trace is not visible to judges.

## 이번 턴 목표

1. Define and implement one additive, safe, capability-scoped Public Live inspectable result/trace projection.
2. Expose only allowlisted durable execution facts; never raw provider/private protocol bodies.
3. Render the Live trace in the existing Bounded Live right column using the same visual language as Recorded Replay.
4. Preserve the current single fixed Live scenario; do not create a Live scenario-card catalog.
5. Keep all provider/worker/admission/reconciliation contracts unchanged.
6. Deploy the additive frontend + read projection while preserving the already released Public Live state.
7. Stop for Browser review; actual public visual/Live trace verification remains Human-owned.

## 이번 턴 비목표

- P3-3/L8 reopen.
- New release attempt.
- New public run.
- Real provider call.
- Provider prompt/model/tool redesign.
- Raw final model text publication.
- Human acceptance automation.
- Replay corpus redesign.
- General Command Center UI redesign.

## 허용 범위

allowed_paths:
- `src/aiscc/persistence/public_live.py`
- `src/aiscc/persistence/public_live_limits.py`
- `src/aiscc/public_live/http.py` only if additive response contract plumbing is necessary
- `migrations/versions/20260919_0028_*.py`
- focused Public Live persistence/read-projection tests
- focused HTTP projection tests
- `public/replay/assets/app.js`
- `public/replay/assets/*.css` or exact existing stylesheet used by the page
- `public/replay/index.html` only if semantic markup is required
- `public/replay/PUBLIC_REPLAY_BUILD_MANIFEST.json`
- directly affected replay/live source tests
- supplied governance lifecycle files

allowed_actions:
- inspect exact current public read contract and durable P1-5 evidence tables/functions;
- add one narrow mediated read projection function;
- add one additive response result contract;
- render safe Live trace;
- apply migration 0028 if used;
- deploy changed frontend and ingress;
- focused static/unit/integration/runtime read-projection verification;
- read-only hosted DB verification through authorized existing access;
- fast-forward Git commit/push.

## 절대 금지

forbidden_paths:
- provider adapter/profile behavior except read-only audit
- worker execution semantics
- worker claim/renewal logic
- admission/start semantics
- 0025/0026/0027 behavior
- unrelated Recorded Replay scenario content
- unrelated application modules

forbidden_actions:
- new Public Live POST/run
- real provider call/canary
- provider resend/retry
- raw OpenAI request/response export
- raw model output publication
- reasoning publication
- provider secret read/export
- read capability/idempotency-key export
- DB DSN/password export
- new DB login
- raw table DML grant
- direct public table access from frontend
- weakening Origin/edge identity/capability checks
- changing `public_control` in normal path
- disabling Live merely to perform this UX enhancement
- L8 reopen
- unrelated source/test broadening
- amend/rebase/force push

## 읽을 문서

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- `.aiassistant/reports/aiscc/20260919_2231_aiscc-p3-3-l8-public-live-terminal-closure-judgment-1.md`
- `.aiassistant/reports/aiscc/20260919_2231_aiscc-browser-command-center-p3-3-l8-terminal-closure-handoff-1.md`
- `.aiassistant/records/aiscc/cycles/20260919_2231_aiscc-p3-3-l8-public-live-terminal-closure-1.cycle.md`
- current source listed below

## agent instruction transport / authority

- repository-root instruction entrypoint는 transport bootstrap이며 policy authority가 아니다.
- Task must-read list는 minimum authoritative context set이다.
- unrelated rules/records/logs를 bulk-read하지 않는다.
- active Task / canonical rule / current source / accepted terminal evidence가 충돌하면 구현을 중단한다.
- L8 CLOSED authority를 이 UX task가 재해석하거나 reopen하지 않는다.
- human browser evidence를 executor-completed로 주장하지 않는다.

## 조사할 source

Mandatory exact audit:
- `src/aiscc/persistence/public_live_limits.py::PublicLiveLimits.read`
- current public run lock/read DB API used by that method
- `src/aiscc/public_live/http.py` GET projection path
- `src/aiscc/public_live/worker.py::_execute_production_claim`
- `src/aiscc/providers/service.py` durable provider/tool operation completion refs
- `src/aiscc/public_live/stockroom_runtime.py`
- `src/aiscc/providers/local_deterministic.py::STOCKROOM_SUMMARY`
- `migrations/versions/20260919_0027_public_live_successful_execution_reconciliation.py`
- `public/replay/assets/app.js::validateProjection`
- `public/replay/assets/app.js::renderLiveProjection`
- existing replay/live CSS and responsive rules

## 구현 범위 A — Public safe projection contract

Current top-level GET contract remains additive and capability-scoped.

Do not change:
- run ID format;
- capability validation;
- Origin handling;
- existing top-level state/timestamps/mode/scenario fields.

Replace terminal `result=null` behavior with an allowlisted `result` object when durable execution evidence exists.

Preferred schema:

```json
{
  "schema": "AISCC-PUBLIC-LIVE-INSPECTABLE-RESULT-V1",
  "workflow_state": "EXECUTOR_COMPLETED",
  "evidence_status": "ADMITTED",
  "summary_text": "Bounded execution completed from durable fixed-scenario evidence.",
  "instruction": {
    "authority": "SERVER_OWNED",
    "text": "Produce the bounded Stockroom summary."
  },
  "trace": [],
  "stockroom": null,
  "human_boundary": {
    "state": "NOT_PERFORMED",
    "statement": "Successful AI execution does not become Human acceptance automatically."
  }
}
```

Exact naming may be refined if current contract conventions require it, but:
- schema must be versioned;
- public fields must be exact/allowlisted;
- frontend validation must remain strict;
- raw/private bodies are never exposed.

## 구현 범위 B — trace semantics

The trace is durable-evidence-driven, not frontend-inferred.

It must support the currently authorized semantic variants, not only the observed fifth run.

### Instruction step

Always allowed only for the exact fixed scenario/profile:

```text
kind: INSTRUCTION
authority: SERVER_OWNED
text: Produce the bounded Stockroom summary.
status: COMPLETED
```

Do not expose the full internal system/developer prompt bundle.

### Provider steps

Project from durable provider operation + public semantic link.

Public-safe fields may include:
- ordered public ordinal;
- kind `PROVIDER`;
- semantic role `PRIMARY | VERIFY | CORRECT`;
- coarse status mapped from durable operation phase/outcome;
- safe action code such as:
  - `APPROVED_TOOL_REQUESTED`
  - `BOUNDED_SUMMARY_PRODUCED`
  - `DEFINITELY_NOT_SENT`
  - `OUTCOME_UNKNOWN`
- approved tool name only when durable evidence proves the tool request/continuation relationship.

Do not expose:
- operation_id;
- event_id;
- request/response hashes unless Browser specifically needs them;
- raw prompt;
- raw response;
- raw error text.

### Tool step

Only exact approved tool:

`stockroom_summary`

Public-safe fields:
- kind `TOOL`;
- tool name;
- coarse durable status;
- no capability/ref identity.

### Execution step

Project:
- `EXECUTOR_COMPLETED` when durable attempt says so;
- otherwise a narrow public-safe running/failed state.

Do not convert Executor completion into WorkRun/Human acceptance.

### Public projection step

Project:
- public run state;
- reservation state if safe;
- slot/outbox/work closure only as coarse labels;
- do not expose money ledger internals unless already explicitly public. Cost is not needed for this UI.

### Human boundary

Always explicit and server-owned:

```text
state: NOT_PERFORMED
statement: Successful AI execution does not become Human acceptance automatically.
```

Do not infer Human acceptance from `COMPLETED`.

## 구현 범위 C — safe Stockroom facts

The public demo should show the synthetic fixed-tool facts when, and only when, durable evidence proves the exact approved tool completed with the canonical fixed result.

Expected safe facts:

```text
BOX-A
on_hand 12
reserved 2
available 10
needs_reorder false

BOX-B
on_hand 5
reserved 5
available 0
needs_reorder true

BOX-C
on_hand 4
reserved 1
available 3
needs_reorder true

total_available 13
```

Required proof gate:
- exact tool resource identity;
- `TOOL_COMPLETED`;
- exact durable result hash matches canonical `STOCKROOM_SUMMARY`;
- no UNKNOWN tool outcome.

Do not return the private stored tool body.

The projection may emit a server-owned safe reconstruction of the fixed synthetic facts only after the durable result-hash gate passes.

Add a test that the expected public safe reconstruction and canonical `STOCKROOM_SUMMARY` cannot silently drift.

If a trustworthy drift check cannot be built without importing runtime application code into an Alembic migration, keep the migration static and enforce the cross-check in source/integration tests.

## 구현 범위 D — migration 0028 / mediated read authority

Preferred new revision:

`20260919_0028`

Suggested purpose:

`public_live_inspectable_execution_projection`

Before creating it, audit whether an existing exact safe read authority already supports this projection.

If not, create one narrow function such as:

`public_live_api.inspectable_execution_projection(bytea) RETURNS jsonb`

Requirements:
- `SECURITY DEFINER`;
- fixed `search_path=pg_catalog`;
- exact run/scenario/profile ownership checks;
- return only allowlisted JSON;
- no raw provider/tool/private protocol body;
- no secret/capability;
- no arbitrary error text;
- no raw internal identifiers required by UI;
- PUBLIC execute revoked;
- grant only to `aiscc_public_live_ingress` unless a narrower existing role is proven;
- no table grant expansion;
- no new login.

The existing capability-scoped GET must authorize the read first, then obtain this safe projection.

Do not create a new unauthenticated trace endpoint.

## 구현 범위 E — nonterminal behavior

The UI must remain truthful during polling.

Rules:
- do not invent future steps;
- show only the fixed instruction plus durable operation steps currently present;
- missing durable operation = not rendered, not assumed complete;
- in-progress durable operation may map to a coarse safe `RUNNING`/`DISPATCHED` state;
- UNKNOWN may be shown only as coarse `OUTCOME_UNKNOWN`;
- no raw failure details.

If no execution attempt/evidence exists yet, `result` may remain null and frontend should render:

`Waiting for durable execution evidence…`

not:

`No bounded public result is available yet.`

## 구현 범위 F — Live UI

Do NOT add Live scenario-selection cards.

Keep the current two-column Bounded Live layout.

Left:
- existing Fixed public scenario card unchanged in meaning.

Right:
1. existing Live session / Server status;
2. new `Live execution trace`;
3. trace step cards;
4. explicit Human decision boundary.

Use the same visual language as Recorded Replay:
- compact numbered badges;
- clear state badges;
- bordered cards;
- readable hierarchy;
- no decorative dashboard excess.

Expected conceptual sequence:

```text
01 · INSTRUCTION
Server-owned instruction
COMPLETED

02 · PROVIDER
PRIMARY
COMPLETED
Approved tool requested: stockroom_summary

03 · TOOL
stockroom_summary
COMPLETED
<safe Stockroom table>

04 · PROVIDER
PRIMARY / continuation
COMPLETED
Bounded summary produced

05 · EXECUTION
EXECUTOR_COMPLETED

06 · PUBLIC PROJECTION
COMPLETED
Evidence admitted / terminalized

Human decision
NOT PERFORMED
AI execution != Human acceptance
```

The renderer must support legitimate variants:
- provider-only successful completion;
- tool path;
- VERIFY/CORRECT roles;
- definitely-not-sent retry ancestry;
- safe failure/UNKNOWN status.

Do not hard-code `exactly 2 provider calls` as the rendering contract.

## 구현 범위 G — public summary text

Do NOT publish raw provider final text in this task.

`summary_text` must be a deterministic server-owned public summary derived from safe state, for example:

- running: `Durable bounded execution evidence is being recorded.`
- completed: `Bounded execution completed from durable fixed-scenario evidence.`
- failed/unknown: a coarse safe statement matching public state.

The UI may say `Bounded summary produced` as an execution event, but it must not present private raw model prose.

## 구현 범위 H — strict frontend validation

Update `validateProjection()` or equivalent with:
- exact schema;
- exact allowed keys;
- bounded arrays;
- bounded strings;
- enum allowlists;
- Stockroom item exact SKU set and integer/boolean ranges;
- no unknown fields;
- no unbounded recursive object.

Malformed trace/result:
- fail closed for Live detail;
- Recorded Replay remains usable;
- no automatic new run.

## 구현 범위 I — tests

### backend/persistence

Required PostgreSQL-backed integration coverage:

1. capability-scoped read still denies bad capability.
2. result absent before execution evidence is available.
3. exact provider-only successful trace.
4. exact provider→tool→provider successful trace.
5. VERIFY/CORRECT semantic roles project safely if constructible under current policy.
6. definitely-not-sent retry ancestry projects safely.
7. UNKNOWN projects coarse status only.
8. raw error/request/response/protocol fields absent.
9. completed fixed tool with canonical hash emits exact safe Stockroom facts.
10. wrong tool resource identity denies Stockroom safe facts.
11. wrong/mismatched result hash denies Stockroom safe facts.
12. no table grant expansion.
13. PUBLIC execute revoked.
14. ingress role only for new projection function.
15. migration 0025/0026/0027 behavior unchanged.
16. migration chain through 0028 green.

### frontend

Required source tests:
- old backend `result=null` remains renderable;
- new exact result schema renders;
- malformed/extra fields rejected;
- trace order is server-provided/validated and bounded;
- Stockroom table renders exact safe facts;
- Human boundary always visually distinct;
- terminal `COMPLETED` no longer renders `No bounded public result is available yet.`;
- Recorded Replay catalog/detail regression PASS;
- Live retry/idempotency behavior unchanged.

### static

- Ruff PASS
- format PASS
- narrow mypy PASS
- `git diff --check` PASS
- no new skip/xfail in changed-path tests
- secret-safe export scan PASS

Do not broaden to unrelated historical suites merely to make a global green claim.

## 구현 범위 J — deployment without new Live run

### pre-deploy

Re-prove:
- `HEAD == origin/main == b821b1ed677ad6d8b93ab1d6b5090218471bd925` at task start;
- Public Live currently released;
- public_control true;
- current frontend live enabled;
- ingress healthy;
- held 0 / slots free / no claim/pin;
- 0025/0026/0027 candidates 0;
- no unexpected active run.

### commit

Use fast-forward commits only.

Recommended:
- source/migration/frontend in one reviewed implementation commit;
- governance lifecycle commit after deployment evidence if needed.

No amend/rebase/force.

### frontend first

Deploy the new frontend before backend projection.

It MUST remain compatible with current backend `result=null`.

Verify:
- public page reachable;
- Live still configured/enabled;
- Recorded Replay works by source/static proof;
- no new run/provider call.

### migration / ingress

Apply migration 0028 if created.

Deploy only the changed public ingress/read-projection source.

Do not intentionally redeploy worker.

If platform passively redeploys unchanged services:
- record it;
- verify worker public domain remains 0;
- no provider call/run;
- changed-path source bytes remain correct.

### hosted read-projection proof

Do not create a new public run.

Use the already completed fifth release/Human QA run selected by strict durable predicates, not copied ID alone, to evaluate the new safe DB projection internally.

Verify the resulting JSON:
- exact schema;
- instruction;
- provider/tool/provider trace as durable truth permits;
- safe Stockroom facts;
- execution terminal state;
- public terminal state;
- Human boundary;
- no raw/private fields.

Do not bypass capability-scoped public HTTP to claim Human/public browser proof.

Internal DB projection proof is only backend runtime evidence.

### post-deploy

Prove:
- Public Live remains RELEASED;
- control remains true;
- frontend remains Live enabled;
- ingress healthy;
- no new run;
- no provider call;
- held 0;
- slots free;
- open claim/pin 0/0;
- candidate sets empty;
- provider secret boundary unchanged.

## workflow transition expectation

- initial_state: `L8_CLOSED / PUBLIC_LIVE_RELEASED / TRACE_UX_NOT_IMPLEMENTED`
- expected_non_terminal_state_when_human_pending: `TRACE_IMPLEMENTED_DEPLOYED / HUMAN_QA_PENDING`
- expected_terminal_candidate: `TRACE_ENHANCEMENT_ACCEPTED`
- transition_authority: `SYSTEM for implementation evidence / HUMAN for browser QA / Browser Command Center for judgment`
- Agent가 직접 terminal state를 결정할 수 있는가: `No`

## evidence contract

executor_required:
- channel: `STATIC_SOURCE`
  scope: exact projection contract, migration ACL, frontend renderer
  allowed_command_or_environment: repository-local audit
  pass_condition: allowlisted projection and no forbidden exposure
- channel: `INTEGRATION_TEST`
  scope: PostgreSQL safe projection + capability read + migration chain
  allowed_command_or_environment: existing disposable PostgreSQL harness
  pass_condition: required changed-path tests pass
- channel: `FRONTEND_SOURCE_TEST`
  scope: strict result validation + trace rendering + Replay regression
  allowed_command_or_environment: repository-local tests
  pass_condition: exact new/old contracts pass
- channel: `DATABASE_RUNTIME`
  scope: hosted 0028 migration/ACL + safe projection of an existing completed run
  allowed_command_or_environment: existing authorized hosted read/migration path
  pass_condition: exact safe JSON, no raw/private fields
- channel: `HTTP_RUNTIME`
  scope: ingress health/current released configuration only
  allowed_command_or_environment: existing released public ingress
  pass_condition: healthy; no new run/provider call
- channel: `PUBLIC_PROVENANCE`
  scope: Git commits + deployment/source identity
  allowed_command_or_environment: GitHub/Railway/Cloudflare existing project
  pass_condition: fast-forward exact changed scope

reuse_allowed:
- channel: `SECURITY_SANDBOX`
  predecessor: accepted L8 terminal closure and fixed-tool boundary
  provenance_condition: worker/provider/tool source unchanged
  applicability_condition: this task does not alter execution/sandbox contract
- channel: `HTTP_RUNTIME`
  predecessor: fifth release accepted
  provenance_condition: ingress/admission contract unchanged
  applicability_condition: only read projection changes

human_owned:
- channel: `HUMAN_VERIFICATION / BROWSER_RUNTIME`
  scope: actual public trace visual/usability + one future Human Live run after Browser review
  expected_result_format: separate Human QA Task issued by Browser Command Center

not_required:
- channel: `REAL_PROVIDER_CALL`
  reason: no new execution authority in this task
- channel: `NEW_PUBLIC_RUN`
  reason: deployment can be proven without creating another run
- channel: `L8_RELEASE_GATE`
  reason: L8 is already CLOSED; this is post-closure UX work

forbidden:
- action_or_channel: `raw provider output inspection/export`
  reason: violates accepted public/private boundary
- action_or_channel: `new Live run/provider call`
  reason: no authority
- action_or_channel: `frontend-only invented trace`
  reason: would violate claim/evidence non-substitution

proof_non_substitution:
- frontend card render != durable backend execution evidence
- DB safe projection test != Human browser QA
- final run state COMPLETED != provider/tool trace detail
- Agent claim != admitted public trace evidence

## conformance reporting

- applicability: `REQUIRED`
- applicable policy_or_invariant:
  - `AGENT_CLAIM != ADMITTED_EVIDENCE`
  - `EXECUTOR_COMPLETED != WorkRun.ACCEPTED`
  - public trace must be derived from durable allowlisted evidence
  - provider/private bodies remain private
- required_actual_owner:
  - DB/public ingress owns projection;
  - frontend owns rendering only;
  - Human owns browser QA.
- planned_vs_actual_scope:
  - report any additional schema/role/migration need before implementing it.
- rollback_or_failure_semantics:
  - additive frontend must tolerate old backend;
  - failed 0028 migration rolls back transaction;
  - failed new ingress deployment must leave/restore prior known-good active deployment;
  - do not create a new public run to diagnose.

## project context impact

architecture:
- `NONE / additive read projection only`

orchestration_contract:
- `NONE`

security_sandbox:
- `NONE / prove unchanged`

public_provenance:
- `TASK_AND_CYCLE_ONLY` unless Browser later determines baseline docs need update

## accept 기준

- exact safe public result schema implemented.
- migration 0028 or equivalent mediated authority proven narrow.
- no raw/private provider/tool material exposed.
- Stockroom facts emitted only behind exact durable tool-result proof gate.
- frontend trace uses server evidence, not guesses.
- Recorded Replay remains intact.
- Public Live remains released throughout/after deploy.
- no new run/provider call.
- hosted safe projection for existing completed run matches expected truth.
- Human browser QA remains pending, not falsely completed.
- exact Git/deployment/export provenance available.

## hold/reject 기준

HOLD/REWORK if:
- trace requires raw provider output;
- ingress needs raw table grants;
- durable evidence cannot distinguish requested steps safely;
- frontend must invent step semantics;
- Stockroom facts cannot be tied to canonical durable result hash;
- backend/frontend compatibility would break current release;
- deployment changes provider/worker behavior;
- current released state regresses.

REJECT/rollback candidate if:
- capability/Origin/edge trust is weakened;
- secret/private protocol data is exposed;
- public control/admission semantics are changed without authority;
- new provider run/call occurs.

## mandatory stop 조건

- policy baseline conflict
- missing required terminal closure artifact
- dirty workspace collision with changed paths
- forbidden action/tool request
- security boundary uncertainty
- `PUBLIC_TRACE_RAW_DATA_EXPOSURE_RISK`
- `PUBLIC_TRACE_AUTHORITY_SCOPE_EXPANSION_REQUIRED`
- `PUBLIC_TRACE_DURABLE_SEMANTICS_AMBIGUOUS`
- `STOCKROOM_SAFE_RESULT_PROOF_GAP`
- `PUBLIC_TRACE_BACKWARD_COMPATIBILITY_FAILED`
- `HOSTED_RELEASE_STATE_REGRESSION`
- `EVIDENCE_SCOPE_EXPANSION_REQUIRED`
- Human decision required before a new run/provider call

Named blocker 이후에는 최소 source evidence, workspace inventory, report/export와 안전한 종료만 수행한다.

## 보고서 필수 항목

- 작업명 / work type / task path
- read canonical paths
- exact baseline
- current released-state preflight
- source inventory
- current read projection audit
- durable evidence → public field mapping table
- forbidden/raw field exclusion audit
- Stockroom safe-result hash gate proof
- migration 0028 design/ACL or NOT_REQUIRED proof
- backend changed files
- frontend changed files
- exact public JSON examples for running/completed/failure-safe cases
- integration tests
- frontend source tests
- static checks
- hosted migration/runtime projection proof
- deployment order and IDs
- current public-control/frontend/ingress final state
- new public run count during task
- provider call count during task
- worker/provider/tool source-change proof
- human pending
- forbidden-not-run
- mandatory stop/scope expansion
- planned-vs-actual conformance
- rollback/revert guide
- Git commit ancestry
- export byte identity
- unverified items

## export bundle 요구

Target:

`.aiassistant/reports/target/20260919_2236_aiscc-public-live-inspectable-execution-trace-projection-and-ui-1/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `RELEASED_STATE_PREFLIGHT.md`
- `CURRENT_PUBLIC_READ_CONTRACT_AUDIT.md`
- `PUBLIC_TRACE_CONTRACT.md`
- `DURABLE_TO_PUBLIC_FIELD_MAPPING.md`
- `FORBIDDEN_FIELD_EXCLUSION.md`
- `STOCKROOM_SAFE_RESULT_PROOF.md`
- `MIGRATION_0028_PROOF.md` if created, otherwise `MIGRATION_0028_NOT_REQUIRED.md`
- `BACKEND_PROJECTION_TESTS.md`
- `FRONTEND_TRACE_UI.md`
- `FRONTEND_TRACE_TESTS.md`
- `HOSTED_SAFE_PROJECTION_PROOF.md`
- `DEPLOYMENT_PROOF.md`
- `FINAL_RELEASED_STATE.md`
- `PROVIDER_WORKER_CONTRACT_UNCHANGED.md`
- `PROVIDER_SECRET_APPLICABILITY.md`
- `HUMAN_QA_PENDING.md`
- `WORKSPACE_STATE.md`
- changed files preserving repository-relative paths using exact Git blob bytes
- `REMOVED_FILES.md` only if deletion exists

## 사람 검증 요구

이번 Executor task에서는 수행하지 않는다.

Browser acceptance 이후 별도 Human QA Gate를 발행한다.

Human QA는 최소 다음을 확인해야 한다:
- public Live trace step cards visible;
- instruction visible;
- provider/tool/provider processing visible;
- Stockroom safe facts visible;
- terminal execution/public projection visible;
- Human decision boundary visible;
- Replay/Live coexistence;
- responsive/readability.

Human QA에서 새 Live run을 생성할 권한은 그 별도 QA Task가 부여할 때만 생긴다.

## 최종 응답 형식

1. result: completed / blocked / rejected-candidate
2. target bundle path
3. target ZIP SHA-256
4. exact baseline/final commit
5. migration 0028 status
6. backend projection summary
7. frontend trace summary
8. safe Stockroom proof
9. tests/static checks
10. hosted projection proof
11. deployment proof
12. Public Live final state
13. new public runs/provider calls during task
14. security/private-field exclusion
15. changed files
16. removed files
17. human verification: `HUMAN_PENDING`
18. blockers/unverified
