# 작업지시서: P2-3 capture-runner core post-commit EOL reconciliation audit

## meta

- task_id: `20260910_1425_aiscc-p2-3-capture-runner-core-postcommit-eol-reconciliation-audit-1`
- created_at: `2026-09-10T14:25:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `QA_ONLY / POST_COMMIT_RECONCILIATION_AUDIT`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_current_HEAD: `6385ab41a92e43e438e8992bacf929e7daf5130d`
- required_parent_HEAD: `04343b8518c76c3fb7ed3f0afaf92bc7e79cbdcf`
- expected_commit_message: `feat(orchestration): persist P2-3 capture runner core`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. purpose

The 1313 persistence Task created a commit and then correctly stopped because raw committed text bytes differed from the pre-commit Browser-issued bytes.

Do **not** amend, reset, restore or recreate the commit in this Task.

Determine whether the existing commit is exactly the accepted A1 content with newline-representation transformation only.

# 1. inbound transport

Verify the Browser ZIP exact filename/SHA-256 from the Short Prompt.

Place TASK first at:

```text
.aiassistant/tasks/active/20260910_1425_aiscc-p2-3-capture-runner-core-postcommit-eol-reconciliation-audit-1.md
```

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260910_1425_aiscc-p2-3-capture-runner-core-postcommit-eol-reconciliation-entry-1.cycle.md
SHA-256:
0c5b7b202830f9db97b2290620bd9904cdfbdea2f3fbf6991c4cf3d7a63a773f

.aiassistant/reports/aiscc/20260910_1425_aiscc-p2-3-capture-runner-core-postcommit-eol-reconciliation-judgment-1.md
SHA-256:
7d114c43fbc8f5c4f32eb06fe0fc94b301306d557e07af004c7d1e7a2e6ef727
```

Bootstrap failure before Task placement:

```text
STOP
no report/export
no project mutation
```

# 2. repository / commit gate

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

commit message:
feat(orchestration): persist P2-3 capture runner core

index:
empty
```

Current Git-visible paths excluding active Task must be exactly:

```text
.aiassistant/records/aiscc/cycles/20260910_1425_aiscc-p2-3-capture-runner-core-postcommit-eol-reconciliation-entry-1.cycle.md
.aiassistant/reports/aiscc/20260910_1425_aiscc-p2-3-capture-runner-core-postcommit-eol-reconciliation-judgment-1.md
```

The ignored partial 1313 target folder may exist and is non-blocking.

Any additional Git-visible path:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Do not cleanup ignored residue.

# 3. exact commit path set

Require `HEAD^..HEAD` changed paths equal these exact 21 paths:

- `.aiassistant/tasks/done/20260910_1008_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1008_aiscc-p2-3-stockroom-settlement-persisted-runtime-entry-audit-retry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1008_aiscc-p2-3-stockroom-settlement-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1040_aiscc-p2-3-actual-capture-runner-core-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1040_aiscc-p2-3-runtime-entry-audit-accepted-capture-runner-core-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1040_aiscc-p2-3-actual-capture-runtime-entry-audit-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1039_aiscc-p2-3-actual-capture-runner-core-ruff-test-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1039_aiscc-p2-3-capture-runner-core-static-failure-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1039_aiscc-p2-3-capture-runner-core-static-failure-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1142_aiscc-p2-3-capture-runner-owner-status-state-authority-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1142_aiscc-p2-3-capture-runner-owner-status-authority-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1142_aiscc-p2-3-capture-runner-owner-status-state-authority-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1157_aiscc-p2-3-capture-runner-nonworkflow-snapshot-binding-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1157_aiscc-p2-3-capture-runner-nonworkflow-snapshot-binding-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1157_aiscc-p2-3-capture-runner-nonworkflow-snapshot-binding-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1313_aiscc-p2-3-capture-runner-core-final-acceptance-git-persistence-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1313_aiscc-p2-3-capture-runner-core-accepted-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1313_aiscc-p2-3-capture-runner-core-final-acceptance-judgment-1.md`
- `src/aiscc/scenarios/capture_runner.py`
- `src/aiscc/scenarios/driver.py`
- `tests/unit/scenarios/test_stockroom_capture_runner.py`

No extra/missing/rename/delete.

Mismatch:

```text
COMMIT_PATHSET_MISMATCH
→ STOP
```

# 4. normalized-LF identity contract

For each committed blob, read raw bytes from the commit object, not from a potentially smudged working-tree checkout.

Validate:

```text
UTF-8 decodable
no UTF-8 replacement decoding
no lone CR byte
```

Compute:

```text
raw_sha256 = SHA256(committed_blob_bytes)

normalized_bytes =
committed_blob_bytes with every CRLF replaced by LF

normalized_lf_sha256 = SHA256(normalized_bytes)
```

Do not normalize any other byte.

Expected normalized-LF SHA-256 for the exact 21 paths:

- `.aiassistant/tasks/done/20260910_1008_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-retry-1.md`  `11db99ba9b22ed8e6dddab96d49d1a9207b928b846c93e53bcd88e48a8d10f52`
- `.aiassistant/records/aiscc/cycles/20260910_1008_aiscc-p2-3-stockroom-settlement-persisted-runtime-entry-audit-retry-1.cycle.md`  `3cc310ccfe052307a906fe2524db6176f7af0d38ba53616096df6ece0ff581a0`
- `.aiassistant/reports/aiscc/20260910_1008_aiscc-p2-3-stockroom-settlement-persistence-final-acceptance-judgment-1.md`  `6cb059aa4206ac5e1f00789e8adbc955f574bf84c71b2e551c4f23a414e51ff0`
- `.aiassistant/tasks/done/20260910_1040_aiscc-p2-3-actual-capture-runner-core-implementation-1.md`  `0109756f710d26b625b42ec90c98f0dd585cad36445473e9fb9e4e20e964d3d2`
- `.aiassistant/records/aiscc/cycles/20260910_1040_aiscc-p2-3-runtime-entry-audit-accepted-capture-runner-core-entry-1.cycle.md`  `6a6195c8c430a9d292c765f6a044992970b945518c25a12e506737873999bbbb`
- `.aiassistant/reports/aiscc/20260910_1040_aiscc-p2-3-actual-capture-runtime-entry-audit-final-acceptance-judgment-1.md`  `48e84d88626bcd5804ff4f3f9c580c7f9d4efa28ea974adb5f69498afa8555c3`
- `.aiassistant/tasks/done/20260910_1039_aiscc-p2-3-actual-capture-runner-core-ruff-test-retry-1.md`  `ed429af33012ecc73613badd4fc743181b5570accccd931be91e24f0bcf81dbf`
- `.aiassistant/records/aiscc/cycles/20260910_1039_aiscc-p2-3-capture-runner-core-static-failure-retry-entry-1.cycle.md`  `56de671d96c839d91d8457ed3c131f152627211ed825489a0222399041b844b6`
- `.aiassistant/reports/aiscc/20260910_1039_aiscc-p2-3-capture-runner-core-static-failure-judgment-1.md`  `5a97033467671e9cbeddc66f8d3010cc8e45bab32d11be1307d8415e8b999983`
- `.aiassistant/tasks/done/20260910_1142_aiscc-p2-3-capture-runner-owner-status-state-authority-rework-1.md`  `1c663fa72c263d5176db907e418f33811aa7f4174bc6db764d4ddb74c17f6648`
- `.aiassistant/records/aiscc/cycles/20260910_1142_aiscc-p2-3-capture-runner-owner-status-authority-rework-entry-1.cycle.md`  `d23c0d5108aa26d7b66b02dcbb0dc047eedd871ba5f208fb7b675758d71d2b63`
- `.aiassistant/reports/aiscc/20260910_1142_aiscc-p2-3-capture-runner-owner-status-state-authority-judgment-1.md`  `079d0593ef198b4f3adebd01bb2e74aebbed645e0550563e90b5b92aea1c5f5c`
- `.aiassistant/tasks/done/20260910_1157_aiscc-p2-3-capture-runner-nonworkflow-snapshot-binding-rework-1.md`  `ec44d11ce4415e25fb3d9fa89d50d2fcd4f09332dc21816fae996cc0777fee5f`
- `.aiassistant/records/aiscc/cycles/20260910_1157_aiscc-p2-3-capture-runner-nonworkflow-snapshot-binding-rework-entry-1.cycle.md`  `dd4d4bf3a8cbfcf35fbdd849fcf22609fa19a6474c05eefdff959f475de094bf`
- `.aiassistant/reports/aiscc/20260910_1157_aiscc-p2-3-capture-runner-nonworkflow-snapshot-binding-judgment-1.md`  `091813d26152595a0c12bf82fd16827dcc105b31bbff6cc3c144bf0a0d8231f9`
- `.aiassistant/tasks/done/20260910_1313_aiscc-p2-3-capture-runner-core-final-acceptance-git-persistence-1.md`  `c18709e91441669c37c041135120dec35fbfc66c72e4deab035cb4214a48c679`
- `.aiassistant/records/aiscc/cycles/20260910_1313_aiscc-p2-3-capture-runner-core-accepted-persistence-entry-1.cycle.md`  `6b3add412720dfec4ad50e4a7cf3784547385de377b4dc478a9a749fc0d913c9`
- `.aiassistant/reports/aiscc/20260910_1313_aiscc-p2-3-capture-runner-core-final-acceptance-judgment-1.md`  `5f37b367fac55c0ce782bdea7f06b9931e6537bd52c3c191625d7d88639d3799`
- `src/aiscc/scenarios/capture_runner.py`  `600de0a4b0e718f02ab2e1907b7be62b2c4a23756559fdf99cb4cd55fb80b3d2`
- `src/aiscc/scenarios/driver.py`  `9871847ec0a236ef61c91518ff95764f3c2138e3854c25a4c8cab4f028503ce6`
- `tests/unit/scenarios/test_stockroom_capture_runner.py`  `a137021608ac9cb5b4c328b6bb88fd0c22cb0d9afd9b1a22054ec5bdd32f68ff`

Require:

```text
21 / 21 normalized_lf_sha256 exact
```

Classify each path as one of:

```text
RAW_EXACT
EOL_ONLY_EQUIVALENT
```

where `EOL_ONLY_EQUIVALENT` means raw differs but normalized-LF hash is exact.

Any normalized hash mismatch:

```text
COMMIT_CONTENT_MISMATCH
→ STOP
```

Do not amend the commit.

# 5. reported 1313 Task transformation cross-check

Specifically verify:

```text
issued normalized/LF:
c18709e91441669c37c041135120dec35fbfc66c72e4deab035cb4214a48c679

reported committed raw:
4218cc043b8cd98343bcad4131cc6b08553ab2c65f38785a59c4a230d5c90433
```

Confirm whether the committed raw Task consists exactly of the issued Task with LF represented as CRLF.

Report:

```text
1313_TASK_EOL_ONLY_EQUIVALENCE:
PASS/FAIL
```

# 6. source/test semantic identity

For the three A1 code/test paths:

```text
src/aiscc/scenarios/capture_runner.py
src/aiscc/scenarios/driver.py
tests/unit/scenarios/test_stockroom_capture_runner.py
```

require normalized-LF hashes exactly match the accepted identities in section 4.

Additionally parse the normalized committed Python bytes with `ast.parse`.

Require:

```text
3 / 3 parse PASS
```

No tests are rerun.

No working-tree rewrite.

# 7. Git EOL mechanism audit

Read only; do not change configuration.

Record:

```text
git version

git config --show-origin --get core.autocrlf
git config --show-origin --get core.eol
git config --show-origin --get core.safecrlf

git check-attr text eol working-tree-encoding --   .aiassistant/tasks/done/20260910_1313_aiscc-p2-3-capture-runner-core-final-acceptance-git-persistence-1.md   src/aiscc/scenarios/capture_runner.py   tests/unit/scenarios/test_stockroom_capture_runner.py
```

If a value is unset, record `UNSET`; do not treat that alone as failure.

If `.gitattributes` or repository config directly explains the transformation, identify exact source/path/config origin.

Do not modify `.gitattributes`, `.gitconfig`, `.git/info/attributes`, or repository policy.

# 8. working-tree representation audit

For each of the same representative three paths, compare:

```text
HEAD committed raw blob SHA
working-tree raw file SHA
normalized-LF SHA of both
```

Purpose is diagnostic only.

A working-tree smudge/checkout representation difference is not itself a commit-content mismatch if section 4 passes.

Do not rewrite files to force equality.

# 9. policy conclusion

Read:

```text
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md
```

Report whether it establishes any exact repository-wide EOL requirement.

Expected current finding:

```text
UTF-8 requirement:
YES

explicit LF-only committed-blob requirement:
NOT_ESTABLISHED
```

If current canonical repository policy materially differs, quote the exact section and STOP with:

```text
CANONICAL_EOL_POLICY_CONFLICT
```

# 10. prohibited Git operations

This Task authorizes **no** Git mutation.

Do not run:

```text
git add
git commit
git commit --amend
git reset
git restore
git checkout
git stash
git clean
git rebase
git cherry-pick
git push
git pull
git fetch
```

Do not alter line endings in the working tree.

# 11. reconciliation result

If sections 2-9 PASS:

```text
result:
POST_COMMIT_RECONCILIATION_PASS

commit:
6385ab41a92e43e438e8992bacf929e7daf5130d

commit_content:
21 / 21 NORMALIZED_LF_EQUIVALENT

amend_required:
NO

source/test rerun:
NOT_REQUIRED

commit candidate:
READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT
```

This Task itself does not declare the commit finally accepted.

If any content/path/policy gate fails, report the exact mismatch and stop without commit mutation.

# 12. Task lifecycle / final workspace

Before Task lifecycle:

```text
current Cycle/Judgment:
2 exact Git-visible paths

index:
empty
```

Then move:

```text
.aiassistant/tasks/active/20260910_1425_aiscc-p2-3-capture-runner-core-postcommit-eol-reconciliation-audit-1.md
→
.aiassistant/tasks/done/20260910_1425_aiscc-p2-3-capture-runner-core-postcommit-eol-reconciliation-audit-1.md
```

Final expected Git-visible:

```text
current Cycle
current Judgment
current done Task

3 exact paths
index empty
```

The ignored partial 1313 target folder is outside this Git-visible count.

# 13. export

Bundle:

```text
.aiassistant/reports/target/20260910_1425_aiscc-p2-3-capture-runner-core-postcommit-eol-reconciliation-audit-1/
```

Required root:

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
```

Include byte-preserving copies of:

```text
current Cycle
current Judgment
current done Task
```

Do not export all 21 committed files; the matrix must contain their path/raw/normalized hashes and classification.

Create adjacent verified ZIP.

# 14. mandatory stop

```text
DOWNLOAD_ZIP_MISSING
DOWNLOAD_ZIP_HASH_MISMATCH
DOWNLOAD_ZIP_CORRUPT
DOWNLOAD_TASK_MEMBER_MISSING
DOWNLOAD_TASK_PLACEMENT_FAILED
TRANSPORT_FAILURE
HEAD_MISMATCH
PARENT_OR_MESSAGE_MISMATCH
INDEX_NOT_EMPTY
DIRTY_WORKSPACE_MIXED
COMMIT_PATHSET_MISMATCH
COMMIT_CONTENT_MISMATCH
PYTHON_SOURCE_PARSE_FAILED
CANONICAL_EOL_POLICY_CONFLICT
UNEXPECTED_WORKSPACE_DELTA
ZIP_EXPORT_FAILED
```

After a post-bootstrap audit blocker, minimal evidence/report/export is allowed by the executor-report policy; no repository/Git mutation is allowed.

# 15. final ceiling

Success:

```text
existing A1 persistence commit:
RECONCILED_CANDIDATE / BROWSER_JUDGMENT_REQUIRED

A1 capture-runner core:
ACCEPTED_CANDIDATE / COMMIT_EXISTS

A2:
NOT_STARTED

actual runtime:
NOT_RUN

actual scenario:
NOT_STARTED
```
