#!/usr/bin/env python3
"""Builds data/*.json from the verified rows below.

Rules used in this file (the "no hallucination" rules):

1. Every row carries at least one official source URL (venue or operator domain).
2. A value is recorded only when it is printed on an official source that was
   fetched and read. Otherwise the value is null and the row is flagged.
3. Entry-rule fields (single entry, re-entry, add-on, fee) are stored
   separately, each with the verbatim source excerpt, the source URL, and the
   date the source was retrieved.
4. Finish times are NOT published on any official source, so the schedule
   overlap check uses only official start times and official late-registration
   close times.

Run:  python3 scripts/build_data.py
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
os.makedirs(DATA, exist_ok=True)

CHECKED_ON = "2026-11-16"

# ---------------------------------------------------------------------------
# Official source URLs. Every URL below was fetched and read on 2026-11-16
# unless the note says otherwise.
# ---------------------------------------------------------------------------
SRC = {
    "dse_nov_sched": "https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/dse-nov-2026-schedule.pdf",
    "dse_nov_page": "https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html",
    "dse_dec_page": "https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-dec-2026.html",
    "dse_nov_struct": "https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_{}.pdf",
    "dse_dec_struct": "https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_dec_2026-structure_{}.pdf",
    "wpt_sched": "https://cdn.wynnresorts.com/image/upload/v1757097329/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Schedule.pdf",
    "wpt_struct": "https://cdn.wynnresorts.com/image/upload/v1750864036/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Structures.pdf",
    "wss_sched": "https://cdn.wynnresorts.com/image/upload/v1753296112/visitwynn_pdfs_files/Poker/Wynn%20Signature%20Series/Wynn_Signature_Series_Schedule.pdf",
    "wynn_poker": "https://www.wynnlasvegas.com/casino/poker",
    "venetian_fee": "https://www.venetianlasvegas.com/resort/resort-fee.html",
    "venetian_terms": "https://www.venetianlasvegas.com/legal/hotel-terms-and-conditions.html",
    "venetian_poker_suite": "https://www.venetianlasvegas.com/resort/casino/poker/suite-rates.html",
    "wynn_terms": "https://www.wynnlasvegas.com/terms-and-conditions/848671",
    "caesars_disclaimer": "https://www.caesars.com/corporate/disclaimer",
}

# Venues. A venue owns one or more series and one or more nearby hotels.
VENUES = [
    {"id": "venetian", "name": "The Venetian Resort",
     "series": ["Venetian DeepStack Extravaganza IV", "Venetian DeepStack Extravaganza NYE"],
     "address": "3355 S Las Vegas Blvd, Las Vegas, NV (official Venetian site)",
     "poker_room_note": "Host of the DeepStack Extravaganza series. Poker room page: venetianlasvegas.com poker section.",
     "sources": [{"label": "DeepStack IV official event page", "url": SRC["dse_nov_page"]},
                 {"label": "DeepStack NYE official event page", "url": SRC["dse_dec_page"]}]},
    {"id": "wynn", "name": "Wynn Las Vegas",
     "series": ["Wynn WPT World Championship", "Wynn Signature Series"],
     "address": "3131 S Las Vegas Blvd, Las Vegas, NV (official Wynn site)",
     "poker_room_note": "Host of the WPT World Championship and the Wynn Signature Series. The official schedule prints wynnpoker.com and (702) 770-7654.",
     "sources": [{"label": "Wynn poker room (official)", "url": SRC["wynn_poker"]},
                 {"label": "WPT World Championship schedule (official PDF)", "url": SRC["wpt_sched"]}]},
]

SERIES_VENUE = {}
for _v in VENUES:
    for _s in _v["series"]:
        SERIES_VENUE[_s] = _v["id"]

# ---------------------------------------------------------------------------
# Verified facts read from each Venetian DeepStack Extravaganza IV structure
# sheet. Every sheet below was fetched and read on 2026-11-16.
#
#   sheet -> dict(
#     events        = event numbers the sheet covers (as printed on the sheet)
#     status        = SE    (single entry: sheet read, no re-entry, rebuy,
#                            add-on or flight clause anywhere on it)
#                     MULTI (multi-flight sheet carrying the Day-2 bagging
#                            clause, which leaves a second entry open)
#                     RE    (sheet offers re-entry)
#                     FLAG  (wording implies a second buy-in but is not explicit)
#     fee_usd       = house fee withheld from the buy-in, as printed
#     fee_excerpt   = verbatim fee sentence from the sheet
#     stack         = starting chips
#     level_min     = level length in minutes, as printed
#     reg_close     = late-registration close clock time, as printed
#     guarantee     = guarantee printed on the sheet (None if not printed)
#     guarantee_note= how the guarantee is defined, when the sheet says
#     rule_excerpt  = the sentence that decides the entry status
#   )
# ---------------------------------------------------------------------------
NO_REENTRY_LINE = ("No re-entry, rebuy, add-on or flight clause appears anywhere on this official "
                   "structure sheet. The Venetian sheet does not print an explicit "
                   "\"no re-entry\" sentence, so this is an absence-of-clause finding, not a written "
                   "guarantee. Confirm with the poker room before you rely on it.")
BAG_CLAUSE = ("Any player who bags chips for Day 2 may not play a subsequent flight.")
BAG_NOTE = ("Multi-flight sheet. Clause 08 restricts only players who bag chips for Day 2; it does "
            "not say whether a player who busts may enter a later flight. That leaves a second "
            "entry open, so this is not counted as single entry.")

DSE4_SHEETS = {
 1: dict(events="09, 11, 13, 15, 21, 22, 23, 25, 60, 61, 62, and 64", status="SE",
    buy=200, fee_usd=40, stack=25000, level_min=30, reg_close="9:40 PM", guarantee=8000,
    start="5:10 PM", gtd_note="Guarantee includes bounties ($50 per elimination).",
    fee_excerpt="$40 of the $200 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $160 of every $200 Buy In."),
 2: dict(events="07", status="MULTI", buy=400, fee_usd=70, stack=40000, level_min=40,
    reg_close="5:55 PM", guarantee=75000, start="11:10 AM", gtd_note=None,
    fee_excerpt="$70 of the $400 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $330 of every $400 Buy In."),
 3: dict(events="19", status="MULTI", buy=400, fee_usd=70, stack=40000, level_min=40,
    reg_close="5:55 PM", guarantee=75000, start="11:10 AM", gtd_note=None,
    fee_excerpt="$70 of the $400 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $330 of every $400 Buy In."),
 4: dict(events="59", status="MULTI", buy=600, fee_usd=95, stack=40000, level_min=40,
    reg_close="5:55 PM", guarantee=150000, start="11:10 AM", gtd_note=None,
    fee_excerpt="$95 of the $600 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $505 of every $600 Buy In. On Day 1A only, players who register before the start of the event (11:10 a.m.), will receive a $20 discount on house fees for a total buy in of $580 instead of $600."),
 5: dict(events="02 and 12", status="SE", buy=300, fee_usd=58, stack=40000, level_min=30,
    reg_close="4:55 PM", guarantee=10000, start="11:10 AM", gtd_note=None,
    fee_excerpt="$58 of the $300 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $242 of every $300 Buy In."),
 6: dict(events="10", status="SE", buy=400, fee_usd=65, stack=40000, level_min=30,
    reg_close="4:55 PM", guarantee=15000, start="11:10 AM", gtd_note=None,
    fee_excerpt="$65 of the $400 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $335 of every $400 Buy In."),
 7: dict(events="14, 28, and 63", status="SE", buy=600, fee_usd=90, stack=40000, level_min=30,
    reg_close="4:55 PM", guarantee=None, start="11:10 AM",
    gtd_note="Sheet prints: Guarantee $30,000 for Event #14 and #63; Guarantee $40,000 for Event #28.",
    fee_excerpt="$90 of the $600 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $510 of every $600 Buy In."),
 8: dict(events="18 and 58", status="FLAG", buy=200, fee_usd=40, stack=25000, level_min=30,
    reg_close="9:40 PM", guarantee=20000, start="5:10 PM",
    gtd_note="Guarantee includes bounties ($50 per elimination).",
    fee_excerpt="$40 of the $200 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $160 of every $200 Buy In.",
    rule_excerpt="PokerAtlas PRO players will receive a twenty ($20) rake discount on their initial $200 buy in only, for a total buy in of $180 instead of $200. ... All subsequent buy in's after the initial buy in will be $200."),
 9: dict(events="01 (Days B and D)", status="MULTI", buy=300, fee_usd=60, stack=30000, level_min=30,
    reg_close="8:40 PM", guarantee=75000, start="5:10 PM", gtd_note=None,
    fee_excerpt="$60 of the $300 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $240 of every $300 Buy In."),
 10: dict(events="01 (Days A and C)", status="MULTI", buy=300, fee_usd=60, stack=30000, level_min=40,
    reg_close="3:40 PM", guarantee=75000, start="11:10 AM", gtd_note=None,
    fee_excerpt="$60 of the $300 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $240 of every $300 Buy In."),
 11: dict(events="16, 30, and 54", status="SE", buy=600, fee_usd=90, stack=40000, level_min=30,
    reg_close="4:55 PM", guarantee=None, start="11:10 AM",
    gtd_note="Sheet prints: $30,000 Event #16, $40,000 Event #30, $50,000 Event #54, each (prize pool + total bounties). Bounty is $200 per elimination, rising to $500 once in the money.",
    fee_excerpt="$90 of the $600 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $510 of every $600 Buy In."),
 12: dict(events="26 (Days A, C, E)", status="MULTI", buy=800, fee_usd=110, stack=40000, level_min=40,
    reg_close="3:40 PM", guarantee=500000, start="11:10 AM", gtd_note=None,
    fee_excerpt="$110 of the $800 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $690 of every $800 Buy In."),
 13: dict(events="26 (Days B, D)", status="MULTI", buy=800, fee_usd=110, stack=40000, level_min=30,
    reg_close="8:40 PM", guarantee=500000, start="5:10 PM", gtd_note=None,
    fee_excerpt="$110 of the $800 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $690 of every $800 Buy In."),
 14: dict(events="26 (Day F, Turbo)", status="MULTI", buy=800, fee_usd=110, stack=40000, level_min=20,
    reg_close="7:25 PM", guarantee=500000, start="5:10 PM", gtd_note=None,
    fee_excerpt="$110 of the $800 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $690 of every $800 Buy In."),
 15: dict(events="29, 31, 34, 38, 42, 50, 51, 53, and 55", status="SE", buy=300, fee_usd=50,
    stack=25000, level_min=30, reg_close="9:40 PM", guarantee=15000, start="5:10 PM",
    gtd_note="Guarantee includes bounties ($100 per elimination).",
    fee_excerpt="$50 of the $300 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $250 of every $300 Buy In."),
 16: dict(events="36", status="SE", buy=800, fee_usd=100, stack=40000, level_min=30,
    reg_close="4:55 PM", guarantee=75000, start="11:10 AM",
    gtd_note="Guarantee includes bounties ($200 per elimination, $500 once in the money).",
    fee_excerpt="$100 of the $800 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $700 of every $800 Buy In."),
 17: dict(events="24 and 32", status="SE", buy=600, fee_usd=90, stack=40000, level_min=30,
    reg_close="3:55 PM", guarantee=40000, start="10:10 AM",
    gtd_note="Eligibility: must be 50+. Sheet: any player who buys into this event that is not 50+ years of age will not be entitled to any prize money or a refund of their buy in.",
    fee_excerpt="$90 of the $600 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $510 of every $600 Buy In."),
 18: dict(events="03, 04, and 05", status="SE", buy=200, fee_usd=35, stack=30000, level_min=None,
    reg_close="12:25 PM", guarantee=None, start="10:10 AM", gtd_note=None,
    level_note="Sheet prints: Level Duration 20/15 minutes (levels 1-6 at 20 minutes, levels 7-28 at 15 minutes).",
    fee_excerpt="$35 of the $200 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $165 of every $200 Buy In."),
 20: dict(events="49", status="MULTI", buy=1100, fee_usd=140, stack=40000, level_min=40,
    reg_close="4:55 PM", guarantee=300000, start="10:10 AM",
    gtd_note="Eligibility: must be 50+. Sheet: any player who buys into this event that is not 50+ years of age will not be entitled to any prize money or a refund of their buy in.",
    fee_excerpt="$140 of the $1,100 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $960 of every $1,100 Buy In."),
 21: dict(events="47 (Day 1A)", status="MULTI", buy=2200, fee_usd=225, stack=40000, level_min=40,
    reg_close="4:55 PM", guarantee=1000000, start="10:10 AM", gtd_note=None,
    fee_excerpt="$225 of the $2,200 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $1,975 of every $2,200 Buy In."),
 22: dict(events="20", status="SE", buy=300, fee_usd=58, stack=30000, level_min=30,
    reg_close="4:40 PM", guarantee=10000, start="12:10 PM",
    gtd_note="Pot Limit Omaha, Double Board Bomb Pot. Plays 8-handed, pays 12.5% of the field.",
    fee_excerpt="$58 of the $300 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $242 of every $300 Buy In."),
 23: dict(events="57", status="SE", buy=600, fee_usd=90, stack=30000, level_min=30,
    reg_close="4:40 PM", guarantee=25000, start="12:10 PM",
    gtd_note="Pot Limit Omaha, Double Board Bomb Pot. Plays 8-handed, pays 12.5% of the field.",
    fee_excerpt="$90 of the $600 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $510 of every $600 Buy In."),
 26: dict(events="17", status="SE", buy=400, fee_usd=60, stack=30000, level_min=30,
    reg_close="4:40 PM", guarantee=15000, start="12:10 PM",
    gtd_note="Guarantee includes bounties ($100 per elimination).",
    fee_excerpt="$60 of the $400 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $340 of every $400 Buy In."),
 27: dict(events="40", status="SE", buy=600, fee_usd=90, stack=30000, level_min=30,
    reg_close="4:40 PM", guarantee=25000, start="12:10 PM",
    gtd_note="Guarantee includes bounties ($200 per elimination).",
    fee_excerpt="$90 of the $600 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $510 of every $600 Buy In."),
 28: dict(events="27", status="SE", buy=600, fee_usd=90, stack=30000, level_min=30,
    reg_close="4:40 PM", guarantee=25000, start="12:10 PM",
    gtd_note="Big O. Plays 8-handed, pays 12.5% of the field.",
    fee_excerpt="$90 of the $600 Buy-In is withheld for house fees (Rake + Staff). Prize pool consists of $510 of every $600 Buy In."),
 29: dict(events="06", status="SE", buy=200, fee_usd=40, stack=30000, level_min=30,
    reg_close="3:40 PM", guarantee=None, start="11:10 AM", gtd_note=None,
    fee_excerpt="$40 of the $200 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $160 of every $200 Buy In."),
 30: dict(events="08", status="SE", buy=200, fee_usd=40, stack=25000, level_min=30,
    reg_close="9:40 PM", guarantee=8000, start="5:10 PM",
    gtd_note="Progressive Knock-Out (PKO). Guarantee includes bounties; each player starts as a $50 bounty.",
    fee_excerpt="$40 of the $200 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $160 of every $200 Buy In."),
 31: dict(events="35", status="SE", buy=600, fee_usd=80, stack=40000, level_min=30,
    reg_close="2:40 PM", guarantee=10000, start="10:10 AM",
    gtd_note="LIPS Poker Jingle Tag Team. Teams are Female/Female or Female/Male and must rotate players every level.",
    fee_excerpt="$80 of the $600 Buy-In is withheld for house fees (Rake + Staff). $10 of the $600 Buy In will be withheld as a flat fee for Vegas Connected, INC, DBA Ladies International Poker Series (LIPS). Prize pool consists of $510 of every $600 Buy In."),
 32: dict(events="39", status="SE", buy=800, fee_usd=90, stack=40000, level_min=40,
    reg_close="4:55 PM", guarantee=40000, start="10:10 AM",
    gtd_note="LIPS Ladies, 2-day event with a single Day 1. Eligibility: must be female 21+.",
    fee_excerpt="$90 of the $800 Buy-In is withheld for house fees (Rake + Staff). $20 of the $800 Buy In will be withheld as a flat fee for Vegas Connected, INC, DBA Ladies International Poker Series (LIPS). Prize pool consists of $690 of every $800 Buy In."),
 33: dict(events="43", status="SE", buy=600, fee_usd=80, stack=40000, level_min=30,
    reg_close="4:55 PM", guarantee=30000, start="11:10 AM",
    gtd_note="LIPS Kings and Queens Bounty, open to all players. Guarantee includes bounties ($200 per elimination).",
    fee_excerpt="$80 of the $600 Buy-In is withheld for house fees (Rake + Staff). $10 of the $600 Buy In will be withheld as a flat fee for Vegas Connected, INC, DBA Ladies International Poker Series (LIPS). Prize pool consists of $510 of every $600 Buy In."),
 34: dict(events="52", status="SE", buy=1100, fee_usd=130, stack=40000, level_min=30,
    reg_close="4:55 PM", guarantee=75000, start="11:10 AM",
    gtd_note="Progressive Knock-Out (PKO). Guarantee includes bounties; each player starts as a $200 bounty.",
    fee_excerpt="$130 of the $1,100 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $970 of every $1,100 Buy In."),
 35: dict(events="56 (Days A, C, E)", status="MULTI", buy=1100, fee_usd=140, stack=40000, level_min=40,
    reg_close="4:55 PM", guarantee=500000, start="10:10 AM", gtd_note=None,
    fee_excerpt="$140 of the $1,100 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $960 of every $1,100 Buy In. On Day 1A, players who register before the start of the event (10:10 a.m.) will receive a forty ($40) discount on house fees for a total buy in of $1,060 instead of $1,100."),
 36: dict(events="56 (Days B, D)", status="MULTI", buy=1100, fee_usd=140, stack=40000, level_min=30,
    reg_close="11:10 PM", guarantee=500000, start="6:10 PM", gtd_note=None,
    fee_excerpt="$140 of the $1,100 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $960 of every $1,100 Buy In. On Day 1B, players who register before the start of the event (6:10 PM.) will receive a forty ($40) discount on house fees for a total buy in of $1,060 instead of $1,100."),
 37: dict(events="47 (Day 1B)", status="MULTI", buy=2200, fee_usd=225, stack=40000, level_min=30,
    reg_close="11:10 PM", guarantee=1000000, start="6:10 PM", gtd_note=None,
    fee_excerpt="$225 of the $2,200 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $1,975 of every $2,200 Buy In."),
}

# Venetian DeepStack Extravaganza NYE structure sheets read on 2026-11-16.
NYE_SHEETS = {
 1: dict(events="01, 03, and 17", status="SE", buy=400, fee_usd=65, stack=30000, level_min=30,
    reg_close="3:40 PM", guarantee=15000, start="11:10 AM", gtd_note=None,
    fee_excerpt="$65 of the $400 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $335 of every $400 Buy In."),
 2: dict(events="02, 04, 13, 22, 26, 29, and 32", status="FLAG", buy=200, fee_usd=40, stack=25000,
    level_min=30, reg_close="9:40 PM", guarantee=8000, start="5:10 PM",
    gtd_note="Guarantee includes bounties ($50 per elimination).",
    fee_excerpt="$40 of the $200 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $160 of every $200 Buy In. For Event #29 only, any player who shows their CES badge at the time of registration will receive a $20 discount on house fees for a total buy in of $180 instead of $200.",
    rule_excerpt="The $20 discount can be applied to the initial entry or any subsequent re-entry"),
}

# ---------------------------------------------------------------------------
# Venetian DeepStack Extravaganza IV rows.
# Order, dates, times, event numbers, names, buy-ins and guarantees are copied
# from the official event page read on 2026-11-16. Entry rule, house fee,
# starting stack, level length and late-registration close come from the
# structure sheet linked on that row, which was read on 2026-11-16.
# Day-2 restarts and satellites are excluded (satellites award seats, not cash).
#   (date, start 24h, event no, name, buy-in, guarantee, sheet, extra note)
# ---------------------------------------------------------------------------
DSE4 = [
 ("2026-11-16","11:10",1,"$300 No Limit Hold'em 1A",300,75000,10,"Flight 1A of 4 (1A-1D)."),
 ("2026-11-16","17:10",1,"$300 No Limit Hold'em 1B",300,75000,9,"Flight 1B of 4 (1A-1D)."),
 ("2026-11-17","11:10",1,"$300 No Limit Hold'em 1C",300,75000,10,"Flight 1C of 4 (1A-1D)."),
 ("2026-11-17","17:10",1,"$300 No Limit Hold'em 1D",300,75000,9,"Flight 1D of 4 (1A-1D)."),
 ("2026-11-18","11:10",2,"$300 No Limit Hold'em (1Day)",300,10000,5,None),
 ("2026-11-19","10:10",3,"$200 NLH RaceDay Stack (1Day)",200,None,18,"Official name adds: race to finish before the race."),
 ("2026-11-20","10:10",4,"$200 NLH RaceDay Stack (1Day)",200,None,18,"Official name adds: race to finish before the race."),
 ("2026-11-21","10:10",5,"$200 NLH RaceDay Stack (1Day)",200,None,18,"Official name adds: race to finish before the race."),
 ("2026-11-22","11:10",6,"$200 No Limit Hold'em (1Day)",200,None,29,None),
 ("2026-11-23","11:10",7,"$400 No Limit Hold'em 1A",400,75000,2,"Flight 1A of 2 (1A-1B)."),
 ("2026-11-23","17:10",8,"$200 No Limit Hold'em PKO Bounty (1Day)",200,8000,30,"Progressive Knock-Out bounty."),
 ("2026-11-24","11:10",7,"$400 No Limit Hold'em 1B",400,75000,2,"Flight 1B of 2 (1A-1B)."),
 ("2026-11-24","17:10",9,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"Bounty $50 per elimination."),
 ("2026-11-25","11:10",10,"$400 No Limit Hold'em (1Day)",400,15000,6,None),
 ("2026-11-25","17:10",11,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"Bounty $50 per elimination."),
 ("2026-11-26","11:10",12,"$300 No Limit Hold'em (1Day)",300,10000,5,None),
 ("2026-11-26","17:10",13,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"Bounty $50 per elimination."),
 ("2026-11-27","11:10",14,"$600 No Limit Hold'em (1Day)",600,30000,7,None),
 ("2026-11-27","17:10",15,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"Bounty $50 per elimination."),
 ("2026-11-28","11:10",16,"$600 No Limit Hold'em Bounty (1Day)",600,30000,11,"$200 bounties to start, $500 in the money."),
 ("2026-11-28","12:10",17,"$400 Pot Limit Omaha Bounty (1Day)",400,15000,26,"Bounty $100 per elimination."),
 ("2026-11-28","17:10",18,"$200 NLH PokerAtlas Valuetown Bounty (1Day)",200,20000,8,"PokerAtlas PRO member $20 rake discount."),
 ("2026-11-29","11:10",19,"$400 No Limit Hold'em 1A",400,75000,3,"Flight 1A of 3 (1A-1C)."),
 ("2026-11-29","12:10",20,"$300 Pot Limit Omaha Double Board Bomb Pot (1Day)",300,10000,22,None),
 ("2026-11-29","17:10",21,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"Bounty $50 per elimination."),
 ("2026-11-30","11:10",19,"$400 No Limit Hold'em 1B",400,75000,3,"Flight 1B of 3 (1A-1C)."),
 ("2026-11-30","17:10",22,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"Bounty $50 per elimination."),
 ("2026-12-01","11:10",19,"$400 No Limit Hold'em 1C",400,75000,3,"Flight 1C of 3 (1A-1C)."),
 ("2026-12-01","17:10",23,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"Bounty $50 per elimination."),
 ("2026-12-02","10:10",24,"$600 No Limit Hold'em Seniors (1Day)",600,40000,17,"Eligibility: must be 50+."),
 ("2026-12-02","17:10",25,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"Bounty $50 per elimination."),
 ("2026-12-03","11:10",26,"$800 No Limit Hold'em 1A",800,500000,12,"Flight 1A of 6 (1A-1F)."),
 ("2026-12-03","12:10",27,"$600 BIG O (1Day)",600,25000,28,None),
 ("2026-12-03","17:10",26,"$800 No Limit Hold'em 1B",800,500000,13,"Flight 1B of 6 (1A-1F)."),
 ("2026-12-04","11:10",26,"$800 No Limit Hold'em 1C",800,500000,12,"Flight 1C of 6 (1A-1F)."),
 ("2026-12-04","17:10",26,"$800 No Limit Hold'em 1D",800,500000,13,"Flight 1D of 6 (1A-1F)."),
 ("2026-12-05","11:10",26,"$800 No Limit Hold'em 1E",800,500000,12,"Flight 1E of 6 (1A-1F)."),
 ("2026-12-05","17:10",26,"$800 No Limit Hold'em 1F (Turbo)",800,500000,14,"Flight 1F of 6 (1A-1F), 20-minute levels."),
 ("2026-12-06","11:10",28,"$600 No Limit Hold'em (1Day)",600,40000,7,None),
 ("2026-12-06","17:10",29,"$300 No Limit Hold'em Bounty (1Day)",300,15000,15,"Bounty $100 per elimination."),
 ("2026-12-07","11:10",30,"$600 No Limit Hold'em Bounty (1Day)",600,40000,11,"$200 bounties to start, $500 in the money."),
 ("2026-12-07","17:10",31,"$300 No Limit Hold'em Bounty (1Day)",300,15000,15,"Bounty $100 per elimination."),
 ("2026-12-08","10:10",32,"$600 No Limit Hold'em Seniors (1Day)",600,40000,17,"Eligibility: must be 50+."),
 ("2026-12-08","17:10",34,"$300 No Limit Hold'em Bounty (1Day)",300,15000,15,"Bounty $100 per elimination."),
 ("2026-12-09","10:10",35,"$600 NLH LIPS Poker Jingle Tag Team (1Day)",600,10000,31,"Teams: Female/Female or Female/Male."),
 ("2026-12-09","11:10",36,"$800 No Limit Hold'em Bounty (1Day)",800,75000,16,"$200 bounties to start, $500 in the money."),
 ("2026-12-09","17:10",38,"$300 No Limit Hold'em Bounty (1Day)",300,15000,15,"Bounty $100 per elimination."),
 ("2026-12-10","10:10",39,"$800 No Limit Hold'em LIPS Ladies (2Day)",800,40000,32,"Women in Poker main event. Eligibility: female."),
 ("2026-12-10","12:10",40,"$600 Pot Limit Omaha Bounty (1Day)",600,25000,27,"Bounty $200 per elimination."),
 ("2026-12-10","17:10",42,"$300 No Limit Hold'em Bounty (1Day)",300,15000,15,"Bounty $100 per elimination."),
 ("2026-12-11","11:10",43,"$600 No Limit Hold'em LIPS Kings and Queens Bounty (1Day)",600,30000,33,"Open to all players. Bounty $200 per elimination."),
 ("2026-12-12","10:10",47,"$2,200 No Limit Hold'em 1A - PokerAtlas Championship",2200,1000000,21,"Flight 1A of 2 (1A-1B)."),
 ("2026-12-12","18:10",47,"$2,200 No Limit Hold'em 1B - PokerAtlas Championship",2200,1000000,37,"Flight 1B of 2 (1A-1B)."),
 ("2026-12-13","10:10",49,"$1,100 No Limit Hold'em Seniors 1A",1100,300000,20,"Flight 1A of 2 (1A-1B). Eligibility: must be 50+."),
 ("2026-12-13","17:10",50,"$300 No Limit Hold'em Bounty (1Day)",300,15000,15,"Bounty $100 per elimination."),
 ("2026-12-14","10:10",49,"$1,100 No Limit Hold'em Seniors 1B",1100,300000,20,"Flight 1B of 2 (1A-1B). Eligibility: must be 50+."),
 ("2026-12-14","17:10",51,"$300 No Limit Hold'em Bounty (1Day)",300,15000,15,"Bounty $100 per elimination."),
 ("2026-12-15","11:10",52,"$1,100 No Limit Hold'em Progressive Knockout Bounty (1Day)",1100,75000,34,"Progressive Knock-Out. Bounty starts at $200."),
 ("2026-12-15","17:10",53,"$300 No Limit Hold'em Bounty (1Day)",300,15000,15,"Bounty $100 per elimination."),
 ("2026-12-16","11:10",54,"$600 No Limit Hold'em Bounty (1Day)",600,50000,11,"$200 bounties to start, $500 in the money."),
 ("2026-12-16","17:10",55,"$300 No Limit Hold'em Bounty (1Day)",300,15000,15,"Bounty $100 per elimination."),
 ("2026-12-17","10:10",56,"$1,100 No Limit Hold'em 1A",1100,500000,35,"Flight 1A of 5 (1A-1E). $40 rake discount for entries before 10:10 AM."),
 ("2026-12-17","12:10",57,"$600 Pot Limit Omaha Double Board Bomb Pot (1Day)",600,25000,23,None),
 ("2026-12-17","18:10",56,"$1,100 No Limit Hold'em 1B",1100,500000,36,"Flight 1B of 5 (1A-1E). $40 rake discount for entries before 6:10 PM."),
 ("2026-12-18","10:10",56,"$1,100 No Limit Hold'em 1C",1100,500000,35,"Flight 1C of 5 (1A-1E)."),
 ("2026-12-18","18:10",56,"$1,100 No Limit Hold'em 1D",1100,500000,36,"Flight 1D of 5 (1A-1E)."),
 ("2026-12-19","10:10",56,"$1,100 No Limit Hold'em 1E",1100,500000,35,"Flight 1E of 5 (1A-1E)."),
 ("2026-12-19","17:10",58,"$200 NLH PokerAtlas Valuetown Bounty (1Day)",200,20000,8,"PokerAtlas PRO member $20 rake discount."),
 ("2026-12-20","11:10",59,"$600 No Limit Hold'em 1A",600,150000,4,"Flight 1A of 3 (1A-1C). $20 rake discount for entries before 11:10 AM."),
 ("2026-12-20","17:10",60,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"Bounty $50 per elimination."),
 ("2026-12-21","11:10",59,"$600 No Limit Hold'em 1B",600,150000,4,"Flight 1B of 3 (1A-1C)."),
 ("2026-12-21","17:10",61,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"Bounty $50 per elimination."),
 ("2026-12-22","11:10",59,"$600 No Limit Hold'em 1C",600,150000,4,"Flight 1C of 3 (1A-1C)."),
 ("2026-12-22","17:10",62,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"Bounty $50 per elimination."),
 ("2026-12-23","11:10",63,"$600 No Limit Hold'em (1Day)",600,30000,7,None),
 ("2026-12-23","17:10",64,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"Bounty $50 per elimination."),
]

# ---------------------------------------------------------------------------
# Venetian DeepStack Extravaganza NYE rows (Dec 24, 2026 - Jan 10, 2027).
# Buy-in, guarantee and date from the official NYE event page, read 2026-11-16.
# Satellites (events 6, 7, 9-12, 15, 16, 18, 19, 21, 23, 24) are excluded.
# ---------------------------------------------------------------------------
NYE_UNV = "Entry rule not verified: this event's NYE structure sheet was not read."
NYE = [
 ("2026-12-24","11:10",1,"$400 No Limit Hold'em (1Day)",400,15000,1,None),
 ("2026-12-24","17:10",2,"$200 No Limit Hold'em Bounty (1Day)",200,8000,2,None),
 ("2026-12-25","11:10",3,"$400 No Limit Hold'em (1Day)",400,15000,1,None),
 ("2026-12-25","17:10",4,"$200 No Limit Hold'em Bounty (1Day)",200,8000,2,None),
 ("2026-12-26","11:10",5,"$600 No Limit Hold'em Bounty (1Day)",600,40000,None,
  "Official page prints this row as 'Saturday, December 26, 2025'. The year conflicts with the series dates; flagged."),
 ("2026-12-27","11:10",8,"$1,100 No Limit Hold'em 1A - Ante Up Championship",1100,300000,None,"Flight 1A of 3 (1A-1C)."),
 ("2026-12-28","11:10",8,"$1,100 No Limit Hold'em 1B - Ante Up Championship",1100,300000,None,"Flight 1B of 3 (1A-1C)."),
 ("2026-12-29","11:10",8,"$1,100 No Limit Hold'em 1C - Ante Up Championship",1100,300000,None,"Flight 1C of 3 (1A-1C)."),
 ("2026-12-29","17:10",13,"$200 No Limit Hold'em Bounty (1Day)",200,8000,2,None),
 ("2026-12-30","11:10",14,"$600 No Limit Hold'em (1Day)",600,50000,None,None),
 ("2026-12-31","11:10",17,"$400 No Limit Hold'em (1Day)",400,15000,1,None),
 ("2027-01-01","11:10",20,"$1,600 No Limit Hold'em MSPT 1A",1600,400000,None,"Flight 1A of 3 (1A-1C). $40 reduced rake until the start of level 4."),
 ("2027-01-01","17:10",22,"$200 No Limit Hold'em Bounty (1Day)",200,8000,2,None),
 ("2027-01-02","11:10",20,"$1,600 No Limit Hold'em MSPT 1B",1600,400000,None,"Flight 1B of 3 (1A-1C)."),
 ("2027-01-02","17:10",25,"$200 NLH PokerAtlas Valuetown Bounty (1Day)",200,20000,None,None),
 ("2027-01-03","11:10",20,"$1,600 No Limit Hold'em MSPT 1C",1600,400000,None,"Flight 1C of 3 (1A-1C)."),
 ("2027-01-03","17:10",26,"$200 No Limit Hold'em Bounty (1Day)",200,8000,2,None),
 ("2027-01-04","11:10",27,"$250 No Limit Hold'em 1A (1Day)",250,75000,None,"Flight 1A of 4. Day 1 payouts with 5% advancing to Day 2. $10 reduced rake for entry before 11:10 AM."),
 ("2027-01-04","17:10",27,"$250 No Limit Hold'em 1B (1Day)",250,75000,None,"Flight 1B of 4. Day 1 payouts with 5% advancing to Day 2."),
 ("2027-01-05","11:10",27,"$250 No Limit Hold'em 1C (1Day)",250,75000,None,"Flight 1C of 4. Day 1 payouts with 5% advancing to Day 2."),
 ("2027-01-05","17:10",27,"$250 No Limit Hold'em 1D (1Day)",250,75000,None,"Flight 1D of 4. Day 1 payouts with 5% advancing to Day 2."),
 ("2027-01-06","11:10",28,"$400 No Limit Hold'em (1Day)",400,15000,None,None),
 ("2027-01-06","17:10",29,"$200 No Limit Hold'em Bounty (1Day)",200,8000,2,"Show your CES badge: $10 rake discount."),
 ("2027-01-07","11:10",30,"$300 No Limit Hold'em 1A (1Day)",300,100000,None,"Flight 1A of 6 (1A-1F)."),
 ("2027-01-07","17:10",30,"$300 No Limit Hold'em 1B (1Day)",300,100000,None,"Flight 1B of 6. Show your CES badge: $10 rake discount."),
 ("2027-01-08","11:10",30,"$300 No Limit Hold'em 1C (1Day)",300,100000,None,"Flight 1C of 6 (1A-1F)."),
 ("2027-01-08","17:10",30,"$300 No Limit Hold'em 1D (1Day)",300,100000,None,"Flight 1D of 6. Show your CES badge: $10 rake discount."),
 ("2027-01-09","11:10",30,"$300 No Limit Hold'em 1E (1Day)",300,100000,None,"Flight 1E of 6 (1A-1F)."),
 ("2027-01-09","17:10",30,"$300 No Limit Hold'em 1F (1Day)",300,100000,None,"Flight 1F of 6 (1A-1F)."),
 ("2027-01-10","10:10",31,"$400 No Limit Hold'em Seniors (1Day)",400,20000,None,"Eligibility: must be 50+."),
 ("2027-01-10","17:10",32,"$200 No Limit Hold'em Bounty (1Day)",200,8000,2,None),
]

# ---------------------------------------------------------------------------
# Wynn WPT World Championship (Nov 27 - Dec 21, 2026).
# Buy-in, guarantee, date and time from the official WPT schedule PDF.
# Entry rule from the official WPT structures PDF, read 2026-11-16 (all 8 parts).
# Restart rows, Day 2/3 rows and satellites are excluded.
#   (date, start 24h, name, buy-in, guarantee, rule_key, note)
#   rule_key: None = not verified; otherwise a key into WPT_RULES.
# ---------------------------------------------------------------------------
WPT_RULES = {
 "nlh600": dict(status="RE", summary="Unlimited re-entry for each starting flight until the start of level 9.",
   excerpt="Unlimited re-entry for each starting flight will be available until the start of level 9. A player who advances to Day 2 is prohibited from entering a subsequent starting flight.",
   fee="$600 Buy-in = $510 (Tournament Prize Pool) + $65 (Tournament Fee) + $25 (Poker Staff Service Charge)",
   fee_usd=90, stack=40000, level_min=30, reg_close=None),
 "torse600": dict(status="RE", summary="Unlimited re-entry until the start of level 9.",
   excerpt="Unlimited re-entry will be available until the start of level 9",
   fee="$600 Buy-in = $510 (Tournament Prize Pool) + $65 (Tournament Fee) + $25 (Poker Staff Service Charge)",
   fee_usd=90, stack=35000, level_min=30, reg_close=None),
 "plo400": dict(status="RE", summary="Unlimited re-entry until the start of level 9 (approximately 5:30 PM).",
   excerpt="Unlimited re-entry will be available until the start of level 9 (approximately 5:30 p.m.).",
   fee="$400 Buy-in = $337 (Tournament Prize Pool) + $45 (Tournament Fee) + $18 (Poker Staff Service Charge)",
   fee_usd=63, stack=30000, level_min=30, reg_close="5:30 PM"),
 "mtd600": dict(status="RE", summary="Unlimited re-entry until the start of level 9.",
   excerpt="Unlimited re-entry will be available until the start of level 9",
   fee="$600 Buy-in = $510 (Tournament Prize Pool) + $65 (Tournament Fee) + $25 (Poker Staff Service Charge)",
   fee_usd=90, stack=35000, level_min=30, reg_close=None),
 "nlh800": dict(status="RE", summary="Unlimited re-entry for each starting flight until the start of level 9.",
   excerpt="Unlimited re-entry for each starting flight will be available until the start of level 9. A player who advances to Day 2 is prohibited from entering a subsequent starting flight.",
   fee="$800 Buy-in = $695 (Tournament Prize Pool) + $72 (Tournament Fee) + $33 (Poker Staff Service Charge)",
   fee_usd=105, stack=40000, level_min=30, reg_close=None),
 "o8_600": dict(status="RE", summary="Unlimited re-entry until the start of level 9.",
   excerpt="Unlimited re-entry will be available until the start of level 9",
   fee="$600 Buy-in = $510 (Tournament Prize Pool) + $65 (Tournament Fee) + $25 (Poker Staff Service Charge)",
   fee_usd=90, stack=35000, level_min=30, reg_close=None),
 "o8stud8_600": dict(status="RE", summary="Unlimited re-entry until the start of level 9.",
   excerpt="Unlimited re-entry will be available until the start of level 9",
   fee="$600 Buy-in = $510 (Tournament Prize Pool) + $65 (Tournament Fee) + $25 (Poker Staff Service Charge)",
   fee_usd=90, stack=35000, level_min=30, reg_close=None),
 "plo1100": dict(status="RE", summary="Unlimited re-entry until the start of level 9 (approximately 5:30 PM).",
   excerpt="Unlimited re-entry will be available until the start of level 9 (approximately 5:30 p.m.).",
   fee="$1,100 Buy-in = $975 (Tournament Prize Pool) + $85 (Tournament Fee) + $45 (Poker Staff Service Charge)",
   fee_usd=130, stack=30000, level_min=30, reg_close="5:30 PM"),
 "nlh1600": dict(status="RE", summary="Unlimited re-entry for each starting flight until the start of level 10.",
   excerpt="Unlimited re-entry for each starting flight will be available until the start of level 10. A player who advances to Day 2 is prohibited from entering a subsequent starting flight.",
   fee="$1,600 Buy-in = $1,430 (Tournament Prize Pool) + $120 (Tournament Fee) + $50 (Poker Staff Service Charge)",
   fee_usd=170, stack=40000, level_min=40, reg_close=None),
 "horse600": dict(status="RE", summary="Unlimited re-entry until the start of level 9 (approximately 4:30 PM).",
   excerpt="Unlimited re-entry will be available until the start of level 9 (approximately 4:30 p.m.).",
   fee="$600 Buy-in = $510 (Tournament Prize Pool) + $65 (Tournament Fee) + $25 (Poker Staff Service Charge)",
   fee_usd=90, stack=35000, level_min=30, reg_close="4:30 PM"),
 "prime1100": dict(status="RE", summary="One entry and one re-entry for each starting flight until the start of level 10 (approximately 6:45 PM).",
   excerpt="One (1) Entry and One (1) re-entry for each starting flight will be available until the start of level 10 (approximately 6:45 p.m.). A player who advances to Day 2 is prohibited from entering a subsequent starting flight.",
   fee="$1,100 Buy-in = $970 (Tournament Prize Pool) + $90 (Tournament Fee) + $40 (Poker Staff Service Charge)",
   fee_usd=130, stack=40000, level_min=40, reg_close="6:45 PM"),
 "turbo600": dict(status="RE", summary="Unlimited re-entry until the start of level 9.",
   excerpt="Unlimited re-entry will be available until the start of level 9",
   fee="$600 Buy-in = $515 (Tournament Prize Pool) + $60 (Tournament Fee) + $25 (Poker Staff Service Charge)",
   fee_usd=85, stack=30000, level_min=20, reg_close=None),
 "plomb1600": dict(status="RE", summary="Unlimited re-entry for each starting flight until the start of level 10.",
   excerpt="Unlimited re-entry for each starting flight will be available until the start of level 10. A player who advances to Day 2 is prohibited from entering a subsequent starting flight.",
   fee="$1,600 Buy-in = $930 (Tournament Prize Pool) + $500 (Mystery Bounty Prize Pool) + $120 (Tournament Fee) + $50 (Poker Staff Service Charge)",
   fee_usd=670, stack=40000, level_min=40, reg_close=None),
}
WPT_UNV_NOTE = ("Entry rule not verified: this event is not covered by the official WPT structures "
                "PDF that was read (8 parts, read 2026-11-16). No per-event structure sheet was found "
                "for it on an official source.")

WPT = [
 ("2026-11-27","11:00","NLH Day 1A","$600 NLH $400K",600,400000,"nlh600",None),
 ("2026-11-27","12:00","TORSE","TORSE",600,None,"torse600",None),
 ("2026-11-27","13:00","PLO","Pot Limit Omaha",400,None,"plo400",None),
 ("2026-11-27","17:00","NLH Day 1B","$600 NLH $400K",600,400000,"nlh600",None),
 ("2026-11-28","11:00","NLH Day 1C","$600 NLH $400K",600,400000,"nlh600",None),
 ("2026-11-28","12:00","Mixed Triple Draw (A-5, 2-7, Badugi)","Mixed Triple Draw",600,None,"mtd600",None),
 ("2026-11-28","17:00","NLH Day 1D","$600 NLH $400K",600,400000,"nlh600",None),
 ("2026-11-29","11:00","NLH Day 1E","$600 NLH $400K",600,400000,"nlh600",None),
 ("2026-11-29","18:00","NLH Day 1F","$600 NLH $400K",600,400000,"nlh600",None),
 ("2026-11-30","11:00","NLH Day 1A","$800 NLH $1M",800,1000000,"nlh800",None),
 ("2026-11-30","12:00","Limit Omaha 8","Limit Omaha 8",600,None,"o8_600",None),
 ("2026-11-30","17:00","NLH Day 1B","$800 NLH $1M",800,1000000,"nlh800",None),
 ("2026-12-01","11:00","NLH Day 1C","$800 NLH $1M",800,1000000,"nlh800",None),
 ("2026-12-01","12:00","Limit Omaha 8/Stud 8","Limit Omaha 8/Stud 8",600,None,"o8stud8_600",None),
 ("2026-12-01","13:00","PLO","Pot Limit Omaha",1100,None,"plo1100",None),
 ("2026-12-01","17:00","NLH Day 1D","$800 NLH $1M",800,1000000,"nlh800",None),
 ("2026-12-02","11:00","NLH Day 1E","$800 NLH $1M",800,1000000,"nlh800",None),
 ("2026-12-02","18:00","NLH Day 1F","$800 NLH $1M",800,1000000,"nlh800",None),
 ("2026-12-03","11:00","NLH Day 1A","$1,600 NLH $1M",1600,1000000,"nlh1600",None),
 ("2026-12-04","11:00","NLH Day 1B","$1,600 NLH $1M",1600,1000000,"nlh1600",None),
 ("2026-12-04","12:00","HORSE","HORSE",600,None,"horse600",None),
 ("2026-12-05","11:00","WPT Prime Championship Day 1A","WPT Prime Championship $5M",1100,5000000,"prime1100",None),
 ("2026-12-05","21:00","NLH Turbo","NLH Turbo $50K",600,50000,"turbo600",None),
 ("2026-12-06","11:00","PLO Mystery Bounty Day 1A","PLO Mystery Bounty $500K",1600,500000,"plomb1600",None),
 ("2026-12-06","11:00","WPT Prime Championship Day 1B","WPT Prime Championship $5M",1100,5000000,"prime1100",None),
 ("2026-12-06","18:00","PLO Mystery Bounty Day 1B","PLO Mystery Bounty $500K",1600,500000,"plomb1600",None),
 ("2026-12-06","21:00","NLH Turbo","NLH Turbo $50K",600,50000,"turbo600",None),
 ("2026-12-07","11:00","HORSE (2 Day)","HORSE (2 Day)",1100,None,None,None),
 ("2026-12-07","11:00","WPT Prime Championship Day 1C","WPT Prime Championship $5M",1100,5000000,"prime1100",None),
 ("2026-12-07","13:00","PLO $500 Bounty","PLO $500 Bounty $100K",1600,100000,None,None),
 ("2026-12-07","21:00","NLH Turbo","NLH Turbo $50K",600,50000,"turbo600",None),
 ("2026-12-08","11:00","WPT Prime Championship Day 1D","WPT Prime Championship $5M",1100,5000000,"prime1100",None),
 ("2026-12-08","21:00","NLH Turbo","NLH Turbo $50K",600,50000,"turbo600",None),
 ("2026-12-09","11:00","No Limit Hold'em (2 Day)","NLH (2 Day) $1M",1600,1000000,None,None),
 ("2026-12-09","13:00","PLO $1,000 Bounty","PLO $1,000 Bounty $250K",3000,250000,None,None),
 ("2026-12-09","13:00","Limit Omaha 8","Limit Omaha 8",800,None,None,None),
 ("2026-12-09","21:00","NLH Turbo","NLH Turbo $50K",600,50000,"turbo600",None),
 ("2026-12-10","10:00","Super Gold Million Mystery Bounty Day 1A","Super Gold Million $3M",400,3000000,None,None),
 ("2026-12-10","18:00","Super Gold Million Mystery Bounty Day 1B","Super Gold Million $3M",400,3000000,None,None),
 ("2026-12-11","10:00","Super Gold Million Mystery Bounty Day 1C","Super Gold Million $3M",400,3000000,None,None),
 ("2026-12-11","18:00","Super Gold Million Mystery Bounty Day 1D","Super Gold Million $3M",400,3000000,None,None),
 ("2026-12-12","10:00","No Limit Hold'em","NLH $100K",800,100000,None,None),
 ("2026-12-12","13:00","PLO","PLO $250K",3000,250000,None,None),
 ("2026-12-12","21:00","NLH Turbo","NLH Turbo $50K",600,50000,"turbo600",None),
 ("2026-12-13","11:00","WPT World Championship Day 1A","WPT World Championship",10400,None,None,
  "Official footnote: $1M added by ClubWPT Gold, which the same footnote says is not available in Nevada. Flagged."),
 ("2026-12-13","11:00","Ladies NIH Championship (2 Day)","Ladies NIH Championship $250K",1100,250000,None,
  "Printed name reads 'NIH'. Printed buy-in is $1,100; official footnote: 'The Tournament Entry for the Ladies Championship is $11,100. Ladies will receive a discounted entry.' Flagged."),
 ("2026-12-13","11:00","No Limit Hold'em Day 1A","NLH $500K",800,500000,None,None),
 ("2026-12-13","12:00","PLO Day 1A","PLO $1M",1600,1000000,None,None),
 ("2026-12-14","11:00","WPT World Championship Day 1B","WPT World Championship",10400,None,None,"Official footnote: ClubWPT Gold addition. Flagged."),
 ("2026-12-14","11:00","No Limit Hold'em Day 1B","NLH $500K",800,500000,None,None),
 ("2026-12-14","12:00","PLO Day 1B","PLO $1M",1600,1000000,None,None),
 ("2026-12-14","12:00","Mixed Triple Draw (2 Day)","Mixed Triple Draw (2 Day)",1100,None,None,None),
 ("2026-12-14","19:00","PLO Turbo","PLO Turbo $100K",1100,100000,None,None),
 ("2026-12-14","21:00","NLH Turbo","NLH Turbo $50K",600,50000,"turbo600",None),
 ("2026-12-15","11:00","WPT World Championship Day 1C","WPT World Championship",10400,None,None,"Official footnote: ClubWPT Gold addition. Flagged."),
 ("2026-12-15","12:00","Big O","Big O",1100,None,None,None),
 ("2026-12-15","12:00","H.O.R.S.E.","H.O.R.S.E.",600,None,None,None),
 ("2026-12-15","19:00","No Limit Hold'em Day 1A","NLH $200K",600,200000,None,None),
 ("2026-12-16","11:00","No Limit Hold'em Day 1B","NLH $200K",600,200000,None,None),
 ("2026-12-16","12:00","Seven Card Stud","Seven Card Stud",600,None,None,None),
 ("2026-12-16","19:00","No Limit Hold'em Day 1A","NLH $300K",1100,300000,None,None),
 ("2026-12-17","11:00","No Limit Hold'em Day 1B","NLH $300K",1100,300000,None,None),
 ("2026-12-17","12:00","Omaha 8/Stud 8 (2 Day)","Omaha 8/Stud 8 (2 Day)",1100,None,None,None),
 ("2026-12-17","13:00","PLO","PLO",10500,None,None,None),
 ("2026-12-17","19:00","No Limit Hold'em Day 1A","NLH $500K",1600,500000,None,None),
 ("2026-12-18","11:00","No Limit Hold'em Day 1B","NLH $500K",1600,500000,None,None),
 ("2026-12-18","12:00","No Limit Hold'em Seniors Day 1A","Seniors NLH $200K",600,200000,None,None),
 ("2026-12-18","13:00","HORSE","HORSE",800,None,None,None),
 ("2026-12-18","13:00","NLH 6-Max","NLH 6-Max",10500,None,None,None),
 ("2026-12-18","18:00","NLH Turbo","NLH Turbo $100K",1100,100000,None,None),
 ("2026-12-18","19:00","No Limit Hold'em Day 1B","NLH $1M",1100,1000000,None,None),
 ("2026-12-19","11:00","Seniors High Roller (3 Day)","Seniors High Roller $250K",5000,250000,None,None),
 ("2026-12-19","11:00","NLH Mystery Bounty Day 1A","NLH Mystery Bounty $1M",1600,1000000,None,None),
 ("2026-12-19","13:00","PLO","PLO",10500,None,None,None),
 ("2026-12-19","13:00","NLH 6-Max","NLH 6-Max $500K",3000,500000,None,None),
 ("2026-12-19","13:00","TORSE Championship (2 Day)","TORSE Championship (2 Day)",1600,None,None,None),
 ("2026-12-19","18:00","NLH 6-Max Turbo","NLH 6-Max Turbo $50K",600,50000,None,None),
 ("2026-12-19","19:00","NLH Mystery Bounty Day 1B","NLH Mystery Bounty $1M",1600,1000000,None,None),
 ("2026-12-20","11:00","NLH Mystery Bounty Day 1C","NLH Mystery Bounty $1M",1600,1000000,None,None),
 ("2026-12-20","12:00","No Limit Hold'em","NLH $50K",600,50000,None,None),
 ("2026-12-20","13:00","NLH 8-Max","NLH 8-Max",10500,None,None,None),
 ("2026-12-20","13:00","Mixed Triple Draw","Mixed Triple Draw",600,None,"mtd600","Official structures PDF lists a Mixed Triple Draw at Dec 20, 1 p.m."),
 ("2026-12-20","18:00","5-Card PLO Turbo","5-Card PLO Turbo $50K",600,50000,None,None),
 ("2026-12-20","19:00","NLH Mystery Bounty Day 1D","NLH Mystery Bounty $1M",1600,1000000,None,None),
 ("2026-12-21","12:00","No Limit Hold'em","NLH $100K",1100,100000,None,None),
 ("2026-12-21","20:00","NLH Turbo","NLH Turbo $50K",600,50000,None,None),
]

# ---------------------------------------------------------------------------
# Wynn Signature Series (Jan 11 - 24, 2027). Buy-in and guarantee from the
# official schedule PDF. No structures PDF was found on an official source, so
# every row is unverified for entry rule.
# ---------------------------------------------------------------------------
WSS_NOTE = ("Buy-in and guarantee from the official Wynn Signature Series schedule PDF. No "
            "structures document for this series was found on an official source, so the entry "
            "rule is not verified.")
WSS = [
 ("2027-01-11","12:00","No Limit Hold'em Day 1A",400,150000),
 ("2027-01-11","17:00","No Limit Hold'em Day 1B",400,150000),
 ("2027-01-12","12:00","No Limit Hold'em Day 1C",400,150000),
 ("2027-01-12","17:00","No Limit Hold'em Day 1D",400,150000),
 ("2027-01-13","12:00","No Limit Hold'em Day 1E",400,150000),
 ("2027-01-13","17:00","No Limit Hold'em Day 1F",400,150000),
 ("2027-01-14","11:00","No Limit Hold'em Day 1A",600,250000),
 ("2027-01-15","11:00","No Limit Hold'em Day 1B",600,250000),
 ("2027-01-15","18:00","NLH Turbo",200,10000),
 ("2027-01-16","11:00","No Limit Hold'em Day 1C",600,250000),
 ("2027-01-16","18:00","No Limit Hold'em Day 1D",600,250000),
 ("2027-01-17","12:00","No Limit Hold'em",400,30000),
 ("2027-01-17","18:00","NLH Turbo",200,10000),
 ("2027-01-18","11:00","No Limit Hold'em Day 1A",400,100000),
 ("2027-01-18","13:00","PLO",400,None),
 ("2027-01-18","18:00","NLH Turbo",200,10000),
 ("2027-01-19","11:00","No Limit Hold'em Day 1B",400,100000),
 ("2027-01-19","13:00","TORSE",400,None),
 ("2027-01-19","18:00","NLH Turbo",200,10000),
 ("2027-01-20","11:00","No Limit Hold'em Day 1C",400,100000),
 ("2027-01-20","13:00","Mixed Triple Draw (A-5, 2-7, Badugi)",400,None),
 ("2027-01-20","18:00","NLH Turbo",200,10000),
 ("2027-01-21","11:00","No Limit Hold'em Day 1A",800,300000),
 ("2027-01-21","13:00","TOE",400,None),
 ("2027-01-22","11:00","No Limit Hold'em Day 1B",800,300000),
 ("2027-01-22","13:00","BIG O",400,None),
 ("2027-01-23","11:00","No Limit Hold'em Day 1C",800,300000),
 ("2027-01-23","18:00","No Limit Hold'em Day 1D",800,300000),
 ("2027-01-24","12:00","Seniors NLH 50+",400,30000),
 ("2027-01-24","13:00","PLO Double Board Bomb Pot",400,None),
 ("2027-01-24","18:00","NLH Turbo",200,10000),
]

# ---------------------------------------------------------------------------
# Hotels.
# ---------------------------------------------------------------------------
HOTELS = [
 {"id":"venetian","name":"The Venetian Resort","venue_id":"venetian",
  "address_note":"Host property for the DeepStack series. On the Strip, north of Flamingo.",
  "resort_fee_usd":55,"resort_fee_status":"verified",
  "resort_fee_note":"Official Venetian hotel terms, read 2026-11-16: $55 plus applicable tax per night.",
  "resort_fee_source":SRC["venetian_terms"],
  "room_rate_usd":None,"room_rate_status":"unverified",
  "room_rate_note":"Official poker-suite page says rates 'start as low as $119 and $209' (Venetian or Palazzo), conditional on poker play. Which rate applies to which tower is not stated, so no value is entered here.",
  "room_tax_pct":13.38,"tax_status":"Verified from full official Venetian hotel terms read 2026-11-16: Clark County Room Tax 13.38%.",
  "tax_source":SRC["venetian_terms"],
  "parking_usd":None,"parking_status":"unverified","parking_note":"No parking rate was confirmed from an official Venetian source.",
  "cancellation_deadline":None,"cancellation_status":"unverified","cancellation_note":"No cancellation deadline was confirmed from an official Venetian source.",
  "booking_url":"https://www.venetianlasvegas.com/book",
  "sources":[{"label":"Resort fee (official)","url":SRC["venetian_fee"]},
             {"label":"Hotel terms incl. 13.38% room tax and resort-fee tax (official)","url":SRC["venetian_terms"]},
             {"label":"Poker suite rates (official)","url":SRC["venetian_poker_suite"]},
             {"label":"Official booking page","url":"https://www.venetianlasvegas.com/book"}]},
 {"id":"palazzo","name":"The Palazzo","venue_id":"venetian",
  "address_note":"Venetian sister property, same resort complex.",
  "resort_fee_usd":55,"resort_fee_status":"verified",
  "resort_fee_note":"Official Venetian poker-suite page: 'There is a $55 resort fee per night stayed' (stated for The Venetian or The Palazzo).",
  "resort_fee_source":SRC["venetian_poker_suite"],
  "room_rate_usd":None,"room_rate_status":"unverified",
  "room_rate_note":"Only conditional poker-suite starting rates are published (see Venetian row). No Palazzo-specific rate confirmed.",
  "room_tax_pct":None,"tax_status":"Unverified for Palazzo: the fetched Venetian hotel terms do not separately identify Palazzo's tax calculation.",
  "tax_source":None,
  "parking_usd":None,"parking_status":"unverified","parking_note":"No parking rate was confirmed from an official source for Palazzo.",
  "cancellation_deadline":None,"cancellation_status":"unverified","cancellation_note":"Not confirmed from an official source.",
  "booking_url":"https://www.venetianlasvegas.com/book",
  "sources":[{"label":"Poker suite rates incl. $55 resort fee (official)","url":SRC["venetian_poker_suite"]},
             {"label":"Venetian hotel terms (official; property-specific Palazzo tax not stated)","url":SRC["venetian_terms"]}]},
 {"id":"wynn","name":"Wynn Las Vegas","venue_id":"wynn",
  "address_note":"Host property for the WPT World Championship and the Wynn Signature Series.",
  "resort_fee_usd":55,"resort_fee_status":"verified",
  "resort_fee_note":"Official Wynn terms (search excerpt, not fetched in full): daily resort fee of $55 plus tax per room night.",
  "resort_fee_source":SRC["wynn_terms"],
  "room_rate_usd":None,"room_rate_status":"unverified",
  "room_rate_note":"No official nightly rate confirmed for any date. Third-party rates are not used.",
  "room_tax_pct":None,"tax_status":"Unverified: no Wynn-specific tax rate was confirmed from official terms.",
  "tax_source":None,
  "parking_usd":None,"parking_status":"unverified","parking_note":"No parking rate was confirmed from an official Wynn source.",
  "cancellation_deadline":None,"cancellation_status":"unverified","cancellation_note":"Not confirmed from an official source.",
  "booking_url":"https://www.wynnlasvegas.com/",
  "sources":[{"label":"Resort fee terms (official)","url":SRC["wynn_terms"]},
             {"label":"Wynn poker room (official)","url":SRC["wynn_poker"]}]},
 {"id":"encore","name":"Encore at Wynn Las Vegas","venue_id":"wynn",
  "address_note":"Same resort operator as Wynn Las Vegas.",
  "resort_fee_usd":55,"resort_fee_status":"verified",
  "resort_fee_note":"Official Wynn terms (search excerpt, not fetched in full) cover 'Wynn and Encore Las Vegas' with a $55 plus tax daily resort fee. Confirm for the specific room.",
  "resort_fee_source":SRC["wynn_terms"],
  "room_rate_usd":None,"room_rate_status":"unverified","room_rate_note":"No official nightly rate confirmed.",
  "room_tax_pct":None,"tax_status":"Unverified: no Encore-specific tax rate was confirmed from official terms.",
  "tax_source":None,
  "parking_usd":None,"parking_status":"unverified","parking_note":"Not confirmed from an official source.",
  "cancellation_deadline":None,"cancellation_status":"unverified","cancellation_note":"Not confirmed from an official source.",
  "booking_url":"https://www.wynnlasvegas.com/",
  "sources":[{"label":"Resort fee terms (official)","url":SRC["wynn_terms"]}]},
 {"id":"bellagio","name":"Bellagio","venue_id":None,
  "address_note":"MGM Resorts property on the Strip.",
  "resort_fee_usd":None,"resort_fee_status":"unverified",
  "resort_fee_note":"No Bellagio-specific official resort-fee terms confirmed. Third-party guides conflict; left blank.",
  "resort_fee_source":None,
  "room_rate_usd":None,"room_rate_status":"unverified","room_rate_note":"No official nightly rate confirmed.",
  "room_tax_pct":None,"tax_status":"Unverified for Bellagio: no Bellagio-specific tax rate confirmed from official terms.",
  "tax_source":None,
  "parking_usd":None,"parking_status":"unverified","parking_note":"Not confirmed from an official source.",
  "cancellation_deadline":None,"cancellation_status":"unverified","cancellation_note":"Not confirmed from an official source.",
  "booking_url":"https://bellagio.mgmresorts.com/en.html",
  "sources":[{"label":"Bellagio official home page (property identification; no fee or tax value)","url":"https://bellagio.mgmresorts.com/en.html"}]},
 {"id":"aria","name":"ARIA Resort & Casino","venue_id":None,
  "address_note":"MGM Resorts property on the Strip.",
  "resort_fee_usd":None,"resort_fee_status":"unverified",
  "resort_fee_note":"Official ARIA home page fetched; no official resort-fee terms located on it. Left blank.",
  "resort_fee_source":None,
  "room_rate_usd":None,"room_rate_status":"unverified","room_rate_note":"No official nightly rate confirmed.",
  "room_tax_pct":None,"tax_status":"Unverified for ARIA: no property-specific tax rate was confirmed from official terms.",
  "tax_source":None,
  "parking_usd":None,"parking_status":"unverified","parking_note":"Not confirmed from an official source.",
  "cancellation_deadline":None,"cancellation_status":"unverified","cancellation_note":"Not confirmed from an official source.",
  "booking_url":"https://aria.mgmresorts.com/en.html",
  "sources":[{"label":"ARIA official home page (fetched)","url":"https://aria.mgmresorts.com/en.html"}]},
 {"id":"caesars","name":"Caesars Palace","venue_id":None,
  "address_note":"Caesars Entertainment property on the Strip.",
  "resort_fee_usd":None,"resort_fee_status":"unverified",
  "resort_fee_note":"Official corporate disclaimer gives a general range of $45 to $50 plus applicable tax, not property-specific. Third-party listings conflict. Left blank.",
  "resort_fee_source":SRC["caesars_disclaimer"],
  "room_rate_usd":None,"room_rate_status":"unverified","room_rate_note":"No official nightly rate confirmed.",
  "room_tax_pct":None,"tax_status":"Unverified for Caesars Palace: no property-specific tax rate was confirmed from official terms.",
  "tax_source":None,
  "parking_usd":None,"parking_status":"unverified","parking_note":"Not confirmed from an official source.",
  "cancellation_deadline":None,"cancellation_status":"unverified","cancellation_note":"Not confirmed from an official source.",
  "booking_url":"https://www.caesars.com/caesars-palace",
  "sources":[{"label":"Caesars corporate disclaimer (official range)","url":SRC["caesars_disclaimer"]}]},
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def to_minutes(hhmm):
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)

def reg_close_24h(sheet, start_24h):
    """Convert a printed late-registration close time to 24h.

    Venetian sheets print e.g. '9 levels + Break (9:40 PM)'. The clock time is
    taken verbatim. Sheets that give no clock time return None.
    """
    rc = sheet.get("reg_close")
    if not rc:
        return None
    rc = rc.strip()
    if rc.endswith("PM") or rc.endswith("AM"):
        t = rc[:-3].strip()
        h, m = t.split(":")
        h = int(h) % 12
        if rc.endswith("PM"):
            h += 12
        return "%02d:%02d" % (h, int(m))
    return None

def sheet_rules(sheet, sheet_url, status):
    """Build the structured rule fields for one structure sheet."""
    rule_excerpt = sheet.get("rule_excerpt")
    if status == "SE":
        se_val, se_exc = True, NO_REENTRY_LINE
        re_val, re_exc = False, "No re-entry clause appears on this official structure sheet."
        ao_val, ao_exc = False, "No add-on or rebuy clause appears on this official structure sheet."
        fl_val, fl_exc = False, "No flight clause appears on this official structure sheet."
    elif status == "MULTI":
        se_val, se_exc = None, BAG_NOTE
        re_val, re_exc = None, ("Not stated. " + BAG_CLAUSE + " The sheet does not say whether a "
                                "player who busts may enter a later flight.")
        ao_val, ao_exc = False, "No add-on or rebuy clause appears on this official structure sheet."
        fl_val, fl_exc = True, ("Multi-flight event. " + BAG_CLAUSE)
    elif status == "RE":
        se_val, se_exc = False, (rule_excerpt or "Re-entry is offered on this official structure sheet.")
        re_val, re_exc = True, (rule_excerpt or "")
        ao_val, ao_exc = None, "Add-on terms not stated on the official structure sheet."
        fl_val, fl_exc = None, "Flight terms as printed on the official structure sheet."
    else:  # FLAG
        se_val, se_exc = None, ("Wording on the official sheet implies a second buy-in but does not "
                                "state it outright: " + (rule_excerpt or ""))
        re_val, re_exc = None, ("Not stated outright. Wording that implies a second buy-in: "
                                + (rule_excerpt or ""))
        ao_val, ao_exc = None, "Not stated."
        fl_val, fl_exc = None, "Not stated."
    def fld(value, excerpt):
        return {"value": value, "excerpt": excerpt, "source_url": sheet_url, "retrieved_on": CHECKED_ON}
    return {
        "single_entry": fld(se_val, se_exc),
        "re_entry": fld(re_val, re_exc),
        "add_on": fld(ao_val, ao_exc),
        "fee": fld(sheet.get("fee_usd"), sheet.get("fee_excerpt")),
    }

def unverified_rules(why, url):
    def fld(value, excerpt):
        return {"value": value, "excerpt": excerpt, "source_url": url, "retrieved_on": CHECKED_ON}
    return {
        "single_entry": fld(None, why),
        "re_entry": fld(None, why),
        "add_on": fld(None, why),
        "fee": fld(None, why),
    }

# ---------------------------------------------------------------------------
# Build tournament rows
# ---------------------------------------------------------------------------
def build_tournaments():
    rows = []

    def sheet_row(series, date, start, ev, name, buy, gtd, sheet_no, sheets, struct_tpl,
                  page_url, sched_url, extra):
        s = sheets[sheet_no]
        sheet_url = struct_tpl.format(sheet_no)
        status = s["status"]
        fee = s["fee_usd"]
        notes = []
        if extra:
            notes.append(extra)
        if s.get("gtd_note"):
            notes.append(s["gtd_note"])
        if s.get("level_note"):
            notes.append(s["level_note"])
        rows.append({
            "id": "",
            "series": series,
            "venue_id": SERIES_VENUE[series],
            "date": date,
            "start": start,
            "start_minutes": to_minutes(start),
            "event_no": ev,
            "name": name,
            "buy_in_usd": buy,
            "guarantee_usd": gtd,
            "house_fee_usd": fee,
            "house_fee_pct": round(fee / buy * 100.0, 2) if fee and buy else None,
            "gtd_multiple": round(gtd / buy, 1) if gtd and buy else None,
            "entry_status": status,
            "starting_chips": s.get("stack"),
            "level_minutes": s.get("level_min"),
            "reg_closes": reg_close_24h(s, start),
            "reg_closes_printed": s.get("reg_close"),
            "rules": sheet_rules(s, sheet_url, status),
            "note": " ".join(notes) if notes else None,
            "sources": [{"label": "Official series event page", "url": page_url},
                        {"label": "Official schedule (PDF)", "url": sched_url},
                        {"label": "Structure sheet #%d (official PDF)" % sheet_no, "url": sheet_url}],
            "last_checked": CHECKED_ON,
        })

    def plain_row(series, date, start, ev, name, buy, gtd, status, why, urls, extra,
                  rules=None):
        notes = [extra] if extra else []
        if status == "UNV":
            notes.append(why)
        rows.append({
            "id": "",
            "series": series,
            "venue_id": SERIES_VENUE[series],
            "date": date,
            "start": start,
            "start_minutes": to_minutes(start),
            "event_no": ev,
            "name": name,
            "buy_in_usd": buy,
            "guarantee_usd": gtd,
            "house_fee_usd": None,
            "house_fee_pct": None,
            "gtd_multiple": round(gtd / buy, 1) if gtd and buy else None,
            "entry_status": status,
            "starting_chips": None,
            "level_minutes": None,
            "reg_closes": None,
            "reg_closes_printed": None,
            "rules": rules or unverified_rules(why, urls[-1]["url"]),
            "note": " ".join(notes) if notes else None,
            "sources": urls,
            "last_checked": CHECKED_ON,
        })

    # ---- Venetian DeepStack Extravaganza IV ----
    for date, start, ev, name, buy, gtd, sheet, extra in DSE4:
        if sheet is None:
            raise SystemExit("DSE4 row %s event %s has no structure sheet" % (date, ev))
        sheet_row("Venetian DeepStack Extravaganza IV", date, start, ev, name, buy, gtd,
                  sheet, DSE4_SHEETS, SRC["dse_nov_struct"], SRC["dse_nov_page"],
                  SRC["dse_nov_sched"], extra)

    # ---- Venetian DeepStack Extravaganza NYE ----
    for date, start, ev, name, buy, gtd, sheet, extra in NYE:
        if sheet is not None:
            sheet_row("Venetian DeepStack Extravaganza NYE", date, start, ev, name, buy, gtd,
                      sheet, NYE_SHEETS, SRC["dse_dec_struct"], SRC["dse_dec_page"],
                      SRC["dse_dec_page"], extra)
        else:
            plain_row("Venetian DeepStack Extravaganza NYE", date, start, ev, name, buy, gtd,
                      "UNV", NYE_UNV,
                      [{"label": "Official NYE event page", "url": SRC["dse_dec_page"]}], extra)

    # ---- Wynn WPT World Championship ----
    for date, start, ev_name, label, buy, gtd, key, extra in WPT:
        if key:
            r = WPT_RULES[key]
            rules = {
                "single_entry": {"value": False, "excerpt": r["excerpt"],
                                 "source_url": SRC["wpt_struct"], "retrieved_on": CHECKED_ON},
                "re_entry": {"value": True, "excerpt": r["excerpt"],
                             "source_url": SRC["wpt_struct"], "retrieved_on": CHECKED_ON},
                "add_on": {"value": None,
                           "excerpt": "Add-on terms are not stated in the official WPT structures PDF.",
                           "source_url": SRC["wpt_struct"], "retrieved_on": CHECKED_ON},
                "fee": {"value": r["fee_usd"], "excerpt": r["fee"],
                        "source_url": SRC["wpt_struct"], "retrieved_on": CHECKED_ON},
            }
            rows.append({
                "id": "", "series": "Wynn WPT World Championship", "venue_id": "wynn",
                "date": date, "start": start, "start_minutes": to_minutes(start),
                "event_no": None, "name": label + " - " + ev_name, "buy_in_usd": buy,
                "guarantee_usd": gtd, "house_fee_usd": r["fee_usd"],
                "house_fee_pct": round(r["fee_usd"] / buy * 100.0, 2) if buy else None,
                "gtd_multiple": round(gtd / buy, 1) if gtd and buy else None,
                "entry_status": "RE", "starting_chips": r["stack"],
                "level_minutes": r["level_min"],
                "reg_closes": None, "reg_closes_printed": r["reg_close"],
                "rules": rules,
                "note": ((extra + " ") if extra else "") + r["summary"],
                "sources": [{"label": "Official WPT schedule (PDF)", "url": SRC["wpt_sched"]},
                            {"label": "Official WPT structures and terms (PDF)", "url": SRC["wpt_struct"]}],
                "last_checked": CHECKED_ON,
            })
        else:
            plain_row("Wynn WPT World Championship", date, start, None,
                      label + " - " + ev_name, buy, gtd, "UNV", WPT_UNV_NOTE,
                      [{"label": "Official WPT schedule (PDF)", "url": SRC["wpt_sched"]}], extra)

    # ---- Wynn Signature Series ----
    for date, start, name, buy, gtd in WSS:
        plain_row("Wynn Signature Series", date, start, None, name, buy, gtd, "UNV", WSS_NOTE,
                  [{"label": "Official Wynn Signature Series schedule (PDF)", "url": SRC["wss_sched"]}], None)

    rows.sort(key=lambda r: (r["date"], r["start"], r["series"], r["name"]))
    for i, r in enumerate(rows, 1):
        r["id"] = "r%03d" % i
    return rows

# ---------------------------------------------------------------------------
# Schedule: one primary event per day plus a conditional fallback.
#
# Overlap method (documented, official values only):
#   * No official source publishes a tournament finish time.
#   * Every official structure sheet does publish a start time and a
#     late-registration close time.
#   * Therefore two events are treated as CONFLICTING when their
#     [start, late-registration close] windows overlap: you cannot be seated in
#     a second event while the first is still open for registration.
#   * A gap of less than 30 minutes between one event's registration close and
#     the next event's start is flagged TIGHT (you would need to leave the
#     first table and move immediately).
#   * Finish times remain unverified, so nothing here is a forecast.
# ---------------------------------------------------------------------------
TIGHT_GAP_MIN = 30

def build_schedule(rows):
    se = [r for r in rows if r["entry_status"] == "SE"]
    by_day = {}
    for r in se:
        by_day.setdefault(r["date"], []).append(r)

    days = []
    for d in sorted(by_day):
        evs = sorted(by_day[d], key=lambda r: r["start_minutes"])
        for e in evs:
            rc = e["reg_closes"]
            e["_window_end"] = to_minutes(rc) if rc else e["start_minutes"] + 240
            e["_window_end_src"] = "official late-registration close" if rc else "no official close time published (4-hour placeholder used, flagged)"
        # Primary = best guarantee / buy-in ratio on the day. Ties break to the
        # earliest start, which is the choice that leaves room for a fallback
        # later in the day (the "play all day" goal).
        def rank(e):
            return (-(e["gtd_multiple"] or 0), e["start_minutes"])
        ordered = sorted(evs, key=rank)
        primary = ordered[0]
        fallback = None
        fallback_reason = None
        for cand in ordered[1:]:
            if cand["start_minutes"] >= primary["_window_end"]:
                fallback = cand
                fallback_reason = ("Starts at %s, after the primary event's official "
                                   "late-registration close of %s."
                                   % (cand["start"], primary["reg_closes"] or "not published"))
                break
        if fallback is None and len(ordered) == 1:
            fallback_reason = ("Only one verified single-entry event runs on this day, so there is "
                               "no conditional fallback.")
        elif fallback is None:
            fallback_reason = ("No second single-entry event on this day starts after the primary "
                               "event's late-registration close (%s). Any second entry would overlap "
                               "the primary, so none is recommended."
                               % (primary["reg_closes"] or "not published"))

        # conflicts for the whole day
        conflicts = []
        for i in range(len(evs)):
            for j in range(i + 1, len(evs)):
                a, b = evs[i], evs[j]
                if b["start_minutes"] < a["_window_end"]:
                    conflicts.append({
                        "a_id": a["id"], "b_id": b["id"],
                        "a_name": a["name"], "b_name": b["name"],
                        "a_start": a["start"], "b_start": b["start"],
                        "a_reg_closes": a["reg_closes"],
                        "severity": "conflict",
                        "reason": ("%s is still open for late registration until %s when %s starts at %s. "
                                   "You cannot be seated in both."
                                   % (a["name"], a["reg_closes"] or "(not published)", b["name"], b["start"])),
                    })
                elif 0 <= b["start_minutes"] - a["_window_end"] < TIGHT_GAP_MIN:
                    conflicts.append({
                        "a_id": a["id"], "b_id": b["id"],
                        "a_name": a["name"], "b_name": b["name"],
                        "a_start": a["start"], "b_start": b["start"],
                        "a_reg_closes": a["reg_closes"],
                        "severity": "tight",
                        "reason": ("Only %d minutes between the end of %s's late-registration window "
                                   "(%s) and the start of %s (%s). You must leave the first table the "
                                   "moment registration closes and may still be playing."
                                   % (b["start_minutes"] - a["_window_end"], a["name"],
                                      a["reg_closes"] or "(not published)", b["name"], b["start"])),
                    })

        def brief(e):
            return {"id": e["id"], "start": e["start"], "name": e["name"],
                    "series": e["series"], "buy_in_usd": e["buy_in_usd"],
                    "guarantee_usd": e["guarantee_usd"], "gtd_multiple": e["gtd_multiple"],
                    "reg_closes": e["reg_closes"], "event_no": e["event_no"],
                    "source": e["sources"][-1]["url"]}

        days.append({
            "date": d,
            "primary": brief(primary),
            "fallback": brief(fallback) if fallback else None,
            "fallback_reason": fallback_reason,
            "options": [brief(e) for e in evs],
            "conflicts": conflicts,
        })

    all_starts = sorted({r["start"] for r in rows})
    return {
        "generated_on": CHECKED_ON,
        "days": days,
        "earliest_listed_start": all_starts[0],
        "method": ("One primary event per day, chosen by guarantee / buy-in among that day's verified "
                   "single-entry events. The conditional fallback is the next-best event that starts "
                   "after the primary's official late-registration close. Overlaps are flagged using "
                   "only official start times and official late-registration close times, because no "
                   "official source publishes a finish time."),
        "note": ("No verified single-entry event in this dataset starts before 10:10 AM, so a full "
                 "day of play beginning at 8 AM is not supported by the official schedules read. "
                 "Registration OPENING times are not printed on any official schedule read; the "
                 "schedules print a registration CLOSE time per event."),
    }

# ---------------------------------------------------------------------------
# Hotels
# ---------------------------------------------------------------------------
def true_cost(h):
    if h["room_rate_usd"] is None or h["resort_fee_usd"] is None or h["room_tax_pct"] is None:
        return None
    return round((h["room_rate_usd"] + h["resort_fee_usd"]) * (1 + h["room_tax_pct"] / 100.0), 2)

def build_hotels():
    out = []
    for h in HOTELS:
        h = dict(h)
        h["true_cost_per_night_usd"] = true_cost(h)
        h["walk_minutes"] = None
        h["walk_status"] = "unverified"
        h["walk_note"] = ("Walking time is not published on any official source. Official addresses "
                          "are recorded for each hotel-venue pair, but no official walking time "
                          "exists, so the cell is blank and the 30-minute test cannot be applied yet.")
        h["last_checked"] = CHECKED_ON
        out.append(h)
    return out

# ---------------------------------------------------------------------------
# Hotel-venue walking pairs. Official addresses only; walking times blank.
# ---------------------------------------------------------------------------
def build_walking():
    pairs = []
    for h in HOTELS:
        for v in VENUES:
            pairs.append({
                "hotel_id": h["id"], "hotel": h["name"],
                "venue_id": v["id"], "venue": v["name"],
                "hotel_address": h["address_note"],
                "venue_address": v["address"],
                "walk_minutes": None,
                "walk_status": "unverified",
                "note": ("No official source publishes a walking time for this pair. Measure it with "
                         "a mapping service at walking pace and record the date; the site applies a "
                         "30-minute limit once a value is recorded."),
                "last_checked": CHECKED_ON,
            })
    return {
        "generated_on": CHECKED_ON,
        "limit_minutes": 30,
        "pairs": pairs,
        "method": ("One row per hotel-venue pair, with both official addresses. Walking minutes are "
                   "null because no official source publishes them. When a value is recorded it is "
                   "compared against the 30-minute limit and the row is labelled pass or fail. "
                   "Nothing is inferred."),
    }

# ---------------------------------------------------------------------------
# Hotel rate log (dated entries, not a single value). Empty until a dated
# official quote is captured.
# ---------------------------------------------------------------------------
def build_rate_log():
    return {
        "generated_on": CHECKED_ON,
        "entries": [],
        "schema": {
            "hotel_id": "hotel id from data/hotels.json",
            "check_in": "stay start date, YYYY-MM-DD",
            "check_out": "stay end date, YYYY-MM-DD",
            "nights": "number of nights",
            "occupancy": "guests and room type as quoted",
            "nightly_rate_usd": "nightly room rate as quoted",
            "resort_fee_usd": "mandatory resort fee per night",
            "tax_pct": "room tax percentage applied",
            "parking_usd": "parking fee per night (null if not quoted)",
            "checkout_total_usd": "total for the stay as shown at checkout",
            "nightly_average_usd": "checkout total / nights",
            "cancellation_deadline": "cancellation deadline as quoted",
            "rate_timestamp": "date and time the quote was captured",
            "source_url": "official booking page or official quote",
        },
        "method": ("Rates are kept as a dated log, one dated quote per row, so price movement over "
                   "your stay window is visible. No entry exists yet: no official dated quote has "
                   "been captured for any hotel. Third-party rates are not recorded."),
    }

# ---------------------------------------------------------------------------
# Change monitoring. The workflow records one dated snapshot per official source
# and flags any change. No snapshot has been taken yet beyond this initial one.
# ---------------------------------------------------------------------------
MONITOR_URLS = [
    {"label": "Venetian DeepStack IV event page", "url": SRC["dse_nov_page"], "kind": "html"},
    {"label": "Venetian DeepStack IV schedule (PDF)", "url": SRC["dse_nov_sched"], "kind": "pdf"},
    {"label": "Venetian DeepStack NYE event page", "url": SRC["dse_dec_page"], "kind": "html"},
    {"label": "Wynn poker room", "url": SRC["wynn_poker"], "kind": "html"},
    {"label": "WPT World Championship schedule (PDF)", "url": SRC["wpt_sched"], "kind": "pdf"},
    {"label": "WPT World Championship structures (PDF)", "url": SRC["wpt_struct"], "kind": "pdf"},
    {"label": "Wynn Signature Series schedule (PDF)", "url": SRC["wss_sched"], "kind": "pdf"},
    {"label": "Venetian hotel terms", "url": SRC["venetian_terms"], "kind": "html"},
    {"label": "Venetian resort fee", "url": SRC["venetian_fee"], "kind": "html"},
    {"label": "Wynn resort fee terms", "url": SRC["wynn_terms"], "kind": "html"},
]

def build_changelog():
    return {
        "generated_on": CHECKED_ON,
        "monitored": MONITOR_URLS,
        "snapshots": [],
        "method": ("A scheduled GitHub Actions job (.github/workflows/source-monitor.yml) fetches "
                   "each official URL above, stores a checksum in data/snapshots.json, and opens an "
                   "issue or commits a dated entry here whenever a checksum changes. Rows whose "
                   "source changed are then re-verified line by line. No automated run has completed "
                   "yet, so no change is recorded."),
    }

# ---------------------------------------------------------------------------
def main():
    rows = build_tournaments()
    with open(os.path.join(DATA, "tournaments.json"), "w") as f:
        json.dump({"generated_on": CHECKED_ON, "rows": rows, "sources": SRC,
                   "venues": VENUES}, f, indent=1)

    hotels = build_hotels()
    with open(os.path.join(DATA, "hotels.json"), "w") as f:
        json.dump({"generated_on": CHECKED_ON, "rows": hotels,
                   "method": ("True nightly cost is computed only when a dated room rate, a resort "
                              "fee and a property-specific tax rate are all verified. No hotel row "
                              "currently has all three. The Venetian terms state a $55 resort fee "
                              "plus applicable tax and a 13.38% Clark County Room Tax; that tax rate "
                              "is not copied to other properties without property-specific support.")},
                  f, indent=1)

    sched = build_schedule(rows)
    with open(os.path.join(DATA, "schedule.json"), "w") as f:
        json.dump(sched, f, indent=1)

    with open(os.path.join(DATA, "walking.json"), "w") as f:
        json.dump(build_walking(), f, indent=1)

    with open(os.path.join(DATA, "hotel_rates.json"), "w") as f:
        json.dump(build_rate_log(), f, indent=1)

    with open(os.path.join(DATA, "changelog.json"), "w") as f:
        json.dump(build_changelog(), f, indent=1)

    counts = {}
    for r in rows:
        counts[r["entry_status"]] = counts.get(r["entry_status"], 0) + 1
    print("total rows", len(rows), dict(sorted(counts.items())))
    for s in sorted({r["series"] for r in rows}):
        print("  ", s, sum(1 for r in rows if r["series"] == s))
    print("days with a verified primary event:", len(sched["days"]))
    print("earliest listed start:", sched["earliest_listed_start"])
    withsrc = sum(1 for r in rows if r["sources"])
    print("rows with at least one source:", withsrc)
    assert withsrc == len(rows), "every row must carry a source"
    ids = [r["id"] for r in rows]
    assert len(set(ids)) == len(ids), "row ids must be unique"

if __name__ == "__main__":
    main()
