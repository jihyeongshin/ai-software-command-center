# 작업지시서: P2-3 private S1 ACL-query transport retry

## meta

- task_id: `20260912_1954_aiscc-p2-3-private-s1-acl-query-transport-retry-1`
- created_at: `2026-09-12T19:54:18+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `REWORK / PRIVATE_SCENARIO_EXECUTION`
- evidence_profile: `HIGH_RISK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `ee623c995cf1c24b4a362834f2d6d1fdf71a30cd`
- required_parent: `4096913e9a117bd49bfecdb1ce5ca8de2735d661`
- required_grandparent: `6d41633210f0e556dd4292ee62a8600c6b54215f`
- fresh_ide_executor_chat: `FORBIDDEN`
- executor_session_action: `KEEP_EXISTING_1749_IDE_EXECUTOR_CHAT`
- scenario_authorized: `S1 only`
- success_ceiling: `S1_EXECUTED_ACCEPTED_CANDIDATE / BROWSER_REVIEW_PENDING`

# 0. purpose

1749 stopped before password read/DB/builder/WorkRun because the native ACL child-process stdout did not form valid JSON.

This Task authorizes one bounded retry of the **same S1 attempt** after correcting only that ACL transport.

```text
run_id:
aiscc-p2-3-private-s1-normal-v1-run

attempt_id:
aiscc-p2-3-private-s1-normal-v1-attempt-1
```

No S2/S3/S4.
No manual adapter orchestration.
No Git persistence.

# 1. transport

Continue in the existing 1749 IDE Executor chat.

Do not use the WindowsApps Python alias.

Bootstrap transport may use either:

```text
the already-resolved actual Python 3.12 runtime in the current Executor environment
or
PowerShell/.NET archive APIs
```

Verify Short Prompt ZIP filename/SHA-256 and require exactly three flat members.

Place current Task first:

```text
.aiassistant/tasks/active/20260912_1954_aiscc-p2-3-private-s1-acl-query-transport-retry-1.md
```

Require byte equality and ignored status.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260912_1954_aiscc-p2-3-private-s1-acl-query-transport-blocked-retry-entry-1.cycle.md
SHA-256:
1bb88d04b2e567a9b11ab8fb99449571696a5e039571cef6438fa62bb3fea870

.aiassistant/reports/aiscc/20260912_1954_aiscc-p2-3-private-s1-acl-query-transport-blocker-hold-judgment-1.md
SHA-256:
ee9436791b8595333090eb2a06b295ef4b3b87f620894756fea0a97176ebd25d
```

Bootstrap mismatch:

```text
STOP
no Docker/private-file/DB access
no WorkRun
no report/export
```

# 2. predecessor blocked provenance

Require exact existing predecessor artifacts:

```text
.aiassistant/tasks/done/20260912_1749_aiscc-p2-3-private-s1-normal-scenario-execution-and-capture-1.md
SHA-256:
0668ed1fb71ce57f6b87dacb91c810f7505596eb6efe835841c019f3a2d51ecd

.aiassistant/records/aiscc/cycles/20260912_1749_aiscc-p2-3-cut-c-persisted-private-s1-execution-entry-1.cycle.md
SHA-256:
75fe2a744d010e327ff2d549aa998e2e64e0449735d50eec69a4fd6a183044ad

.aiassistant/reports/aiscc/20260912_1749_aiscc-p2-3-cut-c-persistence-final-acceptance-private-s1-authorization-judgment-1.md
SHA-256:
6457922c2520c2255edf9574b1c68c3ed633c3615e80be5c95c7e04f9e5961ed
```

Do not edit/remove/commit them.

1749 result ZIP Browser identity:

```text
5171f5e967cafdcfc2dc1eb749c1470619c7609add0d0c77ca357525c4faab59
```

The result ZIP itself is not required to exist in the repository.

# 3. repository/state baseline

Require:

```text
branch main
HEAD ee623c995cf1c24b4a362834f2d6d1fdf71a30cd
HEAD^ 4096913e9a117bd49bfecdb1ce5ca8de2735d661
HEAD^^ 6d41633210f0e556dd4292ee62a8600c6b54215f
index empty
tracked worktree clean
```

Canonical state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `7d0c9954b87e945b8c1c3fb66bda2dd54d23d5c3319202ef9fb24aa0ac56f424`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `04ec792c5e6dd4a7c8d2d35b716d1ed1fd569e60bb557532b811bc33dd434946`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `61ae340fa06e3d87d80f3308a240dacc1e0ba132a3b241a2059757830cf6312a`

Before current delivery, Git-visible untracked exactly:

```text
.aiassistant/tasks/done/20260912_1749_aiscc-p2-3-private-s1-normal-scenario-execution-and-capture-1.md
.aiassistant/records/aiscc/cycles/20260912_1749_aiscc-p2-3-cut-c-persisted-private-s1-execution-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_1749_aiscc-p2-3-cut-c-persistence-final-acceptance-private-s1-authorization-judgment-1.md
```

After current Cycle/Judgment placement while current Task is active/ignored:

```text
Git-visible untracked:
5 exact

three predecessor artifacts
current Cycle
current Judgment
```

Any extra/missing/different path:

```text
DIRTY_WORKSPACE_MIXED
→ STOP_WITH_REPORT_EXPORT
```

# 4. source/provenance reuse boundary

1749 already proved current source tracked at HEAD and the source-owned orchestration entrypoint:

```text
aiscc.scenarios.capture_runner.StockroomCaptureRunner.run
async def run(self, prepared: PreparedStockroomDriver) -> StockroomCaptureResult
HEAD blob b627a28e49ca02392ec224a942c27425d0207985
```

Reuse is allowed only after verifying:

```text
HEAD unchanged
tracked worktree clean
the runner blob ID unchanged
all actual runtime source/config files used by this Task equal HEAD bytes
```

Canonical provenance must remain:

```text
stockroom-image-provenance.v1.json:
e19f2b645aee85878bed7c557064bbbd0be746524f394ad88de1d2509c13b64f

stockroom-private-postgres-provisioning.v1.json:
36b9c93515223ade3d74923141fcbe823907b42b81e5d86bf3666a4f02032b54
```

If any source/provenance identity differs:

```text
SOURCE_OR_PROVENANCE_DRIFT
→ STOP_WITH_REPORT_EXPORT
```

# 5. retained environment identity

Revalidate the exact same four resources read-only:

```text
Stockroom image:
sha256:c51ad05852b58a3b4fd275ee88d183551e745d79ac8239e3da3b98372fe0bb9e

PostgreSQL image:
sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94

PostgreSQL container:
aiscc-p2-3-private-postgres-v1
ID 0b50ac47a79e05ac9b88a8f679d04ddc39f729bf1a8e099d149c4c5570b5999c

PostgreSQL volume:
aiscc-p2-3-private-postgres-data-v1
```

Require:

```text
Stockroom inspect fingerprint:
e5350a7236cc496d1d2abec80e52e900616d3935d1e26db1c7e967ca771f1e57

PostgreSQL sanitized projection:
867e744367eb804c30db6269d0700d8679c5aeb1a9b6fb78306ce1b87918c8e7
```

No Docker mutation before source-owned S1 dispatch.

# 6. secret representation

From exact PostgreSQL container inspect select one read-only bind:

```text
Destination:
/run/secrets/postgres_password
```

Require representation class:

```text
DOCKER_DESKTOP_RUN_DESKTOP_MNT_HOST
```

Validate only:

```regex
^/run/desktop/mnt/host/([A-Za-z])/([^\x00]+)$
```

Suffix segments:

```text
non-empty
not "." / ".."
no ":"
no "\"
```

Reversibly map to the native Windows path and require exact reverse mapping except drive-letter case.

Immediately put all raw/normalized path byte representations into the private export denylist.

Never print/hash/export them.

# 7. corrected ACL query transport

This section supersedes only the 1749 ACL child-process transport.

## 7.1 lexical/private object checks before ACL

Require native secret path, its protected parent, and existing runtime root:

```text
absolute
exists
expected file/directory type
not symlink/reparse
all ancestors not symlink/reparse
outside repository
outside Downloads
outside target/export
strict resolution equals the normalized candidate
```

Do not read password yet.

## 7.2 PowerShell command transport

Build a PowerShell **script with no private path literals embedded in the script text**.

Pass the script using:

```text
powershell.exe
-NoLogo
-NoProfile
-NonInteractive
-EncodedCommand
<base64 of script UTF-16LE bytes>
```

Do not use:

```text
-Command -
shell=True
private path in argv
temporary .ps1 file containing private path
```

The script must begin before reading stdin with:

```powershell
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
[Console]::InputEncoding  = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
```

Private path payload is supplied **only via child stdin** as one UTF-8 JSON document:

```json
{"paths":["<private-parent>","<private-secret-file>","<private-runtime-root>"]}
```

The literal values above are explanatory placeholders only; never log/export the real payload.

The PowerShell script must:

```text
read all stdin via [Console]::In.ReadToEnd()
ConvertFrom-Json
require exactly 3 paths
for each: Get-Acl -LiteralPath
translate each access IdentityReference to SID
emit:
  current user SID
  AreAccessRulesProtected
  access-rule SID
  FileSystemRights as Int64
  AccessControlType
  IsInherited
```

No command in the child may mutate ACLs.

Construct the single result object in memory and serialize:

```powershell
$json = $resultObject | ConvertTo-Json -Depth 8 -Compress
[Console]::Out.Write($json)
```

Do not use `Write-Host`.
Do not emit progress/debug text to stdout.

## 7.3 parent Python capture

Invoke child with:

```text
shell=False
stdin = exact UTF-8 JSON payload bytes
capture stdout/stderr
timeout <= 25s
```

Require:

```text
returncode == 0
stderr stripped == empty
stdout non-empty
stdout strict UTF-8 decode PASS
json.loads PASS
top-level object shape exact
path result count == 3
```

Do not retry this ACL subprocess within the same Task if any requirement fails.

On failure:

```text
PRIVATE_ACL_QUERY_TRANSPORT_FAILED
→ STOP_WITH_REPORT_EXPORT
```

Do not export stdout/stderr or private payload.

Pass contract row:

```text
ACL_QUERY_TRANSPORT_EXACT
```

# 8. ACL policy verdict

From the parsed ACL object require the same accepted private policy as 1749:

Allowed effective Allow SIDs only:

```text
current user SID
S-1-5-18
S-1-5-32-544
```

Require private parent:

```text
AreAccessRulesProtected == true
```

For secret file and runtime root, aggregate Allow rights by SID and require each child mask to be a subset of
that SID's parent Allow mask.

Any broader principal/right:

```text
PRIVATE_ACL_BOUNDARY_VIOLATION
→ STOP_WITH_REPORT_EXPORT
```

On PASS:

```text
SECRET_SOURCE_PRIVATE_EXACT
```

Export only booleans and representation class.
Do not export SIDs, paths or raw ACL JSON.

# 9. runtime-root pre-S1 gate

Use the already-created exact runtime root derived from the verified private parent.

Require:

```text
exists
directory
non-reparse
ACL policy PASS
entry count == 0
```

Do not create/delete/recreate it.

Pass:

```text
PRIVATE_RUNTIME_ROOT_EXISTING_EMPTY_EXACT
```

# 10. private DB preflight

Only now read the password into process memory and add exact password/path/URL forms to the export denylist.

Connect to:

```text
127.0.0.1:55432
database aiscc_private_capture
role aiscc_private_capture
migration head 20260901_0008
```

Require the retained Cut C authority envelope exactly:

```text
evidence_requirement_sets 4
evidence_requirements 4
evidence_checkpoints 4
judgment_policies 2
judgment_policy_projections 2

all other application/domain tables 0
```

Require `aiscc-p2-3-private-s1-normal-v1-run` and `aiscc-p2-3-private-s1-normal-v1-attempt-1` are absent from every applicable durable table.

Collision:

```text
S1_RUN_ID_COLLISION
→ STOP
```

No alternate ID.

# 11. builder re-entry

Read current exact:

```text
aiscc.bootstrap.build_stockroom_production
build_stockroom_production_application
PostgresEvidenceRepository.register_authority
JudgmentPolicyAuthority.register
```

Prove existing identical 4 evidence + 2 judgment registrations are idempotent against the actual retained rows.

Require no supersession/revision/new row on same identity.

If ambiguous:

```text
S1_BUILDER_REENTRY_MUTATION_SCOPE_UNCERTAIN
→ STOP before builder
```

Call public `build_stockroom_production(...)` exactly once with the same persisted Cut C parameters and:

```text
cancellation.run_id = aiscc-p2-3-private-s1-normal-v1-run
cancellation.attempt_id = aiscc-p2-3-private-s1-normal-v1-attempt-1
project_id = aiscc-stockroom-private-capture
requester_identity = aiscc-owner-operator
human_selector_fingerprint = c55280095ff8bbac5ab186e44e3856e6a435da548c1c88b02b66caeba36e8f07
```

Use existing private runtime root and canonical typed image provenance.

Immediately recount DB and require zero builder re-entry delta.

# 12. S1 canonical config + orchestration

Derive S1 from current source/config:

```text
scenario_id = SCENARIO_IDS[0]
normal scenario
Judgment terminal = ACCEPTED
evidence basis = SATISFIED_ATTESTATION
reason = STOCKROOM_EVIDENCE_SATISFIED
```

Reconfirm source-owned full-run entrypoint remains exactly:

```text
StockroomCaptureRunner.run(prepared)
```

No manual adapter orchestration.

# 13. prepare and execute exactly one S1

Call `prepare_capture(...)` exactly once for S1 with the fixed run/attempt IDs.

Then call the source-owned `runner.run(prepared)` exactly once.

No second invocation under any outcome.

Authorized source-owned path may perform:

```text
READY creation
attempt creation
READY → RUNNING
security admission
materialization
local deterministic provider/tool
Stockroom Docker runner dispatch
RUNNING → ADMISSION_PENDING
runtime/static evidence admission
evidence-set evaluation
S1 Judgment
ADMISSION_PENDING → ACCEPTED
settlement
```

External provider/network is forbidden.

# 14. success semantics

Require authoritative progression:

```text
READY
→ RUNNING
→ ADMISSION_PENDING
→ ACCEPTED
```

Require terminal state version `4` only after current matrix/source confirms the same four-admission sequence before WorkRun creation.

Execution:

```text
ExecutionStatus = EXECUTOR_COMPLETED
```

Evidence:

```text
same-attempt admitted runtime evidence
exact S1 checkpoint
SATISFIED
genuine EvidenceSetSatisfactionAttestation
```

Judgment:

```text
ACCEPTED
SATISFIED_ATTESTATION
STOCKROOM_EVIDENCE_SATISFIED
```

HumanGate/HumanResult:

```text
none
```

# 15. DB delta / settlement / poststate

After S1 terminal, enumerate all application/domain tables.

Require every new row is transitively bound to the exact S1 run/attempt or its owner-issued refs.

Cut C authority rows remain unchanged.

No S2/S3/S4 rows.

Use source-owned settlement evidence; no broad Docker inventory discovery.

Require no running S1 transient process/container and retained PostgreSQL resources unchanged.

Do not manually clean private runtime output.

# 16. one-shot rule

Before any durable S1 row exists, a blocker still ends this Task.

After any durable `aiscc-p2-3-private-s1-normal-v1-run`/`aiscc-p2-3-private-s1-normal-v1-attempt-1` row exists:

```text
do not rerun
do not select another ID
do not delete/repair/reset DB
do not clean private runtime output
```

Preserve exact state for Browser review.

# 17. Git/repository boundary

No tracked/source/config/state mutation.
No Git add/commit/push/reset/restore/checkout/stash/clean.

At terminal submission move current Task byte-identically:

```text
.aiassistant/tasks/active/20260912_1954_aiscc-p2-3-private-s1-acl-query-transport-retry-1.md
→
.aiassistant/tasks/done/20260912_1954_aiscc-p2-3-private-s1-acl-query-transport-retry-1.md
```

Expected final Git-visible untracked exactly 6:

```text
three 1749 predecessor artifacts
current done Task
current Cycle
current Judgment
```

HEAD remains `ee623c995cf1c24b4a362834f2d6d1fdf71a30cd`.

# 18. private export guard

Before final bundle creation scan every outbound byte against all acquired exact private forms:

```text
raw Docker Source
normalized private path variants
runtime-root absolute path variants
password raw/decoded
credential-bearing DB URL
JSON-escaped private forms
```

Also reject credential URL patterns independently.

Do not export raw ACL stdout/stderr, raw Docker inspect, private path payload or DB URL.

# 19. contract review

Require exactly 38 rows:

```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_CLEAN
PREDECESSOR_1749_ARTIFACTS_EXACT
CURRENT_STATE_HASHES_EXACT
CURRENT_RUNTIME_SOURCE_TRACKED_AT_HEAD
CANDIDATE_PROVENANCE_HASHES_EXACT
RETAINED_ENVIRONMENT_IDENTITY_EXACT
SECRET_SOURCE_REPRESENTATION_EXACT
ACL_QUERY_TRANSPORT_EXACT
SECRET_SOURCE_PRIVATE_EXACT
PRIVATE_RUNTIME_ROOT_EXISTING_EMPTY_EXACT
PRE_BUILDER_AUTHORITY_ROWS_EXACT
PRE_BUILDER_RUNTIME_ROWS_ZERO
S1_RUN_ATTEMPT_IDS_ABSENT
BUILDER_REENTRY_IDEMPOTENCY_SOURCE_PROVED
PUBLIC_PRODUCTION_BUILD_ONCE_PASS
BUILDER_REENTRY_DB_UNCHANGED
S1_SCENARIO_CONFIG_EXACT
S1_ORCHESTRATION_ENTRYPOINT_UNAMBIGUOUS
S1_PREPARE_CAPTURE_EXACT
S1_SOURCE_OWNED_RUNNER_ONLY
S1_READY_RUNNING_TRANSITIONS_EXACT
S1_SECURITY_NETWORK_DENY_EXACT
S1_MATERIALIZATION_PROVENANCE_EXACT
S1_EXECUTION_COMPLETED_EXACT
S1_RUNTIME_EVIDENCE_ADMITTED
S1_EVIDENCE_SET_SATISFIED
S1_JUDGMENT_ACCEPTED_EXACT
S1_FINAL_TRANSITION_ACCEPTED_EXACT
S1_NO_HUMAN_GATE_RESULT
S1_NO_OTHER_SCENARIO_EXECUTION
S1_DB_DELTA_RUN_SCOPED_EXACT
S1_DOCKER_PROCESS_SETTLED
PRIVATE_SECRET_UNCHANGED
RETAINED_ENVIRONMENT_POST_EXACT
NO_SOURCE_STATE_GIT_MUTATION
SECRET_PRIVATE_PATH_EXPORT_SCAN_PASS
EXPORT_INTEGRITY_PASS
```

Require success:

```text
38 / 38 PASS
```

Blocked rows remain `BLOCKED_REQUIRED_EVIDENCE`.

# 20. export

Success root documents exactly 16:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
SOURCE_BASELINE_VERIFICATION.md
RETAINED_ENVIRONMENT_VERIFICATION.md
SECRET_BOUNDARY_VERIFICATION.md
PRIVATE_RUNTIME_ROOT_VERIFICATION.md
BUILDER_REENTRY_VERIFICATION.md
S1_ORCHESTRATION_ENTRYPOINT_VERIFICATION.md
S1_EXECUTION_VERIFICATION.md
S1_EVIDENCE_VERIFICATION.md
S1_JUDGMENT_TRANSITION_VERIFICATION.md
DATABASE_DELTA_VERIFICATION.md
S1_POSTSTATE_VERIFICATION.md
CONTRACT_REVIEW.md
```

Canonical/candidate copies exactly 5:

```text
current Cycle
current Judgment
current done Task
stockroom-image-provenance.v1.json
stockroom-private-postgres-provisioning.v1.json
```

Success:

```text
21 total members
20 non-self manifest rows
one top-level directory
CRC PASS
folder/archive byte equality
TASK.md == current canonical done Task
```

Blocked export may omit genuinely unavailable success-only evidence.

# 21. success ceiling

```text
private S1:
EXECUTED / ACCEPTED_CANDIDATE

WorkRun:
ACCEPTED

Evidence:
SATISFIED / admitted

Judgment:
ACCEPTED

HumanResult:
NONE

S2/S3/S4:
NOT_EXECUTED

Replay:
NOT_GENERATED

S1 Browser admission:
HUMAN_PENDING

Git persistence:
NOT_PERFORMED

P2-3:
IN_PROGRESS
```
