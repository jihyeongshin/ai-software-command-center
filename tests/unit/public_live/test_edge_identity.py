from __future__ import annotations

import pytest

from aiscc.public_live.edge_identity import RailwayEdgeIdentityAuthority
from aiscc.public_live.identity import AdmissionDenied


def authority(*, accepted: bool = True) -> RailwayEdgeIdentityAuthority:
    return RailwayEdgeIdentityAuthority(
        "https://public-live.up.railway.app",
        "public-live-v1",
        "v1",
        b"k" * 32,
        accepted,
    )


def scope(address: str = "8.8.8.8", *, extra=(), client="203.0.113.10"):
    headers = [
        (b"host", b"public-live.up.railway.app"),
        (b"x-real-ip", address.encode()),
        (b"x-forwarded-proto", b"https"),
        (b"x-railway-edge", b"icn1"),
        *extra,
    ]
    return {"headers": headers, "client": (client, 1234), "scheme": "http"}


@pytest.mark.parametrize("address", ["8.8.8.8", "2606:4700:4700::1111"])
def test_valid_edge_identity_ignores_socket_peer(address: str) -> None:
    first = authority().derive(scope(address, client="192.0.2.1"))
    second = authority().derive(scope(address, client="192.0.2.2"))
    assert first.bucket == second.bucket
    assert first.transport_secure is True


def test_ipv4_mapped_ipv6_normalizes_to_ipv4() -> None:
    assert (
        authority().derive(scope("::ffff:8.8.8.8")).bucket
        == authority().derive(scope("8.8.8.8")).bucket
    )


@pytest.mark.parametrize(
    "mutate",
    [
        lambda h: h + [(b"x-real-ip", b"8.8.4.4")],
        lambda h: [(k, b"8.8.8.8, 8.8.4.4") if k == b"x-real-ip" else (k, v) for k, v in h],
        lambda h: [(k, b"8.8.8.8:443") if k == b"x-real-ip" else (k, v) for k, v in h],
        lambda h: [(k, b"[2606:4700:4700::1111]") if k == b"x-real-ip" else (k, v) for k, v in h],
        lambda h: [(k, b"fe80::1%eth0") if k == b"x-real-ip" else (k, v) for k, v in h],
        lambda h: [(k, b" 8.8.8.8") if k == b"x-real-ip" else (k, v) for k, v in h],
        lambda h: h + [(b"x-forwarded-proto", b"https")],
        lambda h: [(k, b"http") if k == b"x-forwarded-proto" else (k, v) for k, v in h],
        lambda h: [(k, v) for k, v in h if k != b"x-railway-edge"],
        lambda h: [(k, b"invalid") if k == b"x-railway-edge" else (k, v) for k, v in h],
        lambda h: [(k, b"other.up.railway.app") if k == b"host" else (k, v) for k, v in h],
    ],
)
def test_ambiguous_spoofed_or_conflicting_identity_denied(mutate) -> None:
    value = scope()
    value["headers"] = mutate(value["headers"])
    with pytest.raises(AdmissionDenied, match="IDENTITY_UNAVAILABLE"):
        authority().derive(value)


def test_non_authority_forwarding_headers_are_ignored() -> None:
    expected = authority().derive(scope())
    hostile = authority().derive(
        scope(
            extra=[
                (b"forwarded", b"for=not-an-ip;proto=http"),
                (b"forwarded", b"for=192.0.2.1,for=198.51.100.2"),
                (b"x-forwarded-for", b"not-an-ip, 192.0.2.1"),
                (b"x-forwarded-for", b"203.0.113.7"),
                (b"cf-connecting-ip", b"invalid"),
                (b"cf-connecting-ip", b"2001:db8::1"),
            ]
        )
    )
    assert hostile == expected


def test_release_gate_is_fail_closed_and_request_cannot_set_it() -> None:
    value = scope(extra=[(b"direct-peer-verified", b"true")])
    with pytest.raises(AdmissionDenied, match="IDENTITY_UNAVAILABLE"):
        authority(accepted=False).derive(value)
