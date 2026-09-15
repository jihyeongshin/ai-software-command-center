# AISCC Browser Command Center Handoff — baseline repair acceptance → Git persistence

## 목적

Command Center integration baseline의 알려진 3 FAIL debt가 수정되었고 substantive evidence가 Browser Command Center에서 accepted되었다.

다음 단계는 **Git persistence only**다.

## current state

```text
HEAD before persistence:
3709c88fc0abd2f4219228ced931a9164f286dc4

baseline repair:
SUBSTANTIVE ACCEPTED

full suite:
1220 PASS / 3 SKIP / 0 FAIL / 0 ERROR

public provenance:
PENDING_GIT_PERSISTENCE

L2:
NOT_STARTED / ENTRY_ELIGIBLE

Public Live:
NOT_RELEASED

Public admission:
DISABLED
```

## accepted source change

Exactly one tracked test source:

`tests/integration/command_center/test_postgres_read_api.py`

Purpose:

stale generic `G_EXECUTOR_SUBMISSION` fixture issuance를 current issuer-verified execution-ref path로 정렬.

Not changed:

- production/runtime source
- workflow guard implementation
- migration/config
- assertions
- skip/xfail

## accepted evidence

- fresh exact-three reproduction before mutation: 3 FAIL, accepted shared error
- exact-three after repair: 3 PASS
- current full suite: 1220 PASS / 3 SKIP / 0 FAIL / 0 ERROR
- all 1,203 predecessor nodes covered; zero missing
- 20 additional current nodes PASS
- guard source blob unchanged
- PostgreSQL 17.6 isolated runtime and cleanup PASS

## persistence boundary

The next Task must commit only the exact accepted source/provenance allowlist.

Do not:

- modify source,
- rerun broad tests merely to fill report fields,
- stage unrelated untracked files,
- push,
- deploy,
- start L2.

After commit, Browser Command Center will verify commit contents and then decide terminal baseline closure + L2 entry Task.
