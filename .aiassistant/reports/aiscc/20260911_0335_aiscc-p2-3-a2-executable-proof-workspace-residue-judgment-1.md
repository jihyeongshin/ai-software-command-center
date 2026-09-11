# AISCC Command Center Judgment

## meta

- judgment_id: `20260911_0335_aiscc-p2-3-a2-executable-proof-workspace-residue-judgment-1`
- created_at: `2026-09-11T03:35:00+09:00`
- project: `AI Software Command Center (AISCC)`
- submitted_task: `.aiassistant/tasks/done/20260911_0240_aiscc-p2-3-a2-static-command-transport-and-executable-proof-retry-1.md`
- submitted_bundle: `20260911_0240_aiscc-p2-3-a2-static-command-transport-and-executable-proof-retry-1.zip`
- submitted_bundle_sha256: `7492d8e3402422cf463fcbe91ae876ded6f6d70d5efcb76a3457cd5784b34660`
- result_status: `HOLD_CLEANUP_REQUIRED`
- proof_result: `EXECUTABLE_PROOF_COMPLETE`
- blocker: `UNEXPECTED_WORKSPACE_DELTA / TASK_GENERATED_PYCOMPILE_CACHE`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`
- handoff_required: `No`
- fresh_ide_executor_chat_for_successor: `NOT_REQUIRED`

# 판정

`0240` executable proof itself is accepted as complete evidence.

Browser direct verification:

```text
ZIP readability / CRC:
PASS

top-level:
1 exact

members:
11 exact

required roots:
8 / 8

canonical copies:
3 / 3

manifest non-self:
10 / 10 SHA-256 + byte-size PASS

issued 0240 TASK/CYCLE/JUDGMENT:
3 / 3 exact

TASK.md == canonical done Task:
byte exact
```

Submitted ZIP SHA-256:

```text
7492d8e3402422cf463fcbe91ae876ded6f6d70d5efcb76a3457cd5784b34660
```

# accepted executable proof

```text
py_compile:
9 / 9 PASS

Ruff:
9 / 9 PASS

strict A2 config loaders:
3 / 3 PASS

git diff --check:
PASS

B3 prepared-owner:
23 PASS

A1 runner:
51 PASS

A2 PostgreSQL:
2 PASS

direct-owner:
58 PASS

aggregate:
134 PASS
0 fail
0 error
0 skip

contract review:
27 / 27 PASS
```

The frozen candidate remained byte-identical.

# only remaining blocker for this proof subregion

The mandatory `py_compile` command generated nine untracked `.pyc` files.

Executor correctly did not delete them because the prior Task cleanup allowlist authorized only:

```text
Task-owned PostgreSQL container
external temporary strict-config driver
```

The nine paths are therefore Task-generated residue, not product mutation.

They must be removed under an exact cleanup allowlist before this subregion can be marked workspace-conformant.

# exact cleanup authorization

Delete only the following nine regular files if they exist and match the expected py_compile-cache role:

- `src/aiscc/__pycache__/bootstrap.cpython-312.pyc`
- `src/aiscc/scenarios/__pycache__/capture_runner.cpython-312.pyc`
- `src/aiscc/scenarios/__pycache__/composition.cpython-312.pyc`
- `src/aiscc/scenarios/__pycache__/driver.cpython-312.pyc`
- `src/aiscc/scenarios/__pycache__/stockroom_production.cpython-312.pyc`
- `tests/integration/scenarios/__pycache__/test_stockroom_binding.cpython-312.pyc`
- `tests/integration/scenarios/__pycache__/test_stockroom_capture_runner.cpython-312.pyc`
- `tests/unit/scenarios/__pycache__/test_owner_composition.cpython-312.pyc`
- `tests/unit/scenarios/__pycache__/test_stockroom_capture_runner.cpython-312.pyc`

Do not recursively delete `__pycache__` directories.

Do not use `git clean`.

Do not rerun py_compile or pytest.

# proof reuse

Because no source/test/config bytes may change in the cleanup Task:

```text
0240 executable proof:
REUSED_ACCEPTED

134 PASS:
REUSED_ACCEPTED

27/27:
REUSED_ACCEPTED
```

after exact workspace reconciliation.

# later blocker unchanged

A2 is not final after cleanup.

The separate authority blocker remains:

```text
S2 negative EvidenceSetEvaluation
→ P1-7 Judgment
= ADAPTER_LOCAL_BINDING_ONLY
```

That will require a fresh authority Task after workspace cleanup is accepted.
