# AISCC Browser Command Center Handoff — L5 Public Live context-resource capability retry

## repository

```text
HEAD:
04436a11adc6dd6e70b4a98568fe878cc4c9f4aa
```

## current candidate

12 uncommitted source/config/test paths from 1419 remain the working candidate.

Do not revert them.

## blocker

```text
actual durable path
→ P1_3_SECURITY_DENIED:REPOSITORY:EXACT_RESOURCE_GRANT_DENIED
```

The missing authority is for exact Public Live:

```text
REPOSITORY:
profile.public_repository_resource_identity

SCENARIO:
profile.public_scenario_resource_identity
```

## security invariant

These capabilities are required, not optional.

The fix is a narrow production authority, not removal of the guard.

## preferred exact owner

Use a separate Public Live context-resource policy/authority unless the existing source already contains an equivalent exact server-owned owner.

It must bind:

- PUBLIC_BOUNDED_LIVE;
- RUN_EXECUTION_SIDE_EFFECT;
- RUNNING/current version;
- exact run/attempt;
- exact profile/version;
- exact scenario/version;
- exact repository/scenario resource identities.

## after compatibility PASS

Resume:

- pre-dispatch missing/blank secret;
- positive fake secret;
- crash/restart;
- post-dispatch uncertainty;
- PostgreSQL DB secret scan;
- actual sandbox env scan;
- full suite.

No external actions.
