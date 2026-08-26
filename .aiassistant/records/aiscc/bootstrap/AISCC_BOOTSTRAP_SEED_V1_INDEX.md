# AISCC Bootstrap Seed Metadata

- seed_id: `AISCC-BOOTSTRAP-SEED-V1`
- generated_at: `2026-08-26 00:07 KST`
- seed_role: `PRE_REPOSITORY_BROWSER_PROJECT_BOOTSTRAP`
- authority: `TEMPORARY_BOOTSTRAP_AUTHORITY`
- immutable_after_upload: `true`
- retirement_condition: `FIRST_AISCC_REPOSITORY_CANONICAL_MIRROR_V1_SYNC_CONFIRMED`
- domain_leakage_policy: `NO_SOURCE_PROJECT_PRODUCT_OR_DOMAIN_POLICY`

---


# AI Software Command Center Bootstrap Seed Index

## 1. 목적

이 문서군은 아직 Git repository가 존재하지 않는 시점에 새 Browser GPT Project를 시작하기 위한 **일회성 Bootstrap Seed v1**이다.

이 Seed는 다음을 제공한다.

- Browser Command Center 운영 규칙
- Agent instruction transport와 project authority의 분리
- Task File → Executor → Evidence → Judgment → Cycle → Next Action workflow
- 공개 가능한 개발 provenance 보존 정책
- repository 생성 이후 canonical → Project Source Mirror 전환 규칙

이 Seed는 최종 product architecture나 orchestration contract가 아니다. 실제 repository가 생성되면 local canonical 문서가 정본이 되고, 이 Seed 전체는 최초 canonical mirror v1로 교체된다.

## 2. 절대 권위 경계

```text
Bootstrap Seed v1
= repository가 생기기 전의 임시 시작 권위

Repository local canonical
= repository 생성 후 유일한 편집 정본

Browser Project Source mirror
= local canonical의 read-only 복제본
```

금지:

- Bootstrap Seed와 repository mirror를 동시에 active authority로 유지
- Browser Project Source에서 문서를 직접 수정하고 canonical 변경으로 간주
- Seed 문서를 repository canonical보다 우선
- Seed v1을 업로드 후 계속 수정하여 이력 없는 moving baseline으로 사용

## 3. 새 Browser Project에 업로드할 active set

아래 14개 파일을 모두 업로드한다.

1. `00_AISCC_BOOTSTRAP__SEED_INDEX.md`
2. `01_AISCC_BOOTSTRAP__PROJECT_BOOTSTRAP.md`
3. `10_AISCC_RULES__AGENT_AUTHORITY_AND_TRANSPORT.md`
4. `20_AISCC_COMMAND_CENTER__README.md`
5. `21_AISCC_COMMAND_CENTER__WORKFLOW.md`
6. `22_AISCC_COMMAND_CENTER__TASK_FILE_TEMPLATE.md`
7. `23_AISCC_COMMAND_CENTER__SHORT_EXECUTOR_PROMPT_TEMPLATE.md`
8. `24_AISCC_COMMAND_CENTER__JUDGMENT_RUBRIC.md`
9. `25_AISCC_COMMAND_CENTER__CYCLE_RECORD_TEMPLATE.md`
10. `26_AISCC_COMMAND_CENTER__NEXT_ACTION_SELECTION_RUBRIC.md`
11. `30_AISCC_RULES__IDE_EXECUTOR_REPORT_EXPORT.md`
12. `31_AISCC_RULES__ASSET_GIT_AND_ENCODING_POLICY.md`
13. `32_AISCC_RULES__PROJECT_SOURCE_MIRROR.md`
14. `33_AISCC_RULES__DOCUMENT_LANGUAGE_POLICY.md`

`AUDIT/` 디렉터리의 파일은 사람 검토용이며 새 Browser Project active source에 기본 업로드하지 않는다.

## 4. 문서 역할

| group | role |
|---|---|
| `00~01` | 프로젝트 genesis, 임시 권위, 현재 목표와 단계 |
| `10` | Agent instruction transport, canonical authority, conflict stop |
| `20~26` | Browser Command Center의 task 발행·판정·cycle·next-action 운영 |
| `30~31` | IDE Executor report/export, Git/provenance, encoding 안전 규칙 |
| `32` | canonical → Browser Project Source mirror lifecycle |
| `33` | Korean-first 사람 검토 문서와 code identifier 원문 유지 |

## 5. 초기 운영 순서

```text
1. 새 Browser GPT Project 생성
2. 이 active set 14개 전체 업로드
3. P0-2 Product Thesis / Prior-Art Boundary Baseline 작성
4. P0-3 Browser Project bootstrap 확인
5. P0-4 Git repository와 repository canonical 구조 생성
6. Agent transport fresh-session 검증
7. P0-5 first canonical Project Source mirror v1 생성
8. Browser Project의 Seed 14개 전체 제거
9. mirror v1 active set 전체 업로드
10. Seed v1을 historical genesis artifact로만 보존
11. 정상 개발 cycle 시작
```

## 6. repository 생성 후 예상 canonical 구조

```text
.aiassistant/
├── rules/                              # TRACK
├── records/
│   ├── command-center/                 # TRACK
│   └── aiscc/
│       ├── CURRENT_STATE_SUMMARY.md    # TRACK
│       ├── DECISION_REGISTER.md        # TRACK
│       ├── NEXT_ACTIONS.md             # TRACK
│       └── cycles/                     # TRACK: 실제 작업/판정 provenance
├── tasks/
│   ├── active/                         # IGNORE: 실행 중 임시 task
│   └── done/                           # TRACK: AI에게 무엇을 지시했는가
├── reports/
│   ├── target/                         # IGNORE: executor 제출용 임시 bundle
│   └── aiscc/                          # TRACK: curated baseline/handoff only
└── project-sources/
    ├── PROJECT_SOURCE_BUNDLE_REGISTRY.md  # TRACK
    ├── manifests/                         # TRACK
    └── bundles/                           # IGNORE: generated upload copies
```

## 7. 공개 provenance의 세 축

```text
Task File in tasks/done
= AI에게 무엇을 요구했는가

Cycle Record in records/aiscc/cycles
= 실제로 무엇이 일어났고 왜 accept/rework/block했는가

Git commit/diff
= product와 canonical 문서가 실제로 어떻게 바뀌었는가
```

`reports/target`은 위 세 축을 잇는 임시 review artifact이며 최종 공개 이력의 정본이 아니다.

## 8. 다음 작업

```text
work_type: DOC_BASELINE_UPDATE
next_action: AISCC Product Thesis and Prior-Art Boundary Baseline
reason: Prior-Art audit 결과를 repository 이전의 명시적 project thesis와 DO-NOT-CLAIM boundary로 고정
```
