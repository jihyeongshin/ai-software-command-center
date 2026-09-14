# 작업지시서: P2-4 regression fixture closure → durable TaskContract final candidate retry

## meta

- task_id: `20260914_1528_aiscc-p2-4-regression-fixture-closure-durable-taskcontract-final-candidate-retry-1`
- created_at: `2026-09-14T15:28:02+09:00`
- work_type: `CONTINUE_PARTIAL_IMPLEMENTATION + REGRESSION_FIXTURE_CORRECTION + FINAL_VERIFICATION + GIT_PERSISTENCE`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `a81f6633f79798c0bf0582bda00cce7dd5d1d313`
- required_parent: `0400c7839088c10b6530968014180ccb3f7c943a`
- predecessor_result_zip_sha256: `99e2487508d32d422c70f54c2b1c9106df6807552a81b7d1f5949d266a5cadc3`
- predecessor_done_task_sha256: `4c37959901962745e80faff02e3b9921f870b6706a82a4640e1f018a26792225`
- predecessor_result: `BLOCKED / SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED`
- predecessor_executor_disposition: `ACCEPTED_AS_TRUTHFUL_FAIL_CLOSED`
- blocker_classification: `STALE_DIRECT_REGRESSION_FIXTURES / TEST_SCOPE_EXPANSION_ONLY`
- fresh_IDE_chat_required: `No`
- preserve_existing_21_path_candidate: `Yes / exact SHA preflight`
- new_product_semantic_change_authorized: `No`
- additional_test_mutation_authorized: `Yes / exact 3 existing integration test files`
- governance_commit_authorized: `Yes / exact 3 paths / Commit A`
- result_commit_authorized: `Yes / candidate + exact regression fixture paths / Commit B`
- Docker_authorized: `Yes / local postgres:17.6 isolated proof only`
- external_network_authorized: `No`
- provider_LLM_authorized: `No`
- retained_private_DB_authorized: `No`
- actual_self_dogfood_golden_cycle_authorized: `No`
- push_deploy_authorized: `No`
- success_ceiling: `P2_4_TASKCONTRACT_DURABLE_BODY_IMPLEMENTATION_CANDIDATE / BROWSER_REVIEW_REQUIRED`

# 0. Browser judgment of 1302

Independent result verification:

```text
ZIP SHA-256:
99e2487508d32d422c70f54c2b1c9106df6807552a81b7d1f5949d266a5cadc3

75 members
one top-level directory
CRC PASS
74 manifest rows exact by independent size/SHA recalculation
no unmanifested member except EXPORT_MANIFEST.md
TASK/Cycle/Judgment/Human-review byte-exact to issued 1302 package
```

1302 result:

```text
BLOCKED / SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
```

Executor:

```text
ACCEPTED_AS_TRUTHFUL_FAIL_CLOSED
```

Governance Commit A from 1302:

```text
a81f6633f79798c0bf0582bda00cce7dd5d1d313

parent:
0400c7839088c10b6530968014180ccb3f7c943a

message:
docs(aiscc): accept taskcontract v1 issuance domain lock correction
```

1302 achieved:

```text
new/changed TaskContract/P1-6/P1-8 tests:
no reported failures

migration 0009 isolated proof:
PASS

cycle-derived V1 / unsupported recovery gate:
PASS

P1-6 definition owner proof:
PASS in new/changed tests

P1-8 currentness owner proof:
PASS in new/changed tests

lock proof:
PASS in new/changed tests

Ruff changed Python:
PASS

compile:
PASS

git diff --check:
PASS
```

But final direct regression:

```text
178 PASS
13 FAIL
0 SKIP
191 total
```

Therefore no Result Commit B was permitted.

# 1. exact blocker ownership

The 13 failures are accepted as regression-fixture scope blockers, not yet product/runtime defects.

## 12 failures

Observed exact error:

```text
ValueError:
G_EXECUTOR_SUBMISSION requires an issuer-verified execution ref
```

Affected existing test files:

```text
tests/integration/evidence/test_postgres_evidence_admission.py
tests/integration/workflow/test_postgres_kernel.py
tests/integration/human/test_postgres_human_gate_judgment.py
```

Required-base `src/aiscc/workflow/guards.py` already enforces this rule.
The three test files and guard source were unchanged from required base before this Task.

The correction MUST update test fixtures to use the existing canonical issuer-verified execution-submission authority.

It MUST NOT weaken/bypass `G_EXECUTOR_SUBMISSION`.

## 1 failure

Existing:

```text
tests/integration/workflow/test_postgres_kernel.py::test_migration_is_at_exact_head
```

expects:

```text
20260901_0008
```

but authorized current migration head is:

```text
20260914_0009
```

Correct this stale test expectation/current-head fixture.

# 2. accepted input / predecessor evidence

Accepted design SHA:

- `0319/TASKCONTRACT_DURABLE_BODY_BASELINE_PROPOSAL.md`: `803686433f900282117a4318d8f59a14b5b5a68735775b4f1242acf544c16410`
- `0812/20260914_0812_aiscc-p2-4-durable-taskcontract-body-ref-compatibility-human-correction-review-1.md`: `4c6905734e7a48b9688257574d86b1a7215627ac8514c7112747889c6bafa318`
- `0902/BASELINE_SUPERSESSION_DELTA.md`: `47a473ab37a9fec09dee623dc254acf7d0b726f30cbae5c251715679ff6a9448`
- `0902/HUMAN_BINDING_CORRECTION_PROPOSAL.md`: `7ecad09c1e151fc76e83d85d7a84c25c14f09abba7e093393a5cf73b9a1d2833`
- `0902/HUMAN_JUDGMENT_POLICY_SOURCE_AUDIT.md`: `2595ac130c12a0da3cf45dc7867e4cb6806fafc83e0c77feec51147ccc57b0a9`
- `0902/IMPLEMENTATION_IMPACT_ALLOWLIST.md`: `aee264ccc3aaa5aa6906c3c96ad0981d0c5aea11c68895e63dad3b3638632c6b`
- `0902/JUDGMENT_BINDING_CORRECTION_PROPOSAL.md`: `aed8421248cc8700fd0ebc2128ae7f5808037df555fbe8e0ee61606dd0eb9693`
- `0902/OWNER_NON_SUBSTITUTION_PROOF.md`: `7f22c68055d2cb2c118aa7ca67efc01ab36c09811030362bc935d23634e70a92`
- `0940/BASELINE_SUPERSESSION_DELTA.md`: `20f050403f50f9edaa9c445ba049135da896b52cc31dadf03a7912dde34d7e69`
- `0940/IMPLEMENTATION_IMPACT_ALLOWLIST.md`: `cf5a4cc5932d4ebaec1d84376bfbaff7a9c7d93cfba5379f883ebd94d3766080`
- `0940/OWNER_NON_SUBSTITUTION_PROOF.md`: `3ba78e965f88749d6805268d049154366f7bbcee1c1d77697393230c7e6aff23`
- `0940/P1_8_DESCRIPTOR_TEMPLATE_SEMANTICS_AUDIT.md`: `609d6c085b7edd2a79bbf8afd0e2461ec1919642cfdb33e333bea5c64676668c`
- `0940/TASKCONTRACT_TEMPLATE_REQUIREMENT_CORRECTION_PROPOSAL.md`: `da2bf0d59e148d6359b7e979296a7d63b01307f0500df6c2e715937527edd951`
- `0940/TEMPLATE_AUTHORITY_CANONICAL_AUDIT.md`: `2889d21300126671ee1e1b3ecc3acf3b1a96358b1e26c81e253e94413b4f5f85`

1212 Human review:

```text
SHA-256:
6eb6dc79180c885f34b700c2d60a9439f986961078cb06c0f95a640f8c9f81e7
```

Predecessor diagnostic evidence:

- `CONTRACT_REVIEW.md`: `2a43695e1d60319f1ae42ab2cab1f617651274fc10e59dd582313ffd8c31e71e`
- `EXECUTOR_REPORT.md`: `914a7044ffe0d1bddd0c72266f17536ec61dba279235d11373d7da741ff8efc4`
- `MIGRATION_REVIEW.md`: `6d0550e5850de399f2278f147d143bb92c717c8babb5ceadcefc2f2eafacee3d`
- `POSTGRES_RUNTIME_EVIDENCE.md`: `c786a48daaf5e07d5c0e204c0f34c0054737754e78ce63c74f711be92c01de63`
- `SOURCE_CHANGE_REVIEW.md`: `b5aaa31a8fbb147df851012d8dfa8e44956cc72abce164a9c1c37e6b9d125c71`
- `TASKCONTRACT_V1_LOCK_ORDER_PROOF.md`: `a4cb8034d0fda9b481e2010699a791d7bd316a7b51d01502ca9b87fb8f3bf5c3`
- `TEST_RESULTS.md`: `3b769bdf44523c334ec8bfe0bdcc1388d5fdf790d4a4f236588fa3e46614dfa9`
- `V1_ISSUANCE_DOMAIN_ACCEPTANCE_VERIFICATION.md`: `fdc753f08d6bf267688c7095ceefaf40f1aa68e11bfbe7f25ea8a070eab0b8c4`
- `WORKSPACE_VERIFICATION.md`: `5c9ad342ae4eef25d8eaafbf833399e2173c06fa102065e6b1f7896449c775ff`
- `evidence/FAILURE_OWNERSHIP.json`: `dd558bd45067b28eb0a980389d4824a927b112794ecd9491ef75f6683379f034`
- `evidence/POSTGRES_PROOF.json`: `eb002084fe6b34fea8d8b1f8727df3cb9a292939986b652d567dae1156cc236a`
- `evidence/STATIC_CHECKS.json`: `dcd4baceabf46c33354da405a391f430916a9a3608c36e14aba4347ae6e9331c`

Copy package evidence only under:

```text
.aiassistant/reports/target/20260914_1528_aiscc-p2-4-regression-fixture-closure-durable-taskcontract-final-candidate-retry-1/accepted-input/
```

after Task-first read.

Any mismatch -> `BLOCKED_MISSING_ARTIFACT`.

# 3. exact dirty-workspace continuation preflight

Do NOT reset or reconstruct the candidate.

Require:

```text
branch:
main

HEAD:
a81f6633f79798c0bf0582bda00cce7dd5d1d313

HEAD^:
0400c7839088c10b6530968014180ccb3f7c943a

index:
empty
```

The following 21 candidate paths MUST exist at these exact bytes before any product/test mutation:

- `.aiassistant/rules/AISCC_ARCHITECTURE.md`: `490e7fd09edc1d7d7a32357c219dc37274f32ca769261910e7274a8fc111492e`
- `.aiassistant/rules/AISCC_ORCHESTRATION.md`: `c47fcad05133139060701c08c0cb862de655839ed0d212d191ab84b830d690d5`
- `.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md`: `6b3f43e8cf9d2c922175b59a3eb649282c37f747827b4d94be66519ede86b730`
- `.aiassistant/rules/AISCC_TASKCONTRACT_DURABLE_BODY_AUTHORITY.md`: `d1a058d47b46c6f65de7427c6ecc15dfbe41667408ff609e142838974e3a87ed`
- `migrations/versions/20260914_0009_task_contract_durable_bodies.py`: `82aa2c1627732c21162efd38d1e74439672c09702ca5ff35f1802b1407703e8c`
- `src/aiscc/evidence/repository.py`: `1a6f208b7251ec20a145812e846e96208db159a7ffd114a10f46a9d78799f8f5`
- `src/aiscc/next_action/repository.py`: `65328357532182e0fdb79798829a923b158f62329577c0edd13dc300980cd666`
- `src/aiscc/persistence/models.py`: `fe37edea0096e848e825be5eb5664360b02d098e7870425099ff97599281dc77`
- `src/aiscc/task_authority/__init__.py`: `252b917e4e29ead17b352dd22d4cca1a13f21db80dc5eca3642e813f64bbc282`
- `src/aiscc/task_authority/authority.py`: `98aea7d41bc6b99f0ebe1a44ab1c8a06ce324c6d6ce236698c2164632006eef5`
- `src/aiscc/task_authority/contracts.py`: `6ecca22b12398f22c1f5014dbd3363459f4d3d984418aea8ba5bb63b92cf79f1`
- `src/aiscc/task_authority/ports.py`: `edb70684b1a6393df2128a61c9629d8499a09cffafe36b007f5e6f324d5e1b53`
- `src/aiscc/task_authority/ready.py`: `6e39a3390ddd9201daddd501e1e4ed576a49a04f458c7028de2526814af6d756`
- `src/aiscc/task_authority/repository.py`: `b7bc107e4d7805605c3dbc4c96157d623824759fbb2b4012335db9d575ce8500`
- `tests/integration/evidence/test_requirement_definition_resolver.py`: `44689a0a7358249f4f68fe17b9c563b4c9a0c1651d4f94516a47ffe42d239208`
- `tests/integration/memory/test_postgres_project_memory_next_action.py`: `3aa2f698717e254e5dceb2b97a86e56220bdf27a8387f408851ffb38865dd951`
- `tests/integration/task_authority/test_task_contract_durability.py`: `786c8d6472f558e6b7db59319115f27548cefe244eba51e202d018493febe04b`
- `tests/integration/task_authority/test_task_contract_ready.py`: `63f9fdbbb1de190980f7ac035c0affe84ba1f66bec83553b1f7615063d980f2d`
- `tests/unit/evidence/test_requirement_definition_resolver.py`: `2c1a49e546c6bfbf0146dc701d9cadde6f3b228e6ba6877acd833bb9ccf394fa`
- `tests/unit/task_authority/test_task_contract_body.py`: `51a693430140a7c7ca969797620cead61c01963367b45ce5642ec0b862e06690`
- `tests/unit/task_authority/test_task_contract_issuance.py`: `64e418f297282a53d35429497a8b00415178363d00fc03e2003c5c6df0f2f81c`

Expected candidate status:

```text
11 tracked modified
10 untracked added
```

Additionally Git-visible untracked governance path:

```text
.aiassistant/tasks/done/20260914_1302_aiscc-p2-4-cycle-derived-v1-lock-corrected-durable-taskcontract-implementation-continuation-1.md
```

SHA:

```text
4c37959901962745e80faff02e3b9921f870b6706a82a4640e1f018a26792225
```

Exact clean-base hashes for newly authorized regression fixture paths and protected guard source:

- `tests/integration/evidence/test_postgres_evidence_admission.py`: `ea65a1002bcd168c40e4d1ddb2d3b8b736f06f59dba6c61eb9a3022280e15837`
- `tests/integration/workflow/test_postgres_kernel.py`: `10be51d5d7b43b4dbd2df8a19900ac4c116990a42860ffe8a015170cff877240`
- `tests/integration/human/test_postgres_human_gate_judgment.py`: `74998881f78310ec85ac2eb500c754db6b816ae5939f9d09ac9e1d41418f666e`
- `src/aiscc/workflow/guards.py`: `e7509199bca3b901c7a04b4e5a1d8c23bab217eca5b78a3b9319d10300993cab`

The three test paths must initially match those base hashes.

`src/aiscc/workflow/guards.py` must remain read-only and exact.

Preserve legacy:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
SHA:
52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

Canonical state remains:

```text
CURRENT_STATE_SUMMARY.md
80b16f9a5fab2aa7870baeac4ec6fbf27d08bb50637ed61618573ce0bc2ded48

DECISION_REGISTER.md
9da6dde722f2552020a40085995fef062a8920e477da7656c3a176fff52142e5

NEXT_ACTIONS.md
050a93baf1740f298ec2601c08b392118b143f9838002c159b5401ccf6418679
```

Any unexpected path/hash/dirt -> `DIRTY_WORKSPACE_MIXED` and STOP.

# 4. executables

Use only:

```text
Python:
<repository-root>\.venv\Scripts\python.exe

Git:
C:\Program Files\Git\cmd\git.exe

Docker:
C:\Program Files\Docker\Docker\resources\bin\docker.exe
```

No PATH substitution.

# 5. inbound placement + Governance Commit A

Order:

```text
verify ZIP/hash/archive/path safety
→ place current Task in .aiassistant/tasks/active
→ read Task
→ exact workspace/hash preflight
→ place Cycle/Judgment
```

Canonical:

```text
20260914_1528_aiscc-p2-4-regression-fixture-blocker-final-candidate-retry-entry-1.cycle.md
-> .aiassistant/records/aiscc/cycles/

20260914_1528_aiscc-p2-4-1302-regression-fixture-scope-expansion-authorization-1.md
-> .aiassistant/reports/aiscc/
```

Preserve all 21 candidate paths unstaged.

Stage EXACTLY:

```text
.aiassistant/tasks/done/20260914_1302_aiscc-p2-4-cycle-derived-v1-lock-corrected-durable-taskcontract-implementation-continuation-1.md
.aiassistant/records/aiscc/cycles/20260914_1528_aiscc-p2-4-regression-fixture-blocker-final-candidate-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260914_1528_aiscc-p2-4-1302-regression-fixture-scope-expansion-authorization-1.md
```

Commit message exactly:

```text
docs(aiscc): record durable taskcontract regression fixture blocker
```

Require:

```text
Commit A parent = a81f6633f79798c0bf0582bda00cce7dd5d1d313
changed paths = exact 3
index empty
21 candidate paths preserved byte-exact immediately after Commit A
```

# 6. newly authorized regression fixture mutation — exact 3 paths only

You may modify ONLY:

```text
tests/integration/evidence/test_postgres_evidence_admission.py
tests/integration/workflow/test_postgres_kernel.py
tests/integration/human/test_postgres_human_gate_judgment.py
```

for predecessor regression closure.

No other previously-clean test/source path may be modified.

## 6.1 issuer-verified G_EXECUTOR_SUBMISSION fixture correction

Before editing, inspect:

```text
src/aiscc/workflow/guards.py
existing P1-5 / workflow / task-authority tests that already demonstrate the canonical issuer-verified execution-submission path
```

Use the EXISTING source-owned API/type/ref semantics.

Do NOT:

```text
call generic system.issue(...) for G_EXECUTOR_SUBMISSION
weaken P1_4GuardAuthority
add a test-only bypass to product source
construct an arbitrary unverified string and relabel it verified
skip RUNNING -> ADMISSION_PENDING
remove G_EXECUTOR_SUBMISSION from guard requirements
mock away issuer verification
xfail/skip failing cases
```

Test fixtures may create a synthetic-but-valid issuer-owned execution ref using existing authority objects exactly as production source requires.

Where multiple tests share a local helper inside one of the three authorized files, update that helper rather than duplicating ad hoc bypass logic.

The fixture correction is test setup only; tested workflow semantics/assertions must remain materially unchanged.

## 6.2 migration head fixture correction

In:

```text
tests/integration/workflow/test_postgres_kernel.py
```

correct the stale `0008` head expectation to the authorized current code head.

Preferred:

```text
compare DB revision to repository migration current head using an existing deterministic migration helper
```

if such a helper already exists and does not broaden dependencies.

Otherwise exact literal:

```text
20260914_0009
```

is allowed for this current exact-head test.

Do NOT weaken the test to merely check “non-null revision”.

# 7. candidate freeze / conditional product rework rule

First correct ONLY the three fixture paths and rerun the exact 13 predecessor failing cases.

If all 13 pass without changing any of the 21 candidate files:

```text
candidate freeze remains satisfied
```

Then proceed to full final-byte regression.

If a fixture-corrected test exposes a real product defect:

- classify the exact failing assertion;
- product correction is allowed ONLY within the already-authorized 21 candidate paths;
- do not modify any additional source path;
- record exact before/after SHA and reason in `PRODUCT_REWORK_AFTER_FIXTURE.md`.

If product correction would require a path outside the existing 21 candidate set:

```text
SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
```

STOP.

If an accepted owner semantic would need changing:

```text
AUTHORITY_OWNER_SCOPE_EXPANSION_REQUIRED
```

STOP.

# 8. focused 13-case closure

Run exactly the 13 predecessor failed node IDs first.

Required:

```text
13 PASS
0 FAIL
0 SKIP
```

Record:

```text
REGRESSION_FIXTURE_CLOSURE.md
```

For every case record:

```text
node id
prior failure
fixture correction used
current result
whether product candidate bytes changed
```

No count substitution.

# 9. isolated PostgreSQL environment

Use local:

```text
postgres:17.6
```

No pull.

A new Task-owned isolated container is permitted, e.g.:

```text
aiscc-p2-4-taskcontract-1528-pg
```

Loopback-only port, synthetic credentials, no host bind.

Upgrade to current migration head before regression.

No retained/private DB.

Exact container/anonymous-volume cleanup best-effort after proof.

# 10. final-byte regression contract

After focused 13 PASS, rerun the SAME direct regression family used in 1302:

```text
tests/unit/evidence
tests/unit/next_action
tests/unit/task_authority
tests/unit/workflow
tests/unit/human
tests/integration/evidence
tests/integration/memory/test_postgres_project_memory_next_action.py
tests/integration/task_authority
tests/integration/workflow
tests/integration/human
```

Use:

```text
--import-mode=importlib
-q
```

Expected final contract, assuming no tests are added/removed/parameterization changed:

```text
191 PASS
0 FAIL
0 SKIP
```

If collected count != 191:

```text
TEST_CONTRACT_COUNT_MISMATCH
```

STOP and report exact reason unless the count difference is mechanically proven to be pytest collection metadata with identical node IDs. Do not silently accept changed coverage.

No xfail/skip conversion.

# 11. reverify critical new runtime proof

Because this Task changes only legacy regression fixtures, do not rerun every exploratory predecessor probe.

But after final regression PASS, reverify at minimum:

```text
migration head = 20260914_0009
empty DB -> head PASS
0008 -> 0009 PASS
nonempty downgrade fail-closed preservation PASS

96/96 IDs -> 93-char body_ref PASS
V1 cycle-derived issuance PASS
V1 OPERATIONAL_RECOVERY unsupported-source DENY with zero body/ref/event writes
issuer/revoker WorkRun lock count = 0
READY target WorkRun lock first
P1-6 exact definition graph/revocation currentness PASS
P1-8 cycle currentness/invalidation PASS
Human/Judgment READY creates no future facts
```

You may reuse exact predecessor proof only where final relevant source bytes are unchanged AND this Task has an explicit fresh regression covering the same source bytes. State reuse vs rerun explicitly.

# 12. static closure

Run final bytes:

```text
Ruff on all changed Python including the three fixture paths
compile changed Python
git diff --check
UTF-8/control/fence checks on candidate docs
```

Required all PASS.

# 13. forbidden

Forbidden:

```text
modify src/aiscc/workflow/guards.py
modify workflow product source
modify human product source
modify judgment product source
modify evidence requirements/models semantics
weaken issuer verification
bypass G_EXECUTOR_SUBMISSION
skip/xfail failing tests
remove regression tests
reduce collected test count
change migration lineage
remove migration 0009
change 1212 V1 source boundary
support OPERATIONAL_RECOVERY in V1
actual self-dogfood golden cycle
src/aiscc/self_dogfood/** mutation
canonical state mutation
retained/private DB
external network/provider
Docker pull
push/deploy
```

# 14. exact Result Commit B allowlist

On complete PASS, Commit B may include:

## existing 21 candidate paths

- `.aiassistant/rules/AISCC_ARCHITECTURE.md`
- `.aiassistant/rules/AISCC_ORCHESTRATION.md`
- `.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md`
- `.aiassistant/rules/AISCC_TASKCONTRACT_DURABLE_BODY_AUTHORITY.md`
- `migrations/versions/20260914_0009_task_contract_durable_bodies.py`
- `src/aiscc/evidence/repository.py`
- `src/aiscc/next_action/repository.py`
- `src/aiscc/persistence/models.py`
- `src/aiscc/task_authority/__init__.py`
- `src/aiscc/task_authority/authority.py`
- `src/aiscc/task_authority/contracts.py`
- `src/aiscc/task_authority/ports.py`
- `src/aiscc/task_authority/ready.py`
- `src/aiscc/task_authority/repository.py`
- `tests/integration/evidence/test_requirement_definition_resolver.py`
- `tests/integration/memory/test_postgres_project_memory_next_action.py`
- `tests/integration/task_authority/test_task_contract_durability.py`
- `tests/integration/task_authority/test_task_contract_ready.py`
- `tests/unit/evidence/test_requirement_definition_resolver.py`
- `tests/unit/task_authority/test_task_contract_body.py`
- `tests/unit/task_authority/test_task_contract_issuance.py`

## newly corrected regression fixture paths

```text
tests/integration/evidence/test_postgres_evidence_admission.py
tests/integration/workflow/test_postgres_kernel.py
tests/integration/human/test_postgres_human_gate_judgment.py
```

No other path.

Commit message exactly:

```text
feat(aiscc): add durable taskcontract authority
```

Require:

```text
Commit B parent = current Task Governance Commit A
changed paths subset = exact authorized 24-path universe
index empty
tracked clean
```

Do not create Commit B until:

```text
focused 13 = 13 PASS
full direct regression = 191 PASS / 0 FAIL / 0 SKIP
static = PASS
critical proof = PASS/reused exactly as section 11 permits
```

# 15. report/export

Target:

```text
.aiassistant/reports/target/20260914_1528_aiscc-p2-4-regression-fixture-closure-durable-taskcontract-final-candidate-retry-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
ACCEPTED_INPUT_VERIFICATION.md
REGRESSION_FIXTURE_AUDIT.md
REGRESSION_FIXTURE_CLOSURE.md
PRODUCT_REWORK_AFTER_FIXTURE.md
FINAL_REGRESSION_RESULTS.md
CRITICAL_RUNTIME_REVERIFICATION.md
SOURCE_CHANGE_REVIEW.md
MIGRATION_REVIEW.md
POSTGRES_RUNTIME_EVIDENCE.md
STATIC_CHECKS.md
CONTRACT_REVIEW.md
```

`PRODUCT_REWORK_AFTER_FIXTURE.md` must exist even when no product rework occurred; then state `NOT_REQUIRED / candidate bytes unchanged before final regression` except the three fixture files.

Include changed project-relative files, current Cycle/Judgment, and current done Task.

No credentials/raw DB dump/private path leakage.

# 16. terminal success boundary

Success:

```text
HEAD = Result Commit B
index empty
tracked clean

Git-visible untracked exactly:
.aiassistant/tasks/done/20260914_1528_aiscc-p2-4-regression-fixture-closure-durable-taskcontract-final-candidate-retry-1.md
```

Current Task active -> done byte-exact.

Legacy 1400 unchanged.

Canonical state hashes unchanged.

No extra Task-owned container/volume.

# 17. blocked boundary

On any blocker:

```text
no Commit B
preserve truthful candidate/test bytes
no broad reset/clean
export exact evidence
```

Named blockers:

```text
BLOCKED_MISSING_ARTIFACT
DIRTY_WORKSPACE_MIXED
TEST_FIXTURE_SCOPE_EXPANSION_REQUIRED
TEST_CONTRACT_COUNT_MISMATCH
SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
AUTHORITY_OWNER_SCOPE_EXPANSION_REQUIRED
MIGRATION_BASELINE_MISMATCH
ISOLATED_POSTGRES_IMAGE_MISSING
BLOCKED_REQUIRED_EVIDENCE
SECURITY_BOUNDARY_BLOCKED
```

# 18. success ceiling

Complete PASS may report only:

```text
P2_4_TASKCONTRACT_DURABLE_BODY_IMPLEMENTATION_CANDIDATE
/ BROWSER_REVIEW_REQUIRED
```

Do NOT perform/claim:

```text
actual self-dogfood golden cycle
P2_4_SELF_DOGFOOD_ENTRY_SOURCE_CANDIDATE
P2-4 ACCEPTED/CLOSED
```
