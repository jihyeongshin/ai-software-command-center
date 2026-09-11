# 작업지시서: P2-3 A2 S2 negative-basis test-contract rework + proof retry

## meta

- task_id: `20260911_1240_aiscc-p2-3-a2-s2-negative-basis-test-contract-rework-and-proof-retry-1`
- created_at: `2026-09-11T12:40:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `TEST_REWORK / FULL_AUTHORITY_PROOF_RETRY`
- evidence_profile: `HIGH_RISK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `876f232880e652fbf715f13c13b8cc03d27404f0`
- required_base_tree: `0f855b67fcad1be1cb4f635b6b4db8856c43da64`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. purpose

Continue the exact current 0920/1120 implementation candidate.

Do not modify production source/config/model code.

First verify that the 1120 failure is exactly a brittle assertion-message mismatch in:

```text
tests/integration/human/test_postgres_human_gate_judgment.py::test_p1_7_postgres_runtime_proof
```

Then modify only that test assertion and rerun the full blocked proof chain.

# 1. Python discipline

Do not assume bare:

```text
python
python3
py
```

is valid on PATH.

Do not use bare `python` as a probe.

Known interpreter candidate:

```text
C:\Users\oracl\AppData\Roaming\uv\python\cpython-3.12.14-windows-x86_64-none\python.exe
```

For repository imports/tests verify and use exact:

```text
.venv\Scripts\python.exe
```

# 2. inbound transport

Verify Browser delivery ZIP exact filename/SHA-256 from the Short Prompt.

Place current TASK first at:

```text
.aiassistant/tasks/active/20260911_1240_aiscc-p2-3-a2-s2-negative-basis-test-contract-rework-and-proof-retry-1.md
```

Read fully.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260911_1240_aiscc-p2-3-a2-s2-authority-test-contract-rework-entry-1.cycle.md
SHA-256:
ae3cb6503f480119de1feb784b93d967428f8602f93d0e57820f5d161c3e9d5e

.aiassistant/reports/aiscc/20260911_1240_aiscc-p2-3-a2-s2-authority-test-assertion-mismatch-judgment-1.md
SHA-256:
e0132b80291a89c4803204584b075ec6e2b04b41e85a155471d88fea89a831a8
```

Bootstrap failure before current Task placement:

```text
STOP
no project work
no report/export
```

# 3. repository gate

Require:

```text
branch:
main

HEAD:
876f232880e652fbf715f13c13b8cc03d27404f0

HEAD tree:
0f855b67fcad1be1cb4f635b6b4db8856c43da64

index:
empty
```

Expected Git-visible count excluding current active Task:

```text
58 exact
```

This is the accepted 1120 final `56` paths plus current Cycle/Judgment `2`.

Any extra/missing path:

```text
DIRTY_WORKSPACE_MIXED
→ STOP_WITH_REPORT_EXPORT
```

Ignored target/export residue remains non-blocking.

# 4. exact predecessor identity

Require:

- `.aiassistant/tasks/done/20260911_1120_aiscc-p2-3-a2-s2-negative-evaluation-judgment-authority-static-rework-and-proof-retry-1.md`  `1a968fc9fb73f3745e17ecd4b05fc031a3e2c2afae1185fcff40d001b2ac8089`
- `.aiassistant/records/aiscc/cycles/20260911_1120_aiscc-p2-3-a2-s2-static-failure-rework-proof-retry-entry-1.cycle.md`  `844d10e665e5c3a2c83964c27722400a87fbbee449c2edc1c198799a79cb0962`
- `.aiassistant/reports/aiscc/20260911_1120_aiscc-p2-3-a2-s2-static-failure-judgment-1.md`  `95996e287b927c7345ad4c726ac98096214fa55b3f2539e63d863e9bbe88ab81`

Require exact post-style source identities:

- `src/aiscc/evidence/models.py`  `df48a1c8af09c09827a2d5996e8aed19c3642e9f8b099b58e75bd855ded6c54e`
- `src/aiscc/judgment/models.py`  `6a1bed5dca0c0b5a73d4def8c4fdbbc500f81f7e979af312b7cfd6dfebe375c6`

Mismatch:

```text
PREDECESSOR_OR_CANDIDATE_IDENTITY_MISMATCH
→ STOP_WITH_REPORT_EXPORT
```

# 5. root-cause verification before test mutation

Read the exact failing block around the 1120 failing line in:

```text
tests/integration/human/test_postgres_human_gate_judgment.py
```

Also read the exact P1-7 source path that raises:

```text
negative evidence basis requires deterministic rework policy
```

Verify all:

```text
A. the test intentionally supplies a negative basis with an incompatible/non-deterministic-rework policy or target
B. the implementation rejects before Judgment persistence/transition
C. the raised ValueError is the intended policy/basis incompatibility rejection
D. the test fails only because its regex expects narrower wording (`negative Judgment basis`)
E. no production state/evidence authority assertion is bypassed by accepting the actual wording
```

If any premise is false:

```text
ROOT_CAUSE_MISMATCH
→ STOP_WITH_REPORT_EXPORT
```

# 6. exact mutation authority

Only:

```text
MODIFY
tests/integration/human/test_postgres_human_gate_judgment.py
```

All source/config/model paths are frozen, including:

```text
src/aiscc/evidence/models.py
src/aiscc/evidence/repository.py
src/aiscc/judgment/models.py
src/aiscc/judgment/authority.py
src/aiscc/scenarios/stockroom_production.py
config/judgment/stockroom-capture.v2.json
config/judgment/stockroom-capture.v1.json
config/evidence/stockroom-capture.v1.json
config/human/stockroom-capture.v1.json
src/aiscc/workflow/**
src/aiscc/security/**
src/aiscc/providers/**
src/aiscc/runtime/**
all migrations
```

Any production/source/config change requirement:

```text
SCOPE_EXPANSION_REQUIRED
→ STOP_WITH_REPORT_EXPORT
```

# 7. assertion correction

Change only the failing assertion so it verifies the intended semantic rejection without requiring one narrower noun phrase.

Acceptable principle:

```text
ValueError must be raised
AND
its message must establish:
negative basis
AND
deterministic rework policy incompatibility
```

A bounded regex equivalent to:

```text
negative .*basis requires deterministic rework policy
```

is acceptable if it matches the exact current message and remains specific to the intended rejection.

Do not weaken to:

```text
pytest.raises(ValueError)
```

with no semantic assertion.

Do not change production message text merely to satisfy the test.

# 8. no-pyc static gate

Do not use repository `py_compile`.

Use an external temporary verifier to in-memory compile the current eight 0920 implementation Python files and strict-load Judgment v1/v2.

Required Python set:

```text
src/aiscc/evidence/models.py
src/aiscc/evidence/repository.py
src/aiscc/judgment/models.py
src/aiscc/judgment/authority.py
src/aiscc/scenarios/stockroom_production.py
tests/integration/evidence/test_postgres_evidence_admission.py
tests/integration/human/test_postgres_human_gate_judgment.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Run Ruff on the same 8 paths.

Require:

```text
in-memory compile:
8 / 8 PASS

Ruff:
8 / 8 PASS

Judgment v2 strict load:
PASS

Judgment v1 compatibility load:
PASS

git diff --check:
PASS

index:
empty

new repo-visible .pyc:
0
```

Failure:

```text
STATIC_CHECK_FAILURE
→ STOP_WITH_REPORT_EXPORT
```

No same-turn repair after mandatory static failure.

# 9. PostgreSQL prerequisite

After static PASS, use the accepted bounded local disposable PostgreSQL pattern:

```text
postgres:17.6-alpine
--pull=never
local loopback only
Task-owned container
temporary storage
```

No remote DB, pull, or unrelated Docker mutation.

Apply Alembic and require:

```text
20260901_0008 (head)
```

# 10. mandatory P1-6/P1-7 authority proof

Run:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider \
  tests/integration/evidence/test_postgres_evidence_admission.py \
  tests/integration/human/test_postgres_human_gate_judgment.py -ra
```

1120 collected 10 tests.

If inventory remains unchanged, require:

```text
10 passed
0 failed
0 errors
0 skipped
```

If inventory legitimately differs, record exact reason and require all collected tests PASS / zero skip.

# 11. A2 S1-S4 authority integration

Only after section 10 PASS:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider \
  tests/integration/scenarios/test_stockroom_capture_runner.py -ra
```

Require all collected PASS / zero skip.

Must prove bounded authority semantics:

```text
S1 positive basis preserved
S2 authentic current UNSATISFIED evaluation ref -> REWORK_REQUIRED
S3 no Judgment
S4 no premature Judgment
```

No actual Stockroom runtime.

# 12. prepared-owner/A1 regression

Run:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider \
  tests/unit/scenarios/test_owner_composition.py \
  tests/integration/scenarios/test_stockroom_binding.py \
  tests/unit/scenarios/test_stockroom_capture_runner.py -ra
```

Accepted predecessor count:

```text
74 PASS
```

Require all PASS.

# 13. bounded direct-owner regression

Run:

```text
tests/integration/workflow/test_postgres_kernel.py
tests/unit/security/test_stockroom_policy.py
```

Require all collected PASS / zero prerequisite skip.

# 14. compatibility regression

Discover and run only direct existing P1-6/P1-7 evidence/Judgment model/ref/authority tests not already executed above.

Do not run the whole repository suite.

Record exact modules and counts.

# 15. 31-invariant contract review

Require PASS:

```text
P1_6_NEGATIVE_REF_TYPED
P1_6_REF_STRICT_CANONICAL
P1_6_NEGATIVE_ROW_ROUNDTRIP
P1_6_CURRENTNESS_RECOMPUTED
P1_6_STALE_EVALUATION_DENIED
P1_6_NO_SATISFACTION_ATTESTATION_FOR_S2
P1_7_EXPLICIT_BASIS_KIND
P1_7_POSITIVE_NEGATIVE_MUTUAL_EXCLUSION
P1_7_ISSUE_TIME_NEGATIVE_AUTHORITY_VERIFIED
P1_7_PARTICIPANT_NEGATIVE_AUTHORITY_REVERIFIED
P1_7_POLICY_CHECKPOINT_BOUND
P1_7_POLICY_REQUIREMENT_SET_BOUND
P1_7_WRONG_TARGET_BASIS_DENIED
P1_7_FABRICATED_REF_DENIED
P1_7_LEGACY_V1_COMPATIBLE
P1_7_LEGACY_FINGERPRINT_STABLE
JUDGMENT_V1_CONFIG_FROZEN
JUDGMENT_V2_STRICT_ENROLLMENT
A2_S1_POSITIVE_PATH_PRESERVED
A2_S2_AUTHENTIC_NEGATIVE_REF_BOUND
A2_S3_NO_JUDGMENT
A2_S4_NO_PREMATURE_JUDGMENT
ADAPTER_LOCAL_HANDLE_NOT_AUTHORITY
REASON_TEXT_NOT_AUTHORITY
PREPARED_OWNER_MODEL_PRESERVED
MATERIALIZED_OUTPUT_BINDING_PRESERVED
SECURITY_CLOCK_FIX_PRESERVED
TOOL_OUTPUT_RUNTIME_EVIDENCE_BINDING_PRESERVED
NO_WORKFLOW_GUARD_CHANGE
NO_MIGRATION
NO_REAL_STOCKROOM_RUNTIME
```

Require:

```text
31 / 31 PASS
```

# 16. runtime ceiling

Allowed:

```text
PostgreSQL/Alembic
P1-6 evaluation persistence/resolution
P1-7 Judgment issue/participant preparation
bounded WorkflowKernel transitions
A2 production owner construction
config loading
```

Forbidden:

```text
real Stockroom filesystem materialization
Docker/process runtime
provider
tool dispatch
AgentExecutionService runtime execution
network
real secret resolution
actual S1-S4 runtime capture
HumanResult fabrication
Replay
Git add/commit/push
```

# 17. failure handling

After current Task placement, any mandatory STOP must:

```text
stop further product mutation/execution
move current Task byte-identically to done
produce failure report/evidence/export ZIP
```

Only bootstrap failure before Task placement is no-report/export.

# 18. cleanup

Remove only Task-owned PostgreSQL and exact external temporary verifier created by this Task.

No broad cleanup.

# 19. final workspace

Expected Git-visible excluding active current Task before test mutation:

```text
58 exact
```

The test path is already Git-visible, so the assertion edit does not add a path.

After moving current Task to done:

```text
59 exact Git-visible
index empty
```

No other path.

# 20. no Git persistence

Do not run:

```text
git add
git commit
git push
git reset
git restore
git stash
```

# 21. required export

Bundle folder:

```text
.aiassistant/reports/target/20260911_1240_aiscc-p2-3-a2-s2-negative-basis-test-contract-rework-and-proof-retry-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
ROOT_CAUSE_VERIFICATION.md
STATIC_VERIFICATION.md
P1_6_NEGATIVE_REF_VERIFICATION.md
P1_6_CURRENTNESS_VERIFICATION.md
P1_7_NEGATIVE_BASIS_VERIFICATION.md
JUDGMENT_POLICY_V2_VERIFICATION.md
S2_AUTHORITY_VERIFICATION.md
POSTGRESQL_INTEGRATION_VERIFICATION.md
REGRESSION_VERIFICATION.md
COMPATIBILITY_VERIFICATION.md
CONTRACT_REVIEW.md
```

Also include byte-preserving copies of:

```text
current Cycle
current Judgment
current done Task
tests/integration/human/test_postgres_human_gate_judgment.py
```

Expected:

```text
15 root docs
4 canonical/test copies
19 members total
```

`EXPORT_MANIFEST.md` covers all 18 non-self entries with relative path, size, SHA-256.

Require one top-level directory, CRC PASS, exact member set and manifest exactness.

# 22. mandatory stop taxonomy

```text
DOWNLOAD_ZIP_MISSING
DOWNLOAD_ZIP_HASH_MISMATCH
DOWNLOAD_ZIP_CORRUPT
DOWNLOAD_TASK_MEMBER_MISSING
DOWNLOAD_TASK_PLACEMENT_FAILED
TRANSPORT_FAILURE
HEAD_OR_TREE_MISMATCH
INDEX_NOT_EMPTY
DIRTY_WORKSPACE_MIXED
PREDECESSOR_OR_CANDIDATE_IDENTITY_MISMATCH
ROOT_CAUSE_MISMATCH
SCOPE_EXPANSION_REQUIRED
STATIC_CHECK_FAILURE
POSTGRESQL_TEST_PREREQUISITE_MISSING
TEST_FAILURE
CONTRACT_MISMATCH
UNEXPECTED_WORKSPACE_DELTA
ZIP_EXPORT_FAILED
```

# 23. success ceiling

Success:

```text
P1-6 negative evaluation authority:
IMPLEMENTED_CANDIDATE / EXECUTED_PASS

P1-7 negative Judgment basis:
IMPLEMENTED_CANDIDATE / EXECUTED_PASS

A2 S2 authority:
EXECUTED_PASS

A2:
READY_FOR_BROWSER FINAL IMPLEMENTATION JUDGMENT

A2 persistence:
NOT_AUTHORIZED

actual Stockroom runtime:
NOT_STARTED
```
