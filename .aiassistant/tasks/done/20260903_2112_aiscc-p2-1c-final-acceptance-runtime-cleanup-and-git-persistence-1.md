# 작업지시서: P2-1C Final Acceptance Runtime Cleanup and Git Persistence

## meta

- task_id: `20260903_2112_aiscc-p2-1c-final-acceptance-runtime-cleanup-and-git-persistence-1`
- created_at: `2026-09-03T21:12:00+09:00`
- project: `AI Software Command Center (AISCC)`
- phase: `P2-1C`
- work_type: `GIT_PERSISTENCE / RUNTIME_CLEANUP`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `terminal persistence of Human-accepted P2-1C candidate`

## 현재 상태

```text
P2-1C source/runtime:
ACCEPTED

P2-1C Human QA:
HUMAN_PROVIDED / PASS

P2-1C:
ACCEPTED / PERSISTENCE_PENDING

P2-1D:
NOT_STARTED
```

Accepted repository base:

```text
62a3c5135a12afc38ba32e4c5f651c1f1b007549
```

Accepted P2-1C product/test aggregate:

```text
2e4ca49afcd074aa2eac768b6f966d3d48044067917328a35c7839e078b35af3
```

Expected accepted product/test identities:

```text
src/aiscc/api/routes/command_center_ui.py
82d73e29ed5c185948ba82a5fc79083cafdb77b36b3f30760f570c295af01fd2

src/aiscc/command_center/web.py
949f548548d2a92b260e2bb56fd99f4defa1188420263cc61ede49451c05a779

tests/integration/command_center/test_web_ui.py
1eb8d100be9b64c8c2ecd1779f5b67b90862ed96c23be2861b3f809e28a2f4d4

tests/unit/command_center/test_web_shell.py
7bef092098bbf9867378a18520d051fd1c1c6f9c91e050a5d53b481c449da382
```

Current Human acceptance Cycle to transport:

```text
20260903_2112_aiscc-p2-1c-human-browser-qa-final-acceptance-persistence-entry-1.cycle.md
```

## 이번 턴 목표

1. accepted P2-1C source/test bytes가 exact aggregate와 일치하는지 preflight한다.
2. completed Human QA Task를 `tasks/done` provenance로 보존한다.
3. latest Human acceptance Cycle을 canonical cycles path에 보존한다.
4. P2-1C QA용 local web server와 disposable PostgreSQL container를 종료/제거한다.
5. QA-only process environment를 현재 shell에서 제거한다.
6. broad cleanup 없이 exact persistence allowlist만 Git stage한다.
7. staged diff와 exact path set을 검증한다.
8. P2-1C accepted product/test + governance provenance를 하나의 terminal persistence commit으로 생성한다.
9. commit 이후 HEAD/tree/status를 보고한다.
10. P2-1D는 시작하지 않는다.

## 비목표

- P2-1D/P2-1E 구현
- Project Source mirror sync
- source 변경
- test 변경
- migration/config 변경
- README/public docs 변경
- deployment
- push
- PR
- broad cleanup
- `__pycache__` / `.pyc` cleanup

## transport

Downloads의 Task와 latest Cycle을 먼저 read-only로 확인할 수 있다.

Task:

```text
20260903_2112_aiscc-p2-1c-final-acceptance-runtime-cleanup-and-git-persistence-1.md
```

Human acceptance Cycle:

```text
20260903_2112_aiscc-p2-1c-human-browser-qa-final-acceptance-persistence-entry-1.cycle.md
```

Expected Browser-generated Cycle SHA-256:

```text
e69b448642d9165499514f052be6d5be5d730a823bb4f8282c1a3da3b56dc8f0
```

Transport destination:

```text
.aiassistant/records/aiscc/cycles/20260903_2112_aiscc-p2-1c-human-browser-qa-final-acceptance-persistence-entry-1.cycle.md
```

Human QA Task destination:

```text
.aiassistant/tasks/done/20260903_2029_aiscc-p2-1c-workrun-detail-human-browser-qa-1.md
```

If the Human QA Task still exists only under `.aiassistant/tasks/active/`, move it to the exact done path.
Do not alter its bytes.

Environment setup Task:

```text
.aiassistant/tasks/done/20260903_2059_aiscc-p2-1c-human-qa-runtime-environment-setup-only-1.md
```

If its Executor turn already completed and it is in done, preserve it.
If it is still active despite completed setup, move it to done without altering bytes.
If missing, report the provenance gap and STOP before commit.

## preflight

Required:

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

HEAD before commit:
62a3c5135a12afc38ba32e4c5f651c1f1b007549

Git index:
empty
```

Compute exact SHA-256 for the four accepted product/test paths and recompute aggregate.

Pass only if:

```text
aggregate ==
2e4ca49afcd074aa2eac768b6f966d3d48044067917328a35c7839e078b35af3
```

If not exact:

```text
SOURCE_IDENTITY_MISMATCH
STOP
```

Do not restore files to force a match.

## known runtime residue

Previously reported:

```text
133 untracked __pycache__ / .pyc files
```

These are not accepted product source and must not be staged.

Do not use:

```text
git clean
git restore
git checkout
git reset
git stash
```

A different residue count alone is not a blocker if all paths remain within known Python cache residue class.

Unrelated source/config/migration dirt is a blocker.

## QA runtime cleanup

Human QA is complete, so cleanup is now authorized.

### web server

Identify only the AISCC server process created by:

```text
20260903_2059_aiscc-p2-1c-human-qa-runtime-environment-setup-only-1
```

Terminate that exact process.

Do not kill unrelated Python processes.

Verify the previously used AISCC loopback port is no longer listening.

### PostgreSQL

Expected Task-owned container:

```text
aiscc-p2-1c-human-qa
```

Stop/remove only that exact container:

```powershell
docker rm -f aiscc-p2-1c-human-qa
```

Verify:

```powershell
docker ps -a --filter "name=^/aiscc-p2-1c-human-qa$"
```

returns no container.

Do not remove any other container/image/volume.

### QA shell environment

Clear if present:

```powershell
Remove-Item Env:AISCC_DATABASE_URL -ErrorAction SilentlyContinue
Remove-Item Env:AISCC_TEST_DATABASE_URL -ErrorAction SilentlyContinue
Remove-Item Env:PYTHONDONTWRITEBYTECODE -ErrorAction SilentlyContinue
```

This only affects the current Executor shell.
Report if the server used a detached child process and environment lifetime differs.

## exact persistence allowlist

Product/test:

```text
src/aiscc/api/routes/command_center_ui.py
src/aiscc/command_center/web.py
tests/integration/command_center/test_web_ui.py
tests/unit/command_center/test_web_shell.py
```

Governance/provenance:

```text
.aiassistant/tasks/done/20260903_1759_aiscc-p2-1c-workrun-transition-execution-detail-implementation-1.md
.aiassistant/tasks/done/20260903_1949_aiscc-p2-1c-retained-detail-stale-current-authority-labeling-rework-1.md
.aiassistant/tasks/done/20260903_2029_aiscc-p2-1c-workrun-detail-human-browser-qa-1.md
.aiassistant/tasks/done/20260903_2059_aiscc-p2-1c-human-qa-runtime-environment-setup-only-1.md
.aiassistant/tasks/done/20260903_2112_aiscc-p2-1c-final-acceptance-runtime-cleanup-and-git-persistence-1.md

.aiassistant/records/aiscc/cycles/20260903_1934_aiscc-p2-1c-workrun-detail-substantive-review-hold-1.cycle.md
.aiassistant/records/aiscc/cycles/20260903_2029_aiscc-p2-1c-stale-authority-rework-source-runtime-acceptance-human-qa-entry-1.cycle.md
.aiassistant/records/aiscc/cycles/20260903_2112_aiscc-p2-1c-human-browser-qa-final-acceptance-persistence-entry-1.cycle.md

.aiassistant/reports/aiscc/20260903_1936_aiscc-browser-command-center-p2-1c-hold-rework-entry-handoff-1.md
```

Before staging, verify which allowlist paths are already tracked at HEAD, newly untracked, or modified.

Do not stage any path outside this allowlist.

If an allowlist artifact is missing:

```text
BLOCKED_MISSING_ARTIFACT
STOP
```

## stage verification

Stage only exact allowlist paths.

Then verify:

```powershell
git diff --cached --name-only
```

must equal the actual Git-visible changed subset of the allowlist and contain no outside path.

Also run:

```powershell
git diff --cached --check
```

Must PASS.

Review staged diff summary.

Do not modify source after staging.

## commit

If and only if all preconditions pass, create one commit.

Recommended commit message:

```text
feat(command-center): complete P2-1C work run detail
```

No push.

After commit report:

```text
commit SHA
tree SHA
parent SHA
commit message
git status --short
```

Expected parent:

```text
62a3c5135a12afc38ba32e4c5f651c1f1b007549
```

## post-commit state

Successful persistence candidate:

```text
P2-1C:
ACCEPTED / PERSISTED_CANDIDATE

P2-1D:
NOT_STARTED
```

Do not claim P2-1C `PERSISTED` as Browser-final until the commit bundle/report is submitted and Command Center verifies exact commit/tree/path identity.

## evidence contract

executor_required:

```text
STATIC_SOURCE:
exact four-path identity and aggregate

PUBLIC_PROVENANCE:
exact Task/Cycle/Handoff paths

RUNTIME_CLEANUP:
exact QA server/container cleanup

GIT_PERSISTENCE:
exact allowlist stage + diff-check + commit identity
```

human_owned:

```text
already HUMAN_PROVIDED / PASS
no new Human QA required
```

forbidden:

```text
push
deployment
P2-1D
broad cleanup
source mutation
```

## target bundle

```text
.aiassistant/reports/target/20260903_2112_aiscc-p2-1c-final-acceptance-runtime-cleanup-and-git-persistence-1/
```

Required:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
```

Also include exact persisted governance artifact copies and the four accepted product/test files as needed for Browser verification.

Do not include `.git` objects, Python caches, DB data, Docker artifacts, credentials, or logs containing secrets.

## final response

```text
result:
completed / blocked

cleanup:
server = stopped / not-found / blocked
container = removed / not-found / blocked
env = cleared

source identity:
aggregate = ...
result = PASS / FAIL

staged paths:
...

commit:
sha = ...
tree = ...
parent = ...
message = ...

push:
NOT_RUN

P2-1D:
NOT_STARTED

target bundle:
...

preserved exact paths:
...
```
