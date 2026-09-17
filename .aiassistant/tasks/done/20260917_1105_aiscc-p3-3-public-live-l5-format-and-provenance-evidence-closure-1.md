# 작업지시서: P3-3 L5 Format + Provenance Evidence Closure

## meta

- task_id: `20260917_1105_aiscc-p3-3-public-live-l5-format-and-provenance-evidence-closure-1`
- created_at: `2026-09-17 KST`
- work_type: `REWORK`
- evidence_profile: `NARROW_FORMAT_EVIDENCE`
- expected_HEAD: `96a4029ec3a82c9b2a88b9718732aa0f00ecad20`
- reviewed_predecessor_result_zip_sha256: `14d8901d7ddabd8d418f3f65fe2528d0352fdb545d9e8a8bde4dcc776d755b2b`
- authoritative_0825_predecessor_zip_sha256: `7fb19c0fcd1ea44c3d4f683d346fd7c34d748589bf547c8e4dc1835ce27ade4e`

Use the current IDE Executor conversation.

This Task is NOT a semantic/runtime rework.

R1-R3 are Browser-substantively PASS.

## preflight

Verify:

```text
HEAD == 96a4029ec3a82c9b2a88b9718732aa0f00ecad20
index == empty
current cumulative SOURCE_INVENTORY == 41 files
```

Verify the 41 current source/config/test/migration bytes against predecessor result ZIP:

`14d8901d7ddabd8d418f3f65fe2528d0352fdb545d9e8a8bde4dcc776d755b2b`

If mismatch:

`PREDECESSOR_SOURCE_IDENTITY_MISMATCH`

and STOP.

## F1 — identify exact formatter delta

Run `ruff format --check` only on cumulative changed Python paths.

Record the exact paths that would be reformatted.

Expected from predecessor report:

`11`

If the actual count differs, report it. Do not assume 11.

## F2 — formatting only

Run Ruff formatter ONLY on those exact paths.

No manual semantic edits.

No migration edits.

No config edits.

No new source files.

No broad repository formatting.

For every formatted file record:

- before SHA-256;
- after SHA-256;
- Python AST structural hash before;
- Python AST structural hash after.

AST structural hashes must match.

If any formatted path has semantic AST change:

`FORMATTER_SEMANTIC_DRIFT`

and STOP.

## F3 — corrected provenance

Do not rewrite historical evidence.

Record explicitly:

```text
historical WORKSPACE_BEFORE textual SHA:
7fb19c433f74c1f1359a3050cf2490978672e30aad3268058afde517f8ade4e

Browser-verified actual 0825 predecessor SHA:
7fb19c0fcd1ea44c3d4f683d346fd7c34d748589bf547c8e4dc1835ce27ade4e

current 1030 result ZIP SHA:
14d8901d7ddabd8d418f3f65fe2528d0352fdb545d9e8a8bde4dcc776d755b2b
```

Classify the historical SHA as:

`REPORT_PROVENANCE_TYPO / SOURCE_IDENTITY_UNAFFECTED`

## F4 — narrow verification only

DO NOT run the full repository suite.

The predecessor broad regression remains:

```text
1502 PASS
3 existing SKIP
0 FAIL
0 ERROR
REUSED_ACCEPTED
```

The predecessor narrow regression remains:

```text
60 PASS
0 FAIL
0 ERROR
```

After formatting, rerun only these exact critical tests:

```text
tests/integration/public_live/test_hosted_binding.py::test_production_claim_executor_runs_primary_verify_correct

tests/integration/public_live/test_hosted_binding.py::test_known_closed_failure_performs_one_same_role_retry

tests/integration/public_live/test_hosted_binding.py::test_durable_post_dispatch_unknown_quarantines_without_resend

tests/integration/public_live/test_hosted_binding.py::test_production_stockroom_tool_dispatches_once_and_continues

tests/integration/public_live/test_hosted_binding.py::test_production_tool_scope_denies_unknown_and_second_dispatch
```

For the parametrized final test, execute all generated cases.

If formatting touches a directly related unit test file, its exact corresponding unit file may also be run.

No unrelated test module.

## F5 — static closure

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

## evidence expansion

If any exact key test fails after formatting, or AST equivalence fails:

STOP.

Do not expand into full-suite testing automatically.

Use:

`EVIDENCE_SCOPE_EXPANSION_REQUIRED`

when wider evidence is truly necessary.

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

Create one target ZIP containing:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `SOURCE_INVENTORY.json`
- `FORMATTER_CLOSURE_PROOF.md`
- `PROVENANCE_CORRECTION.md`
- `TARGETED_TEST_EVIDENCE.json`
- `WORKSPACE_BEFORE.txt`
- `WORKSPACE_AFTER.txt`

and every cumulative changed source/test/config/migration byte under exact POSIX project-relative paths.

## final response

Report:

1. result
2. HEAD
3. predecessor ZIP verification
4. exact formatted paths/count
5. before/after SHA identities
6. AST equivalence
7. corrected provenance
8. exact key tests
9. Ruff check
10. Ruff format check
11. mypy narrow result
12. git diff check
13. predecessor broad regression reuse
14. full repository pytest run = false
15. external actions
16. Public state
17. workspace/index
18. result ZIP SHA-256
