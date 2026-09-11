# 작업지시서: P2-3 private S1 Cut A test syntax rework + full proof retry

## meta

- task_id: `20260912_0020_aiscc-p2-3-private-s1-cut-a-test-syntax-rework-and-full-proof-retry-1`
- created_at: `2026-09-12T00:20:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `TEST_SYNTAX_REWORK / FULL_CUT_A_PROOF_RETRY`
- evidence_profile: `HIGH_RISK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `21bb0769c5db126c1989d9e0eb8e9f4c5ceade91`
- required_tree: `11b9d62db2d02649509f148aa01f8f74924c5792`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. purpose

Continue the current Cut A draft.

Correct exactly two invalid decorator terminators in:

```text
tests/unit/runtime/test_stockroom_image.py
```

Then run the full previously blocked Cut A proof.

Do not redesign the implementation.

# 1. inbound transport

Verify Browser ZIP filename/SHA-256 from the Short Prompt.

Place current Task first:

```text
.aiassistant/tasks/active/20260912_0020_aiscc-p2-3-private-s1-cut-a-test-syntax-rework-and-full-proof-retry-1.md
```

Read fully; require it is ignored by canonical Git policy.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260912_0020_aiscc-p2-3-cut-a-static-failure-test-syntax-rework-proof-retry-entry-1.cycle.md
SHA-256:
7e8b110761500e12610844457228d24875a020db4c25652a0a22e7a09fa30383

.aiassistant/reports/aiscc/20260912_0020_aiscc-p2-3-cut-a-static-failure-test-syntax-judgment-1.md
SHA-256:
42d40602833c41d196265e71df34b487ec7c44f8451246fd3b95544bcf0cba8b
```

Bootstrap failure before Task placement:

```text
STOP
no product mutation
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

Before this delivery exact Git-visible set is 37:

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
- `.aiassistant/tasks/done/20260912_0010_aiscc-p2-3-private-s1-cut-a-image-provenance-and-docker-runner-source-implementation-1.md`
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

After current Cycle/Judgment placement while current Task is active:

```text
Git-visible:
39 exact

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
- `.aiassistant/tasks/done/20260912_0010_aiscc-p2-3-private-s1-cut-a-image-provenance-and-docker-runner-source-implementation-1.md`
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
- `.aiassistant/records/aiscc/cycles/20260912_0020_aiscc-p2-3-cut-a-static-failure-test-syntax-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0020_aiscc-p2-3-cut-a-static-failure-test-syntax-judgment-1.md`

No extra/missing path.

# 3. exact candidate identity before mutation

Require exact 0010 governance:

- `.aiassistant/tasks/done/20260912_0010_aiscc-p2-3-private-s1-cut-a-image-provenance-and-docker-runner-source-implementation-1.md`  `8001e6e397605e6b3ddd7a241c370c3ab1a1b653f0232177eaa17aefb31db263`
- `.aiassistant/records/aiscc/cycles/20260912_0010_aiscc-p2-3-base-image-authority-reconciled-cut-a-implementation-entry-1.cycle.md`  `420ad30fe70216079081a337aaea11005de672c4c8383ee1f7c2c7d2b9621108`
- `.aiassistant/reports/aiscc/20260912_0010_aiscc-p2-3-base-image-authority-reconciliation-final-acceptance-judgment-1.md`  `544736710f005c3f723731d23143047af9e0e73b90eab87f81d3e62f17c003cb`

Require exact 19-path current draft:

- `src/aiscc/bootstrap.py`  `745b58da26ec300286ed69d1a7477b21afeb7625ec43e7f422560a657bc1c115`
- `src/aiscc/runtime/docker.py`  `7a13158f528679220a282c3b3c19cb853ee2fc2bebbe49817d0fb34c394b0575`
- `src/aiscc/providers/stockroom_tool.py`  `15d8cdbf621a2357c4e317188c41cf62c47b6c02def04e3c33bc50f28f121b78`
- `src/aiscc/providers/local_deterministic.py`  `92ec8ba5553b05fe55fdbac30ab2dde8f57597c1055060a2f786dadd47f1c21a`
- `src/aiscc/scenarios/composition.py`  `10b3b7a4f3c9d62f7674c4b9bf884357300bc7c0fdf284c2689474e80fb31990`
- `src/aiscc/scenarios/stockroom_production.py`  `685e2ec549473e167ed1fe4d7de1050d7a53a449d1d278dcdb3439a471478f1f`
- `tests/unit/runtime/test_stockroom_docker_settlement.py`  `f7a33975072737417b3a922d4acd44e59be29547ceb87c864e24647d46236b19`
- `tests/unit/providers/test_stockroom_tool.py`  `e33b966cf5d575b7e55cd1ced2f3bfcd805833c08c1c66d6c650b693313c285d`
- `tests/unit/providers/test_local_deterministic.py`  `daa58e09dd3e81f2ba4a6edad236685c34a7c63852419ad3188aef51c8fe6209`
- `tests/unit/scenarios/test_owner_composition.py`  `bfbae533d8453bef3940b1b652c5688b3b375b7e0fa40ae03e3196902888d652`
- `tests/integration/scenarios/test_stockroom_binding.py`  `78bc1a342e2d5254d5dca7d93b4c6a7295873c97fa94d05bb44f31df87c074ee`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`  `68fda7c133d134c076e184c2c7b9117a33f5477468647e8098dbae109a7c0d51`
- `src/aiscc/runtime/stockroom_image.py`  `639ddfc6295e45334d204e3b0e5c6d8ae01a5549385fb287600a382f0a32041b`
- `config/providers/stockroom-tools.v2.toml`  `16015a97a00098e26f89a2972c87fd5ce0f4516c1afdf2bc20126fe6d1c61385`
- `config/providers/stockroom-owner-profiles.v2.toml`  `3f20d2d1ac4dd45709c47fc6572db4b97d6c33e0bebf02c6fd489dd9adbd022a`
- `examples/synthetic-stockroom/Dockerfile`  `94f71d8bf4b2f87e678e1a379dead19b7a850cf4522ec835bf6455f95d72b27a`
- `examples/synthetic-stockroom/.dockerignore`  `99637a64da3b1b13bbf9a52459098d07bbc865aca11d004c89c3ee48965849f9`
- `examples/synthetic-stockroom/IMAGE_PROVENANCE.md`  `166cfec29db4f46477b0117fae85a6a937343e3fb019a9b668b223b2eea8bae3`
- `tests/unit/runtime/test_stockroom_image.py`  `049e7a9ebd22c2abd6f55cd2fa7db6816c96fc3005ccd99667ee3ae3b40b10e6`

Any mismatch:

```text
CUT_A_DRAFT_IDENTITY_MISMATCH
→ STOP_WITH_REPORT_EXPORT
```

# 4. exact mutation authority

Only:

```text
tests/unit/runtime/test_stockroom_image.py
```

may change.

All other 18 Cut A paths are frozen byte-exact to section 3.

No new source/config/test/example path.

Any need to change another path:

```text
SCOPE_EXPANSION_REQUIRED
→ STOP_WITH_REPORT_EXPORT
```

# 5. exact syntax repair

Before edit require:

```text
tests/unit/runtime/test_stockroom_image.py
SHA-256:
049e7a9ebd22c2abd6f55cd2fa7db6816c96fc3005ccd99667ee3ae3b40b10e6

byte size:
8108
```

Perform only these two textual corrections:

```text
decorator starting near line 90:
@ pytest.mark.parametrize(... [
...
]):
->
@ pytest.mark.parametrize(... [
...
])

decorator starting near line 107:
@ pytest.mark.parametrize(... [
...
]):
->
@ pytest.mark.parametrize(... [
...
])
```

The actual source spelling is `@pytest.mark.parametrize`, with no inserted whitespace;
the notation above only highlights the decorator.

No test parameter, assertion, name, fixture, import or behavior may otherwise change.

After edit require exactly:

```text
byte size:
8106

SHA-256:
b23f72014cb819530656f79f98818fd968eb8f6e3498ad7246b334953f50bc2c
```

If exact post-fix identity differs:

```text
SYNTAX_REWORK_IDENTITY_MISMATCH
→ STOP_WITH_REPORT_EXPORT
```

# 6. static verifier

Do not run `py_compile`.

Use one external temporary verifier outside the repository.

Compile in memory these exact 14 Python paths:

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

# 7. Ruff must be read-only

Run Ruff on the same 14 Python paths.

Forbidden:

```text
--fix
--unsafe-fixes
ruff format
any formatter mutation
```

Require:

```text
Ruff:
14 / 14 PASS
```

If Ruff fails:

```text
STATIC_CHECK_FAILURE
→ STOP_WITH_REPORT_EXPORT
```

Do not repair it in the same turn.

# 8. strict configuration proof

Through production loaders, strict-load:

```text
config/providers/stockroom-tools.v1.toml
config/providers/stockroom-tools.v2.toml
config/providers/stockroom-owner-profiles.v1.toml
config/providers/stockroom-owner-profiles.v2.toml
```

Require:

```text
4 / 4 PASS
```

Also prove:

```text
v1 semantic identity preserved
v2 image key denied
v2 future image ID absent
mixed/unknown schema denied
source aggregate cannot enter image identity
```

# 9. static workspace gate

Require:

```text
git diff --check:
PASS

index:
empty

repo-visible .pyc introduced by retry:
0

all frozen 18 Cut A paths:
exact section-3 SHA unchanged

only current retry mutation:
tests/unit/runtime/test_stockroom_image.py
```

Any failure:

```text
STATIC_CHECK_FAILURE
→ STOP_WITH_REPORT_EXPORT
```

No same-turn source repair.

# 10. targeted unit proof

Use exact repository interpreter with `-B` and no pytest cache.

Run:

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

No real Docker subprocess.

Mandatory failure:

```text
TEST_FAILURE
→ STOP_WITH_REPORT_EXPORT
```

No same-turn repair.

# 11. required unit semantics

Executable unit proof must cover at least:

```text
strict provenance schema
canonical fingerprint
whole-file SHA binding
typed provenance ref
issuance-ref drift denial
source/build/base-policy drift denial
future image-ID syntax strictness
tag-only denial
source aggregate as image denial
raw object not admitted
missing canonical provenance fail-closed
v1/v2 tool config compatibility
v1/v2 owner profile compatibility
production-v2 composition fingerprint binds provenance
runner exact inspect-before-create
label/projection drift denial
argv/shell safety
bounded stdout/stderr
timeout settlement
cancel settlement
create/start/inspect/remove uncertainty
owner reconciliation
unknown outcome quarantine
no blind redispatch
```

# 12. disposable PostgreSQL prerequisite

Only after static + unit PASS, a Task-owned disposable PostgreSQL test container is
authorized:

```text
postgres:17.6-alpine
--pull=never
loopback only
temporary storage
unique Task-owned name
```

No named persistent capture volume.

Migrate to:

```text
20260901_0008
```

Remove only that exact Task-owned container after tests.

This is test infrastructure, not Cut B.

# 13. integration proof

Run:

```text
tests/integration/scenarios/test_stockroom_binding.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Require all collected PASS / zero skip.

No actual Stockroom image/process/provider/tool execution.

Test-only provenance fixtures must pass through the same parser/admission logic but
must not be usable as production Browser-issued provenance.

# 14. regression proof

Run:

```text
tests/unit/scenarios/test_stockroom_capture_runner.py
tests/unit/security/test_stockroom_policy.py
tests/integration/evidence/test_postgres_evidence_admission.py
tests/integration/human/test_postgres_human_gate_judgment.py
tests/integration/workflow/test_postgres_kernel.py
```

Require all collected PASS / zero skip.

# 15. forbidden runtime actions

Do not execute:

```text
docker image inspect for Stockroom
docker pull
docker build/buildx
docker create/run for Stockroom
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

The section-12 disposable PostgreSQL test container is the only Docker runtime
exception.

# 16. 32/32 contract review

Require:

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

# 17. cleanup

Remove only:

```text
Task-owned disposable PostgreSQL container
external temporary static verifier files
```

No broad cleanup.

# 18. final workspace

Before current Task movement:

```text
Git-visible:
39 exact
index empty
```

After successful proof the same 19 Cut A paths remain Git-visible; only the authorized
test file has new bytes.

Move current active Task byte-identically:

```text
.aiassistant/tasks/active/20260912_0020_aiscc-p2-3-private-s1-cut-a-test-syntax-rework-and-full-proof-retry-1.md
→
.aiassistant/tasks/done/20260912_0020_aiscc-p2-3-private-s1-cut-a-test-syntax-rework-and-full-proof-retry-1.md
```

Final:

```text
Git-visible:
40 exact
index empty
```

Exact final path set:

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
- `.aiassistant/tasks/done/20260912_0010_aiscc-p2-3-private-s1-cut-a-image-provenance-and-docker-runner-source-implementation-1.md`
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
- `.aiassistant/records/aiscc/cycles/20260912_0020_aiscc-p2-3-cut-a-static-failure-test-syntax-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0020_aiscc-p2-3-cut-a-static-failure-test-syntax-judgment-1.md`
- `.aiassistant/tasks/done/20260912_0020_aiscc-p2-3-private-s1-cut-a-test-syntax-rework-and-full-proof-retry-1.md`

# 19. failure semantics

Bootstrap failure:

```text
STOP / no report/export
```

After Task placement any mandatory static/test/workspace failure:

```text
STOP_WITH_REPORT_EXPORT
```

No same-turn source repair after the mandatory gate.

# 20. required export

Folder:

```text
.aiassistant/reports/target/20260912_0020_aiscc-p2-3-private-s1-cut-a-test-syntax-rework-and-full-proof-retry-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
SYNTAX_REWORK_VERIFICATION.md
STATIC_VERIFICATION.md
IMAGE_PROVENANCE_MODEL_VERIFICATION.md
V2_CONFIG_VERIFICATION.md
DOCKER_RUNNER_VERIFICATION.md
BUILD_CONTEXT_CONTRACT_VERIFICATION.md
PRODUCTION_BINDING_VERIFICATION.md
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

all 19 Cut A implementation paths
```

Expected:

```text
15 root docs
3 canonical copies
19 implementation copies
37 members total
```

`EXPORT_MANIFEST.md` covers all 36 non-self entries.

Create adjacent verified ZIP:

```text
one top-level directory
37 exact members
CRC PASS
folder/archive byte equality
```

# 21. success ceiling

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
