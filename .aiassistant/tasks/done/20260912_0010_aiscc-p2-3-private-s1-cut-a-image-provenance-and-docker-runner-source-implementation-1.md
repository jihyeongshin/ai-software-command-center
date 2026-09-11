# 작업지시서: P2-3 private S1 Cut A image provenance + Docker runner source implementation

## meta

- task_id: `20260912_0010_aiscc-p2-3-private-s1-cut-a-image-provenance-and-docker-runner-source-implementation-1`
- created_at: `2026-09-12T00:10:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `SOURCE_CONFIG_TEST_IMPLEMENTATION / CUT_A`
- evidence_profile: `HIGH_RISK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `21bb0769c5db126c1989d9e0eb8e9f4c5ceade91`
- required_tree: `11b9d62db2d02649509f148aa01f8f74924c5792`
- accepted_product_commit: `d98f9ad108e95ba659b9c6a10770119af22175a1`
- accepted_product_aggregate: `3aa781baaf25e09edd15f0713f7d42fc066d51092403cdc473f5030af684b4eb`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `read-only provisioning architecture/evidence audit → source/config/test implementation authority`
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

Use exact repository interpreter when available:

```text
.venv\Scripts\python.exe
```

Use `-B` for test/import execution.

Do not use `py_compile`; use external in-memory `compile(...)` verification.

# 1. purpose

Implement the Browser-accepted Cut A source contract only:

```text
typed Stockroom image provenance authority
static v2 tool/profile policy
source-owned Docker settlement runner
production provenance binding
exact Dockerfile/build-context definition
bounded tests
```

Do not build or run the Stockroom image.

Do not create the canonical provenance JSON.

Do not provision the persistent capture database.

Do not execute S1.

# 2. inbound transport

Verify Browser ZIP filename/SHA-256 from the Short Prompt.

Place current Task first:

```text
.aiassistant/tasks/active/20260912_0010_aiscc-p2-3-private-s1-cut-a-image-provenance-and-docker-runner-source-implementation-1.md
```

Read fully; require it is ignored by canonical Git policy.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260912_0010_aiscc-p2-3-base-image-authority-reconciled-cut-a-implementation-entry-1.cycle.md
SHA-256:
420ad30fe70216079081a337aaea11005de672c4c8383ee1f7c2c7d2b9621108

.aiassistant/reports/aiscc/20260912_0010_aiscc-p2-3-base-image-authority-reconciliation-final-acceptance-judgment-1.md
SHA-256:
544736710f005c3f723731d23143047af9e0e73b90eab87f81d3e62f17c003cb
```

Bootstrap failure before Task placement:

```text
STOP
no product mutation
no report/export
```

# 3. repository gate

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

Before this delivery exact Git-visible set is 15 governance paths:

- `.aiassistant/tasks/done/20260911_1935_aiscc-p2-3-actual-capture-runtime-prerequisite-verification-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_1935_aiscc-p2-3-a2-terminal-persisted-runtime-prerequisite-verification-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1935_aiscc-p2-3-a2-terminal-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260911_2140_aiscc-p2-3-private-s1-runtime-provisioning-contract-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_2140_aiscc-p2-3-runtime-prerequisite-not-ready-provisioning-contract-audit-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2140_aiscc-p2-3-runtime-prerequisite-verification-final-judgment-1.md`
- `.aiassistant/tasks/done/20260911_2148_aiscc-p2-3-private-s1-image-build-input-authority-reconciliation-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_2148_aiscc-p2-3-provisioning-contract-partial-hold-image-build-authority-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2148_aiscc-p2-3-provisioning-contract-audit-image-build-authority-gap-judgment-1.md`
- `.aiassistant/tasks/done/20260911_2250_aiscc-p2-3-base-image-inspect-identity-reconciliation-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_2250_aiscc-p2-3-image-build-authority-inspect-evidence-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2250_aiscc-p2-3-image-build-authority-inspect-identity-inconsistency-judgment-1.md`
- `.aiassistant/tasks/done/20260911_2300_aiscc-p2-3-base-image-inspect-identity-reconciliation-retry-after-replay-conflict-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_2300_aiscc-p2-3-base-image-inspect-replay-conflict-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2300_aiscc-p2-3-base-image-inspect-replay-conflict-judgment-1.md`

After current Cycle/Judgment placement while current Task is active:

```text
Git-visible:
17 exact

active Task:
exists byte-exact
ignored
```

Exact set:

- `.aiassistant/tasks/done/20260911_1935_aiscc-p2-3-actual-capture-runtime-prerequisite-verification-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_1935_aiscc-p2-3-a2-terminal-persisted-runtime-prerequisite-verification-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1935_aiscc-p2-3-a2-terminal-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260911_2140_aiscc-p2-3-private-s1-runtime-provisioning-contract-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_2140_aiscc-p2-3-runtime-prerequisite-not-ready-provisioning-contract-audit-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2140_aiscc-p2-3-runtime-prerequisite-verification-final-judgment-1.md`
- `.aiassistant/tasks/done/20260911_2148_aiscc-p2-3-private-s1-image-build-input-authority-reconciliation-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_2148_aiscc-p2-3-provisioning-contract-partial-hold-image-build-authority-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2148_aiscc-p2-3-provisioning-contract-audit-image-build-authority-gap-judgment-1.md`
- `.aiassistant/tasks/done/20260911_2250_aiscc-p2-3-base-image-inspect-identity-reconciliation-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_2250_aiscc-p2-3-image-build-authority-inspect-evidence-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2250_aiscc-p2-3-image-build-authority-inspect-identity-inconsistency-judgment-1.md`
- `.aiassistant/tasks/done/20260911_2300_aiscc-p2-3-base-image-inspect-identity-reconciliation-retry-after-replay-conflict-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_2300_aiscc-p2-3-base-image-inspect-replay-conflict-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2300_aiscc-p2-3-base-image-inspect-replay-conflict-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260912_0010_aiscc-p2-3-base-image-authority-reconciled-cut-a-implementation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0010_aiscc-p2-3-base-image-authority-reconciliation-final-acceptance-judgment-1.md`

No other dirt.

# 4. accepted current source identity

Before mutation require these 12 existing Cut A files exactly:

- `src/aiscc/bootstrap.py`  `1718e596b20fd107af0cb80b6ad40e3626b7e26d8d45daa649ccf2d2ccf9fe38`
- `src/aiscc/runtime/docker.py`  `f338225c13195d69c41f69f00a47fc1d00c616c94458ef361e32b97f7fde96fa`
- `src/aiscc/providers/stockroom_tool.py`  `ad02321999b2b42039007c4dc6d55d20502004c137486ca33bfc191119d7dbb7`
- `src/aiscc/providers/local_deterministic.py`  `d7fd527fec919bd3488e4a22a3e24ff357d262076de83785f75698548708399d`
- `src/aiscc/scenarios/composition.py`  `2017a18175e0e227fe1514d3d9e85c7d0d64d391ec94649912d9749699b7edfc`
- `src/aiscc/scenarios/stockroom_production.py`  `4ea0177d2e129c394367acbfaef8dc193aac28e48b974844597cba27ce9dfa3f`
- `tests/unit/runtime/test_stockroom_docker_settlement.py`  `ebfb54d92dc446d2afe6bbe51ce261dbdabff92fa4650833f1d576fde6a755c6`
- `tests/unit/providers/test_stockroom_tool.py`  `5d3629381b97cd0d6a449b399b0f1acce156b24e17089cf229fce4feb7641f9d`
- `tests/unit/providers/test_local_deterministic.py`  `7280db790d1d942e851b67ad0f22816ab33d0af6b34e2d51813a599f9ba38870`
- `tests/unit/scenarios/test_owner_composition.py`  `68cf0561e482e1ded6f6bddaa8b91da1fea753b430527e27fe66bf7cf0cb4d12`
- `tests/integration/scenarios/test_stockroom_binding.py`  `063e2b65eb229b5849bc3df61294d72f3f656783ac1257a4dbcaa82bb2d70b34`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`  `2213234f213501be162b1a690a70aba975db9bc26bcc2340f5098ceb700ba3c7`

Require these seven Cut A paths are absent before mutation:

- `src/aiscc/runtime/stockroom_image.py`
- `config/providers/stockroom-tools.v2.toml`
- `config/providers/stockroom-owner-profiles.v2.toml`
- `examples/synthetic-stockroom/Dockerfile`
- `examples/synthetic-stockroom/.dockerignore`
- `examples/synthetic-stockroom/IMAGE_PROVENANCE.md`
- `tests/unit/runtime/test_stockroom_image.py`

Require frozen identities:

- `config/providers/stockroom-tools.v1.toml`  `223c45f224e4aba6ae7f023ed6752b4730e9889d4878cf6d4a053eed71bd457c`
- `config/providers/stockroom-owner-profiles.v1.toml`  `82de20f5a2aa76e039e685fcacbc2da44cd04b2dd863ebb9dd8e9ff7b8e37eee`
- `config/scenarios/stockroom/v1/resource.json`  `a5b8c8a5bd7165073f37647eb791df0bc59aa7b73033d59dd5f3967bbff28a99`
- `examples/synthetic-stockroom/.python-version`  `f50159fad3f4319868eb38717b91d55843c41e9803014c8de05e116a6d0bcfdc`

Any mismatch:

```text
CUT_A_BASE_IDENTITY_MISMATCH
→ STOP_WITH_REPORT_EXPORT
```

# 5. exact mutation allowlist

Only these 19 paths may change/create:

- `src/aiscc/bootstrap.py`
- `src/aiscc/runtime/docker.py`
- `src/aiscc/providers/stockroom_tool.py`
- `src/aiscc/providers/local_deterministic.py`
- `src/aiscc/scenarios/composition.py`
- `src/aiscc/scenarios/stockroom_production.py`
- `tests/unit/runtime/test_stockroom_docker_settlement.py`
- `tests/unit/providers/test_stockroom_tool.py`
- `tests/unit/providers/test_local_deterministic.py`
- `tests/unit/scenarios/test_owner_composition.py`
- `tests/integration/scenarios/test_stockroom_binding.py`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`
- `src/aiscc/runtime/stockroom_image.py`
- `config/providers/stockroom-tools.v2.toml`
- `config/providers/stockroom-owner-profiles.v2.toml`
- `examples/synthetic-stockroom/Dockerfile`
- `examples/synthetic-stockroom/.dockerignore`
- `examples/synthetic-stockroom/IMAGE_PROVENANCE.md`
- `tests/unit/runtime/test_stockroom_image.py`

Classification:

```text
MODIFY:
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

CREATE:
src/aiscc/runtime/stockroom_image.py
config/providers/stockroom-tools.v2.toml
config/providers/stockroom-owner-profiles.v2.toml
examples/synthetic-stockroom/Dockerfile
examples/synthetic-stockroom/.dockerignore
examples/synthetic-stockroom/IMAGE_PROVENANCE.md
tests/unit/runtime/test_stockroom_image.py
```

Everything else is frozen.

If another product/config/test/example path becomes necessary:

```text
SCOPE_EXPANSION_REQUIRED
→ STOP_WITH_REPORT_EXPORT
```

# 6. accepted base-image authority

Cut A must use exactly:

```text
BASE_IMAGE_PIN_MODEL:
SOURCE_FIXED_VERIFIED_REPODIGEST

BASE_IMAGE_REPODIGEST:
python@sha256:0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579

current observed local base config ID:
sha256:0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579

raw inspect SHA-256 admitted by Browser:
cd67997302dedcb0c13c63d4235ac529d34f27b8cc0b383ea86793ea2ca50e65
```

Do not treat the config ID as the RepoDigest even though the hexadecimal payload is
currently equal.

Do not introduce a different base digest.

Do not use a floating base tag as authority.

# 7. `src/aiscc/runtime/stockroom_image.py`

Create the executable image-provenance authority.

It owns, at minimum:

```text
AISCC-STOCKROOM-IMAGE-PROVENANCE-V1 / 1.0.0
AISCC-STOCKROOM-RUNTIME-BUILD-V1
fixed canonical provenance relative path
strict frozen typed provenance model
typed StockroomImageProvenanceRef
resolver/admission owner
canonical provenance fingerprint
whole-file SHA binding
build/source/static-policy cross-binding
inspect projection verification
currentness verification
```

Canonical provenance path:

```text
.aiassistant/records/aiscc/runtime/stockroom-image-provenance.v1.json
```

The file MUST NOT be created in Cut A.

Production resolution must fail closed while it is absent.

# 8. provenance schema contract

The strict future JSON root must contain exactly:

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

Required semantics include:

```text
schema:
AISCC-STOCKROOM-IMAGE-PROVENANCE-V1 / 1.0.0

image identity model:
LOCAL_IMAGE_CONFIG_ID_SHA256

actual image ID:
sha256:<64 lowercase hex>

discovery tag:
optional / non-authoritative

base pin model:
SOURCE_FIXED_VERIFIED_REPODIGEST

base RepoDigest:
python@sha256:0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579

build contract:
AISCC-STOCKROOM-RUNTIME-BUILD-V1

source commit:
05185c57a6265a4002050ce25cdfde3dc87e9779

source subroot:
examples/synthetic-stockroom/

Git subtree:
f3d9203321ae3535abf8e92a7285da1067f6c55e

resource ref:
repository:synthetic-stockroom@be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d

source aggregate:
be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d

source file count:
14

Python:
3.12.14

argv:
python -B -m stockroom summary

workdir:
/workspace

runtime user/group:
65532:65532

network:
none
```

Reject unknown keys, coercion, mutable-tag authority, machine-specific paths and
credentials.

# 9. provenance authority non-forgeability

A raw parsed provenance object is not admitted authority merely because it is typed.

The production resolver must be the only production path that yields the admitted
provenance object consumed by composition/spec construction.

Require:

```text
caller-created raw object != admitted provenance
config != image authority
tag != image authority
source aggregate != image ID
future image ID absent in Cut A
```

Use an internal issuer/token/factory discipline or an equivalent fail-closed source
mechanism.

Tests must prove caller-created/raw/unresolved objects cannot enter the production
`DockerRunSpec`.

# 10. typed provenance ref

The Cut C typed ref must bind at least:

```text
fixed canonical relative path
whole-file SHA-256
canonical provenance fingerprint
provenance ID
provenance version
accepted Cut B Cycle ref
accepted Cut B Judgment ref
```

Resolver requires exact equality among:

```text
typed ref
canonical JSON
static v2 policy
source/build constants
```

Issuance-ref drift, file-hash drift, canonical-fingerprint drift or ID/version drift
must fail closed.

# 11. canonical fingerprint

Use the repository canonical JSON algorithm:

```text
UTF-8
Unicode preserved
sorted keys
compact separators
no insignificant whitespace
SHA-256(canonical bytes)
```

Whole-file SHA-256 remains a separate transport/currentness check.

The JSON must not embed its own fingerprint.

# 12. inspect projection

Define one exact canonical selected-inspect projection for the future built Stockroom
image.

It must bind at least:

```text
.Id
.Os
.Architecture
.Config.User
.Config.WorkingDir
required final-image labels
```

Include other fields only if needed by the accepted runtime contract.

The provenance stores:

```text
inspect_projection_sha256
```

The production runner later recomputes this from exact local inspect and requires
equality before container creation.

# 13. required final-image labels

The accepted required label keys are exactly:

```text
io.aiscc.stockroom.build-contract
io.aiscc.stockroom.source-commit
io.aiscc.stockroom.source-subroot
io.aiscc.stockroom.git-subtree
io.aiscc.stockroom.resource-ref
io.aiscc.stockroom.source-aggregate
io.aiscc.stockroom.source-file-count
io.aiscc.stockroom.python-version
io.aiscc.stockroom.dockerfile-sha256
io.aiscc.stockroom.base-repodigest
```

Unknown additional labels may exist but are non-authoritative unless the source model
explicitly rejects them for safety. The exact required label values must be verified.

# 14. `stockroom-tools.v2.toml`

Create:

```text
config/providers/stockroom-tools.v2.toml
```

It MUST NOT contain:

```text
image = ...
future Stockroom image ID
source aggregate in an image field
floating runtime tag as authority
```

Its static image-binding policy is:

```text
binding_model = IMAGE_IDENTITY_POLICY_AND_PROVENANCE_REF
runtime_identity_model = LOCAL_IMAGE_CONFIG_ID_SHA256
provenance_schema_id = AISCC-STOCKROOM-IMAGE-PROVENANCE-V1
provenance_schema_version = 1.0.0
provenance_ref = .aiassistant/records/aiscc/runtime/stockroom-image-provenance.v1.json
provenance_fingerprint_required = true
base_image_pin_model = SOURCE_FIXED_VERIFIED_REPODIGEST
base_image_ref = python@sha256:0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579
build_contract_version = AISCC-STOCKROOM-RUNTIME-BUILD-V1
source_resource_ref = repository:synthetic-stockroom@be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d
```

Preserve the accepted argv/workdir/network/output/timeout limits.

Use registry version `2`.

V1 config remains byte-frozen.

# 15. owner profiles v2

Create:

```text
config/providers/stockroom-owner-profiles.v2.toml
```

Preserve the existing four profile IDs, profile version `1`, provider/security limits,
scenario bindings and secret compatibility contract.

Change only what is required for v2 source schema and:

```text
tool_registry_version = 2
```

Do not create a security v2 config.

V1 owner profiles remain byte-frozen.

# 16. loader compatibility

`load_stockroom_tool_config(...)` and `load_stockroom_owner_profiles(...)` must support
the exact accepted V1 and V2 schemas.

Require:

```text
v1:
strict / unchanged semantic identity

v2:
strict / exact new policy

unknown/mixed schema:
DENY

v2 `image` key:
DENY

v2 floating image tag:
DENY

v2 source aggregate used as image identity:
DENY
```

Do not loosen V1 parsing to achieve V2.

# 17. production composition split

Preserve legacy/inert owner composition behavior where required by prior B3 contracts.

Add an explicit production-v2 composition path rather than silently rewriting all
legacy composition semantics.

Production v2 must load:

```text
stockroom-owner-profiles.v2.toml
stockroom-tools.v2.toml
existing security config
existing scenario catalog
```

Its composition fingerprint must bind:

```text
v2 provider fingerprint
v2 tool/static image-policy fingerprint
admitted image provenance fingerprint
existing catalog/security fingerprints
```

Changing admitted provenance must change the production composition fingerprint.

# 18. production provenance dependency

`build_stockroom_production(...)` must receive:

```text
typed StockroomImageProvenanceRef
trusted absolute Docker executable
attempt/run-scoped cancellation signal compatible with the accepted runner contract
```

It must NOT receive:

```text
image string
arbitrary admitted provenance object
arbitrary provenance resolver
arbitrary Docker process callback
```

The production root instantiates the fixed source resolver at the fixed canonical path.

Absence of the canonical JSON in Cut A must fail closed before any process authority is
constructed.

# 19. DockerRunSpec provenance binding

For production v2:

```text
spec.image
=
exact admitted future Stockroom local image ID
```

The spec/fingerprint must bind:

```text
provenance fingerprint/ref identity
required image labels or their canonical fingerprint
existing command/workspace/network/resource/time/output fields
```

Remove the source-aggregate pseudo-image constant from the production v2 validation
path.

Legacy V1 compatibility may remain only where required by frozen historical tests; it
must not be selected by production v2.

# 20. source-owned Docker settlement runner

Implement the accepted source-owned Stockroom Docker process runner in:

```text
src/aiscc/runtime/docker.py
```

Production construction is from:

```text
trusted absolute Docker executable
admitted Stockroom image provenance
attempt/run-scoped cancellation signal
```

No arbitrary Task lambda/callback may stand in for the production runner.

# 21. runner pre-create image admission

Before container creation:

```text
inspect exact admitted local image ID
```

Require exact equality for:

```text
.Id
OS/architecture
required labels
selected inspect projection hash
other runtime image fields enrolled by provenance
```

Any drift:

```text
deny before create
```

Never resolve a mutable tag for execution.

# 22. runner process settlement

The source-owned runner must:

```text
use argv sequences only
shell = false
closed stdin
trusted absolute Docker executable
minimal inherited environment

create exact container
capture exact container ID
verify name + aiscc.run_id + aiscc.owner labels
attach/start exact container
concurrently drain stdout/stderr
retain no more than each limit + 1 overflow byte
enforce operation timeout
observe the accepted cancellation signal
on timeout/cancel stop then kill exact container if required
inspect exact container until terminal
derive container exit code from inspected state
remove only exact owned container
confirm exact container absence
```

Set:

```text
termination_proven = true
```

only after exact terminal-state proof.

Set:

```text
owner_reconciled = true
```

only after exact ownership and required removal reconciliation.

Uncertain settlement must remain:

```text
UNKNOWN_TOOL_OUTCOME
quarantine required
no automatic second dispatch
```

# 23. runner test seam

Tests may monkeypatch/module-internally replace low-level subprocess behavior.

Do not expose the test transport as a production composition dependency.

The public production path must always construct the source-owned runner.

# 24. attempt cancellation binding

Use an explicit attempt/run-scoped cancellation input.

If the existing accepted runtime exposes a compatible signal, bind it directly.

If implementation within the 19-path allowlist cannot bind cancellation without
inventing a second authority or changing an out-of-scope owner:

```text
SCOPE_EXPANSION_REQUIRED
→ STOP_WITH_REPORT_EXPORT
```

Do not silently omit cancellation.

# 25. Dockerfile

Create:

```text
examples/synthetic-stockroom/Dockerfile
```

Base:

```text
FROM python@sha256:0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579
```

Requirements:

```text
Python 3.12.14 base
no package install
no network build step
no secret ARG/ENV
COPY only source/ historical payload into provenance-reference location
WORKDIR /workspace
USER 65532:65532
```

Use build-time non-secret immutable arguments only as necessary for required labels.

The Dockerfile must emit the required provenance labels.

Do not claim bit-for-bit reproducible OCI manifest output.

# 26. build context contract

Cut B, not Cut A, will assemble the real build context.

The accepted model is:

```text
TASK_SCOPED_GIT_OBJECT_ASSEMBLED_EXACT_CONTEXT
```

Exact context inventory:

```text
Dockerfile
.dockerignore
source/<14 exact resource-manifest files>
```

The 14 source files come from Git objects at:

```text
commit:
05185c57a6265a4002050ce25cdfde3dc87e9779

subroot:
examples/synthetic-stockroom/

subtree:
f3d9203321ae3535abf8e92a7285da1067f6c55e

aggregate:
be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d
```

Do not build from the mutable current worktree subroot.

`Dockerfile`, `.dockerignore`, and `IMAGE_PROVENANCE.md` are not members of the 14-file
resource aggregate.

# 27. `.dockerignore`

Create deny-first context defense.

It must permit only the Dockerfile and exact intended `source/` tree required by the
assembler.

It is defense in depth; it must not become the source-selection authority.

# 28. IMAGE_PROVENANCE.md

Document operator/build contract without embedding a future image ID.

It must distinguish:

```text
base RepoDigest
base local config observation
historical source aggregate
future final Stockroom image ID
canonical provenance JSON
```

State that the future final image ID is born only in Cut B.

# 29. static verification

Do not use `py_compile`.

Use an external temporary verifier to in-memory compile all 14 Python paths in the
allowlist.

Require:

```text
14 / 14 compile PASS
14 / 14 Ruff PASS
git diff --check PASS
index empty
new repo-visible pyc = 0
```

Strict-load:

```text
stockroom-tools.v1
stockroom-tools.v2
owner-profiles.v1
owner-profiles.v2
```

Require all exact expected schemas.

Verify the frozen files from section 4 remain byte-exact.

Mandatory static failure:

```text
STATIC_CHECK_FAILURE
→ STOP_WITH_REPORT_EXPORT
```

No same-turn source repair after this gate.

# 30. targeted unit proof

Run with `-B` and no pytest cache:

```text
tests/unit/runtime/test_stockroom_image.py
tests/unit/runtime/test_stockroom_docker_settlement.py
tests/unit/providers/test_stockroom_tool.py
tests/unit/providers/test_local_deterministic.py
tests/unit/scenarios/test_owner_composition.py
```

Require:

```text
all collected PASS
0 fail
0 error
0 skip
```

Tests must use fake/mocked process observations only.

No real Docker subprocess is allowed.

# 31. required unit semantics

Unit proof must cover at minimum:

```text
strict provenance schema
canonical fingerprint
whole-file hash binding
issuance-ref drift denial
source/build/base-policy drift denial
future image-ID syntax strictness
tag-only denial
source-aggregate-as-image denial
raw typed object not admitted
missing canonical provenance fail-closed
v1/v2 tool config compatibility
v1/v2 owner profile compatibility
production v2 composition fingerprint binds provenance
runner exact inspect-before-create
runner label/projection drift denial
argv/shell safety
stdout/stderr overflow bounded
timeout settlement
cancel settlement
create/start/inspect/remove uncertainty
owner reconciliation
unknown-outcome quarantine
no blind redispatch
```

# 32. PostgreSQL test prerequisite

The Cut A product does not provision persistent capture DB.

A Task-owned disposable PostgreSQL test container is allowed only for the existing
bounded integration tests.

Use:

```text
postgres:17.6-alpine
--pull=never
loopback only
temporary storage
unique Task-owned name
```

No named persistent capture volume.

Migrate only the disposable test DB to:

```text
20260901_0008
```

Remove only that exact container after tests.

This is test infrastructure, not Cut B provisioning.

# 33. integration proof

Run:

```text
tests/integration/scenarios/test_stockroom_binding.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Require all collected PASS / zero skip.

No actual Stockroom image, Docker process or provider/tool execution.

Use test-only provenance fixtures under temporary paths/seams that pass through the
same source parser/admission logic but cannot be mistaken for Browser-issued production
provenance.

# 34. regression preservation

Run:

```text
tests/unit/scenarios/test_stockroom_capture_runner.py
tests/unit/security/test_stockroom_policy.py
tests/integration/evidence/test_postgres_evidence_admission.py
tests/integration/human/test_postgres_human_gate_judgment.py
tests/integration/workflow/test_postgres_kernel.py
```

Require all collected PASS / zero skip.

This proves Cut A did not reopen:

```text
A1 runner semantics
P1-3 security authority
P1-6 evidence
P1-7 Human/Judgment
P1-4 workflow kernel
```

# 35. no actual runtime actions

Forbidden throughout Cut A:

```text
docker image inspect
docker pull
docker build/buildx
docker create/run for Stockroom
registry/API lookup
Stockroom materialization
LocalDeterministicProvider real execution
tool dispatch
actual S1-S4
persistent PostgreSQL volume/container
canonical image provenance JSON creation
Replay
network
Git add/commit/push
```

Exception:

```text
Task-owned disposable postgres:17.6-alpine test container
```

only as section 32 permits.

# 36. contract review

Require PASS:

```text
BASE_REPODIGEST_FIXED
BASE_CONFIG_ID_NOT_USED_AS_PIN_AUTHORITY
FUTURE_STOCKROOM_IMAGE_ID_ABSENT
V2_CONFIG_HAS_NO_IMAGE_VALUE
V2_CONFIG_PROVENANCE_POLICY_STRICT
V1_CONFIG_FROZEN
V1_OWNER_PROFILES_FROZEN
PROVENANCE_SCHEMA_TYPED
PROVENANCE_REF_TYPED
PROVENANCE_CURRENTNESS_FAIL_CLOSED
RAW_OBJECT_NOT_AUTHORITY
STATIC_CONFIG_NOT_AUTHORITY
SOURCE_AGGREGATE_NOT_IMAGE_ID
PRODUCTION_RESOLVER_FIXED
PRODUCTION_ARBITRARY_RUNNER_REMOVED
DOCKER_SPEC_BINDS_PROVENANCE
RUNNER_INSPECTS_EXACT_IMAGE_ID
RUNNER_LABEL_PROJECTION_VERIFIED
RUNNER_SHELL_FALSE
RUNNER_OUTPUT_BOUNDED
RUNNER_TIMEOUT_SETTLED
RUNNER_CANCEL_SETTLED
RUNNER_OWNER_RECONCILED
UNKNOWN_OUTCOME_NO_RETRY
BUILD_CONTEXT_HISTORICAL_SOURCE_BOUND
DOCKERFILE_NOT_IN_14_FILE_AGGREGATE
NO_STOCKROOM_DOCKER_EXECUTION
NO_CANONICAL_PROVENANCE_JSON
NO_PERSISTENT_CAPTURE_DB
NO_ACTUAL_S1
NO_REPLAY
NO_GIT_PERSISTENCE
```

Require:

```text
32 / 32 PASS
```

# 37. failure behavior

Bootstrap failure:

```text
STOP / no report/export
```

After Task placement:

```text
any mandatory failure
→ STOP_WITH_REPORT_EXPORT
```

No broad repair.

No same-turn source repair after mandatory static/test failure.

# 38. final workspace

Before product mutation:

```text
Git-visible:
17 exact
index empty
```

After successful Cut A mutation and before Task movement:

```text
Git-visible:
36 exact

17 governance
+
19 Cut A paths
```

Move current active Task byte-identically:

```text
.aiassistant/tasks/active/20260912_0010_aiscc-p2-3-private-s1-cut-a-image-provenance-and-docker-runner-source-implementation-1.md
→
.aiassistant/tasks/done/20260912_0010_aiscc-p2-3-private-s1-cut-a-image-provenance-and-docker-runner-source-implementation-1.md
```

Final:

```text
Git-visible:
37 exact
index empty
```

Exact final set:

- `.aiassistant/tasks/done/20260911_1935_aiscc-p2-3-actual-capture-runtime-prerequisite-verification-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_1935_aiscc-p2-3-a2-terminal-persisted-runtime-prerequisite-verification-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1935_aiscc-p2-3-a2-terminal-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260911_2140_aiscc-p2-3-private-s1-runtime-provisioning-contract-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_2140_aiscc-p2-3-runtime-prerequisite-not-ready-provisioning-contract-audit-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2140_aiscc-p2-3-runtime-prerequisite-verification-final-judgment-1.md`
- `.aiassistant/tasks/done/20260911_2148_aiscc-p2-3-private-s1-image-build-input-authority-reconciliation-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_2148_aiscc-p2-3-provisioning-contract-partial-hold-image-build-authority-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2148_aiscc-p2-3-provisioning-contract-audit-image-build-authority-gap-judgment-1.md`
- `.aiassistant/tasks/done/20260911_2250_aiscc-p2-3-base-image-inspect-identity-reconciliation-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_2250_aiscc-p2-3-image-build-authority-inspect-evidence-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2250_aiscc-p2-3-image-build-authority-inspect-identity-inconsistency-judgment-1.md`
- `.aiassistant/tasks/done/20260911_2300_aiscc-p2-3-base-image-inspect-identity-reconciliation-retry-after-replay-conflict-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_2300_aiscc-p2-3-base-image-inspect-replay-conflict-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2300_aiscc-p2-3-base-image-inspect-replay-conflict-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260912_0010_aiscc-p2-3-base-image-authority-reconciled-cut-a-implementation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0010_aiscc-p2-3-base-image-authority-reconciliation-final-acceptance-judgment-1.md`
- `src/aiscc/bootstrap.py`
- `src/aiscc/runtime/docker.py`
- `src/aiscc/providers/stockroom_tool.py`
- `src/aiscc/providers/local_deterministic.py`
- `src/aiscc/scenarios/composition.py`
- `src/aiscc/scenarios/stockroom_production.py`
- `tests/unit/runtime/test_stockroom_docker_settlement.py`
- `tests/unit/providers/test_stockroom_tool.py`
- `tests/unit/providers/test_local_deterministic.py`
- `tests/unit/scenarios/test_owner_composition.py`
- `tests/integration/scenarios/test_stockroom_binding.py`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`
- `src/aiscc/runtime/stockroom_image.py`
- `config/providers/stockroom-tools.v2.toml`
- `config/providers/stockroom-owner-profiles.v2.toml`
- `examples/synthetic-stockroom/Dockerfile`
- `examples/synthetic-stockroom/.dockerignore`
- `examples/synthetic-stockroom/IMAGE_PROVENANCE.md`
- `tests/unit/runtime/test_stockroom_image.py`
- `.aiassistant/tasks/done/20260912_0010_aiscc-p2-3-private-s1-cut-a-image-provenance-and-docker-runner-source-implementation-1.md`

No other path.

# 39. required export

Folder:

```text
.aiassistant/reports/target/20260912_0010_aiscc-p2-3-private-s1-cut-a-image-provenance-and-docker-runner-source-implementation-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
IMPLEMENTATION_MANIFEST.md
BASE_IMAGE_AUTHORITY_VERIFICATION.md
IMAGE_PROVENANCE_MODEL_VERIFICATION.md
V2_CONFIG_VERIFICATION.md
DOCKER_RUNNER_VERIFICATION.md
BUILD_CONTEXT_CONTRACT_VERIFICATION.md
PRODUCTION_BINDING_VERIFICATION.md
STATIC_VERIFICATION.md
UNIT_VERIFICATION.md
INTEGRATION_VERIFICATION.md
REGRESSION_VERIFICATION.md
CONTRACT_REVIEW.md
```

Also include byte-preserving:

```text
current Cycle
current Judgment
current done Task

all 19 Cut A mutation paths
```

Expected:

```text
16 root docs
3 canonical copies
19 implementation copies
38 members total
```

`EXPORT_MANIFEST.md` covers all 37 non-self entries with relative path, byte size and
SHA-256.

Create adjacent verified ZIP:

```text
one top-level directory
38 exact members
CRC PASS
folder/archive byte equality
```

# 40. success ceiling

Success:

```text
Cut A image/provenance source contract:
IMPLEMENTED_CANDIDATE

source-owned Docker settlement runner:
IMPLEMENTED_CANDIDATE

Cut A executable proof:
PASS

Cut A persistence:
NOT_AUTHORIZED

Cut B environment provisioning:
NOT_AUTHORIZED

canonical image provenance JSON:
ABSENT

persistent capture DB:
NOT_PROVISIONED

private S1:
NOT_AUTHORIZED

P2-3:
IN_PROGRESS
```
