# AISCC Command Center Judgment

## meta

- judgment_id: `20260913_1102_aiscc-p2-3-s1-execution-start-candidate-final-acceptance-judgment-1`
- created_at: `2026-09-13T11:02:29+09:00`
- project: `AI Software Command Center (AISCC)`
- reviewed_task: `20260913_1045_aiscc-p2-3-provider-persistence-complete-capture-conditional-fixture-rework-1`
- reviewed_result_zip_sha256: `50dce7aa4ad298021848a9ac96adf32c5ffacd0fc403a3ae5a7f54273283500e`
- result_status: `ACCEPTED / S1_EXECUTION_START_SOURCE_AND_FIXTURE_CANDIDATE_COMPLETE`
- git_persistence_authorized: `Yes`
- retained_runtime_recovery_authorized: `No`

# Browser judgment

1045 is accepted.

Independent Browser verification:

```text
result ZIP:
20 members / one top-level / CRC PASS

manifest:
19 / 19 byte/hash exact

TASK.md:
canonical done bytes exact

contract:
53 / 53 PASS
```

Phase A complete-capture proof:

```text
provider tests:
23 executed

pre-fix:
12 passed / 11 failed

root-cause categories:
10 STALE_DURABLE_SYNTHETIC_DISPATCHER_FINGERPRINT
1 STALE_SAME_DOMAIN_WRONG_RESOURCE_SIGNATURE
0 other categories

candidate causality:
NO_EXECUTION_PATH_FOUND
```

Conditional correction:

```text
modified provider fixture only:
tests/integration/providers/test_execution_persistence.py

production provider source:
unchanged

Stockroom production candidate:
unchanged

scenario integration candidate:
unchanged
```

Post-fix durable verification:

```text
provider persistence:
23 / 23 PASS

scenario durable suite:
55 / 55 PASS

workflow handoff:
3 / 3 PASS

full unit:
741 passed / 2 skipped / 0 failed

py_compile:
PASS

Ruff:
PASS

git diff --check:
PASS
```

Isolated PostgreSQL was migrated to `20260901_0008` and removed without residue.

The retained private S1 environment and stranded 0036 run/attempt were not accessed.

# accepted candidate

Exact accepted tracked paths:

```text
src/aiscc/scenarios/stockroom_production.py
c070e194b5d3e0ca18d952202f71860175ab36f3a51b327c7799fe5ef36bffb3

tests/integration/scenarios/test_stockroom_capture_runner.py
dca16f6ed0de608faa7f06cd4266ad377f140971536e0a82c0e92f679da73b72

tests/integration/providers/test_execution_persistence.py
4f0bbcadf3f0cb38f6406becbb9343cda7c2787e9e2cbef3fff60be363c9c74a
```

Accepted semantics:

```text
Stockroom READY→RUNNING admission
→ exact durable EXECUTION_STARTED
→ authoritative WorkRun/attempt reload
→ RUNNING + exact causal state/version
→ only then downstream execution

S2 setup:
canonical issuer-verified G_EXECUTOR_SUBMISSION

provider test fixtures:
current resolved_dispatch_context fingerprint contract
current _issue_capability optional keyword contract
```

# acceptance limits

This acceptance does not authorize:

```text
rerun of 0036 exact S1 attempt
alternate attempt ID
DB repair/delete/reset
private runtime-root cleanup
manual continuation
```

The stranded durable state remains:

```text
WorkRun:
RUNNING / v2

ExecutionAttempt:
NOT_STARTED

execution operations:
0

runtime evidence:
none

Judgment:
none
```

After persistence, the next governance action is a separate recovery-design/authorization decision for this exact stranded state.
