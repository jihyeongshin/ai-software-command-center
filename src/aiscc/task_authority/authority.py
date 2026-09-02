from __future__ import annotations

from datetime import datetime
from typing import NoReturn

from aiscc.task_authority.models import (
    NextActionContextAuthorityEventV1,
    NextActionContextRefV1,
    NextActionPriorityClass,
    TaskConstraintAuthorityEventV1,
    TaskConstraintOwnerSnapshotV1,
    TaskConstraintRefV1,
    TaskConstraintScopeV1,
)
from aiscc.task_authority.repository import PostgresExternalTaskAuthorityRepository


class _ExternalTaskAuthorityWriter:
    """Opaque live capability owned only by the private Task-authority composition root."""

    __slots__ = ("__repository", "__capability")
    __repository: PostgresExternalTaskAuthorityRepository
    __capability: object

    def __init__(
        self, repository: PostgresExternalTaskAuthorityRepository, capability: object
    ) -> None:
        self.__repository = repository
        self.__capability = capability

    def __copy__(self) -> NoReturn:
        raise TypeError("external Task-authority capability cannot be copied")

    def __deepcopy__(self, memo: object) -> NoReturn:
        del memo
        raise TypeError("external Task-authority capability cannot be copied")

    def __reduce__(self) -> NoReturn:
        raise TypeError("external Task-authority capability cannot be serialized")

    async def issue_task_constraint(
        self,
        *,
        constraint_ref_id: str,
        logical_constraint_id: str,
        scope: TaskConstraintScopeV1,
        constraint_schema_id: str,
        constraint_schema_version: str,
        constraint_payload_ref: str,
        constraint_payload_fingerprint: str,
        event_id: str,
        issued_at: datetime,
    ) -> tuple[TaskConstraintRefV1, TaskConstraintAuthorityEventV1]:
        return await self.__repository._issue_task_constraint(
            self.__capability,
            constraint_ref_id=constraint_ref_id,
            logical_constraint_id=logical_constraint_id,
            scope=scope,
            constraint_schema_id=constraint_schema_id,
            constraint_schema_version=constraint_schema_version,
            constraint_payload_ref=constraint_payload_ref,
            constraint_payload_fingerprint=constraint_payload_fingerprint,
            event_id=event_id,
            issued_at=issued_at,
        )

    async def supersede_task_constraint(
        self,
        *,
        current_constraint_ref: str,
        replacement_ref_id: str,
        constraint_schema_id: str,
        constraint_schema_version: str,
        constraint_payload_ref: str,
        constraint_payload_fingerprint: str,
        event_id: str,
        effective_at: datetime,
    ) -> tuple[TaskConstraintRefV1, TaskConstraintAuthorityEventV1]:
        return await self.__repository._supersede_task_constraint(
            self.__capability,
            current_constraint_ref=current_constraint_ref,
            replacement_ref_id=replacement_ref_id,
            constraint_schema_id=constraint_schema_id,
            constraint_schema_version=constraint_schema_version,
            constraint_payload_ref=constraint_payload_ref,
            constraint_payload_fingerprint=constraint_payload_fingerprint,
            event_id=event_id,
            effective_at=effective_at,
        )

    async def revoke_task_constraint(
        self,
        *,
        current_constraint_ref: str,
        event_id: str,
        effective_at: datetime,
    ) -> TaskConstraintAuthorityEventV1:
        return await self.__repository._revoke_task_constraint(
            self.__capability,
            current_constraint_ref=current_constraint_ref,
            event_id=event_id,
            effective_at=effective_at,
        )

    async def issue_next_action_context(
        self,
        *,
        context_ref_id: str,
        context_logical_local_id: str,
        project_id: str,
        task_contract_id: str,
        task_contract_version: str,
        context_slot_id: str,
        priority_class: NextActionPriorityClass,
        critical_path_ordinal: int,
        event_id: str,
        issued_at: datetime,
    ) -> tuple[NextActionContextRefV1, NextActionContextAuthorityEventV1]:
        return await self.__repository._issue_next_action_context(
            self.__capability,
            context_ref_id=context_ref_id,
            context_logical_local_id=context_logical_local_id,
            project_id=project_id,
            task_contract_id=task_contract_id,
            task_contract_version=task_contract_version,
            context_slot_id=context_slot_id,
            priority_class=priority_class,
            critical_path_ordinal=critical_path_ordinal,
            event_id=event_id,
            issued_at=issued_at,
        )

    async def supersede_next_action_context(
        self,
        *,
        current_context_ref: str,
        replacement_ref_id: str,
        priority_class: NextActionPriorityClass,
        critical_path_ordinal: int,
        event_id: str,
        effective_at: datetime,
    ) -> tuple[NextActionContextRefV1, NextActionContextAuthorityEventV1]:
        return await self.__repository._supersede_next_action_context(
            self.__capability,
            current_context_ref=current_context_ref,
            replacement_ref_id=replacement_ref_id,
            priority_class=priority_class,
            critical_path_ordinal=critical_path_ordinal,
            event_id=event_id,
            effective_at=effective_at,
        )

    async def revoke_next_action_context(
        self,
        *,
        current_context_ref: str,
        event_id: str,
        effective_at: datetime,
    ) -> NextActionContextAuthorityEventV1:
        return await self.__repository._revoke_next_action_context(
            self.__capability,
            current_context_ref=current_context_ref,
            event_id=event_id,
            effective_at=effective_at,
        )

    async def certify_snapshot(
        self, *, snapshot_id: str, issued_at: datetime
    ) -> TaskConstraintOwnerSnapshotV1:
        return await self.__repository._certify_snapshot(
            self.__capability, snapshot_id=snapshot_id, issued_at=issued_at
        )


def _bind_repository_once(
    repository: PostgresExternalTaskAuthorityRepository,
) -> _ExternalTaskAuthorityWriter:
    """Private composition-root hook; intentionally absent from package exports."""

    capability = object()
    repository._bind_writer_capability(capability)
    return _ExternalTaskAuthorityWriter(repository, capability)
