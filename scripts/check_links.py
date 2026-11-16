#!/usr/bin/env python3
"""Check the site: JSON files parse, local links and asset paths exist, and every data row has an https source."""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
problems = []

for rel in ("data/tournaments.json", "data/hotels.json", "data/schedule.json"):
    try:
        json.load(open(os.path.join(ROOT, rel), encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        problems.append(f"{rel}: {e}")

for rel in ("data/tournaments.json", "data/hotels.json"):
    rows = json.load(open(os.path.join(ROOT, rel), encoding="utf-8"))["rows"]
    for r in rows:
        src = r.get("sources") or []
        if not src or not all(s.get("url", "").startswith("https://") for s in src):
            problems.append(f"{rel}: row {r.get('id', r.get('name'))} lacks an https source")

pages = ["index.html"] + [os.path.join("pages", f) for f in sorted(os.listdir(os.path.join(ROOT, "pages")))]
for p in pages:
    html = open(os.path.join(ROOT, p), encoding="utf-8").read()
    static = re.sub(r"<script>[\s\S]*?</script>", "", html)  # only static markup; scripts build links at run time
    for href in re.findall(r'href="([^"#]+)"', static):
        if href.startswith(("http://", "https://", "mailto:")):
            continue
        target = os.path.normpath(os.path.join(os.path.dirname(os.path.join(ROOT, p)), href))
        if not os.path.exists(target):
            problems.append(f"{p}: broken local link {href}")
    if re.search(r'<(link|script)[^>]+src=|<link[^>]+href="https?:', static):
        problems.append(f"{p}: external asset reference")

if problems:
    print("\n".join(problems))
    sys.exit(1)
print(f"check_links: OK ({len(pages)} pages, JSON and source checks passed)")
