# 작업지시서: P2-3 Phase 1B-B3 pre-existing candidate adoption QA

## meta

- task_id: `20260909_2330_aiscc-p2-3-phase1b-b3-preexisting-candidate-adoption-qa-1`
- created_at: `2026-09-09T23:30:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `SOURCE_STATIC_QA / CANDIDATE_ADOPTION_AUDIT`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `40804edfa2dfce244965c59ec94a89c62bf83df5`
- required_base_tree: `1988fc71fc2dce05317eb62879b99c8a5f9dfb53`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. purpose

The predecessor implementation Task stopped correctly because all five B3 paths already existed before its repository gate.

This Task does NOT determine or claim who authored them.

It freezes their exact current bytes as a pre-existing candidate and evaluates whether those bytes satisfy the already-authorized B3 contract.

This is adoption QA, not implementation.

# 1. inbound ZIP bootstrap

The Browser Short Prompt's exact delivery ZIP SHA-256 is the bootstrap integrity anchor.

Current delivery ZIP contains only:

```text
TASK:
20260909_2330_aiscc-p2-3-phase1b-b3-preexisting-candidate-adoption-qa-1.md

CYCLE:
20260909_2330_aiscc-p2-3-phase1b-b3-dirty-candidate-adoption-qa-entry-1.cycle.md
SHA-256:
570d8267404e5e23dd5512e377570a5b81bcca6e514385a3742cb9e2e560a8da
destination:
.aiassistant/records/aiscc/cycles/20260909_2330_aiscc-p2-3-phase1b-b3-dirty-candidate-adoption-qa-entry-1.cycle.md

JUDGMENT:
20260909_2330_aiscc-p2-3-phase1b-b3-preexisting-dirty-candidate-judgment-1.md
SHA-256:
6c85c7c533ffebab14ce1f580cd29a915aa40bd0b52b57d725e29b9a0562c059
destination:
.aiassistant/reports/aiscc/20260909_2330_aiscc-p2-3-phase1b-b3-preexisting-dirty-candidate-judgment-1.md

HANDOFF:
none
```

Place TASK first at:

```text
.aiassistant/tasks/active/20260909_2330_aiscc-p2-3-phase1b-b3-preexisting-candidate-adoption-qa-1.md
```

Read it, then place/hash-verify current CYCLE/JUDGMENT.

Bootstrap failure before canonical TASK placement:

```text
STOP
no report/export
no substantive project mutation
```

After exact canonical transport, inbound cleanup refusal is non-blocking.

# 2. repository gate — adopted dirty baseline

Require:

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

Expected Git-visible set excluding current active Task is exact 10 paths:

- `.aiassistant/tasks/done/20260909_2136_aiscc-p2-3-phase1b-b3-driver-composition-bootstrap-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260909_2136_aiscc-p2-3-b2-state-reconciliation-accepted-b3-implementation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_2136_aiscc-p2-3-b2-state-reconciliation-final-acceptance-judgment-1.md`
- `src/aiscc/bootstrap.py`
- `src/aiscc/scenarios/composition.py`
- `src/aiscc/scenarios/driver.py`
- `tests/unit/scenarios/test_owner_composition.py`
- `tests/integration/scenarios/test_stockroom_binding.py`
- `.aiassistant/records/aiscc/cycles/20260909_2330_aiscc-p2-3-phase1b-b3-dirty-candidate-adoption-qa-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_2330_aiscc-p2-3-phase1b-b3-preexisting-dirty-candidate-judgment-1.md`

No other path.

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Do not cleanup/restore/stash/reset/overwrite.

# 3. predecessor provenance identity

Require exact:

- `.aiassistant/tasks/done/20260909_2136_aiscc-p2-3-phase1b-b3-driver-composition-bootstrap-implementation-1.md`  `1d261d6a7546768f24e14d48678ae344a5d5aa9be77009cc6566dc8805f9af70`
- `.aiassistant/records/aiscc/cycles/20260909_2136_aiscc-p2-3-b2-state-reconciliation-accepted-b3-implementation-entry-1.cycle.md`  `c50a03a48ff75de627b6f94ea93c67886cbdda2815ccfe56d3a21746fb5e156d`
- `.aiassistant/reports/aiscc/20260909_2136_aiscc-p2-3-b2-state-reconciliation-final-acceptance-judgment-1.md`  `bf4375c2e0b7661abaa502a9b3d21fa2bdb38e2dab5cbd6f58f9881e63b22461`

Mismatch:

```text
PREDECESSOR_PROVENANCE_IDENTITY_MISMATCH
→ STOP
```

# 4. exact candidate byte identity

Require exact current workspace SHA-256:

- `src/aiscc/bootstrap.py`  `f23912571b1510ff86d0ad45117ef974e8bb7a84329c8fb08757433cf44d616f`
- `src/aiscc/scenarios/composition.py`  `a516a6a3a42b94202a395996e46919b4a2c2bc06e882334d019aef2829c60b2f`
- `src/aiscc/scenarios/driver.py`  `7740b0a228d37e1034d1938141a903a9c883683b83e90451fa7b82f3381765c4`
- `tests/unit/scenarios/test_owner_composition.py`  `2ccf94c635ecd530d784531dda8d47120a226c12aaab5da5319d9249baa8b024`
- `tests/integration/scenarios/test_stockroom_binding.py`  `92ab7769163fd198c62255be8442ef0dc11ee42b939e8b5930b13a35eeaf894d`

Require:

```text
5 / 5 exact
```

Any mismatch:

```text
PREEXISTING_CANDIDATE_IDENTITY_MISMATCH
→ STOP
```

Do not repair or normalize bytes.

# 5. mutation authority

Product/config/test mutation:

```text
NONE
```

Governance mutation:

```text
current Task active→done only
current issued Cycle/Judgment already placed
```

Forbidden:

```text
editing any of the five candidate paths
creating additional source/config/test files
deleting/restoring the candidate
Git stage/commit
```

If conformance requires a change:

```text
CANDIDATE_REWORK_REQUIRED
→ report exact defect and STOP
```

# 6. must-read authority/source

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

.aiassistant/records/aiscc/cycles/20260909_2330_aiscc-p2-3-phase1b-b3-dirty-candidate-adoption-qa-entry-1.cycle.md
.aiassistant/reports/aiscc/20260909_2330_aiscc-p2-3-phase1b-b3-preexisting-dirty-candidate-judgment-1.md

.aiassistant/tasks/done/20260909_2136_aiscc-p2-3-phase1b-b3-driver-composition-bootstrap-implementation-1.md
.aiassistant/records/aiscc/cycles/20260909_2136_aiscc-p2-3-b2-state-reconciliation-accepted-b3-implementation-entry-1.cycle.md
.aiassistant/reports/aiscc/20260909_2136_aiscc-p2-3-b2-state-reconciliation-final-acceptance-judgment-1.md

.aiassistant/reports/aiscc/20260909_1329_aiscc-p2-3-phase1b-runtime-integration-audit-final-acceptance-judgment-1.md
.aiassistant/reports/aiscc/20260909_1435_aiscc-p2-3-phase1b-b1-final-acceptance-judgment-1.md
.aiassistant/reports/aiscc/20260909_1805_aiscc-p2-3-phase1b-b2-final-acceptance-judgment-1.md

src/aiscc/bootstrap.py
src/aiscc/scenarios/composition.py
src/aiscc/scenarios/driver.py
tests/unit/scenarios/test_owner_composition.py
tests/integration/scenarios/test_stockroom_binding.py

src/aiscc/scenarios/runtime_models.py
src/aiscc/scenarios/enrollment.py
src/aiscc/runtime/stockroom_workspace.py
src/aiscc/runtime/stockroom_materializer.py

src/aiscc/providers/local_deterministic.py
src/aiscc/providers/stockroom_tool.py
src/aiscc/providers/service.py

src/aiscc/security/stockroom_policy.py
src/aiscc/security/policy.py

src/aiscc/workflow/kernel.py
src/aiscc/evidence/service.py
src/aiscc/human/repository.py
src/aiscc/judgment/authority.py
```

Read only direct exact collaborators required to validate imports/types.

No unrelated bulk history.

# 7. complete source contract review

Review the exact five candidate paths line-by-line against the predecessor `2136` B3 contract.

Report PASS/FAIL with concrete symbol references for:

```text
DRIVER_INERTNESS
REAL_OWNER_DEPENDENCY_BINDING
SERVER_OWNED_COMPOSITION
CROSS_CONFIG_IDENTITY_BINDING
CONFIG_FINGERPRINT_PROVENANCE
BOOTSTRAP_EXPLICIT_OWNER_ONLY_FACTORY
DEFAULT_BOOTSTRAP_PRESERVATION
PUBLIC_MODE_SEPARATION
ZERO_IMPLICIT_EXECUTION
NO_CAPTURE_ALGORITHM_IMPLEMENTED
```

Mandatory semantic checks:

```text
OWNER_SELF_DOGFOOD only
resource_ref exact
aiscc-local-deterministic exact
external_llm_executed=false exact
four scenario IDs exact
S3 no tool
S4 HumanResult not synthesized
no default in-memory production owner
no DB construction
no route/public registration
no automatic execute method/path
```

Any substantive mismatch:

```text
CANDIDATE_REWORK_REQUIRED
→ STOP before tests only if source cannot safely import/test
```

If the issue is test-detectable and safe, continue to tests and report both.

# 8. diff provenance review

Because `src/aiscc/bootstrap.py` is tracked-modified while four paths are untracked, inspect:

```text
git diff -- src/aiscc/bootstrap.py
```

Require that its candidate delta is limited to the explicit B3 owner-only preparation factory/imports and does not change existing default bootstrap semantics.

For each untracked file, classify:

```text
exact B3-authorized path
candidate source/test role
no neighboring generated content
```

Do not infer authorship from timestamps or file content.

# 9. static checks

Without changing bytes run exact checks on the five candidate paths.

At minimum:

```text
Python compile:
5 / 5

Ruff:
5 / 5 or repository's exact existing equivalent

git diff --check:
PASS

index:
empty
```

Do not run autoformat/fix mode.

No package install/network/provisioning.

Any formatter/linter that mutates files is forbidden.

# 10. mandatory B3 new tests

Run exactly:

```text
PYTHONDONTWRITEBYTECODE=1
.venv/Scripts/python.exe -B -m pytest -q -p no:cacheprovider tests/unit/scenarios/test_owner_composition.py tests/integration/scenarios/test_stockroom_binding.py -ra
```

Require:

```text
exit 0
failed 0
errors 0
```

Report total passed/skipped count.

If nonzero:

```text
TEST_FAILURE
→ STOP
```

No same-turn file repair.

# 11. targeted B2 regressions

Only after section 10 PASS, run exactly:

```text
.venv/Scripts/python.exe -B -m pytest -q -p no:cacheprovider   tests/unit/scenarios/test_runtime_enrollment.py   tests/unit/providers/test_stockroom_tool.py   tests/unit/providers/test_local_deterministic.py   tests/unit/security/test_stockroom_policy.py
```

Require exit 0.

No same-turn repair after failure.

# 12. bounded bootstrap regression discovery

Search only:

```text
tests/unit/**/test_bootstrap*.py
tests/** imports of the pre-existing bootstrap build_* functions
```

If direct bootstrap regression modules are clearly identified, run that bounded direct set.

If none:

```text
NO_EXISTING_DIRECT_BOOTSTRAP_UNIT_MODULE
```

If ambiguity would require broad suite expansion:

```text
TEST_SCOPE_AMBIGUOUS
→ STOP
```

Do not run DB/Docker/provider integration suites.

# 13. mandatory no-side-effect evidence

The B3 integration test must prove zero calls to the exact real runtime boundaries it maps.

Review and report mapped zero-call targets including available equivalents of:

```text
WorkflowKernel.request_transition
AgentExecutionService execution entry
Postgres execution repository mutation
EvidenceAdmissionService submit/admit entry
Human repository mutation
Judgment authority issue/admit entry
StockroomWorkspace allocation/write
StockroomMaterializer.materialize
SecurityPolicy issue/evaluate capability
LocalDeterministicProvider.call
StockroomSummaryDispatcher dispatch
DockerRuntime run entry
OpenAIResponsesAdapter construction
subprocess process creation
socket/network construction
```

Require:

```text
all mapped call counters:
0
```

If a named method does not exist in current source, report the exact actual mapped callable or `NOT_APPLICABLE_CURRENT_OWNER_INTERFACE`.

Do not silently drop boundaries.

# 14. explicit runtime ceiling verification

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

REPOSITORY_MATERIALIZATION:
NOT_RUN

REAL_PROVIDER_TOOL_DOCKER:
NOT_RUN

DB_MUTATION:
NOT_RUN

REPLAY:
NOT_RUN
```

# 15. post-QA candidate identity

After all checks/tests:

```text
candidate SHA-256:
5 / 5 still exact

other product/config/test delta:
0

index:
empty

Git-visible cache/pyc/pytest residue:
none

git diff --check:
PASS
```

If any candidate byte changed:

```text
UNEXPECTED_WORKSPACE_DELTA
→ STOP
```

# 16. Task lifecycle

After QA/report/export:

```text
.aiassistant/tasks/active/20260909_2330_aiscc-p2-3-phase1b-b3-preexisting-candidate-adoption-qa-1.md
→
.aiassistant/tasks/done/20260909_2330_aiscc-p2-3-phase1b-b3-preexisting-candidate-adoption-qa-1.md
```

Do not edit Task bytes.

Final Git-visible set:

```text
11 exact paths
```

namely predecessor 8 + current Cycle/Judgment + current done Task.

Index remains empty.

# 17. evidence contract

executor_required:

- inbound artifact transport
- exact adopted 10-path workspace gate
- 2136 provenance identity
- frozen five-file candidate identity
- complete B3 source contract review
- bootstrap diff review
- static compile/lint/diff checks
- two new B3 test modules
- four-module B2 targeted regressions
- bounded bootstrap regression result
- no-side-effect boundary mapping/proof
- final exact candidate identity
- outbound result ZIP

reuse_allowed:

- persisted B1/B2 contracts
- accepted 2136 B3 Task contract
- blocked 2136 workspace snapshot as byte provenance only

human_owned:

```text
new Human QA:
NOT_REQUIRED

candidate authorship:
UNKNOWN / do not infer

public distribution/license:
HUMAN_PENDING
```

not_required:

```text
actual runtime/capture
real provider/tool/Docker
DB
Replay
deployment
```

forbidden:

```text
source/test/config mutation
candidate cleanup/deletion
Git add/commit/push
actual scenario execution
network/provider access
Docker
DB
Replay
P2-4/P3
```

# 18. mandatory stop

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
PREEXISTING_CANDIDATE_IDENTITY_MISMATCH
MISSING_REQUIRED_ARTIFACT
CANDIDATE_REWORK_REQUIRED
TEST_SCOPE_AMBIGUOUS
BLOCKED_RUNTIME_PREREQUISITE
TEST_FAILURE
UNEXPECTED_WORKSPACE_DELTA
ZIP_EXPORT_FAILED
```

Inbound cleanup refusal after canonical transport remains non-blocking.

# 19. export bundle + outbound ZIP

Bundle folder:

```text
.aiassistant/reports/target/20260909_2330_aiscc-p2-3-phase1b-b3-preexisting-candidate-adoption-qa-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
CANDIDATE_IDENTITY_VERIFICATION.md
SOURCE_CONTRACT_REVIEW.md
BOOTSTRAP_DIFF_VERIFICATION.md
NO_SIDE_EFFECT_INTEGRATION_VERIFICATION.md
TEST_VERIFICATION.md
```

Include byte-preserving project-relative copies of:

```text
current Cycle
current Judgment
current done Task
all five exact candidate paths
```

After folder completion create:

```text
.aiassistant/reports/target/20260909_2330_aiscc-p2-3-phase1b-b3-preexisting-candidate-adoption-qa-1.zip
```

Require one top-level directory, CRC/readability PASS, required roots, manifest coverage, and folder/archive byte equality.

# 20. final ceiling

Success:

```text
P2-3 Phase 1B-B3 exact pre-existing candidate:
READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT

candidate authorship:
UNKNOWN / NOT_REQUIRED_FOR_CORRECTNESS_ADMISSION

candidate persistence:
NOT_RUN

actual scenario capture:
NOT_STARTED

Replay:
NOT_STARTED
```

Do not declare Phase 1B closed and do not start runtime/capture work.
