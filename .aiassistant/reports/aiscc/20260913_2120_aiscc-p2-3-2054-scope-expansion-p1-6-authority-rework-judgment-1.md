# AISCC Command Center Judgment

## meta

- judgment_id: `20260913_2120_aiscc-p2-3-2054-scope-expansion-p1-6-authority-rework-judgment-1`
- created_at: `2026-09-13T21:20:03+09:00`
- project: `AI Software Command Center (AISCC)`
- reviewed_result_zip_sha256: `cd2cb22994fed6cdf7621eae2dad6dce74c0473ab1d12c76ed40e73d36d83898`
- current_HEAD: `15c9e975ec193526eafa0749fc97321c4d89d713`
- result_status: `REWORK_REQUIRED / P1_6_TIMESTAMP_AUTHORITY_SCOPE_EXPANSION_AUTHORIZED`
- private_runtime_retry_authorized: `No`
- targeted_P1_6_source_rework_authorized: `Yes`

## accepted 2054 diagnosis

2054 correctly stopped at its source allowlist boundary.

Exact reproduced incompatibility:

```text
source authority instant:
2026-09-10T18:24:00+09:00

row-decoded instant:
2026-09-10T09:24:00+00:00

same instant:
true

stored legacy fingerprint:
0f1b766335e5962dfa96aa9e2f029aa4bcc1622d3c3cf9fa70968d48d216b238

recomputed fingerprint from decoded row:
7077ee73f2cb877b8a4120f718051b9c21396e8f4e224cfde745428bec7179d3

error:
HistoricalEvidenceProvenanceError
historical evidence checkpoint immutable authority disagrees
```

P1-7 translated the P1-6 historical-authority failure to `JudgmentAuthorityError(AUTHORITY_CONFLICT)`, preventing final S1 transition.

The correction owner is P1-6. This Task opens only the evidence authority serialization/resolver boundary and related targeted tests.

Required outcome:

```text
same instant / different timezone-offset representation:
canonical equivalent

different instant:
not equivalent / deny

legacy sealed authority:
remains verifiable through an explicit bounded compatibility path

arbitrary fingerprint mismatch:
never accepted
```
