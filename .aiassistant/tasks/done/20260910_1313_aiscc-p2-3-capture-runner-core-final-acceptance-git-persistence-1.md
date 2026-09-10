# 작업지시서: P2-3 capture-runner core final acceptance Git persistence

## meta

- task_id: `20260910_1313_aiscc-p2-3-capture-runner-core-final-acceptance-git-persistence-1`
- created_at: `2026-09-10T13:13:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `QA_ONLY / GIT_PERSISTENCE`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `04343b8518c76c3fb7ed3f0afaf92bc7e79cbdcf`
- required_base_tree: `992a15a33e8b34cc3da35f44bd846ceddccb2526`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `A1 source/test rework + regression → exact Git persistence`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. fresh-session Windows Python bootstrap

This Task begins in a fresh IDE Executor chat.

Do NOT assume any of these commands are valid through PATH:

```text
python
python3
py
```

Do NOT execute bare `python` as a probe.

Known current interpreter candidate:

```text
C:\Users\oracl\AppData\Roaming\uv\python\cpython-3.12.14-windows-x86_64-none\python.exe
```

If Python is needed for transport/hash verification:

1. verify this exact executable path first;
2. if valid, use it by exact path;
3. if unavailable, discover an actually executable Python interpreter;
4. invoke only the exact discovered executable path.

The known path being absent alone is NOT a STOP condition.

This persistence Task does not require pytest.

# 1. inbound ZIP bootstrap

The Browser Short Prompt exact delivery ZIP SHA-256 is the bootstrap integrity anchor.

Current delivery ZIP contains only:

```text
TASK:
20260910_1313_aiscc-p2-3-capture-runner-core-final-acceptance-git-persistence-1.md

CYCLE:
20260910_1313_aiscc-p2-3-capture-runner-core-accepted-persistence-entry-1.cycle.md
SHA-256:
6b3add412720dfec4ad50e4a7cf3784547385de377b4dc478a9a749fc0d913c9
destination:
.aiassistant/records/aiscc/cycles/20260910_1313_aiscc-p2-3-capture-runner-core-accepted-persistence-entry-1.cycle.md

JUDGMENT:
20260910_1313_aiscc-p2-3-capture-runner-core-final-acceptance-judgment-1.md
SHA-256:
5f37b367fac55c0ce782bdea7f06b9931e6537bd52c3c191625d7d88639d3799
destination:
.aiassistant/reports/aiscc/20260910_1313_aiscc-p2-3-capture-runner-core-final-acceptance-judgment-1.md

HANDOFF:
none
```

Place TASK first at:

```text
.aiassistant/tasks/active/20260910_1313_aiscc-p2-3-capture-runner-core-final-acceptance-git-persistence-1.md
```

Read it, then place/hash-verify current Cycle/Judgment.

Bootstrap failure before canonical TASK placement:

```text
STOP
no report/export
no substantive project mutation
```

After canonical transport, Downloads cleanup is best-effort/non-blocking.

# 2. repository gate

After current Cycle/Judgment placement require:

```text
branch:
main

HEAD:
04343b8518c76c3fb7ed3f0afaf92bc7e79cbdcf

HEAD tree:
992a15a33e8b34cc3da35f44bd846ceddccb2526

index:
empty
```

Expected Git-visible set excluding current active Task is exact 20 paths:

- `.aiassistant/tasks/done/20260910_1008_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1008_aiscc-p2-3-stockroom-settlement-persisted-runtime-entry-audit-retry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1008_aiscc-p2-3-stockroom-settlement-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1040_aiscc-p2-3-actual-capture-runner-core-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1040_aiscc-p2-3-runtime-entry-audit-accepted-capture-runner-core-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1040_aiscc-p2-3-actual-capture-runtime-entry-audit-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1039_aiscc-p2-3-actual-capture-runner-core-ruff-test-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1039_aiscc-p2-3-capture-runner-core-static-failure-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1039_aiscc-p2-3-capture-runner-core-static-failure-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1142_aiscc-p2-3-capture-runner-owner-status-state-authority-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1142_aiscc-p2-3-capture-runner-owner-status-authority-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1142_aiscc-p2-3-capture-runner-owner-status-state-authority-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1157_aiscc-p2-3-capture-runner-nonworkflow-snapshot-binding-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1157_aiscc-p2-3-capture-runner-nonworkflow-snapshot-binding-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1157_aiscc-p2-3-capture-runner-nonworkflow-snapshot-binding-judgment-1.md`
- `src/aiscc/scenarios/capture_runner.py`
- `src/aiscc/scenarios/driver.py`
- `tests/unit/scenarios/test_stockroom_capture_runner.py`
- `.aiassistant/records/aiscc/cycles/20260910_1313_aiscc-p2-3-capture-runner-core-accepted-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1313_aiscc-p2-3-capture-runner-core-final-acceptance-judgment-1.md`

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Do not cleanup, restore, stash, reset, overwrite or absorb.

# 3. exact accepted identity — 18 paths

Before any staging verify:

- `.aiassistant/tasks/done/20260910_1008_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-retry-1.md`  `11db99ba9b22ed8e6dddab96d49d1a9207b928b846c93e53bcd88e48a8d10f52`
- `.aiassistant/records/aiscc/cycles/20260910_1008_aiscc-p2-3-stockroom-settlement-persisted-runtime-entry-audit-retry-1.cycle.md`  `3cc310ccfe052307a906fe2524db6176f7af0d38ba53616096df6ece0ff581a0`
- `.aiassistant/reports/aiscc/20260910_1008_aiscc-p2-3-stockroom-settlement-persistence-final-acceptance-judgment-1.md`  `6cb059aa4206ac5e1f00789e8adbc955f574bf84c71b2e551c4f23a414e51ff0`
- `.aiassistant/tasks/done/20260910_1040_aiscc-p2-3-actual-capture-runner-core-implementation-1.md`  `0109756f710d26b625b42ec90c98f0dd585cad36445473e9fb9e4e20e964d3d2`
- `.aiassistant/records/aiscc/cycles/20260910_1040_aiscc-p2-3-runtime-entry-audit-accepted-capture-runner-core-entry-1.cycle.md`  `6a6195c8c430a9d292c765f6a044992970b945518c25a12e506737873999bbbb`
- `.aiassistant/reports/aiscc/20260910_1040_aiscc-p2-3-actual-capture-runtime-entry-audit-final-acceptance-judgment-1.md`  `48e84d88626bcd5804ff4f3f9c580c7f9d4efa28ea974adb5f69498afa8555c3`
- `.aiassistant/tasks/done/20260910_1039_aiscc-p2-3-actual-capture-runner-core-ruff-test-retry-1.md`  `ed429af33012ecc73613badd4fc743181b5570accccd931be91e24f0bcf81dbf`
- `.aiassistant/records/aiscc/cycles/20260910_1039_aiscc-p2-3-capture-runner-core-static-failure-retry-entry-1.cycle.md`  `56de671d96c839d91d8457ed3c131f152627211ed825489a0222399041b844b6`
- `.aiassistant/reports/aiscc/20260910_1039_aiscc-p2-3-capture-runner-core-static-failure-judgment-1.md`  `5a97033467671e9cbeddc66f8d3010cc8e45bab32d11be1307d8415e8b999983`
- `.aiassistant/tasks/done/20260910_1142_aiscc-p2-3-capture-runner-owner-status-state-authority-rework-1.md`  `1c663fa72c263d5176db907e418f33811aa7f4174bc6db764d4ddb74c17f6648`
- `.aiassistant/records/aiscc/cycles/20260910_1142_aiscc-p2-3-capture-runner-owner-status-authority-rework-entry-1.cycle.md`  `d23c0d5108aa26d7b66b02dcbb0dc047eedd871ba5f208fb7b675758d71d2b63`
- `.aiassistant/reports/aiscc/20260910_1142_aiscc-p2-3-capture-runner-owner-status-state-authority-judgment-1.md`  `079d0593ef198b4f3adebd01bb2e74aebbed645e0550563e90b5b92aea1c5f5c`
- `.aiassistant/tasks/done/20260910_1157_aiscc-p2-3-capture-runner-nonworkflow-snapshot-binding-rework-1.md`  `ec44d11ce4415e25fb3d9fa89d50d2fcd4f09332dc21816fae996cc0777fee5f`
- `.aiassistant/records/aiscc/cycles/20260910_1157_aiscc-p2-3-capture-runner-nonworkflow-snapshot-binding-rework-entry-1.cycle.md`  `dd4d4bf3a8cbfcf35fbdd849fcf22609fa19a6474c05eefdff959f475de094bf`
- `.aiassistant/reports/aiscc/20260910_1157_aiscc-p2-3-capture-runner-nonworkflow-snapshot-binding-judgment-1.md`  `091813d26152595a0c12bf82fd16827dcc105b31bbff6cc3c144bf0a0d8231f9`
- `src/aiscc/scenarios/capture_runner.py`  `600de0a4b0e718f02ab2e1907b7be62b2c4a23756559fdf99cb4cd55fb80b3d2`
- `src/aiscc/scenarios/driver.py`  `9871847ec0a236ef61c91518ff95764f3c2138e3854c25a4c8cab4f028503ce6`
- `tests/unit/scenarios/test_stockroom_capture_runner.py`  `a137021608ac9cb5b4c328b6bb88fd0c22cb0d9afd9b1a22054ec5bdd32f68ff`

Require:

```text
18 / 18 exact
```

Any mismatch:

```text
ACCEPTED_CANDIDATE_IDENTITY_MISMATCH
→ STOP
```

Do not repair/re-edit.

# 4. current acceptance identity

Verify:

```text
.aiassistant/records/aiscc/cycles/20260910_1313_aiscc-p2-3-capture-runner-core-accepted-persistence-entry-1.cycle.md
SHA-256:
6b3add412720dfec4ad50e4a7cf3784547385de377b4dc478a9a749fc0d913c9

.aiassistant/reports/aiscc/20260910_1313_aiscc-p2-3-capture-runner-core-final-acceptance-judgment-1.md
SHA-256:
5f37b367fac55c0ce782bdea7f06b9931e6537bd52c3c191625d7d88639d3799
```

Current TASK byte identity is anchored by the verified delivery ZIP and active→done byte equality.

# 5. evidence reuse

If the exact 18-path identity passes, reuse without test rerun:

```text
A1 unit:
51 PASS

B3 regression:
18 PASS

compile:
3 / 3 PASS

Ruff:
3 / 3 PASS

git diff --check:
PASS

contract review:
20 / 20 PASS
```

No source/test/config mutation is authorized.

# 6. pre-stage integrity

Require:

```text
git diff --check:
PASS

index:
empty

Git-visible excluding active Task:
20 exact

other source/config/test delta:
0
```

No tests.

# 7. Task lifecycle

Move without editing bytes:

```text
.aiassistant/tasks/active/20260910_1313_aiscc-p2-3-capture-runner-core-final-acceptance-git-persistence-1.md
→
.aiassistant/tasks/done/20260910_1313_aiscc-p2-3-capture-runner-core-final-acceptance-git-persistence-1.md
```

Then require:

```text
21 exact Git-visible commit candidates
```

# 8. exact final commit allowlist — 21

- `.aiassistant/tasks/done/20260910_1008_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1008_aiscc-p2-3-stockroom-settlement-persisted-runtime-entry-audit-retry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1008_aiscc-p2-3-stockroom-settlement-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1040_aiscc-p2-3-actual-capture-runner-core-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1040_aiscc-p2-3-runtime-entry-audit-accepted-capture-runner-core-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1040_aiscc-p2-3-actual-capture-runtime-entry-audit-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1039_aiscc-p2-3-actual-capture-runner-core-ruff-test-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1039_aiscc-p2-3-capture-runner-core-static-failure-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1039_aiscc-p2-3-capture-runner-core-static-failure-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1142_aiscc-p2-3-capture-runner-owner-status-state-authority-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1142_aiscc-p2-3-capture-runner-owner-status-authority-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1142_aiscc-p2-3-capture-runner-owner-status-state-authority-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1157_aiscc-p2-3-capture-runner-nonworkflow-snapshot-binding-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1157_aiscc-p2-3-capture-runner-nonworkflow-snapshot-binding-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1157_aiscc-p2-3-capture-runner-nonworkflow-snapshot-binding-judgment-1.md`
- `src/aiscc/scenarios/capture_runner.py`
- `src/aiscc/scenarios/driver.py`
- `tests/unit/scenarios/test_stockroom_capture_runner.py`
- `.aiassistant/records/aiscc/cycles/20260910_1313_aiscc-p2-3-capture-runner-core-accepted-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1313_aiscc-p2-3-capture-runner-core-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1313_aiscc-p2-3-capture-runner-core-final-acceptance-git-persistence-1.md`

No other path may be staged.

# 9. Git persistence

Only after all prior gates PASS:

```text
git add -- <21 exact literal paths>
git diff --cached --check
git diff --cached --name-status
```

Require:

```text
staged:
21 exact

extra:
0

missing:
0

unstaged tracked:
0
```

Commit exactly:

```text
git commit -m "feat(orchestration): persist P2-3 capture runner core"
```

Expected:

```text
parent:
04343b8518c76c3fb7ed3f0afaf92bc7e79cbdcf

parent count:
1

message:
feat(orchestration): persist P2-3 capture runner core

changed paths:
21 exact
```

Forbidden:

```text
git add -A
git add .
git reset
git restore
git checkout
git stash
git clean
git push
git pull
git fetch
git merge
git rebase
git cherry-pick
```

# 10. post-commit verification

Verify:

1. result commit/tree;
2. parent `04343b8518c76c3fb7ed3f0afaf92bc7e79cbdcf`;
3. parent count 1;
4. exact commit message;
5. changed paths exact 21;
6. all accepted 18 committed bytes equal exact hashes;
7. current Cycle/Judgment/Task equal issued bytes;
8. A1 final three paths have exact accepted hashes;
9. index empty;
10. Git-visible worktree clean;
11. push/network NOT_RUN.

# 11. committed source semantic spot-check

Without executing runtime, verify committed runner still enforces:

```text
operation-specific exact expected status

initial_ready:
exact READY / expected version

transition:
exact requested target / observed version + 1

non-workflow expected-status result:
exact current authoritative state/version required

non-workflow mismatch:
OWNER_RESULT_STATE_VERSION_MISMATCH
STOP / no authority advancement
```

This is source identity verification, not new runtime proof.

# 12. strict execution ceiling

Do NOT run:

```text
pytest
DB
Docker
Stockroom process
materialization
provider/tool
network
HumanResult
real Judgment
actual scenario
Replay
```

Only the explicitly authorized Git persistence commands may mutate repository state.

# 13. export bundle + outbound ZIP

Bundle folder:

```text
.aiassistant/reports/target/20260910_1313_aiscc-p2-3-capture-runner-core-final-acceptance-git-persistence-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
CANDIDATE_IDENTITY_VERIFICATION.md
GIT_PERSISTENCE_VERIFICATION.md
```

Include byte-preserving committed copies of all 21 changed paths.

Create adjacent outbound ZIP.

Use supported Windows extended-length path handling from the outset if needed.

Require:

```text
one top-level bundle directory
readable / CRC PASS
required root files present
21 committed copies present
manifest coverage
source/commit/export byte equality
folder/archive byte equality
```

Keep folder and ZIP.

# 14. evidence contract

executor_required:

- fresh-session Python discovery discipline
- inbound transport
- exact 20-path preflight
- exact 18-path accepted identity
- exact 21-path staging/commit
- post-commit clean state
- source semantic spot-check
- outbound ZIP

reuse_allowed:

- accepted 1157 evidence
- prior A1/B3 executed tests under exact byte identity
- accepted 1008 runtime-entry audit
- persisted Phase 1B/settlement fix

human_owned:

```text
S4 HumanResult:
HUMAN_PENDING

public distribution/license:
HUMAN_PENDING
```

forbidden:

- source/test re-edit
- test rerun
- A2 implementation
- DB/Docker/provider/tool/materializer runtime
- actual capture
- Replay
- Git network/push

# 15. mandatory stop

```text
DOWNLOAD_ZIP_MISSING
DOWNLOAD_ZIP_HASH_MISMATCH
DOWNLOAD_ZIP_CORRUPT
DOWNLOAD_TASK_MEMBER_MISSING
DOWNLOAD_TASK_PLACEMENT_FAILED
PYTHON_INTERPRETER_REQUIRED_BUT_NOT_FOUND
TRANSPORT_FAILURE
HEAD_OR_TREE_MISMATCH
INDEX_NOT_EMPTY
DIRTY_WORKSPACE_MIXED
ACCEPTED_CANDIDATE_IDENTITY_MISMATCH
GIT_STAGE_ALLOWLIST_MISMATCH
GIT_COMMIT_VERIFICATION_FAILED
UNEXPECTED_WORKSPACE_DELTA
ZIP_EXPORT_FAILED
```

No substantive work after a mandatory STOP.

# 16. final ceiling

Success:

```text
P2-3 A1 capture-runner core:
PERSISTED / READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT

A2 production owner/bootstrap integration:
NOT_STARTED

runtime prerequisites:
NOT_VERIFIED

actual scenario:
NOT_STARTED

Replay:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

Do not begin A2 in this Task.
