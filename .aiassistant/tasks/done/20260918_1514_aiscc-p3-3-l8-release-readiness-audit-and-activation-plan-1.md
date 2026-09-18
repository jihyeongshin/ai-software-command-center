# AISCC Task

## meta

- task_id: `20260918_1514_aiscc-p3-3-l8-release-readiness-audit-and-activation-plan-1`
- phase: `P3-3 / L8`
- work_type: `L8_RELEASE_READINESS_AUDIT`
- execution_model: `THIN_CC_THICK_EXECUTOR`
- entry_commit: `ae39ce084d2af3ffec8a35fc84e5301a9a6daf76`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- external_mutation_authority: `NONE`
- public_release_authority: `NONE`
- real_provider_call_authority: `NONE`

## Goal

Prepare the final L8 Human release-decision package without activating Public Live.

Determine, with current evidence, whether the system is ready for an explicit Human choice between:

```text
RELEASE_PUBLIC_LIVE
```

and

```text
KEEP_REPLAY_PUBLIC
```

Do not make that decision for the Human.

## Must preserve

- Public Replay remains available and unchanged;
- Public admission remains `DISABLED`;
- Public Live remains `NOT_RELEASED`;
- no real provider/OpenAI request;
- no provider secret disclosure;
- no Railway/Cloudflare/OpenAI configuration mutation;
- no new paid resource;
- all accepted L3-L7 evidence remains intact;
- release and activation authority remains Human-owned.

## Must not do

- enable admission/campaign;
- enable Railway edge trust;
- create/change public domain;
- change Railway variables/roles/scale/deployment;
- deploy Cloudflare;
- change `public/replay/live-config.json` to enabled;
- change CSP to a real API origin;
- insert/read/export a raw provider key;
- perform a paid/provider request;
- create a new OpenAI project/service account/key;
- enter release activation.

## Authority closure

The Executor may use read-only inspection of:

- repository/canonical governance;
- Railway service/resource/deployment/variable names and presence-only state where already authenticated;
- current public endpoint/domain presence;
- current DB/campaign/admission projections through existing safe read paths;
- current provider profile/configuration files;
- current account/project capability metadata only when available through an already authorized read-only mechanism and without secret material;
- public Cloudflare Replay response/headers.

If an external service requires login/re-authentication or Human account action, record `HUMAN_REQUIRED`; do not bypass it.

## Required readiness questions

Answer each with `READY`, `NOT_READY`, or `HUMAN_REQUIRED`, plus exact evidence:

1. Railway backend services required for bounded Live still exist and are healthy enough for release planning.
2. Hosted DB is at the expected migration head and accepted least-privilege roles remain intact.
3. Public admission/campaign remains disabled before release.
4. Public ingress domain and edge-trust state are known exactly.
5. One exact API origin can be selected at release time without changing product semantics.
6. Frontend release binding requires only the accepted `live-config.json` + exact CSP origin change (or identify the exact additional change).
7. Application budgets/call ceilings/campaign window remain current and internally consistent.
8. Provider/model/profile authority is still current enough for release, including any freshness window that has expired.
9. OpenAI project/account/service-account/key readiness can be established without exposing secrets; otherwise name the Human evidence required.
10. Decide whether a real-provider canary is materially required before release. This is a factual prerequisite determination, not authorization to run it.
11. Exact release mutations are enumerated in order.
12. Exact rollback-to-Replay-only steps are enumerated and bounded.
13. Post-release smoke checks are enumerated.
14. Any remaining Human decision is isolated to the smallest possible set.

## Provider-canary decision rule

Do not assume a canary is automatically required.

Inspect the accepted L4/provider authority and current freshness requirements.

Return one of:

- `REAL_PROVIDER_CANARY_NOT_REQUIRED_FOR_RELEASE_DECISION`
- `REAL_PROVIDER_CANARY_REQUIRED_BEFORE_RELEASE`
- `REAL_PROVIDER_CANARY_REQUIREMENT_UNRESOLVED`

If required, specify:
- exact reason;
- exact provider profile/version;
- maximum one bounded canary purpose;
- maximum spend envelope;
- evidence to capture;
- Human authorization needed.

Do not execute it.

## Evidence expected

Create a concise decision package with:

- current Git baseline;
- Railway resource/status inventory;
- DB/migration/role/admission/campaign status;
- public ingress/domain/edge-trust status;
- frontend release-binding diff plan;
- provider profile freshness/account readiness;
- canary requirement determination;
- release mutation plan;
- rollback plan;
- smoke plan;
- Human-required checklist;
- final safe-state proof.

## Stop boundary

STOP only if:

- read-only inspection cannot establish a critical prerequisite without Human authentication;
- canonical release semantics conflict;
- current external state is materially different from accepted architecture and would require redesign;
- a new paid resource or security policy is required.

A missing release-time domain/config value is not necessarily a STOP if it can be safely left as a Human release choice and the exact mutation is known.

## acceptance target

Return one of:

```text
L8_RELEASE_DECISION_READY / HUMAN_DECISION_PENDING
```

or a narrower honest blocker such as:

```text
L8_HUMAN_ACCOUNT_EVIDENCE_REQUIRED
L8_REAL_PROVIDER_CANARY_AUTHORIZATION_REQUIRED
L8_RELEASE_READINESS_BLOCKED
```

Do not mark L8 accepted/closed and do not activate anything.

## Git / persistence

Persist the supplied L7 final acceptance Cycle/Judgment/Handoff and move this Task to done at completion.

Governance-only commit/push is authorized.

No product source change is expected from this audit.

## export

Create:

`.aiassistant/reports/target/20260918_1514_aiscc-p3-3-l8-release-readiness-audit-and-activation-plan-1/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `L8_RELEASE_READINESS_MATRIX.md`
- `PROVIDER_CANARY_DECISION.md`
- `ACTIVATION_PLAN.md`
- `ROLLBACK_PLAN.md`
- `HUMAN_DECISION_CHECKLIST.md`
- `FINAL_SAFE_STATE.md`
- `WORKSPACE_STATE.md`

Also create:

`.aiassistant/reports/target/20260918_1514_aiscc-p3-3-l8-release-readiness-audit-and-activation-plan-1.zip`

Verify archive integrity and report SHA-256.
