from __future__ import annotations

from aiscc.scenarios.composition import (
    StockroomOwnerPreparation,
    bind_stockroom_owner_dependencies,
    build_stockroom_owner_composition,
)
from aiscc.scenarios.driver import StockroomOwnerDependencies
from aiscc.security.models import PermissionProfile
from aiscc.security.policy import SecurityPolicy, default_profiles


def build_security_policy() -> SecurityPolicy:
    """Composition root for the P1-3 security policy; it owns no workflow mutation."""
    profiles: dict[str, PermissionProfile] = default_profiles()
    return SecurityPolicy(profiles=profiles)


def build_stockroom_owner_preparation(
    *, owners: StockroomOwnerDependencies
) -> StockroomOwnerPreparation:
    """Explicit owner-only inert preparation root; it performs no execution."""
    return bind_stockroom_owner_dependencies(build_stockroom_owner_composition(), owners)
