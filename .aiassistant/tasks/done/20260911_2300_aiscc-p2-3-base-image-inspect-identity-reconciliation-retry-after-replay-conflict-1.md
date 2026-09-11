# 작업지시서: P2-3 base-image inspect identity reconciliation retry after replay conflict

## meta

- task_id: `20260911_2300_aiscc-p2-3-base-image-inspect-identity-reconciliation-retry-after-replay-conflict-1`
- created_at: `2026-09-11T23:00:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `EVIDENCE_RECONCILIATION_AUDIT_RETRY / NO_MUTATION`
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

Retry the blocked 2250 local Docker inspect reconciliation from its actual completed lifecycle state.

Do not modify product/config/test source.

Do not provision anything.

# 1. inbound transport

Verify this Browser ZIP filename/SHA-256 from the Short Prompt.

Place current Task first:

```text
.aiassistant/tasks/active/20260911_2300_aiscc-p2-3-base-image-inspect-identity-reconciliation-retry-after-replay-conflict-1.md
```

Read fully and require it is ignored by canonical Git policy.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260911_2300_aiscc-p2-3-base-image-inspect-replay-conflict-retry-entry-1.cycle.md
SHA-256:
50e19fcca5e99741174753c2a318844f23813bf4f7f866e17c513c8e4b6efbef

.aiassistant/reports/aiscc/20260911_2300_aiscc-p2-3-base-image-inspect-replay-conflict-judgment-1.md
SHA-256:
b4b4f1f5870ef2d456725599a4e06bbbe0409fd3cc019b1322114707e5cf537d
```

Bootstrap failure:

```text
STOP
no Docker probe
no report/export
```

# 2. base repository gate

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

Before this delivery exact Git-visible set is 12:

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

Require all exact predecessor hashes:

- `.aiassistant/tasks/done/20260911_1935_aiscc-p2-3-actual-capture-runtime-prerequisite-verification-1.md`  `19b8bcc1f51c6d4be0ec3683e41c6d61884769bc01dc72f335a9c8ae6ab19a63`
- `.aiassistant/records/aiscc/cycles/20260911_1935_aiscc-p2-3-a2-terminal-persisted-runtime-prerequisite-verification-entry-1.cycle.md`  `8f1e5fa2ad6a18b1ff5a2118f24e81c249c81618a96b70ff067d54875de9b730`
- `.aiassistant/reports/aiscc/20260911_1935_aiscc-p2-3-a2-terminal-persistence-final-acceptance-judgment-1.md`  `814b5baf655ba5149ab91ecbaa81e9c14eb1f02fb9bfd54f5e737c405a765b03`
- `.aiassistant/tasks/done/20260911_2140_aiscc-p2-3-private-s1-runtime-provisioning-contract-audit-1.md`  `881988722767df492c24f5e68a680c8ea316362b5b8a8f09117695bf538595e7`
- `.aiassistant/records/aiscc/cycles/20260911_2140_aiscc-p2-3-runtime-prerequisite-not-ready-provisioning-contract-audit-entry-1.cycle.md`  `ea3bd58bb66a6ea233013de75161605b249e32bd6537cd095a88ec090ba55144`
- `.aiassistant/reports/aiscc/20260911_2140_aiscc-p2-3-runtime-prerequisite-verification-final-judgment-1.md`  `db3e7d5101c43c22567396d80732f47227c25179bb6544c416a8e0058a994ecd`
- `.aiassistant/tasks/done/20260911_2148_aiscc-p2-3-private-s1-image-build-input-authority-reconciliation-audit-1.md`  `9a3ebd04c4e13512d151d963e25af0424479876ddb21fc8a170878c9e3d74164`
- `.aiassistant/records/aiscc/cycles/20260911_2148_aiscc-p2-3-provisioning-contract-partial-hold-image-build-authority-rework-entry-1.cycle.md`  `63de3c09811b4041979e53dbeeb03fdb6ab9c723a209cee4d2df2f436d0176ed`
- `.aiassistant/reports/aiscc/20260911_2148_aiscc-p2-3-provisioning-contract-audit-image-build-authority-gap-judgment-1.md`  `529719fb0b4ae54ba613b7c6652124318d6f5083fee273c08d47651191311cae`
- `.aiassistant/tasks/done/20260911_2250_aiscc-p2-3-base-image-inspect-identity-reconciliation-audit-1.md`  `c1abadf7cb3571a456a9dca450952d8460eace46b9bb38b357b0d3175ffebd63`
- `.aiassistant/records/aiscc/cycles/20260911_2250_aiscc-p2-3-image-build-authority-inspect-evidence-rework-entry-1.cycle.md`  `48dee03f20432232c9d299af288e062fdbe821335d6b3a5b5567c220c697f71e`
- `.aiassistant/reports/aiscc/20260911_2250_aiscc-p2-3-image-build-authority-inspect-identity-inconsistency-judgment-1.md`  `78d7bd9bf31d63c31d7c0b2fd754794ed1e9d07eae961c450a7742e5089e6603`

No extra/missing Git-visible path.

# 3. exact stale-active duplicate reconciliation

The previous replay reported that both existed:

```text
done:
.aiassistant/tasks/done/20260911_2250_aiscc-p2-3-base-image-inspect-identity-reconciliation-audit-1.md

active:
.aiassistant/tasks/active/20260911_2250_aiscc-p2-3-base-image-inspect-identity-reconciliation-audit-1.md
```

The done Task must exist and hash exactly:

```text
c1abadf7cb3571a456a9dca450952d8460eace46b9bb38b357b0d3175ffebd63
```

If the old active Task does not exist:

```text
record:
ALREADY_ABSENT
continue
```

If it exists, require all:

```text
active SHA-256 == c1abadf7cb3571a456a9dca450952d8460eace46b9bb38b357b0d3175ffebd63
done SHA-256 == c1abadf7cb3571a456a9dca450952d8460eace46b9bb38b357b0d3175ffebd63
active bytes == done bytes
git check-ignore confirms active path is ignored
```

Only then delete exactly:

```text
.aiassistant/tasks/active/20260911_2250_aiscc-p2-3-base-image-inspect-identity-reconciliation-audit-1.md
```

No other cleanup.

If active exists but any equality/ignore check fails:

```text
PREDECESSOR_TASK_DUPLICATE_MISMATCH
→ STOP_WITH_REPORT_EXPORT
```

# 4. corrected current visibility gate

After current Cycle/Judgment placement and after section 3 reconciliation:

```text
Git-visible:
14 exact

active current Task:
exists byte-exact
ignored
```

Exact Git-visible set:

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
- `.aiassistant/records/aiscc/cycles/20260911_2300_aiscc-p2-3-base-image-inspect-replay-conflict-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2300_aiscc-p2-3-base-image-inspect-replay-conflict-judgment-1.md`

Require no other active Task named `20260911_2250_*`.

No product/config/test dirt.

# 5. zero mutation/provisioning

No mutation under:

```text
src/**
config/**
tests/**
examples/**
migrations/**
canonical state records
```

No Git add/commit/push.

Forbidden:

```text
docker pull
docker build/buildx
docker create
docker run
docker tag
docker rmi
docker manifest inspect
registry/API/web lookup
persistent DB creation
actual S1
```

Only local read-only `docker image inspect` is authorized.

# 6. raw local inspect capture

Run:

```text
docker image inspect python:3.12.14-slim-bookworm
```

Capture stdout byte-for-byte to an external Task-owned JSON file outside the repository.

Capture stderr separately.

Require:

```text
exit code == 0
JSON top level == array
array length == 1
```

Compute:

```text
raw stdout byte size
raw stdout SHA-256
raw stderr byte size
raw stderr SHA-256
```

If image is absent:

```text
BASE_IMAGE_LOCAL_EVIDENCE_ABSENT
```

This is a valid audit result; do not pull it.

# 7. independent parse

Use an external temp Python script and exact interpreter path.

Do not use inline `python -c`.

Extract exactly:

```text
.Id
.RepoTags
.RepoDigests
.Os
.Architecture
.Created
.Config.User
.Config.WorkingDir
.Config.Entrypoint
.Config.Cmd
```

Define:

```text
BASE_IMAGE_CONFIG_ID = .Id
BASE_IMAGE_REPODIGESTS = .RepoDigests
```

Check exact membership for:

```text
python@sha256:0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579
```

If absent:

```text
PROPOSED_BASE_REPODIGEST_NOT_VERIFIED
```

Never substitute `.Id` for `.RepoDigests`.

# 8. identity separation

Report separately:

```text
CONFIG_ID_HEX
SELECTED_REPODIGEST_HEX
TEXTUAL_HEX_EQUAL:
true/false
```

Even if the payload text matches, preserve the semantic distinction:

```text
.Id:
image config object identity

.RepoDigests:
repository distribution manifest/index identity
```

# 9. prior P1-3 authority audit

Read:

```text
containers/p1_3/Dockerfile.sandbox
containers/p1_3/Dockerfile.evidence
containers/p1_3/compose.yaml
tests/conftest.py

.aiassistant/records/aiscc/cycles/20260827_1941_aiscc-p1-3-security-runtime-safeguard-final-acceptance-1.cycle.md
```

Search repository for:

```text
0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579
python:3.12.14-slim-bookworm
```

Determine whether accepted P1-3 authority fixed:

```text
RepoDigest
local image config ID
tag only
or neither
```

# 10. corrected base authority classification

Choose exactly one:

```text
VERIFIED_SOURCE_FIXED_REPODIGEST
LOCAL_REPODIGEST_PRESENT_BUT_NOT_PRIOR_ACCEPTED
PROPOSED_REPODIGEST_NOT_PRESENT
BASE_IMAGE_LOCAL_EVIDENCE_ABSENT
OTHER_EXACT_CLASSIFICATION
```

For `VERIFIED_SOURCE_FIXED_REPODIGEST`, require both:

```text
raw local inspect contains exact RepoDigest
AND
tracked/accepted P1-3 provenance supports that exact RepoDigest
```

# 11. architecture reconciliation

Re-evaluate only image-identity-dependent parts of 2148:

```text
BASE_IMAGE_PIN_MODEL
BASE_IMAGE_PIN_AUTHORITY
V2_TOOL_CONFIG_IMAGE_BINDING_MODEL
IMAGE_PROVENANCE_SCHEMA
PRODUCTION_PROVENANCE_DEPENDENCY
DOCKERFILE_BUILD_CONTEXT_MODEL
CUT_A_ALLOWLIST
CUT_B_PROVISIONING_INPUTS
CUT_C_CURRENTNESS_BINDING
```

Preserve unaffected decisions unless contradicted.

State exactly one:

```text
2148_ARCHITECTURE_ACCEPTABLE_WITH_EVIDENCE_CORRECTION

or

2148_ARCHITECTURE_REWORK_REQUIRED
```

# 12. future identity separation

Keep distinct:

```text
BASE_REPODIGEST:
python@sha256:<manifest/index digest>

BASE_LOCAL_CONFIG_ID:
sha256:<base config digest>

FUTURE_STOCKROOM_IMAGE_ID:
sha256:<Cut B built image config digest>
```

Do not invent the future Stockroom image ID.

# 13. contract review

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
STALE_ACTIVE_DUPLICATE_RECONCILED_OR_ABSENT
RAW_INSPECT_CAPTURED_OR_IMAGE_ABSENCE_EXACT
RAW_INSPECT_HASHED_WHEN_PRESENT
ID_AND_REPODIGEST_PARSED_SEPARATELY
PROPOSED_REPODIGEST_MEMBERSHIP_CHECKED_WHEN_PRESENT
P1_3_PRIOR_AUTHORITY_CLASSIFIED
FUTURE_STOCKROOM_IMAGE_ID_NOT_INVENTED
CUT_A_AUTHORIZATION_NOT_SELF_ISSUED
```

Require:

```text
16 / 16 PASS
```

# 14. final workspace

Before current Task movement:

```text
Git-visible:
14 exact
index empty
```

Move current active Task byte-identically:

```text
.aiassistant/tasks/active/20260911_2300_aiscc-p2-3-base-image-inspect-identity-reconciliation-retry-after-replay-conflict-1.md
→
.aiassistant/tasks/done/20260911_2300_aiscc-p2-3-base-image-inspect-identity-reconciliation-retry-after-replay-conflict-1.md
```

Final:

```text
Git-visible:
15 exact
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
- `.aiassistant/records/aiscc/cycles/20260911_2300_aiscc-p2-3-base-image-inspect-replay-conflict-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2300_aiscc-p2-3-base-image-inspect-replay-conflict-judgment-1.md`
- `.aiassistant/tasks/done/20260911_2300_aiscc-p2-3-base-image-inspect-identity-reconciliation-retry-after-replay-conflict-1.md`

# 15. required export

Folder:

```text
.aiassistant/reports/target/20260911_2300_aiscc-p2-3-base-image-inspect-identity-reconciliation-retry-after-replay-conflict-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
PREDECESSOR_TASK_REPLAY_RECONCILIATION.md
BASE_IMAGE_INSPECT_RAW.json
BASE_IMAGE_INSPECT_EXTRACTED.json
BASE_IMAGE_IDENTITY_RECONCILIATION.md
P1_3_BASE_IMAGE_AUTHORITY.md
ARCHITECTURE_RECONCILIATION.md
CONTRACT_REVIEW.md
```

Also include byte-preserving:

```text
current Cycle
current Judgment
current done Task
```

Export exact P1-3 source/provenance evidence actually relied on, maximum 8 files.

Expected total:

```text
14 + N
where 0 <= N <= 8
```

If the base image is absent, `BASE_IMAGE_INSPECT_RAW.json` may instead contain a
minimal non-secret structured record of the failed local inspect command, exit code,
and absence classification; do not fabricate Docker inspect fields.

Manifest covers all non-self entries.

# 16. cleanup

Remove only exact external temp parser/stderr files.

Do not delete local images.

# 17. success ceiling

Success:

```text
replay conflict:
RESOLVED

base image inspect identity:
EXACTLY RECONCILED

2148 architecture:
ACCEPTABLE or EXACT_REWORK_IDENTIFIED

Cut A implementation:
NOT_EXECUTED

Cut B provisioning:
NOT_EXECUTED

private S1:
NOT_AUTHORIZED
```
