/* S16 gate: the print-friendly views must stay real, not aspirational.

   Three things are checked on every run (and therefore on every PR):
   1. assets/style.css keeps a working @media print block: the interactive chrome
      is dropped, table header rows repeat sheet to sheet, no row/card splits
      across a page break, headings do not strand themselves, and every external
      link prints its URL so a paper copy still carries the official sources.
   2. assets/app.js keeps the "Print this page" control for the two paper-first
      views (schedule and single-entry) and nowhere else.
   3. The control actually renders and fires window.print when the two pages are
      run in a headless DOM - and does NOT appear on the home page.

   Run with: node scripts/check_print_views.js */
"use strict";
const fs = require("fs");
const path = require("path");
const { JSDOM } = require("jsdom");

const ROOT = path.resolve(__dirname, "..");
const problems = [];

function read(rel) { return fs.readFileSync(path.join(ROOT, rel), "utf8"); }

/* ---- 1. the stylesheet ------------------------------------------------- */
const css = read("assets/style.css");
const printIdx = css.indexOf("@media print");
if (printIdx < 0) {
  problems.push("style.css: no @media print block at all");
} else {
  const block = css.slice(printIdx);
  const need = [
    ["chrome dropped", /header\.site[^}]*display:\s*none/],
    ["filter/search chrome dropped", /#filters[^}]*display:\s*none|\.filters[^}]*display:\s*none/],
    ["buttons dropped", /button\s*\{\s*display:\s*none\s*!important/],
    ["page margins", /@page\s*\{/],
    ["table headers repeat", /thead\s*\{\s*display:\s*table-header-group/],
    ["rows never split", /tr,\s*li,\s*\.card[^}]*page-break-inside:\s*avoid/],
    ["headings do not strand", /h1,\s*h2,\s*h3\s*\{\s*page-break-after:\s*avoid/],
    ["source URLs printed on paper", /attr\(href\)/],
    ["colour chips survive B&W", /\.chip\s*\{[^}]*current(Color|border)/],
  ];
  for (const [label, re] of need) {
    if (!re.test(block)) problems.push("style.css @media print: missing " + label);
  }
}

/* ---- 2. the control ----------------------------------------------------- */
const app = read("assets/app.js");
if (!/window\.print\(\)/.test(app)) problems.push("app.js: no window.print() call");
if (!/page === "schedule" \|\| page === "singleEntry"/.test(app)) {
  problems.push("app.js: print control is not gated to schedule + single-entry");
}
if (!/addPrintControl/.test(app)) problems.push("app.js: addPrintControl missing");

/* ---- 3. it renders and fires ------------------------------------------- */
function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }

async function checkPage(rel, expectButton) {
  const html = read(rel);
  const errors = [];
  const dom = new JSDOM(html, {
    url: "https://example.test/" + rel,
    runScripts: "dangerously",
    pretendToBeVisual: true,
    beforeParse(window) {
      window.addEventListener("error", (e) => errors.push(String(e.error || e.message)));
      window.print = () => { window.__printed = (window.__printed || 0) + 1; };
      window.fetch = (url) => {
        const clean = String(url).replace(/^\.\//, "");
        const target = path.join(ROOT, path.dirname(rel), clean);
        return Promise.resolve({
          ok: fs.existsSync(target),
          status: fs.existsSync(target) ? 200 : 404,
          json: () => Promise.resolve(JSON.parse(fs.readFileSync(target, "utf8"))),
          text: () => Promise.resolve(fs.readFileSync(target, "utf8")),
        });
      };
    },
  });
  await sleep(600);
  const doc = dom.window.document;
  const btn = doc.getElementById("s16-print");
  if (errors.length) problems.push(rel + ": page errors: " + errors.join(" | "));
  if (expectButton && !btn) problems.push(rel + ": #s16-print control did not render");
  if (!expectButton && btn) problems.push(rel + ": print control must not appear here");
  if (btn && expectButton) {
    btn.click();
    await sleep(50);
    if (!dom.window.__printed) problems.push(rel + ": clicking the control did not call window.print()");
    if (btn.type !== "button") problems.push(rel + ": control must be type=button (not a submit)");
  }
  dom.window.close();
}

(async () => {
  await checkPage("pages/schedule.html", true);
  await checkPage("pages/single-entry.html", true);
  await checkPage("index.html", false);
  if (problems.length) {
    console.error("check_print_views: FAIL");
    for (const p of problems) console.error("  - " + p);
    process.exit(1);
  }
  console.log("check_print_views: OK (print stylesheet rules present; schedule + single-entry render a working print control; other pages do not)");
})();
