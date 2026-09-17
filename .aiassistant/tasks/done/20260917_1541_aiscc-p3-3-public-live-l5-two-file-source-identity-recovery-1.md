# 작업지시서: P3-3 L5 Two-File Source Identity Recovery

## meta

- task_id: `20260917_1541_aiscc-p3-3-public-live-l5-two-file-source-identity-recovery-1`
- created_at: `2026-09-17 KST`
- work_type: `SOURCE_IDENTITY_RECOVERY`
- evidence_profile: `HIGH_RISK_NARROW`
- expected_HEAD: `dc73fe8c7cbdaee176124dfd71f3ac9d76e8eeb6`
- reviewed_evidence_zip_sha256: `a45821f926aad7beeae351c9f85576d2e3be95b56e0794e323753ed345d2f2c4`

Use the current IDE Executor conversation.

This is NOT a new architecture implementation.

It recovers exactly two source files that were changed by the accepted 1030 narrow rework but omitted from its SOURCE_INVENTORY/export.

## exact candidate allowlist

```text
src/aiscc/public_live/luna_profile.py
src/aiscc/public_live/provider_authority.py
```

Expected current worktree identities:

```text
src/aiscc/public_live/luna_profile.py
SHA-256 = e7dfbf5fac42b8fdff4766a7e09a8a4c1cda6a52cf6e4a3c0827d0fbb30196cb
size = 6826

src/aiscc/public_live/provider_authority.py
SHA-256 = 98f3e83662a410e1dae15e7dfe487bb15830f4be80920031c8bf12b43b5e5d0d
size = 6752
```

## R0 — preflight

Require:

```text
HEAD == dc73fe8c7cbdaee176124dfd71f3ac9d76e8eeb6
origin/main == dc73fe8c7cbdaee176124dfd71f3ac9d76e8eeb6
index == empty
```

Verify both exact worktree SHA/size values above BEFORE any command that could mutate source.

If either differs:

`RECOVERY_CANDIDATE_IDENTITY_MISMATCH`

and STOP.

Do NOT:

- restore/reset/checkout/stash;
- format;
- edit;
- stage;
- commit;
- push.

## R1 — static compatibility proof

Without modifying files, prove these exact candidate bytes close the persisted source mismatch.

### provider_authority

Verify the current `LunaToolScopeAuthority` supports:

```text
construction:
spec + principal + run_id

deferred:
build_dispatch_context
→ bind(dispatch_context, fingerprint)
→ issue_context / allows
```

and still enforces:

- exact Stockroom resource id;
- exact command;
- network = none;
- exact expected run_id;
- one stable dispatch binding;
- 64-char operation fingerprint;
- no second conflicting bind.

### luna_profile

Verify `bind_call`:

- INITIAL_SERVER remains text-only;
- DURABLE_LOCAL requires durable_continuation_hash;
- durable continuation hash shape remains exact;
- allowed continuation item types are only:
  `message`, `function_call`, `function_call_output`, `reasoning`;
- provider/model/endpoint/tool/budget/reasoning profile remains server-owned and unchanged.

Create `TWO_FILE_COMPATIBILITY_PROOF.md`.

## R2 — narrow tests only

Do NOT run the full repository suite.

Run only:

```text
tests/unit/providers/test_luna_profile.py
tests/unit/providers/test_luna_tool.py

tests/integration/public_live/test_hosted_binding.py::test_production_claim_executor_runs_primary_verify_correct

tests/integration/public_live/test_hosted_binding.py::test_production_stockroom_tool_dispatches_once_and_continues

tests/integration/public_live/test_hosted_binding.py::test_production_tool_scope_denies_unknown_and_second_dispatch
```

For parametrized tests, execute all generated cases.

These tests must run against the exact preflight candidate bytes.

If a test command generates cache, cache is non-authoritative residue and must not be staged.

Do not broaden testing automatically.

If a direct failure indicates another source owner is required:

`SOURCE_RECOVERY_SCOPE_EXPANSION_REQUIRED`

and STOP.

## R3 — narrow static checks

Run without changing source:

```text
ruff check   src/aiscc/public_live/luna_profile.py   src/aiscc/public_live/provider_authority.py
```

Run mypy only for the two candidate modules plus the direct consumer:

```text
src/aiscc/public_live/luna_profile.py
src/aiscc/public_live/provider_authority.py
src/aiscc/public_live/stockroom_runtime.py
```

Do NOT run `ruff format` and do NOT require repository-wide formatter state.

Run `git diff --check` only as diagnostic.

If its only complaint is CR-at-EOL/mixed-EOL on these exact already-identified dirty files, report it without changing bytes.
Any other whitespace defect is a blocker.

## R4 — post-test exact-byte identity

After all tests/static checks:

- re-hash both source files;
- require exact same SHA/size as R0;
- index must remain empty;
- HEAD/origin unchanged.

No source mutation is permitted in this Task.

## R5 — export exact recovered source

The target ZIP MUST include the current exact bytes at project-relative paths:

```text
src/aiscc/public_live/luna_profile.py
src/aiscc/public_live/provider_authority.py
```

Create `SOURCE_INVENTORY.json` with exactly 2 entries and their SHA/size.

Also include:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `TWO_FILE_COMPATIBILITY_PROOF.md`
- `TARGETED_TEST_EVIDENCE.json`
- `STATIC_CHECKS.md`
- `WORKSPACE_BEFORE.txt`
- `WORKSPACE_AFTER.txt`

POSIX archive paths only.

## evidence reuse

Do not rerun broad regression.

Historical evidence remains contextual:

```text
1030 narrow:
60 PASS

predecessor broad:
1502 PASS / 3 existing SKIP
```

This Task owns only exact-byte recovery proof for the two omitted source files.

## forbidden

```text
source mutation:
0

Git stage/commit/push:
0

Railway:
0

Cloudflare:
0

OpenAI:
0

Public admission:
DISABLED

Public Live:
NOT_RELEASED
```

## expected result

Preferred:

`OMITTED_LOAD_BEARING_SOURCE_RECOVERED / LOCAL_ACCEPTED_CANDIDATE`

Possible blocker:

- `RECOVERY_CANDIDATE_IDENTITY_MISMATCH`
- `SOURCE_RECOVERY_SCOPE_EXPANSION_REQUIRED`

## final response

Report:

1. result
2. HEAD/origin
3. preflight source hashes
4. constructor/deferred-bind compatibility
5. durable-local continuation compatibility
6. exact tests and totals
7. Ruff result
8. narrow mypy result
9. diagnostic diff-check classification
10. post-test source hashes
11. source mutation = 0
12. index state
13. Railway/OpenAI/Cloudflare = 0
14. result ZIP SHA-256
15. next Browser gate = exact two-file source acceptance
