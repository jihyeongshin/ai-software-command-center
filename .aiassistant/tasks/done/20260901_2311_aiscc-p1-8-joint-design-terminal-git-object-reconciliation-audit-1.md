# 작업지시서: P1-8 Joint Design Terminal Git Object Reconciliation Audit

## meta

- task_id: `20260901_2311_aiscc-p1-8-joint-design-terminal-git-object-reconciliation-audit-1`
- created_at: `2026-09-01T23:11:00+09:00`
- phase: `P1-8 Runtime Prerequisite Authority Contracts`
- work_type: `SOURCE_EVIDENCE_EXPORT / QA_ONLY`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `AISCC_REPOSITORY_LOCAL_CANONICAL / GIT_OBJECT_DATABASE`
- expected_start_branch: `main`
- expected_start_head: `1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a`
- mutation_authority: `AUDIT_ARTIFACT_AND_TASK_LIFECYCLE_ONLY`
- git_commit: `FORBIDDEN`
- git_push: `FORBIDDEN`

---

# 1. 현재 판정과 감사 목적

검토 대상:

```text
20260901_2155_aiscc-p1-8-jcs-safe-integer-joint-design-terminal-acceptance-persistence-1.zip
SHA-256:
cb200858cdd4611f0b582bdfecc31b97d7f19e219bd971f8927fe25a0a24b817
```

독립적으로 확인된 내용:

```text
ZIP CRC / 경로 안전성: PASS
manifest 16/16 byte/hash: PASS
TASK.md == done Task: PASS
accepted rule bytes: PASS
22 canonical JCS payload recomputation: 22/22 PASS
unsafe normative JSON integer count: 0
state/Cycle/handoff semantic consistency: PASS
runtime inventory serialization: 19 paths / aggregate PASS
UTF-8/BOM/control/secret/fence scan: PASS
```

그러나 제출물의 `GIT_PROVENANCE.md`는 다음을 서술할 뿐, Commit A/B raw object bytes 또는 repository object
database를 포함하지 않는다.

```text
Commit A object existence / exact object identity
Commit B object existence / exact object identity
exact parent lineage
exact commit title/body
Commit A/B exact changed-path sets at Git tree
committed blob bytes at the claimed commits
actual final HEAD/index/worktree state
```

따라서 현재 Command Center 판정은:

```text
SUBSTANTIVE_CONTENT_PASS
TERMINAL_CLOSURE_GIT_OBJECT_EVIDENCE_AUDIT_REQUIRED
```

이다. 이번 Task는 local canonical repository를 좁게 감사하여 아래 둘 중 하나만 증명한다.

```text
STATE_A_VERIFIED
→ 2155 terminal persistence Git lineage is independently reproducible

STATE_A_NOT_VERIFIED
→ exact mismatch/blocker reported without repository mutation
```

P1-8 Runtime 재개, 새 design 결정, 새 Human 판정은 이번 Task의 범위가 아니다.

---

# 2. expected identities

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

terminal base:
683aaee84d1fc09e9371dd214efc3ff58b7225ee

Commit A candidate:
b271f98df7d53edd3d3bc418443ff192e7aa4cfb

Commit B candidate / expected HEAD:
1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a

accepted source rule SHA-256:
7cf27b77bb961280becfc55ecf8e71c9406da9b7b91df0d2697132c2655108db

accepted prerequisite rule SHA-256:
8b19970629c55629df1560f2329b529992eceb86d5e4216baf0b7e78d3876960

unaccepted runtime candidate:
19 paths /
84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42
```

Human decision remains bound exactly as:

```text
Human exact text: Accept
binding: JOINT_EXACT_BYTES
```

Do not mint, broaden, or request another Human decision.

---

# 3. 목표

1. actual branch, `HEAD`, index, worktree를 read-only로 확인한다.
2. terminal base/Commit A/Commit B raw commit objects를 byte-preserving export하고 object SHA를 재계산한다.
3. Commit A/B exact parent lineage와 no-intervening-commit을 확인한다.
4. Commit A/B title/body를 2155 Task contract와 대조한다.
5. Commit A exact 2-path 및 Commit B exact 10-path boundary를 Git tree에서 검증한다.
6. 모든 12 committed blobs를 commit tree에서 직접 추출하고 SHA-256을 대조한다.
7. final Cycle/state/handoff/Task lifecycle semantics를 Commit B blobs로 확인한다.
8. 현재 index가 비어 있고 residual runtime이 exact 19 paths/aggregate인지 확인한다.
9. Command Center가 Git object identity를 독립 재계산할 수 있는 audit bundle을 생성한다.

---

# 4. 비목표 및 금지

- accepted rule/runtime/state/Cycle/handoff/source/test/migration 수정
- canonical state 보정 또는 새 Cycle 생성
- P1-8 Runtime 구현·테스트·재개·acceptance
- Human acceptance 재요청/재해석
- Git add/commit/amend/reset/restore/clean/rebase/merge/cherry-pick/checkout-overwrite
- push/fetch/pull/remote/PR/network/provider/deployment
- Project Source mirror 생성·동기화
- reflog/filesystem forensic 또는 범위 밖 history 조사
- P2/P3/Public Live 작업

이번 active Task의 `active → done` lifecycle과 ignored target audit bundle 생성만 허용한다.

---

# 5. authoritative reads

다음 exact local canonical만 읽는다.

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/records/aiscc/cycles/20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-hold-1.cycle.md
.aiassistant/records/aiscc/cycles/20260901_2155_aiscc-p1-8-jcs-safe-integer-joint-design-final-acceptance-1.cycle.md

.aiassistant/reports/aiscc/20260901_2155_aiscc-p1-8-prerequisite-authority-accepted-runtime-resume-handoff-1.md

.aiassistant/tasks/done/20260901_1527_aiscc-p1-8-next-action-context-terminal-canonical-git-reconciliation-audit-1.md
.aiassistant/tasks/done/20260901_1601_aiscc-p1-8-prerequisite-owner-authority-exact-contract-and-source-enrollment-design-rework-1.md
.aiassistant/tasks/done/20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-design-rework-1.md
.aiassistant/tasks/done/20260901_2155_aiscc-p1-8-jcs-safe-integer-joint-design-terminal-acceptance-persistence-1.md
```

Browser Project Source snapshots are read-only mirrors and do not override later local canonical bytes.

---

# 6. preflight

Task lifecycle move 전에 확인한다.

```text
branch == main
HEAD == 1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a
index == empty
```

Working-tree tracked dirty set must be exactly the 19 runtime paths in section 12. The current active Task and ignored
target output are excluded from tracked dirty classification.

Accepted rule and terminal-governance working-tree paths must be clean against `HEAD`.

Mismatch가 있어도 reset/clean/restore하지 않는다. Minimal read-only inventory와 report/export만 수행하고:

```text
STATE_A_NOT_VERIFIED / TERMINAL_GIT_PREFLIGHT_MISMATCH
```

로 종료한다.

---

# 7. raw Git object verification

Git object database에서 다음 세 객체가 `commit`인지 확인한다.

```text
683aaee84d1fc09e9371dd214efc3ff58b7225ee
b271f98df7d53edd3d3bc418443ff192e7aa4cfb
1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a
```

각 raw commit object body를 byte-preserving 방식으로 export한다. PowerShell text redirection 등 newline/encoding을
변환할 수 있는 방법을 사용하지 않는다. Binary-safe subprocess/file API 또는 Git Bash binary-safe redirection을
사용한다.

각 export bytes에 대해 다음을 재계산한다.

```text
git hash-object -t commit --stdin
```

결과가 각각 expected object SHA와 동일해야 한다.

Exact parent lineage:

```text
parent(Commit A) == 683aaee84d1fc09e9371dd214efc3ff58b7225ee
parent(Commit B) == b271f98df7d53edd3d3bc418443ff192e7aa4cfb
HEAD == Commit B
```

Commit A/B가 각각 single-parent이고 intervening commit이 없어야 한다.

---

# 8. commit message verification

Commit A title:

```text
docs(governance): accept p1-8 prerequisite authority contracts
```

Commit A body must state all:

- Human joint acceptance binds the two exact rule bytes.
- JCS numeric sequence/high-watermark maximum is `9007199254740991`.
- all 22 direct/transitive cross-contract fingerprints reconcile.
- historical source Commit A/B and prior final Cycle remain immutable lineage.
- runtime implementation is not accepted by this commit.

Commit B title:

```text
chore(governance): close p1-8 prerequisite authority design
```

Commit B body must state all:

- records the fourth Command Center session Human joint acceptance
- closes the safe-integer corrected source and prerequisite authority design
- preserves 1527/1601/1652 review lineage and 1652 HOLD
- retains the 19-path runtime as an unaccepted candidate
- authorizes only a separate runtime rework/resume Task

Meaning-equivalent prose is acceptable only when every required statement is explicit. Missing statement is:

```text
STATE_A_NOT_VERIFIED / COMMIT_MESSAGE_CONTRACT_MISMATCH
```

---

# 9. Commit A exact boundary

Changed path set must be exactly:

```text
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
```

Export both blobs from Commit A tree, never from working-tree copies. Required SHA-256:

```text
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
7cf27b77bb961280becfc55ecf8e71c9406da9b7b91df0d2697132c2655108db

.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
8b19970629c55629df1560f2329b529992eceb86d5e4216baf0b7e78d3876960
```

Commit A contains no runtime/governance path outside these two files.

---

# 10. Commit B exact boundary

Changed path set must be exactly these ten ordinal-sorted paths:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/records/aiscc/cycles/20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-hold-1.cycle.md
.aiassistant/records/aiscc/cycles/20260901_2155_aiscc-p1-8-jcs-safe-integer-joint-design-final-acceptance-1.cycle.md
.aiassistant/reports/aiscc/20260901_2155_aiscc-p1-8-prerequisite-authority-accepted-runtime-resume-handoff-1.md
.aiassistant/tasks/done/20260901_1527_aiscc-p1-8-next-action-context-terminal-canonical-git-reconciliation-audit-1.md
.aiassistant/tasks/done/20260901_1601_aiscc-p1-8-prerequisite-owner-authority-exact-contract-and-source-enrollment-design-rework-1.md
.aiassistant/tasks/done/20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-design-rework-1.md
.aiassistant/tasks/done/20260901_2155_aiscc-p1-8-jcs-safe-integer-joint-design-terminal-acceptance-persistence-1.md
```

Export all ten blobs from Commit B tree, path-preserving and byte-preserving. Required SHA-256 values:

```text
CURRENT_STATE_SUMMARY.md  b20d0928896123e12d4337ba93068a41497982d42cc24e000e3d0a4f998e1b09
DECISION_REGISTER.md      f6fd9e32cd11dd720cfdd375f1f6eb3b9f3d2a1a10e864dbcdab853a4c10e302
NEXT_ACTIONS.md           00b36388c22809b04ee5f3c4b699a0b8a551939621e533df8609b3a88863b6b9
1652 HOLD Cycle           82e3ddf378ff820479cd18625e93a0b2968d79a3162dac48ffb639aecc6bec72
2155 final Cycle          df152a617eeac7d54b03a76ffa4ea53ffbe639e6d8d90e3d813d81196686b6ed
2155 handoff              28e1fd07926121ec638629a73c6e5506736fbd2e8fc18cb59a76d9aa0999d443
1527 done Task            8d5d0e74c88a311dab41869040028aa5a4ebb7df09c556b44dc457c367fc72de
1601 done Task            8fe75a5a948ac73909560163cedd4debab6ac9d7be6f07755b1916eaf175fcc4
1652 done Task            4adee46da6c85e1a69cf672db755af69a38bae1dc3c342f490e06dab167fc3e7
2155 done Task            5c33b75c6b2b16fec6683d981656daa71bf4c6d7ce65269c5f6b2c87f36e01ce
```

Commit B must contain no `src/**`, `tests/**`, `migrations/**`, `.aiassistant/rules/**`,
`.aiassistant/project-sources/**`, or `.aiassistant/reports/target/**` path.

---

# 11. terminal semantic verification

Commit B tree의 final Cycle/state/handoff/done Task에서 동시에 확인한다.

```text
Human: HUMAN_PROVIDED / ACCEPTED
Human exact text: Accept
binding: JOINT_EXACT_BYTES
source SHA: 7cf27b77...
prerequisite SHA: 8b199706...
accepted design Commit A: b271f98...
22/22 JCS PASS / mismatch 0 / unsafe integer 0
corrected source design: ACCEPTED / CLOSED
prerequisite design: ACCEPTED / CLOSED
P1-8 Runtime: NOT_ACCEPTED / SEPARATE_REWORK_RESUME_AUTHORIZED
runtime candidate: exact 19 paths / 84641ac3...
P2/P3: NOT_STARTED
PUBLIC_BOUNDED_LIVE: NOT_RELEASED
```

Historical `35901125... → 683aaee...` source-authority lineage and 1619 final Cycle must remain referenced as immutable
history; it must not be rewritten as the current corrected Commit A/B.

Final Cycle의 terminal governance reference `THIS_COMMIT` is acceptable only if it explicitly resolves to the exact
commit containing the Cycle and the audit proves that commit is `1c9a3ef...`.

---

# 12. residual runtime exact boundary

Task lifecycle move 전 current tracked dirty set must be exactly:

```text
migrations/versions/20260831_0006_p1_8_project_memory_cycle_admission.py
migrations/versions/20260831_0007_p1_8_authority_contract_rework.py
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
tests/integration/evidence/test_postgres_evidence_admission.py
tests/integration/human/test_postgres_human_gate_judgment.py
tests/integration/memory/test_postgres_project_memory_next_action.py
tests/integration/workflow/test_postgres_kernel.py
tests/unit/cycle/test_project_memory_cycle_domain.py
tests/unit/next_action/test_next_action_domain.py
```

Recompute each SHA-256 and ordinal serialization:

```text
<path>\t<lowercase_sha256>\n
```

Expected:

```text
19 paths /
84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42
```

Accepted rule/governance paths must be clean. Unexpected dirty paths must be `0`. Do not clean or edit any mismatch.

---

# 13. evidence contract

executor_required:

- `PUBLIC_PROVENANCE`: raw commit object identity, parents, title/body, exact changed-path sets
- `SOURCE_EVIDENCE_EXPORT`: Commit A 2 blobs + Commit B 10 blobs from committed trees
- `STATIC_SOURCE`: committed terminal semantics and exact runtime residual inventory
- `STATIC_SOURCE`: UTF-8/BOM/control/secret/fence validation for exported Markdown

human_owned:

- joint exact-byte acceptance is already `HUMAN_PROVIDED / ACCEPTED`; do not rerun

not_required:

- build/unit/integration/database/HTTP/browser tests
- Project Source mirror sync

proof_non_substitution:

```text
Executor report != Git object evidence
GIT_PROVENANCE.md narrative != independently recomputed raw commit identity
working-tree copy != committed-tree blob
design acceptance != runtime acceptance
tasks/done != accepted
```

---

# 14. target audit bundle

Create ignored target:

```text
.aiassistant/reports/target/
20260901_2311_aiscc-p1-8-joint-design-terminal-git-object-reconciliation-audit-1/
```

Required root files:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
GIT_OBJECT_PROVENANCE.md
COMMIT_A_CHANGED_PATHS.txt
COMMIT_B_CHANGED_PATHS.txt
RUNTIME_WORKTREE_INVENTORY.md
```

Required raw object files:

```text
RAW_GIT_OBJECTS/683aaee84d1fc09e9371dd214efc3ff58b7225ee.commit
RAW_GIT_OBJECTS/b271f98df7d53edd3d3bc418443ff192e7aa4cfb.commit
RAW_GIT_OBJECTS/1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a.commit
```

Required path-preserved trees:

```text
COMMIT_A_BLOBS/.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
COMMIT_A_BLOBS/.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md

COMMIT_B_BLOBS/.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
COMMIT_B_BLOBS/.aiassistant/records/aiscc/DECISION_REGISTER.md
COMMIT_B_BLOBS/.aiassistant/records/aiscc/NEXT_ACTIONS.md
COMMIT_B_BLOBS/.aiassistant/records/aiscc/cycles/20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-hold-1.cycle.md
COMMIT_B_BLOBS/.aiassistant/records/aiscc/cycles/20260901_2155_aiscc-p1-8-jcs-safe-integer-joint-design-final-acceptance-1.cycle.md
COMMIT_B_BLOBS/.aiassistant/reports/aiscc/20260901_2155_aiscc-p1-8-prerequisite-authority-accepted-runtime-resume-handoff-1.md
COMMIT_B_BLOBS/.aiassistant/tasks/done/20260901_1527_aiscc-p1-8-next-action-context-terminal-canonical-git-reconciliation-audit-1.md
COMMIT_B_BLOBS/.aiassistant/tasks/done/20260901_1601_aiscc-p1-8-prerequisite-owner-authority-exact-contract-and-source-enrollment-design-rework-1.md
COMMIT_B_BLOBS/.aiassistant/tasks/done/20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-design-rework-1.md
COMMIT_B_BLOBS/.aiassistant/tasks/done/20260901_2155_aiscc-p1-8-jcs-safe-integer-joint-design-terminal-acceptance-persistence-1.md
```

`EXPORT_MANIFEST.md` must record every file path, byte length, SHA-256, source commit/path, Git blob object ID when
applicable, and mismatch count. `TASK.md` must be byte-identical to the current done Task.

Do not include runtime file bytes, secrets, private chat history, Project Source mirrors, or unrelated repository
history.

---

# 15. Task lifecycle and final workspace

After all audit evidence is complete, move exactly:

```text
.aiassistant/tasks/active/20260901_2311_aiscc-p1-8-joint-design-terminal-git-object-reconciliation-audit-1.md
→
.aiassistant/tasks/done/20260901_2311_aiscc-p1-8-joint-design-terminal-git-object-reconciliation-audit-1.md
```

Do not stage or commit it.

Final expected semantics:

```text
HEAD: unchanged
index: empty
accepted rules/governance: clean
runtime residual: exact 19 paths / 84641ac3...
additional uncommitted governance path: current done Task only
unexpected dirty paths excluding current done Task: 0
Git commit/push: NOT_RUN
```

---

# 16. terminal result taxonomy

`STATE_A_VERIFIED` requires all:

```text
HEAD == Commit B
all 3 raw commit object SHA recomputations exact
Commit A/B parent lineage exact
Commit A/B title/body contract exact
Commit A changed paths == exact 2
Commit B changed paths == exact 10
all 12 committed blob exports and SHA-256 exact
terminal semantics exact
runtime residual 19-path aggregate exact
index empty
forbidden paths/actions absent
```

Otherwise use:

```text
STATE_A_NOT_VERIFIED / <EXACT_BLOCKER>
```

Do not infer missing evidence as PASS.

---

# 17. Executor report requirements

Report exact:

1. task/work type/task path/done path
2. repository/branch/start and final HEAD
3. initial/final index
4. three raw commit object hashes recomputed from exported bytes
5. Commit A/B parents and no-intervening result
6. Commit A/B exact title/body result
7. Commit A changed paths/count and prohibited paths
8. Commit B changed paths/count and prohibited paths
9. all 12 committed blob Git object IDs and exported SHA-256 values
10. final Cycle/state/handoff semantic result
11. Human exact text/binding carried forward, not minted
12. runtime 19-path inventory/aggregate before and after lifecycle
13. unexpected dirty paths
14. target bundle path and ZIP path
15. UTF-8/BOM/control/secret/fence validation
16. forbidden-not-run
17. tests/runtime/mirror not required
18. unverified items
19. `STATE_A_VERIFIED` or exact `STATE_A_NOT_VERIFIED` blocker
20. preserved exact paths

---

# 18. preserved exact paths

Preserve without modification:

```text
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
.aiassistant/records/aiscc/cycles/20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-hold-1.cycle.md
.aiassistant/records/aiscc/cycles/20260901_2155_aiscc-p1-8-jcs-safe-integer-joint-design-final-acceptance-1.cycle.md
.aiassistant/reports/aiscc/20260901_2155_aiscc-p1-8-prerequisite-authority-accepted-runtime-resume-handoff-1.md
.aiassistant/tasks/done/20260901_1527_aiscc-p1-8-next-action-context-terminal-canonical-git-reconciliation-audit-1.md
.aiassistant/tasks/done/20260901_1601_aiscc-p1-8-prerequisite-owner-authority-exact-contract-and-source-enrollment-design-rework-1.md
.aiassistant/tasks/done/20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-design-rework-1.md
.aiassistant/tasks/done/20260901_2155_aiscc-p1-8-jcs-safe-integer-joint-design-terminal-acceptance-persistence-1.md
.aiassistant/tasks/done/20260901_2311_aiscc-p1-8-joint-design-terminal-git-object-reconciliation-audit-1.md
```

The target audit bundle is temporary and deletable only after substantive Command Center review.

---

# 19. next action boundary

On `STATE_A_VERIFIED`, stop and submit the audit bundle. Do not start runtime work in the same Task.

Only a later Browser Command Center judgment may issue:

```text
P1-8 runtime prerequisite-authority and JCS-safe-integer reconciliation resume
```

On `STATE_A_NOT_VERIFIED`, stop with exact evidence. Do not repair or expand scope.
