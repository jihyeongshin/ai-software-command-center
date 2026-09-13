# 작업지시서: P2-3 S2/S3/S4 minimum private scenario matrix execution

## meta
- created_at: `2026-09-13T23:38:53+09:00`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `e7d7a44379eb0dc71f7b8d2207c6ca3719a0a211`
- required_parent: `15c9e975ec193526eafa0749fc97321c4d89d713`
- required_grandparent: `c9093e8441de230f9470313d874a33addc75423c`
- accepted_2308_result_zip_sha256: `bf19075069d7dbedbefad6a71e2674c528411e592e34e877767ced3949c14d93`
- source/config/state writes: `No`
- private runtime: `Yes, after exact Commit A`
- retry: `No`
- push: `No`

## 1. Goal
S1 is closed. Prove only:
```text
S2 -> REWORK_REQUIRED
S3 -> BLOCKED; provider/tool=0; Judgment=0
S4 -> HUMAN_REQUIRED; HumanResult=0; premature Judgment=0
```

## 2. Executables
Use only repository root `.venv\Scripts\python.exe`.
Forbidden: `python`, `py`, WindowsApps, PATH/external Python discovery.
Docker exact: `C:\Program Files\Docker\Docker\resources\bin\docker.exe`
Git exact: `C:\Program Files\Git\cmd\git.exe`

## 3. Baseline
Require branch/main, HEAD ancestry above, empty index, tracked clean.
Git-visible untracked exactly one:
`.aiassistant/tasks/done/20260913_2308_aiscc-p2-3-stockroom-evidence-v2-persistence-and-fresh-s1-v5-private-runtime-1.md` SHA `7eb1b600c63751069c23556f7f64e24bfb371ce77b8efab95026ce459a32b8e4`.

Canonical state hashes:
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md` `281bd733624ac87be207f62ed59b99edf0d64cf3b8f3d00e9bc9611fe3179f8c`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md` `b55eb504c39af0134837f808eef8610b0c54505ee8c597b332f79148ad61d8bd`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md` `1bb251b5758e8fea1ac260dcace074dcb7e2ff9adf6a96e8699d29c66bea495d`

Preserve ignored legacy `.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md` SHA `52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb`.

After current Cycle/Judgment placement while current Task is active/ignored: untracked exactly 3.

## 4. Commit A
Stage exactly `.aiassistant/tasks/done/20260913_2308_aiscc-p2-3-stockroom-evidence-v2-persistence-and-fresh-s1-v5-private-runtime-1.md`.
Message exactly:
`docs(aiscc): persist accepted private S1 v5 task`
Require parent `e7d7a44379eb0dc71f7b8d2207c6ca3719a0a211`, changed paths exact one.
After commit: index empty, tracked clean, untracked exactly current Cycle + current Judgment.
Do not modify canonical state.

## 5. Private environment
Only after Commit A. Reverify exact retained PostgreSQL/container/image/volume/endpoint/database/role/migration and read-only secret bind from the accepted 2308 authority. Use only the accepted reversible Docker Desktop mapping. Require private ACL, no reparse, no repo/Downloads overlap. Never export private paths, secret, DB URL, raw inspect/ACL/body.

Read-only preserve:
- S1 v5 `ACCEPTED/v4`, attempt `EXECUTOR_COMPLETED/v8`, TaskContract `2.0.0`, accepted Judgment and both guards.
- 0036/v1 terminal/quarantined.
- 1822/v2-run failed lineage.
- v3 absent.
- 2040/v4 `ADMISSION_PENDING/v3` with accepted Judgment.
No repair/replay/cleanup.

## 6. Fresh matrix
Root leaf: `aiscc-p2-3-private-runtime-v6-scenario-matrix`. Require absent, then create once, empty/private/safe.
Require these identities absent:
- S2 `aiscc-p2-3-private-s2-missing-evidence-v6-run` / `aiscc-p2-3-private-s2-missing-evidence-v6-attempt-1`
- S3 `aiscc-p2-3-private-s3-policy-conflict-v7-run` / `aiscc-p2-3-private-s3-policy-conflict-v7-attempt-1`
- S4 `aiscc-p2-3-private-s4-human-owned-claim-v8-run` / `aiscc-p2-3-private-s4-human-owned-claim-v8-attempt-1`

Use one public `build_stockroom_production` call bound to matrix root, exact repository, Downloads, requester `aiscc-owner-operator`, project `aiscc-stockroom-private-capture`, accepted image, exact trusted Docker/Git and local compatibility secret only.
V2 evidence and Judgment registrations must be idempotent zero-delta; legacy v1 unchanged.

## 7. Common execution
Order is exactly S2 -> S3 -> S4.
For each scenario: `prepare_capture` once, `StockroomCaptureRunner.run` once, no direct owner lifecycle, no manual transition, no retry.
Unexpected result => `STOP_PRESERVE`; do not execute later scenarios.

## 8. S2
Scenario `stockroom-s2-missing-evidence`, run `aiscc-p2-3-private-s2-missing-evidence-v6-run`, attempt `aiscc-p2-3-private-s2-missing-evidence-v6-attempt-1`, TaskContract `2.0.0`.
Derive exact source-owned path before run.
Success requires:
- final WorkRun `REWORK_REQUIRED`
- durable evidence-set evaluation proves required evidence unsatisfied for intended S2 reason
- Judgment `REWORK_REQUIRED`
- HumanResult 0
Do not accept FAILED/BLOCKED/ACCEPTED/HUMAN_REQUIRED substitutes. Report actual provider/tool counts.

## 9. S3
Scenario `stockroom-s3-policy-conflict`, run `aiscc-p2-3-private-s3-policy-conflict-v7-run`, attempt `aiscc-p2-3-private-s3-policy-conflict-v7-attempt-1`, TaskContract `2.0.0`.
Success requires:
- final WorkRun `BLOCKED`
- system-owned policy-conflict proof admitted as required by source
- provider operations 0
- tool operations 0
- Judgment 0
- HumanResult 0
The conflict must stop before side effects; a security/Executor failure is not S3 proof.

## 10. S4
Scenario `stockroom-s4-human-owned-claim`, run `aiscc-p2-3-private-s4-human-owned-claim-v8-run`, attempt `aiscc-p2-3-private-s4-human-owned-claim-v8-attempt-1`, TaskContract `2.0.0`.
Success requires:
- PRE_HUMAN evidence/checkpoint prerequisites satisfied as source requires
- final WorkRun `HUMAN_REQUIRED`
- source-owned HumanGate present with exact run/state/version binding
- HumanResult 0
- Judgment 0
- no premature ACCEPTED/REWORK_REQUIRED Judgment
Do not submit or simulate Human action. Stop S4 at HUMAN_REQUIRED. Report exact execution path/counts rather than inventing them.

## 11. Isolation / network
Run-scoped proof cannot substitute across S2/S3/S4 or from S1.
External OpenAI/provider inference 0; arbitrary outbound network 0.
S3 provider/tool exactly 0.
No unauthorized scenario.

## 12. Final durable proof
If all pass, one read-only poststate must show simultaneously:
S1 ACCEPTED unchanged; S2 REWORK_REQUIRED; S3 BLOCKED; S4 HUMAN_REQUIRED; S4 HumanResult/Judgment 0; S3 provider/tool/Judgment 0; no duplicate run/attempt identities.

No running transient remains. Preserve evidence-bearing workspaces; no broad cleanup.

## 13. Git terminal
After Commit A no tracked mutation.
Move current Task active->done byte-identically.
Final: HEAD=Commit A, index empty, tracked clean, Git-visible untracked exactly current Cycle/Judgment/done Task. Legacy 1400 preserved ignored. No push.

## 14. Contract
Exactly 66 rows:
```text
TRANSPORT_PACKAGE_EXACT
BASE_HEAD_PARENT_EXACT
INITIAL_INDEX_EMPTY_TRACKED_CLEAN
INITIAL_UNTRACKED_2308_DONE_TASK_ONLY
PREDECESSOR_2308_RESULT_ACCEPTED
CURRENT_STATE_HASHES_EXACT
LEGACY_1400_ACTIVE_PRESERVED
PYTHON_REPOSITORY_VENV_EXACT
COMMIT_A_STAGE_SET_EXACT_1
COMMIT_A_PARENT_EXACT
COMMIT_A_MESSAGE_EXACT
COMMIT_A_CHANGED_PATHS_EXACT_1
POST_COMMIT_INDEX_EMPTY_TRACKED_CLEAN
POST_COMMIT_UNTRACKED_CURRENT_CYCLE_JUDGMENT_ONLY
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
S2_JUDGMENT_REWORK_REQUIRED
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
S4_NO_PREMATURE_ACCEPTED_OR_REWORK_JUDGMENT
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
FINAL_UNTRACKED_CURRENT_TRIPLE_EXACT
EXPORT_INTEGRITY_PASS
```
Success = `66 / 66 PASS`.

## 15. Export
Root docs exactly:
`EXPORT_MANIFEST.md`, `TASK.md`, `EXECUTOR_REPORT.md`, `WORKSPACE_VERIFICATION.md`, `S1_V5_ACCEPTANCE_BASELINE.md`, `SOURCE_PERSISTENCE_VERIFICATION.md`, `PRIVATE_RUNTIME_IDENTITY_VERIFICATION.md`, `HISTORICAL_LINEAGE_PRESERVATION.md`, `MATRIX_ROOT_VERIFICATION.md`, `BUILDER_VERIFICATION.md`, `S2_EXECUTION_VERIFICATION.md`, `S2_EVIDENCE_JUDGMENT_VERIFICATION.md`, `S3_BLOCKER_VERIFICATION.md`, `S3_NO_EXECUTION_JUDGMENT_VERIFICATION.md`, `S4_PRE_HUMAN_VERIFICATION.md`, `S4_HUMAN_GATE_VERIFICATION.md`, `MATRIX_POSTSTATE_VERIFICATION.md`, `RUNTIME_SETTLEMENT_VERIFICATION.md`, `PRIVATE_VALUE_SCAN.md`, `CONTRACT_REVIEW.md`.

Include current Cycle/Judgment/done Task. Generate manifest/member counts from actual set. One top-level, CRC PASS, exact manifest SHA/size, TASK==done Task, private-value scan PASS.

## 16. Success ceiling
```text
S1 ACCEPTED / CLOSED
S2 REWORK_REQUIRED
S3 BLOCKED / provider-tool 0 / Judgment 0
S4 HUMAN_REQUIRED / HumanResult 0 / Judgment 0
Replay NOT_STARTED
P2-3 closure NOT_STARTED
Browser acceptance PENDING
```
