# AI Software Command Center — Browser Command Center Handoff
## P2-1C substantive HOLD → rework entry

## 0. handoff identity

- handoff_id: `20260903_1936_aiscc-browser-command-center-p2-1c-hold-rework-entry-handoff-1`
- created_at: `2026-09-03T19:36:00+09:00`
- project: `AI Software Command Center (AISCC)`
- source_browser_session_end_state: `P2-1C HOLD_REWORK_REQUIRED`
- destination_browser_session_entry: `P2-1C REWORK_REQUIRED / TASK_NOT_YET_ISSUED`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- current accepted HEAD: `62a3c5135a12afc38ba32e4c5f651c1f1b007549`
- public bounded Live: `NOT_RELEASED`

This is a Browser Command Center continuation document, not an Executor Task.

The destination Browser Command Center must read this Handoff and the immediately preceding HOLD Cycle before issuing the next P2-1C rework Task.

---

# 1. canonical authority and operating doctrine

Authority precedence:

```text
local canonical repository
>
terminal-persisted accepted Cycle/rule/commit
>
latest terminal Browser judgment Cycle
>
current Handoff
>
Browser Project Source mirror
>
chat memory
```

Core non-substitution:

```text
AGENT_OUTPUT != SYSTEM_STATE
AGENT_CLAIM != ADMITTED_EVIDENCE
HUMAN_OWNED_EVIDENCE != EXECUTOR_COMPLETED
tasks/done != accepted
Executor PASS != Command Center acceptance
Commit created != accepted/closed
```

AISCC thesis:

```text
Software Engineering Governance Control Plane
not a Coding Agent
```

Orchestration:

```text
custom explicit state machine
no LangGraph orchestration core
```

---

# 2. current phase state

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

Do not start P2-1D.

Do not open Human QA yet.

---

# 3. accepted persistence lineage

P2-1A:

```text
commit:
4ea1fe6f7cb8e11ff5ccfde70462eba931c4071e

message:
feat(command-center): complete P2-1A read API foundation
```

P2-1B:

```text
commit:
62a3c5135a12afc38ba32e4c5f651c1f1b007549

tree:
1907a1839eb3cb7ccff4ef8eb8bb1371831d6492

parent:
4ea1fe6f7cb8e11ff5ccfde70462eba931c4071e

message:
feat(command-center): complete P2-1B shell and project queue
```

Current accepted HEAD remains P2-1B.

No P2-1C commit exists or is authorized.

---

# 4. P2-1C submitted candidate identity

Original Task:

```text
.aiassistant/tasks/done/20260903_1759_aiscc-p2-1c-workrun-transition-execution-detail-implementation-1.md
```

Submitted ZIP:

```text
20260903_1759_aiscc-p2-1c-workrun-transition-execution-detail-implementation-1.zip
```

ZIP SHA-256:

```text
7371d8d904d1bc4b052377fa0a29ed056661c691ea30994a3253b1d1c156bdc9
```

Task SHA-256:

```text
58dcbc5ff8e89ba849ebe5e4e3cfe914fff6d1b3c4e73909fd81567f95d828d4
```

Browser verified `TASK.md` is byte-identical to the issued Task.

Changed candidate paths:

```text
src/aiscc/api/routes/command_center_ui.py
src/aiscc/command_center/web.py
tests/integration/command_center/test_web_ui.py
tests/unit/command_center/test_web_shell.py
```

Exact candidate hashes:

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

Aggregate:

```text
13f07b59fdaedb706437967e6e2e1bb5253a555f4a385df0b39e6d15c58889eb
```

Browser independently recomputed this aggregate from the ZIP bytes.

This identity is a rejected/hold candidate baseline for the next rework, not an accepted product baseline.

---

# 5. candidate capabilities that should be preserved through rework

The current candidate already has the correct general P2-1C direction.

Preserve:

```text
GET /command-center/work-runs/{work_run_id}
```

Preserve exactly these runtime data authorities:

```text
GET /v1/command-center/work-runs/{work_run_id}
GET /v1/command-center/work-runs/{work_run_id}/transitions
GET /v1/command-center/work-runs/{work_run_id}/execution
```

Do not add P2-1D/P2-1E fetches.

Preserve:

- queue `WorkRun 상세` navigation only; do not redesign the accepted P2-1B queue;
- WorkRun/Task reference;
- WorkflowState/state_version;
- RuntimeMode;
- Task/Scope availability;
- blocker safe projection;
- transition ordered-list presentation;
- request/evaluation/guards/decision separation;
- `ADMITTED` / `DENIED` textual distinction;
- `DENIED` not presented as successful state transition;
- execution attempt/operation cards;
- `EXECUTOR_COMPLETED` explicitly not equal to WorkRun `ACCEPTED`;
- empty states;
- independent endpoint ETag/304;
- `10000ms` visible/nonterminal polling;
- hidden-tab polling stop;
- terminal-only polling stop;
- safe DOM;
- Korean-first;
- local/private security headers/CSP;
- no mutation controls;
- no new backend read authority.

---

# 6. exact blocker

The HOLD is caused by one source-contract defect that is visible directly in the submitted `web.py`.

The accepted Task requires:

```text
If WorkRun summary cannot be established as current/authoritative,
retained transition/execution DOM must not look newly current.

If last successful DOM is retained,
copy must explicitly indicate refresh failure/stale/last-successful semantics.
```

Current candidate sequence:

```text
successful refresh
→ transitionsState = "최신 전이 기록"
→ executionState = "최신 실행 기록"

later refresh
→ summary fails current-authority establishment
→ overall page state says failure / last snapshot retained
→ loadDetail returns before applyTransitions/applyExecution
→ previous section DOM remains
→ previous section labels also remain
```

Result:

```text
overall:
current WorkRun snapshot could not be established

section:
최신 전이 기록
최신 실행 기록
```

This is semantically contradictory.

The stale retained section must not remain labeled `최신`.

---

# 7. minimum rework requirement

The next Browser session should issue one narrow P2-1C REWORK Task.

The Task must require:

1. successful WorkRun detail state remains unchanged;
2. if a later summary refresh cannot establish current authority and prior detail data exists:
   - retain prior transition/execution DOM if desired;
   - immediately change transition/execution section read-state copy to explicit stale/last-successful/refresh-failed wording;
   - never leave `최신 전이 기록` / `최신 실행 기록`;
3. newly returned transition/execution payloads from that failed-summary refresh must not be applied as current;
4. endpoint ETag/data cache state should not be destructively reset merely to solve labeling;
5. next successful summary refresh may again apply/confirm current detail and restore `최신` labels;
6. add a deterministic test covering the actual state sequence:
   `successful refresh → summary authority failure → retained stale DOM + downgraded section labels`;
7. retain all P2-1C security, read-only, endpoint, polling, domain-semantic, responsive, and P2-1B regression boundaries.

No P2-1A API change is required.

No new package/config/migration is required.

---

# 8. testing gap to close

Current unit tests mostly prove source structure and string presence for the detail JavaScript.

They do not exercise the blocker sequence.

The rework test must prove behavior, not merely that a stale-warning string exists somewhere in source.

Required state assertion:

```text
after successful detail render:
section labels may say latest/current

after subsequent summary authority failure:
retained transition/execution data may remain visible
BUT
section labels must no longer say latest/current

page-level and section-level read-state copy must agree
```

If the project has no lightweight JS DOM harness and adding one would require a dependency/package change, do not add a package.

Use the narrowest deterministic test method supported by the existing repository and report any limitation honestly.

Do not broaden into Node/npm.

---

# 9. Human QA state

Human Browser/Visual remains:

```text
HUMAN_PENDING
QA_GATE_NOT_OPENED
```

Do not ask Human to QA the current candidate.

Do not issue a Human QA Task until the rework source/runtime candidate is substantively accepted by Browser Command Center.

Once source/runtime is accepted, the Human QA Gate should cover:

- WorkRun detail hierarchy;
- `ADMITTED` vs `DENIED` comprehensibility;
- execution readability;
- queue → detail → project navigation;
- 1080 / 1280 / 1440 at Zoom 100%;
- actual browser polling/hidden-tab/focus behavior;
- the reworked stale/current failure presentation if practical to reproduce.

---

# 10. transport ambiguity from the previous Task

The previous Task required pre-Move Cycle/Handoff SHA comparison, but the short prompt did not include the expected SHA values and also told the Executor to transport before reading the Task.

The Executor therefore reported comparing expected hashes after Move.

Browser independently verified final source identities:

```text
P2-1B Cycle:
f479952b982af8d7444494d4021db443b84135324a4e4a68f09f0b30355f2488

P2-1C entry Handoff:
ca813f7cd5775d0a2d649bddae6800b4cc8ad114b7ac7110aed4e1d52f7c276d
```

No artifact-integrity defect remains.

For the next transport contract, avoid the circular instruction.

Preferred:

```text
allow the Executor to read the Downloads Task read-only first,
then perform Task-specified pre-Move validation and Move
```

Alternative:

```text
repeat every required expected SHA in the short prompt
```

Do not create a separate product rework for this transport issue.

---

# 11. reported dirty/runtime residue

Executor reports test-created runtime residue:

```text
133 untracked __pycache__ / .pyc files
```

The original Task explicitly prohibited cleanup.

Destination rework Task should classify these as known reported task-runtime residue, not as accepted product source.

Do not use:

```text
git clean
git restore
git checkout
git reset
git stash
```

Do not silently delete the residue merely for clean status.

The rework can proceed against the known candidate dirt if the preflight confirms the workspace contains only:

- the expected P2-1C candidate product/test modifications;
- the already imported governance files;
- the exact done Task;
- task-created bytecode residue consistent with the reported class;
- no unrelated source/config/migration dirt.

If actual dirt exceeds that boundary, stop for `DIRTY_WORKSPACE_MIXED`.

Terminal persistence cleanup can be separately authorized later if needed.

---

# 12. previous Executor evidence

Executor reported:

```text
NEW_P2_1C_IMPLEMENTATION_CHAT:
PASS

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

These results may inform the rework Task's reuse scope only for byte-identical unaffected behavior.

They cannot substitute proof for the newly changed failure-state behavior.

The rework must directly test the changed stale/current label path.

---

# 13. judgment authority

Terminal judgment Cycle for this bundle:

```text
.aiassistant/records/aiscc/cycles/20260903_1934_aiscc-p2-1c-workrun-detail-substantive-review-hold-1.cycle.md
```

Judgment:

```text
HOLD_REWORK_REQUIRED
reject_cause: EXECUTOR_MISREAD_BASELINE
```

No P2-1C source acceptance.

No Human QA acceptance.

No commit authorization.

---

# 14. Browser session rule

The source Browser session must not issue the next Executor Task after bundle judgment.

Therefore:

```text
source session:
Cycle + Handoff only

destination new Browser session:
bootstrap from this Handoff
→ issue narrow P2-1C rework Task
```

---

# 15. preserved artifacts

Must survive cleanup:

- P2-1A commit `4ea1fe6f7cb8e11ff5ccfde70462eba931c4071e`
- P2-1B commit `62a3c5135a12afc38ba32e4c5f651c1f1b007549`
- `.aiassistant/tasks/done/20260903_1759_aiscc-p2-1c-workrun-transition-execution-detail-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260903_1718_aiscc-p2-1b-shell-queue-persistence-final-acceptance-1.cycle.md`
- `.aiassistant/reports/aiscc/20260903_1720_aiscc-browser-command-center-p2-1b-completion-p2-1c-entry-handoff-1.md`
- `.aiassistant/records/aiscc/cycles/20260903_1934_aiscc-p2-1c-workrun-detail-substantive-review-hold-1.cycle.md`
- `.aiassistant/reports/aiscc/20260903_1936_aiscc-browser-command-center-p2-1c-hold-rework-entry-handoff-1.md`

The original P2-1C target ZIP is temporary review material.

---

# 16. exact next action

```text
Browser:
NEW_CHAT_REQUIRED

next phase:
P2-1C

next work type:
REWORK

next title:
P2-1C retained-detail stale/current authority labeling rework

Task:
NOT_ISSUED_IN_SOURCE_SESSION

Human QA:
NOT_OPENED

P2-1D:
DO_NOT_START
```
