# AISCC P1-8 Prerequisite Owner Authority Exact Contract

## 1. Document status

| field | value |
|---|---|
| document_id | `AISCC-P1-8-PREREQUISITE-OWNER-AUTHORITY-DESIGN-3` |
| task_id | `20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-design-rework-1` |
| work_type | `DESIGN_REWORK` |
| design_status | `JOINT_REWORK_CANDIDATE / HUMAN_REVIEW_REQUIRED` |
| acceptance_owner | `Human` |
| implementation_status | `DESIGN_ONLY / RUNTIME_NOT_IMPLEMENTED` |
| accepted P1-8 design SHA-256 | `100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a` |
| historical accepted NEXT_ACTION_CONTEXT predecessor SHA-256 | `19b1d29a8f77ca5cc480a14bc9d1bdd53206951ccf8b34802316f1280dc61cb1` |
| predecessor candidate SHA-256 | `189156a190a13c92830d5b4c7ae28cd41f52f6c438dacda9e145bc82dd2d36d7` |
| blocked P1-8 runtime | `19 paths / 84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42` |
| P1-8 runtime status | `BLOCKED_REQUIRED_EVIDENCE` |

This is a candidate. It changes no accepted canonical rule and authorizes no runtime, migration, Task issuance,
deployment, or Human acceptance.

## 2. Exact scope and non-substitution

This revision closes only TaskConstraint owner event/currentness, P1-4 blocker taxonomy and durable
`G_BLOCKER_RESOLVED` binding, and incorporation of the accepted `NextActionContextRefV1` source contract into
P1-8 catalog/descriptor/eligibility/selection authority.

```text
TaskConstraintRefV1 != MemoryDeclaration
P1_4BlockerProvenanceV1 != ProjectMemoryEntry
P1_4BlockerResolvedAttestationV1 != TransitionDecision
CommandCenterCycleRecord != AdmittedCycle
ProjectMemoryEntryId != MemoryLineageKey
CURRENT ProjectMemory != priority authority
NextActionProposal != NextActionDescriptor
NextActionSelection != TransitionDecision
TaskIssuanceCandidate != TaskContract
```

## 3. Verified owner inventory

| owner/symbol | classification | exact result |
|---|---|---|
| external Command Center Task authority | `EXISTING_BUT_INSUFFICIENT` | Governance issues Tasks, but no accepted runtime-verifiable TaskConstraint ref/event/snapshot owner exists. This candidate defines a prospective external-owner extension only. |
| P1-4 WorkRun/TransitionRequest/Evaluation/Decision | `EXISTING_EXACT_OWNER` | P1-4 owns state/version, evaluation, decision, and atomic mutation. |
| P1-4 `G_BLOCKER`/`G_BLOCKER_RESOLVED` | `EXISTING_BUT_INSUFFICIENT` | Exact guard IDs and owner slots exist, but current `required_bound_refs` is empty for both and there is no typed durable blocker/resolution object. |
| P1-6 TaskContractEvidenceAuthority/durable content | `EXISTING_EXACT_OWNER` | P1-6 owns Requirement/checkpoint/content/admission/terminal-consumed provenance only. |
| P1-7 Human/Judgment authority | `EXISTING_EXACT_OWNER` | P1-7 owns eight Human and three Judgment guards only, not `G_BLOCKER*`. |
| accepted NEXT_ACTION_CONTEXT external source owner | `EXISTING_EXACT_OWNER` at design authority | Exact accepted source/object/event/carrier/Memory/enrollment contracts exist at SHA `19b1d29a...`; runtime is not implemented. |
| P1-8 eligibility/selection owners | `EXISTING_BUT_INSUFFICIENT` | Owner slots and ranking semantics exist, but predecessor catalog/selection payload did not commit accepted external context enrollment. |
| canonical Markdown rule/roadmap | `EXISTING_BUT_INSUFFICIENT` | Path/hash/heading or roadmap presence is not TaskConstraint or descriptor authority. |

Every new contract below is `DESIGN_ONLY / RUNTIME_NOT_IMPLEMENTED`.

## 4. Contract A — TaskConstraint owner object

### 4.1 Exact owner and private boundary

```text
owner = EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY / TASK_CONSTRAINT_AUTHORITY_V1
P1-8 = read/verifier port only
CANONICAL_RULE_CONSTRAINT_SOURCE = NOT_SUPPORTED_V1
```

Only the external Task authority private composition root holds an opaque issue/supersede/revoke capability. It
binds repository and verifier once and exposes only immutable resolution to P1-8. No public/default getter,
repository property, callback, debug hook, serialized/environment token, caller authority instance, copied object,
or matching authority ID can obtain or emulate it. The live process capability permits writes but is not
historical identity; durable payloads, fingerprints, events, snapshot certificates, and issuer binding are.

### 4.2 Exact scope variants

`TaskConstraintRefV1.scope` is a closed discriminated JSON object. Unknown fields, empty strings, sentinels, and
JSON null inside `scope` are forbidden. Non-applicable fields are omitted.

| scope kind | `project_id` | `task_contract_id` | `task_contract_version` | `work_run_id` | `scope_id` |
|---|---|---|---|---|---|
| `PROJECT` | required | forbidden | forbidden | forbidden | absent; display-only derivation `project:{project_id}` |
| `TASK_CONTRACT` | required | required | required | forbidden | absent; display-only derivation `task-contract:{project_id}/{task_contract_id}@{task_contract_version}` |
| `WORK_RUN` | required | required | required | required | absent; display-only derivation `work-run:{project_id}/{task_contract_id}@{task_contract_version}/{work_run_id}` |

The display derivation is never hashed, persisted as another identity, or accepted from a caller.

### 4.3 `TaskConstraintRefV1`

Exact immutable fields are:

```text
constraint_ref / constraint_ref_id / constraint_ref_version = v1
fingerprint_schema = task-constraint-ref-v1
constraint_owner = EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY
authority_ref / authority_version / authority_revision
logical_constraint_id / scope
constraint_schema_id / constraint_schema_version
constraint_payload_ref / constraint_payload_fingerprint
issued_at / issuance_sequence / constraint_fingerprint
```

Supersedes/revokes/effective/current fields are forbidden here and belong only to owner events.
`constraint_fingerprint = sha256(UTF8(JCS_RFC8785(payload_without_constraint_fingerprint)))`.

```json
{"canonicalization":"JCS_RFC8785","fields":["constraint_ref","constraint_ref_id","constraint_ref_version","fingerprint_schema","constraint_owner","authority_ref","authority_version","authority_revision","logical_constraint_id","scope","constraint_schema_id","constraint_schema_version","constraint_payload_ref","constraint_payload_fingerprint","issued_at","issuance_sequence"],"fingerprint_schema":"task-constraint-ref-v1","fixed_values":{"constraint_owner":"EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY","constraint_ref_version":"v1"},"forbidden_fields":["scope_id","supersedes_constraint_ref","revokes_constraint_ref","effective_sequence","current_projection_disposition"],"schema_id":"TASK_CONSTRAINT_REF_SCHEMA_V1","scope_variants":{"PROJECT":{"forbidden":["task_contract_id","task_contract_version","work_run_id"],"required":["scope_kind","project_id"]},"TASK_CONTRACT":{"forbidden":["work_run_id"],"required":["scope_kind","project_id","task_contract_id","task_contract_version"]},"WORK_RUN":{"forbidden":[],"required":["scope_kind","project_id","task_contract_id","task_contract_version","work_run_id"]}},"unknown_fields":"DENY"}
```

Canonical SHA-256: `c3bba5050a43a37c2563518d862a4b7fc1c3ee344cd763ab66da19d15a7126cc`.

### 4.4 `TaskConstraintAuthorityEventV1`

Exact immutable fields:

```text
event_ref / event_id / event_version = v1
fingerprint_schema = task-constraint-authority-event-v1
event_kind = ISSUED | SUPERSEDED | REVOKED
constraint_ref/fingerprint
replacement_constraint_ref/fingerprint
logical_constraint_id / scope
authority_ref/version/revision
event_sequence / effective_sequence / effective_at
current_projection_disposition / event_fingerprint
```

| event | target | replacement | disposition | resulting current |
|---|---|---|---|---|
| `ISSUED` | first object of logical key | exact JSON `null`/`null` | `RETAIN_CURRENT` | target |
| `SUPERSEDED` | exact folded current | required exact ref/fingerprint | `WITHDRAW_CURRENT` | replacement |
| `REVOKED` | exact folded current | exact JSON `null`/`null` | `WITHDRAW_CURRENT` | none |

Pure revoke is only a `REVOKED` event; it creates no constraint object. A revoked logical key is terminal in V1.
Reactivation requires a new logical ID and new `ISSUED` origin.

```json
{"canonicalization":"JCS_RFC8785","event_kinds":["ISSUED","SUPERSEDED","REVOKED"],"fields":["event_ref","event_id","event_version","fingerprint_schema","event_kind","constraint_ref","constraint_fingerprint","replacement_constraint_ref","replacement_constraint_fingerprint","logical_constraint_id","scope","authority_ref","authority_version","authority_revision","event_sequence","effective_sequence","effective_at","current_projection_disposition"],"fingerprint_schema":"task-constraint-authority-event-v1","schema_id":"TASK_CONSTRAINT_AUTHORITY_EVENT_SCHEMA_V1","sequence_bounds":{"maximum":9007199254740991,"minimum":1},"variant_rules":{"ISSUED":{"disposition":"RETAIN_CURRENT","replacement":"NULL"},"REVOKED":{"disposition":"WITHDRAW_CURRENT","replacement":"NULL"},"SUPERSEDED":{"disposition":"WITHDRAW_CURRENT","replacement":"REQUIRED"}}}
```

Canonical SHA-256: `2b4bd41b7dbf7f002f2b48aabcf816ac386d860c12c20e947843bee5390c9b00`.

### 4.5 Certified high-watermark and fold

`TaskConstraintOwnerSnapshotV1` certifies a complete owner prefix. It binds snapshot ref/version/fingerprint,
authority ref/version/revision, H, ordered event-prefix root, issued-at, and issuer authenticity. The root input is
the exact JCS array `[[event_ref,event_fingerprint], ...]` for every authority-global event sequence `1..H` in
ascending sequence order; its value is `sha256(UTF8(JCS_RFC8785(array)))`. Missing any global sequence prevents a
snapshot from verifying.

```json
{"canonicalization":"JCS_RFC8785","fields":["snapshot_ref","snapshot_version","fingerprint_schema","authority_ref","authority_version","authority_revision","owner_event_high_watermark","ordered_event_prefix_root","issued_at"],"fingerprint_schema":"task-constraint-owner-snapshot-v1","high_watermark_bounds":{"maximum":9007199254740991,"minimum":0},"prefix_root_algorithm":"SHA256_JCS_ORDERED_EVENT_REF_FINGERPRINT_PAIRS_GLOBAL_SEQUENCE_1_THROUGH_H","schema_id":"TASK_CONSTRAINT_OWNER_SNAPSHOT_SCHEMA_V1"}
```

Canonical SHA-256: `41330e2502ae9c337a3a1e8dfc693b2fb9307bec9eb5b5138e33ad7cdd35c1aa`.

Fold input is one logical key, one certified snapshot, all key events with global `event_sequence <= H`, and every
referenced immutable object. Verify snapshot issuer/fingerprint/H/root/completeness; verify every object/event
fingerprint/owner/key/scope; sort by global sequence; treat same ID/sequence/fingerprint as replay and any conflict
as `TASK_CONSTRAINT_AUTHORITY_CONFLICT`; require exactly one first `ISSUED` at per-key effective sequence 1;
require each later effective sequence to be prior + 1; require supersede/revoke to target exact current; require a
superseding replacement to pre-exist and match key/scope/schema; apply section 4.4. Unknown kind, missing prefix,
gap, out-of-order target, unresolved ref, incomplete snapshot, event after revoke, or multiple origin fails closed.
Return current ref or none plus consumed events, snapshot ref/fingerprint, and H.

Historical replay stores original ref and original snapshot ref/fingerprint/H and rederives original validity from
that prefix. New admission uses the latest certified H and only its current ref. Later events change current
applicability without rewriting historical Cycle/Memory identity.

## 5. Contract B — P1-4 blocker taxonomy and resolution binding

### 5.1 Ownership and cardinality

```text
blocker/resolution owner = P1_4_SYSTEM_TRANSITION_AUTHORITY
extension = P1_4_BLOCKER_PROVENANCE_AUTHORITY_V1
P1-8 = verify/read plus its own Cycle relation only
```

At most one ACTIVE blocker exists per `(work_run_id, blocked_epoch)`, where `blocked_epoch` is the admitted
transition's resulting BLOCKED state version. Sequential BLOCKED epochs have distinct immutable blockers. Same ID
and fingerprint replays; another ID/fingerprint in the same epoch conflicts. Lists, quorum, and partial resolution
are `NOT_SUPPORTED_V1`.

### 5.2 Closed taxonomy and resumability

| `BlockerKindV1` | `BlockerReasonCodeV1` | resumability | allowed path | positive `G_BLOCKER_RESOLVED` |
|---|---|---|---|---|
| `SECURITY` | `SECURITY_BOUNDARY` | `NON_RESUMABLE` | `BLOCKED -> FAILED` via `G_FAILURE_TERMINAL` only | forbidden |
| `POLICY` | `POLICY_CONFLICT` | `RESUMABLE` | `BLOCKED -> READY | HUMAN_REQUIRED | REWORK_REQUIRED` | allowed |
| `ARTIFACT` | `MISSING_REQUIRED_ARTIFACT` | `RESUMABLE` | same three targets | allowed |
| `BASELINE` | `BASELINE_GAP` | `RESUMABLE` | same three targets | allowed |
| `AUTHORITY` | `AUTHORITY_CONFLICT` | `RESUMABLE` | same three targets | allowed |
| `EXTERNAL_DEPENDENCY` | `EXTERNAL_DEPENDENCY` | `RESUMABLE` | same three targets | allowed |
| `EXECUTION` | `EXECUTION_BLOCKER` | `RESUMABLE` | same three targets | allowed |

No other pair is valid. NON_RESUMABLE never emits positive `G_BLOCKER_RESOLVED`; a later Task/WorkRun may address
the cause but cannot resolve the old blocker.

```json
{"kinds":["SECURITY","POLICY","ARTIFACT","BASELINE","AUTHORITY","EXTERNAL_DEPENDENCY","EXECUTION"],"matrix":[{"kind":"SECURITY","positive_g_blocker_resolved":false,"reason_code":"SECURITY_BOUNDARY","resumability":"NON_RESUMABLE"},{"kind":"POLICY","positive_g_blocker_resolved":true,"reason_code":"POLICY_CONFLICT","resumability":"RESUMABLE"},{"kind":"ARTIFACT","positive_g_blocker_resolved":true,"reason_code":"MISSING_REQUIRED_ARTIFACT","resumability":"RESUMABLE"},{"kind":"BASELINE","positive_g_blocker_resolved":true,"reason_code":"BASELINE_GAP","resumability":"RESUMABLE"},{"kind":"AUTHORITY","positive_g_blocker_resolved":true,"reason_code":"AUTHORITY_CONFLICT","resumability":"RESUMABLE"},{"kind":"EXTERNAL_DEPENDENCY","positive_g_blocker_resolved":true,"reason_code":"EXTERNAL_DEPENDENCY","resumability":"RESUMABLE"},{"kind":"EXECUTION","positive_g_blocker_resolved":true,"reason_code":"EXECUTION_BLOCKER","resumability":"RESUMABLE"}],"reason_codes":["SECURITY_BOUNDARY","POLICY_CONFLICT","MISSING_REQUIRED_ARTIFACT","BASELINE_GAP","AUTHORITY_CONFLICT","EXTERNAL_DEPENDENCY","EXECUTION_BLOCKER"],"schema_id":"P1_4_BLOCKER_TAXONOMY_V1"}
```

Canonical SHA-256: `ec170cd257b04e77410951abe8c7f196a88bf8f35d9e6deaec8d8889bb0e9d0c`.

### 5.3 `P1_4BlockerProvenanceV1`

Exact fields bind blocker ID/ref/version/fingerprint, P1-4 owner authority, kind/reason/resumability,
project/TaskContract/version/WorkRun/BLOCKED epoch, source and resulting state/version, the blocking
Request/Evaluation/Decision refs/fingerprints, an exact resolution-source contract ref/fingerprint, ordered source
authority refs/fingerprints, issuance sequence, and issued-at. It is appended atomically with admission into
BLOCKED. Narrative is private non-authoritative data.

```json
{"canonicalization":"JCS_RFC8785","fields":["blocker_id","blocker_ref","blocker_version","fingerprint_schema","blocker_owner","authority_ref","authority_version","authority_revision","blocker_kind","reason_code","resumability","project_id","task_contract_id","task_contract_version","work_run_id","blocked_epoch","created_source_state","created_source_state_version","blocking_transition_request_ref","blocking_transition_request_fingerprint","blocking_transition_evaluation_ref","blocking_transition_evaluation_fingerprint","blocking_transition_decision_ref","blocking_transition_decision_fingerprint","resulting_state","resulting_state_version","resolution_source_contract_ref","resolution_source_contract_fingerprint","ordered_source_authority_refs","ordered_source_authority_fingerprints","issuance_sequence","issued_at"],"fingerprint_schema":"p1-4-blocker-provenance-v1","fixed_values":{"blocker_owner":"P1_4_SYSTEM_TRANSITION_AUTHORITY","blocker_version":"v1","resulting_state":"BLOCKED"},"schema_id":"P1_4_BLOCKER_PROVENANCE_SCHEMA_V1","taxonomy_fingerprint":"ec170cd257b04e77410951abe8c7f196a88bf8f35d9e6deaec8d8889bb0e9d0c"}
```

Canonical SHA-256: `b984abd21d657015d3b3febbe55588762ee481ea93fcfff868114b09b5943329`.

### 5.4 Single durable `G_BLOCKER_RESOLVED` authority

V1 chooses only explicit `P1_4BlockerResolvedAttestationV1`. Existing generic `GuardObservation`,
`TrustedGuardFact.reason`, or `authority_ref` alone is never durable resolution authority.

The attestation binds its identity/fingerprint and P1-4 owner; `guard_id=G_BLOCKER_RESOLVED`; exact blocker and
resumable reason; resolution source contract/ref/authority refs and fingerprints; project/TaskContract/version/
WorkRun/BLOCKED epoch; source/target/resulting states and versions; exact Request/Evaluation/Decision refs and
fingerprints; admitted outcome; owner event sequence; issued-at. The source tuple is independently resolved through
the exact source-owner verifier enrolled in the blocker. P1-4 records consumption, not source semantics.

```json
{"allowed_targets":["READY","HUMAN_REQUIRED","REWORK_REQUIRED"],"canonicalization":"JCS_RFC8785","fields":["attestation_id","attestation_ref","attestation_version","fingerprint_schema","owner","authority_ref","authority_version","authority_revision","guard_id","blocker_ref","blocker_fingerprint","reason_code","resolution_source_contract_ref","resolution_source_contract_fingerprint","resolution_source_ref","resolution_source_fingerprint","resolution_source_authority_ref","resolution_source_authority_fingerprint","project_id","task_contract_id","task_contract_version","work_run_id","blocked_epoch","source_state","source_state_version","target_state","transition_request_ref","transition_request_fingerprint","transition_evaluation_ref","transition_evaluation_fingerprint","transition_decision_ref","transition_decision_fingerprint","decision_outcome","resulting_state","resulting_state_version","owner_event_sequence","issued_at"],"fingerprint_schema":"p1-4-blocker-resolved-attestation-v1","fixed_values":{"attestation_version":"v1","decision_outcome":"ADMITTED","guard_id":"G_BLOCKER_RESOLVED","owner":"P1_4_SYSTEM_TRANSITION_AUTHORITY","source_state":"BLOCKED"},"non_resumable":"FORBIDDEN","schema_id":"P1_4_BLOCKER_RESOLVED_ATTESTATION_SCHEMA_V1"}
```

Canonical SHA-256: `0d92603174460dfd59be4b5bcb7a577014e8b51dad98fe992f08c3f638c43dbd`.

Exact order: independently verify blocker-enrolled source contract and immutable source; evaluate a fresh request
from exact BLOCKED version; create a typed evaluation observation bound to blocker/source; admit only an allowed
target; in the same P1-4 transaction append decision, state mutation, and final attestation, rolling all back on
failure. No attestation exists for denial. Historical replay rederives all objects; stored attestation hash alone is
insufficient. `g_blocker_resolved_attestation_ref/fingerprint` identifies exactly this object and nothing else.

### 5.5 Resolution transition and terminal transition

```text
blocker_resolution_transition_ref/fingerprint
= first admitted P1-4 transition that consumed the exact attestation and left BLOCKED

terminal_accepted_transition_ref/fingerprint
= later P1-4 terminal TransitionDecision resulting in ACCEPTED
```

P1-8 verifies blocker -> resolution transition -> later accepted Judgment/terminal transition -> exact terminal
epoch in one project/TaskContract/WorkRun lineage, then derives `P1_8_BLOCKER_RESOLUTION_RELATION_V2` by adding
only its current `resolution_cycle_id`. P1-4 never stores or depends on the Cycle ID. Later blocker/currentness
changes never rewrite historical objects.

## 6. Contract C — accepted NEXT_ACTION_CONTEXT enrollment

### 6.1 Immutable accepted inputs

| accepted contract | SHA-256 |
|---|---|
| source contract | `988cdd4c71aca75e3434652044b50ffd703fb32ba4568219c56d52e498cd8698` |
| priority-source enrollment | `f2b090057ae3f5f00ed4ef878a41664e2322988190969458e6a6544f76932f6b` |
| context ref schema | `842ac2619a3069a0b844cbaf89d36ceb252bfe1f1ec149097727f224a6cdc307` |
| owner event schema | `59e695623329908fdabce214a1d80be4249b4767c86844749de93094aeb7fce4` |
| P1-6 result schema | `db08fb7cbe1b55b7c686df28ffccbaf8462dd27dea7416e9b4478ae40e6cd67f` |
| Memory derivation | `6de3e66a0d16a1dc0038838eb58b9ca0ca6c2d790ab3a5cdcab3802b5093b508` |

The fixed serialized contract ref is
`next-action-context-source-contract:v1:NEXT_ACTION_CONTEXT_SOURCE_CONTRACT_V1`; its accepted fingerprint is
`988cdd4c...`. This serialization adds no authority and changes no source semantics beyond the prospective JCS
safe-integer/fingerprint reconciliation.

### 6.2 Exact context-bound descriptor and ActionRef

The catalog entry is an immutable action definition/template, not a selectable CYCLE_DERIVED descriptor. The
eligibility owner must issue a context-bound descriptor containing exact catalog/policy/action/project/
TaskContract/parameter/mode/Human/Task-issuer/security/currentness bindings plus:

```text
priority_classification_source_kind = NEXT_ACTION_CONTEXT_REF_V1
priority_classification_source_ref = exact current context_ref
priority_classification_source_hash = exact context fingerprint
priority_classification_source_contract_ref = fixed ref above
priority_classification_source_contract_fingerprint = 988cdd4c...
critical_path_ordinal = exact external object value 1..1,000,000
descriptor_policy_ordinal = 20
```

The descriptor fingerprint commits all fields except itself. `ActionRefV1` commits eligibility policy ID/version,
action ID/version, and descriptor fingerprint. Template, placeholder, caller binding, or Memory copy cannot produce
an ActionRef.

```json
{"action_id":"open-cycle-derived-task-issuance","action_ref_binding":"DESCRIPTOR_FINGERPRINT_COMMITS_ALL_FIELDS","allowed_selection_mode":"CYCLE_DERIVED","canonicalization":"JCS_RFC8785","critical_path_ordinal":{"maximum":1000000,"minimum":1,"source":"EXACT_ENROLLED_NEXT_ACTION_CONTEXT_REF_V1"},"descriptor_policy_ordinal":20,"fields":["descriptor_schema","eligibility_policy_id","eligibility_policy_version","catalog_ref","catalog_fingerprint","action_id","action_version","project_id","scope_kind","task_contract_id","task_contract_version","parameter_schema_id","parameter_schema_version","parameter_schema_fingerprint","allowed_selection_mode","priority_classification_source_kind","priority_classification_source_ref","priority_classification_source_hash","priority_classification_source_contract_ref","priority_classification_source_contract_fingerprint","critical_path_ordinal","descriptor_policy_ordinal","required_human_input","task_issuance_owner","privacy_restrictions","security_restrictions","issuance_event_sequence","effective_event_sequence","current_projection_on_invalidation"],"fixed_values":{"current_projection_on_invalidation":"WITHDRAW_CURRENT","priority_classification_source_contract_fingerprint":"988cdd4c71aca75e3434652044b50ffd703fb32ba4568219c56d52e498cd8698","priority_classification_source_contract_ref":"next-action-context-source-contract:v1:NEXT_ACTION_CONTEXT_SOURCE_CONTRACT_V1","priority_classification_source_kind":"NEXT_ACTION_CONTEXT_REF_V1","required_human_input":"AFTER_TASK_ISSUANCE_P1_7","scope_kind":"TASK_CONTRACT","task_issuance_owner":"EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY"},"schema_id":"P1_8_CYCLE_DERIVED_CONTEXT_BOUND_DESCRIPTOR_SCHEMA_V1"}
```

Canonical SHA-256: `bef330ffba29c24a76910d22c2de514235224add40b2725d4ac342a25dc4a7ed`.

```json
{"canonicalization":"JCS_RFC8785","fields":["eligibility_policy_id","eligibility_policy_version","action_id","action_version","descriptor_fingerprint"],"fingerprint_requirements":{"descriptor_fingerprint":"64_LOWERCASE_HEX"},"schema_id":"P1_8_ACTION_REF_SCHEMA_V1"}
```

ActionRef schema SHA-256: `d173e426e651497abbf45ba4abb6f38bdc9e9d54e4b3a63e76c33aa9e7edb2a2`.

This Task has no owner-issued context instance, so newly minted selectable descriptor/ActionRef count is exactly
zero. That is a closed boundary, not a placeholder. Future instance hashes are deterministic only after an actual
external owner object exists; no sentinel or design sample may be authority.

### 6.3 Exact evaluation order and ownership

1. verify current eligibility/selection policies, catalog, context-bound descriptor, and ActionRef at exact owner H;
2. verify exact NEXT_ACTION_CONTEXT Memory was CURRENT at selection Memory-applicability H and scope matches;
3. use its external ref/hash only as contextual locator;
4. compare Memory ref/hash with descriptor enrollment;
5. independently resolve accepted source contract and enrolled external ref;
6. fold selection-time external-owner H and require exact ref current;
7. compare resolved class/ordinal with Memory and descriptor equality copies;
8. derive class and `enrolled_critical_path_ordinal` only from external owner object;
9. selection policy maps class to rank and applies the accepted tuple.

External owner owns class and ordinal. Selection policy owns class-to-rank. Memory and descriptor ordinal copies are
equality-only. `descriptor_policy_ordinal` is P1-8 tie-break only. There is no
`source_memory_critical_path_ordinal`, `descriptor_catalog_ordinal`, or new ranking dimension.

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

Mappings remain 4/5/6 for `ACCEPTED_CORE_CRITICAL_PATH`, `OPERATIONAL_HARDENING`, and
`OPTIONAL_OPTIMIZATION`.

## 7. Reworked immutable policy payloads

### 7.1 Selection policy

Ranks/order/tuple are unchanged. Ranks 4–6 now bind the external source and require CURRENT Memory as contextual
input.

```json
{"classes":[{"allowed_source_authority_kinds":["P1_4_BLOCKER_PROVENANCE_V1"],"class":"SECURITY_POLICY_OR_MISSING_ARTIFACT","priority_rank":1,"reason_codes":["MISSING_REQUIRED_ARTIFACT","POLICY_CONFLICT","SECURITY_BOUNDARY"]},{"allowed_source_authority_kinds":["P1_4_BLOCKER_PROVENANCE_V1","P1_4_TRANSITION_DECISION_V1","P1_7_JUDGMENT_V1"],"class":"REJECTED_HOLD_FAILED_REWORK_RECOVERY","priority_rank":2,"reason_codes":["EXTERNAL_DEPENDENCY","FAILED","HOLD_REWORK_REQUIRED","REJECTED","REWORK_REQUIRED"]},{"allowed_source_authority_kinds":["P1_4_BLOCKER_PROVENANCE_V1"],"class":"BASELINE_OR_AUTHORITY_CONFLICT","priority_rank":3,"reason_codes":["AUTHORITY_CONFLICT","BASELINE_GAP"]},{"allowed_source_authority_kinds":["NEXT_ACTION_CONTEXT_REF_V1"],"class":"ACCEPTED_CORE_CRITICAL_PATH","priority_rank":4,"reason_codes":["ACCEPTED_CORE_CRITICAL_PATH"],"required_contextual_inputs":["CURRENT_NEXT_ACTION_CONTEXT_PROJECT_MEMORY_ENTRY"]},{"allowed_source_authority_kinds":["NEXT_ACTION_CONTEXT_REF_V1"],"class":"OPERATIONAL_HARDENING","priority_rank":5,"reason_codes":["OPERATIONAL_HARDENING"],"required_contextual_inputs":["CURRENT_NEXT_ACTION_CONTEXT_PROJECT_MEMORY_ENTRY"]},{"allowed_source_authority_kinds":["NEXT_ACTION_CONTEXT_REF_V1"],"class":"OPTIONAL_OPTIMIZATION","priority_rank":6,"reason_codes":["OPTIONAL_OPTIMIZATION"],"required_contextual_inputs":["CURRENT_NEXT_ACTION_CONTEXT_PROJECT_MEMORY_ENTRY"]}],"next_action_context_priority_source_enrollment_fingerprint":"f2b090057ae3f5f00ed4ef878a41664e2322988190969458e6a6544f76932f6b","policy_id":"P1_8_NEXT_ACTION_SELECTION_POLICY","policy_schema":"P1_8_NEXT_ACTION_PRIORITY_POLICY_V1","policy_version":"v1","proposal_claims":"AUDIT_ONLY","ranking_tuple":["authoritative_priority_rank","policy_dependency_ordinal","enrolled_critical_path_ordinal","descriptor_policy_ordinal","action_ref_lexical","proposal_id_lexical"]}
```

Canonical SHA-256: `4f84dbae89ee1113a2f6eeb28aa5d00100fcb65db2694b8716b52925d9bb312d`.

### 7.2 Catalog

Only two `REQUIRED_FOR_ACCEPTED_V1` Task-issuance handoffs remain. Both produce only
`TaskIssuanceCandidate`, require `AFTER_TASK_ISSUANCE_P1_7`, and leave issuance to the external Task authority.

Exact unchanged operational parameter schema:

```json
{"$schema":"https://json-schema.org/draft/2020-12/schema","additionalProperties":false,"properties":{"observed_state":{"enum":["BLOCKED","FAILED","REJECTED","REWORK_REQUIRED"]},"observed_state_version":{"minimum":1,"type":"integer"},"operational_fact_fingerprint":{"pattern":"^[0-9a-f]{64}$","type":"string"},"operational_fact_ref":{"maxLength":512,"minLength":1,"type":"string"},"operational_work_run_id":{"maxLength":160,"minLength":1,"pattern":"^[A-Za-z0-9][A-Za-z0-9._:/@-]{0,159}$","type":"string"}},"required":["operational_work_run_id","observed_state","observed_state_version","operational_fact_ref","operational_fact_fingerprint"],"type":"object"}
```

Exact unchanged cycle-derived parameter schema:

```json
{"$schema":"https://json-schema.org/draft/2020-12/schema","additionalProperties":false,"properties":{"memory_authority_event_high_watermark":{"minimum":0,"type":"integer"},"memory_entry_refs":{"items":{"maxLength":512,"minLength":1,"type":"string"},"maxItems":16,"minItems":1,"type":"array","uniqueItems":true},"next_action_context_fingerprint":{"pattern":"^[0-9a-f]{64}$","type":"string"},"next_action_context_ref":{"maxLength":512,"minLength":1,"type":"string"},"source_cycle_id":{"maxLength":160,"minLength":1,"pattern":"^[A-Za-z0-9][A-Za-z0-9._:/@-]{0,159}$","type":"string"}},"required":["source_cycle_id","memory_entry_refs","next_action_context_ref","next_action_context_fingerprint","memory_authority_event_high_watermark"],"type":"object"}
```

```json
{"authority_id":"P1_8_NEXT_ACTION_ELIGIBILITY_POLICY_AUTHORITY_V1","authority_revision":1,"authority_version":"AISCC-P1-8-NEXT-ACTION-POLICY-AUTHORITY-V1","catalog_id":"P1_8_POLICY_ACTION_CATALOG","catalog_ref":"p1-8-policy-action-catalog:v1:P1_8_POLICY_ACTION_CATALOG","catalog_schema":"P1_8_POLICY_ACTION_CATALOG_SCHEMA_V1","catalog_version":"v1","effective_sequence":1,"entries":[{"action_id":"open-operational-recovery-task-issuance","action_kind":"TASK_ISSUANCE_REVIEW","action_version":"v1","allowed_priority_classes":["BASELINE_OR_AUTHORITY_CONFLICT","REJECTED_HOLD_FAILED_REWORK_RECOVERY","SECURITY_POLICY_OR_MISSING_ARTIFACT"],"allowed_selection_modes":["OPERATIONAL_RECOVERY"],"critical_path_ordinal":0,"current_projection_on_invalidation":"WITHDRAW_CURRENT","descriptor_policy_ordinal":10,"parameter_defaults":{},"parameter_schema":{"$schema":"https://json-schema.org/draft/2020-12/schema","additionalProperties":false,"properties":{"observed_state":{"enum":["BLOCKED","FAILED","REJECTED","REWORK_REQUIRED"]},"observed_state_version":{"minimum":1,"type":"integer"},"operational_fact_fingerprint":{"pattern":"^[0-9a-f]{64}$","type":"string"},"operational_fact_ref":{"maxLength":512,"minLength":1,"type":"string"},"operational_work_run_id":{"maxLength":160,"minLength":1,"pattern":"^[A-Za-z0-9][A-Za-z0-9._:/@-]{0,159}$","type":"string"}},"required":["operational_work_run_id","observed_state","observed_state_version","operational_fact_ref","operational_fact_fingerprint"],"type":"object"},"parameter_schema_fingerprint":"92fe98cbc7cae63ab1f72161b625eb9bbd3281592f7731f98d24f30b4dd326f1","parameter_schema_id":"P1_8_OPERATIONAL_RECOVERY_PARAMETERS_V1","parameter_schema_version":"v1","policy_dependency_ordinal":10,"priority_rank_source":"RESOLVED_BY_SELECTION_POLICY","priority_source_contract_fingerprint":"4f84dbae89ee1113a2f6eeb28aa5d00100fcb65db2694b8716b52925d9bb312d","priority_source_contract_ref":"p1-8-next-action-selection-policy:v1:P1_8_NEXT_ACTION_SELECTION_POLICY","privacy_restrictions":["INTERNAL_ONLY","NO_PRIVATE_HUMAN_ARTIFACT_EXPORT","NO_RAW_MEMORY_CONTENT"],"project_scope":"CURRENT_SELECTION_PROJECT_ONLY","required_for_accepted_v1":true,"required_human_input":"AFTER_TASK_ISSUANCE_P1_7","scope_restrictions":["EXACT_OBSERVED_STATE_VERSION","EXACT_OPERATIONAL_WORK_RUN","EXACT_PROJECT","OWNER_VERIFIED_OPERATIONAL_FACT"],"security_restrictions":["NO_CREDENTIAL_OR_SECRET_INPUT","NO_PROVIDER_OR_NETWORK_ACTION","NO_TASKCONTRACT_MINT","NO_WORKFLOW_MUTATION","REFERENCE_PARAMETERS_ONLY"],"source_kind":"POLICY_ACTION_CATALOG","task_issuance_owner":"EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY","task_template_hash":null,"task_template_ref":null},{"action_id":"open-cycle-derived-task-issuance","action_kind":"TASK_ISSUANCE_REVIEW","action_version":"v1","allowed_priority_classes":["ACCEPTED_CORE_CRITICAL_PATH","OPERATIONAL_HARDENING","OPTIONAL_OPTIMIZATION"],"allowed_selection_modes":["CYCLE_DERIVED"],"context_bound_descriptor_schema_fingerprint":"bef330ffba29c24a76910d22c2de514235224add40b2725d4ac342a25dc4a7ed","context_bound_descriptor_schema_id":"P1_8_CYCLE_DERIVED_CONTEXT_BOUND_DESCRIPTOR_SCHEMA_V1","critical_path_ordinal_binding":"EXACT_CONTEXT_VALUE_1_TO_1000000","current_projection_on_invalidation":"WITHDRAW_CURRENT","descriptor_instantiation":"ELIGIBILITY_OWNER_CONTEXT_BOUND","descriptor_policy_ordinal":20,"parameter_defaults":{},"parameter_schema":{"$schema":"https://json-schema.org/draft/2020-12/schema","additionalProperties":false,"properties":{"memory_authority_event_high_watermark":{"minimum":0,"type":"integer"},"memory_entry_refs":{"items":{"maxLength":512,"minLength":1,"type":"string"},"maxItems":16,"minItems":1,"type":"array","uniqueItems":true},"next_action_context_fingerprint":{"pattern":"^[0-9a-f]{64}$","type":"string"},"next_action_context_ref":{"maxLength":512,"minLength":1,"type":"string"},"source_cycle_id":{"maxLength":160,"minLength":1,"pattern":"^[A-Za-z0-9][A-Za-z0-9._:/@-]{0,159}$","type":"string"}},"required":["source_cycle_id","memory_entry_refs","next_action_context_ref","next_action_context_fingerprint","memory_authority_event_high_watermark"],"type":"object"},"parameter_schema_fingerprint":"3e4407fef8f429031038018d8ee8fab0cb91ad583277f28e0d75064b226ea646","parameter_schema_id":"P1_8_CYCLE_DERIVED_PARAMETERS_V1","parameter_schema_version":"v1","policy_dependency_ordinal":20,"priority_classification_source_contract_fingerprint":"988cdd4c71aca75e3434652044b50ffd703fb32ba4568219c56d52e498cd8698","priority_classification_source_contract_ref":"next-action-context-source-contract:v1:NEXT_ACTION_CONTEXT_SOURCE_CONTRACT_V1","priority_classification_source_kind":"NEXT_ACTION_CONTEXT_REF_V1","priority_rank_source":"RESOLVED_BY_SELECTION_POLICY","priority_source_contract_fingerprint":"4f84dbae89ee1113a2f6eeb28aa5d00100fcb65db2694b8716b52925d9bb312d","priority_source_contract_ref":"p1-8-next-action-selection-policy:v1:P1_8_NEXT_ACTION_SELECTION_POLICY","priority_source_enrollment_contract_fingerprint":"f2b090057ae3f5f00ed4ef878a41664e2322988190969458e6a6544f76932f6b","privacy_restrictions":["INTERNAL_ONLY","NO_PRIVATE_HUMAN_ARTIFACT_EXPORT","NO_RAW_MEMORY_CONTENT"],"project_scope":"CURRENT_SELECTION_PROJECT_ONLY","required_descriptor_fields":["priority_classification_source_kind","priority_classification_source_ref","priority_classification_source_hash","priority_classification_source_contract_ref","priority_classification_source_contract_fingerprint","critical_path_ordinal","descriptor_policy_ordinal"],"required_for_accepted_v1":true,"required_human_input":"AFTER_TASK_ISSUANCE_P1_7","scope_restrictions":["CURRENT_MEMORY_AT_SELECTION_HIGH_WATERMARK","EXACT_PROJECT","SAME_TASK_CONTRACT_AND_WORK_RUN_MEMORY_CONTEXT","SINGLE_SOURCE_CYCLE"],"security_restrictions":["NO_CREDENTIAL_OR_SECRET_INPUT","NO_PROVIDER_OR_NETWORK_ACTION","NO_TASKCONTRACT_MINT","NO_WORKFLOW_MUTATION","REFERENCE_PARAMETERS_ONLY"],"source_kind":"POLICY_ACTION_CATALOG","task_issuance_owner":"EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY","task_template_hash":null,"task_template_ref":null}],"issuance_sequence":1,"revokes_ref":null,"supersedes_ref":null}
```

Canonical SHA-256: `c02290f5111608efbd3cd12edec9e066ca622133f262a1352d971fcddf02e58c`.

Exact affected descriptor/ActionRef inventory:

```text
operational descriptor payload =
JCS({descriptor_schema:"p1-8-next-action-descriptor-v1",
     catalog_ref:"p1-8-policy-action-catalog:v1:P1_8_POLICY_ACTION_CATALOG",
     catalog_fingerprint:"c02290f5...",
     entry:<the exact operational catalog entry above>})
descriptor fingerprint = 77bf03ba2125b32daef565739274a853cbfa03faab6477e37f4f9108517af8b0

operational ActionRefV1 =
{eligibility_policy_id:"P1_8_NEXT_ACTION_ELIGIBILITY_POLICY",
 eligibility_policy_version:"v1",
 action_id:"open-operational-recovery-task-issuance",
 action_version:"v1",
 descriptor_fingerprint:"77bf03ba..."}
canonical ActionRef identity SHA-256 =
a6a272fc7757439b7cc0877ace775d091539c25a4c3be8c0cd973cf2b746f157

cycle-derived catalog template payload =
JCS({descriptor_schema:"p1-8-next-action-descriptor-template-v1",
     catalog_ref:"p1-8-policy-action-catalog:v1:P1_8_POLICY_ACTION_CATALOG",
     catalog_fingerprint:"c02290f5...",
     entry:<the exact cycle-derived catalog entry above>})
template fingerprint = 7b766d3d3f3062381ebc1792cb4e4bc4768bf7be8963d8adff5b7e5a1bf29ddf
```

The cycle template fingerprint is not a selectable descriptor fingerprint and cannot appear in an ActionRef.
Concrete context-bound CYCLE_DERIVED descriptor/ActionRef count remains exactly zero until an external owner
context exists. `FINGERPRINT_EVIDENCE.md` records all three exact expanded canonical payloads.

Parameter schema payloads and fingerprints remain exact and unchanged:

```text
P1_8_OPERATIONAL_RECOVERY_PARAMETERS_V1 = 92fe98cbc7cae63ab1f72161b625eb9bbd3281592f7731f98d24f30b4dd326f1
P1_8_CYCLE_DERIVED_PARAMETERS_V1 = 3e4407fef8f429031038018d8ee8fab0cb91ad583277f28e0d75064b226ea646
```

Cycle parameters containing context ref/hash are caller locator/equality claims only.

### 7.3 Eligibility policy

```json
{"action_ref_schema_fingerprint":"d173e426e651497abbf45ba4abb6f38bdc9e9d54e4b3a63e76c33aa9e7edb2a2","authority_revision":1,"authority_version":"AISCC-P1-8-NEXT-ACTION-POLICY-AUTHORITY-V1","catalog_fingerprint":"c02290f5111608efbd3cd12edec9e066ca622133f262a1352d971fcddf02e58c","catalog_ref":"p1-8-policy-action-catalog:v1:P1_8_POLICY_ACTION_CATALOG","context_bound_descriptor_schema_fingerprint":"bef330ffba29c24a76910d22c2de514235224add40b2725d4ac342a25dc4a7ed","current_descriptor_requirement":"EXACT_CURRENT_UNSUPERSEDED_OWNER_ISSUED","current_policy_requirement":"EXACT_CURRENT_UNSUPERSEDED","current_projection_on_invalidation":"WITHDRAW_CURRENT","effective_sequence":1,"eligibility_owner":"P1_8_NEXT_ACTION_ELIGIBILITY_POLICY_AUTHORITY_V1","issuance_sequence":1,"policy_id":"P1_8_NEXT_ACTION_ELIGIBILITY_POLICY","policy_ref":"p1-8-next-action-eligibility-policy:v1:P1_8_NEXT_ACTION_ELIGIBILITY_POLICY","policy_schema":"P1_8_NEXT_ACTION_ELIGIBILITY_POLICY_SCHEMA_V1","policy_version":"v1","priority_source_enrollment_contract_fingerprint":"f2b090057ae3f5f00ed4ef878a41664e2322988190969458e6a6544f76932f6b","revokes_ref":null,"selection_precondition_order":["POLICIES_CURRENT","ACTION_REF_DESCRIPTOR_CURRENT","CURRENT_MEMORY_CONTEXT","DESCRIPTOR_SOURCE_ENROLLMENT","EXTERNAL_SOURCE_CURRENT","OWNER_EQUALITY","RANK"],"supersedes_ref":null,"unknown_action_ref":"DENY_BEFORE_RANKING"}
```

Canonical SHA-256: `a0425bee1c2abf26c50a63ff125795e88e0b15e6f182dfbf716fc5f0217d6d03`.

## 8. Historical replay and current applicability

```text
TaskConstraint historical = original ref + original certified event H -> original validity
TaskConstraint current = latest certified H -> current ref or none

blocker historical = blocker + source + resolved attestation + resolution transition
  + later terminal ACCEPTED transition + current Cycle relation -> deterministic rederivation

historical selection = original CURRENT Memory at selection H
  + original policies/catalog/descriptor/ActionRef prefixes
  + external context payload/currentness at selection external-owner H
  + original class/ordinal/mapping/tuple -> same immutable identity

new selection = latest current Memory + policies + descriptor + external source
```

Later revocation/supersession changes only append-only current applicability. Missing/tampered original payload or
prefix is historical corruption; ordinary later staleness is current ineligibility. The accepted carrier/body H is
still `AUTHORING_SNAPSHOT_PROVENANCE_ONLY`, and terminal external-context currentness remains `NOT_REQUIRED_V1`.

## 9. P1-6 boundary

`P1-6 Requirement fingerprint-schema extension = NOT_REQUIRED_V1`. P1-6 V2 already binds schema ID/version,
durable policy, canonical bytes, admission, and terminal-consumed root. Accepted P1-8/external contracts bind
selector, source contract, equality, and priority semantics. Adding a P1-6 semantic-contract field would duplicate
authority and alter accepted identity. Future semantic change uses a new result schema/policy/Requirement
prospectively, never in-place mutation or legacy backfill.

## 10. Fingerprint inventory

For every immutable object/event/snapshot/attestation/descriptor instance defined here, its own fingerprint field
is excluded and the exact remaining payload is hashed as
`sha256(UTF8(JCS_RFC8785(payload_without_own_fingerprint)))`. Schema/policy/catalog contract fingerprints hash the
complete canonical JSON block printed in this document. Unknown fields, non-NFC strings, BOM, floating point, and
non-canonical serialization fail closed.

| item | predecessor | candidate | result |
|---|---|---|---|
| TaskConstraint ref/event/snapshot schemas | 1601 candidate | `c3bba5050a43a37c2563518d862a4b7fc1c3ee344cd763ab66da19d15a7126cc` / `2b4bd41b7dbf7f002f2b48aabcf816ac386d860c12c20e947843bee5390c9b00` / `41330e2502ae9c337a3a1e8dfc693b2fb9307bec9eb5b5138e33ad7cdd35c1aa` | ref unchanged; event/snapshot JCS-safe bounds reconciled |
| blocker taxonomy/provenance/resolved schemas | ambiguous/absent | `ec170cd257b04e77410951abe8c7f196a88bf8f35d9e6deaec8d8889bb0e9d0c` / `b984abd21d657015d3b3febbe55588762ee481ea93fcfff868114b09b5943329` / `0d92603174460dfd59be4b5bcb7a577014e8b51dad98fe992f08c3f638c43dbd` | closed/new |
| six NEXT_ACTION_CONTEXT contracts | historical accepted predecessor in section 6.1 | corrected source graph in section 6.1 | JCS-safe bound and dependent fingerprints only; enrollment unchanged |
| cycle descriptor binding / ActionRef schemas | 1601 candidate | `bef330ffba29c24a76910d22c2de514235224add40b2725d4ac342a25dc4a7ed` / `d173e426e651497abbf45ba4abb6f38bdc9e9d54e4b3a63e76c33aa9e7edb2a2` | binding cascaded; ActionRef schema unchanged |
| operational/cycle parameter schemas | `92fe98cb...` / `3e4407fe...` | unchanged | payloads unchanged |
| selection policy | `f7c69da9...` | `4f84dbae89ee1113a2f6eeb28aa5d00100fcb65db2694b8716b52925d9bb312d` | changed external authority binding |
| catalog | `944e3948...` | `c02290f5111608efbd3cd12edec9e066ca622133f262a1352d971fcddf02e58c` | cascaded source-contract and descriptor-schema fingerprints |
| eligibility policy | `cc0df6f3...` | `a0425bee1c2abf26c50a63ff125795e88e0b15e6f182dfbf716fc5f0217d6d03` | cascaded catalog and descriptor-schema fingerprints |
| concrete bound descriptor/ActionRef | none | none minted | exact zero; owner object absent, sentinel forbidden |

Canonical JSON is UTF-8/no BOM/NFC `JCS_RFC8785`, no floating point. Writer and independent verifier values are
recorded in `FINGERPRINT_EVIDENCE.md`.

## 11. Exact question answers

| # | answer |
|---:|---|
| 1 | Section 4.2 fixes required/forbidden fields; `scope_id` is absent and display-only derived. |
| 2 | Pure revoke is exactly `TaskConstraintAuthorityEventV1(REVOKED)` with null replacements. |
| 3 | Section 4.5 fixes certified H, prefix completeness, ordering, replay/conflict, and result. |
| 4 | Only private external Task composition writes; P1-8/callers receive read/verifier ports. |
| 5 | `SECURITY, POLICY, ARTIFACT, BASELINE, AUTHORITY, EXTERNAL_DEPENDENCY, EXECUTION`. |
| 6 | `SECURITY_BOUNDARY, POLICY_CONFLICT, MISSING_REQUIRED_ARTIFACT, BASELINE_GAP, AUTHORITY_CONFLICT, EXTERNAL_DEPENDENCY, EXECUTION_BLOCKER`. |
| 7 | Section 5.2 is the closed one-to-one matrix. |
| 8 | All except `SECURITY_BOUNDARY` are RESUMABLE. |
| 9 | No; NON_RESUMABLE uses `BLOCKED -> FAILED` only. |
| 10 | Only `P1_4BlockerResolvedAttestationV1`, atomically bound to admitted P1-4 decision/mutation. |
| 11 | The seven accepted enrollment fields listed in section 6.2; descriptor fingerprint/ActionRef commit them. |
| 12 | Policy/catalog/descriptor currentness -> CURRENT Memory -> enrollment equality -> independent external fold -> owner equality -> rank. |
| 13 | External context owner owns class/ordinal; selection policy owns class-to-rank; descriptor policy ordinal is tie-break. |
| 14 | Memory class/ordinal and descriptor ordinal are equality-only copies. |
| 15 | Owner is `P1_8_NEXT_ACTION_SELECTION_POLICY_AUTHORITY_V1`; tuple is the unchanged six-field tuple in section 6.3. |
| 16 | Section 10 records all changed/new policy/schema hashes; no concrete runtime ActionRef existed or is minted. |
| 17 | Both parameter schemas and the priority-source enrollment fingerprint are unchanged; the other five source-graph fingerprints are JCS-safe reconciliations. |
| 18 | Section 8 rederives original prefixes first and folds latest applicability separately. |
| 19 | P1-6 owns carrier provenance; accepted P1-8/external contracts own selector/equality/semantics, so extension would duplicate authority. |
| 20 | No load-bearing semantic alternative remains. Human only accepts/reworks/rejects this exact candidate; owner runtimes are future prerequisites. |

## 12. Persistence cut-line and gate

Future order: external TaskConstraint object/event/snapshot runtime and acceptance; additive P1-4 blocker/source/
attestation/transition runtime and acceptance; additive P1-8 catalog/policy/descriptor persistence; then only a new
authorized P1-8 runtime rework. No accepted row/payload/fingerprint/root/transition/rule or blocked runtime byte is
rewritten. Legacy Task Markdown, generic blocker facts, caller catalog/config, and metadata-only evidence remain
ineligible; no backfill or hash-only grandfathering.

The predecessor candidate SHA-256 is
`189156a190a13c92830d5b4c7ae28cd41f52f6c438dacda9e145bc82dd2d36d7`. These edited bytes change only the
normative JSON safe-integer ceiling and the dependent cross-contract fingerprints. They are a joint rework
candidate, not Human acceptance or runtime authority. Every normative sequence/high-watermark JSON integer is
bounded by `9007199254740991`; arbitrary-precision lexical hashing and a custom JCS dialect are forbidden.

```text
P1-8 prerequisite owner-authority design = JOINT_REWORK_CANDIDATE / HUMAN_REVIEW_REQUIRED
P1-8 Runtime = BLOCKED_REQUIRED_EVIDENCE
P2/P3 = NOT_STARTED
PUBLIC_BOUNDED_LIVE = NOT_RELEASED
```

Human acceptance is necessary but does not implement prerequisites or resume runtime.
