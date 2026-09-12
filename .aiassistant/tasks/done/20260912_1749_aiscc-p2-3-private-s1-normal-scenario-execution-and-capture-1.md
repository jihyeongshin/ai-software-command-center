# 작업지시서: P2-3 private S1 normal scenario execution and capture

## meta

- task_id: `20260912_1749_aiscc-p2-3-private-s1-normal-scenario-execution-and-capture-1`
- created_at: `2026-09-12T17:49:56+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `PRIVATE_SCENARIO_EXECUTION`
- evidence_profile: `HIGH_RISK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `ee623c995cf1c24b4a362834f2d6d1fdf71a30cd`
- required_parent: `4096913e9a117bd49bfecdb1ce5ca8de2735d661`
- required_grandparent: `6d41633210f0e556dd4292ee62a8600c6b54215f`
- fresh_ide_executor_chat: `REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`
- scenario_authorized: `S1 only`
- success_ceiling: `S1_EXECUTED_ACCEPTED_CANDIDATE / BROWSER_REVIEW_PENDING`

# 0. purpose

Execute the first actual private Stockroom scenario through the persisted Cut C production path.

This Task authorizes exactly one S1 normal-scenario attempt:

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

The Executor must not invent the orchestration sequence.
The source-owned `StockroomCaptureRunner` must own it.

# 1. inbound transport

Verify Short Prompt ZIP filename/SHA-256 and require exactly three flat members.

Place current Task first:

```text
.aiassistant/tasks/active/20260912_1749_aiscc-p2-3-private-s1-normal-scenario-execution-and-capture-1.md
```

Require byte equality and ignored status.

Then place:

```text
.aiassistant/records/aiscc/cycles/20260912_1749_aiscc-p2-3-cut-c-persisted-private-s1-execution-entry-1.cycle.md
SHA-256:
75fe2a744d010e327ff2d549aa998e2e64e0449735d50eec69a4fd6a183044ad

.aiassistant/reports/aiscc/20260912_1749_aiscc-p2-3-cut-c-persistence-final-acceptance-private-s1-authorization-judgment-1.md
SHA-256:
6457922c2520c2255edf9574b1c68c3ed633c3615e80be5c95c7e04f9e5961ed
```

Bootstrap mismatch:

```text
STOP
no Docker/private-file/DB access
no WorkRun
no report/export
```

# 2. canonical/read scope

Read applicable exact governance:

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
.aiassistant/records/aiscc/cycles/20260912_1749_aiscc-p2-3-cut-c-persisted-private-s1-execution-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_1749_aiscc-p2-3-cut-c-persistence-final-acceptance-private-s1-authorization-judgment-1.md
```

Read-only production/runtime source scope:

```text
src/aiscc/bootstrap.py
src/aiscc/scenarios/capture_runner.py
src/aiscc/scenarios/driver.py
src/aiscc/scenarios/models.py
src/aiscc/scenarios/composition.py
src/aiscc/scenarios/stockroom_production.py
src/aiscc/runtime/docker.py
src/aiscc/runtime/stockroom_image.py
src/aiscc/runtime/stockroom_materializer.py
src/aiscc/runtime/stockroom_workspace.py
src/aiscc/providers/service.py
src/aiscc/providers/stockroom_tool.py
src/aiscc/providers/local_deterministic.py
src/aiscc/evidence/**
src/aiscc/judgment/**
src/aiscc/human/**
src/aiscc/workflow/**
src/aiscc/persistence/**
config/providers/stockroom-tools.v2.toml
config/providers/stockroom-owner-profiles.v2.toml
config/evidence/stockroom-capture.v1.json
config/human/stockroom-capture.v1.json
config/judgment/stockroom-capture.v2.json
config/scenarios/stockroom/v1/resource.json
config/scenarios/stockroom/v1/fixtures/policy-conflict.json
```

Do not bulk-read unrelated modules.

# 3. repository preflight

Require:

```text
branch:
main

HEAD:
ee623c995cf1c24b4a362834f2d6d1fdf71a30cd

HEAD^:
4096913e9a117bd49bfecdb1ce5ca8de2735d661

HEAD^^:
6d41633210f0e556dd4292ee62a8600c6b54215f

index:
empty

tracked worktree:
clean

Git-visible untracked before delivery:
none
```

Canonical state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `7d0c9954b87e945b8c1c3fb66bda2dd54d23d5c3319202ef9fb24aa0ac56f424`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `04ec792c5e6dd4a7c8d2d35b716d1ed1fd569e60bb557532b811bc33dd434946`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `61ae340fa06e3d87d80f3308a240dacc1e0ba132a3b241a2059757830cf6312a`

After current Cycle/Judgment placement while current Task is active:

```text
Git-visible untracked:
2 exact

current Cycle
current Judgment

current active Task:
byte-exact / ignored
```

Any unexpected dirt/path:

```text
DIRTY_WORKSPACE_MIXED
→ STOP_WITH_REPORT_EXPORT
```

# 4. accepted source baseline

Require all accepted Cut A paths byte-exact:

- `src/aiscc/bootstrap.py`  `745b58da26ec300286ed69d1a7477b21afeb7625ec43e7f422560a657bc1c115`
- `src/aiscc/runtime/docker.py`  `284a3920f13f93928cc61420913506ed38af4e8f4d4e0e1f52d52c9074fa0753`
- `src/aiscc/runtime/stockroom_image.py`  `06e8d85e449a336392b73d9dec9915cd32d776688575a64030024609b08cec0e`
- `src/aiscc/providers/stockroom_tool.py`  `c5c925df000656ce32f65f4742f9a6936c2364d7d58eb92750966d8a8826e075`
- `src/aiscc/providers/local_deterministic.py`  `92ec8ba5553b05fe55fdbac30ab2dde8f57597c1055060a2f786dadd47f1c21a`
- `src/aiscc/scenarios/composition.py`  `a5f7ecb0d1bd9274f07094cbe3a4315098048c468472162e0ad84372fe6c50d3`
- `src/aiscc/scenarios/stockroom_production.py`  `685e2ec549473e167ed1fe4d7de1050d7a53a449d1d278dcdb3439a471478f1f`
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
- `tests/integration/scenarios/test_stockroom_capture_runner.py`  `373f9d5bc6f260785cdf943aa649ce99ab5826e8ae09dd2982c18db09459fbf5`

For every additional source/config file actually used from section 2, require:

```text
tracked by Git
worktree blob == HEAD blob
no staged/worktree delta
```

Record its HEAD blob identity in `SOURCE_BASELINE_VERIFICATION.md`.

No source/config/test mutation is authorized.

# 5. persisted provenance and environment identity

Require canonical provenance bytes:

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
expected ID 0b50ac47a79e05ac9b88a8f679d04ddc39f729bf1a8e099d149c4c5570b5999c

PostgreSQL volume:
aiscc-p2-3-private-postgres-data-v1
```

Stockroom image must retain inspect fingerprint:

```text
e5350a7236cc496d1d2abec80e52e900616d3935d1e26db1c7e967ca771f1e57
```

PostgreSQL sanitized projection must retain:

```text
867e744367eb804c30db6269d0700d8679c5aeb1a9b6fb78306ce1b87918c8e7
```

No Docker mutation is authorized outside source-owned S1 runtime dispatch.

# 6. private secret-source and runtime-root authority

From the exact PostgreSQL container inspect select exactly one read-only bind:

```text
Destination:
/run/secrets/postgres_password
```

Current admitted representation class is:

```text
DOCKER_DESKTOP_RUN_DESKTOP_MNT_HOST
```

Require the raw Source to match only:

```regex
^/run/desktop/mnt/host/([A-Za-z])/([^\x00]+)$
```

Validate every suffix segment:

```text
non-empty
not "." / ".."
no ":"
no "\"
```

Map reversibly:

```text
/run/desktop/mnt/host/c/a/b
→
C:\a\b
```

Reverse-map and require exact daemon representation equality except drive-letter case.

No alternate prefix/search/fallback.

Never print/hash/export the raw or normalized private path.

Require normalized password file:

```text
absolute
regular file
exists
not symlink/reparse
outside repository/Downloads/target
effective ACL within accepted private boundary
```

Derive the already-created runtime root only:

```text
<verified secret parent>/aiscc-p2-3-private-runtime-v1
```

Require:

```text
exists:
Yes

directory:
Yes

symlink/reparse:
No

ACL:
no broader than protected private parent

entries before S1:
0
```

Do not create/delete/recreate the root.

# 7. private DB connection and exact pre-S1 state

Read password into process memory only after section 6 passes.

Construct credential-bearing DB URL in memory only.

Verify:

```text
database:
aiscc_private_capture

role:
aiscc_private_capture

migration head:
20260901_0008
```

Before rebuilding the production application, count every AISCC application/domain table.

Require exactly the Cut C retained authority envelope:

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

Also require no row anywhere is already bound to:

```text
run_id:
aiscc-p2-3-private-s1-normal-v1-run

attempt_id:
aiscc-p2-3-private-s1-normal-v1-attempt-1
```

If any collision exists:

```text
S1_RUN_ID_COLLISION
→ STOP
```

Do not choose another ID.

# 8. production-builder re-entry proof

Before calling the builder, read the current exact implementations of:

```text
aiscc.bootstrap.build_stockroom_production
build_stockroom_production_application
PostgresEvidenceRepository.register_authority
JudgmentPolicyAuthority.register
```

Using current configs and the actual retained rows, mechanically prove that re-registering
the same 4 evidence enrollments and 2 judgment policies is idempotent:

```text
same durable keys
same fingerprints/payload
same authority revisions
no supersession event
no new projection revision
no other table mutation
```

If current source does not prove this unambiguously:

```text
S1_BUILDER_REENTRY_MUTATION_SCOPE_UNCERTAIN
→ STOP before builder
```

# 9. reconstruct production application exactly once

Resolve exact `git.exe` / `docker.exe`.

Build the same typed image provenance ref from canonical bytes.

Call public:

```python
await aiscc.bootstrap.build_stockroom_production(...)
```

exactly once with:

```text
session_factory:
verified private DB

repository_root:
current repository root

private_runtime_root:
existing exact empty root

downloads_root:
C:\Users\oracl\Downloads

trusted_git_executable:
resolved absolute git.exe

image_provenance_ref:
exact canonical typed ref

trusted_docker_executable:
resolved absolute docker.exe

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
exact current LOCAL_COMPATIBILITY_SECRET_REF → LOCAL_COMPATIBILITY_SENTINEL

clock:
production default
```

No direct external call to the internal application builder.

Immediately recount DB.

Require builder re-entry changed **zero rows and zero revisions** from section 7.

If not exact:

```text
S1_BUILDER_REENTRY_MUTATED_AUTHORITY
→ STOP before prepare_capture
```

# 10. S1 canonical scenario/config verification

From current source/config derive:

```text
S1 scenario_id = SCENARIO_IDS[0]
scenario version
task contract ID/version
evidence requirement set/ref/checkpoint
judgment policy/ref
resource ref
provider profile/tool registry identities
```

Require S1 judgment policy:

```text
evidence_basis_kind:
SATISFIED_ATTESTATION

terminal semantic:
ACCEPTED

reason code:
STOCKROOM_EVIDENCE_SATISFIED
```

Require synthetic resource identity remains:

```text
source commit:
05185c57a6265a4002050ce25cdfde3dc87e9779

git subtree:
f3d9203321ae3535abf8e92a7285da1067f6c55e

accepted source aggregate:
be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d
```

If S1 mapping is not exact:

```text
S1_CANONICAL_CONFIG_MISMATCH
→ STOP before WorkRun
```

# 11. source-owned orchestration entrypoint gate

Read the current `StockroomCaptureRunner` class definition completely.

Before creating a WorkRun, identify the **source-owned public end-to-end coroutine** that owns the
complete normal capture sequence from initial READY creation through terminal workflow state.

The candidate must be established from current source call graph, not guessed from naming.

Require:

```text
exactly one unambiguous full-run public entrypoint
it operates on the source-owned prepared capture/driver authority
it sequences owner adapter calls itself
it can reach S1 terminal Judgment + WorkflowState
```

Report:

```text
module
class
method name
signature
HEAD blob ID
bounded source line range or source fingerprint
```

Do not report source text verbatim beyond small identifiers/signature.

If no such method exists or more than one interpretation is possible:

```text
S1_ORCHESTRATION_ENTRYPOINT_AMBIGUOUS
→ STOP before prepare_capture
```

**Forbidden:** manually reproduce the runner by directly calling adapter methods in Browser-invented order.

# 12. one-shot S1 preparation

Only after sections 1–11 PASS:

```python
capture = application.prepare_capture(
    scenario_id=SCENARIO_IDS[0],
    run_id="aiscc-p2-3-private-s1-normal-v1-run",
    attempt_id="aiscc-p2-3-private-s1-normal-v1-attempt-1",
)
```

Require:

```text
capture.runner is current StockroomCaptureRunner
prepared run/attempt/scenario binding exact
configuration fingerprint exact
runtime root still empty
DB run/attempt IDs still absent before runner invocation
```

This is the only authorized `prepare_capture()`.

No S2/S3/S4 prepare_capture.

# 13. execute S1 only through source-owned runner

Invoke the section 11 full-run entrypoint **exactly once** using only arguments required by its
current source signature and the section 12 source-owned capture/prepared objects.

Do not manually invoke adapter stages around it.

The runner may exercise, because this Task authorizes S1:

```text
READY creation
execution-attempt creation
READY → RUNNING
security sealing/admission
repository/filesystem capability issuance
Stockroom materialization
source-owned Docker tool dispatch
local deterministic provider/tool execution
RUNNING → ADMISSION_PENDING
runtime/static evidence admission
evidence-set evaluation
S1 Judgment
ADMISSION_PENDING → ACCEPTED
source-owned settlement
```

No arbitrary shell/network/provider/model/endpoint selection.

External provider/network remains forbidden.

# 14. exact runtime security assertions

From authoritative runtime/security records require:

```text
RuntimeMode:
OWNER_SELF_DOGFOOD

repository capability:
ALLOW / exact run+attempt+state-version bound

filesystem capability:
ALLOW / exact run+attempt+state-version bound

network grant:
not issued / false

secret use:
only current LOCAL_COMPATIBILITY secret contract

normal execution capability:
not reusable after leaving RUNNING
```

Any unexpected network grant or external network/provider path:

```text
S1_SECURITY_BOUNDARY_VIOLATION
→ stop and preserve one-shot run state
```

# 15. S1 materialization/execution evidence

Require materialization provenance binds:

```text
run_id
attempt_id
S1 scenario
exact resource ref
source commit 05185c57a6265a4002050ce25cdfde3dc87e9779
git subtree f3d9203321ae3535abf8e92a7285da1067f6c55e
accepted aggregate
exact existing private runtime root
```

Require execution uses source-owned:

```text
StockroomMaterializer
StockroomAgentExecutionServiceFactory
AgentExecutionService
StockroomSummaryDispatcher
StockroomDockerRunner / DockerRuntime
LocalDeterministicProvider
```

Execution terminal must be:

```text
ExecutionStatus:
EXECUTOR_COMPLETED
```

Remember:

```text
EXECUTOR_COMPLETED != WorkflowState.ACCEPTED
```

Capture exact AgentOutputRef/ToolOutputRef identities and hashes in sanitized form.

# 16. S1 evidence admission

Require S1 runtime evidence is admitted from the same attempt's verified execution refs.

Require exact S1 EvidenceCheckpoint use.

Require evidence evaluation:

```text
SATISFIED
```

Require a genuine:

```text
EvidenceSetSatisfactionAttestation
```

bound to exact:

```text
S1 task contract
run_id
attempt_id
checkpoint
current source/target purpose
state/version
full requirement set
admitted evidence coverage
```

No raw candidate/ref substitution.

# 17. S1 Judgment and final transition

Require S1 Judgment is System-owned and durably admitted:

```text
status:
ACCEPTED

evidence_basis_kind:
SATISFIED_ATTESTATION

evidence_attestation_ref:
authentic S1 satisfaction attestation

reason_code:
STOCKROOM_EVIDENCE_SATISFIED
```

Require:

```text
HumanGate:
none for S1

HumanResult:
none for S1
```

Then require source-owned transition authority reaches:

```text
WorkflowState:
ACCEPTED
```

Expected authoritative state progression:

```text
READY
→ RUNNING
→ ADMISSION_PENDING
→ ACCEPTED
```

Expected final state version is `4` **only if current source/matrix inspection before execution confirms
that exact four-admission sequence**. Otherwise STOP before WorkRun as a source-contract mismatch;
do not weaken the expected S1 normal path after execution begins.

Judgment is evidence authority; it is not itself the TransitionDecision.

# 18. exact DB delta / isolation

After terminal S1, enumerate every AISCC application/domain table.

Require:

```text
Cut C authority rows:
unchanged

every new row:
directly attributable to run_id aiscc-p2-3-private-s1-normal-v1-run
or attempt_id aiscc-p2-3-private-s1-normal-v1-attempt-1
or an owner-issued durable ref transitively bound to that exact S1 run/attempt

no S2/S3/S4 run rows
no unrelated Project/Task/Memory/Cycle mutation
```

Report a table-by-table before/after/delta count and sanitized durable identity summary.

Any unrelated row:

```text
S1_DB_DELTA_SCOPE_VIOLATION
→ preserve current run state
→ no retry/cleanup
→ STOP_WITH_REPORT_EXPORT
```

# 19. Docker/process settlement

Do not use broad Docker inventory discovery.

Use source-owned runner/dispatcher settlement evidence and exact resource identities emitted by the
S1 execution path.

Require:

```text
no still-running S1 Stockroom process/container
no detached/background child
no network attachment beyond source-owned denied/default boundary
no mutation of retained PostgreSQL container/volume
```

If the source-owned execution receipt exposes an exact transient container identity, exact inspect of
that identity for settlement is allowed.

Do not inspect unrelated containers.

# 20. post-run private state

Require retained base environment unchanged:

```text
Stockroom image:
sha256:c51ad05852b58a3b4fd275ee88d183551e745d79ac8239e3da3b98372fe0bb9e

PostgreSQL container:
0b50ac47a79e05ac9b88a8f679d04ddc39f729bf1a8e099d149c4c5570b5999c
running

migration head:
20260901_0008

candidate provenance bytes:
unchanged

private password file:
content and metadata unchanged
```

The private runtime root may contain source-owned S1 materialization/output after execution.

Do **not** manually clean it.

Record only safe facts:

```text
exists
entry count
source-owned manifest/aggregate fingerprints
no reparse escape
```

Never export absolute private paths.

# 21. one-shot failure rule

Before durable run creation, a blocker may be retried only under a new Browser Task.

After the first durable row for `aiscc-p2-3-private-s1-normal-v1-run` or `aiscc-p2-3-private-s1-normal-v1-attempt-1` exists:

```text
do not rerun the runner
do not choose a new run/attempt ID
do not delete/reset/repair DB rows
do not clean private runtime output
do not recreate runtime root
```

Preserve exact state and export safe evidence for Browser judgment.

# 22. repository/Git boundary

No tracked/source/config/state mutation.

No `git add`, `commit`, `push`, `reset`, `restore`, `checkout`, `stash`, or `clean`.

At terminal submission move current Task byte-identically:

```text
.aiassistant/tasks/active/20260912_1749_aiscc-p2-3-private-s1-normal-scenario-execution-and-capture-1.md
→
.aiassistant/tasks/done/20260912_1749_aiscc-p2-3-private-s1-normal-scenario-execution-and-capture-1.md
```

Expected final Git state:

```text
HEAD:
ee623c995cf1c24b4a362834f2d6d1fdf71a30cd

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

Ignored target/helper artifacts do not count.

# 23. private/export guard

Once private values are acquired, deny every exported byte containing exact:

```text
raw Docker secret Source
normalized private password path
private runtime-root absolute path
password bytes
decoded password
credential-bearing DB URL
JSON-escaped path/value forms
```

Do not export raw Docker inspect, DB URL, environment, secret file, or full private materialized path.

S1 Agent/Tool output may be exported only if classified/sanitized as allowed by current evidence/public-provenance rules.
Otherwise export refs/hashes/typed summaries only.

# 24. evidence contract

`executor_required`:

```text
transport/repository/source/state identity
retained environment/private boundary
existing empty runtime root
exact pre-builder 16-row authority envelope
builder reentry idempotency proof + zero DB delta
canonical S1 config
source-owned orchestration entrypoint gate
one S1 prepare_capture
one source-owned S1 runner invocation
security/network deny
materialization/execution provenance
runtime evidence admission
SATISFIED attestation
ACCEPTED Judgment
ACCEPTED transition
run-scoped DB delta
Docker/process settlement
post-environment/private state
secret export scan
```

`reuse_allowed`:

```text
Cut A accepted source proof when current hashes remain exact
Cut B environment/provenance admission
1654 Cut C readiness execution evidence
1707 Cut C persistence acceptance
```

`human_owned`:

```text
Browser review/admission of this S1 result
future S1 persistence/corpus admission
future S2/S3/S4 authorization
```

`not_required`:

```text
source changes
test suite
browser QA
Git persistence
Replay generation
public deployment
cleanup of historical helper residue
```

`forbidden`:

```text
manual adapter orchestration
S2/S3/S4
external provider/network
HumanResult
Replay
canonical state mutation
Git persistence
```

# 25. contract review

Require exactly 37 rows:

```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_CLEAN
CURRENT_STATE_HASHES_EXACT
CUT_A_19_HASHES_EXACT
CURRENT_RUNTIME_SOURCE_TRACKED_AT_HEAD
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

Require:

```text
37 / 37 PASS
```

Blocked rows remain `BLOCKED_REQUIRED_EVIDENCE`; never relabel them PASS.

# 26. success export

Target:

```text
.aiassistant/reports/target/20260912_1749_aiscc-p2-3-private-s1-normal-scenario-execution-and-capture-1/
```

Root documents exactly 16:

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
.aiassistant/records/aiscc/cycles/20260912_1749_aiscc-p2-3-cut-c-persisted-private-s1-execution-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_1749_aiscc-p2-3-cut-c-persistence-final-acceptance-private-s1-authorization-judgment-1.md
.aiassistant/tasks/done/20260912_1749_aiscc-p2-3-private-s1-normal-scenario-execution-and-capture-1.md
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
TASK.md == canonical current done Task
```

A blocked result may omit genuinely unavailable success-only reports.
Do not fabricate success evidence.

# 27. success ceiling

Executor success means only:

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
