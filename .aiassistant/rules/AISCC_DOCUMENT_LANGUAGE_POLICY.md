# AISCC Repository Canonical Metadata

- canonical_owner: `AISCC_REPOSITORY`
- authority: `REPOSITORY_LOCAL_CANONICAL`
- bootstrap_origin: `AISCC-BOOTSTRAP-SEED-V1`
- canonicalized_by_task: `20260826_1108_aiscc-p0-4-canonical-authority-metadata-and-post-bootstrap-state-normalization-rework-2`

---


# AISCC Document Language Policy

## 1. 목적

사람이 검토하고 판정하는 AISCC task, report, judgment, cycle, handoff 문서는 Korean-first로 작성한다. Code/product identifier와 prior-art product name은 원문을 유지한다.

## 2. Korean-first 대상

- Task File
- Executor Report
- Command Center Judgment
- Cycle Record
- current state / decision / next action
- architecture/orchestration/security baseline
- competition submission planning document

English-only 장문 문서를 기본값으로 만들지 않는다.

## 3. 원문 유지 대상

- class/function/module/package/file/path
- state/enum/result code
- API route/field
- DB table/column
- command
- framework/product/research name
- prior-art identifier

예:

```text
TransitionEngine
EvidenceArtifact
HUMAN_REQUIRED
EXECUTED_PASS
Proof-or-Stop
PROJECTMEM
SpecStory
```

원문 identifier를 한글 이름이나 임의 약어로 바꾸지 않는다.

## 4. 병기 허용

- authoritative: 프로젝트 최종 판단(authoritative)
- evidence admission: evidence admission / 증거 입장 판정
- provenance: provenance / 작업·판정 계보
- stale: stale 가능성
- sandbox: 실행 격리(sandbox)
- transition: 상태 전이(transition)
- self-dogfooding: 자기 적용(self-dogfooding)

## 5. MUST / STOP / DO NOT

Executor 정확도를 위해 짧은 English directive를 병기할 수 있다.

예:

- MUST NOT allow an Agent to commit terminal state directly.
- STOP on authority conflict.
- DO NOT treat a generated checklist as human verification.

문서 전체는 Korean-first를 유지한다.

## 6. 사용자 화면 copy

사용자 화면 copy는 Korean-first를 기본으로 한다. 내부 state/error identifier를 그대로 노출하지 않고 사람용 설명과 연결한다.

## 7. prior-art 표현

- product/research name은 원문 유지
- source가 지원하지 않는 최초/유일/세계 최초 표현 금지
- `KNOWN PRIOR ART`, `PARTIAL OVERLAP`, `DO-NOT-CLAIM`, `AISCC DIFFERENTIATION`을 구분
- 비교 문서에서 사실, 추론, project decision을 섞지 않는다.

## 8. 보고서 규칙

다음은 Korean-first로 쓴다.

- 작업 결과
- 변경 이유
- evidence 해석
- human pending/provided
- reject/hold 이유
- rollback
- next action

Code/path/state는 원문 유지한다.
