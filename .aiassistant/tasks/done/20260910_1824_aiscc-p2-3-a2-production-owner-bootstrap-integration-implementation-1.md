# 작업지시서: P2-3 A2 production owner/bootstrap integration implementation

## meta

- task_id: `20260910_1824_aiscc-p2-3-a2-production-owner-bootstrap-integration-implementation-1`
- created_at: `2026-09-10T18:24:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `IMPLEMENTATION / CONFIG_ENROLLMENT / POSTGRESQL_INTEGRATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `876f232880e652fbf715f13c13b8cc03d27404f0`
- required_base_tree: `0f855b67fcad1be1cb4f635b6b4db8856c43da64`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `A2 static feasibility audit → source/config/test implementation + PostgreSQL integration`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. fresh-session Python rule

Do not assume:

```text
python
python3
py
```

is valid on PATH.

Do not run bare `python` as an interpreter probe.

Known interpreter candidate:

```text
C:\Users\oracl\AppData\Roaming\uv\python\cpython-3.12.14-windows-x86_64-none\python.exe
```

Verify and use it by exact path for transport/hash work when valid.

For repository imports/tests use the exact project environment:

```text
.venv\Scripts\python.exe
```

after verifying it exists and executes.

If one candidate is unavailable, discover an actually executable interpreter instead of immediately failing.

# 1. inbound transport

Verify Browser delivery ZIP exact filename/SHA-256 from the Short Prompt.

Place TASK first at:

```text
.aiassistant/tasks/active/20260910_1824_aiscc-p2-3-a2-production-owner-bootstrap-integration-implementation-1.md
```

Read it fully.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260910_1824_aiscc-p2-3-a2-feasibility-accepted-production-integration-entry-1.cycle.md
SHA-256:
a02818022b2c694ad2644c2222e127de87c38f360b65fc33937c42af2cdb9846

.aiassistant/reports/aiscc/20260910_1824_aiscc-p2-3-a2-feasibility-audit-final-acceptance-judgment-1.md
SHA-256:
743103b7e8e22c7833bd555ff8ceedd0e0f34e0ab4994f077006864fbf172a85
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

Expected Git-visible set excluding active Task is exact 5 paths:

- `.aiassistant/tasks/done/20260910_1738_aiscc-p2-3-a2-production-owner-bootstrap-integration-feasibility-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1738_aiscc-p2-3-a1-terminal-persisted-a2-feasibility-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1738_aiscc-p2-3-a1-terminal-state-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1824_aiscc-p2-3-a2-feasibility-accepted-production-integration-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1824_aiscc-p2-3-a2-feasibility-audit-final-acceptance-judgment-1.md`

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Ignored target/export residue may remain non-blocking.

No cleanup/reset/restore/stash.

# 3. exact predecessor/A1 identity

Require exact 1738 provenance:

- `.aiassistant/tasks/done/20260910_1738_aiscc-p2-3-a2-production-owner-bootstrap-integration-feasibility-audit-1.md`  `c8f6615b9ce5943e1bee43046d50dd2dac4efba99a96179043177530f3a96ce4`
- `.aiassistant/records/aiscc/cycles/20260910_1738_aiscc-p2-3-a1-terminal-persisted-a2-feasibility-entry-1.cycle.md`  `0e6b3a12767fc3d5830726e1327d8e0d6f097271aa7aedd4157a4b86a566a782`
- `.aiassistant/reports/aiscc/20260910_1738_aiscc-p2-3-a1-terminal-state-persistence-final-acceptance-judgment-1.md`  `4df00fc71ff6603cb0703077c10c5460d3db2bdb6ec772a2b3fbd8b5983ed476`

Require exact accepted A1 committed source/test:

- `src/aiscc/scenarios/capture_runner.py`  `600de0a4b0e718f02ab2e1907b7be62b2c4a23756559fdf99cb4cd55fb80b3d2`
- `src/aiscc/scenarios/driver.py`  `9871847ec0a236ef61c91518ff95764f3c2138e3854c25a4c8cab4f028503ce6`
- `tests/unit/scenarios/test_stockroom_capture_runner.py`  `a137021608ac9cb5b4c328b6bb88fd0c22cb0d9afd9b1a22054ec5bdd32f68ff`

Mismatch:

```text
PREDECESSOR_OR_A1_IDENTITY_MISMATCH
→ STOP
```

# 4. migration pre-mutation gate

Before modifying source/config/test, inspect repository migration authority.

Run the repository-supported static migration-head command or exact Alembic equivalent using `.venv\Scripts\python.exe`.

Expected current head:

```text
20260901_0008
```

Audit current persistence models required by:

```text
WorkRun / transitions
P1-5 execution attempt/operation/output refs
P1-6 evidence/durable content/checkpoints
P1-7 Human reservation/gate/result
P1-7 Judgment
```

If current models/config implementation requires a schema delta not represented by the existing migration head:

```text
MIGRATION_SCOPE_REQUIRED
→ STOP
```

Do not create a migration in this Task.

If the repository static head differs from `20260901_0008` due to already-persisted unrelated canonical evolution, do not fail solely on the literal number. Reconcile that head to current HEAD and prove the required A2 schema is already present. If ambiguous, STOP.

# 5. exact mutation allowlist

Only these six paths may change:

- `MODIFY` `src/aiscc/bootstrap.py`
- `CREATE` `src/aiscc/scenarios/stockroom_production.py`
- `CONFIG_CREATE` `config/evidence/stockroom-capture.v1.json`
- `CONFIG_CREATE` `config/human/stockroom-capture.v1.json`
- `CONFIG_CREATE` `config/judgment/stockroom-capture.v1.json`
- `TEST_CREATE` `tests/integration/scenarios/test_stockroom_capture_runner.py`

No wildcard expansion.

Exact no-change neighbors:

```text
src/aiscc/scenarios/capture_runner.py
src/aiscc/scenarios/driver.py
src/aiscc/scenarios/composition.py
src/aiscc/scenarios/enrollment.py
```

Do not create:

```text
src/aiscc/evidence/authority.py
```

If another source/config/test/migration path is needed:

```text
SCOPE_EXPANSION_REQUIRED
→ STOP
```

# 6. bootstrap public construction

Modify:

```text
src/aiscc/bootstrap.py
```

only to expose a thin public Stockroom production-construction entrypoint and to ensure the Stockroom security policy is composed with all mandatory policy owners.

The public bootstrap must not become the implementation bucket.

Implementation detail belongs in:

```text
src/aiscc/scenarios/stockroom_production.py
```

No global singleton/service locator.

No PATH search for Git/Docker.

No implicit subprocess runner.

No credential discovery.

Operator/caller must explicitly supply environment-owned dependencies such as:

```text
async session factory
repository root
private runtime root
Downloads exclusion
trusted Git executable
explicit Docker process-runner dependency
project/requester identity
Human selector fingerprint/input
optional clocks
```

Do not persist a real Human identity or selector fingerprint into versioned config.

# 7. production graph

In `stockroom_production.py`, construct the smallest application-scoped graph using current owners.

Required owner families:

```text
PostgresExecutionRepository

P1-6:
TaskContractEvidenceAuthority
durable content authority/registry
issuer registry
EvidenceAdmissionEvaluator
PostgresEvidenceRepository
EvidenceAdmissionService
EvidenceSetEvaluator
checkpoint/use registry
EvidenceGuardAuthority

P1-7 Human:
PostgresHumanAuthorityRepository
HumanGateReservationAuthority
HumanGuardAuthority

P1-7 Judgment:
JudgmentPolicyAuthority
CommandCenterAuthority
PostgresJudgmentAuthority

P1-4:
P1_4GuardAuthority
TransitionEvaluator
PostgresTransitionRepository
WorkflowKernel

security/runtime/provider:
StockroomOwnerRestriction
ProviderToolResourceAuthority
SecretUseAuthority
SecurityPolicy
secret lease/resolver authority
ExecutionReferenceAuthority
LocalDeterministicProvider
StockroomWorkspace
DockerRuntime
```

Use exact current class/module names where repository source differs from audit prose.

All PostgreSQL-backed owners must share the supplied session factory as required by their existing APIs.

The transition repository/kernel remains the only WorkRun state-transition authority.

# 8. application vs attempt scope

Application-scoped:

```text
shared durable repositories/authorities
policy/config registries
SecurityPolicy
StockroomOwnerRestriction
provider/tool/secret authority registries
LocalDeterministicProvider
StockroomWorkspace
DockerRuntime boundary
immutable Stockroom scenario catalog
```

Attempt-scoped:

```text
current-binding holder/callback
typed opaque handle/ref map
MaterializationAuthority
StockroomMaterializer
DockerRunSpec derived only after materialization is available
StockroomSummaryDispatcher
AgentExecutionService
StockroomCaptureOwnerAdapter
PreparedStockroomDriver
StockroomCaptureRunner
```

Do not allocate/mutate the filesystem merely to construct the application graph or prepare an attempt for the integration test.

# 9. StockroomCaptureOwnerAdapter authority contract

Implement one Stockroom-specific adapter satisfying the accepted A1 owner port.

For every operation, call the current semantic owner.

The adapter may:

```text
translate request types
hold authentic opaque refs/instances
map explicit current-owner failure to DENIED/FAILED/UNKNOWN
load current WorkRun snapshot
return OwnerCallResult projections
compose transaction participants only when existing owner APIs require it
```

The adapter must not fabricate or reinterpret:

```text
TransitionDecision
AdmittedEvidenceRef / attestation
HumanResult
Judgment
SecurityAdmissionDecision
```

For every successful non-transition call returned to A1:

```text
workflow_state
state_version
```

must be loaded from the current `WorkflowKernel` authoritative snapshot after the owner call.

For transition calls, use the persisted `TransitionDecision.resulting_state/version` and cross-check a fresh kernel load.

# 10. exact runner-operation mapping

Implement compatibility for all accepted A1 operations:

```text
initial_ready
create_attempt
request_transition
seal_security_context
authorize_runtime
materialize
execute
submit_runtime_evidence
submit_static_policy_evidence
evaluate_evidence
submit_agent_human_claim
open_human_gate
issue_judgment
create_policy_blocker
```

Operation status must remain the accepted A1 domain:

```text
initial_ready ADMITTED
create_attempt ADMITTED
request_transition ADMITTED
seal_security_context ADMITTED
authorize_runtime ADMITTED
materialize ADMITTED
execute COMPLETED
submit_runtime_evidence ADMITTED
submit_static_policy_evidence ADMITTED
evaluate_evidence SATISFIED/UNSATISFIED
submit_agent_human_claim REJECTED
open_human_gate PENDING
issue_judgment ADMITTED
create_policy_blocker ADMITTED
```

Underlying owner denial/unknown must stay fail-closed.

# 11. workflow creation/transition semantics

`initial_ready` must establish READY only through the real WorkflowKernel/transition owner.

Do not insert/update a WorkRun row directly to make it READY.

`create_attempt` uses the real execution repository.

`READY -> RUNNING` uses current P1-4 guard facts and the authentic execution-attempt ref.

Later transition participant composition must preserve each semantic owner.

If the current workflow API permits only one transaction participant and both Human/Judgment hooks are required for a transition, a local composite participant may delegate lifecycle hooks in deterministic order, but:

```text
it cannot mint facts
it cannot reinterpret decisions
it cannot create substitute authority refs
```

# 12. Evidence config

Create:

```text
config/evidence/stockroom-capture.v1.json
```

Strict versioned schema, unknown/missing keys rejected.

Enroll distinct scenario/task-contract-bound requirement/checkpoint authority for S1-S4.

Required semantics:

```text
S1:
runtime summary evidence required
PRE_HUMAN_EVIDENCE
SATISFIED attestation used by Judgment/G_EVIDENCE

S2:
same required evidence shape
candidate intentionally omitted
evaluation UNSATISFIED
no evidence substitution

S3:
static policy-conflict evidence
server-owned canonical source bytes/hash
P1-6 admitted
used only as typed blocker provenance
not Judgment

S4:
runtime summary evidence
pre-Human SATISFIED attestation
feeds Human gate participant
```

For durable evidence, use the existing P1-6 V2 content/fingerprint/registry rules exactly.

Do not create a parallel evidence authority.

# 13. Human config

Create:

```text
config/human/stockroom-capture.v1.json
```

Enroll only the exact S4 required use.

Bind:

```text
scenario:
stockroom-s4-human-owned-claim

source state:
ADMISSION_PENDING

target:
HUMAN_REQUIRED

purpose:
P1_7_WORK_RESULT_REVIEW@v1
```

Use current canonical policy/ref naming rules.

The versioned config may declare an operator-supplied selector slot/contract, but must not contain an actual Human selector identity/fingerprint.

`open_human_gate` preparation may return a reservation/prepared ref as `PENDING`; it must not claim a persisted HumanResult.

Real durable Human gate projection is created only through the current Human transition participant when HUMAN_REQUIRED is admitted.

# 14. Judgment config

Create:

```text
config/judgment/stockroom-capture.v1.json
```

Enroll exact deterministic policies only for S1/S2:

```text
S1:
ADMISSION_PENDING -> ACCEPTED
SYSTEM_DETERMINISTIC
evidence attestation required

S2:
ADMISSION_PENDING -> REWORK_REQUIRED
SYSTEM_DETERMINISTIC
required evidence remains unsatisfied
no fabricated evidence ref
```

Use current accepted Judgment kind/policy enums rather than inventing string values if exact repository names differ.

S2 Judgment must bind to the real current evidence-set/checkpoint evaluation outcome even where no admitted attestation exists.

S4:
no Judgment issuance before Human result.

S3:
no Judgment.

# 15. security composition

Stockroom production security must include:

```text
REPOSITORY
FILESYSTEM
PROCESS
TOOL
PROVIDER
SECRET
```

under existing owner-scoped issuance/use rules.

`NETWORK` remains:

```text
DENIED / NOT_REQUIRED
```

No network capability/grant.

All grants/capabilities used by an attempt must be bound to:

```text
run
attempt
current workflow state/version
exact resource/spec/operation fingerprint
```

Do not weaken `StockroomOwnerRestriction`.

Docker spec still requires network none.

# 16. bounded PostgreSQL integration test

Create:

```text
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Use the repository-supported PostgreSQL integration fixture and one shared async session factory.

No SQLite/in-memory substitute for the durable-owner proof.

Do not use direct SQL state fabrication.

At minimum execute a real bounded workflow prefix through the production-style adapter:

```text
NONE -> READY
create_attempt
READY -> RUNNING
```

Requirements:

```text
WorkflowKernel/PostgresTransitionRepository owns both transitions
PostgresExecutionRepository owns attempt creation
adapter receives/returns authentic refs
adapter non-transition snapshot matches real current RUNNING state/version
```

Then, without materialization, prove only safe construction/lookup boundaries:

```text
all three versioned configs strict-load
P1-6 requirement/checkpoint registrations resolve by exact scenario/task-contract identity
S4 Human required-use/policy resolves
S1/S2 Judgment policies resolve
production runner/driver constructs without A1 edits
sealed Stockroom context can be constructed
REPOSITORY/FILESYSTEM grant evaluation is correctly scoped
NETWORK remains denied/not issued
```

All fake explicit runtime edges must be fail-on-call counters.

Require zero calls to:

```text
Docker process runner
Stockroom materialization
provider
tool/dispatcher execution
AgentExecutionService.execute runtime edge
```

Do not call the full `runner.run()` in this Task.

# 17. PostgreSQL prerequisite

The test may use an already available repository-supported PostgreSQL test service/fixture.

This Task does not authorize provisioning the Stockroom Docker runtime or image.

If no supported PostgreSQL test prerequisite is available and the integration test cannot run without provisioning infrastructure outside the repository's normal integration-test authority:

```text
POSTGRESQL_TEST_PREREQUISITE_MISSING
→ STOP after preserving candidate/evidence
```

Do not silently replace PostgreSQL with SQLite or mocks.

# 18. static gate

After implementation run:

```text
compile:
src/aiscc/bootstrap.py
src/aiscc/scenarios/stockroom_production.py
src/aiscc/scenarios/capture_runner.py
src/aiscc/scenarios/driver.py
tests/integration/scenarios/test_stockroom_capture_runner.py

Ruff:
same Python paths

JSON strict parse:
all 3 new config files

git diff --check
```

Require all PASS and index empty.

If mandatory static gate fails:

```text
STATIC_CHECK_FAILURE
→ STOP
```

No same-turn repair after a mandatory static failure.

# 19. mandatory A2 integration

Only after static PASS:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider   tests/integration/scenarios/test_stockroom_capture_runner.py -ra
```

Require exit 0.

Report exact pass/skip/fail count.

Failure:

```text
TEST_FAILURE
→ STOP
```

No same-turn repair after mandatory test failure.

# 20. mandatory A1/B3 regressions

Only after A2 integration PASS:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider   tests/unit/scenarios/test_stockroom_capture_runner.py   tests/unit/scenarios/test_owner_composition.py   tests/integration/scenarios/test_stockroom_binding.py -ra
```

Require exit 0.

This proves accepted A1/B3 behavior remains intact under the new bootstrap/config source.

# 21. targeted owner regressions

Discover only direct tests for source owners actually imported by `stockroom_production.py` under:

```text
tests/unit/**
tests/integration/**
```

Run a bounded targeted set for:

```text
workflow transition
evidence registration/admission
Human reservation/gate
Judgment policy/authority
security Stockroom policy
```

Do not run the entire repository suite in this Task.

Record exact discovered modules and counts.

# 22. implementation contract review

Require PASS for:

```text
THIN_BOOTSTRAP
NO_GLOBAL_SERVICE_LOCATOR
EXPLICIT_OPERATOR_DEPENDENCIES
SINGLE_SHARED_POSTGRES_SESSION_FACTORY
WORKFLOW_OWNER_PRESERVED
EVIDENCE_OWNER_PRESERVED
HUMAN_OWNER_PRESERVED
JUDGMENT_OWNER_PRESERVED
SECURITY_OWNER_PRESERVED
ADAPTER_DOES_NOT_MINT_AUTHORITY
NONWORKFLOW_SNAPSHOT_FROM_KERNEL
TRANSITION_CROSSCHECKS_KERNEL
EVIDENCE_CONFIG_STRICT_AND_VERSIONED
S2_OMISSION_NOT_SUBSTITUTED
S3_STATIC_EVIDENCE_NOT_JUDGMENT
S4_HUMAN_RESULT_ABSENT
JUDGMENT_ONLY_S1_S2
NETWORK_DENIED
NO_DIRECT_SQL_STATE_FABRICATION
A1_RUNNER_DRIVER_UNCHANGED
NO_STOCKROOM_RUNTIME_EXECUTION
```

Require:

```text
21 / 21 PASS
```

# 23. strict runtime ceiling

Allowed runtime evidence:

```text
PostgreSQL integration test:
YES

real WorkflowKernel transitions:
NONE->READY->RUNNING only

real execution attempt creation:
YES

config/authority registration:
YES

security in-memory/grant evaluation:
YES
```

Forbidden:

```text
Stockroom Docker image build/pull/run
real materialization
filesystem checkout/copy of Stockroom repository
provider call
tool execution
process execution
network
secret resolution against real secret
actual S1-S4 run
HumanResult creation
actual terminal Judgment issuance for scenario
capture/export corpus
Replay
Git add/commit/push
```

# 24. final workspace

Before current Task lifecycle:

```text
1738 governance:
3

current Cycle/Judgment:
2

implementation paths:
6

total excluding active Task:
11 exact

index:
empty
```

Then move active Task byte-identically to done.

Final expected Git-visible set:

- `.aiassistant/tasks/done/20260910_1738_aiscc-p2-3-a2-production-owner-bootstrap-integration-feasibility-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1738_aiscc-p2-3-a1-terminal-persisted-a2-feasibility-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1738_aiscc-p2-3-a1-terminal-state-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1824_aiscc-p2-3-a2-feasibility-accepted-production-integration-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1824_aiscc-p2-3-a2-feasibility-audit-final-acceptance-judgment-1.md`
- `src/aiscc/bootstrap.py`
- `src/aiscc/scenarios/stockroom_production.py`
- `config/evidence/stockroom-capture.v1.json`
- `config/human/stockroom-capture.v1.json`
- `config/judgment/stockroom-capture.v1.json`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`
- `.aiassistant/tasks/done/20260910_1824_aiscc-p2-3-a2-production-owner-bootstrap-integration-implementation-1.md`

Exactly:

```text
12 paths
index empty
```

No other path.

# 25. required evidence bundle

Folder:

```text
.aiassistant/reports/target/20260910_1824_aiscc-p2-3-a2-production-owner-bootstrap-integration-implementation-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
MIGRATION_COMPATIBILITY.md
IMPLEMENTATION_MANIFEST.md
PRODUCTION_GRAPH_VERIFICATION.md
ADAPTER_AUTHORITY_VERIFICATION.md
CONFIG_ENROLLMENT_VERIFICATION.md
POSTGRESQL_INTEGRATION_VERIFICATION.md
SECURITY_BOUNDARY_VERIFICATION.md
TEST_VERIFICATION.md
CONTRACT_REVIEW.md
```

Also include byte-preserving copies of:

```text
current Cycle
current Judgment
current done Task
all 6 implementation/config/test paths
```

Expected:

```text
13 root docs
9 canonical/source copies
22 members total
```

`EXPORT_MANIFEST.md` covers all 21 non-self entries with size + SHA-256.

Create adjacent verified ZIP.

Require:

```text
one top-level directory
22 members exact
CRC PASS
13/13 roots
9/9 copies
manifest 21/21
folder/archive byte equality
```

# 26. mandatory stop

```text
DOWNLOAD_ZIP_MISSING
DOWNLOAD_ZIP_HASH_MISMATCH
DOWNLOAD_ZIP_CORRUPT
DOWNLOAD_TASK_MEMBER_MISSING
DOWNLOAD_TASK_PLACEMENT_FAILED
PYTHON_INTERPRETER_REQUIRED_BUT_NOT_FOUND
TRANSPORT_FAILURE
HEAD_OR_TREE_MISMATCH
INDEX_NOT_EMPTY
DIRTY_WORKSPACE_MIXED
PREDECESSOR_OR_A1_IDENTITY_MISMATCH
MIGRATION_SCOPE_REQUIRED
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
A2 production owner/bootstrap integration:
IMPLEMENTED_CANDIDATE / READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT

PostgreSQL construction/owner-boundary proof:
EXECUTED_PASS

runtime prerequisites:
PARTIAL / STOCKROOM DOCKER + MATERIALIZATION + PROVIDER/TOOL STILL NOT_VERIFIED

actual S1-S4:
NOT_STARTED

capture/export corpus:
NOT_STARTED

Replay:
NOT_STARTED
```
