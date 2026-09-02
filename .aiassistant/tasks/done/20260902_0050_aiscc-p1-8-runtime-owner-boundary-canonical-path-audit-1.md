# 작업지시서: P1-8 Runtime Owner Boundary Canonical Path Audit

## meta

- task_id: `20260902_0050_aiscc-p1-8-runtime-owner-boundary-canonical-path-audit-1`
- created_at: `2026-09-02T00:50:00+09:00`
- phase: `P1-8 Project Memory and Cycle Admission Runtime`
- work_type: `DISCOVERY_AUDIT / SOURCE_EVIDENCE_EXPORT`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `CROSS_OWNER_PREREQUISITE_RUNTIME_PATH_BOUNDARY`
- expected_start_branch: `main`
- expected_start_head: `1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a`
- predecessor_runtime_path_count: `19`
- predecessor_runtime_aggregate_sha256: `84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42`
- predecessor_task_result: `BLOCKED_REQUIRED_EVIDENCE / EVIDENCE_SCOPE_EXPANSION_REQUIRED / RUNTIME_PATH_BOUNDARY_INSUFFICIENT`
- human_p1_8_runtime_verification: `HUMAN_PENDING`
- recommended_executor_session: `NEW_CHAT_REQUIRED_BY_HUMAN`
- session_open_owner: `HUMAN`
- product_source_mutation: `FORBIDDEN`
- git_commit: `FORBIDDEN`
- git_push: `FORBIDDEN`

---

# 1. 목적

2359 runtime rework의 fail-closed 중단 사유를 repository 정본에서 독립 감사하고, 다음 runtime implementation
Task가 사용할 **exact mutation path boundary**를 확정 가능한 증거로 만든다.

이번 Task는 구현 Task가 아니다. 경로를 추측해 source를 만들거나 기존 owner에 새 권한을 끼워 넣지 않는다.
다음 세 영역의 실제 production owner와 composition/transaction 경계를 exact canonical path로 식별한다.

1. `EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY`의 TaskConstraint 및 NEXT_ACTION_CONTEXT source issuer/event/snapshot owner
2. `P1_4BlockerProvenanceV1` 및 `P1_4BlockerResolvedAttestationV1`이 실제 상태 전이와 원자적으로 기록될 P1-4 transaction owner
3. 위 두 owner를 P1-8 read/verifier-only 소비 경계와 연결할 production wiring 및 targeted test 경계

성공 결과는 다음뿐이다.

```text
PATH_BOUNDARY_AUDITED /
EXACT_EXPANDED_ALLOWLIST_PROPOSED /
COMMAND_CENTER_REVIEW_REQUIRED
```

이 결과는 runtime 구현·acceptance, Human acceptance, Git persistence, P2/P3 또는 Public Live를 의미하지 않는다.

---

# 2. 선행 판정과 Task 정체성

2359 제출 번들에 대한 Browser Command Center 독립 검증 결과:

```text
EXPORT_MANIFEST payload rows: 26 / 26 SHA-256 PASS

2359 Task SHA-256:
ca616a7193a69aabd8d12f9e265152187e83806828edc7568f428669093a73b6

2311 done Task SHA-256:
0795bd24b5d1b9531840424dbd7ba6c788fa08df3d19a21564e82250734fc1e7

runtime predecessor/final:
19 paths
84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42
mutation by 2359: 0
```

판정:

```text
BLOCKED_REQUIRED_EVIDENCE /
EVIDENCE_SCOPE_EXPANSION_REQUIRED /
RUNTIME_PATH_BOUNDARY_INSUFFICIENT
```

이는 runtime candidate rejection가 아니다. 2359가 mandatory stop을 정확히 수행한 결과다.

Predecessor done Task:

```text
.aiassistant/tasks/done/20260901_2359_aiscc-p1-8-runtime-prerequisite-authority-and-jcs-safe-integer-reconciliation-rework-1.md
SHA-256:
ca616a7193a69aabd8d12f9e265152187e83806828edc7568f428669093a73b6
```

---

# 3. session boundary

새 IDE Executor 채팅은 Human이 연다. Executor는 새 채팅을 열거나 전환할 수 없다.

새 채팅이 필요한 근거:

```text
predecessor work type:
RUNTIME_REWORK / ORCHESTRATION_IMPLEMENTATION

current work type:
DISCOVERY_AUDIT / SOURCE_EVIDENCE_EXPORT

the current audit must resolve canonical owner paths independently
without carrying forward an implementation turn's proposed path assumptions
```

Human이 새 채팅을 열고 이 Task를 exact active path에 배치한 뒤에만 Executor가 시작한다.

---

# 4. mandatory preflight

Repository:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center
```

작업 전 다음을 확인한다.

```text
branch == main
HEAD == 1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a
Git index == empty
2359 done Task exact path/SHA == expected
2311 done Task exact path/SHA == expected
accepted rule exact paths/SHA == expected
19-path runtime aggregate == 84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42
no unexpected dirty path outside the known 19 runtime paths and current Task lifecycle
```

불일치하면 source 조사 범위를 넓히지 말고 다음 중 정확한 blocker로 중단한다.

```text
BLOCKED_MISSING_ARTIFACT
POLICY_CONFLICT_INVESTIGATION_REQUIRED
DIRTY_WORKSPACE_MIXED
```

---

# 5. 읽을 canonical 문서

아래 exact path를 직접 읽는다.

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
.aiassistant/records/aiscc/cycles/20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-hold-1.cycle.md
.aiassistant/records/aiscc/cycles/20260901_2155_aiscc-p1-8-jcs-safe-integer-joint-design-final-acceptance-1.cycle.md
.aiassistant/reports/aiscc/20260901_2155_aiscc-p1-8-prerequisite-authority-accepted-runtime-resume-handoff-1.md
.aiassistant/tasks/done/20260901_2311_aiscc-p1-8-joint-design-terminal-git-object-reconciliation-audit-1.md
.aiassistant/tasks/done/20260901_2359_aiscc-p1-8-runtime-prerequisite-authority-and-jcs-safe-integer-reconciliation-rework-1.md
```

Accepted rule identities:

```text
AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
7cf27b77bb961280becfc55ecf8e71c9406da9b7b91df0d2697132c2655108db

AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
8b19970629c55629df1560f2329b529992eceb86d5e4216baf0b7e78d3876960
```

Task-listed 문서는 minimum authoritative context다. 관련 없는 rules/records/logs를 bulk-read하지 않는다.

---

# 6. read-only source 조사 범위

이번 Task는 경로 식별 감사이므로 다음 read-only inventory/search를 명시적으로 허용한다.

```text
rg --files src/aiscc tests migrations
targeted rg symbol/import searches under src/aiscc, tests, migrations
exact source reads reached by those imports/exports
git status --short
git diff --name-status
git diff --cached --name-status
git ls-files
git show / git cat-file for the fixed accepted commits and paths only when identity confirmation is needed
sha256sum / file-byte counts
```

Known starting points:

```text
pyproject.toml
src/aiscc/persistence/__init__.py
src/aiscc/workflow/kernel.py
src/aiscc/persistence/models.py
src/aiscc/judgment/authority.py
src/aiscc/memory/models.py
src/aiscc/memory/repository.py
src/aiscc/next_action/models.py
src/aiscc/next_action/repository.py
src/aiscc/cycle/models.py
src/aiscc/cycle/repository.py
tests/integration/workflow/test_postgres_kernel.py
tests/integration/evidence/test_postgres_evidence_admission.py
tests/integration/human/test_postgres_human_gate_judgment.py
tests/integration/memory/test_postgres_project_memory_next_action.py
```

`src/aiscc/persistence/__init__.py`의 export가 `PostgresTransitionRepository`를 다른 exact module로 연결하면 그
module을 읽고 기록한다. `src/aiscc/workflow/kernel.py`가 다른 owner/evaluator/repository port로 연결하면 그 exact
module을 따라간다.

새 production path 후보는 기존 package naming, import direction, private boundary와 test construction evidence로
도출한다. 이름을 먼저 정한 뒤 근거를 맞추지 않는다.

---

# 7. 필수 symbol/owner resolution

아래 symbol 또는 동등한 현재 구현을 exact path와 함께 조사한다.

```text
PostgresTransitionRepository
WorkflowKernel
TransitionEvaluator
TransitionDecision
CommandCenterAuthority
P1_8NextActionPolicyAuthority
ProjectMemory
NextAction
Cycle admission owner/repository
```

Accepted design이 요구하지만 현재 2359 allowlist에서 정의되지 않은 것으로 보고된 대상:

```text
TaskConstraintRefV1
TaskConstraintAuthorityEventV1
TaskConstraintOwnerSnapshotV1
P1_4BlockerProvenanceV1
P1_4BlockerResolvedAttestationV1
NextActionContextRefV1
NextActionContextAuthorityEventV1
```

각 대상에 대해 다음을 구분한다.

1. existing exact production owner path
2. existing port/interface path
3. existing persistence row/table path
4. existing composition/wiring path
5. existing targeted unit/integration test path
6. new file이 필요한 경우 exact proposed path와 package-convention 근거
7. P1-7 또는 P1-8 owner에 쓰기 권한을 넣지 않고 구현 가능한지

동일 이름 검색 결과 0건만으로 architecture 부재를 확정하지 않는다. 동등한 의미의 현재 type/owner/transaction
path도 확인한다.

---

# 8. P1-4 atomic transaction audit

다음을 source로 입증한다.

```text
BLOCKED admission의 실제 state mutation owner
decision admission과 state mutation의 transaction 시작/commit/rollback 경계
PostgresTransitionRepository와 WorkflowKernel의 책임 분리
P1_4BlockerProvenanceV1 append가 들어가야 할 exact production path
P1_4BlockerResolvedAttestationV1가 decision/state mutation과 원자적으로 기록될 exact production path
denial/rollback 시 attestation이 남지 않을 exact failure boundary
필요한 persistence model/migration/test exact paths
```

Accepted P1-4 ownership을 바꿔야만 구현 가능하다면 path proposal로 숨기지 말고:

```text
POLICY_CONFLICT_INVESTIGATION_REQUIRED /
P1_4_TRANSITION_OWNERSHIP_CHANGE_REQUIRED
```

로 중단한다.

---

# 9. external Task authority audit

`EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY`는 P1-7 `CommandCenterAuthority`와 P1-8 Memory/NextAction authority가 아니다.

다음을 source와 accepted rule로 대조한다.

```text
issuer/event/snapshot writer의 semantic owner
private composition boundary
P1-8에 노출되는 read/verifier-only port
current projection 및 restart-durable replay owner
TaskConstraint와 NextActionContext source enrollment의 transaction boundary
existing package가 적합한지 또는 새 package가 필요한지
new package가 필요하면 exact package/file path와 import-direction 근거
```

다음은 금지한다.

```text
P1-7 CommandCenterAuthority에 external Task-authority writer 권한 추가
P1-8 Memory/NextAction/Cycle owner에 external source writer 권한 추가
caller/config/Memory가 priority 또는 source authority를 제공
public P1-8 API가 issuer repository/writer를 직접 노출
```

---

# 10. exact expanded allowlist 산출물

`PATH_BOUNDARY_PROPOSAL.md`에 다음 표를 작성한다.

| requirement | semantic owner | exact path | EXISTING / NEW | next Task action | atomic/private-boundary reason | targeted proof path |
|---|---|---|---|---|---|---|

제안은 반드시 다음을 포함한다.

```text
exact production paths to modify
exact new production paths to create
exact persistence model and migration paths
exact composition/wiring paths
exact unit/integration/regression test paths
exact predecessor 19 paths that remain in scope
exact paths that must remain immutable
```

Wildcard, directory-only allowlist, `TBD`, `or equivalent`, basename-only 표기는 허용하지 않는다.

새 파일 경로는 실제 repository package convention으로 정당화한다. 하나 이상의 architecture 선택지가 남으면
임의로 하나를 선택하지 말고 선택지와 차이를 보고하고:

```text
BLOCKED_POLICY_GAP / COMMAND_CENTER_PATH_SELECTION_REQUIRED
```

로 종료한다.

---

# 11. mutation allowlist

허용되는 repository mutation은 current Task lifecycle과 ignored target bundle뿐이다.

```text
.aiassistant/tasks/active/20260902_0050_aiscc-p1-8-runtime-owner-boundary-canonical-path-audit-1.md
.aiassistant/tasks/done/20260902_0050_aiscc-p1-8-runtime-owner-boundary-canonical-path-audit-1.md
.aiassistant/reports/target/20260902_0050_aiscc-p1-8-runtime-owner-boundary-canonical-path-audit-1/**
```

Product source, test, migration, accepted rule, Cycle, handoff, state summary, decision register, next actions,
repository configuration은 모두 read-only다.

---

# 12. 절대 금지

```text
product source/test/migration edit/create/delete
accepted rule/Cycle/handoff/state/decision/next-actions edit
19-path runtime candidate edit/delete/rename
new owner implementation
schema/table/migration creation
test execution intended to prove unimplemented runtime
Git add/commit/push/fetch/pull/remote
reset/restore/clean/checkout/rebase/merge/cherry-pick
network/provider/credential/browser action
Human/Judgment/TransitionDecision minting
P2/P3/Public Live work
unrelated repository bulk-read
```

보고서 완성을 위해 금지 범위를 실행하지 않는다.

---

# 13. evidence contract

## executor_required

### STATIC_SOURCE

```text
scope:
repository-local import/export/symbol/transaction/composition resolution

pass condition:
every proposed expanded path is supported by exact source evidence
and no owner shoehorning or unresolved alternative remains
```

### PUBLIC_PROVENANCE

```text
scope:
branch/HEAD/index, Task lifecycle, accepted rule/Task identities,
19-path runtime identity, exact read inventory, no product mutation

pass condition:
all expected identities reproduce and final workspace has no unexpected mutation
```

### SOURCE_EVIDENCE_EXPORT

```text
scope:
export every exact source file used as load-bearing path evidence,
preserving repository-relative paths, plus proposal/report/inventory

pass condition:
manifest lists every exported file with bytes and SHA-256
```

## reuse_allowed

```text
2311 STATE_A_VERIFIED only when exact done Task and commit identities match
2359 bundle integrity and 19-path aggregate only when independently recomputed locally
accepted rule fingerprints only when exact rule bytes match
```

## human_owned

```text
final choice if more than one architecture path remains
runtime candidate acceptance
new IDE chat opening
```

현재 결과는 모두 `HUMAN_PENDING` 또는 `NOT_REQUIRED`이며 Executor가 완료했다고 주장하지 않는다.

## not_required

```text
unit/integration/PostgreSQL/Alembic runtime tests: no implementation mutation
browser/visual QA: no frontend work
network/provider/credential proof: out of scope
deployment/release: out of scope
```

## forbidden

```text
test or runtime output used as substitute for missing owner-path evidence
Agent claim used as Human acceptance
```

---

# 14. accept 기준

모두 만족해야 한다.

1. preflight exact identities PASS
2. 2359 blocker를 exact source/import/transaction evidence로 독립 확인 또는 반증
3. P1-4 actual transaction owner exact path 확정
4. external Task authority owner/private composition/read-verifier boundary exact path 확정
5. persistence/migration/wiring/test exact paths 확정
6. proposed next mutation allowlist에 wildcard/TBD/owner shoehorning 없음
7. 19 runtime candidate 바이트 불변
8. product source/test/migration mutation 0
9. complete target bundle과 manifest

성공 taxonomy:

```text
PATH_BOUNDARY_AUDITED /
EXACT_EXPANDED_ALLOWLIST_PROPOSED /
COMMAND_CENTER_REVIEW_REQUIRED
```

---

# 15. hold/block 기준

```text
BLOCKED_MISSING_ARTIFACT
POLICY_CONFLICT_INVESTIGATION_REQUIRED
DIRTY_WORKSPACE_MIXED
BLOCKED_POLICY_GAP / COMMAND_CENTER_PATH_SELECTION_REQUIRED
EVIDENCE_SCOPE_EXPANSION_REQUIRED
P1_4_TRANSITION_OWNERSHIP_CHANGE_REQUIRED
```

named blocker 이후에는 blocker를 입증하는 최소 read-only evidence, workspace inventory, report/export와 안전한
종료만 수행한다.

---

# 16. required target bundle

Target:

```text
.aiassistant/reports/target/20260902_0050_aiscc-p1-8-runtime-owner-boundary-canonical-path-audit-1/
```

Root files:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
PATH_BOUNDARY_PROPOSAL.md
SYMBOL_RESOLUTION_EVIDENCE.md
RUNTIME_INVENTORY.md
```

또한 load-bearing evidence로 읽은 exact source 파일을 repository-relative path 구조로 포함한다. Secret,
credential, DB dump, `.git`, unrelated source, browser mirror는 포함하지 않는다.

`EXPORT_MANIFEST.md`는 manifest 자신을 제외한 모든 payload path, bytes, copy SHA-256, exact source path,
source SHA-256, match 결과를 포함한다.

---

# 17. 보고서 필수 항목

1. task_id / work_type / result taxonomy
2. active→done Task lifecycle 및 exact SHA-256
3. branch/HEAD/index preflight
4. accepted rule/2311/2359 identity 결과
5. predecessor/final runtime path count와 aggregate
6. automatically discovered instruction과 explicit read inventory 구분
7. targeted source inventory와 exact SHA-256
8. `PostgresTransitionRepository` export→definition exact resolution
9. `WorkflowKernel` 및 P1-4 decision/state transaction exact resolution
10. external Task authority existing/new owner path resolution
11. P1-8 read/verifier-only boundary resolution
12. persistence/migration/composition/wiring path resolution
13. exact unit/integration/regression test path proposal
14. alternative architecture 존재 여부
15. product source/test/migration mutation count = 0
16. test/runtime channels `NOT_REQUIRED` 또는 `FORBIDDEN_NOT_RUN`
17. Human-owned items `HUMAN_PENDING`
18. unexpected dirty paths
19. export manifest count/hash result
20. unverified items
21. rollback guide
22. preserved exact paths

---

# 18. preserved exact paths

Accepted governance를 변경하지 않는다.

```text
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
.aiassistant/records/aiscc/cycles/20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-hold-1.cycle.md
.aiassistant/records/aiscc/cycles/20260901_2155_aiscc-p1-8-jcs-safe-integer-joint-design-final-acceptance-1.cycle.md
.aiassistant/reports/aiscc/20260901_2155_aiscc-p1-8-prerequisite-authority-accepted-runtime-resume-handoff-1.md
.aiassistant/tasks/done/20260901_2311_aiscc-p1-8-joint-design-terminal-git-object-reconciliation-audit-1.md
.aiassistant/tasks/done/20260901_2359_aiscc-p1-8-runtime-prerequisite-authority-and-jcs-safe-integer-reconciliation-rework-1.md
```

19-path runtime candidate 전체와 aggregate를 그대로 보존한다.

```text
19
84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42
```

---

# 19. 최종 응답 형식

```text
result:
target bundle path:
Task done path / SHA-256:
2359 blocker independently confirmed or contradicted:
P1-4 owner exact paths:
external Task authority exact paths:
P1-8 read/verifier exact paths:
expanded allowlist proposal result:
product mutation count:
runtime candidate count / aggregate:
tests/runtime evidence:
Human-owned items:
unverified items:
preserved exact paths:
```

