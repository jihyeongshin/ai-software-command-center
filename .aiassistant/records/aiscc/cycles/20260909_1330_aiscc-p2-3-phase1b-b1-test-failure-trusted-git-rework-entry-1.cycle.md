# AISCC Cycle Record

## meta

- cycle_id: `20260909_1330_aiscc-p2-3-phase1b-b1-test-failure-trusted-git-rework-entry-1`
- date: `2026-09-09T13:30:00+09:00`
- project: `AI Software Command Center (AISCC)`
- primary_semantic_owner: `P2-3 Phase 1B-B1 trusted Git executable rework`
- work_type: `BOUNDED_BACKEND_REWORK / QA_ONLY`
- predecessor_task: `.aiassistant/tasks/done/20260909_1329_aiscc-p2-3-phase1b-b1-pinned-resource-materializer-implementation-1.md`
- result_status: `HOLD_REWORK_REQUIRED`
- blocker: `TEST_FAILURE`
- root_cause: `TRUSTED_EXECUTABLE_HARDLINK_POLICY_MISAPPLIED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`
- handoff_required: `No`
- fresh_ide_executor_chat_for_successor: `NOT_REQUIRED`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260909_1330_aiscc-p2-3-phase1b-b1-test-failure-trusted-git-rework-entry-1.cycle.md`

# predecessor result

```text
five B1 files:
created

suite:
5 failed / 95 passed / 1 skipped

root cause:
workspace hardlink policy incorrectly reused for trusted git.exe

source repair after failure:
NOT_RUN

Git:
NOT_RUN
```

# bounded recovery

Modify only:

```text
src/aiscc/runtime/stockroom_materializer.py
tests/unit/runtime/test_stockroom_materializer.py
```

Keep byte-exact:

```text
src/aiscc/runtime/stockroom_workspace.py
src/aiscc/scenarios/runtime_models.py
tests/unit/runtime/test_stockroom_workspace.py
```

# success target

The successor must establish:

```text
trusted Git executable:
valid even when regular-file st_nlink > 1

workspace/materialized regular files:
hardlink denial preserved

full positive pinned materialization:
PASS

intended negative source/manifest branches:
branch-specific proof

partial publication:
all four cases reach allocation and prove cleanup/quarantine

exact two-module B1 suite:
PASS
```

No B2/B3 work.
