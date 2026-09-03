from __future__ import annotations

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.exceptions import HTTPException as StarletteHTTPException

from aiscc.api.routes import command_center, control, health
from aiscc.command_center.postgres_queries import PostgresCommandCenterQueries
from aiscc.command_center.queries import CommandCenterQueries, UnavailableCommandCenterQueries
from aiscc.command_center.read_models import ErrorCode
from aiscc.persistence import create_engine, create_session_factory


def _default_command_center_composition() -> tuple[CommandCenterQueries, AsyncEngine | None]:
    database_url = os.environ.get("AISCC_DATABASE_URL")
    if not database_url:
        return UnavailableCommandCenterQueries(), None
    try:
        engine = create_engine(database_url)
    except (SQLAlchemyError, ValueError):
        return UnavailableCommandCenterQueries(), None
    return PostgresCommandCenterQueries(create_session_factory(engine)), engine


def create_app(command_center_queries: CommandCenterQueries | None = None) -> FastAPI:
    owned_engine: AsyncEngine | None = None
    if command_center_queries is None:
        command_center_queries, owned_engine = _default_command_center_composition()

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        try:
            yield
        finally:
            if owned_engine is not None:
                await owned_engine.dispose()

    application = FastAPI(title="AISCC", version="0.1.0", lifespan=lifespan)
    application.state.command_center_queries = command_center_queries
    application.include_router(health.router)
    application.include_router(control.router)
    application.include_router(command_center.router)

    @application.exception_handler(RequestValidationError)
    async def command_center_validation_error(
        request: Request, exception: RequestValidationError
    ) -> Response:
        if request.url.path.startswith("/v1/command-center"):
            return command_center.command_center_error_response(
                ErrorCode.INVALID_QUERY, status_code=400, retryable=False
            )
        return await request_validation_exception_handler(request, exception)

    @application.exception_handler(StarletteHTTPException)
    async def command_center_http_error(
        request: Request, exception: StarletteHTTPException
    ) -> Response:
        if request.url.path.startswith("/v1/command-center"):
            if exception.status_code == 404:
                return command_center.command_center_error_response(
                    ErrorCode.NOT_FOUND, status_code=404, retryable=False
                )
            if exception.status_code == 405:
                return command_center.command_center_error_response(
                    ErrorCode.INVALID_QUERY, status_code=405, retryable=False
                )
        return await http_exception_handler(request, exception)

    return application


app = create_app()
