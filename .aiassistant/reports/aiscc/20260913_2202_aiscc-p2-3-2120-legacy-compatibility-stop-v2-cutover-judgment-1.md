# AISCC Command Center Judgment

## meta

- judgment_id: `20260913_2202_aiscc-p2-3-2120-legacy-compatibility-stop-v2-cutover-judgment-1`
- created_at: `2026-09-13T22:02:10+09:00`
- project: `AI Software Command Center (AISCC)`
- reviewed_result_zip_sha256: `f3cdd7cd26455bb2796f3a9580bfe635fd5dc0adf1aa0ec58e3c06e6056a80db`
- current_HEAD: `15c9e975ec193526eafa0749fc97321c4d89d713`
- result_status: `REWORK_REQUIRED / LEGACY_COMPATIBILITY_DECLINED_FOR_SUBMISSION_PATH`
- private_runtime_retry_authorized: `No`
- stockroom_v2_cutover_source_rework_authorized: `Yes`

## 2120 acceptance

2120 correctly proved that the existing generic P1-6 rows do not retain enough trusted original `issued_at` representation to reconstruct old literal-offset fingerprints safely.

Accepted stop:

```text
LEGACY_FINGERPRINT_COMPATIBILITY_REQUIRES_EXPLICIT_SCHEMA_OR_MIGRATION
```

Browser direction for the competition submission path:

```text
do not retrofit generic legacy compatibility now
do not migrate or rewrite old authority rows
do not weaken historical verification
preserve legacy v1 authority as historical evidence

instead:
create a prospective Stockroom evidence-authority v2
with UTC-stable timestamp representation and disjoint durable identities
```

This is a scoped product cutover, not a claim that generic P1-6 timestamp semantics are globally repaired.

Success requires the old v1 config/authority to remain byte/identity preserved while new Stockroom runs use v2 only.
