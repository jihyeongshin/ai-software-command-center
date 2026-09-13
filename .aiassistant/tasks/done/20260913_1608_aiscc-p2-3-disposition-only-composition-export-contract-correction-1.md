# 작업지시서: P2-3 disposition-only composition export-contract correction

## meta

- task_id: `20260913_1608_aiscc-p2-3-disposition-only-composition-export-contract-correction-1`
- created_at: `2026-09-13T16:08:10+09:00`
- work_type: `EVIDENCE_EXPORT_CONTRACT_CORRECTION`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `86288febf1cbd94bbb0235cfc680bf6c6c8f7772`
- required_parent: `4341138dde5fbea487f10a8af256f78c5dcf37f3`
- required_grandparent: `5affe61f02994f219b22ca934b5e0b93bc5e6f60`
- python_executable: `C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe`
- predecessor_result_zip_sha256: `ae4b33a00c793f312fb44218c6e7a98c504a81c1220786985d8307f3e8e22009`
- predecessor_delivery_zip_sha256: `c6997cbf25d184e4bc4d0385ba37f58878a12872176871d1c202bb6447d4358b`
- source_test_write_authorized: `No`
- test_rerun_authorized: `No`
- private_runtime_access_authorized: `No`
- success_ceiling: `DISPOSITION_ONLY_COMPOSITION_EVIDENCE_COMPLETE / BROWSER_REVIEW_PENDING`

# 0. purpose

Correct only the 1531 export-contract defect.

Do not modify source/test.
Do not rerun tests.
Do not access Docker, PostgreSQL, retained private runtime/workspace.

# 1. transport / Python

Use only:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe
```

Verify this delivery ZIP/hash and exactly three flat safe members.

Place current Task first in canonical active, then current Cycle/Judgment.

Bootstrap mismatch → STOP without evidence reconstruction.

# 2. repository baseline

Require:

```text
branch main
HEAD 86288febf1cbd94bbb0235cfc680bf6c6c8f7772
HEAD^ 4341138dde5fbea487f10a8af256f78c5dcf37f3
HEAD^^ 5affe61f02994f219b22ca934b5e0b93bc5e6f60
index empty
```

Tracked dirty exactly:

- `src/aiscc/scenarios/stockroom_production.py`  `c41baca3f7cbeaaa18511dd6e94dd5dd5e65d2b282968703f2a4854d86e1b2f4`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`  `d46ec32658be849a6aea659d52e675636f6e78263e5ef6d0c65a6f2855a279bd`

Canonical state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `b551c534dcf55a3e5e20c4cb379cf1957ba8f719f1bb6d75c980ce5de7cd6283`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `551d0df4a5ad14a4fd825057f18d95d157b8fefb3a9821d26ef92fc2664ce74a`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `36687e0653375ca3c3ea4daf6393ced5a1856e1c70f5822408002322a964da24`

Before current Cycle/Judgment placement, Git-visible untracked exactly 15:

- `.aiassistant/tasks/done/20260913_1406_aiscc-p2-3-private-s1-invalid-history-disposition-execution-1.md`
- `.aiassistant/records/aiscc/cycles/20260913_1406_aiscc-p2-3-private-s1-invalid-history-disposition-execution-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260913_1406_aiscc-p2-3-private-s1-invalid-history-disposition-execution-authorization-judgment-1.md`
- `.aiassistant/tasks/done/20260913_1435_aiscc-p2-3-private-s1-invalid-history-disposition-root-authority-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260913_1435_aiscc-p2-3-private-s1-root-authority-reconstructed-disposition-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260913_1435_aiscc-p2-3-private-s1-root-authority-transport-gap-retry-judgment-1.md`
- `.aiassistant/tasks/done/20260913_1511_aiscc-p2-3-disposition-only-composition-entrypoint-source-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260913_1511_aiscc-p2-3-disposition-builder-conflict-source-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260913_1511_aiscc-p2-3-full-builder-retained-root-conflict-rework-judgment-1.md`
- `.aiassistant/tasks/done/20260913_1520_aiscc-p2-3-disposition-only-composition-entrypoint-transport-corrected-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260913_1520_aiscc-p2-3-disposition-composition-transport-baseline-corrected-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260913_1520_aiscc-p2-3-1511-transport-baseline-mismatch-retry-judgment-1.md`
- `.aiassistant/tasks/done/20260913_1531_aiscc-p2-3-disposition-only-composition-active-legacy-corrected-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260913_1531_aiscc-p2-3-disposition-composition-active-legacy-corrected-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260913_1531_aiscc-p2-3-1520-active-legacy-baseline-mismatch-retry-judgment-1.md`

Require legacy non-owned active:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
SHA-256 52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

Do not move/modify it.

After current Cycle/Judgment placement:

```text
Git-visible untracked:
17 exact
```

# 3. predecessor evidence bundle

Locate the exact existing 1531 Executor result ZIP/report by SHA:

```text
ae4b33a00c793f312fb44218c6e7a98c504a81c1220786985d8307f3e8e22009
```

If unavailable locally:

```text
PREDECESSOR_EVIDENCE_UNAVAILABLE
→ STOP
```

Do not rerun tests to recreate it.

Verify predecessor:

```text
CRC PASS
one top-level
17 members
16 manifest rows exact
TASK.md == canonical 1531 done Task
ACTIVE_TASK_OWNERSHIP_VERIFICATION.md absent
```

# 4. preserve prior evidence

Reuse the predecessor evidence claims without new observations:

```text
TRANSPORT_BASELINE_CORRECTION.md
BUILDER_CONFLICT_VERIFICATION.md
DEDICATED_COMPOSITION_VERIFICATION.md
NEGATIVE_COMPOSITION_BOUNDARY.md
NONEMPTY_ROOT_INTEGRATION_VERIFICATION.md
TEST_VERIFICATION.md
GIT_DIFF_VERIFICATION.md
```

No claim may be strengthened.

# 5. create missing ownership evidence

Create:

```text
ACTIVE_TASK_OWNERSHIP_VERIFICATION.md
```

It must record exactly:

```text
legacy non-owned active:
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md

legacy SHA:
52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb

1531 track Task:
already active→done byte-exact in predecessor execution

active-directory exclusivity:
not a governance invariant here

ownership:
only explicitly owned Task paths may be moved/closed

legacy 1400:
preserved unchanged / excluded from export
```

# 6. current Task lifecycle

Before current Task move require:

```text
HEAD unchanged
index empty
tracked dirty same exact two candidate hashes
Git-visible untracked 17 exact
legacy 1400 exact
```

Move only current Task active→done byte-identically.

Final:

```text
Git-visible untracked:
18 exact

current track:
1406 / 1435 / 1511 / 1520 / 1531 / 1608 triples

legacy 1400 active:
preserved / non-owned
```

# 7. contract review

Require exactly 40 rows:

```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_CLEAN
PRE_DELIVERY_UNTRACKED_15_EXACT
LEGACY_1400_ACTIVE_TASK_EXACT
CURRENT_STATE_HASHES_EXACT
CANDIDATE_SOURCE_HASHES_EXACT
TRACKED_DIRTY_EXACT_2
INDEX_EMPTY
PYTHON_EXECUTABLE_EXACT
NO_SOURCE_TEST_WRITE
NO_TEST_RERUN
NO_PRIVATE_RUNTIME_ACCESS
NO_DB_DOCKER_ACCESS
PRIOR_1531_RESULT_ZIP_SHA_EXACT
PRIOR_1531_CRC_PASS
PRIOR_1531_ONE_TOP_LEVEL
PRIOR_1531_MANIFEST_16_EXACT
PRIOR_1531_TASK_DONE_EQUAL
PRIOR_1531_CONTRACT_57_ROWS_READ
PRIOR_1531_MISSING_ACTIVE_OWNERSHIP_DOC_CONFIRMED
PRIOR_1531_MEMBER_COUNT_DEFECT_CONFIRMED
ACTIVE_TASK_OWNERSHIP_DOC_CREATED
ACTIVE_TASK_OWNERSHIP_LEGACY_1400_EXACT
ACTIVE_TASK_OWNERSHIP_1531_DONE_EXACT
ACTIVE_TASK_OWNERSHIP_NON_OWNED_POLICY_EXACT
PRIOR_TEST_EVIDENCE_PRESERVED
PRIOR_BUILDER_EVIDENCE_PRESERVED
PRIOR_NEGATIVE_COMPOSITION_EVIDENCE_PRESERVED
PRIOR_NONEMPTY_ROOT_EVIDENCE_PRESERVED
CURRENT_CYCLE_JUDGMENT_EXACT
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
FINAL_UNTRACKED_18_EXACT
FINAL_LEGACY_1400_ACTIVE_PRESERVED
CORRECTED_EXPORT_19_MEMBERS
CORRECTED_MANIFEST_18_EXACT
CORRECTED_ONE_TOP_LEVEL
CORRECTED_TASK_DONE_EQUAL
CORRECTED_CRC_PASS
CORRECTED_NO_PRIVATE_BYTES
EXPORT_INTEGRITY_PASS
```

Success:

```text
40 / 40 PASS
```

# 8. corrected export

Root docs exactly 14:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
ACTIVE_TASK_OWNERSHIP_VERIFICATION.md
PRIOR_BUNDLE_VERIFICATION.md
TRANSPORT_BASELINE_CORRECTION.md
BUILDER_CONFLICT_VERIFICATION.md
DEDICATED_COMPOSITION_VERIFICATION.md
NEGATIVE_COMPOSITION_BOUNDARY.md
NONEMPTY_ROOT_INTEGRATION_VERIFICATION.md
TEST_VERIFICATION.md
GIT_DIFF_VERIFICATION.md
CONTRACT_REVIEW.md
```

Project-relative copies exactly 5:

```text
current Cycle
current Judgment
current done Task
src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Require:

```text
19 total members
18 non-self manifest rows
one top-level directory
CRC PASS
TASK.md == canonical current done Task
manifest hashes exact
```

# 9. success ceiling

```text
1531 source candidate:
UNCHANGED / TECHNICALLY_ACCEPTABLE

1531 export defect:
CORRECTED

tests:
NOT_RERUN

private runtime:
UNTOUCHED

Browser final source acceptance:
PENDING

Git persistence:
NOT_PERFORMED

P2-3:
IN_PROGRESS
```
