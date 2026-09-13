# 작업지시서: P2-3 S2/S3/S4 minimum private scenario matrix Judgment-literal corrected retry

## meta
- created_at: `2026-09-13T23:57:33+09:00`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `c26ec9eb342d052c726c57b5df42ced70e01a757`
- required_parent: `e7d7a44379eb0dc71f7b8d2207c6ca3719a0a211`
- required_grandparent: `15c9e975ec193526eafa0749fc97321c4d89d713`
- reviewed_2338_result_zip_sha256: `e95b78d82b5495aba138aa1427829efc8051543cde62a38c60944b58bb4ad883`
- source/config/state writes: `No`
- private runtime: `Yes, after exact governance Commit A`
- retry: `No`
- push: `No`

## 1. Corrected authority
2338 stopped correctly before private access because the Command Center conflated a WorkflowState with a JudgmentKind.

Exact S2 contract is now:

```text
final WorkRun:
REWORK_REQUIRED

durable JudgmentKind:
HOLD_REWORK_REQUIRED
```

Do not expect or invent `JudgmentKind.REWORK_REQUIRED`; it does not exist.

S3 and S4 expectations remain:
```text
S3 -> BLOCKED; provider/tool=0; Judgment=0
S4 -> HUMAN_REQUIRED; HumanResult=0; Judgment=0
```

## 2. Executables
Use only `<repository-root>\.venv\Scripts\python.exe`.
Forbidden: `python`, `py`, WindowsApps, PATH/external Python discovery.
Docker exact: `C:\Program Files\Docker\Docker\resources\bin\docker.exe`
Git exact: `C:\Program Files\Git\cmd\git.exe`

## 3. Baseline
Require branch/main, exact HEAD ancestry, index empty, tracked clean.
Git-visible untracked before delivery exactly the 2338 triple:

- `.aiassistant/records/aiscc/cycles/20260913_2338_aiscc-p2-3-s1-accepted-s2-s3-s4-minimum-scenario-matrix-entry-1.cycle.md` `0a9c9c4daff4c21974956fe0407c6c656304526d8ff7c11444ac7fa6b78059d8`
- `.aiassistant/reports/aiscc/20260913_2338_aiscc-p2-3-private-s1-v5-final-acceptance-and-scenario-matrix-authorization-1.md` `89820f6da1b1dd09dbb3048a62891e4ae111af2c5e47175b573f6a55c7da5c5b`
- `.aiassistant/tasks/done/20260913_2338_aiscc-p2-3-s2-s3-s4-minimum-private-scenario-matrix-execution-1.md` `ad3babeeb102de75d4272b89e92ea18fc15006ac1da37b5cba3c4eb9c5104da4`

Canonical state hashes:
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md` `281bd733624ac87be207f62ed59b99edf0d64cf3b8f3d00e9bc9611fe3179f8c`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md` `b55eb504c39af0134837f808eef8610b0c54505ee8c597b332f79148ad61d8bd`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md` `1bb251b5758e8fea1ac260dcace074dcb7e2ff9adf6a96e8699d29c66bea495d`

Preserve ignored legacy `.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md` SHA `52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb`.

After current Cycle/Judgment placement while current Task active/ignored:
Git-visible untracked exactly 5 = predecessor triple + current Cycle/Judgment.

## 4. Governance Commit A
Stage exactly five paths:
- predecessor 2338 Cycle/Judgment/done Task
- current Cycle
- current Judgment

Commit message exactly:
`docs(aiscc): persist scenario matrix retry entry`

Require:
- parent `c26ec9eb342d052c726c57b5df42ced70e01a757`
- changed paths exact 5
- current active Task not staged
- canonical state not staged
- legacy 1400 not staged

After Commit A:
- HEAD=Commit A
- index empty
- tracked clean
- Git-visible untracked 0
- current active Task ignored

Any failure -> STOP before private access.

## 5. Private environment and preservation
Only after Commit A exact verification, reverify the retained PostgreSQL/container/image/volume/endpoint/database/role/migration and read-only secret bind exactly as accepted in 2308. Use the accepted reversible Docker Desktop mapping only. Require private ACL, no reparse, no repo/Downloads overlap. Do not export private path/secret/URL/raw inspect/ACL/body.

Read-only preserve:
- S1 v5 `ACCEPTED/v4`, attempt `EXECUTOR_COMPLETED/v8`, TaskContract 2.0.0, accepted Judgment and both guards.
- 0036/v1 terminal/quarantined.
- 1822/v2-run failed.
- v3 absent.
- 2040/v4 `ADMISSION_PENDING/v3` with accepted Judgment.
No repair/replay/cleanup.

## 6. Matrix identities
Root leaf: `aiscc-p2-3-private-runtime-v6-scenario-matrix`.
Because 2338 performed zero private access, the same planned identities may be used only after current read-only proof that root/run/attempts are absent.

Require absent:
- `aiscc-p2-3-private-runtime-v6-scenario-matrix`
- S2 `aiscc-p2-3-private-s2-missing-evidence-v6-run` / `aiscc-p2-3-private-s2-missing-evidence-v6-attempt-1`
- S3 `aiscc-p2-3-private-s3-policy-conflict-v7-run` / `aiscc-p2-3-private-s3-policy-conflict-v7-attempt-1`
- S4 `aiscc-p2-3-private-s4-human-owned-claim-v8-run` / `aiscc-p2-3-private-s4-human-owned-claim-v8-attempt-1`

If any exists -> STOP. Do not reuse/delete.

Create matrix root once, empty/private/safe.

## 7. Builder
Require exact Stockroom image identity.
Call public `build_stockroom_production` exactly once bound to matrix root, exact current repository, Downloads, requester `aiscc-owner-operator`, project `aiscc-stockroom-private-capture`, accepted image provenance, exact trusted Docker/Git and local compatibility secret only.

V2 EvidenceRequirementSet/Requirement/Checkpoint registration: zero durable delta.
V2 JudgmentPolicy/Projection registration: zero durable delta.
Legacy v1 authority unchanged.

## 8. Common execution
Order exactly S2 -> S3 -> S4.
Each scenario:
- `prepare_capture` exactly once
- `StockroomCaptureRunner.run` exactly once
- no direct owner lifecycle
- no manual transition
- no retry

Unexpected semantic/exception -> STOP_PRESERVE and do not execute later scenarios.

## 9. S2 missing evidence
Use `stockroom-s2-missing-evidence`, run `aiscc-p2-3-private-s2-missing-evidence-v6-run`, attempt `aiscc-p2-3-private-s2-missing-evidence-v6-attempt-1`, TaskContract 2.0.0.

Success requires:
- final WorkRun `REWORK_REQUIRED`
- required evidence set durably UNSATISFIED for the intended missing-evidence reason
- durable JudgmentKind exactly `HOLD_REWORK_REQUIRED`
- source mapping from that JudgmentKind to WorkRun `REWORK_REQUIRED`
- HumanResult 0

Do not accept another workflow terminal or another JudgmentKind.
Report actual provider/tool/execution counts from the source-owned path.

## 10. S3 policy conflict
Use `stockroom-s3-policy-conflict`, run `aiscc-p2-3-private-s3-policy-conflict-v7-run`, attempt `aiscc-p2-3-private-s3-policy-conflict-v7-attempt-1`, TaskContract 2.0.0.

Success:
- WorkRun `BLOCKED`
- system-owned policy-conflict proof per current source
- provider operations 0
- tool operations 0
- Judgment 0
- HumanResult 0
- blocker occurs before side effects

Security failure/Executor exception is not a substitute.

## 11. S4 human-owned claim
Use `stockroom-s4-human-owned-claim`, run `aiscc-p2-3-private-s4-human-owned-claim-v8-run`, attempt `aiscc-p2-3-private-s4-human-owned-claim-v8-attempt-1`, TaskContract 2.0.0.

Success:
- current PRE_HUMAN evidence/checkpoint prerequisites satisfied
- WorkRun `HUMAN_REQUIRED`
- source-owned HumanGate with exact run/state/version binding
- HumanResult 0
- Judgment 0
- no premature ACCEPTED or HOLD_REWORK_REQUIRED Judgment

Do not simulate/submit Human action. Stop at HUMAN_REQUIRED.
Report exact source-owned execution path/counts.

## 12. Isolation/network/poststate
Run-scoped proof cannot substitute across scenarios or from S1.
External OpenAI/provider inference 0; arbitrary outbound network 0.
S3 provider/tool exactly 0.

If all pass, one read-only poststate must simultaneously prove:
- S1 ACCEPTED unchanged
- S2 WorkRun REWORK_REQUIRED + JudgmentKind HOLD_REWORK_REQUIRED
- S3 BLOCKED + provider/tool/Judgment 0
- S4 HUMAN_REQUIRED + HumanResult/Judgment 0
- no duplicate run/attempt identities

No running Stockroom transient. Preserve evidence-bearing workspaces; no broad cleanup.

## 13. Failure semantics
No retry.
Any failure: preserve Commit A and all completed/current evidence, do not execute later scenarios, no DB repair/manual transition/destructive cleanup, STOP_PRESERVE.

## 14. Git terminal
After Commit A no tracked/source/config/state mutation.
Move current Task active->done byte-identically.

Final success:
- HEAD=Commit A
- index empty
- tracked clean
- Git-visible untracked exactly one: current done Task
- legacy 1400 ignored/non-owned
- no push

## 15. Contract
Exactly 66 rows:
```text
TRANSPORT_PACKAGE_EXACT
BASE_HEAD_PARENT_EXACT
INITIAL_INDEX_EMPTY_TRACKED_CLEAN
INITIAL_UNTRACKED_2338_TRIPLE_EXACT
PREDECESSOR_2338_RESULT_ACCEPTED
CURRENT_STATE_HASHES_EXACT
LEGACY_1400_ACTIVE_PRESERVED
PYTHON_REPOSITORY_VENV_EXACT
COMMIT_A_STAGE_SET_EXACT_5
COMMIT_A_PARENT_EXACT
COMMIT_A_MESSAGE_EXACT
COMMIT_A_CHANGED_PATHS_EXACT_5
POST_COMMIT_INDEX_EMPTY_TRACKED_CLEAN
POST_COMMIT_UNTRACKED_ZERO
NO_CANONICAL_STATE_MUTATION
PRIVATE_POSTGRES_IDENTITY_EXACT
PRIVATE_SECRET_BIND_AND_ACL_EXACT
PRIVATE_S1_V5_PRESERVED_ACCEPTED
HISTORICAL_V1_V2_V4_PRESERVED
MATRIX_ROOT_ABSENT_BEFORE_CREATE
S2_RUN_ATTEMPT_ABSENT_BEFORE_CREATE
S3_RUN_ATTEMPT_ABSENT_BEFORE_CREATE
S4_RUN_ATTEMPT_ABSENT_BEFORE_CREATE
MATRIX_ROOT_CREATED_EMPTY_PRIVATE
STOCKROOM_IMAGE_IDENTITY_EXACT
BUILDER_SINGLE_CALL
V2_AUTHORITY_REGISTRATION_ZERO_DELTA
V2_JUDGMENT_REGISTRATION_ZERO_DELTA
S2_PREPARE_SINGLE_CALL
S2_RUNNER_SINGLE_CALL
S2_TASKCONTRACT_V2_SELECTED
S2_FINAL_WORKRUN_REWORK_REQUIRED
S2_MISSING_EVIDENCE_SEMANTIC_PROVEN
S2_JUDGMENT_HOLD_REWORK_REQUIRED
S2_NO_HUMAN_RESULT
S3_PREPARE_SINGLE_CALL
S3_RUNNER_SINGLE_CALL
S3_TASKCONTRACT_V2_SELECTED
S3_FINAL_WORKRUN_BLOCKED
S3_POLICY_CONFLICT_EVIDENCE_PROVEN
S3_PROVIDER_TOOL_EXECUTION_ZERO
S3_JUDGMENT_ZERO
S3_HUMAN_RESULT_ZERO
S4_PREPARE_SINGLE_CALL
S4_RUNNER_SINGLE_CALL
S4_TASKCONTRACT_V2_SELECTED
S4_EXECUTION_COMPLETED_OR_SOURCE_EXPECTED_PREHUMAN_PATH
S4_EVIDENCE_PREHUMAN_REQUIREMENTS_SATISFIED
S4_FINAL_WORKRUN_HUMAN_REQUIRED
S4_HUMAN_GATE_PRESENT
S4_HUMAN_RESULT_ZERO
S4_JUDGMENT_ZERO
S4_NO_PREMATURE_ACCEPTED_OR_HOLD_REWORK_JUDGMENT
NO_EXTERNAL_PROVIDER_NETWORK_ALL_SCENARIOS
NO_SCENARIO_RETRY
NO_UNAUTHORIZED_SCENARIO
NO_HISTORICAL_LINEAGE_MUTATION
NO_SOURCE_TEST_CONFIG_STATE_MUTATION
NO_GIT_PUSH
NO_RUNNING_MATRIX_TRANSIENT
PRIVATE_VALUE_EXPORT_SCAN_PASS
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
FINAL_HEAD_IS_COMMIT_A
FINAL_INDEX_EMPTY_TRACKED_CLEAN
FINAL_UNTRACKED_CURRENT_DONE_TASK_ONLY
EXPORT_INTEGRITY_PASS
```
Success = 66/66 PASS.

## 16. Export
Root docs:
`EXPORT_MANIFEST.md`, `TASK.md`, `EXECUTOR_REPORT.md`, `WORKSPACE_VERIFICATION.md`, `2338_ACCEPTANCE_VERIFICATION.md`, `SOURCE_PERSISTENCE_VERIFICATION.md`, `PRIVATE_RUNTIME_IDENTITY_VERIFICATION.md`, `HISTORICAL_LINEAGE_PRESERVATION.md`, `MATRIX_ROOT_VERIFICATION.md`, `BUILDER_VERIFICATION.md`, `S2_EXECUTION_VERIFICATION.md`, `S2_EVIDENCE_JUDGMENT_VERIFICATION.md`, `S3_BLOCKER_VERIFICATION.md`, `S3_NO_EXECUTION_JUDGMENT_VERIFICATION.md`, `S4_PRE_HUMAN_VERIFICATION.md`, `S4_HUMAN_GATE_VERIFICATION.md`, `MATRIX_POSTSTATE_VERIFICATION.md`, `RUNTIME_SETTLEMENT_VERIFICATION.md`, `PRIVATE_VALUE_SCAN.md`, `CONTRACT_REVIEW.md`.

Include current Cycle/Judgment/done Task.
Generate manifest/member count from actual set. One top-level, CRC PASS, exact manifest SHA/size, TASK==done Task, private-value scan PASS.

## 17. Success ceiling
```text
S1 ACCEPTED / CLOSED
S2 REWORK_REQUIRED + JudgmentKind HOLD_REWORK_REQUIRED
S3 BLOCKED / provider-tool 0 / Judgment 0
S4 HUMAN_REQUIRED / HumanResult 0 / Judgment 0
Replay NOT_STARTED
P2-3 closure NOT_STARTED
Browser acceptance PENDING
```
