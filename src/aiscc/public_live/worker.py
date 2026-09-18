"""Private Public Live worker composition and distinct Live DB binding."""

from __future__ import annotations

import asyncio
import hashlib
import logging
import os
import shutil
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot, WorkflowState
from aiscc.persistence import create_engine, create_session_factory
from aiscc.persistence.public_live import PublicLiveRepository
from aiscc.persistence.repository import PostgresExecutionRepository
from aiscc.providers.authority import (
    ExecutionReferenceAuthority,
    ProviderToolResourceAuthority,
    SecretResolutionLeaseAuthority,
    SecretUseAuthority,
)
from aiscc.providers.hosted_secret import HostedOpenAISecretResolver
from aiscc.providers.models import (
    ExecutionAttemptRef,
    ExecutionStatus,
    ProviderProfile,
)
from aiscc.providers.openai_responses import OpenAIResponsesAdapter
from aiscc.providers.service import AgentExecutionService
from aiscc.public_live.context_authority import PublicLiveContextResourceAuthority
from aiscc.public_live.luna_profile import hosted_luna_profile
from aiscc.public_live.provider_authority import luna_permission_profiles
from aiscc.public_live.provider_pipeline import PipelineStore
from aiscc.public_live.stockroom_runtime import compose_public_stockroom
from aiscc.public_live.worker_authority import (
    ActiveClaim,
    DurableWorkerAuthority,
    WorkerRepository,
    run_worker_loop,
)
from aiscc.security.policy import SecurityPolicy

_LOGGER = logging.getLogger("aiscc.public_live.worker")
_OBSERVATION_DOMAIN = "AISCC-PUBLIC-WORKER-OBSERVATION-V1"


@dataclass(frozen=True, slots=True)
class WorkerObservation:
    """Secret-safe, allowlisted worker diagnostic suitable for hosted logs."""

    stage: str
    code: str
    digest: str


def stockroom_runtime_observation() -> WorkerObservation:
    code = (
        "PUBLIC_LIVE_STOCKROOM_DOCKER_PRESENT"
        if shutil.which("docker") is not None
        else "PUBLIC_LIVE_STOCKROOM_DOCKER_REQUIRED"
    )
    return _worker_observation("RUNTIME_PREREQUISITE", code)


def stockroom_daemon_observation(
    socket_path: Path = Path("/var/run/docker.sock"),
) -> WorkerObservation:
    code = (
        "PUBLIC_LIVE_STOCKROOM_DOCKER_SOCKET_PRESENT"
        if socket_path.is_socket()
        else "PUBLIC_LIVE_STOCKROOM_DOCKER_SOCKET_REQUIRED"
    )
    return _worker_observation("RUNTIME_DAEMON", code)


def classify_worker_failure(error: BaseException) -> WorkerObservation:
    if type(error) is RuntimeError and error.args == ("PUBLIC_LIVE_STOCKROOM_DOCKER_REQUIRED",):
        return _worker_observation(
            "STOCKROOM_COMPOSITION",
            "PUBLIC_LIVE_STOCKROOM_DOCKER_REQUIRED",
        )
    return _worker_observation("CLAIM_EXECUTION", "PUBLIC_WORKER_FAILURE_UNCLASSIFIED")


def _worker_observation(stage: str, code: str) -> WorkerObservation:
    payload = "\0".join((_OBSERVATION_DOMAIN, stage, code)).encode("ascii")
    return WorkerObservation(stage, code, hashlib.sha256(payload).hexdigest())


def _emit_worker_observation(observation: WorkerObservation) -> None:
    _LOGGER.warning(
        "public_live_worker stage=%s code=%s digest=%s",
        observation.stage,
        observation.code,
        observation.digest,
    )


@dataclass(frozen=True)
class WorkerSettings:
    database_url: str

    @classmethod
    def from_environment(cls, environ: Mapping[str, str] = os.environ) -> WorkerSettings:
        if "AISCC_DATABASE_URL" in environ:
            raise ValueError("PUBLIC_WORKER_OWNER_DATABASE_DENIED")
        database_url = environ.get("AISCC_PUBLIC_LIVE_DATABASE_URL", "")
        if not database_url:
            raise ValueError("PUBLIC_WORKER_LIVE_DATABASE_REQUIRED")
        # Worker is the only composition where the hosted key may be present.
        # Its value is not read here; HostedOpenAISecretResolver resolves it only
        # after a single-use server-owned lease is consumed.
        return cls(database_url)


@dataclass
class HostedPublicLiveWorker:
    """Fixed hosted owners; work is supplied only by the durable server pipeline."""

    engine: AsyncEngine
    store: PipelineStore
    adapter: Any
    authority: DurableWorkerAuthority
    semantic_validator: Callable[[str, Any], MappingProxyType[str, Any]] | None
    stockroom_runner: Callable[..., Any] | None
    last_stockroom_dispatcher: Any | None
    execute_claim: Callable[[ActiveClaim], Awaitable[str]]

    @property
    def profile(self) -> ProviderProfile:
        return hosted_luna_profile()

    async def close(self) -> None:
        await self.engine.dispose()

    def check(self) -> None:
        if self.profile != hosted_luna_profile() or self.adapter.invocation_count != 0:
            raise RuntimeError("PUBLIC_WORKER_COMPOSITION_INVALID")

    async def run(self, stop: asyncio.Event) -> None:
        _emit_worker_observation(stockroom_runtime_observation())
        _emit_worker_observation(stockroom_daemon_observation())
        await run_worker_loop(
            self.authority,
            self.execute_claim,
            stop,
            observe_failure=lambda error: _emit_worker_observation(classify_worker_failure(error)),
        )


def create_worker(
    environ: Mapping[str, str] = os.environ,
    *,
    execute_claim: Callable[[ActiveClaim], Awaitable[str]] | None = None,
    semantic_validator: Callable[[str, Any], MappingProxyType[str, Any]] | None = None,
    stockroom_runner: Callable[..., Any] | None = None,
) -> HostedPublicLiveWorker:
    settings = WorkerSettings.from_environment(environ)
    engine = create_engine(settings.database_url, role="aiscc_public_live_execution")
    sessions = create_session_factory(engine)
    repository = PublicLiveRepository(sessions)
    worker_repository = WorkerRepository(sessions)
    authority = DurableWorkerAuthority(worker_repository)
    worker = HostedPublicLiveWorker(
        engine,
        PipelineStore(repository, repository),
        OpenAIResponsesAdapter(hosted=True),
        authority,
        semantic_validator,
        stockroom_runner,
        None,
        execute_claim or (lambda claim: _execute_production_claim(worker, sessions, claim)),
    )
    return worker


async def _execute_production_claim(
    worker: HostedPublicLiveWorker,
    sessions: async_sessionmaker[AsyncSession],
    active: ActiveClaim,
) -> str:
    """Execute one exact claimed Public Live aggregate through canonical P1-5."""
    claim = active.current()
    context = await worker.authority.repository.context(claim)
    state_version = context.get("state_version")
    execution_version = context.get("execution_version")
    work_run_id = context.get("work_run_id")
    attempt_id = context.get("execution_attempt_id")
    if not (
        isinstance(state_version, int)
        and isinstance(execution_version, int)
        and isinstance(work_run_id, str)
        and isinstance(attempt_id, str)
    ):
        raise RuntimeError("PUBLIC_WORKER_CONTEXT_INVALID")
    state_version_value: int = state_version
    execution_version_value: int = execution_version
    work_run_id_value: str = work_run_id
    attempt_id_value: str = attempt_id
    profile = hosted_luna_profile()
    current = WorkflowSnapshot(
        work_run_id_value,
        WorkflowState.RUNNING,
        state_version_value,
    )
    context_owner = PublicLiveContextResourceAuthority(
        profile=profile,
        current=current,
        attempt=attempt_id_value,
        principal="aiscc-public-live-worker",
    )
    stockroom = compose_public_stockroom(
        run_id=work_run_id_value,
        attempt_id=attempt_id_value,
        principal="aiscc-public-live-worker",
        profile=profile,
    )
    stockroom_definition = stockroom.registry.tools["stockroom_summary"]
    stockroom_resource_identity = ":".join(
        (
            stockroom.registry.registry_id,
            stockroom.registry.version,
            stockroom_definition.tool_id,
            stockroom_definition.schema_version,
            stockroom_definition.dispatcher_version,
        )
    )
    provider_authority = ProviderToolResourceAuthority(
        allowed_resource_identities=frozenset(
            {profile.provider_resource_identity, stockroom_resource_identity}
        ),
        allowed_profile_ids=frozenset({profile.profile_id}),
        allowed_scenarios=frozenset({profile.public_scenario_identity}),
        allowed_modes=frozenset({RuntimeMode.PUBLIC_BOUNDED_LIVE}),
    )
    secret_authority = SecretUseAuthority(
        allowed_secret_refs=frozenset({profile.secret_ref}),
        allowed_profile_ids=frozenset({profile.profile_id}),
        allowed_scenarios=frozenset({profile.public_scenario_identity}),
        allowed_destinations=frozenset({profile.endpoint_ref}),
        allowed_modes=frozenset({RuntimeMode.PUBLIC_BOUNDED_LIVE}),
    )
    policy = SecurityPolicy(
        luna_permission_profiles(),
        stockroom_policy=stockroom.scope_authority,
        public_context_policy=context_owner,
        provider_tool_policy=provider_authority,
        secret_use_policy=secret_authority,
    )
    lease_authority = SecretResolutionLeaseAuthority(policy.verify_consumption_receipt)

    class Reader:
        def load(self, **_kw: Any) -> tuple[WorkflowSnapshot, ExecutionAttemptRef]:
            return current, ExecutionAttemptRef(
                attempt_id_value,
                work_run_id_value,
                "public-live",
                "1",
                WorkflowState.RUNNING,
                state_version_value,
                execution_version_value,
                ExecutionStatus.RUNNING,
                "public-live",
                runtime_mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
                project_id=profile.public_repository_resource_identity,
                provider_profile_id=profile.profile_id,
                provider_profile_version=profile.version,
                tool_registry_id=profile.tool_registry_id,
                tool_registry_version=profile.tool_registry_version,
            )

    dispatcher = stockroom.dispatcher(
        policy,
        runner=worker.stockroom_runner,
        attempt_id=attempt_id_value,
    )
    worker.last_stockroom_dispatcher = dispatcher
    execution = AgentExecutionService(
        policy=policy,
        adapter=worker.adapter,
        secret_resolver=HostedOpenAISecretResolver(lease_authority),
        authority_reader=Reader(),
        secret_lease_authority=lease_authority,
        repository=PostgresExecutionRepository(sessions),
        provider_tool_authority=provider_authority,
        secret_use_authority=secret_authority,
        profile=profile,
        tool_registry=stockroom.registry,
        tool_dispatcher=dispatcher,
        execution_ref_authority=ExecutionReferenceAuthority(),
        server_initial_inputs={
            "stockroom-s1-normal": (
                {"role": "system", "content": "Use only the fixed Stockroom context."},
                {"role": "user", "content": "Produce the bounded Stockroom summary."},
            )
        },
        stockroom_context_factory=stockroom.scope_authority.issue_context,
        stockroom_dispatch_context_factory=stockroom.scope_authority.build_dispatch_context,
        public_context_authority=context_owner,
        public_semantic_validator=worker.semantic_validator,
    )
    result = await execution.execute(
        work_run_id=work_run_id,
        execution_attempt_id=attempt_id,
        principal="aiscc-public-live-worker",
        scenario_id="stockroom-s1-normal",
        public_claim=active,
        public_worker_repository=worker.authority.repository,
    )
    return "EXECUTION_TERMINAL" if result.status != "CONTINUATION_REQUIRED" else "KNOWN_STEP_CLOSED"
