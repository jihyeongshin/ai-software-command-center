# 작업지시서: Public Live Canonical Build Manifest EOL Reproducibility Rework

## meta

- task_id: `20260919_2246_aiscc-public-live-canonical-build-manifest-eol-reproducibility-rework-1`
- created_at: `2026-09-19T22:46:00+09:00`
- work_type: `NARROW_REWORK / PUBLIC_ARTIFACT_PROVENANCE`
- evidence_profile: `HIGH_RISK`
- exact_baseline: `3178179986975709f4acec11825fc736cd3ce7c1`
- predecessor_implementation_commit: `f9bb6a5a9de35a8abd6d5b39acb17af4b6add80b`
- fresh_ide_chat_required: `No`
- L8_status: `CLOSED / MUST_REMAIN_CLOSED`
- Public_Live_entry_state: `RELEASED`
- migration_head: `20260919_0028`
- public_run_authority: `NONE`
- real_provider_call_authority: `NONE`
- DB_migration_authority: `NONE`
- ingress_source_change_authority: `NONE`
- worker/provider/admission_change_authority: `NONE`
- frontend_functional_trace_change_authority: `NONE`
- public_build_provenance_change_authority: `YES / NARROW`
- Git_EOL_policy_change_authority: `YES / NARROW`
- Cloudflare_redeploy_authority: `YES / ONLY_IF_NEEDED_TO_ALIGN_CANONICAL_ARTIFACT`
- public_control_mutation_authority: `NONE_UNLESS_SECURITY_SAFETY_REQUIRES_FAIL_CLOSED`
- Human_QA: `HOLD / AFTER_BROWSER_ACCEPTANCE`

## Goal

Close only:

`PUBLIC_REPLAY_BUILD_MANIFEST_CANONICAL_EOL_DRIFT`

without reopening the accepted trace implementation.

## exact defect

Current committed manifest records:

```text
_headers:
484 bytes

live-config.json:
158 bytes
```

Current canonical Git blobs at baseline are:

```text
public/replay/_headers
Git blob:
1ef1bf7fd9533a6a97b338152538f89851f42ad7
bytes:
477
SHA-256:
fd3158e83462fb5db5ed3b17328bc39e5baae132e2e3f62fd01989fe9a1a7b64

public/replay/live-config.json
Git blob:
0d92fa4aa673c45c8a338dd9d4ff70520f337155
bytes:
153
SHA-256:
9a14186fe2179374e25d6c198f34db2d5338cc13307558f8e2c2ef6c9c30d676
```

The difference is consistent with CRLF working-tree bytes being hashed by `scripts/build_public_replay.py`.

## mandatory preflight

Verify:
- `HEAD == origin/main == 3178179986975709f4acec11825fc736cd3ce7c1`;
- implementation commit `f9bb6a5a9de35a8abd6d5b39acb17af4b6add80b` is ancestor;
- migration 0028 remains hosted head;
- Public Live remains RELEASED;
- control remains true;
- frontend Live remains enabled;
- no unexpected active/held/claim/pin state;
- no new run/provider call since predecessor evidence;
- current trace implementation source unchanged.

If current main or functional source has drifted, STOP with:

`CANONICAL_EOL_REWORK_BASELINE_DRIFT`

## source audit

Read:
- `.aiassistant/rules/AISCC_ASSET_GIT_AND_ENCODING_POLICY.md` or the current canonical equivalent;
- `scripts/build_public_replay.py`;
- current `.gitattributes` if any;
- `public/replay/PUBLIC_REPLAY_BUILD_MANIFEST.json`;
- `public/replay/_headers`;
- `public/replay/live-config.json`;
- changed trace assets;
- directly affected public replay build tests.

## allowed paths

- `.gitattributes` if required;
- `scripts/build_public_replay.py` only if a narrow deterministic-EOL fix is necessary;
- `public/replay/PUBLIC_REPLAY_BUILD_MANIFEST.json`;
- directly affected public replay deterministic-build tests;
- governance lifecycle files.

Do not functionally edit:
- `public/replay/assets/app.js`;
- `public/replay/assets/styles.css`;
- `public/replay/live-config.json` values;
- `public/replay/_headers` security policy content.

Line-ending rewrite to LF is allowed and should not alter canonical Git content.

## preferred solution

Use Git-level EOL policy to make authored public Replay text assets LF on Windows and Linux.

Prefer explicit text patterns if `public/replay/**` could contain binary files.

Example direction, not mandatory literal form:

```gitattributes
public/replay/*.html text eol=lf
public/replay/*.json text eol=lf
public/replay/_headers text eol=lf
public/replay/assets/*.js text eol=lf
public/replay/assets/*.css text eol=lf
```

If an existing canonical encoding policy prescribes a different exact mechanism, follow that policy.

Do not make CRLF the canonical artifact.

## manifest repair

After working-tree LF is guaranteed:

1. regenerate the public Replay build manifest;
2. require manifest entries for `_headers` and `live-config.json` to match canonical Git bytes;
3. cross-check all authored static assets against canonical Git blob bytes;
4. ensure no functional trace/config/security content changes.

Expected corrected cross-check:

```text
_headers:
477 bytes
SHA-256 fd3158e83462fb5db5ed3b17328bc39e5baae132e2e3f62fd01989fe9a1a7b64

live-config.json:
153 bytes
SHA-256 9a14186fe2179374e25d6c198f34db2d5338cc13307558f8e2c2ef6c9c30d676
```

If actual canonical Git content changes for an authorized reason, do not force these copied values; prove the new canonical bytes instead.

## deterministic clean-checkout proof

Required.

Prove from a disposable clean Git checkout/worktree at the final candidate commit that:

```text
python/uv <public replay builder> --check
PASS
```

and that:
- generated/checked manifest is byte-identical to committed manifest;
- authored static asset byte sizes/hashes match canonical Git blobs;
- no CRLF/LF-dependent drift exists.

The clean proof must not reuse the dirty development working tree as its only evidence.

## regression tests

Run:
- deterministic public replay build tests;
- trace frontend source tests;
- Node syntax check;
- `git diff --check`;
- repository encoding/EOL policy checks if available.

No provider/DB/runtime regression suite is required because backend/runtime code is not changing.

## deployment

If the currently deployed Cloudflare artifact was uploaded from CRLF working-tree bytes, redeploy the exact LF canonical frontend artifact after the fix.

If independent deployment evidence proves the active artifact already equals canonical LF bytes, redeploy is not required.

Either way prove:
- public site reachable;
- Live remains configured/enabled;
- exact ingress origin/CSP unchanged in meaning;
- Recorded Replay remains available;
- no new run;
- no provider call.

Do not redeploy Railway ingress/worker for this rework.

## Git rules

- fast-forward only;
- no amend/rebase/force;
- current implementation history preserved.

Expected narrow commit content:
- EOL policy file if needed;
- corrected manifest;
- narrow deterministic test/build helper only if needed;
- governance.

Do not touch migration 0028 or trace functional source unless a mandatory stop identifies a separate defect.

## acceptance

Required:

```text
CANONICAL_PUBLIC_BUILD_MANIFEST_REPRODUCIBLE
/
TRACE_IMPLEMENTATION_UNCHANGED
/
PUBLIC_LIVE_RELEASED
/
NEW_RUN_0
/
PROVIDER_CALL_0
/
HUMAN_TRACE_QA_PENDING
/
BROWSER_REVIEW_REQUIRED
```

## stop conditions

- functional trace source must change to fix EOL;
- migration/DB change appears necessary;
- deployed release meaning changes;
- canonical encoding policy conflicts with proposed EOL rule;
- clean checkout still differs from committed manifest;
- asset hash differs without an explained authorized source change.

Use exact blocker:
`PUBLIC_REPLAY_CANONICAL_BUILD_REPRODUCIBILITY_NOT_CLOSED`

## required export

Create:

`.aiassistant/reports/target/20260919_2246_aiscc-public-live-canonical-build-manifest-eol-reproducibility-rework-1/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `BASELINE_REPRODUCTION.md`
- `CANONICAL_GIT_BLOB_PROOF.md`
- `EOL_POLICY.md`
- `CLEAN_CHECKOUT_BUILD_PROOF.md`
- `CORRECTED_BUILD_MANIFEST_PROOF.md`
- `TRACE_IMPLEMENTATION_UNCHANGED.md`
- `PUBLIC_RELEASE_STATE.md`
- `DEPLOYMENT_ALIGNMENT.md`
- `WORKSPACE_STATE.md`
- changed files preserving exact Git blob bytes.

Export manifest must include per-file:
- repository path;
- byte length;
- Git blob SHA-1;
- SHA-256.

Do not repeat the predecessor manifest format that only listed paths.

## final response format

1. result
2. target ZIP path/SHA-256
3. exact baseline/final commit
4. reproduced defect
5. EOL policy fix
6. corrected canonical asset sizes/hashes
7. clean checkout proof
8. tests/static
9. deployment alignment
10. Public Live final state
11. new run/provider call counts
12. changed files
13. Git blob/export identity
14. Human QA status
15. blockers/unverified
