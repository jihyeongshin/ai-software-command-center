from __future__ import annotations

from fastapi import FastAPI

from aiscc.api.routes import control, health


def create_app() -> FastAPI:
    application = FastAPI(title="AISCC", version="0.1.0")
    application.include_router(health.router)
    application.include_router(control.router)
    return application


app = create_app()
