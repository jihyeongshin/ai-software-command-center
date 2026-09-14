# AISCC Command Center Judgment

## meta
- created_at: `2026-09-14T18:03:27+09:00`
- reviewed_result_zip_sha256: `8af53c02e445b3148788edac1cda741b3afd0e8a82e62e210a4561dda3d134df`
- predecessor_decision: `ACCEPTED`
- predecessor_identity: `P2_4_EXTERNAL_IDE_EXECUTION_INGRESS_IMPLEMENTATION_CANDIDATE`
- persisted_predecessor_commit: `e9c17cbf2783669cf7f92df2399d3877e38c4816`
- Human_review: `20260914_1800_aiscc-p2-4-external-ide-execution-start-authority-human-review-1.md`
- Human_review_sha256: `ca4ab0a60b1c05a52befd4e2012934c42b8d6076602b1e7c21c9bdc8e20406a0`
- Human_decision: `ACCEPT`
- decision: `HUMAN_PROVIDED / ACCEPTED`
- design_id: `AISCC-P1-5-EXTERNAL-IDE-EXECUTION-START-V1`
- next_task_authorized: `Yes / implementation only`
- actual_golden_cycle_authorized: `No`
- fresh_ide_chat_required: `No`

## judgment

1721 closes the external IDE completion/submission authority gap.

The remaining known golden-cycle blocker is truthful execution start:

```text
READY
→ G_EXECUTION_STARTED
→ RUNNING
```

Provider execution provenance must not be fabricated for the external IDE producer.

Human accepts one bounded local start authority for:

```text
LOCAL_IDE_SELF_DOGFOOD_V1
```

## authorization

Implement durable one-time external start permit/receipt semantics, reuse existing P1-4 `G_EXECUTION_STARTED` and READY->RUNNING transition, preserve P1-4 as sole state owner, and prove restart/replay/concurrency/completion continuity.

No provider execution, source edit, Evidence, Judgment, Cycle or actual golden run is authorized.

Success remains Browser-review candidate only.
