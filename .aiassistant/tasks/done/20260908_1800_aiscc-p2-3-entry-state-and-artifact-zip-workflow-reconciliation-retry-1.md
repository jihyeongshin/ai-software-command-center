# 작업지시서: P2-3 entry state and artifact-ZIP workflow reconciliation retry

## meta

- task_id: `20260908_1800_aiscc-p2-3-entry-state-and-artifact-zip-workflow-reconciliation-retry-1`
- created_at: `2026-09-08T18:00:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `COMMAND_CENTER_RECORD_UPDATE / WORKFLOW_RULE_UPDATE / GIT_PERSISTENCE`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `05185c57a6265a4002050ce25cdfde3dc87e9779`
- required_base_tree: `df997ec70594d0d451c7d281c975c6cbdb63e453`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. bootstrap status

This Task has already been extracted from a Command Center delivery ZIP whose SHA-256
was verified from the Browser Short Prompt before this file was trusted.

The verified ZIP hash is this Task's bootstrap integrity anchor.

Do not require a SHA-256 value embedded inside this Task for this Task's own bytes.

# 1. issued artifact manifest after TASK bootstrap

The current delivery archive contains six Markdown artifacts:

## predecessor blocked 1741 provenance

```text
TASK:
20260908_1741_aiscc-p2-3-entry-state-and-command-center-export-workflow-reconciliation-1.md
SHA-256:
908b55341b4b87b2f0e4eb85dca9da91e140c4ca8c2a38d173755944ea7b077b
destination:
.aiassistant/tasks/done/20260908_1741_aiscc-p2-3-entry-state-and-command-center-export-workflow-reconciliation-1.md

CYCLE:
20260908_1741_aiscc-p2-3-audit-blocked-stale-current-state-reconciliation-entry-1.cycle.md
SHA-256:
bc2479b77d7c9fd2a6406ad8b21f6a857cdb5c84296a598a6f6aea87c62be72e
destination:
.aiassistant/records/aiscc/cycles/20260908_1741_aiscc-p2-3-audit-blocked-stale-current-state-reconciliation-entry-1.cycle.md

JUDGMENT:
20260908_1741_aiscc-p2-3-audit-stale-current-state-authority-conflict-judgment-1.md
SHA-256:
a9f264d260c52bb1dd9e79e91f49e26b7fb8eda9a79d067c644e45d18e99f63b
destination:
.aiassistant/reports/aiscc/20260908_1741_aiscc-p2-3-audit-stale-current-state-authority-conflict-judgment-1.md
```

## current retry

```text
TASK:
20260908_1800_aiscc-p2-3-entry-state-and-artifact-zip-workflow-reconciliation-retry-1.md
integrity:
verified delivery ZIP bootstrap anchor
destination:
.aiassistant/tasks/active/20260908_1800_aiscc-p2-3-entry-state-and-artifact-zip-workflow-reconciliation-retry-1.md

CYCLE:
20260908_1800_aiscc-p2-3-reconciliation-blocked-bootstrap-hash-contract-retry-entry-1.cycle.md
SHA-256:
b82ed4d3b1fcf45896fb0ec4fea856e18839e5b6ac26597cd086357914328902

destination:
.aiassistant/records/aiscc/cycles/20260908_1800_aiscc-p2-3-reconciliation-blocked-bootstrap-hash-contract-retry-entry-1.cycle.md

JUDGMENT:
20260908_1800_aiscc-p2-3-reconciliation-bootstrap-hash-contract-ambiguity-judgment-1.md
SHA-256:
8ae60b61e9798bde27811d1e378946d46c2d519393257b60c3434729da6c6854

destination:
.aiassistant/reports/aiscc/20260908_1800_aiscc-p2-3-reconciliation-bootstrap-hash-contract-ambiguity-judgment-1.md

HANDOFF:
none
```

The current TASK has already been placed first and read.

Now place/verify the other five artifacts.

# 2. remaining artifact transport

For each remaining artifact:

```text
extracted source exists
→ exact expected SHA-256
→ destination state/hash
→ exact copy or hash-aware overwrite
→ destination SHA-256 equality
→ remove only that verified extracted source
```

Rules:

- no multi-file loop
- no wildcard/recursive copy/delete
- no combined hash+copy+delete process command
- do not overwrite a differing existing `tasks/done` predecessor Task
- any policy/tool/hash/path ambiguity: STOP

After all remaining artifacts PASS, remove the temporary extraction directory if empty.

Do NOT remove the inbound Command Center ZIP yet.
Keep it until terminal Task completion.

# 3. repository gate

Require:

```text
branch:
main

HEAD:
05185c57a6265a4002050ce25cdfde3dc87e9779

HEAD tree:
df997ec70594d0d451c7d281c975c6cbdb63e453

index:
empty
```

Expected Git-visible set is exact eight paths:

- `.aiassistant/tasks/done/20260908_1700_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_1700_aiscc-p2-2-terminal-closure-p2-3-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1700_aiscc-p2-2-terminal-closure-judgment-1.md`
- `.aiassistant/tasks/done/20260908_1741_aiscc-p2-3-entry-state-and-command-center-export-workflow-reconciliation-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_1741_aiscc-p2-3-audit-blocked-stale-current-state-reconciliation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1741_aiscc-p2-3-audit-stale-current-state-authority-conflict-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_1800_aiscc-p2-3-reconciliation-blocked-bootstrap-hash-contract-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1800_aiscc-p2-3-reconciliation-bootstrap-hash-contract-ambiguity-judgment-1.md`

Current active Task is ignored.

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

# 4. must-read canonical files

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md

.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md
.aiassistant/records/command-center/TASK_FILE_TEMPLATE.md
.aiassistant/records/command-center/SHORT_EXECUTOR_PROMPT_TEMPLATE.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/records/aiscc/cycles/20260908_1700_aiscc-p2-2-terminal-closure-p2-3-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_1700_aiscc-p2-2-terminal-closure-judgment-1.md

.aiassistant/records/aiscc/cycles/20260908_1741_aiscc-p2-3-audit-blocked-stale-current-state-reconciliation-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_1741_aiscc-p2-3-audit-stale-current-state-authority-conflict-judgment-1.md

.aiassistant/records/aiscc/cycles/20260908_1800_aiscc-p2-3-reconciliation-blocked-bootstrap-hash-contract-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_1800_aiscc-p2-3-reconciliation-bootstrap-hash-contract-ambiguity-judgment-1.md
```

# 5. allowed existing canonical modifications

Only:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
- `.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md`
- `.aiassistant/records/command-center/TASK_FILE_TEMPLATE.md`
- `.aiassistant/records/command-center/SHORT_EXECUTOR_PROMPT_TEMPLATE.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`

plus current Task lifecycle and already issued provenance.

No product/runtime/test/demo source mutation.

# 6. state authority reconciliation

`CURRENT_STATE_SUMMARY.md` and `NEXT_ACTIONS.md` must reflect current truth:

```text
P2-1:
ACCEPTED / CLOSED / PERSISTED

P2-2:
ACCEPTED / CLOSED / PERSISTED

P2-2 canonical commit:
05185c57a6265a4002050ce25cdfde3dc87e9779

P2-3:
NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE

1700 P2-3 source/contract audit:
BLOCKED / CANONICAL_AUTHORITY_CONFLICT / RETRY_REQUIRED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED

PUBLIC_RECORDED_REPLAY:
NOT_ADMITTED
```

Explicitly current stale assertions that P2-2 is still NOT_STARTED/current executable
must be replaced.

Historical dated provenance is not rewritten merely for containing an older state.

# 7. Command Center inbound artifact workflow

Canonicalize in:

```text
COMMAND_CENTER_WORKFLOW.md
TASK_FILE_TEMPLATE.md
SHORT_EXECUTOR_PROMPT_TEMPLATE.md
```

## Human responsibility

```text
1. download exactly one Command Center delivery ZIP into:
   C:\Users\oracl\Downloads
2. if fresh IDE chat is required, Human opens it
3. send the Short Prompt

Human does not manually extract or place Markdown artifacts.
```

## Short Prompt responsibility

Keep it intentionally short.

Default Short Prompt contains only enough information to bootstrap safely:

```text
- Downloads root
- exact delivery ZIP filename
- exact expected delivery ZIP SHA-256
- exact TASK member filename
- pre-project STOP rule
- instruction to verify ZIP, extract it, place TASK first, then read TASK
```

Do not duplicate Task details such as per-file hashes, canonical paths, workspace inventories,
implementation contract, evidence contract or Git allowlist.

## bootstrap extraction

Executor:

```text
1. verify exact inbound ZIP exists
2. verify ZIP SHA-256 from Short Prompt
3. verify archive readability/integrity
4. extract only that ZIP into a task-owned temporary directory under Downloads
5. verify exact TASK member exists
6. place TASK first at exact canonical tasks/active path
7. read TASK
8. Task governs remaining artifact placement and substantive execution
```

## pre-project failure semantics

Before canonical TASK placement, any:

```text
ZIP missing
ZIP hash mismatch
archive corrupt/unreadable
archive extraction tool/policy failure
TASK member missing
TASK canonical placement failure
```

causes:

```text
STOP
no project mutation beyond an attempted TASK placement
no report/export
no substitute file/path search
retain inbound ZIP if present
tell Human to re-download/reposition ZIP
```

## integrity model

```text
Browser Short Prompt ZIP hash
=
bootstrap integrity anchor for TASK and archive membership

Task per-file hashes
=
remaining CYCLE/JUDGMENT/HANDOFF and predecessor artifact transport integrity
```

Do not require a Task to contain its own exact whole-file SHA.

## cleanup

After all issued archive members have reached exact canonical destinations:

```text
remove task-owned temporary extraction directory when empty
```

At terminal Task completion, success or a repository-level blocker after successful bootstrap:

```text
remove exact inbound Command Center delivery ZIP from Downloads
```

Exception:

```text
pre-project/bootstrap failure
→ retain ZIP for Human correction/retry
```

# 8. Executor outbound result ZIP

Update `IDE_EXECUTOR_REPORT_EXPORT.md` and relevant workflow/template cross-reference.

After completed bundle folder:

```text
.aiassistant/reports/target/<bundle-name>/
```

Executor automatically creates:

```text
.aiassistant/reports/target/<bundle-name>.zip
```

Requirements:

```text
one top-level <bundle-name>/ directory
complete bundle contents
relative layout preserved
readable ZIP / CRC-integrity PASS
required root files present
no unrelated bundle files
original bundle folder retained
```

Final response must report both folder and ZIP paths.

ZIP generation failure:

```text
keep completed folder
report exact ZIP_EXPORT_FAILED blocker
do not claim ZIP success
```

# 9. task templates and Short Prompt size

`SHORT_EXECUTOR_PROMPT_TEMPLATE.md` should include a compact default roughly equivalent to:

```text
이번 Command Center artifact transport부터 수행하라.

Downloads:
C:\Users\oracl\Downloads

ZIP:
<delivery.zip>

SHA-256:
<zip hash>

ZIP이 없거나 hash/압축해제/TASK bootstrap이 실패하면 프로젝트 작업과 report/export 없이 STOP하고 Human에게 재다운로드/재배치를 요청하라.

정상이면 ZIP을 직접 압축해제하고 아래 TASK를 tasks/active에 먼저 배치해 읽은 뒤 Task 지시를 수행하라.

<TASK filename>
```

The Short Prompt should normally remain tens of lines or less, not hundreds.

# 10. document integrity

Require:

- UTF-8
- no control-character corruption
- balanced Markdown fences
- `git diff --check` PASS
- Korean-first where existing document policy requires it

# 11. pre-commit workspace

Before current Task lifecycle move:

```text
8 issued/pending provenance
+
6 modified canonical docs
=
14 exact Git-visible paths
```

Then move current Task:

```text
.aiassistant/tasks/active/20260908_1800_aiscc-p2-3-entry-state-and-artifact-zip-workflow-reconciliation-retry-1.md
→
.aiassistant/tasks/done/20260908_1800_aiscc-p2-3-entry-state-and-artifact-zip-workflow-reconciliation-retry-1.md
```

Final commit candidate:

```text
15 exact paths
```

# 12. exact commit allowlist

- `.aiassistant/tasks/done/20260908_1700_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_1700_aiscc-p2-2-terminal-closure-p2-3-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1700_aiscc-p2-2-terminal-closure-judgment-1.md`
- `.aiassistant/tasks/done/20260908_1741_aiscc-p2-3-entry-state-and-command-center-export-workflow-reconciliation-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_1741_aiscc-p2-3-audit-blocked-stale-current-state-reconciliation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1741_aiscc-p2-3-audit-stale-current-state-authority-conflict-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_1800_aiscc-p2-3-reconciliation-blocked-bootstrap-hash-contract-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1800_aiscc-p2-3-reconciliation-bootstrap-hash-contract-ambiguity-judgment-1.md`
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
- `.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md`
- `.aiassistant/records/command-center/TASK_FILE_TEMPLATE.md`
- `.aiassistant/records/command-center/SHORT_EXECUTOR_PROMPT_TEMPLATE.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/tasks/done/20260908_1800_aiscc-p2-3-entry-state-and-artifact-zip-workflow-reconciliation-retry-1.md`

# 13. Git persistence

Only after all prior gates PASS:

```text
git add -- <exact 15 literal paths>
git diff --cached --check
git diff --cached --name-status
git commit -m "docs(command-center): reconcile P2-3 entry and ZIP artifact workflow"
```

Expected:

```text
parent:
05185c57a6265a4002050ce25cdfde3dc87e9779

parent count:
1

message:
docs(command-center): reconcile P2-3 entry and ZIP artifact workflow

changed paths:
15 exact
```

Forbidden:

```text
git add -A
git add .
git clean
git reset
git restore
git checkout
git stash
git push
git pull
git fetch
git merge
git rebase
git cherry-pick
```

# 14. post-commit verification

Verify:

1. result commit/tree
2. exact parent and parent count 1
3. exact message
4. exact 15 changed paths
5. P2-2 closed/persisted + P2-3 next in current-state docs
6. Short Prompt minimal ZIP bootstrap contract
7. Human manual extraction removed from current workflow
8. Task owns detailed remaining artifact manifest/transport
9. outbound Executor bundle ZIP requirement
10. index empty
11. worktree clean
12. push/network NOT_RUN

# 15. export bundle and outbound ZIP

Bundle folder:

```text
.aiassistant/reports/target/20260908_1800_aiscc-p2-3-entry-state-and-artifact-zip-workflow-reconciliation-retry-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
STATE_RECONCILIATION_VERIFICATION.md
WORKFLOW_RULE_VERIFICATION.md
GIT_PERSISTENCE_VERIFICATION.md
```

After folder completion create:

```text
.aiassistant/reports/target/20260908_1800_aiscc-p2-3-entry-state-and-artifact-zip-workflow-reconciliation-retry-1.zip
```

ZIP must contain exactly one top-level bundle directory and pass readability/CRC verification.

Keep both folder and outbound ZIP.

# 16. inbound ZIP cleanup

After terminal report/export outcome has been produced and outbound bundle ZIP validation is complete:

```text
remove the exact inbound Command Center delivery ZIP from:
C:\Users\oracl\Downloads
```

Do not delete any other Downloads ZIP/file.

# 17. evidence contract

executor_required:

- inbound ZIP bootstrap verification
- remaining artifact transport
- workspace preflight
- state authority reconciliation
- workflow rule update
- exact Git persistence
- outbound bundle ZIP verification
- final provenance/worktree verification

human_owned:

```text
new Human QA:
NOT_REQUIRED

workflow decisions:
HUMAN_PROVIDED
```

forbidden:

- P2-3 substantive audit
- scenario implementation/run
- Replay generation
- product/demo source mutation
- Project Source sync
- Git push

# 18. mandatory stop

```text
DOWNLOAD_ZIP_MISSING
DOWNLOAD_ZIP_HASH_MISMATCH
DOWNLOAD_ZIP_CORRUPT
DOWNLOAD_ZIP_EXTRACTION_BLOCKED
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

Bootstrap blockers before canonical Task placement create no report/export and retain inbound ZIP.

Repository-level blockers after successful bootstrap use minimum report/export and then remove inbound ZIP at terminal completion.

# 19. final ceiling

Success:

```text
P2-3 entry authority reconciliation:
READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT

P2-3 source/contract audit:
RETRY_READY / NOT_STARTED

P2-3 implementation:
NOT_STARTED
```

Do not resume P2-3 audit in this Task.
