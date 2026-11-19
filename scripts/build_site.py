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
<h2>Decision desk</h2><div class="desk"><a href="pages/questions.html">Open questions</a><a href="pages/suggestions.html">Suggestions</a><a href="pages/payouts.html">Payout rules</a><a href="pages/monitoring.html">Change monitor</a><a href="pages/flagged.html">Flagged for review</a><a href="pages/evidence-audit.html">Evidence audit</a><a href="pages/strip-rooms.html">Strip survey</a><a href="pages/review.html">Source audit</a></div>
"""),
    "pages/single-entry.html": ("Single entry", "singleEntry", """
<h1>Freezeout shortlist</h1>
<p class="lead">Only written whole-event rules qualify. There are no confirmed rows in this snapshot. Switch off “Written freezeout confirmed” to inspect candidates by date. Today and later uses Las Vegas dates and includes today’s earlier starts; clear it to inspect past events. A silent sheet is not a prohibition.</p>
<div class="card callout">Guarantee ÷ total entry fee describes the advertised pool, not expected winnings. Bounty prizes and satellite seats are not comparable to ordinary cash payouts. <a href="payouts.html">Every sheet's printed payout rule, line by line →</a></div>
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
    # Session d8a1f37f: the independent evidence audit. Every figure on this page is
    # produced by scripts/audit_entry_labels.py; the page only lays out its record.
    "pages/evidence-audit.html": ("Evidence audit", "evidenceAudit", """
<h1>Evidence audit</h1>
<p class="lead">An independent check of the single most consequential value in the dataset:
whether each event is really single entry, and whether the sentence a row quotes is really on the
document it cites. Built by <code>scripts/audit_entry_labels.py</code> from <code>data/entry_evidence_audit.json</code>.</p>
<div id="content"></div>
"""),
    # Session dd06081b: the requirement-by-requirement audit page.
    "pages/requirements.html": ("Requirement coverage", "requirements", """
<h1>Requirement coverage audit</h1>
<p class="lead">Every line of the brief, examined one at a time and marked done, partial or blocked, with
the file that implements it, the page where it can be seen and the official source behind any value.
A requirement is never marked done because something similar exists: it is marked done when a reader
can check it on this site, and blocked when no official source answers it.
<strong>Blocked</strong> always names the question that would close it, and <strong>partial</strong>
always names the limit.</p>
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

# --- Payout rules page (session 97fc7805 / S18 / P4) -----------------------
# Fully static: every quote was extracted from the archived official snapshot
# by scripts/extract_payouts.py, and scripts/check_links.py re-derives each
# quote from its recorded snapshot lines on every build, so a quote that does
# not appear in its snapshot fails the build instead of reaching the page.
import payout_rows  # noqa: E402  scripts/ is sys.path[0] when run as a script

payout_bundle = payout_rows.load_bundle(ROOT)

with open(os.path.join(ROOT, "data", "tournaments.json"), encoding="utf-8") as _stream:
    _payout_tournament_rows = json.load(_stream)["rows"]
with open(os.path.join(ROOT, "data", "daily.json"), encoding="utf-8") as _stream:
    _payout_daily_rows = json.load(_stream)["rows"]

# Rows whose official source moved since the last scheduled re-check carry the
# same badge the tournament tables print (data/changes.json).
try:
    with open(os.path.join(ROOT, "data", "changes.json"), encoding="utf-8") as _stream:
        _payout_changed_ids = {entry.get("id")
                               for entry in json.load(_stream).get("changed", [])}
except (OSError, ValueError):  # noqa: PERF203 - badge is optional, page is not
    _payout_changed_ids = set()


def _payout_chip(status):
    return '<span class="chip %s">%s</span>' % (
        payout_rows.CHIP_CLASS[status], escape(payout_rows.STATUS_TEXT[status]))


def _snapshot_rel(doc):
    return os.path.relpath(os.path.join(ROOT, doc["snapshot"]),
                           os.path.join(ROOT, "pages"))


def _line_span(clause):
    if clause["line_count"] == 1:
        return "line %d" % clause["line"]
    return "lines %d-%d" % (clause["line"], clause["line"] + clause["line_count"] - 1)


def _quote_html(clause, doc):
    text = escape(clause["text"]).replace("\n", "<br>")
    return ('<div class="small" style="margin:4px 0">“%s” '
            '<a href="%s">%s snapshot · %s</a></div>') % (
        text, escape(_snapshot_rel(doc)), escape(doc["id"]), escape(_line_span(clause)))


def _money(value):
    if value in (None, ""):
        return ""
    if float(value) == int(value):
        return "$" + format(int(value), ",d")
    return "$" + format(value, ",.2f")


def _mult(value):
    if value in (None, ""):
        return ""
    text = format(value, ",.1f").rstrip("0").rstrip(".")
    return text + "x"


def _first_source_link(row):
    sources = row.get("sources") or []
    if not sources:
        return ""
    source = sources[0]
    return '<a class="small" href="%s">%s</a>' % (
        escape(str(source.get("url", ""))), escape(str(source.get("label", ""))[:90]))


def _cited_structure_link(row):
    for source in row.get("sources") or []:
        if "structure" in str(source.get("label", "")).lower():
            return '<a class="small" href="%s">structure PDF cited by the row</a>' % escape(
                str(source.get("url", "")))
    return ""


def _payout_tr(row):
    state = payout_rows.classify_tournament_row(row, payout_bundle)
    status = state["status"]
    badge = ('<br><span class="chip bad">source changed - re-check</span>'
             if row.get("id") in _payout_changed_ids else "")
    event = escape(row["name"]) + badge + "<br>" + _first_source_link(row)

    rule_cell = _payout_chip(status)
    for clause in state["rules"]:
        rule_cell += _quote_html(clause, state["doc"])
    comp_cell = ""
    for clause in state["composition"]:
        comp_cell += _quote_html(clause, state["doc"])
    if not comp_cell:
        comp_cell = '<span class="small">—</span>'

    doc = state["doc"]
    if doc:
        spans = [_line_span(clause)
                 for clause in state["rules"] + state["composition"]]
        sheet = ('<a href="%s">Official structure document</a><br>'
                 '<a class="small" href="%s">archived snapshot · %s</a>') % (
            escape(doc["source_url"]), escape(_snapshot_rel(doc)),
            escape(", ".join(dict.fromkeys(spans))))
    elif status == "sheet-placeholder":
        sheet = (_cited_structure_link(row) +
                 '<br><span class="small">The official structures PDF on file '
                 'prints only a COMING SOON placeholder, so no payout rule can '
                 'be quoted from it.</span>')
    elif status == "sheet-unmapped":
        sheet = (_cited_structure_link(row) +
                 '<br><span class="small">The row cites the structures PDF, but '
                 'its printed title did not map to exactly one structure block. '
                 'Not guessed.</span>')
    else:
        sheet = ('<span class="small">No structure sheet is linked on this row, '
                 'so no payout rule is published for it. The official row source '
                 'is linked under the event name.</span>')

    labels = " · ".join(escape(str(label)) for label in (row.get("labels") or []))
    return ('<tr data-row="%s" data-status="%s">'
            '<td>%s</td>'
            '<td>%s</td>'
            '<td>%s</td>'
            '<td>%s</td>'
            '<td>%s</td>'
            '<td>%s</td>'
            '<td>%s</td>'
            '<td>%s</td>'
            '<td>%s</td>'
            '<td>%s</td>'
            '<td>%s</td>'
            '<td><span class="small">%s</span></td>'
            '</tr>') % (
        escape(str(row.get("id", ""))), escape(status),
        escape(row.get("date", "")),
        escape(row.get("start", "")),
        event,
        escape(row.get("venue", "")),
        _money(row.get("buy_in_usd")),
        _money(row.get("guarantee_usd")),
        _mult(row.get("gtd_multiple")),
        labels or "—",
        rule_cell,
        comp_cell,
        sheet,
        escape(str(row.get("last_checked", ""))),
    )


def _daily_payout_tr(row):
    state = payout_rows.classify_daily_row(row, payout_bundle)
    status = state["status"]
    rule_cell = _payout_chip(status)
    for clause in state["rules"]:
        rule_cell += _quote_html(clause, state["doc"])
    for clause in state["composition"]:
        rule_cell += ('<div class="small" style="margin:4px 0"><em>Composition:</em> “%s” '
                      '<a href="%s">%s snapshot · %s</a></div>') % (
            escape(clause["text"]).replace("\n", "<br>"),
            escape(_snapshot_rel(state["doc"])), escape(state["doc"]["id"]),
            escape(_line_span(clause)))

    source_url = row.get("source_url") or row.get("source") or ""
    source_label = row.get("source_label") or "Official source document"
    source_cell = '<a href="%s">%s</a>' % (
        escape(source_url), escape(source_label))
    doc = state["doc"]
    if doc:
        spans = dict.fromkeys(_line_span(clause)
                              for clause in state["rules"] + state["composition"])
        source_cell += ('<br><a class="small" href="%s">archived snapshot · %s</a>') % (
            escape(_snapshot_rel(doc)), escape(", ".join(spans)))

    labels = " · ".join(escape(str(label)) for label in (row.get("labels") or []))
    return ('<tr data-row="%s" data-status="%s">'
            '<td>%s</td><td>%s</td><td>%s<br><span class="small">%s · starts %s</span></td>'
            '<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><span class="small">%s</span></td>'
            '</tr>') % (
        escape(str(row.get("id", ""))), escape(status),
        escape(row.get("days", "")),
        escape(row.get("venue", "")),
        escape(row.get("name", "")), labels or "—", escape(str(row.get("start", ""))),
        _money(row.get("buy_in_usd")),
        _money(row.get("guarantee_usd")),
        rule_cell,
        source_cell,
        escape(str(row.get("retrieved_on", ""))),
    )


def _payout_counts(rows, classifier):
    counts = {}
    for row in rows:
        status = classifier(row, payout_bundle)["status"]
        counts[status] = counts.get(status, 0) + 1
    return counts


def _payout_legend(counts):
    parts = []
    for status in sorted(counts, key=lambda s: -counts[s]):
        parts.append("%d %s" % (counts[status], payout_rows.STATUS_TEXT[status].lower()))
    return '<div class="toolbar"><span class="small">' + " · ".join(parts) + "</span></div>"


def _caesars_matrix_html():
    doc = payout_bundle["docs_by_id"]["c_daily_flyer"]
    matrix = next(clause for clause in doc["clauses"] if clause["kind"] == "prize-table")
    return """
<h2>Caesars Palace daily flyer: printed payout matrix</h2>
<div class="card">
<p class="small">Reproduced verbatim from the archived capture of the room's own
daily flyer. The text extraction prints the heading &ldquo;Payouts&rdquo; after the
table; the table itself starts at line %d. Percentages are the flyer's own
place-by-field-size ladder &mdash; this page does not convert them into dollar
amounts. <a href="%s">Official flyer</a> · <a href="%s">archived snapshot · %s</a></p>
<pre style="white-space:pre-wrap;font-size:12.5px;margin:8px 0">%s</pre>
</div>""" % (
        matrix["line"],
        escape(doc["source_url"]),
        escape(_snapshot_rel(doc)),
        escape(_line_span(matrix)),
        escape(matrix["text"]),
    )


def _payout_body():
    tournament_sorted = sorted(
        _payout_tournament_rows,
        key=lambda r: (r.get("date", ""), r.get("start", ""),
                       r.get("event_no") if isinstance(r.get("event_no"), int) else -1,
                       r.get("name", "")))
    daily_sorted = sorted(_payout_daily_rows,
                          key=lambda r: (r.get("venue", ""), r.get("start", ""), r.get("id", "")))
    tournament_counts = _payout_counts(_payout_tournament_rows,
                                       payout_rows.classify_tournament_row)
    daily_counts = _payout_counts(_payout_daily_rows,
                                  payout_rows.classify_daily_row)
    return """
<h1>Payout rules</h1>
<p class="lead">What each official structure document actually prints about who
gets paid, quoted line by line with the source document and the archived
snapshot behind every sentence. A sheet that prints no payout rule says so;
nothing on this page is inferred, and a blank means the document was silent,
not that a value was assumed.</p>
<div class="card callout">Guarantee ÷ total entry fee is descriptive of the
advertised pool, not a forecast of winnings. Bounty prizes and satellite seats
are not comparable to ordinary cash payouts, and a payout percentage of the
field is not a dollar ladder. <a href="single-entry.html">Freezeout shortlist →</a></div>
<div class="card callout">Every quote below was collected by
<code>scripts/extract_payouts.py</code> from the official-document snapshots in
<code>data/snapshots/</code>, each carrying the exact lines it came from.
<code>scripts/check_links.py</code> re-derives every quote from those lines on
each build and fails the build on a mismatch, so a quote that is not on the
document cannot be published.</div>
<div id="content">
<h2>Tournament rows (%d)</h2>
%s
<div class="table-wrap"><table class="data">
<thead><tr><th>Date</th><th>Start</th><th>Event</th><th>Venue</th><th>Buy-in</th>
<th>Guarantee</th><th>Guarantee ÷ buy-in</th><th>Labels</th><th>Payout rule</th>
<th>Prize-pool composition</th><th>Structure sheet</th><th>Last checked</th></tr></thead>
<tbody>
%s
</tbody></table></div>
<h2>Daily recurring formats (%d)</h2>
<p class="small">The room's own recurring documents. Composition shows where the
money goes before any payout rule; the flyer's printed matrix is reproduced
below the table.</p>
%s
<div class="table-wrap"><table class="data">
<thead><tr><th>Days</th><th>Room</th><th>Format</th><th>Buy-in</th><th>Guarantee</th>
<th>Payout rule and composition</th><th>Official source</th><th>Retrieved</th></tr></thead>
<tbody>
%s
</tbody></table></div>
%s
<p class="small">Extraction basis: the sentence patterns in
<code>scripts/extract_payouts.py</code>, the section headings of the Wynn WPT
structures PDF, and the Caesars flyer's printed matrix. Documents were last
captured by the scheduled monitors on the dates shown per row; re-checks run
through <a href="monitoring.html">Source monitoring</a>.</p>
</div>
""" % (
        sum(tournament_counts.values()),
        _payout_legend(tournament_counts),
        "\n".join(_payout_tr(row) for row in tournament_sorted),
        sum(daily_counts.values()),
        _payout_legend(daily_counts),
        "\n".join(_daily_payout_tr(row) for row in daily_sorted),
        _caesars_matrix_html(),
    )


PAGES["pages/payouts.html"] = ("Payout rules", "payouts", _payout_body())


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
