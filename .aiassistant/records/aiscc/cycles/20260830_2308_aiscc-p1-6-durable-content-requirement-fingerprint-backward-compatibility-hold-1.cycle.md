# AISCC Cycle Record

## meta

- cycle_id: `20260830_2308_aiscc-p1-6-durable-content-requirement-fingerprint-backward-compatibility-hold-1`
- date: `2026-08-30T23:08:00+09:00`
- phase: `P1-6 Durable Evidence Content Authority Extension Design`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1_6_EVIDENCE_CONTENT / P1_6_EVIDENCE_REQUIREMENT_COMPATIBILITY`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause: `LEGACY_REQUIREMENT_FINGERPRINT_AND_ROOT_COMPATIBILITY_UNDER_SPECIFIED`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260830_2308_aiscc-p1-6-durable-content-requirement-fingerprint-backward-compatibility-hold-1.cycle.md`

## reviewed submission

```text
start/final HEAD:
b111f5f676e1a782de095e2f5b2a106d8b9a0207

accepted P1-6 design SHA:
0d9d4c194efda37f100c6183d1a7e88e1a09fe073dc3a37bbb5a3e1cd577e463

accepted P1-8 design SHA:
100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a

durable-content design candidate SHA:
fc30bcb3f21cd814166cc686ff69c417bfad25d5df8307ca14fadec0f96c4463

runtime implementation:
NOT_STARTED

Git actions:
none
```

Export identity independently verified:

```text
design:
fc30bcb3f21cd814166cc686ff69c417bfad25d5df8307ca14fadec0f96c4463

P1-8 baseline-gap HOLD Cycle:
3dda1f84057884960d54b738dd6610554a4964017139bb156c5a87433e137921

done Task:
3b67947dfb4c2d9ab403d7dead5c36e8a1a247b7a69730e2dedab60e0e4201b2

EXECUTOR_REPORT:
3c25e7651d26bfd8e3588cf56add305017c37f5aecd7a5a72198d612aba92dd3
```

## accepted design strengths

The candidate correctly freezes:

```text
bounded V1 store:
PostgreSQL bytea

hard canonical-body ceiling:
65,536 bytes

canonical structured JSON:
integer-only numeric model
NFC
duplicate-key rejection
depth 32
4,096 nodes

durable kinds:
INLINE_CANONICAL_STRUCTURED_BODY
DATABASE_OBSERVATION_REF
RUNTIME_OBSERVATION_REF

HUMAN_STRUCTURED_REF:
not durable in V1

PUBLIC_SAFE / INTERNAL:
supported

PRIVATE_SENSITIVE:
not durable in V1

SECRET_FORBIDDEN:
never stored

owner write:
P1-6 only

P1-8:
read-only authorized historical consumer

retention:
no automatic deletion in V1

legacy metadata-only evidence:
P1-6 historical validity preserved
P1-8 structured-source eligibility denied

caller-byte backfill:
forbidden

restart:
PostgreSQL reconstructs exact canonical bytes

historical content integrity
!= current evidence effectiveness
```

These decisions should be preserved.

---

# load-bearing finding — new Requirement fields can invalidate accepted historical P1-6 fingerprints unless fingerprint/schema evolution is exact

The candidate defines:

```text
Every newly issued EvidenceRequirement version adds:

durable_content_requirement:
REQUIRED | NOT_APPLICABLE

durable_content_policy_ref
durable_content_policy_fingerprint
```

and then states:

```text
These fields enter Requirement fingerprint,
RequirementSet root,
candidate request binding,
evaluation authority,
and historical admission reconstruction.
```

It also states:

```text
Legacy Requirement versions are exactly NOT_APPLICABLE.
```

That semantic default is insufficient to preserve historical identity.

Accepted P1-6 historical provenance already reconstructs and verifies:

```text
EvidenceRequirement immutable payload/fingerprint
EvidenceRequirementSet ordered requirement root
EvidenceSetEvaluation
EvidenceSetSatisfactionAttestation
historical admitted-evidence/request relationships
```

If the implementation reconstructs an old Requirement as:

```text
old fields
+ durable_content_requirement = NOT_APPLICABLE
+ null durable policy fields
```

and hashes that **new shape**, the result is not necessarily the same fingerprint that was durably stored before
this extension.

That can cascade into:

```text
legacy Requirement fingerprint mismatch

→ RequirementSet root mismatch

→ historical EvidenceSet attestation provenance mismatch

→ P1-6 accepted historical evidence appears corrupt

→ P1-7 historical Human/Judgment provenance may fail

→ P1-8 terminal accepted predecessor provenance may fail
```

Required invariant:

```text
legacy semantic default
!= permission to change legacy canonical bytes/fingerprint
```

---

# required compatibility design

The extension must freeze an explicit versioned immutable fingerprint/payload contract.

At minimum distinguish:

```text
P1_6_EVIDENCE_REQUIREMENT_FINGERPRINT_V1
→ exact pre-extension canonical field set
→ old persisted Requirement rows only

P1_6_EVIDENCE_REQUIREMENT_FINGERPRINT_V2_DURABLE_CONTENT
→ V1 fields
+ durable_content_requirement
+ durable_content_policy_ref
+ durable_content_policy_fingerprint
→ newly issued durable-capable Requirement versions only
```

Exact names may differ.

The design must define how historical reconstruction selects the algorithm without guessing from current code.

Valid discriminator examples:

```text
explicit requirement fingerprint schema/version persisted in immutable payload

or

explicit Requirement contract/schema version that already exists and is durable

or

a separate immutable DurableContentRequirementEnrollment object that avoids changing the core Requirement
fingerprint entirely
```

Do not infer:

```text
row has null new columns
→ therefore V1
```

unless this inference itself is proven unambiguous and frozen as an immutable schema cut-line.

Preferred: explicit versioned identity.

---

# RequirementSet root compatibility

Freeze exact rule:

```text
legacy RequirementSet root
→ recomputed from each exact legacy stored requirement fingerprint

new RequirementSet containing durable-capable Requirement versions
→ recomputed from those exact V2 fingerprints
```

Do not add a synthetic `NOT_APPLICABLE` durable field to the canonical representation of a legacy Requirement.

Existing RequirementSet rows/payload/root must remain byte/fingerprint compatible and must not be rewritten.

If RequirementSet itself has a fingerprint-schema version that must evolve, define the same explicit V1/V2
historical reconstruction rule.

---

# historical row/payload-shape compatibility

Current historical P1-6 verifiers perform exact durable row/payload validation.

The design must freeze:

```text
legacy Requirement row JSON/payload shape
→ remains exact legacy shape
→ no newly-required durable fields

new durable-capable Requirement row shape
→ explicit extension schema/version
→ durable fields mandatory according to that schema
```

Likewise any immutable:

```text
RequirementSet payload
AdmissionRequest payload
Evaluation payload
Attestation payload
```

that gains new durable-content fields must be versioned or must preserve its old exact shape.

A parser/model default value may be convenient in memory, but:

```text
in-memory default
!= canonical historical serialized field
```

---

# admission-request compatibility

The design says durable fields enter:

```text
candidate request binding
evaluation authority
historical admission reconstruction
```

Freeze whether the existing `EvidenceAdmissionRequest` fingerprint changes.

If the durable capability is already fully committed through:

```text
exact Requirement fingerprint
RequirementSet root
checkpoint fingerprint
candidate durable binding
```

then prefer not to add redundant request fingerprint fields.

If request/evaluation payload/fingerprint must change:

```text
explicit request/evaluation schema version
+ exact legacy reconstruction
```

is mandatory.

No existing historical request/evaluation ID/fingerprint may change.

---

# migration compatibility

The proposed additive migration must NOT rewrite immutable historical JSON payloads or fingerprints.

Exact requirements:

```text
existing Requirement rows:
no immutable payload rewrite
no fingerprint rewrite

existing RequirementSet rows:
no root/fingerprint rewrite

existing AdmissionRequest/Evaluation/Attestation rows:
no payload/fingerprint rewrite
```

New nullable columns/defaults used for query convenience must not be interpreted as if they were present in the
old canonical payload.

Backfill is allowed only for non-authoritative derived/query columns if:

```text
it does not change historical identity
and historical verifier still reconstructs the original canonical version
```

No migration-time recomputation of accepted P1-6 roots.

---

# required regression proof contract

Future implementation must include pre-extension fixtures/rows created with the exact old V1 serializer and prove
after migration/runtime upgrade:

```text
legacy Requirement fingerprint
→ exact unchanged

legacy RequirementSet root
→ exact unchanged

legacy EvidenceAdmissionRequest identity/fingerprint
→ exact unchanged

legacy EvidenceSetEvaluation/Attestation historical verification
→ PASS

legacy P1-6 historical admitted-evidence provenance
→ PASS

legacy P1-7 historical HumanResult/Judgment provenance
→ PASS where applicable

legacy evidence:
still not P1-8 durable structured-source eligible
```

Also prove new V2:

```text
durable capability/policy change
→ new Requirement version/fingerprint

new RequirementSet root
→ commits to new Requirement fingerprint

new durable binding
→ required before admission where V2 says REQUIRED
```

---

# command-center judgment

```text
P1-6 core:
ACCEPTED / CLOSED

P1-6 Durable Evidence Content Extension Design:
HOLD_REWORK_REQUIRED / HUMAN_PENDING

P1-8 Design:
ACCEPTED / CLOSED

P1-8 Runtime:
BLOCKED_REQUIRED_EVIDENCE / IMPLEMENTATION_BASELINE_GAP

P2:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

No implementation is authorized.

The store/size/privacy/owner/restart choices do not need redesign. Rework only the versioned historical
Requirement/RequirementSet/request compatibility contract.

## preserved exact paths

```text
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md

.aiassistant/rules/AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md

.aiassistant/rules/AISCC_DURABLE_EVIDENCE_CONTENT_AUTHORITY.md

.aiassistant/records/aiscc/cycles/
20260830_2130_aiscc-p1-8-runtime-durable-evidence-content-baseline-gap-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260830_2308_aiscc-p1-6-durable-content-requirement-fingerprint-backward-compatibility-hold-1.cycle.md

.aiassistant/tasks/done/
20260830_2130_aiscc-p1-6-durable-evidence-content-authority-baseline-design-1.md
```
