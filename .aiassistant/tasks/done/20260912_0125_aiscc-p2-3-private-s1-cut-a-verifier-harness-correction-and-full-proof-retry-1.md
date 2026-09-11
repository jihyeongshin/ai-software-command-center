# 작업지시서: P2-3 private S1 Cut A verifier harness correction + full proof retry

## meta

- task_id: `20260912_0125_aiscc-p2-3-private-s1-cut-a-verifier-harness-correction-and-full-proof-retry-1`
- created_at: `2026-09-12T01:25:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `PROOF_ONLY_RETRY / EXTERNAL_VERIFIER_CORRECTION`
- evidence_profile: `HIGH_RISK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `21bb0769c5db126c1989d9e0eb8e9f4c5ceade91`
- required_tree: `11b9d62db2d02649509f148aa01f8f74924c5792`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. purpose

Correct only the external temporary static verifier defect from `0120`.

Repository product/config/test/example bytes are frozen.

Then complete the full Cut A executable proof.

# 1. inbound transport

Verify Browser ZIP filename/SHA-256 from the Short Prompt.

Place current Task first:

```text
.aiassistant/tasks/active/20260912_0125_aiscc-p2-3-private-s1-cut-a-verifier-harness-correction-and-full-proof-retry-1.md
```

Read fully and require it is ignored by canonical Git policy.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260912_0125_aiscc-p2-3-cut-a-static-verifier-defect-proof-retry-entry-1.cycle.md
SHA-256:
f2d8615ae1ad4c96ce22c0f2b4dbed7c3fc83f1cb63675d29c971f028ddfc8ab

.aiassistant/reports/aiscc/20260912_0125_aiscc-p2-3-cut-a-static-verifier-harness-defect-judgment-1.md
SHA-256:
3875aae0d1e8dc684da7d34f59f6039e93e17ed258027856d160805154045b29
```

Bootstrap failure:

```text
STOP
no proof execution
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

Before this delivery exact Git-visible set is 46:

- `.aiassistant/records/aiscc/cycles/20260911_1935_aiscc-p2-3-a2-terminal-persisted-runtime-prerequisite-verification-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260911_2140_aiscc-p2-3-runtime-prerequisite-not-ready-provisioning-contract-audit-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260911_2148_aiscc-p2-3-provisioning-contract-partial-hold-image-build-authority-rework-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260911_2250_aiscc-p2-3-image-build-authority-inspect-evidence-rework-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260911_2300_aiscc-p2-3-base-image-inspect-replay-conflict-retry-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260912_0010_aiscc-p2-3-base-image-authority-reconciled-cut-a-implementation-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260912_0020_aiscc-p2-3-cut-a-static-failure-test-syntax-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260912_0100_aiscc-p2-3-cut-a-static-ruff-line-wrap-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260912_0120_aiscc-p2-3-cut-a-integration-fixture-runtime-root-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1935_aiscc-p2-3-a2-terminal-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/reports/aiscc/20260911_2140_aiscc-p2-3-runtime-prerequisite-verification-final-judgment-1.md`
- `.aiassistant/reports/aiscc/20260911_2148_aiscc-p2-3-provisioning-contract-audit-image-build-authority-gap-judgment-1.md`
- `.aiassistant/reports/aiscc/20260911_2250_aiscc-p2-3-image-build-authority-inspect-identity-inconsistency-judgment-1.md`
- `.aiassistant/reports/aiscc/20260911_2300_aiscc-p2-3-base-image-inspect-replay-conflict-judgment-1.md`
- `.aiassistant/reports/aiscc/20260912_0010_aiscc-p2-3-base-image-authority-reconciliation-final-acceptance-judgment-1.md`
- `.aiassistant/reports/aiscc/20260912_0020_aiscc-p2-3-cut-a-static-failure-test-syntax-judgment-1.md`
- `.aiassistant/reports/aiscc/20260912_0100_aiscc-p2-3-cut-a-static-ruff-line-length-failure-judgment-1.md`
- `.aiassistant/reports/aiscc/20260912_0120_aiscc-p2-3-cut-a-integration-fixture-runtime-root-collision-judgment-1.md`
- `.aiassistant/tasks/done/20260911_1935_aiscc-p2-3-actual-capture-runtime-prerequisite-verification-1.md`
- `.aiassistant/tasks/done/20260911_2140_aiscc-p2-3-private-s1-runtime-provisioning-contract-audit-1.md`
- `.aiassistant/tasks/done/20260911_2148_aiscc-p2-3-private-s1-image-build-input-authority-reconciliation-audit-1.md`
- `.aiassistant/tasks/done/20260911_2250_aiscc-p2-3-base-image-inspect-identity-reconciliation-audit-1.md`
- `.aiassistant/tasks/done/20260911_2300_aiscc-p2-3-base-image-inspect-identity-reconciliation-retry-after-replay-conflict-1.md`
- `.aiassistant/tasks/done/20260912_0010_aiscc-p2-3-private-s1-cut-a-image-provenance-and-docker-runner-source-implementation-1.md`
- `.aiassistant/tasks/done/20260912_0020_aiscc-p2-3-private-s1-cut-a-test-syntax-rework-and-full-proof-retry-1.md`
- `.aiassistant/tasks/done/20260912_0100_aiscc-p2-3-private-s1-cut-a-ruff-line-wrap-rework-and-full-proof-retry-1.md`
- `.aiassistant/tasks/done/20260912_0120_aiscc-p2-3-private-s1-cut-a-runtime-root-fixture-rework-and-full-proof-retry-1.md`
- `config/providers/stockroom-owner-profiles.v2.toml`
- `config/providers/stockroom-tools.v2.toml`
- `examples/synthetic-stockroom/.dockerignore`
- `examples/synthetic-stockroom/Dockerfile`
- `examples/synthetic-stockroom/IMAGE_PROVENANCE.md`
- `src/aiscc/bootstrap.py`
- `src/aiscc/providers/local_deterministic.py`
- `src/aiscc/providers/stockroom_tool.py`
- `src/aiscc/runtime/docker.py`
- `src/aiscc/runtime/stockroom_image.py`
- `src/aiscc/scenarios/composition.py`
- `src/aiscc/scenarios/stockroom_production.py`
- `tests/integration/scenarios/test_stockroom_binding.py`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`
- `tests/unit/providers/test_local_deterministic.py`
- `tests/unit/providers/test_stockroom_tool.py`
- `tests/unit/runtime/test_stockroom_docker_settlement.py`
- `tests/unit/runtime/test_stockroom_image.py`
- `tests/unit/scenarios/test_owner_composition.py`

After current Cycle/Judgment placement while Task is active:

```text
Git-visible:
48 exact

active Task:
exists byte-exact
ignored
```

Exact visible set:

- `.aiassistant/records/aiscc/cycles/20260911_1935_aiscc-p2-3-a2-terminal-persisted-runtime-prerequisite-verification-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260911_2140_aiscc-p2-3-runtime-prerequisite-not-ready-provisioning-contract-audit-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260911_2148_aiscc-p2-3-provisioning-contract-partial-hold-image-build-authority-rework-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260911_2250_aiscc-p2-3-image-build-authority-inspect-evidence-rework-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260911_2300_aiscc-p2-3-base-image-inspect-replay-conflict-retry-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260912_0010_aiscc-p2-3-base-image-authority-reconciled-cut-a-implementation-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260912_0020_aiscc-p2-3-cut-a-static-failure-test-syntax-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260912_0100_aiscc-p2-3-cut-a-static-ruff-line-wrap-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260912_0120_aiscc-p2-3-cut-a-integration-fixture-runtime-root-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1935_aiscc-p2-3-a2-terminal-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/reports/aiscc/20260911_2140_aiscc-p2-3-runtime-prerequisite-verification-final-judgment-1.md`
- `.aiassistant/reports/aiscc/20260911_2148_aiscc-p2-3-provisioning-contract-audit-image-build-authority-gap-judgment-1.md`
- `.aiassistant/reports/aiscc/20260911_2250_aiscc-p2-3-image-build-authority-inspect-identity-inconsistency-judgment-1.md`
- `.aiassistant/reports/aiscc/20260911_2300_aiscc-p2-3-base-image-inspect-replay-conflict-judgment-1.md`
- `.aiassistant/reports/aiscc/20260912_0010_aiscc-p2-3-base-image-authority-reconciliation-final-acceptance-judgment-1.md`
- `.aiassistant/reports/aiscc/20260912_0020_aiscc-p2-3-cut-a-static-failure-test-syntax-judgment-1.md`
- `.aiassistant/reports/aiscc/20260912_0100_aiscc-p2-3-cut-a-static-ruff-line-length-failure-judgment-1.md`
- `.aiassistant/reports/aiscc/20260912_0120_aiscc-p2-3-cut-a-integration-fixture-runtime-root-collision-judgment-1.md`
- `.aiassistant/tasks/done/20260911_1935_aiscc-p2-3-actual-capture-runtime-prerequisite-verification-1.md`
- `.aiassistant/tasks/done/20260911_2140_aiscc-p2-3-private-s1-runtime-provisioning-contract-audit-1.md`
- `.aiassistant/tasks/done/20260911_2148_aiscc-p2-3-private-s1-image-build-input-authority-reconciliation-audit-1.md`
- `.aiassistant/tasks/done/20260911_2250_aiscc-p2-3-base-image-inspect-identity-reconciliation-audit-1.md`
- `.aiassistant/tasks/done/20260911_2300_aiscc-p2-3-base-image-inspect-identity-reconciliation-retry-after-replay-conflict-1.md`
- `.aiassistant/tasks/done/20260912_0010_aiscc-p2-3-private-s1-cut-a-image-provenance-and-docker-runner-source-implementation-1.md`
- `.aiassistant/tasks/done/20260912_0020_aiscc-p2-3-private-s1-cut-a-test-syntax-rework-and-full-proof-retry-1.md`
- `.aiassistant/tasks/done/20260912_0100_aiscc-p2-3-private-s1-cut-a-ruff-line-wrap-rework-and-full-proof-retry-1.md`
- `.aiassistant/tasks/done/20260912_0120_aiscc-p2-3-private-s1-cut-a-runtime-root-fixture-rework-and-full-proof-retry-1.md`
- `config/providers/stockroom-owner-profiles.v2.toml`
- `config/providers/stockroom-tools.v2.toml`
- `examples/synthetic-stockroom/.dockerignore`
- `examples/synthetic-stockroom/Dockerfile`
- `examples/synthetic-stockroom/IMAGE_PROVENANCE.md`
- `src/aiscc/bootstrap.py`
- `src/aiscc/providers/local_deterministic.py`
- `src/aiscc/providers/stockroom_tool.py`
- `src/aiscc/runtime/docker.py`
- `src/aiscc/runtime/stockroom_image.py`
- `src/aiscc/scenarios/composition.py`
- `src/aiscc/scenarios/stockroom_production.py`
- `tests/integration/scenarios/test_stockroom_binding.py`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`
- `tests/unit/providers/test_local_deterministic.py`
- `tests/unit/providers/test_stockroom_tool.py`
- `tests/unit/runtime/test_stockroom_docker_settlement.py`
- `tests/unit/runtime/test_stockroom_image.py`
- `tests/unit/scenarios/test_owner_composition.py`
- `.aiassistant/records/aiscc/cycles/20260912_0125_aiscc-p2-3-cut-a-static-verifier-defect-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0125_aiscc-p2-3-cut-a-static-verifier-harness-defect-judgment-1.md`

No extra/missing path.

# 3. exact Cut A candidate identity / zero mutation

Require all 19 current implementation paths exactly:

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
- `tests/integration/scenarios/test_stockroom_capture_runner.py`  `1861a8cfdd1008e5efba6588b17de8ad8b1f6f088912fba026d215a8ab6379f2`
- `tests/unit/providers/test_local_deterministic.py`  `daa58e09dd3e81f2ba4a6edad236685c34a7c63852419ad3188aef51c8fe6209`
- `tests/unit/providers/test_stockroom_tool.py`  `e33b966cf5d575b7e55cd1ced2f3bfcd805833c08c1c66d6c650b693313c285d`
- `tests/unit/runtime/test_stockroom_docker_settlement.py`  `f7a33975072737417b3a922d4acd44e59be29547ceb87c864e24647d46236b19`
- `tests/unit/runtime/test_stockroom_image.py`  `e900bf8db350762655a167def704989527928cef575f69e740b013e5bfa4cee7`
- `tests/unit/scenarios/test_owner_composition.py`  `bfbae533d8453bef3940b1b652c5688b3b375b7e0fa40ae03e3196902888d652`

No repository mutation is authorized under:

```text
src/**
config/**
tests/**
examples/**
migrations/**
canonical state records
```

No new product/config/test/example path.

Any byte difference from section 3:

```text
CUT_A_DRAFT_IDENTITY_MISMATCH
→ STOP_WITH_REPORT_EXPORT
```

# 4. external verifier only

Any verifier/helper script must live outside the repository and be Task-owned temporary
evidence.

Do not use inline `python -c`.

Do not create repository helper files.

Do not modify product/test code to satisfy the verifier.

# 5. compile + Ruff

Do not use `py_compile`.

In-memory compile these exact 14 Python paths:

```text
src/aiscc/bootstrap.py
src/aiscc/runtime/docker.py
src/aiscc/providers/stockroom_tool.py
src/aiscc/providers/local_deterministic.py
src/aiscc/scenarios/composition.py
src/aiscc/scenarios/stockroom_production.py
src/aiscc/runtime/stockroom_image.py
tests/unit/runtime/test_stockroom_docker_settlement.py
tests/unit/runtime/test_stockroom_image.py
tests/unit/providers/test_stockroom_tool.py
tests/unit/providers/test_local_deterministic.py
tests/unit/scenarios/test_owner_composition.py
tests/integration/scenarios/test_stockroom_binding.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Require:

```text
14 / 14 PASS
```

Run Ruff read-only on exactly the same 14:

```text
no --fix
no formatter
0 findings
```

# 6. correct owner-profile V1/V2 comparison

Strict-load through:

```text
load_stockroom_owner_profiles(...)
```

both:

```text
config/providers/stockroom-owner-profiles.v1.toml
config/providers/stockroom-owner-profiles.v2.toml
```

The external verifier MUST NOT construct:

```text
LocalStockroomProfile(...)
```

for expected values.

Use only loader-returned values.

For each exact profile ID:

```text
stockroom-owner-s1-v1
stockroom-owner-s2-v1
stockroom-owner-s3-v1
stockroom-owner-s4-v1
```

define:

```text
v1_local = v1_profiles[profile_id]
v2_local = v2_profiles[profile_id]
```

Require wrapper equality:

```text
type(v1_local) is type(v2_local)
v1_local.scenario_id == v2_local.scenario_id
v1_local.tool_dispatch_allowed == v2_local.tool_dispatch_allowed
```

Require nested provider semantics:

```text
v1_local.profile.tool_registry_id == "aiscc-stockroom-tools"
v2_local.profile.tool_registry_id == "aiscc-stockroom-tools"

v1_local.profile.tool_registry_version == "1"
v2_local.profile.tool_registry_version == "2"
```

Use:

```python
dataclasses.fields(type(v1_local.profile))
```

to enumerate ProviderProfile fields.

Require:

```text
type(v1_local.profile) is type(v2_local.profile)

for every ProviderProfile field except tool_registry_version:
getattr(v1_local.profile, field.name)
==
getattr(v2_local.profile, field.name)
```

Require the field set contains exactly one intended V1/V2 semantic difference:

```text
tool_registry_version
```

Do not assume or invent fields on `LocalStockroomProfile`.

# 7. tool config V1/V2 comparison

Strict-load:

```text
config/providers/stockroom-tools.v1.toml
config/providers/stockroom-tools.v2.toml
```

through the production tool loader.

Require:

```text
V1 exact legacy semantics preserved

V2:
registry_version == "2"
image is absent/non-authoritative
binding_model == IMAGE_IDENTITY_POLICY_AND_PROVENANCE_REF
runtime identity == LOCAL_IMAGE_CONFIG_ID_SHA256
fixed provenance schema/ref/base-image/build/source policy
```

Compare loader-returned models/fields directly.

Do not construct expected runtime tool objects with guessed constructor signatures.

# 8. negative static loader cases

After all four positive loaders/comparisons PASS, execute the prior required negative
cases using external temporary mutated config copies only.

Require fail-closed for:

```text
v2 tool config adds `image`
v2 tool config injects a future/local image ID
mixed or unknown schema/version
source aggregate substituted as runtime image identity
unknown owner-profile root/schema
owner profile tool_registry_version mismatched to its schema
```

Record exact exception class/reason for every case.

Temporary mutated configs must remain outside the repository.

# 9. static workspace gate

Require:

```text
git diff --check:
PASS

index:
empty

all 19 Cut A hashes:
exact section-3 identity

new repo-visible pyc:
0
```

Mandatory static failure:

```text
STATIC_CHECK_FAILURE
→ STOP_WITH_REPORT_EXPORT
```

No same-turn repair.

# 10. targeted unit proof

Only after static PASS, run:

```text
tests/unit/runtime/test_stockroom_image.py
tests/unit/runtime/test_stockroom_docker_settlement.py
tests/unit/providers/test_stockroom_tool.py
tests/unit/providers/test_local_deterministic.py
tests/unit/scenarios/test_owner_composition.py
```

Use exact repo interpreter with:

```text
-B
-p no:cacheprovider
-ra
```

Require all collected PASS / zero skip.

No real Stockroom Docker subprocess.

# 11. disposable PostgreSQL prerequisite

Only after unit PASS, create one exact Task-owned disposable PostgreSQL test container:

```text
postgres:17.6-alpine
--pull=never
loopback only
temporary storage
unique Task-owned name
```

Migrate to:

```text
20260901_0008
```

No named persistent capture volume.

# 12. integration proof

Run:

```text
tests/integration/scenarios/test_stockroom_binding.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Require all collected PASS / zero skip.

Specifically for:

```text
test_production_owner_graph_and_bounded_running_prefix
```

record executable proof that:

```text
test-only provenance exists outside private runtime root
fake Docker executable exists outside private runtime root
dedicated private runtime root exists and is empty
build_stockroom_production passes the empty-root invariant
no real Stockroom Docker/provider/tool edge executes
dedicated private runtime root is empty at end
```

# 13. regression proof

Only after integration PASS, run:

```text
tests/unit/scenarios/test_stockroom_capture_runner.py
tests/unit/security/test_stockroom_policy.py
tests/integration/evidence/test_postgres_evidence_admission.py
tests/integration/human/test_postgres_human_gate_judgment.py
tests/integration/workflow/test_postgres_kernel.py
```

Require all collected PASS / zero skip.

# 14. 32/32 contract review

Require all prior Cut A rows PASS:

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

# 15. forbidden actions

Do not execute:

```text
real Stockroom docker inspect/build/pull/create/run
registry/API/network lookup
Stockroom materialization
provider execution
tool dispatch
actual S1-S4
canonical stockroom-image-provenance.v1.json creation
persistent capture DB/volume
Replay
Git add/commit/push
```

The Task-owned disposable PostgreSQL test container is the sole Docker runtime
exception.

# 16. cleanup

Remove only:

```text
Task-owned disposable PostgreSQL container if created
external temporary verifier/config files
```

No broad cleanup.

# 17. final workspace

Before current Task movement:

```text
Git-visible:
48 exact

index:
empty

all 19 Cut A candidate bytes:
unchanged
```

Move current active Task byte-identically:

```text
.aiassistant/tasks/active/20260912_0125_aiscc-p2-3-private-s1-cut-a-verifier-harness-correction-and-full-proof-retry-1.md
→
.aiassistant/tasks/done/20260912_0125_aiscc-p2-3-private-s1-cut-a-verifier-harness-correction-and-full-proof-retry-1.md
```

Final:

```text
Git-visible:
49 exact

index:
empty
```

Exact final path set:

- `.aiassistant/records/aiscc/cycles/20260911_1935_aiscc-p2-3-a2-terminal-persisted-runtime-prerequisite-verification-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260911_2140_aiscc-p2-3-runtime-prerequisite-not-ready-provisioning-contract-audit-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260911_2148_aiscc-p2-3-provisioning-contract-partial-hold-image-build-authority-rework-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260911_2250_aiscc-p2-3-image-build-authority-inspect-evidence-rework-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260911_2300_aiscc-p2-3-base-image-inspect-replay-conflict-retry-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260912_0010_aiscc-p2-3-base-image-authority-reconciled-cut-a-implementation-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260912_0020_aiscc-p2-3-cut-a-static-failure-test-syntax-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260912_0100_aiscc-p2-3-cut-a-static-ruff-line-wrap-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260912_0120_aiscc-p2-3-cut-a-integration-fixture-runtime-root-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1935_aiscc-p2-3-a2-terminal-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/reports/aiscc/20260911_2140_aiscc-p2-3-runtime-prerequisite-verification-final-judgment-1.md`
- `.aiassistant/reports/aiscc/20260911_2148_aiscc-p2-3-provisioning-contract-audit-image-build-authority-gap-judgment-1.md`
- `.aiassistant/reports/aiscc/20260911_2250_aiscc-p2-3-image-build-authority-inspect-identity-inconsistency-judgment-1.md`
- `.aiassistant/reports/aiscc/20260911_2300_aiscc-p2-3-base-image-inspect-replay-conflict-judgment-1.md`
- `.aiassistant/reports/aiscc/20260912_0010_aiscc-p2-3-base-image-authority-reconciliation-final-acceptance-judgment-1.md`
- `.aiassistant/reports/aiscc/20260912_0020_aiscc-p2-3-cut-a-static-failure-test-syntax-judgment-1.md`
- `.aiassistant/reports/aiscc/20260912_0100_aiscc-p2-3-cut-a-static-ruff-line-length-failure-judgment-1.md`
- `.aiassistant/reports/aiscc/20260912_0120_aiscc-p2-3-cut-a-integration-fixture-runtime-root-collision-judgment-1.md`
- `.aiassistant/tasks/done/20260911_1935_aiscc-p2-3-actual-capture-runtime-prerequisite-verification-1.md`
- `.aiassistant/tasks/done/20260911_2140_aiscc-p2-3-private-s1-runtime-provisioning-contract-audit-1.md`
- `.aiassistant/tasks/done/20260911_2148_aiscc-p2-3-private-s1-image-build-input-authority-reconciliation-audit-1.md`
- `.aiassistant/tasks/done/20260911_2250_aiscc-p2-3-base-image-inspect-identity-reconciliation-audit-1.md`
- `.aiassistant/tasks/done/20260911_2300_aiscc-p2-3-base-image-inspect-identity-reconciliation-retry-after-replay-conflict-1.md`
- `.aiassistant/tasks/done/20260912_0010_aiscc-p2-3-private-s1-cut-a-image-provenance-and-docker-runner-source-implementation-1.md`
- `.aiassistant/tasks/done/20260912_0020_aiscc-p2-3-private-s1-cut-a-test-syntax-rework-and-full-proof-retry-1.md`
- `.aiassistant/tasks/done/20260912_0100_aiscc-p2-3-private-s1-cut-a-ruff-line-wrap-rework-and-full-proof-retry-1.md`
- `.aiassistant/tasks/done/20260912_0120_aiscc-p2-3-private-s1-cut-a-runtime-root-fixture-rework-and-full-proof-retry-1.md`
- `config/providers/stockroom-owner-profiles.v2.toml`
- `config/providers/stockroom-tools.v2.toml`
- `examples/synthetic-stockroom/.dockerignore`
- `examples/synthetic-stockroom/Dockerfile`
- `examples/synthetic-stockroom/IMAGE_PROVENANCE.md`
- `src/aiscc/bootstrap.py`
- `src/aiscc/providers/local_deterministic.py`
- `src/aiscc/providers/stockroom_tool.py`
- `src/aiscc/runtime/docker.py`
- `src/aiscc/runtime/stockroom_image.py`
- `src/aiscc/scenarios/composition.py`
- `src/aiscc/scenarios/stockroom_production.py`
- `tests/integration/scenarios/test_stockroom_binding.py`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`
- `tests/unit/providers/test_local_deterministic.py`
- `tests/unit/providers/test_stockroom_tool.py`
- `tests/unit/runtime/test_stockroom_docker_settlement.py`
- `tests/unit/runtime/test_stockroom_image.py`
- `tests/unit/scenarios/test_owner_composition.py`
- `.aiassistant/records/aiscc/cycles/20260912_0125_aiscc-p2-3-cut-a-static-verifier-defect-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0125_aiscc-p2-3-cut-a-static-verifier-harness-defect-judgment-1.md`
- `.aiassistant/tasks/done/20260912_0125_aiscc-p2-3-private-s1-cut-a-verifier-harness-correction-and-full-proof-retry-1.md`

# 18. failure semantics

Bootstrap failure:

```text
STOP / no report/export
```

After Task placement any mandatory failure:

```text
STOP_WITH_REPORT_EXPORT
```

No product/source repair in this Task.

A verifier-only defect may be reported as such, but do not change repository bytes to
work around it.

# 19. required export

Folder:

```text
.aiassistant/reports/target/20260912_0125_aiscc-p2-3-private-s1-cut-a-verifier-harness-correction-and-full-proof-retry-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
VERIFIER_HARNESS_VERIFICATION.md
STATIC_VERIFICATION.md
IMAGE_PROVENANCE_MODEL_VERIFICATION.md
V2_CONFIG_VERIFICATION.md
DOCKER_RUNNER_VERIFICATION.md
BUILD_CONTEXT_CONTRACT_VERIFICATION.md
PRODUCTION_BINDING_VERIFICATION.md
UNIT_VERIFICATION.md
POSTGRESQL_INTEGRATION_VERIFICATION.md
INTEGRATION_VERIFICATION.md
REGRESSION_VERIFICATION.md
CONTRACT_REVIEW.md
```

Also include byte-preserving:

```text
current Cycle
current Judgment
current done Task

all 19 Cut A implementation paths
```

Expected:

```text
16 root docs
3 canonical copies
19 implementation copies
38 members total
```

`EXPORT_MANIFEST.md` covers all 37 non-self entries.

Create adjacent verified ZIP:

```text
one top-level directory
38 exact members
CRC PASS
folder/archive byte equality
```

# 20. success ceiling

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

Cut B:
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
