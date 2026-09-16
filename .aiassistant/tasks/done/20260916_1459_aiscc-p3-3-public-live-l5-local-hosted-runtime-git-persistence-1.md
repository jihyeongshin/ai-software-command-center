# 작업지시서: P3-3 L5 Local Hosted Runtime Git Persistence

## meta

- task_id: `20260916_1459_aiscc-p3-3-public-live-l5-local-hosted-runtime-git-persistence-1`
- created_at: `2026-09-16 KST`
- work_type: `GIT_PERSISTENCE`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_starting_HEAD: `04436a11adc6dd6e70b4a98568fe878cc4c9f4aa`
- predecessor_result_zip_sha256: `7685dd83a608b28056138b6d4bf7c2641415933e25b836b6b9d79cac8a8ea54c`
- expected_commit_path_count: `42`
- commit_message: `feat: add hosted public live runtime boundary`

Use the current IDE Executor conversation. No fresh chat is required.

## current state

```text
L4:
CLOSED

L5 local implementation:
BROWSER_ACCEPTED_CANDIDATE

L5 terminal:
OPEN

Human Railway deployment:
WAITING_FOR_PERSISTENCE

Public admission:
DISABLED

Public Live:
NOT_RELEASED
```

## mandatory preflight

Starting HEAD must equal:

`04436a11adc6dd6e70b4a98568fe878cc4c9f4aa`

Index must be empty before canonical placement/staging.

Do not require the whole worktree to be clean.

Existing untracked `__pycache__`/local residue is known and non-blocking.

Do not delete or stage it.

## accepted source identity

Verify the current worktree bytes for all 17 paths exactly:

- `src/aiscc/providers/external_ide.py` — `cc126eee28ca16f9eb1fd7710c161bcb99a8410f16055de8cc2959d41489e7bc`
- `src/aiscc/providers/openai_responses.py` — `7b225ee1c1aa85d46e38bf93649a79f68a37c95d01a80d7468aa7b98506ba1b6`
- `src/aiscc/providers/service.py` — `59b25a34638d1176c636b9c4845b39669d02fe687ff76282d3d76b52386da3f5`
- `src/aiscc/public_live/luna_profile.py` — `de4117f63066079f5971e0d569fdb22c1d510358675c8d2ebb35a3b4ed742424`
- `src/aiscc/runtime/docker.py` — `1a9904ca8b90beec4027f736b7533015a86f03899bac41eb618790434d3dae98`
- `src/aiscc/runtime/process.py` — `514b528e40dca70b4ddfa44641cdb29d71a8f28698cf08457738fc3bd641d552`
- `tests/fixtures/providers/luna_capabilities.py` — `7ccde687d3c60d06fb5cf732b1a31a40219925eaddea5ff0dff58163405611d7`
- `src/aiscc/runtime/child_environment.py` — `1f1a58a953d4c4409b96a039031890e8c78b8b33986026720ea3465c97c9d5a1`
- `src/aiscc/providers/hosted_secret.py` — `e57fd0d43b9cab748b542fe2fab9b6340e99742835be9a7268bbf025870cb2a8`
- `tests/unit/providers/test_hosted_secret.py` — `ee48943233ef9cd888f3d5bc689372a99fc2063f80df7a517f12b4448e7d0145`
- `config/deployment/public-live-railway.v1.toml` — `090eda293a555afc03635854189e48e889b815ef557bd67276c7c1dcd0c9d063`
- `tests/integration/providers/test_hosted_secret_durable.py` — `4b09ebcd488d0ed1b49ced6979c7574d59634717772203f80be29552c4c00dd3`
- `src/aiscc/security/policy.py` — `8f65d429c6c2d02e9d85b25661333e31e540b21f567212de409e0c868437dacb`
- `src/aiscc/public_live/context_authority.py` — `f5c8f627d0788e4d85b00f45c60755acb2c1bc098d84fc0447ff5a8154e5ea59`
- `src/aiscc/public_live/provider_authority.py` — `b99f469e9e86970c15ed4c0ed37ceee69cb5872f00413a2679d878ef0f19e874`
- `tests/unit/public_live/test_context_authority.py` — `99a08b0b28eebd74d9a575caa5e1769ba3a5f8c23cd9c692a2a9f838779b46e6`
- `tests/runtime/security/test_hosted_container_secret.py` — `7417919a61a6c385178fc1012a11fce3ecc8ad17252707e882e4e493484171ec`

Any mismatch:

`DOCUMENT_CONTRACT_MISMATCH`

and STOP before staging.

## accepted governance identity already in workspace

Verify these exact 21 canonical paths exist:

- `.aiassistant/reports/aiscc/20260916_1310_aiscc-browser-command-center-l4-durable-luna-persistence-final-acceptance-1.md`
- `.aiassistant/reports/aiscc/20260916_1310_aiscc-browser-command-center-l4-implementation-accepted-account-evidence-handoff-1.md`
- `.aiassistant/reports/aiscc/20260916_1352_aiscc-browser-command-center-l4-closed-l5-railway-secret-binding-entry-handoff-1.md`
- `.aiassistant/reports/aiscc/20260916_1352_aiscc-browser-command-center-l4-terminal-acceptance-l5-secret-binding-selection-1.md`
- `.aiassistant/reports/aiscc/20260916_1352_aiscc-p3-3-public-live-l4-openai-account-evidence-human-accepted.md`
- `.aiassistant/reports/aiscc/20260916_1412_aiscc-browser-command-center-l5-local-secret-binding-rework-required-1.md`
- `.aiassistant/reports/aiscc/20260916_1412_aiscc-browser-command-center-l5-secret-binding-durable-missing-secret-retry-handoff-1.md`
- `.aiassistant/reports/aiscc/20260916_1419_aiscc-browser-command-center-l5-predispatch-secret-resolution-policy-conflict-resolution-1.md`
- `.aiassistant/reports/aiscc/20260916_1419_aiscc-browser-command-center-l5-predispatch-secret-resolution-proof-retry-handoff-1.md`
- `.aiassistant/reports/aiscc/20260916_1430_aiscc-browser-command-center-l5-public-context-capability-proof-retry-handoff-1.md`
- `.aiassistant/reports/aiscc/20260916_1430_aiscc-browser-command-center-l5-public-context-resource-capability-gap-resolution-1.md`
- `.aiassistant/records/aiscc/cycles/20260916_1310_aiscc-p3-3-l4-durable-luna-persistence-final-acceptance-account-evidence-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260916_1352_aiscc-p3-3-public-live-l4-terminal-closure-l5-secret-binding-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260916_1412_aiscc-p3-3-l5-local-secret-binding-rework-durable-missing-secret-evidence-gap-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260916_1419_aiscc-p3-3-l5-predispatch-secret-resolution-policy-conflict-resolved-retry-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260916_1430_aiscc-p3-3-l5-public-context-resource-capability-gap-retry-entry-1.cycle.md`
- `.aiassistant/tasks/done/20260916_1310_aiscc-p3-3-public-live-l4-openai-account-evidence-human-gate-1.md`
- `.aiassistant/tasks/done/20260916_1352_aiscc-p3-3-public-live-l5-railway-secret-binding-and-deployment-contract-implementation-1.md`
- `.aiassistant/tasks/done/20260916_1412_aiscc-p3-3-public-live-l5-secret-binding-durable-missing-secret-and-proof-completion-retry-1.md`
- `.aiassistant/tasks/done/20260916_1419_aiscc-p3-3-public-live-l5-predispatch-secret-resolution-and-proof-completion-retry-1.md`
- `.aiassistant/tasks/done/20260916_1430_aiscc-p3-3-public-live-l5-public-context-resource-capability-and-secret-proof-retry-1.md`

Do not silently regenerate or normalize their bytes.

## inbound Command Center artifacts

Place this delivery ZIP's canonical artifacts:

- TASK → `.aiassistant/tasks/active/20260916_1459_aiscc-p3-3-public-live-l5-local-hosted-runtime-git-persistence-1.md`
- CYCLE → `.aiassistant/records/aiscc/cycles/20260916_1459_aiscc-p3-3-public-live-l5-local-hosted-runtime-acceptance-git-persistence-entry-1.cycle.md`
- JUDGMENT → `.aiassistant/reports/aiscc/20260916_1459_aiscc-browser-command-center-l5-local-hosted-runtime-acceptance-1.md`
- HANDOFF → `.aiassistant/reports/aiscc/20260916_1459_aiscc-browser-command-center-l5-local-accepted-git-persistence-handoff-1.md`

Read the Task before substantive execution.

At task completion move the Task exact bytes:

`.aiassistant/tasks/active/20260916_1459_aiscc-p3-3-public-live-l5-local-hosted-runtime-git-persistence-1.md`
→
`.aiassistant/tasks/done/20260916_1459_aiscc-p3-3-public-live-l5-local-hosted-runtime-git-persistence-1.md`

Do not keep both copies.

## exact commit allowlist

The final Git commit must contain exactly 42 paths:

### A. accepted source/config/test — 17

- `src/aiscc/providers/external_ide.py`
- `src/aiscc/providers/openai_responses.py`
- `src/aiscc/providers/service.py`
- `src/aiscc/public_live/luna_profile.py`
- `src/aiscc/runtime/docker.py`
- `src/aiscc/runtime/process.py`
- `tests/fixtures/providers/luna_capabilities.py`
- `src/aiscc/runtime/child_environment.py`
- `src/aiscc/providers/hosted_secret.py`
- `tests/unit/providers/test_hosted_secret.py`
- `config/deployment/public-live-railway.v1.toml`
- `tests/integration/providers/test_hosted_secret_durable.py`
- `src/aiscc/security/policy.py`
- `src/aiscc/public_live/context_authority.py`
- `src/aiscc/public_live/provider_authority.py`
- `tests/unit/public_live/test_context_authority.py`
- `tests/runtime/security/test_hosted_container_secret.py`

### B. accumulated canonical governance — 21

- `.aiassistant/reports/aiscc/20260916_1310_aiscc-browser-command-center-l4-durable-luna-persistence-final-acceptance-1.md`
- `.aiassistant/reports/aiscc/20260916_1310_aiscc-browser-command-center-l4-implementation-accepted-account-evidence-handoff-1.md`
- `.aiassistant/reports/aiscc/20260916_1352_aiscc-browser-command-center-l4-closed-l5-railway-secret-binding-entry-handoff-1.md`
- `.aiassistant/reports/aiscc/20260916_1352_aiscc-browser-command-center-l4-terminal-acceptance-l5-secret-binding-selection-1.md`
- `.aiassistant/reports/aiscc/20260916_1352_aiscc-p3-3-public-live-l4-openai-account-evidence-human-accepted.md`
- `.aiassistant/reports/aiscc/20260916_1412_aiscc-browser-command-center-l5-local-secret-binding-rework-required-1.md`
- `.aiassistant/reports/aiscc/20260916_1412_aiscc-browser-command-center-l5-secret-binding-durable-missing-secret-retry-handoff-1.md`
- `.aiassistant/reports/aiscc/20260916_1419_aiscc-browser-command-center-l5-predispatch-secret-resolution-policy-conflict-resolution-1.md`
- `.aiassistant/reports/aiscc/20260916_1419_aiscc-browser-command-center-l5-predispatch-secret-resolution-proof-retry-handoff-1.md`
- `.aiassistant/reports/aiscc/20260916_1430_aiscc-browser-command-center-l5-public-context-capability-proof-retry-handoff-1.md`
- `.aiassistant/reports/aiscc/20260916_1430_aiscc-browser-command-center-l5-public-context-resource-capability-gap-resolution-1.md`
- `.aiassistant/records/aiscc/cycles/20260916_1310_aiscc-p3-3-l4-durable-luna-persistence-final-acceptance-account-evidence-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260916_1352_aiscc-p3-3-public-live-l4-terminal-closure-l5-secret-binding-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260916_1412_aiscc-p3-3-l5-local-secret-binding-rework-durable-missing-secret-evidence-gap-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260916_1419_aiscc-p3-3-l5-predispatch-secret-resolution-policy-conflict-resolved-retry-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260916_1430_aiscc-p3-3-l5-public-context-resource-capability-gap-retry-entry-1.cycle.md`
- `.aiassistant/tasks/done/20260916_1310_aiscc-p3-3-public-live-l4-openai-account-evidence-human-gate-1.md`
- `.aiassistant/tasks/done/20260916_1352_aiscc-p3-3-public-live-l5-railway-secret-binding-and-deployment-contract-implementation-1.md`
- `.aiassistant/tasks/done/20260916_1412_aiscc-p3-3-public-live-l5-secret-binding-durable-missing-secret-and-proof-completion-retry-1.md`
- `.aiassistant/tasks/done/20260916_1419_aiscc-p3-3-public-live-l5-predispatch-secret-resolution-and-proof-completion-retry-1.md`
- `.aiassistant/tasks/done/20260916_1430_aiscc-p3-3-public-live-l5-public-context-resource-capability-and-secret-proof-retry-1.md`

### C. this Browser acceptance governance — 3

- `.aiassistant/records/aiscc/cycles/20260916_1459_aiscc-p3-3-public-live-l5-local-hosted-runtime-acceptance-git-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260916_1459_aiscc-browser-command-center-l5-local-hosted-runtime-acceptance-1.md`
- `.aiassistant/reports/aiscc/20260916_1459_aiscc-browser-command-center-l5-local-accepted-git-persistence-handoff-1.md`

### D. this persistence Task — 1

- `.aiassistant/tasks/done/20260916_1459_aiscc-p3-3-public-live-l5-local-hosted-runtime-git-persistence-1.md`

Nothing else may be staged.

## staging

Use exact-path `git add` only.

Forbidden:

- `git add .`
- `git add -A`
- broad glob staging
- `git clean`
- cache cleanup as a gate
- unrelated file normalization

After staging, verify:

```text
git diff --cached --name-only
```

contains exactly the 42 allowed paths and no others.

Verify index source bytes still match the 17 accepted SHA-256 identities.

## persistence commit

Create exactly one commit:

`feat: add hosted public live runtime boundary`

Do not amend an existing commit.

Do not push.

## post-commit verification

Required:

- new HEAD != starting HEAD;
- commit message exact;
- committed path count = 42;
- exact committed-path allowlist match;
- 17 source/config/test blob bytes match accepted hashes;
- index empty;
- tracked worktree clean for all 42 committed paths;
- unrelated cache/local residue may remain and is non-blocking;
- no real provider call;
- no credential read;
- no Railway/Cloudflare mutation;
- Public admission remains DISABLED;
- Public Live remains NOT_RELEASED.

## tests

Do not rerun the full repository suite merely for persistence.

Reuse the Browser-accepted 1430 evidence:

`1460 PASS / 3 existing SKIP / 0 FAIL / 0 ERROR`

Run only integrity/static checks necessary to prove commit identity.

## external actions forbidden

```text
OpenAI provider call:
0

Railway account/project/service mutation:
0

Railway deploy:
0

Cloudflare mutation:
0

Git push:
0

Public enable:
0
```

## acceptable outcome

`COMPLETED / GIT_PERSISTENCE_CANDIDATE`

Do not claim L5 terminal acceptance.

## mandatory stop

- starting HEAD mismatch;
- index unexpectedly non-empty;
- any of 17 accepted source hashes mismatch;
- any required governance path missing;
- exact 42-path staged allowlist cannot be achieved;
- commit contains any extra path;
- accepted source blob changes during persistence.

## export

Create:

`.aiassistant/reports/target/20260916_1459_aiscc-p3-3-public-live-l5-local-hosted-runtime-git-persistence-1/`

Include:

- `EXECUTOR_REPORT.md`
- `COMMIT_EVIDENCE.md`
- `COMMITTED_PATHS.txt`
- `SOURCE_HASH_VERIFICATION.json`
- `WORKSPACE_BEFORE.txt`
- `WORKSPACE_AFTER.txt`
- exact Task copy
- result ZIP

## final response

1. result
2. target bundle
3. starting HEAD
4. final HEAD
5. commit message
6. committed path count
7. allowlist match
8. source hash verification
9. governance path verification
10. index/tracked worktree
11. preserved unrelated residue
12. tests reused
13. external actions
14. Public state
15. next Human Railway gate status
