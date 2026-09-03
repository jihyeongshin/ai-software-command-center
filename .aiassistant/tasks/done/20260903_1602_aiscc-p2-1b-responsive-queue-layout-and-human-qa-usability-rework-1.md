# 작업지시서: P2-1B responsive queue layout and Human QA usability rework

## meta

- task_id: `20260903_1602_aiscc-p2-1b-responsive-queue-layout-and-human-qa-usability-rework-1`
- created_at: `2026-09-03T16:02:00+09:00`
- project: `AI Software Command Center (AISCC)`
- phase: `P2-1B — Command Center Shell + Project/Task Queue`
- work_type: `REWORK / FRONTEND_IMPLEMENTATION`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- predecessor_head: `4ea1fe6f7cb8e11ff5ccfde70462eba931c4071e`
- predecessor_task: `.aiassistant/tasks/done/20260903_1329_aiscc-p2-1b-korean-first-visible-copy-and-document-language-rework-1.md`
- predecessor_source_runtime_cycle: `.aiassistant/records/aiscc/cycles/20260903_1431_aiscc-p2-1b-shell-queue-rework-acceptance-pending-human-browser-qa-1.cycle.md`
- human_qa_cycle: `.aiassistant/records/aiscc/cycles/20260903_1600_aiscc-p2-1b-human-browser-qa-rework-responsive-queue-and-visual-hierarchy-1.cycle.md`
- target_bundle: `.aiassistant/reports/target/20260903_1602_aiscc-p2-1b-responsive-queue-layout-and-human-qa-usability-rework-1/`
- fresh_chat_policy: `REUSE_CURRENT_P2_1B_IMPLEMENTATION_CHAT_ALLOWED`
- implementation_commit_authority: `NONE`
- success_boundary: `P2_1B_HUMAN_QA_REWORK_CANDIDATE / COMMAND_CENTER_REVIEW_AND_HUMAN_REQA_REQUIRED`

## 0. Human authority

Human Browser QA result:

```text
P2-1B:
REWORK
```

Functional/API behavior largely passed.

This Task fixes only the Human-owned visual/usability defects admitted in the 1600 Cycle.

## 1. exact goals

1. transport the exact current Task and exact pending governance/Human QA Cycles;
2. reuse the current P2-1B implementation chat;
3. verify exact current five-file source/test candidate identity;
4. fix landing Project-ID field spacing/focus presentation;
5. normalize filter and queue label hierarchy;
6. replace the 9-column queue table with a responsive accessible WorkRun card/list;
7. preserve all nine independent authority dimensions;
8. ensure no horizontal scroll is required for WorkRun authority reading at 1080/1280/1440 Zoom 100%;
9. preserve cursor pagination viewport/focus instead of jumping to document top;
10. preserve accepted P2-1B API/security/ETag/polling/no-mutation behavior;
11. update focused source/integration tests;
12. run normal local HTTP/runtime regression;
13. export candidate evidence;
14. move current Task active→matching done;
15. stop without stage/commit and with Human re-QA still pending.

## 2. Downloads transport

Transport exactly four new files.

### Task

```text
C:\Users\oracl\Downloads\20260903_1602_aiscc-p2-1b-responsive-queue-layout-and-human-qa-usability-rework-1.md
→
.aiassistant/tasks/active/20260903_1602_aiscc-p2-1b-responsive-queue-layout-and-human-qa-usability-rework-1.md
```

### 1431 source/runtime acceptance Cycle

```text
C:\Users\oracl\Downloads\20260903_1431_aiscc-p2-1b-shell-queue-rework-acceptance-pending-human-browser-qa-1.cycle.md
→
.aiassistant/records/aiscc/cycles/20260903_1431_aiscc-p2-1b-shell-queue-rework-acceptance-pending-human-browser-qa-1.cycle.md

expected SHA-256:
ea3b7168e4e9305d0e9fa4a97116d7985620a377432955fdc67b856ecf958e14
```

### 1436 QA guidance correction Cycle

```text
C:\Users\oracl\Downloads\20260903_1436_aiscc-p2-1b-human-browser-qa-gate-execution-guidance-correction-1.cycle.md
→
.aiassistant/records/aiscc/cycles/20260903_1436_aiscc-p2-1b-human-browser-qa-gate-execution-guidance-correction-1.cycle.md

expected SHA-256:
cbb020189e6d454c95afdbe80700d19d267d6a7adebf6191794d0d2bb574d67a
```

### 1600 Human QA rework Cycle

```text
C:\Users\oracl\Downloads\20260903_1600_aiscc-p2-1b-human-browser-qa-rework-responsive-queue-and-visual-hierarchy-1.cycle.md
→
.aiassistant/records/aiscc/cycles/20260903_1600_aiscc-p2-1b-human-browser-qa-rework-responsive-queue-and-visual-hierarchy-1.cycle.md

expected SHA-256:
90ee4190da63e0847dbb0d33854849caa6645fbcac96d6466a42e3455b2c2d9b
```

Precheck all four exact sources and destination identities before moving any newly absent-destination file.

For a Cycle destination that already exists, require exact SHA and do not move a duplicate.

Any conflict:

```text
TRANSPORT_PRECONDITION_FAILED
```

No alternate Downloads path search.

Move, not Copy.

## 3. session authority

Reuse current P2-1B implementation chat.

Required lineage:

```text
1325 P2-1B implementation
→ 1329 Korean-first rework
→ 1602 Human-QA usability rework
```

If another unrelated product mutation Task executed in the chat:

```text
SESSION_LINEAGE_CONFLICT
```

STOP.

## 4. repository baseline

Require:

```text
repository == ai-software-command-center
branch == main
HEAD == 4ea1fe6f7cb8e11ff5ccfde70462eba931c4071e
index == empty
```

Current product/test dirt must be exact:

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

aggregate:
37e1d613f457d4fda84d58b8b2b690981786e088ad03025e1dfd7a276e3bed7e
```

Expected pre-existing governance dirt before 1431/1436/1600 transport:

```text
.aiassistant/records/aiscc/cycles/20260903_1323_aiscc-p2-1a-read-api-foundation-persistence-final-acceptance-1.cycle.md
.aiassistant/tasks/done/20260903_1325_aiscc-p2-1b-command-center-shell-and-project-task-queue-implementation-1.md
.aiassistant/records/aiscc/cycles/20260903_1327_aiscc-p2-1b-shell-queue-partial-acceptance-korean-first-ui-copy-rework-1.cycle.md
.aiassistant/tasks/done/20260903_1329_aiscc-p2-1b-korean-first-visible-copy-and-document-language-rework-1.md
```

No unrelated dirt may be cleaned or absorbed.

## 5. authoritative context

Read exact:

```text
.aiassistant/rules/AISCC_DOCUMENT_LANGUAGE_POLICY.md
.aiassistant/rules/AISCC_SECURITY_SANDBOX.md
.aiassistant/records/aiscc/cycles/20260903_1431_aiscc-p2-1b-shell-queue-rework-acceptance-pending-human-browser-qa-1.cycle.md
.aiassistant/records/aiscc/cycles/20260903_1436_aiscc-p2-1b-human-browser-qa-gate-execution-guidance-correction-1.cycle.md
.aiassistant/records/aiscc/cycles/20260903_1600_aiscc-p2-1b-human-browser-qa-rework-responsive-queue-and-visual-hierarchy-1.cycle.md
.aiassistant/tasks/active/20260903_1602_aiscc-p2-1b-responsive-queue-layout-and-human-qa-usability-rework-1.md

src/aiscc/command_center/web.py
tests/unit/command_center/test_web_shell.py
tests/integration/command_center/test_web_ui.py
```

Read `src/aiscc/api/app.py` / `command_center_ui.py` only to confirm protected identity if needed.

## 6. allowed product/test mutation

Preferred actual modifications:

```text
src/aiscc/command_center/web.py
tests/unit/command_center/test_web_shell.py
tests/integration/command_center/test_web_ui.py
```

Protected byte-identical files:

```text
src/aiscc/api/app.py
SHA-256:
34b9216342dc256fd319ab5c594799b9aa6784c35bc13a8b01595d4204d572f0

src/aiscc/api/routes/command_center_ui.py
SHA-256:
05ac1ba9ce029d9b45b8aa93ee805976b97cc8b4e338af3747c14577e08122e2
```

No new product/test path.

If another path is required:

```text
IMPLEMENTATION_PATH_EXPANSION_REQUIRED
```

STOP before modifying it.

## 7. HQA-1 landing input spacing/focus

Fix the known Project ID form.

Required source/presentation contract:

- label/input vertical separation visibly clear;
- input focus ring does not collide with label;
- one coherent focus indication;
- blur restores the normal border;
- no yellow/orange competing double-outline effect;
- keyboard focus remains clearly visible;
- layout remains stable at 1080/1280/1440.

Do not remove focus-visible accessibility.

## 8. HQA-2 consistent label grammar

Create one reusable visual grammar for filter labels and authority labels.

Required:

```text
primary:
Korean human-facing label

secondary:
exact technical identifier
```

Examples:

```text
워크플로
WorkflowState

실행 상태
ExecutionStatus

사람 검토 관문
HumanGateStatus

판정 존재 여부
Judgment

판정 종류
JudgmentKind

종료 워크플로 여부
terminal
```

No arbitrary:

```text
Korean (Technical)
Korean / Technical
English-only
```

mixture for equivalent authority labels.

Technical secondary lines must use a consistent size/weight/color and predictable wrapping.

Exact enum values remain untranslated.

## 9. HQA-3 responsive queue redesign

The 9-column `<table>` is rejected as the primary queue representation.

Replace it with an accessible WorkRun list/card structure.

Preferred semantics:

```html
<section aria-label="프로젝트 큐">
  <article>...</article>
  <article>...</article>
</section>
```

Each WorkRun card must expose all independent dimensions.

### card identity area

Display:

```text
Task metadata availability
TaskContract ID
TaskContract version
WorkRun ID
```

Long IDs:

```text
overflow-wrap:anywhere
word-break only where necessary
```

Do not hide/truncate authoritative IDs without a full accessible value.

### state strip

Exactly separate:

```text
워크플로
WorkflowState
<exact value>

실행 상태
ExecutionStatus
<exact value or absence explanation>
```

Do not merge into one status badge.

### authority grid

Exactly separate:

```text
사람 검토 관문
HumanGateStatus

Human Result

판정
Judgment

최신 전이 결정
TransitionDecision

다음 작업
NextAction

런타임 모드
RuntimeMode
```

Presence/detail fields remain as accepted from P2-1A.

### responsive layout

Primary acceptance targets:

```text
1080px / Zoom 100%
1280px / Zoom 100%
1440px / Zoom 100%
```

At all three:

- no horizontal scrollbar is required to inspect all dimensions of one WorkRun;
- card itself fits the content region;
- long NextAction/ID values wrap inside their value cell;
- no authority dimension is hidden/collapsed because of viewport width;
- no font-size reduction below the existing readable body-text baseline merely to force fit.

Recommended CSS behavior:

```text
identity:
full-width

state strip:
2 columns when space permits

authority grid:
responsive CSS grid using minmax(0, 1fr)
3 columns around desktop widths where readable
2 columns at narrower widths if necessary
1 column only below the primary desktop target
```

Do not hard-code a width that again requires approximately 1880px.

No horizontal queue-card scroll rail.

### accessibility

Each card must have an accessible WorkRun heading/label.

Use semantic `<dl>/<dt>/<dd>` or equivalent accessible grouping for authority dimensions.

State meaning must not rely on color alone.

## 10. HQA-4 pagination viewport/focus retention

Trace the exact reason current cursor previous/next causes the document to move to top.

Required result:

```text
previous/next:
AJAX only
no page reload/navigation
```

After data replacement:

- maintain the user's working viewport around the queue/pagination region;
- preserve scroll position where possible;
- if DOM replacement/focus behavior requires adjustment, restore focus to the invoked pagination button or a stable
  queue heading without scrolling the document to top;
- do not call `window.scrollTo(0, 0)`;
- do not use focus behavior that implicitly scrolls the page to top;
- no hash navigation.

Filter Apply / Reset / Refresh should not introduce a new uncontrolled top jump.

## 11. behavior that must remain unchanged

Preserve:

```text
GET /command-center
GET /command-center/projects/{project_id}
GET /command-center/assets/app.css
GET /command-center/assets/app.js

P2-1A queue API as sole data authority
no direct DB/repository UI read
no Project catalog/index
Task metadata REFERENCE_ONLY behavior
filter query names/semantics
limit 1..100
opaque cursor semantics
ETag query-shape scoping
If-None-Match / 304
manual refresh
10000ms visible/nonterminal polling
hidden-tab stop
terminal ACCEPTED/REJECTED/FAILED polling stop
safe DOM APIs
Korean-first visible copy
LOCAL_PRIVATE_ONLY
CSP/security headers
no mutation controls
no P2-1C detail route
```

## 12. source tests

Required new/updated assertions:

1. landing label/input structure has explicit spacing class/contract.
2. focus style does not use a conflicting double-outline treatment.
3. filter labels use consistent primary + technical secondary markup.
4. legacy 9-column queue table is absent.
5. WorkRun list/card semantics are present.
6. every card retains all nine independent authority dimensions.
7. WorkflowState and ExecutionStatus remain separate.
8. long ID/NextAction CSS uses wrapping instead of horizontal card overflow.
9. primary queue/card CSS does not require a large fixed/min width producing desktop horizontal scroll.
10. 1080/1280/1440 responsive CSS rules preserve 2/3-column authority grid behavior.
11. no queue horizontal-scroll wrapper remains as the primary usability mechanism.
12. cursor next/previous does not perform location/navigation.
13. cursor next/previous contains no top-scroll command.
14. pagination focus restoration uses a stable control/anchor without forced top scroll.
15. ETag/polling/filter/safe-DOM/security tests continue to pass.
16. protected `app.py` and `command_center_ui.py` SHA-256 remain exact.

Do not use a full-page visual snapshot as a substitute for Human re-QA.

## 13. local HTTP/runtime verification

Use the existing accepted disposable PostgreSQL harness and normal:

```text
python -m aiscc serve
```

entrypoint.

Verify:

- landing/project/assets 200;
- queue API still 200 with accepted fixture;
- card/list markup is served by project shell;
- exact Project ID visible;
- filter API requests unchanged;
- cursor previous/next still return correct rows;
- ETag/304 remains;
- visible/nonterminal polling source contract remains;
- repeated page/asset/API GET leaves authoritative event-count vector unchanged;
- POST/PUT/PATCH/DELETE remain no-mutation/rejected.

No Browser visual acceptance claim.

## 14. validation

Required:

```text
repository-local syntax/compile
Ruff changed Python
mypy changed Python
git diff --check
targeted P2-1B unit/integration
applicable full unit+integration regression
```

No package install/network.

## 15. Human re-QA preparation

Required root report:

```text
HUMAN_REQA_PREP.md
```

It must list only the Human checks that need visual re-verification:

```text
R1 landing label/input spacing + focus
R2 filter label consistency
R3 queue card readability at 1080
R4 queue card readability at 1280
R5 queue card readability at 1440
R6 all nine dimensions visible without horizontal queue scroll
R7 pagination previous/next viewport retention
R8 keyboard/focus after pagination
```

It may also tell Human to spot-check already-passed polling/ETag controls but must not force a complete redo of all
13 operations unless Command Center review finds behavioral drift.

Human status remains:

```text
HUMAN_PENDING
```

## 16. mandatory stop

STOP if rework requires:

```text
P2-1A API semantic change
new product/test path
new dependency/build tool
new Project authority
P1 semantic change
authentication/exposure change
migration/table
P2-1C implementation
unrelated dirty cleanup
```

## 17. Task lifecycle

After implementation/evidence/export:

```text
.aiassistant/tasks/active/20260903_1602_aiscc-p2-1b-responsive-queue-layout-and-human-qa-usability-rework-1.md
→
.aiassistant/tasks/done/20260903_1602_aiscc-p2-1b-responsive-queue-layout-and-human-qa-usability-rework-1.md
```

Move, not Copy.

Do not stage or commit.

## 18. export

Target:

```text
.aiassistant/reports/target/20260903_1602_aiscc-p2-1b-responsive-queue-layout-and-human-qa-usability-rework-1/
```

Required root:

```text
TASK.md
EXECUTOR_REPORT.md
RESPONSIVE_QUEUE_SOURCE_EVIDENCE.md
HTTP_RUNTIME_EVIDENCE.md
HUMAN_REQA_PREP.md
EXPORT_MANIFEST.md
```

Export the full five-file current P2-1B candidate preserving repository-relative paths.

Manifest binds every payload except itself.

## 19. success

Successful Executor result:

```text
P2_1B_HUMAN_QA_REWORK_CANDIDATE
/ RESPONSIVE_QUEUE_AND_USABILITY_REWORK_COMPLETE
/ COMMAND_CENTER_REVIEW_AND_HUMAN_REQA_REQUIRED
```

Do not declare:

```text
P2-1B ACCEPTED
Human QA ACCEPTED
P2-1C STARTED
P2-1 ACCEPTED
P2-2 STARTED
```

## 20. preserved artifacts

Preserve:

- accepted P2-1A commit `4ea1fe6f7cb8e11ff5ccfde70462eba931c4071e`
- `.aiassistant/records/aiscc/cycles/20260903_1431_aiscc-p2-1b-shell-queue-rework-acceptance-pending-human-browser-qa-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260903_1436_aiscc-p2-1b-human-browser-qa-gate-execution-guidance-correction-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260903_1600_aiscc-p2-1b-human-browser-qa-rework-responsive-queue-and-visual-hierarchy-1.cycle.md`
- `.aiassistant/tasks/done/20260903_1602_aiscc-p2-1b-responsive-queue-layout-and-human-qa-usability-rework-1.md` after lifecycle
- current five-file P2-1B rework candidate dirt.

Target bundle remains temporary through Command Center/Human re-QA.
