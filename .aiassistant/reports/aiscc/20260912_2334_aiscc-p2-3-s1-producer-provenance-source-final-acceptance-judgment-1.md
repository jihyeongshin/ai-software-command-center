# AISCC Command Center Judgment

## meta

- judgment_id: `20260912_2334_aiscc-p2-3-s1-producer-provenance-source-final-acceptance-judgment-1`
- created_at: `2026-09-12T23:34:15+09:00`
- project: `AI Software Command Center (AISCC)`
- reviewed_task: `20260912_2300_aiscc-p2-3-s1-static-module-policy-and-bound-ref-candidate-finalization-1`
- reviewed_result_zip_sha256: `d856d9238f78facc870d51837a64c7e446ae0c3309c021ac54f11299ea47e0cf`
- result_status: `ACCEPTED / S1_BOUND_REF_SOURCE_CANDIDATE_COMPLETE`
- reject_cause: `NONE`
- cycle_record_action: `create`
- execution_mode: `MANUAL_COMMAND_CENTER`

# Browser judgment

The 2300 source candidate is accepted for Git persistence.

Independent Browser verification established:

```text
result ZIP:
22 members / one top-level / CRC PASS

manifest:
21 / 21 byte/hash exact

Task/Cycle/Judgment:
issued bytes exact

contract:
38 / 38 PASS

compile:
PASS

Ruff:
PASS

static-contract unit module:
27 passed

targeted scenario module:
41 passed / 1 skipped

full unit suite:
741 passed / 2 skipped

git diff --check:
PASS

private runtime / Docker / PostgreSQL / S1:
NOT EXECUTED
```

# accepted correction

Canonical execution producer binding:

```text
G_EXECUTOR_SUBMISSION bound_refs:
exact V1 submission + execution-attempt binding

issuance:
only after issuer-backed ExecutionSubmissionRef verification

historical persistence:
exact binding retained and reconstructed

CURRENT:
ADMISSION_PENDING/current version

LINK:
exact admitted RUNNING → ADMISSION_PENDING predecessor

PRODUCER:
RUNNING/original producer version + exact submission/attempt

non-substitution:
ExecutionSubmissionRef != EvidenceCandidate != AdmittedEvidence != G_EVIDENCE
```

The source-owned runner ordering remains:

```text
execute
→ RUNNING_TO_ADMISSION_PENDING admitted
→ submit_runtime_evidence
```

The exact same-shape cross-producer regression demonstrates that an independently authentic producer with the same
run/attempt/state/version shape cannot substitute for the producer bound to the admitted predecessor.

# accepted static-module policy

The static scenario contract import policy owns exactly:

```text
src/aiscc/scenarios/__init__.py
src/aiscc/scenarios/catalog.py
src/aiscc/scenarios/models.py
```

This is an exact membership boundary, not a broadened import allowlist.

# acceptance limits

This judgment accepts the source/test candidate only.

It does not claim:

```text
private S1 runtime execution
PostgreSQL durability/restart proof for the new source candidate
deployment/release
Git persistence
```

Those are separate later authorities.

# next action

Persist:

```text
1749 → 2300 canonical governance lineage
six accepted source/test paths
this acceptance Cycle/Judgment
```

Then reconcile canonical state in a second commit.

After persistence, private S1 returns to:

```text
ENTRY_READY / NOT_STARTED / NOT_AUTHORIZED
```

A separate exact Browser-issued S1 execution Task is required.
