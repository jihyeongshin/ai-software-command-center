# 작업지시서: P2-3 Phase 1A terminal state / Phase 1B entry reconciliation

## meta

- task_id: `20260909_1203_aiscc-p2-3-phase1a-terminal-state-phase1b-entry-reconciliation-1`
- created_at: `2026-09-09T12:03:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `COMMAND_CENTER_RECORD_UPDATE / GIT_PERSISTENCE`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `c9214ce21010978682a35ea6e55743610996097d`
- required_base_tree: `a9b2c9676e28b4ed38c0e25e1129cfe15b928029`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. inbound ZIP bootstrap

The Browser Short Prompt's exact delivery ZIP SHA-256 is the bootstrap integrity anchor.

Current delivery ZIP contains only:

```text
TASK:
20260909_1203_aiscc-p2-3-phase1a-terminal-state-phase1b-entry-reconciliation-1.md

CYCLE:
20260909_1203_aiscc-p2-3-phase1a-persisted-phase1b-entry-1.cycle.md
SHA-256:
f44dadb0a1e1c8bfc5914503a387431d1f946286b057c57449839436b274fc63
destination:
.aiassistant/records/aiscc/cycles/20260909_1203_aiscc-p2-3-phase1a-persisted-phase1b-entry-1.cycle.md

JUDGMENT:
20260909_1203_aiscc-p2-3-phase1a-persistence-final-acceptance-judgment-1.md
SHA-256:
4abf092931a29c9c817191405e8dae5835aeccb40738b5085ccb38956419e0a3
destination:
.aiassistant/reports/aiscc/20260909_1203_aiscc-p2-3-phase1a-persistence-final-acceptance-judgment-1.md

HANDOFF:
none
```

Place TASK first at:

```text
.aiassistant/tasks/active/20260909_1203_aiscc-p2-3-phase1a-terminal-state-phase1b-entry-reconciliation-1.md
```

Read it, then place/verify current CYCLE/JUDGMENT.

After exact canonical transport, inbound ZIP/staging cleanup is best-effort/non-blocking.

# 1. repository gate

Require after current artifact placement:

```text
branch:
main

HEAD:
c9214ce21010978682a35ea6e55743610996097d

HEAD tree:
a9b2c9676e28b4ed38c0e25e1129cfe15b928029

index:
empty
```

Expected Git-visible set excluding current active Task:

```text
.aiassistant/records/aiscc/cycles/20260909_1203_aiscc-p2-3-phase1a-persisted-phase1b-entry-1.cycle.md
.aiassistant/reports/aiscc/20260909_1203_aiscc-p2-3-phase1a-persistence-final-acceptance-judgment-1.md
```

exact 2 paths.

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

No cleanup/restore/stash/reset.

# 2. must-read authority

Read:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/records/aiscc/cycles/20260909_1203_aiscc-p2-3-phase1a-persisted-phase1b-entry-1.cycle.md
.aiassistant/reports/aiscc/20260909_1203_aiscc-p2-3-phase1a-persistence-final-acceptance-judgment-1.md

.aiassistant/records/aiscc/cycles/20260909_0115_aiscc-p2-3-phase1a-static-contract-accepted-persistence-entry-1.cycle.md
.aiassistant/reports/aiscc/20260909_0115_aiscc-p2-3-phase1a-static-contract-final-acceptance-judgment-1.md
.aiassistant/tasks/done/20260909_0115_aiscc-p2-3-phase1a-final-acceptance-git-persistence-1.md
```

No unrelated historical bulk-read.

# 3. exact mutation scope

Only these existing tracked files may be edited:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

Plus current Task active→done lifecycle and current issued Cycle/Judgment.

Do not modify:

```text
config/scenarios/**
src/aiscc/scenarios/**
tests/unit/scenarios/**
runtime/provider/tool/security/bootstrap
other governance files
```

# 4. CURRENT_STATE_SUMMARY update

Preserve historical sections.

Update only current authority statements so the document truthfully says:

```text
P2:
IN_PROGRESS

P2-2:
ACCEPTED / CLOSED / PERSISTED

P2-3 source/contract audit:
ACCEPTED_DESIGN / COMPLETE

P2-3 Phase 1A static scenario/resource contract:
ACCEPTED / CLOSED / PERSISTED

Phase 1A persistence commit:
c9214ce21010978682a35ea6e55743610996097d

P2-3 Phase 1B synthetic repository materialization + bounded runtime enrollment:
NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE

P2-3 actual scenario capture:
NOT_STARTED

P2-3 Replay:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED

PUBLIC_RECORDED_REPLAY:
NOT_ADMITTED

public distribution/license:
HUMAN_PENDING
```

Replace explicitly-current stale assertions such as:

```text
P2-3 NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE
first subtask = retry source/contract audit
1700 audit as current blocker
P2-3 implementation has not started
```

with the new current state.

Do not erase dated historical records of those earlier states.

# 5. NEXT_ACTIONS update

Preserve the stable roadmap and completed historical sections.

Update current queue/current release status/current next action so:

```text
P2-3 source/contract audit:
ACCEPTED_DESIGN / COMPLETE

P2-3 Phase 1A:
ACCEPTED / CLOSED / PERSISTED

P2-3 Phase 1B:
NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE

next subtask:
bounded Phase 1B source/integration-surface audit before runtime mutation

P2-3 actual scenario capture:
NOT_STARTED

P2-3 Replay:
NOT_STARTED

P2-4:
NOT_STARTED

P3:
NOT_STARTED
```

The next Task after this reconciliation is NOT direct runtime implementation yet.

Reason:

```text
Phase 1B requires exact current source integration boundaries for:
- synthetic repository materialization
- scenario enrollment/driver
- Stockroom bounded tool enrollment
- provider/profile/security/bootstrap composition

These exact current interfaces must be audited before mutation allowlists are issued.
```

# 6. integrity

Require:

```text
UTF-8
balanced Markdown fences
no control-character corruption
git diff --check PASS
```

No unrelated wording churn.

# 7. pre-commit workspace

Before Task lifecycle:

```text
current Cycle/Judgment:
2

modified current-state docs:
2

total:
4 exact Git-visible paths
```

Then move:

```text
.aiassistant/tasks/active/20260909_1203_aiscc-p2-3-phase1a-terminal-state-phase1b-entry-reconciliation-1.md
→
.aiassistant/tasks/done/20260909_1203_aiscc-p2-3-phase1a-terminal-state-phase1b-entry-reconciliation-1.md
```

Final commit candidate:

```text
5 exact paths
```

# 8. exact final commit allowlist

- `.aiassistant/records/aiscc/cycles/20260909_1203_aiscc-p2-3-phase1a-persisted-phase1b-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_1203_aiscc-p2-3-phase1a-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
- `.aiassistant/tasks/done/20260909_1203_aiscc-p2-3-phase1a-terminal-state-phase1b-entry-reconciliation-1.md`

No other path may be staged.

# 9. Git persistence

Only after prior gates PASS:

```text
git add -- <5 exact literal paths>
git diff --cached --check
git diff --cached --name-status
git commit -m "docs(command-center): advance P2-3 to Phase 1B"
```

Expected:

```text
parent:
c9214ce21010978682a35ea6e55743610996097d

parent count:
1

message:
docs(command-center): advance P2-3 to Phase 1B

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

# 10. post-commit verification

Verify:

1. result commit/tree
2. parent `c9214ce21010978682a35ea6e55743610996097d` / parent count 1
3. exact message
4. changed paths exact 5
5. CURRENT_STATE_SUMMARY shows Phase 1A persisted and Phase 1B next
6. NEXT_ACTIONS shows bounded Phase 1B source/integration audit as next subtask
7. no product/config/test mutation
8. index empty
9. Git-visible worktree clean
10. push/network NOT_RUN

# 11. export bundle + automatic ZIP

Bundle folder:

```text
.aiassistant/reports/target/20260909_1203_aiscc-p2-3-phase1a-terminal-state-phase1b-entry-reconciliation-1/
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

After folder completion create:

```text
.aiassistant/reports/target/20260909_1203_aiscc-p2-3-phase1a-terminal-state-phase1b-entry-reconciliation-1.zip
```

Validate readability/CRC, one top-level bundle directory, required roots, exact committed-copy coverage and byte equality.

# 12. evidence contract

executor_required:

- inbound ZIP/artifact transport
- repository preflight
- current-state semantic reconciliation
- exact 5-path staging/commit
- post-commit clean verification
- outbound bundle ZIP

reuse_allowed:

- 0115 Phase 1A persistence evidence

human_owned:

```text
new Human QA:
NOT_REQUIRED
```

forbidden:

- Phase 1B source/runtime mutation
- scenario execution
- provider/tool/DB/Replay
- public admission
- Git network

# 13. mandatory stop

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
CANONICAL_AUTHORITY_CONFLICT
DOCUMENT_CONTRACT_MISMATCH
GIT_STAGE_ALLOWLIST_MISMATCH
GIT_COMMIT_VERIFICATION_FAILED
ZIP_EXPORT_FAILED
```

Inbound cleanup refusal after canonical transport is non-blocking.

# 14. final ceiling

Success:

```text
P2-3 Phase 1A:
ACCEPTED / CLOSED / PERSISTED

P2-3 Phase 1B:
ENTRY_READY / NEXT_EXECUTABLE

next:
Phase 1B bounded source/integration-surface audit

Phase 1B implementation:
NOT_STARTED
```

Do not start Phase 1B implementation in this Task.
