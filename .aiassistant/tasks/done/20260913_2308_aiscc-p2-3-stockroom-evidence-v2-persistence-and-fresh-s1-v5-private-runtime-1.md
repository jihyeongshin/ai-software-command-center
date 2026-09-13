# 작업지시서: P2-3 Stockroom evidence v2 persistence and fresh S1 v5 private runtime

## meta

- task_id: `20260913_2308_aiscc-p2-3-stockroom-evidence-v2-persistence-and-fresh-s1-v5-private-runtime-1`
- created_at: `2026-09-13T23:08:24+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `SOURCE_PERSISTENCE + PRIVATE_SCENARIO_EXECUTION / S1_NORMAL`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `15c9e975ec193526eafa0749fc97321c4d89d713`
- required_base_parent: `c9093e8441de230f9470313d874a33addc75423c`
- required_base_grandparent: `af5a9f873f11da1fdf71362abde018a2bed313a4`
- accepted_2225_result_zip_sha256: `b6629237ace8eaa995ee399a7a6df343e59fe72fcd22e054d662b9c3a83bd18e`
- source_commit_authorized: `Yes / exact 24 paths`
- private_runtime_authorized: `Yes / only after exact Commit A`
- canonical_state_write_authorized: `No`
- second_runtime_attempt_authorized: `No`
- push_authorized: `No`
- success_ceiling: `FRESH_S1_V5_ACCEPTED_RUNTIME_CANDIDATE / BROWSER_REVIEW_PENDING`

# 0. ordered authority

This Task combines two strictly ordered operations:

```text
A. persist the Browser-accepted Stockroom evidence-v2 source candidate and accumulated governance
B. only if A is exact, execute one fresh private S1 using v2
```

B before A is forbidden.

# 1. executables

Repository:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center
```

Python:

```text
<repository-root>\.venv\Scripts\python.exe
```

Use only that fixed relative executable.

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
HEAD 15c9e975ec193526eafa0749fc97321c4d89d713
HEAD^ c9093e8441de230f9470313d874a33addc75423c
HEAD^^ af5a9f873f11da1fdf71362abde018a2bed313a4
index empty
```

Tracked dirt must be exactly these three modified tracked paths, with exact final candidate hashes:

```text
src/aiscc/scenarios/stockroom_production.py
38a6045cab460405627bc9fdd6f43988b74613cb3adbe60e93e972f8ee9586b5

tests/integration/scenarios/test_stockroom_binding.py
54c9d59b66c69e6da0d7d3e3f5caa4f02d293f505809df945cb501acf2e83e66

tests/integration/scenarios/test_stockroom_capture_runner.py
8ee7391832056839fbd7b54403f7318ee259a73c182c8d922244db852f188d7f
```

Pre-delivery Git-visible untracked must be exactly 19:

```text
18 governance artifacts
+ config/evidence/stockroom-capture.v2.json
```

The 18 governance artifacts are:

- `.aiassistant/records/aiscc/cycles/20260913_2019_aiscc-p2-3-provider-grant-fix-accepted-fresh-s1-v3-retry-entry-1.cycle.md`  `959ac0166ba30510172b2a5a349fab5b622ad7282d67853b8ee8de2830e3561f`
- `.aiassistant/reports/aiscc/20260913_2019_aiscc-p2-3-provider-grant-fix-source-acceptance-and-runtime-retry-authorization-1.md`  `aba7746a9febe65de59fdebc504be9ca889225d3e1e5d181249cdc51ed612d06`
- `.aiassistant/tasks/done/20260913_2019_aiscc-p2-3-provider-grant-fix-persistence-and-fresh-s1-v3-runtime-retry-1.md`  `a7e1d738a03f0a5209f9edd2349d797ef7590afc2b526a9207596c731caeeb87`
- `.aiassistant/records/aiscc/cycles/20260913_2040_aiscc-p2-3-fresh-s1-v4-runtime-retry-entry-1.cycle.md`  `0043e24a5125f12f122e7adcdac14bdca2ed0797a415ebe5ae70ba0fe666de08`
- `.aiassistant/reports/aiscc/20260913_2040_aiscc-p2-3-2019-part-a-accepted-part-b-executor-preflight-retry-judgment-1.md`  `5beb946af3bcf6c1149ac236c797a9492368e19272eb8d1441220ea2c5940c6e`
- `.aiassistant/tasks/done/20260913_2040_aiscc-p2-3-fresh-s1-v4-runtime-retry-after-executor-path-basis-correction-1.md`  `26d530e1500cbcb5347e3ee1ace4e637e71398adf898baaf41340f5d26491cdd`
- `.aiassistant/records/aiscc/cycles/20260913_2054_aiscc-p2-3-s1-final-judgment-guard-handoff-rework-entry-1.cycle.md`  `700d4ee524302a5d69e39a8546e7f308d2c0022edb3340d00b12a1f8ad6cc299`
- `.aiassistant/reports/aiscc/20260913_2054_aiscc-p2-3-s1-v4-final-transition-denied-rework-judgment-1.md`  `64bb57b0cd09d41cd8aa039ffccee846ed32b72bce720b619eff2c16f1c3aa72`
- `.aiassistant/tasks/done/20260913_2054_aiscc-p2-3-s1-final-judgment-guard-handoff-targeted-source-rework-1.md`  `a7122b72247d647039bc50937fa5d9afcc21d98a5359d398a11cc2c9566d0e3b`
- `.aiassistant/records/aiscc/cycles/20260913_2120_aiscc-p2-3-p1-6-timestamp-authority-compatibility-rework-entry-1.cycle.md`  `4a2a92d1691bf7ae204f690a9c6aaa9ebedba11752f4441a48cda0fc91886489`
- `.aiassistant/reports/aiscc/20260913_2120_aiscc-p2-3-2054-scope-expansion-p1-6-authority-rework-judgment-1.md`  `bad8095470e5412d3ae40be8d7378bf359981ddad340f2a04c28d16b03083530`
- `.aiassistant/tasks/done/20260913_2120_aiscc-p2-3-p1-6-evidence-authority-timestamp-canonicalization-compatibility-rework-1.md`  `6d478d01df64255a4dceac205e88e34392c3fc4fa0d74813b102521b7cc99b45`
- `.aiassistant/records/aiscc/cycles/20260913_2202_aiscc-p2-3-stockroom-evidence-authority-v2-cutover-entry-1.cycle.md`  `0b5fb2754bfa0ee6eaf192e5565fee2ac2016aa4b661b2b4570ae22fe4e6bda5`
- `.aiassistant/reports/aiscc/20260913_2202_aiscc-p2-3-2120-legacy-compatibility-stop-v2-cutover-judgment-1.md`  `eaf785ee5bc3b780f22800fbb227e32e120c3756f57a5f742c1161aad61e2bfe`
- `.aiassistant/tasks/done/20260913_2202_aiscc-p2-3-stockroom-evidence-authority-v2-prospective-cutover-rework-1.md`  `bdf547850d02f4724766fb15aee173418a8a4c633b4f01a46afdeaf1352833fc`
- `.aiassistant/records/aiscc/cycles/20260913_2225_aiscc-p2-3-stockroom-evidence-authority-v2-cutover-untracked-scope-correction-entry-1.cycle.md`  `2bde2de2060b40012b810e9c5ba58ef52afeaf83faf38425f8e186a9f2da99e0`
- `.aiassistant/reports/aiscc/20260913_2225_aiscc-p2-3-2202-command-center-untracked-scope-conflict-judgment-1.md`  `875ffbce7d5a78cfb924e2776670be93cd1da73ee8cd304e0374698b85d95fd7`
- `.aiassistant/tasks/done/20260913_2225_aiscc-p2-3-stockroom-evidence-authority-v2-cutover-untracked-scope-corrected-retry-1.md`  `e408dec493cdfcec2713b76adedd522e7c883a199cbd7ebe73711a85e17358bf`

V2 config:

```text
config/evidence/stockroom-capture.v2.json
SHA-256 3c7468dc9f1dc86ed5b77b1e3b9d5996d3e19bac2e5df5c72baaf23c95cd80db
```

Current canonical state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `281bd733624ac87be207f62ed59b99edf0d64cf3b8f3d00e9bc9611fe3179f8c`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `b55eb504c39af0134837f808eef8610b0c54505ee8c597b332f79148ad61d8bd`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `1bb251b5758e8fea1ac260dcace074dcb7e2ff9adf6a96e8699d29c66bea495d`

Preserve ignored non-owned legacy Task:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
SHA-256 52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

After current Cycle/Judgment placement while current Task remains active/ignored:

```text
governance untracked:
20

product untracked:
1

total Git-visible untracked:
21
```

Any mismatch → STOP before staging or private runtime access.

# 3. accepted candidate semantics

Before staging, reverify these exact candidate hashes:

- `config/evidence/stockroom-capture.v2.json`  `3c7468dc9f1dc86ed5b77b1e3b9d5996d3e19bac2e5df5c72baaf23c95cd80db`
- `src/aiscc/scenarios/stockroom_production.py`  `38a6045cab460405627bc9fdd6f43988b74613cb3adbe60e93e972f8ee9586b5`
- `tests/integration/scenarios/test_stockroom_binding.py`  `54c9d59b66c69e6da0d7d3e3f5caa4f02d293f505809df945cb501acf2e83e66`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`  `8ee7391832056839fbd7b54403f7318ee259a73c182c8d922244db852f188d7f`

Require:

```text
v1 config remains byte-identical
generic P1-6 requirements/repository remain tracked at HEAD and unmodified
fresh production selects stockroom-capture.v2.json
fresh TaskContract version = 2.0.0
v2 authority/version and @v2 durable refs are disjoint from v1
v2 timestamps are explicit UTC +00:00
```

Do not change the candidate before persistence.

# 4. Commit A — exact persistence

Stage exactly 24 paths:

```text
20 governance paths:
- 18 predecessor governance artifacts
- current Cycle
- current Judgment

4 candidate paths:
- config/evidence/stockroom-capture.v2.json
- src/aiscc/scenarios/stockroom_production.py
- tests/integration/scenarios/test_stockroom_binding.py
- tests/integration/scenarios/test_stockroom_capture_runner.py
```

Do not stage:

```text
current active Task
canonical state files
legacy 1400 active Task
reports/target
any other path
```

Commit message exactly:

```text
feat(aiscc): cut over stockroom evidence authority v2
```

Require:

```text
Commit A parent = 15c9e975ec193526eafa0749fc97321c4d89d713
Commit A changed paths = exact 24
```

After Commit A:

```text
HEAD = Commit A
index empty
tracked clean
Git-visible untracked = 0
```

Current Task remains ignored in active.

Failure of any Git assertion → STOP; no private runtime access.

# 5. canonical state boundary

Do not modify:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

State reconciliation waits for Browser review of the private S1 result.

# 6. retained private environment

Only after Commit A exact verification, verify retained PostgreSQL:

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
```

Secret bind:

```text
Destination=/run/secrets/postgres_password
Type=bind
RW=false
```

Derive private parent only through the accepted reversible Docker Desktop mapping.

Require:

```text
protected/private ACL
no reparse
no repository/Downloads overlap
```

Never export private absolute paths, password, DB URL, raw inspect or ACL body.

# 7. historical lineage preservation

Read-only verify, do not mutate:

## 0036 / v1 root

```text
WorkRun FAILED/v3
attempt EXECUTION_FAILED/v2
one quarantine
fingerprint 18433a8d92affe915d01e3bb1265b387a07dc6478e09c92306854908ab396068
```

## 1822 / v2-run root

```text
run:
aiscc-p2-3-private-s1-normal-v2-run

attempt:
aiscc-p2-3-private-s1-normal-v2-attempt-1

WorkRun:
RUNNING/v2

attempt:
EXECUTION_FAILED/v3

failure:
P1_3_SECURITY_DENIED:PROVIDER:EXACT_RESOURCE_GRANT_DENIED

workspace:
retained / evidence-bearing
```

## v3 root

Require absent/unused.

## 2040 / v4 root

```text
run:
aiscc-p2-3-private-s1-normal-v4-run

attempt:
aiscc-p2-3-private-s1-normal-v4-attempt-1

WorkRun:
ADMISSION_PENDING/v3

attempt:
EXECUTOR_COMPLETED/v8

admitted evidence:
present

evidence-set attestation:
present

Judgment:
ACCEPTED

final transition:
not admitted

workspace:
retained / evidence-bearing
```

Do not replay, repair, transition, dispose, rename or clean any historical lineage.

# 8. v2 authority pre-builder DB proof

The private DB was created under legacy Stockroom v1 evidence authority.

Before builder, require that the exact v2 durable refs from committed `stockroom-capture.v2.json` are absent from:

```text
EvidenceRequirementSet
EvidenceRequirement
EvidenceCheckpoint
```

Also require the fresh v2 Judgment policy versions projected by the committed source are absent.

Do not require the database to be otherwise pristine.

Capture:

```text
v1 authority row identities/fingerprints
all v2 expected row identities
current counts/fingerprints of authority tables
```

# 9. fresh v5 subject/root

Fresh identities:

```text
project_id:
aiscc-stockroom-private-capture

run_id:
aiscc-p2-3-private-s1-normal-v5-run

attempt_id:
aiscc-p2-3-private-s1-normal-v5-attempt-1

requester_identity:
aiscc-owner-operator

RuntimeMode:
OWNER_SELF_DOGFOOD
```

Fresh root:

```text
<verified private parent>/aiscc-p2-3-private-runtime-v5
```

Require before creation:

```text
v5 root absent
v5 WorkRun absent
v5 attempt absent
```

If any exists → STOP. Do not reuse/delete it.

Then create exactly the v5 root and require:

```text
empty
resolved exact
no reparse
ACL no broader than private parent
no repository/Downloads overlap
```

# 10. Stockroom image

Require exact retained image:

```text
sha256:c51ad05852b58a3b4fd275ee88d183551e745d79ac8239e3da3b98372fe0bb9e
```

Require no running transient bound to v5 identities.

# 11. derive builder registration envelope before builder

Read committed source/config and derive the exact expected builder registration delta for the current private DB.

At minimum cover:

```text
EvidenceRequirementSet rows
EvidenceRequirement rows
EvidenceCheckpoint rows
Evidence authority events/supersession rows
JudgmentPolicy rows
JudgmentPolicyProjection rows
```

Because v2 uses disjoint TaskContract/ref/policy scope, success expectation is:

```text
new v2 rows inserted or idempotently established exactly as source specifies
legacy v1 rows/fingerprints unchanged
no v1 supersession/revocation/reseal
```

Do not hardcode a row count without deriving it from the committed source and current DB snapshot.

# 12. production builder exactly once

Call public `build_stockroom_production` exactly once using:

```text
repository_root = exact Commit A repository
private_runtime_root = v5 root
downloads_root = C:\Users\oracl\Downloads
project_id = aiscc-stockroom-private-capture
requester_identity = aiscc-owner-operator
human_selector_fingerprint = c55280095ff8bbac5ab186e44e3856e6a435da548c1c88b02b66caeba36e8f07
trusted Docker = exact executable
trusted Git = exact executable
accepted Stockroom image provenance
local compatibility secret material only
cancellation bound to v5 run/attempt
```

No direct internal builder call.

After builder require:

```text
fresh production evidence config = v2
S1 TaskContract version = 2.0.0
v2 authority row identities exactly match committed config
v2 row fingerprints survive DB row decode/reverification
v2 Judgment policy rows exactly match committed projection
legacy v1 authority identities/fingerprints unchanged
no unrelated authority mutation beyond source-derived envelope
```

If builder fails or post-builder envelope mismatches → STOP, no prepare/runner.

# 13. source-owned prepare + runner

Use only:

```text
prepare_capture(
    scenario_id="stockroom-s1-normal",
    run_id="aiscc-p2-3-private-s1-normal-v5-run",
    attempt_id="aiscc-p2-3-private-s1-normal-v5-attempt-1",
)

StockroomCaptureRunner.run(prepared)
```

Each exactly once.

No direct owner lifecycle calls.
No manual `PreparedStockroomDriver`.
No runner retry.

# 14. required runtime chain

Success requires durable proof of:

```text
new v5 WorkRun with TaskContract 2.0.0
new v5 attempt

READY→RUNNING:
ADMITTED

EXECUTION_STARTED:
before first provider/tool side effect

provider ResourceGrants:
ADMITTED / exact

local deterministic provider operations:
bounded / completed

Stockroom tool/process grant:
ADMITTED / exact

tool/process execution:
bounded / completed

ExecutionAttempt:
EXECUTOR_COMPLETED

RUNNING→ADMISSION_PENDING:
ADMITTED

v2 runtime evidence:
ADMITTED

v2 historical authority graph:
VERIFIED after durable row round-trip

v2 evidence-set satisfaction attestation:
present

Judgment:
ACCEPTED

Human guard attestation:
present / owner-backed

Judgment guard attestation:
present / owner-backed

ADMISSION_PENDING→ACCEPTED:
ADMITTED

final WorkRun:
ACCEPTED
```

Report exact actual Workflow `state_version` and ExecutionAttempt `execution_version`.

# 15. execution/network boundary

Require:

```text
external OpenAI/provider inference:
0

arbitrary outbound network:
0
```

Only the configured local deterministic provider/tool path is authorized.

# 16. scenario isolation

Forbidden:

```text
S2 execution
S3 execution
S4 execution
HumanResult creation
Replay generation
public deployment
canonical state mutation
historical lineage repair
source/test/config edits after Commit A
```

# 17. failure semantics

Any pre-run blocker:

```text
runner calls = 0
STOP_PRESERVE
```

Any runner exception/STOP/failure:

```text
runner calls = 1 maximum
no second WorkRun
no alternate attempt
no DB repair
no manual transition
no destructive cleanup of v5 evidence
read-only classify durable state
STOP_PRESERVE
```

Commit A remains valid and must not be reset/reverted automatically.

# 18. post-run settlement

Success requires:

```text
v5 WorkRun ACCEPTED
v5 attempt EXECUTOR_COMPLETED
S1 Judgment ACCEPTED
v2 admitted evidence present
v2 evidence-set attestation present
Human/Judgment guard attestations present
no HumanResult
no S2/S3/S4
0036/v1 unchanged
1822/v2-run unchanged
v3 absent
2040/v4 unchanged
no running v5 Stockroom transient
```

Report workspace cleanup/residue exactly as source-owned runtime leaves it.

Local housekeeping residue alone is not a substantive failure unless it violates security/runtime invariants.

# 19. Git terminal boundary

After Commit A, no tracked/source/state mutation is authorized.

Move current Task active→done byte-identically.

Final require:

```text
HEAD = Commit A
index empty
tracked clean

Git-visible untracked exactly one:
.aiassistant/tasks/done/20260913_2308_aiscc-p2-3-stockroom-evidence-v2-persistence-and-fresh-s1-v5-private-runtime-1.md

legacy 1400:
preserved / ignored / non-owned
```

Do not stage/commit the current done Task in this Task.
No push.

# 20. contract review

Exactly 65 rows:

```text
TRANSPORT_PACKAGE_EXACT
BASE_HEAD_PARENT_EXACT
INITIAL_INDEX_EMPTY
INITIAL_TRACKED_DIRT_EXACT_3
INITIAL_UNTRACKED_EXACT_19
PREDECESSOR_GOVERNANCE_HASHES_EXACT
CURRENT_STATE_HASHES_EXACT
CANDIDATE_HASHES_EXACT
LEGACY_1400_ACTIVE_PRESERVED
PYTHON_REPOSITORY_VENV_EXACT
COMMIT_A_STAGE_SET_EXACT_24
COMMIT_A_PARENT_EXACT
COMMIT_A_MESSAGE_EXACT
COMMIT_A_CHANGED_PATHS_EXACT_24
POST_COMMIT_INDEX_EMPTY_TRACKED_CLEAN
POST_COMMIT_UNTRACKED_ZERO
NO_CANONICAL_STATE_MUTATION
PRIVATE_POSTGRES_IDENTITY_EXACT
PRIVATE_SECRET_BIND_AND_ACL_EXACT
HISTORICAL_V1_PRESERVED
FAILED_V2_LINEAGE_PRESERVED
V3_ROOT_ABSENT
V4_EVIDENCE_LINEAGE_PRESERVED
V5_RUNTIME_ROOT_ABSENT_BEFORE_CREATE
V5_RUN_ATTEMPT_ABSENT_BEFORE_CREATE
V2_AUTHORITY_ROWS_ABSENT_BEFORE_BUILDER
V2_JUDGMENT_POLICY_ROWS_ABSENT_BEFORE_BUILDER
V5_RUNTIME_ROOT_CREATED_EMPTY_PRIVATE
STOCKROOM_IMAGE_IDENTITY_EXACT
BUILDER_SINGLE_CALL
V2_AUTHORITY_REGISTRATION_SOURCE_DERIVED_DELTA_EXACT
V1_AUTHORITY_ROWS_UNCHANGED_AFTER_BUILDER
V2_JUDGMENT_REGISTRATION_SOURCE_DERIVED_DELTA_EXACT
PUBLIC_PREPARE_CAPTURE_SINGLE_CALL
SOURCE_OWNED_RUNNER_SINGLE_CALL
V5_TASKCONTRACT_V2_SELECTED
READY_TO_RUNNING_ADMITTED
EXECUTION_STARTED_BEFORE_SIDE_EFFECT
PROVIDER_RESOURCE_GRANTS_ADMITTED
LOCAL_PROVIDER_EXECUTION_BOUNDED
TOOL_EXECUTION_BOUNDED
NO_EXTERNAL_PROVIDER_NETWORK
EXECUTION_COMPLETED
RUNNING_TO_ADMISSION_PENDING_ADMITTED
V2_RUNTIME_EVIDENCE_ADMITTED
V2_HISTORICAL_AUTHORITY_VERIFIED
V2_EVIDENCE_ATTESTATION_PRESENT
S1_JUDGMENT_ACCEPTED
HUMAN_GUARD_ATTESTATION_PRESENT
JUDGMENT_GUARD_ATTESTATION_PRESENT
ADMISSION_PENDING_TO_ACCEPTED_ADMITTED
FINAL_WORKRUN_ACCEPTED
NO_HUMAN_RESULT_CREATED
NO_S2_S3_S4_EXECUTION
NO_HISTORICAL_LINEAGE_MUTATION
NO_SECOND_RUNNER_OR_BLIND_RETRY
NO_SOURCE_STATE_MUTATION_AFTER_COMMIT
NO_GIT_PUSH
NO_STOCKROOM_TRANSIENT_RESIDUE
PRIVATE_VALUE_EXPORT_SCAN_PASS
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
FINAL_HEAD_IS_COMMIT_A
FINAL_INDEX_EMPTY_TRACKED_CLEAN
FINAL_UNTRACKED_CURRENT_DONE_TASK_ONLY
EXPORT_INTEGRITY_PASS
```

Full S1 success requires:

```text
65 / 65 PASS
```

Blocked/failed runtime must leave unobserved success rows non-PASS.

# 21. export

Root documents:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
2225_ACCEPTANCE_VERIFICATION.md
SOURCE_PERSISTENCE_VERIFICATION.md
COMMIT_A_PATHS.md
PRIVATE_RUNTIME_IDENTITY_VERIFICATION.md
HISTORICAL_LINEAGE_PRESERVATION_VERIFICATION.md
V2_PRIVATE_REGISTRATION_VERIFICATION.md
FRESH_V5_ROOT_VERIFICATION.md
PRE_S1_DB_SNAPSHOT.md
BUILDER_VERIFICATION.md
S1_PREPARATION_VERIFICATION.md
S1_EXECUTION_VERIFICATION.md
S1_EVIDENCE_VERIFICATION.md
S1_JUDGMENT_GUARD_VERIFICATION.md
POST_S1_DB_SNAPSHOT.md
RUNTIME_SETTLEMENT_VERIFICATION.md
PRIVATE_VALUE_SCAN.md
CONTRACT_REVIEW.md
```

Include project-relative copies of:

```text
current Cycle
current Judgment
current done Task
the four candidate product/config/test paths persisted by Commit A
```

Generate manifest/member count from the actual declared set. Do not maintain a second independent total.

Require:

```text
one top-level
CRC PASS
manifest SHA/size exact
TASK.md == canonical done Task
private-value/path scan PASS
```

# 22. success ceiling

```text
Stockroom evidence v2:
PERSISTED

fresh private S1 v5:
ACCEPTED runtime candidate

legacy v1:
preserved / known offset-sensitive

generic P1-6 legacy migration:
DEFERRED

historical v1/v2-run/v4:
preserved

S2/S3/S4:
NOT_STARTED

canonical state reconciliation:
NOT_PERFORMED

Browser runtime acceptance:
PENDING

P2-3:
IN_PROGRESS
```
