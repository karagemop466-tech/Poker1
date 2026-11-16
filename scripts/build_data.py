#!/usr/bin/env python3
"""Builds data/*.json from official-source rows.

Two inputs:

  data/official_facts.json  written by scripts/collect_official.py (network).
                            Holds, for every official document, its SHA-256, its
                            fetch time, and the verbatim facts pulled from it.
                            When it is missing, the builder still runs and every
                            entry-rule field is left unverified.
  the curated source rows below (dates, names, buy-ins, guarantees, structure
                            sheet numbers, and WPT rules), each copied from an
                            official document and each carrying that URL.

Nothing is inferred. A field is null when the official document does not print
it, and such a row is listed as unverified in the site.
Run:  python3 scripts/build_data.py
"""
import json, os, re
from datetime import date, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
os.makedirs(DATA, exist_ok=True)

# ---------- when the curated rows below were last read against the official page
VERIFIED_ON = "2026-11-16"

FACTS_PATH = os.path.join(DATA, "official_facts.json")
FACTS = {}
if os.path.exists(FACTS_PATH):
    FACTS = json.load(open(FACTS_PATH, encoding="utf-8"))
STRUCTS = FACTS.get("structures", {})
DOCS = FACTS.get("documents", {})
FACTS_GENERATED = FACTS.get("generated_utc")

# ---------- official source URLs ----------
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

VENUES = {
    "venetian": {
        "id": "venetian", "name": "The Venetian Resort Las Vegas",
        "poker_room": "Venetian Poker Room (Grand Canal Shoppes level)",
        "street": "3355 S Las Vegas Blvd, Las Vegas, NV 89109",
        "street_source": "https://www.venetianlasvegas.com/",
        "poker_page": "https://www.venetianlasvegas.com/resort/casino/poker.html",
        "series": ["Venetian DeepStack Extravaganza IV", "Venetian DeepStack Extravaganza NYE"],
        "walk_note": ("Walking time from a hotel to this room is not published on any official "
                      "source, so no walking minutes are entered. The 30-minute test is "
                      "therefore unverified for every hotel."),
        "walk_minutes_published": None,
    },
    "wynn": {
        "id": "wynn", "name": "Wynn Las Vegas",
        "poker_room": "Wynn Poker Room",
        "street": "3131 S Las Vegas Blvd, Las Vegas, NV 89109",
        "street_source": "https://www.wynnlasvegas.com/",
        "poker_page": "https://www.wynnlasvegas.com/casino/poker",
        "series": ["WPT World Championship (Wynn)", "Wynn Signature Series"],
        "walk_note": ("Walking time from a hotel to this room is not published on any official "
                      "source, so no walking minutes are entered."),
        "walk_minutes_published": None,
    },
}

# ---------- Venetian DeepStack Extravaganza IV (events 1-64) ----------
# (date, time, event#, name, buy-in, guarantee, structure file number or None,
#  note). Structure file numbers are read off the official event page.
DSE_NOV = [
 ("2026-11-16","11:10",1,"$300 No Limit Hold'em 1A",300,75000,10,"Flight 1A of Event 1. Day 2 restarts 12:00 PM Nov 18."),
 ("2026-11-16","17:10",1,"$300 No Limit Hold'em 1B",300,75000,9,"Flight 1B of Event 1."),
 ("2026-11-17","11:10",1,"$300 No Limit Hold'em 1C",300,75000,10,"Flight 1C of Event 1."),
 ("2026-11-17","17:10",1,"$300 No Limit Hold'em 1D",300,75000,9,"Flight 1D of Event 1."),
 ("2026-11-18","11:10",2,"$300 No Limit Hold'em (1Day)",300,10000,5,"Single-day event."),
 ("2026-11-19","10:10",3,"$200 NLH RaceDay Stack (1Day)",200,None,18,"Race-to-finish format. Guarantee not printed on the event page row."),
 ("2026-11-20","10:10",4,"$200 NLH RaceDay Stack (1Day)",200,None,18,"Race-to-finish format. Guarantee not printed on the event page row."),
 ("2026-11-21","10:10",5,"$200 NLH RaceDay Stack (1Day)",200,None,18,"Race-to-finish format. Guarantee not printed on the event page row."),
 ("2026-11-22","11:10",6,"$200 No Limit Hold'em (1Day)",200,None,29,"Single-day event."),
 ("2026-11-23","11:10",7,"$400 No Limit Hold'em 1A",400,75000,2,"Flight 1A of Event 7. Day 2 restarts 11:00 AM Nov 25."),
 ("2026-11-23","17:10",8,"$200 No Limit Hold'em PKO Bounty (1Day)",200,8000,30,"Progressive knockout bounty."),
 ("2026-11-24","11:10",7,"$400 No Limit Hold'em 1B",400,75000,2,"Flight 1B of Event 7."),
 ("2026-11-24","17:10",9,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"$50 bounty per elimination. Guarantee includes bounties."),
 ("2026-11-25","11:10",10,"$400 No Limit Hold'em (1Day)",400,15000,6,"Single-day event."),
 ("2026-11-25","17:10",11,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"$50 bounty per elimination. Guarantee includes bounties."),
 ("2026-11-26","11:10",12,"$300 No Limit Hold'em (1Day)",300,10000,5,"Single-day event."),
 ("2026-11-26","17:10",13,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"$50 bounty per elimination. Guarantee includes bounties."),
 ("2026-11-27","11:10",14,"$600 No Limit Hold'em (1Day)",600,30000,7,"Single-day event."),
 ("2026-11-27","17:10",15,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"$50 bounty per elimination. Guarantee includes bounties."),
 ("2026-11-28","11:10",16,"$600 No Limit Hold'em Bounty (1Day)",600,30000,11,"$200 bounties to start and $500 in the money. Guarantee includes bounties."),
 ("2026-11-28","12:10",17,"$400 Pot Limit Omaha Bounty (1Day)",400,15000,26,"Pot Limit Omaha."),
 ("2026-11-28","17:10",18,"$200 NLH PokerAtlas Valuetown Bounty (1Day)",200,20000,8,"PokerAtlas Pro member $20 rake discount. Guarantee includes bounties."),
 ("2026-11-29","11:10",19,"$400 No Limit Hold'em 1A",400,75000,3,"Flight 1A of Event 19. Day 2 restarts 11:00 AM Dec 2."),
 ("2026-11-29","12:10",20,"$300 Pot Limit Omaha Double Board Bomb Pot (1Day)",300,10000,22,"Pot Limit Omaha bomb pot."),
 ("2026-11-29","17:10",21,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"$50 bounty per elimination. Guarantee includes bounties."),
 ("2026-11-30","11:10",19,"$400 No Limit Hold'em 1B",400,75000,3,"Flight 1B of Event 19."),
 ("2026-11-30","17:10",22,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"$50 bounty per elimination. Guarantee includes bounties."),
 ("2026-12-01","11:10",19,"$400 No Limit Hold'em 1C",400,75000,3,"Flight 1C of Event 19."),
 ("2026-12-01","17:10",23,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"$50 bounty per elimination. Guarantee includes bounties."),
 ("2026-12-02","10:10",24,"$600 No Limit Hold'em Seniors (1Day)",600,40000,17,"Eligibility: must be 50+."),
 ("2026-12-02","17:10",25,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"$50 bounty per elimination. Guarantee includes bounties."),
 ("2026-12-03","11:10",26,"$800 No Limit Hold'em 1A",800,500000,12,"Flight 1A of Event 26."),
 ("2026-12-03","12:10",27,"$600 Big O (1Day)",600,25000,28,"Big O (5-card Omaha hi-lo)."),
 ("2026-12-03","17:10",26,"$800 No Limit Hold'em 1B",800,500000,13,"Flight 1B of Event 26."),
 ("2026-12-04","11:10",26,"$800 No Limit Hold'em 1C",800,500000,12,"Flight 1C of Event 26."),
 ("2026-12-04","17:10",26,"$800 No Limit Hold'em 1D",800,500000,13,"Flight 1D of Event 26."),
 ("2026-12-05","11:10",26,"$800 No Limit Hold'em 1E",800,500000,12,"Flight 1E of Event 26."),
 ("2026-12-05","17:10",26,"$800 No Limit Hold'em 1F (Turbo)",800,500000,14,"Flight 1F of Event 26, turbo."),
 ("2026-12-06","11:10",28,"$600 No Limit Hold'em (1Day)",600,40000,7,"Single-day event."),
 ("2026-12-06","17:10",29,"$300 No Limit Hold'em Bounty (1Day)",300,15000,15,"$100 bounty per elimination. Guarantee includes bounties."),
 ("2026-12-07","11:10",30,"$600 No Limit Hold'em Bounty (1Day)",600,40000,11,"$200 bounties to start and $500 in the money. Guarantee includes bounties."),
 ("2026-12-07","17:10",31,"$300 No Limit Hold'em Bounty (1Day)",300,15000,15,"$100 bounty per elimination. Guarantee includes bounties."),
 ("2026-12-08","10:10",32,"$600 No Limit Hold'em Seniors (1Day)",600,40000,17,"Eligibility: must be 50+."),
 ("2026-12-08","17:10",34,"$300 No Limit Hold'em Bounty (1Day)",300,15000,15,"$100 bounty per elimination. Guarantee includes bounties."),
 ("2026-12-09","10:10",35,"$600 NLH LIPS Poker Jingle Tag Team (1Day)",600,10000,31,"Tag-team event: teams of female/female or female/male."),
 ("2026-12-09","11:10",36,"$800 No Limit Hold'em Bounty (1Day)",800,75000,16,"$200 bounties to start and $500 in the money. Guarantee includes bounties."),
 ("2026-12-09","17:10",38,"$300 No Limit Hold'em Bounty (1Day)",300,15000,15,"$100 bounty per elimination. Guarantee includes bounties."),
 ("2026-12-10","10:10",39,"$800 No Limit Hold'em LIPS Ladies (2Day)",800,40000,32,"Ladies event, two days. Day 2 restart 10:00 AM Dec 11, final table 7:00 PM."),
 ("2026-12-10","12:10",40,"$600 Pot Limit Omaha Bounty (1Day)",600,25000,27,"Pot Limit Omaha bounty."),
 ("2026-12-10","17:10",42,"$300 No Limit Hold'em Bounty (1Day)",300,15000,15,"$100 bounty per elimination. Guarantee includes bounties."),
 ("2026-12-11","11:10",43,"$600 No Limit Hold'em LIPS Kings and Queens Bounty (1Day)",600,30000,33,"Open to all players."),
 ("2026-12-12","10:10",47,"$2,200 No Limit Hold'em 1A",2200,1000000,21,"Flight 1A of the PokerAtlas Championship Title Event."),
 ("2026-12-12","18:10",47,"$2,200 No Limit Hold'em 1B",2200,1000000,37,"Flight 1B of the PokerAtlas Championship Title Event."),
 ("2026-12-13","10:10",49,"$1,100 No Limit Hold'em Seniors 1A",1100,300000,20,"Eligibility: must be 50+. Flight 1A."),
 ("2026-12-13","17:10",50,"$300 No Limit Hold'em Bounty (1Day)",300,15000,15,"$100 bounty per elimination. Guarantee includes bounties."),
 ("2026-12-14","10:10",49,"$1,100 No Limit Hold'em Seniors 1B",1100,300000,20,"Eligibility: must be 50+. Flight 1B."),
 ("2026-12-14","17:10",51,"$300 No Limit Hold'em Bounty (1Day)",300,15000,15,"$100 bounty per elimination. Guarantee includes bounties."),
 ("2026-12-15","11:10",52,"$1,100 No Limit Hold'em PKO Bounty (1Day)",1100,75000,34,"Progressive knockout bounty."),
 ("2026-12-15","17:10",53,"$300 No Limit Hold'em Bounty (1Day)",300,15000,15,"$100 bounty per elimination. Guarantee includes bounties."),
 ("2026-12-16","11:10",54,"$600 No Limit Hold'em Bounty (1Day)",600,50000,11,"$200 bounties to start and $500 in the money. Guarantee includes bounties."),
 ("2026-12-16","17:10",55,"$300 No Limit Hold'em Bounty (1Day)",300,15000,15,"$100 bounty per elimination. Guarantee includes bounties."),
 ("2026-12-17","10:10",56,"$1,100 No Limit Hold'em 1A",1100,500000,35,"Flight 1A. $40 rake discount for entries before 10:10 AM."),
 ("2026-12-17","12:10",57,"$600 Pot Limit Omaha Double Board Bomb Pot (1Day)",600,25000,23,"Pot Limit Omaha bomb pot."),
 ("2026-12-17","18:10",56,"$1,100 No Limit Hold'em 1B",1100,500000,36,"Flight 1B. $40 rake discount for entries before 6:10 PM."),
 ("2026-12-18","10:10",56,"$1,100 No Limit Hold'em 1C",1100,500000,35,"Flight 1C."),
 ("2026-12-18","18:10",56,"$1,100 No Limit Hold'em 1D",1100,500000,36,"Flight 1D."),
 ("2026-12-19","10:10",56,"$1,100 No Limit Hold'em 1E",1100,500000,35,"Flight 1E."),
 ("2026-12-19","17:10",58,"$200 NLH PokerAtlas Valuetown Bounty (1Day)",200,20000,8,"PokerAtlas Pro member $20 rake discount. Guarantee includes bounties."),
 ("2026-12-20","11:10",59,"$600 No Limit Hold'em 1A",600,150000,4,"Flight 1A. $20 rake discount for entries before 11:10 AM on Day 1A."),
 ("2026-12-20","17:10",60,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"$50 bounty per elimination. Guarantee includes bounties."),
 ("2026-12-21","11:10",59,"$600 No Limit Hold'em 1B",600,150000,4,"Flight 1B."),
 ("2026-12-21","17:10",61,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"$50 bounty per elimination. Guarantee includes bounties."),
 ("2026-12-22","11:10",59,"$600 No Limit Hold'em 1C",600,150000,4,"Flight 1C."),
 ("2026-12-22","17:10",62,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"$50 bounty per elimination. Guarantee includes bounties."),
 ("2026-12-23","11:10",63,"$600 No Limit Hold'em (1Day)",600,30000,7,"Single-day event."),
 ("2026-12-23","17:10",64,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"$50 bounty per elimination. Guarantee includes bounties."),
]

# ---------- Venetian DeepStack Extravaganza NYE (Dec 24 2026 - Jan 10 2027) ----------
DSE_NYE = [
 ("2026-12-24","11:10",1,"$400 No Limit Hold'em (1Day)",400,15000,1,""),
 ("2026-12-24","17:10",2,"$200 No Limit Hold'em Bounty (1Day)",200,8000,2,""),
 ("2026-12-25","11:10",3,"$400 No Limit Hold'em (1Day)",400,15000,1,""),
 ("2026-12-25","17:10",4,"$200 No Limit Hold'em Bounty (1Day)",200,8000,2,""),
 ("2026-12-26","11:10",5,"$600 No Limit Hold'em Bounty (1Day)",600,40000,3,""),
 ("2026-12-27","11:10",8,"$1,100 No Limit Hold'em 1A - Ante Up Championship",1100,300000,6,""),
 ("2026-12-28","11:10",8,"$1,100 No Limit Hold'em 1B - Ante Up Championship",1100,300000,6,""),
 ("2026-12-29","11:10",8,"$1,100 No Limit Hold'em 1C - Ante Up Championship",1100,300000,6,""),
 ("2026-12-29","17:10",13,"$200 No Limit Hold'em Bounty (1Day)",200,8000,2,""),
 ("2026-12-30","11:10",14,"$600 No Limit Hold'em (1Day)",600,50000,12,""),
 ("2026-12-31","11:10",17,"$400 No Limit Hold'em (1Day)",400,15000,1,""),
 ("2027-01-01","11:10",20,"$1,600 No Limit Hold'em MSPT 1A",1600,400000,8,""),
 ("2027-01-01","17:10",22,"$200 No Limit Hold'em Bounty (1Day)",200,8000,2,""),
 ("2027-01-02","11:10",20,"$1,600 No Limit Hold'em MSPT 1B",1600,400000,8,""),
 ("2027-01-02","17:10",25,"$200 NLH PokerAtlas Valuetown Bounty (1Day)",200,20000,9,""),
 ("2027-01-03","11:10",20,"$1,600 No Limit Hold'em MSPT 1C",1600,400000,8,""),
 ("2027-01-03","17:10",26,"$200 No Limit Hold'em Bounty (1Day)",200,8000,2,""),
 ("2027-01-04","11:10",27,"$250 No Limit Hold'em 1A $75K GTD (1Day)",250,75000,15,""),
 ("2027-01-04","17:10",27,"$250 No Limit Hold'em 1B $75K GTD (1Day)",250,75000,15,""),
 ("2027-01-05","11:10",27,"$250 No Limit Hold'em 1C $75K GTD (1Day)",250,75000,15,""),
 ("2027-01-05","17:10",27,"$250 No Limit Hold'em 1D $75K GTD (1Day)",250,75000,15,""),
 ("2027-01-06","11:10",28,"$400 No Limit Hold'em (1Day)",400,15000,11,""),
 ("2027-01-06","17:10",29,"$200 No Limit Hold'em Bounty (1Day) - CES badge $10 rake discount",200,8000,2,""),
 ("2027-01-07","11:10",30,"$300 No Limit Hold'em 1A $100K GTD (1Day)",300,100000,13,""),
 ("2027-01-07","17:10",30,"$300 No Limit Hold'em 1B $100K GTD (1Day)",300,100000,14,""),
 ("2027-01-08","11:10",30,"$300 No Limit Hold'em 1C $100K GTD (1Day)",300,100000,13,""),
 ("2027-01-08","17:10",30,"$300 No Limit Hold'em 1D $100K GTD (1Day)",300,100000,14,""),
 ("2027-01-09","11:10",30,"$300 No Limit Hold'em 1E $100K GTD (1Day)",300,100000,13,""),
 ("2027-01-09","17:10",30,"$300 No Limit Hold'em 1F $100K GTD (1Day)",300,100000,14,""),
 ("2027-01-10","10:10",31,"$400 No Limit Hold'em Seniors (1Day)",400,20000,10,""),
 ("2027-01-10","17:10",32,"$200 No Limit Hold'em Bounty (1Day)",200,8000,2,""),
]

# ---------- Wynn WPT World Championship (Nov 27 - Dec 21, 2026) ----------
# (date, time, name, label, buy-in, guarantee, rule, note)
WPT_RE = ("RE", "Official WPT structure terms: unlimited re-entry for each starting flight "
                "until the start of level 9.")
WPT = [
 ("2026-11-27","11:00","NLH Day 1A","$600 NLH $400K",600,400000,"RE","Flight 1A."),
 ("2026-11-27","12:00","TORSE","TORSE",600,None,"UNV","Mixed-game event."),
 ("2026-11-27","13:00","PLO","Pot Limit Omaha",400,None,"UNV","Pot Limit Omaha."),
 ("2026-11-27","17:00","NLH Day 1B","$600 NLH $400K",600,400000,"RE","Flight 1B."),
 ("2026-11-28","11:00","NLH Day 1C","$600 NLH $400K",600,400000,"RE","Flight 1C."),
 ("2026-11-28","12:00","Mixed Triple Draw (A-5, 2-7, Badugi)","Mixed Triple Draw",600,None,"UNV","Mixed game."),
 ("2026-11-28","17:00","NLH Day 1D","$600 NLH $400K",600,400000,"RE","Flight 1D."),
 ("2026-11-29","11:00","NLH Day 1E","$600 NLH $400K",600,400000,"RE","Flight 1E."),
 ("2026-11-29","18:00","NLH Day 1F","$600 NLH $400K",600,400000,"RE","Flight 1F."),
 ("2026-11-30","11:00","NLH Day 1A","$800 NLH $1M",800,1000000,"UNV","Flight 1A."),
 ("2026-11-30","12:00","Limit Omaha 8","Limit Omaha 8",600,None,"UNV","Limit Omaha hi-lo."),
 ("2026-11-30","17:00","NLH Day 1B","$800 NLH $1M",800,1000000,"UNV","Flight 1B."),
 ("2026-12-01","11:00","NLH Day 1C","$800 NLH $1M",800,1000000,"UNV","Flight 1C."),
 ("2026-12-01","12:00","Limit Omaha 8/5/Stud 8","Limit Omaha 8/5/Stud 8",600,None,"UNV","Mixed limit event."),
 ("2026-12-01","13:00","PLO","Pot Limit Omaha",1100,None,"UNV","Pot Limit Omaha."),
 ("2026-12-01","17:00","NLH Day 1D","$800 NLH $1M",800,1000000,"UNV","Flight 1D."),
 ("2026-12-02","11:00","NLH Day 1E","$800 NLH $1M",800,1000000,"UNV","Flight 1E."),
 ("2026-12-02","18:00","NLH Day 1F","$800 NLH $1M",800,1000000,"UNV","Flight 1F."),
 ("2026-12-03","11:00","NLH Day 1A","$1,600 NLH $1M",1600,1000000,"UNV","Flight 1A."),
 ("2026-12-04","11:00","NLH Day 1B","$1,600 NLH $1M",1600,1000000,"UNV","Flight 1B."),
 ("2026-12-04","12:00","HORSE","HORSE",600,None,"UNV","Mixed game."),
 ("2026-12-05","11:00","WPT Prime Championship Day 1A","WPT Prime Championship $5M",1100,5000000,"UNV","Flight 1A of the Prime Championship."),
 ("2026-12-05","21:00","NLH Turbo","NLH Turbo $50K",600,50000,"UNV","Late turbo."),
 ("2026-12-06","11:00","PLO Mystery Bounty Day 1A","PLO Mystery Bounty $500K",1600,500000,"UNV","Flight 1A."),
 ("2026-12-06","11:00","WPT Prime Championship Day 1B","WPT Prime Championship $5M",1100,5000000,"UNV","Flight 1B."),
 ("2026-12-06","18:00","PLO Mystery Bounty Day 1B","PLO Mystery Bounty $500K",1600,500000,"UNV","Flight 1B."),
 ("2026-12-06","21:00","NLH Turbo","NLH Turbo $50K",600,50000,"UNV","Late turbo."),
 ("2026-12-07","11:00","HORSE (2 Day)","HORSE (2 Day)",1100,None,"UNV","Two-day mixed game."),
 ("2026-12-07","11:00","WPT Prime Championship Day 1C","WPT Prime Championship $5M",1100,5000000,"UNV","Flight 1C."),
 ("2026-12-07","13:00","PLO $500 Bounty","PLO $500 Bounty $100K",1600,100000,"UNV","Bounty event."),
 ("2026-12-07","21:00","NLH Turbo","NLH Turbo $50K",600,50000,"UNV","Late turbo."),
 ("2026-12-08","11:00","WPT Prime Championship Day 1D","WPT Prime Championship $5M",1100,5000000,"UNV","Flight 1D."),
 ("2026-12-08","21:00","NLH Turbo","NLH Turbo $50K",600,50000,"UNV","Late turbo."),
 ("2026-12-09","11:00","No Limit Hold'em (2 Day)","NLH (2 Day) $1M",1600,1000000,"UNV","Two-day event."),
 ("2026-12-09","13:00","PLO $1,000 Bounty","PLO $1,000 Bounty $250K",3000,250000,"UNV","Bounty event."),
 ("2026-12-09","13:00","Limit Omaha 8","Limit Omaha 8",800,None,"UNV","Limit Omaha hi-lo."),
 ("2026-12-09","21:00","NLH Turbo","NLH Turbo $50K",600,50000,"UNV","Late turbo."),
 ("2026-12-10","10:00","Super Gold Million Mystery Bounty Day 1A","Super Gold Million $3M",400,3000000,"UNV","Flight 1A. Earliest start in this dataset."),
 ("2026-12-10","18:00","Super Gold Million Mystery Bounty Day 1B","Super Gold Million $3M",400,3000000,"UNV","Flight 1B."),
 ("2026-12-11","10:00","Super Gold Million Mystery Bounty Day 1C","Super Gold Million $3M",400,3000000,"UNV","Flight 1C."),
 ("2026-12-11","18:00","Super Gold Million Mystery Bounty Day 1D","Super Gold Million $3M",400,3000000,"UNV","Flight 1D."),
 ("2026-12-12","10:00","No Limit Hold'em","NLH $100K",800,100000,"UNV","Single-day."),
 ("2026-12-12","13:00","PLO","PLO $250K",3000,250000,"UNV","Pot Limit Omaha."),
 ("2026-12-12","21:00","NLH Turbo","NLH Turbo $50K",600,50000,"UNV","Late turbo."),
 ("2026-12-13","11:00","WPT World Championship Day 1A ($1M added)","WPT World Championship",10400,None,"UNV","Official footnote: $1M added by ClubWPT Gold, which the footnote says is not available in Nevada. Flagged."),
 ("2026-12-13","11:00","Ladies NIH (sic) Championship (2 Day)","Ladies Championship $250K",1100,250000,"UNV","Printed name reads NIH. Footnote prints an $11,100 entry with a discounted ladies entry. Flagged."),
 ("2026-12-13","11:00","No Limit Hold'em Day 1A","NLH $500K",800,500000,"UNV","Flight 1A."),
 ("2026-12-13","12:00","PLO Day 1A","PLO $1M",1600,1000000,"UNV","Flight 1A."),
 ("2026-12-14","11:00","WPT World Championship Day 1B ($1M added)","WPT World Championship",10400,None,"UNV","ClubWPT Gold footnote. Flagged."),
 ("2026-12-14","11:00","No Limit Hold'em Day 1B","NLH $500K",800,500000,"UNV","Flight 1B."),
 ("2026-12-14","12:00","PLO Day 1B","PLO $1M",1600,1000000,"UNV","Flight 1B."),
 ("2026-12-14","12:00","Mixed Triple Draw (2 Day)","Mixed Triple Draw (2 Day)",1100,None,"UNV","Two-day mixed game."),
 ("2026-12-14","19:00","PLO Turbo","PLO Turbo $100K",1100,100000,"UNV","Evening turbo."),
 ("2026-12-14","21:00","NLH Turbo","NLH Turbo $50K",600,50000,"UNV","Late turbo."),
 ("2026-12-15","11:00","WPT World Championship Day 1C ($1M added)","WPT World Championship",10400,None,"UNV","ClubWPT Gold footnote. Flagged."),
 ("2026-12-15","12:00","Big O","Big O",1100,None,"UNV","Big O (5-card Omaha hi-lo)."),
 ("2026-12-15","13:00","PLO Progressive Bounty (PKO)","PLO PKO $250K",3000,250000,"UNV","Progressive knockout."),
 ("2026-12-15","19:00","NIH (sic) $500 Bounty Turbo","NLH $500 Bounty Turbo $100K",1600,100000,"UNV","Printed name reads NIH. Bounty turbo."),
 ("2026-12-17","11:00","Seniors NLH Championship (3 Day)","Seniors NLH $500K",1100,500000,"UNV","Seniors event; age requirement not printed on the schedule row read. Three days."),
 ("2026-12-17","11:00","Wynn Mixed Championship (2 Day)","Wynn Mixed Championship (2 Day)",1600,None,"UNV","Two-day mixed game."),
 ("2026-12-17","12:00","No Limit Hold'em Day 1A","NLH $2M",3000,2000000,"UNV","Flight 1A."),
 ("2026-12-17","13:00","NLH High Roller (2 Day)","NLH High Roller (2 Day)",25800,None,"UNV","Two-day high roller."),
 ("2026-12-18","11:00","No Limit Hold'em Day 1A","NLH $1M",1100,1000000,"UNV","Flight 1A."),
 ("2026-12-18","12:00","PLO Double Board Bomb Pot","PLO Double Board Bomb Pot",800,None,"UNV","Bomb pot."),
 ("2026-12-18","12:00","No Limit Hold'em Day 1B","NLH $2M",3000,2000000,"UNV","Flight 1B."),
 ("2026-12-18","12:00","Limit Omaha 8 Championship (2 Day)","Limit Omaha 8 Championship (2 Day)",1600,None,"UNV","Two-day limit event."),
 ("2026-12-18","12:00","No Limit Hold'em","NLH $100K",600,100000,"UNV","Single-day."),
 ("2026-12-18","13:00","PLO 6-Max","PLO 6-Max",10500,None,"UNV","Six-handed."),
 ("2026-12-18","13:00","HORSE","HORSE",800,None,"UNV","Mixed game."),
 ("2026-12-18","13:00","NLH 6-Max","NLH 6-Max",10500,None,"UNV","Six-handed."),
 ("2026-12-18","18:00","NLH Turbo","NLH Turbo $100K",1100,100000,"UNV","Evening turbo."),
 ("2026-12-18","19:00","No Limit Hold'em Day 1B","NLH $1M",1100,1000000,"UNV","Flight 1B."),
 ("2026-12-19","11:00","Seniors High Roller (3 Day)","Seniors High Roller $250K",5000,250000,"UNV","Seniors event. Three days."),
 ("2026-12-19","11:00","NLH Mystery Bounty Day 1A","NLH Mystery Bounty $1M",1600,1000000,"UNV","Flight 1A."),
 ("2026-12-19","13:00","PLO","PLO",10500,None,"UNV","Pot Limit Omaha."),
 ("2026-12-19","13:00","NLH 6-Max","NLH 6-Max $500K",3000,500000,"UNV","Six-handed."),
 ("2026-12-19","13:00","TORSE Championship (2 Day)","TORSE Championship (2 Day)",1600,None,"UNV","Two-day mixed game."),
 ("2026-12-19","18:00","NLH 6-Max Turbo","NLH 6-Max Turbo $50K",600,50000,"UNV","Evening turbo."),
 ("2026-12-19","19:00","NLH Mystery Bounty Day 1B","NLH Mystery Bounty $1M",1600,1000000,"UNV","Flight 1B."),
 ("2026-12-20","11:00","NLH Mystery Bounty Day 1C","NLH Mystery Bounty $1M",1600,1000000,"UNV","Flight 1C."),
 ("2026-12-20","12:00","No Limit Hold'em","NLH $50K",600,50000,"UNV","Single-day."),
 ("2026-12-20","13:00","NLH 8-Max","NLH 8-Max",10500,None,"UNV","Eight-handed."),
 ("2026-12-20","13:00","Mixed Triple Draw","Mixed Triple Draw",600,None,"UNV","Mixed game."),
 ("2026-12-20","18:00","5-Card PLO Turbo","5-Card PLO Turbo $50K",600,50000,"UNV","Evening turbo."),
 ("2026-12-20","19:00","NLH Mystery Bounty Day 1D","NLH Mystery Bounty $1M",1600,1000000,"UNV","Flight 1D."),
 ("2026-12-21","12:00","No Limit Hold'em","NLH $100K",1100,100000,"UNV","Single-day."),
 ("2026-12-21","20:00","NLH Turbo","NLH Turbo $50K",600,50000,"UNV","Late turbo."),
]

# ---------- Wynn Signature Series (Jan 11 - 24, 2027) ----------
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
WSS_NOTE = "Buy-in and guarantee from the official Wynn Signature Series schedule PDF."

# ------------------------------------------------------------ entry rules --
# Rules are decided only from what an official document prints. The decision is
# a function of (a) verbatim re-entry / rebuy / add-on keyword hits on the sheet,
# (b) whether the sheet's own text describes starting flights, and (c) the
# numbered clause the hit came from. Nothing is assumed.
SE_LABEL = "Single entry (verified)"
RE_LABEL = "Re-entry offered (verified)"
MULTI_LABEL = "Possible multiple entries"
UNV_LABEL = "Unverified"


def structure_for(series_key, number):
    if series_key == "nov":
        key = "dse_nov_2026-structure_%d.pdf" % number
    else:
        key = "dse_dec_2026-structure_%d.pdf" % number
    return STRUCTS.get(key), key


def classify_venetian(sheet_no, series_key):
    """Return (entry_status, structured rule fields, source excerpt).

    Decision inputs, all from the official structure sheet:
      * verbatim hits for re-entry / rebuy / add-on / multiple-entry wording
      * the sheet's own clause 8 text
      * whether the sheet prints numbered rules at all
    A sheet that prints no re-entry wording and no multi-flight clause is
    recorded as single entry. A sheet that prints the multi-flight clause is not.
    """
    facts, key = structure_for(series_key, sheet_no)
    url = (SRC["dse_nov_struct"] if series_key == "nov" else SRC["dse_dec_struct"]).format(sheet_no)
    base = {
        "single_entry": None, "re_entry": None, "rebuy": None, "add_on": None,
        "flights_offered": None, "entries_allowed": None,
        "source_url": url, "structure_sheet": key,
        "retrieved": (facts or {}).get("fetched_utc"),
        "fetched": bool(facts),
        "excerpts": {},
    }
    if not facts:
        base["note"] = ("The official structure sheet was not retrieved by the collector, so the "
                        "entry rule is blank and the row is unverified.")
        return "UNV", base, "Official structure sheet not retrieved."

    ex = base["excerpts"]
    kws = facts.get("keywords") or []
    cash_entry = [k for k in kws if re.search(
        r"re-?entr|rebu|add-?\s?on|multiple entr|subsequent buy", k["keyword"], re.I)]
    clause8 = facts.get("clause_08_sentence") or facts.get("clause_08") or ""
    multi_flight = bool(facts.get("mentions_players_may_not_play_subsequent_flight")) or \
        bool(re.search(r"bags? chips", clause8, re.I))
    if clause8:
        ex["clause_08"] = clause8[:400]
    if facts.get("late_registration"):
        ex["late_registration"] = facts["late_registration"][:200]
    if cash_entry:
        ex["cash_entry_wording"] = cash_entry[0]["excerpt"][:400]
    if facts.get("house_fee_clause"):
        ex["house_fee"] = facts["house_fee_clause"][:300]
    if facts.get("late_registration"):
        ex["late_registration"] = facts["late_registration"][:200]

    base["flights_offered"] = multi_flight
    base["rebuy"] = None
    base["add_on"] = None
    base["house_fee"] = facts.get("house_fee")
    base["buy_in"] = facts.get("buy_in")
    base["levels_printed"] = facts.get("levels_printed")
    base["level_minutes"] = facts.get("level_minutes")

    if cash_entry:
        base["single_entry"] = False
        base["re_entry"] = True
        txt = cash_entry[0]["excerpt"]
        if re.search(r"subsequent re-?entry", txt, re.I):
            base["note"] = ("The official sheet refers to 'any subsequent re-entry' when it describes "
                            "who qualifies for the rake discount, which implies more than one entry is "
                            "permitted for this event. Not counted as single entry.")
        elif re.search(r"subsequent buy", txt, re.I):
            base["note"] = ("The official sheet prints 'All subsequent buy in's after the initial buy in "
                            "will be $200', which implies a second buy-in is possible. Not counted as "
                            "single entry.")
        else:
            base["note"] = ("The official sheet prints cash-entry wording: '%s'. Not counted as single "
                            "entry." % txt[:220])
        return "RE", base, txt[:400]

    if multi_flight:
        base["single_entry"] = False
        base["re_entry"] = None
        base["entries_allowed"] = "one entry per starting flight"
        base["note"] = ("The official sheet prints clause 8: '%s'. A player who bags chips may "
                        "not play a later flight. The sheet does not say that a player who busts "
                        "may enter a later flight, so this row is not counted as single entry."
                        % clause8[:260])
        return "MULTI", base, clause8[:400]

    base["single_entry"] = True
    base["re_entry"] = False
    base["entries_allowed"] = "single entry"
    base["note"] = ("The official sheet was read: no re-entry, rebuy, add-on, multiple-entry or "
                    "multi-flight clause appears. Verified single entry.")
    return "SE", base, "No re-entry, rebuy, add-on or multi-flight clause appears on the official sheet."


WPT_EVENTS = (FACTS.get("series", {}).get("wpt_structures", {}) or {}).get("events", [])


def _norm(t):
    t = re.sub(r"[^a-z0-9 ]+", " ", (t or "").lower())
    return re.sub(r"\s+", " ", t).strip()


def _wpt_key(name, label):
    """The WPT schedule's own wording for an event, e.g. 'NLH Day 1A' + '$600 NLH $400K'."""
    text = _norm(label)
    m = re.search(r"\$([\d,]+)", text)
    fee = int(m.group(1).replace(",", "")) if m else None
    return text, fee, _norm(name)


GAME_WORDS = [
    ("no limit holdem", "nlh"), ("nlh", "nlh"), ("plo", "plo"), ("pot limit omaha", "plo"),
    ("limit omaha", "lo8"), ("horse", "horse"), ("torse", "torse"), ("big o", "bigo"),
    ("mixed triple draw", "mtd"), ("triple draw", "mtd"), ("toe", "toe"), ("stud", "stud"),
]
TYPE_WORDS = [
    ("mystery bounty", "mystery"), ("progressive", "pko"), ("pko", "pko"), ("bounty", "bounty"),
    ("turbo", "turbo"), ("high roller", "highroller"), ("6 max", "6max"), ("8 max", "8max"),
    ("6max", "6max"), ("8max", "8max"), ("shootout", "shootout"),
]
SPECIAL_WORDS = [("super gold", "supergold"), ("prime", "prime"), ("ladies", "ladies"),
                 ("senior", "senior"), ("championship", "champ"), ("main event", "champ"),
                 ("wynn mixed", "mixedchamp"), ("bomb pot", "bombpot")]


def _sig(text):
    t = " " + _norm(text) + " "
    games = {tag for word, tag in GAME_WORDS if word in t}
    types = {tag for word, tag in TYPE_WORDS if word in t}
    specials = {tag for word, tag in SPECIAL_WORDS if word in t}
    return games, types, specials


def _day_pairs(ev):
    return {(d.get("date"), d.get("start")) for d in (ev.get("day_listing") or [])}


def match_wpt(name, label, buy, date=None, start=None):
    """Match a WPT schedule row to its official terms page.

    Primary test: the terms page prints the exact day(s) and start time the
    structure applies to. A row matches when its own date and start time appear
    in that printed list. This needs no string heuristics.

    Fallback test (only when no date match exists): the entry fee printed on the
    event's front page plus the game and format words. A tie is refused, so an
    ambiguous row stays unverified rather than being matched to the wrong event.
    """
    if date and start:
        hits = [ev for ev in WPT_EVENTS if (date, start) in _day_pairs(ev)]
        if len(hits) == 1:
            ev = dict(hits[0])
            ev["match_basis"] = "the terms page prints this event on %s at %s" % (date, start)
            return ev
        if len(hits) > 1:
            hits.sort(key=lambda e: -len(e.get("event_dates") or []))
            ev = dict(hits[0])
            ev["match_basis"] = ("several terms pages list %s at %s; the one with the shortest "
                                 "listed run was used" % (date, start))
            return ev

    sched_text = (name or "") + " " + (label or "")
    g_s, t_s, sp_s = _sig(sched_text)
    gtd = None
    m = re.search(r"\$(\d+(?:\.\d+)?)\s*([KkMm])\b", sched_text)
    if m:
        gtd = int(float(m.group(1)) * (1000 if m.group(2).upper() == "K" else 1000000))
    candidates = []
    for ev in WPT_EVENTS:
        if ev.get("structure_entry_fee_usd") != buy:
            continue
        g_e, t_e, sp_e = _sig(ev.get("structure_title"))
        if g_s and g_e and not (g_s & g_e):
            continue
        title = _norm(ev.get("structure_title"))
        if "torse" in (t_s | g_s) and "torse" not in title:
            continue
        if "turbo" in t_s and "turbo" not in title:
            continue
        if "mystery" in t_s and "mystery" not in title:
            continue
        score = 0
        if gtd is not None and ev.get("structure_guarantee_usd"):
            score += 12 if ev["structure_guarantee_usd"] == gtd else -8
        score += 6 * len(sp_s & sp_e) + 4 * len(t_s & t_e) + 2 * (1 if (g_s & g_e) else 0)
        candidates.append((score, ev))
    if not candidates:
        return None
    candidates.sort(key=lambda x: -x[0])
    if candidates[0][0] <= 0:
        return None
    if len(candidates) > 1 and candidates[1][0] == candidates[0][0]:
        return None
    ev = dict(candidates[0][1])
    ev["match_basis"] = "entry fee and printed game and format wording"
    return ev


def classify_wynn(status, name="", label="", buy=None, date=None, start=None):
    ev = match_wpt(name, label, buy, date, start) if (name or label) else None
    base = {
        "single_entry": None, "re_entry": None, "rebuy": None, "add_on": None,
        "flights_offered": None, "entries_allowed": None,
        "source_url": SRC["wpt_struct"],
        "structure_sheet": "WPT_World_Championship_Structures.pdf",
        "retrieved": (FACTS.get("series", {}).get("wpt_structures", {}) or {}).get("fetched_utc"),
        "fetched": bool(ev), "excerpts": {},
        "house_fee": None, "buy_in": None, "levels_printed": None, "level_minutes": None,
    }
    if not ev:
        base["note"] = ("The official WPT structures document has not been matched to this row, so the "
                        "entry rule is blank and unverified.")
        return "UNV", base, "WPT terms page not matched to this row."
    ex = base["excerpts"]
    if ev.get("registration_rule"):
        ex["re_entry"] = ev["registration_rule"][:420]
    if ev.get("entry_fee_breakdown"):
        ex["entry_fee"] = ev["entry_fee_breakdown"][:260]
    if ev.get("starting_stack"):
        base["starting_stack"] = ev["starting_stack"]
    base["levels_printed"] = ev.get("levels_printed")
    base["level_minutes"] = ev.get("level_minutes")
    reg = ev.get("registration_rule") or ""
    m = re.search(r"\$([\d,]+) \(Tournament Fee\)", ev.get("entry_fee_breakdown") or "")
    m2 = re.search(r"\$([\d,]+) \(Poker Staff Service Charge\)", ev.get("entry_fee_breakdown") or "")
    if m or m2:
        base["house_fee"] = (int(m.group(1).replace(",", "")) if m else 0) + \
                            (int(m2.group(1).replace(",", "")) if m2 else 0)
        base["buy_in"] = ev.get("structure_entry_fee_usd")
    if re.search(r"re-?entr|rebu|add-?\s?on", reg, re.I):
        base["single_entry"] = False
        base["re_entry"] = True
        if re.search(r"unlimited re-?entry", reg, re.I):
            base["entries_allowed"] = "unlimited re-entry"
        elif re.search(r"one \(1\) entr", reg, re.I):
            base["entries_allowed"] = "one entry plus one re-entry"
        base["note"] = ("Official WPT terms for this event print: '%s'. Not single entry." % reg[:320])
        return "RE", base, reg[:420]
    if re.search(r"no re-?entr|single entr|freeze-?out", reg + " " + (ev.get("structure_title") or ""), re.I):
        base["single_entry"] = True
        base["re_entry"] = False
        base["entries_allowed"] = "single entry"
        base["note"] = ("Official WPT terms print no re-entry: '%s'." % reg[:320])
        return "SE", base, reg[:420]
    base["note"] = ("Official WPT terms were read but do not state a re-entry rule: '%s'. Left "
                    "unverified." % reg[:320])
    return "UNV", base, "WPT terms do not state a re-entry rule."


def last_checked(urls):
    """Latest fetch time recorded for any of the given official URLs."""
    times = [DOCS[u]["fetched_utc"] for u in urls
             if u in DOCS and DOCS[u].get("fetched_utc")]
    return max(times) if times else VERIFIED_ON


def changed_status(urls):
    if any(DOCS.get(u, {}).get("changed_since_first_seen") for u in urls):
        return True
    return False


def build_tournaments():
    rows = []

    def emit(record):
        rows.append(record)

    def venetian(series_key, series_name, page_key, entries):
        for date, time, no, name, buy, gtd, sheet, note in entries:
            if sheet is None:
                status, rule, excerpt = "UNV", {
                    "single_entry": None, "re_entry": None, "rebuy": None, "add_on": None,
                    "flights_offered": None, "entries_allowed": None,
                    "source_url": SRC[page_key], "structure_sheet": None,
                    "retrieved": None, "fetched": False, "excerpts": {},
                    "note": "The official event page row does not link a structure sheet.",
                }, "No structure sheet linked from the official event page row."
            else:
                status, rule, excerpt = classify_venetian(sheet, series_key)
            srcs = [{"label": "Official event page (schedule row)", "url": SRC[page_key]}]
            if sheet is not None:
                srcs.append({
                    "label": "Official structure sheet %d (PDF)" % sheet,
                    "url": (SRC["dse_nov_struct"] if series_key == "nov"
                            else SRC["dse_dec_struct"]).format(sheet),
                })
            urls = [s["url"] for s in srcs]
            fee = rule.get("house_fee")
            buy_printed = rule.get("buy_in")
            fee_pct = None
            if rule.get("fetched") and buy_printed and buy_printed != buy:
                note = note + (" Structure sheet prints a $%d buy-in for sheet events %s, "
                               "which is the sheet for a different event number. Fee shown "
                               "as blank." % (buy_printed, rule.get("structure_sheet")))
                fee = None
            elif fee and buy:
                fee_pct = round(100.0 * fee / buy, 2)
            emits = {
                "id": "", "series": series_name, "venue_id": "venetian",
                "venue": "The Venetian Resort Las Vegas",
                "date": date, "start": time, "event_no": no, "name": name,
                "buy_in_usd": buy, "guarantee_usd": gtd,
                "guarantee_includes_bounties": bool(gtd and "bount" in name.lower()),
                "is_bounty": "bount" in name.lower(),
                "is_flight": bool(re.search(r"\b1[A-F]\b", name)) or "Flight" in note,
                "house_fee_usd": fee, "house_fee_pct": fee_pct,
                "gtd_multiple": round(gtd / buy, 2) if gtd and buy else None,
                "entry_status": status, "entry_label": {
                    "SE": SE_LABEL, "RE": RE_LABEL, "MULTI": MULTI_LABEL, "UNV": UNV_LABEL}[status],
                "entry_rule": excerpt, "rules": rule,
                "note": note, "sources": srcs,
                "last_checked": last_checked(urls),
                "source_changed": changed_status(urls),
                "verified_on": VERIFIED_ON,
            }
            emit(emits)

    venetian("nov", "Venetian DeepStack Extravaganza IV", "dse_nov_page", DSE_NOV)
    venetian("dec", "Venetian DeepStack Extravaganza NYE", "dse_dec_page", DSE_NYE)

    for date, time, name, label, buy, gtd, status, note in WPT:
        st, rule, excerpt = classify_wynn(status, name, label, buy, date, time)
        srcs = [{"label": "Official WPT schedule (PDF)", "url": SRC["wpt_sched"]},
                {"label": "Official WPT structures and terms (PDF)", "url": SRC["wpt_struct"]}]
        urls = [s["url"] for s in srcs]
        emit({
            "id": "", "series": "WPT World Championship (Wynn)", "venue_id": "wynn",
            "venue": "Wynn Las Vegas",
            "date": date, "start": time, "event_no": None,
            "name": name + " | " + label, "buy_in_usd": buy, "guarantee_usd": gtd,
            "guarantee_includes_bounties": bool(gtd and "bount" in label.lower()),
            "is_bounty": "bount" in label.lower(),
            "is_flight": "Day 1" in name,
            "house_fee_usd": None, "house_fee_pct": None,
            "gtd_multiple": round(gtd / buy, 2) if gtd and buy else None,
            "entry_status": st, "entry_label": {
                "SE": SE_LABEL, "RE": RE_LABEL, "MULTI": MULTI_LABEL, "UNV": UNV_LABEL}[st],
            "entry_rule": excerpt, "rules": rule, "note": note, "sources": srcs,
            "last_checked": last_checked(urls), "source_changed": changed_status(urls),
            "verified_on": VERIFIED_ON,
        })

    for date, time, name, buy, gtd in WSS:
        srcs = [{"label": "Official Wynn Signature Series schedule (PDF)", "url": SRC["wss_sched"]}]
        urls = [s["url"] for s in srcs]
        emit({
            "id": "", "series": "Wynn Signature Series", "venue_id": "wynn",
            "venue": "Wynn Las Vegas",
            "date": date, "start": time, "event_no": None, "name": name,
            "buy_in_usd": buy, "guarantee_usd": gtd,
            "guarantee_includes_bounties": False, "is_bounty": False,
            "is_flight": "Day 1" in name,
            "house_fee_usd": None, "house_fee_pct": None,
            "gtd_multiple": round(gtd / buy, 2) if gtd and buy else None,
            "entry_status": "UNV", "entry_label": UNV_LABEL,
            "entry_rule": "Official structure document not yet read by the collector.",
            "rules": {"single_entry": None, "re_entry": None, "rebuy": None, "add_on": None,
                      "flights_offered": None, "entries_allowed": None,
                      "source_url": SRC["wss_sched"], "structure_sheet": None,
                      "retrieved": None, "fetched": False, "excerpts": {},
                      "note": "The Wynn Signature Series schedule PDF does not link per-event "
                              "structure sheets that the collector could read."},
            "note": WSS_NOTE, "sources": srcs,
            "last_checked": last_checked(urls), "source_changed": changed_status(urls),
            "verified_on": VERIFIED_ON,
        })

    rows.sort(key=lambda x: (x["date"], x["start"], x["name"]))
    for i, row in enumerate(rows, 1):
        row["id"] = "r%03d" % i
    return rows


# ------------------------------------------------------- overlap / day plan --
EXIT_BUFFER_MIN = 45         # time to leave one event, walk, and register for the next

# Confirmed walking times are not published on any official source, so no walk
# minutes are entered. The fallback test therefore uses the primary event's
# published late-registration close, which is a printed time on official sheets.
WALK_PLACEHOLDER_MIN = 0     # an unverified walk adds no minutes to the test


def minutes(hhmm):
    if not hhmm:
        return None
    h, m = int(hhmm[:2]), int(hhmm[3:])
    return h * 60 + m


def hhmm(total):
    total = total % (24 * 60)
    return "%02d:%02d" % (total // 60, total % 60)


def late_reg_close(row):
    """Latest time a player can still enter, taken from the official sheet's own
    'Late Registration' line (for example '8 levels + Break (9:40 PM)')."""
    rules = row.get("rules") or {}
    text = rules.get("excerpts", {}).get("late_registration")
    if not text:
        return None, None
    m = re.search(r"(\d{1,2}):(\d{2})\s*([AP])\.?\s*M", text)
    if not m:
        return None, None
    h = int(m.group(1)) % 12
    if m.group(3).upper() == "P":
        h += 12
    return "%02d:%s" % (h, m.group(2)), "printed on the official sheet as '%s'" % text.split("  ")[0]


def estimated_finish(row):
    """Estimate only, clearly labelled: start + levels printed x level minutes.
    The operator prints no finish time, so this is marked as an estimate and is
    never used as the sequence test."""
    rules = row.get("rules") or {}
    lvl = rules.get("level_minutes")
    levels = rules.get("levels_printed")
    st = minutes(row.get("start"))
    if not (lvl and levels and st is not None):
        return None, None
    total = st + int(lvl) * int(levels)
    return hhmm(total), ("%s levels of %s minutes after the %s start, breaks excluded"
                         % (levels, lvl, row.get("start")))


def build_schedule(rows):
    """One primary event and, where the printed times allow it, one conditional
    fallback per day.

    Sequence test: the fallback can be reached only if it starts at least
    EXIT_BUFFER_MIN minutes after the primary's printed late-registration close.
    If the primary closes late registration after the fallback starts, the two
    cannot be played in sequence and the row is labelled a conflict.
    """
    se = [r for r in rows if r["entry_status"] == "SE"]
    by_day = {}
    for r in se:
        by_day.setdefault(r["date"], []).append(r)
    days = []
    for d in sorted(by_day):
        evs = sorted(by_day[d], key=lambda e: (e["start"], e["name"]))
        primary = evs[0]
        close, close_basis = late_reg_close(primary)
        opts = []
        for e in evs:
            est, est_basis = estimated_finish(e)
            entry = {
                "id": e["id"], "start": e["start"], "name": e["name"], "series": e["series"],
                "buy_in_usd": e["buy_in_usd"], "guarantee_usd": e["guarantee_usd"],
                "venue_id": e["venue_id"], "entry_status": e["entry_status"],
                "late_reg_close": close if e is primary else None,
                "estimated_finish": est,
                "sequence_check": None, "sequence_note": None,
                "source": e["sources"][-1]["url"],
            }
            if e is not primary:
                if close is None:
                    entry["sequence_check"] = "unknown"
                    entry["sequence_note"] = ("The primary's late-registration close is not printed on "
                                               "the official sheet, so the sequence cannot be tested.")
                else:
                    gap = minutes(e["start"]) - minutes(close)
                    entry["sequence_note"] = (
                        "Fallback starts %d minutes after the primary's late-registration close (%s)."
                        % (gap, close))
                    entry["sequence_check"] = "ok" if gap >= EXIT_BUFFER_MIN else "conflict"
            opts.append(entry)
        fallback = next((o for o in opts[1:] if o["sequence_check"] == "ok"), None)
        conflict = next((o for o in opts[1:] if o["sequence_check"] == "conflict"), None)
        days.append({
            "date": d,
            "primary": opts[0],
            "fallback": fallback,
            "later_event_that_conflicts": conflict,
            "sequence_basis": close_basis or ("Late-registration close not printed for this event, so "
                                              "no sequence is asserted."),
            "conditional_note": (
                None if fallback else
                ("No later verified single-entry event on this day starts at least %d minutes after the "
                 "primary's late-registration close. The later event listed below is an alternative, not "
                 "a sequence." % EXIT_BUFFER_MIN)),
            "options": opts,
        })
    starts = sorted({r["start"] for r in rows})
    return {
        "verified_on": VERIFIED_ON,
        "facts_generated_utc": FACTS_GENERATED,
        "days": days,
        "earliest_listed_start": starts[0] if starts else None,
        "exit_buffer_min": EXIT_BUFFER_MIN,
        "note": ("Primary = the earliest verified single-entry start that day. A fallback is listed only when "
                 "it starts at least %d minutes after the primary's late-registration close, which is a time "
                 "printed on the official structure sheet. Finish times are not printed by the operator; the "
                 "'estimated finish' shown is levels x level length and is labelled an estimate. No official "
                 "walking time is published, so no walking minutes are added." % EXIT_BUFFER_MIN),
    }


# ------------------------------------------------------------------ hotels --
HOTELS = [
 {"id":"venetian","name":"The Venetian Resort Las Vegas","venue_id":"venetian",
  "address_note":"3355 S Las Vegas Blvd. The poker room is at The Palazzo level 2, Grand Canal Shoppes (official poker page).",
  "resort_fee_usd":55,"resort_fee_status":"verified",
  "resort_fee_note":"Official Venetian hotel terms and the official poker suite-rate page: $55 plus applicable tax, per night stayed.",
  "room_rate_usd":None,"room_rate_status":"unverified",
  "room_rate_note":"The official page prints poker-suite rates 'as low as $119 and $209' with no stay date attached, so no nightly value is entered. See the rate log.",
  "clark_county_tax_pct":13.38,
  "tax_status":"Verified from the official Venetian hotel terms: Clark County Room Tax 13.38%.",
  "parking":"Complimentary self-parking for non-registered guests who play three hours or more in tournaments or cash games (official poker page).",
  "cancellation_deadline":None,
  "cancellation_note":"No cancellation deadline is printed on the poker suite-rate page. Poker-rate qualification is six hours of live cash play or a $300+ tournament buy-in per night, or the rate is adjusted to the prevailing rate.",
  "sources":[{"label":"Resort fee (official)","url":SRC["venetian_fee"]},
             {"label":"Hotel terms, 13.38% room tax and resort-fee tax (official)","url":SRC["venetian_terms"]},
             {"label":"Poker suite rates and play requirement (official)","url":SRC["venetian_poker_suite"]},
             {"label":"Poker room location and parking (official)","url":"https://www.venetianlasvegas.com/resort/casino/poker.html"}],
  "walk_to_venetian_min":0,"walk_note":"Same building as the poker room (The Palazzo, level 2, Grand Canal Shoppes).","walk_status":"same building"},
 {"id":"palazzo","name":"The Palazzo at The Venetian Resort","venue_id":"venetian",
  "address_note":"3325 S Las Vegas Blvd. The poker room is inside this tower, level 2, Grand Canal Shoppes (official poker page).",
  "resort_fee_usd":55,"resort_fee_status":"verified",
  "resort_fee_note":"Official poker suite-rate page: 'There is a $55 resort fee per night stayed' for The Venetian or The Palazzo.",
  "room_rate_usd":None,"room_rate_status":"unverified",
  "room_rate_note":"Only the conditional poker-suite range ($119 to $209) is published; no Palazzo-specific dated rate.",
  "clark_county_tax_pct":None,
  "tax_status":"Unverified for The Palazzo: the fetched Venetian terms do not separately identify its tax calculation.",
  "parking":"The poker room has direct access to The Palazzo self-parking garage (official poker page).",
  "cancellation_deadline":None,"cancellation_note":"Not printed on the official page read.",
  "sources":[{"label":"Poker suite rates and $55 resort fee (official)","url":SRC["venetian_poker_suite"]},
             {"label":"Poker room location and parking (official)","url":"https://www.venetianlasvegas.com/resort/casino/poker.html"}],
  "walk_to_venetian_min":0,"walk_note":"Same building as the poker room.","walk_status":"same building"},
 {"id":"wynn","name":"Wynn Las Vegas","venue_id":"wynn",
  "address_note":"3131 S Las Vegas Blvd. The Wynn poker room is in Encore at Wynn Las Vegas (official tournament terms).",
  "resort_fee_usd":55,"resort_fee_status":"verified",
  "resort_fee_note":"Official Wynn terms: daily resort fee of $55 plus tax per room night (terms page read by the collector; see the change log).",
  "room_rate_usd":None,"room_rate_status":"unverified",
  "room_rate_note":"No official nightly rate for any stay date was retrieved. Third-party rates are not used.",
  "clark_county_tax_pct":None,"tax_status":"Unverified: no Wynn-specific tax rate was confirmed from official terms.",
  "parking":None,"cancellation_deadline":None,
  "cancellation_note":"Not verified from an official source.",
  "sources":[{"label":"Resort fee terms (official)","url":SRC["wynn_terms"]},
             {"label":"Wynn poker room (official)","url":SRC["wynn_poker"]}],
  "walk_to_wynn_min":0,"walk_note":"Same resort as the Wynn poker room (the room is in Encore at Wynn Las Vegas).","walk_status":"same resort"},
 {"id":"encore","name":"Encore at Wynn Las Vegas","venue_id":"wynn",
  "address_note":"3121 S Las Vegas Blvd. The Wynn poker room is inside this property (official tournament terms).",
  "resort_fee_usd":55,"resort_fee_status":"verified",
  "resort_fee_note":"Official Wynn terms cover 'Wynn and Encore Las Vegas' with a $55 plus tax daily resort fee.",
  "room_rate_usd":None,"room_rate_status":"unverified","room_rate_note":"No official nightly rate confirmed.",
  "clark_county_tax_pct":None,"tax_status":"Unverified: no Encore-specific tax rate confirmed from official terms.",
  "parking":None,"cancellation_deadline":None,"cancellation_note":"Not verified from an official source.",
  "sources":[{"label":"Resort fee terms (official)","url":SRC["wynn_terms"]},
             {"label":"Wynn poker room (official)","url":SRC["wynn_poker"]}],
  "walk_to_wynn_min":0,"walk_note":"Same property as the Wynn poker room.","walk_status":"same resort"},
 {"id":"bellagio","name":"Bellagio","venue_id":None,
  "address_note":"3600 S Las Vegas Blvd. Not the host of a tournament series in this dataset.",
  "resort_fee_usd":None,"resort_fee_status":"unverified",
  "resort_fee_note":"No Bellagio-specific official resort-fee terms were confirmed. Third-party figures conflict, so the value is blank.",
  "room_rate_usd":None,"room_rate_status":"unverified","room_rate_note":"No official nightly rate confirmed.",
  "clark_county_tax_pct":None,"tax_status":"Unverified for Bellagio.",
  "parking":None,"cancellation_deadline":None,"cancellation_note":"Not verified from an official source.",
  "sources":[{"label":"Bellagio official site (property identification only)","url":"https://bellagio.mgmresorts.com/en.html"}],
  "walk_to_venetian_min":None,"walk_note":"Walking time is not published on any official source.","walk_status":"unverified"},
 {"id":"aria","name":"ARIA Resort & Casino","venue_id":None,
  "address_note":"3730 S Las Vegas Blvd. Not the host of a tournament series in this dataset.",
  "resort_fee_usd":None,"resort_fee_status":"unverified",
  "resort_fee_note":"The official ARIA page was fetched by the collector; no resort-fee terms were found on it, so the value is blank.",
  "room_rate_usd":None,"room_rate_status":"unverified","room_rate_note":"No official nightly rate confirmed.",
  "clark_county_tax_pct":None,"tax_status":"Unverified for ARIA.",
  "parking":None,"cancellation_deadline":None,"cancellation_note":"Not verified from an official source.",
  "sources":[{"label":"ARIA official site","url":"https://aria.mgmresorts.com/en.html"}],
  "walk_to_venetian_min":None,"walk_note":"Walking time is not published on any official source.","walk_status":"unverified"},
 {"id":"caesars","name":"Caesars Palace","venue_id":None,
  "address_note":"3570 S Las Vegas Blvd. Not the host of a tournament series in this dataset.",
  "resort_fee_usd":None,"resort_fee_status":"unverified",
  "resort_fee_note":"The official Caesars corporate disclaimer prints a general range of $45 to $50 plus tax, not a property-specific fee, so the value is blank.",
  "room_rate_usd":None,"room_rate_status":"unverified","room_rate_note":"No official nightly rate confirmed.",
  "clark_county_tax_pct":None,"tax_status":"Unverified for Caesars Palace.",
  "parking":None,"cancellation_deadline":None,"cancellation_note":"Not verified from an official source.",
  "sources":[{"label":"Caesars corporate disclaimer (official range)","url":SRC["caesars_disclaimer"]}],
  "walk_to_venetian_min":None,"walk_note":"Walking time is not published on any official source.","walk_status":"unverified"},
]


RATE_LOG = [
  {
    "id": "venetian-poker-suite-2026",
    "hotel_id": "venetian",
    "entry_date": "2026-11-16",
    "property_scope_printed": "The Venetian or The Palazzo",
    "rate_type": "published poker-play suite rate range (not date-specific)",
    "room_type_printed": "Luxury King Suite, single/double occupancy",
    "rate_low_usd": 119,
    "rate_from_high_usd": 209,
    "rate_text": ("'These rates will start as low as $119 and $209 and can be higher.' "
                  "The page attaches no calendar date to either figure and does not say "
                  "which property each figure belongs to."),
    "applies_to_stay_dates": None,
    "blackout_dates": "Blackout dates may apply (none listed).",
    "mandatory_resort_fee_usd": 55,
    "resort_fee_text": "There is a $55 resort fee per night stayed.",
    "room_tax_pct": 13.38,
    "room_tax_text": "Clark County Room Tax 13.38% (official Venetian hotel terms).",
    "room_tax_applies_to_resort_fee": True,
    "resort_fee_tax_text": "$55 resort fee 'plus applicable tax'.",
    "parking": "Complimentary self-parking with three or more hours of play (official poker page).",
    "cancellation_deadline": None,
    "cancellation_text": ("The poker suite-rate page prints no cancellation deadline. It prints "
                          "the play requirement instead: six hours of live cash play or a $300+ "
                          "tournament buy-in per night stayed, or the nightly rate is adjusted "
                          "to the prevailing rate."),
    "qualification_requirement": ("Six hours of active live cash gameplay or a $300 or higher "
                                  "tournament buy-in, per night stayed, completed before 2 a.m. "
                                  "of the last night stayed."),
    "booking_channel": "Call 866.255.8936 and mention code EPOKR25 (printed on the official page).",
    "rate_ceiling_note": "The page says future rates are provided out to a maximum of 150 days from the current date.",
    "official_url": "https://www.venetianlasvegas.com/resort/casino/poker/suite-rates.html",
    "official_url_secondary": "https://www.venetianlasvegas.com/legal/hotel-terms-and-conditions.html",
    "retrieved_utc": None,   # filled from the collector below
    "date_specific": False,
  },
]


def rate_log_with_totals():
    out = []
    for r in RATE_LOG:
        r = dict(r)
        r["retrieved_utc"] = (DOCS.get(r["official_url"], {}).get("fetched_utc")
                              or r["retrieved_utc"] or VERIFIED_ON)
        r["source_changed"] = bool(DOCS.get(r["official_url"], {}).get("changed_since_first_seen"))
        r["true_cost_per_night_usd"] = None
        r["true_cost_note"] = ("Left blank: neither printed figure is attached to a stay date, "
                               "so no like-for-like total can be computed. The stated components "
                               "are room rate + a $55 mandatory resort fee, with 13.38% room tax. "
                               "The arithmetic is (rate + 55) x 1.1338 once a dated rate exists.")
        out.append(r)
    return out


def build_changes():
    path = os.path.join(DATA, "change_log.json")
    if not os.path.exists(path):
        return {"rows": [], "note": "The change log is written by scripts/collect_official.py."}
    log = json.load(open(path, encoding="utf-8"))
    latest = {}
    for rec in log.get("records", []):
        latest[rec["url"]] = rec
    rows = sorted(latest.values(), key=lambda r: r.get("slug") or "")
    return {
        "updated_utc": log.get("updated_utc"),
        "rows": rows,
        "counts": {
            "documents_tracked": len(rows),
            "changed": sum(1 for r in rows if r["status"] == "changed"),
            "unchanged": sum(1 for r in rows if r["status"] == "unchanged"),
            "new": sum(1 for r in rows if r["status"] == "new"),
            "unreachable": sum(1 for r in rows if r["status"] == "unreachable"),
        },
    }


def true_cost(h):
    """Nightly total only when a date-specific rate, fee and property tax are verified."""
    if h["room_rate_usd"] is None or h["resort_fee_usd"] is None or h["clark_county_tax_pct"] is None:
        return None
    return round((h["room_rate_usd"] + h["resort_fee_usd"]) * (1 + h["clark_county_tax_pct"] / 100.0), 2)


def main():
    rows = build_tournaments()
    with open(os.path.join(DATA, "tournaments.json"), "w", encoding="utf-8") as f:
        json.dump({"verified_on": VERIFIED_ON,
                   "facts_generated_utc": FACTS_GENERATED,
                   "facts_present": bool(STRUCTS),
                   "rows": rows, "sources": SRC, "venues": VENUES}, f, indent=1)
    hotels = []
    for h in HOTELS:
        h = dict(h)
        h["true_cost_per_night_usd"] = true_cost(h)
        hotels.append(h)
    with open(os.path.join(DATA, "hotels.json"), "w", encoding="utf-8") as f:
        json.dump({"verified_on": VERIFIED_ON, "rows": hotels,
                   "method": ("True nightly cost is computed only when a date-specific room "
                              "rate, a resort fee, and a property-specific tax rate are all "
                              "verified. No hotel row has a date-specific rate, so every true "
                              "cost is blank. The Venetian terms state a $55 resort fee plus "
                              "applicable tax and a 13.38% Clark County Room Tax; that rate is "
                              "not copied to other properties without property-specific support.")},
                  f, indent=1)
    with open(os.path.join(DATA, "rates.json"), "w", encoding="utf-8") as f:
        json.dump({"verified_on": VERIFIED_ON,
                   "note": ("A dated log, not a single value. Each entry keeps the printed "
                            "text, the official URL, and the retrieval time. A total is "
                            "computed only when the rate is attached to a stay date."),
                   "rows": rate_log_with_totals()}, f, indent=1)
    with open(os.path.join(DATA, "schedule.json"), "w", encoding="utf-8") as f:
        json.dump(build_schedule(rows), f, indent=1)
    with open(os.path.join(DATA, "changes.json"), "w", encoding="utf-8") as f:
        json.dump(build_changes(), f, indent=1)

    counts = {}
    for r in rows:
        counts[r["entry_status"]] = counts.get(r["entry_status"], 0) + 1
    print("total rows", len(rows), "|", counts)
    for s in sorted({r["series"] for r in rows}):
        print("  ", s, sum(1 for r in rows if r["series"] == s))
    print("last_checked range:",
          min(r["last_checked"] for r in rows), "->", max(r["last_checked"] for r in rows))
    print("single entry events:", counts.get("SE", 0))


if __name__ == "__main__":
    main()
