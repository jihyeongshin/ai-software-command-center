# AISCC Decision Register

각 entry는 decision과 implementation/verification evidence를 분리한다. Executor report나 local commit은 Human acceptance 또는 external runtime proof를 대신하지 않는다.

## AISCC-ORCHESTRATION-CORE-V1

- decision: orchestration core는 AISCC가 직접 소유하는 custom explicit state machine을 사용하며 LangGraph를 core로 사용하지 않는다.
- decision_status: `ACCEPTED_PROJECT_DECISION`
- provenance: P0-1 bootstrap decision; P0-2 Human acceptance
- implementation_status: `NOT_EXECUTED`
- verification_status: `DEFERRED`
- owner / future task: `P1-1 Core Domain / State Machine Design` 및 후속 Governance Kernel implementation
- supersession_rule: architecture baseline을 바꾸는 명시적 Human-accepted decision만 supersede할 수 있다.

## AISCC-PRODUCT-THESIS-V1

- decision: AISCC는 Coding Agent가 아니라 `Software Engineering Governance Control Plane`이다.
- decision_status: `ACCEPTED / CLOSED`
- provenance: accepted P0-2 Task와 terminal Cycle; canonical report `.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md`
- implementation_status: `BASELINE_CANONICALIZED`; product runtime은 `NOT_EXECUTED`
- verification_status: Human P0-2 acceptance recorded; runtime/product effectiveness는 `DEFERRED`
- owner / future task: canonical Product Thesis; future capability claims는 해당 implementation/evidence Task
- supersession_rule: product-thesis baseline update Task와 Human judgment가 필요하다.

## AISCC-PRIOR-ART-BOUNDARY-V1

- decision: known prior-art primitive를 AISCC의 최초 발명으로 주장하지 않으며 strict `DO-NOT-CLAIM`과 eight differentiation hypotheses를 유지한다.
- decision_status: `ACCEPTED / CLOSED`
- provenance: P0-2 primary-source audit와 Human acceptance; `.aiassistant/reports/aiscc/AISCC_PRIOR_ART_BOUNDARY.md`
- implementation_status: `BASELINE_CANONICALIZED`
- verification_status: P0-2 cutoff 기준 accepted; future public claims는 current source/evidence로 재검증 필요
- owner / future task: public documentation, evaluation, submission owner Tasks
- supersession_rule: 새 evidence는 factual register를 보강할 수 있으나 Human-accepted baseline 없이는 claim ceiling을 약화할 수 없다.

## AISCC-COMPETITION-PUBLIC-RUNTIME-V1

- decision: public mode는 `PUBLIC_REPLAY_WITH_BOUNDED_LIVE`; default는 zero-inference `RECORDED_RUN_REPLAY`; Live는 fixed synthetic repository와 allowlisted bounded scenario만 허용하며 실패·예산 소진 시 Replay를 유지한다.
- decision_status: `ACCEPTED_PROJECT_DECISION`
- provenance: P0-2 Task, runtime boundary, terminal Cycle, Human acceptance
- implementation_status: `NOT_EXECUTED`
- verification_status: product boundary accepted; runtime/security/provider/browser verification `DEFERRED`
- owner / future task: `P1-2`, `P1-3`, `P2-3`, `P3-3`
- supersession_rule: public permission, budget, Replay fallback을 약화하는 변경은 security/runtime baseline과 Human judgment가 필요하다.

## AISCC-COMPETITION-DEPLOYMENT-DIRECTION-V1

- decision: Public UI/Replay는 `Cloudflare Pages`, Bounded Live API/PostgreSQL은 `Railway Hobby` Singapore, LLM은 separate `OpenAI API Project`; cost target 약 `USD 30`, absolute cap plan `USD 50`.
- decision_status: `HUMAN_PROVIDED / ACCEPTED_PROJECT_DECISION`
- provenance: P0-2 terminal Cycle의 Human Project Decision
- implementation_status: `NOT_EXECUTED`
- verification_status: `provider_capability_verification: DEFERRED`
- owner / future task: security/runtime design·implementation 이후 `P3-3 Public Release and Competition Submission`
- supersession_rule: current official provider capability/pricing/region/budget-control verification과 Human decision 없이 provider direction을 configured fact로 승격하거나 변경하지 않는다.

대표 URL shape, provider plan/region, pricing, model, call/token/run cap, resource, credential, spend guard 또는 service URL은 P0-4에서 검증·생성·설정되지 않았다.

## AISCC-BOOTSTRAP-SEED-AUTHORITY-V1

- decision: Browser Project의 `AISCC-BOOTSTRAP-SEED-V1`은 P0-5 complete replacement가 Human-confirmed될 때까지 immutable temporary authority다.
- decision_status: `ACTIVE_TEMPORARY_BROWSER_AUTHORITY`
- provenance: Seed v1 index와 Project Source mirror rule
- implementation_status: Browser active set `14/14`은 P0-3 Human-confirmed; P0-5 replacement `NOT_EXECUTED`
- verification_status: current Browser sync beyond P0-3는 `HUMAN_OWNED / DEFERRED`
- owner / future task: `P0-5 First Project Source Mirror v1`
- supersession_rule: P0-5의 complete active-set replacement 확인 시 historical genesis provenance로 retire한다. Seed와 mirror를 mixed current authority로 유지하지 않는다.

## AISCC-ROOT-AGENTS-TRANSPORT-V1

- decision: repository-root `AGENTS.md`는 tracked thin transport bootstrap이며 policy authority가 아니다.
- decision_status: `ACCEPTED_PROJECT_DECISION`
- provenance: Seed agent authority rule과 P0-4 Task
- implementation_status: `IMPLEMENTED_IN_P0_4`
- verification_status: thin body와 Git tracking 검증 대상
- owner / future task: `.aiassistant/rules/AISCC_AGENTS.md`; transport 변경 Task
- supersession_rule: canonical rule body를 root file에 복제하지 않으며 authority 변경은 rule update가 필요하다.

## AISCC-CANONICAL-MIRROR-AUTHORITY-SPLIT-V1

- decision: local repository canonical은 editable source owner이고 Browser Project Source는 Human-uploaded read-only mirror다.
- decision_status: `ACCEPTED_PROJECT_DECISION`
- provenance: Seed index, Project Source mirror rule, P0-4 Task
- implementation_status: repository canonical candidate created; first mirror `NOT_EXECUTED`
- verification_status: local canonical integrity는 P0-4 executor evidence; Browser replacement는 `HUMAN_OWNED / P0-5`
- owner / future task: repository canonical owners; mirror lifecycle는 P0-5
- supersession_rule: Browser direct edit는 canonical change가 아니며 complete mirror generation/sync cycle만 mirror state를 갱신한다.

## AISCC-P1-SAFEGUARD-BEFORE-RELEASE-V1

- decision: P1 security/runtime design 뒤에 dedicated safeguard implementation + verification을 완료하고 accepted하기 전에는 public bounded Live release로 진행할 수 없다.
- decision_status: `HUMAN_PROVIDED / ACCEPTED_QUEUE_INVARIANT`
- provenance: P0-2 Human queue correction과 P0-4 Task
- implementation_status: `NOT_EXECUTED`
- verification_status: `DEFERRED_TO_P1_3`
- owner / future task: `P1-3 Security / Runtime Safeguard Implementation and Verification`; P3-3은 재검증·release configuration owner
- supersession_rule: P3-3을 first safeguard implementation stage로 바꾸는 queue는 금지하며 Human-accepted security policy change 없이는 invariant를 제거할 수 없다.

```text
NO_PUBLIC_BOUNDED_LIVE_RELEASE
BEFORE
P1_SECURITY_RUNTIME_SAFEGUARD_IMPLEMENTATION_AND_VERIFICATION_ACCEPTED
```

## AISCC-P0-4-ENVIRONMENT-CONVENTION-V1

- decision: IntelliJ workspace `C:\Users\oracl\IdeaProjects\ai-software-command-center`와 Human-created empty public Git remote clone을 P0-4 precondition으로 사용한다. `.idea/`는 ignored local metadata이고 `.aiassistant/bootstrap-input/`은 ignored temporary staging이다.
- decision_status: `HUMAN_PROVIDED / ACCEPTED_OPERATIONAL_CONVENTION`
- provenance: environment-gap Cycle과 current P0-4 rework Task
- implementation_status: ignore policy와 canonical bootstrap에 반영
- verification_status: local preflight `EXECUTED_PASS`; remote network state는 조회하지 않음
- owner / future task: repository bootstrap/Git policy
- supersession_rule: operational environment 변경 시 해당 Task가 새 root/repository/metadata boundary를 명시해야 한다.

이 environment convention은 product architecture 결정이 아니다.
