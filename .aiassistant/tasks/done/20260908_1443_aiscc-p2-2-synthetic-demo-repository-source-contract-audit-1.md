# 작업지시서: P2-2 Synthetic Demo Repository source/contract audit

## meta

- task_id: `20260908_1443_aiscc-p2-2-synthetic-demo-repository-source-contract-audit-1`
- created_at: `2026-09-08T14:43:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `DISCOVERY_AUDIT / DESIGN_AUDIT`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P2-2 synthetic demo repository source/domain/layout contract`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `187880eff48cbf2909e0fcadce75c6d2cb30ab31`
- required_base_tree: `1823346f7ec7c4da466d64f6823f0c8b3390f0cd`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `P2-2 demonstration source-contract audit is a distinct authority/context boundary from the completed Command Center workflow-governance update`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

## 이번 Task의 상태 의미

```text
P2-1:
ACCEPTED / CLOSED / PERSISTED

P2-2:
ENTRY_READY
but
NOT_STARTED until this Task begins substantive audit

P2-3:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

이번 Task는 P2-2 구현을 시작하기 전 source/domain/ownership contract를 동결하기 위한 **read-only audit**다.

Product/demo source를 생성하거나 수정하지 않는다.

## Human-owned IDE session prerequisite

이 Task는 fresh IDE Executor chat에서 수행한다.

새 chat 생성은 Human action이며 Executor가 수행하거나 완료를 주장하지 않는다.

## 이번 턴 목표

1. P2-2와 P2-3 사이의 current canonical ownership boundary를 exact source로 확인한다.
2. repository에 이미 존재하는 `demo`, `example`, `fixture`, synthetic-repository 유사 root/convention이 있는지 narrow inventory한다.
3. P2-2가 만들 synthetic repository가 충족해야 할 최소 기능/안전/IP/재현성 contract를 정리한다.
4. P2-3가 소유할 scenario/replay 책임을 P2-2에서 침범하지 않도록 분리한다.
5. synthetic repository domain/layout 후보를 최대 3개 제시하고 하나를 추천한다.
6. 후속 P2-2 implementation Task가 사용할 exact proposed root/path inventory와 verification plan을 제시한다.
7. canonical conflict가 있으면 구현 Task를 발행할 수 있도록 conflict를 exact path/문장 수준으로 보고한다.

## 비목표

- demo repository 파일 생성
- product/runtime/test/config mutation
- scenario pack 구현
- recorded run/replay 생성
- public deployment
- provider/live call
- external repository clone/download
- Browser QA
- Git add/commit/push
- Project Source mirror sync
- P2-3 시작

## 반드시 읽을 canonical source

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

.aiassistant/records/aiscc/cycles/20260908_1443_aiscc-command-center-workflow-correction-final-acceptance-p2-2-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_1443_aiscc-command-center-workflow-correction-final-acceptance-judgment-1.md
```

P2-2/P2-3 boundary를 확인하는 데 필요한 경우에만 repository bootstrap/current architecture의 exact relevant section을 추가로 읽을 수 있다. unrelated historical tasks/cycles/logs를 bulk-read하지 마라.

## initial workspace gate

Transport 완료 후 substantive audit 전에:

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

Git-visible dirt는 이번 transport로 들어온 exact 두 provenance artifact만 허용한다.

```text
.aiassistant/records/aiscc/cycles/20260908_1443_aiscc-command-center-workflow-correction-final-acceptance-p2-2-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_1443_aiscc-command-center-workflow-correction-final-acceptance-judgment-1.md
```

active Task는 ignored 상태여야 한다.

다른 Git-visible dirt가 있으면:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

정리/restore/absorb하지 마라.

## source audit scope

Read-only로 다음을 조사할 수 있다.

```text
repository top-level directory inventory
existing demo/example/fixture/sample roots
pyproject/package/runtime test conventions relevant to a standalone synthetic repository
security/runtime code only where fixed synthetic repository resource identity or isolation contract is encoded
```

금지:

```text
whole-repository bulk read
recursive unrelated source dump
external network
external repository inspection
```

## required semantic boundary audit

반드시 다음을 분리해서 보고한다.

### P2-2 candidate ownership

검증할 후보:

```text
project-owned fixed synthetic repository candidate asset
small public example system
deterministic local setup/build/test
safe synthetic-only data
no company/customer/private source
bounded complexity suitable for repeatable Agent work
intentional but controlled modification hooks/imperfections
no credential requirement
no external repository dependency
```

### P2-3 reserved ownership

P2-2에서 구현하지 말아야 할 후보:

```text
canonical scenario IDs/versions
scenario allowlist
Task/Evidence/Human ownership per scenario
actual AISCC scenario executions
recorded transition/evidence/judgment capture
Replay corpus
Replay sanitization/admission
truthful Recorded Run Replay metadata
```

### Security invariants

P2-2 proposal은 다음을 약화할 수 없다.

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

## phase-number / baseline drift check

Current exact queue:

```text
P2-2 Synthetic Demo Repository
P2-3 Canonical Demo Scenario Pack and Recorded Replay Corpus
```

Older public-runtime baseline may contain broader P2-3 wording including `project-owned synthetic repository/version`.

다음을 판정하라.

```text
A. compatible decomposition
   P2-2 prepares repository candidate;
   P2-3 owns scenario-time canonical version pin/admission

B. actual canonical conflict
   current documents assign the same exclusive semantic ownership incompatibly
```

A이면 exact supporting text/path를 보고한다.

B이면:

```text
POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

로 STOP하고 어떤 canonical baseline이 보정되어야 하는지만 제안한다. 이번 Task에서 baseline을 수정하지 않는다.

## domain/layout candidate requirements

최대 3개 후보만 제시한다.

각 후보마다:

```text
domain name
why public/synthetic-safe
expected language/runtime
proposed repository root
minimum files/modules
deterministic test command
intentional imperfection hooks
expected Agent task duration/complexity
P2-3 scenario extensibility
IP/license/private-data posture
```

추천안 하나를 명확히 선택한다.

Domain은 Dialodog 또는 사용자 회사/private product를 모사하지 마라.

## 후속 implementation Task를 위한 exact 제안

추천안에 대해 다음을 freeze candidate로 제시한다.

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
expected human verification
```

이것은 Command Center가 다음 Task에서 accept/reject할 proposal이며 Executor가 canonical policy로 확정하지 않는다.

## evidence contract

### executor_required

- `WORKSPACE_STATIC`: base HEAD/tree/index + expected transport dirt
- `STATIC_SOURCE`: relevant canonical P2-2/P2-3/security ownership evidence
- `SOURCE_INVENTORY`: narrow existing demo/example convention inventory
- `DESIGN_AUDIT`: candidate comparison + recommended exact implementation contract

### reuse_allowed

- P2-1 terminal closure and workflow correction: `REUSED_ACCEPTED`
- P1 security/public runtime baselines: accepted canonical source, applicability must be shown

### human_owned

```text
new Human QA:
NOT_REQUIRED

final product/domain acceptance:
Command Center judgment after audit, not Executor-owned
```

### not_required

- unit/integration/runtime execution
- Browser QA
- provider call
- deployment
- public release
- Git persistence

### forbidden

- source mutation
- Git mutation
- external network/repository
- P2-3 implementation
- proof substitution

## mandatory stop

STOP on:

```text
MISSING_REQUIRED_ARTIFACT
HEAD_OR_TREE_MISMATCH
INDEX_NOT_EMPTY
DIRTY_WORKSPACE_MIXED
CANONICAL_AUTHORITY_CONFLICT
POLICY_CONFLICT_INVESTIGATION_REQUIRED
SECURITY_BOUNDARY_UNCERTAIN
```

named blocker 뒤에는 최소 evidence/report/export만 수행한다.

## export bundle

Target:

```text
.aiassistant/reports/target/20260908_1443_aiscc-p2-2-synthetic-demo-repository-source-contract-audit-1/
```

Required:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
P2_2_SOURCE_CONTRACT_AUDIT.md
```

No changed product/canonical files should be exported because this Task is read-only apart from Task lifecycle/report artifacts.

## Task lifecycle

Executor-required audit/report/export가 완료되면:

```text
.aiassistant/tasks/active/20260908_1443_aiscc-p2-2-synthetic-demo-repository-source-contract-audit-1.md
→
.aiassistant/tasks/done/20260908_1443_aiscc-p2-2-synthetic-demo-repository-source-contract-audit-1.md
```

This tracked Task lifecycle path may become Git-visible, but do not stage or commit it in this Task.

## final response ceiling

Success:

```text
P2-2 source/contract audit:
READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT

P2-2 implementation:
NOT_STARTED

P2-3:
NOT_STARTED
```

Conflict:

```text
P2-2:
BLOCKED_POLICY_GAP / POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

Do not start implementation.
