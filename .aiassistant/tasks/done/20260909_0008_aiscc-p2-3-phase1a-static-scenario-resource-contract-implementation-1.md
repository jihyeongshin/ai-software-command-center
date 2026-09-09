# 작업지시서: P2-3 Phase 1A static scenario/resource contract implementation

## meta

- task_id: `20260909_0008_aiscc-p2-3-phase1a-static-scenario-resource-contract-implementation-1`
- created_at: `2026-09-09T00:08:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `DEMO_SCENARIO / BOUNDED_BACKEND_IMPLEMENTATION`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P2-3 static scenario/resource contract`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `4cadcb45b44d5bb2a260d7fa9350626ce28ea875`
- required_base_tree: `7d98df6f74eba74427d1be3b0abe9a78ef91a29f`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `read-only P2-3 design audit → source/config/test mutation authority`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. inbound ZIP bootstrap

The Browser Short Prompt's exact delivery ZIP SHA-256 is the bootstrap integrity anchor.

Current delivery ZIP contains only:

```text
TASK:
20260909_0008_aiscc-p2-3-phase1a-static-scenario-resource-contract-implementation-1.md

CYCLE:
20260909_0008_aiscc-p2-3-source-contract-audit-accepted-phase1a-entry-1.cycle.md
SHA-256:
23c0b64e09ecfdf7c4bb27a1842c2be30eb6e341ffc9d25dc4835d39970e979a
destination:
.aiassistant/records/aiscc/cycles/20260909_0008_aiscc-p2-3-source-contract-audit-accepted-phase1a-entry-1.cycle.md

JUDGMENT:
20260909_0008_aiscc-p2-3-source-contract-audit-final-acceptance-judgment-1.md
SHA-256:
ccba59565758e52c3ee89c5daf0bcda0dd6baefe767754497ea2afa14da381a3
destination:
.aiassistant/reports/aiscc/20260909_0008_aiscc-p2-3-source-contract-audit-final-acceptance-judgment-1.md

HANDOFF:
none
```

Human downloads only the ZIP.

Executor:

1. verify exact ZIP filename/SHA-256;
2. validate archive readability/CRC/member safety;
3. materialize TASK first to `.aiassistant/tasks/active/20260909_0008_aiscc-p2-3-phase1a-static-scenario-resource-contract-implementation-1.md`;
4. read TASK;
5. materialize CYCLE/JUDGMENT directly to exact canonical destinations;
6. verify exact hashes.

Bootstrap failure before canonical TASK placement:

```text
STOP
no report/export
no substantive project mutation
ask Human to re-download/reposition ZIP
```

After canonical transport succeeds, inbound cleanup failure is non-blocking local residue.

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

Expected Git-visible governance set is exact five paths:

```text
.aiassistant/tasks/done/20260908_2330_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-retry-2.md
.aiassistant/records/aiscc/cycles/20260908_2330_aiscc-p2-3-decision-register-reconciliation-accepted-source-audit-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_2330_aiscc-p2-3-decision-register-reconciliation-final-acceptance-judgment-1.md
.aiassistant/records/aiscc/cycles/20260909_0008_aiscc-p2-3-source-contract-audit-accepted-phase1a-entry-1.cycle.md
.aiassistant/reports/aiscc/20260909_0008_aiscc-p2-3-source-contract-audit-final-acceptance-judgment-1.md
```

Current active Task is ignored.

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

No cleanup/restore/absorb.

# 2. predecessor identity

Verify exact SHA-256:

- `.aiassistant/tasks/done/20260908_2330_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-retry-2.md`  `1b55a92948cbad4fb86e1d48f5925f38faee8d9662a9da71d320cef1d88bb284`
- `.aiassistant/records/aiscc/cycles/20260908_2330_aiscc-p2-3-decision-register-reconciliation-accepted-source-audit-retry-entry-1.cycle.md`  `016afc405faa85dd0725445ceb8c559130f1d4c58b3fdaf05827d806dc567f61`
- `.aiassistant/reports/aiscc/20260908_2330_aiscc-p2-3-decision-register-reconciliation-final-acceptance-judgment-1.md`  `e93888c32e371d95961286ebe626344a3251c121aadb780c27888bff510872d0`

Mismatch:

```text
PREDECESSOR_PROVENANCE_IDENTITY_MISMATCH
→ STOP
```

# 3. must-read authority

Read fully:

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md
.aiassistant/rules/AISCC_SECURITY_SANDBOX.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/reports/aiscc/AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md

.aiassistant/records/aiscc/cycles/20260908_2330_aiscc-p2-3-decision-register-reconciliation-accepted-source-audit-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_2330_aiscc-p2-3-decision-register-reconciliation-final-acceptance-judgment-1.md
.aiassistant/records/aiscc/cycles/20260909_0008_aiscc-p2-3-source-contract-audit-accepted-phase1a-entry-1.cycle.md
.aiassistant/reports/aiscc/20260909_0008_aiscc-p2-3-source-contract-audit-final-acceptance-judgment-1.md

examples/synthetic-stockroom/README.md
examples/synthetic-stockroom/PROVENANCE.md
```

Bounded source reads are allowed for existing conventions in:

```text
src/aiscc/
tests/unit/
config/
```

Do not bulk-read unrelated history.

# 4. accepted Phase 1A contract

## resource identity

Implement machine-readable static authority for exactly:

```text
resource_schema:
AISCC-SYNTHETIC-RESOURCE-V1

resource_id:
repository:synthetic-stockroom

resource_version:
be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d

resource_ref:
repository:synthetic-stockroom@be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d

source_commit:
05185c57a6265a4002050ce25cdfde3dc87e9779

subroot:
examples/synthetic-stockroom/

git_subtree:
f3d9203321ae3535abf8e92a7285da1067f6c55e

file_count:
14

aggregate_algorithm:
AISCC-SOURCE-MANIFEST-SHA256-V1

aggregate_sha256:
be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d
```

No mutable `latest`.

## scenario pack

Exactly four:

```text
stockroom-s1-normal
stockroom-s2-missing-evidence
stockroom-s3-policy-conflict
stockroom-s4-human-owned-claim
```

All:

```text
scenario_version:
1.0.0

resource_ref:
repository:synthetic-stockroom@be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d
```

# 5. exact mutation allowlist

Only these product/config/test paths may be created:

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

No existing tracked file may be modified.

If implementation cannot be completed within these exact paths:

```text
SCOPE_EXPANSION_REQUIRED
→ STOP
```

Do not broaden scope.

# 6. config directory contract

Create:

```text
config/scenarios/schemas/resource-v1.schema.json
config/scenarios/schemas/scenario-v1.schema.json
```

and:

```text
config/scenarios/stockroom/v1/catalog.json
config/scenarios/stockroom/v1/resource.json
config/scenarios/stockroom/v1/s1-normal.json
config/scenarios/stockroom/v1/s2-missing-evidence.json
config/scenarios/stockroom/v1/s3-policy-conflict.json
config/scenarios/stockroom/v1/s4-human-owned-claim.json
config/scenarios/stockroom/v1/fixtures/missing-evidence.json
config/scenarios/stockroom/v1/fixtures/policy-conflict.json
config/scenarios/stockroom/v1/fixtures/human-owned-claim.json
```

All JSON:

```text
UTF-8
deterministic key/value semantics
no comments
no path/user/provider/credential injection
strict unknown-field rejection at loader boundary
```

# 7. resource schema semantics

`resource-v1.schema.json` and loader model must require exact typed fields sufficient to bind:

```text
schema_id
schema_version
resource_id
resource_version
resource_ref
source_commit
subroot
git_subtree
file_count
aggregate_algorithm
aggregate_sha256
files
```

`files` contains exactly the accepted 14-file manifest with:

```text
path
mode
bytes
sha256
```

Rules:

```text
relative POSIX path only
no absolute path
no .. segment
no duplicate path
mode = 100644 only for v1
sha256 = lowercase 64 hex
file_count = len(files)
sorted unique path order
resource_ref derived/equal to resource_id@resource_version
resource_version = aggregate_sha256 for v1
```

The loader must reject inconsistent identity rather than normalize it silently.

# 8. aggregate algorithm

Implement pure deterministic calculation for:

```text
AISCC-SOURCE-MANIFEST-SHA256-V1
```

Input:

```text
ascending ASCII subroot-relative paths

for each file:
mode<TAB>path<TAB>decimal-byte-count<TAB>lowercase-SHA256<LF>
```

Expected:

```text
be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d
```

This Phase 1A verifies manifest identity only.

It does NOT yet implement historical Git commit extraction/materialization.

# 9. scenario schema semantics

Each scenario file must include strict versioned fields sufficient to freeze:

```text
scenario_id
scenario_version
purpose
resource_ref
task_contract
allowed_actions
forbidden_actions
user_parameters
expected_workflow
evidence_contract
judgment_contract
cycle_next_action_contract
recording_contract
public_disclosure
fixture_refs
```

`user_parameters` for v1 is empty / no arbitrary parameter surface.

`task_contract` must distinguish:

```text
goal
non_goals
```

`evidence_contract` must represent all five ownership classes explicitly:

```text
executor_required
reuse_allowed
human_owned
not_required
forbidden
```

Do not collapse them into a generic evidence list.

# 10. exact four-scenario semantics

## S1 normal

Require machine-readable semantics equivalent to:

```text
goal:
fixed Stockroom summary proof

expected:
READY -> RUNNING -> ADMISSION_PENDING -> ACCEPTED

Judgment:
SYSTEM_DETERMINISTIC / ACCEPTED

Human per-run:
not required

runtime AdmittedCycle:
eligible only after accepted terminal lineage
```

No runtime claim is made in config.

## S2 missing-evidence

Fixture:

```text
fixtures/missing-evidence.json
```

must express a server-owned controlled omission of the required summary-runtime evidence candidate.

Expected:

```text
READY -> RUNNING -> ADMISSION_PENDING
ACCEPTED request denied without version mutation
HOLD_REWORK_REQUIRED Judgment
REWORK_REQUIRED
```

No same-run automatic retry.

No accepted outcome because the negative demonstration itself succeeded.

## S3 policy-conflict

Fixture:

```text
fixtures/policy-conflict.json
```

must bind both synthetic policies:

```text
inclusive-reorder-baseline-v1:
reorder when available <= threshold

strict-reorder-request-v1:
requested replacement uses available < threshold
```

Expected:

```text
READY -> RUNNING -> BLOCKED
blocker_type:
POLICY

blocker_reason:
POLICY_CONFLICT
```

No source mutation.
No security-boundary substitution.
No authoritative outcome Judgment at this capture boundary.

## S4 human-owned-claim

Fixture:

```text
fixtures/human-owned-claim.json
```

must be explicitly synthetic/adversarial and encode an Agent-produced false claim equivalent to:

```text
Human browser QA completed
```

It MUST NOT be represented as actual Human input.

Expected:

```text
READY -> RUNNING -> ADMISSION_PENDING
wrong-owner Human candidate rejected
ACCEPTED request denied without version mutation
fresh PRE_HUMAN attestation
HUMAN_REQUIRED
Human result absent/pending
```

Human-owned requirement must remain explicit.

No fabricated HumanResult/Judgment/Cycle.

# 11. public selector boundary

`catalog.json` must expose only four exact scenario IDs.

Machine-readable public selection schema semantics:

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["scenario_id"],
  "properties": {
    "scenario_id": {
      "type": "string",
      "enum": [
        "stockroom-s1-normal",
        "stockroom-s2-missing-evidence",
        "stockroom-s3-policy-conflict",
        "stockroom-s4-human-owned-claim"
      ]
    }
  }
}
```

Do not add user task text, path, repo, URL, command, provider, model or arbitrary parameters.

# 12. Python model/loader boundary

Implement only:

```text
src/aiscc/scenarios/__init__.py
src/aiscc/scenarios/models.py
src/aiscc/scenarios/catalog.py
```

Required behavior:

```text
typed immutable/frozen representation
strict load from explicit configured paths
unknown field rejection
duplicate scenario ID/version rejection
unknown resource_ref rejection
fixture path traversal rejection
duplicate fixture ref rejection
scenario ID/version exact binding
resource manifest aggregate verification
deterministic catalog ordering
fail closed on malformed/missing file
```

No global implicit discovery from arbitrary filesystem roots.

No network.

No shell/process execution.

No provider/tool/runtime execution.

No bootstrap registration.

# 13. dependency rule

Do not add or change dependencies.

If an already-declared schema library exists, it may be used.

If not, implement the bounded validation required by this Task using existing project facilities / Python standard library.

Do not edit dependency manifests.

# 14. tests

Create only:

```text
tests/unit/scenarios/test_catalog.py
tests/unit/scenarios/test_resource_identity.py
tests/unit/scenarios/test_contracts.py
```

Tests must cover at minimum:

## positive

```text
4 exact scenarios load
all version 1.0.0
all bind exact resource_ref
resource aggregate exact
catalog order deterministic
five-way evidence contract retained
selector admits exactly four IDs
```

## negative

```text
unknown field
unknown scenario ID
duplicate scenario
duplicate fixture ref
unknown resource_ref
absolute fixture path
.. traversal
wrong aggregate
wrong file_count
wrong file hash syntax
mutable/latest-like resource version
nonempty/arbitrary user parameters
S4 Human claim misclassified as Human-owned result
S2 omission missing from fixture
S3 conflict fixture absent/inconsistent
```

Tests must not execute Synthetic Stockroom CLI/build/test suite as scenario runtime.

Reading the fixed source manifest is allowed.

# 15. verification

Use the repository's existing local test environment only.

No package installation/network/environment provisioning.

Run the narrowest existing test command that executes exactly the three new test modules.

Also verify:

```text
all config JSON parses
no extra scenario config files
exact 17 mutation paths only
no existing tracked-file modification
git diff --check PASS
index empty
no Git add/commit
```

If the required existing test environment is unavailable:

```text
BLOCKED_RUNTIME_PREREQUISITE
→ STOP
```

Do not install/fetch.

# 16. non-goals / forbidden

This Task does NOT authorize:

```text
src/aiscc/scenarios/enrollment.py
src/aiscc/scenarios/driver.py
src/aiscc/runtime/synthetic_repository.py
src/aiscc/providers/stockroom_tools.py
recording/replay implementation
security config mutation
provider/tool config mutation
bootstrap.py mutation
migration
DB access/mutation
Docker/container run
actual scenario execution
provider/LLM call
Replay generation
public/replay API
public corpus
license clearance
Git add/commit/push
P2-4/P3
```

Any need for these:

```text
SCOPE_EXPANSION_REQUIRED
→ STOP
```

# 17. expected final workspace

After implementation and before Task lifecycle:

```text
governance pending:
5 exact paths

implementation:
17 exact paths

total Git-visible excluding active Task:
22 exact paths

index:
empty
```

Then move current Task:

```text
.aiassistant/tasks/active/20260909_0008_aiscc-p2-3-phase1a-static-scenario-resource-contract-implementation-1.md
→
.aiassistant/tasks/done/20260909_0008_aiscc-p2-3-phase1a-static-scenario-resource-contract-implementation-1.md
```

Final:

```text
23 exact Git-visible paths
index empty
```

No other path.

# 18. evidence contract

executor_required:

- inbound ZIP bootstrap / artifact transport
- workspace Git preflight
- predecessor provenance identity
- exact config/schema/source implementation
- unit/static verification
- negative contract verification
- exact final workspace inventory
- outbound result ZIP

reuse_allowed:

- accepted 2330 resource/scenario design
- P2-2 exact 14-file source identity
- accepted P1 owner semantics

human_owned:

```text
new Human QA:
NOT_REQUIRED

public license:
HUMAN_PENDING / not part of this Task
```

not_required:

```text
runtime scenario execution
provider execution
DB integration
Replay reader
browser QA
deployment
```

forbidden evidence substitution:

```text
unit test PASS != actual scenario run
config exists != runtime enrollment
static resource identity != materialized runtime repository
Agent claim != Human result
```

# 19. mandatory stop

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
SCOPE_EXPANSION_REQUIRED
DEPENDENCY_CHANGE_REQUIRED
BLOCKED_RUNTIME_PREREQUISITE
TEST_FAILURE
CONTRACT_MISMATCH
UNEXPECTED_EXISTING_PATH
UNEXPECTED_WORKSPACE_DELTA
```

After repository-level blocker, produce minimum report/export.

Inbound cleanup refusal after canonical transport remains non-blocking.

# 20. export bundle + outbound ZIP

Bundle folder:

```text
.aiassistant/reports/target/20260909_0008_aiscc-p2-3-phase1a-static-scenario-resource-contract-implementation-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
IMPLEMENTATION_MANIFEST.md
STATIC_CONTRACT_VERIFICATION.md
TEST_VERIFICATION.md
```

Include byte-preserving project-relative copies of:

```text
current Cycle
current Judgment
current done Task
all 17 implementation paths
```

Do not include unrelated unchanged source.

After folder completion create:

```text
.aiassistant/reports/target/20260909_0008_aiscc-p2-3-phase1a-static-scenario-resource-contract-implementation-1.zip
```

Require readable/CRC-valid archive, one top-level bundle directory, required root files, manifest coverage and folder/archive byte equality.

Keep folder and outbound ZIP.

# 21. inbound cleanup

After terminal outcome/outbound ZIP verification, attempt current inbound delivery ZIP cleanup best-effort.

Any refusal:

```text
NON_BLOCKING_LOCAL_RESIDUE
```

No broad Downloads cleanup.

# 22. final ceiling

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
