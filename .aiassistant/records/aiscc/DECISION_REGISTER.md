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

- decision: AISCC security/runtime boundary는 RuntimeMode별 permission profile, deny-by-default security admission, exact action-class × WorkflowState eligibility, state/version-bound capability freshness, secret/run isolation, bounded timeout/retry/cancel, idempotency/abuse/budget admission, public cancel target authorization, Replay failure-domain separation을 canonical design으로 사용한다.
- decision_status: `HUMAN_PROVIDED / ACCEPTED / CLOSED`
- provenance:
  - `20260827_1115_aiscc-security-sandbox-runtime-boundary-design-1`
  - `20260827_1247_aiscc-p1-2-security-action-state-and-public-cancel-authorization-alignment-rework-1`
  - `20260827_1247_aiscc-p1-2-security-action-state-and-cancel-authorization-hold-1.cycle.md`
  - Human P1-2 final review `ACCEPTED`
  - `.aiassistant/records/aiscc/cycles/20260827_1342_aiscc-p1-2-security-sandbox-runtime-boundary-final-acceptance-1.cycle.md`
- implementation_status: `NOT_IMPLEMENTED`
- verification_status: semantic design + Human acceptance complete; safeguard runtime evidence `DEFERRED_TO_P1_3`
- canonical owner: `.aiassistant/rules/AISCC_SECURITY_SANDBOX.md`
- security decision: `SecurityAdmissionDecision = ALLOW | DENY`; unknown/ambiguous permission fails closed.
- action/state invariant: fresh `state_version` is necessary but not sufficient; action class must be admissible in the authoritative current `WorkflowState`.
- capability invariant: state/version change invalidates prior permission; normal execution/provider capability cannot remain usable in terminal state solely because its lease has not expired.
- cancel invariant: public run/replay visibility or run ID knowledge does not grant cancel authority; public cancel requires exact requester/session/principal → target-run control authorization and fresh target state/version.
- public Live invariant: fixed synthetic repository + allowlisted scenario + server-fixed provider/model + bounded calls/retry/time/budget; no free-form task/external repo/upload/arbitrary shell/network/owner workspace access.
- fallback invariant: `LIVE_UNAVAILABLE_OR_BUDGET_EXHAUSTED → RECORDED_REPLAY_REMAINS_AVAILABLE`.
- owner / future task:
  - `P1-3 Security / Runtime Safeguard Implementation and Verification` = first safeguard implementation + runtime proof
  - `P3-3 Public Release and Competition Submission` = current provider/release configuration reverification
- supersession_rule: weakening public hard prohibitions, fail-closed policy, secret/run isolation, action-state eligibility, cancel authorization, budget/fallback or P1-3-before-release invariant requires a separate Human-accepted security baseline change.

## AISCC-P1-3-RUNTIME-SUBSTRATE-V1

- decision: AISCC executable application/runtime substrate는 Python CPython `3.12.x` (`>=3.12,<3.13`), FastAPI/Pydantic v2/Uvicorn HTTP boundary, `uv` + Hatchling + `pyproject.toml` + `uv.lock`, canonical roots `src/aiscc/` and `tests/`, versioned non-secret security config `config/security/`, Docker Engine Linux containers + Docker Compose v2 sandbox/evidence substrate를 사용한다.
- decision_status: `HUMAN_PROVIDED / ACCEPTED`
- provenance:
  - P1-3 preflight blocker: `BLOCKED_RUNTIME_SUBSTRATE_DECISION_REQUIRED`
  - blocker base commit: `4ec8bf49330128f5fccb70d94a863dc57f9984d2`
  - runtime-substrate design provenance commit: `95de4ae9d5ec36bed8636b608dc5729b47e815fe`
  - `20260827_1442_aiscc-p1-3-runtime-substrate-baseline-design-with-blocker-provenance-commit-1`
  - Human Runtime Substrate final review: `ACCEPTED`
  - `.aiassistant/records/aiscc/cycles/20260827_1513_aiscc-p1-3-runtime-substrate-baseline-final-acceptance-1.cycle.md`
- canonical owner: `.aiassistant/rules/AISCC_RUNTIME_SUBSTRATE.md`
- implementation_status: `NOT_STARTED`
- runtime_security_proof: `NOT_EXECUTED`
- primary runtime: `Python / CPython 3.12.x`
- HTTP/input-output boundary: `FastAPI + Pydantic v2 + Uvicorn`; framework does not own workflow/security authority.
- package/build: `uv`, Hatchling, root `pyproject.toml`, root `uv.lock`, exact 3.12 patch pinned by authorized implementation Task.
- source/test roots:
  - `src/aiscc/`
  - `tests/`
  - `config/security/`
  - `containers/p1_3/`
- security/runtime authority:
  - `src/aiscc/security/` owns `SecurityAdmissionDecision` policy;
  - `src/aiscc/runtime/` executes admitted capabilities and cleanup;
  - `src/aiscc/workflow/` remains P1-4-only;
  - `src/aiscc/providers/` remains P1-5-only.
- sandbox/evidence: Docker Engine Linux containers + Docker Compose v2; actual isolation/network/cleanup proof remains P1-3 runtime evidence.
- persistence direction: PostgreSQL + SQLAlchemy 2 async/asyncpg + Alembic; schema/migrations are not authorized by this baseline or P1-3 bootstrap.
- secret boundary: configuration/domain carries opaque `secret_ref`/capability reference only; no committed credential.
- bootstrap authority: section 11 of `AISCC_RUNTIME_SUBSTRATE.md` is the exact Human-accepted P1-3 creation allowlist.
- version/dependency authority:
  - Python major/minor, framework major boundary, package/build strategy, sandbox strategy, persistence-direction changes require separate Human-accepted baseline update;
  - exact Python `3.12.x` patch and compatible dependency patch/minor may be resolved by an explicitly authorized implementation/maintenance Task with lock/evidence provenance.
- non-substitution:
  - `runtime substrate accepted != P1-3 safeguard accepted`;
  - `Docker installed != isolation proof`;
  - `security test fixture != P1-4 state-machine kernel`.
- supersession_rule: a load-bearing change to runtime family, build/package authority, canonical roots, sandbox/evidence strategy or the P1-3/P1-4/P1-5 ownership boundary requires a separate Human-accepted baseline.

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

## AISCC-P1-3-SECURITY-RUNTIME-SAFEGUARDS-V1

- decision: P1-2의 accepted security/runtime boundary를 Python/Docker 기반 executable safeguard로 구현하고 non-substitutable runtime proof를 완료한 최종 P1-3 candidate를 canonical implementation baseline으로 채택한다.
- decision_status: `HUMAN_PROVIDED / ACCEPTED / CLOSED`
- provenance:
  - runtime substrate: `AISCC-P1-3-RUNTIME-SUBSTRATE-V1`
  - final Executor Task: `20260827_1941_aiscc-p1-3-runtime-proof-assertion-coverage-rework-1`
  - final pre-closure HEAD: `575fb3c4623a28b8537d15c8b34b838982f96ce2`
  - Human P1-3 final review: `ACCEPTED`
  - terminal Cycle: `.aiassistant/records/aiscc/cycles/20260827_1941_aiscc-p1-3-security-runtime-safeguard-final-acceptance-1.cycle.md`
- implementation_status: `IMPLEMENTED / ACCEPTED`
- final candidate:
  - path count: `55`
  - aggregate SHA-256: `4a9f49a70bbe6cc628a9bc9e6612d07b724876beaf3fd0e672b9815343018c4c`
- static/targeted verification:
  - uv build: `PASS`
  - Ruff: `PASS`
  - mypy strict: `PASS`
  - unit + integration: `26 PASS`
- runtime verification:
  - Docker health: `PASS`
  - runtime security tests: `10 PASS`
  - mandatory proof classes: `8 / 8 EXECUTED_PASS`
  - final container/network residue: `none`
- accepted security properties:
  - fail-closed requester/task/resource/limit/budget/idempotency authority;
  - exact action × WorkflowState policy;
  - state/version/RuntimeMode-bound capability lifetime;
  - typed exact resource grants;
  - public cancel target authorization and idempotency;
  - capability-gated process/Docker/network side effects;
  - capability-gated product Docker reads/cleanup;
  - secret non-exposure;
  - Docker filesystem/process isolation;
  - default network deny + exact internal allow;
  - bounded timeout/retry/cancel;
  - application idempotency/abuse/budget;
  - cleanup/residue/quarantine;
  - Replay independence from simulated Live/provider/budget failure.
- authority boundary:
  - `SecurityAdmissionDecision != TransitionDecision`;
  - P1-3 `WorkflowSnapshot` fixtures are not authoritative P1-4 `WorkRun`;
  - caller-created authority values do not become trusted System evidence merely by being typed.
- release effect:
  - `NO_PUBLIC_BOUNDED_LIVE_RELEASE BEFORE P1 security safeguard acceptance` prerequisite is now satisfied;
  - Public Bounded Live itself remains `NOT_RELEASED`.
- owner / future task:
  - P1-4 owns authoritative WorkRun/state/version/TransitionDecision;
  - P1-6 owns evidence admission;
  - P1-7 owns Human gate/result/Judgment;
  - P1-5 owns provider/tool execution.
- supersession_rule: weakening fail-closed admission, RuntimeMode/state-version capability binding, sandbox isolation, public cancel authority, proof non-substitution or P1-4/P1-5 owner separation requires a separate Human-accepted security baseline update.

## AISCC-P1-4-EXPLICIT-STATE-MACHINE-KERNEL-V1

- decision: accepted P1-1 explicit workflow semantics를 PostgreSQL-backed authoritative state-machine kernel로 구현한 final P1-4 candidate를 canonical implementation baseline으로 채택한다.
- decision_status: `HUMAN_PROVIDED / ACCEPTED / CLOSED`
- provenance:
  - final Executor Task: `20260828_1110_aiscc-p1-4-denied-precreation-retry-consistency-semantics-rework-1`
  - final pre-terminal-closure HEAD: `aec4d24ba3ae23d8252c9582130aea99aac333a1`
  - Human P1-4 final review: `ACCEPTED`
  - terminal Cycle: `.aiassistant/records/aiscc/cycles/20260828_1110_aiscc-p1-4-explicit-state-machine-kernel-final-acceptance-1.cycle.md`
- implementation_status: `IMPLEMENTED / ACCEPTED`
- final candidate:
  - path count: `19`
  - aggregate SHA-256: `1316fd14faf6a2ad85f43ae9e9a2bab45c1736e4f28bea40d35865f53dee4cb5`
- accepted state model:
  - exact `WorkflowState` count: `9`
  - exact allowed transition pairs: `22`
  - terminal states: `ACCEPTED`, `REJECTED`, `FAILED`
  - `RuntimeMode != WorkflowState`
- accepted authority:
  - `TransitionRequest → TransitionEvaluation → TransitionDecision → atomic authoritative mutation`;
  - `Judgment != TransitionDecision`;
  - `SecurityAdmissionDecision != TransitionDecision`;
  - production P1-4 cannot mint P1-6 Evidence or P1-7 Human/Judgment authority;
  - raw evidence/Human/Judgment refs are non-authoritative without owner-bound facts.
- persistence/concurrency:
  - PostgreSQL + SQLAlchemy 2 async + asyncpg + Alembic;
  - append-only request/evaluation/decision provenance;
  - per-run/per-request serialization + row lock + CAS;
  - stale-request deny;
  - same-request immutable idempotency;
  - admitted decision/projection mutation atomicity;
  - restart-durable projection/history;
  - projection/event mismatch fail-closed.
- denied-precreation semantics:
  - complete compatible DENIED-only history with absent projection remains authoritative `NONE/v0`;
  - corrected fresh create may proceed;
  - admitted history, partial/orphaned history or immutable run-identity conflict fails closed.
- verification:
  - targeted PostgreSQL integration: `17 PASS`;
  - full unit + integration: `74 PASS`;
  - PostgreSQL: `17.6`;
  - Alembic head: `20260828_0001`;
  - final Task-owned container/network residue: `none`.
- next-owner boundary:
  - P1-5 owns provider/tool execution adapters and execution events/status;
  - P1-6 owns evidence admission;
  - P1-7 owns Human gate/result/Judgment;
  - P1-8 owns Cycle admission/project closure/NextAction projection.
- supersession_rule: changing the exact 9-state set, exact transition authority, state-version concurrency rule, owner-bound guard separation, denied audit semantics, atomicity or consistency fail-closed behavior requires a separate Human-accepted P1-4 baseline update.

## AISCC-P1-5-PROVIDER-TOOL-EXECUTION-DESIGN-V1

- decision: P1-5 provider/tool execution은 exact four-value `ExecutionStatus`, server-owned provider/tool selector authority, P1-3-mediated SECRET capability, bounded AgentExecutionService loop, versioned ProviderProfile/ToolRegistry, append-only execution operation/status persistence, unknown-outcome no-blind-retry, stateless OpenAI Responses V1 local-history continuation, P1-6 producer-ref handoff를 canonical design으로 사용한다.
- decision_status: `HUMAN_PROVIDED / ACCEPTED / CLOSED`
- provenance:
  - initial design Task: `20260828_1110_aiscc-p1-5-provider-tool-execution-contract-design-freeze-with-p1-4-terminal-commit-1`
  - final rework Task: `20260828_1417_aiscc-p1-5-secret-operation-protocol-and-openai-state-mode-design-rework-1`
  - final design base commit: `d96949f3643e6a0610942e33d70e9da259e1e432`
  - Human P1-5 design final review: `ACCEPTED`
  - terminal Cycle: `.aiassistant/records/aiscc/cycles/20260828_1529_aiscc-p1-5-provider-tool-execution-design-final-acceptance-1.cycle.md`
- canonical owner: `.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md`
- accepted design SHA-256: `12070677aa1cfa74b7eea9a52db24f78aacd2bf23d655f125a7689797d172443`
- implementation_status: `READY / NOT_STARTED`
- exact ExecutionStatus:
  - `NOT_STARTED`
  - `RUNNING`
  - `EXECUTOR_COMPLETED`
  - `EXECUTION_FAILED`
- authority invariants:
  - `ExecutionStatus != WorkflowState`;
  - pure execution status/event admission does not increment `WorkRun.state_version`;
  - `EXECUTOR_COMPLETED != ACCEPTED`;
  - `EXECUTION_FAILED != FAILED`;
  - P1-5 provider/tool/secret selector attestation does not mint P1-3 `SecurityAdmissionDecision`, `ResourceGrant` or `Capability`;
  - `PROVIDER Capability != SECRET Capability`;
  - `TOOL Capability != SECRET Capability`;
  - `ToolOutput/AgentOutput != AdmittedEvidence`.
- provider/tool resource contract:
  - ProviderProfile and ToolRegistry are server-owned/versioned;
  - public/Agent input cannot select provider/model/tool/endpoint/secret;
  - exact operation/argument fingerprints bind P1-5 selector authority and P1-3 security capability.
- secret contract:
  - secret material is reachable only through server-side mediated adapter/dispatcher after exact P1-5 SecretUse attestation + P1-3 SECRET capability;
  - raw secret is excluded from Agent/workspace/tool args/provider durable protocol history/public provenance/Replay.
- operation contract:
  - pre-side-effect deny, pre-dispatch cancel, dispatched known outcome and dispatched unknown outcome are exact representable terminal paths;
  - unknown outcome cannot be blindly retried;
  - `RETRY_EXHAUSTED` is attempt-level.
- OpenAI Responses V1:
  - custom functions only;
  - `background=false`, `stream=false`, `store=false`, `parallel_tool_calls=false`, `truncation=disabled`;
  - no provider Conversation authority;
  - no `previous_response_id` sole continuation;
  - AISCC durable private local protocol history is continuation authority;
  - `queued`, `in_progress`, `completed`, `failed`, `cancelled`, `incomplete` are explicitly mapped.
- mode contract:
  - OWNER = bounded server-owned profile/registry;
  - REPLAY = provider/tool/process/network execution exactly zero;
  - PUBLIC LIVE = fixed synthetic repo/scenario/server profile with bounded resources; release remains `NOT_RELEASED`.
- owner handoff:
  - P1-5 runtime implementation may produce immutable execution/output/submission refs;
  - P1-6 remains sole evidence admission owner;
  - P1-7/P1-8 remain separate.
- supersession_rule: changing exact ExecutionStatus, provider/tool/secret authority ownership, unknown-outcome retry semantics, Responses V1 continuation authority, Replay zero-execution, or P1-6 non-substitution requires a separate Human-accepted P1-5 design baseline update.

## AISCC-P1-5-PROVIDER-TOOL-EXECUTION-RUNTIME-V1

- decision: Human-accepted P1-5 provider/tool execution design을 PostgreSQL-backed durable execution runtime으로 구현한 final 42-path candidate를 canonical implementation baseline으로 채택한다.
- decision_status: `HUMAN_PROVIDED / ACCEPTED / CLOSED`
- provenance:
  - final Executor Task: `20260828_2215_aiscc-p1-5-missing-provider-usage-token-accounting-rework-1`
  - final pre-terminal-closure HEAD: `15036a5ff316fccbd6d891b9ce43563de056e342`
  - Human P1-5 runtime final review: `ACCEPTED`
  - terminal Cycle: `.aiassistant/records/aiscc/cycles/20260828_2329_aiscc-p1-5-provider-tool-execution-runtime-final-acceptance-1.cycle.md`
- implementation_status: `IMPLEMENTED / ACCEPTED`
- final candidate:
  - path count: `42`
  - aggregate SHA-256: `ffeb5ba70649c564c482c2cff79ce8e2b0a462f811d8e03f2c1096f170bd39d6`
- accepted execution authority:
  - exact four-value `ExecutionStatus`;
  - execution status/events remain separate from P1-4 WorkflowState/state_version;
  - PostgreSQL restart-durable ExecutionAttempt/Operation/event projections;
  - server-owned ProviderProfile/ToolRegistry;
  - P1-5 selector authority + P1-3 ResourceGrant/SecurityAdmissionDecision/Capability composition;
  - exact consumed-authority secret-resolution lease;
  - exact Tool underlying-resource requirements;
  - durable bounded AgentExecutionService;
  - per-side-effect WorkRun/state-version freshness;
  - fail-closed workflow-left-running terminalization;
  - local-history-only Responses continuation;
  - unknown-outcome no-blind-retry;
  - conservative missing-usage token accounting;
  - Replay provider/tool/process/network/secret execution exactly zero.
- Responses V1:
  - official OpenAI Python SDK;
  - acceptance uses local deterministic fake endpoint only;
  - `background=false`, `stream=false`, `store=false`, `parallel_tool_calls=false`, `truncation=disabled`;
  - provider Conversation and `previous_response_id` are not execution authority;
  - durable local private protocol state is continuation authority.
- Public Live acceptance effect:
  - fixed synthetic repository/version + scenario + server profile/tool registry positive local proof passed;
  - this does not release Public Bounded Live;
  - current release status remains `NOT_RELEASED`.
- verification:
  - unit + integration: `145 PASS`;
  - P1-5 persistence/accounting: `23 PASS`;
  - P1-5 runtime: `10 PASS`;
  - P1-3 Docker runtime regression: `10 PASS`;
  - PostgreSQL `17.6`;
  - Alembic head `20260828_0002`;
  - real provider calls `0`;
  - final Task-owned residue `none`.
- evidence handoff:
  - P1-5 producer/output/submission refs are immutable producer authority only;
  - `AgentOutputRef/ToolOutputRef/ExecutionArtifactRef/ExecutionSubmissionRef != EvidenceCandidate admission != AdmittedEvidence`;
  - P1-6 is the sole Evidence Admission owner.
- supersession_rule: weakening durable bounds, state/version freshness, P1-3 security mediation, secret lease, exact tool resource binding, Replay zero-execution, unknown-outcome no-blind-retry, or producer-ref/evidence non-substitution requires a separate Human-accepted P1-5 baseline update.

## AISCC-P1-6-EVIDENCE-ADMISSION-DESIGN-V1

- decision: Use the exact Human-accepted P1-6 contract for immutable requirement/checkpoint authority, fail-closed evidence admission, checkpoint-specific completeness, and owner-bound `G_EVIDENCE` handoff.
- decision_status: `HUMAN_PROVIDED / ACCEPTED / CLOSED`
- provenance:
  - final design rework Task: `20260829_1026_aiscc-p1-6-checkpoint-human-ingress-and-optional-evidence-design-rework-1`
  - predecessor HOLD Cycle: `.aiassistant/records/aiscc/cycles/20260829_1026_aiscc-p1-6-checkpoint-human-ingress-and-optional-evidence-hold-1.cycle.md`
  - Human P1-6 design final review: `ACCEPTED`
  - terminal Cycle: `.aiassistant/records/aiscc/cycles/20260829_1241_aiscc-p1-6-evidence-admission-design-final-acceptance-1.cycle.md`
- canonical owner: `.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md`
- accepted design SHA-256: `0d9d4c194efda37f100c6183d1a7e88e1a09fe073dc3a37bbb5a3e1cd577e463`
- implementation_status: `NOT_STARTED` at design judgment time
- verification_status: semantic design and Human acceptance complete; implementation/runtime evidence `DEFERRED_TO_P1_6_RUNTIME`
- exact evidence profiles:
  - `EXECUTOR_REQUIRED`
  - `REUSE_ALLOWED`
  - `HUMAN_OWNED`
  - `NOT_REQUIRED`
  - `FORBIDDEN`
- accepted checkpoint authority:
  - `EvidenceCheckpoint` is System/TaskContract-owned and binds source plus exact target or transition-purpose identity;
  - Requirement applicability and evidence-set completeness are evaluated for an exact checkpoint without rewriting the full immutable RequirementSet;
  - `EvidenceSetSatisfactionAttestation` commits full-set, checkpoint-subset, and admitted-evidence coverage roots;
  - same Task/run/state/version does not permit cross-checkpoint `G_EVIDENCE` replay.
- accepted Human boundary:
  - `HUMAN_DIRECT_EVIDENCE` is authenticated/server-issued evidence ingress only;
  - `HUMAN_DIRECT_EVIDENCE != HUMAN_P1_7`;
  - P1-6 does not create HumanGate, HumanResult, Judgment, `G_HUMAN_*`, or `G_JUDGMENT_*`.
- supplemental boundary: unrequired material may remain candidate/provenance only and creates no `EvidenceRequirement`, `AdmittedEvidence`, satisfaction mapping, set/root contribution, or `G_EVIDENCE` authority.
- transition boundary: P1-4 remains the exact WorkflowState, TransitionDecision, and atomic mutation owner; P1-6 owns only evidence admission and owner-bound `G_EVIDENCE` facts.
- runtime/release effect: P1-6 runtime is separately accepted and closed in `AISCC-P1-6-EVIDENCE-ADMISSION-RUNTIME-V1`; P1-7/P1-8 remain `NOT_STARTED`; Public Bounded Live remains `NOT_RELEASED`.
- owner / next task: `P1-7 Human Gate and Judgment` authority design before runtime implementation.
- supersession_rule: changing exact profiles, checkpoint authority/applicability, evidence/guard non-substitution, direct/P1-7 Human producer separation, supplemental non-authority, or transition-owner separation requires a separate Human-accepted P1-6 design baseline update.

## AISCC-P1-6-EVIDENCE-ADMISSION-RUNTIME-V1

- decision: Adopt the exact Human-reviewed 21-path P1-6 Evidence Admission runtime as the canonical implementation baseline.
- decision_status: `HUMAN_PROVIDED / ACCEPTED / CLOSED`
- provenance:
  - final Executor rework Task: `20260829_1617_aiscc-p1-6-authoritative-workrun-admission-freshness-rework-1`
  - accepted design terminal commit: `192e223854a02293809cf6675e3a329e099e628d`
  - runtime acceptance commit: `f36f19f5b84cef9bc1452e7cb9e9e36c4ae2873e`
  - Human P1-6 runtime final review: `ACCEPTED`
  - terminal Cycle: `.aiassistant/records/aiscc/cycles/20260829_1920_aiscc-p1-6-evidence-admission-runtime-final-acceptance-1.cycle.md`
- implementation_status: `IMPLEMENTED / ACCEPTED / CLOSED`
- verification_status: `ACCEPTED / CLOSED`
- final candidate:
  - path count: `21`
  - aggregate SHA-256: `a583647cc94028874aaf78727e854b537dd033a3670332737aaa7fa53d6469f9`
- accepted evidence authority:
  - PostgreSQL durable candidates, requests, evaluations, decisions, admitted mappings, set evaluations, attestations, direct-Human ingress, and authority events;
  - System/TaskContract-owned EvidenceCheckpoint and checkpoint-specific Requirement applicability;
  - finite reuse maximum with concurrency and restart preservation;
  - revocation/supersession/correction invalidation across the complete authority revision;
  - authoritative current WorkRun TaskContract/state/state_version freshness under the shared P1-4/P1-6 run serialization boundary;
  - exact checkpoint/state/version/target-use/root-bound `G_EVIDENCE` attestation.
- authority invariants:
  - `EvidenceCandidate != AdmittedEvidence`;
  - `AdmittedEvidenceRef != G_EVIDENCE`;
  - `EvidenceSetSatisfactionAttestation != TransitionDecision`;
  - `HUMAN_DIRECT_EVIDENCE != HUMAN_P1_7`;
  - P1-6 owns only the exact `G_EVIDENCE` fact/attestation;
  - P1-4 retains WorkflowState/TransitionDecision mutation ownership;
  - P1-7 retains HumanGate/HumanResult/Judgment and Human/Judgment guard ownership.
- verification:
  - unique targeted/regression total: `132 PASS`;
  - P1-4 regression: `48 PASS`;
  - P1-5 unit: `43 PASS`;
  - P1-5 integration: `28 PASS`;
  - PostgreSQL: `17.6`;
  - empty DB to migration head: `PASS`;
  - `20260828_0002` to migration head: `PASS`;
  - real provider/external network/credentialed external actions: `0`.
- release/next-phase effect:
  - P1-7 Human Gate and Judgment is the current next phase but remains `NOT_STARTED`;
  - P1-8 remains `NOT_STARTED`;
  - Public Bounded Live remains `NOT_RELEASED`.
- supersession_rule: weakening evidence/admission/attestation non-substitution, checkpoint binding, WorkRun freshness, P1-4 synchronization, Human producer separation, reuse/revocation authority, or restart durability requires a separate Human-accepted P1-6 baseline update.
