# 작업지시서: P2-3 S1 canonical execution bound-ref contract + source rework

## meta

- task_id: `20260912_2158_aiscc-p2-3-s1-canonical-execution-bound-ref-contract-and-source-rework-1`
- created_at: `2026-09-12T21:58:22+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `SOURCE_REWORK / CANONICAL_BOUND_REF_CONTRACT`
- evidence_profile: `HIGH_RISK_SOURCE`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `ee623c995cf1c24b4a362834f2d6d1fdf71a30cd`
- required_parent: `4096913e9a117bd49bfecdb1ce5ca8de2735d661`
- required_grandparent: `6d41633210f0e556dd4292ee62a8600c6b54215f`
- fresh_ide_executor_chat: `FORBIDDEN`
- executor_session_action: `KEEP_EXISTING_2125_IDE_EXECUTOR_CHAT`
- python_executable: `C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe`
- success_ceiling: `S1_EXECUTION_PROVENANCE_LINK_CORRECTED_CANDIDATE / BROWSER_REVIEW_PENDING`
- private_s1_execution_authorized: `No`

# 0. session and Python rule

Continue the existing 2125 IDE Executor chat.
Do not open a new IDE chat.

For every Python invocation use the exact executable:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe
```

Forbidden:

```text
python
py
WindowsApps Python alias
PATH Python discovery
```

This exact Python path is a known environment fact, not a discovery task.

# 1. purpose

Implement the Command Center-defined canonical execution producer binding contract.

Required simultaneous truths:

```text
CURRENT:
ADMISSION_PENDING/current_version

PRODUCER:
verified ExecutionSubmissionRef
RUNNING/producer_version
exact submission_id
exact execution_attempt_id

LINK:
the current ADMISSION_PENDING is the exact admitted successor transition whose
G_EXECUTOR_SUBMISSION guard bound the same verified submission+attempt identities
```

# 2. transport

Verify Short Prompt ZIP filename/SHA-256 with the exact Python executable above.
Require exactly three flat safe members.

Place current Task first:

```text
.aiassistant/tasks/active/20260912_2158_aiscc-p2-3-s1-canonical-execution-bound-ref-contract-and-source-rework-1.md
```

Require byte equality and ignored status.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260912_2158_aiscc-p2-3-s1-bound-ref-contract-defined-source-rework-entry-1.cycle.md
SHA-256:
85194e69195c77f5e2490b586a7113ffbcb1fd426c4bba5362064bd4a379ebac

.aiassistant/reports/aiscc/20260912_2158_aiscc-p2-3-s1-bound-ref-contract-definition-judgment-1.md
SHA-256:
c99df7f4b9ec25c59dc7d08a931c0770e7cda9c79828f6fae8416cfb94f28247
```

Bootstrap mismatch:

```text
STOP
no source write
no tests
no report/export
```

# 3. repository baseline

Require:

```text
branch main
HEAD ee623c995cf1c24b4a362834f2d6d1fdf71a30cd
HEAD^ 4096913e9a117bd49bfecdb1ce5ca8de2735d661
HEAD^^ 6d41633210f0e556dd4292ee62a8600c6b54215f
index empty
tracked worktree clean
```

Before current delivery Git-visible untracked exactly these 15 predecessor artifacts:

- `.aiassistant/tasks/done/20260912_1749_aiscc-p2-3-private-s1-normal-scenario-execution-and-capture-1.md`  `0668ed1fb71ce57f6b87dacb91c810f7505596eb6efe835841c019f3a2d51ecd`
- `.aiassistant/records/aiscc/cycles/20260912_1749_aiscc-p2-3-cut-c-persisted-private-s1-execution-entry-1.cycle.md`  `75fe2a744d010e327ff2d549aa998e2e64e0449735d50eec69a4fd6a183044ad`
- `.aiassistant/reports/aiscc/20260912_1749_aiscc-p2-3-cut-c-persistence-final-acceptance-private-s1-authorization-judgment-1.md`  `6457922c2520c2255edf9574b1c68c3ed633c3615e80be5c95c7e04f9e5961ed`
- `.aiassistant/tasks/done/20260912_1954_aiscc-p2-3-private-s1-acl-query-transport-retry-1.md`  `f3fbe8fed5d2dfcc6ac6b4586567b410e64653f648943f162219b11648ab3819`
- `.aiassistant/records/aiscc/cycles/20260912_1954_aiscc-p2-3-private-s1-acl-query-transport-blocked-retry-entry-1.cycle.md`  `1bb88d04b2e567a9b11ab8fb99449571696a5e039571cef6438fa62bb3fea870`
- `.aiassistant/reports/aiscc/20260912_1954_aiscc-p2-3-private-s1-acl-query-transport-blocker-hold-judgment-1.md`  `ee9436791b8595333090eb2a06b295ef4b3b87f620894756fea0a97176ebd25d`
- `.aiassistant/tasks/done/20260912_2024_aiscc-p2-3-s1-admission-pending-evidence-state-contract-source-rework-1.md`  `c61d14d7cb8fd3ac929701550a3530577eed99ad083b0bacee29f55c27d7584c`
- `.aiassistant/records/aiscc/cycles/20260912_2024_aiscc-p2-3-s1-source-state-contract-defect-rework-entry-1.cycle.md`  `8c9ca5c06d658e9e2723ee70b2b54b999801cf17494543480caf7743840e7a44`
- `.aiassistant/reports/aiscc/20260912_2024_aiscc-p2-3-s1-source-state-contract-defect-confirmed-judgment-1.md`  `c8a921efc6112c2bbd8532ed0869e08e9c1f1eebea4121805f0c839ad3bbf0c2`
- `.aiassistant/tasks/done/20260912_2052_aiscc-p2-3-s1-current-state-producer-provenance-decoupling-source-rework-1.md`  `bf1c50f34cdd21ccf14d3009aeb309df3904d8903fdbeb30063b911c4a4279f3`
- `.aiassistant/records/aiscc/cycles/20260912_2052_aiscc-p2-3-s1-current-state-producer-provenance-rework-entry-1.cycle.md`  `119f40188ec87d4e98d0152f9c762a90d40f1096316beaba158cc0244b19ce5f`
- `.aiassistant/reports/aiscc/20260912_2052_aiscc-p2-3-s1-current-state-producer-provenance-conflict-judgment-1.md`  `cefcaa10a62e80779121bbf1014caa748195c48cb62d48c5e2406b99cc77bc37`
- `.aiassistant/tasks/done/20260912_2125_aiscc-p2-3-s1-execution-guard-producer-binding-source-rework-1.md`  `51f718131e55004b8f9cb2cfa80889baf52bdac9151d37d0a5e34ec138df891a`
- `.aiassistant/records/aiscc/cycles/20260912_2125_aiscc-p2-3-s1-execution-guard-producer-binding-rework-entry-1.cycle.md`  `fd7877ecab06d40dcac3a36f99a5b0ad72c94a0ffb055a1dab51d79defd4327f`
- `.aiassistant/reports/aiscc/20260912_2125_aiscc-p2-3-s1-execution-guard-producer-binding-scope-expansion-judgment-1.md`  `06cb0d64c092417d1dfd4b98279a9a9b0d8df41e169ac9a2b410f130fadfc7bc`

After current Cycle/Judgment placement while current Task remains active/ignored:

```text
Git-visible untracked:
17 exact

15 predecessors
current Cycle
current Judgment
```

Canonical state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `7d0c9954b87e945b8c1c3fb66bda2dd54d23d5c3319202ef9fb24aa0ac56f424`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `04ec792c5e6dd4a7c8d2d35b716d1ed1fd569e60bb557532b811bc33dd434946`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `61ae340fa06e3d87d80f3308a240dacc1e0ba132a3b241a2059757830cf6312a`

Unexpected path/delta:

```text
DIRTY_WORKSPACE_MIXED
→ STOP_WITH_REPORT_EXPORT
```

# 4. exact five source baselines

Require all exact before mutation:

- `src/aiscc/workflow/guards.py`  `0ad7c75e22755ecd2132805e6c143b99489eea8d7807a505f3798736a0364ba2`
- `src/aiscc/persistence/repository.py`  `74a497fd32eb42176afd19b2ba621da04364b847b0130f52966bcb3001159dd1`
- `src/aiscc/scenarios/capture_runner.py`  `600de0a4b0e718f02ab2e1907b7be62b2c4a23756559fdf99cb4cd55fb80b3d2`
- `src/aiscc/scenarios/stockroom_production.py`  `685e2ec549473e167ed1fe4d7de1050d7a53a449d1d278dcdb3439a471478f1f`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`  `373f9d5bc6f260785cdf943aa649ce99ab5826e8ae09dd2982c18db09459fbf5`

Maximum modifiable tracked paths remain exactly these five.
A subset may be modified:

```text
src/aiscc/workflow/guards.py
src/aiscc/persistence/repository.py
src/aiscc/scenarios/capture_runner.py
src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

No model/schema/migration/config/state path is authorized.

# 5. canonical V1 bound-ref encoding

Command Center freezes the following contract.

For verified `ExecutionSubmissionRef` values:

```text
submission_id = S
execution_attempt_id = A
```

produce exactly:

```text
(
  "aiscc-bound-ref:v1:execution-submission:" + BASE64URL_NOPAD_UTF8(S),
  "aiscc-bound-ref:v1:execution-attempt:" + BASE64URL_NOPAD_UTF8(A),
)
```

## 5.1 BASE64URL_NOPAD_UTF8 encoder

Input:

```text
non-empty Python str
```

Algorithm:

```text
strict UTF-8 encode
URL-safe RFC 4648 Base64
strip trailing "=" padding
payload must remain non-empty
```

No Unicode normalization.
No lower/upper case folding.

## 5.2 decoder

Require exact prefix, type and payload.

Payload alphabet:

```text
A-Z a-z 0-9 _ -
```

No `=` is allowed in stored payload.

Decode by restoring only mathematically required padding.
Use strict base64 validation with URL-safe alphabet.
Decode bytes as strict UTF-8.
Decoded identifier must be non-empty.

Then re-encode with 5.1 and require byte-for-byte/string-for-string equality to the original payload.

Any mismatch:

```text
NON_CANONICAL_BOUND_REF
→ fail closed
```

## 5.3 tuple/cardinality

For `G_EXECUTOR_SUBMISSION`:

```text
tuple length:
exactly 2

index 0 type:
execution-submission

index 1 type:
execution-attempt

extra:
forbidden

wrong order:
forbidden

duplicate type:
forbidden

unknown type/version/prefix:
forbidden
```

# 6. authority source

The encoded IDs may be created only after existing `ExecutionReferenceAuthority.verify(...)`
has authenticated the issuer-backed `ExecutionSubmissionRef`.

Never accept caller-provided submission/attempt strings as sufficient authority.

The canonical encoder may accept identifiers as a pure helper, but production guard issuance must call it only
with fields from the verified authority result/object.

# 7. G_EXECUTOR_SUBMISSION issuance

Preserve existing P1-4/P1-5 separation.

For `G_EXECUTOR_SUBMISSION`:

```text
issue_from_execution_ref
→ verify producer ref first
→ derive canonical two-entry bound_refs
→ issue trusted guard fact
```

Generic/unverified guard issuance must not be able to mint a valid `G_EXECUTOR_SUBMISSION` with caller-selected bindings.

Implement a bounded owner-specific issuance path if necessary within `guards.py`.

Require exact fact:

```text
guard:
G_EXECUTOR_SUBMISSION

authority owner:
existing P1-5 execution authority contract

bound_refs:
canonical exact two-entry tuple
```

Do not treat those refs as evidence refs.

# 8. required-bound-ref validation

Update the existing guard validation so that `G_EXECUTOR_SUBMISSION` cannot have empty `bound_refs`.

Require canonical decoder/cardinality validation.

For facts reconstructed historically:

```text
missing:
deny

one item:
deny

more than two:
deny

wrong prefix/type/order:
deny

malformed/noncanonical Base64URL:
deny
```

Do not auto-upgrade or repair old incomplete rows.

# 9. persistence and historical verification

2125 established that current storage already preserves generic string `bound_refs`.

Do not change schema/model/migration.

Ensure existing fingerprint/serialization/reconstruction continues to preserve the exact two strings.

Historical verification of the exact predecessor transition must fail closed unless the admitted
`G_EXECUTOR_SUBMISSION` guard contains a canonical valid two-entry binding.

Expose the verified canonical binding through existing reconstructed guard facts/evaluation structures;
do not add a persistence column merely for convenience.

# 10. runner predecessor identity

Keep source-owned order unchanged:

```text
execute
→ RUNNING_TO_ADMISSION_PENDING transition admitted
→ runtime evidence submission
```

Thread the minimum exact immutable admitted transition identity to `submit_runtime_evidence`.

Prefer the existing admitted transition `owner_ref`/decision identity already returned by the source-owned adapter.

Do not pass caller-authored state/version claims.

# 11. adapter CURRENT / PRODUCER / LINK proof

Before creating runtime EvidenceCandidate, establish independently:

## CURRENT

Using existing `_current` fail-closed authority:

```text
state = ADMISSION_PENDING
current_version exact
same WorkRun/task
```

## LINK

Using the exact predecessor transition identity:

```text
historical decision = ADMITTED
source state = RUNNING
target state = ADMISSION_PENDING
result state/version = CURRENT
same WorkRun
G_EXECUTOR_SUBMISSION bound_refs canonical and exact
```

Decode the bound refs to:

```text
linked_submission_id
linked_attempt_id
```

## PRODUCER

Use independently verified LINK source state/version as the expected producer context for
`ExecutionReferenceAuthority.verify(...)`.

Require verified producer ref:

```text
state = RUNNING
state_version = LINK source version
submission_id = linked_submission_id
execution_attempt_id = linked_attempt_id
same WorkRun/task
```

Do not derive expected producer state/version only from unverified producer-ref fields.

Only CURRENT + LINK + PRODUCER PASS may proceed to evidence candidate submission.

# 12. non-substitution

Preserve exactly:

```text
ExecutionSubmissionRef
!= EvidenceCandidate
!= AdmittedEvidence
!= G_EVIDENCE
```

The bound refs prove only which P1-5 producer authorized the historical `G_EXECUTOR_SUBMISSION`.

# 13. regression requirements

Use the existing integration test path.

Required positive:

```text
verified RUNNING/vN producer
canonical submission+attempt bound refs
admitted RUNNING/vN → ADMISSION_PENDING/vN+1
historical reconstruction retains exact refs
current ADMISSION_PENDING/vN+1
same exact producer
→ runtime evidence submission reaches normal admission path
```

Required negatives:

```text
empty ID encoder:
reject

wrong prefix:
reject

bad Base64URL:
reject

noncanonical Base64URL:
reject

wrong cardinality:
reject

wrong order/type:
reject

missing historical submission binding:
deny

missing historical attempt binding:
deny

wrong submission:
deny

wrong attempt:
deny

wrong producer version:
deny

unrelated ADMISSION_PENDING predecessor:
deny

authentic ExecutionSubmissionRef alone:
no AdmittedEvidence / no G_EVIDENCE
```

Also prove:

```text
runner order unchanged
_current remains fail closed
ExecutionReferenceAuthority.verify semantics not weakened
```

# 14. validation

Use only:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe
```

Run:

```text
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m py_compile
  src/aiscc/workflow/guards.py
  src/aiscc/persistence/repository.py
  src/aiscc/scenarios/capture_runner.py
  src/aiscc/scenarios/stockroom_production.py
  tests/integration/scenarios/test_stockroom_capture_runner.py

"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -m ruff check
  src/aiscc/workflow/guards.py
  src/aiscc/persistence/repository.py
  src/aiscc/scenarios/capture_runner.py
  src/aiscc/scenarios/stockroom_production.py
  tests/integration/scenarios/test_stockroom_capture_runner.py

"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q
  tests/integration/scenarios/test_stockroom_capture_runner.py

"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q
  tests/unit
```

Do not start Docker/PostgreSQL/private runtime to satisfy tests.

# 15. Git boundary

No staging/commit/push.

Forbidden:

```text
git add
git commit
git push
git reset
git restore
git checkout
git stash
git clean
```

Before Task movement:

```text
modified tracked paths:
non-empty subset of allowed five only

index:
empty

Git-visible untracked:
17 exact
```

Move current Task byte-identically:

```text
.aiassistant/tasks/active/20260912_2158_aiscc-p2-3-s1-canonical-execution-bound-ref-contract-and-source-rework-1.md
→
.aiassistant/tasks/done/20260912_2158_aiscc-p2-3-s1-canonical-execution-bound-ref-contract-and-source-rework-1.md
```

Final Git-visible untracked:

```text
18 exact

15 predecessors
current Cycle
current Judgment
current done Task
```

# 16. runtime prohibition

Do not access:

```text
Docker
PostgreSQL
private password/runtime root
provider/network runtime
prepare_capture
WorkRun runtime creation
S1/S2/S3/S4
Replay
```

No canonical state mutation.

# 17. contract review

Require exactly 48 rows:

```text
TRANSPORT_PACKAGE_EXACT
BASE_HEAD_PARENT_EXACT
PREDECESSOR_15_ARTIFACTS_EXACT
CURRENT_STATE_HASHES_EXACT
FIVE_SOURCE_BASELINES_EXACT
PYTHON_EXECUTABLE_EXACT
BOUND_REF_STORAGE_RECONSTRUCTION_EXISTING
CANONICAL_ENCODING_DEFINED_EXACT
ENCODER_DECODER_CANONICAL_ROUNDTRIP
ENCODER_REJECTS_EMPTY_ID
DECODER_REJECTS_WRONG_PREFIX
DECODER_REJECTS_BAD_BASE64URL
DECODER_REJECTS_NONCANONICAL_PAYLOAD
DECODER_REJECTS_WRONG_CARDINALITY
DECODER_REJECTS_DUPLICATE_OR_WRONG_ORDER_TYPE
ISSUER_VERIFIED_REF_ONLY
G_EXECUTOR_SUBMISSION_REQUIRES_EXACT_TWO_BINDINGS
GENERIC_UNVERIFIED_ISSUANCE_DENIED
HISTORICAL_RECONSTRUCTION_PRESERVES_EXACT_BINDINGS
HISTORICAL_MISSING_BINDING_DENIED
HISTORICAL_MALFORMED_BINDING_DENIED
HISTORICAL_WRONG_TYPE_ORDER_DENIED
CURRENT_STATE_ADMISSION_PENDING_EXACT
PRODUCER_RUNNING_VERSION_IMMUTABLE
PREDECESSOR_TRANSITION_IDENTITY_THREADED
PREDECESSOR_LINK_EXACT_SAME_RUN_ATTEMPT
EXECUTION_REFERENCE_VERIFY_NOT_WEAKENED
P1_6_NON_SUBSTITUTION_PRESERVED
RUNNER_ORDER_UNCHANGED
NO_STATE_VERSION_REBIND
MODIFIED_PATHS_WITHIN_ALLOWED_5
POSITIVE_LINK_REGRESSION_PASS
WRONG_SUBMISSION_REGRESSION_DENIED
WRONG_ATTEMPT_REGRESSION_DENIED
WRONG_PRODUCER_VERSION_REGRESSION_DENIED
UNRELATED_PENDING_TRANSITION_REGRESSION_DENIED
REF_ONLY_NON_SUBSTITUTION_REGRESSION_PASS
TARGETED_SCENARIO_PYTEST_PASS
UNIT_REGRESSION_PYTEST_PASS
RUFF_PASS
PY_COMPILE_PASS
NO_DOCKER_DB_PRIVATE_ACCESS
NO_S1_S4_EXECUTION
NO_CANONICAL_STATE_MUTATION
NO_GIT_COMMIT_PUSH
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
FINAL_DIFF_WITHIN_ALLOWED_5
EXPORT_INTEGRITY_PASS
```

Success:

```text
48 / 48 PASS
```

Blocked rows remain `BLOCKED_REQUIRED_EVIDENCE`.

# 18. success export

Root docs exactly 14:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
BOUND_REF_CONTRACT_VERIFICATION.md
GUARD_PROVENANCE_VERIFICATION.md
HISTORICAL_PROVENANCE_VERIFICATION.md
CURRENT_PRODUCER_LINK_VERIFICATION.md
RUNNER_LINKAGE_VERIFICATION.md
PATCH_VERIFICATION.md
TEST_VERIFICATION.md
GIT_DIFF_VERIFICATION.md
NO_RUNTIME_EXECUTION_VERIFICATION.md
CONTRACT_REVIEW.md
```

Include project-relative copies of:

```text
current Cycle
current Judgment
current done Task
all five bounded source/test paths
```

Success export:

```text
22 total members
21 non-self manifest rows
one top-level directory
CRC PASS
folder/archive byte equality
TASK.md == current done Task
```

# 19. mandatory stop

Stop before source write if:

```text
2125 storage finding no longer reproduces
the defined encoding cannot be implemented without model/schema/migration change
existing verified producer object does not expose exact submission_id + attempt_id
```

Stop after source write if:

```text
path outside allowed five changes
compile/lint/test fails
authority verification is weakened
runtime/private access is attempted
```

Do not broaden scope.

# 20. success ceiling

```text
canonical execution bound-ref contract:
DEFINED / IMPLEMENTED_CANDIDATE

G_EXECUTOR_SUBMISSION producer binding:
exact submission + attempt / durable

current evidence-review authority:
ADMISSION_PENDING

producer authority:
RUNNING/original version / immutable

historical predecessor linkage:
VERIFIED

private S1 runtime:
NOT_EXECUTED

Browser source acceptance:
HUMAN_PENDING

Git persistence:
NOT_PERFORMED

P2-3:
IN_PROGRESS
```
