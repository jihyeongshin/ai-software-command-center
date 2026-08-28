from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

from aiscc.contracts.security import ResourceDomain, SecurityActionClass
from aiscc.contracts.workflow import RuntimeMode, WorkflowState

router = APIRouter(prefix="/v1/security")


class EvaluationInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    principal: str = Field(min_length=1, max_length=128)
    run_id: str = Field(min_length=1, max_length=128)
    mode: RuntimeMode
    state: WorkflowState
    state_version: int = Field(ge=1)
    action: SecurityActionClass
    resource_domain: ResourceDomain
    resource_id: str = Field(min_length=1, max_length=256)


class EvaluationOutput(BaseModel):
    decision: str
    reason: str


@router.post("/evaluate", response_model=EvaluationOutput)
def evaluate_security(candidate: EvaluationInput) -> EvaluationOutput:
    """Public diagnostics cannot manufacture authoritative workflow/security evidence."""
    return EvaluationOutput(decision="DENY", reason="NON_AUTHORITATIVE_DIAGNOSTIC_ONLY")
