# 작업지시서: P1-8 Historical Policy vs Current Policy Separation Design Rework

## meta
- task_id: `20260830_2011_aiscc-p1-8-historical-policy-and-current-policy-separation-design-rework-1`
- phase: `P1-8 Project Memory and Cycle Admission`
- work_type: `DESIGN_REWORK`
- expected_start_head: `4b84a9f66c148b198d3f4b6b01cffc4641fdceb1`
- predecessor_design_sha256: `8024613cc0c4d525e010db937ba8a249dcbfa77feeb7faa5cc9f6862864068b2`
- p1_8_runtime_status: `NOT_STARTED`

## 1. scope
2011 source/current finding은 닫혔다. 재설계하지 마라.

이번 rework는 다음만 닫는다.

```text
historical policy issuance validity
!= current policy applicability
```

대상:

```text
MemoryDeclarationAuthorityPolicy
NextActionEligibilityPolicy
NextActionSelectionPolicy
NextActionDescriptor
```

## 2. MemoryDeclarationAuthorityPolicy

현재 설계의:

```text
exact current MemoryDeclarationAuthorityPolicy
```

를 new-admission path와 historical-replay path로 분리하라.

### new Cycle admission
반드시:

```text
current unsuperseded eligible policy
exact ID/version/fingerprint
valid source enrollment
```

을 요구한다.

### existing Cycle historical replay
반드시:

```text
stored exact policy ref/version/fingerprint
policy immutable payload/fingerprint
policy authority ID/version/revision
policy가 original admission sequence/timestamp에서 valid했음
```

을 검증한다.

하지만:

```text
policy가 지금도 current인가?
```

는 historical Cycle identity criterion이 아니다.

Later policy supersession/revocation은 old Cycle/ProjectMemoryEntry content를 rewrite하지 않는다.

정책 계약상 current-use invalidation이 필요한 경우:

```text
policy owner event
→ ProjectMemoryAuthorityEvent
→ current applicability/view only
```

로 반영하라.

## 3. replay identity

Freeze:

```text
same Cycle ID + same immutable payload + same historical policy version
→ same AdmittedCycle/ProjectMemoryEntry replay

later current policy version changed
→ historical identity unchanged
```

Current policy revision/event sequence는:

```text
cycle_candidate_fingerprint
AdmittedCycle fingerprint
ProjectMemoryEntry content fingerprint
```

에 넣지 마라.

## 4. NextAction historical policy separation

New selection:

```text
current NextActionEligibilityPolicy
current NextActionSelectionPolicy
current enrolled NextActionDescriptor
```

필수.

Historical replay of existing `NextActionSelection`:

```text
exact eligibility policy version/fingerprint
exact selection policy version/fingerprint
exact descriptor version/fingerprint
those objects valid at original selection issuance
```

필수.

하지만:

```text
currently current/enrolled now
```

는 historical replay criterion이 아니다.

Later policy/descriptor supersession/revocation은:

```text
old NextActionSelection immutable history
→ preserve

current-next-action projection/future selection eligibility
→ update/fail closed
```

로 분리하라.

## 5. current selection/use

A stale/revoked descriptor/policy must never be used to create a new current selection.

If current projection still points to a selection whose descriptor/policy has become revoked and policy contract
requires withdrawal:

```text
append-only NextAction authority/current-projection event
→ current selection becomes non-current
```

Do not rewrite old selection.

## 6. typed errors

Add/reuse exact equivalents:

```text
MEMORY_POLICY_HISTORICAL_PROVENANCE_INVALID
MEMORY_POLICY_CURRENTLY_INELIGIBLE

NEXT_ACTION_POLICY_HISTORICAL_PROVENANCE_INVALID
NEXT_ACTION_DESCRIPTOR_CURRENTLY_INELIGIBLE
```

Do not use a generic “stale policy” error for both historical corruption and ordinary current supersession.

## 7. proof examples

Must include:

```text
Cycle admitted under memory policy v1
→ v2 supersedes v1
→ same Cycle replay succeeds
→ new admission using v1 fails

NextActionSelection issued under eligibility/selection policy v1
→ v2 supersedes/revokes v1
→ historical selection replay succeeds
→ new selection using v1 fails

policy v1 was already revoked before original Cycle/Selection issuance
→ historical provenance invalid
```

## 8. preserve

Do not change:

```text
2011 historical source/current applicability semantics
1933 memory authority/lineage/NextAction eligibility semantics
P1-4/P1-6/P1-7 authority
Task issuance boundary
```

## 9. allowed mutation
Modify only:

```text
.aiassistant/rules/AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md
```

Lifecycle:

```text
.aiassistant/tasks/active/
20260830_2011_aiscc-p1-8-historical-policy-and-current-policy-separation-design-rework-1.md

→

.aiassistant/tasks/done/
20260830_2011_aiscc-p1-8-historical-policy-and-current-policy-separation-design-rework-1.md
```

Preserve the HOLD Cycle:

```text
.aiassistant/records/aiscc/cycles/
20260830_2011_aiscc-p1-8-design-historical-policy-current-policy-separation-hold-1.cycle.md
```

## 10. forbidden
No:

```text
src/**
tests/**
migrations/**
canonical state update
P1-8 runtime
P2/P3
Git add/commit/push
```

## 11. accept criteria
All must hold:

```text
new Cycle admission uses current memory declaration policy

historical Cycle replay uses exact historical policy validity, not currentness

later policy supersession does not alter immutable Cycle/entry identity

new NextAction selection uses current eligibility/selection policies/descriptors

historical NextAction replay uses exact historical policy/descriptor validity, not currentness

later policy/descriptor supersession changes only current/future eligibility

historical corruption and ordinary current staleness have distinct typed errors

2011/1933 closed findings remain unchanged

runtime remains NOT_STARTED

Human verification = HUMAN_PENDING
```

## 12. export
Target:

```text
.aiassistant/reports/target/
20260830_2011_aiscc-p1-8-historical-policy-and-current-policy-separation-design-rework-1/
```

Include:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
.aiassistant/rules/AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md
2011 historical-policy HOLD Cycle
done Task
```

## 13. expected final state
```text
P1-8 Design:
REWORKED_DESIGN_CANDIDATE / HUMAN_PENDING

P1-8 Runtime:
NOT_STARTED
```
