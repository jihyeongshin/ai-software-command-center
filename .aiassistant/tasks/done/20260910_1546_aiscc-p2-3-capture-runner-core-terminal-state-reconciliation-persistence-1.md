# 작업지시서: P2-3 capture-runner core terminal state reconciliation persistence

## meta

- task_id: `20260910_1546_aiscc-p2-3-capture-runner-core-terminal-state-reconciliation-persistence-1`
- created_at: `2026-09-10T15:46:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `COMMAND_CENTER_RECORD_UPDATE / GIT_PERSISTENCE`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `6385ab41a92e43e438e8992bacf929e7daf5130d`
- required_base_tree: `f4e3ee79d53e5c5b960992af8de5f477c704c1a0`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `read-only post-commit reconciliation → canonical state/governance Git persistence`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. fresh-session Windows Python bootstrap

Do NOT assume:

```text
python
python3
py
```

is valid on PATH.

Do NOT run bare `python` as an interpreter probe.

Known current interpreter candidate:

```text
C:\Users\oracl\AppData\Roaming\uv\python\cpython-3.12.14-windows-x86_64-none\python.exe
```

If Python is needed for transport/hash verification:

1. verify that exact executable first;
2. use it by exact path when valid;
3. if unavailable, discover another actually executable interpreter;
4. invoke only an exact executable path.

No pytest is required by this Task.

# 1. inbound transport

The Browser Short Prompt delivery ZIP SHA-256 is the bootstrap integrity anchor.

Place this TASK first at:

```text
.aiassistant/tasks/active/20260910_1546_aiscc-p2-3-capture-runner-core-terminal-state-reconciliation-persistence-1.md
```

Then place and hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260910_1546_aiscc-p2-3-capture-runner-core-final-accepted-a2-entry-1.cycle.md
SHA-256:
842c3dd58607e7fd3996a66a874b9aa01588f702b7516d625223c3d6665c53bb

.aiassistant/reports/aiscc/20260910_1546_aiscc-p2-3-capture-runner-core-persistence-final-acceptance-judgment-1.md
SHA-256:
337a13ce7c3f226620c3a2921f2e2977f93404d52b55c1d886645657f4a04953
```

Bootstrap failure before canonical TASK placement:

```text
STOP
no report/export
no substantive project mutation
```

# 2. repository gate

Require:

```text
branch:
main

HEAD:
6385ab41a92e43e438e8992bacf929e7daf5130d

HEAD tree:
f4e3ee79d53e5c5b960992af8de5f477c704c1a0

parent:
04343b8518c76c3fb7ed3f0afaf92bc7e79cbdcf

index:
empty
```

Expected Git-visible set excluding current active Task is exact 8 paths:

- `.aiassistant/tasks/done/20260910_1425_aiscc-p2-3-capture-runner-core-postcommit-eol-reconciliation-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1425_aiscc-p2-3-capture-runner-core-postcommit-eol-reconciliation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1425_aiscc-p2-3-capture-runner-core-postcommit-eol-reconciliation-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1515_aiscc-p2-3-capture-runner-core-reconciliation-evidence-export-transport-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1515_aiscc-p2-3-capture-runner-core-transport-failure-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1515_aiscc-p2-3-capture-runner-core-1428-transport-failure-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1546_aiscc-p2-3-capture-runner-core-final-accepted-a2-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1546_aiscc-p2-3-capture-runner-core-persistence-final-acceptance-judgment-1.md`

Ignored target/export artifacts may exist and are non-blocking.

Any other Git-visible path:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Do not cleanup/reset/restore/stash.

# 3. exact pending governance identities

Require 1425 exact:

- `.aiassistant/tasks/done/20260910_1425_aiscc-p2-3-capture-runner-core-postcommit-eol-reconciliation-audit-1.md`  `d85a672ae6ce2ea19a75d10696fde186e655444e26ae7a184add73d5053a11c6`
- `.aiassistant/records/aiscc/cycles/20260910_1425_aiscc-p2-3-capture-runner-core-postcommit-eol-reconciliation-entry-1.cycle.md`  `0c5b7b202830f9db97b2290620bd9904cdfbdea2f3fbf6991c4cf3d7a63a773f`
- `.aiassistant/reports/aiscc/20260910_1425_aiscc-p2-3-capture-runner-core-postcommit-eol-reconciliation-judgment-1.md`  `7d114c43fbc8f5c4f32eb06fe0fc94b301306d557e07af004c7d1e7a2e6ef727`

Require 1515 exact:

- `.aiassistant/tasks/done/20260910_1515_aiscc-p2-3-capture-runner-core-reconciliation-evidence-export-transport-retry-1.md`  `8a0bf45023e847e2d97447e0affe3c336c55b3b594e870b82420497259841ebe`
- `.aiassistant/records/aiscc/cycles/20260910_1515_aiscc-p2-3-capture-runner-core-transport-failure-retry-entry-1.cycle.md`  `0d553a420c9a752fe53cc1b0bbd5bb37358d4009ca54c9c43bc27aa3d6850ec0`
- `.aiassistant/reports/aiscc/20260910_1515_aiscc-p2-3-capture-runner-core-1428-transport-failure-judgment-1.md`  `f8d10a8baa583139769ff2193cd43bcda8405789e48955fcbd677d9915e50cd7`

Any mismatch:

```text
PENDING_GOVERNANCE_IDENTITY_MISMATCH
→ STOP
```

# 4. exact accepted A1 committed identity

Read the exact committed blobs at current HEAD and require:

- `src/aiscc/scenarios/capture_runner.py`  `600de0a4b0e718f02ab2e1907b7be62b2c4a23756559fdf99cb4cd55fb80b3d2`
- `src/aiscc/scenarios/driver.py`  `9871847ec0a236ef61c91518ff95764f3c2138e3854c25a4c8cab4f028503ce6`
- `tests/unit/scenarios/test_stockroom_capture_runner.py`  `a137021608ac9cb5b4c328b6bb88fd0c22cb0d9afd9b1a22054ec5bdd32f68ff`

Use commit-object raw bytes.

Require:

```text
3 / 3 RAW_EXACT
```

No newline normalization should be necessary for these three at current HEAD.

Any mismatch:

```text
ACCEPTED_A1_COMMIT_IDENTITY_MISMATCH
→ STOP
```

# 5. mutation allowlist

Only these tracked state files may be modified:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

No product/config/test/rule/template/decision-register mutation.

Current Cycle/Judgment/Task lifecycle changes are governance transport/persistence.

# 6. CURRENT_STATE_SUMMARY exact semantic update

Read the current file fully.

Preserve existing historical facts not superseded by this Task.

Update only the current P2/P2-3 phase projection so it truthfully contains these facts:

```text
P2:
IN_PROGRESS

P2-3:
IN_PROGRESS

Phase 1A:
ACCEPTED / CLOSED / PERSISTED

Phase 1B B1/B2/B3:
ACCEPTED / CLOSED / PERSISTED

actual-capture runtime-entry audit:
ACCEPTED / COMPLETE

Stockroom process settlement fix:
ACCEPTED / CLOSED / PERSISTED

A1 capture-runner core:
ACCEPTED / CLOSED / PERSISTED

A1 source commit:
6385ab41a92e43e438e8992bacf929e7daf5130d

A1 post-commit reconciliation:
PASS / 21 of 21 RAW_EXACT / amend not required

A2 production owner/bootstrap integration:
NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE_REGION

runtime prerequisites:
NOT_VERIFIED

actual S1-S4 scenario execution:
NOT_STARTED

capture/export corpus:
NOT_STARTED

Replay:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED

PUBLIC_RECORDED_REPLAY:
NOT_ADMITTED

public distribution/license:
HUMAN_PENDING
```

Do not mark:

```text
P2-3 CLOSED
actual capture complete
runtime ready
public release
```

# 7. NEXT_ACTIONS exact semantic update

Read current file fully.

Preserve unrelated valid next actions.

Make the first executable P2-3 action:

```text
P2-3 A2 — production owner/bootstrap integration
```

Its purpose must state:

```text
bind the accepted A1 capture runner to real production-style durable owners
resolve exact bootstrap construction
resolve exact evidence/Human/Judgment policy/config enrollment
add bounded PostgreSQL-backed integration proof
do not execute Docker/materialization/provider/tool/actual scenario
```

Before A2 product/config mutation, the next Browser-issued Task may include a bounded pre-mutation feasibility/source gate to resolve exact config paths.

Mark later sequence explicitly behind A2:

```text
runtime prerequisite provisioning/verification
→ S1 private actual capture
→ S2/S3/S4 private captures
→ durable capture corpus/sanitization/export
→ Recorded Replay
```

Do not make public Live/Replay the immediate next action.

# 8. state file verification

After editing require:

```text
both files:
UTF-8 strict

git diff --check:
PASS

no product/config/test/rule delta:
PASS

index:
empty
```

Review diff to ensure no unrelated historical deletion or broad reformat.

If broad rewrite occurred:

```text
STATE_RECORD_SCOPE_MISMATCH
→ STOP
```

# 9. Task lifecycle

Before lifecycle expected Git-visible:

```text
pending governance:
8

state files:
2

total excluding active Task:
10
```

Move TASK byte-identically:

```text
.aiassistant/tasks/active/20260910_1546_aiscc-p2-3-capture-runner-core-terminal-state-reconciliation-persistence-1.md
→
.aiassistant/tasks/done/20260910_1546_aiscc-p2-3-capture-runner-core-terminal-state-reconciliation-persistence-1.md
```

Then require exact final Git-visible set:

- `.aiassistant/tasks/done/20260910_1425_aiscc-p2-3-capture-runner-core-postcommit-eol-reconciliation-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1425_aiscc-p2-3-capture-runner-core-postcommit-eol-reconciliation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1425_aiscc-p2-3-capture-runner-core-postcommit-eol-reconciliation-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1515_aiscc-p2-3-capture-runner-core-reconciliation-evidence-export-transport-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1515_aiscc-p2-3-capture-runner-core-transport-failure-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1515_aiscc-p2-3-capture-runner-core-1428-transport-failure-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1546_aiscc-p2-3-capture-runner-core-final-accepted-a2-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1546_aiscc-p2-3-capture-runner-core-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
- `.aiassistant/tasks/done/20260910_1546_aiscc-p2-3-capture-runner-core-terminal-state-reconciliation-persistence-1.md`

Exactly:

```text
11 paths
index empty
```

# 10. exact Git persistence

Stage only the exact 11 paths from section 9.

Use explicit literal path allowlist.

Do not use:

```text
git add .
git add -A
```

Require:

```text
git diff --cached --check:
PASS

staged:
11 exact

extra:
0

missing:
0

unstaged tracked:
0
```

Commit exactly:

```text
git commit -m "docs(command-center): close P2-3 capture runner core and enter A2"
```

Expected:

```text
parent:
6385ab41a92e43e438e8992bacf929e7daf5130d

parent count:
1

changed paths:
11 exact
```

No amend/reset/rebase.

No push/network.

# 11. post-commit verification

Verify from commit object:

```text
parent:
6385ab41a92e43e438e8992bacf929e7daf5130d

message:
docs(command-center): close P2-3 capture runner core and enter A2

changed paths:
11 exact

current Cycle/Judgment/Task:
byte identity exact to delivery

A1 source/test:
unchanged exact

CURRENT_STATE_SUMMARY:
contains section 6 facts

NEXT_ACTIONS:
contains section 7 ordering

index:
empty

Git-visible worktree:
clean
```

For Browser-issued/current governance docs, if any text identity question arises, read raw commit-object bytes rather than text-mode converted output.

# 12. strict execution ceiling

Do NOT run:

```text
pytest
DB
Docker
materializer
provider/tool
network
actual scenario
HumanResult
Judgment runtime issuance
Replay
```

No product/config/test mutation.

# 13. export

Bundle:

```text
.aiassistant/reports/target/20260910_1546_aiscc-p2-3-capture-runner-core-terminal-state-reconciliation-persistence-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
STATE_RECONCILIATION_VERIFICATION.md
GIT_PERSISTENCE_VERIFICATION.md
```

Include byte-preserving committed copies of all 11 changed paths.

Expected bundle:

```text
6 root docs
11 committed copies
17 members total
```

`EXPORT_MANIFEST.md` must cover all 16 non-self entries with SHA-256 + byte size.

Verify CRC, one top-level directory, exact members, folder/archive byte equality.

# 14. mandatory stop

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
PENDING_GOVERNANCE_IDENTITY_MISMATCH
ACCEPTED_A1_COMMIT_IDENTITY_MISMATCH
STATE_RECORD_SCOPE_MISMATCH
GIT_STAGE_ALLOWLIST_MISMATCH
GIT_COMMIT_VERIFICATION_FAILED
UNEXPECTED_WORKSPACE_DELTA
ZIP_EXPORT_FAILED
```

# 15. final ceiling

Success:

```text
P2-3 A1 capture-runner core:
ACCEPTED / CLOSED / PERSISTED / TERMINAL STATE RECONCILED

A2 production owner/bootstrap integration:
ENTRY_READY / NEXT_EXECUTABLE_REGION

runtime prerequisites:
NOT_VERIFIED

actual scenario:
NOT_STARTED

Replay:
NOT_STARTED
```

Do not begin A2 inside this Task.
