# 작업지시서: P2-3 invalid-history abort contract and disposition source rework

## meta

- task_id: `20260913_1242_aiscc-p2-3-invalid-history-abort-contract-and-disposition-source-rework-1`
- created_at: `2026-09-13T12:42:29+09:00`
- work_type: `INVALID_HISTORY_ABORT_CONTRACT_AND_SOURCE_REWORK`
- evidence_profile: `HIGH_RISK_GOVERNANCE_SOURCE`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `5affe61f02994f219b22ca934b5e0b93bc5e6f60`
- required_parent: `a4eb36611dca8d504610d9e3091950b0f32c20e7`
- required_grandparent: `6cc4f988f56f5cbf32e57f4b5e9a52a180044c36`
- python_executable: `C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe`
- accepted_1224_result_zip_sha256: `9d24bf9a9cfe2a2cd86c3c80d1f5fb2c8282c1f0373a4282ea43061efbdf0962`
- contract_write_authorized: `Yes / exact one rule path`
- source_test_write_authorized: `Yes / exact bounded eight code/test paths`
- private_runtime_access_authorized: `No`
- runtime_disposition_authorized: `No`
- success_ceiling: `INVALID_HISTORY_ABORT_CONTRACT_AND_SOURCE_CANDIDATE_COMPLETE / BROWSER_REVIEW_PENDING`

# 0. purpose

Implement a contract-valid disposition mechanism for the stranded-history class without touching the retained private S1.

Accepted current boundary:

```text
in-place continuation:
FORBIDDEN_BY_CURRENT_CONTRACT

complete disposition:
FORBIDDEN_BY_CURRENT_CONTRACT
```

The candidate adds one narrow contract edge and implements it source-first, with synthetic/isolated tests only.

# 1. Python and transport

Use only:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe
```

Forbidden: `python`, `py`, WindowsApps alias, PATH Python discovery.

Verify delivery ZIP/hash and exactly three flat safe members.

Place Task first:
```text
.aiassistant/tasks/active/20260913_1242_aiscc-p2-3-invalid-history-abort-contract-and-disposition-source-rework-1.md
```

Then place:
```text
.aiassistant/records/aiscc/cycles/20260913_1242_aiscc-p2-3-invalid-history-abort-contract-rework-entry-1.cycle.md
SHA-256 f796bdcda330aa6133e2424951e02b82cbd7399400bd87e0d1e9ffd417455980

.aiassistant/reports/aiscc/20260913_1242_aiscc-p2-3-disposition-forbidden-contract-rework-authorization-judgment-1.md
SHA-256 63efbe1860bba000a2b90b9778dcd4c721d61c75e68e61ed9439129841efa59c
```

Bootstrap mismatch → STOP with no write/runtime/report/export.

# 2. baseline

Require:

```text
branch main
HEAD 5affe61f02994f219b22ca934b5e0b93bc5e6f60
HEAD^ a4eb36611dca8d504610d9e3091950b0f32c20e7
HEAD^^ 6cc4f988f56f5cbf32e57f4b5e9a52a180044c36
index empty
tracked clean
```

Before current delivery Git-visible untracked exactly nine:

- `.aiassistant/tasks/done/20260913_1129_aiscc-p2-3-stranded-s1-in-place-recovery-boundary-design-1.md` `d01fbfa993c0e37f06a9066f9def2ca1c4af590d372eaa122a6c53dee4e29e36`
- `.aiassistant/records/aiscc/cycles/20260913_1129_aiscc-p2-3-stranded-s1-recovery-design-entry-1.cycle.md` `02356ec126b9381248ab491b013ad8a74f90abfd8d69a50349ad9f2718dd0b50`
- `.aiassistant/reports/aiscc/20260913_1129_aiscc-p2-3-stranded-s1-recovery-design-authorization-judgment-1.md` `4ab5b734e9802c975e51a761bd4281b7a9359df7bd140711d7e8cb3e49dd214a`
- `.aiassistant/tasks/done/20260913_1208_aiscc-p2-3-stranded-s1-recovery-boundary-corrected-design-retry-1.md` `899c1c650acd90fec2b2e99cf4e49ed5c5804539e57713b00fbb3462d2024e4c`
- `.aiassistant/records/aiscc/cycles/20260913_1208_aiscc-p2-3-stranded-s1-recovery-baseline-conflict-corrected-entry-1.cycle.md` `f87221fb252c6db21f5731f09c58c2393ff4eaf4002d11bba4d8053d8132b9e5`
- `.aiassistant/reports/aiscc/20260913_1208_aiscc-p2-3-stranded-s1-recovery-baseline-conflict-correction-judgment-1.md` `03c66a81c212c075f5e425accd2001106bc9709ee86c9f2833d3d1f32ef1b075`
- `.aiassistant/tasks/done/20260913_1224_aiscc-p2-3-stranded-s1-invalid-history-disposition-design-1.md` `3c05de4c825ee3e3b3c6906add1f2d2f95148f2b286c0f98b5d17fef5059b5dc`
- `.aiassistant/records/aiscc/cycles/20260913_1224_aiscc-p2-3-stranded-s1-invalid-history-disposition-entry-1.cycle.md` `a0d2658398c834550bd89e10d2cc2283422a6a60cdc424fd0fe6808c941e06d3`
- `.aiassistant/reports/aiscc/20260913_1224_aiscc-p2-3-stranded-s1-in-place-continuation-forbidden-judgment-1.md` `9587af829556be5327a4dabe63a1d46bce638f956689c551f7126d4ac0577717`

Canonical state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md` `550b7b3ec6659c5ad86558c84902a5319457334432db452405e31a2eb1153164`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md` `c9496a814cb94a834f53c4dee46032836dfaa4f8490d433a5909c0e46d2e3c3f`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md` `a6130f00deb41a1cae8c42cb62e7eb57d3457e40775794c6efb725fb604c832e`

After current Cycle/Judgment placement with Task active/ignored:

```text
Git-visible untracked = 11 exact
```

# 3. authorized path baselines

Only these nine tracked paths may change:

- `.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md`  HEAD blob `c97da85690c52a0c52ea47e233de591e58bb784a`  SHA-256 `12070677aa1cfa74b7eea9a52db24f78aacd2bf23d655f125a7689797d172443`
- `src/aiscc/providers/events.py`  HEAD blob `a6db3d6549f9ecb3a0c09323ea4aa77ca9026a04`  SHA-256 `6a3a1c227ffaf1e1178be93993ca9cc3622c33987389dd7f873d48cfd89ed461`
- `src/aiscc/persistence/repository.py`  HEAD blob `c70833a40189d687f6415625d8eff2a1443ce46e`  SHA-256 `ab00af3dd871477da74b83275258aa48a47ba9a7081aad0154a808b6e4f1c089`
- `src/aiscc/scenarios/stockroom_production.py`  HEAD blob `b0fbef4c18e7ae5bc90c139349ab9f36696b54c4`  SHA-256 `c070e194b5d3e0ca18d952202f71860175ab36f3a51b327c7799fe5ef36bffb3`
- `src/aiscc/runtime/stockroom_workspace.py`  HEAD blob `88522462dceb4b102603f4cf6960263d2fc7c430`  SHA-256 `fd6c889e518b9fec7bef425ec4ea950b430c38c86f039a62a275949416442347`
- `tests/unit/providers/test_operation_protocol.py`  HEAD blob `21297bdb90fd2bc6b534763bef324cc1620dfdf2`  SHA-256 `47c031e8ca2daf055044b67b48c5acfdf563b19fde8f24f673df91e1de0eb453`
- `tests/integration/providers/test_execution_persistence.py`  HEAD blob `a7b5ad5b3e651b9764990239fdc70e5426222629`  SHA-256 `4f0bbcadf3f0cb38f6406becbb9343cda7c2787e9e2cbef3fff60be363c9c74a`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`  HEAD blob `9f4e5404bd83099295b1d3784f3860bdfb1877a0`  SHA-256 `dca16f6ed0de608faa7f06cd4266ad377f140971536e0a82c0e92f679da73b72`
- `tests/unit/runtime/test_stockroom_workspace.py`  HEAD blob `3c18c98ec99837fc72b5187599f45ac1fbbcfa92`  SHA-256 `ce24c649664461440d4f354d0d311624e07bed840dba4f12df99fbc49dddd1ca`

Before write verify all nine exact HEAD blob + whole SHA-256 values.

Any required tenth tracked path:

```text
UNAUTHORIZED_SCOPE_REQUIRED
→ STOP before that write
```

Explicitly unauthorized unless STOP:
```text
schema/migrations
provider models
workflow matrix
workflow guards
security policy/capability
capture_runner.py
canonical state records
```

# 4. mandatory current-contract reproduction

Before write, prove from current rule/source:

```text
NOT_STARTED has no terminal/dispose edge
EXECUTION_FAILED is currently legal only after RUNNING
generic transition_attempt cannot truthfully dispose the stranded attempt
WorkRun RUNNING→FAILED exists but cannot terminalize child attempt
Stockroom has no invalid-history disposition entrypoint
old workspace lease/capability authority is process-local and not reconstructable
```

Mismatch → STOP before write.

# 5. canonical rule amendment

Modify only:

```text
.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md
```

Add one narrowly defined event:

```text
EXECUTION_ABORTED_INVALID_HISTORY
```

Exact lifecycle:

```text
from:
NOT_STARTED

to:
EXECUTION_FAILED
```

Exact allowed purpose:

```text
dispose an execution attempt whose immutable history proves an execution-side-effect occurred before EXECUTION_STARTED
```

Exact required reason code for this class:

```text
INVALID_HISTORY_SIDE_EFFECT_BEFORE_EXECUTION_START
```

Required normative preconditions:

```text
same exact WorkRun + attempt identity
attempt current status NOT_STARTED
expected execution version exact
current WorkRun RUNNING at expected state version
attempt was created from the same WorkRun lineage
zero execution operations
no execution output/submission
no admitted runtime evidence
no Judgment
trusted source-owned invalid-history provenance
no concurrent state change under lock
```

The rule must state explicitly:

```text
this is not EXECUTION_STARTED
this is not a generic cancellation edge
this is not legal merely because a timeout occurred
this is not legal after provider operation creation
this does not authorize retry
this does not authorize direct DB/projection edits
ordinary EXECUTION_FAILED from RUNNING remains unchanged
```

Audit semantics:

```text
append one typed abort event
preserve original NOT_STARTED/READY causal history in event metadata
bind current RUNNING WorkRun state/version separately
record exact reason code and immutable provenance refs
project attempt to EXECUTION_FAILED
never fabricate provider output/submission
```

Idempotency:

```text
repeating the exact same abort request against the exact already-aborted attempt returns the same authoritative terminal result without a second event
any changed reason/identity/version/provenance conflicts
```

# 6. provider event/lifecycle source

Modify:

```text
src/aiscc/providers/events.py
```

Encode the new exact event and lifecycle edge.

Existing edges must remain unchanged.

Add/extend operation protocol tests so:

```text
NOT_STARTED + EXECUTION_ABORTED_INVALID_HISTORY → EXECUTION_FAILED
NOT_STARTED + EXECUTION_FAILED → denied as before
RUNNING + EXECUTION_ABORTED_INVALID_HISTORY → denied
EXECUTION_FAILED + new abort event → denied/idempotency handled by repository owner, not generic lifecycle replay
```

# 7. dedicated repository disposition API

Modify:

```text
src/aiscc/persistence/repository.py
```

Introduce one explicit public repository operation for invalid-history abort. Use a clear typed name; report the final symbol.

Do NOT make ordinary `transition_attempt(...)` a generic entrypoint for this event.

The dedicated operation must atomically:

```text
lock exact WorkRun
lock exact attempt
reload both
verify exact run/attempt/task lineage
verify WorkRun RUNNING + expected state version
verify attempt NOT_STARTED + expected execution version
verify zero execution operations
verify no execution output/submission rows owned by this attempt where repository authority can prove this
validate exact reason/provenance payload
append exactly one EXECUTION_ABORTED_INVALID_HISTORY event
project attempt status EXECUTION_FAILED
project causal state/version to the current WorkRun RUNNING/version while preserving prior causal READY/v1 in event metadata
increment execution version exactly once
return authoritative attempt
```

Idempotent retry requirement:

```text
if already EXECUTION_FAILED because of the exact same abort event/provenance:
return authoritative result without duplicate event

if EXECUTION_FAILED for another reason, or any field differs:
AuthorityConflictError / fail closed
```

Do not delete or mutate historical rows.

# 8. source-owned Stockroom disposition entrypoint

Modify only:

```text
src/aiscc/scenarios/stockroom_production.py
```

Add one source-owned disposition entrypoint/service for an existing exact run/attempt.

It must not call:

```text
initial_ready
create_attempt
READY→RUNNING
prepare_capture
StockroomCaptureRunner.run
EXECUTION_STARTED
AgentExecutionService.execute
provider/tool dispatch
evidence admission
Judgment
```

Required durable order:

```text
A. load/verify exact invalid-history authority
B. dedicated invalid-history abort
C. reload and require attempt EXECUTION_FAILED
D. issue authentic G_FAILURE_TERMINAL with exact invalid-history failure provenance
E. request WorkRun RUNNING→FAILED
F. reload and require WorkRun FAILED
G. only after both terminal durable boundaries, perform safety settlement/quarantine
```

Partial-retry behavior must be explicit:

```text
attempt already exact-aborted + WorkRun still RUNNING:
continue at WorkRun failure only

attempt exact-aborted + WorkRun FAILED + workspace unsettled:
continue at settlement only

any nonmatching intermediate:
STOP_PRESERVE
```

No new run/attempt.

# 9. WorkRun failure provenance

Use the existing RUNNING→FAILED matrix and `G_FAILURE_TERMINAL`.

Do not change workflow matrix/guard policy.

The source-owned guard fact must be exact to:

```text
failure class:
INVALID_HISTORY_SIDE_EFFECT_BEFORE_EXECUTION_START

run_id
attempt_id
abort event identity/version
current WorkRun RUNNING version
```

Do not issue G_FAILURE_TERMINAL before the attempt is authoritatively EXECUTION_FAILED.

# 10. restart-safe workspace safety support

Modify:

```text
src/aiscc/runtime/stockroom_workspace.py
```

Current historical lease cannot be adopted/reconstructed as if it were authentic.

Add a separate restart-safe safety-settlement path with these invariants:

```text
never synthesize/adopt an old lease
never mark historical materialization CLEANED through the normal lease API
derive only the exact deterministic attempt-scoped workspace target
reject symlink/reparse escape
inventory the exact target before mutation
compute a deterministic inventory fingerprint
require caller-supplied expected identity/fingerprint from immediately preceding authorized preflight
recheck identity immediately before mutation
never recursively delete an ambiguous target
```

For an old workspace with no authentic lease, the only allowed successful disposition action is:

```text
QUARANTINED
```

Quarantine must:

```text
move/rename the exact verified attempt workspace into an isolated quarantine namespace under the authorized root
preserve its bytes for later inspection
return a structured verdict with original identity, quarantine identity, inventory fingerprint, and reason
never make the old materialized content reusable
```

If target absent:

```text
return a distinct truthful ABSENT/NO_RESOURCE verdict only if source contract already supports such a safe result;
otherwise fail closed
```

If content/ownership is ambiguous:

```text
QUARANTINE_DENIED / fail closed
```

No broad `rmtree`, prune, glob cleanup, or adoption.

# 11. security authority handling

Do not modify security policy/capability code.

The disposition path must not fabricate revocation of process-local historical capabilities that no longer exist.

Report source-level security settlement only as:

```text
no new capability issued
no old capability reconstructed
process-local authority not fabricated
WorkRun/attempt terminal durable state precedes workspace settlement
```

# 12. evidence/Judgment boundary

The disposition path must create:

```text
no ExecutionSubmissionRef
no EvidenceCandidate
no evidence-set satisfaction
no semantic/system Judgment
no HumanResult
```

The WorkRun FAILED transition is technical disposition, not an accepted/rework Judgment outcome.

# 13. post-disposition retry boundary

Tests/documentation must prove:

```text
old attempt = EXECUTION_FAILED
old WorkRun = FAILED
old workspace = QUARANTINED or exact safe no-resource verdict
old lineage immutable
same WorkRun retry = forbidden
```

Any future retry requires:

```text
separate new Task/WorkRun lineage
fresh READY
fresh attempt
fresh G_EXECUTION_STARTED
```

This Task does not create that new lineage.

# 14. required tests

Modify exactly the authorized test paths as needed.

## operation protocol

`tests/unit/providers/test_operation_protocol.py`

Prove the narrow lifecycle edge and all adjacent denials.

## durable persistence

`tests/integration/providers/test_execution_persistence.py`

Against isolated PostgreSQL prove:

```text
exact abort succeeds once
attempt becomes EXECUTION_FAILED
execution version increments once
prior READY causal history retained in event metadata
current RUNNING/vN binding recorded
zero operation required
operation-present denied
wrong WorkRun/version denied
wrong attempt/version denied
different provenance replay denied
exact duplicate idempotent
generic transition_attempt cannot invoke the special abort
```

## Stockroom source-owned disposition

`tests/integration/scenarios/test_stockroom_capture_runner.py`

Add tests that construct the exact invalid-history shape without touching private S1 and prove:

```text
no runner replay
no EXECUTION_STARTED
attempt abort first
WorkRun FAILED second
settlement only after both durable boundaries
no provider/tool call
no evidence/Judgment
partial-retry stage handling
mismatch stops before later stages
```

## workspace

`tests/unit/runtime/test_stockroom_workspace.py`

Prove:

```text
restart-safe settlement never adopts lease
exact verified workspace quarantined
fingerprint mismatch denied
symlink escape denied
ambiguous target denied
no broad delete
quarantined bytes preserved
quarantine not reusable as active workspace
idempotent truthful behavior for already-quarantined/absent according to chosen contract
```

# 15. isolated PostgreSQL for tests

Use only a new isolated test PostgreSQL if required by integration tests.

Exact accepted local image:

```text
sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94
```

Use a unique Task-specific container name, localhost-only ephemeral port, fresh ephemeral credential, no retained-private
volume/network/resource reuse.

Use repository-owned Alembic and require migration head:

```text
20260901_0008
```

Never use or inspect:

```text
aiscc-p2-3-private-postgres-v1
aiscc-p2-3-private-postgres-data-v1
aiscc_private_capture
private password file
private runtime root
0036 rows/artifacts
```

Remove only the Task-created test container/storage after tests. No Docker prune.

# 16. validation

Use only the exact Python executable.

At minimum run:

```text
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m py_compile
  src/aiscc/providers/events.py
  src/aiscc/persistence/repository.py
  src/aiscc/scenarios/stockroom_production.py
  src/aiscc/runtime/stockroom_workspace.py
  tests/unit/providers/test_operation_protocol.py
  tests/integration/providers/test_execution_persistence.py
  tests/integration/scenarios/test_stockroom_capture_runner.py
  tests/unit/runtime/test_stockroom_workspace.py

"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -m ruff check <all eight code/test paths>

"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q tests/unit/providers/test_operation_protocol.py
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q tests/unit/runtime/test_stockroom_workspace.py
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q tests/integration/providers/test_execution_persistence.py
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q tests/integration/scenarios/test_stockroom_capture_runner.py
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q tests/integration/providers/test_workflow_handoff.py
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q tests/unit

git diff --check
```

Provider/scenario PostgreSQL tests must have no required DB skip.

# 17. forbidden

Do not:

```text
access retained private runtime
perform real 0036 disposition
create new real run/attempt
edit schema/migrations
edit workflow matrix/guards
edit security policy/capability
edit capture_runner.py
edit canonical state records
git add/commit/push/reset/restore/checkout/stash/clean
```

# 18. final Git boundary

Before Task move require:

```text
HEAD unchanged
index empty
modified tracked paths = non-empty subset of exact nine authorized paths
must include:
  .aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md
  src/aiscc/providers/events.py
  src/aiscc/persistence/repository.py
  src/aiscc/scenarios/stockroom_production.py
  src/aiscc/runtime/stockroom_workspace.py

Git-visible untracked = 11 exact
```

Move current Task byte-identically active→done.

Final Git-visible untracked:

```text
12 exact

1129 Task/Cycle/Judgment
1208 Task/Cycle/Judgment
1224 Task/Cycle/Judgment
current Task/Cycle/Judgment
```

# 19. contract review

Require exactly 60 rows:

```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_EXACT
PREDECESSOR_9_ARTIFACTS_EXACT
CURRENT_STATE_HASHES_EXACT
AUTHORIZED_9_BASELINES_EXACT
INDEX_EMPTY
TRACKED_CLEAN_PREWRITE
PYTHON_EXECUTABLE_EXACT
NO_PRIVATE_RUNTIME_ACCESS
NO_DB_DOCKER_ACCESS
CURRENT_RULE_CONFLICT_REPRODUCED
CONTRACT_EVENT_DEFINED_EXACT
CONTRACT_EDGE_NOT_STARTED_TO_FAILED_EXACT
CONTRACT_REASON_CODE_EXACT
CONTRACT_NO_GENERIC_CANCEL_EXPANSION
CONTRACT_NO_DELAYED_START_ESCAPE
EVENT_LIFECYCLE_MAPPING_IMPLEMENTED
GENERIC_TRANSITION_API_REJECTS_INVALID_HISTORY_ABORT
DEDICATED_ABORT_API_EXISTS
DEDICATED_ABORT_EXACT_IDENTITY_BOUND
DEDICATED_ABORT_WORKRUN_VERSION_BOUND
DEDICATED_ABORT_ZERO_OPERATION_REQUIRED
DEDICATED_ABORT_IDEMPOTENT_EXACT
DEDICATED_ABORT_MISMATCH_FAIL_CLOSED
ABORT_PROVENANCE_APPEND_ONLY
ATTEMPT_POST_ABORT_FAILED_EXACT
WORKRUN_FAILURE_GUARD_AUTHENTIC
WORKRUN_RUNNING_TO_FAILED_EXACT
NO_EVIDENCE_JUDGMENT_CREATED
NO_PROVIDER_TOOL_EXECUTION
NO_READY_RUNNING_REPLAY
NO_NEW_ATTEMPT_CREATED
DISPOSITION_SOURCE_ENTRYPOINT_EXACT
DISPOSITION_PARTIAL_RETRY_IDEMPOTENCY
WORKSPACE_RESTART_SAFE_INSPECTION_DEFINED
WORKSPACE_NO_LEASE_ADOPTION
WORKSPACE_ORPHAN_SETTLEMENT_QUARANTINE_ONLY
WORKSPACE_NO_BROAD_DELETE
WORKSPACE_SYMLINK_ESCAPE_DENIED
WORKSPACE_IDENTITY_FINGERPRINT_VERIFIED
WORKSPACE_QUARANTINE_AFTER_DURABLE_FAILURE
SECURITY_AUTHORITY_NO_FABRICATED_REVOCATION
POST_DISPOSITION_RETRY_NEW_WORKRUN_ONLY
OPERATION_PROTOCOL_UNIT_PASS
EXECUTION_PERSISTENCE_TARGETED_PASS
STOCKROOM_DISPOSITION_INTEGRATION_PASS
WORKSPACE_SETTLEMENT_UNIT_PASS
PROVIDER_PERSISTENCE_REGRESSION_PASS
SCENARIO_REGRESSION_PASS
WORKFLOW_HANDOFF_REGRESSION_PASS
FULL_UNIT_REGRESSION_PASS
RUFF_PASS
PY_COMPILE_PASS
GIT_DIFF_CHECK_PASS
MODIFIED_PATHS_EXACT_SUBSET_9
NO_UNAUTHORIZED_PATH_MUTATION
NO_CANONICAL_STATE_MUTATION
NO_GIT_COMMIT_PUSH
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
EXPORT_INTEGRITY_PASS
```

Success:

```text
60 / 60 PASS
```

# 20. success export

Root docs exactly 14:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
CONTRACT_AMENDMENT_VERIFICATION.md
INVALID_HISTORY_EVENT_VERIFICATION.md
DURABLE_ABORT_VERIFICATION.md
WORKRUN_FAILURE_VERIFICATION.md
WORKSPACE_SETTLEMENT_VERIFICATION.md
DISPOSITION_ORCHESTRATION_VERIFICATION.md
NEGATIVE_BOUNDARY_VERIFICATION.md
TEST_VERIFICATION.md
GIT_DIFF_VERIFICATION.md
CONTRACT_REVIEW.md
```

Project-relative copies:

```text
current Cycle
current Judgment
current done Task
all modified authorized rule/source/test paths
```

Manifest must describe the actual member count; do not hard-code a count before the actual modified-path subset is known.

Require:

```text
one top-level directory
CRC PASS
folder/archive byte equality
TASK.md == canonical done Task
manifest hashes exact
```

# 21. success ceiling

```text
invalid-history abort contract:
CANDIDATE_COMPLETE

source-owned disposition:
CANDIDATE_COMPLETE

restart-safe workspace settlement:
CANDIDATE_COMPLETE

retained 0036 S1:
HOLD / UNTOUCHED

runtime disposition:
NOT_EXECUTED / NOT_AUTHORIZED

Browser acceptance:
HUMAN_PENDING

Git persistence:
NOT_PERFORMED

P2-3:
IN_PROGRESS
```
