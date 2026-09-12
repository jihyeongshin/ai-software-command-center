# 작업지시서: P2-3 private S1 Cut C final readiness binding

## meta

- task_id: `20260912_1605_aiscc-p2-3-private-s1-cut-c-final-readiness-binding-1`
- created_at: `2026-09-12T16:05:08+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `QA_ONLY / PRIVATE_RUNTIME_READINESS_BINDING`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `6d41633210f0e556dd4292ee62a8600c6b54215f`
- required_parent: `fdd3b9ac2f0d8db447ed0ed055aa4b02eab4b30d`
- required_grandparent: `474826340a89b5c597aa066ff0d414bfc8f43229`
- fresh_ide_executor_chat: `REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`
- success_ceiling: `CUT_C_READINESS_COMPLETE / BROWSER_REVIEW_PENDING`
- private_s1_authorized: `No`

# 0. purpose

Cut B는 Browser-final-admitted 및 persisted 상태다.

이번 Task는 다음 네 가지로만 Cut C readiness를 완성한다.

```text
1. retained Cut B image/PostgreSQL actual identity revalidation
2. final private runtime-root creation and authority binding
3. admitted image/database provenance를 production owner graph에 binding
4. production application construction/readiness verification
```

**S1을 실행하지 않는다.**

`build_stockroom_production(...)` 호출은 허용하지만
`application.prepare_capture(...)`부터는 금지다.

# 1. inbound transport

Browser Short Prompt의 ZIP filename/SHA-256을 먼저 검증한다.

ZIP은 정확히 flat 3 members여야 한다.

현재 Task를 먼저 배치:

```text
.aiassistant/tasks/active/20260912_1605_aiscc-p2-3-private-s1-cut-c-final-readiness-binding-1.md
```

Task byte equality와 ignored status를 확인한 뒤 다음 두 artifact를 배치한다.

```text
.aiassistant/records/aiscc/cycles/20260912_1605_aiscc-p2-3-cut-b-reconciled-cut-c-readiness-entry-1.cycle.md
SHA-256:
859d10407bc41266968adb08386e5f9a39ee54f3dfeaa0748620e45a57e3b12b

.aiassistant/reports/aiscc/20260912_1605_aiscc-p2-3-cut-b-state-reconciliation-final-acceptance-cut-c-authorization-judgment-1.md
SHA-256:
bec6679de2659607670bcf13c2fea3f760f369c045413ea666eb0fdb1aff16f2
```

ZIP/hash/member/TASK bootstrap mismatch:

```text
STOP
no Docker inspect
no private file access
no runtime-root creation
no DB connection
no report/export
```

# 2. must-read canonical authority

정확히 읽는다.

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
.aiassistant/records/aiscc/cycles/20260912_1605_aiscc-p2-3-cut-b-reconciled-cut-c-readiness-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_1605_aiscc-p2-3-cut-b-state-reconciliation-final-acceptance-cut-c-authorization-judgment-1.md
```

Current production/readiness source를 다음 exact scope에서 읽는다.

```text
src/aiscc/bootstrap.py
src/aiscc/runtime/docker.py
src/aiscc/runtime/stockroom_image.py
src/aiscc/runtime/stockroom_workspace.py
src/aiscc/scenarios/composition.py
src/aiscc/scenarios/stockroom_production.py
src/aiscc/persistence/**
config/providers/stockroom-tools.v2.toml
config/providers/stockroom-owner-profiles.v2.toml
config/evidence/stockroom-capture.v1.json
config/human/stockroom-capture.v1.json
config/judgment/stockroom-capture.v2.json
config/scenarios/stockroom/v1/resource.json
config/scenarios/stockroom/v1/fixtures/policy-conflict.json
```

`src/aiscc/persistence/**`는 현재 production DB URL/session/table mutation owner를 확인하기 위한 read-only scope다.
그 밖의 source/log bulk-read는 금지한다.

# 3. repository preflight

Require:

```text
branch:
main

HEAD:
6d41633210f0e556dd4292ee62a8600c6b54215f

HEAD^:
fdd3b9ac2f0d8db447ed0ed055aa4b02eab4b30d

HEAD^^:
474826340a89b5c597aa066ff0d414bfc8f43229

index:
empty

tracked worktree:
clean

Git-visible untracked before delivery:
none
```

현재 state owner whole-file SHA-256:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `3be49a5784cdb1d814c65be321c1256f0cd36798e35d9c63c78bd9c5d898b041`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `a17ed3247c88e89cd9ca101fd3944ccb7f2bba01bb1cc4ebc4232aa36c5d5251`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `34ca3d085e6c1b12c73f5a3ff994e71b2189b56e0f10531cb85a6d02ccbbc032`

Current Cycle/Judgment 배치 후:

```text
Git-visible untracked:
2 exact

1. .aiassistant/records/aiscc/cycles/20260912_1605_aiscc-p2-3-cut-b-reconciled-cut-c-readiness-entry-1.cycle.md
2. .aiassistant/reports/aiscc/20260912_1605_aiscc-p2-3-cut-b-state-reconciliation-final-acceptance-cut-c-authorization-judgment-1.md

current active Task:
exists byte-exact / ignored
```

extra/missing/different path:

```text
DIRTY_WORKSPACE_MIXED
→ STOP_WITH_REPORT_EXPORT
```

# 4. accepted Cut A production source identity

다음 19 files는 Cut A accepted/persisted bytes와 정확히 같아야 한다.

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

19개 중 하나라도 다르면:

```text
SOURCE_BASELINE_IDENTITY_MISMATCH
→ STOP_WITH_REPORT_EXPORT
```

현재 HEAD에 존재하는 추가 production dependencies는 section 2 exact source scope 안에서 읽어
current implementation을 해석하되 임의 수정하지 않는다.

# 5. admitted retained provenance

Require exact bytes:

```text
.aiassistant/records/aiscc/runtime/stockroom-image-provenance.v1.json
SHA-256:
e19f2b645aee85878bed7c557064bbbd0be746524f394ad88de1d2509c13b64f

.aiassistant/records/aiscc/runtime/stockroom-private-postgres-provisioning.v1.json
SHA-256:
36b9c93515223ade3d74923141fcbe823907b42b81e5d86bf3666a4f02032b54
```

Admitted immutable image identity:

```text
image ID:
sha256:c51ad05852b58a3b4fd275ee88d183551e745d79ac8239e3da3b98372fe0bb9e

discovery tag:
aiscc-stockroom-runtime:p2-3-private-v1

inspect projection SHA-256:
e5350a7236cc496d1d2abec80e52e900616d3935d1e26db1c7e967ca771f1e57
```

Admitted PostgreSQL identity:

```text
container:
aiscc-p2-3-private-postgres-v1

container ID:
0b50ac47a79e05ac9b88a8f679d04ddc39f729bf1a8e099d149c4c5570b5999c

state:
running

loopback:
127.0.0.1:55432 → 5432

volume:
aiscc-p2-3-private-postgres-data-v1

database:
aiscc_private_capture

role:
aiscc_private_capture

migration head:
20260901_0008

sanitized inspect fingerprint:
867e744367eb804c30db6269d0700d8679c5aeb1a9b6fb78306ce1b87918c8e7
```

Do not rewrite either provenance JSON.

# 6. exact Docker read-only revalidation

Resolve current absolute `docker.exe` without network access.

Only these Docker observation actions are authorized:

```text
inspect exact image ID sha256:c51ad05852b58a3b4fd275ee88d183551e745d79ac8239e3da3b98372fe0bb9e
inspect exact container aiscc-p2-3-private-postgres-v1
inspect exact volume aiscc-p2-3-private-postgres-data-v1
```

Equivalent exact-ID/name filtered read-only queries are allowed.

Forbidden:

```text
docker build
docker pull
docker run
docker create
docker start
docker stop
docker restart
docker rm
docker volume create/rm
docker tag
docker prune
registry lookup
broad Docker inventory cleanup
```

Image observation must pass current `stockroom_image.py` admitted-image inspect verification and
the sanitized projection fingerprint must equal:

```text
e5350a7236cc496d1d2abec80e52e900616d3935d1e26db1c7e967ca771f1e57
```

PostgreSQL inspect must prove exact admitted container ID/name/state/loopback/volume/database-role
configuration and sanitized projection fingerprint:

```text
867e744367eb804c30db6269d0700d8679c5aeb1a9b6fb78306ce1b87918c8e7
```

If retained identity drifted:

```text
RETAINED_ENVIRONMENT_IDENTITY_MISMATCH
→ STOP_WITH_REPORT_EXPORT
```

# 7. private credential bind authority

From the **exact PostgreSQL container inspect only**, identify the mount whose destination is:

```text
/run/secrets/postgres_password
```

Require:

```text
mount type:
bind

read-only:
true

exactly one matching destination
```

The host source path is private authority.

Rules:

```text
do not print it
do not place it in report
do not place it in Task/Cycle/Judgment
do not hash the password value
do not export the path
do not search filesystem for alternatives
```

Privately verify source:

```text
absolute regular file
exists
not symlink/reparse
outside repository
outside Downloads
outside target/export
ACL no broader than the retained protected private parent policy
```

Read the password value only into process memory when section 10 needs the DB connection.

The exact password bytes and host source path must be available to the final export secret scanner
but must never be emitted.

# 8. final private runtime-root derivation

Derive the final runtime root **only** from the verified secret bind source parent:

```text
<private-secret-parent> / aiscc-p2-3-private-runtime-v1
```

The literal parent/full path is private and must not be exported.

Before creation require:

```text
leaf:
aiscc-p2-3-private-runtime-v1

path:
outside repository
outside Downloads
outside target/export

exists:
No
```

If the exact root already exists:

```text
PRIVATE_RUNTIME_ROOT_PREEXISTING
→ STOP_WITH_REPORT_EXPORT
```

Do not delete/reuse a preexisting root.

Create exactly this directory only.

Require after creation:

```text
directory:
exists

symlink/reparse:
No

ACL:
no broader than verified private parent

contents:
0 entries
```

Retain this exact empty root for later separately authorized S1-S4 lifecycle.

Do not print/export its absolute path.
A path/factory fingerprint from current AISCC source may be exported.

# 9. exact typed image provenance resolution

Parse the canonical image provenance with current accepted source APIs.

Construct `StockroomImageProvenanceRef` from those exact canonical bytes:

```text
path:
.aiassistant/records/aiscc/runtime/stockroom-image-provenance.v1.json

whole_file_sha256:
e19f2b645aee85878bed7c557064bbbd0be746524f394ad88de1d2509c13b64f

canonical_fingerprint:
e19f2b645aee85878bed7c557064bbbd0be746524f394ad88de1d2509c13b64f

provenance_id:
stockroom-runtime-p2-3-private-v1

provenance_version:
1

issuance:
use the exact typed issuance parsed from the canonical JSON
```

Require current source:

```text
parse_provenance
provenance_payload
canonical_fingerprint
image_policy
resolve_stockroom_image
verify_image_inspect
```

to admit the same retained image.

`resolve_stockroom_image(...)` must return:

```text
image ID:
sha256:c51ad05852b58a3b4fd275ee88d183551e745d79ac8239e3da3b98372fe0bb9e
```

No pseudo image/ref substitution.

# 10. private PostgreSQL readiness

Recover the password value from the exact private file into memory only.

Construct the database connection value only in process memory using the current repository's
supported persistence/SQLAlchemy path.

Never:

```text
print URL
place URL in argv
write URL to repository
write URL to target/export
write password to environment broader than the single bounded child/process that needs it
```

Verify:

```text
connectivity:
PASS

database:
aiscc_private_capture

role:
aiscc_private_capture

migration head:
20260901_0008
```

Before production application construction, capture row counts for all current AISCC
domain/application tables.

Require the accepted pristine pre-readiness state:

```text
all AISCC domain/application tables:
0 rows
```

`alembic_version` is migration metadata and is not part of the zero-row application-table count.

If non-zero application state exists:

```text
PRIVATE_DB_NOT_PRISTINE
→ STOP_WITH_REPORT_EXPORT
```

# 11. production application readiness build

Resolve absolute current `git.exe` and the already-resolved exact `docker.exe`.

Use current accepted `build_stockroom_production(...)` exactly once with:

```text
repository_root:
current repository root

private_runtime_root:
the exact section 8 root

downloads_root:
C:\Users\oracl\Downloads

image_provenance_ref:
the exact section 9 typed ref

trusted executables:
resolved absolute git.exe / docker.exe

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
the exact current LOCAL_COMPATIBILITY_SECRET_REF → LOCAL_COMPATIBILITY_SENTINEL pair from accepted source
```

No custom/fake owner injection.
No monkeypatch.
No test fixture source.

This call may perform only the durable authority enrollment that current production source itself
performs during construction.

Before invoking it, inspect the exact current implementations of:

```text
PostgresEvidenceRepository.register_authority
JudgmentPolicyAuthority.register
```

and derive the precise DB table mutation envelope attributable to application construction.

If the mutation envelope cannot be determined unambiguously:

```text
PRODUCTION_READINESS_DB_MUTATION_SCOPE_UNCERTAIN
→ STOP before build
```

# 12. application readiness assertions

After one successful construction, verify without calling `prepare_capture()`:

```text
application.repository_root:
exact repository root

application.private_runtime_root:
exact private root

application.project_id:
aiscc-stockroom-private-capture

application.requester_identity:
aiscc-owner-operator

application.human_selector_fingerprint:
c55280095ff8bbac5ab186e44e3856e6a435da548c1c88b02b66caeba36e8f07

composition admitted image:
sha256:c51ad05852b58a3b4fd275ee88d183551e745d79ac8239e3da3b98372fe0bb9e

evidence_enrollments:
all 4 canonical SCENARIO_IDS

judgment_enrollments:
canonical S1 + S2 only

human enrollment:
canonical S4 human-owned requirement

runtime mode authority:
OWNER_SELF_DOGFOOD only as current source defines

private runtime root:
still empty
```

Verify source-owned production objects exist:

```text
StockroomWorkspace
StockroomDockerRunner / DockerRuntime
workflow kernel
evidence admission owners
Human gate owners
Judgment owners
provider/tool/security owners
```

Object construction is readiness proof only.

# 13. database mutation envelope

Capture post-build row counts for all AISCC domain/application tables.

Require:

```text
every changed table:
directly attributable to the exact authority-registration call graph derived in section 11

every created/confirmed authority row:
matches exact canonical Stockroom evidence/judgment enrollment identities

WorkRun/execution attempt/output rows:
0

transition execution/state rows:
0

HumanGate/HumanResult rows:
0

Judgment outcome rows:
0

scenario/capture rows:
0
```

No arbitrary data repair or cleanup is authorized.

If any row outside the exact construction-time authority enrollment envelope changes:

```text
READINESS_DB_MUTATION_ENVELOPE_VIOLATION
→ STOP_WITH_REPORT_EXPORT
```

# 14. hard execution ceiling

The following are forbidden even after readiness construction succeeds:

```text
application.prepare_capture(...)
StockroomCaptureRunner execution
StockroomMaterializer.materialize(...)
StockroomDockerRunner process dispatch
Docker scenario container create/start/run
provider call
tool dispatch
AgentExecutionService.execute(...)
WorkRun creation
TransitionRequest for S1-S4
evidence submission for a scenario run
Human gate opening
HumanResult
scenario Judgment
S1
S2
S3
S4
Replay
```

Cut C is readiness binding only.

# 15. post-readiness retained state

Require before export:

```text
retained Stockroom image:
same exact identity

retained PostgreSQL container:
same ID / still running

retained volume:
same exact identity

migration head:
20260901_0008

candidate provenance JSON hashes:
unchanged

private password file:
retained / untouched

private runtime root:
retained / empty

new Stockroom scenario runtime container:
none
```

Do not clean `CURRENT_HELPER_1..4`.
Do not broadly scan for them.

# 16. repository/Git boundary

No tracked repository file mutation is authorized.

No state file mutation is authorized.

No Git add/commit/push.

At successful executor completion:

```text
move current Task byte-identically:
.aiassistant/tasks/active/20260912_1605_aiscc-p2-3-private-s1-cut-c-final-readiness-binding-1.md
→
.aiassistant/tasks/done/20260912_1605_aiscc-p2-3-private-s1-cut-c-final-readiness-binding-1.md
```

Expected final Git state:

```text
HEAD:
6d41633210f0e556dd4292ee62a8600c6b54215f

index:
empty

tracked worktree:
clean

Git-visible untracked:
3 exact

1. current Cycle
2. current Judgment
3. current done Task
```

Ignored target folder/ZIP do not count.

# 17. evidence contract

executor_required:

```text
transport/hash/member
repository/state/source baseline
retained Docker image/PostgreSQL observation
private secret-bind authority
private runtime-root creation/ACL/emptiness
typed image resolver admission
private PostgreSQL connectivity/pristine-state
production application construction
authority enrollment and exact DB mutation envelope
no-execution ceiling proof
post-readiness retained environment identity
export integrity
```

reuse_allowed:

```text
1533 Browser acceptance
Cut B final admission/persistence
Cut B candidate provenance
1400 cleanup acceptance
Cut A accepted source hashes
```

human_owned:

```text
Browser review of Cut C result
Cut C final admission
future private S1 authorization
```

not_required:

```text
source modification
test suite
browser QA
network
registry
Git persistence
Replay
local residue cleanup
```

forbidden:

```text
all section 14 execution actions
all Docker mutation actions
all Git mutation actions
```

# 18. contract review

Require all 30 rows:

```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_CLEAN
CURRENT_STATE_HASHES_EXACT
CUT_A_19_HASHES_EXACT
CANDIDATE_PROVENANCE_HASHES_EXACT
RETAINED_IMAGE_IDENTITY_EXACT
RETAINED_POSTGRES_IDENTITY_EXACT
SECRET_BIND_DESTINATION_RO_EXACT
SECRET_SOURCE_PRIVATE_EXACT
SECRET_VALUE_NOT_EXPORTED
RUNTIME_ROOT_DERIVATION_EXACT
RUNTIME_ROOT_PREABSENT
RUNTIME_ROOT_CREATED_SECURE_EMPTY
TYPED_IMAGE_REF_EXACT
IMAGE_PRODUCTION_RESOLVER_PASS
LOCAL_IMAGE_INSPECT_BINDING_PASS
PRIVATE_DB_CONNECTION_PASS
MIGRATION_HEAD_EXACT
PRE_READINESS_DATABASE_PRISTINE
PRODUCTION_APPLICATION_BUILD_ONCE_PASS
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
30 / 30 PASS
```

Do not add/remove a row without changing both the row list and required count.

# 19. export contract

Success target:

```text
.aiassistant/reports/target/20260912_1605_aiscc-p2-3-private-s1-cut-c-final-readiness-binding-1/
```

Success root documents exactly 13:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
SOURCE_BASELINE_VERIFICATION.md
RETAINED_ENVIRONMENT_VERIFICATION.md
SECRET_BOUNDARY_VERIFICATION.md
PRIVATE_RUNTIME_ROOT_VERIFICATION.md
IMAGE_RESOLVER_VERIFICATION.md
DATABASE_READINESS_VERIFICATION.md
PRODUCTION_APPLICATION_READINESS_VERIFICATION.md
NO_SCENARIO_EXECUTION_VERIFICATION.md
CONTRACT_REVIEW.md
```

Canonical/candidate copies exactly 5:

```text
.aiassistant/records/aiscc/cycles/20260912_1605_aiscc-p2-3-cut-b-reconciled-cut-c-readiness-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_1605_aiscc-p2-3-cut-b-state-reconciliation-final-acceptance-cut-c-authorization-judgment-1.md
.aiassistant/tasks/done/20260912_1605_aiscc-p2-3-private-s1-cut-c-final-readiness-binding-1.md
.aiassistant/records/aiscc/runtime/stockroom-image-provenance.v1.json
.aiassistant/records/aiscc/runtime/stockroom-private-postgres-provisioning.v1.json
```

Expected success export:

```text
18 members total
one top-level directory
17 non-self manifest rows
CRC PASS
folder/archive byte equality
TASK.md == canonical done Task
```

Blocked result may contain fewer success-only artifacts only when they genuinely do not exist.
Do not fabricate them.

# 20. secret/private-path export guard

Before finalizing any report/manifest/ZIP, scan every exported byte against in-memory exact values for:

```text
private password value
private password host source path
private runtime-root absolute path
database URL containing credential
```

Also ensure no report contains raw Docker inspect with the private bind Source.

Allowed public/sanitized values include:

```text
container/image/volume names and IDs already admitted
loopback endpoint
database/role names
migration head
runtime-root leaf name
non-reversible AISCC-generated semantic/factory fingerprints
```

Any private value leak:

```text
SECRET_OR_PRIVATE_PATH_EXPORT_FINDING
→ remove unsafe target/export copy
→ preserve repository/environment
→ STOP and report only safe non-secret blocker metadata
```

# 21. mandatory stop

After any named blocker:

```text
no S1
no scope expansion
no source repair
no environment rebuild
no broad cleanup
```

Only minimal safe evidence/report/export and safe resource retention are allowed.

If the final private runtime root was already created before a later blocker:

```text
preserve it
do not delete it
report only:
CUT_C_PRIVATE_RUNTIME_ROOT_RETAINED / EMPTY or exact safe state
```

# 22. success ceiling

Executor success means only:

```text
Cut C:
READINESS_COMPLETE_CANDIDATE

private runtime root:
CREATED / RETAINED / EMPTY

production image resolver:
PASS

production application owner graph:
CONSTRUCTED / READINESS_ONLY

database authority enrollment:
BOUNDED / VERIFIED

S1-S4:
NOT_EXECUTED

Cut C Browser admission:
HUMAN_PENDING

private S1 authorization:
NOT_AUTHORIZED

Git persistence:
NOT_PERFORMED

P2-3:
IN_PROGRESS
```
