/* Smoke test: load every generated page in jsdom, let the app render, and
   fail if a page throws, logs an error, or renders nothing.

   Run with:  node scripts/smoke_test.js
   Requires jsdom (npm install jsdom). The test is optional - the site itself
   has no runtime dependency on it. */
"use strict";
const fs = require("fs");
const path = require("path");
const { JSDOM } = require("jsdom");

const ROOT = path.resolve(__dirname, "..");
const PAGE_DIR = path.join(ROOT, "pages");

const pages = ["index.html"].concat(
  fs.readdirSync(PAGE_DIR).filter((f) => f.endsWith(".html")).map((f) => path.join("pages", f))
);

function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }

async function run(rel) {
  const file = path.join(ROOT, rel);
  const html = fs.readFileSync(file, "utf8");
  const errors = [];
  const dom = new JSDOM(html, {
    url: "https://example.test/" + rel,
    runScripts: "dangerously",
    pretendToBeVisual: true,
    beforeParse(window) {
      window.addEventListener("error", (e) => errors.push(String(e.error || e.message)));
      const origError = window.console.error;
      window.console.error = (...args) => { errors.push(args.map(String).join(" ")); origError.apply(window.console, args); };
      window.fetch = (url) => {
        const clean = String(url).replace(/^\.\//, "");
        const target = path.join(ROOT, path.dirname(rel), clean);
        return Promise.resolve({
          ok: fs.existsSync(target),
          status: fs.existsSync(target) ? 200 : 404,
          json: () => Promise.resolve(JSON.parse(fs.readFileSync(target, "utf8"))),
          text: () => Promise.resolve(fs.readFileSync(target, "utf8"))
        });
      };
    }
  });
  const { window } = dom;
  await sleep(600);
  const doc = window.document;
  const page = doc.body.getAttribute("data-page");
  const primary = page === "index" ? doc.getElementById("kpis")
    : (page === "search" ? doc.getElementById("results") : doc.getElementById("content"));
  const html_out = primary ? primary.innerHTML : "";
  const problems = [];
  if (page === "schedule") {
    /* The defect this check exists for: an event that runs past midnight has an estimated
       finish that reads as EARLIER than its start. If the render ever drops the next-day
       marker, a reader is told an 11:10 event finishes at 2:55 in the morning of the same
       day, and the day plan below it inverts. So every rendered event line is re-read. */
    const TIME = /\b(\d{1,2}):(\d{2})\s*(AM|PM)/g;
    const toMin = (m) => {
      let h = parseInt(m[1], 10) % 12;
      if (m[3] === "PM") h += 12;
      return h * 60 + parseInt(m[2], 10);
    };
    let inverted = 0;
    doc.querySelectorAll("#content li").forEach((li) => {
      const txt = li.textContent.replace(/\s+/g, " ").trim();
      const starts = [...txt.matchAll(TIME)];
      const at = txt.search(/(finish about|at most|no later than)\s/);
      if (!starts.length || at < 0) return;
      const ends = [...txt.slice(at).matchAll(TIME)];
      if (!ends.length) return;
      if (toMin(ends[0]) < toMin(starts[0]) && !/next day/.test(txt.slice(at, at + 120))) inverted++;
    });
    if (inverted) {
      problems.push(inverted + " rendered event line(s) show a finish before their start with no next-day marker");
    }
    if (html_out.indexOf("Alternatives on this date") < 0) {
      problems.push("schedule page renders no alternatives block although the data carries them");
    }
    if (/impossible sequence is proposed/.test(html_out)) {
      problems.push("schedule page still claims no impossible sequence is proposed without proving it");
    }
  }
  const tablePages = ["singleEntry", "separate", "unverified", "hotels", "daily"];

  if (errors.length) problems.push("js error: " + errors.join(" | "));
  if (html_out.indexOf("Could not load") >= 0) problems.push("page reported a load error");
  if (!html_out || html_out.length < 40) problems.push("page rendered no content");
  if (tablePages.indexOf(page) >= 0 && doc.querySelectorAll("table").length === 0) {
    problems.push("no table rendered");
  }
  if (page.indexOf("venue:") === 0 && doc.querySelectorAll("table").length === 0) {
    problems.push("no table rendered");
  }
  dom.window.close();
  return problems;
}

(async function main() {
  let failed = 0;
  for (const rel of pages) {
    const problems = await run(rel);
    if (problems.length) {
      failed++;
      console.log("FAIL  " + rel + "\n      " + problems.join("\n      "));
    } else {
      console.log("ok    " + rel);
    }
  }
  console.log("\nsmoke_test: " + (pages.length - failed) + "/" + pages.length + " pages rendered");
  process.exit(failed ? 1 : 0);
})();
