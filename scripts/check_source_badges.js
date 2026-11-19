"use strict";
/* SUGGESTIONS P8 regression: the tournament and hotel tables must surface the
   monitor's per-row verdict, joined by row id from data/changes.json.
   Scenario 1: a fixture changes.json marks the first tournament row of the
   Venetian venue table - that row shows the red chip, the re-check date and a
   link to the official page; every other row shows the explicit "no source
   change as of <fixture date>" line. The marks must survive a re-render
   triggered by a sort click. Scenario 2: the real data/changes.json (no
   changed rows) must produce zero red chips and the as-of date from the file,
   not a date hard-coded in the renderer. No network is used. */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const nodeUrl = require("node:url");
const { JSDOM } = require("jsdom");

const ROOT = path.resolve(__dirname, "..");
const ORIGIN = "https://karagemop466-tech.github.io/Poker1/";

function load(page, overrides) {
  const file = path.join(ROOT, page);
  const base = ORIGIN + page;
  const dom = new JSDOM(fs.readFileSync(file, "utf8"), { runScripts: "dangerously", url: base });
  const w = dom.window;
  w.fetch = (target) => {
    const rel = new URL(nodeUrl.resolve(base, String(target))).pathname.replace(/^\/Poker1\//, "");
    if (overrides && overrides[rel] != null) {
      return Promise.resolve({ ok: true, status: 200, text: () => Promise.resolve(overrides[rel]),
        json: () => Promise.resolve(JSON.parse(overrides[rel])) });
    }
    const p = path.join(ROOT, rel);
    if (!fs.existsSync(p)) return Promise.reject(new Error("404 " + rel));
    const body = fs.readFileSync(p, "utf8");
    return Promise.resolve({ ok: true, status: 200, text: () => Promise.resolve(body),
      json: () => Promise.resolve(JSON.parse(body)) });
  };
  return w;
}
const wait = (ms) => new Promise((r) => setTimeout(r, ms));

(async () => {
  const rows = JSON.parse(fs.readFileSync(path.join(ROOT, "data/tournaments.json"), "utf8")).rows;
  const first = rows.find((r) => r.venue === "The Venetian" || /Venetian/.test(r.venue));
  assert.ok(first, "fixture needs at least one Venetian tournament row");

  /* ---- scenario 1: a source change is marked on exactly the joined row ---- */
  const fixture = JSON.stringify({
    checked_at: "2026-11-19", sources_facts_changed: 1, sources_raw_changed: 1,
    added: [], removed: [],
    changed: [{ id: first.id, kind: "tournament", name: first.name, date: first.date,
      reason: "official source page printed different values on its last re-check",
      source_url: "https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html",
      source_changed_at: "2026-11-19T07:17:00Z",
      diff: { "official source verified against": ["2026-11-17T01:30:45Z", "2026-11-19T07:17:00Z (dse-nov-2026.html)"] } }]
  });
  const w1 = load("pages/venue-venetian.html", { "data/changes.json": fixture });
  await wait(600);
  const tables = w1.document.querySelectorAll("#events table");
  assert.ok(tables.length >= 1, "venue page renders a tournament table");
  const text = (el) => (el ? el.textContent.replace(/\s+/g, " ").trim() : "");
  const markedCells = Array.from(w1.document.querySelectorAll("#events td"))
    .filter((td) => /source changed - re-check/.test(text(td)));
  assert.equal(markedCells.length, 1, "exactly the joined row is marked");
  assert.match(text(markedCells[0]), /as of 2026-11-19/);
  assert.ok(markedCells[0].querySelector('a[href^="https://www.venetianlasvegas.com/"]'),
    "the mark links to the official source page");
  const quiet = Array.from(w1.document.querySelectorAll("#events td"))
    .filter((td) => /no source change as of 2026-11-19/.test(text(td)));
  assert.ok(quiet.length >= 2, "unchanged rows carry the explicit dated 'no change' state");
  assert.ok(!Array.from(w1.document.querySelectorAll("#events td"))
    .some((td) => /no source change as of 2026-11-17/.test(text(td))),
  "the as-of date comes from the file, never from the renderer constant");

  /* the marks survive a sort-driven re-render */
  const buyTh = Array.from(tables[0].querySelectorAll("th"))
    .find((th) => /Buy-in/.test(th.textContent));
  buyTh.dispatchEvent(new w1.Event("click", { bubbles: true }));
  await wait(150);
  assert.equal(Array.from(w1.document.querySelectorAll("#events td"))
    .filter((td) => /source changed - re-check/.test(text(td))).length, 1,
  "the mark survives the re-render after sorting");
  w1.close();

  /* ---- scenario 2: the real changes.json on file - the invariant is the JOIN, not emptiness
     (hardened twice on 2026-11-19: sessions f3a84f9b and 336fb2af independently reached the same
     fix after the monitor landed its first real row changes, which made the old "assert 0 chips"
     check a false alarm). ---- */
  const w2 = load("pages/venue-venetian.html", {});
  await wait(600);
  const real = JSON.parse(fs.readFileSync(path.join(ROOT, "data/changes.json"), "utf8"));
  // The expected count comes from the files on disk, not from a fixed zero: the monitor
  // legitimately lists changed Venetian rows (2026-11-19 refresh), and each must be marked.
  const changedIds = new Set((real.changed || []).map((c) => c.id));
  const dataRows = JSON.parse(fs.readFileSync(path.join(ROOT, "data/tournaments.json"), "utf8")).rows;
  const expectedMarks = dataRows.filter((r) => /Venetian/.test(r.venue) && changedIds.has(r.id)).length;
  const chips2 = Array.from(w2.document.querySelectorAll("#events td"))
    .filter((td) => /source changed - re-check/.test(text(td)));
  assert.equal(chips2.length, expectedMarks,
    "the Venetian marks equal the changed Venetian rows listed in changes.json (" + expectedMarks + ")");
  if (expectedMarks > 0) {
    assert.ok(chips2.every((td) => /as of /.test(text(td)) && td.querySelector("a[href]")),
      "every real-change chip names its re-check date and links its source");
  }
  const asOf = String(real.checked_at || "").slice(0, 10);
  if (asOf) {
    const dated = Array.from(w2.document.querySelectorAll("#events td"))
      .filter((td) => (text(td).match(new RegExp("no source change as of " + asOf)) || []).length > 0);
    assert.ok(dated.length >= 1, "the published state names the real check date " + asOf);
  }
  w2.close();

  /* ---- scenario 3: a PDF layout-baseline warning must not be called a source change
     or a clean "no source change" state. ---- */
  const layoutRow = rows.find((r) => /Wynn/.test(r.venue || "") &&
    (r.sources || []).some((s) => /\.pdf(?:\?|$)/i.test(s.url || "")));
  assert.ok(layoutRow, "fixture needs a Wynn row citing an official PDF");
  const layoutSource = layoutRow.sources.find((s) => /\.pdf(?:\?|$)/i.test(s.url || "")).url;
  const pendingFixture = JSON.stringify({
    checked_at: "2026-11-19", sources_facts_changed: 0, sources_raw_changed: 0,
    added: [], removed: [], changed: [],
    layout_review: [{ id: layoutRow.id, kind: "tournament", name: layoutRow.name, date: layoutRow.date,
      status: "layout-baseline-pending", checked_at: "2026-11-19T16:45:00Z",
      reason: "position-aware PDF facts have no comparison baseline yet", source_url: layoutSource }]
  });
  const w3 = load("pages/venue-wynn.html", { "data/changes.json": pendingFixture });
  await wait(600);
  const pendingCells = Array.from(w3.document.querySelectorAll("#events td"))
    .filter((td) => /PDF layout baseline pending/.test(text(td)));
  assert.equal(pendingCells.length, 1, "only the row with a pending layout comparison is marked");
  assert.ok(pendingCells[0].querySelector("a[href=\"" + layoutSource + "\"]"),
    "the pending notice links to the row's official PDF");
  assert.doesNotMatch(text(pendingCells[0]), /source changed - re-check|no source change as of/,
    "pending coverage is not misreported as either changed or confirmed unchanged");
  w3.close();

  /* ---- scenario 4: extraction failures are distinguished from a missing baseline. ---- */
  const unavailableFixture = JSON.stringify({
    checked_at: "2026-11-19", sources_facts_changed: 0, sources_raw_changed: 0,
    added: [], removed: [], changed: [],
    layout_review: [{ id: layoutRow.id, kind: "tournament", name: layoutRow.name, date: layoutRow.date,
      status: "layout-unavailable", checked_at: "2026-11-19T16:45:00Z",
      reason: "position-aware PDF extraction is incomplete", source_url: layoutSource }]
  });
  const w4 = load("pages/venue-wynn.html", { "data/changes.json": unavailableFixture });
  await wait(600);
  const unavailableCells = Array.from(w4.document.querySelectorAll("#events td"))
    .filter((td) => /PDF layout check unavailable/.test(text(td)));
  assert.equal(unavailableCells.length, 1, "an extraction failure is shown on its affected row");
  assert.ok(unavailableCells[0].querySelector("a[href=\"" + layoutSource + "\"]"),
    "the unavailable notice links to the row's official PDF");
  assert.doesNotMatch(text(unavailableCells[0]), /source changed - re-check|no source change as of/,
    "unavailable coverage is not called changed or unchanged");
  w4.close();
  console.log("check_source_badges: OK");
})().catch((err) => { console.error(err); process.exitCode = 1; });
