#!/usr/bin/env python3
"""Generate the static GitHub Pages site.

Each page inlines assets/style.css and assets/app.js, so the site needs no
external CDN and no build step beyond this script. Data is read at run time
from data/*.json and the Markdown files in the repo root.

Run:  python3 scripts/build_site.py
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
<main class="wrap">
{body}
</main>
<footer id="site-footer"></footer>
<script>
{js}
</script>
</body>
</html>
"""

DEFN = """
<div class="card callout defn">
<strong>How to read this site.</strong> Every row links to an official source
(venue or operator domain). A cell is <strong>blank</strong> when the official
source does not state that value &mdash; nothing is inferred or filled in.
<strong>Pool &divide; entry fee</strong> is a descriptive ratio of the published
guarantee to the published buy-in; it is not a forecast of what you will win or
of likely field size. Bounty and multi-flight events are labelled separately.
</div>
"""

PAGES = {
    "index.html": ("Home", "index", """
<h1>Las Vegas Strip Poker Plan</h1>
<p class="lead">Single-entry poker tournaments on the Las Vegas Strip and walkable hotels, checked
line by line against official sources on <strong>2026-11-16</strong>. Blank cells are unverified.
No value is inferred.</p>
""" + DEFN + """
<div class="grid" id="kpis"></div>
<h2>Start here</h2>
<div class="grid">
  <a class="card tile" href="pages/summary.html"><h3>Executive summary</h3><p>Bottom line, ranked events, hotel status, and the 8 AM question.</p></a>
  <a class="card tile" href="pages/single-entry.html"><h3>Single entry (verified)</h3><p>Events whose official structure sheet was read. Sortable, with date filter and search.</p></a>
  <a class="card tile" href="pages/separate-section.html"><h3>Separate section</h3><p>Multi-entry, re-entry and second-buy-in events. Kept out of the ranking.</p></a>
  <a class="card tile" href="pages/schedule.html"><h3>Schedule</h3><p>One primary event per day plus a conditional fallback, with overlaps flagged.</p></a>
  <a class="card tile" href="pages/trip-cost.html"><h3>Trip cost calculator</h3><p>Entries &times; buy-ins + nights &times; true hotel cost per night.</p></a>
  <a class="card tile" href="pages/hotels.html"><h3>Hotels</h3><p>Resort fee, rate status, parking, cancellation and the 30-minute walking test.</p></a>
  <a class="card tile" href="pages/venues.html"><h3>Venues</h3><p>One page per venue: its series, its events, its hotels.</p></a>
  <a class="card tile" href="pages/unverified.html"><h3>Unverified</h3><p>Official rows whose entry rule is not yet confirmed.</p></a>
  <a class="card tile" href="pages/questions.html"><h3>Questions</h3><p>What must be decided, what is missing, and how to close each gap.</p></a>
  <a class="card tile" href="pages/suggestions.html"><h3>Suggestions</h3><p>Site improvements for you to choose from before anything is built.</p></a>
  <a class="card tile" href="pages/changes.html"><h3>Change log</h3><p>Monitored official sources and any recorded change.</p></a>
  <a class="card tile" href="pages/flagged.html"><h3>Flagged for review</h3><p>Source irregularities and blank values, with links.</p></a>
  <a class="card tile" href="pages/review.html"><h3>Repo review and sources</h3><p>Line-by-line review, corrections made, and the source log.</p></a>
</div>
<div class="card callout" style="margin-top:18px">Flags do not block publication. Every flagged item lists its source and is kept on the Flagged for Review page.</div>
"""),

    "pages/single-entry.html": ("Single entry", "singleEntry", """
<h1>Single-entry tournaments (verified)</h1>
<p class="lead">Each row's official structure sheet was read and shows no re-entry, rebuy, add-on or
flight clause. Sort by any column; the default sort is pool &divide; entry fee.</p>
""" + DEFN + """
<div id="controls"></div>
<div id="content"></div>
<p class="small">The Venetian structure sheets do not print an explicit "no re-entry" sentence. The
single-entry verdict is an absence-of-clause finding, so confirm with the poker room before you rely
on it (see question I1).</p>
"""),

    "pages/separate-section.html": ("Separate section", "separate", """
<h1>Separate section: not single entry</h1>
<p class="lead">Multi-flight events, re-entry events, and events whose sheet wording implies a second
buy-in. Kept out of the single-entry ranking.</p>
""" + DEFN + """
<div class="card callout"><strong>Multi-flight rows.</strong> The structure sheet says a player who
bags chips for Day 2 may not play a subsequent flight. It does not say whether a player who busts may
enter a later flight, so a second entry stays possible. Confirm with the poker room.</div>
<div id="controls"></div>
<div id="content"></div>
"""),

    "pages/unverified.html": ("Unverified", "unverified", """
<h1>Unverified official rows</h1>
<p class="lead">Official schedule rows whose structure sheet has not been read. The entry rule is
unknown, so these rows are not ranked and must not be treated as single entry.</p>
""" + DEFN + """
<div id="controls"></div>
<div id="content"></div>
"""),

    "pages/venues.html": ("Venues", "venues", """
<h1>Venues</h1>
<p class="lead">One section per venue, with the series it hosts, how many rows are verified, and the
hotels recorded against it. Use the Hotels page for the walking-distance table.</p>
""" + DEFN + """
<div id="content"></div>
"""),

    "pages/hotels.html": ("Hotels", "hotels", """
<h1>Hotels near the Strip</h1>
<p class="lead">Resort fee, room rate, room tax, parking and cancellation status are shown per hotel.
True cost per night is blank until a dated room rate is verified.</p>
""" + DEFN + """
<div class="card callout" id="method"></div>
<div id="controls"></div>
<div id="content"></div>
<h2>Hotel &rarr; venue walking pairs</h2>
<p class="small">Every hotel&ndash;venue pair, with both official addresses. The 30-minute limit is
applied as soon as a walking time is recorded. No official source publishes a walking time, so every
value is blank today and the test cannot be applied yet.</p>
<div id="pairs"></div>
<h2>Rate log</h2>
<p class="small">Rates are kept as a dated log, not a single value, so price movement across your stay
window is visible. No dated official quote has been captured for any hotel, so the log
(<code>data/hotel_rates.json</code>) is empty. Each future entry records check-in, check-out, nights,
occupancy, nightly rate, resort fee, tax, parking, cancellation deadline, the checkout total, the
nightly average and the rate timestamp, so stays can be compared like for like.</p>
"""),

    "pages/schedule.html": ("Schedule", "schedule", """
<h1>Day-by-day schedule</h1>
<p class="lead">One primary event per day, plus a conditional fallback that does not clash with it.
Overlaps are flagged.</p>
""" + DEFN + """
<div class="card callout" id="method"></div>
<div class="card callout" id="note"></div>
<p class="small">Earliest start anywhere in the dataset: <strong id="earliest"></strong>. Satellites
are excluded; one Venetian satellite starts at 9:10 AM.</p>
<div class="toolbar">
  <label class="small">From <input id="from" type="date"></label>
  <label class="small">To <input id="to" type="date"></label>
  <span id="count" class="small"></span>
</div>
<div id="content"></div>
"""),

    "pages/trip-cost.html": ("Trip cost", "tripCost", """
<h1>Estimated cost of a trip</h1>
<p class="lead">Entries &times; buy-ins + nights &times; true hotel cost per night. Entry fees are
official buy-ins. The hotel half stays blank until a dated official rate is captured.</p>
""" + DEFN + """
<div id="content"></div>
"""),

    "pages/changes.html": ("Change log", "changes", """
<h1>Change monitoring</h1>
<p class="lead">Each official source is re-checked on a schedule. Rows whose source changed are
flagged here and re-verified line by line.</p>
""" + DEFN + """
<div class="card callout" id="method"></div>
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
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
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
