# 작업지시서: P2-2 transport-policy-compatible source/contract audit retry

## meta

- task_id: `20260908_1519_aiscc-p2-2-transport-policy-compatible-source-contract-audit-retry-1`
- created_at: `2026-09-08T15:19:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `QA_ONLY / TRANSPORT_RECOVERY + DISCOVERY_AUDIT / DESIGN_AUDIT / REWORK`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `Command Center artifact transport recovery + P2-2 synthetic repository contract audit`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `187880eff48cbf2909e0fcadce75c6d2cb30ab31`
- required_base_tree: `1823346f7ec7c4da466d64f6823f0c8b3390f0cd`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# current state

```text
P2-1:
ACCEPTED / CLOSED / PERSISTED

1512 retry:
BLOCKED_POLICY_GAP / TRANSPORT_TOOL_POLICY_BLOCKED

P2-2 substantive audit:
NOT_STARTED

P2-2 implementation:
NOT_STARTED

P2-3:
NOT_STARTED
```

This Task is executed in the already Human-created fresh P2-2 IDE chat.
Do not open or request another IDE chat.

# goal

1. Perform the newly authorized transport recovery exactly.
2. Preserve the blocked `1512` Task/Cycle/Judgment as canonical provenance.
3. Place this current Task/Cycle/Judgment canonically.
4. Only after all transport gates PASS, begin the P2-2 source/contract audit from scratch.
5. Complete the same bounded design/source audit intended by the predecessor retry.
6. Do not implement P2-2 source.

# transport method contract

The semantic copy/hash/remove contract is unchanged.

The previous combined process command was blocked by policy.

For this retry:

```text
FIRST CHOICE:
use IDE-native / agent-native file operations that do not spawn a shell/process,
but only if they can access the exact Downloads source and exact destination.

IF no such native operation is available:
PowerShell may be used, but each step must be one single-purpose operation.

Allowed single-purpose examples:
- calculate one source SHA-256
- create/copy one exact file
- calculate one destination SHA-256
- remove one exact verified Downloads source file

DO NOT combine multiple transport phases in one PowerShell command/script.

DO NOT use:
- recursive delete
- wildcard delete
- broad copy
- loop over Downloads
- package-wide mutation command
```

If any operation receives:

```text
blocked by policy
approval denied
permission denied
ambiguous tool refusal
```

then:

```text
STOP IMMEDIATELY
```

Do not try a second transport mechanism in the same turn.

# issued artifact set

The current flat delivery package contains six exact files:

## predecessor blocked provenance

```text
20260908_1512_aiscc-p2-2-synthetic-demo-repository-source-contract-audit-retry-1.md
20260908_1512_aiscc-p2-2-source-contract-audit-blocked-transport-stop-and-fresh-session-retry-entry-1.cycle.md
20260908_1512_aiscc-p2-2-source-contract-audit-transport-stop-violation-judgment-1.md
```

## current retry

```text
20260908_1519_aiscc-p2-2-transport-policy-compatible-source-contract-audit-retry-1.md
20260908_1519_aiscc-p2-2-audit-blocked-transport-tool-policy-recovery-entry-1.cycle.md
20260908_1519_aiscc-p2-2-audit-transport-tool-policy-blocked-judgment-1.md
```

No HANDOFF.

# exact canonical destinations

```text
PREDECESSOR 1512 TASK
→ .aiassistant/tasks/done/20260908_1512_aiscc-p2-2-synthetic-demo-repository-source-contract-audit-retry-1.md

PREDECESSOR 1512 CYCLE
→ .aiassistant/records/aiscc/cycles/20260908_1512_aiscc-p2-2-source-contract-audit-blocked-transport-stop-and-fresh-session-retry-entry-1.cycle.md

PREDECESSOR 1512 JUDGMENT
→ .aiassistant/reports/aiscc/20260908_1512_aiscc-p2-2-source-contract-audit-transport-stop-violation-judgment-1.md

CURRENT 1519 TASK
→ .aiassistant/tasks/active/20260908_1519_aiscc-p2-2-transport-policy-compatible-source-contract-audit-retry-1.md

CURRENT 1519 CYCLE
→ .aiassistant/records/aiscc/cycles/20260908_1519_aiscc-p2-2-audit-blocked-transport-tool-policy-recovery-entry-1.cycle.md

CURRENT 1519 JUDGMENT
→ .aiassistant/reports/aiscc/20260908_1519_aiscc-p2-2-audit-transport-tool-policy-blocked-judgment-1.md
```

The predecessor Task goes directly to `tasks/done` because its Executor turn is already terminally blocked and judged. This is an explicit lifecycle recovery.

# initial repository gate after transport

After all six transport items PASS:

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

Git-visible expected set:

```text
.aiassistant/tasks/done/20260908_1512_aiscc-p2-2-synthetic-demo-repository-source-contract-audit-retry-1.md
.aiassistant/records/aiscc/cycles/20260908_1512_aiscc-p2-2-source-contract-audit-blocked-transport-stop-and-fresh-session-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_1512_aiscc-p2-2-source-contract-audit-transport-stop-violation-judgment-1.md
.aiassistant/records/aiscc/cycles/20260908_1519_aiscc-p2-2-audit-blocked-transport-tool-policy-recovery-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_1519_aiscc-p2-2-audit-transport-tool-policy-blocked-judgment-1.md
```

exactly 5 paths.

Current active Task is ignored.

Any other Git-visible dirt:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

# must-read after transport

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md

.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md
.aiassistant/reports/aiscc/AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md
.aiassistant/rules/AISCC_SECURITY_SANDBOX.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/records/aiscc/cycles/20260908_1519_aiscc-p2-2-audit-blocked-transport-tool-policy-recovery-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_1519_aiscc-p2-2-audit-transport-tool-policy-blocked-judgment-1.md
```

Do not reuse predecessor partial P2-2 audit observations as accepted evidence.

# P2-2 / P2-3 audit

Independently determine whether the current canonical boundary supports:

```text
P2-2:
fixed synthetic repository candidate asset
small public synthetic example
deterministic local setup/build/test
safe synthetic-only data
bounded complexity
controlled imperfection hooks

P2-3:
canonical scenario IDs/versions
scenario allowlist
scenario Task/Evidence/Human contracts
actual AISCC scenario executions
Recorded Replay corpus
Replay sanitization/admission/metadata
```

Security invariants remain:

```text
PUBLIC_BOUNDED_LIVE:
fixed synthetic repository only
no external repository/upload
no owner/private workspace
no arbitrary shell/network
server-defined bounded scenario actions only

PUBLIC_RECORDED_REPLAY:
no source mutation
no process/tool/network/provider execution
```

# baseline drift judgment

Current queue:

```text
P2-2 Synthetic Demo Repository
P2-3 Canonical Demo Scenario Pack and Recorded Replay Corpus
```

Older baseline may place `project-owned synthetic repository/version` under P2-3.

Choose only:

```text
A. compatible decomposition
P2-2 prepares repository candidate;
P2-3 owns scenario-time canonical version pin/admission

B. actual canonical conflict
```

If B:

```text
POLICY_CONFLICT_INVESTIGATION_REQUIRED
→ STOP
```

No baseline mutation in this Task.

# source inventory

Bounded read-only inventory only:

```text
repository top-level
existing demo/example/fixture/sample roots
relevant package/test conventions
relevant synthetic repository identity/security contract
```

No external network/repository.

# domain/layout candidate output

Maximum 3 candidates.

For each:

```text
domain
public/synthetic safety
language/runtime
proposed repository root
minimum files/modules
deterministic test command
controlled imperfection hooks
Agent-task complexity
P2-3 extensibility
IP/license/private-data posture
```

Recommend exactly one.

Do not model Dialodog or Human company/private products.

# exact implementation proposal

For the recommended candidate provide:

```text
proposed root path
proposed file list
baseline behavior
baseline passing tests
intentional defect/missing-evidence hooks
allowed mutation root
forbidden paths
verification commands
security/public provenance checks
expected Human verification
```

This is a proposal, not Executor-owned acceptance.

# evidence contract

executor_required:

- `COMMAND_CENTER_ARTIFACT_TRANSPORT`
- `WORKSPACE_STATIC`
- `STATIC_SOURCE`
- `SOURCE_INVENTORY`
- `DESIGN_AUDIT`

reuse_allowed:

- P2-1 terminal closure
- accepted P1 security/public runtime baselines

human_owned:

```text
new Human QA:
NOT_REQUIRED

final P2-2 domain/design acceptance:
Browser Command Center
```

not_required:

- unit/integration/runtime execution
- Browser QA
- provider/live calls
- deployment
- Git persistence

forbidden:

- product/demo/runtime/test/config mutation
- Git add/commit/push
- P2-3 implementation
- external network/repository

# mandatory stop

```text
TRANSPORT_TOOL_POLICY_BLOCKED
TRANSPORT_FAILURE
TRANSPORT_AMBIGUITY
MISSING_REQUIRED_ARTIFACT
HEAD_OR_TREE_MISMATCH
INDEX_NOT_EMPTY
DIRTY_WORKSPACE_MIXED
CANONICAL_AUTHORITY_CONFLICT
POLICY_CONFLICT_INVESTIGATION_REQUIRED
SECURITY_BOUNDARY_UNCERTAIN
```

After a named blocker: minimal evidence/report/export only.

# export bundle

Target:

```text
.aiassistant/reports/target/20260908_1519_aiscc-p2-2-transport-policy-compatible-source-contract-audit-retry-1/
```

Required:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
TRANSPORT_VERIFICATION.md
P2_2_SOURCE_CONTRACT_AUDIT.md
```

# Task lifecycle

After audit/report/export completion:

```text
.aiassistant/tasks/active/20260908_1519_aiscc-p2-2-transport-policy-compatible-source-contract-audit-retry-1.md
→
.aiassistant/tasks/done/20260908_1519_aiscc-p2-2-transport-policy-compatible-source-contract-audit-retry-1.md
```

Do not stage or commit.

# final ceiling

Success:

```text
P2-2 source/contract audit:
READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT

P2-2 implementation:
NOT_STARTED

P2-3:
NOT_STARTED
```
