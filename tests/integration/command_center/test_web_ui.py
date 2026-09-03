from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from typing import Any, cast

import pytest
from fastapi.testclient import TestClient
from test_postgres_read_api import (
    _DefaultEntrypointServer,
    _event_counts,
    _seed,
    run,
)

from aiscc.api.app import create_app
from aiscc.command_center.queries import CommandCenterQueries, QueryResult, QueueFilters
from aiscc.command_center.read_models import (
    ExecutionSummaryView,
    HumanGateSummaryView,
    HumanResultSummaryView,
    JudgmentSummaryView,
    NextActionSummaryView,
    Presence,
    QueueData,
    QueueRow,
    TaskContractView,
    TaskDisplayView,
    TransitionDecisionSummaryView,
    WorkflowView,
)
from aiscc.contracts.workflow import RuntimeMode, WorkflowState

NOW = datetime(2026, 9, 3, 5, 0, tzinfo=UTC)
SECURITY_HEADERS = {
    "x-aiscc-exposure": "LOCAL_PRIVATE_ONLY",
    "x-content-type-options": "nosniff",
    "referrer-policy": "no-referrer",
    "cache-control": "no-store",
}


class QueueQuerySpy:
    def __init__(self) -> None:
        self.calls: list[tuple[str, QueueFilters, str | None, int]] = []

    async def queue(
        self,
        project_id: str,
        *,
        filters: QueueFilters,
        cursor: str | None,
        limit: int,
    ) -> QueryResult[QueueData]:
        self.calls.append((project_id, filters, cursor, limit))
        return QueryResult(
            data=QueueData(
                project_id=project_id,
                items=(
                    QueueRow(
                        project_id=project_id,
                        work_run_id="run-ui-1",
                        task_contract=TaskContractView(id="task-ui-1", version="v1"),
                        task_display=TaskDisplayView(),
                        workflow=WorkflowView(
                            state=WorkflowState.RUNNING,
                            state_version=2,
                            updated_at=NOW,
                        ),
                        execution=ExecutionSummaryView(attempt_present=False),
                        human_gate=HumanGateSummaryView(presence=Presence.NONE),
                        human_result=HumanResultSummaryView(presence=Presence.NONE),
                        judgment=JudgmentSummaryView(presence=Presence.NONE),
                        latest_transition_decision=TransitionDecisionSummaryView(
                            presence=Presence.NONE
                        ),
                        next_action=NextActionSummaryView(presence=Presence.NONE),
                        runtime_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
                    ),
                ),
            ),
            snapshot_at=NOW,
            source_revisions={"transition_event_sequence": 7},
        )

    def __getattr__(self, name: str) -> Any:
        raise AssertionError(f"unexpected read query: {name}")


def _assert_security_headers(response: Any, *, html: bool = False) -> None:
    for name, value in SECURITY_HEADERS.items():
        assert response.headers[name] == value
    if html:
        csp = response.headers["content-security-policy"]
        assert "default-src 'self'" in csp
        assert "script-src 'self'" in csp
        assert "unsafe-eval" not in csp
        assert "http:" not in csp and "https:" not in csp


def test_ui_http_routes_render_without_invoking_server_side_queries() -> None:
    queries = QueueQuerySpy()
    with TestClient(create_app(cast(CommandCenterQueries, queries))) as client:
        responses = (
            client.get("/command-center"),
            client.get("/command-center/projects/project-ui"),
            client.get("/command-center/assets/app.css"),
            client.get("/command-center/assets/app.js"),
        )
    assert queries.calls == []
    assert all(response.status_code == 200 for response in responses)
    assert responses[0].headers["content-type"].startswith("text/html")
    assert responses[1].headers["content-type"].startswith("text/html")
    assert responses[2].headers["content-type"].startswith("text/css")
    assert responses[3].headers["content-type"].startswith("application/javascript")
    assert '<html lang="ko">' in responses[0].text
    assert '<html lang="ko">' in responses[1].text
    assert "알고 있는 Project ID 열기" in responses[0].text
    assert "큐 필터" in responses[1].text
    assert 'class="project-id-field"' in responses[0].text
    assert 'id="queue-list" class="work-run-list"' in responses[1].text
    assert "<table" not in responses[1].text
    assert 'class="label-primary">워크플로</span>' in responses[1].text
    assert 'class="label-technical">WorkflowState</span>' in responses[1].text
    assert 'document.createElement("article")' in responses[3].text
    assert 'target.focus({ preventScroll: true })' in responses[3].text
    _assert_security_headers(responses[0], html=True)
    _assert_security_headers(responses[1], html=True)
    _assert_security_headers(responses[2])
    _assert_security_headers(responses[3])


def test_ui_mutation_methods_are_rejected_with_security_boundary() -> None:
    queries = QueueQuerySpy()
    paths = (
        "/command-center",
        "/command-center/projects/project-ui",
        "/command-center/assets/app.css",
        "/command-center/assets/app.js",
    )
    with TestClient(create_app(cast(CommandCenterQueries, queries))) as client:
        for path in paths:
            for method in ("post", "put", "patch", "delete"):
                response = getattr(client, method)(path)
                assert response.status_code == 405
                _assert_security_headers(
                    response,
                    html=not path.startswith("/command-center/assets/"),
                )
    assert queries.calls == []


def test_exact_queue_api_filters_and_etag_remain_the_only_data_path() -> None:
    queries = QueueQuerySpy()
    app = create_app(cast(CommandCenterQueries, queries))
    with TestClient(app) as client:
        page = client.get("/command-center/projects/project-ui")
        assert page.status_code == 200
        assert queries.calls == []
        queue = client.get(
            "/v1/command-center/projects/project-ui/queue",
            params={
                "workflow_state": "RUNNING",
                "execution_status": "EXECUTOR_COMPLETED",
                "human_gate_status": "OPEN",
                "judgment_presence": "NONE",
                "judgment_kind": "ACCEPTED",
                "terminal": "false",
                "q": "run-ui",
                "limit": "25",
            },
        )
        assert queue.status_code == 200
        queue_payload = queue.json()
        assert queue_payload["data"]["items"][0]["workflow"]["state"] == "RUNNING"
        assert queue_payload["data"]["items"][0]["runtime_mode"] == "OWNER_SELF_DOGFOOD"
        etag = queue.headers["etag"]
        unchanged = client.get(
            "/v1/command-center/projects/project-ui/queue",
            params={
                "workflow_state": "RUNNING",
                "execution_status": "EXECUTOR_COMPLETED",
                "human_gate_status": "OPEN",
                "judgment_presence": "NONE",
                "judgment_kind": "ACCEPTED",
                "terminal": "false",
                "q": "run-ui",
                "limit": "25",
            },
            headers={"If-None-Match": etag},
        )
    assert unchanged.status_code == 304
    assert unchanged.content == b""
    assert len(queries.calls) == 2
    project_id, filters, cursor, limit = queries.calls[0]
    assert project_id == "project-ui"
    assert filters == QueueFilters(
        workflow_state="RUNNING",
        execution_status="EXECUTOR_COMPLETED",
        human_gate_status="OPEN",
        judgment_presence="NONE",
        judgment_kind="ACCEPTED",
        terminal=False,
        q="run-ui",
    )
    assert cursor is None and limit == 25


@pytest.mark.postgres
def test_default_entrypoint_ui_queue_etag_and_event_no_mutation() -> None:
    database_url = os.environ.get("AISCC_TEST_DATABASE_URL")
    if not database_url:
        pytest.skip("AISCC_TEST_DATABASE_URL is required for PostgreSQL UI evidence")
    seeded = run(_seed(database_url))
    project_id = seeded["project_id"]
    accepted_run_id = seeded["accepted_run_id"]
    before = run(_event_counts(database_url, project_id))

    with _DefaultEntrypointServer(database_url) as server:
        ui_paths = (
            "/command-center",
            f"/command-center/projects/{project_id}",
            "/command-center/assets/app.css",
            "/command-center/assets/app.js",
        )
        for path in ui_paths:
            status, headers, body = server.request(path)
            assert status == 200
            assert headers["x-aiscc-exposure"] == "LOCAL_PRIVATE_ONLY"
            assert headers["x-content-type-options"] == "nosniff"
            assert headers["referrer-policy"] == "no-referrer"
            assert headers["cache-control"] == "no-store"
            if path in ui_paths[:2]:
                assert b'<html lang="ko">' in body
            if path == f"/command-center/projects/{project_id}":
                assert f'data-project-id="{project_id}"'.encode() in body
                assert b'id="queue-list" class="work-run-list"' in body
                assert b"<table" not in body
            if path == "/command-center/assets/app.js":
                assert b'document.createElement("article")' in body
                assert b'target.focus({ preventScroll: true })' in body

        queue_path = f"/v1/command-center/projects/{project_id}/queue"
        filtered_path = (
            f"{queue_path}?workflow_state=ACCEPTED&terminal=true"
            f"&q={accepted_run_id}&limit=25"
        )
        status, headers, body = server.request(filtered_path)
        assert status == 200
        payload = json.loads(body)
        assert [item["work_run_id"] for item in payload["data"]["items"]] == [
            accepted_run_id
        ]
        etag = headers["etag"]
        not_modified = server.request(filtered_path, headers={"If-None-Match": etag})
        assert not_modified[0] == 304 and not_modified[2] == b""

        for path in (*ui_paths, queue_path, filtered_path):
            assert server.request(path)[0] == 200
        for path in ui_paths:
            for method in ("POST", "PUT", "PATCH", "DELETE"):
                assert server.request(path, method=method)[0] == 405

    after = run(_event_counts(database_url, project_id))
    assert after == before
