"""Mediated Public Live HTTP quotas and committed capability-scoped reads."""

from __future__ import annotations

import hashlib
import hmac
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from sqlalchemy.exc import SQLAlchemyError

from aiscc.persistence.public_live import PublicLiveRepository


class LimitsUnavailable(RuntimeError):
    """Safe condition only; never expose driver errors or credentials."""


class ReadNotFound(ValueError):
    pass


@dataclass(frozen=True)
class LimitResult:
    allowed: bool
    retry_after: int
    bucket: int
    now: datetime

    @classmethod
    def parse(cls, value: Any) -> LimitResult:
        if (
            not isinstance(value, dict)
            or type(value.get("allowed")) is not bool
            or type(value.get("retry_after")) is not int
            or not 1 <= value["retry_after"] <= 60
            or type(value.get("bucket")) is not int
            or value["bucket"] < 0
            or not isinstance(value.get("now"), str)
        ):
            raise LimitsUnavailable("LIVE_UNAVAILABLE")
        try:
            now = datetime.fromisoformat(value["now"])
        except ValueError:
            raise LimitsUnavailable("LIVE_UNAVAILABLE") from None
        if now.tzinfo is None:
            raise LimitsUnavailable("LIVE_UNAVAILABLE")
        return cls(
            value["allowed"],
            value["retry_after"],
            value["bucket"],
            now,
        )


class PublicLiveLimits:
    flood_query = "SELECT public_live_api.flood_consume_retained(:c,:v,:s)"

    def __init__(self, repository: PublicLiveRepository):
        self.repository = repository

    async def flood(self, campaign: str, version: str, source: bytes) -> LimitResult:
        try:
            async with self.repository.transaction() as tx:
                result = LimitResult.parse(
                    await tx._call(self.flood_query, {"c": campaign, "v": version, "s": source})
                )
            return result  # Commit also required for denied ingress accounting.
        except (SQLAlchemyError, OSError, ValueError, RuntimeError, KeyError, TypeError) as exc:
            raise LimitsUnavailable("LIVE_UNAVAILABLE") from exc

    async def read(self, run_id: bytes, capability: bytes) -> tuple[LimitResult, dict[str, Any]]:
        try:
            async with self.repository.transaction() as tx:
                # Existing reviewed composite-row function, never a raw table query.
                row = await tx._call("SELECT to_jsonb(public_live_api.lock_run(:r))", {"r": run_id})
                stored = bytes.fromhex(row["read_hash"][2:])
                valid = hmac.compare_digest(stored, hashlib.sha256(capability).digest())
                if not valid or tx.now >= datetime.fromisoformat(row["read_expires"]):
                    raise ReadNotFound("NOT_FOUND")
                result = LimitResult.parse(
                    await tx._call(
                        "SELECT public_live_api.read_consume_retained(:r)", {"r": run_id}
                    )
                )
                projection = {
                    "state": row["state"],
                    "reason_code": row["state"] if row["state"].startswith("FAILED_") else None,
                    "admitted_at": row["admitted_at"],
                    "updated_at": result.now.isoformat(),
                    "deadline_at": row["deadline"],
                    "mode": "PUBLIC_BOUNDED_LIVE",
                    "scenario_id": "stockroom-s1-normal",
                    "scenario_version": "1.0.0",
                    "result": None,
                }
            return result, projection
        except ReadNotFound:
            raise
        except SQLAlchemyError as exc:
            # lock_run missing row is deliberately indistinguishable from bad capability.
            original = getattr(exc, "orig", None)
            code = getattr(original, "sqlstate", None)
            if code == "P0002" or (code == "P0001" and "READ_EXPIRED" in str(original)):
                hmac.compare_digest(b"\0" * 32, hashlib.sha256(capability).digest())
                raise ReadNotFound("NOT_FOUND") from None
            raise LimitsUnavailable("LIVE_UNAVAILABLE") from exc
        except (OSError, ValueError, RuntimeError, KeyError, TypeError) as exc:
            raise LimitsUnavailable("LIVE_UNAVAILABLE") from exc


class PublicLiveIngressLimits(PublicLiveLimits):
    """Pre-admission flood authority for the frozen hosted campaign.

    The database function validates the exact campaign/version and maintains the
    same authoritative 120/1200 counters without requiring a release campaign
    row. Admission and campaign activation remain separate Human-owned actions.
    """

    flood_query = "SELECT public_live_api.ingress_flood_consume_retained(:c,:v,:s)"
