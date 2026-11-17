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

FILTERS = '<div id="filters"></div>'
COUNT = '<span id="count" class="small"></span>'

VENUE_PAGES = [
    ("venue-venetian.html", "The Venetian Resort", "venetian"),
    ("venue-wynn.html", "Wynn Las Vegas", "wynn"),
    ("venue-aria.html", "ARIA Resort & Casino", "aria"),
    ("venue-bellagio.html", "Bellagio", "bellagio"),
    ("venue-caesars.html", "Caesars Palace", "caesars"),
]


def venue_page(title, venue_id):
    return (title, "venue:" + venue_id, """
<h1>%s</h1>
<p class="lead">Everything in this dataset that belongs to this venue, with the official source behind each row.</p>
<div id="content"></div>
<h2>Hotels here</h2>
<div id="hotels"></div>
<h2>Walking records</h2>
<div id="walking"></div>
<h2>Tournaments</h2>
%s
<div class="toolbar"><span class="small">%s</span></div>
<div id="events"></div>
""" % (title, FILTERS, COUNT))


PAGES = {
    "index.html": ("Home", "index", """
<h1>Las Vegas Strip Poker Plan</h1>
<p class="lead">Single-entry tournaments and walkable hotels, every official source re-checked on 2026-11-17. Blank cells are unverified. No value is inferred.</p>
<div class="grid" id="kpis"></div>
<h2>Start here</h2>
<div class="grid">
  <a class="card tile" href="pages/summary.html"><h3>Executive summary</h3><p>Bottom line, ranked events, hotel status, and the 8 AM question.</p></a>
  <a class="card tile" href="pages/single-entry.html"><h3>Single entry (verified)</h3><p>Every event whose official structure sheet, read clause by clause, contains no re-entry, rebuy, add-on or flight clause. The basis is printed on every row.</p></a>
  <a class="card tile" href="pages/separate-section.html"><h3>Separate section</h3><p>Possible multiple entries and re-entry events. Kept out of the ranking.</p></a>
  <a class="card tile" href="pages/unverified.html"><h3>Unverified</h3><p>Official rows whose entry rule is not yet confirmed.</p></a>
  <a class="card tile" href="pages/daily.html"><h3>Daily feed</h3><p>Wynn's recurring daily tournaments: format, guarantee, fee split and cut-offs.</p></a>
  <a class="card tile" href="pages/schedule.html"><h3>Schedule</h3><p>Day-by-day verified single-entry options, with a date picker.</p></a>
  <a class="card tile" href="pages/hotels.html"><h3>Hotels</h3><p>Resort fees, room-rate status, walking records and the dated rate log.</p></a>
  <a class="card tile" href="pages/calculator.html"><h3>Trip cost calculator</h3><p>Entries × buy-in + nights × true hotel cost + parking, from dated official-engine quotes. Nothing is assumed.</p></a>
  <a class="card tile" href="pages/venues.html"><h3>Venues</h3><p>Each poker room, the hotels attached to it and the events played there.</p></a>
  <a class="card tile" href="pages/search.html"><h3>Search</h3><p>One box across every row, hotel, venue, document and rate on the site.</p></a>
  <a class="card tile" href="pages/monitoring.html"><h3>Monitoring</h3><p>Source health, changed rows and every printed source flag.</p></a>
  <a class="card tile" href="pages/questions.html"><h3>Questions</h3><p>Open decisions and information gaps, with how to close each.</p></a>
  <a class="card tile" href="pages/suggestions.html"><h3>Suggestions</h3><p>Site improvements for your review.</p></a>
  <a class="card tile" href="pages/flagged.html"><h3>Flagged for review</h3><p>Source irregularities and blank values, with links.</p></a>
  <a class="card tile" href="pages/review.html"><h3>Repo review and sources</h3><p>Line-by-line review, corrections made, and the source log.</p></a>
</div>
<div class="card callout" style="margin-top:18px">Flags do not block publication. Every flagged item lists its source and is kept on the Flagged for Review page.</div>
"""),
    "pages/single-entry.html": ("Single entry", "singleEntry", """
<h1>Single-entry tournaments (verified)</h1>
<p class="lead">Each row has its structure sheet read, with no re-entry, rebuy, add-on, or flight clause. Guarantee ÷ buy-in is the default sort. Use the filters to narrow by date, venue, series, buy-in or label.</p>
<div class="card callout">How the single-entry label is decided: the event's own official structure sheet was read clause by clause and contains <strong>no re-entry, rebuy, add-on or multi-flight clause</strong>. No Venetian sheet prints an affirmative "single entry" sentence, so this is single entry <strong>by absence of contrary terms</strong>, not a written maximum-entry promise — each row prints the exact basis with its sheet link. Anything with printed re-entry, limited-entry or flight language is in the separate section, not here.</div>
""" + FILTERS + """
<div class="toolbar"><span class="small">""" + COUNT + """</span></div>
<div id="content"></div>
"""),
    "pages/separate-section.html": ("Separate section", "separate", """
<h1>Separate section: not single entry</h1>
<p class="lead">Possible multiple entries (multi-flight events) and re-entry events. Kept out of the single-entry ranking.</p>
<div class="card callout">Multi-flight rows: the structure sheet says a player who bags Day 2 chips may not play a subsequent flight. It does not say whether a player who busts may enter a later flight. Confirm with the poker room.</div>
""" + FILTERS + """
<div class="toolbar"><span class="small">""" + COUNT + """</span></div>
<div id="content"></div>
"""),
    "pages/unverified.html": ("Unverified", "unverified", """
<h1>Unverified official rows</h1>
<p class="lead">Official schedule rows whose structure sheet has not been read. Entry rule unknown. Not ranked.</p>
""" + FILTERS + """
<div class="toolbar"><span class="small">""" + COUNT + """</span></div>
<div id="content"></div>
"""),
    "pages/daily.html": ("Daily feed", "daily", """
<h1>Wynn daily tournament feed</h1>
<p class="lead">The recurring formats Wynn publishes for every day, read from the official daily structures.</p>
<div class="card callout" id="note"></div>
<div id="content"></div>
<p class="small" id="series-note"></p>
"""),
    "pages/hotels.html": ("Hotels", "hotels", """
<h1>Hotels near the Strip</h1>
<p class="lead">Fee, tax, true cost and routed walking time for every property. True cost per night is the official booking engine's own checkout total divided by the nights, so it exists only where a dated quote was captured.</p>
<div class="card callout" id="method"></div>
<div id="content"></div>
<p class="small">No property publishes a walking time, so these are routed on the OSM foot network, not quoted from an official source (F49). Minutes are rounded up and the 30-minute rule is applied.</p>
<div id="walking"></div>
<div id="rates"></div>
<p class="small"><a href="calculator.html">Price a trip with the trip cost calculator →</a></p>
"""),
    "pages/calculator.html": ("Trip cost calculator", "calculator", """
<h1>Trip cost calculator</h1>
<p class="lead">Price a whole trip: tournament entries x buy-in, plus nights x true hotel cost, plus parking. The hotel side is bound to the dated rate log, so a stay is priced from an official booking-engine quote rather than an assumed rate. Anything unverified stays blank and is reported as missing, never guessed.</p>
<div id="content"></div>
"""),
    "pages/schedule.html": ("Schedule", "schedule", """
<h1>Day-by-day schedule</h1>
<p class="lead">Verified single-entry options per day, earliest first.</p>
<div class="card callout" id="note"></div>
<p class="small">Earliest start among the rows in this dataset: <strong id="earliest"></strong></p>
<div id="content"></div>
"""),
    "pages/venues.html": ("Venues", "venues", """
<h1>Venues</h1>
<p class="lead">Every property in this dataset, the hotels attached to it, and how many verified rows it carries.</p>
<div id="content"></div>
"""),
    "pages/search.html": ("Search", "search", """
<h1>Search</h1>
<p class="lead">One box across every tournament row, hotel, venue, daily format, walking record, rate log entry and document on this site.</p>
<div class="toolbar"><input id="q" type="search" placeholder="Search everything, for example: milestone, ante up, pokeratlas, 13.38" style="min-width:320px"></div>
<p class="small" id="summary"></p>
<div id="results"></div>
"""),
    "pages/monitoring.html": ("Monitoring", "monitoring", """
<h1>Source monitoring</h1>
<p class="lead">Which official sources answered on the last check, which rows changed since the last snapshot, and every printed source flag.</p>
<div id="content"></div>
<h2>Rows carrying a source flag</h2>
<div id="flagged"></div>
<h2>Source status</h2>
<div id="sources"></div>
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

for _file, _title, _vid in VENUE_PAGES:
    PAGES["pages/" + _file] = venue_page(_title, _vid)


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
