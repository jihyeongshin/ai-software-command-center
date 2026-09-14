from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from aiscc.task_authority.contracts import IssuedTaskContractV1, VerifiedTaskContractBindingV1
from aiscc.task_authority.models import (
    NextActionContextAuthorityEventV1,
    NextActionContextFoldResult,
    NextActionContextRefV1,
    TaskConstraintFoldResult,
    TaskConstraintOwnerSnapshotV1,
    TaskConstraintRefV1,
)


class ExternalTaskAuthorityReadPort(Protocol):
    async def get_task_contract(
        self,
        project_id: str,
        contract_id: str,
        version: int,
        *,
        session: AsyncSession | None = None,
    ) -> IssuedTaskContractV1 | None: ...

    async def get_task_constraint(self, constraint_ref: str) -> TaskConstraintRefV1 | None: ...

    async def get_next_action_context(self, context_ref: str) -> NextActionContextRefV1 | None: ...

    async def get_context_event(
        self, event_ref: str
    ) -> NextActionContextAuthorityEventV1 | None: ...

    async def latest_snapshot(
        self, *, session: AsyncSession | None = None
    ) -> TaskConstraintOwnerSnapshotV1: ...


class ExternalTaskAuthorityVerifierPort(ExternalTaskAuthorityReadPort, Protocol):
    async def verify_task_contract(
        self,
        binding: IssuedTaskContractV1,
        *,
        require_current: bool,
        expected_repository_binding: Mapping[str, str],
        expected_next_action_ref: str,
        session: AsyncSession | None = None,
    ) -> VerifiedTaskContractBindingV1: ...

    async def verify_task_constraint(
        self,
        *,
        constraint_ref: str,
        constraint_fingerprint: str,
        snapshot_ref: str,
        snapshot_fingerprint: str,
        owner_event_high_watermark: int,
        require_current: bool,
        session: AsyncSession | None = None,
    ) -> TaskConstraintFoldResult: ...

    async def verify_next_action_context(
        self,
        *,
        context_ref: str,
        context_fingerprint: str,
        introduction_event_ref: str,
        introduction_event_fingerprint: str,
        snapshot_ref: str,
        snapshot_fingerprint: str,
        owner_event_high_watermark: int,
        require_current: bool,
        session: AsyncSession | None = None,
    ) -> NextActionContextFoldResult: ...
