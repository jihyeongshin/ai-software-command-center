# 작업지시서: P1-8 Runtime Final Acceptance Terminal Persistence

## meta

- task_id: `20260902_1222_aiscc-p1-8-runtime-final-acceptance-terminal-persistence-1`
- created_at: `2026-09-02T12:22:00+09:00`
- phase: `P1-8 Project Memory and Cycle Admission Runtime / P1 Terminal Closure`
- work_type: `COMMAND_CENTER_RECORD_UPDATE / GIT_TERMINAL_PERSISTENCE`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1_8_PROJECT_MEMORY_CYCLE / AISCC_REPOSITORY_GIT_HISTORY`
- expected_start_branch: `main`
- expected_start_head: `1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a`
- accepted_runtime_path_count: `36`
- accepted_runtime_aggregate_sha256: `a1d5e9d24eabae3fec13e24cfb9d94e744e6687ca4c00889e85972fb5a633590`
- human_p1_8_runtime_verification: `HUMAN_PROVIDED / ACCEPTED`
- human_acceptance_cycle: `.aiassistant/records/aiscc/cycles/20260902_1222_aiscc-p1-8-runtime-human-final-acceptance-1.cycle.md`
- human_acceptance_cycle_sha256: `f9bfb792e80b83d571066e3a72e18ba825bcf6a515e17606380492137993d77e`
- recommended_executor_session: `NEW_CHAT_REQUIRED_BY_HUMAN`
- session_open_owner: `HUMAN`
- git_commit: `AUTHORIZED_EXACT_TWO_COMMITS`
- git_push: `FORBIDDEN`
- deployment: `FORBIDDEN`

---

# 1. 목적

Command Center가 독립 검증하고 Human이 final review에서 `ACCEPTED`한 P1-8 Runtime의 exact 36-path candidate를
Git에 고정한다. Runtime source와 governance/provenance를 별도 commit으로 분리하고 P1 완료 및 P2 진입 준비
상태를 canonical records에 반영한다.

이번 Task는 runtime behavior를 다시 설계하거나 구현하지 않는다. Accepted bytes를 Commit A로 고정한 뒤,
Human acceptance Cycle, accumulated done Tasks, state records와 P1 completion handoff를 Commit B로 고정한다.

Successful result:

```text
P1-8:
TERMINAL_GIT_PERSISTED /
COMMAND_CENTER_COMMIT_REVIEW_REQUIRED /
SOURCE_MIRROR_SYNC_PENDING
```

Executor는 최종 `CLOSED`, Project Source sync 완료, P2 시작, push 또는 deployment를 선언하지 않는다.

---

# 2. 새 IDE 채팅 근거와 owner

새 IDE 채팅은 Human이 연다. Executor는 스스로 새 채팅을 열거나 전환할 수 없다.

새 채팅 근거:

```text
predecessor work:
RUNTIME_REWORK / ORCHESTRATION_IMPLEMENTATION / QA_ONLY

current work:
COMMAND_CENTER_RECORD_UPDATE / GIT_TERMINAL_PERSISTENCE

authority change:
Git index and exact two commits are now explicitly authorized,
while runtime source mutation is forbidden.
```

Human이 Task와 Cycle을 다운로드 경로에서 exact repository 경로로 Move한 뒤 새 IDE 채팅에서 시작한다.

---

# 3. authoritative acceptance inputs

Human acceptance source:

```text
Human P1-8 runtime final review
판정: ACCEPTED
```

Command Center substantive review:

```text
ACCEPTED_CANDIDATE /
COMMAND_CENTER_REVIEW_PASSED /
HUMAN_REVIEW_REQUIRED
```

Accepted 1100 submission:

```text
ZIP SHA-256:
207f0ae004b92ba705991bd4932e5b681bcf0fbd024735c8d58650307e85581e

Task SHA-256:
4a423a5614e90c882d26ea2c8a47c776670f5f241bcbc3ff92583ef416e787f0

runtime:
36 paths
a1d5e9d24eabae3fec13e24cfb9d94e744e6687ca4c00889e85972fb5a633590
```

Accepted evidence:

```text
provider regression: 1 passed
targeted unit: 59 passed
targeted PostgreSQL: 35 passed
full repository: 231 collected / 231 passed
ruff: PASS
mypy src: PASS, 82 source files
alembic current: 20260901_0008 (head)
alembic check: PASS
fingerprints: 22 / 22 exact
immutable baselines: 3 / 3 exact
unexpected skip/deselection: 0
```

---

# 4. mandatory preflight

Before any index mutation require:

```text
branch == main
HEAD == 1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a
Git index == empty

accepted runtime candidate == 36 paths
accepted aggregate == a1d5e9d24eabae3fec13e24cfb9d94e744e6687ca4c00889e85972fb5a633590
runtime candidate mismatches == 0

.aiassistant/records/aiscc/cycles/20260902_1222_aiscc-p1-8-runtime-human-final-acceptance-1.cycle.md
SHA-256 == f9bfb792e80b83d571066e3a72e18ba825bcf6a515e17606380492137993d77e

.aiassistant/records/aiscc/cycles/20260902_1100_aiscc-p1-8-runtime-expanded-path-implementation-hold-1.cycle.md
SHA-256 == 69f2d28f09180f2fe0d02eecafc48940d1db6de44c68994dca6887f4c9ceb383

unexpected dirty paths == 0
unexpected governance path == 0
```

Verify exact done Task identities when present:

```text
.aiassistant/tasks/done/20260901_2311_aiscc-p1-8-joint-design-terminal-git-object-reconciliation-audit-1.md
0795bd24b5d1b9531840424dbd7ba6c788fa08df3d19a21564e82250734fc1e7

.aiassistant/tasks/done/20260901_2359_aiscc-p1-8-runtime-prerequisite-authority-and-jcs-safe-integer-reconciliation-rework-1.md
ca616a7193a69aabd8d12f9e265152187e83806828edc7568f428669093a73b6

.aiassistant/tasks/done/20260902_0050_aiscc-p1-8-runtime-owner-boundary-canonical-path-audit-1.md
73b5beb16a882d391e174d2b29d8bebb36ebcf76cd95075d3313af8085bf171a

.aiassistant/tasks/done/20260902_0232_aiscc-p1-8-runtime-prerequisite-authority-expanded-path-implementation-rework-1.md
24caae66b547fe2e7cab58522e224dd77f666e7492f0ddf2c2e9c9156e5c3a00

.aiassistant/tasks/done/20260902_1100_aiscc-p1-8-runtime-provider-regression-and-metadata-parity-rework-1.md
4a423a5614e90c882d26ea2c8a47c776670f5f241bcbc3ff92583ef416e787f0
```

Some older accepted provenance paths may already exist in `HEAD`. Distinguish `already committed exact bytes` from
`current Git-dirty exact bytes`; do not stage a path merely to reproduce it. Any missing identity, hash mismatch,
unexpected path or non-empty index is a mandatory stop before Git mutation.

---

# 5. exact accepted runtime inventory

Aggregate serialization:

```text
ordinal case-sensitive UTF-8 without BOM
<repository-relative-path>\t<lowercase_sha256>\n
```

Exact 36 paths:

```text
migrations/versions/20260831_0006_p1_8_project_memory_cycle_admission.py e0072031ffc8be030bfa265d329196b67aad6774df240904fa01d8fdccf8766c
migrations/versions/20260831_0007_p1_8_authority_contract_rework.py 544aef28e3f36d5cff322afa9401b96f45fb050d03c7d41ea7d673e597815e0e
migrations/versions/20260901_0008_p1_8_prerequisite_authority_reconciliation.py c270e10f7d0763e4f5fee1d298ad9d41abb83510a07864cd4d3919afe4362d27
src/aiscc/contracts/canonical_json.py 9e235fff10aea51a44f8b1c6830d8ce724476339239a2d6d245dcdc94094a442
src/aiscc/cycle/__init__.py f9631ca9338109cbcd7a2aa07340a001b742fe4af0b129ca136c1078c4b62fed
src/aiscc/cycle/models.py e5aaa9a84c5d0cf8231c86d2efd300e8b1fa011697642d7d6ee395f46f0e1cf4
src/aiscc/cycle/repository.py d0a11d869ba94383eb35bf98f546968da28e3d2c56f872ad9de77728b9dc357d
src/aiscc/judgment/authority.py 0013e4a2ae6f84aba7341d1e58657ce0973ce7a7d5841d8fb69f7403f15a3941
src/aiscc/memory/__init__.py 842060c4e15da581c17f573e1e4a465592f486947e34eeaaa3cd589d1525fe79
src/aiscc/memory/models.py ba8c0fe2cb2802298b445718f2ae2fa0681b8f2983dec5064d9141fe38b8d308
src/aiscc/memory/repository.py b93856e50e1c5d5a74f7d49e1839bb2a2766a37fe3318fb49c2a2ec065f62ac4
src/aiscc/next_action/__init__.py c1e8cadee709b6ba289fa9f92ed2eeaa04e51444e3a9ff85f2fc97138c42172d
src/aiscc/next_action/models.py 09d5c13d73f2bb1cd4ef05433f73f40eedcb670353dcfae9cdbf480420af1ea6
src/aiscc/next_action/repository.py 51a44c9d28a374aea1359e41752e5ff02fdb21f89844ae61e082707906e213f7
src/aiscc/persistence/models.py 60518bd1ab916a07118de0e2bd6a507565a0fc0dc48d8cc003cd521b3018ca48
src/aiscc/persistence/repository.py 74a497fd32eb42176afd19b2ba621da04364b847b0130f52966bcb3001159dd1
src/aiscc/task_authority/__init__.py eb5c7e78bb891002d4bcbb81bf35ac121b9cbf8f4e2bab0c64b1232422d141d6
src/aiscc/task_authority/authority.py 76fe0027ca2d652efd8a9fe204408d23751aa23175c369a5bc6ce389ba3af165
src/aiscc/task_authority/models.py 101ec23cbf5197ec62e8a9c4b58e5fefa2296eeae43d75053f318cf66e05abd0
src/aiscc/task_authority/ports.py 991ad83420947a35021d6acfcc4ef0bc150d5112582e69b740698374eb8b68e8
src/aiscc/task_authority/repository.py 5de5faf4a7d60c83b181588d691ce36006469095b3e16aa449881ad14143f745
src/aiscc/workflow/__init__.py 3c4cdb62a49cb53c61705e705b77cd9fee14702671690c128076c9c9f7cdc5a1
src/aiscc/workflow/guards.py 0ad7c75e22755ecd2132805e6c143b99489eea8d7807a505f3798736a0364ba2
src/aiscc/workflow/models.py f69e813dea6c35f65c8eb28cfe118b36091dd8cf5225241396e254f6ea0ff99c
src/aiscc/workflow/ports.py afb4b105a4bf55a8dcfc2abb7bc110b7b7262a50851ae3cda6734489ebbc863f
tests/integration/evidence/test_postgres_evidence_admission.py 9f56ced27bdcca3c010240f7d8736a21ff4fe94a97d5330571c584b1cba3f545
tests/integration/human/test_postgres_human_gate_judgment.py 142020f3a81221944e6eb0001160b83aa897662a324c9e89963e4226079a02b5
tests/integration/memory/test_postgres_project_memory_next_action.py 6881eaebbb8c25f34e1589e552b044d4072aebda3e2a06d40f942f2526254bd1
tests/integration/providers/test_execution_persistence.py 717a40b9323d0c42560ef34a8f39634777be0929d3eeaea5b447c9e4e4de1214
tests/integration/task_authority/test_postgres_external_task_authority.py 15dfa7e90807aa02c60cec13f03ca64d24cce56a23049c6043cc9aff554234a5
tests/integration/workflow/test_postgres_kernel.py 10be51d5d7b43b4dbd2df8a19900ac4c116990a42860ffe8a015170cff877240
tests/unit/contracts/test_canonical_json.py 33095e18666620a4b504c719ebdabfd302e8be2bbc9b6f10e0013453964de7d3
tests/unit/cycle/test_project_memory_cycle_domain.py 783aef1e861a68481f818b333a47e8a1da17affe7d2791d3824fbd12e4031d
tests/unit/next_action/test_next_action_domain.py 1a1525c4509302b6f5aaa4ff19965cd4e1680b5e3543db571af38c7067261449
tests/unit/task_authority/test_external_task_authority_domain.py f1b83cd299ac8f6bef239f18aa6206da5034a04ae2d9a5693ff760c1325e0ffd
tests/unit/workflow/test_state_machine.py 7f0501684a30211ab43b7bb9bdae389934c3558a28da266c94254f0fdb867752
```

---

# 6. must read

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
.aiassistant/records/aiscc/cycles/20260901_2155_aiscc-p1-8-jcs-safe-integer-joint-design-final-acceptance-1.cycle.md
.aiassistant/records/aiscc/cycles/20260902_1100_aiscc-p1-8-runtime-expanded-path-implementation-hold-1.cycle.md
.aiassistant/records/aiscc/cycles/20260902_1222_aiscc-p1-8-runtime-human-final-acceptance-1.cycle.md
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/tasks/done/20260902_1100_aiscc-p1-8-runtime-provider-regression-and-metadata-parity-rework-1.md
```

Read exact Git status/diff/tree/object data needed for the two commits. Do not bulk-read unrelated source or logs.

---

# 7. forbidden runtime mutation

No product/test/migration byte may change in this Task.

The accepted 36-path inventory is read-only. Commit A persists existing exact bytes only. If a runtime byte differs,
stop; do not repair it in this terminal Task.

Forbidden runtime actions:

- formatter or import organizer over source/test/migration;
- migration rewrite;
- test assertion change;
- generated code refresh;
- cleanup/reset/restore of unrelated paths;
- deletion or rollback of accepted candidate bytes.

---

# 8. Commit A — exact runtime persistence

The exact expected Git-dirty runtime set contains 29 paths:

```text
migrations/versions/20260901_0008_p1_8_prerequisite_authority_reconciliation.py
src/aiscc/contracts/canonical_json.py
src/aiscc/cycle/models.py
src/aiscc/cycle/repository.py
src/aiscc/memory/models.py
src/aiscc/next_action/models.py
src/aiscc/next_action/repository.py
src/aiscc/persistence/models.py
src/aiscc/persistence/repository.py
src/aiscc/task_authority/__init__.py
src/aiscc/task_authority/authority.py
src/aiscc/task_authority/models.py
src/aiscc/task_authority/ports.py
src/aiscc/task_authority/repository.py
src/aiscc/workflow/__init__.py
src/aiscc/workflow/guards.py
src/aiscc/workflow/models.py
src/aiscc/workflow/ports.py
tests/integration/evidence/test_postgres_evidence_admission.py
tests/integration/human/test_postgres_human_gate_judgment.py
tests/integration/memory/test_postgres_project_memory_next_action.py
tests/integration/providers/test_execution_persistence.py
tests/integration/task_authority/test_postgres_external_task_authority.py
tests/integration/workflow/test_postgres_kernel.py
tests/unit/contracts/test_canonical_json.py
tests/unit/cycle/test_project_memory_cycle_domain.py
tests/unit/next_action/test_next_action_domain.py
tests/unit/task_authority/test_external_task_authority_domain.py
tests/unit/workflow/test_state_machine.py
```

Before staging, prove this set equals the runtime Git-dirty set and every byte equals section 5. Stage only these
exact 29 paths with pathspecs. Verify staged set and staged blob hashes before commit.

Authorized Commit A message:

```text
feat(runtime): complete P1-8 project memory and cycle admission
```

Commit A requirements:

- parent exactly `1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a`;
- exactly 29 changed runtime paths;
- all 36 accepted runtime paths in resulting tree match section 5;
- no governance/repository configuration path;
- no merge commit, amend or GPG requirement;
- record commit object, parent, tree and per-path blob evidence.

If Git identity is unavailable or commit fails, stop without inventing credentials or changing global config.

---

# 9. canonical state and P1 completion handoff

After Commit A, modify only these canonical governance records:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

Create:

```text
.aiassistant/reports/aiscc/20260902_1222_aiscc-p1-completion-p2-entry-handoff-1.md
```

Required semantic updates:

## CURRENT_STATE_SUMMARY

- P1-8 design/runtime/Human final review accepted;
- Commit A exact identity and 36-path aggregate;
- P1-1 through P1-8 implementation complete;
- terminal governance persistence status;
- Project Source state mirror sync pending;
- next phase after mirror synchronization: `P2-1 Command Center Web UI`;
- no claim that P2 has started.

## DECISION_REGISTER

Append, without renumbering or rewriting prior decisions:

- Human P1-8 runtime final review `ACCEPTED`;
- exact 36-path aggregate;
- provider blocker and Alembic parity reconciliation accepted;
- Commit A runtime identity;
- P1 implementation completion and transition toward P2-1;
- Project Source mirror sync remains Human-owned and pending.

## NEXT_ACTIONS

- mark P1-8 runtime/acceptance/terminal runtime commit complete;
- identify terminal governance/Project Source mirror synchronization as the immediate operational gate;
- preserve canonical roadmap next phase `P2-1 Command Center Web UI`;
- do not add per-turn detail that belongs only in Cycles;
- do not begin or design P2-1 in this Task.

## P1 completion handoff

Record:

- product thesis and explicit-state-machine architecture continuity;
- P1-1 through P1-8 completion summary;
- Commit A identity and accepted runtime aggregate;
- Human acceptance source;
- exact accepted authority boundaries and immutable baselines;
- remaining source mirror synchronization gate;
- P2-1 entry prerequisites and non-goals;
- public runtime boundary remains replay-default/bounded-live optional;
- no deployment or competition submission claim.

Use actual current canonical record structure. If local canonical state conflicts with this accepted result or has
newer incompatible decisions, stop with `POLICY_CONFLICT_INVESTIGATION_REQUIRED`; do not overwrite it.

---

# 10. Commit B — governance/provenance persistence

Allowed accumulated accepted provenance paths:

```text
.aiassistant/tasks/done/20260901_2311_aiscc-p1-8-joint-design-terminal-git-object-reconciliation-audit-1.md
.aiassistant/tasks/done/20260901_2359_aiscc-p1-8-runtime-prerequisite-authority-and-jcs-safe-integer-reconciliation-rework-1.md
.aiassistant/tasks/done/20260902_0050_aiscc-p1-8-runtime-owner-boundary-canonical-path-audit-1.md
.aiassistant/tasks/done/20260902_0232_aiscc-p1-8-runtime-prerequisite-authority-expanded-path-implementation-rework-1.md
.aiassistant/tasks/done/20260902_1100_aiscc-p1-8-runtime-provider-regression-and-metadata-parity-rework-1.md
.aiassistant/tasks/done/20260902_1222_aiscc-p1-8-runtime-final-acceptance-terminal-persistence-1.md
.aiassistant/records/aiscc/cycles/20260902_1100_aiscc-p1-8-runtime-expanded-path-implementation-hold-1.cycle.md
.aiassistant/records/aiscc/cycles/20260902_1222_aiscc-p1-8-runtime-human-final-acceptance-1.cycle.md
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/reports/aiscc/20260902_1222_aiscc-p1-completion-p2-entry-handoff-1.md
```

For the older 2311/2359/0050 paths, stage only if they are exact accepted bytes and are not already present in
Commit A's parent tree. Never create a duplicate mutation for an already committed path.

After moving this Task active -> done, resolve the exact Git-dirty governance set as a subset of the allowlist
above. Any other Git-dirty governance/repository configuration path is a mandatory stop.

Authorized Commit B message:

```text
docs(governance): persist P1-8 acceptance and P2 entry handoff
```

Commit B requirements:

- parent exactly Commit A;
- runtime tree unchanged from Commit A;
- only exact allowlisted Git-dirty governance paths;
- Human acceptance Cycle byte-exact to the supplied SHA;
- this Task byte-exact at its done path;
- canonical state records and handoff satisfy section 9;
- no mirror bundle, target bundle or repository configuration path;
- record commit object, parent, tree and per-path blob evidence.

---

# 11. post-commit verification

Required after Commit B:

```text
branch == main
HEAD == Commit B
Commit B parent == Commit A
Commit A parent == 1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a
merge commits == 0
Git index == empty
unexpected Git-visible worktree paths == 0
runtime tree aggregate == a1d5e9d24eabae3fec13e24cfb9d94e744e6687ca4c00889e85972fb5a633590
all 36 runtime tree blobs == accepted SHA-256
Human acceptance Cycle == f9bfb792e80b83d571066e3a72e18ba825bcf6a515e17606380492137993d77e
git diff CommitA..CommitB runtime paths == empty
git diff --check CommitA^..CommitB == PASS
```

Do not rerun product tests merely to refill evidence fields. The complete accepted 1100 proof is reusable because
Commit A must preserve exact accepted bytes. If any byte changes, stop rather than substituting old tests.

---

# 12. evidence contract

## executor_required

- exact preflight branch/HEAD/index/worktree inventory;
- 36-path candidate hash and aggregate verification before staging;
- Human Cycle hash and content identity;
- Commit A staged path/blob set and commit object proof;
- canonical state/handoff semantic diff;
- Commit B staged path/blob set and commit object proof;
- exact parent/tree/runtime immutability checks;
- final clean Git inventory;
- UTF-8/Markdown/control-character/diff checks;
- complete export manifest and source-copy identity.

## reuse_allowed

- accepted 1100 unit/integration/full/static/migration/fingerprint evidence only under exact byte identity;
- accepted joint design, 0050 audit and prior terminal Git lineage;
- Human final review result from the supplied Cycle.

## human_owned

- Project Source active-set replacement after a separately accepted mirror bundle;
- Git push/remote publication;
- P2 product acceptance;
- deployment/Public Live/competition submission.

## not_required

- new runtime tests when bytes remain exact;
- browser QA;
- provider/tool/network/credential action;
- deployment;
- P2 implementation.

## forbidden

- runtime source/test/migration mutation;
- more or fewer than the two authorized commits;
- mixed runtime/governance staging;
- amend, rebase, merge, reset, restore or cleanup of unrelated paths;
- push, PR, release, deployment or Project Source upload;
- Agent-minted Human acceptance;
- modification of supplied Human acceptance Cycle;
- secret/private data collection.

---

# 13. result and stop conditions

Successful Executor result only:

```text
P1-8:
TERMINAL_GIT_PERSISTED /
COMMAND_CENTER_COMMIT_REVIEW_REQUIRED /
SOURCE_MIRROR_SYNC_PENDING
```

Mandatory stop before further mutation on:

- preflight identity mismatch;
- non-empty index;
- unexpected dirty path;
- runtime candidate mismatch;
- Human Cycle mismatch;
- Git identity/commit failure;
- staging set mismatch;
- canonical record conflict;
- Commit parent/tree/path mismatch;
- need for third commit or runtime repair.

After a named blocker, perform only minimal evidence, safe index cleanup limited to this Task's own incomplete
staging when provably necessary, report/export and stop. Do not reset or rewrite commits.

---

# 14. export bundle

Target:

```text
.aiassistant/reports/target/20260902_1222_aiscc-p1-8-runtime-final-acceptance-terminal-persistence-1/
```

Required root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `GIT_OBJECT_EVIDENCE.md`
- `RUNTIME_INVENTORY.md`
- `GOVERNANCE_INVENTORY.md`
- `STATE_HANDOFF_EVIDENCE.md`
- all 36 runtime files copied from Commit A/Commit B tree preserving repository-relative paths
- all Commit B governance files preserving repository-relative paths
- `REMOVED_FILES.md` only if deletion occurred; deletion is not expected

Manifest requirements:

- every payload except manifest listed;
- actual bytes and SHA-256;
- exact source commit/tree/path and blob object for copied tracked files;
- copy/source match;
- no credential, private data, Git object database dump or unrelated file.

---

# 15. preserved paths

The final report must list every durable artifact that must survive cleanup, including:

- all newly committed Task done paths;
- both 1100 and 1222 Cycle paths;
- canonical state records;
- P1 completion/P2 entry handoff;
- accepted authority rules;
- Commit A and Commit B identities.

The ignored target bundle is temporary and may be deleted only after Command Center commit review and any required
source-mirror follow-up has safely consumed its evidence.

---

# 16. final response

1. result;
2. Commit A hash/message/parent/tree/path count;
3. Commit B hash/message/parent/tree/path count;
4. final branch/HEAD/index/worktree status;
5. accepted runtime aggregate verification;
6. canonical state/handoff paths;
7. source mirror sync status;
8. target bundle path;
9. unverified Human-owned actions;
10. preserved exact paths.
