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
    """Return (entry_status, structured rule fields, excerpt, retrieval date)."""
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
        base["note"] = ("Official structure sheet has not been read by the collector, so the "
                        "entry rule is blank and the row is unverified.")
        return "UNV", base, "Official structure sheet not yet read by the collector."

    ex = base["excerpts"]
    kws = facts.get("keywords") or []
    kw_names = sorted({k["keyword"].lower() for k in kws})
    re_hits = [k for k in kws if "re-entr" in k["keyword"].lower()
               or "rebu" in k["keyword"].lower() or "add-on" in k["keyword"].lower()
               or "add on" in k["keyword"].lower() or "multiple entr" in k["keyword"].lower()
               or "subsequent buy" in k["keyword"].lower()]
    flights = [k for k in kws if k["keyword"].lower() == "flights"]
    clause8 = facts.get("clause_08")
    if clause8:
        ex["clause_08"] = clause8
    for k in re_hits[:3]:
        ex["rule_" + str(len(ex))] = k["excerpt"]
    if flights:
        ex["flights"] = flights[0]["excerpt"]

    # Flights: the sheet says a player who bags Day 2 chips may not play another
    # flight. That text only exists if multiple starting flights exist.
    multi_flight = bool(clause8 and re.search(r"bags? chips", clause8, re.I))
    base["flights_offered"] = multi_flight

    if re_hits:
        # An explicit cash-for-entry clause: the label says it is not single entry.
        base["single_entry"] = False
        base["re_entry"] = True
        base["note"] = ("Official sheet prints cash-entry language: '%s'. Treated as not "
                        "single entry." % re_hits[0]["excerpt"][:240])
        return "RE", base, re_hits[0]["excerpt"]

    base["re_entry"] = False
    base["rebuy"] = False
    base["add_on"] = False
    if multi_flight:
        base["single_entry"] = False
        base["entries_allowed"] = "one per starting flight, subject to clause 08"
        base["note"] = ("Official sheet prints clause 08: '%s'. A player who bags chips may not "
                        "play a later flight; the sheet does not say that a player who busts "
                        "may re-enter, so this is not counted as single entry." % clause8[:300])
        return "MULTI", base, clause8

    base["single_entry"] = True
    base["entries_allowed"] = "single entry"
    base["note"] = ("Official sheet read: no re-entry, rebuy, add-on or multi-flight language, "
                    "and no cash-entry clause. Verified single entry.")
    return "SE", base, "No re-entry, rebuy, add-on or flight wording appears on the official sheet."


def classify_wynn(status):
    if status == "RE":
        return "RE", {
            "single_entry": False, "re_entry": True, "rebuy": None, "add_on": None,
            "flights_offered": None, "entries_allowed": "unlimited re-entry until level 9",
            "source_url": SRC["wpt_struct"], "structure_sheet": "WPT_World_Championship_Structures.pdf",
            "retrieved": None, "fetched": False,
            "excerpts": {"re_entry": WPT_RE[1]},
            "note": WPT_RE[1],
        }, WPT_RE[1]
    return "UNV", {
        "single_entry": None, "re_entry": None, "rebuy": None, "add_on": None,
        "flights_offered": None, "entries_allowed": None,
        "source_url": SRC["wpt_struct"], "structure_sheet": None,
        "retrieved": None, "fetched": False, "excerpts": {},
        "note": ("The official WPT structures document has not yet been read by the collector, "
                 "so this row's entry rule is blank and unverified."),
    }, "Official structure document not yet read by the collector."


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
        st, rule, excerpt = classify_wynn(status)
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
DEFAULT_DURATION_MIN = 720   # used only when a finish time is not printed
EXIT_BUFFER_MIN = 30         # time to leave one event and register for the next


def finish_estimate(row):
    """Return (estimated_finish_hhmm, basis). The official sheets print a level
    count but no finish time, so the basis is stated and shown in the UI."""
    facts = STRUCTS.get((row.get("rules") or {}).get("structure_sheet") or "")
    if not facts:
        return None, None
    start = row["start"]
    h, m = int(start[:2]), int(start[3:])
    total = h * 60 + m
    lvl = facts.get("level_minutes")
    levels = facts.get("levels_printed")
    if lvl and levels:
        return "%02d:%02d" % (((total + int(lvl) * int(levels)) // 60) % 24,
                              (total + int(lvl) * int(levels)) % 60), \
               "%s levels x %s minutes, excluding breaks" % (levels, lvl)
    return None, None


def build_schedule(rows):
    """One primary event and one conditional fallback per day.

    Primary = earliest verified single-entry start of the day.
    Fallback = a later verified single-entry event that the primary can
    realistically be abandoned for, i.e. the primary's estimated finish (or the
    documented late-registration close) leaves at least EXIT_BUFFER_MIN before
    the fallback's late registration closes.
    """
    se = [r for r in rows if r["entry_status"] == "SE"]
    by_day = {}
    for r in se:
        by_day.setdefault(r["date"], []).append(r)
    days = []
    for d in sorted(by_day):
        evs = sorted(by_day[d], key=lambda e: e["start"])
        primary = evs[0]
        p_finish, p_basis = finish_estimate(primary)
        options = []
        for e in evs:
            flag = None
            if e is not primary:
                if p_finish:
                    ph, pm = int(p_finish[:2]), int(p_finish[3:])
                    eh, em = int(e["start"][:2]), int(e["start"][3:])
                    gap = (eh * 60 + em) - (ph * 60 + pm)
                    flag = ("ok" if gap >= EXIT_BUFFER_MIN else "conflict")
                else:
                    flag = "unknown"
            options.append({
                "id": e["id"], "start": e["start"], "name": e["name"],
                "series": e["series"], "buy_in_usd": e["buy_in_usd"],
                "guarantee_usd": e["guarantee_usd"], "venue_id": e["venue_id"],
                "entry_status": e["entry_status"],
                "estimated_finish": p_finish if e is primary else None,
                "sequence_check": flag,
                "source": e["sources"][-1]["url"],
            })
        fallback = None
        for o in options[1:]:
            if o["sequence_check"] == "ok":
                fallback = o
                break
        days.append({
            "date": d,
            "primary": options[0],
            "fallback": fallback,
            "conditional_note": (
                None if fallback else
                "No later verified single-entry event is compatible with the primary's "
                "estimated finish. The later event on this day is shown as an alternative, "
                "not as a sequence."),
            "primary_finish_basis": p_basis,
            "options": options,
        })
    starts = sorted({r["start"] for r in rows})
    return {
        "verified_on": VERIFIED_ON,
        "facts_generated_utc": FACTS_GENERATED,
        "days": days,
        "earliest_listed_start": starts[0] if starts else None,
        "exit_buffer_min": EXIT_BUFFER_MIN,
        "duration_default_min": DEFAULT_DURATION_MIN,
        "note": ("Primary = earliest verified single-entry start that day. A fallback is listed "
                 "only when the primary's estimated finish leaves at least %d minutes before the "
                 "fallback starts. Finish times are not printed by the operator; they are "
                 "estimated from the printed level count and level length on the official "
                 "structure sheet and are labelled as estimates. Registration opening times are "
                 "not published, so the 8 AM goal cannot be confirmed from an official source."
                 % EXIT_BUFFER_MIN),
    }


# ------------------------------------------------------------------ hotels --
HOTELS = [
 {"id":"venetian","name":"The Venetian Resort","address_note":"Venetian host property for DeepStack series (official poker page)",
  "resort_fee_usd":55,"resort_fee_status":"verified","resort_fee_note":"Official Venetian hotel terms, read 2026-11-16: $55 plus applicable tax per night.",
  "room_rate_usd":None,"room_rate_status":"unverified","room_rate_note":"Official poker-suite page says rates 'start as low as $119 and $209' (Venetian or Palazzo), conditional on poker play. Which rate applies to which tower is not stated, so no value is entered here.",
  "clark_county_tax_pct":13.38,"tax_status":"Verified from full official Venetian hotel terms read 2026-11-16: Clark County Room Tax 13.38%.",
  "sources":[{"label":"Resort fee (official)","url":SRC["venetian_fee"]},{"label":"Hotel terms incl. 13.38% room tax and resort-fee tax (official)","url":SRC["venetian_terms"]},{"label":"Poker suite rates (official)","url":SRC["venetian_poker_suite"]}],
  "walk_to_venetian_min":None,"walk_note":"Host property. Walking time not applicable (not published)."},
 {"id":"palazzo","name":"The Palazzo","address_note":"Venetian sister property (official poker page names The Palazzo for the $55 fee)",
  "resort_fee_usd":55,"resort_fee_status":"verified","resort_fee_note":"Official Venetian poker-suite page: 'There is a $55 resort fee per night stayed' (stated for The Venetian or The Palazzo).",
  "room_rate_usd":None,"room_rate_status":"unverified","room_rate_note":"Only conditional poker-suite starting rates are published (see Venetian row). No Palazzo-specific rate confirmed.",
  "clark_county_tax_pct":None,"tax_status":"Unverified for Palazzo: the fetched Venetian hotel terms do not separately identify Palazzo's tax calculation.",
  "sources":[{"label":"Poker suite rates incl. $55 resort fee (official)","url":SRC["venetian_poker_suite"]},{"label":"Venetian hotel terms (official; property-specific Palazzo tax not stated)","url":SRC["venetian_terms"]}],
  "walk_to_venetian_min":None,"walk_note":"Unverified: walking time not on an official source."},
 {"id":"wynn","name":"Wynn Las Vegas","address_note":"WPT World Championship and Wynn Signature Series host",
  "resort_fee_usd":55,"resort_fee_status":"verified","resort_fee_note":"Official Wynn terms (search excerpt, not fetched in full): daily resort fee of $55 plus tax per room night.",
  "room_rate_usd":None,"room_rate_status":"unverified","room_rate_note":"No official nightly rate confirmed for any date. Third-party sites quote rates; these are not used.",
  "clark_county_tax_pct":None,"tax_status":"Unverified: no Wynn-specific tax rate was confirmed from official terms.",
  "sources":[{"label":"Resort fee terms (official)","url":SRC["wynn_terms"]},{"label":"Wynn poker room (official)","url":SRC["wynn_poker"]}],
  "walk_to_venetian_min":None,"walk_note":"Unverified: walking time not on an official source."},
 {"id":"encore","name":"Encore at Wynn Las Vegas","address_note":"Same resort operator as Wynn Las Vegas",
  "resort_fee_usd":55,"resort_fee_status":"verified","resort_fee_note":"Official Wynn terms (search excerpt, not fetched in full) cover 'Wynn and Encore Las Vegas' with a $55 plus tax daily resort fee. Confirm for the specific room.",
  "room_rate_usd":None,"room_rate_status":"unverified","room_rate_note":"No official nightly rate confirmed.",
  "clark_county_tax_pct":None,"tax_status":"Unverified: no Encore-specific tax rate was confirmed from official terms.",
  "sources":[{"label":"Resort fee terms (official)","url":SRC["wynn_terms"]}],
  "walk_to_venetian_min":None,"walk_note":"Unverified: walking time not on an official source."},
 {"id":"bellagio","name":"Bellagio","address_note":"MGM Resorts property on the Strip",
  "resort_fee_usd":None,"resort_fee_status":"unverified","resort_fee_note":"No Bellagio-specific official resort-fee terms confirmed. Third-party guides conflict; left blank.",
  "room_rate_usd":None,"room_rate_status":"unverified","room_rate_note":"No official nightly rate confirmed.",
  "clark_county_tax_pct":None,"tax_status":"Unverified for Bellagio: no Bellagio-specific tax rate confirmed from official terms.",
  "sources":[{"label":"Bellagio official home page (property identification; no fee or tax value)","url":"https://bellagio.mgmresorts.com/en.html"}],
  "walk_to_venetian_min":None,"walk_note":"Unverified: walking time not on an official source."},
 {"id":"aria","name":"ARIA Resort & Casino","address_note":"MGM Resorts property on the Strip",
  "resort_fee_usd":None,"resort_fee_status":"unverified","resort_fee_note":"Official ARIA home page fetched; no official resort-fee terms located on it. Left blank.",
  "room_rate_usd":None,"room_rate_status":"unverified","room_rate_note":"No official nightly rate confirmed.",
  "clark_county_tax_pct":None,"tax_status":"Unverified for ARIA: no property-specific tax rate was confirmed from official terms.",
  "sources":[{"label":"ARIA official home page (fetched)","url":"https://aria.mgmresorts.com/en.html"}],
  "walk_to_venetian_min":None,"walk_note":"Unverified: walking time not on an official source."},
 {"id":"caesars","name":"Caesars Palace","address_note":"Caesars Entertainment property",
  "resort_fee_usd":None,"resort_fee_status":"unverified","resort_fee_note":"Official corporate disclaimer gives a general range of $45 to $50 plus applicable tax, not property-specific. Third-party listings conflict. Left blank.",
  "room_rate_usd":None,"room_rate_status":"unverified","room_rate_note":"No official nightly rate confirmed.",
  "clark_county_tax_pct":None,"tax_status":"Unverified for Caesars Palace: no property-specific tax rate was confirmed from official terms.",
  "sources":[{"label":"Caesars corporate disclaimer (official range)","url":SRC["caesars_disclaimer"]}],
  "walk_to_venetian_min":None,"walk_note":"Unverified: walking time not on an official source."},
]


RATE_LOG = [
  {
    "id": "venetian-poker-suite-2026",
    "hotel_id": "venetian",
    "property_scope_printed": "The Venetian or The Palazzo",
    "rate_type": "published poker-play suite rate range",
    "room_type_printed": "Luxury King Suite, single/double occupancy",
    "rate_low_usd": 119,
    "rate_high_from_usd": 209,
    "rate_printed_text": ("'These rates will start as low as $119 and $209 and can be higher.' "
                          "No calendar date is attached to either figure and the page does "
                          "not say which property each figure applies to."),
    "applies_to_dates": None,
    "blackout_dates_printed": "Blackout dates may apply (none listed).",
    "mandatory_resort_fee_usd": 55,
    "resort_fee_text": "There is a $55 resort fee per night stayed.",
    "room_tax_pct": 13.38,
    "room_tax_text": "Clark County Room Tax 13.38% (official Venetian hotel terms).",
    "room_tax_applies_to_resort_fee": True,
    "parking": "Complimentary self-parking for players who play three hours or more "
               "(official poker page).",
    "cancellation_deadline": None,
    "cancellation_note": "The poker-suite page does not print a cancellation deadline. "
                         "It says the poker rate cannot be combined with other promotions "
                         "and requires six hours of live cash play or a $300+ tournament "
                         "buy-in per night stayed, or the rate is adjusted to the "
                         "prevailing rate.",
    "qualification_requirement": "Six hours of active live cash gameplay or a $300 or higher "
                                 "tournament buy-in per night stayed, completed before 2 a.m. "
                                 "of the last night stayed.",
    "booking_channel": "Call 866.255.8936 and mention code EPOKR25 (printed on the official page).",
    "official_url": "https://www.venetianlasvegas.com/resort/casino/poker/suite-rates.html",
    "official_url_secondary": "https://www.venetianlasvegas.com/legal/hotel-terms-and-conditions.html",
    "retrieved_utc": (DOCS.get("https://www.venetianlasvegas.com/resort/casino/poker/suite-rates.html", {}).get("fetched_utc")
                      or VERIFIED_ON),
    "date_specific": False,
  },
]


def rate_log_with_totals():
    rows = []
    for r in RATE_LOG:
        r = dict(r)
        # A true nightly total needs a date-specific rate. A 'from' range is not a
        # date-specific rate, so the total stays blank and the arithmetic is shown.
        r["true_cost_per_night_usd"] = None
        r["true_cost_note"] = ("Not computed: neither printed figure is attached to a stay "
                               "date. The stated components are rate + $55 resort fee, taxed "
                               "at 13.38%. At the printed low figure that arithmetic would be "
                               "(119 + 55) x 1.1338, but the page does not attach $119 to any "
                               "date, so no total is entered.")
        rows.append(r)
    return rows


def build_changes():
    path = os.path.join(DATA, "change_log.json")
    if not os.path.exists(path):
        return {"records": [], "note": "The change log is written by scripts/collect_official.py."}
    log = json.load(open(path, encoding="utf-8"))
    latest = {}
    for rec in log.get("records", []):
        latest[rec["url"]] = rec
    return {
        "updated_utc": log.get("updated_utc"),
        "latest": sorted(latest.values(), key=lambda r: r["slug"]),
        "counts": {
            "documents_tracked": len(latest),
            "changed": sum(1 for r in latest.values() if r["status"] == "changed"),
            "unchanged": sum(1 for r in latest.values() if r["status"] == "unchanged"),
            "new": sum(1 for r in latest.values() if r["status"] == "new"),
            "unreachable": sum(1 for r in latest.values() if r["status"] == "unreachable"),
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
