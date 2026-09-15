# 작업지시서: P3-3 final submission canonical encoding restoration corrected retry

## meta

- task_id: `20260915_1545_aiscc-p3-3-final-submission-canonical-encoding-restoration-corrected-retry-1`
- created_at: `2026-09-15T15:45:38+09:00`
- work_type: `DOCUMENT_ENCODING_REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- fresh_ide_chat_required: `No`

## objective

Retry the already-authorized three-document encoding restoration.

The 1540 attempt stopped only because the Browser Task contained a 63-character typo in one expected SHA-256.

Do not broaden scope.

## repository baseline

Before delivery transport, expected:

```text
branch = main
HEAD = cdba43927490de1a9ecfc2d71e1312d01111cd11
index = empty
tracked worktree = clean
```

Expected Git-visible untracked is exactly these four predecessor governance paths:

- `.aiassistant/records/aiscc/cycles/20260915_1540_aiscc-p3-3-final-submission-persistence-accepted-document-encoding-rework-entry-1.cycle.md`
  - SHA-256 `984bfb82b9d9bf1ba77121cca6708d47d312dc0778d6e624fadd70ebf2b40c64`
- `.aiassistant/reports/aiscc/20260915_1540_aiscc-browser-command-center-p3-3-post-submit-window-encoding-restoration-entry-handoff-1.md`
  - SHA-256 `e2273720b1458a749bbf0f1f3fc59be6ec2b03d0a6e09c2d5cd5aba12e5a7e9b`
- `.aiassistant/reports/aiscc/20260915_1540_aiscc-p3-3-final-submission-persistence-document-encoding-browser-judgment-1.md`
  - SHA-256 `37b9ea5581c3012ea0a2bc1d5f936d35acf6ef4735dafaf5060b622feed05d8d`
- `.aiassistant/tasks/done/20260915_1540_aiscc-p3-3-final-submission-canonical-korean-encoding-restoration-rework-1.md`
  - SHA-256 `3831db10691e65b092afb39200b1bc5a07028311f526b2c0808a3e22b47ccb2c`

Any path/hash mismatch or extra unexplained dirt => STOP.

Do not clean/delete/reset them.

After this delivery is placed, the new Cycle/Judgment/Handoff are additionally authorized provenance; active Task follows normal ignored-task lifecycle.

Run before edits:

```text
python scripts/build_public_replay.py --check
```

PASS required.

## exact current hashes of the three defective tracked documents

### final submission confirmation

```text
path:
.aiassistant/reports/aiscc/AISCC_COMPETITION_FINAL_SUBMISSION_CONFIRMATION.md

SHA-256:
29bc776b70afd6c31713a67640e3737a2b34433e5faa0304e6a1b28cb3506c1d
```

### competition submission package

```text
path:
.aiassistant/reports/aiscc/AISCC_COMPETITION_SUBMISSION_PACKAGE.md

SHA-256:
24f755577f11bd0a94eb3e03e86f130eed2e26f803e2439b611d10d8701e4658
```

### disclosure register

```text
path:
.aiassistant/reports/aiscc/AISCC_PUBLIC_RELEASE_DISCLOSURE_REGISTER.md

SHA-256:
fb5ffc91a854f901773205e8fa1e8c8f6ae87cfe1a4912691a15c4622767acb8
```

All three exact matches are mandatory.

## repair A — final submission confirmation

Replace the entire file with this UTF-8 Korean-first content:

```markdown
# AISCC 대회 최종 제출 확인

대회: Wanted AI Championship 2026.

제출 상태: `HUMAN_PROVIDED / COMPLETED` — Browser가 Human 제출 증거를 확인했다.

Browser 증거 수신/판정 시각: `2026-09-15T15:27:46+09:00`.

실제 플랫폼 submission timestamp: `NOT_SHOWN`.
제공된 화면에는 플랫폼의 정확한 제출 완료 시각이 표시되지 않았으므로 추측하지 않는다.

제출 제목:

`AI Software Command Center — AI 개발 작업을 증거로 통제하는 소프트웨어 거버넌스 콘솔`

서비스 URL:

`https://aiscc-replay.pages.dev`

Predefined AI tag:

`ChatGPT`

Narrative AI tools:

`ChatGPT`, `Codex`

## Human 증거 identity

| 증거 | SHA-256 |
| --- | --- |
| Wanted `내 과제` 화면 | `6213051a242bc8421b1d7e6435920b5149a38ecf748bc9ce5d492ebe631a5d10` |
| Wanted submitted detail 화면 | `088d9986c645fb279f95e8ac64d222e262cae108c0940dcd090c949dd7cd3fdd` |

Browser는 현재 대화에 업로드된 두 이미지의 SHA-256을 위 값과 exact match로 재확인했다.
Screenshot binary 자체는 repository에 포함하지 않는다.

## 제출 이후 상태

Human UI에서 2026-09-20 제출 마감 전까지 수정 가능하고, 마감 이후에는 수정할 수 없고 열람만 가능하다는 안내를 확인했다.

따라서 현재 P3-3 상태는:

```text
SUBMITTED / POST_SUBMISSION_IMPROVEMENT_WINDOW
```

이며 `CLOSED`가 아니다.

마감 전 public experience를 materially 변경할 경우에는 제출 상태와 서비스의 정합성을 다시 검토해야 한다.
마감 이후에는 제출 경험을 동결하고 심사 기간 동안 public Replay 접근 가능성을 유지해야 한다.

## 현재 public release

```text
Public Replay:
DEPLOYED / PUBLIC_VERIFICATION_PASSED / HUMAN_ACCEPTED

Public Bounded Live:
NOT_RELEASED / DISABLED_FOR_INITIAL_RELEASE
```

Live 구현 또는 공개 여부는 이 제출 완료 사실로 자동 승인되지 않는다.
추가 작업은 별도 Task와 Human 판단으로 수행한다.

## claim boundary

이 기록은 다음만 증명한다.

- Human이 최종 제출을 완료했고 Browser가 제공된 화면 증거를 확인했다.
- 제출된 프로젝트가 `내 과제`와 상세 화면에 존재한다.
- 위 service URL과 AI tool disclosure가 제출 상태에 포함되어 있다.

다음은 증명하지 않는다.

- 플랫폼의 정확한 제출 완료 시각
- 향후 uptime
- Public Bounded Live의 구현 또는 공개
- 대회 심사 결과
- 일반적인 성능 우월성

```

Validation:

- UTF-8 decode PASS
- Korean Unicode code point count > 0
- literal ASCII `?` count = 0
- U+FFFD count = 0

## repair B — competition submission package

Preserve the document except the corrupted submitted-title line.

Replace:

```text
Submitted title: AI Software Command Center ? AI ?? ??? ??? ???? ????? ???? ??.
```

with:

```text
Submitted title: AI Software Command Center — AI 개발 작업을 증거로 통제하는 소프트웨어 거버넌스 콘솔
```

No other semantic rewrite.

After repair:

- literal ASCII `?` count = 0
- U+FFFD count = 0
- UTF-8 decode PASS

## repair C — disclosure register

Preserve the document except the corrupted Human model-context line.

Replace it with exactly:

```text
Human-provided model context: ChatGPT: GPT-5.6 Sol; Codex: GPT-5.6 Sol and GPT-6 Astra. Low / Medium / High describe reasoning/thinking effort, not model names. These are Human context, not a reconstructed per-call audit or a claim that the Wanted form required model/version disclosure.
```

After repair:

- literal ASCII `?` count = 0
- U+FFFD count = 0
- UTF-8 decode PASS
- no authority/status semantic change

## lifecycle

Current Task:

`.aiassistant/tasks/active/20260915_1545_aiscc-p3-3-final-submission-canonical-encoding-restoration-corrected-retry-1.md`

Before final staging move to:

`.aiassistant/tasks/done/20260915_1545_aiscc-p3-3-final-submission-canonical-encoding-restoration-corrected-retry-1.md`

Current Cycle:

`.aiassistant/records/aiscc/cycles/20260915_1545_aiscc-p3-3-encoding-rework-base-hash-contract-corrected-retry-entry-1.cycle.md`

Current Judgment:

`.aiassistant/reports/aiscc/20260915_1545_aiscc-p3-3-encoding-rework-base-mismatch-browser-judgment-1.md`

Current Handoff:

`.aiassistant/reports/aiscc/20260915_1545_aiscc-browser-command-center-p3-3-encoding-restoration-corrected-retry-entry-handoff-1.md`

The four 1540 predecessor governance files already present in the repository MUST also be staged unchanged.

## exact commit candidate

Expected changed path count:

```text
11
```

Composition:

```text
3 repaired pre-existing canonical documents
4 pre-existing 1540 governance provenance paths
4 current 1545 lineage paths
```

Target/export artifacts MUST NOT be staged.

## commit message

Use exactly:

```text
fix(aiscc): restore submission document encoding
```

## forbidden

Do NOT:

- revert `cdba43927490de1a9ecfc2d71e1312d01111cd11`;
- modify public/replay/**;
- modify CURRENT_STATE_SUMMARY.md;
- modify NEXT_ACTIONS.md;
- modify release manifest/readiness;
- modify DECISION_REGISTER.md;
- change submission state;
- use network;
- access Wanted/Cloudflare;
- deploy/redeploy;
- repeat Human QA;
- enable Live;
- push/tag/release.

## validation before commit

Require:

- exact baseline and four predecessor provenance hashes PASS;
- exact three defective document hashes PASS;
- builder `--check` PASS;
- only the three authorized tracked docs modified;
- 1540 provenance bytes unchanged;
- current Cycle/Judgment/Handoff match delivery bytes;
- current Task at done path;
- repaired UTF-8 and replacement-character checks PASS;
- staged path set = exact 11;
- `git diff --cached --check` PASS with accepted CRLF-aware procedure if required.

## postcommit validation

Require:

```text
parent = cdba43927490de1a9ecfc2d71e1312d01111cd11
changed_path_count = 11
changed_path_set = exact allowlist

index = empty
tracked worktree = clean
Git-visible untracked = 0

python scripts/build_public_replay.py --check = PASS
public/replay/** unchanged
```

Reopen committed versions of the three repaired docs and repeat:

- UTF-8 decode
- literal `?` count = 0
- U+FFFD count = 0
- Korean codepoint presence in final-submission report
- exact submitted title
- exact model-context line.

## result classification

Success:

```text
PERSISTENCE_CANDIDATE / POST_SUBMISSION_IMPROVEMENT_WINDOW
```

Do not mark P3-3 CLOSED.

## export

Target:

`.aiassistant/reports/target/20260915_1545_aiscc-p3-3-final-submission-canonical-encoding-restoration-corrected-retry-1/`

Required:

- EXPORT_MANIFEST.md
- TASK.md
- EXECUTOR_REPORT.md
- BASELINE_PROVENANCE.json
- ENCODING_REPAIR_VERIFICATION.json
- STAGED_COMMIT_MANIFEST.json
- POSTCOMMIT_VERIFICATION.json
- TERMINAL_WORKSPACE.json
- repaired three canonical documents
- predecessor 1540 provenance
- current lineage

Terminal ZIP:

`.aiassistant/reports/target/20260915_1545_aiscc-p3-3-final-submission-canonical-encoding-restoration-corrected-retry-1.zip`
