# 작업지시서: P1-6 Durable Evidence Content Design Terminal Persistence + Runtime Implementation

## meta

- task_id: `20260830_2357_aiscc-p1-6-durable-evidence-content-design-terminal-persistence-and-runtime-implementation-1`
- created_at: `2026-08-30T23:57:00+09:00`
- phase: `P1-6 Durable Evidence Content Authority Extension`
- work_type: `DESIGN_TERMINAL_PERSISTENCE_AND_RUNTIME_IMPLEMENTATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1_6_EVIDENCE_CONTENT`
- expected_start_head: `b111f5f676e1a782de095e2f5b2a106d8b9a0207`
- accepted_extension_design_path: `.aiassistant/rules/AISCC_DURABLE_EVIDENCE_CONTENT_AUTHORITY.md`
- accepted_extension_design_sha256: `ab54948fb8c253309d5a8c228e31fca1b9afb9e19f0faf9be9cda8d14b735411`
- accepted_p1_6_core_design_sha256: `0d9d4c194efda37f100c6183d1a7e88e1a09fe073dc3a37bbb5a3e1cd577e463`
- accepted_p1_8_design_commit: `c108e9c02f222cf51ce833e311465584447b3571`
- accepted_p1_8_design_sha256: `100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a`
- p1_8_design_terminal_governance_commit: `b111f5f676e1a782de095e2f5b2a106d8b9a0207`
- human_extension_design_review: `HUMAN_PROVIDED / ACCEPTED`
- p1_6_core_status: `HUMAN_PROVIDED / ACCEPTED / CLOSED`
- p1_8_design_status: `HUMAN_PROVIDED / ACCEPTED / CLOSED`
- p1_8_runtime_status: `BLOCKED_REQUIRED_EVIDENCE / IMPLEMENTATION_BASELINE_GAP`
- p2_status: `NOT_STARTED`
- public_bounded_live: `NOT_RELEASED`

---

# 1. Human final design judgment

Human review is complete.

Exact Human decision:

```text
Human P1-6 durable evidence-content extension design final review
판정: ACCEPTED
```

Do not ask for extension design acceptance again.

The exact accepted extension design bytes are:

```text
.aiassistant/rules/AISCC_DURABLE_EVIDENCE_CONTENT_AUTHORITY.md

SHA-256:
ab54948fb8c253309d5a8c228e31fca1b9afb9e19f0faf9be9cda8d14b735411
```

Do not modify those bytes before Stage 0A.

Human acceptance is terminal governance provenance, not a reason to rewrite the accepted design file.

---

# 2. task objective

Strict sequence:

```text
Stage 0A
→ commit exact Human-accepted durable-content extension design

Stage 0B
→ persist Human acceptance, baseline-gap/HOLD lineage, canonical state,
   and implementation authorization in a separate governance commit

Stage 1
→ implement P1-6 durable evidence-content runtime extension only
→ produce uncommitted runtime candidate
→ Human runtime acceptance remains pending
```

Do not combine Stage 0A and Stage 0B.

Do not commit Stage 1 runtime.

Do not resume P1-8 runtime in this Task.

---

# 3. mandatory preflight

Before mutation/index action:

## 3.1 HEAD

Require:

```text
HEAD ==
b111f5f676e1a782de095e2f5b2a106d8b9a0207
```

Mismatch:

```text
STOP
→ REVIEWED_BASELINE_DRIFT
```

No reset/rebase/clean/amend.

## 3.2 accepted designs

Require:

```text
sha256(.aiassistant/rules/AISCC_DURABLE_EVIDENCE_CONTENT_AUTHORITY.md)
==
ab54948fb8c253309d5a8c228e31fca1b9afb9e19f0faf9be9cda8d14b735411
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

Mismatch:

```text
STOP
→ ACCEPTED_DESIGN_DRIFT
```

## 3.3 workspace

Record:

```text
git status --short
git diff --name-only
git diff --cached --name-only
```

Index must be empty.

Expected uncommitted governance/design set before Stage 0A may include:

```text
.aiassistant/rules/AISCC_DURABLE_EVIDENCE_CONTENT_AUTHORITY.md

.aiassistant/tasks/done/
20260830_2130_aiscc-p1-6-durable-evidence-content-authority-baseline-design-1.md

.aiassistant/tasks/done/
20260830_2308_aiscc-p1-6-durable-content-requirement-fingerprint-compatibility-design-rework-1.md

.aiassistant/records/aiscc/cycles/
20260830_2130_aiscc-p1-8-runtime-durable-evidence-content-baseline-gap-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260830_2308_aiscc-p1-6-durable-content-requirement-fingerprint-backward-compatibility-hold-1.cycle.md
```

plus this current active Task after placement.

Any unrelated tracked dirty path:

```text
STOP
→ DIRTY_WORKSPACE_MIXED
```

Forbidden:

```text
git add .
git add -A
git reset
git clean
```

---

# 4. frozen semantic boundary

This extension adds:

```text
durable canonical structured-content reconstruction
```

It does NOT replace or reinterpret:

```text
EvidenceRequirement truth semantics
EvidenceCandidate
EvidenceAdmissionRequest
EvidenceEvaluation
EvidenceAdmissionDecision
AdmittedEvidence
EvidenceSetEvaluation
EvidenceSetSatisfactionAttestation
G_EVIDENCE
P1-7 Human/Judgment authority
P1-8 Cycle/Memory/NextAction authority
```

Mandatory non-substitution:

```text
DurableEvidenceContentObject != EvidenceCandidate
DurableEvidenceContentObject != AdmittedEvidence
Durable content availability != evidence current effectiveness
Durable content resolver != Judgment
Durable content resolver != WorkflowState
P1-8 historical consumer != P1-6 content writer
```

Legacy P1-6 historical admission remains valid.

---

# 5. Stage 0A — exact accepted extension design commit

Stage exactly:

```text
.aiassistant/rules/AISCC_DURABLE_EVIDENCE_CONTENT_AUTHORITY.md
```

Verify staged path set:

```text
exactly 1
```

Verify staged blob SHA:

```text
ab54948fb8c253309d5a8c228e31fca1b9afb9e19f0faf9be9cda8d14b735411
```

Recommended commit message:

```text
docs(design): freeze durable evidence content authority

Freeze the Human-accepted P1-6 extension for bounded PostgreSQL-backed
canonical structured evidence content, restart-safe historical resolution,
prospective durable-content enrollment, and exact legacy fingerprint
compatibility without changing P1-6 admission truth semantics.
```

Create Stage 0A.

Record:

```text
P1_6_DURABLE_CONTENT_DESIGN_ACCEPTANCE_COMMIT=<40-char SHA>
```

Verify:

```text
parent ==
b111f5f676e1a782de095e2f5b2a106d8b9a0207

changed path ==
exact design path

blob SHA ==
ab54948fb8c253309d5a8c228e31fca1b9afb9e19f0faf9be9cda8d14b735411
```

Do not amend.

---

# 6. Stage 0B — terminal governance persistence

Only after Stage 0A SHA is known.

## 6.1 create final acceptance Cycle

Create:

```text
.aiassistant/records/aiscc/cycles/
20260830_2357_aiscc-p1-6-durable-evidence-content-design-final-acceptance-1.cycle.md
```

It must contain actual exact values:

```text
Human review:
HUMAN_PROVIDED / ACCEPTED

accepted extension design commit:
<exact P1_6_DURABLE_CONTENT_DESIGN_ACCEPTANCE_COMMIT>

accepted extension design SHA:
ab54948fb8c253309d5a8c228e31fca1b9afb9e19f0faf9be9cda8d14b735411

P1-6 core:
ACCEPTED / CLOSED

P1-6 Durable Evidence Content Extension Design:
ACCEPTED / CLOSED

P1-6 Durable Evidence Content Extension Runtime:
NOT_STARTED / IMPLEMENTATION_AUTHORIZED

P1-8 Design:
ACCEPTED / CLOSED

P1-8 Runtime:
BLOCKED_REQUIRED_EVIDENCE

P2:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

Record design lineage:

```text
2130 baseline-gap discovery
→ P1-8 runtime correctly stopped

2130 durable-content baseline design

2308 HOLD
→ legacy Requirement fingerprint / RequirementSet root compatibility

2308 compatibility rework
→ explicit V1/V2 Requirement fingerprint schema
→ exact legacy historical identity preservation

Human final extension design acceptance
```

No placeholder SHA.

## 6.2 persist prior design Task/HOLD lineage

Stage exact existing files:

```text
.aiassistant/tasks/done/
20260830_2130_aiscc-p1-6-durable-evidence-content-authority-baseline-design-1.md

.aiassistant/tasks/done/
20260830_2308_aiscc-p1-6-durable-content-requirement-fingerprint-compatibility-design-rework-1.md

.aiassistant/records/aiscc/cycles/
20260830_2130_aiscc-p1-8-runtime-durable-evidence-content-baseline-gap-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260830_2308_aiscc-p1-6-durable-content-requirement-fingerprint-backward-compatibility-hold-1.cycle.md
```

Do not rewrite them.

## 6.3 canonical state

Update exactly:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

Required canonical state:

```text
P1-6 core
→ HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-6 Durable Evidence Content Extension Design
→ HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-6 Durable Evidence Content Extension accepted design commit
→ <exact Stage 0A SHA>

P1-6 Durable Evidence Content Extension accepted design SHA
→ ab54948fb8c253309d5a8c228e31fca1b9afb9e19f0faf9be9cda8d14b735411

P1-6 Durable Evidence Content Extension Runtime
→ NOT_STARTED / IMPLEMENTATION_AUTHORIZED

P1-8 Design
→ HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-8 Runtime
→ BLOCKED_REQUIRED_EVIDENCE
→ WAITING_FOR_P1_6_DURABLE_CONTENT_RUNTIME_ACCEPTANCE

P2
→ NOT_STARTED

PUBLIC_BOUNDED_LIVE
→ NOT_RELEASED
```

`NEXT_ACTIONS.md`:

```text
next:
P1-6 Durable Evidence Content Extension Runtime Implementation
```

Do not mark P1-8 runtime resumed.

## 6.4 current Task

Stage current active Task:

```text
.aiassistant/tasks/active/
20260830_2357_aiscc-p1-6-durable-evidence-content-design-terminal-persistence-and-runtime-implementation-1.md
```

It remains active through Stage 1.

## 6.5 exact Stage 0B allowlist

Exactly 9 paths:

```text
2 prior done design Tasks
2 prior HOLD Cycles
1 final acceptance Cycle
3 canonical state files
1 current active Task
```

No design rule: already Stage 0A.

No source/test/migration.

No target export.

Verify exact 9-path staged set before commit.

Recommended commit message:

```text
chore(governance): accept durable evidence content design

Record Human acceptance of the bounded P1-6 durable evidence-content extension,
preserve its baseline-gap and compatibility review lineage, and authorize its
runtime implementation while keeping P1-8 runtime blocked until extension
runtime acceptance.
```

Create Stage 0B.

Record:

```text
P1_6_DURABLE_CONTENT_DESIGN_TERMINAL_COMMIT=<40-char SHA>
```

Verify lineage:

```text
b111f5f676e1a782de095e2f5b2a106d8b9a0207
→ P1_6_DURABLE_CONTENT_DESIGN_ACCEPTANCE_COMMIT
→ P1_6_DURABLE_CONTENT_DESIGN_TERMINAL_COMMIT
```

Do not amend either commit.

---

# 7. Stage 1 — runtime implementation only

Start only after Stage 0A/0B verification.

Stage 1 output:

```text
P1-6 durable evidence-content runtime candidate
→ uncommitted
→ Human runtime acceptance pending
```

Do NOT resume P1-8 runtime.

Do NOT implement P1-8 source/tests/migration in this Task.

No Stage 1 git add/commit/push.

---

# 8. exact V1 storage model

Implement the accepted bounded store:

```text
PostgreSQL durable canonical structured bytes
```

Exact hard body limit:

```text
65,536 bytes
```

after canonicalization.

Implement immutable logical object equivalent to:

```text
DurableEvidenceContentObject
```

with accepted fields from the design, including:

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

Exact source names may follow existing code conventions but semantics must match.

No body update in place.

---

# 9. canonicalization

Implement:

```text
AISCC_CANONICAL_STRUCTURED_JSON_V1
```

exact accepted behavior.

Mandatory:

```text
UTF-8
Unicode NFC
duplicate object-key rejection
integer-only numeric model
maximum nesting depth 32
maximum total JSON nodes 4,096
deterministic object-key ordering
stable arrays
no NaN/Infinity/floating-point ambiguity
```

Size check:

```text
canonicalized bytes <= 65,536
```

Reject otherwise.

Add fixed canonicalization/fingerprint test vectors.

Do not silently accept non-canonical caller bytes as historical authority.

---

# 10. durable content kinds

Durable in V1 only:

```text
INLINE_CANONICAL_STRUCTURED_BODY
DATABASE_OBSERVATION_REF
RUNTIME_OBSERVATION_REF
```

Not durable in V1:

```text
HUMAN_STRUCTURED_REF
P1_5_IMMUTABLE_PRODUCER_REF
PRIOR_ADMITTED_EVIDENCE_REF
arbitrary CONTENT_ADDRESSED_ARTIFACT_REF
```

Do not copy/refactor P1-5 producer artifacts into this store.

Unsupported kind:

```text
DURABLE_CONTENT_KIND_NOT_SUPPORTED
```

---

# 11. sensitivity/access

Durable supported:

```text
PUBLIC_SAFE
INTERNAL
```

Durable NOT supported:

```text
PRIVATE_SENSITIVE
SECRET_FORBIDDEN
```

Required:

```text
SECRET_FORBIDDEN
→ body never persisted

PRIVATE_SENSITIVE
→ durable structured body rejected in V1
```

Public export:

```text
metadata/hash/ref by default
```

Body export only when exact accepted export policy permits `PUBLIC_SAFE`.

P1-8 read authority must never broaden sensitivity/export permission.

---

# 12. P1-6-only writer boundary

Write path:

```text
owner-backed canonical source
→ P1-6 canonicalization
→ P1-6 durable content repository
→ immutable EvidenceContentRef
→ candidate/admission
```

Forbidden:

```text
P1-8 direct durable-content write
caller direct durable-content write
caller-provided body as historical source replacement
hash-only fabricated body
```

Durable historical authority must not depend on Python process object identity or `_owner_token`.

Internal mutation capability token may remain for process safety but cannot be historical provenance.

---

# 13. Requirement fingerprint compatibility — mandatory

Implement the accepted explicit versioned contract.

Required equivalent schemas:

```text
P1_6_EVIDENCE_REQUIREMENT_FINGERPRINT_V1

P1_6_EVIDENCE_REQUIREMENT_FINGERPRINT_V2_DURABLE_CONTENT
```

V1:

```text
exact pre-extension canonical field set
exact old fingerprint algorithm
NO synthetic durable fields
```

V2:

```text
V1 logical requirement fields
+ explicit fingerprint_schema
+ durable_content_requirement
+ durable_content_policy_ref
+ durable_content_policy_fingerprint
```

Historical selector authority:

```text
persisted immutable requirement fingerprint schema/version
```

Never:

```text
current code version
migration version
current policy
nullable-field heuristic
```

as historical fingerprint authority.

Legacy semantic view may expose:

```text
durable_content_requirement = NOT_APPLICABLE
```

in memory, but that field must not enter V1 historical canonical bytes.

---

# 14. RequirementSet root compatibility

Preserve exact accepted root algorithm over already-verified requirement refs/fingerprints.

Required:

```text
legacy V1 Requirement fingerprints
→ exact unchanged
→ legacy RequirementSet root exact unchanged

new V2 durable-capable Requirements
→ new exact fingerprints
→ new RequirementSet root commits to those exact identities
```

No legacy RequirementSet root rewrite/recompute in migration.

If current implementation stores a set fingerprint/payload beyond the root, preserve its historical schema exactly.

---

# 15. request/evaluation/attestation compatibility

Do not add redundant durable fields to immutable identities unless accepted design explicitly requires them.

Prefer preserving current:

```text
EvidenceAdmissionRequest
EvidenceEvaluation
EvidenceSetEvaluation
EvidenceSetSatisfactionAttestation
EvidenceAdmissionDecision
AdmittedEvidence
```

fingerprint/payload contracts because they already commit transitively to Requirement/RequirementSet/candidate identities.

If implementation proves a new field is mandatory:

```text
STOP
→ POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

Do not casually create hidden V2 downstream fingerprints.

Legacy IDs/fingerprints must remain exact.

---

# 16. prospective durable enrollment

Only newly issued V2 durable-capable Requirement versions can require P1-8 reconstructable structured content.

Implement accepted exact equivalent:

```text
durable_content_requirement:
REQUIRED
```

plus exact durable content policy ref/fingerprint.

Legacy V1:

```text
P1-6 historical validity:
preserved

P1-8 structured-source eligibility:
DENY unless independently durable owner-backed source already satisfies accepted contract
```

No caller-byte backfill.

No mutation of old Requirement to REQUIRED.

A durable capability/policy change means:

```text
new Requirement version/identity
```

not in-place mutation.

---

# 17. transaction and identity

Durable body + ref must become authoritative without metadata/body split-brain.

Implement transaction ordering accepted by design.

Required invariants:

```text
same object_id/version + same immutable payload
→ idempotent replay

same object_id/version + different bytes/payload
→ DURABLE_CONTENT_IDENTITY_CONFLICT

candidate durable ref
→ exact committed durable object

admission requiring durable content
→ durable object/ref exists and verifies before ADMITTED decision
```

No candidate/admitted row may claim REQUIRED durable content that is missing/uncommitted.

No orphan body should become evidence authority.

If body-first transaction leaves non-authoritative orphan rows on rejected admission, they must be safely unreachable/non-admitted and have exact cleanup/retention semantics; prefer same transaction where feasible.

---

# 18. PostgreSQL migration

Create next forward-only Alembic revision after current:

```text
20260829_0004
```

Preferred if free:

```text
20260830_0005_p1_6_durable_evidence_content.py
```

If repository already contains a later revision after Stage 0B, choose next linear revision and report.

Migration must add equivalent durable storage and explicit requirement fingerprint schema support without rewriting historical identities.

Required migration rules:

```text
NO rewrite existing immutable Requirement JSON payload
NO recompute existing Requirement fingerprint
NO recompute existing RequirementSet root/fingerprint
NO rewrite legacy AdmissionRequest/Evaluation/Attestation payloads
NO rewrite Candidate/AdmittedEvidence historical identity
```

If an explicit physical selector column is added:

```text
legacy rows
→ materialize V1 selector without changing canonical historical identity

future rows
→ explicit schema required
```

No migration-time hash/root regeneration.

---

# 19. historical content resolver

Implement owner-side projection-independent APIs equivalent to:

```text
verify_historical_content_ref(...)
resolve_historical_canonical_body(...)
```

Must verify:

```text
serialized content ref
owner id/version
object id/version
content kind
canonicalization
schema id/version
byte count
content hash
sensitivity
retention/access policy
durable object fingerprint
canonical body bytes
```

Required:

```text
sha256(canonical_body_bytes)
==
EvidenceContentRef.content_hash
```

No current WorkRun/current Evidence effectiveness/current RequirementSet requirement.

Historical content integrity:

```text
!= current evidence effectiveness
```

Metadata-only P1-6 historical verifier should remain available without loading body bytes.

Authorized exact-body resolution is opt-in.

---

# 20. restart contract

Prove:

```text
process restart
→ same durable EvidenceContentRef
→ exact same canonical bytes

ephemeral _objects cache empty
→ durable enrolled content still resolves

PostgreSQL
→ authority
```

Process-local `PrivateEvidenceContentStore` may remain only as:

```text
test fixture
ephemeral cache
non-durable content mode
```

not as sole authority for durable-enrolled evidence.

---

# 21. correction/revocation/retention

Body identity immutable.

Correction:

```text
new object/version
→ new candidate/admission
```

Evidence revocation/current staleness:

```text
does not rewrite/delete old body
```

V1 retention:

```text
no automatic deletion before project/competition provenance boundary
```

Deletion/expiry that would break required P1-8 historical reconstruction is forbidden in V1.

Current evidence effectiveness and durable historical content availability remain separate dimensions.

---

# 22. exact P1-8 handoff contract

Expose only the accepted one-way consumer path:

```text
complete historical P1-6 admission provenance
+ exact EvidenceContentRef
+ authorized historical content resolver
→ P1-8 may reconstruct structured field/object
```

P1-8 may later:

```text
resolve canonical bytes
extract policy-fixed field/object
recompute MCF_V1
```

P1-8 may NOT:

```text
write body
supply missing bytes
change content sensitivity
change Requirement durable enrollment
```

Do not implement P1-8 consumer in this Task.

---

# 23. expected source touch points

Expected narrow scope:

```text
src/aiscc/evidence/content.py
src/aiscc/evidence/models.py
src/aiscc/evidence/ports.py
src/aiscc/evidence/service.py
src/aiscc/evidence/repository.py

src/aiscc/persistence/models.py
src/aiscc/persistence/repository.py

migrations/versions/<next>_p1_6_durable_evidence_content.py

tests/unit/evidence/**
tests/integration/evidence/**
```

Touch other packages only for narrow regression fixture/integration compatibility.

Do not change P1-8 runtime source.

---

# 24. required unit tests

At minimum:

```text
canonical JSON fixed vectors
duplicate-key reject
float/NaN/Infinity reject
NFC normalization
depth 32 boundary
4,096 node boundary
65,536 byte boundary
65,537 reject

content-kind allowlist
sensitivity matrix

same object identity/same bytes replay
same identity/different bytes conflict

Requirement V1 exact fingerprint fixture
Requirement V2 exact fingerprint fixture
V1 semantic NOT_APPLICABLE does not alter V1 hash
```

---

# 25. required PostgreSQL integration tests

## 25.1 durable body

Prove:

```text
V2 REQUIRED structured evidence
→ durable body/ref exists
→ candidate/admission succeeds

missing durable body
→ reject

hash mismatch
→ fail closed

schema/canonicalization mismatch
→ fail closed

unsupported kind
→ reject

PRIVATE_SENSITIVE
→ reject

SECRET_FORBIDDEN
→ body never persisted
```

## 25.2 restart

Fresh PostgreSQL:

```text
persist V2 durable content
→ dispose/recreate process services/session
→ no process-local owner/cache
→ historical resolver returns byte-equivalent body
```

## 25.3 legacy fingerprint/root regression

Use fixtures/rows whose expected bytes/hashes are frozen from pre-extension V1.

After migration:

```text
legacy Requirement canonical payload
→ unchanged

legacy Requirement fingerprint
→ exact unchanged

legacy RequirementSet root
→ exact unchanged

legacy AdmissionRequest identity/fingerprint
→ exact unchanged

legacy EvidenceSetEvaluation
→ exact unchanged / verifies

legacy EvidenceSetSatisfactionAttestation
→ verifies

legacy AdmittedEvidence historical provenance
→ verifies
```

## 25.4 P1-7 transitive historical regression

Where P1-7 records consume P1-6 historical provenance:

```text
legacy HumanResult historical provenance
→ PASS

legacy Judgment historical provenance
→ PASS
```

No new durable field/default may break old transitive graph.

## 25.5 legacy P1-8 eligibility cut

Prove:

```text
legacy metadata-only/process-local structured evidence
→ P1-6 historical validity PASS

→ durable P1-8 structured-source eligibility DENY
```

No caller body may upgrade it.

## 25.6 V2 versioning

Prove:

```text
old logical Requirement V1
→ cannot be mutated to REQUIRED

new V2 durable capability
→ new fingerprint

new RequirementSet root
→ commits new V2 fingerprint

V2 historical verifier
→ exact schema-specific reconstruction
```

---

# 26. concurrency tests

Fresh PostgreSQL tests:

```text
same durable object id/version same payload
→ idempotent

same id/version different payload
→ one winner + typed identity conflict

concurrent candidate creation for REQUIRED durable evidence
→ cannot observe uncommitted/mismatched body

concurrent V2 Requirement issuance same immutable id
→ deterministic replay/conflict
```

No last-write-wins.

Use existing project locking conventions; do not invent broad global locks unless required.

---

# 27. corruption/fail-closed tests

At minimum:

```text
missing durable row
body/hash mismatch
byte_count mismatch
schema mismatch
canonicalization mismatch
owner mismatch
content fingerprint mismatch
unknown Requirement fingerprint schema
V1 row with illegal V2 canonical fields
V2 row missing required durable fields
RequirementSet root mismatch
```

All fail closed with typed errors.

Ordinary current evidence revocation/staleness must not be misclassified as historical content corruption.

---

# 28. predecessor regression suites

Mandatory:

```text
full P1-6 unit/integration suite

P1-4 PostgreSQL regression

P1-6 PostgreSQL regression

P1-7 Human/Judgment PostgreSQL regression

full unit + integration suite
```

The extension is not accepted if older provenance stops verifying.

Report exact counts.

---

# 29. static/security verification

Run:

```text
ruff
mypy src
```

Verify migration head/version.

Secret scan without printing values.

Verify durable body table never stores rejected `SECRET_FORBIDDEN` test body.

No provider/network/credentialed external/deployment action.

---

# 30. runtime candidate Git policy

After Stage 0B:

```text
NO git add
NO runtime commit
NO push
```

Runtime candidate stays working-tree only.

At successful Executor completion, move:

```text
.aiassistant/tasks/active/
20260830_2357_aiscc-p1-6-durable-evidence-content-design-terminal-persistence-and-runtime-implementation-1.md

→

.aiassistant/tasks/done/
20260830_2357_aiscc-p1-6-durable-evidence-content-design-terminal-persistence-and-runtime-implementation-1.md
```

That done-path lifecycle change is part of the uncommitted review set, not Stage 0B.

---

# 31. mandatory STOP conditions

STOP with exact report if:

```text
accepted extension design SHA drift

Stage 0A/0B staged path mismatch

exact pre-extension Requirement V1 fingerprint cannot be reproduced

legacy RequirementSet root changes after extension

legacy P1-6 historical provenance fails due to new defaults/schema

P1-7 historical provenance fails due to extension

current P1-6 source architecture cannot enforce durable REQUIRED without changing core admission truth semantics

P1-8 runtime modification becomes necessary to finish extension

PRIVATE_SENSITIVE or SECRET_FORBIDDEN persistence is required

external object store/provider becomes required

unrelated dirty workspace collision
```

Use:

```text
IMPLEMENTATION_BASELINE_GAP
POLICY_CONFLICT_INVESTIGATION_REQUIRED
LEGACY_PROVENANCE_REGRESSION
```

as appropriate.

Do not weaken design to continue.

---

# 32. evidence contract

## executor_required

### DESIGN_TERMINAL_GIT

```text
Stage 0A exact design blob
Stage 0B exact governance paths
first-parent lineage
no amend
```

### DURABLE_CONTENT_RUNTIME

```text
PostgreSQL durable body
65,536 cap
content-kind allowlist
sensitivity enforcement
P1-6-only write path
historical resolver
restart
```

### REQUIREMENT_COMPATIBILITY

```text
V1 exact fingerprint
V2 durable fingerprint
RequirementSet root compatibility
downstream immutable identity preservation
```

### LEGACY_PROVENANCE

```text
legacy P1-6 historical chain
legacy P1-7 transitive historical chain
```

### SECURITY

```text
SECRET_FORBIDDEN absent
PRIVATE_SENSITIVE denied
public export ceiling preserved
```

### STATIC_SOURCE

```text
ruff
mypy
```

## human_owned

```text
P1-6 durable evidence-content extension runtime final acceptance
→ HUMAN_PENDING
```

## forbidden

```text
P1-8 runtime implementation
P2/P3
provider
external IdP
deployment
Public Live
```

---

# 33. runtime aggregate/export

Target:

```text
.aiassistant/reports/target/
20260830_2357_aiscc-p1-6-durable-evidence-content-design-terminal-persistence-and-runtime-implementation-1/
```

Required:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
```

Include byte-preserving copies of Stage 1 changed:

```text
source
migration
tests
done Task lifecycle file
```

Also include review copies of:

```text
2357 design final acceptance Cycle
CURRENT_STATE_SUMMARY.md
DECISION_REGISTER.md
NEXT_ACTIONS.md
```

Runtime aggregate includes only Stage 1:

```text
source
migration
tests
```

Do not mix governance Task/Cycle/state files into runtime aggregate.

Algorithm:

```text
sort repository-relative runtime paths ordinally

serialize:
<path>\t<lowercase_sha256>\n

SHA-256 of concatenated UTF-8 bytes
```

Manifest must report:

```text
start HEAD
Stage 0A SHA
Stage 0B SHA
final HEAD

accepted extension design SHA

runtime path count
per-file SHA
runtime aggregate

source/copy identity
Git status/index
```

---

# 34. Executor report required fields

Report exact:

1. Task path
2. start HEAD
3. P1-6 core design SHA
4. P1-8 accepted design SHA
5. accepted extension design SHA
6. Stage 0A staged path
7. Stage 0A commit SHA
8. Stage 0A parent/blob SHA
9. final acceptance Cycle path
10. Human design acceptance persisted
11. baseline-gap/HOLD lineage persisted
12. canonical state update
13. Stage 0B exact 9-path set
14. Stage 0B commit SHA
15. Stage 0B parent
16. Stage 0A→0B lineage
17. chosen migration revision/head
18. durable content table/schema
19. exact content kinds
20. 65,536 cap enforcement
21. canonicalization implementation
22. sensitivity/access enforcement
23. P1-6-only writer boundary
24. EvidenceContentRef durable identity
25. V1 Requirement fingerprint implementation
26. V2 Requirement fingerprint implementation
27. historical selector authority
28. RequirementSet root compatibility
29. AdmissionRequest/Evaluation/Attestation compatibility
30. legacy migration cut line
31. historical resolver APIs
32. restart evidence
33. identity/concurrency evidence
34. corruption fail-closed evidence
35. legacy P1-6 provenance regression
36. legacy P1-7 provenance regression
37. legacy P1-8 eligibility denial evidence
38. V2 durable admission evidence
39. full unit/integration count
40. P1-4 PostgreSQL regression
41. P1-6 PostgreSQL regression
42. P1-7 PostgreSQL regression
43. PostgreSQL version
44. Alembic revision
45. ruff
46. mypy
47. secret/privacy checks
48. provider/network/credential/deployment = 0
49. P1-8 runtime = NOT_RESUMED
50. runtime path count
51. runtime aggregate SHA-256
52. Stage 1 Git actions = none
53. final HEAD
54. final index
55. Human runtime verification = HUMAN_PENDING
56. preserved exact paths
57. next recommendation

---

# 35. expected successful submission state

```text
P1-6 core:
ACCEPTED / CLOSED

P1-6 Durable Evidence Content Extension Design:
HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-6 Durable Evidence Content Extension Runtime:
EXECUTOR_COMPLETED / HUMAN_PENDING

P1-8 Design:
ACCEPTED / CLOSED

P1-8 Runtime:
BLOCKED_REQUIRED_EVIDENCE
→ NOT_RESUMED

P2:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

Command Center next:

```text
review exact durable-content runtime candidate

→ PASS / HUMAN_FINAL_REVIEW_REQUIRED
or
→ HOLD_REWORK_REQUIRED
```

Only after Human runtime acceptance may P1-8 runtime resume.

---

# 36. preserved exact paths

After successful submission explicitly preserve:

```text
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md

.aiassistant/rules/AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md

.aiassistant/rules/AISCC_DURABLE_EVIDENCE_CONTENT_AUTHORITY.md

.aiassistant/records/aiscc/cycles/
20260830_2130_aiscc-p1-8-runtime-durable-evidence-content-baseline-gap-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260830_2308_aiscc-p1-6-durable-content-requirement-fingerprint-backward-compatibility-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260830_2357_aiscc-p1-6-durable-evidence-content-design-final-acceptance-1.cycle.md

.aiassistant/tasks/done/
20260830_2130_aiscc-p1-6-durable-evidence-content-authority-baseline-design-1.md

.aiassistant/tasks/done/
20260830_2308_aiscc-p1-6-durable-content-requirement-fingerprint-compatibility-design-rework-1.md

.aiassistant/tasks/done/
20260830_2357_aiscc-p1-6-durable-evidence-content-design-terminal-persistence-and-runtime-implementation-1.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

The target export bundle remains review-only and deletable after Command Center judgment unless explicitly
preserved later.
