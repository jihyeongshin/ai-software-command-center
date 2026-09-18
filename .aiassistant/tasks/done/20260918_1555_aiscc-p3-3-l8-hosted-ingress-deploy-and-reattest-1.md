# AISCC Task

## meta

- task_id: `20260918_1555_aiscc-p3-3-l8-hosted-ingress-deploy-and-reattest-1`
- phase: `P3-3 / L8 preactivation`
- work_type: `HOSTED_INGRESS_DEPLOY_AND_REATTEST`
- execution_model: `THIN_CC_THICK_EXECUTOR`
- entry_commit: `dd858cad5c7a40cc4f3968a122762b8415b40403`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- public_release_authority: `NONE`
- provider_call_authority: `NONE`
- campaign_mutation_authority: `NONE`

## Goal

Deploy the accepted ingress AdmissionService composition to the existing Railway Public Live ingress service and establish fresh hosted evidence while keeping the system fail-closed.

Success means:
- the ingress service is running the exact accepted source commit;
- hosted DB and ingress authority are re-attested;
- Public admission remains disabled;
- there is no public ingress domain or edge-trust enablement;
- no provider credential/call is involved.

## Must preserve

- Public Replay unchanged;
- Public admission `DISABLED`;
- Public Live `NOT_RELEASED`;
- hosted PostgreSQL data is observation-only in this Task;
- no campaign/control mutation;
- no DB migration;
- ingress retains least-privilege role only;
- no raw table DML authority;
- no owner/runtime/reconciler/execution/initializer authority granted to ingress;
- ingress has no OpenAI/provider secret;
- no real provider call;
- no public ingress domain;
- Railway edge-trust variable absent;
- worker/initializer/owner services are observation-only.

## Authorized external mutation

The Task authorizes only:

1. deployment/redeployment of the existing `aiscc-public-live-ingress` service to the exact accepted source commit or a narrow in-scope successor commit required to fix an actual deployment-only defect;
2. creation and deletion of a task-owned temporary private verifier inside the existing Railway project when necessary to obtain read-only DB/private-network evidence;
3. safety cleanup that removes accidental ingress public exposure or edge-trust enablement if unexpectedly present.

No new persistent paid resource, plan change, public domain creation or role grant is authorized.

## Must not do

- mutate hosted DB rows;
- insert/update/delete campaign/control data;
- run Alembic upgrade/downgrade;
- grant/revoke DB privileges except no-op verification; if current authority is wrong, STOP;
- create a public ingress domain;
- set/enable edge trust;
- inject/read/export a provider key;
- modify worker/initializer/owner configuration;
- deploy Cloudflare;
- modify frontend release config;
- perform OpenAI/provider request;
- enable Public admission;
- release Public Live.

## Authority closure

Executor owns deployment/read-only verification mechanics.

Allowed equivalent mechanisms include:
- Railway CLI/API;
- existing authenticated project context;
- service deployment status/log inspection;
- private-network health verification;
- task-owned temporary private verifier;
- presence-only variable inspection;
- read-only aggregate/catalog SQL.

Do not STOP because a particular CLI command differs from Browser expectation.

If deployment reveals a narrow source/packaging defect inside the already accepted ingress semantics, Executor may correct it, add regression proof, commit/push and deploy the successor commit. Do not change product/security semantics.

## Required hosted evidence

At minimum:

### A. deployment identity

- exact ingress service name/id;
- exact deployment id;
- source commit;
- region/replica state;
- deployment status healthy/successful;
- private service remains without public HTTP domain/TCP proxy.

### B. ingress environment boundary

Presence-only proof:
- Live DB binding present;
- source HMAC binding present;
- `PUBLIC_LIVE_API_ORIGIN` presence/value classification may be reported without secret material;
- edge-trust variable absent;
- `AISCC_OPENAI_API_KEY` absent;
- `OPENAI_API_KEY` absent;
- owner DB variable absent.

Do not print secret values.

### C. hosted database

Read-only:
- Alembic/current migration head expected `20260918_0023`;
- session/current user expected ingress login when checked through ingress credential path;
- ingress capability membership present;
- runtime/reconciler/execution/initializer memberships absent;
- elevated role flags absent;
- effective raw table INSERT/UPDATE/DELETE authority remains zero;
- effective function surface remains the accepted narrow ingress surface, including the admission/start functions required by the 1549 local proof;
- direct maintenance privilege remains denied.

If any privilege is broader than accepted, STOP. Do not repair it in this Task.

### D. control/campaign observation

Read-only:
- `public_control` row count;
- `enabled` must be false;
- active campaign null/equality classification only;
- incident null/non-null classification;
- `public-live-v1` campaign row count;
- if present: exact scenario/version/HMAC and policy/content digest equality to canonical source values;
- if absent: report `ABSENT_PREACTIVATION`, do not create it.

An absent campaign is not by itself a Task failure because release-time campaign materialization is separately authorized later.

### E. service health

Prove the deployed ingress process starts successfully with the accepted runtime identity.

Use private/internal evidence where possible.

Do not add edge trust or a public domain merely to recreate the already accepted hosted spoof matrix.

### F. final safe state

- Public admission disabled;
- Public Live not released;
- public ingress domain 0;
- edge trust absent;
- provider secret absent from ingress;
- provider calls 0;
- temporary verifier removed;
- Replay unchanged.

## Stop boundary

STOP if:

- DB head differs and would require migration;
- current role/grants are broader or missing and would require privilege mutation;
- control is enabled;
- campaign state conflicts with canonical fixed identity/digests;
- deployment requires public exposure/edge trust;
- deployment requires provider credential;
- success requires worker/initializer/owner mutation;
- a new paid persistent resource/plan is required;
- source defect requires a new semantic/security choice.

Do not STOP for:
- campaign row absence;
- CLI mechanism differences;
- need for a temporary private read-only verifier;
- passive unrelated Railway autodeploy observation.

## acceptance target

Return:

`L8_HOSTED_INGRESS_PREACTIVATION_CANDIDATE / BROWSER_REVIEW_REQUIRED`

Do not mark L8 accepted/closed or release-ready yourself.

## Git / persistence

- verify HEAD/origin main equals entry commit before substantive work;
- persist supplied Cycle/Judgment/Handoff;
- move this Task active -> done;
- commit/push governance and any authorized narrow source correction;
- no amend/rebase/force-push.

## export

Create:

`.aiassistant/reports/target/20260918_1555_aiscc-p3-3-l8-hosted-ingress-deploy-and-reattest-1/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `HOSTED_DEPLOYMENT_IDENTITY.md`
- `HOSTED_DB_AUTHORITY_REATTESTATION.md`
- `CONTROL_CAMPAIGN_OBSERVATION.md`
- `FINAL_SAFE_STATE.md`
- `WORKSPACE_STATE.md`
- changed files preserving project-relative paths

Also create:

`.aiassistant/reports/target/20260918_1555_aiscc-p3-3-l8-hosted-ingress-deploy-and-reattest-1.zip`

Verify archive integrity and report SHA-256.
