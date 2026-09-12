# AISCC Command Center Judgment

## meta

- judgment_id: `20260912_1954_aiscc-p2-3-private-s1-acl-query-transport-blocker-hold-judgment-1`
- created_at: `2026-09-12T19:54:18+09:00`
- project: `AI Software Command Center (AISCC)`
- reviewed_task: `20260912_1749_aiscc-p2-3-private-s1-normal-scenario-execution-and-capture-1`
- reviewed_result_zip_sha256: `5171f5e967cafdcfc2dc1eb749c1470619c7609add0d0c77ca357525c4faab59`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause: `PRIVATE_ACL_QUERY_TRANSPORT_DECODE_FAILURE`
- cycle_record_action: `create`
- execution_mode: `MANUAL_COMMAND_CENTER`
- source_mirror_sync: `not-required`

# Browser judgment

1749 Executor의 blocker STOP을 정당한 fail-closed 결과로 입장한다.

실제 result ZIP 검증:

```text
members:
21 / 21

one top-level:
PASS

CRC:
PASS

manifest:
20 / 20 SHA-256 + byte size exact

TASK.md == canonical done Task:
PASS

issued Task/Cycle/Judgment:
byte exact

contract:
12 PASS / 25 BLOCKED_REQUIRED_EVIDENCE
```

실행된 범위:

```text
repository/state/source/provenance:
PASS

retained Docker identities:
PASS

secret bind selection:
PASS

Docker Desktop source representation normalization:
PASS

StockroomCaptureRunner.run(prepared):
UNAMBIGUOUS / source-owned full-run entrypoint

password read:
0

DB connection:
0

public builder:
0

prepare_capture:
0

runner invocation:
0

WorkRun/attempt creation:
0

S1/S2/S3/S4:
NOT_EXECUTED
```

# blocker

1749 helper invoked Windows PowerShell ACL capture with:

```text
powershell.exe -NoProfile -NonInteractive -Command -
stdin = UTF-8 encoded multi-line PowerShell script
stdout = decoded directly as utf-8-sig JSON
```

The PowerShell process returned exit code 0 but captured stdout could not be decoded as a valid JSON document.
The raw ACL stdout was not retained.

This is an ACL query **transport/serialization blocker**, not evidence that the private ACL itself is invalid.

Executor correctly did not retry after this blocker because 1749 Task section 21 required a new Browser Task before retry.

# corrected authority

The successor Task keeps the same ACL policy and the same S1 run/attempt identity.

Only the ACL child-process transport is corrected:

```text
PowerShell script:
UTF-16LE Base64 via -EncodedCommand

private path payload:
UTF-8 JSON via stdin only
never argv

child InputEncoding:
UTF-8 no BOM

child OutputEncoding:
UTF-8 no BOM

stdout:
exactly one JSON document via [Console]::Out.Write

stderr:
empty

shell:
false
```

No ACL mutation is authorized.

# initial Python bootstrap incident

The initial WindowsApps Python alias failure was reported before archive verification.
Human then explicitly authorized locating the actual Python executable and continuing.
The actual package bootstrap subsequently passed before substantive runtime access.

This operational recovery does not substitute for runtime evidence and is not the 1749 blocker.

# preserved state

```text
Cut C:
FINAL_ADMITTED / PERSISTED

private S1:
ENTRY_READY / execution still NOT_STARTED

run_id:
aiscc-p2-3-private-s1-normal-v1-run
no durable row created by 1749

attempt_id:
aiscc-p2-3-private-s1-normal-v1-attempt-1
no durable row created by 1749

P2-3:
IN_PROGRESS
```
