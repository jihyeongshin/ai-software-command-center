# AISCC Command Center Judgment

## meta

- judgment_id: `20260913_2308_aiscc-p2-3-stockroom-evidence-v2-source-acceptance-and-private-s1-v5-authorization-1`
- created_at: `2026-09-13T23:08:24+09:00`
- project: `AI Software Command Center (AISCC)`
- reviewed_result_zip_sha256: `b6629237ace8eaa995ee399a7a6df343e59fe72fcd22e054d662b9c3a83bd18e`
- base_HEAD: `15c9e975ec193526eafa0749fc97321c4d89d713`
- result_status: `ACCEPTED / STOCKROOM_EVIDENCE_V2_CUTOVER_SOURCE_CANDIDATE`
- source_persistence_authorized: `Yes`
- fresh_private_S1_authorized: `Yes / after exact persistence only`

## 2225 source-candidate acceptance

Independent Browser verification:

```text
ZIP CRC:
PASS

members:
22

manifest rows:
21 / all SHA+size exact

TASK.md == canonical done Task:
PASS

contract:
45 / 45 PASS
```

Accepted candidate:

```text
v1 evidence config:
byte-preserved / known legacy offset-sensitive

v2 evidence config:
new prospective authority

durable identities:
v1/v2 disjoint

v2 timestamps:
UTC-stable

v2 row round-trip:
PASS / RequirementSet + Requirement + Checkpoint / S1-S4

v2 historical resolver:
PASS

v1/v2 coexistence/idempotency:
PASS

local fake S1:
READY→RUNNING→ADMISSION_PENDING→ACCEPTED

Human/Judgment guards:
owner-backed and present
```

This acceptance does not claim generic P1-6 legacy compatibility is fixed.

## next authority

Persist the exact candidate and accumulated governance first.

Only after that exact commit is verified may one new private S1 run execute using fresh v5 root/run/attempt identities and the persisted Stockroom v2 authority.
