#!/usr/bin/env python3
"""Builds data/*.json from the verified rows below.

Every row carries the official source URL it was copied from. Nothing is
inferred: a field is left null when the official source does not state it.
Run:  python3 scripts/build_data.py
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
os.makedirs(DATA, exist_ok=True)

VERIFIED_ON = "2026-11-16"
MULTI_FLIGHT_SHEETS = {2, 3, 9, 10, 12, 13, 14}

# ---------- official source URLs (fetched and read on 2026-11-16) ----------
SRC = {
    "dse_nov_sched": "https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/dse-nov-2026-schedule.pdf",
    "dse_nov_page": "https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html",
    "dse_dec_page": "https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-dec-2026.html",
    "dse_nov_struct": "https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_{}.pdf",
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

# ---------- Venetian DeepStack Extravaganza IV (Nov 16 - Dec 23, 2026) ----------
# Fields: date, time, event#, name, buy-in, guarantee, structure sheet # (or None),
#         status, note.  status: SE = single entry verified (sheet read, no re-entry or
#         add-on language), UNV = not verified (sheet not read or wording unclear).
# House fee (from structure sheet) is recorded per sheet in FEE below.
FEE = {  # structure sheet -> (house fee $, buy-in $)  as printed on the sheet
    1: (40, 200), 2: (70, 400), 3: (70, 400), 5: (58, 300), 6: (65, 400),
    7: (90, 600), 8: (40, 200), 9: (60, 300), 10: (60, 300), 11: (90, 600),
    12: (110, 800), 13: (110, 800), 14: (110, 800), 15: (50, 300), 16: (100, 800),
    17: (90, 600),
}
DSE_NOV = [
 ("2026-11-16","11:10",1,"$300 No Limit Hold'em 1A",300,75000,10,"SE","Flight 1A. Day 2 combines 1A-1D at 12:00 PM Nov 18. Late reg closes 3:40 PM."),
 ("2026-11-16","17:10",1,"$300 No Limit Hold'em 1B",300,75000,9,"SE","Flight 1B. Late reg closes 8:40 PM."),
 ("2026-11-17","11:10",1,"$300 No Limit Hold'em 1C",300,75000,10,"SE","Flight 1C."),
 ("2026-11-17","17:10",1,"$300 No Limit Hold'em 1D",300,75000,9,"SE","Flight 1D."),
 ("2026-11-18","11:10",2,"$300 No Limit Hold'em (1Day)",300,10000,5,"SE","Official sheet covers events 02 and 12."),
 ("2026-11-19","10:10",3,"$200 NLH RaceDay Stack (1Day) - race to finish before the race",200,None,None,"UNV","Structure sheet not read."),
 ("2026-11-20","10:10",4,"$200 NLH RaceDay Stack (1Day) - race to finish before the race",200,None,None,"UNV","Structure sheet not read."),
 ("2026-11-21","10:10",5,"$200 NLH RaceDay Stack (1Day) - race to finish before the race",200,None,None,"UNV","Structure sheet not read."),
 ("2026-11-22","11:10",6,"$200 No Limit Hold'em (1Day)",200,None,None,"UNV","Structure sheet not read."),
 ("2026-11-23","11:10",7,"$400 No Limit Hold'em 1A",400,75000,2,"SE","Flight 1A. Day 2 combines 1A-1B at 11:00 AM Nov 25."),
 ("2026-11-23","17:10",8,"$200 No Limit Hold'em PKO Bounty (1Day)",200,8000,None,"UNV","Progressive knockout bounty. Structure sheet not read."),
 ("2026-11-24","11:10",7,"$400 No Limit Hold'em 1B",400,75000,2,"SE","Flight 1B."),
 ("2026-11-24","17:10",9,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"SE","$50 bounty per elimination. Guarantee includes bounties."),
 ("2026-11-25","11:10",10,"$400 No Limit Hold'em (1Day)",400,15000,6,"SE","Late reg closes 4:55 PM."),
 ("2026-11-25","17:10",11,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"SE","Guarantee includes bounties."),
 ("2026-11-26","11:10",12,"$300 No Limit Hold'em (1Day)",300,10000,5,"SE","Late reg closes 4:55 PM."),
 ("2026-11-26","17:10",13,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"SE","Guarantee includes bounties."),
 ("2026-11-27","11:10",14,"$600 No Limit Hold'em (1Day)",600,30000,7,"SE","Late reg closes 4:55 PM."),
 ("2026-11-27","17:10",15,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"SE","Guarantee includes bounties."),
 ("2026-11-28","11:10",16,"$600 No Limit Hold'em Bounty (1Day)",600,30000,11,"SE","$200 bounties to start, $500 once in the money. Guarantee includes bounties."),
 ("2026-11-28","12:10",17,"$400 Pot Limit Omaha Bounty (1Day)",400,15000,None,"UNV","Structure sheet not read."),
 ("2026-11-28","17:10",18,"$200 NLH PokerAtlas Valuetown Bounty (1Day)",200,20000,8,"UNV","Sheet wording says 'subsequent buy-ins after the initial buy-in will be $200'. Re-entry status unclear, so flagged. Guarantee includes bounties."),
 ("2026-11-29","11:10",19,"$400 No Limit Hold'em 1A",400,75000,3,"SE","Flight 1A. Day 2 combines 1A-1C on Dec 2."),
 ("2026-11-29","12:10",20,"$300 Pot Limit Omaha Double Board Bomb Pot (1Day)",300,10000,None,"UNV","Structure sheet not read."),
 ("2026-11-29","17:10",21,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"SE","Guarantee includes bounties."),
 ("2026-11-30","11:10",19,"$400 No Limit Hold'em 1B",400,75000,3,"SE","Flight 1B."),
 ("2026-11-30","17:10",22,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"SE","Guarantee includes bounties."),
 ("2026-12-01","11:10",19,"$400 No Limit Hold'em 1C",400,75000,3,"SE","Flight 1C."),
 ("2026-12-01","17:10",23,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"SE","Guarantee includes bounties."),
 ("2026-12-02","10:10",24,"$600 No Limit Hold'em Seniors (1Day)",600,40000,17,"SE","ELIGIBILITY: must be 50+. Structure says non-50+ buy-ins get no prize money or refund."),
 ("2026-12-02","17:10",25,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"SE","Guarantee includes bounties."),
 ("2026-12-03","11:10",26,"$800 No Limit Hold'em 1A",800,500000,12,"SE","Flight 1A. Day 2 at 12:00 PM Dec 6 combines 1A-1F. Late reg closes 3:40 PM."),
 ("2026-12-03","12:10",27,"$600 Big O (1Day)",600,25000,None,"UNV","Structure sheet not read."),
 ("2026-12-03","17:10",26,"$800 No Limit Hold'em 1B",800,500000,13,"SE","Flight 1B."),
 ("2026-12-04","11:10",26,"$800 No Limit Hold'em 1C",800,500000,12,"SE","Flight 1C."),
 ("2026-12-04","17:10",26,"$800 No Limit Hold'em 1D",800,500000,13,"SE","Flight 1D."),
 ("2026-12-05","11:10",26,"$800 No Limit Hold'em 1E",800,500000,12,"SE","Flight 1E."),
 ("2026-12-05","17:10",26,"$800 No Limit Hold'em 1F (Turbo)",800,500000,14,"SE","Flight 1F (20-minute levels)."),
 ("2026-12-06","11:10",28,"$600 No Limit Hold'em (1Day)",600,40000,7,"SE","Late reg closes 4:55 PM."),
 ("2026-12-06","17:10",29,"$300 No Limit Hold'em Bounty (1Day)",300,15000,15,"SE","$100 bounty per elimination. Guarantee includes bounties."),
 ("2026-12-07","11:10",30,"$600 No Limit Hold'em Bounty (1Day)",600,40000,11,"SE","$200 bounties to start, $500 in the money. Guarantee includes bounties."),
 ("2026-12-07","17:10",31,"$300 No Limit Hold'em Bounty (1Day)",300,15000,15,"SE","Guarantee includes bounties."),
 ("2026-12-08","10:10",32,"$600 No Limit Hold'em Seniors (1Day)",600,40000,17,"SE","ELIGIBILITY: must be 50+."),
 ("2026-12-08","17:10",34,"$300 No Limit Hold'em Bounty (1Day)",300,15000,15,"SE","Guarantee includes bounties."),
 ("2026-12-09","10:10",35,"$600 NLH LIPS Poker Jingle Tag Team (1Day)",600,10000,None,"UNV","Tag-team format (female/female or female/male). Structure sheet not read."),
 ("2026-12-09","11:10",36,"$800 No Limit Hold'em Bounty (1Day)",800,75000,16,"SE","$200 bounties to start, $500 in the money. Guarantee includes bounties."),
 ("2026-12-09","17:10",38,"$300 No Limit Hold'em Bounty (1Day)",300,15000,15,"SE","Guarantee includes bounties."),
 ("2026-12-10","10:10",39,"$800 No Limit Hold'em LIPS Ladies (2Day) - Women in Poker Main Event",800,40000,None,"UNV","Ladies eligibility. Structure sheet not read."),
 ("2026-12-10","12:10",40,"$600 Pot Limit Omaha Bounty (1Day)",600,25000,None,"UNV","Structure sheet not read."),
 ("2026-12-10","17:10",42,"$300 No Limit Hold'em Bounty (1Day)",300,15000,15,"SE","Guarantee includes bounties."),
 ("2026-12-11","11:10",43,"$600 No Limit Hold'em LIPS Kings and Queens Bounty (1Day)",600,30000,None,"UNV","Structure sheet not read."),
 ("2026-12-12","10:10",47,"$2,200 No Limit Hold'em 1A - PokerAtlas Championship Title Event",2200,1000000,None,"UNV","Structure sheet not read."),
 ("2026-12-12","18:10",47,"$2,200 No Limit Hold'em 1B - PokerAtlas Championship Title Event",2200,1000000,None,"UNV","Structure sheet not read."),
 ("2026-12-13","10:10",49,"$1,100 No Limit Hold'em Seniors 1A",1100,300000,None,"UNV","ELIGIBILITY: must be 50+. Date from official event page. Structure sheet not read."),
 ("2026-12-14","10:10",49,"$1,100 No Limit Hold'em Seniors 1B",1100,300000,None,"UNV","ELIGIBILITY: must be 50+. Date from official event page. Structure sheet not read."),
 ("2026-12-13","17:10",50,"$300 No Limit Hold'em Bounty (1Day)",300,15000,15,"SE","Guarantee includes bounties."),
 ("2026-12-14","17:10",51,"$300 No Limit Hold'em Bounty (1Day)",300,15000,15,"SE","Guarantee includes bounties."),
 ("2026-12-15","11:10",52,"$1,100 No Limit Hold'em Progressive Knockout Bounty (1Day)",1100,75000,None,"UNV","PKO format. Structure sheet not read."),
 ("2026-12-15","17:10",53,"$300 No Limit Hold'em Bounty (1Day)",300,15000,15,"SE","Guarantee includes bounties."),
 ("2026-12-16","11:10",54,"$600 No Limit Hold'em Bounty (1Day)",600,50000,11,"SE","$200 bounties to start, $500 in the money. Guarantee includes bounties."),
 ("2026-12-16","17:10",55,"$300 No Limit Hold'em Bounty (1Day)",300,15000,15,"SE","Guarantee includes bounties."),
 ("2026-12-17","10:10",56,"$1,100 No Limit Hold'em 1A",1100,500000,None,"UNV","Flight 1A. Rake discount for entries before 10:10 AM. Structure sheet not read."),
 ("2026-12-17","12:10",57,"$600 Pot Limit Omaha Double Board Bomb Pot (1Day)",600,25000,None,"UNV","Structure sheet not read."),
 ("2026-12-17","18:10",56,"$1,100 No Limit Hold'em 1B",1100,500000,None,"UNV","Flight 1B. Structure sheet not read."),
 ("2026-12-18","10:10",56,"$1,100 No Limit Hold'em 1C",1100,500000,None,"UNV","Flight 1C. Structure sheet not read."),
 ("2026-12-18","18:10",56,"$1,100 No Limit Hold'em 1D",1100,500000,None,"UNV","Flight 1D. Structure sheet not read."),
 ("2026-12-19","10:10",56,"$1,100 No Limit Hold'em 1E",1100,500000,None,"UNV","Flight 1E. Structure sheet not read."),
 ("2026-12-19","17:10",58,"$200 NLH PokerAtlas Valuetown Bounty (1Day)",200,20000,8,"UNV","Date taken from PDF row position (merged date cell). Re-entry wording unclear, flagged."),
 ("2026-12-20","11:10",59,"$600 No Limit Hold'em 1A",600,150000,None,"UNV","Flight 1A. Rake discount before 11:10 AM. Structure sheet not read."),
 ("2026-12-20","17:10",60,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"SE","Guarantee includes bounties."),
 ("2026-12-21","11:10",59,"$600 No Limit Hold'em 1B",600,150000,None,"UNV","Flight 1B. Structure sheet not read."),
 ("2026-12-21","17:10",61,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"SE","Guarantee includes bounties."),
 ("2026-12-22","11:10",59,"$600 No Limit Hold'em 1C",600,150000,None,"UNV","Flight 1C. Structure sheet not read."),
 ("2026-12-22","17:10",62,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"SE","Guarantee includes bounties."),
 ("2026-12-23","11:10",63,"$600 No Limit Hold'em (1Day)",600,30000,7,"SE","Late reg closes 4:55 PM."),
 ("2026-12-23","17:10",64,"$200 No Limit Hold'em Bounty (1Day)",200,8000,1,"SE","Guarantee includes bounties."),
]

# ---------- Venetian DeepStack Extravaganza NYE (Dec 24, 2026 - Jan 10, 2027) ----------
# Buy-in and guarantee from the official event page. No NYE structure sheets were read,
# so every row is UNV for entry rule.
DSE_NYE_PAGE_NOTE = "Buy-in and guarantee from official event page. NYE structure sheet not read."
DSE_NYE = [
 ("2026-12-24","11:10",1,"$400 No Limit Hold'em (1Day)",400,15000,None,"UNV",DSE_NYE_PAGE_NOTE),
 ("2026-12-24","17:10",2,"$200 No Limit Hold'em Bounty (1Day)",200,8000,None,"UNV",DSE_NYE_PAGE_NOTE),
 ("2026-12-25","11:10",3,"$400 No Limit Hold'em (1Day)",400,15000,None,"UNV",DSE_NYE_PAGE_NOTE),
 ("2026-12-25","17:10",4,"$200 No Limit Hold'em Bounty (1Day)",200,8000,None,"UNV",DSE_NYE_PAGE_NOTE),
 ("2026-12-26","11:10",5,"$600 No Limit Hold'em Bounty (1Day)",600,40000,None,"UNV","Official page prints the date as 'Saturday, December 26, 2025'. Year conflicts with the event series, flagged."),
 ("2026-12-27","11:10",8,"$1,100 No Limit Hold'em 1A - Ante Up Championship",1100,300000,None,"UNV",DSE_NYE_PAGE_NOTE),
 ("2026-12-28","11:10",8,"$1,100 No Limit Hold'em 1B - Ante Up Championship",1100,300000,None,"UNV",DSE_NYE_PAGE_NOTE),
 ("2026-12-29","11:10",8,"$1,100 No Limit Hold'em 1C - Ante Up Championship",1100,300000,None,"UNV",DSE_NYE_PAGE_NOTE),
 ("2026-12-29","17:10",13,"$200 No Limit Hold'em Bounty (1Day)",200,8000,None,"UNV",DSE_NYE_PAGE_NOTE),
 ("2026-12-30","11:10",14,"$600 No Limit Hold'em (1Day)",600,50000,None,"UNV",DSE_NYE_PAGE_NOTE),
 ("2026-12-31","11:10",17,"$400 No Limit Hold'em (1Day)",400,15000,None,"UNV",DSE_NYE_PAGE_NOTE),
 ("2027-01-01","11:10",20,"$1,600 No Limit Hold'em MSPT 1A - $40 reduced rake until Level 4",1600,400000,None,"UNV",DSE_NYE_PAGE_NOTE),
 ("2027-01-01","17:10",22,"$200 No Limit Hold'em Bounty (1Day)",200,8000,None,"UNV",DSE_NYE_PAGE_NOTE),
 ("2027-01-02","11:10",20,"$1,600 No Limit Hold'em MSPT 1B",1600,400000,None,"UNV",DSE_NYE_PAGE_NOTE),
 ("2027-01-02","17:10",25,"$200 No Limit Hold'em PokerAtlas Valuetown Bounty (1Day)",200,20000,None,"UNV",DSE_NYE_PAGE_NOTE),
 ("2027-01-03","11:10",20,"$1,600 No Limit Hold'em MSPT 1C",1600,400000,None,"UNV",DSE_NYE_PAGE_NOTE),
 ("2027-01-03","17:10",26,"$200 No Limit Hold'em Bounty (1Day)",200,8000,None,"UNV",DSE_NYE_PAGE_NOTE),
 ("2027-01-04","11:10",27,"$250 No Limit Hold'em 1A (1Day) - $10 reduced rake before 11:10 AM",250,75000,None,"UNV",DSE_NYE_PAGE_NOTE),
 ("2027-01-04","17:10",27,"$250 No Limit Hold'em 1B (1Day)",250,75000,None,"UNV",DSE_NYE_PAGE_NOTE),
 ("2027-01-05","11:10",27,"$250 No Limit Hold'em 1C (1Day)",250,75000,None,"UNV",DSE_NYE_PAGE_NOTE),
 ("2027-01-05","17:10",27,"$250 No Limit Hold'em 1D (1Day)",250,75000,None,"UNV",DSE_NYE_PAGE_NOTE),
 ("2027-01-06","11:10",28,"$400 No Limit Hold'em (1Day)",400,15000,None,"UNV",DSE_NYE_PAGE_NOTE),
 ("2027-01-06","17:10",29,"$200 No Limit Hold'em Bounty (1Day) - CES badge $10 rake discount",200,8000,None,"UNV",DSE_NYE_PAGE_NOTE),
 ("2027-01-07","11:10",30,"$300 No Limit Hold'em 1A (1Day)",300,100000,None,"UNV",DSE_NYE_PAGE_NOTE),
 ("2027-01-07","17:10",30,"$300 No Limit Hold'em 1B (1Day) - CES badge $10 rake discount",300,100000,None,"UNV",DSE_NYE_PAGE_NOTE),
 ("2027-01-08","11:10",30,"$300 No Limit Hold'em 1C (1Day)",300,100000,None,"UNV",DSE_NYE_PAGE_NOTE),
 ("2027-01-08","17:10",30,"$300 No Limit Hold'em 1D (1Day) - CES badge $10 rake discount",300,100000,None,"UNV",DSE_NYE_PAGE_NOTE),
 ("2027-01-09","11:10",30,"$300 No Limit Hold'em 1E (1Day)",300,100000,None,"UNV",DSE_NYE_PAGE_NOTE),
 ("2027-01-09","17:10",30,"$300 No Limit Hold'em 1F (1Day)",300,100000,None,"UNV",DSE_NYE_PAGE_NOTE),
 ("2027-01-10","10:10",31,"$400 No Limit Hold'em Seniors (1Day) - must be 50+",400,20000,None,"UNV","ELIGIBILITY: must be 50+. "+DSE_NYE_PAGE_NOTE),
 ("2027-01-10","17:10",32,"$200 No Limit Hold'em Bounty (1Day)",200,8000,None,"UNV",DSE_NYE_PAGE_NOTE),
]

# ---------- Wynn WPT World Championship (Nov 27 - Dec 21, 2026) ----------
# Source: official WPT schedule PDF. Restart, satellite and Day 2 rows are excluded.
WPT_RE_ENTRY_NOTE = ("Official WPT structure terms: 'Unlimited re-entry for each starting flight ... until the start of level 9.' "
                     "Placed in the separate re-entry section.")
WPT_UNV = "Entry rule not verified: structure sheet for this event not read."
WPT = [
 ("2026-11-27","11:00","NLH Day 1A","$600 NLH $400K",600,400000,"RE",WPT_RE_ENTRY_NOTE),
 ("2026-11-27","12:00","TORSE","TORSE",600,None,"UNV",WPT_UNV),
 ("2026-11-27","13:00","PLO","Pot Limit Omaha",400,None,"UNV",WPT_UNV),
 ("2026-11-27","17:00","NLH Day 1B","$600 NLH $400K",600,400000,"RE",WPT_RE_ENTRY_NOTE),
 ("2026-11-28","11:00","NLH Day 1C","$600 NLH $400K",600,400000,"RE",WPT_RE_ENTRY_NOTE),
 ("2026-11-28","12:00","Mixed Triple Draw (A-5, 2-7, Badugi)","Mixed Triple Draw",600,None,"UNV",WPT_UNV),
 ("2026-11-28","17:00","NLH Day 1D","$600 NLH $400K",600,400000,"RE",WPT_RE_ENTRY_NOTE),
 ("2026-11-29","11:00","NLH Day 1E","$600 NLH $400K",600,400000,"RE",WPT_RE_ENTRY_NOTE),
 ("2026-11-29","18:00","NLH Day 1F","$600 NLH $400K",600,400000,"RE",WPT_RE_ENTRY_NOTE),
 ("2026-11-30","11:00","NLH Day 1A","$800 NLH $1M",800,1000000,"UNV",WPT_UNV),
 ("2026-11-30","12:00","Limit Omaha 8","Limit Omaha 8",600,None,"UNV",WPT_UNV),
 ("2026-11-30","17:00","NLH Day 1B","$800 NLH $1M",800,1000000,"UNV",WPT_UNV),
 ("2026-12-01","11:00","NLH Day 1C","$800 NLH $1M",800,1000000,"UNV",WPT_UNV),
 ("2026-12-01","12:00","Limit Omaha 8/5/Stud 8","Limit Omaha 8/5/Stud 8",600,None,"UNV",WPT_UNV),
 ("2026-12-01","13:00","PLO","Pot Limit Omaha",1100,None,"UNV",WPT_UNV),
 ("2026-12-01","17:00","NLH Day 1D","$800 NLH $1M",800,1000000,"UNV",WPT_UNV),
 ("2026-12-02","11:00","NLH Day 1E","$800 NLH $1M",800,1000000,"UNV",WPT_UNV),
 ("2026-12-02","18:00","NLH Day 1F","$800 NLH $1M",800,1000000,"UNV",WPT_UNV),
 ("2026-12-03","11:00","NLH Day 1A","$1,600 NLH $1M",1600,1000000,"UNV",WPT_UNV),
 ("2026-12-04","11:00","NLH Day 1B","$1,600 NLH $1M",1600,1000000,"UNV",WPT_UNV),
 ("2026-12-04","12:00","HORSE","HORSE",600,None,"UNV",WPT_UNV),
 ("2026-12-05","11:00","WPT Prime Championship Day 1A","WPT Prime Championship $5M",1100,5000000,"UNV",WPT_UNV),
 ("2026-12-05","21:00","NLH Turbo","NLH Turbo $50K",600,50000,"UNV",WPT_UNV),
 ("2026-12-06","11:00","PLO Mystery Bounty Day 1A","PLO Mystery Bounty $500K",1600,500000,"UNV",WPT_UNV),
 ("2026-12-06","11:00","WPT Prime Championship Day 1B","WPT Prime Championship $5M",1100,5000000,"UNV",WPT_UNV),
 ("2026-12-06","18:00","PLO Mystery Bounty Day 1B","PLO Mystery Bounty $500K",1600,500000,"UNV",WPT_UNV),
 ("2026-12-06","21:00","NLH Turbo","NLH Turbo $50K",600,50000,"UNV",WPT_UNV),
 ("2026-12-07","11:00","HORSE (2 Day)","HORSE (2 Day)",1100,None,"UNV",WPT_UNV),
 ("2026-12-07","11:00","WPT Prime Championship Day 1C","WPT Prime Championship $5M",1100,5000000,"UNV",WPT_UNV),
 ("2026-12-07","13:00","PLO $500 Bounty","PLO $500 Bounty $100K",1600,100000,"UNV",WPT_UNV),
 ("2026-12-07","21:00","NLH Turbo","NLH Turbo $50K",600,50000,"UNV",WPT_UNV),
 ("2026-12-08","11:00","WPT Prime Championship Day 1D","WPT Prime Championship $5M",1100,5000000,"UNV",WPT_UNV),
 ("2026-12-08","21:00","NLH Turbo","NLH Turbo $50K",600,50000,"UNV",WPT_UNV),
 ("2026-12-09","11:00","No Limit Hold'em (2 Day)","NLH (2 Day) $1M",1600,1000000,"UNV",WPT_UNV),
 ("2026-12-09","13:00","PLO $1,000 Bounty","PLO $1,000 Bounty $250K",3000,250000,"UNV",WPT_UNV),
 ("2026-12-09","13:00","Limit Omaha 8","Limit Omaha 8",800,None,"UNV",WPT_UNV),
 ("2026-12-09","21:00","NLH Turbo","NLH Turbo $50K",600,50000,"UNV",WPT_UNV),
 ("2026-12-10","10:00","Super Gold Million Mystery Bounty Day 1A","Super Gold Million $3M",400,3000000,"UNV",WPT_UNV),
 ("2026-12-10","18:00","Super Gold Million Mystery Bounty Day 1B","Super Gold Million $3M",400,3000000,"UNV",WPT_UNV),
 ("2026-12-11","10:00","Super Gold Million Mystery Bounty Day 1C","Super Gold Million $3M",400,3000000,"UNV",WPT_UNV),
 ("2026-12-11","18:00","Super Gold Million Mystery Bounty Day 1D","Super Gold Million $3M",400,3000000,"UNV",WPT_UNV),
 ("2026-12-12","10:00","No Limit Hold'em","NLH $100K",800,100000,"UNV",WPT_UNV),
 ("2026-12-12","13:00","PLO","PLO $250K",3000,250000,"UNV",WPT_UNV),
 ("2026-12-12","21:00","NLH Turbo","NLH Turbo $50K",600,50000,"UNV",WPT_UNV),
 ("2026-12-13","11:00","WPT World Championship Day 1A ($1M added)","WPT World Championship",10400,None,"UNV",WPT_UNV + " Official footnote: $1M added by ClubWPT Gold, which the footnote says is not available in Nevada. Flagged."),
 ("2026-12-13","11:00","Ladies NIH Championship (2 Day)","Ladies NIH Championship $250K",1100,250000,"UNV",WPT_UNV + " Printed name reads 'NIH'. Printed buy-in is $1,100 with footnote: 'The Tournament Entry for the Ladies Championship is $11,100. Ladies will receive a discounted entry.' Flagged."),
 ("2026-12-13","11:00","No Limit Hold'em Day 1A","NLH $500K",800,500000,"UNV",WPT_UNV),
 ("2026-12-13","12:00","PLO Day 1A","PLO $1M",1600,1000000,"UNV",WPT_UNV),
 ("2026-12-14","11:00","WPT World Championship Day 1B ($1M added)","WPT World Championship",10400,None,"UNV",WPT_UNV + " Footnote: ClubWPT Gold addition. Flagged."),
 ("2026-12-14","11:00","No Limit Hold'em Day 1B","NLH $500K",800,500000,"UNV",WPT_UNV),
 ("2026-12-14","12:00","PLO Day 1B","PLO $1M",1600,1000000,"UNV",WPT_UNV),
 ("2026-12-14","12:00","Mixed Triple Draw (2 Day)","Mixed Triple Draw (2 Day)",1100,None,"UNV",WPT_UNV),
 ("2026-12-14","19:00","PLO Turbo","PLO Turbo $100K",1100,100000,"UNV",WPT_UNV),
 ("2026-12-14","21:00","NLH Turbo","NLH Turbo $50K",600,50000,"UNV",WPT_UNV),
 ("2026-12-15","11:00","WPT World Championship Day 1C ($1M added)","WPT World Championship",10400,None,"UNV",WPT_UNV + " Footnote: ClubWPT Gold addition. Flagged."),
 ("2026-12-15","12:00","Big O","Big O",1100,None,"UNV",WPT_UNV),
 ("2026-12-15","13:00","PLO Progressive Bounty (PKO)","PLO PKO $250K",3000,250000,"UNV",WPT_UNV),
 ("2026-12-15","19:00","NIH (sic) $500 Bounty Turbo","NLH $500 Bounty Turbo $100K",1600,100000,"UNV",WPT_UNV),
 ("2026-12-17","11:00","Seniors NLH Championship (3 Day)","Seniors NLH $500K",1100,500000,"UNV",WPT_UNV),
 ("2026-12-17","11:00","Wynn Mixed Championship (2 Day)","Wynn Mixed Championship (2 Day)",1600,None,"UNV",WPT_UNV),
 ("2026-12-17","12:00","No Limit Hold'em Day 1A","NLH $2M",3000,2000000,"UNV",WPT_UNV),
 ("2026-12-17","13:00","NLH High Roller (2 Day)","NLH High Roller (2 Day)",25800,None,"UNV",WPT_UNV),
 ("2026-12-18","11:00","No Limit Hold'em Day 1A","NLH $1M",1100,1000000,"UNV",WPT_UNV),
 ("2026-12-18","12:00","PLO Double Board Bomb Pot","PLO Double Board Bomb Pot",800,None,"UNV",WPT_UNV),
 ("2026-12-18","12:00","No Limit Hold'em Day 1B","NLH $2M",3000,2000000,"UNV",WPT_UNV),
 ("2026-12-18","12:00","Limit Omaha 8 Championship (2 Day)","Limit Omaha 8 Championship (2 Day)",1600,None,"UNV",WPT_UNV),
 ("2026-12-18","12:00","No Limit Hold'em","NLH $100K",600,100000,"UNV",WPT_UNV),
 ("2026-12-18","13:00","PLO 6-Max","PLO 6-Max",10500,None,"UNV",WPT_UNV),
 ("2026-12-18","13:00","HORSE","HORSE",800,None,"UNV",WPT_UNV),
 ("2026-12-18","13:00","NLH 6-Max","NLH 6-Max",10500,None,"UNV",WPT_UNV),
 ("2026-12-18","18:00","NLH Turbo","NLH Turbo $100K",1100,100000,"UNV",WPT_UNV),
 ("2026-12-18","19:00","No Limit Hold'em Day 1B","NLH $1M",1100,1000000,"UNV",WPT_UNV),
 ("2026-12-19","11:00","Seniors High Roller (3 Day)","Seniors High Roller $250K",5000,250000,"UNV",WPT_UNV),
 ("2026-12-19","11:00","NLH Mystery Bounty Day 1A","NLH Mystery Bounty $1M",1600,1000000,"UNV",WPT_UNV),
 ("2026-12-19","13:00","PLO","PLO",10500,None,"UNV",WPT_UNV),
 ("2026-12-19","13:00","NLH 6-Max","NLH 6-Max $500K",3000,500000,"UNV",WPT_UNV),
 ("2026-12-19","13:00","TORSE Championship (2 Day)","TORSE Championship (2 Day)",1600,None,"UNV",WPT_UNV),
 ("2026-12-19","18:00","NLH 6-Max Turbo","NLH 6-Max Turbo $50K",600,50000,"UNV",WPT_UNV),
 ("2026-12-19","19:00","NLH Mystery Bounty Day 1B","NLH Mystery Bounty $1M",1600,1000000,"UNV",WPT_UNV),
 ("2026-12-20","11:00","NLH Mystery Bounty Day 1C","NLH Mystery Bounty $1M",1600,1000000,"UNV",WPT_UNV),
 ("2026-12-20","12:00","No Limit Hold'em","NLH $50K",600,50000,"UNV",WPT_UNV),
 ("2026-12-20","13:00","NLH 8-Max","NLH 8-Max",10500,None,"UNV",WPT_UNV),
 ("2026-12-20","13:00","Mixed Triple Draw","Mixed Triple Draw",600,None,"UNV",WPT_UNV),
 ("2026-12-20","18:00","5-Card PLO Turbo","5-Card PLO Turbo $50K",600,50000,"UNV",WPT_UNV),
 ("2026-12-20","19:00","NLH Mystery Bounty Day 1D","NLH Mystery Bounty $1M",1600,1000000,"UNV",WPT_UNV),
 ("2026-12-21","12:00","No Limit Hold'em","NLH $100K",1100,100000,"UNV",WPT_UNV),
 ("2026-12-21","20:00","NLH Turbo","NLH Turbo $50K",600,50000,"UNV",WPT_UNV),
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
WSS_NOTE = "Buy-in and guarantee from official Wynn Signature Series schedule PDF. Structure sheet not read; entry rule not verified."

def build_tournaments():
    rows = []
    def rule_block(status):
        """Structured entry-rule fields for one event, each tied to its source.

        single_entry / re_entry / rebuy / add_on / flights are true, false, or
        None (not confirmed). source_excerpt is the official wording, and
        retrieved_on is the date it was read. Nothing is inferred: an unread
        sheet yields None everywhere.
        """
        if status == "SE":
            return {
                "single_entry": True, "re_entry": False, "rebuy": False,
                "add_on": False, "flights": False,
                "source_excerpt": ("Structure sheet read on %s: no re-entry, rebuy, "
                                   "add-on or flight clause." % VERIFIED_ON),
                "retrieved_on": VERIFIED_ON,
            }
        if status == "MULTI":
            return {
                "single_entry": None, "re_entry": None, "rebuy": None,
                "add_on": None, "flights": True,
                "source_excerpt": ("Clause 08 (read %s): \"Any player who bags chips for "
                                   "Day 2 may not play a subsequent flight.\" Whether a "
                                   "player who busts may enter a later flight is not stated." % VERIFIED_ON),
                "retrieved_on": VERIFIED_ON,
            }
        if status == "RE":
            return {
                "single_entry": False, "re_entry": True, "rebuy": False,
                "add_on": False, "flights": False,
                "source_excerpt": ("Unlimited re-entry for each starting flight until the "
                                   "start of level 9 (official WPT structure terms, read %s)." % VERIFIED_ON),
                "retrieved_on": VERIFIED_ON,
            }
        return {
            "single_entry": None, "re_entry": None, "rebuy": None,
            "add_on": None, "flights": None,
            "source_excerpt": None, "retrieved_on": None,
        }
    def add(series, sched_key, struct_key, r, note_default=None):
        date, time, no, name, buy, gtd, sheet, status, note = r
        # Multi-flight sheets (2, 3, 9, 10, 12, 13, 14) say "Any player who bags chips for Day 2
        # may not play a subsequent flight". That implies a player who busts may play a later
        # flight, which is effectively a second entry. These are not verified single-entry.
        if status == "SE" and sheet in MULTI_FLIGHT_SHEETS:
            status = "MULTI"
        fee = FEE.get(sheet)
        house_fee = fee[0] if fee and sheet else None
        if status == "SE":
            rule = "Single entry (verified): structure sheet read; no re-entry or add-on language."
        elif status == "MULTI":
            rule = ("Possible multiple entries. Structure sheet clause 08 (read 2026-11-16): \"Any player who bags chips for "
                    "Day 2 may not play a subsequent flight.\" The sheet does not say whether players who bust may enter a later flight. Confirm with the poker room.")
        elif status == "RE":
            rule = "Re-entry offered (verified from official structure terms)."
        else:
            rule = "Unverified: entry rule not confirmed from an official structure sheet."
        srcs = [{"label": "Official schedule", "url": SRC[sched_key]}]
        if sheet and struct_key:
            srcs.append({"label": "Structure sheet #%d" % sheet, "url": SRC[struct_key].format(sheet)})
        rows.append({
            "id": "%s-%s-%s" % (series, date, time.replace(":", "")),
            "series": series, "date": date, "start": time, "event_no": no,
            "name": name, "buy_in_usd": buy, "guarantee_usd": gtd,
            "house_fee_usd": house_fee,
            "house_fee_pct": round(100.0 * house_fee / buy, 2) if house_fee else None,
            "gtd_multiple": round(gtd / buy, 1) if gtd and buy else None,
            "entry_status": status, "entry_rule": rule, "note": note,
            "sources": srcs, "verified_on": VERIFIED_ON,
            "last_checked": VERIFIED_ON,
            "rules": rule_block(status),
            "overlap": None,
        })
    for r in DSE_NOV:
        add("Venetian DeepStack Extravaganza IV", "dse_nov_sched", "dse_nov_struct", r)
    for r in DSE_NYE:
        add("Venetian DeepStack Extravaganza NYE", "dse_nov_sched", None, r)
    # NYE rows get the official NYE event page as their source
    for row in rows:
        if row["series"] == "Venetian DeepStack Extravaganza NYE":
            row["sources"] = [{"label": "Official event page", "url": SRC["dse_dec_page"]}]
    for r in WPT:
        date, time, name, label, buy, gtd, status, note = r
        rows.append({
            "id": "WPT-%s-%s-%s" % (date, time.replace(":", ""), label[:12].replace(" ", "")),
            "series": "WPT World Championship (Wynn)", "date": date, "start": time, "event_no": None,
            "name": name + " | " + label, "buy_in_usd": buy, "guarantee_usd": gtd,
            "house_fee_usd": None, "house_fee_pct": None,
            "gtd_multiple": round(gtd / buy, 1) if gtd and buy else None,
            "entry_status": status, "entry_rule": ("Re-entry offered (verified from official structure terms)." if status == "RE"
                                                   else "Unverified: entry rule not confirmed from an official structure sheet."),
            "note": note,
            "sources": [{"label": "Official schedule", "url": SRC["wpt_sched"]},
                        {"label": "Official structures / terms", "url": SRC["wpt_struct"]}] if status == "RE"
                       else [{"label": "Official schedule", "url": SRC["wpt_sched"]}],
            "verified_on": VERIFIED_ON, "last_checked": VERIFIED_ON,
            "rules": rule_block(status), "overlap": None,
        })
    for date, time, name, buy, gtd in WSS:
        rows.append({
            "id": "WSS-%s-%s" % (date, time.replace(":", "")),
            "series": "Wynn Signature Series", "date": date, "start": time, "event_no": None,
            "name": name, "buy_in_usd": buy, "guarantee_usd": gtd,
            "house_fee_usd": None, "house_fee_pct": None,
            "gtd_multiple": round(gtd / buy, 1) if gtd and buy else None,
            "entry_status": "UNV", "entry_rule": "Unverified: entry rule not confirmed from an official structure sheet.",
            "note": WSS_NOTE,
            "sources": [{"label": "Official schedule", "url": SRC["wss_sched"]}],
            "verified_on": VERIFIED_ON, "last_checked": VERIFIED_ON,
            "rules": rule_block("UNV"), "overlap": None,
        })
    rows.sort(key=lambda x: (x["date"], x["start"], x["name"]))
    for i, row in enumerate(rows, 1):
        row["id"] = "r%03d" % i
    return rows

def build_schedule(rows):
    """Per-day list of single-entry (verified) options, plus the earliest start in the sources."""
    days = {}
    for r in rows:
        if r["entry_status"] != "SE":
            continue
        days.setdefault(r["date"], []).append({
            "id": r["id"], "start": r["start"], "series": r["series"], "name": r["name"],
            "buy_in_usd": r["buy_in_usd"], "guarantee_usd": r["guarantee_usd"],
            "source": r["sources"][-1]["url"]})
    out = []
    for d in sorted(days):
        evs = sorted(days[d], key=lambda e: e["start"])
        out.append({"date": d, "options": evs})
    starts = sorted({r["start"] for r in rows})
    return {"verified_on": VERIFIED_ON, "days": out,
            "earliest_listed_start": starts[0],
            "note": ("Earliest start among the rows in this dataset is 10:00 AM (Wynn, Super Gold Million Day 1A, Dec 10). "
                     "Satellites are excluded from the dataset, and one Venetian satellite starts at 9:10 AM. "
                     "Registration opening times are not printed in the schedules read. The schedules print a REG CLOSES time per event.")}

HOTELS = [
 {"id":"venetian","name":"The Venetian Resort","address_note":"Venetian host property for DeepStack series (official poker page)",
  "last_checked":"2026-11-16",
  "resort_fee_usd":55,"resort_fee_status":"verified","resort_fee_note":"Official Venetian hotel terms, read 2026-11-16: $55 plus applicable tax per night.",
  "rates":[],"rates_note":"Dated rate log: each entry is {date, rate_usd, source, retrieved_on, note}. No official date-specific rate has been retrieved for The Venetian, so the log is empty and no true cost per night can be stated yet.",
  "checkout_total_usd":None,"checkout_total_note":None,
  "nightly_average_usd":None,"parking_usd":None,"cancellation_deadline":None,
  "clark_county_tax_pct":13.38,"tax_status":"Verified from full official Venetian hotel terms read 2026-11-16: Clark County Room Tax 13.38%.",
  "sources":[{"label":"Resort fee (official)","url":SRC["venetian_fee"]},{"label":"Hotel terms incl. 13.38% room tax and resort-fee tax (official)","url":SRC["venetian_terms"]},{"label":"Poker suite rates (official)","url":SRC["venetian_poker_suite"]}],
  "walk_to_venetian_min":None,"walk_note":"Host property. Walking time not applicable (not published)."},
 {"id":"palazzo","name":"The Palazzo","address_note":"Venetian sister property (official poker page names The Palazzo for the $55 fee)",
  "last_checked":"2026-11-16",
  "resort_fee_usd":55,"resort_fee_status":"verified","resort_fee_note":"Official Venetian poker-suite page: 'There is a $55 resort fee per night stayed' (stated for The Venetian or The Palazzo).",
  "rates":[],"rates_note":"Dated rate log: each entry is {date, rate_usd, source, retrieved_on, note}. No official date-specific rate has been retrieved for The Palazzo, so the log is empty and no true cost per night can be stated yet.",
  "checkout_total_usd":None,"checkout_total_note":None,
  "nightly_average_usd":None,"parking_usd":None,"cancellation_deadline":None,
  "clark_county_tax_pct":None,"tax_status":"Unverified for Palazzo: the fetched Venetian hotel terms do not separately identify Palazzo's tax calculation.",
  "sources":[{"label":"Poker suite rates incl. $55 resort fee (official)","url":SRC["venetian_poker_suite"]},{"label":"Venetian hotel terms (official; property-specific Palazzo tax not stated)","url":SRC["venetian_terms"]}],
  "walk_to_venetian_min":None,"walk_note":"Unverified: walking time not on an official source."},
 {"id":"wynn","name":"Wynn Las Vegas","address_note":"WPT World Championship and Wynn Signature Series host",
  "last_checked":"2026-11-16",
  "resort_fee_usd":55,"resort_fee_status":"verified","resort_fee_note":"Official Wynn terms (search excerpt, not fetched in full): daily resort fee of $55 plus tax per room night.",
  "rates":[],"rates_note":"Dated rate log: each entry is {date, rate_usd, source, retrieved_on, note}. No official date-specific rate has been retrieved for Wynn Las Vegas, so the log is empty and no true cost per night can be stated yet.",
  "checkout_total_usd":None,"checkout_total_note":None,
  "nightly_average_usd":None,"parking_usd":None,"cancellation_deadline":None,
  "clark_county_tax_pct":None,"tax_status":"Unverified: no Wynn-specific tax rate was confirmed from official terms.",
  "sources":[{"label":"Resort fee terms (official)","url":SRC["wynn_terms"]},{"label":"Wynn poker room (official)","url":SRC["wynn_poker"]}],
  "walk_to_venetian_min":None,"walk_note":"Unverified: walking time not on an official source."},
 {"id":"encore","name":"Encore at Wynn Las Vegas","address_note":"Same resort operator as Wynn Las Vegas",
  "last_checked":"2026-11-16",
  "resort_fee_usd":55,"resort_fee_status":"verified","resort_fee_note":"Official Wynn terms (search excerpt, not fetched in full) cover 'Wynn and Encore Las Vegas' with a $55 plus tax daily resort fee. Confirm for the specific room.",
  "rates":[],"rates_note":"Dated rate log: each entry is {date, rate_usd, source, retrieved_on, note}. No official date-specific rate has been retrieved for Encore, so the log is empty and no true cost per night can be stated yet.",
  "checkout_total_usd":None,"checkout_total_note":None,
  "nightly_average_usd":None,"parking_usd":None,"cancellation_deadline":None,
  "clark_county_tax_pct":None,"tax_status":"Unverified: no Encore-specific tax rate was confirmed from official terms.",
  "sources":[{"label":"Resort fee terms (official)","url":SRC["wynn_terms"]}],
  "walk_to_venetian_min":None,"walk_note":"Unverified: walking time not on an official source."},
 {"id":"bellagio","name":"Bellagio","address_note":"MGM Resorts property on the Strip",
  "last_checked":"2026-11-16",
  "resort_fee_usd":None,"resort_fee_status":"unverified","resort_fee_note":"No Bellagio-specific official resort-fee terms confirmed. Third-party guides conflict; left blank.",
  "rates":[],"rates_note":"Dated rate log: each entry is {date, rate_usd, source, retrieved_on, note}. No official date-specific rate has been retrieved for Bellagio, so the log is empty and no true cost per night can be stated yet.",
  "checkout_total_usd":None,"checkout_total_note":None,
  "nightly_average_usd":None,"parking_usd":None,"cancellation_deadline":None,
  "clark_county_tax_pct":None,"tax_status":"Unverified for Bellagio: no Bellagio-specific tax rate confirmed from official terms.",
  "sources":[{"label":"Bellagio official home page (property identification; no fee or tax value)","url":"https://bellagio.mgmresorts.com/en.html"}],
  "walk_to_venetian_min":None,"walk_note":"Unverified: walking time not on an official source."},
 {"id":"aria","name":"ARIA Resort & Casino","address_note":"MGM Resorts property on the Strip",
  "last_checked":"2026-11-16",
  "resort_fee_usd":None,"resort_fee_status":"unverified","resort_fee_note":"Official ARIA home page fetched; no official resort-fee terms located on it. Left blank.",
  "rates":[],"rates_note":"Dated rate log: each entry is {date, rate_usd, source, retrieved_on, note}. No official date-specific rate has been retrieved for ARIA, so the log is empty and no true cost per night can be stated yet.",
  "checkout_total_usd":None,"checkout_total_note":None,
  "nightly_average_usd":None,"parking_usd":None,"cancellation_deadline":None,
  "clark_county_tax_pct":None,"tax_status":"Unverified for ARIA: no property-specific tax rate was confirmed from official terms.",
  "sources":[{"label":"ARIA official home page (fetched)","url":"https://aria.mgmresorts.com/en.html"}],
  "walk_to_venetian_min":None,"walk_note":"Unverified: walking time not on an official source."},
 {"id":"caesars","name":"Caesars Palace","address_note":"Caesars Entertainment property",
  "last_checked":"2026-11-16",
  "resort_fee_usd":None,"resort_fee_status":"unverified","resort_fee_note":"Official corporate disclaimer gives a general range of $45 to $50 plus applicable tax, not property-specific. Third-party listings conflict. Left blank.",
  "rates":[],"rates_note":"Dated rate log: each entry is {date, rate_usd, source, retrieved_on, note}. No official date-specific rate has been retrieved for Caesars Palace, so the log is empty and no true cost per night can be stated yet.",
  "checkout_total_usd":None,"checkout_total_note":None,
  "nightly_average_usd":None,"parking_usd":None,"cancellation_deadline":None,
  "clark_county_tax_pct":None,"tax_status":"Unverified for Caesars Palace: no property-specific tax rate was confirmed from official terms.",
  "sources":[{"label":"Caesars corporate disclaimer (official range)","url":SRC["caesars_disclaimer"]}],
  "walk_to_venetian_min":None,"walk_note":"Unverified: walking time not on an official source."},
]

def true_cost(h, rate=None):
    """Compute a nightly total for one logged rate when rate, fee, and property-specific
    tax are all verified. Returns None when any input is missing."""
    r = rate if rate is not None else h.get("room_rate_usd")
    if r is None or h.get("resort_fee_usd") is None or h.get("clark_county_tax_pct") is None:
        return None
    return round((r + h["resort_fee_usd"]) * (1 + h["clark_county_tax_pct"] / 100.0), 2)

def main():
    rows = build_tournaments()
    with open(os.path.join(DATA, "tournaments.json"), "w") as f:
        json.dump({"verified_on": VERIFIED_ON, "rows": rows, "sources": SRC}, f, indent=1)
    hotels = []
    for h in HOTELS:
        h = dict(h)
        h["true_cost_per_night_usd"] = true_cost(h)
        hotels.append(h)
    with open(os.path.join(DATA, "hotels.json"), "w") as f:
        json.dump({"verified_on": VERIFIED_ON, "rows": hotels,
                   "method": "True nightly cost is computed only when a date-specific room rate, resort fee, and property-specific tax rate are verified. No current hotel row has all required values. The Venetian terms state a $55 resort fee plus applicable tax and 13.38% Clark County Room Tax; the tax rate is not copied to other hotel rows without property-specific support."}, f, indent=1)
    with open(os.path.join(DATA, "schedule.json"), "w") as f:
        json.dump(build_schedule(rows), f, indent=1)
    se = [r for r in rows if r["entry_status"] == "SE"]
    multi = [r for r in rows if r["entry_status"] == "MULTI"]
    print("MULTI", len(multi))
    re_ = [r for r in rows if r["entry_status"] == "RE"]
    unv = [r for r in rows if r["entry_status"] == "UNV"]
    print("total rows", len(rows), "| SE", len(se), "| RE", len(re_), "| UNV", len(unv))
    for s in sorted({r["series"] for r in rows}):
        print(" ", s, sum(1 for r in rows if r["series"] == s))

if __name__ == "__main__":
    main()
