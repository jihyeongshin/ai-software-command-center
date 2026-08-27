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

- decision: Browser Project의 `AISCC-BOOTSTRAP-SEED-V1`은 P0-5 complete replacement가 Human-confirmed될 때까지 immutable temporary authority였으며, complete replacement 확인 후 historical genesis provenance로 retire한다.
- decision_status: `RETIRED / HISTORICAL`
- provenance: Seed v1 index, Project Source mirror rule, P0-5 Human complete replacement evidence
- implementation_status: Browser active Seed `0/14`; mirror v1 active `18/18`
- verification_status: `HUMAN_PROVIDED / CONFIRMED`
- owner / future task: historical bootstrap provenance; current Browser source lifecycle owner는 repository canonical mirror policy
- supersession_rule: Seed를 current authority로 재활성화하지 않는다. 향후 Browser source는 repository canonical에서 생성한 complete mirror replacement만 사용한다.


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
- decision_status: `ACCEPTED_PROJECT_DECISION / ACTIVE`
- provenance: Seed index, Project Source mirror rule, P0-4 acceptance, P0-5 terminal Human sync evidence
- implementation_status: first repository mirror v1 complete replacement `IMPLEMENTED`
- verification_status: `HUMAN_PROVIDED / CONFIRMED`; active mirror `18/18`, Seed active `0`
- active mirror: `AISCC-PROJECT-SOURCE-MIRROR-V1`
- mirror snapshot canonical commit: `0dc4e19a6da31c22e08d144eaba24209a4476b4d`
- owner / future task: repository canonical owners; future mirror refreshes follow `.aiassistant/rules/AISCC_PROJECT_SOURCE_MIRROR.md`
- supersession_rule: Browser direct edit는 canonical change가 아니며 tracked manifest + generated bundle + Human complete replacement cycle만 mirror state를 갱신한다.


## AISCC-PROJECT-SOURCE-MIRROR-V1-ACTIVATION

- decision: `AI Software Command Center` Browser Project의 active source를 Bootstrap Seed v1에서 `AISCC-PROJECT-SOURCE-MIRROR-V1` `18/18` complete replacement로 전환한다.
- decision_status: `HUMAN_PROVIDED / ACCEPTED / CLOSED`
- provenance:
  - sync-ready canonical snapshot Commit A: `0dc4e19a6da31c22e08d144eaba24209a4476b4d`
  - regenerated candidate Commit B: `25a81a9d42ecee0185fb36f83b86348b575905aa`
  - Human complete replacement result: Seed `0`, mirror `18`, metadata/hash `complete`
- implementation_status: `BROWSER_PROJECT_SOURCE_REPLACEMENT_COMPLETED`
- verification_status: `HUMAN_PROVIDED / CONFIRMED`
- authority_effect:
  - repository canonical remains editable owner
  - Browser Project Source becomes read-only mirror v1
  - Bootstrap Seed v1 becomes historical-only
- owner / future task: future mirror refresh Task only when active canonical changes warrant a new Browser source snapshot
- supersession_rule: future mirror version may supersede v1 only through complete replacement; mixed current authority is forbidden.


## AISCC-P1-1-CORE-DOMAIN-STATE-MACHINE-V1

- decision: AISCC core domain/orchestration은 `WorkRun` System-owned authoritative aggregate, exact nine-state `WorkflowState`, request/evaluation/decision/mutation separation, state-version concurrency guard, durable transition provenance를 canonical design으로 사용한다.
- decision_status: `HUMAN_PROVIDED / ACCEPTED / CLOSED`
- provenance:
  - `20260826_2157_aiscc-core-domain-and-state-machine-design-1`
  - `20260827_1008_aiscc-p1-1-judgment-transition-admission-semantic-alignment-rework-1`
  - `20260827_1008_aiscc-p1-1-human-gate-result-projection-alignment-rework-1`
  - Human P1-1 final review `ACCEPTED`
  - `.aiassistant/records/aiscc/cycles/20260827_1115_aiscc-p1-1-core-domain-state-machine-design-final-acceptance-1.cycle.md`
- implementation_status: `NOT_IMPLEMENTED`
- verification_status: semantic design + Human acceptance complete; runtime implementation/evidence `DEFERRED`
- canonical owners:
  - `.aiassistant/rules/AISCC_ARCHITECTURE.md`
  - `.aiassistant/rules/AISCC_ORCHESTRATION.md`
- exact WorkflowState:
  - `READY`
  - `RUNNING`
  - `ADMISSION_PENDING`
  - `HUMAN_REQUIRED`
  - `BLOCKED`
  - `REWORK_REQUIRED`
  - `ACCEPTED`
  - `REJECTED`
  - `FAILED`
- authority invariants:
  - `AgentOutput != SystemState`
  - `EvidenceCandidate != AdmittedEvidence`
  - `HumanGateStatus != HumanResult != Judgment != TransitionDecision != WorkflowState`
  - `ExecutorCompleted != WorkRun.ACCEPTED`
  - `WorkRun.ACCEPTED != Project.CLOSED`
- concurrency invariant: transition request는 authoritative current state/version에 대해 평가하며 stale request는 deny되고 current state를 overwrite하지 않는다.
- persistence invariant: authoritative projection과 append-only transition/provenance는 restart 후 reconstruct 가능해야 한다.
- future owners: `P1-2`, `P1-3`, `P1-4`, `P1-5`, `P1-6`, `P1-7`, `P1-8`
- supersession_rule: state set, transition authority, Judgment ordering, Human gate/result projection, concurrency/persistence semantic 변경은 별도 baseline Task와 Human acceptance가 필요하다.

## AISCC-P1-2-SECURITY-SANDBOX-RUNTIME-BOUNDARY-V1

- decision: AISCC security/runtime boundary는 `SecurityAdmissionDecision = ALLOW | DENY`, versioned RuntimeMode profiles, deny-by-default resource admission, exact action-class × current `WorkflowState` eligibility, state/version-bound capability invalidation, exact public requester/session→target-run cancel authorization, secret/isolation/cleanup, bounded timeout/retry/cancel, application idempotency/abuse/budget와 Replay failure-domain separation을 canonical design으로 사용한다.
- decision_status: `HUMAN_PROVIDED / ACCEPTED / CLOSED`
- provenance:
  - `20260827_1115_aiscc-security-sandbox-runtime-boundary-design-1`
  - `20260827_1247_aiscc-p1-2-security-action-state-and-public-cancel-authorization-alignment-rework-1`
  - Human P1-2 final review `ACCEPTED`
  - `.aiassistant/records/aiscc/cycles/20260827_1342_aiscc-p1-2-security-sandbox-runtime-boundary-final-acceptance-1.cycle.md`
- implementation_status: `NOT_IMPLEMENTED`
- verification_status: semantic design + Human acceptance complete; safeguard runtime evidence deferred to P1-3
- canonical owner: `.aiassistant/rules/AISCC_SECURITY_SANDBOX.md`
- authority invariants:
  - `SecurityAdmissionDecision = ALLOW | DENY`
  - `fresh state_version != action admissible in current WorkflowState`
  - `PUBLIC_RUN_OR_REPLAY_VISIBILITY != PUBLIC_CANCEL_AUTHORITY`
  - `RUN_ID_KNOWLEDGE != TARGET_RUN_CONTROL_AUTHORIZATION`
  - `LIVE_UNAVAILABLE_OR_BUDGET_EXHAUSTED → RECORDED_REPLAY_REMAINS_AVAILABLE`
- implementation handoff: P1-3 is the first safeguard implementation + runtime proof owner.
- release handoff: P3-3 owns current provider/configuration and release-time reverification, not first safeguard implementation.
- supersession_rule: permission/state/cancel/secret/isolation/budget/fallback semantics를 변경하려면 별도 security baseline Task와 Human acceptance가 필요하다.

## AISCC-P1-3-RUNTIME-SUBSTRATE-V1

- decision: AISCC P1-3 application/runtime baseline은 CPython 3.12.x, FastAPI/Pydantic v2/Uvicorn HTTP boundary, uv/Hatchling build, exact `src/aiscc/`·`tests/` layout과 Docker Engine Linux containers + Compose v2 sandbox/evidence substrate를 사용한다.
- decision_status: `HUMAN_PROVIDED / ACCEPTED`
- provenance:
  - `20260827_1442_aiscc-p1-3-runtime-substrate-baseline-design-with-blocker-provenance-commit-1`
  - Human Runtime Substrate final review `ACCEPTED`
  - `.aiassistant/records/aiscc/cycles/20260827_1513_aiscc-p1-3-runtime-substrate-baseline-final-acceptance-1.cycle.md`
- implementation_status: `NOT_STARTED`
- runtime_security_proof: `NOT_EXECUTED`
- canonical owner: `.aiassistant/rules/AISCC_RUNTIME_SUBSTRATE.md`
- exact bootstrap boundary: canonical owner section 11 allowlist only; `workflow`, `providers`, `persistence`, migrations, deployment와 actual public scenario corpus 제외
- authority invariants:
  - `SecurityAdmissionDecision != TransitionDecision`
  - `security test state fixture != P1-4 workflow kernel`
  - Docker availability/container strategy `!=` isolation proof
- implementation handoff: P1-3 may prepare the accepted Python/uv environment, create only the exact bootstrap and implement/verify P1-2 safeguards.
- supersession_rule: runtime major/minor, framework major boundary, build/package strategy 또는 sandbox substrate 변경은 separate Human-accepted baseline update가 필요하다.

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
