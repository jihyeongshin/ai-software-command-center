# 작업지시서: P1-6 Durable Content Requirement Fingerprint Compatibility Design Rework

## meta

- task_id: `20260830_2308_aiscc-p1-6-durable-content-requirement-fingerprint-compatibility-design-rework-1`
- created_at: `2026-08-30T23:08:00+09:00`
- phase: `P1-6 Durable Evidence Content Authority Extension Design`
- work_type: `DESIGN_REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1_6_EVIDENCE_CONTENT / P1_6_EVIDENCE_REQUIREMENT_COMPATIBILITY`
- expected_start_head: `b111f5f676e1a782de095e2f5b2a106d8b9a0207`
- predecessor_design_sha256: `fc30bcb3f21cd814166cc686ff69c417bfad25d5df8307ca14fadec0f96c4463`
- accepted_p1_6_design_sha256: `0d9d4c194efda37f100c6183d1a7e88e1a09fe073dc3a37bbb5a3e1cd577e463`
- accepted_p1_8_design_sha256: `100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a`
- p1_8_runtime_status: `BLOCKED_REQUIRED_EVIDENCE / IMPLEMENTATION_BASELINE_GAP`

---

# 1. purpose

Rework only the historical fingerprint/payload compatibility gap.

Preserve the predecessor design decisions:

```text
PostgreSQL bytea V1

65,536 byte hard ceiling

AISCC_CANONICAL_STRUCTURED_JSON_V1

allowed durable kinds:
INLINE_CANONICAL_STRUCTURED_BODY
DATABASE_OBSERVATION_REF
RUNTIME_OBSERVATION_REF

PUBLIC_SAFE / INTERNAL only

PRIVATE_SENSITIVE:
not durable V1

SECRET_FORBIDDEN:
never stored

P1-6-only writer

no automatic deletion

no legacy caller-byte backfill

projection-independent historical content resolver

P1-8 read-only handoff
```

Do not redesign those.

Place/preserve the Command Center HOLD Cycle:

```text
.aiassistant/records/aiscc/cycles/
20260830_2308_aiscc-p1-6-durable-content-requirement-fingerprint-backward-compatibility-hold-1.cycle.md
```

---

# 2. mandatory preflight

Require:

```text
HEAD ==
b111f5f676e1a782de095e2f5b2a106d8b9a0207

sha256(.aiassistant/rules/AISCC_DURABLE_EVIDENCE_CONTENT_AUTHORITY.md)
==
fc30bcb3f21cd814166cc686ff69c417bfad25d5df8307ca14fadec0f96c4463

sha256(.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md)
==
0d9d4c194efda37f100c6183d1a7e88e1a09fe073dc3a37bbb5a3e1cd577e463

sha256(.aiassistant/rules/AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md)
==
100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a
```

Mismatch:

```text
STOP
→ REVIEWED_DESIGN_DRIFT
```

No Git add/commit/push.

---

# 3. allowed mutation

Modify only:

```text
.aiassistant/rules/
AISCC_DURABLE_EVIDENCE_CONTENT_AUTHORITY.md
```

Task lifecycle:

```text
.aiassistant/tasks/active/
20260830_2308_aiscc-p1-6-durable-content-requirement-fingerprint-compatibility-design-rework-1.md

→

.aiassistant/tasks/done/
20260830_2308_aiscc-p1-6-durable-content-requirement-fingerprint-compatibility-design-rework-1.md
```

Temporary target only:

```text
.aiassistant/reports/target/
20260830_2308_aiscc-p1-6-durable-content-requirement-fingerprint-compatibility-design-rework-1/**
```

No runtime source/test/migration.

No canonical state update.

---

# 4. inspect exact existing fingerprint contracts

Read targeted current source for exact existing algorithms/row shapes:

```text
EvidenceRequirement model
requirement fingerprint function/constructor

EvidenceRequirementSet model
RequirementSet root/fingerprint function

EvidenceAdmissionRequest model/fingerprint

EvidenceSetEvaluation
EvidenceSetSatisfactionAttestation

PostgreSQL Requirement/RequirementSet row payload schemas

historical P1-6 verifier reconstruction logic
```

Report exact symbol/path inventory.

Do not assume adding dataclass/default fields preserves hashes.

---

# 5. freeze explicit Requirement fingerprint schema evolution

Select one exact backward-compatible design.

Preferred shape if compatible with current source:

```text
RequirementFingerprintSchema:

P1_6_REQUIREMENT_V1
→ exact existing pre-extension canonical serialization

P1_6_REQUIREMENT_V2_DURABLE_CONTENT
→ exact V1 fields
+ durable_content_requirement
+ durable_content_policy_ref
+ durable_content_policy_fingerprint
```

Exact names may differ.

Required:

```text
legacy persisted Requirement
→ historical verifier chooses V1 deterministically
→ exact old canonical bytes
→ exact old fingerprint

new durable-capable Requirement
→ explicit V2
→ exact new canonical bytes
→ V2 fingerprint
```

The selector must be immutable and non-heuristic.

Preferred discriminator:

```text
explicit fingerprint_schema / contract_schema_version
```

persisted in the immutable new Requirement payload.

If the existing canonical Requirement version field can safely serve this role, prove why it is unambiguous.

Forbidden:

```text
runtime code version
current migration revision
current field defaults
current policy version

→ historical fingerprint algorithm selection
```

Do not silently hash default `NOT_APPLICABLE` fields into legacy V1.

---

# 6. alternative companion-enrollment design

If modifying the core Requirement fingerprint/version contract would create unnecessary P1-6 compatibility risk,
you MAY instead select a separate immutable object equivalent to:

```text
DurableContentRequirementEnrollment
```

bound to:

```text
exact existing Requirement ref/fingerprint

exact RequirementSet ref/root

TaskContract

durable content capability/policy

issued_at

P1-6 content authority
```

In that design:

```text
existing Requirement fingerprint/root
→ unchanged for all versions

durable source eligibility/admission extension
→ proven by exact companion enrollment + candidate binding
```

But the extension must still define how the ordinary P1-6 admission path enforces REQUIRED durability for an
enrolled Requirement without allowing caller selection.

Choose **one** model. Do not leave both as implementation options.

---

# 7. RequirementSet root compatibility

Freeze exact algorithm.

If Requirement V1/V2 is selected:

```text
RequirementSet root
→ canonical ordered list of exact persisted requirement refs/fingerprints

legacy set
→ old fingerprints unchanged
→ root unchanged

new set
→ V2 requirement fingerprints where actually issued
```

No synthetic durable fields are inserted into a legacy Requirement representation.

If RequirementSet fingerprint/payload schema itself must evolve, define:

```text
RequirementSet V1
RequirementSet V2
```

and exact historical selector.

If it does not need to evolve, explicitly state that.

---

# 8. row/payload-shape compatibility

Freeze exact historical shapes.

At minimum:

```text
legacy EvidenceRequirement row/payload
→ old exact allowed/required keys
→ no durable fields required
→ no payload rewrite

new V2 EvidenceRequirement row/payload
→ explicit schema/version
→ durable fields exact

legacy RequirementSet row/payload
→ unchanged

new RequirementSet row/payload
→ exact selected shape
```

In-memory model defaults may exist for developer ergonomics but:

```text
default value
!= historical serialized field
```

Historical verifier must validate the version-appropriate exact payload shape.

No broad “accept missing fields” parser that weakens corruption detection.

---

# 9. AdmissionRequest / Evaluation / Attestation compatibility

Determine exactly whether durable capability needs to alter these immutable identities.

Prefer minimum duplication.

If existing objects already bind:

```text
Requirement fingerprint
RequirementSet root
checkpoint fingerprint
candidate fingerprint/content ref
```

and this is sufficient, preserve their existing fingerprint schema.

If a durable-content ref/policy/binding must be added to an immutable request/evaluation/attestation payload:

```text
explicit V1/V2 schema evolution
```

is mandatory.

Freeze:

```text
legacy request/evaluation/attestation historical IDs/fingerprints unchanged

new schema selects new fields deterministically
```

No current-code defaults may change old identities.

---

# 10. migration cut line

The future migration must be forward-only and identity preserving.

Required:

```text
no UPDATE of existing immutable Requirement payload JSON

no recomputation of existing Requirement fingerprint

no recomputation of existing RequirementSet root/fingerprint

no rewrite of existing AdmissionRequest/Evaluation/Attestation immutable payload

no rewrite of AdmittedEvidence/Candidate historical identity
```

New physical columns may use nullable/default query values only if historical identity reconstruction continues
to use the original schema.

Freeze exact rule for rows created:

```text
before extension activation
after extension activation
```

Do not use migration timestamp alone as historical authority unless exact persisted contract version is also
bound.

---

# 11. historical P1-6 verifier contract

The future verifier must be able to reconstruct both eras.

Required pseudocode equivalent:

```text
load immutable requirement row

switch exact persisted requirement fingerprint schema:
  V1:
    validate exact V1 payload shape
    recompute exact V1 fingerprint
  V2_DURABLE:
    validate exact V2 payload shape
    recompute exact V2 fingerprint
    validate durable policy/enrollment relation
  otherwise:
    fail closed
```

Then:

```text
recompute exact RequirementSet root from the already-verified requirement fingerprints
```

Historical verifier must never normalize a V1 object into a V2 object before fingerprint comparison.

---

# 12. exact legacy compatibility proofs for future implementation

Freeze mandatory fixtures/tests created from pre-extension V1 bytes.

At minimum persist exact old fixtures before migration and, after upgrade, prove:

```text
legacy Requirement payload bytes/shape
→ unchanged

legacy Requirement fingerprint
→ exact unchanged

legacy RequirementSet root
→ exact unchanged

legacy AdmissionRequest ID/fingerprint
→ exact unchanged

legacy EvidenceSetEvaluation ID/root
→ exact unchanged

legacy EvidenceSetSatisfactionAttestation
→ verifies

legacy AdmittedEvidence historical provenance
→ verifies

legacy P1-7 HumanResult historical provenance
→ verifies where Human flow used

legacy P1-7 Judgment historical provenance
→ verifies where Judgment consumed P1-6 evidence
```

Also prove:

```text
legacy metadata-only structured evidence
→ P1-6 historical validity PASS
→ P1-8_STRUCTURED_RESULT_ATTESTED eligibility DENY
```

---

# 13. exact V2 proofs

Future implementation must prove:

```text
new durable capability/policy is immutable and enrolled before candidate creation

same logical Requirement old version
→ cannot be mutated to REQUIRED

new version/capability
→ new exact fingerprint/enrollment identity

new RequirementSet
→ root commits to the exact durable-capable requirement identity

required durable object/binding missing
→ normal accepted P1-6 rejection vocabulary

valid durable object/binding
→ normal P1-6 admission path

historical resolver after restart
→ exact same content bytes
```

---

# 14. accepted semantics preserved

Do not change:

```text
five accepted P1-6 evidence profiles

EvidenceCandidate != AdmittedEvidence

G_EVIDENCE owner/semantics

P1-6 current vs historical evidence authority

P1-7 historical evidence/Human/Judgment provenance

P1-8 historical/current memory semantics
```

This extension can add a versioned durable-content capability for new evidence, but it must not reinterpret an
already-issued V1 Requirement or old P1-6 admission.

---

# 15. typed failure additions

Add/freeze exact equivalents if needed:

```text
DURABLE_CONTENT_REQUIREMENT_SCHEMA_UNKNOWN
DURABLE_CONTENT_REQUIREMENT_FINGERPRINT_MISMATCH
DURABLE_CONTENT_REQUIREMENT_LEGACY_IDENTITY_CONFLICT
```

Do not map ordinary legacy `NOT_APPLICABLE` to corruption.

---

# 16. forbidden

No:

```text
src/**
tests/**
migrations/**

changes to AISCC_EVIDENCE_ADMISSION.md
changes to AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md

P1-8 runtime

Git add/commit/push

provider/network/deployment
```

Do not amend:

```text
c108e9c02f222cf51ce833e311465584447b3571
b111f5f676e1a782de095e2f5b2a106d8b9a0207
```

---

# 17. evidence contract

## executor_required

```text
DESIGN_EXISTING_REQUIREMENT_FINGERPRINT_AUDIT

DESIGN_REQUIREMENT_SCHEMA_EVOLUTION

DESIGN_REQUIREMENT_SET_ROOT_COMPATIBILITY

DESIGN_ROW_PAYLOAD_COMPATIBILITY

DESIGN_ADMISSION_REQUEST_COMPATIBILITY

DESIGN_MIGRATION_IDENTITY_CUT_LINE

DESIGN_HISTORICAL_VERIFIER_DUAL_VERSION

DESIGN_LEGACY_REGRESSION_FIXTURES

STATIC_GOVERNANCE
```

## human_owned

```text
P1-6 durable evidence-content extension design final review
→ HUMAN_PENDING
```

---

# 18. mandatory stop

STOP on:

```text
HEAD drift

predecessor design SHA drift

exact old Requirement fingerprint cannot be reconstructed

existing durable schema has no unambiguous way to distinguish historical fingerprint contract and a safe explicit
version cannot be introduced prospectively without rewriting old identity

P1-6 core admission truth semantics would need retroactive reinterpretation

unrelated dirty collision
```

Report:

```text
POLICY_BASELINE_GAP
```

or:

```text
POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

Do not guess.

---

# 19. accept criteria

All must hold:

```text
one exact compatibility model selected

legacy Requirement canonical bytes/fingerprint remain exact

legacy RequirementSet root remains exact

legacy request/evaluation/attestation identities remain exact

new durable-capable identity is explicitly versioned or companion-enrolled

historical verifier selects identity algorithm from immutable persisted authority

no current default/current code version used as historical discriminator

future migration does not rewrite historical identities

legacy P1-6/P1-7 historical provenance regression contract explicit

legacy evidence remains P1-8 durable-source ineligible

all predecessor store/size/privacy/owner/restart decisions preserved

runtime remains NOT_STARTED

Human verification = HUMAN_PENDING
```

---

# 20. export

Target:

```text
.aiassistant/reports/target/
20260830_2308_aiscc-p1-6-durable-content-requirement-fingerprint-compatibility-design-rework-1/
```

Required:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
```

Include byte-preserving:

```text
.aiassistant/rules/AISCC_DURABLE_EVIDENCE_CONTENT_AUTHORITY.md

.aiassistant/records/aiscc/cycles/
20260830_2308_aiscc-p1-6-durable-content-requirement-fingerprint-backward-compatibility-hold-1.cycle.md

.aiassistant/tasks/done/
20260830_2308_aiscc-p1-6-durable-content-requirement-fingerprint-compatibility-design-rework-1.md
```

---

# 21. expected submission state

```text
P1-6 core:
ACCEPTED / CLOSED

P1-6 Durable Evidence Content Extension Design:
REWORKED_DESIGN_CANDIDATE / HUMAN_PENDING

P1-8 Design:
ACCEPTED / CLOSED

P1-8 Runtime:
BLOCKED_REQUIRED_EVIDENCE / IMPLEMENTATION_BASELINE_GAP

P2:
NOT_STARTED
```

Command Center next:

```text
review compatibility-reworked design
→ PASS / HUMAN_FINAL_REVIEW_REQUIRED
or
→ HOLD_REWORK_REQUIRED
```

---

# 22. preserved exact paths

Preserve:

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

.aiassistant/tasks/done/
20260830_2308_aiscc-p1-6-durable-content-requirement-fingerprint-compatibility-design-rework-1.md
```
