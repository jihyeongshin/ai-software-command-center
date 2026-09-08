# 작업지시서: P2-3 Decision Register artifact-delivery supersession reconciliation

## meta

- task_id: `20260908_2230_aiscc-p2-3-decision-register-artifact-delivery-supersession-reconciliation-1`
- created_at: `2026-09-08T22:30:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `COMMAND_CENTER_RECORD_UPDATE / GIT_PERSISTENCE`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `89ebcffacd9b8e74d3c598ddf6e3274a69a9bc1c`
- required_base_tree: `8c02a4f06c297ed6815fce140b8c5e1bc96e977d`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `read-only P2-3 audit → canonical Decision Register mutation and Git persistence authority`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. inbound ZIP bootstrap

The Browser Short Prompt's exact delivery ZIP SHA-256 is the bootstrap integrity anchor.

Current delivery ZIP contains:

```text
TASK:
20260908_2230_aiscc-p2-3-decision-register-artifact-delivery-supersession-reconciliation-1.md

CYCLE:
20260908_2230_aiscc-p2-3-audit-blocked-stale-decision-register-reconciliation-entry-1.cycle.md
SHA-256:
58c943ba7ea8692383ff141e45345300c2c5811af677ebd713aaa10c237ed009
destination:
.aiassistant/records/aiscc/cycles/20260908_2230_aiscc-p2-3-audit-blocked-stale-decision-register-reconciliation-entry-1.cycle.md

JUDGMENT:
20260908_2230_aiscc-p2-3-audit-stale-decision-register-authority-conflict-judgment-1.md
SHA-256:
c62a52176302a13b58578f08b8cf9d21c1ef819ca7314a2ce338311afa625948
destination:
.aiassistant/reports/aiscc/20260908_2230_aiscc-p2-3-audit-stale-decision-register-authority-conflict-judgment-1.md

HANDOFF:
none
```

Human downloads only the ZIP.

Executor:

1. verify exact ZIP filename/SHA-256;
2. validate archive readability/member safety;
3. materialize TASK first to `.aiassistant/tasks/active/20260908_2230_aiscc-p2-3-decision-register-artifact-delivery-supersession-reconciliation-1.md`;
4. read TASK;
5. materialize CYCLE/JUDGMENT directly to exact canonical destinations;
6. verify exact hashes.

Bootstrap failure before canonical TASK placement:

```text
STOP
no report/export
no substantive project mutation
ask Human to re-download/reposition ZIP
```

Inbound ZIP/staging cleanup after successful canonical transport is best-effort and non-blocking.

# 1. repository gate

After current artifact placement require:

```text
branch:
main

HEAD:
89ebcffacd9b8e74d3c598ddf6e3274a69a9bc1c

HEAD tree:
8c02a4f06c297ed6815fce140b8c5e1bc96e977d

index:
empty
```

Expected Git-visible set is exact five paths:

- `.aiassistant/tasks/done/20260908_2200_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_2200_aiscc-p2-3-entry-reconciliation-accepted-source-audit-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_2200_aiscc-p2-3-entry-reconciliation-final-acceptance-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_2230_aiscc-p2-3-audit-blocked-stale-decision-register-reconciliation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_2230_aiscc-p2-3-audit-stale-decision-register-authority-conflict-judgment-1.md`

Current active Task is ignored.

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

# 2. predecessor provenance identity

Verify exact SHA-256:

- `.aiassistant/tasks/done/20260908_2200_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-retry-1.md`  `13195c511bf4079829c8c9e3b44cae67966d891f937037a6a3fb73573c1a5ced`
- `.aiassistant/records/aiscc/cycles/20260908_2200_aiscc-p2-3-entry-reconciliation-accepted-source-audit-retry-entry-1.cycle.md`  `467cf8974c5fbc9ebb1d1becda9c8723afc0bbc0bcd0e394a4dbcfc709146116`
- `.aiassistant/reports/aiscc/20260908_2200_aiscc-p2-3-entry-reconciliation-final-acceptance-judgment-1.md`  `6b205568bb4fdf3a5bdf5383749e699f0ef0ffaceeb47dfe358156b1b847aeb3`

Any mismatch:

```text
PREDECESSOR_PROVENANCE_IDENTITY_MISMATCH
→ STOP
```

# 3. must-read canonical authority

Read fully:

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md
.aiassistant/records/command-center/TASK_FILE_TEMPLATE.md
.aiassistant/records/command-center/SHORT_EXECUTOR_PROMPT_TEMPLATE.md

.aiassistant/records/aiscc/DECISION_REGISTER.md

.aiassistant/records/aiscc/cycles/20260908_2200_aiscc-p2-3-entry-reconciliation-accepted-source-audit-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_2200_aiscc-p2-3-entry-reconciliation-final-acceptance-judgment-1.md

.aiassistant/records/aiscc/cycles/20260908_2230_aiscc-p2-3-audit-blocked-stale-decision-register-reconciliation-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_2230_aiscc-p2-3-audit-stale-decision-register-authority-conflict-judgment-1.md
```

No unrelated historical bulk-read.

# 4. exact mutation scope

Only one existing tracked canonical document may be edited:

```text
.aiassistant/records/aiscc/DECISION_REGISTER.md
```

Plus current Task active→done lifecycle and already issued provenance.

Do not modify:

- CURRENT_STATE_SUMMARY
- NEXT_ACTIONS
- product/runtime/test/demo source
- security/public-runtime baseline
- other Decision Register entries except the exact delivery lineage needed for supersession

# 5. reconcile AISCC-COMMAND-CENTER-ARTIFACT-DELIVERY-V1

Locate exact decision:

```text
AISCC-COMMAND-CENTER-ARTIFACT-DELIVERY-V1
```

Preserve its historical text and original Human-provided provenance.

Make it unambiguously non-current by adding/updating explicit metadata equivalent to:

```text
status:
SUPERSEDED

current_operational_authority:
NO

superseded_by:
AISCC-COMMAND-CENTER-ARTIFACT-DELIVERY-ZIP-DIRECT-V2
```

Do not delete the old decision body.

The old decision must no longer be reasonably readable as the current transport/cleanup rule.

# 6. add successor decision

Add a new Decision Register entry:

```text
decision_id:
AISCC-COMMAND-CENTER-ARTIFACT-DELIVERY-ZIP-DIRECT-V2

decision_source:
HUMAN_PROVIDED / CANONICALIZED / PERSISTED

authority_commit:
89ebcffacd9b8e74d3c598ddf6e3274a69a9bc1c
```

Record these exact current semantics:

## Human responsibility

```text
- download one Command Center delivery ZIP into C:\Users\oracl\Downloads
- do not manually flat-extract Markdown artifacts
- do not manually place canonical artifact files
- open fresh IDE chat only when Browser explicitly requires it
```

## Browser Short Prompt

```text
compact bootstrap only:
- Downloads root
- exact ZIP filename
- exact ZIP SHA-256
- exact TASK filename
- bootstrap STOP rule
```

Detailed execution authority remains in the Task.

## Executor bootstrap/transport

```text
- verify delivery ZIP hash and archive
- prefer direct archive-member → canonical placement
- place TASK first into tasks/active and read it
- Task governs remaining CYCLE/JUDGMENT/HANDOFF hashes/destinations
```

## cleanup semantics

After exact canonical transport:

```text
inbound ZIP delete refusal:
NON_BLOCKING_LOCAL_RESIDUE

temporary extraction/staging cleanup refusal:
NON_BLOCKING_LOCAL_RESIDUE
```

These do not invalidate substantive work or accepted repository outcome.

## outbound result bundle

Executor completion requires:

```text
.aiassistant/reports/target/<bundle-name>/
.aiassistant/reports/target/<bundle-name>.zip
```

The outbound ZIP is validated and preserved for direct Human upload to Browser Command Center.

## supersession semantics

State explicitly:

```text
This decision supersedes AISCC-COMMAND-CENTER-ARTIFACT-DELIVERY-V1
for current artifact transport, Human extraction, inbound ZIP cleanup,
and Executor result ZIP delivery behavior.
```

Historical V1 provenance remains retained.

# 7. consistency verification

After edit, verify targeted semantic queries no longer yield two simultaneously-current delivery workflows.

At minimum check the current operational authority across:

```text
DECISION_REGISTER.md
COMMAND_CENTER_WORKFLOW.md
TASK_FILE_TEMPLATE.md
SHORT_EXECUTOR_PROMPT_TEMPLATE.md
IDE_EXECUTOR_REPORT_EXPORT.md
```

Require:

```text
manual Human flat extraction:
historical/superseded only

direct ZIP bootstrap:
current

inbound cleanup refusal after canonical transport:
non-blocking

outbound result ZIP:
mandatory
```

If another unqualified canonical artifact-delivery rule conflicts:

```text
CANONICAL_AUTHORITY_CONFLICT
→ STOP
```

Do not widen scope to rewrite unrelated records without new Command Center authority.

# 8. document integrity

Require:

```text
UTF-8
no BOM/control-character corruption
balanced Markdown fences
git diff --check PASS
```

Preserve existing Korean-first style.

# 9. pre-commit workspace

Before current Task lifecycle:

```text
5 issued/pending provenance
+
DECISION_REGISTER.md
=
6 exact Git-visible paths
```

Then move:

```text
.aiassistant/tasks/active/20260908_2230_aiscc-p2-3-decision-register-artifact-delivery-supersession-reconciliation-1.md
→
.aiassistant/tasks/done/20260908_2230_aiscc-p2-3-decision-register-artifact-delivery-supersession-reconciliation-1.md
```

Final commit candidate:

```text
7 exact paths
```

# 10. exact final commit allowlist

- `.aiassistant/tasks/done/20260908_2200_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_2200_aiscc-p2-3-entry-reconciliation-accepted-source-audit-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_2200_aiscc-p2-3-entry-reconciliation-final-acceptance-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_2230_aiscc-p2-3-audit-blocked-stale-decision-register-reconciliation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_2230_aiscc-p2-3-audit-stale-decision-register-authority-conflict-judgment-1.md`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`
- `.aiassistant/tasks/done/20260908_2230_aiscc-p2-3-decision-register-artifact-delivery-supersession-reconciliation-1.md`

No other path may be staged.

# 11. Git persistence

Only after all prior gates PASS:

```text
git add -- <exact 7 literal paths>
git diff --cached --check
git diff --cached --name-status
git commit -m "docs(command-center): supersede legacy artifact delivery decision"
```

Expected:

```text
parent:
89ebcffacd9b8e74d3c598ddf6e3274a69a9bc1c

parent count:
1

message:
docs(command-center): supersede legacy artifact delivery decision

changed paths:
7 exact
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

# 12. post-commit verification

Verify:

1. result commit/tree
2. exact parent `89ebcffacd9b8e74d3c598ddf6e3274a69a9bc1c` / parent count 1
3. exact commit message
4. changed path set exact 7
5. old V1 decision retained but explicitly SUPERSEDED
6. new ZIP-DIRECT-V2 decision present
7. cross-document current delivery semantics are non-conflicting
8. 2200 provenance committed exactly
9. current Cycle/Judgment/Task committed exactly
10. index empty
11. Git-visible worktree clean
12. push/network NOT_RUN

# 13. export bundle + automatic outbound ZIP

Bundle folder:

```text
.aiassistant/reports/target/20260908_2230_aiscc-p2-3-decision-register-artifact-delivery-supersession-reconciliation-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
DECISION_REGISTER_RECONCILIATION_VERIFICATION.md
GIT_PERSISTENCE_VERIFICATION.md
```

After bundle folder completion automatically create:

```text
.aiassistant/reports/target/20260908_2230_aiscc-p2-3-decision-register-artifact-delivery-supersession-reconciliation-1.zip
```

Require:

```text
one top-level bundle directory
readable archive
CRC/integrity PASS
required root files present
folder/archive filename and byte equality
```

Keep folder and outbound ZIP.

# 14. inbound cleanup

At terminal completion, attempt exact current inbound delivery ZIP cleanup best-effort.

Any refusal:

```text
NON_BLOCKING_LOCAL_RESIDUE
```

Do not use broad Downloads cleanup.

# 15. evidence contract

executor_required:

- inbound ZIP bootstrap
- repository/workspace preflight
- 2200 provenance identity
- Decision Register supersession reconciliation
- cross-document authority consistency
- exact 7-path Git persistence
- outbound result ZIP verification
- final provenance/worktree verification

reuse_allowed:

- persisted ZIP-direct workflow at `89ebcffacd9b8e74d3c598ddf6e3274a69a9bc1c`
- 2200 transport/workspace conflict evidence only

human_owned:

```text
new Human QA:
NOT_REQUIRED
```

forbidden:

- P2-3 substantive audit
- scenario implementation/run
- Replay generation
- product/demo source mutation
- Project Source sync
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
INDEX_NOT_EMPTY
DIRTY_WORKSPACE_MIXED
PREDECESSOR_PROVENANCE_IDENTITY_MISMATCH
CANONICAL_AUTHORITY_CONFLICT
DOCUMENT_CONTRACT_MISMATCH
GIT_STAGE_ALLOWLIST_MISMATCH
GIT_COMMIT_VERIFICATION_FAILED
ZIP_EXPORT_FAILED
```

Inbound cleanup refusal after canonical transport is NOT a mandatory blocker.

# 17. final ceiling

Success:

```text
artifact-delivery Decision Register reconciliation:
PERSISTED / READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT

P2-3 source/contract audit:
RETRY_READY / NOT_STARTED

P2-3 implementation:
NOT_STARTED
```

Do not resume the P2-3 audit in this Task.
