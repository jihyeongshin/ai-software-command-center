# 작업지시서: P2-3 A2 production owner/bootstrap integration feasibility audit

## meta

- task_id: `20260910_1738_aiscc-p2-3-a2-production-owner-bootstrap-integration-feasibility-audit-1`
- created_at: `2026-09-10T17:38:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `SOURCE_STATIC_AUDIT / A2_ENTRY`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `876f232880e652fbf715f13c13b8cc03d27404f0`
- required_base_tree: `0f855b67fcad1be1cb4f635b6b4db8856c43da64`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `A1 terminal governance persistence → A2 production owner/bootstrap source-contract audit`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. fresh-session Windows Python bootstrap

Do NOT assume these are valid on PATH:

```text
python
python3
py
```

Do NOT run bare `python` as a probe.

Known current interpreter candidate:

```text
C:\Users\oracl\AppData\Roaming\uv\python\cpython-3.12.14-windows-x86_64-none\python.exe
```

If Python is required:

1. verify this exact executable first;
2. use it by exact path if valid;
3. if unavailable, discover another actually executable Python interpreter;
4. invoke only exact executable paths.

For any repository import/static probe that requires project dependencies, verify and use:

```text
.venv\Scripts\python.exe
```

by exact path.

This Task does not run pytest.

# 1. inbound transport

Verify the Browser delivery ZIP exact filename/SHA-256 from the Short Prompt.

Place TASK first at:

```text
.aiassistant/tasks/active/20260910_1738_aiscc-p2-3-a2-production-owner-bootstrap-integration-feasibility-audit-1.md
```

Read it fully.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260910_1738_aiscc-p2-3-a1-terminal-persisted-a2-feasibility-entry-1.cycle.md
SHA-256:
0e6b3a12767fc3d5830726e1327d8e0d6f097271aa7aedd4157a4b86a566a782

.aiassistant/reports/aiscc/20260910_1738_aiscc-p2-3-a1-terminal-state-persistence-final-acceptance-judgment-1.md
SHA-256:
4df00fc71ff6603cb0703077c10c5460d3db2bdb6ec772a2b3fbd8b5983ed476
```

Bootstrap failure before TASK placement:

```text
STOP
no report/export
no substantive project mutation
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

After current Cycle/Judgment placement, expected Git-visible set excluding active Task is exact:

```text
.aiassistant/records/aiscc/cycles/20260910_1738_aiscc-p2-3-a1-terminal-persisted-a2-feasibility-entry-1.cycle.md
.aiassistant/reports/aiscc/20260910_1738_aiscc-p2-3-a1-terminal-state-persistence-final-acceptance-judgment-1.md
```

Exactly 2 paths.

Any additional Git-visible path:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Ignored target/export residue may exist and is non-blocking.

# 3. exact predecessor/state identity

Require exact current governance/state:

- `.aiassistant/tasks/done/20260910_1546_aiscc-p2-3-capture-runner-core-terminal-state-reconciliation-persistence-1.md`  `7ff31c4436ef3fd66fba4d5af9d648a6451543d795c6aeeff7a5ed242894941d`
- `.aiassistant/records/aiscc/cycles/20260910_1546_aiscc-p2-3-capture-runner-core-final-accepted-a2-entry-1.cycle.md`  `842c3dd58607e7fd3996a66a874b9aa01588f702b7516d625223c3d6665c53bb`
- `.aiassistant/reports/aiscc/20260910_1546_aiscc-p2-3-capture-runner-core-persistence-final-acceptance-judgment-1.md`  `337a13ce7c3f226620c3a2921f2e2977f93404d52b55c1d886645657f4a04953`
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `051041381beb996eebd5ed4ef9397f7e5858d120c9fd157a6055e0dee08419c9`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `7c16fd1c9bbf9d973913e189dd86937d927a0fad8694c62cd8ab55f7144bd7cb`

Require exact A1 committed source/test identities from HEAD:

- `src/aiscc/scenarios/capture_runner.py`  `600de0a4b0e718f02ab2e1907b7be62b2c4a23756559fdf99cb4cd55fb80b3d2`
- `src/aiscc/scenarios/driver.py`  `9871847ec0a236ef61c91518ff95764f3c2138e3854c25a4c8cab4f028503ce6`
- `tests/unit/scenarios/test_stockroom_capture_runner.py`  `a137021608ac9cb5b4c328b6bb88fd0c22cb0d9afd9b1a22054ec5bdd32f68ff`

Any mismatch:

```text
PREDECESSOR_OR_A1_IDENTITY_MISMATCH
→ STOP
```

# 4. mandatory governance reads

Read fully before source audit:

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_RUNTIME_SUBSTRATE.md
.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md
.aiassistant/rules/AISCC_SECURITY_SANDBOX.md
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/records/aiscc/cycles/20260910_1738_aiscc-p2-3-a1-terminal-persisted-a2-feasibility-entry-1.cycle.md
.aiassistant/reports/aiscc/20260910_1738_aiscc-p2-3-a1-terminal-state-persistence-final-acceptance-judgment-1.md

.aiassistant/reports/aiscc/20260910_1008_aiscc-p2-3-stockroom-settlement-persistence-final-acceptance-judgment-1.md
.aiassistant/tasks/done/20260910_1008_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-retry-1.md
.aiassistant/reports/aiscc/20260910_1313_aiscc-p2-3-capture-runner-core-final-acceptance-judgment-1.md
.aiassistant/reports/aiscc/20260910_1546_aiscc-p2-3-capture-runner-core-persistence-final-acceptance-judgment-1.md
```

Do not recursively activate old Task instructions.

# 5. mandatory source reads

Read fully:

```text
src/aiscc/bootstrap.py

src/aiscc/scenarios/capture_runner.py
src/aiscc/scenarios/driver.py
src/aiscc/scenarios/composition.py
src/aiscc/scenarios/enrollment.py
src/aiscc/scenarios/runtime_models.py

src/aiscc/persistence/repository.py
src/aiscc/persistence/models.py

src/aiscc/workflow/kernel.py
src/aiscc/workflow/models.py

src/aiscc/evidence/service.py
src/aiscc/evidence/models.py
src/aiscc/evidence/authority.py

src/aiscc/human/authority.py
src/aiscc/human/repository.py
src/aiscc/human/models.py

src/aiscc/judgment/authority.py
src/aiscc/judgment/models.py

src/aiscc/providers/service.py
src/aiscc/providers/local_deterministic.py
src/aiscc/providers/stockroom_tool.py

src/aiscc/security/policy.py
src/aiscc/security/stockroom_policy.py

src/aiscc/runtime/stockroom_workspace.py
src/aiscc/runtime/stockroom_materializer.py
src/aiscc/runtime/docker.py
```

If a listed file does not exist, record exact absence and follow imports/current source to the actual owner file. Do not create a replacement.

Read direct imported construction/config authority only as needed.

# 6. bounded configuration inventory

Inspect only these roots:

```text
config/evidence/**
config/human/**
config/judgment/**
config/scenarios/stockroom/**
```

Determine actual registry/enrollment mechanisms.

Do not assume these proposed files are necessary:

```text
config/evidence/stockroom-capture.v1.json
config/human/stockroom-capture.v1.json
config/judgment/stockroom-capture.v1.json
```

For each domain classify:

```text
EXISTING_CONFIG_SUFFICIENT
NEW_VERSIONED_CONFIG_REQUIRED
SOURCE_CONSTRUCTION_ONLY
CANONICAL_CONFLICT
```

If `NEW_VERSIONED_CONFIG_REQUIRED`, specify exact filename/schema/loader/registration path based on current source.

No config mutation.

# 7. production construction audit

Determine the smallest truthful production-style construction root that can create and bind:

```text
shared async PostgreSQL session factory

PostgresExecutionRepository
WorkflowKernel

EvidenceAdmissionService
its durable evidence repository/evaluator/content authority dependencies

PostgresHumanAuthorityRepository
HumanGuardAuthority / reservation authority required by current API

PostgresJudgmentAuthority
Judgment policy authority / Command Center authority required by current API

SecurityPolicy
StockroomOwnerRestriction

StockroomWorkspace
StockroomMaterializer

DockerRuntime with explicit runner dependency

LocalDeterministicProvider
StockroomSummaryDispatcher
AgentExecutionService

accepted StockroomCaptureRunner
PreparedStockroomDriver / preparation inputs
```

Answer exact questions:

```text
Where should the A2 construction root live?
Is src/aiscc/bootstrap.py the correct owner?
Does it already have a session-factory/application composition pattern?
Which dependencies are caller/operator supplied?
Which objects must be attempt-scoped vs application-scoped?
Which owner APIs need adapters/wrappers?
```

Do not invent a service locator or global singleton.

# 8. A1 runner-to-real-owner compatibility audit

For every operation expected by `StockroomCaptureRunner`, map:

```text
runner operation name
runner expected OwnerCallResult contract
real current owner/API method
adapter required YES/NO
exact adapter owner/path if required
status mapping
workflow state/version snapshot source
authority ref/provenance source
failure/unknown mapping
```

The adapter layer must not reinterpret semantic authority.

If an adapter would need to fabricate:

```text
TransitionDecision
AdmittedEvidenceRef
HumanResult
Judgment
SecurityAdmissionDecision
```

classify:

```text
CANONICAL_AUTHORITY_CONFLICT
```

and STOP the audit after recording sufficient evidence.

# 9. WorkRun / attempt creation audit

Resolve exact durable creation sequence for:

```text
initial READY
WorkRun identity
attempt identity
create_attempt
READY -> RUNNING
```

Determine whether current `PostgresExecutionRepository`/workflow owner can satisfy A1 runner's `initial_ready` and `create_attempt` operations directly or requires an A2 adapter.

Specify exact source APIs and transaction boundaries.

No DB execution.

# 10. evidence enrollment audit

Resolve exact S1/S2/S3/S4 evidence contracts against current P1-6 APIs.

For each scenario state:

```text
requirement/checkpoint identifier
evidence type/source owner
candidate creation/submission owner
admission API
set/checkpoint evaluation API
durable content requirement
S2 omitted-candidate mechanism
S3 static policy-conflict evidence mechanism
```

Decide whether current config is sufficient.

No Agent/tool output may be treated as admitted evidence without P1-6 owner admission.

# 11. Human gate enrollment audit

For S4 resolve:

```text
gate policy/identifier
principal selector
reservation/open API
producer-ref binding
current state/version binding
expected PENDING/ACTIVE projection
HumanResult remains absent
```

Determine exact config/source changes required for A2 integration proof.

Do not create HumanResult.

# 12. Judgment policy enrollment audit

For S1/S2 resolve:

```text
deterministic policy identifiers
evidence requirement/set binding
current version applicability
issue API
expected ACCEPTED / REWORK_REQUIRED semantics
```

Determine exact config/source changes required.

No actual Judgment issuance.

# 13. security/capability composition audit

Map exact grants/receipts needed by A2 production composition:

```text
REPOSITORY
FILESYSTEM
PROCESS
TOOL
PROVIDER
SECRET
```

and prove:

```text
NETWORK:
DENIED / NOT_REQUIRED
```

Specify which grants are attempt-scoped and how sealed Stockroom context/current-binding callbacks are constructed.

Do not execute any capability.

# 14. integration-test boundary

Design one smallest PostgreSQL-backed A2 integration test module that proves **construction and owner-boundary compatibility** without executing Docker/materializer/provider/tool.

The integration test plan must prove at least:

```text
real PostgreSQL repositories/authorities construct from one session factory

real WorkflowKernel transition path binds to runner adapter

evidence requirement/policy registries load exact A2 enrollment

Human gate policy resolves for S4

Judgment policies resolve for S1/S2

SecurityPolicy grants remain owner-scoped

runner can be constructed with production-style adapters

no Docker/process/filesystem materialization/provider/tool execution
```

It may use a fake/no-call runtime edge after construction.

Determine exact proposed test file path.

Do not run PostgreSQL in this audit.

# 15. exact A2 mutation allowlist

Create an exact proposed next implementation allowlist.

Classify every path:

```text
CREATE
MODIFY
CONFIG_CREATE
CONFIG_MODIFY
TEST_CREATE
TEST_MODIFY
NO_CHANGE_NEIGHBOR
```

Start from the prior 1008 proposal:

```text
MODIFY candidate:
src/aiscc/bootstrap.py

TEST_CREATE candidate:
tests/integration/scenarios/test_stockroom_capture_runner.py

CONFIG conditional:
config/evidence/stockroom-capture.v1.json
config/human/stockroom-capture.v1.json
config/judgment/stockroom-capture.v1.json
```

A1 runner/driver should be `NO_CHANGE_NEIGHBOR` unless current exact source proves a compatibility defect requiring a separately justified rework.

If another production adapter/source file is necessary, name its exact path and reason.

Do not use wildcard mutation scopes in the final allowlist.

# 16. conflict / gap classification

For each issue classify exactly:

```text
READY_CURRENT_SOURCE
IMPLEMENTATION_GAP
CONFIG_ENROLLMENT_REQUIRED
TEST_GAP
RUNTIME_PREREQUISITE_LATER
CANONICAL_AUTHORITY_CONFLICT
```

`CANONICAL_AUTHORITY_CONFLICT` is a mandatory STOP and must identify conflicting accepted rule/source semantics.

Normal implementation/config gaps are not blockers to audit completion.

# 17. recommended A2 implementation cut

Recommend one exact next Task boundary.

Target should normally be:

```text
A2 production construction + adapters/config enrollment + bounded PostgreSQL integration proof
```

but split it if the audit finds a meaningful authority/risk boundary.

Do not include:

```text
Docker image build/provisioning
real Stockroom materialization
real provider/tool/process execution
actual S1-S4 capture
capture/export schema
Replay
public deployment
```

# 18. strict no-mutation / no-runtime ceiling

This audit performs:

```text
source/config/test mutation:
NONE

git add/commit/push:
NONE

pytest:
NOT_RUN

PostgreSQL:
NOT_RUN

Docker:
NOT_RUN

materialization:
NOT_RUN

provider/tool:
NOT_RUN

network:
NOT_RUN

HumanResult:
NOT_CREATED

Judgment:
NOT_CREATED

actual scenario:
NOT_RUN
```

Read-only source/config inspection and static import/signature inspection are allowed.

# 19. final workspace

Before Task lifecycle:

```text
current Cycle/Judgment:
2 exact Git-visible paths

index:
empty
```

Move:

```text
.aiassistant/tasks/active/20260910_1738_aiscc-p2-3-a2-production-owner-bootstrap-integration-feasibility-audit-1.md
→
.aiassistant/tasks/done/20260910_1738_aiscc-p2-3-a2-production-owner-bootstrap-integration-feasibility-audit-1.md
```

Final expected:

```text
current Cycle
current Judgment
current done Task

3 exact Git-visible paths
index empty
```

No source/config/test delta.

# 20. required evidence roots

Bundle folder:

```text
.aiassistant/reports/target/20260910_1738_aiscc-p2-3-a2-production-owner-bootstrap-integration-feasibility-audit-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
A2_FEASIBILITY_AUDIT.md
PRODUCTION_CONSTRUCTION_PLAN.md
RUNNER_REAL_OWNER_COMPATIBILITY.md
EVIDENCE_HUMAN_JUDGMENT_ENROLLMENT_PLAN.md
SECURITY_COMPOSITION_PLAN.md
A2_INTEGRATION_TEST_PLAN.md
A2_IMPLEMENTATION_ALLOWLIST.md
A2_CUT_RECOMMENDATION.md
```

Include byte-preserving copies of:

```text
current Cycle
current Judgment
current done Task
```

Expected bundle member count:

```text
15 exact
```

`EXPORT_MANIFEST.md` covers all 14 non-self members with relative path, size and SHA-256.

Create adjacent verified ZIP.

# 21. success ceiling

Success:

```text
result:
A2_FEASIBILITY_AUDIT_COMPLETE / BROWSER_JUDGMENT_REQUIRED

A2 exact implementation allowlist:
RESOLVED

A2 implementation:
NOT_STARTED

runtime prerequisites:
NOT_VERIFIED

actual scenario:
NOT_STARTED
```

# 22. mandatory stop

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
CANONICAL_AUTHORITY_CONFLICT
UNEXPECTED_WORKSPACE_DELTA
ZIP_EXPORT_FAILED
```
