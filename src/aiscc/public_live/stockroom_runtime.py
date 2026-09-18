"""Fixed brokered Stockroom runtime composition for the Public Live worker."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from aiscc.contracts.security import ResourceDomain, SecurityActionClass
from aiscc.contracts.workflow import RuntimeMode
from aiscc.providers.local_deterministic import STOCKROOM_SUMMARY
from aiscc.providers.models import (
    ProviderProfile,
    ToolDefinition,
    ToolOutputRef,
    ToolRegistry,
    canonical_json_bytes,
    canonical_sha256,
)
from aiscc.providers.tools import KnownToolFailure, ToolDispatchContext, UnknownToolOutcome
from aiscc.public_live.luna_profile import luna_tool_registry
from aiscc.public_live.provider_authority import PublicLiveFixedToolScopeAuthority
from aiscc.scenarios.models import RESOURCE_REF
from aiscc.security.capability import CapabilityConsumeRequest, CapabilityConsumptionReceipt
from aiscc.security.policy import SecurityPolicy

PUBLIC_FIXED_STOCKROOM_IMPLEMENTATION_FINGERPRINT = canonical_sha256(
    {
        "contract": "AISCC-PUBLIC-LIVE-FIXED-STOCKROOM-V1",
        "runtime_mode": RuntimeMode.PUBLIC_BOUNDED_LIVE.value,
        "scenario": "stockroom-s1-normal@1.0.0",
        "profile": "public-live-luna-v1@1",
        "tool": "aiscc-stockroom-tools:2:stockroom_summary:1:stockroom-summary-v1",
        "arguments": {},
        "result_hash": canonical_sha256(STOCKROOM_SUMMARY),
        "resource_domains": [ResourceDomain.TOOL.value],
        "subprocess": False,
        "filesystem": False,
        "network": False,
        "secret": False,
    }
)
_TOOL_RESOURCE_IDENTITY = "aiscc-stockroom-tools:2:stockroom_summary:1:stockroom-summary-v1"
_ALLOWED_RECEIPT_DOMAINS = frozenset(
    {ResourceDomain.TOOL, ResourceDomain.REPOSITORY, ResourceDomain.SCENARIO}
)


class PublicLiveFixedStockroomDispatcher:
    """Receipt-entered deterministic dispatcher with no ambient I/O dependency."""

    def __init__(self, policy: SecurityPolicy) -> None:
        self._policy = policy
        self.invocation_count = 0
        self.last_consumed_domains: tuple[ResourceDomain, ...] = ()

    def dispatch(self, *args: object, **kwargs: object) -> ToolOutputRef:
        del args, kwargs
        raise ValueError("PUBLIC_STOCKROOM_LEGACY_DISPATCH_DENIED")

    def dispatch_with_receipts(
        self,
        definition: ToolDefinition,
        arguments: dict[str, object],
        *,
        receipts: tuple[CapabilityConsumptionReceipt, ...],
        requirements: tuple[CapabilityConsumeRequest, ...],
        dispatch_identity: str,
    ) -> ToolOutputRef:
        if (
            arguments != {}
            or definition.tool_id != "stockroom_summary"
            or definition.schema_version != "1"
            or definition.dispatcher_version != "stockroom-summary-v1"
            or definition.underlying_resource_requirements
            or definition.secret_requirement is not None
        ):
            raise KnownToolFailure("PUBLIC_STOCKROOM_CONTRACT_DENIED")
        if (
            not receipts
            or len(receipts) != len(requirements)
            or len(dispatch_identity) != 64
            or any(character not in "0123456789abcdef" for character in dispatch_identity)
        ):
            raise UnknownToolOutcome("PUBLIC_STOCKROOM_RECEIPT_UNRESOLVED")
        pairs = tuple(zip(receipts, requirements, strict=True))
        domains = tuple(requirement.scope.domain for _, requirement in pairs)
        if any(domain not in _ALLOWED_RECEIPT_DOMAINS for domain in domains):
            raise KnownToolFailure("PUBLIC_STOCKROOM_RESOURCE_DOMAIN_DENIED")
        tool_pairs = tuple(
            (receipt, requirement)
            for receipt, requirement in pairs
            if requirement.scope.domain is ResourceDomain.TOOL
            and requirement.scope.resource_id == _TOOL_RESOURCE_IDENTITY
        )
        if len(tool_pairs) != 1:
            raise UnknownToolOutcome("PUBLIC_STOCKROOM_TOOL_RECEIPT_UNRESOLVED")
        receipt, requirement = tool_pairs[0]
        if not self._policy.enter_claimed_dispatch(
            receipt,
            requirement,
            dispatch_identity=dispatch_identity,
        ):
            raise UnknownToolOutcome("PUBLIC_STOCKROOM_TOOL_RECEIPT_DENIED")

        output = json.loads(canonical_json_bytes(STOCKROOM_SUMMARY))
        if not isinstance(output, dict):
            raise RuntimeError("PUBLIC_STOCKROOM_CANONICAL_OUTPUT_INVALID")
        self.invocation_count += 1
        self.last_consumed_domains = domains
        return ToolOutputRef(
            output_id=(
                "public-stockroom-output-"
                + hashlib.sha256(dispatch_identity.encode("ascii")).hexdigest()[:24]
            ),
            operation_id=dispatch_identity,
            argument_hash=requirement.operation_fingerprint or "",
            result_hash=canonical_sha256(output),
            output=output,
        )


@dataclass(frozen=True, slots=True)
class PublicStockroomComposition:
    registry: ToolRegistry
    implementation_fingerprint: str
    scope_authority: PublicLiveWorkerScopeAuthority

    def dispatcher(self, policy: SecurityPolicy) -> PublicLiveFixedStockroomDispatcher:
        return PublicLiveFixedStockroomDispatcher(policy)


class PublicLiveWorkerScopeAuthority(PublicLiveFixedToolScopeAuthority):
    """Exact provider/secret and one deferred fixed Stockroom TOOL authority."""

    def __init__(
        self,
        *,
        implementation_fingerprint: str,
        principal: str,
        run_id: str,
        profile: ProviderProfile,
    ) -> None:
        super().__init__(
            implementation_fingerprint=implementation_fingerprint,
            principal=principal,
            run_id=run_id,
        )
        self._profile = profile
        self._provider_context = object()
        self._dispatch_context: ToolDispatchContext | None = None

    def build_dispatch_context(self, **values: Any) -> ToolDispatchContext:
        context = ToolDispatchContext(
            task_action="fixed-stockroom-summary",
            work_run_id=values["current"].run_id,
            execution_attempt_id=values["attempt"].execution_attempt_id,
            state="RUNNING",
            state_version=values["current"].state_version,
            runtime_mode=RuntimeMode.PUBLIC_BOUNDED_LIVE.value,
            scenario_id=values["scenario_id"],
            scenario_version="1.0.0",
            profile_id=values["profile"].profile_id,
            profile_version="1",
            resource_ref=RESOURCE_REF,
            provider_operation_id=values["operation_id"],
            provider_call_id=values["provider_call_id"],
            resolved_implementation_fingerprint=PUBLIC_FIXED_STOCKROOM_IMPLEMENTATION_FINGERPRINT,
        )
        self._dispatch_context = context
        return context

    def issue_context(self, **values: Any) -> object | None:
        scope = values["scope"]
        if scope.domain in {ResourceDomain.PROVIDER, ResourceDomain.SECRET}:
            return self._provider_context
        if scope.domain is ResourceDomain.TOOL:
            if self._dispatch_context is None:
                raise ValueError("PUBLIC_STOCKROOM_CONTEXT_REQUIRED")
            return self.bind(
                dispatch_context=self._dispatch_context,
                fingerprint=values["operation_fingerprint"],
            )
        return None

    def allows(self, context: object, **values: Any) -> bool:
        scope = values["scope"]
        if scope.domain in {ResourceDomain.PROVIDER, ResourceDomain.SECRET}:
            identities = {
                ResourceDomain.PROVIDER: self._profile.provider_resource_identity,
                ResourceDomain.SECRET: self._profile.secret_resource_identity,
            }
            return bool(
                context is self._provider_context
                and values["mode"] is RuntimeMode.PUBLIC_BOUNDED_LIVE
                and values["scenario_id"] == "stockroom-s1-normal"
                and values["action"] is SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT
                and values["principal"] == self.principal
                and values["run_id"] == self._expected_run_id
                and scope.resource_id == identities[scope.domain]
            )
        return bool(super().allows(context, **values))


def compose_public_stockroom(
    *, run_id: str, attempt_id: str, principal: str, profile: ProviderProfile
) -> PublicStockroomComposition:
    del attempt_id
    registry = luna_tool_registry()
    authority = PublicLiveWorkerScopeAuthority(
        implementation_fingerprint=PUBLIC_FIXED_STOCKROOM_IMPLEMENTATION_FINGERPRINT,
        principal=principal,
        run_id=run_id,
        profile=profile,
    )
    return PublicStockroomComposition(
        registry,
        PUBLIC_FIXED_STOCKROOM_IMPLEMENTATION_FINGERPRINT,
        authority,
    )
