# AISCC Command Center Judgment

## meta

- judgment_id: `20260912_2238_aiscc-p2-3-s1-bound-ref-partial-candidate-hold-judgment-1`
- created_at: `2026-09-12T22:38:58+09:00`
- project: `AI Software Command Center (AISCC)`
- reviewed_task: `20260912_2158_aiscc-p2-3-s1-canonical-execution-bound-ref-contract-and-source-rework-1`
- reviewed_result_zip_sha256: `f10042c12a6582afb4a8047f92786d27b99f939034b83cf97f20903dbcf5d38e`
- result_status: `HOLD_REWORK_REQUIRED / VALID_PARTIAL_PATCH_RETAINED`
- reject_cause: `UNIT_BASELINE_POLICY_MISMATCH_AND_ONE_NEGATIVE_REGRESSION_GAP`
- cycle_record_action: `create`
- execution_mode: `MANUAL_COMMAND_CENTER`

# Browser judgment

2158 result is a valid partial source candidate, not a success candidate.

Verified bundle:

```text
22 members
one top-level
CRC PASS
manifest 21 / 21 exact
TASK == canonical done Task
```

Executor contract:

```text
46 PASS
1 EXECUTED_FAIL
1 BLOCKED_REQUIRED_EVIDENCE
```

Accepted partial findings:

```text
canonical V1 bound-ref codec:
implemented

verified-only G_EXECUTOR_SUBMISSION issuance:
implemented

historical bound-ref reconstruction:
implemented

CURRENT / LINK / PRODUCER separation:
implemented candidate

runner order:
preserved

compile:
PASS

Ruff:
PASS

targeted integration:
40 passed / 1 skipped
```

Not accepted yet:

```text
UNIT_REGRESSION_PYTEST_PASS:
FAILED

UNRELATED_PENDING_TRANSITION_REGRESSION_DENIED:
BLOCKED_REQUIRED_EVIDENCE
```

# unit failure classification

The unit failure is:

```text
tests/unit/scenarios/test_contracts.py::test_static_module_has_no_execution_or_integration_imports
```

The observed forbidden import is `collections.abc` in `stockroom_production.py`.

2158 mechanically confirmed that exact import already exists at required HEAD and was not introduced by the candidate patch.
Therefore this is a pre-existing source/test-policy mismatch, not evidence that the producer-binding patch introduced the import.

The successor must inspect the test intent before changing it.
If the test's semantic purpose is only to forbid execution/integration coupling and `collections.abc` is a normal standard-library
dependency already present in accepted HEAD, a narrow test-policy correction is authorized.
Broad weakening is not.

# retained dirty candidate

Do not restore or discard the five-path 2158 patch.

The successor starts from the exact dirty hashes recorded in its Task.

# session/Python

Continue the same 2125/2158 IDE Executor chat.

Exact Python:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe
```

No `python`, `py`, WindowsApps alias or PATH discovery.
