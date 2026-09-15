# 작업지시서: P3-2 accepted public documentation Git persistence

## meta

- task_id: `20260915_0911_aiscc-p3-2-accepted-public-documentation-git-persistence-1`
- created_at: `2026-09-15T09:11:00+09:00`
- work_type: `GIT_PERSISTENCE`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- fresh_ide_chat_required: `No`
- primary_semantic_owner: `P3-2 accepted documentation persistence / Browser Command Center`

## goal

Human-accepted P3-2 public documentation and accumulated P3 public provenance are currently outside repository HEAD.

Persist the exact accepted bytes and exact P3 provenance in one local Git commit without changing their semantic content.

## authoritative inputs

Read:

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- `.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md`
- `.aiassistant/records/aiscc/cycles/20260915_0911_aiscc-p3-2-public-documentation-human-acceptance-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260915_0911_aiscc-p3-2-public-documentation-human-acceptance-browser-judgment-1.md`
- `.aiassistant/reports/aiscc/20260915_0911_aiscc-browser-command-center-p3-2-documentation-accepted-persistence-entry-handoff-1.md`

Use this Task as the exact persistence contract.

Do not bulk-read unrelated history.

## Human-accepted public bytes — MUST NOT CHANGE

```text
README.md
SHA-256: 7f9b8ceaa20b086d9ffb450001b1a683b23ddf4fa5745584adb09a63537c57e1

docs/AISCC_COMPARATIVE_EVALUATION.md
SHA-256: ead8c52a517b4a63afc3add77f83d67048b5d147ec41e8ad815b87fc384a2fd2

.aiassistant/reports/aiscc/AISCC_PUBLIC_DOCUMENTATION_TRUTH_MAP.md
SHA-256: 732eba5694e5f5dec835de1d489091a3199af31274f633e3ebe9bcbfe9cf8b9f
```

Before staging and again after commit, hash all three. Any mismatch => `ACCEPTED_ARTIFACT_HASH_MISMATCH` STOP.

## exact predecessor preflight

Required before any Git mutation:

```text
branch = main
HEAD = 82bc047b79cf496280d1b3df6a113f652629a6f5
index = empty
tracked worktree = clean
```

The following 29 Git-visible untracked paths MUST exist with these exact SHA-256 values:

- `.aiassistant/records/aiscc/cycles/20260915_0013_aiscc-p2-terminal-closure-p3-entry-authorization-1.cycle.md`
  - SHA-256 `e044761b340c80a03d5d92fe9438e98842a0d4c7c97b6a6e7801f8f5ca74d080`
- `.aiassistant/records/aiscc/cycles/20260915_0054_aiscc-p3-1-protocol-freeze-entry-contract-blocked-rework-authorization-1.cycle.md`
  - SHA-256 `20e00e800238a8be35c54bb8d1cf1b936633cbc804d75bb1e0a14e0796264965`
- `.aiassistant/records/aiscc/cycles/20260915_0124_aiscc-p3-1-comparative-protocol-human-acceptance-source-gap-entry-1.cycle.md`
  - SHA-256 `6597b857730ae2ae38b869262ae7db85c241d88641f19fe04e7d6c8ff80b9a8f`
- `.aiassistant/records/aiscc/cycles/20260915_0145_aiscc-p3-1-source-packet-audit-accepted-bounded-evaluation-entry-1.cycle.md`
  - SHA-256 `666b4c461ff62f6c13a1e3c0769627f7623e395b13354870abcb85a73bec4368`
- `.aiassistant/records/aiscc/cycles/20260915_0224_aiscc-p3-1-m05-result-candidate-trace-incomplete-rework-entry-1.cycle.md`
  - SHA-256 `d2b67131964929ca303b621007a800baaf0556cd2a39d7d84d153b445103bf89`
- `.aiassistant/records/aiscc/cycles/20260915_0310_aiscc-p3-1-comparative-evaluation-final-acceptance-p3-2-entry-authorization-1.cycle.md`
  - SHA-256 `6a7011c0cd144e31879e709c9b2138a2b07c7e27cacde1b53c1542242ed87e1b`
- `.aiassistant/reports/aiscc/20260915_0013_aiscc-browser-command-center-p2-closed-p3-entry-handoff-1.md`
  - SHA-256 `3930b6c25a11973a302b2770b5369b4e8948400e585be93d8faffc5d99af00d1`
- `.aiassistant/reports/aiscc/20260915_0013_aiscc-p2-4-final-state-reconciliation-browser-acceptance-1.md`
  - SHA-256 `8fe4e4d1f9725434e21aea8058e099744ee8c18c713daaa843f98943161820cf`
- `.aiassistant/reports/aiscc/20260915_0054_aiscc-browser-command-center-p3-1-protocol-freeze-manual-rework-entry-handoff-1.md`
  - SHA-256 `138fc247a48b03077f42f0ed0030cf6ebbe2df1542ceddceaa643861b4f615f2`
- `.aiassistant/reports/aiscc/20260915_0054_aiscc-p3-1-protocol-freeze-entry-contract-blocked-browser-judgment-1.md`
  - SHA-256 `cb2960f4c4abc7fc1016e2c41811ffc2901ea204354abd97d750dcc53e395cd9`
- `.aiassistant/reports/aiscc/20260915_0124_aiscc-browser-command-center-p3-1-protocol-accepted-source-gap-entry-handoff-1.md`
  - SHA-256 `74c85828c4e26729dd557f5b9773a4106a7550c36d4f4cc5d2e7be3c6a05b624`
- `.aiassistant/reports/aiscc/20260915_0124_aiscc-p3-1-comparative-protocol-human-acceptance-browser-judgment-1.md`
  - SHA-256 `93fa51e2e5071398c9dc27253f6c7f5ac7a6a339011c72109910165a396a22dd`
- `.aiassistant/reports/aiscc/20260915_0145_aiscc-browser-command-center-p3-1-source-gap-closed-bounded-evaluation-entry-handoff-1.md`
  - SHA-256 `0e345101f78fca07e4abe7069d2e8ef1232742ec68737b5ea451c986176e9c5c`
- `.aiassistant/reports/aiscc/20260915_0145_aiscc-p3-1-source-packet-audit-browser-acceptance-1.md`
  - SHA-256 `cf20b71ec5d43cc744df52ada12040d013e4e2cae9ea9694c3a5fe991db632ec`
- `.aiassistant/reports/aiscc/20260915_0224_aiscc-browser-command-center-p3-1-m05-trace-conformance-rework-entry-handoff-1.md`
  - SHA-256 `cbb3f9ec23b47a4bb194acb9048557f8cd9846e63b95d33b5f438b323be27fb1`
- `.aiassistant/reports/aiscc/20260915_0224_aiscc-p3-1-m05-result-candidate-trace-incomplete-browser-judgment-1.md`
  - SHA-256 `6982cce64d15f267fb212e93d1b7ec0c7875ce70b09692b4eb6c940361722b4f`
- `.aiassistant/reports/aiscc/20260915_0310_aiscc-browser-command-center-p3-1-closed-p3-2-public-documentation-entry-handoff-1.md`
  - SHA-256 `5974231be57ec35a15e255954de20a7832ad6cdcd1014373539491043e180568`
- `.aiassistant/reports/aiscc/20260915_0310_aiscc-p3-1-comparative-evaluation-final-human-acceptance-browser-judgment-1.md`
  - SHA-256 `f04bd7877be95240f9188070875f0c6d73f3ff0f01d12848f9b9ae1c9b5ddf83`
- `.aiassistant/reports/aiscc/AISCC_COMPARATIVE_EVALUATION_PROTOCOL.md`
  - SHA-256 `a96b1bffb1f927e97f476a923351471994d632ed0fbe40f4d96e51433b996ed6`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_DOCUMENTATION_TRUTH_MAP.md`
  - SHA-256 `732eba5694e5f5dec835de1d489091a3199af31274f633e3ebe9bcbfe9cf8b9f`
- `.aiassistant/tasks/done/20260914_2338_aiscc-p2-4-final-acceptance-persistence-state-reconciliation-1.md`
  - SHA-256 `aca553ed7a14b9a15682046eae1f7180424308768c3e9d93bf67179c3047f8be`
- `.aiassistant/tasks/done/20260915_0033_aiscc-p3-1-comparative-evaluation-protocol-freeze-and-minimum-matrix-1.md`
  - SHA-256 `08b1a5ee10213ee7dcb1ed3aade0a4983b0fc8e909e3e0b2745ae49e42f4a5a2`
- `.aiassistant/tasks/done/20260915_0054_aiscc-p3-1-comparative-evaluation-protocol-freeze-manual-rework-1.md`
  - SHA-256 `450be880653c1bc96171cbe0ad40af7dad673d6ded97cd6a034cd2ce99e343a0`
- `.aiassistant/tasks/done/20260915_0124_aiscc-p3-1-pre-result-source-packet-gap-closure-and-protocol-amendment-1.md`
  - SHA-256 `891871c93066c447f117547b31a53465d5ac638e70a59c8da0652faacac369e4`
- `.aiassistant/tasks/done/20260915_0145_aiscc-p3-1-frozen-protocol-m05-bounded-comparative-evaluation-1.md`
  - SHA-256 `802238879e3230385d335acaeefee57afa5e9dc2bba321126d794ecd38a9bce5`
- `.aiassistant/tasks/done/20260915_0224_aiscc-p3-1-m05-comparator-trace-provenance-conformance-rework-1.md`
  - SHA-256 `c14ef4e4215b4e3432d7d047eb73ccc3882565cba1865bd20028e8d354ede5b1`
- `.aiassistant/tasks/done/20260915_0310_aiscc-p3-2-public-repository-truth-map-readme-and-comparative-summary-1.md`
  - SHA-256 `d56eff46a3be528f29cdceef6e1fe0502bcf5b1b9e0a717d2344b946ddde3199`
- `docs/AISCC_COMPARATIVE_EVALUATION.md`
  - SHA-256 `ead8c52a517b4a63afc3add77f83d67048b5d147ec41e8ad815b87fc384a2fd2`
- `README.md`
  - SHA-256 `7f9b8ceaa20b086d9ffb450001b1a683b23ddf4fa5745584adb09a63537c57e1`

If:
- any listed path is missing;
- any listed hash differs;
- any additional Git-visible modified/untracked/staged path exists outside the explicitly authorized inbound lineage below;

then STOP `DIRTY_WORKSPACE_MIXED` or `SOURCE_IDENTITY_CONFLICT` as applicable.

Do not clean/reset/restore/delete unrelated paths.

## inbound lineage added by this delivery

After exact ZIP transport, these canonical files are additionally authorized:

- `.aiassistant/records/aiscc/cycles/20260915_0911_aiscc-p3-2-public-documentation-human-acceptance-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260915_0911_aiscc-p3-2-public-documentation-human-acceptance-browser-judgment-1.md`
- `.aiassistant/reports/aiscc/20260915_0911_aiscc-browser-command-center-p3-2-documentation-accepted-persistence-entry-handoff-1.md`
- active Task:
  `.aiassistant/tasks/active/20260915_0911_aiscc-p3-2-accepted-public-documentation-git-persistence-1.md`

The active Task is ignored until lifecycle completion. Move it to:

`.aiassistant/tasks/done/20260915_0911_aiscc-p3-2-accepted-public-documentation-git-persistence-1.md`

only after executor-required persistence evidence/report/export is ready according to repository rules.

## exact commit candidate

The Git commit MUST contain exactly:

- the 29 predecessor paths listed above;
- the 3 inbound canonical Cycle/Judgment/Handoff files;
- `.aiassistant/tasks/done/20260915_0911_aiscc-p3-2-accepted-public-documentation-git-persistence-1.md`.

Expected changed-path count:

```text
33
```

No other path may be staged or committed.

## allowed actions

- `git status --porcelain=v1 --untracked-files=all`
- `git diff --check`
- exact SHA-256 calculation
- `git add -- <exact allowlisted paths>`
- inspect staged names/hashes
- `git diff --cached --check`
- one local `git commit`
- `git show --stat --name-status --format=fuller <result-commit>`
- `git diff-tree --no-commit-id --name-only -r <result-commit>`
- `git rev-parse`
- report/export generation

Authorized commit message:

```text
docs(aiscc): persist accepted P3 public documentation
```

## forbidden actions

- edit any of the 29 predecessor artifacts
- edit README, public comparative summary, truth map
- edit product/runtime/test/config source
- edit CURRENT_STATE_SUMMARY / DECISION_REGISTER / NEXT_ACTIONS in this Task
- `.gitignore` change
- commit amend
- rebase/reset/restore/clean
- broad deletion
- `git push`
- PR/merge/release/tag
- deployment
- provider/LLM/network/browser/DB runtime
- source-mirror upload
- quick-start investigation or wording change
- P3-3 work

## commit verification

After commit verify all:

```text
commit parent = 82bc047b79cf496280d1b3df6a113f652629a6f5
changed path count = 33
changed path set = exact authorized set
accepted public file hashes unchanged
all predecessor path hashes unchanged
commit contains no ignored target artifact
commit contains no private/secret file
index = empty
tracked worktree = clean
Git-visible untracked = 0
```

If an unexpected Git-visible residue remains, do not delete it. Report and STOP acceptance claim.

## evidence contract

executor_required:

1. `STATIC_SOURCE / PUBLIC_PROVENANCE`
   - exact 29-path predecessor identity;
   - exact 3 inbound canonical lineage identities;
   - accepted public hashes unchanged.

2. `GIT_PERSISTENCE`
   - exact staged path set;
   - one authorized commit;
   - exact parent/path count/path set;
   - post-commit clean workspace.

3. `CONFORMANCE`
   - no semantic/content edits;
   - no forbidden action;
   - no unrelated dirt mixed into commit;
   - UTF-8/control-character checks for new inbound governance Task/Cycle/Judgment/Handoff;
   - `git diff --check` / cached diff check.

reuse_allowed:

- 0310 documentation validation;
- Human 0911 acceptance;
- P3-1 accepted provenance.

human_owned:

- `NOT_REQUIRED` for byte-preserving persistence.
- Do not claim P3-2 phase terminal closure; Browser Command Center owns post-commit persistence judgment.

not_required:

- unit/integration tests;
- DB/runtime/HTTP/browser;
- provider/network/deployment;
- public release verification.

forbidden:

- any content re-authoring;
- public status upgrade;
- quick-start investigation;
- P3-3 execution.

proof_non_substitution:

- Human acceptance != Git persistence proof;
- commit existence != correct path-set proof;
- clean worktree != accepted-file hash proof;
- tasks/done != accepted phase status;
- local commit != public release/push/deployment.

## expected terminal candidate

```text
PERSISTENCE_CANDIDATE / BROWSER_REVIEW_REQUIRED
```

Do not declare P3-2 phase closed and do not declare P3-3 started.

## target bundle

`.aiassistant/reports/target/20260915_0911_aiscc-p3-2-accepted-public-documentation-git-persistence-1/`

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `PRECOMMIT_INVENTORY.json`
- `STAGED_COMMIT_MANIFEST.json`
- `POSTCOMMIT_VERIFICATION.json`
- `TERMINAL_WORKSPACE.json`
- copy of new Cycle/Judgment/Handoff/Task-done preserving project-relative paths
- no unchanged 29 files need to be copied unless report-export policy requires exact changed-file inclusion; if copied, classify them as commit evidence, not new content
- `REMOVED_FILES.md` only if a project deletion exists — none is expected

Terminal ZIP:

`.aiassistant/reports/target/20260915_0911_aiscc-p3-2-accepted-public-documentation-git-persistence-1.zip`

## mandatory stop

Stop before commit if:
- base HEAD/branch/index/tracked-clean precondition differs;
- exact predecessor 29-path inventory differs;
- accepted public hash differs;
- unexpected Git-visible dirt exists;
- exact staged path set cannot be formed safely.

Stop after commit without claiming persistence acceptance if:
- parent/path set/hash/post-workspace verification fails.

Do not repair by broad cleanup.

## final response

1. result
2. result commit SHA
3. parent SHA
4. changed path count
5. accepted public hash verification
6. pre/post workspace
7. target bundle + ZIP
8. human verification
9. unverified/blockers
10. preserved exact paths
