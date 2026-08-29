# AISCC Evidence Admission Contract

## 1. document status

| field | value |
|---|---|
| document_id | `AISCC-P1-6-EVIDENCE-ADMISSION-V1-CANDIDATE` |
| task_id | `20260829_1026_aiscc-p1-6-checkpoint-human-ingress-and-optional-evidence-design-rework-1` |
| work_type | `DESIGN_REWORK` |
| result_status | `ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING` |
| authority_status | repository canonical design candidate; not accepted until Human review |
| design_base_commit | `c86e291f94bd9acc31e40bc78316132abfddd90b` |
| semantic owner | evidence requirement matching, candidate admission, admitted-evidence identity, set completeness, and P1-4 `G_EVIDENCE` attestation |
| implementation_status | `NOT_STARTED` |
| runtime/database verification | `NOT_EXECUTED` |

This document freezes the P1-6 implementation contract. It does not implement the evidence runtime,
change the P1-4 state machine, implement P1-7 Human/Judgment semantics, admit a Cycle, or claim Human
acceptance.

## 2. authority scope and non-substitution

P1-6 is the sole semantic owner of evidence admission. It consumes immutable, issuer-backed inputs
and decides whether one candidate satisfies one exact evidence requirement. It does not decide what
the work means and does not mutate workflow state.

```text
AgentOutput != EvidenceCandidate
P1-5 producer ref != EvidenceCandidate admission
EvidenceCandidate != AdmittedEvidence
AdmittedEvidence != Judgment
AdmittedEvidence != TransitionDecision
AdmittedEvidence != WorkflowState

EvidenceAdmissionDecision != SecurityAdmissionDecision
EvidenceAdmissionDecision != Judgment
EvidenceAdmissionDecision != TransitionDecision

EvidenceSetEvaluation(SATISFIED) != WorkflowState.ACCEPTED
G_EVIDENCE != G_HUMAN_*
G_EVIDENCE != G_JUDGMENT_*
```

An object is not authoritative merely because it is typed, persisted, content-addressed, reported as
`PASS`, or produced by an accepted runtime. P1-6 owns only the evidence facts defined here. P1-4
remains the TransitionDecision and WorkRun mutation owner; P1-7 remains the HumanGate, HumanResult,
and Judgment owner; P1-8 remains the Cycle, project closure, and NextAction owner.

## 3. exact domain vocabulary

### 3.1 exact enums

```text
EvidenceAdmissionOutcome
= ADMITTED | REJECTED

EvidenceSetOutcome
= SATISFIED | UNSATISFIED

RequirementSatisfaction
= SATISFIED | UNSATISFIED

EvidenceRequirementProfile
= EXECUTOR_REQUIRED | REUSE_ALLOWED | HUMAN_OWNED | NOT_REQUIRED | FORBIDDEN

RequirementObligation
= REQUIRED | NOT_REQUIRED | FORBIDDEN

HumanEvidenceProducerCategory
= HUMAN_DIRECT_EVIDENCE | HUMAN_P1_7

EvidenceSensitivity
= PUBLIC_SAFE | INTERNAL | PRIVATE_SENSITIVE | SECRET_FORBIDDEN

EvidenceDimensionOutcome
= PASS | FAIL | NOT_APPLICABLE
```

`PENDING` is not an `EvidenceAdmissionOutcome`. Transport or worker processing may expose a separate
`RECEIVED | EVALUATING | DECIDED` projection, but only the immutable `ADMITTED` or `REJECTED`
decision has admission authority.

### 3.2 exact typed records

The implementation must provide immutable typed equivalents of:

| concept | exact authority |
|---|---|
| `EvidenceCheckpoint` | immutable System/TaskContract-owned guard-use purpose, including exact source and target transition or non-transition use |
| `EvidenceCheckpointRef` | stable checkpoint identity/version reference; not derivable from WorkflowState alone |
| `EvidenceRequirement` | one versioned, System-issued predicate against which a candidate is evaluated |
| `EvidenceRequirementSet` | immutable snapshot of all applicable requirement directives for one TaskContract version |
| `EvidenceCandidate` | untrusted-until-admitted submission metadata bound to one immutable content or producer ref |
| `EvidenceCandidateRef` | stable reference to the candidate identity and fingerprint; not an admission |
| `EvidenceBodyRef` / `EvidenceContentRef` | owner-backed immutable body or content-addressed reference |
| `EvidenceAdmissionRequest` | immutable proposal to evaluate one candidate against one requirement in one current set |
| `EvidenceEvaluation` | all exact dimension results and evaluated authority versions |
| `EvidenceAdmissionDecision` | exactly `ADMITTED` or `REJECTED`, with durable reason and evaluation ref |
| `AdmittedEvidence` | immutable result of one admitted candidate-to-requirement mapping |
| `AdmittedEvidenceRef` | issuer-backed reference to that immutable mapping, not a set-completeness fact |
| `EvidenceRequirementSatisfaction` | exact per-requirement current mapping from effective admitted evidence |
| `EvidenceSetEvaluation` | current checkpoint-applicable completeness result under one run/state/version |
| `EvidenceSetSatisfactionAttestation` | P1-6 owner-bound proof that one exact checkpoint/set evaluation is satisfied |
| `EvidenceRejectionReason` | exact sanitized rejection taxonomy in section 9 |
| `EvidenceOwner` | authenticated producer/issuer identity and version |
| `EvidenceSemanticOwner` | policy authority that owns requirement/admission semantics; V1 value is `P1_6_EVIDENCE` |

Candidate persistence preserves provenance; it does not turn the candidate into evidence truth.

## 4. EvidenceRequirement and RequirementSet contract

### 4.1 EvidenceRequirement

Every `EvidenceRequirement` binds all of the following immutable fields:

```text
requirement_id
requirement_version
task_contract_id
task_contract_version
requirement_set_id
requirement_set_version
semantic_owner = P1_6_EVIDENCE
profile
obligation
applicable_checkpoint_refs or checkpoint_applicability_predicate_id/version
evidence_type_id / evidence_type_version
allowed_issuer_types
allowed_issuer_ids / minimum issuer versions
content_kind and content-owner constraints
content schema/format/hash algorithm constraints
subject identity and scope selector
resource selector when applicable
freshness policy
applicability policy
coverage policy
reuse policy
sensitivity policy
review/private/public export policy
issued_at / revoked_at / supersedes_requirement_ref
requirement fingerprint
```

Requirement identity is System/server-owned. Agent, Executor, public input, provider output, tool
output, and candidate metadata cannot add, remove, weaken, reinterpret, or select a requirement. A
new requirement version is a new immutable predicate. It does not reinterpret an admission made
under an older TaskContract or RequirementSet.

The exact normalized obligation mapping is:

| profile | obligation | completeness effect |
|---|---|---|
| `EXECUTOR_REQUIRED` | `REQUIRED` | must have a current admitted mapping from an allowed Executor/System producer |
| `REUSE_ALLOWED` | `REQUIRED` | must have a new current-task admission; the candidate may reference compatible prior admitted evidence |
| `HUMAN_OWNED` | `REQUIRED` | must have a current admission from an exact Human producer category explicitly allowed by the requirement |
| `NOT_REQUIRED` | `NOT_REQUIRED` | excluded from required completeness; no synthetic admitted row |
| `FORBIDDEN` | `FORBIDDEN` | matching candidates are rejected; no admitted mapping may exist |

`RequirementObligation` is a derived normalization of the exact five profiles, not another
TaskContract input profile. There is no additional obligation or supplemental-requirement mode in
V1. Material not required by an explicit current requirement may be retained only as an untrusted
candidate and append-only submission provenance. It cannot become `AdmittedEvidence`, create a
satisfaction row, affect `EvidenceSetEvaluation`, enter any evidence-set root, or contribute to
`G_EVIDENCE`.

### 4.2 EvidenceCheckpoint and checkpoint applicability

An `EvidenceCheckpoint` is issued and owned only by the System TaskContract authority. It is derived
from the current TaskContract plus the requested P1-4 transition or exact guard-use context; a
caller cannot provide arbitrary checkpoint metadata and the System cannot infer a checkpoint from
WorkflowState alone. Every checkpoint binds:

```text
checkpoint_id / checkpoint_version
task_contract_id / task_contract_version
source WorkflowState
exactly one of:
  target WorkflowState
  transition_purpose_id / transition_purpose_version
guard_id = G_EVIDENCE
requirement_set_id / requirement_set_version
System TaskContract authority id/version
issued_at / revoked_at / supersedes_checkpoint_ref
checkpoint fingerprint
```

The two exact V1 lifecycle purposes are `PRE_HUMAN_EVIDENCE` and `POST_HUMAN_EVIDENCE`. A versioned
TaskContract may issue more exact purposes, but every purpose is a new System-owned identity rather
than free text. The same Task/run/WorkflowState/state_version evaluated for two different
checkpoints has two different evidence authorities; neither its set evaluation nor attestation is
interchangeable.

Every requirement has either an explicit finite `applicable_checkpoint_refs` set or a System-owned,
versioned checkpoint-applicability predicate. The predicate receives the immutable checkpoint, not
caller metadata. A requirement may apply to more than one checkpoint only when that sharing is
explicit in the issued requirement version. A requirement ignored at checkpoint X remains in the
full immutable RequirementSet; it is not rewritten, removed, or globally reclassified as
`NOT_REQUIRED`.

### 4.3 EvidenceRequirementSet

`EvidenceRequirementSet` binds:

```text
requirement_set_id / requirement_set_version
task_contract_id / task_contract_version
ordered exact requirement refs
requirement fingerprints and canonical requirement root hash
ordered exact checkpoint refs and checkpoint fingerprints
semantic owner / authority version
issued_at / revoked_at / supersedes_set_ref
```

The snapshot is immutable. Exactly one unsuperseded set version is current for a TaskContract version
and WorkRun admission context. Set selection is System-owned; a request cannot supply an arbitrary
catalog version. Missing, ambiguous, revoked, or stale set authority fails closed.

For checkpoint evaluation, P1-6 derives an ordered applicable subset from the immutable full set and
the exact checkpoint. It commits both the full requirement root and a checkpoint-subset root; it
does not issue a modified RequirementSet profile.

## 5. exact evidence profile semantics

### 5.1 EXECUTOR_REQUIRED

The Task cannot satisfy this requirement without a P1-6-admitted candidate from an explicitly
allowed Executor or System proof producer. Executor report prose is not evidence unless the exact
requirement permits that report artifact/type and its exact body, issuer, hash, scope, and provenance
are admitted. A process exit code or `PASS` string alone is insufficient.

### 5.2 REUSE_ALLOWED

Reuse is never automatic. A prior `AdmittedEvidenceRef` is only a current candidate source. A new
current-task reuse admission is allowed only when every gate passes:

```text
same semantic requirement and compatible requirement version
compatible TaskContract/version under an explicit compatibility rule
same subject, scope, and resource
allowed original issuer and current reuse issuer
freshness and applicability still valid
immutable content and exact hash identity
no revocation, supersession, or correction conflict
positive remaining reuse count and policy
new current-task request/evaluation/decision
```

The old set-satisfaction attestation is never replayed. Compatibility must be explicit; similarity,
same filename, same bytes alone, or Human/Agent prose cannot establish it.

### 5.3 HUMAN_OWNED

Executor, Agent, provider, tool, P1-6 service, and P1-4 kernel cannot satisfy this requirement. Only
an authenticated Human producer category explicitly allowed by the requirement may submit it. The
exact V1 categories are `HUMAN_DIRECT_EVIDENCE` and `HUMAN_P1_7`; neither implies the other. A
requirement that names `HUMAN_P1_7` cannot be satisfied by `HUMAN_DIRECT_EVIDENCE`. P1-6 may verify
and admit evidence integrity/provenance but cannot fabricate Human action, open or resolve a
HumanGate, create a HumanResult, or create a Judgment. At a checkpoint where the requirement is
applicable, it remains `UNSATISFIED` until an allowed exact Human producer input is admitted.

### 5.4 NOT_REQUIRED

The current TaskContract requires no evidence item for this directive. It creates no satisfaction
row and no synthetic `AdmittedEvidence`. A candidate submitted against it is rejected as
`NOT_APPLICABLE`; absence is not evidence.

### 5.5 FORBIDDEN

A candidate matching the forbidden type, source, content, sensitivity, or scope is rejected
fail-closed as `FORBIDDEN_EVIDENCE`. Existing or useful content receives no exception. The rejection
cannot satisfy another requirement. Set evaluation records the prohibition as clear only when no
effective admitted mapping violates it; a historical conflicting admission creates an authority
conflict and makes the set `UNSATISFIED` until additive revocation/supersession is resolved.

## 6. producer and issuer authority

### 6.1 exact V1 issuer categories

```text
P1_5_EXECUTION_SUBMISSION
P1_5_AGENT_OUTPUT
P1_5_TOOL_OUTPUT
P1_5_EXECUTION_ARTIFACT
SYSTEM_STATIC_PROOF
SYSTEM_BUILD_PROOF
SYSTEM_DATABASE_OBSERVATION
SYSTEM_RUNTIME_OBSERVATION
HUMAN_DIRECT_EVIDENCE
HUMAN_P1_7
PRIOR_ADMITTED_EVIDENCE
```

Every category requires an injected owner-specific verifier. Absence, unknown issuer, unverifiable
version, or a verifier that can mint another owner's record is fail-closed.

P1-5 issuer-backed `ExecutionSubmissionRef`, `AgentOutputRef`, `ToolOutputRef`, and
`ExecutionArtifactRef` may seed a candidate only after the P1-5 authority verifies their exact
identity, run/attempt, TaskContract, state/version where present, content/event hash, and issuer
version. This verifies producer provenance, not evidence sufficiency.

System proof issuers bind the exact runner/harness identity and version, implementation commit,
Task/run/attempt when applicable, command or observation specification, environment/config/image/DB
versions required by the requirement, and immutable result body. A caller-created DTO, raw claim, or
test name is not a System proof.

`HUMAN_DIRECT_EVIDENCE` requires the Manual Command Center ingress authority and authenticated Human
principal binding in section 6.2. `HUMAN_P1_7` requires the future P1-7 owner verifier and designated
Human identity/gate/result binding named by the requirement. A verifier for either category cannot
mint or verify the other. `PRIOR_ADMITTED_EVIDENCE` requires the P1-6 authority that issued the old
admission plus the full reuse evaluation in section 5.2.

### 6.2 pre-P1-7 HUMAN_DIRECT_EVIDENCE ingress

`HUMAN_DIRECT_EVIDENCE` is a narrow Manual Command Center evidence ingress available before P1-7.
Its server-issued immutable ingress record binds:

```text
authenticated Human principal/operator identity
ingress authority id/version
task_contract_id / task_contract_version
work_run_id
checkpoint_id / checkpoint_version
evidence_type_id / evidence_type_version
subject identity / scope selector / resource identity
content kind / owner-backed ref / exact hash
provided_at
ingress record id/version/fingerprint and issuer authenticity
```

The Human supplies content through an authenticated channel, but the server-owned ingress authority
issues the record; a caller boolean such as `human=true`, display name, role claim, raw path, or hash
is not authority. The record undergoes the same exact requirement, issuer, content, checkpoint,
freshness, applicability, sensitivity, admission, and anti-replay evaluation as every other
candidate. It is not a `HumanGate`, `HumanResult`, `Judgment`, `G_HUMAN_*`, or `G_JUDGMENT_*` fact and
cannot satisfy a requirement restricted to `HUMAN_P1_7`.

### 6.3 EvidenceCandidate minimum fields

```text
candidate_id / candidate_version
candidate_fingerprint
issuer_type / issuer_id / issuer_version / issuer_authority_ref
producer work_run_id / execution_attempt_id / operation_id when applicable
task_contract_id / task_contract_version
checkpoint_id / checkpoint_version
observed WorkflowState / state_version when applicable
subject_id / scope_id / resource identity
evidence_type_id / evidence_type_version
content_kind / content_ref / content_owner_ref
content_hash_algorithm / content_hash / byte_count
schema_id / schema_version
created_at / observed_at
sensitivity classification
producer attestation/signature ref
human producer category / Human ingress record ref when applicable
prior_admitted_evidence_ref when reuse is requested
```

Raw path, URL, hash, display name, report claim, or file existence is locator/metadata only and is
not a trusted producer. `test says PASS != test evidence admitted`.

## 7. content, body, and reference authority

### 7.1 supported exact content kinds

```text
INLINE_CANONICAL_STRUCTURED_BODY
CONTENT_ADDRESSED_ARTIFACT_REF
P1_5_IMMUTABLE_PRODUCER_REF
DATABASE_OBSERVATION_REF
RUNTIME_OBSERVATION_REF
HUMAN_STRUCTURED_REF
PRIOR_ADMITTED_EVIDENCE_REF
```

`EvidenceContentRef` binds content kind, owner/store authority, immutable object identity/version,
canonicalization/schema, byte count, exact lowercase SHA-256, sensitivity, retention, and access
policy. The content owner must prove that the referenced bytes are immutable or version-addressed.

Inline structured bodies use the schema's exact canonical JSON encoding before hashing. Artifact or
blob evidence hashes the exact raw bytes. Database/runtime observations use an issuer-backed
immutable observation body plus environment and observation-spec fingerprint. Producer refs verify
their P1-5 identity and then resolve only through the registered P1-5 authority. A prior admission
resolves through P1-6 and still undergoes current reuse admission.

The evaluator must verify the exact chain:

```text
resolved immutable bytes or structured content
-> canonicalization required by the evidence type
-> exact SHA-256 and byte count
-> expected schema/format/type/classification
-> owner-backed immutable reference
```

The following are never sufficient:

```text
unverified arbitrary local path or URL
mutable latest pointer
hash string without owner-backed body/ref
Executor summary without the raw/supporting body required by the requirement
private content exposed in a public export to make verification convenient
```

Private content may remain in a private evidence store while durable admission records preserve only
the immutable metadata/hash/ref needed for verification. Reference unavailability is
`CONTENT_MISSING`, not permission to infer the body.

## 8. exact admission evaluation

### 8.1 dimensions

Every `EvidenceEvaluation` contains one explicit result for every dimension below:

```text
REQUIREMENT_MATCH
ISSUER_AUTHORITY
TYPE
TASK_CONTRACT_BINDING
CHECKPOINT_BINDING
HUMAN_PRODUCER_CATEGORY
SUBJECT_SCOPE
RESOURCE_BINDING
CONTENT_INTEGRITY
SCHEMA_FORMAT
FRESHNESS
APPLICABILITY
COVERAGE
SENSITIVITY_POLICY
REUSE_POLICY
REVOCATION_SUPERSESSION
DUPLICATE_IDEMPOTENCY
```

Each result records `PASS`, `FAIL`, or policy-explicit `NOT_APPLICABLE`, the evaluated authority ref
and version, and a sanitized reason. `NOT_APPLICABLE` is legal only when the requirement explicitly
declares that dimension irrelevant; unknown or ambiguous is `FAIL`. A candidate is `ADMITTED` only
when every required dimension passes and every permitted not-applicable result is exact.

No score, confidence, LLM review, Agent semantic classification, or majority result can replace a
dimension. An LLM/Agent may propose metadata only. V1 has no semantic-verifier exception.

### 8.2 admission order

The evaluator follows this fail-closed order and records all safely evaluable dimensions without
performing external side effects:

```text
load current TaskContract, EvidenceCheckpoint, and RequirementSet authority
-> immutable request identity/idempotency check
-> exact requirement/profile lookup and checkpoint applicability
-> issuer and producer-ref verification
-> task/run/subject/scope/resource binding
-> resolve immutable content privately
-> hash/schema/type/classification checks
-> freshness/applicability/coverage
-> reuse/revocation/supersession
-> immutable EvidenceEvaluation
-> immutable ADMITTED or REJECTED decision
-> when admitted, immutable AdmittedEvidence + per-requirement mapping atomically
```

A rejection creates no `AdmittedEvidence` and no satisfaction mapping.

## 9. decision and rejection taxonomy

`EvidenceAdmissionDecision.outcome` is exactly `ADMITTED` or `REJECTED`. An admitted decision uses
the non-rejection code `ADMITTED`. A rejected decision uses exactly one primary V1
`EvidenceRejectionReason` and may carry ordered secondary dimension failures.

```text
UNKNOWN_REQUIREMENT
REQUIREMENT_VERSION_MISMATCH
CHECKPOINT_MISMATCH
FORBIDDEN_EVIDENCE
ISSUER_NOT_AUTHORIZED
HUMAN_PRODUCER_CATEGORY_MISMATCH
TASK_CONTRACT_MISMATCH
SUBJECT_SCOPE_MISMATCH
RESOURCE_MISMATCH
TYPE_MISMATCH
CONTENT_MISSING
CONTENT_HASH_MISMATCH
SCHEMA_INVALID
STALE
NOT_APPLICABLE
INSUFFICIENT_COVERAGE
REUSE_NOT_ALLOWED
REUSE_INCOMPATIBLE
REVOKED_OR_SUPERSEDED
HUMAN_OWNED_REQUIRED
DUPLICATE_IDENTITY_CONFLICT
AUTHORITY_CONFLICT
```

The decision records request/evaluation/candidate/requirement/set refs, exact evaluated versions,
outcome, reason, admitting authority version, and timestamp. Reasons and public projections are
sanitized: no raw secret, private body, private path, credential identifier, or unsanitized error.

## 10. evidence-set completeness

### 10.1 per-requirement mapping

One `AdmittedEvidence` satisfies exactly one requirement mapping. The same immutable content or
candidate may satisfy multiple requirements only through separate request/evaluation/decision and
`AdmittedEvidence` identities for each requirement. Each mapping records exact coverage. Hidden
fan-out is forbidden.

`EvidenceRequirementSatisfaction` is derived from currently effective, applicable, non-revoked
admissions:

```text
all exact coverage predicates met -> SATISFIED
otherwise -> UNSATISFIED
```

Multiple items may jointly satisfy a requirement only when its versioned coverage rule explicitly
defines the finite composition and every contributing ref is recorded. A single item never satisfies
the whole set merely because its producer or type is trusted.

### 10.2 exact set algorithm

Under one transaction/serialization boundary, `EvidenceSetEvaluation` binds the current TaskContract,
WorkRun state/version, exact EvidenceCheckpoint, current RequirementSet, and effective evidence
authority version, then:

1. resolves the checkpoint-applicable subset from the immutable full set and records the full-set
   root plus the checkpoint-subset root;
2. evaluates every checkpoint-applicable `EXECUTOR_REQUIRED`, `REUSE_ALLOWED`, and `HUMAN_OWNED`
   requirement as exactly `SATISFIED` or `UNSATISFIED`;
3. excludes checkpoint-applicable `NOT_REQUIRED` from required rows and requires no admitted
   evidence for it;
4. verifies every checkpoint-applicable `FORBIDDEN` directive has no effective admitted violating
   mapping;
5. ignores non-applicable obligations for this checkpoint's completeness while retaining their
   immutable definitions in the full set;
6. computes the ordered applicable requirement-result root and admitted-ref/coverage root;
7. returns `SATISFIED` only if every applicable required row is satisfied and every applicable
   prohibition is clear.

Therefore:

```text
missing executor_required -> UNSATISFIED
missing human_owned -> UNSATISFIED
rejected forbidden candidate -> satisfies nothing
not_required -> no row required
reuse_allowed -> new current-task reuse admission required
one missing required row -> whole set UNSATISFIED
same state/version + different checkpoint -> distinct evaluation and authority
```

An `UNSATISFIED` set evaluation is durable evidence-state provenance but cannot mint a satisfied
guard fact.

The normative Human lifecycle is checkpointed without changing the RequirementSet profile:

```text
PRE_HUMAN_EVIDENCE checkpoint
  executor/static/runtime requirements applicable
  final HUMAN_OWNED requirement not applicable to this checkpoint
  applicable subset may become SATISFIED and issue G_EVIDENCE(PRE_HUMAN_EVIDENCE)

P1-7 Human handling
  P1-6 does not open, resolve, cancel, or project a HumanGate

POST_HUMAN_EVIDENCE checkpoint
  final HUMAN_OWNED requirement applicable and REQUIRED
  exact allowed Human producer input must be admitted
  applicable subset may then become SATISFIED and issue G_EVIDENCE(POST_HUMAN_EVIDENCE)
```

Ignoring the final Human requirement at the pre-Human checkpoint prevents circular admission; it
does not satisfy, waive, delete, or reclassify that requirement for the post-Human checkpoint.

## 11. owner-bound P1-4 G_EVIDENCE handoff

### 11.1 EvidenceSetSatisfactionAttestation

P1-6 may issue an attestation only from a current `EvidenceSetEvaluation(outcome=SATISFIED)`. It binds:

```text
attestation_id / attestation_version
evidence_set_evaluation_id / evaluation_version
task_contract_id / task_contract_version
work_run_id
checkpoint_id / checkpoint_version / checkpoint fingerprint
source WorkflowState / authoritative state_version observed
exactly one target binding:
  target WorkflowState
  transition_purpose_id / transition_purpose_version
guard_id = G_EVIDENCE
requirement_set_id / requirement_set_version / full requirement root hash
ordered applicable requirement refs / checkpoint-subset root hash
ordered admitted-evidence refs / coverage mappings / admitted-ref hash root
satisfied = true
evidence_authority_version
issued_at
expires_at = earliest applicable freshness expiry, otherwise null
P1_6 authority id/version and issuer authenticity
```

For `G_EVIDENCE`, `TransitionRequest.evidence_refs` is the exact one-element tuple containing the
current `EvidenceSetSatisfactionAttestationRef`. Raw `AdmittedEvidenceRef` values, candidate refs, a
set evaluation ID, or an old attestation are invalid. The attestation internally commits to the
full immutable set, exact checkpoint subset, and complete admitted-ref/coverage roots.

The P1-6 guard authority may issue only:

```text
TrustedGuardFact(
  guard_id = G_EVIDENCE,
  semantic_owner = P1_6_EVIDENCE,
  satisfied = true,
  reason = P1_6_EVIDENCE_SET_SATISFIED,
  authority_ref = exact attestation ref,
  bound_refs = TransitionRequest.evidence_refs,
  exact TaskContract/work_run/source state/state_version/target-or-use/checkpoint bindings
)
```

Its private issuer handle is recognized only by an injected `FutureOwnerGuardVerifier` whose
semantic owner is `P1_6_EVIDENCE`. P1-4 verifies issuer authenticity, exact request bindings, current
Task/run/source state/state_version, target transition or exact use purpose, checkpoint/version,
current RequirementSet and evidence-authority versions, non-revocation, expiry, satisfied set
evaluation, full-set root, checkpoint-subset root, and admitted-ref/coverage root before accepting
`G_EVIDENCE`.

The P1-6 owner verifier must be request-aware. The current P1-4
`FutureOwnerGuardVerifier.recognizes(fact)` shape is insufficient by itself because it cannot compare
the attestation's source/target/use binding with the complete `TransitionRequest`. P1-6
implementation therefore narrowly extends the injected owner-verifier handoff to receive the exact
request (or an equivalent immutable request fingerprint) while preserving P1-4 ownership and the
exact transition matrix. Profile-version equality, matching state/version alone, or an authentic
issuer token cannot substitute for checkpoint and target/use equality.

An attestation issued for one checkpoint cannot authorize another checkpoint or transition even
when TaskContract, WorkRun, WorkflowState, state_version, RequirementSet, admitted evidence, and
authority version are otherwise identical. A pre-Human attestation cannot be rebound as a
post-Human attestation.

The current P1-4 matrix consumes `G_EVIDENCE` on exactly
`ADMISSION_PENDING -> ACCEPTED` and `HUMAN_REQUIRED -> ACCEPTED`. A
`PRE_HUMAN_EVIDENCE` purpose attestation for a Task that requires later Human handling records exact
evidence readiness but is not inserted into a transition pair that does not require `G_EVIDENCE`,
does not open a HumanGate, and cannot authorize state mutation. A `POST_HUMAN_EVIDENCE` attestation
for `HUMAN_REQUIRED -> ACCEPTED` is a distinct request-bound guard input. This reconciles one guard
ID with multiple checkpoint/use identities without changing any P1-4 state or transition pair.

P1-6 cannot mint or substitute:

```text
G_CURRENT
G_CONTRACT / G_SCOPE / G_RUNTIME_CONTEXT
G_EXECUTION_STARTED / G_EXECUTOR_SUBMISSION
G_HUMAN_*
G_JUDGMENT_*
G_BLOCKER / G_BLOCKER_RESOLVED / G_REWORK_SPEC / G_FAILURE_TERMINAL
TransitionDecision
WorkflowState or state_version mutation
```

The exact nine WorkflowStates and 22 P1-4 transition pairs remain unchanged.

### 11.2 cross-contract consistency matrix

| fact | P1-4 | P1-6 result |
|---|---|---|
| `G_EVIDENCE` owner | future owner `P1_6_EVIDENCE` | `MATCH`: P1-6 alone evaluates checkpoint-applicable evidence and issues the owner-bound attestation |
| checkpoint/purpose binding | exact transition/use context must reach the future-owner verifier | `MATCH`: System TaskContract authority fixes checkpoint/version, source, target/use, guard, and RequirementSet; state/version alone is insufficient |
| Human gate ownership | P1-7 owns `HumanGate`, `HumanResult`, and `G_HUMAN_*` | `NOT ABSORBED`: P1-6 creates none of them |
| pre-Human evidence completeness | consumes only the exact checkpoint-bound guard fact when the matrix requires it | `NO DEADLOCK`: post-Human `HUMAN_OWNED` evidence remains in the full set but is not applicable to pre-Human completeness |
| post-Human evidence completeness | rejects wrong/missing future-owner guard facts | `NO SUBSTITUTION`: post-Human completeness requires its applicable exact Human evidence; pre-Human proof cannot substitute |
| Human direct evidence | no HumanResult/Judgment authority is delegated to P1-6 | `NOT HumanResult/Judgment`: direct ingress is evidence only and cannot mint Human/Judgment guards |
| exact five profiles | Task evidence vocabulary is consumed without reinterpretation | `MATCH`: exactly `EXECUTOR_REQUIRED`, `REUSE_ALLOWED`, `HUMAN_OWNED`, `NOT_REQUIRED`, `FORBIDDEN` |
| transition authority | P1-4 owns the exact 22-pair matrix, `TransitionDecision`, and atomic mutation | `NOT ABSORBED`: P1-6 issues evidence authority only |

## 12. concurrency, idempotency, and anti-replay

`EvidenceAdmissionRequest` binds:

```text
admission_request_id
candidate_id and candidate fingerprint
requirement_id/version and requirement fingerprint
requirement_set_id/version and root
task_contract_id/version
work_run_id
checkpoint_id/version and checkpoint fingerprint
observed source WorkflowState/state_version
target WorkflowState or exact transition-purpose identity
requested reuse ref when applicable
requester/ingress identity and created_at
canonical request fingerprint
```

Exact rules:

- same request ID plus same fingerprint returns the same immutable evaluation/decision/admission;
- same request ID plus different fingerprint is `DUPLICATE_IDENTITY_CONFLICT` and creates no new
  admission;
- concurrent requests for the same logical candidate/requirement/task/run admit at most one
  authoritative `AdmittedEvidence`; exact duplicates resolve to it;
- requirement-set, TaskContract, candidate, content, and issuer versions are reloaded under the
  admission serialization boundary; stale versions reject;
- admission append, admitted row, and satisfaction mapping are atomic;
- set evaluation reads a serialized current authority snapshot; a satisfied evaluation and its
  attestation are atomic;
- candidate admission does not mutate `WorkRun.state_version`;
- a new Task or state/version-scoped context requires a new admission/set evaluation as dictated by
  freshness policy. An old set attestation is never replayable.
- a different checkpoint, source, target, or guard-use purpose requires a distinct set evaluation
  and attestation even if Task/run/state/version and evidence bytes are identical;
- request-aware P1-6 verification rejects an authentic attestation presented for the wrong
  checkpoint, target transition, or exact use purpose before P1-4 can accept `G_EVIDENCE`.

## 13. persistence, append-only provenance, and restart

The production direction is PostgreSQL with SQLAlchemy 2 async/asyncpg and an Alembic forward-only
migration, consistent with accepted P1-3/P1-4/P1-5. The minimum durable entities are:

```text
EvidenceRequirementRow
EvidenceRequirementSetRow and ordered membership snapshot
EvidenceCheckpointRow and immutable TaskContract/checkpoint membership snapshot
EvidenceCandidateRow and immutable content/ref metadata
HumanDirectEvidenceIngressRow when applicable
EvidenceAdmissionRequestRow
EvidenceEvaluationRow and dimension-result rows/body
EvidenceAdmissionDecisionRow
AdmittedEvidenceRow
EvidenceRequirementSatisfactionRow
EvidenceSetEvaluationRow
EvidenceSetSatisfactionAttestationRow
EvidenceAuthorityEventRow for revocation/supersession/correction
current evidence-authority and set-satisfaction projections
```

Append-only provenance includes requirements/set/checkpoint versions, direct-Human ingress records,
candidates, requests, evaluations, decisions, admitted mappings, set evaluations/attestations,
rejections, and every authority event. Current projections are derived caches protected by
sequence/version CAS. An admitted body/hash/ref, evaluation, decision, or mapping is never mutated
in place.

The admission transaction atomically appends request/evaluation/decision and, only for `ADMITTED`,
the admitted mapping. The set transaction atomically appends the set evaluation and, only for
`SATISFIED`, its attestation. Unavailable private body storage cannot be represented as a successful
metadata-only admission unless the requirement explicitly authorizes an owner-backed reference and
that reference verifies.

Restart reconstructs the current requirement set, checkpoint catalog and applicability, effective
admissions, revocation/supersession lineage, per-checkpoint requirement satisfaction, full-set and
subset roots, set evaluation, authority version, and valid attestations from ordered provenance,
then compares stored projections. Missing/partial/orphaned events, illegal lineage, hash/root
mismatch, conflicting identity, or projection disagreement fails closed with no auto repair and no
inference from report prose or last process state.

## 14. revocation, supersession, and correction

`AdmittedEvidence` remains immutable historical truth about the past admission decision. Change uses
an additive event:

```text
REVOKED        -> exact evidence is no longer effective after the event
SUPERSEDED     -> named new admitted evidence replaces it for named requirement mappings
CORRECTED      -> named new candidate/admission corrects content or metadata; old record remains
REQUIREMENT_SET_SUPERSEDED -> a new set snapshot replaces the old current set
```

Every event binds owner, authority version, reason, affected refs/mappings, Task/run scope, and time.
Revoking or superseding a currently contributing item increments the evidence-authority version,
invalidates affected current satisfaction and every attestation that committed to the old version or
root, and requires a new set evaluation before another `G_EVIDENCE` fact can be issued.

Revocation does not rewrite a prior P1-4 transition or mutate WorkflowState. It may become input to a
separate future governance request owned by P1-4/P1-7/P1-8. P1-6 itself cannot roll back state.

## 15. freshness and applicability

Freshness is requirement-owned and may be a conjunction of these exact V1 policy categories:

| category | exact binding |
|---|---|
| `IMMUTABLE_BUILD_ARTIFACT` | exact content hash, build recipe/toolchain/config/source identity; no time-only expiry unless explicitly added |
| `TASK_EXECUTION_SCOPED` | exact TaskContract/run/attempt and permitted execution lineage |
| `WORKRUN_STATE_VERSION_SCOPED` | exact WorkRun state and state_version at observation/admission/use |
| `TIME_WINDOW` | observed-at plus a positive finite policy duration and trusted clock |
| `CONFIG_VERSION_SCOPED` | exact policy/profile/schema/image/database/config versions named by the requirement |
| `HUMAN_RESULT_SCOPED` | exact P1-7 Human producer/gate/result version and applicability; P1-6 does not create it |

```text
fresh timestamp != fresh evidence
same bytes != applicable evidence when scope/version changed
immutable content != current runtime observation
```

After a WorkRun state/version change, `WORKRUN_STATE_VERSION_SCOPED` evidence and its attestation are
stale. Other evidence survives only if its exact requirement permits the new context and every
Task/run/config/resource/applicability binding still passes. P1-6 never silently rebinds an old
observation to a new state/version; it requires a new admission or current reuse admission.

Applicability independently evaluates TaskContract version, run lineage, current state/version,
checkpoint identity/version and source/target/use purpose, subject/scope/resource, configuration,
mode, and any bounded time window named by the requirement. Requirement checkpoint applicability
is evaluated before completeness; it is never inferred from current WorkflowState alone.

## 16. Human-owned evidence boundary

P1-6 recognizes two non-interchangeable Human evidence producer categories:

```text
HUMAN_DIRECT_EVIDENCE
  Manual Command Center ingress before P1-7
  authenticated Human principal + server-issued ingress record
  never a HumanGate/HumanResult/Judgment fact

HUMAN_P1_7
  future P1-7 owner ingress
  designated Human identity and exact gate/result binding when named
  P1-7 verifier required
```

Every `HUMAN_OWNED` requirement explicitly names one or both allowed producer categories. P1-6
first verifies that exact category's issuer, then applies the same integrity, checkpoint,
provenance, type, scope, freshness, sensitivity, and admission rules. It never falls back from
`HUMAN_P1_7` to direct evidence and never treats authenticated Human identity alone as proof.

The boundary preserves:

```text
HumanResult != Judgment
Human evidence != HumanResult unless the requirement names that exact typed Human-produced artifact
HUMAN_DIRECT_EVIDENCE != HUMAN_P1_7
Admitted Human evidence != Judgment
HumanGateStatus.RESOLVED != evidence-set satisfaction
```

An admitted Human review artifact proves only the evidence predicate written in its requirement. It
does not infer `APPROVE`, create an authoritative Judgment, satisfy a Judgment guard, or mutate state.
P1-7 retains HumanGate/HumanResult admission and Judgment ownership. The direct ingress authenticates
Human principal/operator identity only for its exact evidence record; it does not pre-implement or
simulate P1-7. P1-6 implementation tests may use exact fake category-specific owner verifiers; those
fixtures are not production Human authority and cannot share a universal minting handle.

## 17. sensitivity, private storage, and export

| classification | admission/storage | review export | public/Replay export |
|---|---|---|---|
| `PUBLIC_SAFE` | immutable body/ref may be stored after schema/integrity and export-policy checks | exact body or ref metadata as allowed | only explicitly public-export-approved, sanitized content |
| `INTERNAL` | body/ref in access-controlled evidence storage | authorized review bundle may include exact body or controlled ref | metadata only when policy explicitly allows; body denied by default |
| `PRIVATE_SENSITIVE` | private encrypted/access-controlled body; durable admission keeps exact hash/ref/classification | metadata/hash/ref by default; body only through separate authorized private channel | body always forbidden |
| `SECRET_FORBIDDEN` | raw body is rejected and quarantined/destroyed according to security policy; never admitted | detector class and sanitized rejection metadata only | nothing derived from the raw value |

Raw secrets are never evidence bodies. A secret-boundary proof uses a non-secret canary verdict,
redacted metadata, owner-backed hash/reference, and non-exposure scan result—not the secret. A raw
secret fingerprint that would itself disclose or enable guessing is not retained as a public
content hash.

Redaction does not make the original content admissible. A sanitized derivative is a new candidate
with explicit source linkage, sanitizer identity/version, derivative hash, and its own evaluation.
Run visibility and public Replay visibility confer no private-evidence read authority.

## 18. normative contract examples

These examples apply only the explicit rules above; they add no hidden admission rule.

### 18.1 static/build proof

- requirement: `EXECUTOR_REQUIRED`, exact source commit, build command specification, toolchain and
  result schema, allowed issuer `SYSTEM_BUILD_PROOF`;
- candidate: issuer-backed build-run body containing command fingerprint, versions, exit/result,
  complete bounded logs/artifact refs and exact hash;
- evaluation: all bindings/integrity/schema/freshness/coverage pass;
- decision: `ADMITTED` for this build requirement only;
- set effect: this row becomes `SATISFIED`; other required rows remain independent;
- `G_EVIDENCE` effect: none until the whole current checkpoint-applicable subset is `SATISFIED`.

### 18.2 PostgreSQL migration proof

- requirement: `EXECUTOR_REQUIRED`, empty PostgreSQL database to exact Alembic head, DB engine and
  migration-set versions bound;
- candidate: `SYSTEM_DATABASE_OBSERVATION` with database fixture identity, migration command/result,
  schema/head observation and immutable sanitized body;
- evaluation: exact DB/migration/config/task scope and content pass;
- decision: `ADMITTED` for the migration requirement;
- set effect: migration row becomes `SATISFIED`;
- `G_EVIDENCE` effect: possible only after all remaining checkpoint-applicable required rows pass.

### 18.3 Docker/runtime security proof

- requirement: `EXECUTOR_REQUIRED`, exact image/policy/runtime scenario and
  `WORKRUN_STATE_VERSION_SCOPED` freshness;
- candidate: `SYSTEM_RUNTIME_OBSERVATION` bound to Docker engine/image digest, run/state/version,
  scenario, expected/actual assertions, resource inventory and private bounded logs;
- evaluation: issuer, runtime resource, state/version, content, coverage and private-export policy
  all pass;
- decision: `ADMITTED`;
- set effect: exact runtime-security row becomes `SATISFIED`;
- `G_EVIDENCE` effect: current checkpoint/set attestation may include its admission ref; a
  state/version or checkpoint change invalidates that attestation.

### 18.4 P1-5 ExecutionSubmissionRef

- requirement: `EXECUTOR_REQUIRED`, evidence type `EXECUTION_SUBMISSION_PROVENANCE`, exact Task/run,
  accepted P1-5 issuer version;
- candidate: P1-5-verified `ExecutionSubmissionRef` wrapped by P1-6 candidate ingress;
- evaluation: verifies issuer, `EXECUTOR_COMPLETED`, event-range hash, run/Task/state/version and the
  exact requirement; it does not infer test success or acceptance;
- decision: `ADMITTED` for submission provenance only;
- set effect: only the named submission row becomes `SATISFIED`;
- `G_EVIDENCE` effect: raw submission ref cannot mint it; the applicable checkpoint subset must pass.

### 18.5 reusable immutable artifact

- requirement: `REUSE_ALLOWED`, exact immutable artifact semantics, compatible TaskContract rule,
  subject/resource and config versions;
- candidate: `PRIOR_ADMITTED_EVIDENCE` ref plus exact original content hash and current reuse request;
- evaluation: original issuer/admission, compatibility, freshness, applicability, reuse count and
  non-revocation pass;
- decision: new current-task `ADMITTED` reuse mapping;
- set effect: current requirement becomes `SATISFIED`; the old row is unchanged;
- `G_EVIDENCE` effect: only a new current checkpoint/set attestation can include the new mapping.

### 18.6 Human-owned final review

- checkpoint: exact `POST_HUMAN_EVIDENCE` source and accepted-transition target/use binding;
- requirement: `HUMAN_OWNED`, exact `HUMAN_P1_7` producer and final-review artifact type;
- candidate: exact P1-7-verified Human structured ref or HumanResult ref when that exact type is named;
- evaluation: Human issuer/gate/result/Task/run/version, content integrity and applicability pass;
- decision: `ADMITTED` as evidence that the named Human input exists;
- set effect: Human-owned evidence row becomes `SATISFIED`;
- `G_EVIDENCE` effect: the post-Human checkpoint subset may become satisfied, but the artifact is not
  Judgment and cannot satisfy `G_JUDGMENT_*` or mutate workflow.

### 18.7 forbidden raw secret

- requirement: `FORBIDDEN`, sensitivity/content rule forbids raw credentials and secret material;
- candidate: any issuer submits a raw API key, credential body, or secret-bearing artifact;
- evaluation: `SENSITIVITY_POLICY=FAIL` and prohibition match;
- decision: `REJECTED(FORBIDDEN_EVIDENCE)`; raw body is not admitted/exported;
- set effect: candidate satisfies nothing; sanitized rejection provenance is retained;
- `G_EVIDENCE` effect: none.

### 18.8 stale runtime proof after state_version change

- requirement: `EXECUTOR_REQUIRED` with `WORKRUN_STATE_VERSION_SCOPED` freshness at `RUNNING/v12`;
- candidate: otherwise valid runtime observation captured at `RUNNING/v11`;
- evaluation: `FRESHNESS=FAIL` and applicability to v12 fails despite identical content;
- decision: `REJECTED(STALE)`;
- set effect: requirement remains `UNSATISFIED`;
- `G_EVIDENCE` effect: no attestation; any v11 attestation is invalid for the v12 request.

### 18.9 pre-Human checkpoint without circular Human evidence

- RequirementSet: executor static/runtime rows apply to `PRE_HUMAN_EVIDENCE`; final
  `HUMAN_OWNED` review remains in the full set but applies only to `POST_HUMAN_EVIDENCE`;
- evaluation: all pre-Human applicable required rows pass and applicable prohibitions are clear;
- decision: checkpoint subset is `SATISFIED` without waiving or reclassifying final Human evidence;
- `G_EVIDENCE` effect: P1-6 may issue only the exact pre-Human source/purpose-bound attestation;
- Human effect: P1-6 opens or resolves no HumanGate and creates no HumanResult or Judgment.

### 18.10 post-Human checkpoint requires Human-owned evidence

- checkpoint: exact `POST_HUMAN_EVIDENCE` source and target-transition binding;
- requirement: final `HUMAN_OWNED` evidence is now applicable and `REQUIRED`;
- candidate: exact allowed `HUMAN_P1_7` record is issuer-verified and admitted;
- evaluation: all post-Human applicable required rows and prohibitions pass;
- `G_EVIDENCE` effect: a new post-Human attestation may issue; the pre-Human attestation cannot be
  reused or rebound.

### 18.11 wrong checkpoint at the same state/version

- context: Task/run/state/version, RequirementSet, admitted refs, and authority version match;
- candidate attestation: authentic but issued for another checkpoint or target/use purpose;
- verification: request-aware owner verifier detects checkpoint/target/use mismatch;
- result: `G_EVIDENCE` denied before transition admission, with no new evaluation shortcut and no
  state mutation.

### 18.12 direct Human evidence accepted when explicitly allowed

- requirement: `HUMAN_OWNED`, applies to the exact checkpoint, and explicitly allows
  `HUMAN_DIRECT_EVIDENCE` for a named Command Center artifact type;
- candidate: authenticated Human principal input wrapped by the exact server-issued ingress record
  with matching Task/run/checkpoint/subject/content/hash/provided-at bindings;
- evaluation: all ordinary admission dimensions pass;
- decision: `ADMITTED` for that evidence requirement only; no HumanGate, HumanResult, Judgment, or
  P1-7 guard is created.

### 18.13 direct Human evidence cannot substitute for P1-7

- requirement: `HUMAN_OWNED`, producer category exactly `HUMAN_P1_7`;
- candidate: otherwise authentic and content-valid `HUMAN_DIRECT_EVIDENCE` ingress record;
- evaluation: `HUMAN_PRODUCER_CATEGORY=FAIL`;
- decision: `REJECTED(HUMAN_PRODUCER_CATEGORY_MISMATCH)` and the requirement remains
  `UNSATISFIED`.

### 18.14 unrequired supplemental material has no authority

- input: useful material is submitted but no explicit current requirement/profile applies to it;
- persistence: candidate and sanitized append-only submission provenance may be retained;
- admission: no `AdmittedEvidence`, satisfaction row, coverage mapping, or requirement mapping is
  created;
- set effect: it enters neither full-set/subset satisfaction roots nor admitted-ref roots and cannot
  affect `G_EVIDENCE`.

## 19. next implementation ownership and path contract

The next Human-authorized P1-6 implementation owns a new root:

```text
src/aiscc/evidence/
```

Expected responsibility categories are:

| direction | owner contract |
|---|---|
| `models.py` | exact enums and immutable requirement/candidate/evaluation/decision/admission/set DTOs |
| `ports.py` | issuer, content store, authority clock, requirement registry, persistence, and P1-4 verifier ports |
| `requirements.py` | server-owned RequirementSet/checkpoint registry, applicability, snapshots, and compatibility validation |
| `candidates.py` | typed ingress and immutable candidate fingerprinting; no implicit trust |
| `issuers.py` | exact P1-5/System/Human-direct/P1-7/prior-admission verifier composition with category isolation |
| `content.py` | canonical body/ref resolution, integrity, schema, sensitivity and export policy |
| `evaluator.py` | exact dimension evaluation and rejection taxonomy |
| `service.py` | admission transaction/idempotency/concurrency orchestration |
| `sets.py` | per-checkpoint applicability, per-requirement coverage, and set completeness |
| `authority.py` | P1-6-only checkpoint-bound set attestation and request-aware `G_EVIDENCE` future-owner verifier |
| `events.py` | append-only evidence authority event construction/reconstruction |

The implementation may narrowly change `src/aiscc/workflow/**` only to enforce the exact
one-attestation, request-aware checkpoint/target/use `G_EVIDENCE` handoff and register the P1-6
verifier; it may not change state values, the 22 transition pairs, or other guard ownership. It may narrowly change
`src/aiscc/persistence/**`, one new Alembic revision, and `src/aiscc/contracts/**` for evidence
persistence/DTO integration only. P1-5 provider refs are consumed through existing authority ports;
P1-6 does not change provider execution semantics.

The next Task must publish its exact creation/modification allowlist before implementation. Expected
test/config categories are `tests/unit/evidence/`, `tests/integration/evidence/`, and versioned
non-secret `config/evidence/`. Do not create:

```text
src/aiscc/human/
src/aiscc/memory/
```

Those remain P1-7/P1-8. No new provider call, credential, deployment, or LangGraph core is part of
P1-6.

## 20. next implementation proof matrix

### 20.1 NON_SUBSTITUTION

- `AgentOutputRef` alone is not admitted;
- `ExecutionSubmissionRef` alone is not admitted;
- Executor report claim alone is rejected unless the exact requirement authorizes the exact report
  body/type and its content/provenance passes;
- raw path/hash/string is not admitted;
- `AdmittedEvidenceRef` alone cannot mint `G_EVIDENCE`;
- evidence admission creates no Judgment, TransitionDecision, WorkflowState, or state_version change.

### 20.2 REQUIREMENT_MATCH

- unknown requirement and version mismatch reject with exact reasons;
- forbidden evidence rejects;
- `NOT_REQUIRED` creates no required or synthetic admitted row;
- `HUMAN_OWNED` cannot be Executor/P1-6 satisfied;
- Agent/request input cannot add, remove, weaken, or select requirements.

### 20.3 ISSUER_AND_CONTENT

- forged, absent, wrong-version, or wrong-category issuer rejects;
- wrong run/attempt/TaskContract/subject/resource rejects;
- missing body/ref and mutable/unowned reference reject;
- content hash mismatch rejects;
- schema, format, canonicalization, evidence type, and classification mismatch reject;
- P1-5 producer authority verifies provenance but does not auto-admit.

### 20.4 FRESHNESS_AND_APPLICABILITY

- valid same-version proof admits;
- state-version-scoped proof after a state change rejects as stale;
- immutable reusable artifact under an explicit compatible requirement gets a new current-task reuse
  admission;
- incompatible, over-count, revoked, superseded, wrong-scope, or config-stale reuse rejects;
- timestamp freshness alone does not pass applicability.

### 20.5 SET_COMPLETENESS

- missing one required row produces `UNSATISFIED`;
- all exact required rows and prohibition checks passing produces `SATISFIED`;
- unrequired supplemental material creates no admission/mapping/root contribution and does not alter
  completeness;
- rejected forbidden evidence satisfies nothing;
- multi-requirement content requires separate explicit mappings with no hidden fan-out.

### 20.6 CHECKPOINT_BINDING

- checkpoint identity is System/TaskContract-owned and cannot be caller-selected or inferred from
  WorkflowState alone;
- identical Task/run/state/version evaluated for different checkpoints yields distinct evaluations,
  subset roots, attestations, and guard authority;
- wrong source, target transition, exact use purpose, checkpoint version, full-set root, or subset
  root denies before `G_EVIDENCE` admission;
- explicit multi-checkpoint applicability works only through the issued requirement predicate.

### 20.7 HUMAN_GATE_NON_DEADLOCK

- final Human-owned evidence remains in the immutable full set but does not block a pre-Human
  checkpoint where it is non-applicable;
- pre-Human completeness never reclassifies the final Human requirement as `NOT_REQUIRED`;
- post-Human completeness requires the applicable exact Human producer evidence;
- P1-6 set evaluation opens, resolves, cancels, or projects no HumanGate.

### 20.8 HUMAN_DIRECT_INGRESS

- authenticated Human input without a server-issued exact ingress record rejects;
- direct ingress with wrong Task/run/checkpoint/type/subject/scope/resource/content/hash rejects;
- exact allowed `HUMAN_DIRECT_EVIDENCE` can satisfy only its named requirement;
- direct evidence against a `HUMAN_P1_7`-only requirement rejects with exact category mismatch;
- direct evidence creates no HumanResult, Judgment, Human/Judgment guard, or workflow mutation.

### 20.9 SUPPLEMENTAL_NON_AUTHORITY

- a submission with no explicit current requirement is retained only as candidate/provenance;
- no admission decision can turn unrequired material into `AdmittedEvidence`;
- no satisfaction row, coverage mapping, full/subset satisfaction contribution, or admitted-ref root
  contribution is created;
- unrequired material cannot affect or mint `G_EVIDENCE`.

### 20.10 G_EVIDENCE

- raw candidate/admitted/producer refs make P1-4 deny `G_EVIDENCE`;
- current owner-bound P1-6 set-satisfaction attestation may satisfy it;
- stale/wrong Task/run/source state/state_version/checkpoint/target/use/RequirementSet/full or subset
  root/authority-version/expired attestation denies;
- revocation/supersession invalidates old attestations before new use;
- P1-6 cannot mint any other semantic owner's guard.

### 20.11 CONCURRENCY_AND_IDEMPOTENCY

- duplicate exact admission request returns the same decision/admission;
- same ID with conflicting fingerprint rejects without mutation;
- concurrent same logical candidate admits one authoritative identity;
- stale TaskContract or RequirementSet version rejects;
- concurrent set evaluation and revocation cannot issue a stale satisfied attestation.

### 20.12 REVOCATION_AND_SUPERSESSION

- admitted evidence remains historical and immutable;
- correction creates a new candidate/admission and explicit link;
- revoking/superseding a contributing item invalidates current set satisfaction;
- old `G_EVIDENCE` attestation cannot be reused;
- no evidence event rewrites a past workflow transition.

### 20.13 RESTART

- requirements, sets, candidates, requests, evaluations, decisions, admitted mappings, authority
  events, set evaluations, and attestations reconstruct identically from PostgreSQL;
- incomplete/orphaned/corrupt provenance or projection mismatch fails closed;
- recovery performs no auto repair and infers no success from process/report prose.

### 20.14 SECURITY_AND_EXPORT

- `SECRET_FORBIDDEN` body rejects and is absent from evidence/review/public exports;
- private body is absent from public/Replay export and default review bundle;
- authorized non-secret metadata/hash/ref remains reviewable;
- sanitized derivative is a separate linked candidate, not mutation of the original;
- run/Replay visibility does not grant private evidence read authority.

The implementation proof must use production PostgreSQL persistence for durability/concurrency and
the real P1-4 future-owner verifier boundary. P1-7 is not required for P1-6 acceptance; an exact fake
Human-owner producer is permitted only to prove the P1-6 boundary and cannot be production authority.

## 21. deferred scope and Human boundary

Semantically unresolved questions for the P1-6 implementation boundary: none.

Deliberately deferred:

- P1-7 Human identity, HumanGate, HumanResult, and Judgment implementation;
- P1-8 Cycle, project closure, memory, and NextAction admission;
- public Replay evidence projection implementation;
- production evidence object-store product, retention durations, and deployment topology;
- provider/account/API key/billing/deployment configuration;
- Human acceptance of this design candidate.

```text
design result: ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING
P1-6 runtime implementation: NOT_STARTED
P1-7 / P1-8: NOT_STARTED
provider or deployment action: NOT_EXECUTED
```
