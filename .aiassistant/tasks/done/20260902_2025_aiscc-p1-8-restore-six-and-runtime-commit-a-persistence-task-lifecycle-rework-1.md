# 작업지시서: P1-8 restore six and Runtime Commit A persistence — Task lifecycle destination rework

## meta

- task_id: `20260902_2025_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-task-lifecycle-rework-1`
- created_at: `2026-09-02T20:25:00+09:00`
- project: `AI Software Command Center (AISCC)`
- phase: `P1-8 — Project Memory and Cycle Admission`
- work_type: `REWORK / GIT_TERMINAL_PERSISTENCE`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a — preflight binding only; do not force-reset if current HEAD differs`
- primary_semantic_owner: `P1-8 runtime terminal Git persistence / exact-path restore / Runtime Commit A`
- fresh_chat_policy: `REUSE_CURRENT_1849_FRESH_IDE_SESSION_ALLOWED / NO_NEW_CHAT_REQUIRED`
- fresh_chat_reason: `1849 established the genuinely fresh IDE session; 1849, 1936 and 1942 performed no runtime/index/commit mutation; this Task stays in the same destructive authority class and repairs only the blocked 1942 Task lifecycle before retrying Commit A`
- predecessor_task: `.aiassistant/tasks/active/20260902_1942_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-transport-label-rework-1.md` — blocked lifecycle source; next Task is authorized to move this exact file to its matching done path
- predecessor_judgment_cycle: `.aiassistant/records/aiscc/cycles/20260902_2023_aiscc-p1-8-runtime-commit-a-task-lifecycle-destination-conflict-rework-1.cycle.md`
- continuation_handoff: `.aiassistant/reports/aiscc/20260902_1621_aiscc-browser-command-center-session-handoff-p1-8-runtime-commit-a-fresh-chat-resume-1.md` — retained canonical predecessor; no new Browser Handoff is required for this retry issuance
- target_bundle: `.aiassistant/reports/target/20260902_2025_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-task-lifecycle-rework-1/`

- browser_session_continuation: `HUMAN_PROVIDED — current Browser Command Center continues; 1942 blocked result received substantive judgment and no Browser Handoff is required`
- ide_session_status: `1849 EXECUTED_PASS + 1936/1942 NO-MUTATION BLOCK — current IDE chat remains the genuinely fresh session for this authority class and may be reused`
- superseded_browser_handoff_artifact: `20260902_1759_aiscc-browser-command-center-session-handoff-p1-8-runtime-commit-a-human-fresh-chat-retry-resume-1.md — not required for this same-Browser continuation; do not transport or canonicalize it under this Task`

## 0. Human-provided authority carried into this Task

다음 Human decision은 이미 제공되었으며 이 Task가 새로 판단하거나 확장하지 않는다.

```text
Human P1-8 runtime final review: ACCEPTED
dirty-file disposition: RESTORE_SIX_TO_EXACT_HEAD
```

이 authority의 의미는 다음과 같이 좁다.

1. Human acceptance는 아래 `Accepted 36 runtime identity`에 기록한 exact 36 byte identity에만 적용된다.
2. `RESTORE_SIX_TO_EXACT_HEAD`는 아래 exact six current bytes가 여전히 동일하고 expected HEAD object가 동일할 때만 그 여섯 path의 current worktree bytes를 버릴 수 있다는 뜻이다.
3. broad cleanup, unrelated reset, accepted-36 수정, canonical governance 수정, Commit B, P1 closure 권한이 아니다.
4. 현재 identity가 하나라도 달라졌다면 이전 Human decision을 새 bytes에 자동 적용하지 않는다.

## 1. 현재 기준 상태


1942 Task는 same fresh IDE session에서 실행되었고 exact 1942 Task + 1940 Cycle transport는 PASS했다.

그 뒤 current Task lifecycle destination conflict가 발견되어 runtime mutation 전에 STOP했다.

```text
1942 result:
POLICY_CONFLICT_INVESTIGATION_REQUIRED / TASK_LIFECYCLE_DESTINATION_CONFLICT

restore performed: No
staged paths: 0
Runtime Commit A: NOT_CREATED
```

2023 Command Center judgment:

```text
ACCEPTED_AS_ACCURATE_BLOCKED_RESULT
/ TASK_NOT_COMPLETED
/ TASK_LIFECYCLE_DESTINATION_REWORK_REQUIRED
```

마지막 admitted repository state:

```text
repository: ai-software-command-center
branch: main
HEAD: 1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a
index entries: 0
runtime dirty paths: 42
governance after 1942 transport: 20 Git-visible paths
1942 active Task: EXISTS
1942 correct done Task: ABSENT
Runtime Commit A: NOT_CREATED
```

1942 blocker는 semantic gate 실패가 아니다. Section 9/10 fresh proof는 lifecycle conflict 이후 실행되지 않았다.

1934에서 승인된 corrected semantic gate는 그대로 유지한다.

Human exact-36 acceptance와 `RESTORE_SIX_TO_EXACT_HEAD` authority는 변경되지 않는다.

현재 IDE chat은 1849에서 genuinely fresh session으로 입증됐고 1849/1936/1942 모두 runtime/index/commit mutation이 없었다.
새 IDE chat은 필요하지 않다.

## 2. 이번 턴 목표


1. Downloads의 **신규 2025 Task와 2023 judgment Cycle 두 파일만** exact transport contract에 따라 canonical 위치로 Move한다.
2. transport 직후, blocked predecessor `.aiassistant/tasks/active/20260902_1942_...md`의 exact identity와 matching 1942 done destination noncollision을 확인한다.
3. exact 1942 active Task를 exact matching 1942 done path로 `Move`, not Copy 하여 predecessor lifecycle을 repair한다. 1936 done Task는 절대 overwrite하지 않는다.
4. current fresh IDE session lineage와 local repository branch/HEAD/index/runtime/governance identity를 mutation 전에 재검증한다.
5. exact six current bytes와 expected HEAD bytes가 Human-authorized identity와 일치하는지 검증한다.
6. exact six에 대해 Section 10 corrected semantic-equivalence gate를 current bytes와 exact HEAD bytes로 fresh recomputation한다.
7. 모든 precondition이 PASS일 때만 exact six를 worktree-only로 exact expected HEAD에 restore한다.
8. restore 직후 six가 clean이고 index가 비어 있으며 runtime dirty set이 exact accepted 36인지 검증한다.
9. exact accepted 36 byte identity와 corrected ordinal aggregate를 재검증한다.
10. `git diff --check`와 repository-local Ruff/mypy를 수행한다. 새 install/network는 금지한다.
11. exact accepted 36만 stage하고 staged path/blob set을 재검증한다.
12. Runtime Commit A를 정확히 하나만 생성하고 Commit object/tree/path/blob을 검증한다.
13. Commit A tree에서 exact 36 source copies를 export하고 index empty를 확인한다.
14. current 2025 Task를 **자기 matching 2025 done path**로 Move하고 `COMMIT_A_CREATED / COMMAND_CENTER_REVIEW_REQUIRED`로 종료한다.

## 3. 이번 턴 비목표

- accepted 36 runtime source의 수정 또는 리포맷
- six restore path 외 unrelated worktree cleanup/reset
- canonical state/decision/next-action 문서 갱신
- Commit B
- P1-8 CLOSED 또는 P1 CLOSED 판정
- P2 시작
- Project Source mirror generation/replacement
- `git push`, remote 조회, PR, release, deployment
- browser/runtime/provider/network/credential evidence
- 새 DB/container/full-suite를 만들어 predecessor test evidence를 재생성하는 것
- Git global/user author 설정 변경

## 4. Downloads transport / canonical placement


이번 Downloads transport 대상은 정확히 두 파일뿐이다.

```text
C:\Users\oracl\Downloads\20260902_2025_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-task-lifecycle-rework-1.md
C:\Users\oracl\Downloads\20260902_2023_aiscc-p1-8-runtime-commit-a-task-lifecycle-destination-conflict-rework-1.cycle.md
```

Repository destinations:

```text
Task:
.aiassistant/tasks/active/20260902_2025_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-task-lifecycle-rework-1.md

Cycle:
.aiassistant/records/aiscc/cycles/20260902_2023_aiscc-p1-8-runtime-commit-a-task-lifecycle-destination-conflict-rework-1.cycle.md
```

2023 Cycle expected SHA-256:

```text
353c3dba610320b08979130f0aa17b6e5f39666ba51c3cdebd56a846dd4a8cbf
```

### 4.1 Downloads transport precheck

```text
new Task source: MUST exist
new Task destination: MUST NOT exist
2023 Cycle source: MUST exist
2023 Cycle destination: MUST NOT exist
2023 Cycle source SHA-256: MUST equal 353c3dba610320b08979130f0aa17b6e5f39666ba51c3cdebd56a846dd4a8cbf
```

하나라도 실패하면 두 파일 모두 Move하지 말고 alternate path search 없이
`TRANSPORT_PRECONDITION_FAILED`로 STOP한다.

### 4.2 Downloads transport execution

전체 PASS 후 두 파일만 exact destination으로 `Move`, not Copy 한다.
destination identity와 Downloads source absence를 확인한다.

### 4.3 predecessor 1942 lifecycle repair — explicit new authority

Downloads transport 완료 후 destructive runtime action 전에 다음을 확인한다.

```text
source:
.aiassistant/tasks/active/20260902_1942_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-transport-label-rework-1.md

expected source SHA-256:
95ca0d505509ef3ea60f4e2fc71af73eb09b662c92272c4b5c0a11f1c5f5e279

correct destination:
.aiassistant/tasks/done/20260902_1942_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-transport-label-rework-1.md
```

Required:

- exact source exists
- exact source SHA-256 matches
- correct destination does not exist
- preserved predecessor `.aiassistant/tasks/done/20260902_1936_...md` remains untouched

하나라도 실패하면 1942 lifecycle을 변경하지 말고 runtime mutation 전에
`TASK_LIFECYCLE_REPAIR_PRECONDITION_FAILED`로 STOP한다.

전부 PASS하면 **1942 active Task만** exact matching 1942 done path로 `Move`, not Copy 한다.
post-move source absence, destination identity, 1936 done preservation을 확인한다.

이것은 governance provenance lifecycle repair이며 runtime source/index/commit mutation authority를 확장하지 않는다.

## 5. fresh IDE session precondition


1849 IDE session은 `SESSION_AUTHORITY EXECUTED_PASS`를 얻은 genuinely fresh chat이다.
1936과 1942는 같은 session에서 runtime/index/commit mutation 전에 STOP했다.

```text
NEW CHAT REQUIRED: No
CURRENT FRESH IDE CHAT REUSE: Allowed
```

Pass condition:

- current conversation lineage가 1849→1936→1942 fresh-session chain과 일치
- 1942 이후 Task 밖 runtime/index/commit mutation evidence 없음
- 신규 2025 Task를 새로운 execution authority로 명시적으로 읽음

충돌 시 mutation 전에:

```text
BLOCKED_REQUIRED_EVIDENCE / SESSION_LINEAGE_CONFLICT
```

## 6. 읽을 문서 — minimum authoritative context set


transport 후 exact path로 읽는다.

Core rules:

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`

Current Task / judgment:

- `.aiassistant/tasks/active/20260902_2025_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-task-lifecycle-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260902_2023_aiscc-p1-8-runtime-commit-a-task-lifecycle-destination-conflict-rework-1.cycle.md`

Blocked predecessor lifecycle source, before repair:

- `.aiassistant/tasks/active/20260902_1942_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-transport-label-rework-1.md`

Immediate predecessors:

- `.aiassistant/records/aiscc/cycles/20260902_1940_aiscc-p1-8-runtime-commit-a-transport-authority-label-conflict-rework-1.cycle.md`
- `.aiassistant/tasks/done/20260902_1936_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-semantic-gate-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260902_1934_aiscc-p1-8-runtime-commit-a-six-semantic-equivalence-contract-rework-1.cycle.md`

Accepted authority predecessors:

- `.aiassistant/records/aiscc/cycles/20260902_1222_aiscc-p1-8-runtime-human-final-acceptance-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260902_1355_aiscc-p1-8-terminal-dirty-baseline-audit-acceptance-human-disposition-gate-1.cycle.md`
- `.aiassistant/reports/aiscc/20260902_1621_aiscc-browser-command-center-session-handoff-p1-8-runtime-commit-a-fresh-chat-resume-1.md`

Tool/config only when exact local Ruff/mypy invocation requires:

- `pyproject.toml`

unrelated rules/records/source/log bulk-read 금지.

## 7. authority / conflict guard

Authority precedence:

```text
current local repository canonical
> terminally persisted accepted Cycle/rule/commit
> 2023 judgment Cycle + accepted predecessor Cycles/Handoff
> stale-capable Browser Project Source mirror
> chat memory
```

다음이 충돌하면 destructive action을 하지 않는다.

- current Task
- current branch/HEAD/index
- exact predecessor Cycle/Task identity
- six current/HEAD identity
- accepted 36 current byte identity
- canonical rules

Current local canonical이 1942 blocked result 이후 합법적으로 advance한 흔적이 있으면 `git reset`, checkout, restore로 predecessor HEAD에 맞추지 않는다.

결과:

```text
POLICY_CONFLICT_INVESTIGATION_REQUIRED
or
BLOCKED_REQUIRED_EVIDENCE / REPOSITORY_IDENTITY_ADVANCED
```

정확한 current state를 report/export하고 STOP한다.

## 8. pre-mutation repository preflight

transport 완료 직후의 governance 변화를 별도로 기록한 뒤 destructive action 전에 다음을 검증한다.

### 8.1 repository identity

Required predecessor binding:

```text
repository: ai-software-command-center
branch: main
expected HEAD: 1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a
index: empty
Commit A: absent
```

Pass:

- branch exact `main`
- HEAD exact expected predecessor
- index exact empty
- no Commit A with the required new commit message already created from this task

HEAD가 다르면 **reset하지 말고 STOP**한다.

### 8.2 runtime dirty set

Expected before six restore:

```text
42 runtime dirty paths
= exact accepted 36
+ exact Human-authorized six
```

다른 runtime path가 하나라도 존재하거나 expected path가 빠졌다면 STOP한다.

### 8.3 governance inventory


1942 transport 후 admitted Git-visible governance count는 `20`이고, 1942 Task는 active/ignored 상태로 남아 있다.

정확한 순서:

```text
A. 신규 transport 전:
   Git-visible governance = exact 20
   1942 active exists
   1942 correct done absent

B. 2023 Cycle + current 2025 active Task transport 직후:
   Git-visible governance = exact 21
   - 2023 Cycle tracked
   - current active Task ignored
   - 1942 active still ignored

C. explicit 1942 active→1942 done lifecycle repair 직후:
   Git-visible governance = exact 22
   - 1942 done tracked 추가
   - 1942 active absent
   - 1936 done preserved unchanged

D. current 2025 Task active→2025 done lifecycle 직후:
   Git-visible governance = exact 23
   - current 2025 done tracked 추가
```

unexpected path/count/identity가 있으면 자동 확장하거나 cleanup하지 말고 runtime mutation 전에 STOP한다.

## 9. exact six Human-authorized restore identity

아래 여섯 path만 restore 후보이다.

| path | current SHA-256 authorized to discard | expected HEAD blob SHA-1 | recorded current worktree blob SHA-1 |
|---|---|---|---|
| `src/aiscc/evidence/content.py` | `86fec26a717ec99878d0cd2b69860d2e27aeb30d1a76f1f1e53d1d773611f804` | `63f0334f55aee58297a9bc357493bef4c5dacc50` | `806633d46d13e4cfac54cec7d9e0e19ca91a4e45` |
| `src/aiscc/evidence/models.py` | `7617ad5e9ba531df0ff2b673dff30312889838f61db53395ea344d1ecdd083aa` | `ad72df4dd84a6a5a4863fc3f28a5af1b115b09f1` | `d932babe2097a06139eef9d7aefa2468dab8041c` |
| `src/aiscc/evidence/repository.py` | `db235bb078befbc5afdd5a042410f126e61493ea7818d5adf0e3f223fd9cd9bb` | `c8caa06b12248e27b6b0f345632544302711c81f` | `9b5e9361a263049afbc4c211471cd30f2dfc0c93` |
| `src/aiscc/evidence/requirements.py` | `7fa93582e21bad5bcedbd1c4eed70e3330d8943610891b625e44f028049c0f79` | `a0be7227377853c0cabb12108e74faaa83fba618` | `8ded3c9599b26d2c870d35f56f73e768738bd2a1` |
| `src/aiscc/evidence/service.py` | `0b25caf58eda7b5ae5eb2662b113371e400f82f8bbaa36c1454f26679edcd0b0` | `1d29c39531af55678611b84a4f7f7c4b6df2785e` | `fb1fa979903cf8a2adfa744203fb020567cc0544` |
| `src/aiscc/human/repository.py` | `1ed1d466ec056562433c347bbe903356badd5999656e15118fa8d6ef048e51ea` | `75dfaa00a315696a5b5bd08f0128b290fda7a66b` | `0f98badc2ea52eb887a81e8623ff55a8e482252f` |

각 path에 대해 restore 전에 반드시 확인:

1. current SHA-256 exact match
2. current worktree blob SHA-1 exact match
3. expected `HEAD:<path>` blob SHA-1 exact match
4. path가 tracked file이며 expected HEAD bytes를 읽을 수 있음

하나라도 mismatch면 restore하지 않는다.

## 10. six semantic-equivalence gate


restore 전에 current worktree와 exact `HEAD:<path>` bytes로 gate를 새로 계산한다.

### 10.1 공통 — six 전부

1. Section 9 exact identity 일치
2. 양쪽 `ast.parse` 성공
3. `ast.dump(..., include_attributes=False)` exact-equivalent
4. normalized tokenization은 layout token만 제거하고 identifier/literal/keyword/comment/OP value는 보존
5. source mutation 없음

AST mismatch/parse failure면 즉시 STOP.

### 10.2 strict equality — five paths

아래 5개는 normalized token/comment exact equality가 필요하다.

```text
src/aiscc/evidence/content.py
src/aiscc/evidence/repository.py
src/aiscc/evidence/requirements.py
src/aiscc/evidence/service.py
src/aiscc/human/repository.py
```

### 10.3 narrow exception — exact models.py only

다음 identity에만 적용:

```text
path: src/aiscc/evidence/models.py
current SHA-256: 7617ad5e9ba531df0ff2b673dff30312889838f61db53395ea344d1ecdd083aa
current blob SHA-1: d932babe2097a06139eef9d7aefa2468dab8041c
expected HEAD blob SHA-1: ad72df4dd84a6a5a4863fc3f28a5af1b115b09f1
```

Strict equality면 일반 PASS.

Strict mismatch면 아래 fingerprint가 전부 exact해야만 예외 PASS:

```text
current normalized token count: 2451
HEAD normalized token count: 2453
diff hunk count: exactly 2

hunk 1:
current side: empty insertion
HEAD range: 227:228
HEAD token: OP '('

hunk 2:
current side: empty insertion
HEAD range: 229:230
HEAD token: OP ')'

all diff opcodes: insert-only current -> HEAD
identifier differences: 0
literal differences: 0
keyword/name differences: 0
comment differences: 0
other OP differences: 0
replacement/deletion/reorder differences: 0
AST differences: 0
```

전부 맞으면:

```text
REDUNDANT_PARENTHESIS_ONLY_EQUIVALENCE / PASS
```

이 예외는 일반 parenthesis ignore 규칙이 아니다. 다른 path/identity/위치/개수/토큰 차이는 전부 FAIL.

### 10.4 overall

```text
five strict PASS
AND (models.py strict PASS OR exact narrow exception PASS)
AND six AST PASS
→ SIX_SEMANTIC_EQUIVALENCE_PASS
```

overall PASS 후에만 restore authority를 실행한다.

## 11. exact six restore

모든 precondition과 semantic-equivalence가 PASS한 경우에만 exact six에 대해 worktree-only restore를 수행한다.

허용 개념:

```text
git restore --worktree --source=<exact expected HEAD> -- <exact six paths>
```

금지:

```text
git restore .
git checkout .
git reset --hard
git clean
broad pathspec
index restore/staging during this step
```

Restore 직후 required proof:

- six paths clean against exact HEAD
- six paths index entries unchanged / unstaged
- index still empty
- runtime dirty path count `42 → 36`
- remaining runtime dirty set equals exact accepted 36 only
- governance paths remain unstaged

## 12. Accepted 36 runtime identity

Exact post-restore Commit A candidate는 아래 case-sensitive ordinal path/hash set이다.

```text
migrations/versions/20260831_0006_p1_8_project_memory_cycle_admission.py e0072031ffc8be030bfa265d329196b67aad6774df240904fa01d8fdccf8766c
migrations/versions/20260831_0007_p1_8_authority_contract_rework.py 544aef28e3f36d5cff322afa9401b96f45fb050d03c7d41ea7d673e597815e0e
migrations/versions/20260901_0008_p1_8_prerequisite_authority_reconciliation.py c270e10f7d0763e4f5fee1d298ad9d41abb83510a07864cd4d3919afe4362d27
src/aiscc/contracts/canonical_json.py 9e235fff10aea51a44f8b1c6830d8ce724476339239a2d6d245dcdc94094a442
src/aiscc/cycle/__init__.py f9631ca9338109cbcd7a2aa07340a001b742fe4af0b129ca136c1078c4b62fed
src/aiscc/cycle/models.py e5aaa9a84c5d0cf8231c86d2efd300e8b1fa011697642d7d6ee395f46f0e1cf4
src/aiscc/cycle/repository.py d0a11d869ba94383eb35bf98f546968da28e3d2c56f872ad9de77728b9dc357d
src/aiscc/judgment/authority.py 0013e4a2ae6f84aba7341d1e58657ce0973ce7a7d5841d8fb69f7403f15a3941
src/aiscc/memory/__init__.py 842060c4e15da581c17f573e1e4a465592f486947e34eeaaa3cd589d1525fe79
src/aiscc/memory/models.py ba8c0fe2cb2802298b445718f2ae2fa0681b8f2983dec5064d9141fe38b8d308
src/aiscc/memory/repository.py b93856e50e1c5d5a74f7d49e1839bb2a2766a37fe3318fb49c2a2ec065f62ac4
src/aiscc/next_action/__init__.py c1e8cadee709b6ba289fa9f92ed2eeaa04e51444e3a9ff85f2fc97138c42172d
src/aiscc/next_action/models.py 09d5c13d73f2bb1cd4ef05433f73f40eedcb670353dcfae9cdbf480420af1ea6
src/aiscc/next_action/repository.py 51a44c9d28a374aea1359e41752e5ff02fdb21f89844ae61e082707906e213f7
src/aiscc/persistence/models.py 60518bd1ab916a07118de0e2bd6a507565a0fc0dc48d8cc003cd521b3018ca48
src/aiscc/persistence/repository.py 74a497fd32eb42176afd19b2ba621da04364b847b0130f52966bcb3001159dd1
src/aiscc/task_authority/__init__.py eb5c7e78bb891002d4bcbb81bf35ac121b9cbf8f4e2bab0c64b1232422d141d6
src/aiscc/task_authority/authority.py 76fe0027ca2d652efd8a9fe204408d23751aa23175c369a5bc6ce389ba3af165
src/aiscc/task_authority/models.py 101ec23cbf5197ec62e8a9c4b58e5fefa2296eeae43d75053f318cf66e05abd0
src/aiscc/task_authority/ports.py 991ad83420947a35021d6acfcc4ef0bc150d5112582e69b740698374eb8b68e8
src/aiscc/task_authority/repository.py 5de5faf4a7d60c83b181588d691ce36006469095b3e16aa449881ad14143f745
src/aiscc/workflow/__init__.py 3c4cdb62a49cb53c61705e705b77cd9fee14702671690c128076c9c9f7cdc5a1
src/aiscc/workflow/guards.py 0ad7c75e22755ecd2132805e6c143b99489eea8d7807a505f3798736a0364ba2
src/aiscc/workflow/models.py f69e813dea6c35f65c8eb28cfe118b36091dd8cf5225241396e254f6ea0ff99c
src/aiscc/workflow/ports.py afb4b105a4bf55a8dcfc2abb7bc110b7b7262a50851ae3cda6734489ebbc863f
tests/integration/evidence/test_postgres_evidence_admission.py 9f56ced27bdcca3c010240f7d8736a21ff4fe94a97d5330571c584b1cba3f545
tests/integration/human/test_postgres_human_gate_judgment.py 142020f3a81221944e6eb0001160b83aa897662a324c9e89963e4226079a02b5
tests/integration/memory/test_postgres_project_memory_next_action.py 6881eaebbb8c25f34e1589e552b044d4072aebda3e2a06d40f942f2526254bd1
tests/integration/providers/test_execution_persistence.py 717a40b9323d0c42560ef34a8f39634777be0929d3eeaea5b447c9e4e4de1214
tests/integration/task_authority/test_postgres_external_task_authority.py 15dfa7e90807aa02c60cec13f03ca64d24cce56a23049c6043cc9aff554234a5
tests/integration/workflow/test_postgres_kernel.py 10be51d5d7b43b4dbd2df8a19900ac4c116990a42860ffe8a015170cff877240
tests/unit/contracts/test_canonical_json.py 33095e18666620a4b504c719ebdabfd302e8be2bbc9b6f10e0013453964de7d3
tests/unit/cycle/test_project_memory_cycle_domain.py 783aef1e86191a68481f818b333a47e8a1da17affe7d2791d3824fbd12e4031d
tests/unit/next_action/test_next_action_domain.py 1a1525c4509302b6f5aaa4ff19965cd4e1680b5e3543db571af38c7067261449
tests/unit/task_authority/test_external_task_authority_domain.py f1b83cd299ac8f6bef239f18aa6206da5034a04ae2d9a5693ff760c1325e0ffd
tests/unit/workflow/test_state_machine.py 7f0501684a30211ab43b7bb9bdae389934c3558a28da266c94254f0fdb867752
```

Corrected aggregate serialization:

```text
<case-sensitive repository-relative path>\t<lowercase_sha256>\n
```

- sort: ordinal case-sensitive path order
- one row per path
- final newline included
- path count: `36`
- required aggregate SHA-256: `a82d94c1d607bc379c12d0768ff54d0cd481467eb731e0884f63176bd1207f3c`

Historical legacy provider-last identifier:

```text
a1d5e9d24eabae3fec13e24cfb9d94e744e6687ca4c00889e85972fb5a633590
```

이 legacy value를 current aggregate로 사용하지 않는다.

## 13. accepted-36 revalidation

Restore 후 각 accepted path의 current SHA-256이 위 manifest와 exact match해야 한다.

그리고 corrected aggregate를 위 serialization 규칙으로 다시 계산하여 exact match해야 한다.

Mismatch면:

```text
BLOCKED_REQUIRED_EVIDENCE / ACCEPTED_36_IDENTITY_MISMATCH
```

accepted path를 고치거나 regenerate하지 말고 STOP한다.

## 14. validation before staging

### 14.1 git diff check

```text
git diff --check
```

PASS가 필요하다.

### 14.2 repository-local Ruff/mypy

`pyproject.toml`과 이미 설치된 repository-local tooling을 사용한다.

- network 금지
- package install/upgrade 금지
- 새 environment 생성 금지
- current repository에 이미 존재하는 실행 방식만 사용
- 가능하면 changed source scope를 사용
- existing configuration이 explicit broader local invocation을 요구하면 그 configuration을 따르되 network/credential/container를 새로 만들지 않는다.

Ruff/mypy executable/configuration이 현재 environment에 없어 새 설치가 필요한 경우:

```text
BLOCKED_REQUIRED_EVIDENCE / LOCAL_STATIC_TOOL_UNAVAILABLE
```

로 STOP하고 설치하지 않는다.

### 14.3 reused test evidence

1100 predecessor full test evidence는 다음 조건에서만 `REUSED_ACCEPTED`로 사용할 수 있다.

```text
exact accepted 36 bytes unchanged
AND
six restored to exact expected HEAD bytes
AND
no new runtime source byte introduced
```

Known predecessor evidence:

```text
231 passed plus accepted targeted/database evidence
```

이 Task를 위해 새 DB/container/full-suite를 만들지 않는다.

## 15. exact staging contract

Validation PASS 후 exact accepted 36만 stage한다.

금지:

```text
git add .
git add -A
git add src
git add tests
broad directory/pathspec staging
```

허용:

- 위 exact 36 paths를 명시적으로 stage

Stage 후 반드시 검증:

```text
staged path count: 36
staged path set: exact accepted 36 only
staged content identity: exact accepted manifest
six restore paths staged: 0
governance/provenance paths staged: 0
repository configuration paths staged: 0
```

하나라도 다르면 commit하지 않고 exact staging을 안전하게 해제한 뒤 report/STOP한다. unrelated worktree를 변경하지 않는다.

## 16. Runtime Commit A exact contract

모든 gate가 PASS했을 때만 commit exactly one을 생성한다.

```text
expected parent:
1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a

commit count:
exactly 1

merge parent count:
0

commit message:
feat(runtime): complete P1-8 project memory and cycle admission

changed path count:
exactly 36

changed paths:
exact accepted-36 manifest only

six restore paths in Commit A diff:
0

governance/provenance/configuration paths in Commit A:
0
```

Git author identity:

- 현재 repository/local Git configuration으로 commit 가능할 때만 사용
- global author identity를 설정하지 않는다.
- identity가 없어 configuration mutation이 필요하면 commit 전에 STOP한다.

Failure:

```text
BLOCKED_REQUIRED_EVIDENCE / GIT_AUTHOR_IDENTITY_UNAVAILABLE
```

## 17. Commit A object proof

Commit 생성 직후 최소 다음을 검증한다.

1. new commit hash
2. exact one parent
3. parent = `1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a`
4. merge parent 없음
5. exact commit message
6. changed path count `36`
7. exact path set = accepted 36
8. each committed blob/file bytes = accepted manifest identity
9. six restore paths absent from commit diff
10. governance/provenance/configuration paths absent from commit diff
11. index empty after commit
12. runtime source worktree clean after commit
13. remaining worktree dirt is governance/provenance only and is inventoried exactly

Commit object mismatch를 발견하면 추가 commit/amend/reset을 임의 실행하지 않는다.
`COMMAND_CENTER_REVIEW_REQUIRED` 또는 blocker로 report한다.

## 18. export bundle contract

Target:

```text
.aiassistant/reports/target/20260902_2025_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-task-lifecycle-rework-1/
```

Required root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `RESTORE_EVIDENCE.md`
- `GIT_OBJECT_EVIDENCE.md`
- exact 36 files exported from **Commit A tree**, preserving repository-relative paths, only if Commit A exists
- `REMOVED_FILES.md` only if repository product/governance deletion occurred; normally this Task has no deletion and must omit it

`TASK.md`는 current Task exact byte copy다.

Manifest must include at minimum:

- source repository/branch/HEAD before work
- Commit A hash when created
- each payload relative path
- byte size
- SHA-256 of source/copy
- exported committed source path mapping
- UTF-8/no-BOM/control-character validation for Markdown artifacts
- sensitive-data scan result without secret values

Commit A가 blocker로 생성되지 않았다면 nonexistent commit-tree source copies를 fabricate하지 않는다.
그 경우 blocker를 입증하는 최소 evidence만 export한다.

## 19. Task lifecycle


Executor-required work/report/export가 끝나면 current Task를 **자기 matching done path**로만 Move한다.

```text
.aiassistant/tasks/active/20260902_2025_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-task-lifecycle-rework-1.md
→
.aiassistant/tasks/done/20260902_2025_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-task-lifecycle-rework-1.md
```

이 destination이 이미 존재하면 overwrite/delete하지 않고 `TASK_LIFECYCLE_DESTINATION_CONFLICT`로 STOP한다.

`tasks/done != accepted`이다.

blocked result라도 mandatory-stop branch의 report/export가 완결되고 이 exact lifecycle destination에 충돌이
없으면 active→done lifecycle을 수행할 수 있다.

## 20. workflow transition expectation


- initial_state: `P1-8_RUNTIME_HUMAN_ACCEPTED / RESTORE_SIX_AUTHORIZED / COMMIT_A_PENDING / TASK_LIFECYCLE_REWORK_AUTHORIZED`
- after new transport: `CURRENT_TASK_AND_2023_CYCLE_TRANSPORTED`
- after exact 1942 lifecycle repair: `PREDECESSOR_TASK_LIFECYCLE_REPAIRED`
- after session/repository preflight: `COMMIT_A_PRECONDITIONS_VERIFIED`
- after corrected semantic gate: `SIX_SEMANTIC_EQUIVALENCE_PASS`
- after exact restore: `SIX_RESTORED / ACCEPTED_36_ONLY`
- after validation/staging: `COMMIT_A_READY`
- successful end: `COMMIT_A_CREATED / COMMAND_CENTER_REVIEW_REQUIRED`
- Agent terminal acceptance authority: `No`

Denied:

- `COMMIT_A_ACCEPTED`
- `COMMIT_B_CREATED`
- `P1_8_CLOSED`
- `P1_CLOSED`
- `P2_STARTED`

## 21. evidence contract


### executor_required

- `PUBLIC_PROVENANCE / TRANSPORT`: exact new 2025 Task + 2023 Cycle Move
- `PUBLIC_PROVENANCE / TASK_LIFECYCLE_REPAIR`: exact 1942 active→matching 1942 done Move without touching 1936 done
- `SESSION_AUTHORITY`: 1849→1936→1942 fresh-session lineage reuse
- `STATIC_SOURCE / LOCAL_GIT_PREFLIGHT`: exact branch/HEAD/index/runtime/governance
- `STATIC_SOURCE / RESTORE_IDENTITY`: six `6/6`
- `STATIC_SOURCE / SEMANTIC_EQUIVALENCE`: preserve 1934 corrected gate; fresh recomputation
- `STATIC_SOURCE / POST_RESTORE`: six clean, index empty, runtime 42→36
- `STATIC_SOURCE / ACCEPTED_RUNTIME_IDENTITY`: exact accepted 36 + aggregate
- `STATIC_CHECK`: diff-check + repository-local Ruff/mypy
- `GIT_INDEX`: exact accepted 36 only
- `GIT_OBJECT`: one exact Runtime Commit A
- `SOURCE_EVIDENCE_EXPORT`: manifest + exact Commit A tree copies
- `PUBLIC_PROVENANCE / CURRENT_TASK_LIFECYCLE`: exact current 2025 active→matching 2025 done

### reuse_allowed

- 1222 Human exact-36 acceptance while byte identities remain exact
- 1355 `RESTORE_SIX_TO_EXACT_HEAD` while exact six identities remain exact and Section 10 PASS
- 1934 corrected semantic-gate definition; actual gate must be freshly recomputed
- 1100 accepted tests only under unchanged accepted-36 + exact-HEAD-restored-six applicability

### human_owned

- future substantive review/acceptance of Runtime Commit A
- later Commit B/canonical closure

### not_required

- new IDE chat creation
- browser/provider/network/deployment evidence

### forbidden

- overwrite/delete 1936 done predecessor Task
- broad cleanup/reset/restore/staging
- accepted runtime source modification
- general parenthesis ignore beyond exact Section 10 narrow exception
- Commit B/canonical closure/P1/P2
- push/remote/network/deployment

### proof_non_substitution

```text
tasks/done != accepted
lifecycle repair != runtime proof
Task transport PASS != semantic gate PASS
AST equality alone != corrected semantic gate
restore decision != restore execution
Commit A created != P1-8 closed
```

## 22. conformance reporting

- applicability: `REQUIRED`
- applicable policy_or_invariant: `exact Human authority binding; proof non-substitution; session-bound destructive authority; tracked governance vs runtime separation`
- required_actual_owner: `Human opens chat / Executor performs exact authorized mutation / Browser Command Center judges result`
- planned_vs_actual_scope: `report exact deviations, including transport state and any mandatory stop`
- rollback_or_failure_semantics:
  - pre-mutation blocker → no runtime/index mutation
  - post-restore/pre-commit blocker → report exact six restored state; do not invent broad rollback unless Task explicitly authorizes it
  - staging mismatch → safely unstage only current Task's exact staged paths and STOP
  - post-commit object mismatch → do not amend/reset/create second commit; preserve evidence and STOP for Command Center

## 23. project context impact

architecture:
- `NONE`

orchestration_contract:
- `NONE — persistence of already Human-accepted P1-8 runtime only`

security_sandbox:
- `NONE`

public_provenance:
- `TASK_AND_CYCLE_ONLY — current Task becomes tasks/done; future Command Center creates judgment Cycle`

source_mirror:
- `NOT_REQUIRED in this Task`

## 24. accept 기준


Successful candidate requires:

1. exact 2025 Task + 2023 Cycle transport PASS
2. exact 1942 active→matching 1942 done lifecycle repair PASS; 1936 done preserved
3. session lineage PASS
4. repository/runtime/governance preflight PASS
5. six identity `6/6`
6. Section 10 corrected semantic gate PASS
7. exact six restore; runtime 42→36; index empty
8. accepted 36 + aggregate exact
9. diff-check/Ruff/mypy PASS
10. stage exact 36 only
11. exactly one Runtime Commit A with exact parent/message/path/blob/tree
12. six/governance/config absent from Commit A
13. index empty
14. Commit A tree export/manifest integrity PASS
15. current 2025 active→matching 2025 done lifecycle complete
16. final result `COMMIT_A_CREATED / COMMAND_CENTER_REVIEW_REQUIRED`

## 25. hold/reject 기준


Pre-runtime-mutation STOP:

- new Task/2023 Cycle transport conflict/hash mismatch
- 1942 active identity mismatch
- matching 1942 done already exists
- 1936 done predecessor would be overwritten/changed
- session-lineage conflict
- branch/HEAD/index mismatch or repository advance
- unexpected runtime/governance path/count
- six current/HEAD identity mismatch
- Section 10 corrected semantic gate failure
- accepted 36 identity/aggregate mismatch
- static tool requires install/network

Pre-commit STOP:

- post-restore runtime set not exact accepted 36
- diff/Ruff/mypy fail
- staging not exact 36
- Git author unavailable without config mutation

Current Task lifecycle STOP:

- matching 2025 done destination already exists or cannot be proven noncolliding

Do not create a repair second commit.

## 26. mandatory stop 조건

- `FRESH_CHAT_PRECONDITION_NOT_SATISFIED`
- `TRANSPORT_PRECONDITION_FAILED`
- `REPOSITORY_IDENTITY_ADVANCED`
- `DIRTY_WORKSPACE_MIXED`
- `POLICY_CONFLICT_INVESTIGATION_REQUIRED`
- `SIX_IDENTITY_MISMATCH`
- `SIX_SEMANTIC_EQUIVALENCE_FAILED`
- `ACCEPTED_36_IDENTITY_MISMATCH`
- `LOCAL_STATIC_TOOL_UNAVAILABLE`
- `STATIC_VALIDATION_FAILED`
- `STAGING_SCOPE_MISMATCH`
- `GIT_AUTHOR_IDENTITY_UNAVAILABLE`
- `GIT_OBJECT_CONTRACT_MISMATCH`
- `EVIDENCE_SCOPE_EXPANSION_REQUIRED`

Named blocker 이후에는 blocker를 입증하는 최소 evidence, workspace inventory, report/export, Task lifecycle의 안전한 종료만 수행한다.

## 27. 보고서 필수 항목


- task/work type/task path
- Downloads transport result for current 2025 Task + 2023 Cycle
- exact 1942 predecessor lifecycle repair precheck/action/result
- explicit proof that 1936 done predecessor was preserved
- current IDE session lineage
- read canonical paths
- repository branch/HEAD/index before mutation
- governance inventory at A/B/C/D stages
- runtime dirty inventory before/after restore and after commit
- predecessor identity result
- six current SHA-256/blob/HEAD blob
- Section 10 fresh semantic result including exact models.py fingerprint if narrow exception used
- exact restore path/result
- accepted 36 `36/36` + aggregate
- git diff --check / Ruff / mypy
- staged path/blob inventory
- Commit A hash/message/parent/path/blob/tree proof
- index/worktree after commit
- current 2025 active→matching done lifecycle
- product source / governance / repository-config changes
- evidence classifications
- human pending/provided
- forbidden-not-run
- mandatory stop
- unverified items
- rollback/failure semantics
- UTF-8/control/trailing-whitespace validation
- sensitive-data result without secret values
- preserved exact paths
- next recommendation: `Browser Command Center substantive Commit A review`

## 28. preserved artifacts


- `.aiassistant/tasks/done/20260902_2025_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-task-lifecycle-rework-1.md` — after this Task lifecycle
- `.aiassistant/records/aiscc/cycles/20260902_2023_aiscc-p1-8-runtime-commit-a-task-lifecycle-destination-conflict-rework-1.cycle.md`
- `.aiassistant/tasks/done/20260902_1942_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-transport-label-rework-1.md` — after explicit lifecycle repair
- `.aiassistant/records/aiscc/cycles/20260902_1940_aiscc-p1-8-runtime-commit-a-transport-authority-label-conflict-rework-1.cycle.md`
- `.aiassistant/tasks/done/20260902_1936_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-semantic-gate-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260902_1934_aiscc-p1-8-runtime-commit-a-six-semantic-equivalence-contract-rework-1.cycle.md`
- all previously preserved accepted/terminal P1-8 Task/Cycle/Handoff artifacts
- successful Runtime Commit A object, if created

Temporary target:

```text
.aiassistant/reports/target/20260902_2025_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-task-lifecycle-rework-1/
```

is retained only through Browser substantive judgment.

## 29. 최종 응답 형식

1. `result: completed / blocked / rejected-candidate`
2. semantic result code, especially `COMMIT_A_CREATED / COMMAND_CENTER_REVIEW_REQUIRED` when successful
3. target bundle exact path
4. Commit A hash or `NOT_CREATED`
5. restored six count
6. staged/committed exact path count
7. changed files
8. removed files
9. human verification: `HUMAN_PENDING` for Commit A acceptance
10. unverified items
11. preserved exact paths

장문 report를 chat에 붙이지 않는다.
