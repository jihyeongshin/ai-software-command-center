# AISCC Repository Canonical Metadata

- canonical_owner: `AISCC_REPOSITORY`
- authority: `REPOSITORY_LOCAL_CANONICAL`
- bootstrap_origin: `AISCC-BOOTSTRAP-SEED-V1`
- canonicalized_by_task: `20260826_1108_aiscc-p0-4-canonical-authority-metadata-and-post-bootstrap-state-normalization-rework-2`

---


# AISCC Short Executor Prompt Template

## 1. 목적

IDE Executor chat에는 verified ZIP과 TASK 우선 배치에 필요한 간결한 bootstrap만 전달한다. 상세 transport/evidence/Git/export 권한은 Task artifact에 둔다.

## 2. Human-visible fresh IDE chat notice

fresh IDE Executor chat이 `REQUIRED`일 때만 Browser response의 Short Prompt 위에 다음 문장과 짧은 이유를 표시한다.

```text
이번 작업은 IDE Executor에서 새 채팅세션을 열고 시작해야 합니다.

이유: <explicit authority/context boundary>
```

이 notice는 Human action을 위한 Browser text다. Short Prompt 안에 넣거나 IDE Executor에게 새 chat 생성/open을 지시하지 않는다.

## 3. 기본 direct-ZIP bootstrap prompt

Human은 ZIP만 Downloads에 내려받는다. 수동 압축해제와 Markdown 배치는 요구하지 않는다. 아래 기본 Short Prompt는 수십 줄 이하로 유지하며 per-file hash/destination, workspace/evidence/Git allowlist를 중복하지 않는다.

```text
이번 Command Center artifact transport부터 수행하라.

Downloads:
C:\Users\oracl\Downloads

ZIP:
<exact delivery ZIP filename>

SHA-256:
<exact expected ZIP SHA-256>

ZIP이 없거나 hash 검증, archive 검증, TASK canonical bootstrap이 실패하면
프로젝트 작업/report/export 없이 즉시 STOP하고 Human에게 ZIP 재다운로드/재배치를 요청하라.

정상이면 ZIP에서 아래 TASK를 canonical tasks/active 경로로 가장 먼저 직접 배치해 읽고,
TASK의 지시에 따라 나머지 artifact와 작업을 수행하라.

<exact TASK member filename>
```

## 4. Task와 canonical workflow가 소유하는 상세 계약

- ZIP hash는 TASK와 archive membership의 bootstrap integrity anchor다. TASK 자신의 whole-file SHA를 요구하지 않는다.
- `.aiassistant/records/command-center/TASK_FILE_TEMPLATE.md`에 따라 Task에 remaining member별 hash/authoritative source, canonical destination, expected state, repository gate, evidence, Git allowlist와 export 계약을 기록한다.
- Executor는 archive readability/CRC/member safety를 검증하고 직접 member → canonical path 배치를 우선한다. package-specific staging은 직접 배치 불가 시에만 사용한다.
- exact canonical transport 이후 inbound ZIP/staging cleanup 실패는 `NON_BLOCKING_LOCAL_RESIDUE`다. terminal 시점에 best effort로 시도하고 exact 경로를 보고한다. 같은 turn에서 다른 삭제 수단으로 재시도하지 않는다.
- outbound result ZIP은 필수다. `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`에 따라 folder 완성 후 adjacent ZIP을 생성·검증하며 folder와 ZIP 경로를 모두 보고한다. 실패는 `ZIP_EXPORT_FAILED`다.
- 자세한 bootstrap STOP와 cleanup 경계는 `.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md`를 따른다.

아래 추가 문구는 필요한 좁은 예외에서만 사용한다. 기본 Short Prompt를 장문 Task 복제본으로 확장하지 않는다.

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
