# 작업지시서: P2-3 S1 execution-lifecycle desync source ownership diagnosis

## meta

- task_id: `20260913_0115_aiscc-p2-3-s1-execution-lifecycle-desync-source-ownership-diagnosis-1`
- created_at: `2026-09-13T01:15:17+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `SOURCE_OWNERSHIP_DIAGNOSIS`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `6cc4f988f56f5cbf32e57f4b5e9a52a180044c36`
- required_parent: `35cee94a92d1f12801576ef48038196922687f42`
- required_grandparent: `ee623c995cf1c24b4a362834f2d6d1fdf71a30cd`
- executor_session_action: `CONTINUE_CURRENT_CONTEXT`
- python_executable: `C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe`
- source_write_authorized: `No`
- runtime_access_authorized: `No`
- success_ceiling: `EXECUTION_LIFECYCLE_DEFECT_OWNER_IDENTIFIED / SOURCE_REWORK_PENDING`

# 0. purpose

Diagnose the exact source owner of the persisted S1 execution-lifecycle desynchronization.

Observed durable result from 0036:

```text
WorkRun:
RUNNING / v2

execution attempt:
NOT_STARTED

execution operations:
0

StockroomCaptureRunner:
stopped at EXECUTE with execution:NOT_STARTED
```

The exact S1 run/attempt is already durable.

Never execute or mutate it in this Task.

# 1. Python / transport

Use only:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe
```

Forbidden:

```text
python
py
WindowsApps Python alias
PATH Python discovery
```

Verify the delivery ZIP/hash and exactly three flat safe members.

Place current Task first:

```text
.aiassistant/tasks/active/20260913_0115_aiscc-p2-3-s1-execution-lifecycle-desync-source-ownership-diagnosis-1.md
```

Then place:

```text
.aiassistant/records/aiscc/cycles/20260913_0115_aiscc-p2-3-s1-execution-lifecycle-desync-diagnosis-entry-1.cycle.md
SHA-256:
8b9f180f0e9a0d4ccf505ac2c3de920a5be3c9a088f163ae80066c1d6145b428

.aiassistant/reports/aiscc/20260913_0115_aiscc-p2-3-s1-execution-not-started-runtime-hold-judgment-1.md
SHA-256:
f462080446ad883fea933b48677a7b871dfcd054b8c344c410950db02af3772d
```

# 2. repository baseline

Require:

```text
branch main
HEAD 6cc4f988f56f5cbf32e57f4b5e9a52a180044c36
HEAD^ 35cee94a92d1f12801576ef48038196922687f42
HEAD^^ ee623c995cf1c24b4a362834f2d6d1fdf71a30cd
index empty
tracked clean
```

Before delivery Git-visible untracked exactly six:

- `.aiassistant/tasks/done/20260913_0012_aiscc-p2-3-private-s1-normal-scenario-execution-and-capture-retry-1.md`  `310bcfab97f13c7606bb09fc773ec6c659102e63b6ba1d33fa38b18c7cfeb034`
- `.aiassistant/records/aiscc/cycles/20260913_0012_aiscc-p2-3-private-s1-source-correction-persisted-execution-entry-1.cycle.md`  `ff0ca7f1752fd3a49306b660b1823b57b194a60b1d58c2341867e9c9b75dc702`
- `.aiassistant/reports/aiscc/20260913_0012_aiscc-p2-3-private-s1-source-correction-persisted-execution-authorization-judgment-1.md`  `568268a48fcda0145b549f9b26a5baf4287b8fb7f4937c3bfd9b2db60b5836a8`
- `.aiassistant/tasks/done/20260913_0036_aiscc-p2-3-private-s1-builder-reentry-semantic-datetime-retry-1.md`  `0226353dba304ac01e9add745053502618001f6eecd833a92e9fd2b45d844f4b`
- `.aiassistant/records/aiscc/cycles/20260913_0036_aiscc-p2-3-private-s1-builder-reentry-harness-corrected-retry-entry-1.cycle.md`  `8619cd9bfc9c3476129199c1213366a1bd26127c2f64d2156bddada7a3d97bfa`
- `.aiassistant/reports/aiscc/20260913_0036_aiscc-p2-3-private-s1-builder-reentry-harness-error-retry-judgment-1.md`  `82550b3a3ed60678b1b252fe483f48003757870427ae8c1ecbefd4c35d1f0011`

Canonical state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `02b7a77d3f29d7ee3878157470020ab83b377ba0343867ab81ec6e82d1a9190b`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `9ca1b1a24f3f73c2f81d3342442cf0462b58fecdba2dbccc33509b0d4039ab71`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `7315a943ad4ed82757f4398d9613f3a6f773755f3496fa1e8fa816123422ea84`

Known current source baselines:

- `src/aiscc/persistence/repository.py`  `ab00af3dd871477da74b83275258aa48a47ba9a7081aad0154a808b6e4f1c089`
- `src/aiscc/scenarios/capture_runner.py`  `0dab27e0ce9ce2da7953188bcb26f288b637a4ba524141be2800b08302a59b18`
- `src/aiscc/scenarios/stockroom_production.py`  `1ca58848a837e1130229c7a0e085df999d04c6041c77bb61098185d342ff14a0`

After current Cycle/Judgment placement while Task is active/ignored:

```text
Git-visible untracked:
8 exact
```

Unexpected tracked/untracked delta:

```text
DIRTY_WORKSPACE_MIXED
→ STOP_WITH_REPORT_EXPORT
```

# 3. strict prohibition

This Task is read-only diagnosis.

Do not:

```text
edit source
edit tests
edit state
git add/commit/push/reset/restore/checkout/stash/clean

Docker CLI/API
PostgreSQL connection/query
private secret file
private runtime root

prepare_capture
builder
runner
adapter execution
provider/tool execution
WorkRun transition
execution attempt transition
```

Do not run runtime-bearing pytest.

Static AST/import/source inspection and `git grep` are allowed.

# 4. canonical contract reads

Read exact current canonical authority for:

```text
P1-4 READY → RUNNING
G_EXECUTION_STARTED
ExecutionStatus four-value lifecycle
P1-5 execution attempt event ownership
unknown-outcome / retry rules
workflow-state versus execution-status separation
```

At minimum read the current tracked rules corresponding to:

```text
AISCC_ORCHESTRATION
AISCC_PROVIDER_TOOL_EXECUTION
AISCC_SECURITY_SANDBOX
```

Record exact file/blob/SHA identities.

# 5. complete P1-5 source ownership read

Read completely, not snippets:

```text
src/aiscc/providers/service.py
src/aiscc/persistence/repository.py
```

Also read any directly imported P1-5 authority/model module required to understand:

```text
AgentExecutionService.execute
AgentExecutionService.execute_provider
ExecutionStatus
ExecutionAttemptRef
ExecutionReferenceAuthority
PostgresExecutionRepository.create_attempt
PostgresExecutionRepository.transition_attempt
PostgresExecutionRepository.create_operation
lifecycle_result
```

Record exact HEAD blob and whole-file SHA for every file used.

# 6. complete Stockroom integration read

Read completely:

```text
src/aiscc/scenarios/capture_runner.py
src/aiscc/scenarios/stockroom_production.py
```

Trace exact calls:

```text
initial_ready
create_attempt
READY_TO_RUNNING request
seal_security_context
authorize_runtime
materialize
execute
```

Record every write/read of:

```text
_CurrentAttemptReader.current
_CurrentAttemptReader.attempt
ExecutionAttemptRef
execution_repository.transition_attempt
```

# 7. mechanical callsite inventory

Using `git grep` and AST, enumerate every tracked production callsite of:

```text
transition_attempt(
"EXECUTION_STARTED"
AgentExecutionService.execute(
create_operation(
```

For each callsite record:

```text
path
symbol/function
caller
required preconditions
whether reached by Stockroom S1 production path
```

Do not infer missing calls from naming alone.

# 8. required ownership conclusion

Determine exactly one of:

```text
A. AgentExecutionService owns NOT_STARTED → RUNNING and current Stockroom path prevents/omits that service transition.

B. Stockroom adapter must transition the execution attempt before AgentExecutionService.execute, but current adapter omits it.

C. Workflow READY → RUNNING transaction is intended to coordinate the execution status transition, but durable participant wiring is absent.

D. another exact current source owner/mechanism exists.
```

The conclusion must cite concrete current source callsites and preconditions.

If ownership remains ambiguous:

```text
EXECUTION_LIFECYCLE_OWNER_AMBIGUOUS
→ report/export
→ no source write
```

# 9. explain observed `NOT_STARTED`

Mechanically explain why the actual 0036 path can produce:

```text
WorkRun RUNNING/v2
ExecutionAttempt NOT_STARTED
AgentExecutionService/adapter execute result NOT_STARTED
execution_operations = 0
```

Identify the earliest exact predicate/branch that returns or preserves `NOT_STARTED`.

Do not claim a Docker/provider failure unless source shows Docker/provider dispatch can be reached before that branch.

# 10. source/test rework scope discovery

Without editing, identify the minimal exact source paths required to correct the defect.

Also identify the exact existing test paths that own:

```text
execution lifecycle NOT_STARTED → RUNNING
Stockroom production end-to-end owner binding
runner execute path
durable execution attempt transitions
```

Use `git ls-files`/`git grep`; do not invent test filenames.

For each candidate path provide:

```text
HEAD blob
whole SHA-256
reason required
```

If a model/schema/migration change appears required, state it explicitly and stop at diagnosis.

# 11. runtime recovery boundary

Do not propose or execute a concrete DB/runtime repair in this Task.

Only classify the persisted attempt facts:

```text
run exists
workflow RUNNING/v2
attempt exists
attempt NOT_STARTED
no execution operation
no evidence/judgment
```

State whether current source contracts make in-place continuation obviously safe, obviously forbidden, or not yet decidable.

The next Browser Task owns any recovery design.

# 12. lifecycle / Git

Before Task move require:

```text
HEAD unchanged
index empty
tracked clean
Git-visible untracked 8 exact
```

Move current Task byte-identically to done.

Final Git-visible untracked:

```text
9 exact

0012 Task/Cycle/Judgment
0036 Task/Cycle/Judgment
current Task/Cycle/Judgment
```

# 13. contract review

Require exactly 28 rows:

```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_CLEAN
PREDECESSOR_6_ARTIFACTS_EXACT
CURRENT_STATE_HASHES_EXACT
KNOWN_SOURCE_BASELINES_EXACT
PYTHON_EXECUTABLE_EXACT
NO_PRIVATE_RUNTIME_ACCESS
NO_DB_DOCKER_ACCESS
NO_SOURCE_TEST_MUTATION
NO_GIT_WRITE
P1_4_EXECUTION_STARTED_CONTRACT_READ
P1_5_EXECUTION_STATUS_CONTRACT_READ
AGENT_EXECUTION_SERVICE_COMPLETE_READ
EXECUTION_REPOSITORY_LIFECYCLE_COMPLETE_READ
STOCKROOM_ADAPTER_EXECUTION_PATH_COMPLETE_READ
CAPTURE_RUNNER_EXECUTION_ORDER_COMPLETE_READ
NOT_STARTED_TO_RUNNING_OWNER_IDENTIFIED
NOT_STARTED_TO_RUNNING_DURABLE_CALL_IDENTIFIED
READY_TO_RUNNING_RELATION_IDENTIFIED
CURRENT_PRODUCTION_CALL_GRAPH_EXACT
WHY_NOT_STARTED_RETURNED_IDENTIFIED
EXECUTION_OPERATION_ZERO_CAUSE_IDENTIFIED
DEFECT_OWNER_MODULE_EXACT
REQUIRED_SOURCE_PATHS_EXACT
REQUIRED_TEST_PATHS_EXACT
NO_RUNTIME_RECOVERY_PLAN_FABRICATED
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
EXPORT_INTEGRITY_PASS
```

Success:

```text
28 / 28 PASS
```

# 14. success export

Root docs exactly 10:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
CANONICAL_LIFECYCLE_CONTRACT.md
P1_5_EXECUTION_SOURCE_INVENTORY.md
STOCKROOM_EXECUTION_CALL_GRAPH.md
NOT_STARTED_ROOT_CAUSE.md
SOURCE_TEST_SCOPE_DISCOVERY.md
CONTRACT_REVIEW.md
```

Project-relative copies exactly 7:

```text
current Cycle
current Judgment
current done Task
src/aiscc/providers/service.py
src/aiscc/persistence/repository.py
src/aiscc/scenarios/capture_runner.py
src/aiscc/scenarios/stockroom_production.py
```

Success export:

```text
17 members total
16 non-self manifest rows
one top-level directory
CRC PASS
folder/archive byte equality
TASK.md == current done Task
```

If directly required P1-5 authority/model source files are necessary for proof, include their exact metadata in reports,
not extra source copies, unless required by the export policy.

# 15. success ceiling

```text
0036 runtime:
HOLD / PRESERVED

S1 rerun:
NOT AUTHORIZED

execution lifecycle defect owner:
IDENTIFIED

source rework:
NOT YET PERFORMED

runtime recovery:
NOT YET AUTHORIZED

P2-3:
IN_PROGRESS
```
