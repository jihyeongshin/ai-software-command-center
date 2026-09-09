# 작업지시서: P2-3 Phase 1B-B3 tool fingerprint strict-JSON rework

## meta

- task_id: `20260910_0100_aiscc-p2-3-phase1b-b3-tool-fingerprint-json-subset-rework-1`
- created_at: `2026-09-10T01:00:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `BOUNDED_ORCHESTRATION_REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `40804edfa2dfce244965c59ec94a89c62bf83df5`
- required_base_tree: `1988fc71fc2dce05317eb62879b99c8a5f9dfb53`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. purpose

The 0020 rework correctly fixed the provider timeout canonical representation and completed the zero-side-effect test harness expansion, but canonical owner composition still fails before proof milestones.

The remaining bounded defect is the tool fingerprint's direct use of `asdict(tool)`, which preserves `StockroomToolConfig.argv` as a Python tuple instead of a strict JSON array.

This Task authorizes only the product normalization needed for the canonical fingerprint payload.

# 1. inbound ZIP bootstrap

The Browser Short Prompt's exact delivery ZIP SHA-256 is the bootstrap integrity anchor.

Current delivery ZIP contains only:

```text
TASK:
20260910_0100_aiscc-p2-3-phase1b-b3-tool-fingerprint-json-subset-rework-1.md

CYCLE:
20260910_0100_aiscc-p2-3-phase1b-b3-second-test-failure-tool-fingerprint-rework-entry-1.cycle.md
SHA-256:
b931f3b7de6df604d986cb96c66fc09312a1f769bc5adb0108c38c8dbcdca2fe
destination:
.aiassistant/records/aiscc/cycles/20260910_0100_aiscc-p2-3-phase1b-b3-second-test-failure-tool-fingerprint-rework-entry-1.cycle.md

JUDGMENT:
20260910_0100_aiscc-p2-3-phase1b-b3-second-test-failure-judgment-1.md
SHA-256:
4ed40a08fc831a65b145a7cd3cfaa6ff2873f428f6c608092c7eddee1c5237c7
destination:
.aiassistant/reports/aiscc/20260910_0100_aiscc-p2-3-phase1b-b3-second-test-failure-judgment-1.md

HANDOFF:
none
```

Place TASK first at:

```text
.aiassistant/tasks/active/20260910_0100_aiscc-p2-3-phase1b-b3-tool-fingerprint-json-subset-rework-1.md
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

Expected Git-visible set excluding current active Task is exact 16 paths:

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
- `.aiassistant/tasks/done/20260910_0020_aiscc-p2-3-phase1b-b3-candidate-fingerprint-zero-side-effect-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_0020_aiscc-p2-3-phase1b-b3-adoption-qa-failed-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_0020_aiscc-p2-3-phase1b-b3-adoption-qa-failure-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_0100_aiscc-p2-3-phase1b-b3-second-test-failure-tool-fingerprint-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_0100_aiscc-p2-3-phase1b-b3-second-test-failure-judgment-1.md`

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

Require exact 0020 provenance:

- `.aiassistant/tasks/done/20260910_0020_aiscc-p2-3-phase1b-b3-candidate-fingerprint-zero-side-effect-rework-1.md`  `5a7b1eabc00e0ca2cf36b92d0708bded98e51c4acc63ce8923d1106b9b33e16b`
- `.aiassistant/records/aiscc/cycles/20260910_0020_aiscc-p2-3-phase1b-b3-adoption-qa-failed-rework-entry-1.cycle.md`  `459f70b2e13f87fca6ba0e6b9c8e30e1d96ad613fc5f72db896f5bd1227dbb91`
- `.aiassistant/reports/aiscc/20260910_0020_aiscc-p2-3-phase1b-b3-adoption-qa-failure-judgment-1.md`  `93b61e981d9190bceaa31b39b9687b4446b24d82d4663330e874e420901285f3`

Mismatch:

```text
PREDECESSOR_PROVENANCE_IDENTITY_MISMATCH
→ STOP
```

# 4. exact starting B3 candidate identity

Require:

- `src/aiscc/bootstrap.py`  `f23912571b1510ff86d0ad45117ef974e8bb7a84329c8fb08757433cf44d616f`
- `src/aiscc/scenarios/composition.py`  `ed1ade4433ff24ab96341586722a45a6e8efc3203d776d8af9cfaa89562a8604`
- `src/aiscc/scenarios/driver.py`  `7740b0a228d37e1034d1938141a903a9c883683b83e90451fa7b82f3381765c4`
- `tests/unit/scenarios/test_owner_composition.py`  `2ccf94c635ecd530d784531dda8d47120a226c12aaab5da5319d9249baa8b024`
- `tests/integration/scenarios/test_stockroom_binding.py`  `f1a4fb8b2239dc70982fe4d16701340c14f420c136ae87abee6def331cf9f7bb`

Require:

```text
5 / 5 exact
```

Any mismatch:

```text
PREEXISTING_CANDIDATE_IDENTITY_MISMATCH
→ STOP
```

Candidate authorship remains:

```text
UNKNOWN
```

Do not relabel it.

# 5. exact mutation authority

Only:

```text
src/aiscc/scenarios/composition.py
```

may change.

These four paths must remain byte-exact:

```text
src/aiscc/bootstrap.py
SHA-256:
f23912571b1510ff86d0ad45117ef974e8bb7a84329c8fb08757433cf44d616f

src/aiscc/scenarios/driver.py
SHA-256:
7740b0a228d37e1034d1938141a903a9c883683b83e90451fa7b82f3381765c4

tests/unit/scenarios/test_owner_composition.py
SHA-256:
2ccf94c635ecd530d784531dda8d47120a226c12aaab5da5319d9249baa8b024

tests/integration/scenarios/test_stockroom_binding.py
SHA-256:
f1a4fb8b2239dc70982fe4d16701340c14f420c136ae87abee6def331cf9f7bb
```

No test/config/shared-owner/governance edit other than current Task lifecycle.

If another path is required:

```text
SCOPE_EXPANSION_REQUIRED
→ STOP
```

# 6. exact source defect

Current final 0020 code includes:

```python
tool_hash = canonical_sha256(
    {
        **asdict(tool),
        "allowed_scenarios": list(_TOOL_SCENARIOS),
        "allowed_profiles": list(_TOOL_PROFILES),
        "model_visible_arguments": {},
    }
)
```

`StockroomToolConfig.argv` is typed:

```text
tuple[str, ...]
```

and `asdict(tool)` preserves the tuple.

The canonical hash boundary must receive only the strict JSON value subset.

Do not pass a tuple or dataclass-derived non-JSON container into it.

# 7. exact product correction

In `src/aiscc/scenarios/composition.py`, replace the direct `asdict(tool)` expansion with an explicit deterministic tool fingerprint payload.

It must encode the same accepted tool semantic identity:

```text
registry_id
registry_version
tool_id
schema_version
action
dispatcher_version
process_resource_id
image
argv
workdir
network
stdout_limit_bytes
stderr_limit_bytes
operation_timeout_seconds
cleanup_timeout_seconds
attempt_timeout_seconds
retry_maximum
output_byte_bound
allowed_scenarios
allowed_profiles
model_visible_arguments
```

Required canonical types:

```text
argv:
list(tool.argv)

allowed_scenarios:
list

allowed_profiles:
list

model_visible_arguments:
dict

all limits:
int

all identities:
str
```

Do not add/remove semantic fields silently.

Do not hash raw absolute host paths, secrets, mutable run data or requester input.

# 8. complete strict-JSON fingerprint audit

Review every input passed to `canonical_sha256` within `_fingerprints(...)`.

For every nested value/container, require only:

```text
dict with str keys
list
str
int
bool
None
```

Explicitly prove absent:

```text
float
tuple
frozenset
set
MappingProxyType
dataclass object
Path
datetime
enum object
bytes
```

The existing `_canonical_profile_timeout_seconds(...)` remains the owner of provider total-timeout conversion.

Do not rewrite unrelated fingerprints if they already satisfy the strict subset.

If another non-JSON field is found inside `_fingerprints()` and can be normalized in `composition.py` without semantic change, fix it in the same file and report it exactly.

If correction would require another file:

```text
SCOPE_EXPANSION_REQUIRED
→ STOP
```

# 9. no test modification

Both B3 tests remain frozen.

The existing integration test already contains:

```text
provider whole-second/fractional/non-finite fingerprint proof
early complete zero-call spy installation
all requested durable/Human/evidence/tool boundaries
completion milestones
Ruff-correct imports
```

Do not modify tests to accommodate the product change.

# 10. mandatory static checks

Run compile on all five B3 paths and Ruff on all five B3 paths.

Require:

```text
Python compile:
5 / 5 PASS

Ruff:
5 / 5 PASS

git diff --check:
PASS

index:
empty
```

No auto-fix/formatter.

If nonzero:

```text
STATIC_CHECK_FAILURE
→ STOP
```

No same-turn second repair after mandatory static failure.

# 11. mandatory B3 tests

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

Report passed/skipped count.

If nonzero:

```text
TEST_FAILURE
→ STOP
```

No same-turn second repair.

# 12. targeted B2 regressions

Only after section 11 PASS:

```text
.venv/Scripts/python.exe -B -m pytest -q -p no:cacheprovider   tests/unit/scenarios/test_runtime_enrollment.py   tests/unit/providers/test_stockroom_tool.py   tests/unit/providers/test_local_deterministic.py   tests/unit/security/test_stockroom_policy.py
```

Require exit 0.

Any failure:

```text
TEST_FAILURE
→ STOP
```

No same-turn repair.

# 13. bounded bootstrap regression discovery

Search only:

```text
tests/unit/**/test_bootstrap*.py
tests/** direct imports/calls of pre-existing bootstrap build_* functions
```

Run the clearly direct bounded set if found.

If none:

```text
NO_EXISTING_DIRECT_BOOTSTRAP_UNIT_MODULE
```

If ambiguous:

```text
TEST_SCOPE_AMBIGUOUS
→ STOP
```

No broad DB/Docker/provider integration suite.

# 14. executed zero-side-effect proof

After B3 tests PASS, report all mapped counters from the frozen integration test.

Require:

```text
owner dependency construction milestone:
reached

owner composition milestone:
reached

bootstrap preparation milestone:
reached

S1:
prepared

S2:
prepared

S3:
prepared

S4:
prepared

every installed executable/mutation/network counter:
0
```

A test that terminates before final counter assertion is not proof.

# 15. complete ten-contract review

Require final:

```text
DRIVER_INERTNESS:
PASS

REAL_OWNER_DEPENDENCY_BINDING:
PASS

SERVER_OWNED_COMPOSITION:
PASS

CROSS_CONFIG_IDENTITY_BINDING:
PASS

CONFIG_FINGERPRINT_PROVENANCE:
PASS

BOOTSTRAP_EXPLICIT_OWNER_ONLY_FACTORY:
PASS

DEFAULT_BOOTSTRAP_PRESERVATION:
PASS

PUBLIC_MODE_SEPARATION:
PASS

ZERO_IMPLICIT_EXECUTION:
PASS

NO_CAPTURE_ALGORITHM_IMPLEMENTED:
PASS
```

No hybrid/source-only PASS is sufficient.

# 16. explicit runtime ceiling

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

# 17. post-test identity/scope

Require:

```text
composition.py:
changed from 0020 candidate

other four B3 candidate paths:
exact frozen hashes

B3 candidate:
5 exact paths

other product/config/test delta:
0

B1/B2:
unchanged

index:
empty

git diff --check:
PASS

Git-visible pyc/__pycache__/pytest cache:
none
```

No Git add/commit.

# 18. Task lifecycle / final workspace

Before current Task lifecycle:

```text
existing pending paths:
14

current Cycle/Judgment:
2

total excluding active Task:
16 exact
```

Then move:

```text
.aiassistant/tasks/active/20260910_0100_aiscc-p2-3-phase1b-b3-tool-fingerprint-json-subset-rework-1.md
→
.aiassistant/tasks/done/20260910_0100_aiscc-p2-3-phase1b-b3-tool-fingerprint-json-subset-rework-1.md
```

Final:

```text
17 exact Git-visible paths
index empty
```

No other path.

# 19. evidence contract

executor_required:

- inbound transport
- exact 16-path repository gate
- 2136/2330/0020 provenance identities
- exact starting candidate identity
- exact one-file rework diff
- strict JSON-subset fingerprint audit
- static checks PASS
- B3 mandatory tests PASS
- B2 regressions PASS
- bounded bootstrap regression result
- completed zero-call milestones/counters
- ten-contract final review
- exact final candidate/workspace identity
- outbound result ZIP

reuse_allowed:

- frozen four unchanged B3 paths
- persisted B1/B2
- 0020 accepted harness changes and source diagnosis

human_owned:

```text
new Human QA:
NOT_REQUIRED

candidate authorship:
UNKNOWN

public distribution/license:
HUMAN_PENDING
```

forbidden:

```text
test modification
bootstrap.py modification
driver.py modification
B1/B2/config/shared-owner mutation
canonical hash utility mutation
Git add/commit/push
actual scenario execution
network/provider access
Docker
DB
Replay
P2-4/P3
```

# 20. mandatory stop

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

# 21. export bundle + outbound ZIP

Bundle folder:

```text
.aiassistant/reports/target/20260910_0100_aiscc-p2-3-phase1b-b3-tool-fingerprint-json-subset-rework-1/
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
.aiassistant/reports/target/20260910_0100_aiscc-p2-3-phase1b-b3-tool-fingerprint-json-subset-rework-1.zip
```

Require one top-level directory, readable/CRC PASS, required roots, manifest coverage and folder/archive byte equality.

# 22. final ceiling

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
