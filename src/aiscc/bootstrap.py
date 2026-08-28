from __future__ import annotations

from aiscc.security.models import PermissionProfile
from aiscc.security.policy import SecurityPolicy, default_profiles


def build_security_policy() -> SecurityPolicy:
    """Composition root for the P1-3 security policy; it owns no workflow mutation."""
    profiles: dict[str, PermissionProfile] = default_profiles()
    return SecurityPolicy(profiles=profiles)
