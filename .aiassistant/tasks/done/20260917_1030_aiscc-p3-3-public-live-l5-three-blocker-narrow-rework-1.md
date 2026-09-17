# 작업지시서: P3-3 L5 Three-Blocker Narrow Rework

## meta

- task_id: `20260917_1030_aiscc-p3-3-public-live-l5-three-blocker-narrow-rework-1`
- created_at: `2026-09-17 KST`
- work_type: `REWORK`
- evidence_profile: `HIGH_RISK_NARROW`
- expected_HEAD: `96a4029ec3a82c9b2a88b9718732aa0f00ecad20`
- reviewed_predecessor_zip_sha256: `7fb19c0fcd1ea44c3d4f683d346fd7c34d748589bf547c8e4dc1835ce27ade4e`
- supersedes_prior_command_center_zip_sha256: `c5452a0b9ac21b1911ad34c88a28ef3f39c5ea9c0fb1b8120f7d3aa3cf6d3627`

Use the current IDE Executor conversation.

IMPORTANT:

The earlier 1012 Task is superseded because it incorrectly required the complete repository regression.

This Task is intentionally narrow.

## preflight

Verify:

```text
HEAD == 96a4029ec3a82c9b2a88b9718732aa0f00ecad20
index == empty
predecessor cumulative SOURCE_INVENTORY == 40 files
```

Do not reset or restore the cumulative candidate.

If predecessor identity differs:

`PREDECESSOR_SOURCE_IDENTITY_MISMATCH`

and STOP.

## exact rework scope

Only these three blockers are in scope.

### R1 — semantic role binding

Fix the hosted production path so a semantic plan's server-owned role binding is preserved through physical dispatch.

Required:

```text
PRIMARY = low
VERIFY  = low
CORRECT = medium
```

The downstream P1-5 execution service/adapter may validate but must not overwrite CORRECT to PRIMARY.

Add tests that inspect the actual physical ProviderCall/request binding, not only durable semantic labels.

### R2 — retry physical truth

Fix the QA/proof path where a provider-double receipt was observed and the same operation was then recorded as `DEFINITELY_NOT_SENT`.

Required truth:

```text
DEFINITELY_NOT_SENT
=> remote receipt count for that operation = 0
```

Preferred proof:

```text
first operation
→ conclusively closes before remote receipt
→ DEFINITELY_NOT_SENT
→ receipts 0

single same-role retry
→ new operation
→ one actual provider-double receipt
→ known result
```

UNKNOWN / MAY_HAVE_SENT remains no-blind-retry.

If the accepted P1-5 model cannot truthfully represent the intended retry:

`P1_5_RETRY_REPRESENTATION_GAP`

and STOP.

### R3 — stockroom_summary production runtime

Audit and reuse the existing accepted server-owned Stockroom tool implementation if one exists.

Production Public Live currently advertises:

`stockroom_summary`

and freezes one tool dispatch maximum.

Wire the actual canonical P1-5 tool execution path:

```text
provider function_call
→ exact ToolRegistry validation
→ P1-3/P1-5 authorization
→ stockroom_summary dispatcher
→ durable TOOL operation/result
→ function_call_output
→ provider continuation
```

Hard constraints:

- exactly `stockroom_summary`;
- max one tool dispatch/run;
- no public/user tool selection;
- no arbitrary shell/path/network;
- fixed synthetic Stockroom data only.

If no accepted executable tool owner exists:

`PUBLIC_LIVE_TOOL_RUNTIME_AUTHORITY_GAP`

and STOP.

## test scope — NO FULL REPOSITORY SUITE

The predecessor already executed:

```text
1502 PASS
3 existing SKIP
0 FAIL
0 ERROR
```

Treat that as `REUSED_ACCEPTED` for unchanged scope.

DO NOT run `pytest` over the full repository.

Required targeted tests only:

```text
tests/unit/providers/test_public_semantic.py
tests/unit/providers/test_openai_responses.py
tests/unit/public_live/test_hosted_binding.py
tests/unit/public_live/test_worker_authority.py
tests/integration/public_live/test_hosted_binding.py
tests/integration/public_live/test_start_worker_authority.py
tests/integration/public_live/test_persistence.py
```

Plus any NEW test file created specifically for R1-R3.

If an exact changed production owner has an already-existing directly corresponding test file outside this allowlist, that one file may be added and must be reported.

Do not broaden to unrelated modules.

## mandatory targeted assertions

Prove:

1. actual physical request efforts:
   - PRIMARY low
   - VERIFY low
   - CORRECT medium

2. retry truth:
   - first definitely-not-sent operation has zero remote receipts;
   - retry has new operation identity;
   - one retry maximum;
   - post-dispatch timeout/unknown has no retry.

3. tool runtime:
   - provider emits stockroom_summary call;
   - production dispatcher executes exactly once;
   - durable TOOL result exists;
   - function_call_output continues into next provider call;
   - second tool dispatch denied;
   - unknown tool denied before side effect.

4. retain predecessor-good behavior in the directly affected test files:
   - worker claim/fence/pin;
   - provider-double observation;
   - hosted adapter boundary;
   - secret non-exposure for this path.

## static checks — narrow only

Run only on cumulative Task-changed Python paths:

```text
ruff check
ruff format --check
```

Run mypy only on production modules changed by this narrow rework and their direct typed owners.

Run `git diff --check`.

Do not reformat unrelated repository files.

## PostgreSQL

Do NOT rerun all database regression suites merely because this is HIGH_RISK.

Run PostgreSQL only for the directly impacted R1-R3 integration tests if they require it.

Migrations are unchanged:

```text
20260916_0018
20260917_0019
20260917_0020
```

No migration change is expected.

If R1-R3 requires schema/migration change:

`MIGRATION_SCOPE_EXPANSION_REQUIRED`

and STOP.

## evidence scope expansion rule

If targeted tests reveal that the fix affects an unrelated owner/module and safe judgment requires broad/full-suite testing:

```text
EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

STOP.

Do NOT silently run thousands of tests.

Browser Command Center will decide the expanded evidence scope separately.

## external actions forbidden

```text
real OpenAI:
0

real key read/export:
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

`HOSTED_PUBLIC_LIVE_THREE_BLOCKER_NARROW_REWORKED / LOCAL_ACCEPTED_CANDIDATE`

Possible blockers:

- `P1_5_RETRY_REPRESENTATION_GAP`
- `PUBLIC_LIVE_TOOL_RUNTIME_AUTHORITY_GAP`
- `MIGRATION_SCOPE_EXPANSION_REQUIRED`
- `EVIDENCE_SCOPE_EXPANSION_REQUIRED`
- `PREDECESSOR_SOURCE_IDENTITY_MISMATCH`

## export

Include:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `SOURCE_INVENTORY.json`
- `SEMANTIC_ROLE_BINDING_PROOF.md`
- `RETRY_PHYSICAL_TRUTH_PROOF.md`
- `STOCKROOM_TOOL_RUNTIME_PROOF.md`
- `TARGETED_TEST_EVIDENCE.json`
- `WORKSPACE_BEFORE.txt`
- `WORKSPACE_AFTER.txt`

And every cumulative changed source/test/config/migration byte under exact POSIX project-relative paths.

No complete-repository regression evidence is required in this Task.

## final response

Report:

1. result
2. HEAD
3. predecessor identity
4. R1 fix
5. R1 targeted tests
6. R2 fix
7. actual retry receipt counts
8. R2 targeted tests
9. R3 existing tool owner
10. R3 production dispatcher
11. provider→tool→provider proof
12. targeted test totals
13. changed-path Ruff/format/mypy/diff checks
14. predecessor full regression reused
15. evidence scope expansion triggered or not
16. real provider calls
17. external actions
18. Public state
19. workspace/index
20. result ZIP SHA-256
