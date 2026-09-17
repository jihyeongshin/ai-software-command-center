# 작업지시서: P3-3 L5 Two-File Source Repair Git Persistence

## meta

- task_id: `20260917_1553_aiscc-p3-3-public-live-l5-two-file-source-repair-git-persistence-1`
- created_at: `2026-09-17 KST`
- work_type: `GIT_PERSISTENCE_REPAIR`
- evidence_profile: `NARROW_PERSISTENCE`
- expected_HEAD: `dc73fe8c7cbdaee176124dfd71f3ac9d76e8eeb6`
- accepted_recovery_result_zip_sha256: `901597b5cd27242b2ae32709cb15491790d3eca8af25d3a3dd17b8b25d491874`
- accepted_recovery_source_count: `2`

Use the current IDE Executor conversation.

This Task is Git persistence only.

The exact two source files are already Browser-substantively ACCEPTED.

## P0 — preflight

Require:

```text
HEAD == dc73fe8c7cbdaee176124dfd71f3ac9d76e8eeb6
origin/main == dc73fe8c7cbdaee176124dfd71f3ac9d76e8eeb6
index == empty
```

Do not require a globally clean worktree.

Ignore unstaged generated cache residue.

If HEAD or origin differs:

`REPAIR_PERSISTENCE_HEAD_MISMATCH`

and STOP.

## P1 — exact source identity

Read `ACCEPTED_RECOVERY_SOURCE_INVENTORY.json`.

Verify current worktree exact bytes:

```text
src/aiscc/public_live/luna_profile.py
SHA-256 = e7dfbf5fac42b8fdff4766a7e09a8a4c1cda6a52cf6e4a3c0827d0fbb30196cb
size = 6826

src/aiscc/public_live/provider_authority.py
SHA-256 = 98f3e83662a410e1dae15e7dfe487bb15830f4be80920031c8bf12b43b5e5d0d
size = 6752
```

Require `2 / 2 PASS`.

Do NOT edit, format, normalize, restore, or rewrite either file.

If mismatch:

`ACCEPTED_RECOVERY_SOURCE_IDENTITY_MISMATCH`

and STOP.

## P2 — governance payload

Read `GOVERNANCE_REPAIR_MANIFEST.json`.

For every `payload/<canonical path>`:

- verify payload SHA and size;
- if canonical destination absent: copy exact bytes;
- if destination exists and bytes identical: reuse;
- if destination exists and differs: `GOVERNANCE_REPAIR_CONFLICT` and STOP.

The manifest contains accumulated 1524/1531/1541 Browser provenance plus this recovery acceptance provenance.

Do not rewrite content.

## P3 — current Task done

At terminal completion move the current Task from active to:

`.aiassistant/tasks/done/20260917_1553_aiscc-p3-3-public-live-l5-two-file-source-repair-git-persistence-1.md`

Stage the done copy, not the active copy.

## P4 — exact staging allowlist

Stage ONLY:

- the exact 2 accepted source paths;
- every path in `GOVERNANCE_REPAIR_MANIFEST.json`;
- `.aiassistant/tasks/done/20260917_1553_aiscc-p3-3-public-live-l5-two-file-source-repair-git-persistence-1.md`.

Expected final staged count:

```text
2 accepted source
+ 15 governance payload
+ 1 current Task done
= 18
```

Do NOT use `git add .` or `git add -A`.

Do NOT stage:

- `.aiassistant/reports/target/**`;
- `.aiassistant/tasks/active/**`;
- `__pycache__/**`;
- `.pyc`;
- IDE/build/cache residue;
- unrelated files.

## P5 — staged source byte identity

After staging, verify the Git index blob content for both source paths is byte-identical to the accepted source inventory.

If a Git clean filter or line-ending normalization changes the staged blob:

`GIT_CLEAN_FILTER_SOURCE_IDENTITY_CONFLICT`

and STOP.

Do NOT change Git config or `.gitattributes` to force acceptance.

## P6 — staged verification

Before commit verify:

- staged path set equals the exact allowlist;
- both staged source blobs exact accepted bytes;
- all governance blobs exact manifest bytes;
- current Task done blob exact;
- `git diff --cached --check` PASS;
- secret scan on staged changes PASS without printing secret values;
- no target/cache/active Task staged.

If any extra/missing path:

`GIT_STAGING_SET_MISMATCH`

and STOP.

## P7 — commit

Create exactly one commit:

`fix: persist omitted public live runtime owners`

Requirements:

- parent exactly `dc73fe8c7cbdaee176124dfd71f3ac9d76e8eeb6`;
- no amend;
- no merge;
- no source mutation;
- no tests.

## P8 — committed-tree verification

After commit verify:

- parent == `dc73fe8c7cbdaee176124dfd71f3ac9d76e8eeb6`;
- both source blobs exact accepted bytes;
- all governance manifest blobs exact;
- current Task done present;
- index empty;
- the two accepted source paths have no worktree diff.

Untracked cache residue is NON_BLOCKING.

## P9 — push

Run once:

`git push origin HEAD:main`

No force / force-with-lease.

If push fails:

- preserve local commit;
- do not pull/rebase/merge/reset;
- report `LOCAL_REPAIR_COMMIT_PERSISTED / PUSH_BLOCKED`.

If push succeeds:

`LOCAL_REPAIR_COMMIT_AND_REMOTE_PERSISTED`

Verify `origin/main` resolves to the new commit if possible.

## no tests

Do NOT run unit, integration, full repository, Ruff, formatter, or mypy.

The two source files were already accepted under the 1541 recovery evidence.

## forbidden

```text
source mutation:
0

Railway:
0

Cloudflare:
0

OpenAI:
0

Public admission enable:
0

Public Live release:
0
```

## expected result

Preferred:

`LOCAL_REPAIR_COMMIT_AND_REMOTE_PERSISTED`

Allowed:

`LOCAL_REPAIR_COMMIT_PERSISTED / PUSH_BLOCKED`

## export

Create target ZIP containing:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `REPAIR_PERSISTENCE_PROOF.md`
- `STAGED_PATHS.txt`
- `COMMIT_TREE_SOURCE_IDENTITY.json`
- `GOVERNANCE_COMMIT_IDENTITY.json`
- `WORKSPACE_BEFORE.txt`
- `WORKSPACE_AFTER.txt`

No source re-export and no test evidence required.

## final response

Report:

1. result
2. pre-commit HEAD/origin
3. accepted source identity 2/2
4. governance payload count/identity
5. final staged path count
6. staged source byte identity
7. cached/generated exclusions
8. diff-check
9. secret scan
10. commit SHA
11. commit parent
12. commit message
13. committed source identity 2/2
14. governance committed identity
15. index state
16. source worktree state
17. push result
18. remote ref
19. tests run = false
20. source mutation = 0
21. Railway/OpenAI/Cloudflare = 0
22. Public admission = DISABLED
23. Public Live = NOT_RELEASED
24. result ZIP SHA-256
