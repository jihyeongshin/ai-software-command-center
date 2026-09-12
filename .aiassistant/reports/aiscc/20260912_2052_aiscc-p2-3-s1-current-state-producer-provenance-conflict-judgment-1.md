# AISCC Command Center Judgment

## meta

- judgment_id: `20260912_2052_aiscc-p2-3-s1-current-state-producer-provenance-conflict-judgment-1`
- created_at: `2026-09-12T20:52:11+09:00`
- project: `AI Software Command Center (AISCC)`
- reviewed_task: `20260912_2024_aiscc-p2-3-s1-admission-pending-evidence-state-contract-source-rework-1`
- reviewed_result_zip_sha256: `3c09728ea9a3f221e5362898355758ef04d8bdd58d7b3243fbb0e5a888a29339`
- result_status: `HOLD_REWORK_REQUIRED / SOURCE_AUTHORITY_COUPLING_DEFECT_CONFIRMED`
- reject_cause: `CURRENT_STATE_AND_PRODUCER_PROVENANCE_CONFLATED`
- cycle_record_action: `create`
- execution_mode: `MANUAL_COMMAND_CENTER`
- source_mirror_sync: `not-required`

# Browser judgment

2024 Executor의 mandatory STOP을 정당하게 입장한다.

Browser result verification:

```text
result ZIP:
14 members / one top-level / CRC PASS

manifest:
13 / 13 exact

TASK root == canonical done Task:
PASS

issued Cycle/Judgment:
byte exact

contract:
18 PASS / 9 BLOCKED_REQUIRED_EVIDENCE

tracked/index:
clean / empty

source mutation:
none

tests:
not executed

Docker/private/DB/S1:
not accessed
```

# corrected diagnosis

The 2024 Task correctly identified that evidence admission occurs while the authoritative WorkRun is
`ADMISSION_PENDING`, but its proposed one-line correction was incomplete.

Current source also verifies an immutable P1-5 `ExecutionSubmissionRef` whose producer provenance was
issued for the completed execution in `RUNNING / producer_state_version`.

Canonical invariants require both facts to remain true:

```text
current workflow authority during evidence review:
ADMISSION_PENDING / current_state_version

immutable producer provenance:
RUNNING / producer_state_version

producer ref:
not rebound to current ADMISSION_PENDING

P1-5 producer ref:
not evidence admission authority by itself
```

A correct adapter must therefore decouple:

```text
current-state freshness / evidence-review eligibility
from
producer-ref provenance verification
```

and prove they belong to the same run/attempt and the exact admitted
`RUNNING → ADMISSION_PENDING` predecessor transition.

# forbidden incorrect fixes

Do not:

```text
simply replace every RUNNING request with ADMISSION_PENDING
relabel ExecutionSubmissionRef producer state/version
derive trusted producer provenance only from unverified ref fields
move evidence submission before RUNNING_TO_ADMISSION_PENDING
weaken ExecutionReferenceAuthority.verify
accept either RUNNING or ADMISSION_PENDING as current
bypass _current or AuthorityConflictError
```

# next authorized source rework

Modify only the production Stockroom adapter and its focused integration test if the existing authority APIs are sufficient.

If correct predecessor linkage cannot be proven within those two paths using existing immutable workflow/provider authority,
STOP with `SOURCE_SCOPE_INSUFFICIENT` before source write.

No private S1 runtime execution is authorized.
