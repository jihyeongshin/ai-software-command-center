# 작업지시서: P2-3 S2/S3/S4 separate production applications runtime retry

## meta
- created_at: `2026-09-14T00:09:29+09:00`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `be2489515ba7799466ffdf415b47e4d3e0a79e46`
- required_parent: `c26ec9eb342d052c726c57b5df42ced70e01a757`
- required_grandparent: `e7d7a44379eb0dc71f7b8d2207c6ca3719a0a211`
- reviewed_2357_result_zip_sha256: `ec01a0b28340ca296f9f7d62ef49f112efaa2a150e3f57b9636e946a27a352c9`
- source/config/state writes: `No`
- private runtime: `Yes / after exact Commit A`
- scenario retry: `No`
- push: `No`

## 1. Corrected composition authority
2357 proved that one production application cannot safely execute multiple distinct attempt identities.

Use exactly three public production builds:

```text
S2: root aiscc-p2-3-private-runtime-v6-s2; cancellation (aiscc-p2-3-private-s2-missing-evidence-v6-run, aiscc-p2-3-private-s2-missing-evidence-v6-attempt-1)
S3: root aiscc-p2-3-private-runtime-v7-s3; cancellation (aiscc-p2-3-private-s3-policy-conflict-v7-run, aiscc-p2-3-private-s3-policy-conflict-v7-attempt-1)
S4: root aiscc-p2-3-private-runtime-v8-s4; cancellation (aiscc-p2-3-private-s4-human-owned-claim-v8-run, aiscc-p2-3-private-s4-human-owned-claim-v8-attempt-1)
```

Each application is used only for its matching scenario.

Forbidden: internal builder calls, cancellation rebinding, replacing/resetting Docker runner, resetting dispatch flags, private-attribute mutation, source rework.

## 2. Executables
Use only repository-root `.venv\Scripts\python.exe`.
Forbidden: `python`, `py`, WindowsApps, PATH Python discovery, external Python/venv discovery.
Docker exact: `C:\Program Files\Docker\Docker\resources\bin\docker.exe`
Git exact: `C:\Program Files\Git\cmd\git.exe`

## 3. Repository baseline
Require branch main, HEAD `be2489515ba7799466ffdf415b47e4d3e0a79e46`, HEAD^ `c26ec9eb342d052c726c57b5df42ced70e01a757`, HEAD^^ `e7d7a44379eb0dc71f7b8d2207c6ca3719a0a211`, index empty, tracked clean.

Git-visible untracked exactly one:
`.aiassistant/tasks/done/20260913_2357_aiscc-p2-3-s2-s3-s4-minimum-private-scenario-matrix-judgment-literal-corrected-retry-1.md` SHA `94176e2823b16f06c80bc0eaf7a69c8ea80b40dde5af1f058051cdfe182177dd`.

Canonical state hashes:
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md` `281bd733624ac87be207f62ed59b99edf0d64cf3b8f3d00e9bc9611fe3179f8c`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md` `b55eb504c39af0134837f808eef8610b0c54505ee8c597b332f79148ad61d8bd`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md` `1bb251b5758e8fea1ac260dcace074dcb7e2ff9adf6a96e8699d29c66bea495d`

Preserve ignored legacy:
`.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md` SHA `52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb`.

After current Cycle/Judgment placement while current Task active/ignored: Git-visible untracked exactly three = 2357 done Task + current Cycle + current Judgment.
Mismatch -> STOP before Git/private mutation.

## 4. Commit A
Stage exactly `.aiassistant/tasks/done/20260913_2357_aiscc-p2-3-s2-s3-s4-minimum-private-scenario-matrix-judgment-literal-corrected-retry-1.md`.

Commit message exactly:
`docs(aiscc): persist matrix composition blocker task`

Require parent `be2489515ba7799466ffdf415b47e4d3e0a79e46` and changed paths exact one.

After commit: HEAD=Commit A; index empty; tracked clean; Git-visible untracked exactly current Cycle + current Judgment. Current active Task remains ignored.
Failure -> STOP before private access.

## 5. Private environment / historical baseline
Only after Commit A, reverify the exact retained PostgreSQL/container/image/volume/endpoint/database/role/migration and read-only secret bind from accepted S1 v5 authority.

Use only accepted reversible Docker Desktop mapping. Require protected/private ACL, no reparse, no repo/Downloads overlap. Never export private absolute paths, secret, DB URL, raw inspect, ACL body or evidence body.

Read-only preserve:
- S1 v5 ACCEPTED/v4, attempt EXECUTOR_COMPLETED/v8, TaskContract 2.0.0, accepted Judgment and both guards.
- 0036/v1 terminal/quarantined.
- 1822/v2-run failed.
- v3 absent.
- 2040/v4 ADMISSION_PENDING/v3 with accepted Judgment.

No repair/replay/transition/cleanup.

## 6. Fresh roots and identities
Require roots absent: `aiscc-p2-3-private-runtime-v6-s2`, `aiscc-p2-3-private-runtime-v7-s3`, `aiscc-p2-3-private-runtime-v8-s4`.
Require run/attempts absent:
- S2 `aiscc-p2-3-private-s2-missing-evidence-v6-run` / `aiscc-p2-3-private-s2-missing-evidence-v6-attempt-1`
- S3 `aiscc-p2-3-private-s3-policy-conflict-v7-run` / `aiscc-p2-3-private-s3-policy-conflict-v7-attempt-1`
- S4 `aiscc-p2-3-private-s4-human-owned-claim-v8-run` / `aiscc-p2-3-private-s4-human-owned-claim-v8-attempt-1`

If any exists -> STOP. Do not reuse/delete.

Create each root once and require empty, exact, no reparse, ACL no broader than private parent, no repo/Downloads overlap.

## 7. Common builder rules
Use retained Stockroom image exact identity.

Call public `build_stockroom_production` exactly three times total: once for S2, once for S3, once for S4.

Each call uses exact repository at Commit A, its own private root, exact cancellation matching its own run/attempt, project `aiscc-stockroom-private-capture`, requester `aiscc-owner-operator`, human selector fingerprint `c55280095ff8bbac5ab186e44e3856e6a435da548c1c88b02b66caeba36e8f07`, exact trusted Docker/Git, accepted image provenance and local compatibility secret only.

Before/after each builder prove:
- v2 EvidenceRequirementSet/Requirement/Checkpoint durable registration delta = 0
- v2 JudgmentPolicy/Projection durable registration delta = 0
- legacy v1 authority unchanged

No direct internal builder call. Do not require DB pristine.

## 8. Execution order / stop rule
Execute exactly S2 -> S3 -> S4.

For each: `prepare_capture` exactly once on its own application, `StockroomCaptureRunner.run` exactly once, no direct owner lifecycle, no manual transition, no retry.

Unexpected semantic/exception -> STOP_PRESERVE; do not execute later scenarios.

## 9. S2 missing evidence
Application cancellation `aiscc-p2-3-private-s2-missing-evidence-v6-run` / `aiscc-p2-3-private-s2-missing-evidence-v6-attempt-1`.
Scenario `stockroom-s2-missing-evidence`, TaskContract 2.0.0.

Success:
- final WorkRun `REWORK_REQUIRED`
- evidence set durably `UNSATISFIED` for intended missing-evidence reason
- durable JudgmentKind exactly `HOLD_REWORK_REQUIRED`
- source-owned mapping to WorkflowState `REWORK_REQUIRED`
- HumanResult 0
- no running transient

Report actual provider/tool/execution counts.

## 10. S3 policy conflict
Application cancellation `aiscc-p2-3-private-s3-policy-conflict-v7-run` / `aiscc-p2-3-private-s3-policy-conflict-v7-attempt-1`.
Scenario `stockroom-s3-policy-conflict`, TaskContract 2.0.0.

Success:
- final WorkRun `BLOCKED`
- source-owned policy-conflict proof
- provider operations 0
- tool operations 0
- Judgment 0
- HumanResult 0
- no running transient

Conflict must block before side effects. Security/Executor failure is not a substitute.

## 11. S4 human-owned claim
Application cancellation `aiscc-p2-3-private-s4-human-owned-claim-v8-run` / `aiscc-p2-3-private-s4-human-owned-claim-v8-attempt-1`.
Scenario `stockroom-s4-human-owned-claim`, TaskContract 2.0.0.

Success:
- PRE_HUMAN evidence/checkpoint prerequisites satisfied as source requires
- final WorkRun `HUMAN_REQUIRED`
- source-owned HumanGate exact run/state/version binding
- HumanResult 0
- Judgment 0
- no premature ACCEPTED or HOLD_REWORK_REQUIRED Judgment
- no running transient

Do not submit/simulate Human action. Stop at HUMAN_REQUIRED.

## 12. Cross-scenario isolation
Require each scenario records bind only its own run/attempt.
No S1 or other scenario run-scoped evidence may substitute.
Only canonical non-run-scoped v2 authority may be reused.
External OpenAI/provider inference = 0. Arbitrary outbound network = 0.

## 13. Final simultaneous poststate
If all pass, capture one read-only poststate:

```text
S1 v5: ACCEPTED unchanged
S2: WorkRun REWORK_REQUIRED; JudgmentKind HOLD_REWORK_REQUIRED
S3: WorkRun BLOCKED; provider 0; tool 0; Judgment 0; HumanResult 0
S4: WorkRun HUMAN_REQUIRED; HumanGate present; HumanResult 0; Judgment 0
```

Also prove no duplicate WorkRun/attempt identities.

## 14. Failure / cleanup
No scenario retry.
On failure: preserve Commit A and completed/current evidence; do not run later scenarios; no DB repair/manual transition/destructive cleanup; STOP_PRESERVE.
No broad cleanup.

## 15. Git terminal
After Commit A no tracked/source/config/state mutation.
Move current Task active->done byte-identically.

Final success:
- HEAD=Commit A
- index empty
- tracked clean
- Git-visible untracked exactly current Cycle/Judgment/done Task
- legacy 1400 preserved ignored/non-owned
- no push

## 16. Contract review
Exactly 82 rows:

```text
TRANSPORT_PACKAGE_EXACT
BASE_HEAD_PARENT_EXACT
INITIAL_INDEX_EMPTY_TRACKED_CLEAN
INITIAL_UNTRACKED_2357_DONE_TASK_ONLY
PREDECESSOR_2357_RESULT_ACCEPTED
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
S2_ROOT_ABSENT_BEFORE_CREATE
S3_ROOT_ABSENT_BEFORE_CREATE
S4_ROOT_ABSENT_BEFORE_CREATE
S2_RUN_ATTEMPT_ABSENT_BEFORE_CREATE
S3_RUN_ATTEMPT_ABSENT_BEFORE_CREATE
S4_RUN_ATTEMPT_ABSENT_BEFORE_CREATE
S2_ROOT_CREATED_EMPTY_PRIVATE
S3_ROOT_CREATED_EMPTY_PRIVATE
S4_ROOT_CREATED_EMPTY_PRIVATE
STOCKROOM_IMAGE_IDENTITY_EXACT
SEPARATE_APPLICATION_BUILDER_TOTAL_EXACT_3
S2_BUILDER_SINGLE_CALL
S2_CANCELLATION_BOUND_EXACT
S2_V2_AUTHORITY_REGISTRATION_ZERO_DELTA
S2_V2_JUDGMENT_REGISTRATION_ZERO_DELTA
S2_PREPARE_SINGLE_CALL
S2_RUNNER_SINGLE_CALL
S2_TASKCONTRACT_V2_SELECTED
S2_FINAL_WORKRUN_REWORK_REQUIRED
S2_MISSING_EVIDENCE_SEMANTIC_PROVEN
S2_JUDGMENT_HOLD_REWORK_REQUIRED
S2_NO_HUMAN_RESULT
S2_NO_RUNNING_TRANSIENT
S3_BUILDER_SINGLE_CALL
S3_CANCELLATION_BOUND_EXACT
S3_V2_AUTHORITY_REGISTRATION_ZERO_DELTA
S3_V2_JUDGMENT_REGISTRATION_ZERO_DELTA
S3_PREPARE_SINGLE_CALL
S3_RUNNER_SINGLE_CALL
S3_TASKCONTRACT_V2_SELECTED
S3_FINAL_WORKRUN_BLOCKED
S3_POLICY_CONFLICT_EVIDENCE_PROVEN
S3_PROVIDER_TOOL_EXECUTION_ZERO
S3_JUDGMENT_ZERO
S3_HUMAN_RESULT_ZERO
S3_NO_RUNNING_TRANSIENT
S4_BUILDER_SINGLE_CALL
S4_CANCELLATION_BOUND_EXACT
S4_V2_AUTHORITY_REGISTRATION_ZERO_DELTA
S4_V2_JUDGMENT_REGISTRATION_ZERO_DELTA
S4_PREPARE_SINGLE_CALL
S4_RUNNER_SINGLE_CALL
S4_TASKCONTRACT_V2_SELECTED
S4_PREHUMAN_REQUIREMENTS_SATISFIED
S4_FINAL_WORKRUN_HUMAN_REQUIRED
S4_HUMAN_GATE_PRESENT
S4_HUMAN_RESULT_ZERO
S4_JUDGMENT_ZERO
S4_NO_PREMATURE_ACCEPTED_OR_HOLD_REWORK_JUDGMENT
S4_NO_RUNNING_TRANSIENT
NO_EXTERNAL_PROVIDER_NETWORK_ALL_SCENARIOS
NO_SCENARIO_RETRY
NO_UNAUTHORIZED_SCENARIO
NO_CROSS_SCENARIO_RUN_SCOPED_PROOF_REUSE
NO_HISTORICAL_LINEAGE_MUTATION
NO_SOURCE_TEST_CONFIG_STATE_MUTATION
NO_GIT_PUSH
PRIVATE_VALUE_EXPORT_SCAN_PASS
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
FINAL_HEAD_IS_COMMIT_A
FINAL_INDEX_EMPTY_TRACKED_CLEAN
FINAL_UNTRACKED_CURRENT_TRIPLE_EXACT
EXPORT_INTEGRITY_PASS
```

Full success = 82/82 PASS.

## 17. Export
Root docs:
`EXPORT_MANIFEST.md`, `TASK.md`, `EXECUTOR_REPORT.md`, `WORKSPACE_VERIFICATION.md`, `2357_ACCEPTANCE_VERIFICATION.md`, `SOURCE_PERSISTENCE_VERIFICATION.md`, `PRIVATE_RUNTIME_IDENTITY_VERIFICATION.md`, `HISTORICAL_LINEAGE_PRESERVATION.md`, `S2_APPLICATION_VERIFICATION.md`, `S2_EXECUTION_VERIFICATION.md`, `S2_EVIDENCE_JUDGMENT_VERIFICATION.md`, `S3_APPLICATION_VERIFICATION.md`, `S3_BLOCKER_VERIFICATION.md`, `S3_NO_EXECUTION_JUDGMENT_VERIFICATION.md`, `S4_APPLICATION_VERIFICATION.md`, `S4_PRE_HUMAN_VERIFICATION.md`, `S4_HUMAN_GATE_VERIFICATION.md`, `MATRIX_POSTSTATE_VERIFICATION.md`, `RUNTIME_SETTLEMENT_VERIFICATION.md`, `PRIVATE_VALUE_SCAN.md`, `CONTRACT_REVIEW.md`.

Include current Cycle/Judgment/done Task.
Generate manifest/member count from actual declared set.
Require one top-level, CRC PASS, exact manifest SHA/size, TASK==done Task, private-value scan PASS.

## 18. Success ceiling
```text
S1 ACCEPTED / CLOSED
S2 REWORK_REQUIRED + JudgmentKind HOLD_REWORK_REQUIRED
S3 BLOCKED + provider/tool/Judgment/HumanResult 0
S4 HUMAN_REQUIRED + HumanResult/Judgment 0
Replay NOT_STARTED
P2-3 closure NOT_STARTED
Browser acceptance PENDING
```
