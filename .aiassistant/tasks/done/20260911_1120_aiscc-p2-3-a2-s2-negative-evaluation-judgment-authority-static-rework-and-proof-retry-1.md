# 작업지시서: P2-3 A2 S2 negative-evaluation Judgment authority static rework + proof retry

## meta

- task_id: `20260911_1120_aiscc-p2-3-a2-s2-negative-evaluation-judgment-authority-static-rework-and-proof-retry-1`
- created_at: `2026-09-11T11:20:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `IMPLEMENTATION_REWORK / STATIC_AND_POSTGRESQL_PROOF_RETRY`
- evidence_profile: `HIGH_RISK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `876f232880e652fbf715f13c13b8cc03d27404f0`
- required_base_tree: `0f855b67fcad1be1cb4f635b6b4db8856c43da64`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. purpose

Continue the current `0920` implementation candidate.

Correct only the two reported Ruff findings:

```text
src/aiscc/evidence/models.py: I001
src/aiscc/judgment/models.py: SIM102
```

Then rerun the full blocked proof chain. No semantic redesign is authorized.

# 1. Python discipline

Do not assume bare `python`, `python3`, or `py` is valid on PATH. Do not run bare `python` as a probe.

Known interpreter candidate:

```text
C:\Users\oracl\AppData\Roaming\uv\python\cpython-3.12.14-windows-x86_64-none\python.exe
```

For repository import/test execution, verify and use exact:

```text
.venv\Scripts\python.exe
```

# 2. inbound transport

Verify Browser ZIP exact filename/SHA from the Short Prompt.

Place current TASK first at:

```text
.aiassistant/tasks/active/20260911_1120_aiscc-p2-3-a2-s2-negative-evaluation-judgment-authority-static-rework-and-proof-retry-1.md
```

Read it fully, then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260911_1120_aiscc-p2-3-a2-s2-static-failure-rework-proof-retry-entry-1.cycle.md
SHA-256: 844d10e665e5c3a2c83964c27722400a87fbbee449c2edc1c198799a79cb0962

.aiassistant/reports/aiscc/20260911_1120_aiscc-p2-3-a2-s2-static-failure-judgment-1.md
SHA-256: 95996e287b927c7345ad4c726ac98096214fa55b3f2539e63d863e9bbe88ab81
```

Bootstrap failure before current Task placement:

```text
STOP
no project work
no report/export
```

# 3. predecessor 0920 Task lifecycle normalization

Exactly one of:

```text
.aiassistant/tasks/active/20260911_0920_aiscc-p2-3-a2-s2-negative-evaluation-judgment-authority-implementation-1.md
.aiassistant/tasks/done/20260911_0920_aiscc-p2-3-a2-s2-negative-evaluation-judgment-authority-implementation-1.md
```

must exist with SHA-256:

```text
e2f0299273512e29f77bd4434dc1287be027cd7c7f8e346facf2d6e271ed9a27
```

If both or neither exist: `PREDECESSOR_TASK_LIFECYCLE_MISMATCH` → STOP_WITH_REPORT_EXPORT.

If active, move byte-identically to done and recheck SHA.

Require companion identities:

```text
.aiassistant/records/aiscc/cycles/20260911_0920_aiscc-p2-3-a2-s2-authority-audit-accepted-implementation-entry-1.cycle.md
SHA-256: a769f39a3b1a7c1596d4288b5f6371c7bcebff9101fe8b176033ef269e94d717

.aiassistant/reports/aiscc/20260911_0920_aiscc-p2-3-a2-s2-negative-evaluation-authority-audit-final-acceptance-judgment-1.md
SHA-256: 9cc84eb27055924043b1ac9fad8357b14d153a8cfbd842636625b082957bb9ba
```

# 4. repository gate

Require:

```text
branch: main
HEAD: 876f232880e652fbf715f13c13b8cc03d27404f0
HEAD tree: 0f855b67fcad1be1cb4f635b6b4db8856c43da64
index: empty
```

After predecessor lifecycle normalization and current Cycle/Judgment placement, require exact Git-visible path count excluding current active Task:

```text
55
```

Require that the only newly Git-visible implementation paths introduced by 0920 beyond the previously pending A2 candidate are exactly:

```text
src/aiscc/evidence/models.py
src/aiscc/evidence/repository.py
src/aiscc/judgment/models.py
src/aiscc/judgment/authority.py
config/judgment/stockroom-capture.v2.json
tests/integration/evidence/test_postgres_evidence_admission.py
tests/integration/human/test_postgres_human_gate_judgment.py
```

and that the two already-pending A2 paths remain:

```text
src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Any extra/missing path: `DIRTY_WORKSPACE_MIXED` → STOP_WITH_REPORT_EXPORT.

# 5. exact mutation allowlist

Only:

```text
src/aiscc/evidence/models.py
src/aiscc/judgment/models.py
```

may change in this retry.

Freeze all other source/config/test/migration paths, including the other seven 0920 implementation paths.

If another change is required: `SCOPE_EXPANSION_REQUIRED` → STOP_WITH_REPORT_EXPORT.

# 6. style-only repair

For `src/aiscc/evidence/models.py`, fix `I001` by import ordering only.

For `src/aiscc/judgment/models.py`, fix `SIM102` by logically equivalent conditional flattening only.

Do not change semantics of:

```text
EvidenceSetEvaluationRef
JudgmentEvidenceBasisKind
legacy v1 serialization/fingerprint compatibility
positive/negative basis validation
```

# 7. mandatory static gate without pyc residue

Do not use `py_compile`.

Create one temporary verifier outside the repository, e.g. `%TEMP%\aiscc_p2_3_a2_s2_static_verify_retry.py`, and use it to:

```text
read the 8 changed Python files as UTF-8 strict
compile(source_text, path, "exec") in memory
strict-load Judgment v2
strict-load frozen Judgment v1
```

Then run Ruff on exactly:

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

Require:

```text
in-memory compile: 8/8 PASS
Ruff: 8/8 PASS
Judgment v2 strict load: PASS
Judgment v1 compatibility load: PASS
git diff --check: PASS
index: empty
new repo-visible .pyc: 0
```

Mandatory static failure → STOP_WITH_REPORT_EXPORT. No same-turn source repair after this gate.

# 8. PostgreSQL prerequisite

After static PASS, use the same bounded local disposable PostgreSQL authority used in prior A2 proofs.

Allowed fallback:

```text
postgres:17.6-alpine
--pull=never
local loopback only
Task-owned container only
temporary storage
```

Run Alembic upgrade/current and require:

```text
20260901_0008 (head)
```

No migration creation.

# 9. P1-6/P1-7 mandatory authority tests

Run:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider   tests/integration/evidence/test_postgres_evidence_admission.py   tests/integration/human/test_postgres_human_gate_judgment.py -ra
```

Require all collected tests PASS, 0 fail/error/skip.

# 10. A2 S1-S4 authority integration

Run:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider   tests/integration/scenarios/test_stockroom_capture_runner.py -ra
```

Require all PASS / zero skip.

Must preserve:

```text
S1 SATISFIED_ATTESTATION -> ACCEPTED
S2 durable UNSATISFIED evaluation -> canonical P1-6 ref -> P1-7 issue verification -> participant reverification -> REWORK_REQUIRED
S3 no Judgment
S4 no premature Judgment
```

# 11. prepared-owner/A1 regression

Run:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider   tests/unit/scenarios/test_owner_composition.py   tests/integration/scenarios/test_stockroom_binding.py   tests/unit/scenarios/test_stockroom_capture_runner.py -ra
```

Require all PASS. Accepted baseline: 74 PASS if inventory unchanged.

# 12. bounded direct-owner regression

Run:

```text
tests/integration/workflow/test_postgres_kernel.py
tests/unit/security/test_stockroom_policy.py
```

Require all PASS. Do not double-count the evidence/Human-Judgment modules already run above.

# 13. compatibility regression

Discover and run only direct existing tests for modified P1-6 evidence ref/model/repository and P1-7 Judgment model/policy/authority that are not already covered. Do not run the whole repository suite.

# 14. mandatory contract review

Require 31/31 PASS for the exact 0920 invariants, including:

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

# 15. runtime ceiling

Allowed: PostgreSQL/Alembic, real P1-6 evaluation persistence/resolution, real P1-7 Judgment issue/participant preparation, bounded WorkflowKernel transitions, A2 production owner construction, config loading.

Forbidden: real Stockroom materialization, Docker/process, provider/tool dispatch, AgentExecutionService runtime execution, network, real secret resolution, actual S1-S4 runtime capture, HumanResult fabrication, Replay, Git persistence.

# 16. failure reporting rule

After current Task placement, any mandatory STOP must:

```text
stop further product mutation/execution
move current Task to done byte-identically
produce failure EXECUTOR_REPORT + WORKSPACE_VERIFICATION + relevant evidence
produce verified export ZIP
```

Only bootstrap failure before Task placement has no report/export.

# 17. cleanup

Remove only exact Task-owned disposable PostgreSQL and exact external temporary static-verifier file if created. No broad cleanup.

# 18. final workspace

No new product paths are authorized. After current Task moves to done, expected Git-visible count:

```text
56 exact
index empty
```

# 19. required export

Bundle folder:

```text
.aiassistant/reports/target/20260911_1120_aiscc-p2-3-a2-s2-negative-evaluation-judgment-authority-static-rework-and-proof-retry-1/
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
src/aiscc/evidence/models.py
src/aiscc/judgment/models.py
```

Expected 19 members total. `EXPORT_MANIFEST.md` covers all 18 non-self entries with relative path, size, SHA-256.

# 20. no Git persistence

Do not run `git add`, `git commit`, `git push`, `git reset`, `git restore`, or `git stash`.

# 21. success ceiling

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
