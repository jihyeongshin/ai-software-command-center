# AISCC Browser Command Center Judgment

## 판정

```text
1459 Executor:
CORRECT STOP

executor_fault:
NO

blocker:
RAW_WORKTREE_SHA_VS_GIT_INDEX_LF_NORMALIZATION_CONTRACT

blocker_status:
RESOLVED

Git persistence retry:
AUTHORIZED
```

## finding

The predecessor Task incorrectly required Windows worktree raw bytes and Git index blobs to have identical SHA-256 values.

The actual repository uses:

`core.autocrlf=true`

For 13 accepted text paths, Git staged LF canonical blobs while leaving CRLF worktree bytes unchanged.

Every mismatch satisfied:

`CRLF_TO_LF(worktree_bytes) == index_bytes`

No other source/content difference was reported.

## accepted Git canonicalization rule

For this exact persistence candidate:

```text
CASE A:
index_bytes == worktree_bytes
→ PASS

CASE B:
index_bytes == CRLF_TO_LF(worktree_bytes)
AND worktree contains CRLF
→ PASS

anything else
→ FAIL / STOP
```

This rule applies to all 46 final staged paths, not only source paths.

For the 17 accepted source/config/test paths, additionally require raw worktree SHA-256 to remain exactly equal to the 1430 accepted hashes.

## prohibited

Do not solve this by:

- rewriting source line endings;
- setting `core.autocrlf=false`;
- changing global/local Git config;
- adding `.gitattributes`;
- modifying `.gitignore`;
- unstaging/restaging the existing 42 paths merely to obtain different raw hashes;
- weakening source identity to text-only comparison.

The accepted worktree candidate remains byte-identical to the reviewed 1430 candidate.

The commit stores Git's canonical LF form where its existing clean filter does so.

## current index authority

The predecessor index already contains exactly the intended 42 paths.

Preserve it.

After placing the current governance files and moving the retry Task to done, stage only the four newly authorized paths.

Expected final staged/committed set:

`46 exact paths`

Commit message remains:

`feat: add hosted public live runtime boundary`

## release boundary

No Railway account/project/service creation, secret entry, deployment, OpenAI call, Cloudflare mutation or public enablement belongs to this retry.
