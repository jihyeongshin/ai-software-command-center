# AISCC Cycle Record

## meta
- cycle_id: `20260830_2011_aiscc-p1-8-design-historical-policy-current-policy-separation-hold-1`
- date: `2026-08-30T20:11:00+09:00`
- phase: `P1-8 Project Memory and Cycle Admission Design`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause: `HISTORICAL_POLICY_AND_CURRENT_POLICY_CONFLATED`

## reviewed submission
```text
HEAD:
4b84a9f66c148b198d3f4b6b01cffc4641fdceb1

reworked design SHA-256:
8024613cc0c4d525e010db937ba8a249dcbfa77feeb7faa5cc9f6862864068b2

runtime:
NOT_STARTED

Git actions:
0
```

## closed findings
The 2011 source/current-applicability finding is CLOSED.

```text
historical P1-6 source provenance != current source effectiveness
→ CLOSED

delayed admission / no temporary CURRENT exposure
→ CLOSED

historical Cycle replay survives later source invalidation
→ CLOSED

default retrieval / CYCLE_DERIVED current-only
→ CLOSED
```

## remaining load-bearing finding

The design still requires:

```text
CycleEvaluation:
exact current MemoryDeclarationAuthorityPolicy

NextAction evaluation:
current NextActionEligibilityPolicy
```

while those policies themselves are versioned, immutable, revocable and supersedable.

This creates a contradiction with immutable historical replay.

A Cycle admitted under policy v1 must remain historically replayable after v2 supersedes v1.
A NextActionSelection issued under eligibility/selection policy v1 must remain historically replayable after
policy v2 becomes current.

Required invariant:

```text
historical policy issuance/validity
!= current policy applicability
```

### MemoryDeclarationAuthorityPolicy

For a new Cycle admission:

```text
current eligible policy
→ REQUIRED
```

For replay/verifying an already admitted Cycle:

```text
exact historical policy ref/version/fingerprint
that was valid at original admission
→ REQUIRED

policy still current now
→ NOT REQUIRED
```

Later policy revocation/supersession may affect current ProjectMemory applicability/export/retrieval through an
append-only applicability event when the policy contract says so, but it must not mutate old Cycle/entry identity.

### NextAction policies/descriptors

Likewise:

```text
new NextActionSelection
→ current eligibility + selection policy/descriptor required

historical NextActionSelection replay
→ exact policy/descriptor versions valid at original issuance required

currently enrolled/current now
→ NOT REQUIRED for historical replay
```

Later descriptor/policy revocation changes current-next-action projection and future selection eligibility only.

## judgment
```text
P1-8 Design:
HOLD_REWORK_REQUIRED / HUMAN_PENDING

P1-8 Runtime:
NOT_STARTED

P2:
NOT_STARTED
```

No runtime work is authorized.
