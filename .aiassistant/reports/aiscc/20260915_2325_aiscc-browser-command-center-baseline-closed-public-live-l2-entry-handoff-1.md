# AISCC Browser Command Center Handoff — baseline closed → Public Live L2 entry

## purpose

Continue P3-3 Public Live from a clean accepted baseline.

Do not repeat baseline-debt repair.

## current repository identity

```text
branch:
main

HEAD:
a2672c7a66bfd6b3d805caf2b187dae41b6181e5

commit message:
test: restore command center issuer-verified submission baseline
```

## completed predecessor

```text
P3-3 Public Live L1:
ACCEPTED / CLOSED

Command Center baseline regression repair:
ACCEPTED / CLOSED

broader suite:
1220 PASS / 3 SKIP / 0 FAIL / 0 ERROR
```

The previous three failures were stale test-fixture assumptions around `G_EXECUTOR_SUBMISSION`.

Repair preserved the stronger issuer-verified execution-ref authority. Production/runtime guard code was not weakened.

## current Public Live state

```text
L1:
COMPLETE / ACCEPTED / CLOSED

L2:
SELECTED / ENTRY_AUTHORIZED / NOT_STARTED

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

Public Live:
NOT_RELEASED

Public admission:
DISABLED
```

## selected next action

```text
B — L2 atomic admission service
```

L2 is the next critical-path implementation.

L4 provider profile and L5 Railway ingress/sandbox proof remain separate. Do not pull their work into L2.

## frozen design authority recovery

The accepted Public Live prerequisite design is Human-accepted/frozen at predecessor design commit lineage `209e7534f66e9b07ce9d33742e6993370a70f4fb`.

Known exact basenames:

1. `PUBLIC_LIVE_ADMISSION_SECURITY_DESIGN.md`
2. `PUBLIC_LIVE_DB_SCHEMA_PLAN.md`
3. `PUBLIC_LIVE_HTTP_CONTRACT.md`
4. `PUBLIC_LIVE_FAILURE_STATE_MACHINE.md`
5. `PUBLIC_LIVE_IMPLEMENTATION_SEQUENCE.json`
6. `PUBLIC_LIVE_SECURITY_TEST_MATRIX.json`
7. `PUBLIC_LIVE_OPEN_DECISIONS.md`

This Handoff does not claim their current exact repository paths.

The L2 Executor Task must resolve each basename against Git-tracked files before mutation and fail closed unless every basename has exactly one match.

## accepted high-level invariant

Public Live remains `PUBLIC_REPLAY_WITH_BOUNDED_LIVE`.

Replay/static availability and paid Live inference remain separate failure domains.

Public Live must not introduce arbitrary repository upload, free-form shell/network, user-selected provider/model/credential, or hidden Live fallback.

The exact L2 contract is owned by the frozen seven-document design package, not by this Handoff.

## environment lifecycle

If PostgreSQL runtime evidence is required, a predecessor container is NOT assumed to exist.

Use the Task-authorized lifecycle:

```text
cached postgres:17.6
network pull forbidden
task-owned isolated container/volume
127.0.0.1:55432 only
LOCAL_POSTGRES_RUNTIME.json before DB tests
best-effort task-owned cleanup after evidence
```

## next executor

Use:

`.aiassistant/tasks/active/20260915_2325_aiscc-p3-3-public-live-l2-atomic-admission-service-implementation-1.md`

The Task must complete its authority-resolution gate before any L2 source mutation.
