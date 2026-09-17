# 작업지시서: P3-3 L5 Git Persistence CRLF-Aware Retry

## meta

- task_id: `20260917_1504_aiscc-p3-3-public-live-l5-git-persistence-crlf-aware-retry-1`
- created_at: `2026-09-17 KST`
- work_type: `GIT_PERSISTENCE_RETRY`
- evidence_profile: `NARROW_PERSISTENCE`
- expected_HEAD: `96a4029ec3a82c9b2a88b9718732aa0f00ecad20`
- predecessor_result_zip_sha256: `3a041fb58a65f39f3bf0b36507a23ed42004bd5d9441294fda51109552910faa`
- accepted_local_result_zip_sha256: `d0b5f4f479e47b16df85a995344648a8e79a71453c8009153d92de220357c004`

Use the current IDE Executor conversation.

This is a Git persistence retry only.

The local implementation remains Browser-substantively ACCEPTED.

Do NOT modify source, tests, migrations, config, line endings, `.gitattributes`, or Git configuration.

## R1 — preflight from retained index

Expected current repository state from the accepted stop:

```text
HEAD == 96a4029ec3a82c9b2a88b9718732aa0f00ecad20
index_count == 113
local commit == none
```

Read:

- `PREDECESSOR_STAGED_PATHS.txt`
- `PREDECESSOR_SOURCE_INDEX_IDENTITY.json`
- `PREDECESSOR_GOVERNANCE_INDEX_IDENTITY.json`

Verify the current staged path set is EXACTLY the 113 paths in `PREDECESSOR_STAGED_PATHS.txt`.

Verify current index blobs:

- accepted source: `41 / 41` exact SHA + size PASS;
- predecessor governance: `71 / 71` exact SHA + size PASS;
- predecessor 1331 Task done blob remains present and exact.

If the current index differs, STOP:

`PERSISTENCE_RETRY_INDEX_IDENTITY_MISMATCH`

Do not unstage/restage accepted source to repair it.

## R2 — accepted CRLF exception

The following accepted source blobs intentionally contain authoritative CRLF bytes:

```text
src/aiscc/providers/openai_responses.py
src/aiscc/providers/service.py
src/aiscc/security/policy.py
```

Their exact accepted SHA values MUST remain unchanged.

Do NOT normalize them to LF.

Do NOT edit `.gitattributes`.

Do NOT run `git config` to persist a whitespace setting.

### diagnostic plain check

Run:

`git diff --cached --check`

It may exit non-zero ONLY because of CR-at-EOL warnings in the exact three paths above.

Capture the diagnostic.

If it reports any issue in another path or any whitespace class not attributable solely to those accepted CRLF EOLs:

`UNEXPECTED_STAGED_WHITESPACE_DEFECT`

and STOP.

### authoritative persistence check

Run exactly:

`git -c core.whitespace=cr-at-eol diff --cached --check`

This MUST PASS.

This command-local override is explicitly authorized by Browser Command Center for this persistence attempt.

It does not change repository or user Git configuration.

## R3 — add retry governance only

Read `NEW_GOVERNANCE_MANIFEST.json` and `payload/**`.

For each of its three files:

- verify payload SHA + size;
- canonical destination must be absent or byte-identical;
- copy exact bytes if absent;
- stage exact path.

Move this current Task from active to:

`.aiassistant/tasks/done/20260917_1504_aiscc-p3-3-public-live-l5-git-persistence-crlf-aware-retry-1.md`

Stage the exact done Task.

Do not stage the active copy.

After this step the staged set must be exactly:

```text
113 predecessor paths
+ 3 new governance paths
+ 1 current Task done path
= 117 paths
```

No other path may be staged.

## R4 — final staged identity

Verify:

- staged path count = `117`;
- all predecessor 113 index blobs still exact;
- 3 new governance blobs exact;
- current Task done blob exact;
- accepted source 41/41 still exact;
- no `.aiassistant/reports/target/**`;
- no `.aiassistant/tasks/active/**`;
- no `__pycache__`, `.pyc`, IDE/build/runtime cache;
- no unrelated worktree residue staged.

Run again:

`git -c core.whitespace=cr-at-eol diff --cached --check`

MUST PASS.

Run secret scan on staged diff/names without printing secret values.

## R5 — commit

Create exactly one commit:

`feat: persist public live L5 local runtime`

Requirements:

- parent exactly `96a4029ec3a82c9b2a88b9718732aa0f00ecad20`;
- no amend;
- no merge;
- no source mutation before/after commit;
- all 117 staged paths committed.

## R6 — committed-tree verification

After commit verify:

- parent exact;
- 41 accepted source blobs exact accepted SHA;
- predecessor 71 governance blobs exact;
- predecessor 1331 Task done exact;
- 3 new governance blobs exact;
- current retry Task done exact;
- index empty;
- accepted source paths have no worktree differences.

Untracked `__pycache__` residue remains NON_BLOCKING and must not be staged.

## R7 — push

Run once:

`git push origin HEAD:main`

No force / no force-with-lease.

If push fails due auth/network/non-fast-forward:

- preserve local commit;
- do not pull/rebase/merge/reset;
- export result as `LOCAL_COMMIT_PERSISTED / PUSH_BLOCKED`.

If push succeeds:

`LOCAL_COMMIT_AND_REMOTE_PERSISTED`

If possible, verify remote `origin/main` resolves to the new commit without mutating repository state.

## no tests

Do NOT run tests.

Do NOT run formatter/linter/mypy.

This is persistence-only.

## forbidden

```text
source mutation:
0

line-ending normalization:
0

.gitattributes mutation:
0

persistent git config mutation:
0

Railway:
0

Cloudflare:
0

real OpenAI:
0

OpenAI key read/export:
0

Public admission enable:
0

Public Live release:
0
```

## expected result

Preferred:

`LOCAL_COMMIT_AND_REMOTE_PERSISTED`

Allowed:

`LOCAL_COMMIT_PERSISTED / PUSH_BLOCKED`

Blockers:

- `PERSISTENCE_RETRY_INDEX_IDENTITY_MISMATCH`
- `UNEXPECTED_STAGED_WHITESPACE_DEFECT`
- `GIT_STAGING_SET_MISMATCH`
- `ACCEPTED_SOURCE_IDENTITY_MISMATCH`

## export

Create one target ZIP containing:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `PERSISTENCE_PROOF.md`
- `STAGED_PATHS.txt`
- `COMMIT_TREE_SOURCE_IDENTITY.json`
- `GOVERNANCE_COMMIT_IDENTITY.json`
- `CRLF_WHITESPACE_CHECK_PROOF.md`
- `WORKSPACE_BEFORE.txt`
- `WORKSPACE_AFTER.txt`

No source re-export and no test evidence required.

## final response

Report:

1. result
2. pre-commit HEAD
3. predecessor index 113/113 verification
4. accepted source index 41/41
5. CRLF exact paths
6. plain diff-check diagnostic classification
7. command-local CRLF-aware diff-check result
8. final staged count 117
9. secret scan
10. commit SHA
11. commit parent
12. commit message
13. committed source identity 41/41
14. governance committed identity
15. index state
16. accepted-path worktree state
17. push result
18. remote ref verification
19. tests run = false
20. source mutation = 0
21. Railway/OpenAI/Cloudflare actions = 0
22. Public admission = DISABLED
23. Public Live = NOT_RELEASED
24. result ZIP SHA-256
