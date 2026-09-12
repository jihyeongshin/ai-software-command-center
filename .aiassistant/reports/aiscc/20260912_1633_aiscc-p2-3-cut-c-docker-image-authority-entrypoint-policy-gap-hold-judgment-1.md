# AISCC Command Center Judgment

## meta

- judgment_id: `20260912_1633_aiscc-p2-3-cut-c-docker-image-authority-entrypoint-policy-gap-hold-judgment-1`
- created_at: `2026-09-12T16:33:35+09:00`
- project: `AI Software Command Center (AISCC)`
- reviewed_task: `20260912_1622_aiscc-p2-3-private-s1-cut-c-postgres-projection-contract-retry-1`
- reviewed_result_zip_sha256: `9e272abfe93cb2c0c3f8bc4dcda695f13f7305528427f4b5e3ceba22ae84c9be`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause: `COMMAND_CENTER_DOCKER_OBSERVATION_AUTHORITY_CONFLICT`
- cycle_record_action: `create`
- execution_mode: `MANUAL_COMMAND_CENTER`
- source_mirror_sync: `not-required`

# 판정

1622 Executor의 `POLICY_CONFLICT_INVESTIGATION_REQUIRED / STOP_WITH_REPORT_EXPORT`를 정당한 fail-closed STOP으로 입장한다.

검증된 제출:

```text
ZIP:
12 members / one top-level / CRC PASS

manifest:
11 / 11 SHA/size exact

TASK.md == canonical done Task:
PASS

contract:
13 PASS / 20 BLOCKED_REQUIRED_EVIDENCE

HEAD:
6d41633210f0e556dd4292ee62a8600c6b54215f

index/tracked:
empty / clean

Docker/private file/runtime root/DB/application:
NOT_EXECUTED

S1-S4:
NOT_EXECUTED
```

# exact blocker

1622 Task section 7은 PostgreSQL projection에 다음 live evidence를 요구했다.

```text
image_id = PostgreSQL image inspect .Id
image_repodigest = PostgreSQL image inspect RepoDigests의 exact required digest
```

그러나 section 8의 exclusive read-only Docker allowlist에는 다음만 있었다.

```text
Stockroom image inspect
PostgreSQL container inspect
PostgreSQL volume inspect
```

PostgreSQL image inspect가 빠져 있었다.

Executor가 container Config.Image 또는 expected projection object를 live image evidence로 대체하지 않은 것이 맞다.

# additional Browser preflight correction

Browser가 Cut A accepted source를 다시 확인했다.

Canonical public production entrypoint:

```python
aiscc.bootstrap.build_stockroom_production(...)
```

이 wrapper가 current production owner graph construction의 public authority boundary다.
내부 `build_stockroom_production_application(...)`은 wrapper가 위임하는 implementation 함수다.

1622 retry가 내부 builder direct call로 wording을 바꾼 것은 불필요한 authority drift다.
후속 Task는 public wrapper를 exactly once 호출하도록 복원한다.

# preserved authority

```text
Cut B:
FINAL_ADMITTED / PERSISTED

1533 current state:
RECONCILED

1605/1622:
blocked provenance only

environment mutation in 1605/1622:
none

private runtime root:
not created

private S1:
NOT_AUTHORIZED
```

후속 Task는 corrected Docker observation allowlist와 public production entrypoint를 사용한 Cut C retry만 허가한다.
