# AISCC Cycle Record

## meta

- cycle_id: `20260916_1430_aiscc-p3-3-l5-public-context-resource-capability-gap-retry-entry-1`
- date: `2026-09-16 KST`
- primary_semantic_owner: `Browser Command Center`
- affected_areas: `P3-3 Public Live L5 / P1-3 exact public repository+scenario capability composition / hosted secret proof`
- work_type: `REWORK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- predecessor_task: `.aiassistant/tasks/done/20260916_1419_aiscc-p3-3-public-live-l5-predispatch-secret-resolution-and-proof-completion-retry-1.md`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause: `SECURITY_CAPABILITY_COMPATIBILITY_REQUIRED`
- executor_fault: `NO`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260916_1430_aiscc-p3-3-l5-public-context-resource-capability-gap-retry-entry-1.cycle.md`

## result integrity

Executor result ZIP SHA-256:

`2cda133108ccf88091a70a8ae6b61d8cabbe2919dec9cccd4a92307e8fa1dd6d`

Adjacent sidecar matched exactly.

Repository:

```text
HEAD:
04436a11adc6dd6e70b4a98568fe878cc4c9f4aa

index:
EMPTY

commit/push:
NONE

real provider calls:
0

Railway/Cloudflare mutations:
0

Public admission:
DISABLED

Public Live:
NOT_RELEASED
```

## predecessor candidate integrity

The 1419 turn preserved the existing L5 candidate and added one integration test.

Current uncommitted source/config/test candidate:

```text
12 paths
```

Exact inventory:

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

No source rollback is authorized.

## actual blocker

The pre-dispatch secret-ordering change could not be proven because the authoritative durable Public Live path fails before secret resolution:

```text
P1_3_SECURITY_DENIED:
REPOSITORY:
EXACT_RESOURCE_GRANT_DENIED
```

Current durable provider execution correctly requires:

- PROVIDER capability;
- SECRET capability;
- fixed synthetic REPOSITORY capability;
- exact SCENARIO capability.

However the current `SecurityPolicy` production ownership mapping only has exact selector ownership for PROVIDER/SECRET and scenario tool/process ownership for the existing stockroom authority. It does not provide a production owner for the hosted profile's REPOSITORY/SCENARIO resource scopes.

The integration-test local `FixedScope` cannot substitute for the production ownership contract because `_scope_is_policy_owned` never delegates these domains to it.

## baseline interpretation

This is NOT a request to weaken the security baseline.

Accepted Public Live security already requires:

```text
fixed synthetic repository only
allowlisted scenario only
server-fixed provider/model
exact scenario/resource capability
deny-by-default
```

Therefore the missing REPOSITORY/SCENARIO authority is an implementation compatibility gap.

No Human policy re-decision is required if the fix remains exact, server-owned and deny-by-default.

## authorized compatibility direction

Introduce or designate one narrow production authority for Public Live context resources.

Conceptual owner:

`PublicLiveContextResourceAuthority`

The actual canonical name/location may reuse an existing exact authority if source audit proves it owns the same semantics.

It may authorize ONLY:

```text
RuntimeMode:
PUBLIC_BOUNDED_LIVE

action:
RUN_EXECUTION_SIDE_EFFECT

resource domains:
REPOSITORY
SCENARIO

repository identity:
exact ProviderProfile.public_repository_resource_identity

scenario identity:
exact ProviderProfile.public_scenario_resource_identity

profile:
exact server-owned profile id/version

scenario:
exact server-owned scenario id/version

run/attempt:
exact current run authority

state:
RUNNING / fresh state_version

operation:
exact current operation fingerprint/context
```

No wildcard resource IDs.

No arbitrary URL/repository path.

No user/public selector.

No owner/private repository.

No alternate scenario.

No prefix/display-name matching.

## SecurityPolicy integration

Preferred architecture:

- keep PROVIDER ownership under `ProviderToolResourceAuthority`;
- keep SECRET ownership under `SecretUseAuthority`;
- keep process/tool ownership under existing stockroom/Luna authority;
- add a distinct optional exact Public Live context-resource owner for REPOSITORY/SCENARIO.

Default when that owner is absent:

`DENY`

If current source already has an equivalent accepted authority, wire it rather than creating a duplicate abstraction.

Do not generically reinterpret every `stockroom_policy` as repository/scenario owner unless source audit proves its production contract binds the exact fixed resource identities and cannot broaden other modes/profiles.

## proof requirement

The new owner must make the exact hosted Luna durable path admissible while preserving deny cases for:

- wrong repository identity;
- wrong repository version;
- wrong scenario identity/version;
- wrong profile/version;
- wrong runtime mode;
- stale state/version;
- wrong run/attempt;
- wrong action class;
- absent context-resource authority;
- public/user-selected resource identity.

## retained secret-ordering authority

After context capabilities are admitted, retain the 1419 ordering:

```text
authority freshness
→ PROVIDER + SECRET + REPOSITORY + SCENARIO capability admission
→ single-use SecretResolutionLease
→ hosted secret resolution
→ provider/round/budget reservation
→ final freshness
→ DISPATCH_STARTED
→ provider adapter
```

Missing/blank secret remains pre-dispatch:

```text
OUTCOME_KNOWN / CANCELLED
reason = LIVE_UNAVAILABLE

provider send = 0
provider reservation = 0
round reservation = 0
budget reservation = 0
OUTCOME_UNKNOWN = NO
retry = NO
```

Post-dispatch uncertainty remains unchanged.

## evidence still required

1419 stopped at the first focused capability failure.

Still mandatory:

- full durable missing/blank/positive/crash/freshness/uncertain matrix;
- task-owned PostgreSQL DB sentinel non-exposure;
- actual local sandbox/container sentinel non-exposure;
- child/Git/Docker environment proof;
- build-exposure audit;
- complete repository regression;
- Ruff/format/mypy/diff;
- source secret scan.

Human Railway deployment remains NOT_YET_AUTHORIZED.
