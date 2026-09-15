# AISCC Browser Command Center Handoff — baseline repair PostgreSQL-runtime-authorized retry

## 목적

이 Handoff는 `20260915_2225` repair attempt가 source bug가 아니라 **Task environment authorization defect**로 중단된 상태에서 다음 IDE Executor retry로 이어가기 위한 것이다.

## 현재 authoritative state

```text
repository HEAD:
3709c88fc0abd2f4219228ced931a9164f286dc4

P3-3 Public Live L1:
ACCEPTED / CLOSED

L2:
NOT_STARTED / ENTRY_ELIGIBLE

Public Live:
NOT_RELEASED

Public admission:
DISABLED
```

Known broader baseline debt:

```text
1197 PASS
3 FAIL
3 SKIP
0 ERROR
```

Exact shared failure:

```text
ValueError:
G_EXECUTOR_SUBMISSION requires an issuer-verified execution ref
```

## previous retry outcome

```text
20260915_2225 repair attempt:
BLOCKED / EVIDENCE_SCOPE_EXPANSION_REQUIRED
source changes:
none
```

The previous Task required database-backed reproduction but prohibited recreation of the predecessor PostgreSQL runtime. That predecessor runtime had been correctly removed during terminal cleanup.

This is a Command Center Task-authoring defect, not a product regression.

## corrected runtime policy for this retry

Explicitly authorized:

```text
postgres:17.6 from local cache only
no docker pull
new task-owned isolated container
new task-owned ephemeral volume
127.0.0.1:55432
task-local test credentials only
AISCC_TEST_DATABASE_URL bound to the task-owned DB
LOCAL_POSTGRES_RUNTIME.json PASS before tests
same runtime through targeted + full-suite verification
terminal cleanup best-effort
```

Explicitly forbidden:

```text
private/pre-existing PostgreSQL reuse
aiscc-p2-3-private-postgres-v1 reuse/reset/start
network image pull
0.0.0.0 bind
production/runtime source mutation
G_EXECUTOR_SUBMISSION guard weakening
skip/xfail/assertion dilution
Git commit/push
```

## required proof order

```text
runtime recreate
→ LOCAL_POSTGRES_RUNTIME PASS
→ exact three reproduction BEFORE mutation
→ fixture repair
→ exact three PASS
→ full suite 0 FAIL / 0 ERROR
→ report/export
→ task-owned cleanup best-effort
→ Browser judgment
```

## likely source direction from blocked investigation

Not yet accepted as repair proof:

- `src/aiscc/workflow/guards.py` rejects generic issue for `G_EXECUTOR_SUBMISSION`.
- current verified path uses execution-ref verification.
- Command Center `_GuardAuthority.issue` appears to route this guard through generic issue.
- nearby workflow integration test contains a current issuer-verified execution-submission construction example.

Executor must reproduce before mutating.

## next Task

`.aiassistant/tasks/active/20260915_2230_aiscc-command-center-baseline-regression-repair-postgresql-runtime-authorized-retry-1.md`

Do not start L2 in this retry.
