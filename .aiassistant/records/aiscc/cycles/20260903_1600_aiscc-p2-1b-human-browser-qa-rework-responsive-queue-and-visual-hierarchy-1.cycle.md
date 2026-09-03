# AISCC Cycle Record

## meta

- cycle_id: `20260903_1600_aiscc-p2-1b-human-browser-qa-rework-responsive-queue-and-visual-hierarchy-1`
- date: `2026-09-03T16:00:00+09:00`
- project: `AI Software Command Center (AISCC)`
- primary_semantic_owner: `Human P2-1B Browser visual/usability QA / Browser Command Center admission`
- affected_areas: `P2-1B landing form spacing, filter label hierarchy, queue responsive information architecture, cursor pagination viewport retention`
- work_type: `HUMAN_VERIFICATION / UI_REWORK`
- predecessor_head: `4ea1fe6f7cb8e11ff5ccfde70462eba931c4071e`
- predecessor_source_runtime_cycle: `.aiassistant/records/aiscc/cycles/20260903_1431_aiscc-p2-1b-shell-queue-rework-acceptance-pending-human-browser-qa-1.cycle.md`
- qa_guidance_cycle: `.aiassistant/records/aiscc/cycles/20260903_1436_aiscc-p2-1b-human-browser-qa-gate-execution-guidance-correction-1.cycle.md`
- human_result_status: `HUMAN_PROVIDED / REWORK_REQUIRED / RESPONSIVE_QUEUE_AND_VISUAL_HIERARCHY`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260903_1600_aiscc-p2-1b-human-browser-qa-rework-responsive-queue-and-visual-hierarchy-1.cycle.md`
- P2_status: `STARTED / P2-1 ACTIVE`
- P2_1B_status: `HUMAN_QA_REWORK_REQUIRED`
- P2_1C_status: `NOT_STARTED`

## Human QA environment

Human executed P2-1B Browser QA with:

```text
Chrome
Zoom 100%
1080px
1280px
1440px+
and an approximately 1881px comparison viewport

runtime:
normal local AISCC server + disposable seeded PostgreSQL fixture

Project ID:
cc-project-87f06f16b2a448bdb1a6204ab011f382
```

The exact Project ID is QA fixture identity only and is not product/canonical Project authority.

## Human operation results

```text
Operation 1 — landing page:
PASS with visual defects

Operation 2 — Project ID navigation:
PASS

Operation 3 — queue information hierarchy:
functional PASS / visual REWORK

Operation 4 — Task metadata fallback:
PASS

Operation 5 — filters:
functional PASS / label hierarchy REWORK

Operation 6 — pagination:
functional PASS / viewport-retention REWORK

Operation 7 — manual refresh / ETag:
PASS

Operation 8 — 10-second polling:
PASS

Operation 9 — hidden-tab polling stop:
PASS

Operation 10 — terminal-only polling stop:
PASS

Operation 11 — loading/empty/error:
LOADING visible
EMPTY visible
INVALID_QUERY visible
NOT_FOUND not executed
AUTHORITY_CONFLICT not executed
PROJECTION_UNAVAILABLE not executed
UNEXPECTED_ERROR not executed

Operation 12 — accessibility/usability basics:
REWORK

Operation 13 — scope guard:
PASS
```

Unexecuted error states are not a blocker in this Human QA because the QA contract explicitly allowed non-forced
error cases to remain `NOT_EXECUTED`.

## Human-observed defects

### HQA-1 landing Project-ID field spacing/focus presentation

Human observed:

```text
`알고 있는 Project ID` label and the input are too close.

The yellow focus/blur border presentation looks visually awkward.
```

The screenshot confirms the label visually crowds the input focus ring.

Required result:

- clear vertical separation between label and input;
- one coherent focus treatment;
- no label/focus-outline collision;
- blur state returns to the normal field border without residual/competing yellow presentation.

### HQA-2 mixed technical-label hierarchy

At approximately 1080px the Human observed inconsistent forms such as:

```text
사람 검토 관문 (Human Gate /
HumanGateStatus)

Task / WorkRun

워크플로
(WorkflowState)

실행 상태 (ExecutionStatus)
```

Problems:

- some headings are Korean-first + technical identifier;
- some remain English-only;
- some put technical owner text inline;
- some wrap at arbitrary slash/parenthesis positions;
- filter labels and queue labels do not use one stable visual grammar.

Required result:

```text
human-facing Korean primary label
+
technical identifier as a consistent secondary line
```

Do not translate exact source enum values.

### HQA-3 queue table responsive usability failure

Human screenshots prove:

```text
1080px:
the queue initially exposes only the left portion of the 9 authority dimensions;
Judgment and right-side dimensions are outside the default viewport.

1280px:
still dense and horizontally constrained.

1440px:
still substantially wide/dense.

approximately 1881px:
the 9-column table finally fits without horizontal scrolling.
```

The previous implementation technically provided an internal horizontal scrollbar, but Human visual/usability
acceptance rejects this as the default operator presentation.

Reason:

```text
horizontal overflow supported
!=
operator queue readable at the primary target viewport
```

P2-1B's accepted Human design requires independent authority dimensions, but it does **not** require those dimensions
to be nine simultaneous table columns.

Required responsive information architecture:

```text
replace the single 9-column queue table
with an accessible WorkRun card/list presentation
that preserves all nine authority dimensions separately.
```

Recommended exact structure:

```text
WorkRun card header:
- Task / WorkRun identity
- Task metadata availability
- TaskContract ID/version
- WorkRun ID

primary state strip:
- 워크플로
  technical line: WorkflowState
- 실행 상태
  technical line: ExecutionStatus

authority grid:
- Human Gate
  technical line: HumanGateStatus
- Human Result
- 판정
  technical line: Judgment
- 최신 전이 결정
  technical line: TransitionDecision
- 다음 작업
  technical line: NextAction
- 런타임 모드
  technical line: RuntimeMode
```

All existing nine dimensions remain independently visible.

Responsive contract:

```text
1080px / Zoom 100%:
no horizontal scrolling required to read one WorkRun card's authority dimensions

1280px:
no horizontal scrolling required

1440px:
no horizontal scrolling required

long identifiers/actions:
wrap within their own value region
do not force card/container horizontal overflow
```

An accessible list/card (`article` + heading + `dl`/equivalent semantics) is accepted instead of `<table>`.

Do not solve this by making text illegibly small or by hiding authority dimensions.

### HQA-4 cursor pagination moves the document away from the control

Human observed:

```text
이전 / 다음 cursor 이동 시
현재 pagination 위치를 유지하지 않고 page가 위로 올라감
```

Functional cursor behavior passed, but this is a usability defect.

Required:

- cursor pagination remains AJAX/read-only;
- no full-page navigation;
- after previous/next data replacement, document viewport remains at the queue/pagination working region;
- keyboard focus remains on or is restored to the invoked pagination control or an equivalent stable queue anchor;
- filter/reset/manual refresh behavior must not introduce uncontrolled document-top jumps.

## accepted behavior that remains valid

Human QA accepted and the rework must preserve:

```text
Project ID navigation
Task metadata fallback authority
filter semantics
cursor correctness
manual refresh
ETag / 304
10-second visible/nonterminal polling
hidden-tab polling stop
terminal-only polling stop
Korean-first policy
P2-1C scope guard
read-only boundary
LOCAL_PRIVATE_ONLY
CSP/security headers
no Project catalog/index
no mutation controls
```

## current source/runtime identity before Human rework

Exact current five-file candidate:

```text
src/aiscc/api/app.py
34b9216342dc256fd319ab5c594799b9aa6784c35bc13a8b01595d4204d572f0

src/aiscc/api/routes/command_center_ui.py
05ac1ba9ce029d9b45b8aa93ee805976b97cc8b4e338af3747c14577e08122e2

src/aiscc/command_center/web.py
94a57ddc363e8d4c9a91988a1307b91a7d594363d3b781d6253c1ad7d314e240

tests/integration/command_center/test_web_ui.py
6dfeccdd1104d58e893000aaff108e3462ed707dd882ea95621c8e9ab9cc1bcb

tests/unit/command_center/test_web_shell.py
a137b53d57439ce6dbc7f4b9f4eff1c4c255d355f64b224ee8f15900c86ca451
```

Aggregate:

```text
37e1d613f457d4fda84d58b8b2b690981786e088ad03025e1dfd7a276e3bed7e
```

No Human QA evidence authorizes API route or P2-1A semantic changes.

## QA judgment

The overall Human QA result is:

```text
Human P2-1B browser QA
판정: REWORK
```

This is not converted to ACCEPTED merely because most functional Operations passed.

Human visual/usability judgment is authoritative for this gate.

## state

```text
P2:
STARTED / P2-1 ACTIVE

P2-1A:
ACCEPTED / PERSISTED

P2-1B:
HUMAN_QA_REWORK_REQUIRED

P2-1C:
NOT_STARTED
```

## preserved artifacts

Preserve:

- accepted P2-1A commit `4ea1fe6f7cb8e11ff5ccfde70462eba931c4071e`
- `.aiassistant/records/aiscc/cycles/20260903_1323_aiscc-p2-1a-read-api-foundation-persistence-final-acceptance-1.cycle.md`
- `.aiassistant/tasks/done/20260903_1325_aiscc-p2-1b-command-center-shell-and-project-task-queue-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260903_1327_aiscc-p2-1b-shell-queue-partial-acceptance-korean-first-ui-copy-rework-1.cycle.md`
- `.aiassistant/tasks/done/20260903_1329_aiscc-p2-1b-korean-first-visible-copy-and-document-language-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260903_1431_aiscc-p2-1b-shell-queue-rework-acceptance-pending-human-browser-qa-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260903_1436_aiscc-p2-1b-human-browser-qa-gate-execution-guidance-correction-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260903_1600_aiscc-p2-1b-human-browser-qa-rework-responsive-queue-and-visual-hierarchy-1.cycle.md`
- current five-file P2-1B candidate dirt until rework.

Human screenshots remain chat Human QA evidence; this Cycle records the admitted observations so repository
persistence does not depend on binary screenshot transport.

## next action

next_action:
- work_type: `REWORK / FRONTEND_IMPLEMENTATION`
- title: `P2-1B responsive queue layout and Human QA usability rework`
- blocker: `Human visual/usability REWORK`
- same_IDE_chat: `allowed`
- Human_QA_after_Command_Center_reacceptance: `required`
- P2_1C_execution: `forbidden`
