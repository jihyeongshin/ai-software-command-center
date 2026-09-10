# 작업지시서: P2-3 Stockroom Docker settlement final acceptance Git persistence

## meta

- task_id: `20260910_0943_aiscc-p2-3-stockroom-docker-settlement-final-acceptance-git-persistence-1`
- created_at: `2026-09-10T09:43:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `QA_ONLY / GIT_PERSISTENCE`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `d8fbcfa9d36a7531819149037240855cafdd088d`
- required_base_tree: `e224f31268057e400918ece352b72a0388d4091d`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `runtime source/test rework + regression → exact Git persistence`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. fresh-session Windows Python bootstrap

This Task begins in a fresh IDE Executor chat.

Do NOT assume any of these commands are usable through PATH:

```text
python
python3
py
```

Do NOT run bare `python` as a probe.

Known current Python interpreter candidate:

```text
C:\Users\oracl\AppData\Roaming\uv\python\cpython-3.12.14-windows-x86_64-none\python.exe
```

If Python is needed for transport/verification:

1. first verify that exact path exists and is executable;
2. if valid, use that exact executable path;
3. if unavailable, discover an actually executable Python interpreter first;
4. after discovery, invoke only the exact executable path.

Missing the known path alone is NOT a STOP condition.

Only inability to locate any required executable interpreter after discovery is a prerequisite blocker.

Repository-owned test commands, if ever explicitly authorized, use their exact `.venv\Scripts\...` executables rather than a bare Python command.

This persistence Task does not require test reruns.

# 1. inbound ZIP bootstrap

The Browser Short Prompt's delivery ZIP SHA-256 is the bootstrap integrity anchor.

Current delivery ZIP contains only:

```text
TASK:
20260910_0943_aiscc-p2-3-stockroom-docker-settlement-final-acceptance-git-persistence-1.md

CYCLE:
20260910_0943_aiscc-p2-3-stockroom-docker-settlement-accepted-persistence-entry-1.cycle.md
SHA-256:
a8f03c599f71b4f945f54e2e9a263192053b16ae9eb74d198b884ae3de88af25
destination:
.aiassistant/records/aiscc/cycles/20260910_0943_aiscc-p2-3-stockroom-docker-settlement-accepted-persistence-entry-1.cycle.md

JUDGMENT:
20260910_0943_aiscc-p2-3-stockroom-docker-settlement-final-acceptance-judgment-1.md
SHA-256:
c20a28836d6c7cb898ccc4d5bf6fc76e0acfa9fe9dfc5eb2e6b2f4624e2b722b
destination:
.aiassistant/reports/aiscc/20260910_0943_aiscc-p2-3-stockroom-docker-settlement-final-acceptance-judgment-1.md

HANDOFF:
none
```

Place TASK first at:

```text
.aiassistant/tasks/active/20260910_0943_aiscc-p2-3-stockroom-docker-settlement-final-acceptance-git-persistence-1.md
```

Read it, then place/hash-verify current Cycle/Judgment.

Bootstrap failures follow the persisted ZIP-direct workflow.

After canonical transport, inbound cleanup refusal is non-blocking.

# 2. repository gate

After current artifact placement require:

```text
branch:
main

HEAD:
d8fbcfa9d36a7531819149037240855cafdd088d

HEAD tree:
e224f31268057e400918ece352b72a0388d4091d

index:
empty
```

Expected Git-visible set excluding current active Task is exact 13 paths:

- `.aiassistant/tasks/done/20260910_0207_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_0207_aiscc-p2-3-phase1b-closed-actual-capture-runtime-entry-audit-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_0207_aiscc-p2-3-phase1b-terminal-state-reconciliation-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260910_0918_aiscc-p2-3-stockroom-docker-settlement-quarantine-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_0918_aiscc-p2-3-actual-capture-entry-audit-blocked-runtime-settlement-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_0918_aiscc-p2-3-runtime-settlement-canonical-conflict-judgment-1.md`
- `.aiassistant/tasks/done/20260910_0935_aiscc-p2-3-stockroom-docker-settlement-ruff-test-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_0935_aiscc-p2-3-stockroom-docker-settlement-static-failure-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_0935_aiscc-p2-3-stockroom-docker-settlement-static-failure-judgment-1.md`
- `src/aiscc/runtime/docker.py`
- `tests/unit/runtime/test_stockroom_docker_settlement.py`
- `.aiassistant/records/aiscc/cycles/20260910_0943_aiscc-p2-3-stockroom-docker-settlement-accepted-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_0943_aiscc-p2-3-stockroom-docker-settlement-final-acceptance-judgment-1.md`

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Do not cleanup, restore, stash, reset, overwrite or absorb.

# 3. exact accepted identity — 11 paths

Verify all exact hashes before staging:

- `.aiassistant/tasks/done/20260910_0207_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-1.md`  `e97b19297ce70d9ebb9f714b64ff83facf13e91c44f65c4ca6c4a0d0adb94cb0`
- `.aiassistant/records/aiscc/cycles/20260910_0207_aiscc-p2-3-phase1b-closed-actual-capture-runtime-entry-audit-1.cycle.md`  `5a68361c98b6165cdd6fa20adf0cc6ca8df99ada519c5c51efc6123f91c0b339`
- `.aiassistant/reports/aiscc/20260910_0207_aiscc-p2-3-phase1b-terminal-state-reconciliation-final-acceptance-judgment-1.md`  `e6e9266e9f6feedca478b7062d62af47c1b4442d8e719bb4e7ff8f9d59b3e6fa`
- `.aiassistant/tasks/done/20260910_0918_aiscc-p2-3-stockroom-docker-settlement-quarantine-rework-1.md`  `7448b8ee218e5b3494a10b2987cf2d18053fd11f686aba9ad9dbd1224bd3f747`
- `.aiassistant/records/aiscc/cycles/20260910_0918_aiscc-p2-3-actual-capture-entry-audit-blocked-runtime-settlement-rework-entry-1.cycle.md`  `239b189e270c4fb7e3896bda2ad4552708567b64d0e5abec5065b080277267d3`
- `.aiassistant/reports/aiscc/20260910_0918_aiscc-p2-3-runtime-settlement-canonical-conflict-judgment-1.md`  `5c811f58429fc37b4a212f922d12b52b7632e20f4bb6c7e217c5284246b5092e`
- `.aiassistant/tasks/done/20260910_0935_aiscc-p2-3-stockroom-docker-settlement-ruff-test-retry-1.md`  `dad3399834f5429776c495041c797b5df7478f30de152864a7b5d76708ea601c`
- `.aiassistant/records/aiscc/cycles/20260910_0935_aiscc-p2-3-stockroom-docker-settlement-static-failure-retry-entry-1.cycle.md`  `6bd00596359e8258969ad13bc09131ed1176fa7b868e4dc2a8c64a92508fd6b8`
- `.aiassistant/reports/aiscc/20260910_0935_aiscc-p2-3-stockroom-docker-settlement-static-failure-judgment-1.md`  `0a0dcd8aec677a961b5d4d3412d6797cf8f899ae791ac75c41eeac275bdfcfbd`
- `src/aiscc/runtime/docker.py`  `f338225c13195d69c41f69f00a47fc1d00c616c94458ef361e32b97f7fde96fa`
- `tests/unit/runtime/test_stockroom_docker_settlement.py`  `ebfb54d92dc446d2afe6bbe51ce261dbdabff92fa4650833f1d576fde6a755c6`

Require:

```text
11 / 11 exact
```

Any mismatch:

```text
ACCEPTED_CANDIDATE_IDENTITY_MISMATCH
→ STOP
```

Do not repair or re-edit.

# 4. accepted evidence reuse

If all 11 identities match exactly, reuse without test rerun:

```text
0935 settlement regression:
175 PASS / 0 skipped

0935 Stockroom tool regression:
5 PASS / 0 skipped

Python compile:
PASS

Ruff:
PASS

git diff --check:
PASS

runtime source invariant:
not settled → UNKNOWN_TOOL_OUTCOME + quarantine_required=true
```

No source/test mutation is authorized.

# 5. current acceptance identity

Verify:

```text
.aiassistant/records/aiscc/cycles/20260910_0943_aiscc-p2-3-stockroom-docker-settlement-accepted-persistence-entry-1.cycle.md
SHA-256:
a8f03c599f71b4f945f54e2e9a263192053b16ae9eb74d198b884ae3de88af25

.aiassistant/reports/aiscc/20260910_0943_aiscc-p2-3-stockroom-docker-settlement-final-acceptance-judgment-1.md
SHA-256:
c20a28836d6c7cb898ccc4d5bf6fc76e0acfa9fe9dfc5eb2e6b2f4624e2b722b
```

Current Task byte identity is anchored by the verified delivery ZIP and active/done byte equality.

# 6. pre-stage integrity

Require:

```text
git diff --check:
PASS

index:
empty

Git-visible:
13 exact excluding active Task

other source/config/test delta:
0
```

No test run.

# 7. Task lifecycle

Move:

```text
.aiassistant/tasks/active/20260910_0943_aiscc-p2-3-stockroom-docker-settlement-final-acceptance-git-persistence-1.md
→
.aiassistant/tasks/done/20260910_0943_aiscc-p2-3-stockroom-docker-settlement-final-acceptance-git-persistence-1.md
```

Do not edit bytes.

Then require:

```text
14 exact Git-visible commit candidates
```

# 8. exact final commit allowlist — 14

- `.aiassistant/tasks/done/20260910_0207_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_0207_aiscc-p2-3-phase1b-closed-actual-capture-runtime-entry-audit-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_0207_aiscc-p2-3-phase1b-terminal-state-reconciliation-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260910_0918_aiscc-p2-3-stockroom-docker-settlement-quarantine-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_0918_aiscc-p2-3-actual-capture-entry-audit-blocked-runtime-settlement-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_0918_aiscc-p2-3-runtime-settlement-canonical-conflict-judgment-1.md`
- `.aiassistant/tasks/done/20260910_0935_aiscc-p2-3-stockroom-docker-settlement-ruff-test-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_0935_aiscc-p2-3-stockroom-docker-settlement-static-failure-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_0935_aiscc-p2-3-stockroom-docker-settlement-static-failure-judgment-1.md`
- `src/aiscc/runtime/docker.py`
- `tests/unit/runtime/test_stockroom_docker_settlement.py`
- `.aiassistant/records/aiscc/cycles/20260910_0943_aiscc-p2-3-stockroom-docker-settlement-accepted-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_0943_aiscc-p2-3-stockroom-docker-settlement-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260910_0943_aiscc-p2-3-stockroom-docker-settlement-final-acceptance-git-persistence-1.md`

No other path may be staged.

# 9. Git persistence

Only after all prior gates PASS:

```text
git add -- <14 exact literal paths>
git diff --cached --check
git diff --cached --name-status
```

Require:

```text
staged:
14 exact

extra:
0

missing:
0

unstaged tracked:
0
```

Commit:

```text
git commit -m "fix(runtime): quarantine unsettled Stockroom process"
```

Expected:

```text
parent:
d8fbcfa9d36a7531819149037240855cafdd088d

parent count:
1

message:
fix(runtime): quarantine unsettled Stockroom process

changed paths:
14 exact
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
2. parent `d8fbcfa9d36a7531819149037240855cafdd088d`;
3. parent count 1;
4. exact commit message;
5. changed paths exact 14;
6. accepted 11 committed bytes equal exact hashes;
7. current Cycle/Judgment/Task bytes equal issued bytes;
8. runtime source/test exact accepted hashes;
9. index empty;
10. Git-visible worktree clean;
11. push/network NOT_RUN.

# 11. committed runtime semantic identity

Without executing Docker/process/scenario, verify committed source still contains:

```text
settled =
termination_proven
and owner_reconciled

not settled:
UNKNOWN_TOOL_OUTCOME
quarantine_required=true
```

and that ordinary known success/failure classification follows only after the settled check.

This is source identity verification, not runtime proof.

# 12. export bundle + outbound ZIP

Bundle folder:

```text
.aiassistant/reports/target/20260910_0943_aiscc-p2-3-stockroom-docker-settlement-final-acceptance-git-persistence-1/
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

Include byte-preserving committed copies of all 14 commit paths.

Create adjacent outbound ZIP.

Use supported Windows extended-length path handling from the outset if needed for deep export paths.

Require:

```text
one top-level bundle directory
readable / CRC PASS
required roots present
14 committed copies present
manifest coverage
source/commit/export byte equality
folder/archive byte equality
```

Keep folder and ZIP.

# 13. strict execution ceiling

Do NOT run:

```text
pytest
Docker CLI/daemon/image
Stockroom process/CLI
provider/tool
DB
materializer
scenario
network
Replay
```

Git persistence commands explicitly authorized above are allowed.

# 14. evidence contract

executor_required:

- fresh-session interpreter discovery discipline
- inbound transport
- exact 13-path preflight
- exact 11-path accepted identity
- exact 14-path staging/commit
- post-commit clean state
- committed runtime semantic identity
- outbound ZIP

reuse_allowed:

- 0935 accepted test/static evidence under exact byte identity
- 0918 canonical conflict diagnosis
- persisted Phase 1B contracts

human_owned:

```text
new Human QA:
NOT_REQUIRED

S4 HumanResult:
HUMAN_PENDING

public distribution/license:
HUMAN_PENDING
```

forbidden:

- source/test re-edit
- test rerun
- capture audit continuation
- actual runtime/scenario execution
- DB/Docker/provider/tool
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

Missing the known uv-Python path alone is not a blocker if another executable interpreter can be discovered.

# 16. final ceiling

Success:

```text
runtime settlement fix:
PERSISTED / READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT

actual-capture entry audit:
STILL_INCOMPLETE

actual scenario execution:
NOT_STARTED

Replay:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

Do not resume the wider capture audit in this Task.
