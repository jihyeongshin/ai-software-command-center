from __future__ import annotations

import hashlib
import inspect
import re
from pathlib import Path

from aiscc.api.routes import command_center_ui
from aiscc.command_center import web


def test_exact_ui_route_set_is_get_only_and_includes_work_run_detail() -> None:
    routes = {
        str(getattr(route, "path", "")): set(getattr(route, "methods", set()) or set())
        for route in command_center_ui.router.routes
    }
    assert routes == {
        "/command-center": {"GET"},
        "/command-center/projects/{project_id}": {"GET"},
        "/command-center/work-runs/{work_run_id}": {"GET"},
        "/command-center/assets/app.css": {"GET"},
        "/command-center/assets/app.js": {"GET"},
    }


def test_shell_is_static_and_project_navigation_encodes_the_known_id() -> None:
    landing = web.render_landing_page()
    project = web.render_project_page('project-1"><script>unsafe</script>')
    detail = web.render_work_run_page('run-1"><script>unsafe</script>')
    route_source = inspect.getsource(command_center_ui)
    assert '<html lang="ko">' in landing
    assert '<html lang="ko">' in project
    assert '<html lang="ko">' in detail
    assert "AI Software Command Center" in landing
    assert "운영자 작업공간" in landing
    assert "로컬 / 비공개 / 읽기 전용 (LOCAL / PRIVATE / READ ONLY)" in landing
    assert "알고 있는 Project ID 열기" in landing
    assert "Project 목록을 제공하지 않습니다" in landing
    assert "프로젝트 큐 열기" in landing
    assert "encodeURIComponent(projectId)" in web.APP_JS
    assert "<script>unsafe</script>" not in project
    assert "<script>unsafe</script>" not in detail
    assert "command_center_queries" not in route_source
    assert "Postgres" not in route_source
    assert ".queue(" not in route_source
    assert ".work_run(" not in route_source
    assert ".transitions(" not in route_source
    assert ".execution(" not in route_source


def test_landing_project_field_has_explicit_spacing_and_coherent_focus_contract() -> None:
    landing = web.render_landing_page()
    assert 'class="project-id-field"' in landing
    assert 'class="project-id-label" for="known-project-id"' in landing
    assert ".project-id-field { display: grid; gap: 0.7rem; }" in web.APP_CSS
    input_focus = web.APP_CSS.split("input:focus-visible, select:focus-visible {", 1)[1].split(
        "}", 1
    )[0]
    assert "border-color: var(--accent)" in input_focus
    assert "outline: none" in input_focus
    assert "box-shadow:" in input_focus
    assert "var(--warning)" not in input_focus


def test_filter_labels_use_one_korean_primary_technical_secondary_grammar() -> None:
    project = web.render_project_page("project-1")
    labels = re.findall(
        r'<label><span class="label-stack"><span class="label-primary">([^<]+)</span>\s*'
        r'<span class="label-technical">([^<]+)</span></span>',
        project,
    )
    assert labels == [
        ("워크플로", "WorkflowState"),
        ("실행 상태", "ExecutionStatus"),
        ("사람 검토 관문", "HumanGateStatus"),
        ("판정 존재 여부", "Judgment"),
        ("판정 종류", "JudgmentKind"),
        ("종료 워크플로 여부", "terminal"),
        ("고정 식별자 검색", "q · stable ID"),
        ("페이지 항목 수", "limit"),
        ("불투명 커서", "cursor"),
    ]
    assert ".label-primary" in web.APP_CSS
    assert ".label-technical" in web.APP_CSS


def test_queue_contract_keeps_authority_dimensions_and_metadata_fallbacks_separate() -> None:
    project = web.render_project_page("project-1")
    assert "<table" not in project
    assert "table-scroll" not in project + web.APP_CSS
    assert 'id="queue-list" class="work-run-list"' in project
    assert 'aria-label="프로젝트 큐 WorkRun 목록"' in project
    assert 'document.createElement("article")' in web.APP_JS
    assert 'document.createElement("dl")' in web.APP_JS
    assert 'card.setAttribute("aria-labelledby", heading.id)' in web.APP_JS
    authority_labels = set(
        re.findall(r'makeDefinition\(\s*"([^"]+)",\s*"([^"]+)"', web.APP_JS)
    )
    assert authority_labels == {
        ("작업 실행 식별 정보", "TaskContract · WorkRun"),
        ("워크플로", "WorkflowState"),
        ("실행 상태", "ExecutionStatus"),
        ("사람 검토 관문", "HumanGateStatus"),
        ("사람 검토 결과", "HumanResult"),
        ("판정", "Judgment"),
        ("최신 전이 결정", "TransitionDecision"),
        ("다음 작업", "NextAction"),
        ("런타임 모드", "RuntimeMode"),
    }
    assert "Task metadata 상태: " in web.APP_JS
    assert "TaskContract ID: " in web.APP_JS
    assert "TaskContract version: " in web.APP_JS
    assert "WorkRun ID: " in web.APP_JS
    assert "Task metadata를 사용할 수 없음" in web.APP_JS
    assert "참조만 가능 (REFERENCE_ONLY)" in web.APP_JS
    assert "Overall Status" not in project + web.APP_JS
    assert ">Status<" not in project
    assert 'detailLink.textContent = "WorkRun 상세"' in web.APP_JS
    assert '"/command-center/work-runs/" + encodeURIComponent(item.work_run_id)' in web.APP_JS


def test_queue_cards_wrap_without_desktop_horizontal_scroll_and_have_responsive_grids() -> None:
    assert "overflow-wrap: anywhere" in web.APP_CSS
    assert "overflow-x: auto" not in web.APP_CSS
    assert "min-width: 106rem" not in web.APP_CSS
    assert ".work-run-card" in web.APP_CSS
    assert ".identity-item { grid-column: 1 / -1; }" in web.APP_CSS
    assert ".identity-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }" in (
        web.APP_CSS
    )
    assert "grid-template-columns: repeat(2, minmax(0, 1fr));" in web.APP_CSS
    desktop_rule = web.APP_CSS.split("@media (max-width: 1180px)", 1)[1].split(
        "@media (max-width: 720px)", 1
    )[0]
    assert ".authority-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }" in (
        desktop_rule
    )
    mobile_rule = web.APP_CSS.split("@media (max-width: 720px)", 1)[1]
    assert ".identity-grid, .state-strip, .authority-grid { grid-template-columns: 1fr; }" in (
        mobile_rule
    )


def test_cursor_pagination_is_ajax_only_and_restores_focus_without_top_scroll() -> None:
    pagination_source = web.APP_JS.split(
        'previousButton.addEventListener("click"', 1
    )[1].split('document.addEventListener("visibilitychange"', 1)[0]
    assert "window.location" not in pagination_source
    assert "location.assign" not in pagination_source
    assert "scrollTo" not in pagination_source
    assert "scrollIntoView" not in pagination_source
    assert "loadQueue({ preserveContent: true" in pagination_source
    assert "focusAfterLoad: previousButton" in pagination_source
    assert "focusAfterLoad: nextButton" in pagination_source
    assert 'target.focus({ preventScroll: true })' in web.APP_JS
    assert 'id="queue-heading" tabindex="-1"' in web.render_project_page("project-1")


def test_client_uses_only_accepted_queue_filters_and_exact_api_authority() -> None:
    assert '"/v1/command-center/projects/" + encodeURIComponent(projectId) + "/queue"' in (
        web.APP_JS
    )
    expected = {
        "workflow_state",
        "execution_status",
        "human_gate_status",
        "judgment_presence",
        "judgment_kind",
        "terminal",
        "q",
        "limit",
        "cursor",
    }
    controls = re.findall(
        r'<(?:input|select)[^>]+name="([a-z_]+)"', web.render_project_page("project-1")
    )
    assert set(controls) == expected
    filter_block = web.APP_JS.split("const FILTER_NAMES = [", 1)[1].split("];", 1)[0]
    assert set(re.findall(r'"([a-z_]+)"', filter_block)) == expected


def test_client_has_safe_dom_etag_and_conditional_polling_contracts() -> None:
    forbidden = ("inner" + "HTML", "insertAdjacent" + "HTML", "new " + "Function")
    assert all(token not in web.APP_JS for token in forbidden)
    assert not re.search(r"\beval\s*\(", web.APP_JS)
    assert "textContent" in web.APP_JS
    assert "createElement" in web.APP_JS
    assert "replaceChildren" in web.APP_JS
    assert 'headers["If-None-Match"] = lastSuccessfulEtag' in web.APP_JS
    assert "request.shape !== currentQueryShape" in web.APP_JS
    queue_source = web.APP_JS.split('if (page !== "project-queue")', 1)[1]
    branch_304 = queue_source.split("response.status === 304", 1)[1].split("return;", 1)[0]
    assert "renderRows" not in branch_304
    assert "replaceChildren" not in branch_304
    assert "POLL_INTERVAL_MS = 10000" in web.APP_JS
    assert 'document.visibilityState === "visible" && hasNonterminalWorkRun' in web.APP_JS
    assert 'document.visibilityState === "hidden"' in web.APP_JS
    assert 'new Set(["ACCEPTED", "REJECTED", "FAILED"])' in web.APP_JS
    for state in (
        "LOADING",
        "EMPTY",
        "READY",
        "INVALID_QUERY",
        "NOT_FOUND",
        "AUTHORITY_CONFLICT",
        "PROJECTION_UNAVAILABLE",
        "UNEXPECTED_ERROR",
    ):
        assert f"{state}:" in web.APP_JS
    for visible_label in (
        "불러오는 중",
        "결과 없음",
        "최신 상태",
        "조회 조건 오류",
        "프로젝트 큐 없음",
        "권위 상태 충돌",
        "조회 projection 사용 불가",
        "조회 오류",
    ):
        assert visible_label in web.APP_JS
    assert 'id="refresh-button"' in web.render_project_page("project-1")


def test_visible_accessibility_copy_is_korean_first_and_enum_values_remain_exact() -> None:
    landing = web.render_landing_page()
    project = web.render_project_page("project-1")
    assert "큐 새로고침" in project
    assert 'aria-label="프로젝트 큐 WorkRun 목록"' in project
    assert 'aria-label="큐 페이지 이동"' in project
    assert ">이전</button>" in project
    assert ">다음</button>" in project
    assert "알고 있는 Project ID를 입력하세요." in web.APP_JS
    assert 'return String(value);' in web.APP_JS
    assert 'new Set(["ACCEPTED", "REJECTED", "FAILED"])' in web.APP_JS
    assert "RUNNING" not in landing + project


def test_protected_composition_and_read_authority_files_remain_byte_identical() -> None:
    repository = Path(__file__).resolve().parents[3]
    expected = {
        "src/aiscc/api/app.py": "34b9216342dc256fd319ab5c594799b9aa6784c35bc13a8b01595d4204d572f0",
        "src/aiscc/api/routes/command_center.py": (
            "660ee70d71d9706dea17f20fc52b91ed716b7756fcd6aa425f2e90281004950b"
        ),
        "src/aiscc/command_center/read_models.py": (
            "346daeb778344a8ebf3e5f5905ee7c238a7a8cee0d64a18ddd219462cfe9fe1e"
        ),
        "src/aiscc/command_center/queries.py": (
            "94fe298372622ca82f1158ea9f45be24506e890c1f6a4180eef7d4997a26ed09"
        ),
        "src/aiscc/command_center/postgres_queries.py": (
            "476d084403b2eeefe69cd7a218f98b631188138cce2923920f22ee0c0c66571d"
        ),
        "src/aiscc/command_center/privacy.py": (
            "2f17f4250e11c5ee65a8d26cb65528d7045365255c43d00a74c3dc455cbe990b"
        ),
    }
    for relative_path, expected_hash in expected.items():
        actual_hash = hashlib.sha256((repository / relative_path).read_bytes()).hexdigest()
        assert actual_hash == expected_hash


def test_assets_and_csp_are_local_only_without_mutation_controls() -> None:
    combined = (
        web.render_landing_page()
        + web.render_project_page("project-1")
        + web.render_work_run_page("run-1")
        + web.APP_JS
    )
    assert not re.search(r"https?://", combined)
    assert "unsafe-eval" not in web.CONTENT_SECURITY_POLICY
    assert "unsafe-inline" not in web.CONTENT_SECURITY_POLICY
    assert "default-src 'self'" in web.CONTENT_SECURITY_POLICY
    assert "connect-src 'self'" in web.CONTENT_SECURITY_POLICY
    button_labels = re.findall(r"<button[^>]*>([^<]+)</button>", combined, flags=re.IGNORECASE)
    assert not {label.strip().casefold() for label in button_labels} & {
        "approve",
        "rework",
        "reject",
    }


def test_work_run_detail_information_architecture_is_korean_first_and_accessible() -> None:
    detail = web.render_work_run_page("run-1")
    assert '<html lang="ko">' in detail
    assert 'data-page="work-run-detail"' in detail
    assert "WorkRun 상세" in detail
    assert "현재 상태" in web.APP_JS
    assert "Task / 범위" in detail
    assert "전이 기록 (TransitionDecision)" in detail
    assert "실행 기록 (Execution)" in detail
    assert 'id="transition-list" class="transition-list"' in detail
    assert 'aria-live="polite"' in detail
    assert "수동 새로고침" in detail
    assert "프로젝트 큐로" in detail
    assert "overflow-wrap: anywhere" in web.APP_CSS
    assert ".transition-columns" in web.APP_CSS
    assert "overflow-x: auto" not in web.APP_CSS


def test_work_run_detail_uses_only_three_accepted_read_endpoints_and_safe_dom() -> None:
    detail_source = web.APP_JS.split('if (page === "work-run-detail")', 1)[1].split(
        'if (page !== "project-queue")', 1
    )[0]
    assert 'url: "/v1/command-center/work-runs/" + encodedWorkRunId' in detail_source
    assert '+ "/transitions"' in detail_source
    assert '+ "/execution"' in detail_source
    for forbidden_path in (
        "/evidence",
        "/human-judgment",
        "/outcomes",
        "/cycles/",
        "/next-action",
    ):
        assert forbidden_path not in detail_source
    forbidden = ("inner" + "HTML", "insertAdjacent" + "HTML", "new " + "Function")
    assert all(token not in detail_source for token in forbidden)
    assert not re.search(r"\beval\s*\(", detail_source)
    assert "textContent" in detail_source
    assert "createElement" in detail_source
    assert "replaceChildren" in detail_source


def test_work_run_detail_preserves_transition_and_execution_semantics() -> None:
    source = web.APP_JS
    assert 'taskDisplay.availability === "AVAILABLE"' in source
    assert 'scope.availability === "AVAILABLE"' in source
    assert 'decision.outcome === "DENIED"' in source
    assert 'decision.outcome === "ADMITTED"' in source
    assert 'decision.derived_state_effect === "UNCHANGED"' in source
    assert "authoritative state를 변경하지 않은 요청/결정 기록입니다" in source
    assert "성공한 state transition으로 표시하지 않습니다" in source
    assert "전이 기록 없음" in source
    assert "실행 기록 없음" in source
    assert "operation 기록 없음" in source
    assert 'attempt.status === "EXECUTOR_COMPLETED"' in source
    assert "WorkRun ACCEPTED를 의미하지 않습니다" in source
    for identifier in (
        "WorkflowState",
        "ExecutionStatus",
        "TransitionDecision",
        "ADMITTED",
        "DENIED",
        "EXECUTOR_COMPLETED",
    ):
        assert identifier in source + web.render_work_run_page("run-1")


def test_work_run_detail_has_endpoint_scoped_etag_304_and_polling_contract() -> None:
    source = web.APP_JS.split('if (page === "work-run-detail")', 1)[1].split(
        'if (page !== "project-queue")', 1
    )[0]
    for endpoint in ("summary", "transitions", "execution"):
        assert f'{endpoint}: {{' in source
    assert 'headers["If-None-Match"] = endpoint.etag' in source
    assert 'response.status === 304' in source
    assert 'detailEndpoints[key].etag = result.etag' in source
    assert "기존 전이 기록 유지" in source
    assert "기존 실행 기록 유지" in source
    assert "POLL_INTERVAL_MS = 10000" in source
    assert 'document.visibilityState === "visible"' in source
    assert 'document.visibilityState === "hidden"' in source
    assert 'new Set(["ACCEPTED", "REJECTED", "FAILED"])' in source
    assert "!TERMINAL_WORKFLOW_STATES.has(lastWorkflowState)" in source
    visibility = source.split('document.addEventListener("visibilitychange"', 1)[1]
    assert "void loadDetail()" in visibility


def test_work_run_detail_refresh_state_sequence_downgrades_and_restores_labels() -> None:
    source = web.APP_JS.split('if (page === "work-run-detail")', 1)[1].split(
        'if (page !== "project-queue")', 1
    )[0]
    stale_source = source.split("function markRetainedDetailStale()", 1)[1].split(
        "function applyTransitions", 1
    )[0]
    transitions_source = source.split("function applyTransitions", 1)[1].split(
        "function applyExecution", 1
    )[0]
    execution_source = source.split("function applyExecution", 1)[1].split(
        "async function loadDetail", 1
    )[0]
    failed_summary_branch = source.split("if (!summaryCurrent)", 1)[1].split(
        "const transitionsReady", 1
    )[0]

    retained_labels = re.findall(r'\? "([^"]+)"\s*: "([^"]+)";', stale_source)
    assert len(retained_labels) == 2
    transition_stale, transition_unavailable = retained_labels[0]
    execution_stale, execution_unavailable = retained_labels[1]
    transition_current = re.search(
        r'commitSuccess\("transitions", result\);\s*'
        r'transitionsState\.textContent = "([^"]+)";',
        transitions_source,
    )
    execution_current = re.search(
        r'commitSuccess\("execution", result\);\s*'
        r'executionState\.textContent = "([^"]+)";',
        execution_source,
    )
    assert transition_current is not None
    assert execution_current is not None

    state: dict[str, str | None] = {
        "transition_data": None,
        "execution_data": None,
        "transition_label": None,
        "execution_label": None,
        "page_state": None,
    }

    def apply_successful_refresh(transition_data: str, execution_data: str) -> None:
        state.update(
            transition_data=transition_data,
            execution_data=execution_data,
            transition_label=transition_current.group(1),
            execution_label=execution_current.group(1),
            page_state="READY",
        )

    def apply_summary_authority_failure(
        fresh_transition_data: str, fresh_execution_data: str
    ) -> None:
        assert fresh_transition_data == "transition-b"
        assert fresh_execution_data == "execution-b"
        state.update(
            transition_label=transition_stale,
            execution_label=execution_stale,
            page_state="AUTHORITY_CONFLICT",
        )

    apply_successful_refresh("transition-a", "execution-a")
    assert state == {
        "transition_data": "transition-a",
        "execution_data": "execution-a",
        "transition_label": "최신 전이 기록",
        "execution_label": "최신 실행 기록",
        "page_state": "READY",
    }

    assert failed_summary_branch.index("markRetainedDetailStale()") < (
        failed_summary_branch.index("return;")
    )
    assert "applyTransitions" not in failed_summary_branch
    assert "applyExecution" not in failed_summary_branch
    assert "commitSuccess" not in failed_summary_branch
    assert "replaceChildren" not in stale_source
    assert ".etag = null" not in stale_source
    assert ".hasData = false" not in stale_source
    apply_summary_authority_failure("transition-b", "execution-b")

    assert state["transition_data"] == "transition-a"
    assert state["execution_data"] == "execution-a"
    assert "마지막 성공" in str(state["transition_label"])
    assert "마지막 성공" in str(state["execution_label"])
    assert "새로고침 실패" in str(state["transition_label"])
    assert "새로고침 실패" in str(state["execution_label"])
    assert "최신" not in str(state["transition_label"])
    assert "최신" not in str(state["execution_label"])
    assert state["page_state"] == "AUTHORITY_CONFLICT"
    assert "최신" not in transition_unavailable
    assert "최신" not in execution_unavailable

    apply_successful_refresh("transition-c", "execution-c")
    assert state["transition_data"] == "transition-c"
    assert state["execution_data"] == "execution-c"
    assert state["transition_label"] == "최신 전이 기록"
    assert state["execution_label"] == "최신 실행 기록"
    assert state["page_state"] == "READY"
