# AISCC Command Center Judgment

## meta

- judgment_id: `20260913_1737_aiscc-p2-3-private-s1-workspace-byte-gate-command-center-defect-judgment-1`
- created_at: `2026-09-13T17:37:44+09:00`
- project: `AI Software Command Center (AISCC)`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause: `COMMAND_CENTER_WORKSPACE_BYTE_GATE_DEFECT`
- predecessor_result_zip_sha256: `b43bc0f17eb60e9c7321af5c8f1e23cf1dd65d57f5ba18cb777957d5e6fd8d0d`
- current_HEAD: `d04f6a322f3a3ea49778314e4005b5878b20f121`

## judgment

The 1707 Executor STOP is accepted as correct fail-closed behavior.

Browser/Command Center defect:

```text
1435 reported:
bounded bytes = 2320

1707 independently observed:
actual file bytes = 26727

1435 fingerprint:
18433a8d92affe915d01e3bb1265b387a07dc6478e09c92306854908ab396068

1707 fingerprint:
18433a8d92affe915d01e3bb1265b387a07dc6478e09c92306854908ab396068
```

The persisted source-owned restart inventory fingerprint includes each file's byte length and SHA-256 in the fingerprint payload. Therefore the exact matching fingerprint is the authoritative content-identity predicate. The 1707 Task incorrectly promoted the historical `2320` report field into an exact content-byte mutation gate.

Correction:

```text
remove exact 2320 byte-total gate
do not replace it with an exact 26727 total-byte gate
use source-owned RestartWorkspaceInspection identity/fingerprint
plus exact object/file count and safe-inventory checks
```

No private runtime mutation occurred in 1707. The retained subject remains eligible for one corrected dedicated-builder retry.
