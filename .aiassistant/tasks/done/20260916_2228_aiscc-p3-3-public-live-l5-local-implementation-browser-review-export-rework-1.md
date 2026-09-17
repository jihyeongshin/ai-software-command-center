# 작업지시서: P3-3 L5 Local Implementation Browser-Review Export Rework

## meta

- task_id: `20260916_2228_aiscc-p3-3-public-live-l5-local-implementation-browser-review-export-rework-1`
- created_at: `2026-09-16 KST`
- work_type: `SOURCE_EVIDENCE_EXPORT`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_HEAD: `96a4029ec3a82c9b2a88b9718732aa0f00ecad20`
- predecessor_result_zip_sha256: `d442db35d4745521f975e7234f3696addee5fb6b48fbd000b9c1931b92d8861d`
- product_mutation: `FORBIDDEN`

Use the current IDE Executor conversation. No fresh chat is required.

## blocker being repaired

The 2148 implementation result is not substantively rejected.

Browser review is blocked because the uploaded result ZIP omitted:

1. `EXPORT_MANIFEST.md`;
2. canonical `TASK.md`;
3. all 12 changed source/test files.

The canonical export rule requires changed product/governance/config files in the target bundle preserving project-relative paths.

This Task repairs only that export contract.

## preflight

Verify:

```text
HEAD == 96a4029ec3a82c9b2a88b9718732aa0f00ecad20
index == empty
```

The 12 changed source/test files must still exist with the exact prior SHA-256 values below.

- `src/aiscc/__main__.py` — `7ff93d25c21191aa106a1118eba3ff3332856f2f6030e2e9de2d5eb3c0aaf1dd`
- `src/aiscc/providers/openai_responses.py` — `48d46fd7d1aa859b45ac34f5e7ac6aab5707fac25136acdd86d8512de844044d`
- `src/aiscc/public_live/edge_identity.py` — `c653709cd80da0aa819734b2d21c67bf12c5778f4fb089efd64b8855f8ded871`
- `src/aiscc/public_live/hosted_proof.py` — `dae40ef65220eaf89ce59a43ecc91eea4300765a85b3904fd55e6b635a91df1f`
- `src/aiscc/public_live/http.py` — `7dab6c843bb5867fca5102a986246d6a0170d332913f73e72f5cd127f2276232`
- `src/aiscc/public_live/ingress.py` — `f088266649891499519a08d30948c4b3d32e2a857132fd71f00074152c69a4e8`
- `src/aiscc/public_live/source.py` — `47d10c6d0f0996124c0175add933d5cf4115d8dfc7633e52384850d82f3c6d6a`
- `src/aiscc/public_live/worker.py` — `1d07167f3c471316a288ebe91bea1efb9e8bf4dd7034ca81f09df85867a92983`
- `tests/integration/public_live/test_hosted_binding.py` — `3f1ad44f2f912bcc71116df991bb43a827fcf9155c5750d16cfe890fbf45310c`
- `tests/unit/providers/test_openai_responses.py` — `515450a6cf9f150cae3d1c6981fb97b8e6752e69ab865fb7045c31e6c53a0372`
- `tests/unit/public_live/test_edge_identity.py` — `e6dae7e9fda5a2ba1423a2957aabc13c87801ed73a5c8afa5cec16e4cb89da89`
- `tests/unit/public_live/test_hosted_binding.py` — `c775816a00a061d462a80657956bdf2e3a5b1173bd08a6e1229082c07c7f732d`

If any path is missing or any SHA differs:

`SOURCE_EVIDENCE_IDENTITY_MISMATCH`

and STOP.

Do not modify the file to make the hash match.

## exact export authorization

Byte-preserving export is authorized for exactly those 12 files.

Preserve project-relative paths at ZIP root, for example:

```text
src/aiscc/public_live/ingress.py
tests/unit/public_live/test_hosted_binding.py
```

Do not flatten filenames.

Do not export any other source file.

## replacement bundle

Create a new replacement Browser-review bundle.

Required at ZIP root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
SOURCE_INVENTORY.json
BINDING_IMPLEMENTATION_AUDIT.md
INGRESS_ROUTE_PROOF.md
IDENTITY_AUTHORITY_PROOF.md
EGRESS_MEDIATION_PROOF.md
SUPERVISOR_PROOF.md
SECRET_NON_EXPOSURE_PROOF.md
REPLAY_INDEPENDENCE_PROOF.md
LOCAL_START_COMMANDS.md
TEST_EVIDENCE.json
WORKSPACE_BEFORE.txt
WORKSPACE_AFTER.txt
```

Also include the exact 12 source/test files under their project-relative paths.

### TASK.md

`TASK.md` is the exact copy of this re-export Task.

### EXECUTOR_REPORT.md

This may be a short export-rework report.

It must state:

- predecessor result ZIP SHA `d442db35d4745521f975e7234f3696addee5fb6b48fbd000b9c1931b92d8861d`;
- no implementation mutation;
- 12/12 source identity verification;
- prior proof/test evidence reused unchanged;
- replacement bundle member count;
- product/provider/Railway/Cloudflare/Git actions = 0.

### prior evidence reports

Reuse the evidence files from the prior 2148 target bundle byte-for-byte when available.

Do not rewrite substantive evidence merely to repackage it.

If exact prior evidence files are unavailable locally, STOP with:

`PRIOR_EVIDENCE_ARTIFACT_MISSING`

Do not regenerate them from memory.

### EXPORT_MANIFEST.md

Include:

- task ID;
- predecessor result ZIP SHA;
- HEAD;
- branch;
- index state;
- each included member;
- per-member SHA-256;
- classification (`task`, `report`, `source`, `test`, `evidence`, `workspace`);
- 12/12 source identity result;
- no-secret scan result;
- forbidden external actions count.

## tests

No new product tests are required or authorized.

The existing 2148 test evidence may be reused only because source identity must be 12/12 exact.

Do only packaging/integrity checks:

- file SHA verification;
- ZIP member inventory;
- duplicate path check;
- path traversal check;
- secret scan without printing values;
- `git diff --check` only if it does not modify files.

## forbidden

```text
product/source mutation:
0

test mutation:
0

config/migration mutation:
0

real OpenAI request:
0

real key read/export:
0

Railway mutation/deploy:
0

Cloudflare mutation:
0

Git add/commit/push:
0

Public enable:
0
```

Do not clean unrelated workspace residue as a gate.

## acceptable result

`BROWSER_REVIEW_EXPORT_CONTRACT_RESTORED / SOURCE_IDENTITY_12_OF_12`

This does not accept the implementation. It only restores Browser reviewability.

## export output

Create:

`.aiassistant/reports/target/20260916_2228_aiscc-p3-3-public-live-l5-local-implementation-browser-review-export-rework-1/`

and a ZIP containing the complete replacement bundle above.

## final response

Report only:

1. result;
2. HEAD;
3. predecessor result ZIP SHA;
4. 12/12 source identity;
5. replacement ZIP SHA;
6. member count;
7. prior evidence reuse;
8. product/source/test mutation count;
9. external action count;
10. workspace/index state;
11. Browser review next step.
