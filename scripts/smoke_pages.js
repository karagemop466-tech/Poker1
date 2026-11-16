#!/usr/bin/env node
/* Headless smoke test: load every generated page in jsdom, stub fetch with the
   local files, and check that each page rendered its content without errors.

   Usage: node scripts/smoke_pages.js   (requires: npm i --no-save jsdom)
*/
const fs = require("fs");
const path = require("path");
let JSDOM, VirtualConsole;
try {
  ({ JSDOM, VirtualConsole } = require("jsdom"));
} catch (e) {
  console.log("smoke_pages: jsdom is not installed - skipping (npm i --no-save jsdom to enable)");
  process.exit(0);
}

const ROOT = path.resolve(__dirname, "..");
const PAGES = ["index.html"].concat(
  fs.readdirSync(path.join(ROOT, "pages")).sort().map((f) => "pages/" + f)
);

function load(rel) {
  const abs = path.join(ROOT, rel.replace(/^\//, ""));
  if (!fs.existsSync(abs)) return null;
  return fs.readFileSync(abs, "utf8");
}

async function run() {
  let failures = 0;
  for (const page of PAGES) {
    const html = load(page);
    if (html == null) {
      console.log("MISSING " + page);
      failures++;
      continue;
    }
    const errors = [];
    const vc = new VirtualConsole();
    vc.on("jsdomError", (e) => errors.push("jsdomError: " + e.message));
    vc.on("error", (m) => errors.push("console.error: " + m));
    const base = page.includes("/") ? "../" : "./";
    const dom = new JSDOM(html, {
      url: "https://example.github.io/Poker1/" + page,
      runScripts: "dangerously",
      virtualConsole: vc,
      pretendToBeVisual: true,
    });
    const w = dom.window;
    w.fetch = function (url) {
      const rel = String(url).replace(/^https:\/\/example\.github\.io\/Poker1\//, "");
      const resolved = path.normalize(path.join(ROOT, path.dirname(page), rel));
      const relFromRoot = path.relative(ROOT, resolved);
      const text = load(relFromRoot);
      if (text == null) {
        return Promise.resolve({ ok: false, status: 404, json: () => Promise.reject(new Error("404 " + relFromRoot)), text: () => Promise.reject(new Error("404 " + relFromRoot)) });
      }
      return Promise.resolve({
        ok: true,
        status: 200,
        json: () => Promise.resolve(JSON.parse(text)),
        text: () => Promise.resolve(text),
      });
    };
    // run the page script
    await new Promise((resolve) => {
      w.document.addEventListener("DOMContentLoaded", () => setTimeout(resolve, 60));
      if (w.document.readyState === "complete" || w.document.readyState === "interactive") setTimeout(resolve, 60);
    });
    const doc = w.document;
    const content = doc.getElementById("content");
    const nav = doc.querySelector("header.site nav");
    let rendered = "";
    ["#content", "#events", "#hoteltable", "#results", "#calc", "#kpis", "#venuehead"].forEach((sel) => {
      const el = doc.querySelector(sel);
      if (el && el.textContent.trim()) rendered += " " + sel + "(" + el.textContent.trim().length + " chars)";
    });
    const rows = doc.querySelectorAll("tbody tr").length;
    const errText = (content && /Could not load this page/.test(content.textContent)) ? "PAGE LOAD ERROR: " + content.textContent.trim() : "";
    const ok = !!nav && !errors.length && !errText && (rendered.length > 0 || rows > 0);
    if (!ok) failures++;
    console.log(
      (ok ? "OK   " : "FAIL ") + page.padEnd(28) +
      " nav:" + (nav ? "y" : "n") +
      " rows:" + rows +
      " rendered:" + (rendered.trim() || "none") +
      (errors.length ? " | errors: " + errors.join("; ") : "") +
      (errText ? " | " + errText : "")
    );
    dom.window.close();
  }
  console.log(failures ? "\n" + failures + " page(s) failed the smoke test" : "\nAll " + PAGES.length + " pages rendered with no script errors");
  process.exit(failures ? 1 : 0);
}

run().catch((e) => {
  console.error(e);
  process.exit(1);
});
