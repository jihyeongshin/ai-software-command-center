# 작업지시서: P2-3 Replay canonical path-basis corrected terminal closure retry

## meta
- created_at: `2026-09-14T02:24:00+09:00`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `23311b5283c9412e30783ae46a1925e85579247b`
- required_parent: `a1c934ea75906a548f2bc4adc777c2a0ecc99be5`
- required_grandparent: `33a216f29062176ad196a567a299ba30291c3f72`
- reviewed_0205_result_zip_sha256: `d113a377bcfc821106ee8180d597d73675019b9cf18c2f8eb891799c87e28fe3`
- accepted_0145_result_zip_sha256: `02ef19ba18e7f36de37f8cc1edfa6fd1228973f298c5735ee38402f1b14a995a`
- replay_canonical_persistence_authorized: `Yes`
- replay_index_path_basis_normalization_authorized: `Yes / exact four member paths`
- canonical_state_reconciliation_authorized: `Yes / exact three state paths`
- private_runtime_or_DB_authorized: `No`
- source_test_config_write_authorized: `No`
- scenario_execution_authorized: `No`
- public_release_authorized: `No`
- push_authorized: `No`
- success_ceiling: `P2_3_ACCEPTED_CLOSED / P2_4_ENTRY_READY`

## 0. corrected authority

0205 is a Command Center contract-defect STOP, not a product/Replay defect.

The corrected canonical-index promotion explicitly authorizes:

```text
member_relative_path:
replay/<filename>
→ <filename>
```

for exactly four members because `REPLAY_CORPUS_INDEX.json` and those members are persisted in the same canonical directory.

No other new semantic change is authorized.

Strict order:

```text
A. verify blocked 0205 repository/result state
B. move blocked 0205 active Task → done byte-exact
C. derive canonical Replay with corrected index path basis
D. Commit A: blocked lineage + current entry + canonical Replay
E. reconcile exactly 3 canonical state files
F. Commit B
G. final P2-3 closure verification
```

## 1. executables

Use only:

```text
Python:
<repository-root>\.venv\Scripts\python.exe

Git:
C:\Program Files\Git\cmd\git.exe
```

Forbidden:
`python`, `py`, WindowsApps, PATH/external Python discovery, Docker, private PostgreSQL.

## 2. exact blocked baseline

Require:

```text
branch main
HEAD 23311b5283c9412e30783ae46a1925e85579247b
HEAD^ a1c934ea75906a548f2bc4adc777c2a0ecc99be5
HEAD^^ 33a216f29062176ad196a567a299ba30291c3f72
index empty
tracked clean
```

Git-visible untracked exactly three:

```text
.aiassistant/tasks/done/20260914_0145_aiscc-p2-3-recorded-replay-corpus-capture-and-review-candidate-1.md
.aiassistant/records/aiscc/cycles/20260914_0205_aiscc-p2-3-recorded-replay-final-acceptance-terminal-closure-1.cycle.md
.aiassistant/reports/aiscc/20260914_0205_aiscc-p2-3-0145-recorded-replay-corpus-final-acceptance-closure-authorization-1.md
```

Require exact hashes:

```text
0145 done:
f50b25b17265e8ec0870e1262389428d58989725eaf6c975b1bc494f75f62646

0205 Cycle:
6180cdb13b8d174c0a65efc009de03e358e942e61b7ba4fb786015b03e6c3860

0205 Judgment:
ab746c87acb3c6ef9819f63e623c64385cdfec9edcba30d4de78b3b314bdb5b3
```

Require blocked 0205 Task still active/ignored:

```text
.aiassistant/tasks/active/20260914_0205_aiscc-p2-3-replay-canonical-persistence-terminal-state-reconciliation-and-closure-1.md
SHA-256 42ea6cb678299bb37e36ac4484fd3cd1e1df9c259a742e0c002eed10571dfcf4
```

Canonical Replay directory must still be absent.

Canonical state hashes must remain:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md` `281bd733624ac87be207f62ed59b99edf0d64cf3b8f3d00e9bc9611fe3179f8c`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md` `b55eb504c39af0134837f808eef8610b0c54505ee8c597b332f79148ad61d8bd`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md` `1bb251b5758e8fea1ac260dcace074dcb7e2ff9adf6a96e8699d29c66bea495d`

Preserve ignored non-owned legacy:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
SHA-256 52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

After current Cycle/Judgment placement while current retry Task active/ignored:

```text
Git-visible untracked exactly five
```

Any mismatch → STOP before mutation.

## 3. verify 0205 result evidence

Require uploaded/retained 0205 result evidence SHA:

```text
d113a377bcfc821106ee8180d597d73675019b9cf18c2f8eb891799c87e28fe3
```

Accepted diagnosis:

```text
20 members
19 manifest rows exact
CRC PASS
TASK byte-exact
21 PASS / 1 FAIL / 44 BLOCKED
failed row = CANONICAL_INDEX_HASH_EXACT
```

Do not reinterpret this as a product failure.

## 4. close blocked 0205 Task lineage

Move exactly:

```text
.aiassistant/tasks/active/20260914_0205_aiscc-p2-3-replay-canonical-persistence-terminal-state-reconciliation-and-closure-1.md
→
.aiassistant/tasks/done/20260914_0205_aiscc-p2-3-replay-canonical-persistence-terminal-state-reconciliation-and-closure-1.md
```

Byte-exact.

Do not alter its contents.

After this move and before canonical Replay creation:

```text
Git-visible untracked exactly six:
0145 done
0205 Cycle
0205 Judgment
0205 done Task
current Cycle
current Judgment
```

Legacy 1400 and current retry Task remain active/ignored.

## 5. exact accepted Replay source

Read the accepted predecessor Replay only from the verified 0145 result ZIP:

```text
SHA-256:
02ef19ba18e7f36de37f8cc1edfa6fd1228973f298c5735ee38402f1b14a995a
```

Candidate corpus root:

```text
48462d227a246e8501ea7fd087c07617dab26d8c818f82d098633e5df0c6949c
```

Do not reconstruct Replay from private DB/runtime.

## 6. canonical Replay directory

Create only:

```text
.aiassistant/reports/aiscc/replay/stockroom/v1
```

Exact files:

```text
REPLAY_CORPUS_INDEX.json
stockroom-s1-normal.json
stockroom-s2-missing-evidence.json
stockroom-s3-policy-conflict.json
stockroom-s4-human-owned-claim.json
```

No source/viewer/deployment file.

## 7. canonical member promotion

For each four Replay member JSONs, change exactly:

```text
schema_id:
AISCC-RECORDED-RUN-REPLAY-CANDIDATE-V1
→ AISCC-RECORDED-RUN-REPLAY-V1

public_admission:
PENDING_BROWSER_REVIEW
→ CANONICAL_CORPUS_ACCEPTED_PUBLIC_RELEASE_PENDING
```

All other semantic fields unchanged.

Serialize with:
`ensure_ascii=False`, `sort_keys=True`, `indent=2`, one trailing LF.

Exact outputs:

- `stockroom-s1-normal.json` `6fb493838b0158fc9a8416146e980e027fc1091ec77e0e3504f07b4b71ed26cc` / 12591 bytes / final `ACCEPTED`
- `stockroom-s2-missing-evidence.json` `103b98776d6e79867ea1e8ecac72a619c01a9223049434239e287381e2824201` / 11755 bytes / final `REWORK_REQUIRED`
- `stockroom-s3-policy-conflict.json` `4ad9d71814ce5301fd48b6e40547229f6b76b16c36e69d722130eb82f03b1137` / 9771 bytes / final `BLOCKED`
- `stockroom-s4-human-owned-claim.json` `c6197411795760844bf74b8805476c35377117fb364423ec0a4cbf62734e3034` / 13042 bytes / final `HUMAN_REQUIRED`

## 8. corrected canonical index promotion

From exact candidate `REPLAY_CORPUS_INDEX.json`:

Change:

```text
public_admission:
PENDING_BROWSER_REVIEW
→ CANONICAL_CORPUS_ACCEPTED_PUBLIC_RELEASE_PENDING
```

For each member update:
- `member_sha256`
- `member_bytes`
- `member_relative_path`

Exact path normalization:

```text
replay/stockroom-s1-normal.json
→ stockroom-s1-normal.json

replay/stockroom-s2-missing-evidence.json
→ stockroom-s2-missing-evidence.json

replay/stockroom-s3-policy-conflict.json
→ stockroom-s3-policy-conflict.json

replay/stockroom-s4-human-owned-claim.json
→ stockroom-s4-human-owned-claim.json
```

This is the only additional change relative to 0205.

Update `integrity_algorithm.canonical_tuples` with canonical hashes/sizes and recompute root using the accepted tuple algorithm.

Important:

```text
member_relative_path is NOT part of the corpus integrity tuple.
```

Require:

```text
canonical corpus root:
a870da635941d7149edbbef911e8b2d75ff6fe12e8ade80c09dddc9086df795e

canonical index bytes:
4084

canonical index SHA-256:
c92fb81c43cef9b1c379c2df8dac967aa55f4ddae73780d31f5d51c617aa38e0
```

All other index semantics remain exact.

## 9. canonical Replay truthfulness

Revalidate:

```text
S1 ACCEPTED / Judgment ACCEPTED
S2 REWORK_REQUIRED / HOLD_REWORK_REQUIRED
S3 BLOCKED / POLICY_CONFLICT / provider-tool-Judgment-HumanResult 0
S4 HUMAN_REQUIRED / HumanGate PENDING / HumanResult-Judgment 0

Recorded Run Replay labels present
live=false
viewing_llm_inference_calls=0
raw evidence body absent
private values absent
public release pending
```

Do not claim deployment.

## 10. Commit A — exact 11 paths

Stage exactly:

```text
.aiassistant/tasks/done/20260914_0145_aiscc-p2-3-recorded-replay-corpus-capture-and-review-candidate-1.md
.aiassistant/records/aiscc/cycles/20260914_0205_aiscc-p2-3-recorded-replay-final-acceptance-terminal-closure-1.cycle.md
.aiassistant/reports/aiscc/20260914_0205_aiscc-p2-3-0145-recorded-replay-corpus-final-acceptance-closure-authorization-1.md
.aiassistant/tasks/done/20260914_0205_aiscc-p2-3-replay-canonical-persistence-terminal-state-reconciliation-and-closure-1.md

.aiassistant/records/aiscc/cycles/20260914_0224_aiscc-p2-3-replay-index-path-basis-corrected-closure-entry-1.cycle.md
.aiassistant/reports/aiscc/20260914_0224_aiscc-p2-3-0205-command-center-replay-index-path-basis-conflict-judgment-1.md

.aiassistant/reports/aiscc/replay/stockroom/v1/REPLAY_CORPUS_INDEX.json
.aiassistant/reports/aiscc/replay/stockroom/v1/stockroom-s1-normal.json
.aiassistant/reports/aiscc/replay/stockroom/v1/stockroom-s2-missing-evidence.json
.aiassistant/reports/aiscc/replay/stockroom/v1/stockroom-s3-policy-conflict.json
.aiassistant/reports/aiscc/replay/stockroom/v1/stockroom-s4-human-owned-claim.json
```

Commit message exactly:

```text
feat(aiscc): admit stockroom replay corpus and closure lineage
```

Require:
- parent `23311b5283c9412e30783ae46a1925e85579247b`
- changed paths exact 11
- index empty
- tracked clean
- Git-visible untracked zero

Do not stage current retry Task or canonical state yet.

## 11. canonical state reconciliation

After Commit A, modify exactly:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

No broad replacement.

Required CURRENT_STATE semantics:

```text
P2-1 ACCEPTED / CLOSED
P2-2 ACCEPTED / CLOSED
P2-3 ACCEPTED / CLOSED
P2-4 NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE
P2 IN_PROGRESS
Public Bounded Live NOT_RELEASED
public deployment NOT_COMPLETED
```

Record P2-3 terminal matrix:

```text
S1 ACCEPTED
S2 REWORK_REQUIRED / HOLD_REWORK_REQUIRED
S3 BLOCKED / POLICY_CONFLICT / provider-tool-Judgment-HumanResult 0
S4 HUMAN_REQUIRED / HumanGate PENDING / HumanResult-Judgment 0
```

Record canonical Replay:

```text
directory:
.aiassistant/reports/aiscc/replay/stockroom/v1

four members
zero-inference viewing
sanitized
corpus root:
a870da635941d7149edbbef911e8b2d75ff6fe12e8ade80c09dddc9086df795e
```

Historical limitations remain truthful/non-blocking:
- generic legacy P1-6 literal-offset compatibility deferred;
- stranded S3 v7 preserved/not reused.

## 12. DECISION_REGISTER

Append/update one terminal decision:

```text
decision_id:
AISCC-P2-3-CANONICAL-SCENARIO-REPLAY-CORPUS-V1

decision_status:
ACCEPTED / CLOSED

implementation_status:
PERSISTED

verification_status:
BROWSER_ACCEPTED / PRIVATE_RUNTIME_AND_REPLAY_INTEGRITY_VERIFIED
```

Include exact runtime matrix, Replay directory/root, 0145 and 0205 blocker lineage, zero-inference/sanitization, and `public release pending`.

Do not rewrite historical P0/P1 decisions.
Do not mark Public Bounded Live released.

## 13. NEXT_ACTIONS

Require:

```text
P2-1 → ACCEPTED / CLOSED
P2-2 → ACCEPTED / CLOSED
P2-3 → ACCEPTED / CLOSED
P2-4 → NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE
P2 → IN_PROGRESS
```

Current next action:

```text
phase:
P2-4

title:
Self-Dogfooding Cutover

status:
NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE
```

Keep P2-4 narrow:
one actual AISCC self-dogfood golden cycle; existing governance/runtime reuse; explicit self-dogfood provenance; no generic planner/autonomous loop/public deployment.

P3 must remain NOT_STARTED.

## 14. state consistency gate

Before Commit B prove across all three state files:

```text
P2-3 CLOSED consistent
P2-4 next executable consistent
P2 IN_PROGRESS
Replay root exact a870da635941d7149edbbef911e8b2d75ff6fe12e8ade80c09dddc9086df795e
Public Bounded Live NOT_RELEASED
public release NOT_COMPLETED
no stale P2-3 next action
no premature P3 entry
no false S4 HumanResult
```

## 15. Commit B — exact 3 paths

Stage exactly the three state files.

Commit message exactly:

```text
docs(aiscc): close p2-3 and enter p2-4
```

Require:
- parent = Commit A
- changed paths exact 3
- index empty
- tracked clean

No amend/squash/rebase.

## 16. final Git/semantic state

Final graph:

```text
23311b5283c9412e30783ae46a1925e85579247b
→ Commit A
→ Commit B
```

Move current retry Task active→done byte-exact after Commit B.

Final require:

```text
HEAD = Commit B
index empty
tracked clean
Git-visible untracked exactly one:
.aiassistant/tasks/done/20260914_0224_aiscc-p2-3-replay-canonical-path-basis-corrected-terminal-closure-retry-1.md

legacy 1400 preserved ignored/non-owned
no push
```

Final semantics:

```text
P2-3 ACCEPTED / CLOSED
P2-4 NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE
P2 IN_PROGRESS
Recorded Replay CANONICAL / PERSISTED
public Replay deployment NOT_COMPLETED
Public Bounded Live NOT_RELEASED
P3 NOT_STARTED
```

## 17. contract review

Exactly 70 rows:

```text
TRANSPORT_PACKAGE_EXACT
BASE_HEAD_PARENT_EXACT
INITIAL_INDEX_EMPTY_TRACKED_CLEAN
INITIAL_UNTRACKED_BLOCKED_LINEAGE_EXACT_3
BLOCKED_0205_ACTIVE_TASK_EXACT
PREDECESSOR_0205_RESULT_SHA_EXACT
PREDECESSOR_0205_ARCHIVE_INTEGRITY_PASS
CURRENT_STATE_PRE_HASHES_EXACT
LEGACY_1400_ACTIVE_PRESERVED
PYTHON_REPOSITORY_VENV_EXACT
0205_COMMAND_CENTER_DEFECT_ACCEPTED
PREDECESSOR_0145_RESULT_EXACT
PREDECESSOR_REPLAY_FOUR_MEMBERS_EXACT
CANDIDATE_CORPUS_ROOT_EXACT
BLOCKED_0205_TASK_ACTIVE_TO_DONE_BYTE_EXACT
PRE_COMMIT_A_UNTRACKED_EXACT_6
CANONICAL_REPLAY_DIRECTORY_ABSENT_BEFORE_CREATE
CANONICALIZATION_MEMBER_TWO_FIELDS_ONLY
CANONICAL_INDEX_MEMBER_PATH_BASIS_NORMALIZED_EXACT_4
CANONICAL_INDEX_OTHER_SEMANTICS_PRESERVED
CANONICAL_MEMBER_S1_HASH_EXACT
CANONICAL_MEMBER_S2_HASH_EXACT
CANONICAL_MEMBER_S3_HASH_EXACT
CANONICAL_MEMBER_S4_HASH_EXACT
CANONICAL_INDEX_HASH_EXACT
CANONICAL_CORPUS_ROOT_EXACT
CANONICAL_REPLAY_TRUTHFUL_SEMANTICS_PASS
CANONICAL_REPLAY_PUBLIC_RELEASE_PENDING
CANONICAL_REPLAY_PRIVATE_SANITIZATION_PASS
COMMIT_A_STAGE_SET_EXACT_11
COMMIT_A_PARENT_EXACT
COMMIT_A_MESSAGE_EXACT
COMMIT_A_CHANGED_PATHS_EXACT_11
POST_COMMIT_A_INDEX_EMPTY
POST_COMMIT_A_TRACKED_CLEAN
POST_COMMIT_A_UNTRACKED_ZERO
NO_PRIVATE_DB_RUNTIME_ACCESS
NO_SCENARIO_EXECUTION
NO_SOURCE_TEST_CONFIG_MUTATION
STATE_RECONCILIATION_ONLY_THREE_PATHS
CURRENT_STATE_P2_1_ACCEPTED_CLOSED
CURRENT_STATE_P2_2_ACCEPTED_CLOSED
CURRENT_STATE_P2_3_ACCEPTED_CLOSED
CURRENT_STATE_RUNTIME_MATRIX_EXACT
CURRENT_STATE_REPLAY_CORPUS_EXACT
CURRENT_STATE_P2_4_ENTRY_READY
CURRENT_STATE_PUBLIC_LIVE_NOT_RELEASED
DECISION_REGISTER_P2_3_ENTRY_PRESENT
DECISION_REGISTER_REPLAY_ROOT_EXACT
DECISION_REGISTER_HISTORICAL_LIMITATIONS_TRUTHFUL
DECISION_REGISTER_PUBLIC_RELEASE_PENDING
NEXT_ACTIONS_P2_3_CLOSED
NEXT_ACTIONS_P2_4_NEXT_EXECUTABLE
NEXT_ACTIONS_P2_IN_PROGRESS
NEXT_ACTIONS_NO_P3_PREMATURE_ENTRY
COMMIT_B_STAGE_SET_EXACT_3
COMMIT_B_PARENT_IS_COMMIT_A
COMMIT_B_MESSAGE_EXACT
COMMIT_B_CHANGED_PATHS_EXACT_3
FINAL_P2_3_ACCEPTED_CLOSED
FINAL_P2_4_ENTRY_READY_NEXT_EXECUTABLE
FINAL_P2_IN_PROGRESS
FINAL_PUBLIC_BOUNDED_LIVE_NOT_RELEASED
FINAL_PUBLIC_RELEASE_NOT_COMPLETED
NO_GIT_PUSH
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
FINAL_HEAD_IS_COMMIT_B
FINAL_INDEX_EMPTY_TRACKED_CLEAN
FINAL_UNTRACKED_CURRENT_DONE_TASK_ONLY
EXPORT_INTEGRITY_PASS
```

Success = `70 / 70 PASS`.

## 18. export

Root docs:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
0205_ACCEPTANCE_VERIFICATION.md
REPLAY_PATH_BASIS_CORRECTION_VERIFICATION.md
REPLAY_CANONICALIZATION_VERIFICATION.md
REPLAY_CANONICAL_INTEGRITY_VERIFICATION.md
COMMIT_A_VERIFICATION.md
STATE_RECONCILIATION_VERIFICATION.md
COMMIT_B_VERIFICATION.md
P2_3_TERMINAL_CLOSURE_VERIFICATION.md
PRIVATE_VALUE_SCAN.md
CONTRACT_REVIEW.md
```

Include:
- current Cycle/Judgment/done Task;
- blocked 0205 Cycle/Judgment/done Task;
- five canonical Replay files;
- final three canonical state files.

Manifest/member count from actual set.
Require one top-level, CRC PASS, exact SHA/size, TASK==current done Task, no private values.

## 19. success ceiling

```text
P2-3:
ACCEPTED / CLOSED

P2-4:
NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE

P2:
IN_PROGRESS

Recorded Replay:
CANONICAL / PERSISTED

public deployment:
NOT_COMPLETED

Public Bounded Live:
NOT_RELEASED

P3:
NOT_STARTED
```
