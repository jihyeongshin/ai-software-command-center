# 작업지시서: P2-3 A2 pycompile cache cleanup + proof admission reverification

## meta

- task_id: `20260911_0335_aiscc-p2-3-a2-pycompile-cache-cleanup-and-proof-admission-reverification-1`
- created_at: `2026-09-11T03:35:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `CLEANUP_ONLY / WORKSPACE_REVERIFICATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `876f232880e652fbf715f13c13b8cc03d27404f0`
- required_base_tree: `0f855b67fcad1be1cb4f635b6b4db8856c43da64`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. purpose

Do not rerun implementation/static/tests.

The 0240 executable proof is already complete:

```text
static PASS
B3 23 PASS
A1 51 PASS
A2 2 PASS
direct-owner 58 PASS
aggregate 134 PASS / 0 skip
contract 27/27 PASS
```

This Task only removes nine exact py_compile cache files created by the mandatory proof command and re-verifies workspace/source identity.

# 1. inbound transport

Verify Browser delivery ZIP exact filename/SHA-256 from the Short Prompt.

Place TASK first at:

```text
.aiassistant/tasks/active/20260911_0335_aiscc-p2-3-a2-pycompile-cache-cleanup-and-proof-admission-reverification-1.md
```

Read fully.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260911_0335_aiscc-p2-3-a2-executable-proof-complete-workspace-residue-cleanup-entry-1.cycle.md
SHA-256:
5417303643829f0a8853e62ceac53b115a55f34fc831c12e13e6ecd4bc15df70

.aiassistant/reports/aiscc/20260911_0335_aiscc-p2-3-a2-executable-proof-workspace-residue-judgment-1.md
SHA-256:
3b15a6c0ffc0fc81faefbbd345249e010a00388fbe60da264b636f89829ef1f0
```

Bootstrap failure before canonical Task placement:

```text
STOP
no cleanup
no report/export
```

# 2. repository gate

Require:

```text
branch:
main

HEAD:
876f232880e652fbf715f13c13b8cc03d27404f0

HEAD tree:
0f855b67fcad1be1cb4f635b6b4db8856c43da64

index:
empty
```

Before cleanup, expected Git-visible count excluding active Task:

```text
48
```

Composition:

```text
39 expected governance/candidate paths including current Cycle/Judgment
+
9 exact pycompile cache files
```

No other extra path is allowed.

If another path exists:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

# 3. exact 0240 identity

Require:

- `.aiassistant/tasks/done/20260911_0240_aiscc-p2-3-a2-static-command-transport-and-executable-proof-retry-1.md`  `fe3f99839dd5eff9929f5ac9decea33005c067979fb5c2e76267bec71004c4b9`
- `.aiassistant/records/aiscc/cycles/20260911_0240_aiscc-p2-3-a2-static-command-transport-failure-proof-retry-entry-1.cycle.md`  `4ffd1e8fe6b2cc84d8ed095085e4e658caabfc2656c06cdac96479562f32a2f9`
- `.aiassistant/reports/aiscc/20260911_0240_aiscc-p2-3-a2-static-command-transport-failure-judgment-1.md`  `0098771b51375b373c53364df7e5f4e4a4db4159f5cb688110e7c671290a56c8`

Require frozen candidate exact:

- `src/aiscc/bootstrap.py`  `1718e596b20fd107af0cb80b6ad40e3626b7e26d8d45daa649ccf2d2ccf9fe38`
- `src/aiscc/scenarios/driver.py`  `c83792b0d84d07d584e4b5b32b1925a42a8be25cc0a872f19b92cffa2150a44c`
- `src/aiscc/scenarios/composition.py`  `2017a18175e0e227fe1514d3d9e85c7d0d64d391ec94649912d9749699b7edfc`
- `src/aiscc/scenarios/stockroom_production.py`  `742ffd8122507de941e93b9e721a97335afa9acf475ff8fd01d50fdacbf8137a`
- `config/evidence/stockroom-capture.v1.json`  `70d4dbf219d54abd57877b787d8ac16d0efbe05701e7fb8bf1f84282640b31e7`
- `config/human/stockroom-capture.v1.json`  `7ec43975b8d1f30ded987d05942753dadbd93197ad86da2701514a198e797bab`
- `config/judgment/stockroom-capture.v1.json`  `31f8d08c083218d1fcc47d5ba7a8d1c151a48bbf26ea3319ac9503a666179eef`
- `tests/unit/scenarios/test_owner_composition.py`  `68cf0561e482e1ded6f6bddaa8b91da1fea753b430527e27fe66bf7cf0cb4d12`
- `tests/integration/scenarios/test_stockroom_binding.py`  `063e2b65eb229b5849bc3df61294d72f3f656783ac1257a4dbcaa82bb2d70b34`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`  `016114dbd2ae1fe14476efec862948bf8e1682f8541cd518654dc5769f5dcf13`

Any mismatch:

```text
PREDECESSOR_OR_CANDIDATE_IDENTITY_MISMATCH
→ STOP
```

# 4. exact cleanup allowlist

Only these nine files may be deleted:

- `src/aiscc/__pycache__/bootstrap.cpython-312.pyc`
- `src/aiscc/scenarios/__pycache__/capture_runner.cpython-312.pyc`
- `src/aiscc/scenarios/__pycache__/composition.cpython-312.pyc`
- `src/aiscc/scenarios/__pycache__/driver.cpython-312.pyc`
- `src/aiscc/scenarios/__pycache__/stockroom_production.cpython-312.pyc`
- `tests/integration/scenarios/__pycache__/test_stockroom_binding.cpython-312.pyc`
- `tests/integration/scenarios/__pycache__/test_stockroom_capture_runner.cpython-312.pyc`
- `tests/unit/scenarios/__pycache__/test_owner_composition.cpython-312.pyc`
- `tests/unit/scenarios/__pycache__/test_stockroom_capture_runner.cpython-312.pyc`

For each path before deletion:

```text
must be a regular file
must be untracked
must end in .cpython-312.pyc
must be located at the exact listed path
```

If a listed path is absent, record `ALREADY_ABSENT` and continue only if no unexpected path exists.

If a listed path is tracked, symlink/reparse target, directory, or otherwise non-regular:

```text
CLEANUP_IDENTITY_MISMATCH
→ STOP
```

# 5. cleanup method

Delete each exact file individually.

Do not use:

```text
git clean
recursive Remove-Item on __pycache__
rmdir /s
directory glob deletion
find-delete
repository-wide cache cleanup
```

Empty `__pycache__` directories may remain if ignored/non-Git-visible. Do not remove them unless necessary for one exact file deletion.

# 6. post-cleanup workspace

After deleting the nine exact files require:

```text
Git-visible excluding active Task:
39 exact

index:
empty

extra:
0

missing:
0
```

All candidate SHA-256 values from section 3 must remain exact.

No source/test/config/governance predecessor file may change.

# 7. no proof rerun

Do not run:

```text
py_compile
Ruff
pytest
PostgreSQL
Alembic
Docker
materializer
provider
tool
network
```

Reason:

```text
0240 executable evidence is already admitted for reuse
AND
this cleanup changes no source/test/config bytes
```

# 8. proof admission reverification

Report:

```text
0240 static proof:
REUSED_ACCEPTED

B3 23:
REUSED_ACCEPTED

A1 51:
REUSED_ACCEPTED

A2 2:
REUSED_ACCEPTED

direct-owner 58:
REUSED_ACCEPTED

aggregate 134:
REUSED_ACCEPTED

contract 27/27:
REUSED_ACCEPTED

applicability:
candidate bytes exact before/after cleanup
```

Do not claim final A2 acceptance.

# 9. known next blocker

Preserve:

```text
S2 Judgment negative-evaluation binding:
ADAPTER_LOCAL_BINDING_ONLY / NOT_FIXED

A2 persistence:
NOT_AUTHORIZED

actual S1-S4:
NOT_STARTED
```

# 10. Task lifecycle

Move active Task byte-identically to:

```text
.aiassistant/tasks/done/20260911_0335_aiscc-p2-3-a2-pycompile-cache-cleanup-and-proof-admission-reverification-1.md
```

Final expected Git-visible count:

```text
40 exact
```

That is:

```text
39 expected governance/candidate paths
+
current done Task
```

Require:

```text
index empty
extra 0
missing 0
```

# 11. no Git persistence

Do not run:

```text
git add
git commit
git push
git reset
git restore
git stash
```

# 12. required export

Bundle:

```text
.aiassistant/reports/target/20260911_0335_aiscc-p2-3-a2-pycompile-cache-cleanup-and-proof-admission-reverification-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
CLEANUP_VERIFICATION.md
PROOF_REUSE_VERIFICATION.md
```

Also include byte-preserving copies of:

```text
current Cycle
current Judgment
current done Task
```

Expected:

```text
6 root docs
3 canonical copies
9 members total
```

`EXPORT_MANIFEST.md` covers all 8 non-self entries with path, byte size, SHA-256.

Require one top-level directory, CRC PASS, exact member set, manifest exact.

# 13. mandatory stop

```text
DOWNLOAD_ZIP_MISSING
DOWNLOAD_ZIP_HASH_MISMATCH
DOWNLOAD_ZIP_CORRUPT
DOWNLOAD_TASK_MEMBER_MISSING
DOWNLOAD_TASK_PLACEMENT_FAILED
TRANSPORT_FAILURE
HEAD_OR_TREE_MISMATCH
INDEX_NOT_EMPTY
DIRTY_WORKSPACE_MIXED
PREDECESSOR_OR_CANDIDATE_IDENTITY_MISMATCH
CLEANUP_IDENTITY_MISMATCH
UNEXPECTED_WORKSPACE_DELTA
ZIP_EXPORT_FAILED
```

# 14. success ceiling

Success:

```text
workspace:
RECONCILED

prepared-owner/materialized-output executable proof:
ACCEPTED_CANDIDATE / READY_FOR_NEXT_AUTHORITY

S2 Judgment binding:
STILL REWORK_REQUIRED

A2 persistence:
NOT_AUTHORIZED
```
