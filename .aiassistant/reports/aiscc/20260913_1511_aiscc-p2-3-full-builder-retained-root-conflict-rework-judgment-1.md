# AISCC Command Center Judgment

## meta

- judgment_id: `20260913_1511_aiscc-p2-3-full-builder-retained-root-conflict-rework-judgment-1`
- created_at: `2026-09-13T15:11:18+09:00`
- project: `AI Software Command Center (AISCC)`
- reviewed_task: `20260913_1435_aiscc-p2-3-private-s1-invalid-history-disposition-root-authority-retry-1`
- reviewed_result_zip_sha256: `8c4fdb3ca1494262071d39289301be6ead50b7c47624d8e3c1786a647e839350`
- result_status: `HOLD_REWORK_REQUIRED / FULL_PRODUCTION_BUILDER_INCOMPATIBLE_WITH_RETAINED_ROOT`
- source_rework_authorized: `Yes / exact two paths`
- private_runtime_access_authorized: `No`
- runtime_disposition_authorized: `No`

# Browser judgment

1435 is a truthful P0 stop.

Independent verification:

```text
ZIP:
17 members / one top-level / CRC PASS

manifest:
16 / 16 exact

TASK.md:
canonical done bytes exact

contract:
49 PASS / 27 BLOCKED_REQUIRED_EVIDENCE

private root reconstruction:
PASS

private DB Phase A:
PASS

workspace Phase A:
PASS

dispose calls:
0

runtime mutation:
0
```

The new blocker is source composition, not runtime authority.

The ordinary production builder always constructs:

```text
StockroomWorkspace(private_runtime_root, ...)
```

before returning `StockroomProductionApplication`.

`StockroomWorkspace` intentionally requires the runtime root to be empty for a new execution composition.

The retained 0036 root is correctly nonempty because its historical active attempt workspace still exists.

Therefore:

```text
do not empty the root
do not weaken StockroomWorkspace empty-root invariant
do not bypass the check
do not reuse the full production builder for disposition
```

The accepted disposition service itself requires only:

```text
PostgresExecutionRepository
WorkflowKernel backed by PostgresTransitionRepository + P1_4GuardAuthority
StockroomRestartSafetySettlement
requester_identity
clock
```

The existing integration test already demonstrates this minimal authority composition.

# authorized correction

Add one dedicated public source-owned composition entrypoint:

```text
build_stockroom_invalid_history_disposition(...)
```

It must construct only the authorities needed by `StockroomInvalidHistoryDisposition` and must not instantiate the
execution workspace, Docker runtime, provider/tool execution stack, evidence/human/Judgment authorities, or full
StockroomProductionApplication.

The next private runtime Task will call this dedicated entrypoint only after Browser acceptance/persistence.
