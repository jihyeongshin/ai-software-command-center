# 작업지시서: P2-3 provider-grant fix persistence and fresh S1 v3 runtime retry

## meta

- task_id: `20260913_2019_aiscc-p2-3-provider-grant-fix-persistence-and-fresh-s1-v3-runtime-retry-1`
- created_at: `2026-09-13T20:19:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `SOURCE_PERSISTENCE + PRIVATE_SCENARIO_EXECUTION / S1_NORMAL_RETRY`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `c9093e8441de230f9470313d874a33addc75423c`
- required_base_parent: `af5a9f873f11da1fdf71362abde018a2bed313a4`
- required_base_grandparent: `d04f6a322f3a3ea49778314e4005b5878b20f121`
- accepted_1851_result_zip_sha256: `ea24a2d44a454558b5b845313d5207d6240a5507656048882ace5842d41c6e47`
- source_commit_authorized: `Yes / exact 9 paths`
- private_runtime_authorized: `Yes / only after successful source commit`
- canonical_state_write_authorized: `No`
- second_runtime_attempt_authorized: `No`
- push_authorized: `No`
- success_ceiling: `FRESH_S1_V3_ACCEPTED_RUNTIME_CANDIDATE / BROWSER_REVIEW_PENDING`

# 0. purpose

This Task intentionally combines two sequential operations to reduce submission-path turns:

```text
A. persist the Browser-accepted 1851 source candidate
B. execute exactly one new S1 normal run against that persisted source
```

B is forbidden unless A completes exactly.

# 1. executables

Repository:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center
```

Python:

```text
<repository-root>\.venv\Scripts\python.exe
```

Use only that fixed relative interpreter.

Forbidden:

```text
python
py
WindowsApps
PATH Python discovery
repository-external Python
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

# 2. exact initial Git baseline

Require:

```text
branch main
HEAD c9093e8441de230f9470313d874a33addc75423c
HEAD^ af5a9f873f11da1fdf71362abde018a2bed313a4
HEAD^^ d04f6a322f3a3ea49778314e4005b5878b20f121
index empty
tracked dirt exactly 3
Git-visible untracked exactly 6
```

Tracked dirt must be exactly:

- `src/aiscc/scenarios/stockroom_production.py`  `335678daa9fcd4dd9a4b1a2fc4a53876086cab0d555edb7c413466c531dd6d75`
- `tests/integration/scenarios/test_stockroom_binding.py`  `9bd991b77f711a46662262e12f1471b0b78ba1cc6151b3f6a04650ea68bbf439`
- `tests/unit/providers/test_stockroom_tool.py`  `8acda82618b05364e8a7d31ee1b8f6ed28f1bbf5c6a680dda7e8ffc745466544`

Git-visible untracked must be exactly:

- `.aiassistant/records/aiscc/cycles/20260913_1822_aiscc-p2-3-fresh-s1-normal-production-path-entry-1.cycle.md`  `700c3aef2a050c2850d72e65acf3936d0c1af2cfd702b89d4c1638e02c13b466`
- `.aiassistant/reports/aiscc/20260913_1822_aiscc-p2-3-invalid-history-persistence-accepted-fresh-s1-authorization-judgment-1.md`  `f2e6f62074716ddabe97039d76b91ed73e7d4fed5c80c9094fc846807d8d34d7`
- `.aiassistant/tasks/done/20260913_1822_aiscc-p2-3-fresh-s1-normal-production-path-execution-with-v2-runtime-root-1.md`  `9f4a740b684137752d868c02f5dc8c63a25c1cfa45925f994c15fec4ddd7afd0`
- `.aiassistant/records/aiscc/cycles/20260913_1851_aiscc-p2-3-fresh-s1-provider-resource-grant-denial-rework-entry-1.cycle.md`  `940b80a5ca50444ef260a1d4e215729c5dc1687b790d8ed632b8bb3bc05625e9`
- `.aiassistant/reports/aiscc/20260913_1851_aiscc-p2-3-fresh-s1-runtime-security-denial-rework-judgment-1.md`  `9b8ffee6da925def976487a4683cd11fff4922f826fa63f5ed17941f6f7c21db`
- `.aiassistant/tasks/done/20260913_1851_aiscc-p2-3-fresh-s1-provider-resource-grant-denial-targeted-source-rework-1.md`  `7d743b2286dc7e10b65b0a34c6999475fd67c307d0ef38a249545f13f5954f67`

Current canonical state hashes must remain:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `281bd733624ac87be207f62ed59b99edf0d64cf3b8f3d00e9bc9611fe3179f8c`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `b55eb504c39af0134837f808eef8610b0c54505ee8c597b332f79148ad61d8bd`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `1bb251b5758e8fea1ac260dcace074dcb7e2ff9adf6a96e8699d29c66bea495d`

Preserve ignored non-owned legacy:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
SHA-256 52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

After current Cycle/Judgment placement while current Task is active/ignored:

```text
Git-visible untracked exactly 8
```

Any mismatch → STOP before Git staging or private runtime access.

# 3. accepted source candidate semantics

The persisted candidate must retain exactly the 1851 accepted semantics:

```text
production context factory binds inputs.docker_spec_fingerprint
for provider/secret security context

nonempty caller-supplied conflicting resolved_spec_fingerprint
→ AuthorityConflictError

P1-3 evaluator unchanged
ResourceGrant exact equality unchanged
provider/tool/secret domains remain separate
no wildcard/prefix/contains grant behavior
```

Before commit, verify the exact three candidate hashes from section 2.

# 4. Commit A — source correction persistence

Stage exactly 9 paths:

```text
3 accepted candidate source/test paths
+ 6 exact 1822/1851 Cycle/Judgment/done Task artifacts
```

Do not stage:

```text
current Cycle
current Judgment
current active Task
canonical state files
legacy 1400 active Task
ignored report artifacts
```

Commit message exactly:

```text
fix(aiscc): bind stockroom provider security context
```

Require:

```text
Commit A parent = c9093e8441de230f9470313d874a33addc75423c
Commit A changed paths = exact 9
```

After Commit A:

```text
HEAD = Commit A
index empty
tracked clean
Git-visible untracked exactly 2:
current Cycle
current Judgment
```

Current Task remains active/ignored.

If Commit A validation fails → STOP. Do not access private runtime.

# 5. no canonical state mutation

Do not modify:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

Canonical state reconciliation is deferred until Browser reviews this runtime result.

# 6. exact fresh subject

Fresh v3 only:

```text
project_id:
aiscc-stockroom-private-capture

run_id:
aiscc-p2-3-private-s1-normal-v3-run

attempt_id:
aiscc-p2-3-private-s1-normal-v3-attempt-1

requester_identity:
aiscc-owner-operator

scenario:
stockroom-s1-normal

RuntimeMode:
OWNER_SELF_DOGFOOD
```

Never reuse:

```text
0036 lineage
1822 v2 run/attempt
v1 root
v2 root
```

# 7. retained private environment preflight

Use the exact retained PostgreSQL identity:

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

Secret mount must remain:

```text
Destination=/run/secrets/postgres_password
Type=bind
RW=false
```

Reconstruct the private parent only through the previously accepted reversible Docker Desktop mapping.

Require:

```text
no reparse
private/protected ACL
no repository/Downloads overlap
```

Never export private absolute paths, password, DB URL, raw inspect, or ACL body.

# 8. preserve v1 and failed v2

Historical v1:

```text
0036 WorkRun FAILED/v3
0036 attempt EXECUTION_FAILED/v2
one quarantine
20 objects / 14 files
fingerprint 18433a8d92affe915d01e3bb1265b387a07dc6478e09c92306854908ab396068
```

Require read-only match and do not mutate.

1822 v2 lineage:

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

v2 root:
retained / one materialized run workspace
source verified files:
14

source aggregate:
be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d
```

Read-only verify durable identity and bounded workspace presence. Do not adopt, rename, clean, retry, transition, or repair it.

# 9. create fresh v3 root

Fresh root is exactly:

```text
<verified private parent> / aiscc-p2-3-private-runtime-v3
```

Require absent before creation.

If it exists → STOP. Do not reuse/delete it.

Create that one directory only after sections 7–8 pass.

Require:

```text
empty
resolved exact
no reparse
ACL no broader than private parent
no repository/Downloads overlap
```

# 10. DB preflight

Before builder:

```text
0036 exact terminal state present
1822 v2 exact failed-attempt state present
v3 run absent
v3 attempt absent
```

Snapshot application-table counts and authority-registration fingerprints for builder zero-delta proof.

Do not require DB pristine.

# 11. Stockroom image

Require exact retained image:

```text
sha256:c51ad05852b58a3b4fd275ee88d183551e745d79ac8239e3da3b98372fe0bb9e
```

Require no running Stockroom transient for v3 identities.

# 12. production builder

Call public `build_stockroom_production` exactly once with:

```text
repository_root = exact repository at Commit A
private_runtime_root = v3 root
downloads_root = C:\Users\oracl\Downloads
project_id = aiscc-stockroom-private-capture
requester_identity = aiscc-owner-operator
human_selector_fingerprint = c55280095ff8bbac5ab186e44e3856e6a435da548c1c88b02b66caeba36e8f07
trusted Docker = exact executable
trusted Git = exact executable
accepted Stockroom image provenance
local compatibility secret material only
cancellation bound to v3 run/attempt
```

Require authority-registration fingerprint/count zero delta.

No direct internal builder call.

# 13. preparation and runner

Use only the public/source-owned path:

```text
prepare_capture(...)
StockroomCaptureRunner.run(prepared)
```

Each exactly once.

No manual owner lifecycle calls.

Before runner, derive the expected successful S1 mutation envelope from current Commit A source/config. Do not invent fixed DB row totals where source owns them.

No second runner call under any outcome.

# 14. required runtime proof

Success requires actual durable proof of the normal chain:

```text
new v3 WorkRun created
new v3 attempt created
READY→RUNNING admitted
EXECUTION_STARTED before first execution side effect

provider ResourceGrant admitted with exact server-owned provider scope
local deterministic provider path executed within configured finite bounds

Stockroom tool/process operation admitted with exact TOOL/process resource binding
Stockroom container/tool execution completed within configured finite bounds

execution attempt → EXECUTOR_COMPLETED

RUNNING→ADMISSION_PENDING admitted

S1 runtime evidence candidate created
evidence admitted
evidence-set satisfaction attestation present

Judgment ACCEPTED

ADMISSION_PENDING→ACCEPTED admitted
final WorkRun ACCEPTED
```

Report exact actual state versions and execution version.

Do not substitute process output for admitted evidence or Judgment.

# 15. network boundary

Require:

```text
external OpenAI/provider inference:
0

arbitrary outbound network:
0
```

The local deterministic provider is the authorized S1 provider path.

# 16. failure behavior

Any pre-run blocker:

```text
runner calls 0
STOP_PRESERVE
```

Any runner STOP/exception/failure:

```text
no runner retry
no alternate attempt
no new WorkRun
no DB repair
no manual transition
no v3 cleanup that would destroy evidence
read-only classify durable state
STOP_PRESERVE
```

Source Commit A remains valid and must not be reset/reverted automatically.

# 17. post-run settlement

Success requires:

```text
v3 WorkRun ACCEPTED
v3 attempt EXECUTOR_COMPLETED
S1 Judgment ACCEPTED
required evidence/attestation present
no HumanResult
no S2/S3/S4
0036 unchanged
v2 unchanged
no running v3 Stockroom transient
```

Report source-owned workspace settlement exactly.

Non-blocking local residue must not invalidate an otherwise accepted runtime unless it violates a security/runtime invariant.

# 18. Git terminal boundary

After runtime/reporting, no source/test/config/state mutation is allowed.

Move current Task active→done byte-identically.

Final require:

```text
HEAD = Commit A
index empty
tracked clean

Git-visible untracked exactly 3:
current Cycle
current Judgment
current done Task

legacy 1400:
preserved / ignored / non-owned
```

No push.

# 19. contract review

Exactly 49 rows:

```text
TRANSPORT_PACKAGE_EXACT
BASE_HEAD_AND_DIRT_EXACT
PREDECESSOR_1822_1851_ARTIFACTS_EXACT
CURRENT_STATE_HASHES_EXACT
LEGACY_1400_ACTIVE_PRESERVED
PYTHON_REPOSITORY_VENV_EXACT
SOURCE_CANDIDATE_HASHES_EXACT
COMMIT_A_STAGE_SET_EXACT_9
COMMIT_A_PARENT_EXACT
COMMIT_A_MESSAGE_EXACT
COMMIT_A_CHANGED_PATHS_EXACT_9
POST_COMMIT_TRACKED_CLEAN
NO_CANONICAL_STATE_MUTATION
PRIVATE_POSTGRES_IDENTITY_EXACT
PRIVATE_SECRET_BIND_AND_ACL_EXACT
HISTORICAL_V1_PRESERVED
FAILED_V2_LINEAGE_PRESERVED
V3_RUNTIME_ROOT_ABSENT_BEFORE_CREATE
V3_RUNTIME_ROOT_CREATED_EMPTY_PRIVATE
STOCKROOM_IMAGE_IDENTITY_EXACT
NO_PREEXISTING_V3_RUN_ATTEMPT
BUILDER_SINGLE_CALL
BUILDER_AUTHORITY_REGISTRATION_ZERO_DELTA
PUBLIC_PREPARE_CAPTURE_SINGLE_CALL
SOURCE_OWNED_RUNNER_SINGLE_CALL
EXECUTION_STARTED_BEFORE_SIDE_EFFECT
PROVIDER_RESOURCE_GRANT_ADMITTED
LOCAL_PROVIDER_EXECUTION_BOUNDED
TOOL_EXECUTION_BOUNDED
NO_EXTERNAL_PROVIDER_NETWORK
RUNNING_TO_ADMISSION_PENDING_ADMITTED
S1_RUNTIME_EVIDENCE_ADMITTED
S1_EVIDENCE_ATTESTATION_PRESENT
S1_JUDGMENT_ACCEPTED
ADMISSION_PENDING_TO_ACCEPTED_ADMITTED
FINAL_WORKRUN_ACCEPTED
FINAL_EXECUTION_COMPLETED
NO_HUMAN_RESULT_CREATED
NO_S2_S3_S4_EXECUTION
NO_0036_OR_V2_REUSE_MUTATION
NO_SOURCE_MUTATION_AFTER_COMMIT
NO_SECOND_RUNNER_OR_BLIND_RETRY
NO_GIT_PUSH
NO_STOCKROOM_TRANSIENT_RESIDUE
PRIVATE_VALUE_EXPORT_SCAN_PASS
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
FINAL_HEAD_IS_COMMIT_A
FINAL_UNTRACKED_CURRENT_TRIPLE_EXACT
EXPORT_INTEGRITY_PASS
```

Successful S1 requires:

```text
49 / 49 PASS
```

Blocked/failed runtime must leave unobserved success rows non-PASS.

# 20. export

Root documents:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
SOURCE_PERSISTENCE_VERIFICATION.md
COMMIT_A_PATHS.md
PRIVATE_RUNTIME_IDENTITY_VERIFICATION.md
HISTORICAL_V1_V2_PRESERVATION_VERIFICATION.md
FRESH_V3_ROOT_VERIFICATION.md
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

Include byte-preserving copies of:

```text
current Cycle
current Judgment
current done Task
the exact three product/test paths persisted by Commit A
```

Generate manifest and member counts from the actual declared set; no independent hand-maintained total.

Require:

```text
one top-level
CRC PASS
manifest SHA/size exact
TASK.md == canonical done Task
private-value/path scan PASS
```

# 21. success ceiling

```text
provider-grant source correction:
PERSISTED

fresh S1 v3:
ACCEPTED runtime candidate

0036/v1:
preserved

1822/v2:
preserved / not reused

S2/S3/S4:
NOT_STARTED

canonical state reconciliation:
NOT_PERFORMED

Browser runtime acceptance:
PENDING

P2-3:
IN_PROGRESS
```
