from __future__ import annotations

import hashlib
import json
from collections.abc import Awaitable
from typing import cast
from uuid import uuid4

from fastapi import APIRouter, Request, Response

from aiscc.command_center.queries import (
    AuthorityConflictReadError,
    CommandCenterQueries,
    InvalidQueryError,
    NoLongerCurrentReadError,
    ProjectionUnavailableReadError,
    QueryResult,
    QueueFilters,
    ReadModelNotFoundError,
    validate_limit,
)
from aiscc.command_center.read_models import (
    CycleData,
    ErrorCode,
    ErrorDetail,
    ErrorEnvelope,
    EvidenceData,
    ExecutionData,
    HumanJudgmentData,
    NextActionData,
    OutcomesData,
    QueueData,
    ReadMeta,
    ReadModel,
    SuccessEnvelope,
    TransitionsData,
    WorkRunData,
)

router = APIRouter(prefix="/v1/command-center", tags=["command-center"])

_QUEUE_QUERY_NAMES = frozenset(
    {
        "workflow_state",
        "execution_status",
        "human_gate_status",
        "judgment_presence",
        "judgment_kind",
        "terminal",
        "q",
        "cursor",
        "limit",
    }
)
_PAGE_QUERY_NAMES = frozenset({"cursor", "limit"})


def command_center_error_response(
    code: ErrorCode,
    *,
    status_code: int,
    retryable: bool,
) -> Response:
    messages = {
        ErrorCode.INVALID_QUERY: "The request query is invalid.",
        ErrorCode.NOT_FOUND: "The requested read model is unavailable.",
        ErrorCode.AUTHORITY_CONFLICT: "The authoritative read model is inconsistent.",
        ErrorCode.NO_LONGER_CURRENT: "The requested read model is no longer current.",
        ErrorCode.PROJECTION_UNAVAILABLE: "The read projection is temporarily unavailable.",
        ErrorCode.INTERNAL_ERROR: "The read request could not be completed.",
    }
    envelope = ErrorEnvelope(
        error=ErrorDetail(
            code=code,
            message=messages[code],
            retryable=retryable,
            correlation_id=f"cc-{uuid4().hex}",
        )
    )
    return Response(
        envelope.model_dump_json(),
        status_code=status_code,
        media_type="application/json",
        headers=_base_headers(),
    )


@router.api_route("/projects/{project_id}/queue", methods=["GET", "HEAD", "OPTIONS"])
async def project_queue(request: Request, project_id: str) -> Response:
    if request.method == "OPTIONS":
        return _options_response()

    async def query() -> QueryResult[QueueData]:
        _require_query_names(request, _QUEUE_QUERY_NAMES)
        return await _queries(request).queue(
            project_id,
            filters=QueueFilters(
                workflow_state=request.query_params.get("workflow_state"),
                execution_status=request.query_params.get("execution_status"),
                human_gate_status=request.query_params.get("human_gate_status"),
                judgment_presence=request.query_params.get("judgment_presence"),
                judgment_kind=request.query_params.get("judgment_kind"),
                terminal=_optional_bool(request.query_params.get("terminal")),
                q=request.query_params.get("q"),
            ),
            cursor=request.query_params.get("cursor"),
            limit=_limit(request),
        )

    return await _serve(request, query())


@router.api_route("/work-runs/{work_run_id}", methods=["GET", "HEAD", "OPTIONS"])
async def work_run(request: Request, work_run_id: str) -> Response:
    if request.method == "OPTIONS":
        return _options_response()

    async def query() -> QueryResult[WorkRunData]:
        _require_query_names(request, frozenset())
        return await _queries(request).work_run(work_run_id)

    return await _serve(request, query())


@router.api_route("/work-runs/{work_run_id}/transitions", methods=["GET", "HEAD", "OPTIONS"])
async def transitions(request: Request, work_run_id: str) -> Response:
    if request.method == "OPTIONS":
        return _options_response()

    async def query() -> QueryResult[TransitionsData]:
        _require_query_names(request, frozenset())
        return await _queries(request).transitions(work_run_id)

    return await _serve(request, query())


@router.api_route("/work-runs/{work_run_id}/execution", methods=["GET", "HEAD", "OPTIONS"])
async def execution(request: Request, work_run_id: str) -> Response:
    if request.method == "OPTIONS":
        return _options_response()

    async def query() -> QueryResult[ExecutionData]:
        _require_query_names(request, frozenset())
        return await _queries(request).execution(work_run_id)

    return await _serve(request, query())


@router.api_route("/work-runs/{work_run_id}/evidence", methods=["GET", "HEAD", "OPTIONS"])
async def evidence(request: Request, work_run_id: str) -> Response:
    if request.method == "OPTIONS":
        return _options_response()

    async def query() -> QueryResult[EvidenceData]:
        _require_query_names(request, frozenset())
        return await _queries(request).evidence(work_run_id)

    return await _serve(request, query())


@router.api_route("/work-runs/{work_run_id}/human-judgment", methods=["GET", "HEAD", "OPTIONS"])
async def human_judgment(request: Request, work_run_id: str) -> Response:
    if request.method == "OPTIONS":
        return _options_response()

    async def query() -> QueryResult[HumanJudgmentData]:
        _require_query_names(request, frozenset())
        return await _queries(request).human_judgment(work_run_id)

    return await _serve(request, query())


@router.api_route("/projects/{project_id}/outcomes", methods=["GET", "HEAD", "OPTIONS"])
async def outcomes(request: Request, project_id: str) -> Response:
    if request.method == "OPTIONS":
        return _options_response()

    async def query() -> QueryResult[OutcomesData]:
        _require_query_names(request, _PAGE_QUERY_NAMES)
        return await _queries(request).outcomes(
            project_id,
            cursor=request.query_params.get("cursor"),
            limit=_limit(request),
        )

    return await _serve(request, query())


@router.api_route("/cycles/{cycle_id}", methods=["GET", "HEAD", "OPTIONS"])
async def cycle(request: Request, cycle_id: str) -> Response:
    if request.method == "OPTIONS":
        return _options_response()

    async def query() -> QueryResult[CycleData]:
        _require_query_names(request, frozenset())
        return await _queries(request).cycle(cycle_id)

    return await _serve(request, query())


@router.api_route("/projects/{project_id}/next-action", methods=["GET", "HEAD", "OPTIONS"])
async def next_action(request: Request, project_id: str) -> Response:
    if request.method == "OPTIONS":
        return _options_response()

    async def query() -> QueryResult[NextActionData]:
        _require_query_names(request, frozenset())
        return await _queries(request).next_action(project_id)

    return await _serve(request, query())


async def _serve[DataT: ReadModel](
    request: Request, awaitable: Awaitable[QueryResult[DataT]]
) -> Response:
    try:
        result = await awaitable
        return _success_response(request, result)
    except InvalidQueryError:
        return command_center_error_response(
            ErrorCode.INVALID_QUERY, status_code=400, retryable=False
        )
    except ReadModelNotFoundError:
        return command_center_error_response(ErrorCode.NOT_FOUND, status_code=404, retryable=False)
    except AuthorityConflictReadError:
        return command_center_error_response(
            ErrorCode.AUTHORITY_CONFLICT, status_code=409, retryable=False
        )
    except NoLongerCurrentReadError:
        return command_center_error_response(
            ErrorCode.NO_LONGER_CURRENT, status_code=409, retryable=False
        )
    except ProjectionUnavailableReadError:
        return command_center_error_response(
            ErrorCode.PROJECTION_UNAVAILABLE, status_code=503, retryable=True
        )
    except Exception:
        return command_center_error_response(
            ErrorCode.INTERNAL_ERROR, status_code=500, retryable=False
        )


def _success_response[DataT: ReadModel](request: Request, result: QueryResult[DataT]) -> Response:
    envelope = SuccessEnvelope[DataT](
        data=result.data,
        meta=ReadMeta(
            snapshot_at=result.snapshot_at,
            source_revisions=result.source_revisions,
            next_cursor=result.next_cursor,
            poll_after_ms=result.poll_after_ms,
        ),
    )
    stable = {
        "schema_version": envelope.meta.schema_version,
        "data": envelope.data.model_dump(mode="json"),
        "source_revisions": envelope.meta.source_revisions,
        "next_cursor": envelope.meta.next_cursor,
    }
    encoded = json.dumps(stable, sort_keys=True, separators=(",", ":")).encode("utf-8")
    etag = f'"{hashlib.sha256(encoded).hexdigest()}"'
    headers = {**_base_headers(), "ETag": etag}
    if etag in _if_none_match_values(request.headers.get("if-none-match")):
        return Response(status_code=304, headers=headers)
    if request.method == "HEAD":
        return Response(status_code=200, headers=headers, media_type="application/json")
    return Response(
        envelope.model_dump_json(),
        status_code=200,
        media_type="application/json",
        headers=headers,
    )


def _queries(request: Request) -> CommandCenterQueries:
    return cast(CommandCenterQueries, request.app.state.command_center_queries)


def _limit(request: Request) -> int:
    raw = request.query_params.get("limit", "50")
    try:
        value = int(raw)
    except ValueError as exc:
        raise InvalidQueryError("limit must be an integer") from exc
    if str(value) != raw:
        raise InvalidQueryError("limit must use canonical integer syntax")
    return validate_limit(value)


def _optional_bool(raw: str | None) -> bool | None:
    if raw is None:
        return None
    if raw == "true":
        return True
    if raw == "false":
        return False
    raise InvalidQueryError("terminal must be true or false")


def _require_query_names(request: Request, accepted: frozenset[str]) -> None:
    if any(key not in accepted for key in request.query_params):
        raise InvalidQueryError("query parameter is not accepted")


def _if_none_match_values(value: str | None) -> frozenset[str]:
    if value is None:
        return frozenset()
    return frozenset(item.strip() for item in value.split(","))


def _base_headers() -> dict[str, str]:
    return {
        "Cache-Control": "private, no-cache",
        "X-AISCC-Exposure": "LOCAL_PRIVATE_ONLY",
    }


def _options_response() -> Response:
    return Response(
        status_code=204,
        headers={**_base_headers(), "Allow": "GET, HEAD, OPTIONS"},
    )
