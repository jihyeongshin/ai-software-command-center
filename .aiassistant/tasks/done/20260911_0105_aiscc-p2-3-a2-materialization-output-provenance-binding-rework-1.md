# 작업지시서: P2-3 A2 materialization-output provenance binding rework

## meta

- task_id: `20260911_0105_aiscc-p2-3-a2-materialization-output-provenance-binding-rework-1`
- created_at: `2026-09-11T01:05:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `IMPLEMENTATION_REWORK / PREPARED_OWNER_MODEL / STATIC_AND_POSTGRESQL_PROOF`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `876f232880e652fbf715f13c13b8cc03d27404f0`
- required_base_tree: `0f855b67fcad1be1cb4f635b6b4db8856c43da64`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. purpose

Continue the current 2355 owner-model candidate.

Close two items only:

```text
1. rerun the mandatory static/test evidence using quote-safe command transport
2. close MATERIALIZED_OUTPUT_PROVENANCE_BINDING_MISMATCH
```

Do not fix the separately pending S2 P1-6/P1-7 Judgment issue in this Task.

# 1. inbound transport

Verify Browser delivery ZIP exact filename/SHA-256 from the Short Prompt.

Place TASK first at:

```text
.aiassistant/tasks/active/20260911_0105_aiscc-p2-3-a2-materialization-output-provenance-binding-rework-1.md
```

Read fully.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260911_0105_aiscc-p2-3-a2-owner-model-static-failure-materialization-output-binding-rework-entry-1.cycle.md
SHA-256:
331d32681194e51fbf0a1c469c0b4e690f3800f5ebc25093bc4eff2b81406ccc

.aiassistant/reports/aiscc/20260911_0105_aiscc-p2-3-a2-owner-model-static-failure-materialization-output-binding-judgment-1.md
SHA-256:
83d9fdf0a23d1a0232cacb9645a3195b7e5a9eb8e1cc541fcf31b4d5d7cd933e
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

Expected Git-visible set excluding active Task is exact 30 paths:

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
- `src/aiscc/bootstrap.py`
- `src/aiscc/scenarios/stockroom_production.py`
- `config/evidence/stockroom-capture.v1.json`
- `config/human/stockroom-capture.v1.json`
- `config/judgment/stockroom-capture.v1.json`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`
- `src/aiscc/scenarios/driver.py`
- `src/aiscc/scenarios/composition.py`
- `tests/unit/scenarios/test_owner_composition.py`
- `tests/integration/scenarios/test_stockroom_binding.py`
- `.aiassistant/tasks/done/20260910_2355_aiscc-p2-3-a2-prepared-owner-model-reconciliation-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_2355_aiscc-p2-3-a2-prepared-owner-audit-accepted-model-reconciliation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_2355_aiscc-p2-3-a2-prepared-owner-contract-audit-final-acceptance-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_0105_aiscc-p2-3-a2-owner-model-static-failure-materialization-output-binding-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_0105_aiscc-p2-3-a2-owner-model-static-failure-materialization-output-binding-judgment-1.md`

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Ignored target/export residue is non-blocking.

No reset/restore/stash/broad cleanup.

# 3. exact predecessor/current candidate identity

Require exact 1738→2220 governance:

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

Require exact 2355 governance:

- `.aiassistant/tasks/done/20260910_2355_aiscc-p2-3-a2-prepared-owner-model-reconciliation-implementation-1.md`  `202c6952f9c404437cb72a2ed9bf4ecc920ea3ff653a659c64b356e47a4a4e29`
- `.aiassistant/records/aiscc/cycles/20260910_2355_aiscc-p2-3-a2-prepared-owner-audit-accepted-model-reconciliation-entry-1.cycle.md`  `b3ebb1ce4b9c59afcece0350f6ef51dd35b35f044e59da5ba938d920fb0b013c`
- `.aiassistant/reports/aiscc/20260910_2355_aiscc-p2-3-a2-prepared-owner-contract-audit-final-acceptance-judgment-1.md`  `a22f2962f82998c2b2808b057181f639699e9ccb368daee0bf2fbb3d5450d199`

Require exact current combined candidate:

- `src/aiscc/bootstrap.py`  `1718e596b20fd107af0cb80b6ad40e3626b7e26d8d45daa649ccf2d2ccf9fe38`
- `src/aiscc/scenarios/stockroom_production.py`  `e46edc42b3a830ca283d4398445fe5dadb8ffa8008d598ae7a81036e11f4d5d4`
- `config/evidence/stockroom-capture.v1.json`  `70d4dbf219d54abd57877b787d8ac16d0efbe05701e7fb8bf1f84282640b31e7`
- `config/human/stockroom-capture.v1.json`  `7ec43975b8d1f30ded987d05942753dadbd93197ad86da2701514a198e797bab`
- `config/judgment/stockroom-capture.v1.json`  `31f8d08c083218d1fcc47d5ba7a8d1c151a48bbf26ea3319ac9503a666179eef`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`  `3f9d1c5699c1d22987efc1980043c1d2f46f2414f8e0f9d91c997526f1e1cd73`
- `src/aiscc/scenarios/driver.py`  `137c73cba86f0d0e4e95bbd6629cd9aefbf5e7f5a177805ef6892eefb02e0644`
- `src/aiscc/scenarios/composition.py`  `2017a18175e0e227fe1514d3d9e85c7d0d64d391ec94649912d9749699b7edfc`
- `tests/unit/scenarios/test_owner_composition.py`  `68cf0561e482e1ded6f6bddaa8b91da1fea753b430527e27fe66bf7cf0cb4d12`
- `tests/integration/scenarios/test_stockroom_binding.py`  `063e2b65eb229b5849bc3df61294d72f3f656783ac1257a4dbcaa82bb2d70b34`

Mismatch:

```text
PREDECESSOR_OR_CANDIDATE_IDENTITY_MISMATCH
→ STOP
```

# 4. exact mutation allowlist

Only these three paths may change:

```text
MODIFY
src/aiscc/scenarios/driver.py

MODIFY
src/aiscc/scenarios/stockroom_production.py

MODIFY
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Freeze byte-exact:

```text
src/aiscc/bootstrap.py
1718e596b20fd107af0cb80b6ad40e3626b7e26d8d45daa649ccf2d2ccf9fe38

src/aiscc/scenarios/composition.py
2017a18175e0e227fe1514d3d9e85c7d0d64d391ec94649912d9749699b7edfc

tests/unit/scenarios/test_owner_composition.py
68cf0561e482e1ded6f6bddaa8b91da1fea753b430527e27fe66bf7cf0cb4d12

tests/integration/scenarios/test_stockroom_binding.py
063e2b65eb229b5849bc3df61294d72f3f656783ac1257a4dbcaa82bb2d70b34

config/evidence/stockroom-capture.v1.json
70d4dbf219d54abd57877b787d8ac16d0efbe05701e7fb8bf1f84282640b31e7

config/human/stockroom-capture.v1.json
7ec43975b8d1f30ded987d05942753dadbd93197ad86da2701514a198e797bab

config/judgment/stockroom-capture.v1.json
31f8d08c083218d1fcc47d5ba7a8d1c151a48bbf26ea3319ac9503a666179eef
```

Also frozen:

```text
src/aiscc/scenarios/capture_runner.py
tests/unit/scenarios/test_stockroom_capture_runner.py
src/aiscc/runtime/**
src/aiscc/providers/**
src/aiscc/security/**
src/aiscc/evidence/**
src/aiscc/judgment/**
all migrations
```

If another path is needed:

```text
SCOPE_EXPANSION_REQUIRED
→ STOP
```

# 5. preserve accepted owner-model improvements

Do not regress:

```text
seven stable owners are exact instance bindings

materializer_factory is the exact prepared factory object

agent_execution_service_factory is the exact prepared factory object

PreparedStockroomDriver carries immutable run/attempt/scenario/request/config binding

adapter obtains both late-bound owners through the exact prepared factories

no concrete placeholder materializer/execution service remains

security TTL native-clock fix retained

ToolOutputRef runtime-evidence binding retained

NETWORK remains denied
```

# 6. materialized-output authority gap

Current positive construction path must no longer accept:

```text
arbitrary MaterializedStockroom
+
valid but separately supplied StockroomMaterializerDerivation
```

as sufficient proof for execution-service derivation.

Add the smallest immutable materialization-result binding/derivation model.

Truthful naming is flexible, for example:

```text
StockroomMaterializedResultBinding
StockroomMaterializedDerivation
StockroomMaterializedOutputProvenance
```

The model must represent the causal chain:

```text
prepared binding
→ exact prepared materializer factory
→ exact derived StockroomMaterializer
→ that owner's materialize() return object
```

before the execution-service factory can consume it.

# 7. result-binding minimum identity

The immutable materialization-result provenance must include or cryptographically cover at least:

```text
prepared binding fingerprint
materializer factory ref/fingerprint
materializer derivation provenance fingerprint
run_id
attempt_id
resource_ref
source_commit
subroot
git_subtree
aggregate_sha256
workspace lease identity
resolved source-root fingerprint
materialized file manifest fingerprint
materialized-output fingerprint
```

Use canonical existing hashes/manifest semantics where available.

Do not invent a weaker duplicate source identity.

# 8. exact factory-controlled issuance

The result binding must be issued only through the exact prepared `materializer_factory` authority.

A valid implementation may:

```text
derive the exact StockroomMaterializer
call that exact derived owner's materialize()
immediately bind the returned MaterializedStockroom into an immutable result record
```

or an equivalent fail-closed design.

Requirements:

```text
prepared.owners.materializer_factory is exact issuing factory

materializer derivation belongs to that factory

prepared binding matches run/attempt/config

MaterializedStockroom returned object matches run/attempt/resource

result provenance references the exact materializer derivation

raw caller-created result cannot mint an equivalent accepted binding without the exact factory issuance path
```

Do not use private-field mutation of the materializer.

# 9. execution factory input contract

Change the execution-service factory so its positive derivation path consumes the immutable **bound materialization result**, not a freely supplied raw `MaterializedStockroom`.

It must verify:

```text
result binding issued from prepared materializer factory

prepared binding fingerprint exact

materializer derivation provenance exact

run/attempt exact

resource/source identity exact

workspace/materialized output identity exact

result not foreign/replaced
```

Only then may it create:

```text
DockerRunSpec
ToolRegistry
StockroomSummaryDispatcher
AgentExecutionService
```

and its execution-service derivation provenance.

The execution-service provenance must carry the materialized-output provenance ref/fingerprint, not merely the materializer-construction provenance.

# 10. actual adapter path

`StockroomCaptureOwnerAdapter.materialize()` must use the exact factory-controlled chain.

Expected semantic shape:

```text
prepared materializer factory
→ derive exact materializer
→ exact derived owner materialize()
→ factory-issued immutable materialized-result binding
→ prepared execution-service factory preparation/derive
→ _MaterializedRuntime retains both derivation chains
```

No direct independent execution-service factory input may be assembled from a caller-supplied raw materialized object.

`StockroomPreparedCapture.materializer` / `.agent_execution_service` may remain non-authoritative convenience refs only.

# 11. no-side-effect positive test technique

Do not use a freely constructed synthetic `MaterializedStockroom` as positive authority proof.

For the bounded test, it is allowed to monkeypatch the **exact derived `StockroomMaterializer.materialize` implementation** with a no-side-effect stub that:

```text
is invoked through the production factory/adapter chain
returns one bounded deterministic MaterializedStockroom
does not touch Git/filesystem/network/process
```

Then require the production factory to mint the materialized-result binding from that exact return object.

This stub is test instrumentation only and must be fail-closed outside the monkeypatched test.

The prior positive pattern:

```text
synthetic MaterializedStockroom constructed independently
→ execution_factory.prepare_inputs(...)
```

must be removed.

# 12. mandatory negative tests

Before any side effect, reject:

```text
raw independently fabricated MaterializedStockroom supplied directly to execution factory

materialized result from foreign materializer factory

result binding with foreign prepared binding

foreign run
foreign attempt
foreign resource_ref
altered source_commit/subroot/git_subtree/aggregate
altered file-manifest fingerprint
foreign workspace lease/destination
result/provenance fingerprint mismatch
materializer derivation from a different factory
execution factory from a different prepared owner bundle
```

No unrelated owner may be accepted because hashes happen to look valid.

# 13. factory Protocol/model check

Re-read the B3 factory authority Protocol/model after the above change.

Do not require B3 to import A2 concrete implementation types.

But ensure the prepared model still truthfully exposes:

```text
semantic role
factory ref/fingerprint
exact factory object identity
immutable prepared-attempt binding
derived-owner/result provenance types
```

If the current Protocol remains intentionally metadata-oriented, production must still fail closed by exact concrete factory type/identity before any side-effect path.

Do not weaken existing B3 inert preparation tests.

# 14. S2 remains frozen/pending

Do not change:

```text
src/aiscc/evidence/**
src/aiscc/judgment/**
```

Current known status remains:

```text
S2 negative evaluation Judgment binding:
ADAPTER_LOCAL_BINDING_ONLY
```

Do not create a fake positive attestation for UNSATISFIED evidence.

Do not claim A2 final acceptance.

# 15. quote-safe mandatory static gate

The 2355 mandatory static failure came from an inline PowerShell→Python quoting error.

Do not use an inline quoted Python program for the mandatory gate.

Use direct module/file commands.

For compile, use exact project Python with:

```text
-m py_compile
```

over the required files.

For strict config-loader verification, if a small custom Python driver is required, write it to a temporary file outside the repository (for example `%TEMP%`) and invoke that file by exact interpreter path. Delete the temporary verification file afterward.

Do not create a repo-visible helper script.

Mandatory static paths:

```text
src/aiscc/scenarios/driver.py
src/aiscc/scenarios/composition.py
src/aiscc/scenarios/stockroom_production.py
src/aiscc/scenarios/capture_runner.py
tests/unit/scenarios/test_owner_composition.py
tests/integration/scenarios/test_stockroom_binding.py
tests/integration/scenarios/test_stockroom_capture_runner.py
tests/unit/scenarios/test_stockroom_capture_runner.py
```

Run:

```text
compile:
all above PASS

Ruff:
all above PASS

strict config loaders:
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

No same-turn repair after this mandatory gate.

# 16. B3 owner-model tests

After static PASS:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider   tests/unit/scenarios/test_owner_composition.py   tests/integration/scenarios/test_stockroom_binding.py -ra
```

Require all PASS.

This reuses the 2355 modified but frozen B3 identity tests.

# 17. A1 runner regression

Run unchanged:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider   tests/unit/scenarios/test_stockroom_capture_runner.py -ra
```

Require all PASS.

# 18. PostgreSQL A2 integration

Use the same bounded disposable PostgreSQL prerequisite pattern already accepted in 2215.

No remote DB, no pull, no unrelated container cleanup.

Run Alembic to the existing head and then:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider   tests/integration/scenarios/test_stockroom_capture_runner.py -ra
```

Require:

```text
all collected tests executed
0 failed
0 errors
0 skipped
```

The module must prove:

```text
NONE -> READY -> RUNNING prefix
security prefix
exact prepared factories
factory-controlled materialized-result binding
raw synthetic materialized object rejected as authority
execution-service derivation consumes only bound result
ToolOutputRef binding retained
no real materialization/provider/tool/process side effect
```

# 19. direct-owner regressions

After A2 integration PASS, run exact accepted bounded set:

```text
tests/integration/workflow/test_postgres_kernel.py
tests/integration/evidence/test_postgres_evidence_admission.py
tests/integration/human/test_postgres_human_gate_judgment.py
tests/unit/security/test_stockroom_policy.py
```

Require executable tests PASS with zero DB-prerequisite skip.

# 20. runtime ceiling

Allowed:

```text
PostgreSQL/Alembic test prerequisite
WorkflowKernel NONE->READY->RUNNING
attempt creation
security evaluation
factory object construction
no-side-effect monkeypatched materializer return for provenance-chain proof
```

Forbidden actual side effects:

```text
real StockroomMaterializer.materialize filesystem work
Git source materialization
Docker/process
provider
tool dispatch
AgentExecutionService.execute
network
real secret resolution
full runner.run()
actual S1-S4
HumanResult
terminal scenario Judgment
Replay
Git add/commit/push
```

The no-side-effect materializer stub must not write files or allocate real Stockroom runtime content.

# 21. contract review

Require PASS:

```text
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
25 / 25 PASS
```

# 22. cleanup

If the Task creates a disposable PostgreSQL container, remove only that exact Task-owned container after evidence collection.

If a temporary verification script was created outside the repo, delete only that exact file.

No broad cleanup.

# 23. final workspace

Before Task lifecycle:

```text
existing Git-visible:
28

current Cycle/Judgment:
2

total excluding active Task:
30 exact

index:
empty
```

Only existing candidate paths are modified; no new source/test/config path is authorized.

Move active Task byte-identically to:

```text
.aiassistant/tasks/done/20260911_0105_aiscc-p2-3-a2-materialization-output-provenance-binding-rework-1.md
```

Final expected:

```text
31 exact Git-visible paths
index empty
```

No other path.

# 24. no Git persistence

Do not run:

```text
git add
git commit
git push
```

# 25. required export bundle

Folder:

```text
.aiassistant/reports/target/20260911_0105_aiscc-p2-3-a2-materialization-output-provenance-binding-rework-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
IMPLEMENTATION_MANIFEST.md
STATIC_TRANSPORT_VERIFICATION.md
PREPARED_OWNER_MODEL_VERIFICATION.md
MATERIALIZATION_OUTPUT_BINDING_VERIFICATION.md
FACTORY_AUTHORITY_VERIFICATION.md
OWNER_IDENTITY_MATRIX.md
DERIVATION_PROVENANCE_VERIFICATION.md
ANTI_SWAP_VERIFICATION.md
POSTGRESQL_INTEGRATION_VERIFICATION.md
REGRESSION_VERIFICATION.md
CONTRACT_REVIEW.md
```

Also include byte-preserving copies of:

```text
current Cycle
current Judgment
current done Task

src/aiscc/bootstrap.py
src/aiscc/scenarios/driver.py
src/aiscc/scenarios/composition.py
src/aiscc/scenarios/stockroom_production.py
config/evidence/stockroom-capture.v1.json
config/human/stockroom-capture.v1.json
config/judgment/stockroom-capture.v1.json
tests/unit/scenarios/test_owner_composition.py
tests/integration/scenarios/test_stockroom_binding.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Expected:

```text
15 root docs
13 canonical/source/config/test copies
28 members total
```

`EXPORT_MANIFEST.md` covers all 27 non-self entries with relative path, byte size, SHA-256.

Require:

```text
one top-level directory
28 exact members
CRC PASS
15/15 required roots
13/13 copies
manifest 27/27 exact
folder/archive byte equality
```

# 26. mandatory stop

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
SCOPE_EXPANSION_REQUIRED
STATIC_CHECK_FAILURE
POSTGRESQL_TEST_PREREQUISITE_MISSING
TEST_FAILURE
CONTRACT_MISMATCH
UNEXPECTED_WORKSPACE_DELTA
ZIP_EXPORT_FAILED
```

No same-turn repair after mandatory static/test failure.

# 27. success ceiling

Success:

```text
prepared-owner + materialized-output model:
RECONCILED_CANDIDATE / BROWSER_JUDGMENT_REQUIRED

A2 executable proof:
PASS

S2 Judgment binding:
STILL REWORK_REQUIRED / NEXT AUTHORITY TASK

A2 persistence:
NOT_AUTHORIZED

Stockroom runtime prerequisites:
NOT_VERIFIED

actual S1-S4:
NOT_STARTED
```
