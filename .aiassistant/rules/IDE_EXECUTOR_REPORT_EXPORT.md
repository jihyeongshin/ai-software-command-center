# AISCC Repository Canonical Metadata

- canonical_owner: `AISCC_REPOSITORY`
- authority: `REPOSITORY_LOCAL_CANONICAL`
- bootstrap_origin: `AISCC-BOOTSTRAP-SEED-V1`
- canonicalized_by_task: `20260826_1108_aiscc-p0-4-canonical-authority-metadata-and-post-bootstrap-state-normalization-rework-2`

---


# AISCC IDE Executor Report and Export

## 1. 목적

IDE Executor의 Task lifecycle, temporary export bundle, evidence reporting, final response를 고정한다.

## 2. 경로 의미

- `.aiassistant/tasks/active/*.md`: 실행 중 임시 Task File; Git ignore
- `.aiassistant/tasks/done/*.md`: executor turn 제출 준비 완료 Task; Git track; command-center accepted 의미 아님
- `.aiassistant/reports/target/<timestamp>_<slug>/`: temporary Command Center review bundle; Git ignore
- `.aiassistant/reports/aiscc/`: curated baseline/handoff/reference만 Git track
- `.aiassistant/records/aiscc/cycles/`: terminal judgment와 public provenance; Git track
- `.aiassistant/project-sources/manifests/`: mirror definition; Git track
- `.aiassistant/project-sources/bundles/`: generated upload copy; Git ignore

## 3. Task filename

```text
.aiassistant/tasks/active/YYYYMMDD_HHmm_<safe-slug>.md
```

- KST 또는 프로젝트가 명시한 단일 timezone
- ASCII lowercase/digit/hyphen safe slug
- lexicographic sort가 생성 순서를 보존
- 기존 파일을 임의 rename하지 않음

## 4. target bundle naming

```text
.aiassistant/reports/target/YYYYMMDD_HHmm_<safe-slug>/
```

Task stem과 가능한 한 맞춘다.

## 5. 기본 report 저장

기본 report는 ephemeral이다.

```text
.aiassistant/reports/target/<...>/EXECUTOR_REPORT.md
```

Task가 canonical report를 명시할 때만 `.aiassistant/reports/aiscc/`에도 작성한다.

canonical report 후보:

- accepted architecture/design audit
- security baseline
- orchestration contract
- release-readiness audit
- repeat-use handoff
- competition submission baseline

## 6. target bundle 필수 구성

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- changed product/governance/config files preserving project-relative paths
- deletion이 있을 때만 `REMOVED_FILES.md`

chat-only 작업은 `TASK.md`를 생략할 수 있으나 manifest에 `task_file: chat-only`를 기록한다.

## 7. task lifecycle

```text
.tasks/active/<task>
→ executor-required work/report/export complete
→ .tasks/done/<task>
```

`done` 의미:

- executor turn 제출 준비 완료
- accepted가 아님
- blocked/failed/rejected-candidate도 report/export가 완성되면 done 가능
- reject 후 old task를 active로 되돌리지 않고 새 timestamp rework task 발행

이동 금지:

- executor-required proof 미완료인데 같은 turn을 계속해야 함
- human input을 받아 같은 executor turn이 계속되도록 Task가 명시함
- target bundle 미완성

`human_owned = HUMAN_PENDING`만으로 active에 계속 남길 필요는 없다. executor turn이 종료 가능하면 pending을 기록하고 done으로 이동한다.

## 8. deletion

삭제가 있을 때만 target root에 `REMOVED_FILES.md`를 만든다.

삭제가 없으면 deletion guide류 파일을 만들지 않는다.

## 9. export 제외

기본 제외:

- unchanged source
- previous target bundle
- build/cache/IDE artifacts
- private env/credential/token/cookie/private key
- data dump/PII
- generated Project Source bundle
- runtime sandbox residue

## 10. `SOURCE_EVIDENCE_EXPORT` 좁은 예외

unchanged source export는 아래를 모두 만족할 때만 허용한다.

```text
work_type = SOURCE_EVIDENCE_EXPORT
AND explicit Command Center authorization
AND exact file allowlist or accepted resolved manifest
AND read-only review purpose
AND byte-preserving copy
```

필수:

- repository/branch/HEAD/worktree state
- expected/actual file count
- per-file source/copy SHA-256
- project-relative path preservation
- secret scan without printing secret value
- copy 전후 worktree status
- evidence copy를 product change/commit candidate로 분류하지 않음

## 11. evidence reporting

Task contract의 five-way ownership을 그대로 보고한다.

```text
executed
reused
human_pending
human_provided
not_required
forbidden_not_run
blocked_required
```

result classification:

```text
EXECUTED_PASS
EXECUTED_FAIL
REUSED_ACCEPTED
HUMAN_PROVIDED
HUMAN_PENDING
NOT_REQUIRED
FORBIDDEN_NOT_RUN
BLOCKED_REQUIRED_EVIDENCE
```

## 12. scope expansion / mandatory stop

Task가 허용한 changed-path static check와 targeted test는 가능하다.

새 environment/network/browser/credential/full-suite가 필요하면 `EVIDENCE_SCOPE_EXPANSION_REQUIRED`로 중단한다.

named blocker 이후에는 최소 evidence, workspace inventory, report/export, 안전한 종료만 수행한다.

## 13. proof non-substitution / human ownership

- Agent claim을 admitted evidence로 자동 승격하지 않는다.
- human-owned evidence를 완료로 표시하지 않는다.
- 서로 다른 proof type을 대체하지 않는다.
- predecessor proof는 Task가 재사용을 허용하고 applicability가 맞을 때만 사용한다.

## 14. report 필수 항목

- task/work type/task path
- read canonical paths
- source inventory
- workspace before/after
- product source changes
- governance/provenance changes
- repository configuration changes
- added/modified/removed files
- Task evidence contract
- actual evidence classification
- Agent claim vs admitted evidence when applicable
- human pending/provided
- mandatory stop/scope expansion
- conformance when required
- state transition trace when self-dogfooding
- security/sandbox result when applicable
- UTF-8/Markdown/control-character validation
- unverified items
- rollback/revert guide
- preserved exact paths
- next turn recommendation

## 15. artifact preservation

최종 응답과 report에는 cleanup 이후에도 남겨야 하는 artifact를 exact path로 적는다.

일반적으로 보존:

- `.aiassistant/tasks/done/<task>.md`
- `.aiassistant/records/aiscc/cycles/<cycle>.cycle.md` — Command Center가 생성
- accepted canonical baseline/handoff

명시하지 않은 target bundle은 판정 후 삭제 가능하다.

## 16. Git / commit / deployment

Task가 exact action을 명시하지 않으면 다음을 수행하지 않는다.

- `git add`
- `git commit`
- `git push`
- PR merge
- package publish
- deployment
- Browser Project Source upload

## 17. final response

1. result: completed / blocked / rejected-candidate
2. target bundle path
3. changed files
4. removed files
5. human verification
6. unverified items
7. preserved exact paths

장문 report는 chat에 붙이지 않는다.
