# AISCC Cycle Record

## meta

- cycle_id: `20260903_1327_aiscc-p2-1b-shell-queue-partial-acceptance-korean-first-ui-copy-rework-1`
- date: `2026-09-03T13:27:00+09:00`
- project: `AI Software Command Center (AISCC)`
- primary_semantic_owner: `Browser Command Center P2-1B implementation review`
- affected_areas: `P2-1B shell/queue UI visible copy and document language`
- work_type: `COMMAND_CENTER_JUDGMENT / REWORK`
- predecessor_head: `4ea1fe6f7cb8e11ff5ccfde70462eba931c4071e`
- predecessor_task: `.aiassistant/tasks/done/20260903_1325_aiscc-p2-1b-command-center-shell-and-project-task-queue-implementation-1.md`
- submitted_bundle: `20260903_1325_aiscc-p2-1b-command-center-shell-and-project-task-queue-implementation-1.zip`
- submitted_bundle_sha256: `06c50c52a187371e7f018600554b870d159b4f903a1ae165beabccc081ded881`
- result_status: `PARTIAL_ACCEPTED / HOLD_REWORK_REQUIRED / KOREAN_FIRST_UI_COPY_POLICY`
- reject_cause: `POLICY_BASELINE_CONFLICT / USER_SCREEN_COPY_NOT_KOREAN_FIRST`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260903_1327_aiscc-p2-1b-shell-queue-partial-acceptance-korean-first-ui-copy-rework-1.cycle.md`
- P2_status: `STARTED / P2-1 ACTIVE`
- P2_1B_status: `REWORK_REQUIRED`
- Human_Browser_QA: `NOT_STARTED / BLOCKED_BY_COPY_REWORK`

## submitted-package verification

Browser-side independent verification:

```text
archive SHA-256:
06c50c52a187371e7f018600554b870d159b4f903a1ae165beabccc081ded881

manifest-declared payloads:
11

manifest missing:
0

manifest extra:
0

manifest byte/hash mismatches:
0

UTF-8/BOM/trailing-whitespace issues:
0
```

## admitted implementation scope

The following P2-1B implementation directions are accepted as candidate scope and should not be redesigned by this
rework:

```text
same-process HTML-first FastAPI shell
exact four /command-center UI/assets GET routes
P2-1A queue API as sole runtime data authority
no Project catalog/index authority
separate authority/status dimensions
plain CSS + plain JavaScript
no Node/npm/SPA/CDN
safe DOM APIs
LOCAL_PRIVATE_ONLY response boundary
CSP / nosniff / no-referrer / no-store
accepted queue filters only
ETag / If-None-Match / 304
manual refresh
visible + nonterminal 10-second polling
P2-1C detail exclusion
read-only / no mutation controls
```

Admitted executor evidence:

```text
SESSION_AUTHORITY:
NEW_P2_1B_IMPLEMENTATION_CHAT / PASS

focused non-DB:
9 passed / 1 expected PostgreSQL skip

focused PostgreSQL + UI:
3 passed

full applicable unit + integration:
239 passed

normal default-entrypoint HTTP:
PASS

UI/assets:
200

queue over seeded PostgreSQL:
200

ETag/304:
PASS

event-count no-mutation:
PASS

POST/PUT/PATCH/DELETE:
405 / no mutation

Ruff:
PASS

mypy:
PASS

git diff --check:
PASS
```

Human Browser/Visual QA remains correctly `HUMAN_PENDING`.

## exact current candidate identity

Current P2-1B product/test candidate is exactly five paths:

```text
src/aiscc/api/app.py
SHA-256 34b9216342dc256fd319ab5c594799b9aa6784c35bc13a8b01595d4204d572f0

src/aiscc/api/routes/command_center_ui.py
SHA-256 05ac1ba9ce029d9b45b8aa93ee805976b97cc8b4e338af3747c14577e08122e2

src/aiscc/command_center/web.py
SHA-256 f3a8230ac3d58586fdaf08f1880a6839b8fa2786e0868573b3c171c76e89d5c7

tests/integration/command_center/test_web_ui.py
SHA-256 92d687a0d54ecac12a94c3e4c934b2f1d16f47a7e518e28fbd88fe76199ab8cf

tests/unit/command_center/test_web_shell.py
SHA-256 b4fa4afdf333607161c0bf8d77334e1b1fbdd8e55b678c10f8f1b12c62da4d49
```

Aggregate serialization:

```text
<case-sensitive repository-relative path>\t<lowercase_sha256>\n
```

Aggregate SHA-256:

```text
a8157f255ff6ec2bf87a3a47a2f51b520f0322bb17fe320d591b3859cbc6333c
```

## substantive policy conflict

Canonical owner:

```text
.aiassistant/rules/AISCC_DOCUMENT_LANGUAGE_POLICY.md
```

Current accepted policy includes:

```text
사용자 화면 copy는 Korean-first를 기본으로 한다.
내부 state/error identifier를 그대로 노출하지 않고 사람용 설명과 연결한다.
Code/path/state identifier는 원문을 유지한다.
```

Current P2-1B exported UI instead contains:

```text
<html lang="en">

Operator workspace
Project queue access
Open a known Project ID
Queue filters
Project queue
Loading the queue projection.
Task metadata unavailable
Reference only
Previous / Next
and other primarily English human-facing copy
```

This is not merely Human visual preference. It conflicts with an already-accepted canonical UI-language policy.

The P2-1B Task did not supersede that rule and Human P2-1 design acceptance did not authorize an English-first UI.

Therefore Human Browser QA must not be used as a substitute for correcting the canonical policy conflict.

## required correction

Rework only visible human-facing copy/document language.

Required:

```text
<html lang="ko">
human-facing headings/body/help/button/filter/state/error/accessibility copy:
Korean-first
```

Product name and exact technical identifiers may remain original:

```text
AI Software Command Center
Project ID
TaskContract
WorkRun
WorkflowState
ExecutionStatus
HumanGateStatus
JudgmentKind
RuntimeMode
REFERENCE_ONLY
ACCEPTED
REJECTED
FAILED
```

Recommended rendering style:

```text
워크플로 (WorkflowState)
실행 상태 (ExecutionStatus)
Human Gate
Human Result
판정 (Judgment)
최신 전이 결정 (TransitionDecision)
다음 작업 (Next Action)
런타임 모드 (RuntimeMode)
```

Exact enum/code values remain unchanged.

Internal presentation/error states should remain internal data-state identifiers, while visible copy becomes
human-readable Korean-first.

Examples:

```text
LOADING → 불러오는 중
EMPTY → 결과 없음
READY → 최신 상태
INVALID_QUERY → 조회 조건 오류
NOT_FOUND → 프로젝트 큐 없음
AUTHORITY_CONFLICT → 권위 상태 충돌
PROJECTION_UNAVAILABLE → 조회 projection 사용 불가
UNEXPECTED_ERROR → 조회 오류
```

The exact internal identifiers may remain in JavaScript/state data for deterministic behavior.

## accepted paths that must remain byte-identical

The rework must not alter:

```text
src/aiscc/api/app.py
SHA-256:
34b9216342dc256fd319ab5c594799b9aa6784c35bc13a8b01595d4204d572f0

src/aiscc/api/routes/command_center_ui.py
SHA-256:
05ac1ba9ce029d9b45b8aa93ee805976b97cc8b4e338af3747c14577e08122e2
```

No API/P2-1A semantic change is authorized.

## state

```text
P2:
STARTED / P2-1 ACTIVE

P2-1A:
ACCEPTED / PERSISTED

P2-1B:
PARTIAL_ACCEPTED / REWORK_REQUIRED

Human Browser QA:
BLOCKED until copy rework is Command Center accepted

P2-1C:
NOT_STARTED
```

## preserved artifacts

Preserve:

- accepted P2-1A commit `4ea1fe6f7cb8e11ff5ccfde70462eba931c4071e`
- `.aiassistant/records/aiscc/cycles/20260903_1323_aiscc-p2-1a-read-api-foundation-persistence-final-acceptance-1.cycle.md`
- `.aiassistant/tasks/done/20260903_1325_aiscc-p2-1b-command-center-shell-and-project-task-queue-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260903_1327_aiscc-p2-1b-shell-queue-partial-acceptance-korean-first-ui-copy-rework-1.cycle.md`
- current P2-1B five-file candidate dirt.

## next action

next_action:
- work_type: `REWORK / FRONTEND_IMPLEMENTATION`
- title: `P2-1B Korean-first visible copy and document-language rework`
- blocker: `canonical AISCC_DOCUMENT_LANGUAGE_POLICY conflict`
- same_IDE_chat: `allowed`
- Human_QA_after_rework_acceptance: `required`
- P2_1C_execution: `forbidden`
