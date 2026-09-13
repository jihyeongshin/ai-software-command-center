# 작업지시서: P2-3 stranded S1 in-place recovery boundary design

## meta

- task_id: `20260913_1129_aiscc-p2-3-stranded-s1-in-place-recovery-boundary-design-1`
- created_at: `2026-09-13T11:29:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `PRIVATE_S1_RECOVERY_DESIGN`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `5affe61f02994f219b22ca934b5e0b93bc5e6f60`
- required_parent: `a4eb36611dca8d504610d9e3091950b0f32c20e7`
- required_grandparent: `6cc4f988f56f5cbf32e57f4b5e9a52a180044c36`
- python_executable: `C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe`
- source_write_authorized: `No`
- test_write_authorized: `No`
- private_runtime_access_authorized: `No`
- runtime_recovery_authorized: `No`
- success_ceiling: `STRANDED_S1_RECOVERY_BOUNDARY_DEFINED / EXECUTION_NOT_AUTHORIZED`

# 0. purpose

Design, but do not execute, the legal recovery boundary for the existing stranded S1 state:

```text
run_id:
aiscc-p2-3-private-s1-normal-v1-run

attempt_id:
aiscc-p2-3-private-s1-normal-v1-attempt-1

WorkRun:
RUNNING / v2

ExecutionAttempt:
NOT_STARTED

execution_operations:
0

runtime evidence:
none

Judgment:
none
```

These facts are persisted governance authority from the accepted 0036→1102 lineage.
Do not access the private runtime merely to re-observe them.

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

Verify delivery ZIP/hash and exactly three flat safe members.

Place current Task first:

```text
.aiassistant/tasks/active/20260913_1129_aiscc-p2-3-stranded-s1-in-place-recovery-boundary-design-1.md
```

Then place exact Cycle/Judgment:

```text
.aiassistant/records/aiscc/cycles/20260913_1129_aiscc-p2-3-stranded-s1-recovery-design-entry-1.cycle.md
SHA-256:
02356ec126b9381248ab491b013ad8a74f90abfd8d69a50349ad9f2718dd0b50

.aiassistant/reports/aiscc/20260913_1129_aiscc-p2-3-stranded-s1-recovery-design-authorization-judgment-1.md
SHA-256:
4ab5b734e9802c975e51a761bd4281b7a9359df7bd140711d7e8cb3e49dd214a
```

Bootstrap mismatch:

```text
STOP
no source/test/state write
no runtime/DB/Docker access
no report/export
```

# 2. repository baseline

Require:

```text
branch:
main

HEAD:
5affe61f02994f219b22ca934b5e0b93bc5e6f60

HEAD^:
a4eb36611dca8d504610d9e3091950b0f32c20e7

HEAD^^:
6cc4f988f56f5cbf32e57f4b5e9a52a180044c36

index:
empty

tracked:
clean

Git-visible untracked before delivery:
none
```

Canonical state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `550b7b3ec6659c5ad86558c84902a5319457334432db452405e31a2eb1153164`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `c9496a814cb94a834f53c4dee46032836dfaa4f8490d433a5909c0e46d2e3c3f`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `a6130f00deb41a1cae8c42cb62e7eb57d3457e40775794c6efb725fb604c832e`

Known current source hashes:

- `src/aiscc/scenarios/stockroom_production.py`  `c070e194b5d3e0ca18d952202f71860175ab36f3a51b327c7799fe5ef36bffb3`
- `src/aiscc/scenarios/capture_runner.py`  `0dab27e0ce9ce2da7953188bcb26f288b637a4ba524141be2800b08302a59b18`
- `src/aiscc/providers/service.py`  `f21c3c29443446650e31fb0d4d0d30ceddb8956d51ad2e17221536102c6c5c18`
- `src/aiscc/persistence/repository.py`  `ab00af3dd871477da74b83275258aa48a47ba9a7081aad0154a808b6e4f1c089`
- `src/aiscc/workflow/guards.py`  `e7509199bca3b901c7a04b4e5a1d8c23bab217eca5b78a3b9319d10300993cab`

After current Cycle/Judgment placement while current Task remains active/ignored:

```text
Git-visible untracked:
2 exact

current Cycle
current Judgment
```

Any unexpected dirt/path:

```text
DIRTY_WORKSPACE_MIXED
→ STOP_WITH_REPORT_EXPORT
```

# 3. absolute runtime prohibition

Do not access:

```text
Docker
retained PostgreSQL
private password file
private runtime root
0036 WorkRun row
0036 ExecutionAttempt row
provider/tool runtime
network runtime
```

Do not invoke:

```text
build_stockroom_production
prepare_capture
StockroomCaptureRunner.run
transition_attempt
request_transition
seal_security_context
authorize_runtime
materialize
AgentExecutionService.execute
evidence admission/evaluation
scenario Judgment
```

This Task is source/contract analysis only.

# 4. canonical governance contract

Read current tracked rules governing:

```text
WorkflowState READY / RUNNING / ADMISSION_PENDING / ACCEPTED
G_EXECUTION_STARTED
ExecutionStatus NOT_STARTED / RUNNING / EXECUTOR_COMPLETED / EXECUTION_FAILED
execution-attempt authority
security state-version binding
unknown outcome / retry / same-attempt rules
evidence provenance continuity
Judgment prerequisites
```

At minimum use current canonical:

```text
AISCC_ORCHESTRATION
AISCC_PROVIDER_TOOL_EXECUTION
AISCC_SECURITY_SANDBOX
AISCC_EVIDENCE_ADMISSION
AISCC_HUMAN_GATE_JUDGMENT
```

Record exact rule path + whole SHA-256.

# 5. complete source reads

Read completely:

```text
src/aiscc/scenarios/stockroom_production.py
src/aiscc/scenarios/capture_runner.py
src/aiscc/providers/service.py
src/aiscc/persistence/repository.py
src/aiscc/workflow/guards.py
```

Also discover and read every directly required tracked production module owning:

```text
WorkflowKernel/request_transition
security sealing/authorization
ExecutionReferenceAuthority
ExecutionAttemptRef
materialization
evidence submission/evaluation
Judgment issuance
```

For every source used in the conclusion record:

```text
path
HEAD blob
whole SHA-256
symbol(s) relied upon
```

# 6. separate the two already-consumed authorities

Mechanically prove the current contract distinguishes:

```text
Workflow READY→RUNNING transition:
already admitted / must not be replayed

ExecutionAttempt NOT_STARTED→RUNNING event:
not observed in 0036 / potentially distinct durable lifecycle operation
```

Determine whether `transition_attempt(EXECUTION_STARTED)` is legally callable when:

```text
WorkRun is already RUNNING/v2
attempt is still NOT_STARTED
same run_id
same attempt_id
no execution operation exists
```

Do not infer from repository API existence alone; prove required preconditions.

# 7. delayed EXECUTION_STARTED legality

Determine all invariants required by current source for a delayed start event, including:

```text
attempt current status
expected execution version
causal workflow state
causal workflow version
task contract identity/version
provider/tool registry identity
execution-reference issuer state
event refs, if any
idempotency/duplicate-start behavior
```

Classify delayed start as:

```text
LEGAL_EXACTLY_ONCE
FORBIDDEN
LEGAL_ONLY_WITH_NEW_SOURCE_VALIDATION
UNRESOLVED
```

# 8. public recovery/reconstruction API inventory

Using `git grep` + AST, inventory every public/current production entrypoint that can:

```text
load/reconstruct an existing WorkRun
load/reconstruct an existing execution attempt
construct Stockroom owners for an existing run
continue security/materialization/execution from RUNNING
resume a capture without create_attempt
```

Explicitly inspect whether these are safe for an existing run:

```text
build_stockroom_production
prepare_capture
StockroomCaptureRunner.run
StockroomCaptureOwnerAdapter methods
AgentExecutionService.execute
```

Prove whether each would create/re-register/replay any already-consumed authority.

# 9. prepare_capture / runner re-entry determination

Answer separately:

```text
Can prepare_capture be called for this exact existing run/attempt without creating/replaying READY state?
Can StockroomCaptureRunner.run be called on a reconstructed prepared object without replaying initial_ready/create_attempt/READY→RUNNING?
```

Expected answer must be source-proved, not assumed.

If either is unsafe, identify the earliest duplicated operation.

# 10. security continuation legality

Assuming only for analysis that the attempt were validly advanced to RUNNING against WorkRun RUNNING/v2, determine whether current security contracts permit fresh:

```text
seal_security_context
authorize_runtime
```

for the same exact run/attempt/current state-version.

Prove:

```text
whether an old RUNNING capability exists
whether none was ever issued in 0036
whether fresh capability issuance after delayed execution start is allowed
whether state-version binding remains exact
```

No capability may be created in this Task.

# 11. materialization and execution continuity

Determine whether materialization/provider execution can safely occur after such a delayed execution start.

Prove whether:

```text
materialization from 0036 was already durable or only pre-execution state
repeating materialization would duplicate durable refs/artifacts
AgentExecutionService.execute requires only current RUNNING attempt authority or additional transient owner state
execution operation creation remains first operation
same execution attempt ID remains mandatory
```

Use persisted governance facts where runtime facts are already accepted; do not query runtime.

# 12. evidence provenance continuity

Determine whether a recovered completion using the same exact attempt can still satisfy the accepted producer-provenance contract:

```text
ExecutionSubmissionRef producer state/version
historical RUNNING→ADMISSION_PENDING LINK
G_EXECUTOR_SUBMISSION exact submission+attempt binding
CURRENT/LINK/PRODUCER separation
```

Identify whether delayed start changes any required producer identity or only execution lifecycle timing.

# 13. classification

Conclude exactly one:

```text
IN_PLACE_CONTINUATION_VALID_WITH_EXISTING_PUBLIC_SOURCE
IN_PLACE_CONTINUATION_REQUIRES_BOUNDED_SOURCE_SUPPORT
IN_PLACE_CONTINUATION_FORBIDDEN_BY_CURRENT_CONTRACT
RECOVERY_CONTRACT_UNRESOLVED
```

The conclusion must include a machine-checkable rationale table for:

```text
workflow replay
attempt start
security
materialization
provider execution
evidence
Judgment
```

# 14. if bounded source support is required

Do not edit.

Identify the minimal exact production/test path set needed to implement a source-owned recovery entrypoint.

The proposed entrypoint must:

```text
target an existing exact run/attempt only
verify expected stranded shape before mutation
never call initial_ready
never create_attempt
never replay READY→RUNNING
emit EXECUTION_STARTED at most once if legal
reload authoritative state after each durable boundary
fail closed before downstream side effects on mismatch
reuse existing security/materialization/execution/evidence/Judgment owners rather than duplicating their logic
```

Provide exact path/blob/SHA for every proposed modification.

Do not propose DB-direct repair logic if a source-owned domain operation can express the transition.

# 15. recovery failure boundaries

Define mandatory STOP conditions for a later execution Task, including at minimum:

```text
WorkRun no longer RUNNING/v2
attempt no longer NOT_STARTED
execution operation count no longer zero
runtime evidence/Judgment now exists
run/attempt identity mismatch
transition_attempt start rejection
post-start authority mismatch
security admission failure
materialization ambiguity
unexpected pre-existing transient artifact
```

State whether each condition means:

```text
STOP_PRESERVE
HUMAN_REVIEW
or contract-defined terminalization
```

Do not invent a terminalization path absent current authority.

# 16. no alternate-ID escape hatch

Prove whether current contracts permit or forbid abandoning the stranded attempt and simply issuing another attempt ID.

Do not authorize it.

If a new attempt would require an explicit workflow/error transition first, identify that contract.

# 17. Git lifecycle

Before Task move require:

```text
HEAD unchanged
index empty
tracked clean
Git-visible untracked = 2 exact
```

Move current Task byte-identically:

```text
.aiassistant/tasks/active/20260913_1129_aiscc-p2-3-stranded-s1-in-place-recovery-boundary-design-1.md
→
.aiassistant/tasks/done/20260913_1129_aiscc-p2-3-stranded-s1-in-place-recovery-boundary-design-1.md
```

Final Git-visible untracked:

```text
3 exact

current Cycle
current Judgment
current done Task
```

# 18. contract review

Require exactly 36 rows:

```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_CLEAN
CURRENT_STATE_HASHES_EXACT
KNOWN_SOURCE_BASELINES_EXACT
PYTHON_EXECUTABLE_EXACT
NO_PREEXISTING_UNTRACKED
NO_PRIVATE_RUNTIME_ACCESS
NO_DB_DOCKER_ACCESS
NO_SOURCE_TEST_STATE_MUTATION
NO_GIT_WRITE
WORKFLOW_READY_RUNNING_CONTRACT_READ
EXECUTION_NOT_STARTED_RUNNING_CONTRACT_READ
EXECUTION_STARTED_EVENT_CONTRACT_READ
STOCKROOM_OWNER_CURRENT_SOURCE_READ
CAPTURE_RUNNER_CURRENT_SOURCE_READ
EXECUTION_SERVICE_CURRENT_SOURCE_READ
EXECUTION_REPOSITORY_CURRENT_SOURCE_READ
SECURITY_ADMISSION_CURRENT_SOURCE_READ
PREPARE_CAPTURE_REENTRY_SEMANTICS_IDENTIFIED
EXISTING_RUN_RECONSTRUCTION_API_INVENTORIED
EXISTING_ATTEMPT_CONTINUATION_API_INVENTORIED
WORKFLOW_REPLAY_PROHIBITION_PROVED
ATTEMPT_ID_REUSE_REQUIREMENT_PROVED
EXECUTION_STARTED_DELAYED_EMISSION_LEGALITY_CLASSIFIED
SECURITY_AFTER_DELAYED_START_LEGALITY_CLASSIFIED
MATERIALIZATION_AFTER_DELAYED_START_LEGALITY_CLASSIFIED
PROVIDER_EXECUTION_AFTER_DELAYED_START_LEGALITY_CLASSIFIED
EVIDENCE_PROVENANCE_CONTINUITY_CLASSIFIED
RUNNER_FULL_REENTRY_SAFETY_CLASSIFIED
RECOVERY_ENTRYPOINT_REQUIREMENT_CLASSIFIED
MINIMAL_SOURCE_SCOPE_IF_REQUIRED_IDENTIFIED
RECOVERY_FAILURE_BOUNDARIES_DEFINED
RECOVERY_CLASSIFICATION_EXACT
NO_EXECUTABLE_RECOVERY_PERFORMED
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
EXPORT_INTEGRITY_PASS
```

Success:

```text
36 / 36 PASS
```

# 19. success export

Root docs exactly 10:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
RECOVERY_CONTRACT_INVENTORY.md
RECOVERY_CALL_GRAPH.md
DELAYED_EXECUTION_START_ANALYSIS.md
RECOVERY_CLASSIFICATION.md
RECOVERY_SCOPE_AND_STOP_CONDITIONS.md
CONTRACT_REVIEW.md
```

Project-relative copies exactly 7:

```text
current Cycle
current Judgment
current done Task
src/aiscc/scenarios/stockroom_production.py
src/aiscc/scenarios/capture_runner.py
src/aiscc/providers/service.py
src/aiscc/persistence/repository.py
```

Success export:

```text
17 total members
16 non-self manifest rows
one top-level directory
CRC PASS
folder/archive byte equality
TASK.md == canonical done Task
```

# 20. success ceiling

```text
0036 stranded S1:
HOLD / PRESERVED

recovery contract:
DEFINED

recovery classification:
ONE EXACT VALUE

source changes:
NONE

runtime access:
NONE

runtime recovery:
NOT_EXECUTED / NOT_AUTHORIZED

P2-3:
IN_PROGRESS
```
