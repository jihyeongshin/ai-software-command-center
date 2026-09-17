"""Server-owned direct-peer identity boundary; hosted proxy trust remains L5."""

from __future__ import annotations

import hmac
import ipaddress
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from aiscc.public_live.identity import AdmissionDenied


@dataclass(frozen=True)
class TrustedSource:
    campaign: str
    key_version: str
    bucket: bytes
    address: str = field(repr=False)
    transport_secure: bool = True


@dataclass(frozen=True)
class DirectPeerSource:
    campaign: str
    key_version: str
    secret: bytes = field(repr=False)
    direct_peer_verified: bool = False

    def derive(self, scope: Mapping[str, Any]) -> TrustedSource:
        # Only the server integration may assert original socket peer provenance.
        # No header (including XFF/Forwarded) is consulted, even when present.
        try:
            if not self.direct_peer_verified or not self.campaign or not self.key_version:
                raise ValueError
            if len(self.secret) < 32:
                raise ValueError
            value = scope["client"][0]
            if "%" in value:
                raise ValueError
            address = ipaddress.ip_address(value)
            if isinstance(address, ipaddress.IPv6Address) and address.ipv4_mapped:
                address = address.ipv4_mapped
            if address.is_unspecified or address.is_multicast:
                raise ValueError
            return trusted_source(
                address,
                campaign=self.campaign,
                key_version=self.key_version,
                secret=self.secret,
                transport_secure=scope.get("scheme") == "https",
            )
        except (ValueError, TypeError, KeyError, IndexError, OverflowError):
            raise AdmissionDenied("IDENTITY_UNAVAILABLE") from None


def trusted_source(
    address: ipaddress.IPv4Address | ipaddress.IPv6Address,
    *,
    campaign: str,
    key_version: str,
    secret: bytes,
    transport_secure: bool,
) -> TrustedSource:
    """Mint an opaque source bucket from already verified server authority."""
    if not campaign or not key_version or len(secret) < 32:
        raise AdmissionDenied("IDENTITY_UNAVAILABLE")
    prefix = 32 if address.version == 4 else 64
    network = ipaddress.ip_network((address, prefix), strict=False)
    c, v = campaign.encode(), key_version.encode()
    message = (
        b"aiscc-public-flood-v1\0"
        + len(c).to_bytes(4, "big")
        + c
        + len(v).to_bytes(4, "big")
        + v
        + bytes((address.version, prefix))
        + network.network_address.packed
    )
    return TrustedSource(
        campaign,
        key_version,
        hmac.digest(secret, message, "sha256"),
        str(address),
        transport_secure,
    )
