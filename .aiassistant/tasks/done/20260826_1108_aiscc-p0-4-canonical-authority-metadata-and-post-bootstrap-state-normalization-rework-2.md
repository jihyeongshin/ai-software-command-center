# 작업지시서: P0-4 Canonical Authority Metadata / Post-Bootstrap State Normalization — Narrow Rework

## meta

- task_id: `20260826_1108_aiscc-p0-4-canonical-authority-metadata-and-post-bootstrap-state-normalization-rework-2`
- created_at: `2026-08-26 11:08 KST`
- phase: `P0-4 — Repository Bootstrap / Canonical Authority / Git Policy`
- work_type: `DOC_BASELINE_UPDATE`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `repository-local canonical authority metadata / post-bootstrap wording normalization`
- predecessor_task: `20260826_1038_aiscc-repository-bootstrap-canonical-authority-and-git-policy-rework-1`
- predecessor_candidate_commit: `9e4b100e4adc4b0d1788d4b23b424e34cfe191a6`
- predecessor_judgment: `HOLD_REWORK_REQUIRED`
- predecessor_reject_cause: `POLICY_BASELINE_CONFLICT`
- predecessor_judgment_cycle: `.aiassistant/records/aiscc/cycles/20260826_1108_aiscc-p0-4-canonical-authority-metadata-conflict-hold-1.cycle.md`
- expected_terminal_candidate: `ACCEPTED_CANDIDATE / HUMAN_VERIFICATION_PENDING`
- P0_5_status: `NOT_STARTED`

## 현재 상태

P0-4의 repository/environment bootstrap, Git policy, P0-2 migration, provenance structure,
Decision Register, stable queue, local initial commit은 predecessor Task에서 생성되었다.

Command Center review 결과, Executor scope violation은 없었고 predecessor Task의 literal Seed-body migration
지시 때문에 active repository canonical 문서에 다음 Bootstrap Seed authority wrapper가 그대로 남았다.

```text
# AISCC Bootstrap Seed Metadata
seed_role: PRE_REPOSITORY_BROWSER_PROJECT_BOOTSTRAP
authority: TEMPORARY_BOOTSTRAP_AUTHORITY
```

이 상태는 repository local canonical을 editable source owner로 세우려는 P0-4 목적과 충돌하고,
P0-5가 canonical body를 literal mirror할 경우 stale Bootstrap authority를 Browser Project Source에 다시
복제할 위험이 있으므로 P0-4는 `HOLD_REWORK_REQUIRED`다.

이번 rework는 이 authority metadata conflict와 이미 확정된 post-bootstrap stale wording만 좁게 정규화한다.

## Human-confirmed repository

```text
repository_root:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

origin:
https://github.com/jihyeongshin/ai-software-command-center.git

predecessor_candidate_commit:
9e4b100e4adc4b0d1788d4b23b424e34cfe191a6
```

`git init`, repository recreation, reset, amend, rebase, history rewrite는 금지한다.

## 실행 전 필수 preflight

다음이 모두 맞아야 mutation을 시작한다.

1. repository root가 exact path와 일치한다.
2. branch가 `main`이다.
3. `HEAD`가 exact predecessor commit
   `9e4b100e4adc4b0d1788d4b23b424e34cfe191a6`이다.
4. `origin` fetch/push URL이 exact expected URL과 일치한다.
5. 추가 remote가 없다.
6. predecessor commit 이후 사람이 만든 unrelated tracked/untracked source/config change가 없다.
7. 이 Task File은 exact active path에 존재한다.
8. predecessor HOLD Cycle은 exact canonical cycle path에 존재하며 내용은 수정하지 않는다.

불일치하면 추정·reset·recreate하지 말고:

```text
BLOCKED_REPOSITORY_PRECONDITION_DRIFT
```

로 중단한다.

허용되는 Git inspection은 local read-only command다.

```text
git status
git status --short
git branch --show-current
git rev-parse HEAD
git remote -v
git ls-files
git log --oneline --decorate -n 5
git show
git diff
```

remote network action은 금지한다.

## 이번 턴 목표

1. active repository canonical 12개 문서의 Bootstrap Seed authority wrapper를 repository canonical metadata로 정규화한다.
2. P0-4에서 이미 확정된 사실을 future tense로 남긴 stale wording만 현재형으로 보정한다.
3. historical Bootstrap genesis artifact는 byte-preserving으로 유지한다.
4. accepted P0-2 product/prior-art/public-runtime baseline 내용과 Decision Register/queue decision을 변경하지 않는다.
5. `CURRENT_STATE_SUMMARY.md`에 predecessor HOLD와 이번 narrow corrective candidate 상태를 정확히 반영한다.
6. active canonical authority/stale wording scan을 실행한다.
7. Task를 `tasks/done`으로 이동하고 predecessor HOLD Cycle을 함께 tracked provenance로 포함한다.
8. required evidence가 모두 PASS한 뒤 local corrective commit 1개를 생성한다.
9. P0-5는 실행하지 않는다.

## 이번 턴 비목표

- repository 재생성
- `.git` 재초기화
- initial commit 수정/amend/reset/rebase/history rewrite
- P0-2 substantive content 수정
- product thesis/prior-art/differentiation/runtime decision 재판정
- `AISCC-COMPETITION-PUBLIC-RUNTIME-V1` 변경
- `AISCC-COMPETITION-DEPLOYMENT-DIRECTION-V1` 변경
- `NEXT_ACTIONS.md` queue 재설계
- state machine/product runtime/frontend/backend 구현
- security/sandbox safeguard 설계 또는 구현
- P0-5 manifest/bundle/mirror 생성 또는 Browser Project Source 교체
- deployment/provider resource/API key/billing/spend-limit 설정
- remote Git operation

## 허용 수정 경로

### active canonical metadata + stale wording normalization

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md
.aiassistant/rules/AISCC_PROJECT_SOURCE_MIRROR.md
.aiassistant/rules/AISCC_DOCUMENT_LANGUAGE_POLICY.md

.aiassistant/records/command-center/README.md
.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md
.aiassistant/records/command-center/TASK_FILE_TEMPLATE.md
.aiassistant/records/command-center/SHORT_EXECUTOR_PROMPT_TEMPLATE.md
.aiassistant/records/command-center/JUDGMENT_RUBRIC.md
.aiassistant/records/command-center/CYCLE_RECORD_TEMPLATE.md
.aiassistant/records/command-center/NEXT_ACTION_SELECTION_RUBRIC.md
```

### current state

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
```

### Task lifecycle / provenance

```text
.aiassistant/tasks/active/20260826_1108_aiscc-p0-4-canonical-authority-metadata-and-post-bootstrap-state-normalization-rework-2.md
.aiassistant/tasks/done/20260826_1108_aiscc-p0-4-canonical-authority-metadata-and-post-bootstrap-state-normalization-rework-2.md

.aiassistant/records/aiscc/cycles/20260826_1108_aiscc-p0-4-canonical-authority-metadata-conflict-hold-1.cycle.md
```

### temporary report/export

```text
.aiassistant/reports/target/20260826_1108_aiscc-p0-4-canonical-authority-metadata-and-post-bootstrap-state-normalization-rework-2/**
```

위 경로 외 tracked file mutation은 금지한다.

## 절대 금지 수정 경로

다음은 이번 Task에서 content mutation 금지다.

```text
AGENTS.md
.gitignore

.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md
.aiassistant/reports/aiscc/AISCC_PRIOR_ART_BOUNDARY.md
.aiassistant/reports/aiscc/AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md

.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/records/aiscc/bootstrap/AISCC_BOOTSTRAP_SEED_V1_INDEX.md
.aiassistant/records/aiscc/bootstrap/AISCC_PROJECT_BOOTSTRAP_GENESIS.md

.aiassistant/project-sources/PROJECT_SOURCE_BUNDLE_REGISTRY.md
.aiassistant/project-sources/manifests/**
.aiassistant/project-sources/bundles/**

product/runtime/security/deployment source or config
```

## 읽을 문서

### canonical

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- `.aiassistant/rules/AISCC_PROJECT_SOURCE_MIRROR.md`
- `.aiassistant/rules/AISCC_DOCUMENT_LANGUAGE_POLICY.md`
- `.aiassistant/records/command-center/README.md`
- `.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md`
- `.aiassistant/records/command-center/TASK_FILE_TEMPLATE.md`
- `.aiassistant/records/command-center/SHORT_EXECUTOR_PROMPT_TEMPLATE.md`
- `.aiassistant/records/command-center/JUDGMENT_RUBRIC.md`
- `.aiassistant/records/command-center/CYCLE_RECORD_TEMPLATE.md`
- `.aiassistant/records/command-center/NEXT_ACTION_SELECTION_RUBRIC.md`
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
- `.aiassistant/project-sources/PROJECT_SOURCE_BUNDLE_REGISTRY.md`

### historical provenance — read-only

- `.aiassistant/records/aiscc/bootstrap/AISCC_BOOTSTRAP_SEED_V1_INDEX.md`
- `.aiassistant/records/aiscc/bootstrap/AISCC_PROJECT_BOOTSTRAP_GENESIS.md`
- `.aiassistant/tasks/done/20260826_1038_aiscc-repository-bootstrap-canonical-authority-and-git-policy-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260826_1108_aiscc-p0-4-canonical-authority-metadata-conflict-hold-1.cycle.md`

Task must-read list는 minimum authoritative context set이다.
unrelated source/rules/log를 bulk-read하지 않는다.

## canonical metadata normalization contract

위 12개 active canonical 문서의 기존 Bootstrap Seed wrapper 전체를 다음 repository canonical metadata로 교체한다.

```markdown
# AISCC Repository Canonical Metadata

- canonical_owner: `AISCC_REPOSITORY`
- authority: `REPOSITORY_LOCAL_CANONICAL`
- bootstrap_origin: `AISCC-BOOTSTRAP-SEED-V1`
- canonicalized_by_task: `20260826_1108_aiscc-p0-4-canonical-authority-metadata-and-post-bootstrap-state-normalization-rework-2`

---
```

주의:

- `bootstrap_origin`은 historical provenance다.
- `authority`는 현재 repository-local canonical owner를 의미한다.
- Browser Project Source가 P0-5 전까지 Seed 14/14를 사용한다는 사실과 모순되지 않는다.
- historical bootstrap artifact의 original Seed metadata는 수정하지 않는다.
- canonical metadata 외 substantive body는 stale wording normalization에 필요한 최소 line만 수정한다.

## required stale wording normalization

### 1. `.aiassistant/rules/AISCC_AGENTS.md`

다음을 현재형으로 보정한다.

기존 의미:

```text
Git tracked/ignored 여부는 P0-4 repository bootstrap에서 명시적으로 결정한다.
tracking decision 전에는 ...
향후 canonical template 후보:
repository 생성 후 권위는 ...
예상 owner:
```

현재 의미:

```text
repository-root AGENTS.md는 TRACK되는 thin transport bootstrap이다.
AGENTS.md는 policy authority가 아니다.
root .gitignore와 canonical Git policy는 repository policy owner가 관리한다.
현재 root AGENTS.md transport contract를 설명한다.
repository authority는 의미별 canonical path로 분리되어 있다.
아직 생성되지 않은 future owner 문서는 future target으로 명시한다.
```

root `AGENTS.md` 자체는 수정하지 않는다.

### 2. `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`

기존:

```text
repository-root AGENTS.md의 tracked/ignored 정책은 P0-4 repository bootstrap에서 결정한다.
```

현재:

```text
repository-root AGENTS.md는 TRACK되는 thin transport bootstrap이다.
```

Git index/commit/push는 여전히 active Task의 explicit authorization 없이는 금지한다.

### 3. `.aiassistant/rules/AISCC_PROJECT_SOURCE_MIRROR.md`

다음 stale 문장을 현재 lifecycle로 보정한다.

기존:

```text
현재 Seed v1은 repository 이전의 임시 source set이다.
```

현재 의미:

```text
repository local canonical은 P0-4에서 생성되었다.
Browser Project Source는 P0-5 complete replacement가 Human-confirmed될 때까지
immutable AISCC-BOOTSTRAP-SEED-V1 14/14를 active temporary source로 유지한다.
P0-5 이후 Seed는 historical genesis artifact로 retire한다.
```

lifecycle diagram도 현재 단계가 이해되도록 보정하되,
P0-5 실행·sync 완료를 현재 사실로 쓰지 않는다.

### 4. `.aiassistant/records/command-center/NEXT_ACTION_SELECTION_RUBRIC.md`

기존 section:

```text
## 8. 현재 bootstrap 다음 순서

P0-2
→ P0-3
→ P0-4
→ P0-5
→ P1-1
```

를 post-P0-4 current queue 의미로 보정한다.

최소 의미:

```text
P0-5 First Project Source Mirror v1
→ P1-1 Core Domain / State Machine Design
→ P1-2 Security / Sandbox / Runtime Boundary Design
→ P1-3 Security / Runtime Safeguard Implementation and Verification
```

`NEXT_ACTIONS.md`의 전체 canonical queue를 복제할 필요는 없다.

### 5. 기타 8개 active canonical 문서

Bootstrap Seed wrapper만 repository canonical metadata로 교체한다.
추가 substantive body rewrite는 금지한다.
명백한 P0-4 future-tense residue를 발견하면 mutation 전에 exact line/path를 report하고,
위 1~4와 동일한 post-bootstrap state normalization인지 확인한 뒤 최소 수정한다.
범위를 넓혀 architecture/workflow를 재설계하지 않는다.

## `CURRENT_STATE_SUMMARY.md` update contract

이번 Executor turn 종료 시 다음 의미를 정확히 반영한다.

- P0-4 predecessor candidate는 Command Center에서 `HOLD_REWORK_REQUIRED / POLICY_BASELINE_CONFLICT`.
- current narrow rework는 executor evidence PASS 시
  `ACCEPTED_CANDIDATE / HUMAN_VERIFICATION_PENDING`.
- repository local canonical candidate가 존재한다.
- Browser Project Source는 아직 Seed 14/14이며 P0-5 sync는 `NOT_STARTED`.
- P0-5는 P0-4 Human acceptance 전 실행 불가.
- product/runtime/security/deployment/provider evidence는 여전히 `NOT_EXECUTED` / deferred.

P0-4를 Human acceptance 전에 `ACCEPTED / CLOSED`로 표시하지 않는다.

## evidence contract

### executor_required

#### `WORKSPACE_PREFLIGHT`

Pass 조건:

- exact repository root
- branch `main`
- `HEAD == 9e4b100e4adc4b0d1788d4b23b424e34cfe191a6`
- exact origin, no extra remote
- no unrelated mutation
- Task/Cycle exact path present

#### `ACTIVE_CANONICAL_AUTHORITY_SCAN`

Scope:

```text
.aiassistant/rules/**
.aiassistant/records/command-center/**
```

다음 문자열이 active canonical에 `0`건이어야 한다.

```text
# AISCC Bootstrap Seed Metadata
seed_role: `PRE_REPOSITORY_BROWSER_PROJECT_BOOTSTRAP`
authority: `TEMPORARY_BOOTSTRAP_AUTHORITY`
```

그리고 위 12개 파일 모두 다음을 가져야 한다.

```text
authority: `REPOSITORY_LOCAL_CANONICAL`
bootstrap_origin: `AISCC-BOOTSTRAP-SEED-V1`
```

Historical path는 scan 대상에서 제외한다.

#### `POST_BOOTSTRAP_STALE_WORDING_SCAN`

다음 exact stale phrase가 active canonical에서 `0`건이어야 한다.

```text
Git tracked/ignored 여부는 P0-4 repository bootstrap에서 명시적으로 결정한다.
향후 canonical template 후보:
repository 생성 후 권위는 의미별 canonical path로 분리한다.
repository-root `AGENTS.md`의 tracked/ignored 정책은 P0-4 repository bootstrap에서 결정한다.
현재 Seed v1은 repository 이전의 임시 source set이다.
## 8. 현재 bootstrap 다음 순서
```

변경된 replacement wording이 current repository/browser-source state와 맞는지 source review를 함께 보고한다.

#### `HISTORICAL_BOOTSTRAP_PRESERVATION`

다음 두 파일은 predecessor commit 대비 byte-identical이어야 한다.

```text
.aiassistant/records/aiscc/bootstrap/AISCC_BOOTSTRAP_SEED_V1_INDEX.md
.aiassistant/records/aiscc/bootstrap/AISCC_PROJECT_BOOTSTRAP_GENESIS.md
```

#### `FORBIDDEN_BASELINE_IMMUTABILITY`

다음은 predecessor commit 대비 unchanged여야 한다.

```text
AGENTS.md
.gitignore
.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md
.aiassistant/reports/aiscc/AISCC_PRIOR_ART_BOUNDARY.md
.aiassistant/reports/aiscc/AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/project-sources/PROJECT_SOURCE_BUNDLE_REGISTRY.md
```

#### `DOCUMENT_INTEGRITY`

- UTF-8 decode PASS
- no BOM for newly written Task/Cycle/report
- Markdown fence parity PASS
- unexpected control character none
- `git diff --check` PASS

#### `GIT_LOCAL_PROVENANCE`

모든 위 evidence PASS 후에만:

1. active Task를 `tasks/done`으로 이동
2. allowed tracked changes만 stage
3. local corrective commit 1개 생성

금지:

```text
git commit --amend
git reset
git rebase
git push
git fetch
git pull
history rewrite
```

commit 후 report에:

- predecessor commit
- corrective commit
- committed file count
- changed path list
- remote operation `FORBIDDEN_NOT_RUN`

을 기록한다.

### human_owned

#### `HUMAN_VERIFICATION`

Human/Command Center가 target bundle, diff, scans, corrective commit을 검토한다.

Executor는 최종 P0-4 acceptance를 주장하지 않는다.

### reuse_allowed

- predecessor P0-4 repository preflight, staging input integrity, Git policy, accepted P0-2 migration evidence는
  이번 changed scope와 무관한 범위에 한해 `REUSED_ACCEPTED_CANDIDATE`로 참고 가능하다.
- 이번 authority metadata/stale wording correction의 proof를 predecessor evidence로 대체할 수 없다.

### not_required

- product build
- unit/integration test
- DB/HTTP/browser runtime
- security sandbox runtime
- provider/deployment/billing
- P0-5 mirror generation/sync

### forbidden

- remote Git/network action
- Browser Project Source mutation
- P0-5 execution
- product/runtime/security implementation
- provider/API key/billing/deployment
- history rewrite
- forbidden path mutation

## proof non-substitution

```text
predecessor ACCEPTED_CANDIDATE report
!= current corrected canonical proof

repository path exists
!= canonical authority metadata correct

Seed historical provenance preserved
!= active canonical may retain TEMPORARY_BOOTSTRAP_AUTHORITY

local corrective commit
!= Human P0-4 acceptance

P0-4 acceptance
!= P0-5 mirror sync
```

## accept 기준

Executor candidate accept:

- preflight exact match
- 12 active canonical metadata normalized
- required stale wording corrected
- historical Bootstrap files unchanged
- forbidden baselines unchanged
- authority scan `0` stale hits
- stale wording scan `0` hits
- document integrity PASS
- current state accurately updated
- Task moved to done
- one non-amended local corrective commit created
- P0-5/remote/product/security/deployment actions absent
- target bundle complete

Human/Command Center final acceptance:

- target bundle/diff/evidence/corrective commit independently reviewed
- no semantic drift beyond this Task
- then and only then P0-4 may become `ACCEPTED / CLOSED`

## hold/reject 기준

- repository HEAD/precondition drift
- active canonical still contains temporary Bootstrap authority
- historical Bootstrap record modified
- P0-2/Decision/queue semantic drift
- P0-5 action executed
- remote Git action executed
- history rewrite/amend/reset
- scope expansion outside allowed paths
- Human acceptance falsely claimed

## mandatory stop

다음이면 mutation 중단:

```text
BLOCKED_REPOSITORY_PRECONDITION_DRIFT
POLICY_CONFLICT_INVESTIGATION_REQUIRED
EVIDENCE_SCOPE_EXPANSION_REQUIRED
FORBIDDEN_ACTION_REQUESTED
```

named blocker 후에는 최소 evidence, workspace inventory, report/export와 안전한 종료만 수행한다.

## report/export

Target:

```text
.aiassistant/reports/target/20260826_1108_aiscc-p0-4-canonical-authority-metadata-and-post-bootstrap-state-normalization-rework-2/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
```

Include changed tracked files preserving repository-relative paths.

Deletion이 있을 때만 `REMOVED_FILES.md`.

Report 필수:

- exact preflight
- predecessor commit / result
- read canonical paths
- changed paths
- per-file metadata normalization summary
- stale wording replacements
- active authority scan command/result
- stale wording scan command/result
- historical bootstrap byte-preservation result
- forbidden baseline immutability result
- Task lifecycle
- evidence classification
- forbidden-not-run
- document integrity
- local corrective commit
- human pending
- rollback guide
- preserved exact paths
- next recommendation

## 사람 검증 요구

```text
HUMAN_PENDING
```

Human/Command Center가 다음을 최종 검증한다.

1. active canonical metadata가 repository authority를 정확히 표현하는가.
2. Bootstrap provenance는 historical record로 보존되었는가.
3. stale wording 수정이 현재 상태 정규화에만 한정되었는가.
4. accepted P0-2 / Decision Register / NEXT_ACTIONS semantics가 바뀌지 않았는가.
5. corrective commit이 predecessor history를 rewrite하지 않았는가.
6. P0-5가 실행되지 않았는가.

## 최종 응답 형식

1. result: `completed / blocked / rejected-candidate`
2. result candidate: `ACCEPTED_CANDIDATE / HUMAN_VERIFICATION_PENDING` 또는 blocker
3. target bundle path
4. predecessor commit / corrective commit
5. changed files
6. removed files
7. authority scan result
8. stale wording scan result
9. forbidden baseline immutability
10. human verification
11. unverified/deferred
12. preserved exact paths
