# 작업지시서: P2-3 private S1 Cut B temporary-context cleanup + final proof

## meta

- task_id: `20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1`
- created_at: `2026-09-12T14:00:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `CUT_B / TEMPORARY_ARTIFACT_CLEANUP / FINAL_PROOF`
- evidence_profile: `HIGH_RISK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `0fe2105f35b4fcf9769ae76361cb42b47220ac7d`
- required_tree: `a46a8816acc34214983925fe02ed77df55f6b909`
- accepted_cut_a_commit: `750c37aecb4c264f66aabf12dedb8d54e20a7f95`
- predecessor_task: `.aiassistant/tasks/done/20260912_0420_aiscc-p2-3-private-s1-cut-b-clean-authority-provisioning-retry-1.md`
- fresh_ide_executor_chat: `FORBIDDEN`
- fresh_ide_executor_chat_reason: `cleanup authority depends on exact private temporary paths retained only in the existing 0420 Executor chat`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. purpose

Resolve only the remaining Cut B cleanup evidence.

Do not rebuild, reprovision, mutate candidate provenance, change source/state, or run
private S1.

The retained 0420 provisioning evidence is already Browser-accepted for this cleanup
retry.

# 1. inbound transport

Verify the Browser ZIP filename/SHA-256 from the Short Prompt.

Place the current Task first:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
```

Require it is byte-exact and ignored.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260912_1400_aiscc-p2-3-cut-b-provisioned-candidate-temporary-cleanup-entry-1.cycle.md
SHA-256:
8fb368a5fe226e72741b787cb3b2263d991705b4c699cd46491162004f50f200

.aiassistant/reports/aiscc/20260912_1400_aiscc-p2-3-cut-b-provisioning-candidate-cleanup-hold-judgment-1.md
SHA-256:
5173a486423cdfa02ec45327216ac1a7a6eb111dd1548a0b10145735c4cda176
```

Any bootstrap/member/hash mismatch:

```text
STOP
no cleanup
no environment mutation
no report/export
```

# 2. same-session private cleanup authority

This Task MUST run in the same IDE Executor chat that executed 0420.

Use only the exact temporary paths retained from that 0420 execution context.

Do not reconstruct paths from guesses.

Do not scan the filesystem broadly.

If the exact 0420 temporary build-context path and helper paths are no longer available
with prior-turn provenance:

```text
CLEANUP_PATH_AUTHORITY_UNAVAILABLE
→ STOP_WITH_REPORT_EXPORT
```

Do not ask Human to identify or type private paths.

# 3. repository gate

Require:

```text
branch:
main

HEAD:
0fe2105f35b4fcf9769ae76361cb42b47220ac7d

HEAD tree:
a46a8816acc34214983925fe02ed77df55f6b909

HEAD^:
750c37aecb4c264f66aabf12dedb8d54e20a7f95

index:
empty

tracked worktree:
clean
```

Before this delivery exact Git-visible set:

```text
14 exact
```

Exact path/hash pairs:

- `.aiassistant/records/aiscc/cycles/20260912_0259_aiscc-p2-3-cut-a-persisted-cut-b-environment-provisioning-entry-1.cycle.md`  `2da742f803b402b39f0433a0e1fabb74c8a594b93cd782555797b05d18cfc9c2`
- `.aiassistant/reports/aiscc/20260912_0259_aiscc-p2-3-cut-a-persistence-final-acceptance-cut-b-authorization-judgment-1.md`  `d64582a0a3b7040cf4a56961d7905b194949716eda98e9832a66a1c68996629d`
- `.aiassistant/tasks/done/20260912_0259_aiscc-p2-3-private-s1-cut-b-environment-provisioning-1.md`  `46b9fb7d030053eb12ac75827475ab136c12cb51b83e3a82b5516b7feee80b96`
- `.aiassistant/records/aiscc/cycles/20260912_0348_aiscc-p2-3-cut-b-artifact-hash-correction-provisioning-retry-entry-1.cycle.md`  `f8e7614602db171c3059ba279548a02252ccefb9e2eeb7d86d4fcb602dcf38f0`
- `.aiassistant/reports/aiscc/20260912_0348_aiscc-p2-3-cut-b-artifact-hash-contract-defect-retry-judgment-1.md`  `813bcdcfd13d8e4164bc09761d56ce30e5dc49a54c81d6928011df8bd19c657b`
- `.aiassistant/tasks/done/20260912_0348_aiscc-p2-3-private-s1-cut-b-artifact-hash-correction-provisioning-retry-1.md`  `dd82f0087a4c93131012a0bf6955c3e78116d39fae11dd79bee3818849589a1b`
- `.aiassistant/records/aiscc/cycles/20260912_0410_aiscc-p2-3-cut-b-self-reference-corrected-provisioning-retry-entry-1.cycle.md`  `93f5b7dc5ff55ee7dfe212c79a53e0e7cc1d05b7aafbda7b39f7523947ec8fdc`
- `.aiassistant/reports/aiscc/20260912_0410_aiscc-p2-3-cut-b-self-reference-contract-defect-retry-judgment-1.md`  `78f4ec2f7feb8fac541eb7c258bf39eb359515c4a565a1c4edf0bd4c491618a1`
- `.aiassistant/tasks/done/20260912_0410_aiscc-p2-3-private-s1-cut-b-self-reference-correction-provisioning-retry-1.md`  `9bc85a68c11d56d533923b605a029671365304ba729f17fedbeede1577ceccac`
- `.aiassistant/records/aiscc/cycles/20260912_0420_aiscc-p2-3-cut-b-clean-authority-provisioning-retry-entry-1.cycle.md`  `d3ba1c85183e6e594eccee45eb0d51a141260e0ac10b6e7fe9efd81d7325c50a`
- `.aiassistant/reports/aiscc/20260912_0420_aiscc-p2-3-cut-b-historical-baseline-path-mismatch-retry-judgment-1.md`  `cd5ee11d34d5711de6e8e1ce24aece0bb58ee731febc8516c86c3be24b49a603`
- `.aiassistant/tasks/done/20260912_0420_aiscc-p2-3-private-s1-cut-b-clean-authority-provisioning-retry-1.md`  `424bcebe4a9994db0ad09898452cda9c09537f95f93bee0a47b5164f4b7b7754`
- `.aiassistant/records/aiscc/runtime/stockroom-image-provenance.v1.json`  `e19f2b645aee85878bed7c557064bbbd0be746524f394ad88de1d2509c13b64f`
- `.aiassistant/records/aiscc/runtime/stockroom-private-postgres-provisioning.v1.json`  `36b9c93515223ade3d74923141fcbe823907b42b81e5d86bf3666a4f02032b54`

After current Cycle/Judgment placement while current Task remains active:

```text
Git-visible:
16 exact

current active Task:
exists byte-exact
ignored
```

Exact visible set:

```text
.aiassistant/records/aiscc/cycles/20260912_0259_aiscc-p2-3-cut-a-persisted-cut-b-environment-provisioning-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_0259_aiscc-p2-3-cut-a-persistence-final-acceptance-cut-b-authorization-judgment-1.md
.aiassistant/tasks/done/20260912_0259_aiscc-p2-3-private-s1-cut-b-environment-provisioning-1.md
.aiassistant/records/aiscc/cycles/20260912_0348_aiscc-p2-3-cut-b-artifact-hash-correction-provisioning-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_0348_aiscc-p2-3-cut-b-artifact-hash-contract-defect-retry-judgment-1.md
.aiassistant/tasks/done/20260912_0348_aiscc-p2-3-private-s1-cut-b-artifact-hash-correction-provisioning-retry-1.md
.aiassistant/records/aiscc/cycles/20260912_0410_aiscc-p2-3-cut-b-self-reference-corrected-provisioning-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_0410_aiscc-p2-3-cut-b-self-reference-contract-defect-retry-judgment-1.md
.aiassistant/tasks/done/20260912_0410_aiscc-p2-3-private-s1-cut-b-self-reference-correction-provisioning-retry-1.md
.aiassistant/records/aiscc/cycles/20260912_0420_aiscc-p2-3-cut-b-clean-authority-provisioning-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_0420_aiscc-p2-3-cut-b-historical-baseline-path-mismatch-retry-judgment-1.md
.aiassistant/tasks/done/20260912_0420_aiscc-p2-3-private-s1-cut-b-clean-authority-provisioning-retry-1.md
.aiassistant/records/aiscc/runtime/stockroom-image-provenance.v1.json
.aiassistant/records/aiscc/runtime/stockroom-private-postgres-provisioning.v1.json
.aiassistant/records/aiscc/cycles/20260912_1400_aiscc-p2-3-cut-b-provisioned-candidate-temporary-cleanup-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_1400_aiscc-p2-3-cut-b-provisioning-candidate-cleanup-hold-judgment-1.md
```

No duplicate or extra path.

# 4. retained environment pre-cleanup identity

Before deleting any temporary artifact, verify read-only:

```text
Stockroom image ID:
sha256:c51ad05852b58a3b4fd275ee88d183551e745d79ac8239e3da3b98372fe0bb9e

Stockroom discovery tag:
aiscc-stockroom-runtime:p2-3-private-v1

PostgreSQL container name:
aiscc-p2-3-private-postgres-v1

PostgreSQL container ID:
0b50ac47a79e05ac9b88a8f679d04ddc39f729bf1a8e099d149c4c5570b5999c

PostgreSQL state:
running

PostgreSQL volume:
aiscc-p2-3-private-postgres-data-v1

image provenance SHA-256:
e19f2b645aee85878bed7c557064bbbd0be746524f394ad88de1d2509c13b64f

DB provenance SHA-256:
36b9c93515223ade3d74923141fcbe823907b42b81e5d86bf3666a4f02032b54
```

Require PostgreSQL remains loopback-only on:

```text
127.0.0.1:55432
```

Do not export the private credential host path.

Any retained-environment identity drift:

```text
RETAINED_ENVIRONMENT_IDENTITY_DRIFT
→ STOP_WITH_REPORT_EXPORT
```

# 5. exact build-context ownership proof

Using the exact private path retained from 0420 only, require before deletion:

```text
directory exists
outside repository
outside Downloads
outside target export
not the private password path or its parent
```

Require its exact inventory still contains:

```text
16 regular files
0 symlink/reparse
0 extra
```

Recompute the canonical sorted inventory fingerprint over:

```text
relative path
byte size
SHA-256
```

Require exact:

```text
962e81a7205b109aee8a0c66fa8058aae3019462349d710f28351d4379374604
```

If path/inventory/fingerprint differs:

```text
TEMP_CONTEXT_OWNERSHIP_UNPROVEN
→ do not delete
→ STOP_WITH_REPORT_EXPORT
```

# 6. exact helper ownership proof

For every 0420 temporary verifier/probe helper path retained in the same Executor
session, require:

```text
explicitly created by 0420 Task
outside repository
outside Downloads
outside target export
not the private password file
not parent/ancestor of retained password file
not a Docker storage path
not a Git object path
```

Do not discover unrelated temp files.

If a helper's ownership cannot be proven:

```text
TEMP_HELPER_OWNERSHIP_UNPROVEN
→ preserve that helper
→ STOP_WITH_REPORT_EXPORT
```

# 7. cleanup execution

Delete only:

```text
the exact verified 0420 build-context directory
the exact verified 0420 temporary verifier/probe helper files
```

Use ordinary supported Executor filesystem operations.

Do not bypass or evade platform/tool approval or safety policy.

Do not use broad cleanup commands, wildcard temp cleanup, `git clean`, Docker prune, or
recursive deletion above the exact owned context directory.

If the platform refuses an exact cleanup operation:

```text
LOCAL_CLEANUP_POLICY_BLOCKED
→ preserve all retained environment candidates
→ STOP_WITH_REPORT_EXPORT
```

No alternate policy-bypass method.

# 8. cleanup postcondition

Require:

```text
exact build-context path:
absent

every exact owned temporary helper path:
absent
```

Require no parent/sibling deletion beyond exact Task-owned targets.

Record paths only as redacted stable labels in exported evidence:

```text
BUILD_CONTEXT
HELPER_1
HELPER_2
...
```

Do not export literal private host paths.

# 9. retained environment post-cleanup identity

After cleanup verify read-only again:

```text
Stockroom image ID:
sha256:c51ad05852b58a3b4fd275ee88d183551e745d79ac8239e3da3b98372fe0bb9e

discovery tag:
aiscc-stockroom-runtime:p2-3-private-v1

PostgreSQL container ID:
0b50ac47a79e05ac9b88a8f679d04ddc39f729bf1a8e099d149c4c5570b5999c

PostgreSQL state:
running

PostgreSQL volume:
aiscc-p2-3-private-postgres-data-v1

image provenance SHA-256:
e19f2b645aee85878bed7c557064bbbd0be746524f394ad88de1d2509c13b64f

DB provenance SHA-256:
36b9c93515223ade3d74923141fcbe823907b42b81e5d86bf3666a4f02032b54
```

Require:

```text
no Stockroom runtime container
no private runtime root
no S1 domain state
```

Do not rerun migrations, restart PostgreSQL, rebuild image, or execute Stockroom.

# 10. repository post-cleanup gate

Require:

```text
HEAD/tree:
unchanged

index:
empty

tracked worktree:
clean

source/config/test/example:
unchanged

canonical state:
unchanged

candidate provenance JSON bytes:
unchanged
```

No Git add/commit/push.

# 11. cleanup contract review

Require all:

```text
SAME_EXECUTOR_SESSION_AUTHORITY_AVAILABLE
PRE_CLEANUP_RETAINED_ENVIRONMENT_EXACT
BUILD_CONTEXT_OWNERSHIP_EXACT
BUILD_CONTEXT_FINGERPRINT_EXACT
TEMP_HELPER_OWNERSHIP_EXACT
BUILD_CONTEXT_TEMP_REMOVED
TEMP_HELPERS_REMOVED
PASSWORD_FILE_RETAINED_UNTOUCHED
STOCKROOM_IMAGE_RETAINED_EXACT
POSTGRES_RETAINED_EXACT
CANDIDATE_PROVENANCE_RETAINED_EXACT
NO_RUNTIME_EXECUTION
NO_S1
NO_SOURCE_STATE_MUTATION
NO_GIT_PERSISTENCE
```

Require:

```text
15 / 15 PASS
```

# 12. final Git-visible state

Before current Task movement:

```text
Git-visible:
16 exact
index empty
```

Move current Task byte-identically:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
→
.aiassistant/tasks/done/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
```

Final:

```text
Git-visible:
17 exact
index empty
```

Exact final set:

```text
.aiassistant/records/aiscc/cycles/20260912_0259_aiscc-p2-3-cut-a-persisted-cut-b-environment-provisioning-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_0259_aiscc-p2-3-cut-a-persistence-final-acceptance-cut-b-authorization-judgment-1.md
.aiassistant/tasks/done/20260912_0259_aiscc-p2-3-private-s1-cut-b-environment-provisioning-1.md
.aiassistant/records/aiscc/cycles/20260912_0348_aiscc-p2-3-cut-b-artifact-hash-correction-provisioning-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_0348_aiscc-p2-3-cut-b-artifact-hash-contract-defect-retry-judgment-1.md
.aiassistant/tasks/done/20260912_0348_aiscc-p2-3-private-s1-cut-b-artifact-hash-correction-provisioning-retry-1.md
.aiassistant/records/aiscc/cycles/20260912_0410_aiscc-p2-3-cut-b-self-reference-corrected-provisioning-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_0410_aiscc-p2-3-cut-b-self-reference-contract-defect-retry-judgment-1.md
.aiassistant/tasks/done/20260912_0410_aiscc-p2-3-private-s1-cut-b-self-reference-correction-provisioning-retry-1.md
.aiassistant/records/aiscc/cycles/20260912_0420_aiscc-p2-3-cut-b-clean-authority-provisioning-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_0420_aiscc-p2-3-cut-b-historical-baseline-path-mismatch-retry-judgment-1.md
.aiassistant/tasks/done/20260912_0420_aiscc-p2-3-private-s1-cut-b-clean-authority-provisioning-retry-1.md
.aiassistant/records/aiscc/runtime/stockroom-image-provenance.v1.json
.aiassistant/records/aiscc/runtime/stockroom-private-postgres-provisioning.v1.json
.aiassistant/records/aiscc/cycles/20260912_1400_aiscc-p2-3-cut-b-provisioned-candidate-temporary-cleanup-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_1400_aiscc-p2-3-cut-b-provisioning-candidate-cleanup-hold-judgment-1.md
.aiassistant/tasks/done/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
```

# 13. required export

Folder:

```text
.aiassistant/reports/target/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
CLEANUP_AUTHORITY_VERIFICATION.md
TEMP_CONTEXT_VERIFICATION.md
TEMP_HELPER_VERIFICATION.md
RETAINED_ENVIRONMENT_VERIFICATION.md
SECRET_BOUNDARY_VERIFICATION.md
CONTRACT_REVIEW.md
```

Also include byte-preserving:

```text
current Cycle
current Judgment
current done Task
.aiassistant/records/aiscc/runtime/stockroom-image-provenance.v1.json
.aiassistant/records/aiscc/runtime/stockroom-private-postgres-provisioning.v1.json
```

Expected:

```text
10 root docs
5 canonical/candidate copies
15 members total
```

`EXPORT_MANIFEST.md` covers all 14 non-self entries with SHA-256 and byte size.

Secret/path scan must reject:

```text
private password value
database URL
private password host path
literal temporary build-context path
literal temporary helper host paths
```

Create adjacent verified ZIP:

```text
one top-level directory
15 exact members
CRC PASS
folder/archive byte equality
```

# 14. success ceiling

Success:

```text
Cut B temporary cleanup:
PASS

Cut B provisioning candidate:
COMPLETE / READY_FOR_BROWSER_FINAL_ADMISSION

Cut B persistence:
NOT_AUTHORIZED

Cut C:
NOT_AUTHORIZED

private S1:
NOT_AUTHORIZED

P2-3:
IN_PROGRESS
```
