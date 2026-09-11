# 작업지시서: P2-3 private S1 Cut A runtime-root fixture rework + full proof retry

## meta

- task_id: `20260912_0120_aiscc-p2-3-private-s1-cut-a-runtime-root-fixture-rework-and-full-proof-retry-1`
- created_at: `2026-09-12T01:20:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `TEST_FIXTURE_REWORK / FULL_CUT_A_PROOF_RETRY`
- evidence_profile: `HIGH_RISK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `21bb0769c5db126c1989d9e0eb8e9f4c5ceade91`
- required_tree: `11b9d62db2d02649509f148aa01f8f74924c5792`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. purpose

Correct the single integration-test fixture collision proven by the `0100` result.

Do not weaken production `StockroomWorkspace` runtime-root validation.

Do not redesign Cut A.

Then rerun the complete Cut A proof.

# 1. inbound transport

Verify Browser ZIP filename/SHA-256 from the Short Prompt.

Place current Task first:

```text
.aiassistant/tasks/active/20260912_0120_aiscc-p2-3-private-s1-cut-a-runtime-root-fixture-rework-and-full-proof-retry-1.md
```

Read fully; require it is ignored by canonical Git policy.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260912_0120_aiscc-p2-3-cut-a-integration-fixture-runtime-root-rework-proof-retry-entry-1.cycle.md
SHA-256:
21ac547967a4f1053bd91b743d747ca2415eaa81224386ca63b58ca4c4af5ae4

.aiassistant/reports/aiscc/20260912_0120_aiscc-p2-3-cut-a-integration-fixture-runtime-root-collision-judgment-1.md
SHA-256:
bf8c7f5b016245fcbdc0463673d84afd44c9742b441bfc4d76ffbfd19438bdf5
```

Bootstrap failure:

```text
STOP
no product mutation
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

Before this delivery exact Git-visible set is 43:

- `src/aiscc/bootstrap.py`
- `src/aiscc/providers/local_deterministic.py`
- `src/aiscc/providers/stockroom_tool.py`
- `src/aiscc/runtime/docker.py`
- `src/aiscc/scenarios/composition.py`
- `src/aiscc/scenarios/stockroom_production.py`
- `tests/integration/scenarios/test_stockroom_binding.py`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`
- `tests/unit/providers/test_local_deterministic.py`
- `tests/unit/providers/test_stockroom_tool.py`
- `tests/unit/runtime/test_stockroom_docker_settlement.py`
- `tests/unit/scenarios/test_owner_composition.py`
- `.aiassistant/records/aiscc/cycles/20260911_1935_aiscc-p2-3-a2-terminal-persisted-runtime-prerequisite-verification-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260911_2140_aiscc-p2-3-runtime-prerequisite-not-ready-provisioning-contract-audit-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260911_2148_aiscc-p2-3-provisioning-contract-partial-hold-image-build-authority-rework-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260911_2250_aiscc-p2-3-image-build-authority-inspect-evidence-rework-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260911_2300_aiscc-p2-3-base-image-inspect-replay-conflict-retry-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260912_0010_aiscc-p2-3-base-image-authority-reconciled-cut-a-implementation-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260912_0020_aiscc-p2-3-cut-a-static-failure-test-syntax-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260912_0100_aiscc-p2-3-cut-a-static-ruff-line-wrap-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1935_aiscc-p2-3-a2-terminal-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/reports/aiscc/20260911_2140_aiscc-p2-3-runtime-prerequisite-verification-final-judgment-1.md`
- `.aiassistant/reports/aiscc/20260911_2148_aiscc-p2-3-provisioning-contract-audit-image-build-authority-gap-judgment-1.md`
- `.aiassistant/reports/aiscc/20260911_2250_aiscc-p2-3-image-build-authority-inspect-identity-inconsistency-judgment-1.md`
- `.aiassistant/reports/aiscc/20260911_2300_aiscc-p2-3-base-image-inspect-replay-conflict-judgment-1.md`
- `.aiassistant/reports/aiscc/20260912_0010_aiscc-p2-3-base-image-authority-reconciliation-final-acceptance-judgment-1.md`
- `.aiassistant/reports/aiscc/20260912_0020_aiscc-p2-3-cut-a-static-failure-test-syntax-judgment-1.md`
- `.aiassistant/reports/aiscc/20260912_0100_aiscc-p2-3-cut-a-static-ruff-line-length-failure-judgment-1.md`
- `.aiassistant/tasks/done/20260911_1935_aiscc-p2-3-actual-capture-runtime-prerequisite-verification-1.md`
- `.aiassistant/tasks/done/20260911_2140_aiscc-p2-3-private-s1-runtime-provisioning-contract-audit-1.md`
- `.aiassistant/tasks/done/20260911_2148_aiscc-p2-3-private-s1-image-build-input-authority-reconciliation-audit-1.md`
- `.aiassistant/tasks/done/20260911_2250_aiscc-p2-3-base-image-inspect-identity-reconciliation-audit-1.md`
- `.aiassistant/tasks/done/20260911_2300_aiscc-p2-3-base-image-inspect-identity-reconciliation-retry-after-replay-conflict-1.md`
- `.aiassistant/tasks/done/20260912_0010_aiscc-p2-3-private-s1-cut-a-image-provenance-and-docker-runner-source-implementation-1.md`
- `.aiassistant/tasks/done/20260912_0020_aiscc-p2-3-private-s1-cut-a-test-syntax-rework-and-full-proof-retry-1.md`
- `.aiassistant/tasks/done/20260912_0100_aiscc-p2-3-private-s1-cut-a-ruff-line-wrap-rework-and-full-proof-retry-1.md`
- `config/providers/stockroom-owner-profiles.v2.toml`
- `config/providers/stockroom-tools.v2.toml`
- `examples/synthetic-stockroom/.dockerignore`
- `examples/synthetic-stockroom/Dockerfile`
- `examples/synthetic-stockroom/IMAGE_PROVENANCE.md`
- `src/aiscc/runtime/stockroom_image.py`
- `tests/unit/runtime/test_stockroom_image.py`

After current Cycle/Judgment placement while current Task is active:

```text
Git-visible:
45 exact

active Task:
exists byte-exact
ignored
```

Exact visible set:

- `src/aiscc/bootstrap.py`
- `src/aiscc/providers/local_deterministic.py`
- `src/aiscc/providers/stockroom_tool.py`
- `src/aiscc/runtime/docker.py`
- `src/aiscc/scenarios/composition.py`
- `src/aiscc/scenarios/stockroom_production.py`
- `tests/integration/scenarios/test_stockroom_binding.py`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`
- `tests/unit/providers/test_local_deterministic.py`
- `tests/unit/providers/test_stockroom_tool.py`
- `tests/unit/runtime/test_stockroom_docker_settlement.py`
- `tests/unit/scenarios/test_owner_composition.py`
- `.aiassistant/records/aiscc/cycles/20260911_1935_aiscc-p2-3-a2-terminal-persisted-runtime-prerequisite-verification-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260911_2140_aiscc-p2-3-runtime-prerequisite-not-ready-provisioning-contract-audit-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260911_2148_aiscc-p2-3-provisioning-contract-partial-hold-image-build-authority-rework-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260911_2250_aiscc-p2-3-image-build-authority-inspect-evidence-rework-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260911_2300_aiscc-p2-3-base-image-inspect-replay-conflict-retry-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260912_0010_aiscc-p2-3-base-image-authority-reconciled-cut-a-implementation-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260912_0020_aiscc-p2-3-cut-a-static-failure-test-syntax-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260912_0100_aiscc-p2-3-cut-a-static-ruff-line-wrap-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1935_aiscc-p2-3-a2-terminal-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/reports/aiscc/20260911_2140_aiscc-p2-3-runtime-prerequisite-verification-final-judgment-1.md`
- `.aiassistant/reports/aiscc/20260911_2148_aiscc-p2-3-provisioning-contract-audit-image-build-authority-gap-judgment-1.md`
- `.aiassistant/reports/aiscc/20260911_2250_aiscc-p2-3-image-build-authority-inspect-identity-inconsistency-judgment-1.md`
- `.aiassistant/reports/aiscc/20260911_2300_aiscc-p2-3-base-image-inspect-replay-conflict-judgment-1.md`
- `.aiassistant/reports/aiscc/20260912_0010_aiscc-p2-3-base-image-authority-reconciliation-final-acceptance-judgment-1.md`
- `.aiassistant/reports/aiscc/20260912_0020_aiscc-p2-3-cut-a-static-failure-test-syntax-judgment-1.md`
- `.aiassistant/reports/aiscc/20260912_0100_aiscc-p2-3-cut-a-static-ruff-line-length-failure-judgment-1.md`
- `.aiassistant/tasks/done/20260911_1935_aiscc-p2-3-actual-capture-runtime-prerequisite-verification-1.md`
- `.aiassistant/tasks/done/20260911_2140_aiscc-p2-3-private-s1-runtime-provisioning-contract-audit-1.md`
- `.aiassistant/tasks/done/20260911_2148_aiscc-p2-3-private-s1-image-build-input-authority-reconciliation-audit-1.md`
- `.aiassistant/tasks/done/20260911_2250_aiscc-p2-3-base-image-inspect-identity-reconciliation-audit-1.md`
- `.aiassistant/tasks/done/20260911_2300_aiscc-p2-3-base-image-inspect-identity-reconciliation-retry-after-replay-conflict-1.md`
- `.aiassistant/tasks/done/20260912_0010_aiscc-p2-3-private-s1-cut-a-image-provenance-and-docker-runner-source-implementation-1.md`
- `.aiassistant/tasks/done/20260912_0020_aiscc-p2-3-private-s1-cut-a-test-syntax-rework-and-full-proof-retry-1.md`
- `.aiassistant/tasks/done/20260912_0100_aiscc-p2-3-private-s1-cut-a-ruff-line-wrap-rework-and-full-proof-retry-1.md`
- `config/providers/stockroom-owner-profiles.v2.toml`
- `config/providers/stockroom-tools.v2.toml`
- `examples/synthetic-stockroom/.dockerignore`
- `examples/synthetic-stockroom/Dockerfile`
- `examples/synthetic-stockroom/IMAGE_PROVENANCE.md`
- `src/aiscc/runtime/stockroom_image.py`
- `tests/unit/runtime/test_stockroom_image.py`
- `.aiassistant/records/aiscc/cycles/20260912_0120_aiscc-p2-3-cut-a-integration-fixture-runtime-root-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0120_aiscc-p2-3-cut-a-integration-fixture-runtime-root-collision-judgment-1.md`

No extra/missing path.

# 3. exact Cut A candidate identity

Require current 19 implementation-path identities:

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
- `tests/integration/scenarios/test_stockroom_capture_runner.py`  `68fda7c133d134c076e184c2c7b9117a33f5477468647e8098dbae109a7c0d51`
- `tests/unit/providers/test_local_deterministic.py`  `daa58e09dd3e81f2ba4a6edad236685c34a7c63852419ad3188aef51c8fe6209`
- `tests/unit/providers/test_stockroom_tool.py`  `e33b966cf5d575b7e55cd1ced2f3bfcd805833c08c1c66d6c650b693313c285d`
- `tests/unit/runtime/test_stockroom_docker_settlement.py`  `f7a33975072737417b3a922d4acd44e59be29547ceb87c864e24647d46236b19`
- `tests/unit/runtime/test_stockroom_image.py`  `e900bf8db350762655a167def704989527928cef575f69e740b013e5bfa4cee7`
- `tests/unit/scenarios/test_owner_composition.py`  `bfbae533d8453bef3940b1b652c5688b3b375b7e0fa40ae03e3196902888d652`

Any mismatch:

```text
CUT_A_DRAFT_IDENTITY_MISMATCH
→ STOP_WITH_REPORT_EXPORT
```

# 4. exact mutation authority

Only:

```text
tests/integration/scenarios/test_stockroom_capture_runner.py
```

may change.

The other 18 Cut A paths are frozen exactly:

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
- `tests/unit/providers/test_local_deterministic.py`  `daa58e09dd3e81f2ba4a6edad236685c34a7c63852419ad3188aef51c8fe6209`
- `tests/unit/providers/test_stockroom_tool.py`  `e33b966cf5d575b7e55cd1ced2f3bfcd805833c08c1c66d6c650b693313c285d`
- `tests/unit/runtime/test_stockroom_docker_settlement.py`  `f7a33975072737417b3a922d4acd44e59be29547ceb87c864e24647d46236b19`
- `tests/unit/runtime/test_stockroom_image.py`  `e900bf8db350762655a167def704989527928cef575f69e740b013e5bfa4cee7`
- `tests/unit/scenarios/test_owner_composition.py`  `bfbae533d8453bef3940b1b652c5688b3b375b7e0fa40ae03e3196902888d652`

No new product/config/test/example path.

Any scope need beyond the one test:

```text
SCOPE_EXPANSION_REQUIRED
→ STOP_WITH_REPORT_EXPORT
```

# 5. exact fixture correction

Before edit require:

```text
tests/integration/scenarios/test_stockroom_capture_runner.py

SHA-256:
68fda7c133d134c076e184c2c7b9117a33f5477468647e8098dbae109a7c0d51

byte size:
40752
```

Within:

```text
test_production_owner_graph_and_bounded_running_prefix
```

perform exactly these semantic fixture changes.

Immediately after:

```python
docker_executable = tmp_path / "test-only-docker.exe"
docker_executable.write_bytes(b"fake executable; subprocess forbidden")
```

add:

```python
private_runtime_root = tmp_path / "private-runtime"
private_runtime_root.mkdir()
assert tuple(private_runtime_root.iterdir()) == ()
```

Change only the production-builder argument:

```python
private_runtime_root=tmp_path,
```

to:

```python
private_runtime_root=private_runtime_root,
```

Change only the final runtime cleanup assertion:

```python
assert tuple(tmp_path.iterdir()) == ()
```

to:

```python
assert tuple(private_runtime_root.iterdir()) == ()
```

Do not move the provenance JSON or fake Docker executable into the runtime root.

Do not delete the fixture files to make the root appear empty.

Do not change production workspace code.

After edit require exactly:

```text
byte size:
40920

SHA-256:
1861a8cfdd1008e5efba6588b17de8ad8b1f6f088912fba026d215a8ab6379f2
```

Mismatch:

```text
FIXTURE_REWORK_IDENTITY_MISMATCH
→ STOP_WITH_REPORT_EXPORT
```

# 6. fixture-boundary verification

Before calling `build_stockroom_production`, executable test evidence must establish:

```text
tmp_path / test-only-provenance.json:
exists

tmp_path / test-only-docker.exe:
exists

private_runtime_root:
exists

private_runtime_root:
empty

fixture files are not under private_runtime_root
```

The test must continue to prove at the end:

```text
private_runtime_root:
empty
```

This is a fixture correction, not a weakening of cleanup semantics.

# 7. static proof

Do not use `py_compile`.

In-memory compile the same exact 14 Cut A Python paths used by `0100`.

Require:

```text
14 / 14 PASS
```

Run Ruff read-only on the same 14:

```text
no --fix
no formatter
0 findings
```

Strict-load:

```text
stockroom-tools.v1
stockroom-tools.v2
stockroom-owner-profiles.v1
stockroom-owner-profiles.v2
```

Require:

```text
4 / 4 PASS
```

and preserve the previously proven negative cases.

Require:

```text
git diff --check PASS
index empty
new repo-visible pyc 0
18 frozen Cut A hashes exact
```

Mandatory failure:

```text
STATIC_CHECK_FAILURE
→ STOP_WITH_REPORT_EXPORT
```

No same-turn repair.

# 8. targeted unit proof

Run the same exact five unit modules from the `0100` Task:

```text
tests/unit/runtime/test_stockroom_image.py
tests/unit/runtime/test_stockroom_docker_settlement.py
tests/unit/providers/test_stockroom_tool.py
tests/unit/providers/test_local_deterministic.py
tests/unit/scenarios/test_owner_composition.py
```

Use:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider ... -ra
```

Require:

```text
all collected PASS
0 fail
0 error
0 skip
```

No real Stockroom Docker subprocess.

# 9. disposable PostgreSQL test prerequisite

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

This remains test infrastructure only.

# 10. integration proof

Run:

```text
tests/integration/scenarios/test_stockroom_binding.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Require:

```text
all collected PASS
0 fail
0 error
0 skip
```

For `test_production_owner_graph_and_bounded_running_prefix`, specifically record:

```text
dedicated private runtime root was empty before application construction
production application construction passed RUNTIME_ROOT_NOT_EMPTY gate
no real Stockroom Docker/provider/tool runtime edge executed
final dedicated private runtime root empty
```

If a new independent integration failure appears:

```text
TEST_FAILURE
→ STOP_WITH_REPORT_EXPORT
```

No same-turn repair.

# 11. regression proof

Only after integration PASS, run:

```text
tests/unit/scenarios/test_stockroom_capture_runner.py
tests/unit/security/test_stockroom_policy.py
tests/integration/evidence/test_postgres_evidence_admission.py
tests/integration/human/test_postgres_human_gate_judgment.py
tests/integration/workflow/test_postgres_kernel.py
```

Require all collected PASS / zero skip.

# 12. 32/32 contract review

Require all 32 prior Cut A contract rows PASS:

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

# 13. forbidden actions

Do not execute:

```text
real Stockroom docker image inspect/build/pull/create/run
registry/API/network lookup
Stockroom materialization
provider execution
tool dispatch
actual S1-S4
canonical stockroom-image-provenance.v1.json creation
persistent capture DB/volume
Replay
Git add/commit/push
```

The Task-owned disposable PostgreSQL test container is the sole Docker runtime
exception.

# 14. cleanup

Remove only:

```text
Task-owned disposable PostgreSQL container
external temporary verifier files
```

Do not broad-clean pytest or Docker.

# 15. final workspace

Before current Task movement:

```text
Git-visible:
45 exact

index:
empty
```

The test path was already visible, so its rework adds no path.

Move current active Task byte-identically:

```text
.aiassistant/tasks/active/20260912_0120_aiscc-p2-3-private-s1-cut-a-runtime-root-fixture-rework-and-full-proof-retry-1.md
→
.aiassistant/tasks/done/20260912_0120_aiscc-p2-3-private-s1-cut-a-runtime-root-fixture-rework-and-full-proof-retry-1.md
```

Final:

```text
Git-visible:
46 exact

index:
empty
```

Exact final set:

- `src/aiscc/bootstrap.py`
- `src/aiscc/providers/local_deterministic.py`
- `src/aiscc/providers/stockroom_tool.py`
- `src/aiscc/runtime/docker.py`
- `src/aiscc/scenarios/composition.py`
- `src/aiscc/scenarios/stockroom_production.py`
- `tests/integration/scenarios/test_stockroom_binding.py`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`
- `tests/unit/providers/test_local_deterministic.py`
- `tests/unit/providers/test_stockroom_tool.py`
- `tests/unit/runtime/test_stockroom_docker_settlement.py`
- `tests/unit/scenarios/test_owner_composition.py`
- `.aiassistant/records/aiscc/cycles/20260911_1935_aiscc-p2-3-a2-terminal-persisted-runtime-prerequisite-verification-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260911_2140_aiscc-p2-3-runtime-prerequisite-not-ready-provisioning-contract-audit-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260911_2148_aiscc-p2-3-provisioning-contract-partial-hold-image-build-authority-rework-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260911_2250_aiscc-p2-3-image-build-authority-inspect-evidence-rework-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260911_2300_aiscc-p2-3-base-image-inspect-replay-conflict-retry-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260912_0010_aiscc-p2-3-base-image-authority-reconciled-cut-a-implementation-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260912_0020_aiscc-p2-3-cut-a-static-failure-test-syntax-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260912_0100_aiscc-p2-3-cut-a-static-ruff-line-wrap-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1935_aiscc-p2-3-a2-terminal-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/reports/aiscc/20260911_2140_aiscc-p2-3-runtime-prerequisite-verification-final-judgment-1.md`
- `.aiassistant/reports/aiscc/20260911_2148_aiscc-p2-3-provisioning-contract-audit-image-build-authority-gap-judgment-1.md`
- `.aiassistant/reports/aiscc/20260911_2250_aiscc-p2-3-image-build-authority-inspect-identity-inconsistency-judgment-1.md`
- `.aiassistant/reports/aiscc/20260911_2300_aiscc-p2-3-base-image-inspect-replay-conflict-judgment-1.md`
- `.aiassistant/reports/aiscc/20260912_0010_aiscc-p2-3-base-image-authority-reconciliation-final-acceptance-judgment-1.md`
- `.aiassistant/reports/aiscc/20260912_0020_aiscc-p2-3-cut-a-static-failure-test-syntax-judgment-1.md`
- `.aiassistant/reports/aiscc/20260912_0100_aiscc-p2-3-cut-a-static-ruff-line-length-failure-judgment-1.md`
- `.aiassistant/tasks/done/20260911_1935_aiscc-p2-3-actual-capture-runtime-prerequisite-verification-1.md`
- `.aiassistant/tasks/done/20260911_2140_aiscc-p2-3-private-s1-runtime-provisioning-contract-audit-1.md`
- `.aiassistant/tasks/done/20260911_2148_aiscc-p2-3-private-s1-image-build-input-authority-reconciliation-audit-1.md`
- `.aiassistant/tasks/done/20260911_2250_aiscc-p2-3-base-image-inspect-identity-reconciliation-audit-1.md`
- `.aiassistant/tasks/done/20260911_2300_aiscc-p2-3-base-image-inspect-identity-reconciliation-retry-after-replay-conflict-1.md`
- `.aiassistant/tasks/done/20260912_0010_aiscc-p2-3-private-s1-cut-a-image-provenance-and-docker-runner-source-implementation-1.md`
- `.aiassistant/tasks/done/20260912_0020_aiscc-p2-3-private-s1-cut-a-test-syntax-rework-and-full-proof-retry-1.md`
- `.aiassistant/tasks/done/20260912_0100_aiscc-p2-3-private-s1-cut-a-ruff-line-wrap-rework-and-full-proof-retry-1.md`
- `config/providers/stockroom-owner-profiles.v2.toml`
- `config/providers/stockroom-tools.v2.toml`
- `examples/synthetic-stockroom/.dockerignore`
- `examples/synthetic-stockroom/Dockerfile`
- `examples/synthetic-stockroom/IMAGE_PROVENANCE.md`
- `src/aiscc/runtime/stockroom_image.py`
- `tests/unit/runtime/test_stockroom_image.py`
- `.aiassistant/records/aiscc/cycles/20260912_0120_aiscc-p2-3-cut-a-integration-fixture-runtime-root-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0120_aiscc-p2-3-cut-a-integration-fixture-runtime-root-collision-judgment-1.md`
- `.aiassistant/tasks/done/20260912_0120_aiscc-p2-3-private-s1-cut-a-runtime-root-fixture-rework-and-full-proof-retry-1.md`

No other path.

# 16. required export

Folder:

```text
.aiassistant/reports/target/20260912_0120_aiscc-p2-3-private-s1-cut-a-runtime-root-fixture-rework-and-full-proof-retry-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
FIXTURE_RUNTIME_ROOT_VERIFICATION.md
STATIC_VERIFICATION.md
IMAGE_PROVENANCE_MODEL_VERIFICATION.md
V2_CONFIG_VERIFICATION.md
DOCKER_RUNNER_VERIFICATION.md
BUILD_CONTEXT_CONTRACT_VERIFICATION.md
PRODUCTION_BINDING_VERIFICATION.md
UNIT_VERIFICATION.md
INTEGRATION_VERIFICATION.md
REGRESSION_VERIFICATION.md
CONTRACT_REVIEW.md
POSTGRESQL_INTEGRATION_VERIFICATION.md
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
16 root docs
3 canonical copies
19 implementation copies
38 members total
```

`EXPORT_MANIFEST.md` covers all 37 non-self entries.

Create adjacent verified ZIP:

```text
one top-level directory
38 exact members
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
