# 작업지시서: P1-8 JCS Safe-Integer Cross-Contract Fingerprint Reconciliation Design Rework

## meta

- task_id: `20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-design-rework-1`
- created_at: `2026-09-01T16:52:00+09:00`
- phase: `P1-8 Runtime Prerequisite Authority Contracts`
- work_type: `DESIGN_REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `CROSS_OWNER / AISCC_COMMAND_CENTER`
- expected_start_head: `683aaee84d1fc09e9371dd214efc3ff58b7225ee`
- historical_source_commit: `35901125cc5842734cf1e8eb3374d10e4ee866e3`
- terminal_governance_commit: `683aaee84d1fc09e9371dd214efc3ff58b7225ee`
- source_rule_path: `.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md`
- source_rule_predecessor_sha256: `19b1d29a8f77ca5cc480a14bc9d1bdd53206951ccf8b34802316f1280dc61cb1`
- prerequisite_rule_path: `.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md`
- prerequisite_predecessor_sha256: `189156a190a13c92830d5b4c7ae28cd41f52f6c438dacda9e145bc82dd2d36d7`
- command_center_hold_cycle_path: `.aiassistant/records/aiscc/cycles/20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-hold-1.cycle.md`
- command_center_hold_cycle_sha256: `82e3ddf378ff820479cd18625e93a0b2968d79a3162dac48ffb639aecc6bec72`
- blocked_runtime_path_count: `19`
- blocked_runtime_aggregate_sha256: `84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42`
- runtime_implementation: `FORBIDDEN`
- git_mutation: `FORBIDDEN`
- human_joint_design_review: `PENDING`

---

# 1. 현재 Command Center 판정

```text
1601 prerequisite candidate:
REWORK_REQUIRED / FINGERPRINT_CANONICALIZATION_CONTRACT_MISMATCH

NEXT_ACTION_CONTEXT Source Authority accepted Commit A/B lineage:
HISTORICALLY_PRESERVED

source contract for future implementation:
REOPENED_FOR_NARROW_JCS_CORRECTION / HUMAN_REVIEW_REQUIRED

P1-8 prerequisite owner-authority design:
HOLD_REWORK_REQUIRED

P1-8 Runtime:
BLOCKED_REQUIRED_EVIDENCE
```

이번 Task는 발견된 JCS safe-integer defect만 두 rule에서 dependency-consistent하게 고친다. Commit A/B 또는
기존 terminal Cycle을 amend/rewrite하지 않는다.

---

# 2. purpose

다음 네 submitted/accepted canonical payload가 `9223372036854775807`을 JSON number로 포함하면서
`JCS_RFC8785`를 선언하여 cross-language canonical hash가 불일치한다.

```text
accepted NEXT_ACTION_CONTEXT owner event schema
accepted NEXT_ACTION_CONTEXT P1-6 result schema
1601 TaskConstraint authority event schema
1601 TaskConstraint owner snapshot schema
```

V1 sequence/high-watermark JSON integer maximum을 exact JCS safe integer로 고치고, 두 rule의 모든 direct/
transitive fingerprint를 dependency order로 재계산한다.

```text
old maximum:
9223372036854775807

new exact maximum:
9007199254740991
```

두 수정 rule을 joint candidate로 제출한다.

```text
JOINT_CANDIDATES / HUMAN_REVIEW_REQUIRED
```

Human acceptance를 생성하거나 runtime resume를 선언하지 않는다.

---

# 3. normative correction decision

RFC 8785 section 3.1은 canonicalization input JSON number가 IEEE-754 double precision으로 표현 가능해야
한다고 정한다. 더 긴 integer는 string subtype을 사용하도록 권고한다. Appendix B/D도 integer
interoperability와 `9223372036854775807` 예제를 명시한다.

```text
https://datatracker.ietf.org/doc/html/rfc8785#section-3.1
https://datatracker.ietf.org/doc/html/rfc8785#appendix-B
https://datatracker.ietf.org/doc/html/rfc8785#appendix-D
```

이번 V1 correction은 다음 하나로 고정한다.

```text
sequence/high-watermark type:
JSON integer

minimum:
existing exact minimum 유지

maximum:
9007199254740991

canonicalization:
JCS_RFC8785 그대로 유지
```

선택하지 않는 대안:

```text
decimal string subtype
BigInt JSON extension
arbitrary-precision lexical hashing
custom AISCC JCS dialect
unsafe integer retention
```

Runtime이 아직 구현되지 않았으므로 migration/backfill/compatibility alias는 만들지 않는다.

---

# 4. mandatory preflight

작업 전 다음을 모두 검증한다.

```text
branch:
main

HEAD:
683aaee84d1fc09e9371dd214efc3ff58b7225ee

index:
empty

source rule predecessor:
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
19b1d29a8f77ca5cc480a14bc9d1bdd53206951ccf8b34802316f1280dc61cb1

prerequisite predecessor:
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
189156a190a13c92830d5b4c7ae28cd41f52f6c438dacda9e145bc82dd2d36d7

1601 done Task:
.aiassistant/tasks/done/20260901_1601_aiscc-p1-8-prerequisite-owner-authority-exact-contract-and-source-enrollment-design-rework-1.md
8fe75a5a948ac73909560163cedd4debab6ac9d7be6f07755b1916eaf175fcc4

Command Center HOLD Cycle:
.aiassistant/records/aiscc/cycles/20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-hold-1.cycle.md
82e3ddf378ff820479cd18625e93a0b2968d79a3162dac48ffb639aecc6bec72

blocked runtime:
19 paths /
84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42
```

Pre-lifecycle Git dirty set은 다음 23개 exact path만 허용한다.

```text
19 blocked runtime paths
+ prerequisite candidate 1
+ preserved 1527 done Task 1
+ preserved 1601 done Task 1
+ current Command Center HOLD Cycle 1
= 23
```

Source rule은 preflight에서 Commit B와 byte-identical clean tracked path여야 한다. Current active Task와 ignored
target은 Git dirty count에서 제외한다.

Mismatch, staged path 또는 unexpected path가 있으면 mutation 전에:

```text
STOP / REVIEWED_CANDIDATE_DRIFT_OR_WORKSPACE_COLLISION
```

으로 보고한다.

---

# 5. preserve accepted/historical boundary

다음을 historical immutable lineage로 보존한다.

```text
Commit A:
35901125cc5842734cf1e8eb3374d10e4ee866e3

Commit B:
683aaee84d1fc09e9371dd214efc3ff58b7225ee

.aiassistant/records/aiscc/cycles/
20260831_1619_aiscc-p1-8-next-action-context-source-authority-final-acceptance-1.cycle.md

.aiassistant/reports/aiscc/
20260831_1619_aiscc-p1-8-next-action-context-accepted-prerequisite-design-resume-handoff-1.md
```

Old accepted source SHA는 historical predecessor다. 수정 후 old SHA를 current implementation authority라고
표현하지 않는다. 새 source bytes는 Human reacceptance 전 `REWORK_CANDIDATE / HUMAN_REVIEW_REQUIRED`다.

1601 candidate에서 JCS defect와 dependency fingerprint 외 다음 의미론은 유지한다.

```text
three exact TaskConstraint scope variants
separate immutable ISSUED/SUPERSEDED/REVOKED event
certified complete-prefix fold
private external Task issue/supersede/revoke capability

closed blocker kind/reason one-to-one matrix
SECURITY_BOUNDARY = NON_RESUMABLE
single P1_4BlockerResolvedAttestationV1 durable authority
resolution transition != later terminal ACCEPTED transition
P1-8 alone owns resolution_cycle_id relation

external NEXT_ACTION_CONTEXT owner owns priority class/ordinal
ProjectMemory is contextual/equality-only
selection policy owns class-to-rank
accepted six-field ranking tuple
no placeholder context-bound descriptor/ActionRef
P1-6 Requirement extension = NOT_REQUIRED_V1
```

---

# 6. 허용 범위

allowed_paths:

```text
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md

.aiassistant/tasks/active/
20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-design-rework-1.md

.aiassistant/tasks/done/
20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-design-rework-1.md

.aiassistant/reports/target/
20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-design-rework-1/
```

allowed_actions:

- exact canonical/source read
- two exact rule edits
- deterministic JCS recomputation
- local Node plus independent second-language verifier
- read-only Git/hash/encoding/secret scan
- ignored target generation
- current Task active→done lifecycle

---

# 7. 절대 금지

forbidden_paths:

```text
src/**
tests/**
migrations/**

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
.aiassistant/tasks/done/20260901_1601_aiscc-p1-8-prerequisite-owner-authority-exact-contract-and-source-enrollment-design-rework-1.md
```

The current active→done Task lifecycle is the only exception to the `tasks/done` wildcard boundary.

forbidden_actions:

- Git add/commit/amend/reset/restore/clean/rebase/merge/cherry-pick/push/fetch/pull
- branch/tag/history mutation
- runtime/source/test/migration/config mutation
- existing Cycle/state/decision/handoff mutation
- DB/browser/network/credential/provider/deployment action
- arbitrary-precision lexical bytes를 `JCS_RFC8785` 결과로 주장
- unsafe JSON numeric integer 유지
- old fingerprint retention after dependency payload change
- source semantics, ranking, taxonomy, owner split 또는 state machine redesign
- Human acceptance/status minting
- unrelated bulk-read 또는 evidence scope expansion

---

# 8. minimum authoritative context set

다음 exact path를 직접 읽는다.

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md

.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
.aiassistant/rules/AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md

.aiassistant/records/aiscc/cycles/20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-hold-1.cycle.md
.aiassistant/records/aiscc/cycles/20260831_1619_aiscc-p1-8-next-action-context-source-authority-final-acceptance-1.cycle.md

.aiassistant/reports/aiscc/20260831_1619_aiscc-p1-8-next-action-context-accepted-prerequisite-design-resume-handoff-1.md

.aiassistant/tasks/done/20260901_1601_aiscc-p1-8-prerequisite-owner-authority-exact-contract-and-source-enrollment-design-rework-1.md
```

External standard source:

```text
RFC 8785 sections 3.1, 3.2.2.3, Appendix B, Appendix D
```

Network fetch는 수행하지 않는다. Task/Cycle에 고정된 normative decision과 repository context를 사용한다.

---

# 9. correction A — accepted source rule

Update exactly:

```text
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
```

## 9.1 normative sequence grammar

모든 normative sequence/high-watermark JSON number 범위를 다음으로 통일한다.

```text
JSON integer 1..9007199254740991
```

`0`이 기존 schema에서 유효한 snapshot/Memory high-watermark minimum이면 그 exact minimum은 유지한다.

모든 canonical `json` payload에서 unquoted `9223372036854775807`을 제거한다. Historical comparison prose에 old
value를 기록할 수 있으나 current normative field 또는 canonical payload로 남기지 않는다.

## 9.2 dependency-order recomputation

다음 순서로 recompute한다.

```text
1. owner event schema
2. P1-6 result schema
3. NextActionContextRefV1 schema
4. source contract
5. Memory derivation
6. enrollment payload applicability check
```

Command Center reference calculation:

| source payload | expected corrected SHA-256 |
|---|---|
| owner event schema | `59e695623329908fdabce214a1d80be4249b4767c86844749de93094aeb7fce4` |
| P1-6 result schema | `db08fb7cbe1b55b7c686df28ffccbaf8462dd27dea7416e9b4478ae40e6cd67f` |
| context ref schema | `842ac2619a3069a0b844cbaf89d36ceb252bfe1f1ec149097727f224a6cdc307` |
| source contract | `988cdd4c71aca75e3434652044b50ffd703fb32ba4568219c56d52e498cd8698` |
| Memory derivation | `6de3e66a0d16a1dc0038838eb58b9ca0ca6c2d790ab3a5cdcab3802b5093b508` |
| priority-source enrollment | `f2b090057ae3f5f00ed4ef878a41664e2322988190969458e6a6544f76932f6b` |

Enrollment payload는 unsafe bound나 changed dependency fingerprint를 포함하지 않으므로 expected unchanged다.
실제 canonical payload가 이 최소 correction과 다르면 expected value를 억지로 맞추지 말고 semantic delta와
새 hash를 보고하여 중단한다.

## 9.3 status boundary

Document metadata/prose에 다음을 명확히 한다.

```text
historical accepted predecessor SHA = 19b1d29a...
current edited bytes = REWORK_CANDIDATE / HUMAN_REVIEW_REQUIRED
runtime = NOT_IMPLEMENTED
```

Old accepted Cycle/Commit identity는 그대로 참조한다.

---

# 10. correction B — prerequisite rule

Update exactly:

```text
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
```

## 10.1 direct safe-integer correction

다음 두 canonical schema의 maximum을 `9007199254740991`로 수정한다.

```text
TASK_CONSTRAINT_AUTHORITY_EVENT_SCHEMA_V1
TASK_CONSTRAINT_OWNER_SNAPSHOT_SCHEMA_V1
```

Command Center reference calculation:

| prerequisite payload | expected corrected SHA-256 |
|---|---|
| TaskConstraint ref schema | `c3bba5050a43a37c2563518d862a4b7fc1c3ee344cd763ab66da19d15a7126cc` |
| TaskConstraint event schema | `2b4bd41b7dbf7f002f2b48aabcf816ac386d860c12c20e947843bee5390c9b00` |
| TaskConstraint snapshot schema | `41330e2502ae9c337a3a1e8dfc693b2fb9307bec9eb5b5138e33ad7cdd35c1aa` |

TaskConstraint ref schema는 changed dependency가 없어 expected unchanged다.

## 10.2 source enrollment cascade

Section 9의 corrected source fingerprint graph를 exact input으로 반영하고 다음 순서로 recompute한다.

```text
context-bound descriptor schema
selection policy applicability check
parameter schemas applicability check
catalog
eligibility policy
operational descriptor
operational ActionRef
cycle-derived descriptor template
```

Command Center reference calculation:

| prerequisite payload | expected corrected SHA-256 |
|---|---|
| context-bound descriptor schema | `bef330ffba29c24a76910d22c2de514235224add40b2725d4ac342a25dc4a7ed` |
| ActionRef schema | `d173e426e651497abbf45ba4abb6f38bdc9e9d54e4b3a63e76c33aa9e7edb2a2` |
| selection policy | `4f84dbae89ee1113a2f6eeb28aa5d00100fcb65db2694b8716b52925d9bb312d` |
| operational parameter schema | `92fe98cbc7cae63ab1f72161b625eb9bbd3281592f7731f98d24f30b4dd326f1` |
| cycle parameter schema | `3e4407fef8f429031038018d8ee8fab0cb91ad583277f28e0d75064b226ea646` |
| catalog | `c02290f5111608efbd3cd12edec9e066ca622133f262a1352d971fcddf02e58c` |
| eligibility policy | `a0425bee1c2abf26c50a63ff125795e88e0b15e6f182dfbf716fc5f0217d6d03` |
| operational descriptor | `77bf03ba2125b32daef565739274a853cbfa03faab6477e37f4f9108517af8b0` |
| operational ActionRef | `a6a272fc7757439b7cc0877ace775d091539c25a4c3be8c0cd973cf2b746f157` |
| cycle-derived descriptor template | `7b766d3d3f3062381ebc1792cb4e4bc4768bf7be8963d8adff5b7e5a1bf29ddf` |

다음 blocker payload는 safe-integer/source dependency를 포함하지 않아 expected unchanged다.

```text
taxonomy:
ec170cd257b04e77410951abe8c7f196a88bf8f35d9e6deaec8d8889bb0e9d0c

provenance schema:
b984abd21d657015d3b3febbe55588762ee481ea93fcfff868114b09b5943329

resolved attestation schema:
0d92603174460dfd59be4b5bcb7a577014e8b51dad98fe992f08c3f638c43dbd
```

Concrete CYCLE_DERIVED descriptor/ActionRef count는 계속 exact zero다.

## 10.3 status boundary

Document metadata/prose에 다음을 명확히 한다.

```text
predecessor candidate SHA = 189156a...
current edited bytes = JOINT_REWORK_CANDIDATE / HUMAN_REVIEW_REQUIRED
runtime = NOT_IMPLEMENTED
```

---

# 11. independent JCS verification contract

`JCS_FINGERPRINT_EVIDENCE.md`에 모든 canonical payload를 full single-line JSON으로 기록한다.

두 independent verifier가 필요하다.

## Verifier A — ECMAScript reference behavior

```text
Node native JSON.parse
+ recursive UTF-16 property ordering
+ ECMAScript JSON number serialization/JSON.stringify semantics
+ UTF-8 SHA-256
```

모든 parsed integer에 대해:

```text
Number.isSafeInteger(value) == true
```

를 assert한다. Raw JSON text line hash를 JCS recomputation으로 대체하지 않는다.

## Verifier B — independent second language

Node와 코드를 공유하지 않는 Python/Java/other implementation을 사용한다.

필수 guard:

```text
no floating point
every integer within -9007199254740991..9007199254740991
recursive key sort compatible with UTF-16 ordering
exact compact JSON encoding
UTF-8/no BOM
```

현재 contract key와 values는 ASCII 범위이며, non-ASCII가 있으면 UTF-16 ordering과 JCS string serialization을
별도로 검증한다.

각 payload에 대해 다음을 보고한다.

```text
payload ID
canonical byte length
Verifier A hash
Verifier B hash
document-declared hash
match result
dependency inputs
changed/unchanged reason
```

`9223372036854775807`을 JSON number로 parse한 negative control도 실행한다.

Expected:

```text
Node Number.isSafeInteger = false
JSON serialization = 9223372036854776000
submitted lexical hash != strict JCS hash
```

두 rule의 모든 current normative `json` block에서 unsafe integer count가 `0`이어야 한다.

---

# 12. workflow transition expectation

- initial_state: `HOLD_REWORK_REQUIRED`
- expected_non_terminal_state_when_human_pending: `JOINT_CANDIDATES / HUMAN_REVIEW_REQUIRED`
- expected_terminal_candidate: `NOT_APPLICABLE_IN_EXECUTOR_TURN`
- transition_authority: `HUMAN / COMMAND_CENTER`
- Agent가 직접 terminal state를 결정할 수 있는가: `No`

두 candidate SHA가 모두 제출되어야 한다. 하나만 candidate-ready인 경우 전체 result는 blocked다.

---

# 13. evidence contract

executor_required:

- channel: `STRICT_JCS_RECOMPUTATION`
  scope: `two rules, every direct/transitive canonical payload`
  allowed_command_or_environment: `local Node + independent second language; no network`
  pass_condition: `all integers safe; two verifier hashes == document values; mismatch 0`

- channel: `DEPENDENCY_GRAPH_RECONCILIATION`
  scope: `source event/result/ref/source/Memory -> descriptor/catalog/eligibility/ActionRef cascade`
  allowed_command_or_environment: `deterministic local computation`
  pass_condition: `all dependency inputs exact; no stale fingerprint reference`

- channel: `STATIC_SEMANTIC_CONFORMANCE`
  scope: `1601 closed semantics preserved except numeric bound/fingerprint dependency changes`
  allowed_command_or_environment: `exact rule/source read`
  pass_condition: `no owner/ranking/taxonomy/state semantic drift`

- channel: `WORKSPACE_PRESERVATION`
  scope: `HEAD/index/runtime/prior tasks/HOLD Cycle/allowed paths`
  allowed_command_or_environment: `read-only Git and hashing`
  pass_condition: `expected exact final dirty set; runtime aggregate unchanged; index empty`

human_owned:

- channel: `JOINT_DESIGN_FINAL_REVIEW`
  scope: `corrected source rule exact SHA + corrected prerequisite rule exact SHA`
  expected_result_format: `separate ACCEPTED | REWORK_REQUIRED | REJECTED judgment for both exact SHAs`

not_required:

- channel: `UNIT_INTEGRATION_DB_HTTP_BROWSER_NETWORK_DEPLOYMENT`
  reason: `design-only fingerprint correction; runtime bytes remain blocked`

forbidden:

- action_or_channel: `GIT_MUTATION_OR_REMOTE`
  reason: `Human joint review precedes terminal persistence`

- action_or_channel: `HUMAN_ACCEPTANCE_BY_EXECUTOR`
  reason: `Human-owned evidence`

proof_non_substitution:

- `raw canonical-looking JSON bytes != RFC 8785 parse/serialize proof`
- `two hashes from shared unsafe-number semantics != independent interoperability proof`
- `corrected source candidate != Human reacceptance`
- `joint design acceptance != owner runtime implementation`
- `design correction != P1-8 runtime resume`

---

# 14. accept 기준

다음을 모두 만족해야 `JOINT_CANDIDATES / HUMAN_REVIEW_REQUIRED`로 제출한다.

- exact preflight PASS
- only two allowed rules changed
- every current normative sequence/high-watermark JSON number is safe integer
- no custom/arbitrary-precision JCS semantics
- source fingerprint graph recomputed in dependency order
- prerequisite fingerprint graph recomputed in dependency order
- Command Center reference values all match, or an exact semantic-delta blocker is reported instead
- Node reference and independent second-language verifier mismatch count 0
- negative unsafe-integer control PASS
- no stale old hash in current normative dependency refs
- 1601 owner/taxonomy/ranking semantics preserved
- P1-6 Requirement extension remains `NOT_REQUIRED_V1`
- concrete CYCLE_DERIVED descriptor/ActionRef count remains zero
- runtime 19 paths/aggregate unchanged
- HOLD Cycle and prior Task/report target preserved
- no state/Cycle/handoff/runtime/Git mutation
- final HEAD exact and final index empty
- export integrity PASS

---

# 15. hold/reject 기준

다음 중 하나면 joint candidate-ready로 과장하지 않는다.

- any unsafe JSON number remains
- verifier A/B/document hash mismatch
- stale transitive fingerprint reference
- accepted source semantics beyond numeric bound must change
- 1601 closed owner/ranking/taxonomy semantics drift
- only one rule can be reconciled
- unexpected dirty/staged path
- runtime/source implementation or migration required
- evidence scope expansion required
- Human-owned semantic choice remains open

Correct result:

```text
BLOCKED_REQUIRED_EVIDENCE / JCS_RECONCILIATION_INCOMPLETE
```

---

# 16. expected final workspace

Current Task 종료 후 expected Git dirty set:

```text
19 blocked runtime paths
+ corrected source rule 1
+ corrected prerequisite rule 1
+ preserved 1527 done Task 1
+ preserved 1601 done Task 1
+ current Command Center HOLD Cycle 1
+ current 1652 done Task 1
= 25 exact paths
```

```text
final HEAD:
683aaee84d1fc09e9371dd214efc3ff58b7225ee

final index:
empty
```

---

# 17. 보고서 필수 항목

- task/work type/active→done paths
- initial/final HEAD/branch/index/dirty inventory
- exact read paths
- source predecessor SHA → corrected candidate SHA
- prerequisite predecessor SHA → corrected candidate SHA
- old→new dependency graph table
- all Command Center expected vs actual fingerprints
- Verifier A/B implementation distinction and command summary
- per-payload byte length/hash/match
- unsafe-integer negative control output
- unsafe current canonical JSON number count
- preserved semantic decisions and actual semantic delta
- product/runtime/governance/config change classification
- Agent vs Human evidence separation
- unverified/not-implemented items
- forbidden-not-run
- rollback guide without destructive Git
- preserved artifact exact paths
- exact two-SHA Human review request

---

# 18. export bundle 요구

Target:

```text
.aiassistant/reports/target/
20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-design-rework-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
JCS_FINGERPRINT_EVIDENCE.md
```

Required project-relative changed copies:

```text
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md

.aiassistant/tasks/done/
20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-design-rework-1.md
```

Manifest:

- source/copy SHA and byte identity
- predecessor/candidate two-rule SHA
- HOLD Cycle SHA preservation
- runtime aggregate preservation
- all bundle file path/size/SHA
- Task source/root/path copy identity and final LF presence
- UTF-8/BOM/control-character/Markdown/secret-signature checks
- initial/final workspace identity

---

# 19. 사람 검증 요구

Executor 제출 후 Human/Command Center는 두 SHA를 별도로 판정한다.

```text
Human NEXT_ACTION_CONTEXT source-authority JCS correction final review
candidate path: .aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
candidate SHA-256: <exact sha256>
판정: ACCEPTED | REWORK_REQUIRED | REJECTED

Human P1-8 prerequisite owner-authority JCS reconciliation final review
candidate path: .aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
candidate SHA-256: <exact sha256>
판정: ACCEPTED | REWORK_REQUIRED | REJECTED
```

두 판정이 모두 `ACCEPTED`여야 terminal persistence Task를 발행할 수 있다. 그 acceptance는 owner runtime이나
P1-8 runtime resume를 자동 승인하지 않는다.

---

# 20. 최종 응답 형식

1. result: `completed-joint-candidates / blocked / rejected-candidate`
2. target bundle path
3. source predecessor SHA → candidate SHA
4. prerequisite predecessor SHA → candidate SHA
5. fingerprint reconciliation summary
6. changed/removed files
7. runtime preservation
8. HEAD/index/Git action
9. Human joint verification
10. unverified/not-implemented items
11. preserved exact paths
