# 작업지시서: P2-3 Phase 1B terminal state / actual capture entry reconciliation

## meta

- task_id: `20260910_0205_aiscc-p2-3-phase1b-terminal-state-actual-capture-entry-reconciliation-1`
- created_at: `2026-09-10T02:05:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `COMMAND_CENTER_RECORD_UPDATE / GIT_PERSISTENCE`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `cf3d8c28efbc7c382f7253dde443b60419d9386b`
- required_base_tree: `a52c6ff488d457c228a2f51059c92007a8e9bea3`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. inbound ZIP bootstrap

The Browser Short Prompt's exact delivery ZIP SHA-256 is the bootstrap integrity anchor.

Current delivery ZIP contains only:

```text
TASK:
20260910_0205_aiscc-p2-3-phase1b-terminal-state-actual-capture-entry-reconciliation-1.md

CYCLE:
20260910_0205_aiscc-p2-3-phase1b-b3-persisted-actual-capture-entry-1.cycle.md
SHA-256:
4144d85cd1d6f6955466fe780798858d108037a2c67bcfe5022105165c79123b
destination:
.aiassistant/records/aiscc/cycles/20260910_0205_aiscc-p2-3-phase1b-b3-persisted-actual-capture-entry-1.cycle.md

JUDGMENT:
20260910_0205_aiscc-p2-3-phase1b-b3-persistence-final-acceptance-judgment-1.md
SHA-256:
1c80ba350cf1440ea2c9b9be25c506b861f337806369c2be5bff00805579ad13
destination:
.aiassistant/reports/aiscc/20260910_0205_aiscc-p2-3-phase1b-b3-persistence-final-acceptance-judgment-1.md

HANDOFF:
none
```

Place TASK first at:

```text
.aiassistant/tasks/active/20260910_0205_aiscc-p2-3-phase1b-terminal-state-actual-capture-entry-reconciliation-1.md
```

Read it, then place/hash-verify current CYCLE/JUDGMENT.

Bootstrap failure before canonical TASK placement:

```text
STOP
no report/export
no substantive project mutation
```

After exact canonical transport, inbound ZIP/staging cleanup is best-effort and non-blocking.

# 1. repository gate

Require after current artifact placement:

```text
branch:
main

HEAD:
cf3d8c28efbc7c382f7253dde443b60419d9386b

HEAD tree:
a52c6ff488d457c228a2f51059c92007a8e9bea3

index:
empty
```

Expected Git-visible set excluding current active Task:

```text
.aiassistant/records/aiscc/cycles/20260910_0205_aiscc-p2-3-phase1b-b3-persisted-actual-capture-entry-1.cycle.md
.aiassistant/reports/aiscc/20260910_0205_aiscc-p2-3-phase1b-b3-persistence-final-acceptance-judgment-1.md
```

exact 2 paths.

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Do not cleanup, restore, stash, reset, overwrite or absorb.

# 2. exact predecessor provenance

Verify exact SHA-256:

- `.aiassistant/tasks/done/20260910_0102_aiscc-p2-3-phase1b-b3-final-acceptance-git-persistence-1.md`  `60ccd35df2839b7d4896c752bd0016449b3cd00151eb44783904dde72d3b42cd`
- `.aiassistant/records/aiscc/cycles/20260910_0102_aiscc-p2-3-phase1b-b3-accepted-persistence-entry-1.cycle.md`  `a57cda2d8e296bf53db5aad3e2ba1db0b6f1b68877c0b0515e7651d7b6c4c313`
- `.aiassistant/reports/aiscc/20260910_0102_aiscc-p2-3-phase1b-b3-final-acceptance-judgment-1.md`  `118ff53e3da4ce39d6ca78e3b17bb45b479c40f044474f6f1e5ea697e17957c6`

Any mismatch:

```text
PREDECESSOR_PROVENANCE_IDENTITY_MISMATCH
→ STOP
```

# 3. must-read authority

Read exactly:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/records/aiscc/cycles/20260910_0205_aiscc-p2-3-phase1b-b3-persisted-actual-capture-entry-1.cycle.md
.aiassistant/reports/aiscc/20260910_0205_aiscc-p2-3-phase1b-b3-persistence-final-acceptance-judgment-1.md

.aiassistant/tasks/done/20260910_0102_aiscc-p2-3-phase1b-b3-final-acceptance-git-persistence-1.md
.aiassistant/records/aiscc/cycles/20260910_0102_aiscc-p2-3-phase1b-b3-accepted-persistence-entry-1.cycle.md
.aiassistant/reports/aiscc/20260910_0102_aiscc-p2-3-phase1b-b3-final-acceptance-judgment-1.md
```

No timestamp substitution or similarly named inferred path.

If any listed path is absent:

```text
DOCUMENT_CONTRACT_MISMATCH
→ STOP
```

# 4. exact mutation scope

Only these existing tracked files may be edited:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

Plus current Task active→done lifecycle and current issued Cycle/Judgment.

Do not modify:

```text
src/**
config/**
tests/**
other governance files
```

# 5. CURRENT_STATE_SUMMARY update

Preserve dated historical records.

Update only current authority statements to truthfully state:

```text
P2:
IN_PROGRESS

P2-3 source/contract audit:
ACCEPTED_DESIGN / COMPLETE

P2-3 Phase 1A static scenario/resource contract:
ACCEPTED / CLOSED / PERSISTED

P2-3 Phase 1B source/integration-surface audit:
ACCEPTED_DESIGN / COMPLETE

P2-3 Phase 1B-B1 pinned resource materializer:
ACCEPTED / CLOSED / PERSISTED

B1 persistence commit:
ffbaa11986de54269cbac0f55e980440b639b5a6

P2-3 Phase 1B-B2 scenario/tool/provider/security enrollment:
ACCEPTED / CLOSED / PERSISTED

B2 persistence commit:
8abcfb7cd4dbf7c639e6883dce8be3b33c48b516

P2-3 Phase 1B-B3 driver/composition/bootstrap:
ACCEPTED / CLOSED / PERSISTED

B3 persistence commit:
cf3d8c28efbc7c382f7253dde443b60419d9386b

B3 candidate authorship:
UNKNOWN
correctness admitted by exact-byte Command Center QA

P2-3 Phase 1B:
ACCEPTED / CLOSED / PERSISTED

P2-3 actual scenario capture:
NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE

P2-3 Replay:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED

PUBLIC_RECORDED_REPLAY:
NOT_ADMITTED

public distribution/license:
HUMAN_PENDING
```

Replace current-looking stale assertions that still describe B3 as `NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE` or identify B3 implementation as the next subtask.

Do not erase historical occurrences.

The initial 0102 ZIP export failure is historical process provenance, not a current blocker. Do not label Phase 1B blocked because of it.

# 6. NEXT_ACTIONS update

Preserve roadmap/history.

Set the current queue/current next action to:

```text
P2-3 Phase 1B-B1:
ACCEPTED / CLOSED / PERSISTED

P2-3 Phase 1B-B2:
ACCEPTED / CLOSED / PERSISTED

P2-3 Phase 1B-B3:
ACCEPTED / CLOSED / PERSISTED

P2-3 Phase 1B:
ACCEPTED / CLOSED / PERSISTED

P2-3 actual scenario capture:
NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE

next subtask:
bounded OWNER_SELF_DOGFOOD actual-capture runtime entry

first-capture target:
four exact Stockroom v1 scenarios
LOCAL_DETERMINISTIC_PROVIDER
external_llm_executed=false

Replay:
NOT_STARTED

P2-4:
NOT_STARTED

P3:
NOT_STARTED
```

Also preserve:

```text
PUBLIC_BOUNDED_LIVE remains NOT_RELEASED.
PUBLIC_RECORDED_REPLAY remains NOT_ADMITTED.
public distribution/license remains HUMAN_PENDING.
Actual capture entry is owner-self-dogfood only.
No public runtime mode is authorized.
```

Do not mark actual scenario capture as executed or captured.

# 7. integrity

Require:

```text
UTF-8
balanced Markdown fences
no control-character corruption
git diff --check PASS
```

No unrelated wording churn.

# 8. pre-commit workspace

Before current Task lifecycle:

```text
current Cycle/Judgment:
2 exact

modified current-state docs:
2 exact

total:
4 exact Git-visible paths
```

Then move:

```text
.aiassistant/tasks/active/20260910_0205_aiscc-p2-3-phase1b-terminal-state-actual-capture-entry-reconciliation-1.md
→
.aiassistant/tasks/done/20260910_0205_aiscc-p2-3-phase1b-terminal-state-actual-capture-entry-reconciliation-1.md
```

Final commit candidate:

```text
5 exact paths
```

# 9. exact final commit allowlist

- `.aiassistant/records/aiscc/cycles/20260910_0205_aiscc-p2-3-phase1b-b3-persisted-actual-capture-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_0205_aiscc-p2-3-phase1b-b3-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
- `.aiassistant/tasks/done/20260910_0205_aiscc-p2-3-phase1b-terminal-state-actual-capture-entry-reconciliation-1.md`

No other path may be staged.

# 10. Git persistence

Only after all prior gates PASS:

```text
git add -- <5 exact literal paths>
git diff --cached --check
git diff --cached --name-status
git commit -m "docs(command-center): close P2-3 Phase 1B and enter capture"
```

Expected:

```text
parent:
cf3d8c28efbc7c382f7253dde443b60419d9386b

parent count:
1

message:
docs(command-center): close P2-3 Phase 1B and enter capture

changed paths:
5 exact
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

# 11. post-commit verification

Verify:

1. result commit/tree;
2. parent `cf3d8c28efbc7c382f7253dde443b60419d9386b` / parent count 1;
3. exact commit message;
4. changed paths exact 5;
5. CURRENT_STATE_SUMMARY shows Phase 1B and B3 closed/persisted;
6. CURRENT_STATE_SUMMARY shows actual capture as next, not executed;
7. NEXT_ACTIONS shows bounded OWNER_SELF_DOGFOOD actual-capture runtime entry as next;
8. no product/config/test mutation;
9. index empty;
10. Git-visible worktree clean;
11. push/network NOT_RUN.

# 12. export bundle + automatic ZIP

Bundle folder:

```text
.aiassistant/reports/target/20260910_0205_aiscc-p2-3-phase1b-terminal-state-actual-capture-entry-reconciliation-1/
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

Include byte-preserving committed copies of all 5 commit paths.

After bundle completion create:

```text
.aiassistant/reports/target/20260910_0205_aiscc-p2-3-phase1b-terminal-state-actual-capture-entry-reconciliation-1.zip
```

Use the runtime's supported Windows extended-length path handling from the outset if needed for this exact target path.

This is an export implementation detail only; it does not change repository paths.

Require:

```text
one top-level bundle directory
readable / CRC PASS
required root files present
exact committed-copy coverage
source/commit/export byte equality
folder/archive byte equality
```

Keep folder and ZIP.

If export nevertheless fails:

```text
ZIP_EXPORT_FAILED
→ STOP
```

Do not perform substantive repository work after that failure.

# 13. evidence contract

executor_required:

- inbound ZIP/artifact transport
- exact repository gate
- exact 0102 predecessor provenance identity
- state/next semantic reconciliation
- exact 5-path staging/commit
- post-commit clean verification
- outbound result ZIP

reuse_allowed:

- accepted 0102 B3 persistence evidence
- accepted 0100 B3 QA evidence
- persisted B1/B2

human_owned:

```text
new Human QA:
NOT_REQUIRED

B3 candidate authorship:
UNKNOWN

public distribution/license:
HUMAN_PENDING / outside Task
```

forbidden:

- actual capture/runtime execution
- scenario/provider/tool/Docker execution
- DB
- evidence/Human/Judgment runtime mutation
- Replay
- public admission
- Git network

# 14. mandatory stop

```text
DOWNLOAD_ZIP_MISSING
DOWNLOAD_ZIP_HASH_MISMATCH
DOWNLOAD_ZIP_CORRUPT
DOWNLOAD_TASK_MEMBER_MISSING
DOWNLOAD_TASK_PLACEMENT_FAILED
TRANSPORT_FAILURE
HEAD_OR_TREE_MISMATCH
INDEX_NOT_EMPTY
DIRTY_WORKSPACE_MIXED
PREDECESSOR_PROVENANCE_IDENTITY_MISMATCH
DOCUMENT_CONTRACT_MISMATCH
CANONICAL_AUTHORITY_CONFLICT
GIT_STAGE_ALLOWLIST_MISMATCH
GIT_COMMIT_VERIFICATION_FAILED
ZIP_EXPORT_FAILED
```

Inbound cleanup refusal after canonical transport is non-blocking.

# 15. final ceiling

Success:

```text
P2-3 Phase 1B:
ACCEPTED / CLOSED / PERSISTED

P2-3 actual scenario capture:
ENTRY_READY / NEXT_EXECUTABLE

next:
bounded OWNER_SELF_DOGFOOD actual-capture runtime entry

actual scenario execution:
NOT_STARTED

Replay:
NOT_STARTED
```

Do not start runtime/capture execution in this Task.
