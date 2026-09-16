"""Server-only environment binding to the existing P1-5 lease authority.

Construction does not read environment values. Resolution is single use and
never accepts a variable name or secret reference from a public caller.
"""

import os

from aiscc.contracts.workflow import RuntimeMode
from aiscc.providers.authority import SecretResolutionLeaseAuthority
from aiscc.providers.models import SecretResolutionLease

SECRET_VARIABLE = "AISCC_OPENAI_API_KEY"
SECRET_REF = "secret-ref:openai/public-live/runtime/v1"


class HostedSecretUnavailable(ValueError):
    def __init__(self) -> None:
        super().__init__("LIVE_UNAVAILABLE")


class HostedOpenAISecretResolver:
    def __init__(self, authority: SecretResolutionLeaseAuthority) -> None:
        self._authority = authority

    def resolve(self, lease: SecretResolutionLease) -> str:
        if not isinstance(lease, SecretResolutionLease) or not (
            lease.secret_ref == SECRET_REF
            and lease.profile_id == "public-live-luna-v1"
            and lease.profile_version == "1"
            and lease.runtime_mode is RuntimeMode.PUBLIC_BOUNDED_LIVE
            and lease.scenario_id == "stockroom-s1-normal"
            and lease.destination == "openai-public-live-production-v1"
            and lease.purpose == "RESPONSES_CREATE"
            and self._authority.consume_for_resolution(lease)
        ):
            raise ValueError("SECRET_LEASE_DENIED")
        value = os.environ.get(SECRET_VARIABLE)
        if not value or not value.strip():
            self._authority.close(lease)
            raise HostedSecretUnavailable()
        return value

    def close(self, lease: SecretResolutionLease) -> None:
        self._authority.close(lease)
