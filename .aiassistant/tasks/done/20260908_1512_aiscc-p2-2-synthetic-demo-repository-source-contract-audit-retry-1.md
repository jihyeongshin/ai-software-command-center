# 작업지시서: P2-2 Synthetic Demo Repository source/contract audit retry

## meta

- task_id: `20260908_1512_aiscc-p2-2-synthetic-demo-repository-source-contract-audit-retry-1`
- created_at: `2026-09-08T15:12:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `DISCOVERY_AUDIT / DESIGN_AUDIT / REWORK`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P2-2 synthetic demo repository source/domain/layout contract`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `187880eff48cbf2909e0fcadce75c6d2cb30ab31`
- required_base_tree: `1823346f7ec7c4da466d64f6823f0c8b3390f0cd`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `predecessor audit did not satisfy its required fresh-session boundary and violated mandatory transport STOP`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# Human-owned fresh IDE prerequisite

이번 Task는 반드시 **Human이 새로 연 IDE Executor chat**에서 시작한다.

다음은 fresh chat이 아니다.

```text
same conversation에서 model만 변경
same conversation에서 "작업을 재개하라"
same conversation에서 reasoning level 변경
```

Executor는 fresh chat을 스스로 생성하거나 충족했다고 주장하지 않는다.

# 현재 상태

```text
P2-1:
ACCEPTED / CLOSED / PERSISTED

P2-2 source/contract audit predecessor:
HOLD_REWORK_REQUIRED

P2-2 implementation:
NOT_STARTED

P2-3:
NOT_STARTED
```

# 이번 턴 목표

1. current Command Center transport를 정확히 완료한다.
2. predecessor blocked Task lifecycle을 exact hash 검증 후 `active → done`으로 정규화한다.
3. P2-2와 P2-3 current canonical ownership boundary를 처음부터 독립적으로 다시 감사한다.
4. existing demo/example/fixture/sample convention을 bounded inventory한다.
5. synthetic repository 최소 기능/안전/IP/재현성 contract를 확정 후보로 정리한다.
6. domain/layout 후보 최대 3개를 비교하고 1개 추천한다.
7. 후속 implementation Task용 exact proposed root/file/test/mutation contract를 제시한다.
8. conflict이면 source mutation 없이 exact canonical conflict로 STOP한다.

# 비목표

- predecessor partial audit를 accepted evidence로 승격
- demo/product/runtime/test/config mutation
- P2-3 scenario/replay 구현
- external repository/network
- Browser QA
- Git add/commit/push
- Project Source sync

# 반드시 읽을 canonical source

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

.aiassistant/records/aiscc/cycles/20260908_1512_aiscc-p2-2-source-contract-audit-blocked-transport-stop-and-fresh-session-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_1512_aiscc-p2-2-source-contract-audit-transport-stop-violation-judgment-1.md
```

Predecessor incomplete audit report/body는 retry의 substantive shortcut으로 사용하지 마라.
단, predecessor Task lifecycle/hash 검증을 위해 exact predecessor Task만 읽을 수 있다.

# 1. transport gate

Current package에 포함된 issued artifacts만 transport한다.

Transport failure 또는 ambiguity가 단 한 번이라도 발생하면:

```text
STOP IMMEDIATELY
```

그 뒤 path 수정/recovery를 시도하여 substantive audit을 계속하지 마라.

허용되는 transport recovery는 새 Command Center 지시 이후 별도 turn에서만 한다.

# 2. initial repository gate

Transport PASS 뒤:

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

이어야 한다.

Git-visible dirt는 transport 직후 exact 다음 4개만 허용한다.

```text
.aiassistant/records/aiscc/cycles/20260908_1443_aiscc-command-center-workflow-correction-final-acceptance-p2-2-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_1443_aiscc-command-center-workflow-correction-final-acceptance-judgment-1.md
.aiassistant/records/aiscc/cycles/20260908_1512_aiscc-p2-2-source-contract-audit-blocked-transport-stop-and-fresh-session-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_1512_aiscc-p2-2-source-contract-audit-transport-stop-violation-judgment-1.md
```

`old_cycle`, `old_judgment`는 predecessor package에서 아직 uncommitted provenance이고,
new two paths는 이번 package의 provenance다.

그 외 dirt가 있으면 `DIRTY_WORKSPACE_MIXED`로 STOP.

# 3. predecessor Task lifecycle normalization

Substantive audit 전에:

```text
source:
.aiassistant/tasks/active/20260908_1443_aiscc-p2-2-synthetic-demo-repository-source-contract-audit-1.md

expected SHA-256:
3035f62c1b978da5d835e771dc7138a2e789e3cb7349668d50f44ada3a9be92d
```

를 확인한다.

source가 exact hash이면:

```text
.aiassistant/tasks/active/20260908_1443_aiscc-p2-2-synthetic-demo-repository-source-contract-audit-1.md
→
.aiassistant/tasks/done/20260908_1443_aiscc-p2-2-synthetic-demo-repository-source-contract-audit-1.md
```

으로 이동한다.

destination이 이미 있으면 source/destination hash를 비교하고 exact equality를 보장한다.

이후 Git-visible expected set은:

```text
old CYCLE
old JUDGMENT
new CYCLE
new JUDGMENT
old blocked Task done
```

exact 5 paths다.

이 move는 predecessor audit acceptance를 의미하지 않는다.

# 4. independent source audit

Retry는 아래를 독립적으로 다시 확인한다.

## P2-2 candidate ownership

```text
project-owned fixed synthetic repository candidate asset
small public example system
deterministic local setup/build/test
safe synthetic-only data
no company/customer/private source
bounded Agent-work complexity
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
replay sanitization/admission/metadata
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

# 5. phase-number / baseline drift judgment

Current queue:

```text
P2-2 Synthetic Demo Repository
P2-3 Canonical Demo Scenario Pack and Recorded Replay Corpus
```

Older public-runtime baseline may group synthetic repository/version under P2-3.

Decide one:

```text
A. compatible decomposition
P2-2 prepares repository candidate
P2-3 owns scenario-time canonical version pin/admission

B. actual canonical conflict
```

A이면 exact source/path support를 report한다.

B이면:

```text
POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

로 STOP.
이번 Task에서 baseline 수정 금지.

# 6. domain/layout candidates

최대 3개.

각 후보:

```text
domain name
public/synthetic safety
language/runtime
proposed repository root
minimum files/modules
deterministic test command
intentional imperfection hooks
Agent task complexity
P2-3 extensibility
IP/license/private-data posture
```

추천안 1개를 명확히 선택한다.

Dialodog 또는 Human 회사/private product를 모사하지 마라.

# 7. exact implementation proposal

추천안에 대해:

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

을 proposal로 제출한다.

Executor는 이를 canonical acceptance로 확정하지 않는다.

# evidence contract

## executor_required

- `COMMAND_CENTER_ARTIFACT_TRANSPORT`
- `WORKSPACE_STATIC`
- `STATIC_SOURCE`
- `SOURCE_INVENTORY`
- `DESIGN_AUDIT`

## reuse_allowed

- P2-1 terminal closure
- accepted P1 security/public-runtime baseline only

Predecessor `1443` partial audit finding은 `REUSED_ACCEPTED`가 아니다.

## human_owned

```text
fresh IDE chat creation:
HUMAN_PROVIDED prerequisite

new Human QA:
NOT_REQUIRED

final domain/design acceptance:
Browser Command Center
```

## not_required

- tests/runtime
- Browser QA
- provider/live calls
- deployment
- Git persistence

## forbidden

- source mutation
- Git mutation
- external network/repository
- P2-3 implementation

# mandatory stop

STOP on:

```text
TRANSPORT_FAILURE
TRANSPORT_AMBIGUITY
FRESH_IDE_SESSION_NOT_HUMAN_ESTABLISHED
MISSING_REQUIRED_ARTIFACT
HEAD_OR_TREE_MISMATCH
INDEX_NOT_EMPTY
DIRTY_WORKSPACE_MIXED
PREDECESSOR_TASK_HASH_MISMATCH
CANONICAL_AUTHORITY_CONFLICT
POLICY_CONFLICT_INVESTIGATION_REQUIRED
SECURITY_BOUNDARY_UNCERTAIN
```

named blocker 뒤에는 최소 evidence/report/export만 수행한다.

# export bundle

Target:

```text
.aiassistant/reports/target/20260908_1512_aiscc-p2-2-synthetic-demo-repository-source-contract-audit-retry-1/
```

Required:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
P2_2_SOURCE_CONTRACT_AUDIT.md
```

# Task lifecycle

audit/report/export가 완료되면:

```text
.aiassistant/tasks/active/20260908_1512_aiscc-p2-2-synthetic-demo-repository-source-contract-audit-retry-1.md
→
.aiassistant/tasks/done/20260908_1512_aiscc-p2-2-synthetic-demo-repository-source-contract-audit-retry-1.md
```

Git stage/commit하지 마라.

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

Failure:

```text
P2-2 audit:
BLOCKED / <exact blocker>
```
