# AISCC Command Center Judgment

## meta

- judgment_id: `20260913_0012_aiscc-p2-3-private-s1-source-correction-persisted-execution-authorization-judgment-1`
- created_at: `2026-09-13T00:12:33+09:00`
- project: `AI Software Command Center (AISCC)`
- authorization: `PRIVATE_S1_EXECUTION`
- source_authority_head: `6cc4f988f56f5cbf32e57f4b5e9a52a180044c36`
- persistence_commit_a: `35cee94a92d1f12801576ef48038196922687f42`
- persistence_commit_b: `6cc4f988f56f5cbf32e57f4b5e9a52a180044c36`
- result_status: `AUTHORIZED / S1_ONLY`
- execution_mode: `MANUAL_COMMAND_CENTER`

# authorization

The source correction is FINAL_ADMITTED / PERSISTED.

This Judgment authorizes exactly one private S1 normal scenario execution/capture attempt:

```text
scenario:
S1 only

run_id:
aiscc-p2-3-private-s1-normal-v1-run

attempt_id:
aiscc-p2-3-private-s1-normal-v1-attempt-1
```

S2/S3/S4 are not authorized.

The source-owned `StockroomCaptureRunner.run(...)` remains the only orchestration path.

The persisted correction establishes:

```text
CURRENT:
ADMISSION_PENDING/current authoritative state

LINK:
exact admitted RUNNING → ADMISSION_PENDING predecessor with canonical submission+attempt binding

PRODUCER:
issuer-verified RUNNING/original producer version

cross-producer substitution:
DENIED / regression proved

non-substitution:
ExecutionSubmissionRef != EvidenceCandidate != AdmittedEvidence != G_EVIDENCE
```

# environment authority

Reuse the retained Cut C environment subject to exact runtime preflight:

```text
Stockroom image:
sha256:c51ad05852b58a3b4fd275ee88d183551e745d79ac8239e3da3b98372fe0bb9e

PostgreSQL container:
aiscc-p2-3-private-postgres-v1

PostgreSQL container ID:
0b50ac47a79e05ac9b88a8f679d04ddc39f729bf1a8e099d149c4c5570b5999c

PostgreSQL volume:
aiscc-p2-3-private-postgres-data-v1

migration head:
20260901_0008

private runtime root:
existing / retained / expected empty before S1
absolute path remains private
```

Any preflight mismatch stops before durable S1 creation.

# success semantics

Expected S1 normal outcome:

```text
ExecutionStatus:
EXECUTOR_COMPLETED

Evidence:
SATISFIED / admitted

Judgment:
ACCEPTED / SATISFIED_ATTESTATION

WorkflowState:
ACCEPTED

HumanGate/HumanResult:
NONE

S2/S3/S4:
NOT_EXECUTED
```

Browser admission of the execution result remains HUMAN_PENDING.
