# 작업지시서: P2-1D Final Acceptance Git Persistence Retry

## meta

- task_id: `20260907_1727_aiscc-p2-1d-final-acceptance-git-persistence-retry-1`
- created_at: `2026-09-07T17:27:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `FINAL_ACCEPTANCE_GIT_PERSISTENCE_RETRY`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `NOT_APPLICABLE`
- primary_semantic_owner: `P2-1D accepted candidate terminal Git persistence`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- expected_pre_commit_HEAD: `08368eceac625c9a74b4347021ed65540cb08b3c`
- expected_pre_commit_tree: `c7c601677eb2a4ca2fa7b594465ebd16ed8da9f4`
- authorized_commit_count: `EXACTLY_ONE`
- authorized_commit_message: `feat(command-center): complete P2-1D evidence and judgment detail`
- push: `FORBIDDEN`
- deployment: `FORBIDDEN`
- source_mirror_sync: `NOT_REQUIRED`

---

# 1. 현재 authoritative state

이 Task는 P2-1D 구현 재작업이 아니다.

현재 Browser Command Center authority:

```text
P0:
CLOSED

P1:
ACCEPTED / CLOSED

P2:
STARTED / P2-1 ACTIVE

P2-1A:
ACCEPTED / PERSISTED

P2-1B:
ACCEPTED / PERSISTED

P2-1C:
HUMAN_PROVIDED / ACCEPTED / PERSISTED

P2-1D:
SOURCE_STATIC_ACCEPTED
RUNTIME_EVIDENCE_ACCEPTED
HUMAN_BROWSER_QA:
HUMAN_PROVIDED / PASS
OVERALL_IMPLEMENTATION:
ACCEPTED
PERSISTENCE:
BLOCKED_MISSING_ARTIFACT
NOT_PERSISTED

P2-1E:
NOT_STARTED

P2-2:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

직전 persistence turn의 blocker는 source/runtime/Human QA defect가 아니었다.

```text
classification:
BLOCKED_MISSING_ARTIFACT

reject_cause:
MISSING_REQUIRED_HUMAN_QA_GUIDE

source rework:
NOT_REQUIRED

Human Browser QA repeat:
NOT_REQUIRED

runtime rebuild:
NOT_REQUIRED

next work:
PERSISTENCE RETRY ONLY
```

이 Task가 성공해도 Executor가 선언할 수 있는 최고 상태는:

```text
P2-1D:
GIT_PERSISTED /
COMMAND_CENTER_COMMIT_REVIEW_REQUIRED
```

이다.

Executor는 `ACCEPTED / PERSISTED`, `P2-1E ENTRY_AUTHORIZED`, `P2-1 CLOSED`를 선언하지 않는다.

---

# 2. 이번 턴 목표

1. 직전 persistence blocker였던 exact `1606 Human QA guide`를 canonical `tasks/done`으로 byte-preserving transport한다.
2. exact `1555 Handoff`를 canonical `reports/aiscc`로 transport/canonicalize한다.
3. 직전 Browser terminal provenance인 exact `1712 Cycle + Handoff`를 canonical 위치로 transport한다.
4. 현재 4개 governance-location residue를 정확히 읽고 분류/정리한다.
5. P2-1D accepted product/test candidate 3개와 protected route byte identity를 재확인한다.
6. transport/provenance preflight가 모두 PASS한 뒤에만 retained exact runtime을 좁게 cleanup한다.
7. known Python cache residue를 exact-list 방식으로만 cleanup한다.
8. reconciliation 이후 current inventory에서 최종 staging allowlist를 재구축한다.
9. exact allowlist만 stage하고 `git diff --cached --check`를 통과시킨다.
10. 정확히 하나의 persistence commit을 만든다.
11. commit/tree/parent/message/path/blob과 post-commit index/worktree evidence를 export한다.

---

# 3. 비목표

이번 턴에서 하지 않는다.

- P2-1D product source 또는 test source 수정
- 새로운 implementation
- source/static/runtime evidence 재수집
- Human Browser QA 반복
- Browser automation/visual QA
- PostgreSQL runtime 재구축
- 새 Docker container 생성
- 새 DB schema/migration
- broad test suite 재실행
- package install/update
- external network
- credential 사용
- Git push
- PR
- deployment
- Project Source mirror sync
- P2-1E 시작
- P2-2 시작
- P2-1 terminal acceptance 선언

---

# 4. 절대 금지

다음 Git 명령/행위는 금지한다.

```text
git clean
git restore
git checkout
git reset
git stash
git rebase
git merge
git commit --amend
git add .
git add -A
git add --all
```

또한 금지:

- unrelated dirty file 삭제/수정
- glob 기반 broad cleanup
- `__pycache__` 전체 디렉터리 재귀삭제를 inventory 검증 없이 수행
- 모든 Python process 종료
- 모든 Docker container 종료/삭제
- 다른 QA 문서를 `1606 Human QA guide` 대신 사용
- missing provenance를 Agent가 새로 작성하여 대체
- wrong-location governance file을 읽지 않고 삭제
- hash mismatch를 newline/encoding 차이로 임의 정규화
- source/test byte mismatch를 수정해서 맞추기
- commit author identity를 global 설정으로 새로 구성
- blocker 발생 후 persistence를 계속 진행

---

# 5. minimum authoritative context set

작업 전에 exact path를 직접 읽는다.

## canonical rules

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md
```

## predecessor/current P2-1D provenance

```text
.aiassistant/records/aiscc/cycles/20260904_0150_aiscc-p2-1d-source-static-partial-acceptance-runtime-evidence-expansion-required-1.cycle.md

.aiassistant/reports/aiscc/20260904_0152_aiscc-browser-command-center-p2-1d-runtime-evidence-completion-entry-handoff-1.md

.aiassistant/records/aiscc/cycles/20260907_1555_aiscc-p2-1d-runtime-evidence-acceptance-human-browser-qa-entry-authorization-1.cycle.md

.aiassistant/records/aiscc/cycles/20260907_1631_aiscc-p2-1d-human-browser-qa-final-acceptance-persistence-entry-1.cycle.md

.aiassistant/tasks/done/20260907_1631_aiscc-p2-1d-final-acceptance-runtime-cleanup-and-git-persistence-1.md
```

Transport 후 반드시 추가로 읽는다.

```text
.aiassistant/tasks/done/20260907_1606_aiscc-p2-1d-human-browser-qa-operation-guide-2.md

.aiassistant/reports/aiscc/20260907_1555_aiscc-browser-command-center-p2-1d-runtime-accepted-human-browser-qa-entry-handoff-1.md

.aiassistant/records/aiscc/cycles/20260907_1712_aiscc-p2-1d-persistence-blocked-missing-human-qa-guide-1.cycle.md

.aiassistant/reports/aiscc/20260907_1712_aiscc-browser-command-center-p2-1d-persistence-blocked-retry-entry-handoff-1.md
```

현재 active Task와 위 canonical sources/current source가 충돌하면 mutation을 중단하고 conflict를 보고한다.

Unrelated rules/records/source/logs를 bulk-read하지 않는다.

---

# 6. 시작 Git preflight

어떤 transport/delete/runtime cleanup/staging보다 먼저 확인한다.

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

HEAD:
08368eceac625c9a74b4347021ed65540cb08b3c

tree:
c7c601677eb2a4ca2fa7b594465ebd16ed8da9f4

index:
empty
```

필수:

- `git status --porcelain=v1` 전체 path inventory를 파일로 보존한다.
- status count와 category count를 계산한다.
- product/test/config/migration의 예상 외 dirty path를 따로 분리한다.
- 현재 Task 시작으로 생긴 ignored `tasks/active`는 Git-visible inventory와 혼동하지 않는다.

아래 중 하나면 즉시 STOP:

```text
branch != main
HEAD != 08368eceac625c9a74b4347021ed65540cb08b3c
HEAD tree != c7c601677eb2a4ca2fa7b594465ebd16ed8da9f4
index not empty
unexpected product/config/migration path exists
accepted candidate path identity already conflicts
```

classification:

```text
DIRTY_WORKSPACE_MIXED
or
GOVERNANCE_PROVENANCE_CONFLICT
```

정확한 observed inventory를 report/export한 뒤 종료한다.

---

# 7. Browser artifact transport gate

이 section은 모든 runtime/cache cleanup보다 선행한다.

Browser/Downloads transport는 byte-preserving copy만 허용한다.

브라우저 중복 다운로드 suffix는 아래처럼 허용한다.

```text
<stem>.md
<stem>(1).md
<stem> (1).md
<stem>(2).md
...
```

그러나 선택한 source는 반드시 expected bytes + SHA-256을 동시에 만족해야 한다.

## 7.1 exact 1606 Human QA guide — 직전 blocker

Canonical destination:

```text
.aiassistant/tasks/done/20260907_1606_aiscc-p2-1d-human-browser-qa-operation-guide-2.md
```

Required source identity:

```text
filename:
20260907_1606_aiscc-p2-1d-human-browser-qa-operation-guide-2.md

bytes:
13096

SHA-256:
a737dcdd073d7113f10d55d4878c284d9855675a0f7c8d2a77cde484feac315e
```

순서:

1. canonical destination이 이미 있으면 bytes/hash를 검증한다.
2. 없으면 Human Downloads에서 exact filename 및 같은 stem numeric suffix 후보만 찾는다.
3. 모든 후보의 bytes/hash를 계산한다.
4. expected identity와 정확히 하나 이상 match할 때만 canonical destination으로 byte-preserving copy한다.
5. copy 후 destination bytes/hash를 다시 검증한다.

없거나 mismatch면:

```text
STOP
BLOCKED_MISSING_ARTIFACT
MISSING_REQUIRED_HUMAN_QA_GUIDE
```

다른 QA 문서 substitute 금지.

## 7.2 exact 1555 Handoff

Canonical destination:

```text
.aiassistant/reports/aiscc/20260907_1555_aiscc-browser-command-center-p2-1d-runtime-accepted-human-browser-qa-entry-handoff-1.md
```

Expected identity:

```text
bytes:
9768

SHA-256:
16e3861fdb722370263cb7ee13f07f2959a6231b1de6b458437f07d0fe7ffdb5
```

현재 known wrong-location source:

```text
.aiassistant/records/aiscc/cycles/20260907_1555_aiscc-browser-command-center-p2-1d-runtime-accepted-human-browser-qa-entry-handoff-1.md
```

허용 source 우선순위:

1. canonical destination이 이미 exact면 사용;
2. wrong-location file이 exact expected identity면 canonical destination으로 byte-preserving copy;
3. 위 둘이 불가능하면 Human Downloads exact/suffix source 중 expected identity match를 사용.

canonical destination 검증 완료 전 wrong-location source를 삭제하지 않는다.

## 7.3 exact 1712 terminal blocked Cycle

Canonical destination:

```text
.aiassistant/records/aiscc/cycles/20260907_1712_aiscc-p2-1d-persistence-blocked-missing-human-qa-guide-1.cycle.md
```

Browser-transport identity:

```text
bytes:
10141

SHA-256:
1700efc343533b7448fe10ce8f583633111d35715f986381312fb1038641fd1d
```

Human Downloads에서 exact filename 또는 same-stem numeric suffix를 허용한다.

Canonical destination이 이미 존재하면 exact identity를 검증한다.

missing/mismatch면 새 Cycle을 생성하여 대체하지 말고 STOP한다.

## 7.4 exact 1712 retry-entry Handoff

Canonical destination:

```text
.aiassistant/reports/aiscc/20260907_1712_aiscc-browser-command-center-p2-1d-persistence-blocked-retry-entry-handoff-1.md
```

Browser-transport identity:

```text
bytes:
11301

SHA-256:
3cf877aa33ccb4cc06e41cd5c0e07b3492a6471188eb593c0641bda5bc7c6b76
```

Human Downloads에서 exact filename 또는 same-stem numeric suffix를 허용한다.

Canonical destination이 이미 존재하면 exact identity를 검증한다.

missing/mismatch면 새 Handoff를 생성하여 대체하지 말고 STOP한다.

---

# 8. four governance-location residue reconciliation

직전 blocked persistence inventory의 outside-allowlist 4개는 다음이다.

```text
1.
.aiassistant/records/aiscc/cycles/20260904_0152_aiscc-browser-command-center-p2-1d-runtime-evidence-completion-entry-handoff-1.md

2.
.aiassistant/records/aiscc/cycles/20260907_1521_aiscc-browser-command-center-p2-1d-runtime-evidence-retry-entry-handoff-1.md

3.
.aiassistant/records/aiscc/cycles/20260907_1521_aiscc-p2-1d-runtime-evidence-completion-blocked-missing-browser-provenance-1.cycle.md

4.
.aiassistant/records/aiscc/cycles/20260907_1555_aiscc-browser-command-center-p2-1d-runtime-accepted-human-browser-qa-entry-handoff-1.md
```

각 파일은 먼저 full body를 읽고 role, meta, cross-reference, canonical owner를 기록한다.

## 8.1 0152 wrong-location Handoff

Canonical owner:

```text
.aiassistant/reports/aiscc/20260904_0152_aiscc-browser-command-center-p2-1d-runtime-evidence-completion-entry-handoff-1.md
```

알려진 상태:

```text
canonical report:
already exists
```

필수:

1. wrong-location copy와 canonical report bytes/SHA-256을 비교한다.
2. exact equal이면 wrong-location file만 삭제하도록 허용한다.
3. 다르면 삭제/overwrite 금지.

Conflict:

```text
STOP / GOVERNANCE_PROVENANCE_CONFLICT
```

## 8.2 1555 wrong-location Handoff

Expected identity:

```text
9768 bytes
16e3861fdb722370263cb7ee13f07f2959a6231b1de6b458437f07d0fe7ffdb5
```

Section 7.2의 canonical transport가 PASS한 뒤:

- canonical == wrong-location exact identity인지 재검증;
- exact equal일 때만 wrong-location file을 삭제한다;
- mismatch면 STOP.

## 8.3 1521 Handoff + Cycle

이 두 파일은 disposition을 추정하지 않는다.

```text
.aiassistant/records/aiscc/cycles/20260907_1521_aiscc-browser-command-center-p2-1d-runtime-evidence-retry-entry-handoff-1.md

.aiassistant/records/aiscc/cycles/20260907_1521_aiscc-p2-1d-runtime-evidence-completion-blocked-missing-browser-provenance-1.cycle.md
```

먼저 둘 다 읽고 다음을 분류한다.

```text
A. genuine blocked-turn Browser provenance
B. mislocated duplicate/transport residue
C. conflict/ambiguous
```

분류 기준:

- document heading/meta가 실제 `Cycle Record`인지 `Browser Command Center Handoff`인지;
- `cycle_id` / `handoff_id`, created_at, predecessor/next action이 서로 일관되는지;
- 다른 accepted Cycle/Handoff가 이 artifact를 historical provenance로 참조하는지;
- 동일 canonical destination이 존재한다면 byte identity가 같은지;
- filename role과 canonical directory owner가 일치하는지.

처리:

```text
genuine Cycle
→ cycles 위치에 유지

genuine Handoff
→ reports/aiscc canonical owner로 byte-preserving canonicalize
→ canonical identity 검증 후 wrong-location duplicate만 삭제

duplicate wrong-location file
→ exact canonical identity 확인 후 해당 duplicate만 삭제

conflict / ambiguous
→ STOP / GOVERNANCE_PROVENANCE_CONFLICT
```

어떤 경우에도 읽지 않고 stage/delete하지 않는다.

`GOVERNANCE_RECONCILIATION.md`에 두 파일 각각의 classification, 근거, source/destination hash, 최종 disposition을 기록한다.

---

# 9. accepted candidate byte gate

어떤 source/test byte도 수정하지 않는다.

필수 exact identities:

```text
src/aiscc/command_center/web.py
0e41ffb18256628a3c76150feeb6fc5c6b4d311d566b1e4c5b8d50987b308706

tests/integration/command_center/test_web_ui.py
2913359e913d7974d9165b0b013c7617438e1accf999af3c25bb876bd974821f

tests/unit/command_center/test_web_shell.py
29dfddb01aabfce7b5746cc762575271d2b16ad1c585d3b93e1d6ece1c575fa1
```

Sorted path/hash aggregate serialization:

```text
<case-sensitive repository-relative path>\t<lowercase_sha256>\n
```

Required aggregate:

```text
e051014a7deb3a12d14540264ee6c26ec389011d6cda18c098d7fcee238667ad
```

Protected unchanged route:

```text
src/aiscc/api/routes/command_center_ui.py
82d73e29ed5c185948ba82a5fc79083cafdb77b36b3f30760f570c295af01fd2
```

하나라도 mismatch면:

```text
STOP
ACCEPTED_CANDIDATE_IDENTITY_CONFLICT
```

수정하여 expected hash에 맞추지 않는다.

Accepted source/static/runtime/Human QA evidence는 위 exact-byte identity가 유지될 때만 재사용한다.

새 test/runtime/browser QA를 실행하여 mismatch를 대체하지 않는다.

---

# 10. retained runtime narrow cleanup

Section 6~9가 모두 PASS한 뒤에만 수행한다.

직전 blocked turn이 관찰한 retained runtime:

```text
AISCC server:
127.0.0.1:8765

listener PID:
33096

launcher PID:
60228

expected command:
python -m aiscc serve --host 127.0.0.1 --port 8765

PostgreSQL container name:
aiscc-p2-1d-runtime-evidence

container ID prefix:
b6ca38ceb044
```

## server

- 현재 `127.0.0.1:8765` listener를 확인한다.
- PID가 존재하면 command line이 exact AISCC serve process인지 확인한다.
- exact retained runtime과 일치할 때만 그 process/launcher를 좁게 종료한다.
- 다른 process가 해당 PID를 재사용했거나 command가 다르면 종료하지 말고 기록한다.
- 모든 Python process를 kill하지 않는다.
- 이미 종료되어 있으면 `ALREADY_STOPPED`로 기록한다.

## PostgreSQL container

- exact name `aiscc-p2-1d-runtime-evidence`만 조회한다.
- 존재하고 expected lineage가 맞으면 그 container만 stop/remove한다.
- 다른 container를 건드리지 않는다.
- 이미 없으면 `ALREADY_ABSENT`로 기록한다.

## shell env

Task-local shell/process 환경에서 runtime proof를 위해 사용한 `AISCC_TEST_DATABASE_URL`이 존재하면 현재 Task shell 범위에서만 제거한다.

사용자/시스템 persistent environment 설정을 수정하지 않는다.

Cleanup 후:

```text
127.0.0.1:8765:
no retained AISCC listener

aiscc-p2-1d-runtime-evidence:
absent
```

를 확인한다.

Runtime이 자연 소멸한 것은 source defect가 아니다.

---

# 11. known Python cache exact-list cleanup

직전 blocked Executor가 분류한 cache count:

```text
133 known Python cache paths
```

금지:

```text
git clean
broad recursive repository cleanup
unverified directory-level deletion
```

절차:

1. preflight `git status --porcelain=v1`에서 Python cache 후보를 exact path list로 추출한다.
2. 가능하면 직전 ignored target의 `WORKSPACE_INVENTORY.md`에 기록된 exact cache list와 비교한다.
3. current candidate는 다음 의미만 허용한다:
   - Python runtime-generated `__pycache__` / `.pyc`
   - product/governance source가 아님
   - 모두 Git-untracked
4. known lineage가 그대로라면 expected count `133`과 exact path set을 확인한다.
5. exact list의 파일만 하나씩 삭제한다.
6. 삭제 후 각 path가 absent인지 검증한다.

다음이면 broad cleanup하지 말고 STOP:

```text
cache count unexpected
tracked file included
non-cache path included
path classification ambiguous
```

classification:

```text
DIRTY_WORKSPACE_MIXED
```

새 Python 실행 때문에 cache를 다시 대량 생성하지 않도록 cleanup 이후 Python source execution을 최소화한다.

---

# 12. final staging allowlist rebuild

이 Task는 직전 `1631`의 staging 목록을 그대로 숫자만 믿지 않는다.

먼저 다음을 합쳐 **current exact path inventory**를 만든다.

```text
A.
직전 1631 Task가 persistence 대상으로 허용했던 existing governance set

B.
직전 blocked turn에서 tasks/active → tasks/done으로 이동한
.aiassistant/tasks/done/20260907_1631_aiscc-p2-1d-final-acceptance-runtime-cleanup-and-git-persistence-1.md

C.
이번에 transport된 canonical:
1606 Human QA guide
1555 Handoff
1712 blocked Cycle
1712 retry-entry Handoff

D.
1521 reconciliation 결과 유지/추가되는 genuine canonical provenance

E.
accepted product/test candidate 3 paths

F.
이번 current Task의 done path
.aiassistant/tasks/done/20260907_1727_aiscc-p2-1d-final-acceptance-git-persistence-retry-1.md

G.
reconciliation 결과 tracked deletion이 실제로 존재할 경우 그 exact deletion path
```

중요:

- 직전 `14 allowlisted existing governance` count는 historical preflight reference다.
- current final allowlist는 실제 reconciliation 결과와 newly transported provenance를 반영하여 exact path list로 다시 만든다.
- directory/glob allowlist를 사용하지 않는다.
- path마다 category를 기록한다:
  - `PRODUCT_TEST_ACCEPTED`
  - `GOVERNANCE_EXISTING`
  - `GOVERNANCE_TRANSPORTED`
  - `GOVERNANCE_CANONICALIZED`
  - `GOVERNANCE_DELETION`
  - `CURRENT_TASK_DONE`

`STAGING_ALLOWLIST_FINAL.md`에 exact ordered path list를 기록한다.

staging 전 다음을 증명한다.

```text
Git index:
empty

unexpected product/config/migration:
0

remaining Python cache:
0

unclassified governance residue:
0

accepted candidate hashes:
exact PASS

protected route:
exact PASS
```

unrelated dirty path가 남아 있어도 historical/accepted allowlist로 정확히 분류되지 않으면 stage하지 말고 STOP한다.

---

# 13. Task lifecycle before staging

Pre-commit prerequisite, transport, reconciliation, candidate gate, runtime/cache cleanup, final allowlist 작성까지 모두 PASS한 후:

```text
.aiassistant/tasks/active/20260907_1727_aiscc-p2-1d-final-acceptance-git-persistence-retry-1.md
```

을

```text
.aiassistant/tasks/done/20260907_1727_aiscc-p2-1d-final-acceptance-git-persistence-retry-1.md
```

으로 이동한다.

done path의 bytes/SHA-256을 기록하고 final staging allowlist에 포함한다.

blocker가 이 단계 이전에 발생하면 report/export가 제출 준비 완료된 경우에만 Task를 done으로 이동한다. blocker 이후 commit을 시도하지 않는다.

---

# 14. exact staging

허용된 final exact path만 개별 stage한다.

금지:

```text
git add .
git add -A
git add --all
directory-wide add
```

tracked deletion도 exact path 단위로 stage한다.

staging 직후 반드시:

```text
git diff --cached --name-status
git diff --cached --check
git status --porcelain=v1
```

를 수집한다.

Acceptance:

```text
cached path set
==
STAGING_ALLOWLIST_FINAL의 실제 Git-diff 대상 path set

outside allowlist staged:
0

git diff --cached --check:
PASS
```

stage된 path 하나라도 final allowlist 밖이면:

```text
STOP
DIRTY_WORKSPACE_MIXED
```

이미 staging mutation이 발생한 뒤 conflict를 발견한 경우 금지된 broad reset으로 임의 복구하지 않는다.
현재 index 상태를 그대로 evidence로 남기고 Command Center review로 반환한다.

---

# 15. one persistence commit

Section 14가 PASS일 때만 정확히 하나의 commit을 허용한다.

Required:

```text
parent:
08368eceac625c9a74b4347021ed65540cb08b3c

merge parent:
none

message:
feat(command-center): complete P2-1D evidence and judgment detail

commit count:
exactly one
```

Git author identity가 현재 repository/local environment에 유효하게 이미 구성되어 있지 않아 commit이 불가능하면 global config를 만들지 말고:

```text
STOP
GIT_AUTHOR_IDENTITY_REQUIRED
```

로 보고한다.

amend/rebase/merge 금지.

push 금지.

---

# 16. post-commit proof

commit 후 다음을 exact하게 수집한다.

```text
branch
HEAD
commit parent
commit tree
commit message
merge parent count
commit changed path list
per-path blob/object identity
index status
worktree status
```

필수:

```text
branch == main
HEAD != 08368ece...   # new commit
new commit parent == 08368eceac625c9a74b4347021ed65540cb08b3c
merge parent count == 0
message == feat(command-center): complete P2-1D evidence and judgment detail
index == empty
```

commit tree에서 accepted P2-1D product/test bytes를 다시 추출/검증한다.

```text
src/aiscc/command_center/web.py
0e41ffb18256628a3c76150feeb6fc5c6b4d311d566b1e4c5b8d50987b308706

tests/integration/command_center/test_web_ui.py
2913359e913d7974d9165b0b013c7617438e1accf999af3c25bb876bd974821f

tests/unit/command_center/test_web_shell.py
29dfddb01aabfce7b5746cc762575271d2b16ad1c585d3b93e1d6ece1c575fa1
```

protected route tree blob/content도 다음 identity 유지:

```text
src/aiscc/api/routes/command_center_ui.py
82d73e29ed5c185948ba82a5fc79083cafdb77b36b3f30760f570c295af01fd2
```

canonical Browser provenance도 commit tree에서 존재와 blob identity를 기록한다.

최종 worktree에 unrelated pre-existing path가 남는다면 자동 cleanup하지 않는다.
정확한 leftover를 보고한다.

---

# 17. evidence contract

## executor_required

### GIT_PREFLIGHT

scope:

```text
branch / HEAD / tree / index / complete Git-visible inventory
```

pass:

```text
expected accepted HEAD/tree
empty index
no unexpected product/config/migration collision
```

### PROVENANCE_TRANSPORT

scope:

```text
1606 guide
1555 Handoff
1712 Cycle
1712 Handoff
```

pass:

```text
exact expected bytes + SHA-256
canonical destination verified
```

### GOVERNANCE_RECONCILIATION

scope:

```text
4 exact wrong/outside-location governance paths
```

pass:

```text
each classified
no guessed deletion
no unresolved conflict
```

### ACCEPTED_CANDIDATE_IDENTITY

scope:

```text
3 accepted product/test paths + protected route
```

pass:

```text
all exact SHA-256
aggregate exact
```

### RUNTIME_CLEANUP

scope:

```text
retained 8765 AISCC process
exact PostgreSQL container
Task-local env
```

pass:

```text
exact retained resource stopped/removed or already absent
no unrelated resource touched
```

### CACHE_CLEANUP

scope:

```text
known 133 Python cache lineage
```

pass:

```text
exact-list cleanup only
no ambiguous/non-cache deletion
```

### GIT_PERSISTENCE

scope:

```text
final exact staging allowlist
one commit
commit object proof
```

pass:

```text
outside staged 0
diff --cached --check PASS
one exact-parent non-merge commit
post-commit proof complete
```

## reuse_allowed

다음 predecessor evidence는 accepted candidate bytes가 exact할 때만 재사용한다.

```text
P2-1D source/static acceptance
P2-1D PostgreSQL-backed runtime acceptance
P2-1D Human Browser QA HUMAN_PROVIDED / PASS
```

새 unit/integration/runtime/browser proof로 대체하지 않는다.

## human_owned

```text
final Browser Command Center commit review
P2-1D ACCEPTED / PERSISTED terminal judgment
P2-1E entry authorization
Git push
deployment
Project Source mirror upload
competition/public release
```

## not_required

```text
new browser QA
new DB runtime
new HTTP runtime
new unit/integration suite
source mirror sync
P2-1E implementation
P2-2 implementation
```

## forbidden

```text
source/test mutation
proof type substitution
Agent-minted Human acceptance
broad Git cleanup
push/deploy
external credential/network action
```

---

# 18. proof non-substitution

```text
existing Human QA result
!=
generated QA guide

accepted source/static tests
!=
new runtime proof requirement

Executor commit success
!=
Browser Command Center terminal acceptance

tasks/done
!=
accepted task

commit created
!=
P2-1D ACCEPTED / PERSISTED

Agent claim
!=
admitted evidence
```

---

# 19. mandatory stop

다음 중 하나면 이후 runtime cleanup/staging/commit을 진행하지 않는다.

```text
expected HEAD/tree/index mismatch
missing 1606 QA guide
1606 hash mismatch
1555 Handoff hash mismatch
1712 Cycle/Handoff missing or hash mismatch
governance provenance conflict
1521 disposition ambiguous
accepted candidate hash mismatch
protected route hash mismatch
unexpected product/config/migration dirt
cache classification mismatch
unsafe runtime identity
staging set outside final exact allowlist
git diff --cached --check fail
Git author identity requires unauthorized configuration
```

named blocker 이후에는:

- blocker 입증 최소 evidence
- complete current workspace inventory
- report/export
- 안전한 종료

만 수행한다.

새 evidence scope를 열지 않는다.

---

# 20. export bundle

Target:

```text
.aiassistant/reports/target/20260907_1727_aiscc-p2-1d-final-acceptance-git-persistence-retry-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_INVENTORY.md
PROVENANCE_TRANSPORT_EVIDENCE.md
GOVERNANCE_RECONCILIATION.md
RUNTIME_CLEANUP_EVIDENCE.md
STAGING_ALLOWLIST_FINAL.md
GIT_OBJECT_EVIDENCE.md
```

삭제가 실제로 있었으면:

```text
REMOVED_FILES.md
```

를 추가한다.

Export에는 secret/private material을 넣지 않는다.

`TASK.md`는 executed Task done file과 byte-identical이어야 한다.

Manifest에는 각 payload의:

```text
relative path
bytes
SHA-256
```

을 기록한다.

---

# 21. EXECUTOR_REPORT 필수 항목

- task/work type/task path
- read canonical paths
- branch/HEAD/tree/index preflight
- initial/final workspace counts and categorized exact paths
- Browser artifact candidate locations and exact byte/hash verification
- 1606 guide transport result
- 1555 Handoff canonicalization result
- 1712 Cycle/Handoff transport result
- four governance residue classification/disposition
- accepted candidate 3-path hash + aggregate
- protected route hash
- retained runtime before/after
- PostgreSQL container before/after
- Python cache exact-list count before/after
- source/test mutation: `NONE`
- Human QA repeat: `NOT_REQUIRED`
- staging allowlist exact path list
- cached name-status
- `git diff --cached --check`
- commit hash/tree/parent/message/path/blob evidence
- post-commit index/worktree
- forbidden actions not run
- Human-owned terminal review pending
- rollback/recovery guidance without destructive command execution
- preserved exact paths
- unverified items
- next recommendation

---

# 22. result classification

## success

Executor final response:

```text
result:
completed

P2-1D:
GIT_PERSISTED /
COMMAND_CENTER_COMMIT_REVIEW_REQUIRED
```

반드시 new commit hash를 제시한다.

다음 단계는 Browser Command Center substantive commit review다.

Executor는 P2-1E를 시작하지 않는다.

## blocked

prerequisite/provenance/dirty/runtime/staging/commit blocker가 있으면:

```text
result:
blocked
```

정확한 blocker code, path, expected/actual evidence를 제출한다.

accepted implementation/Human QA를 source defect로 되돌리지 않는다 unless exact accepted candidate bytes themselves conflict.

---

# 23. preserved exact paths

성공 시 최소 보존:

```text
.aiassistant/tasks/done/20260903_2226_aiscc-p2-1d-evidence-human-judgment-detail-implementation-1.md

.aiassistant/tasks/done/20260903_2315_aiscc-p2-1d-evidence-human-judgment-detail-transport-corrected-implementation-retry-1.md

.aiassistant/records/aiscc/cycles/20260904_0150_aiscc-p2-1d-source-static-partial-acceptance-runtime-evidence-expansion-required-1.cycle.md

.aiassistant/reports/aiscc/20260904_0152_aiscc-browser-command-center-p2-1d-runtime-evidence-completion-entry-handoff-1.md

.aiassistant/tasks/done/20260907_1531_aiscc-p2-1d-postgresql-runtime-evidence-completion-1.md

.aiassistant/records/aiscc/cycles/20260907_1555_aiscc-p2-1d-runtime-evidence-acceptance-human-browser-qa-entry-authorization-1.cycle.md

.aiassistant/reports/aiscc/20260907_1555_aiscc-browser-command-center-p2-1d-runtime-accepted-human-browser-qa-entry-handoff-1.md

.aiassistant/tasks/done/20260907_1606_aiscc-p2-1d-human-browser-qa-operation-guide-2.md

.aiassistant/records/aiscc/cycles/20260907_1631_aiscc-p2-1d-human-browser-qa-final-acceptance-persistence-entry-1.cycle.md

.aiassistant/tasks/done/20260907_1631_aiscc-p2-1d-final-acceptance-runtime-cleanup-and-git-persistence-1.md

.aiassistant/records/aiscc/cycles/20260907_1712_aiscc-p2-1d-persistence-blocked-missing-human-qa-guide-1.cycle.md

.aiassistant/reports/aiscc/20260907_1712_aiscc-browser-command-center-p2-1d-persistence-blocked-retry-entry-handoff-1.md

.aiassistant/tasks/done/20260907_1727_aiscc-p2-1d-final-acceptance-git-persistence-retry-1.md
```

1521 artifacts는 Section 8의 reconciliation 결과에 따라 exact canonical path를 추가 보존한다.

wrong-location duplicate는 canonical identity verification 후에만 제거 대상이다.

Target bundle은 Browser Command Center review 전까지 보존한다.

---

# 24. 최종 응답 형식

1. result: completed / blocked
2. P2-1D executor ceiling state
3. target bundle path
4. preflight HEAD/tree/index
5. provenance transport result
6. governance reconciliation result
7. accepted candidate identity result
8. runtime/cache cleanup result
9. staged exact path count + outside allowlist count
10. commit hash/tree/parent/message
11. post-commit index/worktree
12. changed files
13. removed files
14. human verification: `COMMAND_CENTER_COMMIT_REVIEW_REQUIRED`
15. unverified items
16. preserved exact paths

장문 report 전문은 chat에 붙이지 않는다.
