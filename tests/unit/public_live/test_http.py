import asyncio
from datetime import UTC, datetime

import pytest

from aiscc.persistence.public_live_limits import LimitResult, LimitsUnavailable
from aiscc.public_live.http import ORIGIN, ROOT, create_app
from aiscc.public_live.identity import AdmissionDenied
from aiscc.public_live.service import Receipt
from aiscc.public_live.source import DirectPeerSource
from tests.public_live_http_helpers import BODY, call


class Limits:
    def __init__(self):
        self.calls = 0
        self.allowed = True
        self.failure = False

    async def flood(self, *args):
        self.calls += 1
        if self.failure:
            raise LimitsUnavailable("secret DB host")
        return LimitResult(self.allowed, 23, 1, datetime.now(UTC))

    async def read(self, *args):
        raise AssertionError("Unauthorized read must not reach DB")


class Admission:
    def __init__(self):
        self.calls = 0
        self.error = None

    async def admit(self, *args):
        self.calls += 1
        if self.error:
            raise self.error
        return Receipt(b"r" * 16, False, b"t" * 32, datetime(2026, 9, 17, tzinfo=UTC))


def composition():
    limits, admission = Limits(), Admission()
    return (
        create_app(
            source=DirectPeerSource("c", "v1", b"s" * 32, True), limits=limits, admission=admission
        ),
        limits,
        admission,
    )


@pytest.mark.parametrize("method", ["POST", "GET", "OPTIONS"])
@pytest.mark.parametrize("origins", [[], ["null"], ["https://evil.invalid"], [ORIGIN, ORIGIN]])
def test_exact_origin(method, origins):
    app, limits, admission = composition()
    result = asyncio.run(call(app, method, headers=[("origin", o) for o in origins]))
    assert result["status"] == 403
    assert result["json"] == {"error": {"code": "ORIGIN_DENIED", "retryable": False}}
    assert "access-control-allow-origin" not in result["headers"]
    assert limits.calls == 1 and admission.calls == 0 and result["receives"] == 0


def test_preflight_exact_and_no_admission():
    app, limits, admission = composition()
    result = asyncio.run(
        call(
            app,
            "OPTIONS",
            headers=[
                ("origin", ORIGIN),
                ("access-control-request-method", "POST"),
                (
                    "access-control-request-headers",
                    "Content-Type, Idempotency-Key, X-Run-Read-Capability",
                ),
            ],
        )
    )
    assert result["status"] == 204 and result["raw"] == b""
    assert result["headers"]["access-control-allow-methods"] == "POST, OPTIONS"
    assert result["headers"]["access-control-max-age"] == "300"
    assert result["headers"]["vary"] == "Origin"
    assert result["headers"]["access-control-allow-origin"] == ORIGIN
    assert "access-control-allow-credentials" not in result["headers"]
    assert limits.calls == 1 and admission.calls == 0 and result["receives"] == 0


@pytest.mark.parametrize(
    "extra",
    [
        [],
        [("access-control-request-method", "DELETE")],
        [
            ("access-control-request-method", "GET"),
            ("access-control-request-headers", "Authorization"),
        ],
        [("access-control-request-method", "GET"), ("access-control-request-method", "GET")],
    ],
)
def test_invalid_preflight(extra):
    result = asyncio.run(call(composition()[0], "OPTIONS", headers=[("origin", ORIGIN)] + extra))
    assert result["status"] == 403 and result["json"]["error"]["code"] == "ORIGIN_DENIED"


@pytest.mark.parametrize(
    "body",
    [
        b"\xff",
        b"[]",
        b"null",
        b"{}",
        b'{"scenario_id":"stockroom-s1-normal","scenario_id":"stockroom-s1-normal","scenario_version":"1.0.0"}',
        BODY[:-1] + b',"model":"evil"}',
        BODY.replace(b'"1.0.0"', b"1"),
        BODY.replace(b"stockroom-s1-normal", b"https://evil.invalid/repo"),
    ],
)
def test_invalid_body(body):
    app, limits, admission = composition()
    result = asyncio.run(call(app, body=body))
    assert result["status"] == 400 and admission.calls == 0 and limits.calls == 1
    assert result["json"] == {"error": {"code": "INVALID_REQUEST", "retryable": False}}


@pytest.mark.parametrize(
    "media",
    [
        "text/plain",
        "multipart/form-data",
        "application/json; charset=latin1",
        "application/json; charset=utf-8; other=x",
    ],
)
def test_media(media):
    result = asyncio.run(
        call(
            composition()[0],
            headers=[("origin", ORIGIN), ("content-type", media), ("idempotency-key", "a" * 32)],
        )
    )
    assert result["status"] == 415 and result["receives"] == 0


@pytest.mark.parametrize(
    "extra,status",
    [
        ([("content-encoding", "gzip")], 415),
        ([("content-encoding", "identity")], 415),
        ([("idempotency-key", "a" * 32)], 400),
        ([("content-type", "application/json")], 415),
        ([("content-length", "1025")], 413),
        ([("content-length", "-1")], 400),
        ([("content-length", "1"), ("content-length", "1")], 400),
        ([("x-large", "x" * 8192)], 431),
    ],
)
def test_duplicate_compression_length_headers(extra, status):
    app, limits, admission = composition()
    result = asyncio.run(
        call(
            app,
            headers=[
                ("origin", ORIGIN),
                ("content-type", "application/json"),
                ("idempotency-key", "a" * 32),
            ]
            + extra,
        )
    )
    assert result["status"] == status and result["receives"] == 0
    assert limits.calls == 1 and admission.calls == 0


def test_streamed_size_exact_boundary_and_transport():
    app, _, admission = composition()
    result = asyncio.run(call(app, chunks=[BODY, b" " * (1024 - len(BODY))]))
    assert result["status"] == 201 and admission.calls == 1
    result = asyncio.run(call(app, chunks=[b" " * 1024, b"x", b"never-read"]))
    assert result["status"] == 413 and result["receives"] == 2 and admission.calls == 1
    result = asyncio.run(
        call(app, scheme="http", headers=[("origin", ORIGIN), ("x-forwarded-proto", "https")])
    )
    assert result["status"] == 400 and "location" not in result["headers"]


@pytest.mark.parametrize(
    "method,path,status",
    [
        ("DELETE", ROOT, 405),
        ("GET", ROOT, 405),
        ("POST", ROOT + "/abc", 405),
        ("POST", ROOT + "/abc/cancel", 404),
        ("GET", "/docs", 404),
        ("GET", "/openapi.json", 404),
        ("GET", "/v1/control", 404),
        ("GET", ROOT + "/", 404),
        ("GET", ROOT + "/bad!", 404),
    ],
)
def test_only_exact_public_routes(method, path, status):
    app, _, admission = composition()
    result = asyncio.run(call(app, method, path))
    assert result["status"] == status and admission.calls == 0
    assert "location" not in result["headers"]


def test_query_no_capability_recovery_or_cookie_authority():
    app, _, admission = composition()
    assert asyncio.run(call(app, query=b"token=secret"))["status"] == 400
    result = asyncio.run(
        call(
            app,
            "GET",
            ROOT + "/" + "c" * 22,
            headers=[("origin", ORIGIN), ("cookie", "read_capability=secret")],
        )
    )
    assert result["status"] == 404 and b"secret" not in result["raw"] and admission.calls == 0


def test_flood_before_parsing_and_backend_failure_no_side_effects():
    app, limits, admission = composition()
    limits.allowed = False
    result = asyncio.run(call(app, headers=[], chunks=[b"secret" * 10000]))
    assert result["status"] == 429 and result["receives"] == 0 and admission.calls == 0
    assert result["headers"]["retry-after"] == "23"
    assert result["json"] == {"error": {"code": "CLIENT_RATE_LIMIT", "retryable": True}}
    limits.failure = True
    result = asyncio.run(call(app))
    assert result["status"] == 503 and result["receives"] == 0 and admission.calls == 0
    assert result["json"] == {"error": {"code": "LIVE_UNAVAILABLE", "retryable": True}}
    assert b"secret" not in result["raw"]


@pytest.mark.parametrize(
    "code,status,retryable",
    [
        ("INVALID_REQUEST", 400, False),
        ("BODY_TOO_LARGE", 413, False),
        ("UNSUPPORTED_MEDIA", 415, False),
        ("HEADERS_TOO_LARGE", 431, False),
        ("ORIGIN_DENIED", 403, False),
        ("CLIENT_BINDING_DENIED", 403, False),
        ("NOT_FOUND", 404, False),
        ("METHOD_NOT_ALLOWED", 405, False),
        ("IDEMPOTENCY_CONFLICT", 409, False),
        ("IDEMPOTENCY_EXPIRED", 410, False),
        ("CLIENT_RATE_LIMIT", 429, True),
        ("GLOBAL_DAY_LIMIT", 429, True),
        ("READ_RATE_LIMIT", 429, True),
        ("CAPACITY_UNAVAILABLE", 503, True),
        ("DB_UNAVAILABLE", 503, True),
        ("COMMIT_OUTCOME_UNKNOWN", 503, True),
        ("LIVE_UNAVAILABLE", 503, True),
        ("IDENTITY_UNAVAILABLE", 503, False),
        ("LIVE_DISABLED", 503, False),
        ("BUDGET_UNAVAILABLE", 503, False),
        ("CAMPAIGN_CLOSED", 503, False),
        ("POLICY_UNAVAILABLE", 503, False),
        ("INTERNAL_ERROR", 500, False),
    ],
)
def test_safe_frozen_error_mapping(code, status, retryable):
    app, _, admission = composition()
    admission.error = AdmissionDenied(code)
    result = asyncio.run(call(app))
    assert result["status"] == status
    assert result["json"] == {"error": {"code": code, "retryable": retryable}}
    assert result["headers"]["cache-control"] == "no-store"
    assert result["headers"]["x-content-type-options"] == "nosniff"


def test_unknown_failure_uncertain_commit_and_default_disabled(caplog):
    app, _, admission = composition()
    admission.error = OSError("secret DSN raw-ip token")
    result = asyncio.run(call(app))
    assert result["json"] == {"error": {"code": "COMMIT_OUTCOME_UNKNOWN", "retryable": True}}
    admission.error = ValueError("secret DSN raw-ip token")
    assert asyncio.run(call(app))["json"]["error"]["code"] == "INTERNAL_ERROR"
    assert asyncio.run(call(create_app()))["json"]["error"]["code"] == "IDENTITY_UNAVAILABLE"
    assert "secret" not in caplog.text and "token" not in caplog.text


def test_oversized_decimal_length_is_bounded_before_integer_conversion():
    app, _, admission = composition()
    headers = [
        ("origin", ORIGIN),
        ("content-type", "application/json"),
        ("idempotency-key", "a" * 32),
    ]
    result = asyncio.run(call(app, headers=headers + [("content-length", "9" * 5000)]))
    assert result["status"] == 413 and result["receives"] == 0 and admission.calls == 0
    result = asyncio.run(
        call(app, headers=headers + [("content-length", "0" * 5000 + str(len(BODY)))])
    )
    assert result["status"] == 201 and admission.calls == 1


@pytest.mark.parametrize(
    "value",
    [
        None,
        {},
        {"allowed": True, "retry_after": 1, "bucket": 1},
        {"allowed": True, "retry_after": 1, "bucket": -1, "now": "2026-09-16T12:00:00Z"},
        {"allowed": True, "retry_after": 0, "bucket": 1, "now": "2026-09-16T12:00:00Z"},
        {"allowed": True, "retry_after": 61, "bucket": 1, "now": "2026-09-16T12:00:00Z"},
        {"allowed": True, "retry_after": 1, "bucket": 1, "now": "invalid"},
        {"allowed": True, "retry_after": 1, "bucket": 1, "now": "2026-09-16T12:00:00"},
        {"allowed": "true", "retry_after": 1, "bucket": 1, "now": "2026-09-16T12:00:00Z"},
    ],
)
def test_ambiguous_backend_result_fails_closed(value):
    with pytest.raises(LimitsUnavailable, match="LIVE_UNAVAILABLE"):
        LimitResult.parse(value)
