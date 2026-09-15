from dataclasses import replace

import pytest

from aiscc.public_live.identity import AdmissionDenied
from aiscc.public_live.source import DirectPeerSource


def test_source_normalization_and_domain_binding():
    adapter = DirectPeerSource("campaign", "v1", b"s" * 32, True)

    def get(ip, owner=adapter, headers=()):
        return owner.derive({"client": (ip, 1234), "headers": headers})

    assert get("8.8.8.8").bucket == get("::ffff:8.8.8.8").bucket
    assert get("8.8.8.8").bucket != get("8.8.8.9").bucket
    assert get("2001:4860:1:2::1").bucket == get("2001:4860:1:2::ffff").bucket
    assert get("2001:4860:1:2::1").bucket != get("2001:4860:1:3::1").bucket
    original = get("8.8.8.8")
    assert len(original.bucket) == 32 and "8.8.8.8" not in repr(original)
    assert original.bucket != get("8.8.8.8", replace(adapter, campaign="other")).bucket
    assert original.bucket != get("8.8.8.8", replace(adapter, key_version="v2")).bucket
    assert original.bucket != get("8.8.8.8", replace(adapter, secret=b"t" * 32)).bucket
    assert (
        original.bucket
        == get(
            "8.8.8.8", headers=[(b"forwarded", b"for=evil"), (b"x-forwarded-for", b"1.1.1.1")]
        ).bucket
    )


@pytest.mark.parametrize("peer", [None, "", "not-ip", "::", "0.0.0.0", "ff02::1", "fe80::1%eth0"])
def test_source_invalid_fails_closed(peer):
    with pytest.raises(AdmissionDenied, match="IDENTITY_UNAVAILABLE"):
        DirectPeerSource("c", "v", b"s" * 32, True).derive({"client": (peer, 1)})


def test_source_default_unverified_and_missing_peer_fail_closed():
    with pytest.raises(AdmissionDenied):
        DirectPeerSource("c", "v", b"s" * 32).derive({"client": ("8.8.8.8", 1)})
    with pytest.raises(AdmissionDenied):
        DirectPeerSource("c", "v", b"s" * 32, True).derive({})
