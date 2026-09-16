# 작업지시서: P3-3 L5 Public Live Context Resource Capability + Secret Proof Retry

## meta

- task_id: `20260916_1430_aiscc-p3-3-public-live-l5-public-context-resource-capability-and-secret-proof-retry-1`
- created_at: `2026-09-16 KST`
- work_type: `REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `04436a11adc6dd6e70b4a98568fe878cc4c9f4aa`
- predecessor_task: `20260916_1419_aiscc-p3-3-public-live-l5-predispatch-secret-resolution-and-proof-completion-retry-1`
- primary_semantic_owner: `P3-3 L5 exact Public Live context-resource capability compatibility + hosted secret proof`

Use the current IDE Executor conversation. No fresh chat is required.

## current state

```text
HEAD:
04436a11adc6dd6e70b4a98568fe878cc4c9f4aa

L4:
ACCEPTED / CLOSED

L5:
OPEN / LOCAL REWORK

Human Railway deployment:
NOT_AUTHORIZED

Public admission:
DISABLED

Public Live:
NOT_RELEASED
```

## retained candidate

Retain the 1419 cumulative candidate.

Expected source/config/test inventory:

`12`

Exact retained inventory:

- `src/aiscc/providers/external_ide.py` — `cc126eee28ca16f9eb1fd7710c161bcb99a8410f16055de8cc2959d41489e7bc`
- `src/aiscc/providers/openai_responses.py` — `7b225ee1c1aa85d46e38bf93649a79f68a37c95d01a80d7468aa7b98506ba1b6`
- `src/aiscc/providers/service.py` — `05e3788f3ba2ba51b56127e2fae929d0afba11f263d773bc012ddb8785af9a52`
- `src/aiscc/public_live/luna_profile.py` — `de4117f63066079f5971e0d569fdb22c1d510358675c8d2ebb35a3b4ed742424`
- `src/aiscc/runtime/docker.py` — `bc204813d660f4baa417ddb5a659c8586dcfcb741817c05476f9a0e04432df44`
- `src/aiscc/runtime/process.py` — `514b528e40dca70b4ddfa44641cdb29d71a8f28698cf08457738fc3bd641d552`
- `tests/fixtures/providers/luna_capabilities.py` — `7ccde687d3c60d06fb5cf732b1a31a40219925eaddea5ff0dff58163405611d7`
- `src/aiscc/runtime/child_environment.py` — `1f1a58a953d4c4409b96a039031890e8c78b8b33986026720ea3465c97c9d5a1`
- `src/aiscc/providers/hosted_secret.py` — `e57fd0d43b9cab748b542fe2fab9b6340e99742835be9a7268bbf025870cb2a8`
- `tests/unit/providers/test_hosted_secret.py` — `ee48943233ef9cd888f3d5bc689372a99fc2063f80df7a517f12b4448e7d0145`
- `config/deployment/public-live-railway.v1.toml` — `090eda293a555afc03635854189e48e889b815ef557bd67276c7c1dcd0c9d063`
- `tests/integration/providers/test_hosted_secret_durable.py` — `d391e631979a25216209781878dd6a55ef1af716ff868df1de49e1ccc3a01347`

Before mutation verify all 12 paths against the retained 1419 `SOURCE_INVENTORY.json`.

If mismatch/collision exists: STOP.

Do not broadly clean unrelated cache/runtime residue.

## Phase A — exact source audit before mutation

Inspect exact current:

- `src/aiscc/security/policy.py`
- Public Live provider/resource authority owner(s), including `src/aiscc/public_live/provider_authority.py` if present
- `AgentExecutionService._provider_capabilities`
- durable tool context capability path
- current `LunaScopeAuthority` / stockroom authority
- `SecurityPolicy._scope_is_policy_owned`
- related unit/integration tests.

Write first:

`PUBLIC_LIVE_CONTEXT_RESOURCE_AUTHORITY_DESIGN.md`

The design must identify:

1. why current REPOSITORY/SCENARIO grants fail;
2. exact canonical owner chosen;
3. exact allow tuple;
4. negative matrix;
5. compatibility with P1-2/P1-3 baseline;
6. why this is not a generic permission expansion;
7. provider and tool path composition;
8. state/version/concurrency binding;
9. no public-selected resource identity.

If source audit shows a broader Human-accepted security policy amendment is actually required rather than an implementation compatibility repair:

`POLICY_CONFLICT_INVESTIGATION_REQUIRED`

and STOP before mutation.

## Phase B — exact Public Live context authority

Implement the narrowest safe production owner for Public Live context resources.

Preferred conceptual interface:

`PublicLiveContextResourceAuthority`

Actual naming may reuse an existing owner.

### only admissible resource domains

```text
REPOSITORY
SCENARIO
```

### only admissible mode

`PUBLIC_BOUNDED_LIVE`

### only admissible action

`RUN_EXECUTION_SIDE_EFFECT`

### required exact bindings

Authority must validate at least:

- principal/system execution context according to existing P1-3 convention;
- exact work_run_id;
- exact execution_attempt_id when available in the owner context;
- current `RUNNING`;
- exact current `state_version`;
- exact provider profile id/version;
- exact scenario id/version;
- exact operation fingerprint/context when current policy carries it;
- repository resource equals server-owned `profile.public_repository_resource_identity`;
- scenario resource equals server-owned `profile.public_scenario_resource_identity`.

Use existing canonical typed identity properties.

Do not compare on display labels or loose prefixes.

### server-owned only

The public request may select only the already accepted bounded scenario identifier through existing admission.

It cannot supply:

- repository resource identity;
- repository URL/path/version;
- scenario resource identity/version;
- profile;
- capability owner;
- resource grant.

Those values must derive from the immutable server profile/scenario authority.

## SecurityPolicy integration

Prefer explicit separation.

Conceptually:

```text
provider_tool_policy → PROVIDER/TOOL
secret_use_policy    → SECRET
stockroom/tool scope → PROCESS and existing exact tool resources
public context policy → REPOSITORY/SCENARIO for Public Live only
```

A new optional SecurityPolicy dependency is permitted if it is the narrowest clean design.

Requirements if a new dependency is added:

- default `None`;
- absent => current deny behavior;
- no OWNER/REPLAY widening;
- no implicit wildcard;
- no alteration of action-state matrix;
- exact unit tests.

If exact existing authority can be reused instead, prove it is already narrow enough.

Do NOT simply allow every `stockroom_policy` to own REPOSITORY/SCENARIO unless its interface is strengthened to the same exact immutable binding and regression proves no broader caller can obtain those grants.

## both provider and tool context

Public Live provider execution already requests REPOSITORY/SCENARIO context capabilities.

The Public Live tool execution path also requests them.

The compatibility owner must be the same semantic authority for both paths.

Do not make provider and tool context-resource truth diverge.

## required negative tests

At minimum deny:

1. wrong repository identity;
2. owner/private repository identity;
3. wrong repository version;
4. wrong scenario identity;
5. wrong scenario version;
6. another profile id;
7. another profile version;
8. OWNER runtime;
9. REPLAY runtime;
10. stale state_version;
11. non-RUNNING state;
12. wrong run/attempt/context;
13. wrong action class;
14. missing public-context authority;
15. user/caller supplied alternate resource id;
16. prefix/display-name lookalike.

Also prove exact accepted profile/scenario passes.

## Phase C — resume hosted secret ordering proof

After exact capabilities pass, retain the accepted 1419 order:

```text
fresh authority
→ PROVIDER + SECRET + REPOSITORY + SCENARIO admission
→ SecretResolutionLease
→ hosted secret resolution
→ provider/round/budget reservation
→ final freshness
→ DISPATCH_STARTED
→ provider adapter
```

### missing / blank secret

Actual durable `AgentExecutionService.execute()` must produce:

```text
provider SDK/client:
0

provider network:
0

provider reservation:
0

round reservation:
0

provider budget reservation:
0

operation:
OUTCOME_KNOWN / CANCELLED

sanitized reason:
LIVE_UNAVAILABLE

OUTCOME_UNKNOWN:
NO

retry:
NO
```

No fake dispatch marker.

### successful fake secret

Proceed through exact context capabilities, lease, reservation, final freshness and fake SDK.

### post-dispatch uncertainty

Must remain:

`TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME`

with no blind retry.

### restart/crash

Retain cases from 1419 Task:

- crash after secret resolution before reservation;
- restart/recovery before reservation;
- reservation then final freshness failure;
- post-dispatch uncertainty.

## PostgreSQL runtime

Explicitly authorized:

```text
postgres:17.6
cached image only
network pull forbidden
task-owned container/volume
preferred bind 127.0.0.1:55432
private DB reuse forbidden
```

Emit `LOCAL_POSTGRES_RUNTIME.json`.

## DB secret non-exposure

Use synthetic sentinel only.

Execute positive fake hosted flow.

Scan relevant durable provider/execution/public-live text/JSON/protocol/provenance columns.

Required:

`exact synthetic secret occurrences = 0`

No real key.

## actual sandbox/container secret non-exposure

Use existing accepted cached P1-3 sandbox image/product path.

No pull.

Parent trusted environment:

```text
AISCC_OPENAI_API_KEY=<sentinel A>
OPENAI_API_KEY=<sentinel B>
```

Inside actual product-created child/container both must be absent.

Also retain child/Git/Docker environment tests.

## build exposure audit

Re-run after final source changes.

No:

- `RUN env`;
- `printenv`;
- broad environment dumps;
- `.env` copy;
- secret logging;
- secret serialization.

Railway sealed variables remain build-visible; do not claim otherwise.

## full regression — mandatory

Prior accepted baseline:

`1423 PASS / 3 existing Windows symlink-host SKIP / 0 FAIL / 0 ERROR`

Run complete repository suite after all source changes.

Require:

- 0 FAIL;
- 0 ERROR;
- same existing 3 skips only;
- no new xfail;
- no removed/disabled assertions;
- pass count not reduced through dilution.

Also run:

- new public context authority unit tests;
- durable hosted-secret integration;
- P1-3 security policy/runtime tests;
- P1-5 provider persistence/runtime tests;
- Public Live provider/tool tests;
- Ruff;
- format check;
- mypy;
- `git diff --check`.

## secret scan

No real credential-like key may appear in changed source/governance/export.

If detected, STOP and identify path + detector class only.

Synthetic sentinels are permitted when clearly fake/test-only.

## real external actions — forbidden

```text
real OpenAI calls:
0

real credential read/use:
0

Railway mutation:
0

Railway deploy:
0

Cloudflare mutation:
0

Public enable:
0

Git commit/push:
0
```

## source scope

The 12 retained candidate paths may be modified.

Additional narrowly authorized compatibility paths may include:

- `src/aiscc/security/policy.py`;
- exact Public Live resource-authority implementation file(s);
- directly affected tests.

Before editing any additional path, record it in `PUBLIC_LIVE_CONTEXT_RESOURCE_AUTHORITY_DESIGN.md` with why it is the canonical owner.

No unrelated security refactor.

## acceptable final outcome

If all local implementation/proof passes:

`HUMAN_RAILWAY_DEPLOYMENT_REQUIRED / LOCAL_ACCEPTED_CANDIDATE`

Do NOT claim terminal L5 acceptance.

## mandatory stop

- HEAD mismatch;
- retained 12-path identity mismatch;
- fix requires broad P1-2/P1-3 policy weakening;
- generic repository/scenario wildcard is required;
- exact resource owner cannot bind server profile/scenario safely;
- PostgreSQL unavailable;
- cached sandbox unavailable;
- sentinel leaks;
- full regression fails;
- real credential required.

## export

Target:

`.aiassistant/reports/target/20260916_1430_aiscc-p3-3-public-live-l5-public-context-resource-capability-and-secret-proof-retry-1/`

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `SOURCE_INVENTORY.json`
- `PUBLIC_LIVE_CONTEXT_RESOURCE_AUTHORITY_DESIGN.md`
- `PUBLIC_CONTEXT_CAPABILITY_EVIDENCE.md`
- `LOCAL_POSTGRES_RUNTIME.json`
- `PREDISPATCH_SECRET_ORDERING_EVIDENCE.md`
- `DURABLE_MISSING_SECRET_EVIDENCE.md`
- `SECRET_DB_NON_EXPOSURE_EVIDENCE.md`
- `LOCAL_SANDBOX_SECRET_NON_EXPOSURE_EVIDENCE.md`
- `TEST_EVIDENCE.json`
- retained L5 secret/rotation/canary/build documents
- workspace before/after

## final response

1. result
2. target bundle
3. exact compatibility owner/design
4. allow/deny capability matrix
5. source/config/test inventory
6. durable missing/blank result
7. positive fake-secret path
8. post-dispatch unknown regression
9. restart/crash evidence
10. PostgreSQL runtime
11. DB secret non-exposure
12. actual sandbox non-exposure
13. child/Git/Docker proof
14. build audit
15. focused tests
16. full regression
17. static/type/diff
18. secret scan
19. external actions
20. Public state
21. workspace integrity
22. Human Railway pending evidence
