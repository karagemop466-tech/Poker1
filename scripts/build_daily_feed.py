#!/usr/bin/env python3
"""Build the seed daily feed from the official daily documents that were read.

The live scraper (scripts/scrape_daily.py) refreshes this file on a schedule.
This script writes the rows that were read directly from the official daily
structure sheets and posters, so the Daily feed page is useful before the
first scheduled run and so a failed extraction never silently drops a row.

Every row names the official document it came from and the date it was read.
Run:  python3 scripts/build_daily_feed.py
"""
import json
import os
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

VERIFIED_ON = "2026-11-16"

SRC = {
    "wynn_poster": "https://cdn.wynnresorts.com/image/upload/v1752011166/visitwynn_pdfs_files/Poker/Daily%20Tournaments/poker-daily-tournament-poster.pdf",
    "wynn_structures": "https://cdn.wynnresorts.com/image/upload/v1752011191/visitwynn_pdfs_files/Poker/Daily%20Tournaments/Poker-All_Daily_Structures.pdf",
    "wynn_poker": "https://www.wynnlasvegas.com/casino/poker",
    "bellagio_poker": "https://bellagio.mgmresorts.com/en/casino/poker.html",
    "bellagio_fri": "https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/blt9cf95b0e60ec253e/6af491a3a9851d75c40be840/mgm-bellagio-poker-fridays-$600-nlh.pdf",
    "bellagio_sat": "https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/blt6d47974bf5a7d9b6/6af491a391a6e8e4230c9e07/mgm-bellagio-poker-saturdays-$1000-nlh.pdf",
    "bellagio_sun": "https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/blt07fcf1244a6da661/6af491a339e2b4f6b76a86ad/mgm-bellagio-poker-sundays-$400-horse.pdf",
    "aria_poker": "https://aria.mgmresorts.com/en/casino/poker.html",
    "venetian_poker": "https://www.venetianlasvegas.com/resort/casino/poker.html",
}

WYNN_VENUE = "Wynn Las Vegas / Encore Poker Room"
BELLAGIO_VENUE = "Bellagio Poker Room"


def row(venue, venue_name, when, name, fmt, buy, stack, gtd, entry_rule, source, label, note):
    return {
        "venue": venue,
        "venue_name": venue_name,
        "when": when,
        "name": name,
        "format": fmt,
        "buy_in_usd": buy,
        "stack_chips": stack,
        "guarantee_usd": gtd,
        "entry_rule": entry_rule,
        "source": source,
        "source_label": label,
        "verified_on": VERIFIED_ON,
        "retrieved_at": VERIFIED_ON + "T00:00:00+00:00",
        "origin": "read from the official document",
        "notes": note,
    }


SEED = [
    # ---- Wynn daily tournaments, from the official daily poster and the
    # official daily structure sheets.
    row("wynn", WYNN_VENUE, "Monday - Thursday, 12 p.m.",
        "$200 No Limit Hold'em, $10,000 Guarantee",
        "Daily single-day No Limit Hold'em, Big Blind Ante", 200, 25000, 10000,
        "Registration and re-entry until the start of level 9 (about 4:30 p.m.). "
        "The entry fee and the re-entry fee are both $200. All levels play 30 minutes "
        "with a 15-minute break after every 4 levels.",
        SRC["wynn_structures"], "Official Wynn daily tournament structures",
        "The $200 entry fee is distributed as $26 tournament fee, $12 poker staff service charge "
        "and $162 prize pool. The tournament is offered Monday-Thursday and may be suspended "
        "during Seniors Events, Classic Events or other tournament series."),

    row("wynn", WYNN_VENUE, "Friday, 12 p.m.",
        "$240 No Limit Hold'em Rebuy and Add-on, $40,000 Guarantee",
        "Daily single-day No Limit Hold'em with rebuys and add-ons", 240, 25000, 40000,
        "Registration, rebuys and add-ons until the start of level 9 (about 4:30 p.m.). "
        "Re-entry is NOT allowed. Unlimited $200 rebuys for 25,000 chips are available any time "
        "a player is at 15,000 chips or less. One $100 add-on for 25,000 chips is available any "
        "time until the end of registration. All rebuys must be made from the player's original seat.",
        SRC["wynn_structures"], "Official Wynn daily tournament structures",
        "The $240 entry fee is $35 tournament fee, $15 poker staff service charge and $190 prize pool. "
        "$10 from each $200 rebuy and $5 from each $100 add-on are withheld as a staff service charge; "
        "$5 from each $200 rebuy and $5 from each add-on are withheld as a tournament fee."),

    row("wynn", WYNN_VENUE, "Saturday and Sunday, 12 p.m.",
        "$200 No Limit Hold'em, $25,000 Guarantee",
        "Daily single-day No Limit Hold'em with re-entry and one add-on", 200, 25000, 25000,
        "Registration, re-entry and one add-on per entry until the start of level 11 (about 5:30 p.m.). "
        "One $100 add-on for 25,000 chips is available any time until the end of registration. "
        "All levels play 30 minutes with a 15-minute break after every 4 levels.",
        SRC["wynn_structures"], "Official Wynn daily tournament structures",
        "The $200 entry fee is distributed as $26 tournament fee, $12 poker staff service charge "
        "and $162 prize pool. $5 from each $100 add-on is withheld as a tournament fee and $5 from "
        "each add-on as a staff service charge."),

    row("wynn", WYNN_VENUE, "Nightly, Monday - Sunday, 6 p.m.",
        "$160 No Limit Hold'em, $10,000 Guarantee",
        "Nightly single-day No Limit Hold'em with re-entry and one add-on", 160, 25000, 10000,
        "Registration, re-entry and one add-on per entry until the start of level 9 (about 9:00 p.m.). "
        "One $100 add-on for 25,000 chips is available any time until the end of registration. "
        "All levels play 20 minutes with a 10-minute break after every 4 levels.",
        SRC["wynn_structures"], "Official Wynn daily tournament structures",
        "The $160 entry fee is distributed as $20 tournament fee, $10 poker staff service charge "
        "and $130 prize pool. $5 from each $100 add-on is withheld as a tournament fee and $5 from "
        "each add-on as a staff service charge."),

    row("wynn", WYNN_VENUE, "Daily poster",
        "Daily tournament poster: Monday-Thursday $200 NLH $10,000 GTD, Friday $240 NLH Rebuy "
        "$40,000 GTD, Saturday and Sunday $200 NLH $25,000 GTD, nightly $160 NLH $10,000 GTD",
        "Official daily tournament poster", None, None, None,
        "The poster itself states no entry rule; the entry rules are in the daily structure sheets.",
        SRC["wynn_poster"], "Official Wynn daily tournament poster",
        "The poster is the authoritative schedule of which daily tournament runs on which day. "
        "The poster directs players to wynnpoker.com or the event structure sheets for the "
        "complete list of house and staff fees."),

    # ---- Bellagio weekly poker room, from the official structure sheets.
    row("bellagio", BELLAGIO_VENUE, "Friday, 11:00 a.m.",
        "$600 No Limit Hold'em",
        "Weekly single-day No Limit Hold'em with re-entry", 600, 30000, None,
        "Players may buy in and re-enter through the end of level 8 (including the break). "
        "Levels are 30 minutes long with a 12-minute break every 4 levels.",
        SRC["bellagio_fri"], "Official Bellagio Friday $600 No Limit Hold'em structure sheet",
        "The $600 buy-in is allocated as $510 to the prize pool, $50 house fee and $40 voluntary "
        "staff gratuity. Players start with 30,000 tournament chips, including the optional staff "
        "gratuity (15,000 + 15,000). No guarantee is printed on this sheet."),

    row("bellagio", BELLAGIO_VENUE, "Saturday, 11:00 a.m.",
        "No Limit Hold'em, multi-flight",
        "Weekly multi-flight No Limit Hold'em", None, 40000, 50000,
        "Registration is open until the start of level 10. Players start with 40,000 tournament "
        "chips (20,000 + 20,000 optional).",
        SRC["bellagio_sat"], "Official Bellagio Saturday No Limit Hold'em structure sheet",
        "Bellagio guarantees the total combined prize pool will be at least $50,000. The buy-in and "
        "fee split is unverified: rule 07 reads '$600 buy-in, $510 to the prize pool, $50 admin "
        "fees and $40 optional staff gratuity', the document heading reads 'NLH $1100 BUY-IN' and "
        "the published file name says $1000 NLH. The three statements conflict, so the buy-in is "
        "left blank here."),

    row("bellagio", BELLAGIO_VENUE, "Sunday, 11:00 a.m.",
        "$400 H.O.R.S.E.",
        "Weekly single-day H.O.R.S.E. with re-entry", 400, 30000, None,
        "Players may buy in and re-enter through the end of level 8 (including the break). "
        "Each level lasts 30 minutes.",
        SRC["bellagio_sun"], "Official Bellagio Sunday $400 H.O.R.S.E. structure sheet",
        "The $400 buy-in is allocated as $340 to the prize pool, $35 house fee and $25 voluntary "
        "staff gratuity. No guarantee is printed on this sheet."),
]


def main():
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    path = os.path.join(DATA, "daily_feed.json")
    existing = {}
    if os.path.isfile(path):
        try:
            existing = json.load(open(path, encoding="utf-8"))
        except (ValueError, OSError):
            existing = {}

    rows = list(SEED)
    # Keep any rows a previous live scrape produced that are not one of the
    # seed rows, so the scheduled refresh adds information rather than
    # replacing it.
    for r in existing.get("rows", []):
        if r.get("origin") == "read from the official document":
            continue
        if not any(s["name"] == r.get("name") and s["source"] == r.get("source") for s in rows):
            rows.append(r)

    documents = existing.get("documents", [])
    feed = {
        "generated_at": now,
        "verified_on": VERIFIED_ON,
        "note": ("Official daily Strip poker-room schedules. The rows below were read directly from the "
                 "official daily posters and structure sheets on " + VERIFIED_ON + ". A scheduled job "
                 "refreshes the feed from the same official documents; rows it cannot parse are kept "
                 "rather than dropped. Fields the documents do not state are left blank."),
        "sources": [
            {"label": "Official Wynn daily tournament poster", "url": SRC["wynn_poster"], "status": "read"},
            {"label": "Official Wynn daily tournament structures", "url": SRC["wynn_structures"], "status": "read"},
            {"label": "Official Bellagio Friday structure sheet", "url": SRC["bellagio_fri"], "status": "read"},
            {"label": "Official Bellagio Saturday structure sheet", "url": SRC["bellagio_sat"], "status": "read"},
            {"label": "Official Bellagio Sunday structure sheet", "url": SRC["bellagio_sun"], "status": "read"},
            {"label": "Wynn poker room", "url": SRC["wynn_poker"], "status": "read"},
            {"label": "Bellagio poker room", "url": SRC["bellagio_poker"], "status": "read"},
            {"label": "ARIA poker room", "url": SRC["aria_poker"], "status": "read"},
            {"label": "Venetian poker room", "url": SRC["venetian_poker"], "status": "read"},
        ],
        "documents": documents,
        "errors": existing.get("errors", []),
        "rows": rows,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(feed, f, indent=1)
    print("wrote %s (%d rows)" % (path, len(rows)))


if __name__ == "__main__":
    main()
