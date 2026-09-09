# 작업지시서: P2-3 Phase 1B-B1 terminal state / B2 entry reconciliation

## meta

- task_id: `20260909_1537_aiscc-p2-3-phase1b-b1-terminal-state-b2-entry-reconciliation-1`
- created_at: `2026-09-09T15:37:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `COMMAND_CENTER_RECORD_UPDATE / GIT_PERSISTENCE`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `ffbaa11986de54269cbac0f55e980440b639b5a6`
- required_base_tree: `8fb137ce508973d1327b359467b3b5f170ee9d59`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. inbound ZIP bootstrap

The Browser Short Prompt's exact delivery ZIP SHA-256 is the bootstrap integrity anchor.

Current delivery ZIP contains only:

```text
TASK:
20260909_1537_aiscc-p2-3-phase1b-b1-terminal-state-b2-entry-reconciliation-1.md

CYCLE:
20260909_1537_aiscc-p2-3-b1-persisted-b2-entry-1.cycle.md
SHA-256:
e5b918abd9062d282eaac71ae64ccd0ab1f45b5c6907573a5bd61d82e934b744
destination:
.aiassistant/records/aiscc/cycles/20260909_1537_aiscc-p2-3-b1-persisted-b2-entry-1.cycle.md

JUDGMENT:
20260909_1537_aiscc-p2-3-b1-persistence-final-acceptance-judgment-1.md
SHA-256:
44e6a83d65bab0fa23c4521fe8535dab7fe968e65efb83c4c7ddd03d7c702e82
destination:
.aiassistant/reports/aiscc/20260909_1537_aiscc-p2-3-b1-persistence-final-acceptance-judgment-1.md

HANDOFF:
none
```

Place TASK first at:

```text
.aiassistant/tasks/active/20260909_1537_aiscc-p2-3-phase1b-b1-terminal-state-b2-entry-reconciliation-1.md
```

Read it, then place and hash-verify current CYCLE/JUDGMENT.

Bootstrap failures follow the persisted ZIP-direct workflow.

After exact canonical transport, inbound ZIP/staging cleanup is best-effort and non-blocking.

# 1. repository gate

Require after current artifact placement:

```text
branch:
main

HEAD:
ffbaa11986de54269cbac0f55e980440b639b5a6

HEAD tree:
8fb137ce508973d1327b359467b3b5f170ee9d59

index:
empty
```

Expected Git-visible set excluding current active Task:

```text
.aiassistant/records/aiscc/cycles/20260909_1537_aiscc-p2-3-b1-persisted-b2-entry-1.cycle.md
.aiassistant/reports/aiscc/20260909_1537_aiscc-p2-3-b1-persistence-final-acceptance-judgment-1.md
```

exact 2 paths.

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Do not cleanup/restore/stash/reset/absorb.

# 2. must-read authority

Read:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/records/aiscc/cycles/20260909_1537_aiscc-p2-3-b1-persisted-b2-entry-1.cycle.md
.aiassistant/reports/aiscc/20260909_1537_aiscc-p2-3-b1-persistence-final-acceptance-judgment-1.md

.aiassistant/records/aiscc/cycles/20260909_1435_aiscc-p2-3-phase1b-b1-accepted-persistence-entry-1.cycle.md
.aiassistant/reports/aiscc/20260909_1435_aiscc-p2-3-phase1b-b1-final-acceptance-judgment-1.md
.aiassistant/tasks/done/20260909_1435_aiscc-p2-3-phase1b-b1-final-acceptance-git-persistence-1.md

.aiassistant/records/aiscc/cycles/20260909_1300_aiscc-p2-3-phase1a-terminal-accepted-phase1b-audit-entry-1.cycle.md
.aiassistant/reports/aiscc/20260909_1300_aiscc-p2-3-phase1b-runtime-integration-audit-final-acceptance-judgment-1.md
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
src/aiscc/runtime/stockroom_*
src/aiscc/scenarios/**
src/aiscc/providers/**
src/aiscc/security/**
src/aiscc/bootstrap.py
config/**
tests/**
other governance files
```

# 4. CURRENT_STATE_SUMMARY update

Preserve dated historical records.

Update only current authority statements so the document truthfully says:

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
NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE

P2-3 Phase 1B-B3 driver/composition/bootstrap:
NOT_STARTED

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
Phase 1B whole phase:
NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE

next:
Phase 1B source/integration-surface audit

B1:
not yet implemented/persisted
```

with the new current state.

Do not erase historical references to earlier states.

# 5. NEXT_ACTIONS update

Preserve stable roadmap and completed history.

Update current queue/current next action so:

```text
P2-3 Phase 1B-B1:
ACCEPTED / CLOSED / PERSISTED

P2-3 Phase 1B-B2:
NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE

next subtask:
bounded B2 implementation under the already accepted 1300 integration design

B2 scope:
scenario enrollment
+ bounded Stockroom tool
+ LOCAL_DETERMINISTIC_PROVIDER
+ security profile/policy binding

B3:
NOT_STARTED

actual scenario capture:
NOT_STARTED

Replay:
NOT_STARTED

P2-4:
NOT_STARTED

P3:
NOT_STARTED
```

Also state:

```text
B2 remains OWNER_SELF_DOGFOOD only.
PUBLIC_BOUNDED_LIVE remains NOT_RELEASED.
external_llm_executed remains false for the accepted first-capture target.
```

Do not turn B2 readiness into runtime execution authorization.

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

Before current Task lifecycle:

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
.aiassistant/tasks/active/20260909_1537_aiscc-p2-3-phase1b-b1-terminal-state-b2-entry-reconciliation-1.md
→
.aiassistant/tasks/done/20260909_1537_aiscc-p2-3-phase1b-b1-terminal-state-b2-entry-reconciliation-1.md
```

Final commit candidate:

```text
5 exact paths
```

# 8. exact final commit allowlist

- `.aiassistant/records/aiscc/cycles/20260909_1537_aiscc-p2-3-b1-persisted-b2-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_1537_aiscc-p2-3-b1-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
- `.aiassistant/tasks/done/20260909_1537_aiscc-p2-3-phase1b-b1-terminal-state-b2-entry-reconciliation-1.md`

No other path may be staged.

# 9. Git persistence

Only after prior gates PASS:

```text
git add -- <5 exact literal paths>
git diff --cached --check
git diff --cached --name-status
git commit -m "docs(command-center): advance P2-3 Phase 1B to B2"
```

Expected:

```text
parent:
ffbaa11986de54269cbac0f55e980440b639b5a6

parent count:
1

message:
docs(command-center): advance P2-3 Phase 1B to B2

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

1. result commit/tree;
2. parent `ffbaa11986de54269cbac0f55e980440b639b5a6` / parent count 1;
3. exact commit message;
4. changed paths exact 5;
5. CURRENT_STATE_SUMMARY shows B1 persisted and B2 next;
6. NEXT_ACTIONS shows bounded B2 implementation as next subtask;
7. no product/config/test mutation;
8. index empty;
9. Git-visible worktree clean;
10. push/network NOT_RUN.

# 11. export bundle + automatic ZIP

Bundle folder:

```text
.aiassistant/reports/target/20260909_1537_aiscc-p2-3-phase1b-b1-terminal-state-b2-entry-reconciliation-1/
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
.aiassistant/reports/target/20260909_1537_aiscc-p2-3-phase1b-b1-terminal-state-b2-entry-reconciliation-1.zip
```

Validate:

```text
one top-level bundle directory
readable / CRC PASS
required root files present
exact committed-copy coverage
source/commit/export byte equality
folder/archive byte equality
```

Keep folder and ZIP.

# 12. evidence contract

executor_required:

- inbound ZIP/artifact transport
- repository preflight
- current-state semantic reconciliation
- exact 5-path staging/commit
- post-commit clean verification
- outbound result ZIP

reuse_allowed:

- 1435 B1 persistence evidence
- accepted 1300 Phase 1B design for next-action labeling only

human_owned:

```text
new Human QA:
NOT_REQUIRED

public license:
HUMAN_PENDING / outside Task
```

forbidden:

- B2 source/config/security/provider mutation
- B3
- scenario/provider/tool execution
- DB
- Replay
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
P2-3 Phase 1B-B1:
ACCEPTED / CLOSED / PERSISTED

P2-3 Phase 1B-B2:
ENTRY_READY / NEXT_EXECUTABLE

next:
bounded B2 implementation

B2 implementation:
NOT_STARTED
```

Do not start B2 implementation in this Task.
