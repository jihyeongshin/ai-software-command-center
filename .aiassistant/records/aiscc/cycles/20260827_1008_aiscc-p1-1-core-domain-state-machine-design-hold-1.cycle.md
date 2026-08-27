# AISCC Cycle Record

## meta

- cycle_id: `20260827_1008_aiscc-p1-1-core-domain-state-machine-design-hold-1`
- date: `2026-08-27 10:08 KST`
- primary_semantic_owner: `P1-1 Core Domain / State Machine Design judgment`
- affected_areas:
  - core domain authority
  - workflow state machine
  - Judgment / TransitionDecision relationship
  - terminal admission semantics
- work_type: `DESIGN_AUDIT`
- execution_mode: `MANUAL_COMMAND_CENTER`
- task_file: `20260826_2157_aiscc-core-domain-and-state-machine-design-1.md`
- task_done_path: `.aiassistant/tasks/done/20260826_2157_aiscc-core-domain-and-state-machine-design-1.md`
- temporary_target_bundle: `.aiassistant/reports/target/20260826_2157_aiscc-core-domain-and-state-machine-design-1/`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause: `POLICY_BASELINE_CONFLICT`
- cycle_record_action: `create`
- source_mirror_sync: `not-required`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260827_1008_aiscc-p1-1-core-domain-state-machine-design-hold-1.cycle.md`

## product/repository snapshot

Executor report:

- repository root:
  `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- HEAD before/after:
  `25a81a9d42ecee0185fb36f83b86348b575905aa`
- Git index mutation: `none`
- Git commit/push/remote operation: `FORBIDDEN_NOT_RUN`

Candidate artifacts:

- `.aiassistant/rules/AISCC_ARCHITECTURE.md`
  - SHA-256:
    `f053aad5b194a418d5c68402e71a381856494c75f240e0a52057ab247f9fad77`
- `.aiassistant/rules/AISCC_ORCHESTRATION.md`
  - SHA-256:
    `1bc977a252d97576c7913a392bf167b810ce13a1ca85c72c3f5aa68ea3d61cdc`

## command summary

P1-1은 implementation 전에 AISCC core domain, exact finite workflow state set,
transition request/evaluation/admission, terminal semantics, Human gate,
concurrency/stale request, persistence/recovery requirement와 future owner handoff를
canonical design candidate로 정의하도록 지시되었다.

## executor result summary

### product source changes

- none

### governance/provenance changes

- `AISCC_ARCHITECTURE.md` candidate created
- `AISCC_ORCHESTRATION.md` candidate created
- executor Task moved to done
- temporary target bundle created

### repository configuration changes

- none

## accepted candidate scope

다음은 rework에서 유지해도 되는 strong candidate scope다.

1. `WorkRun`을 System-owned authoritative execution aggregate로 둔 구조
2. exact 9-state set:
   - `READY`
   - `RUNNING`
   - `ADMISSION_PENDING`
   - `HUMAN_REQUIRED`
   - `BLOCKED`
   - `REWORK_REQUIRED`
   - `ACCEPTED`
   - `REJECTED`
   - `FAILED`
3. `ExecutionStatus`, `HumanGateStatus`, `JudgmentStatus`, `RuntimeMode`를
   `WorkflowState`와 분리한 구조
4. `TransitionRequest → TransitionEvaluation → TransitionDecision →
   AuthoritativeStateMutation` 분리
5. Agent가 authoritative workflow state를 mutate하지 않는 invariant
6. `WorkRun.state_version`을 concurrency/stale request boundary로 둔 설계
7. stale request:
   `DENIED(STALE_REQUEST) / no mutation / fresh request required`
8. admitted transition과 state-version mutation의 atomicity requirement
9. append-only transition provenance + reconstructable current projection
10. `OWNER_SELF_DOGFOOD`, `PUBLIC_RECORDED_REPLAY`,
    `PUBLIC_BOUNDED_LIVE`를 workflow state가 아닌 RuntimeMode로 분리
11. P1-2/P1-3/P1-4/P1-5/P1-6/P1-7/P1-8 handoff
12. implementation/DB/provider/security detail을 후속 owner로 defer한 경계

이 scope는 terminal acceptance가 아니며 rework 결과에서 다시 consistency 확인한다.

## required rework — load-bearing inconsistency

### A. `JudgmentStatus` contract vs exact transition matrix conflict

`AISCC_ORCHESTRATION.md` section 4.3은 다음 semantic contract를 둔다.

```text
JudgmentStatus:
PENDING / ACCEPTED / REJECTED / HOLD_REWORK_REQUIRED

System은 applicable judgment ref를 검증한 뒤에만
ACCEPTED, REJECTED, REWORK_REQUIRED transition을 입장한다.
```

그러나 exact transition matrix의:

```text
ADMISSION_PENDING → ACCEPTED
```

guard는:

```text
G_EVIDENCE
+ no applicable Human gate
+ no conflict
```

만 요구하며 authoritative `Judgment` / accepted judgment ref를 guard로 요구하지 않는다.

`HUMAN_REQUIRED → ACCEPTED`도:

```text
G_EVIDENCE
+ G_HUMAN_APPROVED
```

만으로 terminal admission이 가능하게 되어 있다.

이 상태에서는 evidence sufficiency 또는 Human approval이 별도 Judgment 없이
직접 `ACCEPTED` state로 이어질 수 있으므로, 설계가 스스로 정의한
`JudgmentStatus` contract와 충돌한다.

### B. Architecture information flow conflict

`AISCC_ARCHITECTURE.md`는 information flow를 다음 순서로 기술한다.

```text
AgentOutput
→ EvidenceCandidateRef / TransitionRequest
→ System evaluation
→ Evidence admission refs + HumanGate result when required
→ TransitionDecision
→ authoritative state mutation
→ Judgment / Cycle admission
→ NextAction
```

이 순서는 `Judgment`를 terminal state mutation 뒤에 둔다.

반면 `AISCC_ORCHESTRATION.md` section 4.3은 applicable `Judgment`가
`ACCEPTED`, `REJECTED`, `REWORK_REQUIRED` transition보다 먼저
입장되어야 한다고 규정한다.

두 canonical candidate가 동일 semantic fact를 반대로 정의하므로
P1-1 accept criteria의 cross-baseline consistency를 충족하지 못한다.

### C. `TransitionDecision` vs `Judgment` non-substitution이 불명확

P1-1은 두 개념을 모두 정의했으나 다음을 exact하게 고정하지 않았다.

```text
TransitionDecision
!= Judgment
```

필요한 구분:

- `Judgment`: Task outcome에 대한 semantic 판단
  (`ACCEPTED`, `REJECTED`, `HOLD_REWORK_REQUIRED` 또는 선택한 canonical values)
- `TransitionDecision`: 현재 authoritative state/version에서
  특정 target mutation을 admission/deny하는 System control decision

Judgment가 존재한다고 transition이 자동 발생해서는 안 되며,
TransitionDecision이 존재한다고 semantic Judgment를 대신해서도 안 된다.

### D. `REWORK_REQUIRED` state wording / predecessor mismatch

State definition은:

```text
현재 submission은 accepted 불가지만 ...
```

라고 정의하지만, exact transition matrix는:

```text
RUNNING → REWORK_REQUIRED
```

를 허용한다.

`RUNNING`에서는 아직 executor submission이 존재하지 않을 수 있으므로
state semantics와 predecessor가 불일치한다.

Rework에서는 다음 중 하나를 exact하게 선택해야 한다.

1. `REWORK_REQUIRED`를 current attempt/submission의 correctable condition으로
   정의를 넓히고 RUNNING transition의 authoritative judgment/reason을 명시한다.
2. 또는 `RUNNING → REWORK_REQUIRED`를 제거하고 execution-time correction을
   다른 기존 semantic path로 처리한다.

State 수를 늘리는 것은 required correction이 아니다.

## command-center judgment

```text
result_status: HOLD_REWORK_REQUIRED
accepted_scope: partial design candidate only
terminal_acceptance: No
human_verification: deferred until corrected candidate
state_set_reopen_required: No, unless rework proves necessary
implementation_allowed: No
P1-2_allowed: No
```

### judgment reason

P1-1 Task는 exact state/transition semantics와 authority boundary를
implementation 전 canonical baseline으로 고정하는 HIGH_RISK design Task다.

현재 candidate의 핵심 state/concurrency/authority 구조는 강하지만,
`Judgment`가 terminal/rework state admission의 선행 semantic input인지,
state mutation 뒤에 생성되는 project record인지 두 문서가 충돌한다.

이 불일치는 P1-4 state machine kernel 및 P1-7 Human/judgment 구현 시
실제 transition authority ambiguity로 이어질 수 있으므로 문구 수준의
minor acceptance condition으로 남길 수 없다.

## proof admission

- Agent claim:
  `ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING`
- admitted:
  - static candidate integrity
  - exact 9-state proposal
  - exact transition matrix proposal
  - concurrency/persistence/runtime-mode handoff proposal
- rejected for terminal admission:
  - cross-document Judgment/transition consistency claim
- proof type substitution detected:
  `No`
- forbidden action detected:
  `No`

## human verification

- owner: Human
- channel: `HUMAN_VERIFICATION`
- status: `DEFERRED_BY_REWORK`
- reason:
  Human에게 conflicting design을 accept/reject하도록 넘기기 전에
  Command Center-level semantic contradiction을 먼저 제거한다.

Human review는 corrected candidate 제출 후 다시 요구한다.

## mandatory stop / scope expansion

- mandatory_stop_triggered: `No` during executor run
- Command Center hold after submission: `Yes`
- implementation after hold: `FORBIDDEN`
- P1-2 execution after hold: `FORBIDDEN`
- evidence_scope_expansion: `none`

## preserved artifacts

Preserve exact paths:

- `.aiassistant/tasks/done/20260826_2157_aiscc-core-domain-and-state-machine-design-1.md`
- `.aiassistant/records/aiscc/cycles/20260827_1008_aiscc-p1-1-core-domain-state-machine-design-hold-1.cycle.md`

The current two design candidate files remain rework inputs until superseded:

- `.aiassistant/rules/AISCC_ARCHITECTURE.md`
- `.aiassistant/rules/AISCC_ORCHESTRATION.md`

The temporary target bundle is not canonical acceptance evidence and may be deleted
after the rework inputs are safely preserved/submitted according to repository policy.

## next action

```text
next_action:
- phase: P1-1
- work_type: REWORK
- title: Judgment / Transition Admission Semantic Alignment
- reason: exact state-machine candidate has a cross-document load-bearing authority inconsistency
- blocker: corrected architecture/orchestration candidate required
- required_baseline:
  - current P1-1 candidate
  - accepted Product Thesis
  - current Decision Register
  - this HOLD Cycle
- human_verification_needed: Yes, after rework candidate
- next_after_acceptance: P1-2 Security / Sandbox / Runtime Boundary Design
```
