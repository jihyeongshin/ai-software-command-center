# 작업지시서: P3-3 L5 Corrected Format + Provenance Closure

## meta

- task_id: `20260917_1154_aiscc-p3-3-public-live-l5-corrected-format-provenance-closure-1`
- created_at: `2026-09-17 KST`
- work_type: `REWORK`
- evidence_profile: `NARROW_FORMAT_EVIDENCE`
- expected_HEAD: `96a4029ec3a82c9b2a88b9718732aa0f00ecad20`
- reviewed_conflict_stop_zip_sha256: `eee560f818015f95ea0d0f461b88c5be61c0b1fa55ff0f1463eccddc32cbc303`
- implementation_base_result_zip_sha256: `14d8901d7ddabd8d418f3f65fe2528d0352fdb545d9e8a8bde4dcc776d755b2b`
- authoritative_0825_predecessor_zip_sha256: `7fb19c0fcd1ea44c3d4f683d346fd7c34d748589bf547c8e4dc1835ce27ade4e`

Use the current IDE Executor conversation.

The previous 1105 Task is superseded due to an internal contract conflict.

This Task is formatting/provenance closure only.

R1/R2/R3 remain Browser-substantively PASS.

## preflight

Verify:

```text
HEAD == 96a4029ec3a82c9b2a88b9718732aa0f00ecad20
index == empty
current cumulative SOURCE_INVENTORY == 41 files
```

Verify current 41 source/config/test/migration bytes match the reviewed conflict-stop bundle:

`eee560f818015f95ea0d0f461b88c5be61c0b1fa55ff0f1463eccddc32cbc303`

Since that stop performed zero source formatting mutations, this also proves continuity from the implementation base.

If mismatch:

`PREDECESSOR_SOURCE_IDENTITY_MISMATCH`

and STOP.

## C1 — exact formatter target discovery

Run `ruff format --check` only on cumulative changed Python paths.

Record exact target paths.

Expected from the accepted stop:

11 paths, including:

`migrations/versions/20260916_0018_public_live_execution_integration.py`

Do not assume the count if actual output differs.

## C2 — formatter-only mutation authority

Run Ruff formatter ONLY on the exact target paths returned by C1.

This explicitly includes formatter-only normalization of:

`migrations/versions/20260916_0018_public_live_execution_integration.py`

### allowed

- whitespace;
- line wrapping;
- quote normalization only where Python AST and string values are unchanged;
- other Ruff formatter-only syntax-preserving normalization.

### forbidden

- manual semantic edit;
- revision change;
- down_revision change;
- SQL content/value change;
- string literal runtime value change;
- migration operation addition/removal/reordering;
- upgrade/downgrade semantic change;
- new migration;
- changes to 0019/0020 unless Ruff itself identifies them as exact formatter targets.

## C3 — mandatory equivalence proof

For every formatted Python file record:

- before SHA-256;
- after SHA-256;
- parsed AST structural hash before;
- parsed AST structural hash after.

AST structural hashes MUST match.

For every formatted migration file additionally prove:

- `revision` exact value unchanged;
- `down_revision` exact value unchanged;
- `ast.dump()` of module before/after identical;
- every string literal value sequence before/after identical;
- upgrade function AST identical;
- downgrade function AST identical;
- migration graph identity unchanged.

If any invariant differs:

`FORMATTER_SEMANTIC_DRIFT`

and STOP.

## C4 — provenance correction

Record, without rewriting historical evidence:

```text
historical WORKSPACE_BEFORE textual SHA:
7fb19c433f74c1f1359a3050cf2490978672e30aad3268058afde517f8ade4e

Browser-verified actual 0825 predecessor SHA:
7fb19c0fcd1ea44c3d4f683d346fd7c34d748589bf547c8e4dc1835ce27ade4e

1030 implementation result ZIP:
14d8901d7ddabd8d418f3f65fe2528d0352fdb545d9e8a8bde4dcc776d755b2b

1105 conflict-stop result ZIP:
eee560f818015f95ea0d0f461b88c5be61c0b1fa55ff0f1463eccddc32cbc303
```

Classification:

`REPORT_PROVENANCE_TYPO / SOURCE_IDENTITY_UNAFFECTED`

## C5 — narrow verification only

DO NOT run the full repository suite.

Reuse:

```text
predecessor broad regression:
1502 PASS / 3 existing SKIP / 0 FAIL / 0 ERROR

predecessor narrow regression:
60 PASS / 0 FAIL / 0 ERROR
```

After formatting, run only these exact critical tests:

```text
tests/integration/public_live/test_hosted_binding.py::test_production_claim_executor_runs_primary_verify_correct

tests/integration/public_live/test_hosted_binding.py::test_known_closed_failure_performs_one_same_role_retry

tests/integration/public_live/test_hosted_binding.py::test_durable_post_dispatch_unknown_quarantines_without_resend

tests/integration/public_live/test_hosted_binding.py::test_production_stockroom_tool_dispatches_once_and_continues

tests/integration/public_live/test_hosted_binding.py::test_production_tool_scope_denies_unknown_and_second_dispatch
```

For parametrized tests, run all generated cases.

If Ruff formatting touches a directly related unit test file, its exact corresponding unit test file may also be run.

No unrelated test module.

## C6 — static closure

On all cumulative changed Python paths:

```text
ruff check
ruff format --check
```

Both MUST PASS.

Also run:

```text
git diff --check
```

Run mypy only on production Python files actually formatted in this Task.

No repository-wide mypy.

## scope expansion

If key tests fail, AST equivalence fails, migration literals differ, or safe closure requires broader evidence:

`EVIDENCE_SCOPE_EXPANSION_REQUIRED`

and STOP.

Do NOT run thousands of tests automatically.

## external actions forbidden

```text
real OpenAI:
0

Railway:
0

Cloudflare:
0

Git add/commit/push:
0

Public admission enable:
0

Public Live release:
0
```

## expected result

`PUBLIC_LIVE_LOCAL_FORMAT_EVIDENCE_CLOSED / LOCAL_ACCEPTED_CANDIDATE`

## export

Include:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `SOURCE_INVENTORY.json`
- `FORMATTER_CLOSURE_PROOF.md`
- `MIGRATION_FORMAT_EQUIVALENCE_PROOF.md`
- `PROVENANCE_CORRECTION.md`
- `TARGETED_TEST_EVIDENCE.json`
- `WORKSPACE_BEFORE.txt`
- `WORKSPACE_AFTER.txt`

and every cumulative changed source/test/config/migration byte under exact POSIX project-relative paths.

## final response

Report:

1. result
2. HEAD
3. conflict-stop predecessor identity
4. exact formatter target paths/count
5. exact migration formatter targets
6. per-file before/after SHA
7. AST equivalence
8. migration revision/down_revision equivalence
9. migration string literal equivalence
10. corrected provenance
11. exact key tests
12. Ruff check
13. Ruff format check
14. narrow mypy
15. git diff check
16. predecessor broad/narrow evidence reuse
17. full repository pytest run = false
18. external actions
19. Public state
20. workspace/index
21. result ZIP SHA-256
