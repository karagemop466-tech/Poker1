#!/usr/bin/env python3
"""Generate the static GitHub Pages site.

Each page inlines assets/style.css and assets/app.js, so the site needs no
external CDN and no build step beyond this script. Data is read at run time
from data/*.json and the Markdown files in the repo root.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
DATA = os.path.join(ROOT, "data")

CSS = open(os.path.join(ASSETS, "style.css"), encoding="utf-8").read()
JS = open(os.path.join(ASSETS, "app.js"), encoding="utf-8").read()

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Las Vegas Strip Poker Plan</title>
<meta name="description" content="{desc}">
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

TOOLBAR = (
    '<div class="toolbar">'
    '<label class="field"><span>Search</span>'
    '<input id="q" type="search" placeholder="Event, series, venue, note, buy-in"></label>'
    '<label class="field"><span>From</span><input id="from" type="date"></label>'
    '<label class="field"><span>To</span><input id="to" type="date"></label>'
    '<label class="field"><span>Venue</span><select id="venue"></select></label>'
    '<label class="field"><span>Format</span><select id="format"></select></label>'
    '<label class="field check"><input id="seOnly" type="checkbox">'
    '<span>Single entry confirmed only</span></label>'
    '<span id="count" class="small count"></span>'
    '<button id="reset" type="button" class="btn">Reset</button>'
    '</div>'
)

PAGES = {}


def page(rel, title, key, body, desc=""):
    PAGES[rel] = (title, key, body, desc)


page(
    "index.html", "Home", "index",
    """
<h1>Las Vegas Strip Poker Plan</h1>
<p class="lead">Official Strip poker tournaments and walkable hotels, checked against official sources.
Every row links to the document it was read from. Blank means unconfirmed, and nothing is inferred.</p>
<div class="grid" id="kpis"></div>
<h2>Plan</h2>
<div class="grid">
  <a class="card tile" href="pages/summary.html"><h3>Executive summary</h3><p>What is confirmed, what is not, and the recommended shape of a trip.</p></a>
  <a class="card tile" href="pages/single-entry.html"><h3>Single entry (verified)</h3><p>Confirmed single-entry freezeouts with their fee, stack, levels and cutoff.</p></a>
  <a class="card tile" href="pages/other-formats.html"><h3>Separate formats</h3><p>Re-entry, multi-flight, bounty, satellite and team formats, grouped by reason.</p></a>
  <a class="card tile" href="pages/unverified.html"><h3>Unverified</h3><p>Official rows whose entry rule is not yet confirmed from a structure sheet.</p></a>
  <a class="card tile" href="pages/venues.html"><h3>Venues</h3><p>One page per poker room: address, series, and the events held there.</p></a>
  <a class="card tile" href="pages/schedule.html"><h3>Schedule</h3><p>Date by date: one primary event and one conditional fallback.</p></a>
  <a class="card tile" href="pages/hotels.html"><h3>Hotels</h3><p>Resort fee, tax, parking, cancellation, occupancy, and computed walk times.</p></a>
  <a class="card tile" href="pages/hotel-rates.html"><h3>Hotel rate log</h3><p>Dated, append-only observations. Like-for-like comparison only.</p></a>
  <a class="card tile" href="pages/cost.html"><h3>Trip cost</h3><p>Entries times buy-ins plus nights times the true nightly hotel cost.</p></a>
  <a class="card tile" href="pages/daily.html"><h3>Daily feed</h3><p>Live official daily poker-room schedules, refreshed by a scheduled job.</p></a>
</div>
<h2>Review material</h2>
<div class="grid">
  <a class="card tile" href="pages/questions.html"><h3>Questions and gaps</h3><p>Open questions, what is missing, and how to close each one.</p></a>
  <a class="card tile" href="pages/suggestions.html"><h3>Suggestions</h3><p>Improvements for review. Nothing here is applied without a decision.</p></a>
  <a class="card tile" href="pages/flagged.html"><h3>Flagged for review</h3><p>Every blank and every flagged value, with its source.</p></a>
  <a class="card tile" href="pages/irregularities.html"><h3>Irregularity log</h3><p>Typos and contradictions found in official documents.</p></a>
  <a class="card tile" href="pages/sources.html"><h3>Official sources</h3><p>Every official URL this site depends on.</p></a>
  <a class="card tile" href="pages/review.html"><h3>Repo review</h3><p>What changed in this pass, and what was corrected.</p></a>
</div>
<div class="card callout" style="margin-top:18px">Flagged and unverified items are published rather than hidden.
They do not block the merge, and each one names the document that would settle it.</div>
""",
    "Official Las Vegas Strip poker tournament and hotel planner.",
)

page(
    "pages/single-entry.html", "Single entry", "singleEntry",
    """
<h1>Single-entry tournaments (verified)</h1>
<p class="lead">Each row below was read from its official structure sheet, and that sheet contains no
re-entry, rebuy, add-on, subsequent-buy-in or multi-flight clause. One entry, one seat, one buy-in.
The prize structure is a separate matter: a bounty or a satellite is still a single-entry event, so those
rows stay here and the <strong>Format</strong> filter sets them aside. The guarantee divided by the
buy-in is a descriptive ratio of two published numbers, not a forecast of what you will receive.</p>
<div class="card callout">The house fee is <strong>withheld from</strong> the buy-in, not added to it. A
$300 buy-in with $58 withheld for house fees puts $242 into the prize pool, and $300 is what you commit
to enter.</div>
""" + TOOLBAR + """
<div id="content"></div>
""",
    "Verified single-entry freezeout poker tournaments on the Las Vegas Strip.",
)

page(
    "pages/other-formats.html", "Separate formats", "otherFormats",
    """
<h1>Separate formats</h1>
<p class="lead">Everything that is not a confirmed single-entry event, grouped by the reason it is
separated. These are legal to play and are shown in full, but they are not ranked against single-entry
events because more than one entry can be taken, the event is a continuation you have already paid for,
or the rule has not been confirmed from a structure sheet.</p>
<div class="tabs" id="formatTabs"></div>
""" + TOOLBAR + """
<div id="content"></div>
""",
    "Re-entry, multi-flight, Day 2 restart and unverified poker tournaments.",
)

page(
    "pages/unverified.html", "Unverified", "unverified",
    """
<h1>Unverified official rows</h1>
<p class="lead">Rows that come from an official schedule, but whose entry rule has not been confirmed
from an official structure sheet. Nothing in this table is ranked and no value is inferred.</p>
""" + TOOLBAR + """
<div id="content"></div>
""",
    "Official poker tournament rows whose entry rule is not yet verified.",
)

page(
    "pages/venues.html", "Venues", "venues",
    """
<h1>Venues</h1>
<p class="lead">Each poker room on this plan, with its official address, the series held there, and a
link to its official page.</p>
<div id="content"></div>
""",
    "Poker room venues on the Las Vegas Strip.",
)

page(
    "pages/schedule.html", "Schedule", "schedule",
    """
<h1>Day-by-day schedule</h1>
<p class="lead">One primary event and, where one exists that does not overlap, one conditional fallback
for each date. Ranking happens only after the total fee and the guarantee are confirmed from an official
structure sheet.</p>
<div class="toolbar">
  <label class="field"><span>Search</span><input id="q" type="search" placeholder="Event, series, venue"></label>
  <label class="field"><span>From</span><input id="from" type="date"></label>
  <label class="field"><span>To</span><input id="to" type="date"></label>
  <label class="field check"><input id="seOnly" type="checkbox"><span>Single entry confirmed only</span></label>
  <span id="count" class="small count"></span>
  <button id="reset" type="button" class="btn">Reset</button>
</div>
<div class="card callout" id="note"></div>
<div id="content"></div>
""",
    "Date-by-date Las Vegas poker schedule with a primary and a fallback event.",
)

page(
    "pages/hotels.html", "Hotels", "hotels",
    """
<h1>Hotels near the Strip</h1>
<p class="lead">Mandatory resort fee, Clark County room tax, parking, cancellation deadline and occupancy
come from each property's own official terms. Walking times are computed with an open pedestrian routing
service and can be confirmed in Google Maps or Apple Maps before you book.</p>
<div class="toolbar">
  <label class="field"><span>Venue to walk to</span><select id="venue"></select></label>
  <label class="field check"><input id="walkOnly" type="checkbox"><span>Only hotels within 30 minutes on foot</span></label>
  <label class="field"><span>Search</span><input id="q" type="search" placeholder="Hotel name, address, note"></label>
  <span id="count" class="small count"></span>
  <button id="reset" type="button" class="btn">Reset</button>
</div>
<div class="card callout" id="method"></div>
<div id="content"></div>
""",
    "Las Vegas Strip hotels with resort fee, tax, parking, cancellation and walking times.",
)

page(
    "pages/hotel-rates.html", "Hotel rate log", "hotelRates",
    """
<h1>Hotel rate log</h1>
<p class="lead">An append-only record. One row per observation of one stay, never an overwrite. Each row
records the room rate, the same-stay checkout total, the nightly average, the mandatory resort fee and
tax, parking, the cancellation deadline, the occupancy and the rate timestamp, each with its own flag.</p>
<div class="card callout" id="method"></div>
<div class="toolbar">
  <label class="field"><span>Search</span><input id="q" type="search" placeholder="Hotel, date, note"></label>
  <span id="count" class="small count"></span>
  <button id="reset" type="button" class="btn">Reset</button>
</div>
<div id="content"></div>
""",
    "Dated hotel rate log with like-for-like comparison.",
)

page(
    "pages/cost.html", "Trip cost", "cost",
    """
<h1>Estimated trip cost</h1>
<p class="lead">Entries times buy-ins, plus nights times the true nightly hotel cost. The hotel component
stays blank until a date-specific room rate is confirmed; the tournament component is fully sourced.</p>
<div class="grid two">
  <div class="card">
    <h3>Tournament entries</h3>
    <div id="entryList"></div>
    <button id="addEntry" type="button" class="btn">Add an entry</button>
    <p class="small">Entries are chosen from the published tournaments. Each one uses its official buy-in.</p>
  </div>
  <div class="card">
    <h3>Hotel</h3>
    <label class="field"><span>Property</span><select id="hotel"></select></label>
    <label class="field"><span>Nights</span><input id="nights" type="number" min="1" value="6"></label>
    <label class="field"><span>Adults</span><input id="adults" type="number" min="1" value="1"></label>
    <p class="small" id="hotelNote"></p>
  </div>
</div>
<div class="card" id="result"></div>
""",
    "Estimate the cost of a Las Vegas poker trip: entries plus hotel nights.",
)

page(
    "pages/daily.html", "Daily feed", "daily",
    """
<h1>Official daily poker-room schedules</h1>
<p class="lead">A live feed scraped from the official daily poker-room pages and posters. Each row names
the document it came from and the moment it was retrieved.</p>
<div class="toolbar">
  <label class="field"><span>Search</span><input id="q" type="search" placeholder="Event, venue, format"></label>
  <label class="field"><span>Venue</span><select id="venue"></select></label>
  <span id="count" class="small count"></span>
  <button id="reset" type="button" class="btn">Reset</button>
</div>
<div class="card callout" id="note"></div>
<div id="content"></div>
""",
    "Live official daily poker-room schedules for the Las Vegas Strip.",
)

page(
    "pages/sources.html", "Official sources", "sources",
    """
<h1>Official sources</h1>
<p class="lead">Every official document this site depends on, with what it was used for and how often it
should be re-checked. A scheduled job watches these URLs and flags any that change.</p>
<div class="toolbar">
  <label class="field"><span>Search</span><input id="q" type="search" placeholder="Label, URL, kind"></label>
  <span id="count" class="small count"></span>
  <button id="reset" type="button" class="btn">Reset</button>
</div>
<div id="content"></div>
""",
    "Official source register for the Las Vegas Strip poker plan.",
)

for _key, _title, _page, _body, _desc in (
    ("summary", "Executive summary", "summary", "<h1>Executive summary</h1>\n<div id=\"content\"></div>", "Executive summary of the Las Vegas Strip poker plan."),
    ("questions", "Questions and gaps", "questions", "<h1>Questions, information, and answers</h1>\n<div id=\"content\"></div>", "Open questions and information gaps."),
    ("suggestions", "Suggestions", "suggestions", "<h1>Improvement suggestions for review</h1>\n<div id=\"content\"></div>", "Suggestions for improving the poker planner."),
    ("flagged", "Flagged for review", "flagged", "<h1>Flagged for review</h1>\n<p class=\"lead\">Published so each item can be reviewed. Flags do not block the merge.</p>\n<div id=\"content\"></div>", "Flagged values and gaps in the poker planner."),
    ("irregularities", "Irregularity log", "irregularities", "<h1>Irregularity log</h1>\n<p class=\"lead\">Typos and contradictions found in official documents, and how each was handled.</p>\n<div id=\"content\"></div>", "Irregularities found in official poker and hotel documents."),
    ("review", "Repo review", "review", "<h1>Repository review</h1>\n<div id=\"content\"></div>", "Review of the poker planner repository."),
):
    page("pages/%s.html" % _key, _title, _page, _body, _desc)


def venue_pages():
    with open(os.path.join(DATA, "venues.json"), encoding="utf-8") as f:
        venues = json.load(f)["venues"]
    for v in venues:
        page(
            "pages/venue-%s.html" % v["id"],
            v["name"],
            "venue",
            """
<h1>{name}</h1>
<p class="lead">{address}</p>
<div class="card callout" id="venueNote"></div>
<div class="grid" id="venueStats"></div>
""" .format(name=v["name"], address=v["address"]) + TOOLBAR + """
<div id="content"></div>
""",
            "%s - poker venue on the Las Vegas Strip." % v["name"],
        )


def write(rel, title, key, body, desc):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path) or ROOT, exist_ok=True)
    html = TEMPLATE.format(title=title, page=key, body=body.strip(), desc=desc, css=CSS, js=JS)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


def main():
    venue_pages()
    for rel, (title, key, body, desc) in PAGES.items():
        write(rel, title, key, body, desc)
        print("wrote", rel)


if __name__ == "__main__":
    main()
