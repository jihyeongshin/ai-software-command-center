# AISCC Cycle Record

## meta

- cycle_id: `20260830_0051_aiscc-p1-7-runtime-authority-binding-policy-expiry-hold-1`
- date: `2026-08-30T00:51:00+09:00`
- primary_semantic_owner: `P1-7_HUMAN_JUDGMENT`
- affected_areas: `HumanGate / HumanResult / Judgment / guard authority / policy / expiry / idempotency`
- work_type: `HUMAN_GATE_JUDGMENT_IMPLEMENTATION`
- execution_mode: `MANUAL_COMMAND_CENTER`
- predecessor_task: `20260829_2328_aiscc-p1-7-design-terminal-persistence-and-runtime-implementation-1`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause: `AUTHORITY_BINDING_INCOMPLETE`
- cycle_record_action: `create`
- source_mirror_sync: `not-required`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260830_0051_aiscc-p1-7-runtime-authority-binding-policy-expiry-hold-1.cycle.md`

## repository snapshot

- expected current HEAD: `c87cfc75f14476e10b4a02a2ab0bd295720a85a0`
- P1-7 design acceptance commit: `238b0b41460c2504fd3244eadb06809d8692a60f`
- P1-7 design terminal governance commit: `c87cfc75f14476e10b4a02a2ab0bd295720a85a0`
- accepted design SHA-256: `22851cd0a6476fe613a3cc7a86a4096ace7236b4bafdd3c7c5a25e701a3b1549`
- reviewed Stage 1 candidate paths: `19`
- reviewed Stage 1 candidate aggregate SHA-256, recalculated by Command Center from exported bytes:
  `89bf0a5e60a6bbfd795866eaf838d99f8c5bffb41e3e490dea68537643ed295c`
- Stage 1 commit: `none`

## executor evidence accepted

The predecessor Executor result correctly established:

```text
Stage 0A:
238b0b41460c2504fd3244eadb06809d8692a60f

Stage 0B:
c87cfc75f14476e10b4a02a2ab0bd295720a85a0

P1-7 Design:
HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-7 Runtime:
IMPLEMENTED_CANDIDATE / HUMAN_PENDING

P1-8:
NOT_STARTED
```

Useful executor evidence is admitted for:

```text
PostgreSQL 17.6 local proof
3 P1-7 tests PASS
61 directly affected P1-4/P1-6 regressions PASS
ruff PASS
mypy src/aiscc PASS
migration 20260829_0004 reached head
no provider/network/credential/deployment/public-live action
no P1-8 implementation
no Stage 1 Git commit
```

These pass results do not override current-source authority gaps discovered during Command Center review.

---

# finding 1 — cross-scope Human authority substitution

## 1A. foreign HumanGateReservation can be paired with another transition request

Current `HumanGuardAuthority.gate_open_participant()` verifies only that the reservation was issued by the configured reservation authority.

The transaction-time `prepare()` path verifies:

```text
reservation issuer token
current P1-6 PRE_HUMAN attestation
current request WorkRun
```

but does not require the reservation itself to match the current request's:

```text
TaskContract id/version
work_run_id
source state/version
target state
purpose/use
gate fingerprint/policy
```

`_human_required_attestation()` then combines:

```text
current request identity
+
reservation-derived gate ref
```

and `_open_gate()` persists the gate using reservation fields after P1-4 admits the current request.

Therefore a reservation created for one WorkRun/use can be substituted into another request if both are issued by the same server authority.

Required invariant:

```text
server-issued reservation
!= reservation authorized for every request
```

A gate-open reservation must be exact-use bound.

## 1B. foreign HumanResult can satisfy another WorkRun's `G_HUMAN_*`

Current `result_guard_participant()` and `_result_guard_current()` load the referenced HumanResult/gate and validate that the **request WorkRun itself** is current, but do not require the result/gate TaskContract/WorkRun/source authority to equal the request.

The missing exact comparisons include at least:

```text
result.task_contract_id/version == request
result.work_run_id == request.work_run_id
result.source_state/state_version == request observed authority
gate.task_contract_id/version == request
gate.work_run_id == request.work_run_id
gate.bound_state/state_version == request observed authority
gate purpose/use applicable to request target
```

This allows a same-kind HumanResult from another current resolved gate to be used as the Human guard input for the wrong WorkRun.

## 1C. Judgment accepts a HumanResult from another WorkRun

`PostgresJudgmentAuthority.issue()` validates:

```text
request WorkRun current
HumanResult exists
HumanGate projection resolved/current
```

but does not require the HumanResult/gate to belong to the request TaskContract/WorkRun/state/use.

`JudgmentTransitionParticipant.prepare()` also rechecks the result/gate currentness without enforcing those cross-object bindings.

Thus Human authority from WorkRun A may become a semantic input to a Judgment for WorkRun B.

### judgment

```text
HUMAN_GATE_AUTHORITY:
REJECTED / INCOMPLETE

G_HUMAN_BINDING:
REJECTED / INCOMPLETE

JUDGMENT_AUTHORITY:
REJECTED / INCOMPLETE

G_JUDGMENT_BINDING:
REJECTED / INCOMPLETE
```

---

# finding 2 — HumanActionAuthority can be issued from a caller-constructed HumanGate value

`HumanPrincipalAuthority.issue_action_authority()` accepts a plain `HumanGate` dataclass.

It verifies:

```text
principal issuer token
principal expiry
gate.status == PENDING
gate.suspension_status == ACTIVE
```

but does not resolve/revalidate that HumanGate through durable P1-7 gate authority.

`HumanGate` itself carries no unforgeable issuer token.

A caller with an authenticated principal can construct a `HumanGate` value and ask the server-owned principal authority to seal an action authority from that value.

`submit_result()` later validates the real gate row by `gate_ref`, but `_validate_result_authority()` does not prove the real gate's TaskContract/WorkRun/state identity equals all values carried in the action authority.

Required:

```text
caller-constructed HumanGate object
!= current server-owned HumanGate authority
```

Human action authority issuance must consume a current durable gate ref/authority that P1-7 itself reloads and verifies, or an equivalent unforgeable server-owned current-gate capability.

### judgment

```text
HUMAN_PRINCIPAL_AUTHORITY:
REJECTED / INCOMPLETE
```

---

# finding 3 — Judgment policy authority is not TaskContract/use bound and `COMMAND_CENTER` is not implemented

Accepted design freezes:

```text
SYSTEM_DETERMINISTIC
HUMAN
COMMAND_CENTER
```

and states:

```text
HUMAN
→ admitted/current HumanResult semantic input

COMMAND_CENTER
→ exact Command Center policy/principal authority required

SYSTEM_DETERMINISTIC
→ versioned deterministic policy
```

Current `JudgmentPolicy` contains no exact:

```text
TaskContract id/version
source state
target state / transition-purpose
policy applicability scope
current policy authority revision
Command Center principal/action authority ref
```

`JudgmentPolicyAuthority.seal()` can therefore issue a policy object reusable across unrelated TaskContracts/transition uses.

Current `PostgresJudgmentAuthority.issue()` treats every non-`SYSTEM_DETERMINISTIC` policy by deriving `JudgmentKind` from `HumanResult`.

Consequently:

```text
COMMAND_CENTER
```

exists in the enum but has no distinct Command Center principal/policy authority implementation or proof.

The Judgment guard path also does not revalidate current TaskContract judgment-policy authority at use time; it trusts the policy snapshot already embedded in Judgment.

Required:

```text
policy id/version/fingerprint
!= policy applicable to this TaskContract/use

COMMAND_CENTER enum
!= implemented COMMAND_CENTER authority
```

### judgment

```text
JUDGMENT_AUTHORITY:
REJECTED / INCOMPLETE

G_JUDGMENT_BINDING:
REJECTED / INCOMPLETE
```

---

# finding 4 — Judgment immutable-ID idempotency conflict is not enforced

Accepted design requires:

```text
same immutable request ID + same canonical fingerprint
→ same immutable Judgment response

same immutable request ID + different fingerprint
→ identity conflict
→ no new authority event
```

Current `PostgresJudgmentAuthority.issue()` performs:

```text
existing = session.get(JudgmentRow, judgment_id)

if existing is not None:
    return existing Judgment
```

before calculating or comparing the proposed immutable Judgment fingerprint.

Therefore the same `judgment_id` with different:

```text
request
policy
HumanResult
evidence attestation
reason
supersedes ref
```

can silently return the old Judgment instead of raising identity conflict.

No predecessor test covers same-Judgment-ID/different-fingerprint.

### judgment

```text
JUDGMENT_AUTHORITY / IDEMPOTENCY:
REJECTED / INCOMPLETE
```

---

# finding 5 — HumanGate expiry is stored but not enforced as authority

Accepted design requires:

```text
current gate must be non-expired

HUMAN_GATE_EXPIRED
→ additive expiry authority event
→ CANCELLED projection for a pending gate

wrong/expired Human guard authority
→ verifier reject
```

Current runtime stores `expires_at`, but:

```text
gate-open prepare
does not reject expired reservation/gate use

issue_action_authority
does not check gate.expires_at

submit_result / _validate_result_authority
does not check gate.expires_at

_result_guard_current
does not check guard/gate expiry

_policy_guard_current
does not apply expiry semantics

HUMAN_GATE_EXPIRED
is declared but not used
```

No expiry lifecycle event implementation or expiry-focused test is present.

An action/result/guard can therefore remain usable beyond the accepted gate expiry semantics.

### judgment

```text
HUMAN_GATE_AUTHORITY:
REJECTED / INCOMPLETE

HUMAN_RESULT_STALENESS:
REJECTED / INCOMPLETE

G_HUMAN_BINDING:
REJECTED / INCOMPLETE
```

---

# finding 6 — predecessor export manifest contains one incorrect SHA-256 row

The predecessor export states:

```text
source_and_copy_sha256_check:
28/28 BYTE_IDENTICAL
```

but its Stage 1 table records:

```text
src/aiscc/evidence/issuers.py
8f07c8eb14c78a887af73996a06f3f2c4d41fb3a7178f860e3540a575f9d9f5
```

This value is 63 hexadecimal characters and does not match the exported file bytes.

Command Center recalculation from the attached export gives:

```text
src/aiscc/evidence/issuers.py
8f07c8eb14c78a77cac6b7d0400733f2c4d41fb3a7178f860e3540a575f9d9f5
```

Using the actual exported bytes for all 19 Stage 1 paths, sorted path + tab + lowercase SHA + newline, the reviewed aggregate is:

```text
89bf0a5e60a6bbfd795866eaf838d99f8c5bffb41e3e490dea68537643ed295c
```

This is a target-bundle provenance defect, not a product-source HOLD by itself. The next export must not repeat it.

---

# command-center judgment

- result_status: `HOLD_REWORK_REQUIRED`
- P1-7 design acceptance: `REMAINS ACCEPTED / CLOSED`
- Stage 0A commit: `PRESERVE`
- Stage 0B commit: `PRESERVE`
- P1-7 runtime: `REWORK_REQUIRED / HUMAN_PENDING`
- P1-8: `NOT_STARTED`
- PUBLIC_BOUNDED_LIVE: `NOT_RELEASED`
- runtime commit: `none`
- required_rework:
  1. exact reservation/request and HumanResult/gate/request cross-scope binding
  2. durable current-gate verification before HumanActionAuthority issuance
  3. TaskContract/use-bound Judgment policy + real COMMAND_CENTER owner authority
  4. Judgment same-ID/different-fingerprint identity conflict
  5. gate expiry/lifecycle/guard enforcement
  6. corrected export SHA provenance
- terminal_decision_reason: multiple accepted P1-7 authority boundaries can currently be substituted across WorkRuns/uses or remain effective without the required policy/expiry checks.

## preserved artifacts

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

.aiassistant/tasks/done/
20260829_2328_aiscc-p1-7-design-terminal-persistence-and-runtime-implementation-1.md

.aiassistant/records/aiscc/cycles/
20260830_0051_aiscc-p1-7-runtime-authority-binding-policy-expiry-hold-1.cycle.md
```

## next action

```text
P1-7 runtime narrow authority rework
→ Command Center review
→ Human final runtime review

P1-8:
NOT_STARTED
```
