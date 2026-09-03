# 작업지시서: P2-1 Command Center Web UI substrate and interaction-contract design audit

## meta

- task_id: `20260903_0313_aiscc-p2-1-command-center-web-ui-substrate-and-contract-design-audit-1`
- created_at: `2026-09-03T03:13:00+09:00`
- project: `AI Software Command Center (AISCC)`
- phase: `P2-1 — Command Center Web UI`
- work_type: `DESIGN_AUDIT / FRONTEND_DISCOVERY`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P2-1 Browser-visible Command Center information architecture and read-model contract`
- predecessor_head: `6b0383fce036471e6760999a2352276e2806fca5`
- predecessor_cycle: `.aiassistant/records/aiscc/cycles/20260903_0311_aiscc-project-source-mirror-v2-activation-persistence-final-acceptance-1.cycle.md`
- phase_handoff: `.aiassistant/reports/aiscc/20260902_2331_aiscc-p1-completion-p2-entry-handoff-1.md`
- target_bundle: `.aiassistant/reports/target/20260903_0313_aiscc-p2-1-command-center-web-ui-substrate-and-contract-design-audit-1/`
- fresh_chat_policy: `NEW_IDE_CHAT_REQUIRED / P2_PHASE_ENTRY`
- implementation_authority: `NONE`
- success_boundary: `P2_1_WEB_UI_DESIGN_CANDIDATE / COMMAND_CENTER_AND_HUMAN_REVIEW_REQUIRED`

## 0. phase authority

Accepted terminal state entering this Task:

```text
P1:
ACCEPTED / CLOSED

Project Source mirror v2:
ACTIVE / HUMAN_SYNC_CONFIRMED / 22

P2:
NOT_STARTED / ENTRY_READY

next executable:
P2-1 Command Center Web UI
```

This Task is the first P2 execution.

It does not automatically mark P2-1 accepted or closed.

## 1. exact goal

1. transport the exact current Task and exact 0311 mirror-activation final-acceptance Cycle;
2. in a genuinely new IDE Executor chat, bootstrap from current canonical authority;
3. verify exact repository baseline and classify current web/frontend/application substrate;
4. identify existing HTTP routes, static/template/frontend assets, application bootstrap, and test/runtime boundaries
   relevant to a Command Center Web UI;
5. map the already-implemented P1 domain/runtime data that can support Browser-visible Command Center projections;
6. identify missing read-model/API/projection boundaries without implementing them;
7. define an exact P2-1 MVP information architecture and screen/interaction contract;
8. define a backend/read-model contract proposal that preserves P1 authority boundaries;
9. split P2-1 into bounded implementation slices with explicit Human browser/visual QA gates;
10. export design evidence and candidate documents;
11. move current Task active→matching done and stop without product-source mutation.

## 2. non-goals / forbidden

This is design/discovery only.

Do not:

- modify `src/**`, `tests/**`, migrations, templates, static assets, frontend files, or runtime config;
- add a frontend framework/package;
- add npm/node tooling merely because a Web UI is planned;
- add API routes or read-model code;
- change database schema;
- modify canonical architecture/orchestration/security/evidence/human/cycle rules;
- modify CURRENT_STATE_SUMMARY / DECISION_REGISTER / NEXT_ACTIONS;
- stage or commit;
- start P2-2 synthetic repository;
- start P2-3 replay corpus;
- start P2-4 self-dogfooding;
- implement Public Bounded Live;
- access network, external Browser, provider, credential, or deployment environment.

Forbidden Git actions:

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

The only repository mutation authorized is Task/Cycle transport and current Task active→done lifecycle.

## 3. fresh IDE chat gate

This Task MUST run in a genuinely new IDE Executor chat.

The new chat must not have executed the P1 terminal-persistence/mirror Tasks.

Before source inspection report:

```text
SESSION_AUTHORITY:
NEW_P2_IDE_CHAT / PASS
```

If the chat contains execution history from the P1 terminal persistence chain, stop before source inspection with:

```text
BLOCKED_REQUIRED_EVIDENCE / NEW_P2_IDE_CHAT_REQUIRED
```

Do not create a substitute session automatically.

## 4. Downloads transport

Exactly two files:

```text
C:\Users\oracl\Downloads\20260903_0313_aiscc-p2-1-command-center-web-ui-substrate-and-contract-design-audit-1.md
C:\Users\oracl\Downloads\20260903_0311_aiscc-project-source-mirror-v2-activation-persistence-final-acceptance-1.cycle.md
```

Destinations:

```text
.aiassistant/tasks/active/20260903_0313_aiscc-p2-1-command-center-web-ui-substrate-and-contract-design-audit-1.md
.aiassistant/records/aiscc/cycles/20260903_0311_aiscc-project-source-mirror-v2-activation-persistence-final-acceptance-1.cycle.md
```

0311 Cycle expected SHA-256:

```text
f984450adafc61fcc5e3b0f066c92e9dde9e2a60c1e4f8fc721d62d10eee48d6
```

Before either Move require:

- both exact Downloads sources exist;
- both exact destinations do not exist;
- Cycle source SHA-256 exact match.

Any failure:

```text
move neither
do not search alternate Downloads path
do not overwrite/delete
STOP: TRANSPORT_PRECONDITION_FAILED
```

All PASS:

- Move exactly both files, not Copy;
- verify destination identity and Downloads-source absence.

## 5. repository preflight

After transport and before discovery require:

```text
repository == ai-software-command-center
branch == main
HEAD == 6b0383fce036471e6760999a2352276e2806fca5
index == empty
runtime/source/test/migration dirt == 0
```

Expected Git-visible governance dirt after current Cycle transport and while Task is active/ignored:

```text
exactly:
.aiassistant/records/aiscc/cycles/20260903_0311_aiscc-project-source-mirror-v2-activation-persistence-final-acceptance-1.cycle.md
```

If repository has advanced or unexpected dirt exists, do not reset/restore. Report exact drift and stop with:

```text
READ_ONLY_RECONCILIATION_REQUIRED
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
.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md
.aiassistant/reports/aiscc/AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md
.aiassistant/reports/aiscc/20260902_2331_aiscc-p1-completion-p2-entry-handoff-1.md

.aiassistant/records/aiscc/cycles/20260903_0311_aiscc-project-source-mirror-v2-activation-persistence-final-acceptance-1.cycle.md
.aiassistant/tasks/active/20260903_0313_aiscc-p2-1-command-center-web-ui-substrate-and-contract-design-audit-1.md
```

If current source discovery proves another accepted P1 rule is directly required to interpret a surfaced symbol,
read that exact rule and report why. Do not bulk-read all rules/history.

## 7. current application/web substrate discovery

Read-only inventory the repository.

Allowed targeted enumeration:

```text
pyproject.toml
src/aiscc/**
tests/**
migrations/**
config/**
```

and exact web/template/static/frontend directories discovered from those sources.

Report:

- application entrypoint(s);
- current FastAPI/Uvicorn or other HTTP bootstrap;
- current route modules and route prefixes;
- HTML/template/static serving, if any;
- current browser-facing routes, if any;
- current JSON API routes, if any;
- existing serialization/read-model patterns;
- frontend/package/tooling currently present or absent;
- test layers relevant to HTTP/frontend;
- authentication/authorization assumptions surfaced by source;
- whether a Command Center UI can be built within the existing Python application or requires a separately justified
  frontend build system.

Do not infer a framework requirement from preference.

## 8. P1 runtime projection inventory

Identify exact source owners that already expose or can read the following P1 concepts:

```text
Project
TaskContract / external task authority
WorkRun
WorkflowState / state_version
ExecutionAttempt / ExecutionOperation
EvidenceCheckpoint / RequirementSet / AdmittedEvidence
HumanGate / HumanResult
Judgment
CycleRecord
NextAction
RuntimeMode / security admission information needed for display
```

For each concept report:

- canonical semantic owner;
- source module/class/repository/service;
- durable store/repository owner;
- existing query/read interface;
- whether Browser display can use an existing read path;
- whether a P2-1 read-model/API adapter is required;
- forbidden semantic reinterpretation.

Do not create a generic "status" that collapses:

```text
WorkflowState
ExecutionStatus
HumanGateStatus
JudgmentStatus
```

## 9. P2-1 MVP information architecture candidate

Design the minimum operator-facing Command Center surface needed to make the AISCC governance mechanism
understandable.

The candidate must include at least:

### A. Project / task queue

Show:

- current Project identity;
- Task/WorkRun identity;
- task title/type;
- current WorkflowState;
- state_version;
- execution status as a separate dimension;
- Human gate indicator;
- Judgment status;
- stable Next Action.

### B. WorkRun detail

Show:

- Task Contract summary;
- allowed/forbidden scope;
- current state/version;
- transition timeline with admitted/denied distinction;
- execution attempts/operations;
- blocker/rework reason when applicable.

### C. Evidence

Show:

- checkpoint/purpose;
- requirement rows;
- owner/type/freshness/applicability;
- candidate vs admitted distinction;
- satisfaction/unsatisfied reason;
- proof provenance.

### D. Human / Judgment

Show separately:

- HumanGate lifecycle;
- HumanResult, when admitted;
- authoritative Judgment;
- transition decision/state effect.

The UI must not imply:

```text
HumanResult == Judgment
Judgment == TransitionDecision
Agent claim == admitted evidence
Executor complete == accepted
```

### E. Cycle / Next Action

Show:

- terminal/rework Cycle summary;
- accepted/rejected judgment;
- commit/result references when present;
- stable next action.

### F. runtime/public-mode boundary

If exposed in P2-1, show RuntimeMode and public/replay/live availability as read-only policy/state; do not implement
P2-3 Replay or Public Live behavior in this phase.

## 10. interaction contract

Define exact operator interactions for the first implementation.

Classify each control as one of:

```text
READ_ONLY
SYSTEM_ACTION_CANDIDATE
HUMAN_OWNED_ACTION
NOT_IN_P2_1
```

Default P2-1 MVP should prefer read-only observability.

Any proposed mutating control must identify:

- P1 authority owner;
- existing service/API that performs the operation;
- required current state/version;
- evidence/human/security gate;
- idempotency/stale behavior;
- visible success/failure semantics.

Do not invent direct UI state mutation.

## 11. API/read-model contract candidate

For each MVP screen define:

- source entities;
- proposed endpoint/query boundary;
- request parameters;
- response fields;
- ordering/pagination;
- stable identifiers;
- status dimensions kept separate;
- empty/loading/error semantics;
- sensitive/private fields excluded;
- whether endpoint is existing or new.

Prefer thin read models over exposing ORM/database entities directly.

Do not implement endpoints.

## 12. visual/presentation contract

Define a functional MVP visual hierarchy, not final brand polish.

Must specify:

- desktop-first primary width/layout assumption;
- global navigation;
- queue/list hierarchy;
- status/state badges and their semantic labels;
- timeline presentation;
- evidence owner/type distinction;
- Human-required emphasis;
- blocked/rework/error emphasis;
- detail drawers/pages/modal policy;
- responsive minimum behavior;
- empty/loading/error states;
- accessibility basics for state not conveyed by color alone.

Do not introduce a design system dependency in this audit.

## 13. implementation slicing

Propose bounded P2-1 implementation slices.

At minimum separate:

```text
P2-1A:
read-model/API projection foundation

P2-1B:
Command Center shell + project/task queue

P2-1C:
WorkRun transition/execution detail

P2-1D:
Evidence + Human/Judgment detail

P2-1E:
Cycle/Next Action + integrated browser QA
```

The audit may recommend a different slice boundary if current source proves a better decomposition, but must explain
why.

Identify which slices can reuse existing runtime tests and which require:

```text
FRONTEND_SOURCE_TEST
HTTP_RUNTIME
BROWSER_RUNTIME
HUMAN_VERIFICATION
```

Human browser/visual QA remains Human-owned.

## 14. design decision questions to resolve

The report must give a recommendation and evidence for each:

1. server-rendered/HTML-first vs separate SPA/build system for P2-1 MVP;
2. existing route family vs new dedicated `/command-center` or equivalent namespace;
3. read-only first release vs mutating operator actions in first P2-1 MVP;
4. one detail page vs drill-down subpages;
5. polling/manual refresh vs live streaming for current-state updates;
6. how to render exact state dimensions without collapsing semantics;
7. how to preserve Replay/Public Live scope for later P2/P3 tasks.

Unresolved product choices requiring Human decision must be explicit.

## 15. required export

Target:

```text
.aiassistant/reports/target/20260903_0313_aiscc-p2-1-command-center-web-ui-substrate-and-contract-design-audit-1/
```

Required root Markdown:

```text
TASK.md
EXECUTOR_REPORT.md
CURRENT_WEB_SUBSTRATE.md
P2_1_UI_INFORMATION_ARCHITECTURE.md
P2_1_READ_MODEL_API_CONTRACT.md
P2_1_IMPLEMENTATION_SLICES.md
EXPORT_MANIFEST.md
```

No unchanged runtime source export is required.

Report exact source paths/symbols instead.

Manifest binds every payload except itself with byte count/SHA-256.

## 16. evidence contract

### executor_required

- `SESSION_AUTHORITY`: genuinely new P2 IDE chat;
- `STATIC_SOURCE`: exact current web/application substrate;
- `STATIC_SOURCE`: P1 read/projection source-owner inventory;
- `DESIGN_EVIDENCE`: MVP information architecture;
- `DESIGN_EVIDENCE`: read-model/API contract candidate;
- `DESIGN_EVIDENCE`: implementation slicing and evidence plan;
- `PUBLIC_PROVENANCE`: Task lifecycle and report bundle.

### reuse_allowed

- accepted P1 semantic/runtime baselines while source identity and canonical authority remain current;
- accepted terminal P1→P2 handoff;
- accepted Project Source v2 activation.

### human_owned

- final product/UI design acceptance;
- Browser visual/usability judgment;
- any decision to add mutating controls beyond the accepted P1 service boundaries.

### not_required

- database/runtime mutation;
- HTTP server execution;
- Browser runtime;
- provider calls;
- network;
- deployment;
- screenshot/visual QA.

### forbidden

- product source mutation;
- package installation;
- external evidence scope expansion;
- P2-2/P2-3/P2-4 implementation.

### proof non-substitution

```text
source inventory != browser QA
design candidate != Human UI acceptance
existing API possibility != implemented endpoint
P2 ENTRY_READY != P2-1 ACCEPTED
```

## 17. Task lifecycle

After required audit/report/export completion:

```text
.aiassistant/tasks/active/20260903_0313_aiscc-p2-1-command-center-web-ui-substrate-and-contract-design-audit-1.md
→
.aiassistant/tasks/done/20260903_0313_aiscc-p2-1-command-center-web-ui-substrate-and-contract-design-audit-1.md
```

Move, not Copy.

Do not stage or commit.

After lifecycle, normal Git-visible governance dirt should be:

```text
0311 acceptance Cycle
+ current 0313 Task done
```

No source/runtime dirt.

## 18. success / stop

Successful result:

```text
P2_1_WEB_UI_DESIGN_CANDIDATE
/ COMMAND_CENTER_AND_HUMAN_REVIEW_REQUIRED
/ NO_PRODUCT_MUTATION
```

Do not declare:

```text
P2-1 ACCEPTED
P2-1 CLOSED
P2-2 STARTED
PUBLIC_BOUNDED_LIVE RELEASED
```

Mandatory stop if:

- fresh P2 chat gate fails;
- repository baseline has unexplained drift;
- accepted P1 semantic owner conflicts with current source;
- design requires a new framework/package decision not supported by source evidence;
- requested source investigation requires network/credentials.

## 19. preserved artifacts

Preserve:

- accepted activation persistence commit `6b0383fce036471e6760999a2352276e2806fca5`;
- `.aiassistant/records/aiscc/cycles/20260903_0311_aiscc-project-source-mirror-v2-activation-persistence-final-acceptance-1.cycle.md`;
- `.aiassistant/tasks/done/20260903_0313_aiscc-p2-1-command-center-web-ui-substrate-and-contract-design-audit-1.md`;
- P1→P2 handoff;
- active Project Source mirror v2 authority.

Target bundle is temporary through Command Center/Human review.
