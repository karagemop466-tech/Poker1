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
  const tablePages = ["singleEntry", "separate", "unverified", "hotels", "daily"];
  const markdownPages = ["summary", "questions", "suggestions", "flagged", "review"];
  const problems = [];
  if (errors.length) problems.push("js error: " + errors.join(" | "));
  if (html_out.indexOf("Could not load") >= 0) problems.push("page reported a load error");
  if (!html_out || html_out.length < 40) problems.push("page rendered no content");
  if (tablePages.indexOf(page) >= 0 && doc.querySelectorAll("table").length === 0) {
    problems.push("no table rendered");
  }
  if (page.indexOf("venue:") === 0 && doc.querySelectorAll("table").length === 0) {
    problems.push("no table rendered");
  }
  // Doubled-title guard: the page template prints the one and only <h1>. A
  // markdown body that renders its own top heading duplicates it (the defect
  // found on pages/flagged.html, session 206debc0).
  const h1Count = doc.querySelectorAll("h1").length;
  if (h1Count !== 1) problems.push("expected exactly 1 <h1>, found " + h1Count);
  if (markdownPages.indexOf(page) >= 0 && doc.getElementById("content") &&
      doc.getElementById("content").querySelectorAll("h1").length !== 0) {
    problems.push("markdown body rendered an <h1> inside #content (doubled title)");
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
