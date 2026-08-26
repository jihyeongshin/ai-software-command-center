# AISCC Repository Canonical Metadata

- canonical_owner: `AISCC_REPOSITORY`
- authority: `REPOSITORY_LOCAL_CANONICAL`
- bootstrap_origin: `AISCC-BOOTSTRAP-SEED-V1`
- canonicalized_by_task: `20260826_1108_aiscc-p0-4-canonical-authority-metadata-and-post-bootstrap-state-normalization-rework-2`

---


# AISCC Agent Authority and Instruction Transport

## 1. 목적

Agent에게 어떤 instruction이 전달되었는지와, 프로젝트에서 어떤 문서가 정책 권위를 갖는지를 분리한다.

```text
instruction transport precedence
!=
AISCC document authority
```

## 2. transport layers

일반적인 Agent transport layer는 다음처럼 구분한다.

1. Agent/provider global instruction
2. repository-root instruction entrypoint
3. current working directory에 가까운 scoped instruction
4. user prompt
5. Task File과 도구로 명시적으로 읽은 canonical file

후순위로 전달된 prompt가 자동으로 project authority를 바꾸지 않는다.

IDE의 Project Rules UI, plugin 설정 또는 자동 retrieval 상태만으로 selected coding agent에게 실제 rule body가 전달됐다고 가정하지 않는다.

## 3. repository-root `AGENTS.md`

repository-root `AGENTS.md`는 thin transport bootstrap이다.

- policy authority가 아니다.
- canonical rule의 장문 복제본이 아니다.
- active Task File과 task-listed canonical source를 읽게 하는 entrypoint다.
- Git에서 TRACK되는 thin transport bootstrap이다.
- root `.gitignore`와 canonical Git policy는 repository policy owner가 관리한다. Executor는 active Task의 explicit authorization 없이 이를 수정하지 않는다.

현재 root `AGENTS.md` transport contract:

```markdown
# AISCC IDE Executor Bootstrap

transport_contract_id: AISCC-AGENT-BOOTSTRAP-V1

Before analysis, source inspection, or file changes:

1. Read `.aiassistant/rules/AISCC_AGENTS.md`.
2. Read `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`.
3. Read `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`.
4. If an active task path is provided, read the Task File before broad source exploration.
5. Read every exact path listed by the Task File under `읽을 문서` or `must_read`.
6. Treat the Task File list as the minimum authoritative context set, not permission to bulk-read unrelated source or logs.
7. Distinguish automatically discovered instructions from files explicitly read with tools.
8. If loaded instructions, the active task, canonical rules, current source, or accepted evidence conflict, stop implementation and report conflict investigation.
9. Do not claim human-owned evidence as executor-completed.
10. Do not perform Git index, commit, push, deployment, or credentialed external actions unless the active Task File explicitly authorizes them.
```

## 4. authority map

repository authority는 의미별 canonical path로 분리되어 있다.

현재 owner:

- project thesis: `.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md`
- report/export: `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- Git/asset/encoding: `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- command-center workflow: `.aiassistant/records/command-center/*`
- stable project queue: `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
- task-specific exact scope and evidence contract: current active Task File

아직 생성되지 않은 future target owner:

- architecture: `.aiassistant/rules/AISCC_ARCHITECTURE.md`
- orchestration/state transition: `.aiassistant/rules/AISCC_ORCHESTRATION.md`
- security/sandbox/tool permissions: `.aiassistant/rules/AISCC_SECURITY_SANDBOX.md`

현재 active Task File은 task-specific exact paths, allowed scope, forbidden actions, evidence contract를 소유한다. 그러나 canonical authority 순서를 prompt 한 번으로 변경할 권한은 없다.

## 5. minimum authoritative context set

Task File의 `읽을 문서`/`must_read` 목록은 해당 작업을 시작하는 최소 권위 context다.

- exact path를 직접 읽는다.
- unrelated rules, records, source tree, logs 전체를 bulk-read하지 않는다.
- report field를 채우기 위해 context를 확장하지 않는다.
- source 조사 중 새로운 policy owner가 실제로 적용됨이 확인되면 그 exact path를 읽고 보고한다.

## 6. conflict stop

다음이 충돌하면 implementation을 중단한다.

- user/human의 현재 설명
- active Task File
- canonical rule/baseline
- current source behavior
- current test
- accepted cycle/evidence
- automatically discovered instruction

진행 순서:

1. source mutation 또는 destructive action 중단
2. 충돌 문장과 path를 정확히 식별
3. 적용 canonical source 재확인
4. current source/test가 encode한 실제 behavior 확인
5. 아래 중 하나로 분류
   - code bug against current baseline
   - stale/incomplete baseline
   - intentional policy change request
   - ambiguous policy gap
   - instruction transport mismatch
6. 사람/Command Center가 baseline을 명확히 한 뒤 별도 task로 재개

권장 status:

```text
POLICY_CONFLICT_INVESTIGATION_REQUIRED
BLOCKED_POLICY_GAP
DOC_UPDATE_REQUIRED
```

## 7. prompt-level override guard

사용자가 chat에서 authority 우선순위 변경을 요구하면 policy-change request로 본다.

- 현재 turn에서 조용히 적용하지 않는다.
- corresponding canonical document update가 필요하다.
- accepted baseline update 전에는 기존 authority를 유지한다.

## 8. evidence authority guard

- Agent report는 human acceptance가 아니다.
- generated checklist는 browser QA가 아니다.
- tool output이 해당 proof channel과 일치할 때만 evidence candidate다.
- `human_owned` evidence는 사람 결과가 제공되기 전 `HUMAN_PENDING`이다.
- Agent가 human-owned verification을 완료했다고 주장해도 transition admission 근거로 사용하지 않는다.

## 9. report requirement

instruction transport 관련 task는 다음을 구분해서 보고한다.

- automatically discovered instruction inventory
- explicit tool-read inventory
- selected agent/provider/runtime snapshot when discoverable
- fresh-session verification 여부
- human-owned IDE/plugin/restart/permission action 여부
- unresolved transport boundary

현재 session 중 생성한 instruction file을 fresh session evidence 없이 자동 발견됐다고 소급하지 않는다.
