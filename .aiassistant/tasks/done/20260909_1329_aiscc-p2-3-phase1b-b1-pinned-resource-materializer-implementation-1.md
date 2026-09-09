# 작업지시서: P2-3 Phase 1B-B1 pinned resource materializer implementation

## meta

- task_id: `20260909_1329_aiscc-p2-3-phase1b-b1-pinned-resource-materializer-implementation-1`
- created_at: `2026-09-09T13:29:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `ORCHESTRATION_IMPLEMENTATION / BOUNDED_BACKEND_IMPLEMENTATION`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P2-3 Phase 1B-B1 pinned resource workspace/materializer`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `472bd11b76dc510562e33d056d9841b6be72c12e`
- required_base_tree: `14195b914b16d5adce7db0c4093907d2af7dcac0`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `read-only Phase 1B audit → source/test mutation authority`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. inbound ZIP bootstrap

The Browser Short Prompt's exact delivery ZIP SHA-256 is the bootstrap integrity anchor.

Current delivery ZIP contains only:

```text
TASK:
20260909_1329_aiscc-p2-3-phase1b-b1-pinned-resource-materializer-implementation-1.md

CYCLE:
20260909_1329_aiscc-p2-3-phase1b-audit-accepted-b1-entry-1.cycle.md
SHA-256:
e1431a3630a83a391485148117566ee63b827ba41a40745b36c11fd3974ae404
destination:
.aiassistant/records/aiscc/cycles/20260909_1329_aiscc-p2-3-phase1b-audit-accepted-b1-entry-1.cycle.md

JUDGMENT:
20260909_1329_aiscc-p2-3-phase1b-runtime-integration-audit-final-acceptance-judgment-1.md
SHA-256:
fc062f0a09ff170f75c204c9bde43c0c0d061f2ed1204583bc7047e88b934169
destination:
.aiassistant/reports/aiscc/20260909_1329_aiscc-p2-3-phase1b-runtime-integration-audit-final-acceptance-judgment-1.md

HANDOFF:
none
```

Human downloads only the ZIP.

Executor:

1. verify exact ZIP filename/SHA-256;
2. validate archive readability/CRC/member safety;
3. materialize TASK first to `.aiassistant/tasks/active/20260909_1329_aiscc-p2-3-phase1b-b1-pinned-resource-materializer-implementation-1.md`;
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

After exact canonical transport, inbound cleanup failure is non-blocking local residue.

# 1. repository gate

After current artifact placement require:

```text
branch:
main

HEAD:
472bd11b76dc510562e33d056d9841b6be72c12e

HEAD tree:
14195b914b16d5adce7db0c4093907d2af7dcac0

index:
empty
```

Expected Git-visible governance set excluding current active Task:

- `.aiassistant/tasks/done/20260909_1300_aiscc-p2-3-phase1b-runtime-integration-surface-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260909_1300_aiscc-p2-3-phase1a-terminal-accepted-phase1b-audit-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_1300_aiscc-p2-3-phase1a-terminal-state-final-acceptance-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260909_1329_aiscc-p2-3-phase1b-audit-accepted-b1-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_1329_aiscc-p2-3-phase1b-runtime-integration-audit-final-acceptance-judgment-1.md`

exact 5 paths.

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Do not cleanup/restore/absorb.

# 2. predecessor identity

Verify exact SHA-256:

- `.aiassistant/tasks/done/20260909_1300_aiscc-p2-3-phase1b-runtime-integration-surface-audit-1.md`  `61fe8fea516e79fb5c66150433bbd79d2abaf70b845f8ca72736597fac3f9f26`
- `.aiassistant/records/aiscc/cycles/20260909_1300_aiscc-p2-3-phase1a-terminal-accepted-phase1b-audit-entry-1.cycle.md`  `998d726c95165db059b697e4ce04184bead4fe50c4fa4a88c14cd5f376444c36`
- `.aiassistant/reports/aiscc/20260909_1300_aiscc-p2-3-phase1a-terminal-state-final-acceptance-judgment-1.md`  `595d283e12ee27ed7cff9484c4305ccbb8760b40b34bc25374e9800618a6ed21`

Mismatch:

```text
PREDECESSOR_PROVENANCE_IDENTITY_MISMATCH
→ STOP
```

# 3. must-read authority/source

Read:

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/AISCC_RUNTIME_SUBSTRATE.md
.aiassistant/rules/AISCC_SECURITY_SANDBOX.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md

.aiassistant/records/aiscc/cycles/20260909_1300_aiscc-p2-3-phase1a-terminal-accepted-phase1b-audit-entry-1.cycle.md
.aiassistant/reports/aiscc/20260909_1300_aiscc-p2-3-phase1a-terminal-state-final-acceptance-judgment-1.md
.aiassistant/records/aiscc/cycles/20260909_1329_aiscc-p2-3-phase1b-audit-accepted-b1-entry-1.cycle.md
.aiassistant/reports/aiscc/20260909_1329_aiscc-p2-3-phase1b-runtime-integration-audit-final-acceptance-judgment-1.md

config/scenarios/stockroom/v1/resource.json
src/aiscc/scenarios/models.py
src/aiscc/runtime/contracts.py
src/aiscc/runtime/cleanup.py
src/aiscc/security/models.py
src/aiscc/security/policy.py
```

Read only additional exact symbols needed to type against existing runtime/security contracts.

Do not bulk-read unrelated history.

# 4. exact B1 mutation allowlist

Only these five product/test paths may be created:

- `src/aiscc/runtime/stockroom_workspace.py`
- `src/aiscc/runtime/stockroom_materializer.py`
- `src/aiscc/scenarios/runtime_models.py`
- `tests/unit/runtime/test_stockroom_materializer.py`
- `tests/unit/runtime/test_stockroom_workspace.py`

All five must be absent before creation.

No existing tracked product/config/test file may be modified.

If any of the five already exists unexpectedly:

```text
UNEXPECTED_EXISTING_PATH
→ STOP
```

If implementation requires another product/config/test path:

```text
SCOPE_EXPANSION_REQUIRED
→ STOP
```

Governance mutation is limited to current Task lifecycle and already issued CYCLE/JUDGMENT.

# 5. accepted pinned identity

B1 must encode/consume the accepted static Resource rather than redefine it:

```text
resource_id:
repository:synthetic-stockroom

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

No `latest`, current-checkout identity, requester-provided commit/subroot/root, or remote fallback.

# 6. runtime_models.py contract

Create immutable/frozen B1 DTOs sufficient for:

```text
StockroomRunBinding
MaterializationAuthority
MaterializedFile
MaterializedStockroom
workspace/materialization failure classification if required
```

Exact naming may differ only if existing repository conventions require a more precise equivalent.

Required semantics:

## StockroomRunBinding

Must bind at least:

```text
runtime mode = OWNER_SELF_DOGFOOD
scenario_id
scenario_version
resource_ref
run_id
attempt_id
workflow state
state_version
profile/config identity placeholders required by later B2
```

It is server-owned runtime context, not requester input.

## MaterializationAuthority

Must be a typed immutable authority envelope/ref set.

It must NOT be:

```text
bool
caller GRANTED flag
Agent-produced DTO
unverified free-form scope
```

B1 may represent future security-issued refs/fingerprints without issuing them.

Materializer must fail closed if exact authority/binding data required by B1 is absent or inconsistent.

## MaterializedStockroom

Must report immutable non-secret provenance:

```text
resource_ref
source_commit
subroot
git_subtree
ordered verified file inventory
aggregate_sha256
workspace lease identity
run_id
attempt_id
resolved source root
```

It grants no tool/provider/evidence capability.

# 7. workspace owner implementation

Create:

```text
src/aiscc/runtime/stockroom_workspace.py
```

It must own a package-private/operator-configured runtime root and produce run/attempt-specific source destinations.

Required constraints:

```text
runtime root:
server/operator configured only

must resolve outside:
- repository primary checkout
- repository .git
- Downloads
- source Git object root if distinct
- sibling run/attempt destination

destination:
<runtime-root>/<run-id>/<attempt-id>/source

allocation:
exclusive

existing destination:
deny

requester-selected path:
none
```

Reject unsafe path components and ambiguous Windows forms.

At minimum handle/reject:

```text
absolute/drive/UNC injection
..
ADS
reserved device names
trailing dot/space ambiguity
case-fold collision
symlink/junction/reparse traversal
existing unexpected sibling/object
```

Workspace lease must be immutable and bind:

```text
lease_id
run_id
attempt_id
runtime root
destination
ownership state
```

No broad directory cleanup API.

# 8. cleanup/quarantine semantics

B1 cleanup operates only on an exact verified lease-owned run/attempt destination.

Required:

```text
known exact ownership + safe containment
→ cleanup may proceed

unknown ownership
unsafe ancestor
unexpected residue/link/reparse
delete uncertainty/failure
→ quarantine / no reuse
```

Do not silently mark cleanup successful.

Return typed cleanup disposition sufficient for later runtime provenance.

Do not modify existing generic cleanup owner in B1.

# 9. materializer implementation

Create:

```text
src/aiscc/runtime/stockroom_materializer.py
```

Preferred source mechanism is exact local Git object reads from the configured primary repository.

No remote network/fetch.

No checkout/worktree/index mutation.

Allowed Git operations are fixed structured read-only object commands equivalent to:

```text
git cat-file -t <fixed-commit>
git rev-parse <fixed-commit>:<fixed-subroot>
git ls-tree -z -r <fixed-commit>:<fixed-subroot>
git cat-file blob <fixed-object>
```

Implementation may use a safer equivalent local-object API if already available.

All Git command arguments are server-owned fixed identifiers derived from accepted Resource/config.

Disable/ignore unsafe ambient Git behavior where current facilities allow, including replace-object and lazy remote fetch assumptions.

No shell string construction.

No requester-controlled Git argument.

# 10. verification-before-publication order

Materializer must fail closed in this order-equivalent contract:

1. validate `StockroomRunBinding` owner mode/scenario/version/resource/run/attempt/state/version;
2. validate configured repository root and trusted local Git executable;
3. validate static Resource manifest invariants and aggregate;
4. resolve exact commit/subtree object types;
5. enumerate exact subtree safely;
6. require 14 exact `100644` regular blobs and exact sorted manifest path set;
7. read each bounded blob and verify bytes/size/SHA before destination publication;
8. allocate exclusive exact workspace lease;
9. create regular destination files only under verified lease root;
10. re-read destination bytes and verify exact inventory/hash/aggregate;
11. return `MaterializedStockroom` only after complete verification.

No partial destination may be returned as successful.

# 11. source path/object safety

Reject:

```text
symlink mode
gitlink/submodule
tree where file expected
duplicate path
case-fold duplicate
absolute path
drive/UNC path
.. or dot-segment escape
ADS/device path
separator ambiguity
trailing dot/space ambiguity
manifest/path mismatch
wrong commit/subtree/tree
wrong mode
wrong byte count
wrong SHA
wrong aggregate
```

B1 must not execute imported Synthetic Stockroom Python.

# 12. finite bounds

Use explicit finite constants/config-local bounds for B1 object reading.

At minimum bound:

```text
expected file count:
14 exact

per-file bytes:
>= accepted manifest max, finite

total bytes:
>= accepted manifest total, finite

Git object-read timeout:
finite

destination write count:
14 exact
```

Do not add dependency/config files in B1.

If a suitable bound cannot be represented without an out-of-scope config change, use a conservative module-private constant and document it for later B2/B3 configuration review.

# 13. authority/state behavior

Actual source copying must require a binding representing:

```text
RuntimeMode:
OWNER_SELF_DOGFOOD

workflow state:
RUNNING
```

An inert workspace reservation/planning helper may be tested for READY if needed, but successful `materialize(...)` must reject non-RUNNING or stale/invalid binding.

B1 does not independently call SecurityPolicy to issue authority.

B1 validates the typed exact authority envelope presented to it.
B2 later owns real security-policy binding.

Do not simulate that B1's synthetic unit authority is runtime admission proof.

# 14. allowed B1 test execution

Create only:

```text
tests/unit/runtime/test_stockroom_materializer.py
tests/unit/runtime/test_stockroom_workspace.py
```

Tests may use:

```text
pytest tmp_path / task-owned temporary directories
synthetic local temporary Git repository fixtures
or read-only access to the current repository's pinned Git objects
```

Tests may materialize into pytest-owned temporary directories.

This is B1 implementation verification, NOT actual AISCC scenario capture.

Tests must not:

```text
run Stockroom CLI/module
run Docker
open network
call provider
mutate DB
modify primary checkout/index
invoke scenario driver
create Replay
```

# 15. required workspace tests

Cover at minimum:

```text
safe server-owned runtime root
exact run/attempt/source destination
exclusive allocation
existing destination denial
runtime root inside checkout denied
runtime root under .git denied
Downloads root denied when deterministically detectable
sibling/cross-run ownership denial
path traversal
absolute/drive/UNC
ADS/device/trailing dot-space
case-fold collision
symlink/junction/reparse safety where platform supports proof
cleanup exact owned destination
cleanup refuses unknown ownership
cleanup failure/ambiguity -> quarantine/no reuse
```

Platform-specific unsupported link primitives must be explicitly skipped with reason, not counted as proven.

# 16. required materializer tests

Cover at minimum:

## positive

```text
accepted resource identity resolves
exact subtree identity
14 exact files
100644 modes
byte counts/SHA exact
aggregate exact
deterministic ordered inventory
destination bytes exact
MaterializedStockroom contains exact immutable provenance
primary checkout/index unchanged
```

## negative

```text
non-owner runtime mode
non-RUNNING binding
stale/wrong resource_ref
wrong commit
missing object
wrong subtree
wrong object type
manifest missing/extra
wrong mode
wrong size
wrong SHA
wrong aggregate
path traversal
symlink/gitlink
duplicate/case-fold collision
existing destination
authority/binding mismatch
Git timeout/nonzero/ambiguous read
partial write/verification failure
```

On partial failure verify:

```text
no successful materialization result
owned partial destination cleaned or quarantined exactly
primary checkout unchanged
```

# 17. test command selection

Use existing project test environment only.

No dependency installation/network/provisioning.

Run the narrowest exact existing command that executes only the two new B1 test modules.

If needed, include an existing no-cache/no-bytecode option consistent with repository practice.

Also run static checks necessary to establish:

```text
git diff --check PASS
no pyc/__pycache__/pytest cache Git-visible residue
index empty
only exact B1 mutation paths
```

If test environment unavailable:

```text
BLOCKED_RUNTIME_PREREQUISITE
→ STOP
```

If tests fail:

```text
TEST_FAILURE
→ STOP
```

No same-turn source repair after mandatory test failure. Return to Browser Command Center.

# 18. explicit non-goals / forbidden

B1 does NOT authorize creating/modifying:

```text
src/aiscc/scenarios/enrollment.py
src/aiscc/scenarios/driver.py
src/aiscc/scenarios/composition.py

src/aiscc/providers/**
src/aiscc/security/**
src/aiscc/bootstrap.py
src/aiscc/runtime/docker.py

config/providers/**
config/security/**
config/scenarios/**

migrations/**
src/aiscc/persistence/**

Replay/public/API/frontend/release code
dependency manifests
```

Also forbidden:

```text
actual scenario execution
Stockroom tool execution
Docker/container run
provider call
DB mutation
network
Git add/commit/push
public release
P2-4/P3
```

# 19. expected final workspace

Before Task lifecycle:

```text
pending governance:
5 exact paths

B1 implementation:
5 exact paths

Git-visible excluding active Task:
10 exact

index:
empty
```

Then move:

```text
.aiassistant/tasks/active/20260909_1329_aiscc-p2-3-phase1b-b1-pinned-resource-materializer-implementation-1.md
→
.aiassistant/tasks/done/20260909_1329_aiscc-p2-3-phase1b-b1-pinned-resource-materializer-implementation-1.md
```

Final:

```text
11 exact Git-visible paths
index empty
```

No other path.

# 20. evidence contract

executor_required:

- inbound ZIP/artifact transport
- repository gate
- 1300 provenance identity
- exact five-file B1 implementation
- workspace/path safety unit proof
- pinned local-object materialization unit proof
- exact final workspace inventory
- outbound result ZIP

reuse_allowed:

- Phase 1A resource identity/contracts
- 1300 accepted Phase 1B audit
- accepted static local Git-object verification from 1300 as design evidence only

human_owned:

```text
new Human QA:
NOT_REQUIRED

public license:
HUMAN_PENDING / outside B1
```

not_required:

```text
security-policy enrollment
provider/tool runtime
scenario capture
DB
Replay
Browser QA
deployment
```

forbidden proof substitution:

```text
B1 unit materialization != actual scenario run
typed authority DTO != issued runtime capability
local Git object proof != public runtime admission
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
UNEXPECTED_EXISTING_PATH
SCOPE_EXPANSION_REQUIRED
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
.aiassistant/reports/target/20260909_1329_aiscc-p2-3-phase1b-b1-pinned-resource-materializer-implementation-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
IMPLEMENTATION_MANIFEST.md
MATERIALIZER_CONTRACT_VERIFICATION.md
TEST_VERIFICATION.md
```

Include byte-preserving project-relative copies of:

```text
current Cycle
current Judgment
current done Task
all five B1 implementation paths
```

After bundle completion create:

```text
.aiassistant/reports/target/20260909_1329_aiscc-p2-3-phase1b-b1-pinned-resource-materializer-implementation-1.zip
```

Require:

```text
one top-level bundle directory
readable archive
CRC/integrity PASS
required root files present
manifest coverage
folder/archive filename equality
folder/archive byte equality
```

Keep folder and outbound ZIP.

# 23. inbound cleanup

After terminal outcome and outbound ZIP verification, attempt exact inbound delivery ZIP cleanup best-effort.

Any refusal:

```text
NON_BLOCKING_LOCAL_RESIDUE
```

No broad Downloads cleanup.

# 24. final ceiling

Success:

```text
P2-3 Phase 1B-B1:
READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT

P2-3 Phase 1B-B2:
NOT_STARTED

P2-3 Phase 1B-B3:
NOT_STARTED

actual scenario capture:
NOT_STARTED

Replay:
NOT_STARTED
```

Do not declare Phase 1B or P2-3 closed.
