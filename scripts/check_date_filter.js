"use strict";
/* Date filter test. The shared filter bar must offer, on every tournament table:
     - a date preset (today, tomorrow, this weekend, next 7 / 30 days, ticked days),
     - a per-date chip list built from the dates the dataset actually holds,
   and both must narrow the rendered rows to exactly those dates. The expected sets are
   recomputed from data/tournaments.json, so the test follows the data instead of
   hard-coding a count that breaks on the next series. */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { JSDOM } = require("jsdom");
const root = path.resolve(__dirname, "..");
const rows = JSON.parse(fs.readFileSync(path.join(root, "data/tournaments.json"), "utf8")).rows;
const html = fs.readFileSync(path.join(root, "pages", "separate-section.html"), "utf8");

const dom = new JSDOM(html, {
  url: "https://example.test/pages/separate-section.html",
  runScripts: "dangerously",
  pretendToBeVisual: true,
  beforeParse(window) {
    window.fetch = async (url) => ({
      ok: true,
      json: async () => JSON.parse(fs.readFileSync(path.resolve(root, "pages", url), "utf8"))
    });
  }
});

const wait = (ms) => new Promise((r) => setTimeout(r, ms));

function vegasToday() {
  const parts = new Intl.DateTimeFormat("en-US", {
    timeZone: "America/Los_Angeles", year: "numeric", month: "2-digit", day: "2-digit"
  }).formatToParts(new Date());
  const get = (t) => parts.find((p) => p.type === t).value;
  return get("year") + "-" + get("month") + "-" + get("day");
}

(async () => {
  await wait(50);
  const doc = dom.window.document;
  const bodyRows = () => [...doc.querySelectorAll("#content tbody tr")];
  const datesShown = () => new Set(bodyRows().map((tr) => tr.getAttribute("data-date")).filter(Boolean));
  const summary = () => doc.querySelector(".filters .summary").textContent;

  // The tables must expose the row date on the <tr>, which is what makes this testable
  // and what a reader sees in the Date column.
  assert.ok(doc.getElementById("date-preset"), "date preset control is missing");
  assert.ok(doc.querySelectorAll(".filters details.day-chips input[type=checkbox]").length ||
            doc.querySelectorAll(".filters .labels.dates input[type=checkbox]").length,
            "per-date chip list is missing");

  const all = bodyRows().length;
  assert.ok(all > 0, "table rendered no rows");
  const allDates = [...new Set(rows.filter((r) => r.entry_status === "MULTI" || r.entry_status === "RE")
    .map((r) => r.date))].sort();
  assert.equal(datesShown().size, allDates.length, "unfiltered table shows every dataset date");

  // ---- per-date chips -------------------------------------------------------
  const chips = [...doc.querySelectorAll(".filters .labels.dates input[type=checkbox]")];
  assert.ok(chips.length >= 10, "chip list looks truncated");
  const target = chips[3].value;
  chips[3].checked = true;
  chips[3].dispatchEvent(new dom.window.Event("change", { bubbles: true }));
  await wait(20);
  assert.deepEqual([...datesShown()], [target], "ticking one day leaves exactly that day");
  assert.equal(doc.getElementById("date-preset").value, "picked", "ticking a day switches the preset to the ticked set");
  assert.match(summary(), /1 ticked day/);
  chips[3].checked = false;
  chips[3].dispatchEvent(new dom.window.Event("change", { bubbles: true }));
  await wait(20);
  assert.equal(bodyRows().length, all, "clearing the tick restores every row");

  // ---- presets -------------------------------------------------------------
  const preset = doc.getElementById("date-preset");
  const today = vegasToday();
  const expectFor = (from, to) => new Set(rows
    .filter((r) => (r.entry_status === "MULTI" || r.entry_status === "RE") && r.date >= from && r.date <= to)
    .map((r) => r.date));

  function apply(value) {
    preset.value = value;
    preset.dispatchEvent(new dom.window.Event("change", { bubbles: true }));
  }

  apply("today");
  await wait(20);
  const tomorrow = new Date(Date.parse(today + "T12:00:00Z") + 86400000).toISOString().slice(0, 10);
  assert.deepEqual([...datesShown()].sort(), [...expectFor(today, today)].sort(), "Today preset shows only today");
  assert.equal(doc.getElementById("date-from").value, today, "Today preset writes the Las Vegas date into From");

  apply("tomorrow");
  await wait(20);
  assert.deepEqual([...datesShown()].sort(), [...expectFor(tomorrow, tomorrow)].sort(), "Tomorrow preset");

  apply("weekend");
  await wait(20);
  const dow = new Date(today + "T12:00:00Z").getUTCDay();
  const toFri = (5 - dow + 7) % 7;
  const fri = new Date(Date.parse(today + "T12:00:00Z") + toFri * 86400000).toISOString().slice(0, 10);
  const sun = new Date(Date.parse(fri + "T12:00:00Z") + 2 * 86400000).toISOString().slice(0, 10);
  assert.deepEqual([...datesShown()].sort(), [...expectFor(fri, sun)].sort(), "This weekend preset spans Fri-Sun");
  assert.equal(doc.getElementById("date-from").value, fri);

  apply("next7");
  await wait(20);
  const plus7 = new Date(Date.parse(today + "T12:00:00Z") + 7 * 86400000).toISOString().slice(0, 10);
  assert.deepEqual([...datesShown()].sort(), [...expectFor(today, plus7)].sort(), "Next 7 days preset");

  apply("next30");
  await wait(20);
  const plus30 = new Date(Date.parse(today + "T12:00:00Z") + 30 * 86400000).toISOString().slice(0, 10);
  assert.deepEqual([...datesShown()].sort(), [...expectFor(today, plus30)].sort(), "Next 30 days preset");

  // ---- reset ---------------------------------------------------------------
  [...doc.querySelectorAll(".filters button")].find((b) => /Reset/.test(b.textContent)).click();
  await wait(20);
  assert.equal(bodyRows().length, all, "Reset restores every row");
  assert.equal(doc.getElementById("date-from").value, "");
  assert.equal([...doc.querySelectorAll(".filters .labels.dates input:checked")].length, 0);
  assert.match(summary(), /No filters active/);

  dom.window.close();
  console.log("check_date_filter: OK (" + allDates.length + " dates, presets and ticked days all narrow the table)");
})().catch((err) => { dom.window.close(); console.error(err); process.exitCode = 1; });
