# AISCC Command Center Judgment

## meta

- judgment_id: `20260912_0120_aiscc-p2-3-cut-a-integration-fixture-runtime-root-collision-judgment-1`
- created_at: `2026-09-12T01:20:00+09:00`
- project: `AI Software Command Center (AISCC)`
- submitted_task: `.aiassistant/tasks/done/20260912_0100_aiscc-p2-3-private-s1-cut-a-ruff-line-wrap-rework-and-full-proof-retry-1.md`
- submitted_bundle: `20260912_0100_aiscc-p2-3-private-s1-cut-a-ruff-line-wrap-rework-and-full-proof-retry-1.zip`
- submitted_bundle_sha256: `e3b431fb67fa2a72259c049bc80a40ff282f06dd5372d59cb328714a1400f35c`
- result_status: `HOLD_REWORK_REQUIRED`
- blocker: `INTEGRATION_TEST_FIXTURE_RUNTIME_ROOT_COLLISION`
- semantic_owner: `CUT_A_INTEGRATION_TEST`
- production_workspace_invariant: `PRESERVED / CORRECTLY_FAIL_CLOSED`
- cut_a_candidate: `UNVERIFIED_DRAFT`
- cut_a_persistence: `NOT_AUTHORIZED`
- cut_b: `NOT_AUTHORIZED`
- private_s1: `NOT_AUTHORIZED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`
- handoff_required: `No`
- fresh_ide_executor_chat_for_successor: `NOT_REQUIRED`

# 판정

`0100` Executor STOP은 conformant하다.

Browser direct bundle verification:

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

manifest:
37 / 37 SHA-256 + byte-size PASS

issued 0100 TASK/CYCLE/JUDGMENT:
3 / 3 exact

TASK.md == canonical done Task:
byte exact
```

Submitted ZIP SHA-256:

```text
e3b431fb67fa2a72259c049bc80a40ff282f06dd5372d59cb328714a1400f35c
```

# admitted progress

```text
six authorized Ruff line-wrap paths:
AST-equivalent

compile:
14 / 14 PASS

Ruff read-only:
0 findings

V1/V2 loaders:
4 / 4 PASS

targeted unit:
246 PASS / 0 skip

disposable PostgreSQL:
20260901_0008 PASS
cleanup PASS

integration:
8 PASS / 1 FAIL / 0 skip
```

Regression and final 32/32 contract proof were correctly withheld after the mandatory
integration failure.

# exact root cause

Failing test:

```text
tests/integration/scenarios/test_stockroom_capture_runner.py::
test_production_owner_graph_and_bounded_running_prefix
```

The test itself creates fixture artifacts under `tmp_path`:

```text
test-only-provenance.json
test-only-docker.exe
```

and then passes the same directory as:

```text
private_runtime_root=tmp_path
```

`StockroomWorkspace` correctly requires:

```text
runtime root exists
AND
runtime root is empty
```

and fails closed with:

```text
RUNTIME_ROOT_NOT_EMPTY
```

Browser independently inspected the exported test source and traceback. This is a
test-fixture/runtime-root collision, not evidence that the production workspace
invariant is wrong.

Do not weaken or remove `RUNTIME_ROOT_NOT_EMPTY`.

# exact rework

Only:

```text
tests/integration/scenarios/test_stockroom_capture_runner.py
```

may change.

Use a dedicated empty child runtime root while keeping provenance/Docker executable
fixtures outside it.

Exact intended semantic patch:

```text
after test-only-docker.exe creation:

private_runtime_root = tmp_path / "private-runtime"
private_runtime_root.mkdir()
assert tuple(private_runtime_root.iterdir()) == ()

build_stockroom_production:
private_runtime_root=private_runtime_root

final cleanup assertion:
assert tuple(private_runtime_root.iterdir()) == ()
```

Expected post-rework identity:

```text
bytes:
40920

SHA-256:
1861a8cfdd1008e5efba6588b17de8ad8b1f6f088912fba026d215a8ab6379f2
```

All other 18 Cut A implementation paths remain frozen.

# phase

```text
Cut A architecture:
ACCEPTED

Cut A static:
PASS

Cut A unit:
PASS

Cut A integration:
BLOCKED BY TEST FIXTURE COLLISION

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
