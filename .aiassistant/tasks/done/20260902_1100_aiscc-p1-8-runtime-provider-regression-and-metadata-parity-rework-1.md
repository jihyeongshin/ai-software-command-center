# 작업지시서: P1-8 Runtime Provider Regression and Metadata Parity Rework

## meta

- task_id: `20260902_1100_aiscc-p1-8-runtime-provider-regression-and-metadata-parity-rework-1`
- created_at: `2026-09-02T11:00:00+09:00`
- phase: `P1-8 Project Memory and Cycle Admission Runtime`
- work_type: `RUNTIME_REWORK / ORCHESTRATION_IMPLEMENTATION / QA_ONLY`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1_4_SYSTEM_TRANSITION_AUTHORITY / P1_8_CROSS_OWNER_PREREQUISITE_RUNTIME`
- expected_start_branch: `main`
- expected_start_head: `1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a`
- predecessor_task: `20260902_0232_aiscc-p1-8-runtime-prerequisite-authority-expanded-path-implementation-rework-1`
- predecessor_task_sha256: `24caae66b547fe2e7cab58522e224dd77f666e7492f0ddf2c2e9c9156e5c3a00`
- predecessor_candidate_path_count: `35`
- predecessor_candidate_aggregate_sha256: `93eccebd0a2865b9584be6707fc57df66a28481cb4cc6b5902b8ce88bfee7dfc`
- human_p1_8_runtime_verification: `HUMAN_PENDING`
- recommended_executor_session: `CONTINUE_CURRENT_IDE_CHAT`
- new_chat_required: `NO`
- git_commit: `FORBIDDEN`
- git_push: `FORBIDDEN`

---

# 1. Command Center 판정

`20260902_0232` 제출물에 대한 독립 검증 결과:

```text
ZIP SHA-256:
cbb2021c82385d050df0c2dfceed07d7a241a1be1160075fcc9775382a9a9a9c

ZIP CRC/path/symlink safety:
PASS

manifest payload:
42 / 42 actual bytes and SHA-256 PASS

accepted fingerprint rows:
22 / 22 present and reported PASS

immutable baseline bytes:
0006 / 0007 / judgment authority PASS
```

Targeted implementation evidence:

```text
targeted unit:       59 passed
targeted PostgreSQL: 35 passed
ruff:                PASS
mypy src:            PASS, 82 source files
```

Acceptance blockers:

```text
complete repository pytest:
230 passed / 1 failed

failing test:
tests/integration/providers/test_execution_persistence.py::
test_provider_returned_tool_is_denied_when_accepted_transition_leaves_running

failure:
AuthorityConflictError:
admission into BLOCKED requires one typed P1_4BlockerClaimV1

alembic check:
FAIL: New upgrade operations detected
```

Command Center judgment:

```text
P1-8 Runtime:
HOLD_REWORK_REQUIRED /
RUNTIME_PATH_BOUNDARY_INSUFFICIENT /
MIGRATION_METADATA_PARITY_REQUIRED /
HUMAN_PENDING
```

The 0232 candidate is retained. It is neither accepted nor rolled back. Human runtime acceptance must not begin
until both blockers are repaired and all required verification passes.

---

# 2. session boundary

This is a narrow continuation of the same implementation candidate and blocker discovered by the current IDE
Executor turn. A new IDE chat is not required.

The Executor cannot open or switch chats. If Human chooses to open another IDE chat for operational reasons, that
is a Human action and does not change authority or acceptance.

---

# 3. mandatory preflight

Before mutation require:

```text
branch == main
HEAD == 1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a
Git index == empty

.aiassistant/tasks/done/20260902_0232_aiscc-p1-8-runtime-prerequisite-authority-expanded-path-implementation-rework-1.md
SHA-256 == 24caae66b547fe2e7cab58522e224dd77f666e7492f0ddf2c2e9c9156e5c3a00

current runtime candidate:
35 paths
93eccebd0a2865b9584be6707fc57df66a28481cb4cc6b5902b8ce88bfee7dfc

unexpected dirty paths == 0
unexpected candidate-byte mismatch == 0
```

Aggregate serialization remains:

```text
ordinal case-sensitive UTF-8 without BOM
<repository-relative-path>\t<lowercase_sha256>\n
```

If the 35-path candidate identity differs, do not absorb or overwrite it. Stop with:

```text
DIRTY_WORKSPACE_MIXED / PREDECESSOR_CANDIDATE_IDENTITY_MISMATCH
```

---

# 4. exact predecessor candidate inventory

The following 35 path/SHA pairs are the accepted starting inventory for this rework. They are not runtime
acceptance.

```text
migrations/versions/20260831_0006_p1_8_project_memory_cycle_admission.py e0072031ffc8be030bfa265d329196b67aad6774df240904fa01d8fdccf8766c
migrations/versions/20260831_0007_p1_8_authority_contract_rework.py 544aef28e3f36d5cff322afa9401b96f45fb050d03c7d41ea7d673e597815e0e
migrations/versions/20260901_0008_p1_8_prerequisite_authority_reconciliation.py 519bc5106ce6ab547c5604f9de4e9ff54e2bbb8292ceb855a6a01b85816e13e5
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
src/aiscc/persistence/models.py 11a86b1b8b54f638d8a808984e49ca10326c422ded8a5340b751b95fa015450d
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
tests/integration/task_authority/test_postgres_external_task_authority.py 15dfa7e90807aa02c60cec13f03ca64d24cce56a23049c6043cc9aff554234a5
tests/integration/workflow/test_postgres_kernel.py 10be51d5d7b43b4dbd2df8a19900ac4c116990a42860ffe8a015170cff877240
tests/unit/contracts/test_canonical_json.py 33095e18666620a4b504c719ebdabfd302e8be2bbc9b6f10e0013453964de7d3
tests/unit/cycle/test_project_memory_cycle_domain.py 783aef1e86191a68481f818b333a47e8a1da17affe7d2791d3824fbd12e4031d
tests/unit/next_action/test_next_action_domain.py 1a1525c4509302b6f5aaa4ff19965cd4e1680b5e3543db571af38c7067261449
tests/unit/task_authority/test_external_task_authority_domain.py f1b83cd299ac8f6bef239f18aa6206da5034a04ae2d9a5693ff760c1325e0ffd
tests/unit/workflow/test_state_machine.py 7f0501684a30211ab43b7bb9bdae389934c3558a28da266c94254f0fdb867752
```

---

# 5. must read

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
.aiassistant/tasks/done/20260902_0232_aiscc-p1-8-runtime-prerequisite-authority-expanded-path-implementation-rework-1.md
migrations/versions/20260901_0008_p1_8_prerequisite_authority_reconciliation.py
src/aiscc/persistence/models.py
src/aiscc/persistence/repository.py
src/aiscc/workflow/models.py
src/aiscc/workflow/guards.py
tests/integration/providers/test_execution_persistence.py
```

Read only the exact supporting symbols imported or invoked by the failing test and Alembic metadata diff. Do not
bulk-read unrelated source, rules, records or logs.

---

# 6. exact mutation allowlist

Only these three product/test/migration paths may be modified:

```text
migrations/versions/20260901_0008_p1_8_prerequisite_authority_reconciliation.py
src/aiscc/persistence/models.py
tests/integration/providers/test_execution_persistence.py
```

Task lifecycle and ignored target bundle are additionally allowed:

```text
.aiassistant/tasks/active/20260902_1100_aiscc-p1-8-runtime-provider-regression-and-metadata-parity-rework-1.md
.aiassistant/tasks/done/20260902_1100_aiscc-p1-8-runtime-provider-regression-and-metadata-parity-rework-1.md
.aiassistant/reports/target/20260902_1100_aiscc-p1-8-runtime-provider-regression-and-metadata-parity-rework-1/**
```

All other predecessor candidate paths remain byte-immutable for this turn. If a different path is materially
required, stop before touching it:

```text
EVIDENCE_SCOPE_EXPANSION_REQUIRED / RUNTIME_PATH_BOUNDARY_INSUFFICIENT
```

Do not shoehorn behavior into an allowed but semantically wrong owner.

---

# 7. required repair A — provider regression

Repair only the existing provider integration test contract for:

```text
test_provider_returned_tool_is_denied_when_accepted_transition_leaves_running
```

The test must continue to prove the actual accepted behavior:

- the provider-returned tool is denied;
- the accepted transition leaves `RUNNING` and enters `BLOCKED`;
- admission carries exactly one typed `P1_4BlockerClaimV1`;
- the claim uses the accepted kind/reason mapping derived from the actual denial, not an invented pair;
- source authority/ref/event/fingerprint is independently verifier-resolvable;
- blocker provenance and WorkRun projection are committed atomically;
- the test does not bypass, mock away, weaken or remove mandatory blocker admission;
- production code is not changed merely to preserve an obsolete test helper contract.

If the test cannot express the accepted runtime contract within this exact path using existing public/read-verifier
interfaces, stop and report the exact missing owner/path. Do not expose a private writer or widen a public API.

---

# 8. required repair B — Alembic metadata parity

Make `alembic check` return PASS while preserving the accepted additive `0008` schema and ORM runtime behavior.

Reconcile exactly the reported drift:

- `ondelete=RESTRICT` parity for Task/context event-sequence foreign keys;
- `ondelete=RESTRICT` parity for P1-4 blocker request/decision/attestation foreign keys;
- unique-constraint name parity for both `issuance_sequence` constraints;
- index-name parity for blocker `work_run_id` and Task snapshot high-watermark;
- mapped ORM foreign-key parity for `project_memory_entries.external_context_ref`.

Required boundaries:

- `0008` remains `revision = 20260901_0008` and `down_revision = 20260831_0007`;
- single linear head;
- additive only;
- no rewrite of `0006` or `0007`;
- no historical backfill or accepted-row mutation;
- no deletion of an intended constraint/index merely to silence autogenerate;
- migration and ORM metadata must describe the same intended database contract.

---

# 9. preserved contracts

The following remain binding and must not be weakened:

- all 22 accepted JCS/safe-integer fingerprints;
- global normative integer ceiling `9007199254740991`;
- external Task authority private writer and public read/verifier separation;
- P1-4 mandatory typed blocker claim and atomic transaction ownership;
- Cycle/Memory/NextAction external-owner verification/currentness/replay;
- immutable `0006`, `0007`, and `src/aiscc/judgment/authority.py` bytes;
- P1-6 carrier and P1-7 Judgment authority non-substitution;
- no caller/backfill/hash-only grandfathering.

---

# 10. evidence contract

## executor_required

Fresh-run evidence:

1. preflight branch/HEAD/index/candidate hash inventory;
2. exact failing provider test: PASS;
3. original five targeted unit files: all PASS;
4. original five targeted PostgreSQL integration files: all PASS;
5. complete repository collection count;
6. complete repository pytest: zero failures, zero unexpected skips/deselections;
7. `ruff check .`: PASS;
8. `mypy src`: PASS;
9. fresh disposable PostgreSQL upgrade base -> `20260901_0008`: PASS;
10. `alembic current`: `20260901_0008 (head)`;
11. `alembic check`: PASS;
12. 22 accepted fingerprints reproduced exactly;
13. immutable baseline hashes unchanged;
14. final runtime candidate inventory and aggregate;
15. UTF-8/control-character/Markdown/diff checks;
16. final Docker/test residue and Git inventory.

No real provider/tool/network/credential action is required.

## reuse_allowed

- accepted joint design bytes and lineage;
- 0050 owner/path audit;
- 0232 targeted implementation proof only where unchanged applicability is proven;
- accepted 22 fingerprint expected values.

Reused evidence does not replace fresh full regression or fresh Alembic parity proof.

## human_owned

```text
P1-8 runtime final review: HUMAN_PENDING
```

Human verification begins only after this Task produces a Command Center-accepted candidate.

## not_required

- browser/visual QA;
- real provider/tool calls;
- Project Source mirror;
- deployment/Public Live;
- P2/P3;
- Git commit/push.

## forbidden

- Agent-minted runtime or Human acceptance;
- `xfail`, deselection, collection reduction or assertion weakening to hide the regression;
- weakening/removing mandatory typed blocker admission;
- exposing the external Task authority private writer;
- Git index/commit/push;
- credentialed/network action;
- unrelated cleanup or mutation.

---

# 11. accept criteria

Successful Executor result is only:

```text
P1-8 Runtime:
REWORKED_CANDIDATE /
COMMAND_CENTER_REVIEW_REQUIRED /
HUMAN_PENDING
```

All of the following are required:

- only the three exact allowed paths changed;
- failing provider regression repaired without contract weakening;
- `alembic check` passes with intended schema parity;
- all targeted and complete tests pass;
- 22 fingerprints and immutable bytes remain exact;
- report/export/manifest is complete;
- no forbidden action occurred.

Executor does not declare `ACCEPTED`, `CLOSED`, Human acceptance, terminal judgment or P1 completion.

---

# 12. hold/reject and mandatory stop

Stop with the narrowest exact blocker if any of the following occurs:

- predecessor candidate identity mismatch;
- another source/test/migration path is required;
- provider test requires private writer exposure or production contract weakening;
- migration/ORM parity requires destructive or predecessor migration rewrite;
- any targeted/full/static/Alembic verification fails;
- unexpected dirty path or forbidden action appears.

After a named blocker, perform only minimal blocker evidence, final workspace inventory, report/export and safe
stop.

---

# 13. Git and governance

Forbidden:

```text
git add
git commit
git push
deployment
Project Source upload
terminal Cycle/Judgment creation
```

Move the exact Task from active to done only after Executor-required work/report/export is complete. `done` means
submission readiness, not acceptance.

---

# 14. export bundle

Target:

```text
.aiassistant/reports/target/20260902_1100_aiscc-p1-8-runtime-provider-regression-and-metadata-parity-rework-1/
```

Required root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `TEST_EVIDENCE.md`
- `MIGRATION_EVIDENCE.md`
- `FINGERPRINT_EVIDENCE.md`
- `RUNTIME_INVENTORY.md`
- all three allowed paths preserving repository-relative paths, whether changed or unchanged
- immutable `0006`, `0007`, and `src/aiscc/judgment/authority.py` evidence copies
- `REMOVED_FILES.md` only if deletion occurred; deletion is not expected

Manifest must list actual bytes and SHA-256 for every payload except itself.

---

# 15. report and final response

Report:

- exact task path/SHA;
- read paths and source symbols;
- workspace before/after;
- predecessor and final runtime aggregate;
- exact changed/unchanged paths;
- provider regression repair and proof;
- Alembic metadata repair and proof;
- targeted/full/static/migration counts;
- fingerprint and immutable baseline results;
- Human status;
- forbidden-not-run actions;
- unverified items;
- rollback guide;
- preserved exact paths.

Final response:

1. result;
2. target bundle path;
3. changed files;
4. removed files;
5. Human verification status;
6. unverified items;
7. preserved exact paths.
