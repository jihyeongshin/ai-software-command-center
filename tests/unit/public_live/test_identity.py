import pytest

from aiscc.public_live.identity import AdmissionDenied, IdentityPolicy, request_identity

BODY = b'{"scenario_id":"stockroom-s1-normal","scenario_version":"1.0.0"}'
POLICY = IdentityPolicy(("10.0.0.0/24",), "synthetic-edge-proof", "campaign", "v1", b"s" * 32)


@pytest.mark.parametrize(
    "body",
    [
        b"{}",
        b"[]",
        b"null",
        b"\xff",
        BODY[:-1] + b',"model":"user-selected"}',
        BODY[:-1] + b',"scenario_id":"stockroom-s1-normal"}',
        BODY.replace(b"1.0.0", b"2.0.0"),
        b"x" * 1025,
    ],
)
def test_forbidden_or_invalid_body(body):
    with pytest.raises(AdmissionDenied):
        request_identity(body, "a" * 32, b"p" * 32, b"c" * 32)


@pytest.mark.parametrize("key", ["A" * 32, "a" * 31, "g" * 32, "a" * 33, "", None])
def test_key_exactness(key):
    with pytest.raises(AdmissionDenied):
        request_identity(BODY, key, b"p" * 32, b"c" * 32)


@pytest.mark.parametrize(
    "address",
    [
        "127.0.0.1",
        "10.0.0.1",
        "0.0.0.0",
        "224.0.0.1",
        "fe80::1",
        "2001:4860::1%eth0",
        "8.8.8.8:443",
        "8.8.8.8,1.1.1.1",
        " 8.8.8.8",
    ],
)
def test_untrusted_identity(address):
    with pytest.raises(AdmissionDenied):
        POLICY.bucket("10.0.0.2", (("X-Forwarded-For", address),))


@pytest.mark.parametrize(
    "headers",
    [
        (),
        (("Forwarded", "for=8.8.8.8"),),
        (("X-Forwarded-For", "8.8.8.8"), ("X-Real-IP", "8.8.8.8")),
        (("X-Forwarded-For", "8.8.8.8"), ("x-forwarded-for", "8.8.8.8")),
    ],
)
def test_header_authority(headers):
    with pytest.raises(AdmissionDenied):
        POLICY.bucket("10.0.0.2", headers)


def test_bucket_normalization_and_missing_edge_proof():
    def bucket(ip):
        return POLICY.bucket("10.0.0.2", (("X-Forwarded-For", ip),))

    assert bucket("8.8.8.8") == bucket("::ffff:8.8.8.8")
    assert bucket("2001:4860:1234:abcd::1") == bucket("2001:4860:1234:abcd:0:0:0:99")
    assert bucket("2001:4860:1234:abcd::1") != bucket("2001:4860:1234:abce::1")
    for edges, proof, peer in [
        ((), "proof", "10.0.0.2"),
        (("0.0.0.0/0",), "proof", "10.0.0.2"),
        (("10.0.0.0/24",), "", "10.0.0.2"),
        (("10.0.0.0/24",), "proof", "1.1.1.1"),
    ]:
        with pytest.raises(AdmissionDenied):
            IdentityPolicy(edges, proof, "campaign", "v1", b"s" * 32).bucket(
                peer, (("X-Forwarded-For", "8.8.8.8"),)
            )


def test_canonical_payload_and_server_pins():
    a = request_identity(BODY, "a" * 32, b"p" * 32, b"c" * 32)
    assert a == request_identity(
        b'{ "scenario_version": "1.0.0", "scenario_id": "stockroom-s1-normal" }',
        "a" * 32,
        b"p" * 32,
        b"c" * 32,
    )
    assert a[1] != request_identity(BODY, "a" * 32, b"q" * 32, b"c" * 32)[1]
