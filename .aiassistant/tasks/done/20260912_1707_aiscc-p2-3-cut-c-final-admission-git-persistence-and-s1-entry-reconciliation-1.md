# 작업지시서: P2-3 Cut C final admission Git persistence + private S1 entry reconciliation

## meta

- task_id: `20260912_1707_aiscc-p2-3-cut-c-final-admission-git-persistence-and-s1-entry-reconciliation-1`
- created_at: `2026-09-12T17:07:07+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `FINAL_ACCEPTANCE_PERSISTENCE / STATE_RECONCILIATION`
- evidence_profile: `HIGH_RISK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `6d41633210f0e556dd4292ee62a8600c6b54215f`
- required_parent: `fdd3b9ac2f0d8db447ed0ed055aa4b02eab4b30d`
- required_grandparent: `474826340a89b5c597aa066ff0d414bfc8f43229`
- fresh_ide_executor_chat: `REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. purpose

Persist Browser-final-admitted Cut C readiness governance and reconcile canonical state for private S1 entry.

This is a **Git/governance persistence Task only**.

Do not touch:

```text
Docker
PostgreSQL
private password file
private runtime root
runtime authority rows
candidate provenance JSON
product/runtime source
```

Do not execute private S1.

1654 runtime evidence is Browser-admitted and reused, not re-executed.

# 1. inbound transport

Verify exact Browser ZIP filename/SHA from Short Prompt.

Place current Task first:

```text
.aiassistant/tasks/active/20260912_1707_aiscc-p2-3-cut-c-final-admission-git-persistence-and-s1-entry-reconciliation-1.md
```

Require byte equality and ignored status.

Then place:

```text
.aiassistant/records/aiscc/cycles/20260912_1707_aiscc-p2-3-cut-c-readiness-final-admission-persistence-entry-1.cycle.md
SHA-256:
df6464dbe707a6df8941f7491e088b7b76ab6fd9c1fb90c203d13f61afece4e1

.aiassistant/reports/aiscc/20260912_1707_aiscc-p2-3-cut-c-readiness-final-acceptance-judgment-1.md
SHA-256:
d96cf397de62caf10c8fb304831f396af76a961acc931f84a87f6595f29c2da9
```

Bootstrap mismatch:

```text
STOP
no Git write
no state mutation
no environment access
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
.aiassistant/records/aiscc/cycles/20260912_1707_aiscc-p2-3-cut-c-readiness-final-admission-persistence-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_1707_aiscc-p2-3-cut-c-readiness-final-acceptance-judgment-1.md
```

Read the twelve predecessor governance artifacts from section 3 only as required to verify their identity/role.
Do not read ignored 1605/1622/1633/1654 helper files.
Do not access the private environment.

# 3. repository baseline

Require:

```text
branch:
main

HEAD:
6d41633210f0e556dd4292ee62a8600c6b54215f

HEAD^:
fdd3b9ac2f0d8db447ed0ed055aa4b02eab4b30d

HEAD^^:
474826340a89b5c597aa066ff0d414bfc8f43229

index:
empty

tracked worktree:
clean
```

Current canonical state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `3be49a5784cdb1d814c65be321c1256f0cd36798e35d9c63c78bd9c5d898b041`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `a17ed3247c88e89cd9ca101fd3944ccb7f2bba01bb1cc4ebc4232aa36c5d5251`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `34ca3d085e6c1b12c73f5a3ff994e71b2189b56e0f10531cb85a6d02ccbbc032`

Before current delivery, Git-visible untracked must be exactly these 12 paths with exact hashes:

- `.aiassistant/tasks/done/20260912_1605_aiscc-p2-3-private-s1-cut-c-final-readiness-binding-1.md`  `de52d47cacb4f45d5f16543e1fecaa517aaf5d2e176123386d69461b52f3c732`
- `.aiassistant/records/aiscc/cycles/20260912_1605_aiscc-p2-3-cut-b-reconciled-cut-c-readiness-entry-1.cycle.md`  `859d10407bc41266968adb08386e5f9a39ee54f3dfeaa0748620e45a57e3b12b`
- `.aiassistant/reports/aiscc/20260912_1605_aiscc-p2-3-cut-b-state-reconciliation-final-acceptance-cut-c-authorization-judgment-1.md`  `bec6679de2659607670bcf13c2fea3f760f369c045413ea666eb0fdb1aff16f2`
- `.aiassistant/tasks/done/20260912_1622_aiscc-p2-3-private-s1-cut-c-postgres-projection-contract-retry-1.md`  `645ea23305463084aed11c4b2eb6536993772a690f6ecba61eb005069d0341fa`
- `.aiassistant/records/aiscc/cycles/20260912_1622_aiscc-p2-3-cut-c-postgres-projection-policy-gap-retry-entry-1.cycle.md`  `6bd67df35b8f6e82f09213e252f64d1d31efdd209b6fdfbef980d4c2eaf1fe37`
- `.aiassistant/reports/aiscc/20260912_1622_aiscc-p2-3-cut-c-postgres-projection-policy-gap-hold-judgment-1.md`  `6f8f1336e4cf5add776a4f756bab4c125ca56e2fb0a50ef80aee4bff7c9a490c`
- `.aiassistant/tasks/done/20260912_1633_aiscc-p2-3-private-s1-cut-c-docker-image-authority-and-public-entrypoint-retry-1.md`  `472d582058c33e1adbe47b60b62fb1f790eaceeceeee37d59a87082e08a17b94`
- `.aiassistant/records/aiscc/cycles/20260912_1633_aiscc-p2-3-cut-c-docker-image-authority-entrypoint-retry-entry-1.cycle.md`  `de18417733a2abb32a7f9e2543a9a7f5ead41f8d82c116b2051402b44b085299`
- `.aiassistant/reports/aiscc/20260912_1633_aiscc-p2-3-cut-c-docker-image-authority-entrypoint-policy-gap-hold-judgment-1.md`  `07937e2486f9f5c2b39801fb3aac16eb8d3599ce7ee1a10d6d7cc928be2f7b3f`
- `.aiassistant/tasks/done/20260912_1654_aiscc-p2-3-private-s1-cut-c-docker-desktop-secret-source-normalization-retry-1.md`  `25cc2abd3e58d89315bdcebc9e2a84d7d06721441ab7a41847ea8f650e90e5c9`
- `.aiassistant/records/aiscc/cycles/20260912_1654_aiscc-p2-3-cut-c-secret-source-representation-retry-entry-1.cycle.md`  `11f4afe011d04432c52df9add6e100f9a93b0452eab9d8835d0dff78b7a74c59`
- `.aiassistant/reports/aiscc/20260912_1654_aiscc-p2-3-cut-c-secret-source-representation-hold-judgment-1.md`  `41ede1e72e2ccde9ca3f3dd1e22bd9faa1bdb26eadb16421967ca4d38c2d2f34`

After current Cycle/Judgment placement while current Task remains active/ignored:

```text
Git-visible untracked:
14 exact

12 predecessor artifacts
current Cycle
current Judgment

index:
empty

tracked:
clean
```

Any extra/missing/hash mismatch:

```text
DIRTY_WORKSPACE_MIXED or BASELINE_IDENTITY_MISMATCH
→ STOP_WITH_REPORT_EXPORT
```

Do not reset/restore/checkout/stash/clean.

# 4. admitted runtime facts — reuse only

Browser Judgment admits the 1654 result.

Persistence may record these facts but must not rerun them:

```text
Cut C readiness:
FINAL_ADMITTED

private secret representation:
DOCKER_DESKTOP_RUN_DESKTOP_MNT_HOST
normalized / private / non-exported

private runtime root:
CREATED / RETAINED / EMPTY

PostgreSQL projection:
867e744367eb804c30db6269d0700d8679c5aeb1a9b6fb78306ce1b87918c8e7

PostgreSQL exported sanitized inspect:
e50fea1be09dd8e2ea44a217c36c08751c94de0d873bb136ef41b2235f9c4b25

public production builder:
aiscc.bootstrap.build_stockroom_production
exactly once

construction-time authority rows:
evidence_requirement_sets 4
evidence_requirements 4
evidence_checkpoints 4
judgment_policies 2
judgment_policy_projections 2

all other application/domain rows:
0

runtime root:
empty after build

S1-S4:
NOT_EXECUTED
```

No private host path/password/credential-bearing URL may be recorded.

# 5. Commit A — persist Cut C governance lineage

Authorize Git write only for exactly these 14 paths:

```text
.aiassistant/tasks/done/20260912_1605_aiscc-p2-3-private-s1-cut-c-final-readiness-binding-1.md
.aiassistant/records/aiscc/cycles/20260912_1605_aiscc-p2-3-cut-b-reconciled-cut-c-readiness-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_1605_aiscc-p2-3-cut-b-state-reconciliation-final-acceptance-cut-c-authorization-judgment-1.md
.aiassistant/tasks/done/20260912_1622_aiscc-p2-3-private-s1-cut-c-postgres-projection-contract-retry-1.md
.aiassistant/records/aiscc/cycles/20260912_1622_aiscc-p2-3-cut-c-postgres-projection-policy-gap-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_1622_aiscc-p2-3-cut-c-postgres-projection-policy-gap-hold-judgment-1.md
.aiassistant/tasks/done/20260912_1633_aiscc-p2-3-private-s1-cut-c-docker-image-authority-and-public-entrypoint-retry-1.md
.aiassistant/records/aiscc/cycles/20260912_1633_aiscc-p2-3-cut-c-docker-image-authority-entrypoint-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_1633_aiscc-p2-3-cut-c-docker-image-authority-entrypoint-policy-gap-hold-judgment-1.md
.aiassistant/tasks/done/20260912_1654_aiscc-p2-3-private-s1-cut-c-docker-desktop-secret-source-normalization-retry-1.md
.aiassistant/records/aiscc/cycles/20260912_1654_aiscc-p2-3-cut-c-secret-source-representation-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_1654_aiscc-p2-3-cut-c-secret-source-representation-hold-judgment-1.md
.aiassistant/records/aiscc/cycles/20260912_1707_aiscc-p2-3-cut-c-readiness-final-admission-persistence-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_1707_aiscc-p2-3-cut-c-readiness-final-acceptance-judgment-1.md
```

Before staging verify every predecessor whole-file SHA plus current Cycle/Judgment SHA.

Use exact-path `git add` only.

Require:

```text
staged:
14 exact
no extra
```

Commit message:

```text
chore(aiscc): persist P2-3 Cut C readiness admission
```

Require:

```text
Commit A parent:
6d41633210f0e556dd4292ee62a8600c6b54215f

Commit A:
created

Commit A changed paths:
14 exact
```

No amend.

# 6. canonical state reconciliation

After Commit A exists, modify only:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

## 6.1 CURRENT_STATE_SUMMARY

Current authority must say at minimum:

```text
P2-3:
IN_PROGRESS

Cut A:
ACCEPTED / PERSISTED

Cut B:
FINAL_ADMITTED / PERSISTED

Cut C:
FINAL_ADMITTED / PERSISTED

Cut C Browser review:
COMPLETED

Cut C persistence governance:
persisted by actual Commit A

private runtime root:
CREATED / RETAINED / EMPTY
absolute path not recorded

private DB authority enrollment:
ESTABLISHED / BOUNDED / RETAINED

scenario execution:
NONE

private S1:
ENTRY_READY / NOT_STARTED / NOT_AUTHORIZED
separate exact Browser Task required
```

Record actual Commit A hash after it exists.

Do not embed the future Commit B hash in any file that Commit B itself contains.

## 6.2 DECISION_REGISTER

Add one new bounded decision entry:

```text
decision_id:
AISCC-P2-3-PRIVATE-S1-CUT-C-READINESS-V1

decision_status:
FINAL_ADMITTED / PERSISTED
```

Record only safe public facts:

```text
Cut C readiness result:
accepted

1654 result ZIP SHA-256:
a8664d010036a59ae2c8e462cd2dc8b8c28b76ce941fadf876c6997685e49bba

production entrypoint:
aiscc.bootstrap.build_stockroom_production

public build count:
1

private source representation class:
DOCKER_DESKTOP_RUN_DESKTOP_MNT_HOST

private runtime root:
retained empty
absolute path omitted

PostgreSQL sanitized projection:
867e744367eb804c30db6269d0700d8679c5aeb1a9b6fb78306ce1b87918c8e7

authority row envelope:
4/4/4 evidence
2/2 judgment
all other application/domain rows 0

scenario execution:
none

next authority:
private S1 exact Task only
```

Reference actual Commit A after creation.

Do not alter unrelated historical decisions except cross-reference if necessary.

## 6.3 NEXT_ACTIONS

Set current immediate next action:

```text
phase:
P2-3

work_type:
PRIVATE_SCENARIO_EXECUTION

title:
P2-3 private S1 normal scenario execution/capture

status:
ENTRY_READY / NOT_STARTED / NOT_AUTHORIZED

reason:
Cut C readiness is FINAL_ADMITTED / PERSISTED.

required authorization:
separate exact Browser-issued S1 Task

scenario:
S1 normal

expected semantic terminal:
ACCEPTED

forbidden before authorization:
prepare_capture
WorkRun
provider/tool execution
scenario Docker dispatch
evidence admission
scenario Judgment
```

Do not mark S1 started or authorized.

# 7. current Task lifecycle + Commit B

After state reconciliation is fully validated, move current Task byte-identically:

```text
.aiassistant/tasks/active/20260912_1707_aiscc-p2-3-cut-c-final-admission-git-persistence-and-s1-entry-reconciliation-1.md
→
.aiassistant/tasks/done/20260912_1707_aiscc-p2-3-cut-c-final-admission-git-persistence-and-s1-entry-reconciliation-1.md
```

Authorize exact-path Git write only for:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/tasks/done/20260912_1707_aiscc-p2-3-cut-c-final-admission-git-persistence-and-s1-entry-reconciliation-1.md
```

Require staged path set:

```text
4 exact
no extra
```

Commit message:

```text
docs(aiscc): reconcile P2-3 Cut C persisted state
```

Require:

```text
Commit B parent:
actual Commit A

Commit B:
created

graph:
6d41633210f0e556dd4292ee62a8600c6b54215f
→ Commit A
→ Commit B

final index:
empty

final tracked worktree:
clean

final Git-visible untracked:
none
```

No push.

# 8. absolute forbidden actions

```text
git push
git reset
git restore
git checkout
git stash
git clean
git commit --amend

Docker CLI/API access
PostgreSQL connection/query
private password file access
private runtime-root access
filesystem search for private paths
runtime authority row mutation
candidate provenance JSON mutation
source/config/test mutation

prepare_capture
S1/S2/S3/S4
WorkRun
provider/tool execution
scenario Docker execution
HumanResult
scenario Judgment
Replay
deployment
```

# 9. contract review

Require exactly 22 rows:

```text
TRANSPORT_PACKAGE_EXACT
BASE_HEAD_PARENT_EXACT
BASELINE_STATE_HASHES_EXACT
PRE_DELIVERY_UNTRACKED_12_EXACT
POST_DELIVERY_UNTRACKED_14_EXACT
INDEX_TRACKED_CLEAN_PREWRITE
COMMIT_A_ALLOWLIST_14_EXACT
COMMIT_A_PARENT_EXACT
COMMIT_A_CREATED
COMMIT_A_PATH_SET_EXACT
THREE_STATE_OWNER_RECONCILIATION_EXACT
RUNTIME_READINESS_FACTS_REUSED_ONLY
NO_PRIVATE_RESOURCE_ACCESS
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
COMMIT_B_ALLOWLIST_4_EXACT
COMMIT_B_PARENT_COMMIT_A
COMMIT_B_CREATED
FINAL_GRAPH_EXACT
FINAL_INDEX_TRACKED_UNTRACKED_CLEAN
NO_DOCKER_DB_RUNTIME_ROOT_MUTATION
NO_S1_S4_EXECUTION
NO_PUSH
```

Require:

```text
22 / 22 PASS
```

# 10. success export

Target:

```text
.aiassistant/reports/target/20260912_1707_aiscc-p2-3-cut-c-final-admission-git-persistence-and-s1-entry-reconciliation-1/
```

Root documents exactly 10:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
BASELINE_HASH_VERIFICATION.md
COMMIT_A_PATHS.md
STATE_RECONCILIATION_VERIFICATION.md
COMMIT_B_PATHS.md
GIT_PERSISTENCE_VERIFICATION.md
CONTRACT_REVIEW.md
```

Also include byte-preserving project-relative copies of all:

```text
14 Commit A paths
4 Commit B paths
```

Expected success export:

```text
28 total members
27 non-self manifest rows
one top-level directory
CRC PASS
folder/archive byte equality
TASK.md == current canonical done Task
```

Do not include:

```text
1654 result ZIP
ignored helper scripts
runtime/private files
raw Docker inspect
DB dumps
private paths
credentials
```

# 11. mandatory stop

Stop with bounded report/export after:

```text
baseline mismatch
unexpected Git-visible path
unexpected staged path
commit failure
state edit outside three exact owners
private/runtime access attempted
S1 execution attempted
```

Do not broaden scope.

# 12. success ceiling

```text
Cut C:
FINAL_ADMITTED / PERSISTED

canonical state:
RECONCILED

private S1:
ENTRY_READY / NOT_STARTED / NOT_AUTHORIZED

S1 execution:
NOT_PERFORMED

P2-3:
IN_PROGRESS
```
