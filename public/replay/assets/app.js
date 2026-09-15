"use strict";

// Only these immutable same-origin data files are ever fetched.
const SCENARIOS = Object.freeze({
  "stockroom-s1-normal": ["01", "Evidence admitted", "stockroom-s1-normal.json"],
  "stockroom-s2-missing-evidence": ["02", "Missing evidence", "stockroom-s2-missing-evidence.json"],
  "stockroom-s3-policy-conflict": ["03", "Policy conflict", "stockroom-s3-policy-conflict.json"],
  "stockroom-s4-human-owned-claim": ["04", "Human decision pending", "stockroom-s4-human-owned-claim.json"]
});
const ABSENT = "Not recorded in this public artifact";
let catalogIndex = null;
let selectionVersion = 0;

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
async function initialize() {
  const status = document.getElementById("catalog-status");
  try { const data = await readJSON("REPLAY_CORPUS_INDEX.json"); validateIndex(data); catalogIndex = data; renderCatalog(data); status.textContent = "Four historical scenarios. Titles describe the recorded outcomes."; }
  catch (error) { status.textContent = error.message + " No execution was started."; status.className = "error"; }
  await selectScenario();
}
window.addEventListener("hashchange", selectScenario);
initialize();
