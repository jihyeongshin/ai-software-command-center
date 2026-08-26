# AISCC Repository Canonical Metadata

- canonical_owner: `AISCC_REPOSITORY`
- authority: `REPOSITORY_LOCAL_CANONICAL`
- bootstrap_origin: `AISCC-BOOTSTRAP-SEED-V1`
- canonicalized_by_task: `20260826_1108_aiscc-p0-4-canonical-authority-metadata-and-post-bootstrap-state-normalization-rework-2`

---


# AISCC Short Executor Prompt Template

## 1. 목적

IDE Executor chat에는 Task File path와 핵심 transport/evidence 규칙만 전달한다. Task 전문을 함께 붙여넣지 않는다.

## 2. 기본 prompt

```markdown
작업 지시서는 아래 파일이다.

.aiassistant/tasks/active/<task-file>.md

작업 전 이 파일을 읽고 이번 턴의 기준으로 삼아라.

repository-root instruction entrypoint는 thin transport bootstrap이며 project policy authority가 아니다.
Project Rules UI 또는 automatic retrieval만으로 canonical rule body가 Agent context에 전달됐다고 가정하지 마라.

자동 발견된 instructions, Task File이 지정한 canonical sources, current source, accepted evidence가 충돌하면 구현하지 말고 conflict investigation으로 보고하라.

Task File의 읽을 문서 목록은 minimum authoritative context set이다.
exact path를 직접 읽고 unrelated rules/records/source/logs를 bulk-read하지 마라.

.aiassistant에는 tracked governance provenance와 ignored temporary artifacts가 함께 존재한다.
product source, governance/provenance, repository configuration 변경을 보고서에서 분리하라.

Task File의 evidence contract가 executor_required, reuse_allowed, human_owned, not_required, forbidden 범위를 결정한다.
Agent claim을 evidence로 과장하지 말고, human_owned verification을 완료했다고 주장하지 마라.

빈 report 항목을 채우기 위해 DB, HTTP runtime, browser, network, credential, full suite 또는 비목표 evidence를 추가 수집하지 마라.
새 환경이나 비목표 검증이 필요하면 EVIDENCE_SCOPE_EXPANSION_REQUIRED로 중단하라.

named blocker 이후에는 blocker를 입증하는 최소 evidence, workspace inventory, report/export와 안전한 종료만 수행하라.

report/export는 아래 canonical rules를 따른다.

- .aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
- .aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md

Target bundle:
.aiassistant/reports/target/YYYYMMDD_HHmm_<safe-slug>/
```

## 3. 문서 기준선 작업 추가 문구

```markdown
이번 턴은 DOC_BASELINE_UPDATE다.
Task File이 허용한 canonical documentation만 변경하고 product runtime source는 수정하지 마라.
```

## 4. orchestration/state-machine 구현 추가 문구

```markdown
이번 턴은 ORCHESTRATION_IMPLEMENTATION이다.
Agent output과 system state를 분리하고 Agent가 terminal transition을 직접 소유하지 않게 하라.
Task File이 지정한 transition/invariant만 구현하며 임의 state 추가를 금지한다.
```

## 5. evidence admission 구현 추가 문구

```markdown
이번 턴은 EVIDENCE_ADMISSION_IMPLEMENTATION이다.
proof type, owner, freshness, provenance를 보존하고 서로 다른 proof channel을 조용히 대체하지 마라.
human_owned evidence는 HUMAN_PENDING 또는 HUMAN_PROVIDED로만 처리하라.
```

## 6. security/sandbox 구현 추가 문구

```markdown
이번 턴은 SECURITY_SANDBOX_IMPLEMENTATION이다.
Task File이 허용하지 않은 network, credential, host filesystem, process, Git remote action을 수행하지 마라.
security boundary가 불명확하면 fail-closed로 중단하라.
```

## 7. frontend 구현 추가 문구

```markdown
이번 턴은 FRONTEND_IMPLEMENTATION이다.
사람 browser/visual QA 전에는 accepted로 단정하지 말고 ACCEPTED_CANDIDATE로 보고하라.
```

## 8. audit/dry-run 추가 문구

```markdown
이번 턴은 audit/dry-run이다.
Task File이 수정 허용을 명시하지 않으면 파일을 변경하지 마라.
충돌 또는 policy gap이 있으면 blocked/doc-update-required로 보고하라.
```

## 9. Project Source mirror 추가 문구

```markdown
이번 턴은 PROJECT_SOURCE_MIRROR_SYNC다.
local canonical을 수정하지 않고 tracked manifest를 기준으로 ignored generated bundle을 만든다.
canonical body와 mirror body hash, file count, active list를 검증하라.
Browser Project Source 업로드 완료는 사람이 보고하기 전까지 HUMAN_PENDING이다.
```
