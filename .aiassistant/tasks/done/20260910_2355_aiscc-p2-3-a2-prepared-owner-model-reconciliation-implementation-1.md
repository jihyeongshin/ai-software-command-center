# 작업지시서: P2-3 A2 prepared-owner model reconciliation implementation

## meta

- task_id: `20260910_2355_aiscc-p2-3-a2-prepared-owner-model-reconciliation-implementation-1`
- created_at: `2026-09-10T23:55:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `IMPLEMENTATION_REWORK / ACCEPTED_B3_OWNER_MODEL / A2_PRODUCTION_COMPOSITION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `876f232880e652fbf715f13c13b8cc03d27404f0`
- required_base_tree: `0f855b67fcad1be1cb4f635b6b4db8856c43da64`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `read-only prepared-owner audit → accepted B3 preparation model + A2 production composition rework`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. fresh-session Python discipline

Do not assume bare:

```text
python
python3
py
```

is valid on PATH.

Do not run bare `python` as a probe.

Known interpreter candidate:

```text
C:\Users\oracl\AppData\Roaming\uv\python\cpython-3.12.14-windows-x86_64-none\python.exe
```

For repository imports/tests, verify and use exact:

```text
.venv\Scripts\python.exe
```

Use exact executable paths only.

# 1. inbound transport

Verify Browser delivery ZIP exact filename/SHA-256 from the Short Prompt.

Place TASK first at:

```text
.aiassistant/tasks/active/20260910_2355_aiscc-p2-3-a2-prepared-owner-model-reconciliation-implementation-1.md
```

Read fully.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260910_2355_aiscc-p2-3-a2-prepared-owner-audit-accepted-model-reconciliation-entry-1.cycle.md
SHA-256:
b3ebb1ce4b9c59afcece0350f6ef51dd35b35f044e59da5ba938d920fb0b013c

.aiassistant/reports/aiscc/20260910_2355_aiscc-p2-3-a2-prepared-owner-contract-audit-final-acceptance-judgment-1.md
SHA-256:
a22f2962f82998c2b2808b057181f639699e9ccb368daee0bf2fbb3d5450d199
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

Expected Git-visible set excluding active Task is exact 23 paths:

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
- `.aiassistant/records/aiscc/cycles/20260910_2355_aiscc-p2-3-a2-prepared-owner-audit-accepted-model-reconciliation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_2355_aiscc-p2-3-a2-prepared-owner-contract-audit-final-acceptance-judgment-1.md`

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Ignored target/export residue is non-blocking.

No reset/restore/stash/broad cleanup.

# 3. exact predecessor and candidate identity

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

Require exact current A2 candidate:

- `src/aiscc/bootstrap.py`  `1718e596b20fd107af0cb80b6ad40e3626b7e26d8d45daa649ccf2d2ccf9fe38`
- `src/aiscc/scenarios/stockroom_production.py`  `03e3f68709b04304f1bb1e33932b97da0df6ccedfad644d62eb545fe71c9ef96`
- `config/evidence/stockroom-capture.v1.json`  `70d4dbf219d54abd57877b787d8ac16d0efbe05701e7fb8bf1f84282640b31e7`
- `config/human/stockroom-capture.v1.json`  `7ec43975b8d1f30ded987d05942753dadbd93197ad86da2701514a198e797bab`
- `config/judgment/stockroom-capture.v1.json`  `31f8d08c083218d1fcc47d5ba7a8d1c151a48bbf26ea3319ac9503a666179eef`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`  `938894d04935cfa0430fdf904524166073e016afb1e37b20075e0a8b94c4d24a`

Require exact committed B3/A1 neighbors before mutation:

- `src/aiscc/scenarios/driver.py`  `9871847ec0a236ef61c91518ff95764f3c2138e3854c25a4c8cab4f028503ce6`
- `src/aiscc/scenarios/composition.py`  `051f89bdceadeb1d08176e9ce0e2ed0ac3d9d14bddb6cd33657420853e50857c`
- `tests/unit/scenarios/test_owner_composition.py`  `2ccf94c635ecd530d784531dda8d47120a226c12aaab5da5319d9249baa8b024`
- `tests/integration/scenarios/test_stockroom_binding.py`  `f1a4fb8b2239dc70982fe4d16701340c14f420c136ae87abee6def331cf9f7bb`
- `src/aiscc/scenarios/capture_runner.py`  `600de0a4b0e718f02ab2e1907b7be62b2c4a23756559fdf99cb4cd55fb80b3d2`
- `tests/unit/scenarios/test_stockroom_capture_runner.py`  `a137021608ac9cb5b4c328b6bb88fd0c22cb0d9afd9b1a22054ec5bdd32f68ff`

Mismatch:

```text
PREDECESSOR_OR_CANDIDATE_IDENTITY_MISMATCH
→ STOP
```

# 4. exact mutation allowlist

Only these six paths may change:

```text
MODIFY
src/aiscc/scenarios/driver.py

MODIFY
src/aiscc/scenarios/composition.py

MODIFY
src/aiscc/scenarios/stockroom_production.py

MODIFY
tests/unit/scenarios/test_owner_composition.py

MODIFY
tests/integration/scenarios/test_stockroom_binding.py

MODIFY
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Frozen:

```text
src/aiscc/bootstrap.py
src/aiscc/scenarios/capture_runner.py
tests/unit/scenarios/test_stockroom_capture_runner.py

config/evidence/stockroom-capture.v1.json
config/human/stockroom-capture.v1.json
config/judgment/stockroom-capture.v1.json

src/aiscc/evidence/**
src/aiscc/judgment/**
src/aiscc/security/**
src/aiscc/providers/**
src/aiscc/runtime/**
all migrations
```

If another path is required:

```text
SCOPE_EXPANSION_REQUIRED
→ STOP
```

# 5. preserve the accepted semantic owner boundary

The prepared model remains an authority/provenance contract, not decoration.

Keep exact concrete instance binding for stable owners:

```text
workflow_kernel
evidence_admission_service
human_gate_owner
judgment_owner
workspace_owner
security_policy
stockroom_owner_restriction
```

Do not weaken these to type-only bindings.

Replace the two impossible concrete placeholder fields:

```text
agent_execution_service
materializer
```

with explicit late-bound factory/derivation authorities.

Use truthful names equivalent to:

```text
agent_execution_service_factory
materializer_factory
```

Do not retain fake/partial concrete owner placeholders merely to satisfy old type checks.

# 6. factory authority interface

Define the smallest explicit factory authority contract in the accepted B3 preparation layer.

The interface/model must make these facts inspectable:

```text
factory semantic role
immutable factory identity/ref
attempt-binding identity/fingerprint
derived-owner provenance
```

Concrete production factory implementation remains in:

```text
src/aiscc/scenarios/stockroom_production.py
```

Do not create a new source file.

The driver/composition layer may define Protocol/ABC/frozen binding value types as needed, but the exact factory object supplied by production must be preserved by object identity through preparation.

Do not use private attribute mutation as late binding.

# 7. immutable prepared attempt binding

The prepared model must contain one immutable binding that at minimum carries:

```text
run_id
attempt_id
scenario_id
request fingerprint
run-binding fingerprint
composition/config fingerprint
```

Use canonical fingerprints already available in the request/config/source model.

Do not invent a weaker duplicate fingerprint where an accepted canonical fingerprint already exists.

The binding must be created/sealed during B3 owner preparation, before runtime side effects.

`prepare_stockroom_driver` and/or `StockroomOwnerPreparation.prepare` must preserve exact owner/factory object identity and this immutable binding.

# 8. B3 identity contract

Update B3 preparation tests so the canonical meaning remains stronger than type compatibility.

Require assertions equivalent to:

```text
prepared.owners is supplied_owners

all seven stable prepared owner fields:
is exact supplied production owner object

prepared materializer factory:
is exact supplied factory object

prepared execution-service factory:
is exact supplied factory object

prepared attempt binding:
immutable
exact run/attempt/scenario/config/request identity
```

No copy-and-replace owner bundle may silently change identity.

# 9. production factory construction

At A2 application composition:

```text
construct one MaterializerFactory authority
construct one AgentExecutionServiceFactory authority
bind those exact objects into StockroomOwnerDependencies
prepare the driver with those exact objects
```

The adapter must obtain late-bound owner authority from the immutable prepared binding.

It must not use a parallel application-side factory instance or instantiate replacement owners directly outside the bound factory authority.

# 10. Materializer factory semantics

Current `StockroomMaterializer` exact instance cannot be safely configured before the authentic attempt `MaterializationAuthority` exists.

The factory is therefore the prepared authority.

Its derive/create operation must require:

```text
the exact prepared attempt binding
authentic current MaterializationAuthority
exact repository root
exact private runtime root
exact current run/attempt
current security refs/context
current operation fingerprint
```

Before construction verify those values against the prepared binding/current authority.

Then create a `StockroomMaterializer` whose `registered_authorities` contains the authentic exact authority.

Return an immutable derivation record/provenance object containing at least:

```text
factory identity/ref
prepared binding fingerprint
run/attempt
derived owner kind
materialization authority ref/fingerprint
relevant root/spec fingerprints
```

Do not call `.materialize()` merely to prove factory derivation in unit/static tests.

# 11. AgentExecutionService factory semantics

The execution-service factory is the prepared authority for late construction after materialization.

Require authentic current:

```text
prepared attempt binding
MaterializedStockroom/workspace identity
DockerRunSpec
ToolRegistry
StockroomSummaryDispatcher
execution reference authority
security/current-binding context factories
```

Verify request/config/run/attempt/spec fingerprints against the immutable prepared binding and materialized runtime provenance.

Then construct the fully configured `AgentExecutionService`.

Return an immutable derivation record containing:

```text
factory identity/ref
prepared binding fingerprint
run/attempt
derived owner kind
DockerRunSpec fingerprint
registry/dispatcher identity/fingerprint
materialization provenance ref/fingerprint
```

Do not execute provider/tool/process in this Task.

# 12. adapter consumption invariant

The production `StockroomCaptureOwnerAdapter` must consume the exact factories from the prepared binding.

Before materialization/execution, require identity/provenance checks proving:

```text
adapter prepared driver:
same immutable prepared driver/binding

factory used:
is prepared.owners.<factory>

derived owner:
was produced by that exact factory

derived provenance:
matches request/config/run/attempt/current runtime refs
```

No direct `StockroomMaterializer(...)` or `AgentExecutionService(...)` construction may remain on the operation path outside the prepared factory authority.

If helper methods remain, they must delegate to the exact bound factories rather than create independent authority.

# 13. mutable convenience fields

`StockroomPreparedCapture.materializer` and `.agent_execution_service` may remain only as non-authoritative convenience/cache fields if needed.

If retained:

```text
they must reference the owner derived by the exact prepared factory
they must not supersede PreparedStockroomDriver authority
they must not permit replacement by an unrelated owner
```

Prefer an immutable runtime derivation record over mutable authority replacement.

# 14. derived-owner anti-swap tests

Add regression coverage that rejects before side effects:

```text
different materializer factory object
different execution-service factory object
foreign prepared binding
foreign run
foreign attempt
altered request fingerprint
altered configuration/composition fingerprint
foreign MaterializationAuthority
mismatched repository/runtime root
foreign/mismatched DockerRunSpec
unrelated ToolRegistry/dispatcher
```

Do not require real materialization/provider/tool/process execution for these negative tests.

# 15. preserve existing A2 candidate corrections

The rework must preserve:

```text
SecurityPolicy native TTL clock-domain correction

historical application clock regression pressure

runtime summary evidence requires authentic same-attempt ToolOutputRef

ToolOutputRef hash == canonical_sha256(STOCKROOM_SUMMARY)

AgentOutputRef does not substitute for runtime-result provenance

NETWORK remains denied
```

No regression is permitted.

# 16. S2 is deliberately not fixed here

Do not modify P1-6/P1-7 source in this Task.

Preserve current S2 behavior as a known blocker:

```text
S2 current result:
ADAPTER_LOCAL_BINDING_ONLY
```

Do not create a fake positive evidence attestation for UNSATISFIED evaluation.

Do not claim A2 final acceptance after this Task.

A separate successor Task will bind the authentic durable P1-6 negative evaluation into P1-7 Judgment authority.

# 17. migration gate

No migration is expected or authorized.

Verify static migration head remains compatible:

```text
20260901_0008
```

If this owner-model change requires schema migration:

```text
MIGRATION_SCOPE_REQUIRED
→ STOP
```

# 18. full static gate

Run exact static checks on all six changed paths plus frozen A1/A2 boundary paths as relevant.

At minimum:

```text
compile:
driver.py
composition.py
stockroom_production.py
capture_runner.py
test_owner_composition.py
test_stockroom_binding.py
test_stockroom_capture_runner.py

Ruff:
same Python path set

strict JSON:
all three frozen A2 configs

git diff --check
index empty
```

Require all PASS.

Mandatory failure:

```text
STATIC_CHECK_FAILURE
→ STOP
```

No same-turn second repair after the mandatory static gate.

# 19. unit/B3 preparation proof

Run:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider   tests/unit/scenarios/test_owner_composition.py   tests/integration/scenarios/test_stockroom_binding.py -ra
```

Require all PASS.

These tests must include exact stable-owner identity, exact factory identity, immutable attempt binding, and anti-swap coverage.

# 20. A1 runner regression

Run unchanged:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider   tests/unit/scenarios/test_stockroom_capture_runner.py -ra
```

Require all PASS.

A1 operation order/status/state-version semantics remain unchanged.

# 21. bounded A2 PostgreSQL integration

Use the same repository-supported disposable PostgreSQL prerequisite pattern used by 2215.

No external pull/network.

If no local supported PostgreSQL prerequisite can be provided under existing Task-owned authority:

```text
POSTGRESQL_TEST_PREREQUISITE_MISSING
→ STOP
```

Run:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider   tests/integration/scenarios/test_stockroom_capture_runner.py -ra
```

Require all tests execute and PASS with zero skip.

The module must prove:

```text
real NONE -> READY
real create_attempt
real READY -> RUNNING
security prefix PASS
prepared stable owners are exact
prepared factory objects are exact
adapter uses those exact factories
factory derivation provenance binds run/attempt/config/request
ToolOutputRef runtime-evidence binding retained
no actual materializer/provider/tool/process execution
```

S2 Judgment final authority binding is excluded from acceptance and may remain a separately marked x-not-executed test only if it is not represented as PASS/skip. Prefer no test pretending that blocker is closed.

# 22. bounded direct-owner regressions

After A2 integration PASS, rerun the exact previously accepted direct-owner set:

```text
tests/integration/workflow/test_postgres_kernel.py
tests/integration/evidence/test_postgres_evidence_admission.py
tests/integration/human/test_postgres_human_gate_judgment.py
tests/unit/security/test_stockroom_policy.py
```

Require all executable tests PASS and zero DB-prerequisite skips.

Do not run whole repository suite.

# 23. zero-side-effect ceiling

Allowed:

```text
unit/static factory construction
PostgreSQL/Alembic integration
WorkflowKernel NONE->READY->RUNNING
attempt creation
security grant evaluation
config lookup
late-bound owner object construction without executing side effects
```

Forbidden:

```text
Stockroom materialize()
Docker/process execution
provider call
tool dispatch
AgentExecutionService.execute
network
real secret resolution
full runner.run()
actual S1-S4
HumanResult
terminal scenario Judgment
capture corpus
Replay
Git add/commit/push
```

# 24. contract review

Require PASS:

```text
PREPARED_OWNER_EXACT_BINDING_PRESERVED
SEVEN_STABLE_OWNER_IDENTITIES_EXACT
NO_PLACEHOLDER_MATERIALIZER
NO_PLACEHOLDER_EXECUTION_SERVICE
MATERIALIZER_FACTORY_EXACTLY_BOUND
EXECUTION_FACTORY_EXACTLY_BOUND
PREPARED_ATTEMPT_BINDING_IMMUTABLE
RUN_ATTEMPT_REQUEST_CONFIG_BOUND
ADAPTER_CONSUMES_PREPARED_FACTORIES
NO_PARALLEL_FACTORY_AUTHORITY
DERIVED_MATERIALIZER_PROVENANCE_BOUND
DERIVED_EXECUTION_SERVICE_PROVENANCE_BOUND
ANTI_OWNER_SWAP_FAIL_CLOSED
NO_PRIVATE_LATE_BINDING_MUTATION
B1_MATERIALIZER_AUTHORITY_PRESERVED
P1_5_EXECUTION_AUTHORITY_PRESERVED
A1_RUNNER_SEMANTICS_UNCHANGED
SECURITY_CLOCK_FIX_RETAINED
TOOL_OUTPUT_RUNTIME_EVIDENCE_BINDING_RETAINED
NETWORK_DENIED
NO_RUNTIME_SIDE_EFFECT
S2_BINDING_STILL_EXPLICITLY_PENDING
```

Require:

```text
22 / 22 PASS
```

# 25. cleanup

If this Task creates a disposable PostgreSQL container, remove only that exact Task-owned container after evidence collection.

No broad Docker cleanup.

# 26. final workspace

Before current Task lifecycle:

```text
existing pending paths:
21

current Cycle/Judgment:
2

total excluding active Task:
23 exact

index:
empty
```

The six mutation paths may change bytes but do not add extra paths except the four previously committed B3/test paths becoming Git-visible; therefore final path count must be computed from actual Git status, not by simply adding six.

Expected final Git-visible set is:

```text
all 18 previously pending governance/candidate paths
2220 Task/Cycle/Judgment
current Cycle/Judgment
current done Task
newly modified committed B3/test paths:
  src/aiscc/scenarios/driver.py
  src/aiscc/scenarios/composition.py
  tests/unit/scenarios/test_owner_composition.py
  tests/integration/scenarios/test_stockroom_binding.py
```

`stockroom_production.py` and the A2 integration test are already pending paths, so they remain one path each.

Expected final unique Git-visible path count:

```text
28
```

Require:

```text
index empty
extra 0
missing 0
```

# 27. no Git persistence

Do not run:

```text
git add
git commit
git push
```

Persistence remains a later Browser judgment.

# 28. required export bundle

Folder:

```text
.aiassistant/reports/target/20260910_2355_aiscc-p2-3-a2-prepared-owner-model-reconciliation-implementation-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
IMPLEMENTATION_MANIFEST.md
PREPARED_OWNER_MODEL_VERIFICATION.md
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

all six mutation paths
```

Expected:

```text
13 root docs
9 canonical/source/test copies
22 members total
```

`EXPORT_MANIFEST.md` covers all 21 non-self entries with relative path, size, SHA-256.

Create adjacent verified ZIP.

Require:

```text
one top-level directory
22 exact members
CRC PASS
13/13 roots
9/9 copies
manifest 21/21
folder/archive byte equality
```

# 29. mandatory stop

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
MIGRATION_SCOPE_REQUIRED
STATIC_CHECK_FAILURE
POSTGRESQL_TEST_PREREQUISITE_MISSING
TEST_FAILURE
CONTRACT_MISMATCH
UNEXPECTED_WORKSPACE_DELTA
ZIP_EXPORT_FAILED
```

No same-turn repair after a mandatory static/test failure.

# 30. success ceiling

Success:

```text
prepared-owner model:
RECONCILED_CANDIDATE / BROWSER_JUDGMENT_REQUIRED

A2 production composition:
OWNER_BINDING_RECONCILED_CANDIDATE

A2 executable regression:
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
