# 작업지시서: P2-3 entry direct-ZIP workflow Git persistence recovery

## meta

- task_id: `20260908_1851_aiscc-p2-3-entry-direct-zip-workflow-git-persistence-recovery-1`
- created_at: `2026-09-08T18:51:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `QA_ONLY / GIT_PERSISTENCE_RECOVERY`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `05185c57a6265a4002050ce25cdfde3dc87e9779`
- required_base_tree: `df997ec70594d0d451c7d281c975c6cbdb63e453`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. bootstrap

The Browser Short Prompt's exact delivery ZIP SHA-256 is this Task's bootstrap integrity anchor.

Place this TASK member first at:

```text
.aiassistant/tasks/active/20260908_1851_aiscc-p2-3-entry-direct-zip-workflow-git-persistence-recovery-1.md
```

Then read this Task.

Current delivery ZIP contains only:

```text
TASK:
20260908_1851_aiscc-p2-3-entry-direct-zip-workflow-git-persistence-recovery-1.md

CYCLE:
20260908_1851_aiscc-p2-3-entry-workflow-reconciliation-staging-gap-recovery-entry-1.cycle.md
SHA-256:
360b2cba02d6099241f9d472162ff7568095c687dfa49fee4a17a2b6cdd0d56b
destination:
.aiassistant/records/aiscc/cycles/20260908_1851_aiscc-p2-3-entry-workflow-reconciliation-staging-gap-recovery-entry-1.cycle.md

JUDGMENT:
20260908_1851_aiscc-p2-3-entry-workflow-reconciliation-staging-gap-judgment-1.md
SHA-256:
45ab9cdb89fa7196cb3de2cecc8c9021f66779ffec895784b49cc81f64c107f5
destination:
.aiassistant/reports/aiscc/20260908_1851_aiscc-p2-3-entry-workflow-reconciliation-staging-gap-judgment-1.md

HANDOFF:
none
```

Materialize current CYCLE/JUDGMENT directly from the verified ZIP to the exact destinations and verify hashes.

Inbound ZIP/staging cleanup remains best-effort and non-blocking after canonical transport.

# 1. inherited blocker state is intentional

Unlike a normal persistence Task, **index empty is NOT expected**.

The required starting repository authority after current artifact placement is:

```text
branch:
main

HEAD:
05185c57a6265a4002050ce25cdfde3dc87e9779

HEAD tree:
df997ec70594d0d451c7d281c975c6cbdb63e453
```

The index must contain exactly the 17 authorized predecessor paths below and no others.

Do not run reset/restore/checkout/stash or restage-all.

# 2. exact inherited staged set — 17

Verify staged path set exactly:

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

Require:

```text
17 / 17 staged
extra staged 0
missing staged 0
no unstaged byte delta on these 17 paths
git diff --cached --check PASS
```

# 3. exact staged byte identity

Verify the staged blob/worktree bytes for each inherited path equal the accepted candidate SHA-256:

- `.aiassistant/tasks/done/20260908_1700_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-1.md`  `583a969afa932f4f72ba20c14e1ccd3deed80f2fefb54bc706ab68b947b4a1ca`
- `.aiassistant/records/aiscc/cycles/20260908_1700_aiscc-p2-2-terminal-closure-p2-3-entry-1.cycle.md`  `cf4a7e71bd8fd4e9cc9b77f18c1843183bcfd6b9e3cef00a1263826489b76b48`
- `.aiassistant/reports/aiscc/20260908_1700_aiscc-p2-2-terminal-closure-judgment-1.md`  `fc25869a18a0ba44316f83c4fec2573a656f4ec55f6f0a2aba8a17eaeab241eb`
- `.aiassistant/tasks/done/20260908_1741_aiscc-p2-3-entry-state-and-command-center-export-workflow-reconciliation-1.md`  `908b55341b4b87b2f0e4eb85dca9da91e140c4ca8c2a38d173755944ea7b077b`
- `.aiassistant/records/aiscc/cycles/20260908_1741_aiscc-p2-3-audit-blocked-stale-current-state-reconciliation-entry-1.cycle.md`  `bc2479b77d7c9fd2a6406ad8b21f6a857cdb5c84296a598a6f6aea87c62be72e`
- `.aiassistant/reports/aiscc/20260908_1741_aiscc-p2-3-audit-stale-current-state-authority-conflict-judgment-1.md`  `a9f264d260c52bb1dd9e79e91f49e26b7fb8eda9a79d067c644e45d18e99f63b`
- `.aiassistant/records/aiscc/cycles/20260908_1800_aiscc-p2-3-reconciliation-blocked-bootstrap-hash-contract-retry-entry-1.cycle.md`  `b82ed4d3b1fcf45896fb0ec4fea856e18839e5b6ac26597cd086357914328902`
- `.aiassistant/reports/aiscc/20260908_1800_aiscc-p2-3-reconciliation-bootstrap-hash-contract-ambiguity-judgment-1.md`  `8ae60b61e9798bde27811d1e378946d46c2d519393257b60c3434729da6c6854`
- `.aiassistant/records/aiscc/cycles/20260908_1815_aiscc-p2-3-reconciliation-blocked-nonblocking-cleanup-retry-entry-1.cycle.md`  `e9dbc77e6ec58802b7657aa0ffa22f7dbb9a0ec1f2692c952ff14dc7330c9ab9`
- `.aiassistant/reports/aiscc/20260908_1815_aiscc-p2-3-reconciliation-cleanup-gate-overconstraint-judgment-1.md`  `ceb1792e44e7a7dc6fb58497d261a8488cffcb8c941d01336cd14d5a8e0af5a9`
- `.aiassistant/tasks/done/20260908_1800_aiscc-p2-3-entry-state-and-artifact-zip-workflow-reconciliation-retry-1.md`  `c234bc8e2350a32e6cb060402fa499b50537004cb148f3a40883f574c88cdb6c`
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `f5099c829e4f5aea5d5422895eba184f60ac53a65f0b7d5423f3fca2e74115f3`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `e7d9454103525b31e2ab770abecc07574e8c8589a3a0a4196e10ea6c3f0d7624`
- `.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md`  `201f4f26b46bc626e6a11e02f9d54707ea8805f66ca77b394c129c88371026e4`
- `.aiassistant/records/command-center/TASK_FILE_TEMPLATE.md`  `991bcd9b68443f8a8ea0ee1a962401d9e96f6bc7a36ad0ae4360c71a284737df`
- `.aiassistant/records/command-center/SHORT_EXECUTOR_PROMPT_TEMPLATE.md`  `bd2a2de79d1f0676c1f16d551798703774db365fea1b1ba5aeed7e4dcb7c270c`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`  `761aeca33d589ca76c5085e45410a9e05b0eca06e6058e2057f05dd99e341218`

Any mismatch:

```text
INHERITED_STAGED_IDENTITY_MISMATCH
→ STOP
```

Do not repair.

# 4. exact unstaged/untracked authorized set after transport

Before current Task lifecycle, the only authorized Git-visible paths outside the inherited staged 17 are:

```text
.aiassistant/tasks/done/20260908_1815_aiscc-p2-3-entry-state-and-direct-zip-workflow-reconciliation-retry-1.md
SHA-256:
1b2018646ac1e287380e7b718ce7f294cac4c9555a60e3a5e4544120c39445cd

.aiassistant/records/aiscc/cycles/20260908_1851_aiscc-p2-3-entry-workflow-reconciliation-staging-gap-recovery-entry-1.cycle.md
SHA-256:
360b2cba02d6099241f9d472162ff7568095c687dfa49fee4a17a2b6cdd0d56b

.aiassistant/reports/aiscc/20260908_1851_aiscc-p2-3-entry-workflow-reconciliation-staging-gap-judgment-1.md
SHA-256:
45ab9cdb89fa7196cb3de2cecc8c9021f66779ffec895784b49cc81f64c107f5
```

Current active Task is ignored.

No other modified/untracked path is allowed.

Require:

```text
total Git-visible paths excluding current active Task:
20 exact
```

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

# 5. no document/source mutation

Do not edit any of the 18 predecessor candidate files.

Do not modify product/runtime/test/demo source.

Do not rerun the P2-3 substantive audit.

Accepted candidate content is reused only under exact hash identity.

# 6. accepted candidate reuse

If sections 2–4 PASS:

```text
1815 state reconciliation candidate:
REUSED_ACCEPTED

1815 direct-ZIP workflow candidate:
REUSED_ACCEPTED

1815 outbound ZIP proof:
REUSED_ACCEPTED

document integrity:
REUSED_ACCEPTED
```

This is content/evidence reuse only; Git persistence is current execution evidence.

# 7. current report/export preparation

Create the current result bundle folder:

```text
.aiassistant/reports/target/20260908_1851_aiscc-p2-3-entry-direct-zip-workflow-git-persistence-recovery-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
INHERITED_INDEX_VERIFICATION.md
GIT_PERSISTENCE_VERIFICATION.md
```

The target folder/ZIP are Git-ignored and are not commit candidates.

# 8. current Task lifecycle

After all pre-persistence evidence and report material required to proceed are complete:

```text
.aiassistant/tasks/active/20260908_1851_aiscc-p2-3-entry-direct-zip-workflow-git-persistence-recovery-1.md
→
.aiassistant/tasks/done/20260908_1851_aiscc-p2-3-entry-direct-zip-workflow-git-persistence-recovery-1.md
```

Do not edit Task bytes.

Then the only four authorized unstaged/untracked commit paths must be:

```text
.aiassistant/tasks/done/20260908_1815_aiscc-p2-3-entry-state-and-direct-zip-workflow-reconciliation-retry-1.md
.aiassistant/records/aiscc/cycles/20260908_1851_aiscc-p2-3-entry-workflow-reconciliation-staging-gap-recovery-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_1851_aiscc-p2-3-entry-workflow-reconciliation-staging-gap-judgment-1.md
.aiassistant/tasks/done/20260908_1851_aiscc-p2-3-entry-direct-zip-workflow-git-persistence-recovery-1.md
```

# 9. stage only the four missing/current paths

Authorize only:

```text
git add -- ".aiassistant/tasks/done/20260908_1815_aiscc-p2-3-entry-state-and-direct-zip-workflow-reconciliation-retry-1.md" ".aiassistant/records/aiscc/cycles/20260908_1851_aiscc-p2-3-entry-workflow-reconciliation-staging-gap-recovery-entry-1.cycle.md" ".aiassistant/reports/aiscc/20260908_1851_aiscc-p2-3-entry-workflow-reconciliation-staging-gap-judgment-1.md" ".aiassistant/tasks/done/20260908_1851_aiscc-p2-3-entry-direct-zip-workflow-git-persistence-recovery-1.md"
```

Do not re-add or reset the inherited staged 17.

Then require:

```text
final staged:
21 exact

unstaged tracked:
0

untracked governance commit candidates:
0

extra staged:
0

git diff --cached --check:
PASS
```

# 10. exact 21-path final commit allowlist

The final staged set is:

## inherited 18 candidate

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

## current recovery provenance

```text
.aiassistant/records/aiscc/cycles/20260908_1851_aiscc-p2-3-entry-workflow-reconciliation-staging-gap-recovery-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_1851_aiscc-p2-3-entry-workflow-reconciliation-staging-gap-judgment-1.md
.aiassistant/tasks/done/20260908_1851_aiscc-p2-3-entry-direct-zip-workflow-git-persistence-recovery-1.md
```

Total:

```text
21 exact
```

# 11. Git commit authorization

Only after exact 21-path staging PASS:

```text
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

# 12. post-commit verification

Verify:

1. result commit hash/tree
2. exact parent `05185c57a6265a4002050ce25cdfde3dc87e9779`
3. parent count 1
4. exact message
5. exact 21 changed paths
6. predecessor candidate 18 committed bytes match accepted hashes
7. current Cycle/Judgment/Task committed bytes match current issued bytes
8. index empty
9. Git-visible worktree clean
10. P2-2 closed/persisted and P2-3 next remain in committed state docs
11. direct-ZIP workflow and automatic outbound ZIP contract remain present
12. push/network NOT_RUN

# 13. complete outbound result ZIP

After terminal report folder contents are complete, create:

```text
.aiassistant/reports/target/20260908_1851_aiscc-p2-3-entry-direct-zip-workflow-git-persistence-recovery-1.zip
```

Require:

```text
one top-level bundle directory
archive readable
CRC/integrity PASS
required root files present
folder/archive filename-set equality
folder/archive byte equality
```

Keep both folder and outbound ZIP.

If creation/validation fails:

```text
ZIP_EXPORT_FAILED
→ report blocker
```

# 14. inbound cleanup

After terminal outcome and outbound ZIP validation, attempt exact current inbound delivery ZIP cleanup best-effort.

Any refusal:

```text
NON_BLOCKING_LOCAL_RESIDUE
```

Do not attempt alternate delete mechanisms or broad Downloads cleanup.

The known prior 1800 staging residue may remain and is not a persistence blocker.

# 15. evidence contract

executor_required:

- current ZIP bootstrap and Cycle/Judgment canonical transport
- inherited staged-set identity
- authorized unstaged set identity
- exact four-path staging recovery
- exact 21-path Git persistence
- post-commit provenance
- outbound result ZIP

reuse_allowed:

- 1815 candidate document content and workflow verification under exact hashes
- 1815 outbound ZIP operational proof as predecessor evidence

human_owned:

```text
new Human QA:
NOT_REQUIRED
```

forbidden:

- document/source re-edit
- reset/restore/restage-all
- P2-3 audit/run/Replay
- Git push/network

# 16. mandatory stop

```text
DOWNLOAD_ZIP_MISSING
DOWNLOAD_ZIP_HASH_MISMATCH
DOWNLOAD_ZIP_CORRUPT
DOWNLOAD_TASK_MEMBER_MISSING
DOWNLOAD_TASK_PLACEMENT_FAILED
TRANSPORT_FAILURE
HEAD_OR_TREE_MISMATCH
INHERITED_STAGED_SET_MISMATCH
INHERITED_STAGED_IDENTITY_MISMATCH
DIRTY_WORKSPACE_MIXED
CURRENT_TASK_IDENTITY_MISMATCH
GIT_STAGE_ALLOWLIST_MISMATCH
GIT_COMMIT_VERIFICATION_FAILED
ZIP_EXPORT_FAILED
```

Inbound cleanup refusal after canonical transport is NOT a mandatory blocker.

# 17. final ceiling

Success:

```text
P2-3 entry authority reconciliation:
PERSISTED / READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT

P2-3 source/contract audit:
RETRY_READY / NOT_STARTED

P2-3 implementation:
NOT_STARTED
```

Do not declare P2-3 implementation started.
