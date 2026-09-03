# 작업지시서: P2-1A Command Center read-model/API projection foundation implementation

## meta

- task_id: `20260903_0910_aiscc-p2-1a-command-center-read-model-api-projection-foundation-implementation-1`
- created_at: `2026-09-03T09:10:00+09:00`
- project: `AI Software Command Center (AISCC)`
- phase: `P2-1A — Command Center Read-model/API Projection Foundation`
- work_type: `BACKEND_IMPLEMENTATION / READ_MODEL_API`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `read-only Browser projection of accepted P1 runtime authority`
- predecessor_head: `6b0383fce036471e6760999a2352276e2806fca5`
- predecessor_design_task: `.aiassistant/tasks/done/20260903_0313_aiscc-p2-1-command-center-web-ui-substrate-and-contract-design-audit-1.md`
- predecessor_human_acceptance_cycle: `.aiassistant/records/aiscc/cycles/20260903_0908_aiscc-p2-1-command-center-web-ui-human-design-final-acceptance-1.cycle.md`
- predecessor_design_gate_cycle: `.aiassistant/records/aiscc/cycles/20260903_0904_aiscc-p2-1-command-center-web-ui-design-audit-command-center-acceptance-human-design-gate-1.cycle.md`
- target_bundle: `.aiassistant/reports/target/20260903_0910_aiscc-p2-1a-command-center-read-model-api-projection-foundation-implementation-1/`
- fresh_chat_policy: `NEW_IDE_CHAT_REQUIRED / FIRST_PRODUCT_MUTATION_AFTER_DESIGN_GATE`
- implementation_commit_authority: `NONE`
- success_boundary: `P2_1A_IMPLEMENTATION_CANDIDATE / COMMAND_CENTER_REVIEW_REQUIRED`

## 0. accepted Human design authority

Human result:

```text
Human P2-1 design review
판정: ACCEPTED
```

Accepted implementation boundary:

```text
HTML-first future direction
GET-only read API
LOCAL_PRIVATE_ONLY
Task metadata REFERENCE_ONLY when trusted metadata absent
runtime AdmittedCycle only
no repository Cycle indexing
no mutation controls
no new auth package
```

This Task implements only P2-1A. It does not implement the HTML shell.

## 1. exact goal

1. transport the exact current Task, exact 0904 design-gate Cycle, and exact 0908 Human-acceptance Cycle;
2. run in a genuinely new IDE Executor chat because this is the first P2 product-source mutation;
3. verify exact repository baseline and existing governance dirt;
4. implement explicit Pydantic read-model DTOs and presentation-only presence/availability values;
5. implement a privacy allowlist/safe-display layer;
6. implement read-only query protocols and PostgreSQL screen/query adapters over existing durable P1 tables/projections;
7. implement GET-only `/v1/command-center/**` JSON routes;
8. compose only read dependencies into FastAPI;
9. implement side-effect-free current NextAction reads without selection/rebuild;
10. implement ETag, consistent snapshot/revision metadata, cursor/limit, error envelope and authority-conflict behavior;
11. add focused unit/source/API/integration tests;
12. run required targeted and regression verification;
13. export changed source + evidence;
14. move current Task active→matching done;
15. stop without staging/commit.

## 2. explicit non-goals / forbidden

Do not:

- create HTML/CSS/JavaScript/template/static files;
- create `/command-center` HTML routes;
- add Node/npm/SPA/frontend framework;
- add or change package dependencies;
- add migrations or new database tables;
- modify P1 architecture/orchestration/security/evidence/Human/Judgment/Cycle semantics;
- modify repository `CommandCenterCycleRecord` indexing;
- parse `.aiassistant/tasks/done/**` as runtime Task authority;
- read arbitrary filesystem payload references from TaskConstraintRef;
- add authentication/authorization package;
- assume external/shared/public operator exposure;
- create mutation endpoints;
- invoke selection/admission/transition/rebuild/reconciliation from GET;
- modify Project Source mirror;
- start P2-1B/P2-2;
- stage/commit/push/deploy/network.

Forbidden Git:

```text
git add
git commit
git restore
git checkout
git reset
git clean
git stash
git push
git fetch
git pull
```

No package install or external network access.

## 3. new IDE chat gate

This Task MUST run in a genuinely new IDE Executor chat.

Reason:

```text
0313:
read-only DESIGN_AUDIT

0910:
first P2 product-source mutation
```

The implementation chat must not contain executed mutation history from the P1 terminal-maintenance chain or another
P2 implementation Task.

Before product source inspection report:

```text
SESSION_AUTHORITY:
NEW_P2_1A_IMPLEMENTATION_CHAT / PASS
```

Failure:

```text
BLOCKED_REQUIRED_EVIDENCE / NEW_IMPLEMENTATION_CHAT_REQUIRED
```

Do not mutate source after a failed session gate.

## 4. Downloads transport

Transport exactly three files.

### current Task

```text
source:
C:\Users\oracl\Downloads\20260903_0910_aiscc-p2-1a-command-center-read-model-api-projection-foundation-implementation-1.md

destination:
.aiassistant/tasks/active/20260903_0910_aiscc-p2-1a-command-center-read-model-api-projection-foundation-implementation-1.md
```

### 0904 design-gate Cycle

```text
source:
C:\Users\oracl\Downloads\20260903_0904_aiscc-p2-1-command-center-web-ui-design-audit-command-center-acceptance-human-design-gate-1.cycle.md

destination:
.aiassistant/records/aiscc/cycles/20260903_0904_aiscc-p2-1-command-center-web-ui-design-audit-command-center-acceptance-human-design-gate-1.cycle.md

expected SHA-256:
621ffae3fc107838efd708ccc418bdfccf5c299c0abe69eb07709ebd06d378af
```

### 0908 Human acceptance Cycle

```text
source:
C:\Users\oracl\Downloads\20260903_0908_aiscc-p2-1-command-center-web-ui-human-design-final-acceptance-1.cycle.md

destination:
.aiassistant/records/aiscc/cycles/20260903_0908_aiscc-p2-1-command-center-web-ui-human-design-final-acceptance-1.cycle.md

expected SHA-256:
b26beab7734f0e68226c353eee1edbea70563f2af353b29ca3f41a460ee475cb
```

Precheck all three before moving any newly absent-destination file:

- exact Task source exists;
- Task active destination absent;
- each Cycle:
  - if destination absent, exact Downloads source exists and SHA matches;
  - if destination already exists, exact destination SHA must match and no duplicate move occurs.

Do not search alternate Downloads paths.

Any identity or destination conflict:

```text
TRANSPORT_PRECONDITION_FAILED
```

No partial new transport after failed all-or-nothing precheck.

## 5. repository baseline

After transport and before product mutation require:

```text
repository == ai-software-command-center
branch == main
HEAD == 6b0383fce036471e6760999a2352276e2806fca5
index == empty
runtime/source/test/migration/config dirt == 0
```

Expected tracked governance/provenance dirt before 0904/0908 transport:

```text
.aiassistant/records/aiscc/cycles/20260903_0311_aiscc-project-source-mirror-v2-activation-persistence-final-acceptance-1.cycle.md
.aiassistant/tasks/done/20260903_0313_aiscc-p2-1-command-center-web-ui-substrate-and-contract-design-audit-1.md
```

After transport, expected additional Git-visible Cycle dirt:

```text
.aiassistant/records/aiscc/cycles/20260903_0904_aiscc-p2-1-command-center-web-ui-design-audit-command-center-acceptance-human-design-gate-1.cycle.md
.aiassistant/records/aiscc/cycles/20260903_0908_aiscc-p2-1-command-center-web-ui-human-design-final-acceptance-1.cycle.md
```

The current active Task is ignored.

If any unrelated product/governance dirt exists, do not clean or auto-expand:

```text
DIRTY_WORKSPACE_MIXED / COMMAND_CENTER_REVIEW_REQUIRED
```

## 6. minimum authoritative context

Read exact:

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md

.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_SECURITY_SANDBOX.md
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/tasks/done/20260903_0313_aiscc-p2-1-command-center-web-ui-substrate-and-contract-design-audit-1.md
.aiassistant/records/aiscc/cycles/20260903_0904_aiscc-p2-1-command-center-web-ui-design-audit-command-center-acceptance-human-design-gate-1.cycle.md
.aiassistant/records/aiscc/cycles/20260903_0908_aiscc-p2-1-command-center-web-ui-human-design-final-acceptance-1.cycle.md
.aiassistant/tasks/active/20260903_0910_aiscc-p2-1a-command-center-read-model-api-projection-foundation-implementation-1.md
```

Also read the 0313 target report only if it is still locally available and exact Task provenance is clear:

```text
P2_1_READ_MODEL_API_CONTRACT.md
CURRENT_WEB_SUBSTRATE.md
P2_1_IMPLEMENTATION_SLICES.md
```

If the ignored target was cleaned, use the exact contract restated in this Task; do not require recovery from Browser.

Read any P1 source module listed below as exact implementation evidence. Do not bulk-read unrelated history.

## 7. source owners that MUST remain authoritative

Use current source semantics from:

```text
src/aiscc/contracts/workflow.py
src/aiscc/workflow/models.py
src/aiscc/workflow/matrix.py
src/aiscc/workflow/ports.py
src/aiscc/persistence/repository.py
src/aiscc/persistence/models.py

src/aiscc/providers/models.py

src/aiscc/evidence/models.py
src/aiscc/evidence/repository.py

src/aiscc/human/models.py
src/aiscc/human/repository.py
src/aiscc/human/authority.py

src/aiscc/judgment/models.py
src/aiscc/judgment/authority.py

src/aiscc/cycle/models.py
src/aiscc/cycle/repository.py

src/aiscc/memory/models.py
src/aiscc/memory/repository.py

src/aiscc/next_action/models.py
src/aiscc/next_action/repository.py

src/aiscc/task_authority/models.py
src/aiscc/task_authority/ports.py

src/aiscc/api/app.py
src/aiscc/api/routes/health.py
src/aiscc/api/routes/control.py
```

Do not reinterpret these owners for UI convenience.

## 8. allowed product paths

Preferred new product module boundary:

```text
src/aiscc/command_center/__init__.py
src/aiscc/command_center/read_models.py
src/aiscc/command_center/queries.py
src/aiscc/command_center/postgres_queries.py
src/aiscc/command_center/privacy.py
src/aiscc/api/routes/command_center.py
```

Existing product file allowed to modify:

```text
src/aiscc/api/app.py
```

Focused tests may be added only under:

```text
tests/unit/command_center/**
tests/integration/command_center/**
```

If current repository structure proves one additional **composition-only** Python module is necessary, do not
silently create it. Report:

```text
IMPLEMENTATION_PATH_EXPANSION_REQUIRED
```

and STOP before adding the path.

Do not modify existing P1 repository/service/model implementation to make the UI easier.

## 9. non-negotiable read API invariants

Implement:

```text
GET/HEAD/framework OPTIONS only
JSON namespace:
/v1/command-center
```

No route in this package may accept mutation bodies or invoke a mutation-capable domain workflow.

Pydantic DTOs only.

Forbidden serialization:

```text
SQLAlchemy ORM rows
repository objects
issuer seals/tokens
private Human identity/comment
provider prompt/message/protocol body
agent/tool output body
evidence content body
raw NextAction private parameters/rationale
secret/credential/environment
SQL/stack trace
```

No generic aggregate field:

```text
status
complete
approved
accepted
```

that collapses independent authority dimensions.

Derived presentation fields MUST use explicit:

```text
presence
availability
derived_*
```

and MUST NOT fabricate authority enum values.

## 10. common response contract

Successful envelope:

```json
{
  "data": {},
  "meta": {
    "schema_version": "p2-1-command-center-read-v1",
    "snapshot_at": "<RFC3339 UTC>",
    "source_revisions": {},
    "consistency": "VERIFIED",
    "next_cursor": null,
    "poll_after_ms": 10000
  }
}
```

Requirements:

- IDs opaque strings;
- timestamps timezone-aware RFC3339 UTC;
- exact source enum spellings;
- source revisions dimensioned; missing omitted, never zero-filled;
- ETag derived from schema/stable ID/relevant owner revisions or stable immutable fingerprint;
- `If-None-Match` unchanged response → `304` no body;
- nonterminal detail/queue may recommend `poll_after_ms=10000`;
- terminal/immutable Cycle → `poll_after_ms=null`;
- cursor opaque and query-shape-bound;
- `limit` default `50`, exact valid range `1..100`.

Error envelope:

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "The requested read model is unavailable.",
    "retryable": false,
    "correlation_id": "<opaque-safe-id>"
  }
}
```

Required codes:

```text
INVALID_QUERY
NOT_FOUND
AUTHORITY_CONFLICT
NO_LONGER_CURRENT
PROJECTION_UNAVAILABLE
INTERNAL_ERROR
```

Never return stack/SQL/private payload content.

## 11. exact P2-1A JSON endpoints

Implement these new read endpoints only:

```text
GET /v1/command-center/projects/{project_id}/queue
GET /v1/command-center/work-runs/{work_run_id}
GET /v1/command-center/work-runs/{work_run_id}/transitions
GET /v1/command-center/work-runs/{work_run_id}/execution
GET /v1/command-center/work-runs/{work_run_id}/evidence
GET /v1/command-center/work-runs/{work_run_id}/human-judgment
GET /v1/command-center/projects/{project_id}/outcomes
GET /v1/command-center/cycles/{cycle_id}
GET /v1/command-center/projects/{project_id}/next-action
```

Do not add HTML routes in this Task.

## 12. Project queue contract

Endpoint:

```text
GET /v1/command-center/projects/{project_id}/queue
```

Accepted filters:

```text
workflow_state
execution_status
human_gate_status
judgment_presence
judgment_kind
terminal
q
cursor
limit
```

`q` v1 searches safe stable IDs only.

Ordering:

```text
WorkRun.updated_at DESC
WorkRun.work_run_id ASC
```

Each row MUST keep separate:

```text
project_id
work_run_id
task_contract {id, version}
task_display {availability, title?, type?, source_ref?}
workflow {state, state_version, updated_at}
execution {attempt_present, execution_attempt_id?, attempt_ordinal?, status?, execution_version?}
human_gate {presence, human_gate_id?, status?, suspension_status?, authority_revision?}
human_result {presence, result_kind?, authority_revision?}
judgment {presence, judgment_id?, kind?, owner_policy?, authority_revision?}
latest_transition_decision {decision_id?, outcome?, reason?, resulting_state?, resulting_state_version?}
next_action {presence, selection_id?, action_ref?, project_revision?, selected_at?}
runtime_mode
```

Task display first-version policy:

```text
no new trusted metadata owner
→ availability = REFERENCE_ONLY or UNAVAILABLE
→ title/type absent when no accepted source exists
```

## 13. WorkRun summary contract

```text
GET /v1/command-center/work-runs/{work_run_id}
```

MUST expose safe:

```text
project_id
work_run_id
task_contract {id, version}
runtime_mode
workflow {state, state_version, created_at, updated_at}
task_constraint safe ref/binding metadata
task_display availability
scope availability
blocker safe provenance
source_revisions
```

Do not dereference arbitrary `constraint_payload_ref`.

If scope content has no trusted source:

```text
scope.availability = REFERENCE_ONLY
allowed/forbidden content omitted
```

Binding inconsistency:

```text
409 AUTHORITY_CONFLICT
```

not partial normal success.

## 14. Transition contract

```text
GET /v1/command-center/work-runs/{work_run_id}/transitions
```

Ordering:

```text
decided_at ASC
transition_decision_id ASC
```

Expose request/evaluation/guards/decision with:

```text
decision.outcome
decision.resulting_state?
decision.resulting_state_version
derived_state_effect = CHANGED | UNCHANGED
```

Exclude requester identity; requester type only.

A `DENIED` decision MUST NOT appear as a state transition.

## 15. Execution contract

```text
GET /v1/command-center/work-runs/{work_run_id}/execution
```

Expose:

- execution attempt identity/order;
- Task contract ref;
- runtime mode;
- creation state/version;
- exact `ExecutionStatus`;
- execution version;
- provider/tool registry identities;
- durable counters;
- submission presence/ref;
- safe operation metadata.

Exclude:

- agent/provider/tool output bodies;
- prompt/message bodies;
- encrypted/private refs;
- unrestricted artifact/resource identity;
- stack/error internals.

No attempt:

```text
attempts = []
```

Do not fabricate an ExecutionStatus.

Durable `SECURITY_ADMITTED` operation phase may be displayed only as durable operation phase, not reconstructed
`SecurityDecision`.

## 16. Evidence contract

```text
GET /v1/command-center/work-runs/{work_run_id}/evidence
```

Preserve:

- checkpoint owner order;
- requirement-set ordered refs;
- candidate vs admission decision vs admitted evidence vs satisfaction distinction;
- requirement profile/obligation/semantic owner/type/freshness/applicability;
- safe content metadata only;
- set satisfaction/attestation separately.

Forbidden:

```text
evidence body
private producer content
admitted evidence == set satisfied inference
unsatisfied evidence == rejected Judgment inference
```

## 17. Human/Judgment contract

```text
GET /v1/command-center/work-runs/{work_run_id}/human-judgment
```

Expose four independent cards:

```text
human_gate
human_result
judgment
transition_effect
```

Exclude:

```text
Human principal_id
authentication/action authority refs
private comment ref/hash/body
```

No source enum named `JudgmentStatus` may be invented.

Use explicit presence plus exact `JudgmentKind`.

## 18. Outcome / Cycle / NextAction

Implement:

```text
GET /v1/command-center/projects/{project_id}/outcomes
GET /v1/command-center/cycles/{cycle_id}
GET /v1/command-center/projects/{project_id}/next-action
```

Runtime Cycle:

```text
AdmittedCycle only
```

Repository Markdown `CommandCenterCycleRecord`:

```text
not indexed
governance_record absent
```

Current memory:

- `current_only=true`;
- privacy-bounded safe summaries;
- no raw payload.

Current NextAction GET MUST use a new side-effect-free read query over existing durable projection/event lineage.

It MUST NOT call:

```text
select
rebuild_projection
issue
```

No current selection returns a normal `presence: NONE`; it does not create one.

## 19. consistency / transaction boundary

A response assembled across owners must be internally consistent.

Preferred:

```text
single repeatable-read snapshot transaction
```

If current architecture cannot provide a trustworthy cross-owner snapshot within allowed paths:

```text
409 AUTHORITY_CONFLICT
or
503 PROJECTION_UNAVAILABLE
```

Do not return a mixed best-effort snapshot.

Do not modify P1 owner persistence semantics.

## 20. local/private exposure boundary

The app currently binds loopback by default.

P2-1A does not add authentication.

Required:

```text
LOCAL_PRIVATE_ONLY
```

Do not change server host defaults or add public exposure behavior.

Framework OpenAPI/docs are not treated as a Command Center product surface.

## 21. validation / tests

### 21.1 static/source

Required:

```text
python -m compileall or repository-equivalent targeted syntax validation
Ruff on changed Python scope
mypy on changed Python scope
git diff --check
```

Use repository-local environment only.

### 21.2 unit/source contract

Add tests proving at minimum:

1. `WorkflowState` and `ExecutionStatus` serialize separately.
2. `EXECUTOR_COMPLETED` never maps to `WorkflowState.ACCEPTED`.
3. HumanResult does not populate Judgment fields.
4. Judgment does not populate TransitionDecision fields.
5. denied transition has `derived_state_effect=UNCHANGED`.
6. absent Judgment uses presence + `kind=null`, not a fabricated Judgment status.
7. task metadata/scope without trusted source is `REFERENCE_ONLY`/unavailable.
8. privacy denylist excludes Human identity/comment and provider/evidence bodies.
9. cursor and limit validation fail closed.
10. `GET` code path cannot invoke NextAction select/rebuild.
11. repository CommandCenterCycleRecord is absent from runtime Cycle DTO.
12. error envelopes do not expose stack/SQL/private payload.

### 21.3 PostgreSQL/read integration

Use existing repository-local PostgreSQL integration harness only.

No new container/image/package/network setup beyond already accepted local test harness.

Required targeted integration proof:

- queue snapshot with independent status dimensions;
- WorkRun + transition admitted/denied ordering;
- no-attempt and completed-attempt behavior;
- Evidence candidate/admitted/satisfaction separation;
- Human gate/result/Judgment separation;
- accepted runtime Cycle lookup;
- side-effect-free current NextAction lookup;
- consistency conflict/fail-closed path;
- privacy redaction against durable fixtures.

If existing integration harness is unavailable without environment expansion:

```text
EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

STOP before inventing a substitute proof.

### 21.4 HTTP runtime

Required, local loopback only.

Use repository-local packages or Python stdlib HTTP client; do not install a client dependency.

Verify:

- all exact endpoints return expected safe envelopes;
- GET/HEAD and framework OPTIONS only;
- unsupported POST/PUT/PATCH/DELETE do not mutate and are rejected;
- query validation;
- `304` ETag behavior;
- `404`, `409`, `503` safe error behavior;
- repeated GET does not mutate authoritative DB/event counts;
- no route invokes select/rebuild/admission/transition;
- app remains loopback/private by existing server default.

### 21.5 regression

After targeted checks PASS, run the repository's existing unit + integration regression suite if it requires no new
environment/network/package scope.

Report exact pass count.

If full integration regression requires unavailable environment expansion, do not substitute; classify it exactly.

### 21.6 not required

```text
BROWSER_RUNTIME
HUMAN visual/usability QA
HTML rendering
SSE/WebSocket
external network
provider real calls
deployment
```

## 22. mandatory stop

STOP before scope expansion if any occurs:

```text
new migration/table required
new dependency/package required
new durable Task metadata authority required
HTTP authentication/exposure decision required
repository Cycle index required
P1 semantic owner change required
new allowed product path required
current repository baseline drift
unrelated dirty source collision
integration proof requires new external environment
```

After STOP:

- capture minimum source evidence;
- preserve workspace inventory;
- write report/export;
- do not continue unrelated implementation.

## 23. changed-path expectation

Expected implementation changes are only within Section 8.

Report exact added/modified path inventory.

No Git staging or commit.

After Task lifecycle, source dirt plus governance provenance may remain for Browser review.

## 24. required export

Target:

```text
.aiassistant/reports/target/20260903_0910_aiscc-p2-1a-command-center-read-model-api-projection-foundation-implementation-1/
```

Required root:

```text
TASK.md
EXECUTOR_REPORT.md
API_CONTRACT_EVIDENCE.md
HTTP_RUNTIME_EVIDENCE.md
EXPORT_MANIFEST.md
```

Export every changed product/test file preserving repository-relative path.

Do not export unchanged P1 source.

`API_CONTRACT_EVIDENCE.md` must enumerate:

- exact implemented endpoint set;
- exact DTO/status separation;
- query owners;
- privacy exclusions;
- consistency/ETag/cursor/error behavior;
- no-write/side-effect proof;
- deviations from accepted design.

`HTTP_RUNTIME_EVIDENCE.md` must record commands/environment, routes/status, ETag behavior and DB no-mutation proof.

Manifest binds every payload except itself with byte count/SHA-256.

## 25. evidence contract

### executor_required

- `SESSION_AUTHORITY`: new P2-1A implementation chat;
- `STATIC_SOURCE`: current owner/source applicability;
- `FRONTEND_SOURCE_TEST`: DTO/read-contract tests;
- `INTEGRATION_TEST`: existing PostgreSQL read integration;
- `HTTP_RUNTIME`: local GET-only API behavior and no-mutation proof;
- `STATIC_CHECK`: Ruff/mypy/diff-check;
- `PUBLIC_PROVENANCE`: Task/report/export lifecycle.

### reuse_allowed

Accepted P1 tests/semantics may be reused only as owner semantics, not as proof of the new API.

### human_owned

No Human browser/visual gate is required for P2-1A because no UI is rendered.

Human P2-1 design acceptance is already `HUMAN_PROVIDED`.

### not_required

- Browser runtime;
- visual QA;
- deployment;
- provider/network;
- P2-1B UI.

### forbidden

- product mutation outside Section 8;
- database migration;
- HTML/UI implementation;
- package install;
- Git staging/commit;
- external network.

### proof non-substitution

```text
P1 repository method exists != new API tested
unit DTO test != PostgreSQL read integration
HTTP artifact/source != HTTP runtime
GET returns 200 != no authoritative mutation
design accepted != implementation accepted
```

## 26. Task lifecycle

After implementation/evidence/report/export completes:

```text
.aiassistant/tasks/active/20260903_0910_aiscc-p2-1a-command-center-read-model-api-projection-foundation-implementation-1.md
→
.aiassistant/tasks/done/20260903_0910_aiscc-p2-1a-command-center-read-model-api-projection-foundation-implementation-1.md
```

Move, not Copy.

Do not stage/commit.

## 27. success / result boundary

Successful candidate:

```text
P2_1A_IMPLEMENTATION_CANDIDATE
/ COMMAND_CENTER_REVIEW_REQUIRED
```

Do not declare:

```text
P2-1A ACCEPTED
P2-1A CLOSED
P2-1B STARTED
P2-1 ACCEPTED
P2-2 STARTED
```

## 28. preserved artifacts

Preserve:

- `.aiassistant/records/aiscc/cycles/20260903_0904_aiscc-p2-1-command-center-web-ui-design-audit-command-center-acceptance-human-design-gate-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260903_0908_aiscc-p2-1-command-center-web-ui-human-design-final-acceptance-1.cycle.md`
- `.aiassistant/tasks/done/20260903_0910_aiscc-p2-1a-command-center-read-model-api-projection-foundation-implementation-1.md`
- `.aiassistant/tasks/done/20260903_0313_aiscc-p2-1-command-center-web-ui-substrate-and-contract-design-audit-1.md`
- accepted mirror activation persistence commit `6b0383fce036471e6760999a2352276e2806fca5`.

Target bundle is temporary through Browser substantive review.
