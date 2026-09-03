# 작업지시서: P2-1B Korean-first visible copy and document-language rework

## meta

- task_id: `20260903_1329_aiscc-p2-1b-korean-first-visible-copy-and-document-language-rework-1`
- created_at: `2026-09-03T13:29:00+09:00`
- project: `AI Software Command Center (AISCC)`
- phase: `P2-1B — Command Center Shell + Project/Task Queue`
- work_type: `REWORK / FRONTEND_IMPLEMENTATION`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- predecessor_head: `4ea1fe6f7cb8e11ff5ccfde70462eba931c4071e`
- predecessor_task: `.aiassistant/tasks/done/20260903_1325_aiscc-p2-1b-command-center-shell-and-project-task-queue-implementation-1.md`
- predecessor_judgment_cycle: `.aiassistant/records/aiscc/cycles/20260903_1327_aiscc-p2-1b-shell-queue-partial-acceptance-korean-first-ui-copy-rework-1.cycle.md`
- accepted_candidate_aggregate_sha256: `a8157f255ff6ec2bf87a3a47a2f51b520f0322bb17fe320d591b3859cbc6333c`
- target_bundle: `.aiassistant/reports/target/20260903_1329_aiscc-p2-1b-korean-first-visible-copy-and-document-language-rework-1/`
- fresh_chat_policy: `REUSE_CURRENT_P2_1B_IMPLEMENTATION_CHAT_ALLOWED`
- implementation_commit_authority: `NONE`
- success_boundary: `P2_1B_REWORK_CANDIDATE / COMMAND_CENTER_REVIEW_AND_HUMAN_BROWSER_QA_REQUIRED`

## 0. rework cause

Current UI implementation is structurally/runtime acceptable but violates:

```text
.aiassistant/rules/AISCC_DOCUMENT_LANGUAGE_POLICY.md
```

because human-facing screen copy is English-first and documents use:

```text
<html lang="en">
```

Canonical requirement:

```text
사용자 화면 copy:
Korean-first

technical identifier:
원문 유지
```

Human Browser QA must remain pending until this policy conflict is corrected.

## 1. exact goal

1. transport exact current Task + exact 1327 rework Cycle;
2. reuse the current P2-1B implementation chat;
3. verify exact current five-file candidate identity;
4. read the canonical document-language policy directly;
5. change only human-facing shell/queue visible copy, accessibility copy, and HTML document language to Korean-first;
6. preserve technical identifiers and exact enum/state values;
7. preserve all accepted API/data/security/polling/ETag behavior;
8. update focused UI source tests for the Korean-first contract;
9. rerun narrow source/runtime/regression evidence;
10. export rework candidate;
11. move current Task active→matching done;
12. stop without Git staging/commit and without Human visual acceptance claims.

## 2. Downloads transport

Exactly two new files:

```text
C:\Users\oracl\Downloads\20260903_1329_aiscc-p2-1b-korean-first-visible-copy-and-document-language-rework-1.md
C:\Users\oracl\Downloads\20260903_1327_aiscc-p2-1b-shell-queue-partial-acceptance-korean-first-ui-copy-rework-1.cycle.md
```

Destinations:

```text
.aiassistant/tasks/active/20260903_1329_aiscc-p2-1b-korean-first-visible-copy-and-document-language-rework-1.md
.aiassistant/records/aiscc/cycles/20260903_1327_aiscc-p2-1b-shell-queue-partial-acceptance-korean-first-ui-copy-rework-1.cycle.md
```

1327 Cycle expected SHA-256:

```text
7460ee73c5b3af13181dd9876436d37b69574ca7cd3f8c9afbff79c78df546b4
```

Precheck both exact Downloads sources, absent destinations, and Cycle hash before moving either.

Failure:

```text
TRANSPORT_PRECONDITION_FAILED
```

All PASS:

- Move, not Copy;
- verify exact destination identity and Downloads-source absence.

## 3. session

Reuse the current P2-1B implementation chat.

Required lineage:

```text
1325 P2-1B implementation
→ 1329 same-slice copy/policy rework
```

If another unrelated product mutation Task has executed in this chat:

```text
SESSION_LINEAGE_CONFLICT
```

STOP before source mutation.

## 4. repository / dirty baseline

Require:

```text
repository == ai-software-command-center
branch == main
HEAD == 4ea1fe6f7cb8e11ff5ccfde70462eba931c4071e
index == empty
```

Current product/test dirt MUST be exactly:

```text
src/aiscc/api/app.py
src/aiscc/api/routes/command_center_ui.py
src/aiscc/command_center/web.py
tests/integration/command_center/test_web_ui.py
tests/unit/command_center/test_web_shell.py
```

Exact pre-rework identity:

```text
src/aiscc/api/app.py
34b9216342dc256fd319ab5c594799b9aa6784c35bc13a8b01595d4204d572f0

src/aiscc/api/routes/command_center_ui.py
05ac1ba9ce029d9b45b8aa93ee805976b97cc8b4e338af3747c14577e08122e2

src/aiscc/command_center/web.py
f3a8230ac3d58586fdaf08f1880a6839b8fa2786e0868573b3c171c76e89d5c7

tests/integration/command_center/test_web_ui.py
92d687a0d54ecac12a94c3e4c934b2f1d16f47a7e518e28fbd88fe76199ab8cf

tests/unit/command_center/test_web_shell.py
b4fa4afdf333607161c0bf8d77334e1b1fbdd8e55b678c10f8f1b12c62da4d49

aggregate:
a8157f255ff6ec2bf87a3a47a2f51b520f0322bb17fe320d591b3859cbc6333c
```

Pre-existing governance/provenance dirt before 1327 transport:

```text
.aiassistant/records/aiscc/cycles/20260903_1323_aiscc-p2-1a-read-api-foundation-persistence-final-acceptance-1.cycle.md
.aiassistant/tasks/done/20260903_1325_aiscc-p2-1b-command-center-shell-and-project-task-queue-implementation-1.md
```

After 1327 transport add only the exact 1327 Cycle.

Do not clean or absorb any unrelated path.

## 5. authoritative context

Read exact:

```text
.aiassistant/rules/AISCC_DOCUMENT_LANGUAGE_POLICY.md
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md

.aiassistant/records/aiscc/cycles/20260903_1327_aiscc-p2-1b-shell-queue-partial-acceptance-korean-first-ui-copy-rework-1.cycle.md
.aiassistant/tasks/active/20260903_1329_aiscc-p2-1b-korean-first-visible-copy-and-document-language-rework-1.md

src/aiscc/command_center/web.py
tests/unit/command_center/test_web_shell.py
tests/integration/command_center/test_web_ui.py
```

Do not reopen unrelated P2-1A source unless a regression test fails.

## 6. allowed product/test mutation

Preferred actual changes:

```text
src/aiscc/command_center/web.py
tests/unit/command_center/test_web_shell.py
tests/integration/command_center/test_web_ui.py
```

The following MUST remain byte-identical:

```text
src/aiscc/api/app.py
SHA-256:
34b9216342dc256fd319ab5c594799b9aa6784c35bc13a8b01595d4204d572f0

src/aiscc/api/routes/command_center_ui.py
SHA-256:
05ac1ba9ce029d9b45b8aa93ee805976b97cc8b4e338af3747c14577e08122e2
```

No new product/test path is authorized.

## 7. Korean-first document contract

Both rendered HTML documents MUST use:

```html
<html lang="ko">
```

Product name may remain:

```text
AI Software Command Center
```

Human-facing title/body/help/action/accessibility text must be Korean-first.

Examples of acceptable direction:

```text
Operator workspace
→ 운영자 작업공간

Project queue access
→ 프로젝트 큐 조회

Open a known Project ID
→ 알고 있는 Project ID 열기

Known Project ID
→ 알고 있는 Project ID

Open project queue
→ 프로젝트 큐 열기

Change project
→ Project 변경

Queue filters
→ 큐 필터

Refresh queue
→ 큐 새로고침

Project queue
→ 프로젝트 큐

Previous / Next
→ 이전 / 다음
```

Do not mechanically translate technical identifiers that are canonical terms.

## 8. authority/status labels

Use Korean-first labels while preserving exact semantic owner names.

Recommended:

```text
Task / WorkRun
→ Task / WorkRun

Workflow
→ 워크플로 (WorkflowState)

Execution
→ 실행 상태 (ExecutionStatus)

Human Gate
→ Human Gate

Human Result
→ Human Result

Judgment
→ 판정 (Judgment)

Latest Transition Decision
→ 최신 전이 결정 (TransitionDecision)

Next Action
→ 다음 작업 (Next Action)

Runtime Mode
→ 런타임 모드 (RuntimeMode)
```

Exact source enum values remain untranslated:

```text
RUNNING
EXECUTOR_COMPLETED
PENDING
APPROVE
ACCEPTED
ADMITTED
OWNER_SELF_DOGFOOD
```

Do not collapse them into Korean-only invented enum values.

## 9. Task metadata fallback

Current accepted authority behavior remains unchanged.

Visible Korean-first fallback:

```text
REFERENCE_ONLY:
참조만 가능 (REFERENCE_ONLY)

metadata unavailable:
Task metadata를 사용할 수 없음
```

Stable TaskContract ID/version and WorkRun ID remain visible with original identifiers.

## 10. presentation-state / error copy

Internal JavaScript state keys remain exact:

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

But visible screen label/message must be Korean-first.

Recommended visible labels:

```text
LOADING:
불러오는 중

EMPTY:
결과 없음

READY:
최신 상태

INVALID_QUERY:
조회 조건 오류

NOT_FOUND:
프로젝트 큐 없음

AUTHORITY_CONFLICT:
권위 상태 충돌

PROJECTION_UNAVAILABLE:
조회 projection 사용 불가

UNEXPECTED_ERROR:
조회 오류
```

Do not expose raw backend stack/SQL/private error payload.

`data-state` or internal state names may remain exact for deterministic styling/testing.

## 11. accessibility copy

Korean-first applies to:

```text
aria-label
field help
button accessible names
pagination labels
scroll-region labels
state aria-live messages
```

Technical identifiers inside accessibility text may remain original.

## 12. behavior that must remain unchanged

Do not change:

```text
exact four UI/assets route set
P2-1A queue endpoint authority
filter query parameter names
limit range 1..100
opaque cursor behavior
safe DOM APIs
CSP/security headers
ETag query-shape behavior
304 keeps rows
manual refresh availability
10000 ms polling
visible-only polling
nonterminal-only polling
terminal set ACCEPTED/REJECTED/FAILED
P2-1C route exclusion
no mutation controls
no Project catalog
```

No API or database behavior change is authorized.

## 13. focused tests

Update/add assertions proving:

1. landing and project HTML use `lang="ko"`;
2. primary human-facing page headings/help/buttons are Korean-first;
3. nine authority/status columns use accepted Korean-first labels without collapsing semantics;
4. exact enum values remain untranslated in runtime rendering;
5. Task metadata fallback is Korean-first;
6. visible presentation/error messages are Korean-first while internal state keys remain exact;
7. accessibility labels/help are Korean-first;
8. original source behavior tests for safe DOM/ETag/polling/security/no mutation continue to pass;
9. app.py and command_center_ui.py SHA-256 remain exact pre-rework identities.

Do not use brittle full HTML snapshot tests.

## 14. runtime / regression proof

Required:

```text
repository-local syntax/compile
Ruff changed Python
mypy changed Python
git diff --check
targeted P2-1B unit/integration
applicable full unit+integration regression
```

Normal default-entrypoint HTTP proof may be narrowly rerun to verify:

```text
GET /command-center → 200 / lang=ko
GET /command-center/projects/<known-project> → 200 / lang=ko
assets → unchanged operational
queue API → unchanged operational
event-count no-mutation → unchanged
```

Use existing local PostgreSQL harness only.

No package install/network/browser automation.

## 15. Human QA boundary

Executor MUST keep:

```text
Human Browser/Visual QA:
HUMAN_PENDING
```

Do not claim that Korean-first source/runtime checks are visual/usability acceptance.

After Command Center accepts this rework candidate, Browser Command Center will issue a separate Human QA Task.

## 16. mandatory stop

STOP if rework requires:

```text
API semantic change
new product path
new dependency
new Project index
P1 authority change
authentication/external exposure decision
migration/table
unrelated dirty source cleanup
```

Do not broaden the task.

## 17. Task lifecycle

After rework/evidence/report/export:

```text
.aiassistant/tasks/active/20260903_1329_aiscc-p2-1b-korean-first-visible-copy-and-document-language-rework-1.md
→
.aiassistant/tasks/done/20260903_1329_aiscc-p2-1b-korean-first-visible-copy-and-document-language-rework-1.md
```

Move, not Copy.

Do not stage or commit.

## 18. export

Target:

```text
.aiassistant/reports/target/20260903_1329_aiscc-p2-1b-korean-first-visible-copy-and-document-language-rework-1/
```

Required root:

```text
TASK.md
EXECUTOR_REPORT.md
KOREAN_FIRST_UI_EVIDENCE.md
HTTP_RUNTIME_EVIDENCE.md
EXPORT_MANIFEST.md
```

Export all five current product/test candidate files, not only the files whose bytes changed during rework, so the
Command Center can rebind the full candidate identity.

Manifest binds every payload except itself.

## 19. success

Successful result:

```text
P2_1B_REWORK_CANDIDATE
/ KOREAN_FIRST_UI_POLICY_ALIGNED
/ COMMAND_CENTER_REVIEW_AND_HUMAN_BROWSER_QA_REQUIRED
```

Do not declare:

```text
P2-1B ACCEPTED
Human QA PASS
P2-1C STARTED
P2-1 ACCEPTED
P2-2 STARTED
```

## 20. preserved artifacts

Preserve:

- accepted P2-1A commit `4ea1fe6f7cb8e11ff5ccfde70462eba931c4071e`
- `.aiassistant/tasks/done/20260903_1325_aiscc-p2-1b-command-center-shell-and-project-task-queue-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260903_1327_aiscc-p2-1b-shell-queue-partial-acceptance-korean-first-ui-copy-rework-1.cycle.md`
- `.aiassistant/tasks/done/20260903_1329_aiscc-p2-1b-korean-first-visible-copy-and-document-language-rework-1.md` after lifecycle
- current P2-1B five-file rework candidate dirt.

Target bundle remains temporary through Browser review.
