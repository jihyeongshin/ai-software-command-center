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
    BlockerView,
    EvidenceData,
    ExecutionData,
    ExecutionSummaryView,
    HumanGateSummaryView,
    HumanGateView,
    HumanJudgmentData,
    HumanResultSummaryView,
    HumanResultView,
    JudgmentSummaryView,
    JudgmentView,
    NextActionSummaryView,
    Presence,
    QueueData,
    QueueRow,
    ScopeView,
    TaskConstraintView,
    TaskContractView,
    TaskDisplayView,
    TransitionDecisionSummaryView,
    TransitionEffectView,
    TransitionsData,
    WorkflowView,
    WorkRunData,
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
        self.detail_calls: list[tuple[str, str]] = []

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

    async def work_run(self, work_run_id: str) -> QueryResult[WorkRunData]:
        self.detail_calls.append(("summary", work_run_id))
        return QueryResult(
            data=WorkRunData(
                project_id="project-ui",
                work_run_id=work_run_id,
                task_contract=TaskContractView(id="task-ui-1", version="v1"),
                runtime_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
                workflow=WorkflowView(
                    state=WorkflowState.RUNNING,
                    state_version=2,
                    updated_at=NOW,
                ),
                task_constraint=TaskConstraintView(presence=Presence.NONE),
                task_display=TaskDisplayView(),
                scope=ScopeView(),
                blocker=BlockerView(presence=Presence.NONE),
            ),
            snapshot_at=NOW,
            source_revisions={"transition_event_sequence": 7},
        )

    async def transitions(self, work_run_id: str) -> QueryResult[TransitionsData]:
        self.detail_calls.append(("transitions", work_run_id))
        return QueryResult(
            data=TransitionsData(work_run_id=work_run_id, items=()),
            snapshot_at=NOW,
            source_revisions={"transition_event_sequence": 7},
        )

    async def execution(self, work_run_id: str) -> QueryResult[ExecutionData]:
        self.detail_calls.append(("execution", work_run_id))
        return QueryResult(
            data=ExecutionData(work_run_id=work_run_id, attempts=()),
            snapshot_at=NOW,
            source_revisions={"execution_event_sequence": 3},
        )

    async def evidence(self, work_run_id: str) -> QueryResult[EvidenceData]:
        self.detail_calls.append(("evidence", work_run_id))
        return QueryResult(
            data=EvidenceData(
                work_run_id=work_run_id,
                requirement_sets=(),
                checkpoints=(),
                requirements=(),
                candidates=(),
                admission_decisions=(),
                admitted_evidence=(),
                satisfactions=(),
                set_evaluations=(),
                set_attestations=(),
            ),
            snapshot_at=NOW,
            source_revisions={"evidence_authority_revision": 4},
        )

    async def human_judgment(self, work_run_id: str) -> QueryResult[HumanJudgmentData]:
        self.detail_calls.append(("human-judgment", work_run_id))
        return QueryResult(
            data=HumanJudgmentData(
                work_run_id=work_run_id,
                human_gate=HumanGateView(presence=Presence.NONE),
                human_result=HumanResultView(presence=Presence.NONE),
                judgment=JudgmentView(presence=Presence.NONE),
                transition_effect=TransitionEffectView(presence=Presence.NONE),
            ),
            snapshot_at=NOW,
            source_revisions={"workflow_state_version": 2},
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
            client.get("/command-center/work-runs/run-ui-1"),
            client.get("/command-center/assets/app.css"),
            client.get("/command-center/assets/app.js"),
        )
    assert queries.calls == []
    assert all(response.status_code == 200 for response in responses)
    assert responses[0].headers["content-type"].startswith("text/html")
    assert responses[1].headers["content-type"].startswith("text/html")
    assert responses[2].headers["content-type"].startswith("text/html")
    assert responses[3].headers["content-type"].startswith("text/css")
    assert responses[4].headers["content-type"].startswith("application/javascript")
    assert '<html lang="ko">' in responses[0].text
    assert '<html lang="ko">' in responses[1].text
    assert "알고 있는 Project ID 열기" in responses[0].text
    assert "큐 필터" in responses[1].text
    assert 'class="project-id-field"' in responses[0].text
    assert 'id="queue-list" class="work-run-list"' in responses[1].text
    assert "<table" not in responses[1].text
    assert 'class="label-primary">워크플로</span>' in responses[1].text
    assert 'class="label-technical">WorkflowState</span>' in responses[1].text
    assert '<html lang="ko">' in responses[2].text
    assert "WorkRun 상세" in responses[2].text
    assert 'id="evidence-state"' in responses[2].text
    assert 'id="human-judgment-state"' in responses[2].text
    assert 'document.createElement("article")' in responses[4].text
    assert 'target.focus({ preventScroll: true })' in responses[4].text
    _assert_security_headers(responses[0], html=True)
    _assert_security_headers(responses[1], html=True)
    _assert_security_headers(responses[2], html=True)
    _assert_security_headers(responses[3])
    _assert_security_headers(responses[4])


def test_ui_mutation_methods_are_rejected_with_security_boundary() -> None:
    queries = QueueQuerySpy()
    paths = (
        "/command-center",
        "/command-center/projects/project-ui",
        "/command-center/work-runs/run-ui-1",
        "/command-center/cycles/cycle-ui-1",
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


def test_detail_read_endpoints_have_independent_etags_and_empty_states() -> None:
    queries = QueueQuerySpy()
    with TestClient(create_app(cast(CommandCenterQueries, queries))) as client:
        paths = (
            "/v1/command-center/work-runs/run-ui-1",
            "/v1/command-center/work-runs/run-ui-1/transitions",
            "/v1/command-center/work-runs/run-ui-1/execution",
            "/v1/command-center/work-runs/run-ui-1/evidence",
            "/v1/command-center/work-runs/run-ui-1/human-judgment",
        )
        first = [client.get(path) for path in paths]
        unchanged = [
            client.get(path, headers={"If-None-Match": response.headers["etag"]})
            for path, response in zip(paths, first, strict=True)
        ]
    assert all(response.status_code == 200 for response in first)
    assert all(response.status_code == 304 and response.content == b"" for response in unchanged)
    assert first[0].json()["data"]["workflow"]["state"] == "RUNNING"
    assert first[1].json()["data"]["items"] == []
    assert first[2].json()["data"]["attempts"] == []
    assert first[3].json()["data"]["requirement_sets"] == []
    assert first[3].json()["data"]["candidates"] == []
    assert first[3].json()["data"]["admitted_evidence"] == []
    assert first[4].json()["data"]["human_gate"]["presence"] == "NONE"
    assert first[4].json()["data"]["human_result"]["presence"] == "NONE"
    assert first[4].json()["data"]["judgment"]["presence"] == "NONE"
    assert first[4].json()["data"]["transition_effect"]["presence"] == "NONE"
    assert queries.detail_calls == [
        ("summary", "run-ui-1"),
        ("transitions", "run-ui-1"),
        ("execution", "run-ui-1"),
        ("evidence", "run-ui-1"),
        ("human-judgment", "run-ui-1"),
        ("summary", "run-ui-1"),
        ("transitions", "run-ui-1"),
        ("execution", "run-ui-1"),
        ("evidence", "run-ui-1"),
        ("human-judgment", "run-ui-1"),
    ]


def test_cycle_shell_is_query_free_and_project_integration_uses_local_assets() -> None:
    queries = QueueQuerySpy()
    with TestClient(create_app(cast(CommandCenterQueries, queries))) as client:
        cycle = client.get("/command-center/cycles/cycle-ui-1")
        project = client.get("/command-center/projects/project-ui")
        script = client.get("/command-center/assets/app.js")
    assert cycle.status_code == project.status_code == script.status_code == 200
    assert queries.calls == queries.detail_calls == []
    assert 'data-cycle-id="cycle-ui-1"' in cycle.text
    assert "Cycle 계보" in cycle.text
    assert 'id="cycle-content"' in cycle.text
    assert 'id="next-action-content"' in project.text
    assert 'id="outcomes-content"' in project.text
    assert "현재 프로젝트 메모리 맥락" in script.text
    assert 'readLink("cycles", cycle.cycle_id' in script.text
    _assert_security_headers(cycle, html=True)
    _assert_security_headers(project, html=True)


def _assert_cycle_next_action_runtime(
    server: _DefaultEntrypointServer, seeded: dict[str, str]
) -> dict[str, Any]:
    """Exercise existing normal-entrypoint harness; return only safe evidence metadata."""
    project_id = seeded["project_id"]
    cycle_id = seeded["cycle_id"]
    observations: dict[str, Any] = {"project_id": project_id, "cycle_id": cycle_id, "reads": []}
    for path in (
        "/command-center",
        f"/command-center/projects/{project_id}",
        f"/command-center/cycles/{cycle_id}",
    ):
        status, headers, body = server.request(path)
        assert status == 200
        assert b'<html lang="ko">' in body
        assert headers["x-aiscc-exposure"] == "LOCAL_PRIVATE_ONLY"
        assert "unsafe-inline" not in headers["content-security-policy"]
        observations["reads"].append({"path": path, "status": status})
    script_status, _, script = server.request("/command-center/assets/app.js")
    assert script_status == 200
    assert b'readLink("cycles", cycle.cycle_id' in script
    assert b'nextActionSection.read(projectApi + "/next-action")' in script
    api_paths = {
        "outcomes": f"/v1/command-center/projects/{project_id}/outcomes",
        "cycle": f"/v1/command-center/cycles/{cycle_id}",
        "next_action": f"/v1/command-center/projects/{project_id}/next-action",
    }
    payloads: dict[str, Any] = {}
    for key, path in api_paths.items():
        status, headers, body = server.request(path)
        assert status == 200
        assert headers["x-aiscc-exposure"] == "LOCAL_PRIVATE_ONLY"
        assert "etag" in headers
        assert b"DO_NOT_EXPORT" not in body
        payloads[key] = json.loads(body)["data"]
        unchanged = server.request(path, headers={"If-None-Match": headers["etag"]})
        assert unchanged[0] == 304 and unchanged[2] == b""
        # Query rejection is a read-only failure hook; subsequent read must recover.
        invalid_status, _, invalid_body = server.request(path + "?unexpected=1")
        assert invalid_status == 400
        assert json.loads(invalid_body)["error"]["code"] == "INVALID_QUERY"
        recovery_status, recovery_headers, recovery_body = server.request(path)
        assert recovery_status == 200
        assert json.loads(recovery_body)["data"] == payloads[key]
        assert recovery_headers["etag"] == headers["etag"]
        assert server.request(path, headers={"If-None-Match": headers["etag"]})[0] == 304
        observations["reads"].append({
            "path": path, "status": status, "own_etag_status": unchanged[0],
            "failure_status": invalid_status, "recovery_status": recovery_status,
            "recovery_data_equal": True, "recovery_etag_equal": True,
        })
    outcomes = payloads["outcomes"]["items"]
    admitted = next(item for item in outcomes if item["work_run_id"] == seeded["accepted_run_id"])
    assert admitted["admitted_cycle"]["presence"] == "PRESENT"
    assert admitted["admitted_cycle"]["cycle_id"] == cycle_id
    assert admitted["admitted_cycle"]["cycle_ref"] == payloads["cycle"]["cycle_ref"]
    assert any(item["admitted_cycle"]["presence"] == "NONE" for item in outcomes)
    assert payloads["cycle"]["project_id"] == project_id
    assert payloads["cycle"]["work_run_id"] == seeded["accepted_run_id"]
    assert payloads["cycle"]["current_memory"][0]["applicability"] == "CURRENT"
    assert payloads["next_action"]["selection"]["selection_id"] == seeded["selection_id"]
    assert payloads["next_action"]["task_issuance_candidate"]["presence"] == "PRESENT"
    for path in (
        "/v1/command-center/cycles/missing-p2-1e-cycle",
        "/v1/command-center/projects/missing-p2-1e-project/next-action",
    ):
        status, _, body = server.request(path)
        assert status == 404 and json.loads(body)["error"]["code"] == "NOT_FOUND"
        observations["reads"].append({"path": path, "status": status})
    for path in (f"/command-center/cycles/{cycle_id}", *api_paths.values()):
        for method in ("POST", "PUT", "PATCH", "DELETE"):
            assert server.request(path, method=method)[0] == 405
    # Exercise the accepted cursor and follow-on page without inventing IDs.
    first_path = api_paths["outcomes"] + "?limit=1"
    status, _, body = server.request(first_path)
    assert status == 200
    first = json.loads(body)
    assert len(first["data"]["items"]) == 1
    cursor = first["meta"]["next_cursor"]
    assert cursor is not None
    from urllib.parse import quote

    status, _, body = server.request(first_path + "&cursor=" + quote(cursor, safe=""))
    assert status == 200
    assert json.loads(body)["data"]["items"][0] != first["data"]["items"][0]
    observations["outcome_navigation_ref_match"] = True
    observations["outcome_pagination"] = "PASS"
    observations["write_methods"] = "405"
    return observations


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
        _assert_cycle_next_action_runtime(server, seeded)
        ui_paths = (
            "/command-center",
            f"/command-center/projects/{project_id}",
            f"/command-center/work-runs/{accepted_run_id}",
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
            if path in ui_paths[:3]:
                assert b'<html lang="ko">' in body
            if path == f"/command-center/projects/{project_id}":
                assert f'data-project-id="{project_id}"'.encode() in body
                assert b'id="queue-list" class="work-run-list"' in body
                assert b"<table" not in body
            if path == f"/command-center/work-runs/{accepted_run_id}":
                assert b'data-page="work-run-detail"' in body
                assert b'id="transition-list" class="transition-list"' in body
                assert b'id="evidence-state"' in body
                assert b'id="human-judgment-state"' in body
            if path == "/command-center/assets/app.js":
                assert b'document.createElement("article")' in body
                assert b'target.focus({ preventScroll: true })' in body

        detail_api_paths = (
            f"/v1/command-center/work-runs/{accepted_run_id}",
            f"/v1/command-center/work-runs/{accepted_run_id}/transitions",
            f"/v1/command-center/work-runs/{accepted_run_id}/execution",
            f"/v1/command-center/work-runs/{accepted_run_id}/evidence",
            f"/v1/command-center/work-runs/{accepted_run_id}/human-judgment",
        )
        detail_payloads = []
        for path in detail_api_paths:
            status, headers, body = server.request(path)
            assert status == 200
            assert headers["x-aiscc-exposure"] == "LOCAL_PRIVATE_ONLY"
            detail_payloads.append(json.loads(body))
            assert server.request(path, headers={"If-None-Match": headers["etag"]})[0] == 304
        assert detail_payloads[0]["data"]["workflow"]["state"] == "ACCEPTED"
        assert any(
            item["decision"]["outcome"] == "DENIED"
            and item["decision"]["derived_state_effect"] == "UNCHANGED"
            for item in detail_payloads[1]["data"]["items"]
        )
        assert detail_payloads[2]["data"]["attempts"][0]["status"] == "EXECUTOR_COMPLETED"
        assert set(detail_payloads[3]["data"]) == {
            "work_run_id",
            "requirement_sets",
            "checkpoints",
            "requirements",
            "candidates",
            "admission_decisions",
            "admitted_evidence",
            "satisfactions",
            "set_evaluations",
            "set_attestations",
        }
        assert set(detail_payloads[4]["data"]) == {
            "work_run_id",
            "human_gate",
            "human_result",
            "judgment",
            "transition_effect",
        }

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
