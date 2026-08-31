# P1-8 Runtime Resume Handoff

## purpose

This handoff allows a fresh Browser Command Center / Executor session to resume the already Human-accepted P1-8
runtime design without relying on chat memory, File Library, or stale Project Source mirrors. It authorizes the next
runtime Task only; it does not start or accept P1-8 runtime implementation.

## exact accepted predecessors

```text
P1-8 accepted design commit:
c108e9c02f222cf51ce833e311465584447b3571

P1-8 accepted design SHA-256:
100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a

P1-8 design terminal governance:
b111f5f676e1a782de095e2f5b2a106d8b9a0207

P1-6 durable-content accepted design commit:
32e88234ad7a7cbaa545e12f8c7e03b5897202cb

P1-6 durable-content accepted design SHA-256:
ab54948fb8c253309d5a8c228e31fca1b9afb9e19f0faf9be9cda8d14b735411

P1-6 durable-content accepted runtime commit:
8320a3c567a58bab5f728a88d5c88862392d187c

P1-6 durable-content runtime aggregate:
13 paths / 2290da92d56d47336de410fd8848177d71f3965f2556d4363cde9dfa40749721
```

## durable historical-content boundary

```text
P1-6 owner write only
P1-8 owner-issued historical read grant only
purpose = P1_8_STRUCTURED_RESULT_V1
read ceiling = PUBLIC_SAFE + INTERNAL internal derivation
write authority = none
export authority = none
```

A caller-supplied writer authority, forged grant, or foreign-authority grant is denied. A valid P1-8 grant provides
only its fixed historical read capability and never gains durable-content write or export authority.

## Requirement compatibility

```text
V1 Requirement fingerprints and RequirementSet roots:
exact historical identity preserved

V2 durable-capable Requirements:
prospective explicit persisted fingerprint schema only

legacy metadata-only evidence:
P1-6 historical validity preserved
P1-8 structured-source eligibility = NOT_ELIGIBLE
```

## load-bearing P1-8 invariants

```text
CommandCenterCycleRecord != AdmittedCycle

raw session != ProjectMemory

Judgment != CycleAdmissionDecision

TransitionDecision != CycleAdmissionDecision

historical source provenance
!= current source effectiveness
!= current ProjectMemory applicability

historical policy validity
!= current policy applicability

ProjectMemoryEntryId != MemoryLineageKey

one CURRENT tip per lineage

EXPLICIT_SUPERSESSION_ONLY

LESSON = NOT_SUPPORTED

NextActionProposal
!= NextActionSelection
!= TransitionDecision

enrolled ActionRef eligibility = before ranking

TaskIssuanceCandidate != TaskContract

Task authority = EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY
```

Deterministic ranking does not create action authority. Proposal priority, security, or blocker claims are not
authority. Only current enrolled versioned ActionRef/Descriptor candidates are eligible for a new selection.
Selection does not mint a `TransitionDecision` or `TaskContract`.

## resume status

```text
P1-6 durable-content runtime:
HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-8 durable-content prerequisite:
SATISFIED

P1-8 Runtime:
NOT_STARTED / RESUME_AUTHORIZED / NEXT_ACTION

P2:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

The 2130 P1-8 implementation Task under `tasks/done` means only that its Executor lifecycle completed after the
mandatory `IMPLEMENTATION_BASELINE_GAP` stop. It does not mean P1-8 runtime was implemented, verified, or accepted.

The next Task must consume the accepted P1-8 design without redesigning or absorbing P1-4/P1-6/P1-7 authority.
