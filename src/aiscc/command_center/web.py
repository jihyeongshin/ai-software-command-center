from __future__ import annotations

from html import escape

CONTENT_SECURITY_POLICY = (
    "default-src 'self'; "
    "script-src 'self'; "
    "style-src 'self'; "
    "connect-src 'self'; "
    "img-src 'self' data:; "
    "object-src 'none'; "
    "base-uri 'none'; "
    "frame-ancestors 'none'; "
    "form-action 'self'"
)


def security_headers(*, html: bool = False) -> dict[str, str]:
    headers = {
        "X-AISCC-Exposure": "LOCAL_PRIVATE_ONLY",
        "X-Content-Type-Options": "nosniff",
        "Referrer-Policy": "no-referrer",
        "Cache-Control": "no-store",
    }
    if html:
        headers["Content-Security-Policy"] = CONTENT_SECURITY_POLICY
    return headers


def render_landing_page() -> str:
    return """<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Software Command Center</title>
  <link rel="stylesheet" href="/command-center/assets/app.css">
  <script src="/command-center/assets/app.js" defer></script>
</head>
<body data-page="landing">
  <header class="site-header">
    <div>
      <p class="eyebrow">운영자 작업공간</p>
      <h1>AI Software Command Center</h1>
    </div>
    <p class="exposure-badge">로컬 / 비공개 / 읽기 전용 (LOCAL / PRIVATE / READ ONLY)</p>
  </header>
  <main class="landing-main">
    <section class="panel hero-panel" aria-labelledby="project-heading">
      <p class="kicker">프로젝트 큐 조회</p>
      <h2 id="project-heading">알고 있는 Project ID 열기</h2>
      <p class="lede">
        새 Project catalog을 만들거나 WorkflowState를 변경하지 않고,
        권위 있는 WorkRun 큐 projection을 조회합니다.
      </p>
      <form id="project-form" class="project-form" method="get" action="/command-center">
        <div class="project-id-field">
          <label class="project-id-label" for="known-project-id">알고 있는 Project ID</label>
          <div class="input-action-row">
            <input id="known-project-id" name="project_id" type="text" required
                   autocomplete="off" spellcheck="false" aria-describedby="project-id-help">
            <button type="submit">프로젝트 큐 열기</button>
          </div>
        </div>
        <p id="project-id-help" class="field-help">
          이 단계에서는 Project 목록을 제공하지 않습니다. 이미 알고 있는 정확한 ID를 입력하세요.
        </p>
      </form>
    </section>
  </main>
</body>
</html>
"""


def render_project_page(project_id: str) -> str:
    safe_project_id = escape(project_id, quote=True)
    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>프로젝트 큐 · AI Software Command Center</title>
  <link rel="stylesheet" href="/command-center/assets/app.css">
  <script src="/command-center/assets/app.js" defer></script>
</head>
<body data-page="project-queue" data-project-id="{safe_project_id}">
  <header class="site-header">
    <div>
      <a class="back-link" href="/command-center">← Project 변경</a>
      <p class="eyebrow">Project / Task 큐</p>
      <h1>AI Software Command Center</h1>
      <p class="project-line">Project ID <strong id="project-id-label"></strong></p>
    </div>
    <p class="exposure-badge">로컬 / 비공개 / 읽기 전용 (LOCAL / PRIVATE / READ ONLY)</p>
  </header>
  <main>
    <section class="panel filters-panel" aria-labelledby="filters-heading">
      <div class="section-heading-row">
        <div>
          <p class="kicker">읽기 projection 제어</p>
          <h2 id="filters-heading">큐 필터</h2>
        </div>
        <button id="refresh-button" type="button">큐 새로고침</button>
      </div>
      <form id="filter-form" class="filter-grid">
        <label><span class="label-stack"><span class="label-primary">워크플로</span>
          <span class="label-technical">WorkflowState</span></span>
          <input name="workflow_state" type="text" autocomplete="off"
                 placeholder="정확한 WorkflowState">
        </label>
        <label><span class="label-stack"><span class="label-primary">실행 상태</span>
          <span class="label-technical">ExecutionStatus</span></span>
          <input name="execution_status" type="text" autocomplete="off"
                 placeholder="정확한 ExecutionStatus">
        </label>
        <label><span class="label-stack"><span class="label-primary">사람 검토 관문</span>
          <span class="label-technical">HumanGateStatus</span></span>
          <input name="human_gate_status" type="text" autocomplete="off"
                 placeholder="정확한 HumanGateStatus">
        </label>
        <label><span class="label-stack"><span class="label-primary">판정 존재 여부</span>
          <span class="label-technical">Judgment</span></span>
          <select name="judgment_presence">
            <option value="">전체</option>
            <option value="PRESENT">PRESENT</option>
            <option value="NONE">NONE</option>
          </select>
        </label>
        <label><span class="label-stack"><span class="label-primary">판정 종류</span>
          <span class="label-technical">JudgmentKind</span></span>
          <input name="judgment_kind" type="text" autocomplete="off"
                 placeholder="정확한 JudgmentKind">
        </label>
        <label><span class="label-stack"><span class="label-primary">종료 워크플로 여부</span>
          <span class="label-technical">terminal</span></span>
          <select name="terminal">
            <option value="">전체</option>
            <option value="true">true</option>
            <option value="false">false</option>
          </select>
        </label>
        <label><span class="label-stack"><span class="label-primary">고정 식별자 검색</span>
          <span class="label-technical">q · stable ID</span></span>
          <input name="q" type="search" autocomplete="off"
                 placeholder="Task 또는 WorkRun stable ID">
        </label>
        <label><span class="label-stack"><span class="label-primary">페이지 항목 수</span>
          <span class="label-technical">limit</span></span>
          <input name="limit" type="number" min="1" max="100" value="50" required>
        </label>
        <label><span class="label-stack"><span class="label-primary">불투명 커서</span>
          <span class="label-technical">cursor</span></span>
          <input id="cursor-input" name="cursor" type="text" autocomplete="off" spellcheck="false">
        </label>
        <div class="filter-actions">
          <button type="submit">필터 적용</button>
          <button type="reset" class="secondary-button">초기화</button>
        </div>
      </form>
    </section>

    <section class="panel queue-panel" aria-labelledby="queue-heading">
      <div class="section-heading-row queue-heading-row">
        <div>
          <p class="kicker">P2-1A 권위 read model</p>
          <h2 id="queue-heading" tabindex="-1">프로젝트 큐</h2>
        </div>
        <div class="read-state" data-state="LOADING" aria-live="polite" aria-atomic="true">
          <span id="state-name" class="state-name">불러오는 중</span>
          <span id="state-message">큐 projection을 불러오고 있습니다.</span>
        </div>
      </div>
      <p class="projection-note">
        각 권위 차원을 분리해 표시합니다. WorkRun 상세 화면은 P2-1C 범위입니다.
      </p>
      <section id="queue-list" class="work-run-list"
               aria-label="프로젝트 큐 WorkRun 목록"></section>
      <div class="pagination" aria-label="큐 페이지 이동">
        <button id="previous-page" type="button" class="secondary-button" disabled>이전</button>
        <span id="page-note">현재 브라우저 페이지에서만 cursor 이력을 유지합니다.</span>
        <button id="next-page" type="button" class="secondary-button" disabled>다음</button>
      </div>
    </section>
  </main>
</body>
</html>
"""


APP_CSS = """:root {
  color-scheme: dark;
  --background: #0b0f14;
  --surface: #121820;
  --surface-raised: #18212b;
  --line: #2b3948;
  --text: #f2f5f7;
  --muted: #9fb0c1;
  --accent: #6de5c4;
  --accent-ink: #06261f;
  --warning: #f2c66d;
  --danger: #ff8f8f;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
    "Segoe UI", sans-serif;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  min-width: 320px;
  min-height: 100vh;
  background:
    radial-gradient(circle at top right, rgba(45, 119, 108, 0.18), transparent 32rem),
    var(--background);
  color: var(--text);
}

a { color: var(--accent); }

button, input, select { font: inherit; }

button, input, select {
  min-height: 2.75rem;
  border: 1px solid var(--line);
  border-radius: 0.45rem;
}

button {
  padding: 0.65rem 1rem;
  border-color: var(--accent);
  background: var(--accent);
  color: var(--accent-ink);
  font-weight: 750;
  cursor: pointer;
}

button:hover { filter: brightness(1.08); }
button:disabled { cursor: not-allowed; filter: grayscale(0.7); opacity: 0.5; }

input, select {
  width: 100%;
  padding: 0.6rem 0.75rem;
  background: #0d131a;
  color: var(--text);
}

:focus-visible {
  outline: 3px solid var(--warning);
  outline-offset: 3px;
}

input:focus-visible, select:focus-visible {
  border-color: var(--accent);
  outline: none;
  box-shadow: 0 0 0 3px rgba(109, 229, 196, 0.28);
}

.site-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 2rem;
  padding: 2rem clamp(1rem, 4vw, 4rem) 1.2rem;
  border-bottom: 1px solid var(--line);
}

h1, h2, p { margin-top: 0; }
h1 { margin-bottom: 0.35rem; font-size: clamp(1.7rem, 3vw, 2.5rem); letter-spacing: -0.035em; }
h2 { margin-bottom: 0.8rem; }

.eyebrow, .kicker {
  margin-bottom: 0.45rem;
  color: var(--accent);
  font-size: 0.76rem;
  font-weight: 800;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.exposure-badge {
  flex: 0 0 auto;
  margin: 0;
  padding: 0.55rem 0.75rem;
  border: 1px solid var(--accent);
  border-radius: 999px;
  color: var(--accent);
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.08em;
}

main { padding: 1.5rem clamp(1rem, 4vw, 4rem) 3rem; }
.landing-main { display: grid; min-height: 70vh; place-items: center; }
.panel { border: 1px solid var(--line); border-radius: 0.8rem; background: rgba(18, 24, 32, 0.96); }
.hero-panel { width: min(46rem, 100%); padding: clamp(1.3rem, 4vw, 3rem); }
.lede, .field-help, .projection-note, #page-note { color: var(--muted); }
.project-form { margin-top: 2rem; }
.project-id-field { display: grid; gap: 0.7rem; }
.project-id-label { display: block; font-size: 0.86rem; font-weight: 750; }
.filter-grid label {
  display: grid;
  align-content: start;
  gap: 0.55rem;
  font-size: 0.82rem;
  font-weight: 700;
}
.label-stack { display: grid; gap: 0.12rem; min-width: 0; }
.label-primary { color: var(--text); font-weight: 750; }
.label-technical {
  color: var(--muted);
  font-size: 0.72rem;
  font-weight: 650;
  letter-spacing: 0.025em;
  overflow-wrap: anywhere;
}
.input-action-row { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 0.7rem; }
.field-help { margin: 0.6rem 0 0; font-size: 0.85rem; }
.back-link { display: inline-block; margin-bottom: 1rem; }
.project-line { margin: 0.45rem 0 0; color: var(--muted); }
.project-line strong { color: var(--text); overflow-wrap: anywhere; }

.filters-panel, .queue-panel { padding: 1.2rem; }
.queue-panel { margin-top: 1.2rem; }
.section-heading-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
}
.filter-grid { display: grid; grid-template-columns: repeat(5, minmax(10rem, 1fr)); gap: 0.9rem; }
.filter-actions { display: flex; align-items: end; gap: 0.6rem; }
.secondary-button {
  border-color: var(--line);
  background: var(--surface-raised);
  color: var(--text);
}
.read-state {
  display: grid;
  justify-items: end;
  gap: 0.25rem;
  text-align: right;
  color: var(--muted);
}
.state-name { color: var(--accent); font-size: 0.78rem; font-weight: 850; letter-spacing: 0.1em; }
.read-state[data-state="INVALID_QUERY"] .state-name,
.read-state[data-state="AUTHORITY_CONFLICT"] .state-name,
.read-state[data-state="UNEXPECTED_ERROR"] .state-name { color: var(--danger); }
.read-state[data-state="PROJECTION_UNAVAILABLE"] .state-name { color: var(--warning); }

.work-run-list { display: grid; gap: 1rem; min-width: 0; }
.work-run-card {
  min-width: 0;
  padding: 1rem;
  border: 1px solid var(--line);
  border-radius: 0.7rem;
  background: #0d131a;
}
.work-run-heading {
  margin: 0 0 0.85rem;
  font-size: 1rem;
  line-height: 1.4;
  overflow-wrap: anywhere;
}
.identity-grid, .state-strip, .authority-grid {
  display: grid;
  margin: 0;
  min-width: 0;
  gap: 0.75rem;
}
.identity-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.state-strip {
  grid-template-columns: repeat(2, minmax(0, 1fr));
  margin-top: 0.75rem;
}
.authority-grid {
  grid-template-columns: repeat(3, minmax(0, 1fr));
  margin-top: 0.75rem;
}
.authority-item {
  min-width: 0;
  padding: 0.8rem;
  border: 1px solid var(--line);
  border-radius: 0.55rem;
  background: var(--surface);
}
.authority-item dt { margin: 0 0 0.55rem; }
.authority-item dd {
  margin: 0;
  min-width: 0;
  font-size: 0.88rem;
  line-height: 1.45;
  overflow-wrap: anywhere;
}
.identity-item { grid-column: 1 / -1; }
.state-item { border-left: 3px solid var(--accent); }
.next-action-item { grid-column: span 2; }
.cell-line { margin: 0 0 0.38rem; }
.cell-line:last-child { margin-bottom: 0; }
.cell-primary { color: var(--text); font-weight: 750; }
.cell-muted { color: var(--muted); }
.cell-reference { color: var(--warning); }
.pagination {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.8rem;
  margin-top: 1rem;
}

@media (max-width: 1180px) {
  .filter-grid { grid-template-columns: repeat(3, minmax(10rem, 1fr)); }
  .authority-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}

@media (max-width: 720px) {
  .site-header, .section-heading-row { flex-direction: column; }
  .input-action-row, .filter-grid { grid-template-columns: 1fr; }
  .identity-grid, .state-strip, .authority-grid { grid-template-columns: 1fr; }
  .next-action-item { grid-column: auto; }
  .read-state { justify-items: start; text-align: left; }
  .pagination { align-items: stretch; flex-direction: column; }
}
"""


APP_JS = r"""(() => {
  "use strict";

  const page = document.body.dataset.page;
  if (page === "landing") {
    const projectForm = document.getElementById("project-form");
    const projectInput = document.getElementById("known-project-id");
    projectForm.addEventListener("submit", (event) => {
      event.preventDefault();
      const projectId = projectInput.value.trim();
      if (!projectId) {
        projectInput.setCustomValidity("알고 있는 Project ID를 입력하세요.");
        projectInput.reportValidity();
        return;
      }
      projectInput.setCustomValidity("");
      window.location.assign("/command-center/projects/" + encodeURIComponent(projectId));
    });
    projectInput.addEventListener("input", () => projectInput.setCustomValidity(""));
    return;
  }

  if (page !== "project-queue") {
    return;
  }

  const FILTER_NAMES = [
    "workflow_state",
    "execution_status",
    "human_gate_status",
    "judgment_presence",
    "judgment_kind",
    "terminal",
    "q",
    "limit",
    "cursor",
  ];
  const TERMINAL_WORKFLOW_STATES = new Set(["ACCEPTED", "REJECTED", "FAILED"]);
  const POLL_INTERVAL_MS = 10000;
  const STATE_COPY = {
    LOADING: {
      label: "불러오는 중",
      message: "큐 projection을 불러오고 있습니다.",
    },
    EMPTY: {
      label: "결과 없음",
      message: "정확한 조회 조건과 일치하는 WorkRun이 없습니다.",
    },
    READY: {
      label: "최신 상태",
      message: "큐 projection을 불러왔습니다.",
    },
    INVALID_QUERY: {
      label: "조회 조건 오류",
      message: "정확한 필터 값과 limit을 확인하세요.",
    },
    NOT_FOUND: {
      label: "프로젝트 큐 없음",
      message: "요청한 프로젝트 큐를 찾을 수 없습니다.",
    },
    AUTHORITY_CONFLICT: {
      label: "권위 상태 충돌",
      message: "projection을 하나의 일관된 snapshot으로 읽을 수 없습니다.",
    },
    PROJECTION_UNAVAILABLE: {
      label: "조회 projection 사용 불가",
      message: "Command Center read projection을 현재 사용할 수 없습니다.",
    },
    UNEXPECTED_ERROR: {
      label: "조회 오류",
      message: "읽기 요청을 안전하게 완료하지 못했습니다.",
    },
  };

  const projectId = document.body.dataset.projectId;
  const projectLabel = document.getElementById("project-id-label");
  const filterForm = document.getElementById("filter-form");
  const cursorInput = document.getElementById("cursor-input");
  const refreshButton = document.getElementById("refresh-button");
  const previousButton = document.getElementById("previous-page");
  const nextButton = document.getElementById("next-page");
  const queueHeading = document.getElementById("queue-heading");
  const queueList = document.getElementById("queue-list");
  const stateName = document.getElementById("state-name");
  const stateMessage = document.getElementById("state-message");
  const readState = stateName.parentElement;

  projectLabel.textContent = projectId;

  let currentQueryShape = null;
  let lastSuccessfulEtag = null;
  let nextCursor = null;
  let cursorHistory = [];
  let renderedItemCount = 0;
  let hasNonterminalWorkRun = false;
  let pollTimer = null;
  let requestInFlight = false;
  let refreshAfterFlight = false;

  function setReadState(name, message) {
    const copy = STATE_COPY[name];
    stateName.textContent = copy.label;
    stateMessage.textContent = message || copy.message;
    readState.dataset.state = name;
  }

  function display(value, fallback = "값 없음") {
    if (value === null || value === undefined || value === "") {
      return fallback;
    }
    return String(value);
  }

  function addLine(container, value, className = "cell-line") {
    const line = document.createElement("p");
    line.className = className;
    line.textContent = value;
    container.appendChild(line);
  }

  function makeLabel(primary, technical) {
    const label = document.createElement("span");
    label.className = "label-stack";
    const primaryLine = document.createElement("span");
    primaryLine.className = "label-primary";
    primaryLine.textContent = primary;
    const technicalLine = document.createElement("span");
    technicalLine.className = "label-technical";
    technicalLine.textContent = technical;
    label.append(primaryLine, technicalLine);
    return label;
  }

  function makeDefinition(primary, technical, lines, className = "") {
    const item = document.createElement("div");
    item.className = ("authority-item " + className).trim();
    const term = document.createElement("dt");
    term.appendChild(makeLabel(primary, technical));
    const description = document.createElement("dd");
    lines.forEach((line) => addLine(description, line.text, line.className));
    item.append(term, description);
    return item;
  }

  function taskLines(item) {
    const taskDisplay = item.task_display || {};
    const metadataAvailable = taskDisplay.availability === "AVAILABLE";
    let metadataLine;
    if (metadataAvailable && (taskDisplay.title || taskDisplay.type)) {
      metadataLine = [taskDisplay.title, taskDisplay.type].filter(Boolean).join(" · ");
    } else if (taskDisplay.availability === "REFERENCE_ONLY") {
      metadataLine = "참조만 가능 (REFERENCE_ONLY)";
    } else {
      metadataLine = "Task metadata를 사용할 수 없음";
    }
    const taskContract = item.task_contract || {};
    return [
      {
        text: "Task metadata 상태: " + display(taskDisplay.availability),
        className: "cell-line cell-muted",
      },
      { text: metadataLine, className: "cell-line cell-reference" },
      { text: "TaskContract ID: " + display(taskContract.id), className: "cell-line cell-primary" },
      {
        text: "TaskContract version: " + display(taskContract.version),
        className: "cell-line cell-muted",
      },
      { text: "WorkRun ID: " + display(item.work_run_id), className: "cell-line cell-muted" },
    ];
  }

  function renderCards(items) {
    const fragment = document.createDocumentFragment();
    items.forEach((item, index) => {
      const workflow = item.workflow || {};
      const execution = item.execution || {};
      const humanGate = item.human_gate || {};
      const humanResult = item.human_result || {};
      const judgment = item.judgment || {};
      const decision = item.latest_transition_decision || {};
      const nextAction = item.next_action || {};
      const card = document.createElement("article");
      card.className = "work-run-card";
      const heading = document.createElement("h3");
      heading.className = "work-run-heading";
      heading.id = "work-run-heading-" + String(index + 1);
      heading.textContent = "WorkRun " + display(item.work_run_id);
      card.setAttribute("aria-labelledby", heading.id);
      card.appendChild(heading);

      const identity = document.createElement("dl");
      identity.className = "identity-grid";
      identity.appendChild(makeDefinition(
        "작업 실행 식별 정보",
        "TaskContract · WorkRun",
        taskLines(item),
        "identity-item",
      ));
      card.appendChild(identity);

      const stateStrip = document.createElement("dl");
      stateStrip.className = "state-strip";
      stateStrip.appendChild(makeDefinition("워크플로", "WorkflowState", [
        { text: display(workflow.state), className: "cell-line cell-primary" },
        {
          text: "상태 버전: " + display(workflow.state_version),
          className: "cell-line cell-muted",
        },
      ], "state-item"));
      stateStrip.appendChild(makeDefinition(
        "실행 상태",
        "ExecutionStatus",
        execution.attempt_present ? [
        { text: display(execution.status), className: "cell-line cell-primary" },
        {
          text: "실행 attempt: " + display(execution.execution_attempt_id),
          className: "cell-line cell-muted",
        },
        {
          text: "실행 버전: " + display(execution.execution_version),
          className: "cell-line cell-muted",
        },
        ] : [{ text: "실행 attempt가 없습니다.", className: "cell-line cell-muted" }],
        "state-item",
      ));
      card.appendChild(stateStrip);

      const authorityGrid = document.createElement("dl");
      authorityGrid.className = "authority-grid";
      authorityGrid.appendChild(makeDefinition("사람 검토 관문", "HumanGateStatus", [
        { text: "존재 여부: " + display(humanGate.presence), className: "cell-line cell-primary" },
        { text: "관문 상태: " + display(humanGate.status), className: "cell-line cell-muted" },
        {
          text: "일시 중지 상태: " + display(humanGate.suspension_status),
          className: "cell-line cell-muted",
        },
      ]));
      authorityGrid.appendChild(makeDefinition("사람 검토 결과", "HumanResult", [
        {
          text: "존재 여부: " + display(humanResult.presence),
          className: "cell-line cell-primary",
        },
        { text: "결과: " + display(humanResult.result_kind), className: "cell-line cell-muted" },
      ]));
      authorityGrid.appendChild(makeDefinition("판정", "Judgment", [
        { text: "존재 여부: " + display(judgment.presence), className: "cell-line cell-primary" },
        { text: "판정 종류: " + display(judgment.kind), className: "cell-line cell-muted" },
        { text: "소유 정책: " + display(judgment.owner_policy), className: "cell-line cell-muted" },
      ]));
      authorityGrid.appendChild(makeDefinition("최신 전이 결정", "TransitionDecision", [
        { text: "존재 여부: " + display(decision.presence), className: "cell-line cell-primary" },
        { text: "결정 결과: " + display(decision.outcome), className: "cell-line cell-muted" },
        { text: "사유: " + display(decision.reason), className: "cell-line cell-muted" },
        {
          text: "결과 WorkflowState: " + display(decision.resulting_state),
          className: "cell-line cell-muted",
        },
      ]));
      authorityGrid.appendChild(makeDefinition("다음 작업", "NextAction", [
        { text: "존재 여부: " + display(nextAction.presence), className: "cell-line cell-primary" },
        { text: "작업 참조: " + display(nextAction.action_ref), className: "cell-line cell-muted" },
        {
          text: "Project revision: " + display(nextAction.project_revision),
          className: "cell-line cell-muted",
        },
      ], "next-action-item"));
      authorityGrid.appendChild(makeDefinition("런타임 모드", "RuntimeMode", [
        { text: display(item.runtime_mode), className: "cell-line cell-primary" },
      ]));
      card.appendChild(authorityGrid);
      fragment.appendChild(card);
    });
    queueList.replaceChildren(fragment);
  }

  function buildQueueRequest() {
    const values = new FormData(filterForm);
    const query = new URLSearchParams();
    FILTER_NAMES.forEach((name) => {
      const value = String(values.get(name) || "").trim();
      if (value) {
        query.append(name, value);
      }
    });
    const queryText = query.toString();
    const endpoint = "/v1/command-center/projects/" + encodeURIComponent(projectId) + "/queue";
    return {
      url: queryText ? endpoint + "?" + queryText : endpoint,
      shape: projectId + "?" + queryText,
    };
  }

  function stopPolling() {
    if (pollTimer !== null) {
      window.clearTimeout(pollTimer);
      pollTimer = null;
    }
  }

  function schedulePolling() {
    stopPolling();
    if (document.visibilityState === "visible" && hasNonterminalWorkRun) {
      pollTimer = window.setTimeout(() => void loadQueue(), POLL_INTERVAL_MS);
    }
  }

  function updatePagination() {
    previousButton.disabled = cursorHistory.length === 0;
    nextButton.disabled = !nextCursor;
  }

  function mapFailure(responseStatus) {
    if (responseStatus === 400) return "INVALID_QUERY";
    if (responseStatus === 404) return "NOT_FOUND";
    if (responseStatus === 409) return "AUTHORITY_CONFLICT";
    if (responseStatus === 503) return "PROJECTION_UNAVAILABLE";
    return "UNEXPECTED_ERROR";
  }

  function restorePaginationFocus(control) {
    const target = control && !control.disabled ? control : queueHeading;
    window.requestAnimationFrame(() => target.focus({ preventScroll: true }));
  }

  async function loadQueue(options = {}) {
    const preserveContent = options.preserveContent === true;
    const focusAfterLoad = options.focusAfterLoad || null;
    if (requestInFlight) {
      refreshAfterFlight = true;
      return;
    }
    requestInFlight = true;
    stopPolling();
    const request = buildQueueRequest();
    if (request.shape !== currentQueryShape) {
      currentQueryShape = request.shape;
      lastSuccessfulEtag = null;
      renderedItemCount = 0;
      hasNonterminalWorkRun = false;
      if (!preserveContent) {
        queueList.replaceChildren();
      }
    }
    if (renderedItemCount === 0) {
      setReadState("LOADING");
    }
    const headers = {};
    if (lastSuccessfulEtag) {
      headers["If-None-Match"] = lastSuccessfulEtag;
    }
    try {
      const response = await fetch(request.url, {
        method: "GET",
        headers,
        cache: "no-store",
        credentials: "same-origin",
      });
      if (response.status === 304) {
        setReadState(
          renderedItemCount === 0 ? "EMPTY" : "READY",
          "큐가 변경되지 않았습니다.",
        );
        return;
      }
      if (response.status !== 200) {
        setReadState(mapFailure(response.status));
        return;
      }
      const envelope = await response.json();
      const items = envelope && envelope.data && Array.isArray(envelope.data.items)
        ? envelope.data.items
        : null;
      if (items === null) {
        setReadState("UNEXPECTED_ERROR");
        return;
      }
      lastSuccessfulEtag = response.headers.get("ETag");
      nextCursor = envelope.meta && typeof envelope.meta.next_cursor === "string"
        ? envelope.meta.next_cursor
        : null;
      renderCards(items);
      renderedItemCount = items.length;
      hasNonterminalWorkRun = items.some((item) => {
        const workflowState = item && item.workflow ? item.workflow.state : null;
        return !TERMINAL_WORKFLOW_STATES.has(workflowState);
      });
      setReadState(items.length === 0 ? "EMPTY" : "READY");
      updatePagination();
    } catch (_error) {
      setReadState("UNEXPECTED_ERROR");
    } finally {
      requestInFlight = false;
      if (focusAfterLoad) {
        restorePaginationFocus(focusAfterLoad);
      }
      if (refreshAfterFlight && document.visibilityState === "visible") {
        refreshAfterFlight = false;
        void loadQueue();
      } else {
        refreshAfterFlight = false;
        schedulePolling();
      }
    }
  }

  filterForm.addEventListener("submit", (event) => {
    event.preventDefault();
    cursorInput.value = "";
    cursorHistory = [];
    nextCursor = null;
    updatePagination();
    void loadQueue();
  });

  filterForm.addEventListener("reset", () => {
    window.setTimeout(() => {
      cursorInput.value = "";
      cursorHistory = [];
      nextCursor = null;
      updatePagination();
      void loadQueue();
    }, 0);
  });

  refreshButton.addEventListener("click", () => void loadQueue());
  previousButton.addEventListener("click", () => {
    const previousCursor = cursorHistory.pop();
    cursorInput.value = previousCursor || "";
    nextCursor = null;
    void loadQueue({ preserveContent: true, focusAfterLoad: previousButton });
  });
  nextButton.addEventListener("click", () => {
    if (!nextCursor) return;
    cursorHistory.push(cursorInput.value);
    cursorInput.value = nextCursor;
    nextCursor = null;
    void loadQueue({ preserveContent: true, focusAfterLoad: nextButton });
  });

  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "hidden") {
      stopPolling();
      return;
    }
    void loadQueue();
  });

  updatePagination();
  void loadQueue();
})();
"""
