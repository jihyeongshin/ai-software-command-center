# 작업지시서: P2-3 private S1 image build-input authority reconciliation audit

## meta

- task_id: `20260911_2148_aiscc-p2-3-private-s1-image-build-input-authority-reconciliation-audit-1`
- created_at: `2026-09-11T21:48:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `PROVISIONING_CONTRACT_REWORK_AUDIT / NO_MUTATION`
- evidence_profile: `HIGH_RISK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `21bb0769c5db126c1989d9e0eb8e9f4c5ceade91`
- required_tree: `11b9d62db2d02649509f148aa01f8f74924c5792`
- accepted_product_commit: `d98f9ad108e95ba659b9c6a10770119af22175a1`
- accepted_product_aggregate: `3aa781baaf25e09edd15f0713f7d42fc066d51092403cdc473f5030af684b4eb`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. purpose

Reconcile only the unresolved image build-input/provenance authority in the `2140`
provisioning architecture.

Do not implement Cut A.

Do not build/pull/run the Stockroom image.

Do not create persistent PostgreSQL.

Do not execute S1.

# 1. inbound transport

Verify Browser ZIP filename/SHA-256 from the Short Prompt.

Place current Task first:

```text
.aiassistant/tasks/active/20260911_2148_aiscc-p2-3-private-s1-image-build-input-authority-reconciliation-audit-1.md
```

Read fully and verify it is ignored by canonical Git policy.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260911_2148_aiscc-p2-3-provisioning-contract-partial-hold-image-build-authority-rework-entry-1.cycle.md
SHA-256:
63de3c09811b4041979e53dbeeb03fdb6ab9c723a209cee4d2df2f436d0176ed

.aiassistant/reports/aiscc/20260911_2148_aiscc-p2-3-provisioning-contract-audit-image-build-authority-gap-judgment-1.md
SHA-256:
529719fb0b4ae54ba613b7c6652124318d6f5083fee273c08d47651191311cae
```

Bootstrap failure:

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

Before this delivery exact Git-visible set is 6:

- `.aiassistant/tasks/done/20260911_1935_aiscc-p2-3-actual-capture-runtime-prerequisite-verification-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_1935_aiscc-p2-3-a2-terminal-persisted-runtime-prerequisite-verification-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1935_aiscc-p2-3-a2-terminal-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260911_2140_aiscc-p2-3-private-s1-runtime-provisioning-contract-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_2140_aiscc-p2-3-runtime-prerequisite-not-ready-provisioning-contract-audit-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2140_aiscc-p2-3-runtime-prerequisite-verification-final-judgment-1.md`

Require exact predecessor hashes:

- `.aiassistant/tasks/done/20260911_1935_aiscc-p2-3-actual-capture-runtime-prerequisite-verification-1.md`  `19b8bcc1f51c6d4be0ec3683e41c6d61884769bc01dc72f335a9c8ae6ab19a63`
- `.aiassistant/records/aiscc/cycles/20260911_1935_aiscc-p2-3-a2-terminal-persisted-runtime-prerequisite-verification-entry-1.cycle.md`  `8f1e5fa2ad6a18b1ff5a2118f24e81c249c81618a96b70ff067d54875de9b730`
- `.aiassistant/reports/aiscc/20260911_1935_aiscc-p2-3-a2-terminal-persistence-final-acceptance-judgment-1.md`  `814b5baf655ba5149ab91ecbaa81e9c14eb1f02fb9bfd54f5e737c405a765b03`
- `.aiassistant/tasks/done/20260911_2140_aiscc-p2-3-private-s1-runtime-provisioning-contract-audit-1.md`  `881988722767df492c24f5e68a680c8ea316362b5b8a8f09117695bf538595e7`
- `.aiassistant/records/aiscc/cycles/20260911_2140_aiscc-p2-3-runtime-prerequisite-not-ready-provisioning-contract-audit-entry-1.cycle.md`  `ea3bd58bb66a6ea233013de75161605b249e32bd6537cd095a88ec090ba55144`
- `.aiassistant/reports/aiscc/20260911_2140_aiscc-p2-3-runtime-prerequisite-verification-final-judgment-1.md`  `db3e7d5101c43c22567396d80732f47227c25179bb6544c416a8e0058a994ecd`

After current Cycle/Judgment placement, while Task remains active:

```text
Git-visible:
8 exact

active Task:
exists byte-exact
ignored
```

Exact visible set:

- `.aiassistant/tasks/done/20260911_1935_aiscc-p2-3-actual-capture-runtime-prerequisite-verification-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_1935_aiscc-p2-3-a2-terminal-persisted-runtime-prerequisite-verification-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1935_aiscc-p2-3-a2-terminal-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260911_2140_aiscc-p2-3-private-s1-runtime-provisioning-contract-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_2140_aiscc-p2-3-runtime-prerequisite-not-ready-provisioning-contract-audit-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2140_aiscc-p2-3-runtime-prerequisite-verification-final-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_2148_aiscc-p2-3-provisioning-contract-partial-hold-image-build-authority-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2148_aiscc-p2-3-provisioning-contract-audit-image-build-authority-gap-judgment-1.md`

No other dirt.

# 3. zero mutation/provisioning

No modification under:

```text
src/**
config/**
tests/**
examples/**
migrations/**
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
```

No Git staging/commit/push.

Forbidden:

```text
docker pull
docker build/buildx
docker create/run
docker manifest inspect
registry API/network lookup
persistent DB create
actual S1
```

Read-only local Docker image inspection is allowed.

# 4. authoritative source reads

Read fully:

```text
src/aiscc/runtime/docker.py
src/aiscc/providers/stockroom_tool.py
src/aiscc/providers/local_deterministic.py
src/aiscc/scenarios/composition.py
src/aiscc/scenarios/enrollment.py
src/aiscc/scenarios/driver.py
src/aiscc/scenarios/stockroom_production.py
src/aiscc/security/stockroom_policy.py

config/providers/stockroom-tools.v1.toml
config/providers/stockroom-owner-profiles.v1.toml
config/security/stockroom-owner.v1.toml
config/scenarios/stockroom/v1/resource.json

examples/synthetic-stockroom/.python-version
examples/synthetic-stockroom/PROVENANCE.md
examples/synthetic-stockroom/tools/build.py

tests/unit/runtime/test_stockroom_docker_settlement.py
tests/unit/providers/test_stockroom_tool.py
tests/unit/security/test_stockroom_policy.py
tests/unit/scenarios/test_stockroom_capture_runner.py
tests/integration/scenarios/test_stockroom_binding.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Follow only direct imports necessary to define config/provenance loading.

# 5. base-image local evidence probe

Without network, determine whether local Docker already has:

```text
python:3.12.14-slim-bookworm
```

Use only:

```text
docker image inspect python:3.12.14-slim-bookworm
```

and, if present, inspect its exact:

```text
Id
RepoTags
RepoDigests
Os
Architecture
Config labels if any
```

No pull.

If absent:

```text
BASE_IMAGE_LOCAL_EVIDENCE = ABSENT
```

If present:

```text
BASE_IMAGE_LOCAL_EVIDENCE = PRESENT
```

A local RepoDigest is environment evidence only until admitted by a future provisioning
Task/Judgment.

# 6. unsupported 2140 digest audit

Audit the exact value:

```text
0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579
```

Determine whether any current repository file, prior canonical evidence, or local
image inspection supports that exact digest.

Classify exactly one:

```text
SUPPORTED_EXACT_REPODIGEST
UNSUPPORTED_EXACT_DIGEST_CLAIM
LOCAL_OBSERVATION_ONLY_NOT_CANONICAL
```

If unsupported, the corrected architecture must remove it as an admitted fixed input.

# 7. base-image pin model

Choose exactly one canonical model:

```text
A. SOURCE_FIXED_VERIFIED_REPODIGEST
B. PROVISIONING_TIME_EXACT_REPODIGEST_INPUT
C. PROVISIONING_TIME_LOCAL_BASE_IMAGE_ID_WITH_EXACT_TAG_BINDING
D. OTHER_DOCKER_SUPPORTED_IMMUTABLE_MODEL
```

Requirements:

```text
no floating tag as authority
no invented digest
no network dependency in Cut A source tests
Cut B can prove exact base identity before build
final image provenance records exact base identity
```

If choosing B, decide whether Dockerfile uses:

```text
ARG AISCC_STOCKROOM_BASE_IMAGE
FROM ${AISCC_STOCKROOM_BASE_IMAGE}
```

or another exact mechanism.

If build args are allowed, classify the base-image arg as:

```text
NON_SECRET_IMMUTABLE_BUILD_INPUT
```

and bind its exact value into build provenance/fingerprint.

# 8. runtime image-ID vs static config separation

The future runtime image ID does not exist until Cut B.

Define exactly what tracked `stockroom-tools.v2.toml` can contain before Cut B.

It must not contain a fabricated future image ID.

Choose one static config model:

```text
IMAGE_PROVENANCE_CONTRACT_REF
IMAGE_IDENTITY_POLICY_AND_PROVENANCE_REF
OTHER_EXACT_STATIC_POLICY
```

Define exact required fields.

Then define which runtime object carries:

```text
actual admitted local image ID sha256:<config-id>
provenance fingerprint/ref
source aggregate
build contract version
base image identity
```

# 9. provenance schema and owner

Resolve the canonical schema for:

```text
.aiassistant/records/aiscc/runtime/stockroom-image-provenance.v1.json
```

At minimum specify:

```text
schema_id/version
provenance_id/version
issuing task/cycle/judgment refs
image identity model
actual image ID
optional discovery tag
Docker server OS/arch/version
base-image immutable identity
Dockerfile path/hash
build contract version
source commit/subroot/subtree
resource ref/source aggregate/file count
Python version
runtime argv/workdir/user/network
required labels
canonical inspect projection hash
issued_at
```

No machine-specific path, credential, or mutable tag as authority.

Define exact source owner for:

```text
parse
canonical fingerprint
currentness verification
runtime admission
```

Do not leave provenance validation only in Task prose.

# 10. production composition binding

Define how:

```text
build_stockroom_production(...)
```

obtains the admitted image provenance.

Choose exact dependency shape:

```text
typed StockroomImageProvenance object
typed provenance ref + resolver
exact immutable image ID + verified provenance object
other exact design
```

Requirements:

```text
production composition cannot synthesize provenance
config cannot mint actual image ID
DockerRunSpec receives exact admitted image ID
runner re-verifies exact local image ID and required labels before create
composition fingerprint binds provenance identity
```

# 11. Cut A must work before Cut B

Prove the source implementation/tests in Cut A can be complete while no built Stockroom
image or image-provenance JSON exists yet.

Use test fixtures issued by test-only provenance constructors only if they cannot be
mistaken for production admission.

Explicitly answer:

```text
How are production constructors fail-closed when provenance is absent?

How do unit/integration tests create an authentic typed provenance fixture without
creating a real Docker image?

Which tests prove a tag-only or source-aggregate pseudo-image cannot enter DockerRunSpec?
```

# 12. Dockerfile/build-context contract

Reconcile Dockerfile and `.dockerignore` with the immutable historical 14-file source
resource.

The build definition is not part of the 14-file resource aggregate.

Specify:

```text
build context root
which exact 14 source paths are admitted into the context
Dockerfile/.dockerignore treatment
pre-build verification against source commit/resource manifest
whether current worktree bytes or git-archive bytes are used
how extra files are excluded
```

Avoid silently treating the current mutable subroot as the accepted source commit.

# 13. corrected Cut A allowlist

Re-evaluate the 2140 first-cut allowlist.

For every previously proposed path classify:

```text
REQUIRED
NOT_REQUIRED
DEFER_TO_CUT_B
NO_CHANGE_NEIGHBOR
```

Previously proposed:

```text
src/aiscc/bootstrap.py
src/aiscc/runtime/docker.py
src/aiscc/providers/stockroom_tool.py
src/aiscc/providers/local_deterministic.py
src/aiscc/scenarios/composition.py
src/aiscc/scenarios/enrollment.py
src/aiscc/scenarios/driver.py
src/aiscc/scenarios/stockroom_production.py
src/aiscc/security/stockroom_policy.py
config/providers/stockroom-tools.v2.toml
config/providers/stockroom-owner-profiles.v2.toml
config/security/stockroom-owner.v2.toml
examples/synthetic-stockroom/Dockerfile
examples/synthetic-stockroom/.dockerignore
examples/synthetic-stockroom/IMAGE_PROVENANCE.md
tests/unit/runtime/test_stockroom_docker_settlement.py
tests/unit/providers/test_stockroom_tool.py
tests/unit/security/test_stockroom_policy.py
tests/unit/scenarios/test_stockroom_capture_runner.py
tests/integration/scenarios/test_stockroom_binding.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

The final next Task allowlist must contain only `REQUIRED` paths.

# 14. preserved DB/runtime-root decisions

Re-check, but do not reopen without contrary source evidence:

```text
PERSISTENT_DB_MODEL =
DEDICATED_LOCAL_DOCKER_POSTGRESQL_NAMED_VOLUME

PERSISTENT_DB_SOURCE_CHANGE_REQUIRED =
NO

RUNTIME_ROOT_MODEL =
TASK_SCOPED_ROOT_ONLY

RUNTIME_ROOT_SOURCE_CHANGE_REQUIRED =
NO
```

If current source contradicts either, report the exact contradiction.

# 15. corrected cut ordering

Produce final ordering:

```text
Cut A:
source/config/test implementation only

Cut B:
environment image build + image provenance issuance
+ persistent DB provisioning

Cut C:
admitted provenance + DB + runtime-root + trusted Docker runner binding readiness

Cut D:
private S1 execution
```

State what Browser acceptance/persistence is required between cuts.

# 16. exact decisions

Success requires exact answers:

```text
BASE_IMAGE_PIN_MODEL
BASE_IMAGE_PIN_AUTHORITY
UNSUPPORTED_2140_BASE_DIGEST_DISPOSITION

V2_TOOL_CONFIG_IMAGE_BINDING_MODEL
IMAGE_PROVENANCE_SCHEMA
IMAGE_PROVENANCE_SOURCE_OWNER
PRODUCTION_PROVENANCE_DEPENDENCY

DOCKERFILE_BUILD_CONTEXT_MODEL
CUT_A_ALLOWLIST
CUT_B_PROVISIONING_INPUTS
CUT_C_CURRENTNESS_BINDING
```

No unsupported exact digest and no `UNKNOWN`.

# 17. contract review

Require:

```text
NO_PRODUCT_MUTATION
NO_CONFIG_MUTATION
NO_DOCKER_PULL
NO_DOCKER_BUILD
NO_DOCKER_CREATE_RUN
NO_REGISTRY_NETWORK_LOOKUP
NO_PERSISTENT_DB_CREATE
NO_ACTUAL_S1
UNSUPPORTED_DIGEST_NOT_ADMITTED
STATIC_CONFIG_DOES_NOT_CONTAIN_FUTURE_IMAGE_ID
RUNTIME_IMAGE_ID_COMES_ONLY_FROM_ADMITTED_PROVENANCE
BASE_IMAGE_AUTHORITY_EXPLICIT
BUILD_CONTEXT_BINDS_HISTORICAL_14_FILE_SOURCE
CUT_A_IMPLEMENTABLE_WITHOUT_BUILT_IMAGE
EXACT_ALLOWLIST_RESOLVED
```

Require:

```text
15 / 15 PASS
```

# 18. final workspace

Before Task movement:

```text
Git-visible:
8 exact
index empty
```

Move active Task byte-identically to:

```text
.aiassistant/tasks/done/20260911_2148_aiscc-p2-3-private-s1-image-build-input-authority-reconciliation-audit-1.md
```

Final:

```text
Git-visible:
9 exact
index empty
```

Exact final set:

- `.aiassistant/tasks/done/20260911_1935_aiscc-p2-3-actual-capture-runtime-prerequisite-verification-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_1935_aiscc-p2-3-a2-terminal-persisted-runtime-prerequisite-verification-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1935_aiscc-p2-3-a2-terminal-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260911_2140_aiscc-p2-3-private-s1-runtime-provisioning-contract-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_2140_aiscc-p2-3-runtime-prerequisite-not-ready-provisioning-contract-audit-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2140_aiscc-p2-3-runtime-prerequisite-verification-final-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_2148_aiscc-p2-3-provisioning-contract-partial-hold-image-build-authority-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2148_aiscc-p2-3-provisioning-contract-audit-image-build-authority-gap-judgment-1.md`
- `.aiassistant/tasks/done/20260911_2148_aiscc-p2-3-private-s1-image-build-input-authority-reconciliation-audit-1.md`

# 19. required export

Folder:

```text
.aiassistant/reports/target/20260911_2148_aiscc-p2-3-private-s1-image-build-input-authority-reconciliation-audit-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
BASE_IMAGE_AUTHORITY_AUDIT.md
IMAGE_CONFIG_PROVENANCE_CONTRACT.md
PRODUCTION_PROVENANCE_BINDING.md
BUILD_CONTEXT_CONTRACT.md
CORRECTED_IMPLEMENTATION_ALLOWLIST.md
CUT_ORDERING.md
CONTRACT_REVIEW.md
```

Also include byte-preserving:

```text
current Cycle
current Judgment
current done Task
```

Export up to 16 source-evidence files directly required by the final corrected allowlist.

Expected total:

```text
14 + N
where 0 <= N <= 16
```

Manifest covers all non-self entries.

# 20. success ceiling

Success:

```text
provisioning architecture:
FULLY RESOLVED

Cut A source implementation:
READY_FOR_BROWSER_AUTHORIZATION

Cut B provisioning:
NOT_EXECUTED

private S1:
NOT_AUTHORIZED
```
