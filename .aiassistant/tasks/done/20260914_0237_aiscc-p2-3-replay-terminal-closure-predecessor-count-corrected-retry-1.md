# 작업지시서: P2-3 Replay terminal closure predecessor-count corrected retry

## meta
- created_at: `2026-09-14T02:37:32+09:00`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `23311b5283c9412e30783ae46a1925e85579247b`
- required_parent: `a1c934ea75906a548f2bc4adc777c2a0ecc99be5`
- required_grandparent: `33a216f29062176ad196a567a299ba30291c3f72`
- reviewed_0224_result_zip_sha256: `3bfd70ea1dfde1b23fe989dc961cdda4e641f7b1e126f6a5b7c1fb05171f0a95`
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

Two prior Command Center defects are now explicitly superseded only for retry authority:

```text
0205:
canonical-index path-basis permission was omitted.

0224:
0205 contract aggregate was transcribed incorrectly.
```

Preserved evidence itself must not be rewritten.

Exact predecessor facts:

```text
0205 result:
25 EXECUTED_PASS
1 EXECUTED_FAIL
40 BLOCKED_REQUIRED_EVIDENCE
total 66
sole failed row = CANONICAL_INDEX_HASH_EXACT

0224 result:
16 EXECUTED_PASS
54 BLOCKED_REQUIRED_EVIDENCE
70 declared rows
STOP reason = PREDECESSOR_CONTRACT_COUNT_AUTHORITY_CONFLICT
```

Strict order:

```text
A. verify repository + exact 0205/0224 results
B. move blocked 0205 and 0224 active Tasks → done byte-exact
C. derive canonical Replay with explicit index path-basis normalization
D. Commit A: historical blocker lineage + current entry + canonical Replay
E. reconcile exactly three canonical state files
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

```text
python
py
WindowsApps
PATH/external Python discovery
Docker
private PostgreSQL/runtime
```

## 2. exact repository baseline

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

Exact hashes:

```text
0145 done:
f50b25b17265e8ec0870e1262389428d58989725eaf6c975b1bc494f75f62646

0205 Cycle:
6180cdb13b8d174c0a65efc009de03e358e942e61b7ba4fb786015b03e6c3860

0205 Judgment:
ab746c87acb3c6ef9819f63e623c64385cdfec9edcba30d4de78b3b314bdb5b3
```

Require both blocked Tasks active/ignored:

```text
.aiassistant/tasks/active/20260914_0205_aiscc-p2-3-replay-canonical-persistence-terminal-state-reconciliation-and-closure-1.md
SHA-256 42ea6cb678299bb37e36ac4484fd3cd1e1df9c259a742e0c002eed10571dfcf4

.aiassistant/tasks/active/20260914_0224_aiscc-p2-3-replay-canonical-path-basis-corrected-terminal-closure-retry-1.md
SHA-256 d23c264fe101db193eb7bff71769772637ac4a89b5b8c513dd820139b5ff5244
```

Canonical Replay directory must be absent.

Canonical state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md` `281bd733624ac87be207f62ed59b99edf0d64cf3b8f3d00e9bc9611fe3179f8c`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md` `b55eb504c39af0134837f808eef8610b0c54505ee8c597b332f79148ad61d8bd`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md` `1bb251b5758e8fea1ac260dcace074dcb7e2ff9adf6a96e8699d29c66bea495d`

Preserve ignored legacy:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
SHA-256 52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

After current Cycle/Judgment placement while current Task active/ignored:

```text
Git-visible untracked exactly five
```

Mismatch → STOP before mutation.

## 3. exact 0205 predecessor evidence

Require 0205 result ZIP SHA:

```text
d113a377bcfc821106ee8180d597d73675019b9cf18c2f8eb891799c87e28fe3
```

Independently count its exact `CONTRACT_REVIEW.md` statuses.

Must equal:

```text
EXECUTED_PASS:
25

EXECUTED_FAIL:
1

BLOCKED_REQUIRED_EVIDENCE:
40

total:
66

sole failed row:
CANONICAL_INDEX_HASH_EXACT
```

Archive must still be:

```text
20 members
19 manifest rows excluding self
CRC PASS
TASK byte-exact
```

Any different aggregate → STOP.
Do not use the erroneous 21/1/44 text from the blocked 0224 Task.

## 4. exact 0224 predecessor evidence

Require 0224 result ZIP SHA:

```text
3bfd70ea1dfde1b23fe989dc961cdda4e641f7b1e126f6a5b7c1fb05171f0a95
```

Require:

```text
21 members
20 manifest rows excluding self
CRC PASS
TASK byte-exact

contract:
16 EXECUTED_PASS
54 BLOCKED_REQUIRED_EVIDENCE
70 declared rows

report stop:
PREDECESSOR_CONTRACT_COUNT_AUTHORITY_CONFLICT
```

Require no Git/canonical Replay/state/private-runtime mutation occurred.

## 5. close both blocked Task lineages

Move byte-exact:

```text
.aiassistant/tasks/active/20260914_0205_aiscc-p2-3-replay-canonical-persistence-terminal-state-reconciliation-and-closure-1.md
→ .aiassistant/tasks/done/20260914_0205_aiscc-p2-3-replay-canonical-persistence-terminal-state-reconciliation-and-closure-1.md

.aiassistant/tasks/active/20260914_0224_aiscc-p2-3-replay-canonical-path-basis-corrected-terminal-closure-retry-1.md
→ .aiassistant/tasks/done/20260914_0224_aiscc-p2-3-replay-canonical-path-basis-corrected-terminal-closure-retry-1.md
```

No content edit.

After both moves and before Replay creation:

```text
Git-visible untracked exactly seven:
0145 done
0205 Cycle
0205 Judgment
0205 done Task
0224 done Task
current Cycle
current Judgment
```

Current Task + legacy 1400 remain active/ignored.

## 6. accepted Replay source

Use only verified 0145 result ZIP:

```text
02ef19ba18e7f36de37f8cc1edfa6fd1228973f298c5735ee38402f1b14a995a
```

Candidate corpus root:

```text
48462d227a246e8501ea7fd087c07617dab26d8c818f82d098633e5df0c6949c
```

Do not reconstruct from DB/runtime.

## 7. canonical Replay destination

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

## 8. canonical member promotion

For four member JSONs change exactly:

```text
schema_id:
AISCC-RECORDED-RUN-REPLAY-CANDIDATE-V1
→ AISCC-RECORDED-RUN-REPLAY-V1

public_admission:
PENDING_BROWSER_REVIEW
→ CANONICAL_CORPUS_ACCEPTED_PUBLIC_RELEASE_PENDING
```

All other semantics exact.

Serialization:
`ensure_ascii=False`, `sort_keys=True`, `indent=2`, one trailing LF.

Canonical outputs:

- `stockroom-s1-normal.json` `6fb493838b0158fc9a8416146e980e027fc1091ec77e0e3504f07b4b71ed26cc` / 12591 bytes / final `ACCEPTED`
- `stockroom-s2-missing-evidence.json` `103b98776d6e79867ea1e8ecac72a619c01a9223049434239e287381e2824201` / 11755 bytes / final `REWORK_REQUIRED`
- `stockroom-s3-policy-conflict.json` `4ad9d71814ce5301fd48b6e40547229f6b76b16c36e69d722130eb82f03b1137` / 9771 bytes / final `BLOCKED`
- `stockroom-s4-human-owned-claim.json` `c6197411795760844bf74b8805476c35377117fb364423ec0a4cbf62734e3034` / 13042 bytes / final `HUMAN_REQUIRED`

## 9. canonical index promotion with explicit path basis

From candidate index change:

```text
public_admission:
PENDING_BROWSER_REVIEW
→ CANONICAL_CORPUS_ACCEPTED_PUBLIC_RELEASE_PENDING
```

Update each:
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

`member_relative_path` is relative to the canonical index directory and is not part of the integrity tuple.

Update canonical tuples with canonical hashes/sizes and recompute root using the accepted algorithm.

Require:

```text
canonical corpus root:
a870da635941d7149edbbef911e8b2d75ff6fe12e8ade80c09dddc9086df795e

canonical index bytes:
4084

canonical index SHA-256:
c92fb81c43cef9b1c379c2df8dac967aa55f4ddae73780d31f5d51c617aa38e0
```

All other index semantics exact.

## 10. canonical Replay truthfulness

Require:

```text
S1:
ACCEPTED / Judgment ACCEPTED

S2:
REWORK_REQUIRED / HOLD_REWORK_REQUIRED

S3:
BLOCKED / POLICY_CONFLICT
provider/tool/Judgment/HumanResult 0

S4:
HUMAN_REQUIRED
HumanGate PENDING
HumanResult/Judgment 0

Recorded Run Replay labels present
live=false
viewing_llm_inference_calls=0
raw evidence body absent
private values absent
public release pending
```

No deployment claim.

## 11. Commit A — exact 12 paths

Stage exactly:

```text
.aiassistant/tasks/done/20260914_0145_aiscc-p2-3-recorded-replay-corpus-capture-and-review-candidate-1.md
.aiassistant/records/aiscc/cycles/20260914_0205_aiscc-p2-3-recorded-replay-final-acceptance-terminal-closure-1.cycle.md
.aiassistant/reports/aiscc/20260914_0205_aiscc-p2-3-0145-recorded-replay-corpus-final-acceptance-closure-authorization-1.md
.aiassistant/tasks/done/20260914_0205_aiscc-p2-3-replay-canonical-persistence-terminal-state-reconciliation-and-closure-1.md
.aiassistant/tasks/done/20260914_0224_aiscc-p2-3-replay-canonical-path-basis-corrected-terminal-closure-retry-1.md

.aiassistant/records/aiscc/cycles/20260914_0237_aiscc-p2-3-predecessor-count-corrected-terminal-closure-entry-1.cycle.md
.aiassistant/reports/aiscc/20260914_0237_aiscc-p2-3-0224-predecessor-count-authority-conflict-judgment-1.md

.aiassistant/reports/aiscc/replay/stockroom/v1/REPLAY_CORPUS_INDEX.json
.aiassistant/reports/aiscc/replay/stockroom/v1/stockroom-s1-normal.json
.aiassistant/reports/aiscc/replay/stockroom/v1/stockroom-s2-missing-evidence.json
.aiassistant/reports/aiscc/replay/stockroom/v1/stockroom-s3-policy-conflict.json
.aiassistant/reports/aiscc/replay/stockroom/v1/stockroom-s4-human-owned-claim.json
```

Commit message exactly:

```text
feat(aiscc): admit replay corpus and preserve closure blockers
```

Require:
- parent `23311b5283c9412e30783ae46a1925e85579247b`
- changed paths exact 12
- index empty
- tracked clean
- Git-visible untracked zero

Do not stage current Task or state files yet.

## 12. state reconciliation

After Commit A modify exactly:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

No broad replacement.

CURRENT_STATE must truthfully establish:

```text
P2-1 ACCEPTED / CLOSED
P2-2 ACCEPTED / CLOSED
P2-3 ACCEPTED / CLOSED
P2-4 NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE
P2 IN_PROGRESS
Public Bounded Live NOT_RELEASED
public deployment NOT_COMPLETED
```

P2-3 terminal evidence:

```text
S1 ACCEPTED
S2 REWORK_REQUIRED / HOLD_REWORK_REQUIRED
S3 BLOCKED / POLICY_CONFLICT / provider-tool-Judgment-HumanResult 0
S4 HUMAN_REQUIRED / HumanGate PENDING / HumanResult-Judgment 0

canonical Replay:
.aiassistant/reports/aiscc/replay/stockroom/v1

corpus root:
a870da635941d7149edbbef911e8b2d75ff6fe12e8ade80c09dddc9086df795e

four members
zero-inference viewing
sanitized
```

Historical limitations remain non-blocking:
- generic legacy P1-6 literal-offset compatibility deferred;
- stranded S3 v7 preserved/not reused;
- 0205/0224 closure blockers recorded as Command Center contract defects.

## 13. DECISION_REGISTER

Append/update terminal decision:

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

Include:
- exact S1-S4 terminal matrix;
- accepted 0145 Replay evidence;
- canonical directory/root;
- 0205 path-basis blocker lineage;
- 0224 predecessor-count blocker lineage;
- zero-inference/read-only/sanitization;
- public release pending.

Do not rewrite historical P0/P1 decisions.
Do not mark Public Bounded Live released.

## 14. NEXT_ACTIONS

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

Scope:
one actual AISCC self-dogfood golden cycle; explicit self-dogfood provenance; reuse existing governance/runtime; no generic planner/autonomous loop/public deployment.

P3 remains NOT_STARTED.

## 15. state consistency gate

Before Commit B require all three state files agree:

```text
P2-3 CLOSED
P2-4 next executable
P2 IN_PROGRESS
Replay root exact a870da635941d7149edbbef911e8b2d75ff6fe12e8ade80c09dddc9086df795e
Public Bounded Live NOT_RELEASED
public release NOT_COMPLETED
P3 NOT_STARTED
no false S4 HumanResult
no stale P2-3 next action
```

## 16. Commit B — exact 3 paths

Stage exactly the three canonical state files.

Commit message exactly:

```text
docs(aiscc): close p2-3 and enter p2-4
```

Require:
- parent = Commit A
- changed paths exact 3
- index empty
- tracked clean
- no amend/squash/rebase

## 17. final terminal state

Move current Task active→done byte-exact after Commit B.

Final graph:

```text
23311b5283c9412e30783ae46a1925e85579247b
→ Commit A
→ Commit B
```

Final require:

```text
HEAD = Commit B
index empty
tracked clean

Git-visible untracked exactly one:
.aiassistant/tasks/done/20260914_0237_aiscc-p2-3-replay-terminal-closure-predecessor-count-corrected-retry-1.md

legacy 1400 preserved ignored/non-owned
no push
```

Final semantics:

```text
P2-3 ACCEPTED / CLOSED
P2-4 NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE
P2 IN_PROGRESS
Recorded Replay CANONICAL / PERSISTED
public deployment NOT_COMPLETED
Public Bounded Live NOT_RELEASED
P3 NOT_STARTED
```

## 18. contract review

Exactly 76 rows:

```text
TRANSPORT_PACKAGE_EXACT
BASE_HEAD_PARENT_EXACT
INITIAL_INDEX_EMPTY_TRACKED_CLEAN
INITIAL_UNTRACKED_BLOCKED_BASELINE_EXACT_3
BLOCKED_0205_ACTIVE_TASK_EXACT
BLOCKED_0224_ACTIVE_TASK_EXACT
PREDECESSOR_0205_RESULT_SHA_EXACT
PREDECESSOR_0205_ARCHIVE_INTEGRITY_PASS
PREDECESSOR_0205_CONTRACT_25_1_40_EXACT
PREDECESSOR_0205_SOLE_FAIL_INDEX_HASH_EXACT
PREDECESSOR_0224_RESULT_SHA_EXACT
PREDECESSOR_0224_ARCHIVE_INTEGRITY_PASS
PREDECESSOR_0224_CONTRACT_16_54_EXACT
PREDECESSOR_0224_STOP_REASON_EXACT
CURRENT_STATE_PRE_HASHES_EXACT
LEGACY_1400_ACTIVE_PRESERVED
PYTHON_REPOSITORY_VENV_EXACT
PREDECESSOR_0145_RESULT_EXACT
CANDIDATE_REPLAY_CORPUS_ROOT_EXACT
BLOCKED_0205_TASK_ACTIVE_TO_DONE_BYTE_EXACT
BLOCKED_0224_TASK_ACTIVE_TO_DONE_BYTE_EXACT
PRE_COMMIT_A_UNTRACKED_EXACT_7
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
COMMIT_A_STAGE_SET_EXACT_12
COMMIT_A_PARENT_EXACT
COMMIT_A_MESSAGE_EXACT
COMMIT_A_CHANGED_PATHS_EXACT_12
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

Success = `76 / 76 PASS`.

## 19. export

Root docs:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
0205_ACCEPTANCE_VERIFICATION.md
0224_ACCEPTANCE_VERIFICATION.md
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
- blocked 0205 done Task;
- blocked 0224 done Task;
- five canonical Replay files;
- final three canonical state files.

Generate manifest/member counts from actual set.

Require:
- one top-level;
- CRC PASS;
- exact SHA/size;
- TASK.md == current done Task;
- no private values/paths/credentials.

## 20. success ceiling

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
