# AISCC Browser Command Center Judgment

## 판정

```text
result_status:
PARTIAL_ACCEPTED

work_type:
REWORK

reject_cause:
none

cycle_record_action:
create

source_mirror_sync:
not-required
```

## accepted scope

Command Center baseline regression repair의 substantive 결과를 ACCEPT한다.

Accepted evidence:

```text
PostgreSQL:
17.6 / local-cache / no pull
127.0.0.1:55432
private_db_reused=false
runtime evidence PASS

fresh reproduction before mutation:
3 FAIL / 0 ERROR / 0 SKIP
all exact shared ValueError

targeted after repair:
3 PASS / 0 FAIL / 0 ERROR

full suite:
1220 PASS
3 SKIP
0 FAIL
0 ERROR

predecessor node coverage:
1203 / 1203
missing = 0

additional current nodes:
20 PASS

guard source:
unchanged

tracked source diff:
tests/integration/command_center/test_postgres_read_api.py only

assertion AST:
53 / 53 unchanged

skip/xfail:
no new entries

cleanup:
task-owned PostgreSQL container/volume removed
```

## root cause judgment

Accepted root cause:

`G_EXECUTOR_SUBMISSION` production authority가 잘못된 것이 아니라 Command Center test fixture가 과거 generic `P1_4GuardAuthority.issue(...)` construction을 사용하고 있었다.

Accepted repair:

```text
synthetic producer-owned ExecutionSubmissionRef
→ ExecutionReferenceAuthority.register_submission(...)
→ P1_4GuardAuthority.issue_from_execution_ref(...)
→ real issuer verification
```

Production/runtime source와 issuer-verification guard는 변경되지 않았다.

## full-suite collection judgment

성공한 full-suite command가 predecessor command와 byte-identical하지 않은 점은 확인했다.

그러나 다음 evidence 때문에 proof narrowing으로 보지 않는다.

- predecessor 1,203 node 전부 포함
- missing predecessor nodes = 0
- 추가 20 node도 PASS
- 기존 3 skip identity/message 동일
- test exclusion 없음
- collection 문제를 해결하기 위한 source change 없음

따라서 `FULL_SUITE = EXECUTED_PASS`를 admit한다.

## remaining gap

Substantive repair는 accepted됐지만 source와 governance provenance가 아직 Git commit으로 고정되지 않았다.

따라서 현재 결과는:

```text
BASELINE_GREEN_RESTORED:
ACCEPTED

PUBLIC_PROVENANCE:
PENDING_GIT_PERSISTENCE

L2:
NOT_STARTED / ENTRY_ELIGIBLE
```

L2 implementation은 persistence 완료 전 시작하지 않는다.

## next action

`20260915_2250_aiscc-command-center-baseline-regression-repair-git-persistence-1`

Exact accepted source/governance allowlist만 stage/commit하고 resulting commit을 Browser Command Center에 제출한다.
