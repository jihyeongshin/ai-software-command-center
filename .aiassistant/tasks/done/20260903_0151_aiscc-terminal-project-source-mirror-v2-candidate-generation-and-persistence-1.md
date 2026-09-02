# 작업지시서: Terminal Project Source mirror v2 candidate generation and persistence

## meta

- task_id: `20260903_0151_aiscc-terminal-project-source-mirror-v2-candidate-generation-and-persistence-1`
- created_at: `2026-09-03T01:51:00+09:00`
- project: `AI Software Command Center (AISCC)`
- phase: `P1 terminal maintenance / P2 entry operational pre-step`
- work_type: `MIRROR_V2_CANDIDATE_GENERATION / GIT_PERSISTENCE`
- evidence_profile: `GOVERNANCE_HIGH`
- execution_mode: `MANUAL_COMMAND_CENTER`
- predecessor_terminal_commit: `b9ed57feb595b3a670b644a213c184f958956924`
- predecessor_terminal_tree: `7886c8592669dc9d26bb339f2248d3a1c6bc03aa`
- predecessor_judgment_cycle: `.aiassistant/records/aiscc/cycles/20260903_0149_aiscc-terminal-project-source-mirror-refresh-preflight-acceptance-and-v2-candidate-authority-1.cycle.md`
- predecessor_audit_task: `.aiassistant/tasks/done/20260903_0107_aiscc-terminal-project-source-mirror-refresh-preflight-audit-1.md`
- target_bundle: `.aiassistant/reports/target/20260903_0151_aiscc-terminal-project-source-mirror-v2-candidate-generation-and-persistence-1/`
- fresh_chat_policy: `NO_NEW_CHAT_REQUIRED / SAME_FRESH_SESSION_ALLOWED`
- success_boundary: `MIRROR_V2_CANDIDATE_COMMIT_CREATED / GENERATED_BUNDLE_22_VERIFIED / COMMAND_CENTER_REVIEW_REQUIRED`

## 0. authority

Accepted terminal canonical remains:

```text
HEAD:
b9ed57feb595b3a670b644a213c184f958956924

P1:
ACCEPTED / CLOSED

P2:
NOT_STARTED / ENTRY_READY

next roadmap item:
P2-1 Command Center Web UI
```

The 0149 Command Center Cycle accepts the 0107 preflight and authorizes one mirror-v2 candidate preparation turn.

This Task does **not** authorize Browser Project Source deletion/upload/replacement.

## 1. exact goal

1. transport exact current Task + exact 0149 Cycle;
2. revalidate terminal repository baseline and exact existing provenance dirt;
3. modify exactly the Project Source registry;
4. add exactly one v2 manifest;
5. add exactly one Python mirror generator at the rule-named path;
6. validate the Python generator and exact v2 manifest;
7. generate the exact ignored 22-file v2 bundle without touching v1 output;
8. verify every generated mirror metadata/body/hash/filename and Git-ignore property;
9. move current Task active→matching done;
10. stage exactly seven tracked paths;
11. create exactly one candidate-preparation commit;
12. export tracked and generated candidate evidence;
13. stop for Browser Command Center review.

## 2. non-goals / forbidden

Do not:

- modify any terminal canonical source/state/rule/baseline/handoff body;
- modify v1 manifest;
- modify v1 PowerShell generator;
- modify `.gitignore` unless this Task's exact existing v2 output is unexpectedly not ignored — in that case STOP,
  do not expand scope;
- upload/remove/replace Browser Project Source;
- update v2 status to Human-synchronized;
- start P2/P2-1 implementation;
- push/fetch/pull/network/deploy;
- alter Git configuration;
- use broad staging/cleanup.

Forbidden:

```text
git add .
git add -A
git restore .
git checkout .
git reset --hard
git clean
git stash
git commit --amend
git rebase
git merge
git revert
```

## 3. Downloads transport

Exactly two Downloads files:

```text
C:\Users\oracl\Downloads\20260903_0151_aiscc-terminal-project-source-mirror-v2-candidate-generation-and-persistence-1.md
C:\Users\oracl\Downloads\20260903_0149_aiscc-terminal-project-source-mirror-refresh-preflight-acceptance-and-v2-candidate-authority-1.cycle.md
```

Destinations:

```text
.aiassistant/tasks/active/20260903_0151_aiscc-terminal-project-source-mirror-v2-candidate-generation-and-persistence-1.md
.aiassistant/records/aiscc/cycles/20260903_0149_aiscc-terminal-project-source-mirror-refresh-preflight-acceptance-and-v2-candidate-authority-1.cycle.md
```

0149 Cycle expected SHA-256:

```text
324f18146ee919856c788f0eb49e0e5cfaabed6979a8f3a2e84669b7f7597f2a
```

Before either Move:

1. both exact source files exist;
2. both exact destinations do not exist;
3. 0149 Cycle SHA-256 exact match.

Failure:

```text
move neither
do not search alternate Downloads path
do not overwrite/delete
STOP: TRANSPORT_PRECONDITION_FAILED
```

All PASS:

- Move exactly both files, not Copy;
- verify destination identity and source absence.

## 4. session

Reuse current IDE Executor session.

No new chat is required.

If any out-of-Task runtime/index/commit mutation is detected after the accepted terminal commit, do not reset or
repair it. Stop before tracked mirror mutation and report exact drift.

## 5. minimum authoritative context

Read exact:

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md
.aiassistant/rules/AISCC_PROJECT_SOURCE_MIRROR.md

.aiassistant/project-sources/PROJECT_SOURCE_BUNDLE_REGISTRY.md
.aiassistant/project-sources/manifests/aiscc-project-source-mirror-v1.json
scripts/generate_project_source_bundle.ps1

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/reports/aiscc/20260902_2331_aiscc-p1-completion-p2-entry-handoff-1.md

.aiassistant/records/aiscc/cycles/20260903_0105_aiscc-p1-terminal-closure-persistence-substantive-acceptance-1.cycle.md
.aiassistant/tasks/done/20260903_0107_aiscc-terminal-project-source-mirror-refresh-preflight-audit-1.md
.aiassistant/records/aiscc/cycles/20260903_0149_aiscc-terminal-project-source-mirror-refresh-preflight-acceptance-and-v2-candidate-authority-1.cycle.md
.aiassistant/tasks/active/20260903_0151_aiscc-terminal-project-source-mirror-v2-candidate-generation-and-persistence-1.md
```

Do not bulk-read unrelated source/logs.

## 6. repository preflight

Require before tracked mutation:

```text
repository == ai-software-command-center
branch == main
HEAD == b9ed57feb595b3a670b644a213c184f958956924
HEAD tree == 7886c8592669dc9d26bb339f2248d3a1c6bc03aa
HEAD parent == c9004e89ae9ed961d7cabe6e3eca1100ef4a13cc
index changes == 0
runtime/source/test/migration dirt == 0
```

Before current 0149 Cycle transport, expected Git-visible dirt is exactly:

```text
.aiassistant/records/aiscc/cycles/20260903_0105_aiscc-p1-terminal-closure-persistence-substantive-acceptance-1.cycle.md
.aiassistant/tasks/done/20260903_0107_aiscc-terminal-project-source-mirror-refresh-preflight-audit-1.md
```

After current transport while Task active remains ignored, expected Git-visible dirt is exactly those two plus:

```text
.aiassistant/records/aiscc/cycles/20260903_0149_aiscc-terminal-project-source-mirror-refresh-preflight-acceptance-and-v2-candidate-authority-1.cycle.md
```

No fourth path is allowed before the authorized tracked edits begin.

If mismatch occurs, do not auto-expand. STOP with exact drift evidence.

## 7. pre-mutation identity guard

Require these exact tracked identities against terminal HEAD:

```text
.aiassistant/project-sources/PROJECT_SOURCE_BUNDLE_REGISTRY.md
SHA-256:
fc38e92d1c43f6e1deeb80fd78ea0289b98577951374ce3b9409866530d573d2

.aiassistant/project-sources/manifests/aiscc-project-source-mirror-v1.json
SHA-256:
5bfe1f0004d0b7f419eb322d68c7b523d03ec7b8759539849b1a35f043db0c62

.aiassistant/rules/AISCC_PROJECT_SOURCE_MIRROR.md
SHA-256:
d02f823a03cebeeb14b33994a8fd93a4f695bef813c097ef651f129ae0aab6c0

scripts/generate_project_source_bundle.ps1
SHA-256:
65c39f9a96f8b74b3f0083ca0609c29df734821f3d46c896f9dcebf5c1ea1703
```

Require absent:

```text
.aiassistant/project-sources/manifests/aiscc-project-source-mirror-v2.json
scripts/generate_project_source_bundle.py
.aiassistant/project-sources/bundles/aiscc/AISCC-PROJECT-SOURCE-MIRROR-V2/
```

If any identity/absence guard fails, do not overwrite or delete. STOP.

## 8. exact registry mutation contract

Modify only:

```text
.aiassistant/project-sources/PROJECT_SOURCE_BUNDLE_REGISTRY.md
```

Preserve authority/ownership history but correct current literal state.

Required current facts after edit:

```text
Bootstrap Seed v1:
RETIRED / ACTIVE 0

AISCC-PROJECT-SOURCE-MIRROR-V1:
ACTIVE / HUMAN_SYNC_CONFIRMED / 18

v1 canonical commit:
0dc4e19a6da31c22e08d144eaba24209a4476b4d

repository terminal canonical:
b9ed57feb595b3a670b644a213c184f958956924

AISCC-PROJECT-SOURCE-MIRROR-V2:
REGENERATED_CANDIDATE / COMMAND_CENTER_REVIEW_PENDING

v2 Browser sync:
NOT_EXECUTED / HUMAN_PENDING

v2 expected active count:
22

source mirror current Browser authority:
V1 until Human complete replacement of accepted V2
```

Registered bundle rows must preserve v1 and add v2.

Do not claim:

```text
V2 ACTIVE
V2 SYNCED
SOURCE_MIRROR_SYNCED
```

## 9. exact v2 manifest contract

Add exactly:

```text
.aiassistant/project-sources/manifests/aiscc-project-source-mirror-v2.json
```

UTF-8 without BOM, deterministic 2-space JSON, final newline.

Root properties exactly in this order:

```text
bundle_id
target_gpt_project
project_scope
canonical_commit
generated_by_task
generated_at
expected_active_count
source_mirror_sync_status
optional_mapping
mapping
```

Exact scalar values:

```text
bundle_id:
AISCC-PROJECT-SOURCE-MIRROR-V2

target_gpt_project:
AI Software Command Center

project_scope:
AISCC Browser Command Center canonical read-only mirror

canonical_commit:
b9ed57feb595b3a670b644a213c184f958956924

generated_by_task:
20260903_0151_aiscc-terminal-project-source-mirror-v2-candidate-generation-and-persistence-1

generated_at:
2026-09-03T01:51:00+09:00

expected_active_count:
22

source_mirror_sync_status:
PENDING_COMMAND_CENTER_REVIEW

optional_mapping:
[]
```

Each mapping row properties exactly:

```text
project_source_filename
canonical_path
group
role
canonical_sha256
upload_status
```

`upload_status` exact for all rows:

```text
REGENERATED_CANDIDATE
```

Exact case-sensitive 22 mappings:

| Project Source filename | Canonical path | Group | Role | Canonical SHA-256 |
|---|---|---|---|---|
| `00_AISCC_STATE__CURRENT_STATE_SUMMARY.md` | `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md` | `STATE` | `accepted project/phase/authority snapshot` | `9a67b2c3df6feeac7ca02ff0fa0126a88567bbc7f65a136c174dce705d0c72ca` |
| `01_AISCC_STATE__DECISION_REGISTER.md` | `.aiassistant/records/aiscc/DECISION_REGISTER.md` | `STATE` | `accepted decision and deferred implementation boundary` | `dd942172b95815f8872287e45e45ce9b4b7c4755ea4a4eafdb6d2fbebba60a24` |
| `02_AISCC_STATE__NEXT_ACTIONS.md` | `.aiassistant/records/aiscc/NEXT_ACTIONS.md` | `STATE` | `stable canonical queue and release invariant` | `9917589884df0dfd00d2350e3498e48c323cc4faa0c70ebda18c61b6b65180d4` |
| `10_AISCC_RULES__AGENTS.md` | `.aiassistant/rules/AISCC_AGENTS.md` | `RULES` | `instruction transport vs project authority` | `fffa447db7388b34d54cdec9d9e3ed4fb58f2f5289d48173efdd8e4c371b3565` |
| `11_AISCC_RULES__EXECUTOR_REPORT_EXPORT.md` | `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md` | `RULES` | `executor lifecycle/report/export` | `e5486b63321ecda069c0ba7b1b6a28ddc707902f77bbe1f9ca2271322b1c9ae9` |
| `12_AISCC_RULES__ASSET_GIT_AND_ENCODING_POLICY.md` | `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md` | `RULES` | `tracked/ignored/provenance/encoding` | `190a903ecc3eb1364503c04c5e1c09a9ca1d50d4fbe9038d5eb25216e72d7c2e` |
| `13_AISCC_RULES__PROJECT_SOURCE_MIRROR.md` | `.aiassistant/rules/AISCC_PROJECT_SOURCE_MIRROR.md` | `RULES` | `canonical/mirror lifecycle` | `d02f823a03cebeeb14b33994a8fd93a4f695bef813c097ef651f129ae0aab6c0` |
| `14_AISCC_RULES__DOCUMENT_LANGUAGE_POLICY.md` | `.aiassistant/rules/AISCC_DOCUMENT_LANGUAGE_POLICY.md` | `RULES` | `Korean-first and claim wording policy` | `1856c09ffd1f1a21ae7d621583ee01f42112af8407372d4c5ddac78f5565e773` |
| `20_AISCC_COMMAND_CENTER__README.md` | `.aiassistant/records/command-center/README.md` | `COMMAND_CENTER` | `command-center artifact chain` | `bc637bcca96f88dec83cbae4a0019d5934ee0a3b2016aaa67e6a90a72a27bc33` |
| `21_AISCC_COMMAND_CENTER__WORKFLOW.md` | `.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md` | `COMMAND_CENTER` | `Task/Evidence/Judgment/Cycle workflow` | `d1348cccec5130259834132e83a38d9fc8d18e401f646c1f0655b3510ef63ab8` |
| `22_AISCC_COMMAND_CENTER__TASK_FILE_TEMPLATE.md` | `.aiassistant/records/command-center/TASK_FILE_TEMPLATE.md` | `COMMAND_CENTER` | `Task Contract template` | `01ed89d33851fb861a07e58c48314b74710df4893ceb5e80540bc43c497f7e99` |
| `23_AISCC_COMMAND_CENTER__SHORT_EXECUTOR_PROMPT_TEMPLATE.md` | `.aiassistant/records/command-center/SHORT_EXECUTOR_PROMPT_TEMPLATE.md` | `COMMAND_CENTER` | `short IDE transport prompt` | `4bd333699ce0a561ec360e823faefb3b4ce20b880437809222e263fae0284742` |
| `24_AISCC_COMMAND_CENTER__JUDGMENT_RUBRIC.md` | `.aiassistant/records/command-center/JUDGMENT_RUBRIC.md` | `COMMAND_CENTER` | `evidence/admission/judgment criteria` | `14e635e288c3907d912110c547ec45be4ffa8eeacc2ca6e27f545387d0593f67` |
| `25_AISCC_COMMAND_CENTER__CYCLE_RECORD_TEMPLATE.md` | `.aiassistant/records/command-center/CYCLE_RECORD_TEMPLATE.md` | `COMMAND_CENTER` | `durable Cycle template` | `286e18c1be20951885bccb72407a8ac8e419fd60fb3305e39a3182d2f069ed13` |
| `26_AISCC_COMMAND_CENTER__NEXT_ACTION_SELECTION_RUBRIC.md` | `.aiassistant/records/command-center/NEXT_ACTION_SELECTION_RUBRIC.md` | `COMMAND_CENTER` | `next-action ordering` | `e4be8bf7b18d46bedd6ca253908dcbcf06e8ee85da29e1d092541330aa3b492c` |
| `30_AISCC_BASELINE__PRODUCT_THESIS.md` | `.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md` | `BASELINE` | `accepted product thesis` | `359d46cfddb10cb9efd85046383b9405869fe2a74f4e66637032915a802eeeb0` |
| `31_AISCC_BASELINE__PRIOR_ART_BOUNDARY.md` | `.aiassistant/reports/aiscc/AISCC_PRIOR_ART_BOUNDARY.md` | `BASELINE` | `prior-art / DO-NOT-CLAIM boundary` | `c7cfdcaeddde8eaec384e72a56070e0924de658dbb3db14a729391d41726a0df` |
| `32_AISCC_BASELINE__COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md` | `.aiassistant/reports/aiscc/AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md` | `BASELINE` | `public Replay/Live/runtime boundary` | `cc5237cd4c0adc7eba0927a36158807bd9c9e4e76b1d31e09525cdaffe093e73` |
| `33_AISCC_BASELINE__ARCHITECTURE.md` | `.aiassistant/rules/AISCC_ARCHITECTURE.md` | `BASELINE` | `accepted core domain and authority architecture` | `f38d90bb3feca83e88f0d67ea5f289c85568334dc4007898925351f8f451e8ef` |
| `34_AISCC_BASELINE__ORCHESTRATION.md` | `.aiassistant/rules/AISCC_ORCHESTRATION.md` | `BASELINE` | `accepted explicit state machine and transition contract` | `b4d6c8646a2defe060634fea86eb503d96f9dbfa9e31f06c7a34786c23828b4b` |
| `35_AISCC_BASELINE__SECURITY_SANDBOX.md` | `.aiassistant/rules/AISCC_SECURITY_SANDBOX.md` | `BASELINE` | `accepted security, sandbox, and runtime boundary` | `d11539925b3025b385dec2146dfa30193fc80dbbbd8b71ce4deccb219ba5738b` |
| `40_AISCC_HANDOFF__P1_COMPLETION_P2_ENTRY.md` | `.aiassistant/reports/aiscc/20260902_2331_aiscc-p1-completion-p2-entry-handoff-1.md` | `HANDOFF` | `accepted P1 closure and P2 entry-ready handoff` | `df792ea78a7e67ac35066fc1e859e1ecf9133965e3c6bc7f83a22539da082935` |

No 23rd mapping. No duplicate filename/path. Do not map manifest/registry/Cycle/Task history into the Browser active set.

## 10. Python generator implementation contract

Add exactly:

```text
scripts/generate_project_source_bundle.py
```

Requirements:

### 10.1 CLI

Support exactly the intended invocation:

```powershell
.\.venv\Scripts\python.exe scripts/generate_project_source_bundle.py --repository-root . --manifest .aiassistant/project-sources/manifests/aiscc-project-source-mirror-v2.json
```

The implementation may accept absolute normalized equivalents for those two arguments but must fail closed on a
manifest outside:

```text
.aiassistant/project-sources/manifests/
```

### 10.2 manifest-driven behavior

Do not hard-code v2 bundle ID, commit hash, mapping count, generated task, or generated timestamp as generator
constants.

Read them from the manifest and validate schema/types/format.

Expected target/project scope may be validated against canonical constants:

```text
AI Software Command Center
AISCC Browser Command Center canonical read-only mirror
```

### 10.3 canonical source ownership

For each mapping, source canonical bytes from exact Git object:

```text
<manifest canonical_commit>:<canonical_path>
```

Do not use mutable worktree bytes as the mirror body authority.

Also require:

- canonical commit resolves exactly to one local commit;
- canonical path is repository-relative, normalized, safe, no `..`, no backslash traversal;
- object exists and is a blob;
- SHA-256 of exact Git blob equals manifest `canonical_sha256`;
- decoded source is strict UTF-8 without BOM;
- source path is an allowed `.md` path under `.aiassistant/rules/`, `.aiassistant/records/`, or `.aiassistant/reports/aiscc/`;
- deny secret/private filename/path markers and high-confidence private-key/API-key patterns.

### 10.4 manifest integrity

Fail on:

- unexpected/missing root keys;
- unexpected/missing mapping keys;
- invalid SHA format;
- invalid timestamp format/offset;
- expected count mismatch;
- optional mapping non-empty for this candidate;
- duplicate filenames, including case-insensitive duplicate;
- duplicate canonical paths, including case-insensitive duplicate;
- output filename not matching the mirror filename convention;
- mapping count != expected active count.

### 10.5 Markdown/text integrity

For each canonical body and generated output:

- strict UTF-8;
- no BOM;
- no NUL;
- reject prohibited C0 control bytes except TAB/LF/CR where applicable;
- reject trailing spaces/tabs on lines;
- validate Markdown fenced-code delimiter balance using a deterministic rule documented in code/report;
- do not normalize or rewrite canonical body bytes.

### 10.6 exact metadata header

Every generated file starts with:

```text
# AISCC Project Source Mirror Metadata

- mirror_type: `GPT_PROJECT_SOURCE_READ_ONLY_MIRROR`
- canonical_path: `<exact canonical_path>`
- project_source_filename: `<exact filename>`
- canonical_owner: `AISCC repository`
- mirror_owner: `AI Software Command Center Browser Project`
- mirror_generated_by_task: `<manifest generated_by_task>`
- mirrored_at: `<manifest generated_at>`
- canonical_commit: `<manifest canonical_commit>`
- canonical_sha256: `<mapping canonical_sha256>`
- authority: `READ_ONLY_MIRROR`
- do_not_edit_in_project_source: `true`

<!-- AISCC_CANONICAL_BODY_START -->
```

followed by exactly one LF and then the literal canonical Git-blob body bytes.

### 10.7 output safety

Output root must be derived only from validated `bundle_id` and resolve exactly under:

```text
.aiassistant/project-sources/bundles/aiscc/
```

For this manifest it must resolve exactly to:

```text
.aiassistant/project-sources/bundles/aiscc/AISCC-PROJECT-SOURCE-MIRROR-V2/
```

Require the exact v2 output directory to be absent before generation. Do not delete or overwrite an existing v2
directory.

Never modify/delete:

```text
.aiassistant/project-sources/bundles/aiscc/AISCC-PROJECT-SOURCE-MIRROR-V1/
```

### 10.8 post-write verification

After writing all files, re-read every generated file and verify:

- exact generated count 22;
- exact filename set;
- metadata values exact;
- canonical body extracted after marker exactly equals Git-blob bytes;
- body SHA-256 exact manifest hash;
- full generated file UTF-8/no-BOM/control/trailing-whitespace/fence validation;
- every generated path is Git-ignored;
- no generated file is Git-visible in `git status --porcelain`.

On any failure, report error. Do not silently repair canonical source or manifest.

## 11. local validation / generation

Before generation:

```text
python -m py_compile scripts/generate_project_source_bundle.py
```

Use repository-local Python / `.venv` if already present. Do not install packages or access network.

Execute exactly the intended v2 generator command.

Required result:

```text
GENERATED_PASS
bundle=AISCC-PROJECT-SOURCE-MIRROR-V2
files=22
canonical_commit=b9ed57feb595b3a670b644a213c184f958956924
```

The exact 22 generated files must remain ignored.

## 12. tracked mutation scope before Task lifecycle

After registry/manifest/generator edits and v2 generation, Git-visible content/provenance changes must be exactly:

```text
.aiassistant/records/aiscc/cycles/20260903_0105_aiscc-p1-terminal-closure-persistence-substantive-acceptance-1.cycle.md
.aiassistant/tasks/done/20260903_0107_aiscc-terminal-project-source-mirror-refresh-preflight-audit-1.md
.aiassistant/records/aiscc/cycles/20260903_0149_aiscc-terminal-project-source-mirror-refresh-preflight-acceptance-and-v2-candidate-authority-1.cycle.md
.aiassistant/project-sources/PROJECT_SOURCE_BUNDLE_REGISTRY.md
.aiassistant/project-sources/manifests/aiscc-project-source-mirror-v2.json
scripts/generate_project_source_bundle.py
```

Count:

```text
6
```

Require v1 manifest, v1 PowerShell generator, mirror rule and terminal canonical files clean against HEAD.

## 13. current Task lifecycle

After successful generator verification and before staging:

```text
.aiassistant/tasks/active/20260903_0151_aiscc-terminal-project-source-mirror-v2-candidate-generation-and-persistence-1.md
→
.aiassistant/tasks/done/20260903_0151_aiscc-terminal-project-source-mirror-v2-candidate-generation-and-persistence-1.md
```

Move, not Copy.

Matching done destination must be absent.

After lifecycle, exact Git-visible set must be Section 12 six plus current Task done:

```text
7 paths
```

No eighth path.

## 14. staging

Stage exactly the seven tracked paths with explicit pathspecs.

Do not broad-stage.

Require:

```text
staged count == 7
staged set == exact seven
unstaged Git-visible dirt == 0
runtime/source/test/migration staged == 0
terminal canonical state/handoff staged == 0
mirror rule staged == 0
v1 manifest staged == 0
v1 PowerShell generator staged == 0
generated bundle staged == 0
```

## 15. candidate-preparation commit

Authorized message:

```text
feat(governance): prepare terminal Project Source mirror v2
```

Create exactly one commit.

Require:

```text
parent == b9ed57feb595b3a670b644a213c184f958956924
parent count == 1
merge parent count == 0
changed path count == 7
changed path set == exact Section 13 set
runtime/source/test/migration changed == 0
terminal canonical body changed == 0
mirror rule changed == 0
v1 manifest/generator changed == 0
generated bundle changed/tracked == 0
```

No amend or second repair commit.

If Git author identity is unavailable, stop without changing Git config.

## 16. post-commit state

Prove:

- branch `main`;
- HEAD is the one new candidate-preparation commit;
- parent exact terminal closure commit;
- index empty;
- Git-visible worktree dirt `0`;
- runtime dirt `0`;
- terminal canonical three/handoff clean;
- exact generated v2 directory still exists with 22 files and remains ignored;
- v1 output, if it existed pre-task, was not modified/deleted;
- no Browser source action occurred.

Do not claim candidate commit or v2 mirror accepted.

## 17. required export

Target:

```text
.aiassistant/reports/target/20260903_0151_aiscc-terminal-project-source-mirror-v2-candidate-generation-and-persistence-1/
```

Required root Markdown:

```text
TASK.md
EXECUTOR_REPORT.md
GIT_OBJECT_EVIDENCE.md
MIRROR_V2_VALIDATION.md
BROWSER_REPLACEMENT_PLAN.md
EXPORT_MANIFEST.md
```

Export byte-exact copies preserving repository-relative paths of:

Tracked candidate:

- modified registry from candidate commit tree;
- new v2 manifest from candidate commit tree;
- new Python generator from candidate commit tree;
- 0149 Cycle from candidate commit tree;
- 0105 Cycle from candidate commit tree;
- 0107 done Task from candidate commit tree;
- current 0151 done Task from candidate commit tree.

Generated candidate:

- all exact 22 files under:
  `.aiassistant/project-sources/bundles/aiscc/AISCC-PROJECT-SOURCE-MIRROR-V2/`

Also export exact v1 manifest, v1 PowerShell generator and mirror rule as unchanged reference copies.

`MIRROR_V2_VALIDATION.md` must include per generated file:

```text
filename
canonical_path
canonical SHA-256
generated full-file SHA-256
body SHA-256
metadata PASS/FAIL
body identity PASS/FAIL
UTF-8/control/fence/trailing-whitespace PASS/FAIL
Git-ignore PASS/FAIL
```

`BROWSER_REPLACEMENT_PLAN.md` must list:

- current v1 18 filenames to remove;
- candidate v2 22 filenames to upload;
- target Browser Project;
- exact canonical commit;
- exact bundle ID;
- Human capacity gate = pending;
- complete replacement requirement;
- required post-upload Human confirmation fields.

Manifest binds every exported payload except itself with bytes and SHA-256.

## 18. Browser capacity / Human boundary

This Task does not infer capacity from subscription or UI assumptions.

It may generate and validate the exact required 22-file candidate.

After Command Center accepts the candidate, Human must confirm the Browser Project can hold all 22 required files
before complete replacement.

If capacity is insufficient:

```text
do not partially replace
do not silently drop mappings
return to Command Center for active-set policy decision
```

## 19. evidence contract

### executor_required

- transport identity;
- terminal repository preflight;
- exact pre-mutation identities;
- registry mutation evidence;
- exact v2 manifest validation;
- Python generator static validation;
- exact 22-file generation and post-write validation;
- Task lifecycle;
- exact seven staging/commit proof;
- generated bundle export/manifest.

### reuse_allowed

- accepted terminal commit;
- accepted 0107 preflight mapping hashes/coverage only while source identities remain exact.

### human_owned

- Browser capacity confirmation;
- complete active-set replacement;
- post-upload sync confirmation.

### forbidden

- Browser source action;
- P2 start;
- runtime/canonical/rule mutation;
- v1 history mutation;
- broad staging/cleanup;
- network/push/deployment.

## 20. success / stop

Success:

```text
MIRROR_V2_CANDIDATE_COMMIT_CREATED
/ GENERATED_BUNDLE_22_VERIFIED
/ COMMAND_CENTER_REVIEW_REQUIRED
```

Do not declare:

```text
SOURCE_MIRROR_SYNCED
V2_BROWSER_ACTIVE
P2_STARTED
P2-1_STARTED
```

Mandatory stop before commit on any path/count/hash/schema/generator/ignore/runtime/canonical mismatch.

Post-commit discrepancy: export exact evidence, do not create a repair second commit.

## 21. preserved artifacts

Preserve:

- terminal closure commit `b9ed57feb595b3a670b644a213c184f958956924`;
- candidate-preparation commit if created;
- `.aiassistant/records/aiscc/cycles/20260903_0149_aiscc-terminal-project-source-mirror-refresh-preflight-acceptance-and-v2-candidate-authority-1.cycle.md`;
- `.aiassistant/tasks/done/20260903_0151_aiscc-terminal-project-source-mirror-v2-candidate-generation-and-persistence-1.md`;
- modified registry;
- v2 manifest;
- Python generator;
- v1 manifest and historical PowerShell generator unchanged.

Ignored v2 bundle may be retained through Human Browser replacement and removed only after sync evidence is accepted.
