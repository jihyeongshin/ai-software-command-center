from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from aiscc.cycle.models import MemoryCategory
from aiscc.evidence.models import canonical_hash
from aiscc.memory.models import (
    MemoryApplicabilityState,
    MemoryAuthorityMode,
    MemoryDeclarationAuthorityPolicy,
    PrivacyClassification,
    ProjectMemoryEntry,
    ProjectMemoryError,
    ProjectMemoryErrorCode,
    RetrievedMemory,
    memory_content_fingerprint,
    memory_lineage_key,
)
from aiscc.persistence.models import (
    AdmittedCycleRow,
    EvidenceAuthorityEventRow,
    ProjectMemoryAuthorityEventRow,
    ProjectMemoryEntryRow,
    ProjectMemoryViewRow,
)


class PostgresProjectMemoryRepository:
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        policy: MemoryDeclarationAuthorityPolicy,
    ) -> None:
        self._session_factory = session_factory
        self._policy = policy

    async def apply_source_invalidation(self, *, evidence_event_id: str) -> int:
        """Append applicability changes; immutable entries/Cycles are never rewritten."""
        async with self._session_factory() as session, session.begin():
            authority = await session.scalar(
                select(EvidenceAuthorityEventRow).where(
                    EvidenceAuthorityEventRow.event_id == evidence_event_id,
                    EvidenceAuthorityEventRow.event_kind.in_(("REVOKED", "SUPERSEDED", "EXPIRED")),
                )
            )
            if authority is None:
                raise ProjectMemoryError(
                    ProjectMemoryErrorCode.SUPERSESSION_AUTHORITY_REQUIRED,
                    "caller invalidation intent is not source-owner authority",
                )
            entries = tuple(
                await session.scalars(
                    select(ProjectMemoryEntryRow).where(
                        ProjectMemoryEntryRow.source_ref == authority.subject_ref
                    )
                )
            )
            changed = 0
            for entry in sorted(entries, key=lambda item: item.memory_lineage_key):
                await session.execute(
                    text("SELECT pg_advisory_xact_lock(hashtextextended(:key, 0))"),
                    {"key": f"p1-8-memory-lineage:{entry.memory_lineage_key}"},
                )
                view = await session.get(
                    ProjectMemoryViewRow, entry.memory_lineage_key, with_for_update=True
                )
                if view is None:
                    raise ProjectMemoryError(
                        ProjectMemoryErrorCode.PROJECTION_CORRUPT,
                        "authority entry lacks projection",
                    )
                if view.current_entry_id != entry.entry_id:
                    continue
                state = MemoryApplicabilityState(authority.event_kind)
                event = ProjectMemoryAuthorityEventRow(
                    event_id="memory-source-event-"
                    + canonical_hash([evidence_event_id, entry.entry_id]),
                    memory_lineage_key=entry.memory_lineage_key,
                    subject_entry_id=entry.entry_id,
                    replacement_entry_id="NONE",
                    event_kind=state.value,
                    prior_revision=view.authority_revision,
                    new_revision=view.authority_revision + 1,
                    authority_ref=evidence_event_id,
                    reason=f"SOURCE_{state.value}",
                    payload={"source_subject_ref": authority.subject_ref},
                    created_at=authority.created_at,
                )
                session.add(event)
                await session.flush()
                view.current_entry_id = None
                view.state = state.value
                view.reason = event.reason
                view.authority_revision = event.new_revision
                view.latest_event_sequence = event.event_sequence
                view.updated_at = authority.created_at
                changed += 1
            return changed

    async def retrieve(
        self,
        *,
        project_id: str,
        categories: frozenset[MemoryCategory] | None = None,
        lineage_key: str | None = None,
        semantic_slot: str | None = None,
        current_only: bool = True,
        authorize_historical: bool = False,
        as_of_event_sequence: int | None = None,
        privacy_clearance: PrivacyClassification = PrivacyClassification.INTERNAL,
        limit: int = 100,
    ) -> tuple[RetrievedMemory, ...]:
        if not 1 <= limit <= 500:
            raise ValueError("memory retrieval limit must be in 1..500")
        if not current_only and not authorize_historical:
            raise ProjectMemoryError(
                ProjectMemoryErrorCode.PRIVACY_DENIED,
                "historical retrieval requires explicit authority",
            )
        async with self._session_factory() as session:
            rows = tuple(
                await session.scalars(
                    select(ProjectMemoryEntryRow)
                    .where(ProjectMemoryEntryRow.project_id == project_id)
                    .order_by(ProjectMemoryEntryRow.entry_id)
                )
            )
            admitted = {
                row.cycle_id: row
                for row in tuple(
                    await session.scalars(
                        select(AdmittedCycleRow).where(AdmittedCycleRow.project_id == project_id)
                    )
                )
            }
            result: list[tuple[tuple[object, ...], RetrievedMemory]] = []
            for row in rows:
                category = MemoryCategory(row.category)
                if categories is not None and category not in categories:
                    continue
                if lineage_key is not None and row.memory_lineage_key != lineage_key:
                    continue
                if semantic_slot is not None and row.payload.get("semantic_slot") != semantic_slot:
                    continue
                privacy = PrivacyClassification(row.privacy)
                if not _privacy_allows(privacy_clearance, privacy):
                    continue
                state, reason, event_sequence = await _state_as_of(
                    session, row, as_of_event_sequence
                )
                if current_only and state is not MemoryApplicabilityState.CURRENT:
                    continue
                cycle = admitted.get(row.cycle_id)
                if cycle is None:
                    raise ProjectMemoryError(
                        ProjectMemoryErrorCode.PROJECTION_CORRUPT,
                        "memory entry Cycle is absent",
                    )
                entry = _entry_from_row(row, cycle)
                marker = (
                    "CURRENT_CONTEXT"
                    if state is MemoryApplicabilityState.CURRENT
                    else "NOT_CURRENT_CONTEXT"
                )
                specificity = _scope_specificity(str(row.payload["applicability_key"]))
                order = (
                    specificity,
                    self._policy.category_priority[category],
                    -event_sequence,
                    -cycle.admission_sequence,
                    row.memory_lineage_key,
                    row.declaration_ordinal,
                    row.entry_id,
                )
                result.append((order, RetrievedMemory(entry, state, reason, marker)))
            return tuple(item[1] for item in sorted(result, key=lambda item: item[0])[:limit])

    async def rebuild_projection(self, project_id: str) -> tuple[str, ...]:
        """Validate event continuity and rebuild byte-equivalent deterministic tips."""
        async with self._session_factory() as session, session.begin():
            entries = tuple(
                await session.scalars(
                    select(ProjectMemoryEntryRow)
                    .where(ProjectMemoryEntryRow.project_id == project_id)
                    .order_by(
                        ProjectMemoryEntryRow.memory_lineage_key, ProjectMemoryEntryRow.entry_id
                    )
                )
            )
            lineages = sorted({entry.memory_lineage_key for entry in entries})
            current_refs: list[str] = []
            for lineage in lineages:
                events = tuple(
                    await session.scalars(
                        select(ProjectMemoryAuthorityEventRow)
                        .where(ProjectMemoryAuthorityEventRow.memory_lineage_key == lineage)
                        .order_by(ProjectMemoryAuthorityEventRow.event_sequence)
                    )
                )
                revision = 0
                current: str | None = None
                state = MemoryApplicabilityState.REVOKED
                reason = "NO_EVENT"
                latest = 0
                updated_at: datetime | None = None
                for event in events:
                    if event.prior_revision != revision or event.new_revision != revision + 1:
                        raise ProjectMemoryError(
                            ProjectMemoryErrorCode.PROJECTION_CORRUPT,
                            "memory authority event gap or duplicate",
                        )
                    revision = event.new_revision
                    state = MemoryApplicabilityState(event.event_kind)
                    if state is MemoryApplicabilityState.CURRENT:
                        if current is not None and current != event.subject_entry_id:
                            raise ProjectMemoryError(
                                ProjectMemoryErrorCode.MULTIPLE_CURRENT_TIPS,
                                "lineage contains multiple CURRENT tips",
                            )
                        current = event.subject_entry_id
                    else:
                        if current is not None and current != event.subject_entry_id:
                            raise ProjectMemoryError(
                                ProjectMemoryErrorCode.PROJECTION_CORRUPT,
                                "applicability event does not address current tip",
                            )
                        current = None
                    reason = event.reason
                    latest = event.event_sequence
                    updated_at = event.created_at
                if not events or updated_at is None:
                    raise ProjectMemoryError(
                        ProjectMemoryErrorCode.PROJECTION_CORRUPT, "lineage has no authority events"
                    )
                projection = await session.get(ProjectMemoryViewRow, lineage)
                if projection is None:
                    projection = ProjectMemoryViewRow(
                        memory_lineage_key=lineage,
                        project_id=project_id,
                        current_entry_id=current,
                        state=state.value,
                        reason=reason,
                        authority_revision=revision,
                        latest_event_sequence=latest,
                        updated_at=updated_at,
                    )
                    session.add(projection)
                else:
                    projection.current_entry_id = current
                    projection.state = state.value
                    projection.reason = reason
                    projection.authority_revision = revision
                    projection.latest_event_sequence = latest
                    projection.updated_at = updated_at
                if current is not None:
                    current_refs.append(current)
            return tuple(current_refs)


async def _state_as_of(
    session: AsyncSession,
    entry: ProjectMemoryEntryRow,
    as_of: int | None,
) -> tuple[MemoryApplicabilityState, str, int]:
    query = (
        select(ProjectMemoryAuthorityEventRow)
        .where(
            ProjectMemoryAuthorityEventRow.memory_lineage_key == entry.memory_lineage_key,
            ProjectMemoryAuthorityEventRow.subject_entry_id == entry.entry_id,
        )
        .order_by(ProjectMemoryAuthorityEventRow.event_sequence.desc())
        .limit(1)
    )
    if as_of is not None:
        query = query.where(ProjectMemoryAuthorityEventRow.event_sequence <= as_of)
    event = await session.scalar(query)
    if event is None:
        raise ProjectMemoryError(
            ProjectMemoryErrorCode.PROJECTION_CORRUPT, "entry has no applicability event"
        )
    return MemoryApplicabilityState(event.event_kind), event.reason, event.event_sequence


def _entry_from_row(row: ProjectMemoryEntryRow, cycle: AdmittedCycleRow) -> ProjectMemoryEntry:
    category = MemoryCategory(row.category)
    mode = MemoryAuthorityMode(str(row.payload["authority_mode"]))
    expected_lineage = memory_lineage_key(
        project_id=row.project_id,
        category=category,
        subject_key=str(row.payload["subject_key"]),
        applicability_key=str(row.payload["applicability_key"]),
        semantic_slot=str(row.payload["semantic_slot"]),
    )
    expected_content = memory_content_fingerprint(
        category=category,
        authority_mode=mode,
        policy_ref=row.policy_ref,
        normalized_derived_content=row.payload["normalized_content"],
    )
    if expected_lineage != row.memory_lineage_key or expected_content != row.content_fingerprint:
        raise ProjectMemoryError(
            ProjectMemoryErrorCode.PROJECTION_CORRUPT,
            "memory lineage/content fingerprint differs from immutable payload",
        )
    return ProjectMemoryEntry(
        row.entry_id,
        row.memory_lineage_key,
        row.project_id,
        cycle.serialized_ref,
        row.declaration_ordinal,
        category,
        str(row.payload["subject_key"]),
        str(row.payload["applicability_key"]),
        str(row.payload["semantic_slot"]),
        mode,
        row.policy_ref,
        row.policy_fingerprint,
        row.source_ref,
        row.content_fingerprint,
        row.payload["normalized_content"],
        PrivacyClassification(row.privacy),
        row.created_at.astimezone(UTC),
    )


def _privacy_allows(clearance: PrivacyClassification, value: PrivacyClassification) -> bool:
    ranks = {
        PrivacyClassification.PUBLIC_SANITIZED: 0,
        PrivacyClassification.INTERNAL: 1,
        PrivacyClassification.NON_EXPORTABLE: 2,
    }
    return ranks[clearance] >= ranks[value]


def _scope_specificity(value: str) -> int:
    if value.startswith("task-contract:"):
        return 0
    if value.startswith("task:"):
        return 1
    return 2
