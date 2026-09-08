# 작업지시서: P2-1E final acceptance runtime cleanup and Git persistence

## meta

- task_id: `20260908_0840_aiscc-p2-1e-final-acceptance-runtime-cleanup-and-git-persistence-1`
- created_at: `2026-09-08T08:40:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `QA_ONLY / FINAL_ACCEPTANCE_PERSISTENCE`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `NOT_APPLICABLE`
- primary_semantic_owner: `P2-1E accepted candidate final runtime cleanup / exact Git persistence / P2-1 closure-readiness evidence`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- accepted_parent_HEAD: `36bed286abf4df6e8cecea2d379896c36be5d58a`
- accepted_parent_tree: `221ee3e4b675bb3ca871ba38557c10ffadbf96fe`

## 현재 상태

Browser Command Center의 현재 authoritative judgment:

```text
P2-1E:
ACCEPTED

P2-1E source/runtime:
ACCEPTED

P2-1E Human QA:
HUMAN_PROVIDED / ACCEPTED

Operation 17:
HUMAN_PROVIDED / PASS

Operation 8:
HUMAN_PROVIDED / PASS

supported deterministic NONE fixture authority:
ESTABLISHED

P2-1:
ACTIVE / NOT_CLOSED

Git persistence:
NOT_COMPLETED

P2-2:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

이번 Task는 `P2-1E`의 acceptance를 재심사하거나 구현을 다시 하는 Task가 아니다.

이번 Task의 역할은:

```text
accepted P2-1E candidate + accepted governance provenance
→ exact workspace identity 확인
→ 남아 있는 P2-1E Human QA runtime을 exact identity로만 cleanup
→ exact allowlisted Git persistence
→ resulting commit/worktree proof 생성
→ P2-1 terminal closure readiness를 Browser Command Center가 별도 판단할 수 있게 evidence 제출
```

이번 Task 자체는 다음을 선언할 수 없다.

```text
P2-1 CLOSED
P2-2 STARTED
public release complete
```

## authority / predecessor

최신 Browser judgment authority:

```text
.aiassistant/records/aiscc/cycles/20260908_0329_aiscc-p2-1e-human-browser-evidence-complete-final-acceptance-persistence-entry-1.cycle.md

.aiassistant/reports/aiscc/20260908_0329_aiscc-browser-command-center-p2-1e-final-acceptance-persistence-entry-handoff-1.md
```

Accepted P2-1E implementation/runtime candidate authority:

```text
.aiassistant/tasks/done/20260907_2328_aiscc-p2-1e-authorized-postgresql-runtime-implementation-retry-1.md

.aiassistant/records/aiscc/cycles/20260908_0020_aiscc-p2-1e-implementation-runtime-candidate-accepted-human-qa-pending-1.cycle.md

.aiassistant/reports/aiscc/20260908_0020_aiscc-browser-command-center-p2-1e-candidate-accepted-human-qa-entry-handoff-1.md
```

P2-1D persisted parent authority:

```text
.aiassistant/records/aiscc/cycles/20260907_1805_aiscc-p2-1d-persistence-final-acceptance-p2-1e-entry-authorization-1.cycle.md

.aiassistant/reports/aiscc/20260907_1805_aiscc-browser-command-center-p2-1d-completion-p2-1e-entry-handoff-1.md
```

Authority precedence:

```text
local canonical repository
>
terminal-persisted accepted Cycle/rule/commit
>
latest Browser judgment Cycle
>
current Handoff
>
Browser Project Source mirror
>
chat memory
```

Browser Project Source mirror의 stale current-state prose를 최신 `0329` Cycle/Handoff보다 우선하지 마라.

---

# 1. 이번 턴 목표

1. mutation 전 exact Git/workspace preflight를 수행한다.
2. accepted P2-1E four-path candidate의 exact final SHA를 재검증한다.
3. inherited governance provenance가 exact expected 23-path set인지 확인한다.
4. 현재 Human QA용 runtime이 남아 있다면 exact identity를 확인한 뒤 Task가 명시한 runtime만 안전하게 종료/제거한다.
5. broad cleanup 없이 ignored temporary artifact와 Git-visible canonical/provenance를 분리한다.
6. 이번 Task lifecycle의 `tasks/done` 경로를 포함한 exact 28-path allowlist만 Git stage/commit한다.
7. resulting commit의 parent/tree/path/blob/worktree/index를 독립적으로 검증한다.
8. Browser Command Center가 `P2-1` terminal closure를 별도 판단할 수 있도록 persistence/cleanup evidence를 export한다.

# 2. 이번 턴 비목표

- P2-1E 구현 변경
- P2-1E source/contract Gate A-F 재감사
- Human Browser QA 재실행
- Operation 1-22 재실행
- 새 fixture 작성
- DB row ad-hoc fabrication
- backend/API/DTO/persistence/migration/dependency/config 변경
- P2-1 closure를 Executor가 직접 선언
- P2-2 시작
- P2-3/P2-4 시작
- Project Source mirror sync
- deployment/public release
- Git push
- ignored target/cache 전체 정리

---

# 3. 읽을 문서 — minimum authoritative context set

반드시 exact path로 직접 읽는다.

## canonical rules

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md
.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md
.aiassistant/records/command-center/JUDGMENT_RUBRIC.md
```

## current acceptance authority

```text
.aiassistant/records/aiscc/cycles/20260908_0329_aiscc-p2-1e-human-browser-evidence-complete-final-acceptance-persistence-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_0329_aiscc-browser-command-center-p2-1e-final-acceptance-persistence-entry-handoff-1.md
```

## accepted candidate / persistence lineage

```text
.aiassistant/records/aiscc/cycles/20260908_0020_aiscc-p2-1e-implementation-runtime-candidate-accepted-human-qa-pending-1.cycle.md
.aiassistant/reports/aiscc/20260908_0020_aiscc-browser-command-center-p2-1e-candidate-accepted-human-qa-entry-handoff-1.md
.aiassistant/tasks/done/20260907_2328_aiscc-p2-1e-authorized-postgresql-runtime-implementation-retry-1.md
.aiassistant/records/aiscc/cycles/20260907_1805_aiscc-p2-1d-persistence-final-acceptance-p2-1e-entry-authorization-1.cycle.md
```

## Human QA / evidence-gap provenance

```text
.aiassistant/tasks/done/20260908_0051_aiscc-p2-1e-human-integrated-browser-qa-operation-guide-1.md
.aiassistant/records/aiscc/cycles/20260908_0158_aiscc-p2-1e-human-browser-qa-partial-accepted-nextaction-none-fixture-gap-1.cycle.md
.aiassistant/tasks/done/20260908_0208_aiscc-p2-1e-nextaction-none-human-qa-evidence-completion-1.md
.aiassistant/records/aiscc/cycles/20260908_0222_aiscc-p2-1e-evidence-gap-closure-blocked-missing-canonical-qa-guide-1.cycle.md
.aiassistant/tasks/done/20260908_0227_aiscc-p2-1e-0051-human-qa-guide-canonical-artifact-restoration-1.md
.aiassistant/records/aiscc/cycles/20260908_0259_aiscc-p2-1e-0051-canonical-qa-guide-restoration-accepted-evidence-gap-retry-entry-1.cycle.md
.aiassistant/tasks/done/20260908_0303_aiscc-p2-1e-nextaction-none-human-qa-evidence-completion-retry-1.md
```

Unrelated rules/records/source/logs를 bulk-read하지 마라.

---

# 4. agent instruction transport / authority

- repository-root instruction entrypoint는 thin transport bootstrap이며 policy authority가 아니다.
- Project Rules UI 또는 automatic retrieval만으로 canonical body가 전달됐다고 가정하지 마라.
- Task File의 위 목록은 minimum authoritative context set이다.
- active Task, canonical rule, latest accepted Cycle/Handoff, current source가 충돌하면 Git action과 runtime destruction을 중단하고 conflict investigation으로 보고한다.
- Human-owned evidence는 이미 `0329` Cycle에서 admitted되었다. 이를 다시 실행하거나 Executor evidence로 재분류하지 마라.

---

# 5. PRE-MUTATION mandatory Git/workspace preflight

Git index/commit/runtime cleanup 전에 다음을 먼저 확인한다.

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

HEAD:
36bed286abf4df6e8cecea2d379896c36be5d58a

HEAD tree:
221ee3e4b675bb3ca871ba38557c10ffadbf96fe

index:
empty
```

위 HEAD가 아니면 STOP.

현재 Task File은 `.aiassistant/tasks/active/`에 있어 Git ignore되는 것이 정상이다.

## 5.1 exact accepted P2-1E product/test paths

Git-visible modified product/test path는 정확히 다음 4개여야 한다.

```text
src/aiscc/command_center/web.py
src/aiscc/api/routes/command_center_ui.py
tests/integration/command_center/test_web_ui.py
tests/unit/command_center/test_web_shell.py
```

Final SHA-256는 정확히 다음과 같아야 한다.

```text
src/aiscc/command_center/web.py
d58360e4df00c167225960ee9fef93e64cc4910adf173b20263c8449d58c5631

src/aiscc/api/routes/command_center_ui.py
10951dee88468bf95faae2c47b3cca649e37fc8adccc7586f47dd8729127bf37

tests/integration/command_center/test_web_ui.py
99bad1694845900870cd83a4e62303653ed7e2b52496fa12dfef766ce45e820d

tests/unit/command_center/test_web_shell.py
8c8ffffdd9546206a3d92d02dc09dcc5a388e7b34a97432b5f6b1685f298ebe5
```

하나라도 hash mismatch이면:

```text
STOP
reason = ACCEPTED_CANDIDATE_IDENTITY_MISMATCH
```

수정하거나 restore하지 마라.

## 5.2 exact inherited governance provenance — 23 paths

PRE-MUTATION Git-visible untracked governance set은 정확히 다음 23개여야 한다.

```text
.aiassistant/records/aiscc/cycles/20260907_1805_aiscc-p2-1d-persistence-final-acceptance-p2-1e-entry-authorization-1.cycle.md
.aiassistant/reports/aiscc/20260907_1805_aiscc-browser-command-center-p2-1d-completion-p2-1e-entry-handoff-1.md
.aiassistant/tasks/done/20260907_1814_aiscc-p2-1e-cycle-next-action-integrated-command-center-implementation-1.md
.aiassistant/records/aiscc/cycles/20260907_2241_aiscc-p2-1e-preflight-blocked-known-governance-dirt-1.cycle.md
.aiassistant/reports/aiscc/20260907_2241_aiscc-browser-command-center-p2-1e-preflight-blocked-retry-entry-handoff-1.md
.aiassistant/tasks/done/20260907_2252_aiscc-p2-1e-cycle-next-action-integrated-command-center-implementation-retry-1.md
.aiassistant/records/aiscc/cycles/20260907_2320_aiscc-p2-1e-runtime-prerequisite-blocked-after-source-audit-1.cycle.md
.aiassistant/reports/aiscc/20260907_2320_aiscc-browser-command-center-p2-1e-runtime-prerequisite-blocked-retry-entry-handoff-1.md
.aiassistant/tasks/done/20260907_2328_aiscc-p2-1e-authorized-postgresql-runtime-implementation-retry-1.md
.aiassistant/records/aiscc/cycles/20260908_0020_aiscc-p2-1e-implementation-runtime-candidate-accepted-human-qa-pending-1.cycle.md
.aiassistant/reports/aiscc/20260908_0020_aiscc-browser-command-center-p2-1e-candidate-accepted-human-qa-entry-handoff-1.md
.aiassistant/tasks/done/20260908_0051_aiscc-p2-1e-human-integrated-browser-qa-operation-guide-1.md
.aiassistant/records/aiscc/cycles/20260908_0158_aiscc-p2-1e-human-browser-qa-partial-accepted-nextaction-none-fixture-gap-1.cycle.md
.aiassistant/reports/aiscc/20260908_0158_aiscc-browser-command-center-p2-1e-human-qa-partial-evidence-completion-entry-handoff-1.md
.aiassistant/tasks/done/20260908_0208_aiscc-p2-1e-nextaction-none-human-qa-evidence-completion-1.md
.aiassistant/records/aiscc/cycles/20260908_0222_aiscc-p2-1e-evidence-gap-closure-blocked-missing-canonical-qa-guide-1.cycle.md
.aiassistant/reports/aiscc/20260908_0222_aiscc-browser-command-center-p2-1e-missing-qa-guide-restoration-entry-handoff-1.md
.aiassistant/tasks/done/20260908_0227_aiscc-p2-1e-0051-human-qa-guide-canonical-artifact-restoration-1.md
.aiassistant/records/aiscc/cycles/20260908_0259_aiscc-p2-1e-0051-canonical-qa-guide-restoration-accepted-evidence-gap-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_0259_aiscc-browser-command-center-p2-1e-0051-restoration-accepted-evidence-gap-retry-entry-handoff-1.md
.aiassistant/tasks/done/20260908_0303_aiscc-p2-1e-nextaction-none-human-qa-evidence-completion-retry-1.md
.aiassistant/records/aiscc/cycles/20260908_0329_aiscc-p2-1e-human-browser-evidence-complete-final-acceptance-persistence-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_0329_aiscc-browser-command-center-p2-1e-final-acceptance-persistence-entry-handoff-1.md
```

PRE-MUTATION expected Git-visible set:

```text
4 accepted product/test modified
+
23 inherited governance untracked
=
27 paths exact
```

다음은 27-path equality에 포함하지 않는다.

```text
.aiassistant/tasks/active/**
.aiassistant/reports/target/**
.aiassistant/project-sources/bundles/**
ignored cache/runtime artifacts
```

그러나 ignored path가 secret/private data 또는 active runtime conflict를 의미하는지 여부는 별도 security check로 확인한다.

## 5.3 exact preflight stop rule

다음 중 하나라도 발생하면 모든 Git mutation과 runtime destructive cleanup을 STOP한다.

```text
branch mismatch
HEAD mismatch
tree mismatch
index non-empty
product/test path extra or missing
product/test SHA mismatch
inherited governance path extra or missing
unexpected tracked/untracked product/test/config/migration
unexpected repository config dirt
```

허용하지 않는다.

```text
git clean
git reset
git restore
git checkout
git stash
broad recursive deletion
silent absorption of extra dirt
```

---

# 6. current Human QA runtime cleanup contract

`0329` Handoff가 마지막으로 기록한 Human QA runtime identity:

```text
PostgreSQL container:
aiscc-p2-1e-human-qa

database bind:
127.0.0.1:55439 -> 5432

AISCC server:
http://127.0.0.1:8765

Task Project:
op8-none-20260908-0303

accepted fixture authority:
tests/integration/memory/test_postgres_project_memory_next_action.py::add_recovery_fact
```

Operation 8 Human QA는 이미 PASS이며 이 runtime의 Browser preservation need는 종료되었다.

하지만 **이름/포트만 보고 blind kill/remove 하지 마라.**

## 6.1 container identity verification

`aiscc-p2-1e-human-qa`가 존재하면 최소 다음을 확인한다.

- exact container name
- image / PostgreSQL version이 P2-1E QA lineage와 일치하는가
- host bind가 `127.0.0.1:55439 -> 5432`인가
- 외부/public bind가 아닌가
- unrelated volume 또는 unrelated project label/identity가 붙지 않았는가

일치하면 이 Task는 다음을 명시적으로 허용한다.

```text
docker stop aiscc-p2-1e-human-qa
docker rm aiscc-p2-1e-human-qa
```

동등한 non-destructive stop/remove 명령은 허용한다.

다음은 금지한다.

```text
docker system prune
docker container prune
docker volume prune
docker rm on any other container
broad image deletion
```

container가 이미 absent이면:

```text
ALREADY_ABSENT / PASS
```

으로 보고하고 재생성하지 마라.

## 6.2 AISCC server identity verification

`127.0.0.1:8765` listener가 존재하면 listener PID와 process command line을 확인한다.

허용 cleanup 조건:

```text
loopback 127.0.0.1:8765
AND
process command identifies AISCC local server / repository runtime
AND
current P2-1E Human QA lineage와 모순되지 않음
```

조건이 맞을 때만 graceful stop을 수행한다.

포트가 다른 unrelated process에 의해 사용 중이면 절대 종료하지 마라.

그 경우:

```text
STOP
reason = RUNTIME_IDENTITY_CONFLICT
```

server가 이미 absent이면:

```text
ALREADY_ABSENT / PASS
```

으로 보고한다.

## 6.3 cleanup pass condition

cleanup 후 최소 다음을 확인한다.

```text
container aiscc-p2-1e-human-qa:
absent

127.0.0.1:55439 listener:
absent

127.0.0.1:8765 P2-1E QA listener:
absent

Task-owned DB tmpfs/container data:
removed with container or confirmed absent
```

다음 ignored artifacts는 이 Task에서 강제로 삭제하지 않는다.

```text
.aiassistant/reports/target/**
retained mypy cache
previous target bundles
```

cleanup scope를 넓히지 마라.

---

# 7. accepted source verification — no implementation change

Runtime cleanup 뒤에도 accepted four-path SHA가 Section 5.1과 동일한지 다시 확인한다.

이번 Task는 product/test source 내용을 수정하면 안 된다.

변경이 감지되면 STOP.

새 unit/integration/browser QA를 acceptance를 만들기 위해 실행하지 마라.

허용되는 narrow checks:

```text
SHA-256
Git status/diff
Git diff --check
Python/Markdown encoding/control-character validation of files being committed
commit object/blob verification
```

기존 accepted Executor/Human evidence를 재실행해 채우지 마라.

---

# 8. current Task lifecycle and final commit allowlist

Preflight와 runtime cleanup이 PASS한 뒤, report/export의 pre-commit 부분을 준비한다.

그 다음 이번 active Task File을 canonical done path로 이동한다.

```text
.aiassistant/tasks/active/20260908_0840_aiscc-p2-1e-final-acceptance-runtime-cleanup-and-git-persistence-1.md
→
.aiassistant/tasks/done/20260908_0840_aiscc-p2-1e-final-acceptance-runtime-cleanup-and-git-persistence-1.md
```

이 done Task는 이번 final persistence commit에 포함해야 하는 새 governance provenance다.

따라서 commit 직전 Git-visible exact allowlist는:

```text
4 accepted P2-1E product/test paths
+
23 inherited governance paths
+
1 current done Task path
=
28 paths exact
```

## 8.1 final exact 28-path allowlist

### product/test — 4

```text
src/aiscc/command_center/web.py
src/aiscc/api/routes/command_center_ui.py
tests/integration/command_center/test_web_ui.py
tests/unit/command_center/test_web_shell.py
```

### inherited governance — 23

Section 5.2의 exact 23 paths.

### current Task provenance — 1

```text
.aiassistant/tasks/done/20260908_0840_aiscc-p2-1e-final-acceptance-runtime-cleanup-and-git-persistence-1.md
```

이 28개 외에는 stage하지 마라.

---

# 9. Git persistence authorization

Section 5-8의 모든 gate가 PASS할 때만 다음 Git action을 허용한다.

```text
git add -- <exact 28-path allowlist only>
git diff --cached --check
git diff --cached --name-status
git commit -m "feat(command-center): complete P2-1E cycle and next-action integration"
```

`git add -A`, `git add .`, broad glob stage는 사용하지 마라.

금지:

```text
git push
git pull
git fetch
git merge
git rebase
git cherry-pick
git reset
git restore
git checkout
git stash
git clean
```

외부 network는 사용하지 마라.

## 9.1 commit acceptance shape

새 commit은:

```text
parent:
36bed286abf4df6e8cecea2d379896c36be5d58a

parent count:
1

merge commit:
No

message:
feat(command-center): complete P2-1E cycle and next-action integration

changed path set:
exact 28
```

이어야 한다.

---

# 10. mandatory post-commit verification

commit 후 반드시 다음을 검증한다.

## 10.1 commit object

- commit hash
- tree hash
- exact parent hash
- parent count = 1
- exact commit message

## 10.2 changed-path equality

다음 세 집합이 exact equal이어야 한다.

```text
Task final 28-path allowlist
==
git diff-tree / git show changed paths
==
exported committed-copy manifest paths
```

extra/missing = 0.

## 10.3 committed blob verification

4 product/test committed blobs의 content SHA-256가 Section 5.1 accepted hashes와 정확히 일치해야 한다.

23 inherited governance + current done Task 1개는 commit blob이 존재하며 path-preserving export copy와 byte-identical이어야 한다.

## 10.4 worktree/index

commit 후:

```text
index:
empty

Git-visible tracked/untracked worktree:
clean
```

ignored temporary target/cache path는 clean 판정에서 Git-visible dirt로 오인하지 마라.

그러나 new unexpected non-ignored path가 남으면 persistence verification FAIL이다.

## 10.5 runtime residue

post-commit에도 Section 6 cleanup 결과를 다시 확인한다.

```text
P2-1E QA container:
absent

P2-1E QA server listener:
absent

DB listener:
absent
```

---

# 11. evidence contract

## executor_required

### STATIC_SOURCE / HASH_IDENTITY

scope:
- accepted four-path final SHA identity

pass_condition:
- 4 / 4 exact

### WORKSPACE_GIT_PREFLIGHT

scope:
- branch / HEAD / tree / index / exact 27 pre-mutation visible set

pass_condition:
- exact equality; extra/missing 0

### RUNTIME_CLEANUP

scope:
- exact Human QA container/server/DB residue only

pass_condition:
- exact identity before destruction or already absent
- authorized residue absent afterward
- unrelated runtime untouched

### GIT_PERSISTENCE

scope:
- exact 28-path stage + single-parent commit

pass_condition:
- exact allowlist only
- commit succeeds
- no push

### PUBLIC_PROVENANCE / COMMIT_VERIFICATION

scope:
- commit parent/tree/message/path/blob/worktree mapping

pass_condition:
- all exact checks PASS

## reuse_allowed

```text
2252 Gate A-F:
REUSED_ACCEPTED

2328 source/static/unit/integration/PostgreSQL/HTTP/frontend evidence:
REUSED_ACCEPTED

P2-1E Human Browser QA including Operation 8 and 17:
HUMAN_PROVIDED / REUSED_ACCEPTED
```

Applicability condition:

```text
accepted four-path hashes unchanged
AND
no new product/test/config/migration mutation
```

## human_owned

```text
new Human verification:
NOT_REQUIRED in this Task
```

P2-1 terminal closure judgment 자체는 Browser Command Center/Human semantic owner가 후속 turn에서 판단한다.

## not_required

```text
UNIT_TEST rerun
INTEGRATION_TEST rerun
DATABASE_RUNTIME functional QA rerun
HTTP_RUNTIME functional QA rerun
BROWSER_RUNTIME rerun
responsive rerun
source/contract Gate A-F rerun
```

## forbidden

```text
P2-2/P2-3/P2-4
source implementation mutation
new fixture/migration/dependency/config
broad runtime cleanup
broad Git cleanup
Git push/network
Project Source sync
deployment
Executor declaring P2-1 CLOSED
```

## proof_non_substitution

```text
successful Git commit
!= P2-1 CLOSED

runtime cleanup
!= product acceptance

accepted predecessor tests
!= new changed-path proof if source hash changed

Executor report
!= Browser terminal judgment
```

---

# 12. mandatory stop conditions

다음이면 commit하지 말고 STOP한다.

```text
MISSING_REQUIRED_ARTIFACT
POLICY_CONFLICT_INVESTIGATION_REQUIRED
ACCEPTED_CANDIDATE_IDENTITY_MISMATCH
DIRTY_WORKSPACE_MIXED
INDEX_NOT_EMPTY
UNEXPECTED_GIT_VISIBLE_PATH
RUNTIME_IDENTITY_CONFLICT
SECURITY_BOUNDARY_UNCERTAIN
EVIDENCE_SCOPE_EXPANSION_REQUIRED
GIT_STAGE_ALLOWLIST_MISMATCH
GIT_COMMIT_VERIFICATION_FAILED
```

Named blocker 이후에는:

```text
blocker를 입증하는 최소 evidence
workspace/runtime inventory
report/export
안전한 종료
```

만 수행한다.

Blocker 이후 broad cleanup, speculative repair, source mutation, unrelated tests를 수행하지 마라.

---

# 13. export bundle 요구

Target:

```text
.aiassistant/reports/target/20260908_0840_aiscc-p2-1e-final-acceptance-runtime-cleanup-and-git-persistence-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
RUNTIME_CLEANUP_VERIFICATION.md
GIT_PERSISTENCE_VERIFICATION.md
```

그리고 final committed 28 paths를 project-relative path를 보존하여 export한다.

삭제된 repository file이 없으므로:

```text
REMOVED_FILES.md:
DO NOT CREATE
```

Manifest에는 최소:

- repository / branch
- parent HEAD/tree
- result commit/tree
- expected/actual payload count
- exact 28-path allowlist
- each committed path source SHA-256
- each exported copy SHA-256
- source/copy byte equality
- task identity
- runtime cleanup summary
- post-commit index/worktree summary

를 포함한다.

Private env/credential/database password/token은 export하지 마라.

---

# 14. 보고서 필수 항목

`EXECUTOR_REPORT.md`에는 최소 다음을 Korean-first로 기록한다.

1. 작업명 / work type / Task path
2. read canonical paths
3. preflight branch/HEAD/tree/index
4. pre-mutation expected 27 / actual / extra / missing
5. accepted four-path SHA 4/4 result
6. governance 23-path presence result
7. ignored temporary artifact 분류
8. runtime identity before cleanup
9. runtime cleanup action / already-absent result
10. unrelated runtime untouched 여부
11. current Task active→done lifecycle
12. final stage allowlist expected 28 / actual
13. `git diff --cached --check`
14. resulting commit hash/tree/parent/parent count/message
15. commit changed paths 28 exact equality
16. committed product/test SHA 4/4
17. exported committed-copy byte equality
18. post-commit index/worktree
19. forbidden-not-run
20. human evidence reuse and no re-run
21. unverified items
22. rollback/revert guide
23. preserved artifact exact paths
24. P2-1 closure-readiness recommendation

P2-1 closure-readiness recommendation은 다음 형식으로 제한한다.

```text
P2-1 terminal closure readiness:
READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT
```

또는 blocker가 있으면:

```text
NOT_READY / <exact reason>
```

Executor가 `P2-1 CLOSED`를 직접 선언하지 마라.

---

# 15. rollback / revert boundary

Commit이 성공하고 post-commit verification이 PASS한 뒤 잘못된 persistence가 후속 Browser에서 판정되더라도, 이 Task 안에서 자의적으로 reset/revert하지 마라.

Report에는:

- result commit hash
- parent hash
- exact changed paths

를 남긴다.

실제 rollback은 별도 Browser-authorized exact Task에서 수행한다.

---

# 16. preserved artifacts

이번 Task/cleanup 이후에도 최소 다음은 보존한다.

```text
.aiassistant/tasks/done/20260907_2328_aiscc-p2-1e-authorized-postgresql-runtime-implementation-retry-1.md
.aiassistant/tasks/done/20260908_0051_aiscc-p2-1e-human-integrated-browser-qa-operation-guide-1.md
.aiassistant/tasks/done/20260908_0208_aiscc-p2-1e-nextaction-none-human-qa-evidence-completion-1.md
.aiassistant/tasks/done/20260908_0227_aiscc-p2-1e-0051-human-qa-guide-canonical-artifact-restoration-1.md
.aiassistant/tasks/done/20260908_0303_aiscc-p2-1e-nextaction-none-human-qa-evidence-completion-retry-1.md
.aiassistant/tasks/done/20260908_0840_aiscc-p2-1e-final-acceptance-runtime-cleanup-and-git-persistence-1.md
.aiassistant/records/aiscc/cycles/20260908_0020_aiscc-p2-1e-implementation-runtime-candidate-accepted-human-qa-pending-1.cycle.md
.aiassistant/records/aiscc/cycles/20260908_0158_aiscc-p2-1e-human-browser-qa-partial-accepted-nextaction-none-fixture-gap-1.cycle.md
.aiassistant/records/aiscc/cycles/20260908_0222_aiscc-p2-1e-evidence-gap-closure-blocked-missing-canonical-qa-guide-1.cycle.md
.aiassistant/records/aiscc/cycles/20260908_0259_aiscc-p2-1e-0051-canonical-qa-guide-restoration-accepted-evidence-gap-retry-entry-1.cycle.md
.aiassistant/records/aiscc/cycles/20260908_0329_aiscc-p2-1e-human-browser-evidence-complete-final-acceptance-persistence-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_0329_aiscc-browser-command-center-p2-1e-final-acceptance-persistence-entry-handoff-1.md
```

그리고 Section 5.2의 나머지 governance lineage도 final commit에서 보존한다.

---

# 17. project context impact

architecture:
- `NONE`

orchestration_contract:
- `NONE`

security_sandbox:
- `NONE` unless runtime identity conflict appears

public_provenance:
- `TASK_AND_COMMIT_PERSISTENCE`

source_mirror_sync:
- `NOT_REQUIRED`

---

# 18. accept 기준

Executor turn의 success 조건:

```text
PRE-MUTATION:
branch/main exact
HEAD/tree exact
index empty
27-path exact visible set
4 candidate hashes exact

RUNTIME:
P2-1E QA runtime exact identity cleanup or already absent
unrelated runtime untouched

GIT:
current Task done lifecycle exact
28-path exact stage
cached diff check PASS
single-parent commit created
parent exact 36bed286...
changed paths exact 28
product/test committed hashes exact
export copies exact
post-commit index empty
post-commit Git-visible worktree clean
no push

JUDGMENT CEILING:
READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT
```

# 19. hold / blocked 기준

위 exact condition 중 하나라도 충족되지 않으면 해당 blocker로 중단한다.

특히 실제 workspace가 예상 27 paths와 다르면:

```text
STOP
```

하고 extra/missing을 exact path로 보고하라.

예상보다 많은 path를 final commit에 흡수하지 마라.

# 20. 최종 응답 형식

1. result: `completed` / `blocked`
2. target bundle path
3. result commit hash or `none`
4. changed/committed path count
5. runtime cleanup result
6. post-commit index/worktree
7. human verification: `REUSED_ACCEPTED / no rerun`
8. unverified items
9. preserved exact paths
10. P2-1 terminal closure readiness: `READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT` or exact blocker
