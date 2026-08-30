# AISCC Durable Evidence Content Authority Design

document_id: `AISCC-P1-6-DURABLE-EVIDENCE-CONTENT-AUTHORITY-DESIGN-1`  
design_status: `REWORKED_DESIGN_CANDIDATE / HUMAN_PENDING`
acceptance_owner: `Human`  
implementation_status: `DESIGN_ONLY / NOT_STARTED`  
semantic_owner: `P1_6_EVIDENCE_CONTENT / P1_6_EVIDENCE_REQUIREMENT_COMPATIBILITY`
accepted_p1_6_design_sha256: `0d9d4c194efda37f100c6183d1a7e88e1a09fe073dc3a37bbb5a3e1cd577e463`  
accepted_p1_8_design_sha256: `100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a`  
created_at_kst: `2026-08-30`

> 이 문서는 P1-6 durable structured-content persistence extension의 design candidate다. Human final
> acceptance 전에는 runtime/schema authority가 아니며 구현을 시작할 수 없다.

## 1. Purpose and scope

이 extension은 P1-6 content persistence만 보충한다. 목적은 owner-backed canonical structured evidence
body를 process restart 뒤에도 byte-exact하게 검증·해결하여, Human-accepted P1-8
`STRUCTURED_RESULT_ATTESTED`가 caller-provided content를 신뢰하지 않고 source field/object를 재구성할
수 있게 하는 것이다.

이 extension은 다음 authority를 supersede, 재판정, 복제 또는 흡수하지 않는다.

```text
EvidenceRequirement
EvidenceCandidate
Evidence admission dimensions and EvidenceAdmissionDecision
AdmittedEvidence
EvidenceSetEvaluation / EvidenceSetSatisfactionAttestation
G_EVIDENCE
P1-4 TransitionDecision / WorkflowState
P1-7 HumanGate / HumanResult / Judgment
P1-8 AdmittedCycle / ProjectMemory / NextActionSelection
```

Normative non-substitution:

```text
DurableEvidenceContentObject != EvidenceCandidate
DurableEvidenceContentObject != AdmittedEvidence
durable content availability != evidence admission
historical content integrity != current evidence effectiveness
content store != Judgment != TransitionDecision
P1-8 content consumer != P1-6 content writer
hash-only metadata != durable canonical body authority
```

## 2. Current baseline gap

Accepted P1-6 correctly admits evidence by resolving an owner-backed body/ref, then durably preserves immutable
metadata/hash/ref and admission provenance. Current `PrivateEvidenceContentStore` holds bytes in process-local
`_objects` and authorizes resolution through process-local `_owner_token` identity. PostgreSQL candidate and
admitted rows preserve `EvidenceContentRef` metadata and `content_hash`, not canonical body bytes.

This remains valid for accepted P1-6 admission history. It is insufficient only for a later consumer that must
reconstruct exact structured field/object bytes after process loss. Missing bytes remain `CONTENT_MISSING`; no
caller summary, matching hash string, or newly supplied body may fill the gap.

### 2.1 Existing fingerprint and historical-verifier audit

The compatibility rework inspected the exact accepted runtime symbols rather than assuming that a dataclass
default preserves an immutable hash:

| Contract | Current exact symbol/path | Existing identity rule |
|---|---|---|
| Requirement issuance/fingerprint | `TaskContractEvidenceAuthority.seal_requirement`, `_requirement_payload` in `src/aiscc/evidence/requirements.py` | SHA-256 `canonical_hash` of the exact pre-extension domain payload |
| Canonical hash | `canonical_json_bytes`, `canonical_hash` in `src/aiscc/evidence/models.py` | UTF-8 JSON, `ensure_ascii=False`, sorted keys, comma/colon separators |
| RequirementSet root/fingerprint | `TaskContractEvidenceAuthority.seal_set`, `_set_payload` in `src/aiscc/evidence/requirements.py` | root over ordered `(requirement_ref, requirement_fingerprint)` pairs; set fingerprint over the unchanged set payload |
| AdmissionRequest fingerprint | `make_admission_request` in `src/aiscc/evidence/admission.py` | commits candidate fingerprint, Requirement fingerprint, RequirementSet root, checkpoint fingerprint and request bindings |
| Requirement/Set rows | `_requirement_row`, `_set_row` in `src/aiscc/evidence/repository.py`; `EvidenceRequirementRow`, `EvidenceRequirementSetRow` in `src/aiscc/persistence/models.py` | immutable fingerprint/root columns plus exact JSONB payload shapes |
| Set evaluation/attestation | `_set_evaluation_payload`, `_attestation_payload`, `verify_historical_set_attestation_provenance` in `src/aiscc/evidence/repository.py` | commits the exact full/subset/admitted roots; exact payload-key validation |
| Admission history | `_historical_request_authority_graph`, `_verify_historical_admission_request`, `_verify_historical_evaluation` in `src/aiscc/evidence/repository.py` | reconstructs exact Requirement/Set/request/evaluation authority and fails on shape or hash drift |
| P1-7 historical consumers | `src/aiscc/human/repository.py`, `src/aiscc/judgment/authority.py` | consume `verify_historical_set_attestation_provenance`; P1-6 root drift propagates into Human/Judgment provenance failure |

The current Requirement row contains no fingerprint-schema discriminator. Therefore adding
`durable_content_requirement=NOT_APPLICABLE` to an in-memory legacy object and hashing the expanded shape would
change the accepted historical identity. This rework closes that gap prospectively without changing any stored
legacy canonical payload, fingerprint, root, request, evaluation, attestation or admission identity.

## 3. Selected V1 owner and storage model

V1 selects exactly:

```text
storage system:
PostgreSQL 17-compatible bytea

content authority:
AISCC_P1_6_DURABLE_CONTENT_AUTHORITY_V1

writer owner:
P1-6 Content Ingress Service only

maximum canonical body bytes:
65,536

external object store/provider:
NOT_USED
```

The PostgreSQL row and its append-only candidate binding are durable authority. A process-local cache may improve
performance but is never an identity, write-authority, historical-validity, or restart input.

## 4. Exact domain vocabulary

- `DurableContentRequirement`: immutable Requirement capability, exactly `REQUIRED | NOT_APPLICABLE`.
- `DurableContentPolicyRef`: exact versioned P1-6 policy for allowed kind, canonicalization, size, sensitivity,
  access, retention, and consumer use.
- `DurableEvidenceContentObject`: immutable bounded canonical structured bytes plus exact owner/store metadata.
- `DurableEvidenceContentRef`: stable serialized reference to one logical owner/object/version identity.
- `EvidenceCandidateDurableContentBinding`: immutable proof that a candidate was created with an exact durable
  object under an already-issued Requirement version and policy.
- `AuthenticatedContentOwnerContextV1`: non-caller-constructible P1-6 ingress context produced after registered
  issuer/content-owner verification.
- `VerifiedHistoricalContent`: recomputed immutable metadata/fingerprint plus canonical bytes.
- `HistoricalContentAccessGrant`: current access authorization for a named internal consumer; it does not create
  or repair historical content authority.
- `RequirementFingerprintSchema`: immutable persisted algorithm selector, exactly
  `P1_6_EVIDENCE_REQUIREMENT_FINGERPRINT_V1 | P1_6_EVIDENCE_REQUIREMENT_FINGERPRINT_V2_DURABLE_CONTENT`.

V1 deliberately has no `OPTIONAL` capability. Ambiguous optional durability would allow a consumer to infer
authority from mere row presence. A Requirement either requires the exact durable path or it does not enroll it.

## 5. Durable object identity

### 5.1 Logical identity

`DurableContentIdentityV1` is canonical JSON over:

```text
{
  identity_schema: "p1-6-durable-content-identity-v1",
  owner_id,
  owner_version,
  object_id,
  object_version
}
```

`content_identity_key = lowercase_sha256(DurableContentIdentityV1 bytes)`.

Stable serialized ref:

```text
p1-6-durable-content:v1:<content_identity_key>
```

The ref does not contain current evidence state, WorkRun state, current RequirementSet, current authority
revision, retention observation time, or P1-8 identity.

### 5.2 Immutable fields

`DurableEvidenceContentObjectV1` contains exactly:

```text
serialized_ref
content_identity_key

owner_id
owner_version
source_owner_authority_ref
source_owner_authority_fingerprint

object_id
object_version

content_kind
canonicalization
schema_id
schema_version

byte_count
content_hash_algorithm = SHA-256
content_hash

sensitivity
retention_policy
access_policy

canonical_body_bytes

created_at

content_authority_id = AISCC_P1_6_DURABLE_CONTENT_AUTHORITY_V1
content_authority_version = 1
content_authority_revision = 1

payload_fingerprint_schema = p1-6-durable-content-payload-v1
payload_fingerprint
```

`payload_fingerprint` is SHA-256 of canonical metadata containing every field above except
`canonical_body_bytes` and `payload_fingerprint`; `content_hash` and `byte_count` commit to the exact bytes.
Historical verification independently hashes the stored `bytea`, so a metadata-only match is insufficient.

Same owner/object identity and same complete payload fingerprint is idempotent. Same identity with different
bytes, hash, schema, kind, sensitivity, retention, access policy, or owner authority is
`DURABLE_CONTENT_IDENTITY_CONFLICT`.

## 6. Exact canonical structured JSON V1

All eligible V1 bodies use `AISCC_CANONICAL_STRUCTURED_JSON_V1`:

```text
encoding: UTF-8, no BOM
JSON values: null, boolean, signed 64-bit integer, string, array, object
floating point / NaN / Infinity: forbidden
object keys: Unicode NFC strings, unique before and after NFC normalization
strings: Unicode NFC
object order: normalized keys sorted by Unicode code point
separators: comma and colon, no insignificant whitespace
ASCII escaping: disabled except required JSON escapes
maximum nesting depth: 32
maximum total value/key nodes: 4,096
```

If ingress begins as raw JSON bytes, its raw byte length must be `1..65,536` before parsing. After parse,
normalization, validation, and canonical serialization, canonical bytes must again be `1..65,536`. An in-memory
object ingress is bounded during traversal by depth/node limits and the same final byte ceiling. V1 provides no
streaming, chunking, compression, large-object, or TOAST-bypass authority path.

## 7. Exact V1 eligible content kinds

| EvidenceContentKind | Durable V1 | Canonicalization | Schema | Max bytes | Sensitivity ceiling | Field/object access |
|---|---:|---|---|---:|---|---|
| `INLINE_CANONICAL_STRUCTURED_BODY` | Yes | `AISCC_CANONICAL_STRUCTURED_JSON_V1` | exact non-empty Requirement-enrolled ID/version | 65,536 | `INTERNAL` | Yes, policy-fixed JSON Pointer only |
| `DATABASE_OBSERVATION_REF` | Yes | `AISCC_CANONICAL_STRUCTURED_JSON_V1` | exact non-empty observation schema ID/version | 65,536 | `INTERNAL` | Yes, policy-fixed JSON Pointer only |
| `RUNTIME_OBSERVATION_REF` | Yes | `AISCC_CANONICAL_STRUCTURED_JSON_V1` | exact non-empty observation schema ID/version | 65,536 | `INTERNAL` | Yes, policy-fixed JSON Pointer only |
| `HUMAN_STRUCTURED_REF` | No | n/a | n/a | n/a | n/a | No |
| `P1_5_IMMUTABLE_PRODUCER_REF` | No | existing owner/ref path | existing | n/a | existing | No new body copy |
| `PRIOR_ADMITTED_EVIDENCE_REF` | No | existing P1-6 reuse path | existing | n/a | existing | No new body copy |
| `CONTENT_ADDRESSED_ARTIFACT_REF` | No | existing artifact/ref path | existing | n/a | existing | No arbitrary blob copy |

`HUMAN_STRUCTURED_REF` remains valid P1-6 evidence when its accepted rules pass, but V1 does not durably copy its
body because the current critical path can consume exact P1-7 Judgment authority separately and no bounded
identity-free Human-content export/encryption contract is accepted. A future Human-accepted revision is required
to add it.

Database/runtime bodies may contain only the bounded structured result object. Raw logs, dumps, stack traces,
attachments, stdout/stderr, filesystem images, or unrestricted result collections remain outside this store.

## 8. Sensitivity, access, and export matrix

| EvidenceSensitivity | Durable body | Historical internal resolution | Review export | Public export |
|---|---:|---|---|---|
| `PUBLIC_SAFE` | Supported when Requirement policy allows | authorized P1-6/P1-8 consumer | metadata by default; body only by exact export policy | body only with `PUBLIC_SAFE_EXPORT` and exact export-policy version |
| `INTERNAL` | Supported | exact internal consumer grant required | metadata/hash/ref by default | body denied |
| `PRIVATE_SENSITIVE` | `NOT_SUPPORTED_IN_DURABLE_STRUCTURED_STORE_V1` | none | metadata-only existing P1-6 path | body denied |
| `SECRET_FORBIDDEN` | Never stored | none | sanitized detector/rejection metadata only | none |

The selected competition V1 makes no unverified encryption-at-rest claim. PostgreSQL connection/storage security
remains deployment policy, but this design avoids relying on it for `PRIVATE_SENSITIVE` eligibility. A
`PRIVATE_SENSITIVE` body may remain in an accepted private owner store and be valid P1-6 evidence; it is simply not
eligible for this extension or P1-8 `STRUCTURED_RESULT_ATTESTED`.

Durable availability never broadens `EvidenceContentRef.sensitivity`, `access_policy`, or export permission.
P1-8 may derive a private/internal memory projection but cannot return or export raw source bytes to its caller.

## 9. Retention policy

V1 durable objects use exactly:

```text
retention_policy = P1_8_HISTORICAL_RECONSTRUCTION_RETAIN_V1
automatic expiry/deletion = NOT_SUPPORTED
owner API update/delete = FORBIDDEN
database FK delete = RESTRICT
```

The body must remain available for at least the complete project/competition provenance lifetime and every
referencing P1-8 historical Cycle/Memory lifetime. V1 avoids an underspecified timer and never turns deletion into
successful historical verification. A future legal deletion/tombstone flow requires a separate Human-accepted
policy, explicit inaccessible state, retained non-secret identity/hash provenance, and fail-closed consumers.

Evidence revocation, supersession, current staleness, or WorkRun transition does not delete or mutate the body.

## 10. Owner-backed write authority

Only `AISCC_P1_6_DURABLE_CONTENT_AUTHORITY_V1` may write. Exact path:

```text
owner-backed canonical source
-> registered P1-6 issuer/content-owner verification
-> AuthenticatedContentOwnerContextV1
-> Requirement durable policy resolution
-> P1-6 canonicalization/schema/sensitivity/size validation
-> P1-6 repository insert
-> DurableEvidenceContentRef
-> immutable candidate binding
```

`AuthenticatedContentOwnerContextV1` binds:

```text
owner_id / owner_version
source_owner_authority_ref / fingerprint
issuer type/id/version and producer attestation ref
TaskContract and exact Requirement ref/fingerprint
DurableContentPolicy ref/fingerprint
candidate ID/version
content ingress request ID/fingerprint
authenticated_at
```

It is constructed only inside P1-6 after existing registered issuer/content-owner verification. Public DTOs,
P1-8, Agent, Executor, caller, and generic repository users cannot mint it. `_owner_token` may remain a local
method-call capability or test fixture, but it is neither serialized nor used by historical verification.

Implementation must additionally grant `INSERT` on content/binding tables only to the P1-6 content-writer DB
role used by the P1-6 service transaction. P1-8 receives read/execute access only through the owner API, not raw
table write access. Tables reject `UPDATE` and `DELETE` by trigger.

Forbidden:

```text
P1-8 direct INSERT/UPDATE/DELETE
caller body passed to historical resolver
hash-only row fabrication
content row created from an already-admitted metadata-only candidate
generic admin/repository method exposed as content authority
```

## 11. Requirement fingerprint schema, enrollment, and cut line

### 11.1 Selected compatibility model

This design selects explicit Requirement fingerprint schema V1/V2. It does **not** select a companion-only
`DurableContentRequirementEnrollment` model.

```text
P1_6_EVIDENCE_REQUIREMENT_FINGERPRINT_V1
  = exact accepted pre-extension Requirement canonical payload and hash algorithm

P1_6_EVIDENCE_REQUIREMENT_FINGERPRINT_V2_DURABLE_CONTENT
  = exact V1 canonical fields
  + explicit fingerprint_schema
  + durable_content_requirement
  + durable_content_policy_ref
  + durable_content_policy_fingerprint
```

The persisted immutable selector is `EvidenceRequirementRow.fingerprint_schema`. It is algorithm authority, not a
current default, runtime-code version, migration revision, current policy version, issuance timestamp heuristic,
or inference from nullable durable fields. The verifier switches only on this stored value.

### 11.2 Exact V1 canonical fingerprint contract

For `P1_6_EVIDENCE_REQUIREMENT_FINGERPRINT_V1`, the canonical domain payload has exactly the existing keys and
structures below and no `fingerprint_schema` or durable-content field:

```text
{
  ref,
  task: [task_contract_id, task_contract_version],
  set: [requirement_set_id, requirement_set_version],
  owner,
  profile,
  obligation,
  checkpoints: [ordered values],
  type: [evidence_type_id, evidence_type_version],
  issuer_types: [sorted values],
  issuer_ids: [sorted values],
  human_categories: [sorted values],
  content_kinds: [sorted values],
  schema: [schema_id, schema_version],
  subject,
  scope,
  resource,
  freshness: {kind, max_age_seconds, config_version},
  coverage: [sorted values],
  reuse_maximum,
  compatible: [sorted values],
  maximum_sensitivity,
  public_export_allowed,
  issued_at,
  revoked_at,
  supersedes
}
```

The exact algorithm remains `SHA-256(canonical_json_bytes(payload))`, where `canonical_json_bytes` is the accepted
UTF-8 `json.dumps(..., ensure_ascii=False, sort_keys=True, separators=(",", ":"))` result. No field may be
inserted, removed, renamed, defaulted or normalized before hashing a V1 object.

A V1 Requirement's durable capability view is semantically `NOT_APPLICABLE`, but that view is **not** a V1
serialized field and is never included in its canonical bytes. In particular:

```text
legacy semantic NOT_APPLICABLE
!= synthesize durable_content_requirement into V1 payload
```

### 11.3 Exact V2 durable-capable fingerprint contract

Only a prospectively issued durable-capable Requirement version uses
`P1_6_EVIDENCE_REQUIREMENT_FINGERPRINT_V2_DURABLE_CONTENT`. Its canonical payload contains every exact V1 field
plus exactly:

```text
fingerprint_schema:
P1_6_EVIDENCE_REQUIREMENT_FINGERPRINT_V2_DURABLE_CONTENT

durable_content_requirement:
REQUIRED

durable_content_policy_ref:
exact non-empty versioned P1-6 policy ref

durable_content_policy_fingerprint:
exact lowercase SHA-256
```

V2 uses the same canonical JSON and SHA-256 algorithm after adding those four exact fields. V2
`durable_content_requirement` is `REQUIRED`; `NOT_APPLICABLE` remains the semantic V1 result rather than a reason
to mint a V2 identity. This preserves the closed two-value domain vocabulary while ensuring that only an actually
durable-capable new version receives the new fingerprint identity.

The current TaskContract/Requirement authority, not a caller, selects issuance through separate server-owned V1
and V2 sealing paths. V2 is legal only for one of the three allowed kinds, the exact canonicalization/schema,
sensitivity `PUBLIC_SAFE | INTERNAL`, and the fixed V1 size/retention/access policy. Changing capability or policy
requires a new Requirement ref/version, new fingerprint, new RequirementSet version/root, and new
candidate/admission.

### 11.4 Exact immutable row shapes

The physical `fingerprint_schema` selector is stored outside the canonical JSONB payload for every row. For V1 it
selects the old algorithm but is excluded from V1 canonical bytes. For V2 it must equal the identical
`fingerprint_schema` value inside the V2 canonical domain payload and V2 row payload.

Legacy/V1 `EvidenceRequirementRow.payload` retains exactly the accepted keys:

```text
task_contract_id
task_contract_version
applicable_checkpoint_refs
evidence_type_id
evidence_type_version
allowed_issuer_types
allowed_issuer_ids
allowed_human_categories
allowed_content_kinds
schema_id
schema_version
subject_id
scope_id
resource_id
freshness_kind
freshness_max_age_seconds
freshness_config_version
required_coverage
reuse_maximum
compatible_requirement_refs
maximum_sensitivity
public_export_allowed
revoked_at
supersedes_requirement_ref
```

V2 row payload has that exact set plus exactly
`fingerprint_schema`, `durable_content_requirement`, `durable_content_policy_ref`, and
`durable_content_policy_fingerprint`. Missing, extra, null, blank, incorrectly cased, or malformed values fail
closed. An in-memory developer default never changes the version-appropriate serialized shape.

### 11.5 RequirementSet root and fingerprint compatibility

`EvidenceRequirementSet` does not acquire a V2 payload or fingerprint schema. Its existing algorithms are
sufficient and remain exact:

```text
requirement_root_hash
= canonical_hash(ordered [(requirement_ref, verified requirement fingerprint)])

RequirementSet fingerprint
= canonical_hash(existing _set_payload shape)
```

For a legacy set, every member is verified with exact V1 canonical bytes; therefore every Requirement fingerprint,
the root, the set payload and the set fingerprint are byte/hash-identical after upgrade. A new set containing a V2
Requirement naturally has a new version/root because the ordered pair contains that exact V2 fingerprint. No
synthetic durable field is inserted into a legacy Requirement or RequirementSet.

### 11.6 AdmissionRequest, evaluation, and attestation compatibility

No durable-content field is added to `EvidenceAdmissionRequest`, `EvidenceEvaluation`, `EvidenceSetEvaluation`, or
`EvidenceSetSatisfactionAttestation` payload/fingerprint schemas. Existing bindings already commit enough:

```text
AdmissionRequest
  -> candidate fingerprint
  -> exact Requirement ref/fingerprint
  -> exact RequirementSet ref/root
  -> checkpoint fingerprint

EvidenceSetEvaluation / Attestation
  -> full RequirementSet root
  -> checkpoint subset root
  -> admitted-evidence root and exact refs
```

The separate immutable durable candidate binding commits the candidate fingerprint, Requirement fingerprint,
RequirementSet root, policy and durable content ref. For V2, P1-6 verifies that binding under the existing
`CONTENT_INTEGRITY` evaluation authority before admission. Redundant durable fields are therefore forbidden in the
request/evaluation/attestation payloads.

Consequences:

- every legacy AdmissionRequest ID/fingerprint remains exact;
- every legacy admission Evaluation/Decision/AdmittedEvidence identity remains exact;
- every legacy set Evaluation ID/root/payload remains exact;
- every legacy set Attestation ID/ref/payload remains exact;
- new V2 values produce new downstream identities only through their prospectively new Requirement fingerprint
  and RequirementSet roots.

This is an additional content-integrity capability inside accepted P1-6 Requirement authority. It does not add a
sixth evidence profile, change obligation/completeness, redefine an admission dimension, change `G_EVIDENCE`, or
make content availability equal evidence truth.

Admission error mapping preserves the accepted `EvidenceRejectionReason` vocabulary:

| Durable detail | Existing P1-6 rejection/result |
|---|---|
| required object/binding absent | `CONTENT_MISSING` |
| kind not allowed | `TYPE_MISMATCH` |
| oversize or canonical/schema mismatch | `SCHEMA_INVALID` |
| sensitivity denied | `FORBIDDEN_EVIDENCE` |
| body hash mismatch | `CONTENT_HASH_MISMATCH` |
| identity/fingerprint/owner conflict | `AUTHORITY_CONFLICT` |

The detailed durable codes in section 20 are owner/verifier diagnostics and do not redesign P1-6 admission
outcomes.

## 12. Candidate transaction and orphan prevention

For `DurableContentRequirement.REQUIRED`, content object, candidate, and binding are written in the same
PostgreSQL transaction used to persist/evaluate the candidate admission request.

Exact order under the existing P1-6/WorkRun serialization boundary:

```text
1. lock current TaskContract/RequirementSet/Requirement authority
2. lock content identity and candidate identity in lexical order
3. verify AuthenticatedContentOwnerContextV1 and current pre-enrollment
4. canonicalize and validate body; compute hash/ref/payload fingerprint
5. insert or exact-replay DurableEvidenceContentObject
6. insert EvidenceCandidate
7. insert EvidenceCandidateDurableContentBinding
8. evaluate all existing P1-6 dimensions
9. persist evaluation and ADMITTED/REJECTED decision
10. if ADMITTED, persist AdmittedEvidence/mapping atomically as before
```

Failure before commit rolls back object, candidate, binding, decision, and mapping together. A committed durable
object is always reachable through at least one immutable candidate binding; no unbound/orphan row is legal.

A rejected candidate may retain its bounded non-secret content object because accepted P1-6 preserves candidate
and rejection provenance. It remains ineligible for `AdmittedEvidence`, set roots, `G_EVIDENCE`, P1-8 Cycle, or
ProjectMemory. Rejection provenance is not reusable memory.

Same identity/same payload is exact replay. Same identity/different payload fails with
`DURABLE_CONTENT_IDENTITY_CONFLICT` before candidate/admission mutation. No last-write-wins path exists.

## 13. Durable candidate binding

`EvidenceCandidateDurableContentBindingV1` contains:

```text
candidate_id / candidate_version / candidate_fingerprint
durable_content_ref / durable_content_payload_fingerprint
EvidenceContentRef canonical metadata fingerprint
requirement_ref / requirement_fingerprint_schema / requirement_fingerprint
requirement_set_ref / root
durable_content_policy_ref / fingerprint
bound_at
binding_fingerprint
```

The candidate's stored `EvidenceContentRef` must byte-for-byte match the durable object metadata projection.
One candidate has at most one durable binding. One durable object may be referenced by multiple new candidates
only when every candidate has its own exact pre-enrolled binding and normal P1-6 admission.

## 14. Historical resolver APIs

### 14.1 Metadata/integrity verifier

```text
verify_historical_content_ref(
  content_ref: EvidenceContentRef,
  expected_payload_fingerprint: sha256 | None
) -> VerifiedHistoricalContentMetadata
```

This owner-side projection-independent API verifies:

```text
serialized ref and identity key
owner identity/version and owner authority ref/fingerprint
object identity/version
allowed content kind and canonicalization
schema ID/version
byte count 1..65,536
content hash and algorithm
sensitivity, retention, access policy
content authority ID/version/revision
payload fingerprint
stored bytea presence
sha256(stored canonical bytes) == content hash
recanonicalize(parse(bytes)) == exact stored bytes
```

It does not load current WorkRun, current evidence effectiveness, current RequirementSet, current authority
revision, or P1-8 applicability.

### 14.2 Authorized body resolver

```text
resolve_historical_canonical_body(
  content_ref: EvidenceContentRef,
  access_grant: HistoricalContentAccessGrant
) -> VerifiedHistoricalContent
```

It first runs the metadata/integrity verifier, then validates the current consumer grant against sensitivity and
access policy. A current access denial is `DURABLE_CONTENT_ACCESS_DENIED`; it does not rewrite or declare the
historical object corrupt.

The API accepts no caller body, replacement body, expected semantic summary, free-form field path, or repair
flag. Its bytes come only from the verified PostgreSQL row.

### 14.3 Admission-plus-content opt-in

The existing P1-6 historical admission/attestation verifiers remain metadata/provenance-only by default and do
not automatically load sensitive bodies. Authorized consumers use:

```text
verify_historical_admitted_evidence_with_content(
  admitted_evidence_ref,
  exact_terminal_attestation_ref,
  consumer = P1_8_STRUCTURED_RESULT_V1,
  policy_fixed_json_pointer
) -> HistoricalAdmittedStructuredContentV1
```

It verifies the complete existing P1-6 issuance graph, exact admitted-ref/root membership, original Requirement
with persisted schema `P1_6_EVIDENCE_REQUIREMENT_FINGERPRINT_V2_DURABLE_CONTENT` and exact recomputed V2
fingerprint, `durable_content_requirement=REQUIRED`, candidate binding, durable object, access grant, and
policy-fixed field extraction. Current evidence effectiveness is explicitly not an input.

## 15. Historical integrity versus current effectiveness

Normative:

```text
historical durable content integrity
!= historical evidence admission validity
!= current evidence effectiveness
!= current P1-8 memory applicability
```

- Missing/corrupt body, metadata mismatch, or original binding/policy invalidity is historical corruption and
  fails closed.
- A later P1-6 `REVOKED`, `SUPERSEDED`, `CORRECTED`, expiry, state-version change, or current-set change does not
  alter content bytes/ref or original admission identity.
- P1-8 validates historical source identity first, then separately observes current evidence effectiveness to
  determine current ProjectMemory applicability under its accepted rules.
- Same historical replay returns the same content bytes/fingerprint despite ordinary later current staleness.

## 16. Restart and corruption contract

After process restart, a fresh P1-6 repository instance resolves the same ref entirely from PostgreSQL rows,
recomputes the identity/payload/body hashes, re-canonicalizes JSON, and returns byte-equivalent canonical bytes.
Empty `_objects`, a new `_owner_token`, or an empty process cache has no effect.

Fail closed on:

```text
content row or candidate binding missing
body NULL/empty
body over hard limit
identity/ref/payload fingerprint mismatch
body hash or byte count mismatch
metadata/EvidenceContentRef mismatch
unknown canonicalization/schema/kind
Requirement fingerprint schema unknown or version-shape mismatch
Requirement fingerprint does not match the exact version-selected canonical bytes
Requirement V2 capability not REQUIRED at original issuance
event/provenance ambiguity
sensitivity or access denial
```

No auto repair, caller resupply, hash-only recovery, or metadata-derived body is permitted.

## 17. Correction, revocation, and deletion

Body and metadata are immutable. Correction requires:

```text
new object_id or object_version
-> new DurableEvidenceContentObject
-> new EvidenceCandidate
-> new normal P1-6 admission
-> explicit existing P1-6 correction/supersession event when applicable
```

Existing evidence revocation/supersession events change current effectiveness only. They do not update/delete
the old body. Content rows and candidate bindings use append-only triggers and `ON DELETE RESTRICT` references.

V1 exposes no content mutation, automatic retention deletion, cascade delete, backfill update, or administrative
body replacement API.

## 18. Backward compatibility, verifier algorithm, and exact cut line

All P1-6 historical admissions issued before this extension remain valid under their exact accepted P1-6
contract. They are not historical corruption merely because they lack a durable body row.

### 18.1 Persisted immutable algorithm selection

The future historical verifier uses this exact order:

```text
load immutable EvidenceRequirementRow
read persisted immutable row.fingerprint_schema

switch row.fingerprint_schema:
  P1_6_EVIDENCE_REQUIREMENT_FINGERPRINT_V1:
    require the exact legacy V1 row payload key set
    reconstruct the exact V1 domain object without durable fields
    recompute exact V1 canonical bytes and fingerprint
    compare to the unchanged stored fingerprint
    expose durable capability view = NOT_APPLICABLE

  P1_6_EVIDENCE_REQUIREMENT_FINGERPRINT_V2_DURABLE_CONTENT:
    require the exact V2 row payload key set
    require physical selector == payload fingerprint_schema
    reconstruct exact V2 canonical fields
    recompute exact V2 canonical bytes and fingerprint
    compare to the stored fingerprint
    verify exact durable policy and candidate-binding relation

  otherwise:
    fail DURABLE_CONTENT_REQUIREMENT_SCHEMA_UNKNOWN
```

The verifier never normalizes V1 into V2, never hashes an in-memory default, and never chooses an algorithm from
current code, current policy, current migration state, field nullability, Requirement ref naming, or timestamps.
After every Requirement fingerprint is version-correctly verified, the unchanged RequirementSet algorithm
recomputes the root from the ordered exact stored/reverified fingerprints.

### 18.2 Legacy identity invariant

For every pre-extension lineage, upgrade must preserve exactly:

```text
EvidenceRequirement canonical V1 bytes and fingerprint
EvidenceRequirementRow JSONB payload shape and stored fingerprint
EvidenceRequirementSet ordered refs, root, payload and fingerprint
EvidenceAdmissionRequest ID, canonical request fingerprint and payload
EvidenceEvaluation ID/dimension payload and EvidenceAdmissionDecision identity
AdmittedEvidence identity and immutable mapping
EvidenceSetEvaluation ID, full/subset/admitted roots and payload
EvidenceSetSatisfactionAttestation ID/ref, roots and payload
P1-7 HumanResult provenance that consumed the exact P1-6 attestation
P1-7 Judgment provenance that consumed the exact P1-6 attestation/root
```

The newly materialized physical V1 selector is not part of any legacy canonical payload or fingerprint. It selects
the old algorithm only. Any attempt to synthesize `NOT_APPLICABLE` or null policy fields into V1 canonical bytes is
`DURABLE_CONTENT_REQUIREMENT_LEGACY_IDENTITY_CONFLICT`, not a migration or repair.

Legacy rule:

```text
persisted fingerprint schema = P1_6_EVIDENCE_REQUIREMENT_FINGERPRINT_V1
canonical durable fields = absent
semantic durable capability view = NOT_APPLICABLE
metadata-only/process-local content = no durable candidate binding
P1-6 historical admission validity = preserved
P1-7 historical Human/Judgment provenance = preserved
P1-8 STRUCTURED_RESULT_ATTESTED eligibility = false
error = P1_8_STRUCTURED_SOURCE_NOT_DURABLE
```

### 18.3 Prospective V2 cut line

```text
new Requirement ref/version
+ persisted schema P1_6_EVIDENCE_REQUIREMENT_FINGERPRINT_V2_DURABLE_CONTENT
+ exact V2 fingerprint with durable_content_requirement=REQUIRED
+ exact current policy enrolled by P1-6 before candidate creation
+ new RequirementSet version/root containing that exact V2 fingerprint
+ owner-authenticated durable object/candidate binding in the original transaction
+ normal P1-6 ADMITTED provenance
+ exact terminal-consumed attestation/root membership
= P1-8 structured source candidate
```

Changing an existing V1 Requirement, reusing its ref/version with V2 fields, or attaching an enrollment after
candidate/admission is forbidden. No legacy row backfill from caller bytes is permitted, even if supplied bytes
hash-match old metadata. Controlled re-ingestion requires a new TaskContract/Requirement V2 version, new set/root,
new owner-backed candidate, and new admission.

## 19. Exact P1-8 handoff

P1-8 may consume only:

```text
EvidenceContentRef
+ complete historical P1-6 admission provenance
+ exact original durable candidate binding
+ P1-6 historical content resolver result
```

P1-8 may then extract only a MemoryDeclarationAuthorityPolicy-fixed JSON Pointer, canonicalize that exact
field/object, recompute `MCF_V1`, and persist its own immutable Cycle/ProjectMemory projection.

P1-8 may not write the P1-6 store, submit replacement bytes, accept a bare content hash, select arbitrary JSON
paths, bypass access/sensitivity policy, or treat content availability as evidence/Judgment/Transition authority.

## 20. Typed failure vocabulary

| Code | Meaning |
|---|---|
| `DURABLE_CONTENT_REQUIRED` | original Requirement requires a durable object/binding but none is present |
| `DURABLE_CONTENT_KIND_NOT_SUPPORTED` | kind is outside the three-kind V1 allowlist |
| `DURABLE_CONTENT_TOO_LARGE` | raw/canonical bytes, depth, or node bounds exceed V1 |
| `DURABLE_CONTENT_SENSITIVITY_DENIED` | sensitivity is not `PUBLIC_SAFE` or `INTERNAL` |
| `DURABLE_CONTENT_IDENTITY_CONFLICT` | same owner/object identity has a different immutable payload |
| `DURABLE_CONTENT_MISSING` | referenced durable row or canonical body is absent |
| `DURABLE_CONTENT_INTEGRITY_MISMATCH` | ref/payload/body hash, byte count, owner, or binding differs |
| `DURABLE_CONTENT_SCHEMA_MISMATCH` | canonical JSON/schema/canonicalization differs from enrollment |
| `DURABLE_CONTENT_ACCESS_DENIED` | current consumer lacks permission to receive verified bytes |
| `DURABLE_CONTENT_REQUIREMENT_SCHEMA_UNKNOWN` | persisted Requirement fingerprint schema is absent after the cutover, unknown, or unsupported |
| `DURABLE_CONTENT_REQUIREMENT_FINGERPRINT_MISMATCH` | stored fingerprint differs from exact canonical bytes selected by the persisted schema |
| `DURABLE_CONTENT_REQUIREMENT_LEGACY_IDENTITY_CONFLICT` | legacy V1 is normalized, rewritten, or reconstructed with synthetic durable fields |
| `P1_8_STRUCTURED_SOURCE_NOT_DURABLE` | evidence is P1-6-valid but lacks original REQUIRED durable enrollment/binding |

`DURABLE_CONTENT_INTEGRITY_MISMATCH` is historical corruption. Ordinary evidence revocation/staleness uses
existing P1-6 current-effectiveness results and must not be recoded as content corruption.

## 21. PostgreSQL implementation direction

The future forward-only migration is expected to be:

```text
revision: 20260830_0005
down_revision: 20260829_0004
file: migrations/versions/20260830_0005_p1_6_durable_evidence_content.py
```

Logical table `evidence_content_objects`:

```text
serialized_ref varchar primary key
content_identity_key char(64) unique not null
owner_id / owner_version
source_owner_authority_ref / fingerprint
object_id / object_version
content_kind / canonicalization / schema_id / schema_version
byte_count integer check 1..65536
content_hash char(64)
sensitivity / retention_policy / access_policy
canonical_body bytea not null
created_at timestamptz
content_authority_id / version / revision
payload_fingerprint char(64)
unique(owner_id, owner_version, object_id, object_version)
check(octet_length(canonical_body) = byte_count)
```

Indexes: unique serialized/identity refs; owner/object unique identity; non-unique schema ID/version and content
hash for integrity investigation. No public body-search index exists.

Logical table `evidence_candidate_content_bindings`:

```text
candidate_id primary key references evidence_candidates on delete restrict
durable_content_ref references evidence_content_objects on delete restrict
requirement_ref / requirement_fingerprint_schema / requirement_fingerprint
requirement_set_ref / root
durable_content_policy_ref / fingerprint
binding_fingerprint
bound_at
```

One object may have many candidate bindings; one candidate has at most one.

The migration cut line for `evidence_requirements` is exact:

1. suspend new Requirement issuance while the schema change is installed;
2. add physical `fingerprint_schema varchar` with the one-time stored legacy value
   `P1_6_EVIDENCE_REQUIREMENT_FINGERPRINT_V1` for every already-existing row;
3. do not place that selector or any durable field into existing JSONB payloads and do not recompute any existing
   fingerprint;
4. remove the database default after legacy selector materialization, require every future insert to supply an
   explicit allowed schema, and extend append-only enforcement to the selector;
5. permit V1 inserts only with the exact legacy payload shape, and V2 inserts only with the exact extended payload
   shape and non-null `REQUIRED` policy binding;
6. reject an omitted/unknown selector after activation rather than guessing from null columns or current code.

The selector backfill is identity-neutral physical algorithm metadata. It neither changes nor participates in the
legacy Requirement canonical bytes/fingerprint. No migration operation may:

```text
UPDATE existing EvidenceRequirement JSONB payload
rewrite or recompute existing Requirement fingerprint
rewrite or recompute existing RequirementSet root or fingerprint
rewrite existing AdmissionRequest payload or request fingerprint
rewrite existing Evaluation/Decision/AdmittedEvidence identity or payload
rewrite existing EvidenceSetEvaluation identity/root/payload
rewrite existing EvidenceSetSatisfactionAttestation identity/ref/root/payload
```

`EvidenceRequirementSet` requires no new schema field. New V2 sets use the unchanged set row/payload algorithm over
their newly issued V2 member fingerprints. Existing rows are never interpreted as though new durable fields were
historically present.

Both new tables are append-only and reject UPDATE/DELETE. Candidate/object/binding transaction order and
deferrable behavior must be proven against PostgreSQL; no cascade is allowed.

## 22. Required implementation proof matrix

Future implementation must prove:

- pre-extension V1 fixture captured before upgrade with exact Requirement canonical bytes, Requirement row JSONB
  shape, stored fingerprint, RequirementSet row/root/fingerprint, AdmissionRequest row/fingerprint,
  Evaluation/Decision/AdmittedEvidence rows, set Evaluation/Attestation rows, and linked P1-7 provenance;
- after upgrade, that fixture's persisted V1 selector chooses the exact old serializer and every captured legacy
  Requirement/RequirementSet/AdmissionRequest/Evaluation/Attestation identity remains byte/hash-equal;
- mandatory P1-6 historical verifier regression: legacy admitted-evidence issuance graph and
  `verify_historical_set_attestation_provenance` both pass without durable fields or body binding;
- mandatory P1-7 historical regression: a legacy HumanResult flow and a legacy Judgment flow that consumed the
  fixture's P1-6 attestation/root both pass their projection-independent historical provenance verifiers;
- negative legacy normalization fixture: adding synthetic `NOT_APPLICABLE`/null durable fields changes the
  calculated shape and is rejected as `DURABLE_CONTENT_REQUIREMENT_LEGACY_IDENTITY_CONFLICT`, never persisted;
- legacy metadata-only structured evidence remains P1-6 historically valid and is denied P1-8
  `STRUCTURED_RESULT_ATTESTED` with `P1_8_STRUCTURED_SOURCE_NOT_DURABLE`;
- new V2 Requirement is issued before candidate creation with exact persisted schema/policy, produces a new
  fingerprint and new RequirementSet root, and cannot reuse or mutate a V1 ref/version;
- unknown schema, V1-with-extra-fields, V2-with-missing/extra/null fields, physical/payload schema mismatch, and
  schema-correct fingerprint mismatch all fail with the frozen typed diagnostics;
- fixed canonicalization vectors, Unicode normalization, duplicate keys, integer/float, depth/node and 65,536
  byte boundaries;
- exact allowlist and exclusion of Human/P1-5/prior/artifact kinds;
- `PUBLIC_SAFE`/`INTERNAL` positive, `PRIVATE_SENSITIVE`/`SECRET_FORBIDDEN` negative;
- owner-authenticated write and P1-8/caller direct-write denial;
- same identity replay and different-byte identity conflict under concurrency;
- object/candidate/binding/admission atomicity and zero orphans;
- fresh-process restart returns byte-identical bodies without `_owner_token`/`_objects`;
- tampered row/body/hash/schema/binding fails closed;
- later revocation changes current effectiveness without changing historical body identity;
- metadata-only historical verifier does not load bodies;
- authorized opt-in P1-8 historical resolver checks exact terminal-consumed admitted ref/root;
- private/public export boundaries and no secret persistence;
- P1-4/P1-6/P1-7 regression and unchanged `G_EVIDENCE` semantics.

The future implementation must materialize these as immutable pre-extension fixtures before executing the future
migration. At minimum the proof suite must contain dedicated PostgreSQL integration fixtures equivalent to:

```text
P1_6_V1_LEGACY_ADMISSION_AND_ATTESTATION
P1_7_V1_LEGACY_HUMAN_RESULT_FROM_P1_6_ATTESTATION
P1_7_V1_LEGACY_JUDGMENT_FROM_P1_6_ATTESTATION
P1_6_V2_DURABLE_REQUIREMENT_AND_SET
```

Hand-constructed post-upgrade objects are not substitutes for pre-extension serialized fixtures.

## 23. Required design examples

### 23.1 Positive restart reconstruction

```text
Requirement R2 has durable_content_requirement=REQUIRED before admission
-> registered System owner produces bounded canonical structured result
-> P1-6 writes object + candidate + binding in one transaction
-> normal P1-6 admission is ADMITTED and terminal attestation consumes its ref/root
-> process restarts with empty cache/new Python object identities
-> historical resolver reads bytea, recomputes ref/fingerprint/hash/canonicalization
-> exact same canonical bytes return to authorized P1-8 internal consumer
-> P1-8 extracts policy-fixed field and recomputes MCF_V1
```

### 23.2 Caller laundering negative

```text
old metadata-only AdmittedEvidence + caller-supplied bytes
-> original Requirement uses exact V1 schema (semantic durable view NOT_APPLICABLE) and no original candidate binding exists
-> P1_8_STRUCTURED_SOURCE_NOT_DURABLE
```

Hash equality does not change this result. The body did not come from original P1-6 owner-backed issuance.

### 23.3 Identity conflict

```text
same owner_id/version/object_id/version + different canonical bytes
-> DURABLE_CONTENT_IDENTITY_CONFLICT
-> no new object/candidate/admission mutation
```

### 23.4 Cache loss

```text
PrivateEvidenceContentStore._objects emptied and _owner_token replaced
-> eligible durable object still resolves from PostgreSQL
-> metadata-only object remains unavailable, without fabricated recovery
```

### 23.5 Sensitivity/export

```text
SECRET_FORBIDDEN -> no durable body row
PRIVATE_SENSITIVE -> not supported in V1 durable structured store
INTERNAL durable body -> authorized internal resolver only; public export denied
PUBLIC_SAFE -> body export still requires PUBLIC_SAFE_EXPORT + exact export policy/version
```

### 23.6 Legacy fingerprint/root replay across upgrade

```text
pre-extension Requirement row
  payload = exact accepted V1 key set
  fingerprint = F1

pre-extension RequirementSet
  ordered pair includes (R1@v1, F1)
  root = ROOT1

future migration
  persist physical fingerprint_schema = P1_6_EVIDENCE_REQUIREMENT_FINGERPRINT_V1
  do not alter Requirement payload/F1 or RequirementSet payload/ROOT1

post-upgrade historical replay
  stored selector chooses exact V1 serializer
  recomputed fingerprint = F1
  recomputed set root = ROOT1
  original AdmissionRequest/Evaluation/Attestation and P1-7 provenance verify unchanged
  durable capability view = NOT_APPLICABLE
  P1-8 structured-source eligibility = P1_8_STRUCTURED_SOURCE_NOT_DURABLE
```

### 23.7 Prospective V2 issuance

```text
TaskContract authority issues new R2@v2
  persisted schema = P1_6_EVIDENCE_REQUIREMENT_FINGERPRINT_V2_DURABLE_CONTENT
  durable requirement = REQUIRED
  exact policy ref/fingerprint included in V2 canonical bytes
-> new fingerprint F2
-> new RequirementSet version root commits to (R2@v2, F2)
-> durable object/candidate binding commits to schema/F2/root/policy before admission
-> normal P1-6 admission and exact terminal attestation/root consumption
```

## 24. Non-goals and boundary

Not designed or implemented here:

```text
general S3/object-store/provider
arbitrary artifact/blob/multimedia storage
RAG/vector/search
generic secrets vault
private Human content store
P1-8 runtime
P2/P3
Self-Dogfooding
deployment/Public Live
```

The existing process-local store may remain a test fixture, ephemeral cache, or non-durable evidence mode. It
must not advertise P1-8 structured reconstruction eligibility.

## 25. Human acceptance gate

Closed V1 proposal choices:

```text
store = PostgreSQL bytea
canonicalization = AISCC_CANONICAL_STRUCTURED_JSON_V1
hard canonical body cap = 65,536 bytes
eligible kinds = INLINE_CANONICAL_STRUCTURED_BODY | DATABASE_OBSERVATION_REF | RUNTIME_OBSERVATION_REF
sensitivity = PUBLIC_SAFE | INTERNAL only
PRIVATE_SENSITIVE = NOT_SUPPORTED_IN_DURABLE_STRUCTURED_STORE_V1
SECRET_FORBIDDEN = never stored
Requirement capability = REQUIRED | NOT_APPLICABLE
Requirement compatibility = explicit persisted V1/V2 fingerprint schema
legacy V1 canonical payload/fingerprint/root = exact unchanged; semantic NOT_APPLICABLE is not serialized
new durable-capable Requirement = V2 REQUIRED only, prospectively issued
RequirementSet/request/evaluation/attestation schemas = unchanged; they commit exact verified fingerprint/root
writer = P1-6 content owner only
retention = no automatic deletion in V1
legacy backfill = forbidden
P1-8 handoff = read-only owner API over exact historical admission + original durable binding
```

Open implementation-policy choice requiring Human acceptance of this design: none. Human may accept, require
rework, or reject the complete proposal.

Current status:

```text
P1-6 core: HUMAN_PROVIDED / ACCEPTED / CLOSED
P1-6 Durable Evidence Content Extension Design: REWORKED_DESIGN_CANDIDATE / HUMAN_PENDING
P1-8 Design: HUMAN_PROVIDED / ACCEPTED / CLOSED
P1-8 Runtime: BLOCKED_REQUIRED_EVIDENCE / IMPLEMENTATION_BASELINE_GAP
P2: NOT_STARTED
PUBLIC_BOUNDED_LIVE: NOT_RELEASED
```
