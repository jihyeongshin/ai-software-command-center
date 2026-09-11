from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from aiscc.scenarios.composition import (
    StockroomOwnerPreparation,
    bind_stockroom_owner_dependencies,
    build_stockroom_owner_composition,
)
from aiscc.scenarios.driver import StockroomOwnerDependencies
from aiscc.security.models import PermissionProfile
from aiscc.security.policy import SecurityPolicy, default_profiles

if TYPE_CHECKING:
    from aiscc.runtime.docker import DockerRunSpec, StockroomProcessObservation
    from aiscc.scenarios.stockroom_production import StockroomProductionApplication


def build_security_policy(
    *,
    provider_tool_policy: object | None = None,
    secret_use_policy: object | None = None,
    stockroom_policy: object | None = None,
) -> SecurityPolicy:
    """Composition root for the P1-3 security policy; it owns no workflow mutation."""
    profiles: dict[str, PermissionProfile] = default_profiles()
    return SecurityPolicy(
        profiles=profiles,
        provider_tool_policy=provider_tool_policy,
        secret_use_policy=secret_use_policy,
        stockroom_policy=stockroom_policy,
    )


def build_stockroom_owner_preparation(
    *, owners: StockroomOwnerDependencies
) -> StockroomOwnerPreparation:
    """Explicit owner-only inert preparation root; it performs no execution."""
    return bind_stockroom_owner_dependencies(build_stockroom_owner_composition(), owners)


async def build_stockroom_production(
    *,
    session_factory: async_sessionmaker[AsyncSession],
    repository_root: Path,
    private_runtime_root: Path,
    downloads_root: Path,
    trusted_git_executable: Path,
    docker_process_runner: Callable[[Sequence[str], DockerRunSpec], StockroomProcessObservation],
    project_id: str,
    requester_identity: str,
    human_selector_fingerprint: str,
    secret_material_by_ref: Mapping[str, str],
    clock: Callable[[], datetime] | None = None,
) -> StockroomProductionApplication:
    """Build the explicit PostgreSQL-backed Stockroom production owner graph."""
    from aiscc.scenarios.stockroom_production import (
        build_stockroom_production_application,
    )

    return await build_stockroom_production_application(
        session_factory=session_factory,
        repository_root=repository_root,
        private_runtime_root=private_runtime_root,
        downloads_root=downloads_root,
        trusted_git_executable=trusted_git_executable,
        docker_process_runner=docker_process_runner,
        project_id=project_id,
        requester_identity=requester_identity,
        human_selector_fingerprint=human_selector_fingerprint,
        secret_material_by_ref=secret_material_by_ref,
        clock=clock,
    )
