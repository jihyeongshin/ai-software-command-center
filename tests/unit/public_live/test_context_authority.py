from dataclasses import replace

import pytest

from aiscc.contracts.security import ResourceDomain, ResourceScope, SecurityActionClass
from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot, WorkflowState
from aiscc.public_live.context_authority import PublicLiveContextResourceAuthority
from aiscc.public_live.luna_profile import hosted_luna_profile


def setup():
    profile = hosted_luna_profile()
    current = WorkflowSnapshot("run", WorkflowState.RUNNING, 2)
    owner = PublicLiveContextResourceAuthority(
        profile=profile, current=current, attempt="attempt", principal="owner"
    )
    args = dict(
        current=current,
        mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
        principal="owner",
        scenario_id="stockroom-s1-normal",
        scope=ResourceScope(ResourceDomain.REPOSITORY, profile.public_repository_resource_identity),
        action=SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        fingerprint="a" * 64,
        execution_attempt_id="attempt",
        provider_profile_id=profile.profile_id,
        provider_profile_version=profile.version,
    )
    return owner, args


@pytest.mark.parametrize(
    "field,value",
    [
        ("mode", RuntimeMode.OWNER_SELF_DOGFOOD),
        ("mode", RuntimeMode.PUBLIC_RECORDED_REPLAY),
        ("principal", "other"),
        ("execution_attempt_id", "other"),
        ("provider_profile_id", "other"),
        ("provider_profile_version", "2"),
        ("scenario_id", "other"),
        ("action", SecurityActionClass.REPLAY_READ_ONLY),
        ("current", WorkflowSnapshot("run", WorkflowState.RUNNING, 3)),
        ("current", WorkflowSnapshot("other", WorkflowState.RUNNING, 2)),
        ("current", WorkflowSnapshot("run", WorkflowState.READY, 2)),
        ("fingerprint", "lookalike"),
    ],
)
def test_wrong_context_denied(field, value):
    owner, args = setup()
    args[field] = value
    with pytest.raises(ValueError):
        owner.issue(**args)


@pytest.mark.parametrize(
    "identity",
    [
        "repository:owner-private",
        "repository:synthetic-stockroom",
        "repository:synthetic-stockroom@2",
        "https://example.com/repo",
        "scenario:stockroom-s1-normal@2",
    ],
)
def test_alternate_resource_denied(identity):
    owner, args = setup()
    args["scope"] = ResourceScope(ResourceDomain.REPOSITORY, identity)
    with pytest.raises(ValueError):
        owner.issue(**args)


@pytest.mark.parametrize("domain", [ResourceDomain.REPOSITORY, ResourceDomain.SCENARIO])
def test_exact_grant_and_missing_owner_denial(domain):
    from aiscc.public_live.provider_authority import luna_permission_profiles
    from aiscc.security.policy import SecurityPolicy

    owner, args = setup()
    profile = hosted_luna_profile()
    identity = (
        profile.public_repository_resource_identity
        if domain is ResourceDomain.REPOSITORY
        else profile.public_scenario_resource_identity
    )
    args["scope"] = ResourceScope(domain, identity)
    token = owner.issue(**args)
    kwargs = dict(
        mode=args["mode"],
        profile_version="p1-3-v2",
        scenario_id=args["scenario_id"],
        principal="owner",
        run_id="run",
        action=args["action"],
        scope=args["scope"],
        operation_fingerprint=args["fingerprint"],
        selector_request=token,
        stockroom_context=token,
    )
    policy = SecurityPolicy(luna_permission_profiles(), public_context_policy=owner)
    assert policy.issue_resource_grant(**kwargs) is not None
    assert SecurityPolicy(luna_permission_profiles()).issue_resource_grant(**kwargs) is None
    assert not owner.current_matches(token, WorkflowSnapshot("run", WorkflowState.RUNNING, 3))
    kwargs["selector_request"] = replace(token)
    assert policy.issue_resource_grant(**kwargs) is None


@pytest.mark.parametrize(
    "field,value",
    [
        ("profile_id", "other"),
        ("version", "2"),
        ("public_scenario_version", "2"),
        ("public_repository_version", "2"),
    ],
)
def test_modified_server_profile_denied(field, value):
    with pytest.raises(ValueError):
        PublicLiveContextResourceAuthority(
            profile=replace(hosted_luna_profile(), **{field: value}),
            current=WorkflowSnapshot("run", WorkflowState.RUNNING, 2),
            attempt="attempt",
            principal="owner",
        )
