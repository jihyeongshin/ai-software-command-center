# 작업지시서: P2-3 private S1 Cut C Docker image authority + public entrypoint retry

## meta

- task_id: `20260912_1633_aiscc-p2-3-private-s1-cut-c-docker-image-authority-and-public-entrypoint-retry-1`
- created_at: `2026-09-12T16:33:35+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `REWORK / PRIVATE_RUNTIME_READINESS_BINDING`
- evidence_profile: `HIGH_RISK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `6d41633210f0e556dd4292ee62a8600c6b54215f`
- required_parent: `fdd3b9ac2f0d8db447ed0ed055aa4b02eab4b30d`
- required_grandparent: `474826340a89b5c597aa066ff0d414bfc8f43229`
- fresh_ide_executor_chat: `FORBIDDEN`
- executor_session_action: `KEEP_EXISTING_1605_1622_IDE_EXECUTOR_CHAT`
- success_ceiling: `CUT_C_READINESS_COMPLETE / BROWSER_REVIEW_PENDING`
- private_s1_authorized: `No`

# 0. purpose

Resolve the exact authority conflict that stopped 1622 and continue Cut C readiness.

Corrections relative to 1622:

```text
A. PostgreSQL image read-only inspect is explicitly authorized.
B. production construction must use public:
   aiscc.bootstrap.build_stockroom_production(...)
   exactly once.
```

No other authority expansion is intended.

# 1. inbound transport

Continue in the existing 1605/1622 IDE Executor chat.
Do not open a new IDE chat.

Verify Browser Short Prompt ZIP filename/SHA-256 and require exactly three flat members.

Place current Task first:

```text
.aiassistant/tasks/active/20260912_1633_aiscc-p2-3-private-s1-cut-c-docker-image-authority-and-public-entrypoint-retry-1.md
```

Require byte equality + ignored status.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260912_1633_aiscc-p2-3-cut-c-docker-image-authority-entrypoint-retry-entry-1.cycle.md
SHA-256:
de18417733a2abb32a7f9e2543a9a7f5ead41f8d82c116b2051402b44b085299

.aiassistant/reports/aiscc/20260912_1633_aiscc-p2-3-cut-c-docker-image-authority-entrypoint-policy-gap-hold-judgment-1.md
SHA-256:
07937e2486f9f5c2b39801fb3aac16eb8d3599ce7ee1a10d6d7cc928be2f7b3f
```

Bootstrap failure:

```text
STOP
no Docker observation
no private file access
no runtime-root action
no DB connection
no report/export
```

# 2. predecessor provenance

Require these six existing blocked-turn artifacts byte-exact:

- `.aiassistant/tasks/done/20260912_1605_aiscc-p2-3-private-s1-cut-c-final-readiness-binding-1.md`  `de52d47cacb4f45d5f16543e1fecaa517aaf5d2e176123386d69461b52f3c732`
- `.aiassistant/records/aiscc/cycles/20260912_1605_aiscc-p2-3-cut-b-reconciled-cut-c-readiness-entry-1.cycle.md`  `859d10407bc41266968adb08386e5f9a39ee54f3dfeaa0748620e45a57e3b12b`
- `.aiassistant/reports/aiscc/20260912_1605_aiscc-p2-3-cut-b-state-reconciliation-final-acceptance-cut-c-authorization-judgment-1.md`  `bec6679de2659607670bcf13c2fea3f760f369c045413ea666eb0fdb1aff16f2`
- `.aiassistant/tasks/done/20260912_1622_aiscc-p2-3-private-s1-cut-c-postgres-projection-contract-retry-1.md`  `645ea23305463084aed11c4b2eb6536993772a690f6ecba61eb005069d0341fa`
- `.aiassistant/records/aiscc/cycles/20260912_1622_aiscc-p2-3-cut-c-postgres-projection-policy-gap-retry-entry-1.cycle.md`  `6bd67df35b8f6e82f09213e252f64d1d31efdd209b6fdfbef980d4c2eaf1fe37`
- `.aiassistant/reports/aiscc/20260912_1622_aiscc-p2-3-cut-c-postgres-projection-policy-gap-hold-judgment-1.md`  `6f8f1336e4cf5add776a4f756bab4c125ca56e2fb0a50ef80aee4bff7c9a490c`

Do not edit, move, remove or commit them.

# 3. read scope

Canonical rules/state/provenance:

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md
.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_SECURITY_SANDBOX.md
.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md
.aiassistant/records/command-center/JUDGMENT_RUBRIC.md
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/records/aiscc/runtime/stockroom-image-provenance.v1.json
.aiassistant/records/aiscc/runtime/stockroom-private-postgres-provisioning.v1.json
.aiassistant/tasks/done/20260912_1605_aiscc-p2-3-private-s1-cut-c-final-readiness-binding-1.md
.aiassistant/tasks/done/20260912_1622_aiscc-p2-3-private-s1-cut-c-postgres-projection-contract-retry-1.md
.aiassistant/records/aiscc/cycles/20260912_1633_aiscc-p2-3-cut-c-docker-image-authority-entrypoint-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_1633_aiscc-p2-3-cut-c-docker-image-authority-entrypoint-policy-gap-hold-judgment-1.md
```

Production/readiness source scope:

```text
src/aiscc/bootstrap.py
src/aiscc/runtime/docker.py
src/aiscc/runtime/stockroom_image.py
src/aiscc/runtime/stockroom_workspace.py
src/aiscc/scenarios/composition.py
src/aiscc/scenarios/stockroom_production.py
src/aiscc/persistence/**
src/aiscc/evidence/repository.py
src/aiscc/judgment/authority.py
config/providers/stockroom-tools.v2.toml
config/providers/stockroom-owner-profiles.v2.toml
config/evidence/stockroom-capture.v1.json
config/human/stockroom-capture.v1.json
config/judgment/stockroom-capture.v2.json
config/scenarios/stockroom/v1/resource.json
config/scenarios/stockroom/v1/fixtures/policy-conflict.json
```

Use targeted reads where appropriate. No unrelated bulk read.

# 4. repository preflight

Require:

```text
branch main
HEAD 6d41633210f0e556dd4292ee62a8600c6b54215f
HEAD^ fdd3b9ac2f0d8db447ed0ed055aa4b02eab4b30d
HEAD^^ 474826340a89b5c597aa066ff0d414bfc8f43229
index empty
tracked worktree clean
```

Current state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `3be49a5784cdb1d814c65be321c1256f0cd36798e35d9c63c78bd9c5d898b041`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `a17ed3247c88e89cd9ca101fd3944ccb7f2bba01bb1cc4ebc4232aa36c5d5251`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `34ca3d085e6c1b12c73f5a3ff994e71b2189b56e0f10531cb85a6d02ccbbc032`

Before delivery require Git-visible untracked exactly six predecessor artifacts from section 2.

After current Cycle/Judgment placement require:

```text
Git-visible untracked:
8 exact

previous six
current Cycle
current Judgment

current active Task:
byte-exact / ignored
```

Any extra/missing/different path:

```text
DIRTY_WORKSPACE_MIXED or BASELINE_IDENTITY_MISMATCH
→ STOP_WITH_REPORT_EXPORT
```

# 5. Cut A source baseline

Require all 19 exact:

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

Mismatch:

```text
SOURCE_BASELINE_IDENTITY_MISMATCH
→ STOP_WITH_REPORT_EXPORT
```

# 6. retained provenance bytes

Require unchanged:

```text
stockroom-image-provenance.v1.json:
e19f2b645aee85878bed7c557064bbbd0be746524f394ad88de1d2509c13b64f

stockroom-private-postgres-provisioning.v1.json:
36b9c93515223ade3d74923141fcbe823907b42b81e5d86bf3666a4f02032b54
```

Do not rewrite them.

# 7. public production entrypoint authority

Current accepted public entrypoint is:

```python
from aiscc.bootstrap import build_stockroom_production
```

Require its current signature to match the accepted source and include exactly the production parameters needed by section 15.

`build_stockroom_production_application(...)` may be read to derive construction-time DB mutation semantics, but **must not be called directly by this Task**.

Production construction invocation count:

```text
build_stockroom_production:
exactly 1 on success

build_stockroom_production_application direct external invocation:
0
```

The wrapper's internal delegation is not a second external invocation.

# 8. exact PostgreSQL sanitized projection

Construct exactly:

```json
{"container_id":"0b50ac47a79e05ac9b88a8f679d04ddc39f729bf1a8e099d149c4c5570b5999c","container_name":"aiscc-p2-3-private-postgres-v1","data_volume":{"destination":"/var/lib/postgresql/data","name":"aiscc-p2-3-private-postgres-data-v1","rw":true},"database_name":"aiscc_private_capture","image_id":"sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94","image_repodigest":"postgres@sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94","labels":{"io.aiscc.lifecycle":"p2-3-s1-s4-corpus","io.aiscc.owner":"p2-3-private-capture","io.aiscc.provisioning-id":"aiscc-p2-3-private-postgres-v1","io.aiscc.task-id":"20260912_0420_aiscc-p2-3-private-s1-cut-b-clean-authority-provisioning-retry-1"},"password_file_destination":"/run/secrets/postgres_password","published_endpoint":{"container_port":5432,"host_ip":"127.0.0.1","host_port":55432},"role_name":"aiscc_private_capture","secret_bind":{"destination":"/run/secrets/postgres_password","read_only":true},"state_status":"running"}
```

Extraction:

```text
container_id:
PostgreSQL container inspect .Id

container_name:
PostgreSQL container inspect .Name without leading slash

image_id:
exact PostgreSQL image inspect .Id

image_repodigest:
select exact required RepoDigest
postgres@sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94
from PostgreSQL image inspect RepoDigests;
it must be present

labels:
exact four AISCC container labels shown above
from PostgreSQL container Config.Labels;
reject any additional io.aiscc.* label

state_status:
PostgreSQL container State.Status

published_endpoint:
single TCP/5432 binding from container inspect

data_volume:
single named-volume mount at /var/lib/postgresql/data

secret_bind:
single bind at /run/secrets/postgres_password;
destination/read_only only;
never include Source

database_name:
POSTGRES_DB

role_name:
POSTGRES_USER

password_file_destination:
POSTGRES_PASSWORD_FILE
```

Cross-check:

```text
container .Image == PostgreSQL image inspect .Id == sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94
```

Canonical fingerprint bytes:

```python
json.dumps(
    projection,
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
).encode("utf-8")
```

Require:

```text
canonical fingerprint:
867e744367eb804c30db6269d0700d8679c5aeb1a9b6fb78306ce1b87918c8e7

exported POSTGRES_SANITIZED_INSPECT.json:
canonical bytes + one LF

whole-file SHA-256:
e50fea1be09dd8e2ea44a217c36c08751c94de0d873bb136ef41b2235f9c4b25
```

No alternate schema/serializer/hash search.

# 9. exact Docker observation allowlist

Resolve absolute current `docker.exe` without network.

**Only these four Docker observation resources are authorized:**

```text
1. docker image inspect sha256:c51ad05852b58a3b4fd275ee88d183551e745d79ac8239e3da3b98372fe0bb9e

2. docker image inspect sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94

3. docker container inspect aiscc-p2-3-private-postgres-v1

4. docker volume inspect aiscc-p2-3-private-postgres-data-v1
```

Equivalent exact-ID/name read-only syntax is allowed only for those four resources.

Forbidden:

```text
all other Docker resources
docker ps/list inventory as discovery
build/pull/run/create/start/stop/restart/rm/tag/prune
registry/network lookup
```

Stockroom image must satisfy accepted source-owned image inspection and retain:

```text
image ID:
sha256:c51ad05852b58a3b4fd275ee88d183551e745d79ac8239e3da3b98372fe0bb9e

inspect projection SHA:
e5350a7236cc496d1d2abec80e52e900616d3935d1e26db1c7e967ca771f1e57
```

PostgreSQL image/container/volume must satisfy section 8 and retained container ID:

```text
0b50ac47a79e05ac9b88a8f679d04ddc39f729bf1a8e099d149c4c5570b5999c
```

# 10. private credential bind authority

From the already-authorized exact PostgreSQL container inspect, select exactly one bind:

```text
destination:
/run/secrets/postgres_password

read_only:
true
```

Its host Source path is private authority.

Never print/export/hash that path or the password value.

Privately verify:

```text
absolute regular file
exists
not symlink/reparse
outside repository
outside Downloads
outside target/export
effective ACL no broader than protected private parent
```

No filesystem search for alternatives.

# 11. final private runtime root

Derive only:

```text
<verified secret Source parent>/aiscc-p2-3-private-runtime-v1
```

Require preexisting = No.

If it already exists:

```text
PRIVATE_RUNTIME_ROOT_PREEXISTING
→ STOP_WITH_REPORT_EXPORT
```

Create exactly this directory.
Require non-reparse, ACL no broader than parent, and zero entries.

Retain it empty.
Do not export its absolute path.

# 12. typed Stockroom image resolution

Parse canonical Stockroom image provenance with accepted source APIs.

Construct exact `StockroomImageProvenanceRef`.

Require production `resolve_stockroom_image(...)` to resolve:

```text
sha256:c51ad05852b58a3b4fd275ee88d183551e745d79ac8239e3da3b98372fe0bb9e
```

No pseudo-ref, monkeypatch, fixture image or custom resolver.

# 13. private PostgreSQL readiness

Read password only into process memory.

Construct DB connection only in memory via current supported persistence/SQLAlchemy APIs.

Never print/export password or credential-bearing URL.

Verify:

```text
connectivity PASS
database aiscc_private_capture
role aiscc_private_capture
migration head 20260901_0008
```

Before production construction, enumerate current AISCC application/domain tables.

Require:

```text
all application/domain rows = 0
```

`alembic_version` is migration metadata and excluded.

# 14. exact construction-time DB mutation envelope

Before invoking the public wrapper, inspect exact current implementations of:

```text
aiscc.bootstrap.build_stockroom_production
aiscc.scenarios.stockroom_production.build_stockroom_production_application
PostgresEvidenceRepository.register_authority
JudgmentPolicyAuthority.register
```

Using current Stockroom configs, derive the exact tables/rows that can be inserted/confirmed solely by application construction.

If the mutation envelope is ambiguous:

```text
PRODUCTION_READINESS_DB_MUTATION_SCOPE_UNCERTAIN
→ STOP before construction
```

# 15. public production build exactly once

Create async session factory through current persistence APIs.

Call:

```python
await build_stockroom_production(...)
```

exactly once with:

```text
session_factory:
verified private DB async session factory

repository_root:
current repository root

private_runtime_root:
section 11 root

downloads_root:
C:\Users\oracl\Downloads

trusted_git_executable:
resolved absolute git.exe

image_provenance_ref:
section 12 exact typed ref

trusted_docker_executable:
section 9 exact docker.exe

cancellation.run_id:
aiscc-cut-c-readiness-only

cancellation.attempt_id:
aiscc-cut-c-readiness-attempt

project_id:
aiscc-stockroom-private-capture

requester_identity:
aiscc-owner-operator

human_selector_fingerprint:
c55280095ff8bbac5ab186e44e3856e6a435da548c1c88b02b66caeba36e8f07

secret_material_by_ref:
exact current LOCAL_COMPATIBILITY_SECRET_REF → LOCAL_COMPATIBILITY_SENTINEL

clock:
omit / use production default
```

No direct external call to `build_stockroom_production_application`.
No fake owner/custom injection/monkeypatch.

# 16. readiness assertions

Without calling `prepare_capture()` verify:

```text
application repository/private/download roots exact
project/requester/Human selector exact
composition admitted image exact

4 evidence enrollments exact
S1 + S2 judgment enrollments exact
S4 human enrollment exact
OWNER_SELF_DOGFOOD policy authority exact

StockroomWorkspace exists
StockroomDockerRunner/DockerRuntime exists
workflow/evidence/human/judgment/provider/security owners exist

private runtime root still empty
```

# 17. DB post-build mutation envelope

Recount all application/domain tables.

Every changed row/table must be explained by section 14 construction-time registration.

Require runtime execution state remains zero:

```text
WorkRun/execution attempt/output = 0
transition runtime/state execution = 0
HumanGate/HumanResult = 0
Judgment outcome = 0
scenario/capture runtime = 0
```

Authority registration rows must match exact current Stockroom config.

Any unexplained mutation:

```text
READINESS_DB_MUTATION_ENVELOPE_VIOLATION
→ STOP_WITH_REPORT_EXPORT
```

# 18. hard execution ceiling

Forbidden:

```text
application.prepare_capture(...)
materialization
StockroomDockerRunner process dispatch
scenario Docker container create/start/run
provider/tool execution
WorkRun creation
TransitionRequest for S1-S4
scenario evidence submission
Human gate opening
HumanResult
scenario Judgment
S1/S2/S3/S4
Replay
```

# 19. post-readiness retained state

Require:

```text
Stockroom image unchanged
PostgreSQL image unchanged
PostgreSQL container same ID / running
PostgreSQL volume same
migration head 20260901_0008
candidate provenance files unchanged
password file untouched
private runtime root retained / empty
new Stockroom scenario runtime container = none by command history and exact authorized resources
```

Do not discover/delete CURRENT_HELPER_1..4.

# 20. repository/Git boundary

No tracked/source/state mutation.
No git add/commit/push.

At terminal completion move current Task byte-identically:

```text
.aiassistant/tasks/active/20260912_1633_aiscc-p2-3-private-s1-cut-c-docker-image-authority-and-public-entrypoint-retry-1.md
→
.aiassistant/tasks/done/20260912_1633_aiscc-p2-3-private-s1-cut-c-docker-image-authority-and-public-entrypoint-retry-1.md
```

Expected final Git-visible untracked exactly nine:

```text
six predecessor done/Cycle/Judgment artifacts
current done Task
current Cycle
current Judgment
```

HEAD remains `6d41633210f0e556dd4292ee62a8600c6b54215f`.

# 21. evidence contract

executor_required:
- transport + six predecessor artifact identities
- repository/state/source/provenance baselines
- public production entrypoint signature/boundary
- four-resource Docker observation allowlist
- exact PostgreSQL projection
- private credential boundary
- private runtime root
- typed image resolver
- private DB connectivity/pristine proof
- mutation-envelope derivation
- public build_stockroom_production exactly once
- owner/enrollment readiness
- post-build DB bounded mutation
- no scenario execution
- retained environment post-state
- exact private-value export scan
- export integrity

reuse_allowed:
- 1605/1622 static/bootstrap proof where current hashes remain exact
- 1533 Browser acceptance
- Cut B admitted/persisted provenance
- 1400 cleanup acceptance

human_owned:
- Browser Cut C review/admission
- future private S1 authorization

not_required:
- source changes
- test suite
- browser QA
- network/registry
- Git persistence
- residue cleanup

# 22. contract review

Require exactly 35 rows:

```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_CLEAN
PREDECESSOR_1605_1622_ARTIFACTS_EXACT
CURRENT_STATE_HASHES_EXACT
CUT_A_19_HASHES_EXACT
CANDIDATE_PROVENANCE_HASHES_EXACT
PUBLIC_PRODUCTION_ENTRYPOINT_EXACT
POSTGRES_PROJECTION_CONTRACT_EXACT
DOCKER_OBSERVATION_ALLOWLIST_EXACT
RETAINED_STOCKROOM_IMAGE_IDENTITY_EXACT
RETAINED_POSTGRES_IMAGE_IDENTITY_EXACT
RETAINED_POSTGRES_CONTAINER_VOLUME_EXACT
POSTGRES_SANITIZED_PROJECTION_EXACT
SECRET_BIND_DESTINATION_RO_EXACT
SECRET_SOURCE_PRIVATE_EXACT
SECRET_VALUE_NOT_EXPORTED
RUNTIME_ROOT_DERIVATION_EXACT
RUNTIME_ROOT_PREABSENT
RUNTIME_ROOT_CREATED_SECURE_EMPTY
TYPED_IMAGE_REF_EXACT
IMAGE_PRODUCTION_RESOLVER_PASS
PRIVATE_DB_CONNECTION_PASS
MIGRATION_HEAD_EXACT
PRE_READINESS_DATABASE_PRISTINE
PUBLIC_PRODUCTION_BUILD_ONCE_PASS
AUTHORITY_ENROLLMENTS_EXACT
DATABASE_MUTATION_ENVELOPE_EXACT
RUNTIME_ROOT_REMAINS_EMPTY
NO_DOCKER_PROCESS_DISPATCH
NO_PREPARE_CAPTURE_WORKRUN_PROVIDER_TOOL
NO_S1_S4_REPLAY
NO_SOURCE_STATE_GIT_MUTATION
RETAINED_ENVIRONMENT_POST_EXACT
SECRET_PRIVATE_PATH_EXPORT_SCAN_PASS
EXPORT_INTEGRITY_PASS
```

Require:

```text
35 / 35 PASS
```

# 23. success export

Target:

```text
.aiassistant/reports/target/20260912_1633_aiscc-p2-3-private-s1-cut-c-docker-image-authority-and-public-entrypoint-retry-1/
```

Root files exactly 14:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
SOURCE_BASELINE_VERIFICATION.md
RETAINED_ENVIRONMENT_VERIFICATION.md
POSTGRES_SANITIZED_INSPECT.json
SECRET_BOUNDARY_VERIFICATION.md
PRIVATE_RUNTIME_ROOT_VERIFICATION.md
IMAGE_RESOLVER_VERIFICATION.md
DATABASE_READINESS_VERIFICATION.md
PRODUCTION_APPLICATION_READINESS_VERIFICATION.md
NO_SCENARIO_EXECUTION_VERIFICATION.md
CONTRACT_REVIEW.md
```

Canonical/candidate copies exactly five:

```text
.aiassistant/records/aiscc/cycles/20260912_1633_aiscc-p2-3-cut-c-docker-image-authority-entrypoint-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_1633_aiscc-p2-3-cut-c-docker-image-authority-entrypoint-policy-gap-hold-judgment-1.md
.aiassistant/tasks/done/20260912_1633_aiscc-p2-3-private-s1-cut-c-docker-image-authority-and-public-entrypoint-retry-1.md
.aiassistant/records/aiscc/runtime/stockroom-image-provenance.v1.json
.aiassistant/records/aiscc/runtime/stockroom-private-postgres-provisioning.v1.json
```

Expected success:

```text
19 total members
18 non-self manifest rows
one top-level directory
CRC PASS
folder/archive byte equality
TASK.md == current done Task
POSTGRES_SANITIZED_INSPECT.json SHA-256 == e50fea1be09dd8e2ea44a217c36c08751c94de0d873bb136ef41b2235f9c4b25
canonical projection fingerprint == 867e744367eb804c30db6269d0700d8679c5aeb1a9b6fb78306ce1b87918c8e7
```

Blocked export may omit genuinely unavailable success-only evidence; never fabricate it.

# 24. private export guard

After private values are acquired, scan every exported byte for exact:

```text
password value
private host secret Source path
private runtime-root absolute path
credential-bearing DB URL
```

Also reject raw Docker inspect containing private bind Source.

Leak:

```text
SECRET_OR_PRIVATE_PATH_EXPORT_FINDING
→ remove unsafe temporary export bytes
→ preserve repository/environment
→ STOP with safe metadata only
```

# 25. mandatory stop

After named blocker:

```text
no S1
no source repair
no environment rebuild
no broad cleanup
no implicit evidence-channel substitution
```

If private runtime root has been created before a later blocker, retain it and report only safe state.

# 26. success ceiling

```text
Cut C:
READINESS_COMPLETE_CANDIDATE

private runtime root:
CREATED / RETAINED / EMPTY

PostgreSQL projection:
PASS / 867e744367eb804c30db6269d0700d8679c5aeb1a9b6fb78306ce1b87918c8e7

production entrypoint:
aiscc.bootstrap.build_stockroom_production / EXACTLY_ONCE

production image resolver:
PASS

owner graph:
CONSTRUCTED / READINESS_ONLY

database authority enrollment:
BOUNDED / VERIFIED

S1-S4:
NOT_EXECUTED

Cut C Browser admission:
HUMAN_PENDING

private S1:
NOT_AUTHORIZED

Git persistence:
NOT_PERFORMED

P2-3:
IN_PROGRESS
```
