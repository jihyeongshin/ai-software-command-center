# AISCC Command Center Judgment

## meta

- judgment_id: `20260912_2125_aiscc-p2-3-s1-execution-guard-producer-binding-scope-expansion-judgment-1`
- created_at: `2026-09-12T21:25:13+09:00`
- project: `AI Software Command Center (AISCC)`
- reviewed_task: `20260912_2052_aiscc-p2-3-s1-current-state-producer-provenance-decoupling-source-rework-1`
- reviewed_result_zip_sha256: `ccf52b7b2a1cb33d2d95587b558087385a4040a0dbb6fffa9461bcb994e98528`
- result_status: `HOLD_REWORK_REQUIRED / SOURCE_SCOPE_INSUFFICIENT_CONFIRMED`
- reject_cause: `P1_4_EXECUTOR_SUBMISSION_BINDING_NOT_DURABLE`
- cycle_record_action: `create`
- execution_mode: `MANUAL_COMMAND_CENTER`
- source_mirror_sync: `not-required`

# Browser judgment

2052 Executor의 `SOURCE_SCOPE_INSUFFICIENT` STOP을 정당하게 입장한다.

Verified blocked result:

```text
ZIP:
15 members / one top-level / CRC PASS

manifest:
14 / 14 exact

TASK root == canonical done Task:
PASS

contract:
20 PASS / 14 BLOCKED_REQUIRED_EVIDENCE

source mutation:
none

tests:
not run

Docker/private/DB/S1:
not accessed

Git:
index empty / tracked clean / no commit
```

# confirmed authority gap

Existing durable workflow history can prove:

```text
same WorkRun
RUNNING/vN
→ admitted RUNNING_TO_ADMISSION_PENDING
→ ADMISSION_PENDING/vN+1
```

but current `G_EXECUTOR_SUBMISSION` provenance loses the exact producer identity:

```text
submission_id
execution_attempt_id
```

because the execution guard emits a generic P1-5 authority fact and its durable `bound_refs` are empty.

A separately authentic `ExecutionSubmissionRef` for the same run/state/version is not sufficient to prove
that it was the exact producer ref used to authorize the historical transition.

# expanded bounded source authority

The successor may inspect and, only if the existing model/serialization is already sufficient, modify up to:

```text
src/aiscc/workflow/guards.py
src/aiscc/persistence/repository.py
src/aiscc/scenarios/capture_runner.py
src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

No model/schema/migration path is authorized.

The intended correction must:

```text
persist exact verified submission + attempt identity in G_EXECUTOR_SUBMISSION guard provenance
reconstruct and validate that binding historically
keep ExecutionSubmissionRef immutable at RUNNING/producer_version
keep current evidence-review authority at ADMISSION_PENDING/current_version
prove exact predecessor linkage before evidence admission
```

If the existing `GuardFact.bound_refs` serialization or a canonical typed-ref encoding is insufficient,
the Task must STOP before source write rather than invent a schema/design.

# runtime boundary

No private S1 execution, Docker, private file, PostgreSQL, provider/network or Git persistence is authorized.
