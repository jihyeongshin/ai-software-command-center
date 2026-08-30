# 작업지시서: P1-6 Durable Evidence Content Authority Baseline Design

## meta

- task_id: `20260830_2130_aiscc-p1-6-durable-evidence-content-authority-baseline-design-1`
- created_at: `2026-08-30T21:30:00+09:00`
- phase: `P1-6 Evidence Admission / P1-8 Prerequisite Extension`
- work_type: `DESIGN_BASELINE_EXTENSION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1_6_EVIDENCE_CONTENT`
- expected_start_head: `b111f5f676e1a782de095e2f5b2a106d8b9a0207`
- p1_6_core_status: `HUMAN_PROVIDED / ACCEPTED / CLOSED`
- p1_8_design_status: `HUMAN_PROVIDED / ACCEPTED / CLOSED`
- p1_8_runtime_status: `BLOCKED_REQUIRED_EVIDENCE / IMPLEMENTATION_BASELINE_GAP`
- accepted_p1_8_design_commit: `c108e9c02f222cf51ce833e311465584447b3571`
- accepted_p1_8_design_sha256: `100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a`
- p2_status: `NOT_STARTED`
- public_bounded_live: `NOT_RELEASED`

---

# 1. purpose

Design a narrow P1-6 extension that makes owner-backed canonical structured evidence content durably
reconstructable after process restart so that the Human-accepted P1-8
`STRUCTURED_RESULT_ATTESTED` contract can be implemented without caller-content laundering.

This Task is DESIGN ONLY.

Do not implement runtime source, migration, tests, object storage, or P1-8 runtime.

The accepted P1-6 core admission semantics remain closed.

---

# 2. mandatory preflight

Require:

```text
HEAD ==
b111f5f676e1a782de095e2f5b2a106d8b9a0207
```

Require:

```text
sha256(.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md)
==
0d9d4c194efda37f100c6183d1a7e88e1a09fe073dc3a37bbb5a3e1cd577e463
```

Require:

```text
sha256(.aiassistant/rules/AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md)
==
100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a
```

Place/preserve the Command Center HOLD Cycle:

```text
.aiassistant/records/aiscc/cycles/
20260830_2130_aiscc-p1-8-runtime-durable-evidence-content-baseline-gap-hold-1.cycle.md
```

Mismatch:

```text
STOP
→ REVIEWED_BASELINE_DRIFT
```

Record:

```text
git status --short
git diff --name-only
git diff --cached --name-only
```

Index must be empty.

No Git add/commit/push.

---

# 3. authoritative context

Read exact canonical owners:

```text
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md
.aiassistant/rules/AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md

.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_HUMAN_GATE_JUDGMENT.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

Read targeted current source only:

```text
src/aiscc/evidence/content.py
src/aiscc/evidence/models.py
src/aiscc/evidence/ports.py
src/aiscc/evidence/service.py
src/aiscc/evidence/repository.py

src/aiscc/persistence/models.py
src/aiscc/persistence/repository.py

migrations/versions/20260829_0004_p1_7_human_gate_judgment.py
```

and any exact P1-6 migration/source symbol needed to establish current schema.

Do not bulk-read unrelated packages.

---

# 4. baseline fact to preserve

Accepted P1-6 already separates:

```text
content body/ref authority
!= EvidenceCandidate
!= EvidenceAdmissionDecision
!= AdmittedEvidence
!= EvidenceSetSatisfactionAttestation
```

It also freezes:

```text
hash string without owner-backed body/ref
→ insufficient for admission

CONTENT_MISSING
→ fail closed

SECRET_FORBIDDEN
→ raw body never admitted

private body
→ not public/export authority
```

Do not weaken any of these.

P1-8 additionally requires an exact historical source-content reconstruction path.

---

# 5. design target artifact

Create a new canonical design extension:

```text
.aiassistant/rules/
AISCC_DURABLE_EVIDENCE_CONTENT_AUTHORITY.md
```

Do not rewrite `.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md` during this design Task.

The extension must explicitly state:

```text
it supplements P1-6 content persistence only

it does not supersede:
EvidenceRequirement
EvidenceCandidate
Evidence admission dimensions
AdmittedEvidence
EvidenceSet attestation
G_EVIDENCE
P1-7/P1-8 authority
```

Human final review is required before implementation.

---

# 6. choose one exact V1 durable content model

The design must select one exact bounded V1 storage model.

Preferred competition-safe direction to evaluate first:

```text
PostgreSQL durable canonical structured bytes
```

for bounded non-secret structured evidence only.

Do NOT introduce S3/object-store/provider dependencies unless PostgreSQL cannot satisfy the exact accepted
requirements.

If PostgreSQL is selected, freeze an exact object equivalent to:

```text
DurableEvidenceContentObject
```

with immutable fields at minimum:

```text
owner_id
owner_version

object_id
object_version

content_kind
canonicalization
schema_id
schema_version

byte_count
content_hash

sensitivity
retention_policy
access_policy

canonical_body_bytes

created_at

content_authority_id
content_authority_version

immutable payload fingerprint
```

Exact names may differ.

Define the stable serialized ref/version contract.

---

# 7. V1 eligible content kinds

Do not automatically durably copy every evidence body.

Freeze exact allowed kinds.

At minimum evaluate the structured kinds currently supported by P1-6:

```text
INLINE_CANONICAL_STRUCTURED_BODY
DATABASE_OBSERVATION_REF
RUNTIME_OBSERVATION_REF
HUMAN_STRUCTURED_REF
```

Decide which are eligible for durable canonical-body storage.

For each exact kind freeze:

```text
canonicalization
schema requirement
maximum bytes
sensitivity ceiling
retention class
downstream structured-field access allowed?
```

Keep these outside the new body store unless separately justified:

```text
P1_5_IMMUTABLE_PRODUCER_REF
PRIOR_ADMITTED_EVIDENCE_REF
arbitrary large CONTENT_ADDRESSED_ARTIFACT_REF
```

Those already have owner/ref semantics and must not be silently duplicated.

---

# 8. exact size and bounded-resource contract

Freeze exact V1 maximum canonical body size.

The design must choose a concrete hard limit.

Requirements:

```text
checked before durable write

checked after canonicalization

no streaming/large blob path in V1

oversize
→ typed rejection / non-durable-content-ineligible result
```

The limit must be sufficient for P1-8 structured `DECISION` / `NEXT_ACTION_CONTEXT` results but bounded enough
for competition PostgreSQL.

Do not leave the limit “configurable” without a Human-accepted default/max ceiling.

---

# 9. sensitivity/privacy contract

Freeze exact behavior for:

```text
PUBLIC_SAFE
INTERNAL
PRIVATE_SENSITIVE
SECRET_FORBIDDEN
```

Non-negotiable:

```text
SECRET_FORBIDDEN
→ never stored

durable content availability
!= public export permission

Run/replay visibility
!= private-content read authority
```

For `PRIVATE_SENSITIVE`, make an explicit V1 decision:

```text
SUPPORTED_DURABLY
or
NOT_SUPPORTED_IN_DURABLE_STRUCTURED_STORE
```

If supported, define exact access-control/retention/encryption assumptions compatible with current competition
runtime.

P1-8 memory cannot broaden the sensitivity/export ceiling.

---

# 10. owner-backed write boundary

Durable bytes must be written only by the P1-6 content owner.

Required path:

```text
owner-backed canonical source
→ P1-6 canonicalization
→ P1-6 durable content write
→ EvidenceContentRef
```

Forbidden:

```text
caller raw bytes
→ historical P1-8 verification source

P1-8 direct write into P1-6 content store

hash-only metadata
→ fabricate durable body
```

Define exact issuer/content-owner authentication used by the runtime.

A process-local `_owner_token` may remain an internal capability for in-process mutation control, but durable
historical authority cannot depend on Python object identity.

---

# 11. transaction and lifecycle

Freeze when durable content is created relative to EvidenceCandidate/admission.

At minimum decide:

```text
content write before candidate persistence
or
same transaction as candidate creation
```

and define orphan handling.

Required invariants:

```text
candidate content ref
→ exact durable content object

same object ID/version + same bytes
→ idempotent

same object ID/version + different bytes
→ identity conflict

ADMITTED evidence may reference only a valid durable body/ref when its requirement requires downstream durable
structured reconstruction
```

Do not allow partially committed metadata that points to uncommitted content.

---

# 12. Requirement-level durable-content eligibility

Not every evidence requirement needs durable bytes.

Freeze an exact immutable Requirement or EvidenceType capability equivalent to:

```text
durable_content_requirement:
REQUIRED
OPTIONAL
NOT_APPLICABLE
```

or a stricter exact alternative.

P1-8 `STRUCTURED_RESULT_ATTESTED` source eligibility must require:

```text
durable canonical structured content capability
```

to have been enrolled **before** the evidence was admitted/consumed.

P1-8 cannot retroactively make an old hash/ref body durable after terminal acceptance.

This prevents:

```text
accepted old metadata-only evidence
→ caller later supplies bytes
→ memory authority
```

---

# 13. historical resolver API

Design an owner-side projection-independent API equivalent to:

```text
verify_historical_content_ref(...)
resolve_historical_canonical_body(...)
```

It must verify/reconstruct:

```text
serialized content ref
owner identity/version
object identity/version
content kind
canonicalization
schema ID/version
byte count
content hash
sensitivity
retention/access policy
durable object fingerprint
exact canonical bytes
```

Then:

```text
sha256(canonical bytes)
== EvidenceContentRef.content_hash
```

The API must not require:

```text
current WorkRun
current evidence effectiveness
current RequirementSet
current authority revision
```

Historical content integrity:

```text
!= current evidence effectiveness
```

---

# 14. relation to P1-6 historical admission verifier

Do not make all P1-6 historical admission verification always load potentially sensitive bytes.

Preserve a metadata/provenance-only default verifier.

Define an explicit opt-in extension for authorized consumers:

```text
historical admission provenance
+ exact content resolution
```

P1-8 `STRUCTURED_RESULT_ATTESTED` is one such authorized internal consumer.

The API must fail closed on:

```text
content row missing
body missing
hash mismatch
metadata/ref mismatch
schema/canonicalization mismatch
sensitivity/access denial
```

---

# 15. restart contract

Freeze:

```text
process restart
→ exact durable content ref resolves to the same canonical bytes

process-local content cache loss
→ no authority loss for eligible durable content

PostgreSQL rows/events
→ authoritative reconstruction
```

The current `PrivateEvidenceContentStore._objects` may remain:

```text
test fixture
ephemeral cache
non-durable content mode
```

but must not be the only authority for evidence enrolled as P1-8 reconstructable structured content.

---

# 16. correction / revocation / deletion

Content object identity is immutable.

Do not update body bytes in place.

Correction:

```text
new object_id/version or new candidate/content ref
→ new admission
```

Evidence revocation/supersession:

```text
does not mutate/delete old body identity
```

Retention deletion, if supported at all in V1, must not make a historical object silently appear valid.

Decide exact behavior:

```text
retained body required for downstream P1-8 historical replay

retention expiry before required project-memory provenance lifetime
→ forbidden
```

Recommended competition V1:

```text
no automatic deletion of enrolled durable structured content before project/competition retention boundary
```

Freeze an exact owner/policy.

---

# 17. public export boundary

Public/review export uses:

```text
metadata/hash/ref
```

by default.

Exact body export only if:

```text
PUBLIC_SAFE
+ access_policy explicitly permits
+ export policy/version explicitly permits
```

P1-8 public projection cannot read/export private content merely because memory derives from it.

Private structured content may produce a separately sanitized derivative only through a new owner-backed
candidate/admission.

---

# 18. schema/migration direction

Design only; do not create migration.

But freeze enough implementation shape to permit one forward-only migration.

Expected equivalent table:

```text
evidence_content_objects
```

Define:

```text
primary key / unique immutable identity

bytea canonical body

metadata columns vs JSONB payload

indexes

FK relation, if any, to candidates

delete behavior:
RESTRICT / no cascade for immutable provenance
```

Do not design destructive modification of existing admitted-evidence rows.

Existing historical metadata-only P1-6 evidence remains valid historical admission provenance.

It simply may be:

```text
NOT_ELIGIBLE_AS_P1_8_STRUCTURED_RESULT_SOURCE
```

unless it was already backed by an independently durable owner content source.

---

# 19. backward compatibility / cut line

Freeze a clear cut line.

Required:

```text
P1-6 historical admissions before durable-content extension
→ remain valid P1-6 historical evidence

but

metadata-only/process-local structured content
→ not automatically P1-8 STRUCTURED_RESULT_ATTESTED eligible
```

After the extension:

```text
Requirement/EvidenceType enrolled for durable structured content
+ owner-backed durable content object
+ normal P1-6 ADMITTED provenance
→ P1-8 eligible source candidate
```

No backfill from untrusted caller bytes.

If controlled re-ingestion/backfill is needed later:

```text
new TaskContract/new candidate/new admission
```

only.

---

# 20. P1-8 integration contract

Freeze the exact handoff P1-8 may consume:

```text
EvidenceContentRef
+ complete historical P1-6 admission provenance
+ durable historical content resolver
```

P1-8 may then:

```text
resolve exact canonical source bytes
extract policy-fixed field/object
recompute MCF_V1
persist its own immutable Cycle/ProjectMemory projection
```

P1-8 may not:

```text
write P1-6 content
replace missing source bytes
trust caller bytes
weaken P1-6 sensitivity/access policy
```

This is the only purpose of the extension for current critical path.

---

# 21. source scope for future implementation

Expected later implementation touch points:

```text
src/aiscc/evidence/content.py
src/aiscc/evidence/models.py
src/aiscc/evidence/ports.py
src/aiscc/evidence/repository.py

src/aiscc/persistence/models.py
src/aiscc/persistence/repository.py

migrations/versions/<next_revision>_p1_6_durable_evidence_content.py

tests/unit/evidence/**
tests/integration/evidence/**
```

P1-8 source should not be modified during the extension implementation except possibly a later dedicated
resume Task that consumes the accepted owner API.

---

# 22. non-goals

Do not design/implement:

```text
general S3/object-store product

large arbitrary artifact blob store

multimedia storage

cross-project file library

RAG/vector store

public content CDN

generic secrets vault

P1-8 runtime

P2/P3

deployment/provider integration
```

This is a bounded durable canonical structured-content authority extension.

---

# 23. failure vocabulary

Freeze exact typed equivalents:

```text
DURABLE_CONTENT_REQUIRED
DURABLE_CONTENT_KIND_NOT_SUPPORTED
DURABLE_CONTENT_TOO_LARGE
DURABLE_CONTENT_SENSITIVITY_DENIED
DURABLE_CONTENT_IDENTITY_CONFLICT
DURABLE_CONTENT_MISSING
DURABLE_CONTENT_INTEGRITY_MISMATCH
DURABLE_CONTENT_SCHEMA_MISMATCH
DURABLE_CONTENT_ACCESS_DENIED
P1_8_STRUCTURED_SOURCE_NOT_DURABLE
```

Distinguish:

```text
historical content corruption
```

from:

```text
ordinary current evidence revocation/staleness
```

---

# 24. required design examples

Include exact positive/negative examples.

## positive

```text
canonical structured result
→ durable P1-6 content write
→ EvidenceContentRef
→ candidate/admission
→ restart
→ historical resolver returns exact same bytes
→ P1-8 may reconstruct exact field and MCF_V1
```

## caller laundering negative

```text
metadata-only old AdmittedEvidence
+ caller supplies bytes matching claimed semantics
→ P1-8 source NOT eligible
```

Even if caller bytes hash-match a separately claimed hash without owner-backed durable ref, fail closed.

## identity corruption

```text
same object ID/version
+ different canonical bytes
→ identity conflict
```

## restart loss

```text
process-local cache emptied
→ durable enrolled content still resolves
```

## sensitivity

```text
SECRET_FORBIDDEN
→ no durable body

private body
→ public export denied
```

---

# 25. allowed mutation

Create only:

```text
.aiassistant/rules/
AISCC_DURABLE_EVIDENCE_CONTENT_AUTHORITY.md
```

Task lifecycle:

```text
.aiassistant/tasks/active/
20260830_2130_aiscc-p1-6-durable-evidence-content-authority-baseline-design-1.md

→

.aiassistant/tasks/done/
20260830_2130_aiscc-p1-6-durable-evidence-content-authority-baseline-design-1.md
```

Temporary review bundle:

```text
.aiassistant/reports/target/
20260830_2130_aiscc-p1-6-durable-evidence-content-authority-baseline-design-1/**
```

Do not update canonical state files in this design Task.

---

# 26. forbidden

No:

```text
src/**
tests/**
migrations/**

changes to AISCC_EVIDENCE_ADMISSION.md
changes to AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md

P1-8 runtime
P2/P3

Git add/commit/push

provider/network/credential/deployment
```

Do not amend:

```text
c108e9c02f222cf51ce833e311465584447b3571
b111f5f676e1a782de095e2f5b2a106d8b9a0207
```

---

# 27. evidence contract

## executor_required

```text
DESIGN_CURRENT_CONTENT_GAP

DESIGN_DURABLE_CONTENT_IDENTITY

DESIGN_ALLOWED_KINDS_AND_SIZE

DESIGN_SENSITIVITY_AND_ACCESS

DESIGN_OWNER_WRITE_BOUNDARY

DESIGN_REQUIREMENT_ELIGIBILITY

DESIGN_HISTORICAL_RESOLVER

DESIGN_RESTART

DESIGN_RETENTION

DESIGN_P1_8_HANDOFF

DESIGN_BACKWARD_COMPATIBILITY

STATIC_GOVERNANCE
```

## human_owned

```text
P1-6 durable evidence-content extension design final review
→ HUMAN_PENDING
```

## not_required

```text
runtime tests
PostgreSQL migration
P1-8 runtime
deployment
```

---

# 28. mandatory stop

STOP on:

```text
HEAD drift

P1-6 accepted design drift

P1-8 accepted design drift

durable content requires changing evidence admission truth semantics

SECRET_FORBIDDEN bytes would need persistence

P1-8 would need direct write authority into P1-6 content

an external object-store/provider is mandatory for V1

unrelated tracked dirty collision
```

Report:

```text
POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

or:

```text
DESIGN_BASELINE_GAP
```

as exact.

---

# 29. accept criteria

All must hold:

```text
one exact bounded durable structured-content model selected

exact allowed content kinds selected

hard byte-size ceiling selected

sensitivity/access/retention behavior explicit

owner-backed write boundary explicit

durable historical identity independent of process object token

Requirement/EvidenceType durable-content enrollment explicit

metadata-only legacy evidence remains P1-6 valid but not automatically P1-8 eligible

historical resolver reconstructs exact canonical bytes after restart

historical content validity separated from current evidence effectiveness

P1-8 handoff exact and one-way

no caller-byte backfill authority

no P1-6 admission semantic change

no runtime implementation

Human verification = HUMAN_PENDING
```

---

# 30. report requirements

Report exact:

1. Task path
2. start/final HEAD
3. P1-6 accepted design SHA
4. P1-8 accepted design SHA
5. current content-store persistence finding
6. exact selected durable store model
7. durable content object fields/identity
8. exact eligible content kinds
9. exact byte-size cap
10. sensitivity matrix
11. retention model
12. owner write authority
13. Requirement/EvidenceType durable eligibility field
14. historical resolver API
15. process-token separation
16. candidate/admission transaction relation
17. correction/revocation behavior
18. restart reconstruction
19. legacy metadata-only compatibility
20. P1-8 eligible source rule
21. caller-laundering negative
22. secret/public-export negative
23. implementation touch points
24. migration direction
25. open Human choices, if any
26. runtime implementation = NOT_STARTED
27. P1-8 runtime = BLOCKED
28. Git actions = none
29. provider/network/deployment = 0
30. human verification = HUMAN_PENDING
31. preserved exact paths
32. next recommendation

---

# 31. export

Target:

```text
.aiassistant/reports/target/
20260830_2130_aiscc-p1-6-durable-evidence-content-authority-baseline-design-1/
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
20260830_2130_aiscc-p1-8-runtime-durable-evidence-content-baseline-gap-hold-1.cycle.md

.aiassistant/tasks/done/
20260830_2130_aiscc-p1-6-durable-evidence-content-authority-baseline-design-1.md
```

---

# 32. expected submission state

```text
P1-6 core:
ACCEPTED / CLOSED

P1-6 Durable Evidence Content Extension Design:
DESIGN_CANDIDATE / HUMAN_PENDING

P1-8 Design:
ACCEPTED / CLOSED

P1-8 Runtime:
BLOCKED_REQUIRED_EVIDENCE / IMPLEMENTATION_BASELINE_GAP

P2:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

Command Center next:

```text
review durable evidence-content design

→ PASS / HUMAN_FINAL_REVIEW_REQUIRED
or
→ HOLD_REWORK_REQUIRED
```

Only after Human acceptance may implementation begin.
