# 작업지시서: P2-3 Stockroom evidence-authority v2 prospective cutover rework

## meta

- task_id: `20260913_2202_aiscc-p2-3-stockroom-evidence-authority-v2-prospective-cutover-rework-1`
- created_at: `2026-09-13T22:02:10+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `TARGETED_SOURCE_REWORK / STOCKROOM_EVIDENCE_AUTHORITY_V2_CUTOVER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `15c9e975ec193526eafa0749fc97321c4d89d713`
- required_parent: `c9093e8441de230f9470313d874a33addc75423c`
- required_grandparent: `af5a9f873f11da1fdf71362abde018a2bed313a4`
- reviewed_2120_result_zip_sha256: `f3cdd7cd26455bb2796f3a9580bfe635fd5dc0adf1aa0ec58e3c06e6056a80db`
- private_runtime_access_authorized: `No`
- retained_PostgreSQL_access_authorized: `No`
- Docker_runtime_execution_authorized: `No`
- source_change_authorized: `Yes / narrow Stockroom evidence v2 cutover only`
- targeted_test_authorized: `Yes / local non-private only`
- canonical_state_write_authorized: `No`
- Git_commit_push_authorized: `No`
- success_ceiling: `STOCKROOM_EVIDENCE_V2_CUTOVER_SOURCE_CANDIDATE / BROWSER_REVIEW_PENDING`

# 0. submission-path decision

2120 established:

```text
generic legacy literal-offset fingerprint compatibility
cannot be safely reconstructed from current durable rows alone
```

Do not continue into a generic migration/compatibility subsystem for P2-3.

For the competition submission path, use a prospective versioned cutover:

```text
legacy Stockroom evidence authority v1:
historical / immutable / preserved

new Stockroom evidence authority v2:
fresh authority identities
fresh requirement-set / requirement / checkpoint identities
UTC-stable timestamp literals
fresh S1 and later S2/S3/S4 use v2 only
```

This Task does not fix or relabel legacy v1 historical verification.

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
Git-visible untracked before delivery exactly 12
```

The twelve predecessor artifacts are:

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

Current canonical state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `281bd733624ac87be207f62ed59b99edf0d64cf3b8f3d00e9bc9611fe3179f8c`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `b55eb504c39af0134837f808eef8610b0c54505ee8c597b332f79148ad61d8bd`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `1bb251b5758e8fea1ac260dcace074dcb7e2ff9adf6a96e8699d29c66bea495d`

Persisted provider-fix identities:

- `src/aiscc/scenarios/stockroom_production.py`  `335678daa9fcd4dd9a4b1a2fc4a53876086cab0d555edb7c413466c531dd6d75`
- `tests/integration/scenarios/test_stockroom_binding.py`  `9bd991b77f711a46662262e12f1471b0b78ba1cc6151b3f6a04650ea68bbf439`
- `tests/unit/providers/test_stockroom_tool.py`  `8acda82618b05364e8a7d31ee1b8f6ed28f1bbf5c6a680dda7e8ffc745466544`

Preserve ignored non-owned legacy:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
SHA-256 52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

After current Cycle/Judgment placement while current Task is active/ignored:

```text
Git-visible untracked exactly 14
```

Mismatch → STOP before source mutation.

# 3. hard prohibitions

Do not:

```text
access retained PostgreSQL
read private secret
inspect or mutate any private runtime root
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
commit
push
```

# 4. immutable v1 baseline

Before changes, capture SHA-256 of:

```text
config/evidence/stockroom-capture.v1.json
```

That exact file must remain byte-identical at Task end.

Read the v1 config and derive all durable authority identities used by each enrollment.

At minimum inventory:

```text
authority id/version
scenario id/version
requirement-set id/version/ref
requirement id/version/ref
checkpoint id/version/ref
issued_at
revoked_at if any
```

Do not mutate v1.

# 5. v2 cutover design

Create a new source-owned Stockroom evidence config:

```text
config/evidence/stockroom-capture.v2.json
```

The exact schema should remain compatible with the current loader unless a minimal loader version branch is required.

V2 must satisfy:

```text
1. all timestamp literals used by immutable authority fingerprints are UTC-stable;
2. parse → row serialize → DB-style UTC normalize → row decode → fingerprint recompute is byte-stable;
3. all durable row identities that would conflict with existing v1 rows are versioned/disjoint;
4. scenario semantic meaning remains S1/S2/S3/S4 equivalent to v1;
5. requirement profiles/checkpoint purpose remain semantically equivalent unless a version field must change solely for durable identity separation;
6. no broad evidence policy relaxation.
```

Use explicit `+00:00`-style UTC values if the current parser/`isoformat()` round-trip requires that literal for byte stability.

Do not use `Z` unless the actual parser+`isoformat()` path is proven byte-stable to the intended payload.

# 6. durable identity disjointness

Derive row primary/ref identities using the real source constructors/serializers.

Require v1 and v2 to be disjoint wherever coexistence in the same PostgreSQL would otherwise collide.

At minimum prove disjointness for:

```text
EvidenceRequirementSet
EvidenceRequirement
EvidenceCheckpoint
```

If `authority_id` / `authority_version` participates in immutable ownership but not row primary key, still version it so provenance clearly distinguishes v1 and v2.

Do not merely rename the file while keeping colliding refs.

# 7. production selection

Update the narrow Stockroom production composition so fresh captures load v2.

Preferred scope:

```text
src/aiscc/scenarios/stockroom_production.py
```

The loader/production application must make v2 selection explicit and mechanically testable.

Old v1 remains available as historical source material but must not be the enrollment used by fresh Stockroom capture after this candidate.

Do not add a generic environment flag or user-selectable evidence config.

# 8. no generic P1-6 behavioral patch

This cutover intentionally avoids changing generic P1-6 fingerprint semantics.

Do not modify:

```text
src/aiscc/evidence/requirements.py
src/aiscc/evidence/repository.py
```

unless static inspection proves the v2 cutover cannot work without a tiny generic change.

If such a generic change is required:

```text
STOP / GENERIC_P1_6_CHANGE_REQUIRED
```

Do not make it in this Task.

The generic legacy offset issue remains a known historical limitation, not silently fixed.

# 9. local v2 round-trip proof

Using real source constructors/serializers/decoders and local ORM row objects only, prove for every v2 enrollment:

```text
source sealed RequirementSet fingerprint
==
row-round-tripped RequirementSet recomputation

source sealed Requirement fingerprint
==
row-round-tripped Requirement recomputation

source sealed Checkpoint fingerprint
==
row-round-tripped Checkpoint recomputation
```

Simulate the same timezone normalization PostgreSQL produced:

```text
row datetime → UTC
```

The fingerprints must remain equal because v2 source timestamps are already UTC-stable.

# 10. local historical graph proof

Use the real P1-6 historical resolver with non-private fake/session fixtures constructed from v2 rows.

For every applicable v2 scenario, require:

```text
_historical_authority_graph:
VERIFIED
```

At minimum S1 must pass.

Negative controls:

```text
changed timestamp instant:
DENIED

changed semantic field:
DENIED

wrong requirement/checkpoint ref:
DENIED

wrong root/parent binding:
DENIED

random stored fingerprint:
DENIED
```

No generic hash bypass.

# 11. v1/v2 coexistence proof

Using local row identity/projection fixtures, prove:

```text
v1 identities remain unchanged
v2 identities are distinct
registering/constructing v2 does not overwrite or reseal v1
```

Do not claim old v1 historical graph is repaired.

A report must explicitly state:

```text
v1:
PRESERVED / LEGACY OFFSET-SENSITIVE

v2:
PROSPECTIVE / UTC-STABLE / FRESH-RUN AUTHORITY
```

# 12. downstream P1-7/P1-4 regression

Using v2 local authority only:

```text
evidence set SATISFIED
→ Judgment ACCEPTED
→ P1-7 Human/Judgment participants prepare
→ owner-backed guard facts valid
→ P1-4 ADMISSION_PENDING→ACCEPTED admitted
```

Raw Judgment remains insufficient.

Do not modify P1-4/P1-7 authority semantics.

# 13. Stockroom local fake acceptance

Run a local/non-private Stockroom S1 path using v2 through:

```text
READY
→ RUNNING
→ ADMISSION_PENDING
→ ACCEPTED
```

Require:

```text
provider/tool local deterministic/fake only
external provider/network = 0
v2 evidence authority selected
evidence ADMITTED
Judgment ACCEPTED
required Human/Judgment guards valid
final WorkRun ACCEPTED
```

If current local fake harness cannot exercise the PostgreSQL historical boundary at all, pair it with the real v2 historical-graph fixture from section 10; do not claim the fake alone proves persistence behavior.

# 14. allowed change scope

Allowed product/config paths:

```text
config/evidence/stockroom-capture.v2.json
src/aiscc/scenarios/stockroom_production.py
```

Allowed tests:

```text
tests/unit/evidence/**
tests/unit/scenarios/**
tests/integration/evidence/**
tests/integration/judgment/**
tests/integration/human/**
tests/integration/scenarios/test_stockroom_binding.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Existing `config/evidence/stockroom-capture.v1.json` may be read but must remain byte-identical.

If another product/config path is actually required:

```text
STOP / SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
```

Report exact path/reason without modifying it.

# 15. targeted verification

Use repository-local Python with `-B`.

Minimum:

```text
v1 config SHA before/after exact
v2 JSON parse/schema/loader test
changed-file py_compile
Ruff on changed Python
v2 row round-trip fingerprint tests
v2 historical resolver tests
v1/v2 identity coexistence tests
P1-7/P1-4 downstream regression
Stockroom local fake S1 ACCEPTED regression
git diff --check
```

No full repository suite automatically.

If targeted evidence indicates broad suite is required:

```text
STOP / EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

# 16. private lineage preservation

Do not access retained private runtime/DB.

Use predecessor evidence only:

```text
0036/v1:
historical terminal/quarantined

1822/v2-run:
failed provider-grant lineage

2040/v4:
ADMISSION_PENDING + ACCEPTED Judgment but final transition denied
```

None may be repaired/replayed.

Future private retry must use a new run/attempt/root after Browser accepts and persists this v2 cutover candidate.

# 17. result classification

Success candidate:

```text
v1 config byte-preserved
v2 config created
all durable v2 identities disjoint
all v2 fingerprint timestamps UTC-stable
production fresh capture selects v2
real row round-trip stable
real historical resolver verifies v2
negative integrity cases deny
P1-7/P1-4 downstream local regression PASS
Stockroom local fake S1 ACCEPTED
private runtime retry NOT performed
```

This success does **not** mean:

```text
generic P1-6 legacy timestamp compatibility fixed
old v1 authority migrated
v4 repaired
```

# 18. Git boundary

No commit.

Final tracked dirt must be only allowed v2 product/config/test paths.

Current Task active→done byte-identically.

Git-visible untracked exactly:

```text
2019 triple
2040 triple
2054 triple
2120 triple
current triple
```

Count:

```text
15
```

Legacy 1400 remains ignored/non-owned.

# 19. contract review

Exactly 39 rows:

```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_CLEAN
PREDECESSOR_2019_2040_2054_2120_TRIPLES_EXACT
PREDECESSOR_2120_RESULT_SHA_EXACT
CURRENT_STATE_HASHES_EXACT
PERSISTED_PROVIDER_FIX_HASHES_EXACT
LEGACY_1400_ACTIVE_PRESERVED
PYTHON_REPOSITORY_VENV_EXACT
2120_SCOPE_STOP_ACCEPTED
NO_PRIVATE_RUNTIME_ACCESS
NO_RETAINED_DB_ACCESS
NO_DOCKER_RUNTIME_EXECUTION
V1_CONFIG_BYTE_PRESERVED
V1_AUTHORITY_IDENTITIES_PRESERVED
V2_CONFIG_CREATED
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
FINAL_CHANGED_PATHS_WITHIN_ALLOWLIST
FINAL_UNTRACKED_GOVERNANCE_EXACT
CUTOVER_REPORT_COMPLETE
EXPORT_INTEGRITY_PASS
```

Successful source candidate requires:

```text
39 / 39 PASS
```

Scoped stop must not mark unperformed work PASS.

# 20. export

Root docs:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
2120_ACCEPTANCE_VERIFICATION.md
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

Include:

```text
current Cycle
current Judgment
current done Task
all changed product/config/test paths
```

Do not export unchanged v1 config unless the report records its SHA; it need not be duplicated.

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
