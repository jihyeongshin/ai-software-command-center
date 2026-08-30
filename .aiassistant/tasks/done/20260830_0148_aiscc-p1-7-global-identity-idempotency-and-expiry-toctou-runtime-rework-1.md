# 작업지시서: P1-7 Global Identity / Idempotency / Expiry TOCTOU Runtime Rework

## meta

- task_id: `20260830_0148_aiscc-p1-7-global-identity-idempotency-and-expiry-toctou-runtime-rework-1`
- created_at: `2026-08-30T01:48:00+09:00`
- phase: `P1-7 Human Gate and Judgment`
- work_type: `REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1-7_HUMAN_JUDGMENT`
- expected_start_head: `c87cfc75f14476e10b4a02a2ab0bd295720a85a0`
- accepted_design_commit: `238b0b41460c2504fd3244eadb06809d8692a60f`
- accepted_design_terminal_commit: `c87cfc75f14476e10b4a02a2ab0bd295720a85a0`
- accepted_design_sha256: `22851cd0a6476fe613a3cc7a86a4096ace7236b4bafdd3c7c5a25e701a3b1549`
- predecessor_runtime_path_count: `19`
- predecessor_runtime_aggregate_sha256: `c486fa6deb84a18ec2b52d56a64981e8ca557653dc26f31ab920784d13773b91`
- p1_7_runtime_status: `REWORK_REQUIRED / HUMAN_PENDING`
- p1_8_status: `NOT_STARTED`
- public_bounded_live_release: `NOT_RELEASED`

---

# 1. current state

The previous 0051 rework successfully closes its original findings.

Do NOT reopen without direct regression cause:

```text
cross-scope reservation/result/Judgment binding
durable current-gate action authority
TaskContract/use-bound Judgment policy
SYSTEM_DETERMINISTIC / HUMAN / COMMAND_CENTER separation
Command Center server-owned action authority
policy currentness/supersession
gate expiry lifecycle/event/projection
export SHA provenance
```

Preserve accepted design and Stage 0 commits:

```text
238b0b41460c2504fd3244eadb06809d8692a60f
c87cfc75f14476e10b4a02a2ab0bd295720a85a0
```

Current P1-7 runtime remains uncommitted.

Command Center judgment:

```text
HOLD_REWORK_REQUIRED
```

Place/preserve:

```text
.aiassistant/records/aiscc/cycles/
20260830_0148_aiscc-p1-7-runtime-idempotency-global-identity-and-expiry-toctou-hold-1.cycle.md
```

---

# 2. predecessor verification

Before mutation verify:

```text
HEAD ==
c87cfc75f14476e10b4a02a2ab0bd295720a85a0

accepted design SHA ==
22851cd0a6476fe613a3cc7a86a4096ace7236b4bafdd3c7c5a25e701a3b1549

current 19-path runtime aggregate ==
c486fa6deb84a18ec2b52d56a64981e8ca557653dc26f31ab920784d13773b91
```

If runtime candidate differs before this rework:

```text
STOP
→ REVIEWED_CANDIDATE_DRIFT
```

Task/HOLD/report governance files are outside the 19 runtime identity.

---

# 3. load-bearing invariants

Preserve:

```text
HumanResult != Judgment

HumanResult/Judgment != WorkflowState

Judgment != TransitionDecision

HUMAN_DIRECT_EVIDENCE != HUMAN_P1_7

P1-4 owns TransitionDecision / WorkflowState mutation

P1-6 owns Evidence admission / G_EVIDENCE

P1-7 owns Human/Judgment authority

FIRST_DURABLY_ADMITTED
→ current HumanResult winner rule

same immutable ID + same proposal
→ same immutable object

same immutable ID + different proposal
→ typed identity conflict

stale historical object
!= current effective guard authority
```

---

# 4. FINDING-1 — move expiry current-time authority inside the canonical lock

## 4.1 rule

For any authority decision that depends on:

```text
now < HumanGate.expires_at
now < principal/action expiry
now < Human/Judgment guard expiry
```

the authoritative `now` must be sampled from the injected server clock **after** the canonical
transaction locks needed for that decision have been acquired.

A pre-lock time may be used only for non-authoritative diagnostics/provenance.

Required:

```text
pre-lock timestamp
!= current-time authority
```

## 4.2 action authority issuance

Current gate action issuance must perform equivalent order:

```text
BEGIN

resolve gate ref enough to find work_run_id

acquire run:{work_run_id} advisory transaction lock

SELECT WorkRun / HumanGate / projection FOR UPDATE

authoritative_now = server_clock()

reconstruct current gate authority

expire pending gate if authoritative_now >= expires_at

validate principal currentness using authoritative_now

issue action only if all authority remains current
```

The final action authority `issued_at` should be this authoritative locked time.

Its expiration must not silently outlive any stricter accepted authority bound if the design requires
a shorter effective deadline.

## 4.3 HumanResult admission

Remove the correctness dependency on:

```text
expire_gate_if_needed()
```

as a separate preflight transaction.

It may remain as a standalone maintenance operation, but `submit_result()` itself must atomically:

```text
acquire current WorkRun lock

lock WorkRun / gate / projection

authoritative_now = server_clock()

verify/expire current pending gate in the same transaction

verify principal/action expiry using authoritative_now

then evaluate existing/new HumanResult identity
and admission according to the exact ordering frozen below
```

No window may exist where:

```text
preflight says unexpired
→ clock crosses expires_at
→ result transaction uses old time
```

## 4.4 deterministic race proof

Use a controllable server clock and a deterministic lock holder.

Required PostgreSQL proof:

```text
gate expires at T5

result/action operation starts at T4
→ captures no authoritative time yet
→ blocks behind canonical WorkRun lock

clock advanced to T6

lock released

operation acquires lock
→ authoritative_now = T6
→ expiry wins
→ no action/result admitted
```

Also prove:

```text
operation acquires canonical lock at T4
and authoritative_now = T4
→ operation may legally win according to accepted transaction semantics
```

Do not use timing sleeps as the only proof; coordinate the lock/race deterministically.

---

# 5. FINDING-2 — global immutable HumanResult-ID serialization

`human_result_id` is a global immutable identity.

Add a PostgreSQL transaction-level serialization boundary for the exact HumanResult ID.

Preferred equivalent:

```text
pg_advisory_xact_lock(
  hashtextextended("aiscc:p1-7:human-result:{human_result_id}", 0)
)
```

or an existing canonical equivalent.

## 5.1 lock ordering

Freeze one deterministic order and use it everywhere.

Recommended:

```text
1. WorkRun advisory lock
2. HumanResult-ID advisory lock
3. WorkRun/gate/result rows FOR UPDATE as required
```

No code path may acquire the HumanResult-ID lock first and later acquire the WorkRun lock.

If a different ordering is required by existing architecture, document and test it.

## 5.2 behavior

After both semantic and object-identity serialization:

```text
existing same ID + same proposal fingerprint
→ same immutable HumanResult

existing same ID + different proposal fingerprint
→ HUMAN_RESULT_IDENTITY_CONFLICT

new ID
→ normal current-authority admission

raw IntegrityError / UniqueViolation
→ must not be the intended authority outcome
```

A DB constraint remains defense-in-depth, not the semantic concurrency mechanism.

## 5.3 cross-WorkRun proof

Create two different current WorkRuns and concurrently submit:

```text
same human_result_id
different gate / WorkRun
therefore different proposal fingerprint
```

Required:

```text
exactly one may create the global identity
other:
HUMAN_RESULT_IDENTITY_CONFLICT

no raw DB integrity exception
no duplicate result/event
both WorkRun/gate projections remain provenance-consistent
```

Also test same global ID + same proposal through concurrent retries when applicable.

---

# 6. FINDING-3 — global immutable Judgment-ID serialization

Apply the same object-identity rule to:

```text
judgments.judgment_id
```

Recommended additional lock:

```text
aiscc:p1-7:judgment:{judgment_id}
```

with deterministic lock ordering:

```text
WorkRun lock
→ Judgment-ID lock
→ policy lock / rows
```

or another documented order that does not deadlock with policy registration/use.

Required cross-WorkRun proof:

```text
WorkRun A
WorkRun B

same judgment_id
different request/work_run → different proposal fingerprint

concurrent issue:
→ exactly one immutable global ID winner
→ other JUDGMENT_IDENTITY_CONFLICT
→ no raw DB unique/integrity exception
```

Same-ID/same-fingerprint concurrent retry must remain one immutable response.

---

# 7. FINDING-4 — split HumanResult proposal identity from server-generated timestamps

Current `human_result_fingerprint` uses the final `submitted_at` value, where omitted caller time is replaced
with server `admitted_at`.

That makes an exact retry with omitted `submitted_at` non-idempotent.

Freeze a clear two-level identity model equivalent to the Judgment implementation:

```text
proposal_fingerprint
→ immutable caller/request inputs only

HumanResult final fingerprint
→ complete durable immutable body
```

## 7.1 proposal fingerprint

Must include exact immutable request inputs such as:

```text
human_result_id/version
gate ref + expected gate authority revision
authenticated principal/action identity
result kind
structured reason / vocabulary
private content refs/hashes/sensitivity
idempotency key

caller submitted_at:
- explicit value if caller supplied one and accepted contract treats it as immutable input
- explicit null/ABSENT marker if omitted
```

Must NOT substitute:

```text
server admitted_at
server current time
```

for an omitted caller field inside proposal identity.

## 7.2 durable result

The final HumanResult may still record:

```text
submitted_at
admitted_at
```

according to accepted provenance semantics.

If caller omitted `submitted_at`, persist a deterministic explicit source marker or server-observed value,
but keep proposal identity stable across retries.

Persist the proposal fingerprint durably so an existing result can be compared without reconstructing
a server-generated timestamp.

## 7.3 proofs

```text
same result ID
same inputs
submitted_at omitted
server clock advances
retry
→ same immutable HumanResult

same result ID
explicit submitted_at changed
→ identity conflict if explicit submitted_at is immutable input

same result ID
reason/result/gate/action/idempotency changed
→ identity conflict

same proposal retry after gate becomes resolved
→ returns historical immutable result
→ does not reopen or mutate gate authority
```

---

# 8. FINDING-5 — Judgment immutable replay before current-effectiveness checks

The existence/identity path must be separated from current-authority issuance.

## 8.1 required ordering

Compute the proposed immutable `proposal_fingerprint` from supplied immutable request inputs without
requiring the current policy/WorkRun to still be effective.

Under the WorkRun + Judgment-ID serialization boundary:

```text
existing Judgment with same judgment_id:

  proposal fingerprint same
  → return exact immutable historical Judgment
  → no new evaluation/event/projection mutation

  proposal fingerprint different
  → JUDGMENT_IDENTITY_CONFLICT
  → no new authority mutation

only when no existing Judgment:
  → perform current WorkRun
  → current policy
  → Human/CommandCenter/evidence authority checks
  → issue new Judgment
```

If cross-WorkRun global-ID serialization requires locating an existing Judgment before choosing a WorkRun
lock strategy, do not invent unsafe lock inversion. Keep the Task's deterministic lock ordering and use a
narrow global Judgment-ID lock after the request WorkRun lock; once held, compare the durable existing row.

## 8.2 current effectiveness remains separate

Returning an existing historical Judgment does NOT mean it is effective for transition.

Existing current-use path must continue to enforce:

```text
current WorkRun state/version
current policy authority
current HumanResult/gate
current Command Center action where applicable
current P1-6 evidence
current Judgment projection/revision
guard expiry
```

through `JudgmentTransitionParticipant.prepare()`.

Required:

```text
immutable replay
!= guard replay authority
```

## 8.3 proofs

```text
issue Judgment X

supersede its policy
retry exact same immutable proposal X
→ same historical Judgment X returned

attempt to use X after policy supersession
→ G_JUDGMENT_* denied

issue Judgment Y
transition WorkRun to new state/version
retry exact same immutable proposal Y
→ same historical Y returned

attempt to use Y for new state/version
→ denied

same ID + changed policy/request/reason/result/evidence/CommandCenter/supersedes
→ identity conflict
```

---

# 9. preserve prior 0051 closures

Fresh regression must prove these remain closed:

```text
foreign reservation A → request B denied

foreign HumanResult A → guard B denied

foreign HumanResult A → Judgment B denied

fake/caller-built HumanGate cannot mint action authority

Task/use-mismatched Judgment policy denied

COMMAND_CENTER cannot be substituted by HumanResult/text

policy supersession invalidates old Judgment guard

pending gate expiry:
one additive EXPIRED event
CANCELLED / NOT_APPLICABLE projection

guard after expiry denied

P1-6 PRE_HUMAN exact binding retained

FIRST_DURABLY_ADMITTED retained
```

Do not weaken any of them while changing lock/idempotency ordering.

---

# 10. persistence / migration

The current `20260829_0004` migration is still an uncommitted P1-7 candidate.

If a durable HumanResult proposal fingerprint needs a new column/payload key, update the same candidate migration.

Prefer payload storage when it is sufficient and immutable/validated by existing append-only rules; use a
column only if indexing/uniqueness/query requirements justify it.

Advisory object locks require no schema solely for locking.

Do not create a second P1-7 migration unless repository migration policy requires it.

---

# 11. required concurrency proofs

Use real PostgreSQL and deterministic coordination.

Fresh:

```text
EXPIRY_LOCK_TIME_AUTHORITY

CROSS_WORKRUN_HUMAN_RESULT_ID_CONFLICT

CROSS_WORKRUN_JUDGMENT_ID_CONFLICT

HUMAN_RESULT_OMITTED_TIMESTAMP_IDEMPOTENCY

JUDGMENT_HISTORICAL_IDEMPOTENT_REPLAY
```

Rerun:

```text
FIRST_DURABLY_ADMITTED

expiry discovery vs result submit

same WorkRun Judgment same-ID/same-fingerprint

same WorkRun Judgment same-ID/different-fingerprint

policy supersession vs Judgment guard use

cross-scope reservation/result/Judgment proofs
```

No correctness proof may rely only on Python process-local locks.

---

# 12. allowed paths

Primary:

```text
migrations/versions/20260829_0004_p1_7_human_gate_judgment.py

src/aiscc/human/**
src/aiscc/judgment/**

src/aiscc/persistence/models.py
src/aiscc/persistence/repository.py

tests/unit/human/**
tests/integration/human/**
tests/unit/judgment/**
tests/integration/judgment/**
tests/integration/workflow/test_postgres_kernel.py
```

Narrow existing integration only if actually required:

```text
src/aiscc/workflow/**
src/aiscc/evidence/**
tests/integration/evidence/**
```

Governance/report:

```text
.aiassistant/records/aiscc/cycles/
20260830_0148_aiscc-p1-7-runtime-idempotency-global-identity-and-expiry-toctou-hold-1.cycle.md

.aiassistant/tasks/active/
20260830_0148_aiscc-p1-7-global-identity-idempotency-and-expiry-toctou-runtime-rework-1.md

.aiassistant/tasks/done/
20260830_0148_aiscc-p1-7-global-identity-idempotency-and-expiry-toctou-runtime-rework-1.md

.aiassistant/reports/target/
20260830_0148_aiscc-p1-7-global-identity-idempotency-and-expiry-toctou-runtime-rework-1/**
```

---

# 13. forbidden

Do not modify:

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

WorkflowState or transition-matrix change

P1-6 evidence semantics change

real provider / external IdP / credentialed network

deployment / Public Live

git add / commit / push
```

Runtime remains an uncommitted review candidate.

---

# 14. evidence contract

## executor_required

```text
STATIC_SOURCE

UNIT_TEST

POSTGRESQL_INTEGRATION

EXPIRY_LOCK_TIME_AUTHORITY

GLOBAL_HUMAN_RESULT_IDENTITY

GLOBAL_JUDGMENT_IDENTITY

HUMAN_RESULT_PROPOSAL_IDEMPOTENCY

JUDGMENT_HISTORICAL_REPLAY

CONCURRENCY

RESTART

SECURITY_EXPORT

PREDECESSOR_P1_7_REGRESSION

P1_4_REGRESSION

P1_6_REGRESSION
```

## reuse_allowed

The 0051 executor evidence may be reused only for unchanged behavior and only after fresh regression proves
the new lock/idempotency ordering did not invalidate it.

## human_owned

```text
P1-7 runtime final acceptance
→ HUMAN_PENDING
```

## forbidden

```text
P1-8
direct WorkflowState mutation
real provider/network/credentials
runtime Git commit
```

---

# 15. mandatory stop

STOP on:

```text
HEAD drift

accepted design SHA drift

predecessor 19-path aggregate drift

need to modify accepted P1-7 design

global identity lock ordering conflicts with P1-4 WorkRun/policy lock ordering

need to change P1-6 evidence truth

unrelated dirty collision

external credential/network requirement
```

If safe lock ordering cannot be established:

```text
STOP
→ POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

Do not rely on catching `IntegrityError` as the primary authority mechanism.

---

# 16. accept criteria

All must hold:

```text
action/result expiry current-time decision sampled after canonical lock

pre-lock clock cannot admit expired authority after waiting

same HumanResult ID across different WorkRuns is globally serialized

different HumanResult proposal:
typed HUMAN_RESULT_IDENTITY_CONFLICT

same Judgment ID across different WorkRuns is globally serialized

different Judgment proposal:
typed JUDGMENT_IDENTITY_CONFLICT

no raw unique/integrity error used as normal authority result

HumanResult retry with submitted_at omitted remains idempotent across server-time advance

HumanResult explicit immutable input changes remain conflicts

existing Judgment same-proposal replay returns same historical immutable object
even after policy/state currentness changes

stale historical Judgment still cannot satisfy current G_JUDGMENT_*

all 0051 authority/policy/cross-scope/expiry closures regress PASS

P1-4/P1-6 directly affected regression PASS

P1-8 remains NOT_STARTED

provider/network/credential/deployment actions = 0

Git Stage 1 commit = none
```

---

# 17. report requirements

Report exact:

1. task path
2. start/final HEAD
3. accepted design SHA
4. predecessor 19-path aggregate verification
5. 0148 HOLD Cycle placement
6. authoritative clock sampling order before/after
7. action expiry transaction order
8. HumanResult expiry transaction order
9. HumanResult-ID global lock key/order
10. Judgment-ID global lock key/order
11. deadlock-order analysis
12. HumanResult proposal fingerprint model
13. omitted submitted_at behavior
14. Judgment existing-object replay ordering
15. cross-WorkRun HumanResult-ID concurrency proof
16. cross-WorkRun Judgment-ID concurrency proof
17. expiry lock-wait deterministic proof
18. policy/state-changed Judgment replay proof
19. guard stale-use denial proof
20. prior 0051 finding regression
21. P1-4 regression
22. P1-6 regression
23. migration changes
24. PostgreSQL/version/test counts
25. security/export result
26. provider/network/credential actions
27. P1-8 source creation = none
28. Git actions = none
29. final runtime candidate path count / aggregate SHA
30. human verification = HUMAN_PENDING
31. preserved exact paths
32. next recommendation

---

# 18. export

Target:

```text
.aiassistant/reports/target/
20260830_0148_aiscc-p1-7-global-identity-idempotency-and-expiry-toctou-runtime-rework-1/
```

Required:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
```

Include all changed runtime/test/migration files plus the 0148 HOLD Cycle.

Manifest requirements remain:

```text
every SHA = actual copied bytes
64 lowercase hex
source/copy byte identity PASS
runtime aggregate computed from actual exported changed-file bytes
```

---

# 19. lifecycle / Git

Start:

```text
.aiassistant/tasks/active/
20260830_0148_aiscc-p1-7-global-identity-idempotency-and-expiry-toctou-runtime-rework-1.md
```

Finish:

```text
.aiassistant/tasks/done/
20260830_0148_aiscc-p1-7-global-identity-idempotency-and-expiry-toctou-runtime-rework-1.md
```

No Git add/commit/push.

Expected final HEAD:

```text
c87cfc75f14476e10b4a02a2ab0bd295720a85a0
```

---

# 20. preserved exact paths

Must preserve:

```text
.aiassistant/rules/
AISCC_HUMAN_GATE_JUDGMENT.md

.aiassistant/records/aiscc/cycles/
20260829_2328_aiscc-p1-7-human-gate-and-judgment-design-final-acceptance-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260830_0051_aiscc-p1-7-runtime-authority-binding-policy-expiry-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260830_0148_aiscc-p1-7-runtime-idempotency-global-identity-and-expiry-toctou-hold-1.cycle.md

.aiassistant/tasks/done/
20260830_0051_aiscc-p1-7-cross-scope-policy-idempotency-expiry-runtime-rework-1.md

.aiassistant/tasks/done/
20260830_0148_aiscc-p1-7-global-identity-idempotency-and-expiry-toctou-runtime-rework-1.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

---

# 21. final state

Successful rework submission:

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

Next:

```text
Command Center runtime re-review
→ Human final P1-7 runtime review only after PASS
```
