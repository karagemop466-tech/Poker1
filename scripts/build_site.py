#!/usr/bin/env python3
"""Generate the static GitHub Pages site.

Each page inlines assets/style.css and assets/app.js, so the site needs no
external CDN and no build step beyond this script. Data is read at run time
from data/*.json and the Markdown files in the repo root.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

CSS = open(os.path.join(ASSETS, "style.css"), encoding="utf-8").read()
JS = open(os.path.join(ASSETS, "app.js"), encoding="utf-8").read()

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Las Vegas Strip Poker Plan</title>
<style>
{css}
</style>
</head>
<body data-page="{page}">
<div id="site-header"></div>
<main>
{body}
</main>
<footer id="site-footer"></footer>
<script>
{js}
</script>
</body>
</html>
"""

TOOLBAR_SEARCH = ('<div class="toolbar"><input id="q" type="search" placeholder="Filter rows (event, series, note)">'
                  '<select id="series"></select><span id="count" class="small"></span></div>')
TOOLBAR_SEARCH_NO_SERIES = ('<div class="toolbar"><input id="q" type="search" placeholder="Filter rows (event, series, note)">'
                            '<span id="count" class="small"></span></div>')

PAGES = {
    "index.html": ("Home", "index", """
<h1>Las Vegas Strip Poker Plan</h1>
<p class="lead">Single-entry tournaments and walkable hotels, checked against official sources on 2026-11-16. Blank cells are unverified. No value is inferred.</p>
<div class="grid" id="kpis"></div>
<h2>Start here</h2>
<div class="grid">
  <a class="card tile" href="pages/summary.html"><h3>Executive summary</h3><p>Bottom line, ranked events, hotel status, and the 8 AM question.</p></a>
  <a class="card tile" href="pages/single-entry.html"><h3>Single entry (verified)</h3><p>33 Venetian events. Sortable table with official source links.</p></a>
  <a class="card tile" href="pages/separate-section.html"><h3>Separate section</h3><p>Possible multiple entries and re-entry events. Kept out of the ranking.</p></a>
  <a class="card tile" href="pages/hotels.html"><h3>Hotels</h3><p>Resort fees, room-rate status, and true cost. Rates are blank until verified.</p></a>
  <a class="card tile" href="pages/schedule.html"><h3>Schedule</h3><p>Day-by-day verified single-entry options. Starts from 10:10 AM.</p></a>
  <a class="card tile" href="pages/unverified.html"><h3>Unverified</h3><p>Official rows whose entry rule is not yet confirmed.</p></a>
  <a class="card tile" href="pages/questions.html"><h3>Questions</h3><p>Open decisions and information gaps, with how to close each.</p></a>
  <a class="card tile" href="pages/suggestions.html"><h3>Suggestions</h3><p>Site improvements for your review. None implemented.</p></a>
  <a class="card tile" href="pages/flagged.html"><h3>Flagged for review</h3><p>Source irregularities and blank values, with links.</p></a>
  <a class="card tile" href="pages/review.html"><h3>Repo review and sources</h3><p>Line-by-line review, corrections made, and the source log.</p></a>
</div>
<div class="card callout" style="margin-top:18px">Flags do not block publication. Every flagged item lists its source and is kept on the Flagged for Review page.</div>
"""),
    "pages/single-entry.html": ("Single entry", "singleEntry", """
<h1>Single-entry tournaments (verified)</h1>
<p class="lead">Each row has its structure sheet read, with no re-entry, rebuy, add-on, or flight clause. Sort by any column. Guarantee ÷ buy-in is the default sort.</p>
""" + TOOLBAR_SEARCH + """
<div id="content"></div>
"""),
    "pages/separate-section.html": ("Separate section", "separate", """
<h1>Separate section: not single entry</h1>
<p class="lead">Possible multiple entries (multi-flight events) and re-entry events. Kept out of the single-entry ranking.</p>
<div class="card callout">Multi-flight rows: the structure sheet says a player who bags Day 2 chips may not play a subsequent flight. It does not say whether a player who busts may enter a later flight. Confirm with the poker room.</div>
""" + TOOLBAR_SEARCH_NO_SERIES + """
<div id="content"></div>
"""),
    "pages/unverified.html": ("Unverified", "unverified", """
<h1>Unverified official rows</h1>
<p class="lead">Official schedule rows whose structure sheet has not been read. Entry rule unknown. Not ranked.</p>
""" + TOOLBAR_SEARCH + """
<div id="content"></div>
"""),
    "pages/hotels.html": ("Hotels", "hotels", """
<h1>Hotels near the Strip</h1>
<p class="lead">Resort fee and room-rate status are shown per hotel. True cost per night is blank until a room rate is verified.</p>
<div class="card callout" id="method"></div>
<div id="content"></div>
<p class="small">Walking time to each venue is not published on any official source, so it is blank.</p>
"""),
    "pages/schedule.html": ("Schedule", "schedule", """
<h1>Day-by-day schedule</h1>
<p class="lead">Verified single-entry options per day, earliest first.</p>
<div class="card callout" id="note"></div>
<p class="small">Earliest start among the rows in this dataset: <strong id="earliest"></strong></p>
<div id="content"></div>
"""),
    "pages/summary.html": ("Executive summary", "summary", """
<h1>Executive summary</h1>
<div id="content"></div>
"""),
    "pages/questions.html": ("Questions", "questions", """
<h1>Questions and information gaps</h1>
<div id="content"></div>
"""),
    "pages/suggestions.html": ("Suggestions", "suggestions", """
<h1>Suggestions for site improvement</h1>
<div id="content"></div>
"""),
    "pages/flagged.html": ("Flagged for review", "flagged", """
<h1>Flagged for review</h1>
<p class="lead">Published so you can review each item. Flags do not block the merge.</p>
<div id="content"></div>
"""),
    "pages/review.html": ("Repo review and sources", "review", """
<h1>Repo review and sources</h1>
<div id="content"></div>
"""),
}


def write(rel, title, page, body):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    html = TEMPLATE.format(title=title, page=page, body=body.strip(), css=CSS, js=JS)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


def main():
    for rel, (title, page, body) in PAGES.items():
        write(rel, title, page, body)
        print("wrote", rel)


if __name__ == "__main__":
    main()
