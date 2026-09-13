# 작업지시서: P2-3 Replay canonical persistence, terminal state reconciliation, and closure

## meta
- created_at: `2026-09-14T02:05:01+09:00`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `23311b5283c9412e30783ae46a1925e85579247b`
- required_base_parent: `a1c934ea75906a548f2bc4adc777c2a0ecc99be5`
- required_base_grandparent: `33a216f29062176ad196a567a299ba30291c3f72`
- accepted_0145_result_zip_sha256: `02ef19ba18e7f36de37f8cc1edfa6fd1228973f298c5735ee38402f1b14a995a`
- replay_canonical_persistence_authorized: `Yes`
- canonical_state_reconciliation_authorized: `Yes / exact three state paths`
- private_runtime_access_authorized: `No`
- retained_PostgreSQL_access_authorized: `No`
- source_test_config_write_authorized: `No`
- scenario_execution_authorized: `No`
- public_release_authorized: `No`
- push_authorized: `No`
- success_ceiling: `P2_3_ACCEPTED_CLOSED / P2_4_ENTRY_READY`

# 0. ordered authority

Strict order:

```text
A. bootstrap and exact repository/predecessor verification
B. derive canonical Replay bytes from the accepted 0145 candidate
C. Commit A: persist 0145 governance + canonical Replay corpus
D. reconcile exactly CURRENT_STATE_SUMMARY / DECISION_REGISTER / NEXT_ACTIONS
E. Commit B: persist state reconciliation
F. final closure verification
```

Do not access retained private DB/runtime.
Do not rerun any scenario.
Do not begin P2-4 implementation in this Task.

# 1. executables

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
PATH Python discovery
external Python/venv discovery
Docker
private PostgreSQL
```

# 2. repository baseline

Require:

```text
branch main
HEAD 23311b5283c9412e30783ae46a1925e85579247b
HEAD^ a1c934ea75906a548f2bc4adc777c2a0ecc99be5
HEAD^^ 33a216f29062176ad196a567a299ba30291c3f72
index empty
tracked clean

Git-visible untracked exactly one:
.aiassistant/tasks/done/20260914_0145_aiscc-p2-3-recorded-replay-corpus-capture-and-review-candidate-1.md

SHA-256:
f50b25b17265e8ec0870e1262389428d58989725eaf6c975b1bc494f75f62646
```

Canonical state pre-hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md` `281bd733624ac87be207f62ed59b99edf0d64cf3b8f3d00e9bc9611fe3179f8c`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md` `b55eb504c39af0134837f808eef8610b0c54505ee8c597b332f79148ad61d8bd`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md` `1bb251b5758e8fea1ac260dcace074dcb7e2ff9adf6a96e8699d29c66bea495d`

Preserve ignored non-owned legacy:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
SHA-256 52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

After current Cycle/Judgment placement with current Task active/ignored:

```text
Git-visible untracked exactly three:
0145 done Task
current Cycle
current Judgment
```

Mismatch → STOP before mutation.

# 3. exact predecessor Replay authority

The Executor-created predecessor result ZIP must exist at:

```text
.aiassistant/reports/target/20260914_0145_aiscc-p2-3-recorded-replay-corpus-capture-and-review-candidate-1.zip
```

Require SHA-256:

```text
02ef19ba18e7f36de37f8cc1edfa6fd1228973f298c5735ee38402f1b14a995a
```

Require:

```text
one top-level
22 members
21 manifest rows excluding self
CRC PASS
all manifest SHA/size exact
TASK.md SHA = f50b25b17265e8ec0870e1262389428d58989725eaf6c975b1bc494f75f62646
```

Candidate public members:

- `stockroom-s1-normal.json` candidate `d43dcd55047972e06c5cd978658f2ad8fecbda19e04cc238476e1d1c88ffdfec` / 12575 bytes → canonical `6fb493838b0158fc9a8416146e980e027fc1091ec77e0e3504f07b4b71ed26cc` / 12591 bytes
- `stockroom-s2-missing-evidence.json` candidate `456cbb587ff770ef6bf1d939c641d30db67570b2bbdd3b83f1397b3e159893b6` / 11739 bytes → canonical `103b98776d6e79867ea1e8ecac72a619c01a9223049434239e287381e2824201` / 11755 bytes
- `stockroom-s3-policy-conflict.json` candidate `2b3ffacbd1446d0d5b4667bea9acb7c84971773c7386b5bcc1efaca9c884d65d` / 9755 bytes → canonical `4ad9d71814ce5301fd48b6e40547229f6b76b16c36e69d722130eb82f03b1137` / 9771 bytes
- `stockroom-s4-human-owned-claim.json` candidate `7570c1423acb45046b0453e3c7c21b5203e5e480127b034e142f0216944cdbe3` / 13026 bytes → canonical `c6197411795760844bf74b8805476c35377117fb364423ec0a4cbf62734e3034` / 13042 bytes

Candidate index:

```text
REPLAY_CORPUS_INDEX.json
SHA-256 a281cc6eff744ba0b35e35dd5942142ae4f063bc979ef0995d82af72ccc95ec8

candidate corpus root:
48462d227a246e8501ea7fd087c07617dab26d8c818f82d098633e5df0c6949c
```

Any mismatch → STOP. Do not reconstruct candidate data from DB/runtime.

# 4. canonical Replay destination

Create only this canonical directory:

```text
.aiassistant/reports/aiscc/replay/stockroom/v1
```

It must be absent before this Task.

Canonical files exactly:

```text
.aiassistant/reports/aiscc/replay/stockroom/v1/REPLAY_CORPUS_INDEX.json
.aiassistant/reports/aiscc/replay/stockroom/v1/stockroom-s1-normal.json
.aiassistant/reports/aiscc/replay/stockroom/v1/stockroom-s2-missing-evidence.json
.aiassistant/reports/aiscc/replay/stockroom/v1/stockroom-s3-policy-conflict.json
.aiassistant/reports/aiscc/replay/stockroom/v1/stockroom-s4-human-owned-claim.json
```

No viewer, HTML, source code or deployment file in this Task.

# 5. deterministic candidate → canonical promotion

For each four candidate Replay JSON files:

1. read exact accepted candidate bytes from the verified predecessor ZIP;
2. parse UTF-8 JSON;
3. assert:
   - `schema_id == "AISCC-RECORDED-RUN-REPLAY-CANDIDATE-V1"`
   - `public_admission == "PENDING_BROWSER_REVIEW"`
4. change exactly:
   - `schema_id = "AISCC-RECORDED-RUN-REPLAY-V1"`
   - `public_admission = "CANONICAL_CORPUS_ACCEPTED_PUBLIC_RELEASE_PENDING"`
5. no other semantic field change;
6. serialize:
   - `ensure_ascii=False`
   - `sort_keys=True`
   - `indent=2`
   - exactly one trailing LF.

Canonical exact outputs:

- `.aiassistant/reports/aiscc/replay/stockroom/v1/stockroom-s1-normal.json`  12591 bytes  `6fb493838b0158fc9a8416146e980e027fc1091ec77e0e3504f07b4b71ed26cc`
- `.aiassistant/reports/aiscc/replay/stockroom/v1/stockroom-s2-missing-evidence.json`  11755 bytes  `103b98776d6e79867ea1e8ecac72a619c01a9223049434239e287381e2824201`
- `.aiassistant/reports/aiscc/replay/stockroom/v1/stockroom-s3-policy-conflict.json`  9771 bytes  `4ad9d71814ce5301fd48b6e40547229f6b76b16c36e69d722130eb82f03b1137`
- `.aiassistant/reports/aiscc/replay/stockroom/v1/stockroom-s4-human-owned-claim.json`  13042 bytes  `c6197411795760844bf74b8805476c35377117fb364423ec0a4cbf62734e3034`

Before writing, compare parsed objects after removing only `schema_id` and `public_admission`; candidate and canonical must be structurally identical.

# 6. canonical index promotion

Read exact candidate `REPLAY_CORPUS_INDEX.json`.

Change:

```text
public_admission:
PENDING_BROWSER_REVIEW
→ CANONICAL_CORPUS_ACCEPTED_PUBLIC_RELEASE_PENDING
```

Replace only member `member_sha256` / `member_bytes` with the exact canonical member values.
Replace `integrity_algorithm.canonical_tuples` accordingly.
Recompute the integrity root with the existing accepted algorithm:

```text
ordered by scenario_id ASCII ascending

tuple:
[scenario_id, member_sha256, member_bytes]

input:
UTF-8 compact JSON array
ensure_ascii=false
separators=(",", ":")
no whitespace
no trailing newline

hash:
SHA-256
```

Require root:

```text
a870da635941d7149edbbef911e8b2d75ff6fe12e8ade80c09dddc9086df795e
```

Serialize the index with sorted keys, indent 2, one trailing LF.

Require:

```text
bytes:
4084

SHA-256:
c92fb81c43cef9b1c379c2df8dac967aa55f4ddae73780d31f5d51c617aa38e0
```

All other index semantics remain exact.

# 7. canonical Replay truthfulness revalidation

Reparse all five canonical files and require:

```text
exact four scenarios
no duplicates

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

Recorded Run Replay labels:
present

live:
false

viewing_llm_inference_calls:
0
```

Require raw evidence body absent and the accepted sanitization/privacy boundary preserved.

Do not add any claim that these files are already publicly deployed.

# 8. Commit A — exact 8 paths

Stage exactly:

```text
.aiassistant/tasks/done/20260914_0145_aiscc-p2-3-recorded-replay-corpus-capture-and-review-candidate-1.md
.aiassistant/records/aiscc/cycles/20260914_0205_aiscc-p2-3-recorded-replay-final-acceptance-terminal-closure-1.cycle.md
.aiassistant/reports/aiscc/20260914_0205_aiscc-p2-3-0145-recorded-replay-corpus-final-acceptance-closure-authorization-1.md

.aiassistant/reports/aiscc/replay/stockroom/v1/REPLAY_CORPUS_INDEX.json
.aiassistant/reports/aiscc/replay/stockroom/v1/stockroom-s1-normal.json
.aiassistant/reports/aiscc/replay/stockroom/v1/stockroom-s2-missing-evidence.json
.aiassistant/reports/aiscc/replay/stockroom/v1/stockroom-s3-policy-conflict.json
.aiassistant/reports/aiscc/replay/stockroom/v1/stockroom-s4-human-owned-claim.json
```

Commit message exactly:

```text
feat(aiscc): admit stockroom recorded replay corpus
```

Require:

```text
Commit A parent = 23311b5283c9412e30783ae46a1925e85579247b
changed paths = exact 8
index empty after commit
```

Do not stage:
- current active Task;
- canonical state files yet;
- legacy 1400;
- reports/target;
- anything else.

# 9. state reconciliation scope

After Commit A, modify exactly these three tracked files:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

No broad timestamp/ID replacement.
Read the current canonical contents first and make narrow semantic updates.

No other tracked file may change.

# 10. CURRENT_STATE_SUMMARY reconciliation

The current summary must truthfully record at minimum:

```text
P2-1:
ACCEPTED / CLOSED

P2-2:
ACCEPTED / CLOSED

P2-3:
ACCEPTED / CLOSED

P2:
IN_PROGRESS

P2-4:
NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE

Public Bounded Live:
NOT_RELEASED

public deployment:
NOT_COMPLETED
```

Record P2-3 terminal evidence:

```text
S1:
ACCEPTED

S2:
REWORK_REQUIRED / HOLD_REWORK_REQUIRED

S3:
BLOCKED / POLICY_CONFLICT / provider-tool-Judgment-HumanResult 0

S4:
HUMAN_REQUIRED / HumanGate PENDING / HumanResult-Judgment 0

Recorded Replay:
4 canonical members
zero-inference viewing
sanitized
canonical corpus root a870da635941d7149edbbef911e8b2d75ff6fe12e8ade80c09dddc9086df795e

canonical Replay directory:
.aiassistant/reports/aiscc/replay/stockroom/v1
```

Record known non-blocking historical limitations truthfully:

```text
generic legacy P1-6 literal-offset fingerprint compatibility:
DEFERRED / historical v1 preserved

stranded historical S3 v7:
preserved / not reused
```

Do not describe those as active P2-3 blockers.

# 11. DECISION_REGISTER reconciliation

Append or update exactly one current P2-3 terminal decision entry:

```text
decision_id:
AISCC-P2-3-CANONICAL-SCENARIO-REPLAY-CORPUS-V1

decision:
Canonical Stockroom scenario pack and four-member Recorded Run Replay corpus are accepted as P2-3 terminal evidence.

decision_status:
ACCEPTED / CLOSED

implementation_status:
PERSISTED

verification_status:
BROWSER_ACCEPTED / PRIVATE_RUNTIME_AND_REPLAY_INTEGRITY_VERIFIED
```

The entry must cite:
- S1/S2/S3/S4 terminal semantics;
- `0145` accepted result SHA `02ef19ba18e7f36de37f8cc1edfa6fd1228973f298c5735ee38402f1b14a995a`;
- canonical Replay directory;
- canonical corpus root `a870da635941d7149edbbef911e8b2d75ff6fe12e8ade80c09dddc9086df795e`;
- zero-inference/read-only Replay;
- sanitization/IP/private-value verification;
- public release still pending;
- Public Bounded Live still NOT_RELEASED.

Do not rewrite historical P1/P0 decisions.

Do not change the accepted `AISCC-COMPETITION-PUBLIC-RUNTIME-V1` into a deployed fact.
Its public release/deployment verification remains future P3-owned work.

# 12. NEXT_ACTIONS reconciliation

Update roadmap truthfully:

```text
P2-1 → ACCEPTED / CLOSED
P2-2 → ACCEPTED / CLOSED
P2-3 → ACCEPTED / CLOSED
P2-4 → NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE
P2 → IN_PROGRESS
```

Current next action must become:

```text
phase:
P2-4

title:
Self-Dogfooding Cutover

status:
NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE
```

Keep scope narrow:

```text
one actual AISCC self-dogfood golden cycle
explicit self-dogfood execution mode/provenance
existing governance/runtime reuse
no generic planner
no autonomous loop
no public deployment
```

Do not mark P3 as entry-ready while P2-4 remains incomplete.

# 13. state semantic consistency check

Before Commit B, verify across all three state files:

```text
P2-3 CLOSED:
consistent

P2-4 next executable:
consistent

P2 overall:
IN_PROGRESS

Recorded Replay root:
exact a870da635941d7149edbbef911e8b2d75ff6fe12e8ade80c09dddc9086df795e

public release:
NOT_COMPLETED

Public Bounded Live:
NOT_RELEASED
```

Reject:
- duplicate conflicting P2-3 current statuses;
- stale `P2-1 NEXT_EXECUTABLE`;
- stale `P2 NOT_STARTED`;
- P3 premature next action;
- claim that Replay is publicly deployed;
- claim that HumanResult exists for S4.

# 14. Commit B — exact three state paths

Stage exactly:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

Commit message exactly:

```text
docs(aiscc): close p2-3 and enter p2-4
```

Require:

```text
Commit B parent = Commit A
changed paths = exact 3
index empty
tracked clean
```

No amend/squash/rebase.

# 15. final closure verification

Require final graph:

```text
23311b5283c9412e30783ae46a1925e85579247b
→ Commit A
→ Commit B
```

Final semantic state:

```text
P2-1:
ACCEPTED / CLOSED

P2-2:
ACCEPTED / CLOSED

P2-3:
ACCEPTED / CLOSED

P2-4:
NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE

P2:
IN_PROGRESS

Recorded Replay:
canonical/persisted
public release pending

Public Bounded Live:
NOT_RELEASED
```

No scenario/runtime/database/Docker access occurred.

# 16. Git terminal boundary

Move current Task active→done byte-identically after Commit B.

Final require:

```text
HEAD = Commit B
index empty
tracked clean

Git-visible untracked exactly one:
.aiassistant/tasks/done/20260914_0205_aiscc-p2-3-replay-canonical-persistence-terminal-state-reconciliation-and-closure-1.md

legacy 1400:
preserved / ignored / non-owned
```

Do not commit current done Task in this Task.
No push.

# 17. contract review

Exactly 66 rows:

```text
TRANSPORT_PACKAGE_EXACT
BASE_HEAD_PARENT_EXACT
INITIAL_INDEX_EMPTY_TRACKED_CLEAN
INITIAL_UNTRACKED_0145_DONE_TASK_ONLY
PREDECESSOR_0145_RESULT_ACCEPTED
PREDECESSOR_0145_RESULT_SHA_EXACT
CURRENT_STATE_PRE_HASHES_EXACT
LEGACY_1400_ACTIVE_PRESERVED
PYTHON_REPOSITORY_VENV_EXACT
PREDECESSOR_REPLAY_ARCHIVE_PRESENT_EXACT
PREDECESSOR_REPLAY_MANIFEST_EXACT
PREDECESSOR_REPLAY_FOUR_MEMBERS_EXACT
PREDECESSOR_REPLAY_INDEX_EXACT
CANDIDATE_CORPUS_ROOT_EXACT
CANONICALIZATION_ONLY_TWO_FIELDS_MEMBER
CANONICAL_MEMBER_S1_HASH_EXACT
CANONICAL_MEMBER_S2_HASH_EXACT
CANONICAL_MEMBER_S3_HASH_EXACT
CANONICAL_MEMBER_S4_HASH_EXACT
CANONICAL_INDEX_HASH_EXACT
CANONICAL_CORPUS_ROOT_EXACT
CANONICAL_REPLAY_LABEL_TRUTHFUL
CANONICAL_REPLAY_PUBLIC_RELEASE_PENDING
CANONICAL_REPLAY_NO_LIVE_CLAIM
CANONICAL_REPLAY_NO_RAW_EVIDENCE_BODY
CANONICAL_REPLAY_PRIVATE_SCAN_PASS
CANONICAL_REPLAY_FOUR_SCENARIOS_EXACT
COMMIT_A_STAGE_SET_EXACT_8
COMMIT_A_PARENT_EXACT
COMMIT_A_MESSAGE_EXACT
COMMIT_A_CHANGED_PATHS_EXACT_8
POST_COMMIT_A_INDEX_EMPTY
POST_COMMIT_A_TRACKED_CLEAN_EXCEPT_STATE_EDIT_PHASE
NO_PRIVATE_DB_RUNTIME_ACCESS
NO_SCENARIO_EXECUTION
NO_SOURCE_TEST_CONFIG_MUTATION
STATE_RECONCILIATION_ONLY_THREE_PATHS
CURRENT_STATE_P2_1_ACCEPTED_CLOSED
CURRENT_STATE_P2_2_ACCEPTED_CLOSED
CURRENT_STATE_P2_3_ACCEPTED_CLOSED
CURRENT_STATE_P2_3_RUNTIME_MATRIX_EXACT
CURRENT_STATE_REPLAY_CORPUS_EXACT
CURRENT_STATE_P2_4_ENTRY_READY
CURRENT_STATE_PUBLIC_LIVE_NOT_RELEASED
DECISION_REGISTER_P2_3_ENTRY_PRESENT
DECISION_REGISTER_REPLAY_ROOT_EXACT
DECISION_REGISTER_LEGACY_LIMITATIONS_TRUTHFUL
DECISION_REGISTER_PUBLIC_RELEASE_PENDING
NEXT_ACTIONS_P2_3_CLOSED
NEXT_ACTIONS_P2_4_NEXT_EXECUTABLE
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

Full closure success:

```text
66 / 66 PASS
```

# 18. export

Root docs:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
0145_ACCEPTANCE_VERIFICATION.md
REPLAY_CANONICALIZATION_VERIFICATION.md
REPLAY_CANONICAL_INTEGRITY_VERIFICATION.md
REPLAY_CANONICAL_SANITIZATION_VERIFICATION.md
COMMIT_A_VERIFICATION.md
STATE_RECONCILIATION_VERIFICATION.md
COMMIT_B_VERIFICATION.md
P2_3_TERMINAL_CLOSURE_VERIFICATION.md
PRIVATE_VALUE_SCAN.md
CONTRACT_REVIEW.md
```

Include project-relative copies of:
- current Cycle;
- current Judgment;
- current done Task;
- five canonical Replay files;
- final three canonical state files.

Generate manifest/member counts from actual declared set.

Require:
- one top-level;
- CRC PASS;
- manifest SHA/size exact;
- TASK.md == canonical done Task;
- canonical Replay hashes exact;
- no private values/paths/credentials;
- no source/test/config copies unless explicitly listed above.

# 19. success ceiling

```text
P2-3:
ACCEPTED / CLOSED

P2-4:
NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE

P2:
IN_PROGRESS

Recorded Replay corpus:
CANONICAL / PERSISTED

public Replay deployment:
NOT_COMPLETED

Public Bounded Live:
NOT_RELEASED

P3:
NOT_STARTED
```
