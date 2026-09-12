# 작업지시서: P2-3 private S1 Cut C Docker Desktop secret-source normalization retry

## meta

- task_id: `20260912_1654_aiscc-p2-3-private-s1-cut-c-docker-desktop-secret-source-normalization-retry-1`
- created_at: `2026-09-12T16:54:45+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `REWORK / PRIVATE_RUNTIME_READINESS_BINDING`
- evidence_profile: `HIGH_RISK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `6d41633210f0e556dd4292ee62a8600c6b54215f`
- required_parent: `fdd3b9ac2f0d8db447ed0ed055aa4b02eab4b30d`
- required_grandparent: `474826340a89b5c597aa066ff0d414bfc8f43229`
- fresh_ide_executor_chat: `FORBIDDEN`
- executor_session_action: `KEEP_EXISTING_1605_1622_1633_IDE_EXECUTOR_CHAT`
- success_ceiling: `CUT_C_READINESS_COMPLETE / BROWSER_REVIEW_PENDING`
- private_s1_authorized: `No`

# 0. purpose

1633 reached the exact retained Docker resources and production image resolver, then stopped
before private-file access because Docker Desktop bind `Source` representation was not defined
as a native Windows-path authority.

This retry adds only an exact reversible source-representation normalization boundary and then
continues the already-authorized Cut C readiness sequence.

Do not execute S1.
Do not mutate product source/state/Git.
Do not rebuild/reprovision retained Docker resources.

# 1. transport

Continue in the existing 1605/1622/1633 IDE Executor chat.

Verify Short Prompt ZIP filename/SHA-256.
Require exactly three flat archive members.

Place current Task first:

```text
.aiassistant/tasks/active/20260912_1654_aiscc-p2-3-private-s1-cut-c-docker-desktop-secret-source-normalization-retry-1.md
```

Require byte equality / ignored.

Then place:

```text
.aiassistant/records/aiscc/cycles/20260912_1654_aiscc-p2-3-cut-c-secret-source-representation-retry-entry-1.cycle.md
SHA-256:
11f4afe011d04432c52df9add6e100f9a93b0452eab9d8835d0dff78b7a74c59

.aiassistant/reports/aiscc/20260912_1654_aiscc-p2-3-cut-c-secret-source-representation-hold-judgment-1.md
SHA-256:
41ede1e72e2ccde9ca3f3dd1e22bd9faa1bdb26eadb16421967ca4d38c2d2f34
```

Bootstrap mismatch:

```text
STOP
no Docker observation
no private path normalization
no file access
no runtime-root action
no DB connection
no report/export
```

# 2. predecessor provenance

Require all nine existing blocked-turn governance artifacts byte-exact:

- `.aiassistant/tasks/done/20260912_1605_aiscc-p2-3-private-s1-cut-c-final-readiness-binding-1.md`  `de52d47cacb4f45d5f16543e1fecaa517aaf5d2e176123386d69461b52f3c732`
- `.aiassistant/records/aiscc/cycles/20260912_1605_aiscc-p2-3-cut-b-reconciled-cut-c-readiness-entry-1.cycle.md`  `859d10407bc41266968adb08386e5f9a39ee54f3dfeaa0748620e45a57e3b12b`
- `.aiassistant/reports/aiscc/20260912_1605_aiscc-p2-3-cut-b-state-reconciliation-final-acceptance-cut-c-authorization-judgment-1.md`  `bec6679de2659607670bcf13c2fea3f760f369c045413ea666eb0fdb1aff16f2`
- `.aiassistant/tasks/done/20260912_1622_aiscc-p2-3-private-s1-cut-c-postgres-projection-contract-retry-1.md`  `645ea23305463084aed11c4b2eb6536993772a690f6ecba61eb005069d0341fa`
- `.aiassistant/records/aiscc/cycles/20260912_1622_aiscc-p2-3-cut-c-postgres-projection-policy-gap-retry-entry-1.cycle.md`  `6bd67df35b8f6e82f09213e252f64d1d31efdd209b6fdfbef980d4c2eaf1fe37`
- `.aiassistant/reports/aiscc/20260912_1622_aiscc-p2-3-cut-c-postgres-projection-policy-gap-hold-judgment-1.md`  `6f8f1336e4cf5add776a4f756bab4c125ca56e2fb0a50ef80aee4bff7c9a490c`
- `.aiassistant/tasks/done/20260912_1633_aiscc-p2-3-private-s1-cut-c-docker-image-authority-and-public-entrypoint-retry-1.md`  `472d582058c33e1adbe47b60b62fb1f790eaceeceeee37d59a87082e08a17b94`
- `.aiassistant/records/aiscc/cycles/20260912_1633_aiscc-p2-3-cut-c-docker-image-authority-entrypoint-retry-entry-1.cycle.md`  `de18417733a2abb32a7f9e2543a9a7f5ead41f8d82c116b2051402b44b085299`
- `.aiassistant/reports/aiscc/20260912_1633_aiscc-p2-3-cut-c-docker-image-authority-entrypoint-policy-gap-hold-judgment-1.md`  `07937e2486f9f5c2b39801fb3aac16eb8d3599ce7ee1a10d6d7cc928be2f7b3f`

Do not edit/remove/commit them.

The ignored helper files from predecessor attempts are operational residue only.
Do not read them as authority and do not clean them.

# 3. authoritative read scope

Read the same bounded rules/state/provenance/source scope used by 1633, including:

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
```

Production/readiness read-only source:

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

No unrelated bulk read.

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

State hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `3be49a5784cdb1d814c65be321c1256f0cd36798e35d9c63c78bd9c5d898b041`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `a17ed3247c88e89cd9ca101fd3944ccb7f2bba01bb1cc4ebc4232aa36c5d5251`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `34ca3d085e6c1b12c73f5a3ff994e71b2189b56e0f10531cb85a6d02ccbbc032`

Before current delivery, Git-visible untracked exactly the nine predecessor artifacts in section 2.

After current Cycle/Judgment placement:

```text
Git-visible untracked:
11 exact

nine predecessor artifacts
current Cycle
current Judgment

current active Task:
byte-exact / ignored
```

Any mismatch:

```text
DIRTY_WORKSPACE_MIXED or BASELINE_IDENTITY_MISMATCH
→ STOP_WITH_REPORT_EXPORT
```

# 5. accepted Cut A source identity

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

Any mismatch:

```text
SOURCE_BASELINE_IDENTITY_MISMATCH
→ STOP_WITH_REPORT_EXPORT
```

# 6. retained provenance

Require:

```text
stockroom-image-provenance.v1.json:
e19f2b645aee85878bed7c557064bbbd0be746524f394ad88de1d2509c13b64f

stockroom-private-postgres-provisioning.v1.json:
36b9c93515223ade3d74923141fcbe823907b42b81e5d86bf3666a4f02032b54
```

Do not rewrite.

# 7. production entrypoint

Public production entrypoint remains:

```python
from aiscc.bootstrap import build_stockroom_production
```

Require current signature exact.

External Task invocation:

```text
build_stockroom_production:
exactly 1 on success

build_stockroom_production_application direct external invocation:
0
```

Internal delegation by the public wrapper is expected.

# 8. PostgreSQL sanitized projection

Construct exactly:

```json
{"container_id":"0b50ac47a79e05ac9b88a8f679d04ddc39f729bf1a8e099d149c4c5570b5999c","container_name":"aiscc-p2-3-private-postgres-v1","data_volume":{"destination":"/var/lib/postgresql/data","name":"aiscc-p2-3-private-postgres-data-v1","rw":true},"database_name":"aiscc_private_capture","image_id":"sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94","image_repodigest":"postgres@sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94","labels":{"io.aiscc.lifecycle":"p2-3-s1-s4-corpus","io.aiscc.owner":"p2-3-private-capture","io.aiscc.provisioning-id":"aiscc-p2-3-private-postgres-v1","io.aiscc.task-id":"20260912_0420_aiscc-p2-3-private-s1-cut-b-clean-authority-provisioning-retry-1"},"password_file_destination":"/run/secrets/postgres_password","published_endpoint":{"container_port":5432,"host_ip":"127.0.0.1","host_port":55432},"role_name":"aiscc_private_capture","secret_bind":{"destination":"/run/secrets/postgres_password","read_only":true},"state_status":"running"}
```

Use exact live image/container/volume observations.

Canonical bytes:

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
fingerprint:
867e744367eb804c30db6269d0700d8679c5aeb1a9b6fb78306ce1b87918c8e7

POSTGRES_SANITIZED_INSPECT.json:
canonical bytes + one LF

whole-file SHA-256:
e50fea1be09dd8e2ea44a217c36c08751c94de0d873bb136ef41b2235f9c4b25
```

The projection excludes bind Source.

# 9. exact Docker observation allowlist

Only these four resources:

```text
docker image inspect sha256:c51ad05852b58a3b4fd275ee88d183551e745d79ac8239e3da3b98372fe0bb9e
docker image inspect sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94
docker container inspect aiscc-p2-3-private-postgres-v1
docker volume inspect aiscc-p2-3-private-postgres-data-v1
```

Equivalent exact-ID/name read-only forms only.

No Docker mutation, inventory discovery, registry or network action.

Require Stockroom inspect fingerprint:

```text
e5350a7236cc496d1d2abec80e52e900616d3935d1e26db1c7e967ca771f1e57
```

Require PostgreSQL container ID:

```text
0b50ac47a79e05ac9b88a8f679d04ddc39f729bf1a8e099d149c4c5570b5999c
```

# 10. exact secret bind selection

From the authorized PostgreSQL container inspect select exactly one:

```text
Type:
bind

Destination:
/run/secrets/postgres_password

RW:
false
```

Let its raw private `Source` string be `raw_source`.

Immediately add the exact raw_source UTF-8 bytes and any platform-native representation bytes
derived below to the private-value export denylist.

Never print, hash, log or export raw_source.

# 11. Docker Desktop source representation normalization

Do **not** call `Path(raw_source).is_absolute()` as the first authority test.

Exactly one of these representation classes is allowed.

## Class A — WINDOWS_NATIVE_ABSOLUTE

Using `PureWindowsPath(raw_source)` require:

```text
is_absolute() == true
drive matches ^[A-Za-z]:$
root == "\"
no relative drive form
```

Native candidate is the same Windows path.

## Class B — DOCKER_DESKTOP_RUN_DESKTOP_MNT_HOST

Require raw_source, after validating it contains `/` separators and no backslash, to match exactly:

```regex
^/run/desktop/mnt/host/([A-Za-z])/([^\x00]+)$
```

Split the suffix on `/`.

Every suffix segment must satisfy:

```text
non-empty
not "."
not ".."
contains no ":"
contains no "\"
```

Map only:

```text
/run/desktop/mnt/host/c/a/b
→
C:\a\b
```

using the captured drive letter and exact suffix segments.

Reverse-map the constructed Windows candidate back to the same daemon representation and require
byte-for-byte equality with raw_source except the drive letter is compared case-insensitively.

## Class C — DOCKER_DESKTOP_HOST_MNT

Same exact segment validation and reversible mapping for:

```regex
^/host_mnt/([A-Za-z])/([^\x00]+)$
```

Example semantic mapping:

```text
/host_mnt/c/a/b
→
C:\a\b
```

Reverse-map and require the same representation class and exact suffix.

## No other class

If none matches:

```text
PRIVATE_SOURCE_REPRESENTATION_UNSUPPORTED
→ STOP_WITH_REPORT_EXPORT
```

Do not:

```text
guess another prefix
search filesystem
use glob
scan user profile
inspect unrelated Docker resources
docker exec
docker cp
copy the secret
ask Human to type the path
```

On successful normalization, report/export only:

```text
source_representation_class:
WINDOWS_NATIVE_ABSOLUTE
or
DOCKER_DESKTOP_RUN_DESKTOP_MNT_HOST
or
DOCKER_DESKTOP_HOST_MNT
```

Never report drive/path/suffix.

Pass row:

```text
SECRET_SOURCE_REPRESENTATION_NORMALIZED_EXACT
```

# 12. normalized private source validation

Only after section 11 succeeds, use the normalized native Windows candidate.

Require:

```text
native Path is absolute
exists
regular file
not symlink/reparse
private parent not symlink/reparse
outside repository
outside Downloads
outside target/export
```

Resolve strictly only after the no-reparse checks.

Require the resolved file still equals the normalized candidate under Windows path semantics.

Verify effective ACL/private access using the same retained Cut B private-boundary policy:
no effective allow broader than current user / LocalSystem / Administrators,
and child rights no broader than the protected private parent.

No password read before this passes.

Pass:

```text
SECRET_SOURCE_PRIVATE_EXACT
```

# 13. final private runtime root

Derive only:

```text
<normalized verified secret parent>/aiscc-p2-3-private-runtime-v1
```

Add its exact absolute representation(s) to the export denylist.

Require before create:

```text
does not exist
not symlink
outside repo/Downloads/target
```

If preexisting:

```text
PRIVATE_RUNTIME_ROOT_PREEXISTING
→ STOP_WITH_REPORT_EXPORT
```

Create exactly this directory only.

Require:

```text
non-reparse directory
ACL no broader than private parent
0 entries
```

Retain it empty.

# 14. typed Stockroom image resolver

Using canonical provenance/source APIs construct exact `StockroomImageProvenanceRef`.

Require production resolver to admit:

```text
sha256:c51ad05852b58a3b4fd275ee88d183551e745d79ac8239e3da3b98372fe0bb9e
```

No fixture/pseudo-ref/monkeypatch.

# 15. private PostgreSQL readiness

Only now read password into process memory.

Add exact raw password bytes, decoded password bytes and credential-bearing DB URL bytes to export denylist.

Build DB URL only in memory.

Verify:

```text
connectivity PASS
database aiscc_private_capture
role aiscc_private_capture
migration head 20260901_0008
```

Before public production construction require all AISCC application/domain tables zero rows.
Exclude only migration metadata table `alembic_version`.

# 16. construction-time mutation envelope

Before public builder call inspect current:

```text
aiscc.bootstrap.build_stockroom_production
aiscc.scenarios.stockroom_production.build_stockroom_production_application
PostgresEvidenceRepository.register_authority
JudgmentPolicyAuthority.register
```

Derive exact construction-time registration envelope.

Expected pristine-DB envelope from current accepted source/config:

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

all other application/domain rows:
0
```

If current source/config cannot prove this exact envelope:

```text
PRODUCTION_READINESS_DB_MUTATION_SCOPE_UNCERTAIN
→ STOP before public build
```

# 17. public production build exactly once

Use current supported async session factory.

Call:

```python
await build_stockroom_production(...)
```

exactly once with:

```text
session_factory:
verified private DB

repository_root:
current repository root

private_runtime_root:
section 13 root

downloads_root:
C:\Users\oracl\Downloads

trusted_git_executable:
resolved absolute git.exe

image_provenance_ref:
section 14 exact typed ref

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
production default
```

No direct external internal-builder call.

# 18. readiness assertions

Without `prepare_capture()` require:

```text
application roots exact
project/requester/human selector exact
admitted image exact
4 evidence enrollments exact
S1 + S2 judgment enrollments exact
S4 human enrollment exact
OWNER_SELF_DOGFOOD mode authority exact
StockroomWorkspace exact type
StockroomDockerRunner/DockerRuntime exact types
workflow/evidence/human/judgment/provider/security owners present
runner dispatched == false
private runtime root remains empty
```

# 19. post-build DB envelope

Recount all application/domain tables.

Require exactly the section 16 envelope.

Verify persisted evidence/judgment authority identities/fingerprints against current config.

Require runtime rows zero:

```text
WorkRun/execution attempt/output
transition execution/state
HumanGate/HumanResult
Judgment outcomes
scenario/capture runtime
```

Any extra mutation:

```text
READINESS_DB_MUTATION_ENVELOPE_VIOLATION
→ STOP_WITH_REPORT_EXPORT
```

# 20. hard execution ceiling

Forbidden throughout:

```text
application.prepare_capture(...)
Stockroom materialization
StockroomDockerRunner process dispatch
scenario Docker create/start/run
provider/tool execution
WorkRun
TransitionRequest
scenario evidence submission
Human gate/result
scenario Judgment
S1/S2/S3/S4
Replay
```

# 21. retained post-state

Require:

```text
Stockroom image unchanged
PostgreSQL image unchanged
PostgreSQL container same ID / running
volume unchanged
migration head unchanged
candidate provenance bytes unchanged
password file metadata unchanged
private runtime root retained / empty
no scenario execution by bounded command history
```

Do not discover/delete prior helpers or CURRENT_HELPER residue.

# 22. repository/Git boundary

No tracked/source/state mutation.
No Git add/commit/push.

At terminal completion move current Task byte-identically:

```text
.aiassistant/tasks/active/20260912_1654_aiscc-p2-3-private-s1-cut-c-docker-desktop-secret-source-normalization-retry-1.md
→
.aiassistant/tasks/done/20260912_1654_aiscc-p2-3-private-s1-cut-c-docker-desktop-secret-source-normalization-retry-1.md
```

Expected final Git-visible untracked:

```text
12 exact

nine predecessor Task/Cycle/Judgment
current done Task
current Cycle
current Judgment
```

Ignored target/helper residue is not Git-visible and is not a gate.

# 23. evidence contract

executor_required:
- transport/predecessor/repository/source/provenance
- public entrypoint
- four-resource Docker observation
- exact sanitized projection
- secret bind exact selection
- reversible source representation normalization
- native private-file/ACL verification
- final private runtime root
- typed image resolver
- private DB pristine proof
- exact construction mutation envelope
- public builder exactly once
- owner graph/enrollment readiness
- exact post-build DB envelope
- no scenario execution
- retained post-state
- exact private-value export scan
- export integrity

reuse_allowed:
- 1633 proof through typed image resolver where exact current bytes/identities remain unchanged
- 1533 Browser acceptance
- Cut B admitted/persisted provenance

human_owned:
- Browser Cut C admission
- future private S1 authorization

not_required:
- product/source changes
- tests
- browser QA
- registry/network
- Git persistence
- residue cleanup

# 24. contract review

Require exactly 36 rows:

```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_CLEAN
PREDECESSOR_1605_1622_1633_ARTIFACTS_EXACT
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
SECRET_SOURCE_REPRESENTATION_NORMALIZED_EXACT
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
36 / 36 PASS
```

# 25. success export

Target:

```text
.aiassistant/reports/target/20260912_1654_aiscc-p2-3-private-s1-cut-c-docker-desktop-secret-source-normalization-retry-1/
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

Five canonical/candidate copies:

```text
.aiassistant/records/aiscc/cycles/20260912_1654_aiscc-p2-3-cut-c-secret-source-representation-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_1654_aiscc-p2-3-cut-c-secret-source-representation-hold-judgment-1.md
.aiassistant/tasks/done/20260912_1654_aiscc-p2-3-private-s1-cut-c-docker-desktop-secret-source-normalization-retry-1.md
.aiassistant/records/aiscc/runtime/stockroom-image-provenance.v1.json
.aiassistant/records/aiscc/runtime/stockroom-private-postgres-provisioning.v1.json
```

Success:

```text
19 total members
18 non-self manifest rows
one top-level directory
CRC PASS
folder/archive bytes exact
TASK.md == current canonical done Task
POSTGRES_SANITIZED_INSPECT.json SHA-256 == e50fea1be09dd8e2ea44a217c36c08751c94de0d873bb136ef41b2235f9c4b25
```

`SECRET_BOUNDARY_VERIFICATION.md` may export only the safe representation class enum and PASS/FAIL booleans,
never raw/normalized private paths.

# 26. private export guard

Scan every outbound byte against all exact acquired private representations:

```text
raw Docker Source bytes
normalized Windows source path bytes
forward-slash normalized source path bytes
private runtime-root path representations
raw password bytes
decoded password bytes
credential-bearing DB URL bytes
JSON-escaped forms where applicable
```

Reject credential URL pattern independently.

Raw Docker inspect is never exported.

Finding:

```text
SECRET_OR_PRIVATE_PATH_EXPORT_FINDING
→ delete unsafe temporary outbound bytes only
→ preserve repository/environment
→ STOP with safe metadata
```

# 27. mandatory stop

After any blocker:

```text
no S1
no source repair
no environment rebuild
no broad cleanup
no alternate-path search
no proof-channel substitution
```

If runtime root or authority rows have already been created by a later-stage attempt,
preserve them and report safe exact state; do not rerun against nonpristine state without new Browser authority.

# 28. success ceiling

```text
Cut C:
READINESS_COMPLETE_CANDIDATE

secret source representation:
NORMALIZED / PRIVATE / NON_EXPORTED

private runtime root:
CREATED / RETAINED / EMPTY

PostgreSQL projection:
PASS / 867e744367eb804c30db6269d0700d8679c5aeb1a9b6fb78306ce1b87918c8e7

public production builder:
EXACTLY_ONCE

authority enrollment:
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
