# AISCC Browser Command Center Judgment

## judgment

- judgment_id: `20260918_0025_aiscc-p3-3-l5-hosted-ingress-edge-proof-partial-acceptance-mandatory-rollback-judgment-1`
- predecessor_task: `20260917_2236_aiscc-p3-3-public-live-l5-hosted-public-ingress-edge-proof-1`
- submitted_zip_sha256: `ae087d11277c52a94fc2dc929536659c8e5afc1f4a102544f2d2aac65a37dfe8`
- result_status: `PARTIAL_ACCEPTED`
- reject_cause: `none`
- blocking_gate: `RAILWAY_EDGE_OVERWRITE_PROOF_FAILED`
- cycle_record_action: `create`
- cycle_record_path: `.aiassistant/records/aiscc/cycles/20260918_0025_aiscc-p3-3-l5-hosted-ingress-edge-proof-partial-acceptance-mandatory-rollback-1.cycle.md`
- source_mirror_sync: `not-required`
- execution_mode: `MANUAL_COMMAND_CENTER`
- fresh_ide_executor_chat_for_successor: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`
- handoff_required: `No browser-session rotation; a narrow execution-entry handoff is included in the delivery package.`

## accepted scope

- Hosted migration `20260917_0021` is accepted and MUST NOT be rerun merely because the edge matrix failed.
- Dedicated ingress role/login boundary is accepted: exactly 8 allowed functions, raw DML 0, forbidden runtime/reconciler/execution/initializer capability absent.
- Dedicated ingress service/runtime identity is accepted.
- Final rollback is accepted: edge trust absent, public domain removed, zero authority effects, temporary migrator/SSH/admin residue absent.
- OpenAI/provider/release effects remained zero.

## not accepted

- Railway `X-Real-IP`/edge overwrite authority.
- Hosted Phase C overall acceptance.
- Public admission enablement.
- Public Live release.

## required rework

Only the edge-identity contract may be reworked. Do not repeat migration 0021, recreate the ingress login, create another ingress service, touch worker/initializer/owner resources, add new infrastructure, or invoke OpenAI.

The next Task first turns opaque `IDENTITY_UNAVAILABLE` into a non-sensitive internal diagnostic classification, without exposing raw IP/header/secret values. A functional trust change is allowed only when the observed failure is explained by a narrow current Railway request-contract mismatch and the change still derives authority solely from a Railway-overwritten `X-Real-IP` plus Railway edge provenance. Caller-controlled forwarding headers must never become identity authority.

## project-scope control

AISCC is a competition submission, not a long-lived production service. This rework is explicitly time-boxed to one bounded cycle. If the next cycle cannot prove the Railway overwrite boundary with a small correction, Public Live is deferred and the already-submitted Replay/static judging surface remains the competition fallback. No production-grade proxy platform redesign is authorized.

## lineage disposition

Resuming the old 2236 Task after the Railway Hobby upgrade is recorded as a provenance deviation, not a technical invalidation. No redo is required. The successor starts from a new Task ID.
