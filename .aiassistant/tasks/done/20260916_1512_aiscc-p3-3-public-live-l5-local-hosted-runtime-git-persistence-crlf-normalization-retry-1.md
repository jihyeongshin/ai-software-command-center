# 작업지시서: P3-3 L5 Local Hosted Runtime Git Persistence — CRLF Normalization Retry

## meta

- task_id: `20260916_1512_aiscc-p3-3-public-live-l5-local-hosted-runtime-git-persistence-crlf-normalization-retry-1`
- created_at: `2026-09-16 KST`
- work_type: `GIT_PERSISTENCE_REWORK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_starting_HEAD: `04436a11adc6dd6e70b4a98568fe878cc4c9f4aa`
- predecessor_result_zip_sha256: `855d73c247013c66f140ff6d4abfbff685bb66d4055461a9663ed0ed55266e8d`
- expected_initial_index_path_count: `42`
- expected_final_commit_path_count: `46`
- commit_message: `feat: add hosted public live runtime boundary`

Use the current IDE Executor conversation. No fresh chat is required.

## current state

```text
L5 local implementation:
BROWSER_ACCEPTED_CANDIDATE

1459 persistence:
BLOCKED / NO COMMIT

normalization policy:
RESOLVED_BY_COMMAND_CENTER

Human Railway deployment:
WAITING_FOR_PERSISTENCE

Public admission:
DISABLED

Public Live:
NOT_RELEASED
```

## mandatory preflight

Starting HEAD must equal:

`04436a11adc6dd6e70b4a98568fe878cc4c9f4aa`

Unlike the predecessor Task, the index MUST NOT be empty.

Expected current index:

`42 exact predecessor allowlisted paths`

Read predecessor evidence:

`.aiassistant/reports/target/20260916_1459_aiscc-p3-3-public-live-l5-local-hosted-runtime-git-persistence-1/`

Verify:

- `STAGED_PATHS.txt`
- `ALLOWLIST.json`
- `SOURCE_HASH_VERIFICATION.json`
- `WORKSPACE_AFTER.txt`
- `EXECUTOR_REPORT.md`

The current index names must exactly equal predecessor `ALLOWLIST.json`.

If not:

`DOCUMENT_CONTRACT_MISMATCH`

and STOP.

Do not unstage/reset/restage those 42 paths.

## accepted source raw-byte identity

The 17 accepted source/config/test worktree paths must still match their 1430 accepted SHA-256 values exactly.

Reuse the expected values from predecessor:

`SOURCE_HASH_VERIFICATION.json`

Required:

`17 / 17 worktree_pass`

Any mismatch:

STOP.

## explicit Git newline canonicalization rule

The predecessor's raw index-SHA == raw worktree-SHA requirement is superseded by this Task.

For every final staged text path, read:

```text
W = raw worktree bytes
I = raw index blob bytes
```

PASS only if one of:

```text
A:
I == W

B:
I == W with every CRLF byte sequence replaced by LF
```

For B additionally require:

- W actually contains at least one CRLF;
- I contains no CRLF at those converted positions;
- every other byte is identical;
- no decoding/re-encoding/substitution;
- no BOM insertion/removal;
- no whitespace transformation other than CR byte removal from CRLF pairs.

Record per-path classification:

`EXACT_BYTES | CRLF_TO_LF_ONLY`

Anything else:

STOP.

Do not use a text parser or semantic AST equality as substitute.

## all 42 predecessor staged paths

Run the above raw-byte/index-blob comparison for all existing 42 staged paths.

The 13 previously known source/config/test CRLF-normalized paths are:

- `src/aiscc/providers/openai_responses.py`
- `src/aiscc/providers/service.py`
- `src/aiscc/public_live/luna_profile.py`
- `src/aiscc/runtime/docker.py`
- `tests/fixtures/providers/luna_capabilities.py`
- `src/aiscc/providers/hosted_secret.py`
- `tests/unit/providers/test_hosted_secret.py`
- `config/deployment/public-live-railway.v1.toml`
- `tests/integration/providers/test_hosted_secret_durable.py`
- `src/aiscc/security/policy.py`
- `src/aiscc/public_live/provider_authority.py`
- `tests/unit/public_live/test_context_authority.py`
- `tests/runtime/security/test_hosted_container_secret.py`

Do not assume only these 13 paths can be normalized.

Governance paths must be checked by the same exact rule.

## no repository EOL policy mutation

Forbidden:

- `.gitattributes` change;
- `.gitignore` change;
- `git config` mutation;
- global Git config mutation;
- source line-ending rewrite;
- checkout/reset intended to change EOL;
- broad restaging.

Observed `core.autocrlf=true` may be recorded but must not be changed.

## inbound retry governance

Place canonical artifacts:

- TASK → `.aiassistant/tasks/active/20260916_1512_aiscc-p3-3-public-live-l5-local-hosted-runtime-git-persistence-crlf-normalization-retry-1.md`
- CYCLE → `.aiassistant/records/aiscc/cycles/20260916_1512_aiscc-p3-3-public-live-l5-git-persistence-blocked-crlf-index-normalization-retry-entry-1.cycle.md`
- JUDGMENT → `.aiassistant/reports/aiscc/20260916_1512_aiscc-browser-command-center-l5-git-persistence-crlf-index-normalization-resolution-1.md`
- HANDOFF → `.aiassistant/reports/aiscc/20260916_1512_aiscc-browser-command-center-l5-git-persistence-crlf-normalization-retry-handoff-1.md`

Read the Task.

At completion, move Task exact bytes to:

`.aiassistant/tasks/done/20260916_1512_aiscc-p3-3-public-live-l5-local-hosted-runtime-git-persistence-crlf-normalization-retry-1.md`

Active copy must be absent.

## stage only four new paths

The predecessor 42 are already staged.

Use exact-path `git add` only for these four:

- `.aiassistant/records/aiscc/cycles/20260916_1512_aiscc-p3-3-public-live-l5-git-persistence-blocked-crlf-index-normalization-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260916_1512_aiscc-browser-command-center-l5-git-persistence-crlf-index-normalization-resolution-1.md`
- `.aiassistant/reports/aiscc/20260916_1512_aiscc-browser-command-center-l5-git-persistence-crlf-normalization-retry-handoff-1.md`
- `.aiassistant/tasks/done/20260916_1512_aiscc-p3-3-public-live-l5-local-hosted-runtime-git-persistence-crlf-normalization-retry-1.md`

Forbidden:

- `git add .`
- `git add -A`
- broad glob
- reset/unstage of predecessor paths
- cache cleanup as a gate

## final stage gate

Before commit:

```text
git diff --cached --name-only
```

must contain exactly:

`46 paths`

Expected composition:

```text
17 accepted source/config/test
21 accumulated governance
3 prior 1459 acceptance governance
1 prior 1459 persistence Task
3 current retry governance
1 current retry Task
= 46
```

No cache/runtime residue.

For all 46, produce:

`GIT_CANONICALIZATION_VERIFICATION.json`

with:

- path;
- worktree SHA-256;
- index SHA-256;
- worktree CRLF count;
- index CRLF count;
- classification `EXACT_BYTES | CRLF_TO_LF_ONLY`;
- pass boolean.

For the 17 accepted source/config/test paths also include:

- 1430 accepted SHA-256;
- raw worktree identity pass.

## commit

Create exactly one commit:

`feat: add hosted public live runtime boundary`

Do not amend.

Do not push.

## post-commit verification

Required:

- final HEAD differs from `04436a11adc6dd6e70b4a98568fe878cc4c9f4aa`;
- commit parent is exactly `04436a11adc6dd6e70b4a98568fe878cc4c9f4aa`;
- commit message exact;
- committed path count exactly `46`;
- committed path set exactly final staged allowlist;
- every committed blob equals the pre-commit index blob;
- 17 source raw worktree identities still match accepted hashes;
- index empty after commit;
- no tracked worktree modifications for the 46 committed paths;
- known unrelated untracked `__pycache__` residue may remain;
- residue must not be staged/cleaned as a gate.

## tests

Do not rerun full tests.

Reuse Browser-accepted 1430 evidence:

`1460 PASS / 3 existing SKIP / 0 FAIL / 0 ERROR`

This turn is Git persistence only.

## external actions forbidden

```text
OpenAI provider calls:
0

real credential read/use:
0

Railway account/project/service mutation:
0

Railway deploy:
0

Cloudflare mutation:
0

Git push:
0

Public enable:
0
```

## acceptable outcome

`COMPLETED / GIT_PERSISTENCE_CANDIDATE`

Do not claim L5 terminal acceptance.

## mandatory stop

- HEAD mismatch;
- current index not exact predecessor 42;
- accepted source worktree 17/17 mismatch;
- any staged path fails EXACT_BYTES or CRLF_TO_LF_ONLY rule;
- final staged set != 46 exact paths;
- commit includes extra/missing path;
- source/worktree bytes mutate;
- repository Git/EOL configuration would need change.

## export

Create:

`.aiassistant/reports/target/20260916_1512_aiscc-p3-3-public-live-l5-local-hosted-runtime-git-persistence-crlf-normalization-retry-1/`

Include:

- `EXECUTOR_REPORT.md`
- `COMMIT_EVIDENCE.md`
- `COMMITTED_PATHS.txt`
- `GIT_CANONICALIZATION_VERIFICATION.json`
- `SOURCE_HASH_VERIFICATION.json`
- `WORKSPACE_BEFORE.txt`
- `WORKSPACE_AFTER.txt`
- exact Task copy
- result ZIP

## final response

1. result
2. target bundle
3. starting/final HEAD
4. predecessor 42-index verification
5. final committed path count
6. commit message
7. exact allowlist match
8. 17 source raw-byte identity
9. 46-path Git canonicalization verification
10. commit blob/index identity
11. index/tracked worktree after commit
12. preserved residue
13. reused tests
14. external actions
15. Public state
16. next Human Railway gate status
