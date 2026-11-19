"use strict";
/* Verify the single-entry page distinguishes written-confirmed rows from
   candidates, and that its strict toggle and date range filter the event table.
   No network is used; page assets/data are loaded from this checkout. */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { JSDOM } = require("jsdom");

const ROOT = path.resolve(__dirname, "..");
const PAGE = "pages/single-entry.html";
const base = "https://karagemop466-tech.github.io/Poker1/" + PAGE;
const data = JSON.parse(fs.readFileSync(path.join(ROOT, "data/tournaments.json"), "utf8"));

function sleep(ms) { return new Promise((resolve) => setTimeout(resolve, ms)); }
function load() {
  return new JSDOM(fs.readFileSync(path.join(ROOT, PAGE), "utf8"), {
    url: base, runScripts: "dangerously", pretendToBeVisual: true,
    beforeParse(window) {
      window.fetch = (target) => {
        const pathname = new URL(String(target), base).pathname.replace(/^\/Poker1\//, "");
        const filename = path.join(ROOT, pathname);
        if (!fs.existsSync(filename)) return Promise.reject(new Error("404 " + pathname));
        const body = fs.readFileSync(filename, "utf8");
        return Promise.resolve({ ok: true, status: 200,
          json: () => Promise.resolve(JSON.parse(body)), text: () => Promise.resolve(body) });
      };
    }
  });
}
function change(window, selector, value) {
  const el = window.document.querySelector(selector);
  assert.ok(el, "control exists: " + selector);
  if (el.type === "checkbox") el.checked = value;
  else el.value = value;
  el.dispatchEvent(new window.Event(el.type === "checkbox" || el.tagName === "SELECT" ? "change" : "input", { bubbles: true }));
}
function visibleRows(window) {
  return Array.from(window.document.querySelectorAll("#content tbody tr"));
}

(async () => {
  const dom = load();
  const w = dom.window;
  await sleep(700);
  const diary = w.document.getElementById("trip-diary");
  assert.ok(diary, "candidate plan renders");
  const diaryText = diary.textContent.replace(/\s+/g, " ");
  assert.match(diaryText, /Candidate day plan.*not booking-ready/i);
  assert.match(diaryText, /Candidate rows are not verified freezeouts/i);
  assert.doesNotMatch(diaryText, /dates in this dataset hold at least one verified single-entry event/i,
    "candidate-only dates are not mislabeled as confirmed freezeouts");
  assert.match(diaryText, /estimated finish about \d{1,2}:\d{2} (?:AM|PM)/,
    "printed estimate renders its clock time");
  assert.doesNotMatch(diaryText, /estimated finish about ·/,
    "the estimate formatter receives the full event record, not only its time string");
  const schedule = JSON.parse(fs.readFileSync(path.join(ROOT, "data/schedule.json"), "utf8"));
  const byId = new Map(data.rows.map((row) => [row.id, row]));
  const candidatePrimaryCards = Array.from(diary.querySelectorAll("ul.diary > li")).filter((card) => {
    const date = card.querySelector("h3").textContent;
    const day = schedule.days.find((entry) => new Date(entry.date + "T12:00:00Z").toLocaleDateString("en-US", {
      weekday: "short", month: "short", day: "numeric", year: "numeric", timeZone: "UTC"
    }) === date);
    return day && byId.get(day.primary_id)?.entry_status === "CAND";
  });
  for (const card of candidatePrimaryCards) {
    assert.match(card.querySelector("li strong").textContent, /policy unconfirmed/i,
      "a candidate primary must not be labeled as a playable commitment");
  }

  const confirmed = data.rows.filter((row) => row.entry_status === "SE");
  const eligible = data.rows.filter((row) => row.entry_status === "SE" || row.entry_status === "CAND");
  const strict = w.document.getElementById("single-only");
  assert.ok(strict && strict.checked, "written-confirmation filter is available and enabled by default");
  change(w, "#future-only", false);
  await sleep(100);
  assert.equal(visibleRows(w).length, confirmed.length,
    "strict mode displays only rows marked SE, never candidate or unverified rows");

  change(w, "#single-only", false);
  await sleep(100);
  assert.equal(visibleRows(w).length, eligible.length,
    "clearing the written-confirmation filter exposes the candidate list");

  const date = eligible.find((row) => row.entry_status === "CAND").date;
  change(w, "#date-from", date);
  change(w, "#date-to", date);
  await sleep(100);
  const expectedOnDate = eligible.filter((row) => row.date === date).length;
  assert.equal(visibleRows(w).length, expectedOnDate,
    "selecting one date leaves only events on that date");
  for (const row of visibleRows(w)) {
    assert.match(row.querySelector("td").textContent, /\w+\s+\d{1,2},\s+\d{4}/,
      "each remaining row prints its event date");
  }

  console.log("check_single_entry_render: OK (" + confirmed.length + " written-confirmed; " +
    (eligible.length - confirmed.length) + " candidates; date filter verified)");
  dom.window.close();
})().catch((error) => { console.error(error); process.exitCode = 1; });
