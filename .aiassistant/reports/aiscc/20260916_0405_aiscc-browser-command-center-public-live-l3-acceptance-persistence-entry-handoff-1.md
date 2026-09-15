# AISCC Browser Command Center Handoff — L3 substantive acceptance → Git persistence

## repository identity

```text
branch:
main

HEAD:
968a7164cb50cfeaee5a6f83b7455ab87f6ccbd1
```

## accepted L3 result

```text
stage:
Public-only HTTP API composition

shared-limit policy:
HUMAN_PROVIDED / ACCEPTED V1

shared limits:
30/min/run
120/min/source
1200/min/campaign

focused:
178 PASS

full suite:
1375 PASS / 3 existing SKIP / 0 FAIL / 0 ERROR

real provider calls:
0

Public admission:
DISABLED
```

## exact accepted source

- `migrations/versions/20260916_0015_public_live_shared_limits.py`
- `src/aiscc/persistence/public_live_limits.py`
- `src/aiscc/public_live/http.py`
- `src/aiscc/public_live/source.py`
- `tests/integration/next_action/test_genesis_bootstrap.py`
- `tests/integration/providers/test_external_ide_execution_ingress.py`
- `tests/integration/providers/test_external_ide_execution_start.py`
- `tests/integration/public_live/test_http.py`
- `tests/integration/public_live/test_persistence.py`
- `tests/integration/public_live/test_shared_limits.py`
- `tests/integration/self_dogfood/test_task_ready_entry.py`
- `tests/integration/task_authority/test_task_contract_durability.py`
- `tests/integration/workflow/test_postgres_kernel.py`
- `tests/public_live_http_helpers.py`
- `tests/unit/public_live/test_http.py`
- `tests/unit/public_live/test_source.py`

## missing governance provenance to transport now

The 0133 policy-decision package was Human-facing and did not enter the canonical Executor repository before 0135.

This persistence delivery therefore includes its exact four documents:

- `20260916_0133_aiscc-p3-3-l3-shared-limit-policy-ambiguity-human-decision-required-1.cycle.md`
- `20260916_0133_aiscc-browser-command-center-p3-3-l3-shared-limit-policy-human-decision-required-1.md`
- `20260916_0133_aiscc-browser-command-center-p3-3-l3-shared-limit-policy-decision-handoff-1.md`
- `20260916_0133_aiscc-p3-3-public-live-shared-limit-policy-amendment-proposal-1.md`

They are provenance, not controlling policy.

The controlling policy remains the 0135 accepted V1 amendment.

## known release blocker

```text
PUBLIC_LIVE_LIMITER_RETENTION_RESOURCE_BOUND_UNRESOLVED
```

Reason:

the current shared limiter keeps historical minute buckets without an accepted finite retention/GC policy.

This does not block L3 persistence.

It must remain visible and unresolved until a later versioned policy/implementation proves bounded storage before Public admission enablement.

## persistence only

Do not:

- edit source;
- add retention cleanup in this turn;
- rerun PostgreSQL/full tests merely to refill evidence;
- implement L4/L5;
- enable Public admission;
- call provider;
- push/deploy.

Use:

`.aiassistant/tasks/active/20260916_0405_aiscc-p3-3-public-live-l3-git-persistence-1.md`
