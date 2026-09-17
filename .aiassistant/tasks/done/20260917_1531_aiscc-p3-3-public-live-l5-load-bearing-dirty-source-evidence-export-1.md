# 작업지시서: P3-3 L5 Load-Bearing Dirty Source Evidence Export

## meta

- task_id: `20260917_1531_aiscc-p3-3-public-live-l5-load-bearing-dirty-source-evidence-export-1`
- created_at: `2026-09-17 KST`
- work_type: `SOURCE_EVIDENCE_EXPORT`
- evidence_profile: `NARROW_READ_ONLY`
- expected_HEAD: `dc73fe8c7cbdaee176124dfd71f3ac9d76e8eeb6`
- predecessor_result_zip_sha256: `468a019563a55e8e813544a8b37344f2214ffa7b9a6a26ff904c6d0541dde022`

Use the current IDE Executor conversation.

This Task is READ-ONLY source evidence export.

It does not authorize source correction, reset, testing, persistence, Railway access, or deployment.

## exact source allowlist

Only these two project source paths are authorized for source evidence export:

```text
src/aiscc/public_live/luna_profile.py
src/aiscc/public_live/provider_authority.py
```

No other unchanged/dirty source may be exported.

## E0 — preflight

Require:

```text
HEAD == dc73fe8c7cbdaee176124dfd71f3ac9d76e8eeb6
origin/main == dc73fe8c7cbdaee176124dfd71f3ac9d76e8eeb6
index == empty
```

Both exact paths should remain tracked-dirty.

If either path is no longer dirty or HEAD/remote changed:

`DIRTY_SOURCE_EVIDENCE_PRECONDITION_CHANGED`

and STOP.

Do NOT:

- reset;
- checkout;
- restore;
- format;
- edit;
- stage;
- stash;
- commit;
- push.

## E1 — committed-byte evidence

For each exact path, obtain committed bytes using:

`git show HEAD:<path>`

Export byte-preserving committed copies under:

```text
SOURCE_EVIDENCE/committed/src/aiscc/public_live/luna_profile.py
SOURCE_EVIDENCE/committed/src/aiscc/public_live/provider_authority.py
```

Record exact SHA-256 and byte size.

## E2 — worktree-byte evidence

Copy current worktree bytes byte-for-byte under:

```text
SOURCE_EVIDENCE/worktree/src/aiscc/public_live/luna_profile.py
SOURCE_EVIDENCE/worktree/src/aiscc/public_live/provider_authority.py
```

Record exact SHA-256 and byte size.

No newline normalization in exported copies.

## E3 — deterministic diff evidence

Create:

`DIRTY_SOURCE_DIFF.md`

For each path include, without secrets:

1. committed SHA/size;
2. worktree SHA/size;
3. newline style/count summary;
4. exact `git diff --no-ext-diff -- <path>` output;
5. unified diff after CRLF/LF normalization;
6. Python AST structural equality result;
7. ordered string-literal equality result;
8. imported module/name additions/removals;
9. top-level class/function additions/removals;
10. changed function/class names inferred from AST positions;
11. constant assignment additions/removals/changed values;
12. whether provider/model/endpoint/reasoning/budget/retry/security semantics appear changed.

Do not replace the raw exported source with prose; Browser needs both exact versions.

## E4 — focused semantic inventory

Create:

`LOAD_BEARING_SEMANTIC_DELTA.json`

For each path provide machine-readable:

- committed_sha256;
- worktree_sha256;
- committed_size;
- worktree_size;
- ast_equal;
- string_literals_equal;
- imports_added;
- imports_removed;
- top_level_symbols_added;
- top_level_symbols_removed;
- changed_top_level_symbols;
- assigned_constants_changed;
- likely_load_bearing_categories.

Do not make an acceptance decision.

## E5 — source origin clues

Read-only Git/history inspection is allowed for only these two paths.

Create:

`DIRTY_SOURCE_ORIGIN_CLUES.md`

Include:

- `git log --oneline --decorate -10 -- <path>`;
- `git blame HEAD -- <path>` only for changed hunk context, not whole-file dump;
- whether the current worktree content exactly matches any blob reachable from local Git history, if determinable without network mutation;
- whether the dirty content textually matches source bytes found in any existing local `.aiassistant/reports/target` artifact, if determinable read-only.

Do not search external services.

## E6 — workspace invariance

Capture workspace before/after.

Require:

- HEAD unchanged;
- index unchanged/empty;
- both dirty source SHAs unchanged from E2;
- no source/config/migration/test mutation;
- no Railway access;
- no tests;
- no Git network action.

Generated export artifacts are allowed.

## forbidden

```text
source mutation:
0

git restore/reset/checkout/stash:
0

git stage/commit/push:
0

tests:
0

Railway access:
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

`LOAD_BEARING_DIRTY_SOURCE_EVIDENCE_EXPORTED / BROWSER_REVIEW_REQUIRED`

Possible blocker:

`DIRTY_SOURCE_EVIDENCE_PRECONDITION_CHANGED`

## export contract

Target ZIP must contain:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `DIRTY_SOURCE_DIFF.md`
- `LOAD_BEARING_SEMANTIC_DELTA.json`
- `DIRTY_SOURCE_ORIGIN_CLUES.md`
- `WORKSPACE_BEFORE.txt`
- `WORKSPACE_AFTER.txt`
- exact committed copies under `SOURCE_EVIDENCE/committed/...`
- exact worktree copies under `SOURCE_EVIDENCE/worktree/...`

Archive member paths must use POSIX `/`.

## final response

Report:

1. result
2. HEAD/origin identity
3. index state
4. committed/worktree hashes for both files
5. AST equality for both
6. changed top-level symbols
7. likely load-bearing categories
8. origin/history clues
9. source mutation = 0
10. tests = 0
11. Railway = 0
12. result ZIP SHA-256
13. next Browser gate = exact source review
