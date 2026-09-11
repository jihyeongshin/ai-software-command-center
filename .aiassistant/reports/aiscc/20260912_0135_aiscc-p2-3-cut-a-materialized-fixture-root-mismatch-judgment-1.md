# AISCC Command Center Judgment

## meta

- judgment_id: `20260912_0135_aiscc-p2-3-cut-a-materialized-fixture-root-mismatch-judgment-1`
- created_at: `2026-09-12T01:35:00+09:00`
- project: `AI Software Command Center (AISCC)`
- submitted_task: `.aiassistant/tasks/done/20260912_0125_aiscc-p2-3-private-s1-cut-a-verifier-harness-correction-and-full-proof-retry-1.md`
- submitted_bundle: `20260912_0125_aiscc-p2-3-private-s1-cut-a-verifier-harness-correction-and-full-proof-retry-1.zip`
- submitted_bundle_sha256: `f9556285b807564cd38b4044e3159b8c4ced6323a848029faa19692e3de4d034`
- result_status: `HOLD_REWORK_REQUIRED`
- blocker: `INTEGRATION_TEST_MATERIALIZED_FIXTURE_ROOT_MISMATCH`
- semantic_owner: `CUT_A_INTEGRATION_TEST`
- production_validation: `PRESERVED / CORRECTLY_FAIL_CLOSED`
- cut_a_candidate: `UNVERIFIED_DRAFT`
- cut_a_persistence: `NOT_AUTHORIZED`
- cut_b: `NOT_AUTHORIZED`
- private_s1: `NOT_AUTHORIZED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`
- handoff_required: `No`
- fresh_ide_executor_chat_for_successor: `NOT_REQUIRED`

# 판정

`0125` Executor STOP은 conformant하다.

Browser direct verification:

```text
ZIP / CRC:
PASS

top-level:
1 exact

members:
38 exact

root docs:
16 / 16

canonical copies:
3 / 3

implementation copies:
19 / 19

manifest non-self:
37 / 37 SHA-256 + byte-size PASS

TASK.md == canonical done Task:
byte exact
```

Submitted result ZIP SHA-256:

```text
f9556285b807564cd38b4044e3159b8c4ced6323a848029faa19692e3de4d034
```

# admitted progress

```text
external verifier correction:
PASS

compile:
14 / 14 PASS

Ruff read-only:
0 findings

strict loaders:
4 / 4 PASS

positive V1/V2 direct object comparison:
PASS

negative loader cases:
9 / 9 PASS

targeted unit:
246 PASS / 0 skip

disposable PostgreSQL:
20260901_0008 PASS
cleanup PASS

integration:
8 PASS / 1 FAIL / 0 skip
```

Regression and final 32/32 contract review were correctly withheld after integration
failure.

# exact root cause

Failing test:

```text
tests/integration/scenarios/test_stockroom_capture_runner.py::
test_production_owner_graph_and_bounded_running_prefix
```

The application private root is:

```text
private_runtime_root = tmp_path / "private-runtime"
```

but the bounded fake materialized result still uses:

```text
materialized_destination = tmp_path

workspace_lease.runtime_root = tmp_path

resolved_source_root = tmp_path
```

Production validation checks in this order:

```text
resolved_source_root.relative_to(application.private_runtime_root)

workspace_lease.runtime_root == application.private_runtime_root

workspace_lease.destination == resolved_source_root
```

Therefore the first check necessarily raises `ValueError` because `tmp_path` is the
parent of, not a descendant of, `tmp_path/private-runtime`.

The adapter converts that `AuthorityConflictError` into the observed:

```text
DENIED / RUNNING / v2
```

This is an integration-test bounded-materialization fixture mismatch. It is not a
reason to weaken production provenance/workspace validation.

# exact rework

Only:

```text
tests/integration/scenarios/test_stockroom_capture_runner.py
```

may change.

Within the bounded materialized fixture:

```text
materialized_destination = tmp_path
->
materialized_destination = private_runtime_root

workspace_lease.runtime_root = tmp_path
->
workspace_lease.runtime_root = private_runtime_root
```

Do not change the later intentional foreign-runtime negative fixture.

Do not create files in `private_runtime_root`.

Expected post-rework identity:

```text
bytes:
40944

SHA-256:
373f9d5bc6f260785cdf943aa649ce99ab5826e8ae09dd2982c18db09459fbf5
```

# phase

```text
Cut A architecture:
ACCEPTED

Cut A static:
PASS

Cut A unit:
PASS

Cut A integration:
BLOCKED BY TEST FIXTURE ROOT MISMATCH

Cut A regression:
NOT_RUN

Cut A contract:
NOT_PROVEN

Cut A persistence:
NOT_AUTHORIZED

Cut B:
NOT_AUTHORIZED

private S1:
NOT_AUTHORIZED
```
