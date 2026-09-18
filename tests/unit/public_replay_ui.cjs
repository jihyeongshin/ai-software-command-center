// Offline DOM contract checks; not a browser/visual QA substitute.
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const assert = require("node:assert/strict");
const root = path.resolve(__dirname, "../..");
const script = fs.readFileSync(path.join(root, "public/replay/assets/app.js"), "utf8");
class Element {
  constructor(tag) { this.tag = tag; this.children = []; this.dataset = {}; this.attrs = {}; this.listeners = {}; this._text = ""; this.disabled = false; this.hidden = false; }
  set textContent(text) { this._text = String(text); this.children = []; }
  get textContent() { return this._text + this.children.map(c => c.textContent).join(" "); }
  append(...children) { this.children.push(...children); }
  replaceChildren(...children) { this._text = ""; this.children = children; }
  setAttribute(name, value) { this.attrs[name] = value; }
  removeAttribute(name) { delete this.attrs[name]; }
  addEventListener(name, fn) { this.listeners[name] = fn; }
  set innerHTML(_) { throw Error("Unsafe HTML insertion"); }
}
async function setup(fault = {}) {
  const ids = Object.fromEntries(["catalog", "catalog-status", "detail", "detail-status", "record", "live", "live-release-note", "live-status", "live-start", "live-stop", "live-result"].map(id => [id, new Element("div")]));
  const listeners = {}; const requests = [];
  const storage = new Map();
  const context = vm.createContext({
    document: { createElement: tag => new Element(tag), getElementById: id => ids[id], querySelectorAll: () => ids.catalog.children },
    location: {hash: ""}, window: {addEventListener: (name, fn) => { listeners[name] = fn; }},
    sessionStorage: {getItem:key => storage.get(key) ?? null, setItem:(key, value) => storage.set(key, String(value)), removeItem:key => storage.delete(key)},
    crypto: {getRandomValues: bytes => bytes.fill(7)},
    setTimeout: () => 1, clearTimeout: () => {}, URL,
    fetch: async (url, options) => {
      requests.push(url); assert.equal(options.method, "GET"); assert.equal(options.credentials, "omit"); assert.equal(options.redirect, "error");
      if (url === "live-config.json") return {ok:true, json:async () => ({schema:"AISCC-PUBLIC-LIVE-FRONTEND-CONFIG-V1", enabled:false, api_origin:null})};
      assert.match(url, /^data\/(REPLAY_CORPUS_INDEX|stockroom-s[1-4]-[a-z-]+)\.json$/);
      const name = url.slice(5);
      if (fault.missing === name) return {ok:false};
      return {ok:true, json:async () => {
        if (fault.malformed === name) throw new SyntaxError("bad JSON");
        const data = JSON.parse(fs.readFileSync(path.join(root, "public/replay", url), "utf8"));
        if (fault.injection && data.scenario) data.agent_claim_vs_system_admission.summary = '<img src=x onerror="alert(1)">';
        return data;
      }};
    }
  });
  await vm.runInContext(script, context);
  return {ids, requests, select:async id => { context.location.hash = id; await listeners.hashchange(); }};
}
(async () => {
  const app = await setup({injection:true}); assert.equal(app.ids.catalog.children.length, 4);
  const ids = ["stockroom-s1-normal", "stockroom-s2-missing-evidence", "stockroom-s3-policy-conflict", "stockroom-s4-human-owned-claim"];
  for (const id of ids) {
    await app.select("#scenario=" + id);
    assert.match(app.ids["detail-status"].textContent, /loaded/);
    assert.match(app.ids.record.textContent, /Not recorded in this public artifact/);
    assert.match(app.ids.record.textContent, /<img src=x/); // retained as text; no HTML parser exists
    assert.match(app.ids.record.textContent, /Evidence admission/);
  }
  const count = app.requests.length; await app.select("#scenario=../../owner");
  assert.match(app.ids["detail-status"].textContent, /Unknown scenario/); assert.equal(app.requests.length, count);
  await app.select("#scenario=%ZZ"); assert.match(app.ids["detail-status"].textContent, /Unknown scenario/);
  for (const fault of ["missing", "malformed"]) {
    const index = await setup({[fault]:"REPLAY_CORPUS_INDEX.json"}); assert.equal(index.ids["catalog-status"].className, "error");
    const scenario = await setup({[fault]:"stockroom-s1-normal.json"}); await scenario.select("#scenario=stockroom-s1-normal");
    assert.equal(scenario.ids["detail-status"].className, "error"); assert.equal(scenario.ids.record.children.length, 0);
  }
  console.log(JSON.stringify({result:"PASS", scenario_details:4, unknown_selector_no_fetch:true, index_missing_and_malformed:true, scenario_missing_and_malformed:true, safe_text_injection:true, scope:"Offline DOM contract; Human visual QA pending"}));
})().catch(error => { console.error(error); process.exitCode = 1; });
