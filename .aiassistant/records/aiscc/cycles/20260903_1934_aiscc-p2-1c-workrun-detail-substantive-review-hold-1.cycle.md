# AISCC Cycle Record

## meta

- cycle_id: `20260903_1934_aiscc-p2-1c-workrun-detail-substantive-review-hold-1`
- date: `2026-09-03T19:34:00+09:00`
- project: `AI Software Command Center (AISCC)`
- primary_semantic_owner: `Browser Command Center P2-1C substantive source/runtime review`
- affected_areas: `P2-1C WorkRun transition/execution detail candidate`
- work_type: `COMMAND_CENTER_JUDGMENT`
- execution_mode: `MANUAL_COMMAND_CENTER`
- task_file: `.aiassistant/tasks/done/20260903_1759_aiscc-p2-1c-workrun-transition-execution-detail-implementation-1.md`
- temporary_target_bundle: `.aiassistant/reports/target/20260903_1759_aiscc-p2-1c-workrun-transition-execution-detail-implementation-1/`
- submitted_bundle: `20260903_1759_aiscc-p2-1c-workrun-transition-execution-detail-implementation-1.zip`
- submitted_bundle_sha256: `7371d8d904d1bc4b052377fa0a29ed056661c691ea30994a3253b1d1c156bdc9`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause: `EXECUTOR_MISREAD_BASELINE`
- cycle_record_action: `create`
- source_mirror_sync: `not-required`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260903_1934_aiscc-p2-1c-workrun-detail-substantive-review-hold-1.cycle.md`

## product/repository snapshot

- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- accepted_base_commit: `62a3c5135a12afc38ba32e4c5f651c1f1b007549`
- candidate_commit: `none`
- accepted P2-1A commit: `4ea1fe6f7cb8e11ff5ccfde70462eba931c4071e`
- accepted P2-1B commit: `62a3c5135a12afc38ba32e4c5f651c1f1b007549`
- P2-1C candidate product/test aggregate: `13f07b59fdaedb706437967e6e2e1bb5253a555f4a385df0b39e6d15c58889eb`
- P2-1C Human Browser/Visual: `HUMAN_PENDING / QA_GATE_NOT_OPENED`

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
HOLD_REWORK_REQUIRED
SOURCE_RUNTIME_CANDIDATE_NOT_ACCEPTED
HUMAN_QA_NOT_OPENED

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
7371d8d904d1bc4b052377fa0a29ed056661c691ea30994a3253b1d1c156bdc9

archive entries:
18

payload files excluding manifest:
6

TASK.md:
byte-identical to Browser-issued Task

TASK SHA-256:
58dcbc5ff8e89ba849ebe5e4e3cfe914fff6d1b3c4e73909fd81567f95d828d4

manifest payload hash mismatches:
0
```

Submitted changed product/test identity:

```text
src/aiscc/api/routes/command_center_ui.py
82d73e29ed5c185948ba82a5fc79083cafdb77b36b3f30760f570c295af01fd2

src/aiscc/command_center/web.py
ec19e71480e49db08e2ff2cdfd88f508e2842c9b653286a7f2e630e61a8f2f37

tests/integration/command_center/test_web_ui.py
1eb8d100be9b64c8c2ecd1779f5b67b90862ed96c23be2861b3f809e28a2f4d4

tests/unit/command_center/test_web_shell.py
72f8dcb7fcdd723523885b391bf2322a6d937a1c8601105d0139d07765eace4b
```

Aggregate serialization:

```text
<case-sensitive repository-relative path>\t<lowercase_sha256>\n
```

Browser Command Center independently recomputed:

```text
13f07b59fdaedb706437967e6e2e1bb5253a555f4a385df0b39e6d15c58889eb
```

and it exactly matches the submitted manifest/report.

Previous accepted transport artifacts were also independently checked against the current Browser-mounted originals:

```text
20260903_1718_aiscc-p2-1b-shell-queue-persistence-final-acceptance-1.cycle.md
f479952b982af8d7444494d4021db443b84135324a4e4a68f09f0b30355f2488

20260903_1720_aiscc-browser-command-center-p2-1b-completion-p2-1c-entry-handoff-1.md
ca813f7cd5775d0a2d649bddae6800b4cc8ad114b7ac7110aed4e1d52f7c276d
```

These match the Executor report.

## executor candidate summary

The candidate correctly introduces:

```text
GET /command-center/work-runs/{work_run_id}
```

and retains the existing UI routes/assets.

The WorkRun detail browser code is limited to the accepted P2-1A read authority:

```text
GET /v1/command-center/work-runs/{work_run_id}
GET /v1/command-center/work-runs/{work_run_id}/transitions
GET /v1/command-center/work-runs/{work_run_id}/execution
```

The submitted source also visibly preserves the intended domain separations:

```text
WorkflowState
ExecutionStatus
TransitionDecision
ADMITTED
DENIED
EXECUTOR_COMPLETED
```

and includes explicit copy that:

```text
DENIED != successful state transition

EXECUTOR_COMPLETED != WorkRun ACCEPTED
```

The implementation uses safe DOM construction rather than API-derived `innerHTML`/`eval` execution paths in the reviewed P2-1C detail block.

Executor reports:

```text
focused P2-1C:
21 passed

full unit + integration:
250 passed

Ruff:
PASS

mypy:
PASS

py_compile:
PASS

git diff --check:
PASS

normal local HTTP runtime:
PASS

authoritative event count before/after:
unchanged
```

These execution claims are not the reason for the HOLD. The blocker is visible directly in the submitted source.

## blocking source-contract defect

### accepted Task requirement

The P2-1C Task explicitly requires:

```text
If WorkRun summary itself cannot be established as current/authoritative,
do not continue presenting stale transitions or execution as if the page is
a trustworthy current snapshot.

Preserve the last successful DOM only if the visual copy clearly indicates
refresh failure and does not relabel it as newly current.
```

### submitted behavior

After a prior successful detail read:

1. transition section becomes:
   `최신 전이 기록`
2. execution section becomes:
   `최신 실행 기록`
3. a later refresh starts all three endpoint requests concurrently.
4. if WorkRun summary then fails or cannot establish current authority,
   `loadDetail()` sets the overall read state to the summary failure and returns before
   `applyTransitions()` / `applyExecution()`.
5. the previous transition/execution DOM is retained.
6. critically, the previous section read labels are also retained unchanged.

Therefore stale sections remain visibly labeled:

```text
최신 전이 기록
최신 실행 기록
```

even while the page-level copy says the new current WorkRun snapshot could not be established.

Relevant submitted source behavior:

```text
applyTransitions success
→ transitionsState.textContent = "최신 전이 기록"

applyExecution success
→ executionState.textContent = "최신 실행 기록"

later summary failure
→ setDetailState(<failure>, "...마지막으로 성공한 snapshot을 유지...")
→ return
```

No source path in that failure branch downgrades the retained section labels.

### judgment

This is not merely a visual preference.

It violates the Task's explicit authority-presentation contract:

```text
stale retained section
!= newly current section
```

and can make stale transition/execution projections look current at exactly the moment when the summary authority check has failed.

The current unit tests do not catch the behavior because they assert string/polling/ETag structure but do not exercise this state sequence:

```text
successful detail refresh
→ later summary authority failure
→ retained transition/execution DOM
→ section read labels must become stale/refresh-failed, not "최신"
```

## required rework boundary

The next P2-1C rework must remain narrow.

Required behavior:

1. preserve the last successful transition/execution DOM when that is the chosen failure behavior;
2. when summary current authority cannot be established, immediately downgrade any retained transition/execution section state copy so it cannot still say `최신`;
3. the section copy must explicitly indicate retained/last-successful/stale-due-to-refresh-failure semantics;
4. do not apply freshly returned transition/execution payloads when summary authority cannot be established;
5. do not discard endpoint-scoped ETag/data state merely to hide the problem;
6. add a deterministic unit/DOM-state test for:
   `success → summary failure with previous data → stale section labels`;
7. preserve all previously accepted P2-1C boundaries:
   - exact three read endpoints only;
   - no P2-1D/P2-1E fetch;
   - no mutation;
   - safe DOM;
   - Korean-first;
   - `DENIED != transition`;
   - `EXECUTOR_COMPLETED != ACCEPTED`;
   - 10-second visible/nonterminal polling;
   - independent ETag/304;
   - P2-1B responsive queue behavior.

The defect does not require a P2-1A API contract change.

## transport chronology note

The Executor report states that the Cycle/Handoff expected SHA values were first read from the moved Task and compared after the Move.

The issued transport contract requested pre-Move hash confirmation, while the short transport prompt did not reproduce the two expected hash values and simultaneously instructed the Executor to perform transport before reading the Task.

That sequencing was not operationally self-contained.

Browser Command Center independently verified that the final source artifact identities are exact, so this is not an artifact-integrity blocker for the current judgment.

For the next Task transport, the Command Center must avoid the circular sequence by doing one of:

```text
A.
allow read-only opening of the Downloads Task before Move

or

B.
repeat all required expected transport hashes in the short prompt
```

Do not attribute this transport ambiguity to the product-source rework blocker.

## evidence admission

### independently verified

- submitted ZIP exists and is readable
- ZIP SHA-256
- archive inventory
- `TASK.md` exact byte identity
- manifest payload hash identity
- exact changed-file SHA-256 values
- exact changed-file aggregate
- submitted source behavior causing the HOLD
- previous Cycle/Handoff original SHA-256 identity

### Executor-reported and not contradicted

- new IDE Executor chat
- repository/branch/base HEAD/index preflight
- exact dirty workspace inventory
- P2-1A protected path identities
- 21 focused tests PASS
- 250 full unit/integration PASS
- Ruff/mypy/py_compile/diff-check PASS
- normal local HTTP runtime PASS
- no-mutation event count PASS
- Task-created runtime bytecode residue count

### human-owned

```text
HUMAN_VERIFICATION:
HUMAN_PENDING
QA_GATE_NOT_OPENED
```

Human browser/visual/usability proof is not substituted by source, unit, integration, or HTTP proof.

## proof admission

Agent claim rejected:

```text
"summary current authority failure retains previous successful DOM with sufficiently explicit refresh-failure semantics"
```

Reason:

```text
retained transition/execution section labels remain "최신 ..."
```

No proof-type substitution by the Executor was used to claim Human QA.

## runtime residue disposition

Executor reports:

```text
133 untracked bytecode files
under task-created __pycache__ paths
```

The current Task explicitly prohibited cleanup merely to normalize Git status.

Therefore:

```text
do not treat these residues as accepted source
do not include them in product/test candidate identity
do not silently clean/reset them
```

The next rework Task must treat them as known reported runtime residue and must not classify them as unrelated product source.

Terminal persistence, if later reached, must resolve runtime residue under an explicit narrow rule rather than broad Git cleanup.

## command-center judgment

```text
result_status:
HOLD_REWORK_REQUIRED

reject_cause:
EXECUTOR_MISREAD_BASELINE

accepted candidate portions:
bundle integrity
Task identity
narrow changed-path shape
route/read-authority direction
domain semantic separation direction
safe-DOM direction
Executor evidence collection direction

not accepted:
P2-1C source/runtime candidate as a whole

Human QA:
NOT OPENED
```

No commit is authorized.

P2-1C does not advance to Human QA until the source-level stale-current labeling defect is corrected and substantively re-reviewed.

## session transition

Current AISCC Browser operating rule:

```text
after bundle judgment:
do not issue the next Executor Task in the same Browser session

publish Cycle
+
publish Handoff
+
continue in a new Browser Command Center chat
```

Therefore no P2-1C rework Task is issued from this session.

## preserved artifacts

Must survive cleanup:

- P2-1A commit `4ea1fe6f7cb8e11ff5ccfde70462eba931c4071e`
- P2-1B commit `62a3c5135a12afc38ba32e4c5f651c1f1b007549`
- `.aiassistant/tasks/done/20260903_1759_aiscc-p2-1c-workrun-transition-execution-detail-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260903_1718_aiscc-p2-1b-shell-queue-persistence-final-acceptance-1.cycle.md`
- `.aiassistant/reports/aiscc/20260903_1720_aiscc-browser-command-center-p2-1b-completion-p2-1c-entry-handoff-1.md`
- `.aiassistant/records/aiscc/cycles/20260903_1934_aiscc-p2-1c-workrun-detail-substantive-review-hold-1.cycle.md`
- Browser Handoff `20260903_1936_aiscc-browser-command-center-p2-1c-hold-rework-entry-handoff-1.md`

The submitted target ZIP remains review-temporary and is not canonical product provenance.

## next action

next_action:
- Browser session: `NEW_CHAT_REQUIRED`
- phase: `P2-1C`
- work_type: `REWORK`
- title: `P2-1C retained-detail stale/current authority labeling rework`
- reason: `summary authority failure leaves retained transition/execution sections labeled as latest`
- blocker: `SOURCE_CONTRACT_GAP`
- Human QA: `not yet; re-open only after source/runtime rework acceptance`
- P2-1D: `DO_NOT_START`
