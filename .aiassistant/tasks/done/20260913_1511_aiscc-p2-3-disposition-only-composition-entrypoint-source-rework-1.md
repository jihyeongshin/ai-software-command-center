# 작업지시서: P2-3 disposition-only composition entrypoint source rework

## meta

- task_id: `20260913_1511_aiscc-p2-3-disposition-only-composition-entrypoint-source-rework-1`
- created_at: `2026-09-13T15:11:18+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `DISPOSITION_ONLY_COMPOSITION_SOURCE_REWORK`
- evidence_profile: `BOUNDED_SOURCE_REWORK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `86288febf1cbd94bbb0235cfc680bf6c6c8f7772`
- required_parent: `4341138dde5fbea487f10a8af256f78c5dcf37f3`
- required_grandparent: `5affe61f02994f219b22ca934b5e0b93bc5e6f60`
- python_executable: `C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe`
- predecessor_1435_result_zip_sha256: `8c4fdb3ca1494262071d39289301be6ead50b7c47624d8e3c1786a647e839350`
- source_test_write_authorized: `Yes / exact two paths`
- private_runtime_access_authorized: `No`
- runtime_disposition_authorized: `No`
- success_ceiling: `DISPOSITION_ONLY_COMPOSITION_CANDIDATE_COMPLETE / BROWSER_REVIEW_PENDING`

# 0. purpose

Fix only the composition defect discovered by 1435.

1435 proved:

```text
private root authority reconstruction:
PASS

private DB preflight:
PASS

workspace preflight:
PASS

runtime mutation:
NONE

full production builder:
fails before application return because retained root is nonempty
```

The retained root must stay nonempty.

Do not weaken the execution-workspace empty-root invariant.

Instead add a source-owned disposition-only builder that constructs only `StockroomInvalidHistoryDisposition` and its
minimal durable dependencies.

# 1. transport / Python

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
.aiassistant/tasks/active/20260913_1511_aiscc-p2-3-disposition-only-composition-entrypoint-source-rework-1.md
```

Then place:

```text
.aiassistant/records/aiscc/cycles/20260913_1511_aiscc-p2-3-disposition-builder-conflict-source-rework-entry-1.cycle.md
SHA-256 a7ed737a6739e812f7266f08a30c9d06f787fb70d6385f1dad3b703447c95cba

.aiassistant/reports/aiscc/20260913_1511_aiscc-p2-3-full-builder-retained-root-conflict-rework-judgment-1.md
SHA-256 284775b7e4aa18fc6d1eac8ecf58ae166a61b55209b92f64fe008f55cf9eb854
```

Bootstrap mismatch:

```text
STOP
no source/test write
no runtime/DB/Docker access
no report/export
```

# 2. repository baseline

Require:

```text
branch main
HEAD 86288febf1cbd94bbb0235cfc680bf6c6c8f7772
HEAD^ 4341138dde5fbea487f10a8af256f78c5dcf37f3
HEAD^^ 5affe61f02994f219b22ca934b5e0b93bc5e6f60
index empty
tracked clean
```

Before current delivery Git-visible untracked exactly three:

- `.aiassistant/tasks/done/20260913_1435_aiscc-p2-3-private-s1-invalid-history-disposition-root-authority-retry-1.md`  `291549aa7fb05199ac78d5adb7f8ff610d7d6311e5a4f1c24cd6bfc01d486ac7`
- `.aiassistant/records/aiscc/cycles/20260913_1435_aiscc-p2-3-private-s1-root-authority-reconstructed-disposition-retry-entry-1.cycle.md`  `e944e78cddea422c1f8f586d2eb307bf4ab160c6c80862d645e5c14cebe9e5c2`
- `.aiassistant/reports/aiscc/20260913_1435_aiscc-p2-3-private-s1-root-authority-transport-gap-retry-judgment-1.md`  `bfd93a83bd7c7b688f940e0a27f3e4c3f56bae3edb13492de9d25138a80df9c7`

Canonical state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `b551c534dcf55a3e5e20c4cb379cf1957ba8f719f1bb6d75c980ce5de7cd6283`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `551d0df4a5ad14a4fd825057f18d95d157b8fefb3a9821d26ef92fc2664ce74a`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `36687e0653375ca3c3ea4daf6393ced5a1856e1c70f5822408002322a964da24`

Exact write-path baselines:

- `src/aiscc/scenarios/stockroom_production.py`  `abbe7f81840de7d9525900511f967512c72cf114104128501c681c19fbacd127`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`  `0f6c21edec2b70695a3727148e47143559aa2dc65b07058c6a8d59a18ee22fb6`

Exact read-only source baselines:

- `src/aiscc/runtime/stockroom_workspace.py`  `1b8366b5c5a6e9054dbd65ef36cd09808074c88ccf6c7ad060a9a76a488efaab`
- `src/aiscc/persistence/repository.py`  `57dac018f6505468d62588761825025776d07384947424dad37b63f9f35e5e54`
- `src/aiscc/bootstrap.py`  `745b58da26ec300286ed69d1a7477b21afeb7625ec43e7f422560a657bc1c115`

After current Cycle/Judgment placement while Task is active/ignored:

```text
Git-visible untracked = 5 exact
```

# 3. exact write scope

May modify exactly:

```text
src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Do not modify:

```text
src/aiscc/runtime/stockroom_workspace.py
src/aiscc/persistence/repository.py
src/aiscc/bootstrap.py
workflow matrix/guards
rules
schema/migrations
canonical state
```

If a third tracked path is genuinely required:

```text
UNAUTHORIZED_SCOPE_REQUIRED
→ STOP before that write
```

# 4. mandatory source reproduction before edit

Read completely the relevant current source and mechanically prove:

```text
build_stockroom_production_application
→ always constructs StockroomWorkspace
→ then constructs DockerRuntime
→ only then returns StockroomProductionApplication
```

Prove `StockroomWorkspace` still enforces the empty-root invariant.

Prove `StockroomProductionApplication.invalid_history_disposition_service()` itself only needs:

```text
session_factory
PostgresExecutionRepository
WorkflowKernel
P1_4GuardAuthority
StockroomRestartSafetySettlement
requester_identity
clock
```

Also prove the existing integration invalid-history test manually composes:

```text
P1_4GuardAuthority
PostgresTransitionRepository(factory, TransitionEvaluator(guard))
WorkflowKernel
PostgresExecutionRepository
StockroomRestartSafetySettlement
StockroomInvalidHistoryDisposition
```

Any mismatch:

```text
SOURCE_BASELINE_MISMATCH
→ STOP before write
```

# 5. dedicated public composition entrypoint

In:

```text
src/aiscc/scenarios/stockroom_production.py
```

add exactly one new public async function:

```text
build_stockroom_invalid_history_disposition
```

Required signature:

```text
async def build_stockroom_invalid_history_disposition(
    *,
    session_factory: async_sessionmaker[AsyncSession],
    repository_root: Path,
    private_runtime_root: Path,
    downloads_root: Path,
    requester_identity: str,
    clock: Callable[[], datetime] | None = None,
) -> StockroomInvalidHistoryDisposition:
```

Do not add Docker/image/provider/secret/execution-runner arguments.

# 6. dedicated builder boundaries

The dedicated function must:

1. Require non-empty `requester_identity`.

2. Resolve `repository_root` and require the same fixed production repository root boundary used by the full production
builder.

3. Construct exactly:

```text
p1_4 = P1_4GuardAuthority()

transition_repository = PostgresTransitionRepository(
    session_factory,
    TransitionEvaluator(p1_4),
)

workflow_kernel = WorkflowKernel(transition_repository)

execution_repository = PostgresExecutionRepository(session_factory)

workspace_settlement = StockroomRestartSafetySettlement(
    private_runtime_root,
    repository_root=root,
    source_object_root=root / ".git",
    downloads_root=downloads_root,
)
```

4. Return exactly one:

```text
StockroomInvalidHistoryDisposition(
    session_factory=session_factory,
    execution_repository=execution_repository,
    workflow_kernel=workflow_kernel,
    guard_authority=p1_4,
    workspace_settlement=workspace_settlement,
    requester_identity=requester_identity,
    clock=clock or UTC-now production clock,
)
```

# 7. strict negative composition boundary

The new function must not instantiate, call, register or construct:

```text
StockroomWorkspace
StockroomDockerRunner
DockerRuntime
LocalDeterministicProvider
ProviderToolResourceAuthority
SecretUseAuthority
SecretResolutionLeaseAuthority
LeaseBoundSecretResolver
ExecutionReferenceAuthority
EvidenceAdmissionService
PostgresEvidenceRepository
PostgresHumanAuthorityRepository
JudgmentPolicyAuthority
PostgresJudgmentAuthority
CommandCenterAuthority
build_stockroom_production_composition
prepare_capture
StockroomCaptureRunner
AgentExecutionService
```

No evidence/human/Judgment authority registration.

No Docker/image resolution.

No filesystem mutation during builder construction; only `StockroomRestartSafetySettlement` construction is allowed.

# 8. full builder invariants stay unchanged

Do not relax or conditionalize:

```text
StockroomWorkspace empty-root requirement
full build_stockroom_production_application composition
normal capture execution path
```

The existing full production builder must retain its current semantics.

Do not add a flag such as:

```text
allow_nonempty_root
disposition_mode
skip_workspace_check
```

to `StockroomWorkspace` or the full builder.

# 9. integration test: nonempty retained root

Modify:

```text
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Add one PostgreSQL-backed test proving the new dedicated function works with a nonempty retained-style root.

The test must:

```text
create isolated temporary repository/.git, downloads and runtime root
create the exact synthetic invalid-history DB shape:
  WorkRun RUNNING/v2
  attempt NOT_STARTED/v1 causal READY/v1
create exact attempt-scoped materialized files under runtime root
confirm runtime root is nonempty before builder call
capture relevant evidence/judgment authority table counts
call build_stockroom_invalid_history_disposition exactly once
confirm builder returns StockroomInvalidHistoryDisposition
confirm authority registration table counts unchanged
confirm runtime root/materialized bytes unchanged by builder construction
```

# 10. test strict composition isolation

Mechanically/behaviorally prove the new builder does not construct the normal execution workspace stack.

At minimum:

```text
no StockroomWorkspace instance
no DockerRuntime
no StockroomDockerRunner
no provider/tool execution owner
no evidence/human/Judgment owner registration
```

Use source/AST evidence and test-visible effects.

Do not depend only on implementation naming.

# 11. synthetic complete disposition using new builder

Using only the isolated PostgreSQL/temp root, invoke:

```text
service = await build_stockroom_invalid_history_disposition(...)
request = await service.authorize(...)
result = await service.dispose(request)
```

Prove:

```text
attempt NOT_STARTED/v1 → EXECUTION_FAILED/v2
WorkRun RUNNING/v2 → FAILED/v3
workspace → QUARANTINED
EXECUTION_STARTED events 0
execution operations 0
execution outputs/submission 0
runtime evidence 0
Judgment 0
new run/attempt 0
```

# 12. partial-retry regression

Existing source-owned partial retry tests must continue to pass:

```text
attempt-aborted-only
attempt+WorkRun-terminal/workspace-active
already-quarantined truthful repeat
mismatch fail closed
```

Do not broaden idempotency or retry semantics.

# 13. isolated PostgreSQL

Use a fresh isolated test PostgreSQL only.

Accepted local image:

```text
sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94
```

Use:

```text
localhost-only Docker-assigned ephemeral port
database aiscc_test
role aiscc_test
fresh ephemeral password
Task-local ephemeral storage
```

Use repository-owned Alembic and require:

```text
migration head 20260901_0008
```

Do not access any retained private S1 container/volume/password/root/rows.

Remove only Task-created isolated test resources after validation.

# 14. validation

Run at minimum:

```text
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m py_compile
  src/aiscc/scenarios/stockroom_production.py
  tests/integration/scenarios/test_stockroom_capture_runner.py

"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -m ruff check
  src/aiscc/scenarios/stockroom_production.py
  tests/integration/scenarios/test_stockroom_capture_runner.py

"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q tests/integration/scenarios/test_stockroom_capture_runner.py
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q tests/integration/providers/test_execution_persistence.py
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q tests/integration/providers/test_workflow_handoff.py
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q tests/unit

git diff --check
```

Expected accepted regression baselines:

```text
provider persistence:
24 / 24 PASS

workflow handoff:
3 / 3 PASS

full unit:
745 passed / 3 host-conditional skipped / 0 failed
```

Scenario suite must have no required PostgreSQL skip and all discovered cases must pass. Record exact new count; one new test
is expected, so `57 / 57` is the expected normal result.

# 15. no private runtime

This source Task must not inspect or access:

```text
aiscc-p2-3-private-postgres-v1
aiscc-p2-3-private-postgres-data-v1
aiscc_private_capture
private password file
private runtime root
0036 workspace
0036 rows
```

No private disposition attempt.

# 16. final Git boundary

Require before Task move:

```text
HEAD unchanged
index empty
modified tracked exactly:
  src/aiscc/scenarios/stockroom_production.py
  tests/integration/scenarios/test_stockroom_capture_runner.py

canonical state unchanged
Git-visible untracked = 5 exact
```

Move current Task byte-identically active→done.

Final Git-visible untracked:

```text
6 exact

1435 Task/Cycle/Judgment
current Task/Cycle/Judgment
```

No git add/commit/push/reset/restore/checkout/stash/clean.

# 17. contract review

Require exactly 48 rows:

```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_CLEAN
PREDECESSOR_1435_ARTIFACTS_EXACT
CURRENT_STATE_HASHES_EXACT
WRITE_PATH_BASELINES_EXACT
READ_ONLY_SOURCE_BASELINES_EXACT
PYTHON_EXECUTABLE_EXACT
PRE_DELIVERY_UNTRACKED_3_EXACT
NO_PRIVATE_RUNTIME_ACCESS
NO_DB_DOCKER_ACCESS
FULL_BUILDER_NONEMPTY_ROOT_CONFLICT_REPRODUCED_STATIC
STOCKROOM_WORKSPACE_EMPTY_ROOT_INVARIANT_PRESERVED
MINIMAL_DISPOSITION_DEPENDENCIES_PROVED
DEDICATED_ENTRYPOINT_SYMBOL_EXACT
DEDICATED_ENTRYPOINT_SIGNATURE_EXACT
DEDICATED_ENTRYPOINT_FIXED_REPOSITORY_ROOT_BOUNDARY
DEDICATED_ENTRYPOINT_REQUESTER_REQUIRED
DEDICATED_ENTRYPOINT_NO_STOCKROOM_WORKSPACE
DEDICATED_ENTRYPOINT_NO_DOCKER_RUNTIME
DEDICATED_ENTRYPOINT_NO_PROVIDER_TOOL_STACK
DEDICATED_ENTRYPOINT_NO_EVIDENCE_AUTHORITY_REGISTRATION
DEDICATED_ENTRYPOINT_NO_HUMAN_AUTHORITY
DEDICATED_ENTRYPOINT_NO_JUDGMENT_AUTHORITY
DEDICATED_ENTRYPOINT_P1_4_GUARD_EXACT
DEDICATED_ENTRYPOINT_TRANSITION_REPOSITORY_EXACT
DEDICATED_ENTRYPOINT_WORKFLOW_KERNEL_EXACT
DEDICATED_ENTRYPOINT_EXECUTION_REPOSITORY_EXACT
DEDICATED_ENTRYPOINT_RESTART_SETTLEMENT_EXACT
DEDICATED_ENTRYPOINT_RETURNS_SOURCE_OWNER_EXACT
FULL_PRODUCTION_BUILDER_UNCHANGED_SEMANTIC
NONEMPTY_ROOT_DISPOSITION_BUILDER_TEST_PASS
DISPOSITION_BUILDER_DB_ZERO_REGISTRATION_DELTA
DISPOSITION_SYNTHETIC_COMPLETE_PATH_PASS
DISPOSITION_PARTIAL_RETRY_PATHS_PASS
DISPOSITION_NO_PROVIDER_EVIDENCE_JUDGMENT_PASS
SCENARIO_INTEGRATION_SUITE_PASS
PROVIDER_PERSISTENCE_REGRESSION_24_PASS
WORKFLOW_HANDOFF_REGRESSION_PASS
FULL_UNIT_745_PASS
RUFF_PASS
PY_COMPILE_PASS
GIT_DIFF_CHECK_PASS
MODIFIED_PATHS_EXACT_2
NO_UNAUTHORIZED_PATH_MUTATION
CANONICAL_STATE_UNCHANGED
NO_GIT_COMMIT_PUSH
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
EXPORT_INTEGRITY_PASS
```

Success requires:

```text
48 / 48 PASS
```

# 18. success export

Root docs exactly 12:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
BUILDER_CONFLICT_VERIFICATION.md
DEDICATED_COMPOSITION_VERIFICATION.md
NEGATIVE_COMPOSITION_BOUNDARY.md
NONEMPTY_ROOT_INTEGRATION_VERIFICATION.md
DISPOSITION_INTEGRATION_VERIFICATION.md
TEST_VERIFICATION.md
GIT_DIFF_VERIFICATION.md
CONTRACT_REVIEW.md
```

Project-relative copies exactly 5:

```text
current Cycle
current Judgment
current done Task
src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_capture_runner.py
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

# 19. success ceiling

```text
disposition-only composition:
CANDIDATE_COMPLETE

full production builder:
UNCHANGED

execution workspace empty-root invariant:
PRESERVED

retained 0036 S1:
HOLD / UNTOUCHED

private runtime disposition:
NOT_EXECUTED

Browser acceptance:
PENDING

Git persistence:
NOT_PERFORMED

P2-3:
IN_PROGRESS
```
