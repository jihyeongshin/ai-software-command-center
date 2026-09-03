# 작업지시서: P2-1A read API foundation Git persistence

## meta

- task_id: `20260903_1036_aiscc-p2-1a-read-api-foundation-git-persistence-1`
- created_at: `2026-09-03T10:36:00+09:00`
- project: `AI Software Command Center (AISCC)`
- phase: `P2-1A — persistence checkpoint`
- work_type: `GIT_PERSISTENCE / P2_1A_CHECKPOINT`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- predecessor_head: `6b0383fce036471e6760999a2352276e2806fca5`
- predecessor_task: `.aiassistant/tasks/done/20260903_1026_aiscc-p2-1a-default-runtime-command-center-read-composition-rework-1.md`
- predecessor_acceptance_cycle: `.aiassistant/records/aiscc/cycles/20260903_1034_aiscc-p2-1a-command-center-read-model-api-final-acceptance-1.cycle.md`
- accepted_product_aggregate_sha256: `932811926fe6ee5bcf3520ac63f555566a4c1c417d1d130f4f14659da9eb7a73`
- target_bundle: `.aiassistant/reports/target/20260903_1036_aiscc-p2-1a-read-api-foundation-git-persistence-1/`
- fresh_chat_policy: `REUSE_CURRENT_P2_1A_IMPLEMENTATION_CHAT_ALLOWED / GIT_PERSISTENCE_ONLY`
- success_boundary: `P2_1A_PERSISTENCE_COMMIT_CREATED / COMMAND_CENTER_REVIEW_REQUIRED`

## 0. authority

Browser Command Center accepted the exact P2-1A implementation bytes.

Accepted product/test count:

```text
9
```

Accepted aggregate:

```text
932811926fe6ee5bcf3520ac63f555566a4c1c417d1d130f4f14659da9eb7a73
```

This Task may persist those exact bytes plus exact accumulated P2 governance provenance.

It may not change product/test content.

## 1. Downloads transport

Exactly two new files:

```text
C:\Users\oracl\Downloads\20260903_1036_aiscc-p2-1a-read-api-foundation-git-persistence-1.md
C:\Users\oracl\Downloads\20260903_1034_aiscc-p2-1a-command-center-read-model-api-final-acceptance-1.cycle.md
```

Destinations:

```text
.aiassistant/tasks/active/20260903_1036_aiscc-p2-1a-read-api-foundation-git-persistence-1.md
.aiassistant/records/aiscc/cycles/20260903_1034_aiscc-p2-1a-command-center-read-model-api-final-acceptance-1.cycle.md
```

Acceptance Cycle expected SHA-256:

```text
528b2e417aa23a01b5a5e66d6a3341eabb6139a6219957c447552e2d574acbf3
```

Precheck both exact sources, absent destinations, and Cycle hash before moving either.

Failure:

```text
TRANSPORT_PRECONDITION_FAILED
```

All PASS:

- Move, not Copy;
- verify exact destination identity and Downloads-source absence.

## 2. session

Reuse the current P2-1A implementation/rework chat.

Allowed lineage:

```text
0910 implementation
→ 1026 rework
→ 1036 persistence
```

This Task is Git persistence only. No source redesign/rework is authorized.

## 3. repository preflight

Require:

```text
repository == ai-software-command-center
branch == main
HEAD == 6b0383fce036471e6760999a2352276e2806fca5
index == empty
```

Product/test dirt before any Task lifecycle MUST equal exact Section 4 nine paths and hashes.

Pre-existing Git-visible governance/provenance dirt before transporting the 1034 Cycle MUST equal these exact seven paths:

```text
.aiassistant/records/aiscc/cycles/20260903_0311_aiscc-project-source-mirror-v2-activation-persistence-final-acceptance-1.cycle.md
.aiassistant/tasks/done/20260903_0313_aiscc-p2-1-command-center-web-ui-substrate-and-contract-design-audit-1.md
.aiassistant/records/aiscc/cycles/20260903_0904_aiscc-p2-1-command-center-web-ui-design-audit-command-center-acceptance-human-design-gate-1.cycle.md
.aiassistant/records/aiscc/cycles/20260903_0908_aiscc-p2-1-command-center-web-ui-human-design-final-acceptance-1.cycle.md
.aiassistant/tasks/done/20260903_0910_aiscc-p2-1a-command-center-read-model-api-projection-foundation-implementation-1.md
.aiassistant/records/aiscc/cycles/20260903_1024_aiscc-p2-1a-command-center-read-model-api-partial-acceptance-default-runtime-composition-rework-1.cycle.md
.aiassistant/tasks/done/20260903_1026_aiscc-p2-1a-default-runtime-command-center-read-composition-rework-1.md
```

Expected exact identities:

```text
0311 Cycle SHA-256:
f984450adafc61fcc5e3b0f066c92e9dde9e2a60c1e4f8fc721d62d10eee48d6

0313 done Task SHA-256:
e9950e17d99ef26f75594e97f19028194dc892145c37828dbd5ada7305f9a3be

0904 Cycle SHA-256:
621ffae3fc107838efd708ccc418bdfccf5c299c0abe69eb07709ebd06d378af

0908 Cycle SHA-256:
b26beab7734f0e68226c353eee1edbea70563f2af353b29ca3f41a460ee475cb

0910 done Task SHA-256:
cda8c49df4a8bc3a43de2c40fcc99b44362f968ac73457cafe1752df151c030c

1024 Cycle SHA-256:
95e0bd4170413abd8ddbc5e4743aad4737aa75fc05247b4a1309eb373e558015

1026 done Task SHA-256:
49ff3e2aac274534ed3356503905b67761e25efaaf2bdf5df367156d1c48f552
```

After transporting the 1034 acceptance Cycle while current Task remains active/ignored:

```text
product/test dirt:
9

governance/provenance dirt:
8
```

No unrelated path is allowed.

Do not clean, restore, or auto-expand.

## 4. exact accepted nine product/test identities

- `src/aiscc/api/app.py` — `3aafd4ebd042be24326c94fe07c7ffb6d032cb6d25f880d049db3f09ea1d6837`
- `src/aiscc/api/routes/command_center.py` — `660ee70d71d9706dea17f20fc52b91ed716b7756fcd6aa425f2e90281004950b`
- `src/aiscc/command_center/__init__.py` — `3ba6d7bc03ff2986d45ed359290aa693cb9dcd8a41c84398a1a46249bb02c9fd`
- `src/aiscc/command_center/postgres_queries.py` — `476d084403b2eeefe69cd7a218f98b631188138cce2923920f22ee0c0c66571d`
- `src/aiscc/command_center/privacy.py` — `2f17f4250e11c5ee65a8d26cb65528d7045365255c43d00a74c3dc455cbe990b`
- `src/aiscc/command_center/queries.py` — `94fe298372622ca82f1158ea9f45be24506e890c1f6a4180eef7d4997a26ed09`
- `src/aiscc/command_center/read_models.py` — `346daeb778344a8ebf3e5f5905ee7c238a7a8cee0d64a18ddd219462cfe9fe1e`
- `tests/integration/command_center/test_postgres_read_api.py` — `a2373d321e86b7d8f2b90a0a8bb3c23060de6f8612a2c58a6e7a942c21e07110`
- `tests/unit/command_center/test_read_contracts.py` — `6132923fe6f73648b60ad80a7d1c299e0876bc1167caa2bc19f4fc684762972a`

Require:

```text
path count == 9
per-path SHA-256 == exact above
aggregate == 932811926fe6ee5bcf3520ac63f555566a4c1c417d1d130f4f14659da9eb7a73
```

Do not modify any of these files.

## 5. validation before staging

Run read-only:

```text
git diff --check
```

Re-run no product tests unless repository drift or Git representation creates a concrete reason.

Accepted 1026 runtime/test proof may be reused because this Task changes no product/test byte.

If any accepted source hash differs:

```text
ACCEPTED_SOURCE_IDENTITY_MISMATCH
```

STOP without restore.

## 6. current Task lifecycle

After all preflight/identity checks:

```text
.aiassistant/tasks/active/20260903_1036_aiscc-p2-1a-read-api-foundation-git-persistence-1.md
→
.aiassistant/tasks/done/20260903_1036_aiscc-p2-1a-read-api-foundation-git-persistence-1.md
```

Move, not Copy.

Verify bytes unchanged.

After lifecycle exact Git-visible changed/untracked set MUST be:

```text
9 accepted product/test
+ 7 predecessor governance/provenance
+ 1034 acceptance Cycle
+ current 1036 Task done
= 18 paths
```

No nineteenth path.

## 7. exact staging

Stage exactly the 18 paths with explicit pathspecs.

Do not use:

```text
git add .
git add -A
```

Require:

```text
staged count == 18
unstaged Git-visible dirt == 0
accepted product/test staged == 9
governance/provenance staged == 9
runtime/product path outside accepted nine == 0
rules/config/migrations == 0
Project Source manifest/bundle == 0
```

For each accepted product/test file, staged blob content SHA-256 must equal Section 4.

## 8. persistence commit

Authorized message:

```text
feat(command-center): complete P2-1A read API foundation
```

Create exactly one non-merge commit.

Require:

```text
parent == 6b0383fce036471e6760999a2352276e2806fca5
parent count == 1
merge parent count == 0
changed path count == 18
changed path set == exact Section 6 set
```

Do not amend, rebase, merge, revert, or create a second repair commit.

If Git author identity is unavailable, STOP without changing Git config.

## 9. post-commit proof

Prove:

- branch remains `main`;
- HEAD is the single new persistence commit;
- parent exact baseline;
- exact commit message;
- exact 18 path set;
- accepted nine commit-tree SHA-256 match Section 4;
- accepted nine aggregate remains `932811926fe6ee5bcf3520ac63f555566a4c1c417d1d130f4f14659da9eb7a73`;
- governance provenance path set exact;
- index empty;
- Git-visible worktree clean;
- no Project Source generated bundle committed;
- no runtime tests/deployment/network were rerun unnecessarily.

Do not declare P2-1B started.

## 10. required export

Target:

```text
.aiassistant/reports/target/20260903_1036_aiscc-p2-1a-read-api-foundation-git-persistence-1/
```

Required root:

```text
TASK.md
EXECUTOR_REPORT.md
GIT_OBJECT_EVIDENCE.md
ACCEPTED_SOURCE_IDENTITY.md
EXPORT_MANIFEST.md
```

Export exact commit-tree copies preserving repository-relative paths for all 18 changed paths.

`ACCEPTED_SOURCE_IDENTITY.md` must list the nine accepted product/test paths, commit-tree SHA-256, and aggregate.

Manifest binds every payload except itself.

## 11. evidence contract

### executor_required

- transport;
- baseline/index/dirty inventory;
- exact nine source identities;
- exact governance identities;
- exact staging;
- commit object/tree/path proof;
- post-commit clean state;
- export manifest.

### reuse_allowed

- 1026 targeted/default-entrypoint/runtime/regression evidence while exact nine bytes remain identical.

### human_owned

- none before persistence;
- Browser Command Center accepts the persistence commit afterward.

### forbidden

- source/test content mutation;
- product path expansion;
- canonical state rewrite;
- Project Source refresh;
- broad cleanup/staging;
- network/push/deploy.

## 12. success

Successful candidate:

```text
P2_1A_PERSISTENCE_COMMIT_CREATED
/ COMMAND_CENTER_REVIEW_REQUIRED
```

Do not declare:

```text
P2-1B STARTED
P2-1 ACCEPTED
P2-1 CLOSED
P2-2 STARTED
```

## 13. preserved artifacts

Preserve:

- new P2-1A persistence commit candidate;
- `.aiassistant/records/aiscc/cycles/20260903_1034_aiscc-p2-1a-command-center-read-model-api-final-acceptance-1.cycle.md`;
- `.aiassistant/tasks/done/20260903_1036_aiscc-p2-1a-read-api-foundation-git-persistence-1.md`;
- exact predecessor P2 governance lineage listed in Section 3.

Target bundle remains temporary through Browser review.
