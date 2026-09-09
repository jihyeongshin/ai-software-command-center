# 작업지시서: P2-3 Phase 1B-B1 trusted Git executable rework

## meta

- task_id: `20260909_1330_aiscc-p2-3-phase1b-b1-trusted-git-executable-rework-1`
- created_at: `2026-09-09T13:30:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `BOUNDED_BACKEND_REWORK / QA_ONLY`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `472bd11b76dc510562e33d056d9841b6be72c12e`
- required_base_tree: `14195b914b16d5adce7db0c4093907d2af7dcac0`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. inbound ZIP bootstrap

The Browser Short Prompt's exact delivery ZIP SHA-256 is the bootstrap integrity anchor.

Current delivery ZIP contains:

```text
TASK:
20260909_1330_aiscc-p2-3-phase1b-b1-trusted-git-executable-rework-1.md

CYCLE:
20260909_1330_aiscc-p2-3-phase1b-b1-test-failure-trusted-git-rework-entry-1.cycle.md
SHA-256:
74e93bfe9d38205a6e42ee60671d8d10d0540f2d7ca9535ef24e860de0cc55cf
destination:
.aiassistant/records/aiscc/cycles/20260909_1330_aiscc-p2-3-phase1b-b1-test-failure-trusted-git-rework-entry-1.cycle.md

JUDGMENT:
20260909_1330_aiscc-p2-3-phase1b-b1-test-failure-trusted-git-judgment-1.md
SHA-256:
864d316a9a34adda32a99afd3f9cf6c3d22c71dcb1d8818cbcd3555e6b3335ed
destination:
.aiassistant/reports/aiscc/20260909_1330_aiscc-p2-3-phase1b-b1-test-failure-trusted-git-judgment-1.md

HANDOFF:
none
```

Place TASK first at:

```text
.aiassistant/tasks/active/20260909_1330_aiscc-p2-3-phase1b-b1-trusted-git-executable-rework-1.md
```

Read it, then place/verify CYCLE/JUDGMENT.

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
472bd11b76dc510562e33d056d9841b6be72c12e

HEAD tree:
14195b914b16d5adce7db0c4093907d2af7dcac0

index:
empty
```

Expected Git-visible set excluding current active Task is exact 13 paths:

- `.aiassistant/tasks/done/20260909_1300_aiscc-p2-3-phase1b-runtime-integration-surface-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260909_1300_aiscc-p2-3-phase1a-terminal-accepted-phase1b-audit-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_1300_aiscc-p2-3-phase1a-terminal-state-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260909_1329_aiscc-p2-3-phase1b-b1-pinned-resource-materializer-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260909_1329_aiscc-p2-3-phase1b-audit-accepted-b1-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_1329_aiscc-p2-3-phase1b-runtime-integration-audit-final-acceptance-judgment-1.md`
- `src/aiscc/runtime/stockroom_workspace.py`
- `src/aiscc/runtime/stockroom_materializer.py`
- `src/aiscc/scenarios/runtime_models.py`
- `tests/unit/runtime/test_stockroom_materializer.py`
- `tests/unit/runtime/test_stockroom_workspace.py`
- `.aiassistant/records/aiscc/cycles/20260909_1330_aiscc-p2-3-phase1b-b1-test-failure-trusted-git-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_1330_aiscc-p2-3-phase1b-b1-test-failure-trusted-git-judgment-1.md`

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Do not cleanup/restore/absorb.

# 2. exact predecessor identity

Require exact 1300 provenance:

- `.aiassistant/tasks/done/20260909_1300_aiscc-p2-3-phase1b-runtime-integration-surface-audit-1.md`  `61fe8fea516e79fb5c66150433bbd79d2abaf70b845f8ca72736597fac3f9f26`
- `.aiassistant/records/aiscc/cycles/20260909_1300_aiscc-p2-3-phase1a-terminal-accepted-phase1b-audit-entry-1.cycle.md`  `998d726c95165db059b697e4ce04184bead4fe50c4fa4a88c14cd5f376444c36`
- `.aiassistant/reports/aiscc/20260909_1300_aiscc-p2-3-phase1a-terminal-state-final-acceptance-judgment-1.md`  `595d283e12ee27ed7cff9484c4305ccbb8760b40b34bc25374e9800618a6ed21`

Require exact 1329 provenance:

- `.aiassistant/tasks/done/20260909_1329_aiscc-p2-3-phase1b-b1-pinned-resource-materializer-implementation-1.md`  `68a9aa6630af1729b8c4a8aad0ff988df28e0d314bf8495b48854ca1b86d2fc3`
- `.aiassistant/records/aiscc/cycles/20260909_1329_aiscc-p2-3-phase1b-audit-accepted-b1-entry-1.cycle.md`  `e1431a3630a83a391485148117566ee63b827ba41a40745b36c11fd3974ae404`
- `.aiassistant/reports/aiscc/20260909_1329_aiscc-p2-3-phase1b-runtime-integration-audit-final-acceptance-judgment-1.md`  `fc062f0a09ff170f75c204c9bde43c0c0d061f2ed1204583bc7047e88b934169`

Require exact five-file B1 starting candidate:

- `src/aiscc/runtime/stockroom_workspace.py`  `fd6c889e518b9fec7bef425ec4ea950b430c38c86f039a62a275949416442347`
- `src/aiscc/runtime/stockroom_materializer.py`  `8b32284fcf928b928ed3d943175a428b3db89a19d5cbc90f8421e88e0916bac8`
- `src/aiscc/scenarios/runtime_models.py`  `2d2264ad0fcc2417febc17d8951ff66e8f3931a074d114c3382d2238e9531cef`
- `tests/unit/runtime/test_stockroom_materializer.py`  `cfe0175d2ad53a77239f8b89c00034ac7f62f10c4eea14f7d492141218bb42d9`
- `tests/unit/runtime/test_stockroom_workspace.py`  `ce24c649664461440d4f354d0d311624e07bed840dba4f12df99fbc49dddd1ca`

Any mismatch:

```text
PREDECESSOR_IMPLEMENTATION_IDENTITY_MISMATCH
→ STOP
```

# 3. exact mutation authority

Only these existing candidate files may change:

```text
src/aiscc/runtime/stockroom_materializer.py
tests/unit/runtime/test_stockroom_materializer.py
```

These three must remain byte-exact:

```text
src/aiscc/runtime/stockroom_workspace.py
SHA-256:
fd6c889e518b9fec7bef425ec4ea950b430c38c86f039a62a275949416442347

src/aiscc/scenarios/runtime_models.py
SHA-256:
2d2264ad0fcc2417febc17d8951ff66e8f3931a074d114c3382d2238e9531cef

tests/unit/runtime/test_stockroom_workspace.py
SHA-256:
ce24c649664461440d4f354d0d311624e07bed840dba4f12df99fbc49dddd1ca
```

No governance file may be edited except current Task lifecycle.

No additional product/config/test path may be created or modified.

If another path is needed:

```text
SCOPE_EXPANSION_REQUIRED
→ STOP
```

# 4. root-cause repair

The current materializer calls workspace `checked_absolute()` on `git_executable`.

That helper rejects regular files with `st_nlink != 1`, which is an ownership invariant for mutable workspace objects.

Do not weaken or modify:

```text
src/aiscc/runtime/stockroom_workspace.py
```

Instead, in `stockroom_materializer.py`, implement a private validator dedicated only to the operator-configured trusted Git executable.

Required semantics:

```text
absolute local path only
no UNC/requester path
parent/ancestor path must remain lexically and resolution-safe
final executable must exist
final object must be a regular file
final object must not be symlink/reparse/special
strict resolution/case consistency
name must remain git or git.exe
os executable-access requirement retained
repository/runtime-root overlap denial retained
```

For this final trusted executable object only:

```text
st_nlink >= 1:
allowed
```

Do not impose `st_nlink == 1`.

This exception MUST NOT apply to:

```text
workspace root
workspace files
materialized source files
repository Git object validation
destination verification
cleanup ownership
```

No PATH fallback, shell resolution, requester-provided executable, remote fetch or config widening.

# 5. trusted-executable proof

Tests must prove the distinction:

```text
trusted operator Git executable:
regular + non-reparse + executable + exact configured path
hardlink count > 1 is not by itself a denial

mutable workspace/materialized file hardlink:
still denied/quarantined by existing workspace rules
```

The unchanged workspace test suite is the proof owner for mutable workspace behavior.

For trusted executable negative cases, add bounded unit coverage for applicable branches such as:

```text
non-absolute/missing path
wrong executable name
directory/special object
symlink or reparse point where host supports proof
repository/runtime-root overlap
```

Platform primitive unavailable:
explicit skip with reason, not PASS claim.

# 6. negative materializer assertion tightening

The 1329 tests used broad:

```text
pytest.raises(StockroomFailure)
```

for several source/manifest cases.

Tighten `tests/unit/runtime/test_stockroom_materializer.py` so the intended branch cannot pass merely because an earlier unrelated configuration guard failed.

For the static Resource mutation cases, prove the expected resource/manifest validation classification or equivalent exact branch-reach signal.

For Git object/list/blob mutation cases, prove the expected source-object classification or equivalent branch-reach signal.

At minimum ensure explicit proof for:

```text
wrong commit type
wrong subtree
wrong tree type
missing/extra tree entry
unsafe mode/symlink/gitlink/tree
duplicate/case-fold duplicate
unsafe path forms
wrong blob size
wrong blob SHA
timeout
nonzero
ambiguous/oversized read
```

Do not weaken production checks merely to satisfy test expected reasons.

# 7. full positive proof

The real configured local Git executable on this Windows host must reach complete:

```text
StockroomMaterializer.materialize(...)
```

and prove:

```text
exact resource_ref
exact source commit/subroot/subtree
14 exact files
exact size/SHA
aggregate exact
destination bytes exact
immutable result provenance
primary checkout/index identity unchanged
exact cleanup
```

Do not substitute direct `_read_git()` success for full materialization.

# 8. partial publication proof

All four existing cases:

```text
write
verify
state-change
unexpected-residue
```

must reach workspace allocation/publication.

Required:

```text
write:
CLEANED

verify:
CLEANED

state-change:
CLEANED

unexpected-residue:
QUARANTINED / residue preserved
```

All must prove:

```text
no successful MaterializedStockroom returned
primary checkout/index unchanged
run/attempt destination cannot be reused
```

Do not accept `cleanup is None`.

# 9. exact required test command

Run exactly the same two-module B1 suite:

```text
PYTHONDONTWRITEBYTECODE=1
.venv/Scripts/python.exe -B -m pytest -q -p no:cacheprovider tests/unit/runtime/test_stockroom_materializer.py tests/unit/runtime/test_stockroom_workspace.py -ra
```

No package installation/network/provisioning.

Required:

```text
exit 0
failed 0
errors 0
```

Skips are allowed only for genuinely unavailable platform primitives and must be separately reported.

If test exit is nonzero:

```text
TEST_FAILURE
→ STOP
```

No same-turn second repair/rerun after a mandatory test failure.

# 10. post-test identity/scope

Require:

```text
stockroom_materializer.py:
changed from 1329 candidate

test_stockroom_materializer.py:
changed from 1329 candidate

other three B1 files:
exact unchanged hashes

existing tracked product/config/test:
no modification

new product/config/test path:
none

index:
empty

git diff --check:
PASS

Git-visible cache/pyc/pytest residue:
none
```

No scenario/provider/tool/DB/Replay execution.

# 11. final workspace

Before current Task lifecycle:

```text
pending governance:
8 exact

B1 implementation:
5 exact

Git-visible excluding active Task:
13 exact

index:
empty
```

Then move:

```text
.aiassistant/tasks/active/20260909_1330_aiscc-p2-3-phase1b-b1-trusted-git-executable-rework-1.md
→
.aiassistant/tasks/done/20260909_1330_aiscc-p2-3-phase1b-b1-trusted-git-executable-rework-1.md
```

Final:

```text
14 exact Git-visible paths
index empty
```

No Git add/commit.

# 12. evidence contract

executor_required:

- inbound ZIP/artifact transport
- exact predecessor/workspace identity
- two-file bounded rework diff
- trusted executable vs workspace hardlink distinction proof
- exact full positive materialization proof
- branch-specific negative materializer proof
- four partial-publication cleanup/quarantine proofs
- exact two-module suite PASS
- exact final workspace inventory
- outbound result ZIP

reuse_allowed:

- unchanged three B1 candidate files under exact hashes
- accepted Phase 1A resource identity
- accepted 1300 Phase 1B design
- 1329 root-cause diagnostics

human_owned:

```text
new Human QA:
NOT_REQUIRED
```

not_required:

```text
B2/B3
actual scenario capture
provider/tool runtime
DB
Replay
Browser QA
```

forbidden:

```text
workspace helper weakening
config/security/provider/bootstrap modification
new dependency
network
Docker
scenario execution
Git add/commit/push
P2-4/P3
```

# 13. mandatory stop

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
TEST_FAILURE
CONTRACT_MISMATCH
UNEXPECTED_WORKSPACE_DELTA
ZIP_EXPORT_FAILED
```

Inbound cleanup refusal after canonical transport is non-blocking.

# 14. export bundle + outbound ZIP

Bundle folder:

```text
.aiassistant/reports/target/20260909_1330_aiscc-p2-3-phase1b-b1-trusted-git-executable-rework-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
REWORK_DIFF_VERIFICATION.md
MATERIALIZER_CONTRACT_VERIFICATION.md
TEST_VERIFICATION.md
IMPLEMENTATION_MANIFEST.md
```

Include byte-preserving project-relative copies of:

```text
current Cycle
current Judgment
current done Task
all five final B1 implementation paths
```

After folder completion create:

```text
.aiassistant/reports/target/20260909_1330_aiscc-p2-3-phase1b-b1-trusted-git-executable-rework-1.zip
```

Require readable/CRC-valid archive, one top-level bundle directory, required root files, manifest coverage and folder/archive byte equality.

# 15. final ceiling

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
