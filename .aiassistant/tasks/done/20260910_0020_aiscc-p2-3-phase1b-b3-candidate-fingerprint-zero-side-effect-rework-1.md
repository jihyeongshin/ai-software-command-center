# 작업지시서: P2-3 Phase 1B-B3 candidate fingerprint / zero-side-effect rework

## meta

- task_id: `20260910_0020_aiscc-p2-3-phase1b-b3-candidate-fingerprint-zero-side-effect-rework-1`
- created_at: `2026-09-10T00:20:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `BOUNDED_ORCHESTRATION_REWORK / QA_PROOF_REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `40804edfa2dfce244965c59ec94a89c62bf83df5`
- required_base_tree: `1988fc71fc2dce05317eb62879b99c8a5f9dfb53`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. purpose

The exact pre-existing B3 candidate was not adopted because its canonical composition cannot be constructed and its zero-side-effect integration proof is incomplete.

This Task authorizes a bounded two-file rework against the frozen candidate.

Candidate authorship remains unknown. Do not relabel authorship.

# 1. inbound ZIP bootstrap

The Browser Short Prompt's exact delivery ZIP SHA-256 is the bootstrap integrity anchor.

Current delivery ZIP contains only:

```text
TASK:
20260910_0020_aiscc-p2-3-phase1b-b3-candidate-fingerprint-zero-side-effect-rework-1.md

CYCLE:
20260910_0020_aiscc-p2-3-phase1b-b3-adoption-qa-failed-rework-entry-1.cycle.md
SHA-256:
459f70b2e13f87fca6ba0e6b9c8e30e1d96ad613fc5f72db896f5bd1227dbb91
destination:
.aiassistant/records/aiscc/cycles/20260910_0020_aiscc-p2-3-phase1b-b3-adoption-qa-failed-rework-entry-1.cycle.md

JUDGMENT:
20260910_0020_aiscc-p2-3-phase1b-b3-adoption-qa-failure-judgment-1.md
SHA-256:
93b61e981d9190bceaa31b39b9687b4446b24d82d4663330e874e420901285f3
destination:
.aiassistant/reports/aiscc/20260910_0020_aiscc-p2-3-phase1b-b3-adoption-qa-failure-judgment-1.md

HANDOFF:
none
```

Place TASK first at:

```text
.aiassistant/tasks/active/20260910_0020_aiscc-p2-3-phase1b-b3-candidate-fingerprint-zero-side-effect-rework-1.md
```

Read it, then place/hash-verify current CYCLE/JUDGMENT.

Bootstrap failure before canonical TASK placement:

```text
STOP
no report/export
no substantive project mutation
```

After exact canonical transport, inbound cleanup refusal is non-blocking.

# 2. repository gate — exact adopted dirty baseline

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

Expected Git-visible set excluding current active Task is exact 13 paths:

- `.aiassistant/tasks/done/20260909_2136_aiscc-p2-3-phase1b-b3-driver-composition-bootstrap-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260909_2136_aiscc-p2-3-b2-state-reconciliation-accepted-b3-implementation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_2136_aiscc-p2-3-b2-state-reconciliation-final-acceptance-judgment-1.md`
- `src/aiscc/bootstrap.py`
- `src/aiscc/scenarios/composition.py`
- `src/aiscc/scenarios/driver.py`
- `tests/unit/scenarios/test_owner_composition.py`
- `tests/integration/scenarios/test_stockroom_binding.py`
- `.aiassistant/tasks/done/20260909_2330_aiscc-p2-3-phase1b-b3-preexisting-candidate-adoption-qa-1.md`
- `.aiassistant/records/aiscc/cycles/20260909_2330_aiscc-p2-3-phase1b-b3-dirty-candidate-adoption-qa-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_2330_aiscc-p2-3-phase1b-b3-preexisting-dirty-candidate-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_0020_aiscc-p2-3-phase1b-b3-adoption-qa-failed-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_0020_aiscc-p2-3-phase1b-b3-adoption-qa-failure-judgment-1.md`

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Do not cleanup/restore/stash/reset/overwrite.

# 3. exact predecessor provenance

Require exact 2136 provenance:

- `.aiassistant/tasks/done/20260909_2136_aiscc-p2-3-phase1b-b3-driver-composition-bootstrap-implementation-1.md`  `1d261d6a7546768f24e14d48678ae344a5d5aa9be77009cc6566dc8805f9af70`
- `.aiassistant/records/aiscc/cycles/20260909_2136_aiscc-p2-3-b2-state-reconciliation-accepted-b3-implementation-entry-1.cycle.md`  `c50a03a48ff75de627b6f94ea93c67886cbdda2815ccfe56d3a21746fb5e156d`
- `.aiassistant/reports/aiscc/20260909_2136_aiscc-p2-3-b2-state-reconciliation-final-acceptance-judgment-1.md`  `bf4375c2e0b7661abaa502a9b3d21fa2bdb38e2dab5cbd6f58f9881e63b22461`

Require exact 2330 provenance:

- `.aiassistant/tasks/done/20260909_2330_aiscc-p2-3-phase1b-b3-preexisting-candidate-adoption-qa-1.md`  `7a4bcd03c69e309ec08d680c2f889564805ad501de0c943f68f98f9240814dac`
- `.aiassistant/records/aiscc/cycles/20260909_2330_aiscc-p2-3-phase1b-b3-dirty-candidate-adoption-qa-entry-1.cycle.md`  `570d8267404e5e23dd5512e377570a5b81bcca6e514385a3742cb9e2e560a8da`
- `.aiassistant/reports/aiscc/20260909_2330_aiscc-p2-3-phase1b-b3-preexisting-dirty-candidate-judgment-1.md`  `6c85c7c533ffebab14ce1f580cd29a915aa40bd0b52b57d725e29b9a0562c059`

Mismatch:

```text
PREDECESSOR_PROVENANCE_IDENTITY_MISMATCH
→ STOP
```

# 4. exact starting candidate identity

Require exact five starting candidate hashes:

- `src/aiscc/bootstrap.py`  `f23912571b1510ff86d0ad45117ef974e8bb7a84329c8fb08757433cf44d616f`
- `src/aiscc/scenarios/composition.py`  `a516a6a3a42b94202a395996e46919b4a2c2bc06e882334d019aef2829c60b2f`
- `src/aiscc/scenarios/driver.py`  `7740b0a228d37e1034d1938141a903a9c883683b83e90451fa7b82f3381765c4`
- `tests/unit/scenarios/test_owner_composition.py`  `2ccf94c635ecd530d784531dda8d47120a226c12aaab5da5319d9249baa8b024`
- `tests/integration/scenarios/test_stockroom_binding.py`  `92ab7769163fd198c62255be8442ef0dc11ee42b939e8b5930b13a35eeaf894d`

Any mismatch:

```text
PREEXISTING_CANDIDATE_IDENTITY_MISMATCH
→ STOP
```

# 5. exact mutation authority

Only these two existing candidate paths may change:

```text
src/aiscc/scenarios/composition.py
tests/integration/scenarios/test_stockroom_binding.py
```

These three must remain byte-exact:

- `src/aiscc/bootstrap.py`  `f23912571b1510ff86d0ad45117ef974e8bb7a84329c8fb08757433cf44d616f`
- `src/aiscc/scenarios/driver.py`  `7740b0a228d37e1034d1938141a903a9c883683b83e90451fa7b82f3381765c4`
- `tests/unit/scenarios/test_owner_composition.py`  `2ccf94c635ecd530d784531dda8d47120a226c12aaab5da5319d9249baa8b024`

No other product/config/test/governance path may be edited except current Task lifecycle.

If another path is needed:

```text
SCOPE_EXPANSION_REQUIRED
→ STOP
```

# 6. fix canonical provider fingerprint

Modify:

```text
src/aiscc/scenarios/composition.py
```

The repository `canonical_sha256` contract rejects floats.

Current B2 Stockroom profile stores `total_timeout_seconds` as a float for compatibility, but the accepted Stockroom owner profile uses a whole-second finite value.

Implement a private B3 canonicalization boundary for this fingerprint field.

Required semantics:

```text
input:
profile.total_timeout_seconds

require:
real numeric float/int compatible with current profile type
finite
> 0
exactly integral
within already validated Stockroom profile maximum

canonical fingerprint representation:
integer seconds
```

Equivalent narrow implementation is acceptable, e.g.:

```text
value = profile.total_timeout_seconds
if not finite or value <= 0 or not value.is_integer():
    raise StockroomCompositionError(...)
canonical_seconds = int(value)
```

Use repository style/types and stable error behavior.

Do NOT:

```text
change canonical_json_bytes/canonical_sha256
serialize arbitrary float with repr/str
round/truncate fractional values
change B2 profile loader/config
change accepted finite limits
```

A fractional/non-finite value must fail composition closed.

Review all `_fingerprints(...)` inputs after the fix and prove no float reaches the canonical subset.

Do not change tool/security semantics merely because they are adjacent.

# 7. fingerprint tests using existing writable integration module

Without modifying the frozen unit test module, add bounded assertions/fixtures in:

```text
tests/integration/scenarios/test_stockroom_binding.py
```

to prove:

```text
canonical real configuration:
composition fingerprint succeeds and is deterministic

whole-second float:
canonicalizes to exact integer semantics

fractional total_timeout_seconds:
composition denied, never rounded

NaN / positive infinity / negative infinity:
composition denied

fingerprint output:
64 lowercase hex where current conventions require it
```

Use test-owned temporary/copy objects only.
Do not mutate canonical config files.

If current strict profile dataclass prevents constructing such negative fixtures, use the narrowest existing immutable replacement/dataclass-copy mechanism.

# 8. zero-side-effect observation order

In the integration test, install all runtime/mutation/network spies BEFORE:

```text
_owners()
build_stockroom_owner_composition()
bootstrap.build_stockroom_owner_preparation(...)
prepare(...)
```

The observed interval must include:

```text
strict config load/cross-binding
owner dependency construction
bootstrap owner factory
four scenario request preparation
```

The expected counter remains:

```text
all mapped executable/mutation boundaries = 0
```

Pure config file reads and pure object construction are allowed.

# 9. complete boundary map

Retain every currently mapped boundary from the 2330 candidate and add every available current callable listed below.

## Stockroom tool

```text
StockroomSummaryDispatcher.dispatch
StockroomSummaryDispatcher.dispatch_with_receipts
```

## durable execution repository

Map available current methods equivalent to:

```text
create_attempt
transition_attempt
create_operation
advance_operation
store_private_protocol_item
reserve_execution_bounds
settle_execution_output
start_dispatch_if_fresh
fail_operation_before_side_effect
close_workflow_left_running
store_output_ref
```

## evidence admission

Map available current mutations equivalent to:

```text
submit
submit_durable
preserve_supplemental
invalidate_authority
```

## Human owner

Map available current mutations equivalent to:

```text
submit_result
issue_current_gate_action_authority
expire_gate_if_needed
supersede_gate
create_producer_ref
```

## Judgment owner

Retain exact current Judgment issuance/admission mutation callable(s).

## existing already-required boundaries

Retain:

```text
Workflow transition
AgentExecutionService provider/execute entries
StockroomWorkspace allocate/write
StockroomMaterializer.materialize
SecurityPolicy grant/evaluate/capability issuance
StockroomOwnerRestriction seal/allows
LocalDeterministicProvider.call
DockerRuntime run/receipt entry
OpenAIResponsesAdapter construction
subprocess.Popen
socket.socket
```

For each requested name:

```text
if exact callable exists:
patch and assert zero

if current repository exposes a renamed direct equivalent:
patch that equivalent and record mapping

if no applicable callable exists:
record NOT_APPLICABLE_CURRENT_OWNER_INTERFACE
```

Do not silently omit.

# 10. spy correctness

Spies must be installed safely without mutating product source.

A patched boundary should:

```text
increment its own counter
raise AssertionError immediately
```

After the four-scenario preparation sequence require:

```text
every installed counter == 0
```

Also assert the test reached completion of:

```text
_owner composition creation
bootstrap owner preparation
S1 request preparation
S2 request preparation
S3 request preparation
S4 request preparation
```

This prevents a pre-spy/preparation failure from being mistaken for zero-call proof.

# 11. Ruff import ordering

Fix only the import ordering in:

```text
tests/integration/scenarios/test_stockroom_binding.py
```

as required by repository Ruff `I001`.

Do not run Ruff auto-fix or formatter mutation.

# 12. static checks before pytest

Run non-mutating checks on exactly:

```text
src/aiscc/scenarios/composition.py
tests/integration/scenarios/test_stockroom_binding.py
```

plus compile validation of all five B3 paths.

Require:

```text
Python compile:
5 / 5 PASS

Ruff:
5 B3 paths PASS

git diff --check:
PASS

index:
empty
```

No package install/network/provisioning.

If static checks fail:

```text
STATIC_CHECK_FAILURE
→ STOP
```

No same-turn second repair after this mandatory check failure.

# 13. mandatory B3 tests

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

Report total passed/skipped.

If nonzero:

```text
TEST_FAILURE
→ STOP
```

No same-turn second repair.

# 14. targeted B2 regressions

Only after B3 tests PASS, run exactly:

```text
.venv/Scripts/python.exe -B -m pytest -q -p no:cacheprovider   tests/unit/scenarios/test_runtime_enrollment.py   tests/unit/providers/test_stockroom_tool.py   tests/unit/providers/test_local_deterministic.py   tests/unit/security/test_stockroom_policy.py
```

Require exit 0.

No same-turn repair on failure.

# 15. bounded bootstrap regression discovery

Search only:

```text
tests/unit/**/test_bootstrap*.py
tests/** direct imports/calls of pre-existing bootstrap build_* functions
```

Run the bounded direct bootstrap regression set if clearly identified.

If none:

```text
NO_EXISTING_DIRECT_BOOTSTRAP_UNIT_MODULE
```

If ambiguity requires broad suite expansion:

```text
TEST_SCOPE_AMBIGUOUS
→ STOP
```

Do not run DB/Docker/provider integration suites.

# 16. complete source contract re-review

After tests, re-review final exact five candidate paths.

Report PASS/FAIL for:

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

Success requires all ten:

```text
PASS
```

No `PASS_SOURCE / FAIL_PROOF` hybrid remains.

# 17. explicit runtime ceiling

Report exactly:

```text
PHASE1B_B3_DB_MIGRATION:
NOT_REQUIRED

DEFAULT_STARTUP_EXECUTION:
ZERO

OWNER_PREPARATION_SIDE_EFFECTS:
ZERO / EXECUTED_PROOF

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

Do not promote never-call proof into runtime execution proof.

# 18. post-QA identity/scope

Require:

```text
composition.py:
changed from frozen candidate

test_stockroom_binding.py:
changed from frozen candidate

other three B3 candidate paths:
exact frozen hashes

B3 candidate path set:
5 exact

other product/config/test delta:
0

B1/B2 files:
unchanged

index:
empty

git diff --check:
PASS

Git-visible pyc/__pycache__/pytest cache:
none
```

No Git add/commit.

# 19. Task lifecycle / final workspace

Before current Task lifecycle:

```text
2136 provenance:
3

B3 candidate:
5

2330 provenance:
3

current Cycle/Judgment:
2

total excluding active Task:
13 exact
```

Then move:

```text
.aiassistant/tasks/active/20260910_0020_aiscc-p2-3-phase1b-b3-candidate-fingerprint-zero-side-effect-rework-1.md
→
.aiassistant/tasks/done/20260910_0020_aiscc-p2-3-phase1b-b3-candidate-fingerprint-zero-side-effect-rework-1.md
```

Final:

```text
14 exact Git-visible paths
index empty
```

No other path.

# 20. evidence contract

executor_required:

- inbound transport
- exact 13-path preflight
- 2136/2330 provenance identity
- exact starting five-file candidate identity
- exact two-file rework
- canonical integer fingerprint proof
- complete zero-call observation mapping
- Ruff/static PASS
- B3 mandatory tests PASS
- B2 targeted regressions PASS
- bounded bootstrap regression result
- complete ten-contract source re-review
- exact final workspace/candidate identity
- outbound result ZIP

reuse_allowed:

- frozen three unchanged B3 candidate files
- persisted B1/B2 contracts
- 2330 source diagnosis

human_owned:

```text
new Human QA:
NOT_REQUIRED

candidate authorship:
UNKNOWN

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
modifying bootstrap.py
modifying driver.py
modifying test_owner_composition.py
B1/B2/config/shared-owner changes
canonical hash utility changes
source/test change outside two-path allowlist
Git add/commit/push
actual scenario execution
network/provider access
Docker
DB
Replay
P2-4/P3
```

# 21. mandatory stop

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
SCOPE_EXPANSION_REQUIRED
STATIC_CHECK_FAILURE
TEST_SCOPE_AMBIGUOUS
BLOCKED_RUNTIME_PREREQUISITE
TEST_FAILURE
CONTRACT_MISMATCH
UNEXPECTED_WORKSPACE_DELTA
ZIP_EXPORT_FAILED
```

Inbound cleanup refusal after canonical transport remains non-blocking.

# 22. export bundle + outbound ZIP

Bundle folder:

```text
.aiassistant/reports/target/20260910_0020_aiscc-p2-3-phase1b-b3-candidate-fingerprint-zero-side-effect-rework-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
CANDIDATE_IDENTITY_VERIFICATION.md
REWORK_DIFF_VERIFICATION.md
SOURCE_CONTRACT_REVIEW.md
FINGERPRINT_VERIFICATION.md
NO_SIDE_EFFECT_INTEGRATION_VERIFICATION.md
TEST_VERIFICATION.md
```

Include byte-preserving project-relative copies of:

```text
current Cycle
current Judgment
current done Task
all five final B3 candidate paths
```

After folder completion create:

```text
.aiassistant/reports/target/20260910_0020_aiscc-p2-3-phase1b-b3-candidate-fingerprint-zero-side-effect-rework-1.zip
```

Require one top-level directory, readable/CRC PASS, required roots, manifest coverage, and folder/archive byte equality.

# 23. final ceiling

Success:

```text
P2-3 Phase 1B-B3:
READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT

candidate authorship:
UNKNOWN

candidate persistence:
NOT_RUN

actual scenario capture:
NOT_STARTED

Replay:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

Do not declare Phase 1B closed and do not start runtime/capture work.
