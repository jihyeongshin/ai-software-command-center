"""R1 identity derivation and bounded A1 input; deployment proof stays external."""

from __future__ import annotations

import hashlib
import hmac
import ipaddress
import json
import re
from dataclasses import dataclass, field


class AdmissionDenied(ValueError):
    """Safe reason only: never echoes untrusted input or credentials."""


@dataclass(frozen=True)
class IdentityPolicy:
    edge_cidrs: tuple[str, ...]
    overwrite_proof_ref: str
    campaign_id: str
    key_version: str
    secret: bytes = field(repr=False)

    def bucket(self, peer: str, headers: tuple[tuple[str, str], ...]) -> bytes:
        try:
            edges = tuple(ipaddress.ip_network(c, strict=True) for c in self.edge_cidrs)
            if not edges or any(e.prefixlen == 0 for e in edges) or not self.overwrite_proof_ref:
                raise ValueError
            if not self.campaign_id or not self.key_version or len(self.secret) < 32:
                raise ValueError
            if "%" in peer:
                raise ValueError
            socket = ipaddress.ip_address(peer)
            if not any(socket in e for e in edges):
                raise ValueError
            identity_headers = [
                (k.lower(), v)
                for k, v in headers
                if k.lower() in {"x-forwarded-for", "forwarded", "x-real-ip", "cf-connecting-ip"}
            ]
            if len(identity_headers) != 1 or identity_headers[0][0] != "x-forwarded-for":
                raise ValueError
            value = identity_headers[0][1]
            if value != value.strip() or any(c in value for c in ("%", ",", "[", "]")):
                raise ValueError
            address = ipaddress.ip_address(value)
            if isinstance(address, ipaddress.IPv6Address) and address.ipv4_mapped:
                address = address.ipv4_mapped
            if not address.is_global or address.is_multicast or address.is_unspecified:
                raise ValueError
            prefix = 32 if address.version == 4 else 64
            network = ipaddress.ip_network((address, prefix), strict=False)
            campaign = self.campaign_id.encode("utf-8")
            message = (
                b"aiscc-public-bucket-v1\0"
                + len(campaign).to_bytes(4, "big")
                + campaign
                + bytes((address.version, prefix))
                + network.network_address.packed
            )
            return hmac.digest(self.secret, message, "sha256")
        except (ValueError, TypeError, OverflowError):
            raise AdmissionDenied("IDENTITY_UNAVAILABLE") from None


def request_identity(
    body: bytes, key: str, policy_digest: bytes, content_digest: bytes
) -> tuple[bytes, bytes]:
    if len(body) > 1024:
        raise AdmissionDenied("BODY_TOO_LARGE")
    if not isinstance(key, str) or re.fullmatch(r"[0-9a-f]{32}", key) is None:
        raise AdmissionDenied("INVALID_REQUEST")

    def unique(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result = {}
        for k, v in pairs:
            if k in result:
                raise ValueError
            result[k] = v
        return result

    try:
        payload = json.loads(body.decode("utf-8"), object_pairs_hook=unique)
        if payload != {"scenario_id": "stockroom-s1-normal", "scenario_version": "1.0.0"}:
            raise ValueError
        if len(policy_digest) != 32 or len(content_digest) != 32:
            raise ValueError
    except (UnicodeError, ValueError, TypeError):
        raise AdmissionDenied("INVALID_REQUEST") from None
    pinned = payload | {
        "schema_version": 1,
        "policy_digest": policy_digest.hex(),
        "content_digest": content_digest.hex(),
    }
    canonical = json.dumps(pinned, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(bytes.fromhex(key)).digest(), hashlib.sha256(canonical).digest()
