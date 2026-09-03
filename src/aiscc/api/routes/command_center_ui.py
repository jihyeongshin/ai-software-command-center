from __future__ import annotations

from fastapi import APIRouter, Response
from fastapi.responses import HTMLResponse

from aiscc.command_center.web import (
    APP_CSS,
    APP_JS,
    render_landing_page,
    render_project_page,
    render_work_run_page,
    security_headers,
)

router = APIRouter(tags=["command-center-ui"])


@router.get("/command-center", response_class=HTMLResponse)
async def command_center_landing() -> HTMLResponse:
    return HTMLResponse(render_landing_page(), headers=security_headers(html=True))


@router.get("/command-center/projects/{project_id}", response_class=HTMLResponse)
async def command_center_project(project_id: str) -> HTMLResponse:
    return HTMLResponse(render_project_page(project_id), headers=security_headers(html=True))


@router.get("/command-center/work-runs/{work_run_id}", response_class=HTMLResponse)
async def command_center_work_run(work_run_id: str) -> HTMLResponse:
    return HTMLResponse(render_work_run_page(work_run_id), headers=security_headers(html=True))


@router.get("/command-center/assets/app.css")
async def command_center_css() -> Response:
    return Response(APP_CSS, media_type="text/css", headers=security_headers())


@router.get("/command-center/assets/app.js")
async def command_center_javascript() -> Response:
    return Response(APP_JS, media_type="application/javascript", headers=security_headers())
