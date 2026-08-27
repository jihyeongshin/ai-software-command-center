# AISCC Security / Sandbox / Runtime Boundary

## 1. 문서 상태

| field | value |
|---|---|
| document_id | `AISCC-P1-2-SECURITY-SANDBOX-V1` |
| task_id | `20260827_1247_aiscc-p1-2-security-action-state-and-public-cancel-authorization-alignment-rework-1` |
| work_type | `REWORK` |
| result_status | `ACCEPTED / CLOSED` |
| authority_status | repository canonical accepted P1-2 baseline |
| implementation_status | `NOT_IMPLEMENTED` |
| runtime_security_proof | `NOT_EXECUTED` |
| semantic_owner | security trust boundary, sandbox, permission, secret, isolation, timeout, retry, abuse, budget와 failure-domain semantics |
| accepted predecessor | P1-1 `ACCEPTED / CLOSED`; repository HEAD `db81e065943970dfd19df4013de40106006fbec0` |
| paired accepted baselines | `.aiassistant/rules/AISCC_ARCHITECTURE.md`, `.aiassistant/rules/AISCC_ORCHESTRATION.md` |
| predecessor judgment | `HOLD_REWORK_REQUIRED` — action/state eligibility and public cancel target authorization required |
| human acceptance provenance | `2026-08-27` Human P1-2 final review: `ACCEPTED` |
| terminal cycle | `.aiassistant/records/aiscc/cycles/20260827_1342_aiscc-p1-2-security-sandbox-runtime-boundary-final-acceptance-1.cycle.md` |

This file is the repository canonical accepted P1-2 security/runtime design baseline. It is NOT runtime safeguard proof. 구현 및 runtime security proof status는 각각 `NOT_IMPLEMENTED`, `NOT_EXECUTED`다.

## 2. 범위와 불변식

P1-2는 `RuntimeMode`별 permission profile과 trust crossing을 정의한다. container, worktree, process supervisor, firewall, secret manager, provider adapter 또는 budget ledger의 제품 선택과 구현은 하지 않는다.

Accepted P1-1 불변식은 그대로 유지한다.

```text
AgentOutput != SystemState
EvidenceCandidate != AdmittedEvidence

HumanGateStatus != HumanResult
HumanResult != Judgment
Judgment != TransitionDecision
TransitionDecision != WorkflowState

RuntimeMode != WorkflowState
```

Security layer의 exact decision은 `SecurityAdmissionDecision = ALLOW | DENY`다. 이는 side effect를 실행할 수 있는지에 대한 System-owned 결정이며 `Judgment`, `TransitionDecision`, `WorkflowState` 또는 Human approval이 아니다.

```text
SecurityAdmissionDecision
!= Judgment
!= TransitionDecision
!= WorkflowState
```

- `DENY`는 side effect를 실행하지 않는다.
- pre-run `DENY`는 새 paid run 또는 provider call을 만들지 않는다.
- running attempt의 security failure는 immutable execution/security event를 만들 수 있지만 상태를 직접 바꾸지 않는다. System이 accepted P1-1 current state/version과 기존 transition matrix에 따라 별도 TransitionRequest를 평가한다.
- Agent prose, tool output, Human silence 또는 generic approval은 permission을 만들거나 hard public prohibition을 우회하지 못한다.
- `PermissionProfile`과 policy version은 `WorkRun`에 binding된다. mode/profile 변경은 같은 run의 state transition이 아니며 새 runtime context 또는 새 run을 요구한다.

## 3. principals와 trust zones

### 3.1 principals

| principal | trusted responsibility | 명시적 비권한 |
|---|---|---|
| `HUMAN_OWNER_OPERATOR` | versioned policy/Task authorization, designated Human decision, exceptional owner action | Agent output을 evidence 없이 System state로 만들기; public hard prohibition의 ad-hoc 우회 |
| `AISCC_SYSTEM` | security evaluation/admission, authoritative workflow integration, durable provenance | Human judgment 대행; unknown permission fail-open |
| `AGENT_PROVIDER` | reasoning/action/tool/evidence candidate 생성 | permission 확대, authoritative state mutation, credential 선택, direct host access |
| `PUBLIC_REQUESTER` | allowlisted public scenario/parameter 선택, authorized read, exact requester/run-bound control grant에 따른 cancel 요청 | free-form task, repository/upload, command/network/credential/provider 선택; visibility/run ID만으로 cancel |
| `OWNER_WORKSPACE_REPOSITORY` | owner-authorized canonical source | public 접근; runtime의 무매개 직접 mutation |
| `FIXED_SYNTHETIC_PUBLIC_REPOSITORY` | version-pinned public Live input | owner/private source 혼입; external remote 교체 |
| `RUN_ISOLATION_BOUNDARY` | 한 admitted run의 ephemeral filesystem/process/tool/network capability 보유 | sibling run 또는 host/private zone 접근 |
| `REPLAY_SERVING_PATH` | sanitized stored Replay의 read-only 제공 | LLM/provider 호출, run/source mutation, hidden Live fallback |
| `EXTERNAL_PROVIDER` | server-fixed bounded request 수행과 response 반환 | workflow truth, permission, model/profile 선택 |
| `PERSISTENCE_EVENT_EVIDENCE_STORE` | authoritative state/provenance와 sanitized Replay projection의 논리적 분리 저장 | secret 원문 또는 unsanitized public artifact 저장 |
| `SECRET_CREDENTIAL_STORE` | credential material 보관과 최소 capability 발행 | public 입력/조회, log/replay 노출, Agent 임의 선택 |

### 3.2 trust zones

| zone | contents | default trust posture |
|---|---|---|
| `Z0_PUBLIC_UNTRUSTED` | anonymous/user request, browser-controlled values | 모든 입력 untrusted; allowlisted schema 밖은 deny |
| `Z1_PUBLIC_READ_ONLY` | static page와 sanitized Replay projection | no inference, no mutation, no shell/network/tool execution |
| `Z2_CONTROL_PLANE` | Task/profile/scenario/security/workflow admission | System-owned; policy/version/current-state 검증 필수 |
| `Z3_PER_RUN_ISOLATED` | ephemeral workspace, process tree, scoped tools/capabilities | run별 격리; host/sibling/private access deny |
| `Z4_OWNER_PRIVATE` | canonical owner repository와 approved private context | explicit owner authorization 전에는 deny; public zone과 분리 |
| `Z5_SECRET` | credential material와 capability issuer | raw value 비노출; mediated use only |
| `Z6_EXTERNAL` | LLM/tool/provider endpoint | untrusted response; outbound capability로만 접근 |
| `Z7_DURABLE_DATA` | authoritative state/events/evidence 및 별도 sanitized Replay projection | least-privilege read/write; public projection은 admission 후에만 노출 |

## 4. trust crossing contract

각 crossing은 allowlist와 current policy version이 exact match할 때만 허용된다.

| crossing | allowed information/action | denied information/action | enforcing owner | failure behavior | required provenance/evidence |
|---|---|---|---|---|---|
| `HUMAN_OWNER_OPERATOR → Z2_CONTROL_PLANE` | authenticated Task/profile authorization와 designated Human input | unversioned broad waiver, public invariant 우회, raw secret 전달 | AISCC System | `DENY`; no side effect | actor, policy/task version, scope, decision, timestamp |
| `Z0_PUBLIC_UNTRUSTED → Z1_PUBLIC_READ_ONLY` | public catalog/run ID, replay controls, bounded query | mutation, free-form prompt, hidden inference trigger | Replay serving boundary | reject request 또는 explicit Replay error; no Live fallback | route/schema decision, replay artifact/version, request correlation |
| `Z0_PUBLIC_UNTRUSTED → Z2_CONTROL_PLANE` | allowlisted scenario ID, bounded enum/range, idempotency/session data; cancel은 requester/session ref와 exact target-run control authorization ref가 함께 있을 때만 candidate | schema-valid하지만 target authorization 없는 cancel, visible/guessed run ID, 다른 session run, repository URL/upload, command, arbitrary network, credential/provider/model selection | public admission gate | target authorization/state/action guard를 fail-closed; unauthorized cancel은 no control effect | normalized request hash, scenario/profile version, requester/session/principal ref, target run ref, authorization/capability ref, observed/current target state/version, decision/reason |
| `Z2_CONTROL_PLANE → Z3_PER_RUN_ISOLATED` | admitted TaskContract, immutable profile/scenario refs, bounded capability handles | raw secret, owner path in public mode, unbounded permission | System security admission | no sandbox allocation or quarantine partial allocation | run/attempt IDs, state/version, policy/profile refs, grant set, lease |
| `Z3_PER_RUN_ISOLATED → repository` | owner mode의 pinned authorized snapshot/worktree 또는 public mode의 fixed synthetic copy | primary checkout direct write, external remote fetch, path escape, sibling repository | filesystem/repository guard | operation deny; security event; no silent fallback | canonicalized resource identity, source version, read/write decision |
| `AGENT_PROVIDER → Z2/Z3` | structured proposal, bounded output, evidence candidate | authoritative mutation, executable permission grant, raw provider error exposure | adapter + System admission | invalid output rejected/quarantined | provider/model policy ref, request/response hashes, sanitization result |
| `Z3_PER_RUN_ISOLATED → tool/process` | exact profile/scenario allowlisted action with bounded arguments/resources | arbitrary shell, dynamic executable, privilege escalation, detached/background escape | process/tool broker | deny before spawn; terminate on post-start violation | executable/tool identity, structured args hash, limits, exit/termination reason |
| `Z3_PER_RUN_ISOLATED → Z6_EXTERNAL` | mediated server-fixed provider action explicitly granted to the run | direct arbitrary outbound network, user-selected endpoint/model, provider fallback outside profile | network broker/provider adapter | deny or bounded provider failure; no alternate endpoint auto-use | destination/action/profile, call count, timeout, budget reservation/result |
| `Z2_CONTROL_PLANE → Z5_SECRET` | minimum scoped opaque capability requested by authorized adapter | raw value to Agent/public/workspace/log, public credential selection | secret capability issuer | fail-closed; revoke partial capability | secret identifier class only, purpose, grantee, expiry, use result; never value |
| `Z2/Z3 → Z7_DURABLE_DATA` | authoritative events, admitted refs, hashes, sanitized candidate metadata, resource usage | raw secret, private prompt in public projection, unsanitized residue | persistence admission boundary | write denied/quarantined; public admission stopped | data classification, sanitizer/scan result, source/run/version, writer decision |
| `Z7_DURABLE_DATA → Z1_PUBLIC_READ_ONLY` | explicitly admitted sanitized Replay projection | owner/private records, secret-bearing events, mutable control-plane view | public projection owner | artifact unavailable with truthful error; no hidden Live call | projection version, source refs, sanitization/IP/license admission |
| `run A → run B` | none by default; explicitly public immutable base image may be independently copied | mutable file, process, IPC, cache, environment, capability, log or secret sharing | isolation boundary | deny and quarantine affected runs/residue | source/destination run IDs, attempted resource, isolation verdict |

## 5. RuntimeMode permission profiles

### 5.1 common profile contract

각 run은 immutable `PermissionProfileRef`를 가진다. effective permission은 다음 교집합만 허용한다.

```text
TaskContract allowed scope
∩ RuntimeMode profile
∩ scenario policy when applicable
∩ SecurityActionClass × current WorkflowState eligibility
∩ current resource capability
∩ time / call / retry / budget limits
= effective permission
```

어느 입력이 없거나 unknown이면 `DENY`다. 상위 집합의 허용을 하위 집합이 자동 상속하지 않으며, Agent가 생성한 plan/command/tool argument가 allowlist를 확장하지 않는다.

### 5.2 profile matrix

| capability | `OWNER_SELF_DOGFOOD` | `PUBLIC_RECORDED_REPLAY` | `PUBLIC_BOUNDED_LIVE` |
|---|---|---|---|
| repository | explicit owner-authorized pinned repository snapshot/worktree | none; sanitized stored projection only | server-fixed synthetic repository/version only |
| filesystem read | exact authorized run workspace/resource roots | application-level read of sanitized Replay projection only | per-run synthetic workspace and scenario assets only |
| filesystem write | per-run mutable workspace only; canonical primary checkout direct write denied | forbidden | per-run ephemeral synthetic workspace only |
| process/shell | explicit task/profile allowlist, structured bounded invocation | forbidden | public user shell forbidden; only server-defined scenario action via broker |
| tool | explicit task/profile/schema allowlist | forbidden | exact scenario tool/action/schema allowlist only |
| outbound network | default deny; exact destination/action allowlist when owner-authorized | forbidden | sandbox direct network forbidden; mediated server-fixed provider capability only when scenario permits |
| provider inference | explicit owner-authorized server profile with finite limits | forbidden; page/replay inference `0` | server-fixed provider/model, finite calls/retries/time/budget |
| credentials | opaque least-privilege capability only when Task/profile authorizes | forbidden | public cannot submit/select/read; server adapter may use one scoped provider capability |
| owner/private data | explicit Task-authorized minimum only | forbidden | forbidden |
| external repository/upload | only explicit owner Task may authorize through a separate profile; never implicit | forbidden | forbidden |
| authoritative store mutation | System services only; Agent/run output remains candidate | forbidden | System services only; public/Agent cannot mutate authority directly |
| public artifact admission | separate sanitization/evidence/judgment path | read-only already-admitted artifact | Live output remains non-public candidate until separate admission |

### 5.3 owner profile constraints

`OWNER_SELF_DOGFOOD` is broader but not unrestricted.

- explicit owner authorization identifies repository, action classes, resource bounds, tool/network destinations and secret purposes;
- runtime writes an isolated worktree/snapshot, not the canonical primary checkout;
- candidate diff/result does not authorize Git add/commit/push or authoritative workflow mutation;
- private data and secret access are purpose-bound and omitted from public provenance;
- owner permission cannot be copied, inherited or downgraded into a public profile.

### 5.4 Recorded Replay hard boundary

```text
PUBLIC_PAGE_VIEW_OR_REPLAY
→ NO_LLM_INFERENCE
→ NO_SOURCE_MUTATION
→ NO_SHELL_OR_PROCESS
→ NO_OUTBOUND_NETWORK_OR_TOOL_EXECUTION
```

Replay rendering reads only an admitted sanitized projection. Missing/corrupt Replay data yields a truthful Replay error and never triggers Live inference.

### 5.5 Public Bounded Live hard boundary

```text
fixed synthetic repository only
allowlisted scenario only
server-fixed provider/model
bounded calls/retries/time/budget
no free-form task
no external repository/upload
no arbitrary shell/network
no owner/private workspace access
```

Public parameters are server-defined enum/range values. They cannot carry instructions, paths, commands, URLs, credentials or provider configuration. A scenario is disabled unless every required bound and capability is present and versioned.

## 6. deny-by-default와 allowlist semantics

### 6.1 exact permission evaluation

`PermissionRequest`는 최소 다음을 가진다.

- principal, `RuntimeMode`, run/attempt ID;
- TaskContract, policy, profile와 scenario version;
- exact `SecurityActionClass`, action kind와 canonical resource identity;
- structured arguments and requested limits;
- authoritative observed `WorkflowState/state_version`;
- requester/session/principal, target-run authorization, idempotency/budget/capability refs when applicable.

System은 evaluation 시작과 side effect/control admission 직전에 current state/version freshness와 action/state eligibility를 각각 재검증한다. freshness가 맞아도 action class가 current `WorkflowState`에서 admissible하지 않으면 `DENY`다. stale request/capability는 `DENY`이며 새 request가 필요하다.

### 6.2 exact security action classes

`SecurityActionClass`의 exact set은 아래 11개다. 목록 밖 action과 한 class로 결정할 수 없는 복합 action은 `UNKNOWN_ACTION_CLASS`로 deny한다. 복합 operation은 각 side effect를 개별 class/guard로 평가한다.

```text
START_EXECUTION_CONTROL
RUN_EXECUTION_SIDE_EFFECT
RUN_REVIEW_READ_ONLY
PUBLIC_CANCEL_CONTROL
ADMINISTRATIVE_TERMINATE_CONTROL
REWORK_START_CONTROL
BLOCKER_RECOVERY_CHECK
SAFETY_CLEANUP_REVOKE_QUARANTINE
RECOVERY_RECONCILIATION
SYSTEM_DURABLE_PROVENANCE
REPLAY_READ_ONLY
```

| action class | requester/principal | may create side effects | admissible `WorkflowState` | class-specific guards | freshness | failure result | minimum provenance |
|---|---|---|---|---|---|---|---|
| `START_EXECUTION_CONTROL` | AISCC System; authorized owner/operator or Agent may request | inert sandbox reservation/start authorization only; no Agent/tool/provider execution or mutable run work | `READY` only | Task/profile/runtime context, start authorization, limits, no unresolved gate | current state/version at evaluation and admission | `ACTION_STATE_NOT_ADMISSIBLE` or failed guard; remain unchanged | requester, READY/version, profile, reservation/start decision |
| `RUN_EXECUTION_SIDE_EFFECT` | AISCC System-brokered Agent/tool/provider | yes: scoped filesystem/process/tool/provider work | `RUNNING` only | Task/profile/scenario/resource capability, limits, budget/idempotency where applicable | current state/version before every new side effect | deny/terminate bounded operation; security event only | action/resource/capability, RUNNING/version, limits, outcome |
| `RUN_REVIEW_READ_ONLY` | AISCC System, authorized reviewer/Human; scoped Agent only when profile permits | no external/process/provider or filesystem mutation | all nine states | read scope, data classification, profile and resource authorization | current state/version for mutable run view | read denied; no mutation | requester, target run, state/version, resource/view decision |
| `PUBLIC_CANCEL_CONTROL` | admitted public requester/session with exact run-control grant | control effect: closes new work and initiates bounded termination/cleanup; no normal execution | `RUNNING` only for a new cancel intent | exact requester/session/principal→target-run binding, cancel capability, idempotency, profile | current target RUNNING/version at new-intent admission | `CANCEL_TARGET_NOT_AUTHORIZED`, stale or action-state deny; no control effect | requester/session/principal, target run, control grant, observed/current state/version, intent/decision |
| `ADMINISTRATIVE_TERMINATE_CONTROL` | AISCC System or Human owner/operator through separate versioned administrative authorization | same bounded stop/cleanup control; no normal execution | `RUNNING` only for a new terminate intent | administrative policy/scope/grant, target run, reason, idempotency | current target RUNNING/version | deny; no public grant reuse and no state mutation | admin actor/path/version, target, state/version, reason, decision |
| `REWORK_START_CONTROL` | AISCC System; authorized owner/operator may request | creates bounded revision/attempt preparation only; no normal execution side effect | `REWORK_REQUIRED` only | admitted rework spec/lineage, Task/profile, no pending gate | current state/version | deny; no attempt execution | requester, rework lineage, state/version, control decision |
| `BLOCKER_RECOVERY_CHECK` | AISCC System or exact blocker owner through authorized path | read/check by default; mediated bounded verification only if separately allowlisted | `BLOCKED` only | blocker/resolution refs, owner, exact verification capability | current state/version | check denied/failed; no implicit resume | blocker/owner, check/capability, BLOCKED/version, result |
| `SAFETY_CLEANUP_REVOKE_QUARANTINE` | AISCC System safety owner only | yes, but only terminate/revoke/delete/quarantine already run-bound resources | all nine states | exact run/resource inventory, cleanup policy, no creation of normal work | current state/version at each cleanup step | quarantine and durable failure; never continue normal work | resource inventory, state/version, cleanup/revoke/quarantine result |
| `RECOVERY_RECONCILIATION` | AISCC System recovery owner only | reconciliation/read; any destructive settling uses cleanup class | all nine states | durable lease/event/resource ownership and recovery policy | current state/version; causal old version recorded separately | fail-closed/quarantine; no automatic execution resume | recovery owner, causal/current versions, inventory, reconciliation result |
| `SYSTEM_DURABLE_PROVENANCE` | AISCC System persistence owner only | append-only durable store write; no external execution or state mutation | all nine states | writer authority, event schema/classification and store scope | current state/version at append; causal prior version may also be recorded | append failure surfaced; no silent success | event/decision IDs, causal/current state/version, writer/result |
| `REPLAY_READ_ONLY` | public or authorized viewer through Replay serving path | none; stored sanitized projection read only | all nine recorded source-state values | admitted public projection, read policy, projection/catalog version | immutable projection version freshness; no mutable target-run control authority | truthful read error; no hidden Live | viewer/session class, projection/version, recorded state metadata, read decision |

`START_EXECUTION_CONTROL`이 `READY`에서 허용된다는 것은 P1-1 `READY → RUNNING`을 위한 bounded start authorization만 뜻한다. mutable filesystem/process/tool/provider work는 authoritative state가 `RUNNING`이 된 뒤 새 capability로 `RUN_EXECUTION_SIDE_EFFECT`를 재평가해야 한다.

`RUN_REVIEW_READ_ONLY`와 `REPLAY_READ_ONLY`는 read permission만 제공한다. 어느 것도 cancel, terminate, workflow mutation 또는 provider execution authority를 만들지 않는다.

### 6.3 exact action × WorkflowState eligibility

아래 표의 class만 해당 current state에서 eligible하다. 표에 없는 action/state 조합은 freshness와 다른 guard가 모두 PASS여도 `DENY(ACTION_STATE_NOT_ADMISSIBLE)`다.

| current `WorkflowState` | exact eligible action classes | normal execution rule |
|---|---|---|
| `READY` | `START_EXECUTION_CONTROL`, `RUN_REVIEW_READ_ONLY`, `SAFETY_CLEANUP_REVOKE_QUARANTINE`, `RECOVERY_RECONCILIATION`, `SYSTEM_DURABLE_PROVENANCE`, `REPLAY_READ_ONLY` | start authorization only; normal side effects denied until `RUNNING` is authoritative |
| `RUNNING` | `RUN_EXECUTION_SIDE_EFFECT`, `RUN_REVIEW_READ_ONLY`, `PUBLIC_CANCEL_CONTROL`, `ADMINISTRATIVE_TERMINATE_CONTROL`, `SAFETY_CLEANUP_REVOKE_QUARANTINE`, `RECOVERY_RECONCILIATION`, `SYSTEM_DURABLE_PROVENANCE`, `REPLAY_READ_ONLY` | exact state in which normal Agent/tool/process/provider execution may advance the attempt |
| `ADMISSION_PENDING` | `RUN_REVIEW_READ_ONLY`, `SAFETY_CLEANUP_REVOKE_QUARANTINE`, `RECOVERY_RECONCILIATION`, `SYSTEM_DURABLE_PROVENANCE`, `REPLAY_READ_ONLY` | submission/evidence review only; prior execution capability unusable |
| `HUMAN_REQUIRED` | `RUN_REVIEW_READ_ONLY`, `SAFETY_CLEANUP_REVOKE_QUARANTINE`, `RECOVERY_RECONCILIATION`, `SYSTEM_DURABLE_PROVENANCE`, `REPLAY_READ_ONLY` | Human/Judgment wait; prior execution capability unusable |
| `BLOCKED` | `RUN_REVIEW_READ_ONLY`, `BLOCKER_RECOVERY_CHECK`, `SAFETY_CLEANUP_REVOKE_QUARANTINE`, `RECOVERY_RECONCILIATION`, `SYSTEM_DURABLE_PROVENANCE`, `REPLAY_READ_ONLY` | normal execution denied; exact blocker check and safety settling only |
| `REWORK_REQUIRED` | `RUN_REVIEW_READ_ONLY`, `REWORK_START_CONTROL`, `SAFETY_CLEANUP_REVOKE_QUARANTINE`, `RECOVERY_RECONCILIATION`, `SYSTEM_DURABLE_PROVENANCE`, `REPLAY_READ_ONLY` | rework preparation/control only; new execution requires later `READY → RUNNING` admission |
| `ACCEPTED` | `RUN_REVIEW_READ_ONLY`, `SAFETY_CLEANUP_REVOKE_QUARANTINE`, `RECOVERY_RECONCILIATION`, `SYSTEM_DURABLE_PROVENANCE`, `REPLAY_READ_ONLY` | terminal; new normal execution/provider/tool side effect denied |
| `REJECTED` | `RUN_REVIEW_READ_ONLY`, `SAFETY_CLEANUP_REVOKE_QUARANTINE`, `RECOVERY_RECONCILIATION`, `SYSTEM_DURABLE_PROVENANCE`, `REPLAY_READ_ONLY` | terminal; new normal execution/provider/tool side effect denied |
| `FAILED` | `RUN_REVIEW_READ_ONLY`, `SAFETY_CLEANUP_REVOKE_QUARANTINE`, `RECOVERY_RECONCILIATION`, `SYSTEM_DURABLE_PROVENANCE`, `REPLAY_READ_ONLY` | terminal; new normal execution/provider/tool side effect denied |

Safety classes are allowed in terminal states only to settle resources that already belong to the run. They cannot create a new execution attempt, provider call, mutable candidate or retry. A retry requires accepted P1-1 new-run/rework lineage and fresh state admission.

### 6.4 independent admission guards and capability lifetime

Exact allow predicate:

```text
SecurityAdmissionDecision = ALLOW
IFF
SG_FRESH_STATE_VERSION
AND SG_ACTION_STATE_ELIGIBLE
AND SG_REQUESTER_AUTHORIZED
AND SG_TASK_PROFILE_SCOPE
AND SG_SCENARIO_RESOURCE_CAPABILITY
AND SG_LIMIT_BUDGET_IDEMPOTENCY
AND SG_TARGET_CONTROL_AUTHORIZATION_WHEN_MUTABLE_CONTROL
```

`SG_FRESH_STATE_VERSION`과 `SG_ACTION_STATE_ELIGIBLE`는 별도 guard다.

```text
fresh state_version
!= action admissible in that WorkflowState
```

- any guard가 missing, unknown, stale 또는 false이면 `DENY`다;
- result는 side-effect permission일 뿐 P1-1 TransitionDecision이나 WorkflowState mutation이 아니다;
- mutable run을 target하지 않는 `REPLAY_READ_ONLY`는 admitted immutable projection/catalog version을 freshness owner로 사용하며 live run control authority를 얻지 않는다.

Capability는 최소 run/attempt, action class, principal, resource, policy/profile/scenario version, evaluated `WorkflowState/state_version`, limits, expiry와 use count에 binding된다.

```text
STATE OR STATE_VERSION CHANGE
→ PREVIOUSLY EVALUATED PERMISSION IS STALE
→ NO REUSE WITHOUT REVALIDATION
```

- `RUN_EXECUTION_SIDE_EFFECT`, `PUBLIC_CANCEL_CONTROL`, `ADMINISTRATIVE_TERMINATE_CONTROL`, `START_EXECUTION_CONTROL`, `REWORK_START_CONTROL`, `BLOCKER_RECOVERY_CHECK` capability는 binding state/version을 떠나는 즉시 새 use가 deny되고 revoke/expire된다.
- `RUNNING`을 떠나는 transition admission은 normal process/tool/provider/network/secret capability의 new-use admission을 닫고 revoke signal을 발행해야 한다. lease 시간이 남아 있어도 사용할 수 없다.
- already in-flight action은 bounded termination/reconciliation 대상이며 old version에 binding된 partial result만 candidate로 남긴다. current version evidence나 success로 자동 재bind하지 않는다.
- terminal state 진입은 normal execution/provider capability를 즉시 unusable로 만들며, cleanup/recovery/provenance는 current terminal state/version에 대해 System이 새 safety capability를 평가·발행한다.
- read/recovery/safety capability도 transition을 가로질러 재사용하지 않는다. 필요하면 current state/version에서 새로 평가한다.
- capability revocation/expiry 실패는 cleanup failure로 기록하고 affected resource를 quarantine한다.

### 6.5 resource-domain rules

| domain | allow condition | fail-closed condition |
|---|---|---|
| filesystem | canonicalized path가 exact allowed root/action에 있고 symlink/junction resolution 후에도 내부 | unknown path, traversal, link escape, alternate stream, host/sibling/private path |
| process/command | broker가 exact executable/action과 structured argument schema, cwd, environment, time/resource limit을 승인 | arbitrary command string, shell expansion, dynamic executable, missing limit, detached child |
| tool | tool/action/version/schema와 resource scope가 exact match | unknown tool/action/field, Agent-generated permission, schema ambiguity |
| network | mediated capability의 exact protocol/destination/port/action과 finite call/time limits가 match | direct socket, wildcard destination, redirect/DNS resolution이 allow scope를 벗어남, unknown endpoint |
| credential/secret | authorized adapter의 purpose-bound opaque handle, expiry와 use count valid | raw secret request, public selection, log/workspace/prompt injection, unknown purpose |
| repository/worktree | pinned repository identity/version과 per-run isolated copy가 profile에 match | primary checkout write, public external repo, remote mutation/fetch not explicitly authorized |
| provider call | provider/model/action이 server profile과 scenario에 고정되고 budget reservation이 valid | user/Agent-selected provider/model, missing cap, budget unknown/exhausted, auto-fallback outside profile |
| scenario/action | exact enabled scenario/version과 bounded parameters | unknown/disabled scenario, free-form field, version mismatch |

Allowlist entry는 principal/mode/action/resource/constraints/version을 함께 지정한다. broad wildcard, display name, Agent prose 또는 string prefix만으로 match하지 않는다. policy exception은 새 versioned policy와 필요한 Human acceptance로만 가능하며 current public run을 소급 확장하지 않는다.

## 7. repository와 mutable run isolation

### 7.1 repository boundary

- repository identity는 canonical root label, resolved root, source commit/snapshot과 policy ref로 고정한다.
- owner run은 exact authorized source에서 per-run isolated worktree/snapshot을 만든다. canonical primary checkout과 `.git` credential/remotes를 runtime write target으로 제공하지 않는다.
- public Live는 version-pinned fixed synthetic repository를 매 run 독립 복사한다. source provenance와 license/IP admission이 없는 snapshot은 public enable 대상이 아니다.
- public run은 external repository URL, upload, remote, owner workspace, IDE metadata, host home 또는 sibling project를 볼 수 없다.
- runtime result는 candidate diff/artifact다. Git mutation 또는 canonical admission은 별도 future Task/authority가 소유한다.

### 7.2 per-run isolation

각 mutable run은 다음을 독립적으로 가진다.

- unique run/attempt identity and lease;
- filesystem namespace/workspace;
- process tree and IPC scope;
- environment and temporary storage;
- tool/network/secret capability set;
- resource/time/call/retry/budget counters;
- stdout/stderr/tool/provider capture with redaction boundary.

run 간 mutable directory, process, IPC endpoint, environment, cache, credential handle 또는 output file 재사용은 금지한다. immutable base artifact는 integrity-verified copy-on-write 또는 독립 복사 의미로만 공유할 수 있다. owner/private와 public workloads는 workspace root, capability issuer, queue/pool과 public projection 경계를 논리적으로 분리해야 한다.

## 8. credential와 secret boundary

- secret material은 public Task, Cycle, Replay, evidence, report, URL, browser state, prompt, command argument, environment dump 또는 log에 들어가지 않는다.
- Agent/run에는 raw secret 대신 explicit policy가 허용한 최소 purpose-bound opaque capability/handle만 제공한다.
- public requester는 credential을 입력·선택·업로드·조회할 수 없다.
- public sandbox는 secret store에 직접 접근하지 않는다. server-side mediated adapter만 scoped capability를 사용할 수 있다.
- secret value는 workspace file, process listing, trace, provider response copy, error message 또는 Replay에 저장하지 않는다.
- log/redaction은 defense-in-depth이며 raw secret 전달 자체를 정당화하지 않는다.
- secret-like material이 public provenance candidate에서 탐지되면 값은 출력하지 않고 artifact admission을 중단·격리한다. path/artifact ID, detector class, decision만 기록한다.
- detection 결과는 `EvidenceCandidate` 또는 security event이며 Task acceptance나 workflow mutation을 직접 결정하지 않는다.
- capability는 run/purpose/destination/use-count/expiry에 binding되고 cancel/timeout/failure/cleanup 시 revoke된다.
- concrete secret manager, credential type와 rotation implementation은 P1-3 이후 implementation/release owner가 선택한다.

## 9. timeout, retry, cancel과 partial failure

각 executable profile/scenario는 enable 전에 positive finite `wall_clock_limit`, `attempt_limit`, provider/tool `call_limit`, output/resource limits를 가져야 한다. missing, zero 의미가 ambiguous하거나 unbounded인 limit은 `DENY`다. exact release 숫자는 P3-3이 current provider/config evidence와 함께 고정한다.

| event | required semantic behavior | prohibited behavior |
|---|---|---|
| timeout | 새 side effect 차단, process tree 종료, capability/lease revoke, partial output를 candidate로 표시, cleanup 시작 | success 처리, child process 방치, silent retry |
| explicit cancel | action/state와 exact requester→target-run authorization을 통과한 idempotent cancel intent 기록; admission 후 새 work 중단, in-flight 작업 bounded termination, cleanup | run ID/visibility만으로 cancel, 다른 session run cancel, 이미 발생한 provider spend/state event 삭제, accepted result로 표시 |
| provider/tool transient failure | policy가 허용한 finite retry만 새 attempt ID와 budget accounting 아래 실행 | unbounded loop, profile 밖 provider/tool fallback |
| provider/tool partial success | committed side effect와 uncertainty 기록, 재시도 전에 idempotency/compensation safety 확인 | blind duplicate side effect, partial artifact를 complete evidence로 승격 |
| retry exhaustion | execution/security event와 exact reason 생성; System이 P1-1 existing transition을 별도 평가 | Agent가 `FAILED`/`REWORK_REQUIRED`를 직접 확정 |
| orchestrator/process crash | lease expiry 후 orphan detection, side effect reconciliation, cleanup/recovery; durable truth에서 재개 | memory-only success 복원, same request 자동 재실행 |

Cancellation 자체는 새 `WorkflowState`가 아니다. timeout/cancel/failure event는 P1-1 `ExecutionStatus`, blocker/failure/rework semantics의 input일 뿐이며 authoritative state mutation에는 current `state_version`을 사용한 별도 TransitionRequest/Evaluation/Decision이 필요하다.

### 9.1 public cancel target authorization

Public cancel의 conceptual authorization record는 `PublicRunControlGrant`다. 구현 token/HTTP/session 기술이 아니라 다음 exact semantic binding을 뜻한다.

- immutable grant ID and version;
- admitted requester principal/session ref;
- exact target `work_run_id` and originating public Live request/idempotency ref;
- allowed action class=`PUBLIC_CANCEL_CONTROL` only;
- `RuntimeMode=PUBLIC_BOUNDED_LIVE`, profile/scenario version;
- issuance state/version, expiry, revocation and optional explicit delegate principal/session ref.

Grant는 isolated public run admission 뒤 AISCC System만 발행한다. run ID, public URL, catalog/Replay entry, read permission, scenario membership 또는 same IP/client hint는 grant가 아니다.

```text
PUBLIC_CANCEL_REQUEST
→ REQUESTER PRINCIPAL/SESSION ADMITTED
→ EXACT TARGET RUN CONTROL BINDING
→ CANCEL GRANT VALID AND NOT REVOKED
→ CURRENT TARGET RUN/STATE/VERSION REVALIDATED
→ ACTION CLASS ELIGIBLE IN CURRENT STATE
→ CANCEL INTENT ADMITTED OR DENIED
```

새 cancel intent의 exact checks:

1. requester principal/session ref가 current request admission과 일치한다.
2. grant의 grantee 또는 exact explicit delegate가 requester와 일치한다.
3. grant target `work_run_id`가 request target과 exact match한다.
4. grant action/profile/scenario/policy/expiry/revocation이 current context에 valid하다.
5. authoritative target state/version이 request observation과 match하고 `PUBLIC_CANCEL_CONTROL`이 current state `RUNNING`에서 eligible하다.
6. cancel idempotency identity가 requester/grant/target run에 binding된다.

어느 하나라도 unknown, expired, revoked, stale 또는 mismatched이면 fail-closed한다. 다른 public principal/session은 explicit delegated control grant 없이는 target run을 cancel할 수 없다.

```text
PUBLIC_RUN_OR_REPLAY_VISIBILITY
!= PUBLIC_CANCEL_AUTHORITY

RUN_ID_KNOWLEDGE
!= TARGET_RUN_CONTROL_AUTHORIZATION
```

첫 valid cancel은 immutable `cancel_intent_id`와 decision을 기록하고 new work admission을 닫으며 bounded revoke/termination/cleanup을 시작한다. cancel intent 자체는 `WorkflowState`를 mutate하지 않는다.

동일 requester/grant/target/idempotency identity의 반복 요청은 기존 cancel decision/intent를 반환하고 새 intent, 새 provider call 또는 추가 workflow mutation을 만들지 않는다. 첫 intent 뒤 state가 바뀌었어도 이는 기존 decision lookup이며 새 cancel admission이 아니다. expired/revoked grant는 새 intent를 deny한다. 기존 intent lookup도 current requester/session read authorization이 없으면 detail을 반환하지 않는다.

Human/System/owner administrative terminate가 허용되면 `ADMINISTRATIVE_TERMINATE_CONTROL`과 별도 versioned administrative grant/policy를 사용한다. public grant를 재사용하거나 public visibility에서 추론하지 않는다. authentication/session/token/API 구현 기술은 P1-3 이후 owner에게 deferred한다.

## 10. idempotency, abuse와 budget admission

### 10.1 public Live admission order

```text
PUBLIC LIVE REQUEST
→ scenario allowlist
→ identity/session/abuse gate
→ idempotency
→ application budget admission
→ provider availability/capability gate
→ isolated run admission
```

모든 gate가 `ALLOW`일 때만 isolated run과 paid capability를 발행한다. 순서를 통과하지 못한 request는 provider call을 만들지 않는다.

### 10.2 idempotency

- idempotency identity는 public session/principal, scenario/version, normalized bounded parameters와 client/server request key에 binding된다.
- same key + same normalized request는 기존 admission/denial/run reference를 반환하며 새 paid run을 만들지 않는다.
- same key + different payload는 conflict로 deny한다.
- browser refresh, double click, transport retry와 timeout ambiguity는 자동 새 run 사유가 아니다.
- retry attempt는 parent run/request와 연결된 distinct attempt ID를 가지며 동일 per-run/global limits 안에서 accounting된다.
- uncertain provider/tool completion은 reconciliation 전 재호출하지 않는다.
- idempotency retention은 가능한 provider retry/late response window보다 짧아서는 안 되며 exact duration은 implementation/release policy가 정한다.

### 10.3 abuse/throttling

Public admission은 최소 session/principal별 request rate, concurrent runs, queued requests, invalid request rate, payload size와 cooldown의 finite policy를 가진다. identity가 anonymous여도 server-issued bounded session identity가 필요하다. missing/unknown abuse policy, exhausted quota, disabled scenario 또는 suspicious repeated conflict는 fail-closed한다.

Abuse result는 access/admission decision이지 Human judgment나 workflow acceptance가 아니다. public error는 internal policy detail, host path, secret 또는 stack trace를 노출하지 않는다.

### 10.4 application budget

- finite per-run, per-session/principal, application-period와 global emergency budget을 둔다.
- application budget ledger/admission이 provider call 전에 authoritative하다.
- budget reservation과 run/call admission은 duplicate paid execution을 막도록 atomic semantic boundary를 가진다.
- successful/known provider use는 reservation에 charge한다. failure 전 no-call이 입증될 때만 release할 수 있다.
- crash/unknown completion은 reconciliation 전 보수적으로 reserved/charged 상태를 유지한다.
- missing meter, stale ledger, concurrency conflict, exhausted/unknown budget은 `DENY`다.
- Agent/Human prose나 provider의 예상 비용 응답은 application ledger를 대체하지 않는다.

Provider spend/hard limit은 지원될 때 defense-in-depth로 사용한다. application guard를 대체하지 않으며 provider capability/configuration이 검증되지 않으면 public Live는 Replay-only로 유지한다. current provider feature, pricing, region, currency와 exact caps는 P3-3 소유다.

## 11. failure-domain separation과 Replay fallback

필수 invariant:

```text
LIVE_UNAVAILABLE_OR_BUDGET_EXHAUSTED
→ RECORDED_REPLAY_REMAINS_AVAILABLE
```

| failure domain | may depend on | must not depend on | degradation behavior |
|---|---|---|---|
| static public page | static assets/public configuration | provider inference, live queue, owner workspace | project explanation과 Replay entry 유지 |
| Recorded Replay path | admitted sanitized Replay projection and read-only serving | live orchestrator, provider, application Live budget, secret store | missing/corrupt artifact를 truthful error로 표시; hidden Live 금지 |
| Live orchestration path | security/admission, isolated runtime, budget ledger, provider capability | Replay success label or owner workspace | Live disable/failure를 명시하고 Replay CTA 유지 |
| external provider path | mediated adapter, scoped credential, current availability | static/replay rendering | bounded retry 후 Live failure; Replay에는 영향 없음 |

- Live component outage, rate limit, provider outage, missing provider guard 또는 budget exhaustion은 static/Replay read path를 차단하지 않는다.
- Replay serving data와 live mutable state는 logical permission/storage path를 분리한다.
- Replay path 자체의 incident는 별도 incident다. 이를 Live로 자동 대체하거나 Replay 성공으로 숨기지 않는다.
- provider/model 자동 fallback은 profile, budget, destination과 truthful labeling을 우회할 수 없다.
- 이 설계는 deployment availability가 구현되었거나 검증되었다는 주장이 아니다.

## 12. cleanup, residue와 recovery

### 12.1 lifecycle cleanup

success, failure, cancel, timeout과 crash recovery 모두 다음 cleanup contract를 적용한다.

1. 새 side effect admission을 닫는다.
2. child process/IPC와 in-flight tool/provider capability를 bounded termination/revoke한다.
3. secret handles, network grants, filesystem leases와 budget reservations를 revoke/reconcile한다.
4. 보존 대상 artifact를 분류·sanitize·hash하고 candidate로만 제출한다.
5. mutable workspace, temp file, socket, cache, environment와 unadmitted output을 파기한다.
6. residue scan이 workspace/process/IPC/capability/secret marker를 검사한다.
7. cleanup/residue result를 durable event로 기록한다.

Cleanup failure는 run success를 취소해 과거를 rewrite하지 않지만, security evidence를 PASS로 만들지 않는다. affected workspace/resource는 quarantine하고 같은 resource의 재할당을 deny한다. System은 exact failure event와 current P1-1 state/version에 따라 별도 transition을 평가한다.

### 12.2 persistence versus destruction

May persist:

- Task/profile/scenario/policy versions and hashes;
- request/admission/denial/idempotency/budget provenance;
- P1-1 state/transition events and admitted evidence refs;
- sanitized candidate output, resource accounting, cleanup/residue verdict;
- separately admitted public Replay projection.

Must destroy or quarantine until destruction:

- mutable run workspace and temporary files;
- process/IPC/network namespace residue;
- raw secret, capability material and credential-bearing environment;
- unsanitized stdout/stderr/provider/tool payload;
- private/owner data not explicitly admitted for durable private storage.

### 12.3 recovery

- durable run/attempt lease와 cleanup phase로 orphan을 식별한다.
- recovery worker는 `run_id`에 binding된 resource inventory만 다루며 broad host cleanup을 하지 않는다.
- restart 후 authoritative P1-1 state/version과 security events를 읽고 projection을 검증한다.
- unknown process/resource ownership, missing cleanup event 또는 event/projection mismatch는 fail-closed/quarantine한다.
- previous Agent message, process exit `0` 또는 missing heartbeat만으로 success를 복원하지 않는다.

## 13. provenance와 관측 요구

Security evaluation/admission/denial은 secret value 없이 최소 다음을 기록한다.

- run/attempt/request/idempotency identities;
- requester/session/principal ref와 target run ref;
- mutable control이면 authorization/capability grant ref, observed/current target state/version과 decision/reason;
- TaskContract, RuntimeMode, policy/profile/scenario versions;
- observed and authoritative WorkflowState/state_version;
- principal, exact `SecurityActionClass`, action kind, canonical resource class/identity;
- freshness guard와 action/state eligibility guard의 separate result;
- allowlist entry/capability reference와 evaluated finite limits;
- budget reservation/charge/release reference and result;
- decision, stable reason code, enforcing owner and timestamp;
- process/tool/provider start/end/timeout/cancel/exit classification;
- cleanup/residue/quarantine result;
- public sanitization/secret-detection admission result without matched value.

Public error와 Replay는 internal path, raw prompt, stack trace, secret identifier detail 또는 private policy content를 노출하지 않는다. Security log 자체도 least-privilege와 retention policy 대상이다.

## 14. P1-1 conformance contract

| accepted P1-1 owner | P1-2 treatment |
|---|---|
| exact nine `WorkflowState` values | unchanged; security status/state를 추가하지 않음 |
| Agent output versus System state | security/tool/provider output은 candidate/event only |
| Judgment before outcome TransitionRequest | unchanged; security result가 Judgment를 생성하거나 대체하지 않음 |
| `Judgment != TransitionDecision` | unchanged; `SecurityAdmissionDecision`도 둘과 별도 |
| Human gate/result lifecycle | unchanged; Human generic approval이 permission grant 또는 secret access가 아님 |
| `state_version` concurrency | permission과 side effect 직전에 current version을 재검증; stale deny |
| action/state semantics | exact action class eligibility를 별도 security guard로 평가; P1-1 state 의미나 transition matrix는 변경하지 않음 |
| durable restart/recovery | security provenance는 accepted state reconstruction을 보조하되 state truth를 대체하지 않음 |
| `RuntimeMode != WorkflowState` | mode는 immutable permission profile selector이며 workflow state가 아님 |

Security deny/failure의 workflow interaction은 P1-1 existing semantics만 사용한다. 예를 들어 unresolved external/security prerequisite는 `BLOCKED` request candidate, correctable policy/evidence gap은 authoritative `HOLD_REWORK_REQUIRED` Judgment 뒤 `REWORK_REQUIRED` request candidate, irrecoverable/retry-exhausted attempt는 `FAILED` request candidate가 될 수 있다. 어느 경우도 security component나 Agent가 target state를 직접 확정하지 않는다.

## 15. P1-3 implementation and evidence handoff

P1-3은 이 문서의 first safeguard implementation owner다. 최소 구현 대상은 다음이다.

- versioned permission profile/evaluator와 deny-by-default resource matching;
- exact action-class/current-WorkflowState evaluator와 state/version-bound capability revocation;
- per-run workspace/process/tool/network capability isolation;
- owner/public/replay profile separation;
- fixed synthetic repository enforcement;
- mediated provider and scoped secret capability boundary;
- timeout/retry/cancel/process-tree termination;
- public requester/session→target-run cancel authorization and separate administrative terminate path;
- idempotency, abuse/throttling and application budget admission;
- cleanup/residue/quarantine/recovery;
- security decision/provenance and redaction/sanitization boundary;
- Replay path와 Live/provider failure-domain separation.

### 15.1 required proof classes

| proof class | minimum question | cannot substitute for |
|---|---|---|
| `STATIC_SOURCE` | policy/profile/deny rules와 forbidden route가 source에 존재하는가 | runtime isolation/network/cleanup proof |
| `UNIT_TEST` | exact allow/deny, stale, limit, idempotency/budget rules가 deterministic한가 | process/filesystem/network runtime proof |
| `INTEGRATION_TEST` | control plane, broker, store, budget와 provider adapter가 함께 fail-closed하는가 | hostile/actual sandbox boundary proof 전체 |
| `SECURITY_SANDBOX_RUNTIME` | run이 host/owner/sibling filesystem/process/IPC로 escape하지 못하고 scoped action만 수행하는가 | source/unit claim |
| `NETWORK_RUNTIME` | direct outbound가 차단되고 exact mediated allow만 가능하며 redirect/resolution escape가 차단되는가 | mock deny/unit test |
| `SECRET_NON_EXPOSURE` | synthetic canary secret가 prompt/workspace/argv/env/log/error/Replay/public artifact에 나타나지 않고 handle이 revoke되는가 | secret scan 하나 또는 redaction unit test |
| `TIMEOUT_RETRY_CANCEL_RUNTIME` | finite timeout, child termination, bounded retry, idempotent cancel과 partial failure가 관측되는가 | policy 문서 또는 mocked clock alone |
| `IDEMPOTENCY_ABUSE_BUDGET_RUNTIME` | double click/refresh/concurrency/crash가 duplicate paid run을 만들지 않고 quota/budget이 atomic fail-closed하는가 | 단일 request unit test |
| `CLEANUP_RESIDUE_RUNTIME` | success/failure/cancel/timeout/crash 뒤 filesystem/process/IPC/capability residue가 탐지·제거/격리되는가 | cleanup function unit test |
| `FAILURE_DOMAIN_RUNTIME` | Live/provider/budget failure 중 static page/Recorded Replay가 provider call 없이 유지되는가 | architecture diagram 또는 isolated component test |
| `ACTION_STATE_CANCEL_AUTHORIZATION_RUNTIME` | wrong-state action, stale/revoked capability, terminal side effect, safety settling과 public cross-session/read-versus-cancel/idempotency boundary가 실제로 fail-closed하는가 | source matrix, authorization unit test 또는 run visibility test 하나 |

P1-3 evidence는 safe synthetic fixtures/canary를 사용하며 실제 credential 값을 출력하지 않는다. 각 proof는 implementation version/commit, OS/runtime/isolation profile, scenario, expected/actual boundary, timestamps와 artifacts에 binding돼야 한다. 실패 evidence도 보존하고 false success로 대체하지 않는다.

`ACTION_STATE_CANCEL_AUTHORIZATION_RUNTIME`은 최소 다음 seven-case matrix를 실행해야 한다.

1. profile/resource capability가 valid해도 wrong `WorkflowState`의 action이 deny된다.
2. state/version transition 전 capability의 new use가 stale/revoked로 deny된다.
3. `ACCEPTED`, `REJECTED`, `FAILED`에서 normal execution/tool/provider side effect를 issue/use할 수 없다.
4. `BLOCKED`와 terminal state에서 System safety cleanup/revoke/quarantine/reconciliation은 exact current-state capability로 기존 resource를 settle할 수 있고 normal work를 만들지 않는다.
5. public session A의 grant로 session B의 run을 cancel할 수 없다.
6. public catalog/Replay/read access와 known run ID만으로 cancel할 수 없다.
7. same authorized cancel identity의 반복 요청은 one intent/one control effect를 유지하고 기존 result를 반환한다.

```text
security unit test
!= sandbox runtime proof

mock network deny
!= actual network isolation proof

secret scan
!= complete secret isolation proof

fresh state_version
!= action admissible in that WorkflowState

run visibility
!= cancel authority
```

P1-3 Human acceptance 전에는 safeguard가 implemented/verified되었다고 주장하거나 public Bounded Live release를 허용하지 않는다.

## 16. P3-3 release reverification handoff

P3-3은 release 시점에 다음을 소유한다.

- current provider capability와 official configuration method 재검증;
- actual provider/resource configuration and evidence;
- current pricing, region, terms and availability verification;
- exact model/call/token/time/run/daily/global/currency caps;
- provider spend/hard-limit configuration evidence when supported;
- deployed URL, browser accessibility, static/Replay availability and release recovery;
- release environment에서 P1-3 safeguards의 current-version reverification;
- competition disclosure, final submission과 Human confirmation.

P3-3은 P1-2 safeguard의 first implementation stage가 아니다. P1-3의 accepted implementation/evidence가 없거나 release environment에서 stale/inapplicable이면 Public Bounded Live를 enable하지 않고 Replay-only를 유지한다.

```text
P1-2 security/runtime design
→ P1-3 safeguard implementation + verification + acceptance
→ P3-3 current-provider/release reverification
```

Application budget design은 provider spend cap configured evidence가 아니며, provider capability document는 deployed configuration evidence가 아니다.

## 17. implementation, claim과 Human boundary

- 이 문서는 sandbox/container/worktree/provider/budget safeguard를 구현하지 않았다.
- provider/resource/API key/billing/deployment 상태는 `NOT_EXECUTED`다.
- exact provider/model/pricing/region/capability/cap 값은 검증하지 않았다.
- security completeness, sandbox escape 불가능 또는 public availability를 주장하지 않는다.
- Browser Project Source를 수정하거나 sync하지 않았다.
- Human은 trust zones, profiles, action/state eligibility, public cancel target authorization, secret/isolation semantics, budget/abuse policy, P1-3 proof contract와 P3-3 handoff를 review해야 한다.

Human acceptance status:

```text
HUMAN_PROVIDED / ACCEPTED / CLOSED
```
