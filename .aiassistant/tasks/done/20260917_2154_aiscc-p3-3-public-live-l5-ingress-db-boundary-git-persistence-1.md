# 작업지시서: P3-3 L5 Ingress DB Boundary Git Persistence

## meta

- task_id: `20260917_2154_aiscc-p3-3-public-live-l5-ingress-db-boundary-git-persistence-1`
- created_at: `2026-09-17 KST`
- work_type: `GIT_PERSISTENCE`
- evidence_profile: `NARROW_PERSISTENCE`
- expected_HEAD: `baed7ea3360f6c67c0409c25f84137ab446b90ac`
- accepted_result_zip_sha256: `3f4fec14cf632374f205eded48afd0e92dcc4e516662840b816a0ab327b9ff61`
- accepted_source_count: `3`

Use the current IDE Executor conversation.

This Task is persistence only.

The ingress DB least-privilege source candidate is already Browser-substantively ACCEPTED.

## P0 — preflight

Require:

```text
HEAD == baed7ea3360f6c67c0409c25f84137ab446b90ac
origin/main == baed7ea3360f6c67c0409c25f84137ab446b90ac
index == empty
```

Do not require a globally clean worktree.

The three accepted source paths are expected to be unstaged changes.

Generated cache/target residue is non-blocking and must not be staged.

If HEAD/origin/index differs:

`INGRESS_PERSISTENCE_PREFLIGHT_MISMATCH`

and STOP.

## P1 — exact accepted source identity

Read `ACCEPTED_SOURCE_INVENTORY.json`.

Verify current worktree exact SHA-256 and byte size for all three paths.

Require:

`3 / 3 PASS`

Do not modify, format, normalize, restore, or rewrite source.

If any source differs:

`ACCEPTED_INGRESS_SOURCE_IDENTITY_MISMATCH`

and STOP.

## P2 — governance payload placement

Read `GOVERNANCE_PERSISTENCE_MANIFEST.json`.

For each `payload/<canonical path>`:

- verify payload SHA and size;
- if canonical destination is absent: copy exact bytes;
- if destination exists and bytes are identical: reuse;
- if destination exists and differs: `GOVERNANCE_PERSISTENCE_CONFLICT` and STOP.

Do not rewrite governance content.

The payload contains the accumulated unpersisted Browser provenance for:

- source-repair persistence → Phase A entry;
- Hosted Phase A acceptance → Phase B entry;
- Hosted Phase B acceptance → ingress DB rework entry;
- current ingress DB boundary final acceptance.

## P3 — current Task done

At terminal completion move this Task to:

`.aiassistant/tasks/done/20260917_2154_aiscc-p3-3-public-live-l5-ingress-db-boundary-git-persistence-1.md`

Stage the done copy only.

Do not stage the active copy.

## P4 — exact staging allowlist

Stage ONLY:

1. the 3 exact accepted source paths;
2. every canonical governance path in `GOVERNANCE_PERSISTENCE_MANIFEST.json`;
3. `.aiassistant/tasks/done/20260917_2154_aiscc-p3-3-public-live-l5-ingress-db-boundary-git-persistence-1.md`.

Expected final staged count:

```text
3 accepted source
+ 15 governance
+ 1 current Task done
= 19
```

Do NOT use:

- `git add .`
- `git add -A`

Do NOT stage:

- `.aiassistant/tasks/active/**`;
- `.aiassistant/reports/target/**`;
- cache/pyc/IDE/build artifacts;
- unrelated dirty/untracked files.

## P5 — staged byte identity

After staging verify:

- all 3 Git index blobs exactly equal `ACCEPTED_SOURCE_INVENTORY.json`;
- all governance blobs exactly equal `GOVERNANCE_PERSISTENCE_MANIFEST.json`;
- current Task done blob equals this package's Task bytes.

The accepted source files are LF-only. Any clean-filter byte change is unexpected.

If any staged source blob differs:

`GIT_INDEX_SOURCE_IDENTITY_MISMATCH`

and STOP.

## P6 — final staged verification

Require:

- staged path count == `19`;
- exact staged path set == allowlist;
- `git diff --cached --check` PASS;
- staged secret scan PASS without printing secret values;
- no active Task/target/cache staged.

If staged set differs:

`GIT_STAGING_SET_MISMATCH`

and STOP.

## P7 — commit

Create exactly one commit:

`fix: isolate public live ingress database authority`

Requirements:

- parent exactly `baed7ea3360f6c67c0409c25f84137ab446b90ac`;
- no amend;
- no merge;
- no source mutation after byte verification.

## P8 — committed-tree verification

After commit verify:

- parent exact;
- all 3 committed source blobs exact accepted SHA + size;
- all governance manifest blobs exact;
- current Task done present;
- index empty;
- accepted source paths have no worktree diff.

Generated untracked residue is non-blocking.

## P9 — push

Run exactly one non-force push:

`git push origin HEAD:main`

No force / force-with-lease.

If push fails:

- preserve local commit;
- do not pull/rebase/merge/reset;
- result `LOCAL_INGRESS_BOUNDARY_COMMIT_PERSISTED / PUSH_BLOCKED`.

If push succeeds:

`LOCAL_INGRESS_BOUNDARY_COMMIT_AND_REMOTE_PERSISTED`

Verify `origin/main` resolves to the new commit if possible.

## no tests / no hosted mutation

Do NOT run tests, Ruff, formatter, or mypy.

Do NOT access or mutate Railway.

Do NOT call OpenAI.

Do NOT modify Cloudflare.

Do NOT deploy Public ingress.

Do NOT enable Public admission.

## expected result

Preferred:

`LOCAL_INGRESS_BOUNDARY_COMMIT_AND_REMOTE_PERSISTED`

Allowed:

`LOCAL_INGRESS_BOUNDARY_COMMIT_PERSISTED / PUSH_BLOCKED`

Possible blockers:

- `INGRESS_PERSISTENCE_PREFLIGHT_MISMATCH`
- `ACCEPTED_INGRESS_SOURCE_IDENTITY_MISMATCH`
- `GOVERNANCE_PERSISTENCE_CONFLICT`
- `GIT_INDEX_SOURCE_IDENTITY_MISMATCH`
- `GIT_STAGING_SET_MISMATCH`

## export

Create target ZIP containing:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `PERSISTENCE_PROOF.md`
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
3. accepted source identity 3/3
4. governance payload count/identity
5. final staged count
6. staged source byte identity
7. diff-check
8. secret scan
9. commit SHA
10. commit parent
11. commit message
12. committed source identity 3/3
13. governance committed identity
14. index state
15. accepted-source worktree state
16. push result
17. remote ref
18. tests run = false
19. Railway/OpenAI/Cloudflare actions = 0
20. Public ingress = NOT_DEPLOYED
21. Public admission = DISABLED
22. Public Live = NOT_RELEASED
23. result ZIP SHA-256
