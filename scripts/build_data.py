#!/usr/bin/env python3
"""Builds data/*.json from verified official-source rows.

Every field carries the official source URL it was copied from, the retrieval
date, and (for quoted values) the verbatim excerpt. Nothing is inferred: a
field is left null when the official source does not state it, and a flag
marks it unverified. Fields that are computed rather than quoted are marked
with a `derived` key naming the method.

Run:  python3 scripts/build_data.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
os.makedirs(DATA, exist_ok=True)

VERIFIED_ON = "2026-11-16"

# ---------------------------------------------------------------- sources ---
SRC = {
    # Venetian — DeepStack Extravaganza
    "dse_nov_page": "https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html",
    "dse_nov_struct": "https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_{}.pdf",
    "dse_dec_page": "https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-dec-2026.html",
    "dse_dec_struct": "https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_dec_2026-structure_{}.pdf",
    "venetian_poker": "https://www.venetianlasvegas.com/resort/casino/poker.html",
    # Wynn
    "wynn_poker": "https://www.wynnlasvegas.com/casino/poker",
    "wpt_sched": "https://cdn.wynnresorts.com/image/upload/v1757097329/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Schedule.pdf",
    "wpt_struct": "https://cdn.wynnresorts.com/image/upload/v1750864036/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Structures.pdf",
    "wss_sched": "https://cdn.wynnresorts.com/image/upload/v1753296112/visitwynn_pdfs_files/Poker/Wynn%20Signature%20Series/Wynn_Signature_Series_Schedule.pdf",
    "wss_struct": "https://cdn.wynnresorts.com/image/upload/v1762299460/visitwynn_pdfs_files/Poker/Wynn%20Signature%20Series/Wynn_Signature_Series_Structures.pdf",
    "wynn_daily_poster": "https://cdn.wynnresorts.com/image/upload/v1752011166/visitwynn_pdfs_files/Poker/Daily%20Tournaments/poker-daily-tournament-poster.pdf",
    "wynn_daily_struct": "https://cdn.wynnresorts.com/image/upload/v1752011191/visitwynn_pdfs_files/Poker/Daily%20Tournaments/Poker-All_Daily_Structures.pdf",
    "wynn_terms": "https://www.wynnlasvegas.com/terms-and-conditions/848671",
    "wynn_parking": "https://www.wynnlasvegas.com/about-us/parking",
    # MGM Resorts
    "bellagio_poker": "https://bellagio.mgmresorts.com/en/casino/poker.html",
    "bellagio_fri": "https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/blt9cf95b0e60ec253e/6af491a3a9851d75c40be840/mgm-bellagio-poker-fridays-$600-nlh.pdf",
    "bellagio_sat": "https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/blt6d47974bf5a7d9b6/6af491a391a6e8e4230c9e07/mgm-bellagio-poker-saturdays-$1000-nlh.pdf",
    "bellagio_sun": "https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/blt07fcf1244a6da661/6af491a339e2b4f6b76a86ad/mgm-bellagio-poker-sundays-$400-horse.pdf",
    "bellagio_terms": "https://bellagio.mgmresorts.com/en/terms-and-conditions.html",
    "aria_poker": "https://aria.mgmresorts.com/en/casino/poker.html",
    "aria_terms": "https://aria.mgmresorts.com/en/terms-and-conditions.html",
    "mgm_parking": "https://www.mgmresorts.com/en/things-to-do/parking.html",
    # Hotels
    "venetian_terms": "https://www.venetianlasvegas.com/legal/hotel-terms-and-conditions.html",
    "venetian_fee": "https://www.venetianlasvegas.com/resort/resort-fee.html",
    "venetian_suite": "https://www.venetianlasvegas.com/resort/casino/poker/suite-rates.html",
    "venetian_book": "https://www.venetianlasvegas.com/book",
    "caesars_book": "https://www.caesars.com/book/?propcode=CLV&action=FindRooms",
    "clark_county": "https://www.clarkcountynv.gov/adobe/assets/urn:aaid:aem:29eabec9-8db1-4deb-b66e-5bae28a89da2/original/as/transient-lodging-licenses-by-category-as-of-07-2021.pdf",
    "osrm_table": "https://routing.openstreetmap.de/routed-foot/table/v1/driving/-115.1693352,36.1217073;-115.1682710,36.1241843;-115.1658180,36.1263781;-115.1653620,36.1289345;-115.1787230,36.1123192;-115.1779977,36.1070287;-115.1751896,36.1167079?annotations=duration,distance",
    "nominatim": "https://nominatim.openstreetmap.org/search?q={}&format=json&limit=1",
}

VENETIAN_VENUE = {
    "id": "venetian",
    "name": "The Venetian Resort Las Vegas (DeepStack Poker Room)",
    "address": "3355 Las Vegas Blvd S, Las Vegas, NV 89109",
    "lat": 36.1217073,
    "lon": -115.1693352,
    "address_source": SRC["clark_county"],
    "poker_room": "DeepStack Extravaganza is held in The Venetian Poker Room.",
    "sources": [
        {"label": "Venetian poker room (official)", "url": SRC["venetian_poker"]},
        {"label": "Official street address (Clark County licence list)", "url": SRC["clark_county"]},
    ],
}

WYNN_VENUE = {
    "id": "wynn",
    "name": "Wynn Las Vegas / Encore Poker Room",
    "address": "3131 Las Vegas Blvd S, Las Vegas, NV 89109",
    "lat": 36.1263781,
    "lon": -115.1658180,
    "address_source": SRC["clark_county"],
    "poker_room": "Official WPT terms: \"Players will register in the Wynn Las Vegas Poker Room, located in Encore at Wynn Las Vegas.\"",
    "sources": [
        {"label": "Wynn poker room (official)", "url": SRC["wynn_poker"]},
        {"label": "Official WPT terms and conditions (official PDF)", "url": SRC["wpt_struct"]},
        {"label": "Official street address (Clark County licence list)", "url": SRC["clark_county"]},
    ],
}

BELLAGIO_VENUE = {
    "id": "bellagio",
    "name": "Bellagio Poker Room",
    "address": "3600 Las Vegas Blvd S, Las Vegas, NV 89109",
    "lat": 36.1123192,
    "lon": -115.1787230,
    "address_source": SRC["clark_county"],
    "poker_room": "Official Bellagio poker page: \"Location: Northside of Casino, next to Sportsbook\".",
    "sources": [
        {"label": "Bellagio poker room (official)", "url": SRC["bellagio_poker"]},
        {"label": "Official street address (Clark County licence list)", "url": SRC["clark_county"]},
    ],
}

ARIA_VENUE = {
    "id": "aria",
    "name": "ARIA Poker Room",
    "address": "3730 Las Vegas Blvd S, Las Vegas, NV 89109",
    "lat": 36.1070287,
    "lon": -115.1779977,
    "address_source": SRC["clark_county"],
    "poker_room": "Official ARIA poker page: \"Location: East side of the casino floor, next to Main Valet Pick-up\".",
    "sources": [
        {"label": "ARIA poker room (official)", "url": SRC["aria_poker"]},
        {"label": "Official street address (Clark County licence list)", "url": SRC["clark_county"]},
    ],
}

CAESARS_VENUE = {
    "id": "caesars",
    "name": "Caesars Palace (center Strip)",
    "address": "3570 Las Vegas Blvd S, Las Vegas, NV 89109",
    "lat": 36.1167079,
    "lon": -115.1751896,
    "address_source": SRC["clark_county"],
    "poker_room": "No official Caesars poker-room tournament schedule for this series was located. Listed as a lodging option and walk reference only.",
    "sources": [
        {"label": "Caesars Palace hotel (official)", "url": "https://www.caesars.com/caesars-palace"},
        {"label": "Official street address (Clark County licence list)", "url": SRC["clark_county"]},
    ],
}

VENUES = [VENETIAN_VENUE, WYNN_VENUE, BELLAGIO_VENUE, ARIA_VENUE, CAESARS_VENUE]
VENUE_BY_ID = {v["id"]: v for v in VENUES}

# --------------------------------------------------- Venetian structure ----
# Every entry below was read from the official structure PDF named in the key.
# `single` is True only when the sheet contains no re-entry, rebuy, add-on,
# subsequent-buy-in or multi-flight clause.
# `fee_note` records any extra flat fee (for example a series organiser fee).
# `level_min` is the printed level duration; `late_reg` the printed cutoff.
# `gtd` is the printed guarantee; `gtd_by_event` overrides it per event number.
NOV_SHEETS = {
    1: dict(buy=200, fee=40, chips=25000, level=30, late="8 levels + Break (9:40 PM)",
            late_time="21:40", gtd=8000, gtd_note="prize pool + total bounties",
            single=True, tags=["bounty"], bounty="$50 per elimination",
            excerpt="$40 of the $200 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $160 of every $200 Buy In. / Players receive $50 bounty for each player they eliminate from the tournament. / A Prize Pool of $8,000 is guaranteed by the Venetian Poker Room which consists of the actual prize pool plus the total amount of $50 bounties that are awarded."),
    2: dict(buy=400, fee=70, chips=40000, level=40, late="9 levels + Break (5:55 PM)",
            late_time="17:55", gtd=75000, single=False, tags=["multi_flight"],
            excerpt="Any player who bags chips for Day 2 may not play a subsequent flight."),
    3: dict(buy=400, fee=70, chips=40000, level=40, late="9 levels + Break (5:55 PM)",
            late_time="17:55", gtd=75000, single=False, tags=["multi_flight"],
            excerpt="Any player who bags chips for Day 2 may not play a subsequent flight."),
    4: dict(buy=600, fee=95, chips=40000, level=40, late="9 levels + Break (5:55 PM)",
            late_time="17:55", gtd=150000, single=False, tags=["multi_flight"],
            excerpt="Any player who bags chips for Day 2 may not play a subsequent flight. / On Day 1A only, players who register before the start of the event (11:10 a.m.), will receive a $20 discount on house fees for a total buy in of $580 instead of $600."),
    5: dict(buy=300, fee=58, chips=40000, level=30, late="10 levels + Break (~4:55 PM)",
            late_time="16:55", gtd=10000, single=True, tags=[],
            excerpt="$58 of the $300 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $242 of every $300 Buy In. / This event pays 12.5% of the field"),
    6: dict(buy=400, fee=65, chips=40000, level=30, late="10 levels + Break (~4:55 PM)",
            late_time="16:55", gtd=15000, single=True, tags=[],
            excerpt="$65 of the $400 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $335 of every $400 Buy In."),
    7: dict(buy=600, fee=90, chips=40000, level=30, late="10 levels + Break (~4:55 PM)",
            late_time="16:55", gtd=30000, gtd_by_event={28: 40000, 63: 30000},
            single=True, tags=[],
            excerpt="$90 of the $600 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $510 of every $600 Buy In."),
    8: dict(buy=200, fee=40, chips=25000, level=30, late="8 levels + Break (9:40 PM)",
            late_time="21:40", gtd=20000, gtd_note="prize pool + total bounties",
            single=False, tags=["bounty", "subsequent_buy_in"], bounty="$50 per elimination",
            excerpt="PokerAtlas PRO players will receive a twenty ($20) rake discount on their initial $200 buy in only, for a total buy in of $180 instead of $200. / All subsequent buy in's after the initial buy in will be $200."),
    9: dict(buy=300, fee=60, chips=30000, level=30, late="6 levels + Break (~8:40 PM)",
            late_time="20:40", gtd=75000, single=False, tags=["multi_flight"],
            excerpt="Any player who bags chips for Day 2 may not play a subsequent flight. / SEE OTHER STRUCTURE SHEET FOR DAYS A+C"),
    10: dict(buy=300, fee=60, chips=30000, level=40, late="6 levels + Break (~3:40 PM)",
             late_time="15:40", gtd=75000, single=False, tags=["multi_flight"],
             excerpt="Any player who bags chips for Day 2 may not play a subsequent flight. / SEE OTHER STRUCTURE SHEET FOR DAYS B+D"),
    11: dict(buy=600, fee=90, chips=40000, level=30, late="10 levels + Break (4:55 PM)",
             late_time="16:55", gtd=30000, gtd_by_event={30: 40000, 54: 50000},
             single=True, tags=["bounty"], bounty="$200 to start, $500 once in the money",
             excerpt="$90 of the $600 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $510 of every $600 Buy In. / Players receive $200 Bounty for each player they eliminate from the tournament. Once we reach the money (posted payouts) – players receive a $500 Bounty…"),
    12: dict(buy=800, fee=110, chips=40000, level=40, late="6 levels + Break (~3:40 PM)",
             late_time="15:40", gtd=500000, single=False, tags=["multi_flight"],
             excerpt="Any player who bags chips for Day 2 may not play a subsequent flight. / SEE OTHER STRUCTURE SHEET FOR DAYS B+D+F"),
    13: dict(buy=800, fee=110, chips=40000, level=30, late="6 levels + Break (~8:40 PM)",
             late_time="20:40", gtd=500000, single=False, tags=["multi_flight"],
             excerpt="Any player who bags chips for Day 2 may not play a subsequent flight. / SEE OTHER STRUCTURE SHEET FOR DAYS A+C+F"),
    14: dict(buy=800, fee=110, chips=40000, level=20, late="6 levels + Break (~7:25 PM)",
             late_time="19:25", gtd=500000, single=False, tags=["multi_flight", "turbo"],
             excerpt="Any player who bags chips for Day 2 may not play a subsequent flight. / SEE OTHER STRUCTURE SHEETS FOR DAYS A+B+C+D+E"),
    15: dict(buy=300, fee=50, chips=25000, level=30, late="8 levels + Break (9:40 PM)",
             late_time="21:40", gtd=15000, gtd_note="prize pool + total bounties",
             single=True, tags=["bounty"], bounty="$100 per elimination",
             excerpt="$50 of the $300 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $250 of every $300 Buy In. / Players receive $100 bounty for each player they eliminate from the tournament."),
    16: dict(buy=800, fee=100, chips=40000, level=30, late="10 levels + Break (4:55 PM)",
             late_time="16:55", gtd=75000, gtd_note="prize pool + total bounties",
             single=True, tags=["bounty"], bounty="$200 to start, $500 once in the money",
             excerpt="$100 of the $800 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $700 of every $800 Buy In."),
    17: dict(buy=600, fee=90, chips=40000, level=30, late="10 levels + Break (~3:55 PM)",
             late_time="15:55", gtd=40000, single=True, tags=["seniors"],
             eligibility="Must be 50+ years of age to participate. Any player who buys into this event that is not 50+ years of age will not be entitled to any prize money or a refund of their buy in.",
             excerpt="$90 of the $600 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $510 of every $600 Buy In. / This event pays 15% of the field"),
    18: dict(buy=200, fee=35, chips=30000, level=20, late="6 levels + Break (~12:25 PM)",
             late_time="12:25", gtd=None, gtd_note="not printed on the sheet",
             single=True, tags=["race_day"],
             excerpt="$35 of the $200 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $165 of every $200 Buy In."),
    19: dict(buy=100, fee=20, chips=20000, level=20, late="6 levels + Break (~6:25 PM)",
             late_time="18:25", gtd=None, gtd_note="2 Seats (direct entry to Event #39)",
             single=True, tags=["satellite", "ladies"],
             eligibility="Open to Female players who must be 21+ years of age.",
             excerpt="Winners will be awarded direct entry to Event #39 / $20 of the $100 Buy-In is withheld for house fees (Rake + Staff)."),
    20: dict(buy=1100, fee=140, chips=40000, level=40, late="9 levels + Break (~4:55 PM)",
             late_time="16:55", gtd=300000, single=False, tags=["multi_flight", "seniors"],
             eligibility="Must be 50+ years of age to participate.",
             excerpt="Any player who bags chips for Day 2 may not play a subsequent flight. / Must be 50+ years of age to participate."),
    21: dict(buy=2200, fee=225, chips=40000, level=40, late="9 levels + Break (~4:55 PM)",
             late_time="16:55", gtd=1000000, single=False, tags=["multi_flight", "title_event"],
             excerpt="Any player who bags chips for Day 2 may not play a subsequent flight."),
    22: dict(buy=300, fee=58, chips=30000, level=30, late="8 levels + break (~4:40 PM)",
             late_time="16:40", gtd=10000, single=True, tags=["bomb_pot"],
             excerpt="$58 of the $300 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $242 of every $300 Buy In. / This event will play eight (8) handed and pay 12.5% of the field."),
    23: dict(buy=600, fee=90, chips=30000, level=30, late="8 levels + break (~4:40 PM)",
             late_time="16:40", gtd=25000, single=True, tags=["bomb_pot"],
             excerpt="$90 of the $600 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $510 of every $600 Buy In."),
    24: dict(buy=260, fee=40, chips=20000, level=20, late="6 levels + Break (~6:25 PM)",
             late_time="18:25", gtd=None, gtd_note="2 Seats (direct entry to Event #47)",
             single=True, tags=["satellite", "milestone"],
             excerpt="Winners will be awarded direct entry to Event #47 / $40 of the $260 Buy-In is withheld for house fees (Rake + Staff)."),
    25: dict(buy=260, fee=35, chips=20000, level=15, late="6 levels + Break",
             late_time=None, gtd=None, gtd_note="2 Seats (direct entry to Event #47)",
             single=True, tags=["satellite", "milestone", "turbo"],
             excerpt="Winners will be awarded direct entry to Event #47 / $35 of the $260 Buy-In is withheld for house fees (Rake + Staff)."),
    26: dict(buy=400, fee=60, chips=30000, level=30, late="8 levels + break (~4:40 PM)",
             late_time="16:40", gtd=15000, gtd_note="prize pool + total bounties",
             single=True, tags=["bounty"],
             excerpt="$60 of the $400 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $340 of every $400 Buy In."),
    27: dict(buy=600, fee=90, chips=30000, level=30, late="8 levels + break (~4:40 PM)",
             late_time="16:40", gtd=25000, gtd_note="prize pool + total bounties",
             single=True, tags=["bounty"],
             excerpt="$90 of the $600 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $510 of every $600 Buy In."),
    28: dict(buy=600, fee=90, chips=30000, level=30, late="8 levels + break (~4:40 PM)",
             late_time="16:40", gtd=25000, single=True, tags=["big_o"],
             excerpt="$90 of the $600 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $510 of every $600 Buy In."),
    29: dict(buy=200, fee=40, chips=30000, level=30, late="8 levels + Break (~3:40 PM)",
             late_time="15:40", gtd=None, gtd_note="not printed on the sheet",
             single=True, tags=[],
             excerpt="$40 of the $200 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $160 of every $200 Buy In."),
    30: dict(buy=200, fee=40, chips=25000, level=30, late="8 levels + Break (9:40 PM)",
             late_time="21:40", gtd=8000, gtd_note="prize pool + total bounties",
             single=True, tags=["pko"], bounty="$50 starting bounty; half of each eliminated player's bounty",
             excerpt="Players start the event as a $50 bounty. For each player they eliminate from the tournament, they will receive ½ of the other players bounty to keep as prize money…"),
    31: dict(buy=600, fee=80, fee_note="$10 LIPS flat fee", total_fee=90, chips=40000, level=30,
             late="8 levels + Break (~2:40 PM)", late_time="14:40", gtd=10000, single=True,
             tags=["tag_team"],
             eligibility="Tag teams consist of Female/Female or Female/Male; players rotate every level.",
             excerpt="$80 of the $600 Buy-In is withheld for house fees (Rake + Staff). $10 of the $600 Buy In will be withheld as a flat fee for Vegas Connected, INC, DBA Ladies International Poker Series (LIPS). Prize pool consists of $510 of every $600 Buy In."),
    32: dict(buy=800, fee=90, fee_note="$20 LIPS flat fee", total_fee=110, chips=40000, level=40,
             late="9 levels + Break (~4:55 PM)", late_time="16:55", gtd=40000, single=True,
             tags=["ladies", "two_day"],
             eligibility="Must be a female 21+ years of age and have a Venetian Rewards card to participate.",
             excerpt="Must be a female 21+ years of age and have a Venetian Rewards card to participate. / Day 1 Dec 10 @ 10:10 AM, Day 2 Dec 11 @ 10:00 AM"),
    33: dict(buy=600, fee=80, fee_note="$10 LIPS flat fee", total_fee=90, chips=40000, level=30,
             late="10 levels + Break (4:55 PM)", late_time="16:55", gtd=30000,
             gtd_note="prize pool + total bounties", single=True, tags=["bounty"],
             bounty="$200 per elimination",
             excerpt="Players receive $200 Bounty for each player they eliminate from the tournament. / Open to all Players; trophy to the last King and last Queen standing."),
    34: dict(buy=1100, fee=130, chips=40000, level=30, late="10 levels + Break (4:55 PM)",
             late_time="16:55", gtd=75000, gtd_note="prize pool + total bounties",
             single=True, tags=["pko"],
             excerpt="$130 of the $1,100 Buy-In is withheld for house fees (Rake + Staff)."),
    35: dict(buy=1100, fee=140, chips=40000, level=40, late="9 levels + Break (~4:55 PM)",
             late_time="16:55", gtd=500000, single=False, tags=["multi_flight"],
             excerpt="Any player who bags chips for Day 2 may not play a subsequent flight. / On Day 1A, players who register before the start of the event (10:10 a.m.) will receive a forty ($40) discount on house fees for a total buy in of $1,060 instead of $1,100."),
    36: dict(buy=1100, fee=140, chips=40000, level=40, late="9 levels + Break (~11:10 PM)",
             late_time="23:10", gtd=500000, single=False, tags=["multi_flight"],
             excerpt="Any player who bags chips for Day 2 may not play a subsequent flight. / On Day 1B, players who register before the start of the event (6:10 p.m.) will receive a forty ($40) discount on house fees for a total buy in of $1,060 instead of $1,100."),
    37: dict(buy=2200, fee=225, chips=40000, level=40, late="9 levels + Break (~11:10 PM)",
             late_time="23:10", gtd=1000000, single=False, tags=["multi_flight", "title_event"],
             excerpt="Any player who bags chips for Day 2 may not play a subsequent flight."),
}

DEC_SHEETS = {
    1: dict(buy=400, fee=65, chips=30000, level=30, late="8 levels + Break (~3:40 PM)",
            late_time="15:40", gtd=15000, single=True, tags=[],
            excerpt="$65 of the $400 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $335 of every $400 Buy In. / This event pays 12.5% of the field"),
    2: dict(buy=200, fee=40, chips=25000, level=30, late="8 levels + Break (9:40 PM)",
            late_time="21:40", gtd=8000, gtd_note="prize pool + total bounties",
            single=True, single_by_event={29: False}, tags=["bounty"],
            bounty="$50 per elimination",
            excerpt="$40 of the $200 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $160 of every $200 Buy In. / For Event #29 only … The $20 discount can be applied to the initial entry or any subsequent re-entry"),
    3: dict(buy=600, fee=90, chips=40000, level=30, late="10 levels + Break (4:55 PM)",
            late_time="16:55", gtd=40000, gtd_note="prize pool + total bounties",
            single=True, tags=["bounty"], bounty="$200 to start, $500 once in the money",
            excerpt="$90 of the $600 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $510 of every $600 Buy In. / Players receive $200 Bounty for each player they eliminate from the tournament. Once we reach the money (posted payouts) – players receive a $500 Bounty…"),
    4: dict(buy=260, fee=40, chips=20000, level=20, late="6 levels + Break (~5:25 PM or ~8:25 PM)",
            late_time=None, gtd=None, gtd_note="4 Seats (direct entry to Event #08)",
            single=True, tags=["satellite", "milestone"],
            excerpt="$40 of the $260 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $220 of every $260 Buy In. / All tournament prizes are direct entry into our $1,100 No Limit Hold'em Ante Up Championship Event #08"),
    5: dict(buy=200, fee=35, chips=20000, level=20, late="6 levels + Break (~5:25 PM or 12:25 PM)",
            late_time=None, gtd=None, gtd_note="2 Seats (direct entry to Event #20)",
            single=True, tags=["satellite", "milestone"],
            excerpt="$35 of the $200 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $165 of every $200 Buy In. / All tournament prizes are direct entry into our $1,600 No Limit Hold'em MSPT Event #20"),
    6: dict(buy=1100, fee=140, chips=40000, level=40, late="9 levels + Break (~5:55 PM)",
            late_time="17:55", gtd=300000, single=False, tags=["multi_flight", "title_event"],
            excerpt="$140 of the $1,100 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $960 of every $1,100 Buy In. / Any player who bags chips for Day 2 may not play a subsequent flight."),
    7: dict(buy=200, fee=30, chips=20000, level=15, late="6 levels + Break (~7:55 PM)",
            late_time="19:55", gtd=None, gtd_note="2 Seats (direct entry to Event #20)",
            single=True, tags=["satellite", "milestone", "turbo"],
            excerpt="$30 of the $200 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $170 of every $200 Buy In. / All tournament prizes are direct entry into our $1,600 No Limit Hold'em MSPT Event #20"),
    8: dict(buy=1600, fee=180, chips=40000, level=40, late="9 levels + Break (~5:55 PM)",
            late_time="17:55", gtd=400000, single=False, tags=["multi_flight", "title_event"],
            excerpt="$180 of the $1,600 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $1,420 of every $1,600 Buy In. On Day 1A, players who register before the start of level four (4) will receive a forty ($40) discount on house fees for a total buy in of $1,560 instead of $1,600. / Any player who bags chips for Day 2 may not play a subsequent flight."),
    9: dict(buy=200, fee=40, chips=25000, level=30, late="8 levels + Break (9:40 PM)",
            late_time="21:40", gtd=20000, gtd_note="prize pool + total bounties",
            single=False, tags=["bounty", "subsequent_buy_in"], bounty="$50 per elimination",
            excerpt="PokerAtlas PRO players will receive a twenty ($20) rake discount on their initial $200 buy in only… All subsequent buy in's after the initial buy in will be $200."),
    10: dict(buy=400, fee=65, chips=40000, level=30, late="10 levels + Break (~3:55 PM)",
             late_time="15:55", gtd=20000, single=True, tags=["seniors"],
             eligibility="Must be 50+ years of age to participate. Any player who buys into this event that is not 50+ years of age will not be entitled to any prize money or a refund of their buy in.",
             excerpt="$65 of the $400 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $335 of every $400 Buy In. / This event pays 15% of the field"),
    11: dict(buy=400, fee=65, chips=40000, level=30, late="10 levels + Break (~4:55 PM)",
             late_time="16:55", gtd=15000, single=True, tags=[],
             excerpt="$65 of the $400 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $335 of every $400 Buy In."),
    12: dict(buy=600, fee=90, chips=40000, level=30, late="10 levels + Break (~4:55 PM)",
             late_time="16:55", gtd=50000, single=True, tags=[],
             excerpt="$90 of the $600 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $510 of every $600 Buy In."),
    13: dict(buy=300, fee=60, chips=30000, level=40, late="6 levels + Break (~3:40 PM)",
             late_time="15:40", gtd=100000, single=False, tags=["multi_flight"],
             excerpt="$60 of the $300 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $240 of every $300 Buy In. / Any player who bags chips for Day 2 may not play a subsequent flight. / SEE OTHER STRUCTURE SHEET FOR DAYS B+D+F"),
    14: dict(buy=300, fee=60, chips=30000, level=30, late="6 levels + Break (~8:40 PM)",
             late_time="20:40", gtd=100000, single=False, tags=["multi_flight"],
             excerpt="$60 of the $300 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $240 of every $300 Buy In. / Any player who bags chips for Day 2 may not play a subsequent flight. / SEE OTHER STRUCTURE SHEET FOR DAYS A+C+E"),
    15: dict(buy=250, fee=50, chips=40000, level=30, late="8 levels + Break (~3:40 PM or ~9:40 PM)",
             late_time=None, gtd=75000, single=False, tags=["multi_flight", "day1_payout"],
             excerpt="$50 of the $250 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $200 of every $250 Buy In. Any player who buys into Day 1A before 11:10 AM or Day 1B before 5:10 PM will only pay $40 in House Fees for a total buy in of $240 instead of $250. / Any player who bags chips for Day 2 may not play a subsequent flight. Players who cash on Day 1 but bust before making Day 2 may play another flight."),
}

# --------------------------------------------------- Venetian schedule rows --
# (date, time, event_no, sheet_no, name, is_restart)
DSE_NOV = [
    ("2026-11-16", "11:10", 1, 10, "$300 No Limit Hold'em 1A $75K GTD", False),
    ("2026-11-16", "17:10", 1, 9, "$300 No Limit Hold'em 1B $75K GTD", False),
    ("2026-11-17", "11:10", 1, 10, "$300 No Limit Hold'em 1C $75K GTD", False),
    ("2026-11-17", "17:10", 1, 9, "$300 No Limit Hold'em 1D $75K GTD", False),
    ("2026-11-18", "11:10", 2, 5, "$300 No Limit Hold'em $10K GTD (1Day)", False),
    ("2026-11-18", "12:00", 1, 10, "$300 No Limit Hold'em Day 2 Restart", True),
    ("2026-11-19", "10:10", 3, 18, "$200 NLH RaceDay Stack (1Day) - Race to finish before the Race", False),
    ("2026-11-20", "10:10", 4, 18, "$200 NLH RaceDay Stack (1Day) - Race to finish before the Race", False),
    ("2026-11-21", "10:10", 5, 18, "$200 NLH RaceDay Stack (1Day) - Race to finish before the Race", False),
    ("2026-11-22", "11:10", 6, 29, "$200 No Limit Hold'em (1Day)", False),
    ("2026-11-23", "11:10", 7, 2, "$400 No Limit Hold'em 1A $75K GTD", False),
    ("2026-11-23", "17:10", 8, 30, "$200 No Limit Hold'em $8K GTD (1Day) - Progressive Knock-Out Bounty (PKO)", False),
    ("2026-11-24", "11:10", 7, 2, "$400 No Limit Hold'em 1B $75K GTD", False),
    ("2026-11-24", "17:10", 9, 1, "$200 No Limit Hold'em Bounty $8K GTD (1Day)", False),
    ("2026-11-25", "11:00", 7, 2, "$400 No Limit Hold'em Day 2 Restart", True),
    ("2026-11-25", "11:10", 10, 6, "$400 No Limit Hold'em $15K GTD (1Day)", False),
    ("2026-11-25", "17:10", 11, 1, "$200 No Limit Hold'em Bounty $8K GTD (1Day)", False),
    ("2026-11-26", "11:10", 12, 5, "$300 No Limit Hold'em $10K GTD (1Day)", False),
    ("2026-11-26", "17:10", 13, 1, "$200 No Limit Hold'em Bounty $8K GTD (1Day)", False),
    ("2026-11-27", "11:10", 14, 7, "$600 No Limit Hold'em $30K GTD (1Day)", False),
    ("2026-11-27", "17:10", 15, 1, "$200 No Limit Hold'em Bounty $8K GTD (1Day)", False),
    ("2026-11-28", "11:10", 16, 11, "$600 No Limit Hold'em Bounty $30K GTD (1Day) - $200 bounties to start & $500 bounties in the money", False),
    ("2026-11-28", "12:10", 17, 26, "$400 Pot Limit Omaha Bounty $15K GTD (1Day)", False),
    ("2026-11-28", "17:10", 18, 8, "$200 NLH PokerAtlas Valuetown Bounty $20K GTD (1Day) - PokerAtlas PRO $20 rake discount", False),
    ("2026-11-29", "11:10", 19, 3, "$400 No Limit Hold'em 1A $75K GTD", False),
    ("2026-11-29", "12:10", 20, 22, "$300 Pot Limit Omaha $10K GTD (1Day) - Double Board Bomb Pot", False),
    ("2026-11-29", "17:10", 21, 1, "$200 No Limit Hold'em Bounty $8K GTD (1Day)", False),
    ("2026-11-30", "11:10", 19, 3, "$400 No Limit Hold'em 1B $75K GTD", False),
    ("2026-11-30", "17:10", 22, 1, "$200 No Limit Hold'em Bounty $8K GTD (1Day)", False),
    ("2026-12-01", "11:10", 19, 3, "$400 No Limit Hold'em 1C $75K GTD", False),
    ("2026-12-01", "17:10", 23, 1, "$200 No Limit Hold'em Bounty $8K GTD (1Day)", False),
    ("2026-12-02", "10:10", 24, 17, "$600 No Limit Hold'em Seniors $40K GTD (1Day) - Must be 50+ years of age", False),
    ("2026-12-02", "11:00", 19, 3, "$400 No Limit Hold'em Day 2 Restart", True),
    ("2026-12-02", "17:10", 25, 1, "$200 No Limit Hold'em Bounty $8K GTD (1Day)", False),
    ("2026-12-03", "11:10", 26, 12, "$800 No Limit Hold'em 1A $500K GTD", False),
    ("2026-12-03", "12:10", 27, 28, "$600 BIG O $25K GTD (1Day)", False),
    ("2026-12-03", "17:10", 26, 13, "$800 No Limit Hold'em 1B $500K GTD", False),
    ("2026-12-04", "11:10", 26, 12, "$800 No Limit Hold'em 1C $500K GTD", False),
    ("2026-12-04", "17:10", 26, 13, "$800 No Limit Hold'em 1D $500K GTD", False),
    ("2026-12-05", "11:10", 26, 12, "$800 No Limit Hold'em 1E $500K GTD", False),
    ("2026-12-05", "17:10", 26, 14, "$800 No Limit Hold'em 1F (Turbo) $500K GTD", False),
    ("2026-12-06", "11:10", 28, 7, "$600 No Limit Hold'em $40K GTD (1Day)", False),
    ("2026-12-06", "12:00", 26, 12, "$800 No Limit Hold'em Day 2 Restart", True),
    ("2026-12-06", "17:10", 29, 15, "$300 No Limit Hold'em Bounty $15K GTD (1Day)", False),
    ("2026-12-07", "11:10", 30, 11, "$600 No Limit Hold'em Bounty $40K GTD (1Day) - $200 bounties to start & $500 bounties in the money", False),
    ("2026-12-07", "17:10", 31, 15, "$300 No Limit Hold'em Bounty $15K GTD (1Day)", False),
    ("2026-12-08", "10:10", 32, 17, "$600 No Limit Hold'em Seniors $40K GTD (1Day) - Must be 50+ years of age", False),
    ("2026-12-08", "16:10", 33, 19, "$100 NLH LIPS Ladies Milestone Satellite (1Day) - Awards Direct Entry to Event #39", False),
    ("2026-12-08", "17:10", 34, 15, "$300 No Limit Hold'em Bounty $15K GTD (1Day)", False),
    ("2026-12-09", "10:10", 35, 31, "$600 NLH LIPS Poker Jingle Tag Team $10K GTD (1Day) - Tag Teams Consist of Female/Female or Female/Male", False),
    ("2026-12-09", "11:10", 36, 16, "$800 No Limit Hold'em Bounty $75K GTD (1Day) - $200 bounties to start & $500 bounties in the money", False),
    ("2026-12-09", "16:10", 37, 19, "$100 NLH LIPS Ladies Milestone Satellite (1Day) - Awards Direct Entry to Event #39", False),
    ("2026-12-09", "17:10", 38, 15, "$300 No Limit Hold'em Bounty $15K GTD (1Day)", False),
    ("2026-12-10", "10:10", 39, 32, "$800 No Limit Hold'em LIPS Ladies $40K GTD (2Day) - Women in Poker Main Event", False),
    ("2026-12-10", "12:10", 40, 27, "$600 Pot Limit Omaha Bounty $25K GTD (1Day)", False),
    ("2026-12-10", "16:10", 41, 24, "$260 NLH Milestone Satellite (1Day) - Awards Direct Entry to Event #47", False),
    ("2026-12-10", "17:10", 42, 15, "$300 No Limit Hold'em Bounty $15K GTD (1Day)", False),
    ("2026-12-11", "10:00", 39, 32, "$800 No Limit Hold'em LIPS Ladies Day 2 Restart - Play Down to Final 7 (PokerGO)", True),
    ("2026-12-11", "11:10", 43, 33, "$600 No Limit Hold'em LIPS $30K GTD (1Day) - KINGS and QUEENS Bounty - Open to all players", False),
    ("2026-12-11", "16:10", 44, 24, "$260 NLH Milestone Satellite (1Day) - Awards Direct Entry to Event #47", False),
    ("2026-12-11", "19:00", 39, 32, "$800 No Limit Hold'em LIPS Ladies Final Table - Streamed Final Table (PokerGO)", True),
    ("2026-12-11", "20:10", 45, 25, "$260 NLH Turbo Milestone Satellite (1Day) - Awards Direct Entry to Event #47", False),
    ("2026-12-12", "09:10", 46, 25, "$260 NLH Turbo Milestone Satellite (1Day) - Awards Direct Entry to Event #47", False),
    ("2026-12-12", "10:10", 47, 21, "$2,200 No Limit Hold'em 1A $1 Mill GTD - PokerAtlas Championship Title Event", False),
    ("2026-12-12", "12:10", 48, 25, "$260 NLH Turbo Milestone Satellite (1Day) - Awards Direct Entry to Event #47", False),
    ("2026-12-12", "18:10", 47, 37, "$2,200 No Limit Hold'em 1B $1 Mill GTD - PokerAtlas Championship Title Event", False),
    ("2026-12-13", "10:10", 49, 20, "$1,100 No Limit Hold'em Seniors 1A $300K GTD - Must be 50+ years of age", False),
    ("2026-12-13", "13:00", 47, 21, "$2,200 NLH PokerAtlas Championship Title Event Day 2 Restart - Play Down to Final 7 (PokerGO)", True),
    ("2026-12-13", "17:10", 50, 15, "$300 No Limit Hold'em Bounty $15K GTD (1Day)", False),
    ("2026-12-14", "10:10", 49, 20, "$1,100 No Limit Hold'em Seniors 1B $300K GTD - Must be 50+ years of age", False),
    ("2026-12-14", "11:00", 47, 21, "$2,200 NLH PokerAtlas Championship Title Event Day 3 Restart - Streamed Final Table (PokerGO)", True),
    ("2026-12-14", "17:10", 51, 15, "$300 No Limit Hold'em Bounty $15K GTD (1Day)", False),
    ("2026-12-15", "10:00", 49, 20, "$1,100 No Limit Hold'em Seniors Day 2 Restart", True),
    ("2026-12-15", "11:10", 52, 34, "$1,100 No Limit Hold'em $75K GTD (1Day) - Progressive Knock-Out Bounty (PKO)", False),
    ("2026-12-15", "17:10", 53, 15, "$300 No Limit Hold'em Bounty $15K GTD (1Day)", False),
    ("2026-12-16", "11:10", 54, 11, "$600 No Limit Hold'em Bounty $50K GTD (1Day) - $200 bounties to start & $500 bounties in the money", False),
    ("2026-12-16", "17:10", 55, 15, "$300 No Limit Hold'em Bounty $15K GTD (1Day)", False),
    ("2026-12-17", "10:10", 56, 35, "$1,100 No Limit Hold'em 1A $500K GTD - $40 Rake Discount for Entries Before 10:10 a.m.", False),
    ("2026-12-17", "12:10", 57, 23, "$600 Pot Limit Omaha $25K GTD (1Day) - Double Board Bomb Pot", False),
    ("2026-12-17", "18:10", 56, 36, "$1,100 No Limit Hold'em 1B $500K GTD - $40 Rake Discount for Entries Before 6:10 p.m.", False),
    ("2026-12-18", "10:10", 56, 35, "$1,100 No Limit Hold'em 1C $500K GTD", False),
    ("2026-12-18", "18:10", 56, 36, "$1,100 No Limit Hold'em 1D $500K GTD", False),
    ("2026-12-19", "10:10", 56, 35, "$1,100 No Limit Hold'em 1E $500K GTD", False),
    ("2026-12-19", "17:10", 58, 8, "$200 NLH PokerAtlas Valuetown Bounty $20K GTD (1Day) - PokerAtlas PRO $20 rake discount", False),
    ("2026-12-20", "11:00", 56, 35, "$1,100 No Limit Hold'em Day 2 Restart", True),
    ("2026-12-20", "11:10", 59, 4, "$600 No Limit Hold'em 1A $150K GTD - $20 Rake Discount for Entries Before 11:10 a.m.", False),
    ("2026-12-20", "17:10", 60, 1, "$200 No Limit Hold'em Bounty $8K GTD (1Day)", False),
    ("2026-12-21", "11:10", 59, 4, "$600 No Limit Hold'em 1B $150K GTD", False),
    ("2026-12-21", "17:10", 61, 1, "$200 No Limit Hold'em Bounty $8K GTD (1Day)", False),
    ("2026-12-22", "11:10", 59, 4, "$600 No Limit Hold'em 1C $150K GTD", False),
    ("2026-12-22", "17:10", 62, 1, "$200 No Limit Hold'em Bounty $8K GTD (1Day)", False),
    ("2026-12-23", "11:00", 59, 4, "$600 No Limit Hold'em Day 2 Restart", True),
    ("2026-12-23", "11:10", 63, 7, "$600 No Limit Hold'em $30K GTD (1Day)", False),
    ("2026-12-23", "17:10", 64, 1, "$200 No Limit Hold'em Bounty $8K GTD (1Day)", False),
]

DSE_DEC = [
    ("2026-12-24", "11:10", 1, 1, "$400 No Limit Hold'em $15K GTD (1Day)", False),
    ("2026-12-24", "17:10", 2, 2, "$200 No Limit Hold'em Bounty $8K GTD (1Day)", False),
    ("2026-12-25", "11:10", 3, 1, "$400 No Limit Hold'em $15K GTD (1Day)", False),
    ("2026-12-25", "17:10", 4, 2, "$200 No Limit Hold'em Bounty $8K GTD (1Day)", False),
    ("2026-12-26", "11:10", 5, 3, "$600 No Limit Hold'em Bounty $40K GTD (1Day) - $200 bounties to start & $500 bounties in the money", False),
    ("2026-12-26", "15:10", 6, 4, "$260 NLH Milestone Satellite (1Day) - Awards 1 in 5 (20%) Direct Entry into Event #08", False),
    ("2026-12-26", "18:10", 7, 4, "$260 NLH Milestone Satellite (1Day) - Awards 1 in 5 (20%) Direct Entry into Event #08", False),
    ("2026-12-27", "11:10", 8, 6, "$1,100 No Limit Hold'em 1A $300K GTD - Ante Up Championship", False),
    ("2026-12-27", "15:10", 9, 4, "$260 NLH Milestone Satellite (1Day) - Awards 1 in 5 (20%) Direct Entry into Event #08", False),
    ("2026-12-27", "18:10", 10, 4, "$260 NLH Milestone Satellite (1Day) - Awards 1 in 5 (20%) Direct Entry into Event #08", False),
    ("2026-12-28", "11:10", 8, 6, "$1,100 No Limit Hold'em 1B $300K GTD - Ante Up Championship", False),
    ("2026-12-28", "15:10", 11, 4, "$260 NLH Milestone Satellite (1Day) - Awards 1 in 5 (20%) Direct Entry into Event #08", False),
    ("2026-12-28", "18:10", 12, 4, "$260 NLH Milestone Satellite (1Day) - Awards 1 in 5 (20%) Direct Entry into Event #08", False),
    ("2026-12-29", "11:10", 8, 6, "$1,100 No Limit Hold'em 1C $300K GTD - Ante Up Championship", False),
    ("2026-12-29", "17:10", 13, 2, "$200 No Limit Hold'em Bounty $8K GTD (1Day)", False),
    ("2026-12-30", "11:00", 8, 6, "$1,100 No Limit Hold'em Ante Up Day 2 Restart - Play Down to Final 7 (PokerGO)", True),
    ("2026-12-30", "11:10", 14, 12, "$600 No Limit Hold'em $50K GTD (1Day)", False),
    ("2026-12-30", "15:10", 15, 5, "$200 NLH Milestone Satellite (1Day) - Awards Direct Entry into Event #20", False),
    ("2026-12-30", "18:10", 16, 7, "$200 NLH Turbo Milestone Satellite (1Day) - Awards Direct Entry into Event #20", False),
    ("2026-12-31", "10:00", 8, 6, "$1,100 No Limit Hold'em Ante Up Day 3 Restart - Streamed Final Table (PokerGO)", True),
    ("2026-12-31", "11:10", 17, 1, "$400 No Limit Hold'em $15K GTD (1Day)", False),
    ("2026-12-31", "15:10", 18, 5, "$200 NLH Milestone Satellite (1Day) - Awards Direct Entry into Event #20", False),
    ("2026-12-31", "18:10", 19, 7, "$200 NLH Turbo Milestone Satellite (1Day) - Awards Direct Entry into Event #20", False),
    ("2027-01-01", "11:10", 20, 8, "$1,600 No Limit Hold'em MSPT 1A $400K GTD - $40 Reduced Rake until the start of Level 4", False),
    ("2027-01-01", "15:10", 21, 5, "$200 NLH Milestone Satellite (1Day) - Awards Direct Entry into Event #20", False),
    ("2027-01-01", "17:10", 22, 2, "$200 No Limit Hold'em Bounty $8K GTD (1Day)", False),
    ("2027-01-02", "10:10", 23, 5, "$200 NLH Milestone Satellite (1Day) - Awards Direct Entry into Event #20", False),
    ("2027-01-02", "11:10", 20, 8, "$1,600 No Limit Hold'em MSPT 1B $400K GTD", False),
    ("2027-01-02", "15:10", 24, 5, "$200 NLH Milestone Satellite (1Day) - Awards Direct Entry into Event #20", False),
    ("2027-01-02", "17:10", 25, 9, "$200 NLH PokerAtlas Valuetown Bounty $20K GTD (1Day) - PokerAtlas PRO $20 rake discount", False),
    ("2027-01-03", "11:10", 20, 8, "$1,600 No Limit Hold'em MSPT 1C $400K GTD", False),
    ("2027-01-03", "17:10", 26, 2, "$200 No Limit Hold'em Bounty $8K GTD (1Day)", False),
    ("2027-01-04", "11:10", 20, 8, "$1,600 No Limit Hold'em MSPT Day 2 Restart", True),
    ("2027-01-04", "11:10", 27, 15, "$250 No Limit Hold'em 1A $75K GTD (1Day) - Day 1 Payouts with 5% advancing to Day 2", False),
    ("2027-01-04", "17:10", 27, 15, "$250 No Limit Hold'em 1B $75K GTD (1Day) - Day 1 Payouts with 5% advancing to Day 2", False),
    ("2027-01-05", "11:10", 27, 15, "$250 No Limit Hold'em 1C $75K GTD (1Day) - Day 1 Payouts with 5% advancing to Day 2", False),
    ("2027-01-05", "17:10", 27, 15, "$250 No Limit Hold'em 1D $75K GTD (1Day) - Day 1 Payouts with 5% advancing to Day 2", False),
    ("2027-01-06", "11:10", 28, 11, "$400 No Limit Hold'em $15K GTD (1Day)", False),
    ("2027-01-06", "12:00", 27, 15, "$250 No Limit Hold'em Day 2 Restart", True),
    ("2027-01-06", "17:10", 29, 2, "$200 No Limit Hold'em Bounty $8K GTD (1Day) - Show Your CES Badge - $10 rake discount", False),
    ("2027-01-07", "11:10", 30, 13, "$300 No Limit Hold'em 1A $100K GTD (1Day)", False),
    ("2027-01-07", "17:10", 30, 14, "$300 No Limit Hold'em 1B $100K GTD (1Day) - Show Your CES Badge - $10 rake discount", False),
    ("2027-01-08", "11:10", 30, 13, "$300 No Limit Hold'em 1C $100K GTD (1Day)", False),
    ("2027-01-08", "17:10", 30, 14, "$300 No Limit Hold'em 1D $100K GTD (1Day) - Show Your CES Badge - $10 rake discount", False),
    ("2027-01-09", "11:10", 30, 13, "$300 No Limit Hold'em 1E $100K GTD (1Day)", False),
    ("2027-01-09", "17:10", 30, 14, "$300 No Limit Hold'em 1F $100K GTD (1Day) - Show Your CES Badge - $10 rake discount", False),
    ("2027-01-10", "10:10", 31, 10, "$400 No Limit Hold'em Seniors $20K GTD (1Day) - Must be 50+ years of age", False),
    ("2027-01-10", "12:00", 30, 13, "$300 No Limit Hold'em Day 2 Restart", True),
    ("2027-01-10", "17:10", 32, 2, "$200 No Limit Hold'em Bounty $8K GTD (1Day)", False),
]

# Official NYE schedule rows whose printed date is wrong. The official page
# prints "Saturday, December 26, 2025" for events 5, 6 and 7 although the
# series runs December 24, 2026 - January 10, 2027. The calendar position and
# the surrounding rows fix the year at 2026; the typo is recorded in the
# irregularity log and flagged on each affected row.
NYE_DATE_TYPO_EVENTS = {5, 6, 7}

# ------------------------------------------------------ Wynn WPT schedule ---
# (date, time, label, name, buy_in, guarantee, structure_key)
# structure_key is the verified official structure section, or None when the
# section was not extracted (the PDF text extraction was capped).
WPT_RE = "Unlimited re-entry for each starting flight will be available until the start of level {lvl}."
WPT = [
    ("2026-11-27", "11:00", "$600 NLH $400K 1A", "$600 No Limit Hold'em $400K GTD - Day 1A", 600, 400000, "n600", 9),
    ("2026-11-27", "12:00", "Mixed Triple Draw", "$600 Mixed Triple Draw (A-5, 2-7, Badugi)", 600, None, "triple", 9),
    ("2026-11-27", "13:00", "PLO $400", "$400 Pot Limit Omaha", 400, None, None, None),
    ("2026-11-27", "17:00", "$600 NLH $400K 1B", "$600 No Limit Hold'em $400K GTD - Day 1B", 600, 400000, "n600", 9),
    ("2026-11-28", "11:00", "$600 NLH $400K 1C", "$600 No Limit Hold'em $400K GTD - Day 1C", 600, 400000, "n600", 9),
    ("2026-11-28", "12:00", "Mixed Triple Draw (2nd)", "$600 Mixed Triple Draw (A-5, 2-7, Badugi) - second listed date", 600, None, "triple", 9),
    ("2026-11-28", "17:00", "$600 NLH $400K 1D", "$600 No Limit Hold'em $400K GTD - Day 1D", 600, 400000, "n600", 9),
    ("2026-11-29", "11:00", "$600 NLH $400K 1E", "$600 No Limit Hold'em $400K GTD - Day 1E", 600, 400000, "n600", 9),
    ("2026-11-29", "18:00", "$600 NLH $400K 1F", "$600 No Limit Hold'em $400K GTD - Day 1F (Turbo)", 600, 400000, "n600", 9),
    ("2026-11-30", "11:00", "$800 NLH $1M 1A", "$800 No Limit Hold'em $1,000,000 GTD - Day 1A", 800, 1000000, "n800", 9),
    ("2026-11-30", "12:00", "Limit Omaha 8", "$600 Limit Omaha 8", 600, None, "lo8", 9),
    ("2026-11-30", "17:00", "$800 NLH $1M 1B", "$800 No Limit Hold'em $1,000,000 GTD - Day 1B", 800, 1000000, "n800", 9),
    ("2026-12-01", "11:00", "$800 NLH $1M 1C", "$800 No Limit Hold'em $1,000,000 GTD - Day 1C", 800, 1000000, "n800", 9),
    ("2026-12-01", "12:00", "Limit Omaha 8/Stud 8", "$600 Limit Omaha 8/Stud 8", 600, None, "lo88", 9),
    ("2026-12-01", "13:00", "PLO $1,100", "$1,100 Pot Limit Omaha", 1100, None, "plo1100", 9),
    ("2026-12-01", "17:00", "$800 NLH $1M 1D", "$800 No Limit Hold'em $1,000,000 GTD - Day 1D", 800, 1000000, "n800", 9),
    ("2026-12-02", "11:00", "$800 NLH $1M 1E", "$800 No Limit Hold'em $1,000,000 GTD - Day 1E", 800, 1000000, "n800", 9),
    ("2026-12-02", "18:00", "$800 NLH $1M 1F", "$800 No Limit Hold'em $1,000,000 GTD - Day 1F (Turbo)", 800, 1000000, "n800", 9),
    ("2026-12-03", "11:00", "$1,600 NLH $1M 1A", "$1,600 No Limit Hold'em $1,000,000 GTD - Day 1A", 1600, 1000000, "n1600", 10),
    ("2026-12-04", "11:00", "$1,600 NLH $1M 1B", "$1,600 No Limit Hold'em $1,000,000 GTD - Day 1B", 1600, 1000000, "n1600", 10),
    ("2026-12-04", "12:00", "HORSE $600", "$600 HORSE", 600, None, None, None),
    ("2026-12-05", "11:00", "WPT Prime 1A", "$1,100 WPT Prime Championship $5M GTD - Day 1A", 1100, 5000000, "prime", 10),
    ("2026-12-05", "21:00", "NLH Turbo $50K", "$600 NLH Turbo $50K GTD", 600, 50000, None, None),
    ("2026-12-06", "11:00", "PLO Mystery Bounty 1A", "$1,600 PLO Mystery Bounty $500K GTD - Day 1A", 1600, 500000, "mystery", 10),
    ("2026-12-06", "11:00", "WPT Prime 1B", "$1,100 WPT Prime Championship $5M GTD - Day 1B", 1100, 5000000, "prime", 10),
    ("2026-12-06", "18:00", "PLO Mystery Bounty 1B", "$1,600 PLO Mystery Bounty $500K GTD - Day 1B", 1600, 500000, "mystery", 10),
    ("2026-12-06", "21:00", "NLH Turbo $50K (2)", "$600 NLH Turbo $50K GTD", 600, 50000, None, None),
    ("2026-12-07", "11:00", "HORSE (2 Day) $1,100", "$1,100 HORSE (2 Day)", 1100, None, None, None),
    ("2026-12-07", "11:00", "WPT Prime 1C", "$1,100 WPT Prime Championship $5M GTD - Day 1C", 1100, 5000000, "prime", 10),
    ("2026-12-07", "13:00", "PLO $500 Bounty", "$1,600 PLO $500 Bounty $100K GTD", 1600, 100000, None, None),
    ("2026-12-07", "21:00", "NLH Turbo $50K (3)", "$600 NLH Turbo $50K GTD", 600, 50000, None, None),
    ("2026-12-08", "11:00", "WPT Prime 1D", "$1,100 WPT Prime Championship $5M GTD - Day 1D", 1100, 5000000, "prime", 10),
    ("2026-12-08", "21:00", "NLH Turbo $50K (4)", "$600 NLH Turbo $50K GTD", 600, 50000, None, None),
    ("2026-12-09", "11:00", "NLH (2 Day) $1,600", "$1,600 No Limit Hold'em (2 Day) $1M GTD", 1600, 1000000, None, None),
    ("2026-12-09", "13:00", "PLO $1,000 Bounty", "$3,000 PLO $1,000 Bounty $250K GTD", 3000, 250000, None, None),
    ("2026-12-09", "13:00", "Limit Omaha 8 $800", "$800 Limit Omaha 8", 800, None, None, None),
    ("2026-12-09", "21:00", "NLH Turbo $50K (5)", "$600 NLH Turbo $50K GTD", 600, 50000, None, None),
    ("2026-12-10", "10:00", "Super Gold Million 1A", "$400 Super Gold Million Mystery Bounty $3M GTD - Day 1A", 400, 3000000, None, None),
    ("2026-12-10", "18:00", "Super Gold Million 1B", "$400 Super Gold Million Mystery Bounty $3M GTD - Day 1B", 400, 3000000, None, None),
    ("2026-12-11", "10:00", "Super Gold Million 1C", "$400 Super Gold Million Mystery Bounty $3M GTD - Day 1C", 400, 3000000, None, None),
    ("2026-12-11", "18:00", "Super Gold Million 1D", "$400 Super Gold Million Mystery Bounty $3M GTD - Day 1D", 400, 3000000, None, None),
    ("2026-12-12", "10:00", "NLH $800", "$800 No Limit Hold'em $100K GTD", 800, 100000, None, None),
    ("2026-12-12", "13:00", "PLO $3,000", "$3,000 Pot Limit Omaha $250K GTD", 3000, 250000, None, None),
    ("2026-12-12", "21:00", "NLH Turbo $50K (6)", "$600 NLH Turbo $50K GTD", 600, 50000, None, None),
    ("2026-12-13", "11:00", "WPT Championship 1A", "$10,400 WPT World Championship - Day 1A ($1M added by ClubWPT Gold)", 10400, None, None, None),
    ("2026-12-13", "11:00", "Ladies NIH Championship", "$1,100 Ladies NIH Championship $250K GTD", 1100, 250000, None, None),
    ("2026-12-13", "11:00", "NLH $800 1A", "$800 No Limit Hold'em $500K GTD - Day 1A", 800, 500000, None, None),
    ("2026-12-13", "12:00", "PLO $1,600 1A", "$1,600 Pot Limit Omaha $1M GTD - Day 1A", 1600, 1000000, None, None),
    ("2026-12-14", "11:00", "WPT Championship 1B", "$10,400 WPT World Championship - Day 1B ($1M added by ClubWPT Gold)", 10400, None, None, None),
    ("2026-12-14", "11:00", "NLH $800 1B", "$800 No Limit Hold'em $500K GTD - Day 1B", 800, 500000, None, None),
    ("2026-12-14", "12:00", "PLO $1,600 1B", "$1,600 Pot Limit Omaha $1M GTD - Day 1B", 1600, 1000000, None, None),
    ("2026-12-14", "12:00", "Mixed Triple Draw (2 Day)", "$1,100 Mixed Triple Draw (2 Day)", 1100, None, None, None),
    ("2026-12-14", "19:00", "PLO Turbo", "$1,100 PLO Turbo $100K GTD", 1100, 100000, None, None),
    ("2026-12-14", "21:00", "NLH Turbo $50K (7)", "$600 NLH Turbo $50K GTD", 600, 50000, None, None),
    ("2026-12-15", "11:00", "WPT Championship 1C", "$10,400 WPT World Championship - Day 1C ($1M added by ClubWPT Gold)", 10400, None, None, None),
    ("2026-12-15", "12:00", "Big O $1,100", "$1,100 BIG O", 1100, None, None, None),
    ("2026-12-15", "13:00", "PLO PKO", "$3,000 PLO Progressive Bounty (PKO) $250K GTD", 3000, 250000, None, None),
    ("2026-12-15", "19:00", "NIH $500 Bounty Turbo", "$1,600 NLH $500 Bounty Turbo $100K GTD", 1600, 100000, None, None),
    ("2026-12-17", "11:00", "Seniors NLH (3 Day)", "$1,100 Seniors No Limit Hold'em Championship (3 Day) $500K GTD", 1100, 500000, None, None),
    ("2026-12-17", "11:00", "Wynn Mixed (2 Day)", "$1,600 Wynn Mixed Championship (2 Day)", 1600, None, None, None),
    ("2026-12-17", "12:00", "NLH $3,000 1A", "$3,000 No Limit Hold'em $2M GTD - Day 1A", 3000, 2000000, None, None),
    ("2026-12-17", "13:00", "NLH High Roller (2 Day)", "$25,800 No Limit Hold'em High Roller (2 Day)", 25800, None, None, None),
    ("2026-12-18", "11:00", "NLH $1,100 1A", "$1,100 No Limit Hold'em $1M GTD - Day 1A", 1100, 1000000, None, None),
    ("2026-12-18", "12:00", "PLO Double Board Bomb Pot", "$800 Pot Limit Omaha Double Board Bomb Pot", 800, None, None, None),
    ("2026-12-18", "12:00", "NLH $3,000 1B", "$3,000 No Limit Hold'em $2M GTD - Day 1B", 3000, 2000000, None, None),
    ("2026-12-18", "12:00", "Limit Omaha 8 Championship (2 Day)", "$1,600 Limit Omaha 8 Championship (2 Day)", 1600, None, None, None),
    ("2026-12-18", "12:00", "NLH $600", "$600 No Limit Hold'em $100K GTD", 600, 100000, None, None),
    ("2026-12-18", "13:00", "PLO 6-Max $10,500", "$10,500 Pot Limit Omaha 6-Max", 10500, None, None, None),
    ("2026-12-18", "13:00", "HORSE $800", "$800 HORSE", 800, None, None, None),
    ("2026-12-18", "13:00", "NLH 6-Max $10,500", "$10,500 No Limit Hold'em 6-Max", 10500, None, None, None),
    ("2026-12-18", "18:00", "NLH Turbo $100K", "$1,100 NLH Turbo $100K GTD", 1100, 100000, None, None),
    ("2026-12-18", "19:00", "NLH $1,100 1B", "$1,100 No Limit Hold'em $1M GTD - Day 1B", 1100, 1000000, None, None),
    ("2026-12-19", "11:00", "Seniors High Roller (3 Day)", "$5,000 Seniors High Roller (3 Day) $250K GTD", 5000, 250000, None, None),
    ("2026-12-19", "11:00", "NLH Mystery Bounty 1A", "$1,600 NLH Mystery Bounty $1M GTD - Day 1A", 1600, 1000000, None, None),
    ("2026-12-19", "13:00", "PLO $10,500", "$10,500 Pot Limit Omaha", 10500, None, None, None),
    ("2026-12-19", "13:00", "NLH 6-Max $3,000", "$3,000 No Limit Hold'em 6-Max $500K GTD", 3000, 500000, None, None),
    ("2026-12-19", "13:00", "TORSE Championship (2 Day)", "$1,600 TORSE Championship (2 Day)", 1600, None, None, None),
    ("2026-12-19", "18:00", "NLH 6-Max Turbo", "$600 NLH 6-Max Turbo $50K GTD", 600, 50000, None, None),
    ("2026-12-19", "19:00", "NLH Mystery Bounty 1B", "$1,600 NLH Mystery Bounty $1M GTD - Day 1B", 1600, 1000000, None, None),
    ("2026-12-20", "11:00", "NLH Mystery Bounty 1C", "$1,600 NLH Mystery Bounty $1M GTD - Day 1C", 1600, 1000000, None, None),
    ("2026-12-20", "12:00", "NLH $600", "$600 No Limit Hold'em $50K GTD", 600, 50000, None, None),
    ("2026-12-20", "13:00", "NLH 8-Max $10,500", "$10,500 No Limit Hold'em 8-Max", 10500, None, None, None),
    ("2026-12-20", "13:00", "Mixed Triple Draw $600", "$600 Mixed Triple Draw", 600, None, None, None),
    ("2026-12-20", "18:00", "5-Card PLO Turbo", "$600 5-Card PLO Turbo $50K GTD", 600, 50000, None, None),
    ("2026-12-20", "19:00", "NLH Mystery Bounty 1D", "$1,600 NLH Mystery Bounty $1M GTD - Day 1D", 1600, 1000000, None, None),
    ("2026-12-21", "12:00", "NLH $1,100", "$1,100 No Limit Hold'em $100K GTD", 1100, 100000, None, None),
    ("2026-12-21", "20:00", "NLH Turbo $50K (8)", "$600 NLH Turbo $50K GTD", 600, 50000, None, None),
]

WPT_STRUCT = {
    "n600": dict(fee=90, chips=40000, level=30, gtd=400000,
                 excerpt="Entry Fee: $600 Buy-in = $510 (Tournament Prize Pool) + $65 (Tournament Fee) + $25 (Poker Staff Service Charge) / Registration: Unlimited re-entry for each starting flight will be available until the start of level 9. / Starting Stack: Players will start with 40,000 in tournament chips."),
    "triple": dict(fee=90, chips=35000, level=30, gtd=None,
                   excerpt="Entry Fee: $600 Buy-in = $510 (Tournament Prize Pool) + $65 (Tournament Fee) + $25 (Poker Staff Service Charge) / Registration: Unlimited re-entry will be available until the start of level 9. / Starting Stack: Players will start with 35,000 in tournament chips."),
    "n800": dict(fee=105, chips=40000, level=30, gtd=1000000,
                 excerpt="Entry Fee: $800 Buy-in = $695 (Tournament Prize Pool) + $72 (Tournament Fee) + $33 (Poker Staff Service Charge) / Registration: Unlimited re-entry for each starting flight will be available until the start of level 9. / Starting Stack: Players will start with 40,000 in tournament chips."),
    "lo8": dict(fee=90, chips=35000, level=30, gtd=None,
                excerpt="Entry Fee: $600 Buy-in = $510 (Tournament Prize Pool) + $65 (Tournament Fee) + $25 (Poker Staff Service Charge) / Registration: Unlimited re-entry will be available until the start of level 9 / Starting Stack: Players will start with 35,000 in tournament chips."),
    "lo88": dict(fee=90, chips=35000, level=30, gtd=None,
                 excerpt="Entry Fee: $600 Buy-in = $510 (Tournament Prize Pool) + $65 (Tournament Fee) + $25 (Poker Staff Service Charge) / Registration: Unlimited re-entry will be available until the start of level 9 / Starting Stack: Players will start with 35,000 in tournament chips."),
    "plo1100": dict(fee=130, chips=30000, level=30, gtd=None,
                    excerpt="Entry Fee: $1,100 Buy-in = $975 (Tournament Prize Pool) + $85 (Tournament Fee) + $45 (Poker Staff Service Charge) / Registration: Unlimited re-entry will be available until the start of level 9 (approximately 5:30 p.m.). / Starting Stack: Players will start with 30,000 in tournament chips."),
    "n1600": dict(fee=170, chips=40000, level=40, gtd=1000000,
                  excerpt="Entry Fee: $1,600 Buy-in = $1,430 (Tournament Prize Pool) + $120 (Tournament Fee) + $50 (Poker Staff Service Charge) / Registration: Unlimited re-entry for each starting flight will be available until the start of level 10. / Starting Stack: Players will start with 40,000 in tournament chips."),
    "prime": dict(fee=None, chips=None, level=None, gtd=5000000,
                  excerpt="WPT Prime Championship: one entry plus one re-entry per flight permitted through level 10. (Official WPT structure PDF.)"),
    "mystery": dict(fee=None, chips=None, level=None, gtd=500000,
                    excerpt="PLO Mystery Bounty: re-entry permitted through level 10. (Official WPT structure PDF.)"),
}

WPT_FLAGS = {
    "WPT Championship 1A": "Official schedule footnote: $1M added by ClubWPT Gold, which the footnote says is not available in Nevada.",
    "WPT Championship 1B": "Official schedule footnote: $1M added by ClubWPT Gold, which the footnote says is not available in Nevada.",
    "WPT Championship 1C": "Official schedule footnote: $1M added by ClubWPT Gold, which the footnote says is not available in Nevada.",
    "Ladies NIH Championship": "Official schedule prints the event name as 'NIH' and footnotes that the Tournament Entry is $11,100 with a discounted entry for ladies. Flagged.",
    "NIH $500 Bounty Turbo": "Official schedule prints the event name as 'NIH (sic)'. Flagged.",
}

# ------------------------------------------------- Wynn Signature Series ----
# Buy-in and guarantee from the official Signature Series schedule PDF. The
# linked structures PDF contains only 'COMING SOON', so no entry rule is
# verified for any Signature Series event.
WSS = [
    ("2027-01-11", "12:00", "No Limit Hold'em Day 1A", 400, 150000),
    ("2027-01-11", "17:00", "No Limit Hold'em Day 1B", 400, 150000),
    ("2027-01-12", "12:00", "No Limit Hold'em Day 1C", 400, 150000),
    ("2027-01-12", "17:00", "No Limit Hold'em Day 1D", 400, 150000),
    ("2027-01-13", "12:00", "No Limit Hold'em Day 1E", 400, 150000),
    ("2027-01-13", "17:00", "No Limit Hold'em Day 1F", 400, 150000),
    ("2027-01-14", "11:00", "No Limit Hold'em Day 1A", 600, 250000),
    ("2027-01-15", "11:00", "No Limit Hold'em Day 1B", 600, 250000),
    ("2027-01-15", "18:00", "NLH Turbo", 200, 10000),
    ("2027-01-16", "11:00", "No Limit Hold'em Day 1C", 600, 250000),
    ("2027-01-16", "18:00", "No Limit Hold'em Day 1D", 600, 250000),
    ("2027-01-17", "12:00", "No Limit Hold'em", 400, 30000),
    ("2027-01-17", "18:00", "NLH Turbo", 200, 10000),
    ("2027-01-18", "11:00", "No Limit Hold'em Day 1A", 400, 100000),
    ("2027-01-18", "13:00", "Pot Limit Omaha", 400, None),
    ("2027-01-18", "18:00", "NLH Turbo", 200, 10000),
    ("2027-01-19", "11:00", "No Limit Hold'em Day 1B", 400, 100000),
    ("2027-01-19", "13:00", "TORSE", 400, None),
    ("2027-01-19", "18:00", "NLH Turbo", 200, 10000),
    ("2027-01-20", "11:00", "No Limit Hold'em Day 1C", 400, 100000),
    ("2027-01-20", "13:00", "Mixed Triple Draw (A-5, 2-7, Badugi)", 400, None),
    ("2027-01-20", "18:00", "NLH Turbo", 200, 10000),
    ("2027-01-21", "11:00", "No Limit Hold'em Day 1A", 800, 300000),
    ("2027-01-21", "13:00", "TOE", 400, None),
    ("2027-01-22", "11:00", "No Limit Hold'em Day 1B", 800, 300000),
    ("2027-01-22", "13:00", "BIG O", 400, None),
    ("2027-01-23", "11:00", "No Limit Hold'em Day 1C", 800, 300000),
    ("2027-01-23", "18:00", "No Limit Hold'em Day 1D", 800, 300000),
    ("2027-01-24", "12:00", "Seniors No Limit Hold'em 50+", 400, 30000),
    ("2027-01-24", "13:00", "Pot Limit Omaha Double Board Bomb Pot", 400, None),
    ("2027-01-24", "18:00", "NLH Turbo", 200, 10000),
]

# ------------------------------------------------------ Bellagio weekly -----
BELLAGIO = [
    ("Friday", "11:00", "$600 No Limit Hold'em", 600, 50, 510, 30000, 30, 8,
     "https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/blt9cf95b0e60ec253e/6af491a3a9851d75c40be840/mgm-bellagio-poker-fridays-$600-nlh.pdf",
     "The $600 Buy-In is allocated as follows: $510 to Prize Pool; $50 House Fee; $40 Voluntary Staff Gratuity. / Players may buy-in and re-enter through the end of level 8 (Including Break). / Players will start with 30,000 tournament chips, including the optional Staff Gratuity. (15,000 + 15,000) / Levels will be 30 Minutes in Length with a 12 minute break every 4 levels."),
    ("Saturday", "11:00", "No Limit Hold'em (multi-flight)", None, None, None, 40000, 30, 10,
     "https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/blt6d47974bf5a7d9b6/6af491a391a6e8e4230c9e07/mgm-bellagio-poker-saturdays-$1000-nlh.pdf",
     "Players start with 40,000 in tournament chips (20,000 + 20,000 optional). / Registration will be open until the start of Level 10. / Bellagio guarantees that the total Combined Prize Pool will be at least $50,000. / Rule 07 reads 'Of the $600 Buy-in, $510 goes to the Prize Pool, $50 is Admin Fees and $40 is optional staff gratuity' while the document heading reads 'NLH $1100 BUY-IN' and the published file name says $1000 NLH. The three statements conflict, so the buy-in and fee split are unverified for this event."),
    ("Sunday", "11:00", "$400 H.O.R.S.E.", 400, 35, 340, 30000, 30, 8,
     "https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/blt07fcf1244a6da661/6af491a339e2b4f6b76a86ad/mgm-bellagio-poker-sundays-$400-horse.pdf",
     "The $400 Buy-In is allocated as follows: $340 to Prize Pool; $35 House Fee; $25 Voluntary Staff Gratuity. / Players may buy-in and re-enter through the end of level 8 (Including Break). / Each level will last thirty (30) minutes."),
]

# ------------------------------------------------------------- helpers ------
# Tags that describe the PRIZE STRUCTURE rather than the number of entries.
# An event with one of these tags can still be a single-entry event: a bounty
# or a satellite takes one entry like any other freezeout. They are kept in the
# single-entry section and surfaced as filters, because the criterion for that
# section is the entry rule and nothing else.
PRIZE_TAGS = {"bounty", "pko", "satellite", "milestone", "title_event",
               "turbo", "ladies", "seniors", "two_day"}

# Tags that mean more than one entry can be taken. These move an event out of
# the single-entry section, because the entry rule is what that section is about.
MULTI_ENTRY_TAGS = {"multi_flight", "day1_payout", "subsequent_buy_in"}

FORMAT_NOTE = {
    "bounty": "Bounty format: part of the buy-in is returned as bounties during play.",
    "pko": "Progressive knockout: the bounty grows as the field shrinks.",
    "satellite": "Satellite: the prizes are seats in another event, not cash.",
    "milestone": "Milestone satellite: seats are awarded at set chip counts.",
    "multi_flight": "Multi-flight: more than one entry can be taken across flights.",
    "day1_payout": "Several flights advance from Day 1, so more than one entry can be taken.",
    "subsequent_buy_in": "A subsequent buy-in is allowed at the published price.",
    "reentry": "Re-entry is offered during the published re-entry window.",
    "title_event": "A title event of the series.",
    "turbo": "Turbo format: shorter levels than a standard event.",
    "ladies": "Ladies event: restricted to women.",
    "seniors": "Seniors event: restricted to players 50 and over.",
    "two_day": "Runs over two days.",
    "tag_team": "Tag-team format: a two-player team entry.",
}


def section_of(status, tags, is_restart):
    """Return (section, reason).

    The section is decided by the ENTRY RULE alone, because that is what the
    single-entry section is about. The prize structure (bounty, satellite,
    progressive knockout, team) does not change how many entries a player may
    take, so those tags stay in the single-entry section and are used as
    filters instead.

    `single`  - one entry only, confirmed from an official structure sheet.
    `other`   - more than one entry allowed, a Day 2 continuation, or an
                entry rule that is not yet confirmed.
    """
    if is_restart:
        return "other", "Day 2 or final-table continuation of an event already entered. It takes no new entry."
    if status == "UNV":
        return "other", "Entry rule not confirmed from an official structure sheet."
    if status == "RE":
        return "other", "Re-entry is offered, so more than one entry can be taken."
    if status == "MULTI":
        return "other", "The structure sheet allows more than one entry, so this is not a single-entry event."
    hits = [t for t in tags if t in MULTI_ENTRY_TAGS]
    if hits:
        return "other", " ".join(FORMAT_NOTE[t] for t in hits)
    return "single", ("Confirmed single entry: the official structure sheet contains no re-entry, rebuy, "
                      "add-on, subsequent-buy-in or multi-flight clause.")


def to_minutes(hhmm):
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def hhmm_to_h(hhmm):
    h = int(hhmm[:2]) % 12
    m = hhmm[3:]
    if h == 0:
        h = 12
    return "%d:%s %s" % (h, m, "AM" if int(hhmm[:2]) < 12 else "PM")


def sheet_url(series, sheet):
    if series == "nov":
        return SRC["dse_nov_struct"].format(sheet)
    return SRC["dse_dec_struct"].format(sheet)


def build_venetian_rows():
    rows = []
    for series, table, sched_key, struct_key in (
        ("Venetian DeepStack Extravaganza IV", DSE_NOV, "dse_nov_page", "dse_nov_struct"),
        ("Venetian DeepStack Extravaganza NYE", DSE_DEC, "dse_dec_page", "dse_dec_struct"),
    ):
        sheets = NOV_SHEETS if series.endswith("IV") else DEC_SHEETS
        for date, time, evno, sheet, name, restart in table:
            sh = sheets[sheet]
            buy = sh["buy"]
            total_fee = sh.get("total_fee", sh["fee"])
            single = sh["single"]
            if evno in sh.get("single_by_event", {}):
                single = sh["single_by_event"][evno]
            gtd = sh.get("gtd_by_event", {}).get(evno, sh["gtd"])
            tags = list(sh.get("tags", []))
            if restart:
                status = "RESTART"
                rule = "Continuation of an event already entered. No new entry is taken."
            elif single:
                status = "SE"
                rule = ("Single entry (verified): the official structure sheet for this event contains no "
                        "re-entry, rebuy, add-on, subsequent-buy-in or multi-flight clause.")
            else:
                status = "MULTI"
                rule = ("Multiple entries possible (verified): the official structure sheet states a "
                        "multi-flight or subsequent-buy-in clause. See the excerpt for the exact wording.")
            fee_pct = round(100.0 * total_fee / buy, 2) if buy else None
            rows.append({
                "series": series,
                "venue": "venetian",
                "venue_name": VENETIAN_VENUE["name"],
                "date": date,
                "start": time,
                "start_label": hhmm_to_h(time),
                "event_no": evno,
                "name": name,
                "buy_in_usd": buy,
                "single_entry_cost_usd": buy if status == "SE" else None,
                "house_fee_usd": total_fee,
                "house_fee_pct": fee_pct,
                "house_fee_note": sh.get("fee_note"),
                "prize_pool_usd": (buy - total_fee) if buy and total_fee else None,
                "reentry_allowed": (not single) if not restart else None,
                "reentry_cutoff": sh["late"] if not single else None,
                "addon_allowed": None,
                "bounty": sh.get("bounty"),
                "multi_flight": "multi_flight" in tags,
                "starting_stack_chips": sh["chips"],
                "level_minutes": sh["level"],
                "late_registration": sh["late"],
                "late_registration_time": sh["late_time"],
                "guarantee_usd": gtd,
                "guarantee_note": sh.get("gtd_note"),
                "gtd_multiple": round(gtd / buy, 1) if (gtd and buy) else None,
                "eligibility": sh.get("eligibility"),
                "format_tags": tags,
                "entry_status": status,
                "entry_rule": rule,
                "is_restart": restart,
                "structure_sheet": sheet,
                "excerpt": sh["excerpt"],
                "notes": [],
                "sources": [
                    {"label": "Official schedule", "url": SRC[sched_key]},
                    {"label": "Official structure sheet #%d" % sheet, "url": sheet_url(series, sheet)},
                ],
                "retrieved_on": VERIFIED_ON,
            })
    return rows


def build_wpt_rows():
    rows = []
    for date, time, label, name, buy, gtd, skey, lvl in WPT:
        st = WPT_STRUCT.get(skey)
        if skey and skey != "prime" and skey != "mystery":
            status = "RE"
            rule = ("Re-entry offered (verified from the official WPT structure terms): "
                    + (WPT_RE.format(lvl=lvl) if lvl else "Unlimited re-entry is stated in the event terms."))
        elif skey in ("prime", "mystery"):
            status = "RE"
            rule = ("Re-entry offered (verified from the official WPT structure terms): "
                    + st["excerpt"])
        else:
            status = "UNV"
            rule = ("Unverified: the structure section for this event was not extracted from the official "
                    "WPT structure PDF, so the entry rule is not confirmed.")
        fee = st["fee"] if st else None
        tags = ["reentry"]
        if "turbo" in label.lower():
            tags.append("turbo")
        if "bounty" in label.lower():
            tags.append("bounty")
        notes = []
        if label in WPT_FLAGS:
            notes.append(WPT_FLAGS[label])
        if "Super Gold Million" in label:
            notes.append("Official Wynn poker page: 'the Super Gold Million brings a $400 buy-in featuring a $3,000,000 guarantee!'")
        rows.append({
            "series": "WPT World Championship (Wynn)",
            "venue": "wynn",
            "venue_name": WYNN_VENUE["name"],
            "date": date,
            "start": time,
            "start_label": hhmm_to_h(time),
            "event_no": None,
            "name": name,
            "buy_in_usd": buy,
            "single_entry_cost_usd": None,
            "house_fee_usd": fee,
            "house_fee_pct": round(100.0 * fee / buy, 2) if (fee and buy) else None,
            "house_fee_note": None,
            "prize_pool_usd": (buy - fee) if (buy and fee) else None,
            "reentry_allowed": True if status == "RE" else None,
            "reentry_cutoff": ("level %d" % lvl) if (status == "RE" and lvl) else None,
            "addon_allowed": None,
            "bounty": None,
            "multi_flight": True if label.endswith(("1A", "1B", "1C", "1D", "1E", "1F")) and "NLH" in label else None,
            "starting_stack_chips": st["chips"] if st else None,
            "level_minutes": st["level"] if st else None,
            "late_registration": "Registration closes at the start of level %d" % lvl if (status == "RE" and lvl) else None,
            "late_registration_time": None,
            "guarantee_usd": gtd,
            "guarantee_note": None,
            "gtd_multiple": round(gtd / buy, 1) if (gtd and buy) else None,
            "eligibility": None,
            "format_tags": tags,
            "entry_status": status,
            "entry_rule": rule,
            "is_restart": False,
            "structure_sheet": skey,
            "excerpt": st["excerpt"] if st else None,
            "notes": notes,
            "sources": [
                {"label": "Official WPT schedule", "url": SRC["wpt_sched"]},
                {"label": "Official WPT structure / terms", "url": SRC["wpt_struct"]},
            ],
            "retrieved_on": VERIFIED_ON,
        })
    return rows


def build_wss_rows():
    rows = []
    note = ("Buy-in and guarantee from the official Wynn Signature Series schedule PDF. The linked official "
            "structures PDF was read on 2026-11-16 and contains only the text 'LAS VEGAS POKER - COMING SOON', "
            "so no entry rule is verified for this event.")
    for date, time, name, buy, gtd in WSS:
        rows.append({
            "series": "Wynn Signature Series",
            "venue": "wynn",
            "venue_name": WYNN_VENUE["name"],
            "date": date,
            "start": time,
            "start_label": hhmm_to_h(time),
            "event_no": None,
            "name": name,
            "buy_in_usd": buy,
            "single_entry_cost_usd": None,
            "house_fee_usd": None,
            "house_fee_pct": None,
            "house_fee_note": None,
            "prize_pool_usd": None,
            "reentry_allowed": None,
            "reentry_cutoff": None,
            "addon_allowed": None,
            "bounty": None,
            "multi_flight": None,
            "starting_stack_chips": None,
            "level_minutes": None,
            "late_registration": None,
            "late_registration_time": None,
            "guarantee_usd": gtd,
            "guarantee_note": None,
            "gtd_multiple": round(gtd / buy, 1) if (gtd and buy) else None,
            "eligibility": None,
            "format_tags": [],
            "entry_status": "UNV",
            "entry_rule": "Unverified: the official Wynn Signature Series structures PDF is a placeholder, so the entry rule is not confirmed.",
            "is_restart": False,
            "structure_sheet": None,
            "excerpt": None,
            "notes": [note],
            "sources": [
                {"label": "Official Signature Series schedule", "url": SRC["wss_sched"]},
                {"label": "Official Signature Series structures (placeholder)", "url": SRC["wss_struct"]},
            ],
            "retrieved_on": VERIFIED_ON,
        })
    return rows


def build_bellagio_rows():
    rows = []
    for day, time, name, buy, fee, pool, chips, level, lvl, url, excerpt in BELLAGIO:
        rows.append({
            "series": "Bellagio weekly poker room",
            "venue": "bellagio",
            "venue_name": BELLAGIO_VENUE["name"],
            "date": None,
            "weekday": day,
            "start": time,
            "start_label": hhmm_to_h(time),
            "event_no": None,
            "name": name,
            "buy_in_usd": buy,
            "single_entry_cost_usd": buy,
            "total_fee_usd": buy,
            "house_fee_usd": fee,
            "house_fee_pct": round(100.0 * fee / buy, 2) if (fee and buy) else None,
            "house_fee_note": ("The house fee is withheld from the buy-in, not added to it. The official sheet "
                               "prints the full allocation of the buy-in.") if (fee and buy) else None,
            "prize_pool_usd": pool,
            "reentry_allowed": True,
            "reentry_cutoff": "end of level %d (including break)" % lvl,
            "addon_allowed": None,
            "bounty": None,
            "multi_flight": True if day == "Saturday" else None,
            "starting_stack_chips": chips,
            "level_minutes": level,
            "late_registration": "end of level %d (including break)" % lvl,
            "late_registration_time": None,
            "guarantee_usd": 50000 if day == "Saturday" else None,
            "guarantee_note": "Guarantee of at least $50,000 combined prize pool." if day == "Saturday" else None,
            "gtd_multiple": None,
            "eligibility": None,
            "format_tags": ["reentry"] + (["multi_flight"] if day == "Saturday" else []),
            "entry_status": "RE",
            "entry_rule": "Re-entry offered (verified from the official Bellagio structure sheet).",
            "is_restart": False,
            "structure_sheet": None,
            "excerpt": excerpt,
            "notes": [],
            "sources": [{"label": "Official Bellagio structure sheet", "url": url},
                        {"label": "Bellagio poker room (official)", "url": SRC["bellagio_poker"]}],
            "recurring": True,
            "retrieved_on": VERIFIED_ON,
        })
    return rows


def build_tournaments():
    rows = build_venetian_rows() + build_wpt_rows() + build_wss_rows() + build_bellagio_rows()
    # Flag the official NYE page's 2025 date typo on the affected rows.
    for r in rows:
        if r["series"] == "Venetian DeepStack Extravaganza NYE" and r["event_no"] in NYE_DATE_TYPO_EVENTS:
            r["notes"].append("Official NYE schedule page prints the date as 'Saturday, December 26, 2025'. "
                              "The series runs December 24, 2026 - January 10, 2027, so the year is a "
                              "publication typo. 2026 is used here and the row is flagged.")
    rows.sort(key=lambda x: (x["date"] or "9999", x["start"], x["name"]))
    for i, r in enumerate(rows, 1):
        r["id"] = "t%04d" % i
        # The house fee is withheld FROM the buy-in on every official sheet
        # read here, so the money a player commits to enter is the buy-in
        # itself. `total_fee_usd` is therefore the buy-in, and the house fee is
        # a component of it, not an addition to it.
        r["total_fee_usd"] = r.get("buy_in_usd")
        r["fee_component_of_buy_in"] = True
        section, reason = section_of(r["entry_status"], r["format_tags"], r["is_restart"])
        r["section"] = section
        r["section_reason"] = reason
        r["format_note"] = " ".join(FORMAT_NOTE[t] for t in r["format_tags"] if t in FORMAT_NOTE)
        # Minimum time the player is committed to: from the printed start to the
        # printed late-registration cutoff. No official source publishes a
        # projected finish time, so this is the part of the commitment that is
        # actually stated, and it is labelled as derived.
        start_m = to_minutes(r["start"])
        cut = r.get("late_registration_time")
        if cut:
            r["minimum_commitment_min"] = to_minutes(cut) - start_m
            r["committed_until"] = cut
        else:
            r["minimum_commitment_min"] = None
            r["committed_until"] = None
        r["duration_note"] = ("No official source publishes a projected finish time for this event. The printed "
                              "late-registration cutoff is the last moment an entry can be taken and is used "
                              "here as the practical end of the registration commitment.")
    return rows


# ------------------------------------------------------------- hotels -------
HOTELS = [
    {
        "id": "venetian", "name": "The Venetian Resort Las Vegas", "venue": "venetian",
        "address": "3355 Las Vegas Blvd S, Las Vegas, NV 89109",
        "address_source": SRC["clark_county"],
        "quality": "Luxury all-suite; host of the DeepStack Extravaganza.",
        "resort_fee_usd": 55, "resort_fee_status": "verified",
        "resort_fee_note": "Official Venetian hotel terms: \"The Venetian Resort has a standard Las Vegas Resort Fee of $55 plus applicable tax per night, payable upon check-in.\"",
        "room_tax_pct": 13.38, "room_tax_status": "verified",
        "room_tax_note": "Official Venetian hotel terms: \"Daily rates do not include the applicable Clark County Room Tax of 13.38%.\" Confirmed for the same rate by the official Clark County transient lodging licence list.",
        "extra_guest_usd": 50,
        "extra_guest_note": "Official Venetian hotel terms: \"For reservations with more than 2 guests per suite, a charge of $50 is added to the daily rate for each additional guest 13 years of age or older.\"",
        "max_occupancy": None,
        "max_occupancy_note": "Not stated as a number in the official terms read. Left blank.",
        "parking_note": "Official Venetian hotel terms: \"The daily fee for registered hotel guests is $20/day, seven days a week. For non-hotel guests, the fee is $20, Monday - Thursday, and $25/day Friday - Sunday. Valet parking is $40/day.\"",
        "parking_self_guest_usd": 20, "parking_self_public_weekday_usd": 20,
        "parking_self_public_weekend_usd": 25, "parking_valet_usd": 40,
        "parking_status": "verified",
        "cancellation_note": "The official terms bill a deposit at reservation confirmation but do not publish a single cancellation deadline; the deadline depends on the booked offer. Left unverified.",
        "cancellation_deadline_hours": None, "cancellation_status": "unverified",
        "incidental_deposit_note": "Official Venetian hotel terms: \"A credit card incidental deposit of $150 per night is required upon check-in for suite charging privileges for non-Signature Suites.\"",
        "check_in": "3:00 PM", "check_out": "11:00 AM",
        "check_in_source": SRC["venetian_terms"],
        "booking_url": SRC["venetian_book"],
        "booking_label": "Official Venetian reservations",
        "poker_rate_note": "Official poker-suite page: rates \"start as low as $119 and $209\" (Venetian or Palazzo) for qualifying players, who must play six hours of cash poker or enter a $300 or larger tournament per night stayed. Quote code EPOKR25.",
        "poker_rate_usd_from": 119,
        "poker_rate_status": "verified_starting_rate",
        "sources": [
            {"label": "Official hotel terms (resort fee, 13.38% tax, parking, occupancy, deposit)", "url": SRC["venetian_terms"]},
            {"label": "Official resort fee page", "url": SRC["venetian_fee"]},
            {"label": "Official poker suite rates (EPOKR25)", "url": SRC["venetian_suite"]},
            {"label": "Official street address and room tax (Clark County licence list)", "url": SRC["clark_county"]},
        ],
    },
    {
        "id": "palazzo", "name": "The Palazzo", "venue": "venetian",
        "address": "3325 Las Vegas Blvd S, Las Vegas, NV 89109",
        "address_source": SRC["clark_county"],
        "quality": "All-suite sister tower of The Venetian; inside the same walkable complex.",
        "resort_fee_usd": 55, "resort_fee_status": "verified",
        "resort_fee_note": "Official Venetian poker-suite page states the $55 per night resort fee for \"The Venetian or The Palazzo\".",
        "room_tax_pct": 13.38, "room_tax_status": "verified",
        "room_tax_note": "Official Clark County transient lodging licence list records \"Venetian Resort Hotel Casino / Palazzo Resort Hotel Casino\" as a licensed Resort Hotel in the Primary Gaming Corridor at 13.38%.",
        "extra_guest_usd": 50,
        "extra_guest_note": "Official Venetian hotel terms: $50 per additional guest 13 years of age or older.",
        "max_occupancy": None,
        "max_occupancy_note": "Not stated as a number in the official terms read. Left blank.",
        "parking_note": "Official Venetian hotel terms: registered hotel guests $20/day self parking; non-guests $20 Mon-Thu and $25 Fri-Sun; valet $40/day.",
        "parking_self_guest_usd": 20, "parking_self_public_weekday_usd": 20,
        "parking_self_public_weekend_usd": 25, "parking_valet_usd": 40,
        "parking_status": "verified",
        "cancellation_note": "No single published cancellation deadline; depends on the booked offer. Left unverified.",
        "cancellation_deadline_hours": None, "cancellation_status": "unverified",
        "incidental_deposit_note": "Official Venetian hotel terms: $150 per night incidental deposit for suite charging privileges.",
        "check_in": "3:00 PM", "check_out": "11:00 AM",
        "check_in_source": SRC["venetian_terms"],
        "booking_url": SRC["venetian_book"],
        "booking_label": "Official Venetian reservations",
        "poker_rate_note": "Official poker-suite page: qualifying poker-player rates \"start as low as $119 and $209\" for The Venetian or The Palazzo, requiring six hours of cash play or a $300+ tournament buy-in per night stayed. Quote code EPOKR25.",
        "poker_rate_usd_from": 119,
        "poker_rate_status": "verified_starting_rate",
        "sources": [
            {"label": "Official poker suite rates and $55 fee (official)", "url": SRC["venetian_suite"]},
            {"label": "Official hotel terms (resort fee, parking, occupancy)", "url": SRC["venetian_terms"]},
            {"label": "Official street address and room tax (Clark County licence list)", "url": SRC["clark_county"]},
        ],
    },
    {
        "id": "wynn", "name": "Wynn Las Vegas", "venue": "wynn",
        "address": "3131 Las Vegas Blvd S, Las Vegas, NV 89109",
        "address_source": SRC["clark_county"],
        "quality": "Luxury; host of the WPT World Championship and the Wynn Signature Series.",
        "resort_fee_usd": 55, "resort_fee_status": "verified",
        "resort_fee_note": "Official Wynn terms: \"A daily resort fee of $55 plus tax will be added to your room account for each room night.\"",
        "room_tax_pct": 13.38, "room_tax_status": "verified",
        "room_tax_note": "Official Clark County transient lodging licence list records \"Wynn Las Vegas / Encore at Wynn Las Vegas\" as a licensed Resort Hotel in the Primary Gaming Corridor at 13.38%.",
        "extra_guest_usd": 50,
        "extra_guest_note": "Official Wynn terms: \"A $50 surcharge per night shall be added for each guest exceeding the two (2) person limit.\"",
        "max_occupancy": 4,
        "max_occupancy_note": "Official Wynn terms: \"Maximum occupancy for all standard rooms is four (4) guests. A fee of $500 per person will be applied to any room or suite in excess of maximum occupancy, up to $3,000.\"",
        "parking_note": "Official Wynn parking page: \"complimentary parking for all Wynn and Encore Resort and Tower Suite registered guests\"; \"The daily parking fee for non-registered guests is $25 per day with the first three (3) hours complimentary\"; valet $40 per day. Official Wynn terms confirm the $55 fee \"entitles you to receive complimentary self-parking for up to two vehicles\".",
        "parking_self_guest_usd": 0, "parking_self_public_weekday_usd": 25,
        "parking_self_public_weekend_usd": 25, "parking_valet_usd": 40,
        "parking_status": "verified",
        "cancellation_note": "Official Wynn terms: \"cancellations must be received at least 48 hours prior to arrival date or deposit will be forfeited\" (published offer terms).",
        "cancellation_deadline_hours": 48, "cancellation_status": "verified_offer_terms",
        "incidental_deposit_note": "Official Wynn terms: \"a credit card authorized to cover room and resort fees and tax, plus $150 a night for incidentals must be presented upon check-in\".",
        "check_in": None, "check_out": None,
        "check_in_note": "Check-in and check-out times were not stated in the official terms read. Left blank.",
        "check_in_source": SRC["wynn_terms"],
        "booking_url": SRC["wynn_poker"],
        "booking_label": "Official Wynn poker page (reserve your stay)",
        "poker_rate_note": "The official Wynn poker page offers a \"Reserve your stay\" link for WPT and Signature Series guests, but no dated rate is published as a static figure. Left blank.",
        "poker_rate_usd_from": None,
        "poker_rate_status": "unverified",
        "sources": [
            {"label": "Official Wynn terms (resort fee, parking, cancellation, occupancy, deposit)", "url": SRC["wynn_terms"]},
            {"label": "Official Wynn parking page", "url": SRC["wynn_parking"]},
            {"label": "Official Wynn poker room", "url": SRC["wynn_poker"]},
            {"label": "Official street address and room tax (Clark County licence list)", "url": SRC["clark_county"]},
        ],
    },
    {
        "id": "encore", "name": "Encore at Wynn Las Vegas", "venue": "wynn",
        "address": "3131 Las Vegas Blvd S, Las Vegas, NV 89109",
        "address_source": SRC["clark_county"],
        "quality": "All-suite tower of the Wynn resort; the WPT poker room itself is located in Encore.",
        "resort_fee_usd": 55, "resort_fee_status": "verified",
        "resort_fee_note": "Official Wynn terms apply to \"Wynn Las Vegas Resort rooms\"; the Clark County licence list records \"Wynn Las Vegas / Encore at Wynn Las Vegas\" as one licensed property.",
        "room_tax_pct": 13.38, "room_tax_status": "verified",
        "room_tax_note": "Official Clark County transient lodging licence list records the Wynn / Encore property as a licensed Resort Hotel in the Primary Gaming Corridor at 13.38%.",
        "extra_guest_usd": 50,
        "extra_guest_note": "Official Wynn terms: $50 per night for each guest exceeding the two person limit.",
        "max_occupancy": 4,
        "max_occupancy_note": "Official Wynn terms: maximum occupancy for all standard rooms is four guests.",
        "parking_note": "Official Wynn parking page: complimentary self-parking for registered Wynn and Encore resort guests; $25 per day for non-registered guests; valet $40 per day.",
        "parking_self_guest_usd": 0, "parking_self_public_weekday_usd": 25,
        "parking_self_public_weekend_usd": 25, "parking_valet_usd": 40,
        "parking_status": "verified",
        "cancellation_note": "Official Wynn terms: 48 hours before arrival (published offer terms).",
        "cancellation_deadline_hours": 48, "cancellation_status": "verified_offer_terms",
        "incidental_deposit_note": "Official Wynn terms: $150 per night incidental deposit.",
        "check_in": None, "check_out": None,
        "check_in_note": "Check-in and check-out times were not stated in the official terms read. Left blank.",
        "check_in_source": SRC["wynn_terms"],
        "booking_url": SRC["wynn_poker"],
        "booking_label": "Official Wynn poker page (reserve your stay)",
        "poker_rate_note": "The official WPT terms place the poker room in Encore. No dated rate is published as a static figure. Left blank.",
        "poker_rate_usd_from": None,
        "poker_rate_status": "unverified",
        "sources": [
            {"label": "Official Wynn terms (resort fee, parking, cancellation, occupancy)", "url": SRC["wynn_terms"]},
            {"label": "Official Wynn parking page", "url": SRC["wynn_parking"]},
            {"label": "Official WPT terms placing the poker room in Encore", "url": SRC["wpt_struct"]},
            {"label": "Official street address and room tax (Clark County licence list)", "url": SRC["clark_county"]},
        ],
    },
    {
        "id": "bellagio", "name": "Bellagio", "venue": "bellagio",
        "address": "3600 Las Vegas Blvd S, Las Vegas, NV 89109",
        "address_source": SRC["clark_county"],
        "quality": "Luxury center-Strip resort with a full poker room and published weekly structures.",
        "resort_fee_usd": 55, "resort_fee_status": "verified",
        "resort_fee_note": "Official Bellagio terms: \"A daily resort fee of $55.00 plus applicable tax will be applied to all reservations.\"",
        "room_tax_pct": 13.38, "room_tax_status": "verified",
        "room_tax_note": "Official Clark County transient lodging licence list records Bellagio as a licensed Resort Hotel in the Primary Gaming Corridor at 13.38%.",
        "extra_guest_usd": 50,
        "extra_guest_note": "Official Bellagio terms: \"There is an additional charge of $50 plus tax per occupant, per night, above 2 occupants per room.\"",
        "max_occupancy": None,
        "max_occupancy_note": "Not stated as a number in the official terms read. Left blank.",
        "parking_note": "Official MGM parking page: self-parking $20 Mon-Thu and $25 Fri-Sun, $20 per day for registered hotel guests; valet $40 per day.",
        "parking_self_guest_usd": 20, "parking_self_public_weekday_usd": 20,
        "parking_self_public_weekend_usd": 25, "parking_valet_usd": 40,
        "parking_status": "verified",
        "cancellation_note": "Official Bellagio terms: \"The first night's deposit is fully refundable provided a timely notice of cancellation is received by Room Reservations at 888.987.6667 at least 72 hours prior to the arrival date.\"",
        "cancellation_deadline_hours": 72, "cancellation_status": "verified",
        "incidental_deposit_note": "Official Bellagio terms: \"a $150 incidental amount per day\" authorisation.",
        "check_in": None, "check_out": None,
        "check_in_note": "Check-in and check-out times were not stated in the Bellagio terms read. Left blank.",
        "check_in_source": SRC["bellagio_terms"],
        "booking_url": "https://www.mgmresorts.com/en/hotels/booking.html",
        "booking_label": "Official MGM Resorts reservations",
        "poker_rate_note": "The official Bellagio poker page lists weekly tournament structures but publishes no room rate for poker players. Left blank.",
        "poker_rate_usd_from": None,
        "poker_rate_status": "unverified",
        "sources": [
            {"label": "Official Bellagio terms (resort fee, cancellation, occupancy, deposit)", "url": SRC["bellagio_terms"]},
            {"label": "Official MGM parking page", "url": SRC["mgm_parking"]},
            {"label": "Official Bellagio poker room and weekly structures", "url": SRC["bellagio_poker"]},
            {"label": "Official street address and room tax (Clark County licence list)", "url": SRC["clark_county"]},
        ],
    },
    {
        "id": "aria", "name": "ARIA Resort & Casino", "venue": "aria",
        "address": "3730 Las Vegas Blvd S, Las Vegas, NV 89109",
        "address_source": SRC["clark_county"],
        "quality": "Modern luxury with 24 poker tables and a dedicated poker-room rate line.",
        "resort_fee_usd": 55, "resort_fee_status": "verified",
        "resort_fee_note": "Official ARIA terms: \"A daily resort fee of $55.00 plus applicable tax will be applied to all reservations.\"",
        "room_tax_pct": 13.38, "room_tax_status": "verified",
        "room_tax_note": "Official Clark County transient lodging licence list records Aria Resort & Casino as a licensed Resort Hotel in the Primary Gaming Corridor at 13.38%.",
        "extra_guest_usd": 50,
        "extra_guest_note": "Official ARIA terms: \"There is an additional charge of $50 plus tax per occupant, per night, above 2 occupants per room.\"",
        "max_occupancy": None,
        "max_occupancy_note": "Not stated as a number in the official terms read. Left blank.",
        "parking_note": "Official MGM parking page: self-parking $20 Mon-Thu and $25 Fri-Sun, $20 per day for registered hotel guests; valet $40 per day.",
        "parking_self_guest_usd": 20, "parking_self_public_weekday_usd": 20,
        "parking_self_public_weekend_usd": 25, "parking_valet_usd": 40,
        "parking_status": "verified",
        "cancellation_note": "Official ARIA terms: \"The first night's deposit is fully refundable provided a timely notice of cancellation is received by Room Reservations at 866.359.7757 at least 72 hours prior to the arrival date.\"",
        "cancellation_deadline_hours": 72, "cancellation_status": "verified",
        "incidental_deposit_note": "Official ARIA terms: $150 per day incidental authorisation for Deluxe Rooms ($250 Tower Suites, $350 Sky Suites, $500 Villas).",
        "check_in": "3:00 PM", "check_out": "11:00 AM",
        "check_in_note": "Official ARIA terms: \"Check in time is 3:00 pm and check out time is 11:00 am.\"",
        "check_in_source": SRC["aria_terms"],
        "booking_url": "https://www.mgmresorts.com/en/hotels/booking.html",
        "booking_label": "Official MGM Resorts reservations",
        "poker_rate_note": "Official ARIA poker page offers \"Exclusive Room Rates for qualifying poker players\" and publishes the poker-room rate line (702.590.7232 / PokerRoomRates@aria.com). No dated rate is published as a static figure. Left blank.",
        "poker_rate_usd_from": None,
        "poker_rate_status": "unverified",
        "poker_rate_contact": "702.590.7232 / PokerRoomRates@aria.com",
        "sources": [
            {"label": "Official ARIA terms (resort fee, cancellation, check-in, occupancy, deposit)", "url": SRC["aria_terms"]},
            {"label": "Official MGM parking page", "url": SRC["mgm_parking"]},
            {"label": "Official ARIA poker room and rate line", "url": SRC["aria_poker"]},
            {"label": "Official street address and room tax (Clark County licence list)", "url": SRC["clark_county"]},
        ],
    },
    {
        "id": "caesars", "name": "Caesars Palace", "venue": "caesars",
        "address": "3570 Las Vegas Blvd S, Las Vegas, NV 89109",
        "address_source": SRC["clark_county"],
        "quality": "Center-Strip landmark; used here as a walk reference and lodging option.",
        "resort_fee_usd": None, "resort_fee_status": "unverified",
        "resort_fee_note": "No Caesars Palace resort-fee figure was confirmed from an official Caesars page in this review. Third-party sites quote $54.95 before tax, but that is not an official source, so the value is left blank.",
        "room_tax_pct": 13.38, "room_tax_status": "verified",
        "room_tax_note": "Official Clark County transient lodging licence list records Caesars Palace as a licensed Resort Hotel in the Primary Gaming Corridor at 13.38%.",
        "extra_guest_usd": None,
        "extra_guest_note": "Not confirmed from an official source. Left blank.",
        "max_occupancy": None,
        "max_occupancy_note": "Not confirmed from an official source. Left blank.",
        "parking_note": "Caesars does not publish a parking tariff on the official Caesars Palace hotel page read on 2026-11-16. Left blank.",
        "parking_self_guest_usd": None, "parking_self_public_weekday_usd": None,
        "parking_self_public_weekend_usd": None, "parking_valet_usd": None,
        "parking_status": "unverified",
        "cancellation_note": "The official Caesars Palace hotel page advertises \"FREE 48-Hour Cancellation*\" as a booking benefit. It is a headline booking-window statement, not a per-rate deadline, so it is recorded with a caveat.",
        "cancellation_deadline_hours": 48, "cancellation_status": "advertised_not_rate_specific",
        "incidental_deposit_note": "The official Caesars Palace hotel page advertises \"FREE Express Checkout\". No deposit amount was confirmed from an official source. Left blank.",
        "check_in": None, "check_out": None,
        "check_in_note": "Not confirmed from an official source. Left blank.",
        "check_in_source": "https://www.caesars.com/caesars-palace",
        "booking_url": SRC["caesars_book"],
        "booking_label": "Official Caesars Palace reservations",
        "poker_rate_note": "No official Caesars Palace poker-room rate was confirmed. Left blank.",
        "poker_rate_usd_from": None,
        "poker_rate_status": "unverified",
        "sources": [
            {"label": "Official Caesars Palace hotel page", "url": "https://www.caesars.com/caesars-palace"},
            {"label": "Official street address and room tax (Clark County licence list)", "url": SRC["clark_county"]},
        ],
    },
]

# --------------------------------------------- walking-time matrix (OSRM) ----
# One OpenStreetMap/OSRM pedestrian table request over the official street
# addresses. Durations in seconds, distances in metres. Order matches
# POINT_IDS below.
OSRM_DURATIONS = [
    [0, 359.2, 779.3, 919.4, 1658.9, 1835.6, 733.3],
    [359.2, 0, 658.9, 799.0, 1814.6, 2012.0, 909.7],
    [779.3, 658.9, 0, 319.3, 2146.6, 2432.1, 1329.8],
    [919.4, 799.0, 319.3, 0, 2284.2, 2572.2, 1469.9],
    [1658.9, 1814.6, 2146.6, 2284.2, 0, 755.8, 1183.9],
    [1835.6, 2012.0, 2432.1, 2572.2, 755.8, 0, 1187.3],
    [733.3, 909.7, 1329.8, 1469.9, 1183.9, 1187.3, 0],
]
OSRM_DISTANCES = [
    [0, 449.1, 974.3, 1146.8, 2073.7, 2290.2, 916.7],
    [449.1, 0, 823.7, 996.2, 2268.2, 2510.6, 1137.2],
    [974.3, 823.7, 0, 396.8, 2683.5, 3035.8, 1662.3],
    [1146.8, 996.2, 396.8, 0, 2852.7, 3208.3, 1834.8],
    [2073.7, 2268.2, 2683.5, 2852.7, 0, 944.7, 1479.9],
    [2290.2, 2510.6, 3035.8, 3208.3, 944.7, 0, 1479.2],
    [916.7, 1137.2, 1662.3, 1834.8, 1479.9, 1479.2, 0],
]
POINT_IDS = ["venetian", "palazzo", "wynn", "encore", "bellagio", "aria", "caesars"]
POINT_LABELS = {
    "venetian": "The Venetian Resort Las Vegas, 3355 Las Vegas Blvd S, Las Vegas, NV 89109",
    "palazzo": "The Palazzo, 3325 Las Vegas Blvd S, Las Vegas, NV 89109",
    "wynn": "Wynn Las Vegas, 3131 Las Vegas Blvd S, Las Vegas, NV 89109",
    "encore": "Encore at Wynn Las Vegas, 3131 Las Vegas Blvd S, Las Vegas, NV 89109",
    "bellagio": "Bellagio, 3600 Las Vegas Blvd S, Las Vegas, NV 89109",
    "aria": "ARIA Resort & Casino, 3730 Las Vegas Blvd S, Las Vegas, NV 89109",
    "caesars": "Caesars Palace, 3570 Las Vegas Blvd S, Las Vegas, NV 89109",
}
VENUE_POINT = {"venetian": "venetian", "wynn": "wynn", "bellagio": "bellagio",
               "aria": "aria", "caesars": "caesars"}


def google_maps_walk(a, b):
    return ("https://www.google.com/maps/dir/?api=1&origin=" +
            POINT_LABELS[a].replace(", ", ",").replace(" ", "+") +
            "&destination=" + POINT_LABELS[b].replace(", ", ",").replace(" ", "+") +
            "&travelmode=walking")


def apple_maps_walk(a, b):
    return ("https://maps.apple.com/?saddr=" + POINT_LABELS[a].replace(", ", ",").replace(" ", "%20") +
            "&daddr=" + POINT_LABELS[b].replace(", ", ",").replace(" ", "%20") +
            "&dirflg=w")


def build_walking():
    pairs = []
    for i, a in enumerate(POINT_IDS):
        for j, b in enumerate(POINT_IDS):
            if i == j:
                continue
            dur = OSRM_DURATIONS[i][j]
            pairs.append({
                "from": a,
                "to": b,
                "from_label": POINT_LABELS[a],
                "to_label": POINT_LABELS[b],
                "walk_minutes": int(-(-dur // 60)),
                "walk_seconds": dur,
                "distance_m": OSRM_DISTANCES[i][j],
                "walk_status": "computed",
                "derived": "OpenStreetMap / OSRM pedestrian route (routing.openstreetmap.de, routed-foot profile), "
                           "computed from the official street addresses of each property. No resort publishes a "
                           "walking time to its poker room, so this figure is computed rather than quoted.",
                "source": SRC["osrm_table"],
                "google_maps": google_maps_walk(a, b),
                "apple_maps": apple_maps_walk(a, b),
            })
    return {
        "verified_on": VERIFIED_ON,
        "method": ("Walking times are computed, not quoted. No Strip resort publishes a walking time from its "
                   "hotel to a poker room. One OpenStreetMap / OSRM pedestrian-routing table request over the "
                   "official street addresses returns every hotel-to-hotel and hotel-to-venue pair used here. "
                   "Each pair also carries a Google Maps and an Apple Maps walking-directions link so the "
                   "figure can be confirmed in a map application before booking."),
        "source": SRC["osrm_table"],
        "geocode_source": SRC["nominatim"],
        "address_source": SRC["clark_county"],
        "pairs": pairs,
    }


# ------------------------------------------------- dated hotel-rate log ----
def build_hotel_rates():
    """An append-only log. Each entry is one observation of one stay.

    Nothing here is inferred. The room rate, same-stay checkout total and
    nightly average stay null until an official dated quote is captured, and
    every null carries a flag explaining why.
    """
    entries = []
    for h in HOTELS:
        entries.append({
            "id": "hr-%s-2026-11-16" % h["id"],
            "hotel_id": h["id"],
            "hotel_name": h["name"],
            "observed_on": VERIFIED_ON,
            "check_in_date": None,
            "check_out_date": None,
            "nights": None,
            "occupancy_adults": 2,
            "occupancy_children": 0,
            "room_type": None,
            "room_rate_usd": None,
            "room_rate_status": "unverified",
            "room_rate_note": "No official dated room rate was confirmable. Every official booking engine on these "
                              "properties is a JavaScript application that returns no static rate table to a "
                              "plain fetch, and no resort publishes a rate card. Left blank rather than inferred.",
            "resort_fee_usd": h["resort_fee_usd"],
            "resort_fee_status": h["resort_fee_status"],
            "room_tax_pct": h["room_tax_pct"],
            "room_tax_status": h["room_tax_status"],
            "tax_note": h["room_tax_note"],
            "parking_status": h["parking_status"],
            "parking_note": h["parking_note"],
            "parking_self_guest_usd": h["parking_self_guest_usd"],
            "parking_self_public_weekday_usd": h["parking_self_public_weekday_usd"],
            "parking_self_public_weekend_usd": h["parking_self_public_weekend_usd"],
            "parking_valet_usd": h["parking_valet_usd"],
            "cancellation_deadline_hours": h["cancellation_deadline_hours"],
            "cancellation_status": h["cancellation_status"],
            "cancellation_note": h["cancellation_note"],
            "max_occupancy": h["max_occupancy"],
            "extra_guest_usd": h["extra_guest_usd"],
            "checkout_total_usd": None,
            "checkout_total_status": "unverified",
            "nightly_average_usd": None,
            "nightly_average_status": "unverified",
            "rate_timestamp": VERIFIED_ON,
            "rate_timestamp_note": "Timestamp of the read of the official fee, tax, parking and cancellation terms "
                                   "that this row records. No dated room rate was observed on that date.",
            "sources": h["sources"],
        })
    return {
        "verified_on": VERIFIED_ON,
        "log_format": ("Append-only. One row per observation of one stay, never an overwrite of a previous row. "
                       "Each row records the room rate, the same-stay checkout total, the nightly average, the "
                       "mandatory resort fee and tax, parking, the cancellation deadline, occupancy and the rate "
                       "timestamp, each with its own verification flag."),
        "comparison_rule": ("Compare like for like: same check-in and check-out dates, same occupancy, same room "
                            "type, and the same resort-fee and tax treatment. Rows whose check-in and check-out "
                            "dates are blank cannot be compared on rate and are shown for their fee terms only."),
        "entries": entries,
    }


# ------------------------------------------------------------ schedule ------
def build_schedule(rows):
    """One primary and one conditional fallback per day.

    Primary = the single-entry event with the highest confirmed guarantee on
    that day, ties broken by the lower total fee and then the earlier start.
    Ranking happens only when both the total fee and the guarantee are
    confirmed, which is the case for every Venetian sheet read. A fallback is
    only listed when the day has a second qualifying event; a fallback that
    starts after the primary would overlap it is dropped.
    """
    by_day = {}
    for r in rows:
        if r["is_restart"]:
            continue
        if not r["guarantee_usd"] or not r["house_fee_usd"]:
            continue
        by_day.setdefault(r["date"], []).append(r)

    # Preference order for the primary: a confirmed single-entry freezeout
    # first, then a re-entry format, then anything else with a confirmed fee
    # and guarantee. Within each tier the higher confirmed guarantee wins.
    TIER = {"SE": 0, "RE": 1, "MULTI": 2, "UNV": 3}

    def overlaps(primary, cand):
        """Does the candidate start inside the primary's registration window?

        The late-registration cutoff is the last moment a second entry can be
        taken, so it is the practical overlap test: a candidate that starts
        before the primary does not conflict, and one that starts after the
        cutoff does not conflict.
        """
        cut = primary.get("late_registration_time")
        if not cut:
            return False
        if cand["start"] < primary["start"]:
            return False
        return cand["start"] < cut

    days = []
    for date in sorted(by_day):
        evs = sorted(by_day[date], key=lambda e: (e["start"], e["name"]))
        ranked = sorted(
            evs,
            key=lambda e: (0 if e["section"] == "single" else 1,
                           -e["guarantee_usd"],
                           TIER.get(e["entry_status"], 3),
                           e["house_fee_usd"], e["start"], e["name"]),
        )
        primary = ranked[0]
        fallback = None
        # Prefer a fallback that starts after the primary's commitment ends;
        # fall back to an earlier-starting alternative only if there is no
        # later option.
        later = [c for c in ranked[1:] if not overlaps(primary, c) and c["start"] > primary["start"]]
        earlier = [c for c in ranked[1:] if not overlaps(primary, c) and c["start"] <= primary["start"]]
        if later:
            fallback = later[0]
        elif earlier:
            fallback = earlier[0]
        entry = {"date": date, "primary": brief(primary), "fallback": None,
                 "all_single_entry": [brief(e) for e in evs if e["section"] == "single"],
                 "all_events": [brief(e) for e in evs],
                 "notes": []}
        if primary["section"] != "single":
            entry["notes"].append(
                "No confirmed single-entry freezeout event with a published fee and guarantee was published for "
                "this date. The primary below is the best published option and its entry format is labelled.")
        if fallback:
            fb = brief(fallback)
            fb["fallback_basis"] = (
                "Same-day alternative with a confirmed fee and guarantee that does not overlap the primary's "
                "registration window. Entry format: %s. %s" % (fallback["entry_status"], fallback["section_reason"]))
            entry["fallback"] = fb
        else:
            entry["notes"].append(
                "No non-overlapping alternative with a confirmed fee and guarantee was published for this date.")
        days.append(entry)
    return {
        "verified_on": VERIFIED_ON,
        "days": days,
        "method": ("Each day lists one primary event and, where a second event exists with a confirmed fee and "
                   "guarantee that does not overlap the primary's registration window, one conditional fallback. "
                   "A confirmed single-entry event is always preferred as the primary; the fallback may be a "
                   "re-entry, multi-flight or unverified format and is labelled with its entry status. Ranking "
                   "happens only after the total fee and the guarantee are confirmed from an official structure "
                   "sheet. Restart rows (Day 2 and final-table continuations) are never offered as primary "
                   "events because they take no new entry."),
        "overlap_rule": ("The overlap test uses the printed late-registration cutoff, the last moment a second "
                         "entry can be taken. No official source publishes a projected finish time, so a "
                         "single-day event that runs past its cutoff could still overlap a later start; the "
                         "late-registration cutoff is the published and practical proxy."),
        "walking_note": ("Venetian to Wynn is the only inter-venue walk that matters for these days and is "
                         "computed at 13 minutes; both venues are also used on the same calendar days during the "
                         "WPT Championship. See the walking-time table for the full matrix."),
    }


def brief(r):
    return {
        "id": r["id"],
        "start": r["start"],
        "start_label": r["start_label"],
        "series": r["series"],
        "venue": r["venue"],
        "venue_name": r["venue_name"],
        "name": r["name"],
        "buy_in_usd": r["buy_in_usd"],
        "house_fee_usd": r["house_fee_usd"],
        "house_fee_pct": r["house_fee_pct"],
        "total_fee_usd": r["total_fee_usd"],
        "fee_component_of_buy_in": r["fee_component_of_buy_in"],
        "guarantee_usd": r["guarantee_usd"],
        "gtd_multiple": r["gtd_multiple"],
        "late_registration": r["late_registration"],
        "late_registration_time": r["late_registration_time"],
        "committed_until": r.get("committed_until"),
        "minimum_commitment_min": r.get("minimum_commitment_min"),
        "starting_stack_chips": r["starting_stack_chips"],
        "level_minutes": r["level_minutes"],
        "entry_status": r["entry_status"],
        "section": r["section"],
        "section_reason": r["section_reason"],
        "format_tags": r["format_tags"],
        "source": r["sources"][-1]["url"],
        "source_label": r["sources"][-1]["label"],
    }


# ------------------------------------------------------------- venues ------
def build_venues(rows):
    out = []
    for v in VENUES:
        mine = [r for r in rows if r["venue"] == v["id"]]
        se = [r for r in mine if r["entry_status"] == "SE"]
        out.append({
            "id": v["id"],
            "name": v["name"],
            "address": v["address"],
            "lat": v["lat"],
            "lon": v["lon"],
            "poker_room": v["poker_room"],
            "event_count": len(mine),
            "single_entry_count": len(se),
            "earliest_date": min([r["date"] for r in mine if r["date"]] or [None]),
            "latest_date": max([r["date"] for r in mine if r["date"]] or [None]),
            "series": sorted({r["series"] for r in mine}),
            "sources": v["sources"],
        })
    return out


# -------------------------------------------------------- source registry ---
def build_registry():
    """Machine-readable registry of every official URL, for change monitoring."""
    reg = []
    seen = set()

    def add(key, url, label, kind, cadence="daily"):
        if url in seen:
            return
        seen.add(url)
        reg.append({"key": key, "url": url, "label": label, "kind": kind, "cadence": cadence})

    add("dse_nov_page", SRC["dse_nov_page"], "Venetian DeepStack Extravaganza IV schedule", "schedule")
    add("dse_dec_page", SRC["dse_dec_page"], "Venetian DeepStack Extravaganza NYE schedule", "schedule")
    for n in range(1, 38):
        add("dse_nov_structure_%d" % n, SRC["dse_nov_struct"].format(n),
            "Venetian DSE November structure sheet %d" % n, "structure")
    for n in range(1, 16):
        add("dse_dec_structure_%d" % n, SRC["dse_dec_struct"].format(n),
            "Venetian DSE NYE structure sheet %d" % n, "structure")
    add("wpt_sched", SRC["wpt_sched"], "Wynn WPT World Championship schedule", "schedule")
    add("wpt_struct", SRC["wpt_struct"], "Wynn WPT World Championship structures", "structure")
    add("wss_sched", SRC["wss_sched"], "Wynn Signature Series schedule", "schedule")
    add("wss_struct", SRC["wss_struct"], "Wynn Signature Series structures", "structure")
    add("wynn_daily_poster", SRC["wynn_daily_poster"], "Wynn daily tournament poster", "daily")
    add("wynn_daily_struct", SRC["wynn_daily_struct"], "Wynn daily tournament structures", "daily")
    add("wynn_poker", SRC["wynn_poker"], "Wynn Las Vegas poker room", "daily")
    add("bellagio_poker", SRC["bellagio_poker"], "Bellagio poker room", "daily")
    add("bellagio_fri", SRC["bellagio_fri"], "Bellagio Friday $600 NLH structure", "structure")
    add("bellagio_sat", SRC["bellagio_sat"], "Bellagio Saturday NLH structure", "structure")
    add("bellagio_sun", SRC["bellagio_sun"], "Bellagio Sunday $400 HORSE structure", "structure")
    add("venetian_poker", SRC["venetian_poker"], "Venetian poker room", "daily")
    add("aria_poker", SRC["aria_poker"], "ARIA poker room", "daily")
    add("venetian_terms", SRC["venetian_terms"], "Venetian hotel terms", "hotel", "weekly")
    add("venetian_fee", SRC["venetian_fee"], "Venetian resort fee", "hotel", "weekly")
    add("venetian_suite", SRC["venetian_suite"], "Venetian poker suite rates", "hotel", "weekly")
    add("wynn_terms", SRC["wynn_terms"], "Wynn offer terms", "hotel", "weekly")
    add("wynn_parking", SRC["wynn_parking"], "Wynn parking policy", "hotel", "weekly")
    add("bellagio_terms", SRC["bellagio_terms"], "Bellagio hotel terms", "hotel", "weekly")
    add("aria_terms", SRC["aria_terms"], "ARIA hotel terms", "hotel", "weekly")
    add("mgm_parking", SRC["mgm_parking"], "MGM Resorts parking rates", "hotel", "weekly")
    add("clark_county", SRC["clark_county"], "Clark County transient lodging licences and tax rates", "hotel", "monthly")
    return {
        "verified_on": VERIFIED_ON,
        "note": ("Every official URL this project depends on, with the kind of document it is and how often it "
                 "should be re-checked. scripts/monitor_sources.py fetches each URL, hashes the body and writes "
                 "a change flag to data/source_changes.json when a body differs from the stored baseline."),
        "sources": reg,
    }


def main():
    rows = build_tournaments()
    venues = build_venues(rows)
    with open(os.path.join(DATA, "tournaments.json"), "w") as f:
        json.dump({"verified_on": VERIFIED_ON, "rows": rows, "sources": SRC}, f, indent=1)
    with open(os.path.join(DATA, "venues.json"), "w") as f:
        json.dump({"verified_on": VERIFIED_ON, "venues": venues}, f, indent=1)
    with open(os.path.join(DATA, "walking.json"), "w") as f:
        json.dump(build_walking(), f, indent=1)
    with open(os.path.join(DATA, "hotel_rates.json"), "w") as f:
        json.dump(build_hotel_rates(), f, indent=1)
    with open(os.path.join(DATA, "schedule.json"), "w") as f:
        json.dump(build_schedule(rows), f, indent=1)
    with open(os.path.join(DATA, "source_registry.json"), "w") as f:
        json.dump(build_registry(), f, indent=1)

    hotels = []
    for h in HOTELS:
        h = dict(h)
        h["true_cost_per_night_usd"] = None
        h["true_cost_status"] = "unverified"
        h["true_cost_note"] = ("A true nightly cost is only computed when a date-specific room rate is also "
                               "confirmed. The mandatory resort fee and the Clark County room tax are confirmed "
                               "for this property, so the tax-inclusive fee component is shown, but no dated room "
                               "rate was confirmable, so the total is left blank rather than estimated.")
        fee = h["resort_fee_usd"]
        tax = h["room_tax_pct"]
        if fee is not None and tax is not None:
            h["tax_inclusive_resort_fee_usd"] = round(fee * (1 + tax / 100.0), 2)
            h["tax_inclusive_resort_fee_note"] = ("$%s resort fee plus the %s%% Clark County room tax, as published "
                                                  "by the official terms for this property." % (fee, tax))
        else:
            h["tax_inclusive_resort_fee_usd"] = None
            h["tax_inclusive_resort_fee_note"] = "Not computed: the resort fee for this property is unverified."
        hotels.append(h)
    with open(os.path.join(DATA, "hotels.json"), "w") as f:
        json.dump({
            "verified_on": VERIFIED_ON,
            "rows": hotels,
            "method": ("True nightly cost is computed only when a date-specific room rate, the mandatory resort "
                       "fee, and the property-specific room tax are all verified. The Clark County room tax of "
                       "13.38% is confirmed from the official Clark County transient lodging licence list for "
                       "every property below, and the resort fee is confirmed from each property's own official "
                       "terms except Caesars Palace. No date-specific room rate was confirmable from an "
                       "official source, so every true nightly total is blank and flagged in data/hotel_rates.json "
                       "rather than estimated."),
            "tax_source": SRC["clark_county"],
        }, f, indent=1)

    counts = {}
    for r in rows:
        counts[r["entry_status"]] = counts.get(r["entry_status"], 0) + 1
    print("tournament rows:", len(rows), counts)
    for s in sorted({r["series"] for r in rows}):
        print("  ", s, sum(1 for r in rows if r["series"] == s))
    print("venues:", len(venues), "| hotels:", len(hotels))


if __name__ == "__main__":
    main()
