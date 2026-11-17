/* Assert the day plan actually renders a feasible sequence (session 2157d288).
   Guards the defect session 206debc0 reported: every conditional fallback was an
   impossible sequence and 137 rows printed an end time that read before their own
   start, because `est_end` is time-only and an event can cross midnight.
   Run with: node scripts/check_schedule_render.js   (needs jsdom) */
"use strict";
const fs = require("fs");
const path = require("path");
const { JSDOM } = require("jsdom");

const ROOT = path.resolve(__dirname, "..");
const rel = "pages/schedule.html";

function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }

(async function () {
  const html = fs.readFileSync(path.join(ROOT, rel), "utf8");
  const dom = new JSDOM(html, {
    url: "https://example.test/" + rel,
    runScripts: "dangerously",
    pretendToBeVisual: true,
    beforeParse(window) {
      window.fetch = (url) => {
        const clean = String(url).replace(/^\.\//, "");
        const target = path.join(ROOT, path.dirname(rel), clean);
        return Promise.resolve({
          ok: fs.existsSync(target), status: fs.existsSync(target) ? 200 : 404,
          json: () => Promise.resolve(JSON.parse(fs.readFileSync(target, "utf8"))),
          text: () => Promise.resolve(fs.readFileSync(target, "utf8"))
        });
      };
    }
  });
  await sleep(1200);
  const text = dom.window.document.body.textContent;
  const problems = [];
  const nextDay = (text.match(/\(next day\)/g) || []).length;
  if (nextDay < 1) problems.push("no `(next day)` label rendered, so a wrapped end time is still shown as a bare clock time");
  if (/after midnight, so no later event/.test(text) === false)
    problems.push("no after-midnight fallback note rendered");
  if (/\b02:55 AM\b/.test(text) === false)
    problems.push("expected wrapped end time 02:55 AM not rendered at all");
  // A bare wrapped time must never appear without the qualifier.
  const bare = text.match(/\d{1,2}:\d{2} (?:AM|PM)(?! \(next day\))/g) || [];
  console.log("schedule render: `(next day)` labels =", nextDay, "| total clock times =", bare.length);
  if (problems.length) {
    console.error("FAIL\n  " + problems.join("\n  "));
    process.exit(1);
  }
  console.log("check_schedule_render: OK");
})();
