from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from aiscc.contracts.security import (
    AuthorityStatus,
    PermissionRequest,
    ResourceDomain,
    ResourceScope,
    SecurityActionClass,
    SecurityAdmissionDecision,
)
from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot, WorkflowState
from aiscc.public_live.initializer import InitializerSettings
from aiscc.public_live.start_authority import (
    PublicLiveStartCandidate,
    PublicLiveStartContextAuthority,
    StartContract,
)
from aiscc.security.policy import SecurityPolicy, default_profiles


def candidate(contract: StartContract) -> PublicLiveStartCandidate:
    now = datetime.now(UTC)
    return PublicLiveStartCandidate(
        b"r" * 16,
        "public-live-v1",
        4,
        now,
        now + timedelta(seconds=90),
        "idem-ref",
        "a" * 64,
        "reserve-ref",
        1,
        "opaque-requester",
        "b" * 64,
        "c" * 64,
        contract.digest,
    )


def test_fixed_manifest_candidate_and_single_use_ready_authority() -> None:
    contract = StartContract.load()
    value = candidate(contract)
    assert value.work_run_id == "public-live-" + (b"r" * 16).hex()
    assert value.candidate_id(contract) == value.candidate_id(contract)
    authority = PublicLiveStartContextAuthority(contract, principal="aiscc-public-live-initializer")
    now = value.admitted_at + timedelta(seconds=1)
    receipt = authority.issue(value, state=WorkflowState.READY, state_version=1, now=now)
    authority.consume(receipt, now=now)
    with pytest.raises(ValueError, match="ALREADY_CONSUMED"):
        authority.consume(receipt, now=now)
    with pytest.raises(ValueError, match="START_CONTEXT_DENIED"):
        authority.issue(value, state=WorkflowState.RUNNING, state_version=2, now=now)


def test_initializer_environment_excludes_owner_provider_and_worker_credentials() -> None:
    good = {"AISCC_PUBLIC_LIVE_START_DATABASE_URL": "postgresql+asyncpg://start@db/live"}
    assert InitializerSettings.from_environment(good).database_url.endswith("/live")
    for key in (
        "AISCC_DATABASE_URL",
        "AISCC_OPENAI_API_KEY",
        "OPENAI_API_KEY",
        "AISCC_PUBLIC_LIVE_DATABASE_URL",
    ):
        with pytest.raises(ValueError, match="FORBIDDEN_AUTHORITY"):
            InitializerSettings.from_environment(good | {key: "presence-only"})


def test_ready_start_repository_and_scenario_admission_is_exact() -> None:
    contract = StartContract.load()
    value = candidate(contract)
    now = value.admitted_at + timedelta(seconds=1)
    authority = PublicLiveStartContextAuthority(contract, principal="aiscc-public-live-initializer")
    receipt = authority.issue(value, state=WorkflowState.READY, state_version=1, now=now)
    current = WorkflowSnapshot(value.work_run_id, WorkflowState.READY, 1)
    policy = SecurityPolicy(default_profiles(), public_context_policy=authority)
    scopes = (
        ResourceScope(
            ResourceDomain.REPOSITORY,
            f"{contract.payload['repository_identity']}@{contract.payload['repository_version']}",
        ),
        ResourceScope(
            ResourceDomain.SCENARIO,
            f"scenario:{contract.payload['scenario_id']}@{contract.payload['scenario_version']}",
        ),
    )
    for scope in scopes:
        context = authority.issue_resource_context(receipt, current=current, scope=scope)
        grant = policy.issue_resource_grant(
            mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
            profile_version="p1-3-v2",
            scenario_id="stockroom-s1-normal",
            principal="aiscc-public-live-initializer",
            run_id=value.work_run_id,
            action=SecurityActionClass.START_EXECUTION_CONTROL,
            scope=scope,
            ttl_seconds=10,
            selector_request=context,
            operation_fingerprint=receipt.operation_fingerprint,
            stockroom_context=context,
            now=now,
        )
        assert grant is not None
        request = PermissionRequest(
            principal="aiscc-public-live-initializer",
            run_id=value.work_run_id,
            mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
            observed=current,
            authoritative=current,
            action=SecurityActionClass.START_EXECUTION_CONTROL,
            resource_scope=scope,
            resource_grant=grant,
            profile_version="p1-3-v2",
            scenario_id="stockroom-s1-normal",
            requester_authority=AuthorityStatus.GRANTED,
            task_scope_authority=AuthorityStatus.GRANTED,
            limit_authority=AuthorityStatus.GRANTED,
            budget_authority=AuthorityStatus.GRANTED,
            idempotency_authority=AuthorityStatus.GRANTED,
            target_control_authority=AuthorityStatus.NOT_APPLICABLE,
        )
        assert policy.evaluate(request).decision is SecurityAdmissionDecision.ALLOW
