"use strict";
/* SUGGESTIONS P3 regression: the derived spend-advantage reading must be visible on
   every tournament table, must agree with data/tournaments.json row for row, and the
   "no further-entry clause printed" filter must select exactly those rows - on both
   the single-entry page (where it keeps the candidates) and the separate section
   (where it must remove every row, because each of those rows' own sheet prices or
   permits a further entry). The two explanation paragraphs the pages print are
   checked against counts computed from the data too, so a number on the page can
   never be older than the dataset. No network is used. */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const nodeUrl = require("node:url");
const { JSDOM } = require("jsdom");

const ROOT = path.resolve(__dirname, "..");
const ORIGIN = "https://karagemop466-tech.github.io/Poker1/";

function load(page) {
  const base = ORIGIN + page;
  const dom = new JSDOM(fs.readFileSync(path.join(ROOT, page), "utf8"),
    { runScripts: "dangerously", url: base });
  const w = dom.window;
  w.fetch = (target) => {
    const rel = new URL(nodeUrl.resolve(base, String(target))).pathname.replace(/^\/Poker1\//, "");
    const p = path.join(ROOT, rel);
    if (!fs.existsSync(p)) return Promise.reject(new Error("404 " + rel));
    const body = fs.readFileSync(p, "utf8");
    return Promise.resolve({ ok: true, status: 200, text: () => Promise.resolve(body),
      json: () => Promise.resolve(JSON.parse(body)) });
  };
  return w;
}
const wait = (ms) => new Promise((r) => setTimeout(r, ms));
const text = (el) => (el ? el.textContent.replace(/\s+/g, " ").trim() : "");

// Mirrors vegasDate() in assets/app.js: the "today and later" toggle is on by
// default on the single-entry page, so the expected row set uses the same day.
function vegasToday() {
  const parts = new Intl.DateTimeFormat("en-US", {
    timeZone: "America/Los_Angeles", year: "numeric", month: "2-digit", day: "2-digit"
  }).formatToParts(new Date());
  const part = (t) => parts.find((p) => p.type === t).value;
  return `${part("year")}-${part("month")}-${part("day")}`;
}

function tally(rows) {
  const out = {};
  rows.forEach((r) => {
    const sa = r.spend_advantage || {};
    if (sa.label) out[sa.label] = (out[sa.label] || 0) + 1;
  });
  return out;
}

function chipCounts(w) {
  const known = new Set();
  JSON.parse(fs.readFileSync(path.join(ROOT, "data/tournaments.json"), "utf8")).rows.forEach((r) => {
    if (r.spend_advantage) known.add(r.spend_advantage.label);
  });
  const counts = {};
  Array.from(w.document.querySelectorAll("#content table tbody tr, #events table tbody tr")).forEach((tr) => {
    const tds = Array.from(tr.querySelectorAll("td"));
    const hits = tds.map(text).filter((t) => Array.from(known).some((k) => t.includes(k)));
    assert.equal(hits.length, 1, "each row must carry exactly one spend-advantage chip");
    const label = Array.from(known).find((k) => hits[0].includes(k));
    counts[label] = (counts[label] || 0) + 1;
  });
  return counts;
}

(async () => {
  const rows = JSON.parse(fs.readFileSync(path.join(ROOT, "data/tournaments.json"), "utf8")).rows;
  assert.ok(rows.every((r) => r.spend_advantage && r.spend_advantage.value),
    "every published row carries a derived reading");

  /* ---- the separate section: every row is there *because* its sheet prices one ---- */
  const sep = rows.filter((r) => r.entry_status === "MULTI" || r.entry_status === "RE");
  const w1 = load("pages/separate-section.html");
  await wait(700);
  const head1 = Array.from(w1.document.querySelectorAll("#content th")).map((th) => text(th));
  assert.ok(head1.some((h) => /Spend advantage/.test(h)), "the column header is printed");
  assert.deepEqual(chipCounts(w1), tally(sep), "the chips equal the rows' own readings");
  const split = Array.from(w1.document.querySelectorAll("#content p.small, #page p.small, p.small"))
    .map(text).join(" | ");
  Object.entries(tally(sep)).forEach(([label, n]) => {
    // The paragraph prints "3 · later buy-in priced on the sheet" style pairs.
    const key = label.toLowerCase();
    const hit = split.split("|").find((line) => line.includes(key));
    assert.ok(hit, `the breakdown paragraph names "${label}"`);
    assert.ok(hit.includes(String(n)), `the paragraph prints ${n} for "${label}"`);
  });
  const box1 = w1.document.getElementById("spend-none");
  assert.ok(box1, "the filter toggle is rendered");
  box1.checked = true;
  box1.dispatchEvent(new w1.Event("change", { bubbles: true }));
  await wait(200);
  assert.equal(w1.document.querySelectorAll("#content table tbody tr").length, 0,
    "no row of the separate section survives a filter for sheets that print no further entry");
  assert.match(text(w1.document.querySelector("#filters .summary") || w1.document.querySelector(".summary")),
    /sheet prints no further-entry or add-on clause/, "the active filter is named back to the reader");
  w1.close();

  /* ---- the single-entry page: the shortlist and the new filter ---- */
  const today = vegasToday();
  const pageRows = rows.filter((r) => r.entry_status === "SE" || r.entry_status === "CAND");
  const visibleBase = pageRows.filter((r) => r.date >= today);
  const silent = pageRows.filter((r) => r.spend_advantage.value === "no-further-entry-clause");
  const w2 = load("pages/single-entry.html");
  await wait(700);
  assert.ok(Array.from(w2.document.querySelectorAll("#content th")).some((th) => /Spend advantage/.test(text(th))),
    "the column is on the single-entry table too");
  // Default state: the written-freezeout toggle is on, and no row qualifies, exactly as
  // the page's own lead says. The table must not quietly widen the gate to look busy.
  const seCount = pageRows.filter((r) => r.entry_status === "SE").length;
  assert.equal(w2.document.querySelectorAll("#content table tbody tr").length, seCount,
    "the shortlist shows only written-freezeout rows by default, whatever that count is");
  const lead = Array.from(w2.document.querySelectorAll(".lead")).map(text).join(" | ");
  if (seCount === 0) assert.match(lead, /no confirmed rows/i, "the lead matches the empty shortlist");
  const strict = w2.document.getElementById("single-only");
  strict.checked = false;
  strict.dispatchEvent(new w2.Event("change", { bubbles: true }));
  await wait(200);
  assert.equal(w2.document.querySelectorAll("#content table tbody tr").length, visibleBase.length,
    "switching the strict toggle off reveals the upcoming candidates");
  const box2 = w2.document.getElementById("spend-none");
  assert.ok(box2, "the new filter is rendered on the shortlist too");
  box2.checked = true;
  box2.dispatchEvent(new w2.Event("change", { bubbles: true }));
  await wait(200);
  const visibleSilent = visibleBase.filter((r) => r.spend_advantage.value === "no-further-entry-clause");
  assert.equal(w2.document.querySelectorAll("#content table tbody tr").length, visibleSilent.length,
    "the filter leaves exactly the rows whose sheet was read and printed no clause");
  assert.equal(silent.length, pageRows.length - pageRows.filter((r) => r.spend_advantage.advantage === "yes").length,
    "the two readings partition the page - no row is left unclassified");
  const gate = Array.from(w2.document.querySelectorAll("p.small")).map(text).join(" | ");
  assert.ok(gate.includes(`${silent.length} of the ${pageRows.length} rows`),
    "the page states the count it computed from the data");
  assert.match(gate, /not a confirmation/);
  w2.close();

  console.log(`check_spend_filter: OK (${pageRows.length} shortlist rows, ${silent.length} silent-sheet rows, ` +
    `${sep.length} excluded rows)`);
})().catch((err) => { console.error(err); process.exitCode = 1; });
