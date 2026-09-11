# AISCC Command Center Judgment

## meta

- judgment_id: `20260911_0228_aiscc-p2-3-a2-materialized-workspace-fixture-test-failure-judgment-1`
- created_at: `2026-09-11T02:28:00+09:00`
- project: `AI Software Command Center (AISCC)`
- submitted_task: `.aiassistant/tasks/done/20260911_0105_aiscc-p2-3-a2-materialization-output-provenance-binding-rework-1.md`
- submitted_bundle: `20260911_0105_aiscc-p2-3-a2-materialization-output-provenance-binding-rework-1.zip`
- submitted_bundle_sha256: `2fb6face15ac299b9dc013e50a14bb690ecf99aa2d3f426b2f631e15c504d4ff`
- result_status: `HOLD_REWORK_REQUIRED`
- blocker: `TEST_FAILURE`
- root_cause: `NO_SIDE_EFFECT_TEST_FIXTURE_VIOLATES_DOCKER_SPEC_WORKSPACE_PRECONDITION`
- product_source_disposition: `FREEZE_CURRENT_CANDIDATE`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`
- handoff_required: `No`
- fresh_ide_executor_chat_for_successor: `NOT_REQUIRED`

# 판정

`0105` mandatory STOP은 conformant하다.

Browser direct bundle verification:

```text
ZIP readability / CRC:
PASS

top-level:
1 exact

members:
28 exact

required root docs:
15 / 15

canonical/source/config/test copies:
13 / 13

manifest non-self:
27 / 27 SHA-256 + byte-size PASS

issued 0105 TASK/CYCLE/JUDGMENT:
3 / 3 exact
```

Submitted ZIP SHA-256:

```text
2fb6face15ac299b9dc013e50a14bb690ecf99aa2d3f426b2f631e15c504d4ff
```

# Executor evidence

```text
mandatory static:
PASS

py_compile:
8 / 8 PASS

Ruff:
8 / 8 PASS

strict config:
3 / 3 PASS

git diff --check:
PASS

B3 owner-model tests:
23 PASS

A1 runner:
51 PASS

PostgreSQL/Alembic:
20260901_0008 PASS

A2 integration:
1 PASS / 1 FAIL / 0 skip

direct-owner regressions:
NOT_RUN after mandatory test failure

Git persistence:
NOT_RUN
```

# Browser independent failure analysis

The current candidate production path is intentionally fail-closed when constructing the Stockroom process specification.

The accepted `DockerRunSpec` validation requires the materialized workspace to be an existing directory before its fingerprint/scope can be admitted.

The 0105 no-side-effect integration fixture instead constructs:

```text
materialized_destination =
tmp_path / "bounded-materialized-output"
```

but deliberately performs no filesystem materialization and does not create that directory.

The exact adapter path then reaches:

```text
bound MaterializedStockroom
→ execution_factory.prepare_inputs(...)
→ build_stockroom_spec(...)
→ stockroom_spec_fingerprint(...)
→ _validate_stockroom_spec(...)
```

where the existing directory precondition fails.

The adapter correctly converts that fail-closed `ValueError` into:

```text
materialize:
DENIED
```

Therefore the observed test failure does not currently demonstrate a product-source defect in the new materialized-result binding.

It demonstrates that the positive no-side-effect test fixture claims a materialized workspace path that does not satisfy the frozen B2 Docker-spec contract.

# correction

Freeze all current production/model/config source.

Modify only:

```text
tests/integration/scenarios/test_stockroom_capture_runner.py
```

For the no-side-effect positive materialization stub, use an **already existing** absolute empty directory as the returned `workspace_lease.destination` / `resolved_source_root`.

The simplest authorized shape is the existing pytest `tmp_path` itself.

Do not create a fake child directory merely to satisfy the test.

Do not relax `_validate_stockroom_spec`.

Do not change production source.

# proof meaning

Using `tmp_path` as the no-side-effect stub destination proves only:

```text
factory-controlled return-object provenance
execution-factory construction contract
anti-swap behavior
```

It does NOT prove real B1 filesystem materialization.

Real materialization remains a later runtime prerequisite.

# known remaining blocker

Even if this retry passes, A2 is not final.

The separately admitted blocker remains:

```text
S2 Judgment negative evidence-set evaluation:
ADAPTER_LOCAL_BINDING_ONLY
```

That requires a separate P1-6/P1-7 authority task after this test-only closure.
