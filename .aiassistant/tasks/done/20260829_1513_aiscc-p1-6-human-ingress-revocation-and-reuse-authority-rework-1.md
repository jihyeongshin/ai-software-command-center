# 작업지시서: P1-6 Human Ingress / Revocation / Reuse Authority Rework

## meta

- task_id: `20260829_1513_aiscc-p1-6-human-ingress-revocation-and-reuse-authority-rework-1`
- created_at: `2026-08-29T15:13:00+09:00`
- phase: `P1-6 Evidence Admission`
- work_type: `REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1-6_EVIDENCE`
- accepted_design_commit: `192e223854a02293809cf6675e3a329e099e628d`
- accepted_design_path: `.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md`
- accepted_design_sha256: `0d9d4c194efda37f100c6183d1a7e88e1a09fe073dc3a37bbb5a3e1cd577e463`
- predecessor_runtime_task: `20260829_1241_aiscc-p1-6-evidence-admission-implementation-and-runtime-verification-1`
- predecessor_judgment: `HOLD_REWORK_REQUIRED`
- p1_7_status: `NOT_STARTED`
- p1_8_status: `NOT_STARTED`
- public_bounded_live_release: `NOT_RELEASED`

---

# 1. 현재 상태

P1-6 design terminal persistence is complete and MUST be preserved:

```text
commit:
192e223854a02293809cf6675e3a329e099e628d
```

The current P1-6 runtime implementation is an uncommitted review candidate.

Command Center judgment:

```text
HOLD_REWORK_REQUIRED
```

HOLD Cycle to place/preserve:

```text
.aiassistant/records/aiscc/cycles/
20260829_1513_aiscc-p1-6-evidence-admission-runtime-authority-gap-hold-1.cycle.md
```

Do not roll back or amend the accepted design commit.

Do not restart P1-6 from scratch. Preserve unaffected candidate implementation and perform narrow rework only.

---

# 2. mandatory findings to close

## FINDING-1 — durable HUMAN_DIRECT_EVIDENCE ingress authority

Accepted design requires a server-issued immutable Human direct ingress record binding:

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
ingress record id/version/fingerprint
issuer authenticity
```

The current in-memory mapping:

```text
HumanDirectEvidenceIngressAuthority._principals
```

is not sufficient durable authority.

Implement an immutable typed/durable equivalent of:

```text
HumanDirectEvidenceIngress
HumanDirectEvidenceIngressRef
HumanDirectEvidenceIngressRow
```

or an exact equivalent consistent with project naming conventions.

Required properties:

- ingress record is server-issued, not caller-authored
- authenticated Human principal identity is durably bound
- authority id/version is durably bound
- TaskContract/work_run/checkpoint/type/subject/scope/resource/content/provided_at are durably bound
- record has exact immutable id/version/fingerprint
- duplicate same identity is idempotent only with identical fingerprint
- same id + different content is identity conflict
- candidate `human_ingress_record_ref` must resolve to this exact durable record
- `HUMAN_DIRECT_EVIDENCE` issuer verification must verify the durable ingress record, not only an in-process token/map
- fresh process/repository/service construction must reconstruct ingress provenance
- `HUMAN_DIRECT_EVIDENCE != HUMAN_P1_7`
- no HumanGate/HumanResult/Judgment/G_HUMAN/G_JUDGMENT authority is added

If the existing `20260829_0003` migration is still uncommitted, update that same candidate migration rather than creating an unnecessary second migration.

## FINDING-2 — revocation/supersession must invalidate all old G_EVIDENCE authority

Accepted design requires every authority event to bind:

```text
owner
authority version/revision
reason
affected refs/mappings
Task/run scope
time
replacement/correction relation when applicable
```

Required semantic chain:

```text
revocation/supersession/correction of contributing authority
→ advance current evidence-authority revision
→ old current satisfaction becomes invalid
→ every attestation committing to old authority revision/root becomes unusable
→ new EvidenceSetEvaluation required
→ only a new attestation may satisfy G_EVIDENCE
```

Close all of these cases:

```text
AdmittedEvidence revoked/superseded/corrected
Requirement revoked/superseded
Checkpoint revoked/superseded
RequirementSet superseded
authority revision changed
```

`load_effective_attestation()` and `EvidenceGuardAuthority` must fail closed against the durable current authority, not merely the attestation's own row and WorkRun state/version.

An old attestation must be rejected after a new RequirementSet supersedes the old set even if:

```text
WorkRun id/state/state_version unchanged
checkpoint ID happens to remain semantically similar
admitted evidence bytes unchanged
old attestation row itself was not directly revoked
```

Do not require in-memory `invalidate()` calls for correctness. In-memory invalidation may be a cache optimization only. A fresh process must reject stale attestations from PostgreSQL authority alone.

## FINDING-3 — finite `reuse_maximum` remaining-count enforcement

Current behavior equivalent to:

```text
reuse_maximum > 0
→ reuse allowed without decrement/count
```

is forbidden.

Implement deterministic durable reuse-count semantics.

At minimum:

```text
reuse_maximum = N
→ at most N successful current-task/current-checkpoint reuse admissions may descend from the governed prior admitted evidence under the exact policy scope
```

The exact counted scope must follow the accepted requirement/reuse policy and be explicit in code/tests.

Required:

- rejected reuse does not consume count
- idempotent retry of the same immutable request does not consume an additional count
- concurrent requests cannot exceed the maximum
- restart preserves consumed/remaining count
- revocation/supersession/correction is still evaluated independently
- `reuse_maximum = 0` rejects reuse
- `reuse_maximum = 1` proves second distinct successful reuse is denied
- no hidden unlimited default

If the accepted design's existing field set is insufficient to represent the exact counted scope, STOP with `POLICY_CONFLICT_INVESTIGATION_REQUIRED` rather than inventing a new public policy dimension.

## FINDING-4 — correction vocabulary

Canonical design uses:

```text
CORRECTED
```

Align implementation vocabulary to the accepted canonical identifier unless the canonical design itself already defines a different exact source identifier elsewhere.

Do not silently retain `CORRECTED_BY` as a divergent first-class event kind.

---

# 3. 이번 턴 목표

1. Place/preserve the Command Center HOLD Cycle.
2. Implement durable Human direct ingress authority.
3. Implement complete durable authority revision/invalidation semantics.
4. Enforce finite `reuse_maximum`.
5. Align correction event vocabulary.
6. Add targeted negative/concurrency/restart tests for every finding.
7. Run directly affected P1-6 + P1-4/P1-5 regression only.
8. Produce a new target bundle.
9. Keep runtime implementation uncommitted for Command Center review.

---

# 4. 비목표

- P1-7 implementation
- P1-8 implementation
- workflow state/transition matrix changes
- P1-5 provider/tool execution redesign
- public Live/deployment
- real provider calls
- unrelated refactor
- Stage 0 accepted design commit modification/amend/revert
- runtime implementation Git commit

---

# 5. predecessor / workspace rules

Expected HEAD:

```text
192e223854a02293809cf6675e3a329e099e628d
```

This HEAD is the accepted P1-6 design terminal persistence commit.

The P1-6 Stage 1 candidate is expected to exist as uncommitted changes from the predecessor Task.

Before mutation:

- verify HEAD exactly
- inventory current uncommitted P1-6 candidate paths
- verify no unrelated dirty collision
- verify accepted design SHA remains exact
- verify predecessor done Task/report evidence as available
- preserve unrelated pre-existing curated handoff artifact untouched

If HEAD differs:

```text
STOP
→ BLOCKED_PREDECESSOR_HEAD_DRIFT
```

Do not clean/reset the Stage 1 candidate.

---

# 6. allowed paths

Primary rework:

```text
src/aiscc/evidence/**
src/aiscc/persistence/models.py
migrations/versions/20260829_0003_p1_6_evidence_admission.py
tests/unit/evidence/**
tests/integration/evidence/**
```

Narrow regression integration only if required:

```text
src/aiscc/workflow/guards.py
tests/unit/workflow/test_state_machine.py
tests/integration/workflow/test_postgres_kernel.py
```

Governance/report lifecycle:

```text
.aiassistant/records/aiscc/cycles/20260829_1513_aiscc-p1-6-evidence-admission-runtime-authority-gap-hold-1.cycle.md
.aiassistant/tasks/active/<this-task>
.aiassistant/tasks/done/<this-task>
.aiassistant/reports/target/20260829_1513_aiscc-p1-6-human-ingress-revocation-and-reuse-authority-rework-1/**
```

Do not modify accepted design/canonical state merely to make implementation fit.

---

# 7. mandatory proof matrix

## HUMAN_DIRECT_DURABLE_INGRESS

Prove:

```text
caller-crafted human_ingress_record_ref
→ rejected

authenticated Human principal
→ server-issued durable ingress record

same ingress ID + same fingerprint
→ immutable same authority

same ingress ID + different fingerprint
→ identity conflict

fresh process/repository/issuer service
→ durable principal/ingress provenance reconstructs

HUMAN_DIRECT_EVIDENCE candidate
→ exact durable ingress record required

HUMAN_DIRECT_EVIDENCE
→ cannot satisfy HUMAN_P1_7-only requirement
```

## AUTHORITY_REVISION_INVALIDATION

Prove separately:

```text
admitted evidence revoked
→ old attestation rejected

Requirement superseded/revoked
→ old attestation rejected

Checkpoint superseded/revoked
→ old attestation rejected

RequirementSet superseded
→ old attestation rejected

fresh process after each authority event
→ old attestation still rejected

new set evaluation under current authority
→ new attestation may be issued only when satisfied
```

The test must not depend on an in-memory `invalidate()` call.

## REUSE_LIMIT

Prove at least:

```text
reuse_maximum = 0
→ reject

reuse_maximum = 1
→ first distinct compatible reuse admitted
→ idempotent retry returns same result
→ second distinct reuse rejected

concurrent distinct reuse attempts at remaining count 1
→ at most one additional authoritative admission

restart
→ consumed reuse count preserved

rejected incompatible/revoked reuse
→ does not consume count
```

## CORRECTION

Prove:

```text
CORRECTED event
→ old evidence/current satisfaction/attestation invalid as defined
→ old historical rows remain immutable
→ named new admission relation is durable
```

---

# 8. persistence requirements

The final durable model must include sufficient data to reconstruct, without process memory:

```text
Human direct ingress principal/authority record
current evidence authority revision
authority event owner
Task/run scope
affected authority refs/mappings
replacement/correction relation
reuse consumption lineage/count
```

Do not encode load-bearing authority only in Python object identity/private tokens.

Private tokens may protect in-process issuance, but durable verification after restart must be derived from trusted persisted authority and injected server ownership.

Append-only mutation-denial rules must cover any newly added durable authority table.

---

# 9. evidence contract

executor_required:

```text
STATIC_SOURCE
UNIT_TEST
INTEGRATION_TEST
DATABASE_RUNTIME
CONCURRENCY
RESTART
P1_4_G_EVIDENCE_HANDOFF
SECURITY_EXPORT
```

reuse_allowed:

```text
predecessor 83 PASS may be reused only for unchanged cases;
all four findings require fresh tests
```

human_owned:

```text
P1-6 runtime final acceptance
```

not_required:

```text
browser
frontend
real provider
external HTTP
deployment
production/test infrastructure
```

forbidden:

```text
P1-7/P1-8 source
real provider call
credentialed external action
public Live
Git push
runtime implementation commit
accepted design commit rewrite
```

---

# 10. accept 기준

Rework candidate is reviewable only if:

```text
Human direct ingress principal/record is durable and restart-reconstructable

old attestation is rejected after any contributing RequirementSet/checkpoint/requirement/evidence authority change

evidence authority revision is durable and advanced deterministically

reuse_maximum has real finite remaining-count semantics under concurrency/restart

CORRECTED canonical vocabulary is aligned

no in-memory-only invalidation is required for correctness

all fresh finding-specific tests PASS

directly affected P1-4/P1-5 regression PASS

PostgreSQL migration from 20260828_0002 and empty DB PASS

raw secret residue = 0

real provider calls = 0

P1-7/P1-8 remain NOT_STARTED

Stage 1 remains uncommitted
```

---

# 11. mandatory stop

STOP on:

```text
accepted design conflict
HEAD drift
need to alter P1-4 transition graph
need to add P1-7 authority
ambiguous reuse count policy not resolvable from canonical design
need for external credential/network/runtime
unrelated dirty collision
```

After stop, collect only minimal blocker evidence/report/export.

---

# 12. report required

Report exact:

```text
start HEAD / workspace
accepted design SHA
HOLD Cycle placement
finding-by-finding changed source
new/changed persistence entities
migration changes
Human ingress durable fields and restart reconstruction
authority revision algorithm
attestation effective-authority verification path
reuse count algorithm and transaction/lock boundary
CORRECTED vocabulary
fresh test commands/pass counts
concurrency result
restart result
P1-4/P1-5 regression
real provider/network/credential count
Git status/index
unverified Human acceptance
preserved exact paths
```

Do not report predecessor PASS as closure of a finding unless a fresh finding-specific test exists.

---

# 13. export bundle

Target:

```text
.aiassistant/reports/target/
20260829_1513_aiscc-p1-6-human-ingress-revocation-and-reuse-authority-rework-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
```

Include all changed P1-6 source/test/migration and the HOLD Cycle preserving repository-relative paths.

---

# 14. lifecycle / Git

Task starts:

```text
.aiassistant/tasks/active/
20260829_1513_aiscc-p1-6-human-ingress-revocation-and-reuse-authority-rework-1.md
```

Executor turn complete:

```text
.aiassistant/tasks/done/
20260829_1513_aiscc-p1-6-human-ingress-revocation-and-reuse-authority-rework-1.md
```

No Git add/commit/push is authorized in this rework Task.

HEAD must remain:

```text
192e223854a02293809cf6675e3a329e099e628d
```

unless a blocker proves it did not start there.

---

# 15. preserved artifacts

Must preserve:

```text
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md

.aiassistant/records/aiscc/cycles/
20260829_1241_aiscc-p1-6-evidence-admission-design-final-acceptance-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260829_1513_aiscc-p1-6-evidence-admission-runtime-authority-gap-hold-1.cycle.md

.aiassistant/tasks/done/
20260829_1241_aiscc-p1-6-evidence-admission-implementation-and-runtime-verification-1.md

.aiassistant/tasks/done/
20260829_1513_aiscc-p1-6-human-ingress-revocation-and-reuse-authority-rework-1.md
```

Stage 0 commit `192e223854a02293809cf6675e3a329e099e628d` is permanent accepted design provenance.

---

# 16. final response

1. result
2. start HEAD
3. HOLD Cycle placement
4. findings closed/not closed
5. target bundle
6. changed files
7. fresh proof summary
8. concurrency/restart summary
9. provider/network/credential actions
10. human verification = `HUMAN_PENDING`
11. Git HEAD/index/status
12. preserved exact paths
13. next recommendation
