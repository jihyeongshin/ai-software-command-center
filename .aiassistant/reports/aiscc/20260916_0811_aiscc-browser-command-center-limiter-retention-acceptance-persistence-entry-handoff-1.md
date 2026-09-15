# AISCC Browser Command Center Handoff — retention substantive acceptance → Git persistence

## repository identity

```text
branch:
main

HEAD:
bd46b40b47cede29a8865a2b78c42f4de36dc567
```

## accepted result

```text
retention policy:
HUMAN_PROVIDED / ACCEPTED V1

implementation:
SUBSTANTIVE ACCEPTED

release blocker:
RESOLVED_CANDIDATE

Git persistence:
PENDING
```

## accepted evidence

```text
focused:
186 PASS

full suite:
1383 PASS / 3 existing SKIP / 0 FAIL / 0 ERROR

PostgreSQL:
17.6

new migration:
20260916_0016

provider calls:
0

Public admission:
DISABLED
```

## exact accepted source

- `migrations/versions/20260916_0016_public_live_limiter_retention.py`
- `src/aiscc/persistence/public_live_limits.py`
- `tests/integration/next_action/test_genesis_bootstrap.py`
- `tests/integration/providers/test_external_ide_execution_ingress.py`
- `tests/integration/providers/test_external_ide_execution_start.py`
- `tests/integration/public_live/test_http.py`
- `tests/integration/public_live/test_persistence.py`
- `tests/integration/public_live/test_retention.py`
- `tests/integration/self_dogfood/test_task_ready_entry.py`
- `tests/integration/task_authority/test_task_contract_durability.py`
- `tests/integration/workflow/test_postgres_kernel.py`

## provenance to persist

0445 policy-decision package and 0447 accepted-policy/implementation lineage are currently uncommitted and must be preserved with the implementation.

## persistence boundary

Do not:

- alter retention code;
- alter 30/120/1200 caps;
- rerun DB/full tests merely to regenerate evidence;
- start L4/L5;
- enable Public admission;
- call provider;
- push/deploy.

After exact commit review, Browser may promote:

`RESOLVED_CANDIDATE -> RESOLVED`
