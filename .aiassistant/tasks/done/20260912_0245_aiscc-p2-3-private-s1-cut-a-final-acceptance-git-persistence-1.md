# 작업지시서: P2-3 private S1 Cut A final acceptance Git persistence

## meta

- task_id: `20260912_0245_aiscc-p2-3-private-s1-cut-a-final-acceptance-git-persistence-1`
- created_at: `2026-09-12T02:45:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `FINAL_ACCEPTANCE_PERSISTENCE / STATE_RECONCILIATION`
- evidence_profile: `HIGH_RISK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `21bb0769c5db126c1989d9e0eb8e9f4c5ceade91`
- required_tree: `11b9d62db2d02649509f148aa01f8f74924c5792`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `accepted source implementation/proof → exact Git persistence and canonical state authority`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. Python / Git discipline

Do not assume bare `python`, `python3`, or `py`.

For any Python verification, use exact repository interpreter if available:

```text
.venv\Scripts\python.exe
```

Git writes are authorized only as explicitly stated in this Task.

No push.

No reset/restore/checkout/stash/clean.

# 1. purpose

Persist the Browser-accepted Cut A implementation candidate and its exact P2-3 governance
lineage, then reconcile the three canonical state records.

Do not alter Cut A product/config/test/example bytes.

Do not provision Cut B.

Do not execute private S1.

# 2. inbound transport

Verify Browser ZIP filename/SHA-256 from the Short Prompt.

Place current Task first:

```text
.aiassistant/tasks/active/20260912_0245_aiscc-p2-3-private-s1-cut-a-final-acceptance-git-persistence-1.md
```

Read fully and require the active Task is ignored.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260912_0245_aiscc-p2-3-cut-a-executable-proof-final-acceptance-persistence-entry-1.cycle.md
SHA-256:
5a295cc9e094941d15deb833a382a4dfe47a90bc094639af074e886620e95d2f

.aiassistant/reports/aiscc/20260912_0245_aiscc-p2-3-cut-a-source-implementation-final-acceptance-judgment-1.md
SHA-256:
252e523081c713dc279040f286cdd30f61be4641167d3d12281dd4386eb5975b
```

Bootstrap failure:

```text
STOP
no Git staging
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

Before this delivery exact Git-visible set is 55.

After current Cycle/Judgment placement while Task remains active:

```text
Git-visible:
57 exact

active Task:
exists byte-exact
ignored
```

Exact 57 paths:

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
- `.aiassistant/tasks/done/20260912_0020_aiscc-p2-3-private-s1-cut-a-test-syntax-rework-and-full-proof-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260912_0020_aiscc-p2-3-cut-a-static-failure-test-syntax-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0020_aiscc-p2-3-cut-a-static-failure-test-syntax-judgment-1.md`
- `.aiassistant/tasks/done/20260912_0100_aiscc-p2-3-private-s1-cut-a-ruff-line-wrap-rework-and-full-proof-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260912_0100_aiscc-p2-3-cut-a-static-ruff-line-wrap-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0100_aiscc-p2-3-cut-a-static-ruff-line-length-failure-judgment-1.md`
- `.aiassistant/tasks/done/20260912_0120_aiscc-p2-3-private-s1-cut-a-runtime-root-fixture-rework-and-full-proof-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260912_0120_aiscc-p2-3-cut-a-integration-fixture-runtime-root-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0120_aiscc-p2-3-cut-a-integration-fixture-runtime-root-collision-judgment-1.md`
- `.aiassistant/tasks/done/20260912_0125_aiscc-p2-3-private-s1-cut-a-verifier-harness-correction-and-full-proof-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260912_0125_aiscc-p2-3-cut-a-static-verifier-defect-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0125_aiscc-p2-3-cut-a-static-verifier-harness-defect-judgment-1.md`
- `.aiassistant/tasks/done/20260912_0135_aiscc-p2-3-private-s1-cut-a-materialized-fixture-root-rework-and-full-proof-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260912_0135_aiscc-p2-3-cut-a-materialized-fixture-root-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0135_aiscc-p2-3-cut-a-materialized-fixture-root-mismatch-judgment-1.md`
- `.aiassistant/tasks/done/20260912_0230_aiscc-p2-3-private-s1-cut-a-direct-pytest-full-proof-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260912_0230_aiscc-p2-3-cut-a-integration-launcher-defect-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0230_aiscc-p2-3-cut-a-integration-launcher-import-path-defect-judgment-1.md`
- `src/aiscc/bootstrap.py`
- `src/aiscc/providers/local_deterministic.py`
- `src/aiscc/providers/stockroom_tool.py`
- `src/aiscc/runtime/docker.py`
- `src/aiscc/runtime/stockroom_image.py`
- `src/aiscc/scenarios/composition.py`
- `src/aiscc/scenarios/stockroom_production.py`
- `config/providers/stockroom-owner-profiles.v2.toml`
- `config/providers/stockroom-tools.v2.toml`
- `examples/synthetic-stockroom/.dockerignore`
- `examples/synthetic-stockroom/Dockerfile`
- `examples/synthetic-stockroom/IMAGE_PROVENANCE.md`
- `tests/integration/scenarios/test_stockroom_binding.py`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`
- `tests/unit/providers/test_local_deterministic.py`
- `tests/unit/providers/test_stockroom_tool.py`
- `tests/unit/runtime/test_stockroom_docker_settlement.py`
- `tests/unit/runtime/test_stockroom_image.py`
- `tests/unit/scenarios/test_owner_composition.py`
- `.aiassistant/records/aiscc/cycles/20260912_0245_aiscc-p2-3-cut-a-executable-proof-final-acceptance-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260912_0245_aiscc-p2-3-cut-a-source-implementation-final-acceptance-judgment-1.md`

No extra/missing path.

# 4. exact existing governance integrity

Require these 36 current tracked governance files exact:

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
- `.aiassistant/tasks/done/20260911_2300_aiscc-p2-3-base-image-inspect-identity-reconciliation-retry-after-replay-conflict-1.md`  `a74d04121dd4627820dcc32d89885b9fc05b29d0d2f378ce888462feac4da3f4`
- `.aiassistant/records/aiscc/cycles/20260911_2300_aiscc-p2-3-base-image-inspect-replay-conflict-retry-entry-1.cycle.md`  `50e19fcca5e99741174753c2a318844f23813bf4f7f866e17c513c8e4b6efbef`
- `.aiassistant/reports/aiscc/20260911_2300_aiscc-p2-3-base-image-inspect-replay-conflict-judgment-1.md`  `b4b4f1f5870ef2d456725599a4e06bbbe0409fd3cc019b1322114707e5cf537d`
- `.aiassistant/tasks/done/20260912_0010_aiscc-p2-3-private-s1-cut-a-image-provenance-and-docker-runner-source-implementation-1.md`  `8001e6e397605e6b3ddd7a241c370c3ab1a1b653f0232177eaa17aefb31db263`
- `.aiassistant/records/aiscc/cycles/20260912_0010_aiscc-p2-3-base-image-authority-reconciled-cut-a-implementation-entry-1.cycle.md`  `420ad30fe70216079081a337aaea11005de672c4c8383ee1f7c2c7d2b9621108`
- `.aiassistant/reports/aiscc/20260912_0010_aiscc-p2-3-base-image-authority-reconciliation-final-acceptance-judgment-1.md`  `544736710f005c3f723731d23143047af9e0e73b90eab87f81d3e62f17c003cb`
- `.aiassistant/tasks/done/20260912_0020_aiscc-p2-3-private-s1-cut-a-test-syntax-rework-and-full-proof-retry-1.md`  `e2e224f3781387b6162f371dfbe260bcfece345a5fca721ca1e75498cf9f9e07`
- `.aiassistant/records/aiscc/cycles/20260912_0020_aiscc-p2-3-cut-a-static-failure-test-syntax-rework-proof-retry-entry-1.cycle.md`  `7e8b110761500e12610844457228d24875a020db4c25652a0a22e7a09fa30383`
- `.aiassistant/reports/aiscc/20260912_0020_aiscc-p2-3-cut-a-static-failure-test-syntax-judgment-1.md`  `42d40602833c41d196265e71df34b487ec7c44f8451246fd3b95544bcf0cba8b`
- `.aiassistant/tasks/done/20260912_0100_aiscc-p2-3-private-s1-cut-a-ruff-line-wrap-rework-and-full-proof-retry-1.md`  `51257ae258b8682cede5d362c0976c71dac5845f6f9d9c9f9464a753d1a53355`
- `.aiassistant/records/aiscc/cycles/20260912_0100_aiscc-p2-3-cut-a-static-ruff-line-wrap-rework-proof-retry-entry-1.cycle.md`  `8fb3f90cc5adc4de6cda947c74e2a8df3f0a97fe9f5330a8332ef7552313efaa`
- `.aiassistant/reports/aiscc/20260912_0100_aiscc-p2-3-cut-a-static-ruff-line-length-failure-judgment-1.md`  `e4b0b2bfeba2ab9bf99514339028539f602cafdf1ca5c0789a8ef50bd67cc14e`
- `.aiassistant/tasks/done/20260912_0120_aiscc-p2-3-private-s1-cut-a-runtime-root-fixture-rework-and-full-proof-retry-1.md`  `2290d7d1605efacd719697b767a13f3eb1a211762c5e7c974af50af94178286c`
- `.aiassistant/records/aiscc/cycles/20260912_0120_aiscc-p2-3-cut-a-integration-fixture-runtime-root-rework-proof-retry-entry-1.cycle.md`  `21ac547967a4f1053bd91b743d747ca2415eaa81224386ca63b58ca4c4af5ae4`
- `.aiassistant/reports/aiscc/20260912_0120_aiscc-p2-3-cut-a-integration-fixture-runtime-root-collision-judgment-1.md`  `bf8c7f5b016245fcbdc0463673d84afd44c9742b441bfc4d76ffbfd19438bdf5`
- `.aiassistant/tasks/done/20260912_0125_aiscc-p2-3-private-s1-cut-a-verifier-harness-correction-and-full-proof-retry-1.md`  `8fbb9029c7d2cccf313360cdb5e8c716ca04871403433cd9db32354c1de72dbb`
- `.aiassistant/records/aiscc/cycles/20260912_0125_aiscc-p2-3-cut-a-static-verifier-defect-proof-retry-entry-1.cycle.md`  `f2d8615ae1ad4c96ce22c0f2b4dbed7c3fc83f1cb63675d29c971f028ddfc8ab`
- `.aiassistant/reports/aiscc/20260912_0125_aiscc-p2-3-cut-a-static-verifier-harness-defect-judgment-1.md`  `3875aae0d1e8dc684da7d34f59f6039e93e17ed258027856d160805154045b29`
- `.aiassistant/tasks/done/20260912_0135_aiscc-p2-3-private-s1-cut-a-materialized-fixture-root-rework-and-full-proof-retry-1.md`  `e117aa7533ce3d287527254efb2309763de1ed73aac736211c7041debcab8c28`
- `.aiassistant/records/aiscc/cycles/20260912_0135_aiscc-p2-3-cut-a-materialized-fixture-root-rework-proof-retry-entry-1.cycle.md`  `38270df63036b9a443bf5f00bcc627514b77bc448d6531de55eccf18af1b5424`
- `.aiassistant/reports/aiscc/20260912_0135_aiscc-p2-3-cut-a-materialized-fixture-root-mismatch-judgment-1.md`  `2b5185af191929ff517518bc599332fe7f848189021394fdc6734ad18d71efdd`
- `.aiassistant/tasks/done/20260912_0230_aiscc-p2-3-private-s1-cut-a-direct-pytest-full-proof-retry-1.md`  `b3de72d487ec639102d46bf1ad4d13cae78e5e613264efacca3f5a594ee09611`
- `.aiassistant/records/aiscc/cycles/20260912_0230_aiscc-p2-3-cut-a-integration-launcher-defect-proof-retry-entry-1.cycle.md`  `2c167dcd9a9f83063601d7a51e32600cb39e8e0847414fefdcf0b5aa9ba35d8c`
- `.aiassistant/reports/aiscc/20260912_0230_aiscc-p2-3-cut-a-integration-launcher-import-path-defect-judgment-1.md`  `9b8ec8ced5192f9db5036d64e514941a98a3439aa5193eca055d930abcbd2224`

Require current acceptance artifacts exact:

```text
.aiassistant/records/aiscc/cycles/20260912_0245_aiscc-p2-3-cut-a-executable-proof-final-acceptance-persistence-entry-1.cycle.md
5a295cc9e094941d15deb833a382a4dfe47a90bc094639af074e886620e95d2f

.aiassistant/reports/aiscc/20260912_0245_aiscc-p2-3-cut-a-source-implementation-final-acceptance-judgment-1.md
252e523081c713dc279040f286cdd30f61be4641167d3d12281dd4386eb5975b
```

Any mismatch:

```text
GOVERNANCE_IDENTITY_MISMATCH
→ STOP_WITH_REPORT_EXPORT
```

# 5. exact Cut A candidate integrity

Require these 19 paths exact and do not modify them:

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
CUT_A_ACCEPTED_CANDIDATE_MISMATCH
→ STOP_WITH_REPORT_EXPORT
```

# 6. pre-state identity

Before any state edit require:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `79cb3adc915928faba18b728bd671625d29a77e3948973555666bc83445a1047`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `9e3562322b4f8e8910f3e59463c77a975cd91531cf3b02e0a640b4b1a80b6206`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `2c0143e1c7177ac92f5d7934e3adc322fc0260191e17601d6a646d5fcfd85f94`

The three state files must be clean against required HEAD before Commit A.

# 7. no runtime / product mutation

Forbidden:

```text
source/config/test/example mutation
Docker build/pull/run/inspect for Stockroom
persistent DB provisioning
actual S1-S4
Replay
network/registry access
migration creation/change
Project Source mirror update
git push
```

No new product/config/test/example path.

# 8. Commit A staging contract

Commit A persists exactly the accepted candidate and accepted/rework provenance already
present before this persistence Task.

Stage exactly the 57 paths from section 3.

The current active persistence Task is ignored and MUST NOT be staged in Commit A.

Require:

```text
git diff --cached --name-only:
57 exact

git diff --cached --check:
PASS
```

No other staged path.

Before commit, re-hash the 19 candidate paths and all section-4 governance artifacts.

Commit message exactly:

```text
feat(orchestration): persist P2-3 private S1 Cut A runtime authority
```

Create Commit A.

Require:

```text
Commit A parent:
21bb0769c5db126c1989d9e0eb8e9f4c5ceade91

Commit A changed-path count:
57 exact

Commit A changed-path set:
section 3 exact

Commit A tree contains every 19 Cut A path at section-5 SHA-256
```

Record:

```text
COMMIT_A
COMMIT_A_TREE
COMMIT_A_PARENT
```

# 9. post-Commit-A gate

After Commit A require:

```text
branch:
main

HEAD:
COMMIT_A

index:
empty

product/config/test/example worktree:
clean

current active persistence Task:
still ignored
```

Only the three canonical state files may be edited next.

# 10. canonical state reconciliation

Modify exactly:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
```

No other path.

## CURRENT_STATE_SUMMARY

Record at minimum:

```text
P2-3:
IN_PROGRESS

Cut A image provenance / Docker settlement source implementation:
ACCEPTED / PERSISTED

Cut A Commit A:
<actual COMMIT_A>

Cut A executable proof:
static PASS
unit 246 PASS
focused integration 1 PASS
full integration 9 PASS
regression 110 PASS
contract 32/32 PASS

Cut B environment provisioning:
NOT_STARTED / AUTHORIZATION_PENDING_BROWSER_AFTER_PERSISTENCE

canonical image provenance:
NOT_ISSUED

persistent capture DB:
NOT_PROVISIONED

private S1:
NOT_EXECUTED

public replay/live:
NOT_RELEASED
```

Do not claim Cut B or S1 readiness beyond this.

## NEXT_ACTIONS

Keep stable roadmap semantics.

Set the current P2-3 priority to:

```text
work_type:
ENVIRONMENT_PROVISIONING

title:
P2-3 private S1 Cut B environment provisioning

reason:
Cut A source authority is accepted/persisted; actual image/provenance/DB/runtime-root
environment is still absent.

blocker:
Cut B exact Browser Task required before provisioning.

forbidden:
actual private S1 until final readiness judgment.
```

Do not reorder unrelated long-term roadmap items unless required to keep this current
priority truthful.

## DECISION_REGISTER

Append one decision entry:

```text
decision_id:
AISCC-P2-3-PRIVATE-S1-CUT-A-IMAGE-PROVENANCE-DOCKER-RUNNER-V1

decision:
Accept and persist the 19-path Cut A source/config/test implementation.

status:
HUMAN_PROVIDED / ACCEPTED / PERSISTED

implementation commit:
<actual COMMIT_A>

base:
21bb0769c5db126c1989d9e0eb8e9f4c5ceade91

accepted source contract:
typed provenance authority
V2 static policy/provenance ref
source-owned Docker settlement runner
production provenance binding
historical Git-object build-context contract

proof:
compile 14/14
Ruff 0
loaders 4/4
negative loader 9/9
unit 246
focused integration 1
full integration 9
regression 110
contract 32/32

non-claim:
no actual image build/runtime
no canonical provenance issuance
no persistent capture DB
no actual S1
```

Preserve all prior decisions.

# 11. state static gate

Require:

```text
only 3 state files modified
index empty
UTF-8 valid
control-character check PASS
Markdown fence balance PASS
git diff --check PASS
```

Require all 19 Cut A candidate hashes still exact.

# 12. prepare report/export before final provenance commit

Prepare the target report/export content for this Task with all evidence available
through Commit A and state reconciliation.

The target directory remains ignored.

It is acceptable for the ignored report/export to receive its final Commit B hash
after Commit B; this does not alter tracked product/state authority.

# 13. move current Task to done

After Commit A is verified, the 3 state edits pass section 11, and report/export source
material is otherwise complete, move current Task byte-identically:

```text
.aiassistant/tasks/active/20260912_0245_aiscc-p2-3-private-s1-cut-a-final-acceptance-git-persistence-1.md
→
.aiassistant/tasks/done/20260912_0245_aiscc-p2-3-private-s1-cut-a-final-acceptance-git-persistence-1.md
```

Require:

```text
active absent
done exists
done bytes == Browser-issued Task
done is Git-visible
```

At this point only four tracked paths may be unstaged:

```text
.aiassistant/tasks/done/20260912_0245_aiscc-p2-3-private-s1-cut-a-final-acceptance-git-persistence-1.md
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
```

# 14. Commit B staging contract

Stage exactly those four paths.

Require:

```text
git diff --cached --name-only:
4 exact

git diff --cached --check:
PASS
```

Commit message exactly:

```text
docs(command-center): reconcile P2-3 Cut A persistence state
```

Create Commit B.

Require:

```text
Commit B parent:
COMMIT_A

Commit B changed-path count:
4 exact

Commit B changed-path set:
current done Task + 3 state records
```

Record:

```text
COMMIT_B
COMMIT_B_TREE
COMMIT_B_PARENT
```

# 15. final Git gate

Require:

```text
branch:
main

HEAD:
COMMIT_B

HEAD^:
COMMIT_A

COMMIT_A^:
21bb0769c5db126c1989d9e0eb8e9f4c5ceade91

index:
empty

git status --porcelain --untracked-files=all:
empty except ignored reports/target artifacts

tracked worktree:
clean
```

Do not push.

Verify:

```text
git show --format=fuller --stat COMMIT_A
git show --format=fuller --stat COMMIT_B
git diff-tree --no-commit-id --name-only -r COMMIT_A
git diff-tree --no-commit-id --name-only -r COMMIT_B
```

Commit A must still contain the 19 accepted candidate bytes at exact section-5 hashes.

# 16. persistence contract review

Require all PASS:

```text
BASE_HEAD_EXACT
PRE_PERSIST_57_PATH_SET_EXACT
36_PREDECESSOR_GOVERNANCE_HASHES_EXACT
CURRENT_ACCEPTANCE_CYCLE_JUDGMENT_EXACT
19_CUT_A_HASHES_EXACT
PRE_STATE_3_HASHES_EXACT
COMMIT_A_PARENT_EXACT
COMMIT_A_57_PATHS_EXACT
COMMIT_A_19_CANDIDATE_BYTES_EXACT
NO_PRODUCT_CHANGE_DURING_PERSISTENCE
STATE_ONLY_3_PATH_MUTATION
TASK_DONE_BYTE_EXACT
COMMIT_B_PARENT_COMMIT_A
COMMIT_B_4_PATHS_EXACT
FINAL_INDEX_EMPTY
FINAL_TRACKED_WORKTREE_CLEAN
NO_PUSH
NO_CUT_B_PROVISIONING
NO_ACTUAL_S1
```

Require:

```text
19 / 19 PASS
```

# 17. required export

Folder:

```text
.aiassistant/reports/target/20260912_0245_aiscc-p2-3-private-s1-cut-a-final-acceptance-git-persistence-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
CUT_A_ACCEPTANCE_VERIFICATION.md
GIT_PERSISTENCE_VERIFICATION.md
STATE_RECONCILIATION_VERIFICATION.md
COMMIT_GRAPH_VERIFICATION.md
COMMIT_A_PATHS.md
COMMIT_B_PATHS.md
CONTRACT_REVIEW.md
```

Also include byte-preserving:

```text
current Cycle
current Judgment
current done Task

final:
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
```

Expected:

```text
11 root docs
3 canonical copies
3 final state copies
17 members total
```

`EXPORT_MANIFEST.md` covers all 16 non-self entries with byte size and SHA-256.

Create adjacent ZIP:

```text
one top-level directory
17 exact members
CRC PASS
folder/archive byte equality
```

After Commit B, finalize ignored report/export with actual Commit B metadata and verify
the ZIP again.

# 18. success ceiling

Success:

```text
Cut A source implementation:
ACCEPTED / PERSISTED

Cut A executable proof:
ACCEPTED

canonical state:
RECONCILED

Cut B:
NOT_EXECUTED

canonical image provenance:
NOT_ISSUED

persistent capture DB:
NOT_PROVISIONED

private S1:
NOT_EXECUTED

push:
NOT_AUTHORIZED

P2-3:
IN_PROGRESS
```
