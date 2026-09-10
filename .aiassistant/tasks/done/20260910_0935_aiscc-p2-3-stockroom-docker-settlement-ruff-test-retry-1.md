# 작업지시서: P2-3 Stockroom Docker settlement Ruff/test retry

## meta

- task_id: `20260910_0935_aiscc-p2-3-stockroom-docker-settlement-ruff-test-retry-1`
- created_at: `2026-09-10T09:35:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `TEST_ONLY_FORMAT_REWORK / RUNTIME_SAFETY_REGRESSION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `Stockroom Docker settlement regression completion`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `d8fbcfa9d36a7531819149037240855cafdd088d`
- required_base_tree: `e224f31268057e400918ece352b72a0388d4091d`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. purpose

The 0918 runtime fix candidate reached the mandatory static gate and stopped on one test-only Ruff E501.

This Task does not authorize further runtime-source changes.

It authorizes only the semantics-preserving test formatting correction required to reach the already-defined dynamic regression gates.

# 1. inbound ZIP bootstrap

The Browser Short Prompt's exact delivery ZIP SHA-256 is the bootstrap integrity anchor.

Current delivery ZIP contains only:

```text
TASK:
20260910_0935_aiscc-p2-3-stockroom-docker-settlement-ruff-test-retry-1.md

CYCLE:
20260910_0935_aiscc-p2-3-stockroom-docker-settlement-static-failure-retry-entry-1.cycle.md
SHA-256:
6bd00596359e8258969ad13bc09131ed1176fa7b868e4dc2a8c64a92508fd6b8
destination:
.aiassistant/records/aiscc/cycles/20260910_0935_aiscc-p2-3-stockroom-docker-settlement-static-failure-retry-entry-1.cycle.md

JUDGMENT:
20260910_0935_aiscc-p2-3-stockroom-docker-settlement-static-failure-judgment-1.md
SHA-256:
0a0dcd8aec677a961b5d4d3412d6797cf8f899ae791ac75c41eeac275bdfcfbd
destination:
.aiassistant/reports/aiscc/20260910_0935_aiscc-p2-3-stockroom-docker-settlement-static-failure-judgment-1.md

HANDOFF:
none
```

Place TASK first at:

```text
.aiassistant/tasks/active/20260910_0935_aiscc-p2-3-stockroom-docker-settlement-ruff-test-retry-1.md
```

Read it, then place/hash-verify current Cycle/Judgment.

Bootstrap failure before canonical TASK placement:

```text
STOP
no report/export
no substantive project mutation
```

After canonical transport, inbound cleanup refusal is non-blocking.

# 2. repository gate — exact dirty baseline

Require:

```text
branch:
main

HEAD:
d8fbcfa9d36a7531819149037240855cafdd088d

HEAD tree:
e224f31268057e400918ece352b72a0388d4091d

index:
empty
```

Expected Git-visible set excluding current active Task is exact 10 paths:

- `.aiassistant/tasks/done/20260910_0207_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_0207_aiscc-p2-3-phase1b-closed-actual-capture-runtime-entry-audit-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_0207_aiscc-p2-3-phase1b-terminal-state-reconciliation-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260910_0918_aiscc-p2-3-stockroom-docker-settlement-quarantine-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_0918_aiscc-p2-3-actual-capture-entry-audit-blocked-runtime-settlement-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_0918_aiscc-p2-3-runtime-settlement-canonical-conflict-judgment-1.md`
- `src/aiscc/runtime/docker.py`
- `tests/unit/runtime/test_stockroom_docker_settlement.py`
- `.aiassistant/records/aiscc/cycles/20260910_0935_aiscc-p2-3-stockroom-docker-settlement-static-failure-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_0935_aiscc-p2-3-stockroom-docker-settlement-static-failure-judgment-1.md`

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Do not cleanup/restore/stash/reset/overwrite.

# 3. exact predecessor identity

Require exact 0207 provenance:

- `.aiassistant/tasks/done/20260910_0207_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-1.md`  `e97b19297ce70d9ebb9f714b64ff83facf13e91c44f65c4ca6c4a0d0adb94cb0`
- `.aiassistant/records/aiscc/cycles/20260910_0207_aiscc-p2-3-phase1b-closed-actual-capture-runtime-entry-audit-1.cycle.md`  `5a68361c98b6165cdd6fa20adf0cc6ca8df99ada519c5c51efc6123f91c0b339`
- `.aiassistant/reports/aiscc/20260910_0207_aiscc-p2-3-phase1b-terminal-state-reconciliation-final-acceptance-judgment-1.md`  `e6e9266e9f6feedca478b7062d62af47c1b4442d8e719bb4e7ff8f9d59b3e6fa`

Require exact 0918 provenance:

- `.aiassistant/tasks/done/20260910_0918_aiscc-p2-3-stockroom-docker-settlement-quarantine-rework-1.md`  `7448b8ee218e5b3494a10b2987cf2d18053fd11f686aba9ad9dbd1224bd3f747`
- `.aiassistant/records/aiscc/cycles/20260910_0918_aiscc-p2-3-actual-capture-entry-audit-blocked-runtime-settlement-rework-entry-1.cycle.md`  `239b189e270c4fb7e3896bda2ad4552708567b64d0e5abec5065b080277267d3`
- `.aiassistant/reports/aiscc/20260910_0918_aiscc-p2-3-runtime-settlement-canonical-conflict-judgment-1.md`  `5c811f58429fc37b4a212f922d12b52b7632e20f4bb6c7e217c5284246b5092e`

Require exact runtime candidate:

```text
src/aiscc/runtime/docker.py
SHA-256:
f338225c13195d69c41f69f00a47fc1d00c616c94458ef361e32b97f7fde96fa
```

Require exact starting test candidate:

```text
tests/unit/runtime/test_stockroom_docker_settlement.py
SHA-256:
8e971ede0fcc045290d97d07627bb75eff95e224e083d0aa130dd6787403110a
```

Any mismatch:

```text
PREDECESSOR_OR_CANDIDATE_IDENTITY_MISMATCH
→ STOP
```

# 4. exact mutation authority

Product/runtime source mutation:

```text
NONE
```

Only this existing test file may change:

```text
tests/unit/runtime/test_stockroom_docker_settlement.py
```

Frozen exact runtime source:

```text
src/aiscc/runtime/docker.py
SHA-256:
f338225c13195d69c41f69f00a47fc1d00c616c94458ef361e32b97f7fde96fa
```

All other source/config/test paths are read-only.

If another path needs modification:

```text
SCOPE_EXPANSION_REQUIRED
→ STOP
```

# 5. exact authorized test edit

Before editing, parse the starting test with Python `ast.parse` and retain a structural dump equivalent to:

```text
ast.dump(tree, include_attributes=False)
```

Correct only the Ruff E501 at the function declaration corresponding to the reported line 166.

Use a normal multi-line function signature consistent with repository style.

Do not change:

```text
test name
parameters
parameter annotations
parametrization
fixtures
assertions
matrix data
receipt/security setup
expected outcomes
tripwires
```

After editing, parse again and require:

```text
AST_BEFORE == AST_AFTER
```

If structural AST differs:

```text
TEST_SEMANTICS_CHANGED
→ STOP
```

No autoformat/auto-fix command.

# 6. no runtime-source re-edit

Reverify after the test edit:

```text
src/aiscc/runtime/docker.py
SHA-256:
f338225c13195d69c41f69f00a47fc1d00c616c94458ef361e32b97f7fde96fa
```

Any change:

```text
UNEXPECTED_RUNTIME_SOURCE_DELTA
→ STOP
```

# 7. mandatory static checks

Run:

```text
Python compile:
src/aiscc/runtime/docker.py
tests/unit/runtime/test_stockroom_docker_settlement.py

Ruff:
src/aiscc/runtime/docker.py
tests/unit/runtime/test_stockroom_docker_settlement.py

git diff --check

git diff --cached --name-only
```

Require:

```text
compile:
PASS

Ruff:
PASS

git diff --check:
PASS

index:
empty
```

If any fails:

```text
STATIC_CHECK_FAILURE
→ STOP
```

No same-turn repair after this gate.

# 8. mandatory new settlement regression

Only after section 7 PASS, run exactly:

```text
.venv/Scripts/python.exe -B -m pytest -q -p no:cacheprovider tests/unit/runtime/test_stockroom_docker_settlement.py -ra
```

Require:

```text
exit 0
failed 0
errors 0
```

Report exact passed/skipped count.

If nonzero:

```text
TEST_FAILURE
→ STOP
```

No same-turn repair.

# 9. mandatory existing Stockroom tool regression

Only after section 8 PASS, run exactly:

```text
.venv/Scripts/python.exe -B -m pytest -q -p no:cacheprovider tests/unit/providers/test_stockroom_tool.py -ra
```

Require exit 0.

If nonzero:

```text
TEST_FAILURE
→ STOP
```

No same-turn repair.

# 10. bounded pre-existing Docker regression discovery

Search only:

```text
tests/unit/runtime/test_docker*.py
tests/unit/runtime/*docker*.py
tests/** direct import of DockerRuntime
```

Exclude the newly created settlement test when deciding whether another pre-existing direct regression exists.

The 0918 result reported:

```text
NO_PREEXISTING_DIRECT_DOCKER_UNIT_MODULE
```

Confirm this result.

If clearly direct pre-existing modules exist, run only that bounded direct set.

If none, record:

```text
NO_PREEXISTING_DIRECT_DOCKER_UNIT_MODULE
```

If ambiguous and broad expansion would be required:

```text
TEST_SCOPE_AMBIGUOUS
→ STOP
```

No integration suite and no Docker command.

# 11. dynamic settlement truth-table admission

After the new regression PASS, report executed evidence for all authored settlement cases.

At minimum confirm executed coverage includes:

```text
unsettled T/F
unsettled F/T
unsettled F/F

exit zero
nonzero
timeout
cancel
bounded output
oversized output
invalid ASCII

settled valid exit zero
settled nonzero

runner absent
runner raises

receipt tampering/rebinding
one-use claimed dispatch
```

Required invariant:

```text
every unsettled case:
UNKNOWN_TOOL_OUTCOME
quarantine_required=true

no unsettled case:
KNOWN_TOOL_COMPLETED
KNOWN_TOOL_FAILURE
```

Settled known semantics must remain unchanged.

# 12. security/receipt preservation

From the executed tests report:

```text
authentic consumed PROCESS receipt:
required

scope/run/attempt binding:
enforced

dispatch claim:
one-use

replay/double consumption:
rejected

capability-free bypass:
absent
```

Do not claim actual runtime capability admission; this is unit/fake evidence.

# 13. strict no-execution ceiling

During this Task:

```text
Docker CLI/daemon/image:
NOT_RUN

Stockroom subprocess:
NOT_RUN

Stockroom CLI:
NOT_RUN

provider:
NOT_RUN

DB:
NOT_RUN

materializer:
NOT_RUN

scenario:
NOT_RUN

network:
NOT_RUN

Git add/commit/push:
NOT_RUN
```

Pytest with injected/fake runner is allowed.

# 14. final workspace

Before current Task lifecycle require:

```text
0207 provenance:
3

0918 provenance:
3

runtime candidate:
1

test candidate:
1

current Cycle/Judgment:
2

total excluding active Task:
10 exact

index:
empty
```

Then move:

```text
.aiassistant/tasks/active/20260910_0935_aiscc-p2-3-stockroom-docker-settlement-ruff-test-retry-1.md
→
.aiassistant/tasks/done/20260910_0935_aiscc-p2-3-stockroom-docker-settlement-ruff-test-retry-1.md
```

Final:

```text
11 exact Git-visible paths
index empty
```

No other path.

# 15. evidence contract

executor_required:

- inbound transport
- exact 10-path workspace gate
- exact predecessor/candidate identity
- AST-equivalent single-test formatting edit
- runtime source byte freeze
- static checks PASS
- new settlement regression PASS
- existing Stockroom tool regression PASS
- bounded Docker regression discovery/result
- executed settlement truth-table evidence
- security/receipt preservation evidence
- exact final workspace
- outbound result ZIP

reuse_allowed:

- 0918 source candidate
- 0918 static conflict diagnosis
- persisted B2/B3 contracts

human_owned:

```text
new Human QA:
NOT_REQUIRED

S4 HumanResult:
HUMAN_PENDING / outside Task

public distribution/license:
HUMAN_PENDING
```

forbidden:

- runtime-source modification
- test semantic modification
- capture audit continuation
- capture-runner implementation
- actual Docker/process/scenario execution
- DB
- Replay
- Git add/commit/push

# 16. mandatory stop

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
PREDECESSOR_OR_CANDIDATE_IDENTITY_MISMATCH
SCOPE_EXPANSION_REQUIRED
TEST_SEMANTICS_CHANGED
UNEXPECTED_RUNTIME_SOURCE_DELTA
STATIC_CHECK_FAILURE
TEST_SCOPE_AMBIGUOUS
TEST_FAILURE
CONTRACT_MISMATCH
UNEXPECTED_WORKSPACE_DELTA
ZIP_EXPORT_FAILED
```

Inbound cleanup refusal after canonical transport remains non-blocking.

# 17. export bundle + outbound ZIP

Bundle folder:

```text
.aiassistant/reports/target/20260910_0935_aiscc-p2-3-stockroom-docker-settlement-ruff-test-retry-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
TEST_FORMAT_EQUIVALENCE.md
SETTLEMENT_TRUTH_TABLE.md
SECURITY_RECEIPT_VERIFICATION.md
TEST_VERIFICATION.md
```

Include byte-preserving copies of:

```text
current Cycle
current Judgment
current done Task
src/aiscc/runtime/docker.py
tests/unit/runtime/test_stockroom_docker_settlement.py
```

Create adjacent outbound ZIP.

Use supported Windows extended-length path handling if needed for export packaging.

Require:

```text
one top-level bundle directory
readable / CRC PASS
required roots present
manifest coverage
folder/archive byte equality
```

# 18. final ceiling

Success:

```text
runtime settlement fix:
READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT

actual-capture entry audit:
STILL_INCOMPLETE

actual scenario execution:
NOT_STARTED

Replay:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

Do not resume the wider actual-capture audit in this Task.
