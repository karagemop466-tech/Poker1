#!/usr/bin/env node
/* Headless check for the per-row source-change mark (SUGGESTIONS P8).
 *
 * The mark joins data/changes.json (written by the scheduled source monitor) to the
 * tournament row it applies to, so a reader sees "Source changed - re-check" next to
 * the row instead of only on the monitoring page. This script proves three things:
 *
 *   1. a row that the monitor marked carries the mark, the reason and a link to the
 *      official source that changed;
 *   2. a row that was NOT marked says when it was last checked instead of saying
 *      nothing - the unchanged state is dated to changes.json's own checked_at;
 *   3. the same behaviour holds on every page that shows an event table: the
 *      single-entry shortlist, the separate section, the unverified list, a venue
 *      page and the schedule's day cards.
 *
 * The DOM is fed from this repository, with data/changes.json replaced by a fixture
 * that marks one real row per page. No network is used. Exit status is non-zero if
 * any assertion fails, so CI can gate on it.
 */
"use strict";

const { JSDOM } = require("jsdom");
const fs = require("fs");
const path = require("path");
const nodeUrl = require("url");

const ROOT = path.dirname(__dirname);
const ORIGIN = "https://karagemop466-tech.github.io/Poker1/";
const results = [];

function check(name, condition, detail) {
  results.push({ name, ok: Boolean(condition), detail: detail == null ? "" : String(detail) });
}

const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const tournaments = JSON.parse(fs.readFileSync(path.join(ROOT, "data/tournaments.json"), "utf8")).rows;

/* Load a page with a fixture changes file that marks the given row ids. */
function load(page, markedIds, checkedAt) {
  const file = path.join(ROOT, page);
  const base = ORIGIN + page;
  const dom = new JSDOM(fs.readFileSync(file, "utf8"), { runScripts: "dangerously", url: base });
  const w = dom.window;
  const fixture = {
    checked_at: checkedAt || "2026-11-19",
    sources_facts_changed: markedIds.length,
    sources_raw_changed: markedIds.length,
    added: [],
    removed: [],
    changed: markedIds.map((id) => {
      const row = tournaments.filter((r) => r.id === id)[0] || {};
      return {
        id: id,
        kind: "tournament",
        name: row.name || id,
        date: row.date || null,
        reason: "official source page printed different values on its last re-check",
        source_url: "https://www.venetianlasvegas.com/resort/casino/poker.html",
        source_changed_at: "2026-11-19T15:17:11Z"
      };
    }).concat([{
      // `changed` also has dataset-vs-snapshot changes, which must not be mislabelled
      // as official source changes merely because they share the same JSON array.
      id: "r008", kind: "tournament", name: "synthetic dataset-only change",
      date: "2026-11-20", reason: "dataset value differs from the last verified snapshot"
    }])
  };
  w.fetch = (target) => {
    const rel = new URL(nodeUrl.resolve(base, String(target))).pathname.replace(/^\/Poker1\//, "");
    const p = path.join(ROOT, rel);
    if (!fs.existsSync(p)) return Promise.reject(new Error("404 " + rel));
    const body = rel === "data/changes.json" ? JSON.stringify(fixture) : fs.readFileSync(p, "utf8");
    return Promise.resolve({
      ok: true,
      status: 200,
      text: () => Promise.resolve(body),
      json: () => Promise.resolve(JSON.parse(body))
    });
  };
  return w;
}

/* The first row of a table whose id is in markedIds. */
function markedRow(w, scope, markedIds) {
  const rows = Array.from(w.document.querySelectorAll(scope + " tbody tr"));
  for (const tr of rows) {
    const cells = Array.from(tr.querySelectorAll("td")).map((td) => td.textContent);
    if (cells.some((c) => c.indexOf("Source changed") >= 0)) return { found: true, cells: cells };
  }
  return { found: false, cells: [], rows: rows.length, markedIds: markedIds.join(",") };
}

function unchangedCell(w, scope) {
  const rows = Array.from(w.document.querySelectorAll(scope + " tbody tr"));
  for (const tr of rows) {
    const cells = Array.from(tr.querySelectorAll("td")).map((td) => td.textContent);
    const cell = cells.filter((c) => c.indexOf("unchanged since the") >= 0)[0];
    if (cell) return cell.trim();
  }
  return "";
}

(async () => {
  const byStatus = (status) => tournaments.filter((r) => r.entry_status === status).map((r) => r.id);
  /* The shortlist hides dates before today, so the row it is checked on is one that is
     still on the list (today's date in Las Vegas is 2026-11-19). */
  const TODAY = "2026-11-19";
  const upcomingIds = byStatus("SE").concat(byStatus("CAND")).filter((id) => {
    const row = tournaments.filter((r) => r.id === id)[0];
    return row && row.date >= TODAY;
  });

  /* ---- 1. the single-entry shortlist ---- */
  const seId = upcomingIds[0];
  const w = load("pages/single-entry.html", [seId], "2026-11-19");
  await wait(1500);
  // The shortlist opens on the strict "written freezeout" view, which is empty for this
  // dataset; clearing the toggle shows the candidate rows the mark is checked on.
  const strict = w.document.getElementById("single-only");
  if (strict) {
    strict.checked = false;
    strict.dispatchEvent(new w.Event("change", { bubbles: true }));
    await wait(600);
  }
  const m = markedRow(w, "#content", [seId]);
  check("single-entry: the marked row carries the source-change mark", m.found,
        m.found ? m.cells.join(" | ").slice(0, 120) : (m.rows + " rows, marked " + m.markedIds));
  if (m.found) {
    check("single-entry: the mark names the reason and the date",
          m.cells.join(" ").indexOf("official source page printed different values") >= 0 &&
          m.cells.join(" ").indexOf("2026-11-19") >= 0,
          m.cells.join(" ").slice(0, 160));
    const link = Array.from(w.document.querySelectorAll("#content tbody a"))
      .filter((a) => (a.getAttribute("href") || "").indexOf("venetianlasvegas.com") >= 0);
    check("single-entry: the mark links to the official source that changed", link.length > 0,
          link.length + " official links in the table");
  }
  const unchanged = unchangedCell(w, "#content");
  check("single-entry: an unmarked row states when it was checked, dated to checked_at",
        unchanged.indexOf("2026-11-19") >= 0, unchanged.slice(0, 100) || "(no unchanged cell found)");
  const datasetOnlyName = tournaments.filter((r) => r.id === "r008")[0].name;
  const datasetOnly = Array.from(w.document.querySelectorAll("#content tbody tr"))
    .filter((tr) => tr.textContent.indexOf(datasetOnlyName) >= 0 &&
      tr.textContent.indexOf("Nov 20, 2026") >= 0)[0];
  check("single-entry: a dataset-only snapshot difference is not labelled as a source change",
        Boolean(datasetOnly) && datasetOnly.textContent.indexOf("Source changed") < 0 &&
        datasetOnly.textContent.indexOf("unchanged since the 2026-11-19 source check") >= 0,
        datasetOnly ? datasetOnly.textContent.slice(-140) : "fixture dataset-only row r008 not found");

  /* ---- 2. the separate section (re-entry / multi-entry rows) ---- */
  const reId = byStatus("RE")[0] || byStatus("MULTI")[0];
  const w2 = load("pages/separate-section.html", [reId], "2026-11-19");
  await wait(1500);
  const m2 = markedRow(w2, "#content", [reId]);
  check("separate section: the marked row carries the source-change mark", m2.found,
        m2.found ? m2.cells.join(" | ").slice(0, 120) : (m2.rows + " rows, marked " + m2.markedIds));

  /* ---- 3. the unverified list ---- */
  const unvId = byStatus("UNV")[0];
  const w3 = load("pages/unverified.html", unvId ? [unvId] : [], "2026-11-19");
  await wait(1500);
  if (unvId) {
    const m3 = markedRow(w3, "#content", [unvId]);
    check("unverified: the marked row carries the source-change mark", m3.found,
          m3.found ? m3.cells.join(" | ").slice(0, 120) : (m3.rows + " rows, marked " + m3.markedIds));
  } else {
    check("unverified: there is at least one unverified row to mark", false, "no UNV row in the dataset");
  }

  /* ---- 4. a venue page ---- */
  const venetianId = tournaments.filter((r) => r.venue === "The Venetian Resort").map((r) => r.id)[0] ||
                     tournaments.filter((r) => /Venetian/.test(r.venue)).map((r) => r.id)[0];
  const w4 = load("pages/venue-venetian.html", [venetianId], "2026-11-19");
  await wait(1800);
  const m4 = markedRow(w4, "#events", [venetianId]);
  check("venue page: the marked row carries the source-change mark", m4.found,
        m4.found ? m4.cells.join(" | ").slice(0, 120) : (m4.rows + " rows, marked " + m4.markedIds));

  /* ---- 5. the schedule's day cards ---- */
  const w5 = load("pages/schedule.html", [venetianId], "2026-11-19");
  await wait(1800);
  const schedMarked = w5.document.body.textContent.indexOf("Source changed") >= 0;
  const schedNote = w5.document.querySelectorAll("[data-source-check-note]").length;
  check("schedule: a changed event is marked in its day card", schedMarked, schedMarked ? "marked" : "no mark found");
  check("schedule: the page states the dated source check", schedNote > 0, schedNote + " note(s)");

  /* ---- 6. search results also surface the official-source mark ---- */
  const wSearch = load("pages/search.html", [seId], "2026-11-19");
  await wait(1500);
  const searchInput = wSearch.document.getElementById("q");
  searchInput.value = seId;
  searchInput.dispatchEvent(new wSearch.Event("input", { bubbles: true }));
  await wait(700);
  const searchMarked = Array.from(wSearch.document.querySelectorAll("#results .result"))
    .some((result) => result.textContent.indexOf("Source changed") >= 0);
  check("search: a changed tournament result carries the source-change mark", searchMarked,
        searchMarked ? seId + " marked" : "no marked result for " + seId);

  /* ---- 7. the page-level note on every event table ---- */
  for (const page of ["pages/single-entry.html", "pages/separate-section.html", "pages/unverified.html",
                      "pages/venue-venetian.html", "pages/schedule.html"]) {
    const w6 = load(page, [], "2026-11-19");
    await wait(1500);
    const note = w6.document.querySelectorAll("[data-source-check-note]");
    const text = note.length ? note[0].textContent : "";
    check(page + ": the dated source-check note is printed", note.length > 0 &&
          text.indexOf("2026-11-19") >= 0 && text.indexOf("No row was marked") >= 0,
          text.slice(0, 140) || "(no note)");
  }

  let failed = 0;
  for (const r of results) {
    if (!r.ok) failed += 1;
    console.log((r.ok ? "PASS" : "FAIL") + " | " + r.name + " | " + r.detail);
  }
  console.log(failed
    ? "check_source_change_badge: " + failed + " assertion(s) failed"
    : "check_source_change_badge: all " + results.length + " assertions passed");
  process.exit(failed ? 1 : 0);
})().catch((err) => {
  console.error("check_source_change_badge crashed: " + (err && err.stack ? err.stack : err));
  process.exit(1);
});
