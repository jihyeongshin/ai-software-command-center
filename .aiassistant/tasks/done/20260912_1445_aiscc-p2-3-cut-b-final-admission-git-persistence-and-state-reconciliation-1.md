# 작업지시서: P2-3 Cut B final admission Git persistence + state reconciliation

## meta

- task_id: `20260912_1445_aiscc-p2-3-cut-b-final-admission-git-persistence-and-state-reconciliation-1`
- created_at: `2026-09-12T14:45:48+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `FINAL_ACCEPTANCE_PERSISTENCE / STATE_RECONCILIATION`
- evidence_profile: `HIGH_RISK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `0fe2105f35b4fcf9769ae76361cb42b47220ac7d`
- required_tree: `a46a8816acc34214983925fe02ed77df55f6b909`
- required_parent: `750c37aecb4c264f66aabf12dedb8d54e20a7f95`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `Cut B runtime candidate final admission → separate Git persistence/state authority boundary`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. purpose

Persist the Browser-final-admitted Cut B provisioning lineage and sanitized candidate provenance,
then reconcile canonical state for Cut C entry.

Do not rebuild/reprovision/restart the retained environment.
Do not execute Cut C or private S1.
Do not search for or delete `CURRENT_HELPER_1..4`.

The four current-turn helper residues from 1400 are:

```text
NON_BLOCKING_LOCAL_RESIDUE / OPERATIONAL_HOUSEKEEPING
```

They are outside this Task's substantive gate and must not be rediscovered by broad filesystem scan.

# 1. inbound transport

Verify Browser ZIP filename/SHA-256 from the Short Prompt.

Place current Task first:

```text
.aiassistant/tasks/active/20260912_1445_aiscc-p2-3-cut-b-final-admission-git-persistence-and-state-reconciliation-1.md
```

Require byte-exact and ignored.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260912_1445_aiscc-p2-3-cut-b-final-admission-persistence-entry-1.cycle.md
SHA-256:
c14539405ec67c87e19861f9a8e50273b1851e912b8a039ee31867a18774a250

.aiassistant/reports/aiscc/20260912_1445_aiscc-p2-3-cut-b-final-admission-judgment-1.md
SHA-256:
05e8fefa4f93267a4e539992edf1c79f16c92fd8c2b0b48f57d94b2281184107
```

Any ZIP/hash/member/TASK bootstrap mismatch:

```text
STOP
no Git write
no environment mutation
no report/export
```

# 2. canonical rules / must-read

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
.aiassistant/records/aiscc/cycles/20260912_1445_aiscc-p2-3-cut-b-final-admission-persistence-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_1445_aiscc-p2-3-cut-b-final-admission-judgment-1.md
```

Do not bulk-read unrelated source/logs.

# 3. repository preflight

Require:

```text
branch:
main

HEAD:
0fe2105f35b4fcf9769ae76361cb42b47220ac7d

HEAD tree:
a46a8816acc34214983925fe02ed77df55f6b909

HEAD^:
750c37aecb4c264f66aabf12dedb8d54e20a7f95

index:
empty

tracked worktree:
clean
```

Before current delivery, require exactly 17 Git-visible paths and these whole-file hashes:

- `.aiassistant/records/aiscc/cycles/20260912_0259_aiscc-p2-3-cut-a-persisted-cut-b-environment-provisioning-entry-1.cycle.md`  `2da742f803b402b39f0433a0e1fabb74c8a594b93cd782555797b05d18cfc9c2`
- `.aiassistant/reports/aiscc/20260912_0259_aiscc-p2-3-cut-a-persistence-final-acceptance-cut-b-authorization-judgment-1.md`  `d64582a0a3b7040cf4a56961d7905b194949716eda98e9832a66a1c68996629d`
- `.aiassistant/tasks/done/20260912_0259_aiscc-p2-3-private-s1-cut-b-environment-provisioning-1.md`  `46b9fb7d030053eb12ac75827475ab136c12cb51b83e3a82b5516b7feee80b96`
- `.aiassistant/records/aiscc/cycles/20260912_0348_aiscc-p2-3-cut-b-artifact-hash-correction-provisioning-retry-entry-1.cycle.md`  `f8e7614602db171c3059ba279548a02252ccefb9e2eeb7d86d4fcb602dcf38f0`
- `.aiassistant/reports/aiscc/20260912_0348_aiscc-p2-3-cut-b-artifact-hash-contract-defect-retry-judgment-1.md`  `813bcdcfd13d8e4164bc09761d56ce30e5dc49a54c81d6928011df8bd19c657b`
- `.aiassistant/tasks/done/20260912_0348_aiscc-p2-3-private-s1-cut-b-artifact-hash-correction-provisioning-retry-1.md`  `dd82f0087a4c93131012a0bf6955c3e78116d39fae11dd79bee3818849589a1b`
- `.aiassistant/records/aiscc/cycles/20260912_0410_aiscc-p2-3-cut-b-self-reference-corrected-provisioning-retry-entry-1.cycle.md`  `93f5b7dc5ff55ee7dfe212c79a53e0e7cc1d05b7aafbda7b39f7523947ec8fdc`
- `.aiassistant/reports/aiscc/20260912_0410_aiscc-p2-3-cut-b-self-reference-contract-defect-retry-judgment-1.md`  `78f4ec2f7feb8fac541eb7c258bf39eb359515c4a565a1c4edf0bd4c491618a1`
- `.aiassistant/tasks/done/20260912_0410_aiscc-p2-3-private-s1-cut-b-self-reference-correction-provisioning-retry-1.md`  `9bc85a68c11d56d533923b605a029671365304ba729f17fedbeede1577ceccac`
- `.aiassistant/records/aiscc/cycles/20260912_0420_aiscc-p2-3-cut-b-clean-authority-provisioning-retry-entry-1.cycle.md`  `d3ba1c85183e6e594eccee45eb0d51a141260e0ac10b6e7fe9efd81d7325c50a`
- `.aiassistant/reports/aiscc/20260912_0420_aiscc-p2-3-cut-b-historical-baseline-path-mismatch-retry-judgment-1.md`  `cd5ee11d34d5711de6e8e1ce24aece0bb58ee731febc8516c86c3be24b49a603`
- `.aiassistant/tasks/done/20260912_0420_aiscc-p2-3-private-s1-cut-b-clean-authority-provisioning-retry-1.md`  `424bcebe4a9994db0ad09898452cda9c09537f95f93bee0a47b5164f4b7b7754`
- `.aiassistant/records/aiscc/runtime/stockroom-image-provenance.v1.json`  `e19f2b645aee85878bed7c557064bbbd0be746524f394ad88de1d2509c13b64f`
- `.aiassistant/records/aiscc/runtime/stockroom-private-postgres-provisioning.v1.json`  `36b9c93515223ade3d74923141fcbe823907b42b81e5d86bf3666a4f02032b54`
- `.aiassistant/records/aiscc/cycles/20260912_1400_aiscc-p2-3-cut-b-provisioned-candidate-temporary-cleanup-entry-1.cycle.md`  `8fb368a5fe226e72741b787cb3b2263d991705b4c699cd46491162004f50f200`
- `.aiassistant/reports/aiscc/20260912_1400_aiscc-p2-3-cut-b-provisioning-candidate-cleanup-hold-judgment-1.md`  `5173a486423cdfa02ec45327216ac1a7a6eb111dd1548a0b10145735c4cda176`
- `.aiassistant/tasks/done/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md`  `52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb`

After current Cycle/Judgment placement while current Task is active:

```text
Git-visible:
19 exact

current active Task:
exists byte-exact
ignored

index:
empty
```

No duplicate/extra Git-visible path.

Canonical state at required HEAD must start with exact hashes:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
01c6f173737924d0fb0fd9deb0c5b66ea78fec499841aa76a61c2b781c17cc65

.aiassistant/records/aiscc/DECISION_REGISTER.md
5ff255dfb6a276d9755cea8af564b0882a9546e97e511e2d0028cada625a171e

.aiassistant/records/aiscc/NEXT_ACTIONS.md
f2004f24ea0ef369702df1f3a0dff2efa9d27642fdff62c816f536d347cff581
```

Any mismatch or unrelated dirt:

```text
DIRTY_WORKSPACE_MIXED or BASELINE_IDENTITY_MISMATCH
→ STOP_WITH_REPORT_EXPORT
```

Do not reset/restore/checkout/stash/clean unrelated files.

# 4. admitted predecessor evidence

Browser final judgment admits:

```text
0420 provisioning evidence:
accepted

1400 cleanup contract:
15 / 15 PASS

Cut B provisioning candidate:
FINAL_ADMITTED
```

Do not rerun Docker, PostgreSQL, migrations, restart probe, image build, or S1 merely to refill evidence.

Reuse is allowed only for exact unchanged candidate hashes:

```text
stockroom-image-provenance.v1.json:
e19f2b645aee85878bed7c557064bbbd0be746524f394ad88de1d2509c13b64f

stockroom-private-postgres-provisioning.v1.json:
36b9c93515223ade3d74923141fcbe823907b42b81e5d86bf3666a4f02032b54
```

# 5. Commit A — persist admitted Cut B provenance

Git write is authorized only for the exact 19-path allowlist below:

```text
.aiassistant/records/aiscc/cycles/20260912_0259_aiscc-p2-3-cut-a-persisted-cut-b-environment-provisioning-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_0259_aiscc-p2-3-cut-a-persistence-final-acceptance-cut-b-authorization-judgment-1.md
.aiassistant/tasks/done/20260912_0259_aiscc-p2-3-private-s1-cut-b-environment-provisioning-1.md
.aiassistant/records/aiscc/cycles/20260912_0348_aiscc-p2-3-cut-b-artifact-hash-correction-provisioning-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_0348_aiscc-p2-3-cut-b-artifact-hash-contract-defect-retry-judgment-1.md
.aiassistant/tasks/done/20260912_0348_aiscc-p2-3-private-s1-cut-b-artifact-hash-correction-provisioning-retry-1.md
.aiassistant/records/aiscc/cycles/20260912_0410_aiscc-p2-3-cut-b-self-reference-corrected-provisioning-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_0410_aiscc-p2-3-cut-b-self-reference-contract-defect-retry-judgment-1.md
.aiassistant/tasks/done/20260912_0410_aiscc-p2-3-private-s1-cut-b-self-reference-correction-provisioning-retry-1.md
.aiassistant/records/aiscc/cycles/20260912_0420_aiscc-p2-3-cut-b-clean-authority-provisioning-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_0420_aiscc-p2-3-cut-b-historical-baseline-path-mismatch-retry-judgment-1.md
.aiassistant/tasks/done/20260912_0420_aiscc-p2-3-private-s1-cut-b-clean-authority-provisioning-retry-1.md
.aiassistant/records/aiscc/runtime/stockroom-image-provenance.v1.json
.aiassistant/records/aiscc/runtime/stockroom-private-postgres-provisioning.v1.json
.aiassistant/records/aiscc/cycles/20260912_1400_aiscc-p2-3-cut-b-provisioned-candidate-temporary-cleanup-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_1400_aiscc-p2-3-cut-b-provisioning-candidate-cleanup-hold-judgment-1.md
.aiassistant/tasks/done/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
.aiassistant/records/aiscc/cycles/20260912_1445_aiscc-p2-3-cut-b-final-admission-persistence-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_1445_aiscc-p2-3-cut-b-final-admission-judgment-1.md
```

Before staging, verify each baseline path remains byte-exact and current Cycle/Judgment match their expected SHA.

Perform exact-path `git add` only for those 19 paths.

Require staged path set:

```text
19 exact
no extra
```

Create Commit A with message:

```text
chore(aiscc): persist P2-3 Cut B admission provenance
```

Require:

```text
Commit A parent:
0fe2105f35b4fcf9769ae76361cb42b47220ac7d

Commit A:
created

Commit A changed-path set:
19 exact
```

No amend.

# 6. canonical state reconciliation

After Commit A, edit only:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

Required semantic reconciliation:

## CURRENT_STATE_SUMMARY

Record at minimum:

```text
P2-3:
IN_PROGRESS

Cut A:
ACCEPTED / PERSISTED

Cut B environment provisioning:
FINAL_ADMITTED / PERSISTENCE_IN_PROGRESS

Cut B candidate image provenance:
admitted / persisted by Commit A

Cut B candidate DB provenance:
admitted / persisted by Commit A

1400 cleanup:
15 / 15 PASS

CURRENT_HELPER_1..4:
NON_BLOCKING_LOCAL_RESIDUE
not a Cut B admission blocker

Cut C:
NEXT_AFTER_PERSISTENCE
not yet executed

private S1:
NOT_AUTHORIZED
```

Include actual Commit A hash after it exists.

## DECISION_REGISTER

Add one bounded decision entry for Cut B private environment provisioning.

Preserve:

```text
image ID:
sha256:c51ad05852b58a3b4fd275ee88d183551e745d79ac8239e3da3b98372fe0bb9e

discovery tag:
aiscc-stockroom-runtime:p2-3-private-v1

PostgreSQL container:
aiscc-p2-3-private-postgres-v1

PostgreSQL volume:
aiscc-p2-3-private-postgres-data-v1

loopback endpoint:
127.0.0.1:55432

migration head:
20260901_0008

candidate provenance hashes:
e19f2b645aee85878bed7c557064bbbd0be746524f394ad88de1d2509c13b64f
36b9c93515223ade3d74923141fcbe823907b42b81e5d86bf3666a4f02032b54
```

Do not record private password value or literal private host paths.

Record that 1400 current-helper residue is non-blocking and not an authorization for broad cleanup.

## NEXT_ACTIONS

Advance the immediate P2-3 action to:

```text
Cut C:
final readiness binding
private runtime-root creation/authority
admitted provenance references
production resolver/readiness verification
```

Do not mark Cut C started.

Do not select private S1 directly before Cut C.

# 7. Task lifecycle + Commit B

After state reconciliation and all checks required before Task movement:

Move byte-identically:

```text
.aiassistant/tasks/active/20260912_1445_aiscc-p2-3-cut-b-final-admission-git-persistence-and-state-reconciliation-1.md
→
.aiassistant/tasks/done/20260912_1445_aiscc-p2-3-cut-b-final-admission-git-persistence-and-state-reconciliation-1.md
```

Git write is authorized only for these four paths:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/tasks/done/20260912_1445_aiscc-p2-3-cut-b-final-admission-git-persistence-and-state-reconciliation-1.md
```

Perform exact-path `git add` only for those four.

Require staged set:

```text
4 exact
no extra
```

Create Commit B with message:

```text
docs(aiscc): reconcile P2-3 Cut B persisted state
```

Require:

```text
Commit B parent:
actual Commit A

Commit B:
created

Commit graph:
required_HEAD
→ Commit A
→ Commit B

final index:
empty

final tracked worktree:
clean

final untracked Git-visible governance/candidate paths:
none
```

No push.

# 8. absolute forbidden actions

Do not:

```text
git push
git reset
git restore
git checkout
git stash
git clean

Docker build/pull/run/remove/prune
PostgreSQL restart/reprovision/migration
password rotation or password-file mutation
candidate JSON rewrite
CURRENT_HELPER_1..4 discovery/deletion
broad temp cleanup
filesystem broad scan

Cut C execution
private runtime-root creation
private S1/S2/S3/S4 execution
Replay generation
public runtime/deployment
Project Source mirror sync
```

# 9. evidence contract

executor_required:

```text
transport/hash/member bootstrap
repository preflight
17 baseline hashes
19 post-delivery visible-set identity
Commit A exact allowlist/pathset/parent
three-file canonical state reconciliation
Task active→done byte equality
Commit B exact allowlist/pathset/parent
final graph/index/worktree
export integrity
```

reuse_allowed:

```text
0420 provisioning evidence
1400 cleanup 15/15
Browser final admission Judgment
```

human_owned:

```text
Browser review of persistence result
Cut C authorization
private S1 authorization
```

not_required:

```text
Docker/DB runtime re-proof
test suite
browser QA
network
credential action
cleanup of 1400 current helpers
```

forbidden:

```text
all actions in section 8
```

# 10. persistence contract review

Require all 20 rows:

```text
TRANSPORT_PACKAGE_EXACT
BASE_HEAD_TREE_PARENT_EXACT
BASELINE_17_HASHES_EXACT
PRE_DELIVERY_VISIBLE_SET_17_EXACT
POST_DELIVERY_VISIBLE_SET_19_EXACT
INDEX_EMPTY_PREWRITE
COMMIT_A_ALLOWLIST_EXACT
COMMIT_A_PARENT_EXACT
COMMIT_A_CREATED
COMMIT_A_PATH_SET_EXACT
STATE_RECONCILIATION_ONLY_3
TASK_DONE_BYTE_EXACT
COMMIT_B_ALLOWLIST_EXACT
COMMIT_B_PARENT_COMMIT_A
COMMIT_B_CREATED
COMMIT_GRAPH_EXACT
FINAL_WORKTREE_CLEAN
NO_ENVIRONMENT_MUTATION
NO_EXTERNAL_RESIDUE_CLEANUP
NO_PUSH_NO_CUTC_NO_S1
```

Require:

```text
20 / 20 PASS
```

The row count above is semantic-contract generated and must equal the actual listed row count.
Do not add an extra row without changing both the list and required count.

# 11. required export

Folder:

```text
.aiassistant/reports/target/20260912_1445_aiscc-p2-3-cut-b-final-admission-git-persistence-and-state-reconciliation-1/
```

Root documents:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
BASELINE_HASH_VERIFICATION.md
COMMIT_A_PATHS.md
COMMIT_B_PATHS.md
GIT_PERSISTENCE_VERIFICATION.md
STATE_RECONCILIATION_VERIFICATION.md
CONTRACT_REVIEW.md
```

Also include byte-preserving project-relative copies of:

```text
all 19 Commit A paths
all 4 Commit B paths
```

Expected:

```text
10 root docs
23 canonical copies
33 members total
```

`EXPORT_MANIFEST.md` covers all 32 non-self entries with SHA-256 and byte size.

Create adjacent ZIP with:

```text
one top-level directory
33 exact members
CRC PASS
folder/archive byte equality
```

Secret/private-path scan must reject:

```text
private password value
database URL containing credential
private password host path
temporary build-context literal path
temporary helper literal host paths
```

# 12. mandatory stop

Stop with minimal evidence/report/export after:

```text
transport mismatch
baseline identity mismatch
DIRTY_WORKSPACE_MIXED
unexpected staged path
commit path-set mismatch
canonical state edit outside exact three files
Git commit failure
secret/private-path export finding
```

Do not broaden execution to repair unrelated state.

# 13. success ceiling

Success means only:

```text
Cut B final admission:
PERSISTED

canonical state:
RECONCILED

next:
Cut C entry-ready

Cut C:
NOT_EXECUTED

private S1:
NOT_AUTHORIZED

P2-3:
IN_PROGRESS
```
