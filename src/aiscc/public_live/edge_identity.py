"""Railway edge identity binding; disabled until hosted overwrite proof is accepted."""

from __future__ import annotations

import ipaddress
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlsplit

from aiscc.public_live.identity import AdmissionDenied
from aiscc.public_live.source import TrustedSource, trusted_source

_EDGE = re.compile(r"[a-z]{3}[1-9][0-9]*", re.ASCII)
_CONFLICTING = frozenset({b"forwarded", b"x-forwarded-for", b"cf-connecting-ip"})


@dataclass(frozen=True)
class RailwayEdgeIdentityAuthority:
    """The sole hosted owner allowed to mint a verified Public Live source.

    Header documentation is insufficient authority. ``overwrite_proof_accepted``
    must remain false until a later hosted spoof matrix is Human accepted.
    """

    public_origin: str
    campaign: str
    key_version: str
    secret: bytes = field(repr=False)
    overwrite_proof_accepted: bool = False

    def __post_init__(self) -> None:
        parsed = urlsplit(self.public_origin)
        if (
            parsed.scheme != "https"
            or not parsed.hostname
            or parsed.username
            or parsed.password
            or parsed.port not in (None, 443)
            or parsed.path not in ("", "/")
            or parsed.query
            or parsed.fragment
            or len(self.secret) < 32
            or not self.campaign
            or not self.key_version
        ):
            raise ValueError("PUBLIC_LIVE_EDGE_CONFIGURATION_DENIED")

    @property
    def expected_host(self) -> str:
        host = urlsplit(self.public_origin).hostname
        if host is None:  # guarded in __post_init__
            raise RuntimeError("PUBLIC_LIVE_EDGE_CONFIGURATION_DENIED")
        return host.lower()

    def derive(self, scope: Mapping[str, Any]) -> TrustedSource:
        try:
            if not self.overwrite_proof_accepted:
                raise ValueError
            raw: Sequence[tuple[bytes, bytes]] = scope["headers"]
            lowered = [(bytes(k).lower(), bytes(v)) for k, v in raw]
            if any(name in _CONFLICTING for name, _ in lowered):
                raise ValueError
            host = self._one(lowered, b"host")
            real_ip = self._one(lowered, b"x-real-ip")
            proto = self._one(lowered, b"x-forwarded-proto")
            edge = self._one(lowered, b"x-railway-edge")
            if host.decode("ascii").lower() != self.expected_host or proto != b"https":
                raise ValueError
            if _EDGE.fullmatch(edge.decode("ascii")) is None:
                raise ValueError
            value = real_ip.decode("ascii")
            if (
                not value
                or value != value.strip()
                or any(char in value for char in (",", "%", "[", "]"))
                or any(char.isspace() for char in value)
            ):
                raise ValueError
            address = ipaddress.ip_address(value)
            if isinstance(address, ipaddress.IPv6Address) and address.ipv4_mapped:
                address = address.ipv4_mapped
            if not address.is_global or address.is_multicast or address.is_unspecified:
                raise ValueError
            return trusted_source(
                address,
                campaign=self.campaign,
                key_version=self.key_version,
                secret=self.secret,
                transport_secure=True,
            )
        except (KeyError, TypeError, ValueError, UnicodeError, OverflowError):
            raise AdmissionDenied("IDENTITY_UNAVAILABLE") from None

    @staticmethod
    def _one(headers: Sequence[tuple[bytes, bytes]], name: bytes) -> bytes:
        values = [value for key, value in headers if key == name]
        if len(values) != 1:
            raise ValueError
        return values[0]
