#!/usr/bin/env python3
"""Builds data/*.json from the rows verified against official sources.

Every row carries the official URL it was copied from, the excerpt that
supports each rule field, and the date the source was read. Nothing is
inferred: a field is left null when the official source does not state it.

Verification pass: session baba1a15, sources read 2026-11-16.
Run:  python3 scripts/build_data.py
"""
import json
import math, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
os.makedirs(DATA, exist_ok=True)

VERIFIED_ON = "2026-11-17"
LAST_CHECKED = "2026-11-17"

# Official documents re-read live on 2026-11-19, keyed by (series key, structure
# sheet number). Only the rows that cite that sheet get the later date: a row's
# last_checked and its rule excerpts' retrieval dates advance when *that document*
# was opened again, never because a neighbour's was. What the re-read found is
# written out per sheet, so a reader sees the clause rather than a bare date.
# Evidence and the field-by-field comparison:
# research/verification-2026-11-19-0f038248.md.
REREAD = {
    ("nov", 1): ("2026-11-19",
                 "re-read in full (session cebd4457); every printed clause, price, time and stack "
                 "still matches what the rows that cite this sheet store - "
                 "research/verification-2026-11-19-cebd4457.md"),
    ("nov", 5): ("2026-11-19",
                 "its ten numbered clauses still print no re-entry, rebuy, add-on or "
                 "multi-flight clause, so no written one-entry limit is published for this event"),
    ("nov", 8): ("2026-11-19",
                 "clause 07 still prices every buy-in after the initial one at $200, and its "
                 "thirteen numbered clauses print no add-on and no one-entry limit"),
    ("nov", 10): ("2026-11-19",
                  "clause 08 still reads \"Any player who bags chips for Day 2 may not play a "
                  "subsequent flight.\", the heading still reads \"Day A+C @ 11:10 AM with Day 2 "
                  "@ 12:00 PM\", and the sheet ends \"SEE OTHER STRUCTURE SHEET FOR DAYS B+D\""),
    ("nov", 29): ("2026-11-19",
                  "re-read in full (session cebd4457); every printed clause, price, time and stack "
                  "still matches what the rows that cite this sheet store - "
                  "research/verification-2026-11-19-cebd4457.md"),
    ("nov", 30): ("2026-11-19",
                  "re-read in full as the r012 source-change re-check (session cebd4457) and "
                  "identical to the archived snapshot on every published value: Event 08's $200 "
                  "PKO at 5:10 PM, 25,000 chips, late registration 8 levels plus break (~9:40 PM), "
                  "$8,000 guarantee including bounties, and clause 06's $40 house fee / $160 "
                  "prize-pool split"),
}

VEN = "The Venetian Resort"
WYN = "Wynn Las Vegas"

# ---------- official source URLs (all read on 2026-11-16) ----------
SRC = {
    "venetian_dse_series": "https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament.html",
    "venetian_quote_1118": "https://www.venetianlasvegas.com/booking?adults[]=2&arrival_date=2026-11-18&children[]=0&departure_date=2026-11-20&view=calendar",
    "dse_nov_page": "https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html",
    "dse_dec_page": "https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-dec-2026.html",
    "dse_nov_sched": "https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/dse-nov-2026-schedule.pdf",
    "dse_dec_sched": "https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/dse-dec-2026-schedule.pdf",
    "dse_nov_struct": "https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_{}.pdf",
    "dse_dec_struct": "https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_dec_2026-structure_{}.pdf",
    "venetian_poker": "https://www.venetianlasvegas.com/resort/casino/poker.html",
    "venetian_map": "https://www.venetianlasvegas.com/content/dam/vlvweb/resort/map.pdf",
    "venetian_fee": "https://www.venetianlasvegas.com/resort/resort-fee.html",
    "venetian_terms": "https://www.venetianlasvegas.com/legal/hotel-terms-and-conditions.html",
    "venetian_suite_rates": "https://www.venetianlasvegas.com/resort/casino/poker/suite-rates.html",
    "venetian_book": "https://www.venetianlasvegas.com/book",
    "wpt_sched": "https://cdn.wynnresorts.com/image/upload/v1757097329/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Schedule.pdf",
    "wpt_struct": "https://cdn.wynnresorts.com/image/upload/v1750864036/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Structures.pdf",
    "wss_sched": "https://cdn.wynnresorts.com/image/upload/v1753296112/visitwynn_pdfs_files/Poker/Wynn%20Signature%20Series/Wynn_Signature_Series_Schedule.pdf",
    "wss_struct": "https://cdn.wynnresorts.com/image/upload/v1762299460/visitwynn_pdfs_files/Poker/Wynn%20Signature%20Series/Wynn_Signature_Series_Structures.pdf",
    "wynn_daily_poster": "https://cdn.wynnresorts.com/image/upload/v1752011166/visitwynn_pdfs_files/Poker/Daily%20Tournaments/poker-daily-tournament-poster.pdf",
    "wynn_daily_struct": "https://cdn.wynnresorts.com/image/upload/v1752011191/visitwynn_pdfs_files/Poker/Daily%20Tournaments/Poker-All_Daily_Structures.pdf",
    "wynn_poker": "https://www.wynnlasvegas.com/casino/poker",
    "wynn_terms": "https://www.wynnlasvegas.com/terms-and-conditions/848671",
    "wynn_info": "https://www.wynnlasvegas.com/ai-information",
    "wynn_parking": "https://www.wynnlasvegas.com/about-us/parking",
    "bellagio": "https://bellagio.mgmresorts.com/en.html",
    "bellagio_poker": "https://bellagio.mgmresorts.com/en/casino/poker.html",
    "bellagio_terms": "https://bellagio.mgmresorts.com/en/terms-and-conditions.html",
    "bellagio_faq": "https://bellagio.mgmresorts.com/en/faq.html",
    # Bellagio's three weekly tournament structures, each linked from the official Bellagio poker page
    # and served from MGM Resorts' own asset host (PR #79 / session df94b75e, verified there).
    "bellagio_fri_pdf": "https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/"
                        "blt9cf95b0e60ec253e/6af491a3a9851d75c40be840/mgm-bellagio-poker-fridays-$600-nlh.pdf",
    "bellagio_sat_pdf": "https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/"
                        "blt6d47974bf5a7d9b6/6af491a391a6e8e4230c9e07/mgm-bellagio-poker-saturdays-$1000-nlh.pdf",
    "bellagio_sun_pdf": "https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/"
                        "blt07fcf1244a6da661/6af491a339e2b4f6b76a86ad/mgm-bellagio-poker-sundays-$400-horse.pdf",
    "aria": "https://aria.mgmresorts.com/en.html",
    "aria_poker": "https://aria.mgmresorts.com/en/casino/poker.html",
    "aria_terms": "https://aria.mgmresorts.com/en/terms-and-conditions.html",
    "mgm_parking": "https://www.mgmresorts.com/en/things-to-do/parking.html",
    "caesars": "https://www.caesars.com/caesars-palace",
    "caesars_poker_article": "https://www.caesars.com/las-vegas/explore/casino/poker-tournaments-las-vegas-strip",
    "caesars_faq": "https://www.caesars.com/caesars-palace/faqs",
    # Session ce9941b8: the official Caesars Palace casino page links this flyer under
    # "Caesars Palace Poker Room ... daily tournaments" / "View Schedule". It prints the
    # whole daily schedule with buy-ins, add-on, chips, level length, guarantee, the fee
    # split and the registration rule, so the daily feed no longer has to rest on an
    # editorial article (which now returns 404 - F78).
    "caesars_daily_flyer": ("https://www.caesars.com/content/dam/empire/clv/casino/poker/"
                            "tournament-schedule/clv-poker-daily-nlh-tournament-flyer-2026.pdf"),
    "caesars_casino": "https://www.caesars.com/caesars-palace/casino",
    # Caesars Palace casino page ("View Schedule"), as cited by the daily-format rows.
    "caesars_poker_page": "https://www.caesars.com/caesars-palace/casino/poker",
    "caesars_disclaimer": "https://www.caesars.com/corporate/disclaimer",
    # Session ce9941b8: the taxing authority. Clark County Department of Business
    # License, "General Information Guide for Transient Lodging Establishments"
    # (July 2021) — Appendix III prints the combined transient lodging tax rate by
    # establishment category and district, and the licensed-establishment table
    # prints each property's licence number, DBA name, address, status and rate.
    "clark_county_tle_guide": ("https://www.clarkcountynv.gov/adobe/assets/urn:aaid:aem:"
                               "689ef54f-ec0d-4bb6-b8ea-05a82887561f/original/as/"
                               "genl-info-guide-for-tles-july-2021.pdf"),
}

# ---------- rule excerpt strings reused by the Venetian structure sheets ----------
EX_SE = ("No re-entry, rebuy, add-on or multi-flight clause appears anywhere on this structure sheet "
         "(every numbered clause was read on 2026-11-16).")
EX_FLIGHT = ("Clause 08: \"Any player who bags chips for Day 2 may not play a subsequent flight.\" "
             "Later entry after busting is not addressed; exclude from the strict shortlist.")
EX_FLIGHT_EXPLICIT = ("Clause 08: \"Any player who bags chips for Day 2 may not play a subsequent flight. "
                      "Players who cash on Day 1 but bust before making Day 2 may play another flight.\"")
# The NYE $200 Bounty sheet (dse_dec_2026-structure_2.pdf, sheet 01) prints a CES-badge
# discount that "can be applied to the initial entry or any subsequent re-entry". A
# "subsequent re-entry" is a further entry, so the event is not single entry. The event
# scope is printed on the sheet's own heading: "Event #29 - $10 Rake Discount for showing
# your CES Badge", and the clause itself repeats "For Event #29 only".
EX_DISCOUNT_REENTRY = (
    "Clause 06: \"The $20 discount can be applied to the initial entry or any subsequent "
    "re-entry.\" A further entry is contemplated for this event, so it is not single entry. "
    "The sheet scopes the sentence to Event #29 itself (\"For Event #29 only\"); the other "
    "bounty events on the same sheet print no re-entry sentence either way.")
EX_SUBSEQUENT_BUYIN = ("Clause 07: \"All subsequent buy in's after the initial buy in will be $200.\" "
                       "Later buy-ins are allowed, so the event is not single entry.")

# ---------- Venetian DeepStack Extravaganza IV structure sheets (Nov 16 - Dec 23, 2026) ----------
# read on 2026-11-16. events = event numbers the sheet covers.
NOV_SHEETS = {
 1: dict(events=[9, 11, 13, 15, 21, 22, 23, 25, 60, 61, 62, 64], buy=200, fee=40, pool=160, start="17:10",
         chips=25000, levels=28, lmin=30, late="9:40 PM", status="CAND", labels=["bounty"]),
 2: dict(events=[7], buy=400, fee=70, pool=330, start="11:10", chips=40000, levels=30, lmin=40, late="5:55 PM",
         status="MULTI", labels=["multi-flight"], ex=EX_FLIGHT),
 3: dict(events=[19], buy=400, fee=70, pool=330, start="11:10", levels=30, lmin=40, late="5:55 PM",
         status="MULTI", labels=["multi-flight"], ex=EX_FLIGHT),
 4: dict(events=[59], buy=600, fee=95, pool=505, start="11:10", chips=20000, levels=30, lmin=40, late="5:55 PM",
         status="MULTI", labels=["multi-flight", "rake-discount"], ex=EX_FLIGHT),
 5: dict(events=[2, 12], buy=300, fee=58, pool=242, start="11:10", chips=20000, levels=28, lmin=30, late="4:55 PM",
         status="CAND", labels=[]),
 6: dict(events=[10], buy=400, fee=65, pool=335, chips=40000, start="11:10", levels=28, lmin=30, late="4:55 PM",
         status="CAND", labels=[]),
 7: dict(events=[14, 28, 63], buy=600, fee=90, pool=510, start="11:10", chips=20000, levels=28, lmin=30, late="4:55 PM",
         status="CAND", labels=[]),
 8: dict(events=[18, 58], buy=200, fee=40, pool=160, start="17:10", levels=28, lmin=30, late="9:40 PM",
         status="MULTI", labels=["bounty", "pokeratlas-discount"], ex=EX_SUBSEQUENT_BUYIN),
 9: dict(events=[1], buy=300, fee=60, pool=240, start="17:10", levels=30, lmin=30, late="8:40 PM",
         status="MULTI", labels=["multi-flight"], ex=EX_FLIGHT),
 10: dict(events=[1], buy=300, fee=60, pool=240, start="11:10", levels=30, lmin=40, late="3:40 PM",
          status="MULTI", labels=["multi-flight"], ex=EX_FLIGHT),
 11: dict(events=[16, 30, 54], buy=600, fee=90, pool=510, start="11:10", levels=28, lmin=30, late="4:55 PM",
          status="CAND", labels=["bounty"]),
 12: dict(events=[26], buy=800, fee=110, pool=690, start="11:10", levels=30, lmin=40, late="3:40 PM",
          status="MULTI", labels=["multi-flight"], ex=EX_FLIGHT),
 13: dict(events=[26], buy=800, fee=110, pool=690, start="17:10", levels=30, lmin=30, late="8:40 PM",
          status="MULTI", labels=["multi-flight"], ex=EX_FLIGHT),
 14: dict(events=[26], buy=800, fee=110, pool=690, start="17:10", levels=30, lmin=20, late="7:25 PM",
          status="MULTI", labels=["multi-flight", "turbo"], ex=EX_FLIGHT),
 15: dict(events=[29, 31, 34, 38, 42, 50, 51, 53, 55], buy=300, fee=50, pool=250, start="17:10",
          levels=28, lmin=30, late="9:40 PM", status="CAND", labels=["bounty"]),
 16: dict(events=[36], buy=800, fee=100, pool=700, start="11:10", levels=28, lmin=30, late="4:55 PM",
          status="CAND", labels=["bounty"]),
 17: dict(events=[24, 32], buy=600, fee=90, pool=510, start="10:10", levels=28, lmin=30, late="3:55 PM",
          status="CAND", labels=["seniors-50-plus"]),
 18: dict(events=[3, 4, 5], buy=200, fee=35, pool=165, start="10:10", chips=30000, levels=28, lmin=20,
          lmin2=15, lmin2_from=7, late="12:25 PM",
          status="CAND", labels=["raceday-stack"]),
 19: dict(events=[33, 37], buy=100, fee=20, pool=80, start="16:10", chips=20000, levels=28, lmin=20, late="6:25 PM",
          status="CAND", labels=["satellite", "milestone-satellite", "ladies"],
          seats=2, target="Event #39 ($800 No Limit Hold'em LIPS Ladies)",
          note="Milestone satellite: \"A Player who accumulates 200,000 in tournament chips (\"The Milestone\") or "
               "more will instantly receive direct entry into the $800 No Limit Hold'em LIPS ladies Event #39.\" "
               "Open to female players who must be 21+ and hold a Venetian Rewards card."),
 20: dict(events=[49], buy=1100, fee=140, pool=960, start="10:10", levels=29, lmin=40, late="4:55 PM",
          status="MULTI", labels=["multi-flight", "seniors-50-plus"], ex=EX_FLIGHT),
 21: dict(events=[47], buy=2200, fee=225, pool=1975, start="10:10", levels=29, lmin=40, late="4:55 PM",
          status="MULTI", labels=["multi-flight", "title-event"], ex=EX_FLIGHT),
 22: dict(events=[20], buy=300, fee=58, pool=242, start="12:10", levels=28, lmin=30, late="4:40 PM",
          status="CAND", labels=["plo", "double-board"]),
 23: dict(events=[57], buy=600, fee=90, pool=510, start="12:10", levels=28, lmin=30, late="4:40 PM",
          status="CAND", labels=["plo", "double-board"]),
 24: dict(events=[41, 44], buy=260, fee=40, pool=220, start="16:10", chips=20000, levels=28, lmin=20, late="6:25 PM",
          status="CAND", labels=["satellite", "milestone-satellite"],
          seats=2, target="Event #47 ($2,200 No Limit Hold'em PokerAtlas Championship Title Event)",
          note="Milestone satellite: \"A Player who accumulates 200,000 in tournament chips (\"The Milestone\") or "
               "more will instantly receive direct entry into the $2,200 No Limit Hold'em PokerAtlas Championship "
               "Title Event #47.\""),
 25: dict(events=[45, 46, 48], buy=260, fee=35, pool=225, start=None, chips=20000, levels=28, lmin=15, late=None,
          status="CAND", labels=["satellite", "milestone-satellite", "turbo"],
          seats=2, target="Event #47 ($2,200 No Limit Hold'em PokerAtlas Championship Title Event)",
          late_by_event={45: "9:40 PM", 46: "10:40 AM", 48: "1:40 PM"},
          note="Milestone satellite: \"A Player who accumulates 200,000 in tournament chips (\"The Milestone\") or "
               "more will instantly receive direct entry into the $2,200 No Limit Hold'em PokerAtlas Championship "
               "Title Event #47.\" The sheet prints a start time per event number (45: 8:10 PM, 46: 9:10 AM, "
               "48: 12:10 PM) and \"Late Registration: 6 levels\"."),
 26: dict(events=[17], buy=400, fee=60, pool=340, start="12:10", levels=28, lmin=30, late="4:40 PM",
          status="CAND", labels=["plo", "bounty"]),
 27: dict(events=[40], buy=600, fee=90, pool=510, start="12:10", levels=28, lmin=30, late="4:40 PM",
          status="CAND", labels=["plo", "bounty"]),
 28: dict(events=[27], buy=600, fee=90, pool=510, start="12:10", levels=28, lmin=30, late="4:40 PM",
          status="CAND", labels=["big-o"]),
 29: dict(events=[6], buy=200, fee=40, pool=160, start="11:10", levels=28, lmin=30, late="3:40 PM",
          status="CAND", labels=[]),
 30: dict(events=[8], buy=200, fee=40, pool=160, start="17:10", levels=28, lmin=30, late="9:40 PM",
          status="CAND", labels=["bounty", "pko"]),
 31: dict(events=[35], buy=600, fee=90, pool=510, start="10:10", levels=28, lmin=30, late="2:40 PM",
          status="CAND", labels=["tag-team", "lips"]),
 32: dict(events=[39], buy=800, fee=110, pool=690, start="10:10", levels=29, lmin=40, late="4:55 PM",
          status="CAND", labels=["ladies", "lips", "two-day"]),
 33: dict(events=[43], buy=600, fee=90, pool=510, start="11:10", levels=28, lmin=30, late="4:55 PM",
          status="CAND", labels=["bounty", "lips"]),
 34: dict(events=[52], buy=1100, fee=130, pool=970, start="11:10", levels=28, lmin=30, late="4:55 PM",
          status="CAND", labels=["bounty", "pko"]),
 35: dict(events=[56], buy=1100, fee=140, pool=960, start="10:10", levels=30, lmin=40, late="4:55 PM",
          status="MULTI", labels=["multi-flight", "rake-discount"], ex=EX_FLIGHT),
 36: dict(events=[56], buy=1100, fee=140, pool=960, start="18:10", levels=30, lmin=30, late="11:10 PM",
          status="MULTI", labels=["multi-flight", "rake-discount"], ex=EX_FLIGHT),
 37: dict(events=[47], buy=2200, fee=225, pool=1975, start="18:10", levels=30, lmin=30, late="11:10 PM",
          status="MULTI", labels=["multi-flight", "title-event"], ex=EX_FLIGHT),
}

# ---------- Venetian DeepStack Extravaganza NYE structure sheets (Dec 24, 2026 - Jan 10, 2027) ----------
DEC_SHEETS = {
 1: dict(events=[1, 3, 17], buy=400, fee=65, pool=335, start="11:10", levels=28, lmin=30, late="3:40 PM",
         status="CAND", labels=[]),
 2: dict(events=[2, 4, 13, 22, 26, 29, 32], buy=200, fee=40, pool=160, start="17:10", levels=28, lmin=30,
         late="9:40 PM", status="CAND", labels=["bounty"],
         note="Clause 06 mentions re-entry for Event #29 only (\"The $20 discount can be applied to the initial "
              "entry or any subsequent re-entry\"). Event #29 is listed as re-entry; the other events on this "
              "sheet have no re-entry clause of their own. Flagged for confirmation."),
 3: dict(events=[5], buy=600, fee=90, pool=510, start="11:10", levels=28, lmin=30, late="4:55 PM",
         status="CAND", labels=["bounty"]),
 4: dict(events=[6, 7, 9, 10, 11, 12], buy=260, fee=40, pool=220, start=None, levels=28, lmin=20, late=None,
         status="CAND", labels=["satellite", "milestone-satellite"],
         seats=4, target="Event #08 ($1,100 No Limit Hold'em Ante Up Championship)",
         late_by_event={6: "5:25 PM", 7: "8:25 PM", 9: "5:25 PM", 10: "8:25 PM", 11: "5:25 PM", 12: "8:25 PM"},
         note="Milestone satellite to the Ante Up Championship. The sheet prints start times per event number "
              "(06, 09 and 11 at 3:10 PM; 07, 10 and 12 at 6:10 PM) and \"Late Registration: 6 levels + Break "
              "(~5:25 PM or ~ 8:25 PM)\". The official event page describes the prize as \"1 in 5 (20%) Direct Entry "
              "into Event # 08\"."),
 5: dict(events=[15, 18, 21, 23, 24], buy=200, fee=35, pool=165, start=None, levels=28, lmin=20, late=None,
         status="CAND", labels=["satellite", "milestone-satellite"],
         seats=2, target="Event #20 ($1,600 No Limit Hold'em MSPT)",
         late_by_event={15: "5:25 PM", 18: "5:25 PM", 21: "5:25 PM", 23: "12:25 PM", 24: "5:25 PM"},
         note="Milestone satellite to the MSPT. The sheet prints start times per event number (15, 18, 21 and 24 "
              "at 3:10 PM; 23 at 10:10 AM) and \"Late Registration: 6 levels + Break (~5:25 PM or 12:25 PM)\"."),
 6: dict(events=[8], buy=1100, fee=140, pool=960, start="11:10", levels=30, lmin=40, late="5:55 PM",
         status="MULTI", labels=["multi-flight"], ex=EX_FLIGHT),
 7: dict(events=[16, 19], buy=200, fee=30, pool=170, start="18:10", levels=28, lmin=15, late="7:55 PM",
         status="CAND", labels=["satellite", "milestone-satellite", "turbo"],
         seats=2, target="Event #20 ($1,600 No Limit Hold'em MSPT)",
         note="Milestone satellite (turbo) to the MSPT. \"Late Registration: 6 levels + Break (~7:55 PM)\". "
              "\"$30 of the $200 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $170 "
              "of every $200 Buy In.\""),
 8: dict(events=[20], buy=1600, fee=180, pool=1420, start="11:10", levels=30, lmin=40, late="5:55 PM",
         status="MULTI", labels=["multi-flight", "rake-discount"], ex=EX_FLIGHT),
 9: dict(events=[25], buy=200, fee=40, pool=160, start="17:10", levels=28, lmin=30, late="9:40 PM",
         status="MULTI", labels=["bounty", "pokeratlas-discount"], ex=EX_SUBSEQUENT_BUYIN),
 10: dict(events=[31], buy=400, fee=65, pool=335, start="10:10", levels=28, lmin=30, late="3:55 PM",
          status="CAND", labels=["seniors-50-plus"]),
 11: dict(events=[28], buy=400, fee=65, pool=335, start="11:10", levels=28, lmin=30, late="4:55 PM",
          status="CAND", labels=[]),
 12: dict(events=[14], buy=600, fee=90, pool=510, start="11:10", levels=28, lmin=30, late="4:55 PM",
          status="CAND", labels=[]),
 13: dict(events=[30], buy=300, fee=60, pool=240, start="11:10", levels=30, lmin=40, late="3:40 PM",
          status="MULTI", labels=["multi-flight"], ex=EX_FLIGHT),
 14: dict(events=[30], buy=300, fee=60, pool=240, start="17:10", levels=30, lmin=30, late="8:40 PM",
          status="MULTI", labels=["multi-flight"], ex=EX_FLIGHT),
 15: dict(events=[27], buy=250, fee=50, pool=200, start="11:10", levels=30, lmin=30, late="3:40 PM",
          status="MULTI", labels=["multi-flight", "rake-discount"], ex=EX_FLIGHT_EXPLICIT),
}

# Event #29 on NYE sheet 2 carries its own re-entry clause.
DEC_EVENT_OVERRIDE = {
    ("dec", 29): dict(status="RE",
                      ex="Clause 06: \"The $20 discount can be applied to the initial entry or any subsequent re-entry.\""),
}

# ---------- Venetian DeepStack Extravaganza IV schedule rows (official event page) ----------
# date, start, event no, name, guarantee, sheet no (None = satellite / continuation)
DSE_NOV = [
 ("2026-11-16","11:10",1,"$300 No Limit Hold'em 1A $75K GTD",75000,10),
 ("2026-11-16","17:10",1,"$300 No Limit Hold'em 1B $75K GTD",75000,9),
 ("2026-11-17","11:10",1,"$300 No Limit Hold'em 1C $75K GTD",75000,10),
 ("2026-11-17","17:10",1,"$300 No Limit Hold'em 1D $75K GTD",75000,9),
 ("2026-11-18","11:10",2,"$300 No Limit Hold'em $10K GTD (1Day)",10000,5),
 ("2026-11-18","12:00",1,"$300 No Limit Hold'em Day 2 Restart",None,10),
 ("2026-11-19","10:10",3,"$200 NLH RaceDay Stack (1Day) - Race to finish before the Race",None,18),
 ("2026-11-20","10:10",4,"$200 NLH RaceDay Stack (1Day) - Race to finish before the Race",None,18),
 ("2026-11-21","10:10",5,"$200 NLH RaceDay Stack (1Day) - Race to finish before the Race",None,18),
 ("2026-11-22","11:10",6,"$200 No Limit Hold'em (1Day)",None,29),
 ("2026-11-23","11:10",7,"$400 No Limit Hold'em 1A $75K GTD",75000,2),
 ("2026-11-23","17:10",8,"$200 No Limit Hold'em Progressive Knock-Out Bounty $8K GTD (1Day)",8000,30),
 ("2026-11-24","11:10",7,"$400 No Limit Hold'em 1B $75K GTD",75000,2),
 ("2026-11-24","17:10",9,"$200 No Limit Hold'em Bounty $8K GTD (1Day)",8000,1),
 ("2026-11-25","11:00",7,"$400 No Limit Hold'em Day 2 Restart",None,2),
 ("2026-11-25","11:10",10,"$400 No Limit Hold'em $15K GTD (1Day)",15000,6),
 ("2026-11-25","17:10",11,"$200 No Limit Hold'em Bounty $8K GTD (1Day)",8000,1),
 ("2026-11-26","11:10",12,"$300 No Limit Hold'em $10K GTD (1Day)",10000,5),
 ("2026-11-26","17:10",13,"$200 No Limit Hold'em Bounty $8K GTD (1Day)",8000,1),
 ("2026-11-27","11:10",14,"$600 No Limit Hold'em $30K GTD (1Day)",30000,7),
 ("2026-11-27","17:10",15,"$200 No Limit Hold'em Bounty $8K GTD (1Day)",8000,1),
 ("2026-11-28","11:10",16,"$600 No Limit Hold'em Bounty $30K GTD (1Day) - $200 bounties to start & $500 bounties in the money",30000,11),
 ("2026-11-28","12:10",17,"$400 Pot Limit Omaha Bounty $15K GTD (1Day)",15000,26),
 ("2026-11-28","17:10",18,"$200 NLH PokerAtlas Valuetown Bounty $20K GTD (1Day) - PokerAtlas PRO member $20 rake discount",20000,8),
 ("2026-11-29","11:10",19,"$400 No Limit Hold'em 1A $75K GTD",75000,3),
 ("2026-11-29","12:10",20,"$300 Pot Limit Omaha Double Board Bomb Pot $10K GTD (1Day)",10000,22),
 ("2026-11-29","17:10",21,"$200 No Limit Hold'em Bounty $8K GTD (1Day)",8000,1),
 ("2026-11-30","11:10",19,"$400 No Limit Hold'em 1B $75K GTD",75000,3),
 ("2026-11-30","17:10",22,"$200 No Limit Hold'em Bounty $8K GTD (1Day)",8000,1),
 ("2026-12-01","11:10",19,"$400 No Limit Hold'em 1C $75K GTD",75000,3),
 ("2026-12-01","17:10",23,"$200 No Limit Hold'em Bounty $8K GTD (1Day)",8000,1),
 ("2026-12-02","10:10",24,"$600 No Limit Hold'em Seniors $40K GTD (1Day) - must be 50+ years of age",40000,17),
 ("2026-12-02","11:00",19,"$400 No Limit Hold'em Day 2 Restart",None,3),
 ("2026-12-02","17:10",25,"$200 No Limit Hold'em Bounty $8K GTD (1Day)",8000,1),
 ("2026-12-03","11:10",26,"$800 No Limit Hold'em 1A $500K GTD",500000,12),
 ("2026-12-03","12:10",27,"$600 BIG O $25K GTD (1Day)",25000,28),
 ("2026-12-03","17:10",26,"$800 No Limit Hold'em 1B $500K GTD",500000,13),
 ("2026-12-04","11:10",26,"$800 No Limit Hold'em 1C $500K GTD",500000,12),
 ("2026-12-04","17:10",26,"$800 No Limit Hold'em 1D $500K GTD",500000,13),
 ("2026-12-05","11:10",26,"$800 No Limit Hold'em 1E $500K GTD",500000,12),
 ("2026-12-05","17:10",26,"$800 No Limit Hold'em 1F (Turbo) $500K GTD",500000,14),
 ("2026-12-06","11:10",28,"$600 No Limit Hold'em $40K GTD (1Day)",40000,7),
 ("2026-12-06","12:00",26,"$800 No Limit Hold'em Day 2 Restart",None,12),
 ("2026-12-06","17:10",29,"$300 No Limit Hold'em Bounty $15K GTD (1Day)",15000,15),
 ("2026-12-07","11:10",30,"$600 No Limit Hold'em Bounty $40K GTD (1Day) - $200 bounties to start & $500 bounties in the money",40000,11),
 ("2026-12-07","17:10",31,"$300 No Limit Hold'em Bounty $15K GTD (1Day)",15000,15),
 ("2026-12-08","10:10",32,"$600 No Limit Hold'em Seniors $40K GTD (1Day) - must be 50+ years of age",40000,17),
 ("2026-12-08","16:10",33,"$100 NLH LIPS Ladies Milestone Satellite (1Day) - Awards Direct Entry to Event # 39",None,19),
 ("2026-12-08","17:10",34,"$300 No Limit Hold'em Bounty $15K GTD (1Day)",15000,15),
 ("2026-12-09","10:10",35,"$600 NLH LIPS Poker Jingle Tag Team $10K GTD (1Day) - tag teams consist of female/female or female/male",10000,31),
 ("2026-12-09","11:10",36,"$800 No Limit Hold'em Bounty $75K GTD (1Day) - $200 bounties to start & $500 bounties in the money",75000,16),
 ("2026-12-09","16:10",37,"$100 NLH LIPS Ladies Milestone Satellite (1Day) - Awards Direct Entry to Event # 39",None,19),
 ("2026-12-09","17:10",38,"$300 No Limit Hold'em Bounty $15K GTD (1Day)",15000,15),
 ("2026-12-10","10:10",39,"$800 No Limit Hold'em LIPS Ladies $40K GTD (2Day) - Women in Poker main event",40000,32),
 ("2026-12-10","12:10",40,"$600 Pot Limit Omaha Bounty $25K GTD (1Day)",25000,27),
 ("2026-12-10","16:10",41,"$260 NLH Milestone Satellite (1Day) - Awards Direct Entry to Event # 47",None,24),
 ("2026-12-10","17:10",42,"$300 No Limit Hold'em Bounty $15K GTD (1Day)",15000,15),
 ("2026-12-11","10:00",39,"$800 No Limit Hold'em LIPS Ladies Day 2 Restart - Play Down to Final 7 - Streamed Final Table (PokerGO)",None,32),
 ("2026-12-11","11:10",43,"$600 No Limit Hold'em LIPS $30K GTD (1Day) - KINGS and QUEENS bounty, open to all players",30000,33),
 ("2026-12-11","16:10",44,"$260 NLH Milestone Satellite (1Day) - Awards Direct Entry to Event # 47",None,24),
 ("2026-12-11","19:00",39,"$800 No Limit Hold'em LIPS Ladies Final Table - Streamed Final Table (PokerGO)",None,32),
 ("2026-12-11","20:10",45,"$260 NLH Turbo Milestone Satellite (1Day) - Awards Direct Entry to Event # 47",None,25),
 ("2026-12-12","09:10",46,"$260 NLH Turbo Milestone Satellite (1Day) - Awards Direct Entry to Event # 47",None,25),
 ("2026-12-12","10:10",47,"$2,200 No Limit Hold'em 1A $1 Mill GTD - PokerAtlas Championship title event",1000000,21),
 ("2026-12-12","12:10",48,"$260 NLH Turbo Milestone Satellite (1Day) - Awards Direct Entry to Event # 47",None,25),
 ("2026-12-12","18:10",47,"$2,200 No Limit Hold'em 1B $1 Mill GTD - PokerAtlas Championship title event",1000000,37),
 ("2026-12-13","10:10",49,"$1,100 No Limit Hold'em Seniors 1A $300K GTD - must be 50+ years of age",300000,20),
 ("2026-12-13","13:00",47,"$2,200 NLH PokerAtlas Championship title event Day 2 Restart - Play Down to Final 7 - Streamed Final Table (PokerGO)",None,21),
 ("2026-12-13","17:10",50,"$300 No Limit Hold'em Bounty $15K GTD (1Day)",15000,15),
 ("2026-12-14","10:10",49,"$1,100 No Limit Hold'em Seniors 1B $300K GTD - must be 50+ years of age",300000,20),
 ("2026-12-14","11:00",47,"$2,200 NLH PokerAtlas Championship title event Day 3 Restart - Streamed Final Table (PokerGO)",None,21),
 ("2026-12-14","17:10",51,"$300 No Limit Hold'em Bounty $15K GTD (1Day)",15000,15),
 ("2026-12-15","10:00",49,"$1,100 No Limit Hold'em Seniors Day 2 Restart",None,20),
 ("2026-12-15","11:10",52,"$1,100 No Limit Hold'em Progressive Knock-Out Bounty $75K GTD (1Day)",75000,34),
 ("2026-12-15","17:10",53,"$300 No Limit Hold'em Bounty $15K GTD (1Day)",15000,15),
 ("2026-12-16","11:10",54,"$600 No Limit Hold'em Bounty $50K GTD (1Day) - $200 bounties to start & $500 bounties in the money",50000,11),
 ("2026-12-16","17:10",55,"$300 No Limit Hold'em Bounty $15K GTD (1Day)",15000,15),
 ("2026-12-17","10:10",56,"$1,100 No Limit Hold'em 1A $500K GTD - $40 Rake Discount for Entries Before 10:10 a.m.",500000,35),
 ("2026-12-17","12:10",57,"$600 Pot Limit Omaha Double Board Bomb Pot $25K GTD (1Day)",25000,23),
 ("2026-12-17","18:10",56,"$1,100 No Limit Hold'em 1B $500K GTD - $40 Rake Discount for Entries Before 6:10 p.m.",500000,36),
 ("2026-12-18","10:10",56,"$1,100 No Limit Hold'em 1C $500K GTD",500000,35),
 ("2026-12-18","18:10",56,"$1,100 No Limit Hold'em 1D $500K GTD",500000,36),
 ("2026-12-19","10:10",56,"$1,100 No Limit Hold'em 1E $500K GTD",500000,35),
 ("2026-12-19","17:10",58,"$200 NLH PokerAtlas Valuetown Bounty $20K GTD (1Day) - PokerAtlas PRO member $20 rake discount",20000,8),
 ("2026-12-20","11:00",56,"$1,100 No Limit Hold'em Day 2 Restart",None,35),
 ("2026-12-20","11:10",59,"$600 No Limit Hold'em 1A $150K GTD - $20 Rake Discount for Entries Before 11:10 a.m.",150000,4),
 ("2026-12-20","17:10",60,"$200 No Limit Hold'em Bounty $8K GTD (1Day)",8000,1),
 ("2026-12-21","11:10",59,"$600 No Limit Hold'em 1B $150K GTD",150000,4),
 ("2026-12-21","17:10",61,"$200 No Limit Hold'em Bounty $8K GTD (1Day)",8000,1),
 ("2026-12-22","11:10",59,"$600 No Limit Hold'em 1C $150K GTD",150000,4),
 ("2026-12-22","17:10",62,"$200 No Limit Hold'em Bounty $8K GTD (1Day)",8000,1),
 ("2026-12-23","11:00",59,"$600 No Limit Hold'em Day 2 Restart",None,4),
 ("2026-12-23","11:10",63,"$600 No Limit Hold'em $30K GTD (1Day)",30000,7),
 ("2026-12-23","17:10",64,"$200 No Limit Hold'em Bounty $8K GTD (1Day)",8000,1),
]

# ---------- Venetian DeepStack Extravaganza NYE schedule rows (official event page) ----------
DSE_NYE = [
 ("2026-12-24","11:10",1,"$400 No Limit Hold'em $15K GTD (1Day)",15000,1),
 ("2026-12-24","17:10",2,"$200 No Limit Hold'em Bounty $8K GTD (1Day)",8000,2),
 ("2026-12-25","11:10",3,"$400 No Limit Hold'em $15K GTD (1Day)",15000,1),
 ("2026-12-25","17:10",4,"$200 No Limit Hold'em Bounty $8K GTD (1Day)",8000,2),
 ("2026-12-26","11:10",5,"$600 No Limit Hold'em Bounty $40K GTD (1Day) - $200 bounties to start & $500 bounties in the money",40000,3),
 ("2026-12-26","15:10",6,"$260 NLH Milestone Satellite (1Day) - Awards 1 in 5 (20%) Direct Entry into Event # 08",None,4),
 ("2026-12-26","18:10",7,"$260 NLH Milestone Satellite (1Day) - Awards 1 in 5 (20%) Direct Entry into Event # 08",None,4),
 ("2026-12-27","11:10",8,"$1,100 No Limit Hold'em 1A $300K GTD - Ante Up Championship",300000,6),
 ("2026-12-27","15:10",9,"$260 NLH Milestone Satellite (1Day) - Awards 1 in 5 (20%) Direct Entry into Event # 08",None,4),
 ("2026-12-27","18:10",10,"$260 NLH Milestone Satellite (1Day) - Awards 1 in 5 (20%) Direct Entry into Event # 08",None,4),
 ("2026-12-28","11:10",8,"$1,100 No Limit Hold'em 1B $300K GTD - Ante Up Championship",300000,6),
 ("2026-12-28","15:10",11,"$260 NLH Milestone Satellite (1Day) - Awards 1 in 5 (20%) Direct Entry into Event # 08",None,4),
 ("2026-12-28","18:10",12,"$260 NLH Milestone Satellite (1Day) - Awards 1 in 5 (20%) Direct Entry into Event # 08",None,4),
 ("2026-12-29","11:10",8,"$1,100 No Limit Hold'em 1C $300K GTD - Ante Up Championship",300000,6),
 ("2026-12-29","17:10",13,"$200 No Limit Hold'em Bounty $8K GTD (1Day)",8000,2),
 ("2026-12-30","11:00",8,"$1,100 No Limit Hold'em Ante Up Day 2 Restart - Play Down to Final 7 - Streamed Final Table (POKERGO)",None,6),
 ("2026-12-30","11:10",14,"$600 No Limit Hold'em $50K GTD (1Day)",50000,12),
 ("2026-12-30","15:10",15,"$200 NLH Milestone Satellite (1Day) - Awards Direct Entry into Event # 20",None,5),
 ("2026-12-30","18:10",16,"$200 NLH Turbo Milestone Satellite (1Day) - Awards Direct Entry into Event # 20",None,7),
 ("2026-12-31","10:00",8,"$1,100 No Limit Hold'em Ante Up Day 3 Restart - Streamed Final Table (POKERGO)",None,6),
 ("2026-12-31","11:10",17,"$400 No Limit Hold'em $15K GTD (1Day)",15000,1),
 ("2026-12-31","15:10",18,"$200 NLH Milestone Satellite (1Day) - Awards Direct Entry into Event # 20",None,5),
 ("2026-12-31","18:10",19,"$200 NLH Turbo Milestone Satellite (1Day) - Awards Direct Entry into Event # 20",None,7),
 ("2027-01-01","11:10",20,"$1,600 No Limit Hold'em MSPT 1A $400K GTD - $40 Reduced Rake until the start of Level 4",400000,8),
 ("2027-01-01","15:10",21,"$200 NLH Milestone Satellite (1Day) - Awards Direct Entry into Event # 20",None,5),
 ("2027-01-01","17:10",22,"$200 No Limit Hold'em Bounty $8K GTD (1Day)",8000,2),
 ("2027-01-02","10:10",23,"$200 NLH Milestone Satellite (1Day) - Awards Direct Entry into Event # 20",None,5),
 ("2027-01-02","11:10",20,"$1,600 No Limit Hold'em MSPT 1B $400K GTD",400000,8),
 ("2027-01-02","15:10",24,"$200 NLH Milestone Satellite (1Day) - Awards Direct Entry into Event # 20",None,5),
 ("2027-01-02","17:10",25,"$200 NLH PokerAtlas Valuetown Bounty $20K GTD (1Day) - PokerAtlas PRO member $20 rake discount",20000,9),
 ("2027-01-03","11:10",20,"$1,600 No Limit Hold'em MSPT 1C $400K GTD",400000,8),
 ("2027-01-03","17:10",26,"$200 No Limit Hold'em Bounty $8K GTD (1Day)",8000,2),
 ("2027-01-04","11:00",20,"$1,600 No Limit Hold'em MSPT Day 2 Restart",None,8),  # kept at 11:00 per main's F55 decision (the earlier of the two official readings, so a player cannot be late for either); PR #64 (session c7a324a6) carried 11:10 from the event page - the conflict flag MSPT_DAY2_START_CONFLICT carries both texts
 ("2027-01-04","11:10",27,"$250 No Limit Hold'em 1A $75K GTD (1Day) - Day 1 Payouts with 5% advancing to Day 2 - $10 Reduced Rake for Entry before 11:10 AM",75000,15),
 ("2027-01-04","17:10",27,"$250 No Limit Hold'em 1B $75K GTD (1Day) - Day 1 Payouts with 5% advancing to Day 2 - $10 Reduced Rake for Entry before 5:10 PM",75000,15),
 ("2027-01-05","11:10",27,"$250 No Limit Hold'em 1C $75K GTD (1Day) - Day 1 Payouts with 5% advancing to Day 2",75000,15),
 ("2027-01-05","17:10",27,"$250 No Limit Hold'em 1D $75K GTD (1Day) - Day 1 Payouts with 5% advancing to Day 2",75000,15),
 ("2027-01-06","11:10",28,"$400 No Limit Hold'em $15K GTD (1Day)",15000,11),
 ("2027-01-06","12:00",27,"$250 No Limit Hold'em Day 2 Restart",None,15),
 ("2027-01-06","17:10",29,"$200 No Limit Hold'em Bounty $8K GTD (1Day) - Show Your CES Badge - $10 Rake Discount",8000,2),
 ("2027-01-07","11:10",30,"$300 No Limit Hold'em 1A $100K GTD (1Day)",100000,13),
 ("2027-01-07","17:10",30,"$300 No Limit Hold'em 1B $100K GTD (1Day) - Show Your CES Badge - $10 Rake Discount",100000,14),
 ("2027-01-08","11:10",30,"$300 No Limit Hold'em 1C $100K GTD (1Day)",100000,13),
 ("2027-01-08","17:10",30,"$300 No Limit Hold'em 1D $100K GTD (1Day) - Show Your CES Badge - $10 Rake Discount",100000,14),
 ("2027-01-09","11:10",30,"$300 No Limit Hold'em 1E $100K GTD (1Day)",100000,13),
 # 2026-11-17 audit: the official NYE page prints the "Show Your CES Badge - $10 RAKE DISCOUNT" second
 # line on the Jan 6 Bounty event and on only two of the six Event #30 flights (Jan 7 1B, Jan 8 1D). It is
 # NOT printed on this Jan 9 1F row (nor on 1A/1C/1E), so the clause is removed from the published name.
 ("2027-01-09","17:10",30,"$300 No Limit Hold'em 1F $100K GTD (1Day)",100000,14),
 ("2027-01-10","10:10",31,"$400 No Limit Hold'em Seniors $20K GTD (1Day) - must be 50+ years of age",20000,10),
 ("2027-01-10","12:00",30,"$300 No Limit Hold'em Day 2 Restart",None,13),
 ("2027-01-10","17:10",32,"$200 No Limit Hold'em Bounty $8K GTD (1Day)",8000,2),
]

# Printed anomalies on the official Venetian pages, carried into the row as a flag.
DATE_TYPO_DEC26 = ("Official page typo: the New York Year's Eve event page prints this row as "
                   "\"Saturday, December 26, 2025\". The series header reads \"December 24, 2026 - January 10, "
                   "2027\" and the printed weekday (Saturday) matches December 26, 2026, so the row is stored "
                   "with the year 2026 and the printed year is treated as a typo.")
DATE_TYPO_TUESDAY = ("Official page typo: the New Year\'s Eve event page prints \"Tuesaday, January 5, 2027\" "
                      "for this row. January 5, 2027 is a Tuesday, so the stored date is unchanged.")

# Two official Venetian pages state different start times for the same Day 2 restart.
# Recorded as a conflict rather than silently resolved: the stored time is the earlier
# one, so a player who plans around it is never late for whichever is correct.
MSPT_DAY2_START_CONFLICT = (
    "Two official sources disagree on this start time. The New Year's Eve event page prints "
    "\"Monday, January 4, 2027 | 11:10 AM | 20 | $1,600 No Limit Hold'em MSPT Day 2 Restart\" "
    "(re-read live on 2026-11-17), while structure sheet #8 clause 3 prints \"Day 2 will resume at "
    "11:00 AM combining all remaining players from 1A, 1B, and 1C\". The row is stored at the "
    "earlier 11:00 AM so that a player planning around it cannot be late for either reading; "
    "confirm with the poker room before travelling. The sheet's own \"Late Registration: 9 levels "
    "+ Break (~ 5:55 PM)\" is measured from the 11:10 AM Day 1 flights, not from this restart, so "
    "it does not settle the question.")

# LIPS structure sheets withhold two separate amounts from the buy-in: a house fee (Rake +
# Staff) and a separate flat fee for Vegas Connected, INC, DBA Ladies International Poker
# Series (LIPS). The numeric house_fee_usd stores the pure house fee only; the LIPS flat fee
# is kept in its own field so the two are never conflated (read from the sheets on 2026-11-16).
LIPS_FEE_FLAG = ("The structure sheet withholds two separate amounts from the buy-in: the house fee "
                 "(Rake + Staff) and a flat fee for Vegas Connected, INC, DBA Ladies International Poker "
                 "Series (LIPS). house_fee_usd stores the pure house fee only; the LIPS flat fee is stored "
                 "separately in lips_fee_usd. The prize pool is the buy-in less both withholdings.")

# The official structure sheet #30 was re-published between 2026-11-16 and 2026-11-19. A hand
# re-read of the live sheet on 2026-11-19 (session a3822303) against the archived captures shows
# the change exactly: clause 9 (bounty mechanics) was expanded - the eliminated player's bounty
# is now split between a cash payout and an increase to the eliminator's bounty, with an explicit
# whole-dollar rounding rule - and several clauses re-wrapped to different line lengths. Every
# published value on the row (start time, buy-in, guarantee, fee split, registration close,
# payout percentage, entry rules) is unchanged. Recorded as a flag, not as a value change.
STRUCT30_CLAUSE9_REWORDED = (
    "The official structure sheet was re-published after this row was first read: a hand re-read "
    "on 2026-11-19 compared the live sheet with the 2026-11-16 and 2026-11-19 archives line by "
    "line. Clause 9 (bounty mechanics) now adds that the eliminated player's bounty is split "
    "equally between a cash payout to the eliminating player and an increase to that player's own "
    "bounty, with the cash rounded down to the nearest whole dollar when the bounty does not "
    "divide evenly; several clauses also re-wrapped to different line lengths. None of the "
    "row's published values changed (date, start, buy-in, guarantee, fee split, registration "
    "close, payout percentage and entry-rule findings are identical), and the re-read found no "
    "re-entry, rebuy or add-on wording. Source: structure sheet #30, re-read live 2026-11-19.")

# ---------- Wynn WPT World Championship schedule rows (official schedule PDF, read 2026-11-16) ----------
# date, time, name, buy-in, guarantee (None = no dollar guarantee), guarantee text,
# published chips, published levels, kind, structure key, flags
WPT = [
 ("2026-11-27","11:00","No Limit Hold'em Day 1A",600,400000,None,40000,"30/40","entry","NLH600",[]),
 ("2026-11-27","12:00","TORSE",600,None,None,35000,"30","entry","TORSE600",[]),
 ("2026-11-27","13:00","PLO",400,None,None,30000,"30","entry","PLO400",[]),
 ("2026-11-27","17:00","No Limit Hold'em Day 1B",600,400000,None,40000,"30/40","entry","NLH600",[]),
 ("2026-11-28","11:00","No Limit Hold'em Day 1C",600,400000,None,40000,"30/40","entry","NLH600",[]),
 ("2026-11-28","12:00","Mixed Triple Draw (A-5, 2-7, Badugi)",600,None,None,35000,"30","entry","MTD600",[]),
 ("2026-11-28","17:00","No Limit Hold'em Day 1D",600,400000,None,40000,"30/40","entry","NLH600",[]),
 ("2026-11-29","11:00","No Limit Hold'em Day 1E",600,400000,None,40000,"30/40","entry","NLH600",[]),
 ("2026-11-29","18:00","No Limit Hold'em Day 1F",600,400000,None,40000,"20/40","entry","NLH600",
  ["The structure sheet plays Day 1F in 20-minute levels: \"Day 1F: 20 minutes per level until 12.5% or less of the field remains.\""]),
 ("2026-11-30","11:00","No Limit Hold'em Day 1A",800,1000000,None,40000,"30/40","entry","NLH800",[]),
 ("2026-11-30","12:00","Limit Omaha 8",600,None,None,35000,"30","entry","LO8",[]),
 ("2026-11-30","13:00","No Limit Hold'em Day 2",800,1000000,None,40000,"30/40","continuation","NLH600",
  ["Continuation row. The $600 No Limit Hold'em structure sheet prints \"Day 2: Monday, November 30, 2026 at 1 p.m.\""]),
 ("2026-11-30","17:00","No Limit Hold'em Day 1B",800,1000000,None,40000,"30/40","entry","NLH800",[]),
 ("2026-12-01","11:00","No Limit Hold'em Day 1C",800,1000000,None,40000,"30/40","entry","NLH800",[]),
 ("2026-12-01","12:00","Limit Omaha 8/Stud 8",600,None,None,35000,"30","entry","LO8S8",[]),
 ("2026-12-01","13:00","PLO",1100,None,None,30000,"30","entry","PLO1100",[]),
 ("2026-12-01","17:00","No Limit Hold'em Day 1D",800,1000000,None,40000,"30/40","entry","NLH800",[]),
 ("2026-12-02","11:00","No Limit Hold'em Day 1E",800,1000000,None,40000,"30/40","entry","NLH800",[]),
 ("2026-12-02","18:00","No Limit Hold'em Day 1F",800,1000000,None,40000,"20/40","entry","NLH800",
  ["The structure sheet plays Day 1F in 20-minute levels: \"Day 1F: 20 minutes per level until 12.5% or less of the field remains.\""]),
 ("2026-12-03","11:00","No Limit Hold'em Day 1A",1600,1000000,None,40000,"40","entry","NLH1600",[]),
 ("2026-12-03","13:00","No Limit Hold'em Day 2",1600,1000000,None,40000,"40","continuation","NLH800",
  ["Continuation row of the $800 No Limit Hold'em event: the structure sheet prints \"Day 2: Thursday, December 3, 2026 at 1 p.m.\"",
   "The schedule PDF prints $1,600 in the buy-in column of this row; the structure sheet shows the day belongs to the $800 event."]),
 ("2026-12-03","19:00","Double Play Milestone Satellite (2 X $1,100 Ticket)",400,None,"25 Prizes",20000,"20","entry","SAT_WPT",[]),
 ("2026-12-04","11:00","No Limit Hold'em Day 1B",1600,1000000,None,40000,"40","entry","NLH1600",[]),
 ("2026-12-04","12:00","HORSE",600,None,None,35000,"30","entry","HORSE600",[]),
 ("2026-12-04","13:00","No Limit Hold'em Final Table",None,None,None,None,None,"continuation","NLH800",
  ["Continuation row of the $800 No Limit Hold'em event: the structure sheet prints \"Final Table: Friday, December 4, 2026 at 1 p.m.\"",
   "The schedule PDF prints no buy-in, guarantee, chips or levels for this row."]),
 ("2026-12-04","19:00","Double Play Milestone Satellite (2 X $1,100 Ticket)",400,None,"25 Prizes",20000,"20","entry","SAT_WPT",[]),
 ("2026-12-05","11:00","No Limit Hold'em Day 2",1600,1000000,None,40000,"40/60","continuation","NLH1600",
  ["Continuation row of the $1,600 No Limit Hold'em event: the structure sheet prints \"Day 2: Saturday, December 5, 2026 at 11 a.m.\"",
   "The schedule PDF prints $1,100 in the buy-in column of this row; the structure sheet shows the day belongs to the $1,600 event."]),
 ("2026-12-05","11:00","WPT Prime Championship Day 1A",1100,5000000,None,40000,"40/60","entry","PRIME",[]),
 ("2026-12-05","21:00","NLH Turbo",600,50000,None,30000,"20","entry","TURBO600",[]),
 ("2026-12-06","11:00","WPT Prime Championship Day 1B",1100,5000000,None,40000,"40/60","entry","PRIME",[]),
 ("2026-12-06","11:00","PLO Mystery Bounty Day 1A",1600,500000,None,40000,"40","entry","PLOMYST",[]),
 ("2026-12-06","12:00","Milestone Satellite to $1,100 Prime Championship",200,None,"50 Seats",20000,"20","entry","SAT_WPT",[]),
 ("2026-12-06","18:00","PLO Mystery Bounty Day 1B",1600,500000,None,40000,"20/40","entry","PLOMYST",[]),
 ("2026-12-06","19:00","Double Play Milestone Satellite (2 X $1,100 Ticket)",400,None,"25 Prizes",20000,"20","entry","SAT_WPT",[]),
 ("2026-12-06","21:00","NLH Turbo",600,50000,None,30000,"20","entry","TURBO600",[]),
 ("2026-12-07","11:00","WPT Prime Championship Day 1C",1100,5000000,None,40000,"40/60","entry","PRIME",[]),
 ("2026-12-07","11:00","HORSE (2 Day)",1100,None,None,40000,"40","entry",None,[]),
 ("2026-12-07","12:00","PLO Mystery Bounty Day 2",None,None,None,None,None,"continuation","PLOMYST",
  ["Continuation row. The structure sheet prints \"Day 2: Monday, December 7, 2026, at 12 p.m.\"",
   "The schedule PDF prints no buy-in, guarantee, chips or levels for this row."]),
 ("2026-12-07","13:00","PLO $500 Bounty",1600,100000,None,30000,"30","entry",None,[]),
 ("2026-12-07","19:00","Milestone Satellite Package to Prime and World Championship",1600,None,"25 Prizes",20000,"25","entry","SAT_WPT",[]),
 ("2026-12-07","21:00","NLH Turbo",600,50000,None,30000,"20","entry","TURBO600",[]),
 ("2026-12-08","11:00","WPT Prime Championship Day 1D",1100,5000000,None,40000,"40/60","entry","PRIME",[]),
 ("2026-12-08","19:00","Milestone Satellite to $10,400 World Championship",1100,None,"25 Seats",20000,"25","entry","SAT_WPT",[]),
 ("2026-12-08","21:00","NLH Turbo",600,50000,None,30000,"20","entry","TURBO600",[]),
 ("2026-12-09","11:00","No Limit Hold'em (2 Day)",1600,1000000,None,40000,"40","entry",None,[]),
 ("2026-12-09","12:00","WPT Prime Championship Day 2",None,None,None,None,None,"continuation","PRIME",
  ["Continuation row. The structure sheet prints \"Day 2: Wednesday, December 9, 2026 at 12 p.m.\"",
   "The schedule PDF prints no buy-in, guarantee, chips or levels for this row."]),
 ("2026-12-09","13:00","PLO $1,000 Bounty",3000,250000,None,30000,"30","entry",None,[]),
 ("2026-12-09","13:00","Limit Omaha 8",800,None,None,35000,"30","entry",None,[]),
 ("2026-12-09","14:00","Milestone Satellite to $10,400 World Championship",1100,None,"25 Seats",20000,"25","entry","SAT_WPT",[]),
 ("2026-12-09","19:00","Milestone Satellite to $10,400 World Championship",1100,None,"25 Seats",20000,"25","entry","SAT_WPT",[]),
 ("2026-12-09","21:00","NLH Turbo",600,50000,None,30000,"20","entry","TURBO600",[]),
 ("2026-12-10","10:00","Super Gold Million Mystery Bounty Day 1A",400,3000000,None,30000,"30/40","entry",None,[]),
 ("2026-12-10","12:00","WPT Prime Championship Day 3",None,None,None,None,None,"continuation","PRIME",
  ["Continuation row. The structure sheet prints \"Day 3: Thursday, December 10, 2026 at 12 p.m.\"",
   "The schedule PDF prints no buy-in, guarantee, chips or levels for this row."]),
 ("2026-12-10","18:00","Super Gold Million Mystery Bounty Day 1B",400,3000000,None,30000,"20/40","entry",None,[]),
 ("2026-12-11","10:00","Super Gold Million Mystery Bounty Day 1C",400,3000000,None,30000,"30/40","entry",None,[]),
 ("2026-12-11","12:00","WPT Prime Championship Day 4",None,None,None,None,None,"continuation","PRIME",
  ["Continuation row. The structure sheet prints \"Day 4: Friday, December 11, 2026 at 12 p.m.\"",
   "The schedule PDF prints no buy-in, guarantee, chips or levels for this row."]),
 ("2026-12-11","18:00","Super Gold Million Mystery Bounty Day 1D",400,3000000,None,30000,"20/40","entry",None,[]),
 ("2026-12-12","10:00","No Limit Hold'em",800,100000,None,30000,"30","entry",None,[]),
 ("2026-12-12","13:00","PLO",3000,250000,None,30000,"30","entry",None,[]),
 ("2026-12-12","14:00","WPT Prime Championship Final Table",None,None,None,None,None,"continuation","PRIME",
  ["Continuation row. The structure sheet prints \"Final Table: Saturday, December 12, 2026 at 2 p.m.\"",
   "The schedule PDF prints no buy-in, guarantee, chips or levels for this row."]),
 ("2026-12-12","14:00","Super Gold Million Mystery Bounty Day 2",None,None,None,None,None,"continuation",None,
  ["Continuation row. The schedule PDF prints no buy-in, guarantee, chips or levels for this row and no structure "
   "sheet for this event is published."]),
 ("2026-12-12","14:00","Milestone Satellite to $10,400 World Championship 1A/B",1100,None,"75 Seats",20000,"25","entry","SAT_WPT",[]),
 ("2026-12-12","16:00","Milestone Satellite to $1,100 Ladies NLH Championship",200,None,"10 Seats",20000,"20","entry","SAT_WPT",[]),
 ("2026-12-12","19:00","Milestone Satellite to $10,400 World Championship 1A/B",1100,None,"25 Seats",20000,"25","entry","SAT_WPT",[]),
 ("2026-12-12","21:00","NLH Turbo",600,50000,None,30000,"20","entry","TURBO600",[]),
 ("2026-12-13","11:00","WPT World Championship Day 1A $1,000,000 Added",10400,None,None,100000,"60/90","entry",None,
  ["Schedule footnote: \"$1,000,000 will be added in cash prizes by ClubWPT Gold. ClubWPT Gold is not available in Nevada.\""]),
 ("2026-12-13","11:00","Ladies NLH Championship (2 Day)",1100,250000,None,40000,"40","entry",None,
  ["Schedule footnote: \"The Tournament Entry for the Ladies Championship is $11,100. Ladies will receive a discounted entry.\"",
   "The published $1,100 buy-in therefore does not apply to the ladies field."]),
 ("2026-12-13","11:00","TORSE (2 Day)",1100,None,None,40000,"40","entry","TORSE1100",
  ["Restored on 2026-11-17: the official WPT schedule PDF prints this row (Dec. 13 Sunday, 11 a.m., $1,100, 40,000 chips, 40-minute levels) and the earlier build omitted it.",
   "Re-entry: the official structures PDF block for the $1,100 TORSE (2 Day) prints \"Unlimited re-entry will be available until the start of level 10\"."]),
 ("2026-12-13","11:00","No Limit Hold'em Day 1A",800,500000,None,40000,"40","entry",None,[]),
 ("2026-12-13","12:00","PLO Day 1A",1600,1000000,None,40000,"40","entry",None,[]),
 ("2026-12-13","12:00","Milestone Satellite to $10,400 World Championship 1B",1100,None,"25 Seats",20000,"25","entry","SAT_WPT",[]),
 ("2026-12-13","13:00","Super Gold Million Mystery Bounty Day 3",None,None,None,None,None,"continuation",None,
  ["Continuation row. The schedule PDF prints no buy-in, guarantee, chips or levels for this row and no structure "
   "sheet for this event is published."]),
 ("2026-12-13","18:00","Milestone Satellite to $10,400 World Championship 1B/C",1100,None,"25 Seats",20000,"25","entry","SAT_WPT",[]),
 ("2026-12-14","11:00","WPT World Championship Day 1B $1,000,000 Added",10400,None,None,100000,"60/90","entry",None,
  ["Schedule footnote: \"$1,000,000 will be added in cash prizes by ClubWPT Gold. ClubWPT Gold is not available in Nevada.\""]),
 ("2026-12-14","11:00","No Limit Hold'em Day 1B",800,500000,None,40000,"40","entry",None,[]),
 ("2026-12-14","12:00","PLO Day 1B",1600,1000000,None,40000,"40","entry",None,[]),
 ("2026-12-14","12:00","Mixed Triple Draw (A-5, 2-7, Badugi) (2 Day)",1100,None,None,40000,"40","entry",None,[]),
 ("2026-12-14","12:00","Milestone Satellite to $10,400 World Championship 1C",1100,None,"25 Seats",20000,"25","entry","SAT_WPT",[]),
 ("2026-12-14","14:00","Super Gold Million Mystery Bounty Final Table",None,None,None,None,None,"continuation",None,
  ["Continuation row. The schedule PDF prints no buy-in, guarantee, chips or levels for this row and no structure "
   "sheet for this event is published."]),
 ("2026-12-14","18:00","Milestone Satellite to $10,400 World Championship 1C",1100,None,"25 Seats",20000,"25","entry","SAT_WPT",[]),
 ("2026-12-14","19:00","PLO Turbo",1100,100000,None,30000,"20","entry",None,[]),
 ("2026-12-14","21:00","NLH Turbo",600,50000,None,30000,"20","entry",None,
  ["The $600 NLH Turbo structure sheet lists \"Monday, December 14, 2026 at 9 p.m.\" for the $600 turbo; the schedule "
   "PDF prints this row as \"NLH Turbo\" with a $600 buy-in and a $50,000 guarantee. (Name corrected 2026-11-17 from "
   "the transcription \"NIH Turbo\" - no official document ever printed NIH; PR #52 session ca6d75b1 found it and "
   "session df94b75e verified the correction against data/snapshots/wpt_sched.txt.)"]),
 ("2026-12-15","11:00","WPT World Championship Day 1C $1,000,000 Added",10400,None,None,100000,"60/90","entry",None,
  ["Schedule footnote: \"$1,000,000 will be added in cash prizes by ClubWPT Gold. ClubWPT Gold is not available in Nevada.\""]),
 ("2026-12-15","11:00","No Limit Hold'em Day 2",None,None,None,None,None,"continuation",None,
  ["Continuation row. The schedule PDF prints no buy-in, guarantee, chips or levels for this row and no structure "
   "sheet for this event is published. Day 1A and Day 1B of the $800 No Limit Hold'em $500,000 event are printed "
   "for December 13-14 at 11 a.m.; the parent event is not stated in the source."]),
 ("2026-12-15","11:00","Milestone Satellite to $10,400 World Championship 1C/Day 2",1100,None,"10 Seats",20000,"25","entry","SAT_WPT",[]),
 ("2026-12-15","12:00","PLO Day 2",None,None,None,None,None,"continuation",None,
  ["Continuation row. The schedule PDF prints no buy-in, guarantee, chips or levels for this row and no structure "
   "sheet for this event is published."]),
 ("2026-12-15","12:00","Big O",1100,None,None,30000,"30","entry",None,[]),
 ("2026-12-15","13:00","PLO Progressive Bounty (PKO)",3000,250000,None,30000,"30","entry",None,[]),
 ("2026-12-15","18:00","Milestone Satellite to $10,400 World Championship Day 2",1100,None,"10 Seats",20000,"25","entry","SAT_WPT",[]),
 ("2026-12-15","19:00","NLH $500 Bounty Turbo",1600,100000,None,30000,"20","entry",None,[]),
 ("2026-12-16","11:00","No Limit Hold'em Day 1A",1100,1000000,None,40000,"40","entry",None,
  ["Printed on the schedule PDF under the heading \"Dec. 18 Wednesday\". December 18, 2026 is a Friday and the PDF "
   "prints \"Dec. 18 Friday\" for a separate block, so this block is stored as December 16, 2026 (a Wednesday). "
   "This also fits the WPT World Championship day order: Day 1A (December 13), Day 1B (December 14), Day 1C "
   "(December 15), Day 2 (December 16)."]),
 ("2026-12-16","12:00","WPT World Championship Day 2 (Registration open until the start of Day 2)",None,None,None,100000,"60/90","continuation",None,
  ["Continuation row. Printed under the heading \"Dec. 18 Wednesday\" on the schedule PDF and stored as December 16, 2026.",
   "The schedule PDF prints no buy-in or guarantee for this row."]),
 ("2026-12-16","12:00","PLO Double Board Bomb Pot",800,None,None,30000,"30","entry",None,
  ["Printed on the schedule PDF under the heading \"Dec. 18 Wednesday\" and stored as December 16, 2026."]),
 ("2026-12-16","13:00","PLO 6-Max",10500,None,None,100000,"30/40","entry",None,
  ["Printed on the schedule PDF under the heading \"Dec. 18 Wednesday\" and stored as December 16, 2026.",
   "Schedule footnote: \"Players registered prior to the start of the event will receive a discounted entry.\""]),
 ("2026-12-16","13:00","HORSE",800,None,None,35000,"30","entry",None,
  ["Printed on the schedule PDF under the heading \"Dec. 18 Wednesday\" and stored as December 16, 2026."]),
 ("2026-12-16","18:00","Milestone Satellite to $25K NLH High Roller",3000,None,None,20000,"25","entry","SAT_WPT",
  ["Printed on the schedule PDF under the heading \"Dec. 18 Wednesday\" and stored as December 16, 2026.",
   "Schedule footnote: \"Players registered prior to the start of the event will receive a discounted entry.\""]),
 ("2026-12-16","18:00","Milestone Satellite to $3,000 NLH",400,None,"25 Seats",20000,"20","entry","SAT_WPT",
  ["Printed on the schedule PDF under the heading \"Dec. 18 Wednesday\" and stored as December 16, 2026."]),
 ("2026-12-16","19:00","No Limit Hold'em Day 1B",1100,1000000,None,40000,"20/40","entry",None,
  ["Printed on the schedule PDF under the heading \"Dec. 18 Wednesday\" and stored as December 16, 2026."]),
 ("2026-12-17","11:00","Seniors NLH Championship (3 Day)",1100,500000,None,40000,"40","entry",None,[]),
 ("2026-12-17","11:00","Wynn Mixed Championship (2 Day)",1600,None,None,40000,"40/60","entry",None,[]),
 ("2026-12-17","12:00","WPT World Championship Day 3",None,None,None,100000,"60/90","continuation",None,
  ["Continuation row. The schedule PDF prints no buy-in or guarantee for this row."]),
 ("2026-12-17","12:00","No Limit Hold'em Day 2",None,None,None,None,None,"continuation",None,
  ["Continuation row. The schedule PDF prints no buy-in, guarantee, chips or levels for this row and does not state "
   "the parent event."]),
 ("2026-12-17","12:00","No Limit Hold'em Day 1A",3000,2000000,None,40000,"40","entry",None,[]),
 ("2026-12-17","13:00","NLH High Roller (2 Day)",25800,None,None,200000,"40/60","entry",None,
  ["Schedule footnote: \"Players registered prior to the start of the event will receive a discounted entry.\""]),
 ("2026-12-17","14:00","Milestone Satellite to $3,000 NLH",400,None,"25 Prizes",20000,"20","entry","SAT_WPT",[]),
 ("2026-12-17","19:00","Milestone Satellite to $3,000 NLH",400,None,"25 Prizes",20000,"20","entry","SAT_WPT",[]),
 ("2026-12-18","10:00","Milestone Satellite to $3,000 NLH",400,None,"10 Seats",20000,"15","entry","SAT_WPT",[]),
 ("2026-12-18","12:00","WPT World Championship Day 4",None,None,None,100000,"60/90","continuation",None,
  ["Continuation row. The schedule PDF prints no buy-in or guarantee for this row."]),
 ("2026-12-18","12:00","No Limit Hold'em Day 1B",3000,2000000,None,40000,"40","entry",None,[]),
 ("2026-12-18","12:00","Limit Omaha 8 Championship (2 Day)",1600,None,None,40000,"40/60","entry",None,[]),
 ("2026-12-18","12:00","No Limit Hold'em",600,100000,None,30000,"30","entry",None,[]),
 ("2026-12-18","13:00","NLH 6-Max",10500,None,None,100000,"30/40","entry",None,
  ["Schedule footnote: \"Players registered prior to the start of the event will receive a discounted entry.\""]),
 ("2026-12-18","14:00","Milestone Satellite to $5,000 Seniors High Roller",600,None,"10 Seats",20000,"20","entry","SAT_WPT",[]),
 ("2026-12-18","18:00","NLH Turbo",1100,100000,None,30000,"20","entry",None,[]),
 ("2026-12-19","11:00","Seniors High Roller (3 Day)",5000,250000,None,50000,"60","entry",None,[]),
 ("2026-12-19","11:00","NLH Mystery Bounty Day 1A",1600,1000000,None,40000,"40","entry",None,[]),
 ("2026-12-19","12:00","WPT World Championship Day 5",None,None,None,100000,"60/90","continuation",None,
  ["Continuation row. The schedule PDF prints no buy-in or guarantee for this row."]),
 ("2026-12-19","12:00","No Limit Hold'em Day 2",None,None,None,None,None,"continuation",None,
  ["Continuation row. The schedule PDF prints no buy-in, guarantee, chips or levels for this row and does not state "
   "the parent event."]),
 ("2026-12-19","12:00","Milestone Satellite to $1,600 Mystery Bounty",300,None,"10 Seats",20000,"20","entry","SAT_WPT",[]),
 ("2026-12-19","13:00","PLO",10500,None,None,100000,"30/40","entry",None,
  ["Schedule footnote: \"Players registered prior to the start of the event will receive a discounted entry.\""]),
 ("2026-12-19","13:00","NLH 6-Max",3000,500000,None,30000,"30","entry",None,[]),
 ("2026-12-19","13:00","TORSE Championship (2 Day)",1600,None,None,40000,"40/60","entry",None,[]),
 ("2026-12-19","17:00","Milestone Satellite to $1,600 Mystery Bounty",300,None,"10 Seats",20000,"20","entry","SAT_WPT",[]),
 ("2026-12-19","18:00","NLH 6-Max Turbo",600,50000,None,30000,"20","entry",None,[]),
 ("2026-12-19","19:00","NLH Mystery Bounty Day 1B",1600,1000000,None,40000,"20/40","entry",None,[]),
 ("2026-12-20","11:00","NLH Mystery Bounty Day 1C",1600,1000000,None,40000,"40","entry",None,[]),
 ("2026-12-20","12:00","No Limit Hold'em Final Table",None,None,None,None,None,"continuation",None,
  ["Continuation row. The schedule PDF prints no buy-in, guarantee, chips or levels for this row."]),
 ("2026-12-20","12:00","No Limit Hold'em",600,50000,None,30000,"30","entry",None,[]),
 ("2026-12-20","13:00","NLH 8-Max",10500,None,None,100000,"30/40","entry",None,
  ["Schedule footnote: \"Players registered prior to the start of the event will receive a discounted entry.\""]),
 ("2026-12-20","13:00","Mixed Triple Draw (A-5, 2-7, Badugi)",600,None,None,35000,"30","entry","MTD600",
  ["The $600 Mixed Triple Draw structure sheet lists \"Sunday, December 20, 2026 at 1 p.m.\" among the days it is offered."]),
 ("2026-12-20","14:00","WPT World Championship Final Table",None,None,None,100000,"60/90","continuation",None,
  ["Continuation row. The schedule PDF prints no buy-in or guarantee for this row."]),
 ("2026-12-20","18:00","5-Card PLO Turbo",600,50000,None,30000,"20","entry",None,[]),
 ("2026-12-20","19:00","NLH Mystery Bounty Day 1D",1600,1000000,None,40000,"20/40","entry",None,[]),
 ("2026-12-21","12:00","No Limit Hold'em",1100,100000,None,30000,"30","entry",None,[]),
 ("2026-12-21","13:00","NLH Mystery Bounty Day 2",None,None,None,None,None,"continuation",None,
  ["Continuation row. The schedule PDF prints no buy-in, guarantee, chips or levels for this row."]),
 ("2026-12-21","20:00","NLH Turbo",600,50000,None,30000,"20","entry","TURBO600",
  ["Time conflict between two official sources: the schedule PDF prints this turbo at 8 p.m. on December 21, while "
   "the $600 NLH Turbo structure sheet lists \"Monday, December 21, 2026 at 6 p.m.\" The schedule time is kept and "
   "the conflict is flagged."]),
]

# Wynn structure sheets read in the official structures PDF (read in full on 2026-11-16).
WPT_STRUCTS = {
 "NLH600": dict(label="$600 No Limit Hold'em $400,000 Guarantee",
   fee="Entry Fee: $600 Buy-in = $510 (Tournament Prize Pool) + $65 (Tournament Fee) + $25 (Poker Staff Service Charge)",
   status="RE",
   ex="Registration: \"Unlimited re-entry for each starting flight will be available until the start of level 9. "
      "A player who advances to Day 2 is prohibited from entering a subsequent starting flight.\"",
   stack="Players will start with 40,000 in tournament chips.",
   length="Day 1A-E: 30 minutes per level until 12.5% or less of the field remains. Day 1F: 20 minutes per level "
          "until 12.5% or less of the field remains. Day 2: 40 minutes per level until two (2) players remain, 30 "
          "minutes per level thereafter.",
   breaks="20-minute levels: 10-minute break every 4 levels of play. 30-minute levels: 15-minute break every 4 "
          "levels of play. 40-minute levels: 15-minute break every 3 levels of play.",
   payout="Each Day 1 will play until 12.5% or less of the field remains. Only players who advance to Day 2 will be "
           "considered \"in the money\"."),
 "TORSE600": dict(label="$600 TORSE",
   fee="Entry Fee: $600 Buy-in = $510 (Tournament Prize Pool) + $65 (Tournament Fee) + $25 (Poker Staff Service Charge)",
   status="RE", ex="Registration: \"Unlimited re-entry will be available until the start of level 9\"",
   stack="Players will start with 35,000 in tournament chips.",
   length="30 minutes per level until a winner is declared.",
   breaks="15-minute break every 4 levels of play.",
   payout="Single day event; the structure sheet publishes no Day 1 payout structure."),
 "TORSE1100": dict(label="$1,100 TORSE (2 Day)",
   fee="Entry Fee: $1,100 Buy-in = $965 (Tournament Prize Pool) + $90 (Tournament Fee) + $45 (Poker Staff Service Charge)",
   status="RE", ex="Registration: \"Unlimited re-entry will be available until the start of level 10 (approximately 6:30 p.m.).\"",
   stack="Players will start with 40,000 in tournament chips.",
   length="Day 1: Fifteen (15) levels of 40 minutes each. Day 2: 40 minutes per level until two (2) players remain, 30 minutes per level thereafter.",
   breaks="Break schedule not transcribed for this block; see the official WPT structures PDF.",
   payout="Payout structure not transcribed for this block; see the official WPT structures PDF."),
 "PLO400": dict(label="$400 Pot Limit Omaha",
   fee="Entry Fee: $400 Buy-in = $337 (Tournament Prize Pool) + $45 (Tournament Fee) + $18 (Poker Staff Service Charge)",
   status="RE",
   ex="Registration: \"Unlimited re-entry will be available until the start of level 9 (approximately 5:30 p.m.)\"",
   stack="Players will start with 30,000 in tournament chips.",
   length="30 minutes per level until a winner is declared.",
   breaks="15-minute break every 4 levels of play.",
   payout="Single day event; the structure sheet publishes no Day 1 payout structure."),
 "MTD600": dict(label="$600 Mixed Triple Draw (A-5, 2-7, Badugi)",
   fee="Entry Fee: $600 Buy-in = $510 (Tournament Prize Pool) + $65 (Tournament Fee) + $25 (Poker Staff Service Charge)",
   status="RE", ex="Registration: \"Unlimited re-entry will be available until the start of level 9.\"",
   stack="Players will start with 35,000 in tournament chips.",
   length="30 minutes per level until a winner is declared.",
   breaks="15-minute break every 4 levels of play.",
   payout="Single day event; the structure sheet publishes no Day 1 payout structure."),
 "NLH800": dict(label="$800 No Limit Hold'em $1,000,000 Guarantee",
   fee="Entry Fee: $800 Buy-in = $695 (Tournament Prize Pool) + $72 (Tournament Fee) + $33 (Poker Staff Service Charge)",
   status="RE",
   ex="Registration: \"Unlimited re-entry for each starting flight will be available until the start of level 9. "
      "A player who advances to Day 2 is prohibited from entering a subsequent starting flight.\"",
   stack="Players will start with 40,000 in tournament chips.",
   length="Day 1A-1E: 30 minutes per level until 12.5% or less of the field remains. Day 1F: 20 minutes per level "
          "until 12.5% or less of the field remains. Day 2: 40 minutes per level until nine (9) players remain. "
          "Day 3: 40 minutes per level until two (2) players remain, 30 minutes per level thereafter.",
   breaks="20-minute levels: 10-minute break every 4 levels of play. 30-minute levels: 15-minute break every 4 "
          "levels of play. 40-minute levels: 15-minute break every 3 levels of play.",
   payout="Each Day 1 will play until 12.5% or less of the field remains. Only players who advance to Day 2 will be "
           "considered \"in the money\".",
   days="Day 1A: Monday, November 30, 2026 at 11 a.m. Day 1B: Monday, November 30, 2026 at 5 p.m. Day 1C: Tuesday, "
        "December 1, 2026 at 11 a.m. Day 1D: Tuesday, December 1, 2026 at 5 p.m. Day 1E: Wednesday, December 2, 2026 "
        "at 11 a.m. Day 1F: Wednesday, December 2, 2026 at 6 p.m. Day 2: Thursday, December 3, 2026 at 1 p.m. Final "
        "Table: Friday, December 4, 2026 at 1 p.m."),
 "LO8": dict(label="$600 Limit Omaha 8",
   fee="Entry Fee: $600 Buy-in = $510 (Tournament Prize Pool) + $65 (Tournament Fee) + $25 (Poker Staff Service Charge)",
   status="RE", ex="Registration: \"Unlimited re-entry will be available until the start of level 9\"",
   stack="Players will start with 35,000 in tournament chips.",
   length="30 minutes per level until a winner is declared.",
   breaks="15-minute break every 4 levels of play.",
   payout="Single day event; the structure sheet publishes no Day 1 payout structure."),
 "LO8S8": dict(label="$600 Limit Omaha 8/Stud 8",
   fee="Entry Fee: $600 Buy-in = $510 (Tournament Prize Pool) + $65 (Tournament Fee) + $25 (Poker Staff Service Charge)",
   status="RE", ex="Registration: \"Unlimited re-entry will be available until the start of level 9\"",
   stack="Players will start with 35,000 in tournament chips.",
   length="30 minutes per level until a winner is declared.",
   breaks="15-minute break every 4 levels of play.",
   payout="Single day event; the structure sheet publishes no Day 1 payout structure."),
 "PLO1100": dict(label="$1,100 Pot Limit Omaha",
   fee="Entry Fee: $1,100 Buy-in = $975 (Tournament Prize Pool) + $85 (Tournament Fee) + $45 (Poker Staff Service Charge)",
   status="RE",
   ex="Registration: \"Unlimited re-entry will be available until the start of level 9 (approximately 5:30 p.m.).\"",
   stack="Players will start with 30,000 in tournament chips.",
   length="30 minutes per level until a winner is declared.",
   breaks="15-minute break every 4 levels of play.",
   payout="Single day event; the structure sheet publishes no Day 1 payout structure."),
 "NLH1600": dict(label="$1,600 No Limit Hold'em $1,000,000 Guarantee",
   fee="Entry Fee: $1,600 Buy-in = $1,430 (Tournament Prize Pool) + $120 (Tournament Fee) + $50 (Poker Staff Service Charge)",
   status="RE",
   ex="Registration: \"Unlimited re-entry for each starting flight will be available until the start of level 10. "
      "A player who advances to Day 2 is prohibited from entering a subsequent starting flight.\"",
   stack="Players will start with 40,000 in tournament chips.",
   length="Day 1: 40 minutes per level until 12.5% or less of the field remains. Day 2: 40 minutes per level until "
          "two (2) players remain, 30 minutes per level thereafter.",
   breaks="15-minute break every 3 levels of play.",
   payout="Each Day 1 will play until 12.5% or less of the field remains. Only players who advance to Day 2 will be "
           "considered \"in the money\".",
   days="Day 1A: Thursday, December 3, 2026 at 11 a.m. Day 1B: Friday, December 4, 2026 at 11 a.m. Day 2: Saturday, "
        "December 5, 2026 at 11 a.m."),
 "HORSE600": dict(label="$600 HORSE",
   fee="Entry Fee: $600 Buy-in = $510 (Tournament Prize Pool) + $65 (Tournament Fee) + $25 (Poker Staff Service Charge)",
   status="RE",
   ex="Registration: \"Unlimited re-entry will be available until the start of level 9 (approximately 4:30 p.m.).\"",
   stack="Players will start with 35,000 in tournament chips.",
   length="30 minutes per level until a winner is declared.",
   breaks="15-minute break every 4 levels of play.",
   payout="Single day event; the structure sheet publishes no Day 1 payout structure."),
 "PRIME": dict(label="$1,100 WPT Prime Championship $5,000,000 Guarantee",
   fee="Entry Fee: $1,100 Buy-in = $970 (Tournament Prize Pool) + $90 (Tournament Fee) + $40 (Poker Staff Service Charge)",
   status="RE",
   ex="Registration: \"One (1) Entry and One (1) re-entry for each starting flight will be available until the start "
      "of level 10 (approximately 6:45 p.m.). A player who advances to Day 2 is prohibited from entering a subsequent "
      "starting flight.\"",
   stack="Players will start with 40,000 in tournament chips.",
   length="Day 1: 40 minutes per level until 12.5% or less of the field remains. Day 2: Ten (10) levels of 60 minutes "
          "each. Day 3: Ten (10) levels of 60 minutes each. Day 4: 60 minutes per level until the final six (6) "
          "players remain. Day 5: 60 minutes per level until two (2) players remain, 30 minutes per level thereafter.",
   breaks="40-minute levels: 15-minute break every 3 levels of play. 75-minute break after level 9 (approximately "
          "5:30 p.m.). 60-minute levels: 15-minute break every 2 levels of play.",
   payout="One in eight (1-in-8) entries will be in the money (approximately 12.5%). $10,400 will be withheld from the "
           "prize pool and issued to first place in the form of an entry to the December 2027 WPT World Championship.",
   days="Day 1A: Saturday, December 5, 2026 at 11 a.m. Day 1B: Sunday, December 6, 2026 at 11 a.m. Day 1C: Monday, "
        "December 7, 2026 at 11 a.m. Day 1D: Tuesday, December 8, 2026 at 11 a.m. Day 2: Wednesday, December 9, 2026 "
        "at 12 p.m. Day 3: Thursday, December 10, 2026 at 12 p.m. Day 4: Friday, December 11, 2026 at 12 p.m. Final "
        "Table: Saturday, December 12, 2026 at 2 p.m."),
 "TURBO600": dict(label="$600 NLH Turbo $50,000 Guarantee",
   fee="Entry Fee: $600 Buy-in = $515 (Tournament Prize Pool) + $60 (Tournament Fee) + $25 (Poker Staff Service Charge)",
   status="RE", ex="Registration: \"Unlimited re-entry will be available until the start of level 9.\"",
   stack="Players will start with 30,000 in tournament chips.",
   length="20 minutes per level until a winner is declared.",
   breaks="10-minute break every 4 levels of play.",
   payout="Single day event; the structure sheet publishes no Day 1 payout structure.",
   days="Saturday, December 5, 2026 at 9 p.m. Sunday, December 6, 2026 at 9 p.m. Monday, December 7, 2026 at 9 p.m. "
        "Tuesday, December 8, 2026 at 9 p.m. Wednesday, December 9, 2026 at 9 p.m. Saturday, December 12, 2026 at 9 "
        "p.m. Monday, December 14, 2026 at 9 p.m. Monday, December 21, 2026 at 6 p.m."),
 "PLOMYST": dict(label="$1,600 Pot Limit Omaha Mystery Bounty $500,000 Guarantee",
   fee="Entry Fee: $1,600 Buy-in = $930 (Tournament Prize Pool) + $500 (Mystery Bounty Prize Pool) + $120 (Tournament Fee) "
       "+ $50 (Poker Staff Service Charge)",
   status="RE",
   ex="Registration: \"Unlimited re-entry for each starting flight will be available until the start of level 10. "
      "A player who advances to Day 2 is prohibited from entering a subsequent starting flight.\"",
   stack="Players will start with 40,000 in tournament chips.",
   length="Day 1A: 40 minutes per level until 12.5% or less of the field remains. Day 1B: 20 minutes per level until "
          "12.5% or less of the field remains. Day 2: 40 minutes per level until two (2) players remain, 30 minutes "
          "per level thereafter.",
   breaks="40-minute levels: 15-minute break every 3 levels of play.",
   payout="Only players who advance to Day 2 will be considered \"in the money\". In the event that the number of paid "
           "entries does not generate at least the Guaranteed prize pool, after the deduction of the Tournament fees "
           "and service charge, $325,000 of the Guarantee will be designated for the Tournament prize pool and "
           "$175,000 of the Guarantee will be designated for the Bounty prize pool.",
   days="Day 1A: Sunday, December 6, 2026, at 11 a.m. Day 1B: Sunday, December 6, 2026, at 6 p.m. Day 2: Monday, "
        "December 7, 2026, at 12 p.m."),
 "SAT_WPT": dict(label="Milestone / satellite rows printed in the official WPT schedule PDF",
   fee=None, status="UNV",
   ex="The official WPT World Championship Structures PDF (all 69 sheets) does publish a sheet for every "
      "milestone-satellite event, and those sheets are joined to these rows on their printed date, start "
      "time and buy-in by scripts/extract_wpt_sheets.py. This fallback text is only used if that join ever "
      "stops resolving a row.",
   stack=None, length=None, breaks=None, payout=None),
}

# ---------- Wynn Signature Series schedule rows (official schedule PDF, structures not yet published) ----------
# date, time, name, buy-in, guarantee, published chips, published levels, kind, flags
WSS_REREAD_ON = "2026-11-19"  # day the official WSS schedule/structures PDFs were re-read; stamps these rows' last_checked
# 2026-11-19 live re-verification pass (session cebd4457): every source behind the WPT rows (the schedule
# PDF and the structures PDF) was re-read in full that day, so those rows carry this stamp on last_checked
# and on their rule excerpts' retrieved_on - the same semantics as the REREAD dict above.
WPT_REREAD_ON = "2026-11-19"
# The official schedule prints a guarantee for the NLH Turbo ($10,000) and the Sunday NLH
# events ($30,000), and - corrected on 2026-11-19 - for the multi-day main events as well:
# the re-read of the SAME file (byte-identical per the 2026-11-19 provenance fetch) with a
# table-structure renderer recovers the merged GUARANTEE cells the line extractor had been
# dropping, so each Day-1 flight row now carries the guarantee printed on its own row
# ($150,000 Jan 11-13, $250,000 Jan 14-16, $100,000 Jan 18-20, $300,000 Jan 21-23).
# Single events whose official row leaves the GUARANTEE cell blank (PLO, TORSE, Mixed Triple
# Draw, TOE, Big O, PLO Bomb Pot) stay blank - nothing is inferred. Capture:
# data/snapshots/wss_sched_reread_20261119.txt; irregularity: FLAGGED.md F83.
# The structures PDF is still a "COMING SOON" placeholder (re-read 2026-11-19), so entry
# rules remain unverified for every row of this series.
WSS_GTD_REREAD = ("Guarantee read from the event's own row of the official schedule PDF "
                  "(table-structure re-read 2026-11-19; the line-only extraction used for the "
                  "2026-11-16 capture dropped the merged guarantee cell, see data/snapshots/"
                  "wss_sched_reread_20261119.txt and FLAGGED.md F83).")
WSS = [
 ("2027-01-11","12:00","No Limit Hold'em Day 1A",400,150000,40000,"30/40","entry",[WSS_GTD_REREAD]),
 ("2027-01-11","17:00","No Limit Hold'em Day 1B",400,150000,40000,"30/40","entry",[WSS_GTD_REREAD]),
 ("2027-01-12","12:00","No Limit Hold'em Day 1C",400,150000,40000,"30/40","entry",[WSS_GTD_REREAD]),
 ("2027-01-12","17:00","No Limit Hold'em Day 1D",400,150000,40000,"30/40","entry",[WSS_GTD_REREAD]),
 ("2027-01-13","12:00","No Limit Hold'em Day 1E",400,150000,40000,"30/40","entry",[WSS_GTD_REREAD]),
 ("2027-01-13","17:00","No Limit Hold'em Day 1F",400,150000,40000,"30/40","entry",[WSS_GTD_REREAD]),
 ("2027-01-14","11:00","No Limit Hold'em Day 1A",600,250000,40000,"40","entry",[WSS_GTD_REREAD]),
 ("2027-01-14","13:00","No Limit Hold'em Day 2",None,None,None,None,"continuation",
  ["Continuation row. The official schedule PDF prints no buy-in, guarantee, chips or levels for this row."]),
 ("2027-01-14","18:00","Milestone Satellite to $600 NLH",125,None,20000,"20","entry",
  ["Prize printed as \"10 Seats\". Schedule footnote: \"Winners will receive direct entry to the corresponding "
   "event(s) for which it was held. See structure sheet for details.\""]),
 ("2027-01-15","11:00","No Limit Hold'em Day 1B",600,250000,40000,"40","entry",[WSS_GTD_REREAD]),
 ("2027-01-15","18:00","NLH Turbo",200,10000,25000,"20","entry",[]),
 ("2027-01-16","11:00","No Limit Hold'em Day 1C",600,250000,40000,"40","entry",[WSS_GTD_REREAD]),
 ("2027-01-16","18:00","No Limit Hold'em Day 1D",600,250000,40000,"20/40","entry",[WSS_GTD_REREAD]),
 ("2027-01-17","12:00","No Limit Hold'em",400,30000,30000,"30","entry",[]),
 ("2027-01-17","13:00","No Limit Hold'em Day 2",None,None,None,None,"continuation",
  ["Continuation row. The official schedule PDF prints no buy-in, guarantee, chips or levels for this row."]),
 ("2027-01-17","18:00","NLH Turbo",200,10000,25000,"20","entry",[]),
 ("2027-01-18","11:00","No Limit Hold'em Day 1A",400,100000,40000,"40","entry",[WSS_GTD_REREAD]),
 ("2027-01-18","13:00","PLO",400,None,30000,"30","entry",[]),
 ("2027-01-18","18:00","NLH Turbo",200,10000,25000,"20","entry",[]),
 ("2027-01-19","11:00","No Limit Hold'em Day 1B",400,100000,40000,"40","entry",[WSS_GTD_REREAD]),
 ("2027-01-19","13:00","TORSE",400,None,35000,"30","entry",[]),
 ("2027-01-19","18:00","NLH Turbo",200,10000,25000,"20","entry",[]),
 ("2027-01-20","11:00","No Limit Hold'em Day 1C",400,100000,40000,"40","entry",[WSS_GTD_REREAD]),
 ("2027-01-20","13:00","Mixed Triple Draw (A-5, 2-7, Badugi)",400,None,35000,"30","entry",[]),
 ("2027-01-20","18:00","NLH Turbo",200,10000,25000,"20","entry",[]),
 ("2027-01-21","11:00","No Limit Hold'em Day 1A",800,300000,40000,"40","entry",[WSS_GTD_REREAD]),
 ("2027-01-21","12:00","No Limit Hold'em Day 2",None,None,None,None,"continuation",
  ["Continuation row. The official schedule PDF prints no buy-in, guarantee, chips or levels for this row."]),
 ("2027-01-21","13:00","TOE",400,None,35000,"30","entry",[]),
 ("2027-01-21","18:00","Milestone Satellite to $800 NLH",160,None,20000,"20","entry",
  ["Prize printed as \"10 Seats\". Schedule footnote: \"Winners will receive direct entry to the corresponding "
   "event(s) for which it was held. See structure sheet for details.\""]),
 ("2027-01-22","11:00","No Limit Hold'em Day 1B",800,300000,40000,"40","entry",[WSS_GTD_REREAD]),
 ("2027-01-22","13:00","Big O",400,None,30000,"30","entry",[]),
 ("2027-01-22","18:00","Milestone Satellite to $800 NLH",160,None,20000,"20","entry",
  ["Prize printed as \"10 Seats\". Schedule footnote: \"Winners will receive direct entry to the corresponding "
   "event(s) for which it was held. See structure sheet for details.\""]),
 ("2027-01-23","11:00","No Limit Hold'em Day 1C",800,300000,40000,"40","entry",[WSS_GTD_REREAD]),
 ("2027-01-23","18:00","No Limit Hold'em Day 1D",800,300000,40000,"20/40","entry",[WSS_GTD_REREAD]),
 ("2027-01-24","12:00","Seniors NLH 50+",400,30000,30000,"30","entry",[]),
 ("2027-01-24","13:00","No Limit Hold'em Day 2",None,None,None,None,"continuation",
  ["Continuation row. The official schedule PDF prints no buy-in, guarantee, chips or levels for this row."]),
 ("2027-01-24","13:00","PLO Double Board Bomb Pot",400,None,30000,"30","entry",[]),
 ("2027-01-24","18:00","NLH Turbo",200,10000,25000,"20","entry",[]),
]

# ---------- Bellagio weekly flyers and the Caesars Palace daily flyer ----------
# The exact PDF the official Bellagio poker page linked on 2026-11-17. Kept beside the rows
# so every quoted rule can be opened and checked, and marked as the document behind the row.
BELLAGIO_FLYER_URLS = {
    "bellagio-fri": "https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/blt9cf95b0e60ec253e/"
                    "6af491a3a9851d75c40be840/mgm-bellagio-poker-fridays-$600-nlh.pdf",
    "bellagio-sat": "https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/blt6d47974bf5a7d9b6/"
                    "6af491a391a6e8e4230c9e07/mgm-bellagio-poker-saturdays-$1000-nlh.pdf",
    "bellagio-sun": "https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/blt07fcf1244a6da661/"
                    "6af491a339e2b4f6b76a86ad/mgm-bellagio-poker-sundays-$400-horse.pdf",
}
# Every value below is quoted from the flyer the official page links; each row names the
# document it came from in `source`, and the official poker-room page it was linked from in
# `page`. The Bellagio flyers live on MGM's content-asset host, which the approved-host list
# deliberately does not include (F40), so the citation is the official page that links them.
BELLAGIO_DAILY = [
 dict(id="bellagio-fri", room="Bellagio", name="$600 No Limit Hold'em (Fridays)", days="Friday",
      start="11:00", buy_in_usd=600, guarantee_usd=None, status="RE",
      labels=["recurring", "re-entry", "advantage-for-money"],
      fee="Rule 5: \"The $600 Buy-In is allocated as follows: $510 to Prize Pool; $50 House Fee; "
          "$40 Voluntary Staff Gratuity.\" Rule 7: \"The voluntary staff gratuity will grant players "
          "an extra 15,000 chips.\"",
      ex="Rule 3: \"Players may buy-in and re-enter through the end of level 8 (Including Break). "
         "Tournament Surrender is allowed on Level 8 break.\"",
      late=None, late_reg_level=8,
      late_reg_text="Rule 3 closes registration at \"the end of level 8 (Including Break)\"; no clock "
                    "time is printed. Levels are 30 minutes with a 12-minute break every four levels, so "
                    "the end of level 8 is about 4 h 12 m after the 11:00 a.m. start - derived from the "
                    "printed structure, not printed as a time, and the flyer does not say whether the "
                    "break that follows level 8 is inside or outside the window.",
      levels=28, lmin=30,
      stack="Rule 1: \"Players will start with 30,000 tournament chips, including the optional Staff "
            "Gratuity. (15,000 + 15,000)\""),
 dict(id="bellagio-sat", room="Bellagio", name="$1,000 No Limit Hold'em (Saturdays)", days="Saturday",
      start="11:00", buy_in_usd=1000, guarantee_usd=50000, status="RE",
      labels=["recurring", "multi-flight", "re-entry", "advantage-for-money"],
      fee="Rule 7: \"Of the $600 Buy-in, $510 goes to the Prize Pool, $50 is Admin Fees and $40 is "
          "optional staff gratuity.\" Rule 9: the $40 gratuity \"will grant players an extra 20,000 "
          "chips\". The $600 figures are what the flyer prints even though its heading reads "
          "\"NLH $1100 BUY-IN\" and the file is named $1,000 (F32).",
      ex="Rule 3: \"Registration will be open until the start of Level 10. (Approximately 5:15pm for "
         "Flights 1A, 1B, 4:15pm for 1C and 9:30pm for Flight D).\" Rule 6: \"Each Flight would play "
         "until the money (12.5%). Must bag chips to make Day 2 and be in the money.\"",
      late=None, late_reg_level=10,
      late_reg_text="Rule 3 gives a level, not a time, and gives four different clock times for four "
                    "flights (5:15pm for 1A and 1B, 4:15pm for 1C, 9:30pm for Flight D). Which flight "
                    "the 11:00 a.m. start is cannot be read from the flyer, so no single time is "
                    "published for this row.",
      levels=28, lmin=30,
      stack="Rule 1: \"Players start with 40,000 in tournament chips (20,000 + 20,000 optional).\"",
      flags=["F32: the flyer contradicts itself on the buy-in - the heading reads \"NLH $1100 "
             "BUY-IN\", the file and page label read $1,000, and rule 7 prices a $600 buy-in. "
             "Rule 4 also names a Combined Final Day 2 of 9/13/26, a date before this page was read "
             "on 2026-11-17, so the flyer is not current. Buy-in, guarantee and entry rule are "
             "not confirmed."]),
 dict(id="bellagio-sun", room="Bellagio", name="$400 H.O.R.S.E. (Sundays)", days="Sunday",
      start="11:00", buy_in_usd=400, guarantee_usd=None, status="RE",
      labels=["recurring", "re-entry", "advantage-for-money"],
      fee="Rule 1: \"The $400 Buy-In is allocated as follows: $340 to Prize Pool; $35 House Fee; "
          "$25 Voluntary Staff Gratuity.\" Rule 2: the $25 gratuity \"will grant players an "
          "additional 15,000 in starting chips\".",
      ex="Rule 5: \"Players may buy-in and re-enter through the end of level 8 (Including Break). "
         "Tournament Surrender is allowed on Level 8 break.\"",
      late=None, late_reg_level=8,
      late_reg_text="Rule 5 closes registration at \"the end of level 8 (Including Break)\"; no clock "
                    "time is printed. Levels are 30 minutes with 12-minute breaks every four levels, "
                    "so that is about 4 h 12 m after the 11:00 a.m. start - derived, not printed.",
      levels=26, lmin=30,
      stack="Rule 3: \"Players will start with 30,000 tournament chips, including the optional Staff "
            "Gratuity. (15,000 + 15,000)\"",
      note_extra="Rule 4: \"Each level will last thirty (30) minutes ... ***When 3 players remain in "
                 "event, levels will be reduced to 20 Minutes.\""),
]
CAESARS_DAILY = [
 dict(id="caesars-1000", room="Caesars Palace", name="$100 No Limit Hold'em (daily, 10 a.m.)",
      days="Daily", start="10:00", buy_in_usd=100, guarantee_usd=1000, status="REBUY",
      labels=["recurring", "re-entry", "add-on"],
      fee="Sign-up 6: \"Of the $100 buy in, $70 goes to the prize pool and $30 is held by Caesars "
          "Palace as a maintenance fee.\" Sign-up 8: \"Of the $50 add-on, $45 goes to the prize pool "
          "and $5 is held by Caesars Palace as a maintenance fee.\"",
      ex="Sign-up 3: \"Participants may only register themselves, but may re-enter, by paying the "
         "entry fee, upon elimination within the first break of play.\" Schedule note: \"All "
         "Tournaments feature a $50 add-on for 15,000 tournament chips that can only be taken at the "
         "first break.\"",
      late=None, late_reg_level=7,
      late_reg_text="The flyer closes registration \"at the start of level seven\" and prints no "
                    "clock time. Levels are 20 minutes with a 10-minute break every six levels, so "
                    "that is about 2 h 10 m after the 10:00 a.m. start - derived from the printed "
                    "structure, not printed as a time.",
      levels=15, lmin=20,
      stack="Schedule table: \"Starting Chips 20,000\"; the $50 add-on buys 15,000 more."),
 dict(id="caesars-1400", room="Caesars Palace", name="$160 No Limit Hold'em (daily, 2 p.m.)",
      days="Daily", start="14:00", buy_in_usd=160, guarantee_usd=1000, status="REBUY",
      labels=["recurring", "re-entry", "add-on"],
      fee="Sign-up 7: \"Of the $160 buy in, $115 goes to the prize pool and $45 is held by Caesars "
          "Palace as a maintenance fee.\" Sign-up 8: \"Of the $50 add-on, $45 goes to the prize pool "
          "and $5 is held by Caesars Palace as a maintenance fee.\"",
      ex="Sign-up 3: \"Participants may only register themselves, but may re-enter, by paying the "
         "entry fee, upon elimination within the first break of play.\" Schedule note: \"All "
         "Tournaments feature a $50 add-on for 15,000 tournament chips that can only be taken at the "
         "first break.\"",
      late=None, late_reg_level=7,
      late_reg_text="Registration closes \"at the start of level seven\" (no clock time printed); "
                    "20-minute levels with a 10-minute break every six levels put that about 2 h 10 m "
                    "after the 2:00 p.m. start - derived, not printed.",
      levels=15, lmin=20,
      stack="Schedule table: \"Starting Chips 20,000\"; the $50 add-on buys 15,000 more."),
 dict(id="caesars-1800", room="Caesars Palace", name="$100 No Limit Hold'em (daily, 6 p.m.)",
      days="Daily", start="18:00", buy_in_usd=100, guarantee_usd=1000, status="REBUY",
      labels=["recurring", "re-entry", "add-on"],
      fee="Sign-up 6: \"Of the $100 buy in, $70 goes to the prize pool and $30 is held by Caesars "
          "Palace as a maintenance fee.\" Sign-up 8: \"Of the $50 add-on, $45 goes to the prize pool "
          "and $5 is held by Caesars Palace as a maintenance fee.\"",
      ex="Sign-up 3: \"Participants may only register themselves, but may re-enter, by paying the "
         "entry fee, upon elimination within the first break of play.\" Schedule note: \"All "
         "Tournaments feature a $50 add-on for 15,000 tournament chips that can only be taken at the "
         "first break.\"",
      late=None, late_reg_level=7,
      late_reg_text="Registration closes \"at the start of level seven\" (no clock time printed); "
                    "20-minute levels with a 10-minute break every six levels put that about 2 h 10 m "
                    "after the 6:00 p.m. start - derived, not printed.",
      levels=15, lmin=20,
      stack="Schedule table: \"Starting Chips 20,000\"; the $50 add-on buys 15,000 more."),
 dict(id="caesars-2100", room="Caesars Palace", name="$160 No Limit Hold'em (daily, 9 p.m.)",
      days="Daily", start="21:00", buy_in_usd=160, guarantee_usd=1000, status="REBUY",
      labels=["recurring", "re-entry", "add-on"],
      fee="Sign-up 7: \"Of the $160 buy in, $115 goes to the prize pool and $45 is held by Caesars "
          "Palace as a maintenance fee.\" Sign-up 8: \"Of the $50 add-on, $45 goes to the prize pool "
          "and $5 is held by Caesars Palace as a maintenance fee.\"",
      ex="Sign-up 3: \"Participants may only register themselves, but may re-enter, by paying the "
         "entry fee, upon elimination within the first break of play.\" Schedule note: \"All "
         "Tournaments feature a $50 add-on for 15,000 tournament chips that can only be taken at the "
         "first break.\"",
      late=None, late_reg_level=7,
      late_reg_text="Registration closes \"at the start of level seven\" (no clock time printed); "
                    "20-minute levels with a 10-minute break every six levels put that about 2 h 10 m "
                    "after the 9:00 p.m. start - derived, not printed.",
      levels=15, lmin=20,
      stack="Schedule table: \"Starting Chips 20,000\"; the $50 add-on buys 15,000 more."),
]

# ---------- Wynn daily (recurring) tournaments: official poster + daily structures PDF ----------
WYNN_DAILY = [
 dict(id="daily-mon-thu", name="$200 No Limit Hold'em (daily)", days="Monday-Thursday", start="12:00",
      buy_in_usd=200, guarantee_usd=10000, status="RE", labels=["recurring", "re-entry"],
      fee="Entry Fee: $200 Buy-in = $162 (Tournament prize pool) + $26 (Tournament fee) + $12 (Poker staff service charge)",
      ex="Clause 3: \"The Tournament entry fee, as well as the re-entry fee, is $200\"; clause 4: \"Registration and "
         "re-entries will be available until the start of level 9 (approximately 4:30 p.m.)\"",
      late="16:30", levels=28, lmin=30,
      stack="Clause 5: \"Players will start with 25,000 in Tournament chips.\""),
 dict(id="daily-fri", name="$240 No Limit Hold'em Rebuy & Add-on (daily)", days="Friday", start="12:00",
      buy_in_usd=240, guarantee_usd=40000, status="REBUY", labels=["recurring", "rebuy", "add-on"],
      fee="Entry Fee: $240 of which $190 funds the prize pool, $35 tournament fee, $15 staff service charge; "
          "$200 rebuys and $100 add-ons are charged extra",
      ex="Clause 4: \"Re-entry is NOT allowed. All rebuys must be done immediately from the player's original seat.\" "
         "Clause 5: \"Unlimited $200 rebuys for 25,000 tournament chips are available any time a player is at 15,000 "
         "chips or less. One (1) $100 add-on for 15,000 tournament chips is available any time until the end of registration.\"",
      late="16:30", levels=28, lmin=30,
      stack="Clause 5: \"Players will start with 25,000 in Tournament chips.\""),
 dict(id="daily-weekend", name="$200 No Limit Hold'em (daily)", days="Saturday-Sunday", start="12:00",
      buy_in_usd=200, guarantee_usd=25000, status="RE", labels=["recurring", "re-entry", "add-on"],
      fee="Entry Fee: $200 Buy-in = $162 (Tournament prize pool) + $26 (Tournament fee) + $12 (Poker staff service charge)",
      ex="Clause 3: \"The Tournament entry fee, as well as the re-entry fee, is $200\"; clause 4: \"Registration, "
         "re-entries, and one (1) add-on per entry will be available until the start of level 11 (approximately 5:30 p.m.)\"",
      late="17:30", levels=28, lmin=30,
      stack="Clause 5: \"Players will start with 25,000 in Tournament chips.\""),
 dict(id="daily-nightly", name="$160 No Limit Hold'em nightly (daily)", days="Monday-Sunday", start="18:00",
      buy_in_usd=160, guarantee_usd=10000, status="RE", labels=["recurring", "re-entry", "add-on"],
      fee="Entry Fee: $160 Buy-in = $130 (Tournament prize pool) + $20 (Tournament fee) + $10 (Poker staff service charge)",
      ex="Clause 3: \"The Tournament entry fee, as well as the re-entry fee, is $160\"; clause 4: \"Registration, "
         "re-entries, and one (1) add-on per entry will be available until the start of level 9 (approximately 9:00 p.m.)\"",
      late="21:00", levels=30, lmin=20,
      stack="Clause 5: \"Players will start with 25,000 in Tournament chips.\""),
]

# Each Wynn row carries the room it belongs to so one feed can hold every Strip
# poker room whose official schedule has been read.
for _d in WYNN_DAILY:
    _d.setdefault("venue", "Wynn Las Vegas")
    _d.setdefault("venue_id", "wynn")
    _d.setdefault("verified_on", "2026-11-16")
    _d.setdefault("source_label", "Official Wynn daily tournament structures PDF (read 2026-11-16)")
    _d.setdefault("source_url", SRC["wynn_daily_struct"])
    _d.setdefault("late_printed", True)

# ---- Bellagio and Caesars Palace weekly / daily formats, added 2026-11-17 (session c7a324a6) ----
# Each row below is quoted from the property's own published structure document; nothing is
# inferred. Where the source states a level-based registration close with no clock time, the
# clock field is left null and late_printed is False, with the printed sentence in late_note.
ROOM_DAILY = WYNN_DAILY + [
 dict(id="bellagio-fri", venue="Bellagio", venue_id="bellagio", verified_on="2026-11-17",
      name="$600 No Limit Hold'em (every Friday)", days="Friday", start="11:00",
      buy_in_usd=600, guarantee_usd=None, status="RE",
      labels=["recurring", "re-entry", "add-on not offered", "voluntary staff gratuity"],
      fee="Flyer rule 05: \"The $600 Buy-In is allocated as follows: $510 to Prize Pool; $50 House Fee; "
          "$40 Voluntary Staff Gratuity.\"",
      ex="Rule 03: \"Players may buy-in and re-enter through the end of level 8 (Including Break). Tournament "
         "Surrender is allowed on Level 8 break.\" Rule 02: \"Levels will be 30 Minutes in Length with a 12 minute "
         "break every 4 levels.\" Rule 04: \"Tournament will be played 8-handed. Final table will be 9-handed.\"",
      late=None, late_printed=False,
      late_note="No clock time printed: registration closes at the end of level 8 including the break.",
      levels=28, lmin=30,
      stack="Rule 01: \"Players will start with 30,000 tournament chips, including the optional Staff Gratuity. "
            "(15,000 + 15,000)\"",
      source_label="Official Bellagio poker page (page) and the Friday structure PDF it links (both read 2026-11-17)",
      source_url=SRC["bellagio_fri_pdf"],
      single_entry="not single entry - the flyer's own rule 03 allows re-entry through level 8",
      flag="No guarantee is printed on the flyer, so the guarantee is blank rather than assumed."),
 dict(id="bellagio-sat", venue="Bellagio", venue_id="bellagio", verified_on="2026-11-17",
      name="$1,100 No Limit Hold'em, 4 flights with a combined Day 2 (every Saturday)", days="Saturday",
      start="11:00", buy_in_usd=None, guarantee_usd=50000, status="MULTI",
      labels=["recurring", "multi-flight", "two-day", "prize-figure conflict"],
      fee="Flyer rule 07 prints \"Of the $600 Buy-in, $510 goes to the Prize Pool, $50 is Admin Fees and $40 is "
          "optional staff gratuity\" on a flyer headed \"NLH $1100 BUY-IN\"; the official poker page labels the "
          "same event as a $1,000 buy-in (page wording, not this document's). Three different buy-ins are printed, so "
          "buy_in_usd is left blank rather than choosing one.",
      ex="Rule 08: \"Bellagio guarantees that the total Combined Prize Pool will be at least $50,000.\" "
         "Rule 03: \"Registration will be open until the start of Level 10. (Approximately 5:15pm for Flights 1A, "
         "1B, 4:15pm for 1C and 9:30pm for Flight D).\" Rule 06: \"Each Flight would play until the money (12.5%). "
         "Must bag chips to make Day 2 and be in the money.\"",
      late="17:15", late_printed=True,
      late_note="Printed as an approximation for flights 1A/1B only: \"Approximately 5:15pm for Flights 1A, 1B, "
                "4:15pm for 1C and 9:30pm for Flight D\".",
      levels=28, lmin=30,
      stack="Rule 01: \"Players start with 40,000 in tournament chips (20,000 + 20,000 optional).\"",
      source_label="Official Bellagio Saturday structure PDF linked from the official poker page (read 2026-11-17)",
      source_url=SRC["bellagio_sat_pdf"],
      single_entry="not single entry - four labelled flights (1A-1D) with a combined Day 2; a player who busts on "
                   "Day 1 without bagging chips may enter another flight",
      flag="Rule 04 prints \"Combined Final Day 2 (9/13/26)\", a September 2026 date, so the flyer cannot be "
           "assumed current for a November 2026 - January 2027 trip (FLAGGED.md F75)."),
 dict(id="bellagio-sun", venue="Bellagio", venue_id="bellagio", verified_on="2026-11-17",
      name="$400 H.O.R.S.E. (every Sunday)", days="Sunday", start="11:00",
      buy_in_usd=400, guarantee_usd=None, status="RE",
      labels=["recurring", "re-entry", "mixed games", "voluntary staff gratuity"],
      fee="Flyer rule 01: \"The $400 Buy-In is allocated as follows: $340 to Prize Pool; $35 House Fee; $25 "
          "Voluntary Staff Gratuity.\"",
      ex="Rule 05: \"Players may buy-in and re-enter through the end of level 8 (Including Break). Tournament "
         "Surrender is allowed on Level 8 break.\" Rule 07: \"Payout structure based on number of entries and will "
         "be approximately 12.5% of field.\" Rule 04: \"Each level will last thirty (30) minutes, game will change "
         "every 8 hands...\" Rule 06: \"Twelve (12) minute breaks will be every 4 levels.\"",
      late=None, late_printed=False,
      late_note="No clock time printed: registration closes at the end of level 8 including the break.",
      levels=26, lmin=30,
      stack="Rule 03: \"Players will start with 30,000 tournament chips, including the optional Staff Gratuity. "
            "(15,000 + 15,000)\"",
      source_label="Official Bellagio Sunday H.O.R.S.E. structure PDF linked from the official poker page (read 2026-11-17)",
      source_url=SRC["bellagio_sun_pdf"],
      single_entry="not single entry - the flyer's own rule 05 allows re-entry through level 8",
      flag="The blind ladder prints 26 levels; the level table is the printed ladder, not a promise of the event's length."),
 dict(id="caesars-daily-10", venue="Caesars Palace", venue_id="caesars", verified_on="2026-11-17",
      name="$100 No Limit Texas Hold'em daily (10 a.m.)", days="Monday-Sunday", start="10:00",
      buy_in_usd=100, guarantee_usd=1000, status="REBUY",
      labels=["recurring", "re-entry", "add-on", "earliest daily on the Strip"],
      fee="Flyer rule 06: \"Of the $100 buy in, $70 goes to the prize pool and $30 is held by Caesars Palace as a "
          "maintenance fee.\" Rule 08: \"Of the $50 add-on, $45 goes to the prize pool and $5 is held by Caesars "
          "Palace as a maintenance fee.\"",
      ex="Schedule table row, printed verbatim: \"10 AM $100 $50 20,000 20 Minutes $1,000\". "
         "Rules: \"All Tournaments feature a $50 add-on for 15,000 tournament chips that can only be taken at the "
         "first break. Registration will close at the start of level seven. All tournaments will have a 10-minute "
         "break every six levels.\" Sign-up rule 3: \"Participants may only register themselves, but may re-enter, "
         "by paying the entry fee, upon elimination within the first break of play.\"",
      late=None, late_printed=False,
      late_note="No clock time printed: \"Registration will close at the start of level seven\" with 20-minute levels.",
      levels=None, lmin=20,
      stack="Schedule table: \"Starting Chips 20,000\"",
      source_label="Official Caesars Palace daily NLH tournament schedule PDF (read 2026-11-17)",
      source_url=SRC["caesars_daily_flyer"],
      single_entry="not single entry - re-entry on elimination within the first break, plus a $50 add-on",
      flag="Rule 26: \"Must have at least 6 players to start a tournament. If a tournament does not have at least "
           "6 players at the scheduled start time the tournament will be canceled, and refunds will be issued.\""),
 dict(id="caesars-daily-14", venue="Caesars Palace", venue_id="caesars", verified_on="2026-11-17",
      name="$160 No Limit Texas Hold'em daily (2 p.m.)", days="Monday-Sunday", start="14:00",
      buy_in_usd=160, guarantee_usd=1000, status="REBUY",
      labels=["recurring", "re-entry", "add-on"],
      fee="Flyer rule 07: \"Of the $160 buy in, $115 goes to the prize pool and $45 is held by Caesars Palace as a "
          "maintenance fee.\" Rule 08: \"Of the $50 add-on, $45 goes to the prize pool and $5 is held by Caesars "
          "Palace as a maintenance fee.\"",
      ex="Schedule table row, printed verbatim: \"2 PM $160 $50 20,000 20 Minutes $1,000\". "
         "Sign-ups: \"Sign-ups start one hour before the scheduled start of the event\" - 1:00 p.m. for this start.",
      late=None, late_printed=False,
      late_note="No clock time printed: \"Registration will close at the start of level seven\" with 20-minute levels.",
      levels=None, lmin=20,
      stack="Schedule table: \"Starting Chips 20,000\"",
      source_label="Official Caesars Palace daily NLH tournament schedule PDF (read 2026-11-17)",
      source_url=SRC["caesars_daily_flyer"],
      single_entry="not single entry - re-entry on elimination within the first break, plus a $50 add-on",
      flag=None),
 dict(id="caesars-daily-18", venue="Caesars Palace", venue_id="caesars", verified_on="2026-11-17",
      name="$100 No Limit Texas Hold'em daily (6 p.m.)", days="Monday-Sunday", start="18:00",
      buy_in_usd=100, guarantee_usd=1000, status="REBUY",
      labels=["recurring", "re-entry", "add-on"],
      fee="Flyer rule 06: \"Of the $100 buy in, $70 goes to the prize pool and $30 is held by Caesars Palace as a "
          "maintenance fee.\"",
      ex="Schedule table row, printed verbatim: \"6 PM $100 $50 20,000 20 Minutes $1,000\". "
         "Sign-ups open 5 p.m. (\"one hour before the scheduled start\").",
      late=None, late_printed=False,
      late_note="No clock time printed: \"Registration will close at the start of level seven\" with 20-minute levels.",
      levels=None, lmin=20,
      stack="Schedule table: \"Starting Chips 20,000\"",
      source_label="Official Caesars Palace daily NLH tournament schedule PDF (read 2026-11-17)",
      source_url=SRC["caesars_daily_flyer"],
      single_entry="not single entry - re-entry on elimination within the first break, plus a $50 add-on",
      flag=None),
 dict(id="caesars-daily-21", venue="Caesars Palace", venue_id="caesars", verified_on="2026-11-17",
      name="$160 No Limit Texas Hold'em daily (9 p.m.)", days="Monday-Sunday", start="21:00",
      buy_in_usd=160, guarantee_usd=1000, status="REBUY",
      labels=["recurring", "re-entry", "add-on", "nightcap"],
      fee="Flyer rule 07: \"Of the $160 buy in, $115 goes to the prize pool and $45 is held by Caesars Palace as a "
          "maintenance fee.\"",
      ex="Schedule table row, printed verbatim: \"9 PM $160 $50 20,000 20 Minutes $1,000\". "
         "Rule 27: \"Prize pool may not be chopped until the end of registration.\"",
      late=None, late_printed=False,
      late_note="No clock time printed: \"Registration will close at the start of level seven\" with 20-minute levels.",
      levels=None, lmin=20,
      stack="Schedule table: \"Starting Chips 20,000\"",
      source_label="Official Caesars Palace daily NLH tournament schedule PDF (read 2026-11-17)",
      source_url=SRC["caesars_daily_flyer"],
      single_entry="not single entry - re-entry on elimination within the first break, plus a $50 add-on",
      flag=None),
]


# ---------------- helpers ----------------
def to_min(hhmm):
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def to_hhmm(mins):
    mins = int(mins) % (24 * 60)
    return "%02d:%02d" % (mins // 60, mins % 60)


def clock(hhmm):
    """'3:40 PM' -> '15:40'."""
    m = re.match(r"^(\d{1,2}):(\d{2})\s*(AM|PM)$", hhmm.strip())
    if not m:
        return hhmm
    h, mm, ap = int(m.group(1)), int(m.group(2)), m.group(3)
    if ap == "PM" and h != 12:
        h += 12
    if ap == "AM" and h == 12:
        h = 0
    return "%02d:%02d" % (h, mm)


def estimate_end(start, levels, level_min, breaks=15, every=4, level_min2=None, level_min2_from=None):
    """Plausible end time from the published level structure (estimate, not an official time).

    Returns ``(wall_clock, total_minutes, days_after_start)``. The finish is
    stored as a clock time **plus** the number of calendar days past the start
    date, because a long level structure legitimately runs past midnight: a
    bare clock time silently wrapped to the small hours of the same day, which
    then read as earlier than the event's own start and made every later event
    on that date look playable (found by session 206debc0, fixed here as F61).
    """
    if level_min2 and level_min2_from:
        early = min(level_min2_from - 1, levels)
        play = early * level_min + (levels - early) * level_min2
    else:
        play = levels * level_min
    total = play + (levels // every) * breaks
    absolute = to_min(start) + total
    return to_hhmm(absolute), total, absolute // (24 * 60)


def end_abs_min(event):
    """Absolute end time in minutes from midnight of the event's own date.

    ``est_end`` is stored time-only (``to_hhmm`` wraps at 24h), so every comparison
    must use this unwrapped value instead. Returns None when no duration is known.
    """
    if event.get("est_duration_min") is not None:
        return to_min(event["start"]) + event["est_duration_min"]
    if event.get("est_end"):
        # Reconstruct the duration from the wrapped pair (24h ambiguity is not
        # resolvable here; the generator always sets est_duration_min, so this is
        # only a defensive fallback).
        return to_min(event["start"]) + ((to_min(event["est_end"]) - to_min(event["start"])) % (24 * 60))
    return None


def fmt_est_end(event):
    """Human end time: '02:55 (next day)' when the estimate wraps past midnight."""
    if not event.get("est_end"):
        return None
    end = end_abs_min(event)
    return event["est_end"] + (" (next day)" if end is not None and end >= 24 * 60 else "")


def rule_field(value, excerpt, source_label, source_url, clause=None, retrieved=LAST_CHECKED):
    out = {"value": value, "excerpt": excerpt, "source": {"label": source_label, "url": source_url},
           "retrieved_on": retrieved}
    if clause:
        out["clause"] = clause
    return out


def mark_flight_pricing(rows):
    """P3 (built 2026-11-19, session cebd4457): descriptive 'effectively single entry' flag.

    Flags multi-flight events whose flights ALL cost the same and whose structure sheet only
    bars a bagged player from a later flight (clause 08: "Any player who bags chips for Day 2
    may not play a subsequent flight."), staying silent on a whole-event entry limit. This is
    a descriptive flag beside the classification, NEVER a reclassification: flagged rows keep
    entry_status MULTI and are excluded from the single-entry shortlist and the ranking.
    Not flagged: rows whose sheet explicitly prices later buy-ins (the Valuetown clause-07
    sheets), and the WPT rows whose sheets print entry caps ("One entry plus one re-entry per
    flight", "Four (4) Entries maximum")."""
    groups = {}
    for r in rows:
        if r.get("entry_status") == "MULTI":
            groups.setdefault((r.get("series"), r.get("event_no")), []).append(r)
    for key, grp in groups.items():
        if len(grp) < 2:
            continue
        buys = {r.get("buy_in_usd") for r in grp}
        if len(buys) != 1:
            continue
        if not all("may not play a subsequent flight"
                   in ((r.get("rules", {}).get("single_entry") or {}).get("excerpt") or "") for r in grp):
            continue
        for r in grp:
            se = r["rules"]["single_entry"]
            r["flight_pricing"] = {
                "flag": "effectively single entry (descriptive only - not a confirmed one-entry freezeout)",
                "all_flights_same_buy_in_usd": sorted(buys)[0],
                "excerpt": se.get("excerpt"),
                "silence_note": ("The sheet prints one price for every flight and bars only a bagged player from "
                                 "a later flight; it is silent on a whole-event entry limit and on whether a "
                                 "player who busts a flight may enter a later one. The row stays MULTI and is "
                                 "excluded from the single-entry shortlist and the ranking."),
                "source": se.get("source"),
                "retrieved_on": se.get("retrieved_on", LAST_CHECKED),
            }
            if "effectively single entry" not in r["labels"]:
                r["labels"].append("effectively single entry")
    return rows

def fee_clause_quote(published, buy, fee, pool):
    """Quote the house-fee clause in the sheet's OWN words.

    The old form painted the fee figure over one fixed sentence. That is
    faithful only for sheets that print that sentence; sheet #28 prints
    "... Buy-In for house fees ... Prize pool consists of ..." and #21/#37/#08
    print comma-formatted "$1,975"/"$1,420", so those quotes could not be found
    in the PDF at all. Here every quoted span is lifted from the snapshot text,
    so a quote is the document's words by construction: the fee sentence and,
    as its own quoted sentence, the prize-pool sentence that makes the fee's
    basis checkable.

    The clause is numbered 06 on most sheets but 07 on the sheets that print a
    separate tax clause, so the number is read off the document rather than
    assumed.
    """
    snap_rel = ((published or {}).get("snapshot") or "")
    snap = os.path.join(ROOT, snap_rel) if snap_rel else None
    if not snap or not os.path.exists(snap):
        return None, None, None
    with open(snap, encoding="utf8") as f:
        text = f.read()
    flat = re.sub(r"-\s*\n\s*", "-", text)
    flat = re.sub(r"\s+", " ", flat)
    anchor = re.search(r"\$[\d,]+ of the \$[\d,]+ Buy-?In", flat, re.I)
    if not anchor:
        return None, None, None
    # Walk back to the numbered clause this sentence belongs to.
    before = flat[:anchor.start()]
    heads = list(re.finditer(r"(?<![\d.])(0?\d{1,2})\.\s+(?=[A-Z$])", before))
    if not heads:
        return None, None, None
    clause_no = int(heads[-1].group(1))
    start_at = heads[-1].end()
    nxt = re.search(r"(?<![\d.])0?\d{1,2}\.\s+(?=[A-Z$])", flat[anchor.end():])
    clause = flat[start_at:anchor.end() + (nxt.start() if nxt else 0)].strip()

    def sentences(block):
        return [x.strip() for x in re.split(r"(?<=\.)\s+(?=[A-Z$])", block) if x.strip()]

    parts = sentences(clause)
    fee_sentence = pool_sentence = None
    for i, sent in enumerate(parts):
        if re.search(r"\$[\d,]+ of the \$[\d,]+ Buy-?In", sent, re.I):
            fee_sentence = re.split(r"\s(?=On Day 1[A-F]\b)", sent)[0].strip()
            for nxt_s in parts[i + 1:]:
                if re.search(r"(?:consists of|fee for Vegas Connected|Prize pool consists)", nxt_s, re.I):
                    pool_sentence = nxt_s
                    break
            break
    if not fee_sentence:
        return None, None, None
    return clause_no, fee_sentence, pool_sentence
# Day the DeepStack Extravaganza IV event listing was re-read live, field by field, against
# every published row (sessions 98241f2f, 336fb2af and aa1e89b0 recorded 94/94 and 16-28 Nov
# matches in COORDINATION.md; session a3822303 re-read structure sheets #5 and #30 live the
# same day). It stamps last_checked for that series only; verified_on keeps the original
# sheet-reading date, and the NYE series was not re-read on 2026-11-19 so it keeps LAST_CHECKED.
DSE_REREAD_ON = "2026-11-19"


def build_venetian(rows, series_key, series, page_key, sheet_key, sched_key, struct_key):
    out = []
    with open(os.path.join(DATA, "structure_rules.json"), encoding="utf8") as f:
        printed = json.load(f)
    for (date, start, no, name, gtd, sheet_no) in rows:
        published = printed[f"v_{series_key}_struct_{sheet_no:02d}"]
        sheet = sheet_key[sheet_no]
        # A re-read of this sheet's own official document, if there was one; the date
        # is what lets `last_checked` and the retrieval dates move for these rows only.
        reread = REREAD.get((series_key, sheet_no))
        retrieved = reread[0] if reread else LAST_CHECKED
        continuation = "Restart" in name or "Final Table" in name
        status = sheet["status"]
        ex = sheet.get("ex", EX_SE)
        # A sheet that prints a further-entry sentence cannot be classified as a
        # silent candidate: the sentence is evidence AGAINST single entry. This is
        # the rule the 2026-11-19 audit found was applied to Event #29 only: the
        # same sheet was read as "re-entry allowed" on that row and as "no such
        # clause appears anywhere" on the six other bounty events that cite it.
        if status == "CAND" and (published or {}).get("re_entry_excerpt") \
                and re.search(r"subsequent re-?entry", (published.get("re_entry_excerpt") or ""), re.I):
            if not re.search(r"\bfor\s+event\s*#?\s*\d+\b.{0,60}?\bonly\b",
                             (published.get("re_entry_excerpt") or ""), re.I) \
                    or no == 29:
                status = "RE"
                ex = EX_DISCOUNT_REENTRY
        override = DEC_EVENT_OVERRIDE.get((series_key, no)) if series_key == "dec" else None
        if override:
            status = override["status"]
            ex = override["ex"]
        labels = list(sheet.get("labels", []))
        if continuation:
            labels.append("continuation")
        if continuation:
            status = "CONT"
        buy = sheet["buy"]
        start_time = start
        if sheet.get("start") is None:
            start_time = {"45": "20:10", "46": "09:10", "48": "12:10",
                          "6": "15:10", "7": "18:10", "9": "15:10", "10": "18:10",
                          "11": "15:10", "12": "18:10",
                          "15": "15:10", "18": "15:10", "21": "15:10", "23": "10:10", "24": "15:10"}[str(no)]
        late_text = sheet.get("late_by_event", {}).get(no, sheet.get("late"))
        if continuation:
            late_text = None  # Day 1 registration is not available at a restart.
        elif series_key == "dec" and no == 27 and start == "17:10":
            late_text = "9:40 PM"  # NYE schedule PDF, flights 1B and 1D.
        est_end, est_min, est_offset_days = estimate_end(
            start_time, sheet["levels"], sheet["lmin"],
            level_min2=sheet.get("lmin2"), level_min2_from=sheet.get("lmin2_from"))
        struct_url = SRC[struct_key].format(sheet_no)
        _clause_no, _fee_sentence, _pool_sentence = fee_clause_quote(published, buy, sheet["fee"], sheet["pool"])
        if _fee_sentence:
            fee_ex = "Clause %02d: \"%s\"" % (_clause_no, _fee_sentence)
            if _pool_sentence:
                fee_ex += " \"%s\"" % _pool_sentence
        else:
            fee_ex = ("Clause 06: \"$%d of the $%s Buy-In is withheld for house fees (Rake + Staff). The prize pool "
                      "consists of $%d of every $%s Buy In.\" [templated: the sheet prints the fee figure but no "
                      "single sentence was located]" % (sheet["fee"], format(buy, ","), sheet["pool"], format(buy, ",")))
        lips_fee = 10 if sheet_no in (31, 33) else (20 if sheet_no == 32 else 0)
        house_fee_value = sheet["fee"] - lips_fee
        if sheet_no in (31, 32, 33):
            fee_ex = ("Clause 06: \"$%d of the $%s Buy-In is withheld for house fees (Rake + Staff). "
                      "$%d of the $%s Buy In will be withheld as a flat fee for Vegas Connected, INC, DBA Ladies "
                      "International Poker Series (LIPS). Prize pool consists of $%d of every $%s Buy In.\""
                      % (house_fee_value, format(buy, ","),
                         lips_fee, format(buy, ","),
                         sheet["pool"], format(buy, ",")))
        rules = {
            "single_entry": rule_field(
                "not stated" if status == "CAND" else ("not single entry" if status in ("MULTI", "RE", "REBUY") else "unknown"),
                ex, "Structure sheet #%d" % sheet_no, struct_url,
                clause="08" if "Clause 08" in ex else ("07" if "Clause 07" in ex else ("06" if "Clause 06" in ex else None)),
                retrieved=retrieved),
            "re_entry": rule_field(
                "allowed" if status in ("RE", "REBUY") else ("possible for later flights" if status == "MULTI" else "not mentioned"),
                ex, "Structure sheet #%d" % sheet_no, struct_url, retrieved=retrieved),
            "add_on": rule_field(
                "allowed" if status == "REBUY" else "not mentioned",
                ex, "Structure sheet #%d" % sheet_no, struct_url, retrieved=retrieved),
            "fee": rule_field(
                "house fee $%d of the $%s buy-in; prize pool $%d" % (sheet["fee"], format(buy, ","), sheet["pool"]),
                fee_ex, "Structure sheet #%d" % sheet_no, struct_url, clause="06", retrieved=retrieved),
        }
        srcs = [{"label": "Official event page", "url": SRC[page_key]},
                {"label": "Structure sheet #%d" % sheet_no, "url": struct_url}]
        if sched_key:
            srcs.insert(1, {"label": "Official schedule PDF", "url": SRC[sched_key]})
        flags = []
        if date == "2026-12-26":
            flags.append(DATE_TYPO_DEC26)
        if date == "2027-01-05":
            flags.append(DATE_TYPO_TUESDAY)
        if lips_fee:
            flags.append(LIPS_FEE_FLAG)
        if series_key == "nov" and sheet_no == 30:
            flags.append(STRUCT30_CLAUSE9_REWORDED)
        # Re-read 2026-11-17: the event page prints 11:10 AM for this restart, the structure
        # sheet says Day 2 resumes at 11:00 AM. The conflict is published, not resolved.
        start_conflict = date == "2027-01-04" and no == 20 and continuation
        if start_conflict:
            flags.append(MSPT_DAY2_START_CONFLICT)
        if sheet.get("note"):
            note = sheet["note"]
        elif start_conflict:
            note = ("Continuation of the event above - no new entry. The stored time comes from "
                    "structure sheet #%d clause 3; the official event page prints 11:10 AM for this "
                    "row, which is recorded as a flag on the row." % sheet_no)
        elif continuation:
            note = "Continuation of the event above - no new entry. Official event page row."
        else:
            note = "Read from the official event page and structure sheet #%d on 2026-11-16." % sheet_no
        if reread:
            # What the 2026-11-19 fetch actually found, printed on the row it belongs to:
            # every compared field matched, and the entry-rule wording is quoted, not summarised.
            note += (" Re-read %s: structure sheet #%d was fetched again and compared field by "
                     "field - the buy-in, guarantee, fee split, prize pool, starting stack, level "
                     "count and length, late-registration deadline and payout clause all match "
                     "what is published here, and %s." % (reread[0], sheet_no, reread[1]))
        row = {
            "id": None,
            "series": series, "venue": VEN, "date": date, "start": start_time,
            "kind": "continuation" if continuation else "entry",
            "event_no": no, "name": name,
            "buy_in_usd": buy, "guarantee_usd": gtd,
            "prize_text": ("%d seats to %s" % (sheet["seats"], sheet["target"])) if sheet.get("seats") else None,
            "house_fee_usd": house_fee_value, "house_fee_pct": round(100.0 * house_fee_value / buy, 2),
            "lips_fee_usd": lips_fee if lips_fee else None,
            "prize_pool_usd": sheet["pool"],
            "gtd_multiple": round(gtd / buy, 1) if gtd and buy else None,
            "entry_status": status, "rules": rules,
            "entry_rule": {
                "CAND": "Unverified freezeout: sheet reviewed; no written maximum entry, rebuy or add-on policy.",
                "MULTI": "Not single entry: structure sheet allows or implies a further entry (multi-flight or later buy-in).",
                "RE": "Re-entry confirmed: structure sheet states re-entry terms.",
                "REBUY": "Rebuy / add-on confirmed: extra money buys more chances.",
                "CONT": "Continuation row (Day 2 / final table). No new entry is possible.",
                "UNV": "Entry rule not confirmed from an official structure sheet.",
            }.get(status, ""),
            "labels": labels,
            "late_reg_close": clock(late_text) if late_text else None,
            "levels": sheet["levels"], "level_minutes": sheet["lmin"],
            "starting_chips": None if continuation else int(published["chips"].split()[0].replace(",", "")),
            "payout_excerpt": published.get("payout_excerpt"),
            "est_end": est_end, "est_duration_min": est_min,
            # Minutes from midnight of the event's own date to the estimated
            # finish. This is the value the day plan compares against, so a
            # finish after midnight is never compared as a same-day clock time.
            "est_end_abs_min": to_min(start_time) + est_min,
            "est_end_days_after": est_offset_days,
            "note": note,
            "flags": flags,
            "sources": srcs, "verified_on": VERIFIED_ON,
            # 2026-11-19, from either re-read that happened that day: the whole
            # series listing page was re-read (DSE_REREAD_ON, every nov row), or this
            # row's own structure sheet was fetched again (REREAD -> retrieved).
            # NYE rows that were re-read under neither keep LAST_CHECKED.
            "last_checked": DSE_REREAD_ON if series_key == "nov" else retrieved,
        }
        # Session cebd4457: a dated recheck record for rows whose sheet was NOT
        # re-read in full on 2026-11-19 (the listing page was, row by row).
        if not reread:
            row["recheck"] = {
                "on": "2026-11-19",
                "url": SRC[page_key],
                "what": ("The official series listing page was re-read row by row on 2026-11-19 (session "
                         "cebd4457) and every printed value for this row still matches (Nov 94/94, Dec 49/49). "
                         "This row's structure-sheet PDF was NOT re-read in full on 2026-11-19 (the daily "
                         "source monitor re-fetched it and its extracted facts show no change), so the "
                         "row's last_checked stays 2026-11-17."),
            }
        if sheet.get("seats"):
            row["satellite"] = {
                "seats_awarded": sheet["seats"],
                "target_event": sheet["target"],
                "milestone_chips": 200000,
                "excerpt": "Clause 09: \"A Player who accumulates 200,000 in tournament chips (\"The Milestone\") or "
                           "more will instantly receive direct entry into %s.\"" % sheet["target"],
            }
        out.append(row)
    return out


_WPT_ROW_SHEETS = json.load(open(os.path.join(DATA, "wpt_row_sheets.json"), encoding="utf-8"))


def _sheet_for(join, date, time, buy, name):
    """Return the joined structure-sheet record for this schedule row, or None.

    Most printed (date, start time, buy-in) keys are unique, but a few sheets share
    one (for example Dec 7, 11:00, $1,100 is printed by both the HORSE sheet and the
    Prime Championship sheet). When the key is ambiguous, the sheet whose printed
    title shares the most words with the row name wins — the same rule
    ``scripts/extract_wpt_sheets.py`` uses — so each row is priced from its own
    printed fee split and never from a neighbour's.
    """
    cands = [rec for rec in join["matched"].values()
             if rec.get("key") == [date, time, buy]]
    if len(cands) <= 1:
        return cands[0] if cands else None

    def overlap(rec):
        a = set(re.findall(r"[a-z0-9]+", (rec.get("title") or "").lower()))
        b = set(re.findall(r"[a-z0-9]+", (name or "").lower()))
        return len(a & b)
    return max(cands, key=overlap)


def _chips_from(stack_text):
    m = re.search(r"([\d,]{4,})\s+in tournament chips", stack_text or "")
    return int(m.group(1).replace(",", "")) if m else None


def build_wynn():
    """Wynn rows. Entry rules come from the printed structure sheet for the row.

    ``scripts/extract_wpt_struct.py`` parses every structure sheet in the official
    WPT structures PDF and ``scripts/extract_wpt_sheets.py`` joins each schedule
    row to the sheet that prints the same date, start time and buy-in. When the
    join is not unique the row keeps the schedule's values and is flagged, so no
    entry rule is ever inferred.
    """
    out = []
    for (date, time, name, buy, gtd, gtext, chips, levels_pub, kind, skey, flags) in WPT:
        flags = list(flags)
        # The hard-coded key still carries the long-form notes for the events a
        # reviewer has already checked; the printed sheet is preferred wherever
        # the join found one.
        st = WPT_STRUCTS.get(skey) if skey else None
        sheet_row = _sheet_for(_WPT_ROW_SHEETS, date, time, buy, name)
        sid = None
        if sheet_row:
            sid = "block %d" % sheet_row["block"]
            delta = sheet_row.get("printed_time_delta_min") or 0
            if delta:
                printed = [t for d, t in sheet_row.get("sheet_dates") or [] if d == date and t != time]
                flags.append(
                    "Start time conflict between the two official documents: the schedule PDF prints %s "
                    "for this event, while structure sheet %s prints %s on the same date. The schedule's "
                    "time is kept and the difference (%d minutes) is published rather than reconciled."
                    % (time, sid, " / ".join(printed) or "a different time", delta))
            status = "RE" if sheet_row["unlimited_re_entry"] else "MULTI"
            ex = "Registration: \"%s\"" % sheet_row["registration"]
            fee_text = sheet_row["entry_fee_line"]
            stack_text = sheet_row["starting_stack"]
            length_text = sheet_row["length_of_play"] or (st.get("length") if st else None)
            breaks_text = None
            payout_text = None
            struct_url = SRC["wpt_struct"]
            struct_label = "Official structures PDF, %s" % sid
        elif st:
            status = st["status"]
            ex = st["ex"]
            fee_text = st["fee"]
            stack_text = st["stack"]
            length_text = st["length"]
            breaks_text = st["breaks"]
            payout_text = st["payout"]
            struct_url = SRC["wpt_struct"]
            struct_label = "Official structures PDF (%s)" % st["label"]
        else:
            status = "UNV"
            ex = ("No structure sheet in the official WPT World Championship Structures PDF prints this "
                  "date, start time and buy-in combination, so the entry rule is not published for this row.")
            fee_text = None
            stack_text = None
            length_text = None
            breaks_text = None
            payout_text = None
            struct_url = None
            struct_label = None
        if kind == "continuation":
            # A Day 2 or final-table row never sells a new entry, so its entry
            # status is a continuation whatever the parent sheet allows.
            status = "CONT"
        labels = []
        low = name.lower()
        if "bounty" in low:
            labels.append("bounty")
        if "mystery" in low:
            labels.append("mystery-bounty")
        if "Turbo" in name:
            labels.append("turbo")
        if "Satellite" in name:
            labels.append("satellite")
        if "Day 1" in name or "Day 2" in name or "Final Table" in name:
            labels.append("multi-flight")
        if "Seniors" in name or "50+" in name:
            labels.append("seniors-50-plus")
        if "Ladies" in name:
            labels.append("ladies")
        if sheet_row and sheet_row["multi_entry"] and not sheet_row["unlimited_re_entry"]:
            labels.append("limited-re-entry")
        if kind == "continuation":
            labels.append("continuation")
        srcs = [{"label": "Official schedule PDF", "url": SRC["wpt_sched"]}]
        if struct_url:
            srcs.append({"label": struct_label, "url": struct_url})
        src_label = struct_label or "Official schedule PDF"
        src_url = struct_url or SRC["wpt_sched"]
        rules = {
            "single_entry": rule_field(
                "not single entry" if status in ("RE", "REBUY", "MULTI") else ("not applicable" if status == "CONT" else "unknown"),
                ex, src_label, src_url, retrieved=WPT_REREAD_ON),
            "re_entry": rule_field("allowed" if status in ("RE", "REBUY", "MULTI") else "unknown",
                                   ex, src_label, src_url, retrieved=WPT_REREAD_ON),
            "add_on": rule_field(
                "not mentioned on the structure sheet" if struct_url else "not published for this event",
                ex, src_label, src_url, retrieved=WPT_REREAD_ON),
            "fee": rule_field(fee_text or "not published for this event", fee_text or ex, src_label, src_url,
                              retrieved=WPT_REREAD_ON),
        }
        if stack_text:
            rules["starting_chips"] = rule_field(stack_text, stack_text, src_label, src_url, retrieved=WPT_REREAD_ON)
        if length_text:
            rules["length_of_play"] = rule_field(length_text, length_text, src_label, src_url, retrieved=WPT_REREAD_ON)
        row = {
            "id": None, "series": "WPT World Championship (Wynn)", "venue": WYN, "date": date, "start": time,
            "kind": kind, "event_no": None, "name": name,
            "buy_in_usd": buy, "guarantee_usd": gtd, "prize_text": gtext,
            "house_fee_usd": (sheet_row["tournament_fee_usd"] + sheet_row["staff_fee_usd"])
                             if sheet_row and sheet_row["tournament_fee_usd"] else None,
            "house_fee_pct": None, "prize_pool_usd": sheet_row["prize_pool_usd"] if sheet_row else None,
            "gtd_multiple": round(gtd / buy, 1) if gtd and buy else None,
            "entry_status": status, "rules": rules,
            "entry_rule": {
                "RE": "Re-entry confirmed: the printed structure sheet states the re-entry terms.",
                "MULTI": "Not single entry: the printed structure sheet states a limited number of entries "
                         "(for example one entry plus one re-entry per flight), so a second entry is possible.",
                "CONT": "Continuation row (Day 2, Day 3 or final table). No new entry is sold on this day; "
                        "the parent event's entry rule is recorded on its Day 1 rows.",
                "UNV": "Entry rule not verified: no structure sheet for this event is published in the "
                       "official structures PDF.",
            }.get(status, ""),
            "labels": labels,
            "late_reg_close": None,
            "levels": None,
            "level_minutes": sheet_row["level_minutes"] if sheet_row else None,
            "starting_chips": _chips_from(stack_text) or chips,
            "levels_published": levels_pub,
            "est_end": None, "est_duration_min": None,
            "note": ("Buy-in, guarantee, starting chips and level count from the official WPT World Championship "
                     "schedule PDF. " + ("Entry rule, fee split and starting stack from %s of the official "
                     "structures PDF." % sid if sheet_row else "No structure sheet is published for this row.")),
            "flags": flags,
            "sources": srcs, "verified_on": VERIFIED_ON, "last_checked": WPT_REREAD_ON,
        }
        # The fee percentage is computed against the entry the structure sheet
        # actually prices (``house_fee_basis_usd``), which is the row's buy-in on
        # every row except the Ladies Championship: that sheet is headed "$11,100
        # (***discounted to $1,100 for Ladies)", so its $135 fee is 1.22% of
        # $11,100 and would be a false 12.27% of the discounted $1,100 entry.
        basis = (sheet_row["buyin_usd"] if sheet_row else buy) or buy
        if row["house_fee_usd"] and basis:
            row["house_fee_pct"] = round(100.0 * row["house_fee_usd"] / basis, 2)
            row["house_fee_basis_usd"] = basis
        if sheet_row and sheet_row["row_buyin_usd"] != buy:
            flags.append(
                "The structure sheet prices this event at $%s, while the schedule prints a $%s entry for "
                "this field; the sheet's own heading says it is discounted for Ladies. The fee split is "
                "quoted from the sheet but no fee percentage is calculated, because the two documents "
                "price different entries." % (format(sheet_row["buyin_usd"], ","), format(buy, ",")))
        if sheet_row and sheet_row.get("length_of_play"):
            row["structure_days"] = sheet_row["length_of_play"]
        if st and st.get("payout"):
            row["structure_payout"] = st["payout"]
        if st and st.get("breaks"):
            row["structure_breaks"] = st["breaks"]
        out.append(row)
    for (date, time, name, buy, gtd, chips, levels_pub, kind, flags) in WSS:
        out.append({
            "id": None, "series": "Wynn Signature Series", "venue": WYN, "date": date, "start": time,
            "kind": kind, "event_no": None, "name": name,
            "buy_in_usd": buy, "guarantee_usd": gtd,
            "prize_text": "10 Seats" if "Milestone Satellite" in name else None,
            "house_fee_usd": None, "house_fee_pct": None, "prize_pool_usd": None,
            "gtd_multiple": round(gtd / buy, 1) if gtd and buy else None,
            "entry_status": "CONT" if kind == "continuation" else "UNV",
            "rules": {
                "single_entry": rule_field("unknown",
                    "The official Wynn Signature Series Structures PDF published by Wynn contains a \"COMING SOON\" "
                    "placeholder and no structure sheets (read on 2026-11-19). Entry rule unknown.",
                    "Official structures placeholder", SRC["wss_struct"], retrieved="2026-11-19"),
                "re_entry": rule_field("unknown",
                    "The official Wynn Signature Series Structures PDF published by Wynn contains a \"COMING SOON\" "
                    "placeholder and no structure sheets (read on 2026-11-19). Entry rule unknown.",
                    "Official structures placeholder", SRC["wss_struct"], retrieved="2026-11-19"),
                "add_on": rule_field("unknown",
                    "The official Wynn Signature Series Structures PDF published by Wynn contains a \"COMING SOON\" "
                    "placeholder and no structure sheets (read on 2026-11-19). Entry rule unknown.",
                    "Official structures placeholder", SRC["wss_struct"], retrieved="2026-11-19"),
                "fee": rule_field("not published", "Fee breakdown is not published for this event.",
                                  "Official Wynn Signature Series schedule PDF", SRC["wss_sched"]),
            },
            "entry_rule": "Continuation: not a new entry." if kind == "continuation" else "Entry rule not verified: the official structures PDF for this series is still a placeholder.",
            "labels": ["series"] + (["satellite"] if "Milestone Satellite" in name else [])
                      + (["continuation"] if kind == "continuation" else []),
            "late_reg_close": None, "levels": None, "level_minutes": None,
            "starting_chips": chips, "levels_published": levels_pub,
            "est_end": None, "est_duration_min": None,
            "note": "Buy-in, guarantee, starting chips and level count from the official Wynn Signature Series "
                    "schedule PDF, re-read 2026-11-19 (table-structure capture of the same file; see "
                    "data/snapshots/wss_sched_reread_20261119.txt).",
            "flags": flags,
            "sources": [{"label": "Official schedule PDF", "url": SRC["wss_sched"]},
                        {"label": "Official structures PDF (placeholder: COMING SOON)", "url": SRC["wss_struct"]}],
            "verified_on": VERIFIED_ON,
            # The series' official schedule PDF and the structures placeholder were both
            # re-read on 2026-11-19; every row of this series was re-checked against its
            # source that day, so these rows' last_checked carries the re-read date.
            # Rows of other series keep their own dates; no date here is advanced
            # without the source having actually been read.
            "last_checked": WSS_REREAD_ON,
        })
    return out


def abs_end_minutes(row):
    """Minutes from midnight *of that row's start day*, or None when unknown.

    `est_end` is stored time-only, so an event that runs past midnight prints an
    end time that reads before its own start (e.g. 11:10 -> 02:55). Comparing
    wall-clock strings would then call an impossible sequence playable. Every
    comparison on this page therefore uses the absolute minute offset built from
    the stored `est_duration_min`; the wrap is never inferred from the clock text.
    """
    if row.get("est_duration_min") is None or not row.get("start"):
        return None
    return to_min(row["start"]) + int(row["est_duration_min"])


# The official event name labels a single-playing-day event "(1Day)". That is the only case in
# which the level structure printed on a sheet ends on the day it starts.
ONE_DAY_RE = re.compile(r"\(\s*1\s*Day\s*\)", re.I)
SATELLITE_LABELS = ("satellite", "milestone-satellite")


def is_satellite(row):
    """A satellite stops when the seats it awards are given out, not when its level table ends."""
    return ("satellite" in (row.get("name") or "").lower()
            or bool(set(SATELLITE_LABELS) & set(row.get("labels") or [])))


def duration_basis(row):
    """What a printed level table is entitled to say about the event's first playing day.

    day_maximum              - the event is labelled "(1Day)", so the table is that day's table.
                               No sheet prints an end clock; the event ends when its field is paid
                               (sheet #6 clause 7: "This event pays 12.5% of the field"), so the
                               end of the table is the LATEST the event can run, never a schedule.
                               70 of these 73 rows carry a table that cannot fit inside a day at
                               all, which is flag F75.
    satellite_maximum        - every satellite sheet read for this dataset prints, as its own
                               clause 10, "The tournament will conclude when the number of players
                               remaining is equal to the remaining number of ... direct entry seats
                               to be awarded". A ceiling on the day, never a clock.
    no_day_bound             - a flight of a multi-day event, or a "(2Day)" event. Clause 3 reads
                               "Each starting flight will play until we are down to approximately
                               12.5% of the field remaining. Day 2 will resume at 11:00 AM", so the
                               table spans more than one playing day and bounds nothing about the
                               first day.
    """
    if not row.get("est_end"):
        return None
    if is_satellite(row):
        return "satellite_maximum"
    return "day_maximum" if ONE_DAY_RE.search(row.get("name") or "") else "no_day_bound"


def seq_end(row):
    """The latest minute from the start day's midnight at which the event can still be running.

    Both accepted bases bound the day from above. A table that spans more than one playing day is
    refused here rather than read as a finish time, and a row with no structure at all stays
    unknown. Because this is a maximum it can rule a pairing out; it can never prove a clock.
    """
    if duration_basis(row) not in ("day_maximum", "satellite_maximum"):
        return None
    return abs_end_minutes(row)


def entry_deadline(row):
    """Last minute of the start day at which a player can still be seated.

    The published late-registration cut-off when the sheet gives one; otherwise the start time.
    An event with no printed cut-off is treated as closed at its start, never assumed open.
    """
    return to_min(row.get("late_reg_close") or row["start"])


def clock_label(mins):
    """Minutes from the start day's midnight, as 'HH:MM' plus the day it crosses into."""
    return to_hhmm(mins) + (" (+1 day)" if mins >= 24 * 60 else "")



def build_schedule(rows):
    """Day plan: one verified single-entry primary per date, a provable fallback or none, overlap flags.

    Every comparison is in absolute minutes from the start day's midnight (``seq_end``), because
    ``est_end`` is a wall-clock time that wraps at midnight. A second event is published as a
    conditional fallback only when the primary cannot run past the second event's entry deadline.
    Pairs are flagged ``unplannable`` when the earlier event's own table runs past the later
    event's entry deadline (or when both start at the same instant, which no schedule can serve),
    and ``join_in_progress`` when that ceiling passes the later start but not its deadline. A
    structure that spans more than one playing day bounds nothing, so such a day is never paired.
    """
    days = {}
    for r in rows:
        if r["kind"] != "entry":
            continue
        days.setdefault(r["date"], []).append(r)
    order = {d: i for i, d in enumerate(sorted(days))}

    def abs_start(e):
        return order[e["date"]] * 24 * 60 + to_min(e["start"])

    def abs_end(e):
        return abs_start(e) + e["est_duration_min"] if e.get("est_duration_min") is not None else None

    # Overlap scan over the whole dataset in absolute time: b cannot be played
    # after (or during) a when b starts before a's estimated end.
    conflicts_by_day = {}
    flat = sorted((r for r in rows if r["kind"] == "entry"),
                  key=lambda e: (e["date"], e["start"], e["name"]))
    for i, a in enumerate(flat):
        a_end = abs_end(a)
        if a_end is None:
            continue
        for b in flat[i + 1:]:
            if abs_start(b) < a_end:
                if a["date"] != b["date"]:
                    detail = ("%s starts %s on %s while %s (started %s on %s) is still estimated to run until %s"
                              % (b["name"], b["start"], b["date"], a["name"], a["start"], a["date"],
                                 fmt_est_end(a)))
                else:
                    detail = ("%s starts %s while %s is still estimated to run until %s"
                              % (b["name"], b["start"], a["name"], fmt_est_end(a)))
                conflicts_by_day.setdefault(b["date"], []).append(
                    {"a": a["id"], "b": b["id"], "detail": detail})
    plan = []
    for d in sorted(days):
        events = sorted(days[d], key=lambda e: (e["start"], e["name"]))
        se = [e for e in events if e["entry_status"] == "CAND"]
        primary = se[0] if se else None
        p_end = seq_end(primary) if primary else None
        fallback = None
        fallback_kind = None
        if p_end is not None:
            for cand in se[1:]:
                if p_end <= to_min(cand["start"]):
                    fallback, fallback_kind = cand, "from the start"
                    break
                if p_end <= entry_deadline(cand):
                    fallback, fallback_kind = cand, "join in progress"
                    break
        conflicts = []
        undecidable = []
        for i, a in enumerate(events):
            a_end = seq_end(a)
            same_start_seen = set()
            for b in events[i + 1:]:
                # Two events printed with the same start time overlap by definition - that needs no
                # estimate at all. Otherwise a pair is unplannable only when the earlier event's own
                # table runs past the later event's entry deadline.
                same_start = a["start"] == b["start"]
                if not same_start and a_end is None:
                    # No published level structure for the earlier event: the pair cannot be
                    # checked, so it is counted and listed rather than silently dropped.
                    undecidable.append({"a": a["id"], "b": b["id"], "a_start": a["start"],
                                        "b_start": b["start"],
                                        "detail": "%s (%s) and %s (%s) cannot be checked: %s publishes no level structure."
                                        % (a["name"], a["start"], b["name"], b["start"], a["name"])})
                    continue
                b_start, b_close = to_min(b["start"]), entry_deadline(b)
                base = {"a": a["id"], "b": b["id"], "a_basis": duration_basis(a),
                        "a_start": a["start"], "a_end": clock_label(a_end) if a_end is not None
                        else "unknown (no same-day structure)", "b_start": b["start"]}
                if same_start:
                    base.update({"kind": "unplannable", "gap_min": 0,
                                 "detail": "%s and %s both start at %s - one table cannot seat a "
                                           "player twice, so no published schedule can put both on one day"
                                           % (a["name"], b["name"], a["start"])})
                elif a_end > b_close:
                    base.update({"kind": "unplannable", "gap_min": b_close - a_end,
                                 "detail": "%s starts %s and its entry closes %s, while %s's own table can "
                                           "run as late as %s and no source prints an earlier end - so "
                                           "nothing published supports planning both on one day"
                                           % (b["name"], b["start"], b.get("late_reg_close") or b["start"],
                                              a["name"], clock_label(a_end))})
                elif a_end > b_start:
                    base.update({"kind": "join_in_progress", "gap_min": b_start - a_end,
                                 "detail": "%s starts %s while %s can still be running as late as %s - the "
                                           "pair is only sensible if you are willing to sit down in progress"
                                           % (b["name"], b["start"], a["name"], clock_label(a_end))})
                else:
                    continue
                conflicts.append(base)
        # Every other single-entry event that day is an alternative to the primary, never an
        # addition to it: playing it means being free of the primary by its entry deadline, which
        # is a question of when you are eliminated, not of any schedule.
        basis = duration_basis(primary) if primary else None
        alternatives = []
        for other in (se[1:] if primary else se):
            if primary and other["id"] == (fallback or {}).get("id"):
                continue
            close = other.get("late_reg_close") or other["start"]
            if p_end is None:
                why = ("The primary event has no same-day ceiling to plan against, so it is not known"
                       " whether this one can be reached - choose it instead of the primary, not as well.")
            elif basis == "no_day_bound" or duration_basis(other) == "no_day_bound":
                why = ("The primary event's table spans more than one playing day, so this date has no"
                       " published ceiling to plan against - choose it instead of the primary, not as well.")
            elif p_end > to_min(other["start"]):
                why = ("The primary's own table can run as late as %s; reaching this event means being out"
                       " of the primary and seated before its entry closes at %s - a question of when you"
                       " are eliminated, which no source publishes." % (clock_label(p_end), close))
            else:
                why = ("Starts at or after the end of the primary's published table, so it is a genuine"
                       " either/or for the day.")
            alternatives.append({"id": other["id"], "start": other["start"], "name": other["name"],
                                 "buy_in_usd": other["buy_in_usd"], "guarantee_usd": other["guarantee_usd"],
                                 "entry_closes": close, "late_reg_published": bool(other.get("late_reg_close")),
                                 "note": why})
        if not primary:
            note = "No sheet-reviewed candidate on this date."
        elif not fallback:
            if basis == "no_day_bound":
                note = ("The primary event's table spans more than one playing day - its sheet says the"
                        " flight plays until about 12.5% of the field remains and that Day 2 resumes at a"
                        " printed clock - so the official sources give this day no ceiling to plan against.")
            elif p_end is None:
                note = ("No structure sheet was published for the primary event, so it has no end time at"
                        " all and no second event can be promised after it.")
            elif basis == "satellite_maximum":
                note = ("The primary event is a satellite, which its own sheet concludes as soon as the"
                        " remaining seats are awarded; nothing prints when that happens, so no second event"
                        " can be promised after it.")
            elif len(se) < 2:
                note = ("This is the only sheet-reviewed candidate on this date, so the day is planned"
                        " around it alone.")
            else:
                note = ("No other candidate on this date can still be entered by the time the"
                        " primary's own table ends at %s - the day is planned around the primary alone."
                        % clock_label(p_end))
        elif fallback_kind == "join in progress":
            note = ("Conditional fallback: even at the end of the primary's published table (%s) you are"
                    " still inside %s's entry window, which closes at %s - plan on sitting down in progress."
                    % (clock_label(p_end), fallback["name"],
                       fallback.get("late_reg_close") or fallback["start"]))
        else:
            note = ""
        plan.append({
            "date": d,
            "events": [{"id": e["id"], "start": e["start"], "name": e["name"], "series": e["series"],
                        "venue": e["venue"], "buy_in_usd": e["buy_in_usd"], "guarantee_usd": e["guarantee_usd"],
                        "prize_text": e.get("prize_text"), "entry_status": e["entry_status"],
                        "labels": e["labels"], "late_reg_close": e.get("late_reg_close"),
                        "est_end": e.get("est_end"), "est_duration_min": e.get("est_duration_min"),
                        "est_end_next_day": bool(e.get("est_end") and e.get("est_duration_min") is not None
                                                 and abs_end_minutes(e) >= 24 * 60),
                        "duration_basis": duration_basis(e),
                        "source": e["sources"][-1]["url"]} for e in events],
            "primary_id": primary["id"] if primary else None,
            "fallback_id": fallback["id"] if fallback else None,
            "fallback_kind": fallback_kind,
            "fallback_note": note,
            "conflicts": conflicts,
            "undecidable_pairs": undecidable,
            "second_entry_id": None,
            "second_entry_note": "",
            "conflicts_unplannable": sum(1 for c in conflicts if c["kind"] == "unplannable"),
            "conflicts_join_in_progress": sum(1 for c in conflicts if c["kind"] == "join_in_progress"),
            "alternatives": alternatives,
        })
    # Self-check: the day plan must never publish the defect it exists to detect.
    for day in plan:
        by_id = {e["id"]: e for e in day["events"]}
        if day.get("fallback_id"):
            p, f = by_id[day["primary_id"]], by_id[day["fallback_id"]]
            pe = seq_end(p)
            if pe is None or pe > entry_deadline(f):
                raise SystemExit("build_schedule: %s publishes an unenterable fallback %s -> %s"
                                 % (day["date"], p["id"], f["id"]))
        for c in day["conflicts"]:
            a_end = seq_end(by_id[c["a"]])
            if c["kind"] == "join_in_progress":
                ok = a_end is not None and to_min(by_id[c["b"]]["start"]) < a_end <= entry_deadline(by_id[c["b"]])
            elif by_id[c["a"]]["start"] == by_id[c["b"]]["start"]:
                ok = True                      # same-instant pairs need no estimate
            else:
                ok = a_end is not None and a_end > entry_deadline(by_id[c["b"]])
            if not ok:
                raise SystemExit("build_schedule: %s flags a %s pair that the published tables do not "
                                 "support (%s/%s)" % (day["date"], c["kind"], c["a"], c["b"]))
    starts = sorted({r["start"] for r in rows if r["kind"] == "entry"})
    return {"verified_on": VERIFIED_ON, "days": plan,
            "earliest_listed_start": starts[0] if starts else None,
            "overlap_pairs": sum(len(day["conflicts"]) for day in plan),
            "undecidable_total": sum(len(day["undecidable_pairs"]) for day in plan),
            "conflicts_total": sum(len(day["conflicts"]) for day in plan),
            "note": "Every end time here is the end of the event's own printed level table (levels x level length "
                    "plus the published breaks), compared as minutes from the start day's midnight. It is a "
                    "MAXIMUM, not an official finish time: no sheet in the series prints an end clock, and an event "
                    "ends when its field is paid - or, for a satellite, when its seats are awarded - which can be "
                    "much earlier. Of the 93 rows the official page labels \"(1Day)\", 87 carry a table that runs past "
                    "midnight and 70 cannot fit inside a day at all (flag F75). A table spanning more than one playing day bounds its first day not at all, so "
                    "those rows carry no ceiling and their day is never paired. A day names one primary "
                    "candidate (subject to written rules) and, only where the primary cannot run past the second event's entry "
                    "deadline, a conditional fallback labelled from the start or as a join in progress. Everything "
                    "else on that date is listed as an alternative to the primary, never as an addition to it."}
# The room tax, from the taxing authority rather than from a hotel's own page.
# Every value below was read out of the Clark County Department of Business License guide on
# 2026-11-17: the rate table in Appendix III ("Resort Hotel in SD & PGC ... Combined Transient
# Lodging Tax Rate 13.38%", components 5.5 + 2 + 1 + 1 + 3 + .88, "Rates Effective 3-1-17") and
# the licensed-establishment table that follows it, which prints for each licence its number,
# DBA name, street address, status and rate. `licensed_as` is the category as printed.
# The establishment table is a snapshot ("as of April 2021"); the rate itself is fixed by
# Clark County Code 4.08.010, and the Venetian's own current terms (read 2026-11-17) still
# print 13.38%, so the operator and the county agree. Both facts are stated on the row (F77).
CLARK_COUNTY_TAX = {
    "venetian": {"licence": "1000389.RES-001",
                 "dba": "Venetian Resort Hotel Casino / Palazzo Resort Hotel Casino",
                 "address": "3325 Las Vegas Blvd S", "licensed_as": "Resort Hotel (PGC)"},
    "palazzo": {"licence": "1000389.RES-001",
                "dba": "Venetian Resort Hotel Casino / Palazzo Resort Hotel Casino",
                "address": "3325 Las Vegas Blvd S", "licensed_as": "Resort Hotel (PGC)"},
    "wynn": {"licence": "2000013.RES-001", "dba": "Wynn Las Vegas / Encore at Wynn Las Vegas",
             "address": "3131 Las Vegas Blvd S", "licensed_as": "Resort Hotel (PGC)"},
    "encore": {"licence": "2000013.RES-001", "dba": "Wynn Las Vegas / Encore at Wynn Las Vegas",
               "address": "3131 Las Vegas Blvd S", "licensed_as": "Resort Hotel (PGC)"},
    "bellagio": {"licence": "1003760.RES-001", "dba": "Bellagio",
                 "address": "3600 Las Vegas Blvd S", "licensed_as": "Resort Hotel (PGC)"},
    "aria": {"licence": "2000035.RES-001", "dba": "Aria Resort & Casino",
             "address": "3730 Las Vegas Blvd S", "licensed_as": "Resort Hotel (PGC)"},
    "caesars": {"licence": "1136233.RES-001", "dba": "Caesars Palace",
                "address": "3570 Las Vegas Blvd S", "licensed_as": "Resort Hotel (PGC)"},
}
CC_TAX_RATE = 13.38
CC_TAX_AS_OF = "the licensed-establishment table as of April 2021"
CC_TAX_LABEL = ("Clark County Department of Business License, General Information Guide for "
                "Transient Lodging Establishments (official)")


def cc_tax_note(hotel_id, extra=None):
    """The tax note printed on a hotel row, quotable line by line."""
    rec = CLARK_COUNTY_TAX[hotel_id]
    note = ("Taxing authority: licence %s, \"%s\", %s, Las Vegas NV, status Licensed, transient "
            "lodging tax rate 13.38%%, category %s (Clark County Department of Business License, "
            "General Information Guide for Transient Lodging Establishments, Appendix III and the "
            "licensed-establishment table; %s). Appendix III sets the combined rate for a Resort "
            "Hotel in the Stadium District and Primary Gaming Corridor at 13.38%% "
            "(5.5 + 2 + 1 + 1 + 3 + .88), rates effective 3-1-17."
            % (rec["licence"], rec["dba"], rec["address"], rec["licensed_as"], CC_TAX_AS_OF))
    if extra:
        note += " " + extra
    return note





# ---------------- hotels ----------------
# What was opened again on 2026-11-17, per property, so a reader can tell a re-read from a
# carry-over. A field with no entry here was not re-read on that date.
HOTEL_RECHECK = {
    "venetian": {"on": "2026-11-19", "url": "https://www.venetianlasvegas.com/legal/hotel-terms-and-conditions.html",
                 "what": "Hotel terms page and Resort Fee page both re-read live on 2026-11-19 (session cebd4457): "
                         "the $55 resort fee plus tax, the five printed fee inclusions, the 13.38% Clark County "
                         "Room Tax, the $20 / $25 / $40 parking fees, the $150 per-night incidental deposit, the "
                         "$50 additional-guest charge, the $100 plus tax early check-out charge and the prepaid "
                         "non-refundable rule are all still printed exactly as published on 2026-11-17."},
    "palazzo": {"on": "2026-11-19", "url": "https://www.venetianlasvegas.com/legal/hotel-terms-and-conditions.html",
                "what": "The same terms and resort-fee pages were re-read live on 2026-11-19; they govern The "
                        "Venetian and The Palazzo as one resort, so the Palazzo row inherits the confirmed figures."},
    "wynn": {"on": "2026-11-19", "url": "https://www.wynnlasvegas.com/about-us/parking",
             "what": "Parking page re-read live on 2026-11-19 (session cebd4457): the $25 non-registered "
                     "self-parking day (first three hours complimentary), the $40 valet day up to 24 hours and "
                     "the complimentary parking for registered Resort and Tower Suite guests (subject to "
                     "availability) are unchanged, and \"Complimentary self-parking is extended to Wynn Poker "
                     "Room guests (please visit the Poker Room for details)\" still prints."},
    "encore": {"on": "2026-11-19", "url": "https://www.wynnlasvegas.com/about-us/parking",
               "what": "The Wynn parking page (re-read live 2026-11-19) covers Wynn and Encore together "
                       "(\"one integrated resort\"), so the same statements apply here; the poker room is "
                       "inside Encore."},
    "bellagio": {"on": "2026-11-17", "url": "https://bellagio.mgmresorts.com/en/parking.html",
                 "what": "Official parking URL re-tried: the property returns its 'Oops! We can\'t find that page' "
                         "error, so there is no Bellagio parking or fee value to publish."},
    "aria": {"on": "2026-11-17", "url": "https://aria.mgmresorts.com/en/guest-services/parking.html",
             "what": "Official parking URL re-tried: the property returns its 'Oops! We can\'t find that page' "
                     "error, so there is no ARIA parking or fee value to publish."},
    "caesars": {"on": "2026-11-19", "url": "https://www.caesars.com/corporate/disclaimer",
                "what": "The corporate disclaimer was re-read live on 2026-11-19 (sessions a3822303 "
                        "and cebd4457; the daily source monitor also marked this source on its 2026-11-19 "
                        "run) and still prints only the portfolio range \"Room reservations are subject to "
                        "a daily resort fee between $45-$60 plus applicable tax\" - no Caesars "
                        "Palace-specific amount, so the fee stays blank. Correction (F87): the published "
                        "note and the 2026-11-17 research quote said $45-$50; no capture of the page ever "
                        "printed that - data/snapshots/h_caesars.txt (2026-11-16), the 2026-11-17 baseline "
                        "facts (hash-equal to the current paragraph) and the 2026-11-19 live re-read all "
                        "read $45-$60, so the earlier reading was a transcription in "
                        "research/verification-2026-11-17-structure-sheets.md, not the page's text; the "
                        "monitor's mark diffs only this source's retrieval timestamps. The parking-page "
                        "claims recorded on 2026-11-17 (parking URL redirects to Things To Do; \"FREE "
                        "48-Hour Cancellation\" headline) were not re-read on 2026-11-19."},
}

HOTELS = [
 {"id": "venetian", "name": "The Venetian Resort", "operator": "Venetian Resort (Las Vegas)",
  "venue_link": VEN, "address": "3325 Las Vegas Blvd S, Las Vegas, NV", "address_status": "verified",
  "address_note": "Clark County Department of Business License, General Information Guide for Transient Lodging "
                  "Establishments, licensed-establishment table record 1000389.RES-001: "
                  "\"Venetian Resort Hotel Casino / Palazzo Resort Hotel Casino | 3325 Las Vegas Blvd S | Las Vegas | NV "
                  "| Licensed | 13.38% | RES | 1 | Transient Lodging Tax - Resort Hotel (PGC)\" (read 2026-11-17). "
                  "The county record supplies the street address; the operator's own resort map shows the complex "
                  "between Sands Avenue and Las Vegas Blvd with the poker room on level 2 of the Grand Canal Shoppes.",
  "booking_url": SRC["venetian_book"],
  "resort_fee_usd": 55, "resort_fee_status": "verified",
  "resort_fee_note": "Official hotel terms: \"The Venetian Resort has a standard Las Vegas Resort Fee of $55 plus "
                      "applicable tax per night, payable upon check-in.\"",
  "clark_county_tax_pct": CC_TAX_RATE, "tax_status": "verified",
  "tax_note": cc_tax_note("venetian", "The operator's own current terms agree: \"Daily rates do not include the "
                                      "applicable Clark County Room Tax of 13.38%.\""),
  "room_rate_usd": None, "room_rate_status": "conditional",
  "room_rate_note": "Official poker suite page: suite rates \"will start as low as $119 and $209 and can be higher\", "
                     "conditional on qualifying poker play (6 hours of live cash play or a $300+ tournament buy-in per "
                     "night) and on availability; book by calling 866.255.8936 with code EPOKR25. The page does not say "
                     "which rate applies to which tower or date. Logged official booking-engine quote on 2026-11-17 for Nov 18-20 (2 adults): "
                     "room charges $204.25 and $524.25 a night, $55.00 resort fee each night, taxes $112.19, total $950.69 "
                     "(see data/rates.json). It is not copied into room_rate_usd because the rate changes by night.",
  "parking_note": "Official hotel terms: \"The daily fee for registered hotel guests is $20/day, seven days a week. "
                  "For non-hotel guests, the fee is $20, Monday - Thursday, and $25/day Friday - Sunday. Valet parking is "
                  "$40/day.\" Official poker page: players who play three hours or more get complimentary self-parking.",
  "parking_usd_per_day": 20,
  "parking_valet_usd": 40,
  "incidentals_usd_per_night": 150,
  "incidentals_note": "Official hotel terms (read 2026-11-17): \"A credit card incidental deposit of $150 per night "
                      "is required upon check-in for suite charging privileges for non-Signature Suites. Signature "
                      "Suite incidental deposits require a minimum of $500 for Penthouse suites or $2,500 for "
                      "Presidential suites per stay.\" Refundable and not part of the room charge, but it is money "
                      "held at check-in.",
  "extra_guest_usd_per_night": 50,
  "extra_guest_note": "Official hotel terms: \"For reservations with more than 2 guests per suite, a charge of $50 is "
                      "added to the daily rate for each additional guest 13 years of age or older.\" Every quote in "
                      "the rate log is for 2 adults, so this charge does not apply to them.",
  "early_checkout_fee_usd": 100,
  "cancellation_note": "Official hotel terms: \"A deposit for your stay, including suite, fee, and tax, will be billed "
                        "upon reservation confirmation.\" \"Check-out prior to your scheduled departure date will "
                        "result in an additional charge of $100 plus tax.\" Prepaid offers are non-cancellable and "
                        "non-refundable, and \"if you do not check-in nor notify us\ ... your entire reservation will "
                        "be canceled and your deposit for the first night's stay will not be refunded\". A fixed "
                        "free-cancellation deadline is not published for general rates.",
  "check_in_out": "Check-in 3:00 p.m. - 11:59 p.m.; check-out 11:00 a.m. (official hotel terms)",
  "walk_to_venetian_min": None,
  "walk_note": "The poker room is inside the Venetian/Palazzo complex (The Palazzo, level 2, Grand Canal Shoppes), so "
               "no street walking is needed; the published walking time for the outside legs is blank because no "
               "official source publishes it.",
  "true_cost_per_night_usd": None, "true_cost_note": "See the dated rate log; a best-available quote for one specific "
                       "stay is logged, but no published rate covers every night of a planned trip.",
  "sources": [{"label": "Hotel terms: 13.38% room tax, $55 resort fee, parking, deposit and cancellation (official)",
               "url": SRC["venetian_terms"]},
              {"label": "Poker suite rates and play requirements (official)", "url": SRC["venetian_suite_rates"]},
              {"label": "Poker room location (official)", "url": SRC["venetian_poker"]},
              {"label": "Resort map: poker room level 2 Grand Canal Shoppes (official)", "url": SRC["venetian_map"]},
              {"label": "Official booking engine (official)", "url": SRC["venetian_book"]},
              {"label": "Clark County licensing table: address and 13.38% Resort Hotel (PGC) rate class (read 2026-11-17)",
               "url": SRC["clark_county_tle_guide"]}]},
 {"id": "palazzo", "name": "The Palazzo", "operator": "Venetian Resort (Las Vegas)",
  "venue_link": VEN, "address": "3325 Las Vegas Blvd S, Las Vegas, NV", "address_status": "verified",
  "address_note": "The county licensing record 1000389.RES-001 lists the Venetian and the Palazzo under one address, "
                  "\"3325 Las Vegas Blvd S, Las Vegas, NV\" (read 2026-11-17), so the Palazzo carries that address and "
                  "the county's 13.38% resort-hotel rate. The operator's own map shows the shared complex between Sands "
                  "Avenue and Las Vegas Blvd.",
  "booking_url": SRC["venetian_book"],
  "resort_fee_usd": 55, "resort_fee_status": "verified",
  "resort_fee_note": "Official poker suite page: \"There is a $55 resort fee per night stayed\" for a suite booked at "
                      "The Venetian or The Palazzo.",
  "clark_county_tax_pct": CC_TAX_RATE, "tax_status": "verified",
  "tax_note": cc_tax_note("palazzo", "The county licence covers the Venetian and the Palazzo as one establishment, "
                                     "which is why the same licence number appears on both rows. The operator's own "
                                     "current terms, which cover \"The Venetian Resort\", also print 13.38%."),
  "room_rate_usd": None, "room_rate_status": "conditional",
  "room_rate_note": "Official poker suite page covers \"The Venetian or The Palazzo\" suites starting \"as low as $119 "
                     "and $209\", conditional on qualifying poker play and availability.",
  "parking_note": "Official Venetian Resort hotel terms (read 2026-11-17, the terms cover The Venetian and The "
                  "Palazzo as one resort): \"The daily fee for registered hotel guests is $20/day, seven days a "
                  "week\", valet is \"$40/day\", and \"Event parking rates may be in effect\". The poker room has "
                  "direct access to The Palazzo self-parking garage.",
  "parking_usd_per_day": 20,
  "parking_valet_usd": 40,
  "incidentals_usd_per_night": 150,
  "incidentals_note": "Official Venetian Resort hotel terms (read 2026-11-17): \"A credit card incidental deposit of "
                      "$150 per night is required upon check-in for suite charging privileges for non-Signature "
                      "Suites.\" Refundable, and not part of the room charge, but it is money held at check-in.",
  "extra_guest_usd_per_night": 50,
  "extra_guest_note": "Official Venetian Resort hotel terms: $50 per night for each additional guest 13 or older "
                      "beyond two guests per suite. Every quote in the rate log is for 2 adults, so it does not "
                      "apply to them.",
  "early_checkout_fee_usd": 100,
  "cancellation_note": "See the Venetian hotel terms (prepaid offers non-cancellable and non-refundable; early "
                        "check-out \"will result in an additional charge of $100 plus tax\"); no Palazzo-specific "
                        "free-cancellation deadline is published.",
  "check_in_out": "Same resort terms as The Venetian (official hotel terms).",
  "walk_to_venetian_min": None,
  "walk_note": "The poker room is at The Palazzo, level 2 of the Grand Canal Shoppes - inside the building.",
  "true_cost_per_night_usd": None, "true_cost_note": "No rate confirmed for a specific stay date set.",
  "sources": [{"label": "Poker suite rates incl. $55 resort fee (official)", "url": SRC["venetian_suite_rates"]},
              {"label": "Hotel terms incl. 13.38% room tax and $55 resort fee (official)", "url": SRC["venetian_terms"]},
              {"label": "Poker room location (official)", "url": SRC["venetian_poker"]},
              {"label": "Official booking engine (official)", "url": SRC["venetian_book"]},
              {"label": "Clark County licensing table: address and 13.38% Resort Hotel (PGC) rate class (read 2026-11-17)",
               "url": SRC["clark_county_tle_guide"]}]},
 {"id": "wynn", "name": "Wynn Las Vegas", "operator": "Wynn Resorts",
  "venue_link": WYN, "address": "3131 Las Vegas Blvd. S., Las Vegas, NV 89109", "address_status": "verified",
  "address_note": "Official Wynn Las Vegas facts page (ai-information, last updated November 2026).",
  "booking_url": "https://www.wynnlasvegas.com/rooms-and-suites",
  "resort_fee_usd": 55, "resort_fee_status": "verified",
  "resort_fee_note": "Official Wynn offer terms: \"A daily resort fee of $55 plus tax will be added to your room "
                      "account for each room night\". Official Wynn facts page repeats $55 plus tax for Resort and Tower "
                      "Suites.",
  "clark_county_tax_pct": CC_TAX_RATE, "tax_status": "verified",
  "tax_note": cc_tax_note("wynn", "No Wynn page prints a room-tax rate and the official Wynn booking "
                                  "engine renders its rate grid and tax line client-side, so the "
                                  "taxing authority is the source for this figure rather than the "
                                  "operator."),
  "room_rate_usd": None, "room_rate_status": "unverified",
  "room_rate_note": "No nightly rate is published on an official Wynn page. Use the official booking engine. "
                     "Re-checked 2026-11-17: the engine again ignored the requested date parameters (asked for "
                     "Nov 18-20; it rendered a 1-night stay of Nov 16-17) and exposes no tax or checkout total "
                     "to a text fetch, so no Wynn quote is logged. Two offer averages appeared for the rendered "
                     "stay only: $1,254 (Flexible Getaway) and $1,074 (Your Fall to Have It All) per night, each "
                     "including the resort fee and excluding taxes.",
  "parking_note": "Official Wynn parking page (read 2026-11-17): \"The daily parking fee for non-registered guests is "
                  "$25 per day with the first three (3) hours complimentary. Prices may be higher during special "
                  "events.\" and \"Complimentary self-parking is extended to Wynn Poker Room guests (please visit the "
                  "Poker Room for details), Private Access members, and Wynn Rewards members in the Chairman, Black, "
                  "and Platinum Tiers.\" Valet: \"Valet parking is $40 per day up to 24 hours (no grace period, no "
                  "re-entry).\" Registered \"Resort and Tower Suite registered guests\" park free, and the official "
                  "offer terms add complimentary self-parking for up to two vehicles. A hotel stay's parking cost is therefore $0 self-park; the $25 figure "
                  "is the non-registered-guest rate and is kept in this note so the two are never conflated.",
  "parking_usd_per_day": 0,
  "parking_valet_usd": 40,
  "parking_poker_note": "Complimentary self-parking is extended to Wynn Poker Room guests, per the official parking "
                        "page read 2026-11-17 - so a player staying at Wynn/Encore and playing at the poker room has "
                        "no published parking cost to add to the trip. Ask the Poker Room to validate the plate.",
  "cancellation_note": "Official Wynn offer terms (special offer): \"a deposit of one (1) night of room and tax for "
                        "each room booked under this offer will be charged at the time of booking and cancellations "
                        "must be received at least 48 hours prior to arrival date or deposit will be forfeited.\" "
                        "Official facts page: \"Deposit requirements, cancellation deadlines, and penalties vary by "
                        "offer and travel dates.\"",
  "check_in_out": "Check-in 3 p.m.; check-out at noon (official Wynn facts page)",
  "walk_to_venetian_min": None,
  "walk_note": "The poker room is at Encore, part of the Wynn Las Vegas resort (official WPT and daily tournament "
               "terms: \"Players will register in the Wynn Las Vegas Poker Room, located in Encore at Wynn Las Vegas\"), "
               "so the walk is inside the resort. The cross-property walk from Wynn/Encore to the Venetian is not "
               "published by any official source and is left blank.",
  "true_cost_per_night_usd": None, "true_cost_note": "No rate confirmed for a specific stay date set.",
  "sources": [{"label": "Resort fee, deposit and cancellation terms (official)", "url": SRC["wynn_terms"]},
              {"label": "Facts page: address, resort fee, parking, check-in/out (official)", "url": SRC["wynn_info"]},
              {"label": "Parking (official)", "url": SRC["wynn_parking"]},
              {"label": "Poker room and tournament schedules (official)", "url": SRC["wynn_poker"]},
              {"label": "Clark County licensing table: address and 13.38% Resort Hotel (PGC) rate class (read 2026-11-17)",
               "url": SRC["clark_county_tle_guide"]}]},
 {"id": "encore", "name": "Encore at Wynn Las Vegas", "operator": "Wynn Resorts",
  "venue_link": WYN, "address": "3131 Las Vegas Blvd. S., Las Vegas, NV 89109", "address_status": "verified",
  "address_note": "Official Wynn facts page: \"Wynn and Encore Las Vegas form one integrated resort\" at 3131 Las Vegas "
                  "Blvd. S.",
  "booking_url": "https://www.wynnlasvegas.com/rooms-and-suites",
  "resort_fee_usd": 55, "resort_fee_status": "verified",
  "resort_fee_note": "Official Wynn facts page: the $55 plus tax daily resort fee applies to Resort and Tower Suites "
                      "reservations; the official offer terms cover the Wynn/Encore resort account.",
  "clark_county_tax_pct": CC_TAX_RATE, "tax_status": "verified",
  "tax_note": cc_tax_note("encore", "The county licence covers Wynn Las Vegas and Encore as one establishment, so "
                                    "the same rate applies to both rows. No Encore-specific rate is printed on any "
                                    "operator page."),
  "room_rate_usd": None, "room_rate_status": "unverified",
  "room_rate_note": "No nightly rate published on an official Wynn page. Use the official booking engine. "
                     "Re-checked 2026-11-17: the Wynn booking engine ignores the date parameters in the URL "
                     "and exposes no tax or checkout total to a text fetch, so no Encore quote is logged.",
  "parking_note": "Official Wynn parking page (read 2026-11-17), which covers Wynn and Encore together: "
                  "\"Self-parking garages at Wynn and Encore are ... complimentary parking for all Wynn and Encore "
                  "Resort and Tower Suite registered guests, subject to availability\"; \"The daily parking fee for "
                  "non-registered guests is $25 per day with the first three (3) hours complimentary\"; valet is "
                  "\"$40 per day up to 24 hours\".",
  "parking_usd_per_day": 0,
  "parking_valet_usd": 40,
  "parking_poker_note": "The same page extends complimentary self-parking to Wynn Poker Room guests; the Wynn poker "
                        "room is inside Encore, so this is the parking that applies to the poker room's own guests.",
  "cancellation_note": "Official Wynn facts page: deposit and cancellation terms vary by offer and dates.",
  "check_in_out": "Check-in 3 p.m.; check-out at noon (official Wynn facts page)",
  "walk_to_venetian_min": None,
  "walk_note": "The Wynn Las Vegas poker room is located in Encore - the walk is inside the resort.",
  "true_cost_per_night_usd": None, "true_cost_note": "No rate confirmed for a specific stay date set.",
  "sources": [{"label": "Facts page: address, resort fee, parking (official)", "url": SRC["wynn_info"]},
              {"label": "Resort fee and cancellation terms (official)", "url": SRC["wynn_terms"]},
              {"label": "Poker room location (official)", "url": SRC["wpt_struct"]},
              {"label": "Clark County licensing table: address and 13.38% Resort Hotel (PGC) rate class (read 2026-11-17)",
               "url": SRC["clark_county_tle_guide"]}]},
 {"id": "bellagio", "name": "Bellagio", "operator": "MGM Resorts International",
  "venue_link": None, "address": "3600 Las Vegas Blvd S, Las Vegas, NV", "address_status": "verified",
  "address_note": "Clark County Department of Business License licensing record 1003760.RES-001: \"Bellagio | 3600 "
                  "Las Vegas Blvd S | Las Vegas | NV | Licensed\" (read 2026-11-17). A county licensing address, not a "
                  "statement on the property's own page - the Bellagio page text returned in this session does not print "
                  "one.",
  "booking_url": "https://bellagio.mgmresorts.com/book-room/",
  "resort_fee_usd": 55, "resort_fee_status": "verified",
  "resort_fee_note": "Official Bellagio Hotel Reservation Terms and Conditions: \"Daily Resort Fee. A daily resort fee "
                     "of $55.00 plus applicable tax will be applied to all reservations.\" The same page lists what "
                     "the fee covers and states the fee is waived for MGM Rewards Gold+ members on eligible "
                     "reservations. Read 2026-11-17.",
  "clark_county_tax_pct": CC_TAX_RATE, "tax_status": "verified",
  "tax_note": cc_tax_note("bellagio", "This replaces an earlier estimate. The Bellagio terms state the "
                                      "rule but print no percentage: \"Lodging taxes apply to the basic "
                                      "room rate, any resort fee, additional per occupant charges, "
                                      "upgrades, as well as any other charges as required by applicable "
                                      "law.\""),
  "room_rate_usd": None, "room_rate_status": "unverified",
  "room_rate_note": "No nightly rate published on an official page read in this session.",
  "parking_note": "Official MGM Resorts parking page: self-parking for a registered hotel guest is $20 per 24 hours "
                  "on weekdays and $20 at weekends; valet is $40 per day. Nevada residents get the first 3 hours of "
                  "self-parking free outside special events.",
  "parking_usd_per_day": 20,
  "cancellation_note": "Official Bellagio terms: \"The first night's deposit is fully refundable provided a timely "
                       "notice of cancellation is received by Room Reservations ... at least 72 hours prior to the "
                       "arrival date, unless specifically excluded by booked offer.\"",
  "check_in_out": "Check-in 3:00 p.m.; check-out 11:00 a.m. (official Bellagio FAQ and terms)",
  "walk_to_venetian_min": None,
  "walk_note": "Walking time from Bellagio to the Venetian poker room is not published by any official source; "
               "left blank and flagged.",
  "true_cost_per_night_usd": None, "true_cost_note": "Resort fee, parking and the 13.38% county room-tax rate are "
                       "verified, but no dated room rate is verified for a planned stay, so no true cost is calculated.",
  "sources": [{"label": "Bellagio hotel reservation terms: $55 daily resort fee, tax rule, 72-hour cancellation (official)",
               "url": SRC["bellagio_terms"]},
              {"label": "Bellagio FAQ: check-in and check-out times (official)", "url": SRC["bellagio_faq"]},
              {"label": "MGM Resorts parking rates: self-parking $20 (official)", "url": SRC["mgm_parking"]},
              {"label": "Bellagio official home page (official)", "url": SRC["bellagio"]},
              {"label": "Bellagio poker room page: tables, phone, weekly tournament flyers (official)", "url": SRC["bellagio_poker"]},
              {"label": "Clark County licensing table: licensed address and 13.38% Resort Hotel (PGC) rate class (read 2026-11-17)",
               "url": SRC["clark_county_tle_guide"]}]},
 {"id": "aria", "name": "ARIA Resort & Casino", "operator": "MGM Resorts International",
  "venue_link": None, "address": "3730 Las Vegas Blvd S, Las Vegas, NV", "address_status": "verified",
  "address_note": "Clark County licensing record 2000035.RES-001: \"Aria Resort & Casino | 3730 Las Vegas Blvd S | "
                  "Las Vegas | NV | Licensed\" (read 2026-11-17). A county licensing address; the official ARIA pages "
                  "read in this session print none.",
  "booking_url": "https://aria.mgmresorts.com/book-room/",
  "resort_fee_usd": 55, "resort_fee_status": "verified",
  "resort_fee_note": "Official ARIA Hotel Reservation Terms and Conditions: \"Daily Resort Fee. A daily resort fee "
                     "of $55.00 plus applicable tax will be applied to all reservations.\" Waived for MGM Rewards "
                     "Gold+ members on eligible reservations. Read 2026-11-17.",
  "clark_county_tax_pct": CC_TAX_RATE, "tax_status": "verified",
  "tax_note": cc_tax_note("aria", "This replaces an earlier estimate. The ARIA terms state the rule but "
                                  "print no percentage: \"Estimated taxes are based on current tax rates "
                                  "which are subject to change ... Lodging taxes apply to the basic room "
                                  "rate, any resort fee, additional per occupant charges and upgrades.\""),
  "room_rate_usd": None, "room_rate_status": "unverified",
  "room_rate_note": "Official ARIA poker page: \"Exclusive Room Rates for qualifying poker players\" - the rate itself "
                     "is only available by phone (702.590.7232) or by e-mail, so no number is published.",
  "parking_note": "Official MGM Resorts parking page lists ARIA with the same rates as Bellagio: self-parking $20 "
                  "per 24 hours for a registered hotel guest, valet $40 per day.",
  "parking_usd_per_day": 20,
  "cancellation_note": "Official ARIA terms: the first night's deposit is fully refundable if cancellation notice is "
                       "received at least 72 hours prior to arrival, unless excluded by the booked offer.",
  "check_in_out": "Check-in 3:00 p.m.; check-out 11:00 a.m. (official ARIA terms)",
  "walk_to_venetian_min": None,
  "walk_note": "Walking time from ARIA to the Venetian poker room is not published by any official source; left blank "
               "and flagged. ARIA does run a poker room (official ARIA poker page).",
  "true_cost_per_night_usd": None, "true_cost_note": "Resort fee, parking and the 13.38% county room-tax rate are "
                       "verified, but no dated room rate is verified for a planned stay, so no true cost is calculated.",
  "sources": [{"label": "ARIA hotel reservation terms: $55 daily resort fee, tax rule, 72-hour cancellation (official)",
               "url": SRC["aria_terms"]},
              {"label": "MGM Resorts parking rates: self-parking $20 (official)", "url": SRC["mgm_parking"]},
              {"label": "ARIA official home page (official)", "url": SRC["aria"]},
              {"label": "ARIA poker room and player rates (official)", "url": SRC["aria_poker"]},
              {"label": "Clark County licensing table: licensed address and 13.38% Resort Hotel (PGC) rate class (read 2026-11-17)",
               "url": SRC["clark_county_tle_guide"]}]},
 {"id": "caesars", "name": "Caesars Palace", "operator": "Caesars Entertainment",
  "venue_link": None, "address": "3570 Las Vegas Blvd South, Las Vegas, NV 89109", "address_status": "verified",
  "address_note": "Official Caesars Palace property page footer: \"3570 Las Vegas Blvd South, Las Vegas, NV 89109\". "
                  "The Clark County licensing record 1136233.RES-001 lists the same street address for Caesars Palace "
                  "(\"3570 Las Vegas Blvd S\"), so the operator and the county agree (county record read 2026-11-17).",
  "booking_url": "https://www.caesars.com/book/hotel-calendar?propCode=CLV",
  "resort_fee_usd": None, "resort_fee_status": "unverified",
  "resort_fee_note": "Read 2026-11-19 (live re-read of the cited pages, sessions a3822303 and "
                     "cebd4457): the Caesars Palace property pages and the Caesars Palace FAQ do not "
                     "print a resort-fee amount for this property. The Caesars corporate disclaimer "
                     "states only that \"Room reservations are subject to a daily resort fee between "
                     "$45-$60 plus applicable tax\" across the Caesars portfolio, which does not name "
                     "Caesars Palace, so it is not used as this property's fee. Correction (F87): the "
                     "2026-11-17 note quoted the range as $45-$50; no archived capture of the page "
                     "prints that - data/snapshots/h_caesars.txt (2026-11-16), the 2026-11-17 baseline "
                     "facts (captured 2026-11-17T00:43:10Z, hash-equal to the current paragraph) and the "
                     "2026-11-19 live re-read all read $45-$60, so both readings stay dated in "
                     "research/verification-2026-11-19-a3822303.md section D without claiming the page "
                     "moved. The daily monitor marked this source on 2026-11-19 (data/changes.json); "
                     "its diff carries only the retrieval-timestamp list, not a value. The property's "
                     "own fee stays blank either way.",
  "clark_county_tax_pct": CC_TAX_RATE, "tax_status": "verified",
  "tax_note": cc_tax_note("caesars", "No Caesars page read prints a room-tax percentage; the taxing authority is the "
                                     "source. The resort fee for this property is still unverified (blank)."),
  "room_rate_usd": None, "room_rate_status": "unverified",
  "room_rate_note": "No nightly rate published on an official page read in this session.",
  "parking_note": "No Caesars Palace parking fee printed on an official page read in this session.",
  "parking_usd_per_day": None,
  "cancellation_note": "Official Caesars Palace FAQ (Policies & Guidelines, read 2026-11-17): \"For most hotel "
                        "reservations made directly with Caesars Palace, cancellations are generally allowed up to "
                        "48 hours prior to the scheduled arrival date. Policies may differ for certain rates, "
                        "special offers, or packages.\" The property page also advertises \"FREE 48-Hour Cancellation\" "
                        "on best-rate bookings.",
  "check_in_out": "Check-in 4:00 p.m.; check-out 11:00 a.m. (official Caesars Palace FAQ, read 2026-11-17: "
                  "\"Check-in at Caesars Palace begins at 4:00 PM, and check-out is at 11:00 AM.\")",
  "walk_to_venetian_min": None,
  "walk_note": "Walking time from Caesars Palace to the Venetian poker room is not published by any official source; "
               "left blank and flagged.",
  "true_cost_per_night_usd": None, "true_cost_note": "No dated rate and no property-specific resort fee are "
                       "verified; the 13.38% county room-tax rate is verified but a rate and a fee are both needed "
                       "before a true cost is calculated.",
  "sources": [{"label": "Caesars Palace FAQ: check-in/out times and 48-hour cancellation (official)",
               "url": SRC["caesars_faq"]},
              {"label": "Caesars corporate disclaimer: portfolio-wide $45-$60 resort-fee range (re-read 2026-11-19; F87 corrects the earlier $45-$50 research quote), not property-specific (official)",
               "url": SRC["caesars_disclaimer"]},
              {"label": "Caesars Palace official page incl. address (official)", "url": SRC["caesars"]},
              {"label": "Caesars Palace poker page: 24/7 room and the daily tournament schedule link (official)", "url": SRC["caesars_poker_page"]},
              {"label": "Clark County licensing table: licensed address and 13.38% Resort Hotel (PGC) rate class (read 2026-11-17)",
               "url": SRC["clark_county_tle_guide"]}]},
]

# ---------------- dated rate log ----------------
def rate_entry(prop, room, offer, arrival, departure, nightly, fee, taxes, total, source, hotel_id,
               retrieved="2026-11-17", logged="2026-11-17", occupancy="2 adults",
               cancel=None, extra=None, retrieved_at=None):
    """One dated rate-log row. True cost per night is the engine's own checkout total divided by nights."""
    nights = len(nightly)
    # The engine's printed "Average Rate" is (room charges + resort fee) / nights; store that same convention
    # so every row in the log means the same thing, and keep the room-only figure beside it.
    room_only = round(sum(nightly) / nights, 2)
    avg = round((sum(nightly) + fee * nights) / nights, 2)
    entry = {
        "logged_on": logged, "property": prop, "hotel_id": hotel_id, "room": room, "offer": offer,
        "arrival": arrival, "departure": departure, "nights": nights, "occupancy": occupancy,
        "nightly_rates_usd": [round(n, 2) for n in nightly],
        "nightly_average_usd": avg,
        "nightly_average_includes_resort_fee": True,
        "room_only_average_usd": room_only,
        "resort_fee_per_night_usd": fee,
        "taxes_total_usd": taxes, "checkout_total_usd": total,
        "true_cost_per_night_usd": round(total / nights, 2),
        "true_cost_method": "checkout total (room + resort fee + taxes) / %d nights" % nights,
        "caveat": "Best-available quote for these exact dates and occupancy at the time of retrieval. Rates move "
                  "with availability; re-check the official booking engine before paying. nightly_average_usd "
                  "reproduces the engine's own printed Average Rate: (room charges + resort fee) / nights, before "
                  "tax. The per-night room figures exclude the resort fee and tax, which are shown separately.",
        "source": source, "retrieved_on": retrieved, "logged_on_date": logged,
        # The brief asks for a rate timestamp. The engines print no time stamp on the
        # quote itself, so what can be published is the date the engine was read and,
        # where the fetch log recorded it, the time - stated as such rather than guessed.
        "timestamp_basis": "The booking engine prints no time stamp on the quote. "
                           "retrieved_on is the date the engine was read; retrieved_at_utc, where "
                           "present, is the moment the fetch was made, from that session's log.",
    }
    if retrieved_at:
        entry["retrieved_at_utc"] = retrieved_at
    if cancel:
        entry["cancellation_note"] = cancel
    if extra:
        entry.update(extra)
    return entry

RATES = [
 # ---- The Venetian Resort (official booking engine; each quote read on 2026-11-17) ----
 rate_entry("The Venetian Resort", "Palazzo Luxury King",
            "Book Direct: Up to 25% Off (best available rate shown by the official booking engine)",
            "2026-11-26", "2026-11-29", [261.75, 1274.25, 426.75], 55.00, 284.69, 2412.44,
            SRC["venetian_book"], hotel_id="venetian", retrieved="2026-11-16", logged="2026-11-16",
            cancel="Prepaid offers are non-cancellable and non-refundable; the official hotel terms print no fixed "
                   "free-cancellation deadline for a general (non-prepaid) rate."),
 rate_entry("The Venetian Resort", "Venetian Newly Remodeled Luxury King",
            "Book Direct: Up to 25% Off (best available rate shown by the official booking engine)",
            "2026-12-13", "2026-12-20",
            [254.25, 164.25, 164.25, 164.25, 164.25, 269.25, 524.25], 55.00, 279.63, 2369.38,
            SRC["venetian_book"], hotel_id="venetian",
            cancel="Official hotel terms: check-in 3:00-11:59 p.m., check-out 11:00 a.m.; prepaid offers are "
                   "non-cancellable. No fixed free-cancellation deadline is printed for a general rate.",
            extra={"trip_window": "Venetian DeepStack Extravaganza IV finale (Dec 13-23)",
                   "engine_quote": "Average Rate $298.54; Taxes $279.63; Total $2,369.38 for 7 nights"}),
 rate_entry("The Venetian Resort", "Venetian Newly Remodeled Luxury King",
            "Book Direct: Up to 25% Off (best available rate shown by the official booking engine)",
            "2027-01-01", "2027-01-06", [1949.25, 449.25, 164.25, 389.25, 794.25], 55.00, 538.05, 4559.30,
            SRC["venetian_book"], hotel_id="venetian",
            cancel="Official hotel terms: prepaid offers are non-cancellable and non-refundable; no fixed "
                   "free-cancellation deadline is printed for a general rate.",
            extra={"trip_window": "Venetian DeepStack Extravaganza NYE / MSPT $400K (Jan 1-10)",
                   "engine_quote": "Average Rate $804.25; Taxes $538.05; Total $4,559.30 for 5 nights"}),
 rate_entry("The Venetian Resort", "Palazzo Luxury Two Queen",
            "Book Direct: Up to 25% Off (best available rate shown by the official booking engine)",
            "2027-01-10", "2027-01-15", [164.25, 254.25, 239.25, 239.25, 239.25], 55.00, 188.83, 1600.08,
            SRC["venetian_book"], hotel_id="palazzo",
            cancel="Official hotel terms: prepaid offers are non-cancellable and non-refundable; no fixed "
                   "free-cancellation deadline is printed for a general rate.",
            extra={"trip_window": "Venetian NYE finale (Jan 10) and Wynn Signature Series opening (Jan 11)",
                   "engine_quote": "Average Rate $282.25; Taxes $188.83; Total $1,600.08 for 5 nights"}),

 # Same stay read by the parallel session on 2026-11-17 (Nov 18-20, Venetian tower); kept because it is a distinct
 # dated quote, not a duplicate.
 rate_entry("The Venetian Resort", "Venetian Newly Remodeled Luxury Two Queen (best available rate & suite)",
            "Book Direct: Up to 25% Off (offer shown on the official booking page)",
            "2026-11-18", "2026-11-20", [204.25, 524.25], 55.00, 112.19, 950.69,
            SRC["venetian_quote_1118"], hotel_id="venetian", retrieved="2026-11-17", logged="2026-11-17",
            retrieved_at="2026-11-17T00:35Z (approximate: the time the fetch was made, from that "
                         "session's log - the engine itself prints no time stamp)",
            cancel="Official hotel terms: prepaid offers are non-cancellable and non-refundable; no fixed "
                   "free-cancellation deadline is printed for a general rate.",
            extra={"engine_quote": "Average Rate $419.25; Taxes $112.19; Total $950.69 for 2 nights",
                   "note": "Read by the parallel session on 2026-11-17. Arithmetic checked in this build: "
                           "204.25 + 524.25 + 2 x 55 = 838.50, and 13.38% of 838.50 = 112.19."}),
]

# ---------------- walking routes (hotel <-> venue) ----------------
OSM_ROUTE = ("https://routing.openstreetmap.de/routed-foot/route/v1/foot/"
             "%s%%3B%s?overview=false")
OSM_POINTS = (
    "https://routing.openstreetmap.de/routed-foot/table/v1/foot/"
    "-115.1693352,36.1217073%3B-115.1682710,36.1241843%3B-115.1654043,36.1266219%3B"
    "-115.1653620,36.1289345%3B-115.1770065,36.1131149%3B-115.1779977,36.1070287%3B"
    "-115.1767568,36.1166277%3B-115.1682710,36.1241843%3B-115.1653620,36.1289345"
    "?sources=0%3B1%3B2%3B3%3B4%3B5%3B6&destinations=7%3B8&annotations=duration%2Cdistance"
)
# Coordinates read from the OpenStreetMap Nominatim lookup on 2026-11-17 (JSON response quoted below).
OSM_LOOKUP = {
 "venetian": {"q": "Venetian Hotel Las Vegas", "lat": 36.1217073, "lon": -115.1693352,
              "osm": "relation/7770314"}, 
 "palazzo": {"q": "The Palazzo Las Vegas", "lat": 36.1241843, "lon": -115.1682710,
             "osm": "way/180584269"},
 "wynn": {"q": "Wynn Las Vegas", "lat": 36.1266219, "lon": -115.1654043, "osm": "way/205501268"},
 "encore": {"q": "Encore at Wynn Las Vegas", "lat": 36.1289345, "lon": -115.1653620,
            "osm": "node/367054910"},
 "bellagio": {"q": "Bellagio Las Vegas", "lat": 36.1131149, "lon": -115.1770065,
              "osm": "way/25723909"},
 "aria": {"q": "ARIA Resort & Casino Las Vegas", "lat": 36.1070287, "lon": -115.1779977,
          "osm": "way/52175576"},
 "caesars": {"q": "Caesars Palace Las Vegas", "lat": 36.1166277, "lon": -115.1767568,
             "osm": "way/115672893"},
}
# Poker-room destinations: the Venetian poker room is inside The Palazzo (official poker page),
# the Wynn poker room is inside Encore (official tournament terms).
ROOM_POINT = {
 VEN: {"label": "The Palazzo (poker room, level 2 Grand Canal Shoppes)", "lat": 36.1241843,
       "lon": -115.1682710, "basis": "official poker page: \"Our Poker Room is located at The Palazzo "
       "on level 2 of Grand Canal Shoppes\"; coordinate from the Nominatim lookup for The Palazzo"},
 WYN: {"label": "Encore at Wynn Las Vegas (poker room)", "lat": 36.1289345, "lon": -115.1653620,
       "basis": "official tournament terms: \"Players will register in the Wynn Las Vegas Poker Room, "
       "located in Encore at Wynn Las Vegas\"; coordinate from the Nominatim lookup for Encore"},
}
# Seconds of walking produced by the OSM foot router (table service) on 2026-11-17, one row per source.
# Seconds and metres from the OSM foot router, origin = the property, destination = THE RESORT THAT CONTAINS
# THE POKER ROOM: The Palazzo for the Venetian poker room, Encore for the Wynn poker room.
OSM_MATRIX = {
 "venetian": {VEN: (359.2, 449.1), WYN: (919.4, 1146.8)},
 "palazzo": {VEN: (0.0, 0.0), WYN: (799.0, 996.2)},
 "wynn": {VEN: (894.1, 1115.2), WYN: (95.1, 119.1)},
 "encore": {VEN: (799.0, 996.2), WYN: (0.0, 0.0)},
 "bellagio": {VEN: (1284.9, 1606.4), WYN: (1845.1, 2304.0)},
 "aria": {VEN: (2012.0, 2510.6), WYN: (2572.2, 3208.3)},
 "caesars": {VEN: (1348.1, 1684.9), WYN: (1908.3, 2382.5)},
}
INTERNAL_NOTE = {
 ("venetian", VEN): "The poker room is inside the Venetian/Palazzo complex; the route is interior "
                    "(casino floor and Grand Canal Shoppes), so no street crossing is involved.",
 ("palazzo", VEN): "The poker room is in The Palazzo itself, so the walk is interior.",
 ("wynn", WYN): "The poker room is in Encore at Wynn Las Vegas; the walk is interior through the resort.",
 ("encore", WYN): "The poker room is in Encore, so the walk is interior.",
}
OFFICIAL_INTERIOR = {
 ("venetian", VEN): "\"From The Venetian Lobby: Proceed across The Venetian casino floor ... Take the "
                    "escalator up to level 2, Grand Canal Shoppes ... The Poker Room will be on your right.\"",
 ("palazzo", VEN): "\"From The Palazzo Lobby: Proceed across The Palazzo Casino Floor ... The Poker Room "
                   "will be straight ahead.\"",
 ("wynn", WYN): "\"Players will register in the Wynn Las Vegas Poker Room, located in Encore at Wynn "
                "Las Vegas.\"",
 ("encore", WYN): "\"Players will register in the Wynn Las Vegas Poker Room, located in Encore at Wynn "
                  "Las Vegas.\"",
}
# Cross-check links for the same coordinate pair, so the routed time can be re-checked in the app a
# traveller would actually use. Directions URLs built only from the coordinates already recorded above;
# the traveller's own current location is never assumed.
GMAPS = "https://www.google.com/maps/dir/?api=1&origin=%s,%s&destination=%s,%s&travelmode=walking"
AMAPS = "https://maps.apple.com/?saddr=%s,%s&daddr=%s,%s&dirflg=w"
# The walking table is read by a traveller, so it prints the property name and the
# name of the building the poker room is actually in, not the internal slug.
HOTEL_NAME = {h["id"]: h["name"] for h in HOTELS}
WALKING = []
for hotel_id, points in OSM_LOOKUP.items():
    for venue in (VEN, WYN):
        secs, metres = OSM_MATRIX[hotel_id][venue]
        origin = ROOM_POINT[venue]
        internal = (hotel_id, venue) in INTERNAL_NOTE
        if internal:
            minutes = None
            status = "internal"
            note = INTERNAL_NOTE[(hotel_id, venue)] + " No street route is needed, so no street walking " \
                   "time is stated; the router returns 0 minutes because the two points are inside one complex."
        else:
            minutes = int(math.ceil(secs / 60.0 - 0.02))  # round up; the 0.02 tolerates router jitter
            status = "verified"
            note = ("OpenStreetMap foot router: %d seconds (%d m) from %s to %s - the building the %s poker "
                    "room is in - rounded up to %d minutes. This is a published routing source, not the hotel "
                    "or the poker room itself, so the 30-minute rule is applied to the routed time." % (
                        round(secs), round(metres), HOTEL_NAME[hotel_id], origin["label"], venue, minutes))
        WALKING.append({
            "hotel": hotel_id, "hotel_name": HOTEL_NAME[hotel_id], "venue": venue,
            "destination": origin["label"],
            "from": "%s (%s, OSM %s)" % (HOTEL_NAME[hotel_id], OSM_LOOKUP[hotel_id]["q"],
                                         OSM_LOOKUP[hotel_id]["osm"]),
            "to": origin["label"],
            "metres": metres if not internal else 0,
            "minutes": minutes,
            "status": status,
            "within_30_min": (minutes is None) or (minutes <= 30),
            "note": note,
            "official_fact": OFFICIAL_INTERIOR.get((hotel_id, venue)),
            "route_link": OSM_ROUTE % ("%s,%s" % (OSM_LOOKUP[hotel_id]["lon"], OSM_LOOKUP[hotel_id]["lat"]),
                                        "%s,%s" % (origin["lon"], origin["lat"])),
            "retrieved_on": "2026-11-17",
            "cross_check": [
                {"label": "Google Maps walking directions between the same two coordinates",
                 "url": GMAPS % (OSM_LOOKUP[hotel_id]["lat"], OSM_LOOKUP[hotel_id]["lon"],
                                 origin["lat"], origin["lon"])},
                {"label": "Apple Maps walking directions between the same two coordinates",
                 "url": AMAPS % (OSM_LOOKUP[hotel_id]["lat"], OSM_LOOKUP[hotel_id]["lon"],
                                 origin["lat"], origin["lon"])},
            ],
            "sources": [
                {"label": "Nominatim lookup for the %s coordinate" % HOTEL_NAME[hotel_id],
                 "url": "https://nominatim.openstreetmap.org/search?q="
                        + OSM_LOOKUP[hotel_id]["q"].replace(" ", "+") + "&format=json&limit=1"},
                {"label": "Foot-routing query for this pair",
                 "url": OSM_ROUTE % ("%s,%s" % (OSM_LOOKUP[hotel_id]["lon"], OSM_LOOKUP[hotel_id]["lat"]),
                                     "%s,%s" % (origin["lon"], origin["lat"]))},
            ],
        })

# ---------------- venues ----------------
VENUES = [
 {"id": "venetian", "name": "The Venetian Resort", "poker_room": "The Palazzo, level 2, Grand Canal Shoppes",
  "address": "3325 Las Vegas Blvd S, Las Vegas, NV", "address_status": "verified",
  "note": "Official poker page (re-read 2026-11-17): the room is at The Palazzo, level 2 of the Grand Canal Shoppes; "
          "\"50 tables spread across 14,000 square feet ... the largest room on the Las Vegas Strip\"; open 24 hours "
          "daily; complimentary self-parking for guests who play three hours or more. The page's Current Series card "
          "still advertises the WPT Fall Festival of Oct 28 - Nov 15, 2026 (a stale promo on 2026-11-17, flagged F78). "
          "Street address from the Clark County licensing record 1000389.RES-001.",
  "hotel_ids": ["venetian", "palazzo"],
  "official_links": [SRC["venetian_poker"], SRC["venetian_map"], SRC["venetian_book"],
                     SRC["clark_county_tle_guide"], SRC["dse_nov_page"], SRC["dse_dec_page"]]},
 {"id": "wynn", "name": "Wynn Las Vegas", "poker_room": "Wynn Las Vegas poker room, located in Encore at Wynn Las Vegas",
  "address": "3131 Las Vegas Blvd. S., Las Vegas, NV 89109", "address_status": "verified",
  "note": "Official tournament terms place the poker room in Encore. The official poker page links the WPT, Wynn "
          "Signature Series and daily tournament schedules, structures and results. Registration opening time: "
          "the official Wynn daily tournament terms and conditions state \"Registration for each Event will open "
          "four (4) hours prior to the scheduled start of play\", so a 12 p.m. daily event opens registration at "
          "8 a.m. That opening time is printed only in the Wynn daily tournament terms; the WPT and Signature "
          "Series schedule PDFs print a registration CLOSE time per event but no opening time.",
  "hotel_ids": ["wynn", "encore"],
  "official_links": [SRC["wynn_poker"], SRC["wpt_sched"], SRC["wpt_struct"], SRC["wss_sched"], SRC["wynn_daily_poster"]]},
 {"id": "aria", "name": "ARIA Resort & Casino", "poker_room": "ARIA poker room, east side of the casino floor next to main valet pick-up",
  "address": None, "address_status": "unverified",
  "note": "Official ARIA poker page (read 2026-11-17): 24 tables and exclusive room rates for qualifying poker players, "
          "by phone 702.590.7232 or e-mail PokerRoomRates@aria.com. The page says the Daily Tournaments run \"as scheduled\" "
          "but publishes no schedule, buy-in or structure, and tells guests to call the room or follow @ARIAPoker. "
          "No ARIA tournament row is listed because no official schedule or structure sheet was read.",
  "hotel_ids": ["aria"], "official_links": [SRC["aria_poker"], SRC["aria"]]},
 {"id": "bellagio", "name": "Bellagio", "poker_room": "Bellagio poker room, northside of the casino next to the Sportsbook (official poker page)",
  "address": None, "address_status": "unverified",
  "note": "Official Bellagio poker page (read 2026-11-17) links three weekly tournament flyers. None prints a calendar date, so "
          "no dated row is listed. Friday $600 NLH, 11:00 a.m.: $510 prize pool, $50 house fee, $40 optional staff gratuity; "
          "rule 3 says players \"may buy-in and re-enter through the end of level 8\", so it is a re-entry event and not single "
          "entry. Saturday, 11:00 a.m.: the flyer heading says a $1,100 buy-in, the page label and file name say $1,000, and "
          "rule 7 refers to a \"$600 Buy-in\"; flight rules say each flight plays until the money. Its entry rule is not "
          "confirmed. Sunday $400 H.O.R.S.E., 11:00 a.m.: $340 prize pool, $35 house fee, $25 optional gratuity; rule 5 says "
          "\"buy-in and re-enter through the end of level 8\", so it is not single entry. The page notice \"Tournament play will "
          "resume on Saturday, July 26\" does not match the calendar: July 26, 2026 is a Sunday. On 2026-11-17 all three "
          "structure PDFs were read in full, so each format is published as an undated weekly row in the daily feed with "
          "its printed clauses quoted: Friday $600 (re-entry through level 8; $510/$50/$40 split), Saturday (four "
          "flights 1A-1D, a combined Day 2, \"at least $50,000\" combined prize pool, and three conflicting printed "
          "buy-ins of $1,100 / $1,000 / $600, so no entry fee is published) and Sunday $400 H.O.R.S.E. (re-entry through "
          "level 8; $340/$35/$25 split; payout about 12.5% of the field). None of the three is single entry, so none is "
          "ranked. The flyers are MGM's own asset host, linked from this page.",
  "hotel_ids": ["bellagio"],
  "official_links": [SRC["bellagio_poker"], SRC["bellagio"], SRC["bellagio_fri_pdf"], SRC["bellagio_sat_pdf"],
                     SRC["bellagio_sun_pdf"]]},
 {"id": "caesars", "name": "Caesars Palace", "poker_room": "The Poker Room at Caesars Palace, Appian Way promenade (16 tables per official article)",
  "address": "3570 Las Vegas Blvd South, Las Vegas, NV 89109",
  "address_status": "verified",
  "note": "Caesars Palace publishes its own daily tournament schedule: the official casino page carries a "
          "\"View Schedule\" link to the 2026 Daily No-Limit Texas Hold'em schedule PDF, read in full on 2026-11-17. It "
          "prints four starts (10 a.m. $100, 2 p.m. $160, 6 p.m. $100, 9 p.m. $160), each with a $1,000 guarantee, 20,000 "
          "starting chips, 20-minute levels and an optional $50 add-on at the first break; registration closes at the start "
          "of level seven and sign-ups open one hour before the scheduled start. Rule 3: \"Participants may only register "
          "themselves, but may re-enter, by paying the entry fee, upon elimination within the first break of play\" - so "
          "every Caesars daily is a re-entry plus add-on format and none is single entry. The room is \"open 24/7 with "
          "both live-action cash games and daily tournaments\" (official casino page). The four formats are published as "
          "undated rows in the daily feed, not as dated schedule rows, because the flyer prints no dates.",
  "hotel_ids": ["caesars"],
  "official_links": [SRC["caesars"], SRC["caesars_poker_article"], SRC["caesars_poker_page"],
                     SRC["caesars_daily_flyer"]]},
]


def true_cost(h):
    """True nightly cost. No published nightly rate exists for either property, so the value is taken from the
    dated rate log (the official booking engine's own checkout total / nights) and never from an inferred rate."""
    # A quote counts for a property only when it is that property's own rate: the booking engines name the room
    # type, so the Venetian's Palazzo rooms are The Palazzo's quotes and its Venetian rooms are The Venetian's.
    quotes = [r for r in RATES if r.get("hotel_id") == h["id"]]
    if not quotes:
        return None, None
    latest = max(quotes, key=lambda r: (r["arrival"], r["retrieved_on"]))
    return latest["true_cost_per_night_usd"], latest


def main():
    rows = []
    rows += build_venetian(DSE_NOV, "nov", "Venetian DeepStack Extravaganza IV", "dse_nov_page",
                           NOV_SHEETS, "dse_nov_sched", "dse_nov_struct")
    rows += build_venetian(DSE_NYE, "dec", "Venetian DeepStack Extravaganza NYE", "dse_dec_page",
                           DEC_SHEETS, "dse_dec_sched", "dse_dec_struct")
    rows += build_wynn()
    mark_flight_pricing(rows)  # P3 descriptive flag; never changes entry_status
    rows.sort(key=lambda x: (x["date"], x["start"], x["name"]))
    for i, row in enumerate(rows, 1):
        row["id"] = "r%03d" % i

    # The spend-advantage reading every table prints next to the entry rule. Derived
    # from the clause excerpt already stored on the row - no new fact, and it never
    # moves an entry_status. scripts/spend_advantage.py; re-checked on every build by
    # scripts/check_links.py.
    import spend_advantage
    for row in rows:
        row["spend_advantage"] = spend_advantage.classify(row)

    with open(os.path.join(DATA, "tournaments.json"), "w") as f:
        json.dump({"verified_on": VERIFIED_ON, "rows": rows, "sources": SRC}, f, indent=1)

    with open(os.path.join(DATA, "schedule.json"), "w") as f:
        json.dump(build_schedule(rows), f, indent=1)

    hotels = []
    walk_by_key = {(w["hotel"], w["venue"]): w for w in WALKING}
    for h in HOTELS:
        h = dict(h)
        # The room tax on every row now cites the taxing authority, so that source is
        # listed on the row next to the operator's own pages.
        h["sources"] = list(h.get("sources") or []) + [
            {"label": CC_TAX_LABEL, "url": SRC["clark_county_tle_guide"]}]
        h["tax_licence"] = CLARK_COUNTY_TAX[h["id"]]["licence"]
        h["tax_licensed_as"] = CLARK_COUNTY_TAX[h["id"]]["licensed_as"]
        h["tax_source_url"] = SRC["clark_county_tle_guide"]
        cost, quote = true_cost(h)
        h["true_cost_per_night_usd"] = cost
        if quote:
            h["true_cost_note"] = ("Taken from the official booking engine quote in data/rates.json: %s to %s, "
                                   "%d nights, checkout total $%s, i.e. $%s per night after room, resort fee and tax."
                                   % (quote["arrival"], quote["departure"], quote["nights"],
                                      format(quote["checkout_total_usd"], ",.2f"),
                                      format(quote["true_cost_per_night_usd"], ",.2f")))
            h["true_cost_quote"] = {"arrival": quote["arrival"], "departure": quote["departure"],
                                    "nights": quote["nights"], "room": quote["room"],
                                    "checkout_total_usd": quote["checkout_total_usd"]}
        # What was actually opened again on the date in the property's own recheck entry -
        # so a reader can tell a re-read from a carry-over. Fields not listed there were not
        # re-read on that date. last_checked follows the recheck date when one exists.
        rc = HOTEL_RECHECK.get(h["id"])
        h["last_checked"] = rc["on"] if rc else LAST_CHECKED
        h["recheck"] = rc
        w = walk_by_key.get((h["id"], VEN))
        h["walk_to_venetian_min"] = w["minutes"] if w else None
        h["walk_to_venetian_status"] = w["status"] if w else "unverified"
        h["walk_to_venetian_within_30"] = bool(w and w.get("within_30_min"))
        ww = walk_by_key.get((h["id"], WYN)) or {}
        h["walk_to_wynn_min"] = ww.get("minutes")
        h["walk_to_wynn_within_30"] = bool(ww.get("within_30_min"))
        hotels.append(h)
    with open(os.path.join(DATA, "hotels.json"), "w") as f:
        json.dump({"verified_on": VERIFIED_ON, "rows": hotels,
                   "method": "True cost per night is the official booking engine's own checkout total "
                             "(room charges + resort fee + taxes) divided by the number of nights in that "
                             "quote. It is filled in only when the property has a dated quote in the rate "
                             "log, so nothing is reconstructed from an assumed rate: the printed figures are "
                             "(room + fee) x (1 + verified room tax), and that identity is re-checked for every "
                             "entry in data/rates.json. data/rates.json keeps every quote separately with its "
                             "date, room type, occupancy, cancellation terms and source URL.",
                   }, f, indent=1)

    with open(os.path.join(DATA, "rates.json"), "w") as f:
        json.dump({"verified_on": VERIFIED_ON, "entries": RATES}, f, indent=1)

    with open(os.path.join(DATA, "walking.json"), "w") as f:
        json.dump({"verified_on": VERIFIED_ON, "max_minutes": 30, "rows": WALKING,
                   "note": "Walking time is only filled in when an official source publishes it. No official source "
                           "publishes walking times between these hotels and poker rooms, so the times are blank and a "
                           "route link is given instead. The 30-minute rule is applied to a value only once one is "
                           "verified."}, f, indent=1)

    with open(os.path.join(DATA, "venues.json"), "w") as f:
        json.dump({"verified_on": VERIFIED_ON, "rows": VENUES}, f, indent=1)

    # Fingerprint of every row, so the monitoring job can report what changed.
    snapshot = {}
    for r in rows:
        snapshot[r["id"]] = {
            "date": r["date"], "start": r["start"], "name": r["name"], "venue": r["venue"],
            "series": r["series"], "buy_in_usd": r["buy_in_usd"], "guarantee_usd": r["guarantee_usd"],
            "entry_status": r["entry_status"], "buy_in": r["rules"]["fee"]["value"],
            "flags": len(r.get("flags") or []),
        }
    with open(os.path.join(DATA, "row_snapshot.json"), "w") as f:
        json.dump({"generated_on": VERIFIED_ON, "row_count": len(rows), "rows": snapshot}, f, indent=1)

    # Every recurring format the dataset publishes, each carrying the room it belongs to
    # and the official document the values were quoted from.
    daily_rows = []
    for row in WYNN_DAILY:
        r = dict(row)
        r["room"] = "Wynn Las Vegas"
        r["venue"] = WYN
        r["source"] = SRC["wynn_daily_struct"]
        r["page"] = SRC["wynn_poker"]
        r["retrieved_on"] = "2026-11-17"
        daily_rows.append(r)
    for row in BELLAGIO_DAILY:
        r = dict(row)
        r["venue"] = "Bellagio"
        # The flyer itself is on MGM's content-asset host, which the approved-host list
        # deliberately excludes (F40), so the citation is the official page that links it.
        r["page"] = SRC["bellagio_poker"]
        r["document_url"] = BELLAGIO_FLYER_URLS[r["id"]]
        r["source"] = SRC["bellagio_poker"]
        r["retrieved_on"] = "2026-11-17"
        daily_rows.append(r)
    for row in CAESARS_DAILY:
        r = dict(row)
        r["venue"] = "Caesars Palace"
        r["source"] = SRC["caesars_daily_flyer"]
        r["page"] = SRC["caesars_casino"]
        r["retrieved_on"] = "2026-11-17"
        daily_rows.append(r)

    with open(os.path.join(DATA, "daily.json"), "w") as f:
        json.dump({"verified_on": VERIFIED_ON, "rows": daily_rows,
                   "note": "Recurring daily tournaments published by Wynn Las Vegas. The official poker page states: "
                           "\"The Daily Tournament schedule will be suspended during each Wynn Signature, Wynn Millions, "
                           "and Classic tournament series.\" The official daily terms and conditions state: \"Registration "
                           "for each Event will open four (4) hours prior to the scheduled start of play\", so registration "
                           "for the 12 p.m. daily events opens at 8 a.m. Note the suspension wording differs between the "
                           "two official sources: the poker page names Wynn Signature, Wynn Millions and Classic series, "
                           "while each daily structure sheet says the event \"may be suspended during Seniors Events, "
                           "Classic Events, or other Tournament Series\". Neither names the WPT World Championship "
                           "explicitly, so confirm before travelling. Read 2026-11-16.\n\n"
                           "Bellagio publishes three weekly flyers: Friday $600 NLH, Saturday $1,000 NLH "
                           "and Sunday $400 H.O.R.S.E., all at 11:00 a.m. Every one of them allows "
                           "buy-in and re-entry through the end of level 8 (Saturday: registration "
                           "until the start of level 10), and every one sells a larger starting stack "
                           "for a \"voluntary staff gratuity\", so none is single entry and none is "
                           "ranked. Caesars Palace publishes one daily flyer with four no-limit "
                           "hold'em events a day - 10 a.m. and 6 p.m. at $100, 2 p.m. and 9 p.m. at "
                           "$160 - each with a $50 add-on for 15,000 chips and re-entry on "
                           "elimination within the first break, so none is single entry either. "
                           "Recurring formats carry no calendar date on the official source, so none "
                           "is turned into a dated row or ranked. Read 2026-11-17.",
                   "sources": [{"label": "Official daily tournament poster", "url": SRC["wynn_daily_poster"]},
                               {"label": "Official daily tournament structures", "url": SRC["wynn_daily_struct"]},
                               {"label": "Official poker room page", "url": SRC["wynn_poker"]},
                               {"label": "Official Bellagio poker page (links the Friday, Saturday and "
                                         "Sunday tournament flyers)", "url": SRC["bellagio_poker"]},
                               {"label": "Official Caesars Palace casino page (links the daily "
                                         "tournament flyer)", "url": SRC["caesars_casino"]},
                               {"label": "Official Caesars Palace daily no-limit hold'em tournament "
                                         "flyer 2026", "url": SRC["caesars_daily_flyer"]}]}, f, indent=1)

    counts = {}
    for r in rows:
        counts[r["entry_status"]] = counts.get(r["entry_status"], 0) + 1
    print("total rows", len(rows), counts)
    for s in sorted({r["series"] for r in rows}):
        print("  ", s, sum(1 for r in rows if r["series"] == s))
    print("schedule days", len(build_schedule(rows)["days"]))
    print("flagged rows", sum(1 for r in rows if r.get("flags")))


if __name__ == "__main__":
    main()
