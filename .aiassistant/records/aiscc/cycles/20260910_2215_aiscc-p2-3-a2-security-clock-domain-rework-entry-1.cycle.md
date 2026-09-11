# AISCC Cycle Record

## meta

- cycle_id: `20260910_2215_aiscc-p2-3-a2-security-clock-domain-rework-entry-1`
- date: `2026-09-10T22:15:00+09:00`
- project: `AI Software Command Center (AISCC)`
- primary_semantic_owner: `P2-3 A2 security TTL clock-domain reconciliation`
- work_type: `IMPLEMENTATION_REWORK / POSTGRESQL_INTEGRATION`
- predecessor_task: `.aiassistant/tasks/done/20260910_1948_aiscc-p2-3-a2-production-integration-static-and-runtime-evidence-binding-rework-1.md`
- result_status: `HOLD_REWORK_REQUIRED`
- blocker: `TEST_FAILURE / SECURITY_TTL_CLOCK_DOMAIN_MISMATCH`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`
- handoff_required: `No`
- fresh_ide_executor_chat_for_successor: `NOT_REQUIRED`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260910_2215_aiscc-p2-3-a2-security-clock-domain-rework-entry-1.cycle.md`

# preserved candidate

```text
static gate:
PASS

runtime evidence ToolOutputRef binding:
VERIFIED_CANDIDATE

three versioned configs:
FROZEN

A1:
FROZEN / ACCEPTED
```

# exact rework

```text
MODIFY:
src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

# clock invariant

```text
durable/application clock
!= security TTL wall-clock domain

SecurityPolicy grant/evaluate/capability lifecycle
must use one internally consistent clock domain.
```

Do not weaken security or change P1-3 source.

# proof sequence

```text
clock-domain correction
→ full static gate
→ PostgreSQL A2 integration
→ A1/B3 regression
→ bounded direct-owner regressions
→ 25/25 contract review
```

# success ceiling

```text
A2:
IMPLEMENTED_CANDIDATE / BROWSER_JUDGMENT_REQUIRED

actual Stockroom runtime:
NOT_EXECUTED

actual capture:
NOT_STARTED
```
