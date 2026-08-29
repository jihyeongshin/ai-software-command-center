# AISCC Cycle Record

## meta

- cycle_id: `20260829_1513_aiscc-p1-6-evidence-admission-runtime-authority-gap-hold-1`
- date: `2026-08-29T15:13:00+09:00`
- primary_semantic_owner: `P1-6_EVIDENCE`
- affected_areas: `evidence admission / human direct ingress / revocation-supersession / reuse anti-replay`
- work_type: `EVIDENCE_ADMISSION_IMPLEMENTATION`
- execution_mode: `MANUAL_COMMAND_CENTER`
- task_file: `.aiassistant/tasks/active/20260829_1241_aiscc-p1-6-evidence-admission-implementation-and-runtime-verification-1.md`
- task_done_path: `.aiassistant/tasks/done/20260829_1241_aiscc-p1-6-evidence-admission-implementation-and-runtime-verification-1.md`
- temporary_target_bundle: `.aiassistant/reports/target/20260829_1241_aiscc-p1-6-evidence-admission-implementation-and-runtime-verification-1/`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause: `POLICY_BASELINE_CONFLICT`
- cycle_record_action: `create`
- source_mirror_sync: `not-required`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260829_1513_aiscc-p1-6-evidence-admission-runtime-authority-gap-hold-1.cycle.md`

## product/repository snapshot

- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- Stage 0 predecessor: `c86e291f94bd9acc31e40bc78316132abfddd90b`
- Stage 0 terminal design persistence commit: `192e223854a02293809cf6675e3a329e099e628d`
- Stage 1 implementation commit: `none`
- workspace: Stage 1 P1-6 source/test/migration candidate remains uncommitted
- Stage 0 accepted design provenance: preserve; do not roll back

## command summary

P1-6 accepted design terminal persistence and Evidence Admission runtime implementation/runtime verification were requested in one staged Task. Stage 0 had to commit only accepted design/canonical provenance; Stage 1 had to remain an uncommitted review candidate.

## executor result summary

Stage 0 provenance separation is accepted as correctly executed:

```text
expected start HEAD:
c86e291f94bd9acc31e40bc78316132abfddd90b

accepted design SHA-256:
0d9d4c194efda37f100c6183d1a7e88e1a09fe073dc3a37bbb5a3e1cd577e463

Stage 0 commit:
192e223854a02293809cf6675e3a329e099e628d

runtime paths in Stage 0 commit:
0

Stage 1 commit:
none
```

Executor reported:

```text
ruff: PASS
mypy --strict: PASS
targeted pytest: 83 PASS
PostgreSQL migration/runtime: PASS
real provider calls: 0
P1-7/P1-8 source creation: none
```

These results are useful executor evidence, but they do not overcome current-source violations of the accepted P1-6 authority contract.

## proof admission / Command Center findings

### accepted

- Stage 0 exact design/canonical persistence separation: `ADMITTED`
- exact five evidence profiles present: `ADMITTED`
- P1-4 request-aware `G_EVIDENCE` verifier direction: `ADMITTED_AS_CANDIDATE_IMPLEMENTATION`
- PostgreSQL append-only base tables/triggers and targeted runtime proof: `ADMITTED_AS_EXECUTOR_EVIDENCE`
- P1-5 producer ref != evidence admission split: `ADMITTED_AS_CANDIDATE_IMPLEMENTATION`
- real provider/network/credential/public release absence: `ADMITTED`

### rejected / insufficient

#### FINDING-1 — durable HUMAN_DIRECT_EVIDENCE ingress authority is missing

Accepted design requires a server-issued immutable Human direct ingress record that durably binds:

```text
authenticated Human principal/operator identity
ingress authority id/version
TaskContract id/version
work_run_id
checkpoint id/version
evidence type
subject/scope/resource
content owner/ref/hash
provided_at
ingress record id/version/fingerprint/authenticity
```

The accepted persistence baseline explicitly requires:

```text
HumanDirectEvidenceIngressRow when applicable
```

Current candidate instead keeps principal identity only in process memory:

```text
HumanDirectEvidenceIngressAuthority._principals: dict[candidate_id, principal_id]
```

The durable candidate row persists only `human_ingress_record_ref` text and does not persist the authenticated principal/immutable ingress authority record. A fresh process therefore cannot reconstruct who provided the Human evidence from ordered durable provenance.

Result:

```text
HUMAN_DIRECT_INGRESS:
REJECTED

RESTART:
PARTIAL / INSUFFICIENT
```

#### FINDING-2 — authority revocation/supersession does not invalidate every committed attestation authority

Accepted design requires:

```text
revoking/superseding currently contributing authority
→ increments evidence-authority version
→ invalidates affected current satisfaction
→ invalidates every attestation committed to the old authority version/root
→ requires a new set evaluation
```

Every authority event must bind owner, authority version, affected refs/mappings, Task/run scope, and time.

Current candidate's `load_effective_attestation()` checks the attestation itself, WorkRun state/version, evaluation roots, and admitted-evidence invalidation, but does not re-check that the committed RequirementSet, checkpoint, and applicable requirement authorities remain current/non-superseded.

`register_authority()` may append `SUPERSEDED` for an old RequirementSet while an old attestation remains otherwise loadable.

Current `EvidenceAuthorityEventRow` also lacks the accepted durable owner + Task/run scope + affected mapping bindings, and `revoke()` accepts an arbitrary `subject_ref`/authority_version without reconstructing and advancing a current evidence-authority version.

Result:

```text
REVOCATION_SUPERSESSION:
REJECTED

G_EVIDENCE:
REJECTED for post-authority-change reuse
```

#### FINDING-3 — `reuse_maximum` is not enforced as a remaining reuse count

Accepted design requires:

```text
positive remaining reuse count and policy
```

Current evaluator checks only:

```text
requirement.reuse_maximum < 1
```

and never counts or reconstructs prior reuse admissions. Any positive configured maximum therefore behaves as effectively unlimited reuse, subject only to the other compatibility gates.

Result:

```text
REUSE_ANTI_REPLAY:
REJECTED
```

#### FINDING-4 — correction event vocabulary drifts from accepted canonical semantics

Accepted design event name:

```text
CORRECTED
```

Current enum:

```text
CORRECTED_BY
```

This is not the primary HOLD reason, but rework must align the canonical event vocabulary or document an explicitly equivalent canonical identifier without silently changing the accepted contract.

## evidence results

### executed

- classification: `EXECUTED_PASS`
  channel: `STATIC_SOURCE / UNIT_TEST / INTEGRATION_TEST / DATABASE_RUNTIME`
  result: Executor reported ruff, strict mypy, 83 targeted tests, PostgreSQL migration/runtime PASS.

### human_provided

- classification: `HUMAN_PROVIDED`
  result_source: Browser Command Center review
  result: `HOLD_REWORK_REQUIRED`

### rejected claims/evidence

- Executor mandatory proof matrix claim `HUMAN_DIRECT_INGRESS = PASS` is not admitted because the durable ingress record required by the accepted design is absent.
- Executor mandatory proof matrix claim `REVOCATION_SUPERSESSION = PASS` is not admitted because old attestation authority is not invalidated for every RequirementSet/checkpoint/requirement authority change.
- Executor mandatory proof matrix claim `REUSE_ANTI_REPLAY = PASS` is not admitted because `reuse_maximum` remaining count is not enforced.
- Executor `RESTART = PASS` is narrowed: repository/set/admission reconstruction is useful proof, but Human direct ingress provenance is not reconstructable from durable records.

## command-center judgment

- result_status: `HOLD_REWORK_REQUIRED`
- accepted_scope: Stage 0 terminal design persistence commit and unaffected P1-6 implementation portions may remain.
- required_rework:
  - durable Human direct ingress authority record + persistence + restart proof
  - current evidence-authority revision and full attestation invalidation across RequirementSet/checkpoint/requirement/admitted-evidence authority changes
  - finite `reuse_maximum` remaining-count enforcement
  - exact correction event vocabulary alignment
  - targeted regression proving all above
- blocked_reason: accepted P1-6 canonical authority contract is not fully implemented
- evidence_contract_satisfied: `No`
- forbidden_action_absent: `Yes`
- proof_non_substitution_satisfied: `Partial`
- transition_authority_satisfied: `Yes for direct mutation boundary; No for stale G_EVIDENCE invalidation`
- security_boundary_satisfied: `Yes for submitted scope`
- public_provenance_satisfied: `Stage 0 yes; Stage 1 remains candidate`
- terminal_decision_reason: three load-bearing authority gaps remain despite otherwise strong implementation/test evidence.

## rollback / preservation

Do not roll back:

```text
192e223854a02293809cf6675e3a329e099e628d
```

Do not remove or rewrite the accepted design terminal provenance.

Rework the current uncommitted Stage 1 source in place under a new timestamped Task. Do not commit P1-6 runtime until a later Command Center/Human acceptance Task explicitly authorizes it.

## preserved artifacts

- `.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md`
- `.aiassistant/tasks/done/20260829_1026_aiscc-p1-6-checkpoint-human-ingress-and-optional-evidence-design-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260829_1026_aiscc-p1-6-checkpoint-human-ingress-and-optional-evidence-hold-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260829_1241_aiscc-p1-6-evidence-admission-design-final-acceptance-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260829_1513_aiscc-p1-6-evidence-admission-runtime-authority-gap-hold-1.cycle.md`
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
- `.aiassistant/tasks/done/20260829_1241_aiscc-p1-6-evidence-admission-implementation-and-runtime-verification-1.md`

## next action

```text
P1-6 Evidence Admission Runtime
→ narrow authority rework

P1-7:
NOT_STARTED

P1-8:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```
