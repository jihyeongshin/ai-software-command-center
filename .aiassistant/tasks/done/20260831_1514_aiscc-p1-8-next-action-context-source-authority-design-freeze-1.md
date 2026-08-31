# 작업지시서: P1-8 NEXT_ACTION_CONTEXT Source Authority Design Freeze

## meta

- task_id: `20260831_1514_aiscc-p1-8-next-action-context-source-authority-design-freeze-1`
- created_at: `2026-08-31T15:14:00+09:00`
- phase: `P1-8 Runtime Prerequisite Authority Contracts`
- work_type: `DESIGN_FREEZE`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `CROSS_OWNER / COMMAND_CENTER_TASK_AUTHORITY`
- expected_start_head: `f4614198c2745944f7ec02639a45b0315bbc903d`
- accepted_p1_8_design_sha256: `100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a`
- predecessor_prerequisite_design_sha256: `556faad8a77d917fcbfc9ab7b0ba62bd65f985a6f4a1e585c08af668dd14393c`
- blocked_runtime_path_count: `19`
- blocked_runtime_aggregate_sha256: `84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42`
- runtime_implementation: `FORBIDDEN`
- human_design_review: `PENDING`

---

# 1. purpose

Design and freeze the missing owner-backed semantic source for:

```text
P1-8 Memory category:
NEXT_ACTION_CONTEXT

P1-8 NextAction priority ranks:
4 ACCEPTED_CORE_CRITICAL_PATH
5 OPERATIONAL_HARDENING
6 OPTIONAL_OPTIMIZATION
```

Do not modify runtime source/tests/migrations.

Do not modify the blocked 19-path runtime candidate.

Do not yet finish the other prerequisite exact-contract findings in this Task.

Those return after this source authority is frozen.

---

# 2. mandatory preflight

Require:

```text
HEAD ==
f4614198c2745944f7ec02639a45b0315bbc903d

accepted P1-8 design SHA ==
100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a

predecessor prerequisite design SHA ==
556faad8a77d917fcbfc9ab7b0ba62bd65f985a6f4a1e585c08af668dd14393c

blocked runtime ==
19 paths /
84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42
```

Require:

```text
.aiassistant/records/aiscc/cycles/
20260831_1514_aiscc-p1-8-next-action-context-source-authority-baseline-gap-hold-1.cycle.md
```

Index must be empty.

No Git add/commit/push.

---

# 3. candidate design artifact

Create:

```text
.aiassistant/rules/
AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
```

Korean-first prose, English identifiers.

Candidate only until Human final design review.

Do not modify:

```text
AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md
AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
AISCC_EVIDENCE_ADMISSION.md
AISCC_DURABLE_EVIDENCE_CONTENT_AUTHORITY.md
AISCC_HUMAN_GATE_JUDGMENT.md
AISCC_ORCHESTRATION.md
```

in this Task.

---

# 4. selected owner direction to evaluate/freeze

Preferred V1 owner:

```text
EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY

extension:
NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY_V1
```

The candidate design must either:

```text
A. freeze this exact owner
```

or, only if repository evidence proves an already-existing stronger exact owner:

```text
B. reuse that existing owner and explain why it is exact
```

Do NOT choose:

```text
P1-8 producer/caller
P1-8 NextActionProposal
P1-8 descriptor configuration
P1-6 durable content store
raw P1-6 JSON body
Markdown NEXT_ACTIONS presence by itself
```

as semantic priority authority.

---

# 5. exact immutable owner object

Freeze an immutable object equivalent to:

```text
NextActionContextRefV1
```

The exact V1 payload must bind at least:

```text
context_ref_id
context_ref_version = v1
fingerprint_schema = next-action-context-ref-v1

context_owner
authority_ref
authority_version
authority_revision

project_id

task_contract_id
task_contract_version

context_slot_id

priority_class:
ACCEPTED_CORE_CRITICAL_PATH
OPERATIONAL_HARDENING
OPTIONAL_OPTIMIZATION

critical_path_ordinal

context_payload_schema_id
context_payload_schema_version

privacy_class
security_class

issued_at
issuance_sequence
effective_sequence

fingerprint
```

Freeze exact grammar/bounds for every ID/integer.

Recommended V1:

```text
critical_path_ordinal:
integer >= 1
upper bound explicitly frozen
```

Do not include:

```text
P1-8 Cycle ID
NextActionSelection ID
TaskIssuanceCandidate ID
caller rationale/free text
```

in semantic authority.

---

# 6. scope/cardinality

Freeze exact V1 scope.

Preferred:

```text
TASK_CONTRACT scoped only
```

because the external owner can issue the context before WorkRun/Cycle existence.

If project-level context is required, define it as a separate schema variant.

Do not make fields conditionally empty.

No sentinel ambiguity.

Explain exactly how:

```text
TaskContract-scoped context
→ same TaskContract P1-6 evidence
→ exact WorkRun terminal provenance
→ P1-8 admitted Cycle
```

is verified.

---

# 7. owner event/currentness model

Freeze immutable:

```text
NextActionContextAuthorityEventV1
```

or exact equivalent.

Event kinds:

```text
ISSUED
SUPERSEDED
REVOKED
```

Freeze:

```text
event ref/version/fingerprint
context ref/fingerprint
replacement ref if applicable
project/task scope
owner authority ref/version/revision
event sequence
effective sequence/time
current projection disposition
```

Fold rules:

```text
one ISSUED origin

same exact duplicate
→ replay

conflicting duplicate
→ authority conflict

SUPERSEDED
→ replacement becomes current when valid

REVOKED
→ no current context

gap/out-of-order/unknown
→ fail closed
```

Historical issuance validity:

```text
!= current applicability
```

---

# 8. capability boundary

Freeze live capability handling.

Required:

```text
Command Center/Task authority composition root
→ owns opaque issue/supersede/revoke capability

P1-8
→ read/verifier port only

P1-6
→ no context mint authority

ordinary runtime caller
→ no live capability getter

public package
→ cannot mint/revoke recognized context
```

Process capability is current authorization only.

Durable payload/event fingerprint is historical authority.

---

# 9. exact structured-result carrier schema

Freeze one exact structured-result schema to carry the owner context through accepted P1-6 evidence.

Candidate name:

```text
P1_8_NEXT_ACTION_CONTEXT_RESULT_V1
```

Freeze exact canonical JSON object fields.

At minimum:

```text
context_ref
context_fingerprint

priority_class
critical_path_ordinal

context_slot_id

project_id
task_contract_id
task_contract_version
```

The result may contain additional non-authoritative diagnostic fields only if explicitly excluded from
NEXT_ACTION_CONTEXT derivation.

No rationale/free text field may determine priority.

Freeze:

```text
schema ID
schema version
exact JSON selector/object path
canonicalization
allowed/required keys
unknown-key rule
enum/bounds
```

---

# 10. semantic-authority split

This section must be normative.

P1-6 owns:

```text
Requirement/checkpoint/attestation/admission provenance
durable exact canonical body
content hash
schema ID/version binding
terminal-consumed evidence membership
```

P1-6 does NOT own:

```text
priority_class meaning
critical_path_ordinal meaning
Command Center roadmap/task priority
```

The Command Center context owner owns those facts.

P1-8 owns:

```text
policy-fixed source selection
historical source verification orchestration
exact equality verification against NextActionContextRefV1
Memory derivation/MCF
current-memory applicability
NextAction deterministic selection
```

P1-8 does NOT mint the source facts.

---

# 11. P1-6 enrollment boundary

Freeze the prospective EvidenceRequirement contract needed for this structured source.

At minimum:

```text
result schema ID/version =
P1_8_NEXT_ACTION_CONTEXT_RESULT_V1 / v1

durable content:
REQUIRED

allowed durable content kind:
exact accepted structured kind

sensitivity:
compatible with PRIVATE_INTERNAL memory ceiling

exact checkpoint/terminal-consumption requirement
```

The source must satisfy accepted P1-8 `HistoricalStructuredResultAuthorityV1`.

Mandatory:

```text
terminal-consumed attestation/root membership
```

No post-terminal optional evidence promotion.

## semantic contract question

Determine explicitly whether existing P1-6 Requirement:

```text
schema_id + schema_version
```

plus P1-8's immutable policy/source contract is sufficient.

Preferred narrow model:

```text
YES

because:
P1-6 does not certify priority semantics;
P1-8 resolves the exact external owner object and compares every semantic field.
```

If historical correctness instead requires a new persisted semantic-contract ref/fingerprint in the P1-6
Requirement identity:

```text
STOP
→ P1_6_REQUIREMENT_SEMANTIC_CONTRACT_EXTENSION_REQUIRED
```

Do not silently change P1-6 Requirement fingerprint schema in this design.

---

# 12. exact P1-8 Memory derivation

Freeze `NEXT_ACTION_CONTEXT` derivation:

```text
P1-6 historical body
→ exact result object at fixed selector
→ context_ref/fingerprint

resolve historical NextActionContextRefV1
→ verify owner payload/fingerprint
→ verify owner issuance valid at terminal/admission relevant boundary

compare body:
priority_class
critical_path_ordinal
context_slot_id
project/task binding

all exact equal

→ normalized derived memory content
→ MCF_V1
```

Caller declaration fields remain:

```text
locator/equality claims only
```

No caller priority authority.

Freeze exact normalized memory object.

Recommended:

```json
{
  "context_ref": "...",
  "context_fingerprint": "...",
  "priority_class": "...",
  "critical_path_ordinal": 1,
  "context_slot_id": "..."
}
```

If more fields are needed, list them exactly.

---

# 13. lineage and applicability

Freeze owner-derived:

```text
subject_key
applicability_key
semantic_slot
```

Recommended:

```text
subject_key
→ context_ref_id or exact stable owner logical ID

applicability_key
→ TaskContract scope + policy ID

semantic_slot
→ next-action-context/{context_payload_schema_id}/{context_slot_id}
```

No caller free-text atoms.

Current applicability requires both:

```text
source P1-6 current applicability rule
AND
NextActionContext owner currentness
AND
Memory policy currentness
```

Historical memory replay uses original as-of validity, not currentness now.

---

# 14. selection-time priority authority

Freeze exact relation:

```text
CURRENT NEXT_ACTION_CONTEXT ProjectMemoryEntry

owner-derived priority_class
owner-derived critical_path_ordinal
selection-time memory applicability high-watermark

→ NextActionSelectionPolicy ranks 4-6
```

Exact class mapping:

```text
ACCEPTED_CORE_CRITICAL_PATH
→ rank 4

OPERATIONAL_HARDENING
→ rank 5

OPTIONAL_OPTIMIZATION
→ rank 6
```

No other class in this source contract.

---

# 15. critical-path ordinal distinction

Resolve this explicitly for the later prerequisite rework.

Required preferred semantics:

```text
source-memory critical_path_ordinal
→ authoritative ranking input for CYCLE_DERIVED

descriptor critical_path_ordinal
→ catalog-local tie-break metadata only
```

If descriptor field should be renamed in later runtime design:

```text
freeze the new semantic name now
```

such as:

```text
descriptor_catalog_ordinal
```

Do not use two fields both called critical-path ordinal with different authority.

---

# 16. historical replay

Freeze exact historical proof.

For an existing AdmittedCycle/ProjectMemory:

```text
original P1-8 Memory policy payload/as-of validity
original P1-6 historical structured evidence provenance
original NextActionContextRefV1 payload/fingerprint
owner event history through original high-watermark

→ rederive exact structured result semantic equality
→ MCF_V1
→ MemoryLineageKey
```

Later context revocation/supersession:

```text
does not corrupt historical memory
```

but may withdraw current applicability.

For historical NextActionSelection:

```text
memory was CURRENT at original selection high-watermark
priority_class/ordinal rederived from same historical context authority
```

---

# 17. current invalidation

Freeze current projection reaction:

```text
NextActionContext REVOKED
or superseded under WITHDRAW_CURRENT

→ append ProjectMemoryAuthorityEvent
→ current NEXT_ACTION_CONTEXT memory withdrawn

→ append/derive NextAction current withdrawal if current selection depended on it
```

Historical Cycle/Memory/Selection remain immutable.

---

# 18. no authority laundering

Mandatory negatives:

```text
producer writes priority_class in admitted JSON
without matching context owner ref
→ DENY

caller supplies context_ref/fingerprint
that does not exist
→ DENY

caller supplies correct ref but different class/ordinal
→ DENY

P1-8 constructs context owner object
→ forbidden

P1-6 durable body alone
→ insufficient semantic priority authority

Markdown NEXT_ACTIONS text
→ insufficient runtime source authority
```

---

# 19. migration/cut-line design only

Do not implement.

Freeze later persistence needs, likely exact equivalents of:

```text
next_action_context_refs
next_action_context_authority_events
```

Owner domain:

```text
external Command Center / Task authority
```

P1-8 persistence stores only:

```text
refs/fingerprints/high-watermarks needed for verification/projection
```

unless existing owner storage is shared by read port.

No retroactive backfill.

Existing accepted Cycles without this prospective context source:

```text
remain historical
cannot be retroactively given NEXT_ACTION_CONTEXT by caller
```

---

# 20. exact questions

Candidate design/report must answer:

1. Who exactly owns `NextActionContextRefV1`?
2. Why is that owner not P1-6 or P1-8?
3. Is V1 scope TaskContract-only?
4. What exact immutable fields define the context ref?
5. What is the exact context fingerprint formula?
6. What are the exact `priority_class` values?
7. What are the exact bounds/meaning of `critical_path_ordinal`?
8. What exact owner event object represents issue/supersede/revoke?
9. How is the live owner capability hidden?
10. What exact P1-6 structured-result schema carries the context?
11. What exact EvidenceRequirement enrollment is required?
12. Does existing P1-6 Requirement schema suffice without a new semantic-contract fingerprint? Why?
13. What exact P1-8 selector/derivation/MCF object is used?
14. What exact lineage atoms are owner-derived?
15. How is current applicability calculated?
16. How is CYCLE_DERIVED selection-time CURRENT state proven?
17. Which critical-path ordinal is authoritative vs descriptor tie-break?
18. What happens on context revocation?
19. What legacy data remains ineligible?
20. Are any further Human-owned choices open?

No implicit answer.

---

# 21. output status

Create candidate:

```text
.aiassistant/rules/
AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
```

Successful Executor submission:

```text
NEXT_ACTION_CONTEXT source authority design
→ CANDIDATE / HUMAN_REVIEW_REQUIRED

P1-8 prerequisite owner-authority design
→ still BLOCKED until this source design is Human-accepted and incorporated

P1-8 Runtime
→ BLOCKED_REQUIRED_EVIDENCE
```

If the design concludes P1-6 Requirement identity must gain a new semantic-contract field/fingerprint:

```text
STOP
→ P1_6_REQUIREMENT_SEMANTIC_CONTRACT_EXTENSION_REQUIRED
```

and do not invent that extension here.

---

# 22. Git policy

```text
NO runtime source/test/migration changes

NO git add
NO commit
NO push

final HEAD:
f4614198c2745944f7ec02639a45b0315bbc903d
```

Move Task active→done on Executor submission.

No canonical state update.

---

# 23. export

Target:

```text
.aiassistant/reports/target/
20260831_1514_aiscc-p1-8-next-action-context-source-authority-design-freeze-1/
```

Required:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
```

Include byte-preserving:

```text
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md

.aiassistant/records/aiscc/cycles/
20260831_1514_aiscc-p1-8-next-action-context-source-authority-baseline-gap-hold-1.cycle.md

done Task
```

Report blocked runtime hash inventory proving unchanged candidate identity.

---

# 24. preserved exact paths

Preserve after submission:

```text
.aiassistant/rules/AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md

.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md

.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md

.aiassistant/records/aiscc/cycles/
20260831_1514_aiscc-p1-8-next-action-context-source-authority-baseline-gap-hold-1.cycle.md

.aiassistant/tasks/done/
20260831_1514_aiscc-p1-8-next-action-context-source-authority-design-freeze-1.md
```
