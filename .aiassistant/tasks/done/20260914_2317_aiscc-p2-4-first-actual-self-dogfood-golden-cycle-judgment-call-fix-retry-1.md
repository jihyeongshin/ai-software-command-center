# 작업지시서: P2-4 actual self-dogfood golden cycle — Judgment call correction retry

## meta
- task_id: `20260914_2317_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-judgment-call-fix-retry-1`
- created_at: `2026-09-14T23:17:10+09:00`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `759ff20699a048e43ac2fbc66ee3498da758a309`
- required_parent: `609d3063ee9e707dae8b2cc7834647b617c2f5a1`
- predecessor_result_zip_sha256: `a10c7276531c05cbf72b91d8dc919540917e33202eace7127ffc971a321cf061`
- migration_head: `20260914_0012`
- fresh_IDE_chat_required: `No`
- execution_mode: `MANUAL_COMMAND_CENTER_OUTER / AISCC_SELF_DOGFOOD_INNER`
- actual_golden_cycle_authorized: `Yes / one fresh lineage`
- governance_commit_authorized: `Yes / exact 4 paths / Commit A`
- exact_failed_target_cleanup_authorized: `Yes / untracked target only / after hash verification`
- product_source_test_rule_migration_state_mutation_authorized: `No`
- provider_LLM_external_network_authorized: `No`
- push_deploy_authorized: `No`
- success_ceiling: `P2_4_FIRST_SELF_DOGFOOD_GOLDEN_CYCLE_CANDIDATE / BROWSER_REVIEW_REQUIRED`

# 0. Browser judgment
2301 is `ACCEPTED_AS_TRUTHFUL_FAIL_CLOSED`.

It is not a product regression or authority gap.

Actual runtime succeeded through P1-6 SATISFIED and failed only because `judgment_owner.issue(...)` omitted the policy-required typed `evidence_basis_kind`.

# 1. predecessor evidence
- `CONTRACT_REVIEW.md`: `d9220b92d304dcb115f3a4f1ec378eac55861e9643d36f3cffce83dcc78e16b5`
- `DRIVER_CORRECTION_REVIEW.md`: `eb762e6b0caa2942a836c03cc1c44f55da8d2ccc7a9937ada28f4ec4227c88a6`
- `EXECUTOR_REPORT.md`: `4388747f17cc3d240b28ccb71fb18bd988f57b2f6bf01375cd09b4276bede278`
- `GOLDEN_EVIDENCE.json`: `9b783bdc0a5604ca4248ed8364375df2046c74fdb5ca6ad394ce5ce534d15535`
- `GOLDEN_EXTERNAL_START.json`: `57977d1524545e1d7188ea8b21ef8f5dbd6e714703d3076c490f09b168353be8`
- `GOLDEN_EXTERNAL_SUBMISSION.json`: `668a7609acafb3fbf93a650f91cbbc810a3660211718f5e96bd27c86d2b2136f`
- `GOLDEN_GENESIS.json`: `64885df27309dc905bac7681376b610ca29e67c6e13ca917ccc3eadfbc287e45`
- `GOLDEN_JUDGMENT.json`: `f7a7bc1e030aa973051be9512e6b340953a8ffd8bfe260e1a1d12870364facb0`
- `GOLDEN_PROVENANCE.json`: `aa89e35384864effa750f470554a3c3e9324c231308e7ef94516373a60eb1395`
- `GOLDEN_RUNTIME_SOURCE_AUDIT.md`: `d87f9e5b83f900d5af80b3ae7da42c3d8241039c2489a056db5f250dd1fe0524`
- `GOLDEN_SPEC.json`: `f5ddf0a7c18cdd03615ec062953a9b7d8d473409296a9112931bbc148185eea2`
- `GOLDEN_TASKCONTRACT.json`: `2ef6ba43a491c1552a9aae7f055089b8eaf90733a5300bd595719d3e723519cf`
- `GOLDEN_TRANSITIONS.json`: `00c373447ae964fa71a6b6113620320d58f58f50c7620f6558cd630a59b72fd8`
- `GOLDEN_WORKRUN.json`: `38a460d82013825e3c1a57e7a2db72c3a31126c182bd3b8f14362351a8c550c9`
- `evidence/COMMIT_A.json`: `6afe0df41ed321b8267ae87f0d3aaf3c2af31ee3b44ac6c63ce1bfac34aff21d`
- `evidence/JUDGMENT_POLICY_OWNER_READ.json`: `8051ffc69f4d23e9a2feacce10f03e777f50371fd0a8720afde8e21983a49dd3`
- `evidence/READONLY_TERMINAL_RUNTIME.json`: `4899a754daeebda941d76e4b04ce70c3a33dd5631714cbacaa1b521a9f1c5dbb`
- `evidence/RUNTIME_STOP.json`: `0fbc85f616c66e0f3cd50dfed9e1e9f8617d1abec3e1ea4399f3ea60008b9fde`
- `evidence/TERMINAL_WORKSPACE.json`: `09ee3ba72f8ca33f93e671a4fbf6bf2c149edf208537f64fe820f1741e51f03d`
- `runtime/golden_driver.py`: `263e4f4acf0d7967ed69c20bd97bdc2eb78c91562ad3df7bf288abe1fd1950e2`

Copy only after Task-first read into:
`.aiassistant/reports/target/20260914_2317_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-judgment-call-fix-retry-1/accepted-input/`

# 2. initial repository preflight
Require:
```text
branch = main
HEAD = 759ff20699a048e43ac2fbc66ee3498da758a309
HEAD^ = 609d3063ee9e707dae8b2cc7834647b617c2f5a1
index empty
tracked clean
Git-visible untracked exactly:
docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md
```

Require target SHA:
`7890b048be5e7c4a1c679c388b0d05267a63445a2c3558b88fce3fd8f518b368`

Require current 2301 Tasks active byte-exact:
```text
.aiassistant/tasks/active/20260914_2301_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-driver-fix-retry-1.md
SHA e99e36aa3b20c528cad0f4c0e5f877f2bed9d3ba710e82497240c947670a6dfb

.aiassistant/tasks/active/20260914_2301_aiscc-p2-4-golden-agent-single-file-proof-change-3.md
SHA 0b3ae3ab85fc0bf3a9d121865735c41f595756e2bc4a185848ab893dfa22c912
```

Preserve legacy 1400 SHA:
`52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb`

Canonical state hashes unchanged:
- CURRENT_STATE_SUMMARY `80b16f9a5fab2aa7870baeac4ec6fbf27d08bb50637ed61618573ce0bc2ded48`
- DECISION_REGISTER `9da6dde722f2552020a40085995fef062a8920e477da7656c3a176fff52142e5`
- NEXT_ACTIONS `050a93baf1740f298ec2601c08b392118b143f9838002c159b5401ccf6418679`

# 3. Governance Commit A
Task-first transport applies.

Move failed 2301 Tasks byte-exact active -> done.

Place current Cycle/Judgment.

Stage EXACTLY:
```text
.aiassistant/tasks/done/20260914_2301_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-driver-fix-retry-1.md
.aiassistant/tasks/done/20260914_2301_aiscc-p2-4-golden-agent-single-file-proof-change-3.md
.aiassistant/records/aiscc/cycles/20260914_2317_aiscc-p2-4-2301-golden-judgment-call-failure-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260914_2317_aiscc-p2-4-2301-golden-judgment-call-composition-failure-retry-authorization-1.md
```

Do NOT stage the untracked target.

Commit message:
`docs(aiscc): record golden judgment call failure and retry`

Require exact four paths and parent `759ff20699a048e43ac2fbc66ee3498da758a309`.

# 4. exact failed-target cleanup
After Commit A and after predecessor bundle evidence is safely copied/exported:

Verify again:
```text
target = docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md
SHA = 7890b048be5e7c4a1c679c388b0d05267a63445a2c3558b88fce3fd8f518b368
Git status = untracked only
```

Delete EXACTLY that untracked file.

If `docs/` becomes empty, removing the empty directory is allowed housekeeping.

No broad clean/reset.

Require repository is now fully clean, including untracked paths = 0.

This deletion is cleanup of the failed 2301 uncommitted Agent artifact, not rewriting historical evidence; the exact bytes remain preserved in the 2301 result bundle.

# 5. exact new inner Task
Package member:
`20260914_2317_aiscc-p2-4-golden-agent-single-file-proof-change-4.md`

SHA:
`b62c43537c5edc0ce99cc8c45b7fc7f73d96ad90561fe6507571c0eed86c88ce`

Target:
`docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md`

Expected target SHA:
`7890b048be5e7c4a1c679c388b0d05267a63445a2c3558b88fce3fd8f518b368`

# 6. mandatory post-evidence driver conformance audit BEFORE runtime
Before creating the new DB, inspect current source signatures/contracts for every remaining operation from P1-6 satisfaction onward:

1. `PostgresJudgmentAuthority.issue`
2. Judgment participant construction
3. terminal P1-4 ACCEPTED transition
4. MemoryDeclaration/current-context projection
5. CycleCandidate construction
6. Cycle admission repository call
7. post-Cycle Genesis currentness verification
8. post-Cycle CYCLE_DERIVED descriptor/proposal/selection
9. final currentness verification

Create:
`GOLDEN_POST_EVIDENCE_CALL_CONFORMANCE_AUDIT.md`

For every call record exact required typed arguments and the intended driver expression.

If a required source API is absent:
`GOLDEN_AUTHORITY_GAP` STOP.

If only driver wiring is needed, correct the Task-owned driver before runtime.

Do not discover another known signature mismatch by execution when static source inspection can establish it.

# 7. mandatory Judgment correction
The driver MUST import/use the existing:
`JudgmentEvidenceBasisKind`.

The Judgment call must pass exactly the registered policy basis:

```python
evidence_basis_kind=JudgmentEvidenceBasisKind.SATISFIED_ATTESTATION
```

alongside the already verified:
- exact policy
- exact SATISFIED attestation ref
- no HumanResult
- exact reason vocabulary fields

Before runtime, static audit must confirm the call includes the argument and matches the current source signature.

Do not weaken policy registration.

# 8. fresh runtime identity
Do not reuse any 2216/2301 operational DB/authority.

Use:
```text
project_id = aiscc-self-dogfood-p2-4-golden-3
genesis_authority_id = aiscc-golden-genesis-3
genesis_selection_id = aiscc-golden-genesis-selection-3
contract_id = aiscc-p2-4-golden-cycle-3
contract_version = 1
work_run_id = aiscc-p2-4-golden-workrun-3
```

Use fresh transition/request IDs.

# 9. actual runtime
Use one Task-owned local `postgres:17.6`, `--pull=never`, loopback-only, empty DB upgraded to `0012`.

No tests imports/pytest fixtures/monkeypatch/direct owner-row writes/fake refs/Replay-current substitution.

# 10. owner chain through P1-6
Repeat the already-proven owner chain with fresh IDs:
```text
P1-6/P1-7 owner config
→ SELF_DOGFOOD_GENESIS current
→ genesis TaskContract
→ SelfDogfoodTaskSpec
→ READY/v1
→ external start
→ RUNNING/v2
→ clean completion lease BEFORE edit
→ parent mkdir if absent
→ exact target edit
→ authenticated external submission
→ ADMISSION_PENDING/v3
→ execution evidence admission
→ structured NEXT_ACTION_CONTEXT evidence admission
→ EvidenceSet SATISFIED
```

Target creation must again use safe parent mkdir immediately before exclusive file creation and only after clean lease.

# 11. Judgment + terminal ACCEPTED
Issue Judgment with the exact corrected typed basis.

Require:
```text
JudgmentKind = ACCEPTED
evidence_basis_kind = SATISFIED_ATTESTATION
HumanResult = none
owner policy exact
```

Then drive existing P1-4 terminal transition.

Require:
```text
WorkRun = ACCEPTED
terminal transition ADMITTED
```

No fabricated guard facts.

# 12. first real Cycle
Admit exactly one P1-8 Cycle through owner APIs.

Bind:
Genesis source NextAction, Task, TaskContract, full WorkRun chain, external start/submission, admitted evidence/satisfaction, Judgment, terminal decision, structured NEXT_ACTION_CONTEXT.

No direct Cycle/memory writes.

Require after admission:
```text
Genesis currentness = DENY permanently
normal current ProjectMemory/NEXT_ACTION_CONTEXT exists
```

# 13. Result Commit B
Only after real Cycle admission.

Stage EXACTLY:
`docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md`

Commit message:
`docs(aiscc): prove first self dogfood golden cycle`

Require exact one path and parent = retry Governance Commit A.

# 14. resulting NextAction
Using the first real Cycle/current memory, produce/select:
```text
source mode = CYCLE_DERIVED
expected action = open-cycle-derived-task-issuance
```

Owner currentness must PASS.

If truthful selection cannot be produced:
`GOLDEN_NEXT_ACTION_UNAVAILABLE` STOP.

# 15. lifecycle/export
After full success only, move current outer/inner Tasks active -> done byte-exact; do not include them in Commit B.

Export full owner-read golden provenance, including:
Genesis, TaskContract, spec, WorkRun/transitions, external start/submission, evidence, Judgment, Cycle, Result Commit B, resulting CYCLE_DERIVED NextAction and provenance root.

Also export `GOLDEN_POST_EVIDENCE_CALL_CONFORMANCE_AUDIT.md`.

# 16. cleanup/final
After frozen exports:
- remove exact Task-owned DB/container/volume
- no prune

Require:
- target committed exact SHA
- index empty
- tracked clean
- canonical state unchanged
- migration head 0012
- legacy 1400 unchanged
- Docker residue 0

# 17. prohibited
No product runtime/test/rule/migration/canonical-state change.
No provider/LLM/external network.
No push/deploy.
No reuse/recovery of prior operational DBs.
No fabricated authority.
No broad Git/Docker cleanup.

# 18. named blockers
`BLOCKED_MISSING_ARTIFACT`
`DIRTY_WORKSPACE_MIXED`
`POLICY_CONFLICT_INVESTIGATION_REQUIRED`
`GOLDEN_AUTHORITY_GAP`
`GOLDEN_EVIDENCE_INGRESS_UNAVAILABLE`
`GOLDEN_JUDGMENT_POLICY_UNAVAILABLE`
`GOLDEN_CYCLE_ADMISSION_UNAVAILABLE`
`GOLDEN_NEXT_ACTION_UNAVAILABLE`
`ISOLATED_POSTGRES_IMAGE_MISSING`
`BLOCKED_REQUIRED_EVIDENCE`
`SECURITY_BOUNDARY_BLOCKED`

# 19. success ceiling
Only:
`P2_4_FIRST_SELF_DOGFOOD_GOLDEN_CYCLE_CANDIDATE / BROWSER_REVIEW_REQUIRED`

Do not claim P2-4 closed or canonical state reconciled.
