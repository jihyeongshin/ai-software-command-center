# 작업지시서: P2-3 private S1 normal scenario execution and capture retry

## meta

- task_id: `20260913_0012_aiscc-p2-3-private-s1-normal-scenario-execution-and-capture-retry-1`
- created_at: `2026-09-13T00:12:33+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `PRIVATE_SCENARIO_EXECUTION`
- evidence_profile: `HIGH_RISK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `6cc4f988f56f5cbf32e57f4b5e9a52a180044c36`
- required_parent: `35cee94a92d1f12801576ef48038196922687f42`
- required_grandparent: `ee623c995cf1c24b4a362834f2d6d1fdf71a30cd`
- python_executable: `C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe`
- scenario_authorized: `S1 only`
- success_ceiling: `S1_EXECUTED_ACCEPTED_CANDIDATE / BROWSER_REVIEW_PENDING`

# 0. purpose

Execute the first actual private Stockroom S1 normal scenario after the producer-provenance source correction has been
FINAL_ADMITTED / PERSISTED.

Authorize exactly one attempt:

```text
scenario_id:
current canonical SCENARIO_IDS[0]

run_id:
aiscc-p2-3-private-s1-normal-v1-run

attempt_id:
aiscc-p2-3-private-s1-normal-v1-attempt-1
```

Expected semantic terminal:

```text
WorkRun:
ACCEPTED

Evidence:
SATISFIED

Judgment:
ACCEPTED / SATISFIED_ATTESTATION

S2/S3/S4:
NOT_EXECUTED
```

Use the source-owned orchestration only.

# 1. Python / transport

Use only:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe
```

Forbidden:

```text
python
py
WindowsApps Python alias
PATH Python discovery
```

Verify Short Prompt ZIP filename/SHA-256 and require exactly three flat safe members.

Place current Task first:

```text
.aiassistant/tasks/active/20260913_0012_aiscc-p2-3-private-s1-normal-scenario-execution-and-capture-retry-1.md
```

Require byte equality and ignored status.

Then place:

```text
.aiassistant/records/aiscc/cycles/20260913_0012_aiscc-p2-3-private-s1-source-correction-persisted-execution-entry-1.cycle.md
SHA-256:
ff0ca7f1752fd3a49306b660b1823b57b194a60b1d58c2341867e9c9b75dc702

.aiassistant/reports/aiscc/20260913_0012_aiscc-p2-3-private-s1-source-correction-persisted-execution-authorization-judgment-1.md
SHA-256:
568268a48fcda0145b549f9b26a5baf4287b8fb7f4937c3bfd9b2db60b5836a8
```

Bootstrap mismatch:

```text
STOP
no Docker/private-file/DB access
no WorkRun
no report/export
```

# 2. repository preflight

Require:

```text
branch:
main

HEAD:
6cc4f988f56f5cbf32e57f4b5e9a52a180044c36

HEAD^:
35cee94a92d1f12801576ef48038196922687f42

HEAD^^:
ee623c995cf1c24b4a362834f2d6d1fdf71a30cd

index:
empty

tracked worktree:
clean

Git-visible untracked before delivery:
none
```

Canonical state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `02b7a77d3f29d7ee3878157470020ab83b377ba0343867ab81ec6e82d1a9190b`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `9ca1b1a24f3f73c2f81d3342442cf0462b58fecdba2dbccc33509b0d4039ab71`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `7315a943ad4ed82757f4398d9613f3a6f773755f3496fa1e8fa816123422ea84`

After current Cycle/Judgment placement while current Task is active/ignored:

```text
Git-visible untracked:
2 exact

current Cycle
current Judgment
```

Unexpected dirt/path:

```text
DIRTY_WORKSPACE_MIXED
→ STOP_WITH_REPORT_EXPORT
```

# 3. accepted source authority

Require the persisted producer-provenance correction byte-exact:

- `src/aiscc/workflow/guards.py`  `e7509199bca3b901c7a04b4e5a1d8c23bab217eca5b78a3b9319d10300993cab`
- `src/aiscc/persistence/repository.py`  `ab00af3dd871477da74b83275258aa48a47ba9a7081aad0154a808b6e4f1c089`
- `src/aiscc/scenarios/capture_runner.py`  `0dab27e0ce9ce2da7953188bcb26f288b637a4ba524141be2800b08302a59b18`
- `src/aiscc/scenarios/stockroom_production.py`  `1ca58848a837e1130229c7a0e085df999d04c6041c77bb61098185d342ff14a0`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`  `02f5835a726f22d81d9d631f120c9d7c9b3c1311cc23ed93db5d3abd9a57f41e`
- `tests/unit/scenarios/test_contracts.py`  `bd56e823f4ae15e82233d2cbd50e2d20d13176dc88c0ee00c7ddab8de752b0d7`

Require the following unchanged accepted source/config/runtime baselines byte-exact:

- `src/aiscc/bootstrap.py`  `745b58da26ec300286ed69d1a7477b21afeb7625ec43e7f422560a657bc1c115`
- `src/aiscc/runtime/docker.py`  `284a3920f13f93928cc61420913506ed38af4e8f4d4e0e1f52d52c9074fa0753`
- `src/aiscc/runtime/stockroom_image.py`  `06e8d85e449a336392b73d9dec9915cd32d776688575a64030024609b08cec0e`
- `src/aiscc/providers/stockroom_tool.py`  `c5c925df000656ce32f65f4742f9a6936c2364d7d58eb92750966d8a8826e075`
- `src/aiscc/providers/local_deterministic.py`  `92ec8ba5553b05fe55fdbac30ab2dde8f57597c1055060a2f786dadd47f1c21a`
- `src/aiscc/scenarios/composition.py`  `a5f7ecb0d1bd9274f07094cbe3a4315098048c468472162e0ad84372fe6c50d3`
- `config/providers/stockroom-tools.v2.toml`  `16015a97a00098e26f89a2972c87fd5ce0f4516c1afdf2bc20126fe6d1c61385`
- `config/providers/stockroom-owner-profiles.v2.toml`  `3f20d2d1ac4dd45709c47fc6572db4b97d6c33e0bebf02c6fd489dd9adbd022a`
- `examples/synthetic-stockroom/Dockerfile`  `94f71d8bf4b2f87e678e1a379dead19b7a850cf4522ec835bf6455f95d72b27a`
- `examples/synthetic-stockroom/.dockerignore`  `99637a64da3b1b13bbf9a52459098d07bbc865aca11d004c89c3ee48965849f9`
- `examples/synthetic-stockroom/IMAGE_PROVENANCE.md`  `166cfec29db4f46477b0117fae85a6a937343e3fb019a9b668b223b2eea8bae3`
- `tests/unit/runtime/test_stockroom_docker_settlement.py`  `f7a33975072737417b3a922d4acd44e59be29547ceb87c864e24647d46236b19`
- `tests/unit/runtime/test_stockroom_image.py`  `e900bf8db350762655a167def704989527928cef575f69e740b013e5bfa4cee7`
- `tests/unit/providers/test_stockroom_tool.py`  `e33b966cf5d575b7e55cd1ced2f3bfcd805833c08c1c66d6c650b693313c285d`
- `tests/unit/providers/test_local_deterministic.py`  `daa58e09dd3e81f2ba4a6edad236685c34a7c63852419ad3188aef51c8fe6209`
- `tests/unit/scenarios/test_owner_composition.py`  `bfbae533d8453bef3940b1b652c5688b3b375b7e0fa40ae03e3196902888d652`
- `tests/integration/scenarios/test_stockroom_binding.py`  `3979ff742a2c82752a7fbccb095b4ab8a4ed4915331ba4ec9d09cfa24aa3d4cf`

For every additional source/config file actually read for runtime proof:

```text
tracked by Git
worktree blob == HEAD blob
index/worktree clean
```

No source/config/test/state mutation is authorized.

# 4. canonical/read scope

Read applicable exact governance and current state:

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md
.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_SECURITY_SANDBOX.md
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md
.aiassistant/rules/AISCC_HUMAN_GATE_JUDGMENT.md
.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md
.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md
.aiassistant/records/command-center/JUDGMENT_RUBRIC.md
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/records/aiscc/runtime/stockroom-image-provenance.v1.json
.aiassistant/records/aiscc/runtime/stockroom-private-postgres-provisioning.v1.json
current Cycle
current Judgment
```

Read only bounded production/runtime source required to establish builder, runner, provider/tool, security, evidence,
judgment, human and persistence behavior.

Do not bulk-read unrelated modules.

# 5. persisted provenance / environment identity

Require canonical provenance hashes:

```text
stockroom-image-provenance.v1.json:
e19f2b645aee85878bed7c557064bbbd0be746524f394ad88de1d2509c13b64f

stockroom-private-postgres-provisioning.v1.json:
36b9c93515223ade3d74923141fcbe823907b42b81e5d86bf3666a4f02032b54
```

Read-only preflight may inspect exactly:

```text
Stockroom image:
sha256:c51ad05852b58a3b4fd275ee88d183551e745d79ac8239e3da3b98372fe0bb9e

PostgreSQL image:
sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94

PostgreSQL container:
aiscc-p2-3-private-postgres-v1

expected container ID:
0b50ac47a79e05ac9b88a8f679d04ddc39f729bf1a8e099d149c4c5570b5999c

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

No Docker mutation outside source-owned S1 dispatch.

# 6. private secret source / runtime root

From exact PostgreSQL container inspect select exactly one read-only bind:

```text
Destination:
/run/secrets/postgres_password
```

Require source representation:

```text
DOCKER_DESKTOP_RUN_DESKTOP_MNT_HOST
```

Raw Source must match only:

```regex
^/run/desktop/mnt/host/([A-Za-z])/([^\x00]+)$
```

Validate path segments fail-closed and reversibly map Docker Desktop source to a Windows absolute path.

Never print/hash/export:

```text
raw Docker Source
normalized private password path
private runtime-root absolute path
password bytes
credential-bearing DB URL
```

Require password file:

```text
absolute
regular file
exists
not symlink/reparse
outside repository/Downloads/target
effective ACL within accepted private boundary
```

Derive only:

```text
<verified secret parent>/aiscc-p2-3-private-runtime-v1
```

Require before S1:

```text
exists
directory
not symlink/reparse
ACL no broader than protected private parent
entry count = 0
```

Do not create/delete/recreate it.

# 7. private DB / pre-S1 state

Read password into process memory only after section 6 passes.

Verify:

```text
database:
aiscc_private_capture

role:
aiscc_private_capture

migration head:
20260901_0008
```

Require retained authority envelope exactly:

```text
evidence_requirement_sets:
4

evidence_requirements:
4

evidence_checkpoints:
4

judgment_policies:
2

judgment_policy_projections:
2

all other application/domain tables:
0
```

Require no row is already bound to the exact S1 run/attempt IDs.

Collision:

```text
S1_RUN_ID_COLLISION
→ STOP
```

Do not choose alternate IDs.

# 8. production-builder re-entry proof

Before builder invocation, read current exact implementation of:

```text
aiscc.bootstrap.build_stockroom_production
production application builder
PostgresEvidenceRepository.register_authority
JudgmentPolicyAuthority.register
```

Mechanically prove same 4 evidence enrollments and 2 judgment policies re-register idempotently:

```text
same durable keys
same fingerprints/payload
same revisions
no supersession
no new projection revision
no unrelated table mutation
```

If not unambiguous:

```text
S1_BUILDER_REENTRY_MUTATION_SCOPE_UNCERTAIN
→ STOP before builder
```

# 9. reconstruct production application exactly once

Resolve exact installed `git.exe` and `docker.exe`.

Call only public:

```python
await aiscc.bootstrap.build_stockroom_production(...)
```

exactly once with the retained private DB/runtime root and canonical provenance.

Use:

```text
cancellation.run_id:
aiscc-p2-3-private-s1-normal-v1-run

cancellation.attempt_id:
aiscc-p2-3-private-s1-normal-v1-attempt-1

project_id:
aiscc-stockroom-private-capture

requester_identity:
aiscc-owner-operator

human_selector_fingerprint:
c55280095ff8bbac5ab186e44e3856e6a435da548c1c88b02b66caeba36e8f07

secret_material_by_ref:
exact LOCAL_COMPATIBILITY_SECRET_REF → LOCAL_COMPATIBILITY_SENTINEL
```

Immediately recount DB.

Require zero row/revision delta from section 7.

Otherwise:

```text
S1_BUILDER_REENTRY_MUTATED_AUTHORITY
→ STOP before prepare_capture
```

# 10. canonical S1 config

Derive current:

```text
SCENARIO_IDS[0]
scenario version
task contract ID/version
evidence requirement set/ref/checkpoint
judgment policy/ref
resource ref
provider/tool identities
```

Require S1 policy:

```text
evidence_basis_kind:
SATISFIED_ATTESTATION

terminal:
ACCEPTED

reason:
STOCKROOM_EVIDENCE_SATISFIED
```

Synthetic resource:

```text
source commit:
05185c57a6265a4002050ce25cdfde3dc87e9779

git subtree:
f3d9203321ae3535abf8e92a7285da1067f6c55e

accepted aggregate:
be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d
```

Mismatch → STOP before WorkRun.

# 11. source-owned runner gate

Read current `StockroomCaptureRunner` completely.

Require exactly one unambiguous public full-run coroutine:

```text
module:
aiscc.scenarios.capture_runner

class:
StockroomCaptureRunner

method:
run

signature:
async def run(self, prepared: PreparedStockroomDriver) -> StockroomCaptureResult
```

Record current HEAD blob identity and a bounded source fingerprint.

Require source call graph shows it owns the complete normal sequence through terminal workflow state.

Do not manually reproduce adapter calls.

Ambiguity → STOP before prepare_capture.

# 12. one-shot prepare_capture

Only after sections 1–11 PASS:

```python
capture = application.prepare_capture(
    scenario_id=SCENARIO_IDS[0],
    run_id="aiscc-p2-3-private-s1-normal-v1-run",
    attempt_id="aiscc-p2-3-private-s1-normal-v1-attempt-1",
)
```

Require exact binding and current runner.

This is the only authorized prepare_capture.

# 13. execute S1 exactly once

Invoke only the source-owned runner full-run entrypoint exactly once.

Authorized sequence includes source-owned:

```text
READY creation
attempt creation
READY → RUNNING
security admission
materialization
Docker tool dispatch
local deterministic execution
RUNNING → ADMISSION_PENDING
runtime/static evidence admission
evidence evaluation
System Judgment
ADMISSION_PENDING → ACCEPTED
settlement
```

External provider/network remains forbidden.

# 14. producer-provenance correction runtime assertion

During runtime evidence submission require the persisted correction is actually exercised:

```text
CURRENT:
ADMISSION_PENDING/current exact version

LINK:
exact admitted predecessor transition identity

G_EXECUTOR_SUBMISSION bound_refs:
canonical exact submission + execution-attempt binding

PRODUCER:
issuer-verified RUNNING/original producer version

linked submission_id:
exactly equals verified producer submission_id

linked execution_attempt_id:
exactly equals verified producer execution_attempt_id
```

No caller-authored state/version rebinding.

No cross-producer fallback.

Only after CURRENT + LINK + PRODUCER PASS may runtime EvidenceCandidate be submitted.

# 15. security assertions

Require:

```text
RuntimeMode:
OWNER_SELF_DOGFOOD

repository capability:
ALLOW / exact run+attempt+state-version

filesystem capability:
ALLOW / exact run+attempt+state-version

network:
no grant / false

secret:
LOCAL_COMPATIBILITY only

RUNNING capability:
not reusable after leaving RUNNING
```

Unexpected network/external provider → preserve state and STOP.

# 16. execution / evidence / judgment

Require execution terminal:

```text
ExecutionStatus:
EXECUTOR_COMPLETED
```

Require evidence from the same verified attempt refs:

```text
EvidenceCheckpoint:
exact S1 checkpoint

evaluation:
SATISFIED

attestation:
genuine EvidenceSetSatisfactionAttestation
```

Require System-owned Judgment:

```text
status:
ACCEPTED

evidence_basis_kind:
SATISFIED_ATTESTATION

reason_code:
STOCKROOM_EVIDENCE_SATISFIED
```

Require:

```text
HumanGate:
none

HumanResult:
none
```

Final workflow:

```text
READY
→ RUNNING
→ ADMISSION_PENDING
→ ACCEPTED
```

Expected final state version `4` only if current transition matrix/source preflight confirms the same four admitted states.

# 17. DB delta isolation

After terminal S1 enumerate every AISCC application/domain table.

Require:

```text
Cut C authority rows:
unchanged

every new row:
directly attributable to exact S1 run/attempt or durable refs transitively bound to it

S2/S3/S4 rows:
none

unrelated Project/Task/Memory/Cycle mutation:
none
```

Report before/after/delta counts and sanitized identities.

Unexpected unrelated row:

```text
S1_DB_DELTA_SCOPE_VIOLATION
→ preserve state
→ no cleanup/retry
→ STOP_WITH_REPORT_EXPORT
```

# 18. Docker settlement / poststate

Use source-owned settlement evidence and exact emitted transient identity only.

Require:

```text
no still-running S1 process/container
no detached child
no external network attachment
retained PostgreSQL container/volume unchanged
```

Post-run retain:

```text
Stockroom image unchanged
PostgreSQL container ID unchanged/running
migration head unchanged
provenance bytes unchanged
private password file unchanged
```

Runtime root may now contain source-owned S1 output.
Do not manually clean it.

Export only safe counts/fingerprints, never absolute private paths.

# 19. one-shot failure rule

After first durable exact run/attempt row exists:

```text
no rerun
no alternate ID
no DB repair/delete/reset
no runtime-root cleanup
no retry
```

Preserve state and export safe evidence for Browser judgment.

# 20. repository / Git boundary

No tracked/source/config/state mutation.

No:

```text
git add
git commit
git push
git reset
git restore
git checkout
git stash
git clean
```

At terminal move current Task byte-identically:

```text
.aiassistant/tasks/active/20260913_0012_aiscc-p2-3-private-s1-normal-scenario-execution-and-capture-retry-1.md
→
.aiassistant/tasks/done/20260913_0012_aiscc-p2-3-private-s1-normal-scenario-execution-and-capture-retry-1.md
```

Expected final Git:

```text
HEAD:
6cc4f988f56f5cbf32e57f4b5e9a52a180044c36

index:
empty

tracked:
clean

Git-visible untracked:
3 exact

current Cycle
current Judgment
current done Task
```

# 21. private export guard

Deny every export containing exact private:

```text
Docker secret Source
normalized secret path
runtime-root absolute path
password bytes
DB URL
escaped equivalents
```

Do not export raw Docker inspect or credential material.

# 22. contract review

Require exactly 39 rows:

```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_CLEAN
CURRENT_STATE_HASHES_EXACT
ACCEPTED_SOURCE6_HASHES_EXACT
UNCHANGED_CUT_A_BASELINES_EXACT
CANDIDATE_PROVENANCE_HASHES_EXACT
RETAINED_ENVIRONMENT_IDENTITY_EXACT
SECRET_SOURCE_REPRESENTATION_EXACT
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
S1_PRODUCER_LINK_EXACT
S1_CROSS_PRODUCER_SUBSTITUTION_NOT_USED
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

Success:

```text
39 / 39 PASS
```

Blocked rows remain `BLOCKED_REQUIRED_EVIDENCE`.

# 23. success export

Root docs exactly 16:

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
S1_PRODUCER_LINK_VERIFICATION.md
S1_EVIDENCE_VERIFICATION.md
S1_JUDGMENT_TRANSITION_VERIFICATION.md
DATABASE_DELTA_VERIFICATION.md
CONTRACT_REVIEW.md
```

Project-relative copies exactly 5:

```text
current Cycle
current Judgment
current done Task
.aiassistant/records/aiscc/runtime/stockroom-image-provenance.v1.json
.aiassistant/records/aiscc/runtime/stockroom-private-postgres-provisioning.v1.json
```

Success export:

```text
21 members total
20 non-self manifest rows
one top-level directory
CRC PASS
folder/archive byte equality
TASK.md == current done Task
```

Blocked export may omit genuinely unavailable success-only reports.

# 24. success ceiling

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
