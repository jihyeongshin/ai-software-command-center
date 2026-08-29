# AISCC Cycle Record

## meta

- cycle_id: `20260829_1617_aiscc-p1-6-authoritative-workrun-admission-freshness-hold-1`
- date: `2026-08-29T16:17:00+09:00`
- primary_semantic_owner: `P1-6_EVIDENCE`
- affected_areas: `evidence admission / WorkRun authority / freshness / stale-proof rejection`
- work_type: `REWORK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- task_file: `.aiassistant/tasks/active/20260829_1513_aiscc-p1-6-human-ingress-revocation-and-reuse-authority-rework-1.md`
- task_done_path: `.aiassistant/tasks/done/20260829_1513_aiscc-p1-6-human-ingress-revocation-and-reuse-authority-rework-1.md`
- temporary_target_bundle: `.aiassistant/reports/target/20260829_1513_aiscc-p1-6-human-ingress-revocation-and-reuse-authority-rework-1/`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause: `POLICY_BASELINE_CONFLICT`
- cycle_record_action: `create`
- source_mirror_sync: `not-required`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260829_1617_aiscc-p1-6-authoritative-workrun-admission-freshness-hold-1.cycle.md`

## product/repository snapshot

- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- accepted design terminal commit: `192e223854a02293809cf6675e3a329e099e628d`
- accepted design SHA-256: `0d9d4c194efda37f100c6183d1a7e88e1a09fe073dc3a37bbb5a3e1cd577e463`
- Stage 1 implementation commit: `none`
- final Executor HEAD reported: `192e223854a02293809cf6675e3a329e099e628d`
- index reported: empty
- runtime candidate: uncommitted

## command summary

Previous Command Center HOLD required four narrow corrections:

```text
1. durable HUMAN_DIRECT_EVIDENCE ingress
2. authority-revision-based attestation invalidation
3. finite reuse_maximum enforcement
4. CORRECTED vocabulary alignment
```

The submitted rework candidate was reviewed against both those findings and the full accepted P1-6 Evidence Admission contract.

## executor result summary

Executor reported:

```text
result:
ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING

start/final HEAD:
192e223854a02293809cf6675e3a329e099e628d

ruff:
PASS

format:
PASS

mypy --strict:
PASS

P1-6 finding proof:
11 PASS

P1-4 workflow regression:
48 PASS

P1-5 unit:
43 PASS

P1-5 integration:
28 PASS

combined:
130 PASS

PostgreSQL:
17.6

migration empty → head:
PASS

migration 20260828_0002 → head:
PASS

real provider calls:
0

external network:
0

Git commit:
0
```

The rework report and actual exported source agree that the original four HOLD findings were materially addressed.

## previous HOLD findings — review result

### FINDING-1 — durable HUMAN_DIRECT_EVIDENCE ingress

```text
CLOSED
```

Candidate now contains:

```text
HumanDirectEvidenceIngress
HumanDirectEvidenceIngressRef
HumanDirectEvidenceIngressRow
candidate → ingress FK
append-only ingress storage
fresh-repository ingress reconstruction
HUMAN_DIRECT_EVIDENCE != HUMAN_P1_7 tests
```

The exact runtime authentication integration remains a future system integration concern, but the previous missing durable ingress-record finding is closed for the current P1-6 boundary.

### FINDING-2 — authority revocation/supersession

```text
CLOSED
```

Candidate now:

- stores append-only authority events with Task/run scope and affected refs/mappings;
- derives a durable current `evidence_authority_revision`;
- commits evaluations/attestations to that revision;
- revalidates RequirementSet/checkpoint/requirement/admitted-evidence authority in `load_effective_attestation()`;
- rejects old attestations after RequirementSet supersession and other invalidating authority events;
- does not require an in-memory invalidation call after restart.

### FINDING-3 — finite reuse_maximum

```text
CLOSED
```

Candidate now:

- persists `evidence_reuse_consumptions`;
- counts an exact prior-evidence / requirement / WorkRun / checkpoint scope;
- serializes that scope with a PostgreSQL advisory transaction lock;
- enforces `reuse_consumed >= reuse_maximum`;
- proves idempotency/concurrency/restart behavior.

### FINDING-4 — correction vocabulary

```text
CLOSED
```

Current first-class event identifier is:

```text
CORRECTED
```

and replacement relation is persisted.

---

# new load-bearing finding

## FINDING-5 — admission freshness is not bound to authoritative current WorkRun state/version

```text
OPEN / REWORK_REQUIRED
```

This finding is independent of the previous four corrections.

Accepted P1-6 contract requires:

```text
EvidenceCandidate != AdmittedEvidence

admission freshness:
requirement-owned

WORKRUN_STATE_VERSION_SCOPED

state-version scoped stale proof
→ rejected
```

Admission request/candidate binding to the same claimed state/version is not sufficient. The current System-owned WorkRun is the authoritative source.

### actual current-source behavior

`PostgresEvidenceRepository.admit()`:

- locks the admission request, TaskContract key, and logical candidate scope;
- loads RequirementSet/checkpoint/requirement authority;
- evaluates issuer/content/reuse/revocation;
- persists request/evaluation/decision/admitted evidence.

But this admission path does **not** load the authoritative `WorkRunRow` before deciding `ADMITTED`.

It therefore does not establish that:

```text
request.work_run_id exists

WorkRun.task_contract_id/version
== request.task_contract_id/version

WorkRun.workflow_state
== request.observed_state
== checkpoint.source_state

WorkRun.state_version
== request.observed_state_version
```

### evaluator behavior

For `WORKRUN_STATE_VERSION_SCOPED`, `_fresh()` currently checks only:

```text
candidate.producer_work_run_id == request.work_run_id
candidate.observed_state == request.observed_state
candidate.observed_state_version == request.observed_state_version
```

This proves internal consistency between two caller/request-side objects, not freshness against current System state.

The unit stale test likewise makes only the candidate stale relative to the request:

```text
candidate state_version = 2
request state_version = 3
→ STALE
```

It does not prove:

```text
candidate state_version = 3
request state_version = 3
current durable WorkRun state_version = 4
→ REJECTED
```

### consequence

A request and candidate may both carry an old or otherwise non-authoritative WorkRun state/version and still produce:

```text
EvidenceAdmissionDecision = ADMITTED
AdmittedEvidence = created
```

provided their local values match each other and other requirement checks pass.

Later `EvidenceSetEvaluation` does reload `WorkRunRow` and can refuse to use stale admitted evidence, so the current implementation does protect the eventual `G_EVIDENCE` path in many cases.

However:

```text
stale candidate
→ AdmittedEvidence
```

is itself forbidden by the accepted P1-6 admission contract.

`AdmittedEvidence` is durable authority and must not be used as a quarantine area for evidence that was stale at admission time.

### additional anti-replay risk

Because admission does not require the WorkRun to exist/current at decision time, an internally self-consistent request can create durable evidence without proving the target WorkRun/current checkpoint authority actually exists at that instant.

That weakens:

```text
TASK_CONTRACT_BINDING
CHECKPOINT_BINDING
FRESHNESS
```

at the admission boundary, even though a later set evaluation may fail closed.

---

# evidence interpretation

## admitted executor evidence

- previous four HOLD findings: fresh implementation/test evidence admitted as corrected candidate behavior
- Stage 0 accepted design commit preservation: admitted
- 130 reported targeted/regression tests: admitted as executor evidence
- PostgreSQL migration/runtime result: admitted as executor evidence
- provider/network/credential/Git prohibited-action absence: admitted

## rejected/insufficient claim

The current candidate cannot yet be accepted as implementing the full mandatory P1-6 proof:

```text
state-version scoped stale proof
→ rejected at admission
```

The existing stale unit test proves only candidate/request mismatch, not stale-vs-System WorkRun authority.

## proof non-substitution

```text
candidate/request self-consistency
!= authoritative current WorkRun freshness

later EvidenceSet rejection
!= correct EvidenceAdmission rejection
```

---

# command-center judgment

- result_status: `HOLD_REWORK_REQUIRED`
- accepted_scope:
  - all four previous rework findings are accepted as closed
  - unaffected P1-6 candidate implementation remains usable
  - accepted design commit `192e223854a02293809cf6675e3a329e099e628d` remains permanent
- required_rework:
  - bind admission to current durable WorkRun authority
  - reject missing/wrong-task/stale WorkRun before `AdmittedEvidence` can be created
  - remove TOCTOU between WorkRun freshness check and admission persistence using the existing P1-4 persistence concurrency convention
  - add fresh PostgreSQL tests where request and candidate agree with each other but disagree with current WorkRun
- blocked_reason: full P1-6 admission freshness contract is not yet implemented
- evidence_contract_satisfied: `No`
- forbidden_action_absent: `Yes`
- proof_non_substitution_satisfied: `No — stale admission boundary still substitutes request self-consistency for System state`
- transition_authority_satisfied: `Yes for G_EVIDENCE transition ownership`
- security_boundary_satisfied: `Yes for submitted scope`
- public_provenance_satisfied: `candidate remains uncommitted`
- terminal_decision_reason: one newly discovered load-bearing admission-authority gap remains.

---

# rollback / preservation

Do not roll back or amend:

```text
192e223854a02293809cf6675e3a329e099e628d
```

Do not discard the corrected Human ingress / authority revision / reuse / correction work.

Perform a narrow rework on the current uncommitted candidate.

P1-7 and P1-8 remain `NOT_STARTED`.

---

# preserved artifacts

- `.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md`
- `.aiassistant/records/aiscc/cycles/20260829_1241_aiscc-p1-6-evidence-admission-design-final-acceptance-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260829_1513_aiscc-p1-6-evidence-admission-runtime-authority-gap-hold-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260829_1617_aiscc-p1-6-authoritative-workrun-admission-freshness-hold-1.cycle.md`
- `.aiassistant/tasks/done/20260829_1241_aiscc-p1-6-evidence-admission-implementation-and-runtime-verification-1.md`
- `.aiassistant/tasks/done/20260829_1513_aiscc-p1-6-human-ingress-revocation-and-reuse-authority-rework-1.md`
- `.aiassistant/reports/aiscc/20260829_1227_aiscc-p1-6-design-accepted-command-center-handoff-1.md`

---

# next action

```text
P1-6 Evidence Admission Runtime
→ narrow authoritative WorkRun admission/freshness rework

P1-7:
NOT_STARTED

P1-8:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```
