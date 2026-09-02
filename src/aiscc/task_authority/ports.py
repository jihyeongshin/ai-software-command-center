from __future__ import annotations

from typing import Protocol

from aiscc.task_authority.models import (
    NextActionContextAuthorityEventV1,
    NextActionContextFoldResult,
    NextActionContextRefV1,
    TaskConstraintFoldResult,
    TaskConstraintOwnerSnapshotV1,
    TaskConstraintRefV1,
)


class ExternalTaskAuthorityReadPort(Protocol):
    async def get_task_constraint(self, constraint_ref: str) -> TaskConstraintRefV1 | None: ...

    async def get_next_action_context(self, context_ref: str) -> NextActionContextRefV1 | None: ...

    async def get_context_event(
        self, event_ref: str
    ) -> NextActionContextAuthorityEventV1 | None: ...

    async def latest_snapshot(self) -> TaskConstraintOwnerSnapshotV1: ...


class ExternalTaskAuthorityVerifierPort(ExternalTaskAuthorityReadPort, Protocol):
    async def verify_task_constraint(
        self,
        *,
        constraint_ref: str,
        constraint_fingerprint: str,
        snapshot_ref: str,
        snapshot_fingerprint: str,
        owner_event_high_watermark: int,
        require_current: bool,
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
    ) -> NextActionContextFoldResult: ...
