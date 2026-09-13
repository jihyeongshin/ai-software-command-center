# 작업지시서: P2-3 Stockroom evidence-authority v2 cutover untracked-scope corrected retry

## meta

- task_id: `20260913_2225_aiscc-p2-3-stockroom-evidence-authority-v2-cutover-untracked-scope-corrected-retry-1`
- created_at: `2026-09-13T22:25:47+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `TARGETED_SOURCE_REWORK / STOCKROOM_EVIDENCE_AUTHORITY_V2_CUTOVER_RETRY`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `15c9e975ec193526eafa0749fc97321c4d89d713`
- required_parent: `c9093e8441de230f9470313d874a33addc75423c`
- required_grandparent: `af5a9f873f11da1fdf71362abde018a2bed313a4`
- reviewed_2202_result_zip_sha256: `c7994e9703f0bd6cbff15670b0d1950fb28693a4ea45c18089f551613dbf1ca0`
- private_runtime_access_authorized: `No`
- retained_PostgreSQL_access_authorized: `No`
- Docker_runtime_execution_authorized: `No`
- source_change_authorized: `Yes / narrow Stockroom evidence v2 cutover only`
- targeted_test_authorized: `Yes / existing tracked tests only`
- canonical_state_write_authorized: `No`
- Git_commit_push_authorized: `No`
- success_ceiling: `STOCKROOM_EVIDENCE_V2_CUTOVER_SOURCE_CANDIDATE / BROWSER_REVIEW_PENDING`

# 0. Command Center correction

2202 stopped because the previous Task conflated governance untracked files with all repository untracked files.

Corrected semantics:

```text
governance untracked:
exact governance artifact set only

Task-owned product untracked:
tracked separately

total Git-visible untracked:
exact union
```

This Task explicitly authorizes one new product/config untracked path:

```text
config/evidence/stockroom-capture.v2.json
```

No new test files may be created.

Existing tracked tests may be modified.

# 1. executables

Repository:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center
```

Python:

```text
<repository-root>\.venv\Scripts\python.exe
```

Use only this fixed repository-local interpreter.

Forbidden:

```text
python
py
WindowsApps
PATH Python discovery
repository-external Python/venv discovery
```

Git may be used read-only only.

# 2. exact baseline

Require:

```text
branch main
HEAD 15c9e975ec193526eafa0749fc97321c4d89d713
HEAD^ c9093e8441de230f9470313d874a33addc75423c
HEAD^^ af5a9f873f11da1fdf71362abde018a2bed313a4
index empty
tracked clean

Git-visible untracked:
exactly 15 governance paths
```

The fifteen predecessor governance paths are:

- `.aiassistant/records/aiscc/cycles/20260913_2019_aiscc-p2-3-provider-grant-fix-accepted-fresh-s1-v3-retry-entry-1.cycle.md`  `959ac0166ba30510172b2a5a349fab5b622ad7282d67853b8ee8de2830e3561f`
- `.aiassistant/reports/aiscc/20260913_2019_aiscc-p2-3-provider-grant-fix-source-acceptance-and-runtime-retry-authorization-1.md`  `aba7746a9febe65de59fdebc504be9ca889225d3e1e5d181249cdc51ed612d06`
- `.aiassistant/tasks/done/20260913_2019_aiscc-p2-3-provider-grant-fix-persistence-and-fresh-s1-v3-runtime-retry-1.md`  `a7e1d738a03f0a5209f9edd2349d797ef7590afc2b526a9207596c731caeeb87`
- `.aiassistant/records/aiscc/cycles/20260913_2040_aiscc-p2-3-fresh-s1-v4-runtime-retry-entry-1.cycle.md`  `0043e24a5125f12f122e7adcdac14bdca2ed0797a415ebe5ae70ba0fe666de08`
- `.aiassistant/reports/aiscc/20260913_2040_aiscc-p2-3-2019-part-a-accepted-part-b-executor-preflight-retry-judgment-1.md`  `5beb946af3bcf6c1149ac236c797a9492368e19272eb8d1441220ea2c5940c6e`
- `.aiassistant/tasks/done/20260913_2040_aiscc-p2-3-fresh-s1-v4-runtime-retry-after-executor-path-basis-correction-1.md`  `26d530e1500cbcb5347e3ee1ace4e637e71398adf898baaf41340f5d26491cdd`
- `.aiassistant/records/aiscc/cycles/20260913_2054_aiscc-p2-3-s1-final-judgment-guard-handoff-rework-entry-1.cycle.md`  `700d4ee524302a5d69e39a8546e7f308d2c0022edb3340d00b12a1f8ad6cc299`
- `.aiassistant/reports/aiscc/20260913_2054_aiscc-p2-3-s1-v4-final-transition-denied-rework-judgment-1.md`  `64bb57b0cd09d41cd8aa039ffccee846ed32b72bce720b619eff2c16f1c3aa72`
- `.aiassistant/tasks/done/20260913_2054_aiscc-p2-3-s1-final-judgment-guard-handoff-targeted-source-rework-1.md`  `a7122b72247d647039bc50937fa5d9afcc21d98a5359d398a11cc2c9566d0e3b`
- `.aiassistant/records/aiscc/cycles/20260913_2120_aiscc-p2-3-p1-6-timestamp-authority-compatibility-rework-entry-1.cycle.md`  `4a2a92d1691bf7ae204f690a9c6aaa9ebedba11752f4441a48cda0fc91886489`
- `.aiassistant/reports/aiscc/20260913_2120_aiscc-p2-3-2054-scope-expansion-p1-6-authority-rework-judgment-1.md`  `bad8095470e5412d3ae40be8d7378bf359981ddad340f2a04c28d16b03083530`
- `.aiassistant/tasks/done/20260913_2120_aiscc-p2-3-p1-6-evidence-authority-timestamp-canonicalization-compatibility-rework-1.md`  `6d478d01df64255a4dceac205e88e34392c3fc4fa0d74813b102521b7cc99b45`
- `.aiassistant/records/aiscc/cycles/20260913_2202_aiscc-p2-3-stockroom-evidence-authority-v2-cutover-entry-1.cycle.md`  `0b5fb2754bfa0ee6eaf192e5565fee2ac2016aa4b661b2b4570ae22fe4e6bda5`
- `.aiassistant/reports/aiscc/20260913_2202_aiscc-p2-3-2120-legacy-compatibility-stop-v2-cutover-judgment-1.md`  `eaf785ee5bc3b780f22800fbb227e32e120c3756f57a5f742c1161aad61e2bfe`
- `.aiassistant/tasks/done/20260913_2202_aiscc-p2-3-stockroom-evidence-authority-v2-prospective-cutover-rework-1.md`  `bdf547850d02f4724766fb15aee173418a8a4c633b4f01a46afdeaf1352833fc`

There must be no other Git-visible untracked path before current delivery.

Current canonical state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `281bd733624ac87be207f62ed59b99edf0d64cf3b8f3d00e9bc9611fe3179f8c`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `b55eb504c39af0134837f808eef8610b0c54505ee8c597b332f79148ad61d8bd`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `1bb251b5758e8fea1ac260dcace074dcb7e2ff9adf6a96e8699d29c66bea495d`

Persisted provider-fix identities:

- `src/aiscc/scenarios/stockroom_production.py`  `335678daa9fcd4dd9a4b1a2fc4a53876086cab0d555edb7c413466c531dd6d75`
- `tests/integration/scenarios/test_stockroom_binding.py`  `9bd991b77f711a46662262e12f1471b0b78ba1cc6151b3f6a04650ea68bbf439`
- `tests/unit/providers/test_stockroom_tool.py`  `8acda82618b05364e8a7d31ee1b8f6ed28f1bbf5c6a680dda7e8ffc745466544`

V1 config:

```text
config/evidence/stockroom-capture.v1.json
SHA-256 70d4dbf219d54abd57877b787d8ac16d0efbe05701e7fb8bf1f84282640b31e7
```

Preserve ignored non-owned legacy:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
SHA-256 52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

After current Cycle/Judgment placement while current Task remains active/ignored:

```text
governance Git-visible untracked:
exactly 17

product Git-visible untracked:
0

total Git-visible untracked:
17
```

Mismatch → STOP before product mutation.

# 3. hard prohibitions

Do not:

```text
access retained PostgreSQL
read private secret
inspect or mutate private runtime roots
run Docker
replay/repair v4
modify generic historical rows
modify existing durable DB values
add a DB migration
relax P1-6 historical fingerprint equality
guess old timezone offsets
enumerate offsets until a legacy hash matches
change old v1 authority IDs/versions/fingerprints
modify canonical state
create any new test file
git add
git commit
git push
```

# 4. immutable v1 baseline

Require v1 config SHA exactly:

```text
70d4dbf219d54abd57877b787d8ac16d0efbe05701e7fb8bf1f84282640b31e7
```

Capture all v1 durable authority identities using the real source loader/constructors/serializers.

At minimum:

```text
authority id/version
scenario id/version
requirement-set id/version/ref
requirement id/version/ref
checkpoint id/version/ref
issued_at
revoked_at if any
```

V1 must remain byte-identical at Task end.

# 5. v2 prospective cutover

Create exactly one new product/config file:

```text
config/evidence/stockroom-capture.v2.json
```

This exact path is authorized to remain Git-visible untracked.

No other new product/config/test file is authorized.

V2 must provide:

```text
fresh authority identities
fresh RequirementSet identities
fresh Requirement identities
fresh Checkpoint identities
UTC-stable timestamp literals
same S1/S2/S3/S4 semantic meaning as v1
```

Use explicit UTC representations that survive parser → `isoformat()` → DB-style UTC normalization byte-stably.

# 6. durable identity disjointness

Using real source constructors/serializers, prove v1/v2 coexistence without collisions.

Require disjointness for:

```text
authority id/version
EvidenceRequirementSet row/ref identity
EvidenceRequirement row/ref identity
EvidenceCheckpoint row/ref identity
```

A renamed config with colliding durable refs is FAIL.

# 7. production selection

Modify only the narrow Stockroom production composition necessary so fresh captures select v2 explicitly.

Preferred product path:

```text
src/aiscc/scenarios/stockroom_production.py
```

No generic runtime flag or user-selectable evidence config.

Fresh capture after this candidate must select v2 only.

# 8. generic P1-6 remains unchanged

Do not modify:

```text
src/aiscc/evidence/requirements.py
src/aiscc/evidence/repository.py
```

If v2 cannot work without generic P1-6 source modification:

```text
STOP / GENERIC_P1_6_CHANGE_REQUIRED
```

Do not implement it here.

Legacy v1 offset sensitivity remains a known historical limitation.

# 9. v2 row round-trip

For every v2 enrollment, use real constructors/serializers/decoders and local ORM row objects.

Simulate DB timezone normalization.

Require sealed fingerprint equality after round-trip for:

```text
EvidenceRequirementSet
EvidenceRequirement
EvidenceCheckpoint
```

# 10. v2 historical authority graph

Use the real historical resolver with local/non-private fixtures.

At minimum S1 must verify.

Negative controls must deny:

```text
changed timestamp instant
changed semantic field
wrong requirement/checkpoint ref
wrong root/parent binding
random stored fingerprint
```

# 11. v1/v2 coexistence

Prove locally:

```text
v1 config bytes unchanged
v1 identities unchanged
v2 identities distinct
v2 construction does not overwrite/reseal v1
```

Report:

```text
v1:
PRESERVED / LEGACY OFFSET-SENSITIVE

v2:
PROSPECTIVE / UTC-STABLE / FRESH-RUN AUTHORITY
```

Do not claim v1 historical verification was fixed.

# 12. downstream P1-7/P1-4

Using v2 local authority:

```text
evidence set SATISFIED
→ Judgment ACCEPTED
→ P1-7 participant preparation
→ owner-backed Human/Judgment guard facts
→ P1-4 ADMISSION_PENDING→ACCEPTED
```

Raw Judgment alone remains insufficient.

# 13. Stockroom local fake S1

Use only local/non-private fake/deterministic boundaries.

Require:

```text
READY
→ RUNNING
→ ADMISSION_PENDING
→ ACCEPTED

v2 evidence authority selected
evidence ADMITTED
Judgment ACCEPTED
Human/Judgment guards valid
final WorkRun ACCEPTED
external provider/network 0
```

# 14. allowed tracked modifications

Product/config:

```text
src/aiscc/scenarios/stockroom_production.py
```

New untracked product/config:

```text
config/evidence/stockroom-capture.v2.json
```

Existing tracked test files may be modified only within:

```text
tests/unit/evidence/**
tests/unit/scenarios/**
tests/integration/evidence/**
tests/integration/judgment/**
tests/integration/human/**
tests/integration/scenarios/test_stockroom_binding.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Important:

```text
new test files:
FORBIDDEN
```

If a required proof cannot be added without a new test file, modify an existing tracked test within the allowed scope.

If another product/config path is required:

```text
STOP / SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
```

# 15. targeted verification

Use repository-local Python with `-B`.

Minimum:

```text
v1 SHA before/after exact
v2 JSON parse/schema/loader
changed-file py_compile
Ruff changed Python
v2 row round-trip fingerprint tests
v2 historical resolver tests
v1/v2 coexistence tests
P1-7/P1-4 downstream regression
Stockroom local fake S1 ACCEPTED regression
git diff --check
```

No full repository suite automatically.

# 16. private lineage preservation

No retained private runtime/DB access.

Use predecessor evidence only:

```text
0036/v1:
historical terminal/quarantined

1822/v2-run:
failed provider-grant lineage

2040/v4:
ADMISSION_PENDING + ACCEPTED Judgment + final transition denied
```

No repair/replay.

# 17. result classification

Successful candidate:

```text
v1 byte-preserved
v2 config created
v1/v2 durable identities disjoint
v2 timestamps UTC-stable
production fresh capture selects v2
round-trip fingerprints stable
historical resolver v2 PASS
negative integrity cases DENY
P1-7/P1-4 downstream PASS
Stockroom local fake S1 ACCEPTED
private runtime retry NOT performed
```

Does not mean:

```text
generic legacy timestamp defect fixed
v1 migrated
v4 repaired
```

# 18. Git terminal boundary — corrected

No Git index mutation and no commit.

Move current Task active→done byte-identically.

At final:

## governance Git-visible untracked

Exactly 18 governance paths:

```text
five predecessor triples:
15

current Cycle/Judgment/done Task:
3
```

No other governance untracked path.

## Task-owned product Git-visible untracked

Exactly one:

```text
config/evidence/stockroom-capture.v2.json
```

## total Git-visible untracked

Exactly:

```text
19
```

The total is the union of the exact 18 governance paths and the exact one v2 config path.

Tracked worktree dirt may contain only existing tracked files modified within section 14.

Index must remain empty.

Legacy 1400 remains ignored/non-owned.

# 19. contract review

Exactly 45 rows:

```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_CLEAN
PREDECESSOR_2019_2040_2054_2120_2202_TRIPLES_EXACT
PREDECESSOR_2202_RESULT_SHA_EXACT
CURRENT_STATE_HASHES_EXACT
PERSISTED_PROVIDER_FIX_HASHES_EXACT
LEGACY_1400_ACTIVE_PRESERVED
PYTHON_REPOSITORY_VENV_EXACT
2202_CONTRACT_CONFLICT_ACCEPTED
PRE_DELIVERY_GOVERNANCE_UNTRACKED_15_EXACT
POST_TRANSPORT_GOVERNANCE_UNTRACKED_17_EXACT
NO_PRIVATE_RUNTIME_ACCESS
NO_RETAINED_DB_ACCESS
NO_DOCKER_RUNTIME_EXECUTION
V1_CONFIG_BYTE_PRESERVED
V1_AUTHORITY_IDENTITIES_PRESERVED
V2_CONFIG_CREATED
V2_CONFIG_ONLY_PRODUCT_UNTRACKED
NO_NEW_TEST_FILES_CREATED
V2_AUTHORITY_IDENTITY_DISJOINT
V2_REQUIREMENT_SET_IDENTITY_DISJOINT
V2_REQUIREMENT_IDENTITY_DISJOINT
V2_CHECKPOINT_IDENTITY_DISJOINT
V2_TIMESTAMPS_UTC_STABLE
V2_LOADER_SELECTED_BY_PRODUCTION
V2_ROW_ROUNDTRIP_FINGERPRINT_STABLE
V2_HISTORICAL_AUTHORITY_GRAPH_PASS
V1_AND_V2_COEXISTENCE_NO_OVERWRITE_PASS
V1_LEGACY_FAILURE_NOT_RELABELED_FIXED
NO_GENERIC_P1_6_HASH_BYPASS
NO_DB_MIGRATION_OR_REPAIR
TARGETED_V2_LOADER_TESTS_PASS
TARGETED_V2_EVIDENCE_AUTHORITY_TESTS_PASS
TARGETED_P1_7_GUARD_INTEGRATION_PASS
TARGETED_STOCKROOM_S1_FAKE_ACCEPTED
NO_EXTERNAL_PROVIDER_NETWORK
NO_CANONICAL_STATE_MUTATION
NO_GIT_COMMIT_PUSH
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
FINAL_CHANGED_TRACKED_PATHS_WITHIN_ALLOWLIST
FINAL_GOVERNANCE_UNTRACKED_18_EXACT
FINAL_PRODUCT_UNTRACKED_V2_CONFIG_EXACT
FINAL_TOTAL_UNTRACKED_19_EXACT
CUTOVER_REPORT_COMPLETE
EXPORT_INTEGRITY_PASS
```

Successful source candidate:

```text
45 / 45 PASS
```

Scoped stop must not mark unperformed rows PASS.

# 20. export

Root docs:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
2202_ACCEPTANCE_VERIFICATION.md
V1_AUTHORITY_BASELINE.md
V2_CUTOVER_DESIGN_VERIFICATION.md
V2_IDENTITY_DISJOINTNESS.md
V2_ROUNDTRIP_VERIFICATION.md
V2_HISTORICAL_RESOLVER_VERIFICATION.md
V1_V2_COEXISTENCE_VERIFICATION.md
DOWNSTREAM_GUARD_REGRESSION_VERIFICATION.md
SOURCE_CHANGE_SUMMARY.md
TEST_VERIFICATION.md
CONTRACT_REVIEW.md
```

Include project-relative copies of:

```text
current Cycle
current Judgment
current done Task
config/evidence/stockroom-capture.v2.json
every modified existing tracked product/test path
```

Generate manifest/member count from actual declared set.

Require:

```text
one top-level
CRC PASS
manifest SHA/size exact
TASK.md == canonical done Task
no private path/value/DB body
```

# 21. success ceiling

```text
2202:
accepted Command Center contract defect / no product mutation

legacy v1 evidence authority:
PRESERVED / KNOWN OFFSET-SENSITIVE

Stockroom evidence authority v2:
SOURCE CANDIDATE READY

generic P1-6 migration:
DEFERRED

private S1 retry:
NOT_PERFORMED

P2-3:
IN_PROGRESS
```
