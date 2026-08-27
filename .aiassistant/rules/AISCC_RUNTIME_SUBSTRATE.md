# AISCC Runtime Substrate Baseline

## 1. 문서 상태

| field | value |
|---|---|
| document_id | `AISCC-P1-3-RUNTIME-SUBSTRATE-V1` |
| task_id | `20260827_1442_aiscc-p1-3-runtime-substrate-baseline-design-with-blocker-provenance-commit-1` |
| work_type | `DESIGN_DECISION` |
| result_status | `HUMAN_PROVIDED / ACCEPTED` |
| authority_status | repository canonical accepted baseline |
| design base commit | `95de4ae9d5ec36bed8636b608dc5729b47e815fe` |
| human acceptance provenance | `2026-08-27` Human Runtime Substrate final review: `ACCEPTED` |
| terminal cycle | `.aiassistant/records/aiscc/cycles/20260827_1513_aiscc-p1-3-runtime-substrate-baseline-final-acceptance-1.cycle.md` |
| application implementation | `NOT_STARTED` |
| P1-3 safeguard implementation | `NOT_STARTED` |
| P1-3 runtime proof | `NOT_EXECUTED` |
| P1-4 state-machine implementation | `NOT_STARTED` |

이 문서는 Human final review에서 `ACCEPTED`된 runtime-substrate repository canonical baseline이다. P1-3 구현이 임의의 언어, framework, build 또는 sandbox substrate를 선택하지 않도록 한다. Acceptance는 substrate decision에만 적용되며 design 문서는 buildable application이나 isolation proof가 아니다.

## 2. 상위 불변식과 범위

Accepted P1-1/P1-2 contract를 변경하지 않는다.

```text
AgentOutput != SystemState
EvidenceCandidate != AdmittedEvidence
HumanResult != Judgment
Judgment != TransitionDecision
SecurityAdmissionDecision != TransitionDecision
TransitionDecision != WorkflowState
RuntimeMode != WorkflowState
```

- P1-1의 exact 9 `WorkflowState`, authoritative ordering, `state_version`, Human gate semantics는 그대로다.
- security layer는 immutable current state/version snapshot을 입력받아 `ALLOW | DENY`만 반환한다. workflow mutation을 호출하거나 소유하지 않는다.
- runtime adapter는 admitted capability만 실행하고, 실행 결과를 event/evidence candidate로 반환한다. terminal/rework state를 결정하지 않는다.
- P1-3은 security safeguard의 first implementation stage다. P1-4 state-machine kernel과 P1-5 provider/tool adapter 구현은 별도 Task다.
- `PUBLIC_RECORDED_REPLAY`는 read-only, page/replay LLM inference `0`이다. `PUBLIC_BOUNDED_LIVE`의 free-form task, external repository/upload, arbitrary shell/network, user-selected provider/model/credential은 계속 금지한다.

## 3. repository와 local evidence inventory

### 3.1 current repository state

- tracked file은 governance/provenance 문서와 mirror utility를 중심으로 55개다.
- product runtime source root, test root, package/build manifest, lockfile, container definition은 없다.
- `scripts/generate_project_source_bundle.ps1`은 P0-5 mirror 생성 utility이며 AISCC product runtime이나 build substrate가 아니다.

### 3.2 non-mutating local probes

| probe | observation | interpretation |
|---|---|---|
| `python --version` | Windows Store alias, exit `9009`; usable Python runtime 아님 | primary candidate 설치 prerequisite 존재 |
| `py --version` | absent | 동일 |
| `uv --version` | absent | primary build tool 설치 prerequisite 존재 |
| `node --version` | IDE-bundled Node `v24.13.0` | local secondary signal only |
| `npm.cmd --version` | `11.6.2`; PowerShell shim은 execution policy로 실패 | Node fallback 선택 근거가 아님 |
| `corepack --version` | IDE-bundled `0.34.5` | local secondary signal only |
| `java` / `javac` | OpenJDK `11.0.28` | proposed JVM 21 baseline을 충족하지 않음 |
| `mvn`, `gradle`, `go`, `podman` | absent | candidate rejection의 단독 근거가 아님 |
| `docker --version` | `28.3.3` | Docker CLI available |
| `docker compose version` | `v2.39.2-desktop.1` | Compose plugin available |
| `docker info` | Linux Docker Desktop engine `28.3.3`, reachable | P1-3 local evidence prerequisite currently available |
| `git --version` | `2.51.0.windows.1` | repository tooling only |

```text
locally installed
!= selected substrate
```

Design Task에서는 Python과 `uv`를 설치하지 않았다. Human이 substrate를 수용했으며 후속 P1-3 Task가 환경 준비를 명시적으로 허용할 때만 설치할 수 있다. 그 준비가 승인된 경로로 불가능하면 `HUMAN_ENVIRONMENT_PREPARATION_REQUIRED`다.

## 4. option analysis와 결정

평가는 competition MVP의 governance/security proof에 맞춘 상대 비교다. `강`, `중`, `약`은 benchmark 수치가 아니라 이 프로젝트의 현재 요구에 대한 설계 판단이다.

| criterion | A. Python typed service | B. TypeScript/Node service | C. JVM service |
|---|---|---|---|
| candidate | CPython 3.12 + FastAPI + Pydantic v2 | Node 24 + TypeScript + Fastify | Java 21 + Spring Boot + Gradle |
| deadline 내 구현 속도 | 강 — policy model, fixture, subprocess proof를 짧게 구성 | 강 — HTTP/JSON과 async 구현이 빠름 | 중 — bootstrap과 framework ceremony가 큼 |
| explicit state-machine clarity | 강 — enum/dataclass와 framework-free core 가능 | 강 — discriminated union과 exhaustive check 가능 | 강 — sealed type/record와 compiler guard가 강함 |
| typed domain model | 중상 — strict mypy/Pydantic discipline 필요 | 강 — strict TypeScript와 schema 결합 | 강 — compile-time type와 mature modeling |
| deterministic admission policy | 강 — pure function/table test가 간결 | 강 — pure function와 schema validation이 좋음 | 강 — type/validation이 견고하나 코드량 증가 |
| subprocess/filesystem control | 강 — 표준 `subprocess`, `pathlib`, Docker CLI adapter가 직접적 | 중상 — child process API는 충분하나 cancellation/stream edge 처리가 더 복잡 | 중상 — ProcessHandle/NIO는 강하지만 proof harness 비용 증가 |
| async provider/API path | 강 — ASGI/async ecosystem 적합 | 강 — event-loop/HTTP ecosystem 적합 | 강 — reactive 또는 virtual-thread path 가능 |
| P1-3 proof tooling | 강 — pytest fixture/parametrize와 runtime harness가 간결 | 강 — Vitest와 integration harness가 적합 | 중상 — JUnit/Testcontainers가 강하지만 bootstrap 비용 큼 |
| PostgreSQL direction | 강 — SQLAlchemy async/asyncpg/Alembic | 강 — node-postgres/ORM/migration 선택지가 많음 | 강 — JDBC/JPA/Flyway ecosystem |
| later bounded Live HTTP | 강 — FastAPI/ASGI, typed validation | 강 — Fastify/schema-first HTTP | 강 — Spring HTTP stack |
| provenance/logging | 강 — typed event + JSON logging 구성 용이 | 강 — JSON-native | 강 — structured logging mature |
| reproducibility | 강 — `pyproject.toml` + `uv.lock` | 강 — `package.json` + `pnpm-lock.yaml` | 강 — Gradle Wrapper + dependency locking |
| container evidence | 강 — small Linux runtime image와 Docker broker harness | 강 — image/tooling 양호 | 중상 — larger runtime/image와 startup cost |
| Railway-compatible direction | 강 — stateless ASGI service와 external PostgreSQL contract | 강 — stateless Node service와 external PostgreSQL contract | 중 — 가능하나 MVP resource/startup 부담이 상대적으로 큼 |
| operational simplicity | 강 | 강 | 중 |
| post-competition maintainability | 강 — strict typing/test boundary를 지킬 때 | 강 — frontend와 language sharing 가능 | 강 — 장기 typed service에 유리 |

### 4.1 primary recommendation

`A. CPython 3.12 + FastAPI + Pydantic v2 + uv`를 primary candidate로 추천한다.

결정 이유:

1. P1-3의 load-bearing work는 UI가 아니라 deterministic policy table, bounded process/container broker, filesystem/network/cleanup harness와 proof artifact 생산이다. Python 표준 library와 pytest가 이 첫 slice를 가장 작은 bootstrap으로 연결한다.
2. FastAPI는 HTTP boundary와 request validation에만 사용하고 core security/domain policy는 framework-free module로 둔다. 따라서 framework가 P1-1 transition authority를 흡수하지 않는다.
3. Python의 동적 특성은 `mypy --strict`, immutable typed models, exhaustive enum handling, Pydantic boundary validation과 unit matrix로 제한한다.
4. Docker Linux container가 실제 isolation boundary를 소유하므로 host Python process isolation의 플랫폼 차이를 security proof로 오인하지 않는다.
5. stateless ASGI service, external PostgreSQL adapter와 environment-driven port/config contract는 Railway-compatible deployment direction을 제공한다. 실제 Railway capability와 sandbox worker 배치는 P3-3에서 재검증하며 deployment를 주장하지 않는다.

### 4.2 fallback

`B. Node 24 + TypeScript strict + Fastify + pnpm`을 유일한 fallback으로 둔다. Python/`uv` bootstrap 또는 required dependency가 authorized implementation environment에서 재현 불가능하다는 evidence가 생길 때만 별도 Human-accepted baseline update로 전환한다.

Fallback 방향:

- runtime: Node 24.x compatibility line;
- framework: Fastify, HTTP/schema boundary only;
- build/package: pnpm + `package.json` + `pnpm-lock.yaml` + TypeScript project references;
- test/type/lint: Vitest, `tsc --noEmit`, ESLint;
- sandbox: 동일 Docker Linux container/broker contract.

Fallback은 자동 전환이 아니다. local IDE-bundled Node 존재만으로 선택하지 않는다.

### 4.3 rejected reason

- JVM candidate는 type safety, concurrency와 persistence가 약해서가 아니라, 현재 deadline에서 Gradle/Spring bootstrap, image/startup, proof harness ceremony가 P1-3 첫 slice의 operational simplicity를 악화하므로 primary/fallback에서 제외한다. 장기 확장성 이점은 인정한다.
- Go는 명시적 concurrency와 small binary 장점이 있지만 required minimum three-family 비교를 넘어 새 fourth option을 채택할 만큼 현재 repository/team evidence가 없고, schema/config/validation/proof fixture를 다시 선택해야 하므로 이번 baseline에 추가하지 않는다.
- local availability는 어느 결정을 확정하지 않는다. 현재 오히려 primary Python이 없지만 project-specific fit을 우선했다.

### 4.4 uncertainties와 deferred decisions

- CPython 3.12 exact patch, dependency exact versions와 image digest는 authorized P1-3 환경 확인 후 lock한다.
- production sandbox worker placement, Railway에서의 container-runtime availability, provider/model, authentication, exact budget/cap 숫자는 이 baseline이 결정하지 않는다.
- PostgreSQL schema, transition transaction implementation과 state-machine code는 P1-4 소유다.
- public scenario corpus/synthetic repository는 P2-3, deployment/provider/release proof는 P3-3 소유다.

## 5. application runtime decision

```text
language: Python
runtime/version policy: CPython 3.12.x; requires-python >=3.12,<3.13
framework: FastAPI with Pydantic v2; Uvicorn ASGI server
framework role: HTTP/input-output adapter and dependency composition only
```

- `.python-version`은 P1-3 bootstrap 시 locally verified exact 3.12 patch를 pin한다.
- core policy, capability, budget, cancellation, provenance code는 FastAPI request object나 global application state에 의존하지 않는다.
- ASGI handler는 input을 typed command로 변환하고 application service를 호출한 뒤 result를 response로 투영한다.
- application process는 stateless HTTP/control process 방향이다. durable truth는 persistence port 뒤에 있고 in-memory globals는 authority가 아니다.
- entrypoint는 installed console script `aiscc = aiscc.__main__:main`이다. 표준 시작은 `uv run aiscc serve`; port는 validated non-secret config에서 읽는다.

## 6. package, build와 reproducibility

| decision | exact convention |
|---|---|
| package/environment manager | `uv` |
| PEP 517 build backend | Hatchling |
| manifest | repository root `pyproject.toml` |
| lockfile | repository root `uv.lock`; direct/transitive dependency resolution authority |
| Python pin | repository root `.python-version`; exact 3.12 patch |
| sync | `uv sync --frozen` |
| start | `uv run aiscc serve` |
| build | `uv build` |
| test | `uv run pytest -q` |
| lint | `uv run ruff check .` |
| format check | `uv run ruff format --check .` |
| static/type check | `uv run mypy --strict src tests` |

- P1-3은 authorized registry access가 있는 별도 Task에서만 dependency resolution과 `uv.lock` 생성을 수행한다.
- CI/review는 `uv sync --frozen`을 사용하고 lockfile drift를 허용하지 않는다.
- source distribution/wheel build 가능성은 reproducibility check이며 deployment proof가 아니다.

## 7. canonical source layout와 entrypoint ownership

```text
runtime_source_root: src/aiscc/
test_root: tests/
versioned_non_secret_configuration_root: config/
container_evidence_root: containers/p1_3/
```

| path/module | semantic ownership |
|---|---|
| `src/aiscc/__main__.py` | console entrypoint; argument parsing 후 composition root만 호출 |
| `src/aiscc/bootstrap.py` | dependency composition; policy/runtime/persistence port 연결. business/security decision 없음 |
| `src/aiscc/api/` | FastAPI request/response adapter; authoritative state나 permission을 직접 mutate하지 않음 |
| `src/aiscc/contracts/` | P1-1/P1-2 exact enum과 immutable boundary DTO; kernel implementation 아님 |
| `src/aiscc/security/` | `SecurityAdmissionDecision`, exact action/state eligibility, permission/capability/cancel/limit/budget/provenance policy owner |
| `src/aiscc/runtime/` | admitted capability를 Docker/process/filesystem/network operation으로 실행하는 adapter와 cleanup owner |
| `src/aiscc/persistence/` | future PostgreSQL port/adapter와 transaction implementation; P1-3에서는 생성하지 않음 |
| `src/aiscc/workflow/` | future P1-4 state-machine kernel 전용; P1-3에서는 생성하지 않음 |
| `src/aiscc/providers/` | future P1-5 provider/tool adapter 전용; P1-3에서는 생성하지 않음 |

Dependency direction:

```text
api / cli
→ application composition
→ security policy port
→ runtime adapter

future workflow kernel
→ security admission port before side effect
→ separate TransitionRequest/Evaluation/Decision for workflow mutation
```

`security`는 workflow kernel을 import하거나 mutation callback을 호출하지 않는다. exact 9-state `WorkflowSnapshot`을 immutable input으로만 받는다. `runtime`은 `ALLOW`에 binding된 short-lived capability만 소비한다. security denial/runtime outcome은 event 또는 candidate이며 state change는 future P1-4 System transition authority가 별도로 입장한다.

## 8. sandbox와 runtime evidence substrate

### 8.1 exact candidate

```text
container sandbox/evidence runtime: Docker Engine with Linux containers
orchestration for local evidence fixtures: Docker Compose v2
host broker invocation: structured argv, shell=False, exact executable/action allowlist
```

P1-3은 Docker 기반 sandbox/evidence runtime을 사용한다. Docker installed/version output은 isolation proof가 아니며, 각 proof run은 engine version, OS/container mode, image digest, policy version과 implementation commit에 binding돼야 한다.

### 8.2 local requirement와 unavailable behavior

- Docker Engine must be reachable in Linux-container mode.
- P1-3 bootstrap에 pin된 image digest를 resolution/verification하려면 별도 authorized registry access가 필요하다.
- Docker/required image가 없고 offline evidence를 재현할 수 없으면 설치나 fallback을 추정하지 않고 `HUMAN_ENVIRONMENT_PREPARATION_REQUIRED`로 중단한다.
- Podman 또는 host-only process isolation로 자동 대체하지 않는다. substrate 변경은 Human-accepted baseline update가 필요하다.

### 8.3 per-run boundary

각 run/attempt는 unique Docker labels, container, workspace volume/directory, PID/process namespace, tmpfs, internal network/capability inventory와 lease를 가진다.

Default sandbox constraints:

- read-only root filesystem;
- exact run workspace만 read/write mount하고 owner repository, `.git`, host home, sibling workspace는 mount하지 않음;
- `/tmp`는 bounded tmpfs;
- non-root UID/GID, `no-new-privileges`, all Linux capabilities dropped;
- host PID/IPC/network namespace 공유 금지;
- finite CPU/memory/PID/file/output/wall-clock limit;
- Docker daemon socket과 host container runtime control을 sandbox 안에 mount하지 않음;
- detached/background escape 금지; host broker가 process/container tree와 lease를 소유.

### 8.4 network proof path

1. default-deny case는 `--network none`에서 direct DNS/socket/outbound attempt가 실제 실패하는지 관측한다.
2. explicit-allow case는 P1-3 전용 `--internal` Docker network와 exact local fixture service/port만 사용한다. external egress는 없고, redirect 또는 destination mismatch는 deny한다.
3. provider mediation은 fake local adapter/capability로만 검증한다. 실제 provider/network/credential은 사용하지 않는다.
4. mock/unit deny는 `NETWORK_RUNTIME` proof를 대체하지 않는다.

### 8.5 filesystem/process/cleanup proof path

- filesystem proof는 allowed workspace write 성공과 traversal/symlink/owner/sibling path 접근 실패를 함께 기록한다.
- process proof는 child/grandchild, detached attempt, PID/resource limit과 bounded termination을 실제 container에서 관측한다.
- timeout/cancel/crash마다 new work admission을 닫고 capability를 revoke한 뒤 container/process/network/volume inventory를 label로 reconcile한다.
- cleanup은 owned resource만 제거하며 broad host cleanup을 하지 않는다. residue가 있거나 ownership이 unknown이면 quarantine하고 PASS를 만들지 않는다.
- result artifact는 sanitization/hash 후 candidate로만 제출한다.

### 8.6 deployment boundary

Docker local evidence substrate가 Railway application service 안에서 Docker daemon을 사용할 수 있다는 뜻은 아니다. application HTTP process는 Railway-compatible direction을 유지하되, public Live sandbox worker placement와 release isolation capability는 후속 accepted design/release verification이 필요하다. compatible isolation plane이 없으면 `PUBLIC_BOUNDED_LIVE`를 enable하지 않고 zero-inference Replay를 유지한다.

## 9. persistence boundary

```text
production direction: PostgreSQL-compatible durable store
Python adapter direction: SQLAlchemy 2 async + asyncpg
migration direction: Alembic, forward-only reviewed revisions
transaction owner: application UnitOfWork / persistence adapter under System authority
```

- schema/table/column은 이 Task에서 설계하지 않는다.
- future P1-4는 transition decision event와 admitted state/version mutation을 하나의 atomic transaction boundary로 구현해야 한다.
- security decision/provenance append는 causal/current state-version binding을 보존하지만 security writer가 workflow state를 직접 mutate하지 않는다.
- P1-3 isolated unit/runtime proof는 in-memory fake repository/event sink를 사용할 수 있다.

```text
test adapter
!= production persistence
```

PostgreSQL adapter, Alembic configuration과 migration file은 P1-3 bootstrap allowlist에 포함하지 않으며 별도 persistence-owning Task가 승인해야 한다.

## 10. configuration과 secret boundary

- versioned non-secret policy는 `config/security/*.toml`에 저장하고 schema/version/hash를 가진다.
- process/deployment config는 `AISCC_` prefix environment에서 typed settings로 읽는다. non-secret environment value와 versioned file 사이 precedence는 code로 deterministic하게 고정한다.
- credential은 raw value가 아니라 `secret_ref`/opaque capability ID만 config와 domain에 들어간다.
- `.env`, API key, token, cookie, private key 또는 real credential fixture를 commit하지 않는다.
- local tests는 in-memory fake secret capability issuer와 synthetic canary를 사용한다. canary는 test process가 ephemeral하게 생성하고 repository file, argv, environment dump, log, evidence body 또는 Replay에 남기지 않는다.
- production secret manager 제품과 provider credential은 선택하거나 구성하지 않는다.
- unknown/missing config, policy version mismatch 또는 unresolved secret ref는 fail-closed `DENY`다.

## 11. future P1-3 bootstrap exact allowlist

Human-accepted reissued P1-3 Task는 아래 directory와 file만 creation 대상으로 삼을 수 있다. 기존 canonical 문서 수정, P1-4/P1-5 directory 생성 또는 목록 밖 확장은 새 Task authorization이 필요하다.

### 11.1 roots and package files

```text
.python-version
pyproject.toml
uv.lock
.dockerignore
src/aiscc/
tests/
config/security/
containers/p1_3/
```

### 11.2 exact application/interface files

```text
src/aiscc/__init__.py
src/aiscc/__main__.py
src/aiscc/bootstrap.py
src/aiscc/api/__init__.py
src/aiscc/api/app.py
src/aiscc/api/routes/__init__.py
src/aiscc/api/routes/health.py
src/aiscc/api/routes/control.py
src/aiscc/contracts/__init__.py
src/aiscc/contracts/workflow.py
src/aiscc/contracts/security.py
```

`contracts/workflow.py`는 accepted P1-1 exact enum/snapshot interface만 담고 transition engine, mutable aggregate 또는 persistence를 구현하지 않는다.

### 11.3 exact security/runtime files

```text
src/aiscc/security/__init__.py
src/aiscc/security/models.py
src/aiscc/security/policy.py
src/aiscc/security/action_state.py
src/aiscc/security/capability.py
src/aiscc/security/cancel.py
src/aiscc/security/limits.py
src/aiscc/security/provenance.py
src/aiscc/security/redaction.py
src/aiscc/runtime/__init__.py
src/aiscc/runtime/contracts.py
src/aiscc/runtime/process.py
src/aiscc/runtime/docker.py
src/aiscc/runtime/network.py
src/aiscc/runtime/cleanup.py
```

### 11.4 exact non-secret config/container files

```text
config/security/permission-profiles.v1.toml
config/security/resource-policy.v1.toml
config/security/limits.v1.toml
containers/p1_3/Dockerfile.sandbox
containers/p1_3/Dockerfile.evidence
containers/p1_3/compose.yaml
```

### 11.5 exact test and fixture files

```text
tests/conftest.py
tests/unit/security/test_permission_policy.py
tests/unit/security/test_action_state_eligibility.py
tests/unit/security/test_public_cancel_authorization.py
tests/unit/security/test_capability_lifetime.py
tests/unit/security/test_limits_idempotency_budget.py
tests/integration/security/test_broker_fail_closed.py
tests/integration/security/test_provenance_redaction.py
tests/runtime/security/test_sandbox_isolation.py
tests/runtime/security/test_network_boundary.py
tests/runtime/security/test_secret_non_exposure.py
tests/runtime/security/test_timeout_retry_cancel.py
tests/runtime/security/test_idempotency_abuse_budget.py
tests/runtime/security/test_cleanup_residue.py
tests/runtime/security/test_failure_domain.py
tests/runtime/security/test_action_state_cancel_authorization.py
tests/fixtures/sandbox/allowed/input.txt
tests/fixtures/sandbox/probe.py
tests/fixtures/network/fixture_server.py
```

This accepted allowlist authorizes an explicit P1-3 implementation Task to create these paths; this baseline itself did not create them. `src/aiscc/workflow/`, `src/aiscc/providers/`, `src/aiscc/persistence/`, database migrations, actual public scenarios and deployment files are explicitly outside P1-3 bootstrap.

## 12. dependency/version authority

| change | authority |
|---|---|
| Python major/minor compatibility line | separate Human-accepted substrate baseline update |
| FastAPI compatibility line/major boundary, Pydantic major | separate Human-accepted substrate baseline update |
| `uv` replacement, build backend replacement, manifest/lock strategy | separate Human-accepted substrate baseline update |
| Docker→Podman/host/remote sandbox strategy or isolation model | separate Human-accepted security/substrate baseline update |
| PostgreSQL/SQLAlchemy/Alembic direction change | separate Human-accepted persistence/substrate baseline update |
| exact runtime patch within 3.12.x | authorized implementation/maintenance Task may update after tests, lock regeneration and evidence freshness check |
| compatible dependency patch/minor | authorized maintenance Task may update with reviewed `uv.lock`, applicable test/security evidence and provenance |
| security-sensitive dependency or container base digest | explicit Task, current advisory/license review and affected runtime proof required |

No Agent/provider output may self-authorize dependency, runtime or sandbox changes. Lockfile change without manifest/reason/evidence provenance is denied.

## 13. P1-3 proof and resume contract

P1-3 must produce non-substitutable evidence for accepted P1-2 proof classes. Static source/unit/integration evidence does not replace actual Docker filesystem/process/network/secret/timeout/cancel/budget/cleanup/failure-domain evidence. Each artifact binds Task, implementation commit, runtime/image/policy version, scenario, expected/actual result and timestamp.

The `ACTION_STATE_CANCEL_AUTHORIZATION_RUNTIME` seven-case matrix remains mandatory, including wrong-state deny, stale capability deny, terminal side-effect deny, safety settling, cross-session cancel deny, read/run-ID not cancel authority, and idempotent one-intent behavior.

```text
After Human accepts AISCC_RUNTIME_SUBSTRATE.md
→ reissued P1-3 implementation Task may create only the authorized runtime bootstrap
→ implement the P1-2 security safeguard slice
→ produce non-substitutable runtime evidence
→ preserve Human judgment as a separate gate

P1-4 remains separate and NOT_STARTED.
```

At design-candidate submission:

```text
result: ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING
runtime bootstrap: NOT_CREATED
safeguard implementation: NOT_STARTED
runtime proof: NOT_EXECUTED
```

Current accepted substrate state:

```text
runtime substrate: HUMAN_PROVIDED / ACCEPTED
P1-3 safeguard implementation: READY / NOT_STARTED
P1-3 runtime proof: NOT_EXECUTED
P1-4: NOT_STARTED
```

## 14. Human acceptance

Human final review accepted:

1. Python primary and TypeScript/Node fallback;
2. FastAPI boundary and strict typing discipline;
3. `uv`/Hatchling manifest-lock-build convention;
4. exact `src/`, `tests/`, `config/`, `containers/p1_3/` layout;
5. Docker Linux sandbox/evidence strategy and release-environment limitation;
6. PostgreSQL/SQLAlchemy/Alembic direction without schema design;
7. configuration/secret-reference convention;
8. exact future P1-3 bootstrap allowlist;
9. version/dependency authority boundary.

Current Human status:

```text
HUMAN_PROVIDED / ACCEPTED
```
