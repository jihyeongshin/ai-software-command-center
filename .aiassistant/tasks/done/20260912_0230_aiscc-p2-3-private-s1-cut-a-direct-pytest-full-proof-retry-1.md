# 작업지시서: P2-3 private S1 Cut A direct-pytest full proof retry

## meta

- task_id: `20260912_0230_aiscc-p2-3-private-s1-cut-a-direct-pytest-full-proof-retry-1`
- created_at: `2026-09-12T02:30:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `PROOF_ONLY_RETRY / DIRECT_PYTEST_LAUNCH`
- evidence_profile: `HIGH_RISK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `21bb0769c5db126c1989d9e0eb8e9f4c5ceade91`
- required_tree: `11b9d62db2d02649509f148aa01f8f74924c5792`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. purpose

Complete the Cut A executable proof without changing repository product/config/test/example bytes.

The prior collection failure was caused by an external pytest launcher.

Use direct repository-root `python -m pytest` only.

# 1. inbound transport

Verify Browser ZIP filename/SHA-256 from the Short Prompt.

Place current Task first:

```text
.aiassistant/tasks/active/20260912_0230_aiscc-p2-3-private-s1-cut-a-direct-pytest-full-proof-retry-1.md
```

Read fully and require it is ignored by canonical Git policy.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260912_0230_aiscc-p2-3-cut-a-integration-launcher-defect-proof-retry-entry-1.cycle.md
SHA-256:
2c167dcd9a9f83063601d7a51e32600cb39e8e0847414fefdcf0b5aa9ba35d8c

.aiassistant/reports/aiscc/20260912_0230_aiscc-p2-3-cut-a-integration-launcher-import-path-defect-judgment-1.md
SHA-256:
9b8ec8ced5192f9db5036d64e514941a98a3439aa5193eca055d930abcbd2224
```

Bootstrap failure:

```text
STOP
no proof execution
no report/export
```

# 2. repository gate

Require:

```text
branch:
main

HEAD:
21bb0769c5db126c1989d9e0eb8e9f4c5ceade91

HEAD tree:
11b9d62db2d02649509f148aa01f8f74924c5792

index:
empty
```

Before this delivery exact Git-visible set is 52:

- `.aiassistant/records/aiscc/cycles/20260911_1935_aiscc-p2-3-a2-terminal-persisted-runtime-prerequisite-verification-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1935_aiscc-p2-3-a2-terminal-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260911_1935_aiscc-p2-3-actual-capture-runtime-prerequisite-verification-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_2140_aiscc-p2-3-runtime-prerequisite-not-ready-provisioning-contract-audit-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2140_aiscc-p2-3-runtime-prerequisite-verification-final-judgment-1.md`
- `.aiassistant/tasks/done/20260911_2140_aiscc-p2-3-private-s1-runtime-provisioning-contract-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_2148_aiscc-p2-3-provisioning-contract-partial-hold-image-build-authority-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2148_aiscc-p2-3-provisioning-contract-audit-image-build-authority-gap-judgment-1.md`
- `.aiassistant/tasks/done/20260911_2148_aiscc-p2-3-private-s1-image-build-input-authority-reconciliation-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_2250_aiscc-p2-3-image-build-authority-inspect-evidence-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2250_aiscc-p2-3-image-build-authority-inspect-identity-inconsistency-judgment-1.md`
- `.aiassistant/tasks/done/20260911_2250_aiscc-p2-3-base-image-inspect-identity-reconciliation-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_2300_aiscc-p2-3-base-image-inspect-replay-conflict-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2300_aiscc-p2-3-base-image-inspect-replay-conflict-judgment-1.md`
- `.aiassistant/tasks/done/20260911_2300_aiscc-p2-3-base-image-inspect-identity-reconciliation-retry-after-replay-conflict-1.md`
- `.aiassistant/records/aiscc/cycles/20260912_0010_aiscc-p2-3-base-image-authority-reconciled-cut-a-implementation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0010_aiscc-p2-3-base-image-authority-reconciliation-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260912_0010_aiscc-p2-3-private-s1-cut-a-image-provenance-and-docker-runner-source-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260912_0020_aiscc-p2-3-cut-a-static-failure-test-syntax-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0020_aiscc-p2-3-cut-a-static-failure-test-syntax-judgment-1.md`
- `.aiassistant/tasks/done/20260912_0020_aiscc-p2-3-private-s1-cut-a-test-syntax-rework-and-full-proof-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260912_0100_aiscc-p2-3-cut-a-static-ruff-line-wrap-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0100_aiscc-p2-3-cut-a-static-ruff-line-length-failure-judgment-1.md`
- `.aiassistant/tasks/done/20260912_0100_aiscc-p2-3-private-s1-cut-a-ruff-line-wrap-rework-and-full-proof-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260912_0120_aiscc-p2-3-cut-a-integration-fixture-runtime-root-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0120_aiscc-p2-3-cut-a-integration-fixture-runtime-root-collision-judgment-1.md`
- `.aiassistant/tasks/done/20260912_0120_aiscc-p2-3-private-s1-cut-a-runtime-root-fixture-rework-and-full-proof-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260912_0125_aiscc-p2-3-cut-a-static-verifier-defect-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0125_aiscc-p2-3-cut-a-static-verifier-harness-defect-judgment-1.md`
- `.aiassistant/tasks/done/20260912_0125_aiscc-p2-3-private-s1-cut-a-verifier-harness-correction-and-full-proof-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260912_0135_aiscc-p2-3-cut-a-materialized-fixture-root-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0135_aiscc-p2-3-cut-a-materialized-fixture-root-mismatch-judgment-1.md`
- `.aiassistant/tasks/done/20260912_0135_aiscc-p2-3-private-s1-cut-a-materialized-fixture-root-rework-and-full-proof-retry-1.md`
- `src/aiscc/bootstrap.py`
- `src/aiscc/providers/local_deterministic.py`
- `src/aiscc/providers/stockroom_tool.py`
- `src/aiscc/runtime/docker.py`
- `src/aiscc/runtime/stockroom_image.py`
- `src/aiscc/scenarios/composition.py`
- `src/aiscc/scenarios/stockroom_production.py`
- `config/providers/stockroom-owner-profiles.v2.toml`
- `config/providers/stockroom-tools.v2.toml`
- `examples/synthetic-stockroom/.dockerignore`
- `examples/synthetic-stockroom/Dockerfile`
- `examples/synthetic-stockroom/IMAGE_PROVENANCE.md`
- `tests/integration/scenarios/test_stockroom_binding.py`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`
- `tests/unit/providers/test_local_deterministic.py`
- `tests/unit/providers/test_stockroom_tool.py`
- `tests/unit/runtime/test_stockroom_docker_settlement.py`
- `tests/unit/runtime/test_stockroom_image.py`
- `tests/unit/scenarios/test_owner_composition.py`

After current Cycle/Judgment placement while Task is active:

```text
Git-visible:
54 exact

active Task:
exists byte-exact
ignored
```

Exact visible set:

- `.aiassistant/records/aiscc/cycles/20260911_1935_aiscc-p2-3-a2-terminal-persisted-runtime-prerequisite-verification-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1935_aiscc-p2-3-a2-terminal-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260911_1935_aiscc-p2-3-actual-capture-runtime-prerequisite-verification-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_2140_aiscc-p2-3-runtime-prerequisite-not-ready-provisioning-contract-audit-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2140_aiscc-p2-3-runtime-prerequisite-verification-final-judgment-1.md`
- `.aiassistant/tasks/done/20260911_2140_aiscc-p2-3-private-s1-runtime-provisioning-contract-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_2148_aiscc-p2-3-provisioning-contract-partial-hold-image-build-authority-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2148_aiscc-p2-3-provisioning-contract-audit-image-build-authority-gap-judgment-1.md`
- `.aiassistant/tasks/done/20260911_2148_aiscc-p2-3-private-s1-image-build-input-authority-reconciliation-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_2250_aiscc-p2-3-image-build-authority-inspect-evidence-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2250_aiscc-p2-3-image-build-authority-inspect-identity-inconsistency-judgment-1.md`
- `.aiassistant/tasks/done/20260911_2250_aiscc-p2-3-base-image-inspect-identity-reconciliation-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_2300_aiscc-p2-3-base-image-inspect-replay-conflict-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2300_aiscc-p2-3-base-image-inspect-replay-conflict-judgment-1.md`
- `.aiassistant/tasks/done/20260911_2300_aiscc-p2-3-base-image-inspect-identity-reconciliation-retry-after-replay-conflict-1.md`
- `.aiassistant/records/aiscc/cycles/20260912_0010_aiscc-p2-3-base-image-authority-reconciled-cut-a-implementation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0010_aiscc-p2-3-base-image-authority-reconciliation-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260912_0010_aiscc-p2-3-private-s1-cut-a-image-provenance-and-docker-runner-source-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260912_0020_aiscc-p2-3-cut-a-static-failure-test-syntax-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0020_aiscc-p2-3-cut-a-static-failure-test-syntax-judgment-1.md`
- `.aiassistant/tasks/done/20260912_0020_aiscc-p2-3-private-s1-cut-a-test-syntax-rework-and-full-proof-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260912_0100_aiscc-p2-3-cut-a-static-ruff-line-wrap-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0100_aiscc-p2-3-cut-a-static-ruff-line-length-failure-judgment-1.md`
- `.aiassistant/tasks/done/20260912_0100_aiscc-p2-3-private-s1-cut-a-ruff-line-wrap-rework-and-full-proof-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260912_0120_aiscc-p2-3-cut-a-integration-fixture-runtime-root-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0120_aiscc-p2-3-cut-a-integration-fixture-runtime-root-collision-judgment-1.md`
- `.aiassistant/tasks/done/20260912_0120_aiscc-p2-3-private-s1-cut-a-runtime-root-fixture-rework-and-full-proof-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260912_0125_aiscc-p2-3-cut-a-static-verifier-defect-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0125_aiscc-p2-3-cut-a-static-verifier-harness-defect-judgment-1.md`
- `.aiassistant/tasks/done/20260912_0125_aiscc-p2-3-private-s1-cut-a-verifier-harness-correction-and-full-proof-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260912_0135_aiscc-p2-3-cut-a-materialized-fixture-root-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0135_aiscc-p2-3-cut-a-materialized-fixture-root-mismatch-judgment-1.md`
- `.aiassistant/tasks/done/20260912_0135_aiscc-p2-3-private-s1-cut-a-materialized-fixture-root-rework-and-full-proof-retry-1.md`
- `src/aiscc/bootstrap.py`
- `src/aiscc/providers/local_deterministic.py`
- `src/aiscc/providers/stockroom_tool.py`
- `src/aiscc/runtime/docker.py`
- `src/aiscc/runtime/stockroom_image.py`
- `src/aiscc/scenarios/composition.py`
- `src/aiscc/scenarios/stockroom_production.py`
- `config/providers/stockroom-owner-profiles.v2.toml`
- `config/providers/stockroom-tools.v2.toml`
- `examples/synthetic-stockroom/.dockerignore`
- `examples/synthetic-stockroom/Dockerfile`
- `examples/synthetic-stockroom/IMAGE_PROVENANCE.md`
- `tests/integration/scenarios/test_stockroom_binding.py`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`
- `tests/unit/providers/test_local_deterministic.py`
- `tests/unit/providers/test_stockroom_tool.py`
- `tests/unit/runtime/test_stockroom_docker_settlement.py`
- `tests/unit/runtime/test_stockroom_image.py`
- `tests/unit/scenarios/test_owner_composition.py`
- `.aiassistant/records/aiscc/cycles/20260912_0230_aiscc-p2-3-cut-a-integration-launcher-defect-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0230_aiscc-p2-3-cut-a-integration-launcher-import-path-defect-judgment-1.md`

No extra/missing path.

# 3. exact Cut A candidate identity / zero mutation

Require all 19 Cut A candidate paths exactly:

- `src/aiscc/bootstrap.py`  `745b58da26ec300286ed69d1a7477b21afeb7625ec43e7f422560a657bc1c115`
- `src/aiscc/providers/local_deterministic.py`  `92ec8ba5553b05fe55fdbac30ab2dde8f57597c1055060a2f786dadd47f1c21a`
- `src/aiscc/providers/stockroom_tool.py`  `c5c925df000656ce32f65f4742f9a6936c2364d7d58eb92750966d8a8826e075`
- `src/aiscc/runtime/docker.py`  `284a3920f13f93928cc61420913506ed38af4e8f4d4e0e1f52d52c9074fa0753`
- `src/aiscc/runtime/stockroom_image.py`  `06e8d85e449a336392b73d9dec9915cd32d776688575a64030024609b08cec0e`
- `src/aiscc/scenarios/composition.py`  `a5f7ecb0d1bd9274f07094cbe3a4315098048c468472162e0ad84372fe6c50d3`
- `src/aiscc/scenarios/stockroom_production.py`  `685e2ec549473e167ed1fe4d7de1050d7a53a449d1d278dcdb3439a471478f1f`
- `config/providers/stockroom-owner-profiles.v2.toml`  `3f20d2d1ac4dd45709c47fc6572db4b97d6c33e0bebf02c6fd489dd9adbd022a`
- `config/providers/stockroom-tools.v2.toml`  `16015a97a00098e26f89a2972c87fd5ce0f4516c1afdf2bc20126fe6d1c61385`
- `examples/synthetic-stockroom/.dockerignore`  `99637a64da3b1b13bbf9a52459098d07bbc865aca11d004c89c3ee48965849f9`
- `examples/synthetic-stockroom/Dockerfile`  `94f71d8bf4b2f87e678e1a379dead19b7a850cf4522ec835bf6455f95d72b27a`
- `examples/synthetic-stockroom/IMAGE_PROVENANCE.md`  `166cfec29db4f46477b0117fae85a6a937343e3fb019a9b668b223b2eea8bae3`
- `tests/integration/scenarios/test_stockroom_binding.py`  `3979ff742a2c82752a7fbccb095b4ab8a4ed4915331ba4ec9d09cfa24aa3d4cf`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`  `373f9d5bc6f260785cdf943aa649ce99ab5826e8ae09dd2982c18db09459fbf5`
- `tests/unit/providers/test_local_deterministic.py`  `daa58e09dd3e81f2ba4a6edad236685c34a7c63852419ad3188aef51c8fe6209`
- `tests/unit/providers/test_stockroom_tool.py`  `e33b966cf5d575b7e55cd1ced2f3bfcd805833c08c1c66d6c650b693313c285d`
- `tests/unit/runtime/test_stockroom_docker_settlement.py`  `f7a33975072737417b3a922d4acd44e59be29547ceb87c864e24647d46236b19`
- `tests/unit/runtime/test_stockroom_image.py`  `e900bf8db350762655a167def704989527928cef575f69e740b013e5bfa4cee7`
- `tests/unit/scenarios/test_owner_composition.py`  `bfbae533d8453bef3940b1b652c5688b3b375b7e0fa40ae03e3196902888d652`

No mutation is authorized under:

```text
src/**
config/**
tests/**
examples/**
migrations/**
canonical state records
```

No new product/config/test/example path.

Any identity mismatch:

```text
CUT_A_DRAFT_IDENTITY_MISMATCH
→ STOP_WITH_REPORT_EXPORT
```

# 4. launcher invariant

All pytest commands in this Task MUST be launched from repository root with:

```text
.venv\Scripts\python.exe -B -m pytest
```

Forbidden:

```text
external Python script calling pytest.main(...)
PYTHONPATH mutation
sys.path mutation
sitecustomize/usercustomize tricks
test import rewrites
adding tests/__init__.py
copying tests package
changing current working directory away from repository root
```

External temporary verifier scripts are allowed only for non-pytest static checks.

# 5. static proof

Do not use `py_compile`.

In-memory compile these exact 14 Python paths:

```text
src/aiscc/bootstrap.py
src/aiscc/runtime/docker.py
src/aiscc/providers/stockroom_tool.py
src/aiscc/providers/local_deterministic.py
src/aiscc/scenarios/composition.py
src/aiscc/scenarios/stockroom_production.py
src/aiscc/runtime/stockroom_image.py
tests/unit/runtime/test_stockroom_docker_settlement.py
tests/unit/runtime/test_stockroom_image.py
tests/unit/providers/test_stockroom_tool.py
tests/unit/providers/test_local_deterministic.py
tests/unit/scenarios/test_owner_composition.py
tests/integration/scenarios/test_stockroom_binding.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Require:

```text
14 / 14 PASS
```

Run Ruff read-only on the same 14:

```text
0 findings
no --fix
no formatter
```

Run the corrected V1/V2 external verifier from the 0125/0135 contract:

```text
4 / 4 positive loaders
4 / 4 owner-profile direct comparisons
tool direct field comparison
9 / 9 negative cases
V1 frozen
```

Require:

```text
git diff --check PASS
index empty
all 19 candidate hashes exact
new repo-visible pyc 0
```

# 6. targeted unit proof

Run directly:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider   tests/unit/runtime/test_stockroom_image.py   tests/unit/runtime/test_stockroom_docker_settlement.py   tests/unit/providers/test_stockroom_tool.py   tests/unit/providers/test_local_deterministic.py   tests/unit/scenarios/test_owner_composition.py -ra
```

Require all collected PASS / zero skip.

No real Stockroom Docker subprocess.

# 7. disposable PostgreSQL prerequisite

Only after static + unit PASS, create one exact Task-owned disposable PostgreSQL
container:

```text
postgres:17.6-alpine
--pull=never
loopback only
temporary storage
unique Task-owned name
```

Migrate to:

```text
20260901_0008
```

No named persistent capture volume.

Export its connection URL only into the child pytest process environment as:

```text
AISCC_TEST_DATABASE_URL
```

Do not persist credentials/config in the repository.

# 8. focused corrected integration proof

First run the exact previously blocked test directly:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider   tests/integration/scenarios/test_stockroom_capture_runner.py::test_production_owner_graph_and_bounded_running_prefix   -ra
```

Require:

```text
1 PASS
0 skip
```

Do not use an external trace wrapper.

The Browser will interpret this PASS together with the frozen test source, whose exact
executable statements establish:

```text
private_runtime_root is created empty

materialized_destination == private_runtime_root

bounded workspace lease runtime_root == private_runtime_root

bounded workspace lease destination == materialized_destination

resolved_source_root == materialized_destination

materialized_call == ADMITTED / RUNNING / v2

later tampered/foreign-runtime negative cases remain

final private_runtime_root empty assertion executes
```

# 9. full integration proof

Only after focused PASS, run directly:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider   tests/integration/scenarios/test_stockroom_binding.py   tests/integration/scenarios/test_stockroom_capture_runner.py -ra
```

Require:

```text
all collected PASS
0 fail
0 error
0 skip
```

Do not substitute focused PASS for full integration.

No actual Stockroom image/process/provider/tool edge may execute.

# 10. regression proof

Only after full integration PASS, run directly:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider   tests/unit/scenarios/test_stockroom_capture_runner.py   tests/unit/security/test_stockroom_policy.py   tests/integration/evidence/test_postgres_evidence_admission.py   tests/integration/human/test_postgres_human_gate_judgment.py   tests/integration/workflow/test_postgres_kernel.py -ra
```

Require all collected PASS / zero skip.

# 11. 32/32 contract review

Require all rows PASS:

```text
BASE_REPODIGEST_FIXED
BASE_CONFIG_ID_NOT_USED_AS_PIN_AUTHORITY
FUTURE_STOCKROOM_IMAGE_ID_ABSENT
V2_CONFIG_HAS_NO_IMAGE_VALUE
V2_CONFIG_PROVENANCE_POLICY_STRICT
V1_CONFIG_FROZEN
V1_OWNER_PROFILES_FROZEN
PROVENANCE_SCHEMA_TYPED
PROVENANCE_REF_TYPED
PROVENANCE_CURRENTNESS_FAIL_CLOSED
RAW_OBJECT_NOT_AUTHORITY
STATIC_CONFIG_NOT_AUTHORITY
SOURCE_AGGREGATE_NOT_IMAGE_ID
PRODUCTION_RESOLVER_FIXED
PRODUCTION_ARBITRARY_RUNNER_REMOVED
DOCKER_SPEC_BINDS_PROVENANCE
RUNNER_INSPECTS_EXACT_IMAGE_ID
RUNNER_LABEL_PROJECTION_VERIFIED
RUNNER_SHELL_FALSE
RUNNER_OUTPUT_BOUNDED
RUNNER_TIMEOUT_SETTLED
RUNNER_CANCEL_SETTLED
RUNNER_OWNER_RECONCILED
UNKNOWN_OUTCOME_NO_RETRY
BUILD_CONTEXT_HISTORICAL_SOURCE_BOUND
DOCKERFILE_NOT_IN_14_FILE_AGGREGATE
NO_STOCKROOM_DOCKER_EXECUTION
NO_CANONICAL_PROVENANCE_JSON
NO_PERSISTENT_CAPTURE_DB
NO_ACTUAL_S1
NO_REPLAY
NO_GIT_PERSISTENCE
```

Require:

```text
32 / 32 PASS
```

# 12. forbidden actions

Do not execute:

```text
real Stockroom docker inspect/build/pull/create/run
registry/API/network lookup
Stockroom materialization outside bounded test seam
provider execution
tool dispatch
actual S1-S4
canonical stockroom-image-provenance.v1.json creation
persistent capture DB/volume
Replay
Git add/commit/push
```

The Task-owned disposable PostgreSQL test container is the sole Docker runtime exception.

# 13. cleanup

Remove only:

```text
Task-owned disposable PostgreSQL container
external temporary static verifier/config files
```

Verify exact container absence.

No broad cleanup.

# 14. final workspace

Before current Task movement:

```text
Git-visible:
54 exact
index empty
all 19 candidate bytes unchanged
```

Move current active Task byte-identically:

```text
.aiassistant/tasks/active/20260912_0230_aiscc-p2-3-private-s1-cut-a-direct-pytest-full-proof-retry-1.md
→
.aiassistant/tasks/done/20260912_0230_aiscc-p2-3-private-s1-cut-a-direct-pytest-full-proof-retry-1.md
```

Final:

```text
Git-visible:
55 exact
index empty
```

Exact final path set:

- `.aiassistant/records/aiscc/cycles/20260911_1935_aiscc-p2-3-a2-terminal-persisted-runtime-prerequisite-verification-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1935_aiscc-p2-3-a2-terminal-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260911_1935_aiscc-p2-3-actual-capture-runtime-prerequisite-verification-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_2140_aiscc-p2-3-runtime-prerequisite-not-ready-provisioning-contract-audit-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2140_aiscc-p2-3-runtime-prerequisite-verification-final-judgment-1.md`
- `.aiassistant/tasks/done/20260911_2140_aiscc-p2-3-private-s1-runtime-provisioning-contract-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_2148_aiscc-p2-3-provisioning-contract-partial-hold-image-build-authority-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2148_aiscc-p2-3-provisioning-contract-audit-image-build-authority-gap-judgment-1.md`
- `.aiassistant/tasks/done/20260911_2148_aiscc-p2-3-private-s1-image-build-input-authority-reconciliation-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_2250_aiscc-p2-3-image-build-authority-inspect-evidence-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2250_aiscc-p2-3-image-build-authority-inspect-identity-inconsistency-judgment-1.md`
- `.aiassistant/tasks/done/20260911_2250_aiscc-p2-3-base-image-inspect-identity-reconciliation-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_2300_aiscc-p2-3-base-image-inspect-replay-conflict-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2300_aiscc-p2-3-base-image-inspect-replay-conflict-judgment-1.md`
- `.aiassistant/tasks/done/20260911_2300_aiscc-p2-3-base-image-inspect-identity-reconciliation-retry-after-replay-conflict-1.md`
- `.aiassistant/records/aiscc/cycles/20260912_0010_aiscc-p2-3-base-image-authority-reconciled-cut-a-implementation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0010_aiscc-p2-3-base-image-authority-reconciliation-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260912_0010_aiscc-p2-3-private-s1-cut-a-image-provenance-and-docker-runner-source-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260912_0020_aiscc-p2-3-cut-a-static-failure-test-syntax-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0020_aiscc-p2-3-cut-a-static-failure-test-syntax-judgment-1.md`
- `.aiassistant/tasks/done/20260912_0020_aiscc-p2-3-private-s1-cut-a-test-syntax-rework-and-full-proof-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260912_0100_aiscc-p2-3-cut-a-static-ruff-line-wrap-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0100_aiscc-p2-3-cut-a-static-ruff-line-length-failure-judgment-1.md`
- `.aiassistant/tasks/done/20260912_0100_aiscc-p2-3-private-s1-cut-a-ruff-line-wrap-rework-and-full-proof-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260912_0120_aiscc-p2-3-cut-a-integration-fixture-runtime-root-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0120_aiscc-p2-3-cut-a-integration-fixture-runtime-root-collision-judgment-1.md`
- `.aiassistant/tasks/done/20260912_0120_aiscc-p2-3-private-s1-cut-a-runtime-root-fixture-rework-and-full-proof-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260912_0125_aiscc-p2-3-cut-a-static-verifier-defect-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0125_aiscc-p2-3-cut-a-static-verifier-harness-defect-judgment-1.md`
- `.aiassistant/tasks/done/20260912_0125_aiscc-p2-3-private-s1-cut-a-verifier-harness-correction-and-full-proof-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260912_0135_aiscc-p2-3-cut-a-materialized-fixture-root-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0135_aiscc-p2-3-cut-a-materialized-fixture-root-mismatch-judgment-1.md`
- `.aiassistant/tasks/done/20260912_0135_aiscc-p2-3-private-s1-cut-a-materialized-fixture-root-rework-and-full-proof-retry-1.md`
- `src/aiscc/bootstrap.py`
- `src/aiscc/providers/local_deterministic.py`
- `src/aiscc/providers/stockroom_tool.py`
- `src/aiscc/runtime/docker.py`
- `src/aiscc/runtime/stockroom_image.py`
- `src/aiscc/scenarios/composition.py`
- `src/aiscc/scenarios/stockroom_production.py`
- `config/providers/stockroom-owner-profiles.v2.toml`
- `config/providers/stockroom-tools.v2.toml`
- `examples/synthetic-stockroom/.dockerignore`
- `examples/synthetic-stockroom/Dockerfile`
- `examples/synthetic-stockroom/IMAGE_PROVENANCE.md`
- `tests/integration/scenarios/test_stockroom_binding.py`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`
- `tests/unit/providers/test_local_deterministic.py`
- `tests/unit/providers/test_stockroom_tool.py`
- `tests/unit/runtime/test_stockroom_docker_settlement.py`
- `tests/unit/runtime/test_stockroom_image.py`
- `tests/unit/scenarios/test_owner_composition.py`
- `.aiassistant/records/aiscc/cycles/20260912_0230_aiscc-p2-3-cut-a-integration-launcher-defect-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0230_aiscc-p2-3-cut-a-integration-launcher-import-path-defect-judgment-1.md`
- `.aiassistant/tasks/done/20260912_0230_aiscc-p2-3-private-s1-cut-a-direct-pytest-full-proof-retry-1.md`

# 15. failure semantics

Bootstrap failure:

```text
STOP / no report/export
```

After Task placement any mandatory failure:

```text
STOP_WITH_REPORT_EXPORT
```

No repository repair in this proof-only Task.

# 16. required export

Folder:

```text
.aiassistant/reports/target/20260912_0230_aiscc-p2-3-private-s1-cut-a-direct-pytest-full-proof-retry-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
STATIC_VERIFICATION.md
VERIFIER_HARNESS_VERIFICATION.md
IMAGE_PROVENANCE_MODEL_VERIFICATION.md
V2_CONFIG_VERIFICATION.md
DOCKER_RUNNER_VERIFICATION.md
BUILD_CONTEXT_CONTRACT_VERIFICATION.md
PRODUCTION_BINDING_VERIFICATION.md
UNIT_VERIFICATION.md
POSTGRESQL_INTEGRATION_VERIFICATION.md
FOCUSED_INTEGRATION_VERIFICATION.md
INTEGRATION_VERIFICATION.md
MATERIALIZED_FIXTURE_ROOT_VERIFICATION.md
REGRESSION_VERIFICATION.md
CONTRACT_REVIEW.md
```

Also include byte-preserving:

```text
current Cycle
current Judgment
current done Task

all 19 Cut A implementation paths
```

Expected:

```text
18 root docs
3 canonical copies
19 implementation copies
40 members total
```

`EXPORT_MANIFEST.md` covers all 39 non-self entries.

Create adjacent verified ZIP:

```text
one top-level directory
40 exact members
CRC PASS
folder/archive byte equality
```

# 17. success ceiling

Success:

```text
Cut A image/provenance source contract:
IMPLEMENTED_CANDIDATE

source-owned Docker settlement runner:
IMPLEMENTED_CANDIDATE

Cut A executable proof:
PASS

Cut A persistence:
NOT_AUTHORIZED

Cut B:
NOT_AUTHORIZED

canonical image provenance JSON:
ABSENT

persistent capture DB:
NOT_PROVISIONED

private S1:
NOT_AUTHORIZED

P2-3:
IN_PROGRESS
```
