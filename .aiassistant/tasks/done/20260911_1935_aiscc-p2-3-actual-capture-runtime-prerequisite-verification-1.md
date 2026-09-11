# 작업지시서: P2-3 actual capture runtime prerequisite verification

## meta

- task_id: `20260911_1935_aiscc-p2-3-actual-capture-runtime-prerequisite-verification-1`
- created_at: `2026-09-11T19:35:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `RUNTIME_PREREQUISITE_VERIFICATION / NO_PRODUCT_MUTATION`
- evidence_profile: `HIGH_RISK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `21bb0769c5db126c1989d9e0eb8e9f4c5ceade91`
- required_tree: `11b9d62db2d02649509f148aa01f8f74924c5792`
- accepted_product_commit: `d98f9ad108e95ba659b9c6a10770119af22175a1`
- accepted_product_aggregate: `3aa781baaf25e09edd15f0713f7d42fc066d51092403cdc473f5030af684b4eb`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `Git persistence/state reconciliation authority → local runtime/environment readiness authority`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. Python discipline

Do not assume bare:

```text
python
python3
py
```

is valid.

Do not run bare `python` as a probe.

Known global interpreter candidate:

```text
C:\Users\oracl\AppData\Roaming\uv\python\cpython-3.12.14-windows-x86_64-none\python.exe
```

For repository imports/config loaders use exact:

```text
.venv\Scripts\python.exe
```

if present and valid.

# 1. purpose and hard boundary

Verify whether the current machine/repository is ready for a **separately authorized private S1 capture**.

Do not execute S1 in this Task.

Do not silently provision a missing prerequisite.

Expected result is one of:

```text
READY_FOR_PRIVATE_S1

NOT_READY / PROVISIONING_REQUIRED
```

Both are successful verification outcomes if supported by exact evidence.

# 2. inbound transport

Verify Browser ZIP filename/SHA-256 from the Short Prompt.

Place current TASK first at:

```text
.aiassistant/tasks/active/20260911_1935_aiscc-p2-3-actual-capture-runtime-prerequisite-verification-1.md
```

Read fully.

Require the active Task to be ignored by canonical Git policy.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260911_1935_aiscc-p2-3-a2-terminal-persisted-runtime-prerequisite-verification-entry-1.cycle.md
SHA-256:
8f1e5fa2ad6a18b1ff5a2118f24e81c249c81618a96b70ff067d54875de9b730

.aiassistant/reports/aiscc/20260911_1935_aiscc-p2-3-a2-terminal-persistence-final-acceptance-judgment-1.md
SHA-256:
814b5baf655ba5149ab91ecbaa81e9c14eb1f02fb9bfd54f5e737c405a765b03
```

Bootstrap failure before current Task placement:

```text
STOP
no environment probes
no report/export
```

# 3. Git/canonical state gate

Require before current Cycle/Judgment placement:

```text
branch:
main

HEAD:
21bb0769c5db126c1989d9e0eb8e9f4c5ceade91

HEAD tree:
11b9d62db2d02649509f148aa01f8f74924c5792

index:
empty

git status --porcelain:
empty
```

After current Cycle/Judgment placement and while Task is active:

```text
Git-visible:
2 exact

current active Task:
exists byte-exact
ignored
```

Exact visible paths:

```text
.aiassistant/records/aiscc/cycles/20260911_1935_aiscc-p2-3-a2-terminal-persisted-runtime-prerequisite-verification-entry-1.cycle.md
.aiassistant/reports/aiscc/20260911_1935_aiscc-p2-3-a2-terminal-persistence-final-acceptance-judgment-1.md
```

No other dirt.

# 4. canonical state identity

Require exact committed state records:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `79cb3adc915928faba18b728bd671625d29a77e3948973555666bc83445a1047`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `9e3562322b4f8e8910f3e59463c77a975cd91531cf3b02e0a640b4b1a80b6206`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `2c0143e1c7177ac92f5d7934e3adc322fc0260191e17601d6a646d5fcfd85f94`

Read all three fully.

Require they still state:

```text
A2 IMPLEMENTATION ACCEPTED / PERSISTED
A2 terminal persistence pending Browser judgment at commit time
runtime prerequisite verification NEXT
actual S1-S4 NOT_STARTED
Replay NOT_ADMITTED
```

The current Browser Judgment in this delivery supersedes only the pending terminal-persistence judgment.

It does not authorize S1.

# 5. accepted historical runtime audit

Read the canonical repository copies of the prior actual-capture runtime-entry audit lineage, including:

```text
.aiassistant/tasks/done/20260910_1008_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-retry-1.md
.aiassistant/reports/aiscc/20260910_1040_aiscc-p2-3-actual-capture-runtime-entry-audit-final-acceptance-judgment-1.md
```

and their direct Cycle/Judgment predecessors as needed.

Treat their runtime-prerequisite matrix as historical source guidance only.

Current committed source at `21bb0769c5db126c1989d9e0eb8e9f4c5ceade91` owns the current answer.

# 6. zero product mutation

No mutation is authorized under:

```text
src/**
config/**
tests/**
migrations/**
pyproject.toml
lock files
Dockerfile/build files
.gitignore
canonical state records
```

No Git staging/commit/push.

Any product/source/config change need is a provisioning gap result for a successor Task.

# 7. current source/config read set

Read fully:

- `src/aiscc/bootstrap.py`
- `src/aiscc/scenarios/composition.py`
- `src/aiscc/scenarios/driver.py`
- `src/aiscc/scenarios/capture_runner.py`
- `src/aiscc/scenarios/stockroom_production.py`
- `src/aiscc/runtime/stockroom_workspace.py`
- `src/aiscc/runtime/stockroom_materializer.py`
- `src/aiscc/runtime/docker.py`
- `src/aiscc/providers/service.py`
- `src/aiscc/providers/local_deterministic.py`
- `src/aiscc/providers/stockroom_tool.py`
- `src/aiscc/security/policy.py`
- `src/aiscc/security/stockroom_policy.py`
- `config/providers/provider-profiles.v1.toml`
- `config/providers/stockroom-owner-profiles.v1.toml`
- `config/providers/stockroom-tools.v1.toml`
- `config/providers/tool-registry.v1.toml`
- `config/security/limits.v1.toml`
- `config/security/permission-profiles.v1.toml`
- `config/security/resource-policy.v1.toml`
- `config/security/stockroom-owner.v1.toml`
- `config/scenarios/stockroom/v1/catalog.json`
- `config/scenarios/stockroom/v1/resource.json`
- `config/scenarios/stockroom/v1/s1-normal.json`
- `config/evidence/stockroom-capture.v1.json`
- `config/human/stockroom-capture.v1.json`
- `config/judgment/stockroom-capture.v2.json`

Follow direct imports only when necessary to determine a prerequisite.

Do not execute actual capture paths.

# 8. Python/runtime packaging readiness

Determine from current packaging/source:

```text
supported Python requirement
repository .venv interpreter identity/version
Stockroom image command Python expectation
```

Verify:

```text
.venv\Scripts\python.exe exists
version is compatible with project packaging
basic repository import of runtime/config modules succeeds
```

Use `-B`.

Do not compile to `.pyc`.

Classification:

```text
READY
NOT_READY_PYTHON
```

# 9. trusted Git executable readiness

Resolve the actual Git executable used by the current environment to an absolute path.

Require:

```text
regular executable file
git --version succeeds
repository operations use the same trusted executable identity
current accepted source commit/object required by Stockroom resource is locally resolvable
```

Use read-only Git operations such as:

```text
git rev-parse
git cat-file -e
```

Do not checkout/materialize source.

Determine exact source commit/subroot/git-subtree/resource aggregate required by S1 from current config.

Classification:

```text
READY
NOT_READY_GIT_EXECUTABLE
NOT_READY_SOURCE_OBJECT
```

# 10. Docker daemon readiness

Run only non-network daemon inspection:

```text
docker version
docker info
```

Do not pull.

Record:

```text
client version
server version
server OS/architecture
storage driver if available
```

Do not print unrelated environment details.

Classification:

```text
READY
NOT_READY_DOCKER_DAEMON
```

# 11. exact Stockroom image identity/provenance

Determine the exact configured Stockroom image reference from current committed source/config.

Then run only:

```text
docker image inspect <exact configured ref>
```

No pull, build, create, or run.

If absent:

```text
NOT_READY_IMAGE_MISSING
```

If present, record:

```text
image ID
RepoTags
RepoDigests
created timestamp
architecture/OS
configured command/entrypoint
```

Then determine whether current repository contains an accepted reproducible image build/provisioning contract for that exact image.

A local tag/reference alone is not sufficient if the configured digest is only a symbolic source pin or provenance cannot be established.

Classify exactly one:

```text
READY_IMAGE_PROVENANCE_ESTABLISHED
NOT_READY_IMAGE_MISSING
NOT_READY_IMAGE_PROVENANCE_UNESTABLISHED
NOT_READY_IMAGE_IDENTITY_MISMATCH
```

Do not repair/provision.

# 12. PostgreSQL image/software readiness

The expected local test/runtime software baseline is:

```text
postgres:17.6-alpine
migration head:
20260901_0008
```

Check local image only:

```text
docker image inspect postgres:17.6-alpine
```

No pull.

If absent, report:

```text
NOT_READY_POSTGRES_IMAGE_MISSING
```

and do not fabricate DB readiness.

# 13. bounded PostgreSQL runtime probe

Only if Docker daemon and local PostgreSQL image are ready, create one Task-owned disposable PostgreSQL container:

```text
unique Task-owned name
--pull=never
loopback-only published port
temporary container storage
```

No named persistent capture volume in this Task.

Use a Task-local non-production credential only in process environment; do not print it.

Verify:

```text
container healthy/reachable
repository DB connection
alembic upgrade head
alembic current == 20260901_0008
basic read/write transaction required by repositories
```

Do not create S1 WorkRun/attempt/scenario state.

Then remove only that exact Task-owned container.

Classification:

```text
READY_SOFTWARE_PROBE
NOT_READY_POSTGRES_RUNTIME
```

Separately answer whether a persistent DB identity/storage plan for actual S1-S4 is already canonically configured.

If not:

```text
ACTUAL_CAPTURE_DB_IDENTITY:
PROVISIONING_REQUIRED
```

A disposable probe DB does not substitute for persistent capture storage.

# 14. operator runtime-root/filesystem readiness

Determine the runtime-root contract from:

```text
StockroomWorkspace
StockroomMaterializer
A2 production composition
```

Do not invent a permanent canonical path.

Create one external temporary readiness root outside:

```text
repository root
Downloads
Git object store
source-object root
```

Verify only:

```text
absolute path
directory create
single small file write/read/delete
subdirectory create/remove
cleanup succeeds
```

Do not call `StockroomMaterializer.materialize`.

Do not invoke Git source extraction.

Classification:

```text
FILESYSTEM_CAPABILITY_READY
NOT_READY_FILESYSTEM
```

Also state:

```text
ACTUAL_CAPTURE_RUNTIME_ROOT:
CONFIGURED
or
TASK_SCOPED_SELECTION_REQUIRED
or
PROVISIONING_REQUIRED
```

# 15. provider/tool config readiness

Strict-load current provider/tool/Stockroom configuration through production loaders where available.

Verify the exact S1 runtime profile resolves to:

```text
provider:
aiscc-local-deterministic

backend:
LOCAL_DETERMINISTIC_PROVIDER

external_llm_executed:
false

network requirement:
none / denied
```

Verify tool identity and process command match committed source/config.

Do not invoke provider or tool.

Classification:

```text
READY
NOT_READY_PROVIDER_CONFIG
```

# 16. security/network/secret readiness

Strict-load current security profiles.

Verify source-level prerequisites:

```text
NETWORK denied
repository/filesystem/process/tool/provider scopes bounded
Stockroom owner restrictions compatible with OWNER_SELF_DOGFOOD
compatibility SECRET is fixed non-secret sentinel only
no external API key/credential is required for S1
```

Do not resolve real OS/user secret stores.

Do not print secret values.

If current source requires an external secret not provided by the fixed non-secret compatibility contract:

```text
NOT_READY_SECRET_AUTHORITY
```

Otherwise:

```text
READY_NO_EXTERNAL_SECRET
```

# 17. source/materializer readiness without materialization

Using current source/config and read-only Git probes, verify:

```text
resource manifest/config parses
source commit object exists locally
subroot is canonical and bounded
expected aggregate/source identity is internally consistent
trusted Git executable satisfies materializer precondition
workspace root capability was proven separately
materializer owner construction requirements are fully known
```

Do not call `materialize()`.

Classification:

```text
READY_FOR_LATER_MATERIALIZATION
NOT_READY_MATERIALIZER_PREREQUISITE
```

# 18. private S1 evidence/provenance destination

Distinguish:

```text
private S1 runtime evidence
vs
future durable sanitized replay corpus/export
```

Determine from current accepted source whether private S1 can be reviewed using:

```text
durable PostgreSQL owner records
transition/evidence/Judgment refs
execution refs
verified Executor target bundle
```

while later corpus/export remains a separate implementation step.

Do not claim Recorded Replay readiness.

Classify:

```text
PRIVATE_S1_EVIDENCE_PATH_READY
PRIVATE_S1_EVIDENCE_PATH_NOT_READY
```

Separately:

```text
CORPUS_EXPORT:
NOT_STARTED / NOT_REQUIRED_FOR_THIS_VERIFICATION
```

If current source proves an immutable capture/export aggregate is mandatory before even private S1, report that exact blocker instead.

# 19. no actual capture

Forbidden in this Task:

```text
capture_runner.run()
real WorkRun for stockroom-s1-normal
real execution attempt for S1
StockroomMaterializer.materialize()
Docker run/create of Stockroom image
LocalDeterministicProvider execution
tool dispatch
Security capability consumption for S1
evidence submission/admission for S1
Judgment issue for S1
actual S1-S4 transition trace
Human gate creation
Replay
```

# 20. readiness decision

Produce an exact matrix with one row for every prerequisite:

```text
Python
trusted Git executable
source Git object
Docker daemon
Stockroom image existence
Stockroom image provenance
PostgreSQL local image
PostgreSQL software probe
actual capture persistent DB identity
runtime-root filesystem capability
actual capture runtime-root selection
provider/tool config
security/network
secret compatibility
materializer prerequisite
private S1 evidence/provenance path
```

Final decision exactly one:

```text
READY_FOR_PRIVATE_S1
```

or:

```text
NOT_READY / PROVISIONING_REQUIRED
```

If NOT_READY, enumerate the minimum exact provisioning gaps and semantic owner for each:

```text
ENVIRONMENT_OPERATOR
RUNTIME_IMAGE_PROVISIONING
DATABASE_PROVISIONING
TASK_SCOPED_RUNTIME_CONFIGURATION
SOURCE_IMPLEMENTATION
OTHER_EXACT_OWNER
```

Do not emit an implementation Task yourself.

# 21. contract review

Require PASS for:

```text
A2_COMMIT_A_EXACT
A2_COMMIT_B_EXACT
WORKTREE_BASE_CLEAN
NO_PRODUCT_MUTATION
NO_GIT_PERSISTENCE
NO_NETWORK_PULL
NO_STOCKROOM_IMAGE_EXECUTION
NO_REAL_MATERIALIZATION
NO_PROVIDER_EXECUTION
NO_TOOL_EXECUTION
NO_ACTUAL_S1
NO_ACTUAL_S2_S4
NO_REPLAY
POSTGRES_PROBE_TASK_OWNED_OR_NOT_RUN
POSTGRES_PROBE_CLEANED
RUNTIME_ROOT_TEMP_ONLY
RUNTIME_ROOT_CLEANED
NETWORK_DENIED_VERIFIED
EXTERNAL_LLM_FALSE_VERIFIED
NO_EXTERNAL_SECRET_REQUIRED_OR_EXACT_BLOCKER
SOURCE_OBJECT_READ_ONLY_VERIFIED
PRIVATE_S1_VS_CORPUS_BOUNDARY_PRESERVED
```

Require:

```text
21 / 21 PASS
```

A missing runtime prerequisite does not fail this contract review if it is truthfully classified and not bypassed.

# 22. cleanup

Remove only Task-owned:

```text
disposable PostgreSQL container
external temporary runtime-readiness root
external temporary verifier files
```

Do not delete local Docker images.

Do not broad-clean Docker.

Do not modify Downloads except best-effort inbound ZIP cleanup under canonical transport policy.

# 23. final repository state

No product/state mutation.

Before current Task movement:

```text
Git-visible:
2 exact
index empty
```

Move active Task byte-identically to:

```text
.aiassistant/tasks/done/20260911_1935_aiscc-p2-3-actual-capture-runtime-prerequisite-verification-1.md
```

Final expected:

```text
Git-visible:
3 exact

paths:
.aiassistant/records/aiscc/cycles/20260911_1935_aiscc-p2-3-a2-terminal-persisted-runtime-prerequisite-verification-entry-1.cycle.md
.aiassistant/reports/aiscc/20260911_1935_aiscc-p2-3-a2-terminal-persistence-final-acceptance-judgment-1.md
.aiassistant/tasks/done/20260911_1935_aiscc-p2-3-actual-capture-runtime-prerequisite-verification-1.md

index:
empty
```

# 24. source-evidence export

This Task explicitly authorizes byte-preserving `SOURCE_EVIDENCE_EXPORT` for the following 27 unchanged accepted files:

- `src/aiscc/bootstrap.py`
- `src/aiscc/scenarios/composition.py`
- `src/aiscc/scenarios/driver.py`
- `src/aiscc/scenarios/capture_runner.py`
- `src/aiscc/scenarios/stockroom_production.py`
- `src/aiscc/runtime/stockroom_workspace.py`
- `src/aiscc/runtime/stockroom_materializer.py`
- `src/aiscc/runtime/docker.py`
- `src/aiscc/providers/service.py`
- `src/aiscc/providers/local_deterministic.py`
- `src/aiscc/providers/stockroom_tool.py`
- `src/aiscc/security/policy.py`
- `src/aiscc/security/stockroom_policy.py`
- `config/providers/provider-profiles.v1.toml`
- `config/providers/stockroom-owner-profiles.v1.toml`
- `config/providers/stockroom-tools.v1.toml`
- `config/providers/tool-registry.v1.toml`
- `config/security/limits.v1.toml`
- `config/security/permission-profiles.v1.toml`
- `config/security/resource-policy.v1.toml`
- `config/security/stockroom-owner.v1.toml`
- `config/scenarios/stockroom/v1/catalog.json`
- `config/scenarios/stockroom/v1/resource.json`
- `config/scenarios/stockroom/v1/s1-normal.json`
- `config/evidence/stockroom-capture.v1.json`
- `config/human/stockroom-capture.v1.json`
- `config/judgment/stockroom-capture.v2.json`

For each copy record:

```text
source relative path
source SHA-256
copy SHA-256
byte equality
```

Do not classify the copies as product changes.

# 25. required export bundle

Folder:

```text
.aiassistant/reports/target/20260911_1935_aiscc-p2-3-actual-capture-runtime-prerequisite-verification-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
RUNTIME_PREREQUISITE_MATRIX.md
PYTHON_GIT_READINESS.md
DOCKER_IMAGE_READINESS.md
POSTGRESQL_READINESS.md
RUNTIME_ROOT_READINESS.md
PROVIDER_SECURITY_READINESS.md
MATERIALIZER_READINESS.md
CAPTURE_OUTPUT_READINESS.md
S1_READINESS_DECISION.md
CONTRACT_REVIEW.md
```

Also include byte-preserving canonical copies of:

```text
current Cycle
current Judgment
current done Task
CURRENT_STATE_SUMMARY.md
NEXT_ACTIONS.md
DECISION_REGISTER.md
```

and the 27 source-evidence copies from section 24.

Expected total:

```text
14 root docs
6 canonical copies
27 source-evidence copies
47 members
```

`EXPORT_MANIFEST.md` covers all 46 non-self entries.

Create adjacent verified ZIP with one top-level result directory, CRC PASS, exact member set, and folder/archive byte equality.

# 26. failure semantics

Bootstrap failure before Task placement:

```text
STOP
no report/export
```

After Task placement, unexpected inability to complete the verification protocol:

```text
STOP_WITH_REPORT_EXPORT
```

Expected missing prerequisites are **not** mandatory-stop errors.

They are readiness findings and the Task must continue far enough to enumerate all safely discoverable independent gaps.

# 27. success ceiling

Successful verification may conclude either:

```text
READY_FOR_PRIVATE_S1
```

or:

```text
NOT_READY / PROVISIONING_REQUIRED
```

In both cases:

```text
actual S1:
NOT_STARTED / NOT_AUTHORIZED

actual S2-S4:
NOT_STARTED / NOT_AUTHORIZED

corpus/export:
NOT_STARTED

Recorded Replay:
NOT_ADMITTED

P2-3:
IN_PROGRESS
```
