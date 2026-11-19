#!/usr/bin/env python3
"""Generate the static GitHub Pages site.

Each page inlines assets/style.css and assets/app.js, so the site needs no
external CDN and no build step beyond this script. Data is read at run time
from data/*.json and the Markdown files in the repo root.
"""
import os
import json
from html import escape

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
<section class="briefing" aria-labelledby="brief-title">
<p class="eyebrow">LAS VEGAS &nbsp;/&nbsp; TRIP BRIEFING</p>
<h1 id="brief-title">The Strip poker planner</h1>
<p>Compare tournament rules, hotel checkout totals and walking routes before committing to a stay.</p>
<form class="home-search" action="pages/search.html"><label for="site-search">Search the research</label><div><input type="search" id="site-search" name="q" placeholder="Tournament, hotel, venue or rule…"><button>Search</button></div></form>
</section>
<div class="decision"><strong>Booking decision: hold</strong><span>No event in the reviewed series has a written whole-event freezeout policy. Hotel prices are dated quotes, not live offers.</span><a href="pages/summary.html">Read the brief →</a></div>
<h2>At a glance</h2><div class="grid" id="kpis"></div>
<h2>Plan your stay</h2><div class="path-grid">
<article class="path"><span class="eyebrow">01 &nbsp; / &nbsp; TOURNAMENTS</span><h3>Check the entry rules</h3><p>Separate a written freezeout from a silent sheet or an event selling more chips.</p><a href="pages/single-entry.html">Freezeout shortlist →</a><a href="pages/separate-section.html">Multiple-entry events</a><a href="pages/unverified.html">Missing rules</a></article>
<article class="path"><span class="eyebrow">02 &nbsp; / &nbsp; SCHEDULE</span><h3>Build a realistic day</h3><p>Compare registration deadlines and conflicts. An alternative replaces the primary; it is not another seat.</p><a href="pages/schedule.html">Day-by-day schedule →</a><a href="pages/daily.html">Morning feed</a><a href="pages/venues.html">Browse venues</a></article>
<article class="path"><span class="eyebrow">03 &nbsp; / &nbsp; LODGING</span><h3>Price the whole trip</h3><p>Use exact dates, occupancy, taxes and mandatory fees. Check the walking route before comparing prices.</p><a href="pages/calculator.html">Trip cost calculator →</a><a href="pages/hotels.html">Hotels and dated rates</a><a href="pages/other-rooms.html">Nearby rooms</a></article></div>
<h2>Decision desk</h2><div class="desk"><a href="pages/questions.html">Open questions</a><a href="pages/suggestions.html">Suggestions</a><a href="pages/monitoring.html">Change monitor</a><a href="pages/flagged.html">Flagged for review</a><a href="pages/strip-rooms.html">Strip survey</a><a href="pages/review.html">Source audit</a></div>
"""),
    "pages/single-entry.html": ("Single entry", "singleEntry", """
<h1>Freezeout shortlist</h1>
<p class="lead">Only written whole-event rules qualify. There are no confirmed rows in this snapshot. Switch off “Written freezeout confirmed” to inspect candidates by date. Today and later uses Las Vegas dates and includes today’s earlier starts; clear it to inspect past events. A silent sheet is not a prohibition.</p>
<div class="card callout">Guarantee ÷ total entry fee describes the advertised pool, not expected winnings. Bounty prizes and satellite seats are not comparable to ordinary cash payouts.</div>
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
<h1>Morning schedule feed</h1>
<p class="lead">Official Strip and nearby room schedules are requested each morning before 8 AM Las Vegas time. Excerpts preserve the source wording; they are not confirmed entries. On a failed request, the last readable capture retains its original date.</p>
<label>Search schedule excerpts <input type="search" id="feed-q" placeholder="Room, time or format"></label>
<div id="feed"></div><h2>Wynn recurring formats</h2>
<p class="lead">Recurring formats the Strip rooms publish: Wynn's dailies, Bellagio's Friday, Saturday and Sunday events, and Caesars Palace's daily tournaments, each read from the room's own official document. The Wynn formats are listed below the schedule feed.</p>
<div class="card callout" id="note"></div>
<div id="content"></div>
<p class="small" id="series-note"></p>
"""),
    "pages/hotels.html": ("Hotels", "hotels", """
<h1>Hotels near the Strip</h1>
<p class="lead">Fee, tax, parking, other mandatory charges, cancellation terms, true cost and routed walking time
for every property. True cost per night is the official booking engine's own checkout total divided by the nights,
so it exists only where a dated quote was captured. Sort by true cost, filter to the hotels within a 30-minute walk
of a poker room, or search any column.</p>
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
<p class="lead">Sheet-reviewed candidates per day, pending written freezeout confirmation, earliest first, with one primary event and a conditional fallback only where a fallback can actually be played.</p>
<div class="card callout">One entry per day is the realistic shape of a single-entry trip. Every Venetian one-day event is estimated at 8h45&ndash;21h05 from its own published level structure, so 10:10 and 11:10 starts are still running after midnight and no later same-date event can follow them. Where that is the case the day says so instead of proposing a sequence that cannot happen. A finish time marked <strong>(next day)</strong> crossed midnight; the estimate is start + published levels, never an official finish time.</div>
<div class="card callout" id="note"></div>
<p class="small">Earliest start among the rows in this dataset: <strong id="earliest"></strong></p>
<p class="small" id="overlap-kpi"></p>
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
<p class="lead">Three things are kept apart on purpose. The <strong>scheduled provenance check</strong> re-fetches every official document from GitHub Actions and reports whether the values printed on it moved. The <strong>row-level check</strong> records which official URL answered, whether each page still prints the values its rows were captured from, and which rows changed since the last snapshot. Every printed source flag is listed below with its source link. A run that reaches nothing at all is labelled a network blackout rather than a source outage.</p>
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
<h1>Flagged for Review</h1>
<div id="content"></div>
"""),
    "pages/strip-rooms.html": ("Strip rooms", "strips", """
<h1>Strip room survey</h1>
<div id="content"></div>
"""),
    "pages/review.html": ("Repo review and sources", "review", """
<h1>Repo review and sources</h1>
<div id="content"></div>
"""),
}

for _file, _title, _vid in VENUE_PAGES:
    PAGES["pages/" + _file] = venue_page(_title, _vid)


# Only properties with a published poker-room record get a room page. No
# lodging is attached on the strength of a similar name or an assumed walk.
with open(os.path.join(ROOT, "data/other_rooms.json"), encoding="utf-8") as source:
    survey = json.load(source)
room_links = []
for room in survey["rooms"]:
    if room["poker_room_status"] != "confirmed" and room["id"] != "resorts-world":
        continue
    slug, name = room["id"], escape(room["name"])
    rel = "room-" + slug + ".html"
    room_links.append(f'<a href="{rel}">{name}</a>')
    PAGES["pages/" + rel] = (name, "roomProfile", f'<h1>{name}</h1><div id="content" data-room="{slug}"></div>')
vt, vp, vb = PAGES["pages/venues.html"]
PAGES["pages/venues.html"] = (vt, vp, vb + '<h2>Additional room profiles</h2><div class="desk">' + ' '.join(room_links) + '</div>')

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
