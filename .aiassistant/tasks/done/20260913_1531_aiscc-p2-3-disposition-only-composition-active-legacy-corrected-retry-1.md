# 작업지시서: P2-3 disposition-only composition active-legacy corrected retry

## meta

- task_id: `20260913_1531_aiscc-p2-3-disposition-only-composition-active-legacy-corrected-retry-1`
- created_at: `2026-09-13T15:31:58+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `DISPOSITION_ONLY_COMPOSITION_SOURCE_REWORK_RETRY`
- evidence_profile: `BOUNDED_SOURCE_REWORK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `86288febf1cbd94bbb0235cfc680bf6c6c8f7772`
- required_parent: `4341138dde5fbea487f10a8af256f78c5dcf37f3`
- required_grandparent: `5affe61f02994f219b22ca934b5e0b93bc5e6f60`
- python_executable: `C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe`
- failed_1520_delivery_zip_sha256: `a7620b288702c5ce4387a2b294a59440c0e18ee2c61273f420e8de7a50ae4daa`
- source_test_write_authorized: `Yes / exact two paths`
- private_runtime_access_authorized: `No`
- runtime_disposition_authorized: `No`
- success_ceiling: `DISPOSITION_ONLY_COMPOSITION_CANDIDATE_COMPLETE / BROWSER_REVIEW_PENDING`

# 0. purpose

Retry the exact source rework after correcting only the 1520 active-task exclusivity defect.

1520 performed no source/test/runtime work.

The old 1400 active Task is a non-owned historical active artifact and must remain untouched.

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

Do not alter either existing active Task during bootstrap.

Place this new Task at:

```text
.aiassistant/tasks/active/20260913_1531_aiscc-p2-3-disposition-only-composition-active-legacy-corrected-retry-1.md
```

Then place:

```text
.aiassistant/records/aiscc/cycles/20260913_1531_aiscc-p2-3-disposition-composition-active-legacy-corrected-entry-1.cycle.md
SHA-256 ebc31620dfdd530930ba6c939b53840a1c08f67fcf660b888d88c745d97f1eae

.aiassistant/reports/aiscc/20260913_1531_aiscc-p2-3-1520-active-legacy-baseline-mismatch-retry-judgment-1.md
SHA-256 85786b83189f5fc6c8173a61500fa12692a68a9bfef3287d8884d7666013ad73
```

Archive/hash/bootstrap mismatch:

```text
STOP
no source/test write
no runtime access
no report/export
```

# 2. corrected repository and active baseline

Require:

```text
branch main
HEAD 86288febf1cbd94bbb0235cfc680bf6c6c8f7772
HEAD^ 4341138dde5fbea487f10a8af256f78c5dcf37f3
HEAD^^ 5affe61f02994f219b22ca934b5e0b93bc5e6f60
index empty
tracked clean
```

Before current Cycle/Judgment placement, Git-visible untracked exactly 11:

- `.aiassistant/tasks/done/20260913_1406_aiscc-p2-3-private-s1-invalid-history-disposition-execution-1.md`  `20d611ac457a9db0a95d331a482123022629fbc80e1c9bc5f307db3ab43115d3`
- `.aiassistant/records/aiscc/cycles/20260913_1406_aiscc-p2-3-private-s1-invalid-history-disposition-execution-entry-1.cycle.md`  `6acf1ab71a82dc16090c14d8b6bf5d4ad4dd46456729ab657afb26d580f86d2e`
- `.aiassistant/reports/aiscc/20260913_1406_aiscc-p2-3-private-s1-invalid-history-disposition-execution-authorization-judgment-1.md`  `c10465e987246d7932a665e2c763c69de7711cba6dafb438e6239e0c02866087`
- `.aiassistant/tasks/done/20260913_1435_aiscc-p2-3-private-s1-invalid-history-disposition-root-authority-retry-1.md`  `291549aa7fb05199ac78d5adb7f8ff610d7d6311e5a4f1c24cd6bfc01d486ac7`
- `.aiassistant/records/aiscc/cycles/20260913_1435_aiscc-p2-3-private-s1-root-authority-reconstructed-disposition-retry-entry-1.cycle.md`  `e944e78cddea422c1f8f586d2eb307bf4ab160c6c80862d645e5c14cebe9e5c2`
- `.aiassistant/reports/aiscc/20260913_1435_aiscc-p2-3-private-s1-root-authority-transport-gap-retry-judgment-1.md`  `bfd93a83bd7c7b688f940e0a27f3e4c3f56bae3edb13492de9d25138a80df9c7`
- `.aiassistant/tasks/done/20260913_1511_aiscc-p2-3-disposition-only-composition-entrypoint-source-rework-1.md`  `241f6c9cad0190457455cdfd1d42083045a07499957c1d6c2456a8b92c997535`
- `.aiassistant/records/aiscc/cycles/20260913_1511_aiscc-p2-3-disposition-builder-conflict-source-rework-entry-1.cycle.md`  `a7ed737a6739e812f7266f08a30c9d06f787fb70d6385f1dad3b703447c95cba`
- `.aiassistant/reports/aiscc/20260913_1511_aiscc-p2-3-full-builder-retained-root-conflict-rework-judgment-1.md`  `284775b7e4aa18fc6d1eac8ecf58ae166a61b55209b92f64fe008f55cf9eb854`
- `.aiassistant/records/aiscc/cycles/20260913_1520_aiscc-p2-3-disposition-composition-transport-baseline-corrected-entry-1.cycle.md`  `acdcef07b9bd8bfdd79438b2a35e27488cef2b32415dfda671558130bc790260`
- `.aiassistant/reports/aiscc/20260913_1520_aiscc-p2-3-1511-transport-baseline-mismatch-retry-judgment-1.md`  `26c95d5758c58f8576534e642bdc6c2a9f0595de02903a29181b995e80301c5e`

Require non-owned legacy active Task exactly:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
SHA-256 52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

Require failed owned 1520 active Task exactly:

```text
.aiassistant/tasks/active/20260913_1520_aiscc-p2-3-disposition-only-composition-entrypoint-transport-corrected-retry-1.md
SHA-256 1a282d0b9df9be3122dd12c461d50c6b189f69bf1ba276a448e269785397ea82
```

Require its done twin absent:

```text
.aiassistant/tasks/done/20260913_1520_aiscc-p2-3-disposition-only-composition-entrypoint-transport-corrected-retry-1.md
```

Do not require the active directory to contain only these Tasks.

If any additional active Task exists:

```text
record path only
do not mutate it
do not fail merely because it exists
```

Only a hash/path mismatch for the explicitly owned or explicitly preserved Tasks is a blocker.

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

After current Cycle/Judgment placement:

```text
Git-visible untracked:
13 exact
```

# 3. active ownership rule

The current track owns only:

```text
failed 1520 Task lifecycle
current 1531 Task lifecycle
```

It does not own:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
```

Do not move/delete/rewrite the 1400 Task.

Before source/test modification, move only:

```text
.aiassistant/tasks/active/20260913_1520_aiscc-p2-3-disposition-only-composition-entrypoint-transport-corrected-retry-1.md
→
.aiassistant/tasks/done/20260913_1520_aiscc-p2-3-disposition-only-composition-entrypoint-transport-corrected-retry-1.md
```

Require SHA unchanged:

```text
1a282d0b9df9be3122dd12c461d50c6b189f69bf1ba276a448e269785397ea82
```

After this move:

```text
Git-visible untracked:
14 exact
```

Re-verify the legacy 1400 active Task still exists with exact SHA.

Do not assert active-directory exclusivity.

# 4. exact write scope

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

A required third tracked path means:

```text
UNAUTHORIZED_SCOPE_REQUIRED
→ STOP before write
```

# 5. mandatory source reproduction

Read current source completely and prove:

```text
build_stockroom_production_application
→ constructs StockroomWorkspace
→ constructs DockerRuntime
→ returns full StockroomProductionApplication
```

Prove `StockroomWorkspace` retains its empty-root invariant.

Prove `StockroomInvalidHistoryDisposition` needs only:

```text
session_factory
PostgresExecutionRepository
WorkflowKernel
P1_4GuardAuthority
StockroomRestartSafetySettlement
requester_identity
clock
```

Prove existing integration disposition tests manually compose those same minimal authorities.

Mismatch → STOP before write.

# 6. dedicated public entrypoint

Add in `src/aiscc/scenarios/stockroom_production.py` exactly one public async function:

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

No Docker/image/provider/secret/execution-runner arguments.

# 7. exact minimal composition

Construct exactly the disposition authorities:

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

Return one `StockroomInvalidHistoryDisposition` with those owners, requester identity and `clock or UTC-now`.

Require non-empty requester identity and the same fixed production repository-root boundary.

# 8. strict negative composition boundary

The dedicated builder must not instantiate/call/register:

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

No Docker/image resolution.
No evidence/human/Judgment registration.
No filesystem mutation during builder construction.

# 9. preserve normal production invariants

Do not relax or bypass:

```text
StockroomWorkspace empty-root requirement
full build_stockroom_production_application composition
normal capture execution path
```

Do not add flags such as `allow_nonempty_root`, `disposition_mode`, or `skip_workspace_check`.

# 10. PostgreSQL-backed nonempty-root test

Modify only the authorized integration test and add one isolated PostgreSQL test that proves:

```text
temporary repo/.git + downloads + nonempty runtime root
exact synthetic invalid-history DB state
attempt-scoped materialized files exist
authority table counts recorded
dedicated builder returns StockroomInvalidHistoryDisposition
authority counts unchanged
runtime-root bytes unchanged by builder construction
```

# 11. synthetic complete disposition via new builder

With isolated DB/temp root only:

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
EXECUTION_STARTED 0
execution operations 0
execution outputs/submission 0
runtime evidence 0
Judgment 0
new run/attempt 0
```

# 12. partial-retry regressions

Preserve/pass:

```text
attempt-aborted-only
attempt+WorkRun-terminal/workspace-active
already-quarantined truthful repeat
mismatch fail closed
```

# 13. isolated PostgreSQL

Use only fresh test PostgreSQL:

```text
image sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94
database/role aiscc_test
localhost-only Docker-assigned ephemeral port
fresh ephemeral credential
Task-local ephemeral storage
migration head 20260901_0008
```

Never access retained private S1 resources.

# 14. validation

Run:

```text
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m py_compile src/aiscc/scenarios/stockroom_production.py tests/integration/scenarios/test_stockroom_capture_runner.py
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -m ruff check src/aiscc/scenarios/stockroom_production.py tests/integration/scenarios/test_stockroom_capture_runner.py
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q tests/integration/scenarios/test_stockroom_capture_runner.py
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q tests/integration/providers/test_execution_persistence.py
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q tests/integration/providers/test_workflow_handoff.py
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q tests/unit
git diff --check
```

Expected retained baselines:

```text
provider persistence 24/24
workflow handoff 3/3
unit 745 passed / 3 host-conditional skipped / 0 failed
scenario expected normal count 57/57
```

Record actual counts.

# 15. no private runtime

Do not access retained:

```text
private PostgreSQL/container/volume
private password
private runtime root
0036 rows/workspace
```

No real disposition.

# 16. final Git and active boundary

Before current Task move require:

```text
HEAD unchanged
index empty

modified tracked exactly:
src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_capture_runner.py

canonical state unchanged

Git-visible untracked:
14 exact
```

Re-verify legacy 1400 Task exact path/hash and leave it active.

Move only current 1531 Task byte-identically active→done.

Final:

```text
Git-visible untracked:
15 exact

current-track lineage:
1406 triple
1435 triple
1511 triple
1520 triple
1531 triple

legacy 1400 active Task:
still present / unchanged / non-owned
```

Do not move any other active Task.

No Git stage/commit/push/reset/restore/checkout/stash/clean.

# 17. contract review

Require exactly 57 rows:

```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_CLEAN
PRE_DELIVERY_UNTRACKED_11_EXACT
LEGACY_1400_ACTIVE_TASK_EXACT
FAILED_1520_ACTIVE_TASK_EXACT
FAILED_1520_DONE_TWIN_ABSENT
CURRENT_STATE_HASHES_EXACT
WRITE_PATH_BASELINES_EXACT
READ_ONLY_SOURCE_BASELINES_EXACT
PYTHON_EXECUTABLE_EXACT
NO_PRIVATE_RUNTIME_ACCESS
NO_DB_DOCKER_ACCESS
CURRENT_CYCLE_JUDGMENT_PLACED_EXACT
POST_CURRENT_PLACEMENT_UNTRACKED_13_EXACT
LEGACY_1400_ACTIVE_PRESERVED_UNCHANGED
FAILED_1520_ACTIVE_TO_DONE_BYTE_EXACT
POST_1520_CLOSURE_UNTRACKED_14_EXACT
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
FINAL_UNTRACKED_15_EXACT
FINAL_LEGACY_1400_ACTIVE_PRESERVED
EXPORT_INTEGRITY_PASS
```

Success:

```text
57 / 57 PASS
```

# 18. success export

Root docs exactly 13:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
ACTIVE_TASK_OWNERSHIP_VERIFICATION.md
TRANSPORT_BASELINE_CORRECTION.md
BUILDER_CONFLICT_VERIFICATION.md
DEDICATED_COMPOSITION_VERIFICATION.md
NEGATIVE_COMPOSITION_BOUNDARY.md
NONEMPTY_ROOT_INTEGRATION_VERIFICATION.md
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
18 total members
17 non-self manifest rows
one top-level directory
CRC PASS
folder/archive byte equality
TASK.md == canonical done Task
```

Do not include the non-owned legacy 1400 Task in the export.

# 19. success ceiling

```text
1520:
CLOSED / ACTIVE_TASK_EXCLUSIVITY_DEFECT

disposition-only composition:
CANDIDATE_COMPLETE

full production builder:
UNCHANGED

StockroomWorkspace empty-root invariant:
PRESERVED

legacy 1400 active:
PRESERVED / NON-OWNED

retained 0036 S1:
HOLD / UNTOUCHED

private disposition:
NOT_EXECUTED

Browser acceptance:
PENDING

Git persistence:
NOT_PERFORMED

P2-3:
IN_PROGRESS
```
