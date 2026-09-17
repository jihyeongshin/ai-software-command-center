"""Pure Public Live semantic plan and ProviderCall construction.

Planning has no reservation, capability, secret, operation or dispatch side
effect.  The P1-5 service remains the only physical lifecycle owner.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.providers.models import (
    ProviderCall,
    ProviderInputAuthority,
    canonical_json_bytes,
)
from aiscc.public_live.luna_profile import ROLE_EFFORT, bind_call, hosted_luna_profile


@dataclass(frozen=True, slots=True)
class SemanticProviderPlan:
    role: str
    semantic_ordinal: int
    physical_ordinal: int
    retry_of_operation_id: str | None
    validation_ref: str | None
    defect_ref: str | None
    plan_digest: str

    def __post_init__(self) -> None:
        if (
            self.role not in ROLE_EFFORT
            or not 1 <= self.semantic_ordinal <= 3
            or not 1 <= self.physical_ordinal <= 4
            or (self.role == "VERIFY") != (self.validation_ref is not None)
            or (self.role == "CORRECT") != (self.defect_ref is not None)
            or len(self.plan_digest) != 64
        ):
            raise ValueError("SEMANTIC_PLAN_INVALID")


def plan_next_semantic_request(
    *,
    prior: tuple[MappingProxyType[str, Any], ...],
    validation: MappingProxyType[str, Any] | None,
    tool_continuation: bool = False,
) -> SemanticProviderPlan:
    physical = len(prior) + 1
    if physical > 4:
        raise ValueError("PHYSICAL_REQUEST_LIMIT")
    retry_of = None
    validation_ref = None
    defect_ref = None
    if not prior:
        role, semantic = "PRIMARY", 1
    else:
        last = prior[-1]
        if tool_continuation and last.get("outcome") == "KNOWN_SUCCESS":
            role = str(last["role"])
            semantic = int(last["semantic_ordinal"])
        elif last.get("outcome") == "KNOWN_FAILURE" and last.get("closed_failure") is True:
            if any(item.get("retry_of_operation_id") for item in prior):
                raise ValueError("RETRY_LIMIT")
            role = str(last["role"])
            semantic = int(last["semantic_ordinal"])
            retry_of = str(last["operation_id"])
        elif last.get("outcome") == "KNOWN_SUCCESS" and validation is not None:
            decision = validation.get("decision")
            validation_ref = str(validation.get("proof"))
            if decision == "VERIFY_REQUIRED" and last.get("role") == "PRIMARY":
                role, semantic = "VERIFY", 2
            elif decision == "CORRECTABLE_DEFECT" and last.get("role") in {
                "PRIMARY",
                "VERIFY",
            }:
                role, semantic = "CORRECT", int(last["semantic_ordinal"]) + 1
                defect_ref = str(validation.get("defect_ref"))
                validation_ref = None
            else:
                raise ValueError("NO_SEMANTIC_TRANSITION")
        else:
            raise ValueError("UNKNOWN_OR_UNVALIDATED_OUTCOME")
    body = {
        "version": "PUBLIC_LIVE_SEMANTIC_PLAN_V1",
        "role": role,
        "semantic_ordinal": semantic,
        "physical_ordinal": physical,
        "retry_of_operation_id": retry_of,
        "validation_ref": validation_ref,
        "defect_ref": defect_ref,
    }
    return SemanticProviderPlan(
        role,
        semantic,
        physical,
        retry_of,
        validation_ref,
        defect_ref,
        hashlib.sha256(canonical_json_bytes(body)).hexdigest(),
    )


def build_public_provider_call(
    *,
    plan: SemanticProviderPlan,
    operation_id: str,
    operation_fingerprint: str,
    work_run_id: str,
    execution_attempt_id: str,
    state_version: int,
    execution_version: int,
    principal: str,
    input_items: tuple[dict[str, Any], ...],
    tools: tuple[dict[str, Any], ...],
    continuation_hash: str | None = None,
) -> ProviderCall:
    if not operation_id or not principal or state_version < 1 or execution_version < 1:
        raise ValueError("PROVIDER_CALL_AUTHORITY_INVALID")
    call = ProviderCall(
        operation_id=operation_id,
        operation_fingerprint=operation_fingerprint,
        execution_attempt_id=execution_attempt_id,
        work_run_id=work_run_id,
        state=WorkflowState.RUNNING,
        state_version=state_version,
        runtime_mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
        principal=principal,
        scenario_id="stockroom-s1-normal",
        execution_version=execution_version,
        profile=hosted_luna_profile(),
        input_items=input_items,
        tools=tools,
        call_ordinal=plan.physical_ordinal,
        input_authority=(
            ProviderInputAuthority.DURABLE_LOCAL
            if continuation_hash is not None
            else ProviderInputAuthority.INITIAL_SERVER
        ),
        durable_continuation_hash=continuation_hash,
    )
    return bind_call(call, role=plan.role)[0]
