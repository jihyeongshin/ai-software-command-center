# 작업지시서: P2-3 Cut B post-persistence state projection correction

## meta

- task_id: `20260912_1510_aiscc-p2-3-cut-b-post-persistence-state-projection-correction-rework-1`
- created_at: `2026-09-12T15:10:44+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `REWORK / STATE_PROJECTION_CORRECTION`
- evidence_profile: `STANDARD`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `fdd3b9ac2f0d8db447ed0ed055aa4b02eab4b30d`
- required_parent: `474826340a89b5c597aa066ff0d414bfc8f43229`
- fresh_ide_executor_chat: `REQUIRED`

# 0. purpose

Correct one Command Center-authored contradiction left by the 1445 persistence Task.

Do not redo Cut B persistence.
Do not amend/revert Commit A or Commit B.
Do not touch environment resources.

Current accepted facts:

```text
Commit A:
474826340a89b5c597aa066ff0d414bfc8f43229
ACCEPTED / PRESERVE

Commit B:
fdd3b9ac2f0d8db447ed0ed055aa4b02eab4b30d
ACCEPTED / PRESERVE

Cut B provisioning:
FINAL_ADMITTED

candidate provenance:
PERSISTED

current projection defect:
PERSISTENCE_IN_PROGRESS label survived after Commit B
```

# 1. inbound transport

Verify exact ZIP filename/SHA from Short Prompt.

Place current Task first:

```text
.aiassistant/tasks/active/20260912_1510_aiscc-p2-3-cut-b-post-persistence-state-projection-correction-rework-1.md
```

Require byte equality and ignored status.

Then place:

```text
.aiassistant/records/aiscc/cycles/20260912_1510_aiscc-p2-3-cut-b-persistence-state-projection-rework-entry-1.cycle.md
SHA-256:
f2094645d1042d54e8e063b97aab7a4fcfb439b2d36142c38def37a42e7fad2e

.aiassistant/reports/aiscc/20260912_1510_aiscc-p2-3-cut-b-persistence-result-state-projection-hold-judgment-1.md
SHA-256:
87c062500d83366e1c3ebbf0413b40ff91cfaa0678307ef524feade32cfe8e88
```

Transport/hash/member failure:

```text
STOP
no Git write
no report/export
no environment action
```

# 2. must-read

Read exact:

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md
.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md
.aiassistant/records/command-center/JUDGMENT_RUBRIC.md
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/tasks/done/20260912_1445_aiscc-p2-3-cut-b-final-admission-git-persistence-and-state-reconciliation-1.md
.aiassistant/records/aiscc/cycles/20260912_1445_aiscc-p2-3-cut-b-final-admission-persistence-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_1445_aiscc-p2-3-cut-b-final-admission-judgment-1.md
.aiassistant/records/aiscc/cycles/20260912_1510_aiscc-p2-3-cut-b-persistence-state-projection-rework-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_1510_aiscc-p2-3-cut-b-persistence-result-state-projection-hold-judgment-1.md
```

# 3. preflight

Require:

```text
branch:
main

HEAD:
fdd3b9ac2f0d8db447ed0ed055aa4b02eab4b30d

HEAD^:
474826340a89b5c597aa066ff0d414bfc8f43229

index:
empty

tracked worktree:
clean
```

Require these exact current hashes before mutation:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `6b7a2cc5af482f1a97e3d7024775eb2441314be567d7289786f52b37af6b65fd`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `7a8dbf5125651378feb27f57c6fe34a62f870d5a5fc34c83620ce65d5f783997`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `3f6fbbc9d979db62210de8581212ddd39815d814658501d4e9fde6f72b57f80d`
- `.aiassistant/tasks/done/20260912_1445_aiscc-p2-3-cut-b-final-admission-git-persistence-and-state-reconciliation-1.md`  `0679c83fd7510a0b5662f9895a009dc55f330f3c933884194a34f3547b7f71ee`
- `.aiassistant/records/aiscc/cycles/20260912_1445_aiscc-p2-3-cut-b-final-admission-persistence-entry-1.cycle.md`  `c14539405ec67c87e19861f9a8e50273b1851e912b8a039ee31867a18774a250`
- `.aiassistant/reports/aiscc/20260912_1445_aiscc-p2-3-cut-b-final-admission-judgment-1.md`  `05e8fefa4f93267a4e539992edf1c79f16c92fd8c2b0b48f57d94b2281184107`

Any mismatch/unrelated dirt:

```text
BASELINE_IDENTITY_MISMATCH or DIRTY_WORKSPACE_MIXED
→ STOP_WITH_REPORT_EXPORT
```

Do not reset/restore/checkout/stash/clean.

# 4. exact correction scope

Modify only:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

Do not modify:

```text
.aiassistant/records/aiscc/DECISION_REGISTER.md
```

It must remain SHA-256:

```text
7a8dbf5125651378feb27f57c6fe34a62f870d5a5fc34c83620ce65d5f783997
```

## CURRENT_STATE_SUMMARY required final semantics

Replace current post-1445 projection so that the current authoritative state says:

```text
P2-3:
IN_PROGRESS

Cut A:
ACCEPTED / PERSISTED

Cut B environment provisioning:
FINAL_ADMITTED / PERSISTED

Cut B candidate image provenance:
admitted / persisted by Commit A 474826340a89b5c597aa066ff0d414bfc8f43229

Cut B candidate DB provenance:
admitted / persisted by Commit A 474826340a89b5c597aa066ff0d414bfc8f43229

Cut B persistence:
COMPLETE

persistence Commit A:
474826340a89b5c597aa066ff0d414bfc8f43229

state reconciliation Commit B:
fdd3b9ac2f0d8db447ed0ed055aa4b02eab4b30d

1400 cleanup:
15 / 15 PASS / REUSED_ACCEPTED

CURRENT_HELPER_1..4:
NON_BLOCKING_LOCAL_RESIDUE
no discovery or cleanup authorization

Cut C:
ENTRY_READY / NOT_STARTED / NOT_AUTHORIZED
separate exact Browser Task required

private S1:
NOT_AUTHORIZED
```

Remove/replace current-authority wording that says:

```text
FINAL_ADMITTED / PERSISTENCE_IN_PROGRESS
NEXT_AFTER_PERSISTENCE
Browser persistence-result review remains HUMAN_PENDING
```

Historical text may remain only when explicitly labeled historical and cannot be mistaken for current authority.

Do not invent a hash for the correction commit inside a file that will be part of that commit.

## NEXT_ACTIONS required final semantics

Current next action:

```text
phase:
P2-3

work_type:
READINESS_BINDING

title:
P2-3 Cut C final readiness binding

status:
ENTRY_READY / NOT_STARTED / NOT_AUTHORIZED

reason:
Cut B is FINAL_ADMITTED / PERSISTED and the 1445 persistence result has been Browser-reviewed.

blocker:
separate exact Cut C authorization Task only

forbidden:
Cut C execution before that Task
private S1 remains NOT_AUTHORIZED
```

Remove Browser persistence review as an outstanding blocker.

# 5. lifecycle and single correction commit

Before Task movement, verify only the two state files are modified plus the two current
Cycle/Judgment are untracked Git-visible governance artifacts.

Move current Task byte-identically:

```text
.aiassistant/tasks/active/20260912_1510_aiscc-p2-3-cut-b-post-persistence-state-projection-correction-rework-1.md
→
.aiassistant/tasks/done/20260912_1510_aiscc-p2-3-cut-b-post-persistence-state-projection-correction-rework-1.md
```

Authorize one exact correction commit with only these five paths:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/records/aiscc/cycles/20260912_1510_aiscc-p2-3-cut-b-persistence-state-projection-rework-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_1510_aiscc-p2-3-cut-b-persistence-result-state-projection-hold-judgment-1.md
.aiassistant/tasks/done/20260912_1510_aiscc-p2-3-cut-b-post-persistence-state-projection-correction-rework-1.md
```

Require staged set exactly `5`.

Commit message:

```text
docs(aiscc): correct P2-3 Cut B persisted state projection
```

Require:

```text
commit parent:
fdd3b9ac2f0d8db447ed0ed055aa4b02eab4b30d

Commit A:
unchanged

Commit B:
unchanged

correction commit:
new child of Commit B

final index:
empty

final tracked worktree:
clean

final Git-visible untracked:
none
```

No amend. No push.

# 6. forbidden

```text
git push
git reset
git restore
git checkout
git stash
git clean
git commit --amend

Docker action of any kind
PostgreSQL action of any kind
image/tag mutation
password/password-file action
candidate provenance JSON rewrite
CURRENT_HELPER_1..4 search/delete
broad filesystem scan

DECISION_REGISTER edit
Cut C execution
private runtime-root creation
S1/S2/S3/S4 execution
Replay generation
deployment
Project Source mirror sync
```

# 7. evidence contract

executor_required:

```text
transport/hash
HEAD/parent/worktree
six critical baseline hashes
two-file exact semantic correction
DECISION_REGISTER unchanged
Task byte-identical active→done
five-path correction commit
final graph/index/worktree
export integrity
```

reuse_allowed:

```text
1445 Commit A/B evidence
Cut B final admission
candidate provenance hashes
1400 cleanup 15/15
```

human_owned:

```text
Browser review of correction result
future Cut C authorization
private S1 authorization
```

not_required:

```text
Docker/DB proof
tests
browser QA
network
credential action
residue cleanup
```

# 8. contract review

Require all 14 rows:

```text
TRANSPORT_PACKAGE_EXACT
HEAD_PARENT_EXACT
BASELINE_CRITICAL_HASHES_EXACT
INDEX_EMPTY_TRACKED_CLEAN
DECISION_REGISTER_UNCHANGED
SUMMARY_ONLY_REQUIRED_SEMANTICS
NEXT_ACTION_ONLY_REQUIRED_SEMANTICS
NO_COMMIT_A_B_REWRITE
CORRECTION_COMMIT_ALLOWLIST_EXACT
TASK_DONE_BYTE_EXACT
FINAL_GRAPH_PARENT_EXACT
FINAL_WORKTREE_CLEAN
NO_ENVIRONMENT_MUTATION
NO_CUTC_NO_S1
```

Require:

```text
14 / 14 PASS
```

# 9. export

Target:

```text
.aiassistant/reports/target/20260912_1510_aiscc-p2-3-cut-b-post-persistence-state-projection-correction-rework-1/
```

Root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
BASELINE_HASH_VERIFICATION.md
STATE_PROJECTION_VERIFICATION.md
COMMIT_PATHS.md
GIT_PERSISTENCE_VERIFICATION.md
CONTRACT_REVIEW.md
```

Also include project-relative copies of the five correction-commit paths.

Expected:

```text
9 root docs
5 canonical copies
14 members total
```

Manifest covers 13 non-self entries with SHA-256 and byte size.

ZIP:

```text
one top-level directory
14 exact members
CRC PASS
folder/archive byte equality
```

# 10. success ceiling

Success means:

```text
Cut B:
FINAL_ADMITTED / PERSISTED

canonical state:
RECONCILED / CURRENT

Cut C:
ENTRY_READY / NOT_STARTED / NOT_AUTHORIZED

private S1:
NOT_AUTHORIZED

P2-3:
IN_PROGRESS
```
