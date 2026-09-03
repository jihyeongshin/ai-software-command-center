# AISCC Cycle Record

## meta

- cycle_id: `20260903_1431_aiscc-p2-1b-shell-queue-rework-acceptance-pending-human-browser-qa-1`
- date: `2026-09-03T14:31:00+09:00`
- project: `AI Software Command Center (AISCC)`
- primary_semantic_owner: `Browser Command Center P2-1B rework review`
- affected_areas: `P2-1B shell/queue source/runtime candidate and Human Browser QA gate`
- work_type: `COMMAND_CENTER_JUDGMENT / HUMAN_QA_GATE`
- predecessor_head: `4ea1fe6f7cb8e11ff5ccfde70462eba931c4071e`
- predecessor_task: `.aiassistant/tasks/done/20260903_1329_aiscc-p2-1b-korean-first-visible-copy-and-document-language-rework-1.md`
- submitted_bundle: `20260903_1329_aiscc-p2-1b-korean-first-visible-copy-and-document-language-rework-1.zip`
- submitted_bundle_sha256: `99975056e1e25a8f021a921c05d213fab3384f1b2f0482c093566d9471fc901d`
- result_status: `ACCEPTED_PENDING_HUMAN_BROWSER_QA / P2_1B_SOURCE_RUNTIME_ACCEPTED`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260903_1431_aiscc-p2-1b-shell-queue-rework-acceptance-pending-human-browser-qa-1.cycle.md`
- P2_status: `STARTED / P2-1 ACTIVE`
- P2_1B_status: `SOURCE_RUNTIME_ACCEPTED / HUMAN_QA_PENDING`
- P2_1C_status: `NOT_STARTED`

## package verification

Browser-side independent verification:

```text
archive SHA-256:
99975056e1e25a8f021a921c05d213fab3384f1b2f0482c093566d9471fc901d

manifest-declared payloads:
10

manifest missing:
0

manifest extra:
0

manifest byte/hash mismatches:
0

UTF-8/BOM/trailing-whitespace issues:
0
```

## exact accepted P2-1B candidate identity

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

Aggregate serialization:

```text
<case-sensitive repository-relative path>\t<lowercase_sha256>\n
```

Aggregate SHA-256:

```text
37e1d613f457d4fda84d58b8b2b690981786e088ad03025e1dfd7a276e3bed7e
```

## rework judgment

The prior blocker:

```text
KOREAN_FIRST_UI_COPY_POLICY
```

is resolved.

Independent comparison of the old 1325 candidate and current 1329 `web.py` confirms the rework is confined to:

- `<html lang="en">` → `<html lang="ko">`;
- Korean-first visible headings/body/help/buttons/filter/pagination/accessibility copy;
- Korean-first visible read/error state labels/messages;
- initial `data-state="LOADING"` presentation marker;
- exact technical identifiers and enum/state values remain untranslated.

Protected source remained byte-identical:

```text
src/aiscc/api/app.py
34b9216342dc256fd319ab5c594799b9aa6784c35bc13a8b01595d4204d572f0

src/aiscc/api/routes/command_center_ui.py
05ac1ba9ce029d9b45b8aa93ee805976b97cc8b4e338af3747c14577e08122e2
```

No API authority, data-query, CSP, ETag, polling, routing, or mutation semantics were broadened.

## admitted evidence

```text
same P2-1B implementation chat lineage:
PASS

pre-rework five-file identity:
PASS

canonical language policy direct read:
PASS

Korean-first source/static contract:
PASS

focused UI:
11 passed / 1 expected PostgreSQL skip

full applicable unit + integration:
241 passed

normal default-entrypoint:
PASS

landing/project lang=ko:
PASS

queue/filter/ETag/304:
PASS

authoritative event-count no-mutation:
PASS

Ruff:
PASS

mypy:
PASS

git diff --check:
PASS

Human Browser/Visual QA:
HUMAN_PENDING
```

## accepted source/runtime scope

The candidate may proceed to Human Browser QA with these accepted implementation facts:

```text
HTML-first same-process FastAPI
exact four /command-center UI/assets GET routes
P2-1A queue API as sole runtime data authority
no Project catalog/index authority
separate status/authority dimensions
plain CSS / plain JavaScript
safe DOM APIs
no Node/npm/SPA/CDN
LOCAL_PRIVATE_ONLY
CSP / security headers
ETag / If-None-Match / 304
manual refresh
visible + nonterminal 10-second polling
read-only / no mutation controls
P2-1C detail absent
Korean-first human-facing copy
technical identifiers/enums preserved
```

## proof boundary

```text
source/runtime PASS
!=
Human Browser visual/usability PASS
```

No P2-1B terminal acceptance is admitted until Human Browser QA is provided.

## Human QA prerequisite

Human QA requires:

```text
normal AISCC local loopback server
+
a known Project ID
```

For complete data-driven checks, the known Project ID should resolve to a queue containing at least one
nonterminal WorkRun; an additional all-terminal query/project is useful for polling-stop verification.

If such a local QA fixture is not available, Human must stop and return:

```text
QA_FIXTURE_REQUIRED
```

Do not invent a Project ID or treat `503 PROJECTION_UNAVAILABLE` as queue QA success.

## state

```text
P2:
STARTED / P2-1 ACTIVE

P2-1A:
ACCEPTED / PERSISTED

P2-1B:
ACCEPTED_PENDING_HUMAN_BROWSER_QA

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
- current exact five-file P2-1B candidate dirt.

## next action

next_action:
- owner: `Human`
- work_type: `HUMAN_BROWSER_VISUAL_QA`
- title: `P2-1B Command Center shell + Project/task queue Human QA`
- blocker: `none if local seeded/known Project ID fixture exists`
- fallback_blocker: `QA_FIXTURE_REQUIRED`
- IDE_Task_required_now: `No`
- P2_1C_execution: `forbidden until Human QA and persistence`
