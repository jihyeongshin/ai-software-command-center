# AISCC Command Center Judgment

## meta

- judgment_id: `20260912_0230_aiscc-p2-3-cut-a-integration-launcher-import-path-defect-judgment-1`
- created_at: `2026-09-12T02:30:00+09:00`
- project: `AI Software Command Center (AISCC)`
- submitted_task: `.aiassistant/tasks/done/20260912_0135_aiscc-p2-3-private-s1-cut-a-materialized-fixture-root-rework-and-full-proof-retry-1.md`
- submitted_bundle: `20260912_0135_aiscc-p2-3-private-s1-cut-a-materialized-fixture-root-rework-and-full-proof-retry-1.zip`
- submitted_bundle_sha256: `d59b50e16b4199295cc1258002d3337d2c5a62f1aecae61ab9029e13e92eac08`
- result_status: `HOLD_RETRY_REQUIRED`
- blocker: `EXTERNAL_INTEGRATION_LAUNCHER_IMPORT_PATH_DEFECT`
- product_defect_admitted: `No`
- fixture_rework_identity: `ACCEPTED_FOR_RETRY`
- cut_a_candidate: `UNVERIFIED_DRAFT`
- cut_a_persistence: `NOT_AUTHORIZED`
- cut_b: `NOT_AUTHORIZED`
- private_s1: `NOT_AUTHORIZED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`
- handoff_required: `No`
- fresh_ide_executor_chat_for_successor: `NOT_REQUIRED`

# 판정

`0135` STOP is conformant.

Browser direct result verification:

```text
ZIP / CRC:
PASS

top-level:
1 exact

members:
39 exact

root docs:
17 / 17

canonical copies:
3 / 3

implementation copies:
19 / 19

manifest non-self:
38 / 38 SHA-256 + byte-size PASS

issued 0135 TASK/CYCLE/JUDGMENT:
3 / 3 exact

TASK.md == canonical done Task:
byte exact
```

Submitted ZIP SHA-256:

```text
d59b50e16b4199295cc1258002d3337d2c5a62f1aecae61ab9029e13e92eac08
```

# admitted fixture correction

The requested bounded materialized-root patch is exact:

```text
tests/integration/scenarios/test_stockroom_capture_runner.py

bytes:
40944

SHA-256:
373f9d5bc6f260785cdf943aa649ce99ab5826e8ae09dd2982c18db09459fbf5
```

Browser independently inspected the exported source and confirmed:

```text
materialized_destination = private_runtime_root
workspace_lease.runtime_root = private_runtime_root
workspace_lease.destination = materialized_destination
resolved_source_root = materialized_destination
later foreign-runtime negative fixture remains
```

Production validation source remains unchanged.

# admitted proof progress

```text
compile:
14 / 14 PASS

Ruff:
0 findings

strict loaders:
4 / 4 PASS

V1/V2 direct comparison:
PASS

negative loader cases:
9 / 9 PASS

targeted unit:
246 PASS / 0 skip

disposable PostgreSQL:
20260901_0008 PASS
cleanup PASS
```

# exact blocker

Integration did not execute any test body.

The Executor changed the launch shape from the repository-valid:

```text
.venv\Scripts\python.exe -B -m pytest ...
```

to an external temporary script:

```text
.venv\Scripts\python.exe -B <TEMP>\aiscc-...-trace.py ...
```

and that script then called:

```python
pytest.main(...)
```

Both integration modules failed collection on:

```text
ModuleNotFoundError: No module named 'tests'
```

for:

```text
from tests.unit.runtime.test_stockroom_image import synthetic_image
```

The same integration modules had previously collected under direct `python -m pytest`.

This is an external launcher/import-path defect. It does not establish a product,
fixture, or repository packaging defect.

# retry authority

No repository mutation is authorized.

The successor must execute pytest directly from repository root:

```text
.venv\Scripts\python.exe -B -m pytest ...
```

Do not wrap `pytest.main()` in an external script.

Do not modify `sys.path`, `PYTHONPATH`, test imports, package layout, or repository
files to compensate.

The integration test source itself is the executable boundary proof: it now contains
the exact root/source/lease assignments plus assertions for ADMITTED materialization
and final empty private root.

# phase

```text
Cut A architecture:
ACCEPTED

Cut A static:
PASS

Cut A unit:
PASS

Cut A integration:
NOT_EXECUTED / COLLECTION BLOCKED BY EXTERNAL LAUNCHER

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
