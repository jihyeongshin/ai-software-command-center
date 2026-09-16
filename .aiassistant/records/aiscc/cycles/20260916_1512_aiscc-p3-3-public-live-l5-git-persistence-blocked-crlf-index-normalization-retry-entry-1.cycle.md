# AISCC Cycle Record

## meta

- cycle_id: `20260916_1512_aiscc-p3-3-public-live-l5-git-persistence-blocked-crlf-index-normalization-retry-entry-1`
- date: `2026-09-16 KST`
- primary_semantic_owner: `Browser Command Center`
- affected_areas: `P3-3 Public Live L5 Git persistence / Windows Git newline canonicalization`
- work_type: `GIT_PERSISTENCE_REWORK`
- predecessor_task: `.aiassistant/tasks/done/20260916_1459_aiscc-p3-3-public-live-l5-local-hosted-runtime-git-persistence-1.md`
- result_status: `BLOCKED_DOCUMENT_CONTRACT_MISMATCH / NORMALIZATION_POLICY_RESOLVED / RETRY_AUTHORIZED`
- executor_fault: `NO`
- starting_HEAD: `04436a11adc6dd6e70b4a98568fe878cc4c9f4aa`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260916_1512_aiscc-p3-3-public-live-l5-git-persistence-blocked-crlf-index-normalization-retry-entry-1.cycle.md`

## predecessor result integrity

Executor result ZIP:

`20260916_1459_aiscc-p3-3-public-live-l5-local-hosted-runtime-git-persistence-1.zip`

SHA-256:

`855d73c247013c66f140ff6d4abfbff685bb66d4055461a9663ed0ed55266e8d`

Adjacent sidecar:

`MATCH`

The predecessor correctly stopped before commit.

Observed:

```text
HEAD:
04436a11adc6dd6e70b4a98568fe878cc4c9f4aa

commit:
NONE

index:
exact 42 intended paths staged

accepted source worktree identity:
17 / 17 PASS

accepted source index raw-byte identity:
4 / 17 PASS

mismatched source paths:
13

core.autocrlf:
true

all 13 mismatches:
worktree CRLF → index LF only
equal_after_crlf_to_lf = true

real provider calls:
0

Railway / Cloudflare mutation:
0

Public admission:
DISABLED

Public Live:
NOT_RELEASED
```

## blocker

The predecessor persistence Task required both:

1. accepted worktree bytes to match the 1430 source SHA-256;
2. staged Git index blobs to match those same raw SHA-256 values.

On Windows with the observed `core.autocrlf=true`, Git applied its standard clean transformation when adding CRLF text files:

```text
worktree CRLF bytes
→ Git index LF bytes
```

The Executor correctly refused to reinterpret that transformation without Command Center authority.

Affected 13 accepted source/config/test paths:

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

No semantic/content mismatch was observed. For every affected path:

`CRLF_TO_LF(worktree_bytes) == index_bytes`

## controlling repository policy

The canonical asset/Git/encoding policy requires UTF-8 handling, explicit Git authorization, and protection against unsafe source/document corruption.

It does not freeze worktree CRLF bytes as the required Git object representation.

Therefore the prior persistence Task's raw worktree-SHA == index-SHA requirement was over-constrained for this Windows repository.

## normalization resolution

For this persistence lineage only, the accepted Git object identity rule is:

```text
accepted worktree bytes remain authoritative for 1430 candidate review

AND

for each staged text path:

index_bytes == worktree_bytes
OR
index_bytes == CRLF_TO_LF(worktree_bytes)
```

No other transformation is permitted.

Requirements:

- worktree bytes for the accepted 17 source/config/test paths MUST still match the 1430 accepted SHA-256 values exactly;
- Git index may contain LF-normalized canonical blobs when and only when exact CRLF→LF transformation proves equality;
- UTF-8 content, code points and non-EOL bytes must be unchanged;
- no source file rewrite is required;
- no `.gitattributes`, `.gitignore`, global Git config or local repository config change is authorized;
- no reset/unstage/restage of the existing predecessor 42-path index is required if it already satisfies the rule;
- final commit identity is the Git index blob identity, not raw Windows worktree storage bytes.

## accumulated persistence state

The predecessor index intentionally remains populated with the exact 42-path allowlist.

This is expected predecessor state, not dirt to clear.

The retry will add exactly four new canonical governance paths:

- this Cycle;
- this Judgment;
- this Handoff;
- this retry Task moved to `tasks/done`.

Final commit expected path count:

`46`

No previous path may be removed.

## result state

```text
1459 persistence:
BLOCKED_CORRECTLY

normalization policy:
RESOLVED

retry:
AUTHORIZED

L5 local runtime:
ACCEPTED_CANDIDATE

L5 terminal:
OPEN

Human Railway deployment:
WAITING_FOR_PERSISTENCE

Public admission:
DISABLED

Public Live:
NOT_RELEASED
```
