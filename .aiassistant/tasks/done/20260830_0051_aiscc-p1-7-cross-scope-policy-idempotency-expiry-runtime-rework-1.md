# 작업지시서: P1-7 Cross-Scope / Policy / Idempotency / Expiry Runtime Rework

## meta

- task_id: `20260830_0051_aiscc-p1-7-cross-scope-policy-idempotency-expiry-runtime-rework-1`
- created_at: `2026-08-30T00:51:00+09:00`
- phase: `P1-7 Human Gate and Judgment`
- work_type: `REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1-7_HUMAN_JUDGMENT`
- expected_start_head: `c87cfc75f14476e10b4a02a2ab0bd295720a85a0`
- accepted_design_commit: `238b0b41460c2504fd3244eadb06809d8692a60f`
- accepted_design_terminal_commit: `c87cfc75f14476e10b4a02a2ab0bd295720a85a0`
- accepted_design_sha256: `22851cd0a6476fe613a3cc7a86a4096ace7236b4bafdd3c7c5a25e701a3b1549`
- predecessor_stage1_path_count: `19`
- predecessor_stage1_actual_aggregate_sha256: `89bf0a5e60a6bbfd795866eaf838d99f8c5bffb41e3e490dea68537643ed295c`
- p1_7_runtime_status: `REWORK_REQUIRED / HUMAN_PENDING`
- p1_8_status: `NOT_STARTED`
- public_bounded_live_release: `NOT_RELEASED`

---

# 1. current state

P1-7 design terminal persistence is complete and accepted.

Preserve:

```text
Stage 0A:
238b0b41460c2504fd3244eadb06809d8692a60f

Stage 0B:
c87cfc75f14476e10b4a02a2ab0bd295720a85a0
```

Do not amend, revert, squash, or rewrite those commits.

Current P1-7 runtime is an uncommitted 19-path candidate.

Command Center judgment:

```text
HOLD_REWORK_REQUIRED
```

Place/preserve HOLD Cycle:

```text
.aiassistant/records/aiscc/cycles/
20260830_0051_aiscc-p1-7-runtime-authority-binding-policy-expiry-hold-1.cycle.md
```

Do not restart P1-7 from scratch. Rework only the current runtime candidate and directly affected tests/migration.

---

# 2. predecessor candidate identity

Before mutation verify:

```text
HEAD ==
c87cfc75f14476e10b4a02a2ab0bd295720a85a0

accepted design SHA ==
22851cd0a6476fe613a3cc7a86a4096ace7236b4bafdd3c7c5a25e701a3b1549
```

The predecessor export manifest had one incorrect SHA row.

Correct exported predecessor identity for:

```text
src/aiscc/evidence/issuers.py
```

is:

```text
8f07c8eb14c78a77cac6b7d0400733f2c4d41fb3a7178f860e3540a575f9d9f5
```

not the 63-character value in the predecessor manifest.

Command Center recalculated the actual 19-path aggregate from exported bytes using:

```text
sort repository-relative paths ascending

serialize:
<path>\t<lowercase_sha256>\n

SHA-256 UTF-8 bytes
```

Expected predecessor aggregate:

```text
89bf0a5e60a6bbfd795866eaf838d99f8c5bffb41e3e490dea68537643ed295c
```

If current local uncommitted candidate differs before rework:

```text
STOP
→ REVIEWED_CANDIDATE_DRIFT
```

unless the only difference is the current Task/HOLD governance artifact outside the 19 runtime paths.

---

# 3. load-bearing invariants

Preserve:

```text
HumanGate = System-owned

HumanResult != Judgment
Judgment != TransitionDecision
HumanResult/Judgment != WorkflowState

HUMAN_DIRECT_EVIDENCE != HUMAN_P1_7

G_EVIDENCE != G_HUMAN_* != G_JUDGMENT_*

P1-4 owns TransitionDecision/WorkflowState mutation

P1-6 owns evidence admission/G_EVIDENCE truth

P1-7 owns Human/Judgment authority only

V1 HumanResultKind:
APPROVE | REWORK | REJECT

V1 JudgmentKind:
ACCEPTED | REJECTED | HOLD_REWORK_REQUIRED

V1 concurrent HumanResult:
FIRST_DURABLY_ADMITTED

V1 policy override:
NOT_SUPPORTED
```

---

# 4. FINDING-1 — close all cross-scope authority substitution

## 4.1 reservation/request binding

A `HumanGateReservation` is valid only for its exact bound transition use.

Before `G_HUMAN_REQUIRED` can be activated, require exact match:

```text
reservation.task_contract_id
== request.task_contract_id

reservation.task_contract_version
== request.task_contract_version

reservation.work_run_id
== request.work_run_id

reservation.opened_from_state
== request.observed_state

reservation.opened_from_state_version
== request.observed_state_version

reservation.target_state
== request.target_state

reservation purpose id/version
== exact accepted HumanGate purpose for this request/use

reservation authority policy id/version
== current configured policy for this TaskContract/use

reservation gate fingerprint
== canonical fingerprint recomputed from current exact reservation fields
```

The transaction participant must revalidate this under the canonical WorkRun transaction, not only before entering it.

Wrong reservation:

```text
→ no current G_HUMAN_REQUIRED
→ no HumanGate row/event/projection
→ P1-4 transition denied
```

`_open_gate()` must defensively require the same exact request/reservation binding before any insert.

## 4.2 HumanResult/gate/request binding for G_HUMAN_*

For result guards require exact current equality:

```text
HumanResult.task_contract_id/version == request
HumanResult.work_run_id == request.work_run_id
HumanResult.source_state == request.observed_state
HumanResult.state_version == request.observed_state_version

HumanGate.task_contract_id/version == request
HumanGate.work_run_id == request.work_run_id
HumanGate.bound_state == request.observed_state
HumanGate.bound_state_version == request.observed_state_version

HumanResult.human_gate_ref == current HumanGate
HumanResult.gate_authority_revision == current gate revision as accepted semantics require
gate purpose/use is applicable to request target
request.human_result_refs == exact one current result ref
```

A result from WorkRun A must never satisfy `G_HUMAN_APPROVED`, `G_HUMAN_REWORK`, or `G_HUMAN_REJECTED` for WorkRun B.

## 4.3 Judgment HumanResult binding

`PostgresJudgmentAuthority.issue()` must independently enforce the same exact TaskContract/WorkRun/state/gate/result/use binding before using HumanResult as semantic input.

Do not rely on a future Human guard check to repair an invalid Judgment.

`JudgmentTransitionParticipant.prepare()` must revalidate these dependencies again under the P1-4 transaction before activating `G_JUDGMENT_*`.

### mandatory PostgreSQL proofs

Create at least two real WorkRuns and prove:

```text
reservation from run A
+ exact PRE_HUMAN attestation for run B
+ gate-open request for run B
→ denied
→ no gate written for A or B by that attempt
→ run B does not transition

current APPROVE result from run A
+ ACCEPT request for run B
→ no G_HUMAN_APPROVED for run B
→ transition denied

current APPROVE result from run A
+ Judgment issue request for run B
→ Judgment rejected
→ no Judgment row/evaluation/event for run B
```

Also prove TaskContract mismatch even when state/version/result kind happen to match.

---

# 5. FINDING-2 — action authority must consume durable current gate authority

Current API must not seal action authority from an arbitrary caller-constructed `HumanGate` dataclass.

Refactor to one accepted equivalent:

```text
A. issue action authority by exact gate ref
   → P1-7 repository loads current durable gate
   → verifies event/projection/current WorkRun
   → seals action authority

or

B. use a private unforgeable CurrentHumanGateAuthority capability
   that only the P1-7 durable repository/authority can issue
```

Preferred V1 is A unless accepted architecture strongly favors B.

Required validation before action authority issuance:

```text
gate exists
gate fingerprint/current projection reconstructs
gate.status = PENDING
gate.suspension_status = ACTIVE
gate not expired
gate TaskContract/WorkRun/current state-version are authoritative
principal is authenticated/current
principal selector/role policy is satisfied
```

Do not trust:

```text
plain HumanGate dataclass
caller gate status
caller WorkRun binding
caller gate revision
```

### mandatory proof

Construct a fake `HumanGate` value that uses:

```text
a real gate serialized ref
but a different WorkRun/state/version or policy binding
```

and prove it cannot produce usable `HumanActionAuthority`.

A caller-created arbitrary gate ref must also fail.

---

# 6. FINDING-3 — complete Judgment policy authority

## 6.1 TaskContract/use-bound policy

`JudgmentPolicy` or exact equivalent must bind enough current authority to prove:

```text
policy is the exact policy for this TaskContract id/version

policy applies to this source WorkflowState/state_version-independent use definition

policy applies to exact target / transition-purpose

owner_policy is exact

policy id/version/fingerprint are exact

policy authority id/version/revision are current
```

Do not let one server-issued policy object silently apply to unrelated TaskContracts.

The policy may be an immutable TaskContract-owned snapshot/registry entry. If a durable policy row is required for restart/currentness, add it using existing PostgreSQL/Alembic conventions.

Do not create P1-8 memory authority.

## 6.2 three owner policies must be semantically distinct

Exact accepted owner vocabulary:

```text
SYSTEM_DETERMINISTIC
HUMAN
COMMAND_CENTER
```

Required semantics:

```text
SYSTEM_DETERMINISTIC
→ versioned deterministic System rule
→ no HumanResult substitution

HUMAN
→ exact current HumanResult semantic input as accepted

COMMAND_CENTER
→ exact server-owned Command Center principal/action/policy authority input
→ HumanResult must not silently substitute for Command Center authority
```

Implement a narrow P1-7 local/server-owned `COMMAND_CENTER` authority abstraction sufficient for current runtime proof.

No external identity provider, browser action, P1-8, or public deployment is required.

Caller text:

```text
owner_policy="COMMAND_CENTER"
principal="command-center"
approved=true
```

must not create Command Center authority.

## 6.3 policy currentness at Judgment issue and guard use

At both:

```text
Judgment issuance
G_JUDGMENT_* transaction-time prepare
```

revalidate current policy authority/applicability.

If policy version/revision/use changed or was superseded:

```text
old Judgment guard
→ unusable
```

The `JudgmentGuardAttestation` must bind exact policy authority id/version/revision in addition to policy id/version/fingerprint if needed to satisfy the accepted design.

### mandatory proofs

```text
Human policy for Task A reused on Task B
→ rejected

Human policy for target ACCEPTED reused for REJECTED
→ rejected

SYSTEM_DETERMINISTIC without exact current deterministic policy
→ rejected

COMMAND_CENTER without exact Command Center authority
→ rejected

COMMAND_CENTER with a HumanResult only
→ rejected

exact current COMMAND_CENTER server-owned authority
→ Judgment may issue for its exact Task/use

policy superseded after Judgment issue
→ old G_JUDGMENT_* unusable after restart too
```

---

# 7. FINDING-4 — Judgment immutable-ID identity conflict

Before returning an existing Judgment for the same `judgment_id`, compute or reconstruct the complete proposed immutable fingerprint.

Required:

```text
same judgment_id + same canonical fingerprint
→ return same immutable Judgment

same judgment_id + different canonical fingerprint
→ identity conflict
→ no new JudgmentEvaluation
→ no new JudgmentAuthorityEvent
→ current projection unchanged
```

Canonical identity must cover all immutable semantic inputs, including exact equivalents of:

```text
judgment_version
request Task/run/source state/version/target-use
policy id/version/fingerprint/authority revision
HumanResult/gate dependencies
P1-6 evidence dependency
judgment kind derivation inputs
reason code/vocabulary
supersedes_judgment_ref
```

Use a durable sanitized reason consistent with the accepted taxonomy.

### mandatory proofs

Same `judgment_id` with each materially changed input must not silently return old truth.

At least prove:

```text
different HumanResult
different policy
different target/use
different reason
different supersedes ref
```

causes identity conflict.

---

# 8. FINDING-5 — enforce HumanGate expiry as authority

Use a System-owned/injectable clock. Caller `TransitionRequest.created_at`, client timestamps, or submitted timestamps are not current-time authority.

## 8.1 gate-open expiry

Before `G_HUMAN_REQUIRED` is activated and again inside the shared transaction:

```text
reservation/gate expires_at is null
or
system_now < expires_at
```

Else:

```text
no G_HUMAN_REQUIRED
no gate open
no HUMAN_REQUIRED transition
```

## 8.2 pending gate expiry lifecycle

When a current `PENDING` gate is discovered expired under the WorkRun lock:

```text
append expiry authority event
→ reason HUMAN_GATE_EXPIRED
→ projection CANCELLED / NOT_APPLICABLE
→ authority revision increment
```

Do not add a sixth lifecycle status.

Make this idempotent under concurrent expiry discovery.

## 8.3 action/result/guard expiry

Require non-expiry for:

```text
HumanActionAuthority issuance

HumanResult admission while gate is pending

G_HUMAN_* guard use according to accepted design

G_RESUMABLE_HUMAN_GATE where applicable
```

If a HumanResult was already durably admitted before expiry, follow the accepted design's exact gate/result/guard semantics. At minimum a guard attestation carrying `expires_at` must not be recognized after its expiry.

Do not silently extend expiry because a result exists.

## 8.4 proof

Use deterministic server clock proof:

```text
expired reservation before gate open
→ denied / no gate

pending gate expires
→ one additive expiry event
→ CANCELLED projection
→ duplicate expiry check adds no second authority event

action authority after gate expiry
→ rejected

result submit after gate expiry
→ rejected

G_HUMAN_* after attestation/gate expiry
→ rejected

restart
→ expired/cancelled authority remains unusable
```

---

# 9. preserve P1-6 / P1-4 boundaries

Do not fix these findings by:

```text
changing WorkflowState set
changing P1-4 transition matrix
allowing P1-7 direct WorkRun update
reimplementing P1-6 evidence truth
using HumanResult as AdmittedEvidence
using COMMAND_CENTER as P1-8 memory
```

P1-4 remains sole transition owner.

P1-6 remains sole evidence admission owner.

---

# 10. directly affected persistence

Existing migration `20260829_0004` is still an uncommitted candidate.

If schema changes are required, update this same candidate migration rather than creating a second P1-7 migration unless repository migration policy forces a new revision.

Potentially required durable concepts may include exact equivalents of:

```text
JudgmentPolicy snapshot/current authority
CommandCenter judgment action/principal authority ref
policy authority revision
expiry event payload/reason
additional Task/run binding constraints
```

Do not add tables merely for convenience if exact currentness can be derived from already durable System-owned TaskContract policy.

Any added policy authority must be restart-reconstructable and fail closed.

---

# 11. correction/restart integrity regression

Preserve already working behavior:

```text
FIRST_DURABLY_ADMITTED

Human gate correction/supersession
old HUMAN_P1_7 producer invalidation

Judgment correction/supersession

P1-6 PRE_HUMAN binding
empty applicable subset path

P1-4 atomic transition participant integration

sanitized public Human projection
```

Add result/Judgment consistency checks where needed so restart does not trust cross-scope or corrupted authority.

Do not weaken append-only history.

---

# 12. mandatory proof matrix for this rework

Fresh proof is required for:

```text
CROSS_SCOPE_GATE_RESERVATION_REJECT

CROSS_SCOPE_HUMAN_RESULT_GUARD_REJECT

CROSS_SCOPE_JUDGMENT_INPUT_REJECT

CURRENT_GATE_ACTION_AUTHORITY

JUDGMENT_POLICY_TASK_USE_BINDING

COMMAND_CENTER_JUDGMENT_AUTHORITY

JUDGMENT_IDEMPOTENCY_CONFLICT

HUMAN_GATE_EXPIRY

GUARD_EXPIRY

RESTART_POLICY_AND_EXPIRY

PREDECESSOR_P1_7_REGRESSION
P1_4_REGRESSION
P1_6_REGRESSION
```

Also rerun the predecessor proof categories affected by these changes:

```text
HUMAN_GATE_AUTHORITY
HUMAN_PRINCIPAL_AUTHORITY
HUMAN_RESULT_STALENESS
JUDGMENT_AUTHORITY
G_HUMAN_BINDING
G_JUDGMENT_BINDING
GUARD_ANTI_REPLAY
RESTART
SECURITY_EXPORT
```

---

# 13. mandatory negative examples

At minimum prove:

```text
foreign reservation A → request B
→ no gate / no transition

foreign result A → Human guard request B
→ no guard / no transition

foreign result A → Judgment request B
→ no Judgment

fake HumanGate object
→ no action authority

wrong TaskContract policy
→ no Judgment

wrong target-use policy
→ no Judgment

COMMAND_CENTER + HumanResult only
→ no Command Center Judgment

caller text pretending Command Center principal
→ no authority

same judgment_id + changed immutable input
→ identity conflict

expired gate-open reservation
→ no gate / no transition

expired pending gate
→ CANCELLED via additive expiry event

expired Human guard
→ no transition
```

Positive cases must still prove each exact legitimate path.

---

# 14. concurrency proofs

Use PostgreSQL real concurrency for:

```text
foreign/correct reservation attempts cannot cross-bind under concurrent runs

two HumanResult submissions still FIRST_DURABLY_ADMITTED

expiry discovery racing HumanResult submit
→ exactly one legal outcome:
   result admitted before authoritative expiry
   OR expiry cancellation wins and result rejected

policy supersession racing G_JUDGMENT_* use
→ stale policy Judgment cannot admit transition

same Judgment ID concurrent same fingerprint
→ one immutable Judgment identity

same Judgment ID concurrent different fingerprint
→ one winner + one identity conflict
```

Correctness must not depend on process-local dict/token state alone.

---

# 15. allowed paths

Primary current candidate:

```text
migrations/versions/20260829_0004_p1_7_human_gate_judgment.py

src/aiscc/human/**
src/aiscc/judgment/**

src/aiscc/evidence/issuers.py
src/aiscc/evidence/repository.py

src/aiscc/persistence/models.py
src/aiscc/persistence/repository.py

src/aiscc/workflow/__init__.py
src/aiscc/workflow/kernel.py
src/aiscc/workflow/participants.py
src/aiscc/workflow/ports.py

tests/unit/human/**
tests/integration/human/**
tests/integration/workflow/test_postgres_kernel.py
```

Add narrow P1-7 judgment-specific test directories if clearer:

```text
tests/unit/judgment/**
tests/integration/judgment/**
```

No other source root unless a concrete accepted-design integration requirement demands it.

Governance/report:

```text
.aiassistant/records/aiscc/cycles/
20260830_0051_aiscc-p1-7-runtime-authority-binding-policy-expiry-hold-1.cycle.md

.aiassistant/tasks/active/
20260830_0051_aiscc-p1-7-cross-scope-policy-idempotency-expiry-runtime-rework-1.md

.aiassistant/tasks/done/
20260830_0051_aiscc-p1-7-cross-scope-policy-idempotency-expiry-runtime-rework-1.md

.aiassistant/reports/target/
20260830_0051_aiscc-p1-7-cross-scope-policy-idempotency-expiry-runtime-rework-1/**
```

---

# 16. forbidden

Do not modify accepted design/canonical state:

```text
.aiassistant/rules/AISCC_HUMAN_GATE_JUDGMENT.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/records/aiscc/cycles/
20260829_2328_aiscc-p1-7-human-gate-and-judgment-design-final-acceptance-1.cycle.md
```

No:

```text
P1-8 source
WorkflowState/transition matrix change
real external IdP
real provider call
external credential/network action
public Live
deployment
git add
git commit
git push
```

This rework remains uncommitted.

---

# 17. evidence contract

## executor_required

```text
STATIC_SOURCE

UNIT_TEST

POSTGRESQL_INTEGRATION

CROSS_SCOPE_BINDING

CURRENT_GATE_AUTHENTICITY

JUDGMENT_POLICY_AUTHORITY

COMMAND_CENTER_AUTHORITY

JUDGMENT_IDEMPOTENCY

EXPIRY_LIFECYCLE

CONCURRENCY

RESTART

SECURITY_EXPORT

DIRECTLY_AFFECTED_REGRESSION
```

## reuse_allowed

Reuse predecessor evidence only for unchanged behavior.

The predecessor:

```text
3 P1-7 PASS
61 directly affected predecessor regression PASS
```

does not close any new finding without fresh negative proof.

## human_owned

```text
P1-7 runtime final acceptance
→ HUMAN_PENDING
```

## not_required

```text
browser QA
frontend
real IdP
real provider
deployment
public release
production/test server
```

## forbidden

```text
P1-8
policy override
direct WorkflowState mutation
real provider
credentialed external action
runtime Git commit
```

---

# 18. export provenance correction

New `EXPORT_MANIFEST.md` must compute every SHA from actual copied bytes.

Required validation:

```text
all SHA strings exactly 64 lowercase hex

every manifest SHA == exported file SHA

source/copy byte identity explicitly verified

aggregate SHA generated from actual exported changed-file bytes
```

The report must explicitly record the predecessor manifest defect:

```text
old issuers.py manifest SHA:
8f07c8eb14c78a887af73996a06f3f2c4d41fb3a7178f860e3540a575f9d9f5
→ INVALID / 63 chars

actual predecessor exported SHA:
8f07c8eb14c78a77cac6b7d0400733f2c4d41fb3a7178f860e3540a575f9d9f5
```

Do not alter the old ignored target bundle in place solely to hide historical evidence.

---

# 19. mandatory stop

STOP on:

```text
HEAD drift

accepted design SHA drift

predecessor 19-path aggregate drift

need to change accepted P1-7 design

need to change P1-4 transition matrix

need to change P1-6 evidence authority semantics

COMMAND_CENTER authority requires P1-8 or external identity system contrary to current design

unrelated dirty collision

external credential/network requirement
```

If an accepted design contradiction is discovered:

```text
STOP
→ POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

Do not silently reinterpret it.

---

# 20. accept criteria

All must hold:

```text
foreign reservation cannot open another run's gate

foreign HumanResult cannot satisfy another run's Human guard

foreign HumanResult cannot produce another run's Judgment

HumanActionAuthority requires a current durable server-owned gate

fake/caller-built HumanGate cannot mint action authority

Judgment policy is exact TaskContract/use bound

SYSTEM_DETERMINISTIC / HUMAN / COMMAND_CENTER are distinct

COMMAND_CENTER requires exact server-owned Command Center authority

policy stale/superseded → old Judgment guard unusable

same Judgment ID + same fingerprint idempotent

same Judgment ID + different fingerprint conflict

gate expiry enforced on open/action/result/guard paths

pending expiry creates exactly one additive cancellation authority event

restart preserves policy/expiry/current authority

previous P1-7 positive flow still passes

P1-4/P1-6 directly affected regression passes

P1-8 remains NOT_STARTED

real provider/network/credential actions = 0

Stage 1 Git commit = none
```

---

# 21. report requirements

Report exact:

1. task path
2. start/final HEAD
3. accepted design SHA
4. predecessor 19-path aggregate verification
5. corrected predecessor `issuers.py` SHA finding
6. HOLD Cycle placement
7. reservation/request binding fix
8. result/gate/request cross-scope fix
9. Judgment HumanResult cross-scope fix
10. current durable gate action-authority fix
11. Judgment policy TaskContract/use model
12. COMMAND_CENTER authority model
13. policy currentness/restart model
14. Judgment identity-conflict implementation
15. expiry clock/authority model
16. expiry event/projection semantics
17. migration changes
18. fresh negative proof item-by-item
19. concurrency proof
20. restart proof
21. predecessor P1-7 regression
22. P1-4 regression
23. P1-6 regression
24. security/export result
25. provider/network/credential actions
26. P1-8 source creation = none
27. Git commit = none
28. workspace after
29. human verification = HUMAN_PENDING
30. new export SHA/aggregate validation
31. preserved exact paths
32. next recommendation

---

# 22. target bundle

Create:

```text
.aiassistant/reports/target/
20260830_0051_aiscc-p1-7-cross-scope-policy-idempotency-expiry-runtime-rework-1/
```

Required:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
```

Include:

```text
all changed runtime/test/migration files
2045-style historical correction is not relevant; do not copy unrelated cycles
current 0051 HOLD Cycle
```

Preserve repository-relative paths.

---

# 23. lifecycle / Git

Start:

```text
.aiassistant/tasks/active/
20260830_0051_aiscc-p1-7-cross-scope-policy-idempotency-expiry-runtime-rework-1.md
```

Finish:

```text
.aiassistant/tasks/done/
20260830_0051_aiscc-p1-7-cross-scope-policy-idempotency-expiry-runtime-rework-1.md
```

No Git add/commit/push is authorized.

Expected final HEAD remains:

```text
c87cfc75f14476e10b4a02a2ab0bd295720a85a0
```

---

# 24. preserved exact paths

Must preserve:

```text
.aiassistant/rules/
AISCC_HUMAN_GATE_JUDGMENT.md

.aiassistant/records/aiscc/cycles/
20260829_2328_aiscc-p1-7-human-gate-and-judgment-design-final-acceptance-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260830_0051_aiscc-p1-7-runtime-authority-binding-policy-expiry-hold-1.cycle.md

.aiassistant/tasks/done/
20260829_2328_aiscc-p1-7-design-terminal-persistence-and-runtime-implementation-1.md

.aiassistant/tasks/done/
20260830_0051_aiscc-p1-7-cross-scope-policy-idempotency-expiry-runtime-rework-1.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

---

# 25. final state

Successful Executor rework submission:

```text
P1-7 Design:
ACCEPTED / CLOSED

P1-7 Runtime:
REWORKED_CANDIDATE / HUMAN_PENDING

P1-8:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

Next action:

```text
Command Center runtime re-review
→ Human final P1-7 runtime review only after PASS
```
