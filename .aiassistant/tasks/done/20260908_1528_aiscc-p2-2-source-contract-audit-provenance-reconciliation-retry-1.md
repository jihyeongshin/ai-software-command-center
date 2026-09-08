# 작업지시서: P2-2 source/contract audit provenance reconciliation retry

## meta

- task_id: `20260908_1528_aiscc-p2-2-source-contract-audit-provenance-reconciliation-retry-1`
- created_at: `2026-09-08T15:28:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `DISCOVERY_AUDIT / DESIGN_AUDIT / REWORK`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P2-2 synthetic demo repository source/domain/layout contract`
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

P2-2 source/contract audit:
RETRY_REQUIRED

P2-2 implementation:
NOT_STARTED

P2-3:
NOT_STARTED
```

This Task continues in the existing Human-created fresh P2-2 IDE chat.

Do not open/request another IDE chat.

# why this retry exists

`1519` transport passed, but its workspace contract omitted two legitimate `1443` Command Center provenance files.

Those files are now explicitly admitted as expected pending governance provenance.

Do not delete or hide them.

# goal

1. Transport the current 1528 TASK/CYCLE/JUDGMENT.
2. Verify exact corrected pending governance inventory.
3. Normalize blocked 1443 and 1519 Task lifecycle from active→done using exact SHA checks.
4. Re-run the P2-2 / P2-3 source/contract audit independently from canonical source.
5. Produce domain/layout candidates and one exact recommendation.
6. Do not implement P2-2 source.
7. Do not start P2-3.

# initial transport contract

Use the already successful policy-compatible transport method from the 1519 turn.

Current package contains only:

```text
TASK:
20260908_1528_aiscc-p2-2-source-contract-audit-provenance-reconciliation-retry-1.md

CYCLE:
20260908_1528_aiscc-p2-2-audit-blocked-command-center-dirt-contract-correction-entry-1.cycle.md

JUDGMENT:
20260908_1528_aiscc-p2-2-audit-command-center-dirt-contract-correction-judgment-1.md

HANDOFF:
none
```

Any transport failure or policy block:

```text
STOP
```

No same-turn mechanism fallback after a policy block.

# repository gate after current transport

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

Expected Git-visible set is exact 9 paths:

```text
.aiassistant/records/aiscc/cycles/20260908_1443_aiscc-command-center-workflow-correction-final-acceptance-p2-2-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_1443_aiscc-command-center-workflow-correction-final-acceptance-judgment-1.md
.aiassistant/tasks/done/20260908_1512_aiscc-p2-2-synthetic-demo-repository-source-contract-audit-retry-1.md
.aiassistant/records/aiscc/cycles/20260908_1512_aiscc-p2-2-source-contract-audit-blocked-transport-stop-and-fresh-session-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_1512_aiscc-p2-2-source-contract-audit-transport-stop-violation-judgment-1.md
.aiassistant/records/aiscc/cycles/20260908_1519_aiscc-p2-2-audit-blocked-transport-tool-policy-recovery-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_1519_aiscc-p2-2-audit-transport-tool-policy-blocked-judgment-1.md
.aiassistant/records/aiscc/cycles/20260908_1528_aiscc-p2-2-audit-blocked-command-center-dirt-contract-correction-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_1528_aiscc-p2-2-audit-command-center-dirt-contract-correction-judgment-1.md
```

Current 1528 active Task is ignored.

No other Git-visible path is allowed.

If extra/missing exists:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Do not cleanup/restore/ignore/absorb.

# exact existing provenance validation

Verify these exact hashes before substantive audit:

```text
.aiassistant/records/aiscc/cycles/20260908_1443_aiscc-command-center-workflow-correction-final-acceptance-p2-2-entry-1.cycle.md
SHA-256:
65c764f1702c96f3750a09d68f4d72baef69303d96155960c78c9a18d2881f4c

.aiassistant/reports/aiscc/20260908_1443_aiscc-command-center-workflow-correction-final-acceptance-judgment-1.md
SHA-256:
8c0ab4ac32f0173af68a8d8db378b23673fcbf50331323d427659466e091e9b6
```

Mismatch:

```text
PENDING_PROVENANCE_HASH_MISMATCH
→ STOP
```

# blocked predecessor Task lifecycle normalization

Before substantive audit:

## 1443 Task

```text
source:
.aiassistant/tasks/active/20260908_1443_aiscc-p2-2-synthetic-demo-repository-source-contract-audit-1.md

expected source SHA-256:
3035f62c1b978da5d835e771dc7138a2e789e3cb7349668d50f44ada3a9be92d

destination:
.aiassistant/tasks/done/20260908_1443_aiscc-p2-2-synthetic-demo-repository-source-contract-audit-1.md
```

## 1519 Task

```text
source:
.aiassistant/tasks/active/20260908_1519_aiscc-p2-2-transport-policy-compatible-source-contract-audit-retry-1.md

expected source SHA-256:
f8b773e14e312cc71129cd6f736d1e591786e95574fcead56f0e499277057268

destination:
.aiassistant/tasks/done/20260908_1519_aiscc-p2-2-transport-policy-compatible-source-contract-audit-retry-1.md
```

For each:

```text
source exists:
verify exact SHA

destination absent:
move source → destination
verify destination SHA equality

destination present:
verify destination SHA
if source/destination equal:
remove only duplicate active source
if hashes differ:
STOP
```

Do not overwrite a differing `tasks/done` provenance file.

After both lifecycle normalizations, expected Git-visible set is exact 11 paths:

```text
the previous 9
+
.aiassistant/tasks/done/20260908_1443_aiscc-p2-2-synthetic-demo-repository-source-contract-audit-1.md
+
.aiassistant/tasks/done/20260908_1519_aiscc-p2-2-transport-policy-compatible-source-contract-audit-retry-1.md
```

active 1443 and 1519 Task paths must be absent.

This lifecycle normalization does not mean predecessor audit acceptance.

# must-read canonical source

Only after transport/workspace/lifecycle gates PASS:

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

.aiassistant/records/aiscc/cycles/20260908_1528_aiscc-p2-2-audit-blocked-command-center-dirt-contract-correction-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_1528_aiscc-p2-2-audit-command-center-dirt-contract-correction-judgment-1.md
```

Do not use partial source/design findings from 1443/1512/1519 as accepted shortcut evidence.

# P2-2 / P2-3 ownership audit

Independently determine whether canonical authority supports:

## P2-2 candidate ownership

```text
project-owned fixed synthetic repository candidate asset
small public synthetic example
deterministic local setup/build/test
safe synthetic-only data
bounded complexity
controlled imperfection hooks
no credential requirement
no external repository dependency
```

## P2-3 reserved ownership

```text
canonical scenario IDs/versions
scenario allowlist
per-scenario Task/Evidence/Human contracts
actual AISCC scenario executions
Recorded Replay corpus
Replay sanitization/admission/metadata
```

## security invariants

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

Older baseline may group `project-owned synthetic repository/version` under P2-3.

Choose only:

```text
A. compatible decomposition

P2-2 prepares repository candidate asset;
P2-3 owns scenario-time canonical version pin/admission.

B. actual canonical conflict
```

If B:

```text
POLICY_CONFLICT_INVESTIGATION_REQUIRED
→ STOP
```

Do not mutate the baseline in this Task.

# bounded source inventory

Read-only:

```text
repository top-level directory inventory
existing demo/example/fixture/sample roots
relevant package/test conventions
relevant fixed synthetic repository identity/security ownership code
```

No external network/repository.

No whole-repository bulk dump.

# domain/layout candidates

Maximum 3 candidates.

For each:

```text
domain name
public/synthetic safety
language/runtime
proposed repository root
minimum files/modules
deterministic test command
controlled imperfection hooks
expected Agent-task complexity
P2-3 extensibility
IP/license/private-data posture
```

Recommend exactly one.

Do not model Dialodog or Human company/private product.

# implementation proposal

Recommended candidate must include:

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

Proposal only.
Executor does not make it canonical.

# evidence contract

executor_required:

- `COMMAND_CENTER_ARTIFACT_TRANSPORT`
- `WORKSPACE_STATIC`
- `GOVERNANCE_PROVENANCE_INTEGRITY`
- `TASK_LIFECYCLE_NORMALIZATION`
- `STATIC_SOURCE`
- `SOURCE_INVENTORY`
- `DESIGN_AUDIT`

reuse_allowed:

- P2-1 terminal closure
- accepted P1 security/public-runtime baselines
- 1519 transport PASS / no-substantive-audit fact only

human_owned:

```text
new Human QA:
NOT_REQUIRED

final P2-2 source/domain acceptance:
Browser Command Center
```

not_required:

- test/runtime execution
- Browser QA
- provider/live calls
- deployment
- Git persistence

forbidden:

- product/demo/runtime/test/config mutation
- Git add/commit/push
- external network/repository
- P2-3 implementation
- deletion of admitted pending governance provenance

# mandatory stop

```text
TRANSPORT_FAILURE
TRANSPORT_TOOL_POLICY_BLOCKED
HEAD_OR_TREE_MISMATCH
INDEX_NOT_EMPTY
DIRTY_WORKSPACE_MIXED
PENDING_PROVENANCE_HASH_MISMATCH
PREDECESSOR_TASK_HASH_MISMATCH
TASK_LIFECYCLE_CONFLICT
CANONICAL_AUTHORITY_CONFLICT
POLICY_CONFLICT_INVESTIGATION_REQUIRED
SECURITY_BOUNDARY_UNCERTAIN
```

After blocker: minimal evidence/report/export only.

# export bundle

Target:

```text
.aiassistant/reports/target/20260908_1528_aiscc-p2-2-source-contract-audit-provenance-reconciliation-retry-1/
```

Required:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
PROVENANCE_RECONCILIATION_VERIFICATION.md
P2_2_SOURCE_CONTRACT_AUDIT.md
```

# current Task lifecycle

When executor-required audit/report/export completes:

```text
.aiassistant/tasks/active/20260908_1528_aiscc-p2-2-source-contract-audit-provenance-reconciliation-retry-1.md
→
.aiassistant/tasks/done/20260908_1528_aiscc-p2-2-source-contract-audit-provenance-reconciliation-retry-1.md
```

Then expected Git-visible pending governance set is exact 12 paths.

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
