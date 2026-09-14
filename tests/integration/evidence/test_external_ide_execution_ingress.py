import asyncio
from dataclasses import replace
from uuid import uuid4

import pytest
from sqlalchemy import text

from aiscc.contracts.workflow import WorkflowState
from aiscc.evidence.issuers import P1_5EvidenceIssuerAuthority
from aiscc.evidence.models import (
    EvidenceCandidate,
    EvidenceCheckpointRef,
    EvidenceContentKind,
    EvidenceContentRef,
    EvidenceIssuerType,
    EvidenceOwner,
    EvidenceSensitivity,
)
from aiscc.evidence.repository import (
    HistoricalEvidenceProvenanceError,
    _verify_historical_p1_5_producer,
)
from aiscc.providers.external_ide import (
    ISSUER,
    VERSION,
    ExternalIdeExecutionRepository,
    LocalGitObserver,
)
from tests.integration.providers.test_external_ide_execution_ingress import complete, fixture
from tests.integration.task_authority.test_task_contract_durability import (
    database_url as database_url,
)
from tests.unit.providers.test_external_ide_execution_ingress import GIT, NOW


def candidate(result):
    ref = result.common_ref
    content = EvidenceContentRef(
        EvidenceContentKind.P1_5_IMMUTABLE_PRODUCER_REF,
        ISSUER,
        VERSION,
        ref.submission_id,
        VERSION,
        "P1_5_IMMUTABLE_REF_EXACT_BYTES",
        "AISCC-EXTERNAL-IDE-SUBMISSION-V1",
        VERSION,
        len(result.canonical_body),
        ref.event_range_hash,
        EvidenceSensitivity.INTERNAL,
        "P1_5_PRIVATE_REF_RETENTION_V1",
        "PRIVATE_AUTHORITY_ONLY",
    )
    return EvidenceCandidate(
        candidate_id="external-" + uuid4().hex,
        candidate_version=VERSION,
        candidate_fingerprint="",
        issuer=EvidenceOwner(
            EvidenceIssuerType.P1_5_EXECUTION_SUBMISSION, ISSUER, VERSION, ISSUER + "@" + VERSION
        ),
        producer_work_run_id=ref.work_run_id,
        execution_attempt_id=ref.execution_attempt_id,
        operation_id=None,
        task_contract_id=ref.task_contract_id,
        task_contract_version=ref.task_contract_version,
        checkpoint_ref=EvidenceCheckpointRef("completion", VERSION),
        observed_state=WorkflowState.RUNNING,
        observed_state_version=ref.state_version,
        subject_id="source",
        scope_id="source",
        resource_id=None,
        evidence_type_id="execution",
        evidence_type_version=VERSION,
        content_ref=content,
        created_at=NOW,
        observed_at=NOW,
        coverage=frozenset(),
        producer_attestation_ref=ref.submission_id,
    )


@pytest.mark.postgres
def test_live_and_historical_restart_exact_external_binding(database_url, tmp_path):
    async def scenario():
        f = await fixture(database_url, tmp_path)
        try:
            (tmp_path / "src/file.txt").write_bytes(b"after\n")
            result = await complete(f)
            restarted = ExternalIdeExecutionRepository(
                f["sessions"], f["repo"], LocalGitObserver(GIT)
            )
            issuer = P1_5EvidenceIssuerAuthority(
                EvidenceIssuerType.P1_5_EXECUTION_SUBMISSION, ISSUER, VERSION, restarted
            )
            raw = candidate(result)
            value = await issuer.seed_external_candidate(raw, restarted)
            assert await issuer.recognizes(value)
            async with f["sessions"]() as session, session.begin():
                await _verify_historical_p1_5_producer(session, value)
                for table in (
                    "evidence_candidates",
                    "admitted_evidence",
                    "judgments",
                    "human_results",
                ):
                    # Completion and producer validation do not insert evidence or judgments.
                    column = (
                        "producer_work_run_id" if table == "evidence_candidates" else "work_run_id"
                    )
                    if table == "evidence_candidates":
                        assert (
                            await session.scalar(
                                text(
                                    "SELECT count(*) FROM evidence_candidates WHERE candidate_id=:i"
                                ),
                                {"i": value.candidate_id},
                            )
                            == 0
                        )
                    elif table != "admitted_evidence":
                        assert (
                            await session.scalar(
                                text(f"SELECT count(*) FROM {table} WHERE {column}=:i"),
                                {"i": value.producer_work_run_id},
                            )
                            == 0
                        )
            variants = [
                replace(raw, producer_attestation_ref="external-ide-submission:missing"),
                replace(raw, content_ref=replace(raw.content_ref, content_hash="f" * 64)),
                replace(raw, producer_work_run_id="wrong-run"),
                replace(raw, task_contract_id="wrong-task"),
                replace(raw, task_contract_version="v2"),
                replace(raw, execution_attempt_id="fake-provider-attempt"),
                replace(raw, issuer=replace(raw.issuer, owner_id="caller-spoof")),
                replace(raw, observed_state_version=3),
            ]
            for wrong in variants:
                with pytest.raises(ValueError):
                    await issuer.seed_external_candidate(wrong, restarted)
                async with f["sessions"]() as session, session.begin():
                    with pytest.raises(HistoricalEvidenceProvenanceError):
                        await _verify_historical_p1_5_producer(session, wrong)
        finally:
            await f["engine"].dispose()

    asyncio.run(scenario())
