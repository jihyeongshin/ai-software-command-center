# AISCC Command Center Judgment

## meta

- judgment_id: `20260913_2019_aiscc-p2-3-provider-grant-fix-source-acceptance-and-runtime-retry-authorization-1`
- created_at: `2026-09-13T20:19:00+09:00`
- project: `AI Software Command Center (AISCC)`
- result_status: `ACCEPTED / PROVIDER_RESOURCE_GRANT_SOURCE_REWORK_CANDIDATE`
- reviewed_result_zip_sha256: `ea24a2d44a454558b5b845313d5207d6240a5507656048882ace5842d41c6e47`
- base_HEAD: `c9093e8441de230f9470313d874a33addc75423c`
- source_persistence_authorized: `Yes / exact candidate only`
- fresh_private_S1_retry_authorized: `Yes / after exact source commit only`

## accepted 1851 candidate

The 1851 result is accepted as a bounded source correction candidate.

Causal defect:

```text
provider/secret capability requests supplied no per-operation process spec
→ production context copied empty resolved_spec_fingerprint
→ StockroomOwnerRestriction rejected the context
→ ResourceGrant issuance returned none
→ EXACT_RESOURCE_GRANT_DENIED
```

Accepted correction:

```text
bind the already verified production factory docker_spec_fingerprint
into StockroomSecurityContext.process_spec_fingerprint

reject any conflicting nonempty caller-supplied spec
```

Security evaluator/config/resource exact-match behavior remains unchanged.

Targeted proof:

```text
pre-fix reproduction:
exact 1822 denial reproduced

targeted test commands:
23 PASS
73 PASS

distinct cases:
95 PASS

py_compile:
PASS

Ruff:
PASS

git diff --check:
PASS

external provider/network:
0
```

## combined next authority

To reduce submission-path turns, this Task may:

1. persist the exact accepted three-path source/test candidate plus the six 1822/1851 governance artifacts in one Git commit;
2. only after that exact commit succeeds, execute one fresh S1 using new v3 run/attempt/root identities.

No canonical-state reconciliation is authorized in this Task. Browser reviews the runtime result next.
