# AISCC Repository Canonical Metadata

- canonical_owner: `AISCC_REPOSITORY`
- authority: `REPOSITORY_LOCAL_CANONICAL`
- bootstrap_origin: `AISCC-BOOTSTRAP-SEED-V1`
- canonicalized_by_task: `20260826_1108_aiscc-p0-4-canonical-authority-metadata-and-post-bootstrap-state-normalization-rework-2`

---


# AISCC Short Executor Prompt Template

## 1. 목적

IDE Executor chat에는 issued artifact transport와 Task File path, 핵심 evidence 규칙만 전달한다. Task 전문을 함께 붙여넣지 않는다.

## 2. Human-visible fresh IDE chat notice

fresh IDE Executor chat이 `REQUIRED`일 때만 Browser response의 Short Prompt 위에 다음 문장과 짧은 이유를 표시한다.

```text
이번 작업은 IDE Executor에서 새 채팅세션을 열고 시작해야 합니다.

이유: <explicit authority/context boundary>
```

이 notice는 Human action을 위한 Browser text다. Short Prompt 안에 넣거나 IDE Executor에게 새 chat 생성/open을 지시하지 않는다.

## 3. transport-first prompt

Command Center가 artifact를 발행한 turn은 다음 block에서 실제 issued artifact subset만 열거한다. absent artifact type과 HANDOFF를 임의 생성하지 않는다.

```markdown
이번 Command Center 발행 artifact transport부터 먼저 수행하라.

Human이 이번 발행 ZIP의 파일들을 아래 경로에 flat 압축해제한 상태다.

C:\Users\oracl\Downloads

[ISSUED ARTIFACTS]

<TYPE>
<exact filename>

expected SHA-256:
<exact sha256>

[SOURCE ROOT]

C:\Users\oracl\Downloads

[REPOSITORY ROOT]

C:\Users\oracl\IdeaProjects\ai-software-command-center

[CANONICAL DESTINATIONS]

<TYPE>
→ <exact canonical destination including filename>

[TRANSPORT PROCEDURE]

각 issued artifact마다 독립적으로 수행하라.

1. Downloads source 존재 확인
2. source SHA-256 계산
3. expected SHA-256과 exact 비교
4. canonical destination 존재 여부 확인

destination이 없으면 source를 byte-preserving copy하고 destination SHA-256을 계산하여 source == destination을 확인하라.

destination이 이미 있으면 기존 destination SHA-256을 먼저 계산하라. source와 같으면 overwrite하지 않는다. 다르면 current issued source로 overwrite한 뒤 destination SHA-256을 다시 계산하여 source == destination을 확인하라.

hash equality가 확인된 artifact에 대해서만 Downloads의 해당 flat source 파일을 remove하라. ZIP 자체는 remove하지 마라. package에 명시되지 않은 Downloads 파일을 읽거나 이동하거나 삭제하지 마라.

source missing, expected SHA mismatch, destination path failure, copy/overwrite failure, source/destination hash mismatch 또는 transport result ambiguity가 있으면 substantive Task를 시작하지 말고 STOP하라.

[AFTER TRANSPORT]

모든 issued artifact transport가 PASS한 뒤에만 아래 active Task를 직접 읽어라.

<exact substantive Task path>
```

## 4. 기본 prompt

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

## 5. 문서 기준선 작업 추가 문구

```markdown
이번 턴은 DOC_BASELINE_UPDATE다.
Task File이 허용한 canonical documentation만 변경하고 product runtime source는 수정하지 마라.
```

## 6. orchestration/state-machine 구현 추가 문구

```markdown
이번 턴은 ORCHESTRATION_IMPLEMENTATION이다.
Agent output과 system state를 분리하고 Agent가 terminal transition을 직접 소유하지 않게 하라.
Task File이 지정한 transition/invariant만 구현하며 임의 state 추가를 금지한다.
```

## 7. evidence admission 구현 추가 문구

```markdown
이번 턴은 EVIDENCE_ADMISSION_IMPLEMENTATION이다.
proof type, owner, freshness, provenance를 보존하고 서로 다른 proof channel을 조용히 대체하지 마라.
human_owned evidence는 HUMAN_PENDING 또는 HUMAN_PROVIDED로만 처리하라.
```

## 8. security/sandbox 구현 추가 문구

```markdown
이번 턴은 SECURITY_SANDBOX_IMPLEMENTATION이다.
Task File이 허용하지 않은 network, credential, host filesystem, process, Git remote action을 수행하지 마라.
security boundary가 불명확하면 fail-closed로 중단하라.
```

## 9. frontend 구현 추가 문구

```markdown
이번 턴은 FRONTEND_IMPLEMENTATION이다.
사람 browser/visual QA 전에는 accepted로 단정하지 말고 ACCEPTED_CANDIDATE로 보고하라.
```

## 10. audit/dry-run 추가 문구

```markdown
이번 턴은 audit/dry-run이다.
Task File이 수정 허용을 명시하지 않으면 파일을 변경하지 마라.
충돌 또는 policy gap이 있으면 blocked/doc-update-required로 보고하라.
```

## 11. Project Source mirror 추가 문구

```markdown
이번 턴은 PROJECT_SOURCE_MIRROR_SYNC다.
local canonical을 수정하지 않고 tracked manifest를 기준으로 ignored generated bundle을 만든다.
canonical body와 mirror body hash, file count, active list를 검증하라.
Browser Project Source 업로드 완료는 사람이 보고하기 전까지 HUMAN_PENDING이다.
```
