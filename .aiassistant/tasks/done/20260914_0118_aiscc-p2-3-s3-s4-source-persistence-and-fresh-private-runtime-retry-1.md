# 작업지시서: P2-3 S3/S4 source persistence and fresh private runtime retry

## meta
- created_at: `2026-09-14T01:18:00+09:00`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `33a216f29062176ad196a567a299ba30291c3f72`
- required_base_parent: `be2489515ba7799466ffdf415b47e4d3e0a79e46`
- required_base_grandparent: `c26ec9eb342d052c726c57b5df42ced70e01a757`
- accepted_0057_result_zip_sha256: `ccbe30d5c348fe80c994d759ef7c269f531863b9593856af54dbd0825c94511c`
- source_commit_authorized: `Yes / exact 13 paths`
- private_runtime_authorized: `Yes / only after exact Commit A`
- S1_S2_rerun_authorized: `No`
- S3_runner_retry_authorized: `No`
- S4_runner_retry_authorized: `No`
- canonical_state_write_authorized: `No`
- push_authorized: `No`
- success_ceiling: `PRIVATE_S3_BLOCKED_AND_S4_HUMAN_REQUIRED_RUNTIME_CANDIDATE / BROWSER_REVIEW_PENDING`

# 0. ordered authority

Strict order:

```text
A. persist the Browser-accepted combined S3/S4 source candidate and accumulated governance
B. verify Commit A exactly
C. execute fresh S3 v9 once
D. only if C proves the intended S3 BLOCKED semantic, execute fresh S4 v10 once
```

B/C/D before their predecessor is forbidden.

Do not rerun S1 or S2.

# 1. executables

Repository:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center
```

Python:

```text
<repository-root>\.venv\Scripts\python.exe
```

Use only that interpreter.

Forbidden:

```text
python
py
WindowsApps
PATH Python discovery
repository-external Python/venv discovery
```

Docker:

```text
C:\Program Files\Docker\Docker\resources\bin\docker.exe
```

Git:

```text
C:\Program Files\Git\cmd\git.exe
```

No executable discovery through PATH.

# 2. exact initial repository baseline

Require:

```text
branch main
HEAD 33a216f29062176ad196a567a299ba30291c3f72
HEAD^ be2489515ba7799466ffdf415b47e4d3e0a79e46
HEAD^^ c26ec9eb342d052c726c57b5df42ced70e01a757
index empty
```

Tracked dirt exactly two paths with final accepted candidate hashes:

- `src/aiscc/scenarios/stockroom_production.py`  `daf6ee6b9e3315ac31905d45863cb0e0edaa950b5a82e3abf76a2acf02d33596`
- `tests/integration/scenarios/test_stockroom_binding.py`  `5734566fa96fdafe9fe7b494580966e6c03f7de95b33d36cc5f71a6313189765`

Git-visible untracked exactly nine predecessor governance artifacts:

- `.aiassistant/records/aiscc/cycles/20260914_0009_aiscc-p2-3-scenario-matrix-separate-applications-entry-1.cycle.md`  `ad576d179e0893f928d0f20a31209c6a5f0ec78845ef5d2f393dd6bd1506e71e`
- `.aiassistant/reports/aiscc/20260914_0009_aiscc-p2-3-2357-single-builder-scope-conflict-retry-judgment-1.md`  `dee53f09c6b8f5771dd09e5e912541faaad803d8a84f1b796c5cd890bc3b7300`
- `.aiassistant/tasks/done/20260914_0009_aiscc-p2-3-s2-s3-s4-separate-production-applications-runtime-retry-1.md`  `3ae3533a620c49408b173c6c113fa244fe84a1950bc025c1de67ede1b9c70a68`
- `.aiassistant/records/aiscc/cycles/20260914_0039_aiscc-p2-3-s3-static-policy-serialization-rework-entry-1.cycle.md`  `64b67ec18501cc5b02b0d441d710ed8cbecb43745d53cd7cb4ab10f5b0259a60`
- `.aiassistant/reports/aiscc/20260914_0039_aiscc-p2-3-0009-s2-accepted-s3-runner-typeerror-rework-judgment-1.md`  `267e1bd3ec73f00af83c88c9a65b3bb5a707e7cc56936a3d738d370d17f6a58d`
- `.aiassistant/tasks/done/20260914_0039_aiscc-p2-3-s3-static-policy-mappingproxy-serialization-targeted-source-rework-1.md`  `538eab59c81e71fb8b976447264e7ecdb230ef24f3d98f6192d35ceec77ea71a`
- `.aiassistant/records/aiscc/cycles/20260914_0057_aiscc-p2-3-s4-human-gate-reservation-reference-rework-entry-1.cycle.md`  `0adc2fb0859f8131ccb7e062df589066e027992f240ff31fecb7ca0f4ecf3fe7`
- `.aiassistant/reports/aiscc/20260914_0057_aiscc-p2-3-0039-s3-source-accepted-s4-reservation-reference-rework-judgment-1.md`  `0c4a42d4a12bca2db9748a67b84e0b80cce92bbfb5f008cfd6d8fcead5dcec65`
- `.aiassistant/tasks/done/20260914_0057_aiscc-p2-3-s4-human-gate-reservation-reference-handoff-targeted-source-rework-1.md`  `c01203c0d43d8804893ec637a9afe8cde2a748af8ad3575b0b90c38e9672d518`

Canonical state:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `281bd733624ac87be207f62ed59b99edf0d64cf3b8f3d00e9bc9611fe3179f8c`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `b55eb504c39af0134837f808eef8610b0c54505ee8c597b332f79148ad61d8bd`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `1bb251b5758e8fea1ac260dcace074dcb7e2ff9adf6a96e8699d29c66bea495d`

Preserve ignored non-owned legacy:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
SHA-256 52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

After current Cycle/Judgment placement while current Task remains active/ignored:

```text
Git-visible untracked exactly 11
```

Any mismatch → STOP before staging/private access.

# 3. accepted combined candidate invariants

Reverify before staging:

```text
S3:
static evidence body and canonical producer hash use the same plain mapping;
generic canonical JSON unchanged.

S4:
real HumanGateReservation is still returned by HumanGateReservationAuthority;
gate_open_participant still receives the same typed reservation;
Stockroom gate ref uses existing P1-7 representation:
p1-7-gate:<human_gate_version>:<human_gate_id>;
same ref is used by pending authority, handle, snapshot and durable gate lookup.

P1-7 models/authority/repository:
unchanged.
```

Do not edit candidate before persistence.

# 4. Commit A — exact 13 paths

Stage exactly:

```text
11 governance paths:
- 9 predecessor governance artifacts
- current Cycle
- current Judgment

2 candidate paths:
- src/aiscc/scenarios/stockroom_production.py
- tests/integration/scenarios/test_stockroom_binding.py
```

Do not stage:

```text
current active Task
canonical state files
legacy 1400 active Task
reports/target
anything else
```

Commit message exactly:

```text
fix(aiscc): correct stockroom S3 S4 authority handoffs
```

Require:

```text
Commit A parent = 33a216f29062176ad196a567a299ba30291c3f72
Commit A changed paths = exact 13
```

After commit:

```text
HEAD = Commit A
index empty
tracked clean
Git-visible untracked = 0
```

Current Task remains active/ignored.

Any assertion failure → STOP; no private access.

# 5. state boundary

Do not modify:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

P2-3 terminal reconciliation waits for Browser acceptance after S3/S4 and Replay.

# 6. retained private environment

Only after Commit A exact verification, reverify accepted retained PostgreSQL:

```text
container:
aiscc-p2-3-private-postgres-v1

container ID:
0b50ac47a79e05ac9b88a8f679d04ddc39f729bf1a8e099d149c4c5570b5999c

image:
sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94

volume:
aiscc-p2-3-private-postgres-data-v1

endpoint:
127.0.0.1:55432

database/role:
aiscc_private_capture

migration:
20260901_0008

secret bind:
Destination=/run/secrets/postgres_password
Type=bind
RW=false
```

Use accepted reversible Docker Desktop mapping only.

Require private ACL, no reparse, no repo/Downloads overlap.

Never export private absolute path, password, DB URL, raw inspect/ACL/evidence body.

# 7. preserved private lineage

Read-only verify and fingerprint before/after:

## accepted S1

```text
run:
aiscc-p2-3-private-s1-normal-v5-run

WorkRun:
ACCEPTED/v4

attempt:
EXECUTOR_COMPLETED/v8

Judgment:
ACCEPTED
```

## accepted S2

```text
run:
aiscc-p2-3-private-s2-missing-evidence-v6-run

WorkRun:
REWORK_REQUIRED/v4

attempt:
EXECUTOR_COMPLETED/v8

JudgmentKind:
HOLD_REWORK_REQUIRED

HumanResult:
0
```

## stranded S3 from 0009

```text
run:
aiscc-p2-3-private-s3-policy-conflict-v7-run

attempt:
aiscc-p2-3-private-s3-policy-conflict-v7-attempt-1

WorkRun:
RUNNING/v2

attempt:
NOT_STARTED/v1

provider/tool/evidence/blocker/Judgment/HumanResult:
0
```

This lineage and its evidence-bearing root are NOT reusable.

## old S4 v8 plan

Preserve any existing root residue from the earlier matrix exactly as found.
Its WorkRun/attempt must remain absent because S4 never started.

## older history

Preserve:
0036/v1 terminal/quarantined;
1822/v2 provider-grant failure;
v3 absent;
2040/v4 ADMISSION_PENDING with accepted Judgment.

No repair/replay/transition/disposition/cleanup of any historical lineage.

# 8. fresh private identities

Fresh S3:

```text
root leaf:
aiscc-p2-3-private-runtime-v9-s3

run:
aiscc-p2-3-private-s3-policy-conflict-v9-run

attempt:
aiscc-p2-3-private-s3-policy-conflict-v9-attempt-1
```

Fresh S4:

```text
root leaf:
aiscc-p2-3-private-runtime-v10-s4

run:
aiscc-p2-3-private-s4-human-owned-claim-v10-run

attempt:
aiscc-p2-3-private-s4-human-owned-claim-v10-attempt-1
```

Before any fresh root creation require both roots and both run/attempt pairs absent.

If any exists → STOP; no delete/reuse.

# 9. S3 fresh root / production application

Create S3 root only after all preceding checks.

Require:

```text
empty
resolved exact
no reparse
ACL no broader than private parent
no repo/Downloads overlap
```

Require exact Stockroom image:

```text
sha256:c51ad05852b58a3b4fd275ee88d183551e745d79ac8239e3da3b98372fe0bb9e
```

Call public `build_stockroom_production` exactly once for S3 with:

```text
repository_root = exact Commit A
private_runtime_root = S3 root
project_id = aiscc-stockroom-private-capture
requester_identity = aiscc-owner-operator
human_selector_fingerprint = c55280095ff8bbac5ab186e44e3856e6a435da548c1c88b02b66caeba36e8f07
cancellation = exact S3 run/attempt
trusted Docker/Git = exact executables
accepted Stockroom image provenance
local compatibility secret only
```

Require v2 evidence/Judgment authority registration zero durable delta and legacy v1 unchanged.

No direct internal builder.

# 10. fresh S3 execution

Use only:

```text
prepare_capture(
    scenario_id="stockroom-s3-policy-conflict",
    run_id="aiscc-p2-3-private-s3-policy-conflict-v9-run",
    attempt_id="aiscc-p2-3-private-s3-policy-conflict-v9-attempt-1",
)

StockroomCaptureRunner.run(prepared)
```

Each exactly once.

Success requires durable proof:

```text
TaskContract:
stockroom-s3-policy-conflict / 2.0.0

READY→RUNNING:
ADMITTED

static policy evidence:
ADMITTED
exact source-owned fixture semantics

evidence-set/checkpoint:
SATISFIED as required for blocker path

P1-4 blocker provenance:
blocker_kind POLICY
reason_code POLICY_CONFLICT

final WorkRun:
BLOCKED

ExecutionAttempt:
must remain not execution-started according to source-owned S3 path

provider operations:
0

tool operations:
0

Judgment:
0

HumanResult:
0

running transient:
0
```

The required result is policy-conflict `BLOCKED`, not exception/security failure.

If S3 does not satisfy every mandatory semantic:
`STOP_PRESERVE`.
Do not create or execute S4.

# 11. S4 admission only after S3 success

After S3 success, reverify:

```text
S3 final BLOCKED
provider/tool/Judgment/HumanResult 0
S4 root/run/attempt still absent
```

Then create S4 root once with the same private-root safety checks.

Call public `build_stockroom_production` exactly once for S4, with its own exact root and S4 cancellation:

```text
run:
aiscc-p2-3-private-s4-human-owned-claim-v10-run

attempt:
aiscc-p2-3-private-s4-human-owned-claim-v10-attempt-1
```

Again require v2 evidence/Judgment registrations zero durable delta and legacy v1 unchanged.

# 12. fresh S4 execution

Use only:

```text
prepare_capture(
    scenario_id="stockroom-s4-human-owned-claim",
    run_id="aiscc-p2-3-private-s4-human-owned-claim-v10-run",
    attempt_id="aiscc-p2-3-private-s4-human-owned-claim-v10-attempt-1",
)

StockroomCaptureRunner.run(prepared)
```

Each exactly once.

Before run, derive the source-owned S4 path from committed source without modifying it.

Mandatory success:

```text
TaskContract:
stockroom-s4-human-owned-claim / 2.0.0

PRE_HUMAN P1-6 evidence/checkpoint:
SATISFIED

HumanGateReservation:
real P1-7 owner-issued typed reservation

gate ref:
p1-7-gate:<human_gate_version>:<human_gate_id>

same ref:
pending authority
adapter handle
owner snapshot
durable HumanGate repository lookup

Human guard attestation:
present / owner-backed

Judgment guard attestation:
0

transition:
ADMISSION_PENDING→HUMAN_REQUIRED admitted

final WorkRun:
HUMAN_REQUIRED

durable HumanGate:
exact run/opened-state/opened-version/bound-version identity

HumanResult:
0

Judgment:
0

premature ACCEPTED / REWORK_REQUIRED judgment:
0

running transient:
0
```

Stop at `HUMAN_REQUIRED`.

Do not submit or simulate Human action.

Report actual execution/provider/tool counts according to the source-owned S4 path. Do not invent S1 counts or make an arbitrary count a success gate unless source semantics require it.

# 13. common runtime prohibitions

Across S3/S4:

```text
external OpenAI/provider inference = 0
arbitrary outbound network = 0
scenario retry = 0
alternate WorkRun/attempt = 0
manual transition = 0
DB repair = 0
private-attribute mutation = 0
source/test/config/state edit after Commit A = 0
```

S1/S2 must not execute.

# 14. final simultaneous private poststate

If S3 and S4 both succeed, capture one read-only poststate proving:

```text
S1 v5:
ACCEPTED unchanged

S2 v6:
REWORK_REQUIRED + HOLD_REWORK_REQUIRED unchanged

stranded S3 v7:
RUNNING/v2 unchanged / not reused

fresh S3 v9:
BLOCKED
POLICY/POLICY_CONFLICT
provider/tool/Judgment/HumanResult 0

fresh S4 v10:
HUMAN_REQUIRED
HumanGate present
HumanResult/Judgment 0

no duplicate WorkRun/attempt identity
no cross-run evidence substitution
```

# 15. settlement / failure

Each application/runner has one chance only.

On any blocker/failure:

```text
preserve Commit A
preserve fresh/historical evidence
do not create replacement identity
do not retry
do not repair DB
do not manually transition
do not delete evidence-bearing root
STOP_PRESERVE
```

No broad cleanup.

Local residue is non-blocking unless it violates security/runtime invariants.

# 16. Git terminal

After Commit A no tracked mutation is allowed.

Move current Task active→done byte-identically.

Final success:

```text
HEAD = Commit A
index empty
tracked clean

Git-visible untracked exactly one:
.aiassistant/tasks/done/20260914_0118_aiscc-p2-3-s3-s4-source-persistence-and-fresh-private-runtime-retry-1.md

legacy 1400:
preserved / ignored / non-owned
```

Do not stage or commit current done Task.
No push.

# 17. contract review

Exactly 79 rows:

```text
TRANSPORT_PACKAGE_EXACT
BASE_HEAD_PARENT_EXACT
INITIAL_INDEX_EMPTY
INITIAL_TRACKED_DIRT_EXACT_2
INITIAL_UNTRACKED_GOVERNANCE_EXACT_9
PREDECESSOR_0057_RESULT_ACCEPTED
PREDECESSOR_GOVERNANCE_HASHES_EXACT
CURRENT_STATE_HASHES_EXACT
LEGACY_1400_ACTIVE_PRESERVED
PYTHON_REPOSITORY_VENV_EXACT
COMBINED_CANDIDATE_HASHES_EXACT
COMMIT_A_STAGE_SET_EXACT_13
COMMIT_A_PARENT_EXACT
COMMIT_A_MESSAGE_EXACT
COMMIT_A_CHANGED_PATHS_EXACT_13
POST_COMMIT_INDEX_EMPTY_TRACKED_CLEAN
POST_COMMIT_UNTRACKED_ZERO
NO_CANONICAL_STATE_MUTATION
PRIVATE_POSTGRES_IDENTITY_EXACT
PRIVATE_SECRET_BIND_AND_ACL_EXACT
PRIVATE_S1_V5_PRESERVED_ACCEPTED
PRIVATE_S2_V6_PRESERVED_REWORK_REQUIRED
STRANDED_S3_V7_PRESERVED
UNUSED_S4_V8_PRESERVED
HISTORICAL_V1_V2_V4_PRESERVED
S3_V9_ROOT_ABSENT_BEFORE_CREATE
S3_V9_RUN_ATTEMPT_ABSENT_BEFORE_CREATE
S4_V10_ROOT_ABSENT_BEFORE_CREATE
S4_V10_RUN_ATTEMPT_ABSENT_BEFORE_CREATE
S3_V9_ROOT_CREATED_EMPTY_PRIVATE
STOCKROOM_IMAGE_IDENTITY_EXACT
S3_BUILDER_SINGLE_CALL
S3_CANCELLATION_BOUND_EXACT
S3_V2_AUTHORITY_REGISTRATION_ZERO_DELTA
S3_V2_JUDGMENT_REGISTRATION_ZERO_DELTA
S3_PREPARE_SINGLE_CALL
S3_RUNNER_SINGLE_CALL
S3_TASKCONTRACT_V2_SELECTED
S3_STATIC_POLICY_EVIDENCE_ADMITTED
S3_POLICY_BLOCKER_ADMITTED
S3_FINAL_WORKRUN_BLOCKED
S3_ATTEMPT_NOT_EXECUTION_STARTED
S3_PROVIDER_OPERATION_ZERO
S3_TOOL_OPERATION_ZERO
S3_JUDGMENT_ZERO
S3_HUMAN_RESULT_ZERO
S3_NO_RUNNING_TRANSIENT
S4_NOT_STARTED_BEFORE_S3_SUCCESS
S4_V10_ROOT_CREATED_EMPTY_PRIVATE
S4_BUILDER_SINGLE_CALL
S4_CANCELLATION_BOUND_EXACT
S4_V2_AUTHORITY_REGISTRATION_ZERO_DELTA
S4_V2_JUDGMENT_REGISTRATION_ZERO_DELTA
S4_PREPARE_SINGLE_CALL
S4_RUNNER_SINGLE_CALL
S4_TASKCONTRACT_V2_SELECTED
S4_PREHUMAN_EVIDENCE_SATISFIED
S4_HUMAN_GATE_RESERVATION_REAL_P1_7
S4_GATE_REFERENCE_SCHEMA_EXACT
S4_HUMAN_GUARD_ATTESTATION_PRESENT
S4_JUDGMENT_GUARD_ATTESTATION_ZERO
S4_FINAL_WORKRUN_HUMAN_REQUIRED
S4_HUMAN_GATE_DURABLE_PRESENT
S4_HUMAN_RESULT_ZERO
S4_JUDGMENT_ZERO
S4_NO_PREMATURE_ACCEPTED_OR_REWORK
S4_NO_RUNNING_TRANSIENT
NO_EXTERNAL_PROVIDER_NETWORK_S3_S4
NO_SCENARIO_RETRY
NO_S1_S2_RERUN
NO_HISTORICAL_LINEAGE_MUTATION
NO_SOURCE_TEST_CONFIG_STATE_MUTATION_AFTER_COMMIT
NO_GIT_PUSH
PRIVATE_VALUE_EXPORT_SCAN_PASS
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
FINAL_HEAD_IS_COMMIT_A
FINAL_INDEX_EMPTY_TRACKED_CLEAN
FINAL_UNTRACKED_CURRENT_DONE_TASK_ONLY
EXPORT_INTEGRITY_PASS
```

Full success:

```text
79 / 79 PASS
```

If S3 fails, all S4 execution success rows remain non-PASS.
If S4 fails, preserve the successful S3 evidence and report the exact S4 blocker.

# 18. export

Root docs:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
0057_ACCEPTANCE_VERIFICATION.md
SOURCE_PERSISTENCE_VERIFICATION.md
COMMIT_A_PATHS.md
PRIVATE_RUNTIME_IDENTITY_VERIFICATION.md
HISTORICAL_LINEAGE_PRESERVATION.md
S3_APPLICATION_VERIFICATION.md
S3_EXECUTION_VERIFICATION.md
S3_POLICY_BLOCKER_VERIFICATION.md
S4_APPLICATION_VERIFICATION.md
S4_EXECUTION_VERIFICATION.md
S4_PREHUMAN_EVIDENCE_VERIFICATION.md
S4_HUMAN_GATE_VERIFICATION.md
MATRIX_POSTSTATE_VERIFICATION.md
RUNTIME_SETTLEMENT_VERIFICATION.md
PRIVATE_VALUE_SCAN.md
CONTRACT_REVIEW.md
```

Include project-relative copies of:

```text
current Cycle
current Judgment
current done Task
src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_binding.py
```

Generate manifest/member counts from actual declared set.

Require:

```text
one top-level
CRC PASS
manifest SHA/size exact
TASK.md == canonical done Task
private-value/path scan PASS
```

# 19. success ceiling

```text
S1:
ACCEPTED / CLOSED

S2:
REWORK_REQUIRED / ACCEPTED

S3:
fresh private BLOCKED runtime candidate

S4:
fresh private HUMAN_REQUIRED runtime candidate
HumanResult/Judgment 0

combined S3/S4 source:
PERSISTED

Replay:
NOT_STARTED

P2-3 terminal closure:
NOT_STARTED

Browser runtime acceptance:
PENDING

P2-3:
IN_PROGRESS
```
