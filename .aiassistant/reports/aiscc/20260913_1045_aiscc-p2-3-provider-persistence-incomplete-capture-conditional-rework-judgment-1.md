# AISCC Command Center Judgment

## meta

- judgment_id: `20260913_1045_aiscc-p2-3-provider-persistence-incomplete-capture-conditional-rework-judgment-1`
- created_at: `2026-09-13T10:45:43+09:00`
- reviewed_task: `20260913_0253_aiscc-p2-3-provider-persistence-failure-ownership-diagnosis-1`
- reviewed_result_zip_sha256: `899f433fd92c57f601c9076ded6721c7cc605339c7ace8dc08b8246298d3bc44`
- result_status: `HOLD_REWORK_REQUIRED / DIAGNOSTIC_CAPTURE_INCOMPLETE`
- conditional_test_rework_authorized: `Yes / only after exact Phase A proof`
- product_source_write_authorized: `No`
- retained_private_runtime_access_authorized: `No`
- isolated_test_postgresql_authorized: `Yes`

# Browser judgment

0253 is a truthful partial diagnosis.

Verified:
```text
16 members / one top-level / CRC PASS
manifest 15 / 15 exact
contract 30 PASS / 3 BLOCKED_REQUIRED_EVIDENCE
provider tests collected/executed once: 23
provider result: 12 passed / 11 failed
candidate bytes unchanged
retained private S1 not accessed
isolated PostgreSQL removed
```

The executor's output filter discarded ten primary traceback sections, therefore these remain unproved:
```text
ALL_11_FAILURES_CATEGORIZED
FAILURE_CATEGORY_COUNTS_SUM_11
MINIMAL_REWORK_PATH_SET_IDENTIFIED
```

Static source evidence independently establishes two stale test discrepancies in:
`tests/integration/providers/test_execution_persistence.py`.

1. `DurableSyntheticDispatcher.dispatch` computes a synthetic argument fingerprint without current canonical
   `resolved_dispatch_context`; ten currently failing positive/bounds nodes use this dispatcher.

2. `SameDomainWrongResourceService._issue_capability` omits current optional keywords
   `execution_attempt_id`, `provider_profile_id`, `provider_profile_version`, `resolved_spec_fingerprint`;
   the SAME_DOMAIN_WRONG_RESOURCE node is already known to fail on `execution_attempt_id`.

These are not yet accepted as the exhaustive cause of all 11 failures.

# conditional authority

Phase A must capture all 23 provider cases with both raw pytest output and built-in JUnit XML, and categorize all 11
failures without losing tracebacks.

Only if Phase A proves exactly:
```text
10 failures = STALE_DURABLE_SYNTHETIC_DISPATCHER_FINGERPRINT
1 failure  = STALE_SAME_DOMAIN_WRONG_RESOURCE_SIGNATURE
0 failures = product service/repository/candidate defect
```
may Phase B edit exactly:
```text
tests/integration/providers/test_execution_persistence.py
```

Any additional or unresolved root cause:
```text
STOP_WITH_REPORT_EXPORT
no source/test write
```
