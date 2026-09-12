# AISCC Command Center Judgment

## meta

- judgment_id: `20260912_1622_aiscc-p2-3-cut-c-postgres-projection-policy-gap-hold-judgment-1`
- created_at: `2026-09-12T16:22:20+09:00`
- project: `AI Software Command Center (AISCC)`
- reviewed_task: `20260912_1605_aiscc-p2-3-private-s1-cut-c-final-readiness-binding-1`
- reviewed_result_zip_sha256: `eb7ab43e856ef20aae92deabbedbe5bdd69b5d22504ef1fac6bced105d92844d`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause: `COMMAND_CENTER_EVIDENCE_CONTRACT_INCOMPLETE`
- cycle_record_action: `create`
- execution_mode: `MANUAL_COMMAND_CENTER`
- source_mirror_sync: `not-required`

# 판정

1605 Executor의 `BLOCKED_POLICY_GAP / STOP_WITH_REPORT_EXPORT`는 정당하다.

```text
result ZIP:
12 members / one top-level / CRC PASS

manifest:
11 / 11 exact

TASK root == canonical done Task:
PASS

contract:
11 PASS / 19 BLOCKED_REQUIRED_EVIDENCE

HEAD:
6d41633210f0e556dd4292ee62a8600c6b54215f

tracked/index:
clean / empty

Docker/private file/runtime root/DB/application:
NOT_EXECUTED

S1-S4:
NOT_EXECUTED
```

성공형 18-member artifact를 만들지 않은 것은 defect가 아니다.
blocker 뒤 존재하지 않는 evidence를 생성했다고 주장하지 않은 것이 맞다.

# root cause

1605 Task는 PostgreSQL sanitized inspect fingerprint:

```text
867e744367eb804c30db6269d0700d8679c5aeb1a9b6fb78306ce1b87918c8e7
```

를 요구했지만 exact projection schema, canonical serializer, file-newline semantics를 제공하지 않았다.

Executor가 schema를 추측하거나 brute-force serialization을 하지 않고 중단한 것이 맞다.

# recovered exact contract

0420 accepted result의 `POSTGRES_SANITIZED_INSPECT.json`을 Browser가 byte-level로 재검증했다.

```text
canonical JSON object fingerprint:
867e744367eb804c30db6269d0700d8679c5aeb1a9b6fb78306ce1b87918c8e7

canonical serializer:
json.dumps(object, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
UTF-8

canonical fingerprint bytes:
no trailing newline

exported POSTGRES_SANITIZED_INSPECT.json:
canonical bytes + LF

exported whole-file SHA-256:
e50fea1be09dd8e2ea44a217c36c08751c94de0d873bb136ef41b2235f9c4b25
```

후속 Task는 exact object schema까지 포함한다.

# preserved state

```text
Cut B:
FINAL_ADMITTED / PERSISTED

Commit A/B/1533 correction:
PRESERVE

1605 environment mutation:
none

private S1:
NOT_AUTHORIZED
```

다음 작업은 corrected PostgreSQL projection contract를 가진 Cut C retry다.
