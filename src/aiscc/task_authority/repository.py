from __future__ import annotations

from datetime import UTC, datetime
from typing import NoReturn, cast

from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from aiscc.contracts.canonical_json import MAX_SAFE_INTEGER, canonical_sha256
from aiscc.persistence.models import (
    ExternalTaskAuthorityCounterRow,
    ExternalTaskAuthorityEventRegistryRow,
    ExternalTaskAuthorityIssuerBindingRow,
    NextActionContextAuthorityEventRow,
    NextActionContextCurrentRow,
    NextActionContextRefRow,
    TaskConstraintAuthorityEventRow,
    TaskConstraintCurrentRow,
    TaskConstraintOwnerSnapshotRow,
    TaskConstraintRefRow,
    TaskContractBodyRow,
)
from aiscc.task_authority.contracts import (
    SCHEMA,
    SUPPORTED_ACTION_ID,
    UNSUPPORTED_SOURCE,
    IssuedTaskContractV1,
    TaskContractBodyV1,
    TaskContractError,
    VerifiedTaskContractBindingV1,
    action_claim,
    candidate_fingerprint,
    plain,
)
from aiscc.task_authority.models import (
    AUTHORITY_REVISION,
    EXTERNAL_TASK_AUTHORITY_OWNER,
    NEXT_ACTION_CONTEXT_AUTHORITY_REF,
    NEXT_ACTION_CONTEXT_AUTHORITY_VERSION,
    NEXT_ACTION_CONTEXT_RESULT_SCHEMA_FINGERPRINT,
    TASK_CONSTRAINT_AUTHORITY_REF,
    TASK_CONSTRAINT_AUTHORITY_VERSION,
    AuthorityEventKind,
    CurrentProjectionDisposition,
    ExternalTaskAuthorityError,
    ExternalTaskAuthorityErrorCode,
    NextActionContextAuthorityEventV1,
    NextActionContextFoldResult,
    NextActionContextRefV1,
    NextActionPriorityClass,
    TaskConstraintAuthorityEventV1,
    TaskConstraintFoldResult,
    TaskConstraintOwnerSnapshotV1,
    TaskConstraintRefV1,
    TaskConstraintScopeKind,
    TaskConstraintScopeV1,
    next_action_context_ref_from_payload,
    ordered_event_prefix_root,
    task_constraint_ref_from_payload,
)

_COUNTER_ID = "external-command-center-task-authority-v1"
_ISSUER_BINDING_REF = "external-task-authority-issuer-binding:v1:command-center"
_ISSUER_BINDING_PAYLOAD: dict[str, object] = {
    "authority_owner": EXTERNAL_TASK_AUTHORITY_OWNER,
    "authority_revision": AUTHORITY_REVISION,
    "authority_version": "AISCC-EXTERNAL-COMMAND-CENTER-TASK-AUTHORITY-V1",
    "binding_ref": _ISSUER_BINDING_REF,
}
_ISSUER_BINDING_FINGERPRINT = canonical_sha256(_ISSUER_BINDING_PAYLOAD)


class PostgresExternalTaskAuthorityRepository:
    """Durable read/verifier implementation with capability-gated private writes."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory
        self.__writer_capability: object | None = None
        self.__contract_composition = None

    def _bind_writer_capability(self, capability: object) -> None:
        if self.__writer_capability is not None or capability is None:
            raise ExternalTaskAuthorityError(
                ExternalTaskAuthorityErrorCode.CAPABILITY_DENIED,
                "repository writer capability is already bound",
            )
        self.__writer_capability = capability

    def _require_capability(self, capability: object) -> None:
        if self.__writer_capability is None or capability is not self.__writer_capability:
            raise ExternalTaskAuthorityError(
                ExternalTaskAuthorityErrorCode.CAPABILITY_DENIED,
                "external Task-authority writer capability denied",
            )

    def _configure_task_contracts(
        self,
        capability,
        *,
        project_id,
        repository_binding,
        next_action_repository,
        evidence_repository,
        required_authority_refs=(),
        human_roles_by_selector=None,
    ):
        from pathlib import Path
        from types import MappingProxyType

        from aiscc.evidence.repository import PostgresEvidenceRepository
        from aiscc.next_action.repository import PostgresNextActionRepository

        self._require_capability(capability)
        if self.__contract_composition is not None:
            raise TaskContractError("TaskContract composition already bound")
        if not isinstance(next_action_repository, PostgresNextActionRepository) or not isinstance(
            evidence_repository, PostgresEvidenceRepository
        ):
            raise TaskContractError("existing concrete owners required")
        if set(repository_binding) != {"repository_id", "repository_root", "base_commit"}:
            raise TaskContractError("repository enrollment differs")
        if not Path(repository_binding["repository_root"]).is_absolute():
            raise TaskContractError("absolute server-enrolled root required")
        self.__contract_composition = (
            project_id,
            MappingProxyType(dict(repository_binding)),
            next_action_repository,
            evidence_repository,
            tuple(required_authority_refs),
            MappingProxyType(
                {
                    k: frozenset(v)
                    for k, v in (
                        human_roles_by_selector
                        or {
                            "reviewers-v1": frozenset({"reviewer"}),
                            "reviewers-v2": frozenset({"reviewer"}),
                        }
                    ).items()
                }
            ),
        )

    def _contract_composition(self):
        if self.__contract_composition is None:
            raise TaskContractError("TaskContract composition not enrolled")
        return self.__contract_composition

    async def _contract_family(self, session, project_id, contract_id):
        await _lock(session, "task-contract-family:" + canonical_sha256([project_id, contract_id]))
        rows = tuple(
            await session.scalars(
                select(TaskContractBodyRow)
                .where(
                    TaskContractBodyRow.project_id == project_id,
                    TaskContractBodyRow.contract_id == contract_id,
                )
                .order_by(TaskContractBodyRow.contract_version)
                .execution_options(populate_existing=True)
            )
        )
        previous = None
        for index, row in enumerate(rows, 1):
            body = TaskContractBodyV1.from_bytes(bytes(row.canonical_body))
            v = body.value
            expected_predecessor = (
                None
                if previous is None
                else {"contract_version": index - 1, "body_sha256": previous.body_sha256}
            )
            if (
                row.contract_version != index
                or v["contract_version"] != index
                or v["project_id"] != project_id
                or v["contract_id"] != contract_id
                or v["task_id"] != row.task_id
                or body.body_ref != row.body_ref
                or body.body_sha256 != row.body_sha256
                or row.body_schema_id != SCHEMA
                or plain(v["predecessor"]) != expected_predecessor
                or row.predecessor_version != (index - 1 if index > 1 else None)
                or row.predecessor_sha256 != (previous.body_sha256 if previous else None)
                or (previous and v["task_id"] != previous.value["task_id"])
            ):
                raise TaskContractError("AUTHORITY_CORRUPTION: body family projection")
            previous = body
        return rows

    async def _contract_constraint_locks(self, session, rows, additional_refs=()):
        keys = set()
        for ref in [*(r.constraint_ref for r in rows), *(r[0] for r in additional_refs)]:
            row = await session.get(TaskConstraintRefRow, ref)
            if row is None:
                raise TaskContractError("AUTHORITY_CORRUPTION: constraint absent")
            keys.add(_constraint_from_row(row).logical_key)
        for key in sorted(keys):
            await _lock(session, f"external-task-authority:constraint:{key}")

    async def _contract_row_receipt(self, session, row):
        body = TaskContractBodyV1.from_bytes(bytes(row.canonical_body))
        refrow = await session.get(TaskConstraintRefRow, row.constraint_ref)
        eventrow = await session.get(TaskConstraintAuthorityEventRow, row.issuance_event_ref)
        if refrow is None or eventrow is None:
            raise TaskContractError("AUTHORITY_CORRUPTION: body envelope absent")
        ref, event = _constraint_from_row(refrow), _constraint_event_from_row(eventrow)
        v = body.value
        if (
            ref.constraint_payload_ref != body.body_ref
            or ref.constraint_payload_fingerprint != body.body_sha256
            or ref.constraint_schema_id != SCHEMA
            or ref.constraint_schema_version != "v1"
            or ref.scope
            != TaskConstraintScopeV1(
                TaskConstraintScopeKind.TASK_CONTRACT,
                v["project_id"],
                v["contract_id"],
                "v" + str(v["contract_version"]),
            )
            or ref.logical_constraint_id
            != "tc-body-" + canonical_sha256([v["project_id"], v["contract_id"]])
            or ref.constraint_ref_id != "tc-body-" + body.body_sha256
            or event.event_kind is not AuthorityEventKind.ISSUED
            or event.constraint_ref != ref.constraint_ref
            or event.constraint_fingerprint != ref.constraint_fingerprint
            or event.event_id != "tc-issued-" + body.body_sha256
            or ref.issued_at != row.issued_at
            or event.effective_at != row.issued_at
        ):
            raise TaskContractError("AUTHORITY_CORRUPTION: body/ref/event binding")
        snapshot_row = await session.get(
            TaskConstraintOwnerSnapshotRow,
            "task-constraint-owner-snapshot:v1:tc-issued-" + body.body_sha256,
        )
        if snapshot_row is None:
            raise TaskContractError("AUTHORITY_CORRUPTION: original body snapshot absent")
        snapshot = await _verify_snapshot(session, snapshot_row)
        await self.verify_task_constraint(
            constraint_ref=ref.constraint_ref,
            constraint_fingerprint=ref.constraint_fingerprint,
            snapshot_ref=snapshot.snapshot_ref,
            snapshot_fingerprint=snapshot.snapshot_fingerprint,
            owner_event_high_watermark=snapshot.owner_event_high_watermark,
            require_current=False,
            session=session,
        )
        return IssuedTaskContractV1(
            body,
            ref.constraint_ref,
            ref.constraint_fingerprint,
            event.event_ref,
            snapshot.snapshot_ref,
            snapshot.snapshot_fingerprint,
            snapshot.owner_event_high_watermark,
        )

    async def _verify_contract_current_projection(self, session, rows):
        latest = await self.latest_snapshot(session=session)
        await _require_latest_snapshot(session, latest)
        current = False
        for index, row in enumerate(rows):
            receipt = await self._contract_row_receipt(session, row)
            refrow = await session.get(TaskConstraintRefRow, receipt.constraint_ref)
            ref = _constraint_from_row(refrow)
            fold = await self.verify_task_constraint(
                constraint_ref=ref.constraint_ref,
                constraint_fingerprint=ref.constraint_fingerprint,
                snapshot_ref=latest.snapshot_ref,
                snapshot_fingerprint=latest.snapshot_fingerprint,
                owner_event_high_watermark=latest.owner_event_high_watermark,
                require_current=False,
                session=session,
            )
            events = await _constraint_events(
                session, ref.logical_key, latest.owner_event_high_watermark
            )
            projection = await session.get(
                TaskConstraintCurrentRow, ref.logical_key, populate_existing=True
            )
            current = fold.current is not None and fold.current.constraint_ref == ref.constraint_ref
            if (
                projection is None
                or projection.current_constraint_ref != (ref.constraint_ref if current else None)
                or projection.terminal_revoked != ("false" if current else "true")
                or projection.effective_sequence != events[-1].effective_sequence
                or projection.latest_event_sequence != events[-1].event_sequence
                or projection.updated_at != events[-1].effective_at
                or (index < len(rows) - 1 and current)
            ):
                raise TaskContractError("AUTHORITY_CORRUPTION: contract current projection")
        return current

    async def _verify_contract_inputs(self, session, body):
        from pathlib import Path

        from aiscc.evidence.models import EvidenceCheckpointRef, EvidenceRequirementProfile
        from aiscc.next_action.models import (
            NextActionError,
            NextActionErrorCode,
            NextActionSelectionMode,
        )

        project, repository, next_actions, evidence, required_refs, selectors = (
            self._contract_composition()
        )
        v = body.value
        if v["project_id"] != project or plain(v["repository_binding"]) != dict(repository):
            raise TaskContractError("repository/project/base binding differs")
        # Resolve only exact enrolled scope paths; never discover a repository/root.
        root = Path(repository["repository_root"]).resolve()
        for path in (*v["allowed_paths"], *v["forbidden_paths"]):
            target = root / (path[:-3] if path.endswith("/**") else path)
            if not target.resolve().is_relative_to(root):
                raise TaskContractError("scope symlink/reparse escape")
        source = v["source_next_action"]
        action = action_claim(source["action_ref"])
        if action.action_id != SUPPORTED_ACTION_ID:
            raise TaskContractError(UNSUPPORTED_SOURCE)
        try:
            selected, candidate, descriptor = await next_actions.verify_current_selection(
                session,
                selection_id=source["selection_id"],
                expected_project_id=project,
                expected_project_revision=source["project_revision"],
                expected_selection_fingerprint=source["selection_fingerprint"],
                expected_action_ref=action,
                expected_descriptor_fingerprint=source["descriptor_fingerprint"],
                allowed_selection_modes=frozenset({NextActionSelectionMode.CYCLE_DERIVED}),
            )
        except NextActionError as exc:
            if exc.code is NextActionErrorCode.NOT_SUPPORTED:
                raise TaskContractError(UNSUPPORTED_SOURCE) from exc
            raise
        if (
            selected.selection_version != source["selection_version"]
            or candidate.candidate_id != source["issuance_candidate_id"]
            or candidate_fingerprint(candidate) != source["issuance_candidate_fingerprint"]
            or descriptor.task_issuance_owner != "EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY"
        ):
            raise TaskContractError("source candidate/descriptor differs")
        context = source["external_context"]
        if context is None or (
            context["context_ref"],
            context["context_fingerprint"],
            context["snapshot_ref"],
            context["snapshot_fingerprint"],
            context["owner_event_high_watermark"],
        ) != (
            selected.external_context_ref,
            selected.external_context_fingerprint,
            selected.external_context_snapshot_ref,
            selected.external_context_snapshot_fingerprint,
            selected.external_context_event_high_watermark,
        ):
            raise TaskContractError("source context differs")
        await self.verify_next_action_context(
            **plain(context), require_current=False, session=session
        )
        supplied = tuple((x["ref"], x["fingerprint"]) for x in v["authority_refs"])
        if supplied != required_refs:
            raise TaskContractError("required independent authority set differs")
        latest = await self.latest_snapshot(session=session)
        for ref, fp in supplied:
            row = await session.get(TaskConstraintRefRow, ref)
            value = _constraint_from_row(row) if row else None
            if (
                value is None
                or value.constraint_payload_ref == body.body_ref
                or value.scope.project_id != project
                or value.scope.scope_kind is TaskConstraintScopeKind.WORK_RUN
                or (
                    value.scope.scope_kind is TaskConstraintScopeKind.TASK_CONTRACT
                    and (
                        value.scope.task_contract_id != v["contract_id"]
                        or value.scope.task_contract_version != "v" + str(v["contract_version"])
                    )
                )
            ):
                raise TaskContractError("independent authority scope/self-reference")
            await self.verify_task_constraint(
                constraint_ref=ref,
                constraint_fingerprint=fp,
                snapshot_ref=latest.snapshot_ref,
                snapshot_fingerprint=latest.snapshot_fingerprint,
                owner_event_high_watermark=latest.owner_event_high_watermark,
                require_current=True,
                session=session,
            )
        eb = v["evidence_binding"]
        checkpoints = []
        for item in eb["checkpoints"]:
            # Owner reference serialization is validated against owner-returned graph below.
            ref_id, version = item["ref"].rsplit("@", 1)
            checkpoints.append((EvidenceCheckpointRef(ref_id, version), item["fingerprint"]))
        result = await evidence.verify_requirement_definition_graph(
            session,
            task_contract_id=v["contract_id"],
            task_contract_version="v" + str(v["contract_version"]),
            requirement_set_ref=eb["requirement_set_ref"],
            expected_requirement_set_fingerprint=eb["requirement_set_fingerprint"],
            expected_checkpoints=tuple(checkpoints),
        )
        if v["human_binding"]["kind"] == "REQUIRED":
            if v["human_binding"]["owner_selector_fingerprint"] not in selectors:
                raise TaskContractError("Human selector not enrolled")
        elif any(req.profile is EvidenceRequirementProfile.HUMAN_OWNED for req in result[1]):
            raise TaskContractError("NOT_REQUIRED conflicts with Human-owned requirement")
        from aiscc.workflow.matrix import TRANSITION_MATRIX

        declared_uses = {
            (p["source_state"], p["target_state"]) for p in v["judgment_binding"]["policies"]
        }
        for cp in result[2]:
            if (
                cp.target_state is not None
                and any(
                    g.value.startswith("G_JUDGMENT_")
                    for g in TRANSITION_MATRIX.get((cp.source_state, cp.target_state), ())
                )
                and (cp.source_state.value, cp.target_state.value) not in declared_uses
            ):
                raise TaskContractError("incomplete Judgment checkpoint-use coverage")
        for policy in v["judgment_binding"]["policies"]:
            cp = next(
                (
                    cp
                    for cp in result[2]
                    if cp.ref.serialized() == policy["evidence_checkpoint_ref"]
                ),
                None,
            )
            if policy["evidence_checkpoint_ref"] is not None and (
                cp is None
                or cp.source_state.value != policy["source_state"]
                or cp.target_state is None
                or cp.target_state.value != policy["target_state"]
            ):
                raise TaskContractError("Judgment checkpoint applicability differs")
        return result

    async def _issue_task_contract(
        self, capability, *, body, expected_current_body_sha256, issued_at
    ):
        self._require_capability(capability)
        if not isinstance(body, TaskContractBodyV1):
            raise TaskContractError("typed immutable body required")
        body = TaskContractBodyV1.from_bytes(body.canonical_body)
        v = body.value
        predecessor = v["predecessor"]
        if expected_current_body_sha256 != (predecessor["body_sha256"] if predecessor else None):
            raise TaskContractError("expected predecessor differs")
        async with self._session_factory() as session, session.begin():
            rows = await self._contract_family(session, v["project_id"], v["contract_id"])
            for row in rows:
                if row.contract_version == v["contract_version"]:
                    if bytes(row.canonical_body) != body.canonical_body:
                        raise TaskContractError("same-version body differs")
                    return await self._contract_row_receipt(session, row)
            if v["contract_version"] != len(rows) + 1 or (
                rows and rows[-1].body_sha256 != expected_current_body_sha256
            ):
                raise TaskContractError("contract version/predecessor differs")
            if rows and rows[-1].task_id != v["task_id"]:
                raise TaskContractError("family Task identity differs")
            _, _, _, _, required_refs, _ = self._contract_composition()
            await self._contract_constraint_locks(session, rows, required_refs)
            # Existing snapshot certification takes its lock before the counter row.
            await _lock(session, "external-task-authority:snapshot")
            await self._verify_contract_inputs(session, body)
            if rows and not await self._verify_contract_current_projection(session, rows):
                raise TaskContractError("latest revoked family cannot issue again")
            expected_ref = "task-constraint:v1:tc-body-" + body.body_sha256
            if await session.get(TaskConstraintRefRow, expected_ref) is not None:
                raise TaskContractError("AUTHORITY_CORRUPTION: orphan body reference")
            if rows:
                await self._revoke_task_constraint(
                    capability,
                    current_constraint_ref=rows[-1].constraint_ref,
                    event_id="tc-replaced-" + body.body_sha256,
                    effective_at=issued_at,
                    session=session,
                )
            ref, event = await self._issue_task_constraint(
                capability,
                constraint_ref_id="tc-body-" + body.body_sha256,
                logical_constraint_id="tc-body-"
                + canonical_sha256([v["project_id"], v["contract_id"]]),
                scope=TaskConstraintScopeV1(
                    TaskConstraintScopeKind.TASK_CONTRACT,
                    v["project_id"],
                    v["contract_id"],
                    "v" + str(v["contract_version"]),
                ),
                constraint_schema_id=SCHEMA,
                constraint_schema_version="v1",
                constraint_payload_ref=body.body_ref,
                constraint_payload_fingerprint=body.body_sha256,
                event_id="tc-issued-" + body.body_sha256,
                issued_at=issued_at,
                session=session,
            )
            await session.flush()
            row = TaskContractBodyRow(
                body_ref=body.body_ref,
                body_schema_id=SCHEMA,
                body_sha256=body.body_sha256,
                project_id=v["project_id"],
                contract_id=v["contract_id"],
                task_id=v["task_id"],
                contract_version=v["contract_version"],
                canonical_body=body.canonical_body,
                constraint_ref=ref.constraint_ref,
                issuance_event_ref=event.event_ref,
                predecessor_version=predecessor["contract_version"] if predecessor else None,
                predecessor_sha256=expected_current_body_sha256,
                issued_at=ref.issued_at,
            )
            session.add(row)
            await session.flush()
            await self._certify_snapshot(
                capability,
                snapshot_id="tc-issued-" + body.body_sha256,
                issued_at=issued_at,
                session=session,
            )
            await session.flush()
            return await self._contract_row_receipt(session, row)

    async def get_task_contract(self, project_id, contract_id, version, *, session=None):
        if session is None:
            async with self._session_factory() as owned, owned.begin():
                return await self.get_task_contract(project_id, contract_id, version, session=owned)
        if not session.in_transaction():
            raise TaskContractError("caller transaction required")
        with session.no_autoflush:
            rows = await self._contract_family(session, project_id, contract_id)
            result = None
            for row in rows:
                receipt = await self._contract_row_receipt(session, row)
                if row.contract_version == version:
                    result = receipt
            return result

    async def verify_task_contract(
        self,
        binding,
        *,
        require_current,
        expected_repository_binding,
        expected_next_action_ref,
        session=None,
    ):
        if session is None:
            async with self._session_factory() as owned, owned.begin():
                return await self.verify_task_contract(
                    binding,
                    require_current=require_current,
                    expected_repository_binding=expected_repository_binding,
                    expected_next_action_ref=expected_next_action_ref,
                    session=owned,
                )
        if not session.in_transaction() or not isinstance(binding, IssuedTaskContractV1):
            raise TaskContractError("caller transaction and issued value required")
        with session.no_autoflush:
            body = TaskContractBodyV1.from_bytes(binding.body.canonical_body)
            v = body.value
            if (
                plain(v["repository_binding"]) != dict(expected_repository_binding)
                or v["source_next_action"]["action_ref"] != expected_next_action_ref
            ):
                raise TaskContractError("expected repository/action differs")
            rows = await self._contract_family(session, v["project_id"], v["contract_id"])
            row = next((r for r in rows if r.contract_version == v["contract_version"]), None)
            if row is None or await self._contract_row_receipt(session, row) != binding:
                raise TaskContractError("AUTHORITY_CORRUPTION: issued receipt differs")
            # Verify every predecessor's original immutable authority chain.
            for other in rows:
                await self._contract_row_receipt(session, other)
            if require_current:
                _, _, _, _, required_refs, _ = self._contract_composition()
                await self._contract_constraint_locks(session, rows, required_refs)
                await self._verify_contract_inputs(session, body)
                if rows[
                    -1
                ].body_ref != body.body_ref or not await self._verify_contract_current_projection(
                    session, rows
                ):
                    raise TaskContractError("TaskContract not current")
            return VerifiedTaskContractBindingV1(binding, require_current)

    async def _revoke_task_contract(
        self,
        capability,
        *,
        project_id,
        contract_id,
        expected_version,
        expected_body_sha256,
        effective_at,
    ):
        self._require_capability(capability)
        async with self._session_factory() as session, session.begin():
            rows = await self._contract_family(session, project_id, contract_id)
            if (
                not rows
                or rows[-1].contract_version != expected_version
                or rows[-1].body_sha256 != expected_body_sha256
            ):
                raise TaskContractError("revoke exact latest body differs")
            await self._contract_constraint_locks(session, rows)
            await _lock(session, "external-task-authority:snapshot")
            await _lock(session, "external-task-authority:global-sequence")
            receipt = await self._contract_row_receipt(session, rows[-1])
            event_id = "tc-revoked-" + expected_body_sha256
            existing = await session.get(
                TaskConstraintAuthorityEventRow, "task-constraint-event:v1:" + event_id
            )
            if existing is not None:
                event = _constraint_event_from_row(existing)
                if event.constraint_ref != receipt.constraint_ref:
                    raise TaskContractError("revoke replay differs")
                return event
            if not await self._verify_contract_current_projection(session, rows):
                raise TaskContractError("latest body not current")
            event = await self._revoke_task_constraint(
                capability,
                current_constraint_ref=receipt.constraint_ref,
                event_id=event_id,
                effective_at=effective_at,
                session=session,
            )
            await session.flush()
            await self._certify_snapshot(
                capability, snapshot_id=event_id, issued_at=effective_at, session=session
            )
            return event

    async def _issue_task_constraint(
        self,
        capability: object,
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
        session: AsyncSession | None = None,
    ) -> tuple[TaskConstraintRefV1, TaskConstraintAuthorityEventV1]:
        self._require_capability(capability)
        constraint_ref = f"task-constraint:v1:{constraint_ref_id}"
        event_ref = f"task-constraint-event:v1:{event_id}"
        if session is None:
            async with self._session_factory() as owned_session, owned_session.begin():
                return await self._issue_task_constraint(
                    capability,
                    constraint_ref_id=constraint_ref_id,
                    logical_constraint_id=logical_constraint_id,
                    scope=scope,
                    constraint_schema_id=constraint_schema_id,
                    constraint_schema_version=constraint_schema_version,
                    constraint_payload_ref=constraint_payload_ref,
                    constraint_payload_fingerprint=constraint_payload_fingerprint,
                    event_id=event_id,
                    issued_at=issued_at,
                    session=owned_session,
                )
        if not session.in_transaction():
            _authority_conflict("caller transaction required")
        await _lock(session, f"external-task-authority:constraint:{logical_constraint_id}")
        existing = await session.get(TaskConstraintRefRow, constraint_ref)
        if existing is not None:
            event_row = await session.get(TaskConstraintAuthorityEventRow, event_ref)
            value = _constraint_from_row(existing)
            if (
                event_row is None
                or value.logical_constraint_id != logical_constraint_id
                or value.scope != scope
                or value.constraint_schema_id != constraint_schema_id
                or value.constraint_schema_version != constraint_schema_version
                or value.constraint_payload_ref != constraint_payload_ref
                or value.constraint_payload_fingerprint != constraint_payload_fingerprint
            ):
                _identity_conflict("TaskConstraint issue replay differs")
            return value, _constraint_event_from_row(event_row)
        logical_key = canonical_sha256(
            {"logical_constraint_id": logical_constraint_id, "scope": scope.payload()}
        )
        projection = await session.get(TaskConstraintCurrentRow, logical_key, with_for_update=True)
        if projection is not None:
            _authority_conflict("TaskConstraint logical key already has an origin")
        object_sequence, event_sequence = await self._reserve_sequences(
            session, object_count=1, event_count=1
        )
        value = _new_constraint(
            constraint_ref_id=constraint_ref_id,
            logical_constraint_id=logical_constraint_id,
            scope=scope,
            constraint_schema_id=constraint_schema_id,
            constraint_schema_version=constraint_schema_version,
            constraint_payload_ref=constraint_payload_ref,
            constraint_payload_fingerprint=constraint_payload_fingerprint,
            issued_at=issued_at,
            issuance_sequence=object_sequence,
        )
        event = _new_constraint_event(
            event_id=event_id,
            event_kind=AuthorityEventKind.ISSUED,
            target=value,
            replacement=None,
            event_sequence=event_sequence,
            effective_sequence=1,
            effective_at=issued_at,
        )
        await self._ensure_issuer_binding(session, issued_at)
        session.add(_constraint_row(value))
        session.add(
            _registry_row(
                event_sequence,
                event.event_ref,
                event.event_fingerprint,
                "TASK_CONSTRAINT",
                issued_at,
            )
        )
        session.add(_constraint_event_row(event, logical_key))
        session.add(
            TaskConstraintCurrentRow(
                logical_key=logical_key,
                current_constraint_ref=value.constraint_ref,
                terminal_revoked="false",
                effective_sequence=1,
                latest_event_sequence=event_sequence,
                updated_at=issued_at,
            )
        )
        return value, event

    async def _supersede_task_constraint(
        self,
        capability: object,
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
        self._require_capability(capability)
        async with self._session_factory() as session, session.begin():
            current_row = await session.get(TaskConstraintRefRow, current_constraint_ref)
            if current_row is None:
                _authority_conflict("TaskConstraint current ref is absent")
            current = _constraint_from_row(current_row)
            await _lock(session, f"external-task-authority:constraint:{current.logical_key}")
            projection = await session.get(
                TaskConstraintCurrentRow, current.logical_key, with_for_update=True
            )
            if (
                projection is None
                or projection.current_constraint_ref != current.constraint_ref
                or projection.terminal_revoked == "true"
            ):
                _authority_conflict("TaskConstraint supersede target is not exact current")
            replacement_ref = f"task-constraint:v1:{replacement_ref_id}"
            event_ref = f"task-constraint-event:v1:{event_id}"
            existing = await session.get(TaskConstraintRefRow, replacement_ref)
            existing_event = await session.get(TaskConstraintAuthorityEventRow, event_ref)
            if existing is not None or existing_event is not None:
                if existing is None or existing_event is None:
                    _identity_conflict("partial TaskConstraint supersede replay")
                return _constraint_from_row(existing), _constraint_event_from_row(existing_event)
            object_sequence, event_sequence = await self._reserve_sequences(
                session, object_count=1, event_count=1
            )
            replacement = _new_constraint(
                constraint_ref_id=replacement_ref_id,
                logical_constraint_id=current.logical_constraint_id,
                scope=current.scope,
                constraint_schema_id=constraint_schema_id,
                constraint_schema_version=constraint_schema_version,
                constraint_payload_ref=constraint_payload_ref,
                constraint_payload_fingerprint=constraint_payload_fingerprint,
                issued_at=effective_at,
                issuance_sequence=object_sequence,
            )
            effective_sequence = projection.effective_sequence + 1
            event = _new_constraint_event(
                event_id=event_id,
                event_kind=AuthorityEventKind.SUPERSEDED,
                target=current,
                replacement=replacement,
                event_sequence=event_sequence,
                effective_sequence=effective_sequence,
                effective_at=effective_at,
            )
            session.add(_constraint_row(replacement))
            session.add(
                _registry_row(
                    event_sequence,
                    event.event_ref,
                    event.event_fingerprint,
                    "TASK_CONSTRAINT",
                    effective_at,
                )
            )
            session.add(_constraint_event_row(event, current.logical_key))
            projection.current_constraint_ref = replacement.constraint_ref
            projection.effective_sequence = effective_sequence
            projection.latest_event_sequence = event_sequence
            projection.updated_at = effective_at
            return replacement, event

    async def _revoke_task_constraint(
        self,
        capability: object,
        *,
        current_constraint_ref: str,
        event_id: str,
        effective_at: datetime,
        session: AsyncSession | None = None,
    ) -> TaskConstraintAuthorityEventV1:
        self._require_capability(capability)
        if session is None:
            async with self._session_factory() as owned_session, owned_session.begin():
                return await self._revoke_task_constraint(
                    capability,
                    current_constraint_ref=current_constraint_ref,
                    event_id=event_id,
                    effective_at=effective_at,
                    session=owned_session,
                )
        if not session.in_transaction():
            _authority_conflict("caller transaction required")
        current_row = await session.get(TaskConstraintRefRow, current_constraint_ref)
        if current_row is None:
            _authority_conflict("TaskConstraint revoke target is absent")
        current = _constraint_from_row(current_row)
        await _lock(session, f"external-task-authority:constraint:{current.logical_key}")
        event_ref = f"task-constraint-event:v1:{event_id}"
        existing = await session.get(TaskConstraintAuthorityEventRow, event_ref)
        if existing is not None:
            event = _constraint_event_from_row(existing)
            if event.constraint_ref != current_constraint_ref:
                _identity_conflict("TaskConstraint revoke replay differs")
            return event
        projection = await session.get(
            TaskConstraintCurrentRow, current.logical_key, with_for_update=True
        )
        if (
            projection is None
            or projection.current_constraint_ref != current.constraint_ref
            or projection.terminal_revoked == "true"
        ):
            _authority_conflict("TaskConstraint revoke target is not exact current")
        _, event_sequence = await self._reserve_sequences(session, object_count=0, event_count=1)
        effective_sequence = projection.effective_sequence + 1
        event = _new_constraint_event(
            event_id=event_id,
            event_kind=AuthorityEventKind.REVOKED,
            target=current,
            replacement=None,
            event_sequence=event_sequence,
            effective_sequence=effective_sequence,
            effective_at=effective_at,
        )
        session.add(
            _registry_row(
                event_sequence,
                event.event_ref,
                event.event_fingerprint,
                "TASK_CONSTRAINT",
                effective_at,
            )
        )
        session.add(_constraint_event_row(event, current.logical_key))
        projection.current_constraint_ref = None
        projection.terminal_revoked = "true"
        projection.effective_sequence = effective_sequence
        projection.latest_event_sequence = event_sequence
        projection.updated_at = effective_at
        return event

    async def _issue_next_action_context(
        self,
        capability: object,
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
        self._require_capability(capability)
        context_ref = f"next-action-context:v1:{context_ref_id}"
        event_ref = f"next-action-context-event:v1:{event_id}"
        logical_id = f"next-action-context-lineage:v1:{context_logical_local_id}"
        logical_key = _context_logical_key(
            project_id,
            task_contract_id,
            task_contract_version,
            logical_id,
            context_slot_id,
        )
        async with self._session_factory() as session, session.begin():
            await _lock(session, f"external-task-authority:context:{logical_key}")
            existing = await session.get(NextActionContextRefRow, context_ref)
            if existing is not None:
                event_row = await session.get(NextActionContextAuthorityEventRow, event_ref)
                value = _context_from_row(existing)
                if (
                    event_row is None
                    or value.logical_key != logical_key
                    or value.priority_class is not priority_class
                    or value.critical_path_ordinal != critical_path_ordinal
                ):
                    _identity_conflict("NextActionContext issue replay differs")
                return value, _context_event_from_row(event_row)
            if await session.get(NextActionContextCurrentRow, logical_key) is not None:
                _authority_conflict("NextActionContext logical key already has an origin")
            object_sequence, event_sequence = await self._reserve_sequences(
                session, object_count=1, event_count=1
            )
            value = _new_context(
                context_ref_id=context_ref_id,
                context_logical_id=logical_id,
                project_id=project_id,
                task_contract_id=task_contract_id,
                task_contract_version=task_contract_version,
                context_slot_id=context_slot_id,
                priority_class=priority_class,
                critical_path_ordinal=critical_path_ordinal,
                issued_at=issued_at,
                issuance_sequence=object_sequence,
                effective_sequence=1,
            )
            event = _new_context_event(
                event_id=event_id,
                event_kind=AuthorityEventKind.ISSUED,
                target=value,
                replacement=None,
                event_sequence=event_sequence,
                effective_sequence=1,
                effective_at=issued_at,
            )
            await self._ensure_issuer_binding(session, issued_at)
            session.add(_context_row(value))
            session.add(
                _registry_row(
                    event_sequence,
                    event.event_ref,
                    event.event_fingerprint,
                    "NEXT_ACTION_CONTEXT",
                    issued_at,
                )
            )
            session.add(_context_event_row(event, logical_key))
            session.add(
                NextActionContextCurrentRow(
                    logical_key=logical_key,
                    current_context_ref=value.context_ref,
                    terminal_revoked="false",
                    effective_sequence=1,
                    latest_event_sequence=event_sequence,
                    updated_at=issued_at,
                )
            )
            return value, event

    async def _supersede_next_action_context(
        self,
        capability: object,
        *,
        current_context_ref: str,
        replacement_ref_id: str,
        priority_class: NextActionPriorityClass,
        critical_path_ordinal: int,
        event_id: str,
        effective_at: datetime,
    ) -> tuple[NextActionContextRefV1, NextActionContextAuthorityEventV1]:
        self._require_capability(capability)
        async with self._session_factory() as session, session.begin():
            current_row = await session.get(NextActionContextRefRow, current_context_ref)
            if current_row is None:
                _authority_conflict("NextActionContext supersede target is absent")
            current = _context_from_row(current_row)
            await _lock(session, f"external-task-authority:context:{current.logical_key}")
            projection = await session.get(
                NextActionContextCurrentRow, current.logical_key, with_for_update=True
            )
            if (
                projection is None
                or projection.current_context_ref != current.context_ref
                or projection.terminal_revoked == "true"
            ):
                _authority_conflict("NextActionContext supersede target is not exact current")
            replacement_ref = f"next-action-context:v1:{replacement_ref_id}"
            event_ref = f"next-action-context-event:v1:{event_id}"
            existing = await session.get(NextActionContextRefRow, replacement_ref)
            existing_event = await session.get(NextActionContextAuthorityEventRow, event_ref)
            if existing is not None or existing_event is not None:
                if existing is None or existing_event is None:
                    _identity_conflict("partial NextActionContext supersede replay")
                return _context_from_row(existing), _context_event_from_row(existing_event)
            object_sequence, event_sequence = await self._reserve_sequences(
                session, object_count=1, event_count=1
            )
            effective_sequence = projection.effective_sequence + 1
            replacement = _new_context(
                context_ref_id=replacement_ref_id,
                context_logical_id=current.context_logical_id,
                project_id=current.project_id,
                task_contract_id=current.task_contract_id,
                task_contract_version=current.task_contract_version,
                context_slot_id=current.context_slot_id,
                priority_class=priority_class,
                critical_path_ordinal=critical_path_ordinal,
                issued_at=effective_at,
                issuance_sequence=object_sequence,
                effective_sequence=effective_sequence,
            )
            event = _new_context_event(
                event_id=event_id,
                event_kind=AuthorityEventKind.SUPERSEDED,
                target=current,
                replacement=replacement,
                event_sequence=event_sequence,
                effective_sequence=effective_sequence,
                effective_at=effective_at,
            )
            session.add(_context_row(replacement))
            session.add(
                _registry_row(
                    event_sequence,
                    event.event_ref,
                    event.event_fingerprint,
                    "NEXT_ACTION_CONTEXT",
                    effective_at,
                )
            )
            session.add(_context_event_row(event, current.logical_key))
            projection.current_context_ref = replacement.context_ref
            projection.effective_sequence = effective_sequence
            projection.latest_event_sequence = event_sequence
            projection.updated_at = effective_at
            return replacement, event

    async def _revoke_next_action_context(
        self,
        capability: object,
        *,
        current_context_ref: str,
        event_id: str,
        effective_at: datetime,
    ) -> NextActionContextAuthorityEventV1:
        self._require_capability(capability)
        async with self._session_factory() as session, session.begin():
            current_row = await session.get(NextActionContextRefRow, current_context_ref)
            if current_row is None:
                _authority_conflict("NextActionContext revoke target is absent")
            current = _context_from_row(current_row)
            await _lock(session, f"external-task-authority:context:{current.logical_key}")
            event_ref = f"next-action-context-event:v1:{event_id}"
            existing = await session.get(NextActionContextAuthorityEventRow, event_ref)
            if existing is not None:
                event = _context_event_from_row(existing)
                if event.context_ref != current_context_ref:
                    _identity_conflict("NextActionContext revoke replay differs")
                return event
            projection = await session.get(
                NextActionContextCurrentRow, current.logical_key, with_for_update=True
            )
            if (
                projection is None
                or projection.current_context_ref != current.context_ref
                or projection.terminal_revoked == "true"
            ):
                _authority_conflict("NextActionContext revoke target is not exact current")
            _, event_sequence = await self._reserve_sequences(
                session, object_count=0, event_count=1
            )
            effective_sequence = projection.effective_sequence + 1
            event = _new_context_event(
                event_id=event_id,
                event_kind=AuthorityEventKind.REVOKED,
                target=current,
                replacement=None,
                event_sequence=event_sequence,
                effective_sequence=effective_sequence,
                effective_at=effective_at,
            )
            session.add(
                _registry_row(
                    event_sequence,
                    event.event_ref,
                    event.event_fingerprint,
                    "NEXT_ACTION_CONTEXT",
                    effective_at,
                )
            )
            session.add(_context_event_row(event, current.logical_key))
            projection.current_context_ref = None
            projection.terminal_revoked = "true"
            projection.effective_sequence = effective_sequence
            projection.latest_event_sequence = event_sequence
            projection.updated_at = effective_at
            return event

    async def _certify_snapshot(
        self,
        capability: object,
        *,
        snapshot_id: str,
        issued_at: datetime,
        session: AsyncSession | None = None,
    ) -> TaskConstraintOwnerSnapshotV1:
        self._require_capability(capability)
        snapshot_ref = f"task-constraint-owner-snapshot:v1:{snapshot_id}"
        if session is None:
            async with self._session_factory() as owned_session, owned_session.begin():
                return await self._certify_snapshot(
                    capability, snapshot_id=snapshot_id, issued_at=issued_at, session=owned_session
                )
        if not session.in_transaction():
            _authority_conflict("caller transaction required")
        await _lock(session, "external-task-authority:snapshot")
        existing = await session.get(TaskConstraintOwnerSnapshotRow, snapshot_ref)
        if existing is not None:
            return _snapshot_from_row(existing)
        counter = await self._counter(session)
        high_watermark = counter.event_sequence
        pairs = await _registry_pairs(session, high_watermark)
        snapshot = _new_snapshot(
            snapshot_ref=snapshot_ref,
            high_watermark=high_watermark,
            prefix_root=ordered_event_prefix_root(pairs),
            issued_at=issued_at,
        )
        await self._ensure_issuer_binding(session, issued_at)
        payload = snapshot.fingerprint_payload() | {
            "snapshot_fingerprint": snapshot.snapshot_fingerprint
        }
        session.add(
            TaskConstraintOwnerSnapshotRow(
                snapshot_ref=snapshot.snapshot_ref,
                snapshot_fingerprint=snapshot.snapshot_fingerprint,
                owner_event_high_watermark=snapshot.owner_event_high_watermark,
                ordered_event_prefix_root=snapshot.ordered_event_prefix_root,
                issuer_binding_fingerprint=_ISSUER_BINDING_FINGERPRINT,
                payload=payload,
                issued_at=snapshot.issued_at,
            )
        )
        return snapshot

    async def get_task_constraint(self, constraint_ref: str) -> TaskConstraintRefV1 | None:
        async with self._session_factory() as session:
            row = await session.get(TaskConstraintRefRow, constraint_ref)
            if row is None:
                return None
            await _verify_binding(session, row.issuer_binding_fingerprint)
            return _constraint_from_row(row)

    async def get_next_action_context(self, context_ref: str) -> NextActionContextRefV1 | None:
        async with self._session_factory() as session:
            row = await session.get(NextActionContextRefRow, context_ref)
            if row is None:
                return None
            await _verify_binding(session, row.issuer_binding_fingerprint)
            return _context_from_row(row)

    async def get_context_event(self, event_ref: str) -> NextActionContextAuthorityEventV1 | None:
        async with self._session_factory() as session:
            row = await session.get(NextActionContextAuthorityEventRow, event_ref)
            if row is None:
                return None
            await _verify_binding(session, row.issuer_binding_fingerprint)
            return _context_event_from_row(row)

    async def latest_snapshot(
        self, *, session: AsyncSession | None = None
    ) -> TaskConstraintOwnerSnapshotV1:
        if session is None:
            async with self._session_factory() as owned_session:
                return await self.latest_snapshot(session=owned_session)
        row = await session.scalar(
            select(TaskConstraintOwnerSnapshotRow).order_by(
                TaskConstraintOwnerSnapshotRow.owner_event_high_watermark.desc()
            )
        )
        if row is None:
            _history_corrupt("certified external Task-authority snapshot is absent")
        return await _verify_snapshot(session, row)

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
    ) -> TaskConstraintFoldResult:
        if session is None:
            async with self._session_factory() as owned_session:
                return await self.verify_task_constraint(
                    constraint_ref=constraint_ref,
                    constraint_fingerprint=constraint_fingerprint,
                    snapshot_ref=snapshot_ref,
                    snapshot_fingerprint=snapshot_fingerprint,
                    owner_event_high_watermark=owner_event_high_watermark,
                    require_current=require_current,
                    session=owned_session,
                )
        row = await session.get(TaskConstraintRefRow, constraint_ref)
        snapshot_row = await session.get(TaskConstraintOwnerSnapshotRow, snapshot_ref)
        if row is None or snapshot_row is None:
            _history_corrupt("TaskConstraint object/snapshot is absent")
        value = _constraint_from_row(row)
        snapshot = await _verify_snapshot(session, snapshot_row)
        if (
            value.constraint_fingerprint != constraint_fingerprint
            or snapshot.snapshot_fingerprint != snapshot_fingerprint
            or snapshot.owner_event_high_watermark != owner_event_high_watermark
        ):
            _history_corrupt("TaskConstraint object/snapshot identity differs")
        result = await _fold_constraints(session, value.logical_key, snapshot)
        history = await _constraint_events(session, value.logical_key, owner_event_high_watermark)
        introduced_refs = {
            ref
            for event in history
            for ref in (event.constraint_ref, event.replacement_constraint_ref)
            if ref is not None
        }
        if value.constraint_ref not in introduced_refs:
            _history_corrupt("TaskConstraint ref was not introduced by the certified prefix")
        if require_current:
            await _require_latest_snapshot(session, snapshot)
            if result.current is None or result.current.constraint_ref != constraint_ref:
                raise ExternalTaskAuthorityError(
                    ExternalTaskAuthorityErrorCode.NOT_CURRENT,
                    "TaskConstraint is not current at latest certified H",
                )
        return result

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
    ) -> NextActionContextFoldResult:
        if session is None:
            async with self._session_factory() as owned_session:
                return await self.verify_next_action_context(
                    context_ref=context_ref,
                    context_fingerprint=context_fingerprint,
                    introduction_event_ref=introduction_event_ref,
                    introduction_event_fingerprint=introduction_event_fingerprint,
                    snapshot_ref=snapshot_ref,
                    snapshot_fingerprint=snapshot_fingerprint,
                    owner_event_high_watermark=owner_event_high_watermark,
                    require_current=require_current,
                    session=owned_session,
                )
        row = await session.get(NextActionContextRefRow, context_ref)
        if require_current and row is not None:
            await _lock(session, f"external-task-authority:context:{row.logical_key}")
            await _lock(session, "external-task-authority:global-sequence")
        intro_row = await session.get(NextActionContextAuthorityEventRow, introduction_event_ref)
        snapshot_row = await session.get(TaskConstraintOwnerSnapshotRow, snapshot_ref)
        if row is None or intro_row is None or snapshot_row is None:
            _history_corrupt("NextActionContext object/event/snapshot is absent")
        value = _context_from_row(row)
        introduction = _context_event_from_row(intro_row)
        snapshot = await _verify_snapshot(session, snapshot_row)
        introduced = (
            introduction.event_kind is AuthorityEventKind.ISSUED
            and introduction.context_ref == context_ref
        ) or (
            introduction.event_kind is AuthorityEventKind.SUPERSEDED
            and introduction.replacement_context_ref == context_ref
        )
        if (
            value.fingerprint != context_fingerprint
            or introduction.event_fingerprint != introduction_event_fingerprint
            or not introduced
            or snapshot.snapshot_fingerprint != snapshot_fingerprint
            or snapshot.owner_event_high_watermark != owner_event_high_watermark
            or introduction.event_sequence > owner_event_high_watermark
        ):
            _history_corrupt("NextActionContext original authority graph differs")
        result = await _fold_contexts(session, value.logical_key, snapshot)
        if require_current:
            await _require_latest_snapshot(session, snapshot)
            if result.current is None or result.current.context_ref != context_ref:
                raise ExternalTaskAuthorityError(
                    ExternalTaskAuthorityErrorCode.NOT_CURRENT,
                    "NextActionContext is not current at latest certified H",
                )
        return result

    async def _counter(self, session: AsyncSession) -> ExternalTaskAuthorityCounterRow:
        counter = await session.get(
            ExternalTaskAuthorityCounterRow, _COUNTER_ID, with_for_update=True
        )
        if counter is None:
            counter = ExternalTaskAuthorityCounterRow(
                counter_id=_COUNTER_ID, object_sequence=0, event_sequence=0
            )
            session.add(counter)
            await session.flush()
        return counter

    async def _reserve_sequences(
        self, session: AsyncSession, *, object_count: int, event_count: int
    ) -> tuple[int, int]:
        await _lock(session, "external-task-authority:global-sequence")
        counter = await self._counter(session)
        counter.object_sequence += object_count
        counter.event_sequence += event_count
        if counter.object_sequence > MAX_SAFE_INTEGER or counter.event_sequence > MAX_SAFE_INTEGER:
            _authority_conflict("external Task-authority sequence exhausted")
        return counter.object_sequence, counter.event_sequence

    @staticmethod
    async def _ensure_issuer_binding(session: AsyncSession, now: datetime) -> None:
        existing = await session.get(ExternalTaskAuthorityIssuerBindingRow, _ISSUER_BINDING_REF)
        if existing is not None:
            await _verify_binding(session, _ISSUER_BINDING_FINGERPRINT)
            return
        session.add(
            ExternalTaskAuthorityIssuerBindingRow(
                binding_ref=_ISSUER_BINDING_REF,
                binding_fingerprint=_ISSUER_BINDING_FINGERPRINT,
                authority_owner=EXTERNAL_TASK_AUTHORITY_OWNER,
                authority_version=str(_ISSUER_BINDING_PAYLOAD["authority_version"]),
                authority_revision=AUTHORITY_REVISION,
                payload=_ISSUER_BINDING_PAYLOAD,
                bound_at=now,
            )
        )


async def _fold_constraints(
    session: AsyncSession, logical_key: str, snapshot: TaskConstraintOwnerSnapshotV1
) -> TaskConstraintFoldResult:
    events = await _constraint_events(session, logical_key, snapshot.owner_event_high_watermark)
    current: TaskConstraintRefV1 | None = None
    expected_effective = 1
    consumed: list[str] = []
    revoked = False
    for event in events:
        if event.effective_sequence != expected_effective or revoked:
            _history_corrupt("TaskConstraint effective history has a gap or post-revoke event")
        target_row = await session.get(TaskConstraintRefRow, event.constraint_ref)
        if target_row is None:
            _history_corrupt("TaskConstraint event target is unresolved")
        target = _constraint_from_row(target_row)
        if event.event_kind is AuthorityEventKind.ISSUED:
            if current is not None or expected_effective != 1:
                _history_corrupt("TaskConstraint origin is not unique")
            current = target
        else:
            if current is None or current.constraint_ref != target.constraint_ref:
                _history_corrupt("TaskConstraint event does not target exact folded current")
            if event.event_kind is AuthorityEventKind.SUPERSEDED:
                replacement_row = await session.get(
                    TaskConstraintRefRow, event.replacement_constraint_ref
                )
                if replacement_row is None:
                    _history_corrupt("TaskConstraint replacement is unresolved")
                replacement = _constraint_from_row(replacement_row)
                if (
                    replacement.logical_key != logical_key
                    or replacement.constraint_fingerprint
                    != event.replacement_constraint_fingerprint
                ):
                    _history_corrupt("TaskConstraint replacement binding differs")
                current = replacement
            else:
                current = None
                revoked = True
        consumed.append(event.event_ref)
        expected_effective += 1
    if not events:
        _history_corrupt("TaskConstraint logical history is absent")
    return TaskConstraintFoldResult(
        current,
        tuple(consumed),
        snapshot.snapshot_ref,
        snapshot.snapshot_fingerprint,
        snapshot.owner_event_high_watermark,
    )


async def _fold_contexts(
    session: AsyncSession, logical_key: str, snapshot: TaskConstraintOwnerSnapshotV1
) -> NextActionContextFoldResult:
    events = await _context_events(session, logical_key, snapshot.owner_event_high_watermark)
    current: NextActionContextRefV1 | None = None
    expected_effective = 1
    consumed: list[str] = []
    revoked = False
    for event in events:
        if event.effective_sequence != expected_effective or revoked:
            _history_corrupt("NextActionContext effective history has a gap or post-revoke event")
        target_row = await session.get(NextActionContextRefRow, event.context_ref)
        if target_row is None:
            _history_corrupt("NextActionContext event target is unresolved")
        target = _context_from_row(target_row)
        if event.event_kind is AuthorityEventKind.ISSUED:
            if current is not None or expected_effective != 1:
                _history_corrupt("NextActionContext origin is not unique")
            current = target
        else:
            if current is None or current.context_ref != target.context_ref:
                _history_corrupt("NextActionContext event does not target exact folded current")
            if event.event_kind is AuthorityEventKind.SUPERSEDED:
                replacement_row = await session.get(
                    NextActionContextRefRow, event.replacement_context_ref
                )
                if replacement_row is None:
                    _history_corrupt("NextActionContext replacement is unresolved")
                replacement = _context_from_row(replacement_row)
                if (
                    replacement.logical_key != logical_key
                    or replacement.fingerprint != event.replacement_context_fingerprint
                    or replacement.effective_sequence != event.effective_sequence
                ):
                    _history_corrupt("NextActionContext replacement binding differs")
                current = replacement
            else:
                current = None
                revoked = True
        consumed.append(event.event_ref)
        expected_effective += 1
    if not events:
        _history_corrupt("NextActionContext logical history is absent")
    return NextActionContextFoldResult(
        current,
        tuple(consumed),
        snapshot.snapshot_ref,
        snapshot.snapshot_fingerprint,
        snapshot.owner_event_high_watermark,
    )


async def _verify_snapshot(
    session: AsyncSession, row: TaskConstraintOwnerSnapshotRow
) -> TaskConstraintOwnerSnapshotV1:
    await _verify_binding(session, row.issuer_binding_fingerprint)
    snapshot = _snapshot_from_row(row)
    pairs = await _registry_pairs(session, snapshot.owner_event_high_watermark)
    if ordered_event_prefix_root(pairs) != snapshot.ordered_event_prefix_root:
        _history_corrupt("owner snapshot complete-prefix root differs")
    return snapshot


async def _require_latest_snapshot(
    session: AsyncSession, snapshot: TaskConstraintOwnerSnapshotV1
) -> None:
    latest = int(
        await session.scalar(
            select(func.coalesce(func.max(ExternalTaskAuthorityEventRegistryRow.event_sequence), 0))
        )
        or 0
    )
    if snapshot.owner_event_high_watermark != latest:
        raise ExternalTaskAuthorityError(
            ExternalTaskAuthorityErrorCode.NOT_CURRENT,
            "current query requires the latest certified owner H",
        )


async def _registry_pairs(
    session: AsyncSession, high_watermark: int
) -> tuple[tuple[str, str], ...]:
    rows = tuple(
        await session.scalars(
            select(ExternalTaskAuthorityEventRegistryRow)
            .where(ExternalTaskAuthorityEventRegistryRow.event_sequence <= high_watermark)
            .order_by(ExternalTaskAuthorityEventRegistryRow.event_sequence)
        )
    )
    if len(rows) != high_watermark or any(
        row.event_sequence != ordinal for ordinal, row in enumerate(rows, 1)
    ):
        _history_corrupt("external Task-authority global prefix is incomplete")
    return tuple((row.event_ref, row.event_fingerprint) for row in rows)


async def _constraint_events(
    session: AsyncSession, logical_key: str, high_watermark: int
) -> tuple[TaskConstraintAuthorityEventV1, ...]:
    rows = tuple(
        await session.scalars(
            select(TaskConstraintAuthorityEventRow)
            .where(
                TaskConstraintAuthorityEventRow.logical_key == logical_key,
                TaskConstraintAuthorityEventRow.event_sequence <= high_watermark,
            )
            .order_by(TaskConstraintAuthorityEventRow.event_sequence)
        )
    )
    return tuple(_constraint_event_from_row(row) for row in rows)


async def _context_events(
    session: AsyncSession, logical_key: str, high_watermark: int
) -> tuple[NextActionContextAuthorityEventV1, ...]:
    rows = tuple(
        await session.scalars(
            select(NextActionContextAuthorityEventRow)
            .where(
                NextActionContextAuthorityEventRow.logical_key == logical_key,
                NextActionContextAuthorityEventRow.event_sequence <= high_watermark,
            )
            .order_by(NextActionContextAuthorityEventRow.event_sequence)
        )
    )
    return tuple(_context_event_from_row(row) for row in rows)


async def _verify_binding(session: AsyncSession, fingerprint: str) -> None:
    row = await session.get(ExternalTaskAuthorityIssuerBindingRow, _ISSUER_BINDING_REF)
    if (
        row is None
        or fingerprint != _ISSUER_BINDING_FINGERPRINT
        or row.binding_fingerprint != _ISSUER_BINDING_FINGERPRINT
        or row.payload != _ISSUER_BINDING_PAYLOAD
        or canonical_sha256(row.payload) != row.binding_fingerprint
    ):
        _history_corrupt("external Task-authority issuer binding differs")


async def _lock(session: AsyncSession, key: str) -> None:
    await session.execute(
        text("SELECT pg_advisory_xact_lock(hashtextextended(:key, 0))"), {"key": key}
    )


def _new_constraint(
    *,
    constraint_ref_id: str,
    logical_constraint_id: str,
    scope: TaskConstraintScopeV1,
    constraint_schema_id: str,
    constraint_schema_version: str,
    constraint_payload_ref: str,
    constraint_payload_fingerprint: str,
    issued_at: datetime,
    issuance_sequence: int,
) -> TaskConstraintRefV1:
    payload: dict[str, object] = {
        "constraint_ref": f"task-constraint:v1:{constraint_ref_id}",
        "constraint_ref_id": constraint_ref_id,
        "constraint_ref_version": "v1",
        "fingerprint_schema": "task-constraint-ref-v1",
        "constraint_owner": EXTERNAL_TASK_AUTHORITY_OWNER,
        "authority_ref": TASK_CONSTRAINT_AUTHORITY_REF,
        "authority_version": TASK_CONSTRAINT_AUTHORITY_VERSION,
        "authority_revision": AUTHORITY_REVISION,
        "logical_constraint_id": logical_constraint_id,
        "scope": scope.payload(),
        "constraint_schema_id": constraint_schema_id,
        "constraint_schema_version": constraint_schema_version,
        "constraint_payload_ref": constraint_payload_ref,
        "constraint_payload_fingerprint": constraint_payload_fingerprint,
        "issued_at": _timestamp(issued_at),
        "issuance_sequence": issuance_sequence,
    }
    return TaskConstraintRefV1(
        str(payload["constraint_ref"]),
        constraint_ref_id,
        "v1",
        "task-constraint-ref-v1",
        EXTERNAL_TASK_AUTHORITY_OWNER,
        TASK_CONSTRAINT_AUTHORITY_REF,
        TASK_CONSTRAINT_AUTHORITY_VERSION,
        AUTHORITY_REVISION,
        logical_constraint_id,
        scope,
        constraint_schema_id,
        constraint_schema_version,
        constraint_payload_ref,
        constraint_payload_fingerprint,
        issued_at,
        issuance_sequence,
        canonical_sha256(payload),
    )


def _new_constraint_event(
    *,
    event_id: str,
    event_kind: AuthorityEventKind,
    target: TaskConstraintRefV1,
    replacement: TaskConstraintRefV1 | None,
    event_sequence: int,
    effective_sequence: int,
    effective_at: datetime,
) -> TaskConstraintAuthorityEventV1:
    disposition = (
        CurrentProjectionDisposition.RETAIN_CURRENT
        if event_kind is AuthorityEventKind.ISSUED
        else CurrentProjectionDisposition.WITHDRAW_CURRENT
    )
    payload: dict[str, object] = {
        "event_ref": f"task-constraint-event:v1:{event_id}",
        "event_id": event_id,
        "event_version": "v1",
        "fingerprint_schema": "task-constraint-authority-event-v1",
        "event_kind": event_kind.value,
        "constraint_ref": target.constraint_ref,
        "constraint_fingerprint": target.constraint_fingerprint,
        "replacement_constraint_ref": replacement.constraint_ref if replacement else None,
        "replacement_constraint_fingerprint": (
            replacement.constraint_fingerprint if replacement else None
        ),
        "logical_constraint_id": target.logical_constraint_id,
        "scope": target.scope.payload(),
        "authority_ref": TASK_CONSTRAINT_AUTHORITY_REF,
        "authority_version": TASK_CONSTRAINT_AUTHORITY_VERSION,
        "authority_revision": AUTHORITY_REVISION,
        "event_sequence": event_sequence,
        "effective_sequence": effective_sequence,
        "effective_at": _timestamp(effective_at),
        "current_projection_disposition": disposition.value,
    }
    return TaskConstraintAuthorityEventV1(
        str(payload["event_ref"]),
        event_id,
        "v1",
        "task-constraint-authority-event-v1",
        event_kind,
        target.constraint_ref,
        target.constraint_fingerprint,
        replacement.constraint_ref if replacement else None,
        replacement.constraint_fingerprint if replacement else None,
        target.logical_constraint_id,
        target.scope,
        TASK_CONSTRAINT_AUTHORITY_REF,
        TASK_CONSTRAINT_AUTHORITY_VERSION,
        AUTHORITY_REVISION,
        event_sequence,
        effective_sequence,
        effective_at,
        disposition,
        canonical_sha256(payload),
    )


def _new_context(
    *,
    context_ref_id: str,
    context_logical_id: str,
    project_id: str,
    task_contract_id: str,
    task_contract_version: str,
    context_slot_id: str,
    priority_class: NextActionPriorityClass,
    critical_path_ordinal: int,
    issued_at: datetime,
    issuance_sequence: int,
    effective_sequence: int,
) -> NextActionContextRefV1:
    payload: dict[str, object] = {
        "context_ref": f"next-action-context:v1:{context_ref_id}",
        "context_ref_id": context_ref_id,
        "context_ref_version": "v1",
        "fingerprint_schema": "next-action-context-ref-v1",
        "context_owner": EXTERNAL_TASK_AUTHORITY_OWNER,
        "authority_ref": NEXT_ACTION_CONTEXT_AUTHORITY_REF,
        "authority_version": NEXT_ACTION_CONTEXT_AUTHORITY_VERSION,
        "authority_revision": AUTHORITY_REVISION,
        "context_logical_id": context_logical_id,
        "project_id": project_id,
        "scope_kind": "TASK_CONTRACT",
        "task_contract_id": task_contract_id,
        "task_contract_version": task_contract_version,
        "context_slot_id": context_slot_id,
        "priority_class": priority_class.value,
        "critical_path_ordinal": critical_path_ordinal,
        "context_payload_schema_id": "P1_8_NEXT_ACTION_CONTEXT_RESULT_V1",
        "context_payload_schema_version": "v1",
        "context_payload_schema_fingerprint": NEXT_ACTION_CONTEXT_RESULT_SCHEMA_FINGERPRINT,
        "privacy_class": "PRIVATE_INTERNAL",
        "security_class": "INTERNAL_REFERENCE_ONLY",
        "issued_at": _timestamp(issued_at),
        "issuance_sequence": issuance_sequence,
        "effective_sequence": effective_sequence,
    }
    return NextActionContextRefV1(
        str(payload["context_ref"]),
        context_ref_id,
        "v1",
        "next-action-context-ref-v1",
        EXTERNAL_TASK_AUTHORITY_OWNER,
        NEXT_ACTION_CONTEXT_AUTHORITY_REF,
        NEXT_ACTION_CONTEXT_AUTHORITY_VERSION,
        AUTHORITY_REVISION,
        context_logical_id,
        project_id,
        "TASK_CONTRACT",
        task_contract_id,
        task_contract_version,
        context_slot_id,
        priority_class,
        critical_path_ordinal,
        "P1_8_NEXT_ACTION_CONTEXT_RESULT_V1",
        "v1",
        NEXT_ACTION_CONTEXT_RESULT_SCHEMA_FINGERPRINT,
        "PRIVATE_INTERNAL",
        "INTERNAL_REFERENCE_ONLY",
        issued_at,
        issuance_sequence,
        effective_sequence,
        canonical_sha256(payload),
    )


def _new_context_event(
    *,
    event_id: str,
    event_kind: AuthorityEventKind,
    target: NextActionContextRefV1,
    replacement: NextActionContextRefV1 | None,
    event_sequence: int,
    effective_sequence: int,
    effective_at: datetime,
) -> NextActionContextAuthorityEventV1:
    disposition = (
        CurrentProjectionDisposition.RETAIN_CURRENT
        if event_kind is AuthorityEventKind.ISSUED
        else CurrentProjectionDisposition.WITHDRAW_CURRENT
    )
    payload: dict[str, object] = {
        "event_ref": f"next-action-context-event:v1:{event_id}",
        "event_id": event_id,
        "event_version": "v1",
        "fingerprint_schema": "next-action-context-authority-event-v1",
        "event_kind": event_kind.value,
        "context_ref": target.context_ref,
        "context_fingerprint": target.fingerprint,
        "replacement_context_ref": replacement.context_ref if replacement else None,
        "replacement_context_fingerprint": replacement.fingerprint if replacement else None,
        "project_id": target.project_id,
        "task_contract_id": target.task_contract_id,
        "task_contract_version": target.task_contract_version,
        "context_logical_id": target.context_logical_id,
        "context_slot_id": target.context_slot_id,
        "authority_ref": NEXT_ACTION_CONTEXT_AUTHORITY_REF,
        "authority_version": NEXT_ACTION_CONTEXT_AUTHORITY_VERSION,
        "authority_revision": AUTHORITY_REVISION,
        "event_sequence": event_sequence,
        "effective_sequence": effective_sequence,
        "effective_at": _timestamp(effective_at),
        "current_projection_disposition": disposition.value,
    }
    return NextActionContextAuthorityEventV1(
        str(payload["event_ref"]),
        event_id,
        "v1",
        "next-action-context-authority-event-v1",
        event_kind,
        target.context_ref,
        target.fingerprint,
        replacement.context_ref if replacement else None,
        replacement.fingerprint if replacement else None,
        target.project_id,
        target.task_contract_id,
        target.task_contract_version,
        target.context_logical_id,
        target.context_slot_id,
        NEXT_ACTION_CONTEXT_AUTHORITY_REF,
        NEXT_ACTION_CONTEXT_AUTHORITY_VERSION,
        AUTHORITY_REVISION,
        event_sequence,
        effective_sequence,
        effective_at,
        disposition,
        canonical_sha256(payload),
    )


def _new_snapshot(
    *, snapshot_ref: str, high_watermark: int, prefix_root: str, issued_at: datetime
) -> TaskConstraintOwnerSnapshotV1:
    payload: dict[str, object] = {
        "snapshot_ref": snapshot_ref,
        "snapshot_version": "v1",
        "fingerprint_schema": "task-constraint-owner-snapshot-v1",
        "authority_ref": TASK_CONSTRAINT_AUTHORITY_REF,
        "authority_version": TASK_CONSTRAINT_AUTHORITY_VERSION,
        "authority_revision": AUTHORITY_REVISION,
        "owner_event_high_watermark": high_watermark,
        "ordered_event_prefix_root": prefix_root,
        "issued_at": _timestamp(issued_at),
    }
    return TaskConstraintOwnerSnapshotV1(
        snapshot_ref,
        "v1",
        "task-constraint-owner-snapshot-v1",
        TASK_CONSTRAINT_AUTHORITY_REF,
        TASK_CONSTRAINT_AUTHORITY_VERSION,
        AUTHORITY_REVISION,
        high_watermark,
        prefix_root,
        issued_at,
        canonical_sha256(payload),
    )


def _constraint_row(value: TaskConstraintRefV1) -> TaskConstraintRefRow:
    return TaskConstraintRefRow(
        constraint_ref=value.constraint_ref,
        constraint_fingerprint=value.constraint_fingerprint,
        logical_key=value.logical_key,
        logical_constraint_id=value.logical_constraint_id,
        scope_kind=value.scope.scope_kind.value,
        project_id=value.scope.project_id,
        task_contract_id=value.scope.task_contract_id,
        task_contract_version=value.scope.task_contract_version,
        work_run_id=value.scope.work_run_id,
        issuance_sequence=value.issuance_sequence,
        issuer_binding_fingerprint=_ISSUER_BINDING_FINGERPRINT,
        payload=value.fingerprint_payload()
        | {"constraint_fingerprint": value.constraint_fingerprint},
        issued_at=value.issued_at,
    )


def _context_row(value: NextActionContextRefV1) -> NextActionContextRefRow:
    return NextActionContextRefRow(
        context_ref=value.context_ref,
        context_fingerprint=value.fingerprint,
        logical_key=value.logical_key,
        context_logical_id=value.context_logical_id,
        project_id=value.project_id,
        task_contract_id=value.task_contract_id,
        task_contract_version=value.task_contract_version,
        context_slot_id=value.context_slot_id,
        priority_class=value.priority_class.value,
        critical_path_ordinal=value.critical_path_ordinal,
        issuance_sequence=value.issuance_sequence,
        effective_sequence=value.effective_sequence,
        issuer_binding_fingerprint=_ISSUER_BINDING_FINGERPRINT,
        payload=value.fingerprint_payload() | {"fingerprint": value.fingerprint},
        issued_at=value.issued_at,
    )


def _constraint_event_row(
    value: TaskConstraintAuthorityEventV1, logical_key: str
) -> TaskConstraintAuthorityEventRow:
    return TaskConstraintAuthorityEventRow(
        event_ref=value.event_ref,
        event_id=value.event_id,
        event_fingerprint=value.event_fingerprint,
        event_sequence=value.event_sequence,
        effective_sequence=value.effective_sequence,
        logical_key=logical_key,
        event_kind=value.event_kind.value,
        constraint_ref=value.constraint_ref,
        replacement_constraint_ref=value.replacement_constraint_ref,
        issuer_binding_fingerprint=_ISSUER_BINDING_FINGERPRINT,
        payload=value.fingerprint_payload() | {"event_fingerprint": value.event_fingerprint},
        effective_at=value.effective_at,
    )


def _context_event_row(
    value: NextActionContextAuthorityEventV1, logical_key: str
) -> NextActionContextAuthorityEventRow:
    return NextActionContextAuthorityEventRow(
        event_ref=value.event_ref,
        event_id=value.event_id,
        event_fingerprint=value.event_fingerprint,
        event_sequence=value.event_sequence,
        effective_sequence=value.effective_sequence,
        logical_key=logical_key,
        event_kind=value.event_kind.value,
        context_ref=value.context_ref,
        replacement_context_ref=value.replacement_context_ref,
        issuer_binding_fingerprint=_ISSUER_BINDING_FINGERPRINT,
        payload=value.fingerprint_payload() | {"event_fingerprint": value.event_fingerprint},
        effective_at=value.effective_at,
    )


def _registry_row(
    sequence: int, event_ref: str, fingerprint: str, domain: str, created_at: datetime
) -> ExternalTaskAuthorityEventRegistryRow:
    return ExternalTaskAuthorityEventRegistryRow(
        event_sequence=sequence,
        event_ref=event_ref,
        event_fingerprint=fingerprint,
        event_domain=domain,
        created_at=created_at,
    )


def _constraint_from_row(row: TaskConstraintRefRow) -> TaskConstraintRefV1:
    if row.payload.get("constraint_fingerprint") != row.constraint_fingerprint:
        _history_corrupt("TaskConstraint row fingerprint binding differs")
    return task_constraint_ref_from_payload(dict(row.payload))


def _context_from_row(row: NextActionContextRefRow) -> NextActionContextRefV1:
    if row.payload.get("fingerprint") != row.context_fingerprint:
        _history_corrupt("NextActionContext row fingerprint binding differs")
    return next_action_context_ref_from_payload(dict(row.payload))


def _constraint_event_from_row(
    row: TaskConstraintAuthorityEventRow,
) -> TaskConstraintAuthorityEventV1:
    payload = row.payload
    raw_scope = payload.get("scope")
    if not isinstance(raw_scope, dict):
        _history_corrupt("TaskConstraint event scope payload is malformed")
    scope_payload = cast(dict[str, object], raw_scope)
    scope = TaskConstraintScopeV1(
        scope_kind=TaskConstraintScopeKind(str(scope_payload["scope_kind"])),
        project_id=str(scope_payload["project_id"]),
        task_contract_id=_optional_str(scope_payload.get("task_contract_id")),
        task_contract_version=_optional_str(scope_payload.get("task_contract_version")),
        work_run_id=_optional_str(scope_payload.get("work_run_id")),
    )
    return TaskConstraintAuthorityEventV1(
        event_ref=str(payload["event_ref"]),
        event_id=str(payload["event_id"]),
        event_version=str(payload["event_version"]),
        fingerprint_schema=str(payload["fingerprint_schema"]),
        event_kind=AuthorityEventKind(str(payload["event_kind"])),
        constraint_ref=str(payload["constraint_ref"]),
        constraint_fingerprint=str(payload["constraint_fingerprint"]),
        replacement_constraint_ref=_optional_str(payload.get("replacement_constraint_ref")),
        replacement_constraint_fingerprint=_optional_str(
            payload.get("replacement_constraint_fingerprint")
        ),
        logical_constraint_id=str(payload["logical_constraint_id"]),
        scope=scope,
        authority_ref=str(payload["authority_ref"]),
        authority_version=str(payload["authority_version"]),
        authority_revision=int(str(payload["authority_revision"])),
        event_sequence=int(str(payload["event_sequence"])),
        effective_sequence=int(str(payload["effective_sequence"])),
        effective_at=_parse_timestamp(str(payload["effective_at"])),
        current_projection_disposition=CurrentProjectionDisposition(
            str(payload["current_projection_disposition"])
        ),
        event_fingerprint=str(payload["event_fingerprint"]),
    )


def _context_event_from_row(
    row: NextActionContextAuthorityEventRow,
) -> NextActionContextAuthorityEventV1:
    payload = row.payload
    return NextActionContextAuthorityEventV1(
        event_ref=str(payload["event_ref"]),
        event_id=str(payload["event_id"]),
        event_version=str(payload["event_version"]),
        fingerprint_schema=str(payload["fingerprint_schema"]),
        event_kind=AuthorityEventKind(str(payload["event_kind"])),
        context_ref=str(payload["context_ref"]),
        context_fingerprint=str(payload["context_fingerprint"]),
        replacement_context_ref=_optional_str(payload.get("replacement_context_ref")),
        replacement_context_fingerprint=_optional_str(
            payload.get("replacement_context_fingerprint")
        ),
        project_id=str(payload["project_id"]),
        task_contract_id=str(payload["task_contract_id"]),
        task_contract_version=str(payload["task_contract_version"]),
        context_logical_id=str(payload["context_logical_id"]),
        context_slot_id=str(payload["context_slot_id"]),
        authority_ref=str(payload["authority_ref"]),
        authority_version=str(payload["authority_version"]),
        authority_revision=int(str(payload["authority_revision"])),
        event_sequence=int(str(payload["event_sequence"])),
        effective_sequence=int(str(payload["effective_sequence"])),
        effective_at=_parse_timestamp(str(payload["effective_at"])),
        current_projection_disposition=CurrentProjectionDisposition(
            str(payload["current_projection_disposition"])
        ),
        event_fingerprint=str(payload["event_fingerprint"]),
    )


def _snapshot_from_row(row: TaskConstraintOwnerSnapshotRow) -> TaskConstraintOwnerSnapshotV1:
    payload = row.payload
    return TaskConstraintOwnerSnapshotV1(
        snapshot_ref=str(payload["snapshot_ref"]),
        snapshot_version=str(payload["snapshot_version"]),
        fingerprint_schema=str(payload["fingerprint_schema"]),
        authority_ref=str(payload["authority_ref"]),
        authority_version=str(payload["authority_version"]),
        authority_revision=int(str(payload["authority_revision"])),
        owner_event_high_watermark=int(str(payload["owner_event_high_watermark"])),
        ordered_event_prefix_root=str(payload["ordered_event_prefix_root"]),
        issued_at=_parse_timestamp(str(payload["issued_at"])),
        snapshot_fingerprint=str(payload["snapshot_fingerprint"]),
    )


def _context_logical_key(
    project_id: str,
    task_contract_id: str,
    task_contract_version: str,
    context_logical_id: str,
    context_slot_id: str,
) -> str:
    return canonical_sha256(
        {
            "project_id": project_id,
            "task_contract_id": task_contract_id,
            "task_contract_version": task_contract_version,
            "context_logical_id": context_logical_id,
            "context_slot_id": context_slot_id,
        }
    )


def _timestamp(value: datetime) -> str:
    return value.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _parse_timestamp(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=UTC)


def _optional_str(value: object) -> str | None:
    return None if value is None else str(value)


def _identity_conflict(message: str) -> NoReturn:
    raise ExternalTaskAuthorityError(ExternalTaskAuthorityErrorCode.IDENTITY_CONFLICT, message)


def _authority_conflict(message: str) -> NoReturn:
    raise ExternalTaskAuthorityError(ExternalTaskAuthorityErrorCode.AUTHORITY_CONFLICT, message)


def _history_corrupt(message: str) -> NoReturn:
    raise ExternalTaskAuthorityError(ExternalTaskAuthorityErrorCode.HISTORY_CORRUPT, message)
