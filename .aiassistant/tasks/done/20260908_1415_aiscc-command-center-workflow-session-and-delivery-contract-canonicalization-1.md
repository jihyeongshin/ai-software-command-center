# 작업지시서: Command Center workflow session and artifact-delivery canonicalization

## meta

- task_id: `20260908_1415_aiscc-command-center-workflow-session-and-delivery-contract-canonicalization-1`
- created_at: `2026-09-08T14:15:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `WORKFLOW_RULE_UPDATE / COMMAND_CENTER_RECORD_UPDATE / GIT_PERSISTENCE`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `Command Center workflow authority + P2-1 terminal state records`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `1fb9fd5e29e85481fa3c6ce78542de1fda6bf138`
- required_base_tree: `eaed171656a15440ea5444ba2d56ac939f625f56`
- fresh_ide_executor_chat: `REQUIRED_BY_COMMAND_CENTER`
- browser_session_rotation: `NOT_REQUIRED`

## Human-owned IDE session boundary

This Task MUST be executed in a fresh IDE Executor chat.

Reason:

```text
the predecessor IDE thread completed P2-1 final persistence
→ this Task changes canonical Command Center workflow authority
→ authority/context boundary is explicit
```

The IDE Executor must not attempt to create a new chat itself.

The Browser Command Center will tell Human to open the fresh IDE chat before providing the Short Prompt.

## 현재 상태

```text
P2-1E:
ACCEPTED / PERSISTED

P2-1:
ACCEPTED / CLOSED by Browser Command Center judgment

P2-1 persistence commit:
1fb9fd5e29e85481fa3c6ce78542de1fda6bf138

P2-2:
NOT_STARTED / ENTRY_READY

current governance prerequisite:
canonicalize corrected Command Center workflow before P2-2 execution
```

## 이번 턴 목표

1. Transported P2-1 terminal Cycle/Judgment를 canonical path에서 검증한다.
2. Human-corrected fresh IDE session rule을 canonical Command Center workflow에 반영한다.
3. 잘못 일반화된 mandatory post-judgment Browser rotation을 명시적으로 supersede한다.
4. TASK/CYCLE/JUDGMENT/HANDOFF flat ZIP delivery + Executor copy/hash/remove transport를 canonicalize한다.
5. Command Center templates/rubrics가 새 계약을 실제 후속 Task 발행에 사용할 수 있도록 정렬한다.
6. `CURRENT_STATE_SUMMARY`, `DECISION_REGISTER`, `NEXT_ACTIONS`에 P2-1 terminal closure와 새 workflow decisions를 반영한다.
7. exact allowlist로 governance-only Git persistence를 수행한다.
8. P2-2는 시작하지 않는다.

## 비목표

- product/runtime/test/config source 수정
- P2-2 Synthetic Demo Repository 구현
- Browser Project Source 업로드
- deployment
- Git push
- historical Cycle/Handoff rewrite
- 과거 `20260902_1621` artifact 삭제 또는 변조
- 모든 Handoff를 금지하는 정책
- 모든 Task에 fresh IDE chat을 강제하는 정책

## 반드시 읽을 문서

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md
.aiassistant/rules/AISCC_PROJECT_SOURCE_MIRROR.md

.aiassistant/records/command-center/README.md
.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md
.aiassistant/records/command-center/TASK_FILE_TEMPLATE.md
.aiassistant/records/command-center/SHORT_EXECUTOR_PROMPT_TEMPLATE.md
.aiassistant/records/command-center/JUDGMENT_RUBRIC.md
.aiassistant/records/command-center/CYCLE_RECORD_TEMPLATE.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/records/aiscc/cycles/20260908_1415_aiscc-p2-1-terminal-closure-and-workflow-correction-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_1415_aiscc-p2-1-terminal-closure-judgment-1.md
```

Task가 아래 historical artifact를 current canonical authority처럼 bulk-read할 필요는 없다.

다만 current canonical docs에 mandatory Browser rotation 문구의 provenance가 불명확하여 exact supersession wording을 작성할 수 없을 때만 다음 historical lineage를 좁게 조회할 수 있다.

```text
20260902_1621 ... fresh-chat / Browser-session handoff lineage
```

Historical artifact는 수정하지 마라.

# 1. initial workspace gate

Substantive mutation 전에:

```text
branch:
main

HEAD:
1fb9fd5e29e85481fa3c6ce78542de1fda6bf138

HEAD tree:
eaed171656a15440ea5444ba2d56ac939f625f56

index:
empty
```

이어야 한다.

이번 Command Center transport 이후 Git-visible worktree는 exact:

```text
.aiassistant/records/aiscc/cycles/20260908_1415_aiscc-p2-1-terminal-closure-and-workflow-correction-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_1415_aiscc-p2-1-terminal-closure-judgment-1.md
```

두 path만 새로 보여야 한다.

active Task는 ignored 상태여야 한다.

다음이면 STOP:

```text
HEAD_OR_TREE_MISMATCH
INDEX_NOT_EMPTY
TRANSPORTED_ARTIFACT_MISSING
UNEXPECTED_GIT_VISIBLE_DIRT
```

다른 dirt를 정리/restore/absorb하지 마라.

# 2. canonical workflow decisions

## 2.1 IDE fresh-session rule

Canonicalize:

```text
fresh IDE Executor chat is task-scoped, not universal.

Command Center decides whether a fresh IDE chat is required from an explicit authority/context boundary.

If required:
- the Browser response MUST visibly tell Human, before the Short Prompt:
  "이번 작업은 IDE Executor에서 새 채팅세션을 열고 시작해야 합니다."
- include a short reason.
- Human opens the fresh IDE chat.
- Short Prompt MUST NOT instruct the IDE Executor to create/open a chat.
```

Task/template representation should include an explicit field such as:

```text
fresh_ide_executor_chat:
REQUIRED / NOT_REQUIRED

fresh_ide_executor_chat_reason:
<reason or none>
```

Do not invent automatic freshness from every Task transition.

## 2.2 Browser session correction

Canonicalize:

```text
IDE fresh-session requirement
!=
Browser Command Center rotation

Cycle issuance
!=
Browser session termination

Handoff issuance
!=
mandatory after every substantive judgment
```

The generalized rule:

```text
every substantive Executor-bundle judgment
→ Cycle + Handoff
→ mandatory new Browser Command Center session
```

must be recorded as:

```text
SUPERSEDED / INVALID_GENERALIZATION
```

Browser Handoff/session migration is used only when an actual Browser-session boundary exists, including:

```text
- explicit Human request
- phase/context migration where continued session risks authority ambiguity
- material context exhaustion / unsafe continuation
- another explicit Browser-session boundary selected by Human/Command Center
```

Do not create a policy that Browser sessions must never rotate.

## 2.3 Command Center artifact-delivery contract

When Command Center issues any subset of:

```text
TASK
CYCLE
JUDGMENT
HANDOFF
```

the Browser turn provides one **flat ZIP package** containing only the issued artifacts.

Human responsibility:

```text
1. download ZIP
2. flat extract issued files into C:\Users\oracl\Downloads
3. if fresh IDE chat is required, open it
4. send the Short Prompt
```

The same Browser turn's Short Prompt must contain:

- exact issued artifact filenames
- exact expected SHA-256 per file
- source root
- exact canonical destination
- transport algorithm
- stop semantics
- substantive Task path after transport

Canonical destinations:

```text
TASK
→ C:\Users\oracl\IdeaProjects\ai-software-command-center\.aiassistant\tasks\active\

CYCLE
→ C:\Users\oracl\IdeaProjects\ai-software-command-center\.aiassistant\records\aiscc\cycles\

JUDGMENT
→ C:\Users\oracl\IdeaProjects\ai-software-command-center\.aiassistant\reports\aiscc\

HANDOFF
→ C:\Users\oracl\IdeaProjects\ai-software-command-center\.aiassistant\reports\aiscc\
```

Executor transport algorithm:

```text
for each issued artifact:

1. verify Downloads source exists
2. calculate source SHA-256
3. compare with Command Center expected SHA-256
4. inspect canonical destination

if destination absent:
    copy source → destination
    calculate destination SHA-256
    require source == destination

if destination present:
    calculate existing destination SHA-256

    if destination == source:
        do not overwrite

    if destination != source:
        overwrite destination from issued source
        recalculate destination SHA-256
        require source == destination

5. only after verified equality:
   remove the flat Downloads source artifact
```

ZIP itself is not removed by this transport rule.

Absent artifact types must not be fabricated.

Failure semantics:

```text
source missing
expected hash mismatch
destination path failure
copy/overwrite failure
post-copy hash mismatch
ambiguous transport result
→ STOP before substantive Task execution
```

Rationale must be retained:

```text
prevent Human manual placement mistakes from causing missing-artifact / wrong-path blockers
```

## 2.4 artifact overwrite boundary

The hash-aware overwrite above is authorized only for exact files explicitly issued by the current Command Center delivery package.

It is not generic permission to overwrite arbitrary canonical files from Downloads.

# 3. canonical files allowed to modify

Only:

```text
.aiassistant/records/command-center/README.md
.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md
.aiassistant/records/command-center/TASK_FILE_TEMPLATE.md
.aiassistant/records/command-center/SHORT_EXECUTOR_PROMPT_TEMPLATE.md
.aiassistant/records/command-center/JUDGMENT_RUBRIC.md
.aiassistant/records/command-center/CYCLE_RECORD_TEMPLATE.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

plus transported Cycle/Judgment and current Task lifecycle.

Do not modify:

```text
.aiassistant/rules/**
product/test source
historical tasks/done
historical cycles
historical reports/handoffs
project-source generated bundle
manifest
```

# 4. required document effects

## COMMAND_CENTER_WORKFLOW.md

Must state:

- standard cycle does not imply Browser rotation
- Handoff is conditional, not per-judgment mandatory
- IDE fresh-session decision and Human action
- delivery package flow before Executor Task execution

## TASK_FILE_TEMPLATE.md

Add durable fields/sections sufficient to encode:

- fresh IDE Executor chat requirement/reason
- Browser session action when relevant
- current delivery artifact prerequisites when needed

Do not require fields that are meaningless for simple Tasks.

## SHORT_EXECUTOR_PROMPT_TEMPLATE.md

Add a transport-first template that can enumerate only issued artifacts with exact hashes.

Separate Human-visible fresh IDE chat notice from the Short Prompt.

Explicitly state that Short Prompt must not tell Executor to create a chat.

## JUDGMENT_RUBRIC.md

Add judgment checks/output fields for:

- `fresh_ide_executor_chat_for_successor`
- `browser_session_action`
- `handoff_required`

Do not infer Browser rotation from `cycle_record_action=create`.

## CYCLE_RECORD_TEMPLATE.md

Add concise reusable fields for:

- IDE successor session decision
- Browser session decision
- Handoff requirement
- Command Center artifact transport result when applicable

## README.md

Summarize the corrected operational boundary.

## CURRENT_STATE_SUMMARY.md

Record:

```text
P2-1: ACCEPTED / CLOSED
P2-1 persistence commit: 1fb9fd5e29e85481fa3c6ce78542de1fda6bf138
P2-2: NOT_STARTED / ENTRY_READY
```

Also record that the immediate governance update is in progress/current before P2-2 execution.

## DECISION_REGISTER.md

Add durable decisions equivalent to:

```text
AISCC-COMMAND-CENTER-IDE-FRESH-SESSION-V1
AISCC-COMMAND-CENTER-BROWSER-SESSION-BOUNDARY-V1
AISCC-COMMAND-CENTER-ARTIFACT-DELIVERY-V1
```

For the Browser decision, explicitly record the prior generalized mandatory post-judgment rotation as superseded/invalid.

## NEXT_ACTIONS.md

After this Task completes, stable queue should become:

```text
P2-1:
ACCEPTED / CLOSED

P2-2:
NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE
```

Do not mark P2-2 started.

# 5. language / integrity

- Korean-first.
- exact identifiers/path/state remain original.
- UTF-8 no BOM preferred.
- preserve valid Markdown fences.
- no control-character corruption.
- run `git diff --check`.

# 6. evidence contract

## executor_required

### WORKSPACE_STATIC

Pass:

- exact base HEAD/tree/index
- exactly transported Cycle/Judgment pre-existing dirt
- only allowed canonical docs changed

### DOCUMENT_CONTRACT

Pass if all three Human decisions are represented without semantic distortion:

```text
IDE fresh session:
task-scoped + visible Human notice + Human opens it

Browser rotation:
independent / conditional / no per-judgment mandate

artifact delivery:
flat ZIP + Downloads + exact copy/hash/remove
```

### GIT_PERSISTENCE

Exact final allowlist:

- `.aiassistant/records/command-center/README.md`
- `.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md`
- `.aiassistant/records/command-center/TASK_FILE_TEMPLATE.md`
- `.aiassistant/records/command-center/SHORT_EXECUTOR_PROMPT_TEMPLATE.md`
- `.aiassistant/records/command-center/JUDGMENT_RUBRIC.md`
- `.aiassistant/records/command-center/CYCLE_RECORD_TEMPLATE.md`
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
- `.aiassistant/records/aiscc/cycles/20260908_1415_aiscc-p2-1-terminal-closure-and-workflow-correction-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1415_aiscc-p2-1-terminal-closure-judgment-1.md`
- `.aiassistant/tasks/done/20260908_1415_aiscc-command-center-workflow-session-and-delivery-contract-canonicalization-1.md`

Expected count:

```text
12
```

No other staged path.

### PUBLIC_PROVENANCE / COMMIT_VERIFICATION

Verify exact commit parent/message/path set/blob presence/worktree cleanliness.

## reuse_allowed

- `1316` P2-1 final persistence commit/evidence: `REUSED_ACCEPTED`
- P2-1 terminal judgment in transported `20260908_1415_aiscc-p2-1-terminal-closure-judgment-1.md`

## human_owned

```text
fresh IDE chat creation:
HUMAN_PROVIDED prerequisite before Executor receives this prompt

new browser/visual QA:
NOT_REQUIRED

Browser Project Source upload:
NOT_REQUIRED in this Task
```

## forbidden

- product/runtime implementation
- P2-2 execution
- Browser session migration
- Project Source upload
- Git push
- broad cleanup
- unrelated file edits

# 7. Task lifecycle and Git persistence

After document verification passes:

```text
.aiassistant/tasks/active/20260908_1415_aiscc-command-center-workflow-session-and-delivery-contract-canonicalization-1.md
→
.aiassistant/tasks/done/20260908_1415_aiscc-command-center-workflow-session-and-delivery-contract-canonicalization-1.md
```

Then final Git-visible/staged allowlist must be exact 12 paths listed in Section 6.

Authorized Git actions only after all gates PASS:

```text
git add -- <exact 12 literal paths>
git diff --cached --check
git diff --cached --name-status
git commit -m "docs(command-center): correct session and artifact delivery workflow"
```

Expected:

```text
parent:
1fb9fd5e29e85481fa3c6ce78542de1fda6bf138

parent count:
1

message:
docs(command-center): correct session and artifact delivery workflow

changed paths:
exact 12
```

Forbidden:

```text
git add -A
git add .
git clean
git reset
git restore
git checkout
git stash
git push
git pull
git fetch
git merge
git rebase
git cherry-pick
```

# 8. post-commit verification

Verify:

1. result commit/tree
2. exact parent `1fb9fd5e29e85481fa3c6ce78542de1fda6bf138`, parent count 1
3. exact commit message
4. exact 12 changed paths
5. all modified canonical docs present in commit
6. transported terminal Cycle/Judgment present in commit
7. current Task done present in commit
8. index empty
9. Git-visible worktree clean
10. push/network NOT_RUN

# 9. mandatory stop

STOP before further mutation on:

```text
MISSING_TRANSPORTED_ARTIFACT
HEAD_OR_TREE_MISMATCH
INDEX_NOT_EMPTY
UNEXPECTED_GIT_VISIBLE_DIRT
CANONICAL_AUTHORITY_CONFLICT
HUMAN_DECISION_SEMANTIC_AMBIGUITY
ALLOWED_PATH_SCOPE_COLLISION
GIT_STAGE_ALLOWLIST_MISMATCH
GIT_COMMIT_VERIFICATION_FAILED
```

Do not silently reinterpret the Human decision.

# 10. export bundle

Target:

```text
.aiassistant/reports/target/20260908_1415_aiscc-command-center-workflow-session-and-delivery-contract-canonicalization-1/
```

Required:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
WORKFLOW_CONTRACT_VERIFICATION.md
GIT_PERSISTENCE_VERIFICATION.md
```

Include changed 12 committed files preserving project-relative paths if commit succeeds.

# 11. final response ceiling

Success:

```text
Command Center workflow correction:
READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT

P2-1:
CLOSED / persisted

P2-2:
NOT_STARTED / ENTRY_READY
```

Do not start P2-2.
