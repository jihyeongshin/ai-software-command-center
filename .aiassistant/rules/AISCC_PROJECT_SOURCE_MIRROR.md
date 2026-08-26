# AISCC Repository Canonical Metadata

- canonical_owner: `AISCC_REPOSITORY`
- authority: `REPOSITORY_LOCAL_CANONICAL`
- bootstrap_origin: `AISCC-BOOTSTRAP-SEED-V1`
- canonicalized_by_task: `20260826_1108_aiscc-p0-4-canonical-authority-metadata-and-post-bootstrap-state-normalization-rework-2`

---


# AISCC Project Source Mirror

## 1. 목적

Local repository canonical을 Browser GPT Project Source에 제공하기 위한 read-only mirror lifecycle을 정의한다.

## 2. Bootstrap Seed lifecycle

repository local canonical candidate는 P0-4에서 생성되었다. Browser Project Source는 P0-5 complete replacement가 Human-confirmed될 때까지 immutable `AISCC-BOOTSTRAP-SEED-V1` `14/14`를 active temporary source로 유지한다. P0-5 이후 Seed는 historical genesis artifact로 retire한다.

```text
[COMPLETED] Seed v1 upload / Browser Project bootstrap
→ [COMPLETED_CANDIDATE] local repository canonical 생성
→ [CURRENT] P0-4 narrow correction / Human verification pending
→ [NEXT_AFTER_P0_4_ACCEPTANCE] P0-5 first mirror v1 생성·판정
→ [HUMAN_OWNED] Browser Project Seed 14개 전체 제거
→ [HUMAN_OWNED] mirror v1 active set 전체 업로드
→ [AFTER_SYNC_CONFIRMATION] Seed v1 historical retirement
```

금지:

- Seed와 mirror v1을 동시에 current authority로 유지
- Seed file을 repository canonical처럼 계속 수정
- 일부 Seed file만 남겨 stale authority 혼합

## 3. canonical / mirror 권위

현재 repository-local canonical / mirror 권위:

- canonical: `.aiassistant/rules/`, `.aiassistant/records/`, `.aiassistant/reports/aiscc/`의 tracked 정본
- manifest: `.aiassistant/project-sources/manifests/`의 tracked active-set definition
- registry: `.aiassistant/project-sources/PROJECT_SOURCE_BUNDLE_REGISTRY.md`
- generated mirror: `.aiassistant/project-sources/bundles/aiscc/`의 ignored upload copy
- Browser Project Source: 사람이 업로드한 read-only copy

Browser Project Source 직접 수정은 canonical 변경이 아니다.

## 4. Git 정책

```text
TRACK
- registry
- manifests
- mirror generator source
- mirror-sync cycle

IGNORE
- generated bundles/aiscc/**
```

Mirror copy 자체보다 **어떤 canonical commit과 manifest로 무엇을 생성·업로드했는가**를 보존한다.

## 5. active set 정책

active Project Source에는 현재 Command Center가 매 turn에 필요한 최소 문서만 둔다.

후보:

- project source index
- core rules
- command-center workflow/templates/rubrics
- current state summary
- decision register
- next actions
- current product/architecture/orchestration/security baselines

기본 active set 제외:

- 모든 `tasks/done`
- 모든 Cycle Record
- raw target bundle/report
- product runtime source
- secret/private material
- screenshots/build/cache

과거 Task/Cycle이 필요하면 selected evidence export 또는 on-demand source로 제공한다. Git 추적 여부와 active Browser Source 포함 여부를 혼동하지 않는다.

## 6. manifest

tracked manifest는 최소 다음을 가진다.

- bundle_id
- target_gpt_project
- project_scope
- canonical_commit
- active file mapping
- optional/on-demand mapping
- expected active count
- upload limit/reserved slots when applicable
- generated_at / generated_by_task
- source mirror sync status

mapping row:

```text
project_source_filename
canonical_path
group
upload_status
role
canonical_sha256
```

## 7. generated mirror filename

```text
<NN>_<GROUP>__<PURPOSE>.md
```

- ASCII uppercase/digit/underscore/hyphen
- directory structure가 사라져도 의미 식별 가능
- canonical path는 metadata에 보존

## 8. mirror metadata

모든 generated mirror 상단:

```text
mirror_type: GPT_PROJECT_SOURCE_READ_ONLY_MIRROR
canonical_path:
project_source_filename:
canonical_owner: AISCC repository
mirror_owner: AI Software Command Center Browser Project
mirror_generated_by_task:
mirrored_at:
canonical_commit:
canonical_sha256:
authority: read-only mirror
do_not_edit_in_project_source: true
```

metadata 뒤에 canonical body를 literal copy한다.

## 9. generator / integrity

권장 generator:

```text
scripts/generate_project_source_bundle.py
```

검증:

- manifest path 존재
- expected/actual count
- duplicate filename/slot 없음
- canonical file missing 없음
- canonical SHA-256 일치
- mirror body SHA-256 일치
- optional file active bundle 혼입 없음
- UTF-8/Markdown fence/control-character 확인
- secret/private path 제외

## 10. sync judgment

향후 P0-5에서 local canonical/manifest/bundle 준비가 완료됐지만 사람이 Browser Source를 교체하지 않았다면:

```text
ACCEPTED_PENDING_SOURCE_MIRROR_SYNC
```

사람은 active set 전체를 complete replacement하고 다음을 보고한다.

```markdown
source mirror sync 완료.

accepted cycle:
<cycle_id>

browser project:
AI Software Command Center

manifest:
<path/version>

active files replaced:
<count>

metadata/hash 확인:
- complete
```

이후 Cycle을 `ACCEPTED / CLOSED`로 갱신한다.

## 11. source sync provenance

Cycle/manifest에 남긴다.

- canonical commit
- manifest version/path
- generated file count
- hash result
- human complete replacement confirmation
- confirmed timestamp

Generated bundle 자체는 cleanup 가능하다.
