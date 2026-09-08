# 작업지시서: P2-2 Synthetic Stockroom candidate implementation

## meta

- task_id: `20260908_1549_aiscc-p2-2-synthetic-stockroom-candidate-implementation-1`
- created_at: `2026-09-08T15:49:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `DEMO / BACKEND_IMPLEMENTATION`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P2-2 fixed synthetic repository candidate asset`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `187880eff48cbf2909e0fcadce75c6d2cb30ab31`
- required_base_tree: `1823346f7ec7c4da466d64f6823f0c8b3390f0cd`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `read-only design audit → new source creation/executable verification authority boundary`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# current state

```text
P2-1:
ACCEPTED / CLOSED / PERSISTED

P2-2 source/contract audit:
ACCEPTED

P2-2 implementation:
AUTHORIZED / NOT_STARTED

P2-3:
NOT_STARTED
```

# Human-owned IDE session prerequisite

이번 Task는 Human이 새로 연 IDE Executor chat에서 시작한다.

Executor가 새 chat을 만들거나 같은 chat의 model/reasoning 변경을 fresh session으로 간주하지 않는다.

# 이번 턴 목표

1. accepted exact 14-file Synthetic Stockroom candidate를 생성한다.
2. Python 3.12.14 / standard-library-only / offline deterministic contract를 구현한다.
3. exact 20-test baseline을 구현하고 모두 통과시킨다.
4. deterministic `.pyz` build를 구현하고 repeat-build byte equality를 검증한다.
5. module CLI와 `.pyz` CLI의 exact output parity를 검증한다.
6. seed/source가 verification 과정에서 변하지 않았음을 증명한다.
7. bounded source/security/provenance checks를 수행한다.
8. implementation candidate를 Browser Command Center에 제출한다.
9. Git persistence와 P2-3는 수행하지 않는다.

# 비목표

- current AISCC application/runtime source 변경
- `src/aiscc/` 수정
- root `tests/`, `config/`, `containers/`, `migrations/`, `scripts/` 수정
- root `pyproject.toml`, `uv.lock`, `.python-version`, `.gitignore` 수정
- P1 security profile/resource/scenario ID 변경
- public Live enrollment
- scenario IDs/allowlist 작성
- actual AISCC scenario run
- Replay corpus 생성
- deployment
- Git add/commit/push
- Project Source mirror sync
- P2-3 시작

# 반드시 읽을 canonical source

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md

.aiassistant/reports/aiscc/AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md
.aiassistant/rules/AISCC_SECURITY_SANDBOX.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/records/aiscc/cycles/20260908_1549_aiscc-p2-2-source-contract-audit-final-acceptance-implementation-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_1549_aiscc-p2-2-source-contract-audit-final-acceptance-judgment-1.md
```

Task body is the exact implementation contract. Do not bulk-read predecessor target reports.

# artifact transport / initial repository gate

Current Command Center package contains only:

```text
TASK:
20260908_1549_aiscc-p2-2-synthetic-stockroom-candidate-implementation-1.md

CYCLE:
20260908_1549_aiscc-p2-2-source-contract-audit-final-acceptance-implementation-entry-1.cycle.md

JUDGMENT:
20260908_1549_aiscc-p2-2-source-contract-audit-final-acceptance-judgment-1.md

HANDOFF:
none
```

Transport must PASS before Task execution.

After transport require:

```text
branch:
main

HEAD:
187880eff48cbf2909e0fcadce75c6d2cb30ab31

HEAD tree:
1823346f7ec7c4da466d64f6823f0c8b3390f0cd

index:
empty
```

Expected Git-visible governance set before source creation is exact 14 paths:

- `.aiassistant/records/aiscc/cycles/20260908_1443_aiscc-command-center-workflow-correction-final-acceptance-p2-2-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1443_aiscc-command-center-workflow-correction-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260908_1512_aiscc-p2-2-synthetic-demo-repository-source-contract-audit-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_1512_aiscc-p2-2-source-contract-audit-blocked-transport-stop-and-fresh-session-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1512_aiscc-p2-2-source-contract-audit-transport-stop-violation-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_1519_aiscc-p2-2-audit-blocked-transport-tool-policy-recovery-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1519_aiscc-p2-2-audit-transport-tool-policy-blocked-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_1528_aiscc-p2-2-audit-blocked-command-center-dirt-contract-correction-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1528_aiscc-p2-2-audit-command-center-dirt-contract-correction-judgment-1.md`
- `.aiassistant/tasks/done/20260908_1443_aiscc-p2-2-synthetic-demo-repository-source-contract-audit-1.md`
- `.aiassistant/tasks/done/20260908_1519_aiscc-p2-2-transport-policy-compatible-source-contract-audit-retry-1.md`
- `.aiassistant/tasks/done/20260908_1528_aiscc-p2-2-source-contract-audit-provenance-reconciliation-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_1549_aiscc-p2-2-source-contract-audit-final-acceptance-implementation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1549_aiscc-p2-2-source-contract-audit-final-acceptance-judgment-1.md`

Current active Task is ignored.

Any extra/missing path:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Do not cleanup/restore/absorb.

# allowed source root

Only:

```text
examples/synthetic-stockroom/
```

may be created/modified as demo source.

Exact source file allowlist — 14:

- `examples/synthetic-stockroom/README.md`
- `examples/synthetic-stockroom/PROVENANCE.md`
- `examples/synthetic-stockroom/.python-version`
- `examples/synthetic-stockroom/.gitignore`
- `examples/synthetic-stockroom/stockroom/__init__.py`
- `examples/synthetic-stockroom/stockroom/__main__.py`
- `examples/synthetic-stockroom/stockroom/model.py`
- `examples/synthetic-stockroom/stockroom/inventory.py`
- `examples/synthetic-stockroom/stockroom/cli.py`
- `examples/synthetic-stockroom/stockroom/data/catalog.json`
- `examples/synthetic-stockroom/tests/test_inventory.py`
- `examples/synthetic-stockroom/tests/test_cli.py`
- `examples/synthetic-stockroom/tests/test_contract.py`
- `examples/synthetic-stockroom/tools/build.py`

Do not create any additional persistent source/config/test/document file.

Generated verification artifact only:

```text
examples/synthetic-stockroom/.build/stockroom.pyz
```

It must be removed before final submission after its hashes/evidence are recorded.

No other generated residue is allowed.

# exact runtime/dependency contract

Precondition:

```text
CPython:
3.12.14 exact
```

If absent:

```text
RUNTIME_PREREQUISITE_MISSING
→ STOP
```

Do not install/download Python or packages.

Allowed runtime/library:

```text
Python standard library only
```

Forbidden:

```text
pip
uv sync
npm
external network
provider
database
server
background process
external repository
```

The candidate must not import `aiscc`.

# exact file contract

## README.md

Must document:

- synthetic public example purpose
- exact commands
- deterministic behavior
- exact input bounds
- controlled future change surfaces
- P2-2 candidate != P2-3 scenario admission
- no external/network/private data
- development build artifact is not sandbox proof

## PROVENANCE.md

Must state truthfully:

- project-authored candidate source/data
- synthetic-only content
- no copied external sample or customer/company source
- zero third-party runtime dependencies
- public distribution/license review status remains pending unless separately authorized
- candidate creation does not equal public release or scenario admission

Do not invent a license grant.

## .python-version

Exact:

```text
3.12.14
```

## .gitignore

Candidate-local generated ignores only:

```text
.build/
__pycache__/
```

No broad parent/root patterns.

## stockroom package

`__init__.py`
- package marker, no side effects

`__main__.py`
- calls CLI main only

`model.py`
- immutable item/result structures
- integer constraints
- bool must not be accepted as integer business quantity/count

`inventory.py`
- fixed seed loader
- pure summary/reorder/reservation preview functions
- no durable mutation

`cli.py`
- exact two commands: `summary`, `reserve`
- deterministic compact JSON
- stable errors / exit codes
- no traceback/host path leakage

`stockroom/data/catalog.json`
- exact three artificial records defined below

## tests

Implement exact 20 baseline tests defined below.

## tools/build.py

- standard-library deterministic ZIP-app builder
- reads exact fixed input allowlist
- writes only `.build/stockroom.pyz`
- fixed timestamps/order/permissions
- no source mutation
- no host-path metadata

# exact baseline seed

JSON array sorted by SKU with exact fields:

```text
sku
on_hand
reserved
reorder_level
```

Records:

```text
BOX-A:
on_hand 12
reserved 2
reorder_level 3

BOX-B:
on_hand 5
reserved 5
reorder_level 2

BOX-C:
on_hand 4
reserved 1
reorder_level 3
```

Derived:

```text
BOX-A available 10 / needs_reorder false
BOX-B available 0 / needs_reorder true
BOX-C available 3 / needs_reorder true

summary total_available:
13
```

# domain constraints

```text
unique SKUs:
required

record count:
1..16

seed bytes:
<= 4096

on_hand/reserved/reorder_level:
integer excluding bool
0..1000

reserved <= on_hand

available:
on_hand - reserved

needs_reorder:
available <= reorder_level

reserve quantity:
integer excluding bool
1..1000
and <= available
```

`reserve` is preview-only. It must not write the seed or durable state.

Every invocation starts from the same fixed seed.

# CLI contract

Only commands:

```text
summary

reserve --sku <SKU> --quantity <INTEGER>
```

No input path, URL, upload, config, plugin, free-form task, shell or network option.

Success:

```text
exit:
0

stderr:
empty
```

Business/argument error:

```text
exit:
2

stderr:
exactly one compact JSON error + LF

stdout:
empty

no traceback
no host path
```

Output encoding:

```text
ASCII
JSON object keys sorted
compact separators
one LF
arrays ordered by SKU
<= 4096 bytes
```

Required example:

```text
reserve --sku BOX-A --quantity 4
```

must preview:

```text
on_hand 12
reserved 6
available 6
```

without modifying catalog.

# exact 20-test contract

## tests/test_inventory.py — 8

```text
test_seed_summary
test_reorder_threshold_inclusive
test_reservation_preview
test_reservation_exact_availability
test_insufficient_stock
test_unknown_sku
test_quantity_and_record_bounds
test_input_immutability_and_sorting
```

## tests/test_cli.py — 6

```text
test_summary_exact_json
test_reserve_exact_json
test_business_error_json_and_exit
test_unknown_command_or_option_rejected
test_repeated_invocation_identical
test_cli_has_no_write_or_network_path
```

The last test proves only the example's bounded behavior. It is not sandbox/runtime-isolation proof.

## tests/test_contract.py — 6

```text
test_exact_source_inventory
test_python_pin_and_stdlib_imports
test_seed_schema_and_size
test_no_links_nested_git_or_private_assets
test_build_reproducible
test_archive_entries_and_metadata
```

The test implementation itself must stay offline and bounded.

# deterministic build contract

Build:

```text
examples/synthetic-stockroom/.build/stockroom.pyz
```

Required archive properties:

- `ZIP_STORED`
- sorted entry order
- fixed `1980-01-01` timestamps
- fixed portable permission metadata
- no host paths
- no tests/docs/cache entries
- exact payload:
  - generated root `__main__.py`
  - `stockroom/__init__.py`
  - `stockroom/__main__.py`
  - `stockroom/model.py`
  - `stockroom/inventory.py`
  - `stockroom/cli.py`
  - `stockroom/data/catalog.json`
- generated root `__main__.py` is a constant launcher importing `stockroom.cli.main`
- repeat builds from unchanged source produce byte-identical archive/hash

# allowed verification commands

Cwd:

```text
examples/synthetic-stockroom/
```

Run only after source implementation:

```text
python -I -B -c "import sys; assert sys.version_info[:3] == (3, 12, 14)"
python -E -s -B -m unittest discover -s tests -p "test_*.py" -v
python -I -B tools/build.py
python -I -B .build/stockroom.pyz summary
python -I -B .build/stockroom.pyz reserve --sku BOX-A --quantity 4
python -E -s -B -m stockroom summary
python -E -s -B -m stockroom reserve --sku BOX-A --quantity 4
```

Additional narrow verification may calculate hashes, inspect exact source/archive inventory, rerun the same test/build commands, and perform `git diff --check`.

No full AISCC test suite is required.

# evidence contract

## executor_required

### COMMAND_CENTER_ARTIFACT_TRANSPORT
- current TASK/CYCLE/JUDGMENT exact source/hash/destination equality

### WORKSPACE_STATIC
- exact base HEAD/tree/index
- exact 14 pending governance paths before source creation
- no unrelated dirt

### SOURCE_IMPLEMENTATION
- exact 14 persistent candidate files
- no other persistent source change

### UNIT_TEST
- exact 20 tests collected/executed
- 20 PASS

### DETERMINISTIC_BUILD
- repeated archive build byte equality
- exact archive inventory/metadata
- seed/source hash stability

### CLI_RUNTIME
- module and pyz required commands PASS
- exact output parity
- error contract targeted verification

### SECURITY_STATIC
- standard-library-only/import inventory
- no nested Git/link/private/credential/network configuration
- bounded generated path only

### WORKSPACE_FINAL
Before current Task lifecycle move:

```text
14 pending governance
+
14 candidate source files
=
28 Git-visible paths exact
```

Generated `.build/stockroom.pyz` must be removed after evidence capture.

No unexpected `__pycache__` or other residue.

After current Task active→done:

```text
29 Git-visible paths exact
```

No Git staging.

## reuse_allowed

- accepted 1528 source/contract audit
- P1 security/public-runtime canonical design invariants

## human_owned

```text
new Human QA:
NOT_REQUIRED

implementation acceptance:
Browser Command Center after Executor bundle
```

## not_required

- AISCC full test suite
- Docker isolation runtime
- Browser QA
- provider/live call
- deployment
- Git persistence
- Project Source sync

## forbidden

- source outside exact 14-file root allowlist
- root/config/security mutation
- scenario enrollment
- external network/repository
- Git add/commit/push
- P2-3 work

# mandatory stop

```text
TRANSPORT_FAILURE
HEAD_OR_TREE_MISMATCH
INDEX_NOT_EMPTY
DIRTY_WORKSPACE_MIXED
RUNTIME_PREREQUISITE_MISSING
SOURCE_SCOPE_EXPANSION_REQUIRED
UNEXPECTED_DEPENDENCY_REQUIRED
SECURITY_BOUNDARY_UNCERTAIN
TEST_CONTRACT_CANNOT_BE_IMPLEMENTED_WITHIN_SCOPE
UNEXPECTED_WORKSPACE_RESIDUE
```

After named blocker: minimal evidence/report/export and safe cleanup of Task-owned generated `.build/stockroom.pyz` only.

# Task lifecycle

When implementation, required evidence, report and export are complete:

```text
.aiassistant/tasks/active/20260908_1549_aiscc-p2-2-synthetic-stockroom-candidate-implementation-1.md
→
.aiassistant/tasks/done/20260908_1549_aiscc-p2-2-synthetic-stockroom-candidate-implementation-1.md
```

Do not Git stage/commit.

# export bundle

Target:

```text
.aiassistant/reports/target/20260908_1549_aiscc-p2-2-synthetic-stockroom-candidate-implementation-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
IMPLEMENTATION_VERIFICATION.md
TEST_VERIFICATION.md
BUILD_CLI_VERIFICATION.md
```

Export:

- all 14 candidate source files preserving project-relative paths
- current CYCLE/JUDGMENT
- current Task at intended done-relative path after completion

Do not export prior unchanged pending governance files.

# final response ceiling

Success:

```text
P2-2 Synthetic Stockroom implementation:
ACCEPTED_CANDIDATE / READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT

P2-2:
NOT_CLOSED

P2-3:
NOT_STARTED
```

Do not issue or start next Task.
