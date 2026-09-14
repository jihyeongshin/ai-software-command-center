"""Deterministic orchestration adapter; no Task issuance or workflow authority."""

from aiscc.self_dogfood.materializer import build_ready_request, enter_ready, materialize_task_spec
from aiscc.self_dogfood.models import SelfDogfoodTaskSpec

__all__ = ["SelfDogfoodTaskSpec", "build_ready_request", "enter_ready", "materialize_task_spec"]
