# 작업지시서: P2-1B Command Center shell and Project/task queue implementation

## meta

- task_id: `20260903_1325_aiscc-p2-1b-command-center-shell-and-project-task-queue-implementation-1`
- created_at: `2026-09-03T13:25:00+09:00`
- project: `AI Software Command Center (AISCC)`
- phase: `P2-1B — Command Center Shell + Project/Task Queue`
- work_type: `FRONTEND_IMPLEMENTATION`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `read-only operator presentation over accepted P2-1A read API`
- predecessor_head: `4ea1fe6f7cb8e11ff5ccfde70462eba931c4071e`
- predecessor_acceptance_cycle: `.aiassistant/records/aiscc/cycles/20260903_1323_aiscc-p2-1a-read-api-foundation-persistence-final-acceptance-1.cycle.md`
- accepted_design_cycle: `.aiassistant/records/aiscc/cycles/20260903_0908_aiscc-p2-1-command-center-web-ui-human-design-final-acceptance-1.cycle.md`
- target_bundle: `.aiassistant/reports/target/20260903_1325_aiscc-p2-1b-command-center-shell-and-project-task-queue-implementation-1/`
- fresh_chat_policy: `NEW_IDE_CHAT_REQUIRED / NEW_IMPLEMENTATION_SLICE_AFTER_ACCEPTED_COMMIT`
- implementation_commit_authority: `NONE`
- success_boundary: `P2_1B_IMPLEMENTATION_CANDIDATE / COMMAND_CENTER_REVIEW_AND_HUMAN_BROWSER_QA_REQUIRED`

## 0. accepted authority

P2-1A is accepted and persisted at:

```text
4ea1fe6f7cb8e11ff5ccfde70462eba931c4071e
```

Human-accepted P2-1 Web UI direction:

```text
HTML-first
same-process FastAPI
plain CSS
minimal progressive JavaScript
no Node/npm/SPA framework
read-only-first
LOCAL_PRIVATE_ONLY
```

P2-1B must consume existing `/v1/command-center/**` read APIs. It must not recreate query logic from repositories or database rows.

## 1. exact goal

1. transport current Task + exact 1323 P2-1A persistence-acceptance Cycle;
2. run in a genuinely new IDE Executor chat;
3. verify clean `main@4ea1fe6f...`;
4. implement a same-process read-only Command Center shell;
5. implement Project/task queue presentation over the existing P2-1A queue API;
6. implement project selection by explicit known project ID without creating a new Project index authority;
7. implement exact separate status/authority dimensions;
8. implement filters, pagination cursor, manual refresh and accepted conditional polling;
9. implement safe loading/empty/error/unavailable states;
10. implement local/private security headers and safe DOM handling;
11. add focused source/HTTP tests;
12. run local HTTP runtime proof;
13. export candidate evidence;
14. move current Task active→matching done;
15. stop without Git staging/commit and without Human visual acceptance claims.

## 2. non-goals / forbidden

Do not:

- implement P2-1C WorkRun detail UI;
- implement Evidence/Human/Judgment detail pages;
- implement Cycle detail page;
- implement mutating operator controls;
- add approve/rework/reject buttons;
- add workflow/evidence/Human/Judgment mutation APIs;
- add a Project-list database query or new Project index owner;
- read repositories/database directly from the UI route;
- parse `.aiassistant/tasks/done/**` or repository Markdown for UI authority;
- add Node/npm/Vite/React/Vue/Svelte/other SPA tooling;
- add template/package dependencies;
- add migrations/tables;
- modify P1 semantic owners;
- modify P2-1A API semantics unless a real defect blocks P2-1B;
- add authentication/external/shared exposure;
- implement SSE/WebSocket;
- start P2-1C/P2-2;
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

## 3. new IDE chat gate

This Task MUST run in a genuinely new IDE Executor chat.

Required before product source inspection:

```text
SESSION_AUTHORITY:
NEW_P2_1B_IMPLEMENTATION_CHAT / PASS
```

If the chat has executed P2-1A implementation/persistence or another product mutation Task:

```text
BLOCKED_REQUIRED_EVIDENCE / NEW_P2_1B_CHAT_REQUIRED
```

STOP before source mutation.

## 4. Downloads transport

Exactly two files:

```text
C:\Users\oracl\Downloads\20260903_1325_aiscc-p2-1b-command-center-shell-and-project-task-queue-implementation-1.md
C:\Users\oracl\Downloads\20260903_1323_aiscc-p2-1a-read-api-foundation-persistence-final-acceptance-1.cycle.md
```

Destinations:

```text
.aiassistant/tasks/active/20260903_1325_aiscc-p2-1b-command-center-shell-and-project-task-queue-implementation-1.md
.aiassistant/records/aiscc/cycles/20260903_1323_aiscc-p2-1a-read-api-foundation-persistence-final-acceptance-1.cycle.md
```

1323 Cycle expected SHA-256:

```text
77b9a5bd0dcca227f0a5bc7d75fde24ce9b57ca04fbbc2aba201440135a250d8
```

Before either Move require:

- both exact Downloads sources exist;
- both destinations absent;
- Cycle SHA exact.

Failure:

```text
move neither
do not search alternate Downloads path
do not overwrite/delete
STOP: TRANSPORT_PRECONDITION_FAILED
```

All PASS:

- Move exactly both, not Copy;
- verify destination identity and Downloads-source absence.

## 5. repository preflight

Require:

```text
repository == ai-software-command-center
branch == main
HEAD == 4ea1fe6f7cb8e11ff5ccfde70462eba931c4071e
index == empty
product/source/test/config/migration dirt == 0
```

After Cycle transport while current Task is active/ignored, expected Git-visible dirt is exactly:

```text
.aiassistant/records/aiscc/cycles/20260903_1323_aiscc-p2-1a-read-api-foundation-persistence-final-acceptance-1.cycle.md
```

Any additional dirt:

```text
DIRTY_WORKSPACE_MIXED / COMMAND_CENTER_REVIEW_REQUIRED
```

Do not clean or absorb it.

## 6. minimum authoritative context

Read exact:

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md
.aiassistant/rules/AISCC_SECURITY_SANDBOX.md

.aiassistant/records/aiscc/cycles/20260903_0908_aiscc-p2-1-command-center-web-ui-human-design-final-acceptance-1.cycle.md
.aiassistant/records/aiscc/cycles/20260903_1323_aiscc-p2-1a-read-api-foundation-persistence-final-acceptance-1.cycle.md
.aiassistant/tasks/active/20260903_1325_aiscc-p2-1b-command-center-shell-and-project-task-queue-implementation-1.md

src/aiscc/api/app.py
src/aiscc/api/routes/command_center.py
src/aiscc/command_center/read_models.py
src/aiscc/command_center/queries.py
```

Read exact P2-1A tests when needed to preserve API behavior.

Do not bulk-read unrelated P1 history/source.

## 7. allowed product/test paths

Preferred new files:

```text
src/aiscc/command_center/web.py
src/aiscc/api/routes/command_center_ui.py
tests/unit/command_center/test_web_shell.py
tests/integration/command_center/test_web_ui.py
```

Existing file allowed to modify:

```text
src/aiscc/api/app.py
```

No other product/test path is authorized.

If another path is necessary:

```text
IMPLEMENTATION_PATH_EXPANSION_REQUIRED
```

STOP before modifying it.

## 8. UI route contract

Implement exactly these product UI/assets routes:

```text
GET /command-center
GET /command-center/projects/{project_id}
GET /command-center/assets/app.css
GET /command-center/assets/app.js
```

HEAD/framework OPTIONS may be generated as normal framework behavior.

No POST/PUT/PATCH/DELETE UI route.

### `/command-center`

Landing shell.

Because P2-1A has no accepted Project-list authority, it MUST NOT fabricate a project catalog.

Show:

- product title: `AI Software Command Center`
- short operator description
- known Project ID input
- GET-only navigation to `/command-center/projects/<encoded-project-id>`
- explicit `LOCAL / PRIVATE / READ ONLY` presentation

No persisted form state.

### `/command-center/projects/{project_id}`

Static shell whose data authority is exclusively:

```text
GET /v1/command-center/projects/{project_id}/queue
```

The HTML route must not query repositories or PostgreSQL directly.

## 9. asset implementation boundary

No package/data-file configuration expansion is authorized.

Therefore CSS/JS may be served as same-process text responses from the new `web.py` module.

Requirements:

```text
plain CSS
plain browser JavaScript
no third-party asset
no CDN
no inline external fetch
no eval/new Function
no dynamic script injection
```

Prefer static HTML/CSS/JS constants or deterministic functions.

Runtime/API data MUST enter the DOM via safe DOM APIs such as:

```text
textContent
setAttribute with validated fixed attribute names
createElement
```

Do not place API values through `innerHTML`, `insertAdjacentHTML`, or string-built executable HTML.

## 10. security / response headers

All `/command-center/**` product UI and asset responses must include:

```text
X-AISCC-Exposure: LOCAL_PRIVATE_ONLY
X-Content-Type-Options: nosniff
Referrer-Policy: no-referrer
Cache-Control: no-store
```

HTML responses should use a CSP compatible with same-origin external-style/script routes and no third-party resources.

Target posture:

```text
default-src 'self'
script-src 'self'
style-src 'self'
connect-src 'self'
img-src 'self' data:
object-src 'none'
base-uri 'none'
frame-ancestors 'none'
form-action 'self'
```

Do not weaken CSP merely to permit inline runtime JavaScript.

## 11. queue presentation contract

Project page MUST present separate columns/cards for:

```text
Task / WorkRun
Workflow
Execution
Human Gate
Human Result
Judgment
Latest Transition Decision
Next Action
Runtime Mode
```

Never render one generic combined:

```text
Status
Overall Status
Approved
Complete
```

as authoritative truth.

### Task metadata

Use API `task_display`.

When unavailable/reference-only:

```text
title/type:
do not fabricate

visible fallback:
Task metadata unavailable
or
Reference only
```

Always display stable `task_contract.id/version` and `work_run_id`.

## 12. filters

Support UI controls that map only to accepted P2-1A query parameters:

```text
workflow_state
execution_status
human_gate_status
judgment_presence
judgment_kind
terminal
q
limit
cursor
```

Rules:

- do not create client-only semantic filters with new authority meanings;
- `q` is clearly labeled as stable-ID search;
- `limit` allowed `1..100`;
- cursor is opaque;
- previous/next behavior may retain locally observed prior cursor history for browser navigation only; it is not authoritative state.

## 13. refresh/polling contract

Manual refresh:

```text
always available
```

Automatic polling:

```text
only while document.visibilityState == "visible"
AND current rendered queue contains at least one nonterminal WorkRun
```

Interval:

```text
10000 ms
```

Terminal WorkflowState exact set for polling presentation logic:

```text
ACCEPTED
REJECTED
FAILED
```

This terminal check is presentation behavior only and must use exact P1 WorkflowState spellings.

On hidden document:

```text
stop timer
```

On visibility return:

```text
refresh once
then schedule again only if nonterminal content remains
```

Do not use SSE/WebSocket.

## 14. ETag / HTTP behavior

The queue client must preserve the last successful ETag for the current query shape and send:

```text
If-None-Match
```

on refresh.

`304`:

```text
do not clear/rebuild rows
retain current rendered data
refresh poll scheduling only
```

New query shape/filter/project:

```text
discard previous ETag
```

Handle:

```text
200
304
400
404
409
503
unexpected safe failure
```

without displaying raw server/stack/SQL/private payload.

## 15. loading / empty / error states

Required distinct states:

```text
LOADING
EMPTY
READY
INVALID_QUERY
NOT_FOUND
AUTHORITY_CONFLICT
PROJECTION_UNAVAILABLE
UNEXPECTED_ERROR
```

Human-readable copy must not reinterpret domain authority.

Examples:

```text
AUTHORITY_CONFLICT:
현재 projection을 일관된 snapshot으로 읽을 수 없습니다.

PROJECTION_UNAVAILABLE:
Command Center read projection을 현재 사용할 수 없습니다.
```

Retry is allowed only as read refresh.

## 16. navigation boundary

P2-1C WorkRun detail is not implemented yet.

Queue rows MUST NOT pretend a working detail page exists.

Allowed:

- work_run_id visible and copyable;
- disabled/non-link detail affordance labeled `Detail — P2-1C`;
- or no detail affordance.

Do not create `/command-center/work-runs/**` page in P2-1B.

## 17. presentation / accessibility

Functional desktop-first MVP.

Requirements:

- semantic heading hierarchy;
- real `<table>` for queue or accessible list equivalent;
- visible table headers;
- keyboard-accessible filters/actions;
- form labels;
- button accessible names;
- focus-visible treatment;
- state meaning conveyed by text, not color alone;
- horizontal overflow handled without document-wide broken layout;
- responsive minimum: readable at approximately 1080px viewport without requiring browser zoom changes;
- no icon-only control unless it has accessible text.

Do not add a design-system dependency.

## 18. source tests

Required targeted tests must prove at minimum:

1. exact UI route set exists.
2. no mutation UI methods are accepted.
3. `/command-center` does not enumerate projects from a repository/DB.
4. project page does not invoke read query server-side.
5. client fetch authority is exact P2-1A queue endpoint.
6. no API value path uses `innerHTML`, `insertAdjacentHTML`, `eval`, or `new Function`.
7. all product UI/assets use LOCAL_PRIVATE_ONLY + required security headers.
8. CSP contains no external origin or `unsafe-eval`.
9. generic combined status label is absent.
10. separate authority/status headings are present.
11. task metadata missing/reference-only has explicit fallback.
12. project ID navigation uses URL encoding.
13. filters map only to accepted API query names.
14. ETag is query-shape scoped.
15. `304` does not clear current rows.
16. polling is `10000ms`, visible-only, nonterminal-only.
17. hidden page stops polling.
18. P2-1C detail route is absent.
19. no external asset/CDN URL exists.
20. HTML/JS does not provide approve/rework/reject or mutation controls.

Prefer behavior/DOM-string contract tests over brittle whole-file snapshots.

## 19. HTTP runtime

Use the normal local AISCC default entrypoint and existing local PostgreSQL harness.

No test-only custom FastAPI app for the primary runtime proof.

Verify:

```text
GET /command-center → 200 HTML
GET /command-center/projects/<known-project> → 200 HTML
GET /command-center/assets/app.css → 200 CSS
GET /command-center/assets/app.js → 200 JavaScript
```

Verify required headers/CSP/content types.

With accepted P2-1A DB fixtures:

- the project page's exact queue API returns 200;
- filter query works;
- ETag/304 behavior remains operational;
- repeated UI page/asset/queue GET leaves authoritative event-count vector unchanged.

Mutation methods against UI paths:

```text
POST/PUT/PATCH/DELETE:
no mutation / rejected
```

Missing DB config:

- shell/assets may still render if source-supported;
- queue API remains safe `503 PROJECTION_UNAVAILABLE`.

Do not require Browser automation for this Task.

## 20. validation

Required:

```text
repository-local syntax/compile validation
Ruff on changed Python
mypy on changed Python
git diff --check
targeted P2-1B unit/integration
applicable full unit+integration regression
```

No package install/network.

If existing harness cannot run without environment expansion:

```text
EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

Do not substitute weaker proof.

## 21. Human browser/visual boundary

Executor MUST report:

```text
HUMAN_PENDING
```

for actual visual/usability acceptance.

Do not claim Browser QA from HTML/source/HTTP tests.

After Command Center accepts the implementation candidate, a separate Human QA Gate will be issued.

## 22. mandatory stop

STOP before scope expansion if any occurs:

```text
new package/dependency required
package-data/build configuration required
new Project index/read authority required
P2-1A API semantic change required
authentication/external exposure decision required
new product/test path outside Section 7 required
P1 semantic owner change required
migration/table required
unrelated dirty source collision
```

Return exact blocker; do not silently broaden P2-1B.

## 23. Task lifecycle

After implementation/evidence/export:

```text
.aiassistant/tasks/active/20260903_1325_aiscc-p2-1b-command-center-shell-and-project-task-queue-implementation-1.md
→
.aiassistant/tasks/done/20260903_1325_aiscc-p2-1b-command-center-shell-and-project-task-queue-implementation-1.md
```

Move, not Copy.

Do not stage or commit.

## 24. required export

Target:

```text
.aiassistant/reports/target/20260903_1325_aiscc-p2-1b-command-center-shell-and-project-task-queue-implementation-1/
```

Required root:

```text
TASK.md
EXECUTOR_REPORT.md
WEB_UI_SOURCE_EVIDENCE.md
HTTP_RUNTIME_EVIDENCE.md
HUMAN_QA_PREP.md
EXPORT_MANIFEST.md
```

Export every changed product/test file preserving repository-relative paths.

`WEB_UI_SOURCE_EVIDENCE.md` must enumerate:

- exact UI routes;
- data authority;
- headers/CSP;
- status separation;
- safe DOM contract;
- filter/query mapping;
- ETag/polling behavior;
- P2-1C exclusion.

`HUMAN_QA_PREP.md` must describe executable Human checks but must mark all as pending.

Manifest binds every payload except itself.

## 25. evidence contract

### executor_required

- new-chat authority;
- source/static contract;
- targeted unit/integration;
- normal default-entrypoint HTTP runtime;
- API no-mutation regression;
- security-header/CSP proof;
- full applicable regression;
- report/export lifecycle.

### reuse_allowed

P2-1A accepted read API semantics may be reused as data authority while baseline remains exact.

### human_owned

- Browser visual/usability QA;
- final shell/queue presentation acceptance.

### not_required

- P2-1C detail UI;
- repository Cycle UI;
- mutation controls;
- deployment;
- external network;
- public exposure.

### forbidden

- new authority owner;
- direct DB/repository UI query;
- package install;
- Git stage/commit;
- P2-1C/P2-2 implementation.

### proof non-substitution

```text
HTML source test != Browser visual QA
HTTP 200 != usability acceptance
API data != new UI authority
Human design acceptance != P2-1B implementation acceptance
```

## 26. success

Successful Executor result:

```text
P2_1B_IMPLEMENTATION_CANDIDATE
/ COMMAND_CENTER_REVIEW_AND_HUMAN_BROWSER_QA_REQUIRED
```

Do not declare:

```text
P2-1B ACCEPTED
P2-1B CLOSED
P2-1C STARTED
P2-1 ACCEPTED
P2-2 STARTED
```

## 27. preserved artifacts

Preserve:

- accepted P2-1A commit `4ea1fe6f7cb8e11ff5ccfde70462eba931c4071e`
- `.aiassistant/records/aiscc/cycles/20260903_1323_aiscc-p2-1a-read-api-foundation-persistence-final-acceptance-1.cycle.md`
- `.aiassistant/tasks/done/20260903_1325_aiscc-p2-1b-command-center-shell-and-project-task-queue-implementation-1.md` after lifecycle.

Target bundle is temporary through Command Center/Human QA review.
