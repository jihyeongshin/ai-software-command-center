# 작업지시서: P0-5 Mirror Snapshot and Metadata Alignment — Narrow Rework

## meta

- task_id: `20260826_2005_aiscc-p0-5-mirror-snapshot-and-metadata-alignment-rework-1`
- created_at: `2026-08-26 20:05 KST`
- phase: `P0-5 — First Project Source Mirror v1`
- work_type: `PROJECT_SOURCE_MIRROR_SYNC`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `pre-sync active-state snapshot correctness / generated mirror metadata`
- predecessor_task: `20260826_1750_aiscc-first-project-source-mirror-v1-1`
- predecessor_candidate_commit: `ae79e0d9b3963c58e69cfa2e96d9a1f778d351d1`
- predecessor_judgment: `HOLD_REWORK_REQUIRED`
- predecessor_reject_cause: `SOURCE_MIRROR_STATE_STALENESS / POLICY_BASELINE_CONFLICT`
- predecessor_hold_cycle: `.aiassistant/records/aiscc/cycles/20260826_2005_aiscc-p0-5-pre-sync-snapshot-staleness-hold-1.cycle.md`
- predecessor_hold_cycle_sha256: `a1b434af0f78d8bb78c637451b4e2d19ed53f0855747a7afc34fae3cd5f77801`
- expected_executor_result: `COMPLETED / COMMAND_CENTER_REVIEW_PENDING`
- Browser_Project_Source_mutation: `FORBIDDEN`
- P1_status: `NOT_STARTED`

## 현재 상태

P0-5 first candidate commit:

```text
ae79e0d9b3963c58e69cfa2e96d9a1f778d351d1
```

은 manifest/generator/body/ZIP integrity 자체는 통과했으나, mirror source snapshot을 P0-4 closure commit
`c218737...`로 고정한 Command Center Task 설계 때문에 Human upload 후 active state가 P0-5 이전으로
회귀하는 문제가 있다.

또한 accepted canonical mirror rule이 요구하는 generated metadata field `mirrored_at`이 first candidate에서 누락됐다.

이번 rework는 위 두 문제만 수정한다.

```text
DO NOT REWRITE HISTORY.
DO NOT TOUCH BROWSER PROJECT SOURCE.
DO NOT START P1.
```

## 실행 전 preflight

다음을 exact 확인한다.

1. repository root:
   `C:\Users\oracl\IdeaProjects\ai-software-command-center`
2. branch: `main`
3. `HEAD == ae79e0d9b3963c58e69cfa2e96d9a1f778d351d1`
4. origin fetch/push:
   `https://github.com/jihyeongshin/ai-software-command-center.git`
5. extra remote: none
6. unrelated tracked/staged mutation: none
7. this Task exact active path exists
8. predecessor HOLD Cycle exact canonical path exists
9. predecessor HOLD Cycle SHA-256 equals:
   `a1b434af0f78d8bb78c637451b4e2d19ed53f0855747a7afc34fae3cd5f77801`
10. Browser Source complete replacement evidence: none
11. current Browser Source remains Seed v1 14/14 according to Human-provided pre-sync state

불일치하면 reset/reconstruct하지 말고:

```text
BLOCKED_REPOSITORY_PRECONDITION_DRIFT
```

로 중단한다.

Remote Git action은 금지한다.

## rework architecture — two local additive commits

이번 Task는 snapshot self-consistency를 위해 **두 개의 additive local commit**을 허용하고 요구한다.

```text
ae79e0d... predecessor candidate

→ Commit A: SYNC_READY_CANONICAL_SNAPSHOT
   active 18 중 stateful canonical 3개만 pre-sync current state로 정규화
   + predecessor HOLD Cycle admission

→ Commit B: REGENERATED_MIRROR_CANDIDATE
   manifest/generator/registry/done Task만 Commit A를 기준으로 갱신
   active 18 body는 Commit A 이후 변경하지 않음
```

Commit A hash가 생성된 뒤에만 manifest/generator의 `canonical_commit`을 Commit A hash로 갱신한다.

Commit B는 active mirror body source 18개를 수정하면 안 된다.

## 이번 턴 목표

1. pre-sync Browser mirror가 P0-5를 `NOT_STARTED`로 되돌리지 않도록 stateful canonical 3개를 정규화한다.
2. sync-ready canonical snapshot Commit A를 만든다.
3. manifest/generator가 Commit A를 exact source snapshot으로 사용하게 한다.
4. generated metadata에 deterministic `mirrored_at`을 추가한다.
5. exact active set 18을 Commit A에서 다시 생성한다.
6. 18/18 body bytes, metadata, SHA-256, deterministic rerun, ZIP을 다시 검증한다.
7. registry를 regenerated candidate / Command Center review pending으로 갱신한다.
8. Task active→done 후 Commit B를 만든다.
9. Browser Project Source replacement는 Human-owned pending으로 유지한다.

## 비목표 / 금지

- accepted P0-2 product/prior-art/runtime baseline 수정
- Decision Register 내용 변경
- canonical queue 전체 재설계
- active set 18 추가/삭제/rename
- Browser Source upload/delete/partial replacement
- Seed retirement 완료 주장
- P0-5 ACCEPTED/CLOSED 주장
- P1-1/product/runtime/security implementation
- deployment/provider/API key/billing
- fetch/pull/push
- reset/amend/rebase/history rewrite

## Phase A — sync-ready canonical snapshot

### 허용 수정 경로

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/rules/AISCC_PROJECT_SOURCE_MIRROR.md
.aiassistant/records/aiscc/cycles/20260826_2005_aiscc-p0-5-pre-sync-snapshot-staleness-hold-1.cycle.md
```

HOLD Cycle은 Human-provided artifact이며 byte-preserving admission만 허용한다.

### `CURRENT_STATE_SUMMARY.md` required meaning

P0-4 상태는 그대로 `ACCEPTED / CLOSED`.

P0-5는 다음 의미를 가져야 한다.

```text
P0-5 First Project Source Mirror v1:
MIRROR_REWORK_CANDIDATE / COMMAND_CENTER_REVIEW_PENDING

mirror generation:
in progress / regenerated candidate required

Browser Project Source:
AISCC-BOOTSTRAP-SEED-V1 14/14 still active

Human complete replacement:
NOT_EXECUTED / HUMAN_PENDING

next after Command Center acceptance:
Human complete replacement

next implementation after P0-5 terminal closure:
P1-1 Core Domain / State Machine Design
```

필수 snapshot note:

```text
This Current State Summary is a repository snapshot used to generate a Browser Project Source mirror.
If it is later read from Browser Project Source, do not re-run P0-5 generation solely because this
snapshot predates the latest Human sync result. Check the latest Human-provided source-sync evidence
and terminal Cycle before selecting the next action.
```

동일 의미를 Korean-first로 작성해도 된다.

### `NEXT_ACTIONS.md` required meaning

canonical queue 순서는 유지한다.

`current next action`만 다음 의미로 정규화한다.

```text
phase: P0-5
current action:
Command Center candidate review
→ if accepted, Human complete Browser Project Source replacement

P1-1:
blocked until P0-5 terminal closure

mirror snapshot guard:
Browser mirror에서 이 snapshot을 읽는 경우,
snapshot의 pre-sync status만 근거로 P0-5 generation을 다시 실행하지 않는다.
latest Human sync evidence / terminal Cycle을 확인한다.
```

P1-2/P1-3 safeguard ordering과 deployment handoff를 변경하지 않는다.

### `AISCC_PROJECT_SOURCE_MIRROR.md` required meaning

lifecycle을 다음 현재 단계로 보정한다.

```text
[COMPLETED] P0-4 repository canonical accepted / closed
→ [CURRENT] P0-5 mirror v1 candidate generation / Command Center review
→ [HUMAN_OWNED AFTER ACCEPTANCE] Seed 14 remove + mirror 18 upload
→ [AFTER HUMAN CONFIRMATION] Seed historical retirement / P0-5 terminal judgment
```

다음 문구가 더 이상 current fact로 존재하면 안 된다.

```text
[NEXT] P0-5 first mirror v1 generation and judgment
```

`mirrored_at`은 required mirror metadata field로 유지한다.

### Phase A evidence

- only 3 active canonical files semantically modified
- HOLD Cycle byte-preserved
- no P0-2/Decision/base policy mutation
- no active-set mapping change
- UTF-8 / Markdown / `git diff --check` PASS

모두 PASS 후 exact allowed paths만 stage하고 local additive Commit A 생성.

Report에:

```text
sync_ready_snapshot_commit:
<40-hex>
```

기록한다.

## Phase B — regenerate mirror from Commit A

Commit A 이후 active set 18개는 수정 금지다.

### canonical snapshot

```text
canonical_commit:
<Commit A exact hash>
```

manifest와 generated metadata의 canonical commit은 모두 Commit A hash여야 한다.

### manifest

Path:

```text
.aiassistant/project-sources/manifests/aiscc-project-source-mirror-v1.json
```

기존 exact active mapping 18 유지.

Update:

- `canonical_commit`: Commit A
- `generated_by_task`:
  `20260826_2005_aiscc-p0-5-mirror-snapshot-and-metadata-alignment-rework-1`
- `generated_at`: rework generation의 단일 fixed offset-aware timestamp
- `source_mirror_sync_status`:
  `PENDING_COMMAND_CENTER_REVIEW`
- 18 `canonical_sha256`: Commit A blob 기준 재계산
- `upload_status`: `REGENERATED_CANDIDATE`

No absolute path / secret / extra active mapping.

### generator

Path unchanged:

```text
scripts/generate_project_source_bundle.ps1
```

Update expected identity to current rework manifest.

Generator MUST:

- use Commit A exact hash
- require exact mapping 18
- accept only `REGENERATED_CANDIDATE`
- verify source working bytes == Commit A blob before generation
- generate exact 18
- body bytes literal copy
- deterministic rerun
- keep output ignored
- fail closed on mismatch

### required metadata

Every generated file MUST include:

```text
mirror_type
canonical_path
project_source_filename
canonical_owner
mirror_owner
mirror_generated_by_task
mirrored_at
canonical_commit
canonical_sha256
authority
do_not_edit_in_project_source
```

`mirrored_at`:

```text
mirrored_at == manifest.generated_at
```

It must be a deterministic fixed value from the manifest, not the generator's wall-clock value on each rerun.

Body marker:

```text
<!-- AISCC_CANONICAL_BODY_START -->
```

Body after marker remains byte-for-byte Commit A canonical blob.

### Registry

`.aiassistant/project-sources/PROJECT_SOURCE_BUNDLE_REGISTRY.md`

Update only current candidate fields:

```text
canonical_commit: <Commit A>
status: REGENERATED_CANDIDATE / COMMAND_CENTER_REVIEW_PENDING
browser_sync: NOT_EXECUTED / HUMAN_PENDING
```

Do not claim accepted/pending-sync yet.

### Current State after Commit A

Do not modify `CURRENT_STATE_SUMMARY.md` during Phase B.

The mirror candidate must represent Commit A exactly.

### Task lifecycle

Task active → done during Phase B.

### upload-only ZIP

Exact filename:

```text
20260826_2005_aiscc-project-source-mirror-v1-rework-upload-only.zip
```

Contract:

- exact 18 root-level Markdown
- no wrapper
- no extra
- no manifest/report/task
- each entry byte-identical to regenerated file
- ZIP SHA-256 report

### Phase B commit

All Phase B proof PASS 후 only:

```text
.aiassistant/project-sources/manifests/aiscc-project-source-mirror-v1.json
.aiassistant/project-sources/PROJECT_SOURCE_BUNDLE_REGISTRY.md
scripts/generate_project_source_bundle.ps1
.aiassistant/tasks/done/20260826_2005_aiscc-p0-5-mirror-snapshot-and-metadata-alignment-rework-1.md
```

를 포함하는 local additive Commit B 생성.

Commit B 이후 clean tracked/staged state 확인.

## exact active set remains 18

Filename/path mapping은 predecessor Task의 exact 18 mapping을 그대로 유지한다.
추가/삭제/rename 금지.

## evidence contract

### executor_required

#### `REPOSITORY_PREFLIGHT`
exact root/main/HEAD/origin/no extra remote/no unrelated mutation.

#### `PHASE_A_SCOPE`
- active semantic modifications exactly 3
- HOLD Cycle byte-preserved
- forbidden canonical baselines unchanged

#### `SYNC_READY_STATE_SCAN`
Active canonical snapshot에서:

```text
P0-5 NOT_STARTED / NEXT
```

current-state 의미가 없어야 한다.

`CURRENT_STATE_SUMMARY`, `NEXT_ACTIONS`, `AISCC_PROJECT_SOURCE_MIRROR`가 모두
P0-5 current review → Human replacement → P1-1-after-closure 방향으로 일치해야 한다.

#### `SYNC_READY_SNAPSHOT_COMMIT`
Commit A additive local commit; no history rewrite.

#### `ACTIVE_SET_SOURCE_SNAPSHOT`
- exact 18
- 18 working bytes == Commit A blobs
- unique filenames/paths
- all SHA values recomputed from Commit A

#### `MANIFEST_INTEGRITY`
- exact task/bundle/target IDs
- canonical commit = Commit A
- expected/mapping 18
- unique/safe paths
- status = pending Command Center review
- canonical SHA 18/18

#### `GENERATOR_EXECUTION`
- exact 18
- rerun deterministic
- ignored output
- nonzero on mismatch

#### `MIRROR_METADATA_INTEGRITY`
18/18:

```text
mirrored_at present
mirrored_at == manifest.generated_at
canonical_commit == Commit A
canonical_sha256 == manifest
authority == READ_ONLY_MIRROR
do_not_edit == true
```

#### `MIRROR_BODY_INTEGRITY`
18/18 body bytes == Commit A blob.

#### `UPLOAD_ONLY_ZIP_INTEGRITY`
exact 18 / no wrapper-extra / byte identity / SHA recorded.

#### `DOCUMENT_INTEGRITY`
UTF-8, no unintended BOM, fence parity, control char, `git diff --check`.

#### `GIT_LOCAL_PROVENANCE`
Commit A + Commit B exact hashes and changed paths; no remote action.

### human_owned

```text
BROWSER_PROJECT_COMPLETE_REPLACEMENT:
HUMAN_PENDING
```

Do not upload or delete Browser Project Source in this Task.

### reuse_allowed

Predecessor technical proof may be reused only for unchanged generator design principles and active-set identity.
All Commit A hash/body/metadata/ZIP proof must be freshly generated.

### not_required

product tests, runtime, DB/HTTP/browser, security sandbox, provider, deployment.

### forbidden

Browser Source mutation, P1, remote Git, deployment/provider/billing, history rewrite.

## proof non-substitution

```text
byte-correct P0-4 snapshot
!= current P0-5 sync-ready mirror

mirror body integrity
!= mirror current-state semantic correctness

generated mirror
!= Human upload

Command Center review pending
!= ACCEPTED_PENDING_SOURCE_MIRROR_SYNC

Human upload
!= terminal closure without Human confirmation evidence
```

## Command Center accept 기준

Rework bundle은 다음 모두 충족 시에만:

```text
ACCEPTED_PENDING_SOURCE_MIRROR_SYNC
```

후보가 된다.

- Commit A state snapshot coherent
- exact 18 unchanged
- mirrored_at 18/18
- Commit A hashes/body 18/18
- deterministic generator
- exact upload-only ZIP
- Commit B tracked scope exact
- no Browser/remote/P1/deployment action
- Human sync pending

## mandatory stop

- precondition drift
- active-set mapping drift
- phase A forbidden baseline mutation
- Commit A 이후 active 18 mutation
- manifest/body mismatch
- metadata required field missing
- private/secret material
- remote/Browser action request

## export bundle

Target:

```text
.aiassistant/reports/target/20260826_2005_aiscc-p0-5-mirror-snapshot-and-metadata-alignment-rework-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
```

Include repository-relative changed files across Commit A and Commit B, HOLD Cycle, and review artifacts:

```text
PROJECT_SOURCE_MIRROR_V1/
  <18 regenerated Markdown>

20260826_2005_aiscc-project-source-mirror-v1-rework-upload-only.zip
```

Report MUST include:

- predecessor candidate commit
- HOLD Cycle hash
- Phase A exact diff
- sync-ready snapshot commit A
- active state semantic scan
- manifest hash
- generator hash
- mirrored_at value
- 18/18 metadata/body result
- ZIP hash
- Phase B candidate commit
- Browser Seed 14/14 still active
- Human sync pending
- forbidden-not-run
- preserved paths

## 보존 대상

- `.aiassistant/tasks/done/20260826_1750_aiscc-first-project-source-mirror-v1-1.md`
- `.aiassistant/tasks/done/20260826_2005_aiscc-p0-5-mirror-snapshot-and-metadata-alignment-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260826_2005_aiscc-p0-5-pre-sync-snapshot-staleness-hold-1.cycle.md`
- `.aiassistant/project-sources/manifests/aiscc-project-source-mirror-v1.json`
- `.aiassistant/project-sources/PROJECT_SOURCE_BUNDLE_REGISTRY.md`
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
- `.aiassistant/rules/AISCC_PROJECT_SOURCE_MIRROR.md`
- `scripts/generate_project_source_bundle.ps1`
- sync-ready snapshot Commit A
- regenerated candidate Commit B

Generated bundle/ZIP remains cleanup-eligible after successful Human sync and durable provenance.

## 최종 응답 형식

1. result
2. target bundle
3. predecessor commit
4. sync-ready snapshot Commit A
5. regenerated candidate Commit B
6. changed paths per phase
7. manifest/generator hashes
8. mirrored_at
9. active 18/hash/body result
10. upload-only ZIP/hash
11. Human sync pending
12. Browser Seed 14/14
13. forbidden-not-run
14. preserved exact paths
