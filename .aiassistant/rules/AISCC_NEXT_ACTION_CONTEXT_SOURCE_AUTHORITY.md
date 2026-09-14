# AISCC NEXT_ACTION_CONTEXT Source Authority Contract

## 1. 문서 상태

| field | value |
|---|---|
| document_id | `AISCC-NEXT-ACTION-CONTEXT-SOURCE-AUTHORITY-DESIGN-2` |
| task_id | `20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-design-rework-1` |
| work_type | `DESIGN_REWORK` |
| design_status | `REWORK_CANDIDATE / HUMAN_REVIEW_REQUIRED` |
| acceptance_owner | `Human` |
| implementation_status | `DESIGN_ONLY / NOT_IMPLEMENTED` |
| accepted P1-8 design SHA-256 | `100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a` |
| predecessor prerequisite design SHA-256 | `556faad8a77d917fcbfc9ab7b0ba62bd65f985a6f4a1e585c08af668dd14393c` |
| predecessor source-authority design SHA-256 | `7dd7274f96d6565233c65f8ade5e81acd8b53f9d7425e377df148d5337d8f4e6` |
| historical accepted predecessor SHA-256 | `19b1d29a8f77ca5cc480a14bc9d1bdd53206951ccf8b34802316f1280dc61cb1` |
| blocked P1-8 runtime | `19 paths / 84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42` |

이 문서는 `NEXT_ACTION_CONTEXT`의 missing semantic source owner만 동결하는 candidate다. Human acceptance 전에는 runtime authority, accepted prerequisite rule의 replacement, migration authorization 또는 P1-8 runtime resume authorization이 아니다.

TaskConstraint exact scope/event와 P1-4 blocker taxonomy/guard-binding rework는 이 문서의 범위가 아니다. 기존 prerequisite candidate와 P1-4/P1-6/P1-7 authority semantics를 변경하지 않는다.

## 2. normative authority split

V1 semantic priority owner는 정확히 다음이다.

```text
context_owner = EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY
owner_extension = NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY_V1
authority_ref = external-command-center-task-authority:next-action-context-source:v1
authority_version = AISCC-EXTERNAL-COMMAND-CENTER-NEXT-ACTION-CONTEXT-AUTHORITY-V1
authority_revision = 1
```

이 owner를 선택하는 이유는 `accepted core critical path`, `operational hardening`, `optional optimization`과 Task 내부 ordering이 evidence storage fact가 아니라 Command Center/Task planning fact이기 때문이다. Repository에는 더 강한 기존 exact semantic owner가 없다.

Normative separation:

```text
P1-6 durable canonical JSON
!= semantic priority authority

P1-8 Memory policy / selector
!= semantic priority authority

NextActionProposal / descriptor configuration
!= semantic priority authority

NextActionContextRefV1
+ verified owner event history
= semantic priority authority

CURRENT ProjectMemoryEntry
= CYCLE_DERIVED contextual/eligibility input
!= priority authority by itself
```

P1-6은 bytes/admission/terminal-consumption provenance를 소유한다. P1-8은 source 선택, equality verification, Memory/MCF와 deterministic selection을 소유한다. 어느 쪽도 external owner 대신 priority fact를 mint하지 않는다.

## 3. exact common grammar

V1은 다음 grammar를 사용한다.

| name | exact rule |
|---|---|
| `AISCC_ID_V1` | ASCII regex `^[A-Za-z0-9][A-Za-z0-9._:/@-]{0,159}$`; case-sensitive |
| `AISCC_VERSION_V1` | ASCII regex `^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$`; case-sensitive |
| `CONTEXT_LOCAL_ID_V1` | ASCII lowercase regex `^[a-z0-9][a-z0-9._:@-]{0,159}$` |
| `CONTEXT_SLOT_ID_V1` | ASCII lowercase regex `^[a-z0-9][a-z0-9._-]{0,63}$` |
| fingerprint | exactly 64 lowercase hexadecimal characters |
| sequence | JSON integer `1..9,007,199,254,740,991` |
| timestamp | UTC `YYYY-MM-DDTHH:MM:SS.ffffffZ`, exactly six fractional digits; leap second forbidden |
| null | JSON `null`; empty string, `NONE`, omitted conditionally applicable field are forbidden where a variant requires null |

All immutable semantic payloads use UTF-8, Unicode NFC strings, no BOM and `JCS_RFC8785`. Integers are JSON integers; floating point is forbidden. Unknown fields are forbidden.

## 4. exact source contract identity

`NEXT_ACTION_CONTEXT_SOURCE_CONTRACT_V1` is the immutable schema contract that the external owner issues and P1-8 policy enrolls by exact fingerprint.

```json
{"canonicalization":"AISCC_CANONICAL_STRUCTURED_JSON_V1","class_to_rank_owner":"P1_8_NEXT_ACTION_SELECTION_POLICY_AUTHORITY_V1","context_ref_schema_fingerprint":"842ac2619a3069a0b844cbaf89d36ceb252bfe1f1ec149097727f224a6cdc307","contract_id":"NEXT_ACTION_CONTEXT_SOURCE_CONTRACT_V1","contract_version":"v1","critical_path_ordinal":{"maximum":1000000,"minimum":1,"ordering":"LOWER_VALUE_PRECEDES_WITHIN_SAME_PRIORITY_CLASS"},"cycle_id_in_owner_object":false,"event_schema_fingerprint":"59e695623329908fdabce214a1d80be4249b4767c86844749de93094aeb7fce4","owner":"EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY","owner_extension":"NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY_V1","priority_authority_role":"EXTERNAL_CANONICAL_PRIORITY_CLASSIFICATION_SOURCE","priority_classes":["ACCEPTED_CORE_CRITICAL_PATH","OPERATIONAL_HARDENING","OPTIONAL_OPTIMIZATION"],"priority_source_enrollment_contract_fingerprint":"f2b090057ae3f5f00ed4ef878a41664e2322988190969458e6a6544f76932f6b","privacy_class":"PRIVATE_INTERNAL","producer_high_watermark_role":"AUTHORING_SNAPSHOT_PROVENANCE_ONLY","project_memory_role":"CURRENT_CONTEXTUAL_ELIGIBILITY_INPUT_NOT_PRIORITY_AUTHORITY","ranking_ordinal_name":"enrolled_critical_path_ordinal","result_schema_fingerprint":"db08fb7cbe1b55b7c686df28ffccbaf8462dd27dea7416e9b4478ae40e6cd67f","result_schema_id":"P1_8_NEXT_ACTION_CONTEXT_RESULT_V1","result_schema_version":"v1","scope_kind":"TASK_CONTRACT","security_class":"INTERNAL_REFERENCE_ONLY","selector":"/next_action_context","terminal_currentness_requirement":"NOT_REQUIRED_V1"}
```

Canonical SHA-256:

```text
988cdd4c71aca75e3434652044b50ffd703fb32ba4568219c56d52e498cd8698
```

Caller, environment, P1-8 bootstrap configuration 또는 raw Markdown가 이 contract payload를 정의하거나 수정할 수 없다. Human-accepted exact payload를 external owner의 private composition이 issue한다. P1-8 Memory policy는 schema/derivation contract를 enroll할 뿐 priority를 만들지 않으며, priority 사용에는 section 4.1의 current eligibility-policy-owned descriptor enrollment가 별도로 필요하다.

### 4.1 exact priority-source enrollment contract

External context는 존재하거나 Memory에 복사되었다는 이유만으로 ranking source가 되지 않는다. Active P1-8 eligibility authority가 issue한 selected `NextActionDescriptor`가 exact source를 enroll해야 한다.

```json
{"action_ref_binding":"DESCRIPTOR_FINGERPRINT_COMMITS_ALL_ENROLLMENT_FIELDS","binding_object":"NEXT_ACTION_DESCRIPTOR","class_to_rank_mapping":{"ACCEPTED_CORE_CRITICAL_PATH":4,"OPERATIONAL_HARDENING":5,"OPTIONAL_OPTIMIZATION":6},"class_to_rank_owner":"P1_8_NEXT_ACTION_SELECTION_POLICY_AUTHORITY_V1","contract_id":"P1_8_NEXT_ACTION_CONTEXT_PRIORITY_SOURCE_ENROLLMENT_V1","contract_version":"v1","descriptor_local_ranking_field":"descriptor_policy_ordinal","enrollment_owner":"P1_8_NEXT_ACTION_ELIGIBILITY_POLICY_AUTHORITY_V1","fixed_source_kind":"NEXT_ACTION_CONTEXT_REF_V1","project_memory_role":"CURRENT_CONTEXTUAL_ELIGIBILITY_INPUT_NOT_PRIORITY_AUTHORITY","ranking_ordinal_name":"enrolled_critical_path_ordinal","required_descriptor_fields":["priority_classification_source_kind","priority_classification_source_ref","priority_classification_source_hash","priority_classification_source_contract_ref","priority_classification_source_contract_fingerprint","critical_path_ordinal","descriptor_policy_ordinal"],"source_contract_binding":"EXACT_CURRENT_REF_AND_FINGERPRINT_REQUIRED","source_resolution":"INDEPENDENT_EXTERNAL_OWNER_READ_PORT"}
```

Canonical SHA-256:

```text
f2b090057ae3f5f00ed4ef878a41664e2322988190969458e6a6544f76932f6b
```

Descriptor fields bind exactly:

```text
priority_classification_source_kind = NEXT_ACTION_CONTEXT_REF_V1
priority_classification_source_ref = exact context_ref
priority_classification_source_hash = exact context fingerprint
priority_classification_source_contract_ref = exact NEXT_ACTION_CONTEXT_SOURCE_CONTRACT_V1 ref
priority_classification_source_contract_fingerprint = 988cdd4c...
critical_path_ordinal = exact owner ordinal copied as enrollment equality value
descriptor_policy_ordinal = existing descriptor-local policy tie-break
```

The descriptor fingerprint, and therefore its `ActionRef`, commits all fields above. Active selection policy independently commits the three class→rank mappings. Missing/stale/mismatched enrollment fails before ranking with `NEXT_ACTION_PRIORITY_SOURCE_NOT_ENROLLED`.

## 5. `NextActionContextRefV1`

### 5.1 exact scope and cardinality

V1은 `TASK_CONTRACT` scope만 지원한다.

```text
project_id                 REQUIRED
scope_kind                 fixed TASK_CONTRACT
task_contract_id           REQUIRED
task_contract_version      REQUIRED
work_run_id                FORBIDDEN
P1-8 Cycle ID              FORBIDDEN
NextActionSelection ID     FORBIDDEN
TaskIssuanceCandidate ID   FORBIDDEN
```

Project-only 및 WorkRun-scoped variant는 V1 `NOT_SUPPORTED`다. 빈 string, null sentinel 또는 조건부 필드로 이를 흉내 내지 않는다.

Stable logical currentness key:

```text
(project_id, task_contract_id, task_contract_version, context_logical_id, context_slot_id)
```

한 key에는 event fold 기준 current context ref가 정확히 `0..1`개다. `context_logical_id`는 successor refs 사이에서 안정적이고 `context_ref_id`는 각 immutable revision마다 새 값이다.

### 5.2 exact immutable fields

`NextActionContextRefV1` payload는 다음 필드 전부를 정확히 포함한다.

```text
context_ref
context_ref_id
context_ref_version = v1
fingerprint_schema = next-action-context-ref-v1

context_owner = EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY
authority_ref = external-command-center-task-authority:next-action-context-source:v1
authority_version = AISCC-EXTERNAL-COMMAND-CENTER-NEXT-ACTION-CONTEXT-AUTHORITY-V1
authority_revision = 1

context_logical_id
project_id
scope_kind = TASK_CONTRACT
task_contract_id
task_contract_version
context_slot_id

priority_class
critical_path_ordinal

context_payload_schema_id = P1_8_NEXT_ACTION_CONTEXT_RESULT_V1
context_payload_schema_version = v1
context_payload_schema_fingerprint = db08fb7cbe1b55b7c686df28ffccbaf8462dd27dea7416e9b4478ae40e6cd67f

privacy_class = PRIVATE_INTERNAL
security_class = INTERNAL_REFERENCE_ONLY

issued_at
issuance_sequence
effective_sequence

fingerprint
```

Derived serialized identifiers:

```text
context_ref = next-action-context:v1:{context_ref_id}
context_logical_id = next-action-context-lineage:v1:{owner-issued stable local ID}
```

`context_ref_id`와 stable local ID는 `CONTEXT_LOCAL_ID_V1`을 만족한다. `project_id`, `task_contract_id`는 `AISCC_ID_V1`; TaskContract version은 `AISCC_VERSION_V1`; slot은 `CONTEXT_SLOT_ID_V1`을 만족한다.

`issuance_sequence`는 owner-global immutable object registration sequence다. `effective_sequence`는 해당 logical currentness key의 event가 이 ref를 최초 도입하는 contiguous position이며, origin은 `1`이다.

### 5.3 exact priority facts

`priority_class` closed enum은 정확히 세 값이다.

```text
ACCEPTED_CORE_CRITICAL_PATH
OPERATIONAL_HARDENING
OPTIONAL_OPTIMIZATION
```

별칭, free text, numeric class, caller priority는 금지한다.

`critical_path_ordinal`은 JSON integer `1..1,000,000`이다. 의미는 다음 하나뿐이다.

```text
same project + same TaskContract version + same priority_class 안에서
external Task authority가 소유한 dependency/critical-path precedence;
smaller integer ranks before larger integer
```

서로 다른 `priority_class` 사이의 순서는 ordinal이 아니라 selection policy의 class rank가 정한다. Equal ordinal은 허용하며 이후 policy/catalog/lexical tie-break로 결정한다. 이 값은 시간, severity, percentage, UI order 또는 global project ordinal이 아니다.

### 5.4 exact fingerprint

Ref schema contract canonical SHA-256:

```text
842ac2619a3069a0b844cbaf89d36ceb252bfe1f1ec149097727f224a6cdc307
```

Hash input canonical payload:

```json
{"canonicalization":"JCS_RFC8785","context_logical_id_grammar":"^next-action-context-lineage:v1:[a-z0-9][a-z0-9._:@-]{0,159}$","context_ref_grammar":"^next-action-context:v1:[a-z0-9][a-z0-9._:@-]{0,159}$","context_slot_id_grammar":"^[a-z0-9][a-z0-9._-]{0,63}$","critical_path_ordinal":{"maximum":1000000,"minimum":1},"fields":["context_ref","context_ref_id","context_ref_version","fingerprint_schema","context_owner","authority_ref","authority_version","authority_revision","context_logical_id","project_id","scope_kind","task_contract_id","task_contract_version","context_slot_id","priority_class","critical_path_ordinal","context_payload_schema_id","context_payload_schema_version","context_payload_schema_fingerprint","privacy_class","security_class","issued_at","issuance_sequence","effective_sequence"],"fingerprint_schema":"next-action-context-ref-v1","fixed_values":{"context_owner":"EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY","context_payload_schema_id":"P1_8_NEXT_ACTION_CONTEXT_RESULT_V1","context_payload_schema_version":"v1","context_ref_version":"v1","privacy_class":"PRIVATE_INTERNAL","scope_kind":"TASK_CONTRACT","security_class":"INTERNAL_REFERENCE_ONLY"},"id_grammar":"^[A-Za-z0-9][A-Za-z0-9._:/@-]{0,159}$","priority_class":["ACCEPTED_CORE_CRITICAL_PATH","OPERATIONAL_HARDENING","OPTIONAL_OPTIMIZATION"],"result_schema_fingerprint":"db08fb7cbe1b55b7c686df28ffccbaf8462dd27dea7416e9b4478ae40e6cd67f","schema_id":"NEXT_ACTION_CONTEXT_REF_SCHEMA_V1"}
```

`fingerprint`를 제외한 section 5.2의 모든 field를 가진 exact object에 대해:

```text
fingerprint = sha256(UTF8(JCS_RFC8785(payload_without_fingerprint)))
```

같은 `context_ref` + 같은 fingerprint는 replay다. 같은 ref + 다른 payload/fingerprint는 `NEXT_ACTION_CONTEXT_IDENTITY_CONFLICT`다. 같은 logical key의 concurrent current refs는 `NEXT_ACTION_CONTEXT_MULTIPLE_CURRENT_CONFLICT`다.

## 6. `NextActionContextAuthorityEventV1`

### 6.1 exact payload

```text
event_ref
event_id
event_version = v1
fingerprint_schema = next-action-context-authority-event-v1
event_kind = ISSUED | SUPERSEDED | REVOKED

context_ref
context_fingerprint
replacement_context_ref
replacement_context_fingerprint

project_id
task_contract_id
task_contract_version
context_logical_id
context_slot_id

authority_ref
authority_version
authority_revision

event_sequence
effective_sequence
effective_at
current_projection_disposition

event_fingerprint
```

```text
event_ref = next-action-context-event:v1:{event_id}
event_id uses CONTEXT_LOCAL_ID_V1
event_fingerprint = sha256(UTF8(JCS_RFC8785(payload_without_event_fingerprint)))
```

Event schema canonical SHA-256:

```text
59e695623329908fdabce214a1d80be4249b4767c86844749de93094aeb7fce4
```

Hash input canonical payload:

```json
{"canonicalization":"JCS_RFC8785","event_kinds":["ISSUED","SUPERSEDED","REVOKED"],"fields":["event_ref","event_id","event_version","fingerprint_schema","event_kind","context_ref","context_fingerprint","replacement_context_ref","replacement_context_fingerprint","project_id","task_contract_id","task_contract_version","context_logical_id","context_slot_id","authority_ref","authority_version","authority_revision","event_sequence","effective_sequence","effective_at","current_projection_disposition"],"fingerprint_schema":"next-action-context-authority-event-v1","schema_id":"NEXT_ACTION_CONTEXT_AUTHORITY_EVENT_SCHEMA_V1","sequence_bounds":{"maximum":9007199254740991,"minimum":1},"variant_rules":{"ISSUED":{"disposition":"RETAIN_CURRENT","replacement":"NULL"},"REVOKED":{"disposition":"WITHDRAW_CURRENT","replacement":"NULL"},"SUPERSEDED":{"disposition":"WITHDRAW_CURRENT","replacement":"REQUIRED"}}}
```

Variant matrix:

| kind | target | replacement fields | disposition on target | resulting current |
|---|---|---|---|---|
| `ISSUED` | first ref of logical key | both exact JSON `null` | `RETAIN_CURRENT` | target ref |
| `SUPERSEDED` | current ref | replacement ref/fingerprint required | `WITHDRAW_CURRENT` | replacement ref |
| `REVOKED` | current ref | both exact JSON `null` | `WITHDRAW_CURRENT` | none |

Pure revoke는 새 `NextActionContextRefV1`을 만들지 않는다. `REVOKED` event 자체가 no-current projection을 나타낸다. V1에서 revoked logical key는 terminal이며 재활성화하지 않는다. 새 planning lineage가 필요하면 새 `context_logical_id`와 owner-issued source를 사용한다.

`SUPERSEDED` replacement는 event commit 전에 immutable store에 존재해야 하고 같은 project/TaskContract/logical ID/slot/schema/privacy/security를 가져야 한다. Replacement의 `effective_sequence`는 event의 `effective_sequence`와 같아야 한다. Semantic class/ordinal은 달라질 수 있으며 새 ref fingerprint에 반영된다. Old withdrawal과 replacement current projection은 한 owner transaction에서 atomic하다.

### 6.2 fold and high-watermark

`event_sequence`는 authority-wide strictly increasing sequence이고 `effective_sequence`는 logical key별로 `1`부터 gap 없이 증가한다. Ordering authority는 sequence이며 timestamp나 file order가 아니다.

Fold input:

```text
logical key
owner_event_high_watermark H
all immutable owner events with event_sequence <= H for that key
all referenced immutable context objects
```

Algorithm:

1. owner signature/capability issuance binding, event/ref fingerprints와 scope equality를 검증한다.
2. `event_sequence`를 strictly ascending sort하고 duplicate sequence/ref를 검사한다.
3. logical key의 first event가 `ISSUED`, `effective_sequence=1`이고 origin이 하나뿐인지 검사한다.
4. subsequent effective sequence가 prior + 1인지 검사한다.
5. `SUPERSEDED`/`REVOKED` target이 fold의 exact current ref인지 검사한다.
6. `SUPERSEDED` replacement object와 fingerprint/schema/scope/effective sequence를 검증하고 current를 replacement로 원자 변경한다.
7. `REVOKED`는 current를 none으로 변경한다.
8. 결과 ref 또는 none, consumed event refs, H를 반환한다.

동일 event ID/ref/sequence + 동일 fingerprint는 replay다. 어느 identity/sequence든 payload가 다르면 `NEXT_ACTION_CONTEXT_AUTHORITY_CONFLICT`다. Unknown kind, missing event, gap, out-of-order effective sequence, unresolved ref 또는 requested H보다 불완전한 owner snapshot은 `NEXT_ACTION_CONTEXT_EVENT_HISTORY_CORRUPT`로 fail closed한다.

New admission/current query는 latest owner-certified high-watermark를 요구한다. Historical replay는 original stored high-watermark와 그때 valid했던 exact event prefix를 요구하며 현재 latest/current를 요구하지 않는다.

## 7. live capability boundary

```text
private Command Center/Task authority composition root
-> creates opaque NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY_V1 issue/supersede/revoke capability
-> binds owner repository/event store once
-> exposes only read/verifier port to P1-8
```

Mandatory:

- P1-8과 P1-6은 issue/supersede/revoke capability를 받지 않는다.
- public/default getter, repository property, serialization/debug hook, environment token 또는 caller-supplied authority instance로 live capability를 노출하지 않는다.
- ordinary caller는 locator/equality claim만 제출할 수 있다.
- copied fields, authority ID string, same class instance 또는 forged event는 recognized authority가 아니다.
- process-local capability는 current authorization일 뿐 historical identity가 아니다. Durable owner object/event bytes, fingerprints, authority version/revision과 issuer binding이 restart/replay authority다.
- test-only capability factory는 production public exports와 production repository에서 격리한다.

## 8. exact P1-6 structured-result carrier

### 8.1 schema identity

```text
schema_id = P1_8_NEXT_ACTION_CONTEXT_RESULT_V1
schema_version = v1
selector = /next_action_context
canonicalization = AISCC_CANONICAL_STRUCTURED_JSON_V1
unknown root keys = DENY
unknown object keys = DENY
diagnostic/free-text fields = NOT_SUPPORTED_V1
```

Exact JSON Schema canonical payload:

```json
{"$id":"P1_8_NEXT_ACTION_CONTEXT_RESULT_V1","$schema":"https://json-schema.org/draft/2020-12/schema","additionalProperties":false,"properties":{"next_action_context":{"additionalProperties":false,"properties":{"context_authority_event_high_watermark":{"maximum":9007199254740991,"minimum":1,"type":"integer"},"context_fingerprint":{"pattern":"^[0-9a-f]{64}$","type":"string"},"context_introduction_event_fingerprint":{"pattern":"^[0-9a-f]{64}$","type":"string"},"context_introduction_event_ref":{"pattern":"^next-action-context-event:v1:[a-z0-9][a-z0-9._:@-]{0,159}$","type":"string"},"context_logical_id":{"pattern":"^next-action-context-lineage:v1:[a-z0-9][a-z0-9._:@-]{0,159}$","type":"string"},"context_ref":{"pattern":"^next-action-context:v1:[a-z0-9][a-z0-9._:@-]{0,159}$","type":"string"},"context_slot_id":{"pattern":"^[a-z0-9][a-z0-9._-]{0,63}$","type":"string"},"critical_path_ordinal":{"maximum":1000000,"minimum":1,"type":"integer"},"priority_class":{"enum":["ACCEPTED_CORE_CRITICAL_PATH","OPERATIONAL_HARDENING","OPTIONAL_OPTIMIZATION"]},"project_id":{"pattern":"^[A-Za-z0-9][A-Za-z0-9._:/@-]{0,159}$","type":"string"},"result_schema_id":{"const":"P1_8_NEXT_ACTION_CONTEXT_RESULT_V1"},"result_schema_version":{"const":"v1"},"task_contract_id":{"pattern":"^[A-Za-z0-9][A-Za-z0-9._:/@-]{0,159}$","type":"string"},"task_contract_version":{"maxLength":64,"minLength":1,"pattern":"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$","type":"string"}},"required":["result_schema_id","result_schema_version","context_ref","context_fingerprint","context_logical_id","context_introduction_event_ref","context_introduction_event_fingerprint","context_authority_event_high_watermark","project_id","task_contract_id","task_contract_version","context_slot_id","priority_class","critical_path_ordinal"],"type":"object"}},"required":["next_action_context"],"type":"object"}
```

Schema canonical SHA-256:

```text
db08fb7cbe1b55b7c686df28ffccbaf8462dd27dea7416e9b4478ae40e6cd67f
```

`context_introduction_event_ref/fingerprint`는 origin `ISSUED` 또는 해당 ref를 도입한 `SUPERSEDED` event를 가리킨다. `context_authority_event_high_watermark`는 producer가 body를 만들 때 external owner에서 resolve한 exact certified H다. 이 세 필드는 authoring snapshot provenance이며 semantic priority를 스스로 만들지 않는다.

Normative ceiling:

```text
body H proves exact owner object/event prefix used when authoring
body H does NOT prove context currentness at later evidence admission
body H does NOT prove context currentness at later terminal transition
cross-domain timestamp comparison is not a substitute
```

## 9. P1-6 prospective enrollment

Existing P1-6 `EvidenceRequirement` V2를 다음 exact 값으로 prospective issue한다.

```text
fingerprint_schema = P1_6_EVIDENCE_REQUIREMENT_FINGERPRINT_V2_DURABLE_CONTENT
evidence_type_id = P1_8_NEXT_ACTION_CONTEXT_RESULT
evidence_type_version = v1
schema_id = P1_8_NEXT_ACTION_CONTEXT_RESULT_V1
schema_version = v1
durable_content_requirement = REQUIRED
allowed_content_kinds = { INLINE_CANONICAL_STRUCTURED_BODY }
maximum_sensitivity = INTERNAL
public_export_allowed = false
durable_content_policy_ref = exact accepted P1-6 V1 durable policy ref
durable_content_policy_fingerprint = exact accepted policy fingerprint
obligation = REQUIRED
```

Content size, retention, access and canonicalization은 accepted P1-6 durable contract를 그대로 따른다: canonical bytes `1..65,536`, `P1_8_HISTORICAL_RECONSTRUCTION_RETAIN_V1`, P1-6-only write, P1-8 owner-issued read grant, no public/raw export.

Requirement의 `applicable_checkpoint_refs`에는 해당 TaskContract가 허용하는 terminal ACCEPTED source별 owner-issued checkpoint를 모두 포함한다.

```text
ADMISSION_PENDING -> ACCEPTED checkpoint
HUMAN_REQUIRED -> ACCEPTED checkpoint
```

실제 WorkRun terminal transition에는 source state와 일치하는 exact checkpoint 하나가 적용되어야 한다. Requirement는 그 checkpoint의 RequirementSet에서 `REQUIRED`이고, its admitted evidence ref는 terminal transition이 소비한 exact `EvidenceSetSatisfactionAttestation`의 ordered refs/root에 포함되어야 한다. Optional evidence, post-terminal admission, unrelated WorkRun/root 또는 later backfill은 source가 아니다.

### 9.1 semantic-contract identity decision

판정은 정확히 `YES`다.

```text
existing P1-6 Requirement schema_id + schema_version
+ existing V2 durable enrollment
+ P1-8 immutable source-policy contract ref/fingerprint
+ external owner object/event equality verification
= sufficient without a new P1-6 Requirement semantic-contract field
```

이유:

1. P1-6은 schema ID/version, canonical bytes와 provenance를 certify하며 priority semantics를 certify하지 않는다.
2. External owner의 `NextActionContextRefV1`과 event graph가 semantics를 소유한다.
3. P1-8 Memory policy fingerprint는 section 4 source contract ref/fingerprint, section 8 schema fingerprint, selector와 equality fields를 고정한다.
4. P1-8은 body의 모든 semantic field를 resolved owner object와 exact 비교한다. P1-6 body/caller value 자체는 authority가 아니다.
5. Schema semantics가 바뀌면 in-place mutation하지 않고 새 result schema ID/version, 새 P1-8 policy revision, 새 prospective P1-6 Requirement ref/fingerprint를 발행한다.

따라서 `P1_6_REQUIREMENT_SEMANTIC_CONTRACT_EXTENSION_REQUIRED` STOP은 이 V1 모델에서 발생하지 않는다. P1-6 Requirement identity나 accepted fingerprint schema를 변경하지 않는다.

## 10. exact P1-8 cross-owner verification

P1-8 policy-owned derivation contract canonical SHA-256:

```text
6de3e66a0d16a1dc0038838eb58b9ca0ca6c2d790ab3a5cdcab3802b5093b508
```

Hash input canonical payload:

```json
{"contract_id":"P1_8_NEXT_ACTION_CONTEXT_MEMORY_DERIVATION_V1","contract_version":"v1","equality_fields":["context_ref","context_fingerprint","context_logical_id","project_id","task_contract_id","task_contract_version","context_slot_id","priority_class","critical_path_ordinal"],"event_provenance_fields":["context_introduction_event_ref","context_introduction_event_fingerprint","context_authority_event_high_watermark"],"memory_content_fingerprint_schema":"p1-8-memory-content-v1","normalized_fields":["context_ref","context_fingerprint","context_logical_id","project_id","task_contract_id","task_contract_version","context_slot_id","priority_class","critical_path_ordinal"],"p1_6_result_schema_fingerprint":"db08fb7cbe1b55b7c686df28ffccbaf8462dd27dea7416e9b4478ae40e6cd67f","p1_6_result_schema_id":"P1_8_NEXT_ACTION_CONTEXT_RESULT_V1","p1_6_result_schema_version":"v1","priority_source_enrollment_contract_fingerprint":"f2b090057ae3f5f00ed4ef878a41664e2322988190969458e6a6544f76932f6b","privacy_ceiling":"PRIVATE_INTERNAL","producer_high_watermark_role":"AUTHORING_SNAPSHOT_PROVENANCE_ONLY","project_memory_role":"CURRENT_CONTEXTUAL_ELIGIBILITY_INPUT_NOT_PRIORITY_AUTHORITY","selector":"/next_action_context","source_contract_fingerprint":"988cdd4c71aca75e3434652044b50ffd703fb32ba4568219c56d52e498cd8698","source_owner":"EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY/NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY_V1","terminal_context_currentness":"NOT_REQUIRED_V1"}
```

Exact pipeline:

1. accepted `HistoricalStructuredResultAuthorityV1`로 P1-6 Requirement/checkpoint/admission/durable bytes/terminal-consumed attestation/root 전체를 검증한다.
2. content metadata의 schema ID/version이 section 8과 일치하고 exact canonical body에서 `/next_action_context`를 선택한다.
3. body의 context ref/fingerprint로 immutable `NextActionContextRefV1`을 external read port에서 resolve한다.
4. ref schema/source contract/fingerprint/owner identity/scope를 검증한다.
5. introduction event와 body H를 검증하고 fold하여 context가 **body authoring snapshot H에서** valid했는지만 확인한다. Body H는 later P1-6 evidence admission 또는 terminal currentness proof가 아니다.
6. body와 owner object의 다음 fields를 exact 비교한다.

```text
context_ref
context_fingerprint
context_logical_id
project_id
task_contract_id
task_contract_version
context_slot_id
priority_class
critical_path_ordinal
```

7. body TaskContract와 P1-6 Requirement/admitted evidence/WorkRun/terminal transition/AdmittedCycle의 project/TaskContract가 동일한지 검증한다. P1-6 historical graph는 exact immutable body가 admitted되고 terminal-consumed되었음을 증명하지만 external context가 terminal까지 current였음을 증명하지 않는다. WorkRun/Cycle IDs는 provenance layer에서 결합하며 owner object에 넣지 않는다.
8. 아래 normalized object를 derive하고 accepted `MCF_V1`을 계산한다.

```json
{"context_ref":"<exact ref>","context_fingerprint":"<exact fingerprint>","context_logical_id":"<stable owner lineage>","project_id":"<exact project>","task_contract_id":"<exact TaskContract>","task_contract_version":"<exact version>","context_slot_id":"<exact slot>","priority_class":"<exact closed enum>","critical_path_ordinal":1}
```

Introduction event refs/body H와 P1-6 graph는 immutable source provenance에 저장하지만 semantic MCF object에는 넣지 않는다. 동일 owner context의 semantic identity가 later owner event 때문에 바뀌지 않게 하기 위함이다.

Caller `MemoryDeclaration`의 ref, selector, class, ordinal, lineage와 claimed fingerprint는 equality claims일 뿐이다. Missing owner object/event, unknown schema, mismatch 또는 forged H는 admission deny이며 memory가 생성되지 않는다.

## 11. owner-derived lineage

```text
subject_key
= context_logical_id

applicability_key
= task-contract/{project_id}/{task_contract_id}@{task_contract_version}

semantic_slot
= next-action-context/P1_8_NEXT_ACTION_CONTEXT_RESULT_V1/{context_slot_id}
```

각 atom은 exact owner payload에서 derive한다. Caller free text, display label, Cycle ID 또는 WorkRun ID를 lineage key에 넣지 않는다. `MemoryLineageKey`는 accepted P1-8 formula로 category + subject + applicability + semantic slot을 commit한다.

Current applicability는 다음 conjunction이다.

```text
P1-6 source is currently applicable under accepted source-currentness rules
AND context owner fold at latest certified H returns exact context_ref current
AND P1-8 Memory policy/source enrollment is current
AND ProjectMemory applicability event fold returns CURRENT
```

Body H에서 valid했고 exact body가 P1-6에 admitted/terminal-consumed되었지만 external context 또는 P1-6 source가 Cycle admission 전에 non-current가 된 경우, immutable historical Cycle/Memory identity는 유지하되 처음부터 non-`CURRENT`로 publish한다. 어느 순간에도 temporary CURRENT 노출을 허용하지 않는다.

## 12. selection-time priority and ordinal separation

`CURRENT ProjectMemoryEntry`는 source relation이 admitted/current context에 사용 가능한지 증명하는 `CYCLE_DERIVED` eligibility/context input이다. Memory content가 class/ordinal copy를 포함해도 그것 자체는 priority authority가 아니다.

New selection requires both:

```text
A. exact NEXT_ACTION_CONTEXT ProjectMemoryEntry is CURRENT
   at selection memory-applicability high-watermark

B. selected current NextActionDescriptor explicitly enrolls
   exact current NextActionContextRefV1 ref/fingerprint
   and exact source-contract ref/fingerprint
```

Exact evaluation order:

1. active eligibility policy, selection policy and selected descriptor/`ActionRef` currentness를 검증한다.
2. Memory entry가 selection H에서 `CURRENT`, `NEXT_ACTION_CONTEXT`, same project/TaskContract scope인지 검증한다.
3. Memory에서 external context ref/fingerprint를 contextual locator로 읽는다.
4. Selected descriptor fingerprint가 section 4.1 exact source ref/hash/contract enrollment를 commit하는지 검증한다.
5. Descriptor-enrolled ref와 Memory locator가 exact 동일한지 검증한다.
6. External owner read port로 enrolled `NextActionContextRefV1`을 Memory와 독립적으로 resolve하고 latest selection-time owner H에서 current인지 검증한다.
7. Resolved owner payload의 class/ordinal을 Memory contextual copy와 equality-check한다.
8. External source의 `priority_class`와 `critical_path_ordinal`을 authoritative facts로 rederive한다.
9. Current selection policy authority가 class를 rank로 mapping한다.
10. Accepted ranking tuple을 적용한다.

Class→rank mapping owner는 `P1_8_NEXT_ACTION_SELECTION_POLICY_AUTHORITY_V1`이다.

| external owner class fact | selection-policy rank |
|---|---:|
| `ACCEPTED_CORE_CRITICAL_PATH` | 4 |
| `OPERATIONAL_HARDENING` | 5 |
| `OPTIONAL_OPTIMIZATION` | 6 |

`enrolled_critical_path_ordinal`은 independently resolved external context object의 `critical_path_ordinal`이며 selected descriptor의 enrolled equality copy와 exact 일치해야 한다. Memory copy는 추가 equality check일 뿐 authority path가 아니다.

Accepted tuple은 변경하지 않는다.

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

Descriptor-local ordinal을 새 ranking dimension으로 추가하지 않는다. 기존 `descriptor_policy_ordinal`만 accepted descriptor-local tie-break다. Predecessor가 제안한 `source_memory_critical_path_ordinal`, `descriptor_catalog_ordinal`과 descriptor field rename은 폐기한다. Descriptor의 existing `critical_path_ordinal` field는 external source ordinal의 enrolled equality copy이며 tuple에서는 `enrolled_critical_path_ordinal`로 읽는다.

Selection payload/evaluation은 exact Memory ref/fingerprint, Memory applicability H, descriptor/ActionRef, enrolled source ref/fingerprint/contract fingerprint, selection-time external owner H, external class/ordinal, selection policy mapping ref/fingerprint과 ranking trace를 저장한다. Proposal priority/security claims는 audit-only다.

## 13. historical replay and current invalidation

Historical Cycle/Memory replay verifies:

```text
original P1-8 Memory policy payload and as-of validity
original P1-6 immutable structured-result graph and terminal-consumed root
original NextActionContextRefV1 payload/fingerprint
original introduction event and producer body-H owner event prefix
exact result/owner equality
normalized object, MCF_V1 and MemoryLineageKey
```

Body H는 authoring snapshot provenance만 증명한다. V1은 external context currentness at terminal을 historical semantic validity 조건으로 요구하지 않는다. P1-6 historical graph가 exact body의 admission/terminal consumption을 증명한다. Body H 이후 revoke/supersede는 historical corruption이 아니라 current applicability 변화다.

Terminal-bound external context currentness가 미래에 필요해지면 별도의 immutable terminal observation authority가 exact terminal WorkRun/transition과 external owner H를 함께 bind해야 한다. V1은 body H 또는 cross-domain timestamp로 이를 추론하지 않는다.

Historical NextActionSelection replay는 다음 graph를 정확히 검증한다.

```text
original Memory entry/ref/MCF
+ Memory was CURRENT at original selection H
+ original selected ActionRef/descriptor fingerprint
+ original descriptor enrollment of exact context ref/hash/source contract
+ original external context payload/fingerprint
+ context was current at stored selection-time external owner H
+ original external class/ordinal
+ original selection policy class->rank mapping
+ accepted original ranking tuple
```

Later Memory, external source, descriptor 또는 policy staleness는 historical corruption이 아니다. Missing/tampered original payload/event/enrollment/mapping 또는 invalid-at-original-selection source는 historical corruption이다.

Current reaction:

```text
context REVOKED
or old context SUPERSEDED under WITHDRAW_CURRENT
-> append ProjectMemoryAuthorityEvent
-> withdraw dependent current NEXT_ACTION_CONTEXT memory
-> append/derive NextAction current-withdrawal event when current selection depended on it
```

Projection update is append-only and idempotent by owner event ref/fingerprint + expected current revision. Old immutable objects remain.

## 14. persistence and no-backfill cut-line

No runtime or migration is implemented here. Later owner-domain persistence needs exact equivalents of:

```text
next_action_context_refs
next_action_context_authority_events
unique context_ref/fingerprint
unique authority event_sequence
unique (logical key, effective_sequence)
one folded current ref per logical key
append-only/owner-only mutation guards
```

P1-8 stores only refs/fingerprints/high-watermarks and its own projections unless the external owner read port shares durable storage. P1-8 foreign keys point outward; external owner never depends on a P1-8 Cycle.

Prospective only:

- legacy metadata-only P1-6 evidence is ineligible;
- legacy durable body with another schema ID/version is ineligible;
- legacy accepted Cycle without exact context owner provenance remains historical but gains no `NEXT_ACTION_CONTEXT`;
- producer JSON without matching owner ref/event is denied;
- correct ref with different class/ordinal/scope is denied;
- caller-created or P1-8-created context object/event is denied;
- P1-6 durable body alone is insufficient;
- Markdown `NEXT_ACTIONS` text alone is insufficient;
- no caller backfill, migration synthesis or hash-only grandfathering is permitted.

## 15. exact question answers

| # | Answer |
|---:|---|
| 1 | No. `CURRENT ProjectMemoryEntry` is required CYCLE_DERIVED contextual/eligibility input, not priority authority. |
| 2 | Exact external `NextActionContextRefV1` plus its verified owner event graph is the classification/ordinal source. |
| 3 | `P1_8_NEXT_ACTION_ELIGIBILITY_POLICY_AUTHORITY_V1` enrolls it through the exact current selected `NextActionDescriptor`; the selection policy separately owns class→rank mapping. |
| 4 | Descriptor priority-source ref/hash/contract fields and ordinal equality copy are committed by descriptor fingerprint and therefore selected `ActionRef`. |
| 5 | `P1_8_NEXT_ACTION_SELECTION_POLICY_AUTHORITY_V1` owns `ACCEPTED_CORE_CRITICAL_PATH→4`, `OPERATIONAL_HARDENING→5`, `OPTIONAL_OPTIMIZATION→6`. |
| 6 | `enrolled_critical_path_ordinal` is the external context object's independently resolved `critical_path_ordinal`, equal to descriptor enrollment copy; Memory copy is equality-only. |
| 7 | No. `descriptor_policy_ordinal` is the only accepted descriptor-local tie-break. No `descriptor_catalog_ordinal` or extra ranking dimension is added. |
| 8 | CURRENT Memory proves admitted/current contextual relation and scope. External descriptor enrollment independently proves the source is eligible as priority authority. Both are required. |
| 9 | Section 13 graph proves original CURRENT Memory, ActionRef/descriptor enrollment, external payload/currentness at selection H, class/ordinal, policy mapping and accepted tuple. |
| 10 | Carrier H proves only the exact external owner prefix observed at body authoring. It proves neither later P1-6 admission nor terminal currentness. |
| 11 | External context currentness at terminal is `NOT_REQUIRED_V1`. Later events affect current applicability; future terminal binding would require a separate terminal observation authority. |
| 12 | The historical accepted predecessor used source contract `c43c8560...` and Memory derivation `82cdb2a5...`. This JCS-safe candidate uses `988cdd4c...` and `6de3e66a...`; enrollment remains `f2b09005...`, while ref/event/result schema hashes are reconciled transitively. |
| 13 | Yes. Existing P1-6 Requirement identity and the section 9 sufficiency decision remain unchanged. |
| 14 | Human must accept/rework/reject this candidate. External owner runtime and later prerequisite descriptor/policy/catalog incorporation remain open; no compatibility semantic choice is intentionally unresolved. |

## 16. JCS correction lineage, acceptance and runtime gate

The historical Human acceptance remains bound to predecessor SHA-256
`19b1d29a8f77ca5cc480a14bc9d1bdd53206951ccf8b34802316f1280dc61cb1`. The current edited bytes are a
prospective narrow JCS safe-integer and dependent-fingerprint correction; they are not covered by that historical
acceptance and require a new Human review. All normative sequence/high-watermark JSON integers in this candidate
are bounded by `9007199254740991`; arbitrary-precision lexical hashing and a custom JCS dialect remain forbidden.

```text
NEXT_ACTION_CONTEXT source authority design:
REWORK_CANDIDATE / HUMAN_REVIEW_REQUIRED

P1-8 prerequisite owner-authority design:
BLOCKED_REQUIRED_EVIDENCE

P1-8 Runtime:
BLOCKED_REQUIRED_EVIDENCE

P2:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

Resume prerequisites:

1. Human accepts this exact candidate and SHA.
2. External Command Center/Task authority runtime implements and verifies the exact source owner, object/event store and private capability boundary in a separately authorized Task.
3. A later prerequisite rework incorporates this contract, finishes TaskConstraint/blocker findings and recomputes all affected priority/catalog/descriptor hashes.
4. Only after those owner runtimes are accepted may a new P1-8 runtime Task resume.

Executor evidence or this document alone cannot satisfy Human acceptance.

## Accepted 2010: one-time self-dogfood Genesis authority

Normative design: `AISCC-P1-8-SELF-DOGFOOD-GENESIS-BOOTSTRAP-V1`.
Human-provided design acceptance is recorded in the byte-exact 1916 Human review
(SHA-256 `09c93a9a67ca064bd269240787b8fdd5380f05693f4394dc74bba778c9f0da8a`).
This amendment extends the earlier source capability statements only as stated below;
all historical catalog JSON, fingerprints, Cycle provenance and other owner boundaries remain unchanged.

`SELF_DOGFOOD_GENESIS` is an explicit source mode with action
`open-self-dogfood-genesis-task-issuance`. It is never a fallback, recovery translation,
Cycle-derived alias, Replay import, Markdown import, or LLM action selection.
The separate Genesis catalog requires exactly one externally owner-issued authority
and one proposal. It fabricates no predecessor WorkRun, source Cycle, memory entry,
CycleMemoryReference, Human result, Evidence or Judgment.

The immutable canonical authority binds project, authority ID, source mode, action,
repository ID, absolute root, exact base commit, phase, OWNER_SELF_DOGFOOD runtime,
AISCC_SELF_DOGFOOD execution mode, external Command Center issuer identity/version,
and UTC issuance time. Its fingerprint authenticates the complete canonical body.
Only a bootstrap-bound external writer can persist it; constructing or parsing bytes
is not owner issuance. Selection and Task issuance verify the persisted authority,
exact enrolled context and currentness in the caller's database transaction.

Initial enrollment requires no operational WorkRun, no admitted operational Cycle,
no CURRENT NEXT_ACTION_CONTEXT lineage, and no conflicting current selection.
After Task binding, only that exact family's own WorkRun lineage may coexist until
its first owner-admitted Cycle. Any admitted Cycle permanently makes Genesis
non-current, even after restart, historical replay, projection rebuild or later
context withdrawal. Any CURRENT cycle-derived context also denies Genesis.
Historical reads remain possible and never confer currentness.

One operational project has at most one Genesis authority and one exact TaskContract
family/body (version 1). Exact retries return the durable result; changed body,
different family or a second distinct authority is denied. Revocation cannot free
this one-time binding. New issuance and currentness after the first Cycle fail with
GENESIS_NOT_ELIGIBLE; corrupt or partial reciprocal authority/body records fail closed.

TaskContract V1 supports exactly SELF_DOGFOOD_GENESIS and CYCLE_DERIVED.
OPERATIONAL_RECOVERY remains a valid P1-8 source but is rejected by this issuer before
any source WorkRun lock or body mutation. No general planner is introduced.

Genesis descriptors use a separate `p1-8-genesis-catalog:v1` authority and exact
`genesis_authority_ref` / `genesis_authority_fingerprint` parameters. The action
fingerprint includes the full immutable context. Project and phase are fixed.
No Cycle/context fields are overloaded or populated. Existing context-bound
CYCLE_DERIVED descriptors, priority mappings and source checks are unchanged.
The first post-Cycle selection continues through owner-admitted structured context,
Cycle/memory provenance, external context authority and existing selection policy.
