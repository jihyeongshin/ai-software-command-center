# 작업지시서: P2-3 S3 static-policy MappingProxy serialization targeted source rework

## meta
- created_at: `2026-09-14T00:39:11+09:00`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `33a216f29062176ad196a567a299ba30291c3f72`
- required_parent: `be2489515ba7799466ffdf415b47e4d3e0a79e46`
- required_grandparent: `c26ec9eb342d052c726c57b5df42ced70e01a757`
- reviewed_0009_result_zip_sha256: `23a2227445ffec05ffdd918896e4dcf2c35799faac7813c1b1bea155cc346a9f`
- private runtime / retained PostgreSQL / Docker: `FORBIDDEN`
- source change: `Conditional / exact S3 serialization defect only`
- canonical state writes: `No`
- Git commit/push: `No`

## 1. Baseline
Require exact branch/HEAD ancestry, empty index, tracked clean and Git-visible untracked exactly three:

- `.aiassistant/records/aiscc/cycles/20260914_0009_aiscc-p2-3-scenario-matrix-separate-applications-entry-1.cycle.md` `ad576d179e0893f928d0f20a31209c6a5f0ec78845ef5d2f393dd6bd1506e71e`
- `.aiassistant/reports/aiscc/20260914_0009_aiscc-p2-3-2357-single-builder-scope-conflict-retry-judgment-1.md` `dee53f09c6b8f5771dd09e5e912541faaad803d8a84f1b796c5cd890bc3b7300`
- `.aiassistant/tasks/done/20260914_0009_aiscc-p2-3-s2-s3-s4-separate-production-applications-runtime-retry-1.md` `3ae3533a620c49408b173c6c113fa244fe84a1950bc025c1de67ede1b9c70a68`

Canonical state:
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md` `281bd733624ac87be207f62ed59b99edf0d64cf3b8f3d00e9bc9611fe3179f8c`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md` `b55eb504c39af0134837f808eef8610b0c54505ee8c597b332f79148ad61d8bd`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md` `1bb251b5758e8fea1ac260dcace074dcb7e2ff9adf6a96e8699d29c66bea495d`

Preserve ignored non-owned legacy:
`.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md` SHA `52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb`.

After current Cycle/Judgment placement while current Task is active/ignored, Git-visible untracked must be exactly five.

## 2. Python
Use only `<repository-root>\.venv\Scripts\python.exe`.
Forbidden: `python`, `py`, WindowsApps, PATH/external Python discovery.
Git read-only only.

## 3. Accepted predecessor facts
Do not access private state. Treat only as accepted predecessor evidence:
- S2 `REWORK_REQUIRED/v4`, attempt `EXECUTOR_COMPLETED/v8`, JudgmentKind `HOLD_REWORK_REQUIRED`, HumanResult 0.
- S3 retained run `aiscc-p2-3-private-s3-policy-conflict-v7-run`: WorkRun `RUNNING/v2`, attempt `NOT_STARTED/v1`, provider/tool/output/evidence/blocker/Judgment/HumanResult 0, runner escaped TypeError.
- S4 not started.

Do not replay/repair/transition/clean retained S3.

## 4. Source baseline
Before modification require:
- `src/aiscc/scenarios/stockroom_production.py` SHA `38a6045cab460405627bc9fdd6f43988b74613cb3adbe60e93e972f8ee9586b5`
- `src/aiscc/evidence/models.py` SHA `df48a1c8af09c09827a2d5996e8aed19c3642e9f8b099b58e75bd855ded6c54e`

Trace:
`submit_static_policy_evidence → _submit_durable_candidate → producer_attestation_ref → canonical_hash`
and builder `static_policy_fixture → MappingProxyType(fixture)`,
plus `canonical_hash → canonical_json_bytes → json.dumps`.

Produce exact source-line/type call-chain evidence.

## 5. Reproduce before fix
Using local/non-private fixtures only, prove:
```text
type(static_policy_fixture) == MappingProxyType
canonical_hash(static_policy_fixture) -> TypeError
canonical_hash(dict(static_policy_fixture)) -> deterministic success
```
Use the actual production fixture/config loader where practical and capture exact local TypeError text.

If this does not reproduce the 0009 failure mechanism: `STOP / DIAGNOSIS_INCONCLUSIVE`.

## 6. Minimal correction
If confirmed, correct only the caller boundary. Preferred semantics:
```text
static_policy_value = dict(self._app.static_policy_fixture)
value = static_policy_value
producer_attestation_ref = "server-fixture:" + canonical_hash(static_policy_value)
```
Equivalent minimal implementation is acceptable.

The admitted static-evidence semantic object and the producer-attestation hashed object must be the same plain canonical mapping.

Do not modify generic `canonical_json_bytes` / `canonical_hash`.
Do not add broad MappingProxy serialization support.
Do not swallow arbitrary TypeError into BLOCKED.

## 7. Allowed scope
Product:
`src/aiscc/scenarios/stockroom_production.py`

Existing tracked tests only:
- `tests/unit/scenarios/**`
- `tests/integration/scenarios/test_stockroom_binding.py`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`

New test files forbidden.
`src/aiscc/evidence/models.py` is read-only.

If another product path is required: `STOP / SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED`.

## 8. Targeted verification
Use repository-local Python with `-B`:
- changed-file py_compile
- Ruff changed Python
- exact MappingProxy reproduction before/after
- static policy evidence local admission
- local S3: `READY→RUNNING→BLOCKED`, provider/tool 0, Judgment 0, HumanResult 0
- local S2 regression: `REWORK_REQUIRED + HOLD_REWORK_REQUIRED`
- local S4 regression: `HUMAN_REQUIRED + HumanResult 0 + Judgment 0`
- git diff --check
- external provider/network 0

Use local fake/deterministic boundaries only. No full suite automatically.

## 9. Semantic preservation
Successful candidate must prove:
- S3 `BLOCKED` is the source-owned policy-conflict semantic, not an exception/security-failure substitute.
- S3 provider/tool/Judgment/HumanResult remain 0.
- S2 semantics remain unchanged.
- S4 semantics remain unchanged.

## 10. Git boundary
No commit.
Final tracked dirt only allowed product/test paths.
Move current Task active→done byte-identically.

Governance untracked exactly six:
- 0009 Cycle/Judgment/done Task
- current Cycle/Judgment/done Task

No other product untracked paths. Legacy 1400 remains ignored/non-owned.

## 11. Contract review
Exactly 37 rows:
```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_CLEAN
PREDECESSOR_0009_TRIPLE_EXACT
PREDECESSOR_0009_RESULT_SHA_EXACT
CURRENT_STATE_HASHES_EXACT
LEGACY_1400_ACTIVE_PRESERVED
PYTHON_REPOSITORY_VENV_EXACT
0009_S2_RUNTIME_ACCEPTED
0009_S3_FAILURE_STATE_ACCEPTED
0009_S4_NOT_STARTED_ACCEPTED
NO_PRIVATE_RUNTIME_ACCESS
NO_RETAINED_DB_ACCESS
NO_DOCKER_RUNTIME_EXECUTION
S3_STATIC_FIXTURE_TYPE_IDENTIFIED
S3_CANONICAL_HASH_CALLSITE_IDENTIFIED
GENERIC_CANONICAL_JSON_BASELINE_IDENTIFIED
LOCAL_MAPPINGPROXY_TYPEERROR_REPRODUCED
EXACT_CAUSAL_SERIALIZATION_DEFECT_PROVEN
MINIMAL_STOCKROOM_CALLER_FIX_ONLY
GENERIC_CANONICAL_JSON_UNCHANGED
STATIC_POLICY_VALUE_HASH_INPUT_ALIGNED
STATIC_POLICY_EVIDENCE_LOCAL_ADMISSION_PASS
S3_LOCAL_FINAL_WORKRUN_BLOCKED
S3_LOCAL_PROVIDER_TOOL_EXECUTION_ZERO
S3_LOCAL_JUDGMENT_ZERO
S3_LOCAL_HUMAN_RESULT_ZERO
S4_LOCAL_HUMAN_REQUIRED_REGRESSION_PASS
S4_LOCAL_HUMAN_RESULT_JUDGMENT_ZERO
S2_LOCAL_REWORK_REGRESSION_PASS
NO_EXTERNAL_PROVIDER_NETWORK
NO_CANONICAL_STATE_MUTATION
NO_GIT_COMMIT_PUSH
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
FINAL_CHANGED_PATHS_WITHIN_ALLOWLIST
FINAL_UNTRACKED_GOVERNANCE_EXACT
DIAGNOSIS_REPORT_COMPLETE
EXPORT_INTEGRITY_PASS
```
Success = `37 / 37 PASS`.

## 12. Export
Root docs:
`EXPORT_MANIFEST.md`, `TASK.md`, `EXECUTOR_REPORT.md`, `WORKSPACE_VERIFICATION.md`, `0009_ACCEPTANCE_VERIFICATION.md`, `S3_SERIALIZATION_DIAGNOSIS.md`, `STATIC_POLICY_VALUE_IDENTITY_VERIFICATION.md`, `SOURCE_CHANGE_SUMMARY.md`, `S2_REGRESSION_VERIFICATION.md`, `S3_LOCAL_BLOCKER_VERIFICATION.md`, `S4_REGRESSION_VERIFICATION.md`, `TEST_VERIFICATION.md`, `CONTRACT_REVIEW.md`.

Include current Cycle/Judgment/done Task and every changed product/test path.
Generate manifest/member counts from actual set.
Require one top-level, CRC PASS, exact manifest SHA/size, TASK==done Task, no private values/paths/DB body.

## 13. Success ceiling
```text
S1 ACCEPTED / CLOSED
S2 private REWORK_REQUIRED / accepted
S3 stranded lineage preserved / not reusable
S3 source corrected candidate
S4 private NOT_STARTED
private retry NOT_PERFORMED
Replay NOT_STARTED
P2-3 IN_PROGRESS
```
