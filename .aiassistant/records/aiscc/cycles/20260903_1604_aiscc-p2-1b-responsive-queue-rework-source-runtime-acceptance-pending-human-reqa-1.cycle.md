# AISCC Cycle Record

## meta

- cycle_id: `20260903_1604_aiscc-p2-1b-responsive-queue-rework-source-runtime-acceptance-pending-human-reqa-1`
- date: `2026-09-03T16:04:00+09:00`
- project: `AI Software Command Center (AISCC)`
- primary_semantic_owner: `Browser Command Center P2-1B Human-QA rework review`
- affected_areas: `responsive WorkRun queue cards, label hierarchy, landing focus spacing, cursor viewport/focus retention`
- work_type: `COMMAND_CENTER_JUDGMENT / HUMAN_REQA_GATE`
- predecessor_head: `4ea1fe6f7cb8e11ff5ccfde70462eba931c4071e`
- predecessor_task: `.aiassistant/tasks/done/20260903_1602_aiscc-p2-1b-responsive-queue-layout-and-human-qa-usability-rework-1.md`
- submitted_bundle: `20260903_1602_aiscc-p2-1b-responsive-queue-layout-and-human-qa-usability-rework-1.zip`
- submitted_bundle_sha256: `65094962fb78f632c0c409cc0e21b3e28c2ee3cb0ffc83d9a4de7830727c360c`
- result_status: `ACCEPTED_PENDING_HUMAN_REQA / P2_1B_RESPONSIVE_REWORK_SOURCE_RUNTIME_ACCEPTED`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260903_1604_aiscc-p2-1b-responsive-queue-rework-source-runtime-acceptance-pending-human-reqa-1.cycle.md`
- P2_status: `STARTED / P2-1 ACTIVE`
- P2_1B_status: `SOURCE_RUNTIME_REWORK_ACCEPTED / HUMAN_REQA_PENDING`
- P2_1C_status: `NOT_STARTED`

## independent package verification

Browser-side independent verification:

```text
archive SHA-256:
65094962fb78f632c0c409cc0e21b3e28c2ee3cb0ffc83d9a4de7830727c360c

manifest-declared payloads:
13

manifest byte/hash mismatches:
0

current candidate paths:
5

current candidate aggregate:
fe68734a4b12b3e3038d8c38dbd93b40e26481c2d8541fd88e8d95717e9454fd
```

Exact current candidate identity:

```text
src/aiscc/api/app.py
34b9216342dc256fd319ab5c594799b9aa6784c35bc13a8b01595d4204d572f0

src/aiscc/api/routes/command_center_ui.py
05ac1ba9ce029d9b45b8aa93ee805976b97cc8b4e338af3747c14577e08122e2

src/aiscc/command_center/web.py
06a281504a3e880dca9d96dfb92fcf8b209f39d4a62a306155e8139cae201b8e

tests/integration/command_center/test_web_ui.py
9eaaf6e5018b811a1a536ec2448baad234d9753944ee6efad4080f33f5499134

tests/unit/command_center/test_web_shell.py
bfbbdd0f71efdccb28bb0a5dd033d9f88d7f2cd19bbfebcce88011def265a410
```

Protected files remained byte-identical:

```text
src/aiscc/api/app.py
src/aiscc/api/routes/command_center_ui.py
```

## rework acceptance

The Command Center accepts the source/runtime implementation of all four Human-QA rework items.

### HQA-1 landing input spacing/focus

Accepted source contract:

```text
project-id-field:
explicit 0.7rem vertical gap

input/select focus:
accent border
single accent box-shadow ring
warning outline suppressed for input/select

blur:
normal border
no separate residual warning-border state
```

### HQA-2 label grammar

A single reusable grammar is used for filter and authority labels:

```text
Korean primary
+
technical secondary
```

Examples:

```text
워크플로
WorkflowState

실행 상태
ExecutionStatus

사람 검토 관문
HumanGateStatus
```

### HQA-3 responsive queue

The rejected legacy 9-column table and queue horizontal-scroll rail are removed.

Current source uses:

```text
section.work-run-list
→ article.work-run-card
→ dl identity/state/authority groups
```

Each WorkRun independently exposes:

```text
Task / WorkRun identity
WorkflowState
ExecutionStatus
HumanGateStatus
HumanResult
Judgment
TransitionDecision
NextAction
RuntimeMode
```

Responsive source contract:

```text
default:
3-column authority grid

<=1180px:
2-column authority grid

<=720px:
1-column authority grid

long identifiers / NextAction:
overflow-wrap:anywhere

queue card/list:
min-width:0
no large fixed/min width
no primary horizontal-scroll rail
```

This source structure is sufficient to proceed to Human visual re-QA but does not substitute for actual
1080/1280/1440 Browser verification.

### HQA-4 cursor viewport/focus retention

Accepted source behavior:

```text
previous/next:
existing AJAX queue load only

pagination request:
preserveContent=true

render completion:
restore invoked enabled control
or stable queue heading

focus:
focus({preventScroll:true})
```

No pagination handler contains:

```text
window.scrollTo
scrollIntoView
hash navigation
location navigation
```

The previous content remains rendered while the request is in flight, preventing queue-height collapse.

## regression/runtime evidence admitted

```text
session lineage:
1325 → 1329 → 1602 / PASS

targeted:
31 passed, 3 environment-expected skips in non-DB pass

full applicable PostgreSQL unit + integration:
245 passed

Ruff:
PASS

mypy:
PASS

compile/syntax:
PASS

git diff --check:
PASS

normal default-entrypoint HTTP:
PASS

landing/project/assets:
200

queue/filter/cursor:
PASS

ETag/304:
PASS

authoritative event-count no-mutation:
PASS

POST/PUT/PATCH/DELETE:
405 / no mutation

CSP/security/LOCAL_PRIVATE_ONLY:
PASS

Human responsive/usability re-QA:
HUMAN_PENDING
```

## accepted behavior preserved

The rework did not broaden or change:

```text
P2-1A API as sole UI data authority
Project ID navigation
Task metadata REFERENCE_ONLY fallback
filter semantics
opaque cursor semantics
ETag / 304
manual refresh
10-second visible/nonterminal polling
hidden-tab polling stop
terminal-only polling stop
Korean-first policy
safe DOM
LOCAL_PRIVATE_ONLY
CSP/security headers
no Project catalog/index
no mutation controls
no P2-1C route
```

## Human re-QA scope

A full repeat of the original 13 Operations is not required.

Human re-QA is narrowed to:

```text
R1 landing label/input spacing + focus
R2 filter label consistency
R3 1080px queue card readability
R4 1280px queue card readability
R5 1440px queue card readability
R6 all nine dimensions visible without queue horizontal scroll
R7 previous/next viewport retention
R8 keyboard/focus retention after pagination
```

Already-passed polling/ETag/security behavior may be spot-checked but is not a required full rerun unless visual
re-QA exposes drift.

## state

```text
P2:
STARTED / P2-1 ACTIVE

P2-1A:
ACCEPTED / PERSISTED

P2-1B:
ACCEPTED_PENDING_HUMAN_REQA

P2-1C:
NOT_STARTED
```

## preserved artifacts

Preserve:

- accepted P2-1A commit `4ea1fe6f7cb8e11ff5ccfde70462eba931c4071e`
- `.aiassistant/records/aiscc/cycles/20260903_1431_aiscc-p2-1b-shell-queue-rework-acceptance-pending-human-browser-qa-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260903_1436_aiscc-p2-1b-human-browser-qa-gate-execution-guidance-correction-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260903_1600_aiscc-p2-1b-human-browser-qa-rework-responsive-queue-and-visual-hierarchy-1.cycle.md`
- `.aiassistant/tasks/done/20260903_1602_aiscc-p2-1b-responsive-queue-layout-and-human-qa-usability-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260903_1604_aiscc-p2-1b-responsive-queue-rework-source-runtime-acceptance-pending-human-reqa-1.cycle.md`
- current exact five-file P2-1B rework candidate dirt.

## next action

next_action:
- owner: `Human`
- work_type: `HUMAN_BROWSER_REQA`
- title: `P2-1B responsive queue focused Human re-QA`
- IDE_Task_required_now: `No`
- required_checks: `R1-R8`
- P2_1C_execution: `forbidden until Human re-QA + P2-1B persistence`
