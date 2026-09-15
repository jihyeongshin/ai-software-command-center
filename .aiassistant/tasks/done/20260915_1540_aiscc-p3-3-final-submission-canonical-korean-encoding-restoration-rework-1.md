# 작업지시서: P3-3 final submission canonical Korean encoding restoration rework

## meta

- task_id: `20260915_1540_aiscc-p3-3-final-submission-canonical-korean-encoding-restoration-rework-1`
- created_at: `2026-09-15T15:40:54+09:00`
- work_type: `DOCUMENT_ENCODING_REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- fresh_ide_chat_required: `No`

## objective

Repair only the canonical document encoding defects introduced in commit `cdba43927490de1a9ecfc2d71e1312d01111cd11`.

Do not undo or reperform any accepted P3-3 submission/deployment work.

## required baseline

```text
branch = main
HEAD = cdba43927490de1a9ecfc2d71e1312d01111cd11
index = empty
tracked worktree = clean
Git-visible untracked = 0
```

Mismatch => STOP.

Before mutation verify exact current SHA-256:

```text
.aiassistant/reports/aiscc/AISCC_COMPETITION_FINAL_SUBMISSION_CONFIRMATION.md
29bc776b70afd6c31713a67640e3737a2b34433e5faa0304e6a1b28cb3506c1

.aiassistant/reports/aiscc/AISCC_COMPETITION_SUBMISSION_PACKAGE.md
24f755577f11bd0a94eb3e03e86f130eed2e26f803e2439b611d10d8701e4658

.aiassistant/reports/aiscc/AISCC_PUBLIC_RELEASE_DISCLOSURE_REGISTER.md
fb5ffc91a854f901773205e8fa1e8c8f6ae87cfe1a4912691a15c4622767acb8
```

Any mismatch => STOP `ENCODING_REWORK_BASE_MISMATCH`.

Run:

```text
python scripts/build_public_replay.py --check
```

PASS required.

## allowed canonical modifications

Exactly these three pre-existing tracked paths:

1. `.aiassistant/reports/aiscc/AISCC_COMPETITION_FINAL_SUBMISSION_CONFIRMATION.md`
2. `.aiassistant/reports/aiscc/AISCC_COMPETITION_SUBMISSION_PACKAGE.md`
3. `.aiassistant/reports/aiscc/AISCC_PUBLIC_RELEASE_DISCLOSURE_REGISTER.md`

Plus this Task/Cycle/Judgment/Handoff lifecycle.

No other path may change.

## repair 1 — final submission confirmation report

Replace the entire file with the following UTF-8 Korean-first content exactly in meaning and structure.

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

Required encoding validation:

- UTF-8 decode PASS;
- at least one Korean Unicode code point exists;
- literal ASCII `?` count = 0;
- no U+FFFD replacement character;
- no control-character corruption.

## repair 2 — competition submission package

Preserve all content except the one corrupted `Submitted title:` line.

Current corrupted line:

```text
Submitted title: AI Software Command Center ? AI ?? ??? ??? ???? ????? ???? ??.
```

Replace exactly with:

```text
Submitted title: AI Software Command Center — AI 개발 작업을 증거로 통제하는 소프트웨어 거버넌스 콘솔
```

No other semantic rewrite is authorized.

After replacement:

- literal ASCII `?` count in this document = 0;
- UTF-8 Korean title exact;
- all unrelated bytes/lines preserved as far as line-ending normalization policy allows.

## repair 3 — disclosure register

Preserve all content except the corrupted Human model-context separator line.

Replace that line with:

```text
Human-provided model context: ChatGPT: GPT-5.6 Sol; Codex: GPT-5.6 Sol and GPT-6 Astra. Low / Medium / High describe reasoning/thinking effort, not model names. These are Human context, not a reconstructed per-call audit or a claim that the Wanted form required model/version disclosure.
```

Use ASCII colon separators intentionally.

After replacement:

- literal ASCII `?` count in this document = 0;
- no change to confirmation/authority semantics.

## inbound lineage

Canonicalize:

Task active first:

`.aiassistant/tasks/active/20260915_1540_aiscc-p3-3-final-submission-canonical-korean-encoding-restoration-rework-1.md`

Before commit move to:

`.aiassistant/tasks/done/20260915_1540_aiscc-p3-3-final-submission-canonical-korean-encoding-restoration-rework-1.md`

Cycle:

`.aiassistant/records/aiscc/cycles/20260915_1540_aiscc-p3-3-final-submission-persistence-accepted-document-encoding-rework-entry-1.cycle.md`

Judgment:

`.aiassistant/reports/aiscc/20260915_1540_aiscc-p3-3-final-submission-persistence-document-encoding-browser-judgment-1.md`

Handoff:

`.aiassistant/reports/aiscc/20260915_1540_aiscc-browser-command-center-p3-3-post-submit-window-encoding-restoration-entry-handoff-1.md`

## exact commit candidate

Expected changed path count:

```text
7
```

Exact categories:

- 3 repaired canonical documents
- new Task at tasks/done
- new Cycle
- new Judgment
- new Handoff

No target/export artifacts staged.

## commit message

Use exactly:

```text
fix(aiscc): restore submission document encoding
```

## forbidden

Do NOT:

- revert `cdba43927490de1a9ecfc2d71e1312d01111cd11`;
- modify public/replay/**;
- modify CURRENT_STATE_SUMMARY/NEXT_ACTIONS;
- modify release manifest/readiness;
- modify DECISION_REGISTER;
- redeploy;
- access Cloudflare/Wanted/network;
- redo submission/QA;
- enable Live;
- push/tag/release.

## precommit validation

Require:

- exact baseline/path hashes PASS;
- three repaired files UTF-8 PASS;
- literal `?` count = 0 in each repaired file;
- U+FFFD count = 0;
- Korean-first report contains Korean code points;
- submitted title exact;
- model-context line exact;
- only three pre-existing files modified;
- staged path set exact 7;
- `git diff --cached --check` PASS using accepted CRLF-aware process if needed;
- builder `--check` PASS.

## postcommit validation

Verify:

```text
parent = cdba43927490de1a9ecfc2d71e1312d01111cd11
changed_path_count = 7
changed_path_set = exact allowlist
index = empty
tracked worktree = clean
Git-visible untracked = 0
builder --check = PASS
public/replay/** unchanged
```

Also reopen committed bytes and repeat UTF-8 / literal-`?` / U+FFFD checks.

## result classification

Success:

```text
PERSISTENCE_CANDIDATE / POST_SUBMISSION_IMPROVEMENT_WINDOW
```

This is a narrow documentation correction only.

Do not declare P3-3 CLOSED.

## target export

`.aiassistant/reports/target/20260915_1540_aiscc-p3-3-final-submission-canonical-korean-encoding-restoration-rework-1/`

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `ENCODING_DEFECT_BEFORE.json`
- `ENCODING_REPAIR_VERIFICATION.json`
- `STAGED_COMMIT_MANIFEST.json`
- `POSTCOMMIT_VERIFICATION.json`
- `TERMINAL_WORKSPACE.json`
- repaired three canonical documents
- new Task/Cycle/Judgment/Handoff preserving relative paths

Terminal ZIP:

`.aiassistant/reports/target/20260915_1540_aiscc-p3-3-final-submission-canonical-korean-encoding-restoration-rework-1.zip`
