# AISCC Task

## meta

- task_id: `20260918_1549_aiscc-p3-3-l8-preactivation-ingress-admission-composition-1`
- phase: `P3-3 / L8 preactivation`
- work_type: `PREACTIVATION_INGRESS_ADMISSION_COMPOSITION`
- execution_model: `THIN_CC_THICK_EXECUTOR`
- entry_commit: `319b502b51aac05b549aaea6cfa3ae0e1949e78d`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- Railway_mutation_authority: `NONE`
- Cloudflare_mutation_authority: `NONE`
- provider_call_authority: `NONE`
- release_authority: `NONE`

## Goal

Remove the current source-level release blocker by binding the already accepted Public Live atomic admission + start contract into the hosted ingress composition.

The resulting source must be release-capable while remaining fail-closed whenever DB control/admission is disabled.

This is a source/local-proof Task only. Do not deploy or activate anything.

## Current known gap

Current canonical `src/aiscc/public_live/ingress.py` constructs:

```python
PublicLiveApp(source, PublicLiveIngressLimits(repository), None)
```

The `admission=None` binding was correct for earlier hosted edge proof, but L8 cannot release until the ingress uses the already accepted `AdmissionService` with the exact frozen Public Live identity/pins/start contract.

## Must preserve

- separate Public Live DB; no owner DB route;
- ingress least-privilege DB identity and exact role boundary;
- fixed campaign `public-live-v1`;
- fixed HMAC version `v1`;
- fixed scenario `stockroom-s1-normal`;
- fixed scenario version `1.0.0`;
- server-owned policy/content pins only;
- accepted atomic admission behavior;
- accepted `StartContract` / durable initializer chain;
- `public_control.enabled=false` still produces `LIVE_DISABLED` and no run/start side effect;
- no provider secret in ingress;
- no provider/OpenAI call;
- no public free-form input;
- no owner/admin/cancel route;
- Replay independence;
- Human release authority.

## Must not do

- deploy or restart Railway;
- change Railway variables/domain/edge trust/roles;
- create or modify campaign rows in hosted DB;
- enable admission/control;
- deploy Cloudflare;
- modify release `live-config.json` to enabled;
- read/insert/export provider credentials;
- execute a real provider request;
- broaden ingress DB grants;
- add owner DB access;
- introduce a new security/product semantic;
- enter final release activation.

## Authority closure

Executor owns the exact implementation mechanism inside the frozen semantics.

The Executor may inspect and reuse current accepted source for:
- `AdmissionService`;
- `IdentityPolicy`;
- `StartContract`;
- admission/start transaction primitives;
- fixed provider/live profile pin helpers;
- repository/digest/config helpers;
- existing tests/fixtures.

Prefer reusing canonical existing owners over creating parallel configuration authority.

If exact policy/content digests are already canonical, load/derive them from that canonical server-owned source. Do not invent duplicate hard-coded policy values when a canonical owner already exists.

If current source lacks a canonical way to supply an already-frozen value, the Executor may add the smallest server-owned helper/config representation needed, provided it does not create a new product/security choice.

## Allowed mutation surface

Primary:
- `src/aiscc/public_live/ingress.py`
- directly required existing `src/aiscc/public_live/**` helper/composition code
- directly related Public Live tests
- current Task/provenance/report export

Conditional:
- fixed server-owned config under existing Public Live config conventions, only for already-frozen values;
- directly related persistence helper only if required to compose the accepted AdmissionService without authority broadening.

No migration expected. If a migration appears necessary, STOP and report why; do not create it in this Task.

## Required proof

At minimum:

1. production ingress `create_app()` constructs a non-None accepted admission binding;
2. binding uses exact fixed campaign/HMAC/scenario/version identity;
3. binding uses canonical server-owned policy/content digests;
4. binding includes the accepted `StartContract`;
5. ingress still rejects provider/owner DB secret authority;
6. runtime identity verification remains unchanged/least-privilege;
7. disabled control returns `LIVE_DISABLED`;
8. disabled control creates:
   - no public run;
   - no reservation;
   - no outbox/start candidate;
   - no provider/worker side effect;
9. when an isolated test DB is explicitly prepared with the accepted disabled→enabled fixture, one accepted admission writes the exact atomic run/start records expected by L2/L5 ownership;
10. replay/idempotency behavior remains accepted;
11. no provider call occurs;
12. directly affected unit/integration tests PASS;
13. Public Live security/admission regression subset PASS;
14. Ruff/format/narrow mypy/diff-check as applicable;
15. Git commit/push exact changed-path inventory.

Do not substitute a mocked `AdmissionService` for the production composition proof.

## Stop boundary

STOP only if success requires:

- a new policy/content digest choice not already frozen;
- a new DB role/grant;
- a schema migration;
- hosted DB mutation;
- Railway/Cloudflare mutation;
- provider credential/call;
- admission enablement;
- new owner-route authority;
- semantic redesign.

Do not STOP for:
- interpreter/shell/helper differences;
- locating the canonical frozen digest owner;
- test fixture construction;
- refactoring composition within allowed source.

## acceptance target

Return:

`L8_PREACTIVATION_INGRESS_COMPOSITION_CANDIDATE / BROWSER_REVIEW_REQUIRED`

Do not mark release-ready, do not mark L8 accepted/closed and do not deploy.

## Git / persistence

- verify HEAD and origin/main exactly equal `319b502b51aac05b549aaea6cfa3ae0e1949e78d`;
- persist supplied Cycle/Judgment/Handoff;
- move this Task active -> done;
- source + governance commit grouping is Executor-owned;
- ordinary commit/push authorized;
- no amend/rebase/force push.

## export

Create:

`.aiassistant/reports/target/20260918_1549_aiscc-p3-3-l8-preactivation-ingress-admission-composition-1/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `INGRESS_ADMISSION_COMPOSITION_PROOF.md`
- `DISABLED_GATE_NO_SIDE_EFFECT_PROOF.md`
- `ENABLED_FIXTURE_ATOMIC_START_PROOF.md`
- `FINAL_SAFE_STATE.md`
- `WORKSPACE_STATE.md`
- changed files preserving project-relative paths

Also create:

`.aiassistant/reports/target/20260918_1549_aiscc-p3-3-l8-preactivation-ingress-admission-composition-1.zip`

Verify archive integrity and report SHA-256.
