# 작업지시서: P2-3 stranded S1 recovery boundary corrected-design retry

## meta

- task_id: `20260913_1208_aiscc-p2-3-stranded-s1-recovery-boundary-corrected-design-retry-1`
- created_at: `2026-09-13T12:08:23+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `PRIVATE_S1_RECOVERY_DESIGN_RETRY`
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
- accepted_0036_result_zip_sha256: `041285052e8fad97636231be69775e0dd7003b3d1b1683b64200cdc931eb0ac5`
- accepted_0115_result_zip_sha256: `14007a21c9adeefc33459eb4d8fd7a2bb274e97e4578ceb59c56bd4523db9838`
- predecessor_1129_result_zip_sha256: `67df0287da57861102e0f86614047249b84a38951df8dfff33670c5734836bd5`
- success_ceiling: `STRANDED_S1_RECOVERY_BOUNDARY_DEFINED / EXECUTION_NOT_AUTHORIZED`

# 0. purpose

Repeat the stranded-S1 recovery design using the corrected accepted factual baseline.

The Browser-issued 1129 statement that security/materialization never began was wrong.

Accepted exact 0036 operation trace:

```text
INITIAL_READY:
ADMITTED / READY v1

CREATE_ATTEMPT:
ADMITTED / NOT_STARTED / READY v1

READY_TO_RUNNING:
ADMITTED / RUNNING v2

SEAL_CONTEXT:
ADMITTED / RUNNING v2

AUTHORIZE_RUNTIME:
ADMITTED / RUNNING v2

MATERIALIZE:
ADMITTED / RUNNING v2

EXECUTE:
UNKNOWN / execution:NOT_STARTED / RUNNING v2
```

Accepted durable state:

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

Do not interpret `MATERIALIZE: ADMITTED` as proof that artifacts are presently available or durable.
Prove those semantics from source.

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
.aiassistant/tasks/active/20260913_1208_aiscc-p2-3-stranded-s1-recovery-boundary-corrected-design-retry-1.md
```

Then place:

```text
.aiassistant/records/aiscc/cycles/20260913_1208_aiscc-p2-3-stranded-s1-recovery-baseline-conflict-corrected-entry-1.cycle.md
SHA-256:
f87221fb252c6db21f5731f09c58c2393ff4eaf4002d11bba4d8053d8132b9e5

.aiassistant/reports/aiscc/20260913_1208_aiscc-p2-3-stranded-s1-recovery-baseline-conflict-correction-judgment-1.md
SHA-256:
03c66a81c212c075f5e425accd2001106bc9709ee86c9f2833d3d1f32ef1b075
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
```

Before current delivery Git-visible untracked exactly three:

- `.aiassistant/tasks/done/20260913_1129_aiscc-p2-3-stranded-s1-in-place-recovery-boundary-design-1.md`  `d01fbfa993c0e37f06a9066f9def2ca1c4af590d372eaa122a6c53dee4e29e36`
- `.aiassistant/records/aiscc/cycles/20260913_1129_aiscc-p2-3-stranded-s1-recovery-design-entry-1.cycle.md`  `02356ec126b9381248ab491b013ad8a74f90abfd8d69a50349ad9f2718dd0b50`
- `.aiassistant/reports/aiscc/20260913_1129_aiscc-p2-3-stranded-s1-recovery-design-authorization-judgment-1.md`  `4ab5b734e9802c975e51a761bd4281b7a9359df7bd140711d7e8cb3e49dd214a`

Canonical state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `550b7b3ec6659c5ad86558c84902a5319457334432db452405e31a2eb1153164`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `c9496a814cb94a834f53c4dee46032836dfaa4f8490d433a5909c0e46d2e3c3f`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `a6130f00deb41a1cae8c42cb62e7eb57d3457e40775794c6efb725fb604c832e`

Known source baselines:

- `src/aiscc/scenarios/stockroom_production.py`  `c070e194b5d3e0ca18d952202f71860175ab36f3a51b327c7799fe5ef36bffb3`
- `src/aiscc/scenarios/capture_runner.py`  `0dab27e0ce9ce2da7953188bcb26f288b637a4ba524141be2800b08302a59b18`
- `src/aiscc/providers/service.py`  `f21c3c29443446650e31fb0d4d0d30ceddb8956d51ad2e17221536102c6c5c18`
- `src/aiscc/persistence/repository.py`  `ab00af3dd871477da74b83275258aa48a47ba9a7081aad0154a808b6e4f1c089`
- `src/aiscc/workflow/guards.py`  `e7509199bca3b901c7a04b4e5a1d8c23bab217eca5b78a3b9319d10300993cab`

After current Cycle/Judgment placement while current Task remains active/ignored:

```text
Git-visible untracked:
5 exact

1129 Task/Cycle/Judgment
current Cycle/Judgment
```

Unexpected path/dirt:

```text
DIRTY_WORKSPACE_MIXED
→ STOP_WITH_REPORT_EXPORT
```

# 3. strict runtime prohibition

Do not access:

```text
Docker
retained PostgreSQL
private password file
private runtime root
0036 WorkRun/attempt rows
materialized filesystem content
provider/tool runtime
network runtime
```

Do not execute:

```text
build_stockroom_production
prepare_capture
runner
transition_attempt
request_transition
security operations
materialization
provider/tool execution
evidence operations
Judgment
```

This Task is source/contract analysis only.

# 4. authority precedence

Use accepted runtime/governance facts in this order:

```text
1. persisted canonical current state at HEAD
2. accepted 0036 source-owned runtime trace/result
3. accepted 0115 diagnosis
4. current corrected Cycle/Judgment
```

The blocked 1129 statement that downstream work never began is superseded by this corrected authority.

Do not stop again on that same conflict.

If another distinct contradiction is found, identify exact documents/statements and STOP.

# 5. complete governance contract reads

Read current tracked rules governing:

```text
WorkflowState / transition replay
G_EXECUTION_STARTED
ExecutionStatus lifecycle
same-attempt semantics
unknown outcome/retry
security seal and capability authority
runtime materialization authority
execution provider/tool dispatch
evidence producer provenance
Judgment prerequisites
```

At minimum read current:

```text
AISCC_ORCHESTRATION
AISCC_PROVIDER_TOOL_EXECUTION
AISCC_SECURITY_SANDBOX
AISCC_EVIDENCE_ADMISSION
AISCC_HUMAN_GATE_JUDGMENT
```

Record path + whole SHA-256.

# 6. complete current source reads

Read completely:

```text
src/aiscc/scenarios/stockroom_production.py
src/aiscc/scenarios/capture_runner.py
src/aiscc/providers/service.py
src/aiscc/persistence/repository.py
src/aiscc/workflow/guards.py
```

Discover and completely read directly required production modules owning:

```text
security context sealing
runtime capability issuance
materializer/materialization handle
execution input preparation
ExecutionReferenceAuthority
execution operation creation
evidence submission
Judgment issuance
```

For every source relied upon record:

```text
path
HEAD blob
whole SHA-256
symbols used
```

# 7. consumed versus unconsumed boundaries

Mechanically classify:

```text
READY creation:
consumed

attempt creation:
consumed

READY→RUNNING workflow transition:
consumed / must not replay

security seal:
previously invoked and ADMITTED

runtime authorization:
previously invoked and ADMITTED

materialization:
previously invoked and ADMITTED

EXECUTION_STARTED durable attempt event:
not consumed

execution operation:
not created

runtime evidence:
not created

Judgment:
not created
```

For security/materialization distinguish:

```text
operation was invoked/admitted
versus
authority/artifact is durably recoverable now
```

# 8. delayed EXECUTION_STARTED legality

Determine whether current repository/domain contract allows:

```text
WorkRun already RUNNING/v2
ExecutionAttempt still NOT_STARTED
same exact run/attempt
no execution operation
```

to receive exactly one delayed:

```text
EXECUTION_STARTED
```

Prove:

```text
current status precondition
expected execution version
causal workflow state/version
run/attempt identity
task/provider/tool identity
event-ref contract
duplicate-start behavior
post-start authoritative shape
```

Classify exactly:

```text
LEGAL_EXACTLY_ONCE
FORBIDDEN
LEGAL_ONLY_WITH_BOUNDED_SOURCE_VALIDATION
UNRESOLVED
```

# 9. prior security authority semantics

Because `SEAL_CONTEXT` and `AUTHORIZE_RUNTIME` were already ADMITTED, determine:

```text
whether they created durable DB authority, in-memory owner state, deterministic recomputable state, or mixed state
whether current source has a public reconstruction/load API
whether replay for same run/attempt/RUNNING-v2 is idempotent, rejected, or unsafe
whether a recovered execution must reuse existing authority rather than issue fresh authority
whether any capability lifetime/nonce makes the old authority unusable after process loss
```

Do not assume replay is legal simply because the normal runner calls these methods.

# 10. prior materialization semantics

Because `MATERIALIZE` was already ADMITTED, trace completely:

```text
materializer_factory.materialize
execution_factory.prepare_inputs
execution_factory.derive
adapter runtime-handle storage
filesystem/runtime-root writes
any DB/reference persistence
settlement ownership
```

Determine:

```text
what exactly ADMITTED means
which outputs are durable
which outputs are process-local
whether a materialized handle can be reconstructed after process loss
whether materialization is deterministic/idempotent for same run/attempt
whether re-materialization can collide with or duplicate existing artifacts
whether an existing artifact must be inspected before any later replay
```

No filesystem/runtime inspection in this Task.

# 11. current public re-entry inventory

Inventory every production API that could reconstruct or continue the exact existing run:

```text
build_stockroom_production
prepare_capture
StockroomCaptureRunner.run
StockroomCaptureOwnerAdapter
security owner/service
materializer
AgentExecutionService.execute
repository authority readers
```

For each classify:

```text
creates/replays READY?
creates a new attempt?
replays READY→RUNNING?
re-seals security?
re-authorizes runtime?
re-materializes?
requires process-local handles?
can bind exact existing attempt?
safe recovery entrypoint as-is?
```

# 12. full runner and prepare_capture safety

Prove separately:

```text
prepare_capture(existing exact run/attempt):
SAFE / UNSAFE / UNRESOLVED

StockroomCaptureRunner.run(existing prepared object):
SAFE / UNSAFE / UNRESOLVED
```

If unsafe, identify the earliest duplicate/illegal operation.

Do not propose using them for recovery if they replay consumed boundaries.

# 13. execution continuation

Assuming for analysis only that delayed `EXECUTION_STARTED` is legal, determine what exact state is required before
`AgentExecutionService.execute` may safely create the first execution operation.

Address the already-admitted materialization:

```text
must reuse old materialized handle?
may reconstruct handle?
may rematerialize?
must inspect runtime root first?
```

Classify whether provider execution can be resumed without duplicating materialization side effects.

# 14. evidence/Judgment continuity

Determine whether same-attempt recovered execution can still create the accepted producer chain:

```text
RUNNING producer
ExecutionSubmissionRef
RUNNING→ADMISSION_PENDING historical LINK
G_EXECUTOR_SUBMISSION bound refs
ADMISSION_PENDING CURRENT
evidence admission/evaluation
Judgment
```

Prove whether prior security/materialization timing changes producer identity or only precedes delayed execution start.

# 15. recovery classification

Conclude exactly one:

```text
IN_PLACE_CONTINUATION_VALID_WITH_EXISTING_PUBLIC_SOURCE

IN_PLACE_CONTINUATION_REQUIRES_BOUNDED_SOURCE_SUPPORT

IN_PLACE_CONTINUATION_FORBIDDEN_BY_CURRENT_CONTRACT

RECOVERY_CONTRACT_UNRESOLVED
```

Provide a rationale matrix:

```text
workflow replay
execution start
security reuse/replay
materialization reuse/replay
provider execution
evidence
Judgment
```

# 16. bounded source support, if required

Do not edit source.

Identify exact minimal source/test paths required for a source-owned recovery entrypoint.

A proposed recovery entrypoint must:

```text
target exact existing run/attempt
verify expected stranded state before first mutation
never initial_ready
never create_attempt
never replay READY→RUNNING
account explicitly for already-admitted security/materialization
emit EXECUTION_STARTED at most once if legal
reload authority after every durable mutation
fail closed before provider execution on ambiguity
reuse existing domain owners instead of DB-direct mutation
preserve same-attempt provenance
```

Provide path/blob/SHA and reason for each proposed path.

# 17. required future runtime preflight

Because materialization was already ADMITTED, define what a later separately authorized execution/recovery Task must inspect
before mutation.

At minimum classify whether it must verify:

```text
WorkRun exact RUNNING/v2
attempt exact NOT_STARTED
execution_operations == 0
runtime evidence absent
Judgment absent

security authority persistence/presence
materialized artifact/runtime-root presence
materialized artifact identity/fingerprint
absence of transient running container/process
whether prior materialization output is complete or partial
```

Do not perform these observations now.

# 18. mandatory STOP conditions

Define later recovery STOP conditions at minimum:

```text
WorkRun not RUNNING/v2
attempt not NOT_STARTED
execution operation exists
evidence/Judgment exists
run/attempt mismatch
delayed start illegal/rejected
prior security authority ambiguous
prior materialization artifact ambiguous
materialization collision or partial artifact
unexpected running transient
post-start authority mismatch
provider operation ambiguity
```

Do not invent rollback/terminalization absent current source authority.

# 19. alternate-attempt question

Determine whether current contract permits abandoning this attempt and creating a new attempt.

Do not authorize it.

Identify exact prerequisite workflow/execution terminal state if current source requires one before a new attempt.

# 20. Git lifecycle

Before Task move require:

```text
HEAD unchanged
index empty
tracked clean
Git-visible untracked = 5 exact
```

Move current Task byte-identically active→done.

Final Git-visible untracked:

```text
6 exact

1129 Task/Cycle/Judgment
current Task/Cycle/Judgment
```

# 21. contract review

Require exactly 41 rows:

```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_CLEAN
PREDECESSOR_1129_ARTIFACTS_EXACT
CURRENT_STATE_HASHES_EXACT
KNOWN_SOURCE_BASELINES_EXACT
PYTHON_EXECUTABLE_EXACT
NO_PRIVATE_RUNTIME_ACCESS
NO_DB_DOCKER_ACCESS
NO_SOURCE_TEST_STATE_MUTATION
NO_GIT_WRITE
CORRECTED_0036_TRACE_ACCEPTED
SECURITY_SEAL_PREVIOUSLY_ADMITTED
RUNTIME_AUTHORIZATION_PREVIOUSLY_ADMITTED
MATERIALIZATION_PREVIOUSLY_ADMITTED
EXECUTION_OPERATION_ABSENT
EXECUTION_ATTEMPT_NOT_STARTED
WORKFLOW_READY_RUNNING_ALREADY_CONSUMED
EXECUTION_STARTED_EVENT_CONTRACT_READ
SECURITY_CONTEXT_PERSISTENCE_CLASSIFIED
RUNTIME_AUTHORIZATION_PERSISTENCE_CLASSIFIED
MATERIALIZATION_HANDLE_PERSISTENCE_CLASSIFIED
MATERIALIZATION_ARTIFACT_PERSISTENCE_CLASSIFIED
MATERIALIZATION_REPLAY_LEGALITY_CLASSIFIED
SECURITY_REPLAY_LEGALITY_CLASSIFIED
DELAYED_EXECUTION_START_LEGALITY_CLASSIFIED
EXISTING_RUN_RECONSTRUCTION_API_INVENTORIED
EXISTING_ATTEMPT_CONTINUATION_API_INVENTORIED
RUNNER_FULL_REENTRY_SAFETY_CLASSIFIED
PREPARE_CAPTURE_REENTRY_SAFETY_CLASSIFIED
RECOVERY_ENTRYPOINT_REQUIREMENT_CLASSIFIED
EXECUTION_PROVIDER_CONTINUITY_CLASSIFIED
EVIDENCE_PROVENANCE_CONTINUITY_CLASSIFIED
JUDGMENT_CONTINUITY_CLASSIFIED
ALTERNATE_ATTEMPT_LEGALITY_CLASSIFIED
MINIMAL_SOURCE_SCOPE_IF_REQUIRED_IDENTIFIED
RUNTIME_PREFLIGHT_REQUIREMENTS_DEFINED
RECOVERY_STOP_CONDITIONS_DEFINED
RECOVERY_CLASSIFICATION_EXACT
NO_EXECUTABLE_RECOVERY_PERFORMED
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
EXPORT_INTEGRITY_PASS
```

Success:

```text
41 / 41 PASS
```

# 22. success export

Root docs exactly 12:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
CORRECTED_RUNTIME_BASELINE.md
RECOVERY_CONTRACT_INVENTORY.md
SECURITY_RECOVERY_ANALYSIS.md
MATERIALIZATION_RECOVERY_ANALYSIS.md
RECOVERY_CALL_GRAPH.md
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
19 total members
18 non-self manifest rows
one top-level directory
CRC PASS
folder/archive byte equality
TASK.md == canonical done Task
```

# 23. success ceiling

```text
1129:
BLOCKED / BASELINE_CONFLICT ACKNOWLEDGED

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
