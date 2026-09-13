# 작업지시서: P2-3 fresh S1 v4 runtime retry after Executor path-basis correction

## meta

- task_id: `20260913_2040_aiscc-p2-3-fresh-s1-v4-runtime-retry-after-executor-path-basis-correction-1`
- created_at: `2026-09-13T20:40:15+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `PRIVATE_SCENARIO_EXECUTION / S1_NORMAL_RETRY`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `15c9e975ec193526eafa0749fc97321c4d89d713`
- required_parent: `c9093e8441de230f9470313d874a33addc75423c`
- required_grandparent: `af5a9f873f11da1fdf71362abde018a2bed313a4`
- predecessor_result_zip_sha256: `fcac3715332ad488f317b213a298dec1c5a9f96997069715f1b4bc7c71008f79`
- source_test_config_write_authorized: `No`
- canonical_state_write_authorized: `No`
- Git_commit_push_authorized: `No`
- private_runtime_authorized: `Yes / exact fresh v4 only`
- external_provider_network_authorized: `No`
- success_ceiling: `FRESH_S1_V4_ACCEPTED_RUNTIME_CANDIDATE / BROWSER_REVIEW_PENDING`

# 0. authority correction

2019 Part A is already persisted and must not be repeated.

Current persisted source baseline:

```text
HEAD:
15c9e975ec193526eafa0749fc97321c4d89d713

provider-grant correction:
PERSISTED / ACCEPTED SOURCE CANDIDATE
```

2019 Part B stopped before runtime because the Executor's temporary preservation harness compared different path bases.

Correct v2 source comparison is now mandatory:

```text
RestartWorkspaceInspection inventory path:
source/<manifest-relative-path>

resource manifest path:
<manifest-relative-path>

comparison algorithm:
1. select exactly inventory files under "source/"
2. strip exactly one leading "source/"
3. require resulting set == resource manifest relative-path set
4. compare each file size and SHA-256 exactly
5. reject duplicate, missing, extra or non-source file substitutions
```

Do not compare attempt-relative inventory paths directly with source-relative manifest paths.

# 1. executables

Repository:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center
```

Python:

```text
<repository-root>\.venv\Scripts\python.exe
```

Use only this fixed relative interpreter.

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

Git, read-only only:

```text
C:\Program Files\Git\cmd\git.exe
```

# 2. exact repository baseline

Require:

```text
branch main
HEAD 15c9e975ec193526eafa0749fc97321c4d89d713
HEAD^ c9093e8441de230f9470313d874a33addc75423c
HEAD^^ af5a9f873f11da1fdf71362abde018a2bed313a4
index empty
tracked clean
Git-visible untracked before delivery exactly 3
```

Those three are the 2019 artifacts:

```text
.aiassistant/records/aiscc/cycles/20260913_2019_aiscc-p2-3-provider-grant-fix-accepted-fresh-s1-v3-retry-entry-1.cycle.md
959ac0166ba30510172b2a5a349fab5b622ad7282d67853b8ee8de2830e3561f

.aiassistant/reports/aiscc/20260913_2019_aiscc-p2-3-provider-grant-fix-source-acceptance-and-runtime-retry-authorization-1.md
aba7746a9febe65de59fdebc504be9ca889225d3e1e5d181249cdc51ed612d06

.aiassistant/tasks/done/20260913_2019_aiscc-p2-3-provider-grant-fix-persistence-and-fresh-s1-v3-runtime-retry-1.md
a7e1d738a03f0a5209f9edd2349d797ef7590afc2b526a9207596c731caeeb87
```

Current canonical state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `281bd733624ac87be207f62ed59b99edf0d64cf3b8f3d00e9bc9611fe3179f8c`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `b55eb504c39af0134837f808eef8610b0c54505ee8c597b332f79148ad61d8bd`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `1bb251b5758e8fea1ac260dcace074dcb7e2ff9adf6a96e8699d29c66bea495d`

Persisted candidate hashes at HEAD:

- `src/aiscc/scenarios/stockroom_production.py`  `335678daa9fcd4dd9a4b1a2fc4a53876086cab0d555edb7c413466c531dd6d75`
- `tests/integration/scenarios/test_stockroom_binding.py`  `9bd991b77f711a46662262e12f1471b0b78ba1cc6151b3f6a04650ea68bbf439`
- `tests/unit/providers/test_stockroom_tool.py`  `8acda82618b05364e8a7d31ee1b8f6ed28f1bbf5c6a680dda7e8ffc745466544`

Preserve ignored non-owned legacy:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
SHA-256 52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

After current Cycle/Judgment placement with Task active/ignored:

```text
Git-visible untracked exactly 5
```

Any mismatch → STOP before private runtime access.

# 3. hard prohibitions

Do not:

```text
repeat or amend Commit 15c9e975ec193526eafa0749fc97321c4d89d713
modify source/test/config
modify canonical state
reuse/repair/retry 0036
reuse/repair/retry 1822 v2
create/use v3 root
manual DB repair
manual workflow transition
manual owner-adapter lifecycle calls
external OpenAI/provider inference
arbitrary outbound network
second runner call
alternate attempt after failure
git commit
git push
```

# 4. retained environment

Verify exact retained PostgreSQL:

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

Derive the private parent only through the accepted reversible Docker Desktop mapping.

Require protected/private ACL, no reparse and no repository/Downloads overlap.

Never export secret values, private absolute paths, DB URL, raw inspect or ACL body.

# 5. v1 preservation

Using source-owned restart inspection require exactly:

```text
active:
absent

quarantine:
1

objects:
20

files:
14

fingerprint:
18433a8d92affe915d01e3bb1265b387a07dc6478e09c92306854908ab396068

safety:
PASS
```

Then DB read-only verify:

```text
0036 WorkRun FAILED/v3
0036 attempt EXECUTION_FAILED/v2
reason INVALID_HISTORY_SIDE_EFFECT_BEFORE_EXECUTION_START
```

No mutation.

# 6. v2 preservation — corrected comparator

V2 identities:

```text
run:
aiscc-p2-3-private-s1-normal-v2-run

attempt:
aiscc-p2-3-private-s1-normal-v2-attempt-1
```

Source-owned restart inspection must report:

```text
objects:
20

files:
14

inventory fingerprint:
d1a885a75b076f928126b8e31c9a73200efa5bfe5110ca027170d0dc4ea0cb70

active workspace:
present
```

For source manifest verification apply the exact algorithm from section 0.

Require:

```text
after stripping exactly one "source/" prefix:
14 exact source-relative paths

per-file:
size exact
SHA-256 exact

aggregate:
be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d
```

The `source/` prefix is not a manifest member. It is the source-owned destination directory created by `StockroomWorkspace.allocate`.

Then DB read-only verify:

```text
WorkRun:
RUNNING/v2

attempt:
EXECUTION_FAILED/v3

failure:
P1_3_SECURITY_DENIED:PROVIDER:EXACT_RESOURCE_GRANT_DENIED
```

Do not transition, dispose, clean or reuse v2.

# 7. v3 reservation state

2019 established that v3 root was absent and never created.

Re-observe exact child:

```text
<verified private parent>/aiscc-p2-3-private-runtime-v3
```

Require absent.

Do not create it.

# 8. fresh v4 subject

Fresh identities:

```text
project_id:
aiscc-stockroom-private-capture

run_id:
aiscc-p2-3-private-s1-normal-v4-run

attempt_id:
aiscc-p2-3-private-s1-normal-v4-attempt-1

requester_identity:
aiscc-owner-operator

RuntimeMode:
OWNER_SELF_DOGFOOD
```

Fresh root:

```text
<verified private parent>/aiscc-p2-3-private-runtime-v4
```

Require root absent and v4 run/attempt absent before creation.

If any exists → STOP. Do not reuse or delete.

# 9. create v4 root

Only after sections 4–8 pass, create exactly the v4 root.

Require:

```text
exists
empty
resolved exact
no reparse
ACL no broader than private parent
no repository/Downloads overlap
```

# 10. Stockroom image

Require:

```text
sha256:c51ad05852b58a3b4fd275ee88d183551e745d79ac8239e3da3b98372fe0bb9e
```

Require no running transient bound to v4 identities.

# 11. DB preflight

Before builder capture:

```text
0036 exact terminal state
v2 exact failed-attempt state
v4 run absent
v4 attempt absent
```

Capture application-table counts and authority fingerprints for zero-delta comparison.

Do not require DB pristine.

# 12. production builder

Call `build_stockroom_production` exactly once using:

```text
repository_root = exact HEAD repository
private_runtime_root = v4 root
downloads_root = C:\Users\oracl\Downloads
project_id = aiscc-stockroom-private-capture
requester_identity = aiscc-owner-operator
human_selector_fingerprint = c55280095ff8bbac5ab186e44e3856e6a435da548c1c88b02b66caeba36e8f07
trusted Docker = exact executable
trusted Git = exact executable
accepted Stockroom image provenance
local compatibility secret material only
cancellation bound to v4 run/attempt
```

Require:

```text
authority enrollment fingerprint/count delta:
0

provider security context:
uses persisted docker_spec_fingerprint binding from HEAD 15c9e975ec193526eafa0749fc97321c4d89d713
```

No internal builder direct call.

# 13. prepare + runner

Use only the source-owned public flow:

```text
prepare_capture(...)
StockroomCaptureRunner.run(prepared)
```

Each exactly once.

No manual `PreparedStockroomDriver` construction.
No direct owner-adapter lifecycle orchestration.

No runner retry.

# 14. required normal S1 runtime proof

Success requires actual durable proof:

```text
new v4 WorkRun
new v4 attempt

READY→RUNNING admitted

EXECUTION_STARTED
before first provider/tool side effect

provider ResourceGrant:
ADMITTED / exact

local deterministic provider operation:
bounded / completed

Stockroom tool/process grant:
ADMITTED / exact

Stockroom execution:
bounded / completed

attempt:
EXECUTOR_COMPLETED

RUNNING→ADMISSION_PENDING:
ADMITTED

S1 runtime evidence candidate:
created

S1 evidence:
ADMITTED

evidence-set satisfaction attestation:
present

Judgment:
ACCEPTED

ADMISSION_PENDING→ACCEPTED:
ADMITTED

final WorkRun:
ACCEPTED
```

Report exact actual Workflow state versions and ExecutionAttempt execution_version.

# 15. provider/network boundary

Require:

```text
external OpenAI/provider inference:
0

arbitrary outbound network:
0
```

Only the configured local deterministic provider path is authorized.

# 16. historical isolation

Success or failure must preserve:

```text
0036/v1:
unchanged

1822/v2:
unchanged

v3:
absent / unused
```

No S2/S3/S4.
No HumanResult.
No Replay generation.

# 17. failure behavior

Pre-run blocker:

```text
runner calls = 0
STOP_PRESERVE
```

Runner failure/exception:

```text
runner calls = 1 maximum
no second attempt
no new WorkRun
no DB repair
no manual transition
no destructive cleanup of evidence-bearing v4 state
read-only poststate classification
STOP_PRESERVE
```

# 18. settlement

On success require:

```text
v4 WorkRun ACCEPTED
v4 attempt EXECUTOR_COMPLETED
S1 Judgment ACCEPTED
required evidence/attestation present
no running v4 Stockroom transient
```

Report v4 workspace settlement exactly as source-owned runtime leaves it.

Cleanup residue that is merely local housekeeping is not a substantive blocker unless it violates a security/runtime invariant.

# 19. Git terminal boundary

No tracked mutation is authorized.

Move current Task active→done byte-identically.

Final:

```text
HEAD:
15c9e975ec193526eafa0749fc97321c4d89d713

index:
empty

tracked:
clean

Git-visible untracked exactly 6:
2019 Cycle/Judgment/done Task
current Cycle/Judgment/done Task

legacy 1400:
preserved / ignored / non-owned
```

No commit/push.

# 20. contract review

Exactly 51 rows:

```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_CLEAN
PREDECESSOR_2019_RESULT_ACCEPTED
PREDECESSOR_2019_TRIPLE_EXACT
CURRENT_STATE_HASHES_EXACT
PERSISTED_SOURCE_HASHES_EXACT
LEGACY_1400_ACTIVE_PRESERVED
PYTHON_REPOSITORY_VENV_EXACT
DOCKER_EXECUTABLE_EXACT
NO_SOURCE_TEST_CONFIG_STATE_MUTATION
PRIVATE_POSTGRES_IDENTITY_EXACT
PRIVATE_SECRET_BIND_AND_ACL_EXACT
HISTORICAL_V1_PRESERVED
FAILED_V2_WORKSPACE_FINGERPRINT_EXACT
FAILED_V2_SOURCE_BASIS_COMPARATOR_PASS
FAILED_V2_SOURCE_AGGREGATE_EXACT
FAILED_V2_DURABLE_STATE_EXACT
V3_RESERVED_ROOT_REMAINS_ABSENT
V4_RUNTIME_ROOT_ABSENT_BEFORE_CREATE
V4_RUNTIME_ROOT_CREATED_EMPTY_PRIVATE
STOCKROOM_IMAGE_IDENTITY_EXACT
NO_PREEXISTING_V4_RUN_ATTEMPT
BUILDER_SINGLE_CALL
BUILDER_AUTHORITY_REGISTRATION_ZERO_DELTA
PUBLIC_PREPARE_CAPTURE_SINGLE_CALL
SOURCE_OWNED_RUNNER_SINGLE_CALL
READY_TO_RUNNING_ADMITTED
EXECUTION_STARTED_BEFORE_SIDE_EFFECT
PROVIDER_RESOURCE_GRANT_ADMITTED
LOCAL_PROVIDER_EXECUTION_BOUNDED
TOOL_EXECUTION_BOUNDED
NO_EXTERNAL_PROVIDER_NETWORK
FINAL_EXECUTION_COMPLETED
RUNNING_TO_ADMISSION_PENDING_ADMITTED
S1_RUNTIME_EVIDENCE_ADMITTED
S1_EVIDENCE_ATTESTATION_PRESENT
S1_JUDGMENT_ACCEPTED
ADMISSION_PENDING_TO_ACCEPTED_ADMITTED
FINAL_WORKRUN_ACCEPTED
NO_HUMAN_RESULT_CREATED
NO_S2_S3_S4_EXECUTION
NO_HISTORICAL_LINEAGE_MUTATION
NO_SECOND_RUNNER_OR_BLIND_RETRY
NO_GIT_COMMIT_PUSH
NO_STOCKROOM_TRANSIENT_RESIDUE
PRIVATE_VALUE_EXPORT_SCAN_PASS
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
FINAL_HEAD_UNCHANGED
FINAL_TRACKED_CLEAN_INDEX_EMPTY
FINAL_UNTRACKED_6_EXACT
EXPORT_INTEGRITY_PASS
```

Full S1 success requires:

```text
51 / 51 PASS
```

Blocked/failed results must leave unobserved success rows non-PASS.

# 21. export

Root documents:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
SOURCE_BASELINE_VERIFICATION.md
PRIVATE_RUNTIME_IDENTITY_VERIFICATION.md
HISTORICAL_V1_VERIFICATION.md
FAILED_V2_PRESERVATION_VERIFICATION.md
V3_ABSENCE_VERIFICATION.md
FRESH_V4_ROOT_VERIFICATION.md
PRE_S1_DB_SNAPSHOT.md
BUILDER_VERIFICATION.md
S1_PREPARATION_VERIFICATION.md
S1_EXECUTION_VERIFICATION.md
S1_EVIDENCE_VERIFICATION.md
S1_JUDGMENT_TRANSITION_VERIFICATION.md
POST_S1_DB_SNAPSHOT.md
RUNTIME_SETTLEMENT_VERIFICATION.md
PRIVATE_VALUE_SCAN.md
CONTRACT_REVIEW.md
```

Include exactly the current Cycle/Judgment/done Task as project-relative copies.

Do not export unchanged source/test files.

Generate manifest/member counts from the actual declared set.

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
provider-grant correction:
PERSISTED

fresh S1 v4:
ACCEPTED runtime candidate

historical v1/v2:
preserved

v3:
unused/absent

S2/S3/S4:
NOT_STARTED

canonical state:
unchanged

Browser runtime acceptance:
PENDING

P2-3:
IN_PROGRESS
```
