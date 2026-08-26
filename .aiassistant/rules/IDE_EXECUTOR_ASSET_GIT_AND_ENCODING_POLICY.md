# AISCC Repository Canonical Metadata

- canonical_owner: `AISCC_REPOSITORY`
- authority: `REPOSITORY_LOCAL_CANONICAL`
- bootstrap_origin: `AISCC-BOOTSTRAP-SEED-V1`
- canonicalized_by_task: `20260826_1108_aiscc-p0-4-canonical-authority-metadata-and-post-bootstrap-state-normalization-rework-2`

---


# AISCC Asset, Git, and Encoding Policy

## 1. 목적

AISCC repository의 product source, tracked governance/provenance, ignored temporary artifact, repository configuration을 구분한다.

기존 비공개 프로젝트와 달리 AISCC는 **AI와 어떻게 일했는가를 증명**해야 하므로 selected governance history를 Git으로 공개 보존한다.

## 2. Git tracking 기본값

### TRACK

```text
.aiassistant/rules/**
.aiassistant/records/command-center/**
.aiassistant/records/aiscc/**
.aiassistant/tasks/done/**
.aiassistant/reports/aiscc/**
.aiassistant/project-sources/PROJECT_SOURCE_BUNDLE_REGISTRY.md
.aiassistant/project-sources/manifests/**
```

`reports/aiscc`에는 curated baseline/handoff/reference만 둔다. raw executor report 적재소로 사용하지 않는다.

### IGNORE

```text
.aiassistant/tasks/active/**
.aiassistant/reports/target/**
.aiassistant/project-sources/bundles/**
```

추후 runtime이 생성하는 sandbox/worktree/log/cache path는 security/runtime design에서 추가한다.

### repository-root transport 결정

repository-root `AGENTS.md`는 TRACK되는 thin transport bootstrap이며 policy authority가 아니다. Executor는 active Task의 explicit authorization 없이 root `.gitignore` 또는 canonical Git policy를 수정하지 않는다.

## 3. 의미 경계

```text
product source changes
= application/runtime/test/config source

governance/provenance changes
= rules, command-center, tasks/done, cycles, curated reports, mirror manifests

temporary generated artifacts
= tasks/active, reports/target, generated mirror bundles, runtime residue

repository configuration
= .gitignore, build config, CI config, container config
```

보고서에서 네 범주를 분리한다.

## 4. `tasks/done`과 `cycles`

`tasks/done`:

- AI에게 정확히 무엇을 요구했는가
- accepted 여부와 무관
- completed/blocked/failed/rework predecessor를 보존 가능

`records/aiscc/cycles`:

- 실제 수행·evidence·human judgment·next action
- accepted-only가 아님
- public provenance에서 raw chat보다 우선

민감정보와 회사/private source는 공개 provenance에 포함하지 않는다.

## 5. `reports/target`과 generated mirror bundle

- `reports/target`은 executor → Command Center 임시 review artifact
- `project-sources/bundles`는 tracked manifest에서 재생성 가능한 upload copy
- 둘 다 Git에 넣지 않는다.
- 판정/동기화 이후 필요한 정보는 Cycle, manifest, canonical, commit에 흡수한다.

## 6. Git status/diff 해석

Executor는 최소한 다음을 구분한다.

- task 전부터 존재한 unrelated dirty path
- current task가 의도적으로 수정한 path
- ignored path라 status에 보이지 않는 artifact
- generated artifact
- repository config change

금지:

- unrelated dirty file reset/cleanup
- 사람 명시 없이 `.gitignore` 변경
- broad ignore pattern으로 future canonical/provenance 숨김
- 사람 명시 없이 Git index/commit/push 조작

## 7. `.gitignore` 변경

Task가 exact pattern과 이유를 승인한 경우에만 수정한다.

현재 repository ignore baseline:

```gitignore
.idea/
.aiassistant/bootstrap-input/
.aiassistant/tasks/active/
.aiassistant/reports/target/
.aiassistant/project-sources/bundles/
```

Task File은 실제 repository 구조와 tooling에 맞춰 exact entry를 재확인해야 한다.

## 8. secrets / private data

다음을 public task/cycle/report/commit/mirror에 넣지 않는다.

- API key/token/cookie
- credential/private key
- private env/datasource
- 개인식별정보 또는 실제 고객 data
- 회사 비공개 source/document
- prompt/session에 포함된 민감 원문

secret 후보 발견 시 값을 출력하지 않고 path와 detection reason만 보고한 뒤 중단한다.

## 9. UTF-8 read/write

- `.md`, `.yaml`, `.json`, `.py`, `.ts`, `.tsx`, `.sql`, `.html`, `.css`는 기본 UTF-8
- 신규 문서/report/manifest는 가능하면 UTF-8 no BOM
- Windows PowerShell에서는 처음부터 explicit UTF-8 사용
- 깨진 뒤 같은 파일을 반복 출력하지 않는다.

## 10. PowerShell Markdown guard

Markdown 백틱이 있는 본문을 PowerShell double-quoted string/here-string으로 직접 작성하지 않는다.

권장:

- IDE file API
- `apply_patch`
- single-quoted here-string
- `.NET WriteAllText` + literal content

작성 후 확인:

- U+0009 의도치 않은 tab
- 깨진 triple backtick fence
- `` `t `` escape 변환 흔적
- `git diff --check` 또는 동등한 검사

## 11. Console output

- 대형 문서 전체를 반복 스트리밍하지 않는다.
- 필요한 heading/path/result만 출력한다.
- report에는 읽은 path와 반영 기준을 남긴다.
- secret/log noise를 최소화한다.

## 12. report 기준

필수 분리:

```text
product source changes:
- ...

governance/provenance changes:
- ...

temporary generated artifacts:
- ...

repository configuration changes:
- ...
```

## 13. 금지

- public provenance에 private/secret material 저장
- `reports/target` 또는 generated bundle을 product source로 보고
- `tasks/done`을 accepted-only 기록으로 해석
- Cycle을 raw report dump로 사용
- 사람 명시 없이 `.gitignore`, Git index, commit, push 변경
- source/mirror Markdown을 unsafe PowerShell interpolation으로 손상
