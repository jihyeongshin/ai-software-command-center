# 작업지시서: P2-3 Phase 1B-B3 driver/composition/bootstrap implementation

## meta

- task_id: `20260909_2136_aiscc-p2-3-phase1b-b3-driver-composition-bootstrap-implementation-1`
- created_at: `2026-09-09T21:36:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `ORCHESTRATION_IMPLEMENTATION / APPLICATION_COMPOSITION_IMPLEMENTATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P2-3 Phase 1B-B3 owner-only driver/composition/bootstrap`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `40804edfa2dfce244965c59ec94a89c62bf83df5`
- required_base_tree: `1988fc71fc2dce05317eb62879b99c8a5f9dfb53`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `governance Git persistence → application composition/bootstrap/source/test mutation`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. inbound ZIP bootstrap

The Browser Short Prompt's exact delivery ZIP SHA-256 is the bootstrap integrity anchor.

Current delivery ZIP contains only:

```text
TASK:
20260909_2136_aiscc-p2-3-phase1b-b3-driver-composition-bootstrap-implementation-1.md

CYCLE:
20260909_2136_aiscc-p2-3-b2-state-reconciliation-accepted-b3-implementation-entry-1.cycle.md
SHA-256:
c50a03a48ff75de627b6f94ea93c67886cbdda2815ccfe56d3a21746fb5e156d
destination:
.aiassistant/records/aiscc/cycles/20260909_2136_aiscc-p2-3-b2-state-reconciliation-accepted-b3-implementation-entry-1.cycle.md

JUDGMENT:
20260909_2136_aiscc-p2-3-b2-state-reconciliation-final-acceptance-judgment-1.md
SHA-256:
bf4375c2e0b7661abaa502a9b3d21fa2bdb38e2dab5cbd6f58f9881e63b22461
destination:
.aiassistant/reports/aiscc/20260909_2136_aiscc-p2-3-b2-state-reconciliation-final-acceptance-judgment-1.md

HANDOFF:
none
```

Executor:

1. verify exact ZIP filename/SHA-256;
2. validate archive readability/CRC/member safety;
3. materialize TASK first to `.aiassistant/tasks/active/20260909_2136_aiscc-p2-3-phase1b-b3-driver-composition-bootstrap-implementation-1.md`;
4. read TASK;
5. materialize CYCLE/JUDGMENT directly to exact canonical destinations;
6. verify exact hashes.

Bootstrap failure before canonical TASK placement:

```text
STOP
no report/export
no substantive project mutation
ask Human to re-download/reposition ZIP
```

After exact canonical transport, inbound cleanup refusal is `NON_BLOCKING_LOCAL_RESIDUE`.

# 1. repository gate

After current artifact placement require:

```text
branch:
main

HEAD:
40804edfa2dfce244965c59ec94a89c62bf83df5

HEAD tree:
1988fc71fc2dce05317eb62879b99c8a5f9dfb53

index:
empty
```

Expected Git-visible set excluding current active Task:

```text
.aiassistant/records/aiscc/cycles/20260909_2136_aiscc-p2-3-b2-state-reconciliation-accepted-b3-implementation-entry-1.cycle.md
.aiassistant/reports/aiscc/20260909_2136_aiscc-p2-3-b2-state-reconciliation-final-acceptance-judgment-1.md
```

exact 2 paths.

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Do not cleanup/restore/stash/reset/absorb.

# 2. exact predecessor provenance

Verify exact committed 2018 artifacts:

- `.aiassistant/tasks/done/20260909_2018_aiscc-p2-3-phase1b-b2-terminal-state-b3-entry-reconciliation-1.md`  `b5e3ec8627ae267595915b241946f266830a017788adf71e8b77edb6b91b396e`
- `.aiassistant/records/aiscc/cycles/20260909_2018_aiscc-p2-3-b2-persisted-b3-entry-1.cycle.md`  `cc523c0971d8471af0bab65eee65be5cacc5f5661f46e74672eb5142030c51ee`
- `.aiassistant/reports/aiscc/20260909_2018_aiscc-p2-3-b2-persistence-final-acceptance-judgment-1.md`  `224434fb8c4deccdf456e63a91b87aca930648c4480d3ad98e187c42228e2a92`

Any mismatch:

```text
PREDECESSOR_PROVENANCE_IDENTITY_MISMATCH
→ STOP
```

# 3. must-read authority and source

Read fully:

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/AISCC_RUNTIME_SUBSTRATE.md
.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md
.aiassistant/rules/AISCC_SECURITY_SANDBOX.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/records/aiscc/cycles/20260909_2136_aiscc-p2-3-b2-state-reconciliation-accepted-b3-implementation-entry-1.cycle.md
.aiassistant/reports/aiscc/20260909_2136_aiscc-p2-3-b2-state-reconciliation-final-acceptance-judgment-1.md

.aiassistant/tasks/done/20260909_2018_aiscc-p2-3-phase1b-b2-terminal-state-b3-entry-reconciliation-1.md
.aiassistant/records/aiscc/cycles/20260909_2018_aiscc-p2-3-b2-persisted-b3-entry-1.cycle.md
.aiassistant/reports/aiscc/20260909_2018_aiscc-p2-3-b2-persistence-final-acceptance-judgment-1.md

.aiassistant/reports/aiscc/20260909_1329_aiscc-p2-3-phase1b-runtime-integration-audit-final-acceptance-judgment-1.md
.aiassistant/reports/aiscc/20260909_1435_aiscc-p2-3-phase1b-b1-final-acceptance-judgment-1.md
.aiassistant/reports/aiscc/20260909_1805_aiscc-p2-3-phase1b-b2-final-acceptance-judgment-1.md

src/aiscc/bootstrap.py

src/aiscc/scenarios/models.py
src/aiscc/scenarios/catalog.py
src/aiscc/scenarios/runtime_models.py
src/aiscc/scenarios/enrollment.py

src/aiscc/runtime/stockroom_workspace.py
src/aiscc/runtime/stockroom_materializer.py

src/aiscc/providers/local_deterministic.py
src/aiscc/providers/stockroom_tool.py
src/aiscc/providers/service.py
src/aiscc/providers/tools.py
src/aiscc/providers/ports.py

src/aiscc/security/stockroom_policy.py
src/aiscc/security/policy.py

src/aiscc/workflow/kernel.py
src/aiscc/workflow/models.py

src/aiscc/evidence/requirements.py
src/aiscc/evidence/models.py
src/aiscc/human/models.py
src/aiscc/judgment/models.py

config/scenarios/stockroom/v1/catalog.json
config/scenarios/stockroom/v1/resource.json
config/providers/stockroom-owner-profiles.v1.toml
config/providers/stockroom-tools.v1.toml
config/security/stockroom-owner.v1.toml
```

Read only direct additional collaborators required to match exact existing owner constructor/protocol signatures.

Do not bulk-read unrelated history or source trees.

If a required real owner contract is absent and cannot be represented within the five-path allowlist:

```text
MISSING_REAL_OWNER_CONTRACT / SCOPE_EXPANSION_REQUIRED
→ STOP
```

# 4. exact B3 mutation allowlist — 5

## CREATE — 4

- `src/aiscc/scenarios/driver.py`
- `src/aiscc/scenarios/composition.py`
- `tests/unit/scenarios/test_owner_composition.py`
- `tests/integration/scenarios/test_stockroom_binding.py`

## MODIFY — 1

```text
src/aiscc/bootstrap.py
```

Rules:

```text
all CREATE paths:
must be absent before mutation

bootstrap.py:
must be tracked and clean at base HEAD

additional product/config/test path:
forbidden
```

If any CREATE path already exists unexpectedly:

```text
UNEXPECTED_EXISTING_PATH
→ STOP
```

No B1/B2/config/state/rules modification.

# 5. fixed B3 authority boundary

B3 is **preparation/composition only**.

It may:

```text
load strict server-owned catalog/config
cross-check immutable identities
compile one of four exact scenario selections
build inert owner composition
build inert driver request/object
bind explicit existing owner dependencies
expose explicit owner-only root bootstrap factory
run unit/integration tests using never-call spies/fakes
```

It may NOT:

```text
create/mutate WorkRun
request workflow transition
call AgentExecutionService.execute
materialize repository workspace
call provider adapter
dispatch Stockroom tool
invoke Docker/container
open network/socket/HTTP/OpenAI
read/resolve real secret
write DB
admit evidence
open/resolve Human gate
create/admit HumanResult
create/admit Judgment
generate Replay
register public route
enable PUBLIC_BOUNDED_LIVE
```

No implicit execution may happen at import, config load, composition, driver construction or bootstrap construction.

# 6. fixed first-capture target remains descriptive only

Every B3 composition/request must preserve:

```text
RuntimeMode:
OWNER_SELF_DOGFOOD

resource_ref:
repository:synthetic-stockroom@be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d

provider_id:
aiscc-local-deterministic

execution_backend_kind:
LOCAL_DETERMINISTIC_PROVIDER

external_llm_executed:
false

tool:
stockroom_summary only where scenario allows it

network:
DENY / none

PUBLIC_BOUNDED_LIVE:
NOT_AUTHORIZED
```

B3 does not convert these descriptors into executed proof.

# 7. driver.py — inert runtime request and owner dependency boundary

Create:

```text
src/aiscc/scenarios/driver.py
```

Implement an immutable driver/request boundary consistent with current repository naming and the accepted Phase 1B design.

Required semantic chain:

```text
StockroomEnrollment
+ private StockroomOwnerContext
+ server-generated run/attempt/state binding descriptors
→
inert StockroomDriverRequest

StockroomDriverRequest
+ explicit existing durable/runtime owner dependencies
→
prepared Stockroom driver/composition object
```

The preparation function must be pure with respect to runtime state.

Required request bindings include at least:

```text
scenario_id / scenario_version
resource_ref
OWNER_SELF_DOGFOOD
provider profile ID/version
tool ID/action when applicable
external_llm_executed=false
run_id / attempt_id
expected initial workflow state/version descriptor
evidence/Human/Judgment descriptors from enrollment
finite owner/config fingerprint refs
```

Do not duplicate or redefine Phase 1A Scenario/TaskContract meaning.

Do not invent a new workflow state.

# 8. explicit real-owner dependency contract

The driver construction boundary must require explicit dependencies for the existing authoritative owners needed by later actual capture.

Use exact current repository types/protocols where available.

At minimum the construction must distinguish and require references equivalent to:

```text
WorkflowKernel / transition owner
AgentExecutionService / provider-tool execution owner
Evidence requirement/admission owner
Human gate owner
Judgment owner
Stockroom workspace/materializer owner/factory
Stockroom security/policy owner
```

Rules:

```text
missing required dependency:
fail closed before any execution

None / wrong type / ambiguous duck-typed substitute:
deny according to current type conventions

silent default in-memory production owner:
forbidden

constructing a DB-backed owner inside B3:
forbidden

constructing AgentExecutionService and calling execute:
forbidden
```

Tests may use explicit never-call typed fakes/spies that satisfy the dependency boundary.

Do not claim those spies are durable runtime acceptance.

# 9. no capture implementation in driver

B3 must NOT implement the scenario execution/capture algorithm.

Preferred ceiling:

```text
driver object contains immutable request + owner dependency bindings
and exposes no automatically invoked execution path.
```

If repository conventions require an explicit future execution method/port, it must:

```text
require a separately supplied future runtime authorization
perform nothing during B3 construction/tests
never be called in B3 verification
```

Do not implement transition/evidence/Judgment sequencing in B3 as if it were already executed.

# 10. composition.py — strict server-owned cross-binding

Create:

```text
src/aiscc/scenarios/composition.py
```

This module owns strict **owner-only composition**, not runtime execution.

Use existing strict loaders:

```text
load_catalog(...)
load_stockroom_owner_profiles(...)
load_stockroom_tool_config(...)
load_stockroom_owner_policy(...)
```

and existing B1/B2 types.

Server-owned paths only. No requester-provided config/catalog path.

Cross-bind exact identities before returning a composition object.

At minimum verify:

## catalog/resource

```text
four exact SCENARIO_IDS in canonical order
scenario_version = 1.0.0
resource_ref exact accepted value
catalog.document/resource identity agrees
```

## provider profile mapping

```text
four exact profile IDs/version 1
one exact scenario per profile
provider_id = aiscc-local-deterministic
adapter_protocol_version = stockroom-local-responses-v1
OWNER_SELF_DOGFOOD only
external_llm_executed = false
```

## tool mapping

```text
registry = aiscc-stockroom-tools / 1
tool = stockroom_summary / fixed-stockroom-summary
S1/S2/S4 tool allowed
S3 tool forbidden
empty model-visible args only
network none
fixed image/argv/workdir/bounds from strict B2 config
```

## security mapping

```text
stockroom-owner-v1
default DENY
OWNER_SELF_DOGFOOD only
four scenario/profile mappings match provider config
tool policy matches tool config
resource_ref exact
NETWORK denied
finite limits agree with B2 provider/tool/security maxima
```

Any cross-config mismatch:

```text
STOCKROOM_COMPOSITION_BINDING_DENIED
```

or a more precise stable fail-closed code.

No fallback to legacy/public provider/tool/security configuration.

# 11. composition output

Return an immutable owner-only composition/factory object containing only server-owned inert identities/factories required to prepare a run.

It may contain references/factories for:

```text
canonical ScenarioCatalog
StockroomOwnerContext
strict provider profiles
strict tool config/registry factory
strict Stockroom owner policy/restriction factory
B1 workspace/materializer factory reference
B3 request/driver factory
configuration fingerprints
```

It must NOT contain:

```text
live WorkRun
admitted capability
consumed capability receipt
materialized workspace
ToolOutputRef
ProviderResult
admitted Evidence
HumanResult
Judgment
Replay projection
```

# 12. configuration fingerprint and cross-binding

Create deterministic non-secret fingerprints for the composed server configuration using current canonical hashing utilities where available.

Fingerprint inputs must include exact:

```text
scenario catalog/resource identities
profile IDs/versions and local backend disclosure
tool registry/version/action/spec identity
security schema/version/scenario mappings/limits
OWNER_SELF_DOGFOOD mode
```

Do not include:

```text
raw secret/sentinel
host absolute path
requester input beyond scenario_id
mutable run output
```

The fingerprint is configuration provenance, not evidence admission.

# 13. bootstrap.py modification boundary

Modify only:

```text
src/aiscc/bootstrap.py
```

Add an explicit root-level owner-only preparation factory consistent with current bootstrap naming.

Semantics equivalent to:

```text
build_stockroom_owner_preparation(...)
```

or exact repository-style naming.

Required:

```text
explicit invocation only
server-owned config roots/paths
returns inert Stockroom owner composition/preparation factory
no DB construction
no Docker/provider/tool execution
no materialization
no route registration
no background task
no public mode enabling
```

Existing default bootstrap functions, especially default security construction, must preserve previous semantics.

Importing `aiscc.bootstrap` must remain inert.

No environment variable may silently enable Stockroom execution/public mode.

# 14. default/public separation

Tests must prove:

```text
existing default bootstrap behavior:
unchanged

PUBLIC_RECORDED_REPLAY:
unaffected

PUBLIC_BOUNDED_LIVE:
not enrolled / not enabled

owner Stockroom composition:
reachable only through explicit owner-only factory
```

Do not reuse the owner composition as a public factory.

Do not add URL/API/frontend route.

# 15. test file — owner composition

Create exactly:

```text
tests/unit/scenarios/test_owner_composition.py
```

Minimum proof:

```text
actual canonical catalog + three B2 strict configs load and cross-bind
four exact profile/scenario/resource mappings
S1/S2/S4 tool allowed; S3 denied
OWNER_SELF_DOGFOOD only
external_llm_executed=false exact
network denied
finite bound agreement
deterministic config fingerprint
composition object frozen/inert
unknown/missing/wrong-version/mismatched config denies
legacy/public config fallback denied
requester cannot supply catalog/config/provider/tool/security path
missing required owner dependency fails closed
default bootstrap remains semantically unchanged
explicit owner factory does not execute anything
```

Use temporary altered config copies only inside test-owned temporary directories for mismatch cases.

Do not modify canonical config.

# 16. integration test — no-side-effect Stockroom binding

Create exactly:

```text
tests/integration/scenarios/test_stockroom_binding.py
```

This is binding integration, not runtime execution.

Use:

```text
actual Phase 1A catalog/resource files
actual B2 owner provider/tool/security configs
actual B1/B2 production classes
explicit never-call spies/fakes for runtime owners
```

For all four exact scenario IDs prove:

```text
catalog selection
→ StockroomEnrollment
→ owner composition
→ inert StockroomDriverRequest
→ prepared driver dependency binding
```

and exact:

```text
scenario/version/resource
profile/version/provider
tool/no-tool branch
security owner/mode
external_llm_executed=false
evidence/Human/Judgment descriptors
finite config fingerprint
```

S4 must still show:

```text
Human requirement:
HUMAN_OWNED / HUMAN_P1_7 / pending

Agent claim:
not substituted as HumanResult
```

S2 must still show:

```text
missing evidence requirement remains required
same-run automatic retry = false
```

S3 must still show:

```text
tool absent/forbidden
policy-conflict static descriptor
```

# 17. mandatory zero-call integration spies

The integration test must inject/patch explicit never-call spies and prove invocation count remains zero for all executable/runtime boundaries available in current source.

At minimum:

```text
AgentExecutionService.execute
DockerRuntime.run / receipt-based Stockroom entry
LocalDeterministicProvider.call
StockroomSummaryDispatcher dispatch
StockroomMaterializer.materialize
WorkflowKernel.request_transition
Evidence admission submission
Human result/gate mutation owner
Judgment admission owner
DB/repository mutation boundary
network/socket/HTTP/OpenAI construction if present
```

If exact owner methods differ, map to the current real direct callable.

Construction/typing checks are allowed.
Invoking these operations is forbidden.

A missing spy target because the current owner contract does not expose an executable method is not itself a failure; document the exact mapped boundary.

# 18. existing bootstrap regression discovery

Because `src/aiscc/bootstrap.py` is modified, perform a bounded exact search for direct bootstrap unit tests.

Search only:

```text
tests/unit/**/test_bootstrap*.py
tests/** symbols importing current bootstrap build_* functions
```

If exactly one direct bootstrap regression module is identified, run it.

If none:

```text
NO_EXISTING_DIRECT_BOOTSTRAP_UNIT_MODULE
```

If multiple direct modules exist, run the bounded set only if all are clearly direct bootstrap regressions.

If ambiguity would require broad suite expansion:

```text
TEST_SCOPE_AMBIGUOUS
→ STOP
```

Do not run broad DB/Docker/provider integration suites.

# 19. required B3 test command

First run exactly the two new B3 modules:

```text
PYTHONDONTWRITEBYTECODE=1
.venv/Scripts/python.exe -B -m pytest -q -p no:cacheprovider tests/unit/scenarios/test_owner_composition.py tests/integration/scenarios/test_stockroom_binding.py -ra
```

Required:

```text
exit 0
failed 0
errors 0
```

If nonzero:

```text
TEST_FAILURE
→ STOP
```

No same-turn product/test repair after mandatory test failure.

# 20. required targeted dependency regressions

Only after section 19 PASS, run:

```text
.venv/Scripts/python.exe -B -m pytest -q -p no:cacheprovider   tests/unit/scenarios/test_runtime_enrollment.py   tests/unit/providers/test_stockroom_tool.py   tests/unit/providers/test_local_deterministic.py   tests/unit/security/test_stockroom_policy.py
```

Then run the bounded direct bootstrap regression module(s) from section 18 if any.

Any nonzero command:

```text
TEST_FAILURE
→ STOP
```

No same-turn repair.

Do not rerun B1 filesystem/materializer suites unless a direct B3 import/type contract failure requires exact browser reauthorization; B3 must not materialize.

# 21. static/source integrity

Require after successful tests:

```text
CREATE paths:
4 exact

MODIFY:
bootstrap.py only

other product/config/test changes:
0

B1 files:
unchanged

B2 product/config/test:
unchanged

Phase 1A config/scenario:
unchanged

dependency manifests:
unchanged

migration:
none

git diff --check:
PASS

index:
empty

Git-visible pyc/__pycache__/pytest cache:
none
```

Run Python compile/Ruff only on the five B3 paths and direct changed-import test scope using the existing environment.

No dependency installation/network/provisioning.

# 22. explicit persistence / runtime boundary

Report exactly:

```text
PHASE1B_B3_DB_MIGRATION:
NOT_REQUIRED

DEFAULT_STARTUP_EXECUTION:
ZERO

OWNER_PREPARATION_SIDE_EFFECTS:
ZERO

PUBLIC_MODE_ENROLLMENT:
NONE

ACTUAL_SCENARIO_EXECUTION:
NOT_RUN
```

If B3 implementation discovers that a DB schema change, startup execution, public route, or extra mutation is required:

```text
SCOPE_EXPANSION_REQUIRED
→ STOP
```

Do not absorb it.

# 23. expected final workspace

Before current Task lifecycle:

```text
pending governance:
2 exact current Cycle/Judgment

B3 product/test:
5 exact changed/created paths

Git-visible excluding active Task:
7 exact

index:
empty
```

Then move:

```text
.aiassistant/tasks/active/20260909_2136_aiscc-p2-3-phase1b-b3-driver-composition-bootstrap-implementation-1.md
→
.aiassistant/tasks/done/20260909_2136_aiscc-p2-3-phase1b-b3-driver-composition-bootstrap-implementation-1.md
```

Final:

```text
8 exact Git-visible paths
index empty
```

No Git add/commit.

# 24. evidence contract

executor_required:

- inbound ZIP/artifact transport
- repository gate
- exact 2018 predecessor identity
- exact five-path B3 implementation
- owner-only cross-config binding proof
- inert driver dependency proof
- explicit root bootstrap binding proof
- mandatory zero-side-effect integration proof
- targeted B2 dependency regressions
- bounded bootstrap regression result
- exact final workspace inventory
- outbound result ZIP

reuse_allowed:

- accepted Phase 1A static scenario/resource contracts
- persisted B1 materializer/workspace
- persisted B2 enrollment/tool/provider/security contracts
- accepted Phase 1B integration design

human_owned:

```text
new Human QA:
NOT_REQUIRED

public distribution/license:
HUMAN_PENDING / outside B3
```

not_required:

```text
actual scenario capture
real provider/tool/Docker execution
DB
Replay
Browser QA
deployment
```

forbidden proof substitution:

```text
composition binding
!=
runtime capability admission

never-call spy integration
!=
actual scenario run

driver object construction
!=
WorkRun execution

config fingerprint
!=
admitted evidence

external_llm_executed=false descriptor
!=
external LLM execution proof
```

# 25. explicit forbidden scope

Do NOT create/modify:

```text
src/aiscc/scenarios/runtime_models.py
src/aiscc/scenarios/enrollment.py
src/aiscc/runtime/stockroom_workspace.py
src/aiscc/runtime/stockroom_materializer.py

src/aiscc/providers/**
src/aiscc/security/**
src/aiscc/workflow/**
src/aiscc/evidence/**
src/aiscc/human/**
src/aiscc/judgment/**
src/aiscc/persistence/**

config/**
migrations/**
Replay/public/API/frontend/release code
dependency manifests
```

Only the exact five B3 paths are writable.

Do not execute:

```text
Docker
Stockroom CLI
provider network
DB
scenario runtime
Git add/commit/push
P2-4/P3
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
PREDECESSOR_PROVENANCE_IDENTITY_MISMATCH
MISSING_REQUIRED_ARTIFACT
UNEXPECTED_EXISTING_PATH
MISSING_REAL_OWNER_CONTRACT
SCOPE_EXPANSION_REQUIRED
DB_SCHEMA_REQUIRED
IMPLICIT_EXECUTION_REQUIRED
PUBLIC_ENABLEMENT_REQUIRED
TEST_SCOPE_AMBIGUOUS
BLOCKED_RUNTIME_PREREQUISITE
TEST_FAILURE
CONTRACT_MISMATCH
UNEXPECTED_WORKSPACE_DELTA
ZIP_EXPORT_FAILED
```

Inbound cleanup refusal after canonical transport is non-blocking.

# 27. export bundle + outbound ZIP

Bundle folder:

```text
.aiassistant/reports/target/20260909_2136_aiscc-p2-3-phase1b-b3-driver-composition-bootstrap-implementation-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
IMPLEMENTATION_MANIFEST.md
DRIVER_CONTRACT_VERIFICATION.md
COMPOSITION_CONTRACT_VERIFICATION.md
BOOTSTRAP_BINDING_VERIFICATION.md
NO_SIDE_EFFECT_INTEGRATION_VERIFICATION.md
TEST_VERIFICATION.md
```

Include byte-preserving project-relative copies of:

```text
current Cycle
current Judgment
current done Task
all five B3 product/test paths
```

After folder completion automatically create:

```text
.aiassistant/reports/target/20260909_2136_aiscc-p2-3-phase1b-b3-driver-composition-bootstrap-implementation-1.zip
```

Require:

```text
one top-level bundle directory
readable archive
CRC PASS
required root files present
manifest coverage
folder/archive filename equality
folder/archive byte equality
```

Keep folder and outbound ZIP.

# 28. Task lifecycle

After implementation/test/report/export completes:

```text
.aiassistant/tasks/active/20260909_2136_aiscc-p2-3-phase1b-b3-driver-composition-bootstrap-implementation-1.md
→
.aiassistant/tasks/done/20260909_2136_aiscc-p2-3-phase1b-b3-driver-composition-bootstrap-implementation-1.md
```

Do not stage or commit.

# 29. final ceiling

Success:

```text
P2-3 Phase 1B-B3:
READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT

P2-3 Phase 1B:
NOT_CLOSED_YET

actual scenario capture:
NOT_STARTED

Replay:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

Do not start actual runtime/capture work.
