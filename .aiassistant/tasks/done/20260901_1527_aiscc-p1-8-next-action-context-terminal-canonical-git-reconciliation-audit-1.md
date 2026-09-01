# 작업지시서: P1-8 NEXT_ACTION_CONTEXT Terminal Canonical Git Reconciliation Audit

## meta

- task_id: `20260901_1527_aiscc-p1-8-next-action-context-terminal-canonical-git-reconciliation-audit-1`
- created_at: `2026-09-01T15:27:00+09:00`
- phase: `P1-8 NEXT_ACTION_CONTEXT Source Authority Terminal Persistence Review`
- work_type: `SOURCE_EVIDENCE_EXPORT / QA_ONLY`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `AISCC_REPOSITORY_LOCAL_CANONICAL / GIT_OBJECT_DATABASE`
- mutation_authority: `AUDIT_ARTIFACT_AND_TASK_LIFECYCLE_ONLY`

---

# 1. 현재 판정과 감사 목적

제출 번들:

```text
20260831_1619_aiscc-p1-8-next-action-context-source-authority-terminal-acceptance-persistence-1(5).zip
```

번들 내부 검증 결과:

```text
ZIP CRC / 경로 안전성: PASS
accepted design exported SHA: PASS
7 exported governance source/copy SHA: PASS
root TASK.md == tasks/done copy: PASS
6 embedded canonical payload fingerprint recomputation: PASS
19-path blocked-runtime aggregate recomputation from manifest: PASS
state/Cycle/handoff semantic consistency: PASS
```

그러나 다음은 제출 번들의 Executor 작성 문서만으로 독립 검증할 수 없다.

```text
Commit A object existence and exact parent/tree boundary
Commit B object existence and exact parent/tree boundary
Commit B exact 19 changed paths
actual local HEAD/index/worktree residual state
all 14 historical/review/final provenance paths at committed tree
```

따라서 현재 Command Center 판정은:

```text
SUBSTANTIVE_CONTENT_PASS
TERMINAL_CLOSURE_EVIDENCE_AUDIT_REQUIRED
```

이다.

이번 Task는 local repository canonical을 read-only로 reconcile하여 아래 둘 중 하나만 증명한다.

```text
STATE_A_VERIFIED
→ 1619 terminal persistence is valid

or

STATE_A_NOT_VERIFIED
→ exact mismatch/blocker reported without mutation
```

이번 Task는 prerequisite design rework나 P1-8 Runtime을 시작하지 않는다.

---

# 2. expected identities

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

terminal base:
f4614198c2745944f7ec02639a45b0315bbc903d

Commit A candidate:
35901125cc5842734cf1e8eb3374d10e4ee866e3

Commit B candidate:
683aaee84d1fc09e9371dd214efc3ff58b7225ee

accepted design:
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md

accepted design SHA-256:
19b1d29a8f77ca5cc480a14bc9d1bdd53206951ccf8b34802316f1280dc61cb1

accepted parent P1-8 design SHA-256:
100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a

blocked runtime:
19 paths /
84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42

unaccepted prerequisite candidate:
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
556faad8a77d917fcbfc9ab7b0ba62bd65f985a6f4a1e585c08af668dd14393c
```

---

# 3. 이번 턴 목표

1. actual `HEAD`, branch, index, worktree를 read-only로 확인한다.
2. Commit A/B Git object와 exact parent lineage를 검증한다.
3. Commit A/B의 exact changed-path set과 금지 path 부재를 검증한다.
4. Commit A accepted blob과 Commit B terminal-governance blobs를 commit tree에서 직접 추출·검증한다.
5. canonical state/Cycle/handoff가 source-authority만 닫고 prerequisite/runtime을 계속 block하는지 검증한다.
6. residual uncommitted runtime/prerequisite candidate identity와 unexpected dirty path 부재를 검증한다.
7. Command Center가 Git object evidence를 독립 재검증할 수 있는 byte-preserving audit bundle을 생성한다.

---

# 4. 이번 턴 비목표

- prerequisite owner-authority candidate 수정
- P1-8 Runtime source/test/migration 수정 또는 실행 재개
- 새 design decision 또는 fingerprint 결정
- Human acceptance 재요청 또는 재해석
- canonical state/Cycle/handoff 수정
- Git commit/amend/rebase/reset/clean/checkout-overwrite
- Git push, remote fetch, network, deployment
- P2/P3/Public Live 작업

---

# 5. 읽을 문서

반드시 exact path로 읽는다.

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
.aiassistant/rules/AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/records/aiscc/cycles/20260831_1619_aiscc-p1-8-next-action-context-source-authority-final-acceptance-1.cycle.md
.aiassistant/reports/aiscc/20260831_1619_aiscc-p1-8-next-action-context-accepted-prerequisite-design-resume-handoff-1.md
```

그리고 이 active Task를 전부 읽는다.

Unrelated rules/source/log를 bulk-read하지 않는다.

---

# 6. 허용 범위

allowed_actions:

- Git read-only plumbing/inspection
- SHA-256 계산
- 현재 파일의 read-only inventory
- ignored target audit bundle 생성
- exact allowlist의 committed blob byte-preserving export
- audit 완료 후 current Task의 `active → done` lifecycle move

allowed_output_root:

```text
.aiassistant/reports/target/
20260901_1527_aiscc-p1-8-next-action-context-terminal-canonical-git-reconciliation-audit-1/
```

Task lifecycle 외 repository canonical/product source mutation은 금지한다.

---

# 7. 절대 금지

```text
git add
git commit
git commit --amend
git reset
git clean
git checkout -- <path>
git restore
git rebase
git merge
git cherry-pick
git push
git fetch
git pull
deployment
network/credential action
```

금지 path mutation:

```text
.aiassistant/rules/**
.aiassistant/records/**
.aiassistant/reports/aiscc/**
src/**
tests/**
migrations/**
```

단, 이번 active Task의 done lifecycle copy/move는 허용한다.

---

# 8. mandatory preflight snapshot

Task가 active/ignored 상태일 때, 어떤 파일도 변경하기 전에 다음을 기록한다.

```text
git rev-parse --show-toplevel
git branch --show-current
git rev-parse HEAD
git status --short --untracked-files=all
git diff --name-only
git diff --cached --name-only
git log --oneline --decorate -n 12
```

Expected:

```text
branch = main
HEAD = 683aaee84d1fc09e9371dd214efc3ff58b7225ee
index = empty
```

HEAD가 다르면 mutation하지 않고 다음으로 STOP한다.

```text
CANONICAL_HEAD_ADVANCED_OR_DIVERGED
```

단, exact HEAD/log/status evidence는 export한다.

---

# 9. Git object and lineage verification

다음을 Git object database에서 직접 검증한다.

```text
git cat-file -t 35901125cc5842734cf1e8eb3374d10e4ee866e3
git cat-file -t 683aaee84d1fc09e9371dd214efc3ff58b7225ee
```

둘 다 `commit`이어야 한다.

Exact lineage:

```text
parent(Commit A)
= f4614198c2745944f7ec02639a45b0315bbc903d

parent(Commit B)
= 35901125cc5842734cf1e8eb3374d10e4ee866e3
```

Raw commit object body를 byte-preserving export하고, export bytes에 대해 다음을 독립 재계산한다.

```text
git hash-object -t commit --stdin
```

Expected result는 각각 Commit A/B SHA와 같아야 한다.

Raw object export 시 PowerShell text redirection으로 newline/encoding을 변환하지 않는다. Git Bash binary-safe redirection 또는 binary-safe file API를 사용한다.

Mismatch:

```text
TERMINAL_COMMIT_OBJECT_OR_LINEAGE_MISMATCH
```

---

# 10. Commit A exact boundary

Commit A changed path는 정확히 하나여야 한다.

```text
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
```

Commit A의 해당 blob을 commit tree에서 byte-preserving export하고 SHA-256을 계산한다.

Expected:

```text
19b1d29a8f77ca5cc480a14bc9d1bdd53206951ccf8b34802316f1280dc61cb1
```

Commit A에 다른 path가 있거나 blob SHA가 다르면:

```text
COMMIT_A_ACCEPTED_DESIGN_BOUNDARY_MISMATCH
```

---

# 11. Commit B exact 19-path boundary

Commit B changed paths는 정확히 다음 19개여야 한다.

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/records/aiscc/cycles/20260831_1143_aiscc-p1-8-runtime-memory-next-action-authority-and-terminal-epoch-hold-1.cycle.md
.aiassistant/records/aiscc/cycles/20260831_1332_aiscc-p1-8-prerequisite-owner-authority-baseline-gap-hold-1.cycle.md
.aiassistant/records/aiscc/cycles/20260831_1332_aiscc-p1-8-prerequisite-owner-authority-exact-contract-gap-hold-1.cycle.md
.aiassistant/records/aiscc/cycles/20260831_1332_aiscc-p1-8-runtime-historical-replay-and-system-owner-capability-hold-1.cycle.md
.aiassistant/records/aiscc/cycles/20260831_1514_aiscc-p1-8-next-action-context-ranking-authority-compatibility-hold-1.cycle.md
.aiassistant/records/aiscc/cycles/20260831_1514_aiscc-p1-8-next-action-context-source-authority-baseline-gap-hold-1.cycle.md
.aiassistant/records/aiscc/cycles/20260831_1619_aiscc-p1-8-next-action-context-source-authority-final-acceptance-1.cycle.md
.aiassistant/records/aiscc/cycles/20260831_1619_aiscc-p1-8-next-action-context-source-authority-human-final-review-recommendation-1.cycle.md
.aiassistant/reports/aiscc/20260831_1619_aiscc-p1-8-next-action-context-accepted-prerequisite-design-resume-handoff-1.md
.aiassistant/tasks/done/20260831_1143_aiscc-p1-8-memory-next-action-authority-and-terminal-epoch-runtime-rework-1.md
.aiassistant/tasks/done/20260831_1332_aiscc-p1-8-historical-replay-and-system-owner-capability-runtime-rework-1.md
.aiassistant/tasks/done/20260831_1332_aiscc-p1-8-prerequisite-owner-authority-contract-design-freeze-1.md
.aiassistant/tasks/done/20260831_1332_aiscc-p1-8-prerequisite-owner-authority-exact-contract-design-rework-1.md
.aiassistant/tasks/done/20260831_1514_aiscc-p1-8-next-action-context-ranking-authority-compatibility-design-rework-1.md
.aiassistant/tasks/done/20260831_1514_aiscc-p1-8-next-action-context-source-authority-design-freeze-1.md
.aiassistant/tasks/done/20260831_1619_aiscc-p1-8-next-action-context-source-authority-terminal-acceptance-persistence-1.md
```

Commit B must contain no:

```text
src/**
tests/**
migrations/**
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
.aiassistant/reports/target/**
```

19개 committed blob 전부를 Commit B tree에서 path-preserving, byte-preserving export한다. Working-tree copy로 대체하지 않는다.

Mismatch:

```text
COMMIT_B_TERMINAL_GOVERNANCE_ALLOWLIST_MISMATCH
```

---

# 12. terminal semantic verification

Commit B tree의 Cycle/state/handoff에서 다음이 동시에 유지돼야 한다.

```text
P1-8 NEXT_ACTION_CONTEXT Source Authority Design
→ HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-8 prerequisite owner-authority design
→ BLOCKED_REQUIRED_EVIDENCE / NEXT_ACTION

P1-8 Runtime
→ BLOCKED_REQUIRED_EVIDENCE

blocked runtime
→ 19 paths / 84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42

P2/P3
→ NOT_STARTED

PUBLIC_BOUNDED_LIVE
→ NOT_RELEASED
```

Acceptance가 prerequisite candidate 또는 Runtime으로 확장돼 있으면:

```text
TERMINAL_STATE_SCOPE_EXPANSION_MISMATCH
```

---

# 13. residual worktree verification

Task lifecycle move 전에 current worktree를 다시 검사한다.

Expected uncommitted set:

```text
19 blocked P1-8 runtime source/test/migration paths
+
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
```

Runtime 19개 path는 1619 export manifest의 per-file SHA inventory와 각각 같아야 한다. Ordinal path sort 후 다음 serialization으로 aggregate를 재계산한다.

```text
<path>\t<lowercase_sha256>\n
```

Expected aggregate:

```text
84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42
```

Prerequisite candidate expected SHA:

```text
556faad8a77d917fcbfc9ab7b0ba62bd65f985a6f4a1e585c08af668dd14393c
```

Index는 empty여야 하고 unexpected dirty path는 없어야 한다.

Mismatch:

```text
REVIEWED_RESIDUAL_CANDIDATE_DRIFT
or
DIRTY_WORKSPACE_MIXED
```

---

# 14. correction provenance clarification

1619 Executor report의 다음 문장을 exact하게 확인한다.

```text
The prior missing recommendation Cycle was supplied and
the unlisted 0813 done Task was removed before resume.
```

보고서에 다음을 기록한다.

1. supplied recommendation Cycle의 exact path와 현재 Commit B blob SHA-256
2. 그것이 Commit B exact allowlist에 포함됐는지
3. removed 0813 done Task의 exact path
4. 제거 직전 tracked/untracked 분류가 available evidence로 확인 가능한지
5. 제거가 Commit A/B deletion으로 들어가지 않았는지
6. 확인 불가능한 항목은 추측하지 않고 `NOT_VERIFIABLE_FROM_CURRENT_GIT_STATE`로 표시

이 항목만으로 과거 상태를 재구성하기 위해 reflog, 삭제 복구, filesystem forensic 범위를 넓히지 않는다.

---

# 15. evidence contract

executor_required:

- `STATIC_SOURCE`: exact canonical terminal semantics
- `PUBLIC_PROVENANCE`: Commit A/B object, parent, changed-path and blob evidence
- `STATIC_SOURCE`: current residual 19-path/prerequisite identity
- `SOURCE_EVIDENCE_EXPORT`: Commit A one blob + Commit B 19 blobs

reuse_allowed:

- 1619 export manifest per-file runtime hashes는 expected identity로만 재사용
- accepted Human text와 exact accepted design SHA는 predecessor authority로 재사용

human_owned:

- 이 audit bundle에 대한 Command Center final judgment
- prerequisite exact-contract design에 대한 future Human acceptance

not_required:

- unit/integration/PostgreSQL/runtime test rerun
- provider/network/browser/deployment evidence

forbidden:

- source mutation
- Git index/commit/push/history mutation
- runtime resume

proof_non_substitution:

```text
Executor report != Git object evidence
GIT_PROVENANCE.md narrative != independently recomputed commit object identity
committed terminal design != accepted P1-8 Runtime
runtime manifest aggregate != current runtime bytes unless per-file hashes are rechecked
```

---

# 16. mandatory stop

첫 mismatch 발견 후 source/history를 보정하지 않는다.

허용되는 후속 행동은:

```text
minimal read-only evidence
workspace inventory
audit report/export
safe stop
```

Stop codes:

```text
CANONICAL_HEAD_ADVANCED_OR_DIVERGED
TERMINAL_COMMIT_OBJECT_OR_LINEAGE_MISMATCH
COMMIT_A_ACCEPTED_DESIGN_BOUNDARY_MISMATCH
COMMIT_B_TERMINAL_GOVERNANCE_ALLOWLIST_MISMATCH
TERMINAL_STATE_SCOPE_EXPANSION_MISMATCH
REVIEWED_RESIDUAL_CANDIDATE_DRIFT
DIRTY_WORKSPACE_MIXED
BLOCKED_MISSING_ARTIFACT
```

---

# 17. audit export bundle

Target:

```text
.aiassistant/reports/target/
20260901_1527_aiscc-p1-8-next-action-context-terminal-canonical-git-reconciliation-audit-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
GIT_OBJECT_EVIDENCE.md
COMMIT_A_OBJECT.raw
COMMIT_B_OBJECT.raw
```

Required path-preserved committed blob copies:

- Commit A exact accepted design blob 1개
- Commit B exact terminal-governance blob 19개

`EXPORT_MANIFEST.md`에 다음을 기록한다.

- repository/branch/HEAD
- initial/final index and worktree classification
- Commit A/B object SHA recomputation
- exact parents
- Commit A/B changed-path lists and counts
- each source commit/path/blob object id
- each exported copy SHA-256 and mismatch count
- terminal semantic checks
- residual runtime per-file hashes and recomputed aggregate
- prerequisite candidate SHA
- secret-signature scan result without secret values
- UTF-8/control-character/Markdown validation

Runtime 19개 bytes와 prerequisite candidate bytes는 복사하지 않는다.

---

# 18. Task lifecycle and final workspace

모든 audit evidence를 수집한 뒤 current Task를:

```text
.aiassistant/tasks/active/
20260901_1527_aiscc-p1-8-next-action-context-terminal-canonical-git-reconciliation-audit-1.md
```

에서:

```text
.aiassistant/tasks/done/
20260901_1527_aiscc-p1-8-next-action-context-terminal-canonical-git-reconciliation-audit-1.md
```

로 이동한다.

이 lifecycle path를 stage/commit하지 않는다.

Final status expected:

```text
index = empty
19 blocked runtime paths
+ prerequisite candidate
+ current audit done Task
```

그 외 unexpected path가 있으면 보고한다.

---

# 19. accept 기준

모두 충족해야 한다.

```text
HEAD == Commit B
Commit A/B object SHA and parent lineage exact
Commit A changed path == accepted design only
Commit A blob SHA exact
Commit B changed paths == exact 19 allowlist
Commit B prohibited paths absent
all 20 committed blobs exported byte-preserving with zero mismatch
terminal Cycle/state/handoff scope exact
runtime residual 19-path aggregate exact
prerequisite candidate SHA exact and uncommitted
index empty
unexpected dirty path absent before audit Task lifecycle move
no forbidden action
```

Expected audit result:

```text
STATE_A_VERIFIED / COMMAND_CENTER_FINAL_REVIEW_READY
```

---

# 20. hold 기준

하나라도 충족되지 않으면:

```text
STATE_A_NOT_VERIFIED / HOLD_RECONCILIATION_REQUIRED
```

exact mismatch만 보고하고 correction을 수행하지 않는다.

---

# 21. 최종 응답 형식

1. result: `STATE_A_VERIFIED` 또는 `STATE_A_NOT_VERIFIED`
2. Task path / done path
3. target audit bundle path
4. actual HEAD and lineage
5. Commit A result
6. Commit B result
7. terminal semantic result
8. residual candidate result
9. correction provenance clarification
10. forbidden-not-run
11. unverified items
12. preserved exact paths

P1-8 Runtime resume 또는 prerequisite design implementation을 이번 응답에서 시작하지 않는다.
