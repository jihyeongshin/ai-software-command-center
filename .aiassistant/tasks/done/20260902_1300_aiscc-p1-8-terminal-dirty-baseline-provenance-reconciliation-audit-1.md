# 작업지시서: P1-8 terminal dirty-baseline provenance reconciliation audit

## meta

- task_id: `20260902_1300_aiscc-p1-8-terminal-dirty-baseline-provenance-reconciliation-audit-1`
- created_at: `2026-09-02T13:00:00+09:00`
- work_type: `DISCOVERY_AUDIT / SOURCE_EVIDENCE_EXPORT`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a`
- primary_semantic_owner: `AISCC Command Center / Git terminal persistence authority`
- fresh_chat_policy: `REUSE_CURRENT_IDE_CHAT_ALLOWED`
- fresh_chat_reason: `1222 turn stopped before mutation and this Task audits the exact same repository state; a new chat is not required unless the current Executor context is unavailable or contaminated.`

## 현재 상태

- current canonical baseline: repository-local `.aiassistant/records/aiscc/**`; canonical state update was not performed by 1222.
- predecessor cycle: `.aiassistant/records/aiscc/cycles/20260902_1300_aiscc-p1-8-terminal-persistence-precondition-blocked-1.cycle.md`
- Human acceptance cycle: `.aiassistant/records/aiscc/cycles/20260902_1222_aiscc-p1-8-runtime-human-final-acceptance-1.cycle.md`
- predecessor Task: `.aiassistant/tasks/done/20260902_1222_aiscc-p1-8-runtime-final-acceptance-terminal-persistence-1.md`
- known branch / HEAD: `main / 1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a`
- known Git index: empty
- known dirty workspace: `42 runtime paths; 8 governance paths after 1222 lifecycle; ignored active/target artifacts excluded`
- open blocker: `RUNTIME_CANDIDATE_IDENTITY_MISMATCH / UNEXPECTED_DIRTY_PATHS`
- Human P1-8 runtime final review: `ACCEPTED`; this Task must not revoke or manufacture that Human decision.

## 확정된 정정 사실

The following facts are Task authority, not implementation requests:

1. `tests/unit/cycle/test_project_memory_cycle_domain.py` actual and accepted 1100 SHA-256 is:

```text
783aef1e86191a68481f818b333a47e8a1da17affe7d2791d3824fbd12e4031d
```

The 1222 Task omitted one `9` and is wrong on that row.

2. The accepted 1100 bundle labeled its serialization ordinal but produced the aggregate by appending the provider
regression path after the previous 35-row serialization:

```text
legacy accepted identifier:
a1d5e9d24eabae3fec13e24cfb9d94e744e6687ca4c00889e85972fb5a633590
```

Using all 36 actual rows in ordinal, case-sensitive path order produces:

```text
corrected ordinal aggregate candidate:
a82d94c1d607bc379c12d0768ff54d0cd481467eb731e0884f63176bd1207f3c
```

This Task must independently reproduce both values and explain the exact ordering difference. It must not edit
runtime bytes to force either aggregate.

3. The 1222 preflight observed all expected 29 paths plus 13 extra runtime Git-dirty paths. Six were outside the
accepted 36-path inventory:

```text
src/aiscc/evidence/content.py
src/aiscc/evidence/models.py
src/aiscc/evidence/repository.py
src/aiscc/evidence/requirements.py
src/aiscc/evidence/service.py
src/aiscc/human/repository.py
```

Seven were accepted 36-path rows but omitted from the 1222 exact expected dirty set:

```text
migrations/versions/20260831_0006_p1_8_project_memory_cycle_admission.py
migrations/versions/20260831_0007_p1_8_authority_contract_rework.py
src/aiscc/cycle/__init__.py
src/aiscc/judgment/authority.py
src/aiscc/memory/__init__.py
src/aiscc/memory/repository.py
src/aiscc/next_action/__init__.py
```

## 이번 턴 목표

1. 현재 repository에서 branch, HEAD, empty index, exact Git-visible path set을 독립적으로 재현한다.
2. 모든 runtime Git-dirty path를 exact status, tracked/untracked, bytes, SHA-256, HEAD-side identity와 함께 한 표로 만든다.
3. runtime 42개 각각을 accepted P1 lineage에 매핑한다. `P1-4`, `P1-5`, `P1-6`, `P1-7`, `P1-8`,
   `UNRELATED`, `UNRESOLVED` 중 하나와 exact Task/Cycle/commit/source 근거를 기록한다.
4. 특히 13 extra paths가 언제부터 dirty였는지 Git 및 tracked governance provenance로 좁혀, future Commit A
   포함/선행 commit/제외/사람 결정 필요 중 하나를 제안한다.
5. accepted 36 runtime bytes를 변경하지 않고 legacy aggregate와 corrected ordinal aggregate를 재현한다.
6. 다음 terminal persistence Task가 사용할 수 있는 exact commit plan을 제안한다. 아직 commit하지 않는다.

## 이번 턴 비목표

- runtime source/test/migration 수정
- accepted 36-path bytes 변경 또는 Human acceptance 재판정
- canonical state/decision/next-actions/handoff 수정
- Cycle 수정
- Git index mutation, commit, reset, restore, cleanup, push
- P1 closure, P2 구현, Project Source mirror 생성·업로드
- 새로운 runtime test, database, provider, network, browser evidence 생성

## 허용 범위

allowed_paths_read:

- repository-root `AGENTS.md`
- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- `.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md`
- `.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md`
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
- `.aiassistant/records/aiscc/cycles/20260901_2155_aiscc-p1-8-jcs-safe-integer-joint-design-final-acceptance-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260902_1100_aiscc-p1-8-runtime-expanded-path-implementation-hold-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260902_1222_aiscc-p1-8-runtime-human-final-acceptance-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260902_1300_aiscc-p1-8-terminal-persistence-precondition-blocked-1.cycle.md`
- `.aiassistant/tasks/done/20260901_2311_aiscc-p1-8-joint-design-terminal-git-object-reconciliation-audit-1.md`
- `.aiassistant/tasks/done/20260901_2359_aiscc-p1-8-runtime-prerequisite-authority-and-jcs-safe-integer-reconciliation-rework-1.md`
- `.aiassistant/tasks/done/20260902_0050_aiscc-p1-8-runtime-owner-boundary-canonical-path-audit-1.md`
- `.aiassistant/tasks/done/20260902_0232_aiscc-p1-8-runtime-prerequisite-authority-expanded-path-implementation-rework-1.md`
- `.aiassistant/tasks/done/20260902_1100_aiscc-p1-8-runtime-provider-regression-and-metadata-parity-rework-1.md`
- `.aiassistant/tasks/done/20260902_1222_aiscc-p1-8-runtime-final-acceptance-terminal-persistence-1.md`
- exact Git-visible runtime/product/test/migration paths only
- exact Git tree/blob/diff/status metadata needed for provenance

allowed_source_evidence_export_paths:

```text
migrations/versions/20260831_0006_p1_8_project_memory_cycle_admission.py
migrations/versions/20260831_0007_p1_8_authority_contract_rework.py
src/aiscc/cycle/__init__.py
src/aiscc/evidence/content.py
src/aiscc/evidence/models.py
src/aiscc/evidence/repository.py
src/aiscc/evidence/requirements.py
src/aiscc/evidence/service.py
src/aiscc/human/repository.py
src/aiscc/judgment/authority.py
src/aiscc/memory/__init__.py
src/aiscc/memory/repository.py
src/aiscc/next_action/__init__.py
```

allowed_actions:

- read-only `git status`, `git diff`, `git ls-files`, `git log`, `git show`, `git cat-file`, `git rev-parse`
- SHA-256 and byte count computation
- exact 36/42 path aggregate computation
- targeted provenance search limited to the listed governance/source paths
- byte-preserving export of the exact 13 allowlisted disputed source paths
- Task lifecycle `active -> done` after report/export completion
- create ignored target bundle and generated audit reports only

## 절대 금지

forbidden_paths_write:

- all runtime/product/test/migration paths
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
- all existing Cycle files
- `.aiassistant/reports/aiscc/**`
- `.gitignore`, repository configuration, CI/build configuration

forbidden_actions:

- `git add`, `git commit`, `git reset`, `git restore`, `git checkout`, `git clean`, `git stash`
- amend, rebase, merge, cherry-pick, push, PR, release, deployment
- source formatting or line-ending normalization
- accepted runtime bytes 수정
- untracked path 생성·삭제·이동 except current Task lifecycle and ignored target bundle
- external network, credentials, provider/tool call, database container/test harness
- P1 terminal closure, P2 work, Project Source mirror generation/upload
- unrelated source/rule/log bulk-read

## 읽을 문서

Read the exact paths listed in `allowed_paths_read`. The minimum set is:

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- current active Task
- 1300 blocker Cycle
- 1222 done Task and 1222 Human acceptance Cycle
- predecessor 2311/2359/0050/0232/1100 done Tasks
- three canonical state records

Do not assume the browser-submitted ZIP is present in the repository. Recompute from repository state.

## agent instruction transport / authority

- repository-root instruction entrypoint는 transport bootstrap이며 policy authority가 아니다.
- Task-listed canonical files must be explicitly read.
- Project Rules UI 또는 automatic retrieval만으로 canonical body가 전달됐다고 가정하지 않는다.
- unrelated source/log/rule bulk-read를 금지한다.
- current Task, canonical rule, current source, accepted evidence가 충돌하면 즉시 중단한다.
- Human acceptance를 Agent가 재발행·철회·확장하지 않는다.

## 감사 절차

### 1. Placement preflight

Human short prompt에 따라 Downloads source와 exact active destination을 확인하고 `Move`한다. 다른 경로를
탐색하지 않는다. source missing 또는 destination collision이면 어느 파일도 Move하지 않고 중단한다.

1300 Cycle은 이미 exact cycles path에 Human이 Move한 상태여야 한다. 현재 Task가 Cycle을 생성·수정하지
않는다.

### 2. Repository preflight

Report exact:

- branch and HEAD
- index entry count
- porcelain v1 or v2 exact path/status set
- ignored active Task/target bundle separation
- tracked governance dirty set
- runtime/product/test/migration dirty set

Expected starting branch/HEAD/index:

```text
main
1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a
0
```

If branch, HEAD, index, 1222 Task/Cycle hash, or 1300 Cycle identity differs, mandatory stop.

### 3. Runtime dirty inventory

For every current runtime/product/test/migration dirty path, record:

- exact repository-relative path
- Git status
- tracked/untracked
- current byte count and SHA-256
- HEAD blob SHA-1 or `ABSENT_IN_HEAD`
- current blob SHA-1 computed by `git hash-object --no-filters` or equivalent read-only method
- whether the path is in accepted 36 inventory
- exact predecessor Task/Cycle/commit provenance
- proposed ownership classification

Do not use timestamps alone as acceptance provenance.

### 4. Aggregate reconciliation

Reconstruct the exact 36 rows from current bytes and the 1100 done Task/result identities. Compute:

1. all 36 rows in ordinal, case-sensitive path order;
2. predecessor accepted 35-row order plus provider regression appended last.

The report must show the two exact ordered path lists or a machine-readable manifest and explain why the aggregates
differ. Status and byte count are excluded; serialization is UTF-8 no BOM:

```text
<repository-relative-path>\t<lowercase_sha256>\n
```

If current accepted 36 bytes differ from the Human-accepted identities, mandatory stop with exact mismatches.

### 5. Thirteen-path provenance resolution

For each disputed path, report one:

- `ACCEPTED_PREDECESSOR_RUNTIME`
- `ACCEPTED_P1_8_RUNTIME`
- `TRACKED_BASELINE_DIFF_REQUIRES_P1_TERMINAL_COMMIT`
- `UNRELATED_DIRTY_PATH`
- `UNRESOLVED_PROVENANCE`

Each non-unresolved classification requires exact evidence: predecessor Task/Cycle identity, accepted commit/tree,
or source/diff ownership that establishes its phase. Mere presence in a previous export is insufficient.

### 6. Future commit plan proposal

Propose but do not execute:

- exact Commit A parent
- exact Commit A path set and count
- exact current SHA-256 per path
- whether Commit A closes all accepted P1 runtime changes or needs a predecessor persistence commit
- exact governance Commit B allowlist expected after this Task lifecycle
- canonical record/handoff mutations that remain pending
- mandatory-stop conditions for the next terminal Task

If any runtime path remains `UNRESOLVED_PROVENANCE` or `UNRELATED_DIRTY_PATH`, do not propose immediate staging.
Instead report `TERMINAL_COMMIT_PLAN_BLOCKED` and the smallest Human/Command Center decision needed.

## workflow transition expectation

- initial_state: `P1-8_RUNTIME_HUMAN_ACCEPTED / TERMINAL_PERSISTENCE_PRECONDITION_BLOCKED`
- expected_non_terminal_state_when_human_pending: `DIRTY_BASELINE_AUDITED / COMMAND_CENTER_REVIEW_REQUIRED`
- expected_terminal_candidate: `EXACT_TERMINAL_COMMIT_PLAN_PROPOSED`
- transition_authority: `NOT_APPLICABLE`
- Agent가 직접 terminal state를 결정할 수 있는가: `No`

## evidence contract

executor_required:

- channel: `PUBLIC_PROVENANCE`
  scope: branch/HEAD/index, Task/Cycle hashes, exact dirty sets, Git object identities
  allowed_command_or_environment: read-only local Git commands
  pass_condition: all reported identities are reproducible and no mutation occurs
- channel: `STATIC_SOURCE`
  scope: exact 42 runtime dirty path inventory and 13-path provenance mapping
  allowed_command_or_environment: listed source/governance paths only
  pass_condition: every path has evidence-backed or explicit unresolved classification
- channel: `SOURCE_EVIDENCE_EXPORT`
  scope: exact 13 disputed source paths only
  allowed_command_or_environment: byte-preserving local copy into ignored target bundle
  pass_condition: source/copy SHA-256 equality, zero extra source files

reuse_allowed:

- channel: `REUSED_ACCEPTED`
  predecessor: Human 1222 acceptance and 1100 runtime evidence
  provenance_condition: exact Task/Cycle/file identities reproduced locally
  applicability_condition: only accepted runtime byte identity; not Git commit boundary

human_owned:

- channel: `HUMAN_VERIFICATION`
  scope: any unresolved path ownership decision, future commit review, Project Source replacement
  expected_result_format: explicit accept/rework decision with exact path/commit identities

not_required:

- channel: `UNIT_TEST / INTEGRATION_TEST / DATABASE_RUNTIME / BROWSER_RUNTIME`
  reason: read-only Git/provenance audit; runtime bytes are not changed

forbidden:

- action_or_channel: source mutation, Git index/commit, external provider/network/database/browser work
  reason: this Task only resolves the terminal boundary

proof_non_substitution:

- previous source export presence != accepted path ownership
- Human runtime acceptance != authorization to commit unrelated dirty paths
- current file hash != provenance of why the file is dirty
- audit proposal != terminal Git persistence

## conformance reporting

- applicability: `REQUIRED`
- applicable policy_or_invariant: `exact Git authorization; mandatory stop; unrelated dirty path protection`
- required_actual_owner: `Git object evidence and accepted Task/Cycle provenance`
- planned_vs_actual_scope: exact current dirty set versus accepted 36 set versus proposed commit set
- rollback_or_failure_semantics: no product/index/canonical mutation; Task lifecycle and ignored target bundle only

## project context impact

architecture:

- `NONE`

orchestration_contract:

- `NONE`

security_sandbox:

- `NONE`

public_provenance:

- `INVESTIGATE / EXACT_TERMINAL_BOUNDARY_REQUIRED`

## accept 기준

- branch/HEAD/index and all required Task/Cycle hashes match.
- exact runtime dirty set is fully enumerated without mutation.
- both aggregate algorithms and values are independently reproduced.
- all 13 disputed paths receive evidence-backed or explicit unresolved classifications.
- future Commit A/B plan is exact and does not silently absorb unrelated paths.
- exact 13 source copies match and bundle contains no extra source/private material.
- Git index/source/canonical records remain byte-identical.
- report/export/Task lifecycle are complete.

## hold/reject 기준

- accepted 36 current bytes differ from Human-accepted identities
- branch/HEAD/index or supplied governance identity mismatch
- any source/index/canonical mutation
- provenance guessed from filename/timestamp/export presence only
- unresolved path silently added to a commit plan
- export includes unrelated or secret/private material

## mandatory stop 조건

- policy baseline conflict
- missing required Task/Cycle/governance artifact
- branch/HEAD/index mismatch
- accepted 36-path byte mismatch
- dirty workspace changes during audit beyond Task lifecycle/target bundle
- forbidden action/tool request
- security/private-data uncertainty
- evidence scope expansion beyond local read-only Git/source inspection

Named blocker 이후에는 최소 source evidence, workspace inventory, report/export와 안전한 종료만 수행한다.

## 보고서 필수 항목

- result taxonomy
- Task placement and exact hash
- read canonical paths
- branch/HEAD/index before/after
- exact runtime and governance Git-visible inventories
- 42-path manifest with status/hash/HEAD blob/current blob/accepted-set/provenance/classification
- exact 36 legacy and corrected ordinal aggregate reproduction
- exact 13 disputed-path disposition
- proposed Commit A/B path sets or `TERMINAL_COMMIT_PLAN_BLOCKED`
- product source changes: none
- governance/provenance changes: Task lifecycle only
- repository configuration changes: none
- evidence ownership classifications
- mandatory stop/scope expansion
- forbidden-not-run
- unverified/Human-owned decisions
- rollback/revert guide
- preserved exact paths
- next-turn recommendation

## export bundle 요구

Target:

```text
.aiassistant/reports/target/20260902_1300_aiscc-p1-8-terminal-dirty-baseline-provenance-reconciliation-audit-1/
```

Required root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `RUNTIME_DIRTY_MANIFEST.md`
- `AGGREGATE_RECONCILIATION.md`
- `PROVENANCE_RECONCILIATION.md`
- `TERMINAL_COMMIT_PLAN.md`
- exact 13 source copies preserving repository-relative paths
- `REMOVED_FILES.md` only if deletion occurred; deletion is forbidden, so normally absent

Manifest requirements:

- manifest excludes itself
- every payload path, byte count, SHA-256, exact source, source SHA-256, match result
- source copy count exactly 13 unless mandatory stop happens before safe export
- generated report rows marked generated/self, not source evidence
- no credential, env, Git object database dump, private data, unrelated source, previous bundle
- strict UTF-8 no BOM and Markdown/control-character validation

## 사람 검증 요구

- audit 자체에는 별도 Human runtime QA가 필요하지 않다.
- unresolved provenance 또는 future Commit A/B proposal은 Command Center가 검토한다.
- Human은 future terminal commit 결과와 Project Source complete replacement를 별도로 확인한다.

## 최종 응답 형식

1. result: `completed / blocked / rejected-candidate`
2. target bundle path
3. 42-path count and aggregate results
4. 13-path disposition summary
5. proposed Commit A/B path counts or blocked reason
6. changed files: governance Task lifecycle only
7. removed files: none
8. Human verification status
9. unverified items
10. preserved exact paths

