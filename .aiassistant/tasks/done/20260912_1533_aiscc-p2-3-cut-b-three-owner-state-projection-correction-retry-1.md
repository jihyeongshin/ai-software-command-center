# 작업지시서: P2-3 Cut B three-owner state projection correction retry

## meta

- task_id: `20260912_1533_aiscc-p2-3-cut-b-three-owner-state-projection-correction-retry-1`
- created_at: `2026-09-12T15:33:16+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `REWORK / AUTHORITY_SCOPE_CORRECTION`
- evidence_profile: `STANDARD`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `fdd3b9ac2f0d8db447ed0ed055aa4b02eab4b30d`
- required_parent: `474826340a89b5c597aa066ff0d414bfc8f43229`
- fresh_ide_executor_chat: `FORBIDDEN`
- executor_session_action: `KEEP_EXISTING_1510_IDE_EXECUTOR_CHAT`
- reason: `1510 stopped on an authority conflict discovered in that same executor session; no private hidden path authority is required`

# 0. purpose

Resolve the policy conflict that correctly stopped 1510.

This retry expands the exact canonical correction owner set from two files to three:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

Do not redo 1445 persistence.
Do not rebuild/reprovision/restart any environment.
Do not execute Cut C or private S1.

# 1. inbound transport

Continue in the existing 1510 IDE Executor chat.

Verify Browser ZIP filename/SHA-256 from the Short Prompt.

Place this Task first:

```text
.aiassistant/tasks/active/20260912_1533_aiscc-p2-3-cut-b-three-owner-state-projection-correction-retry-1.md
```

Require byte equality and ignored status.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260912_1533_aiscc-p2-3-cut-b-state-projection-policy-conflict-retry-entry-1.cycle.md
SHA-256:
c794077b7798b4e02f0278b00ed04e56ac25f88c95e7876d1d23a70def853ed9

.aiassistant/reports/aiscc/20260912_1533_aiscc-p2-3-cut-b-state-projection-policy-conflict-hold-judgment-1.md
SHA-256:
19363d54b86ca3da75f724de65048bfcc21a3158a9ba6193085c94beb62f56dd
```

Any ZIP/hash/archive/current Task bootstrap mismatch:

```text
STOP
no Git write
no state mutation
no environment action
no report/export
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
.aiassistant/tasks/active/20260912_1510_aiscc-p2-3-cut-b-post-persistence-state-projection-correction-rework-1.md
.aiassistant/records/aiscc/cycles/20260912_1510_aiscc-p2-3-cut-b-persistence-state-projection-rework-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_1510_aiscc-p2-3-cut-b-persistence-result-state-projection-hold-judgment-1.md
.aiassistant/records/aiscc/cycles/20260912_1533_aiscc-p2-3-cut-b-state-projection-policy-conflict-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_1533_aiscc-p2-3-cut-b-state-projection-policy-conflict-hold-judgment-1.md
```

Do not bulk-read unrelated source/logs.

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

Require exact current state hashes:

```text
CURRENT_STATE_SUMMARY.md:
6b7a2cc5af482f1a97e3d7024775eb2441314be567d7289786f52b37af6b65fd

DECISION_REGISTER.md:
7a8dbf5125651378feb27f57c6fe34a62f870d5a5fc34c83620ce65d5f783997

NEXT_ACTIONS.md:
3f6fbbc9d979db62210de8581212ddd39815d814658501d4e9fde6f72b57f80d
```

Require predecessor active Task:

```text
.aiassistant/tasks/active/20260912_1510_aiscc-p2-3-cut-b-post-persistence-state-projection-correction-rework-1.md

SHA-256:
c73b8f6e45e08e7bbc0d759a420b125aa7c3d4df2bac894a33811367e4949376

ignored:
Yes
```

Require the two pre-existing 1510 Git-visible untracked artifacts and no other Git-visible untracked path before current delivery:

```text
.aiassistant/records/aiscc/cycles/20260912_1510_aiscc-p2-3-cut-b-persistence-state-projection-rework-entry-1.cycle.md
SHA-256:
f2094645d1042d54e8e063b97aab7a4fcfb439b2d36142c38def37a42e7fad2e

.aiassistant/reports/aiscc/20260912_1510_aiscc-p2-3-cut-b-persistence-result-state-projection-hold-judgment-1.md
SHA-256:
87c062500d83366e1c3ebbf0413b40ff91cfaa0678307ef524feade32cfe8e88
```

After current Cycle/Judgment placement, require Git-visible untracked set exactly four:

```text
previous 1510 Cycle
previous 1510 Judgment
current 1533 Cycle
current 1533 Judgment
```

Both active Tasks are ignored and must exist byte-exact.

Any extra/missing/differing path:

```text
DIRTY_WORKSPACE_MIXED or BASELINE_IDENTITY_MISMATCH
→ STOP_WITH_REPORT_EXPORT
```

Do not reset/restore/checkout/stash/clean.

# 4. predecessor blocked Task lifecycle closure

The 1510 executor turn is complete with blocked-result export.

This retry explicitly supersedes its Task-local "do not move unless correction succeeds" lifecycle condition.

Move byte-identically:

```text
.aiassistant/tasks/active/20260912_1510_aiscc-p2-3-cut-b-post-persistence-state-projection-correction-rework-1.md
→
.aiassistant/tasks/done/20260912_1510_aiscc-p2-3-cut-b-post-persistence-state-projection-correction-rework-1.md
```

Require done SHA-256:

```text
c73b8f6e45e08e7bbc0d759a420b125aa7c3d4df2bac894a33811367e4949376
```

Do not edit its bytes.

# 5. three-owner exact state correction

Modify only these three canonical state files:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

No other tracked file modification is authorized.

## 5.1 CURRENT_STATE_SUMMARY

Current authoritative projection must say:

```text
P2-3:
IN_PROGRESS

Cut A:
ACCEPTED / PERSISTED

Cut B environment provisioning:
FINAL_ADMITTED / PERSISTED

Cut B candidate image provenance:
ADMITTED / PERSISTED

Cut B candidate DB provenance:
ADMITTED / PERSISTED

Cut B persistence:
COMPLETE

persistence Commit A:
474826340a89b5c597aa066ff0d414bfc8f43229

state reconciliation Commit B:
fdd3b9ac2f0d8db447ed0ed055aa4b02eab4b30d

1400 cleanup:
15 / 15 PASS / REUSED_ACCEPTED

1510 projection retry:
BLOCKED_POLICY_CONFLICT / NO_MUTATION

CURRENT_HELPER_1..4:
NON_BLOCKING_LOCAL_RESIDUE
no discovery or cleanup authorization

1445 persistence-result Browser review:
COMPLETED

Cut C:
ENTRY_READY / NOT_STARTED / NOT_AUTHORIZED
separate exact Browser Task required

private S1:
NOT_AUTHORIZED
```

Remove current-authority wording that still presents:

```text
FINAL_ADMITTED / PERSISTENCE_IN_PROGRESS
NEXT_AFTER_PERSISTENCE
Browser persistence-result review HUMAN_PENDING
```

Historical sections may retain historical text only when clearly labeled historical.

Do not embed the unknown hash of the correction commit into a file that is part of that commit.

## 5.2 DECISION_REGISTER

Update only the latest entry:

```text
AISCC-P2-3-PRIVATE-S1-CUT-B-ENVIRONMENT-PROVISIONING-V1
```

Preserve its existing resource/provenance identities and hashes.

Resolve the stale current-looking fields so the entry says semantically:

```text
decision_status:
FINAL_ADMITTED / PROVENANCE_PERSISTED

persistence result Browser review:
COMPLETED

persistence mechanics:
ACCEPTED / Commit A and Commit B PRESERVED

1510 state projection retry:
BLOCKED_POLICY_CONFLICT / NO_MUTATION

current next action:
Cut C final readiness binding under a separate exact Browser Task

authorization boundary:
Cut C ENTRY_READY / NOT_STARTED / NOT_AUTHORIZED
private S1 NOT_AUTHORIZED
P2-3 IN_PROGRESS

residue:
CURRENT_HELPER_1..4 remains NON_BLOCKING_LOCAL_RESIDUE
not an authorization for discovery/cleanup
```

Add provenance refs for the 1510 blocked Task/Cycle/Judgment and current retry Cycle/Judgment as appropriate.

The earlier fields:

```text
only after persistence review
NEXT_AFTER_PERSISTENCE
persistence-result Browser review HUMAN_PENDING
```

must no longer be current authority.

Do not modify unrelated earlier decision entries.

## 5.3 NEXT_ACTIONS

Current next action must say:

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
Cut B is FINAL_ADMITTED / PERSISTED.
The 1445 persistence result has been Browser-reviewed.
The 1510 authority conflict is resolved by the explicit three-owner correction contract.

blocker:
separate exact Cut C authorization Task only

forbidden:
Cut C execution before that Task
private S1 remains NOT_AUTHORIZED
```

Remove Browser persistence review as an outstanding blocker.

# 6. current Task lifecycle

After all exact state validation succeeds, move current Task byte-identically:

```text
.aiassistant/tasks/active/20260912_1533_aiscc-p2-3-cut-b-three-owner-state-projection-correction-retry-1.md
→
.aiassistant/tasks/done/20260912_1533_aiscc-p2-3-cut-b-three-owner-state-projection-correction-retry-1.md
```

# 7. single exact correction commit

Authorize one commit containing exactly these nine paths:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/tasks/done/20260912_1510_aiscc-p2-3-cut-b-post-persistence-state-projection-correction-rework-1.md
.aiassistant/records/aiscc/cycles/20260912_1510_aiscc-p2-3-cut-b-persistence-state-projection-rework-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_1510_aiscc-p2-3-cut-b-persistence-result-state-projection-hold-judgment-1.md
.aiassistant/records/aiscc/cycles/20260912_1533_aiscc-p2-3-cut-b-state-projection-policy-conflict-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_1533_aiscc-p2-3-cut-b-state-projection-policy-conflict-hold-judgment-1.md
.aiassistant/tasks/done/20260912_1533_aiscc-p2-3-cut-b-three-owner-state-projection-correction-retry-1.md
```

Require staged path set:

```text
9 exact
no extra
```

Commit message:

```text
docs(aiscc): reconcile P2-3 Cut B post-persistence authority
```

Require:

```text
parent:
fdd3b9ac2f0d8db447ed0ed055aa4b02eab4b30d

Commit A:
474826340a89b5c597aa066ff0d414bfc8f43229
unchanged

Commit B:
fdd3b9ac2f0d8db447ed0ed055aa4b02eab4b30d
unchanged

new correction commit:
one child of Commit B

final index:
empty

final tracked worktree:
clean

final Git-visible untracked:
none
```

No amend. No push.

# 8. absolute forbidden actions

Do not:

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

product/runtime source modification
Cut C execution
private runtime-root creation
S1/S2/S3/S4 execution
Replay generation
deployment
Project Source mirror sync
```

# 9. evidence contract

executor_required:

```text
transport/hash/member verification
HEAD/parent/index/tracked cleanliness
three state baseline hashes
pre-existing 1510 artifact identity
predecessor active Task identity
predecessor active→done byte equality
three-owner state correction
current active→done byte equality
nine-path staged/commit allowlist
commit parent/graph/final cleanliness
export integrity
```

reuse_allowed:

```text
1445 Commit A/B persistence evidence
Cut B final admission
1400 cleanup 15/15
1510 executed preflight evidence
```

human_owned:

```text
Browser review of this retry result
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
local residue cleanup
```

forbidden:

```text
all section 8 actions
```

# 10. contract review

Require all 16 rows:

```text
TRANSPORT_PACKAGE_EXACT
HEAD_PARENT_EXACT
BASELINE_THREE_STATE_HASHES_EXACT
PREEXISTING_1510_ARTIFACTS_EXACT
PREDECESSOR_ACTIVE_TASK_EXACT
PREDECESSOR_ACTIVE_TO_DONE_BYTE_EXACT
CURRENT_ARTIFACTS_EXACT
THREE_OWNER_STATE_SEMANTICS_EXACT
DECISION_REGISTER_PENDING_FIELDS_RESOLVED
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
CORRECTION_COMMIT_ALLOWLIST_EXACT
CORRECTION_COMMIT_PARENT_EXACT
COMMIT_A_B_UNCHANGED
FINAL_INDEX_TRACKED_UNTRACKED_CLEAN
NO_ENVIRONMENT_MUTATION
NO_CUTC_NO_S1
```

Require:

```text
16 / 16 PASS
```

Do not add/remove a row without changing both the list and required count.

# 11. export

Target:

```text
.aiassistant/reports/target/20260912_1533_aiscc-p2-3-cut-b-three-owner-state-projection-correction-retry-1/
```

Root documents:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
BASELINE_HASH_VERIFICATION.md
SUPERSEDED_TASK_VERIFICATION.md
STATE_PROJECTION_VERIFICATION.md
COMMIT_PATHS.md
GIT_PERSISTENCE_VERIFICATION.md
CONTRACT_REVIEW.md
```

Also include byte-preserving project-relative copies of all nine correction-commit paths.

Expected success export:

```text
10 root docs
9 canonical copies
19 members total
```

Manifest covers all 18 non-self entries with SHA-256 and byte size.

ZIP:

```text
one top-level directory
19 exact members
CRC PASS
folder/archive byte equality
```

Blocked result may contain fewer canonical copies only when those artifacts genuinely do not exist.
Do not fabricate missing success artifacts.

# 12. mandatory stop

Stop with minimal report/export after:

```text
transport mismatch
baseline mismatch
unexpected Git-visible path
policy conflict outside this explicit three-owner correction
unexpected staged path
commit failure
secret/private-path export finding
```

After stop, do not broaden scope.

# 13. success ceiling

Success means only:

```text
Cut B:
FINAL_ADMITTED / PERSISTED

three-owner current state:
RECONCILED

1510 blocked provenance:
PERSISTED

Cut C:
ENTRY_READY / NOT_STARTED / NOT_AUTHORIZED

private S1:
NOT_AUTHORIZED

P2-3:
IN_PROGRESS
```
