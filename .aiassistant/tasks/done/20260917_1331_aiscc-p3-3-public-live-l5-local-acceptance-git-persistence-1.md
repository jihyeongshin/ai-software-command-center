# 작업지시서: P3-3 L5 Local Acceptance Git Persistence

## meta

- task_id: `20260917_1331_aiscc-p3-3-public-live-l5-local-acceptance-git-persistence-1`
- created_at: `2026-09-17 KST`
- work_type: `GIT_PERSISTENCE`
- evidence_profile: `NARROW_PERSISTENCE`
- expected_HEAD: `96a4029ec3a82c9b2a88b9718732aa0f00ecad20`
- accepted_result_zip_sha256: `d0b5f4f479e47b16df85a995344648a8e79a71453c8009153d92de220357c004`
- accepted_source_count: `41`

Use the current IDE Executor conversation.

This Task performs persistence only.

The local Public Live implementation is already Browser-substantively ACCEPTED.

## mandatory input

From the Command Center ZIP, place/read:

- `ACCEPTED_SOURCE_INVENTORY.json`
- `GOVERNANCE_PERSISTENCE_MANIFEST.json`
- `payload/**`

The Task itself goes to `.aiassistant/tasks/active/` first and to `.aiassistant/tasks/done/` at terminal completion.

## P1 — preflight

Verify:

```text
HEAD == 96a4029ec3a82c9b2a88b9718732aa0f00ecad20
index == empty
```

Do not require a globally clean worktree.

Generated `__pycache__` or similar local residue is not a substantive blocker and must never be staged.

If HEAD differs:

`PERSISTENCE_HEAD_MISMATCH`

and STOP.

## P2 — exact accepted source identity

Read `ACCEPTED_SOURCE_INVENTORY.json`.

For all 41 entries verify current worktree:

- exact project-relative path exists;
- SHA-256 exact;
- byte size exact.

Require:

`41 / 41 PASS`

If any differs:

`ACCEPTED_SOURCE_IDENTITY_MISMATCH`

and STOP.

Do not modify source to make it match.

## P3 — governance payload placement

Read `GOVERNANCE_PERSISTENCE_MANIFEST.json`.

For each listed `payload/<canonical-path>`:

- verify payload SHA/size;
- if canonical destination absent: copy exact bytes;
- if destination exists and bytes identical: reuse;
- if destination exists and differs: `GOVERNANCE_PERSISTENCE_CONFLICT` and STOP.

No content rewriting.

This includes the current Browser acceptance Cycle/Judgment/Handoff and the 2012 provenance reconciliation.

## P4 — current Task done record

At terminal execution, move the current Task from active to:

`.aiassistant/tasks/done/20260917_1331_aiscc-p3-3-public-live-l5-local-acceptance-git-persistence-1.md`

Stage that exact done Task as governance provenance.

Do not stage the active copy.

## P5 — exact staging allowlist

Stage ONLY:

1. the 41 exact paths in `ACCEPTED_SOURCE_INVENTORY.json`;
2. every canonical path in `GOVERNANCE_PERSISTENCE_MANIFEST.json`;
3. `.aiassistant/tasks/done/20260917_1331_aiscc-p3-3-public-live-l5-local-acceptance-git-persistence-1.md`.

Do NOT stage:

- `.aiassistant/reports/target/**`;
- `.aiassistant/tasks/active/**`;
- `__pycache__/**`;
- `.pyc`;
- IDE/build/runtime cache;
- Downloads artifacts;
- unrelated dirty/untracked files.

Do not use `git add -A` or `git add .`.

Use exact pathspecs/manifest-driven staging.

## P6 — staged verification

Before commit:

- staged path set must equal the exact allowlist above;
- every staged accepted source blob must equal its accepted SHA;
- every staged governance blob must equal manifest SHA;
- current Task done blob must equal the Task received from this package;
- `git diff --cached --check` PASS;
- no secret/key/token material newly staged;
- no target bundle/cache staged.

If staged set has any extra or missing path:

`GIT_STAGING_SET_MISMATCH`

and STOP.

## P7 — commit

Create exactly one commit.

Commit message:

`feat: persist public live L5 local runtime`

No amend.

No merge commit.

No source mutation after staging verification.

## P8 — committed-tree verification

After commit verify:

- commit parent == `96a4029ec3a82c9b2a88b9718732aa0f00ecad20`;
- all 41 accepted source blobs equal accepted SHA;
- all governance manifest blobs equal manifest SHA;
- current Task done record is present;
- index empty;
- no accepted-path worktree difference.

Generated local cache residue may remain untracked and is NON_BLOCKING.

## P9 — push

Authorize one non-force push:

`git push origin HEAD:main`

No force, no force-with-lease.

If rejected/non-fast-forward/auth/network failure:

- preserve the local commit;
- report exact blocker;
- do not reset/rebase/merge/pull;
- result `LOCAL_COMMIT_PERSISTED / PUSH_BLOCKED`.

If push succeeds:

`LOCAL_COMMIT_AND_REMOTE_PERSISTED`

## no tests

Do NOT rerun unit/integration/full repository tests.

This is byte-identity Git persistence after accepted evidence.

Only Git/hash/static staging verification is required.

## external prohibitions

```text
Railway mutation:
0

Cloudflare mutation:
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

- `PERSISTENCE_HEAD_MISMATCH`
- `ACCEPTED_SOURCE_IDENTITY_MISMATCH`
- `GOVERNANCE_PERSISTENCE_CONFLICT`
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

No need to re-export all accepted source files; the accepted source bundle is already Browser-admitted and the commit-tree identity proof is the persistence evidence.

## final response

Report:

1. result
2. pre-commit HEAD
3. accepted source identity 41/41
4. governance payload identity
5. exact staged path count
6. cached/generated exclusions
7. `git diff --cached --check`
8. secret scan
9. commit SHA
10. commit parent
11. commit message
12. committed source identity 41/41
13. governance committed identity
14. index state
15. accepted-path worktree state
16. push result
17. remote ref if verified
18. tests run = false
19. Railway/OpenAI/Cloudflare actions = 0
20. Public admission = DISABLED
21. Public Live = NOT_RELEASED
22. result ZIP SHA-256
