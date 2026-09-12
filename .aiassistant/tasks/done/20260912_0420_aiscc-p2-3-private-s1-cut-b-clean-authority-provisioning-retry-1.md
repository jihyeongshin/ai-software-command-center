# 작업지시서: P2-3 private S1 Cut B clean-authority provisioning retry

## meta

- task_id: `20260912_0420_aiscc-p2-3-private-s1-cut-b-clean-authority-provisioning-retry-1`
- predecessor_task: `.aiassistant/tasks/done/20260912_0410_aiscc-p2-3-private-s1-cut-b-self-reference-correction-provisioning-retry-1.md`
- created_at: `2026-09-12T04:20:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `ENVIRONMENT_PROVISIONING / CUT_B / CLEAN_AUTHORITY_RETRY`
- evidence_profile: `HIGH_RISK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `0fe2105f35b4fcf9769ae76361cb42b47220ac7d`
- required_tree: `a46a8816acc34214983925fe02ed77df55f6b909`
- accepted_cut_a_commit: `750c37aecb4c264f66aabf12dedb8d54e20a7f95`
- authorization_cycle_ref: `.aiassistant/records/aiscc/cycles/20260912_0259_aiscc-p2-3-cut-a-persisted-cut-b-environment-provisioning-entry-1.cycle.md`
- authorization_judgment_ref: `.aiassistant/reports/aiscc/20260912_0259_aiscc-p2-3-cut-a-persistence-final-acceptance-cut-b-authorization-judgment-1.md`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- fresh_ide_executor_chat_reason: `same Cut B provisioning authority; 0410 stopped before any Docker/environment side effect`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. authority ceiling

This Task provisions the private S1 environment only.

Authorized semantic owners:

```text
RUNTIME_IMAGE_PROVISIONING
DATABASE_PROVISIONING
```

Success ceiling:

```text
PROVISIONED_CANDIDATE / BROWSER_JUDGMENT_REQUIRED
```

Not authorized:

```text
Cut B Git persistence
Cut C final runtime-root/readiness binding
private S1 execution
S2-S4 execution
Replay
public runtime
```

## issued identity roles

The following roles are distinct and MUST NOT be substituted for one another:

```text
AUTHORIZATION_CYCLE:
.aiassistant/records/aiscc/cycles/20260912_0259_aiscc-p2-3-cut-a-persisted-cut-b-environment-provisioning-entry-1.cycle.md

AUTHORIZATION_JUDGMENT:
.aiassistant/reports/aiscc/20260912_0259_aiscc-p2-3-cut-a-persistence-final-acceptance-cut-b-authorization-judgment-1.md

COMPLETED_PREDECESSOR_TASK:
.aiassistant/tasks/done/20260912_0410_aiscc-p2-3-private-s1-cut-b-self-reference-correction-provisioning-retry-1.md

CURRENT_ACTIVE_TASK:
.aiassistant/tasks/active/20260912_0420_aiscc-p2-3-private-s1-cut-b-clean-authority-provisioning-retry-1.md

CURRENT_DONE_TASK:
.aiassistant/tasks/done/20260912_0420_aiscc-p2-3-private-s1-cut-b-clean-authority-provisioning-retry-1.md

CURRENT_RETRY_CYCLE:
.aiassistant/records/aiscc/cycles/20260912_0420_aiscc-p2-3-cut-b-clean-authority-provisioning-retry-entry-1.cycle.md

CURRENT_RETRY_JUDGMENT:
.aiassistant/reports/aiscc/20260912_0420_aiscc-p2-3-cut-b-historical-baseline-path-mismatch-retry-judgment-1.md

RESOURCE_OWNER_TASK_ID:
20260912_0420_aiscc-p2-3-private-s1-cut-b-clean-authority-provisioning-retry-1

EXPORT_STEM:
20260912_0420_aiscc-p2-3-private-s1-cut-b-clean-authority-provisioning-retry-1
```

Candidate image/DB provenance issuance is anchored to the accepted 0259 authorization
Cycle/Judgment. Current retry Cycle/Judgment are retry provenance only.

# 1. Python / executable discipline

Do not assume bare:

```text
python
python3
py
docker
git
```

Use exact repository Python when valid:

```text
.venv\Scripts\python.exe
```

Trusted Git accepted by prior prerequisite evidence:

```text
C:\Program Files\Git\cmd\git.exe
```

Verify it before use.

Discover Docker executable read-only, resolve it to one absolute existing file, and
then use only that exact absolute executable for this Task.

Do not export the literal resolved Docker path.

No inline `python -c` for mandatory gates. Use external Task-owned temporary `.py`
scripts outside the repository.

# 2. inbound transport

Verify Browser ZIP filename/SHA-256 from the Short Prompt.

Place the current Task first:

```text
.aiassistant/tasks/active/20260912_0420_aiscc-p2-3-private-s1-cut-b-clean-authority-provisioning-retry-1.md
```

Read fully and require:

```text
current Task exists byte-exact
current Task is ignored by canonical Git policy
```

Do not test the current active Task for absence.

Require these failed-attempt active Tasks are absent:

```text
.aiassistant/tasks/active/20260912_0310_aiscc-p2-3-private-s1-cut-b-environment-provisioning-contract-count-correction-retry-1.md
.aiassistant/tasks/active/20260912_0400_aiscc-p2-3-private-s1-cut-b-identity-ownership-correction-provisioning-retry-1.md
.aiassistant/tasks/active/20260912_0410_aiscc-p2-3-private-s1-cut-b-self-reference-correction-provisioning-retry-1.md
```

If any predecessor active Task exists:

```text
UNEXPECTED_PREDECESSOR_ACTIVE_TASK
→ STOP
no Docker/environment side effect
no report/export
```

Then place/hash-verify the current retry artifacts:

```text
.aiassistant/records/aiscc/cycles/20260912_0420_aiscc-p2-3-cut-b-clean-authority-provisioning-retry-entry-1.cycle.md
SHA-256:
d3ba1c85183e6e594eccee45eb0d51a141260e0ac10b6e7fe9efd81d7325c50a

.aiassistant/reports/aiscc/20260912_0420_aiscc-p2-3-cut-b-historical-baseline-path-mismatch-retry-judgment-1.md
SHA-256:
cd5ee11d34d5711de6e8e1ce24aece0bb58ee731febc8516c86c3be24b49a603
```

Any archive/member/current-artifact mismatch:

```text
STOP
no Docker/environment side effect
no report/export
```

# 3. repository gate

Require:

```text
branch:
main

HEAD:
0fe2105f35b4fcf9769ae76361cb42b47220ac7d

HEAD tree:
a46a8816acc34214983925fe02ed77df55f6b909

HEAD^:
750c37aecb4c264f66aabf12dedb8d54e20a7f95

index:
empty

tracked worktree:
clean
```

Before this delivery exact Git-visible governance baseline:

```text
9 exact
```

Exact predecessor path/hash pairs:

- `.aiassistant/records/aiscc/cycles/20260912_0259_aiscc-p2-3-cut-a-persisted-cut-b-environment-provisioning-entry-1.cycle.md`  `2da742f803b402b39f0433a0e1fabb74c8a594b93cd782555797b05d18cfc9c2`
- `.aiassistant/reports/aiscc/20260912_0259_aiscc-p2-3-cut-a-persistence-final-acceptance-cut-b-authorization-judgment-1.md`  `d64582a0a3b7040cf4a56961d7905b194949716eda98e9832a66a1c68996629d`
- `.aiassistant/tasks/done/20260912_0259_aiscc-p2-3-private-s1-cut-b-environment-provisioning-1.md`  `46b9fb7d030053eb12ac75827475ab136c12cb51b83e3a82b5516b7feee80b96`
- `.aiassistant/records/aiscc/cycles/20260912_0348_aiscc-p2-3-cut-b-artifact-hash-correction-provisioning-retry-entry-1.cycle.md`  `f8e7614602db171c3059ba279548a02252ccefb9e2eeb7d86d4fcb602dcf38f0`
- `.aiassistant/reports/aiscc/20260912_0348_aiscc-p2-3-cut-b-artifact-hash-contract-defect-retry-judgment-1.md`  `813bcdcfd13d8e4164bc09761d56ce30e5dc49a54c81d6928011df8bd19c657b`
- `.aiassistant/tasks/done/20260912_0348_aiscc-p2-3-private-s1-cut-b-artifact-hash-correction-provisioning-retry-1.md`  `dd82f0087a4c93131012a0bf6955c3e78116d39fae11dd79bee3818849589a1b`
- `.aiassistant/records/aiscc/cycles/20260912_0410_aiscc-p2-3-cut-b-self-reference-corrected-provisioning-retry-entry-1.cycle.md`  `93f5b7dc5ff55ee7dfe212c79a53e0e7cc1d05b7aafbda7b39f7523947ec8fdc`
- `.aiassistant/reports/aiscc/20260912_0410_aiscc-p2-3-cut-b-self-reference-contract-defect-retry-judgment-1.md`  `78f4ec2f7feb8fac541eb7c258bf39eb359515c4a565a1c4edf0bd4c491618a1`
- `.aiassistant/tasks/done/20260912_0410_aiscc-p2-3-private-s1-cut-b-self-reference-correction-provisioning-retry-1.md`  `9bc85a68c11d56d533923b605a029671365304ba729f17fedbeede1577ceccac`

After current retry Cycle/Judgment placement while the current Task remains active:

```text
Git-visible:
11 exact

current active Task:
exists byte-exact
ignored
```

Exact visible set:

```text
.aiassistant/records/aiscc/cycles/20260912_0259_aiscc-p2-3-cut-a-persisted-cut-b-environment-provisioning-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_0259_aiscc-p2-3-cut-a-persistence-final-acceptance-cut-b-authorization-judgment-1.md
.aiassistant/tasks/done/20260912_0259_aiscc-p2-3-private-s1-cut-b-environment-provisioning-1.md
.aiassistant/records/aiscc/cycles/20260912_0348_aiscc-p2-3-cut-b-artifact-hash-correction-provisioning-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_0348_aiscc-p2-3-cut-b-artifact-hash-contract-defect-retry-judgment-1.md
.aiassistant/tasks/done/20260912_0348_aiscc-p2-3-private-s1-cut-b-artifact-hash-correction-provisioning-retry-1.md
.aiassistant/records/aiscc/cycles/20260912_0410_aiscc-p2-3-cut-b-self-reference-corrected-provisioning-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_0410_aiscc-p2-3-cut-b-self-reference-contract-defect-retry-judgment-1.md
.aiassistant/tasks/done/20260912_0410_aiscc-p2-3-private-s1-cut-b-self-reference-correction-provisioning-retry-1.md
.aiassistant/records/aiscc/cycles/20260912_0420_aiscc-p2-3-cut-b-clean-authority-provisioning-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_0420_aiscc-p2-3-cut-b-historical-baseline-path-mismatch-retry-judgment-1.md
```

No duplicate path is permitted.

Require exact canonical state:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `01c6f173737924d0fb0fd9deb0c5b66ea78fec499841aa76a61c2b781c17cc65`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `f2004f24ea0ef369702df1f3a0dff2efa9d27642fdff62c816f536d347cff581`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `5ff255dfb6a276d9755cea8af564b0882a9546e97e511e2d0028cada625a171e`

Require all 19 accepted Cut A paths exact:

- `src/aiscc/bootstrap.py`  `745b58da26ec300286ed69d1a7477b21afeb7625ec43e7f422560a657bc1c115`
- `src/aiscc/providers/local_deterministic.py`  `92ec8ba5553b05fe55fdbac30ab2dde8f57597c1055060a2f786dadd47f1c21a`
- `src/aiscc/providers/stockroom_tool.py`  `c5c925df000656ce32f65f4742f9a6936c2364d7d58eb92750966d8a8826e075`
- `src/aiscc/runtime/docker.py`  `284a3920f13f93928cc61420913506ed38af4e8f4d4e0e1f52d52c9074fa0753`
- `src/aiscc/runtime/stockroom_image.py`  `06e8d85e449a336392b73d9dec9915cd32d776688575a64030024609b08cec0e`
- `src/aiscc/scenarios/composition.py`  `a5f7ecb0d1bd9274f07094cbe3a4315098048c468472162e0ad84372fe6c50d3`
- `src/aiscc/scenarios/stockroom_production.py`  `685e2ec549473e167ed1fe4d7de1050d7a53a449d1d278dcdb3439a471478f1f`
- `config/providers/stockroom-owner-profiles.v2.toml`  `3f20d2d1ac4dd45709c47fc6572db4b97d6c33e0bebf02c6fd489dd9adbd022a`
- `config/providers/stockroom-tools.v2.toml`  `16015a97a00098e26f89a2972c87fd5ce0f4516c1afdf2bc20126fe6d1c61385`
- `examples/synthetic-stockroom/.dockerignore`  `99637a64da3b1b13bbf9a52459098d07bbc865aca11d004c89c3ee48965849f9`
- `examples/synthetic-stockroom/Dockerfile`  `94f71d8bf4b2f87e678e1a379dead19b7a850cf4522ec835bf6455f95d72b27a`
- `examples/synthetic-stockroom/IMAGE_PROVENANCE.md`  `166cfec29db4f46477b0117fae85a6a937343e3fb019a9b668b223b2eea8bae3`
- `tests/integration/scenarios/test_stockroom_binding.py`  `3979ff742a2c82752a7fbccb095b4ab8a4ed4915331ba4ec9d09cfa24aa3d4cf`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`  `373f9d5bc6f260785cdf943aa649ce99ab5826e8ae09dd2982c18db09459fbf5`
- `tests/unit/providers/test_local_deterministic.py`  `daa58e09dd3e81f2ba4a6edad236685c34a7c63852419ad3188aef51c8fe6209`
- `tests/unit/providers/test_stockroom_tool.py`  `e33b966cf5d575b7e55cd1ced2f3bfcd805833c08c1c66d6c650b693313c285d`
- `tests/unit/runtime/test_stockroom_docker_settlement.py`  `f7a33975072737417b3a922d4acd44e59be29547ceb87c864e24647d46236b19`
- `tests/unit/runtime/test_stockroom_image.py`  `e900bf8db350762655a167def704989527928cef575f69e740b013e5bfa4cee7`
- `tests/unit/scenarios/test_owner_composition.py`  `bfbae533d8453bef3940b1b652c5688b3b375b7e0fa40ae03e3196902888d652`

Any mismatch:

```text
CUT_B_BASE_AUTHORITY_MISMATCH
→ STOP_WITH_REPORT_EXPORT
```


# 4. zero source/config/test mutation

No modification is authorized under:

```text
src/**
config/**
tests/**
examples/**
migrations/**
pyproject.toml
lock files
.gitignore
three canonical state records
```

The only tracked files Cut B may create are:

```text
.aiassistant/records/aiscc/runtime/stockroom-image-provenance.v1.json
.aiassistant/records/aiscc/runtime/stockroom-private-postgres-provisioning.v1.json
```

Do not stage or commit anything.

# 5. exact accepted source/build authority

Require current resource manifest:

```text
config/scenarios/stockroom/v1/resource.json

SHA-256:
a5b8c8a5bd7165073f37647eb791df0bc59aa7b73033d59dd5f3967bbff28a99
```

Required historical source authority:

```text
source commit:
05185c57a6265a4002050ce25cdfde3dc87e9779

subroot:
examples/synthetic-stockroom/

Git subtree:
f3d9203321ae3535abf8e92a7285da1067f6c55e

file count:
14

aggregate:
be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d
```

Require Git object access to the source commit and subtree.

Do not source the 14 payload files from the mutable worktree.

# 6. exact 14-file resource inventory

Read the 14 entries from the accepted resource manifest.

For each entry, verify from Git objects at:

```text
05185c57a6265a4002050ce25cdfde3dc87e9779:examples/synthetic-stockroom/<relative-path>
```

exact:

```text
path
mode
byte size
SHA-256
```

Require:

```text
14 / 14 exact
aggregate contract exact
no extra member
no symlink/submodule
```

Any mismatch:

```text
HISTORICAL_SOURCE_IDENTITY_MISMATCH
→ STOP_WITH_REPORT_EXPORT
```

# 7. external exact build context

Create one Task-owned temporary build-context directory outside:

```text
repository
Downloads
Git object store
private PostgreSQL storage
```

Do not report/export the literal machine path.

Assemble exactly:

```text
Dockerfile
.dockerignore
source/<14 exact historical resource files>
```

`Dockerfile` and `.dockerignore` come from the accepted Cut A HEAD and must hash:

```text
Dockerfile:
94f71d8bf4b2f87e678e1a379dead19b7a850cf4522ec835bf6455f95d72b27a

.dockerignore:
99637a64da3b1b13bbf9a52459098d07bbc865aca11d004c89c3ee48965849f9
```

Context inventory must be:

```text
16 exact regular files
0 symlink/reparse
0 extra
```

`IMAGE_PROVENANCE.md` is NOT a build-context member.

Record a canonical context-inventory fingerprint over relative path, byte size and
SHA-256.

# 8. base Python image local authority

Exact base authority:

```text
python@sha256:0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579
```

Using local read-only Docker inspect only, require:

```text
exact RepoDigest membership:
PASS

Os:
linux

Architecture:
amd64

Config.Env contains:
PYTHON_VERSION=3.12.14
```

Record `.Id` separately from RepoDigest.

Forbidden:

```text
docker pull
registry API lookup
docker manifest inspect
alternate/floating base
```

If the exact base is not already local:

```text
BASE_IMAGE_LOCAL_AUTHORITY_MISSING
→ STOP_WITH_REPORT_EXPORT
```

# 9. Stockroom discovery tag precondition

Exact non-authoritative discovery tag:

```text
aiscc-stockroom-runtime:p2-3-private-v1
```

Require before build:

```text
tag absent
```

Do not overwrite or retag an existing image.

The tag is discovery only. Runtime authority will be the resulting immutable local
image config ID.

# 10. Stockroom image build

Build exactly from the Task-owned 16-file context.

Required build semantics:

```text
Dockerfile:
accepted Cut A Dockerfile

base:
python@sha256:0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579

pull:
false / never

build network:
none

secret build args:
none

build secret mounts:
none

build arg:
AISCC_DOCKERFILE_SHA256=94f71d8bf4b2f87e678e1a379dead19b7a850cf4522ec835bf6455f95d72b27a

tag:
aiscc-stockroom-runtime:p2-3-private-v1

push:
forbidden
```

Use the exact absolute Docker executable.

If the local build attempts to require a registry pull or missing external dependency:

```text
BUILD_LOCAL_INPUT_INCOMPLETE
→ fail
```

Do not widen network authority.

# 11. immutable Stockroom image inspect

After successful build, resolve:

```text
STOCKROOM_IMAGE_ID = exact .Id
```

Require:

```text
sha256:<64 lowercase hex>
not sha256:be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d
Os == linux
Architecture == amd64
Config.User == 65532:65532
Config.WorkingDir == /workspace
RepoTags contains exactly the required discovery tag for this Task
Config.Env contains PYTHON_VERSION=3.12.14
```

Verify required labels exactly:

```text
io.aiscc.stockroom.build-contract= AISCC-STOCKROOM-RUNTIME-BUILD-V1
io.aiscc.stockroom.source-commit= 05185c57a6265a4002050ce25cdfde3dc87e9779
io.aiscc.stockroom.source-subroot= examples/synthetic-stockroom/
io.aiscc.stockroom.git-subtree= f3d9203321ae3535abf8e92a7285da1067f6c55e
io.aiscc.stockroom.resource-ref= repository:synthetic-stockroom@be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d
io.aiscc.stockroom.source-aggregate= be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d
io.aiscc.stockroom.source-file-count= 14
io.aiscc.stockroom.python-version= 3.12.14
io.aiscc.stockroom.dockerfile-sha256= 94f71d8bf4b2f87e678e1a379dead19b7a850cf4522ec835bf6455f95d72b27a
io.aiscc.stockroom.base-repodigest= python@sha256:0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579
```

Do not create or start a Stockroom runtime container.

# 12. raw image-inspect evidence

Capture exact:

```text
docker image inspect <STOCKROOM_IMAGE_ID>
```

JSON.

Review it before export.

Require no secret-like material.

The raw image inspect may be exported only after that review.

Do not export the Task-owned build-context path.

# 13. candidate image provenance JSON

Create exactly:

```text
.aiassistant/records/aiscc/runtime/stockroom-image-provenance.v1.json
```

This is a candidate provisioning record, not yet Browser-admitted/persisted.

Root keys must match the strict Cut A source schema exactly:

```text
schema_id
schema_version
provenance_id
provenance_version
issuance
image
base_image
build
source
runtime
required_labels
inspect_projection_sha256
issued_at
```

Exact fixed values:

```text
schema_id:
AISCC-STOCKROOM-IMAGE-PROVENANCE-V1

schema_version:
1.0.0

provenance_id:
stockroom-runtime-p2-3-private-v1

provenance_version:
1

issuance.accepted_cycle_ref:
.aiassistant/records/aiscc/cycles/20260912_0259_aiscc-p2-3-cut-a-persisted-cut-b-environment-provisioning-entry-1.cycle.md

issuance.accepted_judgment_ref:
.aiassistant/reports/aiscc/20260912_0259_aiscc-p2-3-cut-a-persistence-final-acceptance-cut-b-authorization-judgment-1.md

image.identity_model:
LOCAL_IMAGE_CONFIG_ID_SHA256

image.image_id:
<STOCKROOM_IMAGE_ID>

image.os:
linux

image.architecture:
amd64

image.discovery_tag:
aiscc-stockroom-runtime:p2-3-private-v1

base_image.pin_model:
SOURCE_FIXED_VERIFIED_REPODIGEST

base_image.repodigest:
python@sha256:0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579

build.contract_version:
AISCC-STOCKROOM-RUNTIME-BUILD-V1

build.context_model:
TASK_SCOPED_GIT_OBJECT_ASSEMBLED_EXACT_CONTEXT

build.dockerfile_sha256:
94f71d8bf4b2f87e678e1a379dead19b7a850cf4522ec835bf6455f95d72b27a

build.dockerignore_sha256:
99637a64da3b1b13bbf9a52459098d07bbc865aca11d004c89c3ee48965849f9

source.commit:
05185c57a6265a4002050ce25cdfde3dc87e9779

source.subroot:
examples/synthetic-stockroom/

source.git_subtree:
f3d9203321ae3535abf8e92a7285da1067f6c55e

source.resource_ref:
repository:synthetic-stockroom@be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d

source.aggregate_sha256:
be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d

source.file_count:
14

runtime.python_version:
3.12.14

runtime.argv:
["python","-B","-m","stockroom","summary"]

runtime.workdir:
/workspace

runtime.user:
65532:65532

runtime.network:
none
```

`required_labels` must be the exact required map from accepted source.

`inspect_projection_sha256` must be computed from the exact selected projection owned
by:

```text
src/aiscc/runtime/stockroom_image.py::inspect_projection
```

using the built image raw inspect.

`issued_at` must be timezone-aware.

Serialize as UTF-8 JSON with no secret, credential, machine path or Docker executable
path.

# 14. candidate image provenance verification

Using accepted source APIs only:

```text
parse_provenance
provenance_payload
canonical_fingerprint
inspect_projection
```

prove:

```text
strict schema PASS
unknown key rejection remains applicable
required labels exact
build/source/static-policy currentness exact
inspect projection hash exact
whole-file SHA-256 captured
canonical provenance fingerprint captured
```

Do NOT call the production resolver to claim Browser admission.

Do NOT construct/run `StockroomDockerRunner`.

The current Cycle/Judgment are the accepted authorization under which this candidate
was issued. Later Browser provisioning acceptance does not rewrite these issuance
fields.

# 15. PostgreSQL software authority

Exact PostgreSQL image authority:

```text
postgres@sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94
```

Require the exact RepoDigest is already local.

Inspect and record separately:

```text
RepoDigest
local image .Id
Os
Architecture
```

Forbidden:

```text
docker pull
registry lookup
alternate PostgreSQL image
```

If absent:

```text
POSTGRES_IMAGE_LOCAL_AUTHORITY_MISSING
→ fail
```

# 16. persistent DB exact identity preconditions

Exact environment identity:

```text
container:
aiscc-p2-3-private-postgres-v1

volume:
aiscc-p2-3-private-postgres-data-v1

database:
aiscc_private_capture

role:
aiscc_private_capture

host:
127.0.0.1

host port:
55432

container port:
5432

migration head:
20260901_0008
```

Before creation require:

```text
container name absent
volume name absent
127.0.0.1:55432 bindable/free
```

Port collision is a blocker.

Do not select another port silently.

# 17. external private password file

Generate a strong random password using a Task-owned external temporary helper.

Requirements:

```text
at least 48 random bytes of entropy before encoding
value never printed
value never hashed into reports
value never written to repository
value never placed in Docker environment as POSTGRES_PASSWORD
```

Create a retained private password file outside:

```text
repository
Downloads
Git object store
export directory
```

Use an operator-private local filesystem location.

The literal absolute path must not appear in:

```text
Task reports
tracked JSON
export
Git
```

Prove effective ACL/private access before PostgreSQL container creation.

If private ACL cannot be proven:

```text
SECRET_FILE_PRIVATE_BOUNDARY_UNPROVEN
→ fail before DB creation
```

Container credential mechanism:

```text
POSTGRES_PASSWORD_FILE
```

with exact read-only bind destination:

```text
/run/secrets/postgres_password
```

The file remains after successful Cut B for later Cut C/S1-S4 lifecycle.

# 18. exact persistent volume

Create exact volume:

```text
aiscc-p2-3-private-postgres-data-v1
```

Required labels:

```text
io.aiscc.owner=p2-3-private-capture
io.aiscc.provisioning-id=aiscc-p2-3-private-postgres-v1
io.aiscc.lifecycle=p2-3-s1-s4-corpus
io.aiscc.task-id=20260912_0420_aiscc-p2-3-private-s1-cut-b-clean-authority-provisioning-retry-1
```

Require Docker local volume driver.

No other volume.

# 19. exact PostgreSQL container

Create/start exact container from:

```text
postgres@sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94
```

with:

```text
--pull=never

name:
aiscc-p2-3-private-postgres-v1

labels:
same owner/provisioning/lifecycle/task identity

database:
POSTGRES_DB=aiscc_private_capture

role:
POSTGRES_USER=aiscc_private_capture

password:
POSTGRES_PASSWORD_FILE=/run/secrets/postgres_password

data volume:
aiscc-p2-3-private-postgres-data-v1
→ /var/lib/postgresql/data

password bind:
external private file
→ /run/secrets/postgres_password
read-only

published endpoint:
127.0.0.1:55432:5432
```

No other published interface/port.

Do not export raw container inspect because its bind mount may reveal the host secret
path.

# 20. sanitized PostgreSQL inspect projection

From local Docker inspect, generate an exported sanitized projection containing only:

```text
container ID
container name
image RepoDigest authority
image local ID
labels
state/status
published IP/host-port/container-port
data volume name + destination + rw
secret bind destination + read-only boolean
database name
role name
POSTGRES_PASSWORD_FILE container destination
```

Explicitly exclude:

```text
host secret bind source path
password value
connection URL
Docker internal host storage paths
```

Hash the canonical sanitized projection.

# 21. migration

Wait for PostgreSQL readiness without logging the password.

Construct the private database URL only in process memory from the retained password
file.

Pass connection data only through child-process environment.

Do not place the URL in command arguments or reports.

Use the repository's existing supported Alembic database-URL input exactly as current
tracked migration configuration requires.

If the supported migration URL input cannot be established from current source without
source mutation:

```text
DATABASE_MIGRATION_INPUT_CONTRACT_UNAVAILABLE
→ STOP_WITH_REPORT_EXPORT
```

Run:

```text
alembic upgrade head
alembic current
```

Require exact:

```text
20260901_0008 (head)
```

Also query `alembic_version` directly and require:

```text
20260901_0008
```

# 22. non-domain restart-survival probe

Using a Task-owned external Python probe through `asyncpg`/SQLAlchemy:

Create only:

```text
aiscc_private_provisioning_probe
```

with a single fixed Task-owned probe row.

Commit.

Restart the exact PostgreSQL container.

Require after restart:

```text
same container ID
same volume
same loopback endpoint
database reconnect PASS
migration head still 20260901_0008
probe row still exact
```

Then remove all probe residue:

```text
DROP TABLE aiscc_private_provisioning_probe
```

Require after cleanup:

```text
probe table absent
probe row absent
```

Do not create a WorkRun, execution attempt, evidence, Human, Judgment or scenario row.

# 23. zero domain-state proof

After probe cleanup, enumerate current AISCC persistence table set from tracked
repository models/migrations.

Require all application/domain tables have zero rows except migration metadata or any
explicit migration-owned metadata proven by current schema.

At minimum prove zero for tables owned by:

```text
workflow / WorkRun
execution/provider
evidence
human gate/result
judgment
project memory/cycle admission
scenario capture/domain run state
```

No S1 domain row may exist.

If an unexpected non-migration row exists:

```text
PRIVATE_DB_NOT_PRISTINE
→ fail
```

# 24. candidate DB provisioning JSON

After all PostgreSQL checks PASS, create exactly:

```text
.aiassistant/records/aiscc/runtime/stockroom-private-postgres-provisioning.v1.json
```

Strict root object:

```text
schema_id
schema_version
provisioning_id
provisioning_version
issuance
image
container
volume
database
credential
restart_probe
lifecycle
issued_at
```

Exact semantic values:

```text
schema_id:
AISCC-STOCKROOM-PRIVATE-POSTGRES-PROVISIONING-V1

schema_version:
1.0.0

provisioning_id:
aiscc-p2-3-private-postgres-v1

provisioning_version:
1

issuance.accepted_cycle_ref:
.aiassistant/records/aiscc/cycles/20260912_0259_aiscc-p2-3-cut-a-persisted-cut-b-environment-provisioning-entry-1.cycle.md

issuance.accepted_judgment_ref:
.aiassistant/reports/aiscc/20260912_0259_aiscc-p2-3-cut-a-persistence-final-acceptance-cut-b-authorization-judgment-1.md

image.repodigest:
postgres@sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94

image.image_id:
<exact local PostgreSQL image ID>

image.os:
linux

image.architecture:
amd64

container.name:
aiscc-p2-3-private-postgres-v1

container.id:
<exact 64-hex container ID>

container.labels:
exact Task-owned label map

container.loopback_host:
127.0.0.1

container.host_port:
55432

container.container_port:
5432

volume.name:
aiscc-p2-3-private-postgres-data-v1

volume.driver:
local

volume.labels:
exact Task-owned label map

database.name:
aiscc_private_capture

database.role:
aiscc_private_capture

database.migration_head:
20260901_0008

credential.mechanism_id:
POSTGRES_PASSWORD_FILE_EXTERNAL_PRIVATE_V1

credential.value_exported:
false

credential.path_exported:
false

restart_probe.performed:
true

restart_probe.same_container_id:
true

restart_probe.same_volume:
true

restart_probe.survived_restart:
true

restart_probe.residue_removed:
true

lifecycle.owner:
P2-3_PRIVATE_CAPTURE

lifecycle.retention:
THROUGH_S1_S4_CORPUS_REVIEW_UNTIL_EXPLICIT_DISPOSAL

lifecycle.disposal_status:
RETAINED
```

`issued_at` must be timezone-aware.

The JSON must contain no password, password hash, secret file path, database URL,
machine-specific Docker storage path or runtime-root path.

Serialize deterministically with sorted keys and compact separators.

Capture whole-file SHA-256.

# 25. successful retained environment

On SUCCESS retain exactly:

```text
Stockroom image ID:
<one immutable built image>

Stockroom discovery tag:
aiscc-stockroom-runtime:p2-3-private-v1

PostgreSQL container:
aiscc-p2-3-private-postgres-v1
running

PostgreSQL volume:
aiscc-p2-3-private-postgres-data-v1

external private password file:
retained / private / path not exported

candidate image provenance:
.aiassistant/records/aiscc/runtime/stockroom-image-provenance.v1.json

candidate DB provisioning provenance:
.aiassistant/records/aiscc/runtime/stockroom-private-postgres-provisioning.v1.json
```

Delete only the Task-owned build-context directory and temporary verifier/probe helper
files after their evidence is captured.

Do not remove successful environment resources pending Browser review.

# 26. failure rollback / quarantine

If failure occurs before successful candidate completion, rollback only exact resources
whose Task ownership is proven.

Permitted rollback:

```text
remove exact Task-owned PostgreSQL container
remove exact Task-owned named volume after container absence
remove exact Task-created Stockroom discovery tag
remove exact built image ID only if it is proven this Task's image and has no other refs
remove exact Task-created password file only after DB container is proven absent
remove exact temporary build context/helpers
```

Never broad-clean Docker.

If ownership or Docker settlement is uncertain:

```text
ENVIRONMENT_QUARANTINE_REQUIRED
```

Preserve the uncertain exact resource and report its non-secret identity. Do not widen
cleanup.

# 27. no Cut C / no S1

Forbidden throughout this Task:

```text
create final private runtime root
construct final production application for S1
construct/admit StockroomImageProvenanceRef for runtime use
run StockroomDockerRunner
create/start Stockroom runtime container
materialize synthetic source for scenario execution
create S1 WorkRun
execute provider/tool scenario edge
actual S1-S4
Replay
public release
```

Image build is allowed. Stockroom scenario runtime execution is not.

# 28. Git final gate

Before moving the current Task to done, successful provisioning must have exactly:

```text
Git-visible:
13 exact

.aiassistant/records/aiscc/cycles/20260912_0259_aiscc-p2-3-cut-a-persisted-cut-b-environment-provisioning-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_0259_aiscc-p2-3-cut-a-persistence-final-acceptance-cut-b-authorization-judgment-1.md
.aiassistant/tasks/done/20260912_0259_aiscc-p2-3-private-s1-cut-b-environment-provisioning-1.md
.aiassistant/records/aiscc/cycles/20260912_0348_aiscc-p2-3-cut-b-artifact-hash-correction-provisioning-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_0348_aiscc-p2-3-cut-b-artifact-hash-contract-defect-retry-judgment-1.md
.aiassistant/tasks/done/20260912_0348_aiscc-p2-3-private-s1-cut-b-artifact-hash-correction-provisioning-retry-1.md
.aiassistant/records/aiscc/cycles/20260912_0410_aiscc-p2-3-cut-b-self-reference-corrected-provisioning-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_0410_aiscc-p2-3-cut-b-self-reference-contract-defect-retry-judgment-1.md
.aiassistant/tasks/done/20260912_0410_aiscc-p2-3-private-s1-cut-b-self-reference-correction-provisioning-retry-1.md
.aiassistant/records/aiscc/cycles/20260912_0420_aiscc-p2-3-cut-b-clean-authority-provisioning-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_0420_aiscc-p2-3-cut-b-historical-baseline-path-mismatch-retry-judgment-1.md
.aiassistant/records/aiscc/runtime/stockroom-image-provenance.v1.json
.aiassistant/records/aiscc/runtime/stockroom-private-postgres-provisioning.v1.json

index:
empty
```

No state file change.

Move only the current Task byte-identically:

```text
.aiassistant/tasks/active/20260912_0420_aiscc-p2-3-private-s1-cut-b-clean-authority-provisioning-retry-1.md
→
.aiassistant/tasks/done/20260912_0420_aiscc-p2-3-private-s1-cut-b-clean-authority-provisioning-retry-1.md
```

Final successful Git-visible set:

```text
14 exact

.aiassistant/records/aiscc/cycles/20260912_0259_aiscc-p2-3-cut-a-persisted-cut-b-environment-provisioning-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_0259_aiscc-p2-3-cut-a-persistence-final-acceptance-cut-b-authorization-judgment-1.md
.aiassistant/tasks/done/20260912_0259_aiscc-p2-3-private-s1-cut-b-environment-provisioning-1.md
.aiassistant/records/aiscc/cycles/20260912_0348_aiscc-p2-3-cut-b-artifact-hash-correction-provisioning-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_0348_aiscc-p2-3-cut-b-artifact-hash-contract-defect-retry-judgment-1.md
.aiassistant/tasks/done/20260912_0348_aiscc-p2-3-private-s1-cut-b-artifact-hash-correction-provisioning-retry-1.md
.aiassistant/records/aiscc/cycles/20260912_0410_aiscc-p2-3-cut-b-self-reference-corrected-provisioning-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_0410_aiscc-p2-3-cut-b-self-reference-contract-defect-retry-judgment-1.md
.aiassistant/tasks/done/20260912_0410_aiscc-p2-3-private-s1-cut-b-self-reference-correction-provisioning-retry-1.md
.aiassistant/records/aiscc/cycles/20260912_0420_aiscc-p2-3-cut-b-clean-authority-provisioning-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_0420_aiscc-p2-3-cut-b-historical-baseline-path-mismatch-retry-judgment-1.md
.aiassistant/records/aiscc/runtime/stockroom-image-provenance.v1.json
.aiassistant/records/aiscc/runtime/stockroom-private-postgres-provisioning.v1.json
.aiassistant/tasks/done/20260912_0420_aiscc-p2-3-private-s1-cut-b-clean-authority-provisioning-retry-1.md
```

Index remains empty.

No Git commit/push.

# 29. contract review

Require:

```text
BASE_HEAD_EXACT
CUT_A_ANCESTRY_EXACT
CANONICAL_STATE_HASHES_EXACT
CUT_A_19_HASHES_EXACT
RESOURCE_MANIFEST_HASH_EXACT
SOURCE_14_GIT_OBJECTS_EXACT
BUILD_CONTEXT_16_EXACT
DOCKERFILE_HASH_EXACT
DOCKERIGNORE_HASH_EXACT
BASE_REPODIGEST_LOCAL_EXACT
NO_BASE_PULL
STOCKROOM_TAG_PREABSENT
STOCKROOM_BUILD_PASS
STOCKROOM_IMAGE_ID_CAPTURED
STOCKROOM_LABELS_EXACT
STOCKROOM_PYTHON_VERSION_EXACT
IMAGE_PROVENANCE_SCHEMA_PASS
IMAGE_PROVENANCE_PROJECTION_PASS
IMAGE_PROVENANCE_NO_SECRET_MACHINE_PATH
POSTGRES_REPODIGEST_LOCAL_EXACT
POSTGRES_PORT_55432_PRECHECK_FREE
POSTGRES_CONTAINER_VOLUME_PREABSENT
SECRET_FILE_PRIVATE_BOUNDARY_PASS
POSTGRES_VOLUME_IDENTITY_EXACT
POSTGRES_CONTAINER_IDENTITY_EXACT
POSTGRES_LOOPBACK_ONLY
MIGRATION_HEAD_20260901_0008
RESTART_SURVIVAL_PASS
PROBE_RESIDUE_ZERO
AISCC_DOMAIN_STATE_ZERO
DB_PROVENANCE_NO_SECRET_MACHINE_PATH
SUCCESS_RESOURCE_INVENTORY_EXACT
BUILD_CONTEXT_TEMP_REMOVED
NO_STOCKROOM_RUNTIME_CONTAINER
NO_PRIVATE_RUNTIME_ROOT
NO_S1
NO_SOURCE_CONFIG_TEST_MUTATION
NO_STATE_MUTATION
NO_GIT_PERSISTENCE
NO_PUSH
NO_REGISTRY_PUSH
```

Require:

```text
41 / 41 PASS
```

# 30. required export

Folder:

```text
.aiassistant/reports/target/20260912_0420_aiscc-p2-3-private-s1-cut-b-clean-authority-provisioning-retry-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
SOURCE_CONTEXT_VERIFICATION.md
BASE_IMAGE_VERIFICATION.md
STOCKROOM_IMAGE_BUILD_VERIFICATION.md
STOCKROOM_IMAGE_INSPECT_RAW.json
STOCKROOM_IMAGE_PROVENANCE_VERIFICATION.md
POSTGRES_IMAGE_VERIFICATION.md
POSTGRES_PROVISIONING_VERIFICATION.md
POSTGRES_SANITIZED_INSPECT.json
POSTGRES_RESTART_PROBE_VERIFICATION.md
SECRET_BOUNDARY_VERIFICATION.md
RESOURCE_INVENTORY.md
ROLLBACK_RETENTION_VERIFICATION.md
FORBIDDEN_ACTION_VERIFICATION.md
CONTRACT_REVIEW.md
```

Also include byte-preserving:

```text
current Cycle
current Judgment
current done Task
.aiassistant/records/aiscc/runtime/stockroom-image-provenance.v1.json
.aiassistant/records/aiscc/runtime/stockroom-private-postgres-provisioning.v1.json
```

Expected:

```text
18 root docs
5 canonical/candidate copies
23 members total
```

`EXPORT_MANIFEST.md` covers all 22 non-self entries with relative path, byte size and
SHA-256.

Before export, secret-scan every exported member for:

```text
password value
database URL
secret absolute host path
private build-context absolute path
```

Any secret/path leak:

```text
SECRET_EXPORT_VIOLATION
→ do not export unsafe bytes
→ STOP_WITH_REPORT_EXPORT using safe redacted reports only
```

Create adjacent ZIP:

```text
one top-level directory
23 exact members
CRC PASS
folder/archive byte equality
```

# 31. success ceiling

Success:

```text
Cut A:
ACCEPTED / PERSISTED

Cut B Stockroom image:
PROVISIONED_CANDIDATE

Cut B image provenance:
ISSUED_CANDIDATE / NOT_BROWSER_ADMITTED

Cut B persistent PostgreSQL:
PROVISIONED_CANDIDATE / RETAINED

Cut B DB provenance:
ISSUED_CANDIDATE / NOT_BROWSER_ADMITTED

Cut B persistence:
NOT_AUTHORIZED

Cut C:
NOT_AUTHORIZED

private S1:
NOT_AUTHORIZED

P2-3:
IN_PROGRESS
```
