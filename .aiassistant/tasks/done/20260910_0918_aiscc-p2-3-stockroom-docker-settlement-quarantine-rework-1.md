# 작업지시서: P2-3 Stockroom Docker settlement/quarantine rework

## meta

- task_id: `20260910_0918_aiscc-p2-3-stockroom-docker-settlement-quarantine-rework-1`
- created_at: `2026-09-10T09:18:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `RUNTIME_SAFETY_REWORK / UNIT_REGRESSION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `Stockroom Docker process settlement classification`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `d8fbcfa9d36a7531819149037240855cafdd088d`
- required_base_tree: `e224f31268057e400918ece352b72a0388d4091d`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `source/static runtime-entry audit → runtime source/test mutation`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. purpose

The 0207 actual-capture entry audit stopped on a canonical runtime/security conflict.

This Task fixes only that conflict.

It does NOT resume the wider capture audit and does NOT execute Docker or any scenario.

# 1. inbound ZIP bootstrap

The Browser Short Prompt's exact delivery ZIP SHA-256 is the bootstrap integrity anchor.

Current delivery ZIP contains only:

```text
TASK:
20260910_0918_aiscc-p2-3-stockroom-docker-settlement-quarantine-rework-1.md

CYCLE:
20260910_0918_aiscc-p2-3-actual-capture-entry-audit-blocked-runtime-settlement-rework-entry-1.cycle.md
SHA-256:
239b189e270c4fb7e3896bda2ad4552708567b64d0e5abec5065b080277267d3
destination:
.aiassistant/records/aiscc/cycles/20260910_0918_aiscc-p2-3-actual-capture-entry-audit-blocked-runtime-settlement-rework-entry-1.cycle.md

JUDGMENT:
20260910_0918_aiscc-p2-3-runtime-settlement-canonical-conflict-judgment-1.md
SHA-256:
5c811f58429fc37b4a212f922d12b52b7632e20f4bb6c7e217c5284246b5092e
destination:
.aiassistant/reports/aiscc/20260910_0918_aiscc-p2-3-runtime-settlement-canonical-conflict-judgment-1.md

HANDOFF:
none
```

Executor:

1. verify exact ZIP filename/SHA-256;
2. validate archive readability/CRC/member safety;
3. materialize TASK first to `.aiassistant/tasks/active/20260910_0918_aiscc-p2-3-stockroom-docker-settlement-quarantine-rework-1.md`;
4. read TASK;
5. materialize Cycle/Judgment to exact canonical destinations;
6. verify exact hashes.

Bootstrap failure before canonical TASK placement:

```text
STOP
no report/export
no substantive project mutation
```

After canonical transport, inbound cleanup refusal is non-blocking.

# 2. repository gate

Require after current artifact placement:

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

Expected Git-visible set excluding current active Task is exact 5 paths:

- `.aiassistant/records/aiscc/cycles/20260910_0207_aiscc-p2-3-phase1b-closed-actual-capture-runtime-entry-audit-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_0207_aiscc-p2-3-phase1b-terminal-state-reconciliation-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260910_0207_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_0918_aiscc-p2-3-actual-capture-entry-audit-blocked-runtime-settlement-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_0918_aiscc-p2-3-runtime-settlement-canonical-conflict-judgment-1.md`

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Do not cleanup/restore/stash/reset/absorb.

# 3. predecessor identity

Verify exact:

- `.aiassistant/tasks/done/20260910_0207_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-1.md`  `e97b19297ce70d9ebb9f714b64ff83facf13e91c44f65c4ca6c4a0d0adb94cb0`
- `.aiassistant/records/aiscc/cycles/20260910_0207_aiscc-p2-3-phase1b-closed-actual-capture-runtime-entry-audit-1.cycle.md`  `5a68361c98b6165cdd6fa20adf0cc6ca8df99ada519c5c51efc6123f91c0b339`
- `.aiassistant/reports/aiscc/20260910_0207_aiscc-p2-3-phase1b-terminal-state-reconciliation-final-acceptance-judgment-1.md`  `e6e9266e9f6feedca478b7062d62af47c1b4442d8e719bb4e7ff8f9d59b3e6fa`

Verify current source starting hash:

```text
src/aiscc/runtime/docker.py
SHA-256:
196b8568e950a8d422feaceb1fd6601ab7478d4f3488d4f29ddb20c7059891c5
```

Verify frozen neighbors:

- `src/aiscc/providers/stockroom_tool.py`  `ad02321999b2b42039007c4dc6d55d20502004c137486ca33bfc191119d7dbb7`
- `src/aiscc/security/policy.py`  `ecb008330040966436c87d24aba0245627691cb076c4c77b6778b646b074cfe9`

Any mismatch:

```text
PREDECESSOR_OR_SOURCE_IDENTITY_MISMATCH
→ STOP
```

# 4. must-read authority

Read fully before source mutation:

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/AISCC_RUNTIME_SUBSTRATE.md
.aiassistant/rules/AISCC_SECURITY_SANDBOX.md
.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md

.aiassistant/records/aiscc/cycles/20260910_0918_aiscc-p2-3-actual-capture-entry-audit-blocked-runtime-settlement-rework-entry-1.cycle.md
.aiassistant/reports/aiscc/20260910_0918_aiscc-p2-3-runtime-settlement-canonical-conflict-judgment-1.md

.aiassistant/tasks/done/20260910_0207_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-1.md
.aiassistant/records/aiscc/cycles/20260910_0207_aiscc-p2-3-phase1b-closed-actual-capture-runtime-entry-audit-1.cycle.md
.aiassistant/reports/aiscc/20260910_0207_aiscc-p2-3-phase1b-terminal-state-reconciliation-final-acceptance-judgment-1.md

src/aiscc/runtime/docker.py
src/aiscc/providers/stockroom_tool.py
src/aiscc/security/policy.py
```

Read direct type definitions imported by `docker.py` only as needed.

No recursive old Task must-read activation.

# 5. exact mutation allowlist

Only:

```text
MODIFY:
src/aiscc/runtime/docker.py

CREATE:
tests/unit/runtime/test_stockroom_docker_settlement.py
```

Rules:

```text
src/aiscc/runtime/docker.py:
must match starting SHA above

tests/unit/runtime/test_stockroom_docker_settlement.py:
must be absent before mutation

other source/config/test:
0 changes
```

If the test path already exists:

```text
UNEXPECTED_EXISTING_PATH
→ STOP
```

If another product/test path is required:

```text
SCOPE_EXPANSION_REQUIRED
→ STOP
```

# 6. canonical settlement invariant

For the Stockroom consumed-process path, a result may be classified as known completed/known failed only when process/resource settlement is proven.

At minimum:

```text
settled =
termination_proven
and owner_reconciled
```

Required fail-closed rule:

```text
if not settled:
    outcome = UNKNOWN_TOOL_OUTCOME
    quarantine_required = true
```

This rule is independent of:

```text
exit code
timeout
cancel
stdout/stderr size
stdout/stderr content
```

An unsettled observation must never reach:

```text
KNOWN_TOOL_COMPLETED
KNOWN_TOOL_FAILED
quarantine_required=false
```

# 7. preserve settled semantics

When:

```text
termination_proven=true
owner_reconciled=true
```

preserve current bounded semantics.

Required matrix:

```text
settled + exit 0 + valid bounded output:
eligible for KNOWN_TOOL_COMPLETED

settled + nonzero exit:
KNOWN_TOOL_FAILED under current exact contract

settled + timeout/cancel:
retain current known failure classification only if the current contract treats
the observation as completely settled

settled + oversized/invalid bounded capture:
retain current safe known-failure behavior
```

Do not turn all failures into UNKNOWN.

Do not weaken finite timeout/output bounds.

# 8. unknown outcome details

The unknown branch must preserve/emit the current typed unknown result contract, including:

```text
outcome:
UNKNOWN_TOOL_OUTCOME

quarantine_required:
true

no success disclosure

no retry authorization

no false settled/cleanup proof
```

Use existing result/reason types and repository-style stable codes.

Do not add a new competing result type unless required by existing type exhaustiveness.

# 9. no downstream compensation

Do NOT fix this at:

```text
src/aiscc/providers/stockroom_tool.py
```

The runtime boundary itself must enforce the invariant before downstream dispatcher validation.

`stockroom_tool.py` remains byte-frozen.

Do not require callers to remember an additional ownership check.

# 10. regression test owner

Create:

```text
tests/unit/runtime/test_stockroom_docker_settlement.py
```

This is the direct unit owner for the missing settlement invariant.

Use only injected/fake `stockroom_runner` observations.

No subprocess/Docker daemon.

Minimum cases:

```text
exit 0 / bounded / no timeout / no cancel
termination_proven=true
owner_reconciled=false
→ UNKNOWN + quarantine

exit 0 / bounded
termination_proven=false
owner_reconciled=true
→ UNKNOWN + quarantine

exit 0 / bounded
termination_proven=false
owner_reconciled=false
→ UNKNOWN + quarantine

nonzero exit / unsettled
→ UNKNOWN + quarantine

timeout / unsettled
→ UNKNOWN + quarantine

cancel / unsettled
→ UNKNOWN + quarantine

settled valid exit 0
→ KNOWN_TOOL_COMPLETED / no quarantine

settled nonzero
→ existing KNOWN_TOOL_FAILED semantics
```

Also prove the missing-runner branch remains:

```text
UNKNOWN_TOOL_OUTCOME
quarantine_required=true
```

# 11. one-use receipt/security preservation

The test may construct the minimum authentic consumed receipt/claimed dispatch required to reach `run_consumed_stockroom`.

Prove the change does not bypass:

```text
authentic consumed PROCESS receipt requirement
claimed-dispatch one-use binding
scope fingerprint validation
state/run/attempt binding
```

Do not modify SecurityPolicy or receipt code.

If the direct runtime unit cannot construct a valid receipt without unrelated mutation, use the narrowest current test helper/import. Do not invent a capability-free bypass.

# 12. static checks

Before pytest run non-mutating checks:

```text
Python compile:
src/aiscc/runtime/docker.py
tests/unit/runtime/test_stockroom_docker_settlement.py

Ruff:
src/aiscc/runtime/docker.py
tests/unit/runtime/test_stockroom_docker_settlement.py

git diff --check:
PASS

index:
empty
```

No auto-fix/formatter.

If static check fails:

```text
STATIC_CHECK_FAILURE
→ STOP
```

No same-turn repair after a mandatory static failure.

# 13. mandatory new regression

Run exactly:

```text
.venv/Scripts/python.exe -B -m pytest -q -p no:cacheprovider tests/unit/runtime/test_stockroom_docker_settlement.py -ra
```

Require exit 0.

If nonzero:

```text
TEST_FAILURE
→ STOP
```

No same-turn repair.

# 14. mandatory existing Stockroom tool regression

Only after new regression PASS:

```text
.venv/Scripts/python.exe -B -m pytest -q -p no:cacheprovider tests/unit/providers/test_stockroom_tool.py -ra
```

Require exit 0.

This verifies the runtime change did not break the accepted higher-level Stockroom dispatch contract.

Any failure:

```text
TEST_FAILURE
→ STOP
```

No same-turn repair.

# 15. bounded runtime regression discovery

Search only:

```text
tests/unit/runtime/test_docker*.py
tests/unit/runtime/*docker*.py
tests/** direct import of DockerRuntime
```

Exclude the newly created test when deciding whether another pre-existing direct regression exists.

If clearly direct pre-existing unit modules exist, run the bounded set.

If none:

```text
NO_PREEXISTING_DIRECT_DOCKER_UNIT_MODULE
```

If ambiguous and broad expansion would be required:

```text
TEST_SCOPE_AMBIGUOUS
→ STOP
```

Do not run integration suites or Docker commands.

# 16. source review after tests

Verify final source enforces:

```text
NOT settled
→ UNKNOWN_TOOL_OUTCOME
→ quarantine true
```

before ordinary known success/failure classification.

Report a truth table covering at least:

```text
settled/unsettled
exit zero/nonzero
timeout/cancel
bounded/unbounded
```

No row with `settled=false` may produce known outcome.

# 17. strict non-execution boundary

This Task must perform:

```text
0 Docker command
0 subprocess process execution for Stockroom
0 Docker daemon access
0 image inspect/build/pull/run
0 Stockroom CLI
0 provider call
0 tool dispatch outside unit fakes
0 DB
0 materialization
0 scenario execution
0 network
```

Pytest itself is allowed; runtime collaborators must be fake/injected.

# 18. final workspace

Before current Task lifecycle expected:

```text
0207 provenance:
3 exact paths

current Cycle/Judgment:
2 exact paths

runtime source/test:
2 exact paths

total excluding active Task:
7 exact
```

Then move:

```text
.aiassistant/tasks/active/20260910_0918_aiscc-p2-3-stockroom-docker-settlement-quarantine-rework-1.md
→
.aiassistant/tasks/done/20260910_0918_aiscc-p2-3-stockroom-docker-settlement-quarantine-rework-1.md
```

Final:

```text
8 exact Git-visible paths
index empty
```

No Git add/commit.

# 19. evidence contract

executor_required:

- inbound transport
- exact 5-path preflight
- predecessor/source identity
- exact two-path mutation
- settlement truth-table proof
- new direct unit regression PASS
- existing Stockroom tool regression PASS
- bounded pre-existing Docker test discovery/result
- exact no-runtime-execution proof
- final 8-path workspace
- outbound result ZIP

reuse_allowed:

- 0207 source conflict evidence
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

```text
capture audit continuation
capture runner implementation
provider/tool/security shared mutation
actual Docker/process/scenario execution
DB
Replay
Git add/commit/push
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
PREDECESSOR_OR_SOURCE_IDENTITY_MISMATCH
UNEXPECTED_EXISTING_PATH
SCOPE_EXPANSION_REQUIRED
STATIC_CHECK_FAILURE
TEST_SCOPE_AMBIGUOUS
TEST_FAILURE
CONTRACT_MISMATCH
UNEXPECTED_WORKSPACE_DELTA
ZIP_EXPORT_FAILED
```

Inbound cleanup refusal after canonical transport remains non-blocking.

# 21. export bundle + outbound ZIP

Bundle folder:

```text
.aiassistant/reports/target/20260910_0918_aiscc-p2-3-stockroom-docker-settlement-quarantine-rework-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
IMPLEMENTATION_MANIFEST.md
SETTLEMENT_TRUTH_TABLE.md
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

Require:

```text
one top-level bundle directory
readable / CRC PASS
required roots present
manifest coverage
folder/archive byte equality
```

# 22. final ceiling

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

Do not resume the wider capture audit in this Task.
