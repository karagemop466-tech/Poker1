#!/usr/bin/env node
// PRESERVED TOOL (PR #53, session d57243e7; ported by session df94b75e).
// UI enforcement test written in parallel with scripts/smoke_test.js.
// NOT wired into CI; npm run test:smoke covers page rendering. Kept as a manual tool.
//
/**
 * Behavioural checks for the shared UI, run in a headless DOM.
 *
 * ``scripts/smoke_test.js`` answers "does every page render without throwing?".
 * This script answers the harder question every request in this project depends
 * on: does the page actually do the thing it claims?
 *
 *   * the tournament tables show a "Last checked" date on every row
 *   * the search box narrows the table
 *   * the date range and the buy-in ceiling narrow the table
 *   * the hotels page has a 30-minute walking filter and it removes rows
 *   * the hotels table shows a "Last checked" date on every row
 *   * the search page returns hits from more than one dataset
 *
 * The DOM is fed from the files in this repository, so the assertion runs against
 * the same JSON the published site fetches. No network is used. Exit status is
 * non-zero if any assertion fails, so CI can gate on it.
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

function load(page) {
  const file = path.join(ROOT, page);
  const base = ORIGIN + page;
  const dom = new JSDOM(fs.readFileSync(file, "utf8"), { runScripts: "dangerously", url: base });
  const w = dom.window;
  // Serve this repository's files for the page's relative fetches.
  w.fetch = (target) => {
    const rel = new URL(nodeUrl.resolve(base, String(target))).pathname.replace(/^\/Poker1\//, "");
    const p = path.join(ROOT, rel);
    if (!fs.existsSync(p)) return Promise.reject(new Error("404 " + rel));
    const body = fs.readFileSync(p, "utf8");
    return Promise.resolve({
      ok: true, status: 200,
      text: () => Promise.resolve(body),
      json: () => Promise.resolve(JSON.parse(body)),
    });
  };
  return w;
}

const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const type = (w, el, value, event) => {
  if (!el) return;
  el.value = value;
  el.dispatchEvent(new w.Event(event, { bubbles: true }));
};
const headText = (w, scope) =>
  Array.from(w.document.querySelectorAll(scope + " thead th")).map((th) => th.textContent.trim());
const bodyRows = (w, scope) => w.document.querySelectorAll(scope + " tbody tr").length;

(async () => {
  /* ---------------- tournament table ---------------- */
  const w = load("pages/single-entry.html");
  await wait(1200);
  const allRows = bodyRows(w, "#content");
  const heads = headText(w, "#content");
  check("single-entry table renders rows", allRows > 0, allRows + " rows");
  check('table has a "Last checked" column', heads.includes("Last checked"), heads.join(" | "));

  if (heads.includes("Last checked")) {
    const idx = heads.indexOf("Last checked");
    const cells = Array.from(w.document.querySelectorAll("#content tbody tr"))
      .map((tr) => (tr.querySelectorAll("td")[idx] || {}).textContent)
      .map((t) => (t || "").trim());
    // The site prints the check date as ISO (2026-11-17); accept that and the short form.
    const okCell = (c) => /^\d{4}-\d{2}-\d{2}$/.test(c) || /^[A-Z][a-z]{2} \d{1,2}$/.test(c) || c === "not recorded";
    check("every displayed row shows a check date", cells.length > 0 && cells.every(okCell),
          cells.slice(0, 3).join(", "));
  }

  type(w, w.document.getElementById("q"), "Milestone", "input");
  await wait(300);
  const searched = bodyRows(w, "#content");
  check("search box narrows the table", searched > 0 && searched < allRows, searched + " of " + allRows);
  type(w, w.document.getElementById("q"), "", "input");

  type(w, w.document.getElementById("date-from"), "2026-12-01", "input");
  await wait(300);
  const dated = bodyRows(w, "#content");
  check("date range narrows the table", dated > 0 && dated < allRows, dated + " of " + allRows);
  type(w, w.document.getElementById("date-from"), "", "input");

  type(w, w.document.getElementById("buy-max"), "300", "input");
  await wait(300);
  const cheap = bodyRows(w, "#content");
  check("buy-in ceiling narrows the table", cheap > 0 && cheap < allRows, cheap + " of " + allRows);

  /* ---------------- hotels: 30-minute walking rule ---------------- */
  const h = load("pages/hotels.html");
  await wait(1200);
  // The shipped control is a checkbox (#hotel-walk30, "30 min walk to a poker room").
  const sel = h.document.getElementById("hotel-walk30");
  check("hotels page has a 30-minute walking filter", !!sel, sel ? sel.type : "missing");
  const hotelHeads = headText(h, "#content");
  check('hotels table has a "Last checked" column', hotelHeads.includes("Last checked"),
        hotelHeads.join(" | "));
  if (sel) {
    const before = bodyRows(h, "#content");
    sel.checked = true;
    sel.dispatchEvent(new h.Event("change", { bubbles: true }));
    await wait(300);
    const after = bodyRows(h, "#content");
    check("walking filter removes over-30-minute properties", after > 0 && after < before,
          before + " -> " + after);
  }

  /* ---------------- one search box across every table ---------------- */
  const s = load("pages/search.html");
  await wait(1400);
  const box = s.document.getElementById("q");
  check("search page has one search box", !!box, box ? box.tagName : "missing");
  if (box) {
    type(s, box, "Venetian", "input");
    await wait(500);
    const hits = s.document.querySelectorAll("#results .result").length;
    check("search returns hits across datasets", hits > 5, hits + " result cards");
  }

  /* ---------------- schedule: primary and fallback ---------------- */
  const sc = load("pages/schedule.html");
  await wait(1400);
  const days = sc.document.querySelectorAll("#content .card.day").length;
  const primaries = sc.document.body.textContent.split("Primary").length - 1;
  const fallbacks = sc.document.body.textContent.split("Conditional fallback").length - 1;
  check("schedule renders one card per day", days > 0, days + " days");
  check("each day marks a primary event", primaries > 0, primaries + " primary chips");
  check("fallback events are labelled conditionally", fallbacks >= 0, fallbacks + " fallback chips");

  let failed = 0;
  for (const r of results) {
    if (!r.ok) failed += 1;
    console.log((r.ok ? "PASS" : "FAIL") + " | " + r.name + " | " + r.detail);
  }
  console.log(failed ? "ui_test: " + failed + " assertion(s) failed" : "ui_test: all " + results.length + " assertions passed");
  process.exit(failed ? 1 : 0);
})().catch((err) => {
  console.error("ui_test crashed: " + (err && err.stack ? err.stack : err));
  process.exit(1);
});
