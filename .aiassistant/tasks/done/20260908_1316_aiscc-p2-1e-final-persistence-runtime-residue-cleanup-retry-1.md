# 작업지시서: P2-1E final persistence runtime residue cleanup retry

## meta

- task_id: `20260908_1316_aiscc-p2-1e-final-persistence-runtime-residue-cleanup-retry-1`
- created_at: `2026-09-08T13:16:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `QA_ONLY / FINAL_ACCEPTANCE_PERSISTENCE_RETRY`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `exact runtime residue reconciliation + P2-1E accepted candidate Git persistence`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- accepted_parent_HEAD: `36bed286abf4df6e8cecea2d379896c36be5d58a`
- accepted_parent_tree: `221ee3e4b675bb3ca871ba38557c10ffadbf96fe`
- fresh_ide_executor_chat: `NOT_REQUIRED`

## 현재 상태

```text
P2-1E:
ACCEPTED

P2-1:
ACTIVE / NOT_CLOSED

0840 final persistence:
HOLD_REWORK_REQUIRED / DIRTY_WORKSPACE_MIXED

Git persistence:
NOT_COMPLETED

P2-1E QA runtime:
ACTIVE at last inventory

P2-2:
NOT_STARTED
```

`0840` Task는 정확히 60개의 unexpected Git-visible `.pyc` 때문에 mandatory stop했다.

이번 Task는 P2-1E 구현/QA를 다시 하는 Task가 아니다.

이번 Task의 유일한 새 mutation authorization은:

```text
exact 60-path Python bytecode runtime residue cleanup
```

이다.

## 이번 턴 목표

1. transported current Cycle/Judgment가 canonical path에 존재하는지 확인한다.
2. mutation 전 branch/HEAD/tree/index와 current Git-visible set을 exact 검증한다.
3. unexpected dirt가 아래 60-path authorized residue set 이외에 없는지 확인한다.
4. P2-1E QA server/container identity를 확인하고 exact runtime만 stop/remove한다.
5. authorized residue 60개 중 현재 존재하는 파일만 literal-path delete한다.
6. cleanup 후 Git-visible canonical/product set을 exact `30 paths`로 검증한다.
7. accepted four product/test SHA를 다시 `4/4` 검증한다.
8. current Task를 active→done으로 이동한다.
9. exact `31-path` allowlist만 stage/commit한다.
10. commit/tree/parent/path/blob/worktree/runtime absence를 검증하고 Browser Command Center에 제출한다.

## 비목표

- product/test source 수정
- `.gitignore` 변경
- new fixture/migration/config/dependency
- Browser/Human QA rerun
- broad cache cleanup
- broad Git cleanup
- Project Source sync
- deployment
- Git push
- P2-1 CLOSED 선언
- P2-2 시작

## 반드시 읽을 문서

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md
.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md
.aiassistant/records/command-center/JUDGMENT_RUBRIC.md

.aiassistant/records/aiscc/cycles/20260908_0329_aiscc-p2-1e-human-browser-evidence-complete-final-acceptance-persistence-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_0329_aiscc-browser-command-center-p2-1e-final-acceptance-persistence-entry-handoff-1.md

.aiassistant/tasks/done/20260908_0840_aiscc-p2-1e-final-acceptance-runtime-cleanup-and-git-persistence-1.md
.aiassistant/records/aiscc/cycles/20260908_1316_aiscc-p2-1e-final-persistence-blocked-runtime-residue-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_1316_aiscc-p2-1e-final-persistence-preflight-runtime-residue-judgment-1.md
```

Unrelated source/rules/logs를 bulk-read하지 마라.

# 1. initial exact preflight

Substantive mutation 전에:

```text
branch:
main

HEAD:
36bed286abf4df6e8cecea2d379896c36be5d58a

HEAD tree:
221ee3e4b675bb3ca871ba38557c10ffadbf96fe

index:
empty
```

가 아니면 STOP.

이번 Task transport 완료 직후 current active Task는 ignored 상태여야 한다.

정상 Git-visible 구성은:

```text
30 accepted/canonical paths
+
authorized runtime residue up to exact 60 paths
```

이다.

새 Cycle/Judgment가 이번 transport에서 canonical에 추가되므로 `0840` 당시 28-path set에 2개가 추가된다.

## 1.1 exact 30-path non-residue set

- `src/aiscc/command_center/web.py`
- `src/aiscc/api/routes/command_center_ui.py`
- `tests/integration/command_center/test_web_ui.py`
- `tests/unit/command_center/test_web_shell.py`
- `.aiassistant/records/aiscc/cycles/20260907_1805_aiscc-p2-1d-persistence-final-acceptance-p2-1e-entry-authorization-1.cycle.md`
- `.aiassistant/reports/aiscc/20260907_1805_aiscc-browser-command-center-p2-1d-completion-p2-1e-entry-handoff-1.md`
- `.aiassistant/tasks/done/20260907_1814_aiscc-p2-1e-cycle-next-action-integrated-command-center-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260907_2241_aiscc-p2-1e-preflight-blocked-known-governance-dirt-1.cycle.md`
- `.aiassistant/reports/aiscc/20260907_2241_aiscc-browser-command-center-p2-1e-preflight-blocked-retry-entry-handoff-1.md`
- `.aiassistant/tasks/done/20260907_2252_aiscc-p2-1e-cycle-next-action-integrated-command-center-implementation-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260907_2320_aiscc-p2-1e-runtime-prerequisite-blocked-after-source-audit-1.cycle.md`
- `.aiassistant/reports/aiscc/20260907_2320_aiscc-browser-command-center-p2-1e-runtime-prerequisite-blocked-retry-entry-handoff-1.md`
- `.aiassistant/tasks/done/20260907_2328_aiscc-p2-1e-authorized-postgresql-runtime-implementation-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_0020_aiscc-p2-1e-implementation-runtime-candidate-accepted-human-qa-pending-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_0020_aiscc-browser-command-center-p2-1e-candidate-accepted-human-qa-entry-handoff-1.md`
- `.aiassistant/tasks/done/20260908_0051_aiscc-p2-1e-human-integrated-browser-qa-operation-guide-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_0158_aiscc-p2-1e-human-browser-qa-partial-accepted-nextaction-none-fixture-gap-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_0158_aiscc-browser-command-center-p2-1e-human-qa-partial-evidence-completion-entry-handoff-1.md`
- `.aiassistant/tasks/done/20260908_0208_aiscc-p2-1e-nextaction-none-human-qa-evidence-completion-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_0222_aiscc-p2-1e-evidence-gap-closure-blocked-missing-canonical-qa-guide-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_0222_aiscc-browser-command-center-p2-1e-missing-qa-guide-restoration-entry-handoff-1.md`
- `.aiassistant/tasks/done/20260908_0227_aiscc-p2-1e-0051-human-qa-guide-canonical-artifact-restoration-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_0259_aiscc-p2-1e-0051-canonical-qa-guide-restoration-accepted-evidence-gap-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_0259_aiscc-browser-command-center-p2-1e-0051-restoration-accepted-evidence-gap-retry-entry-handoff-1.md`
- `.aiassistant/tasks/done/20260908_0303_aiscc-p2-1e-nextaction-none-human-qa-evidence-completion-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_0329_aiscc-p2-1e-human-browser-evidence-complete-final-acceptance-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_0329_aiscc-browser-command-center-p2-1e-final-acceptance-persistence-entry-handoff-1.md`
- `.aiassistant/tasks/done/20260908_0840_aiscc-p2-1e-final-acceptance-runtime-cleanup-and-git-persistence-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_1316_aiscc-p2-1e-final-persistence-blocked-runtime-residue-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1316_aiscc-p2-1e-final-persistence-preflight-runtime-residue-judgment-1.md`

위 30개 중 missing이 있거나, 아래 authorized residue list 외의 추가 Git-visible path가 있으면 STOP.

## 1.2 accepted product/test SHA

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

4/4가 아니면 STOP. 수정/restore하지 마라.

# 2. exact authorized runtime residue set — 60 paths

이번 Task가 삭제를 허용하는 file path는 아래 exact 60개뿐이다.

- `src/aiscc/__pycache__/__init__.cpython-312.pyc`
- `src/aiscc/__pycache__/__main__.cpython-312.pyc`
- `src/aiscc/api/__pycache__/__init__.cpython-312.pyc`
- `src/aiscc/api/__pycache__/app.cpython-312.pyc`
- `src/aiscc/api/routes/__pycache__/__init__.cpython-312.pyc`
- `src/aiscc/api/routes/__pycache__/command_center.cpython-312.pyc`
- `src/aiscc/api/routes/__pycache__/command_center_ui.cpython-312.pyc`
- `src/aiscc/api/routes/__pycache__/control.cpython-312.pyc`
- `src/aiscc/api/routes/__pycache__/health.cpython-312.pyc`
- `src/aiscc/command_center/__pycache__/__init__.cpython-312.pyc`
- `src/aiscc/command_center/__pycache__/postgres_queries.cpython-312.pyc`
- `src/aiscc/command_center/__pycache__/privacy.cpython-312.pyc`
- `src/aiscc/command_center/__pycache__/queries.cpython-312.pyc`
- `src/aiscc/command_center/__pycache__/read_models.cpython-312.pyc`
- `src/aiscc/command_center/__pycache__/web.cpython-312.pyc`
- `src/aiscc/contracts/__pycache__/__init__.cpython-312.pyc`
- `src/aiscc/contracts/__pycache__/canonical_json.cpython-312.pyc`
- `src/aiscc/contracts/__pycache__/security.cpython-312.pyc`
- `src/aiscc/contracts/__pycache__/workflow.cpython-312.pyc`
- `src/aiscc/cycle/__pycache__/__init__.cpython-312.pyc`
- `src/aiscc/cycle/__pycache__/models.cpython-312.pyc`
- `src/aiscc/evidence/__pycache__/__init__.cpython-312.pyc`
- `src/aiscc/evidence/__pycache__/admission.cpython-312.pyc`
- `src/aiscc/evidence/__pycache__/attestation.cpython-312.pyc`
- `src/aiscc/evidence/__pycache__/checkpoints.cpython-312.pyc`
- `src/aiscc/evidence/__pycache__/content.cpython-312.pyc`
- `src/aiscc/evidence/__pycache__/issuers.cpython-312.pyc`
- `src/aiscc/evidence/__pycache__/models.cpython-312.pyc`
- `src/aiscc/evidence/__pycache__/ports.cpython-312.pyc`
- `src/aiscc/evidence/__pycache__/repository.cpython-312.pyc`
- `src/aiscc/evidence/__pycache__/requirements.cpython-312.pyc`
- `src/aiscc/evidence/__pycache__/service.cpython-312.pyc`
- `src/aiscc/evidence/__pycache__/set_evaluator.cpython-312.pyc`
- `src/aiscc/human/__pycache__/__init__.cpython-312.pyc`
- `src/aiscc/human/__pycache__/authority.cpython-312.pyc`
- `src/aiscc/human/__pycache__/models.cpython-312.pyc`
- `src/aiscc/human/__pycache__/repository.cpython-312.pyc`
- `src/aiscc/judgment/__pycache__/__init__.cpython-312.pyc`
- `src/aiscc/judgment/__pycache__/authority.cpython-312.pyc`
- `src/aiscc/judgment/__pycache__/models.cpython-312.pyc`
- `src/aiscc/memory/__pycache__/__init__.cpython-312.pyc`
- `src/aiscc/memory/__pycache__/models.cpython-312.pyc`
- `src/aiscc/persistence/__pycache__/__init__.cpython-312.pyc`
- `src/aiscc/persistence/__pycache__/database.cpython-312.pyc`
- `src/aiscc/persistence/__pycache__/models.cpython-312.pyc`
- `src/aiscc/persistence/__pycache__/repository.cpython-312.pyc`
- `src/aiscc/providers/__pycache__/__init__.cpython-312.pyc`
- `src/aiscc/providers/__pycache__/events.cpython-312.pyc`
- `src/aiscc/providers/__pycache__/models.cpython-312.pyc`
- `src/aiscc/task_authority/__pycache__/__init__.cpython-312.pyc`
- `src/aiscc/task_authority/__pycache__/models.cpython-312.pyc`
- `src/aiscc/task_authority/__pycache__/ports.cpython-312.pyc`
- `src/aiscc/workflow/__pycache__/__init__.cpython-312.pyc`
- `src/aiscc/workflow/__pycache__/evaluator.cpython-312.pyc`
- `src/aiscc/workflow/__pycache__/guards.cpython-312.pyc`
- `src/aiscc/workflow/__pycache__/kernel.cpython-312.pyc`
- `src/aiscc/workflow/__pycache__/matrix.cpython-312.pyc`
- `src/aiscc/workflow/__pycache__/models.cpython-312.pyc`
- `src/aiscc/workflow/__pycache__/participants.cpython-312.pyc`
- `src/aiscc/workflow/__pycache__/ports.cpython-312.pyc`

삭제 규칙:

```text
- 각 path를 literal path로 다룬다.
- 존재하는 파일만 삭제한다.
- 위 목록에 없는 파일은 삭제하지 않는다.
- directory recursive delete 금지.
- glob delete 금지.
- git clean 금지.
- .gitignore 변경 금지.
- empty __pycache__ directory를 지우기 위해 scope를 넓히지 않는다.
```

`System.IO.File.Delete(exact_path)` 또는 동등한 exact literal-file deletion은 허용한다.

초기 inventory에서 authorized set의 일부가 이미 absent인 것은 허용한다.

그러나 이 60개 외 새로운 Git-visible path가 하나라도 있으면 cleanup 전에 STOP한다.

# 3. P2-1E QA runtime cleanup

Bytecode regeneration 가능성을 제거하기 위해 residue file deletion 전에 runtime identity를 확인하고 exact QA runtime을 먼저 종료한다.

Expected lineage:

```text
PostgreSQL container:
aiscc-p2-1e-human-qa

image:
postgres:17.6-alpine

bind:
127.0.0.1:55439 -> 5432/tcp

AISCC server:
127.0.0.1:8765

known server command:
Python -B -m aiscc serve --host 127.0.0.1 --port 8765
```

Container/server가 이미 absent이면 `ALREADY_ABSENT / PASS`.

존재하면 exact identity를 확인한 뒤에만:

```text
docker stop aiscc-p2-1e-human-qa
docker rm aiscc-p2-1e-human-qa
```

및 exact AISCC listener process graceful termination을 허용한다.

금지:

```text
docker system prune
docker container prune
docker volume prune
other container stop/rm
unrelated process termination
broad image/volume deletion
```

identity가 모호하면 `RUNTIME_IDENTITY_CONFLICT`로 STOP.

Cleanup 후:

```text
aiscc-p2-1e-human-qa:
absent

127.0.0.1:55439:
absent

127.0.0.1:8765 P2-1E QA server:
absent
```

를 확인한다.

# 4. residue cleanup and post-cleanup preflight

Runtime cleanup이 PASS한 뒤 Section 2의 authorized files만 exact delete한다.

그 다음 Git-visible set은 **exact 30 paths**여야 한다.

```text
expected:
30

extra:
0

missing:
0

index:
empty

HEAD:
36bed286abf4df6e8cecea2d379896c36be5d58a
```

60-path cleanup 뒤에도 새로운 `.pyc` 또는 다른 dirt가 남으면 STOP한다.

Product/test SHA도 다시 4/4 확인한다.

# 5. current Task lifecycle

모든 cleanup/preflight gate가 PASS한 뒤:

```text
.aiassistant/tasks/active/20260908_1316_aiscc-p2-1e-final-persistence-runtime-residue-cleanup-retry-1.md
→
.aiassistant/tasks/done/20260908_1316_aiscc-p2-1e-final-persistence-runtime-residue-cleanup-retry-1.md
```

으로 이동한다.

이후 Git-visible final commit candidate는 exact `31 paths`다.

# 6. exact final 31-path commit allowlist

- `src/aiscc/command_center/web.py`
- `src/aiscc/api/routes/command_center_ui.py`
- `tests/integration/command_center/test_web_ui.py`
- `tests/unit/command_center/test_web_shell.py`
- `.aiassistant/records/aiscc/cycles/20260907_1805_aiscc-p2-1d-persistence-final-acceptance-p2-1e-entry-authorization-1.cycle.md`
- `.aiassistant/reports/aiscc/20260907_1805_aiscc-browser-command-center-p2-1d-completion-p2-1e-entry-handoff-1.md`
- `.aiassistant/tasks/done/20260907_1814_aiscc-p2-1e-cycle-next-action-integrated-command-center-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260907_2241_aiscc-p2-1e-preflight-blocked-known-governance-dirt-1.cycle.md`
- `.aiassistant/reports/aiscc/20260907_2241_aiscc-browser-command-center-p2-1e-preflight-blocked-retry-entry-handoff-1.md`
- `.aiassistant/tasks/done/20260907_2252_aiscc-p2-1e-cycle-next-action-integrated-command-center-implementation-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260907_2320_aiscc-p2-1e-runtime-prerequisite-blocked-after-source-audit-1.cycle.md`
- `.aiassistant/reports/aiscc/20260907_2320_aiscc-browser-command-center-p2-1e-runtime-prerequisite-blocked-retry-entry-handoff-1.md`
- `.aiassistant/tasks/done/20260907_2328_aiscc-p2-1e-authorized-postgresql-runtime-implementation-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_0020_aiscc-p2-1e-implementation-runtime-candidate-accepted-human-qa-pending-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_0020_aiscc-browser-command-center-p2-1e-candidate-accepted-human-qa-entry-handoff-1.md`
- `.aiassistant/tasks/done/20260908_0051_aiscc-p2-1e-human-integrated-browser-qa-operation-guide-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_0158_aiscc-p2-1e-human-browser-qa-partial-accepted-nextaction-none-fixture-gap-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_0158_aiscc-browser-command-center-p2-1e-human-qa-partial-evidence-completion-entry-handoff-1.md`
- `.aiassistant/tasks/done/20260908_0208_aiscc-p2-1e-nextaction-none-human-qa-evidence-completion-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_0222_aiscc-p2-1e-evidence-gap-closure-blocked-missing-canonical-qa-guide-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_0222_aiscc-browser-command-center-p2-1e-missing-qa-guide-restoration-entry-handoff-1.md`
- `.aiassistant/tasks/done/20260908_0227_aiscc-p2-1e-0051-human-qa-guide-canonical-artifact-restoration-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_0259_aiscc-p2-1e-0051-canonical-qa-guide-restoration-accepted-evidence-gap-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_0259_aiscc-browser-command-center-p2-1e-0051-restoration-accepted-evidence-gap-retry-entry-handoff-1.md`
- `.aiassistant/tasks/done/20260908_0303_aiscc-p2-1e-nextaction-none-human-qa-evidence-completion-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_0329_aiscc-p2-1e-human-browser-evidence-complete-final-acceptance-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_0329_aiscc-browser-command-center-p2-1e-final-acceptance-persistence-entry-handoff-1.md`
- `.aiassistant/tasks/done/20260908_0840_aiscc-p2-1e-final-acceptance-runtime-cleanup-and-git-persistence-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_1316_aiscc-p2-1e-final-persistence-blocked-runtime-residue-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1316_aiscc-p2-1e-final-persistence-preflight-runtime-residue-judgment-1.md`
- `.aiassistant/tasks/done/20260908_1316_aiscc-p2-1e-final-persistence-runtime-residue-cleanup-retry-1.md`

이 31개 외에는 stage하지 마라.

# 7. Git persistence authorization

모든 이전 gate가 PASS한 경우에만:

```text
git add -- <exact 31 literal paths>
git diff --cached --check
git diff --cached --name-status
git commit -m "feat(command-center): complete P2-1E cycle and next-action integration"
```

를 허용한다.

금지:

```text
git add -A
git add .
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

Expected commit:

```text
parent:
36bed286abf4df6e8cecea2d379896c36be5d58a

parent count:
1

message:
feat(command-center): complete P2-1E cycle and next-action integration

changed paths:
exact 31
```

# 8. post-commit verification

반드시 확인:

1. result commit hash/tree
2. exact parent and parent count=1
3. exact message
4. commit changed paths == Task 31-path allowlist
5. product/test committed SHA 4/4 exact
6. governance committed blobs 존재
7. exported path-preserving committed copies byte equality
8. index empty
9. Git-visible worktree clean
10. QA container absent
11. `127.0.0.1:55439` absent
12. `127.0.0.1:8765` QA listener absent
13. push/network NOT_RUN

# 9. evidence contract

## executor_required

- `WORKSPACE_GIT_PREFLIGHT`: initial non-residue 30 + authorized residue subset, no other dirt
- `RUNTIME_CLEANUP`: exact QA runtime only
- `RUNTIME_RESIDUE_CLEANUP`: exact 60 allowlist only
- `STATIC_SOURCE / HASH_IDENTITY`: 4/4
- `GIT_PERSISTENCE`: exact 31-path commit
- `PUBLIC_PROVENANCE / COMMIT_VERIFICATION`: commit/blob/worktree mapping

## reuse_allowed

- P2-1E source/runtime acceptance: `REUSED_ACCEPTED`
- Human Browser QA Operations 8/17: `HUMAN_PROVIDED / REUSED_ACCEPTED`

조건:

```text
4 product/test hashes unchanged
AND
no product/test/config/migration mutation
```

## human_owned

```text
new Human verification:
NOT_REQUIRED
```

## forbidden

- broad cleanup
- source implementation change
- new tests for acceptance
- Browser QA rerun
- P2-2
- deployment
- mirror sync
- Git push

# 10. mandatory stop

다음이면 즉시 STOP:

```text
MISSING_REQUIRED_ARTIFACT
HEAD_OR_TREE_MISMATCH
INDEX_NOT_EMPTY
ACCEPTED_CANDIDATE_IDENTITY_MISMATCH
UNEXPECTED_GIT_VISIBLE_PATH_OUTSIDE_AUTHORIZED_RESIDUE
RUNTIME_IDENTITY_CONFLICT
RESIDUE_CLEANUP_SCOPE_MISMATCH
POST_CLEANUP_30_PATH_MISMATCH
GIT_STAGE_ALLOWLIST_MISMATCH
GIT_COMMIT_VERIFICATION_FAILED
SECURITY_BOUNDARY_UNCERTAIN
```

Named blocker 뒤에는 blocker 최소 evidence/report/export만 수행한다.

# 11. export bundle

Target:

```text
.aiassistant/reports/target/20260908_1316_aiscc-p2-1e-final-persistence-runtime-residue-cleanup-retry-1/
```

필수 root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
RUNTIME_CLEANUP_VERIFICATION.md
RUNTIME_RESIDUE_CLEANUP_VERIFICATION.md
GIT_PERSISTENCE_VERIFICATION.md
```

Commit 성공 시 final 31 committed paths를 project-relative path로 export한다.

Repository file deletion은 `.pyc` untracked runtime residue뿐이므로 `REMOVED_FILES.md`를 canonical source deletion 증거처럼 만들지 마라. 대신 `RUNTIME_RESIDUE_CLEANUP_VERIFICATION.md`에 exact deleted/absent set을 기록한다.

# 12. final response ceiling

성공 시:

```text
P2-1 terminal closure readiness:
READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT
```

실패 시:

```text
NOT_READY / <exact blocker>
```

Executor는 다음을 선언하지 않는다.

```text
P2-1 CLOSED
P2-2 STARTED
```
