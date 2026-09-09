# 작업지시서: P2-3 Phase 1B-B2 terminal state / B3 entry reconciliation

## meta

- task_id: `20260909_2018_aiscc-p2-3-phase1b-b2-terminal-state-b3-entry-reconciliation-1`
- created_at: `2026-09-09T20:18:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `COMMAND_CENTER_RECORD_UPDATE / GIT_PERSISTENCE`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `8abcfb7cd4dbf7c639e6883dce8be3b33c48b516`
- required_base_tree: `d1b912efbac31540745c119f250e21e5ecfaa28c`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. inbound ZIP bootstrap

The Browser Short Prompt's exact delivery ZIP SHA-256 is the bootstrap integrity anchor.

Current delivery ZIP contains only:

```text
TASK:
20260909_2018_aiscc-p2-3-phase1b-b2-terminal-state-b3-entry-reconciliation-1.md

CYCLE:
20260909_2018_aiscc-p2-3-b2-persisted-b3-entry-1.cycle.md
SHA-256:
cc523c0971d8471af0bab65eee65be5cacc5f5661f46e74672eb5142030c51ee
destination:
.aiassistant/records/aiscc/cycles/20260909_2018_aiscc-p2-3-b2-persisted-b3-entry-1.cycle.md

JUDGMENT:
20260909_2018_aiscc-p2-3-b2-persistence-final-acceptance-judgment-1.md
SHA-256:
224434fb8c4deccdf456e63a91b87aca930648c4480d3ad98e187c42228e2a92
destination:
.aiassistant/reports/aiscc/20260909_2018_aiscc-p2-3-b2-persistence-final-acceptance-judgment-1.md

HANDOFF:
none
```

Place TASK first at:

```text
.aiassistant/tasks/active/20260909_2018_aiscc-p2-3-phase1b-b2-terminal-state-b3-entry-reconciliation-1.md
```

Read it, then place/hash-verify current CYCLE/JUDGMENT.

Bootstrap failures follow the persisted ZIP-direct workflow.

After exact canonical transport, inbound ZIP/staging cleanup is best-effort and non-blocking.

# 1. repository gate

Require after current artifact placement:

```text
branch:
main

HEAD:
8abcfb7cd4dbf7c639e6883dce8be3b33c48b516

HEAD tree:
d1b912efbac31540745c119f250e21e5ecfaa28c

index:
empty
```

Expected Git-visible set excluding current active Task:

```text
.aiassistant/records/aiscc/cycles/20260909_2018_aiscc-p2-3-b2-persisted-b3-entry-1.cycle.md
.aiassistant/reports/aiscc/20260909_2018_aiscc-p2-3-b2-persistence-final-acceptance-judgment-1.md
```

exact 2 paths.

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Do not cleanup/restore/stash/reset/absorb.

# 2. exact predecessor identity

Verify exact SHA-256:

- `.aiassistant/tasks/done/20260909_1805_aiscc-p2-3-phase1b-b2-final-acceptance-git-persistence-1.md`  `c68e27a0b6baba721dfb4d752aeb8335727e73a5899cad8c2b38bab7a444b3ed`
- `.aiassistant/records/aiscc/cycles/20260909_1805_aiscc-p2-3-phase1b-b2-accepted-persistence-entry-1.cycle.md`  `03ee3f7d790a77a55f1a3354963c6a6e9458a183f5bac0aebba6084a3e52cfab`
- `.aiassistant/reports/aiscc/20260909_1805_aiscc-p2-3-phase1b-b2-final-acceptance-judgment-1.md`  `7de14abcfcfba33c5cd13a18ded9214f9b9c270e405ca106037e71861409e5c4`

Any mismatch:

```text
PREDECESSOR_PROVENANCE_IDENTITY_MISMATCH
→ STOP
```

# 3. must-read authority

Read only these exact canonical paths:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/records/aiscc/cycles/20260909_2018_aiscc-p2-3-b2-persisted-b3-entry-1.cycle.md
.aiassistant/reports/aiscc/20260909_2018_aiscc-p2-3-b2-persistence-final-acceptance-judgment-1.md

.aiassistant/tasks/done/20260909_1805_aiscc-p2-3-phase1b-b2-final-acceptance-git-persistence-1.md
.aiassistant/records/aiscc/cycles/20260909_1805_aiscc-p2-3-phase1b-b2-accepted-persistence-entry-1.cycle.md
.aiassistant/reports/aiscc/20260909_1805_aiscc-p2-3-phase1b-b2-final-acceptance-judgment-1.md

.aiassistant/tasks/done/20260909_1635_aiscc-p2-3-phase1b-b1-terminal-state-b2-entry-reconciliation-retry-1.md
.aiassistant/records/aiscc/cycles/20260909_1635_aiscc-p2-3-b1-state-reconciliation-contract-defect-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260909_1635_aiscc-p2-3-b1-state-reconciliation-command-center-task-defect-judgment-1.md
```

No timestamp substitution and no similarly named inferred path.

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

Preserve historical dated records.

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
ACCEPTED / CLOSED / PERSISTED

B2 persistence commit:
8abcfb7cd4dbf7c639e6883dce8be3b33c48b516

P2-3 Phase 1B-B3 driver/composition/bootstrap:
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
B2:
NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE

next:
bounded B2 implementation

B2 implementation:
not started
```

with the new current authority.

Do not erase their historical occurrence.

# 6. NEXT_ACTIONS update

Preserve roadmap/history.

Set current queue/current next action to:

```text
P2-3 Phase 1B-B1:
ACCEPTED / CLOSED / PERSISTED

P2-3 Phase 1B-B2:
ACCEPTED / CLOSED / PERSISTED

P2-3 Phase 1B-B3:
NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE

next subtask:
bounded B3 driver/composition/bootstrap implementation
under the accepted Phase 1B integration design

B3 scope:
scenario runtime driver
+ composition owner
+ bootstrap binding
+ no-side-effect integration verification

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
B3 remains OWNER_SELF_DOGFOOD-only composition.
PUBLIC_BOUNDED_LIVE remains NOT_RELEASED.
external_llm_executed=false remains the accepted first-capture target.
Actual scenario execution is not authorized by B3 entry labeling alone.
```

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
.aiassistant/tasks/active/20260909_2018_aiscc-p2-3-phase1b-b2-terminal-state-b3-entry-reconciliation-1.md
→
.aiassistant/tasks/done/20260909_2018_aiscc-p2-3-phase1b-b2-terminal-state-b3-entry-reconciliation-1.md
```

Final commit candidate:

```text
5 exact paths
```

# 9. exact final commit allowlist

- `.aiassistant/records/aiscc/cycles/20260909_2018_aiscc-p2-3-b2-persisted-b3-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_2018_aiscc-p2-3-b2-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
- `.aiassistant/tasks/done/20260909_2018_aiscc-p2-3-phase1b-b2-terminal-state-b3-entry-reconciliation-1.md`

No other path may be staged.

# 10. Git persistence

Only after prior gates PASS:

```text
git add -- <5 exact literal paths>
git diff --cached --check
git diff --cached --name-status
git commit -m "docs(command-center): advance P2-3 Phase 1B to B3"
```

Expected:

```text
parent:
8abcfb7cd4dbf7c639e6883dce8be3b33c48b516

parent count:
1

message:
docs(command-center): advance P2-3 Phase 1B to B3

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
2. parent `8abcfb7cd4dbf7c639e6883dce8be3b33c48b516` / parent count 1;
3. exact commit message;
4. changed paths exact 5;
5. CURRENT_STATE_SUMMARY shows B2 persisted and B3 next;
6. NEXT_ACTIONS shows bounded B3 implementation as next;
7. no product/config/test mutation;
8. index empty;
9. Git-visible worktree clean;
10. push/network NOT_RUN.

# 12. export bundle + automatic ZIP

Bundle folder:

```text
.aiassistant/reports/target/20260909_2018_aiscc-p2-3-phase1b-b2-terminal-state-b3-entry-reconciliation-1/
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
.aiassistant/reports/target/20260909_2018_aiscc-p2-3-phase1b-b2-terminal-state-b3-entry-reconciliation-1.zip
```

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

# 13. evidence contract

executor_required:

- inbound ZIP/artifact transport
- exact repository gate
- exact 1805 provenance identity
- current-state semantic reconciliation
- exact 5-path staging/commit
- post-commit clean verification
- outbound result ZIP

reuse_allowed:

- 1805 B2 persistence evidence
- 1800 accepted B2 test evidence
- accepted Phase 1B design for next-action labeling

human_owned:

```text
new Human QA:
NOT_REQUIRED

public license:
HUMAN_PENDING / outside Task
```

forbidden:

- B3 source/bootstrap/test mutation
- actual provider/tool/Docker/scenario execution
- DB
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
P2-3 Phase 1B-B2:
ACCEPTED / CLOSED / PERSISTED

P2-3 Phase 1B-B3:
ENTRY_READY / NEXT_EXECUTABLE

next:
bounded B3 implementation

B3 implementation:
NOT_STARTED
```

Do not start B3 implementation in this Task.
