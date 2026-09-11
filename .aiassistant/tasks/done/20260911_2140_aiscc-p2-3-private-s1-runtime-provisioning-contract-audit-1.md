# 작업지시서: P2-3 private S1 runtime provisioning contract audit

## meta

- task_id: `20260911_2140_aiscc-p2-3-private-s1-runtime-provisioning-contract-audit-1`
- created_at: `2026-09-11T21:40:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `PROVISIONING_CONTRACT_AUDIT / NO_MUTATION`
- evidence_profile: `HIGH_RISK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `21bb0769c5db126c1989d9e0eb8e9f4c5ceade91`
- required_tree: `11b9d62db2d02649509f148aa01f8f74924c5792`
- accepted_product_commit: `d98f9ad108e95ba659b9c6a10770119af22175a1`
- accepted_product_aggregate: `3aa781baaf25e09edd15f0713f7d42fc066d51092403cdc473f5030af684b4eb`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `runtime-readiness verification → provisioning/source-authority architecture`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. purpose

Resolve the exact provisioning architecture required before private S1.

Do not provision or implement anything in this Task.

Four accepted gaps:

```text
Stockroom image missing + provenance unestablished
persistent actual-capture DB identity absent
actual runtime-root selection absent
Docker process-runner binding absent
```

The audit must distinguish environment/operator provisioning from actual missing product/source implementation.

# 1. inbound transport

Verify Browser ZIP filename/SHA-256 from the Short Prompt.

Place current TASK first at:

```text
.aiassistant/tasks/active/20260911_2140_aiscc-p2-3-private-s1-runtime-provisioning-contract-audit-1.md
```

Read fully.

Require active Task is ignored by canonical Git policy.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260911_2140_aiscc-p2-3-runtime-prerequisite-not-ready-provisioning-contract-audit-entry-1.cycle.md
SHA-256:
ea3bd58bb66a6ea233013de75161605b249e32bd6537cd095a88ec090ba55144

.aiassistant/reports/aiscc/20260911_2140_aiscc-p2-3-runtime-prerequisite-verification-final-judgment-1.md
SHA-256:
db3e7d5101c43c22567396d80732f47227c25179bb6544c416a8e0058a994ecd
```

Bootstrap failure before Task placement:

```text
STOP
no audit probes
no report/export
```

# 2. repository gate

Require:

```text
branch:
main

HEAD:
21bb0769c5db126c1989d9e0eb8e9f4c5ceade91

HEAD tree:
11b9d62db2d02649509f148aa01f8f74924c5792

index:
empty
```

Before this delivery, exact Git-visible paths are the three 1935 governance paths:

- `.aiassistant/tasks/done/20260911_1935_aiscc-p2-3-actual-capture-runtime-prerequisite-verification-1.md`  `19b8bcc1f51c6d4be0ec3683e41c6d61884769bc01dc72f335a9c8ae6ab19a63`
- `.aiassistant/records/aiscc/cycles/20260911_1935_aiscc-p2-3-a2-terminal-persisted-runtime-prerequisite-verification-entry-1.cycle.md`  `8f1e5fa2ad6a18b1ff5a2118f24e81c249c81618a96b70ff067d54875de9b730`
- `.aiassistant/reports/aiscc/20260911_1935_aiscc-p2-3-a2-terminal-persistence-final-acceptance-judgment-1.md`  `814b5baf655ba5149ab91ecbaa81e9c14eb1f02fb9bfd54f5e737c405a765b03`

After current Cycle/Judgment placement and while Task is active:

```text
Git-visible:
5 exact

active Task:
exists byte-exact
ignored
```

No other dirt.

# 3. zero mutation

Do not modify:

```text
src/**
config/**
tests/**
examples/**
migrations/**
Dockerfile*
compose*
pyproject.toml
lock files
.gitignore
canonical state records
```

No Git add/commit/push.

No Docker image build/pull/create/run for Stockroom.

No persistent DB creation.

No actual S1.

# 4. authoritative reads

Read fully:

```text
20260911_1935 Executor reports if available in target/output evidence
current Cycle/Judgment
CURRENT_STATE_SUMMARY
NEXT_ACTIONS
DECISION_REGISTER

src/aiscc/runtime/docker.py
src/aiscc/runtime/stockroom_workspace.py
src/aiscc/runtime/stockroom_materializer.py
src/aiscc/providers/stockroom_tool.py
src/aiscc/providers/service.py
src/aiscc/scenarios/composition.py
src/aiscc/scenarios/driver.py
src/aiscc/scenarios/capture_runner.py
src/aiscc/scenarios/stockroom_production.py

config/providers/stockroom-tools.v1.toml
config/providers/stockroom-owner-profiles.v1.toml
config/providers/provider-profiles.v1.toml
config/providers/tool-registry.v1.toml
config/scenarios/stockroom/v1/resource.json
config/scenarios/stockroom/v1/s1-normal.json
config/security/stockroom-owner.v1.toml

pyproject.toml
```

Read the synthetic Stockroom source/provenance/build inputs:

```text
examples/synthetic-stockroom/.python-version
examples/synthetic-stockroom/README.md
examples/synthetic-stockroom/PROVENANCE.md
examples/synthetic-stockroom/tools/build.py
```

Use `git ls-files` to discover existing Docker/container/provisioning/runtime CLI files. Read only relevant matches.

# 5. OCI identity audit

Prove the current meanings of:

```text
source resource aggregate:
be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d

configured image ref:
aiscc-stockroom-runtime@sha256:be3dbe...
```

Answer:

```text
Is the suffix intended in accepted source as OCI manifest digest,
source identity pin,
or an overloaded placeholder?

Can Docker locally build an image that truthfully satisfies that exact
repository@sha256:<source-aggregate> identity without a registry/provenance trick?

Does the current DockerRuntime/tool loader validate image syntax,
image digest identity, or merely exact string equality?

Can local Docker inspect/run repo@digest without a RepoDigest-backed image?
```

Classify current design:

```text
OCI_IDENTITY_CONTRACT_VALID
SOURCE_DIGEST_OVERLOADED_AS_OCI_DIGEST
SYMBOLIC_IMAGE_PLACEHOLDER_ONLY
OTHER_EXACT_CLASSIFICATION
```

# 6. image build/provenance architecture

Design the smallest accepted image contract.

It must bind at least:

```text
synthetic source commit
subroot
Git subtree
14-file aggregate/source resource version
Python runtime version
runtime command/module
network-none behavior
build definition identity
resulting local OCI identity
```

Evaluate and choose exactly one image-reference model:

```text
A. registry-style repo@OCI-manifest-digest
B. immutable local image ID sha256:<image-config-id>
C. versioned local tag + separately verified image ID/provenance record
D. another exact Docker-supported immutable model
```

Do not keep the current source aggregate in an OCI-digest field unless Docker semantics prove it is valid.

State whether a registry is required.

Prefer no registry if local private S1 can preserve immutable provenance without one.

# 7. reproducible build definition

Determine what build artifact is needed.

Audit candidate locations such as:

```text
examples/synthetic-stockroom/Dockerfile
examples/synthetic-stockroom/docker/
scripts/
config/runtime/
```

Choose exact path(s).

The build contract must specify:

```text
base image identity and pin policy
Python 3.12.14
no secret build args
source copied only from accepted synthetic subroot
deterministic/normalized build inputs where feasible
runtime workdir /workspace
entry/module compatibility with:
python -B -m stockroom summary
runtime network none
non-root user if compatible with current workspace mount contract
labels/annotations for source commit/resource aggregate/build contract version
```

Distinguish:

```text
reproducible build inputs
vs
bit-for-bit reproducible OCI manifest
```

Do not promise bit-identical digest unless current toolchain supports and proves it.

# 8. image provenance admission artifact

Decide where immutable image provenance lives before S1.

Possible owners:

```text
versioned config
repository provenance JSON/TOML
Task/Cycle admitted environment evidence
runtime config + exact image inspect evidence
```

Choose exactly one canonical model.

It must prevent:

```text
same mutable tag pointing at different image
source aggregate being mistaken for OCI digest
unverified local image being accepted
```

Specify exact required fields and who issues/verifies them.

# 9. image config/source impact

Map every existing hard-coded image identity occurrence.

At minimum inspect:

```text
src/aiscc/runtime/docker.py
src/aiscc/providers/stockroom_tool.py
config/providers/stockroom-tools.v1.toml
```

Search for every exact `aiscc-stockroom-runtime` / `be3dbe...` reference.

For each path classify:

```text
MODIFY_REQUIRED
VERSION_BUMP_REQUIRED
FROZEN
NO_CHANGE_NEIGHBOR
```

Determine whether current `v1` provider/tool configs can remain immutable and a `v2` config is required.

# 10. Docker process-runner contract

Audit `DockerRuntime` and `StockroomProcessObservation`.

The injected runner must return authentic facts for:

```text
exit_code
bounded stdout/stderr
timeout/cancel
termination_proven
owner_reconciled
```

Determine the minimal production adapter required to:

```text
invoke the trusted absolute Docker executable
enforce Task-approved timeout
capture bounded output without deadlock
on timeout/cancel stop/kill exact container
wait for terminal state
inspect/reconcile exact container ownership
remove exact container if contract requires
prove termination and owner reconciliation
never invoke shell interpolation
never widen network or mounts
```

Choose semantic owner and exact source location for the adapter.

Classify:

```text
TASK_SCRIPT_SUFFICIENT
SOURCE_IMPLEMENTATION_REQUIRED
EXISTING_ADAPTER_ALREADY_SUFFICIENT
```

A Task-local lambda wrapping `subprocess.run` is not automatically sufficient unless it satisfies the accepted settlement contract.

# 11. runtime-root contract

Determine whether private S1 needs a source/config change for runtime root.

Current builder accepts:

```text
private_runtime_root: Path
```

Decide exact policy:

```text
TASK_SCOPED_ROOT_ONLY
REPOSITORY_CONFIGURED_ROOT
ENVIRONMENT_VARIABLE_ROOT
OTHER
```

The selected model must preserve:

```text
absolute
existing
empty
private
outside repository
outside Downloads
outside Git object store
Task-owned/attempt-owned cleanup
```

Prefer avoiding machine-specific absolute paths in tracked config.

Specify who selects it and what evidence is required.

# 12. persistent PostgreSQL identity architecture

Audit current production database ownership:

```text
external async_sessionmaker
migration head 20260901_0008
restart-surviving authority requirements
```

Determine whether private S1-S4 should use:

```text
A. dedicated local Docker PostgreSQL with named volume
B. existing operator PostgreSQL instance
C. repository-owned compose service
D. another exact model
```

Choose one for competition/private owner capture.

Required identity must cover:

```text
server/container/service identity
database name
storage/volume identity
migration head
lifecycle owner
retention through S1-S4 and corpus review
credential source without committing secret
connection configuration transport
backup/disposal point
```

Do not put credentials in Git.

# 13. DB source/config impact

Determine whether current source already supports the chosen persistent DB entirely through external `session_factory`.

If yes:

```text
SOURCE_CHANGE_NOT_REQUIRED
```

and define the exact operator provisioning artifact needed.

If no, identify exact source/config paths and why.

Do not conflate an operator provisioning script with domain authority.

# 14. provisioning ordering

Produce an exact sequence before private S1, for example:

```text
1 image build contract implementation
2 build image
3 inspect and admit immutable image provenance
4 provision persistent PostgreSQL identity
5 migrate/verify persistent DB
6 select exact private runtime root
7 bind trusted Docker process runner
8 rerun prerequisite verification
9 Browser readiness judgment
10 only then authorize private S1
```

Adjust based on source findings.

State which steps require separate Tasks/Browser judgments.

# 15. implementation cut selection

Choose an exact cut plan.

Candidate:

```text
CUT A:
source implementation for image contract + process runner

CUT B:
environment provisioning for image + persistent DB

CUT C:
final readiness verification with exact runtime-root binding
```

or another proven decomposition.

For each cut state:

```text
semantic owner
fresh IDE chat required?
mutation/provision scope
test/proof scope
success ceiling
```

Do not combine source mutation and irreversible/environment provisioning if separation materially improves auditability.

# 16. exact next mutation allowlist

For the first implementation cut only, produce exact path-level allowlist.

Candidate paths may include:

```text
src/aiscc/runtime/docker.py
src/aiscc/providers/stockroom_tool.py
src/aiscc/scenarios/composition.py
src/aiscc/scenarios/stockroom_production.py

config/providers/stockroom-tools.v2.toml
config/providers/stockroom-owner-profiles.v2.toml

examples/synthetic-stockroom/Dockerfile
examples/synthetic-stockroom/.dockerignore
examples/synthetic-stockroom/IMAGE_PROVENANCE.md
tests/unit/runtime/test_docker.py
tests/unit/providers/test_stockroom_tool.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Only include proven-required paths.

Do not use wildcard mutation scope.

# 17. environment provisioning allowlist

Separately define the environment-only operations that a later provisioning Task may authorize.

Examples:

```text
docker build/buildx using exact Dockerfile/context
no registry push unless architecture requires it
create exact named PostgreSQL volume/container
bind loopback only
run migration head
create exact external private runtime root
inspect exact image
```

Forbid broad Docker cleanup.

Define rollback/disposal for every created resource.

# 18. test/proof plan

Design exact future proof for image/runner source implementation:

```text
loader rejects old source-aggregate-as-OCI substitution
accepted immutable image identity round-trip
DockerRunSpec binds exact admitted image identity
runner argv has no shell
network none
workspace mount exact
bounded stdout/stderr
timeout settlement
cancel settlement
container ownership reconciliation
unknown tool outcome on unsettled process
no duplicate dispatch
legacy config compatibility/freeze as applicable
A2 S1-S4 bounded regression remains PASS
```

For environment provisioning proof:

```text
image inspect identity/provenance exact
persistent DB survives container restart if containerized
migration exact
DB state survives restart
runtime root exact/disjoint/private
runner executable identity exact
no actual S1
```

# 19. migration/state impact

Determine:

```text
application DB migration:
NO_MIGRATION / REQUIRED

canonical state-record mutation before provisioning:
NO / REQUIRED

new runtime provenance artifact:
exact path/type or NONE
```

No state edits in this audit.

# 20. root decisions

Audit success must provide exact answers:

```text
IMAGE_IDENTITY_MODEL
IMAGE_BUILD_CONTRACT
IMAGE_PROVENANCE_OWNER
IMAGE_SOURCE_CHANGE_REQUIRED

DOCKER_RUNNER_MODEL
DOCKER_RUNNER_SOURCE_CHANGE_REQUIRED

PERSISTENT_DB_MODEL
PERSISTENT_DB_SOURCE_CHANGE_REQUIRED

RUNTIME_ROOT_MODEL
RUNTIME_ROOT_SOURCE_CHANGE_REQUIRED

FIRST_IMPLEMENTATION_CUT
SECOND_PROVISIONING_CUT
FINAL_READINESS_CUT
```

No `UNKNOWN` in a successful audit.

# 21. contract review

Require:

```text
NO_PRODUCT_MUTATION
NO_CONFIG_MUTATION
NO_DOCKER_BUILD
NO_DOCKER_PULL
NO_STOCKROOM_RUN
NO_PERSISTENT_DB_CREATE
NO_ACTUAL_S1
NO_ACTUAL_S2_S4
NO_REPLAY
SOURCE_AGGREGATE_NOT_SILENTLY_TREATED_AS_OCI_DIGEST
CREDENTIALS_NOT_PERSISTED
MACHINE_PATH_NOT_PERSISTED
EXACT_SEMANTIC_OWNERS_ASSIGNED
EXACT_FIRST_ALLOWLIST_RESOLVED
ORDERING_BEFORE_S1_RESOLVED
```

Require:

```text
15 / 15 PASS
```

# 22. final workspace

Before current Task movement:

```text
Git-visible:
5 exact
index empty
```

Move active Task byte-identically to:

```text
.aiassistant/tasks/done/20260911_2140_aiscc-p2-3-private-s1-runtime-provisioning-contract-audit-1.md
```

Final expected:

```text
Git-visible:
6 exact

three 1935 governance paths
current Cycle
current Judgment
current done Task

index:
empty
```

No other delta.

# 23. required export

Folder:

```text
.aiassistant/reports/target/20260911_2140_aiscc-p2-3-private-s1-runtime-provisioning-contract-audit-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
OCI_IDENTITY_AUDIT.md
IMAGE_BUILD_PROVENANCE_ARCHITECTURE.md
DOCKER_RUNNER_CONTRACT.md
PERSISTENT_DB_ARCHITECTURE.md
RUNTIME_ROOT_ARCHITECTURE.md
PROVISIONING_ORDER.md
IMPLEMENTATION_CUT_PLAN.md
IMPLEMENTATION_ALLOWLIST.md
ENVIRONMENT_PROVISIONING_ALLOWLIST.md
REGRESSION_PLAN.md
CONTRACT_REVIEW.md
```

Also include byte-preserving copies of:

```text
current Cycle
current Judgment
current done Task
```

Export source evidence for every file that the final allowlist or architecture directly depends on, up to 20 exact files, and list them in the manifest as `SOURCE_EVIDENCE`.

Expected member count is therefore:

```text
18 + N source-evidence files
where 0 <= N <= 20
```

Record exact N and total.

`EXPORT_MANIFEST.md` covers all non-self entries.

# 24. failure semantics

Bootstrap failure:

```text
STOP / no report/export
```

After Task placement:

```text
STOP_WITH_REPORT_EXPORT
```

if:

```text
HEAD/tree/index mismatch
unexpected Git dirt
accepted predecessor identity mismatch
source/config mutation
Docker/image/DB provisioning occurs
actual S1 occurs
root decisions cannot be resolved
archive export fails
```

# 25. success ceiling

Success:

```text
runtime provisioning architecture:
RESOLVED

first source implementation cut:
AUTHORIZED_NEXT_BY_BROWSER_ONLY

environment provisioning:
NOT_EXECUTED

private S1:
NOT_AUTHORIZED

P2-3:
IN_PROGRESS
```
