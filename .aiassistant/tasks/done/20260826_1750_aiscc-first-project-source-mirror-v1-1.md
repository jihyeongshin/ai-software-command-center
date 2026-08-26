# 작업지시서: P0-5 First Project Source Mirror v1

## meta

- task_id: `20260826_1750_aiscc-first-project-source-mirror-v1-1`
- created_at: `2026-08-26 17:50 KST`
- phase: `P0-5 — First Project Source Mirror v1`
- work_type: `PROJECT_SOURCE_MIRROR_SYNC`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `repository canonical → Browser Project Source read-only mirror`
- predecessor_phase: `P0-4 Repository Bootstrap / Canonical Authority / Git Policy`
- predecessor_status: `ACCEPTED / CLOSED`
- predecessor_closure_commit: `c2187378857c0b13a372235e90cb279ca4b826fa`
- current_browser_source: `AISCC-BOOTSTRAP-SEED-V1 / 14 of 14`
- expected_executor_result: `COMPLETED / COMMAND_CENTER_REVIEW_PENDING`
- expected_command_center_candidate_after_review: `ACCEPTED_PENDING_SOURCE_MIRROR_SYNC`
- human_owned_sync: `Browser Project complete active-set replacement`
- P1_status: `NOT_STARTED`

## 현재 상태

P0-4는 Human/Command Center final judgment와 closure persistence까지 `ACCEPTED / CLOSED`다.

Current accepted repository state:

```text
repository_root:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

accepted P0-4 closure commit:
c2187378857c0b13a372235e90cb279ca4b826fa

repository local canonical:
ACCEPTED EDITABLE SOURCE OWNER

Browser Project Source:
AISCC-BOOTSTRAP-SEED-V1 14/14
ACTIVE TEMPORARY SOURCE

P0-5:
NOT_STARTED / NEXT
```

이번 Task의 목적은 accepted repository canonical snapshot으로부터 최초 read-only Project Source mirror v1을
재현 가능하게 생성하고 검증하는 것이다.

이번 Task는 Browser Project Source를 직접 변경하지 않는다.

```text
Executor
→ manifest / generator / generated mirror candidate / evidence

Command Center
→ candidate judgment

Human
→ Seed 14개 전체 제거 + accepted mirror active set 전체 업로드

Human confirmation
→ P0-5 terminal closure
```

## 핵심 authority invariant

```text
repository local canonical
= EDITABLE SOURCE OWNER

generated mirror bundle
= IGNORED TRANSPORT ARTIFACT

Browser Project Source
= HUMAN-UPLOADED READ-ONLY MIRROR

Seed v1 + mirror v1 mixed active authority
= FORBIDDEN
```

P0-5 Human sync 완료 전까지 Browser Project의 Seed 14/14는 삭제하거나 수정하지 않는다.

## 실행 전 필수 preflight

mutation 전에 다음을 exact 확인한다.

1. repository root:
   `C:\Users\oracl\IdeaProjects\ai-software-command-center`
2. branch:
   `main`
3. `HEAD == c2187378857c0b13a372235e90cb279ca4b826fa`
4. origin fetch/push:
   `https://github.com/jihyeongshin/ai-software-command-center.git`
5. extra remote:
   none
6. unrelated tracked/staged mutation:
   none
7. 이 Task exact active path 존재
8. P0-4 final acceptance Cycle 존재:
   `.aiassistant/records/aiscc/cycles/20260826_1655_aiscc-p0-4-repository-bootstrap-final-acceptance-1.cycle.md`
9. current state에서 P0-4 `ACCEPTED / CLOSED`, P0-5 `NOT_STARTED / NEXT`
10. Browser Project Source sync를 사람이 완료했다고 표시한 evidence가 아직 없음

불일치하면 추정, reset, pull, reconstruction을 하지 말고:

```text
BLOCKED_REPOSITORY_PRECONDITION_DRIFT
```

로 중단한다.

허용 Git inspection:

```text
git status
git status --short
git branch --show-current
git rev-parse HEAD
git remote -v
git ls-files
git log --oneline --decorate -n 10
git diff
git diff --check
git show
```

remote network action은 금지한다.

## 이번 턴 목표

1. first active Project Source set을 exact `18`개 canonical file로 고정한다.
2. tracked machine-readable manifest를 생성한다.
3. tracked deterministic generator를 생성한다.
4. accepted closure commit `c218737...`의 canonical snapshot만 사용하여 mirror v1 candidate를 생성한다.
5. generated mirror body가 canonical body와 byte-for-byte 동일함을 검증한다.
6. canonical SHA-256, mirror body SHA-256, filename, file count, duplicate, UTF-8, Markdown, secret/private exclusion을 검증한다.
7. Project Source Bundle Registry를 first bundle candidate 상태로 갱신한다.
8. Current State를 Executor candidate / Command Center review pending 상태로만 갱신한다.
9. Task를 `tasks/done`으로 이동한다.
10. tracked P0-5 implementation/provenance 변경을 local additive commit 1개로 보존한다.
11. ignored mirror bundle과 upload-only ZIP을 review/export artifact로 제출한다.
12. Browser Project Source replacement는 Human-owned `HUMAN_PENDING`으로 남긴다.

## 이번 턴 비목표

- Browser Project Source 파일 삭제/업로드/부분교체
- Bootstrap Seed retirement 완료 주장
- P0-5 `ACCEPTED / CLOSED` 주장
- P1-1 또는 product/runtime implementation
- state machine/security/sandbox implementation
- deployment
- Cloudflare/Railway/OpenAI provider resource 설정
- API key/credential/billing/spend limit 설정
- public URL 생성
- Git remote fetch/pull/push
- current provider pricing/capability 검증
- existing accepted product/prior-art/runtime baseline 수정
- source mirror active set에 tasks/done, Cycle, raw report, private source를 추가

## canonical snapshot contract

First mirror v1의 body source는 **현재 working tree가 아니라 accepted P0-4 closure snapshot**으로 고정한다.

```text
canonical_commit:
c2187378857c0b13a372235e90cb279ca4b826fa
```

Mirror generation 시작 전 18개 active canonical path가 `HEAD`와 byte-identical이어야 한다.

Generator는 active canonical body를 읽기 전에:

```text
git diff --quiet c2187378857c0b13a372235e90cb279ca4b826fa -- <18 active canonical paths>
```

또는 동등한 per-path local verification으로 snapshot drift가 `0`임을 증명한다.

P0-5 Task 중 이후 `CURRENT_STATE_SUMMARY.md`가 candidate status로 갱신되더라도,
**mirror v1 body와 manifest canonical SHA-256은 accepted closure commit snapshot을 계속 가리킨다.**

즉:

```text
mirror v1
= accepted P0-4 canonical snapshot
!= P0-5 post-execution working tree
```

이를 report/manifest에 명시한다.

## first active set — exact 18 files

다음 mapping은 이번 first mirror v1의 exact active set이다.
Task가 임의 추가/삭제/rename하지 않는다.

| no | project_source_filename | canonical_path | group | role |
|---:|---|---|---|---|
| 1 | `00_AISCC_STATE__CURRENT_STATE_SUMMARY.md` | `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md` | STATE | accepted project/phase/authority snapshot |
| 2 | `01_AISCC_STATE__DECISION_REGISTER.md` | `.aiassistant/records/aiscc/DECISION_REGISTER.md` | STATE | accepted decision and deferred implementation boundary |
| 3 | `02_AISCC_STATE__NEXT_ACTIONS.md` | `.aiassistant/records/aiscc/NEXT_ACTIONS.md` | STATE | stable canonical queue and release invariant |
| 4 | `10_AISCC_RULES__AGENTS.md` | `.aiassistant/rules/AISCC_AGENTS.md` | RULES | instruction transport vs project authority |
| 5 | `11_AISCC_RULES__EXECUTOR_REPORT_EXPORT.md` | `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md` | RULES | executor lifecycle/report/export |
| 6 | `12_AISCC_RULES__ASSET_GIT_AND_ENCODING_POLICY.md` | `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md` | RULES | tracked/ignored/provenance/encoding |
| 7 | `13_AISCC_RULES__PROJECT_SOURCE_MIRROR.md` | `.aiassistant/rules/AISCC_PROJECT_SOURCE_MIRROR.md` | RULES | canonical/mirror lifecycle |
| 8 | `14_AISCC_RULES__DOCUMENT_LANGUAGE_POLICY.md` | `.aiassistant/rules/AISCC_DOCUMENT_LANGUAGE_POLICY.md` | RULES | Korean-first and claim wording policy |
| 9 | `20_AISCC_COMMAND_CENTER__README.md` | `.aiassistant/records/command-center/README.md` | COMMAND_CENTER | command-center artifact chain |
| 10 | `21_AISCC_COMMAND_CENTER__WORKFLOW.md` | `.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md` | COMMAND_CENTER | Task/Evidence/Judgment/Cycle workflow |
| 11 | `22_AISCC_COMMAND_CENTER__TASK_FILE_TEMPLATE.md` | `.aiassistant/records/command-center/TASK_FILE_TEMPLATE.md` | COMMAND_CENTER | Task Contract template |
| 12 | `23_AISCC_COMMAND_CENTER__SHORT_EXECUTOR_PROMPT_TEMPLATE.md` | `.aiassistant/records/command-center/SHORT_EXECUTOR_PROMPT_TEMPLATE.md` | COMMAND_CENTER | short IDE transport prompt |
| 13 | `24_AISCC_COMMAND_CENTER__JUDGMENT_RUBRIC.md` | `.aiassistant/records/command-center/JUDGMENT_RUBRIC.md` | COMMAND_CENTER | evidence/admission/judgment criteria |
| 14 | `25_AISCC_COMMAND_CENTER__CYCLE_RECORD_TEMPLATE.md` | `.aiassistant/records/command-center/CYCLE_RECORD_TEMPLATE.md` | COMMAND_CENTER | durable Cycle template |
| 15 | `26_AISCC_COMMAND_CENTER__NEXT_ACTION_SELECTION_RUBRIC.md` | `.aiassistant/records/command-center/NEXT_ACTION_SELECTION_RUBRIC.md` | COMMAND_CENTER | next-action ordering |
| 16 | `30_AISCC_BASELINE__PRODUCT_THESIS.md` | `.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md` | BASELINE | accepted product thesis |
| 17 | `31_AISCC_BASELINE__PRIOR_ART_BOUNDARY.md` | `.aiassistant/reports/aiscc/AISCC_PRIOR_ART_BOUNDARY.md` | BASELINE | prior-art / DO-NOT-CLAIM boundary |
| 18 | `32_AISCC_BASELINE__COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md` | `.aiassistant/reports/aiscc/AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md` | BASELINE | public Replay/Live/runtime boundary |

### explicitly excluded from active set

```text
AGENTS.md
.gitignore

.aiassistant/tasks/**
.aiassistant/records/aiscc/cycles/**
.aiassistant/records/aiscc/bootstrap/**
.aiassistant/reports/target/**
.aiassistant/project-sources/manifests/**
.aiassistant/project-sources/PROJECT_SOURCE_BUNDLE_REGISTRY.md
.aiassistant/project-sources/bundles/**

raw Executor report
Bootstrap Seed source files
product/runtime source
screenshots/build/cache
secret/private/company/customer material
```

Tracking 여부와 Browser active set 포함 여부를 혼동하지 않는다.

## manifest contract

Tracked manifest exact path:

```text
.aiassistant/project-sources/manifests/aiscc-project-source-mirror-v1.json
```

JSON UTF-8 no BOM.

최소 schema:

```json
{
  "bundle_id": "AISCC-PROJECT-SOURCE-MIRROR-V1",
  "target_gpt_project": "AI Software Command Center",
  "project_scope": "AISCC Browser Command Center canonical read-only mirror",
  "canonical_commit": "c2187378857c0b13a372235e90cb279ca4b826fa",
  "generated_by_task": "20260826_1750_aiscc-first-project-source-mirror-v1-1",
  "expected_active_count": 18,
  "source_mirror_sync_status": "PENDING_HUMAN_COMPLETE_REPLACEMENT",
  "mapping": []
}
```

각 `mapping` item은 최소 다음을 가진다.

```json
{
  "project_source_filename": "...",
  "canonical_path": "...",
  "group": "...",
  "role": "...",
  "canonical_sha256": "...",
  "upload_status": "GENERATED_CANDIDATE"
}
```

금지:

- path를 absolute local path로 기록
- secret/token/credential 포함
- canonical commit을 post-P0-5 candidate commit으로 바꾸기
- upload status를 Human 확인 전 `UPLOADED` 또는 `SYNCED`로 표시

## generator contract

Tracked generator exact path:

```text
scripts/generate_project_source_bundle.ps1
```

이 Task에서는 Python 설치를 요구하거나 수행하지 않는다.

Generator 요구:

1. Windows PowerShell/.NET 기본 기능만으로 실행 가능
2. manifest를 single source로 읽음
3. repository root와 manifest path를 explicit parameter 또는 deterministic repository-relative path로 사용
4. output root:

```text
.aiassistant/project-sources/bundles/aiscc/AISCC-PROJECT-SOURCE-MIRROR-V1/
```

5. output root를 매 generation 전에 안전하게 비우고 manifest-listed 18개만 생성
6. source file을 UTF-8로 decode 검증
7. canonical SHA-256을 manifest 값과 비교
8. duplicate output filename / duplicate canonical path 차단
9. path traversal 차단
10. output metadata는 UTF-8 no BOM
11. metadata 뒤 canonical body는 **byte-for-byte literal copy**
12. body를 PowerShell string interpolation으로 재작성하지 않음
13. source canonical file을 수정하지 않음
14. generated bundle은 ignored path로 유지
15. nonzero/fail-closed exit on mismatch

### generated mirror metadata

각 generated `.md` 최상단에는 deterministic metadata와 body-start marker를 둔다.

예:

```text
# AISCC Project Source Mirror Metadata

- mirror_type: `GPT_PROJECT_SOURCE_READ_ONLY_MIRROR`
- canonical_path: `<repository-relative canonical path>`
- project_source_filename: `<filename>`
- canonical_owner: `AISCC repository`
- mirror_owner: `AI Software Command Center Browser Project`
- mirror_generated_by_task: `20260826_1750_aiscc-first-project-source-mirror-v1-1`
- canonical_commit: `c2187378857c0b13a372235e90cb279ca4b826fa`
- canonical_sha256: `<sha256>`
- authority: `READ_ONLY_MIRROR`
- do_not_edit_in_project_source: `true`

<!-- AISCC_CANONICAL_BODY_START -->
<canonical body bytes exactly>
```

`AISCC_CANONICAL_BODY_START` 뒤의 byte sequence가 canonical source file bytes와 완전히 같아야 한다.

## Registry update contract

Tracked:

```text
.aiassistant/project-sources/PROJECT_SOURCE_BUNDLE_REGISTRY.md
```

기존 authority/ownership boundary는 유지한다.

`registered bundles`에 다음 candidate를 추가한다.

```text
bundle_id:
AISCC-PROJECT-SOURCE-MIRROR-V1

manifest:
.aiassistant/project-sources/manifests/aiscc-project-source-mirror-v1.json

canonical_commit:
c2187378857c0b13a372235e90cb279ca4b826fa

status:
GENERATED_CANDIDATE / COMMAND_CENTER_REVIEW_PENDING

browser_sync:
NOT_EXECUTED / HUMAN_PENDING
```

Current state도 다음 의미로만 보정한다.

```text
first tracked mirror manifest: GENERATED_CANDIDATE
first generated mirror bundle: GENERATED_CANDIDATE
Browser complete active-set replacement: NOT_EXECUTED / HUMAN_PENDING
source mirror sync status: COMMAND_CENTER_REVIEW_PENDING
```

Seed retirement을 완료로 표시하지 않는다.

## Current State update contract

Tracked:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
```

Executor turn 종료 시 다음 의미를 기록한다.

```text
P0-4:
ACCEPTED / CLOSED

P0-5:
EXECUTOR_CANDIDATE / COMMAND_CENTER_REVIEW_PENDING

mirror snapshot canonical commit:
c2187378857c0b13a372235e90cb279ca4b826fa

generated candidate active files:
18

Browser Project Source:
AISCC-BOOTSTRAP-SEED-V1 14/14 still active

Human complete replacement:
HUMAN_PENDING

P1-1:
NOT_STARTED
```

`ACCEPTED_PENDING_SOURCE_MIRROR_SYNC` 또는 `ACCEPTED / CLOSED`는 Executor가 직접 기록하지 않는다.

## generated upload package

Review/Human upload 편의를 위해 exact 18 generated Markdown만 포함하는 upload-only ZIP을 만든다.

Filename:

```text
20260826_1750_aiscc-project-source-mirror-v1-upload-only.zip
```

ZIP contract:

- root wrapper directory 없음
- exact 18 `.md`
- extra manifest/report/task 없음
- `__MACOSX` 없음
- canonical filenames are the exact project_source_filename values
- ZIP SHA-256 report

이 ZIP 자체는 Git track하지 않는다.

## evidence contract

### executor_required

#### `REPOSITORY_PREFLIGHT`

Pass:

- exact root/main/HEAD/origin
- no extra remote
- clean tracked/staged state except current ignored active Task transport
- P0-4 closed state confirmed

#### `ACTIVE_SET_SOURCE_SNAPSHOT`

Pass:

- exact 18 canonical paths exist
- exact 18 output filenames unique
- source paths unique
- all 18 paths byte-identical to `c218737...`
- no active source outside exact table

#### `MANIFEST_INTEGRITY`

Pass:

- JSON parse
- bundle/target/canonical commit/task IDs exact
- expected count `18`
- mapping actual `18`
- mapping filename/path uniqueness
- each `canonical_sha256` independently recomputed and matched
- no absolute path
- no unexpected extra field that carries private/credential value

#### `GENERATOR_EXECUTION`

Pass:

- generator exits success
- generated actual count `18`
- no extra generated file
- output names exact
- generator rerun is deterministic for file bytes
- generated bundle stays Git ignored

#### `MIRROR_BODY_INTEGRITY`

For all `18/18`:

```text
metadata canonical_path == manifest canonical_path
metadata canonical_commit == c218737...
metadata canonical_sha256 == manifest canonical_sha256
body bytes after AISCC_CANONICAL_BODY_START
== source canonical bytes
```

#### `DOCUMENT_INTEGRITY`

For canonical + generated mirror + manifest + generator:

- expected UTF-8 decode where applicable
- no unintended BOM in generated text
- Markdown fence parity for generated mirror body/file
- no unexpected control character
- `git diff --check` PASS on tracked changes

#### `PRIVATE_SECRET_EXCLUSION`

Scoped static scan:

- no `.env`, key, token, cookie, private key path admitted
- no Bootstrap staging source accidentally admitted
- no private/company/customer repository source
- report values, if any, must not print secret values

This is static exclusion proof only, not comprehensive security proof.

#### `UPLOAD_ONLY_ZIP_INTEGRITY`

Pass:

- ZIP exact 18 entries
- root wrapper none
- filenames exact
- each entry byte-identical to generated mirror file
- extra file `0`
- ZIP SHA-256 recorded

#### `GIT_LOCAL_PROVENANCE`

All required proof PASS 후:

tracked changes expected:

```text
scripts/generate_project_source_bundle.ps1
.aiassistant/project-sources/manifests/aiscc-project-source-mirror-v1.json
.aiassistant/project-sources/PROJECT_SOURCE_BUNDLE_REGISTRY.md
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/tasks/done/20260826_1750_aiscc-first-project-source-mirror-v1-1.md
```

Task active→done lifecycle included.

Allowed tracked changes만 stage하고 local additive commit 1개 생성.

금지:

```text
git commit --amend
git reset
git rebase
git fetch
git pull
git push
```

commit 후 report:

- base canonical snapshot commit `c218737...`
- P0-5 candidate commit
- exact committed paths
- remote action `FORBIDDEN_NOT_RUN`

### human_owned

#### `BROWSER_PROJECT_COMPLETE_REPLACEMENT`

Scope:

```text
Browser Project:
AI Software Command Center
```

Human action:

1. Command Center가 먼저 P0-5 candidate를 `ACCEPTED_PENDING_SOURCE_MIRROR_SYNC`로 판정할 때까지 기다린다.
2. Browser Project Source의 Seed 14개를 전체 제거한다.
3. accepted mirror v1 exact 18개를 전체 업로드한다.
4. Seed file과 mirror file이 mixed active 상태로 남지 않았는지 확인한다.
5. active file count `18` 확인한다.
6. 사람이 sync 완료를 Browser Command Center에 보고한다.

Expected Human result:

```text
source mirror sync 완료.

browser project:
AI Software Command Center

bundle:
AISCC-PROJECT-SOURCE-MIRROR-V1

canonical commit:
c2187378857c0b13a372235e90cb279ca4b826fa

active files replaced:
18

Seed v1 active files remaining:
0

mirror v1 active files:
18

metadata/hash 확인:
complete
```

Executor는 이 proof를 수행·완료 주장하지 않는다.

### reuse_allowed

- P0-4 accepted repository/canonical/Git policy evidence:
  unchanged scope에 한해 `REUSED_ACCEPTED`
- P0-4 final Human acceptance:
  accepted Cycle provenance로 재사용
- Browser Seed 14/14 active confirmation:
  current pre-sync Human-provided state로만 재사용

현재 generated mirror/hash proof는 predecessor proof로 대체할 수 없다.

### not_required

- product build/test
- DB/HTTP/browser runtime
- state machine runtime
- security sandbox runtime
- provider/model inference
- deployment
- API key/billing
- public URL

### forbidden

- Browser Project Source mutation by Executor
- human sync 완료 claim
- Seed partial replacement
- P1 implementation
- remote Git action
- provider/deployment/billing action
- accepted baseline semantic mutation
- active set expansion beyond exact 18

## proof non-substitution

```text
manifest exists
!= generated bundle verified

generated bundle verified
!= Browser Project Source uploaded

Browser upload
!= complete replacement unless Seed remaining == 0 and mirror active count == 18

P0-5 Executor candidate
!= Command Center acceptance

ACCEPTED_PENDING_SOURCE_MIRROR_SYNC
!= P0-5 CLOSED

mirror body source commit c218737...
!= P0-5 candidate commit

static secret exclusion
!= runtime security proof
```

## Command Center accept 기준

Executor bundle review 후 다음이 모두 맞으면:

```text
ACCEPTED_PENDING_SOURCE_MIRROR_SYNC
```

후보로 판정할 수 있다.

- exact active set 18
- manifest integrity PASS
- generator deterministic execution PASS
- 18/18 body hash/literal copy PASS
- upload-only ZIP exact 18
- tracked registry/current-state/task/generator/manifest changes only
- local additive candidate commit
- no remote/Browser sync/P1/deployment action
- Human sync remains pending

Command Center가 acceptance Cycle을 생성하기 전 Human이 Browser Source를 교체하지 않는다.

## terminal close 기준

P0-5 final:

```text
ACCEPTED / CLOSED
```

는 다음 이후에만 가능하다.

1. candidate `ACCEPTED_PENDING_SOURCE_MIRROR_SYNC`
2. Human complete replacement result 제공
3. Seed remaining `0`
4. mirror active `18`
5. Browser Project Source mixed authority 없음
6. sync provenance가 Cycle에 기록됨

## hold/reject 기준

- canonical snapshot drift
- wrong canonical commit
- exact 18 set 변경
- manifest/body hash mismatch
- output extra/missing
- non-deterministic generated bytes
- generated bundle accidentally tracked
- private/secret/bootstrap-input inclusion
- accepted baseline mutation
- remote Git action
- Executor Browser Source mutation
- Human sync false claim
- partial Seed/mirror mixed replacement

## mandatory stop

다음이면 named blocker로 중단한다.

```text
BLOCKED_REPOSITORY_PRECONDITION_DRIFT
BLOCKED_CANONICAL_SNAPSHOT_DRIFT
BLOCKED_MANIFEST_INTEGRITY
BLOCKED_MIRROR_BODY_MISMATCH
BLOCKED_PRIVATE_OR_SECRET_MATERIAL
POLICY_CONFLICT_INVESTIGATION_REQUIRED
EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

named blocker 이후에는 minimal evidence, workspace inventory, report/export만 수행하고 P1/P0-5 후속 mutation을 하지 않는다.

## report/export

Target:

```text
.aiassistant/reports/target/20260826_1750_aiscc-first-project-source-mirror-v1-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
```

추가 review artifacts:

```text
PROJECT_SOURCE_MIRROR_V1/
  <exact 18 generated Markdown>

20260826_1750_aiscc-project-source-mirror-v1-upload-only.zip
```

changed tracked files는 repository-relative path를 보존하여 포함한다.

Report 필수:

- exact preflight
- canonical snapshot commit
- active set 18 mapping
- read canonical paths
- manifest path/hash
- per-file canonical SHA-256
- generator path and execution
- deterministic rerun result
- generated file count
- 18/18 body integrity
- ZIP exact entries/hash
- registry/current-state changes
- Task lifecycle
- Git candidate commit
- human pending
- Seed 14/14 still active
- Browser mutation forbidden-not-run
- remote action forbidden-not-run
- product/P1/deployment not-required/not-run
- rollback guide
- preserved exact paths
- next recommendation

## rollback / failure semantics

P0-5 candidate commit이 생성된 뒤 Command Center가 HOLD/REJECT하면 history rewrite하지 않는다.

```text
candidate commit
→ HOLD/REJECT Cycle
→ additive rework/revert task
```

generated ignored bundle/ZIP은 cleanup 가능하다.
tracked manifest/registry/current-state/task/generator는 terminal judgment에 따라 additive correction한다.

## 보존 대상

Executor turn 이후 반드시 보존:

```text
.aiassistant/tasks/done/20260826_1750_aiscc-first-project-source-mirror-v1-1.md
.aiassistant/project-sources/manifests/aiscc-project-source-mirror-v1.json
.aiassistant/project-sources/PROJECT_SOURCE_BUNDLE_REGISTRY.md
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
scripts/generate_project_source_bundle.ps1
<P0-5 local candidate commit>
```

Command Center/Human sync 이후 추가 보존:

```text
.aiassistant/records/aiscc/cycles/<P0-5-cycle>.cycle.md
```

Generated bundle과 upload-only ZIP은 Human sync 및 Cycle provenance가 확정된 뒤 재생성 가능하므로 cleanup 가능하다.

## 최종 응답 형식

1. result: `completed / blocked / rejected-candidate`
2. candidate state: `COMMAND_CENTER_REVIEW_PENDING`
3. target bundle path
4. canonical snapshot commit
5. P0-5 candidate commit
6. manifest path/hash
7. generator path
8. generated active count
9. mirror body verification
10. upload-only ZIP/hash
11. human sync: `HUMAN_PENDING`
12. Browser Seed active state: `14/14`
13. forbidden-not-run
14. preserved exact paths
