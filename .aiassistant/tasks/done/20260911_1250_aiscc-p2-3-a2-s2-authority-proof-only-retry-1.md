# 작업지시서: P2-3 A2 S2 authority proof-only retry

## meta

- task_id: `20260911_1250_aiscc-p2-3-a2-s2-authority-proof-only-retry-1`
- created_at: `2026-09-11T12:50:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `QA_ONLY / STATIC_AND_POSTGRESQL_AUTHORITY_PROOF_RETRY`
- evidence_profile: `HIGH_RISK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `876f232880e652fbf715f13c13b8cc03d27404f0`
- required_base_tree: `0f855b67fcad1be1cb4f635b6b4db8856c43da64`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. purpose

Do not modify the current P1-6/P1-7/A2 S2 candidate.

The 1240 test-contract correction is retained.

This Task only reruns the blocked static + PostgreSQL + regression proof with a literal verifier that contains no extra postconditions.

# 1. inbound transport

Verify Browser delivery ZIP exact filename/SHA-256 from the Short Prompt.

Place current TASK first at:

```text
.aiassistant/tasks/active/20260911_1250_aiscc-p2-3-a2-s2-authority-proof-only-retry-1.md
```

Read fully.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260911_1250_aiscc-p2-3-a2-s2-test-rework-admitted-proof-retry-entry-1.cycle.md
SHA-256:
bbf761e28af988044c6b05e12cc2aa909ef82461484e42a09c060d74df95c336

.aiassistant/reports/aiscc/20260911_1250_aiscc-p2-3-a2-s2-static-verifier-extra-postcondition-failure-judgment-1.md
SHA-256:
084a6f0cc2f76ea6af2ce41005a6e625a1a2758a492e482a49054b5e8f148524
```

Bootstrap failure before current Task placement:

```text
STOP
no project work
no report/export
```

# 2. repository gate

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

Expected Git-visible set excluding current active Task is exact 61 paths:

- `.aiassistant/tasks/done/20260910_1738_aiscc-p2-3-a2-production-owner-bootstrap-integration-feasibility-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1738_aiscc-p2-3-a1-terminal-persisted-a2-feasibility-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1738_aiscc-p2-3-a1-terminal-state-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1824_aiscc-p2-3-a2-production-owner-bootstrap-integration-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1824_aiscc-p2-3-a2-feasibility-accepted-production-integration-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1824_aiscc-p2-3-a2-feasibility-audit-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1948_aiscc-p2-3-a2-production-integration-static-and-runtime-evidence-binding-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1948_aiscc-p2-3-a2-static-failure-runtime-evidence-binding-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1948_aiscc-p2-3-a2-static-failure-runtime-evidence-binding-judgment-1.md`
- `.aiassistant/tasks/done/20260910_2215_aiscc-p2-3-a2-security-clock-domain-test-failure-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_2215_aiscc-p2-3-a2-security-clock-domain-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_2215_aiscc-p2-3-a2-security-clock-domain-test-failure-judgment-1.md`
- `.aiassistant/tasks/done/20260910_2220_aiscc-p2-3-a2-prepared-owner-binding-contract-reconciliation-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_2220_aiscc-p2-3-a2-prepared-owner-binding-contract-reconciliation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_2220_aiscc-p2-3-a2-prepared-owner-binding-mismatch-judgment-1.md`
- `.aiassistant/tasks/done/20260910_2355_aiscc-p2-3-a2-prepared-owner-model-reconciliation-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_2355_aiscc-p2-3-a2-prepared-owner-audit-accepted-model-reconciliation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_2355_aiscc-p2-3-a2-prepared-owner-contract-audit-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260911_0105_aiscc-p2-3-a2-materialization-output-provenance-binding-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_0105_aiscc-p2-3-a2-owner-model-static-failure-materialization-output-binding-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_0105_aiscc-p2-3-a2-owner-model-static-failure-materialization-output-binding-judgment-1.md`
- `.aiassistant/tasks/done/20260911_0228_aiscc-p2-3-a2-materialized-workspace-fixture-contract-test-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_0228_aiscc-p2-3-a2-materialized-workspace-fixture-test-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_0228_aiscc-p2-3-a2-materialized-workspace-fixture-test-failure-judgment-1.md`
- `.aiassistant/tasks/done/20260911_0240_aiscc-p2-3-a2-static-command-transport-and-executable-proof-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_0240_aiscc-p2-3-a2-static-command-transport-failure-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_0240_aiscc-p2-3-a2-static-command-transport-failure-judgment-1.md`
- `.aiassistant/tasks/done/20260911_0335_aiscc-p2-3-a2-pycompile-cache-cleanup-and-proof-admission-reverification-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_0335_aiscc-p2-3-a2-executable-proof-complete-workspace-residue-cleanup-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_0335_aiscc-p2-3-a2-executable-proof-workspace-residue-judgment-1.md`
- `.aiassistant/tasks/done/20260911_0345_aiscc-p2-3-a2-s2-negative-evaluation-judgment-authority-contract-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_0345_aiscc-p2-3-a2-executable-proof-admitted-s2-authority-audit-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_0345_aiscc-p2-3-a2-workspace-reconciled-executable-proof-acceptance-judgment-1.md`
- `src/aiscc/bootstrap.py`
- `src/aiscc/scenarios/driver.py`
- `src/aiscc/scenarios/composition.py`
- `src/aiscc/scenarios/stockroom_production.py`
- `config/evidence/stockroom-capture.v1.json`
- `config/human/stockroom-capture.v1.json`
- `config/judgment/stockroom-capture.v1.json`
- `tests/unit/scenarios/test_owner_composition.py`
- `tests/integration/scenarios/test_stockroom_binding.py`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`
- `.aiassistant/tasks/done/20260911_0920_aiscc-p2-3-a2-s2-negative-evaluation-judgment-authority-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_0920_aiscc-p2-3-a2-s2-authority-audit-accepted-implementation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_0920_aiscc-p2-3-a2-s2-negative-evaluation-authority-audit-final-acceptance-judgment-1.md`
- `src/aiscc/evidence/models.py`
- `src/aiscc/evidence/repository.py`
- `src/aiscc/judgment/models.py`
- `src/aiscc/judgment/authority.py`
- `config/judgment/stockroom-capture.v2.json`
- `tests/integration/evidence/test_postgres_evidence_admission.py`
- `tests/integration/human/test_postgres_human_gate_judgment.py`
- `.aiassistant/tasks/done/20260911_1120_aiscc-p2-3-a2-s2-negative-evaluation-judgment-authority-static-rework-and-proof-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_1120_aiscc-p2-3-a2-s2-static-failure-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1120_aiscc-p2-3-a2-s2-static-failure-judgment-1.md`
- `.aiassistant/tasks/done/20260911_1240_aiscc-p2-3-a2-s2-negative-basis-test-contract-rework-and-proof-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_1240_aiscc-p2-3-a2-s2-authority-test-contract-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1240_aiscc-p2-3-a2-s2-authority-test-assertion-mismatch-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_1250_aiscc-p2-3-a2-s2-test-rework-admitted-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1250_aiscc-p2-3-a2-s2-static-verifier-extra-postcondition-failure-judgment-1.md`

Any extra/missing path:

```text
DIRTY_WORKSPACE_MIXED
→ STOP_WITH_REPORT_EXPORT
```

Ignored target/export residue remains non-blocking.

# 3. exact current identities

Require:

```text
.aiassistant/tasks/done/20260911_1240_aiscc-p2-3-a2-s2-negative-basis-test-contract-rework-and-proof-retry-1.md
SHA-256:
a207774655eaaa65ba819691edfee9f3804d631a3c4cb9ff95de7e5d85b46840

.aiassistant/records/aiscc/cycles/20260911_1240_aiscc-p2-3-a2-s2-authority-test-contract-rework-entry-1.cycle.md
SHA-256:
ae3cb6503f480119de1feb784b93d967428f8602f93d0e57820f5d161c3e9d5e

.aiassistant/reports/aiscc/20260911_1240_aiscc-p2-3-a2-s2-authority-test-assertion-mismatch-judgment-1.md
SHA-256:
e0132b80291a89c4803204584b075ec6e2b04b41e85a155471d88fea89a831a8

src/aiscc/evidence/models.py
SHA-256:
df48a1c8af09c09827a2d5996e8aed19c3642e9f8b099b58e75bd855ded6c54e

src/aiscc/judgment/models.py
SHA-256:
6a1bed5dca0c0b5a73d4def8c4fdbbc500f81f7e979af312b7cfd6dfebe375c6

tests/integration/human/test_postgres_human_gate_judgment.py
SHA-256:
5fbcc635948906250b2795b6f31b9e5a849ab8991e203dcbcad661a571d67058
```

Also compute a deterministic before-task aggregate over all regular files under:

```text
src
config
tests
migrations
```

excluding:

```text
**/__pycache__/**
*.pyc
```

Record the exact relative-path + SHA-256 manifest and aggregate in `WORKSPACE_VERIFICATION.md`.

The same aggregate must remain byte-identical at final verification.

# 4. zero product mutation

No source/config/test/migration mutation is authorized.

Do not edit:

```text
src/**
config/**
tests/**
migrations/**
```

Any perceived need to edit:

```text
SCOPE_EXPANSION_REQUIRED
→ STOP_WITH_REPORT_EXPORT
```

# 5. literal static verifier

Do not use `py_compile`.

Create exactly one temporary Python verifier outside the repository.

Its executable semantic content must be equivalent to this and MUST NOT add assertions on loader-return structure:

```python
from pathlib import Path
import sys

root = Path.cwd()
sys.path.insert(0, str(root / "src"))

python_files = [
    "src/aiscc/evidence/models.py",
    "src/aiscc/evidence/repository.py",
    "src/aiscc/judgment/models.py",
    "src/aiscc/judgment/authority.py",
    "src/aiscc/scenarios/stockroom_production.py",
    "tests/integration/evidence/test_postgres_evidence_admission.py",
    "tests/integration/human/test_postgres_human_gate_judgment.py",
    "tests/integration/scenarios/test_stockroom_capture_runner.py",
]

for rel in python_files:
    source = (root / rel).read_text(encoding="utf-8", errors="strict")
    compile(source, rel, "exec")

from aiscc.scenarios.stockroom_production import load_stockroom_judgment_config

load_stockroom_judgment_config(
    root / "config/judgment/stockroom-capture.v2.json"
)
load_stockroom_judgment_config(
    root / "config/judgment/stockroom-capture.v1.json"
)

print("STATIC_VERIFIER: PASS")
```

Forbidden additions include:

```text
schema_version dictionary lookup
raw JSON-shape assertions after normalized loader return
new config semantics
source mutation
```

Run with exact repository interpreter:

```text
.venv\Scripts\python.exe -B
```

# 6. mandatory static gate

Run Ruff on exactly the same eight Python paths.

Require:

```text
in-memory compile:
8 / 8 PASS

Judgment v2 strict loader call:
PASS

Judgment v1 strict loader call:
PASS

Ruff:
8 / 8 PASS

git diff --check:
PASS

index:
empty

new repo-visible .pyc:
0
```

If any required check fails:

```text
STATIC_CHECK_FAILURE
→ STOP_WITH_REPORT_EXPORT
```

No same-turn repair.

Delete only the exact external verifier afterward.

# 7. PostgreSQL prerequisite

After static PASS, use the accepted bounded local disposable PostgreSQL pattern:

```text
postgres:17.6-alpine
--pull=never
local loopback only
Task-owned container
temporary storage
```

No remote DB, no pull, no unrelated Docker mutation.

Apply:

```text
alembic upgrade head
alembic current
```

Require:

```text
20260901_0008 (head)
```

# 8. P1-6/P1-7 authority proof

Run:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider   tests/integration/evidence/test_postgres_evidence_admission.py   tests/integration/human/test_postgres_human_gate_judgment.py -ra
```

Previous collection was 10 tests.

Require all collected tests:

```text
PASS
0 fail
0 error
0 skip
```

# 9. A2 S1-S4 authority proof

Only after section 8 PASS:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider   tests/integration/scenarios/test_stockroom_capture_runner.py -ra
```

Require all collected tests PASS / zero skip.

Must preserve:

```text
S1:
positive SATISFIED basis

S2:
authentic durable UNSATISFIED evaluation ref
→ P1-7 issue-time verification
→ participant-time reverification
→ REWORK_REQUIRED

S3:
no Judgment

S4:
no premature Judgment
```

# 10. prepared-owner/A1 regression

Run:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider   tests/unit/scenarios/test_owner_composition.py   tests/integration/scenarios/test_stockroom_binding.py   tests/unit/scenarios/test_stockroom_capture_runner.py -ra
```

Accepted predecessor baseline:

```text
74 PASS
```

Require all PASS.

# 11. bounded direct-owner regression

Run:

```text
tests/integration/workflow/test_postgres_kernel.py
tests/unit/security/test_stockroom_policy.py
```

Require all collected tests PASS / zero prerequisite skip.

# 12. compatibility regression

Run only direct existing P1-6/P1-7 model/ref/policy/authority tests not already covered above.

Do not run the whole repository suite.

Report exact modules and counts.

# 13. contract review

Require all 31 invariants PASS:

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

# 14. runtime ceiling

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
Stockroom Docker/process runtime
provider/tool dispatch
AgentExecutionService runtime execution
network
real secret resolution
actual S1-S4 capture
HumanResult fabrication
Replay
Git add/commit/push
```

# 15. failure handling

After current Task placement, any mandatory failure must:

```text
stop further product execution
move current Task byte-identically to done
create failure report/evidence
create verified export ZIP
```

Only bootstrap failure before current Task placement uses no-report/export.

# 16. cleanup

Remove only:

```text
Task-owned disposable PostgreSQL container
exact external temporary verifier file
```

No broad cleanup.

# 17. final workspace

Before current Task lifecycle:

```text
existing Git-visible:
59

current Cycle/Judgment:
2

excluding current active Task:
61 exact
```

No source/config/test mutation is allowed.

Move current active Task byte-identically to:

```text
.aiassistant/tasks/done/20260911_1250_aiscc-p2-3-a2-s2-authority-proof-only-retry-1.md
```

Final expected:

```text
62 exact Git-visible
index empty
```

The source/config/tests/migrations aggregate from section 3 must equal its before-task value exactly.

# 18. no Git persistence

Do not run:

```text
git add
git commit
git push
git reset
git restore
git stash
```

# 19. required export

Bundle:

```text
.aiassistant/reports/target/20260911_1250_aiscc-p2-3-a2-s2-authority-proof-only-retry-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
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
```

Expected:

```text
14 root docs
3 canonical copies
17 members total
```

`EXPORT_MANIFEST.md` covers all 16 non-self entries with relative path, size, SHA-256.

Require one top-level directory, CRC PASS, exact members, manifest exact.

# 20. success ceiling

Success:

```text
P1-6 negative evaluation authority:
IMPLEMENTED_CANDIDATE / EXECUTED_PASS

P1-7 negative Judgment basis:
IMPLEMENTED_CANDIDATE / EXECUTED_PASS

A2 S2 authority:
EXECUTED_PASS

A2 prepared-owner/materialized-output:
PRESERVED

A2:
READY_FOR_BROWSER FINAL IMPLEMENTATION JUDGMENT

A2 persistence:
NOT_AUTHORIZED

actual Stockroom runtime:
NOT_STARTED
```
