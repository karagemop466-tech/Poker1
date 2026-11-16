"""Build data/*.json and root *.html pages from scripts/data_verified.py.

Run:  python3 scripts/build.py
Every output value comes from data_verified.py, which carries official source URLs.
Blank (None) values are rendered as blank cells with a flag marker and listed on
flagged.html. Nothing is inferred here.
"""
import datetime as dt
import html
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import data_verified as D  # noqa: E402

GENERATED = "2026-11-16"
READ_SHEETS = {1, 2, 5, 6, 7, 8, 10, 11, 15, 16, 17, 18, 22, 23, 26, 27, 28, 29, 30, 33, 34}
FLAG = '<span class="flag" title="Not verified from an official source — left blank">&#9873;</span>'


def esc(x):
    return html.escape("" if x is None else str(x))


def money(x):
    if x is None:
        return None
    return f"${x:,.0f}"


def fmt_date(iso):
    d = dt.date.fromisoformat(iso)
    return d.strftime("%a %b %d, %Y").replace(" 0", " ")


# ---------------------------------------------------------------- MAIN LIST
main = []
for r in D.V:
    row = dict(
        event=r["event"], date=r["date"], start=r["start"], name=r["name"],
        buy_in=r["buy_in"], gtd=r["gtd"], house_fee=r["house_fee"], prize_pool=r["prize_pool"],
        bounty=r["bounty"], eligibility=r["eligibility"], notes=r["notes"],
        gtd_note=r["gtd_note"],
        entry_type="Candidate: no re-entry or add-on terms printed on structure sheet (explicit single-entry wording not found)",
        structure_sheet=r["struct"],
        source_schedule=D.VEN_SCHED,
        source_structure=D.vs(r["struct"]),
        sheet_read=r["struct"] in READ_SHEETS,
    )
    main.append(row)
main.sort(key=lambda x: (-(x["buy_in"] or 0), -(x["prize_pool"] or 0), x["date"], x["event"]))
for i, row in enumerate(main, 1):
    row["rank"] = i

# -------------------------------------------------- EXCLUDED: multi-entry etc.
excluded = []
for m in D.VEN_MULTI:
    excluded.append(dict(
        category="Multi-flight / re-entry", source="Venetian DSE IV schedule (official)",
        event=m["event"], date=m["date"], start=m["start"], name=m["name"],
        buy_in=m["buy_in"], gtd=m["gtd"], house_fee=m["house_fee"], prize_pool=m["prize_pool"],
        reason=m["why"], notes=m["notes"], source_schedule=D.VEN_SCHED,
        source_structure=[D.vs(s) for s in m["structure"]],
    ))
for r in D.WYNN_DAILY:
    excluded.append(dict(
        category="Re-entry / rebuy / add-on", source="Wynn daily poster + daily structures (official)",
        event=None, date=r["days"], start=r["start"], name=r["name"], buy_in=r["buy_in"], gtd=r["gtd"],
        house_fee=None, prize_pool=None,
        reason=r["entry"], notes=r["fee"], source_schedule=D.WYNN_POSTER, source_structure=[r["struct"]],
    ))
for b in D.BELL:
    cat = "Pay-to-advantage (gratuity buys chips)" if "gratuity" in b["fee"] else "Re-entry (weekly event)"
    excluded.append(dict(
        category=cat, source="Bellagio poker page + structure PDF (official)",
        event=None, date=b["day"], start=b["start"], name=b["name"], buy_in=b["buy_in"], gtd=b["gtd"],
        house_fee=None, prize_pool=None, reason=b["entry"], notes=b["fee"] + ". " + b["note"],
        source_schedule=D.BELL_POKER_PAGE, source_structure=[b["struct"]],
    ))
excluded.append(dict(
    category="Re-entry (WPT World Championship)", source="Wynn WPT structures PDF (official)",
    event=None, date="2026-11-27 to 2026-11-29", start="11:00 AM (1A) to 6:00 PM (1F)",
    name="$600 No Limit Hold'em $400,000 GTD (Flights 1A–1F + Day 2)", buy_in=600, gtd=400000,
    house_fee=None, prize_pool=510,
    reason="Official terms: 'Unlimited re-entry for each starting flight will be available until the start of level 9.' Entry fee $600 = $510 prize pool + $65 tournament fee + $25 staff service charge.",
    notes="Official structure PDF read (chunk 1 of 8).", source_schedule=D.WYNN_WPT_SCHED, source_structure=[D.WYNN_WPT_STRUCT],
))

# ----------------------------------------------------- UNVERIFIED / NOT RANKED
unverified = []
for s in D.VEN_OTHER:
    unverified.append(dict(
        category=s["kind"], source="Venetian DSE IV schedule (official)", event=s["event"], date=s["date"],
        start=s["start"], name=s["name"], buy_in=s["buy_in"], gtd=s["gtd"],
        reason="Structure sheet not read in full, or format rules not confirmed. Not ranked.",
        notes=s["notes"], source_schedule=D.VEN_SCHED, source_structure=[D.vs(s["structure"][0])],
    ))
wpt_flagged_ids = set()
for (d, t, name, buy, gtd) in D.WPT:
    if buy == 600 and gtd == 400000 and d <= "2026-11-29":
        continue  # covered above as re-entry
    unverified.append(dict(
        category="WPT World Championship (rules not verified)", source="Wynn WPT schedule (official)",
        event=None, date=d, start=t, name=name, buy_in=buy, gtd=gtd,
        reason="Official schedule row only. Re-entry, add-on, and bounty rules not verified for this event.",
        notes="", source_schedule=D.WYNN_WPT_SCHED, source_structure=[D.WYNN_WPT_STRUCT],
    ))
unverified.sort(key=lambda x: (x["date"], x["start"]))

# ----------------------------------------------------------------- HOTELS
hotels = D.build_hotel_costs()
for h in hotels:
    h["walk_minutes_to_venue"] = None
    h["meets_30min_walk"] = None
    h["walk_note"] = "No official walking-time source retrieved. Blank and flagged."

# --------------------------------------------------------------- SCHEDULE
start = dt.date(2026, 11, 16)
end = dt.date(2026, 12, 23)
schedule = []
d = start
while d <= end:
    iso = d.isoformat()
    day_main = [m for m in main if m["date"] == iso]
    day_multi = [m for m in excluded if m["date"] == iso and m["category"].startswith("Multi")]
    schedule.append(dict(
        date=iso, label=fmt_date(iso),
        single_entry_starts=[dict(start=m["start"], event=m["event"], name=m["name"],
                                  buy_in=m["buy_in"], source=D.VEN_SCHED) for m in sorted(day_main, key=lambda x: x["start"])],
        multi_entry_starts=[dict(start=m["start"], event=m["event"], name=m["name"]) for m in day_multi],
        earliest_verified_single_entry_start=None,
        note=("No verified single-entry tournament starts before 10:10 AM on the official schedule. "
              "Arrive at 8:00 AM for the room and tournament check-in; no official event begins at 8:00 AM.")
        if day_main else "No single-entry Venetian start this day (multi-flight or no event). See excluded list.",
    ))
    if day_main:
        schedule[-1]["earliest_verified_single_entry_start"] = min(m["start"] for m in day_main)
    d += dt.timedelta(days=1)

# ----------------------------------------------------------- REPO REVIEW
review = [
    dict(id="R1", check="Venetian DSE IV schedule: every row (date, time, event #, name, structure URL) compared to the fetched official page",
         result="Re-verified on 2026-11-16 across all 4 chunks. Dates, times and sheet mappings in data match the page. Event 1 flights 1A–1D and events 19, 37 confirmed.", status="verified", source=D.VEN_SCHED),
    dict(id="R2", check="Venetian single-day structure sheets (fee, pool, guarantee, late registration)",
         result="Read: sheets 1, 2, 5, 6, 7, 8, 10, 11, 15, 16, 17, 18, 22, 23, 26, 27, 28, 29, 30, 33, 34. Fee/pool/guarantee match the data. Sheets 3, 4, 9, 12–14, 19–21, 24, 25, 31, 32, 35–37 NOT read: those events are not ranked.", status="partial", source=D.VEN_SCHED),
    dict(id="R3", check="Venetian hotel terms: resort fee, room tax, guest surcharge, parking",
         result="$55 resort fee + 13.38% Clark County room tax per night (official). Used in hotel totals.", status="verified", source=D.VEN_HOTEL_TERMS),
    dict(id="R4", check="Venetian poker suite rates and play requirement",
         result="From $119 (Venetian) / $209 (Palazzo); $55 resort fee; conditional on poker play each night. Used as the rate basis, with the condition flagged.", status="verified", source=D.VEN_SUITE_RATES),
    dict(id="R5", check="Bellagio weekly events (PDF structures)",
         result="Fri $600 NLH and Sun $400 H.O.R.S.E. read. Sat PDF conflicts ($1,000 file name/page, $1,100 header, $600 fee sum). Gratuity buys chips (pay-to-advantage).", status="irregular", source=D.BELL_POKER_PAGE),
    dict(id="R6", check="Wynn daily tournaments (structures PDF)",
         result="All five daily structures read. All allow re-entry or add-on, so all are excluded from the single-entry list. Registration text says 'Encore at Wynn'.", status="irregular", source=D.WYNN_DAILY_STRUCT),
    dict(id="R7", check="Wynn WPT schedule (PDF)",
         result="Rows out of chronological order (Dec 18 before Dec 17). A footnote mentions an $11,100 Ladies entry. Not ranked.", status="irregular", source=D.WYNN_WPT_SCHED),
    dict(id="R8", check="Wynn WPT structures PDF ($600 NLH, $400K GTD)",
         result="Unlimited re-entry per flight until level 9. Fee breakdown $510 + $65 + $25 = $600. Excluded from single-entry list.", status="verified", source=D.WYNN_WPT_STRUCT),
    dict(id="R9", check="Wynn hotel rates and resort fee",
         result="Official pages wynnlasvegas.com/hotel are dead. Undated offer 848654 says $45 resort fee and $99/$169 rates. Offer 850225 says $55 and expired Aug 31, 2026. Conflict; left blank.", status="irregular", source=D.WYNN_TERMS_OFFER),
    dict(id="R10", check="Caesars Palace hotel page (resort fee)",
         result="Official page chunks 0–1 read: no resort fee shown. Aggregators conflict ($49.95, $55, $62.30). Left blank.", status="unverified", source=D.CAESARS_HOTEL),
    dict(id="R11", check="Bellagio resort fee and nightly rate",
         result="Not found on official MGM pages retrieved. Aggregator figure $55 + tax not used.", status="unverified", source=D.BELL_POKER_PAGE),
    dict(id="R12", check="RWLV, MGM Grand (SSPS), Aria, Planet Hollywood poker pages",
         result="Official URLs returned email blast, 404, or unrelated domain. No events from these venues are listed.", status="unverified", source="https://rwlasvegas.com/casino/poker"),
    dict(id="R13", check="Stale notice on Bellagio poker page",
         result="Official page carries a tournament-resumption notice dated July 26. Weekly event list may be out of date.", status="irregular", source=D.BELL_POKER_PAGE),
    dict(id="R14", check="Wynn daily suspension during WPT series",
         result="Official poker page says daily tournaments are suspended during the series (Nov 27 – Dec 21). Resume date not stated.", status="irregular", source=D.WYNN_POKER_PAGE),
]

# ---------------------------------------------------------- FLAGGED LIST
flagged = [
    dict(id="F1", type="Conflict", item="Bellagio Saturday event: price", detail="File name and official page say $1,000; the PDF header says $1,100; the fee breakdown ($510 + $50 + $40) totals $600.", source=D.BELL_POKER_PAGE),
    dict(id="F2", type="Conflict", item="Wynn Hotel resort fee", detail="Undated offer 848654: $45 + tax. Expired offer 850225: $55 + tax. No current official value. Left blank.", source=D.WYNN_TERMS_OFFER),
    dict(id="F3", type="Conflict", item="Wynn daily registration location", detail="Daily T&C say registration is in 'Encore at Wynn'; the poker room is documented at Wynn. Confirm before play.", source=D.WYNN_DAILY_STRUCT),
    dict(id="F4", type="Irregularity", item="Wynn WPT schedule order", detail="Dec 18 rows appear before Dec 17 rows. A footnote lists an $11,100 Ladies entry.", source=D.WYNN_WPT_SCHED),
    dict(id="F5", type="Unverified", item="Caesars Palace resort fee", detail="Official page chunks 0–1 read, no fee shown. Aggregators disagree. Left blank.", source=D.CAESARS_HOTEL),
    dict(id="F6", type="Unverified", item="Bellagio resort fee and nightly rate", detail="No official MGM page retrieved. Left blank.", source=D.BELL_POKER_PAGE),
    dict(id="F7", type="Unverified", item="Wynn base rate", detail="Official wynnlasvegas.com/hotel page is dead. Offer rates are undated or expired. Left blank.", source=D.WYNN_TERMS_OFFER),
    dict(id="F8", type="Unverified", item="Hotel walking times to venues", detail="No official source for walking time. The 30-minute walking criterion cannot be verified for any hotel. Blank.", source=D.VEN_HOTEL_TERMS),
    dict(id="F9", type="Unverified", item="Venetian structure sheets not read", detail="Sheets 3, 4, 9, 12–14, 19–21, 24, 25, 31, 32, 35–37 not read. Affected events are multi-flight, satellite, tag-team or 2-day, so they are not ranked.", source=D.VEN_SCHED),
    dict(id="F10", type="Unverified", item="Venetian single-day sheets: re-entry rule", detail="Read sheets print no re-entry or add-on provision. Classified single-entry on that basis. Confirm at the cage.", source=D.VEN_SCHED),
    dict(id="F11", type="Policy decision", item="Bounty / PKO events in the single-entry list", detail="Bounties are prize money and do not add chips. Kept in the single-entry list with a Bounty flag. Owner to confirm.", source=D.VEN_SCHED),
    dict(id="F12", type="Policy decision", item="PokerAtlas PRO $20 rake discount (events 18, 58)", detail="Membership-linked discount on the initial buy-in only. Kept in the list, flagged.", source=D.VEN_SCHED),
    dict(id="F13", type="Policy decision", item="Bellagio optional staff gratuity", detail="$40 Fri / $25 Sun / Sat gratuity buys extra chips. Treated as pay-to-advantage and excluded.", source=D.BELL_POKER_PAGE),
    dict(id="F14", type="Unverified", item="Wynn daily tournaments during WPT series", detail="Official page says daily tournaments are suspended during the series. Resume date not stated.", source=D.WYNN_POKER_PAGE),
    dict(id="F15", type="Unverified", item="8:00 AM start", detail="No official single-entry event starts before 10:10 AM (verified). The 9:10 AM satellite (event 46) is unranked.", source=D.VEN_SCHED),
    dict(id="F16", type="Unverified", item="Venetian DSE event durations", detail="Official schedule gives start times and some late-registration windows, not durations. Stacking events cannot be confirmed.", source=D.VEN_SCHED),
]

# ---------------------------------------------------------------- WRITE JSON
os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)


def dump(name, obj):
    with open(os.path.join(ROOT, "data", name), "w") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")


dump("tournaments.json", dict(
    generated=GENERATED, as_of="2026-11-16 (Houston, TX local date)",
    series="Venetian DeepStack Extravaganza IV (Nov 16 – Dec 23, 2026)",
    main_single_entry=main, excluded=excluded, unverified_not_ranked=unverified,
    sources={k: v for k, v in D.SOURCES.items()},
))
dump("hotels.json", dict(generated=GENERATED, hotels=hotels, tax_rate=D.TAX_RATE,
                         formula="(nightly rate + resort fee) x (1 + room tax)"))
dump("schedule.json", dict(generated=GENERATED, days=schedule))
dump("repo_review.json", dict(generated=GENERATED, checks=review, flagged=flagged))

# ----------------------------------------------------------- HTML PAGES

NAV = [("index.html", "Home"), ("tournaments.html", "Single-entry candidates"), ("excluded.html", "Excluded & unranked"),
       ("hotels.html", "Hotels"), ("schedule.html", "Schedule"), ("flagged.html", "Flagged for Review"),
       ("review.html", "Repo review"), ("decision.html", "Decision brief"), ("suggestions.html", "Suggestions")]


def page(title, body, active, prefix=""):
    # Flat root layout (matches .github/workflows/pages.yml staging).
    nav = "".join(
        f'<a href="{href}"{" class=active" if href == active else ""}>{esc(lbl)}</a>'
        for href, lbl in NAV)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} · Las Vegas Strip Poker</title>
<link rel="stylesheet" href="{prefix}assets/style.css"></head>
<body><header class="top"><div class="wrap"><a class="brand" href="{prefix}index.html">Las Vegas Strip Poker</a>
<nav>{nav}</nav></div></header>
<main class="wrap">
<h1>{esc(title)}</h1>
{body}
</main>
<footer class="wrap small">Values are from official sources linked on each row. Blank cells with &#9873; are unverified and listed on <a href="flagged.html">Flagged for Review</a>. Generated {GENERATED}.</footer>
</body></html>
"""


def cell(v, fmt=None):
    if v is None or v == "":
        return f'<td class="blank">{FLAG}</td>'
    if fmt == "money":
        return f"<td class=num>{esc(money(v))}</td>"
    return f"<td>{esc(v)}</td>"


def link(url, label):
    if not url:
        return ""
    return f'<a href="{esc(url)}" rel="noopener">{esc(label)}</a>'


def table(headers, rows):
    th = "".join(f"<th>{esc(h)}</th>" for h in headers)
    return f'<div class="scroll"><table><thead><tr>{th}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'


# tournaments
rows = []
for r in main:
    src = f'{link(r["source_schedule"], "Schedule")} · {link(r["source_structure"], "Structure")}'
    rows.append(
        f"<tr><td>{r['rank']}</td><td>{r['event']}</td><td>{esc(fmt_date(r['date']))}</td><td>{esc(r['start'])}</td>"
        f"<td>{esc(r['name'])}</td>{cell(r['buy_in'],'money')}{cell(r['gtd'],'money')}{cell(r['house_fee'],'money')}"
        f"{cell(r['prize_pool'],'money')}<td>{'Bounty' if r['bounty'] else ''}</td><td>{esc(r['eligibility'])}</td>"
        f"<td class=small>{esc(r['notes'] or '')}{(' ' + esc(r['gtd_note'])) if r['gtd_note'] else ''}</td><td class=src>{src}</td></tr>")
tour_body = f"""<p class="lead">Single-entry, single-day Venetian DeepStack Extravaganza IV events, ranked by buy-in and then prize pool.
{len(main)} candidates. Every row links to the official schedule and structure sheet. Source: <a href="{esc(D.VEN_SCHED)}">Venetian official schedule</a>.</p>
<p class="small">Entry type: each row is a candidate because its structure sheet prints no re-entry or add-on terms. Explicit single-entry wording was not found on the sheets read, so the confirmed count under a strict standard is 0. Bounty events are included (no chip purchase) and marked. The buy-in is the total charged; the house fee is buy-in minus prize pool.</p>
{table(["Rank","Event #","Date","Start","Event","Buy-in","GTD","House fee","Prize pool","Bounty","Eligibility","Notes","Sources"], rows)}
"""
open(os.path.join(ROOT, "tournaments.html"), "w").write(page("Single-entry candidates", tour_body, "tournaments.html"))

# excluded
er = []
for x in excluded:
    src = x["source_schedule"]
    srcs = src if isinstance(src, str) else ""
    structs = x.get("source_structure") or []
    if isinstance(structs, str):
        structs = [structs]
    s_links = " · ".join(link(u, f"Structure {i+1}" if len(structs) > 1 else "Structure") for i, u in enumerate(structs))
    er.append(
        f"<tr><td>{esc(x['category'])}</td><td>{esc(x['event'] or '')}</td><td>{esc(x['date'])}</td><td>{esc(x['start'])}</td>"
        f"<td>{esc(x['name'])}</td>{cell(x['buy_in'],'money')}{cell(x['gtd'],'money')}"
        f"<td class=small>{esc(x['reason'])}</td><td class=small>{esc(x.get('notes') or '')}</td>"
        f"<td class=src>{link(srcs, 'Official')} · {s_links}</td></tr>")
ex_body = f"""<p class="lead">Events that do not qualify for the single-entry list: re-entry or flight structures, add-ons or rebuys,
and pay-to-advantage gratuities. Also includes unverified events that are not ranked.</p>
<h2>A. Excluded: re-entry, flights, add-on, rebuy, pay-to-advantage ({len(excluded)} rows)</h2>
{table(["Category","Event #","Date","Start","Event","Buy-in","GTD","Why excluded","Notes","Sources"], er)}
<h2>B. Unverified and not ranked ({len(unverified)} rows)</h2>
<p class="small">These rows could not be confirmed as single-entry from a read structure sheet or official terms. They are shown for transparency and are not ranked.</p>
{table(["Category","Event #","Date","Start","Event","Buy-in","GTD","Reason","Notes","Sources"],
        [f"<tr><td>{esc(u['category'])}</td><td>{esc(u['event'] or '')}</td><td>{esc(u['date'])}</td><td>{esc(u['start'])}</td><td>{esc(u['name'])}</td>{cell(u['buy_in'],'money')}{cell(u['gtd'],'money')}<td class=small>{esc(u['reason'])}</td><td class=small>{esc(u['notes'] or '')}</td><td class=src>{link(u['source_schedule'],'Official')} · {link(u['source_structure'][0],'Structure')}</td></tr>" for u in unverified])}
"""
open(os.path.join(ROOT, "excluded.html"), "w").write(page("Excluded and unverified events", ex_body, "excluded.html"))

# hotels
hr = []
for h in hotels:
    srcs = " · ".join(link(D.SOURCES[k]["url"], k.replace("_", " ").title()) for k in h["sources"])
    hr.append(
        f"<tr><td><strong>{esc(h['name'])}</strong><div class=small>{esc(h['tournaments'])}</div></td>"
        f"<td class=small>{esc(h['in_building'])}</td>{cell(h['base_rate_from'],'money')}"
        f"<td class=small>{esc(h['rate_basis'])}</td>{cell(h['resort_fee'],'money')}"
        f"{cell(h['true_cost_from_per_night'],'money')}"
        f"<td class=small>{esc(h['resort_fee_basis'])}</td>"
        f"<td class=small>{esc(h['walk_note'])}</td>"
        f"<td class=src>{srcs}</td></tr>")
hotel_body = f"""<p class="lead">Hotel costs use official rates, resort fees and room tax only. <strong>True nightly cost</strong> =
(rate + resort fee) × (1 + {D.TAX_RATE*100:.2f}% room tax). Blank cells are unverified (see Flagged).</p>
<p class="small"><strong>Walking requirement:</strong> the brief asks for hotels at least 30 minutes' walk from the venue. No official source gives walking times, so no hotel is confirmed to meet this. The Venetian/Palazzo is the venue itself, so it does not meet the 30-minute requirement. Its figures are shown as a cost reference only.</p>
{table(["Hotel","Position vs. venue","Rate from (official, conditional)","Rate basis","Resort fee / night","True cost / night from","Resort-fee basis","Walking","Sources"], hr)}
"""
open(os.path.join(ROOT, "hotels.html"), "w").write(page("Hotels", hotel_body, "hotels.html"))

# schedule
sched_rows = []
for dd in schedule:
    if dd["single_entry_starts"]:
        items = "<br>".join(f"{esc(s['start'])} · #{s['event']} {esc(s['name'])} ({money(s['buy_in'])})" for s in dd["single_entry_starts"])
    else:
        items = '<span class="small">No single-entry starts</span>'
    multi = "<br>".join(f"{esc(s['start'])} · #{s['event']} {esc(s['name'])}" for s in dd["multi_entry_starts"]) or ""
    sched_rows.append(f"<tr><td>{esc(dd['label'])}</td><td>{items}</td><td class=small>{multi}</td><td class=small>{esc(dd['note'])}</td></tr>")
sched_body = f"""<p class="lead">Single-entry starts by day, from the official Venetian schedule. Arrive at 8:00 AM to register; the first verified single-entry start is 10:10 AM.</p>
<p class="small">Event durations and stacking feasibility are not published, so no per-day chain of events is claimed. The list shows official start times only. Multi-flight events are listed for reference and are excluded.</p>
{table(["Date","Single-entry starts (official)","Excluded multi-entry starts (reference)","Note"], sched_rows)}
<p class="small">Schedule source: <a href="{esc(D.VEN_SCHED)}">Venetian DeepStack Extravaganza IV (official)</a>.</p>
"""
open(os.path.join(ROOT, "schedule.html"), "w").write(page("Schedule", sched_body, "schedule.html"))

# flagged
fl_rows = [f"<tr><td>{esc(f['id'])}</td><td>{esc(f['type'])}</td><td>{esc(f['item'])}</td><td>{esc(f['detail'])}</td><td class=src>{link(f['source'],'Source') if f['source'].startswith('http') else esc(f['source'])}</td></tr>" for f in flagged]
fl_body = f"""<p class="lead">Irregularities, conflicts, unverified values and policy decisions. Flagged items do not block the merge; they are published here for review.</p>
{table(["ID","Type","Item","Detail","Source"], fl_rows)}
"""
open(os.path.join(ROOT, "flagged.html"), "w").write(page("Flagged for Review", fl_body, "flagged.html"))

# repo review
rv_rows = [f"<tr><td>{esc(c['id'])}</td><td>{esc(c['check'])}</td><td>{esc(c['result'])}</td><td>{esc(c['status'])}</td><td class=src>{link(c['source'],'Source') if c['source'].startswith('http') else esc(c['source'])}</td></tr>" for c in review]
rv_body = f"""<p class="lead">Line-by-line verification log against official sources, with irregularities. Also in <code>REVIEW.md</code> and <code>data/repo_review.json</code>.</p>
{table(["ID","Check","Result","Status","Source"], rv_rows)}
"""
open(os.path.join(ROOT, "review.html"), "w").write(page("Repo review", rv_body, "review.html"))

print("built", len(main), "main;", len(excluded), "excluded;", len(unverified), "unverified;", len(hotels), "hotels;", len(schedule), "days;", len(flagged), "flags")


# ----------------------------------------------------------- INDEX (T7)
def index_page():
    nav_items = [("index.html", "Home"), ("tournaments.html", "Single-entry candidates"), ("excluded.html", "Excluded & unranked"),
                 ("hotels.html", "Hotels"), ("schedule.html", "Schedule"), ("flagged.html", "Flagged for Review"),
                 ("review.html", "Repo review"), ("decision.html", "Decision brief"), ("suggestions.html", "Suggestions")]
    nav = "".join(f'<a href="{h}"{" class=active" if h == "index.html" else ""}>{esc(l)}</a>' for h, l in nav_items)
    repo = "https://github.com/karagemop466-tech/Poker1/blob/main/"
    cards = [
        ("tournaments.html", "Single-entry candidates", f"{len(main)} Venetian DSE IV single-day candidates with no re-entry or add-on terms printed, ranked by buy-in and prize pool.", len(main)),
        ("excluded.html", "Excluded and unverified", f"{len(excluded)} excluded (re-entry, flights, add-ons, pay-to-advantage) and {len(unverified)} unranked rows.", len(excluded)),
        ("hotels.html", "Hotels", "Official rates, resort fees and true nightly cost. Walking times not verified.", len(hotels)),
        ("schedule.html", "Schedule", "Candidate single-entry starts by day, Nov 16 – Dec 23, 2026. First verified start 10:10 AM.", len(schedule)),
        ("flagged.html", "Flagged for Review", f"{len(flagged)} flags: conflicts, unverified values, policy decisions.", len(flagged)),
        ("review.html", "Repo review", f"{len(review)} verification checks against official sources, with irregularities.", len(review)),
    ]
    cards_html = "".join(
        f'<a class="card" href="{h}"><h3>{esc(t)}</h3><p>{esc(d)}</p><div class="stat">{n}</div></a>' for h, t, d, n in cards)
    docs = [("EXECUTIVE_SUMMARY.md", "Executive summary"), ("research/analysis.md", "Analysis"),
            ("SUGGESTIONS.md", "Suggestions (for review)"), ("QUESTIONS.md", "Questions and gaps"), ("REVIEW.md", "Repo review (markdown)")]
    docs_html = "".join(f'<li><a href="{repo}{p}">{esc(t)}</a></li>' for p, t in docs)
    body = f"""<section><p class="lead">Las Vegas Strip poker, November 16 – December 23, 2026. A verified list of single-entry tournaments,
the hotels nearby, and a day-by-day schedule. Every value links to an official source. Unverified values are blank and flagged,
not inferred.</p>
<div class="notice"><strong>Key facts.</strong> No verified single-entry event starts before 10:10 AM. Hotels: no walking times are verified,
so no hotel is confirmed to meet the 30-minute walking requirement. The Venetian is the venue itself (true cost from $197.28 per night).</div>
<div class="cards">{cards_html}</div>
<h2>Documents</h2><ul>{docs_html}</ul>
<p class="small">Data: <a href="{repo}data/tournaments.json">tournaments.json</a> · <a href="{repo}data/hotels.json">hotels.json</a> · <a href="{repo}data/schedule.json">schedule.json</a> · <a href="{repo}data/repo_review.json">repo_review.json</a></p>
</section>"""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Las Vegas Strip Poker · Dashboard</title>
<link rel="stylesheet" href="assets/style.css"></head>
<body><header class="top"><div class="wrap"><a class="brand" href="index.html">Las Vegas Strip Poker</a>
<nav>{nav}</nav></div></header>
<main class="wrap"><h1>Las Vegas Strip Poker — Dashboard</h1>{body}</main>
<footer class="wrap small">Generated {GENERATED} from official sources. Blank cells with &#9873; are unverified.</footer>
</body></html>
"""


open(os.path.join(ROOT, "index.html"), "w").write(index_page())
open(os.path.join(ROOT, ".nojekyll"), "w").write("")
print("index written")
