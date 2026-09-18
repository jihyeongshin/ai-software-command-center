# Executor Report

## Result

`RELEASE_ROLLED_BACK_TO_REPLAY_ONLY`

The authorized release sequence reached final backend enablement and created exactly one public smoke run. The run returned `201 ADMITTED`, but it remained `ADMITTED` beyond its 90-second deadline. The executor made no second run and performed the authorized rollback.

## Material finding

The initializer completed the durable start path through `BOUND`. The worker acquired one claim, but no canonical provider operation was created. The claim was never renewed, expired after 15 seconds, and was recovered with `LIVE_UNAVAILABLE`.

Durable post-failure facts:

- public runs: 1
- start requests: 1, phase `BOUND`
- worker claims: 1, released `LIVE_UNAVAILABLE`
- operation bound: false
- execution operations: 0
- operation events: 0
- public dispatch rows: 0
- provider request rows: 0
- real provider sends attributable to this smoke: 0
- unknown provider/send outcome: no

This localizes the release failure to the production worker's pre-dispatch execution path. The worker loop intentionally swallows claim-execution exceptions, and hosted logs contain no exception detail, so a narrower exception class cannot be asserted from retained evidence.

## Persistence

- release frontend commit: `918f5e8ad62038b967c982ef5aa860d1785f5742`
- rollback frontend commit: `57c20374c2c2799aa354c43309b1515a3d13fe3f`
- both commits were ordinary fast-forward pushes to `origin/main`

## Tests

- frontend/build and hosted-binding unit selection: `15 passed`
- Live UI Node contract: PASS
- Replay UI Node contract: PASS
- deterministic Replay build/check: PASS
- corpus root unchanged: `a870da635941d7149edbbef911e8b2d75ff6fe12e8ade80c09dddc9086df795e`
- Ruff and Git diff checks: PASS
- the PostgreSQL integration test selected during release preparation reported one setup error because `AISCC_TEST_DATABASE_URL` was absent; it was not pointed at hosted production. Its 15 non-PostgreSQL tests passed.

## Final safety state

- public admission: disabled
- public Live: not released
- public ingress domains: 0
- Railway edge trust: absent
- Cloudflare frontend: Replay-only
- Replay scenarios: 4 and unchanged
- task-owned SSH keys/tunnel: removed
