from __future__ import annotations

import asyncio

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from aiscc.evidence.models import EvidenceAuthorityConflictError
from aiscc.evidence.repository import PostgresEvidenceRepository


def test_definition_resolver_denies_before_access_without_caller_transaction():
    def no_session_factory():
        raise AssertionError("definition resolver opened a session")

    async def scenario():
        repository = PostgresEvidenceRepository(no_session_factory)
        async with AsyncSession() as session:
            with pytest.raises(EvidenceAuthorityConflictError, match="caller transaction"):
                await repository.verify_requirement_definition_graph(
                    session,
                    task_contract_id="task",
                    task_contract_version="v1",
                    requirement_set_ref="set@v1",
                    expected_requirement_set_fingerprint="0" * 64,
                    expected_checkpoints=(),
                )
            assert not session.in_transaction()

    asyncio.run(scenario())
