# 작업지시서: P2-1D 최종 승인 Runtime 정리 및 Git Persistence

## meta

- task_id: `20260907_1631_aiscc-p2-1d-final-acceptance-runtime-cleanup-and-git-persistence-1`
- created_at: `2026-09-07T16:31:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `FINAL_ACCEPTANCE_GIT_PERSISTENCE`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `NOT_APPLICABLE`
- primary_semantic_owner: `P2-1D accepted candidate terminal Git persistence`

## 현재 상태

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

current accepted HEAD:
08368eceac625c9a74b4347021ed65540cb08b3c

current accepted tree:
c7c601677eb2a4ca2fa7b594465ebd16ed8da9f4

P2-1D:
SOURCE_STATIC_ACCEPTED
RUNTIME_EVIDENCE_ACCEPTED
HUMAN_BROWSER_QA:
HUMAN_PROVIDED / PASS
OVERALL:
ACCEPTED / PERSISTENCE_PENDING

P2-1E:
NOT_STARTED

P2-2:
NOT_STARTED
```

이번 Task는 구현 Task가 아니다.

```text
accepted bytes 검증
→ Human QA provenance transport
→ retained QA runtime 좁은 정리
→ exact allowlist staging
→ 단일 Git commit
→ persistence evidence export
```

만 수행한다.

---

# 1. 이번 턴 목표

1. P2-1D accepted product/test candidate bytes가 정확히 유지됐는지 검증한다.
2. 최신 `1555 Cycle/Handoff`, Human QA guide, `1631 Human final acceptance Cycle`을 exact identity로 repository canonical path에 transport한다.
3. Human QA를 위해 유지했던 P2-1D local runtime을 정확한 대상만 정리한다.
4. known Python cache residue를 explicit narrow rule 아래에서만 정리한다.
5. P2-1D product/test + accumulated accepted governance/provenance를 exact allowlist로 stage한다.
6. 단 하나의 P2-1D persistence commit을 생성한다.
7. Git object/path/tree 증거와 최종 inventory를 export한다.

---

# 2. 이번 턴 비목표

```text
source 구현 변경
test 구현 변경
migration 변경
repository config 변경
new runtime test
new browser QA
new DB fixture
P2-1E
P2-2
push
deployment
Project Source sync
```

---

# 3. must-read

먼저 exact path를 읽는다.

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md

.aiassistant/records/aiscc/cycles/20260903_2218_aiscc-p2-1c-persistence-final-acceptance-p2-1d-entry-authorization-1.cycle.md

.aiassistant/reports/aiscc/20260903_2220_aiscc-browser-command-center-p2-1c-completion-p2-1d-entry-handoff-1.md

.aiassistant/records/aiscc/cycles/20260904_0150_aiscc-p2-1d-source-static-partial-acceptance-runtime-evidence-expansion-required-1.cycle.md

.aiassistant/reports/aiscc/20260904_0152_aiscc-browser-command-center-p2-1d-runtime-evidence-completion-entry-handoff-1.md

.aiassistant/tasks/done/20260907_1531_aiscc-p2-1d-postgresql-runtime-evidence-completion-1.md
```

그리고 아래 Human-provided artifact를 exact transport 후 읽는다.

```text
20260907_1555_aiscc-p2-1d-runtime-evidence-acceptance-human-browser-qa-entry-authorization-1.cycle.md

20260907_1555_aiscc-browser-command-center-p2-1d-runtime-accepted-human-browser-qa-entry-handoff-1.md

20260907_1606_aiscc-p2-1d-human-browser-qa-operation-guide-2.md

20260907_1631_aiscc-p2-1d-human-browser-qa-final-acceptance-persistence-entry-1.cycle.md
```

unrelated rules/records/source/logs를 bulk-read하지 않는다.

---

# 4. Human-provided transport identity

Human은 Browser에서 아래 파일을 다운로드하여 제공한다.

Canonical filename 기준으로 exact identity를 검증한다.

## 1555 Cycle

Expected downloaded source name may contain a Browser-added suffix such as `(1)`.

Canonical destination:

```text
.aiassistant/records/aiscc/cycles/20260907_1555_aiscc-p2-1d-runtime-evidence-acceptance-human-browser-qa-entry-authorization-1.cycle.md
```

Expected bytes:

```text
14579
```

Expected SHA-256:

```text
2662ba127dd01da78d1056931c84bffedb5cce83ef3d45133b4b7c61cb5126d8
```

## 1555 Handoff

Canonical destination:

```text
.aiassistant/reports/aiscc/20260907_1555_aiscc-browser-command-center-p2-1d-runtime-accepted-human-browser-qa-entry-handoff-1.md
```

Expected bytes:

```text
9768
```

Expected SHA-256:

```text
16e3861fdb722370263cb7ee13f07f2959a6231b1de6b458437f07d0fe7ffdb5
```

## Human QA guide

Canonical destination:

```text
.aiassistant/tasks/done/20260907_1606_aiscc-p2-1d-human-browser-qa-operation-guide-2.md
```

Expected bytes:

```text
13096
```

Expected SHA-256:

```text
a737dcdd073d7113f10d55d4878c284d9855675a0f7c8d2a77cde484feac315e
```

## Human final acceptance Cycle

Canonical destination:

```text
.aiassistant/records/aiscc/cycles/20260907_1631_aiscc-p2-1d-human-browser-qa-final-acceptance-persistence-entry-1.cycle.md
```

이 파일은 현재 Task와 함께 Human이 다운로드하여 제공한다.

Transport rule:

```text
exact filename 우선
Browser suffix가 있는 경우 content identity로 canonical destination을 확정
alternate semantic guessing 금지
hash mismatch 시 STOP
```

`1631 Cycle`의 source bytes/SHA는 실제 다운로드 파일에서 계산하고 destination copy와 exact match를 증명한다.

---

# 5. accepted candidate exact identity

아래 3개 파일은 수정하지 않는다.

```text
src/aiscc/command_center/web.py
0e41ffb18256628a3c76150feeb6fc5c6b4d311d566b1e4c5b8d50987b308706

tests/integration/command_center/test_web_ui.py
2913359e913d7974d9165b0b013c7617438e1accf999af3c25bb876bd974821f

tests/unit/command_center/test_web_shell.py
29dfddb01aabfce7b5746cc762575271d2b16ad1c585d3b93e1d6ece1c575fa1
```

Sorted path/hash aggregate:

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
P2_1D_ACCEPTED_BYTE_IDENTITY_MISMATCH
```

source를 수정해서 맞추지 않는다.

---

# 6. repository preflight

mutation 전에 확인:

```text
branch == main
HEAD == 08368eceac625c9a74b4347021ed65540cb08b3c
index == empty
```

latest accepted runtime evidence의 workspace provenance:

```text
148 Git-visible entries
=
133 known Python cache
+
12 governance/provenance
+
3 accepted P2-1D candidate paths

unexpected product/config/migration:
0
```

이 숫자를 blindly trust하지 않는다.

현재 `git status`를 다시 수집하고 다음으로 분류한다.

```text
accepted P2-1D candidate
known accepted governance/provenance
Human-provided current artifacts
known Python runtime cache
unexpected dirt
```

unexpected product/config/migration/repository-config dirt가 하나라도 있으면 STOP한다.

금지:

```text
git clean
git restore
git checkout
git reset
git stash
```

---

# 7. retained QA runtime narrow cleanup

Human QA가 PASS했으므로 retained local runtime은 더 이상 필요하지 않다.

## AISCC server

Expected:

```text
127.0.0.1:8765
```

정리 전:

- listener/process identity를 확인한다.
- P2-1D retained server임을 합리적으로 식별할 수 있어야 한다.

정리:

```text
P2-1D retained AISCC server만 종료
```

금지:

```text
unrelated python/process kill
broad taskkill
port와 무관한 process 종료
```

정리 후:

```text
127.0.0.1:8765 listener count == 0
```

단, 해당 port가 이미 비어 있으면 그것을 source defect로 보지 않는다.
`already stopped`로 기록한다.

## PostgreSQL container

Exact name:

```text
aiscc-p2-1d-runtime-evidence
```

존재하면 exact-name container만 stop/remove한다.

정리 후:

```text
exact-name container count == 0
```

금지:

```text
other container removal
Docker image removal
volume prune
system prune
image pull
```

## shell env

현재 Executor shell에 아래가 Task runtime용으로 남아 있다면 제거한다.

```text
AISCC_DATABASE_URL
AISCC_TEST_DATABASE_URL
PYTHONDONTWRITEBYTECODE
```

다른 shell/system/user environment를 광범위하게 변경하지 않는다.

---

# 8. Python cache narrow cleanup authorization

이번 terminal persistence Task에서는 Git persistence를 위해 known untracked Python runtime residue 정리를 명시적으로 허용한다.

대상은 아래 조건을 모두 만족해야 한다.

```text
untracked
Python bytecode/cache
repository source tree 하위
__pycache__/*.pyc 또는 해당 정리 후 empty __pycache__ directory
```

허용:

```text
exact candidate list를 먼저 출력/기록
Git tracked file가 아님을 확인
그 exact list만 삭제
empty __pycache__ directory 정리
```

금지:

```text
git clean
glob으로 unrelated file 삭제
tracked file 삭제
source/test 파일 삭제
broad filesystem cleanup
```

정리 전후 count를 보고한다.

identity가 애매한 residue는 삭제하지 말고 blocker로 보고한다.

---

# 9. exact staging allowlist

Transport와 runtime/cache cleanup이 끝난 뒤 index가 empty인지 재확인한다.

아래 tracked-worthy P2-1 lineage와 candidate만 stage할 수 있다.

## inherited accepted governance/provenance

```text
.aiassistant/records/aiscc/cycles/20260903_1718_aiscc-p2-1b-shell-queue-persistence-final-acceptance-1.cycle.md

.aiassistant/reports/aiscc/20260903_1720_aiscc-browser-command-center-p2-1b-completion-p2-1c-entry-handoff-1.md

.aiassistant/records/aiscc/cycles/20260903_2218_aiscc-p2-1c-persistence-final-acceptance-p2-1d-entry-authorization-1.cycle.md

.aiassistant/reports/aiscc/20260903_2220_aiscc-browser-command-center-p2-1c-completion-p2-1d-entry-handoff-1.md
```

## P2-1D governance/provenance

```text
.aiassistant/tasks/done/20260903_2226_aiscc-p2-1d-evidence-human-judgment-detail-implementation-1.md

.aiassistant/records/aiscc/cycles/20260903_2255_aiscc-p2-1d-predecessor-transport-blocked-missing-artifact-1.cycle.md

.aiassistant/reports/aiscc/20260903_2255_aiscc-browser-command-center-p2-1d-transport-blocked-rework-entry-handoff-1.md

.aiassistant/tasks/done/20260903_2315_aiscc-p2-1d-evidence-human-judgment-detail-transport-corrected-implementation-retry-1.md

.aiassistant/records/aiscc/cycles/20260904_0150_aiscc-p2-1d-source-static-partial-acceptance-runtime-evidence-expansion-required-1.cycle.md

.aiassistant/reports/aiscc/20260904_0152_aiscc-browser-command-center-p2-1d-runtime-evidence-completion-entry-handoff-1.md

.aiassistant/tasks/done/20260904_0157_aiscc-p2-1d-runtime-evidence-completion-1.md

.aiassistant/tasks/done/20260907_1531_aiscc-p2-1d-postgresql-runtime-evidence-completion-1.md

.aiassistant/records/aiscc/cycles/20260907_1555_aiscc-p2-1d-runtime-evidence-acceptance-human-browser-qa-entry-authorization-1.cycle.md

.aiassistant/reports/aiscc/20260907_1555_aiscc-browser-command-center-p2-1d-runtime-accepted-human-browser-qa-entry-handoff-1.md

.aiassistant/tasks/done/20260907_1606_aiscc-p2-1d-human-browser-qa-operation-guide-2.md

.aiassistant/records/aiscc/cycles/20260907_1631_aiscc-p2-1d-human-browser-qa-final-acceptance-persistence-entry-1.cycle.md

.aiassistant/tasks/done/20260907_1631_aiscc-p2-1d-final-acceptance-runtime-cleanup-and-git-persistence-1.md
```

## accepted P2-1D product/test

```text
src/aiscc/command_center/web.py

tests/integration/command_center/test_web_ui.py

tests/unit/command_center/test_web_shell.py
```

No other path may be staged.

중복 없이 stage 후:

```text
git diff --cached --name-only
```

가 exact allowlist와 일치해야 한다.

현재 존재하지 않는 inherited path가 있다면 임의 생성/추측하지 말고 STOP한다.

---

# 10. pre-commit checks

반드시:

```text
accepted 3-file hashes exact
aggregate exact
protected route hash exact

git diff --cached --check:
PASS

outside allowlist staged:
0

index staged set:
exact
```

새 test 실행은 필요하지 않다.

이유:

```text
source/test bytes unchanged
source/static accepted
PostgreSQL runtime accepted
Human Browser QA accepted
```

새 test를 실행해 report 항목을 채우지 않는다.

---

# 11. Git commit

위 조건이 모두 PASS일 때만 단 하나의 commit을 생성한다.

Commit message:

```text
feat(command-center): complete P2-1D evidence and human judgment detail
```

금지:

```text
두 번째 commit
amend
rebase
merge
reset
push
tag
PR
deployment
```

Commit 후 증명:

```text
commit hash
tree hash
parent == 08368eceac625c9a74b4347021ed65540cb08b3c
message exact
committed path set exact
candidate blob/hash exact
index empty
```

P2-1D persistence commit이 생성되었다는 사실만으로 Browser Command Center terminal acceptance를 직접 주장하지 않는다.

Executor 결과 상태:

```text
P2-1D:
GIT_PERSISTED /
COMMAND_CENTER_COMMIT_REVIEW_REQUIRED
```

---

# 12. post-commit inventory

최종 확인:

```text
branch
HEAD
index
git status
```

기대:

- index empty
- P2-1D product/test candidate는 committed
- staged allowlist governance/provenance committed
- known Python cache cleanup 완료
- unexpected product/config/migration dirt 없음

allowlist 밖 inherited dirty path가 남으면 exact path와 classification을 기록한다.
임의 cleanup하지 않는다.

---

# 13. evidence contract

## executor_required

```text
exact preflight branch/HEAD/index/worktree
accepted 3-file hash + aggregate
protected route hash
Human artifact transport byte/hash identity
retained server cleanup evidence
exact PostgreSQL container cleanup evidence
Python cache exact-list cleanup evidence
exact staging set
git diff --cached --check
commit object/tree/parent/message/path evidence
post-commit index/worktree inventory
export manifest integrity
```

## reuse_allowed

```text
20260904_0150 source/static acceptance
20260907_1555 PostgreSQL runtime acceptance
20260907_1631 Human Browser QA acceptance
```

재사용 조건:

```text
accepted bytes exact
provenance exact
no contradictory current evidence
```

## human_owned

```text
P2-1D Human Browser QA:
HUMAN_PROVIDED / PASS
```

Executor가 재수행하거나 재판정하지 않는다.

## not_required

```text
new browser QA
new unit/integration suite
new PostgreSQL runtime
new HTTP runtime
provider/network
deployment
Project Source sync
```

## forbidden

```text
source/test/migration/config mutation
new fixture creation
Git push
deployment
P2-1E
P2-2
broad cleanup
Human acceptance 재작성
```

---

# 14. mandatory stop

다음이면 commit 전 STOP:

```text
HEAD mismatch
non-empty unexpected index
accepted candidate hash mismatch
protected route mismatch
Human artifact hash mismatch
missing required canonical predecessor artifact
unexpected product/config/migration dirt
runtime cleanup이 unrelated process/container에 영향을 줄 위험
cache cleanup exact ownership 불명확
staged path set mismatch
git diff --cached --check failure
third-party/private/secret material 발견
```

named blocker 이후:

```text
minimal evidence
safe index cleanup limited to this Task's own provable staging if necessary
report/export
STOP
```

`reset/restore/clean/stash`를 사용하지 않는다.

---

# 15. export bundle

Target:

```text
.aiassistant/reports/target/20260907_1631_aiscc-p2-1d-final-acceptance-runtime-cleanup-and-git-persistence-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
GIT_OBJECT_EVIDENCE.md
RUNTIME_CLEANUP_EVIDENCE.md
WORKSPACE_INVENTORY.md
HUMAN_QA_PROVENANCE.md
```

그리고 committed allowlist 파일을 repository-relative path로 복사한다.

Manifest에는:

```text
payload path
bytes
SHA-256
source repository path
source commit/tree/blob when applicable
copy/source exact match
```

를 기록한다.

Secret/private data를 export하지 않는다.

---

# 16. preserved exact paths

최종 report에 최소 아래를 보존 대상으로 명시한다.

```text
.aiassistant/tasks/done/20260907_1631_aiscc-p2-1d-final-acceptance-runtime-cleanup-and-git-persistence-1.md

.aiassistant/records/aiscc/cycles/20260907_1631_aiscc-p2-1d-human-browser-qa-final-acceptance-persistence-entry-1.cycle.md

.aiassistant/tasks/done/20260907_1606_aiscc-p2-1d-human-browser-qa-operation-guide-2.md

.aiassistant/records/aiscc/cycles/20260907_1555_aiscc-p2-1d-runtime-evidence-acceptance-human-browser-qa-entry-authorization-1.cycle.md

.aiassistant/reports/aiscc/20260907_1555_aiscc-browser-command-center-p2-1d-runtime-accepted-human-browser-qa-entry-handoff-1.md

.aiassistant/tasks/done/20260907_1531_aiscc-p2-1d-postgresql-runtime-evidence-completion-1.md

.aiassistant/records/aiscc/cycles/20260904_0150_aiscc-p2-1d-source-static-partial-acceptance-runtime-evidence-expansion-required-1.cycle.md

.aiassistant/reports/aiscc/20260904_0152_aiscc-browser-command-center-p2-1d-runtime-evidence-completion-entry-handoff-1.md
```

그리고 commit에 포함된 accepted P2-1D lineage 전체를 exact path로 보고한다.

Target bundle은 Browser Command Center의 commit substantive review 전까지 유지한다.

---

# 17. 성공 결과

성공 시 Executor가 주장할 수 있는 최대 상태:

```text
P2-1D:
GIT_PERSISTED /
COMMAND_CENTER_COMMIT_REVIEW_REQUIRED
```

Executor는 다음을 주장하면 안 된다.

```text
P2-1D CLOSED
P2-1E ENTRY_AUTHORIZED
P2-1E STARTED
P2-2 STARTED
```

그 판정은 제출 bundle을 Browser Command Center가 검토한 뒤 결정한다.
