#!/usr/bin/env python3
"""Check the site: JSON files parse, local links and asset paths exist, and every data row has an https source."""
import json
import os
import re
import sys
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
problems = []
REQUIRED_SITE_DOCS = (
    "EXECUTIVE_SUMMARY.md",
    "QUESTIONS.md",
    "SUGGESTIONS.md",
    "FLAGGED.md",
    "REVIEW.md",
    "IRREGULARITIES.md",
)
OFFICIAL_SOURCE_HOSTS = {
    "www.venetianlasvegas.com",
    "www.wynnlasvegas.com",
    "cdn.wynnresorts.com",
    "aria.mgmresorts.com",
    "bellagio.mgmresorts.com",
    "www.caesars.com",
    # MGM Resorts' own corporate site and asset CDN. assets.contentstack.io is
    # the content store that bellagio.mgmresorts.com serves its own PDFs from.
    "www.mgmresorts.com",
    "assets.contentstack.io",
    # Clark County Nevada is the taxing authority for the room tax applied to
    # every Strip property, so its own licensing list is an official source.
    "www.clarkcountynv.gov",
}

for rel in REQUIRED_SITE_DOCS:
    if not os.path.isfile(os.path.join(ROOT, rel)):
        problems.append(f"{rel}: required Markdown content for the deployed dashboard is missing")

for rel in ("data/tournaments.json", "data/hotels.json", "data/schedule.json",
            "data/hotel_rates.json", "data/venues.json", "data/walking.json",
            "data/source_registry.json", "data/daily_feed.json"):
    path = os.path.join(ROOT, rel)
    if not os.path.isfile(path):
        problems.append(f"{rel}: required data file is missing")
        continue
    try:
        json.load(open(path, encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        problems.append(f"{rel}: {e}")

for rel in ("data/tournaments.json", "data/hotels.json"):
    rows = json.load(open(os.path.join(ROOT, rel), encoding="utf-8"))["rows"]
    for r in rows:
        src = r.get("sources") or []
        if not src or not all(s.get("url", "").startswith("https://") for s in src):
            problems.append(f"{rel}: row {r.get('id', r.get('name'))} lacks an https source")
            continue
        for source in src:
            host = urlparse(source["url"]).hostname
            if host not in OFFICIAL_SOURCE_HOSTS:
                problems.append(f"{rel}: row {r.get('id', r.get('name'))} has a non-approved source host: {host}")

# Every tournament row must be classified, and every row in the single-entry
# section must genuinely be a single-entry freezeout with a read structure sheet.
tournaments = json.load(open(os.path.join(ROOT, "data/tournaments.json"), encoding="utf-8"))["rows"]
for r in tournaments:
    if r.get("section") not in ("single", "other"):
        problems.append(f"data/tournaments.json: row {r.get('id')} has no section classification")
    if r.get("section") == "single":
        if r.get("entry_status") != "SE":
            problems.append(f"data/tournaments.json: row {r.get('id')} is in the single-entry section "
                            f"but its entry status is {r.get('entry_status')}")
        if not r.get("sources"):
            problems.append(f"data/tournaments.json: row {r.get('id')} in the single-entry section has no source")
        if r.get("total_fee_usd") is None:
            problems.append(f"data/tournaments.json: row {r.get('id')} in the single-entry section has no "
                            "confirmed total fee")

schedule = json.load(open(os.path.join(ROOT, "data/schedule.json"), encoding="utf-8"))
for day in schedule.get("days", []):
    for key in ("primary", "fallback"):
        event = day.get(key)
        if not event:
            continue
        url = event.get("source", "")
        if not url.startswith("https://") or urlparse(url).hostname not in OFFICIAL_SOURCE_HOSTS:
            problems.append(f"data/schedule.json: {key} on {day.get('date')} has a non-official source")
    if not day.get("primary"):
        problems.append(f"data/schedule.json: {day.get('date')} has no primary event")

# Walking pairs must be complete for every hotel and every venue.
walking = json.load(open(os.path.join(ROOT, "data/walking.json"), encoding="utf-8"))
hotels = json.load(open(os.path.join(ROOT, "data/hotels.json"), encoding="utf-8"))["rows"]
venues = json.load(open(os.path.join(ROOT, "data/venues.json"), encoding="utf-8"))["venues"]
have = {(p["from"], p["to"]) for p in walking.get("pairs", [])}
for h in hotels:
    for v in venues:
        if h["id"] == v["id"]:
            continue
        if (h["id"], v["id"]) not in have:
            problems.append(f"data/walking.json: missing pair {h['id']} -> {v['id']}")

# The daily feed is optional in a fresh checkout but must be valid when present.
feed_path = os.path.join(ROOT, "data/daily_feed.json")
if os.path.isfile(feed_path):
    feed = json.load(open(feed_path, encoding="utf-8"))
    if "generated_at" not in feed:
        problems.append("data/daily_feed.json: no generated_at timestamp")
    for row in feed.get("rows", []):
        if not row.get("source", "").startswith("https://"):
            problems.append("data/daily_feed.json: a row has no https source")

REQUIRED_DATA_FILES = (
    "tournaments.json", "hotels.json", "schedule.json", "hotel_rates.json",
    "venues.json", "walking.json", "source_registry.json", "daily_feed.json",
)


def check_app_js():
    """Static contract check between assets/app.js and the generated pages.

    Every element the script looks up must exist on at least one page, every
    data-page key it switches on must be emitted by the site generator, and
    every data file it fetches must exist. This catches the failures a headless
    environment cannot catch by loading the page.
    """
    js = open(os.path.join(ROOT, "assets", "app.js"), encoding="utf-8").read()
    app_problems = []

    for rel in REQUIRED_DATA_FILES:
        if not os.path.isfile(os.path.join(ROOT, "data", rel)):
            app_problems.append(f"assets/app.js: data/{rel} is fetched but missing")
    # source_changes.json is written by the scheduled source watch. It is
    # optional in a fresh checkout and the page states plainly when it is
    # absent, so its absence is not an error.
    optional = {"source_changes.json"}
    for name in re.findall(r'getJSON\("data/([^"]+)"\)', js):
        if name in optional:
            continue
        if not os.path.isfile(os.path.join(ROOT, "data", name)):
            app_problems.append(f"assets/app.js: fetches data/{name} which does not exist")

    wanted_ids = set(re.findall(r'getElementById\("([^"]+)"\)', js))
    page_files = ["index.html"] + [os.path.join("pages", f)
                                   for f in sorted(os.listdir(os.path.join(ROOT, "pages")))]
    present_ids = set()
    page_keys = set()
    for p in page_files:
        html = open(os.path.join(ROOT, p), encoding="utf-8").read()
        present_ids |= set(re.findall(r'id="([^"]+)"', html))
        page_keys |= set(re.findall(r'data-page="([^"]+)"', html))
    for i in sorted(wanted_ids - present_ids):
        app_problems.append(f"assets/app.js: looks up #{i} which no page defines")

    handled = set(re.findall(r'case "([^"]+)":', js))
    for k in sorted(page_keys - handled):
        app_problems.append(f"assets/app.js: no handler for data-page='{k}'")
    for k in sorted(handled - page_keys):
        app_problems.append(f"assets/app.js: handles data-page='{k}' which no page emits")

    required_docs = set(re.findall(r'getText\("([^"]+)"\)', js))
    for d in sorted(required_docs):
        if not os.path.isfile(os.path.join(ROOT, d)):
            app_problems.append(f"assets/app.js: reads {d} which does not exist")

    return app_problems


problems.extend(check_app_js())

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
