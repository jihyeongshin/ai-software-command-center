# 작업지시서: P3-3 L5 Two-File Git-Normalized Repair Persistence

## meta

- task_id: `20260917_1601_aiscc-p3-3-public-live-l5-two-file-git-normalized-repair-persistence-1`
- created_at: `2026-09-17 KST`
- work_type: `GIT_PERSISTENCE_RETRY`
- evidence_profile: `NARROW_PERSISTENCE`
- expected_HEAD: `dc73fe8c7cbdaee176124dfd71f3ac9d76e8eeb6`
- predecessor_result_zip_sha256: `fce07684a9350c5974b0035a593146c7b4964acce263b19054267915384fb430`

Use the current IDE Executor conversation.

This Task is persistence only.

The two source files remain Browser-substantively ACCEPTED.

The predecessor stop occurred only because Git's clean filter converted CRLF sequences to LF in the index.

## P0 — retained-index preflight

Require:

```text
HEAD == dc73fe8c7cbdaee176124dfd71f3ac9d76e8eeb6
origin/main == dc73fe8c7cbdaee176124dfd71f3ac9d76e8eeb6
index path count == 18
```

Read the predecessor result's `STAGED_PATHS.txt` and verify the current staged path set is exactly those 18 paths.

Do NOT unstage/restage the existing index if it matches.

If the index differs:

`PERSISTENCE_RETRY_INDEX_IDENTITY_MISMATCH`

and STOP.

## P1 — raw worktree source identity

Verify current worktree bytes remain exactly:

```text
src/aiscc/public_live/luna_profile.py
SHA-256:
e7dfbf5fac42b8fdff4766a7e09a8a4c1cda6a52cf6e4a3c0827d0fbb30196cb
size:
6826

src/aiscc/public_live/provider_authority.py
SHA-256:
98f3e83662a410e1dae15e7dfe487bb15830f4be80920031c8bf12b43b5e5d0d
size:
6752
```

Do not edit, format, normalize, checkout, restore, or rewrite either worktree file.

## P2 — canonical Git source identity

Read `SOURCE_NORMALIZATION_IDENTITY.json`.

Verify the currently staged index bytes are exactly:

```text
src/aiscc/public_live/luna_profile.py
SHA-256:
bb90ad7337045e5cea3006b52a39e04ce28f16b1fbdf47b26c6db7210b9199a4
size:
6688

src/aiscc/public_live/provider_authority.py
SHA-256:
b3a8373c5ea1bbdb61efe999643aef0412687a2171849d1dc1fc48982cbaf851
size:
6673
```

For each file independently prove:

```text
index_bytes == worktree_bytes.replace(b"\r\n", b"\n")
```

Also require:

- no other byte transformation;
- UTF-8 parse succeeds;
- Python AST of worktree and index text is identical;
- ordered string literal values are identical.

If any condition fails:

`UNEXPECTED_GIT_FILTER_TRANSFORMATION`

and STOP.

This Task explicitly accepts these LF-normalized index bytes as the canonical Git representation.

Do NOT change `.gitattributes` or Git configuration.

## P3 — add only retry governance

Read `NEW_GOVERNANCE_MANIFEST.json` and `payload/**`.

For each of its 3 files:

- verify payload SHA/size;
- canonical destination absent or byte-identical;
- copy exact bytes if absent;
- stage exact path.

At terminal completion move this Task to:

`.aiassistant/tasks/done/20260917_1601_aiscc-p3-3-public-live-l5-two-file-git-normalized-repair-persistence-1.md`

Stage the done Task and not the active copy.

Final staged count must be exactly:

```text
18 retained predecessor paths
+ 3 new governance paths
+ 1 current Task done
= 22
```

## P4 — final staged verification

Verify exact 22-path allowlist.

Require:

- both raw worktree source hashes unchanged;
- both staged source blobs equal the canonical normalized SHA values;
- all 20 governance/task blobs exact to their expected source bytes;
- no active Task staged;
- no reports/target staged;
- no cache/pyc/IDE artifacts staged.

Run:

`git diff --cached --check`

It MUST PASS because the index source blobs are LF-normalized.

Run staged secret scan without printing secret values.

If any extra/missing staged path exists:

`GIT_STAGING_SET_MISMATCH`

and STOP.

## P5 — commit

Create exactly one commit:

`fix: persist omitted public live runtime owners`

Requirements:

- parent exactly `dc73fe8c7cbdaee176124dfd71f3ac9d76e8eeb6`;
- no amend;
- no merge;
- no source mutation;
- all 22 staged paths committed.

## P6 — committed-tree verification

After commit verify:

```text
git show HEAD:src/aiscc/public_live/luna_profile.py
SHA-256 = bb90ad7337045e5cea3006b52a39e04ce28f16b1fbdf47b26c6db7210b9199a4

git show HEAD:src/aiscc/public_live/provider_authority.py
SHA-256 = b3a8373c5ea1bbdb61efe999643aef0412687a2171849d1dc1fc48982cbaf851
```

Also verify:

- raw worktree files still have the previously accepted CRLF-containing SHA values;
- Git status reports the two source paths clean after filtering;
- index empty;
- governance identities exact.

The committed LF blobs and unchanged CRLF-containing worktree bytes are expected to coexist under the repository's active clean/smudge behavior.

## P7 — push

Run once:

`git push origin HEAD:main`

No force / force-with-lease.

If push fails:

- preserve local commit;
- do not pull/rebase/merge/reset;
- report `LOCAL_NORMALIZED_REPAIR_COMMIT_PERSISTED / PUSH_BLOCKED`.

If push succeeds:

`LOCAL_NORMALIZED_REPAIR_COMMIT_AND_REMOTE_PERSISTED`

Verify `origin/main` resolves to the new commit if possible.

## no tests

Do NOT run unit/integration/full tests, Ruff, formatter, or mypy.

This is persistence-only after accepted source recovery.

## forbidden

```text
worktree source mutation:
0

.gitattributes mutation:
0

persistent Git config mutation:
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

`LOCAL_NORMALIZED_REPAIR_COMMIT_AND_REMOTE_PERSISTED`

Allowed:

`LOCAL_NORMALIZED_REPAIR_COMMIT_PERSISTED / PUSH_BLOCKED`

Possible blockers:

- `PERSISTENCE_RETRY_INDEX_IDENTITY_MISMATCH`
- `UNEXPECTED_GIT_FILTER_TRANSFORMATION`
- `GIT_STAGING_SET_MISMATCH`

## export

Create target ZIP containing:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `NORMALIZED_REPAIR_PERSISTENCE_PROOF.md`
- `STAGED_PATHS.txt`
- `COMMIT_TREE_SOURCE_IDENTITY.json`
- `GOVERNANCE_COMMIT_IDENTITY.json`
- `WORKSPACE_BEFORE.txt`
- `WORKSPACE_AFTER.txt`

## final response

Report:

1. result
2. pre-commit HEAD/origin
3. retained predecessor index 18/18
4. raw worktree source identity 2/2
5. canonical normalized index identity 2/2
6. exact CRLF→LF-only proof
7. AST/string equivalence
8. final staged count 22
9. diff-check
10. secret scan
11. commit SHA
12. commit parent
13. commit message
14. committed source canonical identity 2/2
15. raw worktree source identity after commit 2/2
16. Git status for two source paths
17. governance committed identity
18. index state
19. push result
20. remote ref
21. tests run = false
22. Railway/OpenAI/Cloudflare = 0
23. Public admission = DISABLED
24. Public Live = NOT_RELEASED
25. result ZIP SHA-256
