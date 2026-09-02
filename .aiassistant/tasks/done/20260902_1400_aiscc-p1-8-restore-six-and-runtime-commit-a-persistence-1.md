# 작업지시서: P1-8 restore six and runtime Commit A persistence

## meta

- task_id: `20260902_1400_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-1`
- created_at: `2026-09-02T14:00:00+09:00`
- work_type: `REWORK / GIT_TERMINAL_PERSISTENCE`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a`
- primary_semantic_owner: `Human destructive-action authority / AISCC Command Center Git boundary`
- fresh_chat_policy: `NEW_CHAT_REQUIRED_BY_HUMAN`
- fresh_chat_reason: `1300은 read-only audit이었고 이번 Task는 exact destructive restore와 Git commit 권한을 새로 부여한다. Human이 새 IDE Executor 채팅을 열고 이 Task만 전달한다.`

## 현재 상태

- repository: `ai-software-command-center`
- expected branch / HEAD: `main / 1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a`
- expected index: empty
- Human P1-8 runtime final review: `HUMAN_PROVIDED / ACCEPTED`
- Human dirty-file disposition: `HUMAN_PROVIDED / RESTORE_SIX_TO_EXACT_HEAD`
- accepted runtime identity: exact 36 paths; corrected ordinal aggregate
  `a82d94c1d607bc379c12d0768ff54d0cd481467eb731e0884f63176bd1207f3c`
- legacy accepted identifier: `a1d5e9d24eabae3fec13e24cfb9d94e744e6687ca4c00889e85972fb5a633590`
- current runtime dirty set: 42 = accepted 36 + unaccepted tracked six
- current governance dirty set after Human places the updated 1355 Cycle: exact 11 untracked paths
- open blocker: exact six tracked formatting-shaped diffs must be restored before accepted-only Commit A staging.

## Human decision authority

Human selected the exact decision code:

```text
RESTORE_SIX_TO_EXACT_HEAD
```

Decision Cycle:

```text
.aiassistant/records/aiscc/cycles/20260902_1355_aiscc-p1-8-terminal-dirty-baseline-audit-acceptance-human-disposition-gate-1.cycle.md
SHA-256: a7ae3c92d3feba97e835a8962c6da0dd6cd66dea72732ae018cae056830e7116
```

This authority permits discarding only the six exact current byte states listed below and restoring each exact
path from the expected HEAD commit. It does not authorize restoration, cleanup, reset, or deletion of any other
path.

## 이번 턴 목표

1. 모든 precondition과 Human decision Cycle identity를 index mutation 전에 검증한다.
2. exact six current hashes와 HEAD blobs가 audit evidence와 일치하는 경우에만 six worktree paths를 HEAD로 복원한다.
3. 복원 후 runtime dirty set이 exact accepted 36인지 검증한다.
4. accepted 36만 staging하여 exact Commit A 하나를 생성한다.
5. Commit A parent/tree/path/blob proof와 final workspace evidence를 제출하고 중단한다.

## 이번 턴 비목표

- accepted 36 runtime bytes 수정
- canonical state/decision/next-actions 갱신
- P1 completion/P2 entry handoff 생성
- governance Commit B 생성
- final terminal Cycle 생성 또는 기존 Cycle 수정
- P1 CLOSED 선언, P2 시작, Project Source mirror 생성·업로드
- push, PR, release, deployment

## 허용 범위

allowed_restore_paths:

```text
src/aiscc/evidence/content.py
src/aiscc/evidence/models.py
src/aiscc/evidence/repository.py
src/aiscc/evidence/requirements.py
src/aiscc/evidence/service.py
src/aiscc/human/repository.py
```

allowed_commit_a_paths:

```text
migrations/versions/20260831_0006_p1_8_project_memory_cycle_admission.py
migrations/versions/20260831_0007_p1_8_authority_contract_rework.py
migrations/versions/20260901_0008_p1_8_prerequisite_authority_reconciliation.py
src/aiscc/contracts/canonical_json.py
src/aiscc/cycle/__init__.py
src/aiscc/cycle/models.py
src/aiscc/cycle/repository.py
src/aiscc/judgment/authority.py
src/aiscc/memory/__init__.py
src/aiscc/memory/models.py
src/aiscc/memory/repository.py
src/aiscc/next_action/__init__.py
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

allowed_actions:

- exact read-only Git/hash/token/AST preflight
- `git restore --source=1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a --worktree -- <exact six paths>`
- exact 36-path `git add -- <pathspecs>` only after restore/post-restore verification passes
- one non-merge Commit A with exact message and expected parent
- read-only post-commit Git object/tree/blob verification
- `git diff --check`, repository-local Ruff and mypy verification
- Task lifecycle `active -> done` only after report/export completion
- ignored target bundle and exact Commit A source-evidence copies

## 절대 금지

forbidden_paths_write:

- any path outside `allowed_restore_paths` before staging
- any accepted 36 path content
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
- every Cycle file
- `.aiassistant/reports/aiscc/**`
- `.gitignore`, repository configuration, CI/build configuration

forbidden_actions:

- broad `git restore`, `git checkout`, `git reset`, `git clean`, `git stash`
- restore from any commit other than exact expected HEAD
- deletion or recreation of the six paths
- staging governance/provenance or any path outside exact accepted 36
- more than one commit
- amend, rebase, merge, cherry-pick, push, PR, release, deployment
- canonical state/handoff update, Commit B, final acceptance/closure claim
- external network, credentials, provider/tool action, browser runtime
- unrelated source/rule/log bulk-read

## 읽을 문서

- repository-root `AGENTS.md` — transport bootstrap only
- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- current active Task
- `.aiassistant/records/aiscc/cycles/20260902_1222_aiscc-p1-8-runtime-human-final-acceptance-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260902_1300_aiscc-p1-8-terminal-persistence-precondition-blocked-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260902_1355_aiscc-p1-8-terminal-dirty-baseline-audit-acceptance-human-disposition-gate-1.cycle.md`
- `.aiassistant/tasks/done/20260902_1100_aiscc-p1-8-runtime-provider-regression-and-metadata-parity-rework-1.md`
- `.aiassistant/tasks/done/20260902_1222_aiscc-p1-8-runtime-final-acceptance-terminal-persistence-1.md`
- `.aiassistant/tasks/done/20260902_1300_aiscc-p1-8-terminal-dirty-baseline-provenance-reconciliation-audit-1.md`
- exact six restore paths and exact accepted 36 paths only as needed
- exact Git objects at expected HEAD for those paths

## agent instruction transport / authority

- Human opens the new IDE Executor chat; the Executor cannot open a chat itself.
- short prompt는 Task/Cycle placement와 Task 실행만 전달한다.
- repository-root instructions are transport bootstrap, not project policy authority.
- Task-listed canonical rules and evidence must be explicitly read.
- current Task, canonical rule, source, accepted evidence conflict 시 mutation 전에 mandatory stop한다.
- Human decision is exact-path scoped and must not be generalized to other dirty files.

## mandatory preflight — before restore or index mutation

### 1. Repository and identity

Require all:

```text
branch == main
HEAD == 1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a
index entry count == 0
1222 Human Cycle SHA-256 == f9bfb792e80b83d571066e3a72e18ba825bcf6a515e17606380492137993d77e
1300 blocker Cycle SHA-256 == 2c3808a6510ea947146965f97455659c8edba78ebe926fb00d14e9da2735582b
1355 decision Cycle SHA-256 == a7ae3c92d3feba97e835a8962c6da0dd6cd66dea72732ae018cae056830e7116
1300 done Task SHA-256 == e034d2c1d7092ded19b78ebbafd39384e0b9abfdb56bd48d38a842eab84be385
```

The Git-visible governance set before current Task lifecycle must be exactly these 11 paths:

```text
.aiassistant/tasks/done/20260901_2311_aiscc-p1-8-joint-design-terminal-git-object-reconciliation-audit-1.md
.aiassistant/tasks/done/20260901_2359_aiscc-p1-8-runtime-prerequisite-authority-and-jcs-safe-integer-reconciliation-rework-1.md
.aiassistant/tasks/done/20260902_0050_aiscc-p1-8-runtime-owner-boundary-canonical-path-audit-1.md
.aiassistant/tasks/done/20260902_0232_aiscc-p1-8-runtime-prerequisite-authority-expanded-path-implementation-rework-1.md
.aiassistant/tasks/done/20260902_1100_aiscc-p1-8-runtime-provider-regression-and-metadata-parity-rework-1.md
.aiassistant/tasks/done/20260902_1222_aiscc-p1-8-runtime-final-acceptance-terminal-persistence-1.md
.aiassistant/tasks/done/20260902_1300_aiscc-p1-8-terminal-dirty-baseline-provenance-reconciliation-audit-1.md
.aiassistant/records/aiscc/cycles/20260902_1100_aiscc-p1-8-runtime-expanded-path-implementation-hold-1.cycle.md
.aiassistant/records/aiscc/cycles/20260902_1222_aiscc-p1-8-runtime-human-final-acceptance-1.cycle.md
.aiassistant/records/aiscc/cycles/20260902_1300_aiscc-p1-8-terminal-persistence-precondition-blocked-1.cycle.md
.aiassistant/records/aiscc/cycles/20260902_1355_aiscc-p1-8-terminal-dirty-baseline-audit-acceptance-human-disposition-gate-1.cycle.md
```

The active Task and target bundle are ignored and excluded. Any other governance/repository-configuration dirty
path is a mandatory stop.

### 2. Exact six pre-restore identities

Require exact current SHA-256 and HEAD blob SHA-1:

| path | current SHA-256 to discard | expected HEAD blob SHA-1 |
|---|---|---|
| `src/aiscc/evidence/content.py` | `86fec26a717ec99878d0cd2b69860d2e27aeb30d1a76f1f1e53d1d773611f804` | `63f0334f55aee58297a9bc357493bef4c5dacc50` |
| `src/aiscc/evidence/models.py` | `7617ad5e9ba531df0ff2b673dff30312889838f61db53395ea344d1ecdd083aa` | `ad72df4dd84a6a5a4863fc3f28a5af1b115b09f1` |
| `src/aiscc/evidence/repository.py` | `db235bb078befbc5afdd5a042410f126e61493ea7818d5adf0e3f223fd9cd9bb` | `c8caa06b12248e27b6b0f345632544302711c81f` |
| `src/aiscc/evidence/requirements.py` | `7fa93582e21bad5bcedbd1c4eed70e3330d8943610891b625e44f028049c0f79` | `a0be7227377853c0cabb12108e74faaa83fba618` |
| `src/aiscc/evidence/service.py` | `0b25caf58eda7b5ae5eb2662b113371e400f82f8bbaa36c1454f26679edcd0b0` | `1d29c39531af55678611b84a4f7f7c4b6df2785e` |
| `src/aiscc/human/repository.py` | `1ed1d466ec056562433c347bbe903356badd5999656e15118fa8d6ef048e51ea` | `75dfaa00a315696a5b5bd08f0128b290fda7a66b` |

For each path, verify current blob SHA-1 also matches the 1300 audit manifest. Verify Python AST and normalized
token/comment sequence of current bytes versus expected HEAD bytes are equivalent. If any identity or semantic
equivalence check fails, do not restore anything; mandatory stop.

### 3. Exact 42-path starting state

- runtime dirty count must be exactly 42.
- accepted 36 identities must match the table below.
- the only other six runtime dirty paths must equal `allowed_restore_paths` with the exact current hashes above.
- any missing or extra runtime path is a mandatory stop.

## restore procedure

After all preflight checks pass, run one exact-path worktree-only restore from the expected HEAD:

```text
git restore --source=1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a --worktree -- <the exact six paths>
```

Do not use a directory pathspec, wildcard, reset, checkout, clean, stash, index restore, or deletion/recreation.

After restore require:

- all six paths absent from `git status --porcelain`;
- all six current Git blob identities equal their expected HEAD blobs;
- Git index still empty;
- runtime dirty set exactly 36 and no other runtime path;
- governance dirty set unchanged at exact 11;
- `git diff --check` passes.

If post-restore validation fails, do not stage. Report the exact state and stop. Do not attempt compensating edits.

## accepted 36 identity and Commit A

The exact post-restore runtime set and expected SHA-256 values are:

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
tests/unit/cycle/test_project_memory_cycle_domain.py 783aef1e86191a68481f818b333a47e8a1da17affe7d2791d3824fbd12e4031d
tests/unit/next_action/test_next_action_domain.py 1a1525c4509302b6f5aaa4ff19965cd4e1680b5e3543db571af38c7067261449
tests/unit/task_authority/test_external_task_authority_domain.py f1b83cd299ac8f6bef239f18aa6206da5034a04ae2d9a5693ff760c1325e0ffd
tests/unit/workflow/test_state_machine.py 7f0501684a30211ab43b7bb9bdae389934c3558a28da266c94254f0fdb867752
```

Compute the ordinal aggregate and require:

```text
path count == 36
ordinal aggregate == a82d94c1d607bc379c12d0768ff54d0cd481467eb731e0884f63176bd1207f3c
```

Stage only these exact 36 pathspecs. Verify index path set equals the list and staged blob contents match every
SHA-256 above. Governance paths must remain unstaged.

Authorized Commit A message:

```text
feat(runtime): complete P1-8 project memory and cycle admission
```

Commit A requirements:

- exactly one non-merge commit;
- parent exactly `1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a`;
- changed path set exactly 36;
- committed tree bytes match all exact SHA-256 values;
- the six restored paths equal parent/HEAD and are absent from the commit diff;
- no governance, repository configuration, generated, private, or unrelated path.

If author identity is unavailable, stop without changing global Git configuration. Do not invent credentials or
modify Git config.

## verification and evidence reuse

Executor-required current checks:

- pre/post restore Git/hash/blob evidence
- AST and normalized token/comment equality for six pre-restore versus HEAD bytes
- post-restore exact 36 dirty set and aggregate
- staged exact 36 path/blob proof
- Commit A hash/message/parent/tree/path proof
- repository-local `ruff check .`
- repository-local `mypy src`
- `git diff --check`

Reuse allowed:

- 1100 complete repository pytest `231 passed`, targeted tests, fresh PostgreSQL/Alembic, fingerprints, Ruff and
  mypy only because all accepted 36 bytes remain exact and the six restored paths return to the clean HEAD bytes
  that preceded the 1100 candidate execution.
- 1222 Human runtime acceptance only for exact 36 bytes.

Do not create a new database/container or rerun full pytest merely to fill report fields. If current Ruff/mypy
cannot run in the repository-local environment without new dependency/network/environment setup, report
`EVIDENCE_SCOPE_EXPANSION_REQUIRED` before Commit A rather than broadening scope.

Proof non-substitution:

- restore success != Commit A proof
- staged path list != committed tree/blob proof
- accepted test evidence != permission to change accepted bytes
- Commit A != P1 closure or canonical Commit B

## workflow transition expectation

- initial_state: `P1-8_RUNTIME_HUMAN_ACCEPTED / RESTORE_SIX_AUTHORIZED / COMMIT_A_PENDING`
- expected_non_terminal_state_when_human_pending: `COMMIT_A_CREATED / COMMAND_CENTER_REVIEW_REQUIRED`
- expected_terminal_candidate: `RUNTIME_COMMIT_A_PERSISTED`
- transition_authority: `HUMAN for restore; SYSTEM/Command Center for exact commit authorization`
- Agent가 직접 P1 terminal state를 결정할 수 있는가: `No`

## evidence contract

executor_required:

- channel: `PUBLIC_PROVENANCE`
  scope: restore/Commit A Git identities and exact path/blob/tree proof
  allowed_command_or_environment: local Git and hashing only
  pass_condition: exact six restored, exact 36 committed, exact parent, empty index
- channel: `STATIC_SOURCE`
  scope: six AST/token equivalence; accepted 36 hash preservation
  allowed_command_or_environment: local repository only
  pass_condition: equivalence and all hashes pass before mutation
- channel: `BUILD`
  scope: Ruff and mypy
  allowed_command_or_environment: existing repository-local environment only
  pass_condition: both pass without dependency/environment mutation
- channel: `SOURCE_EVIDENCE_EXPORT`
  scope: exact 36 files read from Commit A tree
  allowed_command_or_environment: byte-preserving export into ignored target bundle
  pass_condition: 36/36 committed-tree/source-copy equality

reuse_allowed:

- channel: `UNIT_TEST / INTEGRATION_TEST / DATABASE_RUNTIME`
  predecessor: `20260902_1100 accepted evidence`
  provenance_condition: exact 36 current/committed bytes and six exact HEAD restorations
  applicability_condition: no source semantic change; all hashes and preflight equivalence pass

human_owned:

- channel: `HUMAN_VERIFICATION`
  scope: Commit A Command Center/Human review, later Commit B, Project Source replacement
  expected_result_format: exact commit hash/parent/tree/path judgment

not_required:

- channel: `BROWSER_RUNTIME / EXTERNAL_PROVIDER / NETWORK / DEPLOYMENT`
  reason: local terminal persistence only

forbidden:

- action_or_channel: source implementation, broad cleanup, canonical update, governance commit, push/deployment
  reason: outside exact restore and Commit A boundary

## project context impact

architecture:

- `NONE`

orchestration_contract:

- `NONE`

security_sandbox:

- `NONE`

public_provenance:

- `COMMAND_CENTER_COMMIT_REVIEW_REQUIRED`

## accept 기준

- all mandatory preflight identities match.
- six current hashes and HEAD blobs match audit evidence; AST/token equivalence passes.
- only exact six are restored to exact HEAD; no other worktree cleanup occurs.
- post-restore runtime dirty set is exact accepted 36 with aggregate `a82d94c...`.
- Ruff, mypy and diff checks pass or reuse is reported exactly as authorized.
- staging contains exact 36 only with expected bytes.
- exactly one Commit A exists with exact parent/message/path/blob/tree proof.
- final index is empty; six restore paths are clean.
- canonical/governance remains unmodified except Task lifecycle after report/export.
- target bundle and manifest satisfy the contract.

## hold/reject 기준

- preflight mismatch or additional dirty path
- six current or HEAD identity mismatch
- AST/token semantic difference
- accepted 36 hash/aggregate mismatch
- restore touches any other path
- staged/committed path set differs from exact 36
- governance/canonical path staged or changed
- more than one commit or wrong parent/message
- forbidden Git/network/deployment action

## mandatory stop 조건

- source or policy authority conflict
- branch/HEAD/index mismatch
- missing or mismatched Task/Cycle identity
- dirty-set/path/hash/blob mismatch
- semantic equivalence check failure
- restore or post-restore validation failure
- Git author identity requires configuration mutation
- evidence scope expansion or security/private-data uncertainty

After a named blocker, do not stage or commit. Produce minimum evidence, preserve workspace, complete report/export
and lifecycle only when safe.

## 보고서 필수 항목

- result taxonomy and Task identity/lifecycle
- read canonical paths
- branch/HEAD/index before restore, after restore, after Commit A, and final
- exact six pre-restore current hashes/blobs, HEAD blobs, AST/token result, post-restore hashes/blobs
- exact 42 -> 36 runtime dirty transition
- accepted 36 aggregate before staging and in committed tree
- staged exact path/blob set
- Commit A hash/message/parent/tree/path count and merge-parent count
- six paths absent from Commit A diff
- governance exact 11 before lifecycle and exact 12 after lifecycle
- product source changes: exact six restored; accepted 36 committed without content edit
- governance/provenance changes: Task lifecycle only
- repository configuration changes: none
- current checks and reused evidence classifications
- forbidden-not-run, mandatory stop/scope expansion, unverified/Human-owned
- rollback guide that does not execute reset/amend
- preserved exact paths and next-turn recommendation

## export bundle 요구

Target:

```text
.aiassistant/reports/target/20260902_1400_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-1/
```

Required root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `RESTORE_EVIDENCE.md`
- `RUNTIME_COMMIT_MANIFEST.md`
- `GIT_OBJECT_EVIDENCE.md`
- exact 36 files exported from Commit A tree preserving repository-relative paths
- `REMOVED_FILES.md` absent because no file deletion is authorized

Manifest requirements:

- manifest excludes itself
- every payload path, byte count, SHA-256, exact source/object identity and match result
- Commit A source copy count exactly 36 on success
- no copy of the six discarded pre-restore bytes; the accepted 1300 audit bundle already preserves review evidence
- no credential, env, private data, Git object database dump, unrelated source or previous bundle
- strict UTF-8 no BOM and Markdown/control-character validation

## Task lifecycle and final workspace

After source-evidence export and report completion, move this exact Task from active to done. That lifecycle does
not mean Command Center acceptance.

Final expected state on success:

- branch `main` at Commit A
- index empty
- runtime dirty paths `0`
- six restore paths clean
- governance Git-visible paths `12`, exact previous 11 plus:

```text
.aiassistant/tasks/done/20260902_1400_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-1.md
```

- canonical records unchanged
- Commit B not created
- ignored target bundle present

## 사람 검증 요구

- Human restore decision is already provided and scoped to exact six paths.
- No new runtime QA is required if all current/reused applicability conditions match.
- Command Center must review exact Commit A object evidence before issuing Commit B/canonical closure work.

## 최종 응답 형식

1. result: `completed / blocked / rejected-candidate`
2. target bundle path
3. restore result for exact six
4. Commit A hash/message/parent/tree/path count
5. runtime/index/governance final state
6. changed/restored files
7. removed files: none
8. Human-provided and Human-pending items
9. unverified items
10. preserved exact paths

