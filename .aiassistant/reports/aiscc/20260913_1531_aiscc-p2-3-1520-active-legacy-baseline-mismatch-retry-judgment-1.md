# AISCC Command Center Judgment

## meta

- judgment_id: `20260913_1531_aiscc-p2-3-1520-active-legacy-baseline-mismatch-retry-judgment-1`
- created_at: `2026-09-13T15:31:58+09:00`
- project: `AI Software Command Center (AISCC)`
- reviewed_delivery_zip_sha256: `a7620b288702c5ce4387a2b294a59440c0e18ee2c61273f420e8de7a50ae4daa`
- result_status: `HOLD_RETRY_REQUIRED / COMMAND_CENTER_ACTIVE_TASK_EXCLUSIVITY_DEFECT`
- source_rework_authorized: `Yes / exact two paths after corrected bootstrap`
- private_runtime_access_authorized: `No`
- runtime_disposition_authorized: `No`

# Browser judgment

1520 correctly stopped before source modification.

Verified Human/Executor report:

```text
1520 transport/hash/archive:
PASS

1511 active→done:
byte-exact PASS

Git-visible untracked:
11 exact

source/test mutation:
0

tests:
0

Docker/DB/private runtime:
0

report/export:
0
```

The blocker was introduced by the Browser-issued Task:

```text
active Tasks:
current 1520 Task only
```

That exclusivity assumption is invalid for this repository.

A pre-existing non-owned active Task exists:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md

SHA-256:
52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

This Task belongs to an older in-flight lineage and is not owned by the current disposition track.

# correction

The retry must:

- verify the exact legacy 1400 active Task;
- preserve it in place;
- never delete, move, overwrite, complete, or reinterpret it;
- close only the failed 1520 Task lifecycle active→done byte-exactly;
- perform the same exact two-path disposition-only composition rework.

Active-directory exclusivity is not a governance invariant here.
Task ownership is path-specific.
