from __future__ import annotations

from aiscc.evidence.models import EvidenceCheckpoint, EvidenceRequirement


def requirement_applies(
    requirement: EvidenceRequirement,
    checkpoint: EvidenceCheckpoint,
) -> bool:
    return checkpoint.ref.serialized() in requirement.applicable_checkpoint_refs


def applicable_requirements(
    requirements: tuple[EvidenceRequirement, ...],
    checkpoint: EvidenceCheckpoint,
) -> tuple[EvidenceRequirement, ...]:
    return tuple(item for item in requirements if requirement_applies(item, checkpoint))
