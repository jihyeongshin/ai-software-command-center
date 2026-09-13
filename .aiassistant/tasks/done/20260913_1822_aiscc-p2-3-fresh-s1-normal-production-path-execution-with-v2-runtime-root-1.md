# 작업지시서: P2-3 fresh S1 normal production-path execution with isolated v2 runtime root

## meta

- task_id: `20260913_1822_aiscc-p2-3-fresh-s1-normal-production-path-execution-with-v2-runtime-root-1`
- created_at: `2026-09-13T18:22:27+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `PRIVATE_SCENARIO_EXECUTION / S1_NORMAL`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `c9093e8441de230f9470313d874a33addc75423c`
- required_parent: `af5a9f873f11da1fdf71362abde018a2bed313a4`
- required_grandparent: `d04f6a322f3a3ea49778314e4005b5878b20f121`
- predecessor_persistence_result_sha256: `6369612923befab54a001dcdad2b306ae2d1b2de43c34e197518c908066a800f`
- runtime_mode: `OWNER_SELF_DOGFOOD`
- source_write_authorized: `No`
- state_file_write_authorized: `No`
- Git_commit_push_authorized: `No`
- Docker_runtime_authorized: `Yes / exact Stockroom S1 only`
- private_PostgreSQL_authorized: `Yes / exact retained DB`
- external_provider_network_authorized: `No`
- success_ceiling: `S1_ACCEPTED_RUNTIME_CANDIDATE / BROWSER_REVIEW_PENDING`

# 0. purpose and scope

Execute one **fresh** normal S1 through the current source-owned production path.

Do not reuse 0036.

Fresh identities:

```text
project_id:
aiscc-stockroom-private-capture

run_id:
aiscc-p2-3-private-s1-normal-v2-run

attempt_id:
aiscc-p2-3-private-s1-normal-v2-attempt-1

requester_identity:
aiscc-owner-operator
```

Expected scenario semantic:

```text
READY
→ RUNNING
→ ADMISSION_PENDING
→ ACCEPTED
```

The accepted 0036 lineage remains:

```text
WorkRun FAILED/v3
ExecutionAttempt EXECUTION_FAILED/v2
workspace QUARANTINED
CLOSED_FOR_REUSE
```

# 1. transport and executable rules

Repository:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center
```

Python:

```text
<repository-root>\.venv\Scripts\python.exe
```

Use that fixed relative path only.

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

No Docker PATH discovery.

Git, if the production builder requires a trusted executable:

```text
C:\Program Files\Git\cmd\git.exe
```

Do not use Git for mutation.

# 2. repository baseline

Require:

```text
branch main
HEAD c9093e8441de230f9470313d874a33addc75423c
HEAD^ af5a9f873f11da1fdf71362abde018a2bed313a4
HEAD^^ d04f6a322f3a3ea49778314e4005b5878b20f121
index empty
tracked clean
Git-visible untracked before delivery none
```

Current state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `281bd733624ac87be207f62ed59b99edf0d64cf3b8f3d00e9bc9611fe3179f8c`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `b55eb504c39af0134837f808eef8610b0c54505ee8c597b332f79148ad61d8bd`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `1bb251b5758e8fea1ac260dcace074dcb7e2ff9adf6a96e8699d29c66bea495d`

Persisted source identities that must remain exact:

```text
src/aiscc/scenarios/stockroom_production.py
c41baca3f7cbeaaa18511dd6e94dd5dd5e65d2b282968703f2a4854d86e1b2f4

src/aiscc/runtime/stockroom_workspace.py
1b8366b5c5a6e9054dbd65ef36cd09808074c88ccf6c7ad060a9a76a488efaab

src/aiscc/bootstrap.py
745b58da26ec300286ed69d1a7477b21afeb7625ec43e7f422560a657bc1c115
```

Preserve non-owned ignored legacy Task:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
SHA-256 52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

After current Cycle/Judgment placement with current Task active/ignored:

```text
Git-visible untracked exactly 2
```

# 3. mandatory current-source semantic gate

Before Docker/private DB mutation, inspect current HEAD source.

Require all:

```text
1. StockroomCaptureRunner.run is the single source-owned public scenario runner.
2. READY→RUNNING occurs before materialization/provider execution.
3. the prepared attempt transitions to EXECUTION_STARTED after RUNNING and before the first execution side effect.
4. S1 RUNNING→ADMISSION_PENDING occurs before submit_runtime_evidence.
5. StockroomCaptureOwnerAdapter.submit_runtime_evidence validates ADMISSION_PENDING,
   not RUNNING, for the post-transition evidence submission.
6. S1 Judgment path selects ACCEPTED only from admitted S1 evidence/attestation.
7. final state transition is ADMISSION_PENDING→ACCEPTED.
```

If any source semantic differs, STOP with `POLICY_CONFLICT_INVESTIGATION_REQUIRED` before private mutation.

Do not patch source in this Task.

# 4. retained private environment

Using exact retained PostgreSQL container inspect, require:

```text
container:
aiscc-p2-3-private-postgres-v1

container ID:
0b50ac47a79e05ac9b88a8f679d04ddc39f729bf1a8e099d149c4c5570b5999c

PostgreSQL image:
sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94

volume:
aiscc-p2-3-private-postgres-data-v1

endpoint:
127.0.0.1:55432

database/role:
aiscc_private_capture
```

Secret bind:

```text
Destination = /run/secrets/postgres_password
Type = bind
RW = false
```

Reconstruct the native secret parent using the already accepted reversible Docker Desktop mapping. No path search.

Require:

```text
secret + parent exact
no reparse
protected/private ACL
no repository/Downloads overlap
```

Never print/export/hash the secret value or private absolute path.

# 5. historical v1 preservation gate

Derive historical root only as:

```text
<verified secret parent> / aiscc-p2-3-private-runtime-v1
```

Using `StockroomRestartSafetySettlement` read-only inspection for 0036 require:

```text
active workspace exists:
false

matching quarantine:
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

Do not rename/delete/change v1 or its quarantine.

# 6. fresh v2 root

Fresh root:

```text
<verified secret parent> / aiscc-p2-3-private-runtime-v2
```

Require it does **not** exist before this Task.

If it already exists, STOP. Do not inspect/use/delete it as a fallback.

After all private parent/ACL checks pass, create exactly this one directory.

Require immediately after creation:

```text
directory exists
empty
no reparse
resolved path exact
ACL no broader than verified private parent
no repository/Downloads overlap
```

No other host directory creation.

# 7. DB preflight

Read the retained DB with the exact secret.

Require migration:

```text
20260901_0008
```

Require historical 0036 remains exactly terminal:

```text
WorkRun FAILED/v3
attempt EXECUTION_FAILED/v2
abort reason INVALID_HISTORY_SIDE_EFFECT_BEFORE_EXECUTION_START
```

Require absent:

```text
run_id aiscc-p2-3-private-s1-normal-v2-run
attempt_id aiscc-p2-3-private-s1-normal-v2-attempt-1
```

Capture current application-table counts and exact authority enrollment identities/fingerprints for comparison.

Do not require database pristine/empty.

# 8. Stockroom image / transient preflight

Require image:

```text
sha256:c51ad05852b58a3b4fd275ee88d183551e745d79ac8239e3da3b98372fe0bb9e
```

Require no running transient Stockroom container belonging to this fresh run/attempt.

# 9. build production application exactly once

Use the public production builder exactly once with:

```text
repository_root = exact repository
private_runtime_root = fresh v2 root
downloads_root = C:\Users\oracl\Downloads
project_id = aiscc-stockroom-private-capture
requester_identity = aiscc-owner-operator
human_selector_fingerprint = c55280095ff8bbac5ab186e44e3856e6a435da548c1c88b02b66caeba36e8f07
trusted Docker = exact executable above
trusted Git = exact executable above
accepted Stockroom image provenance
source-owned local compatibility secret material only
cancellation bound to fresh run/attempt
```

Use `build_stockroom_production`.

Do not call the internal builder directly.

After builder construction require:

```text
private_runtime_root == fresh v2 root
workspace bound to fresh v2 root
Docker runner not dispatched
all expected authority owners present
authority registration rows/fingerprints unchanged from pre-builder snapshot
```

Builder idempotent authority registration must be zero-delta.

# 10. source-owned S1 preparation and execution

Do not manually instantiate `PreparedStockroomDriver`.
Do not call owner-adapter lifecycle methods directly.

Use the current public/source-owned preparation API (`prepare_capture`) for S1 with the exact fresh run/attempt identities, then call:

```text
StockroomCaptureRunner.run(prepared)
```

exactly once.

Derive the exact expected DB mutation envelope from current source/config **before** runner invocation. Do not invent hardcoded row counts where the current source/config owns them.

No automatic second runner invocation.

# 11. required runtime semantics

Require actual durable evidence that the source-owned path did all of the following:

```text
new WorkRun created with exact fresh run identity
fresh attempt created with exact attempt identity
READY→RUNNING admitted
attempt EXECUTION_STARTED before materialization/provider/tool side effect
bounded Stockroom materialization/execution occurred
attempt terminal execution status = EXECUTOR_COMPLETED
RUNNING→ADMISSION_PENDING admitted
S1 runtime evidence candidate submitted through source-owned adapter
S1 evidence admitted
S1 evidence-set satisfaction attestation exists
S1 Judgment = ACCEPTED
ADMISSION_PENDING→ACCEPTED admitted
final WorkRun = ACCEPTED
```

Expected final WorkRun state version is source-derived from the normal four-state path; report the actual exact version.

Do not substitute process exit/output for admitted evidence/Judgment/state.

# 12. network/provider boundary

This private S1 uses the configured local deterministic/provider-tool path already accepted for Stockroom capture.

Require:

```text
external OpenAI/provider inference:
0

arbitrary outbound network:
0
```

Docker runtime activity for the exact Stockroom execution is allowed.

# 13. scenario isolation

Forbidden:

```text
S2
S3
S4
HumanResult
Replay generation
public deployment
source modification
config modification
test modification
canonical state modification
Git add/commit/push
0036 mutation
v1 quarantine mutation
```

# 14. post-run settlement

After runner returns or raises, inspect durable DB and Docker state.

Success requires:

```text
fresh S1 WorkRun ACCEPTED
fresh attempt EXECUTOR_COMPLETED
S1 Judgment ACCEPTED
required evidence/attestation present
no HumanResult
no S2/S3/S4 records attributable to this Task
no running fresh Stockroom transient
0036 durable state unchanged
v1 quarantine unchanged
```

Report the fresh v2 workspace/cleanup outcome exactly as observed. Do not turn cleanup residue into ACCEPTED if the source-owned security/cleanup verdict is failed.

# 15. failure behavior

Any named blocker before runner:

```text
STOP_PRESERVE
runner calls = 0
```

Any runner exception:

```text
do not call runner again
do not create another run/attempt
do not DB-repair
do not manually transition
read-only classify actual durable state
STOP_PRESERVE
```

No blind retry.

# 16. Git boundary

No tracked modifications are authorized.

At terminal report preparation:

```text
HEAD remains c9093e8441de230f9470313d874a33addc75423c
index empty
tracked clean
current Task active→done byte-identically
Git-visible untracked exactly 3:
current Cycle
current Judgment
current done Task
```

Legacy 1400 remains ignored/non-owned.

No commit/push.

# 17. contract review

Require exactly 44 rows:

```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_CLEAN
CURRENT_STATE_HASHES_EXACT
LEGACY_1400_ACTIVE_PRESERVED
PYTHON_REPOSITORY_VENV_EXACT
DOCKER_EXECUTABLE_EXACT
CURRENT_SOURCE_TRACKED_AT_HEAD
S1_SOURCE_SEMANTIC_GATE_PASS
PRIVATE_POSTGRES_IDENTITY_EXACT
PRIVATE_SECRET_BIND_AND_ACL_EXACT
HISTORICAL_V1_QUARANTINE_PRESERVED
V2_RUNTIME_ROOT_ABSENT_BEFORE_CREATE
V2_RUNTIME_ROOT_CREATED_EMPTY_PRIVATE
STOCKROOM_IMAGE_IDENTITY_EXACT
NO_PREEXISTING_FRESH_S1_RUN
NO_PREEXISTING_FRESH_S1_ATTEMPT
0036_TERMINAL_STATE_PRESERVED
BUILDER_SINGLE_CALL
BUILDER_AUTHORITY_REGISTRATION_ZERO_DELTA
PUBLIC_PREPARE_CAPTURE_SINGLE_CALL
SOURCE_OWNED_RUNNER_SINGLE_CALL
NEW_WORKRUN_IDENTITY_EXACT
NEW_ATTEMPT_IDENTITY_EXACT
READY_TO_RUNNING_ADMITTED
EXECUTION_STARTED_BEFORE_SIDE_EFFECT
PROVIDER_TOOL_EXECUTION_BOUNDED
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
NO_0036_REUSE_OR_MUTATION
NO_SOURCE_TEST_STATE_GIT_MUTATION
NO_GIT_COMMIT_PUSH
NO_STOCKROOM_TRANSIENT_RESIDUE
PRIVATE_VALUE_EXPORT_SCAN_PASS
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
FINAL_UNTRACKED_3_EXACT
EXPORT_INTEGRITY_PASS
```

Success requires:

```text
44 / 44 PASS
```

For a blocked/failed execution, do not mark unobserved success postconditions PASS.

# 18. export

Root documents:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
SOURCE_SEMANTIC_GATE_VERIFICATION.md
PRIVATE_RUNTIME_IDENTITY_VERIFICATION.md
HISTORICAL_V1_PRESERVATION_VERIFICATION.md
FRESH_V2_ROOT_VERIFICATION.md
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

Include exactly these current canonical copies:

```text
current Cycle
current Judgment
current done Task
```

Generate the manifest from the actual declared member set; do not hand-maintain an independent member-count constant.

Require:

```text
one top-level folder
manifest SHA-256 + byte size exact
CRC PASS
TASK.md == canonical done Task
no private absolute path
no password
no credential URL
no raw Docker/ACL/DB dump
```

# 19. success ceiling

```text
fresh S1:
ACCEPTED runtime candidate

0036:
terminal / preserved / not reused

historical v1:
quarantine preserved

fresh v2:
source-owned runtime outcome recorded

S2/S3/S4:
NOT_STARTED

Browser acceptance:
PENDING

P2-3:
IN_PROGRESS
```
