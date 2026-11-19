"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { JSDOM } = require("jsdom");
const root = path.resolve(__dirname, "..");
const dom = new JSDOM(fs.readFileSync(path.join(root, "pages/calculator.html"), "utf8"), {
  url: "https://example.test/pages/calculator.html",
  runScripts: "dangerously",
  beforeParse(window) {
    window.fetch = async (url) => ({ ok: true, json: async () =>
      JSON.parse(fs.readFileSync(path.resolve(root, "pages", url), "utf8")) });
  }
});
(async () => {
  await new Promise(setImmediate);
  const doc = dom.window.document;
  const result = (label) => [...doc.querySelectorAll("#c-out .box")]
    .find((box) => box.querySelector(".l").textContent.startsWith(label)).querySelector(".n").textContent;
  const set = (id, value) => {
    const el = doc.getElementById("c-" + id);
    el.value = value;
    el.dispatchEvent(new dom.window.Event("input"));
  };
  assert.equal(result("Trip total"), "$2,712.44");
  set("buyin", "125.50");
  assert.equal(result("Trip total"), "$2,537.94");
  set("buyin", "");
  assert.equal(result("Trip total"), "n/a");
  set("entries", "0");
  assert.equal(result("Trip total"), "$2,412.44");
  set("entries", "1.5");
  assert.equal(result("Trip total"), "n/a");
  assert.match(doc.getElementById("c-window").textContent, /not a playable sequence/);
  assert.equal(doc.querySelectorAll("#c-compare tbody tr").length, 1);
  assert.ok(doc.querySelector('#c-compare a[href="https://www.venetianlasvegas.com/book"]'));
  dom.window.close();
  console.log("check_calculator: OK");
})().catch((err) => { dom.window.close(); console.error(err); process.exitCode = 1; });
