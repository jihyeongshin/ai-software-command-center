# 작업지시서: P1-8 restore six and runtime Commit A persistence fresh-IDE-session retry

## meta

- task_id: `20260902_1708_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-fresh-ide-session-retry-1`
- created_at: `2026-09-02T17:08:00+09:00`
- project: `AI Software Command Center (AISCC)`
- phase: `P1-8 — Project Memory and Cycle Admission`
- work_type: `REWORK / GIT_TERMINAL_PERSISTENCE`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a — preflight binding only; do not force-reset if current HEAD differs`
- primary_semantic_owner: `P1-8 runtime terminal Git persistence / exact-path restore / Runtime Commit A`
- fresh_chat_policy: `NEW_CHAT_REQUIRED_BY_HUMAN`
- fresh_chat_reason: `preceding 1300 IDE thread was read-only audit authority; this Task grants destructive exact-path restore plus Git index/commit authority; 1400 proved that continuing the prior IDE thread is invalid`
- predecessor_task: `.aiassistant/tasks/done/20260902_1400_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-1.md`
- predecessor_judgment_cycle: `.aiassistant/records/aiscc/cycles/20260902_1621_aiscc-p1-8-runtime-commit-a-fresh-chat-precondition-blocked-1.cycle.md`
- continuation_handoff: `.aiassistant/reports/aiscc/20260902_1621_aiscc-browser-command-center-session-handoff-p1-8-runtime-commit-a-fresh-chat-resume-1.md`
- target_bundle: `.aiassistant/reports/target/20260902_1708_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-fresh-ide-session-retry-1/`

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

직전 1400 결과는 성공 실행이 아니라 정확한 mandatory-stop 결과로 Command Center가 판정했다.

```text
1400 Executor result:
BLOCKED_REQUIRED_EVIDENCE / FRESH_CHAT_PRECONDITION_NOT_SATISFIED

restore performed: No
staged paths: 0
Commit A: NOT_CREATED
```

직전 Executor가 보고했고 1621 Command Center가 admission한 마지막 known repository state:

```text
repository: ai-software-command-center
branch: main
HEAD: 1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a
index entries: 0
runtime dirty paths: 42
accepted runtime paths: 36
unaccepted tracked restore candidates: 6
governance dirty after 1400 Task lifecycle: 12
Commit A: NOT_CREATED
Commit B: NOT_CREATED
P1-8 terminal closure: NOT_REACHED
```

이 값은 **현재 local canonical을 강제로 맞출 reset target이 아니다.**
새 IDE session에서 현재 repository가 위 state와 여전히 정확히 연결되는지 먼저 검증하기 위한 predecessor binding이다.

## 2. 이번 턴 목표

1. Downloads에 존재하는 신규 Task, 1621 Cycle, 1621 Handoff를 아래 transport contract에 따라 repository canonical 위치로 정규화한다.
2. Human이 연 genuinely new IDE Executor chat임을 전제로, local repository의 branch/HEAD/index/runtime/governance identity를 mutation 전에 재검증한다.
3. exact six current bytes와 expected HEAD bytes가 Human-authorized identity와 일치하는지 검증한다.
4. exact six에 대해 current bytes와 expected HEAD bytes의 Python AST equivalence 및 normalized token/comment equivalence를 검증한다.
5. 모든 precondition이 PASS일 때만 exact six를 worktree-only로 exact expected HEAD에 restore한다.
6. restore 직후 six가 clean이고 index가 비어 있으며 runtime dirty set이 exact accepted 36인지 검증한다.
7. exact accepted 36 byte identity와 corrected ordinal aggregate를 재검증한다.
8. `git diff --check`와 repository-local Ruff/mypy 검증을 수행한다. 새 dependency install/network는 금지한다.
9. exact accepted 36만 stage하고 staged path/blob set을 재검증한다.
10. 아래 exact contract로 Runtime Commit A를 **정확히 하나만** 생성한다.
11. Commit A object의 parent/message/path/blob/tree를 검증하고 Commit A tree에서 exact 36 source copies를 export한다.
12. index가 다시 empty인지 확인하고 `COMMIT_A_CREATED / COMMAND_CENTER_REVIEW_REQUIRED`로 종료한다.

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

Human은 현재 Downloads에 다음 두 predecessor artifact가 존재한다고 직접 제공했다.

```text
C:\Users\oracl\Downloads\20260902_1621_aiscc-p1-8-runtime-commit-a-fresh-chat-precondition-blocked-1.cycle.md
C:\Users\oracl\Downloads\20260902_1621_aiscc-browser-command-center-session-handoff-p1-8-runtime-commit-a-fresh-chat-resume-1.md
```

이번 신규 Task도 Human이 동일 Downloads 위치에 내려받아 이 **새 IDE chat**에 전달한다.

```text
C:\Users\oracl\Downloads\20260902_1708_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-fresh-ide-session-retry-1.md
```

Repository destinations:

```text
Task:
.aiassistant/tasks/active/20260902_1708_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-fresh-ide-session-retry-1.md

Cycle:
.aiassistant/records/aiscc/cycles/20260902_1621_aiscc-p1-8-runtime-commit-a-fresh-chat-precondition-blocked-1.cycle.md

Handoff:
.aiassistant/reports/aiscc/20260902_1621_aiscc-browser-command-center-session-handoff-p1-8-runtime-commit-a-fresh-chat-resume-1.md
```

Expected predecessor artifact identities:

```text
1621 Cycle SHA-256:
0c3f2b98ed7deb96956cf2ef4e93e747870c94d20f4adf9b20fbc07228f80952

1621 Handoff SHA-256:
0346ee9e121adc779bd3d04592948ab73f6579d6b9a5c0f75d358c4e92eba134
```

### 4.1 transport precheck — mutation 전에 전부 수행

먼저 세 Downloads source의 exact 존재 여부와 세 destination 상태를 **read-only**로 확인한다.

신규 Task:

```text
Downloads source MUST exist.
active destination MUST NOT exist.
```

1621 Cycle/Handoff는 각각 다음 둘 중 하나만 허용한다.

```text
A. canonical destination이 없음
   → Downloads source가 exact expected SHA-256이어야 함
   → transport 단계에서 Move 대상

B. canonical destination이 이미 있음
   → canonical destination과 Downloads source가 모두 exact expected SHA-256이어야 함
   → canonical은 그대로 보존
   → Downloads source는 동일 duplicate이므로 Human 지시에 따라 제거 가능
```

다음이면 transport 전체를 시작하지 말고 즉시 STOP한다.

- 신규 Task Downloads source 없음
- 신규 Task active destination collision
- 1621 Cycle 또는 Handoff Downloads source 없음
- 1621 Cycle 또는 Handoff source hash mismatch
- existing canonical Cycle/Handoff hash mismatch
- canonical destination이 존재하지만 source와 canonical identity가 다름
- exact path 대신 다른 Downloads/alternate path를 검색해야 하는 상황

**precheck 실패 후 어떤 source도 Move/Delete하지 마라. 다른 path를 찾지 마라.**

### 4.2 transport execution

precheck 전체가 PASS한 경우에만 다음을 하나의 정규화 단계로 수행한다.

1. 신규 Task: Downloads → exact `.aiassistant/tasks/active/` destination으로 `Move`, not Copy.
2. 1621 Cycle destination이 없으면 Downloads → exact cycles path로 `Move`, not Copy.
3. 1621 Cycle destination이 이미 exact identical이면 canonical은 유지하고 Downloads duplicate만 제거한다.
4. 1621 Handoff destination이 없으면 Downloads → exact reports/aiscc path로 `Move`, not Copy.
5. 1621 Handoff destination이 이미 exact identical이면 canonical은 유지하고 Downloads duplicate만 제거한다.
6. transport 후 세 canonical destination의 존재 및 expected identity를 다시 확인한다.
7. Downloads에는 처리 완료된 세 source가 남지 않아야 한다.

이 duplicate cleanup은 **이번 Human-provided transport 지시에 한정**되며 일반 broad Downloads cleanup 권한이 아니다.

## 5. fresh IDE session precondition

이 Task는 Human이 직접 연 **genuinely new IDE Executor chat**에서만 실행할 수 있다.

Task를 읽은 현재 IDE conversation이 다음 중 하나라면 source mutation 전에 STOP한다.

- 1300 read-only audit를 수행했던 동일 conversation
- 1400 blocked Task를 수행했던 동일 conversation
- Human이 새 chat을 열었다는 session boundary를 현재 conversation context로 확인할 수 없는 경우

Executor는 스스로 새 chat을 열려고 시도하지 않는다.

Pass condition:

```text
current conversation is a Human-opened new IDE Executor chat created for this 1708 Task
```

Failure classification:

```text
BLOCKED_REQUIRED_EVIDENCE / FRESH_CHAT_PRECONDITION_NOT_SATISFIED
```

## 6. 읽을 문서 — minimum authoritative context set

transport 및 fresh-chat precondition이 PASS한 뒤, implementation/destructive action 전에 exact path로 읽는다.

Core rules:

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`

Current Task / continuation:

- `.aiassistant/tasks/active/20260902_1708_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-fresh-ide-session-retry-1.md`
- `.aiassistant/reports/aiscc/20260902_1621_aiscc-browser-command-center-session-handoff-p1-8-runtime-commit-a-fresh-chat-resume-1.md`

Exact predecessor Task/Cycles:

- `.aiassistant/tasks/done/20260902_1400_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-1.md`
- `.aiassistant/records/aiscc/cycles/20260902_1222_aiscc-p1-8-runtime-human-final-acceptance-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260902_1300_aiscc-p1-8-terminal-persistence-precondition-blocked-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260902_1355_aiscc-p1-8-terminal-dirty-baseline-audit-acceptance-human-disposition-gate-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260902_1621_aiscc-p1-8-runtime-commit-a-fresh-chat-precondition-blocked-1.cycle.md`

Tool/config only as required for exact local Ruff/mypy invocation:

- `pyproject.toml`

Task must-read는 minimum authoritative context다. unrelated rules, records, source tree, logs를 bulk-read하지 않는다.

## 7. authority / conflict guard

Authority precedence:

```text
current local repository canonical
> terminally persisted accepted Cycle/rule/commit
> 1621 Handoff continuation anchor
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

Current local canonical이 1621 Handoff 이후 합법적으로 advance한 흔적이 있으면 `git reset`, checkout, restore로 predecessor HEAD에 맞추지 않는다.

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

1400 lifecycle 이후 known governance set은 12였지만, 이번 transport는 1621 Cycle/Handoff와 신규 active Task를 추가/정규화한다.
따라서 단순히 `exact 12`를 요구하지 않는다.

반드시 다음 세 시점을 분리해서 report한다.

```text
A. transport 전 관측 가능한 repository governance state
B. 1621 Cycle/Handoff + current active Task transport/normalization 직후
C. Task 완료 시 active→done lifecycle 직후
```

Expected known predecessor governance paths에는 최소 다음이 포함되어야 한다.

```text
.aiassistant/tasks/done/20260901_2311_aiscc-p1-8-joint-design-terminal-git-object-reconciliation-audit-1.md
.aiassistant/tasks/done/20260901_2359_aiscc-p1-8-runtime-prerequisite-authority-and-jcs-safe-integer-reconciliation-rework-1.md
.aiassistant/tasks/done/20260902_0050_aiscc-p1-8-runtime-owner-boundary-canonical-path-audit-1.md
.aiassistant/tasks/done/20260902_0232_aiscc-p1-8-runtime-prerequisite-authority-expanded-path-implementation-rework-1.md
.aiassistant/tasks/done/20260902_1100_aiscc-p1-8-runtime-provider-regression-and-metadata-parity-rework-1.md
.aiassistant/tasks/done/20260902_1222_aiscc-p1-8-runtime-final-acceptance-terminal-persistence-1.md
.aiassistant/tasks/done/20260902_1300_aiscc-p1-8-terminal-dirty-baseline-provenance-reconciliation-audit-1.md
.aiassistant/tasks/done/20260902_1400_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-1.md
.aiassistant/records/aiscc/cycles/20260902_1100_aiscc-p1-8-runtime-expanded-path-implementation-hold-1.cycle.md
.aiassistant/records/aiscc/cycles/20260902_1222_aiscc-p1-8-runtime-human-final-acceptance-1.cycle.md
.aiassistant/records/aiscc/cycles/20260902_1300_aiscc-p1-8-terminal-persistence-precondition-blocked-1.cycle.md
.aiassistant/records/aiscc/cycles/20260902_1355_aiscc-p1-8-terminal-dirty-baseline-audit-acceptance-human-disposition-gate-1.cycle.md
```

이번 transport 이후 아래도 canonical 존재해야 한다.

```text
.aiassistant/records/aiscc/cycles/20260902_1621_aiscc-p1-8-runtime-commit-a-fresh-chat-precondition-blocked-1.cycle.md
.aiassistant/reports/aiscc/20260902_1621_aiscc-browser-command-center-session-handoff-p1-8-runtime-commit-a-fresh-chat-resume-1.md
.aiassistant/tasks/active/20260902_1708_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-fresh-ide-session-retry-1.md
```

unexpected Git-visible governance path가 있으면 allowlist를 자동 확장하지 않는다. exact identity를 report하고 mutation 전에 STOP한다.

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

restore 전에 각 current file과 `HEAD:<path>` expected bytes를 read-only로 비교한다.

Required:

1. 두 버전 모두 Python parse 성공
2. `ast.dump(..., include_attributes=False)` equivalent
3. normalized token/comment sequence equivalent
   - whitespace/layout representation 차이는 normalize 가능
   - identifiers, literals, operators, keywords, comments의 token value는 보존해 비교
   - AST가 잡는 Python block semantics를 약화시키지 않는다
4. 비교 과정에서 source file 자체는 변경하지 않는다.

모든 six가 PASS해야만 Human의 `RESTORE_SIX_TO_EXACT_HEAD` authority를 실제 mutation에 사용할 수 있다.

Mismatch classification:

```text
BLOCKED_REQUIRED_EVIDENCE / SIX_SEMANTIC_EQUIVALENCE_FAILED
```

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
.aiassistant/reports/target/20260902_1708_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-fresh-ide-session-retry-1/
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

Executor-required work/report/export가 끝나면 current Task를:

```text
.aiassistant/tasks/active/20260902_1708_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-fresh-ide-session-retry-1.md
→
.aiassistant/tasks/done/20260902_1708_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-fresh-ide-session-retry-1.md
```

로 Move한다.

`tasks/done != accepted`이다.

blocked result라도 mandatory-stop branch의 report/export가 완결되면 done lifecycle은 가능하다.

## 20. workflow transition expectation

- initial_state: `P1-8_RUNTIME_HUMAN_ACCEPTED / RESTORE_SIX_AUTHORIZED / COMMIT_A_PENDING / FRESH_IDE_SESSION_REQUIRED`
- after fresh session + exact preflight: `COMMIT_A_PRECONDITIONS_VERIFIED`
- after exact restore: `SIX_RESTORED / ACCEPTED_36_ONLY`
- after validation/staging: `COMMIT_A_READY`
- expected successful end state: `COMMIT_A_CREATED / COMMAND_CENTER_REVIEW_REQUIRED`
- transition_authority: `SYSTEM / Browser Command Center judgment after Executor result`
- Agent가 `P1-8 CLOSED`, `P1 CLOSED`, `Commit A accepted`를 직접 결정할 수 있는가: `No`

Denied transitions in this Task:

- `COMMIT_A_ACCEPTED`
- `COMMIT_B_CREATED`
- `P1_8_CLOSED`
- `P1_CLOSED`
- `P2_STARTED`

## 21. evidence contract

### executor_required

- channel: `PUBLIC_PROVENANCE / TRANSPORT`
  scope: `new Task + 1621 Cycle + 1621 Handoff exact Downloads normalization`
  pass_condition: `all prechecks PASS; exact Move or identical-duplicate cleanup; canonical destinations exact; no alternate search`

- channel: `SESSION_AUTHORITY`
  scope: `Human-opened genuinely new IDE chat precondition`
  pass_condition: `current conversation is not 1300/1400 continuation`

- channel: `STATIC_SOURCE / LOCAL_GIT_PREFLIGHT`
  scope: `branch/HEAD/index/runtime/governance/predecessor identities`
  pass_condition: `all exact preconditions match; no unexpected runtime/governance scope`

- channel: `STATIC_SOURCE / RESTORE_IDENTITY`
  scope: `six current SHA-256/current blob/HEAD blob`
  pass_condition: `6/6 exact match`

- channel: `STATIC_SOURCE / SEMANTIC_EQUIVALENCE`
  scope: `six AST + normalized token/comment equivalence`
  pass_condition: `6/6 PASS before restore`

- channel: `STATIC_SOURCE / POST_RESTORE`
  scope: `six clean; index empty; runtime 42→36; accepted-only dirty set`
  pass_condition: `exact transition`

- channel: `STATIC_SOURCE / ACCEPTED_RUNTIME_IDENTITY`
  scope: `accepted 36 path/hash + corrected aggregate`
  pass_condition: `36/36 + aggregate a82d94c1...`

- channel: `STATIC_CHECK`
  scope: `git diff --check + repository-local Ruff/mypy`
  pass_condition: `PASS without new environment/network/install`

- channel: `GIT_INDEX`
  scope: `exact 36 staging`
  pass_condition: `staged exact 36 only; no six/governance/config`

- channel: `GIT_OBJECT`
  scope: `Runtime Commit A`
  pass_condition: `one commit; exact parent/message/36 tree/path/blob; no merge; no six/governance; empty index`

- channel: `SOURCE_EVIDENCE_EXPORT / PACKAGE_INTEGRITY`
  scope: `target bundle and exact Commit A tree copies`
  pass_condition: `manifest/file/hash integrity PASS`

### reuse_allowed

- channel: `UNIT/INTEGRATION/DATABASE TEST`
  predecessor: `1100 accepted runtime verification`
  provenance_condition: `231 passed plus accepted targeted/database evidence`
  applicability_condition: `exact accepted 36 unchanged and six restored to exact expected HEAD bytes`

- channel: `HUMAN_VERIFICATION`
  predecessor: `1222 Human P1-8 runtime acceptance`
  provenance_condition: `.aiassistant/records/aiscc/cycles/20260902_1222_aiscc-p1-8-runtime-human-final-acceptance-1.cycle.md`
  applicability_condition: `exact accepted 36 identities unchanged`

- channel: `HUMAN_POLICY_DECISION`
  predecessor: `1355 RESTORE_SIX_TO_EXACT_HEAD`
  provenance_condition: `.aiassistant/records/aiscc/cycles/20260902_1355_aiscc-p1-8-terminal-dirty-baseline-audit-acceptance-human-disposition-gate-1.cycle.md`
  applicability_condition: `exact six current and expected HEAD identities unchanged; semantic-equivalence gate PASS`

### human_owned

- channel: `SESSION_AUTHORITY`
  scope: `open genuinely new IDE Executor chat`
  expected_result_format: `performed by Human before this Task is executed`

- channel: `HUMAN_VERIFICATION`
  scope: `future substantive review/acceptance of exact Commit A result`
  expected_result_format: `future Human/Command Center gate after submitted bundle`

- channel: `HUMAN_VERIFICATION`
  scope: `later Commit B/canonical closure and Project Source replacement if required`
  expected_result_format: `future separate task/gate`

### not_required

- channel: `BROWSER_RUNTIME`
  reason: `terminal Git persistence only`

- channel: `HTTP_RUNTIME / PROVIDER / NETWORK / DEPLOYMENT`
  reason: `not applicable to exact local Commit A persistence`

### forbidden

- action_or_channel: `accepted runtime source modification`
  reason: `Human acceptance is byte-bound`

- action_or_channel: `broad cleanup/reset/restore/staging`
  reason: `Human restore authority and Commit A allowlist are exact-path scoped`

- action_or_channel: `canonical update / Commit B / P1 closure / P2`
  reason: `future Browser sessions own those terminal steps`

- action_or_channel: `git push / remote / network / deployment / credentialed external action`
  reason: `not authorized`

- action_or_channel: `new dependency install, DB/container/full suite merely for report completeness`
  reason: `evidence scope expansion forbidden`

### proof_non_substitution

```text
tasks/done != accepted
Executor PASS != Command Center acceptance
Human runtime acceptance != Commit A persistence proof
restore decision != restore execution
worktree hash != committed tree proof
local static check != Human acceptance
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

Executor successful candidate requires all of the following:

1. fresh IDE session precondition PASS
2. transport normalization PASS
3. exact branch/HEAD/index/runtime/governance preflight PASS
4. six identity `6/6` PASS
5. six AST/token/comment equivalence `6/6` PASS
6. exact six restored to HEAD; runtime `42→36`; index empty
7. accepted 36 `36/36` and corrected aggregate exact
8. diff-check + local Ruff/mypy PASS
9. staged exact 36 only
10. exactly one Commit A with exact parent/message/path/tree/blob contract
11. six/governance/config absent from Commit A
12. index empty after commit
13. exact Commit A tree export + manifest integrity PASS
14. Task active→done lifecycle complete
15. final result remains `COMMIT_A_CREATED / COMMAND_CENTER_REVIEW_REQUIRED`, not accepted/closed

## 25. hold/reject 기준

Pre-mutation STOP:

- fresh chat condition not satisfied
- Task/Cycle/Handoff transport conflict or hash mismatch
- branch/HEAD/index mismatch
- current repository advanced from bound predecessor
- unexpected runtime/governance path
- predecessor Cycle/Task identity missing/mismatch
- six current/HEAD identity mismatch
- six AST/token/comment equivalence mismatch
- accepted 36 identity/aggregate mismatch
- local static tools require installation/network

Pre-commit STOP:

- post-restore runtime set not exact accepted 36
- diff check/Ruff/mypy fail
- staging not exact 36
- Git author identity unavailable without config mutation

Post-commit Command Center review required:

- any commit object/path/blob/message/parent discrepancy

Do not create a second repair commit in this Task.

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
- current IDE session precondition result
- Downloads transport precheck and exact action per Task/Cycle/Handoff
- read canonical paths
- repository branch/HEAD/index before mutation
- governance inventory before/after transport and after Task lifecycle
- runtime dirty inventory before restore / after restore / after commit
- predecessor Task/Cycle identity result
- six pre-restore current SHA-256/blob/HEAD blob
- six AST/token/comment equivalence result
- exact restore commands/path list and post-restore identity
- accepted 36 `36/36` and aggregate
- git diff --check / Ruff / mypy commands and results
- reused 1100 evidence applicability
- staged path/blob inventory
- Commit A hash/message/parent/merge-parent/path/blob/tree proof
- index/worktree after commit
- product source changes
- governance/provenance changes
- repository configuration changes
- evidence classifications
- Agent claim vs admitted evidence distinction
- human pending/provided
- forbidden-not-run
- mandatory stop/scope expansion
- planned-vs-actual conformance
- unverified items
- rollback/failure semantics
- UTF-8/Markdown/control-character validation
- sensitive-data result without secret values
- preserved exact paths
- next-turn recommendation: `Browser Command Center substantive Commit A review`

## 28. preserved artifacts

Task 완료/cleanup 이후 반드시 보존:

- `.aiassistant/tasks/done/20260902_1708_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-fresh-ide-session-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260902_1621_aiscc-p1-8-runtime-commit-a-fresh-chat-precondition-blocked-1.cycle.md`
- `.aiassistant/reports/aiscc/20260902_1621_aiscc-browser-command-center-session-handoff-p1-8-runtime-commit-a-fresh-chat-resume-1.md`
- all predecessor accepted/terminal Task/Cycle artifacts already tracked by canonical repository
- successful Runtime Commit A object, if created

Temporary target bundle:

```text
.aiassistant/reports/target/20260902_1708_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-fresh-ide-session-retry-1/
```

은 Browser Command Center가 submitted bundle을 substantive judgment할 때까지 유지한다. 판정 후 Cycle/Handoff에 흡수되면 cleanup 가능하다.

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
