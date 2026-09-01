# 작업지시서: P1-8 Prerequisite Owner Authority Exact Contract and Source Enrollment Design Rework

## meta

- task_id: `20260901_1601_aiscc-p1-8-prerequisite-owner-authority-exact-contract-and-source-enrollment-design-rework-1`
- created_at: `2026-09-01T16:01:00+09:00`
- phase: `P1-8 Runtime Prerequisite Authority Contracts`
- work_type: `DESIGN_REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `CROSS_OWNER / AISCC_COMMAND_CENTER`
- expected_start_head: `683aaee84d1fc09e9371dd214efc3ff58b7225ee`
- accepted_source_design_commit: `35901125cc5842734cf1e8eb3374d10e4ee866e3`
- terminal_governance_commit: `683aaee84d1fc09e9371dd214efc3ff58b7225ee`
- predecessor_design_path: `.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md`
- predecessor_design_sha256: `556faad8a77d917fcbfc9ab7b0ba62bd65f985a6f4a1e585c08af668dd14393c`
- accepted_source_design_path: `.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md`
- accepted_source_design_sha256: `19b1d29a8f77ca5cc480a14bc9d1bdd53206951ccf8b34802316f1280dc61cb1`
- blocked_runtime_path_count: `19`
- blocked_runtime_aggregate_sha256: `84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42`
- predecessor_audit_task_sha256: `8d5d0e74c88a311dab41869040028aa5a4ebb7df09c556b44dc457c367fc72de`
- runtime_implementation: `FORBIDDEN`
- git_mutation: `FORBIDDEN`
- human_design_review: `PENDING`

---

# 1. 현재 Command Center 판정

독립 검증된 현재 상태는 다음과 같다.

```text
20260901_1527 terminal canonical Git reconciliation audit:
ACCEPTED / CLOSED

1619 terminal persistence:
STATE_A_VERIFIED

P1-8 NEXT_ACTION_CONTEXT Source Authority Design:
HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-8 prerequisite owner-authority design:
BLOCKED_REQUIRED_EVIDENCE / NEXT_ACTION

P1-8 Runtime:
BLOCKED_REQUIRED_EVIDENCE

P2/P3:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

1527 Audit가 검증한 terminal lineage:

```text
base:
f4614198c2745944f7ec02639a45b0315bbc903d

Commit A:
35901125cc5842734cf1e8eb3374d10e4ee866e3
parent = base

Commit B:
683aaee84d1fc09e9371dd214efc3ff58b7225ee
parent = Commit A
```

Commit A/B object, parent, exact changed-path allowlist, 20 committed blob identity와 terminal semantics는
`STATE_A_VERIFIED`다.

0813 removed done Task의 immediate pre-removal tracked/untracked classification만
`NOT_VERIFIABLE_FROM_CURRENT_GIT_STATE`다. 이 항목은 1527 Audit의 허용된 bounded uncertainty이며 이번 Task의
blocker가 아니다. reflog, deleted-file recovery, filesystem forensic로 범위를 확장하지 않는다.

---

# 2. 이번 턴 목표

같은 prerequisite candidate rule 하나만 rework하여 다음 세 계약을 구현 가능한 수준의 exact V1 design으로
동시에 닫는다.

1. `TaskConstraint` scope별 cardinality, immutable owner event, currentness fold, private issue/revoke capability.
2. P1-4 blocker taxonomy, reason별 resumability, exact durable `G_BLOCKER_RESOLVED` binding.
3. accepted `NextActionContextRefV1` source-authority 계약을 P1-8 catalog/descriptor/eligibility/selection authority에
   exact enrollment하고 모든 영향 fingerprint를 재계산.

Output은 다음 중 하나다.

```text
CANDIDATE / HUMAN_REVIEW_REQUIRED
```

모든 exact contract와 fingerprint가 닫혔을 때만 위 결과를 사용한다.

필수 owner contract 또는 accepted baseline과의 compatibility가 닫히지 않으면:

```text
BLOCKED_REQUIRED_EVIDENCE / IMPLEMENTATION_BASELINE_GAP
```

으로 중단한다.

---

# 3. 이번 턴 비목표

- external TaskConstraint owner runtime 구현
- external NEXT_ACTION_CONTEXT owner runtime 구현
- P1-4/P1-6/P1-7/P1-8 runtime, migration, test 변경
- blocked P1-8 runtime candidate 수정 또는 재검증 확대
- accepted source-authority rule 재설계 또는 수정
- accepted P1-4/P1-6/P1-7 authority 의미 변경
- Human acceptance 생성 또는 대행
- canonical state/decision/next-action/Cycle 갱신
- Git index/commit/history/remote 작업
- P2/P3, deployment, Public Live 작업

---

# 4. mandatory preflight

작업 전 다음을 모두 검증한다.

```text
repository root:
expected AISCC repository

branch:
main

HEAD:
683aaee84d1fc09e9371dd214efc3ff58b7225ee

index:
empty

accepted source design:
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
19b1d29a8f77ca5cc480a14bc9d1bdd53206951ccf8b34802316f1280dc61cb1

predecessor prerequisite candidate:
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
556faad8a77d917fcbfc9ab7b0ba62bd65f985a6f4a1e585c08af668dd14393c

prior accepted audit done Task:
.aiassistant/tasks/done/20260901_1527_aiscc-p1-8-next-action-context-terminal-canonical-git-reconciliation-audit-1.md
8d5d0e74c88a311dab41869040028aa5a4ebb7df09c556b44dc457c367fc72de

blocked runtime:
19 paths /
84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42
```

Pre-lifecycle working tree는 정확히 다음 21개 uncommitted path만 허용한다.

```text
19 blocked runtime paths
+ predecessor prerequisite candidate 1 path
+ prior 1527 audit done Task 1 path
```

현재 active Task path와 ignored target bundle은 Git dirty path count에 포함하지 않는다.

unexpected path, staged path, HEAD mismatch, accepted source drift, predecessor candidate drift, prior audit Task drift가
하나라도 있으면 mutation 전에:

```text
STOP / REVIEWED_CANDIDATE_DRIFT_OR_WORKSPACE_COLLISION
```

으로 보고한다.

---

# 5. preserve exact artifacts

다음 항목은 byte-identical 또는 immutable Git identity로 보존한다.

```text
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md

.aiassistant/rules/AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md

.aiassistant/records/aiscc/cycles/
20260831_1332_aiscc-p1-8-prerequisite-owner-authority-baseline-gap-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260831_1332_aiscc-p1-8-prerequisite-owner-authority-exact-contract-gap-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260831_1619_aiscc-p1-8-next-action-context-source-authority-final-acceptance-1.cycle.md

.aiassistant/reports/aiscc/
20260831_1619_aiscc-p1-8-next-action-context-accepted-prerequisite-design-resume-handoff-1.md

.aiassistant/tasks/done/
20260901_1527_aiscc-p1-8-next-action-context-terminal-canonical-git-reconciliation-audit-1.md

.aiassistant/reports/target/
20260901_1527_aiscc-p1-8-next-action-context-terminal-canonical-git-reconciliation-audit-1/
```

Commit A/B와 그 committed blob identity를 변경, amend, replace 또는 재작성하지 않는다.

Blocked runtime 19 path는 모두 byte-identical로 보존한다.

| # | exact path |
|---:|---|
| 1 | `migrations/versions/20260831_0006_p1_8_project_memory_cycle_admission.py` |
| 2 | `migrations/versions/20260831_0007_p1_8_authority_contract_rework.py` |
| 3 | `src/aiscc/cycle/__init__.py` |
| 4 | `src/aiscc/cycle/models.py` |
| 5 | `src/aiscc/cycle/repository.py` |
| 6 | `src/aiscc/judgment/authority.py` |
| 7 | `src/aiscc/memory/__init__.py` |
| 8 | `src/aiscc/memory/models.py` |
| 9 | `src/aiscc/memory/repository.py` |
| 10 | `src/aiscc/next_action/__init__.py` |
| 11 | `src/aiscc/next_action/models.py` |
| 12 | `src/aiscc/next_action/repository.py` |
| 13 | `src/aiscc/persistence/models.py` |
| 14 | `tests/integration/evidence/test_postgres_evidence_admission.py` |
| 15 | `tests/integration/human/test_postgres_human_gate_judgment.py` |
| 16 | `tests/integration/memory/test_postgres_project_memory_next_action.py` |
| 17 | `tests/integration/workflow/test_postgres_kernel.py` |
| 18 | `tests/unit/cycle/test_project_memory_cycle_domain.py` |
| 19 | `tests/unit/next_action/test_next_action_domain.py` |

Aggregate serialization은 ordinal path sort 후 각 줄을
`<path>\t<lowercase_sha256>\n`, UTF-8로 만든 SHA-256이다.

---

# 6. 허용 범위

allowed_paths:

```text
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md

.aiassistant/tasks/active/
20260901_1601_aiscc-p1-8-prerequisite-owner-authority-exact-contract-and-source-enrollment-design-rework-1.md

.aiassistant/tasks/done/
20260901_1601_aiscc-p1-8-prerequisite-owner-authority-exact-contract-and-source-enrollment-design-rework-1.md

.aiassistant/reports/target/
20260901_1601_aiscc-p1-8-prerequisite-owner-authority-exact-contract-and-source-enrollment-design-rework-1/
```

allowed_actions:

- exact canonical/context/source read
- narrow source-symbol inventory read
- same prerequisite candidate rule update
- deterministic canonical payload/fingerprint calculation
- static Markdown/UTF-8/control-character/secret-signature validation
- ignored target export generation
- current Task active→done lifecycle
- read-only Git inspection

---

# 7. 절대 금지

forbidden_paths:

```text
src/**
tests/**
migrations/**

.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
.aiassistant/rules/AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md
.aiassistant/rules/AISCC_DURABLE_EVIDENCE_CONTENT_AUTHORITY.md
.aiassistant/rules/AISCC_HUMAN_GATE_JUDGMENT.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/records/aiscc/cycles/**
.aiassistant/reports/aiscc/**

.aiassistant/tasks/done/20260901_1527_aiscc-p1-8-next-action-context-terminal-canonical-git-reconciliation-audit-1.md
```

forbidden_actions:

- Git add/commit/amend/reset/restore/clean/rebase/merge/cherry-pick/push/fetch/pull
- branch/tag creation or mutation
- accepted Git object/history rewrite
- product runtime/source/test/migration mutation
- DB, HTTP runtime, browser, network, credential, provider, deployment action
- full suite 또는 비목표 runtime validation
- Human acceptance/status minting
- caller/config/Memory/proposal에 authority 부여
- old candidate hash를 semantic payload 변경 후 유지
- unrelated rules/records/source/log bulk-read
- 0813 removed Task forensic scope expansion

---

# 8. minimum authoritative context set

다음 exact path를 직접 읽는다.

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md

.aiassistant/rules/AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md
.aiassistant/rules/AISCC_DURABLE_EVIDENCE_CONTENT_AUTHORITY.md
.aiassistant/rules/AISCC_HUMAN_GATE_JUDGMENT.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/records/aiscc/cycles/20260831_1332_aiscc-p1-8-prerequisite-owner-authority-baseline-gap-hold-1.cycle.md
.aiassistant/records/aiscc/cycles/20260831_1332_aiscc-p1-8-prerequisite-owner-authority-exact-contract-gap-hold-1.cycle.md
.aiassistant/records/aiscc/cycles/20260831_1619_aiscc-p1-8-next-action-context-source-authority-final-acceptance-1.cycle.md

.aiassistant/reports/aiscc/20260831_1619_aiscc-p1-8-next-action-context-accepted-prerequisite-design-resume-handoff-1.md

.aiassistant/tasks/done/20260831_1332_aiscc-p1-8-prerequisite-owner-authority-contract-design-freeze-1.md
.aiassistant/tasks/done/20260831_1332_aiscc-p1-8-prerequisite-owner-authority-exact-contract-design-rework-1.md
.aiassistant/tasks/done/20260901_1527_aiscc-p1-8-next-action-context-terminal-canonical-git-reconciliation-audit-1.md
```

어떤 exact path가 현재 accepted baseline에 존재하지 않으면 이름이 비슷한 문서를 임의 대체하지 않는다.
read inventory에 `MISSING`으로 기록하고, 그 문서가 load-bearing authority라면 중단한다.

repository-root instruction entrypoint는 transport bootstrap이며 policy authority가 아니다. Project Rules UI 또는
automatic retrieval만으로 canonical body가 전달됐다고 가정하지 않는다.

---

# 9. authority-owner inventory

문서 변경 전에 current accepted source에서 다음 owner/symbol을 narrow-read하고 실제 exact owner graph를 표로
보고한다.

```text
TaskContract / external Command Center Task authority
Task constraint ref/event/currentness source

P1-4 WorkRun / TransitionRequest / TransitionEvaluation /
TransitionDecision / guard consumption / blocker representation

P1-6 TaskContractEvidenceAuthority /
durable structured-result requirement/checkpoint/content provenance

P1-7 Judgment/Human provenance

P1-8 ProjectMemory / NextAction catalog /
descriptor / eligibility / selection policy authority
```

각 항목을 다음 중 하나로 분류한다.

```text
EXISTING_EXACT_OWNER
EXISTING_BUT_INSUFFICIENT
ABSENT
```

Markdown에 이름이 존재한다는 사실만으로 runtime authority가 존재한다고 판단하지 않는다. 후보 rule이 새 owner
extension을 설계하는 경우 `DESIGN_ONLY / RUNTIME_NOT_IMPLEMENTED`를 명시한다.

---

# 10. Contract A — TaskConstraint exact scope and owner event

다음 accepted direction은 유지한다.

```text
TaskConstraint owner:
EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY extension

P1-8:
verifier/read port only

canonical-rule constraints:
NOT_SUPPORTED_V1
```

## 10.1 scope-specific cardinality

다음 세 scope variant 각각에 대해 exact field presence/cardinality를 닫는다.

```text
PROJECT
TASK_CONTRACT
WORK_RUN
```

각 variant에서 다음을 표로 명시한다.

```text
project_id: required/forbidden
task_contract_id: required/forbidden
task_contract_version: required/forbidden
work_run_id: required/forbidden
scope_id: exact derivation source or absence
```

implementation-dependent optional field, empty string, implicit sentinel을 허용하지 않는다. Schema variant에서
omit하거나 exact JSON `null` 의미를 canonical hashing에 포함하는 둘 중 하나를 명시적으로 선택한다.

## 10.2 immutable owner event

`TaskConstraintAuthorityEventV1` 또는 정확히 동등한 단 하나의 immutable owner event schema를 freeze한다.

최소 exact fields:

```text
event identity/ref/version/fingerprint
constraint ref/fingerprint
event kind = ISSUED | SUPERSEDED | REVOKED
replacement/superseding ref/fingerprint presence rule
project/scope identity
owner authority ID/version/revision
event sequence
effective sequence/time
current projection disposition
```

Pure revoke without replacement를 새 constraint object로 가장하지 않는다.

## 10.3 fail-closed fold/currentness

다음을 exact algorithm으로 freeze한다.

```text
exactly one ISSUED origin
monotonic owner event sequence
duplicate same event -> idempotent replay
conflicting duplicate -> authority conflict
SUPERSEDED -> exact replacement current candidate
REVOKED -> no current constraint
unknown/gap/out-of-order -> fail closed
```

Historical replay와 new admission을 분리한다.

```text
historical:
original ref + owner events through original high-watermark
-> original validity rederivation

new admission:
latest certified owner fold
-> exact current eligible ref only
```

## 10.4 private capability boundary

```text
external Command Center Task authority bootstrap/composition
-> opaque issue/supersede/revoke capability owner

P1-8
-> verifier/read port only

ordinary caller/runtime repository
-> cannot mint/revoke TaskConstraintRef or authority event
```

Process-local capability는 historical identity가 아니다. Durable owner payload/event provenance와 private live
capability boundary를 분리한다.

---

# 11. Contract B — P1-4 blocker taxonomy and resolved guard binding

다음 accepted ownership split은 유지한다.

```text
P1-4:
blocker identity/provenance owner
blocker-resolution transition provenance owner

P1-8:
resolution_cycle_id relation projection owner

blocker resolution transition:
not equal to final terminal ACCEPTED transition

V1 cardinality:
at most one ACTIVE blocker per WorkRun BLOCKED epoch
```

## 11.1 exact taxonomy

`blocker_kind`와 `reason_code`를 하나의 exact representation으로 닫는다.

허용 방식:

```text
A. one authoritative reason enum

or

B. exact BlockerKindV1 + exact BlockerReasonCodeV1
   with closed kind -> reason matrix
```

둘을 interchangeable alternative로 남기지 않는다. 기존 accepted P1-4 semantics와 실제 source representation에
가장 작은 compatible extension 하나를 선택하고 근거를 보고한다.

각 exact reason에 대해 다음을 고정한다.

```text
RESUMABLE | NON_RESUMABLE
allowed next/terminal paths
positive G_BLOCKER_RESOLVED allowed | forbidden
```

`NON_RESUMABLE`이 positive `G_BLOCKER_RESOLVED`를 emit할 수 있는지 명시적으로 답한다.

## 11.2 exact durable guard binding

`g_blocker_resolved_attestation_ref/fingerprint`가 가리키는 durable authority를 정확히 하나로 고정한다.

```text
Option A:
existing P1-4 TransitionEvaluation/TransitionDecision의
immutable typed guard-consumption binding

or

Option B:
exact P1_4BlockerResolvedAttestationV1
```

V1에서 양쪽을 interchangeable authority로 지원하지 않는다.

Exact binding에는 최소 다음이 포함되어야 한다.

```text
guard_id = G_BLOCKER_RESOLVED
blocker_ref/fingerprint
resolution_source_ref/fingerprint
same TaskContract/WorkRun/BLOCKED epoch
TransitionRequest/Evaluation/Decision refs/fingerprints
resulting state/version
owner event sequence
```

Resolution object, guard consumption, resolution transition, later terminal ACCEPTED transition의 ordering/replay와
same-lineage 검증을 freeze한다.

---

# 12. Contract C — accepted NEXT_ACTION_CONTEXT source enrollment

이 section은 source schema를 재설계하는 작업이 아니다. 다음 accepted rule과 exact SHA가 유일한 source authority
input이다.

```text
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
19b1d29a8f77ca5cc480a14bc9d1bdd53206951ccf8b34802316f1280dc61cb1
```

Accepted semantic owner:

```text
EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY /
NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY_V1
```

Exact accepted fingerprints:

```text
source contract:
c43c8560f785d765c677a8bce4310a4ae166e2a35913acc10ffc72ee883fa395

priority-source enrollment contract:
f2b090057ae3f5f00ed4ef878a41664e2322988190969458e6a6544f76932f6b

NextActionContextRefV1 schema:
c840402637e48de4914e28bf3e26802d7402915fa60fcc17d5a6b2098c72a11c

owner event schema:
d210552fa3bd27688ed74ad45a9869dc42dad6228dee8f5d0b8d850c758a50ea

P1-6 result schema:
f3aa618cc1fa06b73fa4467b73032f5d59dc1e6e4fe39fbc12c2bf0b5ae6a89b

Memory derivation:
82cdb2a5eab5dee63fd2050c6a23ea005be7147e292f1a6faadfc8d5f892a7a5
```

## 12.1 descriptor/ActionRef enrollment

Affected `CYCLE_DERIVED` descriptor와 selected `ActionRef` fingerprint가 최소 다음을 exact commit하도록
catalog/descriptor/eligibility contract를 수정한다.

```text
priority_classification_source_kind
priority_classification_source_ref
priority_classification_source_hash
priority_classification_source_contract_ref
priority_classification_source_contract_fingerprint
critical_path_ordinal
descriptor_policy_ordinal
```

`critical_path_ordinal`은 independently resolved external owner object ordinal의 enrolled equality copy다.

New selection에는 둘 다 필요하다.

```text
A. selection memory-applicability H에서 CURRENT인 exact
   NEXT_ACTION_CONTEXT ProjectMemoryEntry

B. selected current descriptor가 enroll한 exact current
   NextActionContextRefV1 ref/fingerprint + source-contract ref/fingerprint
```

ProjectMemory는 contextual/eligibility input이며 priority authority가 아니다. Memory class/ordinal copy는 equality
check일 뿐이다. Caller/config/proposal claim은 locator 또는 audit-only claim이며 authority가 아니다.

## 12.2 ranking authority

Class→rank mapping owner는 정확히 다음이다.

```text
P1_8_NEXT_ACTION_SELECTION_POLICY_AUTHORITY_V1
```

| external owner class | rank |
|---|---:|
| `ACCEPTED_CORE_CRITICAL_PATH` | 4 |
| `OPERATIONAL_HARDENING` | 5 |
| `OPTIONAL_OPTIMIZATION` | 6 |

Accepted ranking tuple을 변경하지 않는다.

```text
(
  authoritative_priority_rank,
  policy_dependency_ordinal,
  enrolled_critical_path_ordinal,
  descriptor_policy_ordinal,
  ActionRef lexical,
  proposal_id lexical
)
```

금지:

```text
source_memory_critical_path_ordinal 추가
descriptor_catalog_ordinal 추가
descriptor-local ranking dimension 추가
Memory/proposal/caller-owned class-to-rank mapping
```

Existing descriptor `critical_path_ordinal`은 external source ordinal의 enrolled equality copy로 읽고, tuple에서
`enrolled_critical_path_ordinal`로 해석한다. `descriptor_policy_ordinal`만 accepted descriptor-local tie-break다.

## 12.3 P1-6 boundary

P1-6는 durable bytes/schema/admission/terminal-consumed provenance를 소유하지만 priority semantics를 소유하지
않는다.

```text
P1-6 Requirement fingerprint-schema extension:
NOT_REQUIRED_V1
```

이 결정을 유지한다. Accepted P1-6 rule 또는 requirement identity를 수정하지 않는다.

---

# 13. catalog/descriptor/policy fingerprint rework

V1 action inventory와 ownership은 유지한다.

```text
P1_8_POLICY_ACTION_CATALOG_V1
owner-authored immutable catalog
caller/config cannot define descriptors

open-operational-recovery-task-issuance
open-cycle-derived-task-issuance

both output:
TaskIssuanceCandidate only

Task issuance owner:
EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY

both:
AFTER_TASK_ISSUANCE_P1_7
```

Predecessor fingerprints는 비교 기준일 뿐 accepted authority가 아니다.

```text
catalog:
57c2b89286311038faae9d780ae5572124cc850065a0012954e2f8eefdea121c

operational parameter schema:
92fe98cbc7cae63ab1f72161b625eb9bbd3281592f7731f98d24f30b4dd326f1

cycle-derived parameter schema:
3e4407fef8f429031038018d8ee8fab0cb91ad583277f28e0d75064b226ea646

priority policy:
f7c69da9e2e4ad8fadc93d813703023c63c712ab8662b7aa29402e0a7217d315
```

Accepted source enrollment로 semantic payload가 바뀌는 모든 항목을 재계산한다.

최소 inventory:

```text
catalog canonical payload/fingerprint
each affected action descriptor payload/fingerprint
each affected ActionRef
operational parameter schema fingerprint
cycle-derived parameter schema fingerprint
eligibility policy payload/fingerprint
selection/priority policy payload/fingerprint
source-contract/enrollment bindings
```

변하지 않는 hash는 canonical payload가 byte-for-byte/semantic-equivalent로 불변인 이유를 항목별로 증명한다.
Semantic payload가 바뀐 경우 old hash 유지 금지.

작성자가 문서에 기입한 값과 독립 verifier 재계산 값을 분리하여 보고한다. Canonicalization algorithm, exact
payload bytes/serialization, calculated SHA-256를 `FINGERPRINT_EVIDENCE.md`에 기록한다. 모든 affected hash의
writer value와 independent verifier value가 일치해야 한다.

---

# 14. historical replay and current applicability

세 owner graph의 historical replay/current applicability를 분리한다.

## TaskConstraint

```text
original TaskConstraintRef
+ owner events through original admission high-watermark
-> original validity

latest certified owner fold
-> new-admission current applicability
```

## blocker

```text
blocker object
+ exact guard-consumption binding
+ resolution transition object
+ later terminal ACCEPTED transition
+ current P1-8 Cycle relation
-> same-lineage deterministic rederivation
```

Resolution transition과 terminal ACCEPTED transition을 하나의 ref로 overload하지 않는다.

## NEXT_ACTION_CONTEXT

Accepted source rule의 replay semantics를 그대로 참조한다.

```text
producer/body high-watermark:
AUTHORING_SNAPSHOT_PROVENANCE_ONLY

terminal external-context currentness:
NOT_REQUIRED_V1

historical provenance:
not equal to current applicability
```

Historical selection은 original CURRENT Memory at selection H, original ActionRef/descriptor enrollment, exact
external context payload/currentness at selection H, class/ordinal, selection-policy mapping과 accepted tuple을
재검증한다. Later revoke/supersede는 historical identity를 rewrite하지 않는다.

---

# 15. exact questions — 전부 명시적으로 답할 것

1. 각 TaskConstraint scope kind에서 어떤 field가 required/forbidden인가?
2. Pure constraint revocation을 표현하는 exact object는 무엇인가?
3. TaskConstraint owner-event fold/high-watermark algorithm은 무엇인가?
4. TaskConstraint issue/supersede/revoke capability를 P1-8/caller에서 어떻게 숨기는가?
5. Exact `blocker_kind` 값은 무엇인가, 또는 왜 단일 enum으로 제거했는가?
6. Exact `reason_code` 값은 무엇인가, 또는 왜 단일 enum으로 통합했는가?
7. Separate enum이면 exact kind→reason closed matrix는 무엇인가?
8. 각 blocker reason은 RESUMABLE/NON_RESUMABLE 중 무엇인가?
9. NON_RESUMABLE blocker가 positive `G_BLOCKER_RESOLVED`를 emit할 수 있는가?
10. `g_blocker_resolved_attestation_ref`가 identify하는 exact durable object/binding은 무엇인가?
11. 어떤 exact descriptor fields가 `NextActionContextRefV1` source를 enroll하는가?
12. External source ref/hash와 source-contract ref/fingerprint의 currentness/equality 검증 순서는 무엇인가?
13. `priority_class`와 authoritative ordinal의 owner는 누구인가?
14. ProjectMemory와 descriptor ordinal copy는 어떤 equality-only 역할인가?
15. Accepted class→rank mapping owner와 exact tuple은 무엇인가?
16. 어떤 catalog/descriptor/ActionRef/policy/schema fingerprint가 변경됐고 왜 변경됐는가?
17. 어떤 fingerprint가 불변이고 왜 불변인가?
18. Historical replay와 current applicability는 각 owner graph에서 어떻게 분리되는가?
19. P1-6 Requirement fingerprint extension이 여전히 불필요한 이유는 무엇인가?
20. Human-owned semantic choice가 하나라도 열려 있는가?

암묵적 답, 복수 선택지 유지, `implementation may choose`를 허용하지 않는다.

---

# 16. workflow transition expectation

- initial_state: `BLOCKED_REQUIRED_EVIDENCE / PREREQUISITE_DESIGN_REWORK_AUTHORIZED`
- expected_non_terminal_state_when_human_pending: `CANDIDATE / HUMAN_REVIEW_REQUIRED`
- expected_terminal_candidate: `NOT_APPLICABLE_IN_EXECUTOR_TURN`
- transition_authority: `HUMAN / COMMAND_CENTER`
- Agent가 직접 terminal state를 결정할 수 있는가: `No`

Executor는 candidate SHA와 evidence만 제출한다. Human이 exact SHA를 accept하기 전에는 prerequisite design을
accepted/closed로 표시하지 않는다. Owner runtime 또는 P1-8 runtime resume authority를 추론하지 않는다.

---

# 17. evidence contract

executor_required:

- channel: `STATIC_DESIGN_CONFORMANCE`
  scope: `three exact prerequisite contracts, accepted-owner compatibility, closed question set`
  allowed_command_or_environment: `local read-only source inspection and deterministic local hashing`
  pass_condition: `all exact questions closed; no accepted-authority contradiction`

- channel: `FINGERPRINT_RECOMPUTATION`
  scope: `all affected canonical payloads/descriptors/ActionRefs/policies/schemas`
  allowed_command_or_environment: `local deterministic scripts/commands; no network`
  pass_condition: `writer values == independent verifier values; payload/canonicalization recorded`

- channel: `WORKSPACE_AND_PRESERVATION`
  scope: `HEAD/index/allowed paths/runtime aggregate/accepted files/prior audit Task`
  allowed_command_or_environment: `read-only Git and byte hashing`
  pass_condition: `no unexpected delta; final index empty; preserved identities exact`

- channel: `EXPORT_INTEGRITY`
  scope: `Task/report/candidate/fingerprint evidence/manifest source-copy identity`
  allowed_command_or_environment: `local filesystem validation`
  pass_condition: `all required root files; UTF-8/control-character/secret scan PASS; byte identity PASS`

reuse_allowed:

- channel: `TERMINAL_GIT_RECONCILIATION`
  predecessor: `20260901_1527 audit — ACCEPTED / CLOSED`
  provenance_condition: `exact Commit A/B and prior audit done Task identity preserved`
  applicability_condition: `used only for terminal Git/source authority baseline; not runtime evidence`

- channel: `ACCEPTED_SOURCE_AUTHORITY`
  predecessor: `AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md @ 19b1d29...`
  provenance_condition: `exact accepted Commit A blob identity`
  applicability_condition: `read-only semantic input to prerequisite enrollment`

human_owned:

- channel: `PREREQUISITE_DESIGN_FINAL_REVIEW`
  scope: `new exact candidate path + SHA + semantic closure`
  expected_result_format: `ACCEPTED | REWORK_REQUIRED | REJECTED with exact candidate SHA`

not_required:

- channel: `UNIT_INTEGRATION_RUNTIME_DB_BROWSER_NETWORK_DEPLOYMENT`
  reason: `design-only Task; runtime candidate must remain byte-identical`

forbidden:

- action_or_channel: `GIT_MUTATION_OR_REMOTE`
  reason: `design candidate and Human review must precede terminal persistence`

- action_or_channel: `HUMAN_ACCEPTANCE_BY_EXECUTOR`
  reason: `Human-owned evidence cannot be self-issued`

proof_non_substitution:

- `candidate document completeness != Human acceptance`
- `hash equality != semantic acceptance`
- `accepted source contract != prerequisite catalog enrollment completion`
- `static design conformance != owner runtime implementation`
- `1527 Git reconciliation != P1-8 runtime acceptance`

---

# 18. conformance reporting

- applicability: `REQUIRED`
- applicable policy_or_invariant: `cross-owner authority separation, fail-closed currentness, immutable provenance, no authority laundering`
- required_actual_owner: `external Task authority / P1-4 / P1-6 / P1-7 / P1-8 policy owners as explicitly assigned`
- planned_vs_actual_scope: `candidate rule + Task lifecycle + ignored target only`
- rollback_or_failure_semantics: `restore predecessor candidate bytes only if local edit fails before report; do not use destructive Git commands; otherwise submit BLOCKED bundle`

Project context impact:

```text
architecture: UPDATE_REQUIRED_IN_CANDIDATE_ONLY
orchestration_contract: INVESTIGATE_AND_BIND_WITHOUT_ACCEPTED_RULE_MUTATION
security_sandbox: PRIVATE_CAPABILITY_BOUNDARY_DESIGN_REQUIRED
public_provenance: TASK_AND_EXPORT_ONLY_UNTIL_HUMAN_REVIEW
```

---

# 19. accept 기준

다음을 모두 만족해야 `CANDIDATE / HUMAN_REVIEW_REQUIRED`로 제출한다.

- preflight exact PASS
- only allowed candidate rule changed
- TaskConstraint scope/event/fold/capability contract exact
- blocker taxonomy/resumability/guard binding exact and single-choice
- accepted source rule exact SHA preserved
- exact `NextActionContextRefV1` enrollment reflected in affected catalog/descriptor/eligibility/selection payloads
- ProjectMemory remains contextual/eligibility-only
- accepted class→rank mapping and ranking tuple preserved
- no `source_memory_critical_path_ordinal` or new ranking dimension
- P1-6 Requirement extension remains `NOT_REQUIRED_V1`
- all affected fingerprints independently recomputed and match
- all 20 exact questions answered without open alternatives
- runtime 19 paths/aggregate unchanged
- prior 1527 done Task and audit target preserved
- no canonical state/Cycle/source/runtime mutation
- no Git action; final HEAD exact; final index empty
- final done Task added as the only new non-runtime dirty path
- export integrity PASS

---

# 20. hold/reject 기준

다음 중 하나면 candidate-ready로 과장하지 않는다.

- accepted P1-4/P1-6/P1-7 authority와의 unresolved conflict
- TaskConstraint owner/event/currentness schema를 exact하게 닫을 수 없음
- blocker taxonomy 또는 durable guard owner binding이 복수 선택지로 남음
- accepted source enrollment을 descriptor/ActionRef/policy payload에 exact 반영할 수 없음
- canonical payload/fingerprint independent recomputation 불일치
- Human-owned semantic decision이 여전히 load-bearing하게 열림
- predecessor/accepted source/runtime/audit artifact drift
- unexpected dirty/staged path
- runtime/source/test/migration 변경 필요
- evidence scope expansion 필요

Correct result:

```text
BLOCKED_REQUIRED_EVIDENCE / IMPLEMENTATION_BASELINE_GAP
```

또는 collision/drift 유형이면:

```text
STOP / REVIEWED_CANDIDATE_DRIFT_OR_WORKSPACE_COLLISION
```

---

# 21. mandatory stop 조건

- policy baseline conflict
- missing required authority artifact
- dirty workspace collision
- forbidden action/tool request
- security/private capability boundary uncertainty
- `EVIDENCE_SCOPE_EXPANSION_REQUIRED`
- Human decision required before further mutation
- accepted source contract reinterpretation required
- P1-4/P1-6/P1-7 canonical mutation required
- runtime implementation required

Named blocker 이후에는 최소 source evidence, workspace inventory, report/export와 안전한 종료만 수행한다.

---

# 22. 변경/output

Update exactly one candidate rule:

```text
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
```

새 competing prerequisite rule을 만들지 않는다.

Canonical state/decision/next/Cycle는 이번 Task에서 변경하지 않는다.

작업 종료 시 active Task를 exact done path로 이동한다.

```text
.aiassistant/tasks/done/
20260901_1601_aiscc-p1-8-prerequisite-owner-authority-exact-contract-and-source-enrollment-design-rework-1.md
```

Expected final Git dirty set:

```text
19 blocked runtime paths
+ updated prerequisite candidate 1 path
+ preserved 1527 audit done Task 1 path
+ current design done Task 1 path
= 22 exact paths
```

Final index must remain empty. Final HEAD must remain
`683aaee84d1fc09e9371dd214efc3ff58b7225ee`.

---

# 23. 보고서 필수 항목

- 작업명 / work type / active→done Task path
- initial/final HEAD, branch, index
- initial/final exact dirty inventory and delta
- read canonical paths and missing path classification
- owner/symbol inventory with `EXISTING_EXACT_OWNER | EXISTING_BUT_INSUFFICIENT | ABSENT`
- predecessor candidate SHA and new candidate SHA
- accepted source SHA and six exact accepted fingerprints
- all 20 exact question answers
- TaskConstraint scope table/event schema/fold/capability result
- blocker enum or matrix/resumability/guard binding result
- catalog/descriptor/ActionRef/eligibility/selection policy change inventory
- old→new fingerprint table with changed/unchanged rationale
- writer-vs-independent-verifier result
- product/runtime source changes: must be none
- governance/provenance changes: candidate rule + current done Task only
- repository configuration changes: must be none
- evidence classification: executed/reused/human-owned/not-required/forbidden
- Agent claim vs admitted/Human evidence separation
- planned-vs-actual conformance
- mandatory stop/scope expansion
- unverified items
- rollback/revert guide without destructive Git commands
- preserved artifact exact paths
- Human verification requirement and exact candidate SHA

---

# 24. export bundle 요구

Target:

```text
.aiassistant/reports/target/
20260901_1601_aiscc-p1-8-prerequisite-owner-authority-exact-contract-and-source-enrollment-design-rework-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
FINGERPRINT_EVIDENCE.md
```

Required project-relative copies:

```text
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md

.aiassistant/tasks/done/
20260901_1601_aiscc-p1-8-prerequisite-owner-authority-exact-contract-and-source-enrollment-design-rework-1.md
```

Manifest에 다음을 기록한다.

```text
source/copy SHA-256 and byte identity
accepted source SHA preservation
predecessor/new candidate SHA
runtime 19-path aggregate preservation
prior 1527 done Task SHA preservation
initial/final HEAD/index/dirty inventory
all bundle path/size/SHA-256
encoding/control-character/secret-signature scan
```

Accepted source rule과 predecessor HOLD/final handoff를 bundle에 추가 복사할 필요는 없다. Report가 exact path/SHA를
기록하고 repository source를 직접 읽는다.

---

# 25. 사람 검증 요구

Executor 제출 후 Human/Command Center가 새 candidate exact SHA를 독립 검토한다.

필수 Human 결과 형식:

```text
Human P1-8 prerequisite owner-authority design final review
candidate path: <exact path>
candidate SHA-256: <exact sha256>
판정: ACCEPTED | REWORK_REQUIRED | REJECTED
```

Human `ACCEPTED` 이전 상태:

```text
P1-8 prerequisite owner-authority design:
CANDIDATE / HUMAN_REVIEW_REQUIRED

P1-8 Runtime:
BLOCKED_REQUIRED_EVIDENCE
```

Human acceptance가 생겨도 별도 owner runtime Task와 그 acceptance 없이 P1-8 runtime을 자동 재개하지 않는다.

---

# 26. 최종 응답 형식

1. result: `completed-candidate / blocked / rejected-candidate`
2. target bundle path
3. predecessor candidate SHA → new candidate SHA
4. changed files
5. removed files
6. fingerprint verification summary
7. runtime preservation result
8. HEAD/index/Git action result
9. Human verification
10. unverified items
11. preserved artifact exact paths
