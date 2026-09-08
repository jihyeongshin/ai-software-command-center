# 작업지시서: P2-2 Synthetic Stockroom candidate implementation transport retry

## meta

- task_id: `20260908_1602_aiscc-p2-2-synthetic-stockroom-candidate-implementation-transport-retry-1`
- created_at: `2026-09-08T16:02:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `QA_ONLY / TRANSPORT_RECOVERY + DEMO / BACKEND_IMPLEMENTATION / REWORK`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P2-2 fixed synthetic repository candidate asset`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `187880eff48cbf2909e0fcadce75c6d2cb30ab31`
- required_base_tree: `1823346f7ec7c4da466d64f6823f0c8b3390f0cd`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# current state

```text
P2-2 source/contract audit:
ACCEPTED

1549 implementation turn:
BLOCKED BEFORE TASK READ

P2-2 implementation:
NOT_STARTED / RETRY_AUTHORIZED

P2-3:
NOT_STARTED
```

Continue in the same Human-created fresh P2-2 implementation IDE chat.

# predecessor contract reuse

The exact implementation contract remains:

```text
.aiassistant/tasks/done/20260908_1549_aiscc-p2-2-synthetic-stockroom-candidate-implementation-1.md
```

After current transport succeeds, read:

1. this current active Task
2. `.aiassistant/tasks/done/20260908_1549_aiscc-p2-2-synthetic-stockroom-candidate-implementation-1.md`

The predecessor Task's **transport/session/lifecycle instructions are superseded** by this current Task.

The predecessor Task's following implementation sections are reused unchanged as the accepted implementation contract:

```text
- allowed source root
- exact 14-file allowlist
- Python 3.12.14 / stdlib-only contract
- exact file contracts
- exact seed
- domain constraints
- CLI contract
- exact 20-test contract
- deterministic build contract
- allowed verification commands
- implementation evidence boundaries
- P2-3 prohibitions
```

Do not treat the predecessor blocked status as implementation evidence.

# transport gate

The Browser Short Prompt for this Task is authoritative for the pre-Task transport procedure.

Transport must complete before this Task is substantively read/executed.

After transport, verify current package artifacts at exact canonical destinations.

# repository gate after transport

Require:

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

Expected Git-visible governance set is exact 17 paths:

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
- `.aiassistant/tasks/done/20260908_1549_aiscc-p2-2-synthetic-stockroom-candidate-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_1549_aiscc-p2-2-source-contract-audit-final-acceptance-implementation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1549_aiscc-p2-2-source-contract-audit-final-acceptance-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_1602_aiscc-p2-2-implementation-blocked-transport-prompt-regression-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1602_aiscc-p2-2-implementation-transport-prompt-regression-judgment-1.md`

Current active Task is ignored.

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

No cleanup/restore/ignore/absorb.

# implementation authority

Once transport and repository gates PASS, implement the Synthetic Stockroom contract from the predecessor done Task.

Only persistent source root:

```text
examples/synthetic-stockroom/
```

Exact persistent source count:

```text
14
```

Expected baseline tests:

```text
20
```

Runtime:

```text
CPython 3.12.14 exact
Python standard library only
offline
```

Generated verification artifact only:

```text
examples/synthetic-stockroom/.build/stockroom.pyz
```

Remove it after evidence capture.

No source/config/test changes outside the predecessor Task's exact allowlist.

# evidence contract

executor_required:

- current artifact transport
- exact workspace gate
- exact 14-file source implementation
- 20/20 unit tests
- deterministic repeat-build byte equality
- module CLI / pyz CLI parity
- seed/source hash stability
- bounded static security/provenance checks
- exact final workspace inventory

reuse_allowed:

- accepted 1528 source/contract audit
- exact implementation contract in `.aiassistant/tasks/done/20260908_1549_aiscc-p2-2-synthetic-stockroom-candidate-implementation-1.md`
- P1 security/public-runtime canonical invariants

human_owned:

```text
new Human QA:
NOT_REQUIRED

implementation acceptance:
Browser Command Center
```

not_required:

- full AISCC suite
- Docker isolation proof
- public Live
- Replay
- Git persistence
- P2-3

forbidden:

- external network/package install/repository
- Git add/commit/push
- scenario enrollment
- source outside exact candidate allowlist
- P2-3 work

# final workspace

Before current Task lifecycle move:

```text
17 governance
+
14 Synthetic Stockroom source
=
31 Git-visible paths exact
```

No `.build/stockroom.pyz`, `__pycache__`, `.pyc`, or other residue.

After current Task active→done:

```text
18 governance
+
14 source
=
32 Git-visible paths exact
```

Do not stage or commit.

# Task lifecycle

After implementation/evidence/report/export complete:

```text
.aiassistant/tasks/active/20260908_1602_aiscc-p2-2-synthetic-stockroom-candidate-implementation-transport-retry-1.md
→
.aiassistant/tasks/done/20260908_1602_aiscc-p2-2-synthetic-stockroom-candidate-implementation-transport-retry-1.md
```

# export bundle

Target:

```text
.aiassistant/reports/target/20260908_1602_aiscc-p2-2-synthetic-stockroom-candidate-implementation-transport-retry-1/
```

Required:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
IMPLEMENTATION_VERIFICATION.md
TEST_VERIFICATION.md
BUILD_CLI_VERIFICATION.md
TRANSPORT_VERIFICATION.md
```

Export current changed source/provenance only, preserving project-relative paths.

# mandatory stop

```text
TRANSPORT_TOOL_POLICY_BLOCKED
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

# final ceiling

Success:

```text
P2-2 Synthetic Stockroom implementation:
ACCEPTED_CANDIDATE / READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT

P2-2:
NOT_CLOSED

P2-3:
NOT_STARTED
```
