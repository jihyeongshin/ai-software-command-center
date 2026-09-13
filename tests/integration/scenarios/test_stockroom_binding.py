from __future__ import annotations

import asyncio
import inspect
import socket
import subprocess
from dataclasses import FrozenInstanceError, dataclass, replace
from pathlib import Path
from threading import Event
from types import MappingProxyType

import pytest

import aiscc.scenarios.composition as composition_module
from aiscc import bootstrap
from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.evidence.service import EvidenceAdmissionService
from aiscc.human.repository import PostgresHumanAuthorityRepository
from aiscc.judgment.authority import PostgresJudgmentAuthority
from aiscc.persistence.repository import PostgresExecutionRepository
from aiscc.providers.local_deterministic import LocalDeterministicProvider
from aiscc.providers.openai_responses import OpenAIResponsesAdapter
from aiscc.providers.service import AgentExecutionService
from aiscc.providers.stockroom_tool import StockroomSummaryDispatcher
from aiscc.runtime.docker import DockerRuntime, StockroomCancellation
from aiscc.runtime.stockroom_materializer import StockroomMaterializer
from aiscc.runtime.stockroom_workspace import StockroomWorkspace
from aiscc.scenarios.composition import build_stockroom_owner_composition
from aiscc.scenarios.driver import StockroomOwnerDependencies
from aiscc.scenarios.models import RESOURCE_REF, SCENARIO_IDS
from aiscc.security.policy import SecurityPolicy, default_profiles
from aiscc.security.stockroom_policy import StockroomOwnerRestriction
from aiscc.workflow.kernel import WorkflowKernel
from tests.unit.runtime.test_stockroom_image import synthetic_image


def test_production_missing_provenance_denies_before_process_or_database(tmp_path, monkeypatch):
    _, ref, _, path, _ = synthetic_image(tmp_path, monkeypatch)
    path.unlink()
    signature = inspect.signature(bootstrap.build_stockroom_production)
    assert "docker_process_runner" not in signature.parameters
    assert "image_provenance_ref" in signature.parameters
    assert "cancellation" in signature.parameters
    with pytest.raises(FileNotFoundError):
        asyncio.run(bootstrap.build_stockroom_production(
            session_factory=None, repository_root=Path(__file__).resolve().parents[3],
            private_runtime_root=tmp_path, downloads_root=tmp_path,
            trusted_git_executable=tmp_path / "git.exe", image_provenance_ref=ref,
            trusted_docker_executable=tmp_path / "absent-docker.exe",
            cancellation=StockroomCancellation("run", "attempt", Event()),
            project_id="test", requester_identity="test", human_selector_fingerprint="a" * 64,
            secret_material_by_ref={
                "secret-ref:stockroom-local-non-secret-compat-v1": (
                    "aiscc-local-non-secret-sentinel-v1"
                )
            },
        ))


@dataclass(frozen=True, slots=True)
class _FactoryAuthority:
    semantic_role: str
    factory_ref: str
    factory_fingerprint: str


def _owners() -> StockroomOwnerDependencies:
    config = build_stockroom_owner_composition().security_config
    restriction = StockroomOwnerRestriction(config)
    materializer_factory = _FactoryAuthority(
        "STOCKROOM_MATERIALIZER_FACTORY", "binding-materializer-factory", "1" * 64
    )
    execution_factory = _FactoryAuthority(
        "STOCKROOM_AGENT_EXECUTION_SERVICE_FACTORY",
        "binding-execution-factory",
        "2" * 64,
    )
    return StockroomOwnerDependencies(
        workflow_kernel=object.__new__(WorkflowKernel),
        agent_execution_service_factory=execution_factory,
        evidence_admission_service=object.__new__(EvidenceAdmissionService),
        human_gate_owner=object.__new__(PostgresHumanAuthorityRepository),
        judgment_owner=object.__new__(PostgresJudgmentAuthority),
        workspace_owner=object.__new__(StockroomWorkspace),
        materializer_factory=materializer_factory,
        security_policy=SecurityPolicy(default_profiles(), stockroom_policy=restriction),
        stockroom_owner_restriction=restriction,
    )


def test_s1_runner_uses_production_provider_grant_with_fake_owners(tmp_path, monkeypatch):
    """S1 sequencing plus real production provider admission; no durable/runtime owners."""
    from aiscc.scenarios.capture_runner import StockroomCaptureRunner
    from aiscc.scenarios.driver import StockroomCaptureStatus
    from tests.unit.providers.test_stockroom_tool import production_provider_fixture
    from tests.unit.scenarios.test_stockroom_capture_runner import RecordingOwners

    # Initialize asyncio's local self-pipe before forbidding socket connections.
    loop = asyncio.new_event_loop()
    fixture = production_provider_fixture(tmp_path, monkeypatch)

    class LocalOwners(RecordingOwners):
        async def execute(self, prepared, materialization_ref):
            assert prepared is fixture.prepared
            assert materialization_ref == "owner:materialize"
            capabilities, secret = fixture.service._provider_capabilities(
                fixture.call, fixture.current, fixture.call.operation_id
            )
            result = fixture.service.execute_provider(fixture.call, capabilities=capabilities,
                                                      secret_request=secret)
            assert result.status == "completed" and result.tool_call.name == "stockroom_summary"
            return self._result("execute", WorkflowState.RUNNING, "COMPLETED")

    owners = LocalOwners()
    try:
        result = loop.run_until_complete(StockroomCaptureRunner(owners).run(fixture.prepared))
    finally:
        loop.close()
    assert result.status is StockroomCaptureStatus.COMPLETED
    assert (result.workflow_state, result.state_version) == (WorkflowState.ACCEPTED, 4)
    assert fixture.app.local_provider.invocation_count == 1
    assert [name for name, _ in owners.calls] == [
        "initial_ready", "create_attempt", "transition:RUNNING", "security", "grant",
        "materialize", "execute", "transition:ADMISSION_PENDING", "submit_runtime",
        "evaluate", "judgment:ACCEPTED", "transition:ACCEPTED",
    ]


def test_four_owner_bindings_prepare_without_runtime_side_effects(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: dict[str, int] = {}
    reached: list[str] = []

    def forbid(name: str):
        def forbidden(*args: object, **kwargs: object) -> None:
            del args, kwargs
            calls[name] = calls.get(name, 0) + 1
            raise AssertionError(f"runtime boundary called: {name}")

        return forbidden

    boundaries = (
        (WorkflowKernel, "request_transition"),
        (AgentExecutionService, "execute_provider"),
        (AgentExecutionService, "execute"),
        (PostgresExecutionRepository, "create_attempt"),
        (PostgresExecutionRepository, "transition_attempt"),
        (PostgresExecutionRepository, "create_operation"),
        (PostgresExecutionRepository, "advance_operation"),
        (PostgresExecutionRepository, "store_private_protocol_item"),
        (PostgresExecutionRepository, "reserve_execution_bounds"),
        (PostgresExecutionRepository, "settle_execution_output"),
        (PostgresExecutionRepository, "start_dispatch_if_fresh"),
        (PostgresExecutionRepository, "fail_operation_before_side_effect"),
        (PostgresExecutionRepository, "close_workflow_left_running"),
        (PostgresExecutionRepository, "store_output_ref"),
        (EvidenceAdmissionService, "submit"),
        (EvidenceAdmissionService, "submit_durable"),
        (EvidenceAdmissionService, "preserve_supplemental"),
        (EvidenceAdmissionService, "invalidate_authority"),
        (PostgresHumanAuthorityRepository, "submit_result"),
        (
            PostgresHumanAuthorityRepository,
            "issue_current_gate_action_authority",
        ),
        (PostgresHumanAuthorityRepository, "expire_gate_if_needed"),
        (PostgresHumanAuthorityRepository, "supersede_gate"),
        (PostgresHumanAuthorityRepository, "create_producer_ref"),
        (PostgresJudgmentAuthority, "issue"),
        (StockroomWorkspace, "allocate"),
        (StockroomWorkspace, "write_file"),
        (StockroomMaterializer, "materialize"),
        (SecurityPolicy, "issue_resource_grant"),
        (SecurityPolicy, "evaluate"),
        (SecurityPolicy, "issue_capability"),
        (StockroomOwnerRestriction, "seal_context"),
        (StockroomOwnerRestriction, "allows"),
        (LocalDeterministicProvider, "call"),
        (StockroomSummaryDispatcher, "dispatch"),
        (StockroomSummaryDispatcher, "dispatch_with_receipts"),
        (DockerRuntime, "run"),
        (DockerRuntime, "run_consumed_stockroom"),
        (OpenAIResponsesAdapter, "__init__"),
    )
    for owner, method in boundaries:
        name = f"{owner.__name__}.{method}"
        calls[name] = 0
        monkeypatch.setattr(owner, method, forbid(name))
    for owner, method in ((subprocess, "Popen"), (socket, "socket")):
        name = f"{owner.__name__}.{method}"
        calls[name] = 0
        monkeypatch.setattr(owner, method, forbid(name))

    owners = _owners()
    reached.append("owner_dependency_construction")
    prepared_root = bootstrap.build_stockroom_owner_preparation(owners=owners)
    reached.extend(("owner_composition_creation", "bootstrap_owner_preparation"))

    prepared_drivers = []
    for index, scenario_id in enumerate(SCENARIO_IDS):
        prepared_drivers.append(
            prepared_root.prepare(
                scenario_id=scenario_id,
                run_id=f"run-b3-{index + 1}",
                attempt_id="attempt-1",
                expected_initial_state_version=1,
            )
        )
        reached.append(f"S{index + 1}_request_preparation")
    prepared_drivers = tuple(prepared_drivers)
    requests = tuple(item.request for item in prepared_drivers)

    assert tuple(item.scenario_id for item in requests) == SCENARIO_IDS
    assert all(item.scenario_version == "1.0.0" for item in requests)
    assert all(item.resource_ref == RESOURCE_REF for item in requests)
    assert all(item.runtime_mode is RuntimeMode.OWNER_SELF_DOGFOOD for item in requests)
    assert all(item.enrollment.external_llm_executed is False for item in requests)
    assert all(item.run_binding.expected_initial_state is WorkflowState.READY for item in requests)
    assert all(item.run_binding.expected_initial_state_version == 1 for item in requests)
    assert len({item.configuration_fingerprints.composition_sha256 for item in requests}) == 1
    assert all(len(item.request_fingerprint) == 64 for item in requests)
    assert all(item.owners is owners for item in prepared_drivers)
    assert all(
        item.owners.materializer_factory is owners.materializer_factory
        and item.owners.agent_execution_service_factory is owners.agent_execution_service_factory
        for item in prepared_drivers
    )
    assert all(
        item.attempt_binding.request_fingerprint == item.request.request_fingerprint
        and item.attempt_binding.run_binding_fingerprint
        == item.request.run_binding.binding_fingerprint
        and item.attempt_binding.configuration_fingerprint
        == item.request.configuration_fingerprints.composition_sha256
        for item in prepared_drivers
    )
    with pytest.raises(FrozenInstanceError):
        prepared_drivers[0].attempt_binding.attempt_id = "foreign"  # type: ignore[misc]

    s1, s2, s3, s4 = requests
    assert (s1.tool_id, s1.tool_action) == (
        "stockroom_summary",
        "fixed-stockroom-summary",
    )
    assert s2.tool_id == "stockroom_summary"
    assert s2.enrollment.suppress_summary_evidence_candidate is True
    assert s2.enrollment.same_run_automatic_retry is False
    assert {item.requirement_id for item in s2.evidence_descriptors} == {"summary-runtime"}
    assert s3.tool_id is None and s3.tool_action is None
    assert {item.proof_type for item in s3.evidence_descriptors} == {"STATIC_SOURCE"}
    assert s4.tool_id == "stockroom_summary"
    assert s4.human_descriptor is not None
    assert (
        s4.human_descriptor.ownership,
        s4.human_descriptor.producer,
        s4.human_descriptor.status,
    ) == ("HUMAN_OWNED", "HUMAN_P1_7", "HUMAN_PENDING")
    assert s4.enrollment.human_result is None
    assert all(item.enrollment.admitted_evidence == () for item in requests)
    assert all(item.enrollment.judgment is None for item in requests)
    assert reached == [
        "owner_dependency_construction",
        "owner_composition_creation",
        "bootstrap_owner_preparation",
        "S1_request_preparation",
        "S2_request_preparation",
        "S3_request_preparation",
        "S4_request_preparation",
    ]
    assert calls and all(count == 0 for count in calls.values())


def _profiles_with_timeout(value: float | int) -> MappingProxyType:
    composed = build_stockroom_owner_composition()
    return MappingProxyType(
        {
            profile_id: replace(
                local,
                profile=replace(local.profile, total_timeout_seconds=value),
            )
            for profile_id, local in composed.provider_profiles.items()
        }
    )


def test_provider_timeout_fingerprint_uses_exact_integer_seconds() -> None:
    composed = build_stockroom_owner_composition()
    whole_float = composition_module._fingerprints(
        composed.catalog,
        _profiles_with_timeout(30.0),
        composed.tool_config,
        composed.security_config,
    )
    whole_integer = composition_module._fingerprints(
        composed.catalog,
        _profiles_with_timeout(30),
        composed.tool_config,
        composed.security_config,
    )

    assert whole_float == whole_integer == composed.fingerprints
    assert all(
        len(value) == 64 and value == value.lower() and set(value) <= set("0123456789abcdef")
        for value in (
            whole_float.provider_profiles_sha256,
            whole_float.composition_sha256,
        )
    )


@pytest.mark.parametrize("value", [29.5, float("nan"), float("inf"), float("-inf")])
def test_provider_timeout_fingerprint_denies_non_integral_or_non_finite(
    value: float,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    composed = build_stockroom_owner_composition()
    profiles = _profiles_with_timeout(value)
    with pytest.raises(
        composition_module.StockroomCompositionError,
        match="STOCKROOM_COMPOSITION_BINDING_DENIED",
    ):
        composition_module._fingerprints(
            composed.catalog,
            profiles,
            composed.tool_config,
            composed.security_config,
        )

    monkeypatch.setattr(
        composition_module,
        "load_stockroom_owner_profiles",
        lambda path: profiles,
    )
    with pytest.raises(
        composition_module.StockroomCompositionError,
        match="STOCKROOM_COMPOSITION_BINDING_DENIED",
    ):
        build_stockroom_owner_composition()


def _v2_evidence_fixture(version="v2"):
    from aiscc.evidence.issuers import TokenEvidenceIssuer
    from aiscc.evidence.models import EvidenceIssuerType
    from aiscc.evidence.requirements import TaskContractEvidenceAuthority
    from aiscc.scenarios.stockroom_production import (
        _RUNTIME_ISSUER_ID,
        _STATIC_ISSUER_ID,
        _build_evidence_enrollment,
        load_stockroom_evidence_config,
    )

    raw = load_stockroom_evidence_config(
        Path(__file__).resolve().parents[3] / f"config/evidence/stockroom-capture.{version}.json"
    )
    authority = TaskContractEvidenceAuthority(raw["authority_id"], raw["authority_version"])
    runtime = TokenEvidenceIssuer(
        EvidenceIssuerType.SYSTEM_RUNTIME_OBSERVATION, _RUNTIME_ISSUER_ID, "v1"
    )
    static = TokenEvidenceIssuer(EvidenceIssuerType.SYSTEM_STATIC_PROOF, _STATIC_ISSUER_ID, "v1")
    return (
        raw,
        authority,
        tuple(
            _build_evidence_enrollment(
                item, authority, raw["durable_policy_fingerprint"], runtime, static
            )
            for item in raw["enrollments"]
        ),
    )


def _v2_authority_rows(enrollment):
    from datetime import UTC
    from types import SimpleNamespace

    from aiscc.evidence.repository import _checkpoint_row, _requirement_row, _set_row

    checkpoint, requirement, requirement_set = (
        enrollment.checkpoint,
        enrollment.requirement,
        enrollment.requirement_set,
    )
    rows = (_checkpoint_row(checkpoint), _requirement_row(requirement), _set_row(requirement_set))
    for row in rows:
        row.issued_at = row.issued_at.astimezone(UTC)
    request = SimpleNamespace(
        **{
            key: getattr(checkpoint, key)
            for key in (
                "task_contract_id",
                "task_contract_version",
                "source_state",
                "target_state",
                "transition_purpose_id",
                "transition_purpose_version",
                "requirement_set_id",
                "requirement_set_version",
            )
        },
        checkpoint_ref=checkpoint.ref,
    )

    class RowsOnlySession:
        async def get(self, model, key):
            for row in rows:
                if isinstance(row, model):
                    primary = next(iter(model.__table__.primary_key)).name
                    return row if getattr(row, primary) == key else None
            raise AssertionError("unexpected authority model")

        async def scalars(self, statement):
            assert set(statement.compile().params.values()) == {rows[2].requirement_set_ref}
            return (rows[1],)

    return rows, request, RowsOnlySession()


def test_v2_config_selection_and_policy_scope_preserve_v1():
    import hashlib
    import json

    from aiscc.scenarios.stockroom_production import _load_stockroom_fresh_authority_configs

    root = Path(__file__).resolve().parents[3]
    before = (root / "config/evidence/stockroom-capture.v1.json").read_bytes()
    assert hashlib.sha256(before).hexdigest() == (
        "70d4dbf219d54abd57877b787d8ac16d0efbe05701e7fb8bf1f84282640b31e7"
    )
    old_raw, _, old = _v2_evidence_fixture("v1")
    new_raw, _, new = _v2_evidence_fixture()
    assert (old_raw["authority_id"], old_raw["authority_version"]) != (
        new_raw["authority_id"],
        new_raw["authority_version"],
    )
    old_json = json.loads(before)
    new_json = json.loads((root / "config/evidence/stockroom-capture.v2.json").read_bytes())
    changed = {
        "task_contract_version",
        "requirement_set_version",
        "requirement_version",
        "checkpoint_version",
        "issued_at",
    }
    for legacy, fresh in zip(old_json["enrollments"], new_json["enrollments"], strict=True):
        assert {k: v for k, v in legacy.items() if k not in changed} == {
            k: v for k, v in fresh.items() if k not in changed
        }
    assert old_json["durable_content_policy"] == new_json["durable_content_policy"]
    for legacy, fresh in zip(old, new, strict=True):
        old_rows, _, _ = _v2_authority_rows(legacy)
        new_rows, _, _ = _v2_authority_rows(fresh)
        for lhs, rhs in zip(old_rows, new_rows, strict=True):
            key = next(iter(type(lhs).__table__.primary_key)).name
            assert getattr(lhs, key) != getattr(rhs, key)
            assert lhs.fingerprint != rhs.fingerprint
        assert legacy.requirement.task_contract_version == "1.0.0"
        assert fresh.requirement.task_contract_version == "2.0.0"
    evidence, human, judgment = _load_stockroom_fresh_authority_configs(root)
    assert evidence == new_raw
    assert human["required_use"]["task_contract_version"] == "2.0.0"
    for policy, enrollment in zip(judgment["policies"], new[:2], strict=True):
        assert policy["policy_version"] == "stockroom-judgment-v3-evidence-v2"
        assert policy["task_contract_version"] == "2.0.0"
        assert policy["evidence_checkpoint_ref"] == enrollment.checkpoint.ref.serialized()
        assert policy["evidence_requirement_set_ref"].endswith("@v2")
    assert (root / "config/evidence/stockroom-capture.v1.json").read_bytes() == before


@pytest.mark.parametrize("scenario_index", range(4))
def test_v2_real_row_roundtrip_and_historical_graph(scenario_index):
    from aiscc.evidence.models import canonical_hash
    from aiscc.evidence.repository import (
        _checkpoint_from_row,
        _historical_authority_graph,
        _requirement_from_row,
        _set_from_row,
    )
    from aiscc.evidence.requirements import _checkpoint_payload, _requirement_payload, _set_payload

    enrollment = _v2_evidence_fixture()[2][scenario_index]
    rows, request, session = _v2_authority_rows(enrollment)
    for row, decode, payload in zip(
        rows,
        (_checkpoint_from_row, _requirement_from_row, _set_from_row),
        (_checkpoint_payload, _requirement_payload, _set_payload),
        strict=True,
    ):
        assert row.fingerprint == canonical_hash(payload(decode(row)))
    checkpoint, requirement_set, requirements = asyncio.run(
        _historical_authority_graph(session, request)
    )
    assert checkpoint == enrollment.checkpoint
    assert requirement_set == enrollment.requirement_set
    assert requirements == (enrollment.requirement,)


@pytest.mark.parametrize("row_index", range(3))
@pytest.mark.parametrize("mutation", ["instant", "semantic", "identity", "parent", "hash"])
def test_v2_historical_graph_integrity_denies(row_index, mutation):
    from datetime import timedelta

    from aiscc.evidence.models import EvidenceAuthorityConflictError
    from aiscc.evidence.repository import _historical_authority_graph

    rows, request, session = _v2_authority_rows(_v2_evidence_fixture()[2][0])
    row = rows[row_index]
    if mutation == "instant":
        row.issued_at += timedelta(seconds=1)
    elif mutation == "semantic":
        if row_index == 1:
            row.payload = {**row.payload, "scope_id": "wrong-scope"}
        else:
            row.task_contract_version = "wrong-task-version"
    elif mutation == "identity":
        key = next(iter(type(row).__table__.primary_key)).name
        setattr(row, key, getattr(row, key) + "-wrong")
    elif mutation == "parent":
        if row_index == 2:
            row.requirement_root_hash = "f" * 64
        else:
            row.requirement_set_ref = "wrong-parent@v2"
    else:
        row.fingerprint = "f" * 64
    with pytest.raises(EvidenceAuthorityConflictError):
        asyncio.run(_historical_authority_graph(session, request))


@pytest.mark.parametrize(
    "mutation", ["offset", "z", "naive", "legacy-ref", "legacy-task", "authority"]
)
def test_v2_loader_rejects_noncanonical_scope(tmp_path, mutation):
    import json

    from aiscc.scenarios.stockroom_production import load_stockroom_evidence_config

    root = Path(__file__).resolve().parents[3]
    value = json.loads((root / "config/evidence/stockroom-capture.v2.json").read_bytes())
    if mutation == "authority":
        value["authority"]["authority_version"] = "v1"
    else:
        key, changed = {
            "offset": ("issued_at", "2026-09-10T18:24:00+09:00"),
            "z": ("issued_at", "2026-09-10T09:24:00Z"),
            "naive": ("issued_at", "2026-09-10T09:24:00"),
            "legacy-ref": ("checkpoint_version", "v1"),
            "legacy-task": ("task_contract_version", "1.0.0"),
        }[mutation]
        value["enrollments"][0][key] = changed
    path = tmp_path / "malformed-v2.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    with pytest.raises(ValueError):
        load_stockroom_evidence_config(path)


@pytest.fixture
def local_authority_sessions():
    """In-memory row adapter, not PostgreSQL/DDL/concurrency evidence.

    Run the real repository SQL/owner functions on local SQLite projections.
    PostgreSQL-only CHECK/sequence/advisory-lock mechanics are simulated here;
    application verification, identities, hashes and owner capabilities are not mocked.
    """
    from collections import defaultdict
    from contextlib import asynccontextmanager
    from datetime import UTC, datetime

    from sqlalchemy import CheckConstraint, MetaData, create_engine, event
    from sqlalchemy.dialects.postgresql import JSONB
    from sqlalchemy.ext.compiler import compiles, deregister
    from sqlalchemy.orm import Session
    from sqlalchemy.orm.attributes import set_committed_value

    from aiscc.persistence.models import Base

    @compiles(JSONB, "sqlite")
    def jsonb_type(element, compiler, **kwargs):
        return "JSON"

    engine = create_engine("sqlite:///:memory:")
    metadata = MetaData()
    for table in Base.metadata.sorted_tables:
        clone = table.to_metadata(metadata)
        for constraint in tuple(clone.constraints):
            if isinstance(constraint, CheckConstraint):
                clone.constraints.remove(constraint)
        for column in clone.columns:
            column.identity = None
            column.server_default = None
    metadata.create_all(engine)
    sequences = defaultdict(int)

    class LocalSession(Session):
        pass

    @event.listens_for(LocalSession, "loaded_as_persistent")
    def normalize_utc(session, instance):
        for column in instance.__table__.columns:
            value = getattr(instance, column.name)
            if isinstance(value, datetime) and value.tzinfo is None:
                set_committed_value(instance, column.name, value.replace(tzinfo=UTC))

    @event.listens_for(LocalSession, "before_flush")
    def identity_columns(session, flush_context, instances):
        for item in session.new:
            for column in item.__table__.columns:
                if column.identity is not None and getattr(item, column.name) is None:
                    key = (item.__tablename__, column.name)
                    sequences[key] += 1
                    setattr(item, column.name, sequences[key])

    class AsyncRows:
        def __init__(self):
            self.session = LocalSession(engine, expire_on_commit=False)

        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc):
            self.session.close()

        @asynccontextmanager
        async def begin(self):
            with self.session.begin():
                yield self

        async def get(self, model, key, **kwargs):
            return self.session.get(model, key, **kwargs)

        async def scalar(self, statement, *args, **kwargs):
            return self.session.scalar(statement, *args, **kwargs)

        async def scalars(self, statement, *args, **kwargs):
            return self.session.scalars(statement, *args, **kwargs)

        async def execute(self, statement, *args, **kwargs):
            if str(statement).startswith("SELECT pg_advisory_xact_lock("):
                return None
            return self.session.execute(statement, *args, **kwargs)

        def add(self, value):
            self.session.add(value)

        def add_all(self, values):
            self.session.add_all(values)

        async def flush(self):
            self.session.flush()

        async def refresh(self, value):
            self.session.refresh(value)
            normalize_utc(self.session, value)

    try:
        yield AsyncRows
    finally:
        engine.dispose()
        deregister(JSONB)


def test_v2_real_registration_coexists_with_v1(local_authority_sessions):
    from sqlalchemy import select

    from aiscc.evidence.repository import PostgresEvidenceRepository
    from aiscc.persistence.models import (
        EvidenceAuthorityEventRow,
        EvidenceCheckpointRow,
        EvidenceRequirementRow,
        EvidenceRequirementSetRow,
    )

    async def check():
        repository = PostgresEvidenceRepository(local_authority_sessions)
        snapshots = []
        for version in ("v1", "v2", "v2"):
            _, authority, enrollments = _v2_evidence_fixture(version)
            for enrollment in enrollments:
                await repository.register_authority(
                    requirement_set=enrollment.requirement_set,
                    requirements=(enrollment.requirement,),
                    checkpoints=(enrollment.checkpoint,),
                    authority=authority,
                )
            async with local_authority_sessions() as session:
                snapshot = {}
                for model in (
                    EvidenceRequirementSetRow,
                    EvidenceRequirementRow,
                    EvidenceCheckpointRow,
                ):
                    rows = await session.scalars(select(model))
                    key = next(iter(model.__table__.primary_key)).name
                    snapshot[model.__name__] = {getattr(row, key): row.fingerprint for row in rows}
                snapshots.append(snapshot)
                assert not list(await session.scalars(select(EvidenceAuthorityEventRow)))
        for model, legacy in snapshots[0].items():
            assert len(legacy) == 4 and len(snapshots[1][model]) == 8
            assert legacy.items() <= snapshots[1][model].items()
        assert snapshots[1] == snapshots[2]

    asyncio.run(check())


def test_v2_local_s1_owner_guard_handoff_accepts(local_authority_sessions):
    """Fake execution/storage edges; real P1-6/P1-7 owners and P1-4 kernel.

    Does not prove PostgreSQL locking/DDL or provider/runtime provenance. The
    deterministic execution output is explicitly supplied at the local fake boundary.
    """
    from datetime import UTC, datetime
    from types import SimpleNamespace

    from sqlalchemy import func, select

    from aiscc.evidence.admission import EvidenceAdmissionEvaluator, EvidenceContentRegistry
    from aiscc.evidence.attestation import EvidenceCheckpointUseRegistry, EvidenceGuardAuthority
    from aiscc.evidence.content import P1_6DurableContentAuthority
    from aiscc.evidence.issuers import EvidenceIssuerRegistry
    from aiscc.evidence.repository import PostgresEvidenceRepository
    from aiscc.evidence.set_evaluator import EvidenceSetEvaluator
    from aiscc.human.authority import HumanGateReservationAuthority, HumanGuardAuthority
    from aiscc.judgment.authority import JudgmentPolicyAuthority
    from aiscc.persistence.models import (
        AdmittedEvidenceRow,
        HumanGuardAttestationRow,
        JudgmentGuardAttestationRow,
        JudgmentRow,
    )
    from aiscc.persistence.repository import PostgresTransitionRepository
    from aiscc.providers.authority import ExecutionReferenceAuthority
    from aiscc.providers.local_deterministic import STOCKROOM_SUMMARY
    from aiscc.providers.models import ExecutionStatus, ExecutionSubmissionRef
    from aiscc.scenarios.capture_runner import StockroomCaptureRunner
    from aiscc.scenarios.driver import StockroomCaptureStatus
    from aiscc.scenarios.stockroom_production import (
        StockroomCaptureOwnerAdapter,
        _load_stockroom_fresh_authority_configs,
    )
    from aiscc.workflow.evaluator import TransitionEvaluator
    from aiscc.workflow.guards import GUARD_OWNER_POLICY, P1_4GuardAuthority
    from aiscc.workflow.matrix import TRANSITION_MATRIX
    from aiscc.workflow.models import GuardId, GuardSemanticOwner
    from tests.unit.scenarios.test_stockroom_capture_runner import RecordingOwners, prepared_driver

    async def check():
        root = Path(__file__).resolve().parents[3]
        _, human_config, judgment_config = _load_stockroom_fresh_authority_configs(root)
        _, authority, enrollments = _v2_evidence_fixture()
        enrollment = enrollments[0]

        def now():
            return datetime.now(UTC)

        content = P1_6DurableContentAuthority()
        evidence = PostgresEvidenceRepository(
            local_authority_sessions, durable_content_authority=content
        )
        for item in enrollments:
            await evidence.register_authority(
                requirement_set=item.requirement_set,
                requirements=(item.requirement,),
                checkpoints=(item.checkpoint,),
                authority=authority,
            )
        uses = EvidenceCheckpointUseRegistry(tuple(item.checkpoint for item in enrollments))
        evidence_guard = EvidenceGuardAuthority(evidence, uses)
        human_repository = PostgresHumanAuthorityRepository(local_authority_sessions, clock=now)
        use = human_config["required_use"]
        reservation = HumanGateReservationAuthority(
            frozenset(
                {
                    (
                        use["task_contract_id"],
                        use["task_contract_version"],
                        use["source_state"],
                        use["target_state"],
                    )
                }
            ),
            authority_policy_ref=human_config["authority_policy_ref"],
            authority_policy_version=human_config["authority_policy_version"],
        )
        human = HumanGuardAuthority(
            local_authority_sessions, human_repository, evidence, uses, reservation, clock=now
        )
        policy_authority = JudgmentPolicyAuthority(
            local_authority_sessions,
            clock=lambda: judgment_config["issued_at"],
            authority_version=judgment_config["authority_version"],
        )
        policy = await policy_authority.register(
            **{
                k: v
                for k, v in judgment_config["policies"][0].items()
                if k not in {"scenario_id", "scenario_version"}
            }
        )
        judgment = PostgresJudgmentAuthority(
            local_authority_sessions, evidence, policy_authority, clock=now
        )
        system = P1_4GuardAuthority()
        repository = PostgresTransitionRepository(
            local_authority_sessions, TransitionEvaluator(system, (evidence_guard, human, judgment))
        )
        kernel = WorkflowKernel(repository)
        issuer = enrollment.issuer
        service = EvidenceAdmissionService(
            evidence,
            EvidenceAdmissionEvaluator(
                EvidenceIssuerRegistry((issuer,)), EvidenceContentRegistry(())
            ),
            durable_content_authority=content,
        )
        app = SimpleNamespace(
            project_id="local-v2-test",
            requester_identity="local-v2-test",
            clock=now,
            workflow_kernel=kernel,
            p1_4_guard_authority=system,
            evidence_enrollments={item.scenario_id: item for item in enrollments},
            evidence_service=service,
            durable_content_authority=content,
            evidence_set_evaluator=EvidenceSetEvaluator(evidence),
            evidence_guard_authority=evidence_guard,
            human_guard_authority=human,
            judgment_authority=judgment,
            judgment_enrollments={enrollment.scenario_id: SimpleNamespace(policy=policy)},
        )
        prepared = prepared_driver(SCENARIO_IDS[0])
        adapter = StockroomCaptureOwnerAdapter(
            app,
            SimpleNamespace(prepared=prepared),
            SimpleNamespace(value=None),
            SimpleNamespace(current=None, attempt=None),
        )
        execution_authority = ExecutionReferenceAuthority()

        class LocalOwners(RecordingOwners):
            async def initial_ready(self, value):
                return await adapter.initial_ready(value)

            async def request_transition(
                self, value, *, target, observed_state, observed_version, authority_refs
            ):
                if target is WorkflowState.ACCEPTED:
                    result = await adapter.request_transition(
                        value,
                        target=target,
                        observed_state=observed_state,
                        observed_version=observed_version,
                        authority_refs=authority_refs,
                    )
                else:
                    request = adapter._request(value, observed_state, observed_version, target)
                    facts = []
                    for guard in TRANSITION_MATRIX[(observed_state, target)]:
                        assert GUARD_OWNER_POLICY[guard] is GuardSemanticOwner.P1_4_SYSTEM
                        if guard is GuardId.G_EXECUTOR_SUBMISSION:
                            ref = execution_authority.register_submission(
                                ExecutionSubmissionRef(
                                    submission_id="local-fake-submission",
                                    execution_attempt_id="attempt-1",
                                    work_run_id=request.work_run_id,
                                    task_contract_id=request.task_contract_id,
                                    task_contract_version=request.task_contract_version,
                                    state=observed_state,
                                    state_version=observed_version,
                                    status=ExecutionStatus.EXECUTOR_COMPLETED,
                                    event_range_hash="a" * 64,
                                    issuer_ref=execution_authority.issuer_ref,
                                )
                            )
                            facts.append(
                                system.issue_from_execution_ref(
                                    guard_id=guard,
                                    execution_ref=ref,
                                    verifier=execution_authority,
                                    request=request,
                                )
                            )
                        else:
                            facts.append(
                                system.issue(
                                    guard_id=guard,
                                    satisfied=True,
                                    reason="LOCAL_FAKE_EXECUTION_BOUNDARY",
                                    authority_ref=f"local-fake:{guard.value}",
                                    request=request,
                                )
                            )
                    decision = await kernel.request_transition(request, tuple(facts))
                    adapter._handles[decision.transition_decision_id] = decision
                    result = await adapter._transition_result(decision, request)
                self.version = result.state_version
                return result

            async def submit_runtime_evidence(self, value, execution_ref):
                assert (
                    adapter._handles[execution_ref].resulting_state
                    is WorkflowState.ADMISSION_PENDING
                )
                ref = await adapter._submit_durable_candidate(
                    value,
                    enrollment,
                    issuer,
                    value=STOCKROOM_SUMMARY,
                    producer_attestation_ref="local-fake:deterministic-summary",
                    execution_attempt_id=None,
                    operation_id=None,
                )
                return await adapter._snapshot_result(value, "ADMITTED", ref)

            async def evaluate_evidence(self, value, candidate_ref):
                result = await adapter.evaluate_evidence(value, candidate_ref)
                assert result.status == "SATISFIED", result
                return result

            async def issue_judgment(self, value, *, judgment_status, evidence_ref):
                result = await adapter.issue_judgment(
                    value, judgment_status=judgment_status, evidence_ref=evidence_ref
                )
                assert result.status == "ADMITTED", result
                from aiscc.workflow.models import DecisionOutcome

                pending = adapter._pending_requests[WorkflowState.ACCEPTED]
                raw_only = replace(
                    pending, transition_request_id=pending.transition_request_id + "-raw-only"
                )
                evidence_fact = await evidence_guard.issue_for_transition(raw_only)
                denied = await kernel.request_transition(raw_only, (evidence_fact,))
                assert denied.outcome is DecisionOutcome.DENIED
                assert (await kernel.load("run-1")).state is WorkflowState.ADMISSION_PENDING
                return result

        result = await StockroomCaptureRunner(LocalOwners()).run(prepared)
        assert result.status is StockroomCaptureStatus.COMPLETED, result
        assert (result.workflow_state, result.state_version) == (WorkflowState.ACCEPTED, 4)
        current = await kernel.verify_consistency("run-1")
        assert current.task_contract_version == "2.0.0"
        assert current.state is WorkflowState.ACCEPTED
        async with local_authority_sessions() as session:
            for model in (
                AdmittedEvidenceRow,
                JudgmentRow,
                HumanGuardAttestationRow,
                JudgmentGuardAttestationRow,
            ):
                assert await session.scalar(select(func.count()).select_from(model)) == 1

    asyncio.run(check())
