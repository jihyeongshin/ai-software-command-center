# 작업지시서: P2-3 Phase 1B-B2 first-suite contract rework

## meta

- task_id: `20260909_1800_aiscc-p2-3-phase1b-b2-first-suite-contract-rework-1`
- created_at: `2026-09-09T18:00:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `BOUNDED_BACKEND_REWORK / SECURITY_SANDBOX_REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `0f5f19c8f8109e192275d1123f90ae50120be203`
- required_base_tree: `750ea4882f5d8688d1be20ea953b710a21c1052c`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. inbound ZIP bootstrap

The Browser Short Prompt's exact delivery ZIP SHA-256 is the bootstrap integrity anchor.

Current delivery ZIP contains:

```text
TASK:
20260909_1800_aiscc-p2-3-phase1b-b2-first-suite-contract-rework-1.md

CYCLE:
20260909_1800_aiscc-p2-3-phase1b-b2-test-failure-contract-rework-entry-1.cycle.md
SHA-256:
4e31117d68f02a3e3d295940610ce04991e01cfc1e48230ff4f2938bbfa6c86e
destination:
.aiassistant/records/aiscc/cycles/20260909_1800_aiscc-p2-3-phase1b-b2-test-failure-contract-rework-entry-1.cycle.md

JUDGMENT:
20260909_1800_aiscc-p2-3-phase1b-b2-first-suite-test-failure-judgment-1.md
SHA-256:
cc2461db492d9a5af1d3af7e056bde30297e50d27254b7894bd370a57c9ae7a9
destination:
.aiassistant/reports/aiscc/20260909_1800_aiscc-p2-3-phase1b-b2-first-suite-test-failure-judgment-1.md

HANDOFF:
none
```

Place TASK first at:

```text
.aiassistant/tasks/active/20260909_1800_aiscc-p2-3-phase1b-b2-first-suite-contract-rework-1.md
```

Read it, then place/hash-verify CYCLE/JUDGMENT.

Bootstrap failure before canonical TASK placement:

```text
STOP
no report/export
no substantive project mutation
```

After canonical transport, inbound cleanup refusal is non-blocking.

# 1. repository gate

Require:

```text
branch:
main

HEAD:
0f5f19c8f8109e192275d1123f90ae50120be203

HEAD tree:
750ea4882f5d8688d1be20ea953b710a21c1052c

index:
empty
```

Expected Git-visible set excluding current active Task is exact 21 paths:

- `.aiassistant/tasks/done/20260909_1648_aiscc-p2-3-phase1b-b2-scenario-tool-provider-security-enrollment-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260909_1648_aiscc-p2-3-b1-state-reconciliation-accepted-b2-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_1648_aiscc-p2-3-b1-state-reconciliation-final-acceptance-judgment-1.md`
- `src/aiscc/scenarios/enrollment.py`
- `src/aiscc/providers/stockroom_tool.py`
- `src/aiscc/providers/local_deterministic.py`
- `src/aiscc/security/stockroom_policy.py`
- `config/providers/stockroom-owner-profiles.v1.toml`
- `config/providers/stockroom-tools.v1.toml`
- `config/security/stockroom-owner.v1.toml`
- `tests/unit/scenarios/test_runtime_enrollment.py`
- `tests/unit/providers/test_stockroom_tool.py`
- `tests/unit/providers/test_local_deterministic.py`
- `tests/unit/security/test_stockroom_policy.py`
- `src/aiscc/providers/ports.py`
- `src/aiscc/providers/tools.py`
- `src/aiscc/providers/service.py`
- `src/aiscc/runtime/docker.py`
- `src/aiscc/security/policy.py`
- `.aiassistant/records/aiscc/cycles/20260909_1800_aiscc-p2-3-phase1b-b2-test-failure-contract-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_1800_aiscc-p2-3-phase1b-b2-first-suite-test-failure-judgment-1.md`

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Do not cleanup/restore/stash/reset/absorb.

# 2. exact predecessor candidate identity

Require exact SHA-256 for all 19 predecessor pending paths:

- `.aiassistant/tasks/done/20260909_1648_aiscc-p2-3-phase1b-b2-scenario-tool-provider-security-enrollment-implementation-1.md`  `527cb6ac675efc935dabcbffa09f5e62f4f443b779f094c6f0463c5e192521f0`
- `.aiassistant/records/aiscc/cycles/20260909_1648_aiscc-p2-3-b1-state-reconciliation-accepted-b2-entry-1.cycle.md`  `286e75593b24bf215f5c47e1339f41c5a5e3e32bdddd2cd6745cb5279db5472c`
- `.aiassistant/reports/aiscc/20260909_1648_aiscc-p2-3-b1-state-reconciliation-final-acceptance-judgment-1.md`  `643d3dbf8f8639966d78386bc632bd5645480fd7109f71f34bd179cb1807ecd6`
- `src/aiscc/scenarios/enrollment.py`  `b84e82d3078c8c3822007bc165a107be4f91a60b091b9d081fc72ac259c666fc`
- `src/aiscc/providers/stockroom_tool.py`  `8cb8113534077970600a6c203334818db49053e89694e851cb300f6bb01c2944`
- `src/aiscc/providers/local_deterministic.py`  `d7fd527fec919bd3488e4a22a3e24ff357d262076de83785f75698548708399d`
- `src/aiscc/security/stockroom_policy.py`  `ccf8b2ce282a93c11a864413b99d5f2384db4032b49660cf815e33778f7f06e2`
- `config/providers/stockroom-owner-profiles.v1.toml`  `82de20f5a2aa76e039e685fcacbc2da44cd04b2dd863ebb9dd8e9ff7b8e37eee`
- `config/providers/stockroom-tools.v1.toml`  `223c45f224e4aba6ae7f023ed6752b4730e9889d4878cf6d4a053eed71bd457c`
- `config/security/stockroom-owner.v1.toml`  `88b3b015b3b52ceb9338025945abf5b4e422d0efe9c2a021fe7f15e46f6dae15`
- `tests/unit/scenarios/test_runtime_enrollment.py`  `26c270f8bdd5b06f41cb97427752d90a6e8de970f7e4a0f250689fe114c8c10c`
- `tests/unit/providers/test_stockroom_tool.py`  `5d3629381b97cd0d6a449b399b0f1acce156b24e17089cf229fce4feb7641f9d`
- `tests/unit/providers/test_local_deterministic.py`  `7280db790d1d942e851b67ad0f22816ab33d0af6b34e2d51813a599f9ba38870`
- `tests/unit/security/test_stockroom_policy.py`  `d76ef98f121651820c587067295d1a59bfbae12fa02ff598020cfa519124beb0`
- `src/aiscc/providers/ports.py`  `8489359ea53c28e41bdf5e0f0d4970f567f0e763bee96f9f599cffc5a5ebfec4`
- `src/aiscc/providers/tools.py`  `0718889ccf4e98eeb18486b740e741fef005b7d580abd5cfd7c8452f2ffb9b3d`
- `src/aiscc/providers/service.py`  `f21c3c29443446650e31fb0d4d0d30ceddb8956d51ad2e17221536102c6c5c18`
- `src/aiscc/runtime/docker.py`  `196b8568e950a8d422feaceb1fd6601ab7478d4f3488d4f29ddb20c7059891c5`
- `src/aiscc/security/policy.py`  `ecb008330040966436c87d24aba0245627691cb076c4c77b6778b646b074cfe9`

Any mismatch:

```text
PREDECESSOR_IMPLEMENTATION_IDENTITY_MISMATCH
→ STOP
```

# 3. exact mutation authority

Only these three existing B2 candidate files may change:

```text
src/aiscc/scenarios/enrollment.py
src/aiscc/providers/stockroom_tool.py
src/aiscc/security/stockroom_policy.py
```

All other 13 B2 product/config/test paths must remain byte-exact:

- `src/aiscc/providers/local_deterministic.py`  `d7fd527fec919bd3488e4a22a3e24ff357d262076de83785f75698548708399d`
- `config/providers/stockroom-owner-profiles.v1.toml`  `82de20f5a2aa76e039e685fcacbc2da44cd04b2dd863ebb9dd8e9ff7b8e37eee`
- `config/providers/stockroom-tools.v1.toml`  `223c45f224e4aba6ae7f023ed6752b4730e9889d4878cf6d4a053eed71bd457c`
- `config/security/stockroom-owner.v1.toml`  `88b3b015b3b52ceb9338025945abf5b4e422d0efe9c2a021fe7f15e46f6dae15`
- `tests/unit/scenarios/test_runtime_enrollment.py`  `26c270f8bdd5b06f41cb97427752d90a6e8de970f7e4a0f250689fe114c8c10c`
- `tests/unit/providers/test_stockroom_tool.py`  `5d3629381b97cd0d6a449b399b0f1acce156b24e17089cf229fce4feb7641f9d`
- `tests/unit/providers/test_local_deterministic.py`  `7280db790d1d942e851b67ad0f22816ab33d0af6b34e2d51813a599f9ba38870`
- `tests/unit/security/test_stockroom_policy.py`  `d76ef98f121651820c587067295d1a59bfbae12fa02ff598020cfa519124beb0`
- `src/aiscc/providers/ports.py`  `8489359ea53c28e41bdf5e0f0d4970f567f0e763bee96f9f599cffc5a5ebfec4`
- `src/aiscc/providers/tools.py`  `0718889ccf4e98eeb18486b740e741fef005b7d580abd5cfd7c8452f2ffb9b3d`
- `src/aiscc/providers/service.py`  `f21c3c29443446650e31fb0d4d0d30ceddb8956d51ad2e17221536102c6c5c18`
- `src/aiscc/runtime/docker.py`  `196b8568e950a8d422feaceb1fd6601ab7478d4f3488d4f29ddb20c7059891c5`
- `src/aiscc/security/policy.py`  `ecb008330040966436c87d24aba0245627691cb076c4c77b6778b646b074cfe9`

No governance file may be edited except current Task lifecycle.

No additional product/config/test path may be created or modified.

If another path is required:

```text
SCOPE_EXPANSION_REQUIRED
→ STOP
```

# 4. fix 1 — canonical ScenarioCatalog integration

Current defect:

```text
compile_stockroom_selection(..., catalog=...)
expects exact CatalogDocument
but canonical load_catalog returns ScenarioCatalog
```

Use the canonical Phase 1A type:

```text
aiscc.scenarios.catalog.ScenarioCatalog
```

Required resolution in:

```text
src/aiscc/scenarios/enrollment.py
```

Semantics:

```text
compile_stockroom_selection(
    selection,
    *,
    catalog: ScenarioCatalog,
    owner_context
)
```

or an exact repository-style equivalent that accepts only the canonical `load_catalog()` boundary.

Preserve fail-closed server ownership:

```text
type/identity must remain canonical
catalog.scenarios must be exact SCENARIO_IDS
catalog.resource.resource_ref must equal accepted RESOURCE_REF
catalog.document.resource_ref must equal accepted RESOURCE_REF
scenario version/resource binding must remain exact
```

Do not:

```text
accept arbitrary duck-typed requester objects
accept CatalogDocument alone
reload from filesystem inside compile
weaken scenario_id-only public selection
change Phase 1A catalog/models
```

The existing unchanged enrollment tests must pass.

# 5. fix 2 — typed unresolved receipt classification

Current defect:

```text
StockroomSummaryDispatcher.dispatch_with_receipts
uses zip(..., strict=True) before cardinality resolution

missing receipts:
generic ValueError
```

Modify only:

```text
src/aiscc/providers/stockroom_tool.py
```

Before strict pairing, establish exact consumed-receipt cardinality/binding.

Required behavior:

```text
len(receipts) != len(requirements)
→ UnknownToolOutcome("STOCKROOM_PROCESS_RECEIPT_UNRESOLVED")
```

Then require exactly one PROCESS receipt/requirement pair.

Any missing/extra/ambiguous PROCESS consumed-receipt crossing:

```text
UnknownToolOutcome
```

not:

```text
ValueError
KnownToolFailure
known completion
```

Receipt forgery/stale/cross-run/cross-state/cross-spec behavior remains fail-closed through existing verification.

Do not modify `providers/tools.py`, `runtime/docker.py`, capability issuance, or receipt-claim semantics.

# 6. fix 3 — full finite-limit security intersection

Current defect:

```text
PROCESS scope may remain eligible when:
remaining_provider_calls == 0
or
remaining_tool_calls == 0
```

Modify only:

```text
src/aiscc/security/stockroom_policy.py
```

The sealed Stockroom owner context must require the full finite-limit intersection before any Stockroom domain is eligible.

At minimum common eligibility must require:

```text
0 < remaining_provider_calls <= scenario.provider_call_limit
0 < remaining_tool_calls <= config.tool_calls
0 < remaining_process_calls <= config.process_calls
0 < remaining_seconds <= config.attempt_timeout_seconds
0 < remaining_budget_units <= config.budget_units
```

Domain-specific checks may remain stricter, including:

```text
S3 tool_allowed=false
NETWORK always denied
SECRET requires provider capacity
```

Do not:

```text
grant capability in StockroomOwnerRestriction
change public profiles
weaken base SecurityPolicy
change hard security baseline
change owner config TOML
```

The unchanged security test parameter cases for exhausted provider/tool/process limits must all deny.

# 7. no test modification

These four B2 new test modules must remain exact bytes:

```text
tests/unit/scenarios/test_runtime_enrollment.py
SHA-256:
26c270f8bdd5b06f41cb97427752d90a6e8de970f7e4a0f250689fe114c8c10c

tests/unit/providers/test_stockroom_tool.py
SHA-256:
5d3629381b97cd0d6a449b399b0f1acce156b24e17089cf229fce4feb7641f9d

tests/unit/providers/test_local_deterministic.py
SHA-256:
7280db790d1d942e851b67ad0f22816ab33d0af6b34e2d51813a599f9ba38870

tests/unit/security/test_stockroom_policy.py
SHA-256:
d76ef98f121651820c587067295d1a59bfbae12fa02ff598020cfa519124beb0
```

They correctly exposed the product defects.

Do not alter expected outcomes to make tests pass.

# 8. static checks

Before mandatory pytest:

```text
Python compile:
three modified product files + unchanged four new B2 test modules

Ruff:
same exact Python scope

three B2 TOML files:
byte-exact predecessor hashes and strict loader PASS

git diff --check:
PASS

index:
empty
```

No dependency/network/environment change.

# 9. first mandatory B2 unit rerun

Run exactly:

```text
.venv/Scripts/python.exe -B -m pytest -q -p no:cacheprovider tests/unit/scenarios/test_runtime_enrollment.py tests/unit/providers/test_stockroom_tool.py tests/unit/providers/test_local_deterministic.py tests/unit/security/test_stockroom_policy.py
```

Required:

```text
exit 0
failed 0
errors 0
```

Explicitly report total passed/skipped count.

If nonzero:

```text
TEST_FAILURE
→ STOP
```

No same-turn second repair or source/test mutation after the failure.

# 10. required shared regressions after first suite PASS

Only after section 9 PASS, run:

```text
.venv/Scripts/python.exe -B -m pytest -q -p no:cacheprovider tests/unit/providers/test_tools.py tests/unit/providers/test_service.py tests/unit/security/test_permission_policy.py
```

The predecessor bounded discovery reported:

```text
direct Docker unit module:
NO_EXISTING_DIRECT_DOCKER_UNIT_MODULE
```

Confirm by bounded filename/symbol search only; do not broaden into integration suites.

If one exact direct Docker unit module now resolves without changing the path set, run it separately.
If none, report `NO_EXISTING_DIRECT_DOCKER_UNIT_MODULE`.
If ambiguous:

```text
TEST_SCOPE_AMBIGUOUS
→ STOP
```

Any regression command nonzero:

```text
TEST_FAILURE
→ STOP
```

No same-turn repair.

# 11. strict non-execution boundary

All verification remains:

```text
0 real provider/network/socket/HTTP/OpenAI
0 Docker/container CLI
0 Stockroom CLI/module execution
0 DB
0 repository materialization
0 scenario driver
0 Replay
```

Use only unit/static/fake collaborators already present.

# 12. post-test byte/scope verification

Require:

```text
three authorized product files:
changed from predecessor

other 13 B2 product/config/test files:
exact predecessor hashes

B2 total path set:
16 exact

other product/config/test delta:
0

B1 files:
unchanged

Phase 1A files:
unchanged

bootstrap.py:
unchanged

dependency manifests:
unchanged

migration:
none

index:
empty

git diff --check:
PASS

Git-visible pyc/__pycache__/pytest cache:
none
```

# 13. final workspace

Before current Task lifecycle:

```text
predecessor pending:
19 exact paths

current Cycle/Judgment:
2 exact paths

Git-visible excluding active Task:
21 exact

index:
empty
```

Then move:

```text
.aiassistant/tasks/active/20260909_1800_aiscc-p2-3-phase1b-b2-first-suite-contract-rework-1.md
→
.aiassistant/tasks/done/20260909_1800_aiscc-p2-3-phase1b-b2-first-suite-contract-rework-1.md
```

Final:

```text
22 exact Git-visible paths
index empty
```

No Git add/commit.

# 14. evidence contract

executor_required:

- inbound ZIP/artifact transport
- exact 21-path repository preflight
- 19-path predecessor identity
- exact three-file product rework
- unchanged four-test proof
- first B2 suite PASS
- existing provider/security shared regressions PASS
- direct Docker module bounded discovery/result
- exact 16-path final B2 identity
- final 22-path workspace
- outbound result ZIP

reuse_allowed:

- unchanged 13 B2 paths under exact hashes
- 1648 local deterministic provider PASS as diagnostic history only
- accepted 1329 Phase 1B design
- persisted B1

human_owned:

```text
new Human QA:
NOT_REQUIRED

public license:
HUMAN_PENDING / outside B2
```

not_required:

```text
B3
actual scenario capture
real provider/tool/Docker execution
DB
Replay
Browser QA
deployment
```

forbidden:

```text
test edits
providers/tools.py re-edit
providers/service.py re-edit
runtime/docker.py re-edit
security/policy.py re-edit
B1 or Phase 1A mutation
new dependency
network
Docker
scenario execution
Git add/commit/push
P2-4/P3
```

# 15. mandatory stop

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
BLOCKED_RUNTIME_PREREQUISITE
TEST_SCOPE_AMBIGUOUS
TEST_FAILURE
CONTRACT_MISMATCH
UNEXPECTED_WORKSPACE_DELTA
ZIP_EXPORT_FAILED
```

Inbound cleanup refusal after canonical transport is non-blocking.

# 16. export bundle + outbound ZIP

Bundle folder:

```text
.aiassistant/reports/target/20260909_1800_aiscc-p2-3-phase1b-b2-first-suite-contract-rework-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
IMPLEMENTATION_MANIFEST.md
REWORK_DIFF_VERIFICATION.md
ENROLLMENT_CONTRACT_VERIFICATION.md
TOOL_AUTHORITY_VERIFICATION.md
LOCAL_PROVIDER_VERIFICATION.md
SECURITY_POLICY_VERIFICATION.md
TEST_VERIFICATION.md
```

Include byte-preserving project-relative copies of:

```text
current Cycle
current Judgment
current done Task
all 16 final B2 product/config/test paths
```

After folder completion create:

```text
.aiassistant/reports/target/20260909_1800_aiscc-p2-3-phase1b-b2-first-suite-contract-rework-1.zip
```

Require readable/CRC PASS, one top-level bundle directory, required root files, manifest coverage and folder/archive byte equality.

# 17. final ceiling

Success:

```text
P2-3 Phase 1B-B2:
READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT

P2-3 Phase 1B-B3:
NOT_STARTED

actual scenario capture:
NOT_STARTED

Replay:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

Do not declare Phase 1B or P2-3 closed.
