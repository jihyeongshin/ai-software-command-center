"""Isolated public ASGI composition. No owner application or environment binding.

The default factory is fail-closed. Positive local bindings require server-owned
direct-peer provenance; hosted proxy/transport configuration remains L5 authority.
"""

from __future__ import annotations

import base64
import binascii
import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Protocol

from sqlalchemy.exc import SQLAlchemyError
from starlette.requests import ClientDisconnect, Request
from starlette.responses import Response
from starlette.types import Receive, Scope, Send

from aiscc.persistence.public_live_limits import LimitsUnavailable, PublicLiveLimits, ReadNotFound
from aiscc.public_live.identity import AdmissionDenied, request_identity
from aiscc.public_live.service import AdmissionService
from aiscc.public_live.source import TrustedSource

ORIGIN = "https://aiscc-replay.pages.dev"
ROOT = "/v1/public-live/runs"
ALLOWED_HEADERS = {"content-type", "idempotency-key", "x-run-read-capability"}
ERRORS = {
    "INVALID_REQUEST": (400, False),
    "BODY_TOO_LARGE": (413, False),
    "UNSUPPORTED_MEDIA": (415, False),
    "HEADERS_TOO_LARGE": (431, False),
    "ORIGIN_DENIED": (403, False),
    "CLIENT_BINDING_DENIED": (403, False),
    "NOT_FOUND": (404, False),
    "METHOD_NOT_ALLOWED": (405, False),
    "IDEMPOTENCY_CONFLICT": (409, False),
    "IDEMPOTENCY_EXPIRED": (410, False),
    "CLIENT_RATE_LIMIT": (429, True),
    "GLOBAL_DAY_LIMIT": (429, True),
    "READ_RATE_LIMIT": (429, True),
    "CAPACITY_UNAVAILABLE": (503, True),
    "DB_UNAVAILABLE": (503, True),
    "COMMIT_OUTCOME_UNKNOWN": (503, True),
    "LIVE_UNAVAILABLE": (503, True),
    "IDENTITY_UNAVAILABLE": (503, False),
    "LIVE_DISABLED": (503, False),
    "BUDGET_UNAVAILABLE": (503, False),
    "CAMPAIGN_CLOSED": (503, False),
    "POLICY_UNAVAILABLE": (503, False),
    "INTERNAL_ERROR": (500, False),
}


def encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def decode(value: str, size: int) -> bytes:
    if re.fullmatch(r"[A-Za-z0-9_-]+", value) is None:
        raise ReadNotFound("NOT_FOUND")
    try:
        raw = base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))
    except (ValueError, binascii.Error):
        raise ReadNotFound("NOT_FOUND") from None
    if len(raw) != size or encode(raw) != value:
        raise ReadNotFound("NOT_FOUND")
    return raw


def timestamp(value: str | datetime) -> str:
    stamp = datetime.fromisoformat(value) if isinstance(value, str) else value
    if stamp.tzinfo is None:
        raise ValueError("INVALID_DB_TIME")
    return stamp.astimezone(UTC).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class LocalAdmissionBinding:
    """Explicit in-process bridge to unchanged L2 identity validation.

    trusted_peer is a server-supplied local bridge peer covered by the L2 policy.
    The sole forwarded value is constructed from the verified direct socket
    source, never copied from request headers. This is not hosted proxy proof.
    """

    service: AdmissionService
    trusted_peer: str

    async def admit(self, body: bytes, key: str, source: TrustedSource) -> Any:
        if (source.campaign, source.key_version) != (
            self.service.identity.campaign_id,
            self.service.identity.key_version,
        ):
            raise AdmissionDenied("IDENTITY_UNAVAILABLE")
        return await self.service.admit(
            body,
            key,
            peer=self.trusted_peer,
            headers=(("X-Forwarded-For", source.address),),
        )


class SourceAuthority(Protocol):
    def derive(self, scope: Scope) -> TrustedSource: ...


class PublicLiveApp:
    def __init__(
        self,
        source: SourceAuthority | None,
        limits: PublicLiveLimits | None,
        admission: LocalAdmissionBinding | None,
    ) -> None:
        self.source, self.limits, self.admission = source, limits, admission

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "lifespan":
            while True:
                message = await receive()
                if message["type"] == "lifespan.startup":
                    await send({"type": "lifespan.startup.complete"})
                elif message["type"] == "lifespan.shutdown":
                    await send({"type": "lifespan.shutdown.complete"})
                    return
        if scope["type"] != "http":
            await send({"type": "websocket.close", "code": 1008})
            return
        headers = scope.get("headers", [])

        def values(name: str) -> list[str]:
            return [v.decode("latin-1") for k, v in headers if k.lower() == name.encode()]

        cors = values("origin") == [ORIGIN]
        safe_headers = {"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff"}
        if cors:
            safe_headers.update({"Access-Control-Allow-Origin": ORIGIN, "Vary": "Origin"})

        def response(
            status: int, payload: Any = None, extra: dict[str, str] | None = None
        ) -> Response:
            body = (
                b""
                if payload is None
                else json.dumps(
                    payload, separators=(",", ":"), ensure_ascii=False, allow_nan=False
                ).encode("utf-8")
            )
            if len(body) > 16384:
                raise ValueError("PROJECTION_TOO_LARGE")
            return Response(
                body, status, safe_headers | (extra or {}), media_type="application/json"
            )

        def error(code: str, retry: int | None = None) -> Response:
            code = code if code in ERRORS else "INTERNAL_ERROR"
            status, retryable = ERRORS[code]
            return response(
                status,
                {"error": {"code": code, "retryable": retryable}},
                {"Retry-After": str(retry)} if retry is not None else None,
            )

        def one(name: str, missing: str = "INVALID_REQUEST") -> str:
            found = values(name)
            if len(found) != 1:
                raise AdmissionDenied(missing)
            return found[0]

        async def dispatch() -> Response:
            path = scope.get("path", "")
            if path == "/health":
                if scope.get("method") != "GET":
                    return error("METHOD_NOT_ALLOWED")
                return response(200, {"status": "ok"})
            if not path.startswith("/v1/public-live/"):
                return error("NOT_FOUND")
            if self.source is None:
                return error("IDENTITY_UNAVAILABLE")
            source = self.source.derive(scope)
            if self.limits is None:
                return error("LIVE_UNAVAILABLE")
            flood = await self.limits.flood(source.campaign, source.key_version, source.bucket)
            if not flood.allowed:
                return error("CLIENT_RATE_LIMIT", flood.retry_after)
            # Flood has committed before all remaining parsing/authorization work.
            if sum(len(k) + len(v) + 4 for k, v in headers) > 8192:
                return error("HEADERS_TOO_LARGE")
            if not cors:
                return error("ORIGIN_DENIED")
            if not source.transport_secure:
                return error("INVALID_REQUEST")  # No redirects or forwarded-proto authority.
            is_run = path.startswith(ROOT + "/") and "/" not in path[len(ROOT) + 1 :]
            if path != ROOT and not is_run:
                return error("NOT_FOUND")
            if scope.get("query_string"):
                return error("INVALID_REQUEST")
            method = scope["method"]
            if method == "OPTIONS":
                allowed_method = "GET" if is_run else "POST"
                if one("access-control-request-method", "ORIGIN_DENIED") != allowed_method:
                    return error("ORIGIN_DENIED")
                requested = values("access-control-request-headers")
                if len(requested) > 1:
                    return error("ORIGIN_DENIED")
                if requested and any(
                    h.strip().lower() not in ALLOWED_HEADERS for h in requested[0].split(",")
                ):
                    return error("ORIGIN_DENIED")
                return response(
                    204,
                    extra={
                        "Access-Control-Allow-Methods": f"{allowed_method}, OPTIONS",
                        "Access-Control-Allow-Headers": (
                            "Content-Type, Idempotency-Key, X-Run-Read-Capability"
                        ),
                        "Access-Control-Max-Age": "300",
                    },
                )
            if method != ("GET" if is_run else "POST"):
                return error("METHOD_NOT_ALLOWED")
            if is_run:
                run = decode(path[len(ROOT) + 1 :], 16)
                capability = decode(one("x-run-read-capability", "NOT_FOUND"), 32)
                limit, projection = await self.limits.read(run, capability)
                if not limit.allowed:
                    return error("READ_RATE_LIMIT", limit.retry_after)
                for name in ("admitted_at", "updated_at", "deadline_at"):
                    projection[name] = timestamp(projection[name])
                return response(200, {"run_id": encode(run), **projection})
            if values("content-encoding"):
                return error("UNSUPPORTED_MEDIA")
            media = one("content-type", "UNSUPPORTED_MEDIA")
            if re.fullmatch(r"application/json(?:\s*;\s*charset=utf-8)?", media, re.I) is None:
                return error("UNSUPPORTED_MEDIA")
            key = one("idempotency-key")
            if re.fullmatch(r"[0-9a-f]{32}", key) is None:
                return error("INVALID_REQUEST")
            lengths = values("content-length")
            if len(lengths) > 1 or (lengths and not re.fullmatch(r"[0-9]+", lengths[0])):
                return error("INVALID_REQUEST")
            length = (lengths[0].lstrip("0") or "0") if lengths else None
            if length is not None and (len(length) > 4 or int(length) > 1024):
                return error("BODY_TOO_LARGE")
            body = bytearray()
            async for chunk in Request(scope, receive).stream():
                if len(body) + len(chunk) > 1024:
                    return error("BODY_TOO_LARGE")
                body.extend(chunk)
            if length is not None and len(body) != int(length):
                return error("INVALID_REQUEST")
            # Validate before binding; L2 repeats this with its actual server-owned pins.
            request_identity(bytes(body), key, b"\0" * 32, b"\0" * 32)
            if self.admission is None:
                return error("LIVE_DISABLED")
            try:
                receipt = await self.admission.admit(bytes(body), key, source)
            except (SQLAlchemyError, OSError):
                # A transport/driver exception may follow a committed transaction.
                # Never infer rollback or expose a token before confirmed return.
                return error("COMMIT_OUTCOME_UNKNOWN")
            if receipt.replayed:
                return response(202, {"run_id": encode(receipt.run_id), "replayed": True})
            return response(
                201,
                {
                    "run_id": encode(receipt.run_id),
                    "state": "ADMITTED",
                    "read_capability": encode(receipt.read_capability),
                    "read_expires_at": timestamp(receipt.read_expires_at),
                    "replayed": False,
                },
            )

        try:
            result = await dispatch()
        except AdmissionDenied as exc:
            result = error(str(exc))
        except ReadNotFound:
            result = error("NOT_FOUND")
        except LimitsUnavailable:
            result = error("LIVE_UNAVAILABLE")
        except ClientDisconnect:
            return
        except Exception:
            result = error("INTERNAL_ERROR")  # No raw error/input logging or reflection.
        await result(scope, receive, send)


def create_app(
    *,
    source: SourceAuthority | None = None,
    limits: PublicLiveLimits | None = None,
    admission: LocalAdmissionBinding | None = None,
) -> PublicLiveApp:
    return PublicLiveApp(source, limits, admission)
