"""Integration checks for the static site (T7). Exit non-zero on any failure."""
import glob, json, os, re, sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errors = []

# 1. JSON parses and every row has an official source URL
for f in glob.glob(os.path.join(ROOT, "data", "*.json")):
    try:
        json.load(open(f))
    except Exception as e:
        errors.append(f"JSON invalid {f}: {e}")
t = json.load(open(os.path.join(ROOT, "data", "tournaments.json")))
for section in ("main_single_entry", "excluded", "unverified_not_ranked"):
    for r in t[section]:
        srcs = [r.get("source_schedule")] + (r.get("source_structure") if isinstance(r.get("source_structure"), list) else [r.get("source_structure")])
        if not any(s and s.startswith("https://") for s in srcs):
            errors.append(f"{section} row without official link: {r.get('name')}")
for r in t["main_single_entry"]:
    if not (r["source_schedule"].startswith("https://www.venetianlasvegas.com/")):
        errors.append(f"main row source not official Venetian: {r['name']}")

# 2. Internal links resolve
class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.links = []; self.stack = []; self.bad = []
        self.void = {"meta", "link", "br", "img", "input", "hr"}
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag not in self.void:
            self.stack.append(tag)
    def handle_endtag(self, tag):
        if tag in self.void:
            return
        if not self.stack or self.stack[-1] != tag:
            self.bad.append(f"unbalanced </{tag}>, open={self.stack[-1] if self.stack else None}")
        else:
            self.stack.pop()

pages = [os.path.join(ROOT, "index.html")] + glob.glob(os.path.join(ROOT, "pages", "*.html"))
for p in pages:
    text = open(p).read()
    if re.search(r"\bNone\b|\bnan\b", re.sub(r"<[^>]+>", " ", text)):
        errors.append(f"raw None/nan in {os.path.relpath(p, ROOT)}")
    lp = LinkParser(); lp.feed(text)
    if lp.bad or lp.stack:
        errors.append(f"HTML structure issue in {os.path.relpath(p, ROOT)}: {lp.bad[:3]} open={lp.stack[:3]}")
    for href in lp.links:
        if href.startswith(("http://", "https://", "#", "mailto:")):
            continue
        target = os.path.normpath(os.path.join(os.path.dirname(p), href))
        if not os.path.exists(target):
            errors.append(f"broken link in {os.path.relpath(p, ROOT)}: {href}")
    if "stylesheet" in text and "assets/style.css" not in text and "../assets/style.css" not in text:
        errors.append(f"no stylesheet link in {p}")

print(f"pages checked: {len(pages)}; rows: main={len(t['main_single_entry'])} excluded={len(t['excluded'])} unverified={len(t['unverified_not_ranked'])}")
if errors:
    print("FAILURES:"); [print(" -", e) for e in errors]
    sys.exit(1)
print("ALL CHECKS PASSED")
