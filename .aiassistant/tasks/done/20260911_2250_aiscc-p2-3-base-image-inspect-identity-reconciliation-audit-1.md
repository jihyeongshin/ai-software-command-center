# 작업지시서: P2-3 base-image Docker inspect identity reconciliation audit

## meta

- task_id: `20260911_2250_aiscc-p2-3-base-image-inspect-identity-reconciliation-audit-1`
- created_at: `2026-09-11T22:50:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `EVIDENCE_RECONCILIATION_AUDIT / NO_MUTATION`
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

Resolve the exact Docker local-image identity evidence underlying the proposed base pin.

Do not implement Cut A.

Do not build/pull/create/run any Stockroom or Python image.

Do not use registry/network lookup.

# 1. inbound transport

Verify Browser ZIP filename/SHA-256 from the Short Prompt.

Place current Task first:

```text
.aiassistant/tasks/active/20260911_2250_aiscc-p2-3-base-image-inspect-identity-reconciliation-audit-1.md
```

Read fully; require it is ignored by canonical Git policy.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260911_2250_aiscc-p2-3-image-build-authority-inspect-evidence-rework-entry-1.cycle.md
SHA-256:
48dee03f20432232c9d299af288e062fdbe821335d6b3a5b5567c220c697f71e

.aiassistant/reports/aiscc/20260911_2250_aiscc-p2-3-image-build-authority-inspect-identity-inconsistency-judgment-1.md
SHA-256:
78d7bd9bf31d63c31d7c0b2fd754794ed1e9d07eae961c450a7742e5089e6603
```

Bootstrap failure:

```text
STOP
no Docker probe
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

Before this delivery exact Git-visible set is 9:

- `.aiassistant/tasks/done/20260911_1935_aiscc-p2-3-actual-capture-runtime-prerequisite-verification-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_1935_aiscc-p2-3-a2-terminal-persisted-runtime-prerequisite-verification-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1935_aiscc-p2-3-a2-terminal-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260911_2140_aiscc-p2-3-private-s1-runtime-provisioning-contract-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_2140_aiscc-p2-3-runtime-prerequisite-not-ready-provisioning-contract-audit-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2140_aiscc-p2-3-runtime-prerequisite-verification-final-judgment-1.md`
- `.aiassistant/tasks/done/20260911_2148_aiscc-p2-3-private-s1-image-build-input-authority-reconciliation-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_2148_aiscc-p2-3-provisioning-contract-partial-hold-image-build-authority-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2148_aiscc-p2-3-provisioning-contract-audit-image-build-authority-gap-judgment-1.md`

Require exact predecessor hashes:

- `.aiassistant/tasks/done/20260911_1935_aiscc-p2-3-actual-capture-runtime-prerequisite-verification-1.md`  `19b8bcc1f51c6d4be0ec3683e41c6d61884769bc01dc72f335a9c8ae6ab19a63`
- `.aiassistant/records/aiscc/cycles/20260911_1935_aiscc-p2-3-a2-terminal-persisted-runtime-prerequisite-verification-entry-1.cycle.md`  `8f1e5fa2ad6a18b1ff5a2118f24e81c249c81618a96b70ff067d54875de9b730`
- `.aiassistant/reports/aiscc/20260911_1935_aiscc-p2-3-a2-terminal-persistence-final-acceptance-judgment-1.md`  `814b5baf655ba5149ab91ecbaa81e9c14eb1f02fb9bfd54f5e737c405a765b03`
- `.aiassistant/tasks/done/20260911_2140_aiscc-p2-3-private-s1-runtime-provisioning-contract-audit-1.md`  `881988722767df492c24f5e68a680c8ea316362b5b8a8f09117695bf538595e7`
- `.aiassistant/records/aiscc/cycles/20260911_2140_aiscc-p2-3-runtime-prerequisite-not-ready-provisioning-contract-audit-entry-1.cycle.md`  `ea3bd58bb66a6ea233013de75161605b249e32bd6537cd095a88ec090ba55144`
- `.aiassistant/reports/aiscc/20260911_2140_aiscc-p2-3-runtime-prerequisite-verification-final-judgment-1.md`  `db3e7d5101c43c22567396d80732f47227c25179bb6544c416a8e0058a994ecd`
- `.aiassistant/tasks/done/20260911_2148_aiscc-p2-3-private-s1-image-build-input-authority-reconciliation-audit-1.md`  `9a3ebd04c4e13512d151d963e25af0424479876ddb21fc8a170878c9e3d74164`
- `.aiassistant/records/aiscc/cycles/20260911_2148_aiscc-p2-3-provisioning-contract-partial-hold-image-build-authority-rework-entry-1.cycle.md`  `63de3c09811b4041979e53dbeeb03fdb6ab9c723a209cee4d2df2f436d0176ed`
- `.aiassistant/reports/aiscc/20260911_2148_aiscc-p2-3-provisioning-contract-audit-image-build-authority-gap-judgment-1.md`  `529719fb0b4ae54ba613b7c6652124318d6f5083fee273c08d47651191311cae`

After current Cycle/Judgment placement while Task is active:

```text
Git-visible:
11 exact

active Task:
exists byte-exact
ignored
```

No other dirt.

# 3. zero mutation/provisioning

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

# 4. capture raw local inspect evidence

Run exactly one logical local inspection of:

```text
python:3.12.14-slim-bookworm
```

Use:

```text
docker image inspect python:3.12.14-slim-bookworm
```

Capture stdout byte-for-byte into an external Task-owned temporary JSON file outside
the repository.

Capture stderr separately.

Require:

```text
exit code == 0
JSON top level == array
array length == 1
```

Do not summarize before preserving the raw evidence.

Compute:

```text
raw stdout byte size
raw stdout SHA-256
raw stderr byte size
raw stderr SHA-256
```

# 5. parse inspect evidence independently

Use an external temporary Python script with an exact interpreter path.

Do not use inline `python -c`.

Parse the captured JSON and extract exactly:

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

Record exact JSON scalar/array types.

Define:

```text
BASE_IMAGE_CONFIG_ID = .Id

BASE_IMAGE_REPODIGESTS = .RepoDigests

BASE_IMAGE_SELECTED_REPODIGEST =
exact member equal to:
python@sha256:0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579
```

If that exact member is absent:

```text
PROPOSED_BASE_REPODIGEST_NOT_VERIFIED
```

Do not substitute `.Id`.

# 6. identity-separation invariant

Treat `.Id` and `.RepoDigests[]` as separate semantic fields.

Report:

```text
CONFIG_ID_HEX
SELECTED_REPODIGEST_HEX
TEXTUAL_HEX_EQUAL:
true/false
```

Do not infer that equality would collapse the concepts.

If the parsed values differ from `2148` report prose, classify:

```text
2148_LOCAL_INSPECT_REPORTING_ERROR
```

and correct the architecture reports accordingly.

If raw JSON actually shows textual equality, preserve that exact evidence and classify:

```text
2148_RAW_INSPECT_CONFIRMED
```

without inventing a new explanation.

# 7. repository P1-3 support audit

Read current tracked:

```text
containers/p1_3/Dockerfile.sandbox
containers/p1_3/Dockerfile.evidence
containers/p1_3/compose.yaml
tests/conftest.py
```

Search the repository for the exact proposed RepoDigest.

Read the accepted P1-3 terminal provenance named by the current Decision Register:

```text
.aiassistant/records/aiscc/cycles/20260827_1941_aiscc-p1-3-security-runtime-safeguard-final-acceptance-1.cycle.md
```

and the immediately relevant predecessor runtime-evidence Cycle only if required.

Determine precisely whether prior accepted source/evidence fixed:

```text
the repository RepoDigest
the local config ID
both
or neither
```

Do not merge the two identities.

# 8. corrected base authority decision

Choose exactly one:

```text
A. VERIFIED_SOURCE_FIXED_REPODIGEST
B. LOCAL_REPODIGEST_PRESENT_BUT_NOT_PRIOR_ACCEPTED
C. PROPOSED_REPODIGEST_NOT_PRESENT
D. OTHER_EXACT_CLASSIFICATION
```

For A, require both:

```text
current raw local inspect contains exact RepoDigest
and
tracked/accepted P1-3 provenance supports that RepoDigest as prior accepted input
```

If only local inspect supports it, choose B.

# 9. 2148 architecture reconciliation

Re-evaluate only image-identity-dependent parts of:

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

Preserve unaffected `2148` decisions unless exact evidence contradicts them.

Explicitly state whether:

```text
2148 architecture can be accepted unchanged except inspect-report correction
```

or:

```text
architecture change is required
```

# 10. no future image-ID confusion

The final architecture must keep three identities distinct:

```text
BASE_REPODIGEST:
python@sha256:<manifest/index digest>

BASE_LOCAL_CONFIG_ID:
sha256:<base image config digest>

FUTURE_STOCKROOM_IMAGE_ID:
sha256:<Cut B built image config digest>
```

The future Stockroom image ID must remain absent until Cut B.

# 11. contract review

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
RAW_INSPECT_CAPTURED
RAW_INSPECT_HASHED
ID_AND_REPODIGEST_PARSED_SEPARATELY
PROPOSED_REPODIGEST_EXACT_MEMBERSHIP_CHECKED
P1_3_PRIOR_AUTHORITY_CLASSIFIED
FUTURE_STOCKROOM_IMAGE_ID_NOT_INVENTED
CUT_A_AUTHORIZATION_NOT_SELF_ISSUED
```

Require:

```text
15 / 15 PASS
```

# 12. final workspace

Before Task movement:

```text
Git-visible:
11 exact
index empty
```

Move active Task byte-identically:

```text
.aiassistant/tasks/active/20260911_2250_aiscc-p2-3-base-image-inspect-identity-reconciliation-audit-1.md
→
.aiassistant/tasks/done/20260911_2250_aiscc-p2-3-base-image-inspect-identity-reconciliation-audit-1.md
```

Final:

```text
Git-visible:
12 exact
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
- `.aiassistant/records/aiscc/cycles/20260911_2250_aiscc-p2-3-image-build-authority-inspect-evidence-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_2250_aiscc-p2-3-image-build-authority-inspect-identity-inconsistency-judgment-1.md`
- `.aiassistant/tasks/done/20260911_2250_aiscc-p2-3-base-image-inspect-identity-reconciliation-audit-1.md`

# 13. required export

Folder:

```text
.aiassistant/reports/target/20260911_2250_aiscc-p2-3-base-image-inspect-identity-reconciliation-audit-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
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

Export exact source-evidence copies of the P1-3 files actually relied on, maximum 8.

Expected total:

```text
13 + N
where 0 <= N <= 8
```

`EXPORT_MANIFEST.md` covers all non-self entries with byte size and SHA-256.

Raw inspect JSON is permitted as evidence, but review it for credential/secret material
before export. If any unexpected secret-like material exists, do not export raw
content; instead STOP_WITH_REPORT_EXPORT and report only the path/hash/detection reason.

# 14. cleanup

Remove only exact external temporary parser/stderr files after verified export.

Do not delete local images.

Inbound Downloads cleanup remains best-effort/non-blocking.

# 15. success ceiling

Success:

```text
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
