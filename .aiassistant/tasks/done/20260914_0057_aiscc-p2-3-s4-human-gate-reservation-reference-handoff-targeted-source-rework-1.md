# 작업지시서: P2-3 S4 HumanGate reservation-reference handoff targeted source rework

## meta
- created_at: `2026-09-14T00:57:21+09:00`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `33a216f29062176ad196a567a299ba30291c3f72`
- required_parent: `be2489515ba7799466ffdf415b47e4d3e0a79e46`
- required_grandparent: `c26ec9eb342d052c726c57b5df42ced70e01a757`
- reviewed_0039_result_zip_sha256: `9796fdba7b9e90a1ef2122fd64c0719b5b8da604579c90fdc5657e7417f074f4`
- private_runtime_access_authorized: `No`
- retained_PostgreSQL_access_authorized: `No`
- Docker_runtime_execution_authorized: `No`
- source_change_authorized: `Conditional / exact S4 reservation-reference handoff only`
- canonical_state_write_authorized: `No`
- Git_commit_push_authorized: `No`
- success_ceiling: `COMBINED_S3_S4_SOURCE_CANDIDATE / BROWSER_REVIEW_PENDING`

## 1. repository baseline

Require:

```text
branch main
HEAD 33a216f29062176ad196a567a299ba30291c3f72
HEAD^ be2489515ba7799466ffdf415b47e4d3e0a79e46
HEAD^^ c26ec9eb342d052c726c57b5df42ced70e01a757
index empty
```

Tracked dirt must be exactly two accepted 0039 candidate paths with exact hashes:

- `src/aiscc/scenarios/stockroom_production.py` `d860fd8c1c98f8a3fd1e2f4a8b1bb5f0f0ba81c11cd6ab6df648a59e1ea56f0f`
- `tests/integration/scenarios/test_stockroom_binding.py` `8176af244b044404e91ca5405cc93520f7b9dcad909f7ba5fa13b34377e61ca3`

Git-visible untracked must be exactly six predecessor governance paths:

- `.aiassistant/records/aiscc/cycles/20260914_0009_aiscc-p2-3-scenario-matrix-separate-applications-entry-1.cycle.md` `ad576d179e0893f928d0f20a31209c6a5f0ec78845ef5d2f393dd6bd1506e71e`
- `.aiassistant/reports/aiscc/20260914_0009_aiscc-p2-3-2357-single-builder-scope-conflict-retry-judgment-1.md` `dee53f09c6b8f5771dd09e5e912541faaad803d8a84f1b796c5cd890bc3b7300`
- `.aiassistant/tasks/done/20260914_0009_aiscc-p2-3-s2-s3-s4-separate-production-applications-runtime-retry-1.md` `3ae3533a620c49408b173c6c113fa244fe84a1950bc025c1de67ede1b9c70a68`
- `.aiassistant/records/aiscc/cycles/20260914_0039_aiscc-p2-3-s3-static-policy-serialization-rework-entry-1.cycle.md` `64b67ec18501cc5b02b0d441d710ed8cbecb43745d53cd7cb4ab10f5b0259a60`
- `.aiassistant/reports/aiscc/20260914_0039_aiscc-p2-3-0009-s2-accepted-s3-runner-typeerror-rework-judgment-1.md` `267e1bd3ec73f00af83c88c9a65b3bb5a707e7cc56936a3d738d370d17f6a58d`
- `.aiassistant/tasks/done/20260914_0039_aiscc-p2-3-s3-static-policy-mappingproxy-serialization-targeted-source-rework-1.md` `538eab59c81e71fb8b976447264e7ecdb230ef24f3d98f6192d35ceec77ea71a`

Canonical state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md` `281bd733624ac87be207f62ed59b99edf0d64cf3b8f3d00e9bc9611fe3179f8c`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md` `b55eb504c39af0134837f808eef8610b0c54505ee8c597b332f79148ad61d8bd`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md` `1bb251b5758e8fea1ac260dcace074dcb7e2ff9adf6a96e8699d29c66bea495d`

Preserve ignored non-owned legacy:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
SHA-256 52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

After current Cycle/Judgment placement while current Task remains active/ignored:

```text
Git-visible untracked exactly 8
```

Mismatch → STOP before source mutation.

## 2. executable rule

Use only:

```text
<repository-root>\.venv\Scripts\python.exe
```

Forbidden:

```text
python
py
WindowsApps
PATH Python discovery
repository-external Python/venv discovery
```

Git read-only only.

## 3. accepted S3 candidate preservation

Before any edit require:

```text
src/aiscc/scenarios/stockroom_production.py
d860fd8c1c98f8a3fd1e2f4a8b1bb5f0f0ba81c11cd6ab6df648a59e1ea56f0f

tests/integration/scenarios/test_stockroom_binding.py
8176af244b044404e91ca5405cc93520f7b9dcad909f7ba5fa13b34377e61ca3

src/aiscc/evidence/models.py
df48a1c8af09c09827a2d5996e8aed19c3642e9f8b099b58e75bd855ded6c54e
```

The accepted S3 semantic must remain:

```text
static_policy_value = plain dict at caller boundary
same value used for evidence body and canonical hash
generic canonical JSON unchanged
S3 local final BLOCKED
provider/tool/Judgment/HumanResult 0
```

Do not revert or replace the S3 fix.

## 4. source-owner diagnosis scope

Read-only inspect:

```text
src/aiscc/human/models.py
src/aiscc/human/authority.py
src/aiscc/human/repository.py
src/aiscc/scenarios/stockroom_production.py
tests covering P1-7 HumanGate reservation/open lifecycle
```

Trace exact source ownership:

```text
HumanGateReservation dataclass fields
HumanGateReservationAuthority.reserve return contract
reservation identity/fingerprint/ref helper if any
HumanGuardAuthority.gate_open_participant input contract
HumanGate durable repository identity
StockroomCaptureOwnerAdapter.open_human_gate
```

Produce a table:

```text
stage
source owner
typed value
canonical identity/ref
consumer
current Stockroom use
mismatch
source location
```

## 5. reproduce S4 failure before correction

Using the existing local/non-private scenario fixture and real P1-7 owners, reproduce:

```text
HumanGateReservationAuthority.reserve
→ real HumanGateReservation

Stockroom open_human_gate
→ AttributeError because `.serialized_ref` is absent
```

Capture:

```text
exact exception type/message
reservation actual type
reservation fields
canonical reservation identity/ref API supported by current P1-7 source
```

Do not invent a reference string from field names.

If no existing P1-7-supported canonical reservation reference can be identified:

```text
STOP / P1_7_RESERVATION_REFERENCE_API_GAP
```

Do not extend P1-7 models/authority in this Task.

## 6. correction rule

If current P1-7 source already exposes a canonical reservation reference/identity, modify only the Stockroom adapter to use it consistently for:

```text
_pending_authority_refs[HUMAN_REQUIRED]
_handles key
_snapshot_result reference
```

The exact same canonical ref must identify the same reservation object throughout the adapter.

`gate_open_participant` must still receive the real typed `HumanGateReservation` object as its source contract requires.

Do not:
- construct a fake reservation
- derive a new hash/ref schema in Stockroom
- mutate HumanGateReservation
- add `.serialized_ref` to P1-7 merely for Stockroom convenience
- bypass `HumanGateReservationAuthority`
- bypass `HumanGuardAuthority`
- fabricate a HumanResult
- synthesize HUMAN_REQUIRED directly

## 7. allowed change scope

Product change allowed only:

```text
src/aiscc/scenarios/stockroom_production.py
```

Existing tracked test change allowed only:

```text
tests/integration/scenarios/test_stockroom_binding.py
```

No new test files.

Read-only owner source:

```text
src/aiscc/human/models.py
src/aiscc/human/authority.py
src/aiscc/human/repository.py
src/aiscc/evidence/models.py
```

If a correct solution requires changing P1-7 source:

```text
STOP / SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
```

Name the exact required path/API and preserve current S3 candidate.

## 8. required local S4 semantic

After correction, local/non-private source-owned path must prove:

```text
PRE_HUMAN P1-6 evidence/checkpoint:
SATISFIED

HumanGateReservation:
real P1-7 reservation

Human guard participant:
owner-backed

transition:
ADMISSION_PENDING→HUMAN_REQUIRED admitted

final WorkRun:
HUMAN_REQUIRED

HumanGate:
present / exact run+state+version binding

HumanResult:
0

Judgment:
0
```

Stop at HUMAN_REQUIRED. Do not simulate Human action.

## 9. full targeted regression

Run the existing parametrized local scenario owner-handoff test for all four cases after all edits are complete.

Require:

```text
S1:
ACCEPTED

S2:
REWORK_REQUIRED
JudgmentKind HOLD_REWORK_REQUIRED

S3:
BLOCKED
provider/tool 0
Judgment 0
HumanResult 0

S4:
HUMAN_REQUIRED
HumanResult 0
Judgment 0
```

All four must pass in the **final file bytes**.

Also run:

```text
changed-file in-memory compile or py_compile with no tracked residue
Ruff on changed Python
git diff --check
```

Do not treat pre-format test output as proof of final changed test bytes. The final local pytest invocation must occur after the last product/test edit.

External provider/network = 0.

No full repository suite automatically.

## 10. Git boundary

No commit.

Final tracked dirt must remain exactly:

```text
src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_binding.py
```

No third tracked path.

Current Task active→done byte-identically.

Final Git-visible governance untracked exactly nine:

```text
0009 Cycle/Judgment/done Task
0039 Cycle/Judgment/done Task
current Cycle/Judgment/done Task
```

No other untracked product/test path.

Legacy 1400 remains ignored/non-owned.

## 11. contract review

Exactly 44 rows:

```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_EXACT
INITIAL_INDEX_EMPTY
INITIAL_TRACKED_DIRT_EXACT_2
INITIAL_UNTRACKED_GOVERNANCE_EXACT_6
PREDECESSOR_0039_RESULT_SHA_EXACT
CURRENT_STATE_HASHES_EXACT
LEGACY_1400_ACTIVE_PRESERVED
PYTHON_REPOSITORY_VENV_EXACT
S3_ACCEPTED_CANDIDATE_HASHES_EXACT
GENERIC_EVIDENCE_MODELS_HASH_UNCHANGED
NO_PRIVATE_RUNTIME_ACCESS
NO_RETAINED_DB_ACCESS
NO_DOCKER_RUNTIME_EXECUTION
HUMAN_RESERVATION_MODEL_FIELDS_IDENTIFIED
HUMAN_RESERVATION_AUTHORITY_CONTRACT_IDENTIFIED
HUMAN_GATE_PARTICIPANT_CONTRACT_IDENTIFIED
STOCKROOM_SERIALIZED_REF_MISMATCH_PROVEN
LOCAL_S4_ATTRIBUTEERROR_REPRODUCED
CANONICAL_RESERVATION_REFERENCE_API_IDENTIFIED
MINIMAL_STOCKROOM_RESERVATION_HANDOFF_FIX_ONLY
P1_7_HUMAN_MODELS_UNCHANGED
P1_7_HUMAN_AUTHORITY_UNCHANGED
P1_7_HUMAN_REPOSITORY_UNCHANGED
S4_RESERVATION_REFERENCE_BOUND_EXACT
S4_LOCAL_PREHUMAN_EVIDENCE_SATISFIED
S4_LOCAL_HUMAN_GATE_PRESENT
S4_LOCAL_FINAL_WORKRUN_HUMAN_REQUIRED
S4_LOCAL_HUMAN_RESULT_ZERO
S4_LOCAL_JUDGMENT_ZERO
S3_LOCAL_BLOCKED_REGRESSION_PASS
S3_LOCAL_PROVIDER_TOOL_JUDGMENT_ZERO
S2_LOCAL_REWORK_REGRESSION_PASS
S1_LOCAL_ACCEPTED_REGRESSION_PASS
ALL_FOUR_LOCAL_SCENARIO_TESTS_PASS
NO_EXTERNAL_PROVIDER_NETWORK
NO_CANONICAL_STATE_MUTATION
NO_GIT_COMMIT_PUSH
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
FINAL_CHANGED_PATHS_EXACT_2
FINAL_UNTRACKED_GOVERNANCE_EXACT_9
TEST_STATIC_CHECKS_PASS
DIAGNOSIS_REPORT_COMPLETE
EXPORT_INTEGRITY_PASS
```

Success requires:

```text
44 / 44 PASS
```

If P1-7 source expansion is required, later rows remain non-PASS.

## 12. export

Root docs:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
0039_ACCEPTANCE_VERIFICATION.md
S4_RESERVATION_REFERENCE_DIAGNOSIS.md
P1_7_RESERVATION_AUTHORITY_VERIFICATION.md
S4_HANDOFF_CORRECTION_VERIFICATION.md
S1_REGRESSION_VERIFICATION.md
S2_REGRESSION_VERIFICATION.md
S3_REGRESSION_VERIFICATION.md
S4_REGRESSION_VERIFICATION.md
SOURCE_CHANGE_SUMMARY.md
TEST_VERIFICATION.md
CONTRACT_REVIEW.md
```

Include current Cycle/Judgment/done Task and the two changed tracked paths.

Generate manifest/member counts from actual declared set.

Require:

```text
one top-level
CRC PASS
manifest SHA/size exact
TASK.md == canonical done Task
no private path/value/DB body
```

## 13. success ceiling

```text
S1:
ACCEPTED / CLOSED

S2 private:
REWORK_REQUIRED / accepted

S3 source:
CORRECTED / accepted candidate

S3 private stranded:
preserved / not reusable

S4 source:
CORRECTED candidate

S4 private:
NOT_STARTED

combined S3+S4 source persistence:
NOT_PERFORMED

private S3/S4 retry:
NOT_PERFORMED

Replay:
NOT_STARTED

P2-3:
IN_PROGRESS
```
