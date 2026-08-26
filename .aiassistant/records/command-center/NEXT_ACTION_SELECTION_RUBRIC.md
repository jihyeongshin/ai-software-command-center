# AISCC Repository Canonical Metadata

- canonical_owner: `AISCC_REPOSITORY`
- authority: `REPOSITORY_LOCAL_CANONICAL`
- bootstrap_origin: `AISCC-BOOTSTRAP-SEED-V1`
- canonicalized_by_task: `20260826_1108_aiscc-p0-4-canonical-authority-metadata-and-post-bootstrap-state-normalization-rework-2`

---


# AISCC Next Action Selection Rubric

## 1. 기본 우선순위

1. security/policy/missing-artifact blocker 해소
2. rejected / hold / failed rework
3. canonical baseline gap 또는 authority conflict 해소
4. explicit state machine / evidence admission / human gate core
5. sandbox/tool permission 안전성
6. active feature의 release-readiness와 directly affected QA
7. self-dogfooding cutover prerequisite
8. demo/evaluation/submission critical path
9. workflow/public provenance 개선
10. optional polish/scale/integration

## 2. 구현 전 기준선

아래가 흔들리면 구현 Task를 발행하지 않는다.

- product thesis
- state/transition authority
- evidence type/owner/admission
- sandbox/tool/network/secret boundary
- human gate ownership
- persistence/recovery semantics

우선 작업:

```text
DOC_BASELINE_UPDATE
DESIGN_AUDIT
DISCOVERY_AUDIT
```

## 3. 핵심 MVP 우선

다음보다 핵심 governance chain을 우선한다.

```text
Task Contract
→ Explicit State Machine
→ Agent Execution
→ Evidence Admission
→ Human Gate
→ Judgment
→ Cycle Memory
```

후순위:

- 다수 Agent 병렬 최적화
- model routing 고도화
- 대형 RAG/vector platform
- Kubernetes/microservice
- enterprise integration
- UI polish

## 4. Self-Dogfooding cutover gate

아래가 없으면 cutover를 열지 않는다.

- deterministic transition engine
- durable task/run state
- required evidence admission
- proof type/owner guard
- human-required transition
- forbidden action/tool permission guard
- retry/rework/failure path
- cycle/provenance emission
- 사람이 확인한 safe fallback

Cutover 뒤에도 AISCC 결과를 자동 accepted하지 않는다.

## 5. demo/submission 우선

상위 순위보다 실제 제출을 우선한다.

- 작동하는 MVP
- 4개 canonical demo scenario
- public task/cycle/commit provenance
- prior-art와 DO-NOT-CLAIM boundary
- self-dogfooding evidence
- 재현 가능한 실행/영상/README

deadline 위험이 생기면 optional architecture polish보다 submission-ready vertical slice를 선택한다.

## 6. `NEXT_ACTIONS.md` 갱신 기준

갱신:

- 장기 queue 순서 변경
- current priority 완료 후 승격
- blocker로 기존 queue가 위험
- hold/defer/reopen 변경
- self-dogfooding cutover 상태 변경
- submission critical path 변경
- 새 Browser session이 stale handoff를 따를 위험

갱신하지 않음:

- 이미 queue에 있던 task의 단순 수행
- 같은 track의 design → implementation → targeted verification
- 작은 보정이 Cycle Record로 충분

## 7. next action template

```markdown
next_action:
- work_type:
- title:
- reason:
- blocker:
- required_baseline:
- allowed_scope:
- forbidden_scope:
- required_evidence:
- human_verification_needed:
- public_provenance_expected:
```

## 8. current post-P0-4 queue entry

```text
P0-5 First Project Source Mirror v1
→ P1-1 Core Domain / State Machine Design
→ P1-2 Security / Sandbox / Runtime Boundary Design
→ P1-3 Security / Runtime Safeguard Implementation and Verification
```
