# AISCC Cycle Record

## meta

- cycle_id: `20260830_0148_aiscc-p1-7-runtime-idempotency-global-identity-and-expiry-toctou-hold-1`
- date: `2026-08-30T01:48:00+09:00`
- primary_semantic_owner: `P1-7_HUMAN_JUDGMENT`
- affected_areas: `HumanResult / Judgment / global immutable identity / expiry authority / idempotent replay`
- work_type: `P1_7_RUNTIME_REWORK_REVIEW`
- execution_mode: `MANUAL_COMMAND_CENTER`
- predecessor_task: `20260830_0051_aiscc-p1-7-cross-scope-policy-idempotency-expiry-runtime-rework-1`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause: `AUTHORITY_IDEMPOTENCY_AND_TIME_TOCTOU`
- cycle_record_action: `create`
- source_mirror_sync: `not-required`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260830_0148_aiscc-p1-7-runtime-idempotency-global-identity-and-expiry-toctou-hold-1.cycle.md`

## repository snapshot

- expected current HEAD: `c87cfc75f14476e10b4a02a2ab0bd295720a85a0`
- P1-7 design acceptance commit: `238b0b41460c2504fd3244eadb06809d8692a60f`
- P1-7 design terminal governance commit: `c87cfc75f14476e10b4a02a2ab0bd295720a85a0`
- accepted design SHA-256: `22851cd0a6476fe613a3cc7a86a4096ace7236b4bafdd3c7c5a25e701a3b1549`
- predecessor reworked candidate path count: `19`
- predecessor reworked candidate aggregate SHA-256:
  `c486fa6deb84a18ec2b52d56a64981e8ca557653dc26f31ab920784d13773b91`
- Stage 1 commit: `none`

## predecessor rework review summary

The 0051 rework materially closes the previous Command Center findings.

Accepted as closed:

```text
cross-WorkRun HumanGate reservation substitution
→ CLOSED

cross-WorkRun HumanResult guard substitution
→ CLOSED

cross-WorkRun Judgment HumanResult substitution
→ CLOSED

caller-constructed HumanGate → HumanActionAuthority
→ CLOSED

Judgment policy TaskContract/use binding
→ CLOSED

SYSTEM_DETERMINISTIC / HUMAN / COMMAND_CENTER owner split
→ CLOSED

COMMAND_CENTER durable server-owned action authority
→ CLOSED

Judgment same-ID/different-fingerprint sequential conflict
→ CLOSED for same current authority context

HumanGate expiry lifecycle / guard expiry
→ materially implemented

predecessor export invalid issuers.py SHA
→ corrected in new manifest
```

Verified export provenance:

```text
19 runtime paths
all listed SHA-256:
64 lowercase hex

source/copy byte identity:
PASS

exported runtime aggregate:
c486fa6deb84a18ec2b52d56a64981e8ca557653dc26f31ab920784d13773b91
```

Executor reported:

```text
uv build:
PASS

ruff:
PASS

mypy src:
PASS / 67 source files

targeted unit/integration:
123 PASS

P1-7 focused:
4 PASS

PostgreSQL:
17.6

empty DB → Alembic head:
PASS / 20260829_0004

provider/network/credential/deployment:
0

P1-8:
NOT_STARTED

Git Stage 1 commit:
none
```

These results are admitted as executor evidence but do not close the newly discovered authority gaps below.

---

# FINDING-1 — expiry current-time authority is sampled before the canonical lock

## actual source behavior

`PostgresHumanAuthorityRepository.issue_current_gate_action_authority()` currently does:

```text
issued_at = self._now()

BEGIN transaction
→ load gate
→ acquire run:{work_run_id} advisory lock
→ SELECT gate/run/projection FOR UPDATE
→ _expire_pending_gate_in_session(..., issued_at)
```

The authoritative expiry comparison therefore uses a time captured **before** waiting for the WorkRun lock.

`submit_result()` is more exposed:

```text
admitted_at = self._now()

→ expire_gate_if_needed(gate_ref)
   # separate transaction / lock

→ second transaction
→ acquire WorkRun lock
→ existing/result/gate checks
→ _validate_result_authority(..., admitted_at)
```

`_validate_result_authority()` does not independently compare the durable gate `expires_at`
against a fresh System clock sampled after the WorkRun/gate lock is acquired.

Therefore:

```text
T0:
server clock < gate.expires_at
submit_result captures admitted_at

T1:
another transaction holds WorkRun lock

T2:
server clock crosses gate.expires_at

T3:
submit_result acquires WorkRun lock

current code:
can still evaluate using T0 admitted_at
```

The separate preflight `expire_gate_if_needed()` cannot close this TOCTOU because expiry may occur
after that transaction releases its lock and before the result transaction reaches its authority decision.

The same principle applies to action authority issuance when it waits on the WorkRun lock after
capturing `issued_at`.

Required invariant:

```text
pre-lock time observation
!= authoritative current-time proof
```

For any gate-expiry authority decision, System time used to admit the action/result must be sampled
inside the canonical locked authority transaction after the relevant WorkRun/gate rows are current.

### judgment

```text
HUMAN_GATE_EXPIRY:
PARTIAL / REWORK_REQUIRED

HUMAN_RESULT_STALENESS:
PARTIAL / REWORK_REQUIRED

CURRENT_GATE_ACTION_AUTHORITY:
PARTIAL / REWORK_REQUIRED
```

---

# FINDING-2 — global immutable HumanResult ID is serialized only by WorkRun

`human_results.human_result_id` is a global PostgreSQL primary key.

`submit_result()` serializes with:

```text
run:{action_authority.work_run_id}
```

only.

Two different WorkRuns can therefore concurrently submit the same `human_result_id`:

```text
WorkRun A
→ lock run:A
→ existing HumanResult ID X = none

WorkRun B
→ lock run:B
→ existing HumanResult ID X = none

A and B
→ both attempt global PK X
```

Because the WorkRun locks are independent, the global immutable identity is not serialized.

One transaction may then fail with a raw database uniqueness/integrity error rather than the accepted:

```text
HUMAN_RESULT_IDENTITY_CONFLICT
```

or an immutable same-fingerprint replay.

Required:

```text
global immutable object identity
→ global object-identity serialization
```

WorkRun locking remains necessary for semantic authority, but it is not sufficient for a globally unique
HumanResult ID.

### judgment

```text
HUMAN_RESULT_IDEMPOTENCY:
REWORK_REQUIRED

CONCURRENCY:
REWORK_REQUIRED
```

---

# FINDING-3 — global immutable Judgment ID has the same cross-WorkRun race

`judgments.judgment_id` is also a global PostgreSQL primary key.

`PostgresJudgmentAuthority.issue()` serializes first by:

```text
run:{request.work_run_id}
```

and no Judgment-ID advisory/object lock exists.

The predecessor concurrency tests correctly prove:

```text
same Judgment ID / same WorkRun / same fingerprint
→ one immutable Judgment

same Judgment ID / same WorkRun / different fingerprint
→ one winner + JUDGMENT_IDENTITY_CONFLICT
```

but do not prove the same invariant across two different WorkRuns.

For different WorkRuns:

```text
run:A lock
!= run:B lock
```

so both transactions may observe `JudgmentRow(judgment_id=X) == none` before one global PK insert wins.

Required accepted behavior remains:

```text
same immutable Judgment ID + same fingerprint
→ one immutable identity / same response

same immutable Judgment ID + different fingerprint
→ one winner + JUDGMENT_IDENTITY_CONFLICT

never:
raw database uniqueness failure as authority semantics
```

### judgment

```text
JUDGMENT_IDEMPOTENCY:
REWORK_REQUIRED

CONCURRENCY:
REWORK_REQUIRED
```

---

# FINDING-4 — HumanResult proposal idempotency depends on a server-generated timestamp

Current `submit_result()` derives:

```text
admitted_at = self._now()
submitted = submitted_at or admitted_at
```

and then includes:

```text
submitted_at = submitted.isoformat()
```

inside `human_result_fingerprint`.

Therefore two otherwise identical calls using:

```text
same human_result_id
same gate
same principal/action
same result kind
same reason
same idempotency key
submitted_at omitted
```

produce different fingerprints when the server clock has advanced.

The predecessor positive idempotency test avoids this by explicitly passing the same fixed `submitted_at`
on both calls.

That does not prove the public runtime contract when the optional parameter is omitted.

Required distinction:

```text
caller proposal identity
!= server-generated admitted_at / observation time
```

An omitted caller `submitted_at` must not cause an exact retry to become a different immutable proposal
merely because the server received it later.

A clean implementation may persist both:

```text
proposal_fingerprint
immutable final HumanResult fingerprint
```

or an exact equivalent.

If caller explicitly supplies `submitted_at` and accepted policy treats it as immutable request input,
that explicit value may participate in the proposal fingerprint.

### judgment

```text
HUMAN_RESULT_IDEMPOTENCY:
REWORK_REQUIRED
```

---

# FINDING-5 — Judgment same-fingerprint replay is checked only after current authority validation

The 0051 rework correctly added a `proposal_fingerprint`, but `issue()` currently performs:

```text
load existing Judgment

load current WorkRun
→ reject if stale

verify current JudgmentPolicy
→ reject if stale/superseded

compute proposal_fingerprint

compare existing proposal_fingerprint
```

Thus an exact retry for an already-issued immutable Judgment may fail after:

```text
WorkRun state changes
or
Judgment policy is superseded
```

before the code reaches the immutable same-fingerprint replay path.

Accepted idempotency semantics distinguish:

```text
historical immutable Judgment identity
```

from:

```text
whether that Judgment is still effective for a new P1-4 guard use
```

The latter is already correctly handled by `JudgmentTransitionParticipant.prepare()` through current
WorkRun/policy/Human/evidence checks.

Required:

```text
same judgment_id + exact same proposal_fingerprint
→ return the same immutable historical Judgment
→ no new evaluation/event/projection mutation

current policy/state stale
→ prevents new authority use
→ does not rewrite the historical identity of the existing Judgment
```

Different proposal fingerprint must still produce:

```text
JUDGMENT_IDENTITY_CONFLICT
```

without depending on whether current policy/run authority is still effective.

### judgment

```text
JUDGMENT_IDEMPOTENCY:
REWORK_REQUIRED

GUARD_ANTI_REPLAY:
already separately enforced; must remain so
```

---

# command-center judgment

- result_status: `HOLD_REWORK_REQUIRED`
- P1-7 Design: `REMAINS ACCEPTED / CLOSED`
- Stage 0A commit: `PRESERVE`
- Stage 0B commit: `PRESERVE`
- previous 0051 findings: `CLOSED`
- P1-7 Runtime: `REWORK_REQUIRED / HUMAN_PENDING`
- P1-8: `NOT_STARTED`
- PUBLIC_BOUNDED_LIVE: `NOT_RELEASED`
- Stage 1 runtime commit: `none`
- required rework:
  1. sample expiry authority time only after canonical lock/current-row acquisition;
  2. global HumanResult-ID serialization and deterministic conflict mapping;
  3. global Judgment-ID serialization and deterministic conflict mapping;
  4. separate HumanResult proposal identity from server-generated observation timestamps;
  5. make existing same-fingerprint Judgment replay immutable before current-effectiveness checks.
- terminal_decision_reason: the previous authority substitution/policy/expiry implementation is materially corrected, but immutable identity and time authority still have race/idempotency gaps that can surface as incorrect authority outcomes or raw DB conflicts.

## preservation

Do not amend/revert:

```text
238b0b41460c2504fd3244eadb06809d8692a60f
c87cfc75f14476e10b4a02a2ab0bd295720a85a0
```

Preserve:

```text
.aiassistant/rules/AISCC_HUMAN_GATE_JUDGMENT.md

.aiassistant/records/aiscc/cycles/
20260829_2328_aiscc-p1-7-human-gate-and-judgment-design-final-acceptance-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260830_0051_aiscc-p1-7-runtime-authority-binding-policy-expiry-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260830_0148_aiscc-p1-7-runtime-idempotency-global-identity-and-expiry-toctou-hold-1.cycle.md

.aiassistant/tasks/done/
20260830_0051_aiscc-p1-7-cross-scope-policy-idempotency-expiry-runtime-rework-1.md
```

## next action

```text
P1-7 narrow runtime rework
→ global immutable identity + expiry current-time authority
→ Command Center re-review
→ Human final runtime review only after PASS

P1-8:
NOT_STARTED
```
