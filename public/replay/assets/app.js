"use strict";

// Only these immutable same-origin Replay data files are ever fetched.
const SCENARIOS = Object.freeze({
  "stockroom-s1-normal": ["01", "Evidence admitted", "stockroom-s1-normal.json"],
  "stockroom-s2-missing-evidence": ["02", "Missing evidence", "stockroom-s2-missing-evidence.json"],
  "stockroom-s3-policy-conflict": ["03", "Policy conflict", "stockroom-s3-policy-conflict.json"],
  "stockroom-s4-human-owned-claim": ["04", "Human decision pending", "stockroom-s4-human-owned-claim.json"]
});
const ABSENT = "Not recorded in this public artifact";
const LIVE_SCENARIO_ID = "stockroom-s1-normal";
const LIVE_SCENARIO_VERSION = "1.0.0";
const LIVE_CONFIG_SCHEMA = "AISCC-PUBLIC-LIVE-FRONTEND-CONFIG-V1";
const LIVE_SESSION_SCHEMA = "AISCC-PUBLIC-LIVE-BROWSER-SESSION-V1";
const LIVE_SESSION_KEY = "aiscc.public-live.session.v1";
const LIVE_ROOT = "/v1/public-live/runs";
const LIVE_POLL_INTERVAL_MS = 3000;
const LIVE_MAX_POLLS = 40;
const TERMINAL_LIVE_STATES = new Set([
  "GOVERNANCE_PENDING", "UNKNOWN_OUTCOME", "COMPLETED", "FAILED_NOT_DISPATCHED",
  "FAILED_PROVIDER", "FAILED_TIMEOUT", "FAILED_SAFETY"
]);
let catalogIndex = null;
let selectionVersion = 0;
const liveRuntime = {
  config: null,
  session: null,
  pollTimer: null,
  expiryTimer: null,
  polls: 0,
  stopped: true
};

function node(tag, text, className) {
  const el = document.createElement(tag);
  if (text !== undefined) el.textContent = String(text);
  if (className) el.className = className;
  return el;
}
function value(v) { return v === null || v === undefined ? ABSENT : String(v); }
function raw(parent, label, data) {
  const detail = node("details");
  detail.append(node("summary", label), node("pre", JSON.stringify(data, null, 2)));
  parent.append(detail);
}
function fact(parent, label, data) {
  const dl = node("dl"); dl.append(node("dt", label), node("dd", value(data))); parent.append(dl);
}
function panel(title, summary, data) {
  const el = node("section", undefined, "panel");
  el.append(node("h3", title), node("p", summary));
  if (data !== undefined) raw(el, "Inspect recorded fields", data);
  return el;
}
function hasExactKeys(data, keys) {
  return data && typeof data === "object" && !Array.isArray(data) &&
    Object.keys(data).sort().join("\n") === [...keys].sort().join("\n");
}

async function readJSON(filename) {
  const allowed = ["REPLAY_CORPUS_INDEX.json", ...Object.values(SCENARIOS).map(v => v[2])];
  if (!allowed.includes(filename)) throw new Error("Unknown scenario selector.");
  let response;
  try { response = await fetch("data/" + filename, {method: "GET", credentials: "omit", redirect: "error", cache: "no-store"}); }
  catch { throw new Error(filename === "REPLAY_CORPUS_INDEX.json" ? "Corpus index unavailable." : "Selected scenario unavailable."); }
  if (!response.ok) throw new Error(filename === "REPLAY_CORPUS_INDEX.json" ? "Corpus index unavailable." : "Selected scenario missing.");
  try { return await response.json(); } catch { throw new Error("Malformed JSON in the recorded artifact."); }
}
function validateIndex(data) {
  if (!data || data.schema_id !== "AISCC-RECORDED-REPLAY-CORPUS-INDEX-V1" || data.live !== false ||
      !Array.isArray(data.members) || data.members.length !== 4 ||
      new Set(data.members.map(m => m.scenario_id)).size !== 4 ||
      data.members.some(m => !Object.hasOwn(SCENARIOS, m.scenario_id) || m.member_relative_path !== SCENARIOS[m.scenario_id][2])) {
    throw new Error("Malformed recorded catalog: expected the four accepted scenarios.");
  }
}
function renderCatalog(data) {
  const catalog = document.getElementById("catalog"); catalog.replaceChildren();
  for (const m of data.members) {
    const [number, title] = SCENARIOS[m.scenario_id];
    const card = node("article", undefined, "card");
    const link = node("a", title); link.href = "#scenario=" + encodeURIComponent(m.scenario_id);
    const heading = node("h3"); heading.append(link);
    card.dataset.scenario = m.scenario_id;
    card.append(node("span", number + " · " + value(m.final_state), "badge"), heading,
      node("p", m.scenario_id + " · v" + value(m.scenario_version)),
      node("p", "Recorded " + value(m.recorded_at)), node("p", "Recorded Run Replay · live=false"));
    raw(card, "Execution provenance", {execution_commit: m.execution_commit, source_run_fingerprint_sha256: m.source_run_fingerprint_sha256});
    catalog.append(card);
  }
}
function renderRecord(r, id) {
  const record = document.getElementById("record"); record.replaceChildren();
  const overview = node("section", undefined, "overview");
  overview.append(node("span", "Recorded outcome · " + value(r.final_workflow_state), "badge"),
    node("h3", SCENARIOS[id][1]), node("p", value(r.agent_claim_vs_system_admission?.summary)));
  const facts = node("div", undefined, "facts");
  for (const [label, v] of [["Scenario / version", id + " / " + value(r.scenario.version)], ["Recorded at", r.recorded_at],
    ["Execution source commit", r.orchestrator?.execution_commit], ["Replay identity", r.replay_id],
    ["Run fingerprint (not a WorkRun ID)", r.source_run_fingerprint_sha256], ["WorkRun identity", r.work_run_id],
    ["Synthetic repository", r.synthetic_repository?.name], ["Recorded state version", r.state_version]]) fact(facts, label, v);
  overview.append(facts); record.append(overview);
  const chain = node("div", undefined, "chain");
  chain.append(panel("1. Task & scope", ABSENT, r.task));
  const timeline = panel("2. State transitions", "System-admitted transitions as recorded; no transition is executed here.");
  const list = node("ol", undefined, "timeline");
  for (const t of r.transition_trace || []) {
    const li = node("li");
    li.append(node("strong", (t.source_state === null ? "Initial" : value(t.source_state)) + " → " + value(t.resulting_state)),
      node("small", value(t.outcome) + " · " + value(t.decided_at)));
    raw(li, "Guard and admission details", t); list.append(li);
  }
  timeline.append(list); chain.append(timeline);
  chain.append(panel("3. Execution", value(r.execution_summary?.attempt_status), r.execution_summary));
  chain.append(panel("4. Evidence admission", "Admitted: " + value(r.evidence_summary?.admitted_count) + "; rejected: " + value(r.evidence_summary?.rejected_count) + ". Raw evidence bodies are not included.", r.evidence_summary));
  chain.append(panel("5. Human-owned gate", value(r.human?.state) + " · recorded results: " + value(r.human?.result_count), r.human));
  chain.append(panel("6. Judgment", r.judgment?.kind ? value(r.judgment.kind) : "No Judgment recorded. This is not an implied acceptance.", r.judgment));
  chain.append(panel("7. Cycle / history", ABSENT, r.cycle));
  chain.append(panel("8. NextAction", ABSENT, r.next_action));
  chain.append(panel("Blocker", value(r.blocker?.presence), r.blocker));
  chain.append(panel("Claim ≠ admission", value(r.agent_claim_vs_system_admission?.summary), r.agent_claim_vs_system_admission));
  record.append(chain); raw(record, "Inspect the complete public recording", r);
}
async function selectScenario() {
  const version = ++selectionVersion;
  const status = document.getElementById("detail-status");
  document.getElementById("record").replaceChildren();
  document.getElementById("detail").setAttribute("aria-busy", "false");
  status.className = "";
  for (const card of document.querySelectorAll(".card")) card.removeAttribute("aria-current");
  if (!location.hash || location.hash === "#catalog-heading" || location.hash === "#main") { status.textContent = "Choose a scenario above."; return; }
  let id;
  try {
    if (!location.hash.startsWith("#scenario=")) throw new Error();
    id = decodeURIComponent(location.hash.slice(10));
    if (!Object.hasOwn(SCENARIOS, id)) throw new Error();
  } catch { status.textContent = "Unknown scenario selector. Choose one of the four recorded scenarios."; status.className = "error"; return; }
  if (!catalogIndex) { status.textContent = "Corpus index unavailable. No recording can be selected."; status.className = "error"; return; }
  status.textContent = "Loading historical recording…";
  document.getElementById("detail").setAttribute("aria-busy", "true");
  try {
    const r = await readJSON(SCENARIOS[id][2]);
    if (version !== selectionVersion) return;
    if (!r || r.schema_id !== "AISCC-RECORDED-RUN-REPLAY-V1" || r.scenario?.id !== id || r.live !== false || !Array.isArray(r.transition_trace)) throw new Error("Malformed or mismatched recorded scenario.");
    renderRecord(r, id); status.textContent = "Recorded Run Replay loaded. Viewing it does not execute AI.";
    for (const card of document.querySelectorAll(".card")) if (card.dataset.scenario === id) card.setAttribute("aria-current", "true");
  } catch (error) { if (version === selectionVersion) { status.textContent = error.message + " No execution was started."; status.className = "error"; } }
  finally { if (version === selectionVersion) document.getElementById("detail").setAttribute("aria-busy", "false"); }
}
async function initializeReplay() {
  const status = document.getElementById("catalog-status");
  try { const data = await readJSON("REPLAY_CORPUS_INDEX.json"); validateIndex(data); catalogIndex = data; renderCatalog(data); status.textContent = "Four historical scenarios. Titles describe the recorded outcomes."; }
  catch (error) { status.textContent = error.message + " No execution was started."; status.className = "error"; }
  await selectScenario();
}

function liveStatus(message, isError = false) {
  const status = document.getElementById("live-status");
  status.textContent = message;
  status.className = isError ? "error" : "";
}
function liveReleaseNote(message) {
  document.getElementById("live-release-note").textContent = message;
}
function liveButton(enabled, label) {
  const button = document.getElementById("live-start");
  button.disabled = !enabled;
  button.textContent = label;
}
function clearLiveResult() { document.getElementById("live-result").replaceChildren(); }
function stopPolling(message) {
  if (liveRuntime.pollTimer !== null) clearTimeout(liveRuntime.pollTimer);
  liveRuntime.pollTimer = null;
  liveRuntime.stopped = true;
  document.getElementById("live-stop").hidden = true;
  if (message) liveStatus(message);
}
function clearExpiryTimer() {
  if (liveRuntime.expiryTimer !== null) clearTimeout(liveRuntime.expiryTimer);
  liveRuntime.expiryTimer = null;
}
function removeLiveSession() {
  try { sessionStorage.removeItem(LIVE_SESSION_KEY); } catch {}
  liveRuntime.session = null;
}
function saveLiveSession(session) {
  sessionStorage.setItem(LIVE_SESSION_KEY, JSON.stringify(session));
  liveRuntime.session = session;
}
function validIdempotencyKey(input) { return typeof input === "string" && /^[0-9a-f]{32}$/.test(input); }
function validRunId(input) { return typeof input === "string" && /^[A-Za-z0-9_-]{22}$/.test(input); }
function validCapability(input) { return typeof input === "string" && /^[A-Za-z0-9_-]{43}$/.test(input); }
function validTimestamp(input) { return typeof input === "string" && /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$/.test(input) && Number.isFinite(Date.parse(input)); }
function validBaseSession(session) {
  return session && session.schema === LIVE_SESSION_SCHEMA &&
    session.api_origin === liveRuntime.config.apiOrigin &&
    session.scenario_id === LIVE_SCENARIO_ID && session.scenario_version === LIVE_SCENARIO_VERSION;
}
function loadLiveSession() {
  let parsed;
  try {
    const stored = sessionStorage.getItem(LIVE_SESSION_KEY);
    if (!stored) return null;
    parsed = JSON.parse(stored);
  } catch { removeLiveSession(); return null; }
  if (!validBaseSession(parsed) || !["admission_pending", "active", "capability_unavailable", "closed"].includes(parsed.phase)) {
    removeLiveSession(); return null;
  }
  if (parsed.phase === "admission_pending" && !validIdempotencyKey(parsed.idempotency_key)) {
    removeLiveSession(); return null;
  }
  if (parsed.phase === "active" && (!validRunId(parsed.run_id) || !validCapability(parsed.read_capability) || !validTimestamp(parsed.read_expires_at))) {
    removeLiveSession(); return null;
  }
  if (parsed.phase === "capability_unavailable" && !validRunId(parsed.run_id)) {
    removeLiveSession(); return null;
  }
  return parsed;
}
function expireLiveSession() {
  stopPolling();
  clearExpiryTimer();
  removeLiveSession();
  clearLiveResult();
  liveButton(true, "Start bounded Live");
  liveStatus("The same-tab read capability expired and was discarded. No replacement run was started.");
}
function scheduleExpiry(session) {
  clearExpiryTimer();
  const remaining = Date.parse(session.read_expires_at) - Date.now();
  if (remaining <= 0) { expireLiveSession(); return false; }
  liveRuntime.expiryTimer = setTimeout(expireLiveSession, remaining);
  return true;
}
function storageAvailable() {
  const probe = LIVE_SESSION_KEY + ".probe";
  try { sessionStorage.setItem(probe, "1"); sessionStorage.removeItem(probe); return true; }
  catch { return false; }
}
function randomIdempotencyKey() {
  const bytes = new Uint8Array(16);
  crypto.getRandomValues(bytes);
  return Array.from(bytes, byte => byte.toString(16).padStart(2, "0")).join("");
}
function newPendingSession() {
  return {
    schema: LIVE_SESSION_SCHEMA,
    phase: "admission_pending",
    api_origin: liveRuntime.config.apiOrigin,
    scenario_id: LIVE_SCENARIO_ID,
    scenario_version: LIVE_SCENARIO_VERSION,
    idempotency_key: randomIdempotencyKey()
  };
}
function validateLiveConfig(data) {
  if (!hasExactKeys(data, ["schema", "enabled", "api_origin"]) || data.schema !== LIVE_CONFIG_SCHEMA || typeof data.enabled !== "boolean") return null;
  if (!data.enabled) return data.api_origin === null ? Object.freeze({enabled: false, apiOrigin: null}) : null;
  if (typeof data.api_origin !== "string") return null;
  let parsed;
  try { parsed = new URL(data.api_origin); } catch { return null; }
  if (parsed.protocol !== "https:" || parsed.origin !== data.api_origin || parsed.pathname !== "/" || parsed.search || parsed.hash || parsed.username || parsed.password) return null;
  return Object.freeze({enabled: true, apiOrigin: parsed.origin});
}
async function readLiveConfig() {
  let response;
  try { response = await fetch("live-config.json", {method: "GET", credentials: "omit", redirect: "error", cache: "no-store"}); }
  catch { return null; }
  if (!response.ok) return null;
  try { return validateLiveConfig(await response.json()); } catch { return null; }
}
function validateReceipt201(data) {
  return hasExactKeys(data, ["run_id", "state", "read_capability", "read_expires_at", "replayed"]) &&
    validRunId(data.run_id) && data.state === "ADMITTED" && validCapability(data.read_capability) &&
    validTimestamp(data.read_expires_at) && Date.parse(data.read_expires_at) > Date.now() && data.replayed === false;
}
function validateReceipt202(data) {
  return hasExactKeys(data, ["run_id", "replayed"]) && validRunId(data.run_id) && data.replayed === true;
}
function validBoundedText(value, maximum) {
  return typeof value === "string" && value.length > 0 && value.length <= maximum;
}
function validateStockroom(data) {
  if (!hasExactKeys(data, ["items", "total_available"]) || data.total_available !== 13 ||
      !Array.isArray(data.items) || data.items.length !== 3) return false;
  const expected = [["BOX-A", 12, 2, 10, false], ["BOX-B", 5, 5, 0, true], ["BOX-C", 4, 1, 3, true]];
  return data.items.every((item, index) => hasExactKeys(item,
    ["sku", "on_hand", "reserved", "available", "needs_reorder"]) &&
    [item.sku, item.on_hand, item.reserved, item.available, item.needs_reorder]
      .every((value, field) => value === expected[index][field]));
}
function validateTraceStep(step, index) {
  if (!step || step.ordinal !== index + 2 || !["PROVIDER", "TOOL", "EXECUTION", "PUBLIC_PROJECTION"].includes(step.kind)) return false;
  if (step.kind === "PROVIDER") return hasExactKeys(step,
    ["ordinal", "kind", "role", "status", "action", "tool_name", "retry"]) &&
    ["PRIMARY", "VERIFY", "CORRECT"].includes(step.role) &&
    ["COMPLETED", "IN_PROGRESS", "DEFINITELY_NOT_SENT", "OUTCOME_UNKNOWN"].includes(step.status) &&
    ["APPROVED_TOOL_REQUESTED", "BOUNDED_SUMMARY_PRODUCED", "PROVIDER_STEP_RECORDED", "DEFINITELY_NOT_SENT", "OUTCOME_UNKNOWN"].includes(step.action) &&
    (step.tool_name === null || step.tool_name === "stockroom_summary") && typeof step.retry === "boolean";
  if (step.kind === "TOOL") return hasExactKeys(step, ["ordinal", "kind", "tool_name", "status"]) &&
    step.tool_name === "stockroom_summary" && ["COMPLETED", "IN_PROGRESS", "OUTCOME_UNKNOWN"].includes(step.status);
  if (step.kind === "EXECUTION") return hasExactKeys(step, ["ordinal", "kind", "status"]) &&
    ["NOT_STARTED", "RUNNING", "EXECUTOR_COMPLETED", "EXECUTION_FAILED"].includes(step.status);
  return hasExactKeys(step, ["ordinal", "kind", "state", "reservation", "slot", "outbox", "work"]) &&
    validBoundedText(step.state, 64) && ["HELD", "SETTLED", "INCIDENT"].includes(step.reservation) &&
    ["FREE", "OCCUPIED", "SUSPECT"].includes(step.slot) && ["PENDING", "BOUND", "CLOSED"].includes(step.outbox) &&
    validBoundedText(step.work, 64);
}
function validateInspectableResult(result) {
  return hasExactKeys(result, ["schema", "workflow_state", "evidence_status", "summary_text", "instruction", "trace", "stockroom", "human_boundary"]) &&
    result.schema === "AISCC-PUBLIC-LIVE-INSPECTABLE-RESULT-V1" &&
    ["NOT_STARTED", "RUNNING", "EXECUTOR_COMPLETED", "EXECUTION_FAILED"].includes(result.workflow_state) &&
    result.evidence_status === "ADMITTED" && validBoundedText(result.summary_text, 4000) &&
    hasExactKeys(result.instruction, ["authority", "text"]) && result.instruction.authority === "SERVER_OWNED" &&
    result.instruction.text === "Produce the bounded Stockroom summary." && Array.isArray(result.trace) &&
    result.trace.length >= 2 && result.trace.length <= 8 && result.trace.every(validateTraceStep) &&
    (result.stockroom === null || validateStockroom(result.stockroom)) &&
    hasExactKeys(result.human_boundary, ["state", "statement"]) && result.human_boundary.state === "NOT_PERFORMED" &&
    result.human_boundary.statement === "Successful AI execution does not become Human acceptance automatically.";
}
function validateProjection(data, runId) {
  if (!hasExactKeys(data, ["run_id", "state", "reason_code", "admitted_at", "updated_at", "deadline_at", "mode", "scenario_id", "scenario_version", "result"]) ||
      data.run_id !== runId || typeof data.state !== "string" || data.state.length > 64 ||
      (data.reason_code !== null && (typeof data.reason_code !== "string" || data.reason_code.length > 64)) ||
      !validTimestamp(data.admitted_at) || !validTimestamp(data.updated_at) || !validTimestamp(data.deadline_at) ||
      data.mode !== "PUBLIC_BOUNDED_LIVE" || data.scenario_id !== LIVE_SCENARIO_ID || data.scenario_version !== LIVE_SCENARIO_VERSION) return false;
  if (data.result === null) return true;
  return validateInspectableResult(data.result);
}
function traceCard(step) {
  const card = node("article", undefined, "trace-card");
  card.append(node("span", String(step.ordinal).padStart(2, "0") + " · " + step.kind, "trace-step"));
  if (step.kind === "PROVIDER") {
    card.append(node("h5", step.role + (step.retry ? " · RETRY" : "")), node("p", step.action.replaceAll("_", " ")));
    if (step.tool_name) card.append(node("p", "Approved tool: " + step.tool_name));
  } else if (step.kind === "TOOL") {
    card.append(node("h5", step.tool_name));
  } else if (step.kind === "EXECUTION") card.append(node("h5", step.status));
  else card.append(node("h5", step.state), node("p", "Reservation " + step.reservation + " · Slot " + step.slot + " · Outbox " + step.outbox + " · Work " + step.work));
  if (step.kind !== "EXECUTION" && step.kind !== "PUBLIC_PROJECTION") card.append(node("span", step.status, "trace-status"));
  return card;
}
function stockroomTable(stockroom) {
  const table = node("table", undefined, "stockroom-table");
  const head = node("tr"); ["SKU", "On hand", "Reserved", "Available", "Reorder"].forEach(label => head.append(node("th", label)));
  const thead = node("thead"); thead.append(head); const tbody = node("tbody");
  for (const item of stockroom.items) { const row = node("tr");
    [item.sku, item.on_hand, item.reserved, item.available, item.needs_reorder ? "Yes" : "No"].forEach(value => row.append(node("td", value))); tbody.append(row); }
  table.append(thead, tbody); return table;
}
function renderLiveProjection(data) {
  const result = document.getElementById("live-result"); result.replaceChildren(); result.className = "live-result";
  result.append(node("h4", "Server status"));
  for (const [label, content] of [["Run", data.run_id], ["Run state", data.state], ["Reason", data.reason_code],
    ["Admitted at", data.admitted_at], ["Updated at", data.updated_at], ["Deadline", data.deadline_at],
    ["Mode", data.mode], ["Scenario / version", data.scenario_id + " / " + data.scenario_version]]) fact(result, label, content);
  if (data.result !== null) {
    result.append(node("h4", "Live execution trace"), node("p", data.result.summary_text));
    const trace = node("div", undefined, "trace-list");
    const instruction = node("article", undefined, "trace-card");
    instruction.append(node("span", "01 · INSTRUCTION", "trace-step"), node("h5", data.result.instruction.text), node("span", "COMPLETED · " + data.result.instruction.authority, "trace-status"));
    trace.append(instruction);
    for (const step of data.result.trace) { const card = traceCard(step);
      if (step.kind === "TOOL" && data.result.stockroom !== null) card.append(stockroomTable(data.result.stockroom)); trace.append(card); }
    result.append(trace);
    const boundary = node("section", undefined, "human-boundary");
    boundary.append(node("strong", "Human decision · " + data.result.human_boundary.state), node("p", data.result.human_boundary.statement));
    result.append(boundary);
  } else {
    result.append(node("p", "Waiting for durable execution evidence."));
  }
}
async function safeResponseJSON(response) {
  try { return await response.json(); } catch { return null; }
}
function scheduleNextPoll() {
  if (!liveRuntime.stopped) liveRuntime.pollTimer = setTimeout(pollLive, LIVE_POLL_INTERVAL_MS);
}
async function pollLive() {
  liveRuntime.pollTimer = null;
  const session = liveRuntime.session;
  if (!session || session.phase !== "active" || liveRuntime.stopped) return;
  if (Date.parse(session.read_expires_at) <= Date.now()) { expireLiveSession(); return; }
  if (liveRuntime.polls >= LIVE_MAX_POLLS) {
    stopPolling("Automatic status updates paused after the bounded polling window. Refresh this tab to resume while the capability remains valid.");
    return;
  }
  liveRuntime.polls += 1;
  let response;
  document.getElementById("live").setAttribute("aria-busy", "true");
  try {
    response = await fetch(liveRuntime.config.apiOrigin + LIVE_ROOT + "/" + session.run_id, {
      method: "GET",
      headers: {"X-Run-Read-Capability": session.read_capability},
      credentials: "omit",
      redirect: "error",
      cache: "no-store"
    });
  } catch {
    stopPolling("Live status is unavailable. The Recorded Replay remains usable.");
    document.getElementById("live").setAttribute("aria-busy", "false");
    return;
  }
  const data = await safeResponseJSON(response);
  document.getElementById("live").setAttribute("aria-busy", "false");
  if (!response.ok || !validateProjection(data, session.run_id)) {
    if (response.status === 404) { clearExpiryTimer(); removeLiveSession(); }
    stopPolling("Live status is unavailable or no longer readable. The Recorded Replay remains usable.");
    return;
  }
  renderLiveProjection(data);
  liveStatus("Live status loaded from the bounded public projection. This is not a Human acceptance decision.");
  if (TERMINAL_LIVE_STATES.has(data.state)) {
    stopPolling("Live reached server state " + data.state + ". Automatic status updates stopped. This is not a Human acceptance decision.");
    return;
  }
  scheduleNextPoll();
}
async function resumeActiveSession(session) {
  if (!scheduleExpiry(session)) return;
  liveRuntime.session = session;
  liveRuntime.polls = 0;
  liveRuntime.stopped = false;
  liveButton(false, "Live session active");
  document.getElementById("live-stop").hidden = false;
  liveStatus("Resuming this tab's bounded Live status with its session-only read capability.");
  await pollLive();
}
function uncertainAdmission(session, message) {
  saveLiveSession(session);
  liveButton(true, "Retry same admission request");
  liveStatus(message + " A retry will reuse this tab's same idempotency key; no replacement run was created.", true);
}
async function startLive() {
  if (!liveRuntime.config?.enabled) return;
  let session = liveRuntime.session;
  if (!session) {
    session = newPendingSession();
    try { saveLiveSession(session); }
    catch { liveButton(false, "Live unavailable"); liveStatus("Same-tab session storage is unavailable. Live remains disabled; Replay remains usable.", true); return; }
  }
  if (session.phase !== "admission_pending") return;
  liveButton(false, "Submitting bounded request…");
  liveStatus("Submitting the fixed stockroom-s1-normal / 1.0.0 request.");
  let response;
  try {
    response = await fetch(liveRuntime.config.apiOrigin + LIVE_ROOT, {
      method: "POST",
      headers: {"Content-Type": "application/json", "Idempotency-Key": session.idempotency_key},
      body: JSON.stringify({scenario_id: LIVE_SCENARIO_ID, scenario_version: LIVE_SCENARIO_VERSION}),
      credentials: "omit",
      redirect: "error",
      cache: "no-store"
    });
  } catch {
    uncertainAdmission(session, "The admission response was not received.");
    return;
  }
  const data = await safeResponseJSON(response);
  if (response.status === 201 && validateReceipt201(data)) {
    const active = {
      schema: LIVE_SESSION_SCHEMA, phase: "active", api_origin: liveRuntime.config.apiOrigin,
      scenario_id: LIVE_SCENARIO_ID, scenario_version: LIVE_SCENARIO_VERSION,
      run_id: data.run_id, read_capability: data.read_capability, read_expires_at: data.read_expires_at
    };
    try { saveLiveSession(active); }
    catch { liveButton(false, "Live unavailable"); liveStatus("The read capability could not be kept in same-tab session storage. Status recovery is unavailable.", true); return; }
    await resumeActiveSession(active);
    return;
  }
  if (response.status === 202 && validateReceipt202(data)) {
    const unavailable = {
      schema: LIVE_SESSION_SCHEMA, phase: "capability_unavailable", api_origin: liveRuntime.config.apiOrigin,
      scenario_id: LIVE_SCENARIO_ID, scenario_version: LIVE_SCENARIO_VERSION, run_id: data.run_id
    };
    saveLiveSession(unavailable);
    liveButton(false, "Capability unavailable");
    liveStatus("The server confirmed a prior admission, but this tab never received its one-time read capability. Status recovery is unavailable and no replacement run was created.", true);
    return;
  }
  const retryable = data?.error?.retryable === true && (response.status === 429 || response.status === 503);
  if (response.status === 500 || retryable) {
    uncertainAdmission(session, "The admission outcome is uncertain.");
    return;
  }
  const closed = {
    schema: LIVE_SESSION_SCHEMA, phase: "closed", api_origin: liveRuntime.config.apiOrigin,
    scenario_id: LIVE_SCENARIO_ID, scenario_version: LIVE_SCENARIO_VERSION,
    error_code: typeof data?.error?.code === "string" ? data.error.code.slice(0, 64) : "SAFE_ERROR"
  };
  saveLiveSession(closed);
  liveButton(false, "Live unavailable");
  liveStatus("Live admission was denied or unavailable. No replacement run was started; the Recorded Replay remains usable.", true);
}
async function initializeLive() {
  const config = await readLiveConfig();
  if (!config || !config.enabled) {
    removeLiveSession();
    liveRuntime.config = config;
    if (config) {
      liveReleaseNote("Live is not enabled in this release. Recorded Run Replay remains available.");
      liveButton(false, "Live is not enabled");
      liveStatus("Live is not enabled in this release. Recorded Run Replay remains available.");
    } else {
      liveReleaseNote("Live is unavailable because release configuration is missing or invalid. Recorded Run Replay remains available.");
      liveButton(false, "Live unavailable");
      liveStatus("Live configuration is missing or invalid, so Live failed closed. Recorded Run Replay remains available.");
    }
    return;
  }
  liveRuntime.config = config;
  liveReleaseNote("Bounded Live is configured for this release. Recorded Run Replay remains available.");
  if (!storageAvailable()) {
    liveReleaseNote("Bounded Live is configured, but unavailable in this browser session. Recorded Run Replay remains available.");
    liveButton(false, "Live unavailable");
    liveStatus("Same-tab session storage is unavailable. Live remains disabled; Replay remains usable.", true);
    return;
  }
  const session = loadLiveSession();
  liveRuntime.session = session;
  if (!session) {
    liveButton(true, "Start bounded Live");
    liveStatus("Live is configured for one fixed scenario. Starting creates one bounded public run.");
  } else if (session.phase === "admission_pending") {
    liveButton(true, "Retry same admission request");
    liveStatus("A prior admission response was uncertain. Retry will reuse this tab's same idempotency key.");
  } else if (session.phase === "active") {
    await resumeActiveSession(session);
  } else if (session.phase === "capability_unavailable") {
    liveButton(false, "Capability unavailable");
    liveStatus("A prior run exists, but this tab has no read capability. Status recovery is unavailable and no replacement run was created.", true);
  } else {
    liveButton(false, "Live unavailable");
    liveStatus("This tab's Live attempt is closed. No replacement run was started; Replay remains usable.", true);
  }
}

window.addEventListener("hashchange", selectScenario);
window.addEventListener("pagehide", () => stopPolling());
document.getElementById("live-start").addEventListener("click", startLive);
document.getElementById("live-stop").addEventListener("click", () => stopPolling("Automatic status updates stopped locally. Refresh this tab to resume while the capability remains valid."));
Promise.all([initializeReplay(), initializeLive()]);
