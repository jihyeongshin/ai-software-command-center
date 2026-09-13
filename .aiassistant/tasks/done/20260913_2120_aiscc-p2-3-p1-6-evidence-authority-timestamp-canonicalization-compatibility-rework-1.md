# 작업지시서: P2-3 P1-6 evidence-authority timestamp canonicalization and legacy compatibility rework

## meta

- task_id: `20260913_2120_aiscc-p2-3-p1-6-evidence-authority-timestamp-canonicalization-compatibility-rework-1`
- created_at: `2026-09-13T21:20:03+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `TARGETED_SOURCE_REWORK / P1_6_EVIDENCE_AUTHORITY_TIMESTAMP`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `15c9e975ec193526eafa0749fc97321c4d89d713`
- required_parent: `c9093e8441de230f9470313d874a33addc75423c`
- required_grandparent: `af5a9f873f11da1fdf71362abde018a2bed313a4`
- reviewed_2054_result_zip_sha256: `cd2cb22994fed6cdf7621eae2dad6dce74c0473ab1d12c76ed40e73d36d83898`
- private_runtime_access_authorized: `No`
- retained_PostgreSQL_access_authorized: `No`
- Docker_runtime_execution_authorized: `No`
- source_change_authorized: `Conditional / P1-6 timestamp authority defect only`
- targeted_test_authorized: `Yes / local non-private only`
- canonical_state_write_authorized: `No`
- Git_commit_push_authorized: `No`
- success_ceiling: `P1_6_TIMESTAMP_COMPATIBILITY_SOURCE_CANDIDATE / BROWSER_REVIEW_PENDING`

# 0. accepted diagnosis

2054 is accepted as a correct scoped stop.

Mechanically reproduced source fact:

```text
source checkpoint issued_at:
2026-09-10T18:24:00+09:00

DB-decoded equivalent:
2026-09-10T09:24:00+00:00

same instant:
true

literal isoformat fingerprints:
different
```

Observed local error:

```text
HistoricalEvidenceProvenanceError:
historical evidence checkpoint immutable authority disagrees
```

This error occurs during P1-7 Judgment participant preparation through the P1-6 historical authority graph, before P1-4 final transition evaluation.

Do not modify or replay v4 in this Task.

# 1. executable rule

Repository:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center
```

Python:

```text
<repository-root>\.venv\Scripts\python.exe
```

Use this fixed repository-local executable only.

Forbidden:

```text
python
py
WindowsApps
PATH Python discovery
repository-external Python/venv discovery
```

Git may be used read-only only.

# 2. repository baseline

Require:

```text
branch main
HEAD 15c9e975ec193526eafa0749fc97321c4d89d713
HEAD^ c9093e8441de230f9470313d874a33addc75423c
HEAD^^ af5a9f873f11da1fdf71362abde018a2bed313a4
index empty
tracked clean
Git-visible untracked before delivery exactly 9
```

The nine predecessor artifacts are:

- `.aiassistant/records/aiscc/cycles/20260913_2019_aiscc-p2-3-provider-grant-fix-accepted-fresh-s1-v3-retry-entry-1.cycle.md`  `959ac0166ba30510172b2a5a349fab5b622ad7282d67853b8ee8de2830e3561f`
- `.aiassistant/reports/aiscc/20260913_2019_aiscc-p2-3-provider-grant-fix-source-acceptance-and-runtime-retry-authorization-1.md`  `aba7746a9febe65de59fdebc504be9ca889225d3e1e5d181249cdc51ed612d06`
- `.aiassistant/tasks/done/20260913_2019_aiscc-p2-3-provider-grant-fix-persistence-and-fresh-s1-v3-runtime-retry-1.md`  `a7e1d738a03f0a5209f9edd2349d797ef7590afc2b526a9207596c731caeeb87`
- `.aiassistant/records/aiscc/cycles/20260913_2040_aiscc-p2-3-fresh-s1-v4-runtime-retry-entry-1.cycle.md`  `0043e24a5125f12f122e7adcdac14bdca2ed0797a415ebe5ae70ba0fe666de08`
- `.aiassistant/reports/aiscc/20260913_2040_aiscc-p2-3-2019-part-a-accepted-part-b-executor-preflight-retry-judgment-1.md`  `5beb946af3bcf6c1149ac236c797a9492368e19272eb8d1441220ea2c5940c6e`
- `.aiassistant/tasks/done/20260913_2040_aiscc-p2-3-fresh-s1-v4-runtime-retry-after-executor-path-basis-correction-1.md`  `26d530e1500cbcb5347e3ee1ace4e637e71398adf898baaf41340f5d26491cdd`
- `.aiassistant/records/aiscc/cycles/20260913_2054_aiscc-p2-3-s1-final-judgment-guard-handoff-rework-entry-1.cycle.md`  `700d4ee524302a5d69e39a8546e7f308d2c0022edb3340d00b12a1f8ad6cc299`
- `.aiassistant/reports/aiscc/20260913_2054_aiscc-p2-3-s1-v4-final-transition-denied-rework-judgment-1.md`  `64bb57b0cd09d41cd8aa039ffccee846ed32b72bce720b619eff2c16f1c3aa72`
- `.aiassistant/tasks/done/20260913_2054_aiscc-p2-3-s1-final-judgment-guard-handoff-targeted-source-rework-1.md`  `a7122b72247d647039bc50937fa5d9afcc21d98a5359d398a11cc2c9566d0e3b`

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

After current Cycle/Judgment placement with current Task active/ignored:

```text
Git-visible untracked exactly 11
```

Mismatch → STOP before source mutation.

# 3. hard prohibitions

Do not:

```text
access retained PostgreSQL
read private secret
inspect/mutate private runtime roots
run Docker
replay/repair v4
manually transition any retained WorkRun
modify v4 Judgment/guard/evidence rows
weaken P1-6 historical provenance checks
accept arbitrary fingerprint mismatches
rewrite existing authority IDs
silently reseal existing authority under same identity
modify canonical state
commit
push
```

# 4. exact P1-6 diagnosis scope

Inspect all timestamp-bearing fields that participate in immutable P1-6 authority fingerprints for:

```text
EvidenceCheckpoint
EvidenceRequirement
EvidenceRequirementSet
```

At minimum inspect:

```text
src/aiscc/evidence/requirements.py
- _checkpoint_payload
- requirement payload/fingerprint helpers
- requirement-set payload/root helpers
- canonical_hash/fingerprint inputs used by these objects

src/aiscc/evidence/repository.py
- row serialization
- _aware or timestamp decoding normalization
- _checkpoint_from_row
- requirement/set row decoders
- _historical_authority_graph
- register_authority / historical resolver compatibility paths
```

Produce a table:

```text
authority kind
timestamp field
creation representation
DB round-trip representation
fingerprint producer
historical recomputation
offset-sensitive?
compatibility requirement
```

Do not assume only checkpoint is affected; prove the requirement and requirement-set status.

# 5. canonical timestamp semantics

A new canonical timestamp representation used in immutable fingerprint payloads must satisfy:

```text
aware datetime required
same instant across offsets → identical canonical bytes
different instant → different canonical bytes
deterministic across restart/platform
no locale dependence
```

Preferred semantic shape:

```text
UTC-normalized instant
```

The exact textual encoding is source-owner choice, but it must be one deterministic representation.

Do not alter business/event timestamps themselves merely for presentation. This Task concerns immutable fingerprint serialization/verification semantics.

# 6. legacy sealed-authority compatibility

Existing authority rows/fingerprints were created before canonicalization.

The fix must preserve existing legitimate sealed authority without creating a generic hash bypass.

A permitted compatibility design must satisfy all:

```text
1. compatibility applies only to an explicitly identified legacy fingerprint schema/path;
2. semantic non-time fields must match exactly;
3. decoded timestamp instant must equal the trusted authority instant exactly;
4. stored legacy fingerprint must itself be validated against a trusted legacy-authority representation;
5. altered instant must fail;
6. non-time field change must fail;
7. random fingerprint mismatch must fail;
8. compatibility cannot mint a new authority ID or silently overwrite a durable fingerprint;
9. compatibility is read/verification semantics, not DB repair.
```

If the existing source does not retain enough trusted information to validate a legacy fingerprint without guessing the lost original offset, STOP with:

```text
LEGACY_FINGERPRINT_COMPATIBILITY_REQUIRES_EXPLICIT_SCHEMA_OR_MIGRATION
```

Do not implement a permissive fallback.

# 7. allowed source scope

Conditional source changes are allowed only in:

```text
src/aiscc/evidence/requirements.py
src/aiscc/evidence/repository.py
```

Related tests may be changed/added only under:

```text
tests/unit/evidence/**
tests/integration/evidence/**
tests/integration/judgment/**
tests/integration/human/**
tests/integration/scenarios/test_stockroom_binding.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

If the correct bounded solution requires persistence schema/model/migration or another product path outside this allowlist, STOP with:

```text
SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
```

and name the exact required path and semantic reason.

Do not broaden scope implicitly.

# 8. pre-fix reproduction

Before source correction, reproduce locally/non-privately:

```text
same source checkpoint instant:
+09:00 representation

row-decoded representation:
+00:00

legacy stored fingerprint:
matches source creation form

historical recomputation:
fails on current source
```

Also determine whether equivalent failures are possible for Requirement and RequirementSet.

No PostgreSQL connection is required; DTO/ORM row fixtures are acceptable when they execute the real serialization/decoder/resolver functions.

# 9. required correction behavior

After correction, local evidence must prove:

## new canonical authority

```text
+09:00 instant
==
UTC equivalent instant
for fingerprint bytes
```

for every affected authority kind.

## legacy compatibility

The exact existing S1 legacy checkpoint fixture must verify successfully without changing its stored fingerprint or ID.

If Requirement/RequirementSet were offset-sensitive and legacy instances exist, equivalent compatibility proof is also required.

## negative cases

```text
timestamp +1 second:
DENIED

different semantic field:
DENIED

different requirement/checkpoint identity:
DENIED

random stored fingerprint:
DENIED

wrong parent/root binding:
DENIED
```

# 10. P1-7 / P1-4 regression objective

After P1-6 compatibility succeeds, use only local/non-private fixtures to prove the original downstream handoff:

```text
evidence set SATISFIED
→ Judgment ACCEPTED
→ P1-7 Human/Judgment participants prepare successfully
→ owner-backed guard facts valid
→ P1-4 ADMISSION_PENDING→ACCEPTED admitted
```

A raw Judgment row remains insufficient.

No P1-4 or P1-7 source weakening is authorized.

# 11. Stockroom local fake regression

Run a local/non-private Stockroom S1 path through:

```text
READY
→ RUNNING
→ ADMISSION_PENDING
→ ACCEPTED
```

Require:

```text
provider/tool path uses local deterministic/fake only
external provider/network = 0
Judgment ACCEPTED
required Human/Judgment guard facts present
final WorkRun ACCEPTED
```

Do not use retained private PostgreSQL/runtime.

If existing local fixture requires PostgreSQL and no authorized non-private test DB is already available in the test harness, use supported in-memory/fake boundaries where possible. Do not create/access the retained private DB.

# 12. targeted verification

Use repository-local Python with `-B`.

Minimum:

```text
changed-file py_compile
Ruff on changed Python
P1-6 timestamp/fingerprint unit tests
P1-6 historical resolver compatibility tests
P1-7 Judgment guard integration regression
Stockroom local fake S1 acceptance regression
git diff --check
```

Do not run a full repository suite automatically.

If targeted failures prove broader evidence is needed:

```text
STOP / EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

# 13. 2040/v4 preservation

Do not access retained runtime/DB.

Use only accepted predecessor evidence:

```text
v4 WorkRun:
ADMISSION_PENDING/v3

v4 attempt:
EXECUTOR_COMPLETED/v8

S1 evidence:
ADMITTED

evidence-set:
SATISFIED

Judgment:
ACCEPTED

Human/Judgment guard rows:
0 / 0

final transition:
not admitted
```

No replay, repair or direct completion.

# 14. result classification

Successful source candidate requires:

```text
exact affected timestamp payloads identified
canonical instant encoding implemented
legacy verification explicitly bounded
same-instant offset equivalence PASS
altered-instant rejection PASS
random mismatch rejection PASS
historical resolver PASS
P1-7/P1-4 downstream regression PASS
Stockroom local fake S1 ACCEPTED
private runtime retry NOT performed
```

If compatibility cannot be made safe within allowed paths:

```text
STOP / SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
```

# 15. Git boundary

No commit.

Final tracked dirt must contain only allowed P1-6 source/tests.

Current Task active→done byte-identically.

Git-visible untracked exactly:

```text
2019 triple
2040 triple
2054 triple
current triple
```

Count:

```text
12
```

Legacy 1400 remains ignored/non-owned.

# 16. contract review

Exactly 37 rows:

```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_CLEAN
PREDECESSOR_2019_2040_2054_TRIPLES_EXACT
PREDECESSOR_2054_RESULT_SHA_EXACT
CURRENT_STATE_HASHES_EXACT
PERSISTED_PROVIDER_FIX_HASHES_EXACT
LEGACY_1400_ACTIVE_PRESERVED
PYTHON_REPOSITORY_VENV_EXACT
2054_DIAGNOSIS_ACCEPTED
NO_PRIVATE_RUNTIME_ACCESS
NO_RETAINED_DB_ACCESS
NO_DOCKER_RUNTIME_EXECUTION
P1_6_TIMESTAMP_PAYLOAD_SCOPE_IDENTIFIED
CHECKPOINT_TIMESTAMP_ROUNDTRIP_REPRODUCED
REQUIREMENT_TIMESTAMP_SCOPE_AUDITED
REQUIREMENT_SET_TIMESTAMP_SCOPE_AUDITED
CANONICAL_INSTANT_ENCODING_DEFINED
SAME_INSTANT_OFFSET_EQUIVALENCE_PASS
ALTERED_INSTANT_REJECTION_PASS
LEGACY_FINGERPRINT_COMPATIBILITY_BOUNDED
ARBITRARY_HASH_MISMATCH_STILL_DENIED
NON_TIME_FIELD_MISMATCH_STILL_DENIED
NO_AUTHORITY_ID_REWRITE
NO_DB_DATA_REPAIR_OR_MIGRATION
MINIMAL_P1_6_CHANGE_ONLY
TARGETED_P1_6_UNIT_TESTS_PASS
TARGETED_P1_6_HISTORICAL_RESOLVER_PASS
TARGETED_P1_7_JUDGMENT_GUARD_INTEGRATION_PASS
TARGETED_STOCKROOM_S1_FAKE_ACCEPTED
NO_EXTERNAL_PROVIDER_NETWORK
NO_CANONICAL_STATE_MUTATION
NO_GIT_COMMIT_PUSH
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
FINAL_CHANGED_PATHS_WITHIN_ALLOWLIST
FINAL_UNTRACKED_GOVERNANCE_EXACT
DIAGNOSIS_AND_COMPATIBILITY_REPORT_COMPLETE
EXPORT_INTEGRITY_PASS
```

Successful candidate:

```text
37 / 37 PASS
```

Blocked result must leave unperformed rows non-PASS.

# 17. export

Root docs:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
2054_ACCEPTANCE_VERIFICATION.md
P1_6_TIMESTAMP_SCOPE_AUDIT.md
TIMESTAMP_CANONICALIZATION_VERIFICATION.md
LEGACY_FINGERPRINT_COMPATIBILITY_VERIFICATION.md
HISTORICAL_RESOLVER_VERIFICATION.md
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
all changed product/test paths
```

Generate manifest/member counts from actual declared set.

Require:

```text
one top-level
CRC PASS
manifest SHA/size exact
TASK.md == canonical done Task
no private path/value/DB body
```

# 18. success ceiling

```text
2040 v4:
preserved / REWORK_REQUIRED

P1-6 timestamp authority:
SOURCE CANDIDATE CORRECTED

P1-7/P1-4 downstream:
local regression PASS

private S1 retry:
NOT_PERFORMED

P2-3:
IN_PROGRESS
```
