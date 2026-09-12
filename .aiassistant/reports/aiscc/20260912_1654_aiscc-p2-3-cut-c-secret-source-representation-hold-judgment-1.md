# AISCC Command Center Judgment

## meta

- judgment_id: `20260912_1654_aiscc-p2-3-cut-c-secret-source-representation-hold-judgment-1`
- created_at: `2026-09-12T16:54:45+09:00`
- project: `AI Software Command Center (AISCC)`
- reviewed_task: `20260912_1633_aiscc-p2-3-private-s1-cut-c-docker-image-authority-and-public-entrypoint-retry-1`
- reviewed_result_zip_sha256: `4d51bcca975ed84661b1a52e0ba413ffdab825ee820b0cbf8e97986e5422420e`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause: `COMMAND_CENTER_DOCKER_DESKTOP_SECRET_SOURCE_REPRESENTATION_GAP`
- cycle_record_action: `create`
- execution_mode: `MANUAL_COMMAND_CENTER`
- source_mirror_sync: `not-required`

# 판정

1633 Executor의 `BLOCKED / PRIVATE_SOURCE_NOT_ABSOLUTE`는 정당한 fail-closed STOP이다.

Browser 검증:

```text
result ZIP:
16 members / one top-level / CRC PASS

manifest:
15 / 15 non-self hash/size exact

TASK root == canonical done Task:
PASS

contract:
22 / 35 PASS

Docker observations:
exact four-resource allowlist reached

PostgreSQL canonical projection:
867e744367eb804c30db6269d0700d8679c5aeb1a9b6fb78306ce1b87918c8e7 PASS

POSTGRES_SANITIZED_INSPECT.json:
e50fea1be09dd8e2ea44a217c36c08751c94de0d873bb136ef41b2235f9c4b25 PASS

typed Stockroom image resolver:
PASS

public build calls:
0

DB connection:
not reached

private runtime root:
not created

S1-S4:
NOT_EXECUTED

repository/Git mutation:
none
```

# blocker

The exact container bind was located and sanitized projection succeeded.

The failing implementation then did:

```python
password_path = Path(secret_mount["Source"])
require(password_path.is_absolute(), "PRIVATE_SOURCE_NOT_ABSOLUTE")
```

Docker Desktop may represent a native Windows bind source through its Linux daemon namespace.
Such a source is not necessarily a Windows-absolute `Path` string even though it refers to the retained native-host file.

The Task did not define an authorized reversible representation conversion.
Executor correctly refused to guess.

# privacy result

The raw mount Source was not exported.
The helper added the observed private source bytes to the exact-value export scan before the failing check.
No password value was acquired.

# required retry correction

The successor Task may normalize only these exact source representation classes:

```text
WINDOWS_NATIVE_ABSOLUTE

DOCKER_DESKTOP_RUN_DESKTOP_MNT_HOST
/run/desktop/mnt/host/<drive-letter>/<segments>

DOCKER_DESKTOP_HOST_MNT
/host_mnt/<drive-letter>/<segments>
```

For the two Docker Desktop classes the conversion must be reversible and exact.
No broad filesystem discovery or alternative-path search is authorized.

Only the normalized native-host path may be used for ACL/file/runtime-root authority.

# preserved state

```text
Cut B:
FINAL_ADMITTED / PERSISTED

Cut C:
IN_PROGRESS / readiness not admitted

1605/1622/1633:
blocked provenance

private runtime root:
NOT_CREATED

public production build:
NOT_CALLED

DB authority rows:
NOT_CREATED

private S1:
NOT_AUTHORIZED
```
