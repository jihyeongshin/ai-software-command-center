# AISCC Command Center Judgment

## meta

- judgment_id: `20260912_0010_aiscc-p2-3-base-image-authority-reconciliation-final-acceptance-judgment-1`
- created_at: `2026-09-12T00:10:00+09:00`
- project: `AI Software Command Center (AISCC)`
- submitted_task: `.aiassistant/tasks/done/20260911_2300_aiscc-p2-3-base-image-inspect-identity-reconciliation-retry-after-replay-conflict-1.md`
- submitted_bundle: `20260911_2300_aiscc-p2-3-base-image-inspect-identity-reconciliation-retry-after-replay-conflict-1.zip`
- submitted_bundle_sha256: `ab7fa5a8a39e4259c00eac89e1d585e0969299d111fc7055952f09eafde8c153`
- result_status: `ACCEPTED / BASE_IMAGE_AUTHORITY_RECONCILED`
- provisioning_architecture: `2148_ARCHITECTURE_ACCEPTED_WITH_EVIDENCE_CORRECTION`
- cut_a: `AUTHORIZED_NEXT`
- cut_b: `NOT_AUTHORIZED`
- private_s1: `NOT_AUTHORIZED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`
- handoff_required: `No`
- fresh_ide_executor_chat_for_successor: `REQUIRED`

# 판정

`2300` retry result를 ACCEPT한다.

Browser direct verification:

```text
ZIP / CRC:
PASS

top-level:
1 exact

members:
19 exact

required root docs:
11 / 11

canonical copies:
3 / 3

source evidence:
5 / 5

manifest non-self:
18 / 18 SHA-256 + byte-size PASS

issued 2300 TASK/CYCLE/JUDGMENT:
3 / 3 exact

TASK.md == canonical done Task:
byte exact
```

Submitted ZIP:

```text
SHA-256:
ab7fa5a8a39e4259c00eac89e1d585e0969299d111fc7055952f09eafde8c153
```

# raw Docker identity evidence

Browser independently parsed `BASE_IMAGE_INSPECT_RAW.json`.

Exact current local observation:

```text
.Id:
sha256:0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579

.RepoTags:
["python:3.12.14-slim-bookworm"]

.RepoDigests:
["python@sha256:0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579"]

.Os:
linux

.Architecture:
amd64

raw inspect SHA-256:
cd67997302dedcb0c13c63d4235ac529d34f27b8cc0b383ea86793ea2ca50e65
```

The `.Id` and `.RepoDigests[]` hexadecimal payloads happen to be textually equal in
this local Docker observation.

They remain different semantic identities:

```text
.Id:
local image config object identity

.RepoDigests[]:
repository distribution manifest/index identity
```

# prior accepted P1-3 authority

Current tracked P1-3 Dockerfiles, compose, test fixture and the terminal accepted P1-3
Cycle all use the exact repository-qualified digest:

```text
python@sha256:0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579
```

Terminal P1-3 Cycle SHA-256:

```text
cbbd3f0394298ca5d0dc72e500db8a84a87b4ff83fbbb20d7f98aec5054c2b36
```

Therefore the accepted classification is:

```text
BASE_IMAGE_PIN_MODEL:
SOURCE_FIXED_VERIFIED_REPODIGEST

BASE_IMAGE_PIN_AUTHORITY:
prior accepted P1-3 RepoDigest + current exact local RepoDigest membership
```

The local config ID is observed evidence, not the base pin authority.

# accepted 2148 architecture

The image-identity evidence gap is closed.

Accept:

```text
V2_TOOL_CONFIG_IMAGE_BINDING_MODEL:
IMAGE_IDENTITY_POLICY_AND_PROVENANCE_REF

IMAGE_PROVENANCE_SCHEMA:
AISCC-STOCKROOM-IMAGE-PROVENANCE-V1 / 1.0.0

IMAGE_PROVENANCE_SOURCE_OWNER:
src/aiscc/runtime/stockroom_image.py

PRODUCTION_PROVENANCE_DEPENDENCY:
TYPED_PROVENANCE_REF_PLUS_FIXED_SOURCE_RESOLVER

DOCKERFILE_BUILD_CONTEXT_MODEL:
TASK_SCOPED_GIT_OBJECT_ASSEMBLED_EXACT_CONTEXT

DOCKER_RUNNER_MODEL:
source-owned Stockroom Docker settlement adapter

PERSISTENT_DB_MODEL:
dedicated local Docker PostgreSQL + named volume
source change not required

RUNTIME_ROOT_MODEL:
TASK_SCOPED_ROOT_ONLY
source change not required
```

The future Stockroom runtime image ID does not exist yet and MUST NOT be invented in
Cut A.

# Cut A authorization

Cut A is now authorized as a source/config/test implementation candidate only.

Exact mutation allowlist:

```text
src/aiscc/bootstrap.py
src/aiscc/runtime/docker.py
src/aiscc/providers/stockroom_tool.py
src/aiscc/providers/local_deterministic.py
src/aiscc/scenarios/composition.py
src/aiscc/scenarios/stockroom_production.py
tests/unit/runtime/test_stockroom_docker_settlement.py
tests/unit/providers/test_stockroom_tool.py
tests/unit/providers/test_local_deterministic.py
tests/unit/scenarios/test_owner_composition.py
tests/integration/scenarios/test_stockroom_binding.py
tests/integration/scenarios/test_stockroom_capture_runner.py
src/aiscc/runtime/stockroom_image.py
config/providers/stockroom-tools.v2.toml
config/providers/stockroom-owner-profiles.v2.toml
examples/synthetic-stockroom/Dockerfile
examples/synthetic-stockroom/.dockerignore
examples/synthetic-stockroom/IMAGE_PROVENANCE.md
tests/unit/runtime/test_stockroom_image.py
```

Cut A must not:

```text
build/pull/run Stockroom image
create canonical image provenance JSON
create persistent DB
execute private S1
perform Git persistence
```

After executable proof, Browser must separately judge and persist Cut A before Cut B.
