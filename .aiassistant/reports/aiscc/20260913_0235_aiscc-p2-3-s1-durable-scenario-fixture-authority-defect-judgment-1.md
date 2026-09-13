# AISCC Command Center Judgment

## meta

- judgment_id: `20260913_0235_aiscc-p2-3-s1-durable-scenario-fixture-authority-defect-judgment-1`
- created_at: `2026-09-13T02:35:57+09:00`
- reviewed_task: `20260913_0206_aiscc-p2-3-s1-execution-start-durable-postgresql-verification-1`
- reviewed_result_zip_sha256: `9a60f9d9ab0849eb1b7cb1acdab815272934acc80bdb003f5c5cbae75da7fda1`
- result_status: `HOLD_REWORK_REQUIRED / DURABLE_SCENARIO_REGRESSION_TEST_SETUP_DEFECT`
- product_patch_status: `VALID_CANDIDATE / PRESERVE`
- source_write_authorized: `No`
- test_write_authorized: `Yes / exact one path`
- retained_private_runtime_access_authorized: `No`
- isolated_test_postgresql_authorized: `Yes`

# Browser judgment

0206 is a truthful verification failure, not a product-source failure.

Verified:

```text
result ZIP:
16 members / one top-level / CRC PASS

manifest:
15 / 15 exact

contract:
30 PASS / 1 FAIL / 3 BLOCKED_REQUIRED_EVIDENCE

isolated PostgreSQL:
provisioned correctly
migration head 20260901_0008
removed completely after failure

retained private S1:
not accessed
```

The failing durable scenario test did not reach the new S1 lifecycle assertions.

Exact failure:

```text
tests/integration/scenarios/test_stockroom_capture_runner.py
S2 setup loop

generic P1_4GuardAuthority.issue(...)
attempted for G_EXECUTOR_SUBMISSION

current guard contract:
G_EXECUTOR_SUBMISSION requires issuer-verified execution ref
```

This test setup predates the accepted canonical producer-binding contract.

# correction authority

Preserve product source exactly:

```text
src/aiscc/scenarios/stockroom_production.py
SHA-256:
c070e194b5d3e0ca18d952202f71860175ab36f3a51b327c7799fe5ef36bffb3
```

Modify only:

```text
tests/integration/scenarios/test_stockroom_capture_runner.py
```

The S2 setup must construct `G_EXECUTOR_SUBMISSION` through the existing canonical verified-ref path.

Required invariant:

```text
G_EXECUTOR_SUBMISSION
→ P1_4GuardAuthority.issue_from_execution_ref(...)
→ ExecutionSubmissionRef authenticated by application.execution_reference_authority
```

Do not weaken `P1_4GuardAuthority.issue`.
Do not bypass issuer verification.
Do not change production code to accommodate a stale test fixture.

After the test-only correction, rerun the same isolated PostgreSQL durable verification.
