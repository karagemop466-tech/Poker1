"use strict";
/* The trip calculator has two entry modes and both must be arithmetically sound:
     plan   - one entry per night, priced at the printed buy-in of the event this site
              already publishes as that date's primary (no typed input);
     manual - entries x buy-in typed by the reader (the original behaviour).
   The test reads the same JSON the page reads, so it recomputes the expected plan
   total from the published rows instead of hard-coding a number that would have to
   be edited every time a schedule changes. */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { JSDOM } = require("jsdom");
const root = path.resolve(__dirname, "..");
const data = (rel) => JSON.parse(fs.readFileSync(path.join(root, "data", rel), "utf8"));
const dom = new JSDOM(fs.readFileSync(path.join(root, "pages/calculator.html"), "utf8"), {
  url: "https://example.test/pages/calculator.html",
  runScripts: "dangerously",
  beforeParse(window) {
    window.fetch = async (url) => ({ ok: true, json: async () =>
      JSON.parse(fs.readFileSync(path.resolve(root, "pages", url), "utf8")) });
  }
});
(async () => {
  await new Promise(setImmediate);
  const doc = dom.window.document;
  const result = (label) => [...doc.querySelectorAll("#c-out .box")]
    .find((box) => box.querySelector(".l").textContent.startsWith(label)).querySelector(".n").textContent;
  const set = (id, value) => {
    const el = doc.getElementById("c-" + id);
    el.value = value;
    el.dispatchEvent(new dom.window.Event(el.tagName === "SELECT" ? "change" : "input"));
  };
  const money = (v) => "$" + Number(v).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

  const quote = data("rates.json").entries[+doc.getElementById("c-quote").value];
  const rows = data("tournaments.json").rows;

  /* ---- plan mode is the default ------------------------------------------- */
  assert.equal(doc.getElementById("c-mode").value, "plan");
  assert.equal(doc.getElementById("c-entries").disabled, true,
    "manual entry count must be disabled while the plan prices the entry side");

  // Recompute the plan from the published rows: one line per night in [arrival, departure),
  // continuations excluded, the SE/CAND primary preferred, earliest start first.
  const nights = [];
  for (let d = quote.arrival; d < quote.departure; d = new Date(Date.parse(d + "T12:00:00Z") + 86400000).toISOString().slice(0, 10)) {
    const same = rows.filter((r) => r.date === d && r.entry_status !== "CONT");
    if (!same.length) { nights.push(null); continue; }
    const prefer = same.filter((r) => r.entry_status === "SE" || r.entry_status === "CAND");
    const pool = (prefer.length ? prefer : same).slice().sort((a, b) => String(a.start).localeCompare(String(b.start)));
    nights.push(pool[0]);
  }
  const expectedEntry = nights.filter((r) => r && r.buy_in_usd != null).reduce((n, r) => n + r.buy_in_usd, 0);
  assert.ok(expectedEntry > 0, "the default quote must have at least one priced night");
  assert.equal(result("Tournament entries"), money(expectedEntry), "plan entry total");
  assert.equal(result("Trip total"), money(quote.checkout_total_usd + expectedEntry));
  assert.match(doc.getElementById("c-note").textContent, /prices one entry per night/);
  assert.match(doc.getElementById("c-note").textContent, /candidate pending a written one-entry ruling/);

  // The night-by-night table must exist, have one row per night, link an official source
  // for every priced night, and its own total must equal the box above.
  const planRows = [...doc.querySelectorAll("#c-plan tbody tr")];
  assert.equal(planRows.length, nights.length + 1, "one row per night plus the total row");
  const pricedRows = planRows.slice(0, nights.length).filter((tr) => !tr.querySelector(".muted"));
  pricedRows.forEach((tr) => assert.ok(tr.querySelector('a[href^="https://"]'), "every priced night links its official source"));
  assert.ok(doc.getElementById("c-plan").textContent.includes(money(expectedEntry)));

  /* ---- manual mode still does entries x buy-in ---------------------------- */
  set("mode", "manual");
  assert.equal(doc.getElementById("c-entries").disabled, false);
  assert.equal(result("Trip total"), "$2,712.44");
  set("buyin", "125.50");
  assert.equal(result("Trip total"), "$2,537.94");
  set("buyin", "");
  assert.equal(result("Trip total"), "n/a");
  set("entries", "0");
  assert.equal(result("Trip total"), "$2,412.44");
  set("entries", "1.5");
  assert.equal(result("Trip total"), "n/a");

  /* ---- unchanged page guarantees ----------------------------------------- */
  set("mode", "plan");
  assert.match(doc.getElementById("c-window").textContent, /not a playable sequence/);
  assert.equal(doc.querySelectorAll("#c-compare tbody tr").length, 1);
  assert.ok(doc.querySelector('#c-compare a[href="https://www.venetianlasvegas.com/book"]'));
  dom.window.close();
  console.log("check_calculator: OK (plan mode priced from the published schedule; manual mode unchanged)");
})().catch((err) => { dom.window.close(); console.error(err); process.exitCode = 1; });
