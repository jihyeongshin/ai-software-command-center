# AISCC Browser Command Center Handoff — L1 Complete / Next Action Selection

## purpose

Start the next Browser Command Center session from the terminally accepted Public Live L1 state.

Do not repeat L1 implementation.

## current canonical implementation identity

```text
branch:
main

HEAD:
3709c88fc0abd2f4219228ced931a9164f286dc4

parent:
209e7534f66e9b07ce9d33742e6993370a70f4fb

commit message:
feat(aiscc): add public live persistence primitives
```

## L1 status

```text
L1 additive schema/repository transaction primitives:
IMPLEMENTED / ACCEPTED / CLOSED

Alembic:
20260915_0013

PostgreSQL evidence:
17.6

focused:
129 PASS

standalone L1:
23 PASS
```

## product truth

```text
Public Live:
NOT_RELEASED

Public admission:
DISABLED

Public HTTP routes:
NOT_IMPLEMENTED_BY_L1

Provider paid calls:
IMPOSSIBLE_FROM_L1

L2:
NOT_STARTED / ENTRY_ELIGIBLE
```

## known baseline regression debt

Broader suite:

```text
1197 PASS
3 FAIL
3 SKIP
0 ERROR
```

Exact failures:

```text
tests/integration/command_center/test_postgres_read_api.py::
test_postgres_read_models_http_runtime_and_no_mutation

tests/integration/command_center/test_postgres_read_api.py::
test_postgres_conflict_and_http_503_fail_closed

tests/integration/command_center/test_web_ui.py::
test_default_entrypoint_ui_queue_etag_and_event_no_mutation
```

Shared failure:

```text
ValueError:
G_EXECUTOR_SUBMISSION requires an issuer-verified execution ref
```

Disposition:

```text
PREEXISTING_NOT_L1_CAUSED
DEFERRED_SEPARATE_TASK
```

Do not call the repository full-suite green.

Do not weaken `G_EXECUTOR_SUBMISSION`, skip/xfail these tests, or treat the debt as L1 regression without new evidence.

## frozen implementation DAG

```text
L0:
COMPLETE / HUMAN_ACCEPTED

L1:
COMPLETE / ACCEPTED

L2:
ENTRY_ELIGIBLE

L3:
blocked on L2

L4:
ENTRY_ELIGIBLE

L5:
ENTRY_ELIGIBLE

L6:
blocked on L3 + L4 + L5

L7:
blocked on L6

L8:
Human release decision
```

## next-action candidates

The next Browser Command Center should evaluate, not automatically execute:

### A — baseline debt repair first

Repair the three Command Center integration fixtures so they use the current issuer-verified executor-submission authority contract.

Goal:

```text
restore green baseline before additional Public Live implementation
```

This is Browser's recommended candidate because future regression attribution is cleaner when baseline is green.

### B — L2 atomic admission service

Implement the frozen atomic Public Live admission orchestration on top of accepted L1 primitives.

Do not begin unless Browser explicitly accepts carrying the known baseline debt during L2.

### C — L4 provider profile prerequisite

Independently progress the real provider profile / exact token-envelope prerequisite.

No paid provider action without separate authorization.

### D — L5 Railway ingress/sandbox proof

Independently investigate hosted ingress identity, trusted proxy and sandbox feasibility.

No deployment or paid resource mutation without separate authorization.

## recommended first decision

Prefer:

```text
A — baseline debt repair first
```

Reason:

The three failures are already known to be pre-existing and unrelated to L1, but leaving a known non-green baseline into L2 would make later regression attribution noisier.

The repair must preserve the stronger issuer-verified `G_EXECUTOR_SUBMISSION` authority. The tests/fixtures should be updated to satisfy current authority, not the guard weakened to satisfy old fixtures.

## workflow instruction

This is a Browser-session handoff.

No IDE Executor Task accompanies this handoff.

In the new Browser Command Center session:

1. load this Handoff;
2. confirm HEAD `3709c88fc0abd2f4219228ced931a9164f286dc4`;
3. perform next-action selection;
4. only then issue the selected Executor Task.
