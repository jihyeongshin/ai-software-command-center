import asyncio

import pytest

from aiscc.evidence.repository import (
    HistoricalEvidenceProvenanceError,
    _verify_historical_p1_5_producer,
)


def test_caller_external_label_without_durable_row_fails_closed():
    from types import SimpleNamespace

    from aiscc.providers.external_ide import ISSUER

    class EmptySession:
        async def get(self, model, identity):
            return None

    value = SimpleNamespace(
        producer_attestation_ref="external-ide-submission:missing",
        issuer=SimpleNamespace(owner_id=ISSUER),
    )
    with pytest.raises(HistoricalEvidenceProvenanceError):
        asyncio.run(_verify_historical_p1_5_producer(EmptySession(), value))
