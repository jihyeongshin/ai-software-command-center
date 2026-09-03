# AISCC Cycle Record

## meta

- cycle_id: `20260903_2029_aiscc-p2-1c-stale-authority-rework-source-runtime-acceptance-human-qa-entry-1`
- date: `2026-09-03T20:29:00+09:00`
- project: `AI Software Command Center (AISCC)`
- primary_semantic_owner: `Browser Command Center P2-1C rework substantive source/runtime review`
- affected_areas: `P2-1C WorkRun detail stale/current authority presentation`
- work_type: `COMMAND_CENTER_JUDGMENT`
- execution_mode: `MANUAL_COMMAND_CENTER`
- task_file: `.aiassistant/tasks/done/20260903_1949_aiscc-p2-1c-retained-detail-stale-current-authority-labeling-rework-1.md`
- temporary_target_bundle: `.aiassistant/reports/target/20260903_1949_aiscc-p2-1c-retained-detail-stale-current-authority-labeling-rework-1/`
- submitted_bundle: `20260903_1949_aiscc-p2-1c-retained-detail-stale-current-authority-labeling-rework-1.zip`
- submitted_bundle_sha256: `48d4620b3becb9a28f57a6c5b879785f9d09177902c94a1fbd60446be400268b`
- result_status: `ACCEPTED_CANDIDATE`
- reject_cause: `none`
- cycle_record_action: `create`
- source_mirror_sync: `not-required`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260903_2029_aiscc-p2-1c-stale-authority-rework-source-runtime-acceptance-human-qa-entry-1.cycle.md`

## product/repository snapshot

- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- accepted_base_commit: `62a3c5135a12afc38ba32e4c5f651c1f1b007549`
- candidate_commit: `none`
- accepted P2-1A commit: `4ea1fe6f7cb8e11ff5ccfde70462eba931c4071e`
- accepted P2-1B commit: `62a3c5135a12afc38ba32e4c5f651c1f1b007549`
- predecessor rejected P2-1C aggregate: `13f07b59fdaedb706437967e6e2e1bb5253a555f4a385df0b39e6d15c58889eb`
- current P2-1C product/test aggregate: `2e4ca49afcd074aa2eac768b6f966d3d48044067917328a35c7839e078b35af3`
- Human Browser/Visual: `HUMAN_PENDING / QA_GATE_OPENED`

## phase state

```text
P0:
CLOSED

P1:
ACCEPTED / CLOSED

P2:
STARTED / P2-1 ACTIVE

P2-1A:
ACCEPTED / PERSISTED

P2-1B:
ACCEPTED / PERSISTED

P2-1C:
SOURCE_RUNTIME_ACCEPTED_CANDIDATE
HUMAN_QA_OPENED
OVERALL_NOT_ACCEPTED_OR_CLOSED

P2-1D:
NOT_STARTED

P2-1E:
NOT_STARTED

P2-2:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

P2-1 itself remains active and is not accepted/closed.

## submitted bundle verification

Browser Command Center independently verified the mounted ZIP.

```text
ZIP SHA-256:
48d4620b3becb9a28f57a6c5b879785f9d09177902c94a1fbd60446be400268b

archive entries:
29

payload files excluding manifest:
9

manifest payload hash mismatches:
0

TASK.md SHA-256:
0e2a7e169d7bf10e4bac299c8e40a6332ebe94c213eb4d3fe028a6f0d761bb9b

TASK.md:
byte-identical to Browser-issued Task

done Task SHA-256:
0e2a7e169d7bf10e4bac299c8e40a6332ebe94c213eb4d3fe028a6f0d761bb9b
```

Predecessor transport artifacts:

```text
HOLD Cycle:
dee7ffbb786e070ef2b8d531f9c04b5a02cace75fce253fbe81a6ea480ef7eea
exact expected match

Browser Handoff:
87e1b804ac31ac70b6c1fa70f135ef626222ef2033a951c00aa24009c2ee65d1
exact expected match
```

Current changed product/test identity:

```text
src/aiscc/api/routes/command_center_ui.py
82d73e29ed5c185948ba82a5fc79083cafdb77b36b3f30760f570c295af01fd2

src/aiscc/command_center/web.py
949f548548d2a92b260e2bb56fd99f4defa1188420263cc61ede49451c05a779

tests/integration/command_center/test_web_ui.py
1eb8d100be9b64c8c2ecd1779f5b67b90862ed96c23be2861b3f809e28a2f4d4

tests/unit/command_center/test_web_shell.py
7bef092098bbf9867378a18520d051fd1c1c6f9c91e050a5d53b481c449da382
```

Browser Command Center independently recomputed sorted aggregate serialization:

```text
<case-sensitive repository-relative path>\t<lowercase_sha256>\n
```

Result:

```text
2e4ca49afcd074aa2eac768b6f966d3d48044067917328a35c7839e078b35af3
```

This exactly matches the submitted manifest/report.

## predecessor blocker

Predecessor judgment:

```text
HOLD_REWORK_REQUIRED
reject_cause: EXECUTOR_MISREAD_BASELINE
```

Rejected behavior:

```text
successful detail refresh
→ transition/execution sections labeled "최신 ..."

later WorkRun summary current-authority failure
→ page-level failure copy
→ prior transition/execution DOM retained
→ section labels incorrectly remained "최신 ..."
```

This violated the explicit authority-presentation contract:

```text
retained stale data
!= newly current data
```

## substantive source review

Browser Command Center directly reviewed the submitted `web.py`.

The rework adds:

```text
markRetainedDetailStale()
```

and the failed-summary branch now behaves as follows:

```text
if (!summaryCurrent) {
    if (detailEndpoints.summary.hasData) {
        markRetainedDetailStale();
    } else {
        clearUnestablishedSnapshot();
    }
    return;
}
```

When prior transition/execution data exists, section copy becomes:

```text
마지막 성공 전이 기록 유지 · 새로고침 실패로 보존된 과거 snapshot입니다.
마지막 성공 실행 기록 유지 · 새로고침 실패로 보존된 과거 snapshot입니다.
```

Therefore retained sections no longer remain labeled:

```text
최신 전이 기록
최신 실행 기록
```

when WorkRun summary current authority cannot be established.

The failed-summary branch returns before:

```text
applyTransitions(transitionsResult)
applyExecution(executionResult)
```

and therefore fresh concurrent transition/execution payloads from that failed-summary refresh are not applied as current.

The stale-label helper does not:

```text
replaceChildren()
etag = null
hasData = false
```

so the accepted endpoint-scoped ETag/data state is not destructively reset merely to hide the defect.

A later successful summary refresh still reaches normal apply paths and restores:

```text
최신 전이 기록
최신 실행 기록
```

The Browser review found no new read endpoint, mutation control, P2-1D/P2-1E fetch, unsafe DOM path, polling change, or backend authority expansion in the reviewed rework path.

## deterministic test judgment

The new unit test covers the required A → B → C sequence:

```text
A:
successful refresh
→ current labels
→ A transition/execution data

B:
summary authority failure
→ retained A data
→ stale/last-successful labels
→ no "최신"
→ page state AUTHORITY_CONFLICT
→ no applyTransitions/applyExecution/commitSuccess in the failed-summary branch
→ no cache reset / DOM clear in stale helper

C:
subsequent successful refresh
→ C data
→ current labels restored
```

The test does not execute a real browser JavaScript DOM. It derives the actual source labels and failed-branch wiring from `APP_JS`, then executes the state sequence using the repository's existing Python test substrate.

This limitation is explicitly reported.

Judgment:

```text
not real browser DOM proof
BUT
more than source-string-presence-only proof
AND
acceptable for this Task's dependency-free deterministic source/runtime gate
```

Real browser DOM/visual/polling behavior remains Human-owned and is not substituted by this unit test.

## evidence admission

### independently verified by Browser Command Center

- mounted ZIP readability
- ZIP SHA-256
- archive inventory
- manifest payload hashes: exact
- Task root/done byte identity
- predecessor HOLD Cycle/Handoff transport identities
- exact current four-path SHA-256 identities
- exact product/test aggregate
- `web.py` failed-summary branch
- stale-label helper semantics
- no fresh detail application after summary failure in the reviewed source path
- no stale-helper cache reset/DOM clear
- later normal-success label restoration source path
- unit test A → B → C structure and assertions

### Executor-reported and not contradicted

```text
STATIC_SOURCE:
EXECUTED_PASS

focused UNIT_TEST:
17 passed

focused INTEGRATION_TEST:
4 passed, 1 skipped
skip reason: AISCC_TEST_DATABASE_URL absent

applicable non-PostgreSQL full regression:
190 passed, 61 deselected

unfiltered full regression:
190 passed, 38 skipped, 23 failed
all reported failures require absent AISCC_TEST_DATABASE_URL in unrelated PostgreSQL provider tests

Ruff:
PASS

mypy:
PASS

py_compile:
PASS

git diff --check:
PASS

runtime residue:
133 untracked __pycache__ / .pyc files retained, not cleaned
```

The absent PostgreSQL environment is not treated as a blocker for this rework because this Task explicitly classified `DATABASE_RUNTIME` as `NOT_REQUIRED`, and no database contract was changed.

### human-owned

```text
HUMAN_VERIFICATION:
HUMAN_PENDING
QA_GATE_OPENED
```

Human browser/visual/usability proof is still required before P2-1C overall acceptance.

## proof admission

Admitted:

```text
source/runtime blocker corrected:
YES

deterministic dependency-free state-sequence test:
YES

Human browser/visual proof:
NO / HUMAN_PENDING
```

No proof-type substitution is admitted.

```text
unit/source proof
!=
Human browser QA
```

## command-center judgment

```text
판정:
ACCEPTED_CANDIDATE

scope:
P2-1C source/runtime rework only

reject_cause:
none

P2-1C overall:
NOT_ACCEPTED_OR_CLOSED

Human QA:
REQUIRED / GATE_OPENED

P2-1D:
DO_NOT_START
```

The predecessor `EXECUTOR_MISREAD_BASELINE` blocker is resolved for source/runtime review.

This acceptance does not establish Human Browser/Visual quality and does not authorize Git persistence yet.

## human verification

Owner:

```text
human
```

Next exact artifact:

```text
.aiassistant/tasks/active/20260903_2029_aiscc-p2-1c-workrun-detail-human-browser-qa-1.md
```

Required Human QA includes:

- WorkRun detail hierarchy/readability;
- `ADMITTED` vs `DENIED` comprehensibility;
- execution readability and `EXECUTOR_COMPLETED != ACCEPTED`;
- queue → detail → project navigation;
- 1080 / 1280 / 1440 at Zoom 100%;
- visible/nonterminal polling;
- hidden-tab stop and visible-tab resume/focus behavior;
- terminal polling stop;
- retained stale/current refresh-failure presentation.

## source mirror sync

```text
required:
No

status:
not-required
```

No canonical baseline requiring Browser Project Source replacement changed in this source/runtime rework.

## preserved artifacts

Must preserve after cleanup:

- `.aiassistant/tasks/done/20260903_1759_aiscc-p2-1c-workrun-transition-execution-detail-implementation-1.md`
- `.aiassistant/tasks/done/20260903_1949_aiscc-p2-1c-retained-detail-stale-current-authority-labeling-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260903_1934_aiscc-p2-1c-workrun-detail-substantive-review-hold-1.cycle.md`
- `.aiassistant/reports/aiscc/20260903_1936_aiscc-browser-command-center-p2-1c-hold-rework-entry-handoff-1.md`
- `.aiassistant/records/aiscc/cycles/20260903_2029_aiscc-p2-1c-stale-authority-rework-source-runtime-acceptance-human-qa-entry-1.cycle.md`
- `.aiassistant/tasks/active/20260903_2029_aiscc-p2-1c-workrun-detail-human-browser-qa-1.md` until Human QA completes
- accepted P2-1A commit `4ea1fe6f7cb8e11ff5ccfde70462eba931c4071e`
- accepted P2-1B commit `62a3c5135a12afc38ba32e4c5f651c1f1b007549`

The submitted target bundle remains temporary review evidence and may be deleted after this judgment is durably persisted unless a later Task explicitly preserves it.

## public provenance mapping

- implementation Task:
  `.aiassistant/tasks/done/20260903_1949_aiscc-p2-1c-retained-detail-stale-current-authority-labeling-rework-1.md`
- predecessor HOLD Cycle:
  `.aiassistant/records/aiscc/cycles/20260903_1934_aiscc-p2-1c-workrun-detail-substantive-review-hold-1.cycle.md`
- current source/runtime judgment Cycle:
  `.aiassistant/records/aiscc/cycles/20260903_2029_aiscc-p2-1c-stale-authority-rework-source-runtime-acceptance-human-qa-entry-1.cycle.md`
- commits:
  - P2-1A accepted: `4ea1fe6f7cb8e11ff5ccfde70462eba931c4071e`
  - P2-1B accepted: `62a3c5135a12afc38ba32e4c5f651c1f1b007549`
  - P2-1C candidate: `none`
- sensitive data check:
  no secret/private material identified in Browser-reviewed bundle content

## reusable lesson

For UI projections that preserve prior successful data after an authority/read failure:

```text
retained bytes
must carry retained/stale semantics
```

A page-level authority failure message is insufficient if section-level state still represents the retained projection as current.

The correct invariant is:

```text
current-authority failure
→ retained DOM allowed
→ current/latest label forbidden
→ fresh dependent payload application forbidden
→ current label restoration only after authority succeeds again
```

## next action

```text
next_action:
- work_type: QA_ONLY / HUMAN_VERIFICATION
- title: P2-1C WorkRun Detail Human Browser QA
- reason: source/runtime blocker is substantively corrected; Human-owned browser/visual/polling proof remains
- blocker: HUMAN_VERIFICATION_PENDING
- required_baseline: current P2-1C accepted source/runtime candidate aggregate 2e4ca49afcd074aa2eac768b6f966d3d48044067917328a35c7839e078b35af3
- human_verification_needed: Yes
- P2-1D: NOT_STARTED
```
