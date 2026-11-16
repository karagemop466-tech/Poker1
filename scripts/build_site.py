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
<title>{title} · Vegas Poker Trip Planner</title>
<meta name="description" content="Source-verified Las Vegas Strip poker tournaments, hotel costs and a day-by-day plan. Every value links to an official operator document.">
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

# Shared toolbars -------------------------------------------------------------
TOOLBAR = ('<div class="toolbar">'
           '<input id="q" type="search" placeholder="Search all columns (event, series, venue, note, source)">'
           '<label>From <input id="from" type="date"></label>'
           '<label>To <input id="to" type="date"></label>'
           '<select id="series"></select>'
           '<button class="chipbtn" id="flights-only" aria-pressed="false" title="Show only rows that are a starting flight">Flights only</button>'
           '<span id="count" class="small"></span>'
           '</div>')

TOOLBAR_PLAIN = ('<div class="toolbar">'
                 '<input id="q" type="search" placeholder="Search all columns (event, series, venue, note, source)">'
                 '<label>From <input id="from" type="date"></label>'
                 '<label>To <input id="to" type="date"></label>'
                 '<select id="series"></select>'
                 '<span id="count" class="small"></span>'
                 '</div>')

PRINCIPLES = ('<div class="card callout">Every row carries a link to the official operator document it came '
              'from. A value that the official document does not print is left blank and marked unverified. '
              'Nothing is inferred, filled in or averaged.</div>')

PAGES = {
"index.html": ("Home", "index", """
<h1>Las Vegas Strip poker trip planner</h1>
<p class="lead">Single-entry tournaments at The Venetian and Wynn, the hotels you can stay in, and the true nightly
cost of each. Every figure on this site comes from an official operator document, and every table row links to it.</p>
<div class="grid" id="kpis"></div>
<div class="card" id="headline"></div>
<h2>Start here</h2>
<div class="grid">
  <a class="card tile" href="pages/tournaments.html"><h3>All tournaments</h3><p>Every official row, with the entry rule, house fee, guarantee and last-checked date. Search and date filter.</p></a>
  <a class="card tile" href="pages/single-entry.html"><h3>Single entry only</h3><p>Events whose official structure sheet prints no re-entry, rebuy, add-on or multi-flight clause.</p></a>
  <a class="card tile" href="pages/separate-section.html"><h3>Multi-entry, kept separate</h3><p>Events that print re-entry, a multi-flight clause or an add-on. Never ranked with the single-entry set.</p></a>
  <a class="card tile" href="pages/schedule.html"><h3>Day-by-day plan</h3><p>One primary event a day plus a conditional fallback that the primary can realistically be abandoned for.</p></a>
  <a class="card tile" href="pages/cost.html"><h3>Trip cost calculator</h3><p>Entries &times; buy-in plus nights &times; true hotel cost, with each input labelled by its source.</p></a>
  <a class="card tile" href="pages/venues.html"><h3>Venues</h3><p>One page per venue: the poker room, its series, its hotels, and what is verified.</p></a>
  <a class="card tile" href="pages/hotels.html"><h3>Hotels</h3><p>Resort fee, room tax, parking, cancellation terms and the dated rate log.</p></a>
  <a class="card tile" href="pages/changes.html"><h3>Source monitor</h3><p>Every official URL, its content hash, and whether it changed since the first check.</p></a>
  <a class="card tile" href="pages/summary.html"><h3>Executive summary</h3><p>Bottom line, the ranking method, and what is still unknown.</p></a>
  <a class="card tile" href="pages/questions.html"><h3>Questions</h3><p>Every open question, the information needed, and how to get it.</p></a>
  <a class="card tile" href="pages/suggestions.html"><h3>Suggestions</h3><p>Proposed improvements, each with the decision it would unlock. Nothing implemented without your choice.</p></a>
  <a class="card tile" href="pages/flagged.html"><h3>Flagged for review</h3><p>Source irregularities and blank values, each with its official link.</p></a>
</div>
""" + PRINCIPLES + """
<h2>How the numbers are built</h2>
<div class="card">
<ul>
  <li><strong>Entry rule.</strong> A row is single entry only when its official structure sheet prints no re-entry,
  rebuy, add-on, multiple-entry or starting-flight clause. The clause text is quoted on the row.</li>
  <li><strong>House fee.</strong> Taken from the sheet's own fee sentence, e.g. "$58 of the $300 Buy-In is withheld
  for house fees". Blank when the sheet does not print it.</li>
  <li><strong>Guarantee &divide; buy-in</strong> is a descriptive ratio of two printed numbers. It is not a forecast
  of profit or of field size.</li>
  <li><strong>Hotel true cost</strong> = (dated room rate + mandatory resort fee) &times; (1 + room tax). It stays
  blank until a rate is attached to a stay date on an official page.</li>
  <li><strong>Walking time</strong> is not published on any official source, so the 30-minute test is unverified
  for every hotel. Only same-building stays are confirmed.</li>
</ul>
</div>
"""),

"pages/tournaments.html": ("All tournaments", "tournaments", """
<h1>All tournaments</h1>
<p class="lead">Every official row in the dataset. Sort by any column, search anything, and narrow by date or series.
The <strong>Entry rule</strong> column is decided from the official structure sheet only.</p>
""" + TOOLBAR + """
<div id="content"></div>
<p class="small">Rows on a tinted background are built on an official document that has changed since it was first
checked. See the <a href="changes.html">source monitor</a>.</p>
"""),

"pages/single-entry.html": ("Single entry", "singleEntry", """
<h1>Single-entry tournaments (verified)</h1>
<p class="lead">Each of these rows has its official structure sheet read, and that sheet prints no re-entry, rebuy,
add-on, multiple-entry or starting-flight clause. Sorted by guaranteed pool &divide; buy-in.</p>
""" + TOOLBAR + """
<div id="content"></div>
<div class="card callout" style="margin-top:14px">Guarantee &divide; buy-in compares two printed numbers so you can
see which events post the largest guaranteed pool per dollar of entry. It is a descriptive ratio, not a forecast.
Bounty events are marked where the guarantee includes the bounties.</div>
"""),

"pages/separate-section.html": ("Multi-entry", "separate", """
<h1>Separate section: not single entry</h1>
<p class="lead">Events that print re-entry, a buy-in after the initial buy-in, or a multi-flight clause. They are
kept out of the single-entry ranking on purpose: spending more money can change your position in these.</p>
""" + TOOLBAR_PLAIN + """
<div id="content"></div>
<div class="card callout" style="margin-top:14px">A multi-flight row is one where the official sheet prints "any
player who bags chips for Day 2 may not play a subsequent flight". The sheet does not say that a player who busts
may buy in again, so the row is not counted as single entry and is not counted as confirmed re-entry either.</div>
"""),

"pages/unverified.html": ("Unverified", "unverified", """
<h1>Unverified rows</h1>
<p class="lead">Official schedule rows whose entry rule is not yet confirmed from an official structure sheet.
The rule is left blank. Not ranked, not recommended.</p>
""" + TOOLBAR_PLAIN + """
<div id="content"></div>
<p class="small">These rows still carry their official source link, so you can read the schedule yourself. The
reason each row is unverified is in the <strong>Official source</strong> and rule columns.</p>
"""),

"pages/schedule.html": ("Day plan", "schedule", """
<h1>Day-by-day plan</h1>
<p class="lead">For each day: the earliest verified single-entry event as the <strong>primary</strong>, and a later
event as a <strong>conditional fallback</strong> only when the primary's estimated finish leaves at least 30 minutes
before the fallback starts.</p>
<div class="card callout" id="note"></div>
<div class="toolbar">
  <label>From <input id="from" type="date"></label>
  <label>To <input id="to" type="date"></label>
  <span id="daycount" class="small"></span>
</div>
<div id="content"></div>
"""),

"pages/venues.html": ("Venues", "venues", """
<h1>Venues</h1>
<p class="lead">One section per venue: the poker room, the series it hosts, the hotels in the same building, and
what is verified about each.</p>
<div id="content"></div>
"""),

"pages/hotels.html": ("Hotels", "hotels", """
<h1>Hotels and their true nightly cost</h1>
<p class="lead">Mandatory resort fee, room rate, room tax, parking and cancellation terms, each with a status and
an official link. True cost is blank until a dated official rate exists.</p>
<div class="card callout" id="method"></div>
<div id="content"></div>
<h2>Dated rate log</h2>
<p class="lead">Rates are kept as a dated log, not a single value, so a later check can show what changed.</p>
<div class="card callout" id="method2"></div>
<div id="content-rates"></div>
"""),

"pages/cost.html": ("Trip cost", "cost", """
<h1>Trip cost calculator</h1>
<p class="lead">Estimated cost = (entries &times; buy-in) + (nights &times; true hotel cost per night), where the true
hotel cost is (room rate + mandatory resort fee) &times; (1 + room tax). The hotel side stays blank until you enter a
dated official rate, because no official dated rate has been published that this project could verify.</p>
<div class="card">
  <div class="toolbar">
    <label style="flex:1 1 100%">Event <select id="eventpick" style="width:100%"></select></label>
  </div>
  <div class="toolbar">
    <label>Entries <input id="entries" type="number" min="1" step="1" placeholder="e.g. 5"></label>
    <label>Nights <input id="nights" type="number" min="0" step="1" placeholder="e.g. 4"></label>
    <button class="chipbtn" id="reset">Reset</button>
  </div>
  <div class="toolbar">
    <label>Official room rate / night <input id="rate" type="number" min="0" step="0.01"></label>
    <label>Mandatory resort fee / night <input id="fee" type="number" min="0" step="0.01" value="55"></label>
    <label>Room tax % <input id="tax" type="number" min="0" step="0.01" value="13.38"></label>
  </div>
  <p class="small">The $55 resort fee and 13.38% room tax are pre-filled because both are printed on official
  <a href="https://www.venetianlasvegas.com/legal/hotel-terms-and-conditions.html" target="_blank" rel="noopener">Venetian
  hotel terms</a>. They are pre-filled for The Venetian only; change them for any other property. The room rate is
  deliberately empty: no official dated rate has been verified, and a figure from a third-party site is not used.</p>
  <div class="calc-out" id="result"></div>
</div>
<div class="card callout">The calculator never invents a hotel rate. If the official sites publish a dated rate you
can verify, type it in and the total is computed with the same formula the site documents, so you can check the
arithmetic by hand.</div>
"""),

"pages/changes.html": ("Source monitor", "changes", """
<h1>Source monitor</h1>
<p class="lead">A scheduled workflow re-checks every official URL, stores a hash of the visible content of each
document, and records the result. A row whose source changed is tinted in the tournament tables.</p>
<div class="grid" id="kpis"></div>
<div class="card callout">The hash is taken over the document's visible text, so a change in page markup or a
rotating token is not reported as a content change. If a document cannot be fetched, the previous facts are kept
and the run is logged as unreachable. Values are never replaced with a guess.</div>
<div class="toolbar">
  <input id="q" type="search" placeholder="Filter documents">
  <span id="count" class="small"></span>
</div>
<div id="content"></div>
"""),

"pages/summary.html": ("Summary", "summary", """
<h1>Executive summary</h1>
<div id="content"></div>
"""),

"pages/questions.html": ("Questions", "questions", """
<h1>Questions and information gaps</h1>
<p class="lead">Every question that has to be answered before a booking decision, with what is known, what is
missing, and how the missing piece can be obtained.</p>
<div id="content"></div>
"""),

"pages/suggestions.html": ("Suggestions", "suggestions", """
<h1>Suggestions</h1>
<p class="lead">Proposed changes to this site, each with the decision it would unlock and the cost of doing it.
Nothing here has been implemented without your choice.</p>
<div id="content"></div>
"""),

"pages/flagged.html": ("Flagged", "flagged", """
<h1>Flagged for review</h1>
<p class="lead">Source irregularities and values that could not be verified, each with the official link so you can
check it yourself. Nothing here blocks the site: it is published so you can review it.</p>
<div id="content"></div>
"""),

"pages/review.html": ("Sources and review", "review", """
<h1>Repo review and source log</h1>
<div id="content"></div>
"""),
}


def write(rel, title, page, body):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path) or ROOT, exist_ok=True)
    html = TEMPLATE.format(title=title, page=page, body=body.strip(), css=CSS, js=JS)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


def main():
    # remove pages that are no longer generated, so the site cannot keep a stale page
    keep = {os.path.basename(p) for p in PAGES if p.startswith("pages/")}
    pages_dir = os.path.join(ROOT, "pages")
    if os.path.isdir(pages_dir):
        for f in sorted(os.listdir(pages_dir)):
            if f.endswith(".html") and f not in keep:
                os.unlink(os.path.join(pages_dir, f))
                print("removed stale page", f)
    for rel, (title, page, body) in PAGES.items():
        write(rel, title, page, body)
        print("wrote", rel)


if __name__ == "__main__":
    main()
