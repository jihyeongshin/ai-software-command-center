"""Exact accepted Stockroom runtime composition for the Public Live worker."""

from __future__ import annotations

import hashlib
import shutil
from collections.abc import Callable, Sequence
from dataclasses import dataclass, replace
from pathlib import Path
from threading import Event
from typing import Any, Literal, cast

from aiscc.contracts.security import ResourceDomain, SecurityActionClass
from aiscc.contracts.workflow import RuntimeMode
from aiscc.providers.models import ProviderProfile, ToolRegistry
from aiscc.providers.stockroom_tool import (
    StockroomSummaryDispatcher,
    build_dispatch_context,
    build_stockroom_spec,
    load_stockroom_tool_config,
)
from aiscc.providers.tools import ToolDispatchContext
from aiscc.public_live.luna_profile import luna_tool_registry
from aiscc.public_live.provider_authority import LunaToolScopeAuthority
from aiscc.runtime.docker import (
    DockerRunSpec,
    DockerRuntime,
    StockroomCancellation,
    StockroomDockerRunner,
    StockroomProcessObservation,
)
from aiscc.runtime.stockroom_image import (
    PROVENANCE_PATH,
    StockroomImageProvenanceRef,
    canonical_fingerprint,
    image_policy,
    parse_provenance,
    provenance_payload,
    resolve_stockroom_image,
)
from aiscc.security.policy import SecurityPolicy

_ROOT = Path(__file__).resolve().parents[3]


@dataclass(frozen=True, slots=True)
class PublicStockroomComposition:
    registry: ToolRegistry
    spec: DockerRunSpec
    scope_authority: PublicLiveWorkerScopeAuthority

    def dispatcher(
        self,
        policy: SecurityPolicy,
        *,
        runner: Callable[[Sequence[str], DockerRunSpec], StockroomProcessObservation] | None,
        attempt_id: str,
    ) -> StockroomSummaryDispatcher:
        selected = runner
        if selected is None:
            executable = shutil.which("docker")
            if executable is None:
                raise RuntimeError("PUBLIC_LIVE_STOCKROOM_DOCKER_REQUIRED")
            selected = StockroomDockerRunner(
                Path(executable).resolve(strict=True),
                resolve_stockroom_image(_provenance_ref(), image_policy()),
                StockroomCancellation(self.spec.run_id, attempt_id, Event()),
            )
        return StockroomSummaryDispatcher(
            DockerRuntime(policy, stockroom_runner=selected),
            self.spec,
        )


class PublicLiveWorkerScopeAuthority(LunaToolScopeAuthority):
    """Exact provider/secret and one deferred Stockroom tool/process authority."""

    def __init__(
        self,
        *,
        spec: DockerRunSpec,
        principal: str,
        run_id: str,
        profile: ProviderProfile,
    ) -> None:
        super().__init__(spec=spec, principal=principal, run_id=run_id)
        self._spec = spec
        self._profile = profile
        self._provider_context = object()
        self._dispatch_context: ToolDispatchContext | None = None

    def build_dispatch_context(self, **values: Any) -> ToolDispatchContext:
        context = build_dispatch_context(
            run_id=values["current"].run_id,
            attempt_id=values["attempt"].execution_attempt_id,
            state_version=values["current"].state_version,
            scenario_id=values["scenario_id"],
            profile_id=values["profile"].profile_id,
            provider_operation_id=values["operation_id"],
            provider_call_id=values["provider_call_id"],
            spec=self._spec,
        )
        context = replace(context, runtime_mode=RuntimeMode.PUBLIC_BOUNDED_LIVE.value)
        self._dispatch_context = context
        return context

    def issue_context(self, **values: Any) -> object | None:
        scope = values["scope"]
        if scope.domain in {ResourceDomain.PROVIDER, ResourceDomain.SECRET}:
            return self._provider_context
        if scope.domain in {ResourceDomain.TOOL, ResourceDomain.PROCESS}:
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
    config = load_stockroom_tool_config(_ROOT / "config/providers/stockroom-tools.v2.toml")
    image = resolve_stockroom_image(_provenance_ref(), dict(config.image_binding_policy))
    spec = build_stockroom_spec(
        config,
        name=f"aiscc-{attempt_id}",
        run_id=run_id,
        workspace=_ROOT / "examples/synthetic-stockroom",
        image_provenance=image,
    )
    authority = PublicLiveWorkerScopeAuthority(
        spec=spec,
        principal=principal,
        run_id=run_id,
        profile=profile,
    )
    return PublicStockroomComposition(luna_tool_registry(config, spec), spec, authority)


def _provenance_ref() -> StockroomImageProvenanceRef:
    path = _ROOT / PROVENANCE_PATH
    data = path.read_bytes()
    value = parse_provenance(data)
    return StockroomImageProvenanceRef(
        path=cast(
            Literal[".aiassistant/records/aiscc/runtime/stockroom-image-provenance.v1.json"],
            PROVENANCE_PATH,
        ),
        whole_file_sha256=hashlib.sha256(data).hexdigest(),
        canonical_fingerprint=canonical_fingerprint(provenance_payload(value)),
        provenance_id=value.provenance_id,
        provenance_version=value.provenance_version,
        issuance=value.issuance,
    )
