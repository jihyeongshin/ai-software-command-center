# 작업지시서: P2-3 A2 materialized-workspace fixture contract test retry

## meta

- task_id: `20260911_0228_aiscc-p2-3-a2-materialized-workspace-fixture-contract-test-retry-1`
- created_at: `2026-09-11T02:28:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `TEST_REWORK / POSTGRESQL_REGRESSION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `876f232880e652fbf715f13c13b8cc03d27404f0`
- required_base_tree: `0f855b67fcad1be1cb4f635b6b4db8856c43da64`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. purpose

Do not redesign the current prepared-owner/materialized-result candidate.

The 0105 production source candidate is frozen.

Correct only the no-side-effect integration fixture whose declared materialized workspace does not exist, then rerun the complete blocked proof chain.

# 1. inbound transport

Verify Browser delivery ZIP exact filename/SHA-256 from the Short Prompt.

Place TASK first at:

```text
.aiassistant/tasks/active/20260911_0228_aiscc-p2-3-a2-materialized-workspace-fixture-contract-test-retry-1.md
```

Read fully.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260911_0228_aiscc-p2-3-a2-materialized-workspace-fixture-test-retry-entry-1.cycle.md
SHA-256:
ad098a086ae45c164db4e6ecbadfc53e189811e2f6f76f243d5b661a81306062

.aiassistant/reports/aiscc/20260911_0228_aiscc-p2-3-a2-materialized-workspace-fixture-test-failure-judgment-1.md
SHA-256:
676937b4e48e32d5798a31d203632239023df0c79c47d382d0b74fa61d99cf27
```

Bootstrap failure before canonical Task placement:

```text
STOP
no report/export
no substantive mutation
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

Expected Git-visible set excluding active Task is exact 33 paths:

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
- `.aiassistant/records/aiscc/cycles/20260911_0228_aiscc-p2-3-a2-materialized-workspace-fixture-test-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_0228_aiscc-p2-3-a2-materialized-workspace-fixture-test-failure-judgment-1.md`

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Ignored target/export residue remains non-blocking.

# 3. exact identity gate

Require exact pending governance:

- `.aiassistant/tasks/done/20260910_1738_aiscc-p2-3-a2-production-owner-bootstrap-integration-feasibility-audit-1.md`  `c8f6615b9ce5943e1bee43046d50dd2dac4efba99a96179043177530f3a96ce4`
- `.aiassistant/records/aiscc/cycles/20260910_1738_aiscc-p2-3-a1-terminal-persisted-a2-feasibility-entry-1.cycle.md`  `0e6b3a12767fc3d5830726e1327d8e0d6f097271aa7aedd4157a4b86a566a782`
- `.aiassistant/reports/aiscc/20260910_1738_aiscc-p2-3-a1-terminal-state-persistence-final-acceptance-judgment-1.md`  `4df00fc71ff6603cb0703077c10c5460d3db2bdb6ec772a2b3fbd8b5983ed476`
- `.aiassistant/tasks/done/20260910_1824_aiscc-p2-3-a2-production-owner-bootstrap-integration-implementation-1.md`  `13b3561669bfa5c9343bc0339f52bb77b06eab56e1c97369f6a4973766178997`
- `.aiassistant/records/aiscc/cycles/20260910_1824_aiscc-p2-3-a2-feasibility-accepted-production-integration-entry-1.cycle.md`  `a02818022b2c694ad2644c2222e127de87c38f360b65fc33937c42af2cdb9846`
- `.aiassistant/reports/aiscc/20260910_1824_aiscc-p2-3-a2-feasibility-audit-final-acceptance-judgment-1.md`  `743103b7e8e22c7833bd555ff8ceedd0e0f34e0ab4994f077006864fbf172a85`
- `.aiassistant/tasks/done/20260910_1948_aiscc-p2-3-a2-production-integration-static-and-runtime-evidence-binding-rework-1.md`  `2592d9fc0635c4fc61b41929d78bab59b9de19c496fe8d98334bb14e12148e5b`
- `.aiassistant/records/aiscc/cycles/20260910_1948_aiscc-p2-3-a2-static-failure-runtime-evidence-binding-rework-entry-1.cycle.md`  `2206f489bca4de6f1da211beeba932e0125da05dceeb329bef9fe19938770dd1`
- `.aiassistant/reports/aiscc/20260910_1948_aiscc-p2-3-a2-static-failure-runtime-evidence-binding-judgment-1.md`  `534a863b8df861cd96091e7678b58ed12b35eebd6272ed867ab55a1d240e58ea`
- `.aiassistant/tasks/done/20260910_2215_aiscc-p2-3-a2-security-clock-domain-test-failure-rework-1.md`  `50f35f57def86ab6535befafdb7022b7a0806f60f52d67a0fc9697a883834482`
- `.aiassistant/records/aiscc/cycles/20260910_2215_aiscc-p2-3-a2-security-clock-domain-rework-entry-1.cycle.md`  `dde57e4dae071826ca377b9cc32a4a34cf25dd3d368b897d695156e600022eec`
- `.aiassistant/reports/aiscc/20260910_2215_aiscc-p2-3-a2-security-clock-domain-test-failure-judgment-1.md`  `ea62c1e759018fcc21b32e0760915c38f8c1afe092ecb550025a9021ac2ce201`
- `.aiassistant/tasks/done/20260910_2220_aiscc-p2-3-a2-prepared-owner-binding-contract-reconciliation-audit-1.md`  `46716dd1ad7c292768e65319cc5116cca74ed48e45e50dd55b117c5376f5f7b1`
- `.aiassistant/records/aiscc/cycles/20260910_2220_aiscc-p2-3-a2-prepared-owner-binding-contract-reconciliation-entry-1.cycle.md`  `fd54dd082ad71f5bf7c130efa015ec944f35bfbd6203dc96ccc6dab8aaf959cb`
- `.aiassistant/reports/aiscc/20260910_2220_aiscc-p2-3-a2-prepared-owner-binding-mismatch-judgment-1.md`  `c301beb57ebb85706b22df0a144225e8b608160e5cd53a788a162b8029aa48e3`
- `.aiassistant/tasks/done/20260910_2355_aiscc-p2-3-a2-prepared-owner-model-reconciliation-implementation-1.md`  `202c6952f9c404437cb72a2ed9bf4ecc920ea3ff653a659c64b356e47a4a4e29`
- `.aiassistant/records/aiscc/cycles/20260910_2355_aiscc-p2-3-a2-prepared-owner-audit-accepted-model-reconciliation-entry-1.cycle.md`  `b3ebb1ce4b9c59afcece0350f6ef51dd35b35f044e59da5ba938d920fb0b013c`
- `.aiassistant/reports/aiscc/20260910_2355_aiscc-p2-3-a2-prepared-owner-contract-audit-final-acceptance-judgment-1.md`  `a22f2962f82998c2b2808b057181f639699e9ccb368daee0bf2fbb3d5450d199`
- `.aiassistant/tasks/done/20260911_0105_aiscc-p2-3-a2-materialization-output-provenance-binding-rework-1.md`  `5ee0cd082646eeddaf7e56030d9f728c72835e144577c01a427e14f844fa129c`
- `.aiassistant/records/aiscc/cycles/20260911_0105_aiscc-p2-3-a2-owner-model-static-failure-materialization-output-binding-rework-entry-1.cycle.md`  `331d32681194e51fbf0a1c469c0b4e690f3800f5ebc25093bc4eff2b81406ccc`
- `.aiassistant/reports/aiscc/20260911_0105_aiscc-p2-3-a2-owner-model-static-failure-materialization-output-binding-judgment-1.md`  `83d9fdf0a23d1a0232cacb9645a3195b7e5a9eb8e1cc541fcf31b4d5d7cd933e`

Require exact current A2/B3 candidate:

- `src/aiscc/bootstrap.py`  `1718e596b20fd107af0cb80b6ad40e3626b7e26d8d45daa649ccf2d2ccf9fe38`
- `src/aiscc/scenarios/driver.py`  `c83792b0d84d07d584e4b5b32b1925a42a8be25cc0a872f19b92cffa2150a44c`
- `src/aiscc/scenarios/composition.py`  `2017a18175e0e227fe1514d3d9e85c7d0d64d391ec94649912d9749699b7edfc`
- `src/aiscc/scenarios/stockroom_production.py`  `742ffd8122507de941e93b9e721a97335afa9acf475ff8fd01d50fdacbf8137a`
- `config/evidence/stockroom-capture.v1.json`  `70d4dbf219d54abd57877b787d8ac16d0efbe05701e7fb8bf1f84282640b31e7`
- `config/human/stockroom-capture.v1.json`  `7ec43975b8d1f30ded987d05942753dadbd93197ad86da2701514a198e797bab`
- `config/judgment/stockroom-capture.v1.json`  `31f8d08c083218d1fcc47d5ba7a8d1c151a48bbf26ea3319ac9503a666179eef`
- `tests/unit/scenarios/test_owner_composition.py`  `68cf0561e482e1ded6f6bddaa8b91da1fea753b430527e27fe66bf7cf0cb4d12`
- `tests/integration/scenarios/test_stockroom_binding.py`  `063e2b65eb229b5849bc3df61294d72f3f656783ac1257a4dbcaa82bb2d70b34`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`  `61918fd28e68e0bf7140256f9e7c876f8be50491a6f972f37f4e6ea6698788a4`

Mismatch:

```text
PREDECESSOR_OR_CANDIDATE_IDENTITY_MISMATCH
→ STOP
```

# 4. pre-mutation root-cause verification

Read current:

```text
src/aiscc/runtime/docker.py
src/aiscc/providers/stockroom_tool.py
src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Before editing, verify:

```text
A. Stockroom execution construction calls build_stockroom_spec
B. Stockroom spec fingerprint/validation requires workspace.is_dir()
C. current positive stub uses:
   tmp_path / "bounded-materialized-output"
D. that child directory is not created before adapter.materialize()
E. adapter materialize catches the resulting construction ValueError fail-closed as DENIED
```

If any premise is false:

```text
ROOT_CAUSE_MISMATCH
→ STOP
```

Do not guess another fix.

# 5. exact mutation authority

Only:

```text
MODIFY
tests/integration/scenarios/test_stockroom_capture_runner.py
```

All source/config/model paths are frozen, including:

```text
src/aiscc/bootstrap.py
src/aiscc/scenarios/driver.py
src/aiscc/scenarios/composition.py
src/aiscc/scenarios/stockroom_production.py
src/aiscc/scenarios/capture_runner.py
src/aiscc/runtime/**
src/aiscc/providers/**
src/aiscc/security/**
src/aiscc/evidence/**
src/aiscc/judgment/**
config/evidence/stockroom-capture.v1.json
config/human/stockroom-capture.v1.json
config/judgment/stockroom-capture.v1.json
all migrations
```

If production source appears to require change:

```text
SCOPE_EXPANSION_REQUIRED
→ STOP
```

# 6. positive fixture correction

In the bounded positive materializer stub setup, replace the nonexistent declared workspace destination with an already existing absolute directory.

Authorized intended form:

```text
materialized_destination = tmp_path
```

Then keep:

```text
workspace_lease.runtime_root = tmp_path
workspace_lease.destination = materialized_destination
resolved_source_root = materialized_destination
```

Do not create:

```text
tmp_path / "bounded-materialized-output"
```

or any other child solely to satisfy `workspace.is_dir()`.

The test must still end with:

```text
tuple(tmp_path.iterdir()) == ()
```

to prove no filesystem content/materialization was created.

# 7. test meaning must remain narrow

The stub remains test instrumentation.

It may prove:

```text
the exact derived materializer method was called
the exact return object was bound by the exact factory
execution-factory construction consumes only that bound result
anti-swap cases reject
```

It may not claim:

```text
real Stockroom filesystem materialization
real Git object read
real Docker/process readiness
```

# 8. preserve all anti-swap coverage

Do not remove or weaken existing 0105 negative cases for:

```text
raw MaterializedStockroom
replacement result binding
foreign prepared binding
foreign materializer factory
foreign execution factory
foreign run
foreign attempt
foreign resource
source commit/subroot/subtree/aggregate mutation
file-manifest mutation
workspace lease mutation
resolved-source-root mutation
provenance fingerprint mutation
spec/registry/dispatcher/execution-reference swap
```

Keep the exact factory-return object identity proof.

# 9. preserve known candidate invariants

Do not regress:

```text
seven stable exact owner identities
exact materializer_factory binding
exact execution-service factory binding
immutable prepared attempt binding
factory-issued materialized-result provenance
execution provenance binds materialized-result fingerprint
security native TTL clock fix
ToolOutputRef runtime-summary evidence binding
NETWORK denied
A1 runner semantics
```

# 10. static gate

Run quote-safe static checks.

Required Python set:

```text
src/aiscc/bootstrap.py
src/aiscc/scenarios/driver.py
src/aiscc/scenarios/composition.py
src/aiscc/scenarios/stockroom_production.py
src/aiscc/scenarios/capture_runner.py
tests/unit/scenarios/test_owner_composition.py
tests/integration/scenarios/test_stockroom_binding.py
tests/integration/scenarios/test_stockroom_capture_runner.py
tests/unit/scenarios/test_stockroom_capture_runner.py
```

Require:

```text
py_compile:
9 / 9 PASS

Ruff:
all PASS

strict A2 configs:
3 / 3 PASS

git diff --check:
PASS

index:
empty
```

Failure:

```text
STATIC_CHECK_FAILURE
→ STOP
```

No same-turn repair after mandatory static failure.

# 11. B3 prepared-owner proof

Run:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider   tests/unit/scenarios/test_owner_composition.py   tests/integration/scenarios/test_stockroom_binding.py -ra
```

Expected current baseline:

```text
23 passed
```

Require all PASS.

# 12. A1 runner proof

Run:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider   tests/unit/scenarios/test_stockroom_capture_runner.py -ra
```

Expected:

```text
51 passed
```

Require all PASS.

# 13. PostgreSQL prerequisite

Use the same bounded local disposable PostgreSQL pattern already used by 0105/2215.

No external pull/network.

Require Alembic head:

```text
20260901_0008
```

# 14. mandatory A2 integration

Run once:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider   tests/integration/scenarios/test_stockroom_capture_runner.py -ra
```

Expected current collection:

```text
2 tests
```

Require:

```text
2 passed
0 failed
0 errors
0 skipped
```

The positive owner-model test must now reach and pass all materialized-result / execution-factory / anti-swap assertions.

No real materializer filesystem work may occur.

# 15. direct-owner regressions

Only after A2 module PASS, run exact bounded set:

```text
tests/integration/workflow/test_postgres_kernel.py
tests/integration/evidence/test_postgres_evidence_admission.py
tests/integration/human/test_postgres_human_gate_judgment.py
tests/unit/security/test_stockroom_policy.py
```

Expected predecessor baseline:

```text
58 passed
```

Require all PASS and no DB-prerequisite skip.

# 16. aggregate expected executable evidence

If test inventories remain unchanged:

```text
B3:
23 PASS

A1:
51 PASS

A2:
2 PASS

direct-owner:
58 PASS

aggregate:
134 PASS
0 fail
0 error
0 skip
```

If a legitimate inventory difference exists, report exact reason and require every collected test to execute and PASS.

# 17. runtime ceiling

Allowed:

```text
PostgreSQL/Alembic
NONE -> READY -> RUNNING
attempt creation
security evaluation
factory object construction
monkeypatched no-side-effect StockroomMaterializer.materialize return
```

Forbidden:

```text
real Stockroom filesystem materialization
Git source-object materialization
Stockroom Docker/process
provider
tool dispatch
AgentExecutionService.execute
network
real secret
full runner.run()
actual S1-S4
HumanResult
terminal scenario Judgment
Replay
Git add/commit/push
```

# 18. contract review

Require PASS:

```text
TEST_FIXTURE_WORKSPACE_PRECONDITION_SATISFIED
NO_FIXTURE_FILESYSTEM_CONTENT_CREATED
PREPARED_OWNER_EXACT_BINDING_PRESERVED
SEVEN_STABLE_OWNER_IDENTITIES_EXACT
MATERIALIZER_FACTORY_EXACTLY_BOUND
EXECUTION_FACTORY_EXACTLY_BOUND
PREPARED_ATTEMPT_BINDING_IMMUTABLE
ADAPTER_CONSUMES_PREPARED_FACTORIES
NO_PARALLEL_FACTORY_AUTHORITY
DERIVED_MATERIALIZER_PROVENANCE_BOUND
MATERIALIZED_RESULT_FACTORY_ISSUED
MATERIALIZED_RESULT_BINDS_EXACT_DERIVED_OWNER
MATERIALIZED_RESULT_BINDS_PREPARED_RUN_ATTEMPT_CONFIG
RAW_MATERIALIZED_OBJECT_NOT_AUTHORITY
MATERIALIZED_OUTPUT_FINGERPRINT_BOUND
EXECUTION_FACTORY_REQUIRES_BOUND_RESULT
DERIVED_EXECUTION_SERVICE_PROVENANCE_BINDS_MATERIALIZED_RESULT
ANTI_OWNER_SWAP_FAIL_CLOSED
NO_PRIVATE_LATE_BINDING_MUTATION
B1_MATERIALIZER_AUTHORITY_PRESERVED
P1_5_EXECUTION_AUTHORITY_PRESERVED
A1_RUNNER_SEMANTICS_UNCHANGED
SECURITY_CLOCK_FIX_RETAINED
TOOL_OUTPUT_RUNTIME_EVIDENCE_BINDING_RETAINED
NETWORK_DENIED
NO_REAL_RUNTIME_SIDE_EFFECT
S2_BINDING_STILL_EXPLICITLY_PENDING
```

Require:

```text
27 / 27 PASS
```

# 19. cleanup

Remove only the exact Task-owned disposable PostgreSQL container after evidence collection.

No broad cleanup.

# 20. final workspace

Before current Task lifecycle:

```text
existing Git-visible:
31

current Cycle/Judgment:
2

total excluding active Task:
33 exact

index:
empty
```

The integration test is already Git-visible, so changing its bytes does not add another path.

Move active Task byte-identically to:

```text
.aiassistant/tasks/done/20260911_0228_aiscc-p2-3-a2-materialized-workspace-fixture-contract-test-retry-1.md
```

Final expected:

```text
34 exact Git-visible paths
index empty
```

No other delta.

# 21. no Git persistence

Do not run:

```text
git add
git commit
git push
```

# 22. required export bundle

Folder:

```text
.aiassistant/reports/target/20260911_0228_aiscc-p2-3-a2-materialized-workspace-fixture-contract-test-retry-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
ROOT_CAUSE_VERIFICATION.md
STATIC_VERIFICATION.md
POSTGRESQL_INTEGRATION_VERIFICATION.md
MATERIALIZATION_OUTPUT_BINDING_VERIFICATION.md
ANTI_SWAP_VERIFICATION.md
REGRESSION_VERIFICATION.md
CONTRACT_REVIEW.md
```

Also include byte-preserving copies of:

```text
current Cycle
current Judgment
current done Task
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Expected:

```text
11 root docs
4 canonical/test copies
15 members total
```

`EXPORT_MANIFEST.md` covers all 14 non-self entries with relative path, byte size, SHA-256.

Require one top-level directory, CRC PASS, exact members, manifest exact, and folder/archive byte equality.

# 23. mandatory stop

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

No same-turn repair after mandatory static/test failure.

# 24. success ceiling

Success:

```text
prepared-owner + materialized-output candidate:
EXECUTABLE_PROOF_COMPLETE / BROWSER_JUDGMENT_REQUIRED

A2 S2 Judgment binding:
STILL REWORK_REQUIRED / NEXT AUTHORITY TASK

A2 persistence:
NOT_AUTHORIZED

Stockroom runtime prerequisites:
NOT_VERIFIED

actual S1-S4:
NOT_STARTED
```
