# 작업지시서: P2-1C WorkRun transition/execution detail 구현

## meta

- task_id: `20260903_1759_aiscc-p2-1c-workrun-transition-execution-detail-implementation-1`
- created_at: `2026-09-03T17:59:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `FRONTEND_IMPLEMENTATION`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `NOT_APPLICABLE`
- primary_semantic_owner: `P2-1C WorkRun transition/execution detail`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_head: `62a3c5135a12afc38ba32e4c5f651c1f1b007549`

## 현재 상태

```text
P0:
CLOSED

P1:
ACCEPTED / CLOSED

P2:
STARTED / P2-1 ACTIVE

P2-1 Design:
HUMAN_PROVIDED / ACCEPTED

P2-1A:
ACCEPTED / PERSISTED

P2-1B:
ACCEPTED / PERSISTED

P2-1C:
ENTRY_AUTHORIZED / NOT_STARTED

P2-1D:
NOT_STARTED

P2-1E:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

Current accepted HEAD:

```text
62a3c5135a12afc38ba32e4c5f651c1f1b007549
```

Accepted P2-1B product/test aggregate:

```text
fe68734a4b12b3e3038d8c38dbd93b40e26481c2d8541fd88e8d95717e9454fd
```

P2-1B current UI is already Human-accepted and persisted. Do not reopen its accepted responsive queue/card design, filters,
pagination, polling, Korean-first copy, or 1080-width usability merely as cleanup/polish.

The approximately `1080px × 910px` vertical-density observation is accepted/non-blocking and deferred to P2-1E
integrated browser QA unless this Task materially worsens it.

## 이번 턴 목표

1. 기존 P2-1A read API만 사용하여 canonical WorkRun detail page를 추가한다.
2. WorkRun summary / Task-Scope reference / current WorkflowState-state_version을 읽기 전용으로 표시한다.
3. transition history를 `ADMITTED`/`DENIED` 의미를 훼손하지 않고 시간순으로 표시한다.
4. execution attempts/operations를 safe read projection 그대로 표시한다.
5. P2-1B Project queue의 각 WorkRun에서 새 detail page로 이동할 수 있게 최소 navigation만 추가한다.
6. manual refresh와 visible + nonterminal WorkRun 10-second polling을 detail page에도 적용한다.
7. P2-1B accepted shell/security/accessibility/read-only 경계를 회귀 없이 유지한다.
8. source/runtime candidate 제출 후 실제 Browser/Visual/Usability acceptance는 `HUMAN_PENDING`으로 남긴다.

## 이번 턴 비목표

- P2-1D Evidence detail 구현
- P2-1D HumanGate/HumanResult/Judgment detail 구현
- P2-1E Cycle/NextAction detail 구현
- Runtime `AdmittedCycle` detail page 구현
- workflow mutation
- evidence admission mutation
- HumanResult submit
- Judgment issue
- approve/rework/reject control
- authentication 또는 external/shared operator exposure
- Project catalog/index
- 새로운 durable Task display metadata owner
- repository Markdown Cycle indexing
- SSE/WebSocket
- Node/npm/SPA/design-system dependency
- public Replay 또는 `PUBLIC_BOUNDED_LIVE`
- P2-1B vertical-density speculative redesign

## 절대 보존해야 하는 semantic invariants

```text
WorkflowState != ExecutionStatus
HumanGateStatus != HumanResult
HumanResult != Judgment
Judgment != TransitionDecision
Agent claim != AdmittedEvidence
Executor completed != Accepted
DENIED TransitionDecision != state transition
```

UI 편의를 위해 위 차원을 하나의 generic `status`, `complete`, `approved`, `accepted`로 합치지 마라.

---

# 1. fresh IDE Executor chat gate

이번 Task는 accepted Git boundary 이후의 새 implementation slice다.

반드시 genuinely new IDE Executor chat에서 실행한다.

작업 전 report에:

```text
SESSION_AUTHORITY:
NEW_P2_1C_IMPLEMENTATION_CHAT / PASS
```

를 기록한다.

현재 IDE chat이 P2-1B implementation/rework/persistence execution history를 직접 수행한 동일 chat이면 source inspection 전에:

```text
BLOCKED_REQUIRED_EVIDENCE / NEW_P2_1C_IMPLEMENTATION_CHAT_REQUIRED
```

로 중단한다.

Executor가 새 chat을 스스로 만들 수 있다고 가정하지 않는다. Human이 새 chat을 연다.

---

# 2. Downloads transport — Move, not Copy

정확히 세 파일을 다룬다.

Sources:

```text
C:\Users\oracl\Downloads\20260903_1759_aiscc-p2-1c-workrun-transition-execution-detail-implementation-1.md

C:\Users\oracl\Downloads\20260903_1718_aiscc-p2-1b-shell-queue-persistence-final-acceptance-1.cycle.md

C:\Users\oracl\Downloads\20260903_1720_aiscc-browser-command-center-p2-1b-completion-p2-1c-entry-handoff-1.md
```

Destinations:

```text
.aiassistant/tasks/active/20260903_1759_aiscc-p2-1c-workrun-transition-execution-detail-implementation-1.md

.aiassistant/records/aiscc/cycles/20260903_1718_aiscc-p2-1b-shell-queue-persistence-final-acceptance-1.cycle.md

.aiassistant/reports/aiscc/20260903_1720_aiscc-browser-command-center-p2-1b-completion-p2-1c-entry-handoff-1.md
```

Expected SHA-256:

```text
20260903_1718_aiscc-p2-1b-shell-queue-persistence-final-acceptance-1.cycle.md
f479952b982af8d7444494d4021db443b84135324a4e4a68f09f0b30355f2488

20260903_1720_aiscc-browser-command-center-p2-1b-completion-p2-1c-entry-handoff-1.md
ca813f7cd5775d0a2d649bddae6800b4cc8ad114b7ac7110aed4e1d52f7c276d
```

Before any Move require:

- all three exact Downloads sources exist;
- all three exact destinations do not exist;
- the Cycle and Handoff source SHA-256 values exactly match above.

Any failure:

```text
move none
do not search alternate Downloads path
do not rename around browser duplicate suffixes
do not overwrite/delete an existing destination
STOP: TRANSPORT_PRECONDITION_FAILED
```

All PASS:

- Move exactly all three files, not Copy;
- verify destination files exist;
- verify exact Downloads sources are absent.

---

# 3. repository preflight

After transport and before source mutation require:

```text
repository == ai-software-command-center
branch == main
HEAD == 62a3c5135a12afc38ba32e4c5f651c1f1b007549
index == empty
```

Expected Git-visible governance dirt after transport, while current Task remains under ignored `tasks/active`:

```text
exactly:
.aiassistant/records/aiscc/cycles/20260903_1718_aiscc-p2-1b-shell-queue-persistence-final-acceptance-1.cycle.md
.aiassistant/reports/aiscc/20260903_1720_aiscc-browser-command-center-p2-1b-completion-p2-1c-entry-handoff-1.md
```

Expected product/source/test/config/migration dirt before implementation:

```text
0
```

Any additional Git-visible dirt:

```text
DIRTY_WORKSPACE_MIXED / COMMAND_CENTER_REVIEW_REQUIRED
```

Do not clean, reset, restore, stash, or absorb it.

Explicitly forbidden broad cleanup:

```text
git clean
git restore
git checkout
git reset
git stash
```

Do not delete `__pycache__`/`.pyc` residue preemptively. If tests later create ignored/untracked runtime residue, report
it precisely; cleanup is not authorized merely to make Git status look clean.

---

# 4. minimum authoritative context set

Read exact:

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md
.aiassistant/rules/AISCC_DOCUMENT_LANGUAGE_POLICY.md
.aiassistant/rules/AISCC_SECURITY_SANDBOX.md

.aiassistant/records/aiscc/cycles/20260903_0908_aiscc-p2-1-command-center-web-ui-human-design-final-acceptance-1.cycle.md
.aiassistant/records/aiscc/cycles/20260903_1718_aiscc-p2-1b-shell-queue-persistence-final-acceptance-1.cycle.md
.aiassistant/reports/aiscc/20260903_1720_aiscc-browser-command-center-p2-1b-completion-p2-1c-entry-handoff-1.md
.aiassistant/tasks/active/20260903_1759_aiscc-p2-1c-workrun-transition-execution-detail-implementation-1.md

src/aiscc/api/app.py
src/aiscc/api/routes/command_center.py
src/aiscc/api/routes/command_center_ui.py
src/aiscc/command_center/read_models.py
src/aiscc/command_center/queries.py
src/aiscc/command_center/web.py

tests/unit/command_center/test_web_shell.py
tests/integration/command_center/test_web_ui.py
```

Read existing P2-1A command-center unit/integration tests narrowly when needed to understand the exact accepted JSON field
shape for WorkRun summary, transitions, and execution.

Do not bulk-read unrelated P1 history/source. If a currently used DTO field references an exact semantic owner and its
meaning cannot be determined from the above sources, read only that exact owner path and report why it became necessary.

---

# 5. protected P2-1A read authority

P2-1C UI must use only these existing accepted endpoints:

```text
GET /v1/command-center/work-runs/{work_run_id}
GET /v1/command-center/work-runs/{work_run_id}/transitions
GET /v1/command-center/work-runs/{work_run_id}/execution
```

Do not add, change, or reinterpret backend read authority merely for UI convenience.

Protected product/API paths are read-only in this Task:

```text
src/aiscc/api/routes/command_center.py
src/aiscc/command_center/read_models.py
src/aiscc/command_center/queries.py
src/aiscc/command_center/postgres_queries.py
src/aiscc/command_center/privacy.py
```

If current accepted read DTO/API semantics are insufficient for the required P2-1C screen:

```text
P2_1A_API_CONTRACT_CHANGE_REQUIRED
```

STOP before modifying any protected read-authority path.

Required source meanings to preserve:

### WorkRun summary

Expected safe semantic surface includes:

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

If trusted scope content is unavailable:

```text
scope.availability = REFERENCE_ONLY
allowed/forbidden content remains absent
```

Do not dereference arbitrary `constraint_payload_ref`.

### transitions

Ordering is authoritative API order:

```text
decided_at ASC
transition_decision_id ASC
```

Render request/evaluation/guards/decision distinctions from the DTO.

Required semantics:

```text
decision.outcome
decision.resulting_state?
decision.resulting_state_version
derived_state_effect = CHANGED | UNCHANGED
```

A `DENIED` decision is a denied request/decision record, not a successful state transition.

Do not expose or infer requester identity beyond the accepted safe requester type.

### execution

Render accepted safe data only:

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

Forbidden UI reconstruction/display:

```text
agent/provider/tool output bodies
prompt/message bodies
encrypted/private refs
unrestricted artifact/resource identity
stack/error internals
reconstructed SecurityDecision from SECURITY_ADMITTED operation phase
```

If API returns:

```text
attempts = []
```

show an explicit empty state. Do not fabricate `ExecutionStatus`.

---

# 6. allowed product/test mutation

Preferred actual product changes:

```text
src/aiscc/api/routes/command_center_ui.py
src/aiscc/command_center/web.py
tests/unit/command_center/test_web_shell.py
tests/integration/command_center/test_web_ui.py
```

Protected existing composition file:

```text
src/aiscc/api/app.py
expected SHA-256:
34b9216342dc256fd319ab5c594799b9aa6784c35bc13a8b01595d4204d572f0
```

`src/aiscc/api/app.py` MUST remain byte-identical unless current source proves the already-registered UI router cannot
expose a new route without changing composition. If change becomes necessary:

```text
IMPLEMENTATION_PATH_EXPANSION_REQUIRED
```

STOP before modifying it.

No new product/test path is authorized.

No package/config/migration path is authorized.

P2-1A protected paths from Section 5 must remain byte-identical.

---

# 7. exact UI route boundary

Add exactly one new product HTML route:

```text
GET /command-center/work-runs/{work_run_id}
```

Existing routes remain:

```text
GET /command-center
GET /command-center/projects/{project_id}
GET /command-center/assets/app.css
GET /command-center/assets/app.js
```

HEAD/framework OPTIONS may remain normal framework behavior.

No new POST/PUT/PATCH/DELETE route.

All mutation methods against `/command-center/**` must remain non-mutating/rejected.

The WorkRun detail HTML route itself is a static same-process shell and MUST NOT directly query PostgreSQL/repositories.

Runtime data authority is browser fetch to the exact three accepted P2-1A endpoints in Section 5.

---

# 8. queue → WorkRun navigation

P2-1B terminal state intentionally had no detail route.

P2-1C may change only the directly affected navigation affordance:

```text
each rendered WorkRun card
→ visible keyboard-accessible detail link
→ /command-center/work-runs/<URL-encoded work_run_id>
```

Recommended Korean-first visible copy:

```text
WorkRun 상세
```

Do not redesign the accepted WorkRun card body, authority grid, filters, pagination, focus behavior, or queue responsive
breakpoints.

The detail link must not require a Project catalog.

Use URL encoding for `work_run_id`.

---

# 9. WorkRun detail information architecture

P2-1C owns these visible sections:

```text
1. WorkRun / Task reference
2. 현재 상태 (WorkflowState / state_version / RuntimeMode)
3. Task / Scope availability
4. blocker, when present
5. 전이 기록 (TransitionDecision timeline)
6. 실행 기록 (Execution attempts / operations)
```

P2-1D/P2-1E data MUST NOT be implemented in this Task.

Do not fetch:

```text
/evidence
/human-judgment
/outcomes
/cycles/**
/next-action
```

If the page reserves future section space, it must be non-interactive and explicitly say that the detail is not yet
implemented in the current slice. It must not display fabricated empty authoritative state.

Prefer no large placeholder sections if they create avoidable vertical density.

Navigation:

- product title or breadcrumb → `/command-center`
- after successful WorkRun summary load, Project link → `/command-center/projects/<URL-encoded project_id>`
- current `work_run_id` remains visible/copyable as text

No persisted browser state is required.

---

# 10. Korean-first visible copy

Both page language and human-facing copy remain Korean-first.

Required HTML language:

```html
<html lang="ko">
```

Exact technical identifiers/enums remain original:

```text
WorkflowState
ExecutionStatus
TransitionDecision
ADMITTED
DENIED
RUNNING
EXECUTOR_COMPLETED
OWNER_SELF_DOGFOOD
```

Recommended heading direction:

```text
WorkRun 상세
Task / 범위
현재 상태 (WorkflowState)
전이 기록 (TransitionDecision)
실행 기록 (Execution)
수동 새로고침
프로젝트 큐로
```

Do not translate canonical enum values into invented Korean enum values.

---

# 11. transition presentation contract

Use an accessible ordered timeline/list, not a wide horizontal table that requires document-level horizontal scrolling.

Each decision item should preserve, when present in accepted DTO:

```text
request target/from context
requester type
evaluation / guard results
decision id
decision outcome
decision reason
resulting_state
resulting_state_version
derived_state_effect
decided_at
```

Presentation rules:

- `ADMITTED` and `DENIED` are visibly and textually distinguishable.
- color alone must not carry the distinction.
- `DENIED` must say it did not change authoritative state when `derived_state_effect=UNCHANGED`.
- do not visually connect a denied decision as if it were a successful state transition.
- long IDs/reasons wrap inside their region.
- no hidden authority dimension behind horizontal scrolling.
- preserve API ordering; do not client-sort into a new semantic order.

If transition list is empty, render a truthful empty state.

---

# 12. execution presentation contract

Use attempt sections/cards.

Each attempt should keep separate:

```text
attempt identity / ordinal
Task contract ref
runtime mode
creation state/version
ExecutionStatus
execution version
provider registry identity
tool registry identity
durable counters
submission presence/ref
operation list
```

Operation rows/cards must show only accepted safe metadata.

Do not display a generic task success badge from `ExecutionStatus`.

Required semantic copy example:

```text
EXECUTOR_COMPLETED
→ 실행 산출 제출 완료를 의미
→ WorkRun ACCEPTED를 의미하지 않음
```

The UI may provide short help text, but must not reinterpret the domain enum.

No attempts:

```text
실행 기록 없음
```

No operations within an attempt:

```text
operation 기록 없음
```

Do not fabricate absent values.

---

# 13. detail refresh / ETag / polling

Manual refresh:

```text
always available
```

Initial page load:

```text
fetch WorkRun summary
fetch transitions
fetch execution
```

Maintain ETag independently per endpoint/query identity.

For each endpoint:

```text
send If-None-Match after first successful ETag
304:
retain currently rendered section
do not clear/rebuild it
```

Automatic polling condition:

```text
document.visibilityState == "visible"
AND last successfully rendered WorkRun WorkflowState is nonterminal
```

Interval:

```text
10000 ms
```

Terminal presentation set:

```text
ACCEPTED
REJECTED
FAILED
```

When summary becomes terminal:

```text
stop automatic polling
```

When document becomes hidden:

```text
stop timer
```

When visibility returns:

```text
if last known WorkRun is nonterminal:
refresh once
then schedule again only if still nonterminal
```

If the last successful summary is terminal, visibility return does not start automatic polling.

Manual refresh remains available for terminal WorkRuns.

Do not use SSE/WebSocket.

A manual/detail refresh should update all three owned sections as one UI refresh action, but each endpoint keeps its own
ETag and `304` behavior.

Do not make one endpoint's `304` erase another endpoint's newer `200` data.

---

# 14. loading / empty / error behavior

Each page must distinguish the overall initial load and section-level read result without exposing raw server details.

Accepted safe error codes may include:

```text
INVALID_QUERY
NOT_FOUND
AUTHORITY_CONFLICT
NO_LONGER_CURRENT
PROJECTION_UNAVAILABLE
INTERNAL_ERROR
```

Required presentation principles:

- no stack trace;
- no SQL;
- no private payload;
- no raw provider/tool/agent body;
- retry only means read refresh;
- `404 NOT_FOUND` gives a clear WorkRun-not-found state;
- `409 AUTHORITY_CONFLICT` does not render partial data as authoritative success;
- `503 PROJECTION_UNAVAILABLE` remains a truthful read-projection unavailable state;
- unexpected error uses safe Korean-first copy.

If WorkRun summary itself cannot be established as current/authoritative, do not continue presenting stale transitions
or execution as if the page is a trustworthy current snapshot. Preserve the last successful DOM only if the visual copy
clearly indicates refresh failure and does not relabel it as newly current.

No fabricated authority enum for loading/error.

---

# 15. security / safe DOM / asset boundary

Preserve all existing `/command-center/**` response headers:

```text
X-AISCC-Exposure: LOCAL_PRIVATE_ONLY
X-Content-Type-Options: nosniff
Referrer-Policy: no-referrer
Cache-Control: no-store
```

Preserve CSP posture:

```text
default-src 'self';
script-src 'self';
style-src 'self';
connect-src 'self';
img-src 'self' data:;
object-src 'none';
base-uri 'none';
frame-ancestors 'none';
form-action 'self'
```

No external asset/CDN.

No inline policy weakening.

Runtime/API values enter DOM only through safe DOM APIs such as:

```text
textContent
createElement
setAttribute with fixed validated attribute names
```

Forbidden for API-derived values:

```text
innerHTML
insertAdjacentHTML
eval
new Function
string-built executable HTML
dynamic script injection
```

Do not display secret/private values even if an unexpected payload contains them.

---

# 16. responsive/accessibility contract

Functional desktop-first MVP.

Target Human widths remain:

```text
1080
1280
1440
Zoom 100%
```

Requirements:

- no document-level horizontal scroll required to inspect transition/execution authority data;
- long IDs/reasons wrap;
- page remains keyboard navigable;
- visible `:focus-visible` treatment;
- buttons/links have accessible names;
- timeline/list semantics are screen-reader meaningful;
- loading/error/status meaning is conveyed by text, not color alone;
- no icon-only control without accessible text;
- do not reduce accepted P2-1B queue readability.

Do not solve density by shrinking text below practical readability.

---

# 17. source/unit tests

Targeted tests must prove at minimum:

1. exact new HTML route exists:
   `GET /command-center/work-runs/{work_run_id}`.
2. no new mutation route exists.
3. WorkRun detail shell does not server-side query repository/PostgreSQL.
4. detail JavaScript fetches only the exact three accepted P2-1A endpoints.
5. detail page does not fetch P2-1D/P2-1E APIs.
6. queue WorkRun card now links to URL-encoded canonical WorkRun detail route.
7. P2-1B accepted filters/pagination/card responsive structure remains present.
8. WorkRun page is `lang="ko"` and visible copy is Korean-first.
9. technical identifiers/enums remain exact.
10. no generic combined authoritative `status` presentation is introduced.
11. `ADMITTED` vs `DENIED` distinction is preserved.
12. denied decision is not rendered as successful state change.
13. execution status is not presented as acceptance.
14. empty transition list and `attempts=[]` have truthful empty states.
15. no API value path uses `innerHTML`, `insertAdjacentHTML`, `eval`, or `new Function`.
16. ETag is endpoint-scoped.
17. `304` preserves current rendered section.
18. polling interval is exactly `10000ms`.
19. hidden page stops polling.
20. terminal WorkRun stops polling.
21. visibility return refreshes only last-known nonterminal WorkRun automatically.
22. all `/command-center/**` UI/assets preserve required security headers/CSP.
23. no external asset/CDN appears.
24. `src/aiscc/api/app.py` remains exact unless mandatory stop was triggered.
25. P2-1A protected read-authority files remain byte-identical.

Prefer semantic/DOM behavior tests over brittle whole-file snapshots.

---

# 18. HTTP/runtime evidence

Use the normal AISCC local loopback default entrypoint and existing local PostgreSQL test harness already accepted for
P2-1A/P2-1B.

No test-only custom FastAPI app for primary runtime proof.

Required runtime checks:

```text
GET /command-center → 200 HTML
GET /command-center/projects/<known-project> → 200 HTML
GET /command-center/work-runs/<known-work-run> → 200 HTML
GET /command-center/assets/app.css → 200 CSS
GET /command-center/assets/app.js → 200 JavaScript
```

Verify required headers/CSP/content types.

With accepted fixture data containing at least one WorkRun with transition history and execution data:

```text
GET /v1/command-center/work-runs/<known-work-run> → 200
GET /v1/command-center/work-runs/<known-work-run>/transitions → 200
GET /v1/command-center/work-runs/<known-work-run>/execution → 200
```

Verify:

- detail page uses only these endpoints;
- ETag/304 works independently on them;
- repeated UI/detail/API GET does not mutate authoritative event-count/state;
- mutation methods against UI routes remain rejected/no mutation.

If a terminal WorkRun fixture exists, use it for source/runtime polling-contract support where current harness can
observe it without Browser automation.

Do not claim actual tab-visibility/user visual behavior from HTTP tests.

Missing DB configuration remains safe:

```text
shell/assets/detail HTML may render if source-supported
read APIs → safe 503 PROJECTION_UNAVAILABLE
```

No external network/package install.

If the accepted local harness cannot satisfy required runtime proof without new environment/scope:

```text
EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

STOP; do not substitute weaker proof.

---

# 19. validation

Required:

```text
repository-local syntax/compile validation
Ruff on changed Python
mypy on changed Python
git diff --check
targeted P2-1C unit/integration tests
applicable full unit + integration regression
```

Use current project tooling only.

No package install/network.

---

# 20. evidence contract

executor_required:

- channel: `STATIC_SOURCE`
  scope: exact allowed-path implementation and protected-path identity
  pass_condition: route/data-authority/security/read-only/invariant contracts match

- channel: `UNIT_TEST`
  scope: P2-1C UI source/DOM/polling/ETag/navigation semantics
  pass_condition: targeted tests pass

- channel: `INTEGRATION_TEST`
  scope: existing FastAPI + PostgreSQL command-center read path
  pass_condition: focused P2-1C integration passes with no mutation

- channel: `HTTP_RUNTIME`
  scope: normal local loopback entrypoint and exact P2-1C routes/read endpoints
  pass_condition: required status/content/security/ETag behavior passes

- channel: `BUILD`
  scope: syntax/compile + Ruff + mypy + git diff --check
  pass_condition: all required checks pass

reuse_allowed:

- P2-1A accepted read API semantics may be reused as authority if protected read files remain byte-identical.
- P2-1B Human responsive acceptance may be reused for unchanged queue behavior only.
- P2-1B Human QA does not count as Human QA for the new WorkRun detail page.

human_owned:

- channel: `HUMAN_VERIFICATION`
  scope:
    - WorkRun detail visual hierarchy
    - transition admitted/denied comprehensibility
    - execution detail readability
    - queue→detail→project navigation usability
    - 1080/1280/1440 responsive usability
    - actual browser focus/visibility/polling user-observable behavior as selected by later Human QA Gate
  expected_result: `HUMAN_PENDING` in Executor report

not_required:

- `DATABASE_MIGRATION`
- `EXTERNAL_NETWORK`
- `PUBLIC_DEPLOYMENT`
- `AUTHENTICATION`
- `P2-1D Evidence/Human/Judgment UI`
- `P2-1E Cycle/NextAction UI`
- `PUBLIC_BOUNDED_LIVE`

forbidden:

- workflow/evidence/Human/Judgment mutation
- approve/rework/reject UI
- backend read-model semantic change
- P1 semantic owner change
- package install
- external network
- Git index/commit/push
- broad cleanup/reset/restore/stash

proof_non_substitution:

```text
source test != browser visual QA
HTTP runtime != browser visual QA
P2-1B Human QA != P2-1C detail Human QA
ExecutionStatus != WorkflowState
DENIED TransitionDecision != state transition
Executor report != Command Center acceptance
```

---

# 21. Human Browser/Visual boundary

Executor MUST finish the implementation turn with:

```text
HUMAN_PENDING
```

for P2-1C visual/usability acceptance.

Do not launch Browser automation unless this Task explicitly authorizes it; it does not.

After Browser Command Center substantive source/runtime review, Command Center will determine the exact Human QA Gate.

---

# 22. mandatory stop conditions

STOP before scope expansion for any of:

```text
TRANSPORT_PRECONDITION_FAILED
NEW_P2_1C_IMPLEMENTATION_CHAT_REQUIRED
DIRTY_WORKSPACE_MIXED
P2_1A_API_CONTRACT_CHANGE_REQUIRED
IMPLEMENTATION_PATH_EXPANSION_REQUIRED
new package/dependency required
package/build/repository config change required
new table/migration required
new Project index/read authority required
new Task metadata authority required
authentication/external exposure decision required
P1 semantic owner/rule change required
P2-1D/P2-1E data required to make P2-1C function
external network required
EVIDENCE_SCOPE_EXPANSION_REQUIRED
security/privacy boundary uncertainty
```

Named blocker 이후에는 blocker를 입증하는 최소 evidence, workspace inventory, report/export와 안전한 종료만 수행한다.

Do not continue unrelated tests or mutation after the blocker.

---

# 23. Task lifecycle

After executor-required implementation/evidence/export is complete:

```text
.aiassistant/tasks/active/20260903_1759_aiscc-p2-1c-workrun-transition-execution-detail-implementation-1.md
→
.aiassistant/tasks/done/20260903_1759_aiscc-p2-1c-workrun-transition-execution-detail-implementation-1.md
```

Move, not Copy.

`tasks/done` means Executor submission-ready only.

It does NOT mean:

```text
Command Center accepted
P2-1C accepted
P2-1 accepted/closed
```

Do not stage or commit.

---

# 24. required export

Target:

```text
.aiassistant/reports/target/20260903_1759_aiscc-p2-1c-workrun-transition-execution-detail-implementation-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
```

Include changed files preserving repository-relative paths.

Include `REMOVED_FILES.md` only if deletion exists.

Expected product/test export is limited to actual changed allowed paths.

Do not export unchanged P2-1A read-authority files merely as evidence.

Report exact SHA-256 for:

- changed product/test files;
- protected P2-1A read-authority files used for identity checks when Task requires them;
- `src/aiscc/api/app.py`.

Report a deterministic aggregate for actual changed product/test files:

```text
<case-sensitive repository-relative path>\t<lowercase_sha256>\n
```

sorted by repository-relative path.

Do not include:

- prior target bundles;
- cache/bytecode;
- DB data dump;
- env/credentials;
- private provider/tool output;
- unrelated source.

---

# 25. 보고서 필수 항목

- 작업명 / work type / Task path
- `SESSION_AUTHORITY`
- Downloads transport result and exact SHA verification
- repository/branch/base HEAD/index/worktree before
- minimum authoritative paths actually read
- product source changes
- governance/provenance changes
- repository configuration changes
- added/modified/removed files
- protected path identity results
- exact new UI route inventory
- exact API fetch authority inventory
- P2-1B regression boundary
- WorkRun summary presentation
- transition ADMITTED/DENIED presentation semantics
- execution attempts/operations presentation semantics
- polling/ETag/visibility behavior
- Korean-first compliance
- safe DOM/security header/CSP result
- evidence contract classification
- human verification: `HUMAN_PENDING`
- forbidden-not-run
- mandatory stop/scope expansion
- test/runtime/build results
- authoritative event/state no-mutation result
- unverified items
- runtime/container/env residue
- rollback/revert guide
- preserved artifact exact paths
- next-turn recommendation

---

# 26. accept 기준

Command Center substantive review candidate가 되려면 최소:

```text
new canonical WorkRun detail route implemented
queue→detail navigation implemented with no P2-1B redesign
exact 3 P2-1A read endpoints only
P2-1A protected read authority unchanged
Task/Scope reference semantics truthful
WorkflowState/state_version separate
transition ADMITTED/DENIED semantics correct
DENIED not shown as state change
execution status not shown as acceptance
read-only / no mutation control
Korean-first
safe DOM
LOCAL_PRIVATE_ONLY + CSP preserved
ETag/304 preserved
10-second visible/nonterminal polling preserved
targeted tests PASS
applicable full unit+integration PASS
normal local HTTP runtime PASS
Ruff/mypy/diff-check PASS
Human Browser/Visual = HUMAN_PENDING
```

## hold/reject 기준

Examples:

```text
generic combined status
DENIED rendered as successful transition
ExecutionStatus treated as acceptance
new backend/read authority invented for UI convenience
P2-1A protected path changed
P2-1D/P2-1E scope pulled forward
queue responsive design regressed without necessity
unsafe DOM insertion
CSP/security weakening
mutation UI or route added
Human QA falsely claimed
unexpected dirty workspace absorbed
mandatory stop ignored
```

---

# 27. preserved artifacts

This Task must explicitly preserve:

```text
.aiassistant/tasks/done/20260903_1759_aiscc-p2-1c-workrun-transition-execution-detail-implementation-1.md

.aiassistant/records/aiscc/cycles/20260903_1718_aiscc-p2-1b-shell-queue-persistence-final-acceptance-1.cycle.md

.aiassistant/reports/aiscc/20260903_1720_aiscc-browser-command-center-p2-1b-completion-p2-1c-entry-handoff-1.md

P2-1A commit:
4ea1fe6f7cb8e11ff5ccfde70462eba931c4071e

P2-1B commit:
62a3c5135a12afc38ba32e4c5f651c1f1b007549
```

Target bundle is temporary Command Center review material and is deletable after terminal judgment unless later explicitly
preserved.

---

# 28. 최종 응답 형식

1. result: `completed / blocked / rejected-candidate`
2. target bundle path
3. changed files
4. removed files
5. protected-path identity result
6. tests/runtime evidence
7. human verification
8. unverified items
9. preserved exact paths
