# 작업지시서: P2-3 capture-runner core reconciliation evidence export transport retry

## meta

- task_id: `20260910_1515_aiscc-p2-3-capture-runner-core-reconciliation-evidence-export-transport-retry-1`
- created_at: `2026-09-10T15:15:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `QA_ONLY / EVIDENCE_EXPORT_RETRY`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_current_HEAD: `6385ab41a92e43e438e8992bacf929e7daf5130d`
- required_parent_HEAD: `04343b8518c76c3fb7ed3f0afaf92bc7e79cbdcf`
- expected_commit_message: `feat(orchestration): persist P2-3 capture runner core`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. transport recovery provenance

The prior 1428 delivery failed before canonical Task placement.

It is not canonical predecessor Task provenance.

The only authorized pre-placement residue recovery was the exact noncanonical failed-transport file described in the Browser Short Prompt.

After this TASK is correctly placed at:

```text
.aiassistant/tasks/active/20260910_1515_aiscc-p2-3-capture-runner-core-reconciliation-evidence-export-transport-retry-1.md
```

the noncanonical file must be absent.

Do not recursively clean `.assistant`.

# 1. inbound canonical placement

This Task's canonical active path is exactly:

```text
.aiassistant/tasks/active/20260910_1515_aiscc-p2-3-capture-runner-core-reconciliation-evidence-export-transport-retry-1.md
```

Important:

```text
.aiassistant
```

is correct.

```text
.assistant
```

is incorrect.

After reading this Task, place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260910_1515_aiscc-p2-3-capture-runner-core-transport-failure-retry-entry-1.cycle.md
SHA-256:
0d553a420c9a752fe53cc1b0bbd5bb37358d4009ca54c9c43bc27aa3d6850ec0

.aiassistant/reports/aiscc/20260910_1515_aiscc-p2-3-capture-runner-core-1428-transport-failure-judgment-1.md
SHA-256:
f8d10a8baa583139769ff2193cd43bcda8405789e48955fcbd677d9915e50cd7
```

# 2. repository gate

Require:

```text
branch:
main

HEAD:
6385ab41a92e43e438e8992bacf929e7daf5130d

parent:
04343b8518c76c3fb7ed3f0afaf92bc7e79cbdcf

parent count:
1

message:
feat(orchestration): persist P2-3 capture runner core

index:
empty
```

Require exact failed-residue path:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center\.assistant\tasks\active\20260910_1428_aiscc-p2-3-capture-runner-core-reconciliation-evidence-export-retry-1.md
```

to be absent.

Expected Git-visible set excluding active Task is exact 5 paths:

- `.aiassistant/tasks/done/20260910_1425_aiscc-p2-3-capture-runner-core-postcommit-eol-reconciliation-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1425_aiscc-p2-3-capture-runner-core-postcommit-eol-reconciliation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1425_aiscc-p2-3-capture-runner-core-postcommit-eol-reconciliation-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1515_aiscc-p2-3-capture-runner-core-transport-failure-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1515_aiscc-p2-3-capture-runner-core-1428-transport-failure-judgment-1.md`

Ignored target/export directories/ZIPs may exist and are non-blocking.

Any additional Git-visible path:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

No broad cleanup.

# 3. exact 1425 canonical provenance

Require:

- `.aiassistant/tasks/done/20260910_1425_aiscc-p2-3-capture-runner-core-postcommit-eol-reconciliation-audit-1.md`  `d85a672ae6ce2ea19a75d10696fde186e655444e26ae7a184add73d5053a11c6`
- `.aiassistant/records/aiscc/cycles/20260910_1425_aiscc-p2-3-capture-runner-core-postcommit-eol-reconciliation-entry-1.cycle.md`  `0c5b7b202830f9db97b2290620bd9904cdfbdea2f3fbf6991c4cf3d7a63a773f`
- `.aiassistant/reports/aiscc/20260910_1425_aiscc-p2-3-capture-runner-core-postcommit-eol-reconciliation-judgment-1.md`  `7d114c43fbc8f5c4f32eb06fe0fc94b301306d557e07af004c7d1e7a2e6ef727`

Mismatch:

```text
PREDECESSOR_PROVENANCE_IDENTITY_MISMATCH
→ STOP
```

# 4. commit metadata verification

Create:

```text
COMMIT_METADATA_VERIFICATION.md
```

Record actual read-only evidence for:

```text
HEAD
tree
parent
parent count
commit message
author/committer timestamps
index state
Git-visible worktree state
push/network NOT_RUN
```

# 5. exact commit pathset verification

Create:

```text
COMMIT_PATHSET_VERIFICATION.md
```

Require `HEAD^..HEAD` exact 21-path set from section 6:

```text
21 exact
extra 0
missing 0
rename 0
delete 0
```

# 6. 21-row EOL identity matrix

Create:

```text
EOL_IDENTITY_MATRIX.md
```

Exact paths and expected normalized-LF SHA-256:

- `.aiassistant/tasks/done/20260910_1008_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-retry-1.md`  expected_normalized_lf=`11db99ba9b22ed8e6dddab96d49d1a9207b928b846c93e53bcd88e48a8d10f52`
- `.aiassistant/records/aiscc/cycles/20260910_1008_aiscc-p2-3-stockroom-settlement-persisted-runtime-entry-audit-retry-1.cycle.md`  expected_normalized_lf=`3cc310ccfe052307a906fe2524db6176f7af0d38ba53616096df6ece0ff581a0`
- `.aiassistant/reports/aiscc/20260910_1008_aiscc-p2-3-stockroom-settlement-persistence-final-acceptance-judgment-1.md`  expected_normalized_lf=`6cb059aa4206ac5e1f00789e8adbc955f574bf84c71b2e551c4f23a414e51ff0`
- `.aiassistant/tasks/done/20260910_1040_aiscc-p2-3-actual-capture-runner-core-implementation-1.md`  expected_normalized_lf=`0109756f710d26b625b42ec90c98f0dd585cad36445473e9fb9e4e20e964d3d2`
- `.aiassistant/records/aiscc/cycles/20260910_1040_aiscc-p2-3-runtime-entry-audit-accepted-capture-runner-core-entry-1.cycle.md`  expected_normalized_lf=`6a6195c8c430a9d292c765f6a044992970b945518c25a12e506737873999bbbb`
- `.aiassistant/reports/aiscc/20260910_1040_aiscc-p2-3-actual-capture-runtime-entry-audit-final-acceptance-judgment-1.md`  expected_normalized_lf=`48e84d88626bcd5804ff4f3f9c580c7f9d4efa28ea974adb5f69498afa8555c3`
- `.aiassistant/tasks/done/20260910_1039_aiscc-p2-3-actual-capture-runner-core-ruff-test-retry-1.md`  expected_normalized_lf=`ed429af33012ecc73613badd4fc743181b5570accccd931be91e24f0bcf81dbf`
- `.aiassistant/records/aiscc/cycles/20260910_1039_aiscc-p2-3-capture-runner-core-static-failure-retry-entry-1.cycle.md`  expected_normalized_lf=`56de671d96c839d91d8457ed3c131f152627211ed825489a0222399041b844b6`
- `.aiassistant/reports/aiscc/20260910_1039_aiscc-p2-3-capture-runner-core-static-failure-judgment-1.md`  expected_normalized_lf=`5a97033467671e9cbeddc66f8d3010cc8e45bab32d11be1307d8415e8b999983`
- `.aiassistant/tasks/done/20260910_1142_aiscc-p2-3-capture-runner-owner-status-state-authority-rework-1.md`  expected_normalized_lf=`1c663fa72c263d5176db907e418f33811aa7f4174bc6db764d4ddb74c17f6648`
- `.aiassistant/records/aiscc/cycles/20260910_1142_aiscc-p2-3-capture-runner-owner-status-authority-rework-entry-1.cycle.md`  expected_normalized_lf=`d23c0d5108aa26d7b66b02dcbb0dc047eedd871ba5f208fb7b675758d71d2b63`
- `.aiassistant/reports/aiscc/20260910_1142_aiscc-p2-3-capture-runner-owner-status-state-authority-judgment-1.md`  expected_normalized_lf=`079d0593ef198b4f3adebd01bb2e74aebbed645e0550563e90b5b92aea1c5f5c`
- `.aiassistant/tasks/done/20260910_1157_aiscc-p2-3-capture-runner-nonworkflow-snapshot-binding-rework-1.md`  expected_normalized_lf=`ec44d11ce4415e25fb3d9fa89d50d2fcd4f09332dc21816fae996cc0777fee5f`
- `.aiassistant/records/aiscc/cycles/20260910_1157_aiscc-p2-3-capture-runner-nonworkflow-snapshot-binding-rework-entry-1.cycle.md`  expected_normalized_lf=`dd4d4bf3a8cbfcf35fbdd849fcf22609fa19a6474c05eefdff959f475de094bf`
- `.aiassistant/reports/aiscc/20260910_1157_aiscc-p2-3-capture-runner-nonworkflow-snapshot-binding-judgment-1.md`  expected_normalized_lf=`091813d26152595a0c12bf82fd16827dcc105b31bbff6cc3c144bf0a0d8231f9`
- `.aiassistant/tasks/done/20260910_1313_aiscc-p2-3-capture-runner-core-final-acceptance-git-persistence-1.md`  expected_normalized_lf=`c18709e91441669c37c041135120dec35fbfc66c72e4deab035cb4214a48c679`
- `.aiassistant/records/aiscc/cycles/20260910_1313_aiscc-p2-3-capture-runner-core-accepted-persistence-entry-1.cycle.md`  expected_normalized_lf=`6b3add412720dfec4ad50e4a7cf3784547385de377b4dc478a9a749fc0d913c9`
- `.aiassistant/reports/aiscc/20260910_1313_aiscc-p2-3-capture-runner-core-final-acceptance-judgment-1.md`  expected_normalized_lf=`5f37b367fac55c0ce782bdea7f06b9931e6537bd52c3c191625d7d88639d3799`
- `src/aiscc/scenarios/capture_runner.py`  expected_normalized_lf=`600de0a4b0e718f02ab2e1907b7be62b2c4a23756559fdf99cb4cd55fb80b3d2`
- `src/aiscc/scenarios/driver.py`  expected_normalized_lf=`9871847ec0a236ef61c91518ff95764f3c2138e3854c25a4c8cab4f028503ce6`
- `tests/unit/scenarios/test_stockroom_capture_runner.py`  expected_normalized_lf=`a137021608ac9cb5b4c328b6bb88fd0c22cb0d9afd9b1a22054ec5bdd32f68ff`

Read each blob directly from the commit object.

For every path report:

```text
path
raw_sha256
normalized_lf_sha256
expected_normalized_lf_sha256
utf8_strict_decode
lone_cr_count
crlf_count
classification
result
```

Normalization:

```text
CRLF -> LF
```

only.

Allowed classification:

```text
RAW_EXACT
EOL_ONLY_EQUIVALENT
```

Require:

```text
UTF-8 strict:
21/21

lone CR:
0 paths

normalized_lf_sha256:
21/21 exact

result:
21/21 PASS
```

Any mismatch:

```text
COMMIT_CONTENT_MISMATCH
→ STOP
```

# 7. 1313 Task diagnostic

For:

```text
.aiassistant/tasks/done/20260910_1313_aiscc-p2-3-capture-runner-core-final-acceptance-git-persistence-1.md
```

record:

```text
actual committed raw SHA-256
actual normalized-LF SHA-256
expected:
c18709e91441669c37c041135120dec35fbfc66c72e4deab035cb4214a48c679

LF->CRLF diagnostic hash:
4218cc043b8cd98343bcad4131cc6b08553ab2c65f38785a59c4a230d5c90433
```

State explicitly whether `4218...` is:

```text
actual commit-object raw hash
```

or:

```text
CRLF representation diagnostic only
```

# 8. Git EOL configuration evidence

Create:

```text
GIT_EOL_CONFIGURATION.md
```

Record read-only outputs for:

```text
git version
git config --show-origin --get core.autocrlf
git config --show-origin --get core.eol
git config --show-origin --get core.safecrlf
```

and representative:

```text
git check-attr text eol working-tree-encoding
```

for the 1313 Task, runner, and runner unit test.

Compare HEAD raw blob SHA vs working-tree raw SHA for those three representative paths.

No configuration mutation.

# 9. policy verification

Create:

```text
POLICY_VERIFICATION.md
```

Read canonical asset/Git/encoding policy and report exact policy text/section for:

```text
UTF-8 requirement:
YES/NO

repository-wide committed-blob LF-only requirement:
YES/NO
```

If a canonical LF-only blob policy actually exists and conflicts with current commit:

```text
CANONICAL_EOL_POLICY_CONFLICT
→ STOP
```

# 10. source/test parse spot-check

Parse normalized committed Python bytes with `ast.parse`:

```text
src/aiscc/scenarios/capture_runner.py
src/aiscc/scenarios/driver.py
tests/unit/scenarios/test_stockroom_capture_runner.py
```

Require:

```text
3/3 PASS
```

No pytest.

# 11. reconciliation conclusion

Create:

```text
RECONCILIATION_CONCLUSION.md
```

Report:

```text
commit metadata:
PASS/FAIL

commit pathset:
PASS/FAIL

normalized content:
N/21 PASS

raw exact:
N/21

EOL-only equivalent:
N/21

source/test parse:
N/3

Git EOL mechanism:
identified / partially identified / unknown

canonical EOL policy conflict:
YES/NO

amend required:
YES/NO

result:
POST_COMMIT_RECONCILIATION_PASS
or exact blocker
```

Do not declare final Browser acceptance.

# 12. no mutation ceiling

Forbidden:

```text
source/test/config edit
working-tree line-ending rewrite
git add
git commit
git commit --amend
git reset
git restore
git checkout
git stash
git clean
git rebase
git push/pull/fetch
pytest
DB
Docker
provider/tool/materializer
runtime/scenario execution
```

Read-only Git/Python/PowerShell verification is allowed.

# 13. Task lifecycle

Before lifecycle:

```text
1425 provenance:
3

current Cycle/Judgment:
2

total excluding active Task:
5 exact

index:
empty
```

Move active Task byte-identically to:

```text
.aiassistant/tasks/done/20260910_1515_aiscc-p2-3-capture-runner-core-reconciliation-evidence-export-transport-retry-1.md
```

Final Git-visible:

```text
6 exact
index empty
```

# 14. exact outbound export

Bundle:

```text
.aiassistant/reports/target/20260910_1515_aiscc-p2-3-capture-runner-core-reconciliation-evidence-export-transport-retry-1/
```

Root must contain exactly these 10 Markdown files:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
COMMIT_METADATA_VERIFICATION.md
COMMIT_PATHSET_VERIFICATION.md
EOL_IDENTITY_MATRIX.md
GIT_EOL_CONFIGURATION.md
POLICY_VERIFICATION.md
RECONCILIATION_CONCLUSION.md
```

Additionally include byte-preserving project-relative copies of exactly:

```text
.aiassistant/tasks/done/20260910_1515_aiscc-p2-3-capture-runner-core-reconciliation-evidence-export-transport-retry-1.md
.aiassistant/records/aiscc/cycles/20260910_1515_aiscc-p2-3-capture-runner-core-transport-failure-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260910_1515_aiscc-p2-3-capture-runner-core-1428-transport-failure-judgment-1.md
```

Expected ZIP member count:

```text
13 exact
```

`EXPORT_MANIFEST.md` enumerates all 12 non-self entries with relative path, size, SHA-256.

Verify:

```text
one top-level directory
13 members exact
CRC PASS
10/10 required roots
3/3 canonical copies
manifest 12/12 exact
folder/archive byte equality
```

# 15. mandatory stop

```text
DOWNLOAD_ZIP_MISSING
DOWNLOAD_ZIP_HASH_MISMATCH
DOWNLOAD_ZIP_CORRUPT
DOWNLOAD_TASK_MEMBER_MISSING
DOWNLOAD_TASK_PLACEMENT_FAILED
TRANSPORT_RESIDUE_MISMATCH
TRANSPORT_FAILURE
HEAD_MISMATCH
PARENT_OR_MESSAGE_MISMATCH
INDEX_NOT_EMPTY
DIRTY_WORKSPACE_MIXED
PREDECESSOR_PROVENANCE_IDENTITY_MISMATCH
COMMIT_PATHSET_MISMATCH
COMMIT_CONTENT_MISMATCH
PYTHON_SOURCE_PARSE_FAILED
CANONICAL_EOL_POLICY_CONFLICT
UNEXPECTED_WORKSPACE_DELTA
ZIP_EXPORT_FAILED
```

# 16. final ceiling

Success:

```text
existing A1 persistence commit:
RECONCILIATION_EVIDENCE_COMPLETE / BROWSER_JUDGMENT_REQUIRED

A1:
COMMIT_EXISTS / FINAL_ACCEPTANCE_PENDING

A2:
NOT_STARTED

actual runtime:
NOT_RUN
```
