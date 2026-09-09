# 작업지시서: P2-3 Phase 1A Windows pytest parameter-ID rework

## meta

- task_id: `20260909_0110_aiscc-p2-3-phase1a-windows-pytest-parameter-id-rework-1`
- created_at: `2026-09-09T01:10:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `QA_ONLY / BOUNDED_TEST_REWORK`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `4cadcb45b44d5bb2a260d7fa9350626ce28ea875`
- required_base_tree: `7d98df6f74eba74427d1be3b0abe9a78ef91a29f`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. inbound ZIP bootstrap

The Browser Short Prompt's exact delivery ZIP SHA-256 is the bootstrap integrity anchor.

Current delivery ZIP contains only:

```text
TASK:
20260909_0110_aiscc-p2-3-phase1a-windows-pytest-parameter-id-rework-1.md

CYCLE:
20260909_0110_aiscc-p2-3-phase1a-test-failure-parameter-id-rework-entry-1.cycle.md
SHA-256:
f9fc4e87ef383b97516dc3bd900d48775b187e2c50f6da473ac1e7609888b6f2
destination:
.aiassistant/records/aiscc/cycles/20260909_0110_aiscc-p2-3-phase1a-test-failure-parameter-id-rework-entry-1.cycle.md

JUDGMENT:
20260909_0110_aiscc-p2-3-phase1a-test-failure-parameter-id-judgment-1.md
SHA-256:
c8bcb571191cbf647cd54fa8d65b1b99837e757d76423e5a1d2cd46aa553f607
destination:
.aiassistant/reports/aiscc/20260909_0110_aiscc-p2-3-phase1a-test-failure-parameter-id-judgment-1.md

HANDOFF:
none
```

Place TASK first at:

```text
.aiassistant/tasks/active/20260909_0110_aiscc-p2-3-phase1a-windows-pytest-parameter-id-rework-1.md
```

Read it, then place/verify CYCLE/JUDGMENT.

Bootstrap failure before canonical TASK placement:

```text
STOP
no report/export
no substantive project mutation
```

Inbound cleanup after canonical transport remains best-effort/non-blocking.

# 1. repository gate

After current artifact placement require:

```text
branch:
main

HEAD:
4cadcb45b44d5bb2a260d7fa9350626ce28ea875

HEAD tree:
7d98df6f74eba74427d1be3b0abe9a78ef91a29f

index:
empty
```

Expected Git-visible set excluding current active Task is exact 25 paths:

- `.aiassistant/tasks/done/20260908_2330_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-retry-2.md`
- `.aiassistant/records/aiscc/cycles/20260908_2330_aiscc-p2-3-decision-register-reconciliation-accepted-source-audit-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_2330_aiscc-p2-3-decision-register-reconciliation-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260909_0008_aiscc-p2-3-phase1a-static-scenario-resource-contract-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260909_0008_aiscc-p2-3-source-contract-audit-accepted-phase1a-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_0008_aiscc-p2-3-source-contract-audit-final-acceptance-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260909_0110_aiscc-p2-3-phase1a-test-failure-parameter-id-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_0110_aiscc-p2-3-phase1a-test-failure-parameter-id-judgment-1.md`
- `config/scenarios/schemas/resource-v1.schema.json`
- `config/scenarios/schemas/scenario-v1.schema.json`
- `config/scenarios/stockroom/v1/catalog.json`
- `config/scenarios/stockroom/v1/resource.json`
- `config/scenarios/stockroom/v1/s1-normal.json`
- `config/scenarios/stockroom/v1/s2-missing-evidence.json`
- `config/scenarios/stockroom/v1/s3-policy-conflict.json`
- `config/scenarios/stockroom/v1/s4-human-owned-claim.json`
- `config/scenarios/stockroom/v1/fixtures/missing-evidence.json`
- `config/scenarios/stockroom/v1/fixtures/policy-conflict.json`
- `config/scenarios/stockroom/v1/fixtures/human-owned-claim.json`
- `src/aiscc/scenarios/__init__.py`
- `src/aiscc/scenarios/models.py`
- `src/aiscc/scenarios/catalog.py`
- `tests/unit/scenarios/test_catalog.py`
- `tests/unit/scenarios/test_resource_identity.py`
- `tests/unit/scenarios/test_contracts.py`

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

No cleanup/restore/absorb.

# 2. predecessor implementation identity

All 17 Phase 1A implementation paths must exist.

Starting SHA-256 values:

- `config/scenarios/schemas/resource-v1.schema.json`  `bc4d25c0f898e6c78d6df0b4b359ee0b990094bf590666124dbe5c2fa60e8cb5`
- `config/scenarios/schemas/scenario-v1.schema.json`  `8ed61bb2dbb6c2391ad3dc0440f855cf47d3c7947c3d4e2beda700fce7949823`
- `config/scenarios/stockroom/v1/catalog.json`  `bbc94776d53c06b472ab8879971a0d52f7901f600e3e88f4dadd1abc0d37cd17`
- `config/scenarios/stockroom/v1/resource.json`  `a5b8c8a5bd7165073f37647eb791df0bc59aa7b73033d59dd5f3967bbff28a99`
- `config/scenarios/stockroom/v1/s1-normal.json`  `fcca50e5876c4b276cc0f3ab865abc1eae8376e3e4dd68f7d675878a1b1cccc8`
- `config/scenarios/stockroom/v1/s2-missing-evidence.json`  `7473b8ec6b808866f16184edf4267ce7b2757e32c7205feb646c25041f938f51`
- `config/scenarios/stockroom/v1/s3-policy-conflict.json`  `73704589a51f59228bb72e770532f9153d35183cf3c1708e5db5ab80f6220cbe`
- `config/scenarios/stockroom/v1/s4-human-owned-claim.json`  `f364408f8874967b693b80c05144d23e382a40fe5d368e330908548af3938d29`
- `config/scenarios/stockroom/v1/fixtures/missing-evidence.json`  `c9a430ae61452b841e6deb06220cf59b748d57e698aa6108ca8966f522a04d1c`
- `config/scenarios/stockroom/v1/fixtures/policy-conflict.json`  `f01d061b5625d3c5f1e0f154f2f8eca97e3b64a6bd5e77551231b836be31bb91`
- `config/scenarios/stockroom/v1/fixtures/human-owned-claim.json`  `1a4ab952c40e43680e5d352928d2e076e8957d71acdc9dfa4cbf4793e3a7d5d4`
- `src/aiscc/scenarios/__init__.py`  `18a0f227f6c9633de56b03dcf746edc59f315e368692446a18040a8c92d1323c`
- `src/aiscc/scenarios/models.py`  `09936eaa8c59dfcca7afd4fef9fdad31c7b5e97e576abf396854a826daf4190a`
- `src/aiscc/scenarios/catalog.py`  `597a0788700d3302808b72771230636a5e5959ad68fea08183f457c9379e5a2d`
- `tests/unit/scenarios/test_catalog.py`  `8e2d1a20d25bb2be79bb6d8acff5d0fe2b3d42288e6a3f1b33996487980d7ba5`
- `tests/unit/scenarios/test_resource_identity.py`  `d5a0e2b125bc355f37c6e25e701c0281a42b1d97dfc52236409e004f6e3013fd`
- `tests/unit/scenarios/test_contracts.py`  `d72b4f2acccefb8b0dd5069005b49d21f90a12424adf79e8e5de4906171b2784`

Before rework require:

```text
17 / 17 exact
```

Mismatch:

```text
PREDECESSOR_IMPLEMENTATION_IDENTITY_MISMATCH
→ STOP
```

# 3. exact mutation authority

Only this existing untracked candidate file may change:

```text
tests/unit/scenarios/test_catalog.py
```

No other source/config/test/governance file may be edited.

The allowed semantic edit is only the malformed-input pytest parameterization that currently includes:

```text
b'{"schema_id": "x", "schema_id": "y"}'
b'{"x": NaN}'
b'{"x": Infinity}'
b'{"schema_id":'
b"\xff"
b"[]"
b"null"
b" " * 131073
```

Add concise explicit parameter IDs so pytest never derives a node ID from the full payload.

Recommended IDs:

```text
duplicate-key
nan
infinity
truncated-json
invalid-utf8
array-root
null-root
oversize
```

Equivalent short stable IDs are allowed.

Do NOT change:

```text
the eight payload values
the 131073-byte size
test function body
expected ContractError assertion
loader size limit
catalog/source/config implementation
other parameterized tests
```

If another change is required:

```text
SCOPE_EXPANSION_REQUIRED
→ STOP
```

# 4. exact required Windows test

Run exactly:

```text
.venv/Scripts/python.exe -B -m pytest -q -p no:cacheprovider --confcutdir=tests/unit/scenarios tests/unit/scenarios/test_catalog.py tests/unit/scenarios/test_resource_identity.py tests/unit/scenarios/test_contracts.py
```

No package installation/network/environment provisioning.

Required success:

```text
exit:
0

all collected cases:
PASS

setup errors:
0

teardown errors:
0

failed assertions:
0
```

The oversized-input case must be visibly represented by the explicit short parameter ID and must execute its assertion body.

If test exit is nonzero:

```text
TEST_FAILURE
→ STOP
```

No same-turn further source/test repair.

# 5. post-test identity verification

Require:

```text
16 predecessor implementation paths:
SHA unchanged exact

tests/unit/scenarios/test_catalog.py:
SHA changed from predecessor

only semantic diff:
explicit parameter IDs for malformed-input parameterization
```

Also require:

```text
all 11 config JSON parse
exact four scenarios
resource aggregate:
be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d

git diff --check:
PASS

index:
empty

existing tracked files modified:
0
```

Do not run scenario/runtime/provider/DB/Replay execution.

# 6. final workspace

Before current Task lifecycle:

```text
governance pending:
8 exact

implementation:
17 exact

Git-visible excluding active Task:
25 exact

index:
empty
```

Then:

```text
.aiassistant/tasks/active/20260909_0110_aiscc-p2-3-phase1a-windows-pytest-parameter-id-rework-1.md
→
.aiassistant/tasks/done/20260909_0110_aiscc-p2-3-phase1a-windows-pytest-parameter-id-rework-1.md
```

Final:

```text
26 exact Git-visible paths
index empty
```

No Git add/commit.

# 7. evidence contract

executor_required:

- inbound ZIP/artifact transport
- exact workspace gate
- predecessor 17-file identity
- one-file test-harness rework diff
- exact three-module Windows test PASS
- post-test 17-file identity/inventory
- outbound bundle ZIP

reuse_allowed:

- 0008 static/config/source candidate under exact hashes
- 0008 112 passing cases as diagnostic history only
- 2330 accepted design

human_owned:

```text
new Human QA:
NOT_REQUIRED

public license:
HUMAN_PENDING / outside Task
```

not_required:

- runtime scenario execution
- provider/tool execution
- DB
- Replay
- browser QA
- deployment

forbidden:

- config/source changes beyond test_catalog.py metadata edit
- runtime enrollment/materialization
- Git add/commit/push
- P2-4/P3

# 8. export bundle + outbound ZIP

Bundle folder:

```text
.aiassistant/reports/target/20260909_0110_aiscc-p2-3-phase1a-windows-pytest-parameter-id-rework-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
REWORK_DIFF_VERIFICATION.md
TEST_VERIFICATION.md
IMPLEMENTATION_MANIFEST.md
```

Include byte-preserving project-relative copies of:

```text
current Cycle
current Judgment
current done Task
all 17 Phase 1A implementation paths
```

`IMPLEMENTATION_MANIFEST.md` must report final SHA-256 for all 17 paths and explicitly identify `test_catalog.py` as the sole changed predecessor implementation path.

After bundle completion automatically create:

```text
.aiassistant/reports/target/20260909_0110_aiscc-p2-3-phase1a-windows-pytest-parameter-id-rework-1.zip
```

Require readable/CRC-valid archive, one top-level bundle directory, required root files, manifest coverage and folder/archive byte equality.

# 9. mandatory stop

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
PREDECESSOR_IMPLEMENTATION_IDENTITY_MISMATCH
SCOPE_EXPANSION_REQUIRED
TEST_FAILURE
UNEXPECTED_WORKSPACE_DELTA
ZIP_EXPORT_FAILED
```

Inbound cleanup refusal after canonical transport is non-blocking.

# 10. final ceiling

Success:

```text
P2-3 Phase 1A static scenario/resource contract implementation:
READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT

P2-3 runtime enrollment/materialization:
NOT_STARTED

P2-3 actual run capture:
NOT_STARTED

P2-3 Replay implementation:
NOT_STARTED
```

Do not declare P2-3 closed.
