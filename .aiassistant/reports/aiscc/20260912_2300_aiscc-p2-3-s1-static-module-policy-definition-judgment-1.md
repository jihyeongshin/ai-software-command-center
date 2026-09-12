# AISCC Command Center Judgment

## meta

- judgment_id: `20260912_2300_aiscc-p2-3-s1-static-module-policy-definition-judgment-1`
- created_at: `2026-09-12T23:00:00+09:00`
- project: `AI Software Command Center (AISCC)`
- reviewed_task: `20260912_2251_aiscc-p2-3-scenario-static-module-boundary-inventory-1`
- reviewed_result_zip_sha256: `32dc144746472d8d9a565ba1dda51923d80666c5a0e9e2da615fb6a206b179c0`
- result_status: `ACCEPTED / STATIC_MODULE_BOUNDARY_INVENTORY_COMPLETE`
- cycle_record_action: `create`
- execution_mode: `MANUAL_COMMAND_CENTER`

# Browser judgment

2251 inspection result is accepted.

Verified result:

```text
ZIP:
13 members / one top-level / CRC PASS

manifest:
12 / 12 exact

contract:
26 / 26 PASS

source/test changes:
none

2158 five-path dirty candidate:
preserved byte-identically

runtime/private:
not accessed
```

The Task contained an incorrect Python executable string.
Human explicitly authorized the existing corrected executable and the Executor truthfully recorded the correction.
This is admitted as an operational transport correction; issued Task bytes were not rewritten.

Correct executable:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe
```

# canonical static scenario module policy

The exact static contract/API module set is:

```text
src/aiscc/scenarios/__init__.py
src/aiscc/scenarios/catalog.py
src/aiscc/scenarios/models.py
```

Rationale from accepted inspection facts:

```text
ContractError:
defined by catalog.py

load_catalog:
defined by catalog.py

Resource:
defined by models.py

Scenario:
defined by models.py

__init__.py:
re-exports the public static API

catalog.py:
depends only on models.py within aiscc.scenarios

models.py:
has no scenario-local dependency
```

These three modules are the only members of the static import-policy check.

The following top-level scenario modules are not members of that static policy:

```text
capture_runner.py
composition.py
driver.py
enrollment.py
runtime_models.py
stockroom_production.py
```

This is a membership boundary, not an import allowlist expansion.

The existing allowed import-root set remains unchanged.

# next action

Retain the 2158 five-path candidate.
Change the unit policy from `glob("*.py")` to the exact three-module membership above.
Add the missing same-shape cross-producer negative regression.
Run the bounded validation.

Continue the existing IDE Executor chat.
No private S1 execution or Git persistence yet.
