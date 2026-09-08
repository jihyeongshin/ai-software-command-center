# 작업지시서: P2-3 entry state and direct-ZIP workflow reconciliation retry

## meta

- task_id: `20260908_1815_aiscc-p2-3-entry-state-and-direct-zip-workflow-reconciliation-retry-1`
- created_at: `2026-09-08T18:15:00+09:00`
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

# 0. bootstrap authority

This Task is trusted only after the Browser Short Prompt's exact inbound delivery ZIP SHA-256 has passed.

The delivery ZIP SHA is the bootstrap integrity anchor for this TASK member.

Do not require this Task to contain its own whole-file SHA.

# 1. current delivery manifest

Current delivery ZIP contains exactly:

```text
TASK:
20260908_1815_aiscc-p2-3-entry-state-and-direct-zip-workflow-reconciliation-retry-1.md

CYCLE:
20260908_1815_aiscc-p2-3-reconciliation-blocked-nonblocking-cleanup-retry-entry-1.cycle.md
SHA-256:
e9dbc77e6ec58802b7657aa0ffa22f7dbb9a0ec1f2692c952ff14dc7330c9ab9
destination:
.aiassistant/records/aiscc/cycles/20260908_1815_aiscc-p2-3-reconciliation-blocked-nonblocking-cleanup-retry-entry-1.cycle.md

JUDGMENT:
20260908_1815_aiscc-p2-3-reconciliation-cleanup-gate-overconstraint-judgment-1.md
SHA-256:
ceb1792e44e7a7dc6fb58497d261a8488cffcb8c941d01336cd14d5a8e0af5a9
destination:
.aiassistant/reports/aiscc/20260908_1815_aiscc-p2-3-reconciliation-cleanup-gate-overconstraint-judgment-1.md

HANDOFF:
none
```

The TASK member must be materialized first to:

```text
.aiassistant/tasks/active/20260908_1815_aiscc-p2-3-entry-state-and-direct-zip-workflow-reconciliation-retry-1.md
```

and read.

Then materialize CYCLE/JUDGMENT directly from the verified ZIP to their exact canonical destinations.

Preferred method:

```text
archive member
→ exact canonical destination
```

Do not require flat extraction to Downloads.

If the available archive operation cannot directly materialize one member, a package-specific temporary extraction directory is allowed.

# 2. canonical artifact integrity

For current CYCLE/JUDGMENT:

```text
archive member exists
→ expected SHA-256 exact
→ destination absent or expected-state check
→ exact materialization
→ destination SHA-256 exact
```

Any failure before exact canonical placement:

```text
TRANSPORT_FAILURE
→ STOP
```

# 3. inbound cleanup is non-blocking

After all issued members are exact at canonical destinations:

```text
canonical transport:
PASS
```

From this point onward, these are **not mandatory gates**:

```text
temporary extracted member removal
empty staging-directory removal
inbound Downloads ZIP removal
```

At terminal completion, attempt exact cleanup only as best effort.

If cleanup is refused/blocked:

```text
classify:
NON_BLOCKING_LOCAL_RESIDUE

record exact remaining path if known
continue substantive work / preserve accepted result
do not retry with alternate deletion mechanism in the same turn
```

Never perform broad Downloads cleanup.

# 4. repository gate after current artifact placement

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

Expected Git-visible set is exact ten paths:

- `.aiassistant/tasks/done/20260908_1700_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_1700_aiscc-p2-2-terminal-closure-p2-3-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1700_aiscc-p2-2-terminal-closure-judgment-1.md`
- `.aiassistant/tasks/done/20260908_1741_aiscc-p2-3-entry-state-and-command-center-export-workflow-reconciliation-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_1741_aiscc-p2-3-audit-blocked-stale-current-state-reconciliation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1741_aiscc-p2-3-audit-stale-current-state-authority-conflict-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_1800_aiscc-p2-3-reconciliation-blocked-bootstrap-hash-contract-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1800_aiscc-p2-3-reconciliation-bootstrap-hash-contract-ambiguity-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_1815_aiscc-p2-3-reconciliation-blocked-nonblocking-cleanup-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1815_aiscc-p2-3-reconciliation-cleanup-gate-overconstraint-judgment-1.md`

Current `1815` active Task is ignored.
Current `1800` active Task is also ignored at this gate.

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

# 5. existing provenance identity

Verify current canonical bytes before mutation.

## 1700

- `.aiassistant/tasks/done/20260908_1700_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-1.md`  `583a969afa932f4f72ba20c14e1ccd3deed80f2fefb54bc706ab68b947b4a1ca`
- `.aiassistant/records/aiscc/cycles/20260908_1700_aiscc-p2-2-terminal-closure-p2-3-entry-1.cycle.md`  `cf4a7e71bd8fd4e9cc9b77f18c1843183bcfd6b9e3cef00a1263826489b76b48`
- `.aiassistant/reports/aiscc/20260908_1700_aiscc-p2-2-terminal-closure-judgment-1.md`  `fc25869a18a0ba44316f83c4fec2573a656f4ec55f6f0a2aba8a17eaeab241eb`

## 1741

- `.aiassistant/tasks/done/20260908_1741_aiscc-p2-3-entry-state-and-command-center-export-workflow-reconciliation-1.md`  `908b55341b4b87b2f0e4eb85dca9da91e140c4ca8c2a38d173755944ea7b077b`
- `.aiassistant/records/aiscc/cycles/20260908_1741_aiscc-p2-3-audit-blocked-stale-current-state-reconciliation-entry-1.cycle.md`  `bc2479b77d7c9fd2a6406ad8b21f6a857cdb5c84296a598a6f6aea87c62be72e`
- `.aiassistant/reports/aiscc/20260908_1741_aiscc-p2-3-audit-stale-current-state-authority-conflict-judgment-1.md`  `a9f264d260c52bb1dd9e79e91f49e26b7fb8eda9a79d067c644e45d18e99f63b`

## 1800

```text
active Task:
.aiassistant/tasks/active/20260908_1800_aiscc-p2-3-entry-state-and-artifact-zip-workflow-reconciliation-retry-1.md
SHA-256:
c234bc8e2350a32e6cb060402fa499b50537004cb148f3a40883f574c88cdb6c
```

- `.aiassistant/records/aiscc/cycles/20260908_1800_aiscc-p2-3-reconciliation-blocked-bootstrap-hash-contract-retry-entry-1.cycle.md`  `b82ed4d3b1fcf45896fb0ec4fea856e18839e5b6ac26597cd086357914328902`
- `.aiassistant/reports/aiscc/20260908_1800_aiscc-p2-3-reconciliation-bootstrap-hash-contract-ambiguity-judgment-1.md`  `8ae60b61e9798bde27811d1e378946d46c2d519393257b60c3434729da6c6854`

Any mismatch:

```text
PREDECESSOR_PROVENANCE_IDENTITY_MISMATCH
→ STOP
```

# 6. normalize blocked 1800 Task

After exact source hash verification:

```text
.aiassistant/tasks/active/20260908_1800_aiscc-p2-3-entry-state-and-artifact-zip-workflow-reconciliation-retry-1.md
→
.aiassistant/tasks/done/20260908_1800_aiscc-p2-3-entry-state-and-artifact-zip-workflow-reconciliation-retry-1.md
```

Destination absent:
- move exact source
- verify exact destination SHA

Destination present:
- verify exact hash
- if equal, remove only duplicate active source
- if different, STOP

Do not overwrite a differing done artifact.

After normalization:

```text
Git-visible governance:
11 exact paths
```

# 7. must-read canonical sources

Read:

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

.aiassistant/records/aiscc/cycles/20260908_1815_aiscc-p2-3-reconciliation-blocked-nonblocking-cleanup-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_1815_aiscc-p2-3-reconciliation-cleanup-gate-overconstraint-judgment-1.md
```

No unrelated historical bulk-read.

# 8. exact allowed canonical modifications

Only these existing canonical documents may be edited:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
- `.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md`
- `.aiassistant/records/command-center/TASK_FILE_TEMPLATE.md`
- `.aiassistant/records/command-center/SHORT_EXECUTOR_PROMPT_TEMPLATE.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`

Plus:

- existing issued provenance already listed
- current Task active→done lifecycle

No product/runtime/test/demo source mutation.

# 9. current-state reconciliation

Update `CURRENT_STATE_SUMMARY.md` and `NEXT_ACTIONS.md` so current authority states:

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

Remove/replace explicitly current stale claims that P2-2 is NOT_STARTED/current next work.

Do not rewrite dated historical lineage merely because it records an older state.

# 10. canonical inbound delivery workflow

Update:

```text
COMMAND_CENTER_WORKFLOW.md
TASK_FILE_TEMPLATE.md
SHORT_EXECUTOR_PROMPT_TEMPLATE.md
```

to make this the default:

## Human

```text
download one delivery ZIP to:
C:\Users\oracl\Downloads

do not manually extract
do not manually place Markdown artifacts

open a fresh IDE chat only when Browser explicitly requires it
send Short Prompt
```

## Browser Short Prompt

Must normally remain compact and contain only:

```text
Downloads root
exact delivery ZIP filename
delivery ZIP expected SHA-256
exact TASK filename
bootstrap STOP rule
instruction to place TASK first and read it
```

Detailed artifact hashes/destinations/workspace/evidence/Git instructions belong in Task.

## Executor bootstrap

```text
1. verify exact inbound ZIP exists
2. verify exact ZIP SHA-256
3. validate archive readability/member safety
4. materialize TASK member directly to canonical tasks/active if supported
5. otherwise use package-specific staging only as needed
6. read TASK
7. Task governs remaining artifact placement and substantive work
```

Archive members must not escape their intended names/paths.

## blocking bootstrap failures

Before TASK canonical placement:

```text
ZIP missing
ZIP hash mismatch
archive corrupt/unreadable
TASK member absent
TASK canonical placement failed
```

→ STOP with no report/export and ask Human to re-download/reposition ZIP.

## cleanup distinction

After exact canonical placement:

```text
Downloads ZIP/staging cleanup failure
!=
transport failure
```

It is `NON_BLOCKING_LOCAL_RESIDUE`.

# 11. outbound Executor bundle ZIP

Update `IDE_EXECUTOR_REPORT_EXPORT.md` and relevant workflow/template references.

Completed bundle folder:

```text
.aiassistant/reports/target/<bundle-name>/
```

must be followed by:

```text
.aiassistant/reports/target/<bundle-name>.zip
```

Requirements:

```text
- exactly one top-level <bundle-name>/ directory
- full completed bundle below it
- relative layout preserved
- readable archive
- CRC/integrity PASS
- required root files present
- original bundle folder retained
```

Outbound result ZIP is a required deliverable.

If outbound ZIP creation/validation fails:

```text
ZIP_EXPORT_FAILED
```

Preserve the bundle folder and do not claim export completion.

# 12. document integrity

Require:

```text
UTF-8
no control-character corruption
balanced Markdown fences
git diff --check PASS
```

Preserve Korean-first document policy where applicable.

# 13. pre-commit workspace

Before current Task lifecycle move:

```text
11 governance provenance
+
6 modified canonical docs
=
17 exact Git-visible paths
```

Then:

```text
.aiassistant/tasks/active/20260908_1815_aiscc-p2-3-entry-state-and-direct-zip-workflow-reconciliation-retry-1.md
→
.aiassistant/tasks/done/20260908_1815_aiscc-p2-3-entry-state-and-direct-zip-workflow-reconciliation-retry-1.md
```

Final commit candidate:

```text
18 exact paths
```

# 14. exact commit allowlist

- `.aiassistant/tasks/done/20260908_1700_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_1700_aiscc-p2-2-terminal-closure-p2-3-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1700_aiscc-p2-2-terminal-closure-judgment-1.md`
- `.aiassistant/tasks/done/20260908_1741_aiscc-p2-3-entry-state-and-command-center-export-workflow-reconciliation-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_1741_aiscc-p2-3-audit-blocked-stale-current-state-reconciliation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1741_aiscc-p2-3-audit-stale-current-state-authority-conflict-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_1800_aiscc-p2-3-reconciliation-blocked-bootstrap-hash-contract-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1800_aiscc-p2-3-reconciliation-bootstrap-hash-contract-ambiguity-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_1815_aiscc-p2-3-reconciliation-blocked-nonblocking-cleanup-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1815_aiscc-p2-3-reconciliation-cleanup-gate-overconstraint-judgment-1.md`
- `.aiassistant/tasks/done/20260908_1800_aiscc-p2-3-entry-state-and-artifact-zip-workflow-reconciliation-retry-1.md`
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
- `.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md`
- `.aiassistant/records/command-center/TASK_FILE_TEMPLATE.md`
- `.aiassistant/records/command-center/SHORT_EXECUTOR_PROMPT_TEMPLATE.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/tasks/done/20260908_1815_aiscc-p2-3-entry-state-and-direct-zip-workflow-reconciliation-retry-1.md`

No other path may be staged.

# 15. Git persistence

Only after all prior gates PASS:

```text
git add -- <exact 18 literal paths>
git diff --cached --check
git diff --cached --name-status
git commit -m "docs(command-center): reconcile P2-3 entry and direct ZIP workflow"
```

Expected:

```text
parent:
05185c57a6265a4002050ce25cdfde3dc87e9779

parent count:
1

message:
docs(command-center): reconcile P2-3 entry and direct ZIP workflow

changed paths:
18 exact
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

# 16. post-commit verification

Verify:

1. result commit/tree
2. exact parent / parent count 1
3. exact commit message
4. changed paths exact 18
5. current state says P2-2 closed/persisted and P2-3 next
6. Short Prompt is compact ZIP bootstrap
7. Human manual extraction is no longer required
8. direct archive-member canonical placement is preferred
9. staging/inbound cleanup failure is non-blocking after canonical transport
10. Task owns detailed transport contract
11. outbound Executor result ZIP is mandatory and verified
12. index empty
13. Git-visible worktree clean
14. push/network NOT_RUN

# 17. export bundle + automatic result ZIP

Bundle folder:

```text
.aiassistant/reports/target/20260908_1815_aiscc-p2-3-entry-state-and-direct-zip-workflow-reconciliation-retry-1/
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

After the folder is complete, create:

```text
.aiassistant/reports/target/20260908_1815_aiscc-p2-3-entry-state-and-direct-zip-workflow-reconciliation-retry-1.zip
```

Validate:

```text
readable
CRC/integrity PASS
one top-level bundle directory
required root files present
```

Keep both folder and outbound ZIP.

# 18. best-effort inbound cleanup

Only after terminal outcome and outbound result ZIP verification:

Attempt exact cleanup of:

```text
current inbound Command Center delivery ZIP
current Task-owned staging residue, if any
```

If an exact known prior `1800` Task-owned staging residue is present and can be safely identified without broad search, it may also be removed best-effort.

Any delete refusal:

```text
NON_BLOCKING_LOCAL_RESIDUE
```

Report it and continue.

Do not use wildcard/broad Downloads cleanup.
Do not make final task acceptance depend on inbound cleanup.

# 19. evidence contract

executor_required:

- inbound ZIP bootstrap
- current artifact canonical placement
- predecessor provenance identity
- 1800 blocked Task lifecycle normalization
- state authority reconciliation
- workflow rule update
- Git persistence
- outbound result ZIP verification
- final repository provenance

human_owned:

```text
new Human QA:
NOT_REQUIRED

workflow decisions:
HUMAN_PROVIDED
```

forbidden:

- P2-3 substantive source/contract audit
- scenario implementation/run
- Replay generation
- product/demo source mutation
- Project Source sync
- Git push

# 20. mandatory stop

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
CANONICAL_AUTHORITY_CONFLICT
DOCUMENT_CONTRACT_MISMATCH
GIT_STAGE_ALLOWLIST_MISMATCH
GIT_COMMIT_VERIFICATION_FAILED
ZIP_EXPORT_FAILED
```

Explicitly NOT a mandatory blocker after canonical transport:

```text
DOWNLOADS_CLEANUP_REFUSED
STAGING_CLEANUP_REFUSED
INBOUND_ZIP_DELETE_REFUSED
```

# 21. final ceiling

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
