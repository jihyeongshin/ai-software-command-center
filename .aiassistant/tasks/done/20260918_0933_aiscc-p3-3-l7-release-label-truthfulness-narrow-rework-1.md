# AISCC Task

## meta

- task_id: `20260918_0933_aiscc-p3-3-l7-release-label-truthfulness-narrow-rework-1`
- phase: `P3-3 / L7`
- work_type: `L7_FRONTEND_NARROW_REWORK`
- execution_model: `THIN_CC_THICK_EXECUTOR`
- entry_commit: `6950fe9047dbff9d0752fd63958e359a48414f0b`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- public_deployment_authority: `NONE`
- public_release_authority: `NONE`
- real_provider_authority: `NONE`

## Goal

Remove the one release-truthfulness defect in the accepted L7 source candidate.

A later valid enabled Live config must not leave any visible stale claim that Live is disabled/not enabled, while disabled/invalid config must continue to truthfully show Live as unavailable.

## Must preserve

- all four Replay scenarios and corpus bytes;
- Replay independence;
- current default `live-config.json` remains `enabled=false`, `api_origin=null`;
- fixed Live scenario/version remains `stockroom-s1-normal / 1.0.0`;
- H5 sessionStorage/idempotency/GET/polling behavior;
- no capability disclosure;
- text-only rendering;
- exact-origin CSP direction;
- Public admission `DISABLED`;
- Public Live `NOT_RELEASED`;
- current deployed Cloudflare artifact unchanged;
- zero real provider calls.

## Must not do

- deploy Cloudflare;
- mutate Railway;
- choose/create a real API origin/domain;
- enable admission or Live;
- perform provider/OpenAI request;
- alter backend API semantics;
- broaden CSP;
- redesign the page or framework;
- change Replay corpus;
- enter L8.

## Authority closure

Executor owns the narrow implementation mechanism.

Acceptable approaches include dynamic top-level release-state text, conditional visibility, or another equally truthful mechanism.

Do not stop because the exact implementation differs from Browser expectation.

## Allowed mutation surface

- `public/replay/**` only as directly required by this correction;
- directly affected frontend tests;
- deterministic build manifest/output required by changed asset bytes;
- `docs/AISCC_PUBLIC_REPLAY_DEPLOYMENT.md` only if release-binding wording needs synchronization;
- current Task/provenance/report export.

No backend source/migration changes.

## Evidence expected

At minimum:

- disabled config visibly communicates Live disabled and sends no API request;
- invalid/missing config visibly communicates fail-closed unavailable state;
- valid synthetic enabled config makes Start available and leaves no visible stale `Live is not enabled` / equivalent contradictory disabled claim;
- Replay remains usable in all three states;
- existing H5/sessionStorage/202/retry/polling tests remain PASS;
- deterministic build/check PASS;
- corpus identities unchanged;
- CSP remains narrow;
- no backend/Railway/Cloudflare/provider action;
- exact final Git commit/push;
- result ZIP manifest integrity.

## Stop boundary

STOP only if fixing this requires:
- backend semantic change;
- release/API-origin selection;
- CSP broadening;
- deployment/Railway mutation;
- provider call/credential;
- admission enablement;
- new product/security policy.

A normal frontend implementation/test adjustment is not a stop condition.

## acceptance target

Return:

`L7_FRONTEND_SOURCE_REWORK_CANDIDATE / BROWSER_REVIEW_REQUIRED`

Do not mark L7 accepted/closed yourself.

Human physical browser QA is intentionally not part of this Executor Task.

## export

Create:
`.aiassistant/reports/target/20260918_0933_aiscc-p3-3-l7-release-label-truthfulness-narrow-rework-1/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `RELEASE_LABEL_TRUTHFULNESS_PROOF.md`
- `REGRESSION_EVIDENCE.md`
- `FINAL_SAFE_STATE.md`
- changed files preserving project-relative paths

Also create:
`.aiassistant/reports/target/20260918_0933_aiscc-p3-3-l7-release-label-truthfulness-narrow-rework-1.zip`

Verify member integrity and report SHA-256.
