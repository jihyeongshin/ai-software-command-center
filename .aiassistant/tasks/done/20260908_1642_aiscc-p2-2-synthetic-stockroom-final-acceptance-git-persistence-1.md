# 작업지시서: P2-2 Synthetic Stockroom final acceptance Git persistence

## meta

- task_id: `20260908_1642_aiscc-p2-2-synthetic-stockroom-final-acceptance-git-persistence-1`
- created_at: `2026-09-08T16:42:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `QA_ONLY / FINAL_ACCEPTANCE_PERSISTENCE`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P2-2 accepted Synthetic Stockroom candidate exact Git persistence`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `187880eff48cbf2909e0fcadce75c6d2cb30ab31`
- required_base_tree: `1823346f7ec7c4da466d64f6823f0c8b3390f0cd`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `accepted source implementation → exact staging/commit authority boundary`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# current state

```text
P2-2 source/contract audit:
ACCEPTED

P2-2 implementation:
ACCEPTED_CANDIDATE

P2-2 Git persistence:
NOT_COMPLETED

P2-2:
ACTIVE / NOT_CLOSED

P2-3:
NOT_STARTED
```

# Human-owned IDE session prerequisite

This Task must start in a Human-created fresh IDE Executor chat.

Executor must not create/open a new chat or infer that a model change inside an existing conversation satisfies this prerequisite.

# goal

1. Transport current TASK/CYCLE/JUDGMENT exactly.
2. Verify repository authority and exact pending workspace.
3. Verify all 18 pending governance artifact hashes.
4. Verify all 14 accepted Synthetic Stockroom source hashes.
5. Verify no generated candidate residue exists.
6. Reuse accepted implementation/test/build/CLI evidence only if exact identity remains unchanged.
7. Move this Task active→done.
8. Stage and commit exact 35 paths only.
9. Verify commit parent/tree/message/path/blob/worktree provenance.
10. Submit P2-2 terminal-closure readiness to Browser Command Center.
11. Do not start P2-3.

# non-goals

- source modification
- test modification
- rerun Human QA
- full AISCC test suite
- scenario enrollment
- public release
- license decision
- P2-3 implementation
- Git push

# must-read after transport

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md

.aiassistant/records/aiscc/cycles/20260908_1642_aiscc-p2-2-synthetic-stockroom-implementation-accepted-persistence-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_1642_aiscc-p2-2-synthetic-stockroom-implementation-final-acceptance-judgment-1.md

.aiassistant/tasks/done/20260908_1602_aiscc-p2-2-synthetic-stockroom-candidate-implementation-transport-retry-1.md
```

Read the predecessor implementation verification bundle only as narrowly necessary to confirm accepted evidence identity. Do not rerun unrelated discovery.

# initial repository gate

After current package transport:

```text
branch:
main

HEAD:
187880eff48cbf2909e0fcadce75c6d2cb30ab31

HEAD tree:
1823346f7ec7c4da466d64f6823f0c8b3390f0cd

index:
empty
```

Expected Git-visible set is exact **34 paths**:

- existing accepted pending set: 32
- current Cycle: 1
- current Judgment: 1

Current active Task is ignored.

Exact expected 34 paths:

- `.aiassistant/records/aiscc/cycles/20260908_1443_aiscc-command-center-workflow-correction-final-acceptance-p2-2-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1443_aiscc-command-center-workflow-correction-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260908_1512_aiscc-p2-2-synthetic-demo-repository-source-contract-audit-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_1512_aiscc-p2-2-source-contract-audit-blocked-transport-stop-and-fresh-session-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1512_aiscc-p2-2-source-contract-audit-transport-stop-violation-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_1519_aiscc-p2-2-audit-blocked-transport-tool-policy-recovery-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1519_aiscc-p2-2-audit-transport-tool-policy-blocked-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_1528_aiscc-p2-2-audit-blocked-command-center-dirt-contract-correction-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1528_aiscc-p2-2-audit-command-center-dirt-contract-correction-judgment-1.md`
- `.aiassistant/tasks/done/20260908_1443_aiscc-p2-2-synthetic-demo-repository-source-contract-audit-1.md`
- `.aiassistant/tasks/done/20260908_1519_aiscc-p2-2-transport-policy-compatible-source-contract-audit-retry-1.md`
- `.aiassistant/tasks/done/20260908_1528_aiscc-p2-2-source-contract-audit-provenance-reconciliation-retry-1.md`
- `.aiassistant/tasks/done/20260908_1549_aiscc-p2-2-synthetic-stockroom-candidate-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_1549_aiscc-p2-2-source-contract-audit-final-acceptance-implementation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1549_aiscc-p2-2-source-contract-audit-final-acceptance-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_1602_aiscc-p2-2-implementation-blocked-transport-prompt-regression-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1602_aiscc-p2-2-implementation-transport-prompt-regression-judgment-1.md`
- `.aiassistant/tasks/done/20260908_1602_aiscc-p2-2-synthetic-stockroom-candidate-implementation-transport-retry-1.md`
- `examples/synthetic-stockroom/.gitignore`
- `examples/synthetic-stockroom/.python-version`
- `examples/synthetic-stockroom/PROVENANCE.md`
- `examples/synthetic-stockroom/README.md`
- `examples/synthetic-stockroom/stockroom/__init__.py`
- `examples/synthetic-stockroom/stockroom/__main__.py`
- `examples/synthetic-stockroom/stockroom/cli.py`
- `examples/synthetic-stockroom/stockroom/data/catalog.json`
- `examples/synthetic-stockroom/stockroom/inventory.py`
- `examples/synthetic-stockroom/stockroom/model.py`
- `examples/synthetic-stockroom/tests/test_cli.py`
- `examples/synthetic-stockroom/tests/test_contract.py`
- `examples/synthetic-stockroom/tests/test_inventory.py`
- `examples/synthetic-stockroom/tools/build.py`
- `.aiassistant/records/aiscc/cycles/20260908_1642_aiscc-p2-2-synthetic-stockroom-implementation-accepted-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1642_aiscc-p2-2-synthetic-stockroom-implementation-final-acceptance-judgment-1.md`

Any extra or missing path:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Do not cleanup, restore, ignore, absorb, or stage unexpected dirt.

# exact pending governance identity — 18

Before any Git mutation, verify every path and SHA-256:

- `.aiassistant/records/aiscc/cycles/20260908_1443_aiscc-command-center-workflow-correction-final-acceptance-p2-2-entry-1.cycle.md`  `65c764f1702c96f3750a09d68f4d72baef69303d96155960c78c9a18d2881f4c`
- `.aiassistant/reports/aiscc/20260908_1443_aiscc-command-center-workflow-correction-final-acceptance-judgment-1.md`  `8c0ab4ac32f0173af68a8d8db378b23673fcbf50331323d427659466e091e9b6`
- `.aiassistant/tasks/done/20260908_1512_aiscc-p2-2-synthetic-demo-repository-source-contract-audit-retry-1.md`  `81a4a226aee9529213980bd2dc69e4435e7b2cbad5965e56fdf4be889a81dc9d`
- `.aiassistant/records/aiscc/cycles/20260908_1512_aiscc-p2-2-source-contract-audit-blocked-transport-stop-and-fresh-session-retry-entry-1.cycle.md`  `e451a2530fd3fef3690ffe9665318555911c2a244f20a4f91e1ec1fc4e3763ac`
- `.aiassistant/reports/aiscc/20260908_1512_aiscc-p2-2-source-contract-audit-transport-stop-violation-judgment-1.md`  `6b57422d9b86613773e31bbb97c2751d616deb9e6266c8e4c13644844e6818a6`
- `.aiassistant/records/aiscc/cycles/20260908_1519_aiscc-p2-2-audit-blocked-transport-tool-policy-recovery-entry-1.cycle.md`  `16ec36ee281a7f296dfc8ed3b20dd00ad21f5288c5e67f890d4c796e6dcd2edf`
- `.aiassistant/reports/aiscc/20260908_1519_aiscc-p2-2-audit-transport-tool-policy-blocked-judgment-1.md`  `eddc2cf216403814d80517e94c0c335c928ad2f723396b8d3b2823979214d686`
- `.aiassistant/records/aiscc/cycles/20260908_1528_aiscc-p2-2-audit-blocked-command-center-dirt-contract-correction-entry-1.cycle.md`  `a39289cdf1bb8556d592b95b0158c390a04da93943f2aaff2f3ee22af7b5db51`
- `.aiassistant/reports/aiscc/20260908_1528_aiscc-p2-2-audit-command-center-dirt-contract-correction-judgment-1.md`  `d576891c7d7ebef39c0cc225ee1dd130fa1a0170705249bd4a5020dd6b0895f7`
- `.aiassistant/tasks/done/20260908_1443_aiscc-p2-2-synthetic-demo-repository-source-contract-audit-1.md`  `3035f62c1b978da5d835e771dc7138a2e789e3cb7349668d50f44ada3a9be92d`
- `.aiassistant/tasks/done/20260908_1519_aiscc-p2-2-transport-policy-compatible-source-contract-audit-retry-1.md`  `f8b773e14e312cc71129cd6f736d1e591786e95574fcead56f0e499277057268`
- `.aiassistant/tasks/done/20260908_1528_aiscc-p2-2-source-contract-audit-provenance-reconciliation-retry-1.md`  `31a1b4f6bd02c59dcff832b26252507308ddf38183e4c418fbe512e4ab186489`
- `.aiassistant/tasks/done/20260908_1549_aiscc-p2-2-synthetic-stockroom-candidate-implementation-1.md`  `4311a7798d37ac63d3161ad7427217381088c0d53c1f642f391f43f693dcaae1`
- `.aiassistant/records/aiscc/cycles/20260908_1549_aiscc-p2-2-source-contract-audit-final-acceptance-implementation-entry-1.cycle.md`  `d9cd5fa4bc5114d7868eedc6b0af6f9aa17af73ad3f6015e6560586a7b4eacaf`
- `.aiassistant/reports/aiscc/20260908_1549_aiscc-p2-2-source-contract-audit-final-acceptance-judgment-1.md`  `0b10603b3dea8dacdf481ee8d3d7290a655a1dd28118b045520d8407a5f7c0d6`
- `.aiassistant/records/aiscc/cycles/20260908_1602_aiscc-p2-2-implementation-blocked-transport-prompt-regression-retry-entry-1.cycle.md`  `f58015a3e8fc1094e8f5b18584ec9e954b8cb4747ac3421310b321a9fff23455`
- `.aiassistant/reports/aiscc/20260908_1602_aiscc-p2-2-implementation-transport-prompt-regression-judgment-1.md`  `7804fba2f036a26228b33e0108698ad9bdf861b20c782b37dbca4054bcf81b9c`
- `.aiassistant/tasks/done/20260908_1602_aiscc-p2-2-synthetic-stockroom-candidate-implementation-transport-retry-1.md`  `8ddedd9dfc2682e79e4933ae79c6f4b6915525baa502f5179fa52495e70c828d`

Any mismatch:

```text
PENDING_GOVERNANCE_IDENTITY_MISMATCH
→ STOP
```

Do not overwrite or repair.

# exact accepted source identity — 14

Verify every source SHA-256:

- `examples/synthetic-stockroom/.gitignore`  `03824949a66ab6db1429bd078d10d1bc2d75706aa1b756c547f9a7ff541c77cb`
- `examples/synthetic-stockroom/.python-version`  `f50159fad3f4319868eb38717b91d55843c41e9803014c8de05e116a6d0bcfdc`
- `examples/synthetic-stockroom/PROVENANCE.md`  `83e55cadfd99ec0fe53f0b6fabd70e93dc5281829b7f7d47fdeab728d0479507`
- `examples/synthetic-stockroom/README.md`  `c98195e31173cd2e735b44112b033d3e292e70827571978ad3fb2e8bb05e9489`
- `examples/synthetic-stockroom/stockroom/__init__.py`  `d1aac4ef42c031fc7ba3804859afdfe9216ad6efedbdf23b62bdc6fba9651b42`
- `examples/synthetic-stockroom/stockroom/__main__.py`  `307299fda7b77d22c64cb51430ec75e5f59d78e9c948786afb3b2544fe45e4b7`
- `examples/synthetic-stockroom/stockroom/cli.py`  `1db02a0f67e880ebe0adcdc76bfec49cd9f1eca2f5ec7d918534001b27f59de7`
- `examples/synthetic-stockroom/stockroom/data/catalog.json`  `02ee3b0d41166f9a33ac0445a9db289b304a6005b13664e5a80eebea39d4b41a`
- `examples/synthetic-stockroom/stockroom/inventory.py`  `6b03fd5774c7dc24dfba70e7ff35acf0794582110fc5c5f0371a0aeb722d6cdb`
- `examples/synthetic-stockroom/stockroom/model.py`  `ed385912ab0fe0ab3b9d454a8d2c90edc72199324f09989bda5de9afe3863be1`
- `examples/synthetic-stockroom/tests/test_cli.py`  `e432c84d8add1210d45fd2be677be190329449db9e81c7313f3749ddca58dbe6`
- `examples/synthetic-stockroom/tests/test_contract.py`  `9b93a776c664a984df156c03aa25ab4d9e6708b7e8f2d241547ad06cc5e5ce3f`
- `examples/synthetic-stockroom/tests/test_inventory.py`  `dbe11542333091048908b32eb14cb0d026001d9e9f67d9b0b28d7938b5e13a4e`
- `examples/synthetic-stockroom/tools/build.py`  `f02aaea4c347648ca59471b50973c5f571c910c5e7d5e950a62e41e48a74b18f`

Require:

```text
14 / 14 exact
```

Any mismatch:

```text
ACCEPTED_CANDIDATE_IDENTITY_MISMATCH
→ STOP
```

Do not modify or restore.

# residue gate

The following must be absent under `examples/synthetic-stockroom/`:

```text
.build/
stockroom.pyz
__pycache__/
*.pyc
```

No unexpected persistent path is allowed.

Do not use broad cleanup to make this pass.

If residue exists:

```text
UNEXPECTED_WORKSPACE_RESIDUE
→ STOP
```

# evidence reuse

If all exact identity gates PASS:

```text
1602 source implementation:
REUSED_ACCEPTED

20/20 unit tests:
REUSED_ACCEPTED

CPython 3.12.14 runtime verification:
REUSED_ACCEPTED

deterministic repeat build:
REUSED_ACCEPTED

module/pyz CLI parity:
REUSED_ACCEPTED

source/seed stability:
REUSED_ACCEPTED
```

No new implementation/runtime execution is required.

This reuse is valid only because source identity is exact and no source/config/test mutation is permitted.

# current Task lifecycle

After all pre-persistence gates PASS:

```text
.aiassistant/tasks/active/20260908_1642_aiscc-p2-2-synthetic-stockroom-final-acceptance-git-persistence-1.md
→
.aiassistant/tasks/done/20260908_1642_aiscc-p2-2-synthetic-stockroom-final-acceptance-git-persistence-1.md
```

Do not edit Task body.

Then Git-visible final commit candidate must be exact **35 paths**.

# exact 35-path commit allowlist

- `.aiassistant/records/aiscc/cycles/20260908_1443_aiscc-command-center-workflow-correction-final-acceptance-p2-2-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1443_aiscc-command-center-workflow-correction-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260908_1512_aiscc-p2-2-synthetic-demo-repository-source-contract-audit-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_1512_aiscc-p2-2-source-contract-audit-blocked-transport-stop-and-fresh-session-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1512_aiscc-p2-2-source-contract-audit-transport-stop-violation-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_1519_aiscc-p2-2-audit-blocked-transport-tool-policy-recovery-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1519_aiscc-p2-2-audit-transport-tool-policy-blocked-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_1528_aiscc-p2-2-audit-blocked-command-center-dirt-contract-correction-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1528_aiscc-p2-2-audit-command-center-dirt-contract-correction-judgment-1.md`
- `.aiassistant/tasks/done/20260908_1443_aiscc-p2-2-synthetic-demo-repository-source-contract-audit-1.md`
- `.aiassistant/tasks/done/20260908_1519_aiscc-p2-2-transport-policy-compatible-source-contract-audit-retry-1.md`
- `.aiassistant/tasks/done/20260908_1528_aiscc-p2-2-source-contract-audit-provenance-reconciliation-retry-1.md`
- `.aiassistant/tasks/done/20260908_1549_aiscc-p2-2-synthetic-stockroom-candidate-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_1549_aiscc-p2-2-source-contract-audit-final-acceptance-implementation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1549_aiscc-p2-2-source-contract-audit-final-acceptance-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_1602_aiscc-p2-2-implementation-blocked-transport-prompt-regression-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1602_aiscc-p2-2-implementation-transport-prompt-regression-judgment-1.md`
- `.aiassistant/tasks/done/20260908_1602_aiscc-p2-2-synthetic-stockroom-candidate-implementation-transport-retry-1.md`
- `examples/synthetic-stockroom/.gitignore`
- `examples/synthetic-stockroom/.python-version`
- `examples/synthetic-stockroom/PROVENANCE.md`
- `examples/synthetic-stockroom/README.md`
- `examples/synthetic-stockroom/stockroom/__init__.py`
- `examples/synthetic-stockroom/stockroom/__main__.py`
- `examples/synthetic-stockroom/stockroom/cli.py`
- `examples/synthetic-stockroom/stockroom/data/catalog.json`
- `examples/synthetic-stockroom/stockroom/inventory.py`
- `examples/synthetic-stockroom/stockroom/model.py`
- `examples/synthetic-stockroom/tests/test_cli.py`
- `examples/synthetic-stockroom/tests/test_contract.py`
- `examples/synthetic-stockroom/tests/test_inventory.py`
- `examples/synthetic-stockroom/tools/build.py`
- `.aiassistant/records/aiscc/cycles/20260908_1642_aiscc-p2-2-synthetic-stockroom-implementation-accepted-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_1642_aiscc-p2-2-synthetic-stockroom-implementation-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260908_1642_aiscc-p2-2-synthetic-stockroom-final-acceptance-git-persistence-1.md`

No other path may be staged.

# Git persistence authorization

Only after all previous gates PASS:

```text
git add -- <exact 35 literal paths>
git diff --cached --check
git diff --cached --name-status
git commit -m "feat(demo): add P2-2 synthetic stockroom candidate"
```

Expected commit:

```text
parent:
187880eff48cbf2909e0fcadce75c6d2cb30ab31

parent count:
1

message:
feat(demo): add P2-2 synthetic stockroom candidate

changed paths:
exact 35
```

Forbidden:

```text
git add -A
git add .
git clean
git reset
git restore
git checkout
git stash
git push
git pull
git fetch
git merge
git rebase
git cherry-pick
```

# post-commit verification

Verify:

1. result commit hash and tree
2. exact parent `187880eff48cbf2909e0fcadce75c6d2cb30ab31`
3. parent count `1`
4. exact commit message
5. changed path set == exact 35 allowlist
6. committed 14 Synthetic Stockroom blobs match accepted SHA-256 exactly
7. committed pending governance blobs exist and match pre-commit hashes where specified
8. current Cycle/Judgment/Task done are present in commit
9. index empty
10. Git-visible worktree clean
11. generated `.build`, `__pycache__`, `.pyc` absent
12. push/network `NOT_RUN`

# evidence contract

## executor_required

- `COMMAND_CENTER_ARTIFACT_TRANSPORT`
- `WORKSPACE_GIT_PREFLIGHT`
- `PENDING_GOVERNANCE_IDENTITY`
- `ACCEPTED_CANDIDATE_IDENTITY`
- `GIT_PERSISTENCE`
- `PUBLIC_PROVENANCE / COMMIT_VERIFICATION`

## reuse_allowed

- 1602 implementation/test/build/CLI evidence under exact 14-file identity

## human_owned

```text
new Human QA:
NOT_REQUIRED

P2-2 terminal CLOSED judgment:
Browser Command Center only
```

## forbidden

- source/test mutation
- broad cleanup
- test rerun as substitute for identity mismatch
- public Live/Replay/scenario enrollment
- P2-3
- Git push

# mandatory stop

```text
TRANSPORT_FAILURE
TRANSPORT_TOOL_POLICY_BLOCKED
HEAD_OR_TREE_MISMATCH
INDEX_NOT_EMPTY
DIRTY_WORKSPACE_MIXED
PENDING_GOVERNANCE_IDENTITY_MISMATCH
ACCEPTED_CANDIDATE_IDENTITY_MISMATCH
UNEXPECTED_WORKSPACE_RESIDUE
TASK_LIFECYCLE_CONFLICT
GIT_STAGE_ALLOWLIST_MISMATCH
GIT_COMMIT_VERIFICATION_FAILED
SECURITY_BOUNDARY_UNCERTAIN
```

After named blocker: minimal evidence/report/export only.

# export bundle

Target:

```text
.aiassistant/reports/target/20260908_1642_aiscc-p2-2-synthetic-stockroom-final-acceptance-git-persistence-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
CANDIDATE_IDENTITY_VERIFICATION.md
GIT_PERSISTENCE_VERIFICATION.md
```

If commit succeeds, export the exact 35 committed files preserving project-relative paths and prove source/commit/export byte identity for the 14 candidate source files and current governance files.

# final response ceiling

Success:

```text
P2-2 terminal closure readiness:
READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT

P2-2 persistence:
COMPLETED

P2-3:
NOT_STARTED
```

Do not declare `P2-2 CLOSED`.
Do not start P2-3.
