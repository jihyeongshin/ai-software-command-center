# 작업지시서: P2-3 fresh S1 provider resource-grant denial targeted source rework

## meta

- task_id: `20260913_1851_aiscc-p2-3-fresh-s1-provider-resource-grant-denial-targeted-source-rework-1`
- created_at: `2026-09-13T18:51:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `TARGETED_SOURCE_REWORK / S1_SECURITY_GRANT_BINDING`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `c9093e8441de230f9470313d874a33addc75423c`
- required_parent: `af5a9f873f11da1fdf71362abde018a2bed313a4`
- required_grandparent: `d04f6a322f3a3ea49778314e4005b5878b20f121`
- reviewed_1822_result_zip_sha256: `a5cc2c840664f5f2e184082768839048170a178afc077f4acf19d45eddceefcd`
- private_runtime_access_authorized: `No`
- retained_PostgreSQL_access_authorized: `No`
- Docker_runtime_execution_authorized: `No`
- source_change_authorized: `Conditional / exact causal mismatch only`
- test_execution_authorized: `Yes / targeted local only`
- Git_commit_push_authorized: `No`
- success_ceiling: `SOURCE_REWORK_CANDIDATE / BROWSER_REVIEW_PENDING`

# 0. accepted failure

Browser accepts the 1822 executor evidence as an actual fail-closed runtime defect:

```text
fresh run:
aiscc-p2-3-private-s1-normal-v2-run

fresh attempt:
aiscc-p2-3-private-s1-normal-v2-attempt-1

WorkRun:
RUNNING/v2

attempt:
EXECUTION_FAILED/v3

failure class:
SECURITY_DENIAL

reason:
P1_3_SECURITY_DENIED:PROVIDER:EXACT_RESOURCE_GRANT_DENIED

provider operation:
DENIED_BEFORE_SIDE_EFFECT

provider invocation:
0

tool dispatch:
0

runtime evidence/Judgment:
0
```

Do not retry that run or attempt.

# 1. executable rule

Repository:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center
```

Python:

```text
<repository-root>\.venv\Scripts\python.exe
```

Only this fixed repository-local interpreter may be used.

Forbidden:

```text
python
py
WindowsApps
PATH Python discovery
repository-external Python
```

# 2. repository baseline

Require:

```text
branch main
HEAD c9093e8441de230f9470313d874a33addc75423c
HEAD^ af5a9f873f11da1fdf71362abde018a2bed313a4
HEAD^^ d04f6a322f3a3ea49778314e4005b5878b20f121
index empty
tracked clean
Git-visible untracked before delivery exactly 3
```

Those three are the 1822 predecessor artifacts:

```text
.aiassistant/records/aiscc/cycles/20260913_1822_aiscc-p2-3-fresh-s1-normal-production-path-entry-1.cycle.md
700c3aef2a050c2850d72e65acf3936d0c1af2cfd702b89d4c1638e02c13b466

.aiassistant/reports/aiscc/20260913_1822_aiscc-p2-3-invalid-history-persistence-accepted-fresh-s1-authorization-judgment-1.md
f2e6f62074716ddabe97039d76b91ed73e7d4fed5c80c9094fc846807d8d34d7

.aiassistant/tasks/done/20260913_1822_aiscc-p2-3-fresh-s1-normal-production-path-execution-with-v2-runtime-root-1.md
9f4a740b684137752d868c02f5dc8c63a25c1cfa45925f994c15fec4ddd7afd0
```

Current state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `281bd733624ac87be207f62ed59b99edf0d64cf3b8f3d00e9bc9611fe3179f8c`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `b55eb504c39af0134837f808eef8610b0c54505ee8c597b332f79148ad61d8bd`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `1bb251b5758e8fea1ac260dcace074dcb7e2ff9adf6a96e8699d29c66bea495d`

Preserve ignored non-owned legacy:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

After current Cycle/Judgment placement:

```text
Git-visible untracked exactly 5
```

# 3. hard prohibitions

Do not:

```text
access retained PostgreSQL
read private secret
inspect or modify v1/v2 private runtime roots
run Stockroom Docker execution
invoke build_stockroom_production against retained resources
invoke prepare_capture against retained resources
run the 1822 fresh lineage again
create another WorkRun/attempt
manually repair DB state
relax P1-3 fail-closed semantics
change exact-match security rule into wildcard/prefix/contains matching
grant broad PROVIDER access
enable external provider/network
modify canonical state files
commit or push
```

# 4. diagnosis scope

Read the current source/config path from S1 preparation through the first provider security admission.

At minimum trace:

```text
StockroomCaptureRunner.run
StockroomCaptureOwnerAdapter / production composition
AgentExecutionService provider operation preparation
P1-5 provider selector attestation
P1-3 PermissionRequest
ResourceGrant issuance/construction
SecurityAdmissionDecision exact-resource comparison
server-owned ProviderProfile resource identity
```

Produce a table:

```text
semantic field
request actual
grant actual
profile/config owner
expected relation
mismatch yes/no
source location
```

The diagnosis must identify the exact differing resource identity field(s), not merely repeat `EXACT_RESOURCE_GRANT_DENIED`.

# 5. accepted invariant

Preserve:

```text
P1-5 selector authority != P1-3 ResourceGrant
PROVIDER capability != TOOL capability
PROVIDER capability != SECRET capability
Agent/provider input cannot mint or widen grants
exact resource identity matching remains fail-closed
```

The fix must make the authorized production S1 resource representations agree; it must not weaken the evaluator.

# 6. conditional implementation rule

Only if section 4 proves **one unambiguous causal production binding mismatch**, implement the smallest correction.

Allowed product/config modification scope:

```text
src/aiscc/scenarios/stockroom_production.py
src/aiscc/scenarios/composition.py
src/aiscc/providers/service.py
src/aiscc/providers/local_deterministic.py
src/aiscc/providers/stockroom_tool.py
config/providers/stockroom-owner-profiles.v2.toml
config/providers/stockroom-tools.v2.toml
```

Allowed tests:

```text
tests/unit/providers/**
tests/unit/scenarios/**
tests/integration/scenarios/test_stockroom_binding.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Do not edit all allowed paths mechanically. Change only the causal owner plus minimum regression tests.

If the causal owner lies outside this allowlist, STOP with:

```text
SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
```

and report the exact required path/reason. Do not modify that outside path.

# 7. correction quality

The correction must demonstrate all:

```text
normal OWNER S1 provider resource request
==
exact server-owned provider ResourceGrant identity

wrong provider resource:
still DENIED

wrong run/attempt:
still DENIED

wrong state/version:
still DENIED

wrong RuntimeMode/profile:
still DENIED

tool/secret resource substituted for provider:
still DENIED
```

No wildcard resource matching.

# 8. targeted verification

Use repository-local Python with `-B`.

Run the minimum targeted tests necessary to prove the causal correction.

At minimum:

```text
changed-file py_compile
ruff on changed Python files
existing/added unit tests covering exact provider grant match + mismatch
targeted local deterministic provider security path
targeted Stockroom S1 integration using non-private fixture/fake only
git diff --check
```

No full repository suite unless a targeted failure makes it necessary; if so STOP with scope expansion rather than silently running it.

No external network/provider.

# 9. 1822 lineage preservation

This Task does not inspect private DB, so do not claim current DB state from new observation.

Treat the following only as accepted predecessor evidence:

```text
1822 WorkRun RUNNING/v2
1822 attempt EXECUTION_FAILED/v3
0036 FAILED/quarantined preserved
v1 preserved
v2 contains retained materialized workspace
```

No cleanup or reuse.

# 10. result classification

Success candidate:

```text
exact mismatch diagnosed
minimal correction applied
security exact-match invariant preserved
targeted tests PASS
private runtime retry NOT performed
```

If no single causal mismatch is proven:

```text
STOP / DIAGNOSIS_INCONCLUSIVE
```

If required change is outside allowlist:

```text
STOP / SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
```

# 11. Git boundary

No commit.

Final tracked dirt must be exactly the changed product/test/config paths within section 6 allowlist.

Current Task moves active→done byte-identically.

Git-visible untracked must include exactly:

```text
1822 Cycle/Judgment/done Task
current Cycle/Judgment/done Task
```

No unrelated untracked files.

Legacy 1400 stays ignored/non-owned.

# 12. contract review

Exactly 30 rows:

```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_CLEAN
PREDECESSOR_1822_TRIPLE_EXACT
CURRENT_STATE_HASHES_EXACT
LEGACY_1400_ACTIVE_PRESERVED
PYTHON_REPOSITORY_VENV_EXACT
1822_FAILURE_REASON_ACCEPTED
1822_RUNTIME_STATE_ACCEPTED
1822_0036_V1_PRESERVATION_ACCEPTED
NO_PRIVATE_RUNTIME_ACCESS
NO_RETAINED_DB_ACCESS
NO_DOCKER_RUNTIME_EXECUTION
GRANT_REQUEST_CALLCHAIN_IDENTIFIED
PROVIDER_RESOURCE_IDENTITY_IDENTIFIED
RESOURCE_GRANT_IDENTITY_IDENTIFIED
EXACT_MISMATCH_PROVEN
SECURITY_POLICY_NOT_WEAKENED
MINIMAL_CAUSAL_CHANGE_ONLY
NO_UNRELATED_CONFIG_RELAXATION
TARGETED_UNIT_TESTS_PASS
TARGETED_PROVIDER_SECURITY_TEST_PASS
TARGETED_S1_INTEGRATION_FAKE_PASS
NO_EXTERNAL_PROVIDER_NETWORK
NO_CANONICAL_STATE_MUTATION
NO_GIT_COMMIT_PUSH
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
FINAL_CHANGED_PATHS_WITHIN_ALLOWLIST
FINAL_UNTRACKED_GOVERNANCE_EXACT
DIAGNOSIS_REPORT_COMPLETE
EXPORT_INTEGRITY_PASS
```

A successful rework candidate requires 30/30 PASS.

A scoped stop must not relabel unperformed correction/tests as PASS.

# 13. export

Root docs:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
1822_ACCEPTANCE_VERIFICATION.md
RESOURCE_GRANT_DIAGNOSIS.md
SECURITY_INVARIANT_VERIFICATION.md
SOURCE_CHANGE_SUMMARY.md
TEST_VERIFICATION.md
CONTRACT_REVIEW.md
```

Include:

```text
current Cycle
current Judgment
current done Task
every changed product/config/test path
```

Generate manifest/member counts from the actual declared set.

Require:

```text
one top-level
CRC PASS
TASK.md == canonical done Task
all manifest SHA/size exact
no private path/value/DB content
```

# 14. success ceiling

```text
1822 runtime:
REWORK_REQUIRED / preserved

provider resource-grant defect:
DIAGNOSED + SOURCE_CANDIDATE_CORRECTED

private S1 retry:
NOT_PERFORMED / Browser authorization pending

P2-3:
IN_PROGRESS
```
