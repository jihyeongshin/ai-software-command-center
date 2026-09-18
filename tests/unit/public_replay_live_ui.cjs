// Offline DOM/session contract checks; Human browser/visual QA remains pending.
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const assert = require("node:assert/strict");

const root = path.resolve(__dirname, "../..");
const script = fs.readFileSync(path.join(root, "public/replay/assets/app.js"), "utf8");
const apiOrigin = "https://live.synthetic.invalid";
const runId = "A".repeat(22);
const capability = "B".repeat(43);
const sessionKey = "aiscc.public-live.session.v1";
const enabledConfig = {schema:"AISCC-PUBLIC-LIVE-FRONTEND-CONFIG-V1", enabled:true, api_origin:apiOrigin};
const disabledConfig = {schema:"AISCC-PUBLIC-LIVE-FRONTEND-CONFIG-V1", enabled:false, api_origin:null};

class Element {
  constructor(tag) {
    this.tag = tag; this.children = []; this.dataset = {}; this.attrs = {}; this.listeners = {};
    this._text = ""; this.disabled = false; this.hidden = false; this.className = "";
  }
  set textContent(text) { this._text = String(text); this.children = []; }
  get textContent() { return this._text + this.children.map(child => child.textContent).join(" "); }
  append(...children) { this.children.push(...children); }
  replaceChildren(...children) { this._text = ""; this.children = children; }
  setAttribute(name, value) { this.attrs[name] = value; }
  removeAttribute(name) { delete this.attrs[name]; }
  addEventListener(name, fn) { this.listeners[name] = fn; }
  set innerHTML(_) { throw Error("Unsafe HTML insertion"); }
}

function response(status, data) {
  return {status, ok:status >= 200 && status < 300, json:async () => data};
}
function projection(state = "ADMITTED", result = null) {
  return {
    run_id:runId, state, reason_code:null,
    admitted_at:"2026-09-18T00:00:00Z", updated_at:"2026-09-18T00:00:01Z",
    deadline_at:"2026-09-18T00:01:30Z", mode:"PUBLIC_BOUNDED_LIVE",
    scenario_id:"stockroom-s1-normal", scenario_version:"1.0.0", result
  };
}
function storageObject(map) {
  return {
    getItem:key => map.get(key) ?? null,
    setItem:(key, value) => map.set(key, String(value)),
    removeItem:key => map.delete(key)
  };
}

async function setup({config = enabledConfig, apiHandler = async () => { throw Error("unexpected API request"); }, storage = new Map()} = {}) {
  const ids = Object.fromEntries([
    "catalog", "catalog-status", "detail", "detail-status", "record",
    "live", "live-status", "live-start", "live-stop", "live-result"
  ].map(id => [id, new Element(id === "live-start" || id === "live-stop" ? "button" : "div")]));
  const windowListeners = {}; const calls = []; const logs = []; const timers = new Map();
  let timerSequence = 0; let localStorageTouches = 0;
  const location = {hash:"", href:"https://aiscc-replay.pages.dev/"};
  const document = {
    cookie:"harmless=1",
    createElement:tag => new Element(tag),
    getElementById:id => ids[id],
    querySelectorAll:selector => selector === ".card" ? ids.catalog.children : []
  };
  const context = vm.createContext({
    document, location, URL, Uint8Array,
    window:{addEventListener:(name, fn) => { windowListeners[name] = fn; }},
    sessionStorage:storageObject(storage),
    localStorage:{
      getItem:() => { localStorageTouches += 1; throw Error("localStorage forbidden"); },
      setItem:() => { localStorageTouches += 1; throw Error("localStorage forbidden"); }
    },
    crypto:{getRandomValues:bytes => { for (let i = 0; i < bytes.length; i += 1) bytes[i] = i; return bytes; }},
    console:{log:value => logs.push(String(value)), error:value => logs.push(String(value))},
    setTimeout:(fn, delay) => { const id = ++timerSequence; timers.set(id, {fn, delay}); return id; },
    clearTimeout:id => timers.delete(id),
    fetch:async (url, options) => {
      calls.push({url, options});
      if (url === "live-config.json") return response(200, config);
      if (url.startsWith("data/")) {
        const data = JSON.parse(fs.readFileSync(path.join(root, "public/replay", url), "utf8"));
        return response(200, data);
      }
      return apiHandler(url, options, calls);
    }
  });
  await vm.runInContext(script, context);
  return {
    ids, calls, logs, storage, location, document, timers,
    localStorageTouches:() => localStorageTouches,
    clickStart:async () => ids["live-start"].listeners.click(),
    select:async id => { location.hash = id; await windowListeners.hashchange(); },
    runPollTimer:async () => {
      const entry = [...timers.entries()].find(([, timer]) => timer.delay === 3000);
      if (!entry) return false;
      timers.delete(entry[0]); await entry[1].fn(); return true;
    }
  };
}

(async () => {
  // Default/disabled is inert while Replay stays independently usable.
  const disabled = await setup({config:disabledConfig});
  assert.equal(disabled.ids["live-start"].disabled, true);
  assert.match(disabled.ids["live-status"].textContent, /not enabled/);
  assert.equal(disabled.calls.some(call => call.url.startsWith(apiOrigin)), false);
  await disabled.select("#scenario=stockroom-s1-normal");
  assert.match(disabled.ids["detail-status"].textContent, /loaded/);
  const invalidConfig = await setup({config:{schema:"AISCC-PUBLIC-LIVE-FRONTEND-CONFIG-V1", enabled:true, api_origin:"https://invalid.example/path"}});
  assert.equal(invalidConfig.ids["live-start"].disabled, true);
  assert.match(invalidConfig.ids["live-status"].textContent, /failed closed/);
  assert.equal(invalidConfig.calls.some(call => call.url.startsWith("https://invalid.example")), false);

  // Exact POST, 201 sessionStorage, exact GET capability header and safe rendering.
  const sharedStorage = new Map();
  const active = await setup({storage:sharedStorage, apiHandler:async (url, options) => {
    if (options.method === "POST") return response(201, {
      run_id:runId, state:"ADMITTED", read_capability:capability,
      read_expires_at:"2099-09-19T00:00:00Z", replayed:false
    });
    return response(200, projection());
  }});
  await active.clickStart();
  const post = active.calls.find(call => call.options.method === "POST");
  assert.equal(post.url, apiOrigin + "/v1/public-live/runs");
  assert.equal(post.options.body, '{"scenario_id":"stockroom-s1-normal","scenario_version":"1.0.0"}');
  assert.equal(post.options.headers["Content-Type"], "application/json");
  assert.match(post.options.headers["Idempotency-Key"], /^[0-9a-f]{32}$/);
  assert.equal(post.options.credentials, "omit");
  const get = active.calls.find(call => call.options.method === "GET" && call.url.startsWith(apiOrigin));
  assert.equal(get.url, apiOrigin + "/v1/public-live/runs/" + runId);
  assert.equal(get.options.headers["X-Run-Read-Capability"], capability);
  assert.equal(get.options.credentials, "omit");
  const stored = JSON.parse(sharedStorage.get(sessionKey));
  assert.equal(stored.phase, "active"); assert.equal(stored.read_capability, capability);
  assert.equal(stored.idempotency_key, undefined); // no longer needed after confirmed 201
  const allRendered = Object.values(active.ids).map(element => element.textContent).join(" ");
  assert.equal(allRendered.includes(capability), false);
  assert.equal(active.location.href.includes(capability) || active.location.hash.includes(capability), false);
  assert.equal(active.document.cookie.includes(capability), false);
  assert.equal(active.logs.join(" ").includes(capability), false);
  assert.equal(active.localStorageTouches(), 0);

  // Same-tab reload resumes GET; an independent session has no recovery.
  const resumed = await setup({storage:sharedStorage, apiHandler:async (_url, options) => {
    assert.equal(options.method, "GET"); return response(200, projection());
  }});
  assert.equal(resumed.calls.filter(call => call.url.startsWith(apiOrigin) && call.options.method === "GET").length, 1);
  const independent = await setup({storage:new Map(), apiHandler:async () => { throw Error("independent tab must not call API"); }});
  assert.equal(independent.calls.some(call => call.url.startsWith(apiOrigin)), false);
  assert.equal(independent.ids["live-start"].disabled, false);

  // 202 never fabricates/reissues capability or starts a replacement run.
  let replayPosts = 0;
  const replayed = await setup({apiHandler:async (_url, options) => {
    assert.equal(options.method, "POST"); replayPosts += 1;
    return response(202, {run_id:runId, replayed:true});
  }});
  await replayed.clickStart();
  assert.equal(replayPosts, 1);
  assert.match(replayed.ids["live-status"].textContent, /Status recovery is unavailable/);
  assert.equal(JSON.parse(replayed.storage.get(sessionKey)).read_capability, undefined);
  assert.equal(replayed.ids["live-start"].disabled, true);

  // Uncertain response permits only an explicit retry with the same key.
  const uncertainKeys = [];
  const uncertain = await setup({apiHandler:async (_url, options) => {
    uncertainKeys.push(options.headers["Idempotency-Key"]);
    return uncertainKeys.length === 1
      ? response(503, {error:{code:"COMMIT_OUTCOME_UNKNOWN", retryable:true}})
      : response(202, {run_id:runId, replayed:true});
  }});
  await uncertain.clickStart();
  assert.equal(uncertain.ids["live-start"].disabled, false);
  await uncertain.clickStart();
  assert.deepEqual(uncertainKeys, [uncertainKeys[0], uncertainKeys[0]]);
  assert.equal(uncertain.calls.filter(call => call.options.method === "POST").length, 2);

  // A safe API denial is visible and does not impair Replay.
  const denied = await setup({apiHandler:async () => response(503, {error:{code:"LIVE_DISABLED", retryable:false}})});
  await denied.clickStart();
  assert.match(denied.ids["live-status"].textContent, /denied or unavailable/);
  await denied.select("#scenario=stockroom-s2-missing-evidence");
  assert.match(denied.ids["detail-status"].textContent, /loaded/);

  // Polling is 20/minute and capped at 40 reads; no fresh run is created.
  let boundedGets = 0; let boundedPosts = 0;
  const bounded = await setup({apiHandler:async (_url, options) => {
    if (options.method === "POST") {
      boundedPosts += 1;
      return response(201, {run_id:runId, state:"ADMITTED", read_capability:capability, read_expires_at:"2099-09-19T00:00:00Z", replayed:false});
    }
    boundedGets += 1; return response(200, projection());
  }});
  await bounded.clickStart();
  while (await bounded.runPollTimer()) {}
  assert.equal(boundedGets, 40); assert.equal(boundedPosts, 1);
  assert.match(bounded.ids["live-status"].textContent, /bounded polling window/);

  // Terminal projection renders allowlisted text and stops polling without claiming acceptance.
  const terminalSummary = '<img src=x onerror="alert(1)"> provider finished';
  const terminal = await setup({apiHandler:async (_url, options) => options.method === "POST"
    ? response(201, {run_id:runId, state:"ADMITTED", read_capability:capability, read_expires_at:"2099-09-19T00:00:00Z", replayed:false})
    : response(200, projection("GOVERNANCE_PENDING", {workflow_state:"GOVERNANCE_PENDING", summary_text:terminalSummary, evidence_status:"PENDING"}))});
  await terminal.clickStart();
  assert.match(terminal.ids["live-result"].textContent, /<img src=x/);
  assert.match(terminal.ids["live-result"].textContent, /Server workflow state/);
  assert.match(terminal.ids["live-status"].textContent, /not a Human acceptance decision/);
  assert.equal([...terminal.timers.values()].some(timer => timer.delay === 3000), false);

  // Expired capability is discarded before any GET.
  const expiredStorage = new Map([[sessionKey, JSON.stringify({
    schema:"AISCC-PUBLIC-LIVE-BROWSER-SESSION-V1", phase:"active", api_origin:apiOrigin,
    scenario_id:"stockroom-s1-normal", scenario_version:"1.0.0",
    idempotency_key:"0".repeat(32), run_id:runId, read_capability:capability,
    read_expires_at:"2000-01-01T00:00:00Z"
  })]]);
  const expired = await setup({storage:expiredStorage});
  assert.equal(expiredStorage.has(sessionKey), false);
  assert.match(expired.ids["live-status"].textContent, /expired and was discarded/);
  assert.equal(expired.calls.some(call => call.url.startsWith(apiOrigin)), false);

  console.log(JSON.stringify({
    result:"PASS", disabled_no_api:true, exact_post:true, session_storage_201:true,
    same_tab_resume:true, independent_session_no_recovery:true, capability_non_disclosure:true,
    no_local_storage:true, replay_202_no_recovery:true, uncertain_same_key_retry:true,
    bounded_polling_reads:boundedGets, polling_interval_ms:3000, terminal_stop:true,
    expiry_discard:true, human_visual_qa:"PENDING"
  }));
})().catch(error => { console.error(error); process.exitCode = 1; });
