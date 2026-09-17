# 작업지시서: P3-3 L5 Accepted Source GitHub Publication Push

## meta

- task_id: `20260916_1610_aiscc-p3-3-public-live-l5-accepted-source-github-publication-push-1`
- created_at: `2026-09-16 KST`
- work_type: `GIT_REMOTE_PUBLICATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_HEAD: `96a4029ec3a82c9b2a88b9718732aa0f00ecad20`
- primary_semantic_owner: `P3-3 deployment source publication`

Use the current IDE Executor conversation. No fresh chat is required.

## objective

Publish the already accepted and persisted local source commit to the repository's existing GitHub default/upstream branch so Railway can later bind to that exact source.

This Task explicitly authorizes the narrow Git network actions below.

## mandatory preflight

Required local HEAD:

`96a4029ec3a82c9b2a88b9718732aa0f00ecad20`

Required commit message:

`feat: add hosted public live runtime boundary`

Require:

- index empty;
- no tracked product/source/config/test modification after the accepted commit;
- unrelated known untracked/cache residue may remain;
- current branch is a named local branch, not detached HEAD.

The newly delivered Cycle/Judgment/Handoff may be uncommitted governance files. They must not be staged or committed in this Task.

## remote identity

Read, but do not print credentials.

Verify:

1. remote `origin` exists;
2. origin host is `github.com`;
3. repository basename is exactly `ai-software-command-center`;
4. current branch has an existing upstream `origin/<same-branch>`;
5. remote symbolic HEAD/default branch resolves to that same branch.

Accept HTTPS or SSH remote syntax.

If any condition fails or is ambiguous:

`BLOCKED_REMOTE_IDENTITY_OR_BRANCH_AUTHORITY`

and STOP before push.

Do not change remote URLs or Git config.

## remote ancestry verification

Network read is explicitly authorized.

Use a bounded fetch/remote query sufficient to establish the current remote branch SHA.

Require:

```text
remote branch == HEAD
OR
remote branch is a strict ancestor of 96a4029ec3a82c9b2a88b9718732aa0f00ecad20
```

If remote is ahead or histories diverge:

`BLOCKED_NON_FAST_FORWARD_OR_REMOTE_DIVERGENCE`

and STOP.

Do not pull, merge, rebase, reset, cherry-pick or amend.

## push authorization

If all preflight and ancestry checks pass, authorize exactly one normal push equivalent to:

```text
git push origin HEAD:refs/heads/<verified-current-branch>
```

Requirements:

- no `--force`;
- no `--force-with-lease`;
- no tag push;
- no branch deletion;
- no new branch target;
- no GitHub release;
- no credential printed to console/report.

If authentication requires interactive Human login that cannot be safely completed in the current Executor environment:

`HUMAN_GITHUB_AUTH_REQUIRED`

and STOP without changing repository state.

## post-push proof

Verify with a remote read that:

```text
refs/heads/<verified-current-branch>
== 96a4029ec3a82c9b2a88b9718732aa0f00ecad20
```

Record:

- remote host class: GitHub;
- repository basename;
- local branch;
- upstream;
- remote default branch;
- pre-push remote SHA;
- post-push remote SHA;
- fast-forward relationship;
- push result.

Do not record credential/token/cookie values.

## repository integrity after push

Require:

- local HEAD unchanged at `96a4029ec3a82c9b2a88b9718732aa0f00ecad20`;
- commit count created by this Task = 0;
- index empty;
- accepted source/config/test bytes unchanged;
- no Git config mutation;
- no tracked product source mutation.

## forbidden external actions

```text
Railway source connection:
0

Railway deployment:
0

Railway variable/secret mutation:
0

Cloudflare mutation:
0

OpenAI/provider call:
0

Public admission enable:
0
```

## tests

No tests are required. This is remote publication of an already Browser-accepted commit.

Reuse accepted local evidence:

`1460 PASS / 3 existing SKIP / 0 FAIL / 0 ERROR`

## acceptable outcome

`COMPLETED / GITHUB_PUBLICATION_CANDIDATE`

Do not claim Railway deployment or L5 terminal acceptance.

## mandatory stop

- HEAD mismatch;
- commit message mismatch;
- tracked source mutation;
- origin is not the expected GitHub repository basename;
- missing/mismatched upstream;
- current branch differs from remote default branch;
- remote ahead/diverged;
- push would require force;
- credential disclosure would be required;
- any source/commit mutation would be required.

## export

Create:

`.aiassistant/reports/target/20260916_1610_aiscc-p3-3-public-live-l5-accepted-source-github-publication-push-1/`

Include:

- `EXECUTOR_REPORT.md`
- `GIT_REMOTE_PUBLICATION_EVIDENCE.md`
- `WORKSPACE_BEFORE.txt`
- `WORKSPACE_AFTER.txt`
- exact Task copy
- result ZIP

## final response

1. result
2. local HEAD
3. remote identity
4. local branch/upstream/default branch
5. pre-push remote SHA
6. ancestry verdict
7. push result
8. post-push remote SHA
9. local repository integrity
10. external actions
11. Public state
12. next Human Railway source-binding status
