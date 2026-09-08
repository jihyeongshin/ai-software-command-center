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
        <button id="refresh-button" type="button">큐 새로고침 · 다음 행동 / 결과 함께</button>
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
        각 권위 차원을 분리해 표시합니다. 상세 링크는 읽기 전용 WorkRun 화면으로 이동합니다.
      </p>
      <section id="queue-list" class="work-run-list"
               aria-label="프로젝트 큐 WorkRun 목록"></section>
      <div class="pagination" aria-label="큐 페이지 이동">
        <button id="previous-page" type="button" class="secondary-button" disabled>이전</button>
        <span id="page-note">현재 브라우저 페이지에서만 cursor 이력을 유지합니다.</span>
        <button id="next-page" type="button" class="secondary-button" disabled>다음</button>
      </div>
    </section>
    <section class="panel queue-panel" aria-labelledby="next-action-heading">
      <div class="section-heading-row">
        <h2 id="next-action-heading">다음 행동 (NextAction)</h2>
        <p id="next-action-state" class="section-read-state" aria-live="polite">불러오는 중</p>
      </div>
      <p class="projection-note">
        현재 projection, 선택 기록, Task 발행 후보는 별개입니다.
        조회로 선택하거나 발행하지 않습니다.
        제목 정보가 없는 행동은 참조만 표시합니다 (REFERENCE_ONLY).
      </p>
      <div id="next-action-content" class="detail-grid"></div>
    </section>
    <section class="panel queue-panel" aria-labelledby="outcomes-heading">
      <div class="section-heading-row">
        <h2 id="outcomes-heading">작업 결과 / Cycle 계보</h2>
        <p id="outcomes-state" class="section-read-state" aria-live="polite">불러오는 중</p>
      </div>
      <p class="projection-note">
        큐 필터와 별도로 프로젝트 결과를 조회합니다. 입장된 Cycle 참조가 있을 때만 연결합니다.
      </p>
      <div id="outcomes-content" class="record-list"></div>
      <div class="pagination" aria-label="작업 결과 페이지 이동">
        <button id="outcomes-first" type="button" class="secondary-button" disabled>
          결과 처음</button>
        <button id="outcomes-next" type="button" class="secondary-button" disabled>
          다음 결과</button>
      </div>
    </section>
  </main>
</body>
</html>
"""


def render_cycle_page(cycle_id: str) -> str:
    safe_cycle_id = escape(cycle_id, quote=True)
    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Cycle 계보 · AI Software Command Center</title>
  <link rel="stylesheet" href="/command-center/assets/app.css">
  <script src="/command-center/assets/app.js" defer></script>
</head>
<body data-page="cycle-detail" data-cycle-id="{safe_cycle_id}">
  <header class="site-header">
    <div>
      <a class="back-link" href="/command-center">← Command Center</a>
      <p class="eyebrow">입장된 런타임 Cycle</p>
      <h1>Cycle 계보</h1>
    </div>
    <p class="exposure-badge">로컬 / 비공개 / 읽기 전용 (LOCAL / PRIVATE / READ ONLY)</p>
  </header>
  <main class="detail-main">
    <section class="panel detail-panel" aria-labelledby="cycle-heading">
      <div class="section-heading-row">
        <h2 id="cycle-heading">작업 / 판정 / 증거 계보</h2>
        <button id="cycle-refresh-button" type="button">수동 새로고침</button>
      </div>
      <p class="projection-note">
        런타임 AdmittedCycle을 조회합니다. 저장소 Markdown Cycle 문서와는 별도입니다.
        판정 참조와 전이·증거 참조를 구분합니다.
      </p>
      <p id="cycle-state" class="section-read-state" aria-live="polite">불러오는 중</p>
      <div id="cycle-content" class="detail-grid"></div>
    </section>
  </main>
</body>
</html>
"""


def render_work_run_page(work_run_id: str) -> str:
    safe_work_run_id = escape(work_run_id, quote=True)
    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>WorkRun 상세 · AI Software Command Center</title>
  <link rel="stylesheet" href="/command-center/assets/app.css">
  <script src="/command-center/assets/app.js" defer></script>
</head>
<body data-page="work-run-detail" data-work-run-id="{safe_work_run_id}">
  <header class="site-header">
    <div>
      <a class="back-link" href="/command-center">← Command Center</a>
      <p class="eyebrow">WorkRun 읽기 projection</p>
      <h1>WorkRun 상세</h1>
      <p class="project-line">WorkRun ID <strong id="work-run-id-label"></strong></p>
      <p class="project-line"><a id="detail-project-link" hidden>프로젝트 큐로</a></p>
    </div>
    <p class="exposure-badge">로컬 / 비공개 / 읽기 전용 (LOCAL / PRIVATE / READ ONLY)</p>
  </header>
  <main class="detail-main">
    <section class="panel detail-panel" aria-labelledby="detail-summary-heading">
      <div class="section-heading-row">
        <div>
          <p class="kicker">권위 있는 현재 snapshot</p>
          <h2 id="detail-summary-heading">WorkRun / Task reference</h2>
        </div>
        <button id="detail-refresh-button" type="button">수동 새로고침</button>
      </div>
      <div id="detail-read-state" class="read-state detail-read-state" data-state="LOADING"
           aria-live="polite" aria-atomic="true">
        <span id="detail-state-name" class="state-name">불러오는 중</span>
        <span id="detail-state-message">WorkRun snapshot을 불러오고 있습니다.</span>
      </div>
      <div id="work-run-summary" class="detail-grid"></div>
    </section>

    <section class="panel detail-panel" aria-labelledby="task-scope-heading">
      <p class="kicker">참조와 availability</p>
      <h2 id="task-scope-heading">Task / 범위</h2>
      <div id="task-scope-content" class="detail-grid"></div>
    </section>

    <section id="blocker-section" class="panel detail-panel"
             aria-labelledby="blocker-heading" hidden>
      <p class="kicker">안전한 provenance</p>
      <h2 id="blocker-heading">blocker</h2>
      <div id="blocker-content" class="detail-grid"></div>
    </section>

    <section class="panel detail-panel" aria-labelledby="transitions-heading">
      <div class="section-heading-row">
        <div>
          <p class="kicker">API 순서 그대로</p>
          <h2 id="transitions-heading">전이 기록 (TransitionDecision)</h2>
        </div>
        <p id="transitions-state" class="section-read-state" aria-live="polite">불러오는 중</p>
      </div>
      <p class="projection-note">
        ADMITTED와 DENIED는 서로 다른 결정 결과입니다. DENIED는 성공한 상태 전이를 뜻하지 않습니다.
      </p>
      <ol id="transition-list" class="transition-list"></ol>
    </section>

    <section class="panel detail-panel" aria-labelledby="execution-heading">
      <div class="section-heading-row">
        <div>
          <p class="kicker">safe read projection</p>
          <h2 id="execution-heading">실행 기록 (Execution)</h2>
        </div>
        <p id="execution-state" class="section-read-state" aria-live="polite">불러오는 중</p>
      </div>
      <div id="execution-list" class="execution-list"></div>
    </section>

    <section class="panel detail-panel" aria-labelledby="evidence-heading">
      <div class="section-heading-row">
        <div>
          <p class="kicker">requirement부터 attestation까지 분리</p>
          <h2 id="evidence-heading">증거 상세 (Evidence)</h2>
        </div>
        <p id="evidence-state" class="section-read-state" aria-live="polite">불러오는 중</p>
      </div>
      <p class="projection-note">
        EvidenceCandidate, admission decision, AdmittedEvidence, requirement satisfaction,
        set satisfaction은 서로 대체되지 않습니다.
        증거 부재나 UNSATISFIED를 Judgment로 해석하지 않습니다.
      </p>
      <div id="evidence-meta" class="endpoint-meta"></div>
      <div class="evidence-sections">
        <section class="evidence-group" aria-labelledby="requirement-sets-heading">
          <h3 id="requirement-sets-heading">요구사항 집합 (EvidenceRequirementSet)</h3>
          <div id="requirement-set-list" class="record-list"></div>
        </section>
        <section class="evidence-group" aria-labelledby="checkpoints-heading">
          <h3 id="checkpoints-heading">체크포인트 (EvidenceCheckpoint)</h3>
          <div id="checkpoint-list" class="record-list"></div>
        </section>
        <section class="evidence-group" aria-labelledby="requirements-heading">
          <h3 id="requirements-heading">요구사항 (EvidenceRequirement)</h3>
          <div id="requirement-list" class="record-list"></div>
        </section>
        <section class="evidence-group" aria-labelledby="candidates-heading">
          <h3 id="candidates-heading">후보 (EvidenceCandidate)</h3>
          <div id="candidate-list" class="record-list"></div>
        </section>
        <section class="evidence-group" aria-labelledby="admission-decisions-heading">
          <h3 id="admission-decisions-heading">입장 판정 (EvidenceAdmissionDecision)</h3>
          <div id="admission-decision-list" class="record-list"></div>
        </section>
        <section class="evidence-group" aria-labelledby="admitted-evidence-heading">
          <h3 id="admitted-evidence-heading">입장된 증거 (AdmittedEvidence)</h3>
          <div id="admitted-evidence-list" class="record-list"></div>
        </section>
        <section class="evidence-group" aria-labelledby="satisfaction-heading">
          <h3 id="satisfaction-heading">요구사항 충족 기록 (RequirementSatisfaction)</h3>
          <div id="satisfaction-list" class="record-list"></div>
        </section>
        <section class="evidence-group" aria-labelledby="set-authority-heading">
          <h3 id="set-authority-heading">집합 평가 / attestation</h3>
          <div id="set-evaluation-list" class="record-list"></div>
          <div id="set-attestation-list" class="record-list record-list-secondary"></div>
        </section>
      </div>
    </section>

    <section class="panel detail-panel" aria-labelledby="human-judgment-heading">
      <div class="section-heading-row">
        <div>
          <p class="kicker">서로 독립된 네 권위 차원</p>
          <h2 id="human-judgment-heading">사람 검토 / 판정 상세</h2>
        </div>
        <p id="human-judgment-state" class="section-read-state" aria-live="polite">
          불러오는 중
        </p>
      </div>
      <p class="projection-note">
        HumanGate, HumanResult, Judgment, Transition Effect는 별도 기록입니다.
        HumanResult나 Judgment만으로 WorkflowState 전이가 완료됐다고 해석하지 않습니다.
      </p>
      <div id="human-judgment-meta" class="endpoint-meta"></div>
      <div class="human-dimension-grid">
        <article class="authority-dimension-card" aria-labelledby="human-gate-heading">
          <h3 id="human-gate-heading">사람 검토 관문 (HumanGate)</h3>
          <div id="human-gate-content"></div>
        </article>
        <article class="authority-dimension-card" aria-labelledby="human-result-heading">
          <h3 id="human-result-heading">사람 검토 결과 (HumanResult)</h3>
          <div id="human-result-content"></div>
        </article>
        <article class="authority-dimension-card" aria-labelledby="judgment-heading">
          <h3 id="judgment-heading">판정 (Judgment)</h3>
          <div id="judgment-content"></div>
        </article>
        <article class="authority-dimension-card" aria-labelledby="transition-effect-heading">
          <h3 id="transition-effect-heading">전이 효과 (Transition Effect)</h3>
          <div id="transition-effect-content"></div>
        </article>
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
.work-run-detail-link { display: inline-block; margin-bottom: 0.9rem; font-weight: 750; }
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

.detail-main { display: grid; gap: 1.2rem; }
.detail-panel { min-width: 0; padding: 1.2rem; }
.detail-read-state {
  margin: 0 0 1rem auto;
  padding: 0.75rem;
  border: 1px solid var(--line);
  border-radius: 0.55rem;
  background: #0d131a;
}
.detail-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.75rem;
  min-width: 0;
}
.detail-definition {
  min-width: 0;
  margin: 0;
  padding: 0.8rem;
  border: 1px solid var(--line);
  border-radius: 0.55rem;
  background: #0d131a;
}
.detail-definition dt {
  margin-bottom: 0.5rem;
  color: var(--muted);
  font-size: 0.78rem;
  font-weight: 750;
}
.detail-definition dd { margin: 0; line-height: 1.5; overflow-wrap: anywhere; }
.detail-definition-wide { grid-column: 1 / -1; }
.section-read-state { margin: 0; color: var(--muted); text-align: right; }
.transition-list, .operation-list { display: grid; gap: 0.9rem; margin: 0; padding-left: 1.5rem; }
.transition-item, .execution-attempt, .operation-item {
  min-width: 0;
  padding: 1rem;
  border: 1px solid var(--line);
  border-radius: 0.7rem;
  background: #0d131a;
  overflow-wrap: anywhere;
}
.transition-item::marker { color: var(--muted); font-weight: 800; }
.transition-admitted { border-left: 4px solid var(--accent); }
.transition-denied { border-left: 4px solid var(--danger); }
.decision-badge {
  display: inline-block;
  margin: 0 0 0.8rem;
  padding: 0.28rem 0.55rem;
  border: 1px solid currentColor;
  border-radius: 999px;
  font-size: 0.76rem;
  font-weight: 850;
  letter-spacing: 0.08em;
}
.transition-admitted .decision-badge { color: var(--accent); }
.transition-denied .decision-badge { color: var(--danger); }
.transition-columns {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.75rem;
}
.transition-column { min-width: 0; }
.transition-column h3, .execution-attempt h3, .operation-item h4 { margin: 0 0 0.7rem; }
.guard-list { margin: 0.5rem 0 0; padding-left: 1.2rem; }
.semantic-warning { color: var(--warning); font-weight: 750; }
.empty-state {
  margin: 0;
  padding: 1rem;
  border: 1px dashed var(--line);
  border-radius: 0.55rem;
  color: var(--muted);
}
.execution-list { display: grid; gap: 1rem; }
.attempt-meta { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 0.75rem; }
.execution-help { margin: 0.8rem 0; color: var(--warning); }
.operation-list { margin-top: 0.8rem; }
.endpoint-meta { margin-bottom: 1rem; }
.endpoint-meta:empty { display: none; }
.evidence-sections { display: grid; gap: 1rem; min-width: 0; }
.evidence-group {
  min-width: 0;
  padding: 1rem;
  border: 1px solid var(--line);
  border-radius: 0.7rem;
  background: var(--surface);
}
.evidence-group h3, .authority-dimension-card h3 { margin: 0 0 0.8rem; }
.record-list { display: grid; gap: 0.75rem; min-width: 0; }
.record-list-secondary { margin-top: 0.75rem; }
.evidence-card, .authority-dimension-card {
  min-width: 0;
  padding: 0.9rem;
  border: 1px solid var(--line);
  border-radius: 0.6rem;
  background: #0d131a;
  overflow-wrap: anywhere;
}
.evidence-card h4 { margin: 0 0 0.7rem; }
.human-dimension-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.9rem;
  min-width: 0;
}
.authority-dimension-card { border-left: 3px solid var(--accent); }

@media (max-width: 1180px) {
  .filter-grid { grid-template-columns: repeat(3, minmax(10rem, 1fr)); }
  .authority-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .detail-grid, .transition-columns, .attempt-meta {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 720px) {
  .site-header, .section-heading-row { flex-direction: column; }
  .input-action-row, .filter-grid { grid-template-columns: 1fr; }
  .identity-grid, .state-strip, .authority-grid { grid-template-columns: 1fr; }
  .detail-grid, .transition-columns, .attempt-meta, .human-dimension-grid {
    grid-template-columns: 1fr;
  }
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

  // These read sections commit a fully validated detached tree, never a partial snapshot.
  function readText(value) {
    if (value === null || value === undefined || value === "") return "제공되지 않음";
    if (typeof value !== "string" && typeof value !== "number") {
      throw new Error("invalid scalar");
    }
    return String(value);
  }

  function requireId(value) {
    if (typeof value !== "string" || !value.trim()) throw new Error("missing identity");
    return value;
  }

  function readDefinition(label, values, wide = false) {
    const list = document.createElement("dl");
    list.className = "detail-definition" + (wide ? " detail-definition-wide" : "");
    const term = document.createElement("dt");
    term.textContent = label;
    const description = document.createElement("dd");
    values.forEach(([name, value]) => {
      const line = document.createElement("p");
      line.className = "cell-line";
      line.textContent = name + ": " + readText(value);
      description.appendChild(line);
    });
    list.append(term, description);
    return list;
  }

  function readLink(kind, id, label) {
    const link = document.createElement("a");
    link.className = "work-run-detail-link";
    link.href = "/command-center/" + kind + "/" + encodeURIComponent(requireId(id));
    link.textContent = label;
    return link;
  }

  function presenceFields(value, fields) {
    if (!value || !["PRESENT", "NONE"].includes(value.presence)) {
      throw new Error("invalid presence");
    }
    return value.presence === "NONE"
      ? [["기록", "없음 (NONE)"]]
      : [["기록", "있음 (PRESENT)"], ...fields.map(([label, key]) => [label, value[key]])];
  }

  function createReadSection(contentId, stateId, label, render) {
    const content = document.getElementById(contentId);
    const state = document.getElementById(stateId);
    const endpoint = { etag: null, url: null, hasData: false };
    function retained(reason) {
      state.textContent = endpoint.hasData
        ? label + " · 마지막 성공 결과 보존 (retained/stale) · " + reason
        : label + " · 성공한 snapshot 없음 · " + reason;
    }
    async function read(url) {
      const headers = {};
      if (endpoint.hasData && endpoint.url === url && endpoint.etag) {
        headers["If-None-Match"] = endpoint.etag;
      }
      try {
        const response = await fetch(url, {
          method: "GET", headers, cache: "no-store", credentials: "same-origin",
        });
        if (response.status === 304) {
          return endpoint.hasData && endpoint.url === url
            ? { kind: "not-modified", url }
            : { kind: "error", reason: "확인할 이전 snapshot 없이 304 응답" };
        }
        if (response.status !== 200) {
          const failures = {
            400: "조회 요청 오류", 404: "요청한 기록 없음",
            409: "권위 상태 충돌", 503: "조회 projection 사용 불가",
          };
          return { kind: "error", reason: failures[response.status] || "조회 오류" };
        }
        const envelope = await response.json();
        return {
          kind: "success", url, data: envelope.data, meta: envelope.meta,
          etag: response.headers.get("ETag"),
        };
      } catch (_error) {
        return { kind: "error", reason: "읽기 요청을 완료하지 못했습니다" };
      }
    }
    function apply(result) {
      if (result.kind === "not-modified" && endpoint.hasData && endpoint.url === result.url) {
        state.textContent = label + " · 변경 없음 · 기존 snapshot 재확인";
        return true;
      }
      if (result.kind !== "success") {
        retained("새로고침 실패 · " + (result.reason || "조회 오류"));
        return false;
      }
      try {
        const fragment = render(result.data, result.meta);
        content.replaceChildren(fragment);
        endpoint.etag = result.etag;
        endpoint.url = result.url;
        endpoint.hasData = true;
        state.textContent = label + " · 현재 조회 결과";
        return true;
      } catch (_error) {
        retained("새로고침 실패 · projection 형식을 확인할 수 없습니다");
        return false;
      }
    }
    return { read, apply, retained };
  }

  function renderCycle(data) {
    if (!data || data.cycle_id !== document.body.dataset.cycleId ||
        !data.task_contract || !data.task_constraint || !Array.isArray(data.current_memory)) {
      throw new Error("invalid Cycle projection");
    }
    const fragment = document.createDocumentFragment();
    const navigation = document.createElement("nav");
    navigation.className = "detail-definition-wide";
    navigation.setAttribute("aria-label", "Cycle 연결된 프로젝트와 작업");
    navigation.append(
      readLink("projects", data.project_id, "프로젝트 큐 / 다음 행동으로"),
      document.createTextNode(" · "),
      readLink("work-runs", data.work_run_id, "WorkRun 증거 / 사람 검토 / 판정으로"),
    );
    fragment.append(
      navigation,
      readDefinition("Cycle 식별 / 입장 계보", [
        ["Cycle ID", data.cycle_id], ["version", data.cycle_version],
        ["참조", data.cycle_ref], ["fingerprint", data.cycle_fingerprint],
        ["입장 순번", data.admission_sequence], ["입장 시각", data.admitted_at],
      ]),
      readDefinition("작업 연결", [
        ["Project ID", data.project_id], ["WorkRun ID", data.work_run_id],
        ["TaskContract ID", data.task_contract.id],
        ["TaskContract version", data.task_contract.version],
      ]),
      readDefinition("판정 / 전이 계보 (서로 다른 참조)", [
        ["Judgment ref", data.judgment_ref],
        ["TransitionDecision ID", data.transition_decision_id],
        ["종료 상태 버전", data.terminal_state_version],
      ]),
      readDefinition("입장된 증거 계보", [
        ["Evidence attestation ref", data.evidence_attestation_ref],
        ["Evidence root", data.evidence_root],
      ]),
      readDefinition("Task 제약 참조", presenceFields(data.task_constraint, [
        ["constraint_ref", "constraint_ref"], ["constraint_fingerprint", "constraint_fingerprint"],
        ["snapshot_ref", "snapshot_ref"], ["snapshot_fingerprint", "snapshot_fingerprint"],
        ["owner_event_high_watermark", "owner_event_high_watermark"],
      ])),
    );
    const memory = document.createElement("section");
    memory.className = "detail-definition-wide record-list";
    const heading = document.createElement("h3");
    heading.textContent = "현재 프로젝트 메모리 맥락 · 과거 Cycle 결과와 별개";
    memory.appendChild(heading);
    if (data.current_memory.length === 0) {
      const empty = document.createElement("p");
      empty.textContent = "표시 가능한 현재 프로젝트 메모리 없음";
      memory.appendChild(empty);
    }
    data.current_memory.forEach((item) => memory.appendChild(readDefinition("메모리 요약", [
      ["entry_id", item.entry_id], ["category", item.category], ["privacy", item.privacy],
      ["content_fingerprint", item.content_fingerprint], ["applicability", item.applicability],
      ["authority_revision", item.authority_revision], ["created_at", item.created_at],
    ])));
    fragment.appendChild(memory);
    return fragment;
  }

  if (page === "cycle-detail") {
    const url = "/v1/command-center/cycles/" + encodeURIComponent(document.body.dataset.cycleId);
    const cycle = createReadSection("cycle-content", "cycle-state", "Cycle", renderCycle);
    const refresh = document.getElementById("cycle-refresh-button");
    let inFlight = false;
    async function loadCycle() {
      if (inFlight) return;
      inFlight = true;
      refresh.disabled = true;
      try {
        cycle.apply(await cycle.read(url));
      } finally {
        inFlight = false;
        refresh.disabled = false;
      }
    }
    refresh.addEventListener("click", () => void loadCycle());
    void loadCycle();
    return;
  }

  if (page === "work-run-detail") {
    const TERMINAL_WORKFLOW_STATES = new Set(["ACCEPTED", "REJECTED", "FAILED"]);
    const POLL_INTERVAL_MS = 10000;
    const SAFE_ERROR_CODES = new Set([
      "INVALID_QUERY",
      "NOT_FOUND",
      "AUTHORITY_CONFLICT",
      "NO_LONGER_CURRENT",
      "PROJECTION_UNAVAILABLE",
      "INTERNAL_ERROR",
    ]);
    const DETAIL_STATE_COPY = {
      LOADING: ["불러오는 중", "WorkRun snapshot을 불러오고 있습니다."],
      READY: ["최신 상태", "다섯 read projection을 확인했습니다."],
      UNCHANGED: ["변경 없음", "현재 표시 중인 section을 그대로 유지합니다."],
      PARTIAL_ERROR: [
        "일부 조회 실패",
        "현재 WorkRun은 확인했지만 일부 section을 갱신하지 못했습니다.",
      ],
      NOT_FOUND: ["WorkRun 없음", "요청한 WorkRun을 찾을 수 없습니다."],
      AUTHORITY_CONFLICT: ["권위 상태 충돌", "권위 있는 현재 snapshot을 확정할 수 없습니다."],
      NO_LONGER_CURRENT: ["현재 snapshot 아님", "요청 결과가 더 이상 현재 상태가 아닙니다."],
      PROJECTION_UNAVAILABLE: [
        "조회 projection 사용 불가",
        "Command Center read projection을 현재 사용할 수 없습니다.",
      ],
      INVALID_QUERY: ["조회 요청 오류", "WorkRun 읽기 요청을 처리할 수 없습니다."],
      INTERNAL_ERROR: ["조회 오류", "읽기 요청을 안전하게 완료하지 못했습니다."],
      UNEXPECTED_ERROR: ["조회 오류", "읽기 요청을 안전하게 완료하지 못했습니다."],
    };

    const workRunId = document.body.dataset.workRunId;
    const encodedWorkRunId = encodeURIComponent(workRunId);
    const detailEndpoints = {
      summary: {
        url: "/v1/command-center/work-runs/" + encodedWorkRunId,
        etag: null,
        hasData: false,
      },
      transitions: {
        url: "/v1/command-center/work-runs/" + encodedWorkRunId + "/transitions",
        etag: null,
        hasData: false,
      },
      execution: {
        url: "/v1/command-center/work-runs/" + encodedWorkRunId + "/execution",
        etag: null,
        hasData: false,
      },
      evidence: {
        url: "/v1/command-center/work-runs/" + encodedWorkRunId + "/evidence",
        etag: null,
        hasData: false,
      },
      humanJudgment: {
        url: "/v1/command-center/work-runs/" + encodedWorkRunId + "/human-judgment",
        etag: null,
        hasData: false,
      },
    };
    const workRunLabel = document.getElementById("work-run-id-label");
    const projectLink = document.getElementById("detail-project-link");
    const refreshButton = document.getElementById("detail-refresh-button");
    const detailState = document.getElementById("detail-read-state");
    const detailStateName = document.getElementById("detail-state-name");
    const detailStateMessage = document.getElementById("detail-state-message");
    const summaryContent = document.getElementById("work-run-summary");
    const taskScopeContent = document.getElementById("task-scope-content");
    const blockerSection = document.getElementById("blocker-section");
    const blockerContent = document.getElementById("blocker-content");
    const transitionsState = document.getElementById("transitions-state");
    const transitionList = document.getElementById("transition-list");
    const executionState = document.getElementById("execution-state");
    const executionList = document.getElementById("execution-list");
    const evidenceState = document.getElementById("evidence-state");
    const evidenceMeta = document.getElementById("evidence-meta");
    const requirementSetList = document.getElementById("requirement-set-list");
    const checkpointList = document.getElementById("checkpoint-list");
    const requirementList = document.getElementById("requirement-list");
    const candidateList = document.getElementById("candidate-list");
    const admissionDecisionList = document.getElementById("admission-decision-list");
    const admittedEvidenceList = document.getElementById("admitted-evidence-list");
    const satisfactionList = document.getElementById("satisfaction-list");
    const setEvaluationList = document.getElementById("set-evaluation-list");
    const setAttestationList = document.getElementById("set-attestation-list");
    const humanJudgmentState = document.getElementById("human-judgment-state");
    const humanJudgmentMeta = document.getElementById("human-judgment-meta");
    const humanGateContent = document.getElementById("human-gate-content");
    const humanResultContent = document.getElementById("human-result-content");
    const judgmentContent = document.getElementById("judgment-content");
    const transitionEffectContent = document.getElementById("transition-effect-content");

    workRunLabel.textContent = workRunId;

    let lastWorkflowState = null;
    let pollTimer = null;
    let requestInFlight = false;
    let refreshAfterFlight = false;

    function display(value, fallback = "값 없음") {
      if (value === null || value === undefined || value === "") return fallback;
      return String(value);
    }

    function setDetailState(name, message = null) {
      const copy = DETAIL_STATE_COPY[name] || DETAIL_STATE_COPY.UNEXPECTED_ERROR;
      detailStateName.textContent = copy[0];
      detailStateMessage.textContent = message || copy[1];
      detailState.dataset.state = name;
    }

    function paragraph(text, className = "cell-line") {
      const item = document.createElement("p");
      item.className = className;
      item.textContent = text;
      return item;
    }

    function definition(label, lines, wide = false) {
      const list = document.createElement("dl");
      list.className = "detail-definition" + (wide ? " detail-definition-wide" : "");
      const term = document.createElement("dt");
      term.textContent = label;
      const description = document.createElement("dd");
      lines.forEach((line) => description.appendChild(paragraph(line)));
      list.append(term, description);
      return list;
    }

    function fixedArrayLines(label, values) {
      if (!Array.isArray(values) || values.length === 0) return [label + ": 없음"];
      return values.map((value) => label + ": " + display(value));
    }

    function sourceRevisionLines(sourceRevisions) {
      if (!sourceRevisions || typeof sourceRevisions !== "object") {
        return ["source revision 없음"];
      }
      const entries = Object.entries(sourceRevisions);
      if (entries.length === 0) return ["source revision 없음"];
      return entries.map(([name, value]) => name + ": " + display(value));
    }

    function renderSummary(data, meta) {
      if (
        !data || data.work_run_id !== workRunId || !data.workflow ||
        !data.task_contract || typeof data.project_id !== "string"
      ) {
        throw new Error("invalid WorkRun summary projection");
      }
      projectLink.href = "/command-center/projects/" + encodeURIComponent(data.project_id);
      projectLink.hidden = false;
      summaryContent.replaceChildren(
        definition("Project ID", [data.project_id]),
        definition("WorkRun ID", [data.work_run_id]),
        definition("TaskContract", [
          "ID: " + display(data.task_contract.id),
          "version: " + display(data.task_contract.version),
        ]),
        definition("현재 상태 (WorkflowState)", [
          display(data.workflow.state),
          "state_version: " + display(data.workflow.state_version),
        ]),
        definition("RuntimeMode", [display(data.runtime_mode)]),
        definition("Workflow 시간", [
          "created_at: " + display(data.workflow.created_at),
          "updated_at: " + display(data.workflow.updated_at),
        ]),
        definition("source_revisions", sourceRevisionLines(meta && meta.source_revisions), true),
      );

      const taskDisplay = data.task_display || {};
      const scope = data.scope || {};
      const constraint = data.task_constraint || {};
      const taskLines = [
        "availability: " + display(taskDisplay.availability),
        "message: " + display(taskDisplay.message),
      ];
      if (taskDisplay.availability === "AVAILABLE") {
        if (taskDisplay.title) taskLines.push("title: " + display(taskDisplay.title));
        if (taskDisplay.type) taskLines.push("type: " + display(taskDisplay.type));
        if (taskDisplay.source_ref) {
          taskLines.push("source_ref: " + display(taskDisplay.source_ref));
        }
      }
      const scopeLines = [
        "availability: " + display(scope.availability),
        "message: " + display(scope.message),
      ];
      if (scope.availability === "AVAILABLE") {
        if (Array.isArray(scope.allowed)) {
          scopeLines.push(...fixedArrayLines("allowed", scope.allowed));
        }
        if (Array.isArray(scope.forbidden)) {
          scopeLines.push(...fixedArrayLines("forbidden", scope.forbidden));
        }
      }
      taskScopeContent.replaceChildren(
        definition("Task display", taskLines),
        definition("Scope availability", scopeLines),
        definition("Task constraint reference", [
          "presence: " + display(constraint.presence),
          "constraint_ref: " + display(constraint.constraint_ref),
          "constraint_fingerprint: " + display(constraint.constraint_fingerprint),
          "snapshot_ref: " + display(constraint.snapshot_ref),
          "snapshot_fingerprint: " + display(constraint.snapshot_fingerprint),
          "owner_event_high_watermark: " + display(constraint.owner_event_high_watermark),
        ]),
      );

      const blocker = data.blocker || {};
      blockerSection.hidden = blocker.presence !== "PRESENT";
      if (blocker.presence === "PRESENT") {
        blockerContent.replaceChildren(definition("현재 blocker", [
          "blocker_ref: " + display(blocker.blocker_ref),
          "blocker_kind: " + display(blocker.blocker_kind),
          "reason_code: " + display(blocker.reason_code),
          "resumability: " + display(blocker.resumability),
          "blocked_epoch: " + display(blocker.blocked_epoch),
          "authority_revision: " + display(blocker.authority_revision),
          "updated_at: " + display(blocker.updated_at),
        ], true));
      } else {
        blockerContent.replaceChildren();
      }
      lastWorkflowState = data.workflow.state;
    }

    function appendLines(container, lines) {
      lines.forEach((line) => container.appendChild(paragraph(line)));
    }

    function renderTransitions(data) {
      if (!data || data.work_run_id !== workRunId || !Array.isArray(data.items)) {
        throw new Error("invalid transitions projection");
      }
      if (data.items.length === 0) {
        const empty = document.createElement("li");
        empty.className = "empty-state";
        empty.textContent = "전이 기록 없음";
        transitionList.replaceChildren(empty);
        return;
      }
      const fragment = document.createDocumentFragment();
      data.items.forEach((record) => {
        const request = record && record.request ? record.request : {};
        const evaluation = record && record.evaluation ? record.evaluation : {};
        const decision = record && record.decision ? record.decision : {};
        const item = document.createElement("li");
        const outcomeClass = decision.outcome === "DENIED"
          ? "transition-denied"
          : decision.outcome === "ADMITTED" ? "transition-admitted" : "";
        item.className = ("transition-item " + outcomeClass).trim();
        const badge = document.createElement("p");
        badge.className = "decision-badge";
        badge.textContent = "TransitionDecision · " + display(decision.outcome);
        item.appendChild(badge);
        if (decision.outcome === "DENIED") {
          const deniedCopy = decision.derived_state_effect === "UNCHANGED"
            ? "DENIED · authoritative state를 변경하지 않은 요청/결정 기록입니다."
            : "DENIED · 성공한 state transition으로 표시하지 않습니다.";
          item.appendChild(paragraph(deniedCopy, "semantic-warning"));
        }
        const columns = document.createElement("div");
        columns.className = "transition-columns";

        const requestColumn = document.createElement("section");
        requestColumn.className = "transition-column";
        const requestHeading = document.createElement("h3");
        requestHeading.textContent = "요청 (TransitionRequest)";
        requestColumn.appendChild(requestHeading);
        appendLines(requestColumn, [
          "request ID: " + display(request.transition_request_id),
          "observed WorkflowState: " + display(request.observed_state),
          "observed state_version: " + display(request.observed_state_version),
          "target WorkflowState: " + display(request.target_state),
          "requester type: " + display(request.requester_type),
          "RuntimeMode: " + display(request.runtime_mode),
          "parent request ID: " + display(request.parent_request_id),
          "created_at: " + display(request.created_at),
          ...fixedArrayLines("evidence ref", request.evidence_refs),
          ...fixedArrayLines("HumanResult ref", request.human_result_refs),
          ...fixedArrayLines("Judgment ref", request.judgment_refs),
        ]);

        const evaluationColumn = document.createElement("section");
        evaluationColumn.className = "transition-column";
        const evaluationHeading = document.createElement("h3");
        evaluationHeading.textContent = "평가 / guards";
        evaluationColumn.appendChild(evaluationHeading);
        appendLines(evaluationColumn, [
          "evaluation ID: " + display(evaluation.transition_evaluation_id),
          "authoritative WorkflowState: " + display(evaluation.authoritative_state),
          "authoritative state_version: " + display(evaluation.authoritative_state_version),
          "evaluated_at: " + display(evaluation.evaluated_at),
          ...fixedArrayLines("missing guard", evaluation.missing_guards),
        ]);
        const guardList = document.createElement("ul");
        guardList.className = "guard-list";
        const guards = Array.isArray(evaluation.guards) ? evaluation.guards : [];
        if (guards.length === 0) {
          const guard = document.createElement("li");
          guard.textContent = "guard 기록 없음";
          guardList.appendChild(guard);
        } else {
          guards.forEach((guardValue) => {
            const guard = document.createElement("li");
            guard.textContent = display(guardValue.guard_id) + " · " +
              display(guardValue.outcome) + " · " + display(guardValue.reason);
            guardList.appendChild(guard);
          });
        }
        evaluationColumn.appendChild(guardList);

        const decisionColumn = document.createElement("section");
        decisionColumn.className = "transition-column";
        const decisionHeading = document.createElement("h3");
        decisionHeading.textContent = "결정 (TransitionDecision)";
        decisionColumn.appendChild(decisionHeading);
        appendLines(decisionColumn, [
          "decision ID: " + display(decision.transition_decision_id),
          "outcome: " + display(decision.outcome),
          "reason: " + display(decision.reason),
          "resulting WorkflowState: " + display(decision.resulting_state),
          "resulting state_version: " + display(decision.resulting_state_version),
          "derived_state_effect: " + display(decision.derived_state_effect),
          "decided_at: " + display(decision.decided_at),
        ]);
        columns.append(requestColumn, evaluationColumn, decisionColumn);
        item.appendChild(columns);
        fragment.appendChild(item);
      });
      transitionList.replaceChildren(fragment);
    }

    function renderExecution(data) {
      if (!data || data.work_run_id !== workRunId || !Array.isArray(data.attempts)) {
        throw new Error("invalid execution projection");
      }
      if (data.attempts.length === 0) {
        const empty = document.createElement("p");
        empty.className = "empty-state";
        empty.textContent = "실행 기록 없음";
        executionList.replaceChildren(empty);
        return;
      }
      const fragment = document.createDocumentFragment();
      data.attempts.forEach((attempt) => {
        const card = document.createElement("article");
        card.className = "execution-attempt";
        const heading = document.createElement("h3");
        heading.textContent = "Attempt " + display(attempt.attempt_ordinal) + " · " +
          display(attempt.execution_attempt_id);
        card.appendChild(heading);
        const meta = document.createElement("div");
        meta.className = "attempt-meta";
        const taskContract = attempt.task_contract || {};
        const counters = attempt.counters || {};
        const submission = attempt.submission || {};
        meta.append(
          definition("TaskContract", [
            "ID: " + display(taskContract.id),
            "version: " + display(taskContract.version),
          ]),
          definition("RuntimeMode", [display(attempt.runtime_mode)]),
          definition("생성 WorkflowState", [
            display(attempt.creation_state),
            "state_version: " + display(attempt.creation_state_version),
          ]),
          definition("ExecutionStatus", [
            display(attempt.status),
            "execution_version: " + display(attempt.execution_version),
          ]),
          definition("provider registry identity", [
            "provider_profile_id: " + display(attempt.provider_profile_id),
            "provider_profile_version: " + display(attempt.provider_profile_version),
          ]),
          definition("tool registry identity", [
            "tool_registry_id: " + display(attempt.tool_registry_id),
            "tool_registry_version: " + display(attempt.tool_registry_version),
          ]),
          definition("durable counters", [
            "schema_version: " + display(counters.schema_version),
            "provider_calls: " + display(counters.provider_calls),
            "agent_rounds: " + display(counters.agent_rounds),
            "tool_calls: " + display(counters.tool_calls),
            "provider_retries: " + display(counters.provider_retries),
            "output_bytes: " + display(counters.output_bytes),
            "output_tokens: " + display(counters.output_tokens),
            "budget_units: " + display(counters.budget_units),
            "started_at: " + display(counters.started_at),
            "deadline_at: " + display(counters.deadline_at),
          ]),
          definition("submission", [
            "presence: " + display(submission.presence),
            "submission_ref: " + display(submission.submission_ref),
            "content_hash: " + display(submission.content_hash),
          ]),
          definition("attempt provenance", [
            "parent_attempt_id: " + display(attempt.parent_attempt_id),
            "causal WorkflowState: " + display(attempt.causal_state),
            "causal state_version: " + display(attempt.causal_state_version),
            "created_at: " + display(attempt.created_at),
            "updated_at: " + display(attempt.updated_at),
          ]),
        );
        card.appendChild(meta);
        if (attempt.status === "EXECUTOR_COMPLETED") {
          card.appendChild(paragraph(
            "EXECUTOR_COMPLETED는 실행 산출 제출 완료를 의미하며 " +
              "WorkRun ACCEPTED를 의미하지 않습니다.",
            "execution-help",
          ));
        }

        const operationsHeading = document.createElement("h4");
        operationsHeading.textContent = "operations";
        card.appendChild(operationsHeading);
        const operations = Array.isArray(attempt.operations) ? attempt.operations : [];
        if (operations.length === 0) {
          card.appendChild(paragraph("operation 기록 없음", "empty-state"));
        } else {
          const operationList = document.createElement("ol");
          operationList.className = "operation-list";
          operations.forEach((operation) => {
            const operationItem = document.createElement("li");
            operationItem.className = "operation-item";
            const operationHeading = document.createElement("h4");
            operationHeading.textContent = "Operation " + display(operation.call_ordinal);
            operationItem.appendChild(operationHeading);
            appendLines(operationItem, [
              "operation_id: " + display(operation.operation_id),
              "kind: " + display(operation.kind),
              "fingerprint: " + display(operation.fingerprint),
              "phase: " + display(operation.phase),
              "outcome: " + display(operation.outcome),
              "resource: " + display(operation.resource),
              "parent_operation_id: " + display(operation.parent_operation_id),
              "created_at: " + display(operation.created_at),
              "updated_at: " + display(operation.updated_at),
            ]);
            operationList.appendChild(operationItem);
          });
          card.appendChild(operationList);
        }
        fragment.appendChild(card);
      });
      executionList.replaceChildren(fragment);
    }

    function evidenceCard(title, lines) {
      const card = document.createElement("article");
      card.className = "evidence-card";
      const heading = document.createElement("h4");
      heading.textContent = title;
      card.appendChild(heading);
      appendLines(card, lines);
      return card;
    }

    function renderRecordList(container, records, emptyCopy, buildCard) {
      if (records.length === 0) {
        container.replaceChildren(paragraph(emptyCopy, "empty-state"));
        return;
      }
      const fragment = document.createDocumentFragment();
      records.forEach((record, index) => fragment.appendChild(buildCard(record || {}, index)));
      container.replaceChildren(fragment);
    }

    function renderEvidence(data, meta) {
      const collectionNames = [
        "requirement_sets",
        "checkpoints",
        "requirements",
        "candidates",
        "admission_decisions",
        "admitted_evidence",
        "satisfactions",
        "set_evaluations",
        "set_attestations",
      ];
      if (
        !data || data.work_run_id !== workRunId ||
        collectionNames.some((name) => !Array.isArray(data[name]))
      ) {
        throw new Error("invalid evidence projection");
      }
      evidenceMeta.replaceChildren(definition(
        "Evidence endpoint source_revisions",
        sourceRevisionLines(meta && meta.source_revisions),
        true,
      ));
      renderRecordList(
        requirementSetList,
        data.requirement_sets,
        "EvidenceRequirementSet 기록 없음",
        (item, index) => evidenceCard(
          "EvidenceRequirementSet " + display(index + 1),
          [
            "requirement_set_ref: " + display(item.requirement_set_ref),
            "semantic_owner: " + display(item.semantic_owner),
            ...fixedArrayLines("ordered requirement ref", item.ordered_requirement_refs),
            ...fixedArrayLines("ordered checkpoint ref", item.ordered_checkpoint_refs),
            "requirement_root_hash: " + display(item.requirement_root_hash),
            "fingerprint: " + display(item.fingerprint),
          ],
        ),
      );
      renderRecordList(
        checkpointList,
        data.checkpoints,
        "EvidenceCheckpoint 기록 없음",
        (item, index) => evidenceCard(
          "EvidenceCheckpoint " + display(index + 1),
          [
            "checkpoint_ref: " + display(item.checkpoint_ref),
            "source WorkflowState: " + display(item.source_state),
            "target WorkflowState: " + display(item.target_state),
            "transition_purpose_id: " + display(item.transition_purpose_id),
            "transition_purpose_version: " + display(item.transition_purpose_version),
            "requirement_set_ref: " + display(item.requirement_set_ref),
            "fingerprint: " + display(item.fingerprint),
          ],
        ),
      );
      renderRecordList(
        requirementList,
        data.requirements,
        "EvidenceRequirement 기록 없음",
        (item, index) => evidenceCard(
          "EvidenceRequirement " + display(index + 1),
          [
            "requirement_ref: " + display(item.requirement_ref),
            "profile: " + display(item.profile),
            "obligation: " + display(item.obligation),
            "semantic_owner: " + display(item.semantic_owner),
            "evidence_type_id: " + display(item.evidence_type_id),
            "evidence_type_version: " + display(item.evidence_type_version),
            "freshness_kind: " + display(item.freshness_kind),
            ...fixedArrayLines("applicable checkpoint ref", item.applicable_checkpoint_refs),
            "fingerprint: " + display(item.fingerprint),
          ],
        ),
      );
      renderRecordList(
        candidateList,
        data.candidates,
        "EvidenceCandidate 기록 없음",
        (item, index) => {
          const content = item.durable_content;
          const contentLines = content && typeof content === "object" ? [
            "safe content ref: " + display(content.content_ref),
            "content kind: " + display(content.content_kind),
            "schema: " + display(content.schema_id) + " / " + display(content.schema_version),
            "byte_count: " + display(content.byte_count),
            "safe content hash: " + display(content.content_hash),
            "content sensitivity: " + display(content.sensitivity),
          ] : ["durable content metadata: 없음"];
          return evidenceCard(
            "EvidenceCandidate " + display(index + 1),
            [
              "candidate_id: " + display(item.candidate_id),
              "candidate_version: " + display(item.candidate_version),
              "candidate_fingerprint: " + display(item.candidate_fingerprint),
              "checkpoint_ref: " + display(item.checkpoint_ref),
              "issuer_type: " + display(item.issuer_type),
              "sensitivity: " + display(item.sensitivity),
              "content_hash: " + display(item.content_hash),
              "created_at: " + display(item.created_at),
              ...contentLines,
            ],
          );
        },
      );
      renderRecordList(
        admissionDecisionList,
        data.admission_decisions,
        "EvidenceAdmissionDecision 기록 없음",
        (item, index) => evidenceCard(
          "EvidenceAdmissionDecision " + display(index + 1),
          [
            "decision_id: " + display(item.decision_id),
            "candidate_id: " + display(item.candidate_id),
            "requirement_ref: " + display(item.requirement_ref),
            "checkpoint_ref: " + display(item.checkpoint_ref),
            "outcome: " + display(item.outcome),
            "reason: " + display(item.reason),
            "decided_at: " + display(item.decided_at),
          ],
        ),
      );
      renderRecordList(
        admittedEvidenceList,
        data.admitted_evidence,
        "AdmittedEvidence 기록 없음",
        (item, index) => evidenceCard(
          "AdmittedEvidence " + display(index + 1),
          [
            "admitted_evidence_id: " + display(item.admitted_evidence_id),
            "decision_id: " + display(item.decision_id),
            "candidate_id: " + display(item.candidate_id),
            "requirement_ref: " + display(item.requirement_ref),
            "checkpoint_ref: " + display(item.checkpoint_ref),
            "content_hash: " + display(item.content_hash),
            ...fixedArrayLines("coverage", item.coverage),
            "admitted_at: " + display(item.admitted_at),
          ],
        ),
      );
      renderRecordList(
        satisfactionList,
        data.satisfactions,
        "RequirementSatisfaction 기록 없음",
        (item, index) => evidenceCard(
          "RequirementSatisfaction " + display(index + 1),
          [
            "satisfaction_id: " + display(item.satisfaction_id),
            "admitted_evidence_id: " + display(item.admitted_evidence_id),
            "requirement_ref: " + display(item.requirement_ref),
            "checkpoint_ref: " + display(item.checkpoint_ref),
            ...fixedArrayLines("coverage", item.coverage),
            "created_at: " + display(item.created_at),
          ],
        ),
      );
      renderRecordList(
        setEvaluationList,
        data.set_evaluations,
        "EvidenceSetEvaluation 기록 없음",
        (item, index) => evidenceCard(
          "EvidenceSetEvaluation " + display(index + 1),
          [
            "evaluation_id: " + display(item.evaluation_id),
            "checkpoint_ref: " + display(item.checkpoint_ref),
            "requirement_set_ref: " + display(item.requirement_set_ref),
            "outcome: " + display(item.outcome),
            "evidence_authority_revision: " + display(item.evidence_authority_revision),
            "evaluated_at: " + display(item.evaluated_at),
          ],
        ),
      );
      renderRecordList(
        setAttestationList,
        data.set_attestations,
        "EvidenceSetAttestation 기록 없음",
        (item, index) => evidenceCard(
          "EvidenceSetAttestation " + display(index + 1),
          [
            "attestation_id: " + display(item.attestation_id),
            "serialized_ref: " + display(item.serialized_ref),
            "checkpoint_ref: " + display(item.checkpoint_ref),
            "state_version: " + display(item.state_version),
            "evidence_authority_revision: " + display(item.evidence_authority_revision),
            "issued_at: " + display(item.issued_at),
            "expires_at: " + display(item.expires_at),
          ],
        ),
      );
    }

    function renderPresenceDimension(container, value, presentLines, emptyCopy) {
      if (!value || (value.presence !== "PRESENT" && value.presence !== "NONE")) {
        throw new Error("invalid presence projection");
      }
      if (value.presence === "NONE") {
        container.replaceChildren(paragraph(emptyCopy + " · presence: NONE", "empty-state"));
        return;
      }
      container.replaceChildren(...presentLines.map((line) => paragraph(line)));
    }

    function renderHumanJudgment(data, meta) {
      if (
        !data || data.work_run_id !== workRunId || !data.human_gate ||
        !data.human_result || !data.judgment || !data.transition_effect
      ) {
        throw new Error("invalid Human/Judgment projection");
      }
      humanJudgmentMeta.replaceChildren(definition(
        "Human/Judgment endpoint source_revisions",
        sourceRevisionLines(meta && meta.source_revisions),
        true,
      ));
      const gate = data.human_gate;
      renderPresenceDimension(humanGateContent, gate, [
        "presence: " + display(gate.presence),
        "human_gate_id: " + display(gate.human_gate_id),
        "gate_ref: " + display(gate.gate_ref),
        "purpose_id: " + display(gate.purpose_id),
        "purpose_version: " + display(gate.purpose_version),
        "HumanGateStatus: " + display(gate.status),
        "HumanGateSuspensionStatus: " + display(gate.suspension_status),
        "bound WorkflowState: " + display(gate.bound_state),
        "bound state_version: " + display(gate.bound_state_version),
        "authority_revision: " + display(gate.authority_revision),
        "opened_at: " + display(gate.opened_at),
        "updated_at: " + display(gate.updated_at),
      ], "HumanGate 기록 없음");
      const result = data.human_result;
      renderPresenceDimension(humanResultContent, result, [
        "presence: " + display(result.presence),
        "human_result_id: " + display(result.human_result_id),
        "human_result_ref: " + display(result.human_result_ref),
        "HumanResultKind: " + display(result.result_kind),
        "structured_reason_code: " + display(result.structured_reason_code),
        "authority_revision: " + display(result.authority_revision),
        "admitted_at: " + display(result.admitted_at),
        "HumanResult는 Judgment가 아닙니다.",
      ], "HumanResult 기록 없음");
      const judgment = data.judgment;
      renderPresenceDimension(judgmentContent, judgment, [
        "presence: " + display(judgment.presence),
        "judgment_id: " + display(judgment.judgment_id),
        "judgment_ref: " + display(judgment.judgment_ref),
        "JudgmentKind: " + display(judgment.kind),
        "owner_policy: " + display(judgment.owner_policy),
        "reason_code: " + display(judgment.reason_code),
        "state_version: " + display(judgment.state_version),
        "authority_revision: " + display(judgment.authority_revision),
        "issued_at: " + display(judgment.issued_at),
        "Judgment는 TransitionDecision이나 WorkflowState가 아닙니다.",
      ], "Judgment 기록 없음");
      const effect = data.transition_effect;
      renderPresenceDimension(transitionEffectContent, effect, [
        "presence: " + display(effect.presence),
        "transition_decision_id: " + display(effect.transition_decision_id),
        "DecisionOutcome: " + display(effect.outcome),
        "resulting WorkflowState: " + display(effect.resulting_state),
        "resulting state_version: " + display(effect.resulting_state_version),
        "derived_state_effect: " + display(effect.derived_state_effect),
      ], "Transition Effect 기록 없음");
    }

    function mapFailure(status, code) {
      if (SAFE_ERROR_CODES.has(code)) return code;
      if (status === 404) return "NOT_FOUND";
      if (status === 409) return "AUTHORITY_CONFLICT";
      if (status === 503) return "PROJECTION_UNAVAILABLE";
      if (status === 400) return "INVALID_QUERY";
      if (status === 500) return "INTERNAL_ERROR";
      return "UNEXPECTED_ERROR";
    }

    async function fetchEndpoint(key) {
      const endpoint = detailEndpoints[key];
      const headers = {};
      if (endpoint.etag) headers["If-None-Match"] = endpoint.etag;
      try {
        const response = await fetch(endpoint.url, {
          method: "GET",
          headers,
          cache: "no-store",
          credentials: "same-origin",
        });
        if (response.status === 304) return { kind: "not-modified" };
        if (response.status !== 200) {
          let code = null;
          try {
            const envelope = await response.json();
            code = envelope && envelope.error ? envelope.error.code : null;
          } catch (_error) {
            code = null;
          }
          return { kind: "error", state: mapFailure(response.status, code) };
        }
        const envelope = await response.json();
        return {
          kind: "success",
          data: envelope ? envelope.data : null,
          meta: envelope ? envelope.meta : null,
          etag: response.headers.get("ETag"),
        };
      } catch (_error) {
        return { kind: "error", state: "UNEXPECTED_ERROR" };
      }
    }

    function commitSuccess(key, result) {
      detailEndpoints[key].etag = result.etag;
      detailEndpoints[key].hasData = true;
    }

    function stopPolling() {
      if (pollTimer !== null) {
        window.clearTimeout(pollTimer);
        pollTimer = null;
      }
    }

    function shouldPoll() {
      return document.visibilityState === "visible" && lastWorkflowState !== null &&
        !TERMINAL_WORKFLOW_STATES.has(lastWorkflowState);
    }

    function schedulePolling() {
      stopPolling();
      if (shouldPoll()) {
        pollTimer = window.setTimeout(() => void loadDetail(), POLL_INTERVAL_MS);
      }
    }

    function clearUnestablishedSnapshot() {
      projectLink.hidden = true;
      summaryContent.replaceChildren();
      taskScopeContent.replaceChildren();
      blockerSection.hidden = true;
      blockerContent.replaceChildren();
      transitionList.replaceChildren();
      executionList.replaceChildren();
      evidenceMeta.replaceChildren();
      requirementSetList.replaceChildren();
      checkpointList.replaceChildren();
      requirementList.replaceChildren();
      candidateList.replaceChildren();
      admissionDecisionList.replaceChildren();
      admittedEvidenceList.replaceChildren();
      satisfactionList.replaceChildren();
      setEvaluationList.replaceChildren();
      setAttestationList.replaceChildren();
      humanJudgmentMeta.replaceChildren();
      humanGateContent.replaceChildren();
      humanResultContent.replaceChildren();
      judgmentContent.replaceChildren();
      transitionEffectContent.replaceChildren();
      transitionsState.textContent = "WorkRun 현재 상태를 확정할 수 없어 표시하지 않습니다.";
      executionState.textContent = "WorkRun 현재 상태를 확정할 수 없어 표시하지 않습니다.";
      evidenceState.textContent = "WorkRun 현재 상태를 확정할 수 없어 표시하지 않습니다.";
      humanJudgmentState.textContent =
        "WorkRun 현재 상태를 확정할 수 없어 표시하지 않습니다.";
    }

    function markRetainedDetailStale() {
      transitionsState.textContent = detailEndpoints.transitions.hasData
        ? "마지막 성공 전이 기록 유지 · 새로고침 실패로 보존된 과거 snapshot입니다."
        : "전이 기록 미확정 · WorkRun 현재 상태 새로고침 실패로 표시하지 않습니다.";
      executionState.textContent = detailEndpoints.execution.hasData
        ? "마지막 성공 실행 기록 유지 · 새로고침 실패로 보존된 과거 snapshot입니다."
        : "실행 기록 미확정 · WorkRun 현재 상태 새로고침 실패로 표시하지 않습니다.";
      evidenceState.textContent = detailEndpoints.evidence.hasData
        ? "마지막 성공 Evidence 상세 유지 · 새로고침 실패로 보존된 과거 snapshot입니다."
        : "Evidence 상세 미확정 · WorkRun 현재 상태 새로고침 실패로 표시하지 않습니다.";
      humanJudgmentState.textContent = detailEndpoints.humanJudgment.hasData
        ? "마지막 성공 Human/Judgment 상세 유지 · 새로고침 실패로 보존된 과거 snapshot입니다."
        : "Human/Judgment 상세 미확정 · WorkRun 현재 상태 새로고침 실패로 표시하지 않습니다.";
    }

    function applyTransitions(result) {
      if (result.kind === "not-modified" && detailEndpoints.transitions.hasData) {
        transitionsState.textContent = "변경 없음 · 기존 전이 기록 유지";
        return true;
      }
      if (result.kind !== "success") {
        transitionsState.textContent =
          "전이 기록 갱신 실패 · 마지막 성공 결과가 있으면 유지합니다.";
        return false;
      }
      try {
        renderTransitions(result.data);
        commitSuccess("transitions", result);
        transitionsState.textContent = "최신 전이 기록";
        return true;
      } catch (_error) {
        transitionsState.textContent = "전이 projection 형식을 확인할 수 없습니다.";
        return false;
      }
    }

    function applyExecution(result) {
      if (result.kind === "not-modified" && detailEndpoints.execution.hasData) {
        executionState.textContent = "변경 없음 · 기존 실행 기록 유지";
        return true;
      }
      if (result.kind !== "success") {
        executionState.textContent = "실행 기록 갱신 실패 · 마지막 성공 결과가 있으면 유지합니다.";
        return false;
      }
      try {
        renderExecution(result.data);
        commitSuccess("execution", result);
        executionState.textContent = "최신 실행 기록";
        return true;
      } catch (_error) {
        executionState.textContent = "실행 projection 형식을 확인할 수 없습니다.";
        return false;
      }
    }

    function applyEvidence(result) {
      if (result.kind === "not-modified" && detailEndpoints.evidence.hasData) {
        evidenceState.textContent = "변경 없음 · 현재 Evidence 상세 유지";
        return true;
      }
      if (result.kind !== "success") {
        evidenceState.textContent = detailEndpoints.evidence.hasData
          ? "마지막 성공 Evidence 상세 유지 · endpoint 새로고침 실패"
          : "Evidence 상세 사용 불가 · 성공한 snapshot 없음";
        return false;
      }
      try {
        renderEvidence(result.data, result.meta);
        commitSuccess("evidence", result);
        evidenceState.textContent = "현재 Evidence 상세";
        return true;
      } catch (_error) {
        evidenceState.textContent = "Evidence projection 형식을 확인할 수 없습니다.";
        return false;
      }
    }

    function applyHumanJudgment(result) {
      if (result.kind === "not-modified" && detailEndpoints.humanJudgment.hasData) {
        humanJudgmentState.textContent = "변경 없음 · 현재 Human/Judgment 상세 유지";
        return true;
      }
      if (result.kind !== "success") {
        humanJudgmentState.textContent = detailEndpoints.humanJudgment.hasData
          ? "마지막 성공 Human/Judgment 상세 유지 · endpoint 새로고침 실패"
          : "Human/Judgment 상세 사용 불가 · 성공한 snapshot 없음";
        return false;
      }
      try {
        renderHumanJudgment(result.data, result.meta);
        commitSuccess("humanJudgment", result);
        humanJudgmentState.textContent = "현재 Human/Judgment 상세";
        return true;
      } catch (_error) {
        humanJudgmentState.textContent =
          "Human/Judgment projection 형식을 확인할 수 없습니다.";
        return false;
      }
    }

    async function loadDetail() {
      if (requestInFlight) {
        refreshAfterFlight = true;
        return;
      }
      requestInFlight = true;
      stopPolling();
      if (!detailEndpoints.summary.hasData) setDetailState("LOADING");
      try {
        const [
          summaryResult,
          transitionsResult,
          executionResult,
          evidenceResult,
          humanJudgmentResult,
        ] = await Promise.all([
          fetchEndpoint("summary"),
          fetchEndpoint("transitions"),
          fetchEndpoint("execution"),
          fetchEndpoint("evidence"),
          fetchEndpoint("humanJudgment"),
        ]);

        let summaryCurrent = false;
        let summaryUnchanged = false;
        if (summaryResult.kind === "not-modified" && detailEndpoints.summary.hasData) {
          summaryCurrent = true;
          summaryUnchanged = true;
        } else if (summaryResult.kind === "success") {
          try {
            renderSummary(summaryResult.data, summaryResult.meta);
            commitSuccess("summary", summaryResult);
            summaryCurrent = true;
          } catch (_error) {
            setDetailState(
              "UNEXPECTED_ERROR",
              "WorkRun summary projection 형식을 확인할 수 없습니다.",
            );
          }
        } else {
          const state = summaryResult.state || "UNEXPECTED_ERROR";
          const suffix = detailEndpoints.summary.hasData
            ? " 마지막으로 성공한 snapshot을 유지하며 새 현재 상태로 표시하지 않습니다."
            : "";
          setDetailState(state, DETAIL_STATE_COPY[state][1] + suffix);
        }

        if (!summaryCurrent) {
          if (detailEndpoints.summary.hasData) {
            markRetainedDetailStale();
          } else {
            clearUnestablishedSnapshot();
          }
          return;
        }
        const transitionsReady = applyTransitions(transitionsResult);
        const executionReady = applyExecution(executionResult);
        const evidenceReady = applyEvidence(evidenceResult);
        const humanJudgmentReady = applyHumanJudgment(humanJudgmentResult);
        if (
          !transitionsReady || !executionReady || !evidenceReady || !humanJudgmentReady
        ) {
          setDetailState("PARTIAL_ERROR");
        } else {
          setDetailState(summaryUnchanged ? "UNCHANGED" : "READY");
        }
      } finally {
        requestInFlight = false;
        if (refreshAfterFlight && document.visibilityState === "visible") {
          refreshAfterFlight = false;
          void loadDetail();
        } else {
          refreshAfterFlight = false;
          schedulePolling();
        }
      }
    }

    refreshButton.addEventListener("click", () => void loadDetail());
    document.addEventListener("visibilitychange", () => {
      if (document.visibilityState === "hidden") {
        stopPolling();
        return;
      }
      if (lastWorkflowState !== null && !TERMINAL_WORKFLOW_STATES.has(lastWorkflowState)) {
        void loadDetail();
      }
    });
    void loadDetail();
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

  const outcomesFirst = document.getElementById("outcomes-first");
  const outcomesNext = document.getElementById("outcomes-next");
  const projectApi = "/v1/command-center/projects/" + encodeURIComponent(projectId);
  let outcomeCursor = "";
  let shownOutcomeCursor = "";
  let nextOutcomeCursor = null;

  function renderNextAction(data) {
    if (!data || data.project_id !== projectId) throw new Error("invalid project binding");
    const fragment = document.createDocumentFragment();
    fragment.append(
      readDefinition("프로젝트", [["Project ID", data.project_id]]),
      readDefinition("현재 projection (선택 실행 아님)", presenceFields(data.projection, [
        ["상태", "state"], ["사유", "reason"], ["Project revision", "project_revision"],
        ["event sequence", "latest_event_sequence"], ["갱신 시각", "updated_at"],
      ])),
      readDefinition("선택 기록 (Task 발행 아님)", presenceFields(data.selection, [
        ["selection_id", "selection_id"], ["selection_ref", "selection_ref"],
        ["행동 참조 (REFERENCE_ONLY)", "action_ref"],
        ["Project revision", "project_revision"], ["선택 시각", "selected_at"],
      ])),
      readDefinition("Task 발행 후보 (발행 완료 아님)", presenceFields(
        data.task_issuance_candidate, [
        ["candidate_id", "candidate_id"], ["발행 소유자", "issuance_owner"],
        ["발행 후 필요한 사람 입력", "required_post_issuance_human_input"],
        ["생성 시각", "created_at"],
        ],
      )),
    );
    return fragment;
  }

  function renderOutcomes(data) {
    if (!data || data.project_id !== projectId || !Array.isArray(data.items)) {
      throw new Error("invalid outcomes projection");
    }
    const fragment = document.createDocumentFragment();
    if (data.items.length === 0) {
      const empty = document.createElement("p");
      empty.className = "empty-state";
      empty.textContent = "이 페이지에 작업 결과 기록 없음";
      fragment.appendChild(empty);
    }
    data.items.forEach((item) => {
      if (item.project_id !== projectId || !item.workflow || !item.task_contract) {
        throw new Error("invalid outcome binding");
      }
      const card = document.createElement("article");
      card.className = "work-run-card";
      const heading = document.createElement("h3");
      heading.textContent = "작업 결과 · " + requireId(item.work_run_id);
      card.append(heading, readLink("work-runs", item.work_run_id, "WorkRun 상세"));
      card.appendChild(readDefinition("작업 / 워크플로", [
        ["TaskContract ID", item.task_contract.id], ["version", item.task_contract.version],
        ["WorkflowState", item.workflow.state], ["state_version", item.workflow.state_version],
      ]));
      card.appendChild(readDefinition("판정 (워크플로와 별개)", presenceFields(item.judgment, [
        ["Judgment ID", "judgment_id"], ["종류", "kind"], ["소유 정책", "owner_policy"],
      ])));
      const cycle = item.admitted_cycle;
      card.appendChild(readDefinition("입장된 Cycle 참조", presenceFields(cycle, [
        ["Cycle ID", "cycle_id"], ["참조", "cycle_ref"],
        ["입장 순번", "admission_sequence"], ["입장 시각", "admitted_at"],
      ])));
      if (cycle.presence === "PRESENT" &&
          typeof cycle.cycle_id === "string" && cycle.cycle_id.trim()) {
        card.appendChild(readLink("cycles", cycle.cycle_id, "Cycle 계보 보기"));
      }
      fragment.appendChild(card);
    });
    return fragment;
  }

  const nextActionSection = createReadSection(
    "next-action-content", "next-action-state", "NextAction", renderNextAction,
  );
  const outcomesSection = createReadSection(
    "outcomes-content", "outcomes-state", "작업 결과", renderOutcomes,
  );

  function retainProjectSections() {
    nextActionSection.retained("프로젝트 큐 현재 상태를 확인하지 못했습니다");
    outcomesSection.retained("프로젝트 큐 현재 상태를 확인하지 못했습니다");
  }

  function applyProjectSections(nextActionResult, outcomesResult, requestedCursor) {
    nextActionSection.apply(nextActionResult);
    if (outcomesSection.apply(outcomesResult) && outcomesResult.kind === "success") {
      shownOutcomeCursor = requestedCursor;
      nextOutcomeCursor = outcomesResult.meta && typeof outcomesResult.meta.next_cursor === "string"
        ? outcomesResult.meta.next_cursor : null;
    }
  }

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
      const detailLink = document.createElement("a");
      detailLink.className = "work-run-detail-link";
      detailLink.href = "/command-center/work-runs/" + encodeURIComponent(item.work_run_id);
      detailLink.textContent = "WorkRun 상세";
      card.appendChild(detailLink);

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
    outcomesFirst.disabled = true;
    outcomesNext.disabled = true;
    stopPolling();
    const request = buildQueueRequest();
    const requestedOutcomeCursor = outcomeCursor;
    const outcomesUrl = projectApi + "/outcomes?limit=25" + (requestedOutcomeCursor
      ? "&cursor=" + encodeURIComponent(requestedOutcomeCursor) : "");
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
      const [response, nextActionResult, outcomesResult] = await Promise.all([
        fetch(request.url, {
          method: "GET", headers, cache: "no-store", credentials: "same-origin",
        }).catch(() => null),
        nextActionSection.read(projectApi + "/next-action"),
        outcomesSection.read(outcomesUrl),
      ]);
      if (!response) {
        setReadState("UNEXPECTED_ERROR");
        retainProjectSections();
        return;
      }
      if (response.status === 304) {
        if (!lastSuccessfulEtag) {
          setReadState("UNEXPECTED_ERROR");
          retainProjectSections();
          return;
        }
        setReadState(
          renderedItemCount === 0 ? "EMPTY" : "READY",
          "큐가 변경되지 않았습니다.",
        );
        applyProjectSections(nextActionResult, outcomesResult, requestedOutcomeCursor);
        return;
      }
      if (response.status !== 200) {
        setReadState(mapFailure(response.status));
        retainProjectSections();
        return;
      }
      const envelope = await response.json();
      const items = envelope && envelope.data && envelope.data.project_id === projectId &&
        Array.isArray(envelope.data.items)
        ? envelope.data.items
        : null;
      if (items === null) {
        setReadState("UNEXPECTED_ERROR");
        retainProjectSections();
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
      applyProjectSections(nextActionResult, outcomesResult, requestedOutcomeCursor);
    } catch (_error) {
      setReadState("UNEXPECTED_ERROR");
      retainProjectSections();
    } finally {
      requestInFlight = false;
      outcomesFirst.disabled = !shownOutcomeCursor;
      outcomesNext.disabled = !nextOutcomeCursor;
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
  outcomesFirst.addEventListener("click", () => {
    outcomeCursor = "";
    void loadQueue();
  });
  outcomesNext.addEventListener("click", () => {
    if (!nextOutcomeCursor) return;
    outcomeCursor = nextOutcomeCursor;
    void loadQueue();
  });
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
